from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_protocol_lane_readiness")
DEFAULT_PROTOCOL_STATUS = Path(
    "0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json"
)
DEFAULT_DECISION_PACKET = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_packet/formal_gate_protocol_lane_decision_packet.json"
)
DEFAULT_DECISION_RECORD = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json"
)
DEFAULT_LANE_MATRIX = Path("0_trials/module2_formal_gate_protocol_lane_matrix/formal_gate_protocol_lane_matrix.json")
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_REMOTE_PACKET_SAFETY = Path(
    "0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json"
)
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_PROOF_SUMMARY_CHAIN = Path(
    "0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json"
)
DEFAULT_MAINLINE_AUDIT = Path(
    "0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json"
)
EXPECTED_LANE_IDS = (
    "stronger_obstacle_summary_warm_start",
    "full_patch_cnn_policy",
    "hybrid_ppo_analytic_fallback",
    "stop_or_reframe_module2_claim",
)
EXPECTED_BLOCKED_ACTIONS = {
    "local_training",
    "remote_success_training",
    "remote_preflight_for_new_success_attempt",
    "formal_claim",
    "paper_result_material",
}


@dataclass(frozen=True)
class FormalGateProtocolLaneReadinessConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    protocol_status_path: Path = DEFAULT_PROTOCOL_STATUS
    decision_packet_path: Path = DEFAULT_DECISION_PACKET
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    lane_matrix_path: Path = DEFAULT_LANE_MATRIX
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    remote_packet_safety_path: Path = DEFAULT_REMOTE_PACKET_SAFETY
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    proof_summary_chain_path: Path = DEFAULT_PROOF_SUMMARY_CHAIN
    mainline_audit_path: Path = DEFAULT_MAINLINE_AUDIT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProtocolLaneReadinessConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        protocol_status_path=args.protocol_status,
        decision_packet_path=args.decision_packet,
        decision_record_path=args.decision_record,
        lane_matrix_path=args.lane_matrix,
        next_round_requirements_path=args.next_round_requirements,
        remaining_deliverables_path=args.remaining_deliverables,
        remote_packet_safety_path=args.remote_packet_safety,
        claim_safety_path=args.claim_safety,
        paper_readiness_path=args.paper_readiness,
        proof_summary_chain_path=args.proof_summary_chain,
        mainline_audit_path=args.mainline_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "protocol_lane_readiness.json"
    markdown_out = config.markdown_out or output_dir / "protocol_lane_readiness.md"
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


