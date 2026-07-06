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
EXPECTED_POST_DECISION_CONTRACT_PLAN_ARTIFACT = "module2_formal_gate_post_decision_contract_plan"
EXPECTED_POST_DECISION_CONTRACT_SECTION_COUNT = 8
EXPECTED_POST_DECISION_SHARED_ARTIFACT_COUNT = 10
EXPECTED_POST_DECISION_LANE_COUNT = 4
EXPECTED_PENDING_POST_DECISION_CONTRACT_PLAN_STATUS = "post_decision_contract_plan_ready_blocked_pending_lane_decision"
EXPECTED_RECORDED_POST_DECISION_CONTRACT_PLAN_STATUS = "post_decision_contract_plan_ready_for_contract_draft"
EXPECTED_NEXT_SUCCESS_CATEGORY_COUNTS = {
    "contract": 1,
    "training": 3,
    "evaluation": 2,
    "acceptance": 3,
    "formal_acceptance": 1,
}


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
    post_plan = (
        contract_gate.get("post_decision_contract_plan_summary")
        if isinstance(contract_gate.get("post_decision_contract_plan_summary"), dict)
        else {}
    )
    artifact_summary = _next_success_artifact_summary(next_round)
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
        "post_decision_contract_plan_summary_present": bool(post_plan),
        "post_decision_contract_plan_artifact_name": post_plan.get("artifact_name"),
        "post_decision_contract_plan_status": post_plan.get("status")
        or contract_gate_state.get("post_decision_contract_plan_status"),
        "post_decision_contract_plan_audit_issue_count": int(post_plan.get("audit_issue_count") or 0),
        "post_decision_contract_plan_required_section_count": int(
            post_plan.get("required_contract_section_count")
            or contract_gate_state.get("post_decision_contract_plan_required_section_count")
            or 0
        ),
        "post_decision_contract_plan_shared_artifact_count": int(
            post_plan.get("shared_next_success_attempt_artifact_count")
            or contract_gate_state.get("post_decision_contract_plan_shared_artifact_count")
            or 0
        ),
        "post_decision_contract_plan_lane_count": int(
            post_plan.get("lane_count") or contract_gate_state.get("post_decision_contract_plan_lane_count") or 0
        ),
        "post_decision_contract_plan_selected_lane_id": post_plan.get("gate_selected_lane_id")
        if post_plan
        else contract_gate_state.get("post_decision_contract_plan_selected_lane_id"),
        "post_decision_contract_plan_writes_contract": post_plan.get("writes_contract"),
        "post_decision_contract_plan_approves_contract": post_plan.get("approves_contract"),
        "post_decision_contract_plan_runs_training": post_plan.get("runs_training"),
        "post_decision_contract_plan_runs_remote_preflight": post_plan.get("runs_remote_preflight"),
        "post_decision_contract_plan_remote_training_allowed_now": post_plan.get("remote_training_allowed_now"),
        "post_decision_contract_plan_formal_claim_allowed": post_plan.get("formal_claim_allowed"),
        "post_decision_contract_plan_paper_result_material_allowed": post_plan.get(
            "paper_result_material_allowed"
        ),
        "post_decision_contract_plan_gate_contract_drafting_allowed_now": post_plan.get(
            "gate_contract_drafting_allowed_now"
        ),
        "next_success_attempt_artifact_status": artifact_summary["status"],
        "next_success_attempt_artifact_count": artifact_summary["artifact_count"],
        "next_success_attempt_artifact_category_counts": artifact_summary["category_counts"],
        "next_success_attempt_artifact_ids_by_category": artifact_summary["artifact_ids_by_category"],
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
    issues.extend(_post_decision_plan_issues(current))
    if current["lane_matrix_status"] != "formal_gate_protocol_lane_matrix_ready":
        issues.append(_issue("lane_matrix_not_ready", "Protocol lane matrix must be ready.", observed=current["lane_matrix_status"]))
    if current["next_round_requirements_status"] != "formal_gate_next_round_requirements_ready":
        issues.append(_issue("next_round_requirements_not_ready", "Next-round requirements must be ready.", observed=current["next_round_requirements_status"]))
    if current["lane_count"] != 4:
        issues.append(_issue("lane_count_not_four", "Protocol lane matrix must expose exactly four lanes.", observed=current["lane_count"]))
    if current["next_success_attempt_artifact_count"] != EXPECTED_POST_DECISION_SHARED_ARTIFACT_COUNT:
        issues.append(
            _issue(
                "next_success_attempt_artifact_count_drift",
                "Next success-attempt artifact index must expose the full 10-artifact formal gate list.",
                observed=current["next_success_attempt_artifact_count"],
            )
        )
    if current["next_success_attempt_artifact_category_counts"] != EXPECTED_NEXT_SUCCESS_CATEGORY_COUNTS:
        issues.append(
            _issue(
                "next_success_attempt_artifact_category_counts_drift",
                "Next success-attempt artifact counts must stay at contract/training/evaluation/acceptance/formal_acceptance = 1/3/2/3/1.",
                observed=current["next_success_attempt_artifact_category_counts"],
            )
        )
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


