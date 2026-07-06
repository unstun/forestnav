from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit import DEFAULT_CONTRACT_PATH


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_post_promotion_regeneration_plan")
DEFAULT_CHAIN_AUDIT = Path("0_trials/module2_v2_formal_gate_chain_audit/v2_formal_gate_chain_audit.json")
DEFAULT_READINESS_GATE = Path("0_trials/module2_v2_contract_readiness_gate/v2_contract_readiness_gate.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_v2_remote_execution_packet/v2_remote_execution_packet.json")
DEFAULT_REMAINING_EVIDENCE = Path(
    "0_trials/module2_v2_formal_gate_remaining_evidence/v2_formal_gate_remaining_evidence.json"
)
DEFAULT_PROMOTION_DRY_RUN = Path("0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json")


@dataclass(frozen=True)
class Module2V2PostPromotionRegenerationPlanConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    chain_audit_path: Path = DEFAULT_CHAIN_AUDIT
    readiness_gate_path: Path = DEFAULT_READINESS_GATE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    remaining_evidence_path: Path = DEFAULT_REMAINING_EVIDENCE
    promotion_dry_run_path: Path = DEFAULT_PROMOTION_DRY_RUN


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2PostPromotionRegenerationPlanConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        chain_audit_path=args.chain_audit,
        readiness_gate_path=args.readiness_gate,
        source_freshness_path=args.source_freshness,
        remote_packet_path=args.remote_packet,
        remaining_evidence_path=args.remaining_evidence,
        promotion_dry_run_path=args.promotion_dry_run,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_post_promotion_regeneration_plan.json"
    markdown_out = config.markdown_out or output_dir / "v2_post_promotion_regeneration_plan.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: Module2V2PostPromotionRegenerationPlanConfig) -> dict[str, Any]:
    contract_status = _contract_status(config.contract_path)
    chain = _read_json(config.chain_audit_path)
    readiness = _read_json(config.readiness_gate_path)
    source_freshness = _read_json(config.source_freshness_path)
    remote_packet = _read_json(config.remote_packet_path)
    remaining = _read_json(config.remaining_evidence_path)
    dry_run = _read_json(config.promotion_dry_run_path)
    targets = _ordered_targets(
        contract_status=contract_status,
        chain=chain,
        readiness=readiness,
        source_freshness=source_freshness,
        remote_packet=remote_packet,
        remaining=remaining,
        dry_run=dry_run,
    )
    status = _status(contract_status=contract_status, chain=chain, targets=targets)
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_post_promotion_regeneration_plan",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "inputs": {
            "contract": str(config.contract_path),
            "chain_audit": str(config.chain_audit_path),
            "readiness_gate": str(config.readiness_gate_path),
            "source_freshness": str(config.source_freshness_path),
            "remote_packet": str(config.remote_packet_path),
            "remaining_evidence": str(config.remaining_evidence_path),
            "promotion_dry_run": str(config.promotion_dry_run_path),
        },
        "contract_status": contract_status,
        "chain_audit_summary": {
            "status": chain.get("status"),
            "current_blocking_stage_id": chain.get("current_blocking_stage_id"),
            "next_allowed_action": chain.get("next_allowed_action"),
            "audit_issue_count": int(chain.get("audit_issue_count") or 0),
        },
        "source_state_summary": {
            "readiness_status": readiness.get("status"),
            "source_freshness_status": source_freshness.get("status"),
            "remote_packet_status": remote_packet.get("status"),
            "remaining_evidence_status": remaining.get("status"),
            "promotion_dry_run_status": dry_run.get("status"),
        },
        "target_count": len(targets),
        "ready_target_count": sum(1 for target in targets if target["satisfied_now"]),
        "blocked_target_count": sum(1 for target in targets if not target["allowed_now"]),
        "ordered_targets": targets,
        "next_action": _next_action(targets),
        "invalid_substitutes": [
            "promotion dry-run treated as approval",
            "running source freshness before contract is approved or frozen",
            "old v1 remote execution packet",
            "remote preflight smoke",
            "remote training before ready preflight manifest",
            "paper result prose before H02 formal acceptance",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Module2 v2 post-promotion regeneration plan without executing it.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--chain-audit", type=Path, default=DEFAULT_CHAIN_AUDIT)
    parser.add_argument("--readiness-gate", type=Path, default=DEFAULT_READINESS_GATE)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--remaining-evidence", type=Path, default=DEFAULT_REMAINING_EVIDENCE)
    parser.add_argument("--promotion-dry-run", type=Path, default=DEFAULT_PROMOTION_DRY_RUN)
    return parser.parse_args(list(argv) if argv is not None else None)


def _ordered_targets(
    *,
    contract_status: str,
    chain: dict[str, Any],
    readiness: dict[str, Any],
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    remaining: dict[str, Any],
    dry_run: dict[str, Any],
) -> list[dict[str, Any]]:
    contract_promoted = contract_status in {"approved", "frozen"}
    readiness_ready = readiness.get("status") == "v2_contract_ready_for_source_freshness"
    source_ready = source_freshness.get("status") in {
        "source_freshness_clean_current",
        "source_freshness_tracked_artifact_lag_only_gate_ready",
    }
    packet_ready = remote_packet.get("status") == "ready_for_v2_remote_preflight"
    preflight_ready = chain.get("current_blocking_stage_id") not in {
        "v2_contract_promoted",
        "v2_contract_readiness_ready",
        "source_freshness_ready",
        "v2_remote_packet_ready",
        "v2_remote_preflight_ready",
    }
    remaining_summary = remaining.get("remaining_evidence_summary") if isinstance(remaining.get("remaining_evidence_summary"), dict) else {}
    training_ready = int(remaining_summary.get("training_missing_or_unsatisfied") or 0) == 0 and bool(remaining_summary)
    evaluation_ready = int(remaining_summary.get("evaluation_missing_or_unsatisfied") or 0) == 0 and bool(remaining_summary)
    acceptance_ready = int(remaining_summary.get("acceptance_missing_or_unsatisfied") or 0) == 0 and bool(remaining_summary)
    return [
        _target(
            "apply_v2_contract_promotion",
            "contract",
            "Apply Dr Sun's explicit approved/frozen promotion to the v2 contract.",
            satisfied_now=contract_promoted,
            allowed_now=False,
            blocked_by=[] if dry_run.get("status") == "promotion_apply_ready" else ["promotion_dry_run_not_ready"],
            command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.apply_module2_v2_contract_promotion --status approved --decider 'Dr Sun' --remote-alias gpu3070ti-relay --confirm-training-budget --confirm-unsafe-failure-thresholds",
            writes_files=True,
            requires_dr_sun=True,
        ),
        _target(
            "rerun_v2_contract_readiness_gate",
            "local_gate",
            "Regenerate v2 contract readiness after promotion.",
            satisfied_now=readiness_ready,
            allowed_now=contract_promoted,
            blocked_by=[] if contract_promoted else ["v2_contract_not_promoted"],
            command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_contract_readiness_gate",
        ),
        _target(
            "rerun_source_freshness_audit",
            "local_gate",
            "Regenerate source freshness before any remote preflight.",
            satisfied_now=source_ready,
            allowed_now=contract_promoted and readiness_ready,
            blocked_by=_blockers((contract_promoted, "v2_contract_not_promoted"), (readiness_ready, "v2_contract_readiness_not_ready")),
            command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit",
        ),
        _target(
            "regenerate_v2_remote_execution_packet",
            "local_gate",
            "Regenerate v2 remote command packet after source freshness is ready.",
            satisfied_now=packet_ready,
            allowed_now=contract_promoted and readiness_ready and source_ready,
            blocked_by=_blockers(
                (contract_promoted, "v2_contract_not_promoted"),
                (readiness_ready, "v2_contract_readiness_not_ready"),
                (source_ready, "source_freshness_not_ready"),
            ),
            command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_remote_execution_packet",
        ),
        _target(
            "rerun_v2_formal_gate_chain_audit",
            "local_gate",
            "Refresh the chain audit after each gate regeneration.",
            satisfied_now=chain.get("audit_issue_count") == 0,
            allowed_now=True,
            blocked_by=[],
            command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit",
        ),
        _target(
            "run_remote_preflight_only",
            "remote_preflight",
            "Run remote preflight only after the regenerated packet allows preflight.",
            satisfied_now=preflight_ready,
            allowed_now=contract_promoted and readiness_ready and source_ready and packet_ready,
            blocked_by=_blockers(
                (contract_promoted, "v2_contract_not_promoted"),
                (readiness_ready, "v2_contract_readiness_not_ready"),
                (source_ready, "source_freshness_not_ready"),
                (packet_ready, "v2_remote_packet_not_ready"),
            ),
            command=_remote_packet_command(remote_packet, "run_remote_preflight"),
            runs_remote_preflight=True,
        ),
        _target(
            "run_remote_training_after_preflight",
            "remote_training",
            "Run remote training only after the preflight manifest is ready.",
            satisfied_now=training_ready,
            allowed_now=False,
            blocked_by=[] if preflight_ready else ["v2_remote_preflight_not_ready"],
            command=_remote_packet_command(remote_packet, "run_remote_training"),
            runs_training=True,
        ),
        _target(
            "pullback_eval_audit_hash_artifacts",
            "acceptance",
            "Pull back eval/audit/hash evidence and refresh remaining-evidence ledger.",
            satisfied_now=training_ready and evaluation_ready and acceptance_ready,
            allowed_now=False,
            blocked_by=[] if training_ready else ["remote_training_not_completed"],
            command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence",
        ),
    ]


def _target(
    target_id: str,
    category: str,
    purpose: str,
    *,
    satisfied_now: bool,
    allowed_now: bool,
    blocked_by: Sequence[str],
    command: str,
    writes_files: bool = False,
    requires_dr_sun: bool = False,
    runs_remote_preflight: bool = False,
    runs_training: bool = False,
) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "category": category,
        "purpose": purpose,
        "satisfied_now": bool(satisfied_now),
        "allowed_now": bool(allowed_now),
        "blocked_by": list(blocked_by),
        "command": command,
        "executes_now": False,
        "writes_files": bool(writes_files),
        "requires_dr_sun": bool(requires_dr_sun),
        "runs_remote_preflight": bool(runs_remote_preflight),
        "runs_training": bool(runs_training),
    }


