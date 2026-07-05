from __future__ import annotations

import json
from pathlib import Path

from forest_n3p.scripts.build_module2_formal_gate_status_report import (
    _formal_gate_execution_veto_issues,
)
from forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit import (
    FormalGateProofSummaryChainAuditConfig,
    _handoff_single_next_action_issues,
    _next_action_guard_issues,
    _next_action_guard_rows,
)
from forest_n3p.scripts.build_module2_post_f02_6_plan_audit import (
    _cross_artifact_issues,
    _status_report_issues,
)
from forest_n3p.scripts.build_module2_claim_safety import (
    _status_report_next_action_guard_blockers,
)
from forest_n3p.scripts.build_module2_remote_packet_safety_audit import (
    _status_report_execution_veto_issues,
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
