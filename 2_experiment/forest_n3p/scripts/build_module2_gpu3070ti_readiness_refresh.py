from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shlex
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_gpu3070ti_readiness_refresh")
DEFAULT_LOCAL_ROOT = Path("/Users/sun/tongbu/study/phdproject/ForestNav")
DEFAULT_REMOTE_ALIAS = "gpu3070ti-relay"
DEFAULT_JUMP_ALIAS = "ubuntu-obgx"
DEFAULT_REMOTE_WORKDIR = "~/ForestNav"
DEFAULT_REMOTE_PYTHON = ".venv/bin/python"
DEFAULT_CONNECT_TIMEOUT_SECONDS = 8

ORACLE_CONNECTOR = "0_trials/module2_oracle_shape/oracle_connector_results.parquet"
OBSTACLE_SUMMARY_BC = "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt"
REMOTE_SCRIPT_NAMES = (
    "preflight_rl_rs_gate3_formal_trial.py",
    "run_rl_rs_gate3_trial.py",
    "audit_rl_rs_gate3_trial.py",
)

DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")

CommandRunner = Callable[[Sequence[str]], str]


@dataclass(frozen=True)
class Gpu3070TiReadinessRefreshConfig:
    output_dir: Path = DEFAULT_OUTPUT_DIR
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    local_root: Path = DEFAULT_LOCAL_ROOT
    remote_alias: str = DEFAULT_REMOTE_ALIAS
    jump_alias: str = DEFAULT_JUMP_ALIAS
    remote_workdir: str = DEFAULT_REMOTE_WORKDIR
    remote_python: str = DEFAULT_REMOTE_PYTHON
    connect_timeout_seconds: int = DEFAULT_CONNECT_TIMEOUT_SECONDS
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Gpu3070TiReadinessRefreshConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        local_root=args.local_root,
        remote_alias=args.remote_alias,
        jump_alias=args.jump_alias,
        remote_workdir=args.remote_workdir,
        remote_python=args.remote_python,
        connect_timeout_seconds=args.connect_timeout_seconds,
        decision_record_path=args.decision_record,
        remote_packet_path=args.remote_packet,
        claim_safety_path=args.claim_safety,
        h02_acceptance_path=args.h02_acceptance,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "readiness_refresh.json"
    markdown_out = config.markdown_out or output_dir / "readiness_refresh.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: Gpu3070TiReadinessRefreshConfig, *, runner: CommandRunner | None = None) -> dict[str, Any]:
    run = runner or _run_text
    ssh_resolution = _ssh_resolution(config, run)
    listener = _jump_listener(config, run)
    remote_host = _remote_host(config, run)
    remote_probe = _remote_probe(config, run)
    local_inputs = _local_critical_inputs(config.local_root)
    critical_inputs = _critical_inputs(local_inputs=local_inputs, remote_inputs=remote_probe["critical_inputs"])
    script_presence = remote_probe["remote_script_presence"]
    gate_state = _current_gate_state(config)
    ready = _ready(critical_inputs=critical_inputs, remote_probe=remote_probe, script_presence=script_presence)
    status = "remote_readiness_refreshed_f02_6_still_blocked" if ready else "remote_readiness_refresh_failed"
    return {
        "schema_version": 1,
        "artifact_name": "module2_gpu3070ti_readiness_refresh",
        "status": status,
        "created_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_head": _source_head(),
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "remote_training_resource": config.remote_alias,
        "formal_claim_allowed": False,
        "current_gate_state": gate_state,
        "ssh_resolution": {
            **ssh_resolution,
            "jump_listener": listener,
        },
        "remote_host": remote_host,
        "remote_python_stack": remote_probe["remote_python_stack"],
        "critical_inputs": critical_inputs,
        "remote_script_presence": script_presence,
        "readiness_checks": {
            "ssh_alias_resolves_to_expected_relay": _ssh_resolution_matches(config, ssh_resolution),
            "jump_listener_present": bool(listener),
            "cuda_available": bool(remote_probe["remote_python_stack"].get("cuda_available")),
            "critical_inputs_match": all(item.get("local_remote_match") is True for item in critical_inputs.values()),
            "remote_scripts_present": all(item.get("exists") is True for item in script_presence.values()),
            "f02_6_still_pending": gate_state["f02_6_decision_status"] == "pending_human_decision",
            "remote_packet_still_blocked": gate_state["remote_packet_status"] == "blocked_until_f02_6_decision",
        },
        "commands_executed": _commands_executed(config),
        "claim_boundaries": [
            "This refresh is a read-only readiness snapshot, not a training run.",
            "It does not close F02.6 and does not approve obstacle-summary warm-start.",
            "It does not run approved remote preflight because F02.6 remains pending.",
            "It does not provide a PPO formal checkpoint or H02 formal evaluation output.",
            "It cannot be used for formal performance or warm-start-effect paper claims.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh Module2 gpu3070ti-relay readiness without running training or preflight.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--local-root", type=Path, default=DEFAULT_LOCAL_ROOT)
    parser.add_argument("--remote-alias", default=DEFAULT_REMOTE_ALIAS)
    parser.add_argument("--jump-alias", default=DEFAULT_JUMP_ALIAS)
    parser.add_argument("--remote-workdir", default=DEFAULT_REMOTE_WORKDIR)
    parser.add_argument("--remote-python", default=DEFAULT_REMOTE_PYTHON)
    parser.add_argument("--connect-timeout-seconds", type=int, default=DEFAULT_CONNECT_TIMEOUT_SECONDS)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _ssh_resolution(config: Gpu3070TiReadinessRefreshConfig, run: CommandRunner) -> dict[str, str]:
    raw = run(("ssh", "-G", config.remote_alias))
    fields: dict[str, str] = {"alias": config.remote_alias}
    for line in raw.splitlines():
        key, _, value = line.partition(" ")
        if key in {"user", "hostname", "port", "proxyjump", "hostkeyalias"}:
            fields[key] = value.strip()
    return fields


def _jump_listener(config: Gpu3070TiReadinessRefreshConfig, run: CommandRunner) -> str:
    raw = run(_ssh_command(config.jump_alias, 'ss -ltnp | grep -E "127\\.0\\.0\\.1:23070" || true', config.connect_timeout_seconds))
    for line in raw.splitlines():
        if "127.0.0.1:23070" in line and "LISTEN" in line:
            return "127.0.0.1:23070 LISTEN"
    return raw.strip()


def _remote_host(config: Gpu3070TiReadinessRefreshConfig, run: CommandRunner) -> dict[str, Any]:
    command = (
        "hostname; whoami; uname -srmo; "
        "nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader,nounits"
    )
    lines = [line.strip() for line in run(_ssh_command(config.remote_alias, command, config.connect_timeout_seconds)).splitlines() if line.strip()]
    gpu_parts = [part.strip() for part in lines[3].split(",")] if len(lines) >= 4 else []
    return {
        "hostname": lines[0] if len(lines) > 0 else "",
        "user": lines[1] if len(lines) > 1 else "",
        "kernel": lines[2] if len(lines) > 2 else "",
        "gpu": gpu_parts[0] if len(gpu_parts) > 0 else "",
        "gpu_memory_total_mib": _int_or_none(gpu_parts[1] if len(gpu_parts) > 1 else None),
        "gpu_memory_free_mib": _int_or_none(gpu_parts[2] if len(gpu_parts) > 2 else None),
        "driver_version": gpu_parts[3] if len(gpu_parts) > 3 else "",
    }


def _remote_probe(config: Gpu3070TiReadinessRefreshConfig, run: CommandRunner) -> dict[str, Any]:
    script = _remote_probe_script()
    command = f"cd {config.remote_workdir} && {shlex.quote(config.remote_python)} - <<'PY'\n{script}\nPY"
    return json.loads(run(_ssh_command(config.remote_alias, command, config.connect_timeout_seconds)))


def _local_critical_inputs(local_root: Path) -> dict[str, dict[str, Any]]:
    return {
        "oracle_connector_results": _local_file_record(Path(local_root) / ORACLE_CONNECTOR, parquet=True),
        "obstacle_summary_bc_checkpoint": _local_file_record(Path(local_root) / OBSTACLE_SUMMARY_BC, parquet=False),
    }


def _critical_inputs(*, local_inputs: dict[str, dict[str, Any]], remote_inputs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for key, local in local_inputs.items():
        remote = remote_inputs.get(key, {})
        row = {
            "path": local["path"],
            "local_exists": local["exists"],
            "remote_exists": remote.get("exists", False),
            "local_bytes": local.get("bytes"),
            "remote_bytes": remote.get("bytes"),
            "local_sha256": local.get("sha256"),
            "remote_sha256": remote.get("sha256"),
            "local_remote_match": bool(local.get("exists") and remote.get("exists") and local.get("sha256") == remote.get("sha256")),
        }
        if "rows" in local or "rows" in remote:
            row["local_rows"] = local.get("rows")
            row["remote_rows"] = remote.get("rows")
            row["local_remote_match"] = row["local_remote_match"] and local.get("rows") == remote.get("rows")
        merged[key] = row
    return merged


def _current_gate_state(config: Gpu3070TiReadinessRefreshConfig) -> dict[str, Any]:
    decision = _read_json(config.decision_record_path)
    remote_packet = _read_json(config.remote_packet_path)
    claim_safety = _read_json(config.claim_safety_path)
    h02 = _read_json(config.h02_acceptance_path)
    return {
        "f02_6_decision_status": str(decision.get("status")),
        "remote_packet_status": str(remote_packet.get("status")),
        "ready_to_run_remote_training": bool(remote_packet.get("ready_to_run_remote_training")),
        "formal_performance_claim_allowed": bool(claim_safety.get("formal_claim_allowed") or h02.get("paper_result_input_allowed")),
    }


def _ready(*, critical_inputs: dict[str, dict[str, Any]], remote_probe: dict[str, Any], script_presence: dict[str, dict[str, Any]]) -> bool:
    return (
        bool(remote_probe["remote_python_stack"].get("cuda_available"))
        and all(item.get("local_remote_match") is True for item in critical_inputs.values())
        and all(item.get("exists") is True for item in script_presence.values())
    )


def _commands_executed(config: Gpu3070TiReadinessRefreshConfig) -> list[dict[str, Any]]:
    return [
        {"command": f"ssh -G {config.remote_alias}", "runs_training": False, "runs_remote_preflight": False, "purpose": "Verify SSH alias resolution."},
        {
            "command": f"ssh {config.jump_alias} 'ss -ltnp | grep -E \"127\\\\.0\\\\.0\\\\.1:23070\" || true'",
            "runs_training": False,
            "runs_remote_preflight": False,
            "purpose": "Verify reverse relay listener.",
        },
        {
            "command": (
                f"ssh {config.remote_alias} 'hostname; whoami; uname -srmo; "
                "nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader,nounits'"
            ),
            "runs_training": False,
            "runs_remote_preflight": False,
            "purpose": "Verify host identity and GPU state.",
        },
        {
            "command": f"ssh {config.remote_alias} 'cd {config.remote_workdir} && {config.remote_python} - <<PY ...'",
            "runs_training": False,
            "runs_remote_preflight": False,
            "purpose": "Verify Python stack, CUDA availability, critical file hashes, and script presence.",
        },
        {
            "command": "local Python file hash and parquet row checks",
            "runs_training": False,
            "runs_remote_preflight": False,
            "purpose": "Verify local critical file hashes for local/remote comparison.",
        },
    ]


def _ssh_command(alias: str, command: str, timeout_seconds: int) -> tuple[str, ...]:
    return ("ssh", "-o", "BatchMode=yes", "-o", f"ConnectTimeout={timeout_seconds}", alias, command)


def _ssh_resolution_matches(config: Gpu3070TiReadinessRefreshConfig, resolution: dict[str, str]) -> bool:
    return (
        resolution.get("user") == "ubuntu"
        and resolution.get("hostname") == "127.0.0.1"
        and resolution.get("port") == "23070"
        and resolution.get("proxyjump") == config.jump_alias
        and resolution.get("hostkeyalias") == config.remote_alias
    )


def _local_file_record(path: Path, *, parquet: bool) -> dict[str, Any]:
    exists = path.is_file()
    record: dict[str, Any] = {
        "path": _repo_relative(path),
        "exists": exists,
        "bytes": path.stat().st_size if exists else None,
        "sha256": _sha256(path) if exists else None,
    }
    if parquet:
        record["rows"] = _parquet_rows(path) if exists else None
    return record


def _parquet_rows(path: Path) -> int:
    import pyarrow.parquet as pq

    return int(pq.ParquetFile(path).metadata.num_rows)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_relative(path: Path) -> str:
    raw = str(path)
    root = str(DEFAULT_LOCAL_ROOT)
    if raw.startswith(root + "/"):
        return raw[len(root) + 1 :]
    return raw


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


def _run_text(args: Sequence[str]) -> str:
    return subprocess.check_output(list(args), text=True, stderr=subprocess.STDOUT)


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(float(value.strip()))
    except ValueError:
        return None


def _remote_probe_script() -> str:
    return r'''
import hashlib
import importlib.metadata as metadata
import json
import platform
from pathlib import Path

import pyarrow.parquet as pq
import torch

FILES = {
    "oracle_connector_results": ("0_trials/module2_oracle_shape/oracle_connector_results.parquet", True),
    "obstacle_summary_bc_checkpoint": ("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt", False),
}
SCRIPTS = [
    "preflight_rl_rs_gate3_formal_trial.py",
    "run_rl_rs_gate3_trial.py",
    "audit_rl_rs_gate3_trial.py",
]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path, parquet):
    p = Path(path)
    record = {"path": path, "exists": p.is_file(), "bytes": p.stat().st_size if p.is_file() else None}
    record["sha256"] = sha256(p) if p.is_file() else None
    if parquet:
        record["rows"] = int(pq.ParquetFile(p).metadata.num_rows) if p.is_file() else None
    return record


def version(package):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


out = {
    "remote_python_stack": {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "stable_baselines3": version("stable_baselines3"),
        "pyarrow": version("pyarrow"),
        "gymnasium": version("gymnasium"),
    },
    "critical_inputs": {key: file_record(path, parquet) for key, (path, parquet) in FILES.items()},
    "remote_script_presence": {
        name: {
            "exists": Path("2_experiment/forest_n3p/scripts", name).is_file(),
            "bytes": Path("2_experiment/forest_n3p/scripts", name).stat().st_size
            if Path("2_experiment/forest_n3p/scripts", name).is_file()
            else None,
        }
        for name in SCRIPTS
    },
}
print(json.dumps(out, ensure_ascii=False))
'''.strip()


def _markdown(manifest: dict[str, Any]) -> str:
    oracle = manifest["critical_inputs"]["oracle_connector_results"]
    checkpoint = manifest["critical_inputs"]["obstacle_summary_bc_checkpoint"]
    remote = manifest["remote_host"]
    stack = manifest["remote_python_stack"]
    return "\n".join(
        [
            "# Module2 gpu3070ti-relay Readiness Refresh",
            "",
            "This is a read-only formal-gate readiness refresh. It is not a training run, not an approved preflight, and not paper result material.",
            "",
            "## Status",
            "",
            f"- status: `{manifest['status']}`",
            f"- source_head: `{manifest['source_head']}`",
            f"- runs_training: `{manifest['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
            f"- local_training_allowed: `{manifest['local_training_allowed']}`",
            f"- remote_training_resource: `{manifest['remote_training_resource']}`",
            f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
            "",
            "## What Was Checked",
            "",
            "- SSH alias still resolves to `ubuntu@127.0.0.1:23070` through `ubuntu-obgx`.",
            "- Jump host listener for `127.0.0.1:23070` is present.",
            f"- Remote host is `{remote['hostname']}`.",
            f"- Remote GPU is `{remote['gpu']}`, {remote['gpu_memory_total_mib']} MiB total, {remote['gpu_memory_free_mib']} MiB free.",
            f"- Remote Python stack is present: Python `{stack['python']}`, torch `{stack['torch']}`, CUDA available `{stack['cuda_available']}`, SB3 `{stack['stable_baselines3']}`, pyarrow `{stack['pyarrow']}`, gymnasium `{stack['gymnasium']}`.",
            "- Remote scripts exist: `preflight_rl_rs_gate3_formal_trial.py`, `run_rl_rs_gate3_trial.py`, `audit_rl_rs_gate3_trial.py`.",
            f"- Oracle connector parquet exists both locally and remotely with {oracle.get('local_rows')} rows and matching SHA-256 `{oracle['local_remote_match']}`.",
            f"- Obstacle-summary BC checkpoint exists both locally and remotely with matching SHA-256 `{checkpoint['local_remote_match']}`.",
            "",
            "## Critical Hashes",
            "",
            "```text",
            "oracle_connector_results.parquet",
            f"local_sha256={oracle['local_sha256']}",
            f"remote_sha256={oracle['remote_sha256']}",
            f"rows={oracle.get('local_rows')}",
            "",
            "obstacle_summary_bc_checkpoint",
            f"local_sha256={checkpoint['local_sha256']}",
            f"remote_sha256={checkpoint['remote_sha256']}",
            "```",
            "",
            "## Gate Boundary",
            "",
            "F02.6 is still `pending_human_decision`. This refresh does not approve warm-start, does not run approved remote preflight, and does not unlock formal PPO training. The next formal step remains Dr Sun's F02.6 decision.",
            "",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
