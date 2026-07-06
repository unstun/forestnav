from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_post_decision_contract_plan")
DEFAULT_PROTOCOL_LANE_READINESS = Path(
    "0_trials/module2_formal_gate_protocol_lane_readiness/protocol_lane_readiness.json"
)
DEFAULT_DECISION_RECORD = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json"
)
DEFAULT_CONTRACT_INTAKE = Path("0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json")
DEFAULT_CONTRACT_AUTHORING_GATE = Path(
    "0_trials/module2_formal_gate_contract_authoring_gate_audit/contract_authoring_gate_audit.json"
)
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)
EXPECTED_LANE_IDS = (
    "stronger_obstacle_summary_warm_start",
    "full_patch_cnn_policy",
    "hybrid_ppo_analytic_fallback",
    "stop_or_reframe_module2_claim",
)
EXPECTED_REQUIRED_CONTRACT_SECTIONS = (
    "protocol_lane",
    "hypothesis",
    "success_signal",
    "failure_signal",
    "protocol_delta_from_failed_run",
    "training_budget_and_seed_policy",
    "evaluation_and_acceptance_plan",
    "paper_claim_boundary",
)
EXPECTED_SUCCESS_ARTIFACT_COUNT = 10
EXPECTED_SUCCESS_ARTIFACT_CATEGORY_COUNTS = {
    "contract": 1,
    "training": 3,
    "evaluation": 2,
    "acceptance": 3,
    "formal_acceptance": 1,
}
BLOCKED_ACTIONS = (
    "local_training",
    "remote_success_training",
    "remote_preflight_for_new_success_attempt",
    "formal_claim",
    "paper_result_material",
)
PENDING_DECISION_STATUS = "pending_protocol_lane_decision"
RECORDED_DECISION_STATUS = "protocol_lane_decision_recorded"
PENDING_CONTRACT_AUTHORING_STATUS = "contract_authoring_gate_blocked_pending_lane_decision"
READY_CONTRACT_AUTHORING_STATUS = "contract_authoring_gate_ready_for_contract_draft"
BOOTSTRAP_CONTRACT_AUTHORING_STATUS = "contract_authoring_gate_audit_failed"
BOOTSTRAP_CONTRACT_AUTHORING_ISSUE = "post_decision_contract_plan_missing_selected_lane_after_record"


@dataclass(frozen=True)
class FormalGatePostDecisionContractPlanConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    protocol_lane_readiness_path: Path = DEFAULT_PROTOCOL_LANE_READINESS
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    contract_intake_path: Path = DEFAULT_CONTRACT_INTAKE
    contract_authoring_gate_path: Path = DEFAULT_CONTRACT_AUTHORING_GATE
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGatePostDecisionContractPlanConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        protocol_lane_readiness_path=args.protocol_lane_readiness,
        decision_record_path=args.decision_record,
        contract_intake_path=args.contract_intake,
        contract_authoring_gate_path=args.contract_authoring_gate,
        next_round_requirements_path=args.next_round_requirements,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "post_decision_contract_plan.json"
    markdown_out = config.markdown_out or output_dir / "post_decision_contract_plan.md"
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


