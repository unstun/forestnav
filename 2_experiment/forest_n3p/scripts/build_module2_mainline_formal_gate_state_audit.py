from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_mainline_formal_gate_state_audit")
DEFAULT_MAINLINE = Path(".pipeline/mainline_module2_rl_rs_replacement.md")
DEFAULT_FORMAL_GATE_STATUS_REPORT = Path(
    "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json"
)
DEFAULT_PROOF_SUMMARY_CHAIN_AUDIT = Path(
    "0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json"
)
DEFAULT_PROTOCOL_LANE_STATUS_REPORT = Path(
    "0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json"
)
DEFAULT_PROTOCOL_LANE_READINESS = Path(
    "0_trials/module2_formal_gate_protocol_lane_readiness/protocol_lane_readiness.json"
)
DEFAULT_POST_DECISION_CONTRACT_PLAN = Path(
    "0_trials/module2_formal_gate_post_decision_contract_plan/post_decision_contract_plan.json"
)

CURRENT_STATE_MARKER = "当前 formal gate 下一步清单已同步到主任务书"
EXPECTED_DECISION_EVIDENCE_MATRIX_ID = "module2_f02_6_decision_evidence_matrix"
EXPECTED_DECISION_EVIDENCE_MATRIX_STATUS = "ready_for_dr_sun_decision_not_authorization"
EXPECTED_DECISION_EVIDENCE_MATRIX_ROUTES = (
    "approve_obstacle_summary_warm_start",
    "reject_obstacle_summary_warm_start",
)
MIN_REQUIRED_DECISION_EVIDENCE_ROWS = 7
MIN_GLOBAL_INVALID_SUBSTITUTE_ROWS = 4
REQUIRED_CURRENT_BOUNDARY_TOKENS = (
    "local training",
    "remote preflight",
    "remote training",
    "formal claim",
    "paper-result material",
    "gpu3070ti-relay",
)
FORBIDDEN_CURRENT_ALLOWED_TOKENS = (
    "local_training_allowed=true",
    "remote_preflight_allowed=true",
    "remote_training_allowed=true",
    "formal_claim_allowed=true",
    "paper_result_material_allowed=true",
    "formal_result_material_allowed=true",
)
DECISION_EVIDENCE_MATRIX_ALLOWED_KEYS = (
    "current_authorization_allowed_now",
    "remote_preflight_allowed_now",
    "remote_training_allowed_now",
    "local_training_allowed_now",
    "formal_claim_allowed_now",
    "paper_result_material_allowed_now",
)
EXPECTED_PROTOCOL_LANE_STATUS = "protocol_lane_status_blocked_pending_lane_decision"
EXPECTED_PROTOCOL_LANE_RECORDED_STATUS = "protocol_lane_status_ready_for_contract_draft"
EXPECTED_PROTOCOL_LANE_NEXT_BLOCKED = "protocol_lane_decision"
EXPECTED_PROTOCOL_LANE_RECORDED_NEXT_BLOCKED = "new_or_revised_contract"
EXPECTED_PROTOCOL_LANE_DECISION_RECORD_STATUS = "pending_protocol_lane_decision"
EXPECTED_PROTOCOL_LANE_RECORDED_DECISION_RECORD_STATUS = "protocol_lane_decision_recorded"
EXPECTED_PROTOCOL_LANE_ALLOWED_NEXT_ACTIONS = ("record_protocol_lane_decision",)
EXPECTED_PROTOCOL_LANE_RECORDED_ALLOWED_NEXT_ACTIONS = ("draft_new_or_revised_contract_after_lane_decision",)
EXPECTED_PROTOCOL_LANE_IDS = (
    "stronger_obstacle_summary_warm_start",
    "full_patch_cnn_policy",
    "hybrid_ppo_analytic_fallback",
    "stop_or_reframe_module2_claim",
)
EXPECTED_PROTOCOL_LANE_BLOCKED_ACTIONS = (
    "local_training",
    "remote_success_training",
    "remote_preflight_for_new_success_attempt",
    "formal_claim",
    "paper_result_material",
)
EXPECTED_PROTOCOL_LANE_READINESS_STATUS = "protocol_lane_readiness_ready_for_dr_sun_decision"
EXPECTED_PROTOCOL_LANE_READINESS_ARTIFACT = "module2_formal_gate_protocol_lane_readiness"
EXPECTED_PROTOCOL_LANE_READINESS_SHARED_ARTIFACT_COUNT = 10
EXPECTED_POST_DECISION_CONTRACT_PLAN_STATUS = "post_decision_contract_plan_ready_blocked_pending_lane_decision"
EXPECTED_POST_DECISION_CONTRACT_PLAN_RECORDED_STATUS = "post_decision_contract_plan_ready_for_contract_draft"
EXPECTED_POST_DECISION_CONTRACT_PLAN_ARTIFACT = "module2_formal_gate_post_decision_contract_plan"
EXPECTED_POST_DECISION_CONTRACT_SECTION_COUNT = 8
EXPECTED_POST_DECISION_CONTRACT_LANE_COUNT = 4
EXPECTED_POST_DECISION_CONTRACT_SHARED_ARTIFACT_COUNT = 10
EXPECTED_NEXT_SUCCESS_ARTIFACT_CATEGORY_COUNTS = {
    "contract": 1,
    "training": 3,
    "evaluation": 2,
    "acceptance": 3,
    "formal_acceptance": 1,
}
EXPECTED_OLD_FAILED_RUN_INVALID_FOR_NEXT_SUCCESS_ATTEMPT = True
EXPECTED_NEXT_SUCCESS_ARTIFACT_IDS_BY_CATEGORY = {
    "contract": ("new_or_revised_research_contract",),
    "training": ("train_final_model_zip", "train_summary_json", "train_training_manifest_json"),
    "evaluation": ("eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"),
    "acceptance": (
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
    ),
    "formal_acceptance": ("h02_formal_output_acceptance",),
}
PROTOCOL_LANE_FALSE_FLAGS = (
    "contract_approval_allowed_now",
    "draft_contract_allows_training",
    "local_training_allowed_now",
    "remote_training_allowed_now",
    "formal_claim_allowed_now",
    "paper_result_material_allowed_now",
    "new_success_training_allowed_now",
)


@dataclass(frozen=True)
class MainlineFormalGateStateAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    mainline_path: Path = DEFAULT_MAINLINE
    formal_gate_status_report_path: Path = DEFAULT_FORMAL_GATE_STATUS_REPORT
    proof_summary_chain_audit_path: Path = DEFAULT_PROOF_SUMMARY_CHAIN_AUDIT
    protocol_lane_status_report_path: Path = DEFAULT_PROTOCOL_LANE_STATUS_REPORT
    protocol_lane_readiness_path: Path = DEFAULT_PROTOCOL_LANE_READINESS
    post_decision_contract_plan_path: Path = DEFAULT_POST_DECISION_CONTRACT_PLAN


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = MainlineFormalGateStateAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        mainline_path=args.mainline,
        formal_gate_status_report_path=args.formal_gate_status_report,
        proof_summary_chain_audit_path=args.proof_summary_chain_audit,
        protocol_lane_status_report_path=args.protocol_lane_status_report,
        protocol_lane_readiness_path=args.protocol_lane_readiness,
        post_decision_contract_plan_path=args.post_decision_contract_plan,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "mainline_formal_gate_state_audit.json"
    markdown_out = config.markdown_out or output_dir / "mainline_formal_gate_state_audit.md"
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


