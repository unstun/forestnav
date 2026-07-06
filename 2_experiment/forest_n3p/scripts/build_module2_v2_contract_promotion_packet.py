from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_contract_readiness_gate import (
    DEFAULT_CONTRACT_PATH,
    DEFAULT_GAP_LEDGER_PATH,
    DEFAULT_ORACLE_PATH,
    EXPECTED_PROTOCOL_LANE,
    READY_CONTRACT_STATUSES,
)


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_contract_promotion_packet")
DEFAULT_READINESS_GATE = Path("0_trials/module2_v2_contract_readiness_gate/v2_contract_readiness_gate.json")
DEFAULT_REMOTE_READINESS = Path("0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.md")
DEFAULT_ALIASES = ("gpu3070ti-relay", "gpu3070ti-reply")
EXPECTED_BLOCKER_FOR_DRAFT = "contract_status_not_approved_or_frozen"
EXPECTED_BUDGET = {
    "seed": 20260706,
    "train_total_timesteps": 500000,
    "train_n_envs": 4,
    "train_n_steps": 256,
    "train_batch_size": 256,
    "train_n_epochs": 8,
    "train_learning_rate": 0.0001,
    "train_ent_coef": 0.01,
    "train_checkpoint_freq": 25000,
}
EXPECTED_UNSAFE_FAILURE_THRESHOLDS = {
    "collision_rate_gte": 0.30,
    "truncation_rate_gte": 0.20,
}


