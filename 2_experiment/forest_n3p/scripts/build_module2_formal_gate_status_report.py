from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_status_report")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_DECISION_INTAKE = Path("0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_HANDOFF_BUNDLE = Path("0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_FORMAL_GATE_PROOF_AUDIT = Path("0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json")
DEFAULT_MAINLINE_FORMAL_GATE_STATE_AUDIT = Path(
    "0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json"
)
REMOTE_EXECUTION_STEP_IDS = (
    "sync_to_remote",
    "run_remote_preflight",
    "run_remote_training",
    "run_remote_audit",
)
REMOTE_PREFLIGHT_REQUIREMENT_IDS = (
    "f02_6_decision_closed_for_preflight",
    "approved_remote_preflight_manifest",
    "remote_preflight_protocol_contract",
    "remote_preflight_command_packetized",
)
POST_RUN_ACCEPTANCE_REQUIREMENT_IDS = (
    "pullback_expected_artifacts_complete",
    "checkpoint_hash_manifest_recorded",
    "gate3_formal_audit_accepts_remote_run",
    "h01_h02_regenerated_from_audited_checkpoint",
)
H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS = (
    "h01_schema_and_h02_output_schema_match",
    "h02_formal_scope_and_scale_match_h01",
    "gate3_audit_and_pullback_acceptance",
    "ppo_rows_and_checkpoint_hash_present",
)
CLOSURE_REMOTE_STAGE_IDS = (
    "approved_remote_preflight",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
)
FORMAL_REQUIREMENT_RESPONSIBLE_STAGES = {
    "training_remote_ppo_checkpoint": "gate3_remote_training",
    "evaluation_gate3_episode_outputs": "gate3_remote_audit_pullback",
    "acceptance_remote_pullback_and_audit": "gate3_remote_audit_pullback",
    "h01_h02_formal_evaluation_acceptance": "regenerate_h01_h02_formal_artifacts",
}
REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS = {
    "training": (
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ),
    "evaluation": (
        "eval_gate3_eval_episodes_csv",
        "eval_gate3_summary_json",
    ),
    "acceptance": (
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
    ),
    "formal_acceptance": (
        "h01_ready_for_formal_run",
        "h02_formal_output_acceptance",
    ),
}
CLAIM_GATE_REGENERATION_ARTIFACT_IDS = (
    "formal_gate_proof_summary_chain_audit",
    "mainline_formal_gate_state_audit",
    "claim_safety",
    "paper_readiness",
)


@dataclass(frozen=True)
class FormalGateStatusReportConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    decision_intake_path: Path = DEFAULT_DECISION_INTAKE
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    handoff_bundle_path: Path = DEFAULT_HANDOFF_BUNDLE
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    formal_gate_proof_audit_path: Path = DEFAULT_FORMAL_GATE_PROOF_AUDIT
    mainline_formal_gate_state_audit_path: Path = DEFAULT_MAINLINE_FORMAL_GATE_STATE_AUDIT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateStatusReportConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        formal_gate_path=args.formal_gate,
        missing_artifacts_path=args.missing_artifacts,
        closure_checklist_path=args.closure_checklist,
        decision_record_path=args.decision_record,
        decision_intake_path=args.decision_intake,
        remote_packet_path=args.remote_packet,
        h01_manifest_path=args.h01_manifest,
        h02_acceptance_path=args.h02_acceptance,
        claim_safety_path=args.claim_safety,
        paper_readiness_path=args.paper_readiness,
        handoff_bundle_path=args.handoff_bundle,
        remaining_deliverables_path=args.remaining_deliverables,
        source_freshness_path=args.source_freshness,
        formal_gate_proof_audit_path=args.formal_gate_proof_audit,
        mainline_formal_gate_state_audit_path=args.mainline_formal_gate_state_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_status_report.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_status_report.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateStatusReportConfig) -> dict[str, Any]:
    formal_gate = _read_json(config.formal_gate_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    closure_checklist = _read_json(config.closure_checklist_path)
    decision = _read_json(config.decision_record_path)
    decision_intake = _read_json(config.decision_intake_path)
    remote_packet = _read_json(config.remote_packet_path)
    h01 = _read_json(config.h01_manifest_path)
    h02 = _read_json(config.h02_acceptance_path)
    claim_safety = _read_json(config.claim_safety_path)
    paper_readiness = _read_json(config.paper_readiness_path)
    handoff_bundle = _read_json(config.handoff_bundle_path)
    remaining_deliverables = _read_json(config.remaining_deliverables_path)
    source_freshness = _read_json(config.source_freshness_path)
    formal_gate_proof_audit = _read_json(config.formal_gate_proof_audit_path)
    mainline_formal_gate_state_audit = _read_json(config.mainline_formal_gate_state_audit_path)
    remote_execution_steps = _remote_execution_step_summary(remote_packet)
    remote_preflight_requirements = _remote_requirement_matrix_summary(
        remote_packet=remote_packet,
        requirement_key="remote_preflight_requirements",
        count_key="remote_preflight_requirement_counts",
        required_ids=REMOTE_PREFLIGHT_REQUIREMENT_IDS,
    )
    post_run_acceptance_requirements = _remote_requirement_matrix_summary(
        remote_packet=remote_packet,
        requirement_key="post_run_acceptance_requirements",
        count_key="post_run_acceptance_requirement_counts",
        required_ids=POST_RUN_ACCEPTANCE_REQUIREMENT_IDS,
    )
    h02_acceptance_requirements = _h02_formal_acceptance_requirement_summary(h02)
    closure_remote_stages = _closure_remote_stage_summary(closure_checklist)
    handoff_summary = _handoff_bundle_summary(handoff_bundle)
    requirement_stage_summary = _formal_gate_requirement_stage_summary(handoff_bundle)
    missing_artifacts_handoff_summary = _missing_artifacts_handoff_index_summary(missing_artifacts)
    formal_gate_execution_veto = _formal_gate_execution_veto_summary(formal_gate)
    decision_intake_summary = _decision_intake_summary(decision_intake)
    remaining_deliverables_acceptance_summary = _remaining_deliverables_acceptance_summary(remaining_deliverables)
    remaining_deliverables_gap_summary = _remaining_deliverables_gap_summary(remaining_deliverables)
    remaining_deliverables_unlock_chain_summary = _remaining_deliverables_unlock_chain_summary(remaining_deliverables)
    next_required_formal_deliverables = _next_required_formal_deliverables(
        remaining_deliverables_gap_summary
    )
    remaining_deliverables_proof_command_plan = _remaining_deliverables_proof_command_plan(remaining_deliverables)
    formal_gate_proof_audit_summary = _formal_gate_proof_audit_summary(formal_gate_proof_audit)
    formal_gate_proof_audit_gap_summary = _formal_gate_proof_audit_gap_summary(formal_gate_proof_audit_summary)
    formal_gate_proof_audit_missing_evidence_summary = formal_gate_proof_audit_summary[
        "missing_evidence_summary"
    ]
    mainline_formal_gate_state_audit_summary = _mainline_formal_gate_state_audit_summary(
        mainline_formal_gate_state_audit
    )
    next_action_guard_summary = _next_action_guard_summary(
        decision=decision,
        decision_intake_summary=decision_intake_summary,
        handoff_summary=handoff_summary,
        missing_artifacts_handoff_summary=missing_artifacts_handoff_summary,
        remote_packet=remote_packet,
        remote_execution_steps=remote_execution_steps,
        closure_remote_stages=closure_remote_stages,
    )
    formal_gate_gap_audit_remaining_deliverables_gap_summary = (
        _formal_gate_gap_audit_remaining_deliverables_gap_summary(formal_gate)
    )
    remote_packet_safety_proof_deliverables_summary = (
        _formal_gate_remote_packet_safety_proof_deliverables_summary(formal_gate)
    )
    remote_packet_safety_status_report_proof_deliverables_summary = (
        _formal_gate_remote_packet_safety_status_report_proof_deliverables_summary(formal_gate)
    )
    remote_packet_safety_claim_gate_command_index_summary = (
        _formal_gate_remote_packet_safety_claim_gate_command_index_summary(formal_gate)
    )
    source_freshness_summary = _source_freshness_summary(source_freshness)

    input_safety_issues = _input_safety_issues(
        {
            "formal_gate": formal_gate,
            "missing_artifacts": missing_artifacts,
            "closure_checklist": closure_checklist,
            "decision_record": decision,
            "decision_intake": decision_intake,
            "remote_packet": remote_packet,
            "h01_manifest": h01,
            "h02_acceptance": h02,
            "claim_safety": claim_safety,
            "paper_readiness": paper_readiness,
            "handoff_bundle": handoff_bundle,
            "remaining_deliverables": remaining_deliverables,
            "source_freshness": source_freshness,
            "formal_gate_proof_audit": formal_gate_proof_audit,
            "mainline_formal_gate_state_audit": mainline_formal_gate_state_audit,
        }
    )
    input_safety_issues = _unique_issues(
        input_safety_issues
        + _formal_gate_execution_veto_issues(
            formal_gate=formal_gate,
            formal_gate_execution_veto=formal_gate_execution_veto,
        )
        + _remaining_deliverables_acceptance_issues(
            remaining_deliverables=remaining_deliverables,
            summary=remaining_deliverables_acceptance_summary,
        )
        + _remaining_deliverables_gap_summary_issues(
            remaining_deliverables=remaining_deliverables,
            acceptance_summary=remaining_deliverables_acceptance_summary,
            gap_summary=remaining_deliverables_gap_summary,
        )
        + _remaining_deliverables_unlock_chain_issues(
            remaining_deliverables=remaining_deliverables,
            acceptance_summary=remaining_deliverables_acceptance_summary,
            unlock_chain_summary=remaining_deliverables_unlock_chain_summary,
        )
        + _remaining_deliverables_proof_command_plan_issues(
            remaining_deliverables=remaining_deliverables,
            acceptance_summary=remaining_deliverables_acceptance_summary,
            gap_summary=remaining_deliverables_gap_summary,
            proof_plan=remaining_deliverables_proof_command_plan,
        )
        + _formal_gate_proof_audit_issues(
            proof_audit=formal_gate_proof_audit,
            summary=formal_gate_proof_audit_summary,
            proof_plan=remaining_deliverables_proof_command_plan,
        )
        + _mainline_formal_gate_state_audit_issues(mainline_formal_gate_state_audit_summary)
        + _formal_gate_gap_audit_remaining_deliverables_gap_summary_issues(
            formal_gate=formal_gate,
            formal_gate_gap_summary=formal_gate_gap_audit_remaining_deliverables_gap_summary,
            ledger_gap_summary=remaining_deliverables_gap_summary,
        )
        + _formal_gate_remote_packet_safety_proof_deliverables_summary_issues(
            formal_gate=formal_gate,
            proof_summary=remote_packet_safety_proof_deliverables_summary,
            status_report_summary=remote_packet_safety_status_report_proof_deliverables_summary,
            proof_audit_summary=formal_gate_proof_audit_summary[
                "remaining_deliverables_top_level_summary"
            ],
        )
        + _formal_gate_remote_packet_safety_claim_gate_command_index_issues(
            remote_packet_safety_claim_gate_command_index_summary
        )
        + _source_freshness_execution_issues(
            source_freshness=source_freshness,
            remote_packet=remote_packet,
            closure_checklist=closure_checklist,
        )
        + _next_action_guard_issues(next_action_guard_summary)
    )
    lanes = _lanes(
        formal_gate=formal_gate,
        missing_artifacts=missing_artifacts,
        closure_checklist=closure_checklist,
        decision=decision,
        remote_packet=remote_packet,
        h01=h01,
        h02=h02,
        claim_safety=claim_safety,
        paper_readiness=paper_readiness,
    )
    permissions = _permissions(
        formal_gate=formal_gate,
        closure_checklist=closure_checklist,
        decision=decision,
        remote_packet=remote_packet,
        h01=h01,
        h02=h02,
        claim_safety=claim_safety,
        paper_readiness=paper_readiness,
        source_freshness=source_freshness,
        input_safety_issues=input_safety_issues,
    )
    ready = all(lane["status"] == "complete" for lane in lanes) and not input_safety_issues and permissions["formal_claim_allowed_now"]
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_status_report",
        "status": "formal_gate_status_ready_for_claim_audit" if ready else "formal_gate_status_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "formal_gate_missing_artifacts": str(config.missing_artifacts_path),
            "formal_gate_closure_checklist": str(config.closure_checklist_path),
            "f02_6_decision_record": str(config.decision_record_path),
            "f02_6_decision_intake": str(config.decision_intake_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "h01_manifest": str(config.h01_manifest_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "claim_safety": str(config.claim_safety_path),
            "paper_readiness": str(config.paper_readiness_path),
            "formal_gate_handoff_bundle": str(config.handoff_bundle_path),
            "formal_gate_remaining_deliverables": str(config.remaining_deliverables_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "formal_gate_proof_audit": str(config.formal_gate_proof_audit_path),
            "mainline_formal_gate_state_audit": str(config.mainline_formal_gate_state_audit_path),
        },
        "current_state": {
            "decision_status": decision.get("status"),
            "decision_decider": decision.get("decider"),
            "decision_remote_preflight_allowed_now": decision.get("remote_preflight_allowed_now"),
            "decision_remote_training_allowed_now": decision.get("remote_training_allowed_now"),
            "decision_intake_status": decision_intake_summary["status"],
            "decision_intake_record_status": decision_intake_summary["record_status"],
            "decision_intake_next_blocked_lane": decision_intake_summary["next_blocked_lane"],
            "decision_intake_audit_issue_count": decision_intake_summary["audit_issue_count"],
            "decision_intake_valid_decision_count": decision_intake_summary["valid_decision_count"],
            "decision_intake_required_record_field_count": decision_intake_summary[
                "required_record_field_count"
            ],
            "decision_intake_decision_note_required": decision_intake_summary["decision_note_required"],
            "decision_intake_record_command_template_count": decision_intake_summary[
                "record_command_template_count"
            ],
            "decision_intake_post_decision_non_authorization_count": decision_intake_summary[
                "post_decision_non_authorization_count"
            ],
            "decision_intake_post_decision_route_count": decision_intake_summary[
                "post_decision_route_count"
            ],
        "decision_intake_remote_preflight_allowed_now": decision_intake_summary["remote_preflight_allowed_now"],
        "decision_intake_remote_training_allowed_now": decision_intake_summary["remote_training_allowed_now"],
        "decision_intake_formal_claim_allowed_now": decision_intake_summary["formal_claim_allowed_now"],
        "decision_intake_packet_authorization_status": decision_intake_summary[
            "packet_authorization_status"
        ],
        "decision_intake_packet_current_allowed_action_ids": decision_intake_summary[
            "packet_current_allowed_action_ids"
        ],
        "decision_intake_packet_current_blocked_action_ids": decision_intake_summary[
            "packet_current_blocked_action_ids"
        ],
        "decision_intake_packet_post_decision_routes_are_current_authorization": decision_intake_summary[
            "packet_post_decision_routes_are_current_authorization"
        ],
        "decision_intake_packet_remote_preflight_allowed_now": decision_intake_summary[
            "packet_remote_preflight_allowed_now"
        ],
        "decision_intake_packet_remote_training_allowed_now": decision_intake_summary[
            "packet_remote_training_allowed_now"
        ],
        "decision_intake_packet_paper_result_material_allowed_now": decision_intake_summary[
            "packet_paper_result_material_allowed_now"
        ],
        "decision_intake_next_request_status": decision_intake_summary["next_request_status"],
        "decision_intake_next_request_current_allowed_action_ids": decision_intake_summary[
            "next_request_current_allowed_action_ids"
        ],
        "decision_intake_next_request_current_blocked_action_ids": decision_intake_summary[
            "next_request_current_blocked_action_ids"
        ],
        "decision_intake_next_request_post_decision_routes_are_current_authorization": decision_intake_summary[
            "next_request_post_decision_routes_are_current_authorization"
        ],
        "decision_intake_next_request_all_execution_disabled_now": decision_intake_summary[
            "next_request_all_execution_disabled_now"
        ],
        "decision_intake_decision_impact_present": decision_intake_summary[
            "decision_impact_present"
        ],
        "decision_intake_decision_impact_current_blocker": decision_intake_summary[
            "decision_impact_current_blocker"
        ],
        "decision_intake_decision_impact_missing_deliverable_count": decision_intake_summary[
            "decision_impact_missing_deliverable_count"
        ],
        "decision_intake_decision_record_is_not_training_authorization": decision_intake_summary[
            "decision_record_is_not_training_authorization"
        ],
        "decision_intake_decision_record_is_not_paper_result_material": decision_intake_summary[
            "decision_record_is_not_paper_result_material"
        ],
        "decision_intake_decision_impact_remote_preflight_allowed_now": decision_intake_summary[
            "decision_impact_remote_preflight_allowed_now"
        ],
        "decision_intake_decision_impact_remote_training_allowed_now": decision_intake_summary[
            "decision_impact_remote_training_allowed_now"
        ],
        "decision_intake_decision_impact_formal_claim_allowed_now": decision_intake_summary[
            "decision_impact_formal_claim_allowed_now"
        ],
        "decision_intake_decision_impact_paper_result_material_allowed_now": decision_intake_summary[
            "decision_impact_paper_result_material_allowed_now"
        ],
            "formal_gate_status": formal_gate.get("status"),
            "missing_artifacts_status": missing_artifacts.get("status"),
            "missing_artifacts_handoff_index_status": missing_artifacts_handoff_summary["status"],
            "missing_artifacts_handoff_next_action": missing_artifacts_handoff_summary["next_action_id"],
            "missing_artifacts_handoff_open_requirement_count": missing_artifacts_handoff_summary["open_requirement_count"],
            "missing_artifacts_handoff_remote_training_allowed_now": missing_artifacts_handoff_summary["remote_training_allowed_now"],
            "missing_artifacts_handoff_formal_result_material_allowed_now": missing_artifacts_handoff_summary["formal_result_material_allowed_now"],
            "closure_checklist_status": closure_checklist.get("status"),
            "closure_open_item_count": closure_checklist.get("open_item_count"),
            "closure_remote_preflight_allowed_now": closure_remote_stages["approved_remote_preflight"]["allowed_now"],
            "closure_remote_training_allowed_now": closure_remote_stages["gate3_remote_training"]["allowed_now"],
            "closure_remote_audit_pullback_allowed_now": closure_remote_stages["gate3_remote_audit_pullback"]["allowed_now"],
            "remote_packet_status": remote_packet.get("status"),
            "ready_to_run_remote_training": remote_packet.get("ready_to_run_remote_training"),
            "remote_packet_sync_allowed_now": remote_execution_steps["sync_to_remote"]["allowed_now"],
            "remote_packet_preflight_allowed_now": remote_execution_steps["run_remote_preflight"]["allowed_now"],
            "remote_packet_training_allowed_now": remote_execution_steps["run_remote_training"]["allowed_now"],
            "remote_packet_audit_allowed_now": remote_execution_steps["run_remote_audit"]["allowed_now"],
            "remote_preflight_requirement_satisfied_count": remote_preflight_requirements["status_counts"].get("satisfied", 0),
            "remote_preflight_requirement_blocked_count": remote_preflight_requirements["blocked_requirement_count"],
            "post_run_acceptance_requirement_satisfied_count": post_run_acceptance_requirements["status_counts"].get("satisfied", 0),
            "post_run_acceptance_requirement_blocked_count": post_run_acceptance_requirements["blocked_requirement_count"],
            "h01_status": h01.get("status"),
            "h02_status": h02.get("status"),
            "h02_formal_output_accepted": h02.get("formal_output_accepted"),
            "h02_formal_acceptance_requirement_satisfied_count": h02_acceptance_requirements["status_counts"].get(
                "satisfied", 0
            ),
            "h02_formal_acceptance_requirement_blocked_count": h02_acceptance_requirements[
                "blocked_requirement_count"
            ],
            "claim_safety_status": claim_safety.get("status"),
            "claim_safety_formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed"),
            "paper_readiness_status": paper_readiness.get("status"),
            "paper_readiness_formal_results_ready": paper_readiness.get("formal_results_ready"),
            "handoff_bundle_status": handoff_bundle.get("status"),
            "remaining_deliverables_status": remaining_deliverables.get("status"),
            "remaining_deliverables_missing_deliverable_count": remaining_deliverables.get(
                "missing_deliverable_count"
            ),
            "remaining_deliverables_acceptance_matrix_count": remaining_deliverables_acceptance_summary[
                "matrix_row_count"
            ],
            "remaining_deliverables_acceptance_missing_row_count": remaining_deliverables_acceptance_summary[
                "missing_row_count"
            ],
            "remaining_deliverables_acceptance_blocked_category_count": remaining_deliverables_acceptance_summary[
                "blocked_category_count"
            ],
            "remaining_deliverables_unlock_chain_present": remaining_deliverables_unlock_chain_summary[
                "present"
            ],
            "remaining_deliverables_unlock_chain_row_count": remaining_deliverables_unlock_chain_summary[
                "row_count"
            ],
            "remaining_deliverables_unlock_chain_blocked_row_count": remaining_deliverables_unlock_chain_summary[
                "blocked_row_count"
            ],
            "remaining_deliverables_unlock_chain_rows_with_missing_required_blockers": remaining_deliverables_unlock_chain_summary[
                "rows_with_missing_required_blockers"
            ],
            "remaining_deliverables_unlock_chain_rows_allowed_while_missing": remaining_deliverables_unlock_chain_summary[
                "rows_allowed_while_missing"
            ],
            "remaining_deliverables_gap_total_missing_deliverable_count": remaining_deliverables_gap_summary[
                "total_missing_deliverables"
            ],
            "remaining_deliverables_gap_open_category_count": remaining_deliverables_gap_summary[
                "open_category_count"
            ],
            "next_required_formal_deliverable_count": next_required_formal_deliverables[
                "total_missing_deliverables"
            ],
            "next_required_formal_deliverable_blocked_category_count": next_required_formal_deliverables[
                "blocked_category_count"
            ],
            "remaining_deliverables_proof_plan_present": remaining_deliverables_proof_command_plan["present"],
            "remaining_deliverables_proof_plan_matrix_row_count": remaining_deliverables_proof_command_plan[
                "total_matrix_rows"
            ],
            "remaining_deliverables_proof_plan_command_count": remaining_deliverables_proof_command_plan[
                "total_proof_command_count"
            ],
            "formal_gate_proof_audit_status": formal_gate_proof_audit_summary["status"],
            "formal_gate_proof_audit_command_count": formal_gate_proof_audit_summary[
                "total_proof_command_count"
            ],
            "formal_gate_proof_audit_passed_count": formal_gate_proof_audit_summary[
                "passed_proof_command_count"
            ],
            "formal_gate_proof_audit_failed_count": formal_gate_proof_audit_summary[
                "failed_proof_command_count"
            ],
            "formal_gate_proof_audit_blocked_count": formal_gate_proof_audit_summary[
                "blocked_proof_command_count"
            ],
            "formal_gate_proof_audit_missing_artifact_count": formal_gate_proof_audit_gap_summary[
                "missing_artifact_count"
            ],
            "formal_gate_proof_audit_failed_acceptance_artifact_count": formal_gate_proof_audit_gap_summary[
                "failed_acceptance_artifact_count"
            ],
            "formal_gate_proof_audit_training_missing_artifact_count": _missing_evidence_count(
                formal_gate_proof_audit_missing_evidence_summary,
                "training",
                "missing_artifact_ids",
            ),
            "formal_gate_proof_audit_evaluation_missing_artifact_count": _missing_evidence_count(
                formal_gate_proof_audit_missing_evidence_summary,
                "evaluation",
                "missing_artifact_ids",
            ),
            "formal_gate_proof_audit_acceptance_missing_artifact_count": _missing_evidence_count(
                formal_gate_proof_audit_missing_evidence_summary,
                "acceptance",
                "missing_artifact_ids",
            ),
            "formal_gate_proof_audit_formal_acceptance_failed_artifact_count": _missing_evidence_count(
                formal_gate_proof_audit_missing_evidence_summary,
                "formal_acceptance",
                "failed_artifact_ids",
            ),
            "mainline_formal_gate_state_audit_status": mainline_formal_gate_state_audit_summary["status"],
            "mainline_formal_gate_state_audit_issue_count": mainline_formal_gate_state_audit_summary[
                "audit_issue_count"
            ],
            "mainline_formal_gate_state_audit_proof_summary_chain_status": mainline_formal_gate_state_audit_summary[
                "proof_summary_chain_status"
            ],
            "mainline_formal_gate_state_audit_proof_summary_chain_issue_count": mainline_formal_gate_state_audit_summary[
                "proof_summary_chain_audit_issue_count"
            ],
            "mainline_formal_gate_state_audit_proof_audit_input_safety_issue_count": mainline_formal_gate_state_audit_summary[
                "proof_summary_chain_proof_audit_input_safety_issue_count"
            ],
            "handoff_bundle_next_action": handoff_summary["next_handoff_action_id"],
            "handoff_bundle_safety_issue_count": handoff_summary["safety_issue_count"],
            "handoff_bundle_remote_training_allowed_now": handoff_summary["remote_training_allowed_now"],
            "handoff_requirement_stage_mapped_count": requirement_stage_summary["mapped_requirement_count"],
            "handoff_requirement_stage_unmapped_count": requirement_stage_summary["unmapped_requirement_count"],
            "formal_gate_execution_veto_present": formal_gate_execution_veto["present"],
            "formal_gate_execution_veto_all_rows_consistent": formal_gate_execution_veto["all_rows_consistent"],
            "formal_gate_execution_veto_remote_training_allowed_now": formal_gate_execution_veto["row_consensus"].get("remote_training"),
            "formal_gate_execution_veto_formal_claim_allowed_now": formal_gate_execution_veto["row_consensus"].get("formal_claim"),
            "formal_gate_gap_audit_remaining_total_missing_deliverables": formal_gate_gap_audit_remaining_deliverables_gap_summary[
                "total_missing_deliverables"
            ],
            "formal_gate_gap_audit_remaining_open_category_count": formal_gate_gap_audit_remaining_deliverables_gap_summary[
                "open_category_count"
            ],
            "remote_packet_safety_proof_summary_present": remote_packet_safety_proof_deliverables_summary[
                "present"
            ],
            "remote_packet_safety_proof_training_missing_count": remote_packet_safety_proof_deliverables_summary[
                "missing_counts_by_formal_category"
            ].get(
                "training", 0
            ),
            "remote_packet_safety_proof_evaluation_missing_count": remote_packet_safety_proof_deliverables_summary[
                "missing_counts_by_formal_category"
            ].get(
                "evaluation", 0
            ),
            "remote_packet_safety_proof_acceptance_missing_count": remote_packet_safety_proof_deliverables_summary[
                "missing_counts_by_formal_category"
            ].get(
                "acceptance", 0
            ),
            "remote_packet_safety_proof_formal_acceptance_missing_count": remote_packet_safety_proof_deliverables_summary[
                "missing_counts_by_formal_category"
            ].get(
                "formal_acceptance", 0
            ),
            "remote_packet_safety_proof_next_blocked_lane": remote_packet_safety_proof_deliverables_summary[
                "next_blocked_lane"
            ],
            "remote_packet_safety_proof_h02_paper_result_input_allowed": remote_packet_safety_proof_deliverables_summary[
                "h02_paper_result_input_allowed"
            ],
            "remote_packet_safety_status_report_proof_summary_present": remote_packet_safety_status_report_proof_deliverables_summary[
                "present"
            ],
            "source_freshness_status": source_freshness_summary["status"],
            "source_freshness_regeneration_required": source_freshness_summary[
                "regeneration_required_before_remote_formal_execution"
            ],
            "source_freshness_blocking_regeneration_required": source_freshness_summary[
                "blocking_regeneration_required_before_remote_formal_execution"
            ],
            "source_freshness_non_self_changed_records": source_freshness_summary[
                "records_with_non_self_changed_paths_since_source"
            ],
            "source_freshness_self_artifact_only_lag_records": source_freshness_summary[
                "records_with_self_artifact_only_lag"
            ],
            "remote_packet_safety_command_index_present": remote_packet_safety_claim_gate_command_index_summary[
                "present"
            ],
            "remote_packet_safety_command_index_row_count": remote_packet_safety_claim_gate_command_index_summary[
                "index_row_count"
            ],
            "remote_packet_safety_command_index_source_target_count": remote_packet_safety_claim_gate_command_index_summary[
                "source_target_count"
            ],
            "remote_packet_safety_command_index_missing_target_count": len(
                remote_packet_safety_claim_gate_command_index_summary["missing_target_ids"]
            ),
            "next_action_guard_status": next_action_guard_summary["status"],
        },
        "permissions_now": permissions,
        "missing_counts_by_category": missing_artifacts.get("missing_counts_by_category") if isinstance(missing_artifacts.get("missing_counts_by_category"), dict) else {},
        "training_artifacts_required": _artifact_list(closure_checklist, "training_artifacts_required"),
        "evaluation_artifacts_required": _artifact_list(closure_checklist, "evaluation_artifacts_required"),
        "acceptance_artifacts_required": _artifact_list(closure_checklist, "acceptance_artifacts_required"),
        "evaluation_acceptance_required": _artifact_list(closure_checklist, "evaluation_acceptance_required"),
        "claim_gate_artifacts_required": _artifact_list(closure_checklist, "claim_gate_artifacts_required"),
        "closure_remote_stage_summary": closure_remote_stages,
        "remote_execution_step_summary": remote_execution_steps,
        "remote_preflight_requirement_summary": remote_preflight_requirements,
        "post_run_acceptance_requirement_summary": post_run_acceptance_requirements,
        "h02_formal_acceptance_requirement_summary": h02_acceptance_requirements,
        "f02_6_decision_intake_summary": decision_intake_summary,
        "formal_gate_handoff_summary": handoff_summary,
        "formal_gate_requirement_stage_summary": requirement_stage_summary,
        "missing_artifacts_handoff_index_summary": missing_artifacts_handoff_summary,
        "formal_gate_execution_veto_summary": formal_gate_execution_veto,
        "remaining_deliverables_acceptance_summary": remaining_deliverables_acceptance_summary,
        "remaining_deliverables_gap_summary": remaining_deliverables_gap_summary,
        "remaining_deliverables_unlock_chain_summary": remaining_deliverables_unlock_chain_summary,
        "next_required_formal_deliverables": next_required_formal_deliverables,
        "remaining_deliverables_proof_command_plan": remaining_deliverables_proof_command_plan,
        "formal_gate_proof_audit_summary": formal_gate_proof_audit_summary,
        "formal_gate_proof_audit_remaining_deliverables_top_level_summary": (
            formal_gate_proof_audit_summary["remaining_deliverables_top_level_summary"]
        ),
        "formal_gate_proof_audit_gap_summary": formal_gate_proof_audit_gap_summary,
        "formal_gate_proof_audit_missing_evidence_summary": formal_gate_proof_audit_missing_evidence_summary,
        "mainline_formal_gate_state_audit_summary": mainline_formal_gate_state_audit_summary,
        "next_action_guard_summary": next_action_guard_summary,
        "formal_gate_gap_audit_remaining_deliverables_gap_summary": (
            formal_gate_gap_audit_remaining_deliverables_gap_summary
        ),
        "remote_packet_safety_proof_deliverables_summary": remote_packet_safety_proof_deliverables_summary,
        "remote_packet_safety_status_report_proof_deliverables_summary": (
            remote_packet_safety_status_report_proof_deliverables_summary
        ),
        "remote_packet_safety_claim_gate_command_index_summary": (
            remote_packet_safety_claim_gate_command_index_summary
        ),
        "formal_gate_lanes": lanes,
        "next_blocked_lane": _next_blocked_lane(lanes),
        "input_safety_issue_count": len(input_safety_issues),
        "input_safety_issues": input_safety_issues,
        "safe_work_without_f02_6_decision": [
            "Maintain or harden read-only gate artifacts.",
            "Add tests for gate ordering, artifact inventory, and claim blocking.",
            "Do not run approved remote preflight, formal PPO training, H02 formal evaluation, pullback, or result-claim writing.",
        ],
        "claim_boundaries": [
            "This status report is an execution-orientation artifact, not a result table or paper appendix.",
            "It does not execute commands, remote preflight, training, evaluation, sync, audit, or pullback.",
            "It must not be used to approve F02.6; only Dr Sun's decision record can do that.",
            "Formal PPO training remains gpu3070ti-relay-only and blocked until F02.6, source freshness, and remote packet gates close.",
            "Formal result writing remains blocked until H02 acceptance, claim safety, paper readiness, and the closure checklist all pass after audited pullback hashes.",
            "The formal gate execution veto matrix must agree across status, handoff, remote packet, and remote packet safety before this report can become claim-ready.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only Module2 formal gate status report.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--missing-artifacts", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--decision-intake", type=Path, default=DEFAULT_DECISION_INTAKE)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--handoff-bundle", type=Path, default=DEFAULT_HANDOFF_BUNDLE)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--formal-gate-proof-audit", type=Path, default=DEFAULT_FORMAL_GATE_PROOF_AUDIT)
    parser.add_argument(
        "--mainline-formal-gate-state-audit",
        type=Path,
        default=DEFAULT_MAINLINE_FORMAL_GATE_STATE_AUDIT,
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def _permissions(
    *,
    formal_gate: dict[str, Any],
    closure_checklist: dict[str, Any],
    decision: dict[str, Any],
    remote_packet: dict[str, Any],
    h01: dict[str, Any],
    h02: dict[str, Any],
    claim_safety: dict[str, Any],
    paper_readiness: dict[str, Any],
    source_freshness: dict[str, Any],
    input_safety_issues: Sequence[dict[str, str]],
) -> dict[str, bool]:
    decision_closed = decision.get("status") in {"approved", "rejected"} and decision.get("decider") == "Dr Sun"
    approved = decision.get("status") == "approved" and decision.get("decider") == "Dr Sun"
    remote_ready = remote_packet.get("ready_to_run_remote_training") is True
    remote_steps = _remote_execution_step_summary(remote_packet)
    remote_preflight_ready = remote_steps["run_remote_preflight"]["allowed_now"] is True
    remote_training_ready = remote_steps["run_remote_training"]["allowed_now"] is True
    h01_ready = h01.get("status") == "ready_for_formal_run"
    h02_accepted = h02.get("formal_output_accepted") is True and h02.get("paper_result_input_allowed") is True
    claim_ready = claim_safety.get("formal_performance_claim_allowed") is True
    readiness_ready = paper_readiness.get("formal_results_ready") is True
    closure_ready = closure_checklist.get("status") == "formal_gate_closure_ready_for_result_audit"
    formal_gate_ready = formal_gate.get("status") == "formal_gate_ready_for_result_audit"
    source_fresh_ready = _source_freshness_ready_for_remote_preflight(source_freshness)
    safe = not input_safety_issues
    return {
        "f02_6_decision_closed": decision_closed,
        "warm_start_formal_chain_approved": approved,
        "remote_preflight_allowed_now": approved and source_fresh_ready and remote_preflight_ready and safe,
        "remote_training_allowed_now": approved and source_fresh_ready and remote_ready and remote_training_ready and safe,
        "formal_h01_evaluation_allowed_now": h01_ready and remote_ready and safe,
        "formal_h02_acceptance_allowed_now": h01_ready and h02_accepted and safe,
        "formal_claim_allowed_now": (
            source_fresh_ready
            and formal_gate_ready
            and closure_ready
            and h02_accepted
            and claim_ready
            and readiness_ready
            and safe
        ),
        "local_training_allowed_now": False,
        "source_freshness_ready_for_remote_preflight": source_fresh_ready,
    }


def _lanes(
    *,
    formal_gate: dict[str, Any],
    missing_artifacts: dict[str, Any],
    closure_checklist: dict[str, Any],
    decision: dict[str, Any],
    remote_packet: dict[str, Any],
    h01: dict[str, Any],
    h02: dict[str, Any],
    claim_safety: dict[str, Any],
    paper_readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    checklist = {
        str(item.get("checklist_id")): item
        for item in closure_checklist.get("closure_checklist", ())
        if isinstance(item, dict)
    }
    gate_steps = {
        str(step.get("step_id")): step
        for step in formal_gate.get("ordered_next_steps", ())
        if isinstance(step, dict)
    }
    groups = {
        str(group.get("group_id")): group
        for group in missing_artifacts.get("missing_evidence_groups", ())
        if isinstance(group, dict)
    }
    return [
        _lane(
            lane_id="decision",
            phase="decision",
            primary_status=str(decision.get("status") or "missing"),
            checklist_item=checklist.get("F02.6_decision"),
            formal_step=gate_steps.get("F02.6"),
            group=groups.get("f02_6_decision_record"),
            completion_signal="F02.6 decision record is approved or rejected by Dr Sun.",
            action_when_blocked="Record Dr Sun's F02.6 decision before any formal preflight or training.",
        ),
        _lane(
            lane_id="source_fresh_preflight",
            phase="regeneration",
            primary_status=str(missing_artifacts.get("current_gate_summary", {}).get("source_freshness_status") if isinstance(missing_artifacts.get("current_gate_summary"), dict) else "unknown"),
            checklist_item=checklist.get("preflight_source_fresh_regeneration"),
            formal_step=gate_steps.get("remote_preflight"),
            group=groups.get("source_fresh_regeneration_targets"),
            completion_signal="Source-fresh preflight targets are regenerated from the current head.",
            action_when_blocked="After F02.6 closes, regenerate source-fresh gate artifacts before approved preflight.",
        ),
        _lane(
            lane_id="remote_packet_preflight",
            phase="remote_preflight",
            primary_status=str(remote_packet.get("status") or "missing"),
            checklist_item=checklist.get("approved_remote_preflight_and_packet"),
            formal_step=gate_steps.get("remote_preflight"),
            group=groups.get("post_f02_6_ordered_stages"),
            completion_signal="Approved gpu3070ti preflight passes and remote packet reports ready.",
            action_when_blocked="Run only approved remote preflight after F02.6 and source freshness close.",
        ),
        _lane(
            lane_id="gate3_remote_training",
            phase="training",
            primary_status=str(gate_steps.get("gate3_remote_training", {}).get("status") or "missing"),
            checklist_item=checklist.get("gate3_remote_training_outputs"),
            formal_step=gate_steps.get("gate3_remote_training"),
            group=groups.get("remote_training_outputs"),
            completion_signal="final_model.zip, train summary, and training manifest are pulled back.",
            action_when_blocked="Run formal PPO only on gpu3070ti-relay after remote packet is ready.",
            runs_training=True,
            host="gpu3070ti-relay",
        ),
        _lane(
            lane_id="gate3_eval_and_audit_pullback",
            phase="acceptance",
            primary_status=str(gate_steps.get("gate3_remote_audit_pullback", {}).get("status") or "missing"),
            checklist_item=checklist.get("gate3_audit_pullback_hashes"),
            formal_step=gate_steps.get("gate3_remote_audit_pullback"),
            group=groups.get("gate3_acceptance_pullback"),
            extra_group=groups.get("gate3_evaluation_outputs"),
            completion_signal="Gate3 eval outputs, trial manifest, formal audit, and checkpoint hash are present.",
            action_when_blocked="Audit remote trial and pull back the complete trial directory with hashes.",
        ),
        _lane(
            lane_id="h01_h02_formal_evaluation",
            phase="evaluation_acceptance",
            primary_status=f"h01={h01.get('status')}; h02={h02.get('status')}",
            checklist_item=checklist.get("h01_h02_formal_acceptance"),
            formal_step=gate_steps.get("h01_h02_regeneration"),
            group=groups.get("h01_h02_formal_evaluation_acceptance"),
            completion_signal="H01 is ready and H02 accepts formal-scale PPO outputs.",
            action_when_blocked="Regenerate H01/H02 only after audited checkpoint pullback is complete.",
        ),
        _lane(
            lane_id="claim_gate",
            phase="claim_gate",
            primary_status=f"claim_safety={claim_safety.get('status')}; paper_readiness={paper_readiness.get('status')}",
            checklist_item=checklist.get("claim_gate_regeneration"),
            formal_step=gate_steps.get("claim_safety_final_gate"),
            group=groups.get("claim_gate_regeneration"),
            completion_signal="Claim safety and paper readiness allow formal results after H02 acceptance.",
            action_when_blocked="Regenerate claim gates only after H02 formal acceptance passes.",
        ),
    ]


def _lane(
    *,
    lane_id: str,
    phase: str,
    primary_status: str,
    checklist_item: dict[str, Any] | None,
    formal_step: dict[str, Any] | None,
    group: dict[str, Any] | None,
    completion_signal: str,
    action_when_blocked: str,
    extra_group: dict[str, Any] | None = None,
    runs_training: bool = False,
    host: str | None = None,
) -> dict[str, Any]:
    checklist_item = checklist_item or {}
    formal_step = formal_step or {}
    group = group or {}
    missing_items = _group_missing_items(group) + _group_missing_items(extra_group or {})
    blocked_by = _unique(
        _strings(group.get("blocked_by"))
        + _strings((extra_group or {}).get("blocked_by"))
        + _strings(formal_step.get("blocked_by"))
        + _strings(checklist_item.get("blocked_by"))
    )
    complete = checklist_item.get("complete") is True and not missing_items and not blocked_by
    return {
        "lane_id": lane_id,
        "phase": phase,
        "status": "complete" if complete else "blocked",
        "primary_status": primary_status,
        "runs_training": runs_training,
        "host": host,
        "blocked_by": blocked_by,
        "missing_item_count": len(missing_items),
        "missing_items": missing_items,
        "completion_signal": completion_signal,
        "action_when_blocked": action_when_blocked,
    }


def _input_safety_issues(named_payloads: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for name, payload in named_payloads.items():
        if payload.get("executes_commands") is True:
            issues.append(_issue(f"{name}_executes_commands", f"{name} must be read-only for status reporting."))
        if payload.get("runs_training") is True:
            issues.append(_issue(f"{name}_runs_training", f"{name} must not run training as status input."))
        if payload.get("runs_remote_preflight") is True:
            issues.append(_issue(f"{name}_runs_remote_preflight", f"{name} must not run remote preflight as status input."))
        if payload.get("local_training_allowed") is True:
            issues.append(_issue(f"{name}_allows_local_training", f"{name} must preserve the local-training prohibition."))
        if payload.get("formal_claim_allowed") is True:
            issues.append(_issue(f"{name}_allows_formal_claim", f"{name} must not allow formal claims through status reporting."))
        if name == "remote_packet" and payload.get("formal_claim_allowed_before_audit") is True:
            issues.append(_issue("remote_packet_allows_claim_before_audit", "remote packet must not allow claims before audit."))
        if name == "missing_artifacts":
            issues.extend(_missing_artifacts_handoff_index_issues(payload))
        if name == "decision_intake":
            issues.extend(_decision_intake_safety_issues(payload))
        if name == "decision_record":
            issues.extend(_decision_record_safety_issues(payload))
        if name == "closure_checklist":
            issues.extend(_closure_remote_stage_safety_issues(payload))
        if name == "remote_packet":
            issues.extend(_remote_execution_step_safety_issues(payload))
            issues.extend(_remote_requirement_matrix_safety_issues(payload))
        if name == "h02_acceptance":
            issues.extend(_h02_formal_acceptance_requirement_safety_issues(payload))
        if name == "handoff_bundle":
            issues.extend(_handoff_bundle_safety_issues(payload))
    return _unique_issues(issues)


def _source_freshness_summary(source_freshness: dict[str, Any]) -> dict[str, Any]:
    commit_lag_summary = (
        source_freshness.get("commit_lag_summary")
        if isinstance(source_freshness.get("commit_lag_summary"), dict)
        else {}
    )
    return {
        "status": source_freshness.get("status"),
        "regeneration_required_before_remote_formal_execution": source_freshness.get(
            "regeneration_required_before_remote_formal_execution"
        ),
        "blocking_regeneration_required_before_remote_formal_execution": _source_freshness_blocking_regeneration_required(
            source_freshness
        ),
        "records_with_non_self_changed_paths_since_source": commit_lag_summary.get(
            "records_with_non_self_changed_paths_since_source"
        ),
        "records_with_self_artifact_only_lag": commit_lag_summary.get("records_with_self_artifact_only_lag"),
    }


def _source_freshness_ready_for_remote_preflight(source_freshness: dict[str, Any]) -> bool:
    return (
        source_freshness.get("status")
        in {
            "source_freshness_clean_current",
            "source_freshness_self_artifact_lag_only_gate_ready",
            "source_freshness_tracked_artifact_lag_only_gate_ready",
        }
        and _source_freshness_blocking_regeneration_required(source_freshness) is False
    )


def _source_freshness_blocking_regeneration_required(source_freshness: dict[str, Any]) -> bool:
    if "blocking_regeneration_required_before_remote_formal_execution" in source_freshness:
        return source_freshness.get("blocking_regeneration_required_before_remote_formal_execution") is True
    return source_freshness.get("regeneration_required_before_remote_formal_execution") is True


def _source_freshness_execution_issues(
    *,
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    closure_checklist: dict[str, Any],
) -> list[dict[str, str]]:
    if _source_freshness_ready_for_remote_preflight(source_freshness):
        return []
    remote_steps = _remote_execution_step_summary(remote_packet)
    closure_stages = _closure_remote_stage_summary(closure_checklist)
    remote_allowed = any(bool(step.get("allowed_now")) for step in remote_steps.values()) or any(
        bool(stage.get("allowed_now")) for stage in closure_stages.values()
    )
    if not remote_allowed:
        return []
    return [
        _issue(
            "source_freshness_blocks_remote_execution",
            "remote preflight/training cannot be allowed while source freshness requires regeneration.",
        )
    ]


def _decision_record_safety_issues(decision_record: dict[str, Any]) -> list[dict[str, str]]:
    if not decision_record:
        return [_issue("decision_record_missing", "status report must consume the F02.6 decision record.")]
    issues: list[dict[str, str]] = []
    if decision_record.get("status") not in {"pending_human_decision", "approved", "rejected"}:
        issues.append(_issue("decision_record_unknown_status", "F02.6 decision record status must be pending_human_decision, approved, or rejected."))
    if decision_record.get("status") == "pending_human_decision" and decision_record.get("decision_note") not in {None, ""}:
        issues.append(_issue("decision_record_pending_has_decision_note", "Pending F02.6 decision record must not contain a decision note."))
    if decision_record.get("status") in {"approved", "rejected"}:
        if decision_record.get("decider") != "Dr Sun":
            issues.append(_issue("decision_record_closed_decider_not_dr_sun", "Closed F02.6 decision record must name Dr Sun as decider."))
        if not str(decision_record.get("decision_note") or "").strip():
            issues.append(_issue("decision_record_closed_missing_decision_note", "Closed F02.6 decision record must include a non-empty decision note."))
    if decision_record.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("decision_record_allows_remote_preflight_now", "F02.6 decision record alone must not allow remote preflight now."))
    if decision_record.get("remote_training_allowed_now") is not False:
        issues.append(_issue("decision_record_allows_remote_training_now", "F02.6 decision record alone must not allow remote training now."))
    if decision_record.get("local_training_allowed") is not False:
        issues.append(_issue("decision_record_allows_local_training", "F02.6 decision record must never allow local training."))
    if decision_record.get("formal_claim_allowed") is not False:
        issues.append(_issue("decision_record_allows_formal_claim", "F02.6 decision record must not allow formal claims."))
    return issues


def _decision_intake_summary(decision_intake: dict[str, Any]) -> dict[str, Any]:
    current_state = (
        decision_intake.get("current_state")
        if isinstance(decision_intake.get("current_state"), dict)
        else {}
    )
    contract = (
        decision_intake.get("decision_intake_contract")
        if isinstance(decision_intake.get("decision_intake_contract"), dict)
        else {}
    )
    request = (
        decision_intake.get("next_human_decision_request")
        if isinstance(decision_intake.get("next_human_decision_request"), dict)
        else {}
    )
    valid_decisions = _string_list(contract.get("valid_decisions"))
    required_fields = _string_list(contract.get("required_record_fields_for_non_pending_decision"))
    command_templates = (
        contract.get("record_command_templates")
        if isinstance(contract.get("record_command_templates"), list)
        else []
    )
    human_actions = (
        contract.get("allowed_next_human_actions_from_gate_audit")
        if isinstance(contract.get("allowed_next_human_actions_from_gate_audit"), list)
        else []
    )
    invalid_inputs = (
        decision_intake.get("invalid_inputs")
        if isinstance(decision_intake.get("invalid_inputs"), list)
        else []
    )
    non_authorizations = (
        decision_intake.get("post_decision_non_authorizations")
        if isinstance(decision_intake.get("post_decision_non_authorizations"), list)
        else []
    )
    route_matrix = (
        decision_intake.get("post_decision_route_matrix")
        if isinstance(decision_intake.get("post_decision_route_matrix"), list)
        else []
    )
    impact = (
        decision_intake.get("formal_gate_decision_impact_summary")
        if isinstance(decision_intake.get("formal_gate_decision_impact_summary"), dict)
        else {}
    )
    impact_invariants = (
        impact.get("invariants_after_any_decision_record")
        if isinstance(impact.get("invariants_after_any_decision_record"), dict)
        else {}
    )
    impact_routes = (
        impact.get("decision_routes") if isinstance(impact.get("decision_routes"), list) else []
    )
    routes = {
        str(item.get("decision")): item
        for item in route_matrix
        if isinstance(item, dict) and item.get("decision")
    }
    impact_route_by_decision = {
        str(item.get("decision")): item
        for item in impact_routes
        if isinstance(item, dict) and item.get("decision")
    }
    approved_route = routes.get("approve_obstacle_summary_warm_start", {})
    rejected_route = routes.get("reject_obstacle_summary_warm_start", {})
    approved_impact = impact_route_by_decision.get("approve_obstacle_summary_warm_start", {})
    rejected_impact = impact_route_by_decision.get("reject_obstacle_summary_warm_start", {})
    return {
        "present": bool(decision_intake),
        "status": decision_intake.get("status"),
        "audit_issue_count": int(decision_intake.get("audit_issue_count") or 0),
        "record_status": current_state.get("record_status"),
        "record_decider": current_state.get("record_decider"),
        "effective_warm_start_decision": current_state.get("effective_warm_start_decision"),
        "next_blocked_lane": current_state.get("next_blocked_lane"),
        "missing_deliverable_count": current_state.get("missing_deliverable_count"),
        "remote_preflight_allowed_now": current_state.get("status_report_remote_preflight_allowed_now")
        if isinstance(current_state.get("status_report_remote_preflight_allowed_now"), bool)
        else None,
        "remote_training_allowed_now": current_state.get("status_report_remote_training_allowed_now")
        if isinstance(current_state.get("status_report_remote_training_allowed_now"), bool)
        else None,
        "formal_claim_allowed_now": current_state.get("status_report_formal_claim_allowed_now")
        if isinstance(current_state.get("status_report_formal_claim_allowed_now"), bool)
        else None,
        "local_training_allowed_now": current_state.get("status_report_local_training_allowed_now")
        if isinstance(current_state.get("status_report_local_training_allowed_now"), bool)
        else None,
        "packet_authorization_status": current_state.get("packet_authorization_status"),
        "packet_current_allowed_action_ids": _string_list(current_state.get("packet_current_allowed_action_ids")),
        "packet_current_blocked_action_ids": _string_list(current_state.get("packet_current_blocked_action_ids")),
        "packet_post_decision_routes_are_current_authorization": current_state.get(
            "packet_post_decision_routes_are_current_authorization"
        ),
        "packet_remote_preflight_allowed_now": current_state.get("packet_remote_preflight_allowed_now")
        if isinstance(current_state.get("packet_remote_preflight_allowed_now"), bool)
        else None,
        "packet_remote_training_allowed_now": current_state.get("packet_remote_training_allowed_now")
        if isinstance(current_state.get("packet_remote_training_allowed_now"), bool)
        else None,
        "packet_local_training_allowed_now": current_state.get("packet_local_training_allowed_now")
        if isinstance(current_state.get("packet_local_training_allowed_now"), bool)
        else None,
        "packet_formal_claim_allowed_now": current_state.get("packet_formal_claim_allowed_now")
        if isinstance(current_state.get("packet_formal_claim_allowed_now"), bool)
        else None,
        "packet_paper_result_material_allowed_now": current_state.get("packet_paper_result_material_allowed_now")
        if isinstance(current_state.get("packet_paper_result_material_allowed_now"), bool)
        else None,
        "next_request_status": request.get("status"),
        "next_request_decision_owner_required": request.get("decision_owner_required"),
        "next_request_valid_decisions": _string_list(request.get("valid_decisions")),
        "next_request_required_record_fields": _string_list(request.get("required_record_fields")),
        "next_request_current_allowed_action_ids": _string_list(request.get("current_allowed_action_ids")),
        "next_request_current_blocked_action_ids": _string_list(request.get("current_blocked_action_ids")),
        "next_request_post_decision_routes_are_current_authorization": request.get(
            "post_decision_routes_are_current_authorization"
        ),
        "next_request_all_execution_disabled_now": request.get("all_execution_disabled_now"),
        "decision_owner_required": contract.get("decision_owner_required"),
        "valid_decisions": valid_decisions,
        "valid_decision_count": len(valid_decisions),
        "required_record_fields": required_fields,
        "required_record_field_count": len(required_fields),
        "decision_note_required": "decision_note" in required_fields,
        "record_command_template_count": len(command_templates),
        "allowed_next_human_action_count": len(human_actions),
        "invalid_input_count": len(invalid_inputs),
        "post_decision_non_authorization_count": len(non_authorizations),
        "post_decision_route_count": len(route_matrix),
        "post_decision_route_decisions": sorted(routes),
        "approved_route_next_lane": approved_route.get("next_lane_after_record"),
        "approved_route_allows_local_training_now": approved_route.get("allows_local_training_now"),
        "approved_route_allows_remote_preflight_now": approved_route.get("allows_remote_preflight_now"),
        "approved_route_allows_remote_training_now": approved_route.get("allows_remote_training_now"),
        "approved_route_allows_formal_claim_now": approved_route.get("allows_formal_claim_now"),
        "rejected_route_next_lane": rejected_route.get("next_lane_after_record"),
        "rejected_route_allows_remote_training_now": rejected_route.get("allows_remote_training_now"),
        "rejected_route_requires_new_protocol_contract": rejected_route.get("requires_new_protocol_contract"),
        "decision_impact_present": bool(impact),
        "decision_impact_summary_id": impact.get("summary_id"),
        "decision_impact_not_paper_result_material": impact.get("not_paper_result_material"),
        "decision_impact_current_blocker": impact.get("current_blocker"),
        "decision_impact_current_record_status": impact.get("current_record_status"),
        "decision_impact_missing_deliverable_count": impact.get("missing_deliverable_count"),
        "decision_impact_current_allowed_action_ids": _string_list(impact.get("current_allowed_action_ids")),
        "decision_impact_current_blocked_action_ids": _string_list(impact.get("current_blocked_action_ids")),
        "decision_impact_route_decisions": sorted(impact_route_by_decision),
        "decision_impact_approved_route_next_lane": approved_impact.get("next_lane_after_record"),
        "decision_impact_approved_route_allows_remote_training_now": approved_impact.get(
            "allows_remote_training_now"
        ),
        "decision_impact_rejected_route_next_lane": rejected_impact.get("next_lane_after_record"),
        "decision_impact_rejected_route_requires_new_protocol_contract": rejected_impact.get(
            "requires_new_protocol_contract"
        ),
        "decision_record_is_not_training_authorization": impact_invariants.get(
            "decision_record_is_not_training_authorization"
        ),
        "decision_record_is_not_paper_result_material": impact_invariants.get(
            "decision_record_is_not_paper_result_material"
        ),
        "decision_impact_local_training_allowed_now": impact_invariants.get("local_training_allowed_now"),
        "decision_impact_remote_preflight_allowed_now": impact_invariants.get(
            "remote_preflight_allowed_now"
        ),
        "decision_impact_remote_training_allowed_now": impact_invariants.get("remote_training_allowed_now"),
        "decision_impact_formal_claim_allowed_now": impact_invariants.get("formal_claim_allowed_now"),
        "decision_impact_paper_result_material_allowed_now": impact_invariants.get(
            "paper_result_material_allowed_now"
        ),
        "decision_impact_formal_training_still_requires": _string_list(
            impact_invariants.get("formal_training_still_requires")
        ),
    }


def _decision_intake_safety_issues(decision_intake: dict[str, Any]) -> list[dict[str, str]]:
    summary = _decision_intake_summary(decision_intake)
    if not summary["present"]:
        return [_issue("decision_intake_missing", "status report must consume the F02.6 decision intake.")]
    issues: list[dict[str, str]] = []
    if summary["status"] not in {"f02_6_decision_intake_pending_clean", "f02_6_decision_intake_closed_clean"}:
        issues.append(_issue("decision_intake_not_clean", "F02.6 decision intake must be clean before status reporting."))
    if summary["audit_issue_count"] > 0:
        issues.append(_issue("decision_intake_audit_issues_open", "F02.6 decision intake reports open audit issues."))
    if summary["decision_owner_required"] != "Dr Sun":
        issues.append(_issue("decision_intake_contract_decision_owner_not_dr_sun", "F02.6 intake contract must require Dr Sun as decision owner."))
    expected_decisions = {"approve_obstacle_summary_warm_start", "reject_obstacle_summary_warm_start"}
    if not expected_decisions.issubset(set(summary["valid_decisions"])):
        issues.append(_issue("decision_intake_contract_missing_valid_decisions", "F02.6 intake contract must list approve and reject decisions."))
    expected_fields = {"decision", "decider", "decision_note"}
    if not expected_fields.issubset(set(summary["required_record_fields"])):
        issues.append(_issue("decision_intake_contract_missing_required_record_fields", "F02.6 intake contract must require decision, decider, and decision_note."))
    if summary["invalid_input_count"] == 0:
        issues.append(_issue("decision_intake_invalid_inputs_missing", "F02.6 intake must list invalid substitutes and malformed inputs."))
    if summary["post_decision_non_authorization_count"] == 0:
        issues.append(_issue("decision_intake_post_decision_non_authorizations_missing", "F02.6 intake must state what approval still does not authorize."))
    if summary["post_decision_route_count"] == 0:
        issues.append(_issue("decision_intake_post_decision_route_matrix_missing", "F02.6 intake must include approve/reject post-decision routes."))
    if not expected_decisions.issubset(set(summary["post_decision_route_decisions"])):
        issues.append(_issue("decision_intake_post_decision_route_matrix_missing_decisions", "F02.6 route matrix must include approve and reject decisions."))
    if summary["approved_route_next_lane"] != "source_fresh_regeneration":
        issues.append(_issue("decision_intake_approved_route_next_lane_invalid", "Approval must route first to source-fresh regeneration."))
    for field in (
        "approved_route_allows_local_training_now",
        "approved_route_allows_remote_preflight_now",
        "approved_route_allows_remote_training_now",
        "approved_route_allows_formal_claim_now",
    ):
        if summary[field] is not False:
            issues.append(_issue(f"decision_intake_{field}_not_false", "Approval route must not directly authorize execution or claims."))
    if summary["rejected_route_next_lane"] != "protocol_redesign":
        issues.append(_issue("decision_intake_rejected_route_next_lane_invalid", "Rejection must route to protocol redesign."))
    if summary["rejected_route_requires_new_protocol_contract"] is not True:
        issues.append(_issue("decision_intake_rejected_route_missing_protocol_contract", "Rejection route must require a new or revised protocol contract."))
    if summary["rejected_route_allows_remote_training_now"] is not False:
        issues.append(_issue("decision_intake_rejected_route_allows_remote_training", "Rejection route must keep remote training blocked."))
    if not summary["decision_impact_present"]:
        issues.append(
            _issue(
                "decision_intake_impact_summary_missing",
                "F02.6 intake must expose formal_gate_decision_impact_summary.",
            )
        )
    if summary["decision_impact_not_paper_result_material"] is not True:
        issues.append(
            _issue(
                "decision_intake_impact_is_paper_result_material",
                "F02.6 decision impact summary must not be paper result material.",
            )
        )
    if summary["decision_impact_current_allowed_action_ids"] not in (["record_f02_6_decision"], []):
        issues.append(
            _issue(
                "decision_intake_impact_allowed_actions_unexpected",
                "F02.6 decision impact summary must not allow execution actions.",
            )
        )
    for field in (
        "decision_record_is_not_training_authorization",
        "decision_record_is_not_paper_result_material",
    ):
        if summary[field] is not True:
            issues.append(
                _issue(
                    f"decision_intake_impact_{field}_not_true",
                    "F02.6 decision impact summary must state that a decision record is not execution or result evidence.",
                )
            )
    for field in (
        "decision_impact_local_training_allowed_now",
        "decision_impact_remote_preflight_allowed_now",
        "decision_impact_remote_training_allowed_now",
        "decision_impact_formal_claim_allowed_now",
        "decision_impact_paper_result_material_allowed_now",
        "decision_impact_approved_route_allows_remote_training_now",
    ):
        if summary[field] is not False:
            issues.append(
                _issue(
                    f"decision_intake_impact_{field}_not_false",
                    "F02.6 decision impact summary must not authorize execution or result material.",
                )
            )
    if summary["decision_impact_approved_route_next_lane"] != "source_fresh_regeneration":
        issues.append(
            _issue(
                "decision_intake_impact_approved_route_next_lane_invalid",
                "F02.6 approval impact must route first to source-fresh regeneration.",
            )
        )
    if summary["decision_impact_rejected_route_next_lane"] != "protocol_redesign":
        issues.append(
            _issue(
                "decision_intake_impact_rejected_route_next_lane_invalid",
                "F02.6 rejection impact must route to protocol redesign.",
            )
        )
    if summary["decision_impact_rejected_route_requires_new_protocol_contract"] is not True:
        issues.append(
            _issue(
                "decision_intake_impact_rejected_route_missing_protocol_contract",
                "F02.6 rejection impact must require a new or revised protocol contract.",
            )
        )
    for required in (
        "source_freshness_audit",
        "post_f02_6_regeneration_plan",
        "post_f02_6_plan_audit",
        "remote_formal_execution_packet_ready",
        "approved_remote_preflight",
    ):
        if required not in summary["decision_impact_formal_training_still_requires"]:
            issues.append(
                _issue(
                    f"decision_intake_impact_missing_required_{required}",
                    "F02.6 decision impact summary must list every pre-training gate still required.",
                )
            )
    record_status = summary["record_status"]
    if record_status == "pending_human_decision":
        if summary["next_blocked_lane"] != "decision":
            issues.append(_issue("decision_intake_pending_next_lane_not_decision", "pending F02.6 intake must keep the next blocked lane at decision."))
        for field in ("local_training_allowed_now", "remote_preflight_allowed_now", "remote_training_allowed_now", "formal_claim_allowed_now"):
            if summary[field] is not False:
                issues.append(_issue(f"decision_intake_{field}_not_false", "pending F02.6 intake must not allow execution or claim permissions."))
        if summary["packet_authorization_status"] != "blocked_until_dr_sun_decision":
            issues.append(_issue("decision_intake_packet_authorization_not_blocked", "pending F02.6 intake must report packet authorization blocked until Dr Sun decision."))
        if summary["packet_current_allowed_action_ids"] != ["record_f02_6_decision"]:
            issues.append(_issue("decision_intake_packet_allowed_actions_not_decision_only", "pending F02.6 packet authorization must allow only the decision record action."))
        if summary["next_request_status"] != "awaiting_dr_sun_decision":
            issues.append(_issue("decision_intake_next_request_not_awaiting_dr_sun", "pending F02.6 intake must expose an awaiting Dr Sun decision request."))
        if summary["next_request_decision_owner_required"] != "Dr Sun":
            issues.append(_issue("decision_intake_next_request_owner_not_dr_sun", "pending F02.6 decision request must require Dr Sun."))
        if not expected_decisions.issubset(set(summary["next_request_valid_decisions"])):
            issues.append(_issue("decision_intake_next_request_missing_valid_decisions", "pending F02.6 decision request must list approve and reject options."))
        if not expected_fields.issubset(set(summary["next_request_required_record_fields"])):
            issues.append(_issue("decision_intake_next_request_missing_required_fields", "pending F02.6 decision request must require decision, decider, and decision_note."))
        if summary["next_request_current_allowed_action_ids"] != ["record_f02_6_decision"]:
            issues.append(_issue("decision_intake_next_request_allowed_actions_not_decision_only", "pending F02.6 decision request must allow only the decision record action."))
        required_blocked_actions = {
            "remote_preflight",
            "remote_training",
            "local_training",
            "formal_claim",
            "paper_result_material",
        }
        missing_blocked_actions = required_blocked_actions.difference(summary["packet_current_blocked_action_ids"])
        if missing_blocked_actions:
            issues.append(_issue("decision_intake_packet_missing_blocked_actions", "pending F02.6 packet authorization must block execution and result material paths."))
        missing_request_blocked_actions = required_blocked_actions.difference(
            summary["next_request_current_blocked_action_ids"]
        )
        if missing_request_blocked_actions:
            issues.append(_issue("decision_intake_next_request_missing_blocked_actions", "pending F02.6 decision request must block execution and result material paths."))
        if summary["packet_post_decision_routes_are_current_authorization"] is not False:
            issues.append(_issue("decision_intake_packet_treats_routes_as_authorization", "post-decision routes must not be current authorization."))
        if summary["next_request_post_decision_routes_are_current_authorization"] is not False:
            issues.append(_issue("decision_intake_next_request_treats_routes_as_authorization", "decision request post-decision routes must not be current authorization."))
        if summary["next_request_all_execution_disabled_now"] is not True:
            issues.append(_issue("decision_intake_next_request_execution_not_disabled", "pending F02.6 decision request must report all execution disabled."))
        for field in (
            "packet_remote_preflight_allowed_now",
            "packet_remote_training_allowed_now",
            "packet_local_training_allowed_now",
            "packet_formal_claim_allowed_now",
            "packet_paper_result_material_allowed_now",
        ):
            if summary[field] is not False:
                issues.append(_issue(f"decision_intake_{field}_not_false", "packet current authorization must not allow execution or result material while F02.6 is pending."))
        if summary["packet_remote_preflight_allowed_now"] != summary["remote_preflight_allowed_now"]:
            issues.append(_issue("decision_intake_packet_status_report_remote_preflight_mismatch", "packet and status report must agree on pending remote preflight permission."))
        if summary["packet_remote_training_allowed_now"] != summary["remote_training_allowed_now"]:
            issues.append(_issue("decision_intake_packet_status_report_remote_training_mismatch", "packet and status report must agree on pending remote training permission."))
    elif record_status in {"approved", "rejected"}:
        if summary["record_decider"] != "Dr Sun":
            issues.append(_issue("decision_intake_closed_decider_not_dr_sun", "closed F02.6 intake must be decided by Dr Sun."))
        if summary["local_training_allowed_now"] is not False:
            issues.append(_issue("decision_intake_closed_allows_local_training", "F02.6 closure must not allow local training."))
    else:
        issues.append(_issue("decision_intake_unknown_record_status", "F02.6 intake record_status must be pending_human_decision, approved, or rejected."))
    return issues


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _missing_artifacts_handoff_index_summary(missing_artifacts: dict[str, Any]) -> dict[str, Any]:
    index = missing_artifacts.get("formal_gate_handoff_index")
    index = index if isinstance(index, dict) else {}
    next_action = index.get("next_action") if isinstance(index.get("next_action"), dict) else {}
    return {
        "present": bool(index),
        "status": index.get("status"),
        "next_action_id": next_action.get("action_id"),
        "next_action_requires_dr_sun": next_action.get("requires_dr_sun"),
        "next_action_allowed_for_agent_now": next_action.get("allowed_for_agent_now"),
        "requirement_count": index.get("requirement_count"),
        "open_requirement_count": index.get("open_requirement_count"),
        "local_training_allowed_now": bool(index.get("local_training_allowed_now")),
        "remote_training_allowed_now": bool(index.get("remote_training_allowed_now")),
        "formal_result_material_allowed_now": bool(index.get("formal_result_material_allowed_now")),
    }


def _missing_artifacts_handoff_index_issues(missing_artifacts: dict[str, Any]) -> list[dict[str, str]]:
    if not missing_artifacts:
        return []
    summary = _missing_artifacts_handoff_index_summary(missing_artifacts)
    if not summary["present"]:
        return [
            _issue(
                "missing_artifacts_handoff_index_missing",
                "formal gate missing-artifacts inventory must expose formal_gate_handoff_index.",
            )
        ]
    issues: list[dict[str, str]] = []
    inventory_open = missing_artifacts.get("status") != "formal_gate_artifacts_complete"
    if summary["local_training_allowed_now"]:
        issues.append(_issue("missing_artifacts_handoff_allows_local_training", "missing-artifacts handoff index must never allow local training."))
    if inventory_open and summary["remote_training_allowed_now"]:
        issues.append(_issue("missing_artifacts_handoff_allows_remote_training_while_open", "open missing-artifacts inventory must not allow remote training."))
    if summary["formal_result_material_allowed_now"]:
        issues.append(_issue("missing_artifacts_handoff_allows_result_material", "missing-artifacts handoff index must not allow formal result material."))
    if inventory_open and not summary["next_action_id"]:
        issues.append(_issue("missing_artifacts_handoff_missing_next_action", "open missing-artifacts handoff index must expose the next blocked action."))
    return issues


def _handoff_bundle_summary(handoff_bundle: dict[str, Any]) -> dict[str, Any]:
    permissions = handoff_bundle.get("permissions_now") if isinstance(handoff_bundle.get("permissions_now"), dict) else {}
    next_action = handoff_bundle.get("next_handoff_action") if isinstance(handoff_bundle.get("next_handoff_action"), dict) else {}
    steps = handoff_bundle.get("remote_execution_steps") if isinstance(handoff_bundle.get("remote_execution_steps"), dict) else {}
    current_state = handoff_bundle.get("current_state") if isinstance(handoff_bundle.get("current_state"), dict) else {}
    step_summary: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = steps.get(step_id) if isinstance(steps.get(step_id), dict) else {}
        step_summary[step_id] = {
            "present": bool(step),
            "allowed_now": step.get("allowed_now") if isinstance(step.get("allowed_now"), bool) else None,
            "runs_training": step.get("runs_training") if isinstance(step.get("runs_training"), bool) else None,
            "blocked_by": _strings(step.get("blocked_by")),
        }
    return {
        "present": bool(handoff_bundle),
        "status": handoff_bundle.get("status"),
        "transition_gate_status": current_state.get("transition_gate_status"),
        "transition_gate_audit_issue_count": current_state.get("transition_gate_audit_issue_count"),
        "next_handoff_action_id": next_action.get("action_id"),
        "next_action_requires_dr_sun": next_action.get("requires_dr_sun"),
        "safety_issue_count": int(handoff_bundle.get("safety_issue_count") or 0),
        "remote_training_allowed_now": bool(permissions.get("remote_training_allowed_now")),
        "remote_preflight_allowed_now": bool(permissions.get("remote_preflight_allowed_now")),
        "formal_claim_allowed_now": bool(permissions.get("formal_claim_allowed_now")),
        "remote_execution_steps": step_summary,
    }


def _next_action_guard_summary(
    *,
    decision: dict[str, Any],
    decision_intake_summary: dict[str, Any],
    handoff_summary: dict[str, Any],
    missing_artifacts_handoff_summary: dict[str, Any],
    remote_packet: dict[str, Any],
    remote_execution_steps: dict[str, dict[str, Any]],
    closure_remote_stages: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    pending = decision.get("status") == "pending_human_decision" or decision_intake_summary["record_status"] == "pending_human_decision"
    expected_action = "record_f02_6_decision" if pending else None
    execution_surfaces: list[dict[str, Any]] = []

    def add_surface(surface_id: str, allowed: Any) -> None:
        execution_surfaces.append({"surface_id": surface_id, "allowed_now": allowed if isinstance(allowed, bool) else None})

    add_surface("decision_remote_preflight_allowed_now", decision.get("remote_preflight_allowed_now"))
    add_surface("decision_remote_training_allowed_now", decision.get("remote_training_allowed_now"))
    add_surface("decision_intake_remote_preflight_allowed_now", decision_intake_summary["remote_preflight_allowed_now"])
    add_surface("decision_intake_remote_training_allowed_now", decision_intake_summary["remote_training_allowed_now"])
    add_surface("decision_intake_formal_claim_allowed_now", decision_intake_summary["formal_claim_allowed_now"])
    add_surface("handoff_remote_preflight_allowed_now", handoff_summary["remote_preflight_allowed_now"])
    add_surface("handoff_remote_training_allowed_now", handoff_summary["remote_training_allowed_now"])
    add_surface("handoff_formal_claim_allowed_now", handoff_summary["formal_claim_allowed_now"])
    add_surface("missing_artifacts_remote_training_allowed_now", missing_artifacts_handoff_summary["remote_training_allowed_now"])
    add_surface(
        "missing_artifacts_formal_result_material_allowed_now",
        missing_artifacts_handoff_summary["formal_result_material_allowed_now"],
    )
    add_surface("remote_packet_ready_to_run_remote_training", remote_packet.get("ready_to_run_remote_training"))
    for step_id, step in remote_execution_steps.items():
        add_surface(f"remote_execution_step:{step_id}", step["allowed_now"])
    for stage_id, stage in closure_remote_stages.items():
        add_surface(f"closure_remote_stage:{stage_id}", stage["allowed_now"])

    execution_leaks = [surface for surface in execution_surfaces if surface["allowed_now"] is True]
    remote_execution_allowed_count = sum(
        1 for step in remote_execution_steps.values() if step["allowed_now"] is True
    )
    remote_stage_allowed_count = sum(1 for stage in closure_remote_stages.values() if stage["allowed_now"] is True)
    violations: list[dict[str, str]] = []
    if pending and handoff_summary["next_handoff_action_id"] != expected_action:
        violations.append(
            _issue(
                "next_action_guard_unexpected_handoff_action",
                "Pending F02.6 must hand off only to record_f02_6_decision.",
            )
        )
    if pending and handoff_summary["next_action_requires_dr_sun"] is not True:
        violations.append(
            _issue(
                "next_action_guard_handoff_action_not_dr_sun_gated",
                "Pending F02.6 handoff must remain gated by Dr Sun.",
            )
        )
    if pending and missing_artifacts_handoff_summary["next_action_id"] != expected_action:
        violations.append(
            _issue(
                "next_action_guard_unexpected_missing_artifacts_action",
                "Missing-artifacts handoff must point to record_f02_6_decision while F02.6 is pending.",
            )
        )
    if pending and decision_intake_summary["next_blocked_lane"] != "decision":
        violations.append(
            _issue(
                "next_action_guard_decision_intake_lane_not_decision",
                "Decision intake must keep next_blocked_lane=decision while F02.6 is pending.",
            )
        )
    if pending and execution_leaks:
        violations.append(
            _issue(
                "next_action_guard_execution_leak",
                "Pending F02.6 must not allow preflight, training, audit, evaluation, pullback, or formal claims.",
            )
        )
    status = "next_action_guard_failed" if violations else "next_action_guard_passed"
    if not pending:
        status = "next_action_guard_not_applicable"
    return {
        "present": True,
        "status": status,
        "pending_f02_6_decision": pending,
        "next_blocked_lane_id": decision_intake_summary["next_blocked_lane"],
        "expected_next_action_id": expected_action,
        "handoff_next_action_id": handoff_summary["next_handoff_action_id"],
        "handoff_next_action_requires_dr_sun": handoff_summary["next_action_requires_dr_sun"],
        "missing_artifacts_next_action_id": missing_artifacts_handoff_summary["next_action_id"],
        "decision_intake_next_blocked_lane": decision_intake_summary["next_blocked_lane"],
        "all_execution_disabled_now": not execution_leaks,
        "execution_leak_count": len(execution_leaks),
        "remote_execution_allowed_count": remote_execution_allowed_count,
        "remote_stage_allowed_count": remote_stage_allowed_count,
        "execution_leak_surface_ids": [surface["surface_id"] for surface in execution_leaks],
        "execution_surfaces": execution_surfaces,
        "violation_count": len(violations),
        "violations": violations,
    }


def _next_action_guard_issues(summary: dict[str, Any]) -> list[dict[str, str]]:
    if summary["status"] != "next_action_guard_failed":
        return []
    return list(summary["violations"])


def _handoff_bundle_safety_issues(handoff_bundle: dict[str, Any]) -> list[dict[str, str]]:
    if not handoff_bundle:
        return [_issue("handoff_bundle_missing", "formal gate status report must consume the handoff bundle.")]
    issues: list[dict[str, str]] = []
    summary = _handoff_bundle_summary(handoff_bundle)
    issues.extend(_formal_gate_requirement_stage_issues(handoff_bundle))
    if summary["safety_issue_count"] > 0:
        issues.append(_issue("handoff_bundle_safety_issues_open", "handoff bundle reports open safety issues."))
    pending = handoff_bundle.get("current_state", {}).get("decision_status") == "pending_human_decision" if isinstance(handoff_bundle.get("current_state"), dict) else False
    if pending:
        for step_id, step in summary["remote_execution_steps"].items():
            if step["allowed_now"] is True:
                issues.append(_issue(f"handoff_bundle_pending_allows_{step_id}", "handoff bundle must not allow remote steps while F02.6 is pending."))
    if summary["remote_training_allowed_now"] and handoff_bundle.get("status") != "ready_for_manual_remote_execution_review":
        issues.append(_issue("handoff_bundle_training_allowed_without_ready_status", "handoff bundle remote training permission requires ready_for_manual_remote_execution_review."))
    training_step = summary["remote_execution_steps"].get("run_remote_training", {})
    if training_step.get("present") and training_step.get("runs_training") is not True:
        issues.append(_issue("handoff_bundle_training_step_not_marked_training", "handoff bundle run_remote_training must remain marked as training."))
    for step_id, step in summary["remote_execution_steps"].items():
        if step_id != "run_remote_training" and step.get("runs_training") is True:
            issues.append(_issue(f"handoff_bundle_{step_id}_claims_training", f"handoff bundle {step_id} must not be marked as training."))
    return issues


def _formal_gate_requirement_stage_summary(handoff_bundle: dict[str, Any]) -> dict[str, Any]:
    requirements = handoff_bundle.get("formal_gate_requirements")
    requirements = requirements if isinstance(requirements, list) else []
    by_id = {
        str(req.get("requirement_id")): req
        for req in requirements
        if isinstance(req, dict) and req.get("requirement_id")
    }
    rows: dict[str, dict[str, Any]] = {}
    for requirement_id, expected_stage_id in FORMAL_REQUIREMENT_RESPONSIBLE_STAGES.items():
        req = by_id.get(requirement_id, {})
        responsible_stage_id = req.get("responsible_stage_id")
        stage_allowed = req.get("responsible_stage_allowed_now")
        mapped = bool(responsible_stage_id)
        rows[requirement_id] = {
            "present": bool(req),
            "status": req.get("status"),
            "phase": req.get("phase"),
            "complete": req.get("complete") if isinstance(req.get("complete"), bool) else None,
            "execution_allowed_now": req.get("execution_allowed_now") if isinstance(req.get("execution_allowed_now"), bool) else None,
            "expected_stage_id": expected_stage_id,
            "responsible_stage_id": responsible_stage_id,
            "responsible_stage_status": req.get("responsible_stage_status"),
            "responsible_stage_allowed_now": stage_allowed if isinstance(stage_allowed, bool) else None,
            "responsible_stage_blocked_by": _strings(req.get("responsible_stage_blocked_by")),
            "responsible_stage_evidence_paths": _strings(req.get("responsible_stage_evidence_paths")),
            "mapping_present": mapped,
            "mapping_matches_expected": responsible_stage_id == expected_stage_id,
        }
    unmapped = [req_id for req_id, row in rows.items() if not row["mapping_present"]]
    mismatched = [req_id for req_id, row in rows.items() if row["mapping_present"] and not row["mapping_matches_expected"]]
    blocked_stage_count = sum(1 for row in rows.values() if row["responsible_stage_allowed_now"] is False)
    return {
        "required_requirement_count": len(FORMAL_REQUIREMENT_RESPONSIBLE_STAGES),
        "present_requirement_count": sum(1 for row in rows.values() if row["present"]),
        "mapped_requirement_count": sum(1 for row in rows.values() if row["mapping_present"]),
        "unmapped_requirement_count": len(unmapped),
        "mismatched_requirement_count": len(mismatched),
        "blocked_stage_count": blocked_stage_count,
        "unmapped_requirement_ids": unmapped,
        "mismatched_requirement_ids": mismatched,
        "requirements": rows,
    }


def _formal_gate_requirement_stage_issues(handoff_bundle: dict[str, Any]) -> list[dict[str, str]]:
    summary = _formal_gate_requirement_stage_summary(handoff_bundle)
    issues: list[dict[str, str]] = []
    if summary["present_requirement_count"] == 0:
        issues.append(_issue("handoff_bundle_missing_formal_gate_requirements", "handoff bundle must expose formal_gate_requirements."))
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            issues.append(_issue(f"handoff_bundle_missing_{requirement_id}", f"handoff bundle missing formal requirement {requirement_id}."))
            continue
        if not row["mapping_present"]:
            issues.append(_issue(f"handoff_bundle_{requirement_id}_missing_responsible_stage", f"{requirement_id} must expose responsible_stage_id."))
            continue
        if not row["mapping_matches_expected"]:
            issues.append(
                _issue(
                    f"handoff_bundle_{requirement_id}_wrong_responsible_stage",
                    f"{requirement_id} must map to {row['expected_stage_id']}.",
                )
            )
        if row["responsible_stage_allowed_now"] is False and not row["responsible_stage_blocked_by"]:
            issues.append(
                _issue(
                    f"handoff_bundle_{requirement_id}_stage_missing_blocked_by",
                    f"disabled responsible stage for {requirement_id} must explain blocked_by.",
                )
            )
        if row["status"] != "satisfied" and row["responsible_stage_allowed_now"] is True:
            issues.append(
                _issue(
                    f"handoff_bundle_{requirement_id}_stage_ready_while_requirement_blocked",
                    f"responsible stage for blocked requirement {requirement_id} must not be ready.",
                )
            )
    return issues


def _formal_gate_execution_veto_summary(formal_gate: dict[str, Any]) -> dict[str, Any]:
    veto = formal_gate.get("execution_veto_matrix") if isinstance(formal_gate.get("execution_veto_matrix"), dict) else {}
    rows = veto.get("rows") if isinstance(veto.get("rows"), list) else []
    row_summary: dict[str, dict[str, Any]] = {}
    row_consensus: dict[str, bool | None] = {}
    for row in rows:
        if not isinstance(row, dict) or not row.get("row_id"):
            continue
        row_id = str(row["row_id"])
        row_summary[row_id] = {
            "consistent": row.get("consistent") if isinstance(row.get("consistent"), bool) else None,
            "consensus_allowed_now": row.get("consensus_allowed_now") if isinstance(row.get("consensus_allowed_now"), bool) else None,
            "allowed_now_by_source": row.get("allowed_now_by_source") if isinstance(row.get("allowed_now_by_source"), dict) else {},
        }
        row_consensus[row_id] = row_summary[row_id]["consensus_allowed_now"]
    return {
        "present": bool(veto),
        "matrix_version": veto.get("matrix_version"),
        "f02_6_decision_status": veto.get("f02_6_decision_status"),
        "all_rows_consistent": veto.get("all_rows_consistent") if isinstance(veto.get("all_rows_consistent"), bool) else None,
        "mismatch_rows": _strings(veto.get("mismatch_rows")),
        "row_count": len(row_summary),
        "row_consensus": row_consensus,
        "rows": row_summary,
    }


def _formal_gate_execution_veto_issues(
    *,
    formal_gate: dict[str, Any],
    formal_gate_execution_veto: dict[str, Any],
) -> list[dict[str, str]]:
    if not formal_gate_execution_veto["present"]:
        return [_issue("formal_gate_missing_execution_veto_matrix", "formal gate gap audit must expose execution_veto_matrix.")]
    issues: list[dict[str, str]] = []
    if formal_gate_execution_veto["all_rows_consistent"] is not True:
        issues.append(_issue("formal_gate_execution_veto_rows_inconsistent", "formal gate execution veto matrix has inconsistent rows."))
    if formal_gate_execution_veto["mismatch_rows"]:
        issues.append(_issue("formal_gate_execution_veto_mismatch_rows_open", "formal gate execution veto matrix reports mismatch rows."))
    required_rows = {
        "local_training",
        "remote_preflight",
        "remote_training",
        "remote_audit",
        "formal_claim",
    }
    observed_rows = set(formal_gate_execution_veto["rows"])
    for row_id in sorted(required_rows - observed_rows):
        issues.append(_issue(f"formal_gate_execution_veto_missing_{row_id}", f"formal gate execution veto matrix missing row {row_id}."))
    blocked_gate = formal_gate.get("status") != "formal_gate_ready_for_result_audit"
    if blocked_gate:
        for row_id in ("local_training", "remote_preflight", "remote_training", "remote_audit", "formal_claim"):
            if formal_gate_execution_veto["row_consensus"].get(row_id) is True:
                issues.append(_issue(f"blocked_formal_gate_execution_veto_allows_{row_id}", f"blocked formal gate must not allow {row_id}."))
    return issues


def _closure_remote_stage_summary(closure_checklist: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = closure_checklist.get("post_plan_remote_stage_summary")
    stages = raw if isinstance(raw, dict) else {}
    summary: dict[str, dict[str, Any]] = {}
    for stage_id in CLOSURE_REMOTE_STAGE_IDS:
        stage = stages.get(stage_id) if isinstance(stages.get(stage_id), dict) else {}
        summary[stage_id] = {
            "present": bool(stage),
            "status": stage.get("status"),
            "allowed_now": stage.get("allowed_now") if isinstance(stage.get("allowed_now"), bool) else None,
            "runs_training": stage.get("runs_training") if isinstance(stage.get("runs_training"), bool) else None,
            "runs_remote_preflight": stage.get("runs_remote_preflight") if isinstance(stage.get("runs_remote_preflight"), bool) else None,
            "host": stage.get("host"),
            "blocked_by": _strings(stage.get("blocked_by")),
        }
    return summary


def _closure_remote_stage_safety_issues(closure_checklist: dict[str, Any]) -> list[dict[str, str]]:
    raw = closure_checklist.get("post_plan_remote_stage_summary")
    if not isinstance(raw, dict):
        return [_issue("closure_checklist_missing_remote_stage_summary", "closure checklist must expose post_plan_remote_stage_summary.")]
    summary = _closure_remote_stage_summary(closure_checklist)
    issues: list[dict[str, str]] = []
    for stage_id, stage in summary.items():
        if not stage["present"]:
            issues.append(_issue(f"closure_checklist_missing_{stage_id}", f"closure checklist missing remote stage {stage_id}."))
            continue
        if stage["allowed_now"] is False and not stage["blocked_by"]:
            issues.append(_issue(f"closure_checklist_{stage_id}_missing_blocked_by", f"disabled closure remote stage {stage_id} must explain blocked_by."))
        if stage["allowed_now"] is True and stage["blocked_by"]:
            issues.append(_issue(f"closure_checklist_{stage_id}_allowed_with_blockers", f"allowed closure remote stage {stage_id} must not carry blocked_by."))
    training = summary.get("gate3_remote_training", {})
    if training.get("runs_training") is not True:
        issues.append(_issue("closure_checklist_training_stage_not_marked_training", "gate3_remote_training must remain marked as training."))
    for stage_id in ("approved_remote_preflight", "gate3_remote_audit_pullback"):
        if summary.get(stage_id, {}).get("runs_training") is True:
            issues.append(_issue(f"closure_checklist_{stage_id}_claims_training", f"{stage_id} must not be marked as training."))
    preflight = summary.get("approved_remote_preflight", {})
    if preflight.get("runs_remote_preflight") is not True:
        issues.append(_issue("closure_checklist_preflight_stage_not_marked_preflight", "approved_remote_preflight must remain marked as remote preflight."))
    for stage_id, stage in summary.items():
        if (stage.get("runs_training") is True or stage.get("runs_remote_preflight") is True) and stage.get("host") != "gpu3070ti-relay":
            issues.append(_issue(f"closure_checklist_{stage_id}_wrong_host", f"{stage_id} must run only on gpu3070ti-relay."))
    return issues


def _remote_execution_step_summary(remote_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    steps = remote_packet.get("execution_steps") if isinstance(remote_packet.get("execution_steps"), dict) else {}
    summary: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = steps.get(step_id) if isinstance(steps.get(step_id), dict) else {}
        summary[step_id] = {
            "present": bool(step),
            "allowed_now": step.get("allowed_now") if isinstance(step.get("allowed_now"), bool) else None,
            "runs_training": step.get("runs_training") if isinstance(step.get("runs_training"), bool) else None,
            "blocked_by": _strings(step.get("blocked_by")),
        }
    return summary


def _remote_execution_step_safety_issues(remote_packet: dict[str, Any]) -> list[dict[str, str]]:
    steps = remote_packet.get("execution_steps")
    if not isinstance(steps, dict):
        return [_issue("remote_packet_missing_execution_steps", "remote packet must expose execution_steps for status reporting.")]
    issues: list[dict[str, str]] = []
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = steps.get(step_id)
        if not isinstance(step, dict):
            issues.append(_issue(f"remote_packet_missing_{step_id}", f"remote packet missing execution step {step_id}."))
            continue
        blockers = _strings(step.get("blocked_by"))
        if step.get("allowed_now") is False and not blockers:
            issues.append(_issue(f"remote_packet_{step_id}_missing_blocked_by", f"disabled remote step {step_id} must explain blocked_by."))
        if step.get("allowed_now") is True and blockers:
            issues.append(_issue(f"remote_packet_{step_id}_allowed_with_blockers", f"allowed remote step {step_id} must not carry blocked_by."))
        if step_id == "run_remote_training" and step.get("runs_training") is not True:
            issues.append(_issue("remote_packet_training_step_not_marked_training", "run_remote_training must remain marked as the only training step."))
        if step_id != "run_remote_training" and step.get("runs_training") is True:
            issues.append(_issue(f"remote_packet_{step_id}_claims_training", f"{step_id} must not be marked as a training step."))
    return issues


def _remote_requirement_matrix_summary(
    *,
    remote_packet: dict[str, Any],
    requirement_key: str,
    count_key: str,
    required_ids: Sequence[str],
) -> dict[str, Any]:
    requirements = remote_packet.get(requirement_key)
    raw_requirements = requirements if isinstance(requirements, list) else []
    by_id = {str(item.get("requirement_id")): item for item in raw_requirements if isinstance(item, dict)}
    rows: dict[str, dict[str, Any]] = {}
    for requirement_id in required_ids:
        row = by_id.get(requirement_id, {})
        rows[requirement_id] = {
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
            "required_before": row.get("required_before"),
            "missing_artifact_ids": _strings(row.get("missing_artifact_ids")),
            "blocked_by": _strings(row.get("blocked_by")),
            "acceptable_evidence_count": len(_strings(row.get("acceptable_evidence"))),
            "invalid_substitute_count": len(_strings(row.get("invalid_substitutes"))),
        }
    status_counts = (
        remote_packet.get(count_key)
        if isinstance(remote_packet.get(count_key), dict)
        else _requirement_status_counts(rows)
    )
    return {
        "present": isinstance(requirements, list),
        "required_requirement_count": len(required_ids),
        "present_requirement_count": sum(1 for row in rows.values() if row["present"]),
        "blocked_requirement_count": sum(
            1 for row in rows.values() if row["present"] and row["status"] not in {None, "satisfied"}
        ),
        "status_counts": status_counts,
        "missing_requirement_ids": [requirement_id for requirement_id, row in rows.items() if not row["present"]],
        "requirements": rows,
    }


def _remaining_deliverables_acceptance_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    raw_rows = remaining_deliverables.get("deliverable_acceptance_matrix")
    rows_list = raw_rows if isinstance(raw_rows, list) else []
    expected_by_category = REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS
    row_by_matrix_id = {
        str(row.get("matrix_id")): row
        for row in rows_list
        if isinstance(row, dict) and row.get("matrix_id")
    }
    rows: dict[str, dict[str, Any]] = {}
    missing_expected_ids: list[str] = []
    for category, artifact_ids in expected_by_category.items():
        for artifact_id in artifact_ids:
            matrix_id = f"{category}:{artifact_id}"
            raw = row_by_matrix_id.get(matrix_id, {})
            if not raw:
                missing_expected_ids.append(matrix_id)
            rows[matrix_id] = {
                "present": bool(raw),
                "category": category,
                "artifact_id": artifact_id,
                "expected_path": raw.get("expected_path"),
                "current_exists": raw.get("current_exists") if isinstance(raw.get("current_exists"), bool) else None,
                "current_state": raw.get("current_state"),
                "missing": raw.get("missing") if isinstance(raw.get("missing"), bool) else None,
                "responsible_stage_id": raw.get("responsible_stage_id"),
                "responsible_stage_status": raw.get("responsible_stage_status"),
                "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now")
                if isinstance(raw.get("responsible_stage_allowed_now"), bool)
                else None,
                "responsible_stage_blocked_by": _strings(raw.get("responsible_stage_blocked_by")),
                "acceptance_predicate_count": len(_strings(raw.get("acceptance_predicates"))),
                "proof_command_count": len(_proof_commands(raw.get("proof_commands"))),
                "proof_command_ids": [
                    command["command_id"]
                    for command in _proof_commands(raw.get("proof_commands"))
                    if command.get("command_id")
                ],
                "acceptable_evidence_count": len(_strings(raw.get("acceptable_evidence"))),
                "invalid_substitute_count": len(_strings(raw.get("invalid_substitutes"))),
                "execution_boundary": raw.get("execution_boundary"),
            }
    category_counts = remaining_deliverables.get("category_counts")
    category_counts = category_counts if isinstance(category_counts, dict) else {}
    blocked_categories = [
        str(category)
        for category, payload in category_counts.items()
        if isinstance(payload, dict) and int(payload.get("missing_count") or 0) > 0
    ]
    return {
        "present": bool(rows_list),
        "status": remaining_deliverables.get("status"),
        "missing_deliverable_count": int(remaining_deliverables.get("missing_deliverable_count") or 0),
        "matrix_row_count": len(rows_list),
        "expected_matrix_row_count": sum(len(ids) for ids in expected_by_category.values()),
        "missing_row_count": sum(1 for row in rows.values() if row["missing"] is True),
        "blocked_category_count": len(blocked_categories),
        "blocked_categories": blocked_categories,
        "missing_expected_matrix_ids": missing_expected_ids,
        "permissions_now": remaining_deliverables.get("permissions_now")
        if isinstance(remaining_deliverables.get("permissions_now"), dict)
        else {},
        "rows": rows,
    }


def _remaining_deliverables_gap_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    raw_summary = remaining_deliverables.get("deliverable_gap_summary")
    raw_summary = raw_summary if isinstance(raw_summary, dict) else {}
    raw_categories = raw_summary.get("categories")
    raw_categories = raw_categories if isinstance(raw_categories, list) else []
    categories: dict[str, dict[str, Any]] = {}
    for category in REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS:
        raw = next(
            (
                item
                for item in raw_categories
                if isinstance(item, dict) and item.get("category") == category
            ),
            {},
        )
        missing_artifacts_raw = raw.get("missing_artifacts")
        missing_artifacts_raw = missing_artifacts_raw if isinstance(missing_artifacts_raw, list) else []
        missing_artifacts = []
        for item in missing_artifacts_raw:
            if not isinstance(item, dict):
                continue
            invalid_substitutes = item.get("invalid_substitutes")
            proof_command_ids = _strings(item.get("proof_command_ids"))
            missing_artifacts.append(
                {
                    "matrix_id": item.get("matrix_id"),
                    "artifact_id": item.get("artifact_id"),
                    "expected_path": item.get("expected_path"),
                    "current_state": item.get("current_state"),
                    "missing_reason": item.get("missing_reason"),
                    "acceptance_predicate_count": int(item.get("acceptance_predicate_count") or 0),
                    "proof_command_count": int(item.get("proof_command_count") or 0),
                    "proof_command_ids": proof_command_ids,
                    "invalid_substitute_count": len(invalid_substitutes)
                    if isinstance(invalid_substitutes, list)
                    else 0,
                }
            )
        categories[category] = {
            "present": bool(raw),
            "status": raw.get("status"),
            "missing_count": int(raw.get("missing_count") or 0),
            "present_count": int(raw.get("present_count") or 0),
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now")
            if isinstance(raw.get("responsible_stage_allowed_now"), bool)
            else None,
            "responsible_stage_blocked_by": _strings(raw.get("responsible_stage_blocked_by")),
            "next_required_evidence_count": len(_strings(raw.get("next_required_evidence"))),
            "missing_artifact_count": len(missing_artifacts),
            "missing_artifact_matrix_ids": [
                str(item["matrix_id"]) for item in missing_artifacts if item.get("matrix_id")
            ],
            "proof_command_ids": _unique(
                command_id
                for item in missing_artifacts
                for command_id in item.get("proof_command_ids", [])
            ),
            "missing_artifacts": missing_artifacts,
        }
    return {
        "present": bool(raw_summary),
        "summary_id": raw_summary.get("summary_id"),
        "execution_boundary": raw_summary.get("execution_boundary"),
        "not_paper_result_material": raw_summary.get("not_paper_result_material") is True,
        "total_missing_deliverables": int(raw_summary.get("total_missing_deliverables") or 0),
        "open_category_count": int(raw_summary.get("open_category_count") or 0),
        "category_order": _strings(raw_summary.get("category_order")),
        "categories": categories,
    }


def _next_required_formal_deliverables(gap_summary: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    categories = gap_summary.get("categories") if isinstance(gap_summary.get("categories"), dict) else {}
    category_order = _strings(gap_summary.get("category_order")) or list(REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS)
    for category in category_order:
        payload = categories.get(category) if isinstance(categories.get(category), dict) else {}
        for item in payload.get("missing_artifacts", []):
            if not isinstance(item, dict) or not item.get("matrix_id"):
                continue
            rows.append(
                {
                    "matrix_id": item.get("matrix_id"),
                    "category": category,
                    "artifact_id": item.get("artifact_id"),
                    "expected_path": item.get("expected_path"),
                    "current_state": item.get("current_state"),
                    "missing_reason": item.get("missing_reason"),
                    "responsible_stage_id": payload.get("responsible_stage_id"),
                    "responsible_stage_allowed_now": payload.get("responsible_stage_allowed_now"),
                    "responsible_stage_blocked_by": _strings(payload.get("responsible_stage_blocked_by")),
                    "proof_command_ids": _strings(item.get("proof_command_ids")),
                    "invalid_substitute_count": int(item.get("invalid_substitute_count") or 0),
                }
            )
    blocked_categories = [
        category
        for category in category_order
        if isinstance(categories.get(category), dict)
        and categories[category].get("missing_count", 0) > 0
        and categories[category].get("responsible_stage_allowed_now") is False
    ]
    return {
        "present": bool(gap_summary.get("present")),
        "status": "blocked_missing_formal_deliverables" if rows else "no_missing_formal_deliverables",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_missing_deliverables": len(rows),
        "blocked_category_count": len(blocked_categories),
        "blocked_categories": blocked_categories,
        "category_order": category_order,
        "rows": rows,
    }


def _remaining_deliverables_proof_command_plan(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    raw_plan = remaining_deliverables.get("proof_command_plan")
    raw_plan = raw_plan if isinstance(raw_plan, dict) else {}
    raw_rows = raw_plan.get("rows")
    raw_rows = raw_rows if isinstance(raw_rows, list) else []
    rows: dict[str, dict[str, Any]] = {}
    for raw in raw_rows:
        if not isinstance(raw, dict) or not raw.get("matrix_id"):
            continue
        matrix_id = str(raw["matrix_id"])
        rows[matrix_id] = {
            "present": True,
            "category": raw.get("category"),
            "artifact_id": raw.get("artifact_id"),
            "expected_path": raw.get("expected_path"),
            "proof_command_count": int(raw.get("proof_command_count") or 0),
            "proof_command_ids": _strings(raw.get("proof_command_ids")),
        }
    return {
        "present": bool(raw_plan),
        "plan_id": raw_plan.get("plan_id"),
        "execution_boundary": raw_plan.get("execution_boundary"),
        "not_paper_result_material": raw_plan.get("not_paper_result_material") is True,
        "runs_training": raw_plan.get("runs_training") is True,
        "runs_remote_preflight": raw_plan.get("runs_remote_preflight") is True,
        "total_matrix_rows": int(raw_plan.get("total_matrix_rows") or 0),
        "total_proof_command_count": int(raw_plan.get("total_proof_command_count") or 0),
        "rows": rows,
    }


def _remaining_deliverables_unlock_chain_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    raw_chain = remaining_deliverables.get("deliverable_unlock_chain")
    raw_chain = raw_chain if isinstance(raw_chain, dict) else {}
    raw_rows = raw_chain.get("rows")
    raw_rows = raw_rows if isinstance(raw_rows, list) else []
    rows: dict[str, dict[str, Any]] = {}
    categories: dict[str, dict[str, Any]] = {}
    for raw in raw_rows:
        if not isinstance(raw, dict) or not raw.get("matrix_id"):
            continue
        matrix_id = str(raw["matrix_id"])
        category = str(raw.get("category") or "unknown")
        row = {
            "present": True,
            "matrix_id": matrix_id,
            "category": category,
            "artifact_id": raw.get("artifact_id"),
            "current_state": raw.get("current_state"),
            "missing": raw.get("missing") if isinstance(raw.get("missing"), bool) else raw.get("current_state") == "missing",
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now")
            if isinstance(raw.get("responsible_stage_allowed_now"), bool)
            else None,
            "required_current_blockers": _strings(raw.get("required_current_blockers")),
            "missing_required_current_blockers": _strings(raw.get("missing_required_current_blockers")),
            "unlock_sequence_before_stage_allowed": _strings(raw.get("unlock_sequence_before_stage_allowed")),
            "execution_boundary": raw.get("execution_boundary"),
        }
        rows[matrix_id] = row
        category_summary = categories.setdefault(
            category,
            {
                "row_count": 0,
                "blocked_row_count": 0,
                "rows_with_missing_required_blockers": 0,
                "rows_allowed_while_missing": 0,
                "required_current_blockers": [],
                "unlock_sequence_before_stage_allowed": [],
            },
        )
        category_summary["row_count"] += 1
        if row["missing"] is True and row["responsible_stage_allowed_now"] is not True:
            category_summary["blocked_row_count"] += 1
        if row["missing_required_current_blockers"]:
            category_summary["rows_with_missing_required_blockers"] += 1
        if row["missing"] is True and row["responsible_stage_allowed_now"] is True:
            category_summary["rows_allowed_while_missing"] += 1
        category_summary["required_current_blockers"] = _unique(
            [*category_summary["required_current_blockers"], *row["required_current_blockers"]]
        )
        category_summary["unlock_sequence_before_stage_allowed"] = _unique(
            [*category_summary["unlock_sequence_before_stage_allowed"], *row["unlock_sequence_before_stage_allowed"]]
        )
    derived_blocked_row_count = sum(
        1 for row in rows.values() if row["missing"] is True and row["responsible_stage_allowed_now"] is not True
    )
    derived_missing_blockers = sum(1 for row in rows.values() if row["missing_required_current_blockers"])
    derived_allowed_while_missing = sum(
        1 for row in rows.values() if row["missing"] is True and row["responsible_stage_allowed_now"] is True
    )
    return {
        "present": bool(raw_chain),
        "chain_id": raw_chain.get("chain_id"),
        "status": raw_chain.get("status"),
        "not_paper_result_material": raw_chain.get("not_paper_result_material") is True,
        "execution_boundary": raw_chain.get("execution_boundary"),
        "row_count": int(raw_chain.get("row_count") or 0),
        "derived_row_count": len(rows),
        "blocked_row_count": int(raw_chain.get("blocked_row_count") or 0),
        "derived_blocked_row_count": derived_blocked_row_count,
        "rows_with_missing_required_blockers": derived_missing_blockers,
        "rows_allowed_while_missing": derived_allowed_while_missing,
        "declared_rows_with_missing_required_blockers": int(raw_chain.get("rows_with_missing_required_blockers") or 0),
        "declared_rows_allowed_while_missing": int(raw_chain.get("rows_allowed_while_missing") or 0),
        "categories": categories,
        "rows": rows,
    }


def _formal_gate_proof_audit_summary(proof_audit: dict[str, Any]) -> dict[str, Any]:
    raw_results = proof_audit.get("proof_command_results")
    raw_results = raw_results if isinstance(raw_results, list) else []
    results_by_id: dict[str, dict[str, Any]] = {}
    for raw in raw_results:
        if not isinstance(raw, dict) or not raw.get("command_id"):
            continue
        command_id = str(raw["command_id"])
        results_by_id[command_id] = {
            "present": True,
            "matrix_id": raw.get("matrix_id"),
            "category": raw.get("category"),
            "artifact_id": raw.get("artifact_id"),
            "status": raw.get("status"),
            "expected_path": raw.get("expected_path"),
            "command_was_executed": raw.get("command_was_executed") is True,
            "diagnostic": raw.get("diagnostic"),
        }
    raw_counts = proof_audit.get("category_status_counts")
    raw_counts = raw_counts if isinstance(raw_counts, dict) else {}
    category_status_counts: dict[str, dict[str, int]] = {}
    for category, counts in raw_counts.items():
        if not isinstance(counts, dict):
            continue
        category_status_counts[str(category)] = {
            "passed": int(counts.get("passed") or 0),
            "failed": int(counts.get("failed") or 0),
            "blocked_missing_artifact": int(counts.get("blocked_missing_artifact") or 0),
        }
    return {
        "present": bool(proof_audit),
        "status": proof_audit.get("status"),
        "not_paper_result_material": proof_audit.get("not_paper_result_material") is True,
        "executes_commands": proof_audit.get("executes_commands") is True,
        "runs_training": proof_audit.get("runs_training") is True,
        "runs_remote_preflight": proof_audit.get("runs_remote_preflight") is True,
        "formal_claim_allowed": proof_audit.get("formal_claim_allowed") is True,
        "proof_command_plan_id": proof_audit.get("proof_command_plan_id"),
        "execution_boundary": proof_audit.get("execution_boundary"),
        "total_matrix_rows": int(proof_audit.get("total_matrix_rows") or 0),
        "total_proof_command_count": int(proof_audit.get("total_proof_command_count") or 0),
        "declared_total_proof_command_count": int(proof_audit.get("declared_total_proof_command_count") or 0),
        "passed_proof_command_count": int(proof_audit.get("passed_proof_command_count") or 0),
        "failed_proof_command_count": int(proof_audit.get("failed_proof_command_count") or 0),
        "blocked_proof_command_count": int(proof_audit.get("blocked_proof_command_count") or 0),
        "category_status_counts": category_status_counts,
        "blockers": _strings(proof_audit.get("blockers")),
        "input_safety_issue_count": int(proof_audit.get("input_safety_issue_count") or 0),
        "results_by_id": results_by_id,
        "remaining_deliverables_top_level_summary": _proof_audit_remaining_deliverables_top_level_summary(
            proof_audit
        ),
        "missing_evidence_summary": _formal_gate_proof_audit_missing_evidence_summary(
            proof_audit=proof_audit,
            results_by_id=results_by_id,
        ),
    }


def _mainline_formal_gate_state_audit_summary(mainline_audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "present": bool(mainline_audit),
        "status": mainline_audit.get("status"),
        "not_paper_result_material": mainline_audit.get("not_paper_result_material") is True,
        "executes_commands": mainline_audit.get("executes_commands") is True,
        "runs_training": mainline_audit.get("runs_training") is True,
        "runs_remote_preflight": mainline_audit.get("runs_remote_preflight") is True,
        "local_training_allowed": mainline_audit.get("local_training_allowed") is True,
        "formal_claim_allowed": mainline_audit.get("formal_claim_allowed") is True,
        "audit_issue_count": int(mainline_audit.get("audit_issue_count") or 0),
        "proof_summary_chain_status": mainline_audit.get("proof_summary_chain_status"),
        "proof_summary_chain_audit_issue_count": int(
            mainline_audit.get("proof_summary_chain_audit_issue_count") or 0
        ),
        "proof_summary_chain_proof_audit_input_safety_issue_count": int(
            mainline_audit.get("proof_summary_chain_proof_audit_input_safety_issue_count") or 0
        ),
        "proof_summary_chain_proof_audit_blockers": _strings(
            mainline_audit.get("proof_summary_chain_proof_audit_blockers")
        ),
    }


def _proof_audit_remaining_deliverables_top_level_summary(proof_audit: dict[str, Any]) -> dict[str, Any]:
    return _normalize_proof_deliverables_summary(proof_audit.get("remaining_deliverables_top_level_summary"))


def _normalize_proof_deliverables_summary(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    raw_counts = raw.get("missing_counts_by_formal_category")
    raw_counts = raw_counts if isinstance(raw_counts, dict) else {}
    raw_matrix_ids = raw.get("missing_matrix_ids_by_formal_category")
    raw_matrix_ids = raw_matrix_ids if isinstance(raw_matrix_ids, dict) else {}
    return {
        "present": raw.get("present") is True or bool(raw_counts or raw_matrix_ids),
        "missing_counts_by_formal_category": {
            str(category): int(count) for category, count in raw_counts.items()
        },
        "missing_matrix_ids_by_formal_category": {
            str(category): [str(item) for item in items] if isinstance(items, list) else []
            for category, items in raw_matrix_ids.items()
        },
        "next_blocked_lane": raw.get("next_blocked_lane"),
        "h01_status": raw.get("h01_status"),
        "h02_status": raw.get("h02_status"),
        "h02_formal_output_accepted": raw.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": raw.get("h02_paper_result_input_allowed"),
    }


def _proof_deliverables_signature(summary: dict[str, Any]) -> dict[str, Any]:
    matrix_ids = summary.get("missing_matrix_ids_by_formal_category")
    matrix_ids = matrix_ids if isinstance(matrix_ids, dict) else {}
    return {
        "missing_counts_by_formal_category": summary.get("missing_counts_by_formal_category"),
        "missing_matrix_ids_by_formal_category": {
            str(category): sorted(str(item) for item in items)
            for category, items in matrix_ids.items()
            if isinstance(items, list)
        },
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed"),
    }


def _proof_deliverables_missing_total(summary: dict[str, Any]) -> int:
    counts = summary.get("missing_counts_by_formal_category")
    counts = counts if isinstance(counts, dict) else {}
    return sum(int(count) for count in counts.values())


def _formal_gate_proof_audit_missing_evidence_summary(
    *,
    proof_audit: dict[str, Any],
    results_by_id: dict[str, dict[str, Any]],
) -> dict[str, dict[str, list[str]]]:
    raw = proof_audit.get("formal_gate_missing_evidence_summary")
    if isinstance(raw, dict):
        return _normalize_missing_evidence_summary(raw)
    summary = _empty_missing_evidence_summary()
    for result in results_by_id.values():
        category = str(result.get("category") or "")
        if category not in summary:
            summary[category] = {"missing_artifact_ids": [], "failed_artifact_ids": []}
        artifact_id = str(result.get("artifact_id") or "")
        if not artifact_id:
            continue
        if result.get("status") == "blocked_missing_artifact":
            summary[category]["missing_artifact_ids"].append(artifact_id)
        elif result.get("status") == "failed":
            summary[category]["failed_artifact_ids"].append(artifact_id)
    return {
        category: {
            "missing_artifact_ids": _unique(payload["missing_artifact_ids"]),
            "failed_artifact_ids": _unique(payload["failed_artifact_ids"]),
        }
        for category, payload in summary.items()
    }


def _normalize_missing_evidence_summary(raw: dict[str, Any]) -> dict[str, dict[str, list[str]]]:
    summary = _empty_missing_evidence_summary()
    for category, payload in raw.items():
        if not isinstance(payload, dict):
            continue
        category_key = str(category)
        summary[category_key] = {
            "missing_artifact_ids": _strings(payload.get("missing_artifact_ids")),
            "failed_artifact_ids": _strings(payload.get("failed_artifact_ids")),
        }
    return summary


def _empty_missing_evidence_summary() -> dict[str, dict[str, list[str]]]:
    return {
        category: {"missing_artifact_ids": [], "failed_artifact_ids": []}
        for category in REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS
    }


def _missing_evidence_count(summary: dict[str, dict[str, list[str]]], category: str, key: str) -> int:
    payload = summary.get(category)
    if not isinstance(payload, dict):
        return 0
    values = payload.get(key)
    return len(values) if isinstance(values, list) else 0


def _formal_gate_proof_audit_gap_summary(summary: dict[str, Any]) -> dict[str, Any]:
    categories: dict[str, dict[str, Any]] = {
        category: {
            "missing_artifact_count": 0,
            "failed_acceptance_artifact_count": 0,
            "blocked_proof_command_count": 0,
            "failed_proof_command_count": 0,
            "missing_artifact_ids": [],
            "failed_artifact_ids": [],
            "blocked_proof_command_ids": [],
            "failed_proof_command_ids": [],
            "expected_paths": [],
        }
        for category in REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS
    }
    for command_id, result in summary["results_by_id"].items():
        category = str(result.get("category") or "")
        if category not in categories:
            continue
        payload = categories[category]
        status = result.get("status")
        artifact_id = str(result.get("artifact_id") or "")
        expected_path = str(result.get("expected_path") or "")
        if status == "blocked_missing_artifact":
            payload["blocked_proof_command_ids"].append(command_id)
            if artifact_id:
                payload["missing_artifact_ids"].append(artifact_id)
            if expected_path:
                payload["expected_paths"].append(expected_path)
        elif status == "failed":
            payload["failed_proof_command_ids"].append(command_id)
            if artifact_id:
                payload["failed_artifact_ids"].append(artifact_id)
            if expected_path:
                payload["expected_paths"].append(expected_path)
    for payload in categories.values():
        payload["missing_artifact_ids"] = _unique(payload["missing_artifact_ids"])
        payload["failed_artifact_ids"] = _unique(payload["failed_artifact_ids"])
        payload["blocked_proof_command_ids"] = _unique(payload["blocked_proof_command_ids"])
        payload["failed_proof_command_ids"] = _unique(payload["failed_proof_command_ids"])
        payload["expected_paths"] = _unique(payload["expected_paths"])
        payload["missing_artifact_count"] = len(payload["missing_artifact_ids"])
        payload["failed_acceptance_artifact_count"] = len(payload["failed_artifact_ids"])
        payload["blocked_proof_command_count"] = len(payload["blocked_proof_command_ids"])
        payload["failed_proof_command_count"] = len(payload["failed_proof_command_ids"])
    return {
        "present": summary["present"],
        "status": summary["status"],
        "total_proof_command_count": summary["total_proof_command_count"],
        "passed_proof_command_count": summary["passed_proof_command_count"],
        "failed_proof_command_count": summary["failed_proof_command_count"],
        "blocked_proof_command_count": summary["blocked_proof_command_count"],
        "missing_artifact_count": sum(
            payload["missing_artifact_count"] for payload in categories.values()
        ),
        "failed_acceptance_artifact_count": sum(
            payload["failed_acceptance_artifact_count"] for payload in categories.values()
        ),
        "category_order": list(REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS),
        "categories": categories,
    }


def _formal_gate_gap_audit_remaining_deliverables_gap_summary(formal_gate: dict[str, Any]) -> dict[str, Any]:
    return _normalize_gap_summary(formal_gate.get("remaining_deliverables_gap_summary"))


def _normalize_gap_summary(raw: Any) -> dict[str, Any]:
    raw_summary = raw if isinstance(raw, dict) else {}
    raw_categories = raw_summary.get("categories")
    if isinstance(raw_categories, dict):
        raw_items = raw_categories.items()
    elif isinstance(raw_categories, list):
        raw_items = ((item.get("category"), item) for item in raw_categories if isinstance(item, dict))
    else:
        raw_items = ()
    categories: dict[str, dict[str, Any]] = {
        category: {
            "present": False,
            "status": None,
            "missing_count": 0,
            "present_count": 0,
            "responsible_stage_id": None,
            "responsible_stage_allowed_now": None,
            "responsible_stage_blocked_by": [],
            "next_required_evidence_count": 0,
            "missing_artifact_count": 0,
            "missing_artifact_matrix_ids": [],
            "missing_artifacts": [],
        }
        for category in REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS
    }
    for category_key, raw_category in raw_items:
        category = str(category_key) if category_key else ""
        if category not in categories or not isinstance(raw_category, dict):
            continue
        missing_artifacts_raw = raw_category.get("missing_artifacts")
        missing_artifacts_raw = missing_artifacts_raw if isinstance(missing_artifacts_raw, list) else []
        matrix_ids = raw_category.get("missing_artifact_matrix_ids")
        if not isinstance(matrix_ids, list):
            matrix_ids = [item.get("matrix_id") for item in missing_artifacts_raw if isinstance(item, dict)]
        categories[category] = {
            "present": True,
            "status": raw_category.get("status"),
            "missing_count": int(raw_category.get("missing_count") or 0),
            "present_count": int(raw_category.get("present_count") or 0),
            "responsible_stage_id": raw_category.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw_category.get("responsible_stage_allowed_now")
            if isinstance(raw_category.get("responsible_stage_allowed_now"), bool)
            else None,
            "responsible_stage_blocked_by": _strings(raw_category.get("responsible_stage_blocked_by")),
            "next_required_evidence_count": len(_strings(raw_category.get("next_required_evidence"))),
            "missing_artifact_count": len([item for item in missing_artifacts_raw if isinstance(item, dict)])
            if missing_artifacts_raw
            else len([item for item in matrix_ids if item]),
            "missing_artifact_matrix_ids": [str(item) for item in matrix_ids if item],
            "missing_artifacts": [],
        }
    return {
        "present": bool(raw_summary),
        "summary_id": raw_summary.get("summary_id"),
        "execution_boundary": raw_summary.get("execution_boundary"),
        "not_paper_result_material": raw_summary.get("not_paper_result_material") is True,
        "total_missing_deliverables": int(raw_summary.get("total_missing_deliverables") or 0),
        "open_category_count": int(raw_summary.get("open_category_count") or 0),
        "category_order": _strings(raw_summary.get("category_order")),
        "categories": categories,
    }


def _gap_signature(summary: dict[str, Any]) -> dict[str, Any]:
    categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    return {
        "summary_id": summary.get("summary_id"),
        "total_missing_deliverables": summary.get("total_missing_deliverables"),
        "open_category_count": summary.get("open_category_count"),
        "category_order": summary.get("category_order"),
        "categories": {
            key: {
                "missing_count": value.get("missing_count"),
                "responsible_stage_id": value.get("responsible_stage_id"),
                "missing_artifact_matrix_ids": value.get("missing_artifact_matrix_ids", []),
            }
            for key, value in sorted(categories.items())
            if isinstance(value, dict)
        },
    }


def _formal_gate_remote_packet_safety_proof_deliverables_summary(formal_gate: dict[str, Any]) -> dict[str, Any]:
    remote_safety = formal_gate.get("remote_packet_safety") if isinstance(formal_gate.get("remote_packet_safety"), dict) else {}
    return _normalize_proof_deliverables_summary(remote_safety.get("proof_deliverables_summary"))


def _formal_gate_remote_packet_safety_status_report_proof_deliverables_summary(
    formal_gate: dict[str, Any],
) -> dict[str, Any]:
    remote_safety = formal_gate.get("remote_packet_safety") if isinstance(formal_gate.get("remote_packet_safety"), dict) else {}
    return _normalize_proof_deliverables_summary(remote_safety.get("status_report_proof_deliverables_summary"))


def _formal_gate_remote_packet_safety_proof_deliverables_summary_issues(
    *,
    formal_gate: dict[str, Any],
    proof_summary: dict[str, Any],
    status_report_summary: dict[str, Any],
    proof_audit_summary: dict[str, Any],
) -> list[dict[str, str]]:
    if not formal_gate:
        return [_issue("formal_gate_gap_audit_missing", "status report must consume formal gate gap audit.")]
    issues: list[dict[str, str]] = []
    if not proof_summary["present"]:
        issues.append(
            _issue(
                "formal_gate_remote_packet_safety_missing_proof_deliverables_summary",
                "formal gate gap audit must forward remote packet safety proof-deliverables summary.",
            )
        )
    if not status_report_summary["present"]:
        issues.append(
            _issue(
                "formal_gate_remote_packet_safety_missing_status_report_proof_deliverables_summary",
                "formal gate gap audit must forward the status-report proof-deliverables summary from remote packet safety.",
            )
        )
    if proof_summary["present"] and status_report_summary["present"]:
        if _proof_deliverables_signature(proof_summary) != _proof_deliverables_signature(status_report_summary):
            issues.append(
                _issue(
                    "formal_gate_remote_packet_safety_proof_deliverables_summary_mismatch",
                    "remote packet safety proof summary and status-report proof summary must match.",
                )
            )
    if proof_summary["present"] and proof_audit_summary["present"]:
        if _proof_deliverables_signature(proof_summary) != _proof_deliverables_signature(proof_audit_summary):
            issues.append(
                _issue(
                    "formal_gate_remote_packet_safety_proof_deliverables_summary_drifted_from_proof_audit",
                    "remote packet safety proof summary must match the local proof-audit top-level deliverable summary.",
                )
            )
    for summary_id, summary in (
        ("proof", proof_summary),
        ("status_report_proof", status_report_summary),
    ):
        if (
            summary["present"]
            and _proof_deliverables_missing_total(summary) > 0
            and summary["h02_paper_result_input_allowed"] is True
        ):
            issues.append(
                _issue(
                    f"formal_gate_remote_packet_safety_{summary_id}_allows_paper_results_with_missing_deliverables",
                    "remote packet safety proof summary must not allow paper result input while formal deliverables are missing.",
                )
            )
    return issues


def _formal_gate_remote_packet_safety_claim_gate_command_index_summary(formal_gate: dict[str, Any]) -> dict[str, Any]:
    remote_safety = formal_gate.get("remote_packet_safety") if isinstance(formal_gate.get("remote_packet_safety"), dict) else {}
    summary = (
        remote_safety.get("claim_gate_command_index_summary")
        if isinstance(remote_safety.get("claim_gate_command_index_summary"), dict)
        else {}
    )
    rows = summary.get("claim_gate_rows") if isinstance(summary.get("claim_gate_rows"), dict) else {}
    claim_gate_rows: dict[str, dict[str, Any]] = {}
    for artifact_id in CLAIM_GATE_REGENERATION_ARTIFACT_IDS:
        row = rows.get(artifact_id) if isinstance(rows.get(artifact_id), dict) else {}
        claim_gate_rows[artifact_id] = {
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
        "missing_target_ids": _strings(summary.get("missing_target_ids")),
        "unknown_manual_count": int(summary.get("unknown_manual_count") or 0),
        "unknown_manual_ids": _strings(summary.get("unknown_manual_ids")),
        "forbidden_command_count": int(summary.get("forbidden_command_count") or 0),
        "forbidden_command_ids": _strings(summary.get("forbidden_command_ids")),
        "claim_gate_rows": claim_gate_rows,
    }


def _formal_gate_remote_packet_safety_claim_gate_command_index_issues(
    summary: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not summary["present"]:
        return [
            _issue(
                "formal_gate_missing_remote_packet_safety_command_index_summary",
                "formal gate must forward remote packet safety claim-gate command index summary.",
            )
        ]
    if summary["missing_target_ids"]:
        issues.append(
            _issue(
                "formal_gate_remote_packet_safety_command_index_missing_targets",
                "remote packet safety command index reports missing source targets.",
            )
        )
    if summary["unknown_manual_count"] > 0:
        issues.append(
            _issue(
                "formal_gate_remote_packet_safety_command_index_unknown_manual_rows",
                "remote packet safety command index reports unknown manual rows.",
            )
        )
    if summary["forbidden_command_count"] > 0:
        issues.append(
            _issue(
                "formal_gate_remote_packet_safety_command_index_forbidden_commands",
                "remote packet safety command index contains forbidden execution commands.",
            )
        )
    for artifact_id, row in summary["claim_gate_rows"].items():
        if not row["present"]:
            if artifact_id not in summary["missing_target_ids"]:
                continue
            issues.append(
                _issue(
                    f"formal_gate_remote_packet_safety_command_index_missing_{artifact_id}",
                    f"remote packet safety command index must include {artifact_id}.",
                )
            )
            continue
        if row["stage_id"] != "regenerate_claim_gate_artifacts":
            issues.append(
                _issue(
                    f"formal_gate_remote_packet_safety_command_index_{artifact_id}_wrong_stage",
                    f"{artifact_id} must regenerate in regenerate_claim_gate_artifacts.",
                )
            )
        if row["required_before"] != "formal_claim_gate":
            issues.append(
                _issue(
                    f"formal_gate_remote_packet_safety_command_index_{artifact_id}_wrong_required_before",
                    f"{artifact_id} must be required before formal_claim_gate.",
                )
            )
        if row["command_kind"] == "unknown_manual":
            issues.append(
                _issue(
                    f"formal_gate_remote_packet_safety_command_index_{artifact_id}_manual_command",
                    f"{artifact_id} must use a known builder command in the safety command index.",
                )
            )
    return issues


def _remaining_deliverables_acceptance_issues(
    *,
    remaining_deliverables: dict[str, Any],
    summary: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not remaining_deliverables:
        return [_issue("remaining_deliverables_missing", "status report must consume remaining-deliverables ledger.")]
    if not summary["present"]:
        return [
            _issue(
                "remaining_deliverables_acceptance_matrix_missing",
                "remaining-deliverables ledger must expose deliverable_acceptance_matrix.",
            )
        ]
    if summary["matrix_row_count"] != summary["expected_matrix_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_acceptance_matrix_count_mismatch",
                "remaining-deliverables acceptance matrix must cover all expected formal-gate deliverables.",
            )
        )
    for matrix_id in summary["missing_expected_matrix_ids"]:
        safe_matrix_id = matrix_id.replace(":", "_")
        issues.append(_issue(f"remaining_deliverables_acceptance_missing_{safe_matrix_id}", f"missing matrix row {matrix_id}."))
    permissions = summary["permissions_now"]
    if permissions.get("local_training_allowed_now") is True:
        issues.append(_issue("remaining_deliverables_allows_local_training", "remaining-deliverables must not allow local training."))
    if permissions.get("remote_training_allowed_now") is True and summary["status"] != "formal_gate_deliverables_ready_for_claim_audit":
        issues.append(
            _issue(
                "remaining_deliverables_allows_remote_training_while_blocked",
                "remaining-deliverables must not allow remote training while deliverables are blocked.",
            )
        )
    if permissions.get("formal_claim_allowed_now") is True and summary["status"] != "formal_gate_deliverables_ready_for_claim_audit":
        issues.append(
            _issue(
                "remaining_deliverables_allows_formal_claim_while_blocked",
                "remaining-deliverables must not allow formal claims while deliverables are blocked.",
            )
        )
    blocked_status = summary["status"] != "formal_gate_deliverables_ready_for_claim_audit"
    for matrix_id, row in summary["rows"].items():
        if not row["present"]:
            continue
        safe_matrix_id = matrix_id.replace(":", "_")
        if row["execution_boundary"] != "read_only_no_execution":
            issues.append(
                _issue(
                    f"remaining_deliverables_{safe_matrix_id}_execution_boundary_invalid",
                    f"{matrix_id} must be read-only.",
                )
            )
        if row["acceptance_predicate_count"] <= 0:
            issues.append(
                _issue(
                    f"remaining_deliverables_{safe_matrix_id}_missing_acceptance_predicates",
                    f"{matrix_id} must list acceptance predicates.",
                )
            )
        if row["invalid_substitute_count"] <= 0:
            issues.append(
                _issue(
                    f"remaining_deliverables_{safe_matrix_id}_missing_invalid_substitutes",
                    f"{matrix_id} must list invalid substitutes.",
                )
            )
        if blocked_status and row["responsible_stage_allowed_now"] is True:
            issues.append(
                _issue(
                    f"remaining_deliverables_{safe_matrix_id}_stage_allowed_while_blocked",
                    f"{matrix_id} responsible stage cannot be allowed while remaining deliverables are blocked.",
                )
            )
    return issues


def _remaining_deliverables_gap_summary_issues(
    *,
    remaining_deliverables: dict[str, Any],
    acceptance_summary: dict[str, Any],
    gap_summary: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not remaining_deliverables:
        return []
    if not gap_summary["present"]:
        return [
            _issue(
                "remaining_deliverables_gap_summary_missing",
                "remaining-deliverables ledger must expose deliverable_gap_summary.",
            )
        ]
    if gap_summary["summary_id"] != "module2_formal_gate_missing_training_eval_acceptance_summary":
        issues.append(
            _issue(
                "remaining_deliverables_gap_summary_id_invalid",
                "remaining-deliverables gap summary id must match the formal gate contract.",
            )
        )
    if gap_summary["execution_boundary"] != "read_only_no_execution":
        issues.append(
            _issue(
                "remaining_deliverables_gap_summary_execution_boundary_invalid",
                "remaining-deliverables gap summary must be read-only.",
            )
        )
    if not gap_summary["not_paper_result_material"]:
        issues.append(
            _issue(
                "remaining_deliverables_gap_summary_marked_as_paper_result",
                "remaining-deliverables gap summary must not be paper result material.",
            )
        )
    if gap_summary["total_missing_deliverables"] != acceptance_summary["missing_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_gap_total_missing_mismatch",
                "gap summary total missing deliverables must match the acceptance matrix missing row count.",
            )
        )
    if gap_summary["open_category_count"] != acceptance_summary["blocked_category_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_gap_open_category_mismatch",
                "gap summary open category count must match acceptance blocked category count.",
            )
        )
    expected_order = list(REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS)
    if gap_summary["category_order"] != expected_order:
        issues.append(
            _issue(
                "remaining_deliverables_gap_category_order_mismatch",
                "gap summary category order must cover training, evaluation, acceptance, and formal_acceptance.",
            )
        )
    category_counts = remaining_deliverables.get("category_counts")
    category_counts = category_counts if isinstance(category_counts, dict) else {}
    stage_by_category = {
        "training": "gate3_remote_training",
        "evaluation": "gate3_remote_audit_pullback",
        "acceptance": "gate3_remote_audit_pullback",
        "formal_acceptance": "regenerate_h01_h02_formal_artifacts",
    }
    blocked_status = remaining_deliverables.get("status") != "formal_gate_deliverables_ready_for_claim_audit"
    for category, artifact_ids in REMAINING_DELIVERABLE_ACCEPTANCE_MATRIX_IDS.items():
        raw_counts = category_counts.get(category) if isinstance(category_counts.get(category), dict) else {}
        expected_missing_count = int(raw_counts.get("missing_count") or 0)
        summary_category = gap_summary["categories"][category]
        if not summary_category["present"]:
            issues.append(
                _issue(
                    f"remaining_deliverables_gap_missing_category_{category}",
                    f"gap summary must include {category}.",
                )
            )
            continue
        if summary_category["missing_count"] != expected_missing_count:
            issues.append(
                _issue(
                    f"remaining_deliverables_gap_{category}_missing_count_mismatch",
                    f"gap summary {category} missing count must match category_counts.",
                )
            )
        if summary_category["responsible_stage_id"] != stage_by_category[category]:
            issues.append(
                _issue(
                    f"remaining_deliverables_gap_{category}_wrong_responsible_stage",
                    f"gap summary {category} responsible stage is wrong.",
                )
            )
        if blocked_status and summary_category["responsible_stage_allowed_now"] is True:
            issues.append(
                _issue(
                    f"remaining_deliverables_gap_{category}_stage_allowed_while_blocked",
                    f"gap summary {category} stage cannot be allowed while remaining deliverables are blocked.",
                )
            )
        expected_missing_matrix_ids = [
            matrix_id
            for matrix_id, row in acceptance_summary["rows"].items()
            if row["category"] == category and row["missing"] is True
        ]
        if summary_category["missing_artifact_matrix_ids"] != expected_missing_matrix_ids:
            issues.append(
                _issue(
                    f"remaining_deliverables_gap_{category}_missing_artifact_ids_mismatch",
                    f"gap summary {category} missing artifact ids must match acceptance matrix missing rows.",
                )
            )
        for artifact in summary_category["missing_artifacts"]:
            matrix_id = artifact.get("matrix_id")
            if matrix_id not in expected_missing_matrix_ids:
                continue
            safe_matrix_id = str(matrix_id).replace(":", "_")
            if artifact["acceptance_predicate_count"] <= 0:
                issues.append(
                    _issue(
                        f"remaining_deliverables_gap_{safe_matrix_id}_missing_predicates",
                        f"gap summary {matrix_id} must preserve acceptance predicate count.",
                    )
                )
            if artifact["proof_command_count"] <= 0:
                issues.append(
                    _issue(
                        f"remaining_deliverables_gap_{safe_matrix_id}_missing_proof_commands",
                        f"gap summary {matrix_id} must preserve proof command count.",
                    )
                )
            if artifact["invalid_substitute_count"] <= 0:
                issues.append(
                    _issue(
                        f"remaining_deliverables_gap_{safe_matrix_id}_missing_invalid_substitutes",
                        f"gap summary {matrix_id} must preserve invalid substitutes.",
                    )
                )
        expected_artifact_count = len(artifact_ids)
        if expected_missing_count > expected_artifact_count:
            issues.append(
                _issue(
                    f"remaining_deliverables_gap_{category}_missing_count_too_large",
                    f"gap summary {category} missing count exceeds expected artifact count.",
                )
            )
    return issues


def _remaining_deliverables_proof_command_plan_issues(
    *,
    remaining_deliverables: dict[str, Any],
    acceptance_summary: dict[str, Any],
    gap_summary: dict[str, Any],
    proof_plan: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not remaining_deliverables:
        return []
    if not proof_plan["present"]:
        return [
            _issue(
                "remaining_deliverables_proof_command_plan_missing",
                "remaining-deliverables ledger must expose proof_command_plan.",
            )
        ]
    if proof_plan["plan_id"] != "module2_formal_gate_local_read_only_proof_commands":
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_id_invalid",
                "proof command plan id must match the formal gate contract.",
            )
        )
    if proof_plan["execution_boundary"] != "local_read_only_after_formal_remote_pullback":
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_boundary_invalid",
                "proof command plan must be local read-only after formal remote pullback.",
            )
        )
    if not proof_plan["not_paper_result_material"]:
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_marked_as_paper_result",
                "proof command plan must not be paper result material.",
            )
        )
    if proof_plan["runs_training"]:
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_runs_training",
                "proof command plan must not run training.",
            )
        )
    if proof_plan["runs_remote_preflight"]:
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_runs_remote_preflight",
                "proof command plan must not run remote preflight.",
            )
        )
    if proof_plan["total_matrix_rows"] != acceptance_summary["matrix_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_matrix_count_mismatch",
                "proof command plan row count must match the acceptance matrix row count.",
            )
        )
    expected_total = sum(row["proof_command_count"] for row in acceptance_summary["rows"].values() if row["present"])
    if proof_plan["total_proof_command_count"] != expected_total:
        issues.append(
            _issue(
                "remaining_deliverables_proof_command_plan_command_count_mismatch",
                "proof command plan command count must match acceptance matrix proof commands.",
            )
        )
    for matrix_id, row in acceptance_summary["rows"].items():
        if not row["present"]:
            continue
        safe_matrix_id = matrix_id.replace(":", "_")
        if row["proof_command_count"] <= 0:
            issues.append(
                _issue(
                    f"remaining_deliverables_{safe_matrix_id}_missing_proof_commands",
                    f"{matrix_id} must list local read-only proof commands.",
                )
            )
        proof_row = proof_plan["rows"].get(matrix_id)
        if not proof_row:
            issues.append(
                _issue(
                    f"remaining_deliverables_proof_command_plan_missing_{safe_matrix_id}",
                    f"proof command plan must include {matrix_id}.",
                )
            )
            continue
        if proof_row["proof_command_count"] != row["proof_command_count"]:
            issues.append(
                _issue(
                    f"remaining_deliverables_proof_command_plan_{safe_matrix_id}_count_mismatch",
                    f"proof command plan count for {matrix_id} must match the acceptance matrix.",
                )
            )
        if proof_row["proof_command_ids"] != row["proof_command_ids"]:
            issues.append(
                _issue(
                    f"remaining_deliverables_proof_command_plan_{safe_matrix_id}_ids_mismatch",
                    f"proof command plan ids for {matrix_id} must match the acceptance matrix.",
                )
            )
    for category, payload in gap_summary["categories"].items():
        if not payload["present"]:
            continue
        for artifact in payload["missing_artifacts"]:
            matrix_id = str(artifact.get("matrix_id"))
            if matrix_id and artifact["proof_command_count"] <= 0:
                safe_matrix_id = matrix_id.replace(":", "_")
                issues.append(
                    _issue(
                        f"remaining_deliverables_proof_command_gap_{safe_matrix_id}_missing_commands",
                        f"gap summary must preserve proof commands for {matrix_id}.",
                    )
                )
    return issues


