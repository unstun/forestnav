from __future__ import annotations

import argparse
import csv
import json
import os
import socket
import subprocess
import sys
from time import perf_counter
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
from forest_n3p.rl_rs.training_logging import RlRsEpisodeLoggingWrapper, file_sha256


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    if bool(args.allow_duplicate_openmp):
        os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    PPO = _load_ppo()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model = PPO.load(args.model, device=str(args.device))
    episodes_csv = output_dir / "gate3_eval_episodes.csv"
    env = _make_eval_env(args=args, csv_path=episodes_csv)
    try:
        for episode_idx in range(int(args.episodes)):
            obs, _info = env.reset(seed=int(args.seed) + int(episode_idx))
            done = False
            while not done:
                predict_start_s = perf_counter()
                action, _state = model.predict(obs, deterministic=True)
                env.record_nn_forward_time(perf_counter() - predict_start_s)
                obs, _reward, terminated, truncated, _info = env.step(action)
                done = bool(terminated or truncated)
    finally:
        env.close()

    episode_rows = _read_episode_rows(episodes_csv)
    summary = _gate_summary(args=args, raw_argv=raw_argv, rows=episode_rows, episodes_csv=episodes_csv)
    (output_dir / "gate3_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Module2 RL-RS PPO Gate #3 terminal-RS-connectable success.")
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260704)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--allow-duplicate-openmp", action="store_true")
    parser.add_argument("--curriculum-preset", choices=("open", "obstacle", "f03"), default="f03")
    parser.add_argument("--oracle-path", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--heldout-seed", type=int, default=20260704)
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--min-episodes", type=int, default=64)
    parser.add_argument("--success-threshold", type=float, default=0.8)
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


def _load_ppo():
    from stable_baselines3 import PPO

    return PPO


def _make_eval_env(*, args: argparse.Namespace, csv_path: Path) -> RlRsEpisodeLoggingWrapper:
    cfg = _curriculum_config(args)
    sampler = _sampler(args, cfg=cfg)
    env = GymAnalyticExpansionEnv(sampler, observation_config=cfg.observation_config)
    return RlRsEpisodeLoggingWrapper(env, csv_path=csv_path)


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


def _read_episode_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _gate_summary(*, args: argparse.Namespace, raw_argv: Sequence[str], rows: list[dict[str, str]], episodes_csv: Path) -> dict[str, Any]:
    episodes = len(rows)
    successes = sum(1 for row in rows if _csv_bool(row.get("terminal_rs_success")))
    collisions = sum(1 for row in rows if _csv_bool(row.get("collision")))
    truncated = sum(1 for row in rows if _csv_bool(row.get("truncated")))
    nn_forward_time_s = sum(_csv_float(row.get("nn_forward_time_s")) for row in rows)
    success_rate = float(successes) / float(episodes) if episodes else 0.0
    threshold = float(args.success_threshold)
    enough_episodes = episodes >= int(args.min_episodes)
    decision = "pass" if enough_episodes and success_rate >= threshold else "fail"
    return {
        "schema_version": 1,
        "gate_name": "module2_f03_gate3",
        "contract": ".pipeline/contracts/module2-ppo-funnel-expansion.md",
        "decision": decision,
        "decision_rule": "pass iff episodes >= min_episodes and terminal_rs_success_rate >= success_threshold",
        "success_threshold": threshold,
        "min_episodes": int(args.min_episodes),
        "episodes": int(episodes),
        "terminal_rs_success": int(successes),
        "terminal_rs_success_rate": float(success_rate),
        "collision": int(collisions),
        "collision_rate": float(collisions) / float(episodes) if episodes else 0.0,
        "truncated": int(truncated),
        "truncation_rate": float(truncated) / float(episodes) if episodes else 0.0,
        "nn_forward_time_s": float(nn_forward_time_s),
        "mean_nn_forward_time_s": float(nn_forward_time_s) / float(episodes) if episodes else 0.0,
        "model": str(args.model),
        "model_sha256": file_sha256(args.model),
        "episodes_csv": str(episodes_csv),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "config": {
            "command": " ".join(["python -m forest_n3p.scripts.eval_rl_rs_gate3", *raw_argv]),
            "seed": int(args.seed),
            "device": str(args.device),
            "curriculum_preset": str(args.curriculum_preset),
            "oracle_path": str(args.oracle_path),
            "heldout_seed": int(args.heldout_seed),
            "episodes": int(args.episodes),
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
        },
    }


def _csv_bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def _csv_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop evaluation.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