@dataclass(frozen=True)
class Module2V2ContractPromotionPacketConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    readiness_gate_path: Path = DEFAULT_READINESS_GATE
    gap_ledger_path: Path = DEFAULT_GAP_LEDGER_PATH
    remote_readiness_path: Path = DEFAULT_REMOTE_READINESS
    oracle_path: Path = DEFAULT_ORACLE_PATH
    aliases: tuple[str, ...] = DEFAULT_ALIASES


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2ContractPromotionPacketConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        readiness_gate_path=args.readiness_gate,
        gap_ledger_path=args.gap_ledger,
        remote_readiness_path=args.remote_readiness,
        oracle_path=args.oracle_path,
        aliases=tuple(args.aliases),
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_contract_promotion_packet.json"
    markdown_out = config.markdown_out or output_dir / "v2_contract_promotion_packet.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(
        json.dumps(
            {"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(config: Module2V2ContractPromotionPacketConfig) -> dict[str, Any]:
    readiness_gate = _read_json(config.readiness_gate_path)
    contract_text = _read_text(config.contract_path)
    remote_readiness_text = _read_text(config.remote_readiness_path)
    alias_records = _ssh_config_records(config.aliases)
    audit_issues = _audit_issues(
        config=config,
        readiness_gate=readiness_gate,
        contract_text=contract_text,
        remote_readiness_text=remote_readiness_text,
        alias_records=alias_records,
    )
    approval_items = _approval_items(alias_records=alias_records)
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_contract_promotion_packet",
        "status": "v2_contract_promotion_packet_ready_awaiting_dr_sun" if not audit_issues else "v2_contract_promotion_packet_audit_failed",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "writes_contract": False,
        "approves_contract": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "contract_promotion_allowed_by_packet": False,
        "inputs": {
            "contract": str(config.contract_path),
            "readiness_gate": str(config.readiness_gate_path),
            "gap_ledger": str(config.gap_ledger_path),
            "remote_readiness": str(config.remote_readiness_path),
            "oracle_path": str(config.oracle_path),
        },
        "current_gate": _current_gate(readiness_gate),
        "remote_alias_evidence": _remote_alias_evidence(alias_records=alias_records, remote_readiness_text=remote_readiness_text),
        "approval_item_count": len(approval_items),
        "approval_items": approval_items,
        "post_approval_next_steps": [
            "commit the contract status promotion to approved or frozen",
            "re-run v2 contract readiness gate and require v2_contract_ready_for_source_freshness",
            "regenerate source-freshness artifacts from the post-promotion commit",
            "generate the v2 remote execution packet",
            "run remote preflight only after the regenerated packet allows it",
        ],
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Dr Sun approval packet for the Module2 v2 stronger warm-start contract.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--readiness-gate", type=Path, default=DEFAULT_READINESS_GATE)
    parser.add_argument("--gap-ledger", type=Path, default=DEFAULT_GAP_LEDGER_PATH)
    parser.add_argument("--remote-readiness", type=Path, default=DEFAULT_REMOTE_READINESS)
    parser.add_argument("--oracle-path", type=Path, default=DEFAULT_ORACLE_PATH)
    parser.add_argument("--aliases", nargs="+", default=list(DEFAULT_ALIASES))
    return parser.parse_args(list(argv) if argv is not None else None)


def _approval_items(*, alias_records: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "item_id": "remote_alias",
            "status": "awaiting_dr_sun_confirmation",
            "recommended_value": _recommended_alias(alias_records),
            "options": list(DEFAULT_ALIASES),
            "evidence": "local ssh -G shows gpu3070ti-relay has ProxyJump/localhost:23070, while gpu3070ti-reply resolves as a direct hostname unless Dr Sun provides another route",
            "promotion_effect": "sets the remote route used by source-freshness and remote packet generation",
        },
        {
            "item_id": "training_budget",
            "status": "awaiting_dr_sun_approval",
            "recommended_value": EXPECTED_BUDGET,
            "promotion_effect": "locks the stronger PPO budget before any remote run",
        },
        {
            "item_id": "unsafe_failure_thresholds",
            "status": "awaiting_dr_sun_approval",
            "recommended_value": EXPECTED_UNSAFE_FAILURE_THRESHOLDS,
            "promotion_effect": "locks independent failure criteria before seeing new rollout results",
        },
        {
            "item_id": "contract_status_action",
            "status": "awaiting_dr_sun_approval",
            "options": sorted(READY_CONTRACT_STATUSES),
            "recommended_value": "approved",
            "promotion_effect": "allows only the next source-freshness gate, not immediate remote training",
        },
    ]


def _current_gate(readiness_gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": readiness_gate.get("status"),
        "source_head": readiness_gate.get("source_head"),
        "next_action": readiness_gate.get("next_action"),
        "blocker_count": readiness_gate.get("blocker_count"),
        "blockers": [str(item.get("issue_id")) for item in readiness_gate.get("blockers", []) if isinstance(item, dict)],
        "runner_command_contains_v2_params": bool(readiness_gate.get("runner_command_contains_v2_params")),
        "remote_training_allowed_now": bool(readiness_gate.get("remote_training_allowed_now")),
    }


def _remote_alias_evidence(*, alias_records: dict[str, dict[str, str]], remote_readiness_text: str) -> dict[str, Any]:
    return {
        "recommended_alias": _recommended_alias(alias_records),
        "ssh_config_records": alias_records,
        "readiness_artifact_mentions_gpu3070ti_relay": "gpu3070ti-relay" in remote_readiness_text,
        "readiness_artifact_mentions_rtx_3070_ti": "RTX 3070 Ti" in remote_readiness_text,
    }


def _audit_issues(
    *,
    config: Module2V2ContractPromotionPacketConfig,
    readiness_gate: dict[str, Any],
    contract_text: str,
    remote_readiness_text: str,
    alias_records: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not config.contract_path.exists():
        issues.append(_issue("contract_missing", "v2 contract file is missing", observed=str(config.contract_path)))
    if not config.readiness_gate_path.exists():
        issues.append(_issue("readiness_gate_missing", "v2 readiness gate is missing", observed=str(config.readiness_gate_path)))
    if not config.gap_ledger_path.exists():
        issues.append(_issue("gap_ledger_missing", "v2 gap ledger is missing", observed=str(config.gap_ledger_path)))
    if not config.remote_readiness_path.exists():
        issues.append(_issue("remote_readiness_missing", "gpu3070ti readiness artifact is missing", observed=str(config.remote_readiness_path)))
    if readiness_gate.get("status") != "v2_contract_readiness_blocked":
        issues.append(
            _issue(
                "readiness_gate_not_in_expected_draft_blocked_state",
                "promotion packet expects the current gate to be blocked only by draft status",
                observed=readiness_gate.get("status"),
                expected="v2_contract_readiness_blocked",
            )
        )
    if readiness_gate.get("blocker_count") != 1:
        issues.append(
            _issue(
                "readiness_gate_blocker_count_not_one",
                "promotion packet expects exactly one readiness blocker before approval",
                observed=readiness_gate.get("blocker_count"),
                expected=1,
            )
        )
    blockers = [str(item.get("issue_id")) for item in readiness_gate.get("blockers", []) if isinstance(item, dict)]
    if blockers != [EXPECTED_BLOCKER_FOR_DRAFT]:
        issues.append(
            _issue(
                "readiness_gate_blocker_not_contract_status",
                "promotion packet expects the only blocker to be draft contract status",
                observed=blockers,
                expected=[EXPECTED_BLOCKER_FOR_DRAFT],
            )
        )
    if not bool(readiness_gate.get("runner_command_contains_v2_params")):
        issues.append(_issue("runner_command_v2_params_not_verified", "readiness gate did not verify v2 runner parameters"))
    if bool(readiness_gate.get("remote_training_allowed_now")):
        issues.append(_issue("remote_training_allowed_before_contract_promotion", "readiness gate must not allow remote training"))
    for required in [
        EXPECTED_PROTOCOL_LANE,
        "500000",
        "collision_rate >= 0.30",
        "truncation_rate >= 0.20",
        "approved",
        "frozen",
    ]:
        if required not in contract_text:
            issues.append(_issue("contract_promotion_evidence_missing", f"contract text missing {required!r}", observed=required))
    relay = alias_records.get("gpu3070ti-relay", {})
    if relay.get("proxyjump") in {None, "", "none"} or relay.get("hostname") != "127.0.0.1":
        issues.append(
            _issue(
                "gpu3070ti_relay_ssh_config_not_ready",
                "gpu3070ti-relay should resolve through the local relay route before promotion",
                observed=relay,
            )
        )
    if "gpu3070ti-relay" not in remote_readiness_text or "RTX 3070 Ti" not in remote_readiness_text:
        issues.append(_issue("remote_readiness_artifact_missing_relay_gpu_evidence", "remote readiness artifact does not mention relay and RTX 3070 Ti evidence"))
    return _unique_issues(issues)


def _ssh_config_records(aliases: Sequence[str]) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for alias in aliases:
        records[str(alias)] = _ssh_config_record(str(alias))
    return records


def _ssh_config_record(alias: str) -> dict[str, str]:
    try:
        raw = subprocess.check_output(["ssh", "-G", alias], text=True, stderr=subprocess.DEVNULL)
    except Exception as exc:  # noqa: BLE001 - this is local evidence, not an execution blocker by itself.
        return {"alias": alias, "error": str(exc)}
    record = {"alias": alias}
    for line in raw.splitlines():
        if " " not in line:
            continue
        key, value = line.split(None, 1)
        if key in {"hostname", "user", "port", "proxyjump"}:
            record[key] = value
    return record


def _recommended_alias(alias_records: dict[str, dict[str, str]]) -> str:
    relay = alias_records.get("gpu3070ti-relay", {})
    if relay.get("hostname") == "127.0.0.1" and relay.get("proxyjump") not in {None, "", "none"}:
        return "gpu3070ti-relay"
    return "requires_dr_sun_confirmation"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _issue(issue_id: str, message: str, *, observed: Any | None = None, expected: Any | None = None) -> dict[str, Any]:
    issue = {"issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
    if expected is not None:
        issue["expected"] = expected
    return issue


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id") or "")
        if issue_id and issue_id not in seen:
            seen.add(issue_id)
            out.append(dict(issue))
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Contract Promotion Packet",
        "",
        "This file is an approval packet for Dr Sun. It does not approve the contract, run preflight, run training, or write paper results.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- contract_promotion_allowed_by_packet: `{manifest['contract_promotion_allowed_by_packet']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        "",
        "## Current Gate",
        "",
    ]
    for key, value in manifest["current_gate"].items():
        lines.append(f"- {key}: `{_fmt(value)}`")
    lines.extend(["", "## Remote Alias Evidence", ""])
    alias_evidence = manifest["remote_alias_evidence"]
    lines.append(f"- recommended_alias: `{alias_evidence['recommended_alias']}`")
    for alias, record in alias_evidence["ssh_config_records"].items():
        lines.append(f"- {alias}: `{_fmt(record)}`")
    lines.extend(["", "## Approval Items", ""])
    for item in manifest["approval_items"]:
        lines.append(f"- `{item['item_id']}`: {item['status']} -> `{_fmt(item.get('recommended_value'))}`")
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Post-Approval Next Steps", ""])
    for step in manifest["post_approval_next_steps"]:
        lines.append(f"- {step}")
    return "\n".join(lines) + "\n"


def _fmt(value: Any) -> str:
    if isinstance(value, dict):
        return ", ".join(f"{key}={val}" for key, val in value.items())
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