def build_manifest(config: FormalGatePostDecisionContractPlanConfig) -> dict[str, Any]:
    readiness = _read_json(config.protocol_lane_readiness_path)
    decision_record = _read_json(config.decision_record_path)
    contract_intake = _read_json(config.contract_intake_path)
    contract_authoring_gate = _read_json(config.contract_authoring_gate_path)
    next_round = _read_json(config.next_round_requirements_path)

    required_sections = _required_contract_sections(contract_intake)
    shared_artifacts = _shared_next_success_artifacts(readiness, next_round)
    next_round_summary = _next_round_summary(next_round=next_round, shared_artifacts=shared_artifacts)
    gate = _gate_state(
        readiness=readiness,
        decision_record=decision_record,
        contract_authoring_gate=contract_authoring_gate,
        next_round=next_round,
    )
    lane_rows = _lane_contract_rows(
        readiness=readiness,
        required_sections=required_sections,
        shared_artifacts=shared_artifacts,
    )
    issues = _audit_issues(
        readiness=readiness,
        decision_record=decision_record,
        contract_intake=contract_intake,
        contract_authoring_gate=contract_authoring_gate,
        next_round=next_round,
        gate=gate,
        required_sections=required_sections,
        lane_rows=lane_rows,
        shared_artifacts=shared_artifacts,
        next_round_summary=next_round_summary,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_post_decision_contract_plan",
        "status": _status(issues=issues, gate=gate),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "writes_contract": False,
        "approves_contract": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "inputs": {
            "protocol_lane_readiness": str(config.protocol_lane_readiness_path),
            "decision_record": str(config.decision_record_path),
            "contract_intake": str(config.contract_intake_path),
            "contract_authoring_gate": str(config.contract_authoring_gate_path),
            "next_round_requirements": str(config.next_round_requirements_path),
        },
        "gate_state": gate,
        "required_contract_section_count": len(required_sections),
        "required_contract_sections": required_sections,
        "shared_next_success_attempt_artifact_count": len(shared_artifacts),
        "shared_next_success_attempt_artifact_category_counts": next_round_summary[
            "next_success_attempt_artifact_category_counts"
        ],
        "old_failed_run_artifacts_invalid_for_next_success_attempt": next_round_summary[
            "old_failed_run_artifacts_invalid_for_next_success_attempt"
        ],
        "shared_next_success_attempt_artifacts": shared_artifacts,
        "lane_count": len(lane_rows),
        "lane_contract_plans": lane_rows,
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This artifact is a post-decision contract planning index, not a contract draft.",
            "It does not select a protocol lane and does not authorize contract authoring while selected_lane_id is None.",
            "It does not authorize local training, remote preflight, remote training, formal claims, or paper result material.",
            "Any success lane still needs a selected lane, an approved/frozen new or revised contract, remote training artifacts, formal Gate3 pass, checkpoint hash, and H02 acceptance.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 post-decision contract planning index.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--protocol-lane-readiness", type=Path, default=DEFAULT_PROTOCOL_LANE_READINESS)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--contract-intake", type=Path, default=DEFAULT_CONTRACT_INTAKE)
    parser.add_argument("--contract-authoring-gate", type=Path, default=DEFAULT_CONTRACT_AUTHORING_GATE)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _gate_state(
    *,
    readiness: dict[str, Any],
    decision_record: dict[str, Any],
    contract_authoring_gate: dict[str, Any],
    next_round: dict[str, Any],
) -> dict[str, Any]:
    readiness_gate = readiness.get("gate_state") if isinstance(readiness.get("gate_state"), dict) else {}
    contract_gate = (
        contract_authoring_gate.get("contract_gate")
        if isinstance(contract_authoring_gate.get("contract_gate"), dict)
        else {}
    )
    permissions = next_round.get("permissions_now") if isinstance(next_round.get("permissions_now"), dict) else {}
    decision_record_status = decision_record.get("status") or contract_gate.get("decision_record_status")
    decision_recorded = decision_record_status == RECORDED_DECISION_STATUS
    selected_lane_id = decision_record.get("selected_lane_id") if decision_recorded else readiness_gate.get("selected_lane_id")
    allowed_next_action_ids = (
        ["draft_new_or_revised_contract_after_lane_decision"]
        if decision_recorded
        else _strings(readiness_gate.get("next_action_ids"))
    )
    return {
        "next_blocked_lane": "new_or_revised_contract" if decision_recorded else readiness_gate.get("next_blocked_lane"),
        "selected_lane_id": selected_lane_id,
        "decision_owner_required": readiness_gate.get("decision_owner_required"),
        "decision_record_status": decision_record_status,
        "contract_action": decision_record.get("contract_action") or contract_gate.get("contract_action"),
        "contract_authoring_gate_status": contract_authoring_gate.get("status"),
        "contract_drafting_allowed_now": bool(
            decision_recorded or contract_gate.get("contract_drafting_allowed_now")
        ),
        "contract_approval_allowed_now": bool(contract_gate.get("contract_approval_allowed_now")),
        "draft_contract_allows_training": bool(contract_gate.get("draft_contract_allows_training")),
        "new_or_revised_contract_required_before_training": permissions.get(
            "new_or_revised_contract_required_before_new_success_training"
        )
        is True,
        "local_training_allowed_now": _truthy_any(
            readiness.get("local_training_allowed"),
            readiness_gate.get("local_training_allowed_now"),
            permissions.get("local_training_allowed_now"),
        ),
        "remote_preflight_allowed_now": _truthy_any(
            readiness.get("runs_remote_preflight"),
            permissions.get("remote_preflight_allowed_now"),
        ),
        "remote_training_allowed_now": _truthy_any(
            readiness.get("remote_training_allowed_now"),
            readiness_gate.get("remote_training_allowed_now"),
            permissions.get("remote_training_allowed_now_for_existing_packet"),
        ),
        "formal_claim_allowed_now": _truthy_any(
            readiness.get("formal_claim_allowed"),
            readiness_gate.get("formal_claim_allowed_now"),
            permissions.get("formal_claim_allowed_now"),
        ),
        "paper_result_material_allowed_now": _truthy_any(
            readiness.get("paper_result_material_allowed"),
            readiness_gate.get("paper_result_material_allowed_now"),
        ),
        "allowed_next_action_ids": allowed_next_action_ids,
        "blocked_action_ids": _strings(readiness_gate.get("blocked_action_ids")),
        "post_decision_plan_authorizes_lane_selection": False,
        "post_decision_plan_authorizes_contract_write": False,
        "post_decision_plan_authorizes_training": False,
    }