def build_manifest(config: MainlineFormalGateStateAuditConfig) -> dict[str, Any]:
    mainline_text = Path(config.mainline_path).read_text(encoding="utf-8")
    status_report = _read_json(config.formal_gate_status_report_path)
    proof_chain = _read_json(config.proof_summary_chain_audit_path)
    protocol_lane_status = _normalize_protocol_lane_status_report(
        _read_json(config.protocol_lane_status_report_path)
    )
    protocol_lane_readiness = _normalize_protocol_lane_readiness(
        _read_json(config.protocol_lane_readiness_path)
    )
    post_decision_contract_plan = _normalize_post_decision_contract_plan(
        _read_json(config.post_decision_contract_plan_path)
    )
    next_action_guard = _normalize_next_action_guard(status_report.get("next_action_guard_summary"))
    next_required = _normalize_next_required_deliverables(status_report.get("next_required_formal_deliverables"))
    decision_matrix = _normalize_decision_evidence_matrix_summary(
        status_report.get("f02_6_decision_evidence_matrix_summary")
    )
    current_section = _current_section(mainline_text)
    deliverable_rows = _deliverable_rows(next_required, mainline_text=mainline_text, current_section=current_section)
    issues = (
        _mainline_issues(
            mainline_text=mainline_text,
            current_section=current_section,
            next_action_guard=next_action_guard,
            next_required=next_required,
            decision_matrix=decision_matrix,
            protocol_lane_status=protocol_lane_status,
            protocol_lane_readiness=protocol_lane_readiness,
            post_decision_contract_plan=post_decision_contract_plan,
            deliverable_rows=deliverable_rows,
            proof_chain=proof_chain,
        )
        + _status_report_issues(next_action_guard=next_action_guard, next_required=next_required)
        + _decision_evidence_matrix_issues(decision_matrix)
        + _protocol_lane_status_issues(protocol_lane_status)
        + _protocol_lane_readiness_issues(protocol_lane_readiness)
        + _post_decision_contract_plan_issues(post_decision_contract_plan)
        + _proof_chain_issues(proof_chain)
    )
    issues = _unique_issues(issues)
    if issues:
        status = "mainline_formal_gate_state_audit_failed"
    elif status_report.get("status") == "formal_gate_status_blocked" or proof_chain.get("proof_open") is True:
        status = "mainline_formal_gate_state_consistent_blocked"
    else:
        status = "mainline_formal_gate_state_consistent_ready"

    expected_next_action_id = next_action_guard["expected_next_action_id"]
    expected_next_action_mentioned = (
        isinstance(expected_next_action_id, str) and expected_next_action_id in mainline_text
    )

    return {
        "schema_version": 1,
        "artifact_name": "module2_mainline_formal_gate_state_audit",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "mainline": str(config.mainline_path),
            "formal_gate_status_report": str(config.formal_gate_status_report_path),
            "proof_summary_chain_audit": str(config.proof_summary_chain_audit_path),
            "protocol_lane_status_report": str(config.protocol_lane_status_report_path),
            "protocol_lane_readiness": str(config.protocol_lane_readiness_path),
            "post_decision_contract_plan": str(config.post_decision_contract_plan_path),
        },
        "mainline_current_state_section_present": bool(current_section),
        "expected_next_action_id": expected_next_action_id,
        "expected_next_action_mentioned": expected_next_action_mentioned,
        "all_execution_disabled_now": next_action_guard["all_execution_disabled_now"],
        "execution_leak_count": next_action_guard["execution_leak_count"],
        "next_required_formal_deliverables_status": next_required["status"],
        "total_missing_deliverables": next_required["total_missing_deliverables"],
        "blocked_category_count": next_required["blocked_category_count"],
        "f02_6_decision_evidence_matrix_summary": decision_matrix,
        "f02_6_decision_evidence_matrix_mentioned": decision_matrix["matrix_id"] in current_section,
        "f02_6_decision_evidence_matrix_status_mentioned": decision_matrix["status"] in current_section,
        "f02_6_decision_evidence_matrix_route_mentions": [
            {"route_decision": route, "mentioned": route in current_section}
            for route in EXPECTED_DECISION_EVIDENCE_MATRIX_ROUTES
        ],
        "protocol_lane_status_summary": protocol_lane_status,
        "protocol_lane_status_mentioned": protocol_lane_status["status"] in current_section,
        "protocol_lane_next_blocked_mentioned": protocol_lane_status["next_blocked_lane"] in current_section,
        "protocol_lane_next_action_mentioned": all(
            action in current_section for action in protocol_lane_status["allowed_next_action_ids"]
        ),
        "protocol_lane_decision_record_status_mentioned": (
            protocol_lane_status["decision_record_status"] in current_section
        ),
        "protocol_lane_lane_mentions": [
            {"lane_id": lane_id, "mentioned": lane_id in current_section}
            for lane_id in EXPECTED_PROTOCOL_LANE_IDS
        ],
        "protocol_lane_blocked_action_mentions": [
            {"action_id": action_id, "mentioned": action_id in current_section}
            for action_id in EXPECTED_PROTOCOL_LANE_BLOCKED_ACTIONS
        ],
        "protocol_lane_status_post_plan_summary_mentioned": (
            "protocol_lane_status_report" in current_section
            and "post-decision contract plan summary" in current_section
            and str(protocol_lane_status["post_decision_contract_plan_required_section_count"])
            in current_section
            and str(protocol_lane_status["post_decision_contract_plan_shared_artifact_count"])
            in current_section
            and str(protocol_lane_status["post_decision_contract_plan_lane_count"]) in current_section
        ),
        "protocol_lane_status_next_artifact_category_counts_mentioned": (
            "contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1"
            in current_section
        ),
        "protocol_lane_status_old_failed_invalid_mentioned": (
            "protocol_lane_status_report" in current_section
            and "old_failed_run_artifacts_invalid_for_next_success_attempt=true" in current_section
        ),
        "protocol_lane_readiness_summary": protocol_lane_readiness,
        "protocol_lane_readiness_artifact_mentioned": protocol_lane_readiness["artifact_name"] in current_section,
        "protocol_lane_readiness_status_mentioned": protocol_lane_readiness["status"] in current_section,
        "protocol_lane_readiness_shared_artifact_count_mentioned": (
            protocol_lane_readiness["artifact_name"] in current_section
            and protocol_lane_readiness["status"] in current_section
            and str(protocol_lane_readiness["shared_next_success_attempt_artifact_count"]) in current_section
        ),
        "post_decision_contract_plan_summary": post_decision_contract_plan,
        "post_decision_contract_plan_artifact_mentioned": (
            post_decision_contract_plan["artifact_name"] in current_section
        ),
        "post_decision_contract_plan_status_mentioned": post_decision_contract_plan["status"] in current_section,
        "post_decision_contract_plan_required_section_count_mentioned": (
            post_decision_contract_plan["artifact_name"] in current_section
            and post_decision_contract_plan["status"] in current_section
            and str(post_decision_contract_plan["required_contract_section_count"]) in current_section
        ),
        "post_decision_contract_plan_shared_artifact_count_mentioned": (
            post_decision_contract_plan["artifact_name"] in current_section
            and post_decision_contract_plan["status"] in current_section
            and str(post_decision_contract_plan["shared_next_success_attempt_artifact_count"]) in current_section
        ),
        "post_decision_contract_plan_lane_count_mentioned": (
            post_decision_contract_plan["artifact_name"] in current_section
            and post_decision_contract_plan["status"] in current_section
            and str(post_decision_contract_plan["lane_count"]) in current_section
        ),
        "post_decision_contract_plan_old_failed_invalid_mentioned": (
            post_decision_contract_plan["artifact_name"] in current_section
            and "old_failed_run_artifacts_invalid_for_next_success_attempt=true" in current_section
        ),
        "mainline_missing_deliverable_mention_count": sum(1 for row in deliverable_rows if not row["mentioned"]),
        "deliverable_rows": deliverable_rows,
        "deliverable_rows_by_matrix_id": {row["matrix_id"]: row for row in deliverable_rows},
        "proof_summary_chain_status": proof_chain.get("status"),
        "proof_summary_chain_audit_issue_count": proof_chain.get("audit_issue_count"),
        "proof_summary_chain_proof_audit_input_safety_issue_count": proof_chain.get(
            "proof_audit_input_safety_issue_count"
        ),
        "proof_summary_chain_proof_audit_blockers": _strings(proof_chain.get("proof_audit_blockers")),
        "proof_summary_next_action_guard_consistency": {
            "row_count": proof_chain.get("next_action_guard_row_count"),
            "consistent_row_count": proof_chain.get("next_action_guard_consistent_row_count"),
        },
        "proof_summary_next_required_deliverables_consistency": {
            "row_count": proof_chain.get("next_required_deliverables_row_count"),
            "consistent_row_count": proof_chain.get("next_required_deliverables_consistent_row_count"),
        },
        "proof_summary_handoff_single_next_action_consistency": {
            "row_count": proof_chain.get("handoff_single_next_action_row_count"),
            "consistent_row_count": proof_chain.get("handoff_single_next_action_consistent_row_count"),
        },
        "current_boundary_tokens": [
            {"token": token, "mentioned": token in current_section} for token in REQUIRED_CURRENT_BOUNDARY_TOKENS
        ],
        "forbidden_current_allowed_tokens": [
            {"token": token, "mentioned": token in current_section}
            for token in FORBIDDEN_CURRENT_ALLOWED_TOKENS
        ],
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This audit only checks that the long-term mainline task book mirrors the current formal-gate state.",
            "It does not execute commands, run local training, run remote preflight, run remote PPO training, evaluate PPO, pull back artifacts, or write paper results.",
            "A consistent blocked audit does not prove PPO has replaced RS in formal evaluation.",
            "Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.",
            "Protocol-lane status must remain blocked on record_protocol_lane_decision before any new or revised contract can authorize future remote success attempts.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 mainline task-book formal-gate state.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--mainline", type=Path, default=DEFAULT_MAINLINE)
    parser.add_argument("--formal-gate-status-report", type=Path, default=DEFAULT_FORMAL_GATE_STATUS_REPORT)
    parser.add_argument("--proof-summary-chain-audit", type=Path, default=DEFAULT_PROOF_SUMMARY_CHAIN_AUDIT)
    parser.add_argument("--protocol-lane-status-report", type=Path, default=DEFAULT_PROTOCOL_LANE_STATUS_REPORT)
    parser.add_argument("--protocol-lane-readiness", type=Path, default=DEFAULT_PROTOCOL_LANE_READINESS)
    parser.add_argument("--post-decision-contract-plan", type=Path, default=DEFAULT_POST_DECISION_CONTRACT_PLAN)
    return parser.parse_args(list(argv) if argv is not None else None)


