from __future__ import annotations

import argparse
import json
import shlex
import socket
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_PATH = Path(".pipeline/contracts/module2-ppo-funnel-expansion.md")
DEFAULT_ORACLE_PATH = Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet")
ALLOWED_CONTRACT_STATUSES = {"approved", "frozen"}


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    output_dir = Path(args.output_dir)
    manifest_out = Path(args.manifest_out) if args.manifest_out else output_dir / "gate3_preflight_manifest.json"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_preflight_manifest(args=args, raw_argv=raw_argv, output_dir=output_dir, manifest_out=manifest_out)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a formal Module2 F03 Gate #3 PPO trial protocol without running training.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--seed", type=int, default=20260704)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--allow-duplicate-openmp", action="store_true")
    parser.add_argument("--bc-checkpoint", type=Path, default=None)
    parser.add_argument(
        "--warm-start-decision",
        choices=("pending", "approved_obstacle_summary", "not_used"),
        default="pending",
        help="Current F02.6 decision state. Pending blocks formal warm-start runs.",
    )
    parser.add_argument("--oracle-path", type=Path, default=DEFAULT_ORACLE_PATH)
    parser.add_argument("--heldout-seed", type=int, default=20260704)
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
    parser.add_argument("--train-checkpoint-freq", type=int, default=10_000)
    parser.add_argument("--eval-episodes", type=int, default=64)
    parser.add_argument("--eval-min-episodes", type=int, default=64)
    parser.add_argument("--eval-success-threshold", type=float, default=0.8)
    parser.add_argument("--obs-patch-size-m", type=float, default=6.4)
    parser.add_argument("--obs-patch-cells", type=int, default=64)
    parser.add_argument("--max-steps", type=int, default=32)
    parser.add_argument("--allow-existing-output-dir", action="store_true")
    return parser.parse_args(list(argv))


def build_preflight_manifest(*, args: argparse.Namespace, raw_argv: Sequence[str], output_dir: Path, manifest_out: Path) -> dict[str, Any]:
    protocol = _protocol_record(args=args, output_dir=output_dir)
    blockers = _formal_blockers(args=args, output_dir=output_dir, protocol=protocol)
    runner_argv = _runner_argv(args=args, output_dir=output_dir)
    audit_argv = _audit_argv(args=args, output_dir=output_dir)
    return {
        "schema_version": 1,
        "preflight_name": "module2_f03_gate3_formal_trial_preflight",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "command": _join_command(["python", "-m", "forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial", *raw_argv]),
        "contract": str(args.contract_path),
        "contract_status": _contract_status(args.contract_path),
        "output_dir": str(output_dir),
        "manifest_out": str(manifest_out),
        "preflight_status": "ready" if not blockers else "blocked",
        "formal_trial_ready": not blockers,
        "formal_blockers": blockers,
        "formal_warnings": _formal_warnings(args=args),
        "warm_start_decision": str(args.warm_start_decision),
        "protocol": protocol,
        "runner_argv": runner_argv,
        "runner_command": _join_command(runner_argv),
        "audit_argv": audit_argv,
        "audit_command": _join_command(audit_argv),
        "expected_artifacts": _expected_artifacts(output_dir),
    }


