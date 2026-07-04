import csv
import json
import os
from pathlib import Path

import numpy as np

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from forest_n3p.rl_rs.sb3_policy import RlRsObstacleSummaryExtractor
from forest_n3p.scripts.train_bc_policy import _build_scalar_steering_mlp, _policy_features_from_scalar_and_patch
from forest_n3p.scripts.train_rl_rs_ppo import (
    _apply_obstacle_summary_bc_warm_start,
    _apply_smoke_overrides,
    _make_env_factory,
    _parse_args,
    _policy_kwargs,
    main as train_rl_rs_ppo_main,
)


BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")


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
    assert manifest["config"]["policy"] == "MultiInputPolicy"
    assert "2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py" in manifest["source_hashes"]
    assert any(checkpoint["path"] == "final_model.zip" for checkpoint in manifest["checkpoints"])

    episode_csv = tmp_path / "episodes_env0.csv"
    rows = list(csv.DictReader(episode_csv.open(newline="", encoding="utf-8")))
    assert rows
    assert {"reward_total", "terminal_rs_success", "rollout_length_m"}.issubset(rows[0])


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
        "MultiInputPolicy",
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
    env.close()

    assert record["status"] == "applied_obstacle_summary_bc"
    assert float(action.reshape(-1)[0]) == pytest_approx(expected, abs=1e-5)


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


def pytest_approx(value: float, *, abs: float):
    import pytest

    return pytest.approx(value, abs=abs)
