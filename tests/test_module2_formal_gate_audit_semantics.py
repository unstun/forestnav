from __future__ import annotations

import json
from pathlib import Path

from forest_n3p.scripts.build_module2_formal_gate_status_report import (
    _formal_gate_execution_veto_issues,
    _remaining_deliverables_acceptance_issues,
)
from forest_n3p.scripts.build_module2_f02_6_transition_gate_audit import (
    _approved_scenario_issues,
    _common_scenario_issues,
)
from forest_n3p.scripts.build_module2_formal_gate_gap_audit import (
    _execution_veto_matrix,
)
from forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables import (
    _deliverable_unlock_chain,
    _production_plan_safety_issues,
    _unlock_chain_safety_issues,
)
from forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit import (
    FormalGateProofSummaryChainAuditConfig,
    _handoff_single_next_action_issues,
    _next_action_guard_issues,
    _next_action_guard_rows,
)
from forest_n3p.scripts.build_module2_post_f02_6_plan_audit import (
    _cross_artifact_issues,
    _handoff_coverage_issues,
    _status_report_issues,
)
from forest_n3p.scripts.build_module2_claim_safety import (
    _status_report_next_action_guard_blockers,
)
from forest_n3p.scripts.build_module2_remote_packet_safety_audit import (
    _cross_gate_issues as _remote_packet_cross_gate_issues,
    _status_report_execution_veto_issues,
)
from forest_n3p.scripts.build_module2_remote_formal_execution_packet import (
    RemoteFormalExecutionPacketConfig,
    _blockers as _remote_packet_blockers,
    _status as _remote_packet_status,
    build_packet as _build_remote_packet,
)


def test_post_f02_6_plan_compares_blocking_source_freshness_flag() -> None:
    issues = _cross_artifact_issues(
        plan={
            "current_gate_summary": {
                "f02_6_decision_status": "approved",
                "source_freshness_regeneration_required": True,
                "source_freshness_blocking_regeneration_required": False,
            },
            "source_regeneration_targets_by_gate": {},
        },
        formal_gate={"current_gate_state": {"f02_6_decision_status": "approved"}},
        source_freshness={
            "regeneration_required_before_remote_formal_execution": True,
            "blocking_regeneration_required_before_remote_formal_execution": False,
            "ordered_regeneration_targets": [],
        },
    )

    assert "plan_source_freshness_requirement_mismatch" not in {
        issue["issue_id"] for issue in issues
    }


def test_blocked_result_gate_may_still_surface_approved_remote_preflight(tmp_path: Path) -> None:
    status_report_path = tmp_path / "formal_gate_status_report.json"
    status_report_path.write_text("{}\n", encoding="utf-8")
    status_report = {
        "status": "formal_gate_status_blocked",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": True,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
        "remote_execution_step_summary": {
            "sync_to_remote": {"present": True, "allowed_now": True, "runs_training": False, "blocked_by": []},
            "run_remote_preflight": {"present": True, "allowed_now": True, "runs_training": False, "blocked_by": []},
            "run_remote_training": {
                "present": True,
                "allowed_now": False,
                "runs_training": True,
                "blocked_by": ["remote_packet_not_ready"],
            },
            "run_remote_audit": {
                "present": True,
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["remote_packet_not_ready"],
            },
        },
        "formal_gate_execution_veto_summary": {
            "present": True,
            "all_rows_consistent": True,
            "mismatch_rows": [],
            "row_count": 5,
            "row_consensus": {
                "local_training": False,
                "remote_preflight": True,
                "remote_training": False,
                "remote_audit": False,
                "formal_claim": False,
            },
            "rows": {},
        },
    }

    issues = _status_report_issues(
        plan={"ordered_stages": [{"stage_id": "regenerate_claim_gate_artifacts", "allowed_now": False}]},
        status_report=status_report,
        status_report_path=status_report_path,
    )

    issue_ids = {issue["issue_id"] for issue in issues}
    assert "formal_gate_status_report_blocked_but_sync_to_remote_allowed" not in issue_ids
    assert "formal_gate_status_report_blocked_but_run_remote_preflight_allowed" not in issue_ids
    assert "formal_gate_status_report_blocked_veto_allows_remote_preflight" not in issue_ids