def _status(*, contract_status: str, chain: dict[str, Any], targets: Sequence[dict[str, Any]]) -> str:
    if contract_status not in {"approved", "frozen"}:
        return "blocked_until_v2_contract_promotion"
    if chain.get("audit_issue_count"):
        return "blocked_until_chain_audit_clean"
    first_open = next((target for target in targets if not target["satisfied_now"] and not target["requires_dr_sun"]), None)
    if first_open is None:
        return "v2_post_promotion_regeneration_plan_complete"
    return f"ready_for_{first_open['target_id']}" if first_open["allowed_now"] else f"blocked_before_{first_open['target_id']}"


def _next_action(targets: Sequence[dict[str, Any]]) -> str:
    for target in targets:
        if not target["satisfied_now"]:
            if target["requires_dr_sun"]:
                return f"await_dr_sun_before_{target['target_id']}"
            if target["allowed_now"]:
                return target["target_id"]
            return f"blocked_before_{target['target_id']}"
    return "no_open_regeneration_target"


def _remote_packet_command(remote_packet: dict[str, Any], step_id: str) -> str:
    command_plan = remote_packet.get("command_plan") if isinstance(remote_packet.get("command_plan"), dict) else {}
    step = command_plan.get(step_id) if isinstance(command_plan.get(step_id), dict) else {}
    return str(step.get("command") or "")