def _mainline_issues(
    *,
    mainline_text: str,
    current_section: str,
    next_action_guard: dict[str, Any],
    next_required: dict[str, Any],
    decision_matrix: dict[str, Any],
    protocol_lane_status: dict[str, Any],
    protocol_lane_readiness: dict[str, Any],
    post_decision_contract_plan: dict[str, Any],
    deliverable_rows: Sequence[dict[str, Any]],
    proof_chain: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not current_section:
        issues.append(
            {
                "issue_id": "mainline_current_formal_gate_section_missing",
                "message": "Mainline task book must include the current formal-gate state section.",
            }
        )
    expected_next_action = next_action_guard["expected_next_action_id"]
    if expected_next_action and expected_next_action not in mainline_text:
        issues.append(
            {
                "issue_id": "mainline_missing_expected_next_action",
                "message": "Mainline task book must mention the current expected next action.",
                "expected_next_action_id": expected_next_action,
            }
        )
    for row in deliverable_rows:
        if not row["mentioned"]:
            issues.append(
                {
                    "issue_id": f"mainline_missing_deliverable_{row['safe_matrix_id']}",
                    "message": "Mainline task book must mention every missing formal deliverable artifact id.",
                    "matrix_id": row["matrix_id"],
                    "artifact_id": row["artifact_id"],
                }
            )
    for token in REQUIRED_CURRENT_BOUNDARY_TOKENS:
        if token not in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_missing_boundary_{_safe_id(token)}",
                    "message": "Current formal-gate section must mention this blocked boundary.",
                    "token": token,
                }
            )
    for token in FORBIDDEN_CURRENT_ALLOWED_TOKENS:
        if token in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_forbidden_allowed_token_{_safe_id(token)}",
                    "message": "Current formal-gate section must not mark a blocked execution or claim surface as allowed.",
                    "token": token,
                }
            )
    if decision_matrix["matrix_id"] and decision_matrix["matrix_id"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_decision_evidence_matrix",
                "message": "Current formal-gate section must mention the F02.6 decision evidence matrix id.",
                "matrix_id": decision_matrix["matrix_id"],
            }
        )
    if decision_matrix["status"] and decision_matrix["status"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_decision_evidence_matrix_status",
                "message": "Current formal-gate section must mention that the F02.6 matrix is a decision aid, not authorization.",
                "matrix_status": decision_matrix["status"],
            }
        )
    for route_decision in EXPECTED_DECISION_EVIDENCE_MATRIX_ROUTES:
        if route_decision not in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_missing_decision_route_{_safe_id(route_decision)}",
                    "message": "Current formal-gate section must mention both F02.6 decision routes.",
                    "route_decision": route_decision,
                }
            )
    if "invalid substitutes" not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_invalid_substitutes_boundary",
                "message": "Current formal-gate section must mention invalid substitutes so the decision matrix is not treated as weak evidence.",
            }
        )
    if protocol_lane_status["status"] and protocol_lane_status["status"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_lane_status",
                "message": "Current formal-gate section must mention the protocol-lane status report state.",
                "protocol_lane_status": protocol_lane_status["status"],
            }
        )
    if protocol_lane_status["next_blocked_lane"] and protocol_lane_status["next_blocked_lane"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_lane_next_blocked",
                "message": "Current formal-gate section must mention protocol_lane_decision as the current blocked lane.",
                "next_blocked_lane": protocol_lane_status["next_blocked_lane"],
            }
        )
    for action_id in EXPECTED_PROTOCOL_LANE_ALLOWED_NEXT_ACTIONS:
        if action_id not in current_section:
            issues.append(
                {
                    "issue_id": "mainline_current_section_missing_protocol_lane_next_action",
                    "message": "Current formal-gate section must mention the only allowed protocol-lane next action.",
                    "action_id": action_id,
                }
            )
    if (
        protocol_lane_status["decision_record_status"]
        and protocol_lane_status["decision_record_status"] not in current_section
    ):
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_lane_decision_record_status",
                "message": "Current formal-gate section must mention the pending protocol-lane decision record.",
                "decision_record_status": protocol_lane_status["decision_record_status"],
            }
        )
    for lane_id in EXPECTED_PROTOCOL_LANE_IDS:
        if lane_id not in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_missing_protocol_lane_{_safe_id(lane_id)}",
                    "message": "Current formal-gate section must mention every protocol-lane option.",
                    "lane_id": lane_id,
                }
            )
    for action_id in EXPECTED_PROTOCOL_LANE_BLOCKED_ACTIONS:
        if action_id not in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_missing_protocol_lane_blocked_action_{_safe_id(action_id)}",
                    "message": "Current formal-gate section must mention every blocked protocol-lane action.",
                    "action_id": action_id,
                }
            )
    protocol_status_context_present = (
        "protocol_lane_status_report" in current_section
        and protocol_lane_status["status"] in current_section
    )
    for key, issue_id in (
        (
            "post_decision_contract_plan_required_section_count",
            "mainline_current_section_missing_protocol_status_post_plan_section_count",
        ),
        (
            "post_decision_contract_plan_shared_artifact_count",
            "mainline_current_section_missing_protocol_status_post_plan_artifact_count",
        ),
        (
            "post_decision_contract_plan_lane_count",
            "mainline_current_section_missing_protocol_status_post_plan_lane_count",
        ),
    ):
        token = str(protocol_lane_status[key])
        if token and (not protocol_status_context_present or token not in current_section):
            issues.append(
                {
                    "issue_id": issue_id,
                    "message": "Current formal-gate section must mention the protocol status report's inherited post-plan count.",
                    key: protocol_lane_status[key],
                }
            )
    if "contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1" not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_status_next_artifact_category_counts",
                "message": "Current formal-gate section must mention the protocol status report's next-attempt artifact category counts.",
                "expected_counts": EXPECTED_NEXT_SUCCESS_ARTIFACT_CATEGORY_COUNTS,
            }
        )
    if "old_failed_run_artifacts_invalid_for_next_success_attempt=true" not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_old_failed_invalid_boundary",
                "message": "Current formal-gate section must mention that old failed-run artifacts are invalid substitutes for the next success attempt.",
            }
        )
    if protocol_lane_readiness["artifact_name"] and protocol_lane_readiness["artifact_name"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_lane_readiness_artifact",
                "message": "Current formal-gate section must mention the protocol-lane readiness packet artifact name.",
                "artifact_name": protocol_lane_readiness["artifact_name"],
            }
        )
    if protocol_lane_readiness["status"] and protocol_lane_readiness["status"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_lane_readiness_status",
                "message": "Current formal-gate section must mention the readiness packet status.",
                "readiness_status": protocol_lane_readiness["status"],
            }
        )
    shared_count_token = str(protocol_lane_readiness["shared_next_success_attempt_artifact_count"])
    readiness_context_present = (
        protocol_lane_readiness["artifact_name"] in current_section
        and protocol_lane_readiness["status"] in current_section
    )
    if shared_count_token and (not readiness_context_present or shared_count_token not in current_section):
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_protocol_lane_readiness_shared_artifact_count",
                "message": "Current formal-gate section must mention the readiness packet shared artifact count.",
                "shared_next_success_attempt_artifact_count": protocol_lane_readiness[
                    "shared_next_success_attempt_artifact_count"
                ],
            }
        )
    if post_decision_contract_plan["artifact_name"] and post_decision_contract_plan["artifact_name"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_post_decision_contract_plan_artifact",
                "message": "Current formal-gate section must mention the post-decision contract plan artifact name.",
                "artifact_name": post_decision_contract_plan["artifact_name"],
            }
        )
    if post_decision_contract_plan["status"] and post_decision_contract_plan["status"] not in current_section:
        issues.append(
            {
                "issue_id": "mainline_current_section_missing_post_decision_contract_plan_status",
                "message": "Current formal-gate section must mention the post-decision contract plan status.",
                "plan_status": post_decision_contract_plan["status"],
            }
        )
    for key, issue_id in (
        ("required_contract_section_count", "mainline_current_section_missing_post_decision_contract_section_count"),
        (
            "shared_next_success_attempt_artifact_count",
            "mainline_current_section_missing_post_decision_contract_shared_artifact_count",
        ),
        ("lane_count", "mainline_current_section_missing_post_decision_contract_lane_count"),
    ):
        token = str(post_decision_contract_plan[key])
        post_plan_context_present = (
            post_decision_contract_plan["artifact_name"] in current_section
            and post_decision_contract_plan["status"] in current_section
        )
        if token and (not post_plan_context_present or token not in current_section):
            issues.append(
                {
                    "issue_id": issue_id,
                    "message": "Current formal-gate section must mention this post-decision contract plan count.",
                    key: post_decision_contract_plan[key],
                }
            )
    proof_status = str(proof_chain.get("status", ""))
    if proof_status and proof_status not in mainline_text:
        issues.append(
            {
                "issue_id": "mainline_missing_proof_chain_status",
                "message": "Mainline task book must mention the current proof-summary chain status.",
                "proof_summary_chain_status": proof_status,
            }
        )
    if next_required["total_missing_deliverables"] != len(deliverable_rows):
        issues.append(
            {
                "issue_id": "mainline_audit_deliverable_row_count_mismatch",
                "message": "Normalized deliverable row count must match total missing deliverables.",
                "total_missing_deliverables": next_required["total_missing_deliverables"],
                "row_count": len(deliverable_rows),
            }
        )
    return issues


