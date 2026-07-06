from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from forest_n3p.rl_rs.curriculum import (
    CurriculumContextConfig,
    ObstacleBypassContextSampler,
    OpenConnectorContextSampler,
    make_f03_curriculum_sampler,
)
from forest_n3p.rl_rs.gym_env import GymAnalyticExpansionEnv
from forest_n3p.rl_rs.obs import ObservationConfig
from forest_n3p.rl_rs.reward import RewardConfig, reward_config_from_mapping, reward_config_to_record
from forest_n3p.rl_rs.training_logging import RlRsEpisodeLoggingWrapper, file_sha256, write_training_manifest
from forest_n3p.scripts._module2_contract_gate import require_contract_ready


DEFAULT_CONTRACT_PATH = ".pipeline/contracts/module2-ppo-funnel-expansion.md"


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    if bool(args.allow_duplicate_openmp):
        os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    _apply_smoke_overrides(args)
    _validate_arg_combination(args)
    contract_status = require_contract_ready(
        args.contract_path,
        allow_unapproved=bool(args.smoke),
        context="Module2 PPO training",
    )
    reward_config = _load_reward_config(args.reward_config)
    PPO, CallbackList, CheckpointCallback, DummyVecEnv = _load_sb3()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = _config_record(args=args, raw_argv=raw_argv, contract_status=contract_status, reward_config=reward_config)
    env = DummyVecEnv([
        _make_env_factory(args=args, output_dir=output_dir, rank=rank, reward_config=reward_config)
        for rank in range(int(args.n_envs))
    ])
    callbacks = _callbacks(args=args, output_dir=output_dir, n_envs=int(args.n_envs), CallbackList=CallbackList, CheckpointCallback=CheckpointCallback)
    model = PPO(
        _policy_spec(args),
        env,
        learning_rate=_learning_rate(args),
        n_steps=int(args.n_steps),
        batch_size=int(args.batch_size),
        n_epochs=int(args.n_epochs),
        gamma=float(args.gamma),
        gae_lambda=float(args.gae_lambda),
        clip_range=float(args.clip_range),
        ent_coef=float(args.ent_coef),
        vf_coef=float(args.vf_coef),
        max_grad_norm=float(args.max_grad_norm),
        policy_kwargs=_policy_kwargs(args),
        tensorboard_log=str(args.tensorboard_log) if args.tensorboard_log else None,
        seed=int(args.seed),
        device=str(args.device),
        verbose=int(args.verbose),
    )
    warm_start = _apply_obstacle_summary_bc_warm_start(model, args.bc_checkpoint) if args.bc_checkpoint else _no_warm_start_record()
    config["warm_start"] = warm_start
    config["warm_start_status"] = warm_start["status"]
    try:
        if int(args.value_pretrain_timesteps) > 0:
            _value_pretrain(model, timesteps=int(args.value_pretrain_timesteps))
        model.learn(total_timesteps=int(args.total_timesteps), callback=callbacks)
        final_model_path = output_dir / "final_model.zip"
        model.save(final_model_path)
    finally:
        env.close()

    checkpoints = _checkpoint_records(output_dir)
    manifest_path = write_training_manifest(
        output_dir,
        config=config,
        source_hashes=_source_hashes(),
        checkpoints=checkpoints,
        command=config["command"],
    )
    summary = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "contract": str(args.contract_path),
        "contract_status": str(contract_status),
        "output_dir": str(output_dir),
        "manifest": str(manifest_path),
        "final_model": "final_model.zip",
        "checkpoint_count": int(len(checkpoints)),
        "warm_start_status": warm_start["status"],
        "config": config,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a Module2 RL-RS PPO analytic-expansion policy.")
    parser.add_argument("--output-dir", type=Path, default=Path("2_experiment/forest_n3p/models/module2_rl_rs_ppo_f03"))
    parser.add_argument("--contract-path", default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--seed", type=int, default=20260704)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--allow-duplicate-openmp", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="Run a tiny open-connector training smoke.")
    parser.add_argument("--bc-checkpoint", type=Path, default=None, help="Optional F02 obstacle-summary BC checkpoint for PPO actor initialization.")
    parser.add_argument("--reward-config", type=Path, default=None, help="Optional JSON RewardConfig override; omitted keeps sparse defaults.")
    parser.add_argument(
        "--features-extractor",
        choices=("summary", "patch_cnn"),
        default="summary",
        help="summary: 21-dim hand-pooled region statistics (F02 legacy); patch_cnn: full-patch CNN encoder.",
    )
    parser.add_argument("--cnn-output-dim", type=int, default=256, help="CNN feature dimension for --features-extractor patch_cnn.")
    parser.add_argument(
        "--lr-schedule",
        choices=("constant", "linear"),
        default="constant",
        help="linear anneals the learning rate from --learning-rate to 0 over training.",
    )
    parser.add_argument(
        "--value-pretrain-timesteps",
        type=int,
        default=0,
        help="Freeze the warm-started actor and train only the value function for this many timesteps before PPO (requires --bc-checkpoint).",
    )
    parser.add_argument("--curriculum-preset", choices=("open", "obstacle", "f03"), default="f03")
    parser.add_argument("--oracle-path", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--heldout-seed", type=int, default=20260704)
    parser.add_argument("--n-envs", type=int, default=1)
    parser.add_argument("--total-timesteps", type=int, default=100_000)
    parser.add_argument("--n-steps", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--n-epochs", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--gae-lambda", type=float, default=0.95)
    parser.add_argument("--clip-range", type=float, default=0.2)
    parser.add_argument("--ent-coef", type=float, default=0.0)
    parser.add_argument("--vf-coef", type=float, default=0.5)
    parser.add_argument("--max-grad-norm", type=float, default=0.5)
    parser.add_argument("--policy-net-arch", default="128,128,64")
    parser.add_argument("--value-net-arch", default="128,128,64")
    parser.add_argument("--tensorboard-log", type=Path, default=None)
    parser.add_argument("--checkpoint-freq", type=int, default=10_000)
    parser.add_argument("--verbose", type=int, default=0)
    parser.add_argument("--obs-patch-size-m", type=float, default=6.4)
    parser.add_argument("--obs-patch-cells", type=int, default=64)
    parser.add_argument("--obs-include-edt", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--obs-edt-clip-m", type=float, default=2.0)
    parser.add_argument("--max-steps", type=int, default=32)
    parser.add_argument("--action-step-m", type=float, default=0.3)
    parser.add_argument("--collision-sample-step-m", type=float, default=0.1)
    parser.add_argument("--terminal-check-every", type=int, default=1)
    parser.add_argument("--theta-bins", type=int, default=72)
    return parser.parse_args(list(argv))


def _apply_smoke_overrides(args: argparse.Namespace) -> None:
    if not bool(args.smoke):
        return
    args.curriculum_preset = "open"
    args.n_envs = 1
    args.total_timesteps = 16
    args.n_steps = 8
    args.batch_size = 8
    args.n_epochs = 1
    args.checkpoint_freq = 0
    args.obs_patch_size_m = 0.4
    args.obs_patch_cells = 5
    args.max_steps = 4
    args.verbose = 0


def _validate_arg_combination(args: argparse.Namespace) -> None:
    if str(args.features_extractor) == "patch_cnn" and args.bc_checkpoint is not None:
        raise ValueError(
            "--features-extractor patch_cnn is incompatible with --bc-checkpoint: "
            "the F02 BC checkpoint encodes obstacle-summary features, not CNN features."
        )
    if int(args.value_pretrain_timesteps) > 0 and args.bc_checkpoint is None:
        raise ValueError("--value-pretrain-timesteps requires --bc-checkpoint (it exists to protect a warm-started actor).")
    if int(args.value_pretrain_timesteps) < 0:
        raise ValueError("--value-pretrain-timesteps must be non-negative")


def _learning_rate(args: argparse.Namespace):
    lr = float(args.learning_rate)
    if str(args.lr_schedule) == "constant":
        return lr

    def _linear_schedule(progress_remaining: float) -> float:
        return lr * float(progress_remaining)

    return _linear_schedule


def _value_pretrain(model: Any, *, timesteps: int) -> None:
    """Train only the value function while the (warm-started) actor stays frozen.

    JSRL-style guard: a randomly initialized critic emits a poor learning signal
    that degrades a BC-initialized actor during early PPO updates, so the critic
    is fitted first under the frozen actor's own state distribution.
    """
    frozen = _actor_parameters(model.policy)
    for parameter in frozen:
        parameter.requires_grad_(False)
    try:
        model.learn(total_timesteps=int(timesteps), reset_num_timesteps=True)
    finally:
        for parameter in frozen:
            parameter.requires_grad_(True)
        _rebuild_policy_optimizer(model.policy)


def _actor_parameters(policy: Any) -> list[Any]:
    parameters = list(policy.mlp_extractor.policy_net.parameters())
    parameters.extend(policy.action_net.parameters())
    log_std = getattr(policy, "log_std", None)
    if log_std is not None:
        parameters.append(log_std)
    return parameters


def _load_sb3():
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback
    from stable_baselines3.common.vec_env import DummyVecEnv

    return PPO, CallbackList, CheckpointCallback, DummyVecEnv


def _policy_spec(args: argparse.Namespace):
    if args.bc_checkpoint is None:
        return "MultiInputPolicy"
    from forest_n3p.rl_rs.sb3_policy import RlRsMultiInputPolicy

    return RlRsMultiInputPolicy


def _load_reward_config(path: Path | None) -> RewardConfig:
    if path is None:
        return RewardConfig()
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("--reward-config must point to a JSON object")
    return reward_config_from_mapping(raw)


def _make_env_factory(*, args: argparse.Namespace, output_dir: Path, rank: int, reward_config: RewardConfig | None = None):
    def _factory():
        cfg = _curriculum_config(args, reward_config=reward_config)
        sampler = _sampler(args, cfg=cfg)
        env = GymAnalyticExpansionEnv(sampler, observation_config=cfg.observation_config)
        csv_path = output_dir / f"episodes_env{int(rank)}.csv"
        return RlRsEpisodeLoggingWrapper(env, csv_path=csv_path)

    return _factory


def _curriculum_config(args: argparse.Namespace, *, reward_config: RewardConfig | None = None) -> CurriculumContextConfig:
    obs_config = ObservationConfig(
        patch_size_m=float(args.obs_patch_size_m),
        patch_cells=int(args.obs_patch_cells),
        include_edt=bool(args.obs_include_edt),
        edt_clip_m=float(args.obs_edt_clip_m),
    )
    return CurriculumContextConfig(
        max_steps=int(args.max_steps),
        action_step_m=float(args.action_step_m),
        collision_sample_step_m=float(args.collision_sample_step_m),
        terminal_check_every=int(args.terminal_check_every),
        theta_bins=int(args.theta_bins),
        observation_config=obs_config,
        reward_config=reward_config or RewardConfig(),
    )


def _sampler(args: argparse.Namespace, *, cfg: CurriculumContextConfig):
    if str(args.curriculum_preset) == "open":
        return OpenConnectorContextSampler(config=cfg)
    if str(args.curriculum_preset) == "obstacle":
        return ObstacleBypassContextSampler(config=cfg)
    return make_f03_curriculum_sampler(oracle_path=args.oracle_path, heldout_seed=int(args.heldout_seed), config=cfg)


def _policy_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    import torch
    from forest_n3p.rl_rs.sb3_policy import RlRsObstacleSummaryExtractor, RlRsPatchCnnExtractor

    kwargs = {
        "activation_fn": torch.nn.ReLU,
        "net_arch": {
            "pi": list(_parse_ints(str(args.policy_net_arch))),
            "vf": list(_parse_ints(str(args.value_net_arch))),
        },
    }
    if str(args.features_extractor) == "patch_cnn":
        kwargs["features_extractor_class"] = RlRsPatchCnnExtractor
        kwargs["features_extractor_kwargs"] = {
            "cnn_output_dim": int(args.cnn_output_dim),
            "scalar_scale": _scalar_scale(args),
        }
    else:
        kwargs["features_extractor_class"] = RlRsObstacleSummaryExtractor
    if args.bc_checkpoint is not None:
        kwargs["use_tanh_action_head"] = True
    return kwargs


def _scalar_scale(args: argparse.Namespace) -> list[float]:
    """Fixed scaling for the 8 scalar features (dx, dy, distance, 4 already-bounded
    trig terms, remaining_steps) so the CNN policy sees O(1) inputs without a
    VecNormalize statistics file to keep in sync at evaluation time."""
    distance_scale = 1.0 / max(float(args.obs_patch_size_m), 1e-6)
    steps_scale = 1.0 / max(float(args.max_steps), 1.0)
    return [distance_scale, distance_scale, distance_scale, 1.0, 1.0, 1.0, 1.0, steps_scale]


def _apply_obstacle_summary_bc_warm_start(model: Any, checkpoint_path: Path) -> dict[str, Any]:
    import torch
    from forest_n3p.rl_rs.sb3_policy import TanhLinearActionHead

    path = Path(checkpoint_path)
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    _validate_bc_checkpoint(checkpoint, path)
    state_dict = checkpoint["state_dict"]
    hidden_dims = tuple(int(value) for value in checkpoint["hidden_dims"])
    policy_layers = [module for module in model.policy.mlp_extractor.policy_net if isinstance(module, torch.nn.Linear)]
    if len(policy_layers) != len(hidden_dims):
        raise ValueError(f"BC hidden_dims {hidden_dims} do not match PPO policy_net {len(policy_layers)} linear layers")
    for idx, (layer, expected_out) in enumerate(zip(policy_layers, hidden_dims, strict=True)):
        if int(layer.out_features) != int(expected_out):
            raise ValueError(f"BC hidden layer {idx} out_features {expected_out} does not match PPO policy layer")
        key = f"net.{2 * idx}"
        weight = state_dict[f"{key}.weight"]
        bias = state_dict[f"{key}.bias"]
        if tuple(layer.weight.shape) != tuple(weight.shape) or tuple(layer.bias.shape) != tuple(bias.shape):
            raise ValueError(f"BC layer {key} shape does not match PPO policy layer {idx}")
        layer.weight.data.copy_(weight.to(device=layer.weight.device, dtype=layer.weight.dtype))
        layer.bias.data.copy_(bias.to(device=layer.bias.device, dtype=layer.bias.dtype))

    old_action_net = model.policy.action_net
    if isinstance(old_action_net, TanhLinearActionHead):
        action_head = old_action_net
    else:
        action_head = TanhLinearActionHead(old_action_net.in_features, old_action_net.out_features).to(old_action_net.weight.device)
    action_key = f"net.{2 * len(hidden_dims)}"
    final_weight = state_dict[f"{action_key}.weight"]
    final_bias = state_dict[f"{action_key}.bias"]
    if tuple(action_head.linear.weight.shape) != tuple(final_weight.shape) or tuple(action_head.linear.bias.shape) != tuple(final_bias.shape):
        raise ValueError("BC final action layer shape does not match PPO action head")
    action_head.linear.weight.data.copy_(final_weight.to(device=action_head.linear.weight.device, dtype=action_head.linear.weight.dtype))
    action_head.linear.bias.data.copy_(final_bias.to(device=action_head.linear.bias.device, dtype=action_head.linear.bias.dtype))
    model.policy.action_net = action_head
    _set_feature_normalization(model.policy, checkpoint["feature_mean"], checkpoint["feature_std"])
    _persist_feature_normalization(model, checkpoint["feature_mean"], checkpoint["feature_std"])
    _rebuild_policy_optimizer(model.policy)
    return {
        "status": "applied_obstacle_summary_bc",
        "checkpoint": str(path),
        "checkpoint_sha256": file_sha256(path),
        "feature_mode": str(checkpoint["feature_mode"]),
        "model_type": str(checkpoint["model_type"]),
        "hidden_dims": list(hidden_dims),
        "max_steer": float(checkpoint["max_steer"]),
        "action_head": "TanhLinearActionHead",
    }


def _validate_bc_checkpoint(checkpoint: dict[str, Any], path: Path) -> None:
    required = {"model_type", "state_dict", "input_dim", "hidden_dims", "max_steer", "feature_mode", "feature_mean", "feature_std"}
    missing = sorted(required.difference(checkpoint))
    if missing:
        raise ValueError(f"BC checkpoint {path} missing keys: {missing}")
    if str(checkpoint["feature_mode"]) != "obstacle_summary":
        raise ValueError("Only obstacle_summary BC checkpoints are supported for PPO warm-start.")
    if int(checkpoint["input_dim"]) != 29:
        raise ValueError("Obstacle-summary PPO warm-start requires 29 input features.")


def _set_feature_normalization(policy: Any, feature_mean: Sequence[float], feature_std: Sequence[float]) -> None:
    import torch

    for attr in ("features_extractor", "pi_features_extractor", "vf_features_extractor"):
        extractor = getattr(policy, attr, None)
        if extractor is None or not hasattr(extractor, "_feature_mean") or not hasattr(extractor, "_feature_std"):
            continue
        mean = torch.as_tensor(feature_mean, dtype=extractor._feature_mean.dtype, device=extractor._feature_mean.device).reshape(-1)
        std = torch.as_tensor(feature_std, dtype=extractor._feature_std.dtype, device=extractor._feature_std.device).reshape(-1).clamp_min(1e-6)
        if tuple(mean.shape) != tuple(extractor._feature_mean.shape) or tuple(std.shape) != tuple(extractor._feature_std.shape):
            raise ValueError("BC feature normalization shape does not match PPO feature extractor")
        extractor._feature_mean.data.copy_(mean)
        extractor._feature_std.data.copy_(std)
        extractor._has_normalization = True


def _persist_feature_normalization(model: Any, feature_mean: Sequence[float], feature_std: Sequence[float]) -> None:
    kwargs = dict(getattr(model, "policy_kwargs", {}) or {})
    kwargs["features_extractor_kwargs"] = {
        "feature_mean": [float(value) for value in feature_mean],
        "feature_std": [float(value) for value in feature_std],
    }
    model.policy_kwargs = kwargs
    if hasattr(model.policy, "features_extractor_kwargs"):
        model.policy.features_extractor_kwargs = dict(kwargs["features_extractor_kwargs"])


def _rebuild_policy_optimizer(policy: Any) -> None:
    lr = float(policy.optimizer.param_groups[0]["lr"]) if getattr(policy, "optimizer", None) is not None else 3e-4
    policy.optimizer = policy.optimizer_class(
        policy.parameters(),
        lr=lr,
        **policy.optimizer_kwargs,
    )


def _no_warm_start_record() -> dict[str, Any]:
    return {"status": "not_applied_f02_6_pending"}


def _callbacks(*, args: argparse.Namespace, output_dir: Path, n_envs: int, CallbackList: Any, CheckpointCallback: Any):
    callbacks = []
    if int(args.checkpoint_freq) > 0:
        save_freq = max(1, int(args.checkpoint_freq) // max(1, int(n_envs)))
        callbacks.append(
            CheckpointCallback(
                save_freq=save_freq,
                save_path=str(output_dir),
                name_prefix="rl_rs_ppo",
                verbose=int(args.verbose),
            )
        )
    return CallbackList(callbacks) if callbacks else None


def _checkpoint_records(output_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(output_dir.glob("*.zip")):
        records.append(
            {
                "path": path.name,
                "size_bytes": int(path.stat().st_size),
                "sha256": file_sha256(path),
            }
        )
    return records


def _source_hashes() -> dict[str, str]:
    paths = (
        "2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py",
        "2_experiment/forest_n3p/scripts/_module2_contract_gate.py",
        "2_experiment/forest_n3p/rl_rs/sb3_policy.py",
        "2_experiment/forest_n3p/rl_rs/gym_env.py",
        "2_experiment/forest_n3p/rl_rs/curriculum.py",
        "2_experiment/forest_n3p/rl_rs/training_logging.py",
        "2_experiment/forest_n3p/rl_rs/env.py",
        "2_experiment/forest_n3p/rl_rs/reward.py",
    )
    return {path: file_sha256(path) for path in paths if Path(path).exists()}


def _config_record(*, args: argparse.Namespace, raw_argv: Sequence[str], contract_status: str, reward_config: RewardConfig | None = None) -> dict[str, Any]:
    effective_reward_config = reward_config or RewardConfig()
    return {
        "command": " ".join(["python -m forest_n3p.scripts.train_rl_rs_ppo", *raw_argv]),
        "smoke": bool(args.smoke),
        "contract": str(args.contract_path),
        "contract_status": str(contract_status),
        "seed": int(args.seed),
        "policy": "MultiInputPolicy" if args.bc_checkpoint is None else "RlRsMultiInputPolicy",
        "features_extractor": "RlRsPatchCnnExtractor" if str(args.features_extractor) == "patch_cnn" else "RlRsObstacleSummaryExtractor",
        "cnn_output_dim": int(args.cnn_output_dim) if str(args.features_extractor) == "patch_cnn" else None,
        "scalar_scale": _scalar_scale(args) if str(args.features_extractor) == "patch_cnn" else None,
        "lr_schedule": str(args.lr_schedule),
        "value_pretrain_timesteps": int(args.value_pretrain_timesteps),
        "warm_start_status": "not_applied_f02_6_pending",
        "bc_checkpoint": None if args.bc_checkpoint is None else str(args.bc_checkpoint),
        "reward_config_path": None if args.reward_config is None else str(args.reward_config),
        "reward_config": reward_config_to_record(effective_reward_config),
        "curriculum_preset": str(args.curriculum_preset),
        "oracle_path": str(args.oracle_path),
        "heldout_seed": int(args.heldout_seed),
        "n_envs": int(args.n_envs),
        "total_timesteps": int(args.total_timesteps),
        "n_steps": int(args.n_steps),
        "batch_size": int(args.batch_size),
        "n_epochs": int(args.n_epochs),
        "learning_rate": float(args.learning_rate),
        "gamma": float(args.gamma),
        "gae_lambda": float(args.gae_lambda),
        "clip_range": float(args.clip_range),
        "ent_coef": float(args.ent_coef),
        "vf_coef": float(args.vf_coef),
        "max_grad_norm": float(args.max_grad_norm),
        "policy_net_arch": list(_parse_ints(str(args.policy_net_arch))),
        "value_net_arch": list(_parse_ints(str(args.value_net_arch))),
        "tensorboard_log": None if args.tensorboard_log is None else str(args.tensorboard_log),
        "checkpoint_freq": int(args.checkpoint_freq),
        "device": str(args.device),
        "allow_duplicate_openmp": bool(args.allow_duplicate_openmp),
        "observation_config": {
            "patch_size_m": float(args.obs_patch_size_m),
            "patch_cells": int(args.obs_patch_cells),
            "include_edt": bool(args.obs_include_edt),
            "edt_clip_m": float(args.obs_edt_clip_m),
        },
        "env_config": {
            "max_steps": int(args.max_steps),
            "action_step_m": float(args.action_step_m),
            "collision_sample_step_m": float(args.collision_sample_step_m),
            "terminal_check_every": int(args.terminal_check_every),
            "theta_bins": int(args.theta_bins),
        },
    }


def _parse_ints(raw: str) -> tuple[int, ...]:
    values = tuple(int(part.strip()) for part in str(raw).split(",") if part.strip())
    if not values:
        raise ValueError("network architecture must contain at least one hidden layer")
    return values


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop training.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
