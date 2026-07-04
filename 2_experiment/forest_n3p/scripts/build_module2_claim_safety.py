from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_claim_safety")
DEFAULT_PAPER_TABLES = Path("0_trials/module2_paper_tables/module2_paper_tables.json")
DEFAULT_H02_FORMAL_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_F02_6_PACKET = Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json")
DEFAULT_GATE3_AUDIT = Path("0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json")
DEFAULT_METHOD_ALGORITHMS = Path("0_trials/module2_method_algorithms/module2_method_algorithms.json")
DEFAULT_SYSTEM_DIAGRAM = Path("0_trials/module2_system_diagram/module2_system_diagram.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
STATUS_REPORT_CLOSURE_STAGE_IDS = (
    "approved_remote_preflight",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
)
STATUS_REPORT_REMOTE_STEP_IDS = (
    "sync_to_remote",
    "run_remote_preflight",
    "run_remote_training",
    "run_remote_audit",
)
STATUS_REPORT_REQUIREMENT_IDS = (
    "training_remote_ppo_checkpoint",
    "evaluation_gate3_episode_outputs",
    "acceptance_remote_pullback_and_audit",
    "h01_h02_formal_evaluation_acceptance",
)
STATUS_REPORT_REMOTE_PREFLIGHT_REQUIREMENT_IDS = (
    "f02_6_decision_closed_for_preflight",
    "approved_remote_preflight_manifest",
    "remote_preflight_protocol_contract",
    "remote_preflight_command_packetized",
)
STATUS_REPORT_POST_RUN_ACCEPTANCE_REQUIREMENT_IDS = (
    "pullback_expected_artifacts_complete",
    "checkpoint_hash_manifest_recorded",
    "gate3_formal_audit_accepts_remote_run",
    "h01_h02_regenerated_from_audited_checkpoint",
)
STATUS_REPORT_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS = (
    "h01_schema_and_h02_output_schema_match",
    "h02_formal_scope_and_scale_match_h01",
    "gate3_audit_and_pullback_acceptance",
    "ppo_rows_and_checkpoint_hash_present",
)
STATUS_REPORT_REMAINING_DELIVERABLE_MATRIX_IDS = (
    "training:train_final_model_zip",
    "training:train_summary_json",
    "training:train_training_manifest_json",
    "evaluation:eval_gate3_eval_episodes_csv",
    "evaluation:eval_gate3_summary_json",
    "acceptance:gate3_trial_manifest_json",
    "acceptance:gate3_formal_audit_json",
    "acceptance:pulled_back_checkpoint_hash_record",
    "formal_acceptance:h01_ready_for_formal_run",
    "formal_acceptance:h02_formal_output_acceptance",
)
STATUS_REPORT_REMAINING_DELIVERABLE_CATEGORY_IDS = (
    "training",
    "evaluation",
    "acceptance",
    "formal_acceptance",
)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _repo_root()
    manifest = build_manifest(
        repo_root=repo_root,
        paper_tables_path=args.paper_tables,
        h02_formal_acceptance_path=args.h02_formal_acceptance,
        h01_manifest_path=args.h01_manifest,
        f02_6_packet_path=args.f02_6_packet,
        gate3_audit_path=args.gate3_audit,
        method_algorithms_path=args.method_algorithms,
        system_diagram_path=args.system_diagram,
        closure_checklist_path=args.closure_checklist,
        status_report_path=args.status_report,
        draft_text_path=args.draft_text,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = args.manifest_out or output_dir / "module2_claim_safety.json"
    markdown_out = args.markdown_out or output_dir / "module2_claim_safety.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(
    *,
    repo_root: Path,
    paper_tables_path: Path,
    h02_formal_acceptance_path: Path,
    h01_manifest_path: Path,
    f02_6_packet_path: Path,
    gate3_audit_path: Path,
    method_algorithms_path: Path,
    system_diagram_path: Path,
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST,
    status_report_path: Path = DEFAULT_STATUS_REPORT,
    draft_text_path: Path | None = None,
) -> dict[str, Any]:
    paper_tables = _read_json(paper_tables_path)
    h02_formal_acceptance = _read_json(h02_formal_acceptance_path)
    h01_manifest = _read_json(h01_manifest_path)
    f02_6_packet = _read_json(f02_6_packet_path)
    gate3_audit = _read_json(gate3_audit_path)
    method_algorithms = _read_json(method_algorithms_path)
    system_diagram = _read_json(system_diagram_path)
    closure_checklist = _read_json(closure_checklist_path)
    status_report = _read_json(status_report_path)

    formal_blockers = _formal_performance_blockers(
        paper_tables=paper_tables,
        h02_formal_acceptance=h02_formal_acceptance,
        h01_manifest=h01_manifest,
        f02_6_packet=f02_6_packet,
        closure_checklist=closure_checklist,
        status_report=status_report,
    )
    status_report_remote_gate_summary = _status_report_remote_gate_summary(status_report)
    status_report_handoff_summary = _status_report_handoff_summary(status_report)
    status_report_missing_artifacts_handoff_summary = _status_report_missing_artifacts_handoff_summary(status_report)
    status_report_requirement_stage_summary = _status_report_requirement_stage_summary(status_report)
    status_report_remote_requirement_summary = _status_report_remote_requirement_summary(status_report)
    status_report_h02_acceptance_requirement_summary = _status_report_h02_acceptance_requirement_summary(status_report)
    status_report_remaining_deliverables_acceptance_summary = _status_report_remaining_deliverables_acceptance_summary(
        status_report
    )
    status_report_remaining_deliverables_gap_summary = _status_report_remaining_deliverables_gap_summary(status_report)
    status_report_decision_intake_summary = _status_report_decision_intake_summary(status_report)
    formal_allowed = not formal_blockers
    prohibited = _prohibited_claims()
    allowed = _allowed_claims(
        method_algorithms=method_algorithms,
        system_diagram=system_diagram,
        gate3_audit=gate3_audit,
    )
    draft_audit = _audit_draft(draft_text_path, prohibited)
    return {
        "schema_version": 1,
        "artifact_name": "module2_claim_safety",
        "status": "formal_performance_claims_allowed" if formal_allowed else "blocked_formal_performance_claims",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(repo_root),
        "formal_performance_claim_allowed": formal_allowed,
        "formal_performance_blockers": formal_blockers,
        "inputs": {
            "paper_tables": str(paper_tables_path),
            "h02_formal_acceptance": str(h02_formal_acceptance_path),
            "h01_manifest": str(h01_manifest_path),
            "f02_6_packet": str(f02_6_packet_path),
            "gate3_audit": str(gate3_audit_path),
            "method_algorithms": str(method_algorithms_path),
            "system_diagram": str(system_diagram_path),
            "formal_gate_closure_checklist": str(closure_checklist_path),
            "formal_gate_status_report": str(status_report_path),
            "draft_text": None if draft_text_path is None else str(draft_text_path),
        },
        "input_status": {
            "paper_tables_status": paper_tables.get("status"),
            "paper_tables_formal_claim_allowed": paper_tables.get("formal_claim_allowed"),
            "h02_formal_acceptance_status": h02_formal_acceptance.get("status"),
            "h02_formal_output_accepted": h02_formal_acceptance.get("formal_output_accepted"),
            "h02_paper_result_input_allowed": h02_formal_acceptance.get("paper_result_input_allowed"),
            "h01_manifest_status": h01_manifest.get("status"),
            "f02_6_status": f02_6_packet.get("status"),
            "gate3_formal_decision": gate3_audit.get("formal_decision"),
            "gate3_formal_claim_allowed": gate3_audit.get("formal_claim_allowed"),
            "method_algorithms_status": method_algorithms.get("status"),
            "system_diagram_status": system_diagram.get("status"),
            "closure_checklist_status": closure_checklist.get("status"),
            "closure_checklist_open_item_count": closure_checklist.get("open_item_count"),
            "closure_checklist_input_safety_issue_count": closure_checklist.get("input_safety_issue_count"),
            "status_report_status": status_report.get("status"),
            "status_report_formal_claim_allowed_now": (
                status_report.get("permissions_now", {}).get("formal_claim_allowed_now")
                if isinstance(status_report.get("permissions_now"), dict)
                else None
            ),
            "status_report_input_safety_issue_count": status_report.get("input_safety_issue_count"),
            "status_report_next_blocked_lane_id": _next_blocked_lane_id(status_report),
            "status_report_decision_intake_status": status_report_decision_intake_summary["status"],
            "status_report_decision_intake_record_status": status_report_decision_intake_summary["record_status"],
            "status_report_decision_intake_audit_issue_count": status_report_decision_intake_summary[
                "audit_issue_count"
            ],
            "status_report_decision_intake_decision_owner_required": status_report_decision_intake_summary[
                "decision_owner_required"
            ],
            "status_report_decision_intake_valid_decision_count": status_report_decision_intake_summary[
                "valid_decision_count"
            ],
            "status_report_decision_intake_required_record_field_count": status_report_decision_intake_summary[
                "required_record_field_count"
            ],
            "status_report_decision_intake_decision_note_required": status_report_decision_intake_summary[
                "decision_note_required"
            ],
            "status_report_decision_intake_invalid_input_count": status_report_decision_intake_summary[
                "invalid_input_count"
            ],
            "status_report_decision_intake_post_decision_non_authorization_count": status_report_decision_intake_summary[
                "post_decision_non_authorization_count"
            ],
            "status_report_decision_intake_remote_training_allowed_now": status_report_decision_intake_summary[
                "remote_training_allowed_now"
            ],
            "status_report_decision_intake_formal_claim_allowed_now": status_report_decision_intake_summary[
                "formal_claim_allowed_now"
            ],
            "status_report_handoff_status": status_report_handoff_summary["status"],
            "status_report_transition_gate_status": status_report_handoff_summary["transition_gate_status"],
            "status_report_transition_gate_audit_issue_count": status_report_handoff_summary[
                "transition_gate_audit_issue_count"
            ],
            "status_report_handoff_safety_issue_count": status_report_handoff_summary["safety_issue_count"],
            "status_report_handoff_remote_training_allowed_now": status_report_handoff_summary[
                "remote_training_allowed_now"
            ],
            "status_report_missing_artifacts_handoff_status": status_report_missing_artifacts_handoff_summary["status"],
            "status_report_missing_artifacts_next_action": status_report_missing_artifacts_handoff_summary[
                "next_action_id"
            ],
            "status_report_missing_artifacts_open_requirement_count": status_report_missing_artifacts_handoff_summary[
                "open_requirement_count"
            ],
            "status_report_missing_artifacts_remote_training_allowed_now": status_report_missing_artifacts_handoff_summary[
                "remote_training_allowed_now"
            ],
            "status_report_missing_artifacts_formal_result_material_allowed_now": status_report_missing_artifacts_handoff_summary[
                "formal_result_material_allowed_now"
            ],
            "status_report_requirement_stage_mapped_count": status_report_requirement_stage_summary[
                "mapped_requirement_count"
            ],
            "status_report_requirement_stage_unmapped_count": status_report_requirement_stage_summary[
                "unmapped_requirement_count"
            ],
            "status_report_requirement_stage_mismatched_count": status_report_requirement_stage_summary[
                "mismatched_requirement_count"
            ],
            "status_report_requirement_stage_blocked_stage_count": status_report_requirement_stage_summary[
                "blocked_stage_count"
            ],
            "status_report_closure_remote_training_allowed_now": status_report_remote_gate_summary[
                "closure_remote_stage_summary"
            ]["gate3_remote_training"]["allowed_now"],
            "status_report_remote_packet_training_allowed_now": status_report_remote_gate_summary[
                "remote_execution_step_summary"
            ]["run_remote_training"]["allowed_now"],
            "status_report_remote_preflight_requirement_present": status_report_remote_requirement_summary[
                "remote_preflight_requirement_summary"
            ]["present"],
            "status_report_remote_preflight_requirement_satisfied_count": status_report_remote_requirement_summary[
                "remote_preflight_requirement_summary"
            ]["status_counts"].get("satisfied", 0),
            "status_report_remote_preflight_requirement_blocked_count": status_report_remote_requirement_summary[
                "remote_preflight_requirement_summary"
            ]["blocked_requirement_count"],
            "status_report_post_run_acceptance_requirement_present": status_report_remote_requirement_summary[
                "post_run_acceptance_requirement_summary"
            ]["present"],
            "status_report_post_run_acceptance_requirement_satisfied_count": status_report_remote_requirement_summary[
                "post_run_acceptance_requirement_summary"
            ]["status_counts"].get("satisfied", 0),
            "status_report_post_run_acceptance_requirement_blocked_count": status_report_remote_requirement_summary[
                "post_run_acceptance_requirement_summary"
            ]["blocked_requirement_count"],
            "status_report_h02_formal_acceptance_requirement_present": status_report_h02_acceptance_requirement_summary[
                "present"
            ],
            "status_report_h02_formal_acceptance_requirement_satisfied_count": status_report_h02_acceptance_requirement_summary[
                "status_counts"
            ].get("satisfied", 0),
            "status_report_h02_formal_acceptance_requirement_blocked_count": status_report_h02_acceptance_requirement_summary[
                "blocked_requirement_count"
            ],
            "status_report_remaining_deliverables_acceptance_present": status_report_remaining_deliverables_acceptance_summary[
                "present"
            ],
            "status_report_remaining_deliverables_acceptance_matrix_row_count": status_report_remaining_deliverables_acceptance_summary[
                "matrix_row_count"
            ],
            "status_report_remaining_deliverables_acceptance_missing_row_count": status_report_remaining_deliverables_acceptance_summary[
                "missing_row_count"
            ],
            "status_report_remaining_deliverables_acceptance_blocked_category_count": status_report_remaining_deliverables_acceptance_summary[
                "blocked_category_count"
            ],
            "status_report_remaining_deliverables_gap_present": status_report_remaining_deliverables_gap_summary[
                "present"
            ],
            "status_report_remaining_deliverables_gap_total_missing_deliverables": status_report_remaining_deliverables_gap_summary[
                "total_missing_deliverables"
            ],
            "status_report_remaining_deliverables_gap_open_category_count": status_report_remaining_deliverables_gap_summary[
                "open_category_count"
            ],
        },
        "status_report_handoff_summary": status_report_handoff_summary,
        "status_report_missing_artifacts_handoff_summary": status_report_missing_artifacts_handoff_summary,
        "status_report_requirement_stage_summary": status_report_requirement_stage_summary,
        "status_report_remote_requirement_summary": status_report_remote_requirement_summary,
        "status_report_h02_acceptance_requirement_summary": status_report_h02_acceptance_requirement_summary,
        "status_report_remaining_deliverables_acceptance_summary": status_report_remaining_deliverables_acceptance_summary,
        "status_report_remaining_deliverables_gap_summary": status_report_remaining_deliverables_gap_summary,
        "status_report_decision_intake_summary": status_report_decision_intake_summary,
        "status_report_remote_gate_summary": status_report_remote_gate_summary,
        "allowed_claims": allowed,
        "conditional_claims": _conditional_claims(),
        "prohibited_claims": prohibited,
        "draft_audit": draft_audit,
        "code_anchors": _code_anchors(repo_root),
        "claim_boundaries": [
            "Do not claim formal performance improvement until formal_performance_claim_allowed=true.",
            "No-warm Gate #3 failure is scoped to no-warm PPO only; it does not reject obstacle-summary warm-start.",
            "Method claims must say the learned policy is an analytic-expansion operator inside Hybrid A*, not a standalone global planner.",
            "Completeness/global-optimality/generalization claims are prohibited unless a future contract explicitly proves them.",
            "Formal PPO training/checkpoint production must run on gpu3070ti-relay or another explicitly approved remote GPU.",
            "Formal gate closure checklist must be closed before any formal performance claim is allowed.",
            "Formal gate status report must be ready before any formal performance claim is allowed.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 paper claim safety guard.")
    parser.add_argument("--paper-tables", type=Path, default=DEFAULT_PAPER_TABLES)
    parser.add_argument("--h02-formal-acceptance", type=Path, default=DEFAULT_H02_FORMAL_ACCEPTANCE)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--f02-6-packet", type=Path, default=DEFAULT_F02_6_PACKET)
    parser.add_argument("--gate3-audit", type=Path, default=DEFAULT_GATE3_AUDIT)
    parser.add_argument("--method-algorithms", type=Path, default=DEFAULT_METHOD_ALGORITHMS)
    parser.add_argument("--system-diagram", type=Path, default=DEFAULT_SYSTEM_DIAGRAM)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--draft-text", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _formal_performance_blockers(
    *,
    paper_tables: dict[str, Any],
    h02_formal_acceptance: dict[str, Any],
    h01_manifest: dict[str, Any],
    f02_6_packet: dict[str, Any],
    closure_checklist: dict[str, Any],
    status_report: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if paper_tables.get("formal_claim_allowed") is not True:
        blockers.append("paper_tables_not_formal")
    for blocker in paper_tables.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if h02_formal_acceptance.get("formal_output_accepted") is not True or h02_formal_acceptance.get("paper_result_input_allowed") is not True:
        _append_unique(blockers, "h02_formal_acceptance_not_accepted")
    for blocker in h02_formal_acceptance.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if str(h01_manifest.get("status")) not in {"ready", "formal_ready", "ready_for_formal_run", "ready_for_formal_evaluation"}:
        _append_unique(blockers, "h01_manifest_not_ready")
    for blocker in h01_manifest.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if str(f02_6_packet.get("status")) == "pending_human_decision":
        _append_unique(blockers, "f02_6_pending")
    for blocker in f02_6_packet.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if closure_checklist.get("status") != "formal_gate_closure_ready_for_result_audit":
        _append_unique(blockers, "formal_gate_closure_checklist_open")
    if closure_checklist.get("executes_commands") is not False:
        _append_unique(blockers, "closure_checklist_executes_commands")
    if closure_checklist.get("runs_training") is not False:
        _append_unique(blockers, "closure_checklist_runs_training")
    if closure_checklist.get("runs_remote_preflight") is not False:
        _append_unique(blockers, "closure_checklist_runs_remote_preflight")
    if closure_checklist.get("local_training_allowed") is not False:
        _append_unique(blockers, "closure_checklist_allows_local_training")
    if closure_checklist.get("formal_claim_allowed") is not False:
        _append_unique(blockers, "closure_checklist_allows_formal_claim")
    if int(closure_checklist.get("input_safety_issue_count") or 0) > 0:
        _append_unique(blockers, "closure_checklist_input_safety_issues_open")
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
        _append_unique(blockers, "formal_gate_status_report_blocked")
    if status_report.get("executes_commands") is not False:
        _append_unique(blockers, "status_report_executes_commands")
    if status_report.get("runs_training") is not False:
        _append_unique(blockers, "status_report_runs_training")
    if status_report.get("runs_remote_preflight") is not False:
        _append_unique(blockers, "status_report_runs_remote_preflight")
    if status_report.get("local_training_allowed") is not False:
        _append_unique(blockers, "status_report_allows_local_training")
    if status_report.get("formal_claim_allowed") is not False:
        _append_unique(blockers, "status_report_allows_formal_claim")
    if permissions.get("local_training_allowed_now") is True:
        _append_unique(blockers, "status_report_allows_local_training_now")
    if int(status_report.get("input_safety_issue_count") or 0) > 0:
        _append_unique(blockers, "status_report_input_safety_issues_open")
    blockers.extend(_status_report_handoff_blockers(status_report))
    blockers.extend(_status_report_missing_artifacts_handoff_blockers(status_report))
    blockers.extend(_status_report_requirement_stage_blockers(status_report))
    blockers.extend(_status_report_remote_requirement_blockers(status_report))
    blockers.extend(_status_report_h02_acceptance_requirement_blockers(status_report))
    blockers.extend(_status_report_remaining_deliverables_acceptance_blockers(status_report))
    blockers.extend(_status_report_decision_intake_blockers(status_report))
    blockers.extend(_status_report_remote_summary_blockers(status_report))
    return blockers


def _status_report_handoff_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = status_report.get("formal_gate_handoff_summary")
    if not isinstance(summary, dict):
        summary = {}
    return {
        "present": bool(summary),
        "status": summary.get("status"),
        "transition_gate_status": summary.get("transition_gate_status"),
        "transition_gate_audit_issue_count": summary.get("transition_gate_audit_issue_count"),
        "safety_issue_count": int(summary.get("safety_issue_count") or 0),
        "remote_training_allowed_now": summary.get("remote_training_allowed_now")
        if isinstance(summary.get("remote_training_allowed_now"), bool)
        else None,
        "remote_preflight_allowed_now": summary.get("remote_preflight_allowed_now")
        if isinstance(summary.get("remote_preflight_allowed_now"), bool)
        else None,
        "formal_claim_allowed_now": summary.get("formal_claim_allowed_now")
        if isinstance(summary.get("formal_claim_allowed_now"), bool)
        else None,
    }


def _status_report_decision_intake_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = status_report.get("f02_6_decision_intake_summary")
    if not isinstance(summary, dict):
        summary = {}
    valid_decisions = _string_list(summary.get("valid_decisions"))
    required_fields = _string_list(summary.get("required_record_fields"))
    return {
        "present": bool(summary),
        "status": summary.get("status"),
        "audit_issue_count": int(summary.get("audit_issue_count") or 0),
        "record_status": summary.get("record_status"),
        "record_decider": summary.get("record_decider"),
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "decision_owner_required": summary.get("decision_owner_required"),
        "valid_decisions": valid_decisions,
        "valid_decision_count": int(summary.get("valid_decision_count") or len(valid_decisions)),
        "required_record_fields": required_fields,
        "required_record_field_count": int(summary.get("required_record_field_count") or len(required_fields)),
        "decision_note_required": bool(summary.get("decision_note_required")),
        "invalid_input_count": int(summary.get("invalid_input_count") or 0),
        "post_decision_non_authorization_count": int(summary.get("post_decision_non_authorization_count") or 0),
        "remote_preflight_allowed_now": summary.get("remote_preflight_allowed_now")
        if isinstance(summary.get("remote_preflight_allowed_now"), bool)
        else None,
        "remote_training_allowed_now": summary.get("remote_training_allowed_now")
        if isinstance(summary.get("remote_training_allowed_now"), bool)
        else None,
        "formal_claim_allowed_now": summary.get("formal_claim_allowed_now")
        if isinstance(summary.get("formal_claim_allowed_now"), bool)
        else None,
    }


def _status_report_decision_intake_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_decision_intake_summary(status_report)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("status_report_missing_f02_6_decision_intake_summary")
        return blockers
    if summary["status"] not in {"f02_6_decision_intake_pending_clean", "f02_6_decision_intake_closed_clean"}:
        blockers.append("status_report_f02_6_decision_intake_not_clean")
    if summary["audit_issue_count"] > 0:
        blockers.append("status_report_f02_6_decision_intake_audit_issues_open")
    if summary["decision_owner_required"] != "Dr Sun":
        blockers.append("status_report_f02_6_decision_intake_decision_owner_not_dr_sun")
    expected_decisions = {"approve_obstacle_summary_warm_start", "reject_obstacle_summary_warm_start"}
    if not expected_decisions.issubset(set(summary["valid_decisions"])):
        blockers.append("status_report_f02_6_decision_intake_valid_decisions_incomplete")
    expected_fields = {"decision", "decider", "decision_note"}
    if not expected_fields.issubset(set(summary["required_record_fields"])):
        blockers.append("status_report_f02_6_decision_intake_required_fields_incomplete")
    if not summary["decision_note_required"]:
        blockers.append("status_report_f02_6_decision_intake_decision_note_not_required")
    if summary["invalid_input_count"] == 0:
        blockers.append("status_report_f02_6_decision_intake_invalid_inputs_missing")
    if summary["post_decision_non_authorization_count"] == 0:
        blockers.append("status_report_f02_6_decision_intake_non_authorizations_missing")
    if summary["record_status"] == "pending_human_decision":
        if summary["next_blocked_lane"] != "decision":
            blockers.append("status_report_pending_f02_6_intake_next_lane_not_decision")
        if summary["remote_preflight_allowed_now"] is not False:
            blockers.append("status_report_pending_f02_6_intake_allows_remote_preflight")
        if summary["remote_training_allowed_now"] is not False:
            blockers.append("status_report_pending_f02_6_intake_allows_remote_training")
        if summary["formal_claim_allowed_now"] is not False:
            blockers.append("status_report_pending_f02_6_intake_allows_formal_claim")
    elif summary["record_status"] in {"approved", "rejected"}:
        if summary["record_decider"] != "Dr Sun":
            blockers.append("status_report_closed_f02_6_intake_decider_not_dr_sun")
    else:
        blockers.append("status_report_f02_6_decision_intake_unknown_record_status")
    return blockers


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _status_report_handoff_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_handoff_summary(status_report)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("status_report_missing_formal_gate_handoff_summary")
        return blockers
    if summary["transition_gate_status"] != "f02_6_transition_gate_audit_passed":
        blockers.append("status_report_transition_gate_not_passed")
    if int(summary["transition_gate_audit_issue_count"] or 0) > 0:
        blockers.append("status_report_transition_gate_issues_open")
    if int(summary["safety_issue_count"] or 0) > 0:
        blockers.append("status_report_handoff_safety_issues_open")
    if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
        if summary["remote_preflight_allowed_now"] is True:
            blockers.append("status_report_blocked_but_handoff_remote_preflight_allowed")
        if summary["remote_training_allowed_now"] is True:
            blockers.append("status_report_blocked_but_handoff_remote_training_allowed")
        if summary["formal_claim_allowed_now"] is True:
            blockers.append("status_report_blocked_but_handoff_formal_claim_allowed")
    return blockers


def _status_report_missing_artifacts_handoff_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = status_report.get("missing_artifacts_handoff_index_summary")
    if not isinstance(summary, dict):
        summary = {}
    return {
        "present": bool(summary),
        "status": summary.get("status"),
        "next_action_id": summary.get("next_action_id"),
        "next_action_requires_dr_sun": summary.get("next_action_requires_dr_sun"),
        "open_requirement_count": summary.get("open_requirement_count"),
        "local_training_allowed_now": summary.get("local_training_allowed_now")
        if isinstance(summary.get("local_training_allowed_now"), bool)
        else None,
        "remote_training_allowed_now": summary.get("remote_training_allowed_now")
        if isinstance(summary.get("remote_training_allowed_now"), bool)
        else None,
        "formal_result_material_allowed_now": summary.get("formal_result_material_allowed_now")
        if isinstance(summary.get("formal_result_material_allowed_now"), bool)
        else None,
    }


def _status_report_missing_artifacts_handoff_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_missing_artifacts_handoff_summary(status_report)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("status_report_missing_artifacts_handoff_index_missing")
        return blockers
    if summary["local_training_allowed_now"] is True:
        blockers.append("status_report_missing_artifacts_handoff_allows_local_training")
    if summary["formal_result_material_allowed_now"] is True:
        blockers.append("status_report_missing_artifacts_handoff_allows_result_material")
    if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
        if summary["remote_training_allowed_now"] is True:
            blockers.append("status_report_blocked_but_missing_artifacts_handoff_remote_training_allowed")
    else:
        if summary["status"] != "formal_gate_evidence_ready_for_h01_h02_claim_gates":
            blockers.append("status_report_ready_but_missing_artifacts_handoff_not_clear")
        if int(summary["open_requirement_count"] or 0) > 0:
            blockers.append("status_report_ready_but_missing_artifacts_handoff_requirements_open")
    return blockers


def _status_report_requirement_stage_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = status_report.get("formal_gate_requirement_stage_summary")
    summary = summary if isinstance(summary, dict) else {}
    raw_requirements = summary.get("requirements") if isinstance(summary.get("requirements"), dict) else {}
    requirements: dict[str, dict[str, Any]] = {}
    for requirement_id in STATUS_REPORT_REQUIREMENT_IDS:
        row = raw_requirements.get(requirement_id) if isinstance(raw_requirements.get(requirement_id), dict) else {}
        stage_blockers = row.get("responsible_stage_blocked_by")
        requirements[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "expected_stage_id": row.get("expected_stage_id"),
            "responsible_stage_id": row.get("responsible_stage_id"),
            "responsible_stage_status": row.get("responsible_stage_status"),
            "responsible_stage_allowed_now": row.get("responsible_stage_allowed_now")
            if isinstance(row.get("responsible_stage_allowed_now"), bool)
            else None,
            "responsible_stage_blocked_by": [str(value) for value in stage_blockers if value]
            if isinstance(stage_blockers, list)
            else [],
            "mapping_present": row.get("mapping_present") if isinstance(row.get("mapping_present"), bool) else None,
            "mapping_matches_expected": row.get("mapping_matches_expected")
            if isinstance(row.get("mapping_matches_expected"), bool)
            else None,
        }
    return {
        "present": bool(summary),
        "mapped_requirement_count": int(summary.get("mapped_requirement_count") or 0),
        "unmapped_requirement_count": int(summary.get("unmapped_requirement_count") or 0),
        "mismatched_requirement_count": int(summary.get("mismatched_requirement_count") or 0),
        "blocked_stage_count": int(summary.get("blocked_stage_count") or 0),
        "unmapped_requirement_ids": [str(value) for value in summary.get("unmapped_requirement_ids", []) if value]
        if isinstance(summary.get("unmapped_requirement_ids"), list)
        else [],
        "mismatched_requirement_ids": [
            str(value) for value in summary.get("mismatched_requirement_ids", []) if value
        ]
        if isinstance(summary.get("mismatched_requirement_ids"), list)
        else [],
        "requirements": requirements,
    }


def _status_report_requirement_stage_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_requirement_stage_summary(status_report)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("status_report_missing_requirement_stage_summary")
        return blockers
    if summary["unmapped_requirement_count"] > 0:
        blockers.append("status_report_requirement_stage_unmapped")
    if summary["mismatched_requirement_count"] > 0:
        blockers.append("status_report_requirement_stage_mismatched")
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            _append_unique(blockers, f"status_report_requirement_stage_missing_{requirement_id}")
            continue
        if row["mapping_present"] is not True:
            _append_unique(blockers, f"status_report_{requirement_id}_missing_responsible_stage")
        if row["mapping_matches_expected"] is not True:
            _append_unique(blockers, f"status_report_{requirement_id}_wrong_responsible_stage")
        if row["responsible_stage_allowed_now"] is False and not row["responsible_stage_blocked_by"]:
            _append_unique(blockers, f"status_report_{requirement_id}_responsible_stage_missing_blocked_by")
        if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
            if row["responsible_stage_allowed_now"] is True:
                _append_unique(blockers, f"status_report_blocked_but_{requirement_id}_responsible_stage_allowed")
    return blockers


def _status_report_remote_gate_summary(status_report: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    return {
        "closure_remote_stage_summary": _summary_items(
            status_report.get("closure_remote_stage_summary"),
            STATUS_REPORT_CLOSURE_STAGE_IDS,
        ),
        "remote_execution_step_summary": _summary_items(
            status_report.get("remote_execution_step_summary"),
            STATUS_REPORT_REMOTE_STEP_IDS,
        ),
    }


def _status_report_remote_requirement_summary(status_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "remote_preflight_requirement_summary": _remote_requirement_matrix_summary(
            status_report=status_report,
            summary_key="remote_preflight_requirement_summary",
            required_ids=STATUS_REPORT_REMOTE_PREFLIGHT_REQUIREMENT_IDS,
        ),
        "post_run_acceptance_requirement_summary": _remote_requirement_matrix_summary(
            status_report=status_report,
            summary_key="post_run_acceptance_requirement_summary",
            required_ids=STATUS_REPORT_POST_RUN_ACCEPTANCE_REQUIREMENT_IDS,
        ),
    }


def _remote_requirement_matrix_summary(
    *,
    status_report: dict[str, Any],
    summary_key: str,
    required_ids: Sequence[str],
) -> dict[str, Any]:
    summary = status_report.get(summary_key)
    summary = summary if isinstance(summary, dict) else {}
    raw_requirements = summary.get("requirements") if isinstance(summary.get("requirements"), dict) else {}
    requirements: dict[str, dict[str, Any]] = {}
    for requirement_id in required_ids:
        row = raw_requirements.get(requirement_id) if isinstance(raw_requirements.get(requirement_id), dict) else {}
        requirements[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "phase": row.get("phase"),
            "complete": row.get("complete") if isinstance(row.get("complete"), bool) else None,
            "execution_allowed_now": row.get("execution_allowed_now")
            if isinstance(row.get("execution_allowed_now"), bool)
            else None,
            "remote_training_ready_now": row.get("remote_training_ready_now")
            if isinstance(row.get("remote_training_ready_now"), bool)
            else None,
            "missing_artifact_ids": _strings(row.get("missing_artifact_ids")),
            "blocked_by": _strings(row.get("blocked_by")),
            "acceptable_evidence_count": int(row.get("acceptable_evidence_count") or 0),
            "invalid_substitute_count": int(row.get("invalid_substitute_count") or 0),
        }
    status_counts = summary.get("status_counts") if isinstance(summary.get("status_counts"), dict) else {}
    return {
        "present": bool(summary),
        "required_requirement_count": int(summary.get("required_requirement_count") or len(required_ids)),
        "present_requirement_count": int(summary.get("present_requirement_count") or 0),
        "blocked_requirement_count": int(summary.get("blocked_requirement_count") or 0),
        "status_counts": {str(key): int(value or 0) for key, value in status_counts.items()},
        "missing_requirement_ids": _strings(summary.get("missing_requirement_ids")),
        "requirements": requirements,
    }


def _status_report_remote_requirement_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_remote_requirement_summary(status_report)
    blockers: list[str] = []
    blockers.extend(
        _remote_requirement_matrix_blockers(
            status_report=status_report,
            summary=summary["remote_preflight_requirement_summary"],
            prefix="status_report_remote_preflight_requirement",
            required_ids=STATUS_REPORT_REMOTE_PREFLIGHT_REQUIREMENT_IDS,
        )
    )
    blockers.extend(
        _remote_requirement_matrix_blockers(
            status_report=status_report,
            summary=summary["post_run_acceptance_requirement_summary"],
            prefix="status_report_post_run_acceptance_requirement",
            required_ids=STATUS_REPORT_POST_RUN_ACCEPTANCE_REQUIREMENT_IDS,
        )
    )
    return blockers


def _status_report_h02_acceptance_requirement_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = status_report.get("h02_formal_acceptance_requirement_summary")
    summary = summary if isinstance(summary, dict) else {}
    raw_requirements = summary.get("requirements") if isinstance(summary.get("requirements"), dict) else {}
    requirements: dict[str, dict[str, Any]] = {}
    for requirement_id in STATUS_REPORT_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS:
        row = raw_requirements.get(requirement_id) if isinstance(raw_requirements.get(requirement_id), dict) else {}
        requirements[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "phase": row.get("phase"),
            "complete": row.get("complete") if isinstance(row.get("complete"), bool) else None,
            "paper_result_input_allowed_now": row.get("paper_result_input_allowed_now")
            if isinstance(row.get("paper_result_input_allowed_now"), bool)
            else None,
            "missing_artifact_ids": _strings(row.get("missing_artifact_ids")),
            "acceptable_evidence_count": int(row.get("acceptable_evidence_count") or 0),
            "invalid_substitute_count": int(row.get("invalid_substitute_count") or 0),
        }
    status_counts = summary.get("status_counts") if isinstance(summary.get("status_counts"), dict) else {}
    return {
        "present": bool(summary),
        "required_requirement_count": int(
            summary.get("required_requirement_count") or len(STATUS_REPORT_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS)
        ),
        "present_requirement_count": int(summary.get("present_requirement_count") or 0),
        "blocked_requirement_count": int(summary.get("blocked_requirement_count") or 0),
        "status_counts": {str(key): int(value or 0) for key, value in status_counts.items()},
        "missing_requirement_ids": _strings(summary.get("missing_requirement_ids")),
        "requirements": requirements,
    }


def _status_report_h02_acceptance_requirement_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_h02_acceptance_requirement_summary(status_report)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("status_report_h02_formal_acceptance_requirement_summary_missing")
        return blockers
    if int(summary["required_requirement_count"] or 0) != len(STATUS_REPORT_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS):
        blockers.append("status_report_h02_formal_acceptance_requirement_required_count_mismatch")
    for requirement_id in summary["missing_requirement_ids"]:
        _append_unique(blockers, f"status_report_h02_formal_acceptance_requirement_missing_{requirement_id}")
    if status_report.get("status") == "formal_gate_status_ready_for_claim_audit" and int(summary["blocked_requirement_count"] or 0) > 0:
        blockers.append("status_report_h02_formal_acceptance_requirement_blocked_while_status_ready")
    blocked_status = status_report.get("status") != "formal_gate_status_ready_for_claim_audit"
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            _append_unique(blockers, f"status_report_h02_formal_acceptance_requirement_missing_{requirement_id}")
            continue
        if int(row["acceptable_evidence_count"] or 0) <= 0:
            _append_unique(
                blockers,
                f"status_report_h02_formal_acceptance_requirement_{requirement_id}_missing_acceptable_evidence",
            )
        if int(row["invalid_substitute_count"] or 0) <= 0:
            _append_unique(
                blockers,
                f"status_report_h02_formal_acceptance_requirement_{requirement_id}_missing_invalid_substitutes",
            )
        if blocked_status and row["paper_result_input_allowed_now"] is True:
            _append_unique(
                blockers,
                f"status_report_h02_formal_acceptance_requirement_{requirement_id}_allows_paper_result_while_status_blocked",
            )
        if row["complete"] is True and row["status"] != "satisfied":
            _append_unique(
                blockers,
                f"status_report_h02_formal_acceptance_requirement_{requirement_id}_complete_not_satisfied",
            )
        if row["status"] == "satisfied" and row["missing_artifact_ids"]:
            _append_unique(
                blockers,
                f"status_report_h02_formal_acceptance_requirement_{requirement_id}_satisfied_with_missing_artifacts",
            )
    return blockers


def _status_report_remaining_deliverables_acceptance_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = status_report.get("remaining_deliverables_acceptance_summary")
    summary = summary if isinstance(summary, dict) else {}
    raw_rows = summary.get("rows") if isinstance(summary.get("rows"), dict) else {}
    rows: dict[str, dict[str, Any]] = {}
    for matrix_id in STATUS_REPORT_REMAINING_DELIVERABLE_MATRIX_IDS:
        row = raw_rows.get(matrix_id) if isinstance(raw_rows.get(matrix_id), dict) else {}
        rows[matrix_id] = {
            "present": bool(row),
            "missing": row.get("missing") if isinstance(row.get("missing"), bool) else None,
            "responsible_stage_id": row.get("responsible_stage_id"),
            "responsible_stage_allowed_now": row.get("responsible_stage_allowed_now")
            if isinstance(row.get("responsible_stage_allowed_now"), bool)
            else None,
            "acceptance_predicate_count": int(row.get("acceptance_predicate_count") or 0),
            "invalid_substitute_count": int(row.get("invalid_substitute_count") or 0),
        }
    return {
        "present": bool(summary),
        "status": summary.get("status"),
        "missing_deliverable_count": int(summary.get("missing_deliverable_count") or 0),
        "matrix_row_count": int(summary.get("matrix_row_count") or 0),
        "expected_matrix_row_count": int(
            summary.get("expected_matrix_row_count") or len(STATUS_REPORT_REMAINING_DELIVERABLE_MATRIX_IDS)
        ),
        "missing_row_count": int(summary.get("missing_row_count") or 0),
        "blocked_category_count": int(summary.get("blocked_category_count") or 0),
        "missing_expected_matrix_ids": _strings(summary.get("missing_expected_matrix_ids")),
        "rows": rows,
    }


def _status_report_remaining_deliverables_acceptance_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_remaining_deliverables_acceptance_summary(status_report)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("status_report_missing_remaining_deliverables_acceptance_summary")
        return blockers
    if summary["matrix_row_count"] != len(STATUS_REPORT_REMAINING_DELIVERABLE_MATRIX_IDS):
        blockers.append("status_report_remaining_deliverables_acceptance_matrix_count_mismatch")
    for matrix_id in summary["missing_expected_matrix_ids"]:
        _append_unique(blockers, f"status_report_remaining_deliverables_acceptance_missing_{matrix_id.replace(':', '_')}")
    if status_report.get("status") == "formal_gate_status_ready_for_claim_audit":
        if summary["missing_row_count"] > 0:
            blockers.append("status_report_remaining_deliverables_missing_rows_while_status_ready")
        if summary["blocked_category_count"] > 0:
            blockers.append("status_report_remaining_deliverables_blocked_categories_while_status_ready")
    for matrix_id, row in summary["rows"].items():
        safe_matrix_id = matrix_id.replace(":", "_")
        if not row["present"]:
            _append_unique(blockers, f"status_report_remaining_deliverables_acceptance_missing_{safe_matrix_id}")
            continue
        if row["acceptance_predicate_count"] <= 0:
            _append_unique(blockers, f"status_report_remaining_deliverables_acceptance_{safe_matrix_id}_missing_predicates")
        if row["invalid_substitute_count"] <= 0:
            _append_unique(blockers, f"status_report_remaining_deliverables_acceptance_{safe_matrix_id}_missing_invalid_substitutes")
        if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
            if row["responsible_stage_allowed_now"] is True:
                _append_unique(blockers, f"status_report_remaining_deliverables_acceptance_{safe_matrix_id}_stage_allowed_while_blocked")
    return blockers


def _remote_requirement_matrix_blockers(
    *,
    status_report: dict[str, Any],
    summary: dict[str, Any],
    prefix: str,
    required_ids: Sequence[str],
) -> list[str]:
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append(f"{prefix}_summary_missing")
        return blockers
    if int(summary["required_requirement_count"] or 0) != len(required_ids):
        blockers.append(f"{prefix}_required_count_mismatch")
    for requirement_id in summary["missing_requirement_ids"]:
        _append_unique(blockers, f"{prefix}_missing_{requirement_id}")
    if status_report.get("status") == "formal_gate_status_ready_for_claim_audit" and int(summary["blocked_requirement_count"] or 0) > 0:
        blockers.append(f"{prefix}_blocked_while_status_ready")
    blocked_status = status_report.get("status") != "formal_gate_status_ready_for_claim_audit"
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            _append_unique(blockers, f"{prefix}_missing_{requirement_id}")
            continue
        if int(row["acceptable_evidence_count"] or 0) <= 0:
            _append_unique(blockers, f"{prefix}_{requirement_id}_missing_acceptable_evidence")
        if int(row["invalid_substitute_count"] or 0) <= 0:
            _append_unique(blockers, f"{prefix}_{requirement_id}_missing_invalid_substitutes")
        if blocked_status and row["execution_allowed_now"] is True:
            _append_unique(blockers, f"{prefix}_{requirement_id}_allowed_while_status_blocked")
        if row["complete"] is True and row["status"] != "satisfied":
            _append_unique(blockers, f"{prefix}_{requirement_id}_complete_not_satisfied")
        if row["status"] == "satisfied" and row["missing_artifact_ids"]:
            _append_unique(blockers, f"{prefix}_{requirement_id}_satisfied_with_missing_artifacts")
    return blockers


def _summary_items(raw: Any, item_ids: Sequence[str]) -> dict[str, dict[str, Any]]:
    items = raw if isinstance(raw, dict) else {}
    out: dict[str, dict[str, Any]] = {}
    for item_id in item_ids:
        item = items.get(item_id) if isinstance(items.get(item_id), dict) else {}
        blocked_by = item.get("blocked_by")
        out[item_id] = {
            "present": bool(item),
            "status": item.get("status"),
            "allowed_now": item.get("allowed_now") if isinstance(item.get("allowed_now"), bool) else None,
            "runs_training": item.get("runs_training") if isinstance(item.get("runs_training"), bool) else None,
            "runs_remote_preflight": item.get("runs_remote_preflight") if isinstance(item.get("runs_remote_preflight"), bool) else None,
            "host": item.get("host"),
            "blocked_by": [str(value) for value in blocked_by if value] if isinstance(blocked_by, list) else [],
        }
    return out


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _status_report_remote_summary_blockers(status_report: dict[str, Any]) -> list[str]:
    summary = _status_report_remote_gate_summary(status_report)
    blockers: list[str] = []
    closure_raw = status_report.get("closure_remote_stage_summary")
    remote_raw = status_report.get("remote_execution_step_summary")
    if not isinstance(closure_raw, dict):
        blockers.append("status_report_missing_closure_remote_stage_summary")
    if not isinstance(remote_raw, dict):
        blockers.append("status_report_missing_remote_execution_step_summary")
    for group_id, group in summary.items():
        for item_id, item in group.items():
            if not item["present"]:
                _append_unique(blockers, f"status_report_missing_{item_id}")
                continue
            if item["allowed_now"] is False and not item["blocked_by"]:
                _append_unique(blockers, f"status_report_{item_id}_missing_blocked_by")
            if status_report.get("status") != "formal_gate_status_ready_for_claim_audit" and item["allowed_now"] is True:
                _append_unique(blockers, f"status_report_blocked_but_{item_id}_allowed")
    closure_training = summary["closure_remote_stage_summary"].get("gate3_remote_training", {})
    if closure_training.get("runs_training") is not True:
        _append_unique(blockers, "status_report_closure_training_stage_not_marked_training")
    remote_training = summary["remote_execution_step_summary"].get("run_remote_training", {})
    if remote_training.get("runs_training") is not True:
        _append_unique(blockers, "status_report_remote_training_step_not_marked_training")
    return blockers


def _next_blocked_lane_id(status_report: dict[str, Any]) -> str | None:
    lane = status_report.get("next_blocked_lane")
    if not isinstance(lane, dict):
        return None
    value = lane.get("lane_id")
    return str(value) if value else None


def _allowed_claims(*, method_algorithms: dict[str, Any], system_diagram: dict[str, Any], gate3_audit: dict[str, Any]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    if method_algorithms.get("status") == "code_anchored" and system_diagram.get("status") == "code_anchored_drawio":
        claims.append(
            {
                "claim_id": "method_is_ha_star_analytic_operator",
                "scope": "method_structure",
                "claim_text": "Module2 implements a learned analytic-expansion operator inside Hybrid A*, with terminal RS certification and primitive fallback.",
                "required_qualifier": "Do not describe it as an end-to-end RL global planner.",
                "evidence": [
                    "0_trials/module2_method_algorithms/module2_method_algorithms.json",
                    "0_trials/module2_system_diagram/module2_system_diagram.json",
                ],
            }
        )
    if gate3_audit.get("formal_claim_allowed") is True and str(gate3_audit.get("formal_decision")) == "fail":
        rate = gate3_audit.get("terminal_rs_success_rate")
        episodes = gate3_audit.get("episodes")
        threshold = gate3_audit.get("success_threshold") or gate3_audit.get("required_success_threshold")
        claims.append(
            {
                "claim_id": "no_warm_gate3_formal_failure",
                "scope": "no_warm_only",
                "claim_text": f"No-warm PPO Gate #3 formal trial failed: terminal-RS success rate was {rate} over {episodes} episodes, below threshold {threshold}.",
                "required_qualifier": "This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction.",
                "evidence": ["0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json"],
            }
        )
    return claims


def _conditional_claims() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "formal_performance_improvement",
            "status": "blocked_until_formal_h02",
            "template": "On the approved procedural and real-map evaluation suite, RL-RS funnel reduces expansions/time/timeout relative to Dang multi-RS.",
            "required_evidence": [
                "H02 formal_acceptance=true",
                "H02 formal acceptance artifact has formal_output_accepted=true and paper_result_input_allowed=true",
                "H01 manifest ready/formal_ready",
                "real PPO checkpoint rows present",
                "paired Wilcoxon p<0.05 for total_time_s and total_expansions",
                "bootstrap CI for success/failure/timeout-rate differences",
            ],
        },
        {
            "claim_id": "warm_start_effect",
            "status": "blocked_until_f02_6_and_remote_formal",
            "template": "Obstacle-summary BC warm-start improves PPO analytic operator reliability.",
            "required_evidence": [
                "F02.6 approved by Dr Sun",
                "warm-start formal PPO run on gpu3070ti-relay",
                "formal audit without smoke blockers",
            ],
        },
    ]


def _prohibited_claims() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "global_optimality",
            "severity": "hard_block",
            "patterns": ["全局最优", "globally optimal", "global optimality"],
            "reason": "Current contract and evaluation do not prove global optimality.",
        },
        {
            "claim_id": "completeness_enhancement",
            "severity": "hard_block",
            "patterns": ["完备性增强", "提高完备性", "completeness enhancement", "improves completeness"],
            "reason": "The allowed claim is fallback safety semantics, not completeness improvement.",
        },
        {
            "claim_id": "rl_replaces_hybrid_astar",
            "severity": "hard_block",
            "patterns": ["RL 替代 Hybrid A*", "RL replaces Hybrid A*", "replace Hybrid A*", "替代 Hybrid A*"],
            "reason": "The learned policy is only an analytic-expansion operator inside Hybrid A*.",
        },
        {
            "claim_id": "universal_generalization",
            "severity": "hard_block",
            "patterns": ["泛化到所有森林", "all forest environments", "universal generalization", "generalizes to all"],
            "reason": "Current protocol is scoped to specified procedural and real-map evaluations.",
        },
        {
            "claim_id": "warm_start_approved",
            "severity": "hard_block",
            "patterns": ["warm-start approved", "热启动已批准", "obstacle-summary warm-start is approved"],
            "reason": "F02.6 remains pending until Dr Sun explicitly approves or rejects.",
        },
    ]