def _post_decision_contract_plan_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not plan["present"]:
        issues.append(
            {
                "issue_id": "post_decision_contract_plan_missing",
                "message": "Mainline audit must consume the post-decision contract plan.",
            }
        )
        return issues
    if plan["artifact_name"] != EXPECTED_POST_DECISION_CONTRACT_PLAN_ARTIFACT:
        issues.append(
            {
                "issue_id": "post_decision_contract_plan_artifact_drift",
                "message": "Post-decision contract plan artifact name drifted.",
                "artifact_name": plan["artifact_name"],
            }
        )
    if plan["status"] != EXPECTED_POST_DECISION_CONTRACT_PLAN_STATUS:
        issues.append(
            {
                "issue_id": "post_decision_contract_plan_status_drift",
                "message": "Post-decision contract plan must remain blocked pending protocol-lane decision.",
                "status": plan["status"],
            }
        )
    if plan["audit_issue_count"] != 0:
        issues.append(
            {
                "issue_id": "post_decision_contract_plan_audit_issues_open",
                "message": "Post-decision contract plan must be audit-clean before mainline mirrors it.",
                "audit_issue_count": plan["audit_issue_count"],
            }
        )
    expected_counts = {
        "required_contract_section_count": EXPECTED_POST_DECISION_CONTRACT_SECTION_COUNT,
        "shared_next_success_attempt_artifact_count": EXPECTED_POST_DECISION_CONTRACT_SHARED_ARTIFACT_COUNT,
        "lane_count": EXPECTED_POST_DECISION_CONTRACT_LANE_COUNT,
    }
    for key, expected in expected_counts.items():
        if plan[key] != expected:
            issues.append(
                {
                    "issue_id": f"post_decision_contract_plan_{key}_drift",
                    "message": "Post-decision contract plan count drifted.",
                    "expected": expected,
                    "observed": plan[key],
                }
            )
    true_flags = [
        key
        for key in (
            "writes_contract",
            "approves_contract",
            "runs_training",
            "runs_remote_preflight",
            "remote_training_allowed_now",
            "formal_claim_allowed",
            "paper_result_material_allowed",
            "gate_contract_drafting_allowed_now",
            "gate_remote_training_allowed_now",
            "gate_formal_claim_allowed_now",
        )
        if plan.get(key) is True
    ]
    if true_flags:
        issues.append(
            {
                "issue_id": "post_decision_contract_plan_authorization_leak",
                "message": "Post-decision contract plan must not authorize contract writing, training, or claims.",
                "true_flags": true_flags,
            }
        )
    if plan["gate_selected_lane_id"] is not None:
        issues.append(
            {
                "issue_id": "post_decision_contract_plan_selected_lane_present",
                "message": "Post-decision plan mirrored by mainline must not select a lane while protocol decision is pending.",
                "selected_lane_id": plan["gate_selected_lane_id"],
            }
        )
    return issues