def build_manifest(config: FormalGateProtocolLaneReadinessConfig) -> dict[str, Any]:
    protocol_status = _read_json(config.protocol_status_path)
    decision_packet = _read_json(config.decision_packet_path)
    decision_record = _read_json(config.decision_record_path)
    lane_matrix = _read_json(config.lane_matrix_path)
    next_round = _read_json(config.next_round_requirements_path)
    remaining = _read_json(config.remaining_deliverables_path)
    remote_safety = _read_json(config.remote_packet_safety_path)
    claim_safety = _read_json(config.claim_safety_path)
    paper_readiness = _read_json(config.paper_readiness_path)
    proof_chain = _read_json(config.proof_summary_chain_path)
    mainline_audit = _read_json(config.mainline_audit_path)

    gate = _gate_state(
        protocol_status=protocol_status,
        decision_packet=decision_packet,
        decision_record=decision_record,
        next_round=next_round,
        remaining=remaining,
        remote_safety=remote_safety,
        claim_safety=claim_safety,
        paper_readiness=paper_readiness,
        proof_chain=proof_chain,
        mainline_audit=mainline_audit,
    )
    lane_rows = _lane_rows(
        lane_matrix=lane_matrix,
        decision_packet=decision_packet,
        next_round=next_round,
    )
    shared_artifacts = _next_success_attempt_artifacts(next_round)
    issues = _audit_issues(gate=gate, lane_rows=lane_rows, shared_artifacts=shared_artifacts)
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_protocol_lane_readiness",
        "status": _status(issues=issues, gate=gate),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "inputs": {
            "protocol_status": str(config.protocol_status_path),
            "decision_packet": str(config.decision_packet_path),
            "decision_record": str(config.decision_record_path),
            "lane_matrix": str(config.lane_matrix_path),
            "next_round_requirements": str(config.next_round_requirements_path),
            "remaining_deliverables": str(config.remaining_deliverables_path),
            "remote_packet_safety": str(config.remote_packet_safety_path),
            "claim_safety": str(config.claim_safety_path),
            "paper_readiness": str(config.paper_readiness_path),
            "proof_summary_chain": str(config.proof_summary_chain_path),
            "mainline_audit": str(config.mainline_audit_path),
        },
        "gate_state": gate,
        "lane_count": len(lane_rows),
        "lane_readiness_rows": lane_rows,
        "shared_next_success_attempt_artifact_count": len(shared_artifacts),
        "shared_next_success_attempt_artifacts": shared_artifacts,
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This readiness packet is not a protocol-lane decision record.",
            "It does not authorize local training, remote preflight, remote training, formal claims, or paper result material.",
            "Every non-stop success lane still requires a new or revised approved/frozen Research Contract before remote training.",
            "The failed Gate3 run is negative evidence only: terminal-RS success 0.53125 remains below the 0.8 threshold.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 protocol-lane readiness packet.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--protocol-status", type=Path, default=DEFAULT_PROTOCOL_STATUS)
    parser.add_argument("--decision-packet", type=Path, default=DEFAULT_DECISION_PACKET)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--lane-matrix", type=Path, default=DEFAULT_LANE_MATRIX)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--remote-packet-safety", type=Path, default=DEFAULT_REMOTE_PACKET_SAFETY)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--proof-summary-chain", type=Path, default=DEFAULT_PROOF_SUMMARY_CHAIN)
    parser.add_argument("--mainline-audit", type=Path, default=DEFAULT_MAINLINE_AUDIT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _gate_state(
    *,
    protocol_status: dict[str, Any],
    decision_packet: dict[str, Any],
    decision_record: dict[str, Any],
    next_round: dict[str, Any],
    remaining: dict[str, Any],
    remote_safety: dict[str, Any],
    claim_safety: dict[str, Any],
    paper_readiness: dict[str, Any],
    proof_chain: dict[str, Any],
    mainline_audit: dict[str, Any],
) -> dict[str, Any]:
    current = protocol_status.get("current_status") if isinstance(protocol_status.get("current_status"), dict) else {}
    failed = next_round.get("current_failed_run") if isinstance(next_round.get("current_failed_run"), dict) else {}
    permissions = next_round.get("permissions_now") if isinstance(next_round.get("permissions_now"), dict) else {}
    auth = decision_record.get("current_authorization") if isinstance(decision_record.get("current_authorization"), dict) else {}
    gap = remaining.get("gap_summary") if isinstance(remaining.get("gap_summary"), dict) else {}
    next_action_ids = _strings(auth.get("current_allowed_action_ids")) or _strings(current.get("allowed_next_action_ids"))
    blocked_actions = _strings(auth.get("current_blocked_action_ids")) or _strings(current.get("blocked_action_ids"))
    return {
        "next_blocked_lane": current.get("next_blocked_lane"),
        "decision_required": decision_packet.get("decision_required") is True,
        "decision_owner_required": decision_record.get("decision_owner_required"),
        "decision_packet_status": decision_packet.get("status"),
        "decision_record_status": decision_record.get("status"),
        "selected_lane_id": decision_record.get("selected_lane_id"),
        "next_action_ids": next_action_ids,
        "blocked_action_ids": blocked_actions,
        "contract_action": decision_record.get("contract_action"),
        "contract_drafting_allowed_now": current.get("contract_drafting_allowed_now") is True,
        "new_or_revised_contract_required_before_training": permissions.get(
            "new_or_revised_contract_required_before_new_success_training"
        )
        is True,
        "current_formal_decision": failed.get("formal_decision"),
        "current_failure_mode": failed.get("failure_mode"),
        "terminal_rs_success_rate": failed.get("terminal_rs_success_rate"),
        "required_success_threshold": failed.get("required_success_threshold"),
        "threshold_deficit": failed.get("threshold_deficit"),
        "remote_packet_safety_status": remote_safety.get("status"),
        "claim_safety_status": claim_safety.get("status"),
        "paper_readiness_status": paper_readiness.get("status"),
        "proof_summary_chain_status": proof_chain.get("status"),
        "mainline_audit_status": mainline_audit.get("status"),
        "remaining_deliverables_status": remaining.get("status"),
        "remaining_gap_total_missing": int(gap.get("total_missing_deliverables") or 0),
        "local_training_allowed_now": _truthy_any(
            protocol_status.get("local_training_allowed"),
            current.get("local_training_allowed_now"),
            permissions.get("local_training_allowed_now"),
            decision_record.get("local_training_allowed_now"),
        ),
        "remote_training_allowed_now": _truthy_any(
            protocol_status.get("remote_training_allowed_now"),
            current.get("remote_training_allowed_now"),
            permissions.get("remote_training_allowed_now_for_existing_packet"),
            decision_record.get("remote_training_allowed_now"),
        ),
        "formal_claim_allowed_now": _truthy_any(
            protocol_status.get("formal_claim_allowed"),
            current.get("formal_claim_allowed_now"),
            permissions.get("formal_claim_allowed_now"),
            decision_record.get("formal_claim_allowed_now"),
        ),
        "paper_result_material_allowed_now": _truthy_any(
            protocol_status.get("paper_result_material_allowed"),
            current.get("paper_result_material_allowed_now"),
            decision_record.get("paper_result_material_allowed_now"),
        ),
        "new_success_training_allowed_now": _truthy_any(
            current.get("new_success_training_allowed_now"),
            permissions.get("new_success_training_allowed_now"),
        ),
        "agent_may_record_decision_now": False,
        "remote_training_authorized_by_this_packet": False,
    }


def _lane_rows(
    *,
    lane_matrix: dict[str, Any],
    decision_packet: dict[str, Any],
    next_round: dict[str, Any],
) -> list[dict[str, Any]]:
    matrix_rows = {
        str(row.get("lane_id")): row
        for row in lane_matrix.get("protocol_lane_evidence_matrix", [])
        if isinstance(row, dict) and row.get("lane_id")
    }
    packet_rows = {
        str(row.get("lane_id")): row
        for row in decision_packet.get("lane_options", [])
        if isinstance(row, dict) and row.get("lane_id")
    }
    artifact_ids = [row["artifact_id"] for row in _next_success_attempt_artifacts(next_round)]
    rows: list[dict[str, Any]] = []
    for lane_id in EXPECTED_LANE_IDS:
        matrix = matrix_rows.get(lane_id, {})
        packet = packet_rows.get(lane_id, {})
        stop_lane = lane_id == "stop_or_reframe_module2_claim"
        rows.append(
            {
                "lane_id": lane_id,
                "present_in_matrix": bool(matrix),
                "present_in_decision_packet": bool(packet),
                "status": matrix.get("status") or packet.get("status"),
                "claim_scope": matrix.get("claim_scope") or packet.get("claim_scope"),
                "what_changes": matrix.get("what_changes"),
                "new_success_training_required_if_selected": not stop_lane,
                "can_start_remote_training_now": False,
                "agent_may_select_lane_now": False,
                "requires_dr_sun_decision": True,
                "requires_new_or_revised_contract": matrix.get("requires_new_or_revised_contract") is True
                or packet.get("requires_new_or_revised_contract") is True,
                "next_action_after_selection": (
                    "draft_stop_or_reframe_contract"
                    if stop_lane
                    else "draft_new_or_revised_contract_then_remote_training_packet"
                ),
                "blocked_until": [
                    "record_protocol_lane_decision",
                    "approved_or_frozen_new_or_revised_contract",
                ]
                if not stop_lane
                else [
                    "record_protocol_lane_decision",
                    "approved_or_frozen_negative_or_reframe_contract",
                ],
                "required_decision_justification": _strings(packet.get("required_decision_justification")),
                "must_justify": _strings(matrix.get("must_justify")),
                "required_contract_deltas": _strings(matrix.get("required_contract_deltas")),
                "required_training_evidence": _strings(matrix.get("required_training_evidence")),
                "required_evaluation_evidence": _strings(matrix.get("required_evaluation_evidence")),
                "required_acceptance_evidence": _strings(matrix.get("required_acceptance_evidence")),
                "invalid_substitutes": _strings(matrix.get("invalid_substitutes")),
                "shared_next_success_artifact_ids": [] if stop_lane else artifact_ids,
            }
        )
    return rows


def _next_success_attempt_artifacts(next_round: dict[str, Any]) -> list[dict[str, Any]]:
    index = (
        next_round.get("next_success_attempt_artifact_index")
        if isinstance(next_round.get("next_success_attempt_artifact_index"), dict)
        else {}
    )
    rows = index.get("rows") if isinstance(index.get("rows"), list) else []
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or not row.get("artifact_id"):
            continue
        out.append(
            {
                "category": row.get("category"),
                "artifact_id": row.get("artifact_id"),
                "status": row.get("status"),
                "expected_path": row.get("expected_path"),
                "required_before": row.get("required_before"),
                "blocked_until": row.get("blocked_until"),
                "proof_requirement": row.get("proof_requirement"),
                "invalid_substitutes": _strings(row.get("invalid_substitutes")),
            }
        )
    return out


def _status(*, issues: list[dict[str, Any]], gate: dict[str, Any]) -> str:
    if issues:
        return "protocol_lane_readiness_audit_failed"
    if gate["next_blocked_lane"] == "protocol_lane_decision":
        return "protocol_lane_readiness_ready_for_dr_sun_decision"
    if gate["contract_drafting_allowed_now"]:
        return "protocol_lane_readiness_ready_for_contract_draft"
    return "protocol_lane_readiness_blocked_unknown"


def _audit_issues(
    *,
    gate: dict[str, Any],
    lane_rows: Sequence[dict[str, Any]],
    shared_artifacts: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if gate["decision_packet_status"] != "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun":
        issues.append(_issue("decision_packet_not_ready", "Protocol-lane decision packet must be ready."))
    if gate["decision_record_status"] not in {"pending_protocol_lane_decision", "protocol_lane_decision_recorded"}:
        issues.append(_issue("decision_record_status_invalid", "Decision record must be pending or recorded."))
    if gate["next_blocked_lane"] == "protocol_lane_decision":
        if gate["selected_lane_id"] is not None:
            issues.append(_issue("pending_gate_has_selected_lane", "Pending protocol-lane gate must not select a lane."))
        if gate["next_action_ids"] != ["record_protocol_lane_decision"]:
            issues.append(
                _issue(
                    "pending_gate_next_action_not_protocol_lane_record",
                    "Pending gate must expose only record_protocol_lane_decision.",
                    observed=gate["next_action_ids"],
                )
            )
    if gate["decision_owner_required"] != "Dr Sun":
        issues.append(_issue("decision_owner_not_dr_sun", "Protocol-lane decision owner must be Dr Sun."))
    if not EXPECTED_BLOCKED_ACTIONS.issubset(set(gate["blocked_action_ids"])):
        issues.append(_issue("blocked_actions_incomplete", "Training, claim, and paper-result actions must stay blocked."))
    for key in (
        "local_training_allowed_now",
        "remote_training_allowed_now",
        "formal_claim_allowed_now",
        "paper_result_material_allowed_now",
        "new_success_training_allowed_now",
        "agent_may_record_decision_now",
        "remote_training_authorized_by_this_packet",
    ):
        if gate[key] is True:
            issues.append(_issue(f"{key}_unexpectedly_true", f"{key} must remain false."))
    expected_statuses = {
        "remote_packet_safety_status": "remote_packet_safety_audit_passed",
        "claim_safety_status": "blocked_formal_performance_claims",
        "paper_readiness_status": "partial_methods_ready_results_blocked",
        "proof_summary_chain_status": "formal_gate_proof_summary_chain_consistent_blocked",
        "mainline_audit_status": "mainline_formal_gate_state_consistent_blocked",
    }
    for key, expected in expected_statuses.items():
        if gate[key] != expected:
            issues.append(_issue(f"{key}_unexpected", f"{key} must be {expected}.", observed=gate[key]))
    if len(lane_rows) != len(EXPECTED_LANE_IDS):
        issues.append(_issue("lane_count_invalid", "Readiness packet must cover all four protocol lanes."))
    for row in lane_rows:
        lane_id = row["lane_id"]
        if row["present_in_matrix"] is not True:
            issues.append(_issue(f"{lane_id}_missing_from_matrix", "Lane is missing from protocol-lane matrix."))
        if row["present_in_decision_packet"] is not True:
            issues.append(_issue(f"{lane_id}_missing_from_decision_packet", "Lane is missing from decision packet."))
        if row["agent_may_select_lane_now"] is not False or row["can_start_remote_training_now"] is not False:
            issues.append(_issue(f"{lane_id}_authorization_leak", "Readiness rows must not authorize selection or training."))
        if not row["claim_scope"]:
            issues.append(_issue(f"{lane_id}_missing_claim_scope", "Lane must preserve claim-scope text."))
        if not row["required_decision_justification"]:
            issues.append(_issue(f"{lane_id}_missing_decision_justification", "Lane must list decision justification fields."))
        if not row["required_contract_deltas"]:
            issues.append(_issue(f"{lane_id}_missing_contract_deltas", "Lane must list contract deltas."))
        if not row["invalid_substitutes"]:
            issues.append(_issue(f"{lane_id}_missing_invalid_substitutes", "Lane must list invalid substitutes."))
        if lane_id != "stop_or_reframe_module2_claim" and not row["shared_next_success_artifact_ids"]:
            issues.append(_issue(f"{lane_id}_missing_next_success_artifacts", "Success lanes must carry the next-attempt artifact index."))
    if len(shared_artifacts) < 10:
        issues.append(_issue("shared_artifact_index_incomplete", "Next success-attempt artifact index must contain at least 10 artifacts."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    gate = manifest["gate_state"]
    lines = [
        "# Module2 Protocol Lane Readiness Packet",
        "",
        "This packet is a read-only decision-preparation artifact. It is not paper result material.",
        "",
        "## Current Gate",
        "",
        f"- status: `{manifest['status']}`",
        f"- next_blocked_lane: `{gate['next_blocked_lane']}`",
        f"- decision_owner_required: `{gate['decision_owner_required']}`",
        f"- selected_lane_id: `{gate['selected_lane_id']}`",
        f"- next_action_ids: `{', '.join(gate['next_action_ids'])}`",
        f"- remote_training_allowed_now: `{gate['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{gate['formal_claim_allowed_now']}`",
        f"- paper_result_material_allowed_now: `{gate['paper_result_material_allowed_now']}`",
        "",
        "## Failed Gate3 Basis",
        "",
        f"- formal_decision: `{gate['current_formal_decision']}`",
        f"- failure_mode: `{gate['current_failure_mode']}`",
        f"- terminal_rs_success_rate: `{gate['terminal_rs_success_rate']}`",
        f"- required_success_threshold: `{gate['required_success_threshold']}`",
        f"- threshold_deficit: `{gate['threshold_deficit']}`",
        "",
        "## Lane Readiness",
        "",
        "| lane_id | claim_scope | next_action_after_selection | remote_training_now |",
        "|---|---|---|---|",
    ]
    for row in manifest["lane_readiness_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['lane_id']}`",
                    str(row["claim_scope"]),
                    f"`{row['next_action_after_selection']}`",
                    f"`{row['can_start_remote_training_now']}`",
                ]
            )
            + " |"
        )
    lines.extend(["", "## Lane Evidence Details"])
    for row in manifest["lane_readiness_rows"]:
        lines.extend(
            [
                "",
                f"### {row['lane_id']}",
                "",
                f"- new_success_training_required_if_selected: `{row['new_success_training_required_if_selected']}`",
                f"- blocked_until: `{', '.join(row['blocked_until'])}`",
                "- required_decision_justification:",
            ]
        )
        lines.extend(f"  - {item}" for item in row["required_decision_justification"])
        lines.append("- required_contract_deltas:")
        lines.extend(f"  - {item}" for item in row["required_contract_deltas"])
        lines.append("- required_training_evidence:")
        lines.extend(f"  - {item}" for item in row["required_training_evidence"])
        lines.append("- required_evaluation_evidence:")
        lines.extend(f"  - {item}" for item in row["required_evaluation_evidence"])
        lines.append("- required_acceptance_evidence:")
        lines.extend(f"  - {item}" for item in row["required_acceptance_evidence"])
        lines.append("- invalid_substitutes:")
        lines.extend(f"  - {item}" for item in row["invalid_substitutes"])
    lines.extend(["", "## Shared Next Success Attempt Artifact Index", ""])
    for artifact in manifest["shared_next_success_attempt_artifacts"]:
        lines.append(
            f"- `{artifact['artifact_id']}` ({artifact['category']}): "
            f"status=`{artifact['status']}`, blocked_until=`{artifact['blocked_until']}`"
        )
    lines.extend(["", "## Claim Boundaries"])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    lines.extend(["", "## Audit", "", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- no audit issues")
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _strings(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item) for item in value if item]


def _truthy_any(*values: Any) -> bool:
    return any(value is True for value in values)


def _issue(issue_id: str, message: str, *, observed: Any = None) -> dict[str, Any]:
    issue: dict[str, Any] = {"issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
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


if __name__ == "__main__":
    raise SystemExit(main())
