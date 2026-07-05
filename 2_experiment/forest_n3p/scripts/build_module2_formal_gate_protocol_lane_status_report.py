from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_protocol_lane_status_report")
DEFAULT_DECISION_PACKET = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_packet/formal_gate_protocol_lane_decision_packet.json"
)
DEFAULT_DECISION_RECORD = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json"
)
DEFAULT_DECISION_GATE_AUDIT = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_gate_audit/protocol_lane_decision_gate_audit.json"
)
DEFAULT_CONTRACT_AUTHORING_GATE_AUDIT = Path(
    "0_trials/module2_formal_gate_contract_authoring_gate_audit/contract_authoring_gate_audit.json"
)
DEFAULT_LANE_MATRIX = Path("0_trials/module2_formal_gate_protocol_lane_matrix/formal_gate_protocol_lane_matrix.json")
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)


@dataclass(frozen=True)
class FormalGateProtocolLaneStatusReportConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_packet_path: Path = DEFAULT_DECISION_PACKET
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    decision_gate_audit_path: Path = DEFAULT_DECISION_GATE_AUDIT
    contract_authoring_gate_audit_path: Path = DEFAULT_CONTRACT_AUTHORING_GATE_AUDIT
    lane_matrix_path: Path = DEFAULT_LANE_MATRIX
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProtocolLaneStatusReportConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_packet_path=args.decision_packet,
        decision_record_path=args.decision_record,
        decision_gate_audit_path=args.decision_gate_audit,
        contract_authoring_gate_audit_path=args.contract_authoring_gate_audit,
        lane_matrix_path=args.lane_matrix,
        next_round_requirements_path=args.next_round_requirements,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "protocol_lane_status_report.json"
    markdown_out = config.markdown_out or output_dir / "protocol_lane_status_report.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateProtocolLaneStatusReportConfig) -> dict[str, Any]:
    decision_packet = _read_json(config.decision_packet_path)
    decision_record = _read_json(config.decision_record_path)
    decision_gate = _read_json(config.decision_gate_audit_path)
    contract_gate = _read_json(config.contract_authoring_gate_audit_path)
    lane_matrix = _read_json(config.lane_matrix_path)
    next_round = _read_json(config.next_round_requirements_path)

    current = _current_status(
        decision_packet=decision_packet,
        decision_record=decision_record,
        decision_gate=decision_gate,
        contract_gate=contract_gate,
        lane_matrix=lane_matrix,
        next_round=next_round,
    )
    issues = _audit_issues(current)
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_protocol_lane_status_report",
        "status": _status(issues=issues, current=current),
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
            "decision_packet": str(config.decision_packet_path),
            "decision_record": str(config.decision_record_path),
            "decision_gate_audit": str(config.decision_gate_audit_path),
            "contract_authoring_gate_audit": str(config.contract_authoring_gate_audit_path),
            "lane_matrix": str(config.lane_matrix_path),
            "next_round_requirements": str(config.next_round_requirements_path),
        },
        "current_status": current,
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This report summarizes protocol-lane gates; it does not record a lane decision.",
            "The old remote execution packet may remain ready, but it is not authorization for a new success attempt.",
            "Current allowed actions do not include local training, remote training, formal claims, or paper result material.",
            "New success training still requires a recorded protocol lane decision and an approved/frozen new or revised contract.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 protocol-lane gate status report.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-packet", type=Path, default=DEFAULT_DECISION_PACKET)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--decision-gate-audit", type=Path, default=DEFAULT_DECISION_GATE_AUDIT)
    parser.add_argument("--contract-authoring-gate-audit", type=Path, default=DEFAULT_CONTRACT_AUTHORING_GATE_AUDIT)
    parser.add_argument("--lane-matrix", type=Path, default=DEFAULT_LANE_MATRIX)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _current_status(
    *,
    decision_packet: dict[str, Any],
    decision_record: dict[str, Any],
    decision_gate: dict[str, Any],
    contract_gate: dict[str, Any],
    lane_matrix: dict[str, Any],
    next_round: dict[str, Any],
) -> dict[str, Any]:
    contract_gate_state = contract_gate.get("contract_gate") if isinstance(contract_gate.get("contract_gate"), dict) else {}
    allowed_actions = _strings(contract_gate_state.get("allowed_next_action_ids"))
    blocked_actions = _strings(contract_gate_state.get("blocked_action_ids"))
    selected_lane = decision_record.get("selected_lane_id")
    return {
        "next_blocked_lane": "protocol_lane_decision" if selected_lane is None else "new_or_revised_contract",
        "decision_packet_status": decision_packet.get("status"),
        "decision_packet_audit_issue_count": int(decision_packet.get("audit_issue_count") or 0),
        "decision_record_status": decision_record.get("status"),
        "decision_record_audit_issue_count": int(decision_record.get("audit_issue_count") or 0),
        "decision_gate_status": decision_gate.get("status"),
        "decision_gate_audit_issue_count": int(decision_gate.get("audit_issue_count") or 0),
        "contract_authoring_gate_status": contract_gate.get("status"),
        "contract_authoring_gate_audit_issue_count": int(contract_gate.get("audit_issue_count") or 0),
        "lane_matrix_status": lane_matrix.get("status"),
        "lane_count": int(lane_matrix.get("lane_count") or len(lane_matrix.get("protocol_lane_evidence_matrix") or [])),
        "next_round_requirements_status": next_round.get("status"),
        "selected_lane_id": selected_lane,
        "contract_action": decision_record.get("contract_action"),
        "contract_drafting_allowed_now": bool(contract_gate_state.get("contract_drafting_allowed_now")),
        "contract_approval_allowed_now": bool(contract_gate_state.get("contract_approval_allowed_now")),
        "draft_contract_allows_training": bool(contract_gate_state.get("draft_contract_allows_training")),
        "allowed_next_action_ids": allowed_actions,
        "blocked_action_ids": blocked_actions,
        "local_training_allowed_now": bool(decision_record.get("local_training_allowed_now")),
        "remote_training_allowed_now": bool(decision_record.get("remote_training_allowed_now")),
        "formal_claim_allowed_now": bool(decision_record.get("formal_claim_allowed_now")),
        "paper_result_material_allowed_now": bool(decision_record.get("paper_result_material_allowed_now")),
        "new_success_training_allowed_now": False,
    }