def _protocol_record(*, args: argparse.Namespace, output_dir: Path) -> dict[str, Any]:
    return {
        "trial_name": "module2_f03_gate3_formal_train_eval",
        "runner": "forest_n3p.scripts.run_rl_rs_gate3_trial",
        "audit": "forest_n3p.scripts.audit_rl_rs_gate3_trial",
        "output_dir": str(output_dir),
        "smoke": False,
        "formal_gate_claim_expected": False,
        "formal_audit_required": True,
        "contract": str(args.contract_path),
        "seed": int(args.seed),
        "device": str(args.device),
        "bc_checkpoint": None if args.bc_checkpoint is None else str(args.bc_checkpoint),
        "train_curriculum_preset": "f03",
        "eval_curriculum_preset": "f03",
        "oracle_path": str(args.oracle_path),
        "heldout_seed": int(args.heldout_seed),
        "train_total_timesteps": int(args.train_total_timesteps),
        "train_n_envs": int(args.train_n_envs),
        "train_n_steps": int(args.train_n_steps),
        "train_batch_size": int(args.train_batch_size),
        "train_n_epochs": int(args.train_n_epochs),
        "train_learning_rate": float(args.train_learning_rate),
        "train_gamma": float(args.train_gamma),
        "train_gae_lambda": float(args.train_gae_lambda),
        "train_clip_range": float(args.train_clip_range),
        "train_ent_coef": float(args.train_ent_coef),
        "train_vf_coef": float(args.train_vf_coef),
        "train_max_grad_norm": float(args.train_max_grad_norm),
        "train_policy_net_arch": str(args.train_policy_net_arch),
        "train_value_net_arch": str(args.train_value_net_arch),
        "train_checkpoint_freq": int(args.train_checkpoint_freq),
        "eval_episodes": int(args.eval_episodes),
        "eval_min_episodes": int(args.eval_min_episodes),
        "eval_success_threshold": float(args.eval_success_threshold),
        "obs_patch_size_m": float(args.obs_patch_size_m),
        "obs_patch_cells": int(args.obs_patch_cells),
        "max_steps": int(args.max_steps),
    }