def _remaining_deliverables_unlock_chain_issues(
    *,
    remaining_deliverables: dict[str, Any],
    acceptance_summary: dict[str, Any],
    unlock_chain_summary: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not remaining_deliverables:
        return []
    if not unlock_chain_summary["present"]:
        return [
            _issue(
                "remaining_deliverables_unlock_chain_missing",
                "remaining-deliverables ledger must expose deliverable_unlock_chain.",
            )
        ]
    if unlock_chain_summary["chain_id"] != "module2_formal_gate_missing_deliverable_unlock_chain":
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_id_invalid",
                "unlock chain id must match the formal gate contract.",
            )
        )
    if unlock_chain_summary["execution_boundary"] != "read_only_no_execution":
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_boundary_invalid",
                "unlock chain must be read-only.",
            )
        )
    if not unlock_chain_summary["not_paper_result_material"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_marked_as_paper_result",
                "unlock chain must not be paper result material.",
            )
        )
    if unlock_chain_summary["row_count"] != acceptance_summary["matrix_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_row_count_mismatch",
                "unlock chain row count must match the acceptance matrix row count.",
            )
        )
    if unlock_chain_summary["derived_row_count"] != acceptance_summary["matrix_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_rows_missing",
                "unlock chain rows must cover every acceptance matrix row.",
            )
        )
    if unlock_chain_summary["blocked_row_count"] != acceptance_summary["missing_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_blocked_row_count_mismatch",
                "unlock chain blocked row count must match acceptance matrix missing row count.",
            )
        )
    if unlock_chain_summary["derived_blocked_row_count"] != acceptance_summary["missing_row_count"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_derived_blocked_row_count_mismatch",
                "unlock chain row blockers must match acceptance matrix missing rows.",
            )
        )
    if unlock_chain_summary["rows_with_missing_required_blockers"] > 0:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_rows_missing_required_blockers",
                "unlock chain rows must include all required current blockers while formal deliverables are missing.",
            )
        )
    if unlock_chain_summary["rows_allowed_while_missing"] > 0:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_rows_allowed_while_missing",
                "unlock chain must not allow responsible stages while their formal deliverables are missing.",
            )
        )
    if unlock_chain_summary["declared_rows_with_missing_required_blockers"] != unlock_chain_summary["rows_with_missing_required_blockers"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_missing_blocker_count_mismatch",
                "unlock chain declared missing-blocker count must match derived row count.",
            )
        )
    if unlock_chain_summary["declared_rows_allowed_while_missing"] != unlock_chain_summary["rows_allowed_while_missing"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_allowed_while_missing_count_mismatch",
                "unlock chain declared allowed-while-missing count must match derived row count.",
            )
        )
    for matrix_id, acceptance_row in acceptance_summary["rows"].items():
        if not acceptance_row["present"]:
            continue
        safe_matrix_id = matrix_id.replace(":", "_")
        chain_row = unlock_chain_summary["rows"].get(matrix_id)
        if not chain_row:
            issues.append(
                _issue(
                    f"remaining_deliverables_unlock_chain_missing_{safe_matrix_id}",
                    f"unlock chain must include {matrix_id}.",
                )
            )
            continue
        if chain_row["missing"] != acceptance_row["missing"]:
            issues.append(
                _issue(
                    f"remaining_deliverables_unlock_chain_{safe_matrix_id}_missing_mismatch",
                    f"unlock chain missing flag for {matrix_id} must match the acceptance matrix.",
                )
            )
        if chain_row["responsible_stage_id"] != acceptance_row["responsible_stage_id"]:
            issues.append(
                _issue(
                    f"remaining_deliverables_unlock_chain_{safe_matrix_id}_stage_mismatch",
                    f"unlock chain responsible stage for {matrix_id} must match the acceptance matrix.",
                )
            )
        if chain_row["execution_boundary"] != "read_only_no_execution":
            issues.append(
                _issue(
                    f"remaining_deliverables_unlock_chain_{safe_matrix_id}_boundary_invalid",
                    f"unlock chain row {matrix_id} must be read-only.",
                )
            )
    return issues


