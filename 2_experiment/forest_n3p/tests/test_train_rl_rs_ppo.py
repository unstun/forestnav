import csv
import json
import os
from pathlib import Path

import numpy as np
import pytest

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from forest_n3p.rl_rs.sb3_policy import (
    RlRsObstacleSummaryExtractor,
    RlRsPatchCnnExtractor,
    RlRsPatchTransformerExtractor,
)
from forest_n3p.scripts.train_bc_policy import _build_scalar_steering_mlp, _policy_features_from_scalar_and_patch
from forest_n3p.scripts.train_rl_rs_ppo import (
    DEFAULT_CONTRACT_PATH,
    _apply_obstacle_summary_bc_warm_start,
    _apply_smoke_overrides,
    _load_reward_config,
    _learning_rate,
    _make_env_factory,
    _parse_args,
    _policy_spec,
    _policy_kwargs,
    _source_head as train_source_head,
    _validate_arg_combination,
    _value_pretrain,
    main as train_rl_rs_ppo_main,
)


BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")
V2_DRAFT_CONTRACT = Path(".pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md")
DENSE_REWARD_CONFIG = Path("2_experiment/configs/module2_encoder_pilot_reward_dense.json")


def test_obstacle_summary_extractor_matches_bc_feature_semantics():
    observation_space = spaces.Dict(
        {
            "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
            "patch": spaces.Box(low=0.0, high=1.0, shape=(2, 5, 5), dtype=np.float32),
        }
    )
    extractor = RlRsObstacleSummaryExtractor(observation_space)
    scalar = np.arange(8, dtype=np.float32)
    patch = np.zeros((2, 5, 5), dtype=np.float32)
    patch[1] = 1.0
    patch[0, 2, 4] = 1.0
    patch[1, 2, 4] = 0.0

    with torch.no_grad():
        features = extractor(
            {
                "scalar": torch.as_tensor(scalar.reshape(1, -1), dtype=torch.float32),
                "patch": torch.as_tensor(patch.reshape(1, 2, 5, 5), dtype=torch.float32),
            }
        ).detach().cpu().numpy()[0]

    expected = _policy_features_from_scalar_and_patch(scalar, patch, feature_mode="obstacle_summary")
    assert features.shape == (29,)
    assert np.allclose(features, expected, atol=1e-6)


