from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_remote_formal_execution_packet")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_REMOTE_PREFLIGHT = Path(
    "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json"
)
DEFAULT_GPU_ALIAS = "gpu3070ti-relay"
DEFAULT_REMOTE_WORKDIR = "~/ForestNav"
DEFAULT_REMOTE_PYTHON = ".venv/bin/python"
DEFAULT_LOCAL_ROOT = Path("/Users/sun/tongbu/study/phdproject/ForestNav")
DEFAULT_APPROVED_TRIAL_DIR = Path("0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1")


@dataclass(frozen=True)
class RemoteFormalExecutionPacketConfig:
    output_dir: Path
    packet_out: Path | None = None
    markdown_out: Path | None = None
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    remote_preflight_path: Path = DEFAULT_REMOTE_PREFLIGHT
    gpu_alias: str = DEFAULT_GPU_ALIAS
    remote_workdir: str = DEFAULT_REMOTE_WORKDIR
    remote_python: str = DEFAULT_REMOTE_PYTHON
    local_root: Path = DEFAULT_LOCAL_ROOT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = RemoteFormalExecutionPacketConfig(
        output_dir=args.output_dir,
        packet_out=args.packet_out,
        markdown_out=args.markdown_out,
        decision_record_path=args.decision_record,
        h01_manifest_path=args.h01_manifest,
        remote_preflight_path=args.remote_preflight,
        gpu_alias=args.gpu_alias,
        remote_workdir=args.remote_workdir,
        remote_python=args.remote_python,
        local_root=args.local_root,
    )
    packet = build_packet(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_out = config.packet_out or output_dir / "remote_formal_execution_packet.json"
    markdown_out = config.markdown_out or output_dir / "remote_formal_execution_packet.md"
    packet_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    packet_out.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(packet), encoding="utf-8")
    print(
        json.dumps(
            {"packet": str(packet_out), "markdown": str(markdown_out), "status": packet["status"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_packet(config: RemoteFormalExecutionPacketConfig) -> dict[str, Any]:
    decision_record = _read_json(config.decision_record_path)
    h01_manifest = _read_json(config.h01_manifest_path)
    remote_preflight = _read_json(config.remote_preflight_path)

    h01 = _h01_record(config.h01_manifest_path, h01_manifest)
    preflight = _preflight_record(config.remote_preflight_path, remote_preflight)
    decision = _decision_record(config.decision_record_path, decision_record)
    commands = _commands(config=config, decision_record=decision_record, remote_preflight=remote_preflight)
    blockers = _blockers(decision=decision, h01=h01, preflight=preflight)
    status = _status(decision=decision, blockers=blockers, preflight=preflight)
    ready = status == "ready_for_gpu3070ti_remote_training"

    commands["sync_to_remote"]["allowed_now"] = decision["status"] == "approved"
    commands["run_remote_preflight"]["allowed_now"] = decision["status"] == "approved"
    commands["run_remote_training"]["allowed_now"] = ready
    commands["run_remote_audit"]["allowed_now"] = ready

    return {
        "schema_version": 1,
        "packet_name": "module2_remote_formal_execution_packet",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "ready_to_run_remote_training": ready,
        "local_training_allowed": False,
        "formal_claim_allowed_before_audit": False,
        "blockers": blockers,
        "execution_environment": {
            "gpu_alias": config.gpu_alias,
            "remote_workdir": config.remote_workdir,
            "remote_python": config.remote_python,
            "local_root": str(config.local_root),
            "training_host_required": config.gpu_alias,
        },
        "decision_record": decision,
        "h01_manifest": h01,
        "remote_preflight": preflight,
        "execution_steps": commands,
        "post_run_pullback": _post_run_pullback(config=config, trial_dir=commands["trial_dir"]),
        "downstream_after_successful_audit": _downstream_after_successful_audit(commands["trial_dir"]),
        "claim_boundaries": [
            "This packet is an execution protocol, not a training result.",
            "It must not be used to run PPO on the local Mac.",
            "F02.6 approval by Dr Sun is required before warm-start formal training.",
            "Remote runner completion is still insufficient for a paper claim until formal audit passes and artifacts are pulled back.",
            "H01/H02 must be regenerated with the audited checkpoint before any formal performance table is written.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 remote formal execution packet.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--packet-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--remote-preflight", type=Path, default=DEFAULT_REMOTE_PREFLIGHT)
    parser.add_argument("--gpu-alias", default=DEFAULT_GPU_ALIAS)
    parser.add_argument("--remote-workdir", default=DEFAULT_REMOTE_WORKDIR)
    parser.add_argument("--remote-python", default=DEFAULT_REMOTE_PYTHON)
    parser.add_argument("--local-root", type=Path, default=DEFAULT_LOCAL_ROOT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _decision_record(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": str(record.get("status")),
        "effective_warm_start_decision": str(record.get("effective_warm_start_decision")),
        "remote_training_allowed": bool(record.get("remote_training_allowed")),
        "local_training_allowed": bool(record.get("local_training_allowed")),
        "formal_claim_allowed": bool(record.get("formal_claim_allowed")),
        "blockers": [str(item) for item in record.get("blockers", ()) if item],
    }


def _h01_record(path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    schema = manifest.get("required_output_schema") if isinstance(manifest.get("required_output_schema"), dict) else None
    schema_checks = {
        "required_output_schema": "present" if schema else "missing",
        "schema_status": schema.get("schema_status") if schema else None,
        "records_csv_required_columns": len(schema.get("records_csv_required_columns", ())) if schema else 0,
        "summary_by_method_bucket_required_columns": len(schema.get("summary_by_method_bucket_required_columns", ()))
        if schema
        else 0,
        "summary_json_required_sections": len(schema.get("summary_json_required_sections", ())) if schema else 0,
    }
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": str(manifest.get("status")),
        "blockers": [str(item) for item in manifest.get("blockers", ()) if item],
        "schema_checks": schema_checks,
    }


def _preflight_record(path: Path, preflight: dict[str, Any]) -> dict[str, Any]:
    formal_blockers = preflight.get("formal_blockers") if isinstance(preflight.get("formal_blockers"), list) else []
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "preflight_status": str(preflight.get("preflight_status")),
        "formal_trial_ready": bool(preflight.get("formal_trial_ready")),
        "warm_start_decision": str(preflight.get("warm_start_decision")),
        "blocker_codes": [str(item.get("code")) for item in formal_blockers if isinstance(item, dict) and item.get("code")],
    }


def _blockers(*, decision: dict[str, Any], h01: dict[str, Any], preflight: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if decision["local_training_allowed"]:
        blockers.append("decision_record_allows_local_training")
    if decision["status"] == "pending_human_decision":
        blockers.extend(decision["blockers"] or ["requires_dr_sun_approval"])
    elif decision["status"] != "approved":
        blockers.append(f"f02_6_decision_status_{decision['status']}")
    if decision["status"] == "approved" and not decision["remote_training_allowed"]:
        blockers.append("remote_training_not_allowed_by_decision_record")
    if h01["schema_checks"]["required_output_schema"] != "present":
        blockers.append("h01_required_output_schema_missing")
    elif h01["schema_checks"]["schema_status"] != "frozen_for_module2_v1":
        blockers.append("h01_required_output_schema_not_frozen")
    blockers.extend(h01["blockers"])
    if decision["status"] == "approved" and not preflight["formal_trial_ready"]:
        blockers.append("remote_formal_preflight_not_ready")
        blockers.extend(preflight["blocker_codes"])
    return _unique(blockers)


def _status(*, decision: dict[str, Any], blockers: Sequence[str], preflight: dict[str, Any]) -> str:
    if decision["status"] == "pending_human_decision":
        return "blocked_until_f02_6_decision"
    if decision["status"] != "approved":
        return "blocked_by_f02_6_decision"
    if "remote_formal_preflight_not_ready" in blockers or not preflight["formal_trial_ready"]:
        return "blocked_remote_preflight_not_ready"
    if blockers:
        return "blocked_preconditions"
    return "ready_for_gpu3070ti_remote_training"


def _commands(
    *,
    config: RemoteFormalExecutionPacketConfig,
    decision_record: dict[str, Any],
    remote_preflight: dict[str, Any],
) -> dict[str, Any]:
    approved_actions = _approved_actions(decision_record)
    preflight_command = str(approved_actions.get("preflight_command") or remote_preflight.get("command") or "")
    runner_command = str(approved_actions.get("runner_command_after_ready_preflight") or remote_preflight.get("runner_command") or "")
    audit_command = str(approved_actions.get("audit_command_after_ready_preflight") or remote_preflight.get("audit_command") or "")
    trial_dir = Path(_argument_value(runner_command, "--output-dir") or _argument_value(audit_command, "--trial-dir") or DEFAULT_APPROVED_TRIAL_DIR)
    return {
        "trial_dir": str(trial_dir),
        "sync_to_remote": {
            "allowed_now": False,
            "runs_training": False,
            "command": _sync_to_remote_command(config),
            "note": "No --delete: preserve remote virtualenvs and prior artifacts unless manually reviewed.",
        },
        "run_remote_preflight": {
            "allowed_now": False,
            "runs_training": False,
            "command": _remote_command(config, preflight_command),
        },
        "run_remote_training": {
            "allowed_now": False,
            "runs_training": True,
            "command": _remote_command(config, runner_command),
        },
        "run_remote_audit": {
            "allowed_now": False,
            "runs_training": False,
            "command": _remote_command(config, audit_command),
        },
    }


def _approved_actions(decision_record: dict[str, Any]) -> dict[str, Any]:
    actions = decision_record.get("conditional_actions") if isinstance(decision_record.get("conditional_actions"), dict) else {}
    approved = actions.get("if_approved_obstacle_summary") if isinstance(actions.get("if_approved_obstacle_summary"), dict) else {}
    return approved


def _post_run_pullback(*, config: RemoteFormalExecutionPacketConfig, trial_dir: str) -> dict[str, Any]:
    trial = Path(trial_dir)
    expected = [
        trial / "train/final_model.zip",
        trial / "train/summary.json",
        trial / "train/training_manifest.json",
        trial / "eval/gate3_eval_episodes.csv",
        trial / "eval/gate3_summary.json",
        trial / "gate3_trial_manifest.json",
        trial / "gate3_formal_audit.json",
    ]
    remote_path = f"{config.gpu_alias}:{config.remote_workdir.rstrip('/')}/{trial}/"
    local_path = f"{Path(config.local_root) / trial}/"
    return {
        "required_before_local_claim": True,
        "expected_artifacts": [str(item) for item in expected],
        "pullback_command": " ".join(shlex.quote(part) for part in ["rsync", "-az", remote_path, local_path]),
        "hash_manifest_required": True,
    }


def _downstream_after_successful_audit(trial_dir: str) -> dict[str, Any]:
    checkpoint = str(Path(trial_dir) / "train/final_model.zip")
    return {
        "h01_manifest_must_be_regenerated": True,
        "h02_full_smoke_must_be_regenerated": True,
        "paper_tables_must_be_regenerated_from_h02_formal_outputs": True,
        "checkpoint_candidate": checkpoint,
        "formal_claim_requires": [
            "gate3_formal_audit.formal_decision is pass",
            "pulled-back checkpoint hash is recorded",
            "H01 manifest status becomes ready_for_formal_run with this checkpoint",
            "H02 full all-method smoke and formal evaluation outputs include required_output_schema columns",
        ],
    }


def _sync_to_remote_command(config: RemoteFormalExecutionPacketConfig) -> str:
    local_root = str(Path(config.local_root)) + "/"
    remote_root = f"{config.gpu_alias}:{config.remote_workdir.rstrip('/')}/"
    argv = [
        "rsync",
        "-az",
        "--exclude",
        ".git",
        "--exclude",
        ".venv*",
        "--exclude",
        "__pycache__",
        "--exclude",
        ".pytest_cache",
        "--exclude",
        "1_survey",
        local_root,
        remote_root,
    ]
    return " ".join(shlex.quote(str(part)) for part in argv)


def _remote_command(config: RemoteFormalExecutionPacketConfig, command: str) -> str:
    if not command:
        return ""
    normalized = command
    if normalized.startswith("python "):
        normalized = f"{config.remote_python} {normalized[len('python ') :]}"
    shell_inner = f"cd {config.remote_workdir} && PYTHONPATH=2_experiment {normalized}"
    return " ".join(shlex.quote(str(part)) for part in ["ssh", config.gpu_alias, shell_inner])


def _argument_value(command: str, option: str) -> str | None:
    if not command:
        return None
    try:
        parts = shlex.split(command)
    except ValueError:
        return None
    for index, part in enumerate(parts[:-1]):
        if part == option:
            return parts[index + 1]
    return None


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop packet generation.
        return "unknown"


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
        "# Module2 Remote Formal Execution Packet",
        "",
        f"- status: `{packet['status']}`",
        f"- ready to run remote training: `{packet['ready_to_run_remote_training']}`",
        f"- local training allowed: `{packet['local_training_allowed']}`",
        f"- GPU alias: `{packet['execution_environment']['gpu_alias']}`",
        "",
        "## Blockers",
    ]
    if packet["blockers"]:
        lines.extend(f"- `{item}`" for item in packet["blockers"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Commands",
            "",
            "### Sync To Remote",
            "",
            "```bash",
            packet["execution_steps"]["sync_to_remote"]["command"],
            "```",
            "",
            "### Remote Training",
            "",
            "```bash",
            packet["execution_steps"]["run_remote_training"]["command"],
            "```",
            "",
            "### Remote Audit",
            "",
            "```bash",
            packet["execution_steps"]["run_remote_audit"]["command"],
            "```",
            "",
            "### Pull Back",
            "",
            "```bash",
            packet["post_run_pullback"]["pullback_command"],
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