def _audit_draft(draft_text_path: Path | None, prohibited_claims: Sequence[dict[str, Any]]) -> dict[str, Any]:
    if draft_text_path is None:
        return {"status": "not_requested", "draft_text": None, "violations": []}
    text = Path(draft_text_path).read_text(encoding="utf-8")
    lower = text.lower()
    violations: list[dict[str, Any]] = []
    for claim in prohibited_claims:
        matched = [pattern for pattern in claim["patterns"] if pattern.lower() in lower]
        if matched:
            violations.append(
                {
                    "claim_id": claim["claim_id"],
                    "severity": claim["severity"],
                    "matched_patterns": matched,
                    "reason": claim["reason"],
                }
            )
    return {
        "status": "violations_found" if violations else "clean",
        "draft_text": str(draft_text_path),
        "violations": violations,
    }


def _code_anchors(repo_root: Path) -> list[dict[str, Any]]:
    return [
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_paper_tables.py", "formal_claim_allowed = not blockers", "paper_table_formal_gate"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_h02_formal_acceptance.py", '"formal_output_accepted": accepted', "h02_formal_acceptance_gate"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py", "f02_6_decision_packet_pending", "h01_f02_6_guard"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py", '"formal_claim_allowed": formal_decision in {"pass", "fail"}', "gate3_formal_claim_gate"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_method_algorithms.py", "The learned component is an analytic-expansion operator", "method_claim_boundary"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_system_diagram.py", "not a standalone RL planner", "system_diagram_claim_boundary"),
    ]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _anchor(repo_root: Path, path: str, pattern: str, symbol: str) -> dict[str, Any]:
    lines = (repo_root / path).read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        if pattern in line:
            return {"path": path, "line": index, "symbol": symbol, "pattern": pattern}
    raise RuntimeError(f"Could not find pattern {pattern!r} in {path}")