def test_train_rl_rs_ppo_smoke_writes_model_manifest_and_episode_csv(tmp_path):
    rc = train_rl_rs_ppo_main(
        [
            "--allow-duplicate-openmp",
            "--smoke",
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )

    assert rc == 0
    assert (tmp_path / "final_model.zip").exists()
    assert (tmp_path / "training_manifest.json").exists()
    assert (tmp_path / "summary.json").exists()

    manifest = json.loads((tmp_path / "training_manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["config"]["smoke"] is True
    assert manifest["config"]["contract"] == DEFAULT_CONTRACT_PATH
    assert manifest["config"]["policy"] == "MultiInputPolicy"
    assert manifest["config"]["reward_config_path"] is None
    assert manifest["config"]["reward_config"]["distance_progress_scale"] == 0.0
    assert manifest["config"]["reward_config"]["clearance_scale"] == 0.0
    assert manifest["config"]["reward_config"]["step_penalty"] == 0.0
    assert "2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py" in manifest["source_hashes"]
    assert any(checkpoint["path"] == "final_model.zip" for checkpoint in manifest["checkpoints"])
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert summary["contract"] == DEFAULT_CONTRACT_PATH

    episode_csv = tmp_path / "episodes_env0.csv"
    rows = list(csv.DictReader(episode_csv.open(newline="", encoding="utf-8")))
    assert rows
    assert {"reward_total", "terminal_rs_success", "rollout_length_m"}.issubset(rows[0])


def test_train_rl_rs_ppo_injects_reward_config_into_step_info(tmp_path):
    args = _parse_args(
        [
            "--smoke",
            "--reward-config",
            str(DENSE_REWARD_CONFIG),
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260707",
        ]
    )
    _apply_smoke_overrides(args)
    reward_config = _load_reward_config(args.reward_config)
    env = _make_env_factory(args=args, output_dir=tmp_path, rank=0, reward_config=reward_config)()
    env.reset(seed=20260707)

    _, _reward, _terminated, _truncated, info = env.step(np.asarray([0.0], dtype=np.float32))
    env.close()

    terms = info["reward_terms"]
    assert terms["progress"] > 0.0
    assert terms["clearance"] > 0.0
    assert terms["step"] == pytest.approx(-0.01)


def test_train_rl_rs_ppo_manifest_records_injected_reward_config(tmp_path):
    rc = train_rl_rs_ppo_main(
        [
            "--allow-duplicate-openmp",
            "--smoke",
            "--reward-config",
            str(DENSE_REWARD_CONFIG),
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260707",
        ]
    )

    assert rc == 0
    manifest = json.loads((tmp_path / "training_manifest.json").read_text(encoding="utf-8"))
    reward_config = manifest["config"]["reward_config"]
    assert manifest["config"]["reward_config_path"] == str(DENSE_REWARD_CONFIG)
    assert reward_config["terminal_rs_success"] == 1.0
    assert reward_config["collision_penalty"] == -1.0
    assert reward_config["terminal_rs_failure_penalty"] == -0.25
    assert reward_config["distance_progress_scale"] == 0.2
    assert reward_config["clearance_scale"] == 0.1
    assert reward_config["step_penalty"] == -0.01


def test_train_rl_rs_ppo_source_head_can_use_env_override(monkeypatch):
    monkeypatch.setenv("FORESTNAV_SOURCE_HEAD", "abc123-pilot")

    assert train_source_head() == "abc123-pilot"


def test_train_rl_rs_ppo_blocks_non_smoke_draft_contract_before_training(tmp_path):
    with pytest.raises(ValueError, match="requires contract status approved or approved_by_dr_sun or frozen"):
        train_rl_rs_ppo_main(
            [
                "--output-dir",
                str(tmp_path),
                "--contract-path",
                str(V2_DRAFT_CONTRACT),
                "--total-timesteps",
                "16",
            ]
        )

    assert not (tmp_path / "summary.json").exists()


def test_obstacle_summary_bc_warm_start_matches_bc_normalized_action(tmp_path):
    args = _parse_args(
        [
            "--smoke",
            "--bc-checkpoint",
            str(BC_CHECKPOINT),
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )
    _apply_smoke_overrides(args)
    env = DummyVecEnv([_make_env_factory(args=args, output_dir=tmp_path, rank=0)])
    model = PPO(
        _policy_spec(args),
        env,
        n_steps=8,
        batch_size=8,
        n_epochs=1,
        policy_kwargs=_policy_kwargs(args),
        seed=20260704,
        verbose=0,
    )

    record = _apply_obstacle_summary_bc_warm_start(model, BC_CHECKPOINT)
    obs = env.reset()
    action, _state = model.predict(obs, deterministic=True)
    expected = _bc_normalized_action(obs)
    model_path = tmp_path / "warm_start_roundtrip.zip"
    model.save(model_path)
    loaded = PPO.load(model_path, device="cpu")
    loaded_action, _loaded_state = loaded.predict(obs, deterministic=True)
    env.close()

    assert record["status"] == "applied_obstacle_summary_bc"
    assert float(action.reshape(-1)[0]) == pytest.approx(expected, abs=1e-5)
    assert float(loaded_action.reshape(-1)[0]) == pytest.approx(expected, abs=1e-5)


def test_patch_cnn_extractor_forward_shape_handles_tiny_patch():
    observation_space = spaces.Dict(
        {
            "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
            "patch": spaces.Box(low=0.0, high=1.0, shape=(2, 5, 5), dtype=np.float32),
        }
    )
    extractor = RlRsPatchCnnExtractor(observation_space, cnn_output_dim=32, scalar_scale=[0.5] * 8)

    with torch.no_grad():
        features = extractor(
            {
                "scalar": torch.ones((3, 8), dtype=torch.float32),
                "patch": torch.rand((3, 2, 5, 5), dtype=torch.float32),
            }
        )

    assert tuple(features.shape) == (3, 40)
    assert torch.allclose(features[:, :8], torch.full((3, 8), 0.5))


def test_train_rl_rs_ppo_patch_cnn_smoke_roundtrip(tmp_path):
    rc = train_rl_rs_ppo_main(
        [
            "--allow-duplicate-openmp",
            "--smoke",
            "--features-extractor",
            "patch_cnn",
            "--cnn-output-dim",
            "16",
            "--lr-schedule",
            "linear",
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )

    assert rc == 0
    manifest = json.loads((tmp_path / "training_manifest.json").read_text(encoding="utf-8"))
    assert manifest["config"]["features_extractor"] == "RlRsPatchCnnExtractor"
    assert manifest["config"]["cnn_output_dim"] == 16
    assert manifest["config"]["lr_schedule"] == "linear"
    assert len(manifest["config"]["scalar_scale"]) == 8

    loaded = PPO.load(tmp_path / "final_model.zip", device="cpu")
    assert type(loaded.policy.features_extractor).__name__ == "RlRsPatchCnnExtractor"


def test_patch_transformer_extractor_forward_shape():
    observation_space = spaces.Dict(
        {
            "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
            "patch": spaces.Box(low=0.0, high=1.0, shape=(2, 64, 64), dtype=np.float32),
        }
    )
    extractor = RlRsPatchTransformerExtractor(observation_space, scalar_scale=[0.5] * 8)

    with torch.no_grad():
        features = extractor(
            {
                "scalar": torch.ones((3, 8), dtype=torch.float32),
                "patch": torch.rand((3, 2, 64, 64), dtype=torch.float32),
            }
        )

    assert tuple(features.shape) == (3, 264)
    assert torch.allclose(features[:, :8], torch.full((3, 8), 0.5))


def test_patch_transformer_extractor_handles_tiny_patch():
    observation_space = spaces.Dict(
        {
            "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
            "patch": spaces.Box(low=0.0, high=1.0, shape=(2, 5, 5), dtype=np.float32),
        }
    )
    extractor = RlRsPatchTransformerExtractor(observation_space)

    with torch.no_grad():
        features = extractor(
            {
                "scalar": torch.ones((3, 8), dtype=torch.float32),
                "patch": torch.rand((3, 2, 5, 5), dtype=torch.float32),
            }
        )

    assert tuple(features.shape) == (3, 264)


def test_patch_transformer_param_count_below_two_million():
    observation_space = spaces.Dict(
        {
            "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
            "patch": spaces.Box(low=0.0, high=1.0, shape=(2, 64, 64), dtype=np.float32),
        }
    )
    extractor = RlRsPatchTransformerExtractor(observation_space)

    assert sum(parameter.numel() for parameter in extractor.parameters()) < 2_000_000


def test_patch_cnn_rejects_obstacle_summary_bc_checkpoint():
    args = _parse_args(["--features-extractor", "patch_cnn", "--bc-checkpoint", str(BC_CHECKPOINT)])
    with pytest.raises(ValueError, match="incompatible with --bc-checkpoint"):
        _validate_arg_combination(args)


def test_patch_transformer_rejects_obstacle_summary_bc_checkpoint():
    args = _parse_args(["--features-extractor", "transformer", "--bc-checkpoint", str(BC_CHECKPOINT)])
    with pytest.raises(ValueError, match="transformer is incompatible with --bc-checkpoint"):
        _validate_arg_combination(args)


def test_value_pretrain_requires_bc_checkpoint():
    args = _parse_args(["--value-pretrain-timesteps", "8"])
    with pytest.raises(ValueError, match="requires --bc-checkpoint"):
        _validate_arg_combination(args)


def test_value_pretrain_freezes_actor_and_updates_critic(tmp_path):
    args = _parse_args(
        [
            "--smoke",
            "--bc-checkpoint",
            str(BC_CHECKPOINT),
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )
    _apply_smoke_overrides(args)
    env = DummyVecEnv([_make_env_factory(args=args, output_dir=tmp_path, rank=0)])
    model = PPO(
        _policy_spec(args),
        env,
        n_steps=8,
        batch_size=8,
        n_epochs=1,
        policy_kwargs=_policy_kwargs(args),
        seed=20260704,
        verbose=0,
    )
    _apply_obstacle_summary_bc_warm_start(model, BC_CHECKPOINT)
    actor_before = {name: param.detach().clone() for name, param in model.policy.action_net.named_parameters()}
    critic_before = {name: param.detach().clone() for name, param in model.policy.value_net.named_parameters()}

    _value_pretrain(model, timesteps=8)
    env.close()

    for name, param in model.policy.action_net.named_parameters():
        assert torch.equal(param.detach(), actor_before[name]), f"actor parameter {name} changed during value pretrain"
    assert any(
        not torch.equal(param.detach(), critic_before[name])
        for name, param in model.policy.value_net.named_parameters()
    ), "critic parameters did not update during value pretrain"
    assert all(param.requires_grad for param in model.policy.parameters())


def test_value_pretrain_rebuilds_positive_optimizer_lr_after_linear_schedule(tmp_path):
    args = _parse_args(
        [
            "--smoke",
            "--bc-checkpoint",
            str(BC_CHECKPOINT),
            "--lr-schedule",
            "linear",
            "--learning-rate",
            "0.0001",
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )
    _apply_smoke_overrides(args)
    env = DummyVecEnv([_make_env_factory(args=args, output_dir=tmp_path, rank=0)])
    model = PPO(
        _policy_spec(args),
        env,
        learning_rate=_learning_rate(args),
        n_steps=8,
        batch_size=8,
        n_epochs=1,
        policy_kwargs=_policy_kwargs(args),
        seed=20260704,
        verbose=0,
    )
    _apply_obstacle_summary_bc_warm_start(model, BC_CHECKPOINT)

    _value_pretrain(model, timesteps=8)
    env.close()

    assert model.policy.optimizer.param_groups[0]["lr"] == pytest.approx(0.0001)


def _bc_normalized_action(obs) -> float:
    checkpoint = torch.load(BC_CHECKPOINT, map_location="cpu", weights_only=False)
    bc_model = _build_scalar_steering_mlp(
        torch=torch,
        input_dim=int(checkpoint["input_dim"]),
        hidden_dims=tuple(int(value) for value in checkpoint["hidden_dims"]),
        max_steer=float(checkpoint["max_steer"]),
    )
    bc_model.load_state_dict(checkpoint["state_dict"])
    bc_model.eval()
    features = _policy_features_from_scalar_and_patch(
        obs["scalar"][0],
        obs["patch"][0],
        feature_mode="obstacle_summary",
    )
    normalized = (features - np.asarray(checkpoint["feature_mean"], dtype=np.float32)) / np.asarray(checkpoint["feature_std"], dtype=np.float32)
    with torch.no_grad():
        physical = float(bc_model(torch.as_tensor(normalized.reshape(1, -1), dtype=torch.float32)).detach().cpu().numpy()[0, 0])
    return physical / float(checkpoint["max_steer"])