def test_remote_packet_safety_allows_preflight_before_result_gate_is_claim_ready() -> None:
    packet = {
        "execution_steps": {
            "sync_to_remote": {"allowed_now": True, "blocked_by": []},
            "run_remote_preflight": {"allowed_now": True, "blocked_by": []},
            "run_remote_training": {"allowed_now": False, "blocked_by": ["remote_packet_not_ready"]},
            "run_remote_audit": {"allowed_now": False, "blocked_by": ["remote_packet_not_ready"]},
        },
        "ready_to_run_remote_training": False,
    }
    status_summary = {
        "status": "formal_gate_status_blocked",
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
    }
    execution_veto = {
        "all_rows_consistent": True,
        "mismatch_rows": [],
        "row_consensus": {
            "local_training": False,
            "remote_preflight": True,
            "remote_training": False,
            "remote_audit": False,
            "formal_claim": False,
        },
    }

    issues = _status_report_execution_veto_issues(
        packet=packet,
        status_summary=status_summary,
        execution_veto=execution_veto,
    )

    assert "blocked_status_report_execution_veto_allows_remote_preflight" not in {
        issue["issue_id"] for issue in issues
    }


def test_remote_packet_training_ready_ignores_downstream_h01_output_blockers() -> None:
    decision = {
        "status": "approved",
        "local_training_allowed": False,
        "remote_training_allowed": True,
        "blockers": [],
    }
    h01 = {
        "schema_checks": {
            "required_output_schema": "present",
            "schema_status": "frozen_for_module2_v1",
        },
        "blockers": [
            "missing_module2_rl_rs_checkpoint",
            "realmap_query_generation_not_frozen",
        ],
    }
    preflight = {"formal_trial_ready": True, "blocker_codes": []}

    blockers = _remote_packet_blockers(decision=decision, h01=h01, preflight=preflight)

    assert blockers == []
    assert _remote_packet_status(decision=decision, blockers=blockers, preflight=preflight) == (
        "ready_for_gpu3070ti_remote_training"
    )


def test_remote_packet_training_still_blocks_unfrozen_h01_schema() -> None:
    decision = {
        "status": "approved",
        "local_training_allowed": False,
        "remote_training_allowed": True,
        "blockers": [],
    }
    h01 = {
        "schema_checks": {
            "required_output_schema": "present",
            "schema_status": "draft",
        },
        "blockers": [],
    }
    preflight = {"formal_trial_ready": True, "blocker_codes": []}

    blockers = _remote_packet_blockers(decision=decision, h01=h01, preflight=preflight)

    assert blockers == ["h01_required_output_schema_not_frozen"]
    assert _remote_packet_status(decision=decision, blockers=blockers, preflight=preflight) == "blocked_preconditions"


