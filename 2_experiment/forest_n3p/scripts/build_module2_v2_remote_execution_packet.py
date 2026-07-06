from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_contract_promotion_packet import (
    DEFAULT_REMOTE_READINESS,
)
from forest_n3p.scripts.build_module2_v2_contract_readiness_gate import (
    DEFAULT_BC_CHECKPOINT,
    DEFAULT_CONTRACT_PATH,
    DEFAULT_ORACLE_PATH,
)


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_remote_execution_packet")
DEFAULT_READINESS_GATE = Path("0_trials/module2_v2_contract_readiness_gate/v2_contract_readiness_gate.json")
DEFAULT_PROMOTION_PACKET = Path("0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.json")
DEFAULT_DRY_RUN = Path("0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_ATTEMPT_DIR = Path(
    "0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706"
)
DEFAULT_PREFLIGHT_MANIFEST = Path(
    "0_trials/module2_remote_preflight/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/"
    "gate3_preflight_manifest.json"
)
DEFAULT_GPU_ALIAS = "gpu3070ti-relay"
DEFAULT_REMOTE_WORKDIR = "~/ForestNav"
DEFAULT_REMOTE_PYTHON = ".venv/bin/python"
DEFAULT_LOCAL_ROOT = Path("/Users/sun/tongbu/study/phdproject/ForestNav")
READY_READINESS_STATUS = "v2_contract_ready_for_source_freshness"
READY_PROMOTION_PACKET_STATUS = "v2_contract_promotion_packet_ready_awaiting_dr_sun"
READY_DRY_RUN_STATUS = "promotion_apply_ready"
SOURCE_FRESHNESS_READY_STATUSES = {
    "source_freshness_clean_current",
    "source_freshness_tracked_artifact_lag_only_gate_ready",
}
V2_TRAINING_ARGS = {
    "--seed": "20260706",
    "--device": "cuda",
    "--train-total-timesteps": "500000",
    "--train-n-envs": "4",
    "--train-n-steps": "256",
    "--train-batch-size": "256",
    "--train-n-epochs": "8",
    "--train-learning-rate": "0.0001",
    "--train-ent-coef": "0.01",
    "--train-checkpoint-freq": "25000",
    "--eval-episodes": "64",
    "--eval-min-episodes": "64",
    "--eval-success-threshold": "0.8",
}


@dataclass(frozen=True)
class Module2V2RemoteExecutionPacketConfig:
    output_dir: Path
    packet_out: Path | None = None
    markdown_out: Path | None = None
    readiness_gate_path: Path = DEFAULT_READINESS_GATE
    promotion_packet_path: Path = DEFAULT_PROMOTION_PACKET
    promotion_dry_run_path: Path = DEFAULT_DRY_RUN
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remote_readiness_path: Path = DEFAULT_REMOTE_READINESS
    contract_path: Path = DEFAULT_CONTRACT_PATH
    oracle_path: Path = DEFAULT_ORACLE_PATH
    bc_checkpoint: Path = DEFAULT_BC_CHECKPOINT
    attempt_dir: Path = DEFAULT_ATTEMPT_DIR
    preflight_manifest_path: Path = DEFAULT_PREFLIGHT_MANIFEST
    gpu_alias: str = DEFAULT_GPU_ALIAS
    remote_workdir: str = DEFAULT_REMOTE_WORKDIR
    remote_python: str = DEFAULT_REMOTE_PYTHON
    local_root: Path = DEFAULT_LOCAL_ROOT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2RemoteExecutionPacketConfig(
        output_dir=args.output_dir,
        packet_out=args.packet_out,
        markdown_out=args.markdown_out,
        readiness_gate_path=args.readiness_gate,
        promotion_packet_path=args.promotion_packet,
        promotion_dry_run_path=args.promotion_dry_run,
        source_freshness_path=args.source_freshness,
        remote_readiness_path=args.remote_readiness,
        contract_path=args.contract_path,
        oracle_path=args.oracle_path,
        bc_checkpoint=args.bc_checkpoint,
        attempt_dir=args.attempt_dir,
        preflight_manifest_path=args.preflight_manifest,
        gpu_alias=args.gpu_alias,
        remote_workdir=args.remote_workdir,
        remote_python=args.remote_python,
        local_root=args.local_root,
    )
    packet = build_packet(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_out = config.packet_out or output_dir / "v2_remote_execution_packet.json"
    markdown_out = config.markdown_out or output_dir / "v2_remote_execution_packet.md"
    packet_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    packet_out.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(packet), encoding="utf-8")
    print(json.dumps({"packet": str(packet_out), "markdown": str(markdown_out), "status": packet["status"]}, indent=2))
    return 0


