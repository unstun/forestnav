from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_paper_readiness")
DEFAULT_METHOD_ALGORITHMS = Path("0_trials/module2_method_algorithms/module2_method_algorithms.json")
DEFAULT_SYSTEM_DIAGRAM = Path("0_trials/module2_system_diagram/module2_system_diagram.json")
DEFAULT_PAPER_TABLES = Path("0_trials/module2_paper_tables/module2_paper_tables.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_H02_FORMAL_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_F02_6_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_REMOTE_EXECUTION_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
CLAIM_SAFETY_REQUIREMENT_IDS = (
    "training_remote_ppo_checkpoint",
    "evaluation_gate3_episode_outputs",
    "acceptance_remote_pullback_and_audit",
    "h01_h02_formal_evaluation_acceptance",
)
CLAIM_SAFETY_REMOTE_PREFLIGHT_REQUIREMENT_IDS = (
    "f02_6_decision_closed_for_preflight",
    "approved_remote_preflight_manifest",
    "remote_preflight_protocol_contract",
    "remote_preflight_command_packetized",
)
CLAIM_SAFETY_POST_RUN_ACCEPTANCE_REQUIREMENT_IDS = (
    "pullback_expected_artifacts_complete",
    "checkpoint_hash_manifest_recorded",
    "gate3_formal_audit_accepts_remote_run",
    "h01_h02_regenerated_from_audited_checkpoint",
)
CLAIM_SAFETY_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS = (
    "h01_schema_and_h02_output_schema_match",
    "h02_formal_scope_and_scale_match_h01",
    "gate3_audit_and_pullback_acceptance",
    "ppo_rows_and_checkpoint_hash_present",
)
CLAIM_SAFETY_REMAINING_DELIVERABLE_MATRIX_IDS = (
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
CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS = (
    "training",
    "evaluation",
    "acceptance",
    "formal_acceptance",
)
CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_COMMAND_IDS = {
    "training:train_final_model_zip": (
        "train_final_model_zip_exists_nonempty",
        "train_final_model_zip_valid_zip",
    ),
    "training:train_summary_json": (
        "train_summary_json_exists_nonempty",
        "train_summary_json_formal_warm_start_metadata",
    ),
    "training:train_training_manifest_json": (
        "train_training_manifest_json_exists_nonempty",
        "train_training_manifest_json_provenance",
    ),
    "evaluation:eval_gate3_eval_episodes_csv": (
        "eval_gate3_eval_episodes_csv_exists_nonempty",
        "eval_gate3_eval_episodes_csv_schema",
    ),
    "evaluation:eval_gate3_summary_json": (
        "eval_gate3_summary_json_exists_nonempty",
        "eval_gate3_summary_json_formal_scope",
    ),
    "acceptance:gate3_trial_manifest_json": (
        "gate3_trial_manifest_json_exists_nonempty",
        "gate3_trial_manifest_json_formal_warm_start_scope",
    ),
    "acceptance:gate3_formal_audit_json": (
        "gate3_formal_audit_json_exists_nonempty",
        "gate3_formal_audit_json_accepts_formal_scope",
    ),
    "acceptance:pulled_back_checkpoint_hash_record": (
        "pulled_back_checkpoint_hash_record_exists_nonempty",
        "pulled_back_checkpoint_hash_record_matches_model",
    ),
    "formal_acceptance:h01_ready_for_formal_run": (
        "h01_ready_for_formal_run_exists_nonempty",
        "h01_ready_for_formal_run_status",
    ),
    "formal_acceptance:h02_formal_output_acceptance": (
        "h02_formal_output_acceptance_exists_nonempty",
        "h02_formal_output_acceptance_status",
    ),
}
CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_PLAN_ID = "module2_formal_gate_local_read_only_proof_commands"
CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_EXECUTION_BOUNDARY = "local_read_only_after_formal_remote_pullback"
CLAIM_SAFETY_DECISION_INTAKE_CLEAN_STATUSES = (
    "f02_6_decision_intake_pending_clean",
    "f02_6_decision_intake_closed_clean",
)
CLAIM_SAFETY_DECISION_INTAKE_RECORD_STATUSES = (
    "pending_human_decision",
    "approved",
    "rejected",
)
CLAIM_SAFETY_CLAIM_GATE_REGENERATION_ARTIFACT_IDS = (
    "formal_gate_proof_summary_chain_audit",
    "mainline_formal_gate_state_audit",
    "claim_safety",
    "paper_readiness",
)


@dataclass(frozen=True)
class PaperReadinessConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    method_algorithms_path: Path = DEFAULT_METHOD_ALGORITHMS
    system_diagram_path: Path = DEFAULT_SYSTEM_DIAGRAM
    paper_tables_path: Path = DEFAULT_PAPER_TABLES
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    h02_formal_acceptance_path: Path = DEFAULT_H02_FORMAL_ACCEPTANCE
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    f02_6_decision_record_path: Path = DEFAULT_F02_6_DECISION_RECORD
    remote_execution_packet_path: Path = DEFAULT_REMOTE_EXECUTION_PACKET
    status_report_path: Path = DEFAULT_STATUS_REPORT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = PaperReadinessConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        method_algorithms_path=args.method_algorithms,
        system_diagram_path=args.system_diagram,
        paper_tables_path=args.paper_tables,
        claim_safety_path=args.claim_safety,
        h02_formal_acceptance_path=args.h02_formal_acceptance,
        h01_manifest_path=args.h01_manifest,
        f02_6_decision_record_path=args.f02_6_decision_record,
        remote_execution_packet_path=args.remote_execution_packet,
        status_report_path=args.status_report,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "module2_paper_readiness.json"
    markdown_out = config.markdown_out or output_dir / "module2_paper_readiness.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: PaperReadinessConfig) -> dict[str, Any]:
    method_algorithms = _read_json(config.method_algorithms_path)
    system_diagram = _read_json(config.system_diagram_path)
    paper_tables = _read_json(config.paper_tables_path)
    claim_safety = _read_json(config.claim_safety_path)
    h02_acceptance = _read_json(config.h02_formal_acceptance_path)
    h01_manifest = _read_json(config.h01_manifest_path)
    decision_record = _read_json(config.f02_6_decision_record_path)
    remote_packet = _read_json(config.remote_execution_packet_path)
    status_report = _read_json(config.status_report_path)

    inputs = {
        "method_algorithms": str(config.method_algorithms_path),
        "system_diagram": str(config.system_diagram_path),
        "paper_tables": str(config.paper_tables_path),
        "claim_safety": str(config.claim_safety_path),
        "h02_formal_acceptance": str(config.h02_formal_acceptance_path),
        "h01_manifest": str(config.h01_manifest_path),
        "f02_6_decision_record": str(config.f02_6_decision_record_path),
        "remote_execution_packet": str(config.remote_execution_packet_path),
        "formal_gate_status_report": str(config.status_report_path),
    }
    status_permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    claim_handoff = claim_safety.get("status_report_handoff_summary")
    if not isinstance(claim_handoff, dict):
        claim_handoff = {}
    claim_missing_handoff = claim_safety.get("status_report_missing_artifacts_handoff_summary")
    if not isinstance(claim_missing_handoff, dict):
        claim_missing_handoff = {}
    claim_requirement_stage_summary = _claim_safety_requirement_stage_summary(claim_safety)
    claim_remote_requirement_summary = _claim_safety_remote_requirement_summary(claim_safety)
    claim_h02_acceptance_requirement_summary = _claim_safety_h02_acceptance_requirement_summary(claim_safety)
    claim_decision_intake_summary = _claim_safety_decision_intake_summary(claim_safety)
    claim_remaining_deliverables_acceptance_summary = _claim_safety_remaining_deliverables_acceptance_summary(
        claim_safety
    )
    claim_remaining_deliverables_gap_summary = _claim_safety_remaining_deliverables_gap_summary(claim_safety)
    claim_formal_gate_gap_audit_remaining_deliverables_gap_summary = (
        _claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_summary(claim_safety)
    )
    claim_remaining_deliverables_proof_command_plan = _claim_safety_remaining_deliverables_proof_command_plan(
        claim_safety
    )
    claim_remote_packet_safety_proof_deliverables_summary = (
        _claim_safety_remote_packet_safety_proof_deliverables_summary(claim_safety)
    )
    claim_remote_packet_safety_status_report_proof_deliverables_summary = (
        _claim_safety_remote_packet_safety_status_report_proof_deliverables_summary(claim_safety)
    )
    claim_remote_packet_safety_claim_gate_command_index_summary = (
        _claim_safety_remote_packet_safety_claim_gate_command_index_summary(claim_safety)
    )
    claim_next_action_guard_summary = _claim_safety_next_action_guard_summary(claim_safety)
    claim_next_required_formal_deliverables = _claim_safety_next_required_formal_deliverables(claim_safety)
    input_status = {
        "method_algorithms_status": method_algorithms.get("status"),
        "system_diagram_status": system_diagram.get("status"),
        "paper_tables_status": paper_tables.get("status"),
        "paper_tables_formal_claim_allowed": paper_tables.get("formal_claim_allowed"),
        "claim_safety_status": claim_safety.get("status"),
        "claim_safety_formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed"),
        "claim_safety_handoff_status": claim_handoff.get("status"),
        "claim_safety_transition_gate_status": claim_handoff.get("transition_gate_status"),
        "claim_safety_transition_gate_audit_issue_count": claim_handoff.get("transition_gate_audit_issue_count"),
        "claim_safety_handoff_safety_issue_count": claim_handoff.get("safety_issue_count"),
        "claim_safety_missing_artifacts_handoff_status": claim_missing_handoff.get("status"),
        "claim_safety_missing_artifacts_next_action": claim_missing_handoff.get("next_action_id"),
        "claim_safety_missing_artifacts_open_requirement_count": claim_missing_handoff.get("open_requirement_count"),
        "claim_safety_missing_artifacts_remote_training_allowed_now": claim_missing_handoff.get(
            "remote_training_allowed_now"
        ),
        "claim_safety_missing_artifacts_formal_result_material_allowed_now": claim_missing_handoff.get(
            "formal_result_material_allowed_now"
        ),
        "claim_safety_requirement_stage_present": claim_requirement_stage_summary["present"],
        "claim_safety_requirement_stage_mapped_count": claim_requirement_stage_summary["mapped_requirement_count"],
        "claim_safety_requirement_stage_unmapped_count": claim_requirement_stage_summary["unmapped_requirement_count"],
        "claim_safety_requirement_stage_mismatched_count": claim_requirement_stage_summary[
            "mismatched_requirement_count"
        ],
        "claim_safety_requirement_stage_blocked_stage_count": claim_requirement_stage_summary["blocked_stage_count"],
        "claim_safety_remote_preflight_requirement_present": claim_remote_requirement_summary[
            "remote_preflight_requirement_summary"
        ]["present"],
        "claim_safety_remote_preflight_requirement_satisfied_count": claim_remote_requirement_summary[
            "remote_preflight_requirement_summary"
        ]["status_counts"].get("satisfied", 0),
        "claim_safety_remote_preflight_requirement_blocked_count": claim_remote_requirement_summary[
            "remote_preflight_requirement_summary"
        ]["blocked_requirement_count"],
        "claim_safety_post_run_acceptance_requirement_present": claim_remote_requirement_summary[
            "post_run_acceptance_requirement_summary"
        ]["present"],
        "claim_safety_post_run_acceptance_requirement_satisfied_count": claim_remote_requirement_summary[
            "post_run_acceptance_requirement_summary"
        ]["status_counts"].get("satisfied", 0),
        "claim_safety_post_run_acceptance_requirement_blocked_count": claim_remote_requirement_summary[
            "post_run_acceptance_requirement_summary"
        ]["blocked_requirement_count"],
        "claim_safety_h02_formal_acceptance_requirement_present": claim_h02_acceptance_requirement_summary[
            "present"
        ],
        "claim_safety_h02_formal_acceptance_requirement_satisfied_count": claim_h02_acceptance_requirement_summary[
            "status_counts"
        ].get("satisfied", 0),
        "claim_safety_h02_formal_acceptance_requirement_blocked_count": claim_h02_acceptance_requirement_summary[
            "blocked_requirement_count"
        ],
        "claim_safety_decision_intake_present": claim_decision_intake_summary["present"],
        "claim_safety_decision_intake_status": claim_decision_intake_summary["status"],
        "claim_safety_decision_intake_record_status": claim_decision_intake_summary["record_status"],
        "claim_safety_decision_intake_audit_issue_count": claim_decision_intake_summary["audit_issue_count"],
        "claim_safety_decision_intake_decision_owner_required": claim_decision_intake_summary[
            "decision_owner_required"
        ],
        "claim_safety_decision_intake_valid_decision_count": claim_decision_intake_summary[
            "valid_decision_count"
        ],
        "claim_safety_decision_intake_required_record_field_count": claim_decision_intake_summary[
            "required_record_field_count"
        ],
        "claim_safety_decision_intake_decision_note_required": claim_decision_intake_summary[
            "decision_note_required"
        ],
        "claim_safety_decision_intake_invalid_input_count": claim_decision_intake_summary[
            "invalid_input_count"
        ],
        "claim_safety_decision_intake_post_decision_non_authorization_count": claim_decision_intake_summary[
            "post_decision_non_authorization_count"
        ],
        "claim_safety_decision_intake_post_decision_route_count": claim_decision_intake_summary[
            "post_decision_route_count"
        ],
        "claim_safety_decision_intake_approved_route_next_lane": claim_decision_intake_summary[
            "approved_route_next_lane"
        ],
        "claim_safety_decision_intake_approved_route_allows_remote_training_now": claim_decision_intake_summary[
            "approved_route_allows_remote_training_now"
        ],
        "claim_safety_decision_intake_rejected_route_requires_new_protocol_contract": claim_decision_intake_summary[
            "rejected_route_requires_new_protocol_contract"
        ],
        "claim_safety_decision_intake_next_blocked_lane": claim_decision_intake_summary["next_blocked_lane"],
        "claim_safety_decision_intake_remote_preflight_allowed_now": claim_decision_intake_summary[
            "remote_preflight_allowed_now"
        ],
        "claim_safety_decision_intake_remote_training_allowed_now": claim_decision_intake_summary[
            "remote_training_allowed_now"
        ],
        "claim_safety_decision_intake_formal_claim_allowed_now": claim_decision_intake_summary[
            "formal_claim_allowed_now"
        ],
        "claim_safety_remaining_deliverables_acceptance_present": claim_remaining_deliverables_acceptance_summary[
            "present"
        ],
        "claim_safety_remaining_deliverables_acceptance_matrix_row_count": claim_remaining_deliverables_acceptance_summary[
            "matrix_row_count"
        ],
        "claim_safety_remaining_deliverables_acceptance_missing_row_count": claim_remaining_deliverables_acceptance_summary[
            "missing_row_count"
        ],
        "claim_safety_remaining_deliverables_acceptance_blocked_category_count": claim_remaining_deliverables_acceptance_summary[
            "blocked_category_count"
        ],
        "claim_safety_remaining_deliverables_gap_present": claim_remaining_deliverables_gap_summary["present"],
        "claim_safety_remaining_deliverables_gap_total_missing_deliverables": claim_remaining_deliverables_gap_summary[
            "total_missing_deliverables"
        ],
        "claim_safety_remaining_deliverables_gap_open_category_count": claim_remaining_deliverables_gap_summary[
            "open_category_count"
        ],
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_present": claim_formal_gate_gap_audit_remaining_deliverables_gap_summary[
            "present"
        ],
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables": claim_formal_gate_gap_audit_remaining_deliverables_gap_summary[
            "total_missing_deliverables"
        ],
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_open_category_count": claim_formal_gate_gap_audit_remaining_deliverables_gap_summary[
            "open_category_count"
        ],
        "claim_safety_remaining_deliverables_proof_command_plan_present": claim_remaining_deliverables_proof_command_plan[
            "present"
        ],
        "claim_safety_remaining_deliverables_proof_command_plan_matrix_row_count": claim_remaining_deliverables_proof_command_plan[
            "total_matrix_rows"
        ],
        "claim_safety_remaining_deliverables_proof_command_plan_command_count": claim_remaining_deliverables_proof_command_plan[
            "total_proof_command_count"
        ],
        "claim_safety_remote_packet_safety_proof_summary_present": claim_remote_packet_safety_proof_deliverables_summary[
            "present"
        ],
        "claim_safety_remote_packet_safety_proof_training_missing_count": claim_remote_packet_safety_proof_deliverables_summary[
            "missing_counts_by_formal_category"
        ].get(
            "training", 0
        ),
        "claim_safety_remote_packet_safety_proof_evaluation_missing_count": claim_remote_packet_safety_proof_deliverables_summary[
            "missing_counts_by_formal_category"
        ].get(
            "evaluation", 0
        ),
        "claim_safety_remote_packet_safety_proof_acceptance_missing_count": claim_remote_packet_safety_proof_deliverables_summary[
            "missing_counts_by_formal_category"
        ].get(
            "acceptance", 0
        ),
        "claim_safety_remote_packet_safety_proof_formal_acceptance_missing_count": claim_remote_packet_safety_proof_deliverables_summary[
            "missing_counts_by_formal_category"
        ].get(
            "formal_acceptance", 0
        ),
        "claim_safety_remote_packet_safety_proof_next_blocked_lane": claim_remote_packet_safety_proof_deliverables_summary[
            "next_blocked_lane"
        ],
        "claim_safety_remote_packet_safety_proof_h02_paper_result_input_allowed": claim_remote_packet_safety_proof_deliverables_summary[
            "h02_paper_result_input_allowed"
        ],
        "claim_safety_remote_packet_safety_status_report_proof_summary_present": claim_remote_packet_safety_status_report_proof_deliverables_summary[
            "present"
        ],
        "claim_safety_remote_packet_safety_command_index_present": claim_remote_packet_safety_claim_gate_command_index_summary[
            "present"
        ],
        "claim_safety_remote_packet_safety_command_index_row_count": claim_remote_packet_safety_claim_gate_command_index_summary[
            "index_row_count"
        ],
        "claim_safety_remote_packet_safety_command_index_source_target_count": claim_remote_packet_safety_claim_gate_command_index_summary[
            "source_target_count"
        ],
        "claim_safety_remote_packet_safety_command_index_missing_target_count": len(
            claim_remote_packet_safety_claim_gate_command_index_summary["missing_target_ids"]
        ),
        "claim_safety_next_action_guard_present": claim_next_action_guard_summary["present"],
        "claim_safety_next_action_guard_status": claim_next_action_guard_summary["status"],
        "claim_safety_next_action_guard_expected_next_action_id": claim_next_action_guard_summary[
            "expected_next_action_id"
        ],
        "claim_safety_next_action_guard_all_execution_disabled_now": claim_next_action_guard_summary[
            "all_execution_disabled_now"
        ],
        "claim_safety_next_action_guard_execution_leak_count": claim_next_action_guard_summary[
            "execution_leak_count"
        ],
        "claim_safety_next_action_guard_violation_count": claim_next_action_guard_summary["violation_count"],
        "claim_safety_next_required_formal_deliverables_present": claim_next_required_formal_deliverables[
            "present"
        ],
        "claim_safety_next_required_formal_deliverables_status": claim_next_required_formal_deliverables["status"],
        "claim_safety_next_required_formal_deliverables_total_missing": claim_next_required_formal_deliverables[
            "total_missing_deliverables"
        ],
        "claim_safety_next_required_formal_deliverables_blocked_category_count": claim_next_required_formal_deliverables[
            "blocked_category_count"
        ],
        "claim_safety_next_required_formal_deliverables_row_count": claim_next_required_formal_deliverables[
            "row_count"
        ],
        "h02_formal_acceptance_status": h02_acceptance.get("status"),
        "h02_formal_output_accepted": h02_acceptance.get("formal_output_accepted"),
        "h02_paper_result_input_allowed": h02_acceptance.get("paper_result_input_allowed"),
        "h01_manifest_status": h01_manifest.get("status"),
        "f02_6_decision_status": decision_record.get("status"),
        "remote_execution_packet_status": remote_packet.get("status"),
        "remote_execution_ready": remote_packet.get("ready_to_run_remote_training"),
        "status_report_status": status_report.get("status"),
        "status_report_formal_claim_allowed_now": status_permissions.get("formal_claim_allowed_now"),
        "status_report_input_safety_issue_count": status_report.get("input_safety_issue_count"),
    }
    allowed_claims = [item for item in claim_safety.get("allowed_claims", []) if isinstance(item, dict)]
    conditional_claims = [item for item in claim_safety.get("conditional_claims", []) if isinstance(item, dict)]
    allowed_claim_ids = [str(item.get("claim_id")) for item in allowed_claims if item.get("claim_id")]
    conditional_claim_ids = [str(item.get("claim_id")) for item in conditional_claims if item.get("claim_id")]
    global_blockers = _global_blockers(
        paper_tables=paper_tables,
        claim_safety=claim_safety,
        h02_acceptance=h02_acceptance,
        h01_manifest=h01_manifest,
        decision_record=decision_record,
        remote_packet=remote_packet,
        status_report=status_report,
    )
    section_readiness = _section_readiness(
        method_algorithms=method_algorithms,
        system_diagram=system_diagram,
        paper_tables=paper_tables,
        claim_safety=claim_safety,
        h02_acceptance=h02_acceptance,
        decision_record=decision_record,
        remote_packet=remote_packet,
        status_report=status_report,
        inputs=inputs,
    )
    manuscript_ready = not global_blockers and all(item["status"] != "blocked" for item in section_readiness)
    return {
        "schema_version": 1,
        "artifact_name": "module2_paper_readiness",
        "status": "paper_evidence_ready" if manuscript_ready else "partial_methods_ready_results_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "manuscript_ready": manuscript_ready,
        "formal_results_ready": not global_blockers,
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "inputs": inputs,
        "input_status": input_status,
        "claim_safety_requirement_stage_summary": claim_requirement_stage_summary,
        "claim_safety_remote_requirement_summary": claim_remote_requirement_summary,
        "claim_safety_h02_acceptance_requirement_summary": claim_h02_acceptance_requirement_summary,
        "claim_safety_decision_intake_summary": claim_decision_intake_summary,
        "claim_safety_remaining_deliverables_acceptance_summary": claim_remaining_deliverables_acceptance_summary,
        "claim_safety_remaining_deliverables_gap_summary": claim_remaining_deliverables_gap_summary,
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_summary": claim_formal_gate_gap_audit_remaining_deliverables_gap_summary,
        "claim_safety_remaining_deliverables_proof_command_plan": claim_remaining_deliverables_proof_command_plan,
        "claim_safety_remote_packet_safety_proof_deliverables_summary": (
            claim_remote_packet_safety_proof_deliverables_summary
        ),
        "claim_safety_remote_packet_safety_status_report_proof_deliverables_summary": (
            claim_remote_packet_safety_status_report_proof_deliverables_summary
        ),
        "claim_safety_remote_packet_safety_claim_gate_command_index_summary": (
            claim_remote_packet_safety_claim_gate_command_index_summary
        ),
        "claim_safety_next_action_guard_summary": claim_next_action_guard_summary,
        "claim_safety_next_required_formal_deliverables": claim_next_required_formal_deliverables,
        "global_blockers": global_blockers,
        "allowed_claim_ids": allowed_claim_ids,
        "conditional_claim_ids": conditional_claim_ids,
        "section_readiness": section_readiness,
        "claim_boundaries": [
            "Method and system-description sections may be drafted from code-anchored artifacts.",
            "Formal result, ablation, and performance-improvement sections remain blocked until H02 acceptance and claim safety are both formal-ready.",
            "No-warm Gate #3 failure can be written only with no-warm scope qualification.",
            "Obstacle-summary warm-start effect remains blocked until F02.6 closes and a remote formal run/audit is pulled back.",
            "Do not use this readiness ledger as a performance result; it only routes paper writing work to evidence.",
            "Formal gate status report must be ready before formal result sections can be treated as ready.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 paper readiness/evidence ledger without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--method-algorithms", type=Path, default=DEFAULT_METHOD_ALGORITHMS)
    parser.add_argument("--system-diagram", type=Path, default=DEFAULT_SYSTEM_DIAGRAM)
    parser.add_argument("--paper-tables", type=Path, default=DEFAULT_PAPER_TABLES)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--h02-formal-acceptance", type=Path, default=DEFAULT_H02_FORMAL_ACCEPTANCE)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--f02-6-decision-record", type=Path, default=DEFAULT_F02_6_DECISION_RECORD)
    parser.add_argument("--remote-execution-packet", type=Path, default=DEFAULT_REMOTE_EXECUTION_PACKET)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _global_blockers(
    *,
    paper_tables: dict[str, Any],
    claim_safety: dict[str, Any],
    h02_acceptance: dict[str, Any],
    h01_manifest: dict[str, Any],
    decision_record: dict[str, Any],
    remote_packet: dict[str, Any],
    status_report: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if paper_tables.get("formal_claim_allowed") is not True:
        blockers.append("paper_tables_not_formal")
    _extend_unique(blockers, paper_tables.get("blockers", []))
    if h02_acceptance.get("formal_output_accepted") is not True or h02_acceptance.get("paper_result_input_allowed") is not True:
        _append_unique(blockers, "h02_formal_acceptance_not_accepted")
    _extend_unique(blockers, h02_acceptance.get("blockers", []))
    if claim_safety.get("formal_performance_claim_allowed") is not True:
        _append_unique(blockers, "claim_safety_blocks_formal_performance")
    _extend_unique(blockers, claim_safety.get("formal_performance_blockers", []))
    _extend_unique(blockers, _claim_safety_requirement_stage_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_remote_requirement_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_h02_acceptance_requirement_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_decision_intake_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_remaining_deliverables_acceptance_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_remaining_deliverables_gap_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_remaining_deliverables_proof_command_plan_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_remote_packet_safety_proof_deliverables_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_remote_packet_safety_claim_gate_command_index_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_next_action_guard_blockers(claim_safety))
    _extend_unique(blockers, _claim_safety_next_required_formal_deliverables_blockers(claim_safety))
    _extend_unique(blockers, h01_manifest.get("blockers", []))
    if str(decision_record.get("status")) == "pending_human_decision":
        _append_unique(blockers, "f02_6_pending")
    _extend_unique(blockers, decision_record.get("blockers", []))
    if remote_packet.get("ready_to_run_remote_training") is not True:
        _append_unique(blockers, "remote_execution_packet_not_ready")
    _extend_unique(blockers, remote_packet.get("blockers", []))
    _extend_unique(blockers, _status_report_blockers(status_report))
    return blockers


def _section_readiness(
    *,
    method_algorithms: dict[str, Any],
    system_diagram: dict[str, Any],
    paper_tables: dict[str, Any],
    claim_safety: dict[str, Any],
    h02_acceptance: dict[str, Any],
    decision_record: dict[str, Any],
    remote_packet: dict[str, Any],
    status_report: dict[str, Any],
    inputs: dict[str, str],
) -> list[dict[str, Any]]:
    method_ready = method_algorithms.get("status") == "code_anchored"
    figure_ready = system_diagram.get("status") == "code_anchored_drawio"
    no_warm_ready = any(item.get("claim_id") == "no_warm_gate3_formal_failure" for item in claim_safety.get("allowed_claims", []))
    formal_blockers = _global_blockers(
        paper_tables=paper_tables,
        claim_safety=claim_safety,
        h02_acceptance=h02_acceptance,
        h01_manifest={},
        decision_record=decision_record,
        remote_packet=remote_packet,
        status_report=status_report,
    )
    table_blockers = _unique([str(item) for item in paper_tables.get("blockers", [])] + [str(item) for item in h02_acceptance.get("blockers", [])])
    warm_start_blockers = _unique([str(item) for item in decision_record.get("blockers", [])] + [str(item) for item in remote_packet.get("blockers", [])])
    if str(decision_record.get("status")) != "approved":
        warm_start_blockers.insert(0, "f02_6_not_approved")

    return [
        {
            "section_id": "method_algorithm",
            "paper_target": "Methods: RL-RS analytic-expansion operator and PPO environment",
            "status": "ready_to_write" if method_ready else "blocked",
            "evidence": [inputs["method_algorithms"]],
            "blockers": [] if method_ready else ["method_algorithms_not_code_anchored"],
        },
        {
            "section_id": "system_figure",
            "paper_target": "Figure: system architecture and fallback semantics",
            "status": "ready_to_write" if figure_ready else "blocked",
            "evidence": [inputs["system_diagram"]],
            "blockers": [] if figure_ready else ["system_diagram_not_code_anchored"],
        },
        {
            "section_id": "no_warm_failure_claim",
            "paper_target": "Scoped result note: no-warm PPO Gate #3 failure",
            "status": "ready_with_scope_limit" if no_warm_ready else "blocked",
            "evidence": [inputs["claim_safety"]],
            "blockers": [] if no_warm_ready else ["no_warm_failure_claim_not_allowed"],
        },
        {
            "section_id": "main_results_table",
            "paper_target": "Results: main H02 formal comparison table",
            "status": "ready_to_write" if paper_tables.get("formal_claim_allowed") is True and not table_blockers else "blocked",
            "evidence": [inputs["paper_tables"], inputs["h02_formal_acceptance"]],
            "blockers": table_blockers,
        },
        {
            "section_id": "formal_results",
            "paper_target": "Results: formal performance improvement claims",
            "status": "ready_to_write" if claim_safety.get("formal_performance_claim_allowed") is True and not formal_blockers else "blocked",
            "evidence": [inputs["claim_safety"], inputs["h02_formal_acceptance"], inputs["paper_tables"], inputs["formal_gate_status_report"]],
            "blockers": formal_blockers,
        },
        {
            "section_id": "warm_start_effect",
            "paper_target": "Ablation: obstacle-summary warm-start effect",
            "status": "ready_to_write" if not warm_start_blockers and remote_packet.get("ready_to_run_remote_training") is True else "blocked",
            "evidence": [inputs["f02_6_decision_record"], inputs["remote_execution_packet"]],
            "blockers": warm_start_blockers,
        },
    ]


def _status_report_blockers(status_report: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
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
    return blockers


def _claim_safety_requirement_stage_summary(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_requirement_stage_summary")
    if not isinstance(summary, dict):
        summary = {}
    raw_requirements = summary.get("requirements") if isinstance(summary.get("requirements"), dict) else {}
    requirements: dict[str, dict[str, Any]] = {}
    for requirement_id in CLAIM_SAFETY_REQUIREMENT_IDS:
        row = raw_requirements.get(requirement_id) if isinstance(raw_requirements.get(requirement_id), dict) else {}
        requirements[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "responsible_stage_id": row.get("responsible_stage_id"),
            "responsible_stage_status": row.get("responsible_stage_status"),
            "responsible_stage_allowed_now": row.get("responsible_stage_allowed_now")
            if isinstance(row.get("responsible_stage_allowed_now"), bool)
            else None,
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
        "requirements": requirements,
    }


def _claim_safety_requirement_stage_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_requirement_stage_summary(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_requirement_stage_summary")
        return blockers
    if summary["mapped_requirement_count"] != len(CLAIM_SAFETY_REQUIREMENT_IDS):
        blockers.append("claim_safety_requirement_stage_mapping_incomplete")
    if summary["unmapped_requirement_count"] > 0:
        blockers.append("claim_safety_requirement_stage_unmapped")
    if summary["mismatched_requirement_count"] > 0:
        blockers.append("claim_safety_requirement_stage_mismatched")
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            _append_unique(blockers, f"claim_safety_requirement_stage_missing_{requirement_id}")
        elif row["mapping_present"] is not True or row["mapping_matches_expected"] is not True:
            _append_unique(blockers, f"claim_safety_requirement_stage_invalid_{requirement_id}")
    return blockers


def _claim_safety_remote_requirement_summary(claim_safety: dict[str, Any]) -> dict[str, dict[str, Any]]:
    summary = claim_safety.get("status_report_remote_requirement_summary")
    summary = summary if isinstance(summary, dict) else {}
    return {
        "remote_preflight_requirement_summary": _claim_safety_remote_requirement_matrix_summary(
            summary=summary,
            group_id="remote_preflight_requirement_summary",
            required_ids=CLAIM_SAFETY_REMOTE_PREFLIGHT_REQUIREMENT_IDS,
        ),
        "post_run_acceptance_requirement_summary": _claim_safety_remote_requirement_matrix_summary(
            summary=summary,
            group_id="post_run_acceptance_requirement_summary",
            required_ids=CLAIM_SAFETY_POST_RUN_ACCEPTANCE_REQUIREMENT_IDS,
        ),
    }


def _claim_safety_remote_requirement_matrix_summary(
    *,
    summary: dict[str, Any],
    group_id: str,
    required_ids: Sequence[str],
) -> dict[str, Any]:
    group = summary.get(group_id)
    group = group if isinstance(group, dict) else {}
    raw_requirements = group.get("requirements") if isinstance(group.get("requirements"), dict) else {}
    requirements: dict[str, dict[str, Any]] = {}
    for requirement_id in required_ids:
        row = raw_requirements.get(requirement_id) if isinstance(raw_requirements.get(requirement_id), dict) else {}
        requirements[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "complete": row.get("complete") if isinstance(row.get("complete"), bool) else None,
            "execution_allowed_now": row.get("execution_allowed_now")
            if isinstance(row.get("execution_allowed_now"), bool)
            else None,
            "remote_training_ready_now": row.get("remote_training_ready_now")
            if isinstance(row.get("remote_training_ready_now"), bool)
            else None,
        }
    status_counts = group.get("status_counts") if isinstance(group.get("status_counts"), dict) else {}
    return {
        "present": bool(group),
        "required_requirement_count": int(group.get("required_requirement_count") or len(required_ids)),
        "present_requirement_count": int(group.get("present_requirement_count") or 0),
        "blocked_requirement_count": int(group.get("blocked_requirement_count") or 0),
        "status_counts": {str(key): int(value or 0) for key, value in status_counts.items()},
        "missing_requirement_ids": [str(value) for value in group.get("missing_requirement_ids", []) if value]
        if isinstance(group.get("missing_requirement_ids"), list)
        else [],
        "requirements": requirements,
    }


def _claim_safety_remote_requirement_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_remote_requirement_summary(claim_safety)
    blockers: list[str] = []
    blockers.extend(
        _claim_safety_remote_requirement_group_blockers(
            summary=summary["remote_preflight_requirement_summary"],
            prefix="claim_safety_remote_preflight_requirement",
            required_ids=CLAIM_SAFETY_REMOTE_PREFLIGHT_REQUIREMENT_IDS,
        )
    )
    blockers.extend(
        _claim_safety_remote_requirement_group_blockers(
            summary=summary["post_run_acceptance_requirement_summary"],
            prefix="claim_safety_post_run_acceptance_requirement",
            required_ids=CLAIM_SAFETY_POST_RUN_ACCEPTANCE_REQUIREMENT_IDS,
        )
    )
    return blockers


def _claim_safety_h02_acceptance_requirement_summary(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_h02_acceptance_requirement_summary")
    summary = summary if isinstance(summary, dict) else {}
    raw_requirements = summary.get("requirements") if isinstance(summary.get("requirements"), dict) else {}
    requirements: dict[str, dict[str, Any]] = {}
    for requirement_id in CLAIM_SAFETY_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS:
        row = raw_requirements.get(requirement_id) if isinstance(raw_requirements.get(requirement_id), dict) else {}
        requirements[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "complete": row.get("complete") if isinstance(row.get("complete"), bool) else None,
            "paper_result_input_allowed_now": row.get("paper_result_input_allowed_now")
            if isinstance(row.get("paper_result_input_allowed_now"), bool)
            else None,
        }
    status_counts = summary.get("status_counts") if isinstance(summary.get("status_counts"), dict) else {}
    return {
        "present": bool(summary),
        "required_requirement_count": int(
            summary.get("required_requirement_count") or len(CLAIM_SAFETY_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS)
        ),
        "present_requirement_count": int(summary.get("present_requirement_count") or 0),
        "blocked_requirement_count": int(summary.get("blocked_requirement_count") or 0),
        "status_counts": {str(key): int(value or 0) for key, value in status_counts.items()},
        "missing_requirement_ids": [str(value) for value in summary.get("missing_requirement_ids", []) if value]
        if isinstance(summary.get("missing_requirement_ids"), list)
        else [],
        "requirements": requirements,
    }


def _claim_safety_h02_acceptance_requirement_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_h02_acceptance_requirement_summary(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_h02_acceptance_requirement_summary")
        return blockers
    if int(summary["required_requirement_count"] or 0) != len(CLAIM_SAFETY_H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS):
        blockers.append("claim_safety_h02_acceptance_requirement_required_count_mismatch")
    for requirement_id in summary["missing_requirement_ids"]:
        _append_unique(blockers, f"claim_safety_h02_acceptance_requirement_missing_{requirement_id}")
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            _append_unique(blockers, f"claim_safety_h02_acceptance_requirement_missing_{requirement_id}")
    return blockers


def _claim_safety_decision_intake_summary(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_decision_intake_summary")
    if not isinstance(summary, dict):
        summary = {}
    valid_decisions = _string_list(summary.get("valid_decisions"))
    route_decisions = _string_list(summary.get("post_decision_route_decisions"))
    required_fields = _string_list(summary.get("required_record_fields"))
    impact_required = _string_list(summary.get("decision_impact_formal_training_still_requires"))
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
        "post_decision_route_count": int(summary.get("post_decision_route_count") or len(route_decisions)),
        "post_decision_route_decisions": route_decisions,
        "approved_route_next_lane": summary.get("approved_route_next_lane"),
        "approved_route_allows_remote_training_now": summary.get("approved_route_allows_remote_training_now")
        if isinstance(summary.get("approved_route_allows_remote_training_now"), bool)
        else None,
        "rejected_route_next_lane": summary.get("rejected_route_next_lane"),
        "rejected_route_requires_new_protocol_contract": summary.get("rejected_route_requires_new_protocol_contract")
        if isinstance(summary.get("rejected_route_requires_new_protocol_contract"), bool)
        else None,
        "remote_preflight_allowed_now": summary.get("remote_preflight_allowed_now")
        if isinstance(summary.get("remote_preflight_allowed_now"), bool)
        else None,
        "remote_training_allowed_now": summary.get("remote_training_allowed_now")
        if isinstance(summary.get("remote_training_allowed_now"), bool)
        else None,
        "formal_claim_allowed_now": summary.get("formal_claim_allowed_now")
        if isinstance(summary.get("formal_claim_allowed_now"), bool)
        else None,
        "decision_impact_present": summary.get("decision_impact_present")
        if isinstance(summary.get("decision_impact_present"), bool)
        else None,
        "decision_impact_not_paper_result_material": summary.get("decision_impact_not_paper_result_material")
        if isinstance(summary.get("decision_impact_not_paper_result_material"), bool)
        else None,
        "decision_record_is_not_training_authorization": summary.get(
            "decision_record_is_not_training_authorization"
        )
        if isinstance(summary.get("decision_record_is_not_training_authorization"), bool)
        else None,
        "decision_record_is_not_paper_result_material": summary.get(
            "decision_record_is_not_paper_result_material"
        )
        if isinstance(summary.get("decision_record_is_not_paper_result_material"), bool)
        else None,
        "decision_impact_remote_preflight_allowed_now": summary.get(
            "decision_impact_remote_preflight_allowed_now"
        )
        if isinstance(summary.get("decision_impact_remote_preflight_allowed_now"), bool)
        else None,
        "decision_impact_remote_training_allowed_now": summary.get(
            "decision_impact_remote_training_allowed_now"
        )
        if isinstance(summary.get("decision_impact_remote_training_allowed_now"), bool)
        else None,
        "decision_impact_formal_claim_allowed_now": summary.get(
            "decision_impact_formal_claim_allowed_now"
        )
        if isinstance(summary.get("decision_impact_formal_claim_allowed_now"), bool)
        else None,
        "decision_impact_paper_result_material_allowed_now": summary.get(
            "decision_impact_paper_result_material_allowed_now"
        )
        if isinstance(summary.get("decision_impact_paper_result_material_allowed_now"), bool)
        else None,
        "decision_impact_formal_training_still_requires": impact_required,
    }


def _claim_safety_decision_intake_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_decision_intake_summary(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_f02_6_decision_intake_summary")
        return blockers
    if summary["status"] not in CLAIM_SAFETY_DECISION_INTAKE_CLEAN_STATUSES:
        blockers.append("claim_safety_f02_6_decision_intake_not_clean")
    if summary["audit_issue_count"] > 0:
        blockers.append("claim_safety_f02_6_decision_intake_audit_issues_open")
    if summary["decision_owner_required"] != "Dr Sun":
        blockers.append("claim_safety_f02_6_decision_intake_decision_owner_not_dr_sun")
    expected_decisions = {"approve_obstacle_summary_warm_start", "reject_obstacle_summary_warm_start"}
    if not expected_decisions.issubset(set(summary["valid_decisions"])):
        blockers.append("claim_safety_f02_6_decision_intake_valid_decisions_incomplete")
    expected_fields = {"decision", "decider", "decision_note"}
    if not expected_fields.issubset(set(summary["required_record_fields"])):
        blockers.append("claim_safety_f02_6_decision_intake_required_fields_incomplete")
    if not summary["decision_note_required"]:
        blockers.append("claim_safety_f02_6_decision_intake_decision_note_not_required")
    if summary["invalid_input_count"] == 0:
        blockers.append("claim_safety_f02_6_decision_intake_invalid_inputs_missing")
    if summary["post_decision_non_authorization_count"] == 0:
        blockers.append("claim_safety_f02_6_decision_intake_non_authorizations_missing")
    if summary["post_decision_route_count"] < 2:
        blockers.append("claim_safety_f02_6_decision_intake_route_count_incomplete")
    if not expected_decisions.issubset(set(summary["post_decision_route_decisions"])):
        blockers.append("claim_safety_f02_6_decision_intake_route_decisions_incomplete")
    if summary["approved_route_next_lane"] != "source_fresh_regeneration":
        blockers.append("claim_safety_f02_6_decision_intake_approved_route_next_lane_invalid")
    if summary["approved_route_allows_remote_training_now"] is not False:
        blockers.append("claim_safety_f02_6_decision_intake_approved_route_allows_remote_training")
    if summary["rejected_route_next_lane"] != "protocol_redesign":
        blockers.append("claim_safety_f02_6_decision_intake_rejected_route_next_lane_invalid")
    if summary["rejected_route_requires_new_protocol_contract"] is not True:
        blockers.append("claim_safety_f02_6_decision_intake_rejected_route_missing_protocol_contract")
    if summary["record_status"] == "pending_human_decision":
        blockers.append("claim_safety_f02_6_decision_intake_pending")
        if summary["next_blocked_lane"] != "decision":
            blockers.append("claim_safety_pending_f02_6_intake_next_lane_not_decision")
        if summary["remote_preflight_allowed_now"] is not False:
            blockers.append("claim_safety_pending_f02_6_intake_allows_remote_preflight")
        if summary["remote_training_allowed_now"] is not False:
            blockers.append("claim_safety_pending_f02_6_intake_allows_remote_training")
        if summary["formal_claim_allowed_now"] is not False:
            blockers.append("claim_safety_pending_f02_6_intake_allows_formal_claim")
    elif summary["record_status"] in {"approved", "rejected"}:
        if summary["record_decider"] != "Dr Sun":
            blockers.append("claim_safety_closed_f02_6_intake_decider_not_dr_sun")
    elif summary["record_status"] not in CLAIM_SAFETY_DECISION_INTAKE_RECORD_STATUSES:
        blockers.append("claim_safety_f02_6_decision_intake_unknown_record_status")
    if summary["decision_impact_present"] is not True:
        blockers.append("claim_safety_f02_6_decision_intake_impact_missing")
    if summary["decision_impact_not_paper_result_material"] is not True:
        blockers.append("claim_safety_f02_6_decision_intake_impact_is_paper_result_material")
    if summary["decision_record_is_not_training_authorization"] is not True:
        blockers.append("claim_safety_f02_6_decision_record_may_authorize_training")
    if summary["decision_record_is_not_paper_result_material"] is not True:
        blockers.append("claim_safety_f02_6_decision_record_may_be_paper_result_material")
    for field, blocker in (
        ("decision_impact_remote_preflight_allowed_now", "claim_safety_f02_6_decision_impact_allows_remote_preflight"),
        ("decision_impact_remote_training_allowed_now", "claim_safety_f02_6_decision_impact_allows_remote_training"),
        ("decision_impact_formal_claim_allowed_now", "claim_safety_f02_6_decision_impact_allows_formal_claim"),
        ("decision_impact_paper_result_material_allowed_now", "claim_safety_f02_6_decision_impact_allows_paper_result_material"),
    ):
        if summary[field] is not False:
            blockers.append(blocker)
    for required in (
        "source_freshness_audit",
        "post_f02_6_regeneration_plan",
        "post_f02_6_plan_audit",
        "remote_formal_execution_packet_ready",
        "approved_remote_preflight",
    ):
        if required not in summary["decision_impact_formal_training_still_requires"]:
            blockers.append(f"claim_safety_f02_6_decision_impact_missing_required_{required}")
    return blockers


def _claim_safety_next_action_guard_summary(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_next_action_guard_summary")
    summary = summary if isinstance(summary, dict) else {}
    return {
        "present": bool(summary.get("present")) or bool(summary),
        "status": summary.get("status"),
        "pending_f02_6_decision": summary.get("pending_f02_6_decision")
        if isinstance(summary.get("pending_f02_6_decision"), bool)
        else None,
        "next_blocked_lane_id": summary.get("next_blocked_lane_id"),
        "expected_next_action_id": summary.get("expected_next_action_id"),
        "handoff_next_action_id": summary.get("handoff_next_action_id"),
        "handoff_next_action_requires_dr_sun": summary.get("handoff_next_action_requires_dr_sun")
        if isinstance(summary.get("handoff_next_action_requires_dr_sun"), bool)
        else None,
        "missing_artifacts_next_action_id": summary.get("missing_artifacts_next_action_id"),
        "decision_intake_next_blocked_lane": summary.get("decision_intake_next_blocked_lane"),
        "all_execution_disabled_now": summary.get("all_execution_disabled_now")
        if isinstance(summary.get("all_execution_disabled_now"), bool)
        else None,
        "execution_leak_count": int(summary.get("execution_leak_count") or 0),
        "remote_execution_allowed_count": int(summary.get("remote_execution_allowed_count") or 0),
        "remote_stage_allowed_count": int(summary.get("remote_stage_allowed_count") or 0),
        "violation_count": int(summary.get("violation_count") or 0),
        "execution_leak_surface_ids": _strings(summary.get("execution_leak_surface_ids")),
    }


def _claim_safety_next_action_guard_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_next_action_guard_summary(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_next_action_guard_summary")
        return blockers
    if summary["status"] != "next_action_guard_passed":
        blockers.append("claim_safety_next_action_guard_not_passed")
    if summary["violation_count"] > 0:
        blockers.append("claim_safety_next_action_guard_violations_open")
    if summary["pending_f02_6_decision"] is not True:
        return blockers
    expected_action = "record_f02_6_decision"
    if summary["next_blocked_lane_id"] != "decision":
        blockers.append("claim_safety_next_action_guard_lane_not_decision")
    if summary["expected_next_action_id"] != expected_action:
        blockers.append("claim_safety_next_action_guard_next_action_not_decision")
    if summary["handoff_next_action_id"] != expected_action:
        blockers.append("claim_safety_next_action_guard_handoff_action_not_decision")
    if summary["missing_artifacts_next_action_id"] != expected_action:
        blockers.append("claim_safety_next_action_guard_missing_artifacts_action_not_decision")
    if summary["decision_intake_next_blocked_lane"] != "decision":
        blockers.append("claim_safety_next_action_guard_intake_lane_not_decision")
    if summary["handoff_next_action_requires_dr_sun"] is not True:
        blockers.append("claim_safety_next_action_guard_handoff_not_gated_by_dr_sun")
    if summary["all_execution_disabled_now"] is not True:
        blockers.append("claim_safety_next_action_guard_execution_not_disabled")
    if summary["execution_leak_count"] > 0:
        blockers.append("claim_safety_next_action_guard_execution_leaks_open")
    if summary["remote_execution_allowed_count"] > 0:
        blockers.append("claim_safety_next_action_guard_remote_execution_allowed")
    if summary["remote_stage_allowed_count"] > 0:
        blockers.append("claim_safety_next_action_guard_remote_stage_allowed")
    return blockers


def _claim_safety_next_required_formal_deliverables(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_next_required_formal_deliverables")
    summary = summary if isinstance(summary, dict) else {}
    raw_rows = summary.get("rows")
    rows: dict[str, dict[str, Any]] = {}
    if isinstance(raw_rows, dict):
        iterable_rows = (
            dict(raw_row, matrix_id=matrix_id) if isinstance(raw_row, dict) and "matrix_id" not in raw_row else raw_row
            for matrix_id, raw_row in raw_rows.items()
        )
    elif isinstance(raw_rows, list):
        iterable_rows = (raw_row for raw_row in raw_rows if isinstance(raw_row, dict))
    else:
        iterable_rows = ()
    for raw_row in iterable_rows:
        if not isinstance(raw_row, dict):
            continue
        matrix_id = raw_row.get("matrix_id")
        if not matrix_id:
            continue
        rows[str(matrix_id)] = {
            "present": True,
            "category": raw_row.get("category"),
            "current_state": raw_row.get("current_state"),
            "responsible_stage_id": raw_row.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw_row.get("responsible_stage_allowed_now")
            if isinstance(raw_row.get("responsible_stage_allowed_now"), bool)
            else None,
            "proof_command_ids": _strings(raw_row.get("proof_command_ids")),
            "invalid_substitute_count": int(raw_row.get("invalid_substitute_count") or 0),
        }
    return {
        "present": bool(summary.get("present")) or bool(summary),
        "status": summary.get("status"),
        "execution_boundary": summary.get("execution_boundary"),
        "not_paper_result_material": summary.get("not_paper_result_material") is True,
        "runs_training": summary.get("runs_training") is True,
        "runs_remote_preflight": summary.get("runs_remote_preflight") is True,
        "total_missing_deliverables": int(summary.get("total_missing_deliverables") or 0),
        "blocked_category_count": int(summary.get("blocked_category_count") or 0),
        "blocked_categories": _strings(summary.get("blocked_categories")),
        "category_order": _strings(summary.get("category_order")),
        "row_count": len(rows),
        "missing_matrix_ids": [
            matrix_id for matrix_id in CLAIM_SAFETY_REMAINING_DELIVERABLE_MATRIX_IDS if matrix_id not in rows
        ],
        "rows": rows,
    }


def _claim_safety_next_required_formal_deliverables_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_next_required_formal_deliverables(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_next_required_formal_deliverables")
        return blockers
    if not summary["not_paper_result_material"]:
        blockers.append("claim_safety_next_required_formal_deliverables_marked_as_paper_result")
    if summary["runs_training"]:
        blockers.append("claim_safety_next_required_formal_deliverables_runs_training")
    if summary["runs_remote_preflight"]:
        blockers.append("claim_safety_next_required_formal_deliverables_runs_remote_preflight")
    if summary["category_order"] != list(CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS):
        blockers.append("claim_safety_next_required_formal_deliverables_category_order_mismatch")
    if summary["row_count"] != len(CLAIM_SAFETY_REMAINING_DELIVERABLE_MATRIX_IDS):
        blockers.append("claim_safety_next_required_formal_deliverables_row_count_mismatch")
    for matrix_id in summary["missing_matrix_ids"]:
        _append_unique(
            blockers,
            f"claim_safety_next_required_formal_deliverables_missing_{matrix_id.replace(':', '_')}",
        )
    if claim_safety.get("formal_performance_claim_allowed") is True:
        if summary["total_missing_deliverables"] > 0:
            blockers.append("claim_safety_next_required_formal_deliverables_missing_while_claim_ready")
        if summary["blocked_category_count"] > 0:
            blockers.append("claim_safety_next_required_formal_deliverables_categories_blocked_while_claim_ready")
    else:
        if summary["status"] != "blocked_missing_formal_deliverables":
            blockers.append("claim_safety_next_required_formal_deliverables_status_not_blocked")
        if summary["total_missing_deliverables"] <= 0:
            blockers.append("claim_safety_next_required_formal_deliverables_zero_missing_while_blocked")
        if summary["blocked_category_count"] <= 0:
            blockers.append("claim_safety_next_required_formal_deliverables_zero_blocked_categories_while_blocked")
        if summary["blocked_categories"] != list(CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS):
            blockers.append("claim_safety_next_required_formal_deliverables_blocked_categories_mismatch")
    for matrix_id, row in summary["rows"].items():
        safe_matrix_id = matrix_id.replace(":", "_")
        if not row["proof_command_ids"]:
            _append_unique(
                blockers,
                f"claim_safety_next_required_formal_deliverables_{safe_matrix_id}_missing_proof_commands",
            )
        if row["invalid_substitute_count"] <= 0:
            _append_unique(
                blockers,
                f"claim_safety_next_required_formal_deliverables_{safe_matrix_id}_missing_invalid_substitutes",
            )
        if claim_safety.get("formal_performance_claim_allowed") is not True and row["responsible_stage_allowed_now"] is True:
            _append_unique(
                blockers,
                f"claim_safety_next_required_formal_deliverables_{safe_matrix_id}_stage_allowed_while_blocked",
            )
    return blockers


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _claim_safety_remaining_deliverables_acceptance_summary(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_remaining_deliverables_acceptance_summary")
    summary = summary if isinstance(summary, dict) else {}
    raw_rows = summary.get("rows") if isinstance(summary.get("rows"), dict) else {}
    rows: dict[str, dict[str, Any]] = {}
    for matrix_id in CLAIM_SAFETY_REMAINING_DELIVERABLE_MATRIX_IDS:
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
            summary.get("expected_matrix_row_count") or len(CLAIM_SAFETY_REMAINING_DELIVERABLE_MATRIX_IDS)
        ),
        "missing_row_count": int(summary.get("missing_row_count") or 0),
        "blocked_category_count": int(summary.get("blocked_category_count") or 0),
        "missing_expected_matrix_ids": [str(value) for value in summary.get("missing_expected_matrix_ids", []) if value]
        if isinstance(summary.get("missing_expected_matrix_ids"), list)
        else [],
        "rows": rows,
    }


def _claim_safety_remaining_deliverables_acceptance_blockers(claim_safety: dict[str, Any]) -> list[str]:
    summary = _claim_safety_remaining_deliverables_acceptance_summary(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_remaining_deliverables_acceptance_summary")
        return blockers
    if summary["matrix_row_count"] != len(CLAIM_SAFETY_REMAINING_DELIVERABLE_MATRIX_IDS):
        blockers.append("claim_safety_remaining_deliverables_acceptance_matrix_count_mismatch")
    for matrix_id in summary["missing_expected_matrix_ids"]:
        _append_unique(blockers, f"claim_safety_remaining_deliverables_acceptance_missing_{matrix_id.replace(':', '_')}")
    if summary["missing_row_count"] > 0:
        blockers.append("claim_safety_remaining_deliverables_acceptance_rows_missing")
    if summary["blocked_category_count"] > 0:
        blockers.append("claim_safety_remaining_deliverables_acceptance_categories_blocked")
    for matrix_id, row in summary["rows"].items():
        safe_matrix_id = matrix_id.replace(":", "_")
        if not row["present"]:
            _append_unique(blockers, f"claim_safety_remaining_deliverables_acceptance_missing_{safe_matrix_id}")
            continue
        if row["acceptance_predicate_count"] <= 0:
            _append_unique(blockers, f"claim_safety_remaining_deliverables_acceptance_{safe_matrix_id}_missing_predicates")
        if row["invalid_substitute_count"] <= 0:
            _append_unique(blockers, f"claim_safety_remaining_deliverables_acceptance_{safe_matrix_id}_missing_invalid_substitutes")
    return blockers


def _claim_safety_remaining_deliverables_gap_summary(claim_safety: dict[str, Any]) -> dict[str, Any]:
    return _claim_safety_gap_summary(claim_safety.get("status_report_remaining_deliverables_gap_summary"))


def _claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_summary(
    claim_safety: dict[str, Any],
) -> dict[str, Any]:
    return _claim_safety_gap_summary(
        claim_safety.get("status_report_formal_gate_gap_audit_remaining_deliverables_gap_summary")
    )


def _claim_safety_gap_summary(raw_summary: Any) -> dict[str, Any]:
    summary = raw_summary
    summary = summary if isinstance(summary, dict) else {}
    raw_categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    categories: dict[str, dict[str, Any]] = {}
    for category in CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS:
        raw = raw_categories.get(category) if isinstance(raw_categories.get(category), dict) else {}
        categories[category] = {
            "present": bool(raw),
            "missing_count": int(raw.get("missing_count") or 0),
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now")
            if isinstance(raw.get("responsible_stage_allowed_now"), bool)
            else None,
            "missing_artifact_matrix_ids": [str(value) for value in raw.get("missing_artifact_matrix_ids", []) if value]
            if isinstance(raw.get("missing_artifact_matrix_ids"), list)
            else [],
        }
    return {
        "present": bool(summary),
        "summary_id": summary.get("summary_id"),
        "total_missing_deliverables": int(summary.get("total_missing_deliverables") or 0),
        "open_category_count": int(summary.get("open_category_count") or 0),
        "category_order": [str(value) for value in summary.get("category_order", []) if value]
        if isinstance(summary.get("category_order"), list)
        else [],
        "categories": categories,
    }


def _claim_safety_remaining_deliverables_gap_blockers(claim_safety: dict[str, Any]) -> list[str]:
    return _claim_safety_gap_blockers(
        summary=_claim_safety_remaining_deliverables_gap_summary(claim_safety),
        prefix="claim_safety_remaining_deliverables_gap",
        missing_summary_id="claim_safety_missing_remaining_deliverables_gap_summary",
    )


def _claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_blockers(
    claim_safety: dict[str, Any],
) -> list[str]:
    return _claim_safety_gap_blockers(
        summary=_claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_summary(claim_safety),
        prefix="claim_safety_formal_gate_gap_audit_remaining_deliverables_gap",
        missing_summary_id="claim_safety_missing_formal_gate_gap_audit_remaining_deliverables_gap_summary",
    )


def _claim_safety_gap_blockers(*, summary: dict[str, Any], prefix: str, missing_summary_id: str) -> list[str]:
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append(missing_summary_id)
        return blockers
    if summary["category_order"] != list(CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS):
        blockers.append(f"{prefix}_category_order_mismatch")
    if summary["total_missing_deliverables"] > 0:
        blockers.append(f"{prefix}_rows_missing")
    if summary["open_category_count"] > 0:
        blockers.append(f"{prefix}_categories_blocked")
    for category, payload in summary["categories"].items():
        if not payload["present"]:
            _append_unique(blockers, f"{prefix}_missing_{category}")
            continue
        if payload["missing_count"] != len(payload["missing_artifact_matrix_ids"]):
            _append_unique(blockers, f"{prefix}_{category}_missing_artifact_count_mismatch")
    return blockers


def _claim_safety_remaining_deliverables_proof_command_plan(claim_safety: dict[str, Any]) -> dict[str, Any]:
    summary = claim_safety.get("status_report_remaining_deliverables_proof_command_plan")
    summary = summary if isinstance(summary, dict) else {}
    raw_rows = summary.get("rows") if isinstance(summary.get("rows"), dict) else {}
    rows: dict[str, dict[str, Any]] = {}
    for matrix_id, expected_command_ids in CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_COMMAND_IDS.items():
        raw = raw_rows.get(matrix_id) if isinstance(raw_rows.get(matrix_id), dict) else {}
        command_ids = [str(value) for value in raw.get("proof_command_ids", []) if value] if isinstance(
            raw.get("proof_command_ids"), list
        ) else []
        rows[matrix_id] = {
            "present": bool(raw.get("present")),
            "proof_command_count": int(raw.get("proof_command_count") or 0),
            "expected_proof_command_count": len(expected_command_ids),
            "proof_command_ids": command_ids,
            "missing_proof_command_ids": [
                command_id for command_id in expected_command_ids if command_id not in command_ids
            ],
            "unexpected_proof_command_ids": [
                command_id for command_id in command_ids if command_id not in expected_command_ids
            ],
        }
    expected_total_proof_command_count = sum(
        len(command_ids) for command_ids in CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_COMMAND_IDS.values()
    )
    return {
        "present": bool(summary.get("present")),
        "plan_id": summary.get("plan_id"),
        "execution_boundary": summary.get("execution_boundary"),
        "not_paper_result_material": summary.get("not_paper_result_material")
        if isinstance(summary.get("not_paper_result_material"), bool)
        else None,
        "runs_training": summary.get("runs_training") if isinstance(summary.get("runs_training"), bool) else None,
        "runs_remote_preflight": summary.get("runs_remote_preflight")
        if isinstance(summary.get("runs_remote_preflight"), bool)
        else None,
        "total_matrix_rows": int(summary.get("total_matrix_rows") or 0),
        "expected_matrix_rows": len(CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_COMMAND_IDS),
        "total_proof_command_count": int(summary.get("total_proof_command_count") or 0),
        "expected_proof_command_count": expected_total_proof_command_count,
        "rows": rows,
    }


def _claim_safety_remaining_deliverables_proof_command_plan_blockers(
    claim_safety: dict[str, Any],
) -> list[str]:
    plan = _claim_safety_remaining_deliverables_proof_command_plan(claim_safety)
    blockers: list[str] = []
    if not plan["present"]:
        blockers.append("claim_safety_missing_remaining_deliverables_proof_command_plan")
        return blockers
    if plan["plan_id"] != CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_PLAN_ID:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_wrong_plan_id")
    if plan["execution_boundary"] != CLAIM_SAFETY_REMAINING_DELIVERABLE_PROOF_EXECUTION_BOUNDARY:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_wrong_execution_boundary")
    if plan["not_paper_result_material"] is not True:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_result_material")
    if plan["runs_training"] is not False:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_runs_training")
    if plan["runs_remote_preflight"] is not False:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_runs_remote_preflight")
    if plan["total_matrix_rows"] != plan["expected_matrix_rows"]:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_row_count_mismatch")
    if plan["total_proof_command_count"] != plan["expected_proof_command_count"]:
        blockers.append("claim_safety_remaining_deliverables_proof_command_plan_command_count_mismatch")
    for matrix_id, row in plan["rows"].items():
        safe_matrix_id = matrix_id.replace(":", "_")
        if not row["present"]:
            _append_unique(blockers, f"claim_safety_remaining_deliverables_proof_command_plan_missing_{safe_matrix_id}")
            continue
        if row["proof_command_count"] != row["expected_proof_command_count"] or row["proof_command_count"] != len(
            row["proof_command_ids"]
        ):
            _append_unique(
                blockers,
                f"claim_safety_remaining_deliverables_proof_command_plan_{safe_matrix_id}_command_count_mismatch",
            )
        for command_id in row["missing_proof_command_ids"]:
            _append_unique(
                blockers,
                f"claim_safety_remaining_deliverables_proof_command_plan_{safe_matrix_id}_missing_{command_id}",
            )
        if row["unexpected_proof_command_ids"]:
            _append_unique(
                blockers,
                f"claim_safety_remaining_deliverables_proof_command_plan_{safe_matrix_id}_unexpected_commands",
            )
    return blockers


def _claim_safety_remote_packet_safety_claim_gate_command_index_summary(
    claim_safety: dict[str, Any],
) -> dict[str, Any]:
    summary = claim_safety.get("status_report_remote_packet_safety_claim_gate_command_index_summary")
    summary = summary if isinstance(summary, dict) else {}
    raw_rows = summary.get("claim_gate_rows") if isinstance(summary.get("claim_gate_rows"), dict) else {}
    rows: dict[str, dict[str, Any]] = {}
    for artifact_id in CLAIM_SAFETY_CLAIM_GATE_REGENERATION_ARTIFACT_IDS:
        row = raw_rows.get(artifact_id) if isinstance(raw_rows.get(artifact_id), dict) else {}
        rows[artifact_id] = {
            "present": bool(row.get("present")),
            "stage_id": row.get("stage_id"),
            "required_before": row.get("required_before"),
            "command_kind": row.get("command_kind"),
            "command_template": row.get("command_template"),
        }
    return {
        "present": bool(summary.get("present")),
        "index_row_count": int(summary.get("index_row_count") or 0),
        "source_target_count": int(summary.get("source_target_count") or 0),
        "missing_target_ids": [str(value) for value in summary.get("missing_target_ids", []) if value]
        if isinstance(summary.get("missing_target_ids"), list)
        else [],
        "unknown_manual_count": int(summary.get("unknown_manual_count") or 0),
        "unknown_manual_ids": [str(value) for value in summary.get("unknown_manual_ids", []) if value]
        if isinstance(summary.get("unknown_manual_ids"), list)
        else [],
        "forbidden_command_count": int(summary.get("forbidden_command_count") or 0),
        "forbidden_command_ids": [str(value) for value in summary.get("forbidden_command_ids", []) if value]
        if isinstance(summary.get("forbidden_command_ids"), list)
        else [],
        "claim_gate_rows": rows,
    }


def _claim_safety_remote_packet_safety_claim_gate_command_index_blockers(
    claim_safety: dict[str, Any],
) -> list[str]:
    summary = _claim_safety_remote_packet_safety_claim_gate_command_index_summary(claim_safety)
    blockers: list[str] = []
    if not summary["present"]:
        blockers.append("claim_safety_missing_remote_packet_safety_claim_gate_command_index_summary")
        return blockers
    if summary["missing_target_ids"]:
        blockers.append("claim_safety_remote_packet_safety_command_index_missing_targets")
    if summary["unknown_manual_count"] > 0:
        blockers.append("claim_safety_remote_packet_safety_command_index_unknown_manual_rows")
    if summary["forbidden_command_count"] > 0:
        blockers.append("claim_safety_remote_packet_safety_command_index_forbidden_commands")
    for artifact_id, row in summary["claim_gate_rows"].items():
        if not row["present"]:
            _append_unique(blockers, f"claim_safety_remote_packet_safety_command_index_missing_{artifact_id}")
            continue
        if row["stage_id"] != "regenerate_claim_gate_artifacts":
            _append_unique(blockers, f"claim_safety_remote_packet_safety_command_index_{artifact_id}_wrong_stage")
        if row["required_before"] != "formal_claim_gate":
            _append_unique(
                blockers,
                f"claim_safety_remote_packet_safety_command_index_{artifact_id}_wrong_required_before",
            )
        if row["command_kind"] == "unknown_manual":
            _append_unique(blockers, f"claim_safety_remote_packet_safety_command_index_{artifact_id}_manual_command")
    return blockers


def _claim_safety_remote_packet_safety_proof_deliverables_summary(
    claim_safety: dict[str, Any],
) -> dict[str, Any]:
    return _normalize_proof_deliverables_summary(
        claim_safety.get("status_report_remote_packet_safety_proof_deliverables_summary")
    )


def _claim_safety_remote_packet_safety_status_report_proof_deliverables_summary(
    claim_safety: dict[str, Any],
) -> dict[str, Any]:
    return _normalize_proof_deliverables_summary(
        claim_safety.get("status_report_remote_packet_safety_status_report_proof_deliverables_summary")
    )


def _normalize_proof_deliverables_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    raw_counts = summary.get("missing_counts_by_formal_category")
    raw_counts = raw_counts if isinstance(raw_counts, dict) else {}
    raw_matrix_ids = summary.get("missing_matrix_ids_by_formal_category")
    raw_matrix_ids = raw_matrix_ids if isinstance(raw_matrix_ids, dict) else {}
    return {
        "present": summary.get("present") is True or bool(raw_counts or raw_matrix_ids),
        "missing_counts_by_formal_category": {
            category: int(raw_counts.get(category) or 0)
            for category in CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS
        },
        "missing_matrix_ids_by_formal_category": {
            category: _strings(raw_matrix_ids.get(category))
            for category in CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS
        },
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed"),
    }


def _proof_deliverables_signature(summary: dict[str, Any]) -> dict[str, Any]:
    matrix_ids = summary.get("missing_matrix_ids_by_formal_category")
    matrix_ids = matrix_ids if isinstance(matrix_ids, dict) else {}
    return {
        "missing_counts_by_formal_category": summary.get("missing_counts_by_formal_category"),
        "missing_matrix_ids_by_formal_category": {
            category: sorted(_strings(items))
            for category, items in matrix_ids.items()
        },
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed"),
    }


def _proof_deliverables_gap_signature(summary: dict[str, Any]) -> dict[str, Any]:
    signature = _proof_deliverables_signature(summary)
    return {
        "missing_counts_by_formal_category": signature["missing_counts_by_formal_category"],
        "missing_matrix_ids_by_formal_category": signature["missing_matrix_ids_by_formal_category"],
    }


def _proof_deliverables_signature_from_gap(summary: dict[str, Any]) -> dict[str, Any]:
    categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    return {
        "missing_counts_by_formal_category": {
            category: int(categories.get(category, {}).get("missing_count") or 0)
            for category in CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS
        },
        "missing_matrix_ids_by_formal_category": {
            category: sorted(_strings(categories.get(category, {}).get("missing_artifact_matrix_ids")))
            for category in CLAIM_SAFETY_REMAINING_DELIVERABLE_CATEGORY_IDS
        },
    }


def _proof_deliverables_missing_total(summary: dict[str, Any]) -> int:
    counts = summary.get("missing_counts_by_formal_category")
    counts = counts if isinstance(counts, dict) else {}
    return sum(int(count) for count in counts.values())


def _claim_safety_remote_packet_safety_proof_deliverables_blockers(
    claim_safety: dict[str, Any],
) -> list[str]:
    proof_summary = _claim_safety_remote_packet_safety_proof_deliverables_summary(claim_safety)
    status_report_summary = _claim_safety_remote_packet_safety_status_report_proof_deliverables_summary(claim_safety)
    gap_summary = _claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_summary(claim_safety)
    blockers: list[str] = []
    if not proof_summary["present"]:
        blockers.append("claim_safety_missing_remote_packet_safety_proof_deliverables_summary")
    if not status_report_summary["present"]:
        blockers.append("claim_safety_missing_remote_packet_safety_status_report_proof_deliverables_summary")
    if proof_summary["present"] and status_report_summary["present"]:
        if _proof_deliverables_signature(proof_summary) != _proof_deliverables_signature(status_report_summary):
            blockers.append("claim_safety_remote_packet_safety_proof_deliverables_summary_mismatch")
    if proof_summary["present"] and gap_summary["present"]:
        if _proof_deliverables_gap_signature(proof_summary) != _proof_deliverables_signature_from_gap(gap_summary):
            blockers.append("claim_safety_remote_packet_safety_proof_deliverables_summary_drifted_from_gap")
    for summary_id, summary in (
        ("proof", proof_summary),
        ("status_report_proof", status_report_summary),
    ):
        if (
            summary["present"]
            and _proof_deliverables_missing_total(summary) > 0
            and summary["h02_paper_result_input_allowed"] is True
        ):
            blockers.append(
                f"claim_safety_remote_packet_safety_{summary_id}_allows_paper_results_with_missing_deliverables"
            )
    return blockers


def _claim_safety_remote_requirement_group_blockers(
    *,
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
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            _append_unique(blockers, f"{prefix}_missing_{requirement_id}")
    return blockers


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _extend_unique(items: list[str], values: Any) -> None:
    for value in values or []:
        _append_unique(items, str(value))


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _unique(values: Sequence[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        _append_unique(out, value)
    return out


def _source_head() -> str:
    return module2_source_head()


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Paper Readiness",
        "",
        f"- status: `{manifest['status']}`",
        f"- manuscript ready: `{manifest['manuscript_ready']}`",
        f"- formal results ready: `{manifest['formal_results_ready']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        f"- remote training resource: `{manifest['remote_training_resource']}`",
        "",
        "## Global Blockers",
        "",
    ]
    if manifest["global_blockers"]:
        lines.extend(f"- `{item}`" for item in manifest["global_blockers"])
    else:
        lines.append("- none")
    input_status = manifest["input_status"]
    lines.extend(
        [
            "",
            "## Claim Safety Handoff Summary",
            "",
            f"- claim_safety_handoff_status: `{input_status.get('claim_safety_handoff_status')}`",
            f"- claim_safety_transition_gate_status: `{input_status.get('claim_safety_transition_gate_status')}`",
            f"- claim_safety_transition_gate_audit_issue_count: `{input_status.get('claim_safety_transition_gate_audit_issue_count')}`",
            f"- claim_safety_handoff_safety_issue_count: `{input_status.get('claim_safety_handoff_safety_issue_count')}`",
            "",
            "## Claim Safety Missing-Artifacts Handoff Index",
            "",
            f"- claim_safety_missing_artifacts_handoff_status: `{input_status.get('claim_safety_missing_artifacts_handoff_status')}`",
            f"- claim_safety_missing_artifacts_next_action: `{input_status.get('claim_safety_missing_artifacts_next_action')}`",
            f"- claim_safety_missing_artifacts_open_requirement_count: `{input_status.get('claim_safety_missing_artifacts_open_requirement_count')}`",
            f"- claim_safety_missing_artifacts_remote_training_allowed_now: `{input_status.get('claim_safety_missing_artifacts_remote_training_allowed_now')}`",
            f"- claim_safety_missing_artifacts_formal_result_material_allowed_now: `{input_status.get('claim_safety_missing_artifacts_formal_result_material_allowed_now')}`",
            "",
            "## Claim Safety Requirement Stage Summary",
            "",
            f"- claim_safety_requirement_stage_present: `{input_status.get('claim_safety_requirement_stage_present')}`",
            f"- claim_safety_requirement_stage_mapped_count: `{input_status.get('claim_safety_requirement_stage_mapped_count')}`",
            f"- claim_safety_requirement_stage_unmapped_count: `{input_status.get('claim_safety_requirement_stage_unmapped_count')}`",
            f"- claim_safety_requirement_stage_mismatched_count: `{input_status.get('claim_safety_requirement_stage_mismatched_count')}`",
            f"- claim_safety_requirement_stage_blocked_stage_count: `{input_status.get('claim_safety_requirement_stage_blocked_stage_count')}`",
            "",
            "## Claim Safety Remote Requirement Matrices",
            "",
            f"- claim_safety_remote_preflight_requirement_present: `{input_status.get('claim_safety_remote_preflight_requirement_present')}`",
            f"- claim_safety_remote_preflight_requirement_satisfied_count: `{input_status.get('claim_safety_remote_preflight_requirement_satisfied_count')}`",
            f"- claim_safety_remote_preflight_requirement_blocked_count: `{input_status.get('claim_safety_remote_preflight_requirement_blocked_count')}`",
            f"- claim_safety_post_run_acceptance_requirement_present: `{input_status.get('claim_safety_post_run_acceptance_requirement_present')}`",
            f"- claim_safety_post_run_acceptance_requirement_satisfied_count: `{input_status.get('claim_safety_post_run_acceptance_requirement_satisfied_count')}`",
            f"- claim_safety_post_run_acceptance_requirement_blocked_count: `{input_status.get('claim_safety_post_run_acceptance_requirement_blocked_count')}`",
            "",
            "## Claim Safety H02 Acceptance Requirement Matrix",
            "",
            f"- claim_safety_h02_formal_acceptance_requirement_present: `{input_status.get('claim_safety_h02_formal_acceptance_requirement_present')}`",
            f"- claim_safety_h02_formal_acceptance_requirement_satisfied_count: `{input_status.get('claim_safety_h02_formal_acceptance_requirement_satisfied_count')}`",
            f"- claim_safety_h02_formal_acceptance_requirement_blocked_count: `{input_status.get('claim_safety_h02_formal_acceptance_requirement_blocked_count')}`",
            "",
            "## Claim Safety F02.6 Decision Intake",
            "",
            f"- claim_safety_decision_intake_present: `{input_status.get('claim_safety_decision_intake_present')}`",
            f"- claim_safety_decision_intake_status: `{input_status.get('claim_safety_decision_intake_status')}`",
            f"- claim_safety_decision_intake_record_status: `{input_status.get('claim_safety_decision_intake_record_status')}`",
            f"- claim_safety_decision_intake_audit_issue_count: `{input_status.get('claim_safety_decision_intake_audit_issue_count')}`",
            f"- claim_safety_decision_intake_decision_owner_required: `{input_status.get('claim_safety_decision_intake_decision_owner_required')}`",
            f"- claim_safety_decision_intake_valid_decision_count: `{input_status.get('claim_safety_decision_intake_valid_decision_count')}`",
            f"- claim_safety_decision_intake_required_record_field_count: `{input_status.get('claim_safety_decision_intake_required_record_field_count')}`",
            f"- claim_safety_decision_intake_decision_note_required: `{input_status.get('claim_safety_decision_intake_decision_note_required')}`",
            f"- claim_safety_decision_intake_invalid_input_count: `{input_status.get('claim_safety_decision_intake_invalid_input_count')}`",
            f"- claim_safety_decision_intake_post_decision_non_authorization_count: `{input_status.get('claim_safety_decision_intake_post_decision_non_authorization_count')}`",
            f"- claim_safety_decision_intake_post_decision_route_count: `{input_status.get('claim_safety_decision_intake_post_decision_route_count')}`",
            f"- claim_safety_decision_intake_approved_route_next_lane: `{input_status.get('claim_safety_decision_intake_approved_route_next_lane')}`",
            f"- claim_safety_decision_intake_approved_route_allows_remote_training_now: `{input_status.get('claim_safety_decision_intake_approved_route_allows_remote_training_now')}`",
            f"- claim_safety_decision_intake_rejected_route_requires_new_protocol_contract: `{input_status.get('claim_safety_decision_intake_rejected_route_requires_new_protocol_contract')}`",
            f"- claim_safety_decision_intake_next_blocked_lane: `{input_status.get('claim_safety_decision_intake_next_blocked_lane')}`",
            f"- claim_safety_decision_intake_remote_preflight_allowed_now: `{input_status.get('claim_safety_decision_intake_remote_preflight_allowed_now')}`",
            f"- claim_safety_decision_intake_remote_training_allowed_now: `{input_status.get('claim_safety_decision_intake_remote_training_allowed_now')}`",
            f"- claim_safety_decision_intake_formal_claim_allowed_now: `{input_status.get('claim_safety_decision_intake_formal_claim_allowed_now')}`",
            "",
            "## Claim Safety Remaining Deliverables Acceptance Matrix",
            "",
            f"- claim_safety_remaining_deliverables_acceptance_present: `{input_status.get('claim_safety_remaining_deliverables_acceptance_present')}`",
            f"- claim_safety_remaining_deliverables_acceptance_matrix_row_count: `{input_status.get('claim_safety_remaining_deliverables_acceptance_matrix_row_count')}`",
            f"- claim_safety_remaining_deliverables_acceptance_missing_row_count: `{input_status.get('claim_safety_remaining_deliverables_acceptance_missing_row_count')}`",
            f"- claim_safety_remaining_deliverables_acceptance_blocked_category_count: `{input_status.get('claim_safety_remaining_deliverables_acceptance_blocked_category_count')}`",
            "",
            "## Claim Safety Remaining Deliverables Gap Summary",
            "",
            f"- claim_safety_remaining_deliverables_gap_present: `{input_status.get('claim_safety_remaining_deliverables_gap_present')}`",
            f"- claim_safety_remaining_deliverables_gap_total_missing_deliverables: `{input_status.get('claim_safety_remaining_deliverables_gap_total_missing_deliverables')}`",
            f"- claim_safety_remaining_deliverables_gap_open_category_count: `{input_status.get('claim_safety_remaining_deliverables_gap_open_category_count')}`",
            "",
            "## Claim Safety Formal Gate Gap Audit Remaining Deliverables Gap Summary",
            "",
            f"- claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_present: `{input_status.get('claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_present')}`",
            f"- claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables: `{input_status.get('claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables')}`",
            f"- claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_open_category_count: `{input_status.get('claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_open_category_count')}`",
            "",
            "## Claim Safety Remaining Deliverables Proof Command Plan",
            "",
            f"- claim_safety_remaining_deliverables_proof_command_plan_present: `{input_status.get('claim_safety_remaining_deliverables_proof_command_plan_present')}`",
            f"- claim_safety_remaining_deliverables_proof_command_plan_matrix_row_count: `{input_status.get('claim_safety_remaining_deliverables_proof_command_plan_matrix_row_count')}`",
            f"- claim_safety_remaining_deliverables_proof_command_plan_command_count: `{input_status.get('claim_safety_remaining_deliverables_proof_command_plan_command_count')}`",
            "",
            "## Claim Safety Remote-Safety Proof Deliverables Summary",
            "",
            f"- claim_safety_remote_packet_safety_proof_summary_present: `{input_status.get('claim_safety_remote_packet_safety_proof_summary_present')}`",
            f"- claim_safety_remote_packet_safety_proof_training_missing_count: `{input_status.get('claim_safety_remote_packet_safety_proof_training_missing_count')}`",
            f"- claim_safety_remote_packet_safety_proof_evaluation_missing_count: `{input_status.get('claim_safety_remote_packet_safety_proof_evaluation_missing_count')}`",
            f"- claim_safety_remote_packet_safety_proof_acceptance_missing_count: `{input_status.get('claim_safety_remote_packet_safety_proof_acceptance_missing_count')}`",
            f"- claim_safety_remote_packet_safety_proof_formal_acceptance_missing_count: `{input_status.get('claim_safety_remote_packet_safety_proof_formal_acceptance_missing_count')}`",
            f"- claim_safety_remote_packet_safety_proof_next_blocked_lane: `{input_status.get('claim_safety_remote_packet_safety_proof_next_blocked_lane')}`",
            f"- claim_safety_remote_packet_safety_proof_h02_paper_result_input_allowed: `{input_status.get('claim_safety_remote_packet_safety_proof_h02_paper_result_input_allowed')}`",
            f"- claim_safety_remote_packet_safety_status_report_proof_summary_present: `{input_status.get('claim_safety_remote_packet_safety_status_report_proof_summary_present')}`",
            "",
            "## Claim Safety Remote-Safety Claim-Gate Command Index",
            "",
            f"- claim_safety_remote_packet_safety_command_index_present: `{input_status.get('claim_safety_remote_packet_safety_command_index_present')}`",
            f"- claim_safety_remote_packet_safety_command_index_row_count: `{input_status.get('claim_safety_remote_packet_safety_command_index_row_count')}`",
            f"- claim_safety_remote_packet_safety_command_index_source_target_count: `{input_status.get('claim_safety_remote_packet_safety_command_index_source_target_count')}`",
            f"- claim_safety_remote_packet_safety_command_index_missing_target_count: `{input_status.get('claim_safety_remote_packet_safety_command_index_missing_target_count')}`",
            "",
            "## Claim Safety Next-Action Guard",
            "",
            f"- claim_safety_next_action_guard_present: `{input_status.get('claim_safety_next_action_guard_present')}`",
            f"- claim_safety_next_action_guard_status: `{input_status.get('claim_safety_next_action_guard_status')}`",
            f"- claim_safety_next_action_guard_expected_next_action_id: `{input_status.get('claim_safety_next_action_guard_expected_next_action_id')}`",
            f"- claim_safety_next_action_guard_all_execution_disabled_now: `{input_status.get('claim_safety_next_action_guard_all_execution_disabled_now')}`",
            f"- claim_safety_next_action_guard_execution_leak_count: `{input_status.get('claim_safety_next_action_guard_execution_leak_count')}`",
            f"- claim_safety_next_action_guard_violation_count: `{input_status.get('claim_safety_next_action_guard_violation_count')}`",
            "",
            "## Claim Safety Next Required Formal Deliverables",
            "",
            f"- claim_safety_next_required_formal_deliverables_present: `{input_status.get('claim_safety_next_required_formal_deliverables_present')}`",
            f"- claim_safety_next_required_formal_deliverables_status: `{input_status.get('claim_safety_next_required_formal_deliverables_status')}`",
            f"- claim_safety_next_required_formal_deliverables_total_missing: `{input_status.get('claim_safety_next_required_formal_deliverables_total_missing')}`",
            f"- claim_safety_next_required_formal_deliverables_blocked_category_count: `{input_status.get('claim_safety_next_required_formal_deliverables_blocked_category_count')}`",
            f"- claim_safety_next_required_formal_deliverables_row_count: `{input_status.get('claim_safety_next_required_formal_deliverables_row_count')}`",
        ]
    )
    lines.extend(["", "## Section Readiness", ""])
    for section in manifest["section_readiness"]:
        lines.append(f"### {section['section_id']}")
        lines.append(f"- target: {section['paper_target']}")
        lines.append(f"- status: `{section['status']}`")
        if section["blockers"]:
            lines.append("- blockers: " + ", ".join(f"`{item}`" for item in section["blockers"]))
        else:
            lines.append("- blockers: none")
        lines.append("- evidence: " + ", ".join(f"`{item}`" for item in section["evidence"]))
        lines.append("")
    lines.extend(["## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