def _post_decision_plan_issues(current: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not current["post_decision_contract_plan_summary_present"]:
        return [
            _issue(
                "post_decision_contract_plan_summary_missing",
                "Protocol-lane status report must consume contract-authoring post-decision plan summary.",
            )
        ]
    if current["post_decision_contract_plan_artifact_name"] != EXPECTED_POST_DECISION_CONTRACT_PLAN_ARTIFACT:
        issues.append(
            _issue(
                "post_decision_contract_plan_artifact_drift",
                "Post-decision contract plan artifact name drifted.",
                observed=current["post_decision_contract_plan_artifact_name"],
            )
        )
    expected_status = (
        EXPECTED_PENDING_POST_DECISION_CONTRACT_PLAN_STATUS
        if current["next_blocked_lane"] == "protocol_lane_decision"
        else EXPECTED_RECORDED_POST_DECISION_CONTRACT_PLAN_STATUS
    )
    if current["post_decision_contract_plan_status"] != expected_status:
        issues.append(
            _issue(
                "post_decision_contract_plan_status_drift",
                "Post-decision contract plan status does not match the protocol-lane state.",
                observed=current["post_decision_contract_plan_status"],
            )
        )
    if current["post_decision_contract_plan_audit_issue_count"] != 0:
        issues.append(
            _issue(
                "post_decision_contract_plan_audit_issues_open",
                "Post-decision contract plan must be audit-clean before status report consumes it.",
                observed=current["post_decision_contract_plan_audit_issue_count"],
            )
        )
    expected_counts = {
        "post_decision_contract_plan_required_section_count": EXPECTED_POST_DECISION_CONTRACT_SECTION_COUNT,
        "post_decision_contract_plan_shared_artifact_count": EXPECTED_POST_DECISION_SHARED_ARTIFACT_COUNT,
        "post_decision_contract_plan_lane_count": EXPECTED_POST_DECISION_LANE_COUNT,
    }
    for key, expected in expected_counts.items():
        if current[key] != expected:
            issues.append(
                _issue(
                    f"{key}_drift",
                    "Post-decision contract plan count drifted.",
                    observed=current[key],
                )
            )
    leaked_flags = [
        key
        for key in (
            "post_decision_contract_plan_writes_contract",
            "post_decision_contract_plan_approves_contract",
            "post_decision_contract_plan_runs_training",
            "post_decision_contract_plan_runs_remote_preflight",
            "post_decision_contract_plan_remote_training_allowed_now",
            "post_decision_contract_plan_formal_claim_allowed",
            "post_decision_contract_plan_paper_result_material_allowed",
        )
        if current[key] is True
    ]
    if leaked_flags:
        issues.append(
            _issue(
                "post_decision_contract_plan_authorization_leak",
                "Post-decision contract plan must not authorize contract writing/approval, training, remote preflight, claims, or paper-result material.",
                observed=leaked_flags,
            )
        )
    if current["next_blocked_lane"] == "protocol_lane_decision":
        if current["post_decision_contract_plan_selected_lane_id"] is not None:
            issues.append(
                _issue(
                    "post_decision_contract_plan_selected_lane_while_pending",
                    "Pending protocol-lane status must consume a post-plan without selected lane.",
                    observed=current["post_decision_contract_plan_selected_lane_id"],
                )
            )
        if current["post_decision_contract_plan_gate_contract_drafting_allowed_now"] is True:
            issues.append(
                _issue(
                    "post_decision_contract_plan_contract_drafting_leak_while_pending",
                    "Post-decision plan must not open contract drafting while lane decision is pending.",
                )
            )
    elif not current["post_decision_contract_plan_selected_lane_id"]:
        issues.append(
            _issue(
                "post_decision_contract_plan_missing_selected_lane_after_record",
                "Recorded protocol-lane status must consume a post-plan with selected lane context.",
            )
        )
    return issues


def _next_success_artifact_summary(next_round: dict[str, Any]) -> dict[str, Any]:
    index = next_round.get("next_success_attempt_artifact_index")
    if not isinstance(index, dict):
        index = {}
    rows = index.get("rows")
    rows = rows if isinstance(rows, list) else []
    ids_by_category: dict[str, list[str]] = {}
    category_counts: dict[str, int] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        category = str(row.get("category") or "")
        artifact_id = str(row.get("artifact_id") or row.get("requirement_id") or "")
        if not category or not artifact_id:
            continue
        ids_by_category.setdefault(category, []).append(artifact_id)
        category_counts[category] = category_counts.get(category, 0) + 1
    return {
        "status": index.get("status"),
        "artifact_count": int(index.get("artifact_count") or len(rows)),
        "category_counts": category_counts,
        "artifact_ids_by_category": ids_by_category,
    }


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
        f"- next_success_attempt_artifact_count: `{state['next_success_attempt_artifact_count']}`",
        f"- next_success_attempt_artifact_category_counts: `{state['next_success_attempt_artifact_category_counts']}`",
        "",
        "## Post-Decision Contract Plan",
        "",
        f"- status: `{state['post_decision_contract_plan_status']}`",
        f"- audit_issue_count: `{state['post_decision_contract_plan_audit_issue_count']}`",
        f"- required_contract_section_count: `{state['post_decision_contract_plan_required_section_count']}`",
        f"- shared_next_success_attempt_artifact_count: `{state['post_decision_contract_plan_shared_artifact_count']}`",
        f"- lane_count: `{state['post_decision_contract_plan_lane_count']}`",
        f"- selected_lane_id: `{state['post_decision_contract_plan_selected_lane_id']}`",
        f"- writes_contract: `{state['post_decision_contract_plan_writes_contract']}`",
        f"- approves_contract: `{state['post_decision_contract_plan_approves_contract']}`",
        f"- runs_training: `{state['post_decision_contract_plan_runs_training']}`",
        f"- runs_remote_preflight: `{state['post_decision_contract_plan_runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{state['post_decision_contract_plan_formal_claim_allowed']}`",
        f"- paper_result_material_allowed: `{state['post_decision_contract_plan_paper_result_material_allowed']}`",
        "",
        "## Missing Next-Attempt Artifacts",
        "",
        f"- index_status: `{state['next_success_attempt_artifact_status']}`",
    ]
    for category, artifact_ids in state["next_success_attempt_artifact_ids_by_category"].items():
        joined = ", ".join(f"`{artifact_id}`" for artifact_id in artifact_ids)
        lines.append(f"- {category}: {joined}")
    lines.extend(
        [
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
    )
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