def build_packet(config: Module2V2RemoteExecutionPacketConfig) -> dict[str, Any]:
    readiness = _read_json(config.readiness_gate_path)
    promotion = _read_json(config.promotion_packet_path)
    dry_run = _read_json(config.promotion_dry_run_path)
    source_freshness = _read_json(config.source_freshness_path)
    preflight_manifest = _read_json(config.preflight_manifest_path)
    contract_status = _contract_status(config.contract_path)
    remote_readiness_text = _read_text(config.remote_readiness_path)
    command_plan = _command_plan(config)
    blockers = _blockers(
        readiness=readiness,
        promotion=promotion,
        dry_run=dry_run,
        source_freshness=source_freshness,
        preflight_manifest=preflight_manifest,
        contract_status=contract_status,
        remote_readiness_text=remote_readiness_text,
        command_plan=command_plan,
    )
    status = _status(blockers=blockers, readiness=readiness, source_freshness=source_freshness)
    source_ready = _source_freshness_ready(source_freshness)
    readiness_ready = readiness.get("status") == READY_READINESS_STATUS
    remote_preflight_allowed = readiness_ready and source_ready and not blockers
    remote_training_allowed = False
    _annotate_commands(
        command_plan=command_plan,
        readiness_ready=readiness_ready,
        source_ready=source_ready,
        remote_preflight_allowed=remote_preflight_allowed,
        remote_training_allowed=remote_training_allowed,
        blockers=blockers,
        preflight_manifest=preflight_manifest,
    )
    return {
        "schema_version": 1,
        "packet_name": "module2_v2_remote_execution_packet",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_training": False,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": bool(remote_preflight_allowed),
        "remote_training_allowed_now": bool(remote_training_allowed),
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "ready_to_run_remote_preflight": bool(remote_preflight_allowed),
        "ready_to_run_remote_training": False,
        "inputs": {
            "readiness_gate": str(config.readiness_gate_path),
            "promotion_packet": str(config.promotion_packet_path),
            "promotion_dry_run": str(config.promotion_dry_run_path),
            "source_freshness": str(config.source_freshness_path),
            "remote_readiness": str(config.remote_readiness_path),
            "contract": str(config.contract_path),
            "preflight_manifest": str(config.preflight_manifest_path),
        },
        "contract_status": contract_status,
        "gate_summary": {
            "readiness_status": readiness.get("status"),
            "promotion_packet_status": promotion.get("status"),
            "promotion_dry_run_status": dry_run.get("status"),
            "source_freshness_status": source_freshness.get("status"),
            "preflight_status": preflight_manifest.get("preflight_status"),
            "preflight_formal_trial_ready": bool(preflight_manifest.get("formal_trial_ready")),
        },
        "blocker_count": len(blockers),
        "blockers": blockers,
        "execution_environment": {
            "gpu_alias": config.gpu_alias,
            "remote_workdir": config.remote_workdir,
            "remote_python": config.remote_python,
            "local_root": str(config.local_root),
            "training_host_required": config.gpu_alias,
        },
        "command_plan": command_plan,
        "expected_pullback_artifacts": _expected_pullback_artifacts(config.attempt_dir),
        "post_packet_next_requirements": [
            "remote_preflight_manifest_ready_before_training",
            "remote_training_completion_before_audit",
            "gate3_formal_audit_pass_before_h02",
            "h02_formal_output_accepted_true_before_paper_results",
        ],
        "invalid_substitutes": [
            "local PPO training output",
            "old v1 remote execution packet",
            "failed gate3_obstacle_summary_warm_approved_v1 checkpoint",
            "remote preflight smoke",
            "paper table or appendix prose",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 v2 remote execution packet without running remote commands.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--packet-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--readiness-gate", type=Path, default=DEFAULT_READINESS_GATE)
    parser.add_argument("--promotion-packet", type=Path, default=DEFAULT_PROMOTION_PACKET)
    parser.add_argument("--promotion-dry-run", type=Path, default=DEFAULT_DRY_RUN)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remote-readiness", type=Path, default=DEFAULT_REMOTE_READINESS)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--oracle-path", type=Path, default=DEFAULT_ORACLE_PATH)
    parser.add_argument("--bc-checkpoint", type=Path, default=DEFAULT_BC_CHECKPOINT)
    parser.add_argument("--attempt-dir", type=Path, default=DEFAULT_ATTEMPT_DIR)
    parser.add_argument("--preflight-manifest", type=Path, default=DEFAULT_PREFLIGHT_MANIFEST)
    parser.add_argument("--gpu-alias", default=DEFAULT_GPU_ALIAS)
    parser.add_argument("--remote-workdir", default=DEFAULT_REMOTE_WORKDIR)
    parser.add_argument("--remote-python", default=DEFAULT_REMOTE_PYTHON)
    parser.add_argument("--local-root", type=Path, default=DEFAULT_LOCAL_ROOT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _command_plan(config: Module2V2RemoteExecutionPacketConfig) -> dict[str, Any]:
    preflight_argv = _preflight_argv(config)
    runner_argv = _runner_argv(config)
    audit_argv = _audit_argv(config)
    return {
        "sync_to_remote": {
            "allowed_now": False,
            "runs_training": False,
            "command": _sync_command(config),
            "note": "No --delete is used; remote artifacts and virtualenvs are preserved.",
        },
        "run_remote_preflight": {
            "allowed_now": False,
            "runs_training": False,
            "command": _remote_python_command(config, preflight_argv),
        },
        "run_remote_training": {
            "allowed_now": False,
            "runs_training": True,
            "command": _remote_python_command(config, runner_argv),
        },
        "run_remote_audit": {
            "allowed_now": False,
            "runs_training": False,
            "command": _remote_python_command(config, audit_argv),
        },
        "pullback_after_audit": {
            "allowed_now": False,
            "runs_training": False,
            "command": _pullback_command(config),
        },
    }


def _preflight_argv(config: Module2V2RemoteExecutionPacketConfig) -> list[str]:
    return [
        "-m",
        "forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial",
        "--output-dir",
        str(config.attempt_dir),
        "--manifest-out",
        str(config.preflight_manifest_path),
        "--contract-path",
        str(config.contract_path),
        "--seed",
        "20260706",
        "--device",
        "cuda",
        "--oracle-path",
        str(config.oracle_path),
        "--heldout-seed",
        "20260706",
        "--train-total-timesteps",
        "500000",
        "--train-n-envs",
        "4",
        "--train-n-steps",
        "256",
        "--train-batch-size",
        "256",
        "--train-n-epochs",
        "8",
        "--train-learning-rate",
        "0.0001",
        "--train-ent-coef",
        "0.01",
        "--train-checkpoint-freq",
        "25000",
        "--eval-episodes",
        "64",
        "--eval-min-episodes",
        "64",
        "--eval-success-threshold",
        "0.8",
        "--bc-checkpoint",
        str(config.bc_checkpoint),
        "--warm-start-decision",
        "approved_obstacle_summary",
        "--allow-existing-output-dir",
        "--allow-duplicate-openmp",
    ]


def _runner_argv(config: Module2V2RemoteExecutionPacketConfig) -> list[str]:
    return [
        "-m",
        "forest_n3p.scripts.run_rl_rs_gate3_trial",
        "--output-dir",
        str(config.attempt_dir),
        "--contract-path",
        str(config.contract_path),
        "--seed",
        "20260706",
        "--device",
        "cuda",
        "--train-curriculum-preset",
        "f03",
        "--eval-curriculum-preset",
        "f03",
        "--oracle-path",
        str(config.oracle_path),
        "--heldout-seed",
        "20260706",
        "--train-total-timesteps",
        "500000",
        "--train-n-envs",
        "4",
        "--train-n-steps",
        "256",
        "--train-batch-size",
        "256",
        "--train-n-epochs",
        "8",
        "--train-learning-rate",
        "0.0001",
        "--train-ent-coef",
        "0.01",
        "--train-checkpoint-freq",
        "25000",
        "--eval-episodes",
        "64",
        "--eval-min-episodes",
        "64",
        "--eval-success-threshold",
        "0.8",
        "--bc-checkpoint",
        str(config.bc_checkpoint),
        "--allow-duplicate-openmp",
    ]


def _audit_argv(config: Module2V2RemoteExecutionPacketConfig) -> list[str]:
    return [
        "-m",
        "forest_n3p.scripts.audit_rl_rs_gate3_trial",
        "--trial-dir",
        str(config.attempt_dir),
        "--contract-path",
        str(config.contract_path),
        "--min-formal-episodes",
        "64",
        "--required-success-threshold",
        "0.8",
        "--required-train-curriculum",
        "f03",
        "--required-eval-curriculum",
        "f03",
        "--warm-start-decision",
        "approved_obstacle_summary",
    ]


def _blockers(
    *,
    readiness: dict[str, Any],
    promotion: dict[str, Any],
    dry_run: dict[str, Any],
    source_freshness: dict[str, Any],
    preflight_manifest: dict[str, Any],
    contract_status: str,
    remote_readiness_text: str,
    command_plan: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if contract_status not in {"approved", "frozen"}:
        blockers.append("v2_contract_not_promoted")
    if readiness.get("status") != READY_READINESS_STATUS:
        blockers.append("v2_contract_readiness_not_ready")
    if promotion.get("status") != READY_PROMOTION_PACKET_STATUS:
        blockers.append("promotion_packet_not_ready")
    if dry_run.get("status") != READY_DRY_RUN_STATUS:
        blockers.append("promotion_dry_run_not_ready")
    if not _source_freshness_ready(source_freshness):
        blockers.append("source_freshness_not_ready")
    if "gpu3070ti-relay" not in remote_readiness_text or "RTX 3070 Ti" not in remote_readiness_text:
        blockers.append("remote_readiness_not_current")
    if not _commands_contain_v2_contract_and_params(command_plan):
        blockers.append("v2_command_plan_missing_required_args")
    if preflight_manifest and not _preflight_ready(preflight_manifest):
        blockers.append("v2_remote_preflight_not_ready")
    return _unique(blockers)


def _status(*, blockers: Sequence[str], readiness: dict[str, Any], source_freshness: dict[str, Any]) -> str:
    if "v2_contract_not_promoted" in blockers or readiness.get("status") != READY_READINESS_STATUS:
        return "blocked_until_v2_contract_promotion"
    if "source_freshness_not_ready" in blockers or not _source_freshness_ready(source_freshness):
        return "blocked_until_source_freshness"
    if blockers:
        return "blocked_pre_remote_preflight"
    return "ready_for_v2_remote_preflight"


def _annotate_commands(
    *,
    command_plan: dict[str, Any],
    readiness_ready: bool,
    source_ready: bool,
    remote_preflight_allowed: bool,
    remote_training_allowed: bool,
    blockers: Sequence[str],
    preflight_manifest: dict[str, Any],
) -> None:
    sync_blockers = [] if readiness_ready and source_ready else list(blockers)
    command_plan["sync_to_remote"]["allowed_now"] = bool(remote_preflight_allowed)
    command_plan["sync_to_remote"]["blocked_by"] = [] if remote_preflight_allowed else sync_blockers
    command_plan["run_remote_preflight"]["allowed_now"] = bool(remote_preflight_allowed)
    command_plan["run_remote_preflight"]["blocked_by"] = [] if remote_preflight_allowed else sync_blockers
    training_blockers = list(blockers)
    if not _preflight_ready(preflight_manifest):
        training_blockers.append("v2_remote_preflight_not_ready")
    command_plan["run_remote_training"]["allowed_now"] = bool(remote_training_allowed)
    command_plan["run_remote_training"]["blocked_by"] = [] if remote_training_allowed else _unique(training_blockers)
    audit_blockers = _unique([*training_blockers, "remote_training_not_completed"])
    command_plan["run_remote_audit"]["blocked_by"] = audit_blockers
    command_plan["pullback_after_audit"]["blocked_by"] = _unique([*audit_blockers, "remote_audit_not_completed"])


def _commands_contain_v2_contract_and_params(command_plan: dict[str, Any]) -> bool:
    joined = "\n".join(str(step.get("command") or "") for step in command_plan.values() if isinstance(step, dict))
    required = [
        "--contract-path",
        "--train-total-timesteps 500000",
        "--train-n-envs 4",
        "--train-learning-rate 0.0001",
        "--train-ent-coef 0.01",
        "--train-checkpoint-freq 25000",
        "--warm-start-decision approved_obstacle_summary",
    ]
    return all(item in joined for item in required)


def _preflight_ready(preflight_manifest: dict[str, Any]) -> bool:
    return preflight_manifest.get("preflight_status") == "ready" and preflight_manifest.get("formal_trial_ready") is True


def _source_freshness_ready(source_freshness: dict[str, Any]) -> bool:
    return str(source_freshness.get("status")) in SOURCE_FRESHNESS_READY_STATUSES


def _sync_command(config: Module2V2RemoteExecutionPacketConfig) -> str:
    return _join(
        [
            "rsync",
            "-az",
            "--exclude",
            ".git",
            f"{str(config.local_root).rstrip('/')}/",
            f"{config.gpu_alias}:{config.remote_workdir.rstrip('/')}/",
        ]
    )


def _pullback_command(config: Module2V2RemoteExecutionPacketConfig) -> str:
    return _join(
        [
            "rsync",
            "-az",
            f"{config.gpu_alias}:{config.remote_workdir.rstrip('/')}/{config.attempt_dir.as_posix()}/",
            f"{config.local_root / config.attempt_dir}/",
        ]
    )


def _remote_python_command(config: Module2V2RemoteExecutionPacketConfig, argv: Sequence[str]) -> str:
    remote = f"cd {shlex.quote(config.remote_workdir)} && PYTHONPATH=2_experiment {shlex.quote(config.remote_python)} {_join(argv)}"
    return _join(["ssh", config.gpu_alias, remote])


def _expected_pullback_artifacts(attempt_dir: Path) -> list[str]:
    return [
        str(attempt_dir / "train" / "final_model.zip"),
        str(attempt_dir / "train" / "final_model.zip.sha256"),
        str(attempt_dir / "train" / "summary.json"),
        str(attempt_dir / "train" / "training_manifest.json"),
        str(attempt_dir / "eval" / "gate3_eval_episodes.csv"),
        str(attempt_dir / "eval" / "gate3_summary.json"),
        str(attempt_dir / "gate3_trial_manifest.json"),
        str(attempt_dir / "gate3_formal_audit.json"),
    ]


def _contract_status(path: Path) -> str:
    text = _read_text(path)
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing" if not path.exists() else "unknown"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _join(parts: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in parts)


def _unique(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Remote Execution Packet",
        "",
        "This file packetizes remote commands only. It does not run preflight, train, audit, pull back artifacts, or write paper results.",
        "",
        "## Status",
        "",
        f"- status: `{packet['status']}`",
        f"- ready_to_run_remote_preflight: `{packet['ready_to_run_remote_preflight']}`",
        f"- ready_to_run_remote_training: `{packet['ready_to_run_remote_training']}`",
        f"- remote_training_allowed_now: `{packet['remote_training_allowed_now']}`",
        f"- blocker_count: `{packet['blocker_count']}`",
        "",
        "## Blockers",
        "",
    ]
    if packet["blockers"]:
        lines.extend(f"- `{blocker}`" for blocker in packet["blockers"])
    else:
        lines.append("- none")
    lines.extend(["", "## Command Plan", ""])
    for step_id, step in packet["command_plan"].items():
        lines.append(f"### `{step_id}`")
        lines.append(f"- allowed_now: `{step['allowed_now']}`")
        lines.append(f"- runs_training: `{step['runs_training']}`")
        lines.append(f"- blocked_by: `{', '.join(step.get('blocked_by', []))}`")
        lines.append("")
        lines.append("```bash")
        lines.append(str(step["command"]))
        lines.append("```")
        lines.append("")
    lines.extend(["## Invalid Substitutes", ""])
    lines.extend(f"- {item}" for item in packet["invalid_substitutes"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
