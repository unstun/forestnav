from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence import (
    DEFAULT_CONTRACT_PATH,
    DEFAULT_DECISION_RECORD,
    DEFAULT_H02_ACCEPTANCE,
    DEFAULT_PREFLIGHT_MANIFEST,
    DEFAULT_PROMOTION_DRY_RUN,
    DEFAULT_PROMOTION_PACKET,
    DEFAULT_READINESS_GATE,
    DEFAULT_REMOTE_PACKET,
    DEFAULT_SOURCE_FRESHNESS,
    EXPECTED_CONTRACT_ACTION,
    EXPECTED_LANE,
    READY_CONTRACT_STATUSES,
    READY_READINESS_STATUS,
    READY_REMOTE_PACKET_STATUS,
    SOURCE_FRESHNESS_READY_STATUSES,
)


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_formal_gate_chain_audit")
DEFAULT_REMAINING_EVIDENCE = Path(
    "0_trials/module2_v2_formal_gate_remaining_evidence/v2_formal_gate_remaining_evidence.json"
)
READY_PROMOTION_PACKET_STATUS = "v2_contract_promotion_packet_ready_awaiting_dr_sun"
READY_PROMOTION_DRY_RUN_STATUS = "promotion_apply_ready"


@dataclass(frozen=True)
class Module2V2FormalGateChainAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    promotion_packet_path: Path = DEFAULT_PROMOTION_PACKET
    promotion_dry_run_path: Path = DEFAULT_PROMOTION_DRY_RUN
    readiness_gate_path: Path = DEFAULT_READINESS_GATE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    preflight_manifest_path: Path = DEFAULT_PREFLIGHT_MANIFEST
    remaining_evidence_path: Path = DEFAULT_REMAINING_EVIDENCE
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2FormalGateChainAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        decision_record_path=args.decision_record,
        promotion_packet_path=args.promotion_packet,
        promotion_dry_run_path=args.promotion_dry_run,
        readiness_gate_path=args.readiness_gate,
        source_freshness_path=args.source_freshness,
        remote_packet_path=args.remote_packet,
        preflight_manifest_path=args.preflight_manifest,
        remaining_evidence_path=args.remaining_evidence,
        h02_acceptance_path=args.h02_acceptance,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_formal_gate_chain_audit.json"
    markdown_out = config.markdown_out or output_dir / "v2_formal_gate_chain_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: Module2V2FormalGateChainAuditConfig) -> dict[str, Any]:
    contract_frontmatter = _frontmatter(_read_text(config.contract_path))
    decision = _read_json(config.decision_record_path)
    promotion = _read_json(config.promotion_packet_path)
    dry_run = _read_json(config.promotion_dry_run_path)
    readiness = _read_json(config.readiness_gate_path)
    source_freshness = _read_json(config.source_freshness_path)
    remote_packet = _read_json(config.remote_packet_path)
    preflight = _read_json(config.preflight_manifest_path)
    remaining = _read_json(config.remaining_evidence_path)
    h02 = _read_json(config.h02_acceptance_path)

    stages = _stages(
        contract_frontmatter=contract_frontmatter,
        decision=decision,
        promotion=promotion,
        dry_run=dry_run,
        readiness=readiness,
        source_freshness=source_freshness,
        remote_packet=remote_packet,
        preflight=preflight,
        remaining=remaining,
        h02=h02,
    )
    blocking_stage = _first_unsatisfied_strict_stage(stages)
    audit_issues = _audit_issues(stages=stages, readiness=readiness, remote_packet=remote_packet, remaining=remaining, h02=h02)
    status = _status(blocking_stage=blocking_stage, audit_issues=audit_issues)
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_formal_gate_chain_audit",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": _remote_preflight_allowed_now(stages=stages, remote_packet=remote_packet),
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "inputs": {
            "contract": str(config.contract_path),
            "decision_record": str(config.decision_record_path),
            "promotion_packet": str(config.promotion_packet_path),
            "promotion_dry_run": str(config.promotion_dry_run_path),
            "readiness_gate": str(config.readiness_gate_path),
            "source_freshness": str(config.source_freshness_path),
            "remote_packet": str(config.remote_packet_path),
            "preflight_manifest": str(config.preflight_manifest_path),
            "remaining_evidence": str(config.remaining_evidence_path),
            "h02_acceptance": str(config.h02_acceptance_path),
        },
        "current_blocking_stage_id": None if blocking_stage is None else blocking_stage["stage_id"],
        "current_blocking_stage_label": None if blocking_stage is None else blocking_stage["label"],
        "next_allowed_action": _next_allowed_action(blocking_stage),
        "strict_stage_order": [stage["stage_id"] for stage in stages if stage["strict_order_index"] is not None],
        "stage_count": len(stages),
        "satisfied_stage_count": sum(1 for stage in stages if stage["satisfied"]),
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "stages": stages,
        "invalid_substitutes": [
            "draft contract",
            "promotion dry-run treated as approval",
            "old v1 remote packet",
            "remote smoke without formal preflight ready",
            "failed warm-start PPO checkpoint",
            "local PPO output",
            "paper prose or table before H02 acceptance",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the ordered Module2 v2 formal gate chain without running remote commands.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--promotion-packet", type=Path, default=DEFAULT_PROMOTION_PACKET)
    parser.add_argument("--promotion-dry-run", type=Path, default=DEFAULT_PROMOTION_DRY_RUN)
    parser.add_argument("--readiness-gate", type=Path, default=DEFAULT_READINESS_GATE)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--preflight-manifest", type=Path, default=DEFAULT_PREFLIGHT_MANIFEST)
    parser.add_argument("--remaining-evidence", type=Path, default=DEFAULT_REMAINING_EVIDENCE)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _stages(
    *,
    contract_frontmatter: dict[str, str],
    decision: dict[str, Any],
    promotion: dict[str, Any],
    dry_run: dict[str, Any],
    readiness: dict[str, Any],
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    preflight: dict[str, Any],
    remaining: dict[str, Any],
    h02: dict[str, Any],
) -> list[dict[str, Any]]:
    remaining_summary = remaining.get("remaining_evidence_summary") if isinstance(remaining.get("remaining_evidence_summary"), dict) else {}
    return [
        _stage(
            "protocol_lane_decision_recorded",
            "Protocol lane decision recorded",
            decision.get("status") == "protocol_lane_decision_recorded"
            and decision.get("selected_lane_id") == EXPECTED_LANE
            and decision.get("contract_action") == EXPECTED_CONTRACT_ACTION,
            observed={"status": decision.get("status"), "selected_lane_id": decision.get("selected_lane_id"), "contract_action": decision.get("contract_action")},
            expected={"selected_lane_id": EXPECTED_LANE, "contract_action": EXPECTED_CONTRACT_ACTION},
            strict_order_index=None,
        ),
        _stage(
            "promotion_packet_ready",
            "Promotion packet ready for Dr Sun",
            promotion.get("status") == READY_PROMOTION_PACKET_STATUS,
            observed=promotion.get("status"),
            expected=READY_PROMOTION_PACKET_STATUS,
            strict_order_index=None,
        ),
        _stage(
            "promotion_dry_run_ready",
            "Promotion apply dry-run ready",
            dry_run.get("status") == READY_PROMOTION_DRY_RUN_STATUS,
            observed=dry_run.get("status"),
            expected=READY_PROMOTION_DRY_RUN_STATUS,
            strict_order_index=None,
        ),
        _stage(
            "v2_contract_promoted",
            "V2 contract approved or frozen",
            contract_frontmatter.get("status") in READY_CONTRACT_STATUSES,
            observed=contract_frontmatter.get("status", "missing"),
            expected=sorted(READY_CONTRACT_STATUSES),
            strict_order_index=0,
        ),
        _stage(
            "v2_contract_readiness_ready",
            "V2 contract readiness gate ready",
            readiness.get("status") == READY_READINESS_STATUS,
            observed=readiness.get("status"),
            expected=READY_READINESS_STATUS,
            strict_order_index=1,
        ),
        _stage(
            "source_freshness_ready",
            "Source freshness ready for remote preflight",
            source_freshness.get("status") in SOURCE_FRESHNESS_READY_STATUSES,
            observed=source_freshness.get("status"),
            expected=sorted(SOURCE_FRESHNESS_READY_STATUSES),
            strict_order_index=2,
        ),
        _stage(
            "v2_remote_packet_ready",
            "V2 remote execution packet ready for preflight",
            remote_packet.get("status") == READY_REMOTE_PACKET_STATUS and remote_packet.get("remote_preflight_allowed_now") is True,
            observed={"status": remote_packet.get("status"), "remote_preflight_allowed_now": remote_packet.get("remote_preflight_allowed_now")},
            expected={"status": READY_REMOTE_PACKET_STATUS, "remote_preflight_allowed_now": True},
            strict_order_index=3,
        ),
        _stage(
            "v2_remote_preflight_ready",
            "V2 remote preflight manifest ready",
            preflight.get("preflight_status") == "ready" and preflight.get("formal_trial_ready") is True,
            observed={"preflight_status": preflight.get("preflight_status", "missing"), "formal_trial_ready": preflight.get("formal_trial_ready")},
            expected={"preflight_status": "ready", "formal_trial_ready": True},
            strict_order_index=4,
        ),
        _stage(
            "v2_training_artifacts_ready",
            "Fresh v2 training artifacts pulled back",
            int(remaining_summary.get("training_missing_or_unsatisfied") or 0) == 0 and bool(remaining_summary),
            observed=remaining_summary.get("training_missing_or_unsatisfied"),
            expected=0,
            strict_order_index=5,
        ),
        _stage(
            "v2_evaluation_artifacts_ready",
            "Fresh v2 evaluation artifacts pulled back",
            int(remaining_summary.get("evaluation_missing_or_unsatisfied") or 0) == 0 and bool(remaining_summary),
            observed=remaining_summary.get("evaluation_missing_or_unsatisfied"),
            expected=0,
            strict_order_index=6,
        ),
        _stage(
            "v2_acceptance_artifacts_ready",
            "Fresh v2 Gate3 audit and hash acceptance ready",
            int(remaining_summary.get("acceptance_missing_or_unsatisfied") or 0) == 0 and bool(remaining_summary),
            observed=remaining_summary.get("acceptance_missing_or_unsatisfied"),
            expected=0,
            strict_order_index=7,
        ),
        _stage(
            "h02_formal_acceptance_ready",
            "H02 formal output acceptance ready",
            h02.get("formal_output_accepted") is True and h02.get("paper_result_input_allowed") is True,
            observed={"status": h02.get("status"), "formal_output_accepted": h02.get("formal_output_accepted"), "paper_result_input_allowed": h02.get("paper_result_input_allowed")},
            expected={"formal_output_accepted": True, "paper_result_input_allowed": True},
            strict_order_index=8,
        ),
    ]


def _stage(
    stage_id: str,
    label: str,
    satisfied: bool,
    *,
    observed: Any,
    expected: Any,
    strict_order_index: int | None,
) -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "label": label,
        "satisfied": bool(satisfied),
        "observed": observed,
        "expected": expected,
        "strict_order_index": strict_order_index,
    }


