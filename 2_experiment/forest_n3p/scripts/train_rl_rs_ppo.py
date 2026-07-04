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
from forest_n3p.rl_rs.training_logging import RlRsEpisodeLoggingWrapper, file_sha256, write_training_manifest


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    if bool(args.allow_duplicate_openmp):
        os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    _apply_smoke_overrides(args)
    PPO, CallbackList, CheckpointCallback, DummyVecEnv = _load_sb3()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = _config_record(args=args, raw_argv=raw_argv)
    env = DummyVecEnv([_make_env_factory(args=args, output_dir=output_dir, rank=rank) for rank in range(int(args.n_envs))])
    callbacks = _callbacks(args=args, output_dir=output_dir, n_envs=int(args.n_envs), CallbackList=CallbackList, CheckpointCallback=CheckpointCallback)
    model = PPO(
        "MultiInputPolicy",
        env,
        learning_rate=float(args.learning_rate),
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
    try:
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
        "output_dir": str(output_dir),
        "manifest": str(manifest_path),
        "final_model": "final_model.zip",
        "checkpoint_count": int(len(checkpoints)),
        "warm_start_status": "not_applied_f02_6_pending",
        "config": config,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a Module2 RL-RS PPO analytic-expansion policy.")
    parser.add_argument("--output-dir", type=Path, default=Path("2_experiment/forest_n3p/models/module2_rl_rs_ppo_f03"))
    parser.add_argument("--seed", type=int, default=20260704)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--allow-duplicate-openmp", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="Run a tiny open-connector training smoke.")
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


def _load_sb3():
    from stable_baselines3 import PPO
    from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback
    from stable_baselines3.common.vec_env import DummyVecEnv

    return PPO, CallbackList, CheckpointCallback, DummyVecEnv


def _make_env_factory(*, args: argparse.Namespace, output_dir: Path, rank: int):
    def _factory():
        cfg = _curriculum_config(args)
        sampler = _sampler(args, cfg=cfg)
        env = GymAnalyticExpansionEnv(sampler, observation_config=cfg.observation_config)
        csv_path = output_dir / f"episodes_env{int(rank)}.csv"
        return RlRsEpisodeLoggingWrapper(env, csv_path=csv_path)

    return _factory


def _curriculum_config(args: argparse.Namespace) -> CurriculumContextConfig:
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
    )


def _sampler(args: argparse.Namespace, *, cfg: CurriculumContextConfig):
    if str(args.curriculum_preset) == "open":
        return OpenConnectorContextSampler(config=cfg)
    if str(args.curriculum_preset) == "obstacle":
        return ObstacleBypassContextSampler(config=cfg)
    return make_f03_curriculum_sampler(oracle_path=args.oracle_path, heldout_seed=int(args.heldout_seed), config=cfg)


def _policy_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    from forest_n3p.rl_rs.sb3_policy import RlRsObstacleSummaryExtractor

    return {
        "features_extractor_class": RlRsObstacleSummaryExtractor,
        "net_arch": {
            "pi": list(_parse_ints(str(args.policy_net_arch))),
            "vf": list(_parse_ints(str(args.value_net_arch))),
        },
    }


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
        "2_experiment/forest_n3p/rl_rs/sb3_policy.py",
        "2_experiment/forest_n3p/rl_rs/gym_env.py",
        "2_experiment/forest_n3p/rl_rs/curriculum.py",
        "2_experiment/forest_n3p/rl_rs/training_logging.py",
        "2_experiment/forest_n3p/rl_rs/env.py",
        "2_experiment/forest_n3p/rl_rs/reward.py",
    )
    return {path: file_sha256(path) for path in paths if Path(path).exists()}


def _config_record(*, args: argparse.Namespace, raw_argv: Sequence[str]) -> dict[str, Any]:
    return {
        "command": " ".join(["python -m forest_n3p.scripts.train_rl_rs_ppo", *raw_argv]),
        "smoke": bool(args.smoke),
        "seed": int(args.seed),
        "policy": "MultiInputPolicy",
        "features_extractor": "RlRsObstacleSummaryExtractor",
        "warm_start_status": "not_applied_f02_6_pending",
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