def _protocol_lane_readiness_issues(protocol_lane_readiness: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not protocol_lane_readiness["present"]:
        issues.append(
            {
                "issue_id": "protocol_lane_readiness_missing",
                "message": "Mainline audit must consume the protocol-lane readiness packet.",
            }
        )
        return issues
    if protocol_lane_readiness["artifact_name"] != EXPECTED_PROTOCOL_LANE_READINESS_ARTIFACT:
        issues.append(
            {
                "issue_id": "protocol_lane_readiness_artifact_drift",
                "message": "Protocol-lane readiness artifact name drifted.",
                "artifact_name": protocol_lane_readiness["artifact_name"],
            }
        )
    if protocol_lane_readiness["status"] != EXPECTED_PROTOCOL_LANE_READINESS_STATUS:
        issues.append(
            {
                "issue_id": "protocol_lane_readiness_status_drift",
                "message": "Readiness packet must stay ready for Dr Sun's decision, not become execution authorization.",
                "status": protocol_lane_readiness["status"],
            }
        )
    if protocol_lane_readiness["audit_issue_count"] != 0:
        issues.append(
            {
                "issue_id": "protocol_lane_readiness_audit_issues_open",
                "message": "Readiness packet must be audit-clean before mainline mirrors it.",
                "audit_issue_count": protocol_lane_readiness["audit_issue_count"],
            }
        )
    if protocol_lane_readiness["shared_next_success_attempt_artifact_count"] != (
        EXPECTED_PROTOCOL_LANE_READINESS_SHARED_ARTIFACT_COUNT
    ):
        issues.append(
            {
                "issue_id": "protocol_lane_readiness_shared_artifact_count_drift",
                "message": "Readiness packet must retain the 10-item next-success artifact index.",
                "shared_next_success_attempt_artifact_count": protocol_lane_readiness[
                    "shared_next_success_attempt_artifact_count"
                ],
            }
        )
    true_flags = [
        key
        for key in (
            "runs_training",
            "runs_remote_preflight",
            "remote_training_allowed_now",
            "formal_claim_allowed",
            "paper_result_material_allowed",
            "gate_remote_training_allowed_now",
            "gate_formal_claim_allowed_now",
            "gate_paper_result_material_allowed_now",
        )
        if protocol_lane_readiness.get(key) is True
    ]
    if true_flags:
        issues.append(
            {
                "issue_id": "protocol_lane_readiness_authorization_leak",
                "message": "Readiness packet must not authorize training, remote preflight, claims, or paper-result material.",
                "true_flags": true_flags,
            }
        )
    return issues


def _protocol_lane_status_issues(protocol_lane_status: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not protocol_lane_status["present"]:
        issues.append(
            {
                "issue_id": "protocol_lane_status_report_missing",
                "message": "Mainline audit must consume the protocol-lane status report.",
            }
        )
        return issues
    if protocol_lane_status["status"] != EXPECTED_PROTOCOL_LANE_STATUS:
        issues.append(
            {
                "issue_id": "protocol_lane_status_drift",
                "message": "Protocol-lane status must remain blocked pending Dr Sun's lane decision.",
                "observed_status": protocol_lane_status["status"],
            }
        )
    if protocol_lane_status["audit_issue_count"] != 0:
        issues.append(
            {
                "issue_id": "protocol_lane_status_audit_issues_open",
                "message": "Protocol-lane status report must be audit-clean before mainline mirrors it.",
                "audit_issue_count": protocol_lane_status["audit_issue_count"],
            }
        )
    if protocol_lane_status["next_blocked_lane"] != EXPECTED_PROTOCOL_LANE_NEXT_BLOCKED:
        issues.append(
            {
                "issue_id": "protocol_lane_status_next_blocked_lane_drift",
                "message": "Current blocked lane must remain protocol_lane_decision.",
                "observed_next_blocked_lane": protocol_lane_status["next_blocked_lane"],
            }
        )
    if protocol_lane_status["decision_record_status"] != EXPECTED_PROTOCOL_LANE_DECISION_RECORD_STATUS:
        issues.append(
            {
                "issue_id": "protocol_lane_status_decision_record_not_pending",
                "message": "Mainline audit currently mirrors the pending protocol-lane decision state.",
                "observed_decision_record_status": protocol_lane_status["decision_record_status"],
            }
        )
    if protocol_lane_status["selected_lane_id"] is not None:
        issues.append(
            {
                "issue_id": "protocol_lane_status_selected_lane_present",
                "message": "Pending protocol-lane state must not already have a selected lane.",
                "selected_lane_id": protocol_lane_status["selected_lane_id"],
            }
        )
    if protocol_lane_status["lane_count"] != len(EXPECTED_PROTOCOL_LANE_IDS):
        issues.append(
            {
                "issue_id": "protocol_lane_status_lane_count_drift",
                "message": "Protocol-lane matrix must expose exactly the four expected lane options.",
                "lane_count": protocol_lane_status["lane_count"],
            }
        )
    if protocol_lane_status["allowed_next_action_ids"] != list(EXPECTED_PROTOCOL_LANE_ALLOWED_NEXT_ACTIONS):
        issues.append(
            {
                "issue_id": "protocol_lane_status_allowed_actions_drift",
                "message": "Pending protocol-lane state may only allow record_protocol_lane_decision.",
                "allowed_next_action_ids": protocol_lane_status["allowed_next_action_ids"],
            }
        )
    missing_blocked_actions = [
        action for action in EXPECTED_PROTOCOL_LANE_BLOCKED_ACTIONS
        if action not in protocol_lane_status["blocked_action_ids"]
    ]
    if missing_blocked_actions:
        issues.append(
            {
                "issue_id": "protocol_lane_status_missing_blocked_actions",
                "message": "Protocol-lane status must keep training, preflight, claim, and paper-result actions blocked.",
                "missing_blocked_action_ids": missing_blocked_actions,
            }
        )
    true_flags = [key for key in PROTOCOL_LANE_FALSE_FLAGS if protocol_lane_status.get(key) is True]
    if true_flags:
        issues.append(
            {
                "issue_id": "protocol_lane_status_authorization_leak",
                "message": "Protocol-lane status must not authorize contract approval, training, preflight, claims, or paper-result material.",
                "true_flags": true_flags,
            }
        )
    if protocol_lane_status["post_decision_contract_plan_summary_present"] is not True:
        issues.append(
            {
                "issue_id": "protocol_lane_status_post_plan_summary_missing",
                "message": "Protocol-lane status report must expose the inherited post-decision contract plan summary.",
            }
        )
    if (
        protocol_lane_status["post_decision_contract_plan_status"]
        != EXPECTED_POST_DECISION_CONTRACT_PLAN_STATUS
    ):
        issues.append(
            {
                "issue_id": "protocol_lane_status_post_plan_status_drift",
                "message": "Protocol-lane status report must mirror the pending post-decision contract plan status.",
                "status": protocol_lane_status["post_decision_contract_plan_status"],
            }
        )
    expected_counts = {
        "post_decision_contract_plan_required_section_count": EXPECTED_POST_DECISION_CONTRACT_SECTION_COUNT,
        "post_decision_contract_plan_shared_artifact_count": EXPECTED_POST_DECISION_CONTRACT_SHARED_ARTIFACT_COUNT,
        "post_decision_contract_plan_lane_count": EXPECTED_POST_DECISION_CONTRACT_LANE_COUNT,
    }
    for key, expected in expected_counts.items():
        if protocol_lane_status[key] != expected:
            issues.append(
                {
                    "issue_id": f"protocol_lane_status_{key}_drift",
                    "message": "Protocol-lane status report post-plan count drifted.",
                    "expected": expected,
                    "observed": protocol_lane_status[key],
                }
            )
    post_plan_true_flags = [
        key
        for key in (
            "post_decision_contract_plan_writes_contract",
            "post_decision_contract_plan_approves_contract",
            "post_decision_contract_plan_runs_training",
            "post_decision_contract_plan_runs_remote_preflight",
            "post_decision_contract_plan_remote_training_allowed_now",
            "post_decision_contract_plan_formal_claim_allowed",
            "post_decision_contract_plan_paper_result_material_allowed",
            "post_decision_contract_plan_gate_contract_drafting_allowed_now",
        )
        if protocol_lane_status.get(key) is True
    ]
    if post_plan_true_flags:
        issues.append(
            {
                "issue_id": "protocol_lane_status_post_plan_authorization_leak",
                "message": "Protocol-lane status report's inherited post-plan summary must not authorize contract drafting, training, preflight, claims, or paper-result material while pending.",
                "true_flags": post_plan_true_flags,
            }
        )
    if protocol_lane_status["post_decision_contract_plan_selected_lane_id"] is not None:
        issues.append(
            {
                "issue_id": "protocol_lane_status_post_plan_selected_lane_present",
                "message": "Protocol-lane status report must not expose a selected post-plan lane while the decision is pending.",
                "selected_lane_id": protocol_lane_status["post_decision_contract_plan_selected_lane_id"],
            }
        )
    if protocol_lane_status["next_success_attempt_artifact_count"] != EXPECTED_POST_DECISION_CONTRACT_SHARED_ARTIFACT_COUNT:
        issues.append(
            {
                "issue_id": "protocol_lane_status_next_artifact_count_drift",
                "message": "Protocol-lane status report must expose the 10 next-attempt formal artifacts.",
                "artifact_count": protocol_lane_status["next_success_attempt_artifact_count"],
            }
        )
    if protocol_lane_status["next_success_attempt_artifact_category_counts"] != (
        EXPECTED_NEXT_SUCCESS_ARTIFACT_CATEGORY_COUNTS
    ):
        issues.append(
            {
                "issue_id": "protocol_lane_status_next_artifact_category_counts_drift",
                "message": "Protocol-lane status report next-attempt artifact category counts drifted.",
                "category_counts": protocol_lane_status["next_success_attempt_artifact_category_counts"],
            }
        )
    if (
        protocol_lane_status["post_decision_contract_plan_shared_artifact_category_counts"]
        != EXPECTED_NEXT_SUCCESS_ARTIFACT_CATEGORY_COUNTS
    ):
        issues.append(
            {
                "issue_id": "protocol_lane_status_post_plan_shared_artifact_category_counts_drift",
                "message": "Protocol-lane status report post-plan artifact category counts drifted.",
                "category_counts": protocol_lane_status[
                    "post_decision_contract_plan_shared_artifact_category_counts"
                ],
            }
        )
    if (
        protocol_lane_status["post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"]
        is not EXPECTED_OLD_FAILED_RUN_INVALID_FOR_NEXT_SUCCESS_ATTEMPT
    ):
        issues.append(
            {
                "issue_id": "protocol_lane_status_post_plan_old_failed_invalid_flag_drift",
                "message": "Protocol-lane status report post-plan summary must keep old failed-run artifacts invalid for the next success attempt.",
                "observed": protocol_lane_status[
                    "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"
                ],
            }
        )
    if (
        protocol_lane_status["old_failed_run_artifacts_invalid_for_next_success_attempt"]
        is not EXPECTED_OLD_FAILED_RUN_INVALID_FOR_NEXT_SUCCESS_ATTEMPT
    ):
        issues.append(
            {
                "issue_id": "protocol_lane_status_old_failed_invalid_flag_drift",
                "message": "Protocol-lane status report must keep old failed-run artifacts invalid for the next success attempt.",
                "observed": protocol_lane_status["old_failed_run_artifacts_invalid_for_next_success_attempt"],
            }
        )
    missing_artifact_ids: list[str] = []
    ids_by_category = protocol_lane_status["next_success_attempt_artifact_ids_by_category"]
    for category, expected_ids in EXPECTED_NEXT_SUCCESS_ARTIFACT_IDS_BY_CATEGORY.items():
        observed_ids = ids_by_category.get(category, [])
        for artifact_id in expected_ids:
            if artifact_id not in observed_ids:
                missing_artifact_ids.append(f"{category}:{artifact_id}")
    if missing_artifact_ids:
        issues.append(
            {
                "issue_id": "protocol_lane_status_next_artifact_ids_missing",
                "message": "Protocol-lane status report must list every next-attempt artifact id by category.",
                "missing_artifact_ids": missing_artifact_ids,
            }
        )
    return issues


def _decision_evidence_matrix_issues(decision_matrix: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not decision_matrix["present"]:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_missing",
                "message": "Status report must expose the F02.6 decision evidence matrix summary.",
            }
        )
    if decision_matrix["matrix_id"] != EXPECTED_DECISION_EVIDENCE_MATRIX_ID:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_id_drift",
                "message": "Status report decision evidence matrix id must remain the F02.6 matrix.",
                "observed_matrix_id": decision_matrix["matrix_id"],
            }
        )
    if decision_matrix["status"] != EXPECTED_DECISION_EVIDENCE_MATRIX_STATUS:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_status_drift",
                "message": "Decision evidence matrix must remain a decision aid, not authorization.",
                "observed_status": decision_matrix["status"],
            }
        )
    if decision_matrix["route_count"] != len(EXPECTED_DECISION_EVIDENCE_MATRIX_ROUTES):
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_route_count_drift",
                "message": "Decision evidence matrix must retain the approve and reject routes.",
                "observed_route_count": decision_matrix["route_count"],
            }
        )
    missing_routes = [
        route for route in EXPECTED_DECISION_EVIDENCE_MATRIX_ROUTES if route not in decision_matrix["route_decisions"]
    ]
    if missing_routes:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_missing_routes",
                "message": "Decision evidence matrix must retain both F02.6 route decisions.",
                "missing_routes": missing_routes,
            }
        )
    if decision_matrix["required_evidence_count"] < MIN_REQUIRED_DECISION_EVIDENCE_ROWS:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_too_few_required_rows",
                "message": "Decision evidence matrix must retain the full required evidence basis.",
                "required_evidence_count": decision_matrix["required_evidence_count"],
            }
        )
    if decision_matrix["satisfied_required_evidence_count"] != decision_matrix["required_evidence_count"]:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_unsatisfied_required_rows",
                "message": "Decision evidence matrix must not hide unsatisfied required evidence rows.",
                "required_evidence_count": decision_matrix["required_evidence_count"],
                "satisfied_required_evidence_count": decision_matrix["satisfied_required_evidence_count"],
            }
        )
    if decision_matrix["missing_required_evidence_count"] != 0:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_missing_required_evidence",
                "message": "Decision evidence matrix cannot be mirrored into the mainline while required evidence is missing.",
                "missing_required_evidence_count": decision_matrix["missing_required_evidence_count"],
                "missing_required_evidence_ids": decision_matrix["missing_required_evidence_ids"],
            }
        )
    if decision_matrix["source_issue_count"] != 0:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_source_issues_open",
                "message": "Decision evidence matrix cannot be mirrored while source integrity issues are open.",
                "source_issue_count": decision_matrix["source_issue_count"],
            }
        )
    if decision_matrix["global_invalid_substitute_count"] < MIN_GLOBAL_INVALID_SUBSTITUTE_ROWS:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_invalid_substitutes_missing",
                "message": "Decision evidence matrix must retain invalid substitutes so weak evidence is rejected.",
                "global_invalid_substitute_count": decision_matrix["global_invalid_substitute_count"],
            }
        )
    allowed_leaks = [
        key for key in DECISION_EVIDENCE_MATRIX_ALLOWED_KEYS if decision_matrix["authorization_flags"].get(key) is True
    ]
    if allowed_leaks:
        issues.append(
            {
                "issue_id": "status_report_decision_evidence_matrix_authorization_leak",
                "message": "Decision evidence matrix must not authorize training, preflight, claims, or paper-result material.",
                "allowed_leaks": allowed_leaks,
            }
        )
    return issues