def _formal_blockers(*, args: argparse.Namespace, output_dir: Path, protocol: dict[str, Any]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    contract_status = _contract_status(args.contract_path)
    if contract_status not in ALLOWED_CONTRACT_STATUSES:
        blockers.append(
            _reason(
                "contract_not_approved",
                f"contract status is {contract_status!r}",
                observed=contract_status,
                expected="approved or frozen",
            )
        )
    if not Path(args.oracle_path).exists():
        blockers.append(_reason("missing_oracle_path", f"oracle path does not exist: {args.oracle_path}", observed=str(args.oracle_path)))
    if args.bc_checkpoint is not None and not Path(args.bc_checkpoint).exists():
        blockers.append(_reason("missing_bc_checkpoint", f"BC checkpoint does not exist: {args.bc_checkpoint}", observed=str(args.bc_checkpoint)))
    if args.bc_checkpoint is not None and str(args.warm_start_decision) == "pending":
        blockers.append(
            _reason(
                "warm_start_decision_pending",
                "BC warm-start requested but F02.6 is still pending",
                observed=str(args.bc_checkpoint),
                expected="approved_obstacle_summary or no --bc-checkpoint",
            )
        )
    if args.bc_checkpoint is None and str(args.warm_start_decision) == "approved_obstacle_summary":
        blockers.append(
            _reason(
                "warm_start_decision_mismatch",
                "warm-start decision is approved_obstacle_summary but no BC checkpoint was provided",
                observed="no --bc-checkpoint",
                expected="--bc-checkpoint",
            )
        )
    if int(args.eval_episodes) < 64 or int(args.eval_min_episodes) < 64:
        blockers.append(
            _reason(
                "insufficient_formal_eval_episodes",
                f"eval_episodes={args.eval_episodes}, eval_min_episodes={args.eval_min_episodes}, required>=64",
                observed={"eval_episodes": int(args.eval_episodes), "eval_min_episodes": int(args.eval_min_episodes)},
                expected={">=": 64},
            )
        )
    if float(args.eval_success_threshold) < 0.8:
        blockers.append(
            _reason(
                "success_threshold_too_low",
                f"eval_success_threshold={args.eval_success_threshold}, required>=0.8",
                observed=float(args.eval_success_threshold),
                expected={">=": 0.8},
            )
        )
    if _has_existing_trial_outputs(output_dir) and not bool(args.allow_existing_output_dir):
        blockers.append(
            _reason(
                "existing_trial_outputs",
                f"output dir already contains trial outputs: {output_dir}",
                observed=str(output_dir),
                expected="empty trial output dir or --allow-existing-output-dir",
            )
        )
    if protocol["train_curriculum_preset"] != "f03" or protocol["eval_curriculum_preset"] != "f03":
        blockers.append(_reason("curriculum_not_f03", "formal Gate #3 requires f03 train/eval curriculum"))
    return blockers


def _formal_warnings(*, args: argparse.Namespace) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    if int(args.train_total_timesteps) < 100_000:
        warnings.append(
            _reason(
                "low_training_budget",
                f"train_total_timesteps={args.train_total_timesteps}; this may be useful only as a pilot",
                observed=int(args.train_total_timesteps),
                expected={">=": 100_000},
            )
        )
    return warnings


def _runner_argv(*, args: argparse.Namespace, output_dir: Path) -> list[str]:
    argv = [
        "python",
        "-m",
        "forest_n3p.scripts.run_rl_rs_gate3_trial",
        "--output-dir",
        str(output_dir),
        "--contract-path",
        str(args.contract_path),
        "--seed",
        str(args.seed),
        "--device",
        str(args.device),
        "--train-curriculum-preset",
        "f03",
        "--eval-curriculum-preset",
        "f03",
        "--oracle-path",
        str(args.oracle_path),
        "--heldout-seed",
        str(args.heldout_seed),
        "--train-total-timesteps",
        str(args.train_total_timesteps),
        "--train-n-envs",
        str(args.train_n_envs),
        "--train-n-steps",
        str(args.train_n_steps),
        "--train-batch-size",
        str(args.train_batch_size),
        "--train-n-epochs",
        str(args.train_n_epochs),
        "--train-learning-rate",
        str(args.train_learning_rate),
        "--train-gamma",
        str(args.train_gamma),
        "--train-gae-lambda",
        str(args.train_gae_lambda),
        "--train-clip-range",
        str(args.train_clip_range),
        "--train-ent-coef",
        str(args.train_ent_coef),
        "--train-vf-coef",
        str(args.train_vf_coef),
        "--train-max-grad-norm",
        str(args.train_max_grad_norm),
        "--train-policy-net-arch",
        str(args.train_policy_net_arch),
        "--train-value-net-arch",
        str(args.train_value_net_arch),
        "--train-checkpoint-freq",
        str(args.train_checkpoint_freq),
        "--eval-episodes",
        str(args.eval_episodes),
        "--eval-min-episodes",
        str(args.eval_min_episodes),
        "--eval-success-threshold",
        str(args.eval_success_threshold),
        "--obs-patch-size-m",
        str(args.obs_patch_size_m),
        "--obs-patch-cells",
        str(args.obs_patch_cells),
        "--max-steps",
        str(args.max_steps),
    ]
    if bool(args.allow_duplicate_openmp):
        argv.append("--allow-duplicate-openmp")
    if args.bc_checkpoint is not None:
        argv.extend(["--bc-checkpoint", str(args.bc_checkpoint)])
    return argv


def _audit_argv(*, args: argparse.Namespace, output_dir: Path) -> list[str]:
    return [
        "python",
        "-m",
        "forest_n3p.scripts.audit_rl_rs_gate3_trial",
        "--trial-dir",
        str(output_dir),
        "--contract-path",
        str(args.contract_path),
        "--min-formal-episodes",
        str(args.eval_min_episodes),
        "--required-success-threshold",
        str(args.eval_success_threshold),
        "--required-train-curriculum",
        "f03",
        "--required-eval-curriculum",
        "f03",
        "--warm-start-decision",
        str(args.warm_start_decision),
    ]


def _expected_artifacts(output_dir: Path) -> list[str]:
    return [
        str(output_dir / "train" / "final_model.zip"),
        str(output_dir / "train" / "summary.json"),
        str(output_dir / "train" / "training_manifest.json"),
        str(output_dir / "eval" / "gate3_eval_episodes.csv"),
        str(output_dir / "eval" / "gate3_summary.json"),
        str(output_dir / "gate3_trial_manifest.json"),
        str(output_dir / "gate3_formal_audit.json"),
    ]


def _contract_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def _has_existing_trial_outputs(output_dir: Path) -> bool:
    markers = (
        output_dir / "gate3_trial_manifest.json",
        output_dir / "train" / "summary.json",
        output_dir / "eval" / "gate3_summary.json",
    )
    return any(path.exists() for path in markers)


def _join_command(argv: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in argv)


def _reason(code: str, message: str, *, observed: Any | None = None, expected: Any | None = None) -> dict[str, Any]:
    reason = {"code": code, "message": message}
    if observed is not None:
        reason["observed"] = observed
    if expected is not None:
        reason["expected"] = expected
    return reason


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop preflight.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