def _status(*, issues: list[dict[str, Any]], current: dict[str, Any]) -> str:
    if issues:
        return "protocol_lane_status_report_audit_failed"
    if current["next_blocked_lane"] == "protocol_lane_decision":
        return "protocol_lane_status_blocked_pending_lane_decision"
    if current["contract_drafting_allowed_now"]:
        return "protocol_lane_status_ready_for_contract_draft"
    return "protocol_lane_status_blocked_unknown"


def _audit_issues(current: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    expected = {
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    }
    forbidden_allowed_actions = {
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    }
    if current["decision_packet_status"] != "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun":
        issues.append(_issue("decision_packet_not_ready", "Decision packet must be ready for Dr Sun.", observed=current["decision_packet_status"]))
    if current["decision_record_status"] not in {"pending_protocol_lane_decision", "protocol_lane_decision_recorded"}:
        issues.append(_issue("decision_record_status_invalid", "Decision record status must be pending or recorded.", observed=current["decision_record_status"]))
    if current["decision_gate_status"] not in {"protocol_lane_decision_gate_pending_clean", "protocol_lane_decision_gate_recorded_clean"}:
        issues.append(_issue("decision_gate_not_clean", "Decision gate audit must be clean.", observed=current["decision_gate_status"]))
    if current["contract_authoring_gate_audit_issue_count"] != 0:
        issues.append(_issue("contract_authoring_gate_has_issues", "Contract authoring gate must have no audit issues.", observed=current["contract_authoring_gate_audit_issue_count"]))
    if current["lane_matrix_status"] != "formal_gate_protocol_lane_matrix_ready":
        issues.append(_issue("lane_matrix_not_ready", "Protocol lane matrix must be ready.", observed=current["lane_matrix_status"]))
    if current["next_round_requirements_status"] != "formal_gate_next_round_requirements_ready":
        issues.append(_issue("next_round_requirements_not_ready", "Next-round requirements must be ready.", observed=current["next_round_requirements_status"]))
    if current["lane_count"] != 4:
        issues.append(_issue("lane_count_not_four", "Protocol lane matrix must expose exactly four lanes.", observed=current["lane_count"]))
    if current["next_blocked_lane"] == "protocol_lane_decision":
        if current["selected_lane_id"] is not None:
            issues.append(_issue("pending_lane_has_selected_lane", "Pending lane state must not have selected_lane_id.", observed=current["selected_lane_id"]))
        if current["contract_drafting_allowed_now"]:
            issues.append(_issue("contract_drafting_allowed_while_lane_pending", "Contract drafting must be blocked while lane decision is pending."))
        if current["allowed_next_action_ids"] != ["record_protocol_lane_decision"]:
            issues.append(_issue("pending_allowed_actions_drift", "Pending lane state should only allow record_protocol_lane_decision.", observed=current["allowed_next_action_ids"]))
    elif current["allowed_next_action_ids"] != ["draft_new_or_revised_contract_after_lane_decision"]:
        issues.append(
            _issue(
                "recorded_allowed_actions_not_contract_draft_only",
                "Recorded lane state may only allow contract drafting before any new success attempt.",
                observed=current["allowed_next_action_ids"],
            )
        )
    if forbidden_allowed_actions.intersection(current["allowed_next_action_ids"]):
        issues.append(
            _issue(
                "allowed_actions_include_blocked_execution_or_claim",
                "Allowed actions must not include training, preflight, claim, or paper-result actions.",
                observed=current["allowed_next_action_ids"],
            )
        )
    if not expected.issubset(set(current["blocked_action_ids"])):
        issues.append(_issue("blocked_actions_missing_safety_actions", "Training, preflight, claim, and paper actions must stay blocked.", observed=current["blocked_action_ids"]))
    for key in ("local_training_allowed_now", "remote_training_allowed_now", "formal_claim_allowed_now", "paper_result_material_allowed_now", "new_success_training_allowed_now"):
        if current[key]:
            issues.append(_issue(f"{key}_unexpectedly_true", f"{key} must remain false.", observed=current[key]))
    if current["contract_approval_allowed_now"]:
        issues.append(_issue("contract_approval_allowed_too_early", "Status report must not allow contract approval directly."))
    if current["draft_contract_allows_training"]:
        issues.append(_issue("draft_contract_allows_training", "Draft contract must not authorize training."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    state = manifest["current_status"]
    lines = [
        "# Module2 Formal Gate Protocol Lane Status Report",
        "",
        "This file summarizes protocol-lane gates; it is not paper result material.",
        "",
        "## Current Status",
        "",
        f"- next_blocked_lane: `{state['next_blocked_lane']}`",
        f"- decision_record_status: `{state['decision_record_status']}`",
        f"- selected_lane_id: `{state['selected_lane_id']}`",
        f"- contract_drafting_allowed_now: `{state['contract_drafting_allowed_now']}`",
        f"- remote_training_allowed_now: `{state['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{state['formal_claim_allowed_now']}`",
        "",
        "## Safety Flags",
        "",
        f"- local_training_allowed_now: `{state['local_training_allowed_now']}`",
        f"- remote_training_allowed_now: `{state['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{state['formal_claim_allowed_now']}`",
        f"- paper_result_material_allowed_now: `{state['paper_result_material_allowed_now']}`",
        f"- new_success_training_allowed_now: `{state['new_success_training_allowed_now']}`",
        f"- contract_approval_allowed_now: `{state['contract_approval_allowed_now']}`",
        f"- draft_contract_allows_training: `{state['draft_contract_allows_training']}`",
        "",
        "## Allowed Next Actions",
    ]
    for action in state["allowed_next_action_ids"]:
        lines.append(f"- `{action}`")
    lines.extend(["", "## Blocked Actions"])
    for action in state["blocked_action_ids"]:
        lines.append(f"- `{action}`")
    lines.extend(["", "## Claim Boundaries"])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.extend(["", "## Audit", "", f"- status: `{manifest['status']}`", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
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