def test_remote_packet_ready_stage_does_not_allow_audit_before_training(tmp_path: Path) -> None:
    decision_path = tmp_path / "decision.json"
    h01_path = tmp_path / "h01.json"
    preflight_path = tmp_path / "preflight.json"
    decision_path.write_text(
        json.dumps(
            {
                "status": "approved",
                "effective_warm_start_decision": "approved_obstacle_summary",
                "remote_training_allowed": True,
                "local_training_allowed": False,
                "formal_claim_allowed": False,
                "blockers": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    h01_path.write_text(
        json.dumps(
            {
                "status": "blocked_protocol_gap",
                "blockers": ["missing_module2_rl_rs_checkpoint"],
                "required_output_schema": {
                    "schema_status": "frozen_for_module2_v1",
                    "records_csv_required_columns": ["query_id"],
                    "summary_by_method_bucket_required_columns": ["method"],
                    "summary_json_required_sections": ["record_count"],
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    preflight_path.write_text(
        json.dumps(
            {
                "preflight_status": "ready",
                "formal_trial_ready": True,
                "warm_start_decision": "approved_obstacle_summary",
                "formal_blockers": [],
                "protocol": {
                    "device": "cuda",
                    "smoke": False,
                    "formal_audit_required": True,
                    "train_total_timesteps": 100000,
                    "eval_min_episodes": 64,
                    "eval_success_threshold": 0.8,
                },
                "runner_command": "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --output-dir trial",
                "audit_command": "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --trial-dir trial",
                "expected_artifacts": ["trial/train/final_model.zip"],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    packet = _build_remote_packet(
        RemoteFormalExecutionPacketConfig(
            output_dir=tmp_path,
            decision_record_path=decision_path,
            h01_manifest_path=h01_path,
            remote_preflight_path=preflight_path,
        )
    )

    steps = packet["execution_steps"]
    assert packet["ready_to_run_remote_training"] is True
    assert steps["run_remote_training"]["allowed_now"] is True
    assert steps["run_remote_audit"]["allowed_now"] is False
    assert steps["run_remote_audit"]["blocked_by"] == ["remote_training_not_completed"]


def test_execution_veto_uses_authoritative_training_sources_not_downstream_audits() -> None:
    matrix = _execution_veto_matrix(
        decision={
            "status": "approved",
            "remote_training_allowed": True,
        },
        remote={
            "local_training_allowed": False,
            "execution_steps": {
                "run_remote_preflight": {"allowed_now": True},
                "run_remote_training": {"allowed_now": True},
                "run_remote_audit": {"allowed_now": False},
            },
        },
        status_report={
            "permissions_now": {
                "local_training_allowed_now": False,
                "remote_preflight_allowed_now": True,
                "remote_training_allowed_now": True,
                "formal_claim_allowed_now": False,
            }
        },
        handoff_bundle={
            "permissions_now": {
                "local_training_allowed_now": False,
                "remote_preflight_allowed_now": False,
                "remote_training_allowed_now": False,
                "formal_claim_allowed_now": False,
            },
            "remote_execution_steps": {
                "run_remote_audit": {"allowed_now": False},
            },
        },
        remote_packet_safety={
            "packet_summary": {
                "remote_preflight_allowed_now": False,
                "remote_training_allowed_now": False,
                "remote_audit_allowed_now": False,
            }
        },
    )

    rows = {row["row_id"]: row for row in matrix["rows"]}
    assert rows["remote_preflight"]["consistent"] is True
    assert rows["remote_preflight"]["consensus_allowed_now"] is True
    assert rows["remote_training"]["consistent"] is True
    assert rows["remote_training"]["consensus_allowed_now"] is True
    assert "handoff_bundle" not in rows["remote_training"]["allowed_now_by_source"]
    assert "remote_packet_safety" not in rows["remote_training"]["allowed_now_by_source"]
    assert rows["remote_audit"]["consensus_allowed_now"] is False


def test_f02_6_approved_transition_allows_remote_training_entry_not_claim() -> None:
    summary = {
        "scenario_id": "approved",
        "record_status": "approved",
        "record_local_training_allowed": False,
        "record_formal_claim_allowed": False,
        "record_remote_preflight_allowed_now": False,
        "record_remote_training_allowed_now": False,
        "decision_gate_audit_issue_count": 0,
        "post_plan_audit_issue_count": 0,
        "remote_packet_safety_issue_count": 0,
        "decision_gate_status": "f02_6_decision_gate_audit_passed",
        "post_plan_audit_status": "post_f02_6_plan_audit_passed",
        "remote_packet_safety_status": "remote_packet_safety_audit_passed",
        "post_plan_status": "ready_for_remote_training_packet_execution",
        "formal_gate_status_report_next_blocked_lane_id": "gate3_remote_audit_pullback",
        "formal_gate_status_report_permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": True,
            "remote_training_allowed_now": True,
            "formal_claim_allowed_now": False,
        },
        "post_plan_stage_summary": {
            "regenerate_preflight_gate_artifacts": {"allowed_now": False},
            "approved_remote_preflight": {"allowed_now": True},
            "gate3_remote_training": {"allowed_now": True},
            "gate3_remote_audit_pullback": {"allowed_now": False},
            "regenerate_claim_gate_artifacts": {"allowed_now": False},
        },
    }

    issue_ids = {
        issue["issue_id"]
        for issue in _common_scenario_issues(summary) + _approved_scenario_issues(summary)
    }

    assert "status_report_allows_remote_training" not in issue_ids
    assert "approved_post_plan_wrong_status" not in issue_ids
    assert "approved_status_report_allows_remote_preflight_too_early" not in issue_ids
    assert "approved_remote_preflight_ready_too_early" not in issue_ids
    assert "approved_training_ready_too_early" not in issue_ids


def test_remaining_deliverables_allow_training_generation_while_missing() -> None:
    production_issues = _production_plan_safety_issues(
        {
            "execution_boundary": "reference_only_no_execution",
            "runs_training": False,
            "runs_remote_preflight": False,
            "row_count": 1,
            "rows": [
                {
                    "matrix_id": "training:train_final_model_zip",
                    "category": "training",
                    "artifact_id": "train_final_model_zip",
                    "execution_boundary": "reference_only_no_execution",
                    "current_missing": True,
                    "remote_generation_stage_id": "gate3_remote_training",
                    "local_materialization_stage_id": "gate3_remote_audit_pullback",
                    "remote_generation_stage": {"allowed_now": True},
                    "local_materialization_stage": {"allowed_now": False},
                    "hash_manifest_required_by_remote_packet": False,
                }
            ],
        }
    )
    unlock_issues = _unlock_chain_safety_issues(
        {
            "execution_boundary": "read_only_no_execution",
            "rows": [
                {
                    "matrix_id": "training:train_final_model_zip",
                    "missing": True,
                    "responsible_stage_id": "gate3_remote_training",
                    "responsible_stage_allowed_now": True,
                    "missing_required_current_blockers": [],
                    "execution_boundary": "read_only_no_execution",
                    "unlock_sequence_before_stage_allowed": ["remote_formal_execution_packet_ready"],
                }
            ],
        }
    )

    assert not {
        issue["issue_id"]
        for issue in production_issues + unlock_issues
        if issue["issue_id"].endswith("_allowed_while_missing")
    }


def test_status_report_allows_training_stage_in_remaining_deliverables_summary() -> None:
    issues = _remaining_deliverables_acceptance_issues(
        remaining_deliverables={"status": "formal_gate_deliverables_blocked"},
        summary={
            "present": True,
            "status": "formal_gate_deliverables_blocked",
            "matrix_row_count": 1,
            "expected_matrix_row_count": 1,
            "missing_expected_matrix_ids": [],
            "permissions_now": {
                "local_training_allowed_now": False,
                "remote_training_allowed_now": True,
                "formal_claim_allowed_now": False,
            },
            "rows": {
                "training:train_final_model_zip": {
                    "present": True,
                    "category": "training",
                    "execution_boundary": "read_only_no_execution",
                    "acceptance_predicate_count": 1,
                    "invalid_substitute_count": 1,
                    "responsible_stage_allowed_now": True,
                    "responsible_stage_id": "gate3_remote_training",
                }
            },
        },
    )

    assert "remaining_deliverables_training_train_final_model_zip_stage_allowed_while_blocked" not in {
        issue["issue_id"] for issue in issues
    }
    assert "remaining_deliverables_allows_remote_training_while_blocked" not in {
        issue["issue_id"] for issue in issues
    }


def test_evaluation_unlock_chain_waits_for_remote_training_completion() -> None:
    chain = _deliverable_unlock_chain(
        [
            {
                "matrix_id": "evaluation:eval_gate3_summary_json",
                "category": "evaluation",
                "artifact_id": "eval_gate3_summary_json",
                "missing": True,
                "current_state": "missing",
                "responsible_stage_id": "gate3_remote_audit_pullback",
                "responsible_stage_allowed_now": False,
                "responsible_stage_blocked_by": ["remote_training_not_completed"],
                "execution_boundary": "read_only_no_execution",
            }
        ]
    )

    row = chain["rows"][0]
    assert row["required_current_blockers"] == ["remote_training_not_completed"]
    assert row["missing_required_current_blockers"] == []


def test_handoff_remote_training_generation_is_allowed_while_status_blocked() -> None:
    issues = _handoff_coverage_issues(
        plan={
            "source_regeneration_targets_by_gate": {
                "approved_remote_preflight": [
                    {"artifact_id": "formal_gate_handoff_bundle"},
                ]
            },
            "ordered_stages": [
                {
                    "stage_id": "regenerate_preflight_gate_artifacts",
                    "command_templates": [
                        "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle"
                    ],
                }
            ],
        },
        source_freshness={
            "ordered_regeneration_targets": [
                {
                    "artifact_id": "formal_gate_handoff_bundle",
                    "required_before": "approved_remote_preflight",
                }
            ]
        },
        status_report={
            "status": "formal_gate_status_blocked",
            "formal_gate_handoff_summary": {"remote_training_allowed_now": True},
        },
    )

    assert "status_report_handoff_training_allowed_while_blocked" not in {
        issue["issue_id"] for issue in issues
    }


def test_remote_packet_safety_allows_handoff_training_generation_while_status_blocked() -> None:
    issues = _remote_packet_cross_gate_issues(
        packet={"execution_steps": {"run_remote_training": {"allowed_now": True}}},
        decision_gate={"decision_state": {"training_allowed_now": True}},
        plan_audit={
            "inputs": {"formal_gate_status_report": "status.json"},
            "current_blocking_summary": {"training_allowed_now": True},
            "status_report_summary": {
                "status": "formal_gate_status_blocked",
                "formal_gate_handoff_summary": {"remote_training_allowed_now": True},
            },
        },
    )

    assert "blocked_status_report_handoff_allows_training" not in {
        issue["issue_id"] for issue in issues
    }


def test_status_report_execution_veto_blocks_only_local_and_claim_when_result_gate_blocked() -> None:
    issues = _formal_gate_execution_veto_issues(
        formal_gate={"status": "blocked_formal_gate_gaps_open"},
        formal_gate_execution_veto={
            "present": True,
            "all_rows_consistent": True,
            "mismatch_rows": [],
            "rows": {"remote_preflight": {}, "local_training": {}, "formal_claim": {}},
            "row_consensus": {
                "remote_preflight": True,
                "local_training": False,
                "formal_claim": False,
            },
        },
    )

    assert "blocked_formal_gate_execution_veto_allows_remote_preflight" not in {
        issue["issue_id"] for issue in issues
    }


def test_post_approval_next_action_guard_is_not_a_pending_execution_leak() -> None:
    rows = [
        {
            "row_id": "status_report_next_action_guard",
            "present": True,
            "path": "status.json",
            "summary_key_path": ("next_action_guard_summary",),
            "signature_matches_baseline": True,
            "status": "next_action_guard_not_applicable",
            "pending_f02_6_decision": False,
            "execution_leak_count": 2,
            "remote_execution_allowed_count": 2,
            "remote_stage_allowed_count": 0,
        }
    ]

    assert _next_action_guard_issues(rows=rows) == []


def test_next_action_guard_rows_preserve_pending_decision_state(tmp_path: Path) -> None:
    summary = {
        "present": True,
        "status": "next_action_guard_not_applicable",
        "pending_f02_6_decision": False,
        "next_blocked_lane_id": "remote_packet_preflight",
        "expected_next_action_id": None,
        "handoff_next_action_id": "manual_handoff_stage_review",
        "handoff_next_action_requires_dr_sun": False,
        "missing_artifacts_next_action_id": "resolve_training_remote_ppo_checkpoint",
        "decision_intake_next_blocked_lane": "remote_packet_preflight",
        "all_execution_disabled_now": False,
        "execution_leak_count": 2,
        "remote_execution_allowed_count": 2,
        "remote_stage_allowed_count": 0,
        "violation_count": 0,
        "execution_leak_surface_ids": [],
    }
    status_report = tmp_path / "status.json"
    claim_safety = tmp_path / "claim.json"
    paper_readiness = tmp_path / "paper.json"
    status_report.write_text(
        json.dumps({"next_action_guard_summary": summary}) + "\n",
        encoding="utf-8",
    )
    claim_safety.write_text(
        json.dumps({"status_report_next_action_guard_summary": summary}) + "\n",
        encoding="utf-8",
    )
    paper_readiness.write_text(
        json.dumps({"claim_safety_next_action_guard_summary": summary}) + "\n",
        encoding="utf-8",
    )

    rows = _next_action_guard_rows(
        FormalGateProofSummaryChainAuditConfig(
            output_dir=tmp_path,
            formal_gate_status_report_path=status_report,
            claim_safety_path=claim_safety,
            paper_readiness_path=paper_readiness,
        )
    )

    assert {row["pending_f02_6_decision"] for row in rows} == {False}
    assert _next_action_guard_issues(rows=rows) == []


def test_post_approval_handoff_single_next_action_can_follow_stages() -> None:
    rows = [
        {
            "row_id": "handoff_bundle_single_next_action_index",
            "present": True,
            "path": "handoff.json",
            "summary_key_path": ("single_next_action_index",),
            "signature_matches_baseline": True,
            "status": "follow_handoff_stages",
            "single_current_human_entry": False,
            "next_action_id": "manual_handoff_stage_review",
            "decision_owner_required": "Dr Sun",
            "valid_decisions": [
                "approve_obstacle_summary_warm_start",
                "reject_obstacle_summary_warm_start",
            ],
            "required_record_fields": ["decision", "decider", "decision_note"],
            "current_allowed_action_ids": [],
            "current_blocked_action_ids": [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "post_decision_routes_are_current_authorization": False,
            "all_execution_disabled_now": False,
            "record_command_template_count": 0,
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "missing_deliverable_count": 10,
            "open_category_count": 4,
            "source_freshness_status": "source_freshness_clean_current",
            "source_freshness_blocking_regeneration_required": False,
            "approved_route_next_lane": "source_fresh_regeneration",
            "rejected_route_next_lane": "protocol_redesign",
            "after_approval_still_requires": [
                "source_freshness_audit",
                "post_f02_6_regeneration_plan",
                "post_f02_6_plan_audit",
                "remote_formal_execution_packet_ready",
                "approved_remote_preflight",
            ],
        }
    ]

    assert _handoff_single_next_action_issues(rows=rows) == []


def test_claim_safety_does_not_require_pending_next_action_guard_after_approval() -> None:
    blockers = _status_report_next_action_guard_blockers(
        {
            "status": "formal_gate_status_blocked",
            "next_action_guard_summary": {
                "present": True,
                "status": "next_action_guard_not_applicable",
                "pending_f02_6_decision": False,
                "next_blocked_lane_id": "remote_packet_preflight",
                "expected_next_action_id": None,
                "handoff_next_action_id": "manual_handoff_stage_review",
                "handoff_next_action_requires_dr_sun": False,
                "missing_artifacts_next_action_id": "resolve_training_remote_ppo_checkpoint",
                "decision_intake_next_blocked_lane": "remote_packet_preflight",
                "all_execution_disabled_now": False,
                "execution_leak_count": 2,
                "remote_execution_allowed_count": 2,
                "remote_stage_allowed_count": 0,
                "violation_count": 0,
            },
        }
    )

    assert blockers == []
