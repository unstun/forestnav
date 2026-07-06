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

from forest_n3p.rl_rs.training_logging import file_sha256
from forest_n3p.scripts._module2_contract_gate import require_contract_ready
from forest_n3p.scripts.eval_rl_rs_gate3 import main as eval_gate3_main
from forest_n3p.scripts.train_rl_rs_ppo import main as train_rl_rs_ppo_main


DEFAULT_CONTRACT_PATH = ".pipeline/contracts/module2-ppo-funnel-expansion.md"


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    if bool(args.allow_duplicate_openmp):
        os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    _apply_smoke_overrides(args)
    contract_status = require_contract_ready(
        args.contract_path,
        allow_unapproved=bool(args.smoke),
        context="Module2 Gate3 trial",
    )

    output_dir = Path(args.output_dir)
    train_dir = output_dir / "train"
    eval_dir = output_dir / "eval"
    output_dir.mkdir(parents=True, exist_ok=True)

    train_rc = train_rl_rs_ppo_main(_train_argv(args=args, train_dir=train_dir))
    if train_rc != 0:
        _write_incomplete_manifest(args=args, raw_argv=raw_argv, output_dir=output_dir, status="train_failed", train_rc=train_rc, eval_rc=None)
        return int(train_rc)

    model_path = train_dir / "final_model.zip"
    eval_rc = eval_gate3_main(_eval_argv(args=args, model_path=model_path, eval_dir=eval_dir))
    if eval_rc != 0:
        _write_incomplete_manifest(args=args, raw_argv=raw_argv, output_dir=output_dir, status="eval_failed", train_rc=train_rc, eval_rc=eval_rc)
        return int(eval_rc)

    manifest = _trial_manifest(
        args=args,
        raw_argv=raw_argv,
        output_dir=output_dir,
        train_dir=train_dir,
        eval_dir=eval_dir,
        contract_status=contract_status,
    )
    manifest_path = output_dir / "gate3_trial_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a full Module2 F03 Gate #3 PPO train-then-eval trial.")
    parser.add_argument("--output-dir", type=Path, default=Path("0_trials/module2_ppo_gate3_trial"))
    parser.add_argument("--contract-path", default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--seed", type=int, default=20260704)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--allow-duplicate-openmp", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="Run the tiny open-connector train/eval smoke path.")
    parser.add_argument("--bc-checkpoint", type=Path, default=None, help="Optional F02 obstacle-summary BC checkpoint for PPO actor initialization.")
    parser.add_argument("--oracle-path", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--heldout-seed", type=int, default=20260704)

    parser.add_argument("--train-curriculum-preset", choices=("open", "obstacle", "f03"), default="f03")
    parser.add_argument("--train-total-timesteps", type=int, default=100_000)
    parser.add_argument("--train-n-envs", type=int, default=1)
    parser.add_argument("--train-n-steps", type=int, default=128)
    parser.add_argument("--train-batch-size", type=int, default=64)
    parser.add_argument("--train-n-epochs", type=int, default=4)
    parser.add_argument("--train-learning-rate", type=float, default=3e-4)
    parser.add_argument("--train-gamma", type=float, default=0.99)
    parser.add_argument("--train-gae-lambda", type=float, default=0.95)
    parser.add_argument("--train-clip-range", type=float, default=0.2)
    parser.add_argument("--train-ent-coef", type=float, default=0.0)
    parser.add_argument("--train-vf-coef", type=float, default=0.5)
    parser.add_argument("--train-max-grad-norm", type=float, default=0.5)
    parser.add_argument("--train-policy-net-arch", default="128,128,64")
    parser.add_argument("--train-value-net-arch", default="128,128,64")
    parser.add_argument("--train-tensorboard-log", type=Path, default=None)
    parser.add_argument("--train-checkpoint-freq", type=int, default=10_000)
    parser.add_argument("--train-verbose", type=int, default=0)

    parser.add_argument("--eval-curriculum-preset", choices=("open", "obstacle", "f03"), default="f03")
    parser.add_argument("--eval-episodes", type=int, default=64)
    parser.add_argument("--eval-min-episodes", type=int, default=64)
    parser.add_argument("--eval-success-threshold", type=float, default=0.8)

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
    args.train_curriculum_preset = "open"
    args.train_total_timesteps = 16
    args.train_n_envs = 1
    args.train_n_steps = 8
    args.train_batch_size = 8
    args.train_n_epochs = 1
    args.train_checkpoint_freq = 0
    args.train_verbose = 0
    args.eval_curriculum_preset = "open"
    args.eval_episodes = 4
    args.eval_min_episodes = 4
    args.eval_success_threshold = 0.8
    args.obs_patch_size_m = 0.4
    args.obs_patch_cells = 5
    args.max_steps = 4


def _train_argv(*, args: argparse.Namespace, train_dir: Path) -> list[str]:
    argv = [
        "--output-dir",
        str(train_dir),
        "--contract-path",
        str(args.contract_path),
        "--seed",
        str(args.seed),
        "--device",
        str(args.device),
        "--curriculum-preset",
        str(args.train_curriculum_preset),
        "--oracle-path",
        str(args.oracle_path),
        "--heldout-seed",
        str(args.heldout_seed),
        "--n-envs",
        str(args.train_n_envs),
        "--total-timesteps",
        str(args.train_total_timesteps),
        "--n-steps",
        str(args.train_n_steps),
        "--batch-size",
        str(args.train_batch_size),
        "--n-epochs",
        str(args.train_n_epochs),
        "--learning-rate",
        str(args.train_learning_rate),
        "--gamma",
        str(args.train_gamma),
        "--gae-lambda",
        str(args.train_gae_lambda),
        "--clip-range",
        str(args.train_clip_range),
        "--ent-coef",
        str(args.train_ent_coef),
        "--vf-coef",
        str(args.train_vf_coef),
        "--max-grad-norm",
        str(args.train_max_grad_norm),
        "--policy-net-arch",
        str(args.train_policy_net_arch),
        "--value-net-arch",
        str(args.train_value_net_arch),
        "--checkpoint-freq",
        str(args.train_checkpoint_freq),
        "--verbose",
        str(args.train_verbose),
        "--obs-patch-size-m",
        str(args.obs_patch_size_m),
        "--obs-patch-cells",
        str(args.obs_patch_cells),
        "--obs-edt-clip-m",
        str(args.obs_edt_clip_m),
        "--max-steps",
        str(args.max_steps),
        "--action-step-m",
        str(args.action_step_m),
        "--collision-sample-step-m",
        str(args.collision_sample_step_m),
        "--terminal-check-every",
        str(args.terminal_check_every),
        "--theta-bins",
        str(args.theta_bins),
    ]
    if bool(args.allow_duplicate_openmp):
        argv.append("--allow-duplicate-openmp")
    if bool(args.smoke):
        argv.append("--smoke")
    if not bool(args.obs_include_edt):
        argv.append("--no-obs-include-edt")
    if args.bc_checkpoint is not None:
        argv.extend(["--bc-checkpoint", str(args.bc_checkpoint)])
    if args.train_tensorboard_log is not None:
        argv.extend(["--tensorboard-log", str(args.train_tensorboard_log)])
    return argv


def _eval_argv(*, args: argparse.Namespace, model_path: Path, eval_dir: Path) -> list[str]:
    argv = [
        "--model",
        str(model_path),
        "--output-dir",
        str(eval_dir),
        "--contract-path",
        str(args.contract_path),
        "--seed",
        str(args.seed),
        "--device",
        str(args.device),
        "--curriculum-preset",
        str(args.eval_curriculum_preset),
        "--oracle-path",
        str(args.oracle_path),
        "--heldout-seed",
        str(args.heldout_seed),
        "--episodes",
        str(args.eval_episodes),
        "--min-episodes",
        str(args.eval_min_episodes),
        "--success-threshold",
        str(args.eval_success_threshold),
        "--obs-patch-size-m",
        str(args.obs_patch_size_m),
        "--obs-patch-cells",
        str(args.obs_patch_cells),
        "--obs-edt-clip-m",
        str(args.obs_edt_clip_m),
        "--max-steps",
        str(args.max_steps),
        "--action-step-m",
        str(args.action_step_m),
        "--collision-sample-step-m",
        str(args.collision_sample_step_m),
        "--terminal-check-every",
        str(args.terminal_check_every),
        "--theta-bins",
        str(args.theta_bins),
    ]
    if bool(args.allow_duplicate_openmp):
        argv.append("--allow-duplicate-openmp")
    if bool(args.smoke):
        argv.append("--allow-unapproved-contract-for-smoke")
    if not bool(args.obs_include_edt):
        argv.append("--no-obs-include-edt")
    return argv


def _trial_manifest(
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    output_dir: Path,
    train_dir: Path,
    eval_dir: Path,
    contract_status: str,
) -> dict[str, Any]:
    train_summary = _read_json(train_dir / "summary.json")
    eval_summary = _read_json(eval_dir / "gate3_summary.json")
    train_manifest = train_dir / "training_manifest.json"
    model_path = train_dir / "final_model.zip"
    eval_csv = eval_dir / "gate3_eval_episodes.csv"
    return {
        "schema_version": 1,
        "trial_name": "module2_f03_gate3_train_eval",
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "command": " ".join(["python -m forest_n3p.scripts.run_rl_rs_gate3_trial", *raw_argv]),
        "contract": str(args.contract_path),
        "contract_status": str(contract_status),
        "smoke": bool(args.smoke),
        "formal_gate_claim": False,
        "formal_gate_boundary": "runner produces auditable train/eval evidence only; formal Gate #3 judgment requires protocol review",
        "warm_start_status": str(train_summary.get("warm_start_status", "unknown")),
        "bc_checkpoint": None if args.bc_checkpoint is None else str(args.bc_checkpoint),
        "train_output_dir": _rel(train_dir, output_dir),
        "eval_output_dir": _rel(eval_dir, output_dir),
        "train_model": _rel(model_path, output_dir),
        "train_summary": _rel(train_dir / "summary.json", output_dir),
        "train_manifest": _rel(train_manifest, output_dir),
        "eval_summary": _rel(eval_dir / "gate3_summary.json", output_dir),
        "eval_episodes_csv": _rel(eval_csv, output_dir),
        "gate3_decision": str(eval_summary.get("decision", "unknown")),
        "terminal_rs_success_rate": float(eval_summary.get("terminal_rs_success_rate", 0.0)),
        "terminal_rs_success": int(eval_summary.get("terminal_rs_success", 0)),
        "episodes": int(eval_summary.get("episodes", 0)),
        "success_threshold": float(eval_summary.get("success_threshold", args.eval_success_threshold)),
        "train_config": train_summary.get("config", {}),
        "eval_config": eval_summary.get("config", {}),
        "source_hashes": _source_hashes(),
    }


def _write_incomplete_manifest(
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    output_dir: Path,
    status: str,
    train_rc: int | None,
    eval_rc: int | None,
) -> None:
    manifest = {
        "schema_version": 1,
        "trial_name": "module2_f03_gate3_train_eval",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "command": " ".join(["python -m forest_n3p.scripts.run_rl_rs_gate3_trial", *raw_argv]),
        "contract": str(args.contract_path),
        "smoke": bool(args.smoke),
        "formal_gate_claim": False,
        "warm_start_status": "unknown",
        "bc_checkpoint": None if args.bc_checkpoint is None else str(args.bc_checkpoint),
        "train_exit_code": train_rc,
        "eval_exit_code": eval_rc,
        "source_hashes": _source_hashes(),
    }
    (output_dir / "gate3_trial_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return str(path)


def _source_hashes() -> dict[str, str]:
    paths = (
        "2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py",
        "2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py",
        "2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py",
        "2_experiment/forest_n3p/rl_rs/sb3_policy.py",
        "2_experiment/forest_n3p/rl_rs/gym_env.py",
        "2_experiment/forest_n3p/rl_rs/curriculum.py",
        "2_experiment/forest_n3p/rl_rs/training_logging.py",
        "2_experiment/forest_n3p/rl_rs/env.py",
        "2_experiment/forest_n3p/rl_rs/reward.py",
    )
    return {path: file_sha256(path) for path in paths if Path(path).exists()}


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop trial orchestration.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