def _status_report_issues(
    *, next_action_guard: dict[str, Any], next_required: dict[str, Any]
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not next_action_guard["present"]:
        issues.append(
            {
                "issue_id": "status_report_next_action_guard_missing",
                "message": "Status report must expose next_action_guard_summary.",
            }
        )
        return issues
    pending_f02_6 = next_action_guard["pending_f02_6_decision"] is True
    if not pending_f02_6:
        if next_action_guard["status"] not in {"next_action_guard_not_applicable", "next_action_guard_passed"}:
            issues.append(
                {
                    "issue_id": "status_report_next_action_guard_invalid_after_f02_6",
                    "message": "After F02.6 closes, next-action guard should be not-applicable or passed.",
                    "observed_status": next_action_guard["status"],
                }
            )
    elif next_action_guard["status"] != "next_action_guard_passed":
        issues.append(
            {
                "issue_id": "status_report_next_action_guard_not_passed",
                "message": "Status report next-action guard must be passed before the mainline can mirror it.",
                "observed_status": next_action_guard["status"],
            }
        )
    if pending_f02_6 and next_action_guard["expected_next_action_id"] != "record_f02_6_decision":
        issues.append(
            {
                "issue_id": "status_report_unexpected_next_action",
                "message": "F02.6-pending mainline audit expects the next action to remain the human decision record.",
                "observed_next_action_id": next_action_guard["expected_next_action_id"],
            }
        )
    guarded_next_action_active = pending_f02_6 or bool(next_action_guard["expected_next_action_id"])
    if guarded_next_action_active and (
        next_action_guard["execution_leak_count"] > 0 or not next_action_guard["all_execution_disabled_now"]
    ):
        issues.append(
            {
                "issue_id": "status_report_next_action_guard_execution_leak",
                "message": "Status report exposes an execution leak while the mainline is mirroring a gated state.",
                "execution_leak_count": next_action_guard["execution_leak_count"],
                "all_execution_disabled_now": next_action_guard["all_execution_disabled_now"],
            }
        )
    if not next_required["present"]:
        issues.append(
            {
                "issue_id": "status_report_next_required_deliverables_missing",
                "message": "Status report must expose next_required_formal_deliverables.",
            }
        )
    if next_required["not_paper_result_material"] is not True:
        issues.append(
            {
                "issue_id": "status_report_next_required_marked_as_paper_result",
                "message": "Next-required formal deliverables must not be marked as paper-result material.",
            }
        )
    if next_required["runs_training"] is True or next_required["runs_remote_preflight"] is True:
        issues.append(
            {
                "issue_id": "status_report_next_required_executes_work",
                "message": "Next-required formal deliverables summary must remain read-only.",
                "runs_training": next_required["runs_training"],
                "runs_remote_preflight": next_required["runs_remote_preflight"],
            }
        )
    if next_required["total_missing_deliverables"] != next_required["row_count"]:
        issues.append(
            {
                "issue_id": "status_report_next_required_row_count_mismatch",
                "message": "Next-required formal deliverable rows must match the total missing deliverable count.",
                "total_missing_deliverables": next_required["total_missing_deliverables"],
                "row_count": next_required["row_count"],
            }
        )
    return issues


def _proof_chain_issues(proof_chain: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if proof_chain.get("audit_issue_count") != 0:
        issues.append(
            {
                "issue_id": "proof_summary_chain_has_audit_issues",
                "message": "Mainline task-book state should only mirror a clean proof-summary chain.",
                "audit_issue_count": proof_chain.get("audit_issue_count"),
            }
        )
    proof_audit_input_safety_issue_count = int(proof_chain.get("proof_audit_input_safety_issue_count") or 0)
    if proof_audit_input_safety_issue_count > 0:
        issues.append(
            {
                "issue_id": "proof_summary_chain_proof_audit_input_safety_issues_open",
                "message": "Mainline task-book state cannot mirror a proof-summary chain with upstream proof-audit input-safety issues.",
                "proof_audit_input_safety_issue_count": proof_audit_input_safety_issue_count,
            }
        )
    proof_audit_blockers = _strings(proof_chain.get("proof_audit_blockers"))
    if "proof_audit_input_safety_issues_open" in proof_audit_blockers:
        issues.append(
            {
                "issue_id": "proof_summary_chain_proof_audit_input_safety_blocker_open",
                "message": "Mainline task-book state cannot ignore an upstream proof-audit input-safety blocker.",
                "proof_audit_blockers": proof_audit_blockers,
            }
        )
    if proof_chain.get("next_action_guard_row_count") != proof_chain.get("next_action_guard_consistent_row_count"):
        issues.append(
            {
                "issue_id": "proof_summary_chain_next_action_guard_inconsistent",
                "message": "Proof-summary chain must agree on the next-action guard before mainline mirrors it.",
                "row_count": proof_chain.get("next_action_guard_row_count"),
                "consistent_row_count": proof_chain.get("next_action_guard_consistent_row_count"),
            }
        )
    if proof_chain.get("next_required_deliverables_row_count") != proof_chain.get(
        "next_required_deliverables_consistent_row_count"
    ):
        issues.append(
            {
                "issue_id": "proof_summary_chain_next_required_deliverables_inconsistent",
                "message": "Proof-summary chain must agree on next required formal deliverables before mainline mirrors them.",
                "row_count": proof_chain.get("next_required_deliverables_row_count"),
                "consistent_row_count": proof_chain.get("next_required_deliverables_consistent_row_count"),
            }
        )
    handoff_single_next_action_row_count = proof_chain.get("handoff_single_next_action_row_count")
    handoff_single_next_action_consistent_row_count = proof_chain.get(
        "handoff_single_next_action_consistent_row_count"
    )
    if (
        not isinstance(handoff_single_next_action_row_count, int)
        or handoff_single_next_action_row_count <= 0
        or handoff_single_next_action_row_count != handoff_single_next_action_consistent_row_count
    ):
        issues.append(
            {
                "issue_id": "proof_summary_chain_handoff_single_next_action_inconsistent",
                "message": "Proof-summary chain must agree on the handoff single-next-action index before mainline mirrors it.",
                "row_count": handoff_single_next_action_row_count,
                "consistent_row_count": handoff_single_next_action_consistent_row_count,
            }
        )
    if proof_chain.get("runs_training") is True or proof_chain.get("runs_remote_preflight") is True:
        issues.append(
            {
                "issue_id": "proof_summary_chain_executes_work",
                "message": "Proof-summary chain audit must remain read-only.",
                "runs_training": proof_chain.get("runs_training"),
                "runs_remote_preflight": proof_chain.get("runs_remote_preflight"),
            }
        )
    if proof_chain.get("formal_claim_allowed") is True:
        issues.append(
            {
                "issue_id": "proof_summary_chain_allows_formal_claim",
                "message": "Proof-summary chain audit must not allow formal claims while proof is open.",
            }
        )
    return issues


def _deliverable_rows(
    next_required: dict[str, Any], *, mainline_text: str, current_section: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in next_required["rows"]:
        matrix_id = str(row.get("matrix_id", ""))
        artifact_id = str(row.get("artifact_id", ""))
        rows.append(
            {
                "matrix_id": matrix_id,
                "safe_matrix_id": _safe_id(matrix_id),
                "category": row.get("category"),
                "artifact_id": artifact_id,
                "mentioned": bool(artifact_id and artifact_id in mainline_text),
                "mentioned_in_current_section": bool(artifact_id and artifact_id in current_section),
                "responsible_stage_id": row.get("responsible_stage_id"),
                "responsible_stage_allowed_now": bool(row.get("responsible_stage_allowed_now")),
            }
        )
    return rows


def _current_section(mainline_text: str) -> str:
    marker_index = mainline_text.rfind(CURRENT_STATE_MARKER)
    if marker_index < 0:
        return ""
    return mainline_text[marker_index:]


def _normalize_next_action_guard(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    return {
        "present": bool(raw),
        "status": raw.get("status"),
        "pending_f02_6_decision": raw.get("pending_f02_6_decision")
        if isinstance(raw.get("pending_f02_6_decision"), bool)
        else None,
        "expected_next_action_id": raw.get("expected_next_action_id"),
        "all_execution_disabled_now": bool(raw.get("all_execution_disabled_now")),
        "execution_leak_count": int(raw.get("execution_leak_count") or 0),
    }


def _normalize_next_required_deliverables(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    rows = raw.get("rows", [])
    if isinstance(rows, dict):
        normalized_rows = list(rows.values())
    elif isinstance(rows, list):
        normalized_rows = [row for row in rows if isinstance(row, dict)]
    else:
        normalized_rows = []
    return {
        "present": bool(raw),
        "status": raw.get("status"),
        "not_paper_result_material": raw.get("not_paper_result_material"),
        "runs_training": raw.get("runs_training"),
        "runs_remote_preflight": raw.get("runs_remote_preflight"),
        "total_missing_deliverables": int(raw.get("total_missing_deliverables") or 0),
        "blocked_category_count": int(raw.get("blocked_category_count") or 0),
        "row_count": len(normalized_rows),
        "rows": normalized_rows,
    }


def _normalize_decision_evidence_matrix_summary(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    authorization_flags = {key: raw.get(key) for key in DECISION_EVIDENCE_MATRIX_ALLOWED_KEYS}
    return {
        "present": bool(raw.get("present")) if "present" in raw else bool(raw),
        "matrix_id": str(raw.get("matrix_id") or ""),
        "status": str(raw.get("status") or ""),
        "route_count": int(raw.get("route_count") or 0),
        "route_decisions": _strings(raw.get("route_decisions")),
        "required_evidence_count": int(raw.get("required_evidence_count") or 0),
        "satisfied_required_evidence_count": int(raw.get("satisfied_required_evidence_count") or 0),
        "missing_required_evidence_count": int(raw.get("missing_required_evidence_count") or 0),
        "missing_required_evidence_ids": _strings(raw.get("missing_required_evidence_ids")),
        "source_issue_count": int(raw.get("source_issue_count") or 0),
        "global_invalid_substitute_count": int(raw.get("global_invalid_substitute_count") or 0),
        "authorization_flags": authorization_flags,
        "evidence_counts_by_route": raw.get("evidence_counts_by_route")
        if isinstance(raw.get("evidence_counts_by_route"), dict)
        else {},
        "invalid_substitute_counts_by_route": raw.get("invalid_substitute_counts_by_route")
        if isinstance(raw.get("invalid_substitute_counts_by_route"), dict)
        else {},
    }


def _normalize_protocol_lane_status_report(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    current = raw.get("current_status") if isinstance(raw.get("current_status"), dict) else {}
    artifact_ids_by_category = current.get("next_success_attempt_artifact_ids_by_category")
    if not isinstance(artifact_ids_by_category, dict):
        artifact_ids_by_category = {}
    category_counts = current.get("next_success_attempt_artifact_category_counts")
    if not isinstance(category_counts, dict):
        category_counts = {}
    post_plan_category_counts = current.get("post_decision_contract_plan_shared_artifact_category_counts")
    if not isinstance(post_plan_category_counts, dict):
        post_plan_category_counts = {}
    normalized = {
        "present": bool(raw),
        "status": str(raw.get("status") or ""),
        "audit_issue_count": int(raw.get("audit_issue_count") or 0),
        "next_blocked_lane": str(current.get("next_blocked_lane") or ""),
        "decision_packet_status": str(current.get("decision_packet_status") or ""),
        "decision_record_status": str(current.get("decision_record_status") or ""),
        "decision_gate_status": str(current.get("decision_gate_status") or ""),
        "contract_authoring_gate_status": str(current.get("contract_authoring_gate_status") or ""),
        "lane_matrix_status": str(current.get("lane_matrix_status") or ""),
        "lane_count": int(current.get("lane_count") or 0),
        "next_round_requirements_status": str(current.get("next_round_requirements_status") or ""),
        "selected_lane_id": current.get("selected_lane_id"),
        "contract_action": str(current.get("contract_action") or ""),
        "allowed_next_action_ids": _strings(current.get("allowed_next_action_ids")),
        "blocked_action_ids": _strings(current.get("blocked_action_ids")),
        "post_decision_contract_plan_summary_present": bool(
            current.get("post_decision_contract_plan_summary_present")
        ),
        "post_decision_contract_plan_status": str(current.get("post_decision_contract_plan_status") or ""),
        "post_decision_contract_plan_audit_issue_count": int(
            current.get("post_decision_contract_plan_audit_issue_count") or 0
        ),
        "post_decision_contract_plan_required_section_count": int(
            current.get("post_decision_contract_plan_required_section_count") or 0
        ),
        "post_decision_contract_plan_shared_artifact_count": int(
            current.get("post_decision_contract_plan_shared_artifact_count") or 0
        ),
        "post_decision_contract_plan_shared_artifact_category_counts": {
            str(key): int(value or 0) for key, value in post_plan_category_counts.items()
        },
        "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt": current.get(
            "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"
        )
        if isinstance(
            current.get("post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"),
            bool,
        )
        else None,
        "post_decision_contract_plan_lane_count": int(
            current.get("post_decision_contract_plan_lane_count") or 0
        ),
        "post_decision_contract_plan_selected_lane_id": current.get(
            "post_decision_contract_plan_selected_lane_id"
        ),
        "post_decision_contract_plan_writes_contract": current.get(
            "post_decision_contract_plan_writes_contract"
        ),
        "post_decision_contract_plan_approves_contract": current.get(
            "post_decision_contract_plan_approves_contract"
        ),
        "post_decision_contract_plan_runs_training": current.get(
            "post_decision_contract_plan_runs_training"
        ),
        "post_decision_contract_plan_runs_remote_preflight": current.get(
            "post_decision_contract_plan_runs_remote_preflight"
        ),
        "post_decision_contract_plan_remote_training_allowed_now": current.get(
            "post_decision_contract_plan_remote_training_allowed_now"
        ),
        "post_decision_contract_plan_formal_claim_allowed": current.get(
            "post_decision_contract_plan_formal_claim_allowed"
        ),
        "post_decision_contract_plan_paper_result_material_allowed": current.get(
            "post_decision_contract_plan_paper_result_material_allowed"
        ),
        "post_decision_contract_plan_gate_contract_drafting_allowed_now": current.get(
            "post_decision_contract_plan_gate_contract_drafting_allowed_now"
        ),
        "next_success_attempt_artifact_status": str(current.get("next_success_attempt_artifact_status") or ""),
        "next_success_attempt_artifact_count": int(current.get("next_success_attempt_artifact_count") or 0),
        "next_success_attempt_artifact_category_counts": {
            str(key): int(value or 0) for key, value in category_counts.items()
        },
        "next_success_attempt_artifact_ids_by_category": {
            str(key): _strings(value) for key, value in artifact_ids_by_category.items()
        },
        "old_failed_run_artifacts_invalid_for_next_success_attempt": current.get(
            "old_failed_run_artifacts_invalid_for_next_success_attempt"
        )
        if isinstance(current.get("old_failed_run_artifacts_invalid_for_next_success_attempt"), bool)
        else None,
    }
    for key in PROTOCOL_LANE_FALSE_FLAGS:
        normalized[key] = bool(current.get(key))
    return normalized


def _normalize_protocol_lane_readiness(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    gate = raw.get("gate_state") if isinstance(raw.get("gate_state"), dict) else {}
    return {
        "present": bool(raw),
        "artifact_name": str(raw.get("artifact_name") or ""),
        "status": str(raw.get("status") or ""),
        "audit_issue_count": int(raw.get("audit_issue_count") or 0),
        "lane_count": int(raw.get("lane_count") or 0),
        "shared_next_success_attempt_artifact_count": int(
            raw.get("shared_next_success_attempt_artifact_count") or 0
        ),
        "not_paper_result_material": raw.get("not_paper_result_material"),
        "executes_commands": raw.get("executes_commands"),
        "runs_training": raw.get("runs_training"),
        "runs_remote_preflight": raw.get("runs_remote_preflight"),
        "remote_training_allowed_now": raw.get("remote_training_allowed_now"),
        "formal_claim_allowed": raw.get("formal_claim_allowed"),
        "paper_result_material_allowed": raw.get("paper_result_material_allowed"),
        "gate_next_blocked_lane": str(gate.get("next_blocked_lane") or ""),
        "gate_selected_lane_id": gate.get("selected_lane_id"),
        "gate_decision_owner_required": str(gate.get("decision_owner_required") or ""),
        "gate_remote_training_allowed_now": gate.get("remote_training_allowed_now"),
        "gate_formal_claim_allowed_now": gate.get("formal_claim_allowed_now"),
        "gate_paper_result_material_allowed_now": gate.get("paper_result_material_allowed_now"),
    }


def _normalize_post_decision_contract_plan(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    gate = raw.get("gate_state") if isinstance(raw.get("gate_state"), dict) else {}
    return {
        "present": bool(raw),
        "artifact_name": str(raw.get("artifact_name") or ""),
        "status": str(raw.get("status") or ""),
        "audit_issue_count": int(raw.get("audit_issue_count") or 0),
        "required_contract_section_count": int(raw.get("required_contract_section_count") or 0),
        "shared_next_success_attempt_artifact_count": int(
            raw.get("shared_next_success_attempt_artifact_count") or 0
        ),
        "shared_next_success_attempt_artifact_category_counts": {
            str(key): int(value or 0)
            for key, value in raw.get("shared_next_success_attempt_artifact_category_counts", {}).items()
        }
        if isinstance(raw.get("shared_next_success_attempt_artifact_category_counts"), dict)
        else {},
        "old_failed_run_artifacts_invalid_for_next_success_attempt": raw.get(
            "old_failed_run_artifacts_invalid_for_next_success_attempt"
        )
        if isinstance(raw.get("old_failed_run_artifacts_invalid_for_next_success_attempt"), bool)
        else None,
        "lane_count": int(raw.get("lane_count") or 0),
        "not_paper_result_material": raw.get("not_paper_result_material"),
        "executes_commands": raw.get("executes_commands"),
        "writes_contract": raw.get("writes_contract"),
        "approves_contract": raw.get("approves_contract"),
        "runs_training": raw.get("runs_training"),
        "runs_remote_preflight": raw.get("runs_remote_preflight"),
        "remote_training_allowed_now": raw.get("remote_training_allowed_now"),
        "formal_claim_allowed": raw.get("formal_claim_allowed"),
        "paper_result_material_allowed": raw.get("paper_result_material_allowed"),
        "gate_next_blocked_lane": str(gate.get("next_blocked_lane") or ""),
        "gate_selected_lane_id": gate.get("selected_lane_id"),
        "gate_contract_drafting_allowed_now": gate.get("contract_drafting_allowed_now"),
        "gate_remote_training_allowed_now": gate.get("remote_training_allowed_now"),
        "gate_formal_claim_allowed_now": gate.get("formal_claim_allowed_now"),
    }


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Mainline Formal Gate State Audit",
        "",
        "This file checks that the long-term Module2 mainline task book mirrors the current formal-gate state. It is not a training run, remote preflight, formal evaluation, or paper result.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- expected_next_action_id: `{manifest['expected_next_action_id']}`",
        f"- expected_next_action_mentioned: `{manifest['expected_next_action_mentioned']}`",
        f"- total_missing_deliverables: `{manifest['total_missing_deliverables']}`",
        f"- mainline_missing_deliverable_mention_count: `{manifest['mainline_missing_deliverable_mention_count']}`",
        "- f02_6_decision_evidence_matrix_summary: "
        f"`{manifest['f02_6_decision_evidence_matrix_summary']}`",
        "- f02_6_decision_evidence_matrix_mentioned: "
        f"`{manifest['f02_6_decision_evidence_matrix_mentioned']}`",
        "- f02_6_decision_evidence_matrix_status_mentioned: "
        f"`{manifest['f02_6_decision_evidence_matrix_status_mentioned']}`",
        "- protocol_lane_status_summary: "
        f"`{manifest['protocol_lane_status_summary']}`",
        f"- protocol_lane_status_mentioned: `{manifest['protocol_lane_status_mentioned']}`",
        f"- protocol_lane_next_blocked_mentioned: `{manifest['protocol_lane_next_blocked_mentioned']}`",
        f"- protocol_lane_next_action_mentioned: `{manifest['protocol_lane_next_action_mentioned']}`",
        "- protocol_lane_readiness_summary: "
        f"`{manifest['protocol_lane_readiness_summary']}`",
        f"- protocol_lane_readiness_artifact_mentioned: `{manifest['protocol_lane_readiness_artifact_mentioned']}`",
        f"- protocol_lane_readiness_status_mentioned: `{manifest['protocol_lane_readiness_status_mentioned']}`",
        "- post_decision_contract_plan_summary: "
        f"`{manifest['post_decision_contract_plan_summary']}`",
        "- post_decision_contract_plan_artifact_mentioned: "
        f"`{manifest['post_decision_contract_plan_artifact_mentioned']}`",
        "- post_decision_contract_plan_status_mentioned: "
        f"`{manifest['post_decision_contract_plan_status_mentioned']}`",
        f"- proof_summary_chain_status: `{manifest['proof_summary_chain_status']}`",
        "- proof_summary_handoff_single_next_action_consistency: "
        f"`{manifest['proof_summary_handoff_single_next_action_consistency']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        "",
        "## Audit Issues",
        "",
    ]
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Missing Formal Deliverables", ""])
    for row in manifest["deliverable_rows"]:
        lines.append(
            f"- `{row['matrix_id']}`: artifact_id=`{row['artifact_id']}`, mentioned=`{row['mentioned']}`, "
            f"mentioned_in_current_section=`{row['mentioned_in_current_section']}`"
        )
    lines.extend(["", "## F02.6 Decision Evidence Matrix", ""])
    decision_matrix = manifest["f02_6_decision_evidence_matrix_summary"]
    lines.extend(
        [
            f"- matrix_id: `{decision_matrix['matrix_id']}`",
            f"- status: `{decision_matrix['status']}`",
            f"- route_count: `{decision_matrix['route_count']}`",
            f"- required_evidence_count: `{decision_matrix['required_evidence_count']}`",
            f"- missing_required_evidence_count: `{decision_matrix['missing_required_evidence_count']}`",
            f"- authorization_flags: `{decision_matrix['authorization_flags']}`",
        ]
    )
    lines.extend(["", "## Protocol Lane Status", ""])
    protocol_lane = manifest["protocol_lane_status_summary"]
    lines.extend(
        [
            f"- status: `{protocol_lane['status']}`",
            f"- next_blocked_lane: `{protocol_lane['next_blocked_lane']}`",
            f"- decision_record_status: `{protocol_lane['decision_record_status']}`",
            f"- selected_lane_id: `{protocol_lane['selected_lane_id']}`",
            f"- lane_count: `{protocol_lane['lane_count']}`",
            f"- allowed_next_action_ids: `{protocol_lane['allowed_next_action_ids']}`",
            f"- blocked_action_ids: `{protocol_lane['blocked_action_ids']}`",
        ]
    )
    for row in manifest["protocol_lane_lane_mentions"]:
        lines.append(f"- lane `{row['lane_id']}`: mentioned=`{row['mentioned']}`")
    for row in manifest["protocol_lane_blocked_action_mentions"]:
        lines.append(f"- blocked action `{row['action_id']}`: mentioned=`{row['mentioned']}`")
    lines.extend(["", "## Protocol Lane Readiness", ""])
    readiness = manifest["protocol_lane_readiness_summary"]
    lines.extend(
        [
            f"- artifact_name: `{readiness['artifact_name']}`",
            f"- status: `{readiness['status']}`",
            f"- audit_issue_count: `{readiness['audit_issue_count']}`",
            f"- lane_count: `{readiness['lane_count']}`",
            "- shared_next_success_attempt_artifact_count: "
            f"`{readiness['shared_next_success_attempt_artifact_count']}`",
            f"- gate_next_blocked_lane: `{readiness['gate_next_blocked_lane']}`",
            f"- gate_selected_lane_id: `{readiness['gate_selected_lane_id']}`",
            f"- gate_remote_training_allowed_now: `{readiness['gate_remote_training_allowed_now']}`",
        ]
    )
    lines.extend(["", "## Post-Decision Contract Plan", ""])
    post_plan = manifest["post_decision_contract_plan_summary"]
    lines.extend(
        [
            f"- artifact_name: `{post_plan['artifact_name']}`",
            f"- status: `{post_plan['status']}`",
            f"- audit_issue_count: `{post_plan['audit_issue_count']}`",
            f"- required_contract_section_count: `{post_plan['required_contract_section_count']}`",
            "- shared_next_success_attempt_artifact_count: "
            f"`{post_plan['shared_next_success_attempt_artifact_count']}`",
            f"- lane_count: `{post_plan['lane_count']}`",
            f"- gate_selected_lane_id: `{post_plan['gate_selected_lane_id']}`",
            f"- gate_contract_drafting_allowed_now: `{post_plan['gate_contract_drafting_allowed_now']}`",
            f"- gate_remote_training_allowed_now: `{post_plan['gate_remote_training_allowed_now']}`",
        ]
    )
    lines.extend(["", "## Current Boundary Tokens", ""])
    for row in manifest["current_boundary_tokens"]:
        lines.append(f"- `{row['token']}`: mentioned=`{row['mentioned']}`")
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _source_head() -> str:
    return module2_source_head()


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value).strip("_") or "unknown"


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id", "unknown_issue"))
        if issue_id in seen:
            continue
        seen.add(issue_id)
        unique.append(issue)
    return unique


if __name__ == "__main__":
    raise SystemExit(main())
