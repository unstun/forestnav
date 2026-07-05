from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_f02_6_decision_intake")
DEFAULT_PACKET = Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json")
DEFAULT_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_DECISION_GATE_AUDIT = Path("0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
APPROVE_OBSTACLE_SUMMARY = "approve_obstacle_summary_warm_start"
REJECT_OBSTACLE_SUMMARY = "reject_obstacle_summary_warm_start"
DECISION_OWNER = "Dr Sun"
DECISION_NOTE_GUIDANCE = (
    "selected decision",
    "human rationale",
    "evidence basis",
    "risk accepted or avoided",
    "next gated action",
)


@dataclass(frozen=True)
class F026DecisionIntakeConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    packet_path: Path = DEFAULT_PACKET
    decision_record_path: Path = DEFAULT_RECORD
    decision_gate_audit_path: Path = DEFAULT_DECISION_GATE_AUDIT
    status_report_path: Path = DEFAULT_STATUS_REPORT
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = F026DecisionIntakeConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        packet_path=args.packet,
        decision_record_path=args.decision_record,
        decision_gate_audit_path=args.decision_gate_audit,
        status_report_path=args.status_report,
        remaining_deliverables_path=args.remaining_deliverables,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "f02_6_decision_intake.json"
    markdown_out = config.markdown_out or output_dir / "f02_6_decision_intake.md"
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


def build_manifest(config: F026DecisionIntakeConfig) -> dict[str, Any]:
    packet = _read_json(config.packet_path)
    record = _read_json(config.decision_record_path)
    gate_audit = _read_json(config.decision_gate_audit_path)
    status_report = _read_json(config.status_report_path)
    remaining = _read_json(config.remaining_deliverables_path)
    current_state = _current_state(packet=packet, record=record, gate_audit=gate_audit, status_report=status_report, remaining=remaining)
    decision_evidence_matrix_summary = _decision_evidence_matrix_summary(packet)
    issues = _audit_issues(
        config=config,
        packet=packet,
        record=record,
        gate_audit=gate_audit,
        status_report=status_report,
        remaining=remaining,
        current_state=current_state,
    )
    decision_intake_contract = _decision_intake_contract(gate_audit)
    post_decision_route_matrix = _post_decision_route_matrix()
    formal_gate_decision_impact_summary = _formal_gate_decision_impact_summary(
        current_state=current_state,
        post_decision_route_matrix=post_decision_route_matrix,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_f02_6_decision_intake",
        "status": _status(record_status=current_state["record_status"], issues=issues),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "inputs": {
            "decision_packet": str(config.packet_path),
            "decision_record": str(config.decision_record_path),
            "decision_gate_audit": str(config.decision_gate_audit_path),
            "formal_gate_status_report": str(config.status_report_path),
            "remaining_deliverables": str(config.remaining_deliverables_path),
        },
        "current_state": current_state,
        "decision_evidence_matrix_summary": decision_evidence_matrix_summary,
        "next_human_decision_request": _next_human_decision_request(
            current_state=current_state,
            decision_intake_contract=decision_intake_contract,
            post_decision_route_matrix=post_decision_route_matrix,
        ),
        "formal_gate_decision_impact_summary": formal_gate_decision_impact_summary,
        "decision_intake_contract": decision_intake_contract,
        "post_decision_route_matrix": post_decision_route_matrix,
        "post_decision_non_authorizations": _post_decision_non_authorizations(),
        "invalid_inputs": _invalid_inputs(),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This intake explains how to close F02.6; it does not close F02.6.",
            "It must not be cited as a PPO performance result or warm-start effect result.",
            "The only valid decider for a non-pending F02.6 record is Dr Sun.",
            "Approval records the human decision and leads to source-fresh gate regeneration; it is not a command to train.",
            "Rejected obstacle-summary warm-start keeps formal warm-start PPO blocked and routes to a stronger/full patch-CNN protocol.",
            "Local PPO training remains disallowed.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only Module2 F02.6 human decision intake artifact.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_RECORD)
    parser.add_argument("--decision-gate-audit", type=Path, default=DEFAULT_DECISION_GATE_AUDIT)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    return parser.parse_args(list(argv) if argv is not None else None)


def _current_state(
    *,
    packet: dict[str, Any],
    record: dict[str, Any],
    gate_audit: dict[str, Any],
    status_report: dict[str, Any],
    remaining: dict[str, Any],
) -> dict[str, Any]:
    recommendation = packet.get("recommendation") if isinstance(packet.get("recommendation"), dict) else {}
    authorization = packet.get("current_authorization") if isinstance(packet.get("current_authorization"), dict) else {}
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    remaining_permissions = remaining.get("permissions_now") if isinstance(remaining.get("permissions_now"), dict) else {}
    category_counts = remaining.get("category_counts") if isinstance(remaining.get("category_counts"), dict) else {}
    next_blocked_lane = _next_blocked_lane(status_report=status_report, remaining=remaining)
    return {
        "packet_status": packet.get("status"),
        "packet_recommendation": recommendation.get("decision"),
        "packet_decision_owner": recommendation.get("decision_owner"),
        "packet_formal_claim_allowed": recommendation.get("formal_claim_allowed"),
        "record_status": record.get("status"),
        "record_requested_decision": record.get("requested_decision"),
        "record_decider": record.get("decider"),
        "effective_warm_start_decision": record.get("effective_warm_start_decision"),
        "record_remote_training_allowed": record.get("remote_training_allowed"),
        "record_remote_preflight_allowed_now": record.get("remote_preflight_allowed_now"),
        "record_remote_training_allowed_now": record.get("remote_training_allowed_now"),
        "record_local_training_allowed": record.get("local_training_allowed"),
        "record_formal_claim_allowed": record.get("formal_claim_allowed"),
        "packet_authorization_status": authorization.get("authorization_status"),
        "packet_current_allowed_action_ids": list(authorization.get("current_allowed_action_ids") or ()),
        "packet_current_blocked_action_ids": list(authorization.get("current_blocked_action_ids") or ()),
        "packet_post_decision_routes_are_current_authorization": authorization.get(
            "post_decision_routes_are_current_authorization"
        ),
        "packet_remote_preflight_allowed_now": authorization.get("remote_preflight_allowed_now"),
        "packet_remote_training_allowed_now": authorization.get("remote_training_allowed_now"),
        "packet_local_training_allowed_now": authorization.get("local_training_allowed_now"),
        "packet_formal_claim_allowed_now": authorization.get("formal_claim_allowed_now"),
        "packet_paper_result_material_allowed_now": authorization.get("paper_result_material_allowed_now"),
        "decision_gate_status": gate_audit.get("status"),
        "decision_gate_issue_count": gate_audit.get("audit_issue_count"),
        "status_report_status": status_report.get("status"),
        "next_blocked_lane": next_blocked_lane,
        "status_report_local_training_allowed_now": permissions.get("local_training_allowed_now"),
        "status_report_remote_preflight_allowed_now": permissions.get("remote_preflight_allowed_now"),
        "status_report_remote_training_allowed_now": permissions.get("remote_training_allowed_now"),
        "status_report_formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        "remaining_deliverables_status": remaining.get("status"),
        "missing_deliverable_count": remaining.get("missing_deliverable_count"),
        "open_category_count": remaining.get("open_category_count"),
        "remaining_local_training_allowed_now": remaining_permissions.get("local_training_allowed_now"),
        "remaining_remote_preflight_allowed_now": remaining_permissions.get("remote_preflight_allowed_now"),
        "remaining_remote_training_allowed_now": remaining_permissions.get("remote_training_allowed_now"),
        "remaining_formal_claim_allowed_now": remaining_permissions.get("formal_claim_allowed_now"),
        "missing_by_category": {
            name: payload.get("missing_count")
            for name, payload in category_counts.items()
            if isinstance(payload, dict)
        },
    }


def _decision_evidence_matrix_summary(packet: dict[str, Any]) -> dict[str, Any]:
    matrix = packet.get("decision_evidence_matrix")
    matrix = matrix if isinstance(matrix, dict) else {}
    routes = matrix.get("routes") if isinstance(matrix.get("routes"), list) else []
    route_decisions = [str(route.get("decision")) for route in routes if isinstance(route, dict) and route.get("decision")]
    evidence_counts_by_route: dict[str, int] = {}
    invalid_substitute_counts_by_route: dict[str, int] = {}
    for route in routes:
        if not isinstance(route, dict) or not route.get("decision"):
            continue
        decision = str(route["decision"])
        required_evidence = route.get("required_evidence") if isinstance(route.get("required_evidence"), list) else []
        invalid_substitutes = route.get("invalid_substitutes") if isinstance(route.get("invalid_substitutes"), list) else []
        evidence_counts_by_route[decision] = len(required_evidence)
        invalid_substitute_counts_by_route[decision] = len(invalid_substitutes)
    missing_ids = _strings(matrix.get("missing_required_evidence_ids"))
    return {
        "present": bool(matrix),
        "matrix_id": matrix.get("matrix_id"),
        "status": matrix.get("status"),
        "route_count": int(matrix.get("route_count") or len(routes)),
        "route_decisions": sorted(route_decisions),
        "required_evidence_count": int(matrix.get("required_evidence_count") or sum(evidence_counts_by_route.values())),
        "satisfied_required_evidence_count": int(matrix.get("satisfied_required_evidence_count") or 0),
        "missing_required_evidence_count": int(matrix.get("missing_required_evidence_count") or len(missing_ids)),
        "missing_required_evidence_ids": missing_ids,
        "current_authorization_allowed_now": matrix.get("current_authorization_allowed_now")
        if isinstance(matrix.get("current_authorization_allowed_now"), bool)
        else None,
        "remote_preflight_allowed_now": matrix.get("remote_preflight_allowed_now")
        if isinstance(matrix.get("remote_preflight_allowed_now"), bool)
        else None,
        "remote_training_allowed_now": matrix.get("remote_training_allowed_now")
        if isinstance(matrix.get("remote_training_allowed_now"), bool)
        else None,
        "local_training_allowed_now": matrix.get("local_training_allowed_now")
        if isinstance(matrix.get("local_training_allowed_now"), bool)
        else None,
        "formal_claim_allowed_now": matrix.get("formal_claim_allowed_now")
        if isinstance(matrix.get("formal_claim_allowed_now"), bool)
        else None,
        "paper_result_material_allowed_now": matrix.get("paper_result_material_allowed_now")
        if isinstance(matrix.get("paper_result_material_allowed_now"), bool)
        else None,
        "source_issue_count": int(matrix.get("source_issue_count") or 0),
        "global_invalid_substitute_count": len(matrix.get("global_invalid_substitutes") or []),
        "evidence_counts_by_route": evidence_counts_by_route,
        "invalid_substitute_counts_by_route": invalid_substitute_counts_by_route,
    }


def _next_blocked_lane(*, status_report: dict[str, Any], remaining: dict[str, Any]) -> str | None:
    lane = status_report.get("next_blocked_lane")
    if isinstance(lane, dict) and lane.get("lane_id"):
        return str(lane["lane_id"])
    if isinstance(lane, str):
        return lane
    status_summary = status_report.get("current_gate_summary")
    if isinstance(status_summary, dict) and status_summary.get("next_blocked_lane"):
        return str(status_summary["next_blocked_lane"])
    remaining_summary = remaining.get("current_gate_summary")
    if isinstance(remaining_summary, dict) and remaining_summary.get("next_blocked_lane"):
        return str(remaining_summary["next_blocked_lane"])
    return None


def _decision_intake_contract(gate_audit: dict[str, Any]) -> dict[str, Any]:
    audit_actions = gate_audit.get("allowed_next_human_actions") if isinstance(gate_audit.get("allowed_next_human_actions"), list) else []
    return {
        "decision_owner_required": DECISION_OWNER,
        "valid_decisions": [APPROVE_OBSTACLE_SUMMARY, REJECT_OBSTACLE_SUMMARY],
        "required_record_fields_for_non_pending_decision": [
            "decision",
            "decider",
            "decision_note",
        ],
        "field_rules": {
            "decision": f"must be one of {APPROVE_OBSTACLE_SUMMARY} or {REJECT_OBSTACLE_SUMMARY}",
            "decider": f"must equal {DECISION_OWNER}",
            "decision_note": "must be a human-readable Dr Sun note explaining the approval or rejection rationale",
        },
        "decision_note_guidance": list(DECISION_NOTE_GUIDANCE),
        "record_command_templates": [
            _command_template(APPROVE_OBSTACLE_SUMMARY),
            _command_template(REJECT_OBSTACLE_SUMMARY),
        ],
        "allowed_next_human_actions_from_gate_audit": audit_actions,
    }


def _next_human_decision_request(
    *,
    current_state: dict[str, Any],
    decision_intake_contract: dict[str, Any],
    post_decision_route_matrix: list[dict[str, Any]],
) -> dict[str, Any]:
    route_by_decision = {
        str(route["decision"]): route
        for route in post_decision_route_matrix
        if isinstance(route, dict) and route.get("decision")
    }
    valid_decisions = _strings(decision_intake_contract.get("valid_decisions"))
    return {
        "status": "awaiting_dr_sun_decision"
        if current_state.get("record_status") == "pending_human_decision"
        else "decision_recorded",
        "decision_owner_required": decision_intake_contract.get("decision_owner_required"),
        "valid_decisions": valid_decisions,
        "required_record_fields": _strings(
            decision_intake_contract.get("required_record_fields_for_non_pending_decision")
        ),
        "current_allowed_action_ids": _strings(current_state.get("packet_current_allowed_action_ids")),
        "current_blocked_action_ids": _strings(current_state.get("packet_current_blocked_action_ids")),
        "post_decision_routes_are_current_authorization": current_state.get(
            "packet_post_decision_routes_are_current_authorization"
        )
        is True,
        "all_execution_disabled_now": all(
            current_state.get(key) is False
            for key in (
                "packet_remote_preflight_allowed_now",
                "packet_remote_training_allowed_now",
                "packet_local_training_allowed_now",
                "packet_formal_claim_allowed_now",
                "packet_paper_result_material_allowed_now",
                "status_report_remote_preflight_allowed_now",
                "status_report_remote_training_allowed_now",
                "status_report_local_training_allowed_now",
                "status_report_formal_claim_allowed_now",
                "remaining_remote_preflight_allowed_now",
                "remaining_remote_training_allowed_now",
                "remaining_local_training_allowed_now",
                "remaining_formal_claim_allowed_now",
            )
        ),
        "route_effects": {
            decision: {
                "next_lane_after_record": route_by_decision.get(decision, {}).get("next_lane_after_record"),
                "allows_remote_preflight_now": route_by_decision.get(decision, {}).get(
                    "allows_remote_preflight_now"
                ),
                "allows_remote_training_now": route_by_decision.get(decision, {}).get(
                    "allows_remote_training_now"
                ),
                "allows_formal_claim_now": route_by_decision.get(decision, {}).get(
                    "allows_formal_claim_now"
                ),
                "required_next_artifacts": _strings(
                    route_by_decision.get(decision, {}).get("required_next_artifacts")
                ),
            }
            for decision in valid_decisions
        },
    }


def _post_decision_non_authorizations() -> list[dict[str, Any]]:
    return [
        {
            "action": "local_training",
            "allowed_after_decision_record": False,
            "reason": "Formal PPO training is remote-only on gpu3070ti-relay.",
        },
        {
            "action": "paper_formal_result_claim",
            "allowed_after_decision_record": False,
            "reason": "A decision record is not a PPO checkpoint, evaluation CSV, H02 acceptance, or paper-result input.",
        },
        {
            "action": "skip_source_fresh_regeneration",
            "allowed_after_decision_record": False,
            "reason": "The post-F02.6 plan must regenerate gate artifacts before approved remote preflight.",
        },
        {
            "action": "treat_smoke_or_no_warm_failure_as_warm_start_result",
            "allowed_after_decision_record": False,
            "reason": "Smoke and no-warm failure artifacts are invalid substitutes for the approved warm-start formal run.",
        },
    ]


def _formal_gate_decision_impact_summary(
    *,
    current_state: dict[str, Any],
    post_decision_route_matrix: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    route_by_decision = {
        str(route["decision"]): route
        for route in post_decision_route_matrix
        if isinstance(route, dict) and route.get("decision")
    }
    return {
        "summary_id": "module2_f02_6_formal_gate_decision_impact",
        "purpose": "make the human F02.6 decision effect explicit before any formal gate execution",
        "not_paper_result_material": True,
        "current_blocker": current_state.get("next_blocked_lane"),
        "current_record_status": current_state.get("record_status"),
        "missing_deliverable_count": current_state.get("missing_deliverable_count"),
        "missing_by_category": current_state.get("missing_by_category"),
        "current_allowed_action_ids": _strings(current_state.get("packet_current_allowed_action_ids")),
        "current_blocked_action_ids": _strings(current_state.get("packet_current_blocked_action_ids")),
        "decision_routes": [
            _decision_route_impact(
                decision=APPROVE_OBSTACLE_SUMMARY,
                route=route_by_decision.get(APPROVE_OBSTACLE_SUMMARY, {}),
            ),
            _decision_route_impact(
                decision=REJECT_OBSTACLE_SUMMARY,
                route=route_by_decision.get(REJECT_OBSTACLE_SUMMARY, {}),
            ),
        ],
        "invariants_after_any_decision_record": {
            "decision_record_is_not_training_authorization": True,
            "decision_record_is_not_paper_result_material": True,
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "formal_training_still_requires": [
                "source_freshness_audit",
                "post_f02_6_regeneration_plan",
                "post_f02_6_plan_audit",
                "remote_formal_execution_packet_ready",
                "approved_remote_preflight",
            ],
        },
    }


def _decision_route_impact(*, decision: str, route: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision": decision,
        "next_lane_after_record": route.get("next_lane_after_record"),
        "next_protocol": route.get("next_protocol"),
        "requires_new_protocol_contract": route.get("requires_new_protocol_contract"),
        "allows_local_training_now": route.get("allows_local_training_now"),
        "allows_remote_preflight_now": route.get("allows_remote_preflight_now"),
        "allows_remote_training_now": route.get("allows_remote_training_now"),
        "allows_formal_claim_now": route.get("allows_formal_claim_now"),
        "required_next_artifacts": _strings(route.get("required_next_artifacts")),
        "claim_boundary": route.get("claim_boundary"),
    }


def _post_decision_route_matrix() -> list[dict[str, Any]]:
    return [
        {
            "decision": APPROVE_OBSTACLE_SUMMARY,
            "record_status_after_command": "approved",
            "next_lane_after_record": "source_fresh_regeneration",
            "next_protocol": "obstacle-summary BC warm-start PPO formal gate",
            "requires_new_protocol_contract": False,
            "allows_local_training_now": False,
            "allows_remote_preflight_now": False,
            "allows_remote_training_now": False,
            "allows_formal_claim_now": False,
            "required_next_artifacts": [
                "source_freshness_audit",
                "post_f02_6_regeneration_plan",
                "post_f02_6_plan_audit",
            ],
            "first_remote_stage_after_regeneration": "approved_remote_preflight",
            "remote_training_stage": "gate3_remote_training",
            "claim_boundary": "Approval records Dr Sun's decision; it does not directly run preflight, train, or allow paper claims.",
        },
        {
            "decision": REJECT_OBSTACLE_SUMMARY,
            "record_status_after_command": "rejected",
            "next_lane_after_record": "protocol_redesign",
            "next_protocol": "stronger/full patch-CNN warm-start protocol",
            "requires_new_protocol_contract": True,
            "allows_local_training_now": False,
            "allows_remote_preflight_now": False,
            "allows_remote_training_now": False,
            "allows_formal_claim_now": False,
            "required_next_artifacts": [
                "new_or_revised_research_contract",
                "stronger_patch_cnn_protocol_spec",
                "fresh_formal_gate_artifact_plan",
            ],
            "first_remote_stage_after_regeneration": None,
            "remote_training_stage": None,
            "claim_boundary": "Rejection blocks obstacle-summary warm-start PPO until a stronger protocol is approved.",
        },
    ]


def _invalid_inputs() -> list[dict[str, Any]]:
    return [
        {
            "input": "decider other than Dr Sun",
            "why_invalid": "Only Dr Sun can close F02.6.",
        },
        {
            "input": "approval or rejection without a decision note",
            "why_invalid": "A formal research decision must preserve rationale for audit and future paper rebuttal.",
        },
        {
            "input": "manual permission flips in downstream JSON",
            "why_invalid": "Downstream permissions must be regenerated from the decision record and gate artifacts.",
        },
        {
            "input": "local training output",
            "why_invalid": "The formal PPO checkpoint must be produced on gpu3070ti-relay after the gate opens.",
        },
        {
            "input": "paper result table or claim preview",
            "why_invalid": "F02.6 intake is not formal evaluation evidence.",
        },
    ]


def _audit_issues(
    *,
    config: F026DecisionIntakeConfig,
    packet: dict[str, Any],
    record: dict[str, Any],
    gate_audit: dict[str, Any],
    status_report: dict[str, Any],
    remaining: dict[str, Any],
    current_state: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for label, path, payload in (
        ("decision_packet", config.packet_path, packet),
        ("decision_record", config.decision_record_path, record),
        ("decision_gate_audit", config.decision_gate_audit_path, gate_audit),
        ("formal_gate_status_report", config.status_report_path, status_report),
        ("remaining_deliverables", config.remaining_deliverables_path, remaining),
    ):
        if not Path(path).is_file():
            issues.append(_issue(f"missing_{label}", f"Required F02.6 intake input is missing: {path}"))
        elif not payload:
            issues.append(_issue(f"empty_{label}", f"Required F02.6 intake input is empty or unreadable: {path}"))

    if current_state["packet_decision_owner"] != DECISION_OWNER:
        issues.append(_issue("packet_decision_owner_not_dr_sun", "Decision packet must name Dr Sun as owner.", current_state["packet_decision_owner"]))
    if current_state["packet_formal_claim_allowed"] is not False:
        issues.append(_issue("packet_allows_formal_claim", "Decision packet must not allow formal claims.", current_state["packet_formal_claim_allowed"]))
    if current_state["packet_recommendation"] != APPROVE_OBSTACLE_SUMMARY:
        issues.append(_issue("packet_recommendation_not_obstacle_summary", "Current intake expects the obstacle-summary warm-start recommendation.", current_state["packet_recommendation"]))
    if current_state["packet_authorization_status"] != "blocked_until_dr_sun_decision":
        issues.append(
            _issue(
                "packet_current_authorization_not_blocked",
                "Decision packet current authorization must remain blocked until Dr Sun records F02.6.",
                current_state["packet_authorization_status"],
            )
        )
    if current_state["packet_current_allowed_action_ids"] != ["record_f02_6_decision"]:
        issues.append(
            _issue(
                "packet_current_allowed_actions_not_decision_only",
                "Decision packet must allow only recording F02.6 while the gate is pending.",
                current_state["packet_current_allowed_action_ids"],
            )
        )
    required_blocked_actions = {
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    }
    missing_blocked_actions = sorted(required_blocked_actions.difference(current_state["packet_current_blocked_action_ids"]))
    if missing_blocked_actions:
        issues.append(
            _issue(
                "packet_current_authorization_missing_blocked_actions",
                "Decision packet current authorization must block every execution and result-claim path.",
                missing_blocked_actions,
            )
        )
    if current_state["packet_post_decision_routes_are_current_authorization"] is not False:
        issues.append(
            _issue(
                "packet_treats_post_decision_routes_as_current_authorization",
                "Post-decision routes must not be current execution authorization.",
                current_state["packet_post_decision_routes_are_current_authorization"],
            )
        )
    for field in (
        "packet_remote_preflight_allowed_now",
        "packet_remote_training_allowed_now",
        "packet_local_training_allowed_now",
        "packet_formal_claim_allowed_now",
        "packet_paper_result_material_allowed_now",
    ):
        if current_state[field] is not False:
            issues.append(_issue(f"{field}_not_false", "Decision packet current authorization must not allow execution or result material.", current_state[field]))

    matrix_summary = _decision_evidence_matrix_summary(packet)
    expected_decisions = {APPROVE_OBSTACLE_SUMMARY, REJECT_OBSTACLE_SUMMARY}
    if not matrix_summary["present"]:
        issues.append(_issue("decision_evidence_matrix_missing", "Decision packet must expose a decision evidence matrix."))
    if matrix_summary["matrix_id"] != "module2_f02_6_decision_evidence_matrix":
        issues.append(_issue("decision_evidence_matrix_id_invalid", "Decision evidence matrix must use the expected matrix id.", matrix_summary["matrix_id"]))
    if matrix_summary["status"] != "ready_for_dr_sun_decision_not_authorization":
        issues.append(_issue("decision_evidence_matrix_status_invalid", "Decision evidence matrix must be ready for Dr Sun decision but not authorization.", matrix_summary["status"]))
    if matrix_summary["route_count"] != 2:
        issues.append(_issue("decision_evidence_matrix_route_count_invalid", "Decision evidence matrix must cover approve and reject routes.", matrix_summary["route_count"]))
    if not expected_decisions.issubset(set(matrix_summary["route_decisions"])):
        issues.append(_issue("decision_evidence_matrix_route_decisions_incomplete", "Decision evidence matrix must cover approve and reject decisions.", matrix_summary["route_decisions"]))
    if matrix_summary["required_evidence_count"] < 7:
        issues.append(_issue("decision_evidence_matrix_required_evidence_incomplete", "Decision evidence matrix must preserve the seven current F02.6 evidence rows.", matrix_summary["required_evidence_count"]))
    if matrix_summary["missing_required_evidence_count"] != 0:
        issues.append(_issue("decision_evidence_matrix_missing_required_evidence", "Decision evidence matrix must not have missing required evidence before it supports the human decision.", matrix_summary["missing_required_evidence_ids"]))
    if matrix_summary["source_issue_count"] != 0:
        issues.append(_issue("decision_evidence_matrix_source_issues_open", "Decision evidence matrix must not inherit source integrity issues.", matrix_summary["source_issue_count"]))
    if matrix_summary["global_invalid_substitute_count"] == 0:
        issues.append(_issue("decision_evidence_matrix_global_invalid_substitutes_missing", "Decision evidence matrix must list global invalid substitutes."))
    for decision in expected_decisions:
        if matrix_summary["evidence_counts_by_route"].get(decision, 0) == 0:
            issues.append(_issue(f"decision_evidence_matrix_{decision}_missing_evidence", "Each decision route must list required evidence rows."))
        if matrix_summary["invalid_substitute_counts_by_route"].get(decision, 0) == 0:
            issues.append(_issue(f"decision_evidence_matrix_{decision}_missing_invalid_substitutes", "Each decision route must list invalid substitutes."))
    for field in (
        "current_authorization_allowed_now",
        "remote_preflight_allowed_now",
        "remote_training_allowed_now",
        "local_training_allowed_now",
        "formal_claim_allowed_now",
        "paper_result_material_allowed_now",
    ):
        if matrix_summary[field] is not False:
            issues.append(_issue(f"decision_evidence_matrix_{field}_not_false", "Decision evidence matrix must not authorize execution or result material.", matrix_summary[field]))

    record_status = current_state["record_status"]
    if record_status not in {"pending_human_decision", "approved", "rejected"}:
        issues.append(_issue("record_status_unknown", "Decision record status must be pending_human_decision, approved, or rejected.", record_status))
    if current_state["record_local_training_allowed"] is not False:
        issues.append(_issue("record_allows_local_training", "Decision record must never allow local training.", current_state["record_local_training_allowed"]))
    if current_state["record_formal_claim_allowed"] is not False:
        issues.append(_issue("record_allows_formal_claim", "Decision record must never allow formal result claims.", current_state["record_formal_claim_allowed"]))
    if record_status == "pending_human_decision" and current_state["record_decider"] is not None:
        issues.append(_issue("pending_record_has_decider", "Pending F02.6 record must not name a decider.", current_state["record_decider"]))
    if record_status in {"approved", "rejected"} and current_state["record_decider"] != DECISION_OWNER:
        issues.append(_issue("closed_record_decider_not_dr_sun", "Approved/rejected F02.6 record must be decided by Dr Sun.", current_state["record_decider"]))

    if current_state["decision_gate_issue_count"] not in {0, "0"}:
        issues.append(_issue("decision_gate_has_issues", "F02.6 decision gate audit must be clean before using this intake.", current_state["decision_gate_issue_count"]))
    if current_state["decision_gate_status"] == "f02_6_decision_gate_audit_failed":
        issues.append(_issue("decision_gate_failed", "F02.6 decision gate audit currently failed.", current_state["decision_gate_status"]))

    for field in (
        "status_report_local_training_allowed_now",
        "status_report_formal_claim_allowed_now",
        "remaining_local_training_allowed_now",
        "remaining_formal_claim_allowed_now",
    ):
        if current_state[field] is not False:
            issues.append(_issue(f"{field}_not_false", "F02.6 intake must not coincide with local training or formal claim permission.", current_state[field]))

    if record_status == "pending_human_decision":
        if current_state["next_blocked_lane"] != "decision":
            issues.append(_issue("pending_next_blocked_lane_not_decision", "Pending F02.6 should keep next blocked lane at decision.", current_state["next_blocked_lane"]))
        for field in (
            "status_report_remote_preflight_allowed_now",
            "status_report_remote_training_allowed_now",
            "remaining_remote_preflight_allowed_now",
            "remaining_remote_training_allowed_now",
        ):
            if current_state[field] is not False:
                issues.append(_issue(f"{field}_not_false", "Pending F02.6 must not allow remote preflight or remote training.", current_state[field]))
        if current_state["packet_remote_preflight_allowed_now"] != current_state["status_report_remote_preflight_allowed_now"]:
            issues.append(
                _issue(
                    "packet_status_report_remote_preflight_permission_mismatch",
                    "Packet and status report must agree on remote preflight permission while F02.6 is pending.",
                    {
                        "packet": current_state["packet_remote_preflight_allowed_now"],
                        "status_report": current_state["status_report_remote_preflight_allowed_now"],
                    },
                )
            )
        if current_state["packet_remote_training_allowed_now"] != current_state["status_report_remote_training_allowed_now"]:
            issues.append(
                _issue(
                    "packet_status_report_remote_training_permission_mismatch",
                    "Packet and status report must agree on remote training permission while F02.6 is pending.",
                    {
                        "packet": current_state["packet_remote_training_allowed_now"],
                        "status_report": current_state["status_report_remote_training_allowed_now"],
                    },
                )
            )
        if current_state["remaining_deliverables_status"] != "formal_gate_deliverables_blocked":
            issues.append(_issue("remaining_deliverables_not_blocked", "Pending F02.6 should keep remaining deliverables blocked.", current_state["remaining_deliverables_status"]))

    return _unique_issues(issues)


def _status(*, record_status: Any, issues: Sequence[dict[str, Any]]) -> str:
    if issues:
        return "f02_6_decision_intake_failed"
    if record_status == "pending_human_decision":
        return "f02_6_decision_intake_pending_clean"
    if record_status in {"approved", "rejected"}:
        return "f02_6_decision_intake_closed_clean"
    return "f02_6_decision_intake_failed"


def _command_template(decision: str) -> dict[str, str]:
    note = "<Dr Sun approval note>" if decision == APPROVE_OBSTACLE_SUMMARY else "<Dr Sun rejection note>"
    return {
        "decision": decision,
        "command": (
            "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record "
            f"--decision {decision} --decider 'Dr Sun' --decision-note '{note}'"
        ),
    }


def _issue(issue_id: str, message: str, observed: Any | None = None) -> dict[str, Any]:
    issue = {"issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
    return issue


def _strings(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    return [str(item) for item in raw if item]


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id"))
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        out.append(issue)
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    state = manifest["current_state"]
    lines = [
        "# Module2 F02.6 Decision Intake",
        "",
        "This read-only artifact explains how F02.6 can be closed. It does not record a decision, run preflight, train, or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- decision_owner_required: `{manifest['decision_intake_contract']['decision_owner_required']}`",
        f"- record_status: `{state['record_status']}`",
        f"- effective_warm_start_decision: `{state['effective_warm_start_decision']}`",
        f"- packet_recommendation: `{state['packet_recommendation']}`",
        f"- packet_authorization_status: `{state['packet_authorization_status']}`",
        f"- packet_allowed_now: `{', '.join(state['packet_current_allowed_action_ids'])}`",
        f"- packet_blocked_now: `{', '.join(state['packet_current_blocked_action_ids'])}`",
        f"- next_blocked_lane: `{state['next_blocked_lane']}`",
        f"- missing_deliverable_count: `{state['missing_deliverable_count']}`",
        f"- local_training_allowed_now: `{state['status_report_local_training_allowed_now']}`",
        f"- remote_preflight_allowed_now: `{state['status_report_remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{state['status_report_remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{state['status_report_formal_claim_allowed_now']}`",
        "",
        "## Next Human Decision Request",
        "",
    ]
    request = manifest["next_human_decision_request"]
    lines.append(f"- status: `{request['status']}`")
    lines.append(f"- decision_owner_required: `{request['decision_owner_required']}`")
    lines.append(f"- valid_decisions: `{', '.join(request['valid_decisions'])}`")
    lines.append(f"- required_record_fields: `{', '.join(request['required_record_fields'])}`")
    lines.append(f"- current_allowed_action_ids: `{', '.join(request['current_allowed_action_ids'])}`")
    lines.append(f"- current_blocked_action_ids: `{', '.join(request['current_blocked_action_ids'])}`")
    lines.append(
        f"- post_decision_routes_are_current_authorization: `{request['post_decision_routes_are_current_authorization']}`"
    )
    lines.append(f"- all_execution_disabled_now: `{request['all_execution_disabled_now']}`")
    for decision, route in request["route_effects"].items():
        lines.append(
            f"- `{decision}`: next_lane_after_record=`{route['next_lane_after_record']}`, "
            f"remote_preflight_now=`{route['allows_remote_preflight_now']}`, "
            f"remote_training_now=`{route['allows_remote_training_now']}`, "
            f"formal_claim_now=`{route['allows_formal_claim_now']}`"
        )
    impact = manifest["formal_gate_decision_impact_summary"]
    invariants = impact["invariants_after_any_decision_record"]
    lines.extend([
        "",
        "## Formal Gate Decision Impact",
        "",
        f"- current_blocker: `{impact['current_blocker']}`",
        f"- current_record_status: `{impact['current_record_status']}`",
        f"- missing_deliverable_count: `{impact['missing_deliverable_count']}`",
        f"- missing_by_category: `{impact['missing_by_category']}`",
        f"- current_allowed_action_ids: `{', '.join(impact['current_allowed_action_ids'])}`",
        f"- current_blocked_action_ids: `{', '.join(impact['current_blocked_action_ids'])}`",
    ])
    for route in impact["decision_routes"]:
        lines.extend(
            [
                f"- `{route['decision']}`: next_lane_after_record=`{route['next_lane_after_record']}`, "
                f"requires_new_protocol_contract=`{route['requires_new_protocol_contract']}`, "
                f"remote_training_now=`{route['allows_remote_training_now']}`, "
                f"formal_claim_now=`{route['allows_formal_claim_now']}`",
            ]
        )
    lines.extend(
        [
            f"- decision_record_is_not_training_authorization: `{invariants['decision_record_is_not_training_authorization']}`",
            f"- decision_record_is_not_paper_result_material: `{invariants['decision_record_is_not_paper_result_material']}`",
            f"- local_training_allowed_now_after_record: `{invariants['local_training_allowed_now']}`",
            f"- remote_preflight_allowed_now_after_record: `{invariants['remote_preflight_allowed_now']}`",
            f"- remote_training_allowed_now_after_record: `{invariants['remote_training_allowed_now']}`",
            f"- formal_claim_allowed_now_after_record: `{invariants['formal_claim_allowed_now']}`",
            f"- paper_result_material_allowed_now_after_record: `{invariants['paper_result_material_allowed_now']}`",
            f"- formal_training_still_requires: `{', '.join(invariants['formal_training_still_requires'])}`",
        ]
    )
    lines.extend([
        "",
        "## Required Fields",
        "",
    ])
    for field in manifest["decision_intake_contract"]["required_record_fields_for_non_pending_decision"]:
        rule = manifest["decision_intake_contract"]["field_rules"][field]
        lines.append(f"- `{field}`: {rule}")
    lines.append(
        f"- decision_note_guidance: `{', '.join(manifest['decision_intake_contract']['decision_note_guidance'])}`"
    )
    lines.extend(["", "## Command Templates", ""])
    for template in manifest["decision_intake_contract"]["record_command_templates"]:
        lines.extend([f"### {template['decision']}", "```bash", template["command"], "```", ""])
    lines.extend(["## Post-Decision Route Matrix", ""])
    for route in manifest["post_decision_route_matrix"]:
        lines.extend(
            [
                f"### {route['decision']}",
                f"- next_lane_after_record: `{route['next_lane_after_record']}`",
                f"- next_protocol: `{route['next_protocol']}`",
                f"- requires_new_protocol_contract: `{route['requires_new_protocol_contract']}`",
                f"- allows_local_training_now: `{route['allows_local_training_now']}`",
                f"- allows_remote_preflight_now: `{route['allows_remote_preflight_now']}`",
                f"- allows_remote_training_now: `{route['allows_remote_training_now']}`",
                f"- allows_formal_claim_now: `{route['allows_formal_claim_now']}`",
                f"- required_next_artifacts: `{', '.join(route['required_next_artifacts'])}`",
                f"- claim_boundary: {route['claim_boundary']}",
                "",
            ]
        )
    lines.extend(["## Invalid Inputs", ""])
    for invalid in manifest["invalid_inputs"]:
        lines.append(f"- `{invalid['input']}`: {invalid['why_invalid']}")
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