def _required_contract_sections(contract_intake: dict[str, Any]) -> list[dict[str, Any]]:
    requirements = (
        contract_intake.get("contract_output_requirements")
        if isinstance(contract_intake.get("contract_output_requirements"), dict)
        else {}
    )
    section_ids = _strings(requirements.get("required_sections")) or list(EXPECTED_REQUIRED_CONTRACT_SECTIONS)
    fields = {
        str(row.get("field")): row
        for row in contract_intake.get("decision_fields_required_for_contract", [])
        if isinstance(row, dict) and row.get("field")
    }
    rows: list[dict[str, Any]] = []
    for section_id in section_ids:
        field = fields.get(section_id, {})
        rows.append(
            {
                "section_id": section_id,
                "status_before_lane_decision": field.get("status") or "awaiting_dr_sun_decision",
                "prompt": field.get("prompt") or _default_section_prompt(section_id),
                "must_be_locked_before_training": True,
            }
        )
    return rows


def _lane_contract_rows(
    *,
    readiness: dict[str, Any],
    required_sections: Sequence[dict[str, Any]],
    shared_artifacts: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    readiness_rows = {
        str(row.get("lane_id")): row
        for row in readiness.get("lane_readiness_rows", [])
        if isinstance(row, dict) and row.get("lane_id")
    }
    shared_ids = [str(row.get("artifact_id")) for row in shared_artifacts if row.get("artifact_id")]
    rows: list[dict[str, Any]] = []
    for lane_id in EXPECTED_LANE_IDS:
        lane = readiness_rows.get(lane_id, {})
        stop_lane = lane_id == "stop_or_reframe_module2_claim"
        section_plan = [
            _section_plan(
                section=row,
                lane=lane,
                lane_id=lane_id,
                stop_lane=stop_lane,
            )
            for row in required_sections
        ]
        rows.append(
            {
                "lane_id": lane_id,
                "present_in_readiness": bool(lane),
                "claim_scope": lane.get("claim_scope"),
                "decision_required_before_use": True,
                "agent_may_select_lane_now": False,
                "contract_write_allowed_now": False,
                "contract_approval_allowed_now": False,
                "remote_training_allowed_now": False,
                "post_decision_contract_action": lane.get("next_action_after_selection"),
                "expected_contract_path_template": f".pipeline/contracts/module2-{lane_id}-v2.md",
                "new_success_training_required_if_selected": bool(
                    lane.get("new_success_training_required_if_selected")
                ),
                "section_plan": section_plan,
                "required_decision_justification": _strings(lane.get("required_decision_justification")),
                "required_contract_deltas": _strings(lane.get("required_contract_deltas")),
                "required_training_evidence": _strings(lane.get("required_training_evidence")),
                "required_evaluation_evidence": _strings(lane.get("required_evaluation_evidence")),
                "required_acceptance_evidence": _strings(lane.get("required_acceptance_evidence")),
                "invalid_substitutes": _strings(lane.get("invalid_substitutes")),
                "next_success_attempt_artifact_ids": [] if stop_lane else shared_ids,
            }
        )
    return rows


def _section_plan(
    *,
    section: dict[str, Any],
    lane: dict[str, Any],
    lane_id: str,
    stop_lane: bool,
) -> dict[str, Any]:
    section_id = str(section.get("section_id") or "")
    return {
        "section_id": section_id,
        "status_before_lane_decision": section.get("status_before_lane_decision"),
        "prompt": _lane_section_prompt(section_id=section_id, lane=lane, lane_id=lane_id, stop_lane=stop_lane),
        "must_be_locked_before_training": True,
        "must_reference_failed_gate3": section_id
        in {"protocol_lane", "failure_signal", "protocol_delta_from_failed_run", "paper_claim_boundary"},
    }


def _shared_next_success_artifacts(
    readiness: dict[str, Any],
    next_round: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = readiness.get("shared_next_success_attempt_artifacts")
    if not isinstance(rows, list) or not rows:
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


def _next_round_summary(*, next_round: dict[str, Any], shared_artifacts: Sequence[dict[str, Any]]) -> dict[str, Any]:
    protocol_summary = (
        next_round.get("protocol_gate_summary")
        if isinstance(next_round.get("protocol_gate_summary"), dict)
        else {}
    )
    reconciliation = (
        next_round.get("current_vs_next_attempt_reconciliation")
        if isinstance(next_round.get("current_vs_next_attempt_reconciliation"), dict)
        else {}
    )
    category_counts = protocol_summary.get("next_success_attempt_artifact_category_counts")
    if not isinstance(category_counts, dict):
        category_counts = _artifact_category_counts(shared_artifacts)
    return {
        "next_success_attempt_artifact_count": protocol_summary.get(
            "next_success_attempt_artifact_count",
            len(shared_artifacts),
        ),
        "next_success_attempt_artifact_category_counts": {
            str(category): int(count) for category, count in category_counts.items()
        },
        "old_failed_run_artifacts_invalid_for_next_success_attempt": reconciliation.get(
            "old_failed_run_artifacts_invalid_for_next_success_attempt"
        ),
    }


def _artifact_category_counts(shared_artifacts: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts = {category: 0 for category in EXPECTED_SUCCESS_ARTIFACT_CATEGORY_COUNTS}
    for artifact in shared_artifacts:
        category = str(artifact.get("category") or "")
        if category:
            counts[category] = counts.get(category, 0) + 1
    return counts


def _status(*, issues: Sequence[dict[str, Any]], gate: dict[str, Any]) -> str:
    if issues:
        return "post_decision_contract_plan_audit_failed"
    if gate["next_blocked_lane"] == "protocol_lane_decision" and gate["selected_lane_id"] is None:
        return "post_decision_contract_plan_ready_blocked_pending_lane_decision"
    if gate["contract_drafting_allowed_now"]:
        return "post_decision_contract_plan_ready_for_contract_draft"
    return "post_decision_contract_plan_blocked_unknown"


def _audit_issues(
    *,
    readiness: dict[str, Any],
    contract_intake: dict[str, Any],
    contract_authoring_gate: dict[str, Any],
    next_round: dict[str, Any],
    gate: dict[str, Any],
    required_sections: Sequence[dict[str, Any]],
    lane_rows: Sequence[dict[str, Any]],
    shared_artifacts: Sequence[dict[str, Any]],
    next_round_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if readiness.get("status") != "protocol_lane_readiness_ready_for_dr_sun_decision":
        issues.append(_issue("readiness_not_ready", "Protocol-lane readiness must be ready for Dr Sun decision."))
    if readiness.get("audit_issue_count") != 0:
        issues.append(_issue("readiness_audit_issues_open", "Protocol-lane readiness must be audit-clean."))
    if contract_intake.get("status") != "formal_gate_contract_intake_ready_for_dr_sun":
        issues.append(_issue("contract_intake_not_ready", "Contract intake must be ready before post-decision planning."))
    if contract_authoring_gate.get("status") != "contract_authoring_gate_blocked_pending_lane_decision":
        issues.append(
            _issue(
                "contract_authoring_gate_not_pending",
                "This plan mirrors the pending-lane state and must not pretend contract drafting is open.",
                observed=contract_authoring_gate.get("status"),
            )
        )
    if next_round.get("status") != "formal_gate_next_round_requirements_ready":
        issues.append(_issue("next_round_requirements_not_ready", "Next-round requirements must be ready."))
    if gate["selected_lane_id"] is not None:
        issues.append(_issue("selected_lane_present", "Pending contract plan must not select a lane."))
    if gate["allowed_next_action_ids"] != ["record_protocol_lane_decision"]:
        issues.append(
            _issue(
                "allowed_next_actions_drift",
                "Pending state may only allow record_protocol_lane_decision.",
                observed=gate["allowed_next_action_ids"],
            )
        )
    missing_blocked = [action for action in BLOCKED_ACTIONS if action not in gate["blocked_action_ids"]]
    if missing_blocked:
        issues.append(_issue("blocked_actions_incomplete", "Training, preflight, claim, and paper actions must stay blocked.", observed=missing_blocked))
    for key in (
        "contract_drafting_allowed_now",
        "contract_approval_allowed_now",
        "draft_contract_allows_training",
        "local_training_allowed_now",
        "remote_preflight_allowed_now",
        "remote_training_allowed_now",
        "formal_claim_allowed_now",
        "paper_result_material_allowed_now",
        "post_decision_plan_authorizes_lane_selection",
        "post_decision_plan_authorizes_contract_write",
        "post_decision_plan_authorizes_training",
    ):
        if gate[key] is True:
            issues.append(_issue(f"{key}_unexpectedly_true", f"{key} must remain false."))
    section_ids = {str(row.get("section_id")) for row in required_sections}
    for section_id in EXPECTED_REQUIRED_CONTRACT_SECTIONS:
        if section_id not in section_ids:
            issues.append(_issue(f"required_contract_section_missing_{section_id}", "Required contract section missing."))
    if len(lane_rows) != len(EXPECTED_LANE_IDS):
        issues.append(_issue("lane_count_invalid", "Plan must cover all four protocol lanes."))
    if len(shared_artifacts) != EXPECTED_SUCCESS_ARTIFACT_COUNT:
        issues.append(
            _issue(
                "shared_artifact_count_invalid",
                "Success-lane artifact index must retain all 10 next-attempt artifacts.",
                observed=len(shared_artifacts),
            )
        )
    if next_round_summary["next_success_attempt_artifact_category_counts"] != EXPECTED_SUCCESS_ARTIFACT_CATEGORY_COUNTS:
        issues.append(
            _issue(
                "shared_artifact_category_counts_invalid",
                "Success-lane artifact category counts must remain contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1.",
                observed=next_round_summary["next_success_attempt_artifact_category_counts"],
            )
        )
    if next_round_summary["old_failed_run_artifacts_invalid_for_next_success_attempt"] is not True:
        issues.append(
            _issue(
                "old_failed_run_artifacts_not_marked_invalid",
                "Post-decision contract plan must preserve that old failed-run artifacts are invalid for the next success attempt.",
                observed=next_round_summary["old_failed_run_artifacts_invalid_for_next_success_attempt"],
            )
        )
    for row in lane_rows:
        lane_id = str(row.get("lane_id"))
        stop_lane = lane_id == "stop_or_reframe_module2_claim"
        if row.get("present_in_readiness") is not True:
            issues.append(_issue(f"{lane_id}_missing_from_readiness", "Lane must be present in readiness packet."))
        for key in ("agent_may_select_lane_now", "contract_write_allowed_now", "remote_training_allowed_now"):
            if row.get(key) is True:
                issues.append(_issue(f"{lane_id}_{key}_leak", "Lane plan must not authorize selection, contract write, or training."))
        if len(row.get("section_plan", [])) != len(required_sections):
            issues.append(_issue(f"{lane_id}_section_plan_count_mismatch", "Lane must include every required contract section."))
        if not row.get("required_decision_justification"):
            issues.append(_issue(f"{lane_id}_missing_decision_justification", "Lane must retain decision justification prompts."))
        if not row.get("invalid_substitutes"):
            issues.append(_issue(f"{lane_id}_missing_invalid_substitutes", "Lane must retain invalid substitutes."))
        if stop_lane:
            if row.get("next_success_attempt_artifact_ids"):
                issues.append(_issue(f"{lane_id}_should_not_carry_success_artifacts", "Stop/reframe lane must not imply a success training attempt."))
        else:
            if len(row.get("next_success_attempt_artifact_ids", [])) != EXPECTED_SUCCESS_ARTIFACT_COUNT:
                issues.append(_issue(f"{lane_id}_missing_next_success_artifacts", "Success lane must carry the 10-artifact next-attempt index."))
            for key in ("required_training_evidence", "required_evaluation_evidence", "required_acceptance_evidence"):
                if not row.get(key):
                    issues.append(_issue(f"{lane_id}_{key}_missing", "Success lane must retain training/evaluation/acceptance evidence prompts."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    gate = manifest["gate_state"]
    lines = [
        "# Module2 Post-Decision Contract Plan",
        "",
        "This file is a read-only planning index. It is not a contract draft, training run, remote preflight, formal evaluation, or paper result.",
        "",
        "## Gate State",
        "",
        f"- status: `{manifest['status']}`",
        f"- next_blocked_lane: `{gate['next_blocked_lane']}`",
        f"- selected_lane_id: `{gate['selected_lane_id']}`",
        f"- decision_owner_required: `{gate['decision_owner_required']}`",
        f"- allowed_next_action_ids: `{gate['allowed_next_action_ids']}`",
        f"- contract_drafting_allowed_now: `{gate['contract_drafting_allowed_now']}`",
        f"- remote_training_allowed_now: `{gate['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{gate['formal_claim_allowed_now']}`",
        "",
        "## Required Contract Sections",
        "",
    ]
    for section in manifest["required_contract_sections"]:
        lines.append(
            f"- `{section['section_id']}`: status=`{section['status_before_lane_decision']}`, "
            f"must_lock_before_training=`{section['must_be_locked_before_training']}`"
        )
    lines.extend(["", "## Lane Contract Plans", ""])
    for lane in manifest["lane_contract_plans"]:
        lines.extend(
            [
                f"### {lane['lane_id']}",
                "",
                f"- expected_contract_path_template: `{lane['expected_contract_path_template']}`",
                f"- new_success_training_required_if_selected: `{lane['new_success_training_required_if_selected']}`",
                f"- contract_write_allowed_now: `{lane['contract_write_allowed_now']}`",
                f"- remote_training_allowed_now: `{lane['remote_training_allowed_now']}`",
                f"- next_success_attempt_artifact_ids: `{lane['next_success_attempt_artifact_ids']}`",
                "- required_contract_deltas:",
            ]
        )
        lines.extend(f"  - {item}" for item in lane["required_contract_deltas"])
        lines.append("- invalid_substitutes:")
        lines.extend(f"  - {item}" for item in lane["invalid_substitutes"])
        lines.append("")
    lines.extend(["## Shared Next Success Attempt Artifacts", ""])
    lines.append(
        "- shared_next_success_attempt_artifact_category_counts: "
        f"`{manifest['shared_next_success_attempt_artifact_category_counts']}`"
    )
    lines.append(
        "- old_failed_run_artifacts_invalid_for_next_success_attempt: "
        f"`{manifest['old_failed_run_artifacts_invalid_for_next_success_attempt']}`"
    )
    for artifact in manifest["shared_next_success_attempt_artifacts"]:
        lines.append(
            f"- `{artifact['artifact_id']}` ({artifact['category']}): "
            f"status=`{artifact['status']}`, blocked_until=`{artifact['blocked_until']}`"
        )
    lines.extend(["", "## Audit", "", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- no audit issues")
    lines.extend(["", "## Claim Boundaries"])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _lane_section_prompt(*, section_id: str, lane: dict[str, Any], lane_id: str, stop_lane: bool) -> str:
    if section_id == "protocol_lane":
        return f"Lock selected protocol lane as {lane_id} and cite the failed Gate3 0.53125 vs 0.8 basis."
    if section_id == "hypothesis":
        return str(lane.get("claim_scope") or "Lock the lane-specific hypothesis before training.")
    if section_id == "success_signal":
        if stop_lane:
            return "No new success signal; define the negative/reframe evidence scope."
        return "Define the lane-specific formal Gate3 and H02 acceptance signal before training."
    if section_id == "failure_signal":
        return "Define lane-specific independent failure criteria before observing any new run."
    if section_id == "protocol_delta_from_failed_run":
        deltas = _strings(lane.get("required_contract_deltas"))
        return "; ".join(deltas) if deltas else "List every protocol delta from the failed warm-start Gate3 run."
    if section_id == "training_budget_and_seed_policy":
        if stop_lane:
            return "State that no new success-attempt training is planned under this lane."
        return "Lock remote-only budget, seed policy, checkpoint path, manifest, and hash requirements."
    if section_id == "evaluation_and_acceptance_plan":
        return "Lock formal Gate3 eval, audit, checkpoint hash, and H02 acceptance requirements."
    if section_id == "paper_claim_boundary":
        return "State exactly which paper claim is allowed and which success wording remains blocked."
    return _default_section_prompt(section_id)


def _default_section_prompt(section_id: str) -> str:
    return f"Lock {section_id} before any new success-attempt training."


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    payload = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


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