def _formal_gate_proof_audit_issues(
    *,
    proof_audit: dict[str, Any],
    summary: dict[str, Any],
    proof_plan: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not proof_audit:
        return [_issue("formal_gate_proof_audit_missing", "status report must consume formal gate proof audit.")]
    if summary["proof_command_plan_id"] != "module2_formal_gate_local_read_only_proof_commands":
        issues.append(
            _issue(
                "formal_gate_proof_audit_plan_id_invalid",
                "formal gate proof audit must reference the formal gate proof command plan.",
            )
        )
    if summary["execution_boundary"] != "local_read_only_after_formal_remote_pullback":
        issues.append(
            _issue(
                "formal_gate_proof_audit_boundary_invalid",
                "formal gate proof audit must stay within the local read-only post-pullback boundary.",
            )
        )
    if not summary["not_paper_result_material"]:
        issues.append(
            _issue(
                "formal_gate_proof_audit_marked_as_paper_result",
                "formal gate proof audit must not be marked as paper result material.",
            )
        )
    if summary["formal_claim_allowed"]:
        issues.append(
            _issue(
                "formal_gate_proof_audit_allows_formal_claim",
                "formal gate proof audit must not directly allow formal claims.",
            )
        )
    if summary["input_safety_issue_count"] > 0:
        issues.append(
            _issue(
                "formal_gate_proof_audit_input_safety_issues_open",
                "formal gate proof audit input safety issues must be resolved before status reporting.",
            )
        )
    if summary["total_matrix_rows"] != proof_plan["total_matrix_rows"]:
        issues.append(
            _issue(
                "formal_gate_proof_audit_matrix_count_mismatch",
                "formal gate proof audit matrix row count must match the proof command plan.",
            )
        )
    if summary["total_proof_command_count"] != proof_plan["total_proof_command_count"]:
        issues.append(
            _issue(
                "formal_gate_proof_audit_command_count_mismatch",
                "formal gate proof audit command count must match the proof command plan.",
            )
        )
    observed_count = len(summary["results_by_id"])
    if observed_count != proof_plan["total_proof_command_count"]:
        issues.append(
            _issue(
                "formal_gate_proof_audit_result_count_mismatch",
                "formal gate proof audit must include one result per proof command.",
            )
        )
    for matrix_id, proof_row in proof_plan["rows"].items():
        safe_matrix_id = matrix_id.replace(":", "_")
        for command_id in proof_row["proof_command_ids"]:
            result = summary["results_by_id"].get(command_id)
            if not result:
                issues.append(
                    _issue(
                        f"formal_gate_proof_audit_missing_{command_id}",
                        f"formal gate proof audit must include result {command_id}.",
                    )
                )
                continue
            if result["matrix_id"] != matrix_id:
                issues.append(
                    _issue(
                        f"formal_gate_proof_audit_{command_id}_matrix_mismatch",
                        f"proof audit result {command_id} must point to {safe_matrix_id}.",
                    )
                )
            if result["command_was_executed"]:
                issues.append(
                    _issue(
                        f"formal_gate_proof_audit_{command_id}_executed_command",
                        f"proof audit result {command_id} must be derived from local checks, not command execution.",
                    )
                )
    return issues


def _mainline_formal_gate_state_audit_issues(summary: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not summary["present"]:
        return [
            _issue(
                "mainline_formal_gate_state_audit_missing",
                "status report must consume the mainline formal gate state audit.",
            )
        ]
    if summary["status"] == "mainline_formal_gate_state_audit_failed":
        issues.append(
            _issue(
                "mainline_formal_gate_state_audit_failed",
                "mainline formal gate state audit must not be failed.",
            )
        )
    if not summary["not_paper_result_material"]:
        issues.append(
            _issue(
                "mainline_formal_gate_state_audit_marked_as_paper_result",
                "mainline formal gate state audit must not be marked as paper result material.",
            )
        )
    if summary["audit_issue_count"] > 0:
        issues.append(
            _issue(
                "mainline_formal_gate_state_audit_issues_open",
                "mainline formal gate state audit issues must be resolved before status reporting.",
            )
        )
    if summary["proof_summary_chain_audit_issue_count"] > 0:
        issues.append(
            _issue(
                "mainline_formal_gate_state_audit_proof_summary_issues_open",
                "mainline audit must not inherit open proof-summary audit issues.",
            )
        )
    if summary["proof_summary_chain_proof_audit_input_safety_issue_count"] > 0:
        issues.append(
            _issue(
                "mainline_formal_gate_state_audit_proof_audit_input_safety_issues_open",
                "mainline audit must not inherit open proof-audit input-safety issues.",
            )
        )
    if "proof_audit_input_safety_issues_open" in summary["proof_summary_chain_proof_audit_blockers"]:
        issues.append(
            _issue(
                "mainline_formal_gate_state_audit_proof_audit_input_safety_blocker_open",
                "mainline audit proof-summary blockers must not include proof-audit input-safety blockers.",
            )
        )
    return issues


def _formal_gate_gap_audit_remaining_deliverables_gap_summary_issues(
    *,
    formal_gate: dict[str, Any],
    formal_gate_gap_summary: dict[str, Any],
    ledger_gap_summary: dict[str, Any],
) -> list[dict[str, str]]:
    if not formal_gate:
        return [_issue("formal_gate_gap_audit_missing", "status report must consume formal gate gap audit.")]
    if not formal_gate_gap_summary["present"]:
        return [
            _issue(
                "formal_gate_gap_audit_missing_remaining_deliverables_gap_summary",
                "formal gate gap audit must expose remaining_deliverables_gap_summary.",
            )
        ]
    issues: list[dict[str, str]] = []
    if formal_gate_gap_summary["execution_boundary"] != "read_only_no_execution":
        issues.append(
            _issue(
                "formal_gate_gap_audit_gap_summary_execution_boundary_invalid",
                "formal gate gap audit remaining-deliverables gap summary must be read-only.",
            )
        )
    if not formal_gate_gap_summary["not_paper_result_material"]:
        issues.append(
            _issue(
                "formal_gate_gap_audit_gap_summary_marked_as_paper_result",
                "formal gate gap audit remaining-deliverables gap summary must not be paper result material.",
            )
        )
    if ledger_gap_summary["present"] and _gap_signature(formal_gate_gap_summary) != _gap_signature(ledger_gap_summary):
        issues.append(
            _issue(
                "formal_gate_gap_audit_remaining_deliverables_gap_summary_mismatch",
                "formal gate gap audit remaining-deliverables gap summary must match the ledger summary.",
            )
        )
    if formal_gate.get("status") != "formal_gate_ready_for_result_audit" and formal_gate_gap_summary["total_missing_deliverables"] == 0:
        issues.append(
            _issue(
                "blocked_formal_gate_gap_audit_claims_no_remaining_deliverables",
                "blocked formal gate gap audit must not claim zero remaining deliverables.",
            )
        )
    return issues


def _requirement_status_counts(rows: dict[str, dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows.values():
        status = row.get("status")
        if not status:
            continue
        counts[str(status)] = counts.get(str(status), 0) + 1
    return counts


def _remote_requirement_matrix_safety_issues(remote_packet: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    issues.extend(
        _remote_requirement_matrix_group_issues(
            remote_packet=remote_packet,
            requirement_key="remote_preflight_requirements",
            count_key="remote_preflight_requirement_counts",
            required_ids=REMOTE_PREFLIGHT_REQUIREMENT_IDS,
            issue_prefix="remote_preflight_requirement",
        )
    )
    issues.extend(
        _remote_requirement_matrix_group_issues(
            remote_packet=remote_packet,
            requirement_key="post_run_acceptance_requirements",
            count_key="post_run_acceptance_requirement_counts",
            required_ids=POST_RUN_ACCEPTANCE_REQUIREMENT_IDS,
            issue_prefix="post_run_acceptance_requirement",
        )
    )
    return issues


def _h02_formal_acceptance_requirement_summary(h02_acceptance: dict[str, Any]) -> dict[str, Any]:
    requirements = h02_acceptance.get("formal_acceptance_requirements")
    raw_requirements = requirements if isinstance(requirements, list) else []
    by_id = {str(item.get("requirement_id")): item for item in raw_requirements if isinstance(item, dict)}
    rows: dict[str, dict[str, Any]] = {}
    for requirement_id in H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS:
        row = by_id.get(requirement_id, {})
        rows[requirement_id] = {
            "present": bool(row),
            "status": row.get("status"),
            "phase": row.get("phase"),
            "complete": row.get("complete") if isinstance(row.get("complete"), bool) else None,
            "paper_result_input_allowed_now": row.get("paper_result_input_allowed_now")
            if isinstance(row.get("paper_result_input_allowed_now"), bool)
            else None,
            "required_before": row.get("required_before"),
            "missing_artifact_ids": _strings(row.get("missing_artifact_ids")),
            "acceptable_evidence_count": len(_strings(row.get("acceptable_evidence"))),
            "invalid_substitute_count": len(_strings(row.get("invalid_substitutes"))),
        }
    status_counts = (
        h02_acceptance.get("formal_acceptance_requirement_counts")
        if isinstance(h02_acceptance.get("formal_acceptance_requirement_counts"), dict)
        else _requirement_status_counts(rows)
    )
    return {
        "present": isinstance(requirements, list),
        "required_requirement_count": len(H02_FORMAL_ACCEPTANCE_REQUIREMENT_IDS),
        "present_requirement_count": sum(1 for row in rows.values() if row["present"]),
        "blocked_requirement_count": sum(
            1 for row in rows.values() if row["present"] and row["status"] not in {None, "satisfied"}
        ),
        "status_counts": status_counts,
        "missing_requirement_ids": [requirement_id for requirement_id, row in rows.items() if not row["present"]],
        "requirements": rows,
    }


def _h02_formal_acceptance_requirement_safety_issues(h02_acceptance: dict[str, Any]) -> list[dict[str, str]]:
    summary = _h02_formal_acceptance_requirement_summary(h02_acceptance)
    if not summary["present"]:
        return [
            _issue(
                "h02_formal_acceptance_requirement_matrix_missing",
                "H02 acceptance must expose formal_acceptance_requirements for status reporting.",
            )
        ]
    issues: list[dict[str, str]] = []
    if not isinstance(h02_acceptance.get("formal_acceptance_requirement_counts"), dict):
        issues.append(
            _issue(
                "h02_formal_acceptance_requirement_counts_missing",
                "H02 acceptance must expose formal_acceptance_requirement_counts.",
            )
        )
    for requirement_id in summary["missing_requirement_ids"]:
        issues.append(
            _issue(
                f"h02_formal_acceptance_requirement_missing_{requirement_id}",
                f"H02 acceptance missing requirement {requirement_id}.",
            )
        )
    h02_accepted = (
        h02_acceptance.get("formal_output_accepted") is True
        and h02_acceptance.get("paper_result_input_allowed") is True
    )
    if h02_accepted and summary["blocked_requirement_count"] > 0:
        issues.append(
            _issue(
                "h02_formal_acceptance_requirements_blocked_while_accepted",
                "H02 cannot accept paper result input while acceptance requirements remain blocked.",
            )
        )
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            continue
        if row["acceptable_evidence_count"] <= 0:
            issues.append(
                _issue(
                    f"h02_formal_acceptance_requirement_{requirement_id}_missing_acceptable_evidence",
                    f"{requirement_id} must list acceptable evidence.",
                )
            )
        if row["invalid_substitute_count"] <= 0:
            issues.append(
                _issue(
                    f"h02_formal_acceptance_requirement_{requirement_id}_missing_invalid_substitutes",
                    f"{requirement_id} must list invalid substitutes.",
                )
            )
        if not h02_accepted and row["paper_result_input_allowed_now"] is True:
            issues.append(
                _issue(
                    f"h02_formal_acceptance_requirement_{requirement_id}_allows_paper_result_while_h02_blocked",
                    f"{requirement_id} must not allow paper result input while H02 is blocked.",
                )
            )
        if row["complete"] is True and row["status"] != "satisfied":
            issues.append(
                _issue(
                    f"h02_formal_acceptance_requirement_{requirement_id}_complete_not_satisfied",
                    f"{requirement_id} complete=true must use status=satisfied.",
                )
            )
        if row["status"] == "satisfied" and row["missing_artifact_ids"]:
            issues.append(
                _issue(
                    f"h02_formal_acceptance_requirement_{requirement_id}_satisfied_with_missing_artifacts",
                    f"{requirement_id} satisfied rows must not list missing artifacts.",
                )
            )
    return issues


def _remote_requirement_matrix_group_issues(
    *,
    remote_packet: dict[str, Any],
    requirement_key: str,
    count_key: str,
    required_ids: Sequence[str],
    issue_prefix: str,
) -> list[dict[str, str]]:
    summary = _remote_requirement_matrix_summary(
        remote_packet=remote_packet,
        requirement_key=requirement_key,
        count_key=count_key,
        required_ids=required_ids,
    )
    issues: list[dict[str, str]] = []
    if not summary["present"]:
        return [_issue(f"{issue_prefix}_matrix_missing", f"remote packet must expose {requirement_key}.")]
    if not isinstance(remote_packet.get(count_key), dict):
        issues.append(_issue(f"{issue_prefix}_counts_missing", f"remote packet must expose {count_key}."))
    for requirement_id in summary["missing_requirement_ids"]:
        issues.append(_issue(f"{issue_prefix}_missing_{requirement_id}", f"remote packet missing requirement {requirement_id}."))
    packet_blocked = remote_packet.get("status") == "blocked_until_f02_6_decision"
    for requirement_id, row in summary["requirements"].items():
        if not row["present"]:
            continue
        if row["acceptable_evidence_count"] <= 0:
            issues.append(_issue(f"{issue_prefix}_{requirement_id}_missing_acceptable_evidence", f"{requirement_id} must list acceptable evidence."))
        if row["invalid_substitute_count"] <= 0:
            issues.append(_issue(f"{issue_prefix}_{requirement_id}_missing_invalid_substitutes", f"{requirement_id} must list invalid substitutes."))
        if packet_blocked and row["execution_allowed_now"] is True:
            issues.append(_issue(f"{issue_prefix}_{requirement_id}_allowed_while_packet_blocked", f"{requirement_id} must not be executable while remote packet is blocked."))
        if row["complete"] is True and row["status"] != "satisfied":
            issues.append(_issue(f"{issue_prefix}_{requirement_id}_complete_not_satisfied", f"{requirement_id} complete=true must use status=satisfied."))
        if row["status"] == "satisfied" and row["missing_artifact_ids"]:
            issues.append(_issue(f"{issue_prefix}_{requirement_id}_satisfied_with_missing_artifacts", f"{requirement_id} satisfied rows must not list missing artifacts."))
    return issues


def _group_missing_items(group: dict[str, Any]) -> list[dict[str, Any]]:
    items = group.get("items")
    if not isinstance(items, list):
        return []
    out: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict) or item.get("missing") is not True:
            continue
        out.append(
            {
                "artifact_id": item.get("artifact_id"),
                "path": item.get("path"),
                "state": item.get("state"),
                "reason": item.get("reason"),
            }
        )
    return out


def _artifact_list(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    items = payload.get(key)
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def _next_blocked_lane(lanes: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    for lane in lanes:
        if lane.get("status") == "blocked":
            return {
                "lane_id": lane.get("lane_id"),
                "phase": lane.get("phase"),
                "action_when_blocked": lane.get("action_when_blocked"),
                "blocked_by": lane.get("blocked_by"),
            }
    return None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _proof_commands(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    commands: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        commands.append(
            {
                "command_id": str(item.get("command_id") or ""),
                "command": str(item.get("command") or ""),
                "execution_boundary": str(item.get("execution_boundary") or ""),
            }
        )
    return commands


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


def _unique(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _unique_issues(issues: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for issue in issues:
        issue_id = issue.get("issue_id") or ""
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        out.append(issue)
    return out


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Status Report",
        "",
        "This file is a read-only formal-gate status report. It does not execute commands, run remote preflight, train, evaluate, sync, audit, pull back artifacts, or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- source_head: `{manifest['source_head']}`",
        f"- input_safety_issue_count: `{manifest['input_safety_issue_count']}`",
        f"- local_training_allowed_now: `{manifest['permissions_now']['local_training_allowed_now']}`",
        f"- remote_preflight_allowed_now: `{manifest['permissions_now']['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['permissions_now']['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{manifest['permissions_now']['formal_claim_allowed_now']}`",
        "",
        "## Current State",
        "",
    ]
    for key, value in manifest["current_state"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Next Blocked Lane", ""])
    if manifest["next_blocked_lane"]:
        lane = manifest["next_blocked_lane"]
        lines.append(f"- lane_id: `{lane['lane_id']}`")
        lines.append(f"- phase: `{lane['phase']}`")
        lines.append(f"- blocked_by: `{', '.join(lane['blocked_by'])}`")
        lines.append(f"- action: {lane['action_when_blocked']}")
    else:
        lines.append("- none")
    lines.extend(["", "## F02.6 Decision Intake", ""])
    intake = manifest["f02_6_decision_intake_summary"]
    lines.append(f"- present: `{intake['present']}`")
    lines.append(f"- status: `{intake['status']}`")
    lines.append(f"- record_status: `{intake['record_status']}`")
    lines.append(f"- record_decider: `{intake['record_decider']}`")
    lines.append(f"- effective_warm_start_decision: `{intake['effective_warm_start_decision']}`")
    lines.append(f"- next_blocked_lane: `{intake['next_blocked_lane']}`")
    lines.append(f"- audit_issue_count: `{intake['audit_issue_count']}`")
    lines.append(f"- decision_owner_required: `{intake['decision_owner_required']}`")
    lines.append(f"- valid_decision_count: `{intake['valid_decision_count']}`")
    lines.append(f"- required_record_field_count: `{intake['required_record_field_count']}`")
    lines.append(f"- decision_note_required: `{intake['decision_note_required']}`")
    lines.append(f"- invalid_input_count: `{intake['invalid_input_count']}`")
    lines.append(f"- post_decision_non_authorization_count: `{intake['post_decision_non_authorization_count']}`")
    lines.append(f"- post_decision_route_count: `{intake['post_decision_route_count']}`")
    lines.append(f"- post_decision_route_decisions: `{', '.join(intake['post_decision_route_decisions'])}`")
    lines.append(f"- approved_route_next_lane: `{intake['approved_route_next_lane']}`")
    lines.append(f"- approved_route_allows_remote_training_now: `{intake['approved_route_allows_remote_training_now']}`")
    lines.append(f"- rejected_route_next_lane: `{intake['rejected_route_next_lane']}`")
    lines.append(f"- rejected_route_requires_new_protocol_contract: `{intake['rejected_route_requires_new_protocol_contract']}`")
    lines.append(f"- missing_deliverable_count: `{intake['missing_deliverable_count']}`")
    lines.append(f"- remote_preflight_allowed_now: `{intake['remote_preflight_allowed_now']}`")
    lines.append(f"- remote_training_allowed_now: `{intake['remote_training_allowed_now']}`")
    lines.append(f"- formal_claim_allowed_now: `{intake['formal_claim_allowed_now']}`")
    lines.append(f"- decision_impact_present: `{intake['decision_impact_present']}`")
    lines.append(f"- decision_impact_summary_id: `{intake['decision_impact_summary_id']}`")
    lines.append(f"- decision_impact_current_blocker: `{intake['decision_impact_current_blocker']}`")
    lines.append(
        f"- decision_impact_missing_deliverable_count: `{intake['decision_impact_missing_deliverable_count']}`"
    )
    lines.append(
        "- decision_record_is_not_training_authorization: "
        f"`{intake['decision_record_is_not_training_authorization']}`"
    )
    lines.append(
        "- decision_record_is_not_paper_result_material: "
        f"`{intake['decision_record_is_not_paper_result_material']}`"
    )
    lines.append(
        f"- decision_impact_remote_preflight_allowed_now: `{intake['decision_impact_remote_preflight_allowed_now']}`"
    )
    lines.append(
        f"- decision_impact_remote_training_allowed_now: `{intake['decision_impact_remote_training_allowed_now']}`"
    )
    lines.append(
        f"- decision_impact_formal_claim_allowed_now: `{intake['decision_impact_formal_claim_allowed_now']}`"
    )
    lines.append(
        "- decision_impact_paper_result_material_allowed_now: "
        f"`{intake['decision_impact_paper_result_material_allowed_now']}`"
    )
    lines.append(
        "- decision_impact_formal_training_still_requires: "
        f"`{', '.join(intake['decision_impact_formal_training_still_requires'])}`"
    )
    next_guard = manifest["next_action_guard_summary"]
    lines.extend(["", "## Next Action Guard", ""])
    lines.append(f"- present: `{next_guard['present']}`")
    lines.append(f"- status: `{next_guard['status']}`")
    lines.append(f"- pending_f02_6_decision: `{next_guard['pending_f02_6_decision']}`")
    lines.append(f"- expected_next_action_id: `{next_guard['expected_next_action_id']}`")
    lines.append(f"- handoff_next_action_id: `{next_guard['handoff_next_action_id']}`")
    lines.append(f"- missing_artifacts_next_action_id: `{next_guard['missing_artifacts_next_action_id']}`")
    lines.append(f"- all_execution_disabled_now: `{next_guard['all_execution_disabled_now']}`")
    lines.append(f"- execution_leak_count: `{next_guard['execution_leak_count']}`")
    lines.append(f"- remote_execution_allowed_count: `{next_guard['remote_execution_allowed_count']}`")
    lines.append(f"- remote_stage_allowed_count: `{next_guard['remote_stage_allowed_count']}`")
    if next_guard["violations"]:
        for violation in next_guard["violations"]:
            lines.append(f"- violation `{violation['issue_id']}`: {violation['message']}")
    else:
        lines.append("- violations: `none`")
    lines.extend(["", "## Formal Gate Lanes", ""])
    for lane in manifest["formal_gate_lanes"]:
        host = f", host=`{lane['host']}`" if lane.get("host") else ""
        lines.append(
            f"- `{lane['lane_id']}` ({lane['phase']}): status=`{lane['status']}`, "
            f"missing=`{lane['missing_item_count']}`, runs_training=`{lane['runs_training']}`{host}"
        )
        if lane["blocked_by"]:
            lines.append(f"  - blocked_by: `{', '.join(lane['blocked_by'])}`")
        lines.append(f"  - completion_signal: {lane['completion_signal']}")
        lines.append(f"  - action_when_blocked: {lane['action_when_blocked']}")
    lines.extend(["", "## Remote Execution Steps", ""])
    for step_id, step in manifest["remote_execution_step_summary"].items():
        blocked_by = ", ".join(step["blocked_by"]) if step["blocked_by"] else "none"
        lines.append(
            f"- `{step_id}`: present=`{step['present']}`, allowed_now=`{step['allowed_now']}`, "
            f"runs_training=`{step['runs_training']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Remote Preflight Requirement Matrix", ""])
    preflight_requirements = manifest["remote_preflight_requirement_summary"]
    lines.append(f"- present: `{preflight_requirements['present']}`")
    lines.append(f"- status_counts: `{preflight_requirements['status_counts']}`")
    lines.append(f"- blocked_requirement_count: `{preflight_requirements['blocked_requirement_count']}`")
    for requirement_id, row in preflight_requirements["requirements"].items():
        blocked_by = ", ".join(row["blocked_by"]) if row["blocked_by"] else "none"
        lines.append(
            f"- `{requirement_id}`: status=`{row['status']}`, complete=`{row['complete']}`, "
            f"execution_allowed_now=`{row['execution_allowed_now']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Post-Run Acceptance Requirement Matrix", ""])
    post_run_requirements = manifest["post_run_acceptance_requirement_summary"]
    lines.append(f"- present: `{post_run_requirements['present']}`")
    lines.append(f"- status_counts: `{post_run_requirements['status_counts']}`")
    lines.append(f"- blocked_requirement_count: `{post_run_requirements['blocked_requirement_count']}`")
    for requirement_id, row in post_run_requirements["requirements"].items():
        lines.append(
            f"- `{requirement_id}`: status=`{row['status']}`, complete=`{row['complete']}`, "
            f"remote_training_ready_now=`{row['remote_training_ready_now']}`"
        )
    lines.extend(["", "## H02 Formal Acceptance Requirement Matrix", ""])
    h02_requirements = manifest["h02_formal_acceptance_requirement_summary"]
    lines.append(f"- present: `{h02_requirements['present']}`")
    lines.append(f"- status_counts: `{h02_requirements['status_counts']}`")
    lines.append(f"- blocked_requirement_count: `{h02_requirements['blocked_requirement_count']}`")
    for requirement_id, row in h02_requirements["requirements"].items():
        lines.append(
            f"- `{requirement_id}`: status=`{row['status']}`, complete=`{row['complete']}`, "
            f"paper_result_input_allowed_now=`{row['paper_result_input_allowed_now']}`"
        )
    lines.extend(["", "## Remaining Deliverables Acceptance Matrix", ""])
    remaining = manifest["remaining_deliverables_acceptance_summary"]
    lines.append(f"- present: `{remaining['present']}`")
    lines.append(f"- status: `{remaining['status']}`")
    lines.append(f"- matrix_row_count: `{remaining['matrix_row_count']}`")
    lines.append(f"- missing_row_count: `{remaining['missing_row_count']}`")
    lines.append(f"- blocked_category_count: `{remaining['blocked_category_count']}`")
    for matrix_id, row in remaining["rows"].items():
        blocked_by = ", ".join(row["responsible_stage_blocked_by"]) if row["responsible_stage_blocked_by"] else "none"
        lines.append(
            f"- `{matrix_id}`: missing=`{row['missing']}`, current_state=`{row['current_state']}`, "
            f"stage=`{row['responsible_stage_id']}`, stage_allowed_now=`{row['responsible_stage_allowed_now']}`, "
            f"acceptance_predicate_count=`{row['acceptance_predicate_count']}`, "
            f"proof_command_count=`{row['proof_command_count']}`, "
            f"invalid_substitute_count=`{row['invalid_substitute_count']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Remaining Deliverables Gap Summary", ""])
    gap = manifest["remaining_deliverables_gap_summary"]
    lines.append(f"- present: `{gap['present']}`")
    lines.append(f"- summary_id: `{gap['summary_id']}`")
    lines.append(f"- total_missing_deliverables: `{gap['total_missing_deliverables']}`")
    lines.append(f"- open_category_count: `{gap['open_category_count']}`")
    lines.append(f"- execution_boundary: `{gap['execution_boundary']}`")
    for category, payload in gap["categories"].items():
        blocked_by = ", ".join(payload["responsible_stage_blocked_by"]) if payload["responsible_stage_blocked_by"] else "none"
        missing_ids = ", ".join(payload["missing_artifact_matrix_ids"]) if payload["missing_artifact_matrix_ids"] else "none"
        proof_ids = ", ".join(payload["proof_command_ids"]) if payload["proof_command_ids"] else "none"
        lines.append(
            f"- `{category}`: missing_count=`{payload['missing_count']}`, "
            f"stage=`{payload['responsible_stage_id']}`, "
            f"stage_allowed_now=`{payload['responsible_stage_allowed_now']}`, "
            f"missing_artifacts=`{missing_ids}`, proof_commands=`{proof_ids}`, blocked_by=`{blocked_by}`"
        )
    unlock_chain = manifest["remaining_deliverables_unlock_chain_summary"]
    lines.extend(["", "## Remaining Deliverables Unlock Chain", ""])
    lines.append(f"- present: `{unlock_chain['present']}`")
    lines.append(f"- chain_id: `{unlock_chain['chain_id']}`")
    lines.append(f"- status: `{unlock_chain['status']}`")
    lines.append(f"- row_count: `{unlock_chain['row_count']}`")
    lines.append(f"- blocked_row_count: `{unlock_chain['blocked_row_count']}`")
    lines.append(f"- rows_with_missing_required_blockers: `{unlock_chain['rows_with_missing_required_blockers']}`")
    lines.append(f"- rows_allowed_while_missing: `{unlock_chain['rows_allowed_while_missing']}`")
    for category, payload in unlock_chain["categories"].items():
        blockers = ", ".join(payload["required_current_blockers"]) if payload["required_current_blockers"] else "none"
        lines.append(
            f"- `{category}`: row_count=`{payload['row_count']}`, blocked_row_count=`{payload['blocked_row_count']}`, "
            f"rows_with_missing_required_blockers=`{payload['rows_with_missing_required_blockers']}`, "
            f"rows_allowed_while_missing=`{payload['rows_allowed_while_missing']}`, blockers=`{blockers}`"
        )
    next_deliverables = manifest["next_required_formal_deliverables"]
    lines.extend(["", "## Next Required Formal Deliverables", ""])
    lines.append(f"- status: `{next_deliverables['status']}`")
    lines.append(f"- execution_boundary: `{next_deliverables['execution_boundary']}`")
    lines.append(f"- not_paper_result_material: `{next_deliverables['not_paper_result_material']}`")
    lines.append(f"- runs_training: `{next_deliverables['runs_training']}`")
    lines.append(f"- runs_remote_preflight: `{next_deliverables['runs_remote_preflight']}`")
    lines.append(f"- total_missing_deliverables: `{next_deliverables['total_missing_deliverables']}`")
    lines.append(f"- blocked_categories: `{', '.join(next_deliverables['blocked_categories'])}`")
    for row in next_deliverables["rows"]:
        blocked_by = ", ".join(row["responsible_stage_blocked_by"]) if row["responsible_stage_blocked_by"] else "none"
        proof_ids = ", ".join(row["proof_command_ids"]) if row["proof_command_ids"] else "none"
        lines.append(
            f"- `{row['matrix_id']}`: category=`{row['category']}`, artifact=`{row['artifact_id']}`, "
            f"expected_path=`{row['expected_path']}`, current_state=`{row['current_state']}`, "
            f"stage=`{row['responsible_stage_id']}`, stage_allowed_now=`{row['responsible_stage_allowed_now']}`, "
            f"proof_commands=`{proof_ids}`, invalid_substitute_count=`{row['invalid_substitute_count']}`, "
            f"blocked_by=`{blocked_by}`"
        )
    proof_plan = manifest["remaining_deliverables_proof_command_plan"]
    lines.extend(["", "## Remaining Deliverables Proof Command Plan", ""])
    lines.append(f"- present: `{proof_plan['present']}`")
    lines.append(f"- plan_id: `{proof_plan['plan_id']}`")
    lines.append(f"- execution_boundary: `{proof_plan['execution_boundary']}`")
    lines.append(f"- total_matrix_rows: `{proof_plan['total_matrix_rows']}`")
    lines.append(f"- total_proof_command_count: `{proof_plan['total_proof_command_count']}`")
    lines.append(f"- runs_training: `{proof_plan['runs_training']}`")
    lines.append(f"- runs_remote_preflight: `{proof_plan['runs_remote_preflight']}`")
    for matrix_id, row in proof_plan["rows"].items():
        command_ids = ", ".join(row["proof_command_ids"]) if row["proof_command_ids"] else "none"
        lines.append(f"- `{matrix_id}`: proof_command_count=`{row['proof_command_count']}`, command_ids=`{command_ids}`")
    proof_gap = manifest["formal_gate_proof_audit_gap_summary"]
    lines.extend(["", "## Formal Gate Proof Audit Gap Summary", ""])
    lines.append(f"- present: `{proof_gap['present']}`")
    lines.append(f"- status: `{proof_gap['status']}`")
    lines.append(f"- missing_artifact_count=`{proof_gap['missing_artifact_count']}`")
    lines.append(f"- failed_acceptance_artifact_count=`{proof_gap['failed_acceptance_artifact_count']}`")
    for category, payload in proof_gap["categories"].items():
        missing_ids = ", ".join(payload["missing_artifact_ids"]) if payload["missing_artifact_ids"] else "none"
        failed_ids = ", ".join(payload["failed_artifact_ids"]) if payload["failed_artifact_ids"] else "none"
        blocked_commands = (
            ", ".join(payload["blocked_proof_command_ids"]) if payload["blocked_proof_command_ids"] else "none"
        )
        failed_commands = (
            ", ".join(payload["failed_proof_command_ids"]) if payload["failed_proof_command_ids"] else "none"
        )
        lines.append(
            f"- `{category}`: missing_artifact_count=`{payload['missing_artifact_count']}`, "
            f"failed_acceptance_artifact_count=`{payload['failed_acceptance_artifact_count']}`, "
            f"blocked_proof_command_count=`{payload['blocked_proof_command_count']}`, "
            f"failed_proof_command_count=`{payload['failed_proof_command_count']}`, "
            f"missing_artifacts=`{missing_ids}`, failed_artifacts=`{failed_ids}`, "
            f"blocked_commands=`{blocked_commands}`, failed_commands=`{failed_commands}`"
        )
    proof_audit = manifest["formal_gate_proof_audit_summary"]
    lines.extend(["", "## Formal Gate Proof Audit", ""])
    lines.append(f"- present: `{proof_audit['present']}`")
    lines.append(f"- status: `{proof_audit['status']}`")
    lines.append(f"- total_matrix_rows: `{proof_audit['total_matrix_rows']}`")
    lines.append(f"- total_proof_command_count: `{proof_audit['total_proof_command_count']}`")
    lines.append(f"- passed_proof_command_count: `{proof_audit['passed_proof_command_count']}`")
    lines.append(f"- failed_proof_command_count: `{proof_audit['failed_proof_command_count']}`")
    lines.append(f"- blocked_proof_command_count: `{proof_audit['blocked_proof_command_count']}`")
    proof_deliverables = manifest["formal_gate_proof_audit_remaining_deliverables_top_level_summary"]
    lines.append(f"- remaining_deliverables_summary_present: `{proof_deliverables['present']}`")
    lines.append(
        f"- remaining_missing_counts_by_formal_category: `{proof_deliverables['missing_counts_by_formal_category']}`"
    )
    lines.append(f"- remaining_next_blocked_lane: `{proof_deliverables['next_blocked_lane']}`")
    lines.append(f"- remaining_h01_status: `{proof_deliverables['h01_status']}`")
    lines.append(f"- remaining_h02_status: `{proof_deliverables['h02_status']}`")
    for category, matrix_ids in proof_deliverables["missing_matrix_ids_by_formal_category"].items():
        joined = ", ".join(matrix_ids) if matrix_ids else "none"
        lines.append(f"- remaining_{category}_missing_matrix_ids: `{joined}`")
    for command_id, result in proof_audit["results_by_id"].items():
        lines.append(f"- `{command_id}`: status=`{result['status']}`, matrix_id=`{result['matrix_id']}`")
    formal_gate_gap = manifest["formal_gate_gap_audit_remaining_deliverables_gap_summary"]
    lines.extend(["", "## Formal Gate Gap Audit Remaining Deliverables Gap Summary", ""])
    lines.append(f"- present: `{formal_gate_gap['present']}`")
    lines.append(f"- summary_id: `{formal_gate_gap['summary_id']}`")
    lines.append(f"- total_missing_deliverables: `{formal_gate_gap['total_missing_deliverables']}`")
    lines.append(f"- open_category_count: `{formal_gate_gap['open_category_count']}`")
    lines.append(f"- matches_ledger_signature: `{_gap_signature(formal_gate_gap) == _gap_signature(gap)}`")
    remote_proof = manifest["remote_packet_safety_proof_deliverables_summary"]
    remote_status_proof = manifest["remote_packet_safety_status_report_proof_deliverables_summary"]
    lines.extend(["", "## Remote Packet Safety Proof Deliverables Summary", ""])
    lines.append(f"- proof_summary_present: `{remote_proof['present']}`")
    lines.append(f"- proof_missing_counts_by_formal_category: `{remote_proof['missing_counts_by_formal_category']}`")
    lines.append(f"- proof_next_blocked_lane: `{remote_proof['next_blocked_lane']}`")
    lines.append(f"- proof_h01_status: `{remote_proof['h01_status']}`")
    lines.append(f"- proof_h02_status: `{remote_proof['h02_status']}`")
    lines.append(f"- proof_h02_paper_result_input_allowed: `{remote_proof['h02_paper_result_input_allowed']}`")
    lines.append(f"- status_report_proof_summary_present: `{remote_status_proof['present']}`")
    lines.append(
        "- status_report_proof_matches_remote_proof: "
        f"`{_proof_deliverables_signature(remote_status_proof) == _proof_deliverables_signature(remote_proof)}`"
    )
    lines.append(
        "- remote_proof_matches_proof_audit: "
        f"`{_proof_deliverables_signature(remote_proof) == _proof_deliverables_signature(proof_deliverables)}`"
    )
    for category, matrix_ids in remote_proof["missing_matrix_ids_by_formal_category"].items():
        joined = ", ".join(matrix_ids) if matrix_ids else "none"
        lines.append(f"- remote_proof_{category}_missing_matrix_ids: `{joined}`")
    command_index = manifest["remote_packet_safety_claim_gate_command_index_summary"]
    lines.extend(["", "## Remote Packet Safety Claim-Gate Command Index", ""])
    lines.append(f"- present: `{command_index['present']}`")
    lines.append(f"- index_row_count: `{command_index['index_row_count']}`")
    lines.append(f"- source_target_count: `{command_index['source_target_count']}`")
    lines.append(f"- missing_target_ids: `{command_index['missing_target_ids']}`")
    lines.append(f"- unknown_manual_count: `{command_index['unknown_manual_count']}`")
    lines.append(f"- forbidden_command_count: `{command_index['forbidden_command_count']}`")
    for artifact_id, row in command_index["claim_gate_rows"].items():
        lines.append(
            f"- `{artifact_id}`: present=`{row['present']}`, stage=`{row['stage_id']}`, "
            f"required_before=`{row['required_before']}`, command_kind=`{row['command_kind']}`"
        )
    lines.extend(["", "## Closure Remote Stages", ""])
    for stage_id, stage in manifest["closure_remote_stage_summary"].items():
        blocked_by = ", ".join(stage["blocked_by"]) if stage["blocked_by"] else "none"
        lines.append(
            f"- `{stage_id}`: present=`{stage['present']}`, allowed_now=`{stage['allowed_now']}`, "
            f"runs_training=`{stage['runs_training']}`, runs_remote_preflight=`{stage['runs_remote_preflight']}`, "
            f"host=`{stage['host']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Missing-Artifacts Handoff Index", ""])
    missing_handoff = manifest["missing_artifacts_handoff_index_summary"]
    lines.append(f"- present: `{missing_handoff['present']}`")
    lines.append(f"- status: `{missing_handoff['status']}`")
    lines.append(f"- next_action: `{missing_handoff['next_action_id']}`")
    lines.append(f"- next_action_requires_dr_sun: `{missing_handoff['next_action_requires_dr_sun']}`")
    lines.append(f"- open_requirement_count: `{missing_handoff['open_requirement_count']}`")
    lines.append(f"- local_training_allowed_now: `{missing_handoff['local_training_allowed_now']}`")
    lines.append(f"- remote_training_allowed_now: `{missing_handoff['remote_training_allowed_now']}`")
    lines.append(f"- formal_result_material_allowed_now: `{missing_handoff['formal_result_material_allowed_now']}`")
    lines.extend(["", "## Formal Gate Handoff Bundle", ""])
    handoff = manifest["formal_gate_handoff_summary"]
    lines.append(f"- present: `{handoff['present']}`")
    lines.append(f"- status: `{handoff['status']}`")
    lines.append(f"- next_handoff_action: `{handoff['next_handoff_action_id']}`")
    lines.append(f"- safety_issue_count: `{handoff['safety_issue_count']}`")
    lines.append(f"- remote_training_allowed_now: `{handoff['remote_training_allowed_now']}`")
    for step_id, step in handoff["remote_execution_steps"].items():
        blocked_by = ", ".join(step["blocked_by"]) if step["blocked_by"] else "none"
        lines.append(
            f"- `{step_id}`: present=`{step['present']}`, allowed_now=`{step['allowed_now']}`, "
            f"runs_training=`{step['runs_training']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Formal Gate Requirement Stage Summary", ""])
    stage_summary = manifest["formal_gate_requirement_stage_summary"]
    lines.append(f"- mapped_requirement_count: `{stage_summary['mapped_requirement_count']}`")
    lines.append(f"- unmapped_requirement_count: `{stage_summary['unmapped_requirement_count']}`")
    lines.append(f"- mismatched_requirement_count: `{stage_summary['mismatched_requirement_count']}`")
    for requirement_id, row in stage_summary["requirements"].items():
        blocked_by = ", ".join(row["responsible_stage_blocked_by"]) if row["responsible_stage_blocked_by"] else "none"
        lines.append(
            f"- `{requirement_id}`: expected_stage=`{row['expected_stage_id']}`, "
            f"responsible_stage=`{row['responsible_stage_id']}`, "
            f"stage_status=`{row['responsible_stage_status']}`, "
            f"stage_allowed_now=`{row['responsible_stage_allowed_now']}`, "
            f"blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Formal Gate Execution Veto Matrix", ""])
    veto = manifest["formal_gate_execution_veto_summary"]
    lines.append(f"- present: `{veto['present']}`")
    lines.append(f"- all_rows_consistent: `{veto['all_rows_consistent']}`")
    lines.append(f"- mismatch_rows: `{veto['mismatch_rows']}`")
    for row_id, row in veto["rows"].items():
        lines.append(
            f"- `{row_id}`: consistent=`{row['consistent']}`, "
            f"consensus_allowed_now=`{row['consensus_allowed_now']}`, sources=`{row['allowed_now_by_source']}`"
        )
    lines.extend(["", "## Required Training Artifacts", ""])
    _append_artifacts(lines, manifest["training_artifacts_required"])
    lines.extend(["", "## Required Evaluation Artifacts", ""])
    _append_artifacts(lines, manifest["evaluation_artifacts_required"])
    lines.extend(["", "## Required Acceptance Artifacts", ""])
    _append_artifacts(lines, manifest["acceptance_artifacts_required"])
    lines.extend(["", "## Input Safety Issues", ""])
    if manifest["input_safety_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["input_safety_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Safe Work Without F02.6 Decision", ""])
    lines.extend(f"- {item}" for item in manifest["safe_work_without_f02_6_decision"])
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _append_artifacts(lines: list[str], artifacts: Sequence[dict[str, Any]]) -> None:
    if not artifacts:
        lines.append("- none")
        return
    for artifact in artifacts:
        lines.append(
            f"- `{artifact.get('artifact_id')}`: missing=`{artifact.get('missing')}`, "
            f"path=`{artifact.get('path')}`"
        )


if __name__ == "__main__":
    raise SystemExit(main())