def _source_head(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - provenance is best-effort for generated artifacts.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Claim Safety",
        "",
        f"- Status: `{manifest['status']}`",
        f"- Formal performance claim allowed: `{manifest['formal_performance_claim_allowed']}`",
        "",
        "## Formal Performance Blockers",
        "",
    ]
    if manifest["formal_performance_blockers"]:
        for blocker in manifest["formal_performance_blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")
    lines.extend(["", "## Allowed Claims", ""])
    for claim in manifest["allowed_claims"]:
        lines.append(f"- `{claim['claim_id']}` ({claim['scope']}): {claim['claim_text']}")
        lines.append(f"  - qualifier: {claim['required_qualifier']}")
    lines.extend(["", "## Conditional Claims", ""])
    for claim in manifest["conditional_claims"]:
        lines.append(f"- `{claim['claim_id']}`: {claim['status']}")
    lines.extend(["", "## Status Report Handoff Summary", ""])
    handoff = manifest["status_report_handoff_summary"]
    lines.append(
        f"- present=`{handoff['present']}`, status=`{handoff['status']}`, "
        f"transition_gate_status=`{handoff['transition_gate_status']}`, "
        f"transition_gate_audit_issue_count=`{handoff['transition_gate_audit_issue_count']}`, "
        f"safety_issue_count=`{handoff['safety_issue_count']}`, "
        f"remote_training_allowed_now=`{handoff['remote_training_allowed_now']}`"
    )
    lines.extend(["", "## F02.6 Decision Intake Summary", ""])
    intake = manifest["status_report_decision_intake_summary"]
    lines.append(
        f"- present=`{intake['present']}`, status=`{intake['status']}`, "
        f"record_status=`{intake['record_status']}`, record_decider=`{intake['record_decider']}`, "
        f"next_blocked_lane=`{intake['next_blocked_lane']}`, "
        f"audit_issue_count=`{intake['audit_issue_count']}`, "
        f"decision_owner_required=`{intake['decision_owner_required']}`, "
        f"valid_decision_count=`{intake['valid_decision_count']}`, "
        f"required_record_field_count=`{intake['required_record_field_count']}`, "
        f"decision_note_required=`{intake['decision_note_required']}`, "
        f"invalid_input_count=`{intake['invalid_input_count']}`, "
        f"post_decision_non_authorization_count=`{intake['post_decision_non_authorization_count']}`, "
        f"remote_training_allowed_now=`{intake['remote_training_allowed_now']}`, "
        f"formal_claim_allowed_now=`{intake['formal_claim_allowed_now']}`"
    )
    lines.extend(["", "## Status Report Missing-Artifacts Handoff Index", ""])
    missing_handoff = manifest["status_report_missing_artifacts_handoff_summary"]
    lines.append(
        f"- present=`{missing_handoff['present']}`, status=`{missing_handoff['status']}`, "
        f"next_action=`{missing_handoff['next_action_id']}`, "
        f"open_requirement_count=`{missing_handoff['open_requirement_count']}`, "
        f"remote_training_allowed_now=`{missing_handoff['remote_training_allowed_now']}`, "
        f"formal_result_material_allowed_now=`{missing_handoff['formal_result_material_allowed_now']}`"
    )
    lines.extend(["", "## Status Report Requirement Stage Summary", ""])
    requirement_summary = manifest["status_report_requirement_stage_summary"]
    lines.append(f"- present=`{requirement_summary['present']}`")
    lines.append(f"- mapped_requirement_count=`{requirement_summary['mapped_requirement_count']}`")
    lines.append(f"- unmapped_requirement_count=`{requirement_summary['unmapped_requirement_count']}`")
    lines.append(f"- mismatched_requirement_count=`{requirement_summary['mismatched_requirement_count']}`")
    lines.append(f"- blocked_stage_count=`{requirement_summary['blocked_stage_count']}`")
    for requirement_id, row in requirement_summary["requirements"].items():
        blocked_by = ", ".join(row["responsible_stage_blocked_by"]) if row["responsible_stage_blocked_by"] else "none"
        lines.append(
            f"- `{requirement_id}`: stage=`{row['responsible_stage_id']}`, "
            f"stage_status=`{row['responsible_stage_status']}`, "
            f"allowed_now=`{row['responsible_stage_allowed_now']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Status Report Remote Gate Summary", ""])
    for group_id, group in manifest["status_report_remote_gate_summary"].items():
        lines.append(f"### {group_id}")
        for item_id, item in group.items():
            blocked_by = ", ".join(item["blocked_by"]) if item["blocked_by"] else "none"
            lines.append(
                f"- `{item_id}`: allowed_now=`{item['allowed_now']}`, runs_training=`{item['runs_training']}`, "
                f"runs_remote_preflight=`{item['runs_remote_preflight']}`, host=`{item['host']}`, blocked_by=`{blocked_by}`"
            )
    lines.extend(["", "## Status Report Remote Requirement Matrices", ""])
    remote_requirements = manifest["status_report_remote_requirement_summary"]
    for group_id, group in remote_requirements.items():
        lines.append(f"### {group_id}")
        lines.append(f"- present=`{group['present']}`")
        lines.append(f"- status_counts=`{group['status_counts']}`")
        lines.append(f"- blocked_requirement_count=`{group['blocked_requirement_count']}`")
        for requirement_id, row in group["requirements"].items():
            lines.append(
                f"- `{requirement_id}`: status=`{row['status']}`, complete=`{row['complete']}`, "
                f"execution_allowed_now=`{row['execution_allowed_now']}`, "
                f"remote_training_ready_now=`{row['remote_training_ready_now']}`"
            )
    lines.extend(["", "## Status Report H02 Acceptance Requirement Matrix", ""])
    h02_requirements = manifest["status_report_h02_acceptance_requirement_summary"]
    lines.append(f"- present=`{h02_requirements['present']}`")
    lines.append(f"- status_counts=`{h02_requirements['status_counts']}`")
    lines.append(f"- blocked_requirement_count=`{h02_requirements['blocked_requirement_count']}`")
    for requirement_id, row in h02_requirements["requirements"].items():
        lines.append(
            f"- `{requirement_id}`: status=`{row['status']}`, complete=`{row['complete']}`, "
            f"paper_result_input_allowed_now=`{row['paper_result_input_allowed_now']}`"
        )
    lines.extend(["", "## Status Report Remaining Deliverables Acceptance Matrix", ""])
    remaining = manifest["status_report_remaining_deliverables_acceptance_summary"]
    lines.append(f"- present=`{remaining['present']}`")
    lines.append(f"- status=`{remaining['status']}`")
    lines.append(f"- matrix_row_count=`{remaining['matrix_row_count']}`")
    lines.append(f"- missing_row_count=`{remaining['missing_row_count']}`")
    lines.append(f"- blocked_category_count=`{remaining['blocked_category_count']}`")
    lines.extend(["", "## Prohibited Claims", ""])
    for claim in manifest["prohibited_claims"]:
        lines.append(f"- `{claim['claim_id']}`: not allowed; patterns={', '.join(claim['patterns'])}")
    lines.extend(["", "## Draft Audit", ""])
    draft = manifest["draft_audit"]
    lines.append(f"- status: `{draft['status']}`")
    for violation in draft["violations"]:
        lines.append(f"- violation `{violation['claim_id']}`: {', '.join(violation['matched_patterns'])}")
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