def _blockers(*checks: tuple[bool, str]) -> list[str]:
    return [name for ok, name in checks if not ok]


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
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Post-Promotion Regeneration Plan",
        "",
        "This artifact plans the local gate regeneration sequence after v2 contract promotion. It does not execute the commands, train, run remote preflight, or write paper results.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- contract_status: `{manifest['contract_status']}`",
        f"- next_action: `{manifest['next_action']}`",
        f"- remote_preflight_allowed_now: `{manifest['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        "",
        "## Ordered Targets",
        "",
    ]
    for target in manifest["ordered_targets"]:
        lines.append(f"### `{target['target_id']}`")
        lines.append(f"- category: `{target['category']}`")
        lines.append(f"- satisfied_now: `{target['satisfied_now']}`")
        lines.append(f"- allowed_now: `{target['allowed_now']}`")
        lines.append(f"- blocked_by: `{', '.join(target['blocked_by'])}`")
        lines.append(f"- runs_remote_preflight: `{target['runs_remote_preflight']}`")
        lines.append(f"- runs_training: `{target['runs_training']}`")
        lines.append("")
        lines.append("```bash")
        lines.append(target["command"])
        lines.append("```")
        lines.append("")
    lines.extend(["## Invalid Substitutes", ""])
    lines.extend(f"- {item}" for item in manifest["invalid_substitutes"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