def _first_unsatisfied_strict_stage(stages: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    strict = sorted((stage for stage in stages if stage["strict_order_index"] is not None), key=lambda stage: int(stage["strict_order_index"]))
    return next((stage for stage in strict if not stage["satisfied"]), None)


def _audit_issues(
    *,
    stages: Sequence[dict[str, Any]],
    readiness: dict[str, Any],
    remote_packet: dict[str, Any],
    remaining: dict[str, Any],
    h02: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    strict = sorted((stage for stage in stages if stage["strict_order_index"] is not None), key=lambda stage: int(stage["strict_order_index"]))
    first_unsatisfied_index = next((int(stage["strict_order_index"]) for stage in strict if not stage["satisfied"]), None)
    if first_unsatisfied_index is not None:
        for stage in strict:
            if int(stage["strict_order_index"]) > first_unsatisfied_index and stage["satisfied"]:
                issues.append(
                    {
                        "issue_id": "downstream_stage_satisfied_before_upstream_gate",
                        "stage_id": stage["stage_id"],
                        "first_unsatisfied_stage_id": strict[first_unsatisfied_index]["stage_id"],
                    }
                )
    for source_name, source in (
        ("readiness_gate", readiness),
        ("remote_packet", remote_packet),
        ("remaining_evidence", remaining),
    ):
        if source.get("remote_training_allowed_now") is True:
            issues.append({"issue_id": "remote_training_allowed_before_chain_complete", "source": source_name})
        if source.get("local_training_allowed_now") is True or source.get("local_training_allowed") is True:
            issues.append({"issue_id": "local_training_allowed_in_formal_gate", "source": source_name})
        if source.get("paper_result_material_allowed_now") is True or source.get("paper_result_material_allowed") is True:
            issues.append({"issue_id": "paper_result_material_allowed_before_h02", "source": source_name})
    if h02.get("paper_result_input_allowed") is True and not (h02.get("formal_output_accepted") is True):
        issues.append({"issue_id": "h02_paper_input_allowed_without_formal_acceptance"})
    return issues


def _status(*, blocking_stage: dict[str, Any] | None, audit_issues: Sequence[dict[str, Any]]) -> str:
    if audit_issues:
        return "v2_formal_gate_chain_inconsistent"
    if blocking_stage is None:
        return "v2_formal_gate_chain_complete"
    if blocking_stage["stage_id"] == "v2_contract_promoted":
        return "blocked_until_v2_contract_promotion"
    if blocking_stage["stage_id"] == "source_freshness_ready":
        return "blocked_until_source_freshness"
    if blocking_stage["stage_id"] == "v2_remote_preflight_ready":
        return "blocked_until_v2_remote_preflight"
    return f"blocked_at_{blocking_stage['stage_id']}"


def _remote_preflight_allowed_now(*, stages: Sequence[dict[str, Any]], remote_packet: dict[str, Any]) -> bool:
    required = {"v2_contract_promoted", "v2_contract_readiness_ready", "source_freshness_ready", "v2_remote_packet_ready"}
    satisfied = {stage["stage_id"] for stage in stages if stage["satisfied"]}
    return required.issubset(satisfied) and remote_packet.get("remote_preflight_allowed_now") is True


def _next_allowed_action(blocking_stage: dict[str, Any] | None) -> str:
    if blocking_stage is None:
        return "regenerate_h02_and_claim_gates_only_after_evidence_review"
    return {
        "v2_contract_promoted": "await_dr_sun_explicit_contract_promotion_then_apply_promotion",
        "v2_contract_readiness_ready": "rerun_v2_contract_readiness_gate",
        "source_freshness_ready": "rerun_source_freshness_for_v2_contract",
        "v2_remote_packet_ready": "regenerate_v2_remote_execution_packet",
        "v2_remote_preflight_ready": "run_remote_preflight_only",
        "v2_training_artifacts_ready": "run_remote_training_after_ready_preflight",
        "v2_evaluation_artifacts_ready": "pull_back_and_audit_gate3_evaluation",
        "v2_acceptance_artifacts_ready": "complete_gate3_audit_and_checkpoint_hash_pullback",
        "h02_formal_acceptance_ready": "regenerate_h02_formal_acceptance",
    }.get(str(blocking_stage["stage_id"]), "inspect_blocking_stage")


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    out: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip("'\"")
    return out


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Formal Gate Chain Audit",
        "",
        "This artifact audits the ordered formal-gate chain only. It does not run local training, remote preflight, remote training, audit, pullback, H02 acceptance, or paper-result writing.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- current_blocking_stage_id: `{manifest['current_blocking_stage_id']}`",
        f"- next_allowed_action: `{manifest['next_allowed_action']}`",
        f"- remote_preflight_allowed_now: `{manifest['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        "",
        "## Stages",
        "",
    ]
    for stage in manifest["stages"]:
        lines.append(f"- `{stage['stage_id']}`: satisfied=`{stage['satisfied']}`, observed=`{stage['observed']}`, expected=`{stage['expected']}`")
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue}" for issue in manifest["audit_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Invalid Substitutes", ""])
    lines.extend(f"- {item}" for item in manifest["invalid_substitutes"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
