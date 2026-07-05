from __future__ import annotations

import json
from pathlib import Path

from forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit import (
    CURRENT_STATE_MARKER,
    EXPECTED_DECISION_EVIDENCE_MATRIX_ID,
    EXPECTED_DECISION_EVIDENCE_MATRIX_STATUS,
    MainlineFormalGateStateAuditConfig,
    build_manifest,
)


def _write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_not_applicable_next_action_guard_is_accepted_after_f02_6_closes(tmp_path: Path) -> None:
    mainline = tmp_path / "mainline.md"
    status_report = tmp_path / "formal_gate_status_report.json"
    proof_chain = tmp_path / "formal_gate_proof_summary_chain_audit.json"

    mainline.write_text(
        "\n".join(
            [
                "# Module2 Mainline",
                CURRENT_STATE_MARKER,
                "local training remote preflight remote training formal claim paper-result material gpu3070ti-relay",
                EXPECTED_DECISION_EVIDENCE_MATRIX_ID,
                EXPECTED_DECISION_EVIDENCE_MATRIX_STATUS,
                "approve_obstacle_summary_warm_start reject_obstacle_summary_warm_start invalid substitutes",
                "formal_gate_proof_summary_chain_consistent_blocked",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    _write_json(
        status_report,
        {
            "status": "formal_gate_status_blocked",
            "next_action_guard_summary": {
                "present": True,
                "status": "next_action_guard_not_applicable",
                "pending_f02_6_decision": False,
                "expected_next_action_id": None,
                "all_execution_disabled_now": False,
                "execution_leak_count": 2,
            },
            "next_required_formal_deliverables": {
                "present": True,
                "status": "formal_gate_deliverables_blocked",
                "not_paper_result_material": True,
                "runs_training": False,
                "runs_remote_preflight": False,
                "total_missing_deliverables": 0,
                "blocked_category_count": 0,
                "rows": [],
            },
            "f02_6_decision_evidence_matrix_summary": {
                "present": True,
                "matrix_id": EXPECTED_DECISION_EVIDENCE_MATRIX_ID,
                "status": EXPECTED_DECISION_EVIDENCE_MATRIX_STATUS,
                "route_count": 2,
                "route_decisions": [
                    "approve_obstacle_summary_warm_start",
                    "reject_obstacle_summary_warm_start",
                ],
                "required_evidence_count": 7,
                "satisfied_required_evidence_count": 7,
                "missing_required_evidence_count": 0,
                "missing_required_evidence_ids": [],
                "source_issue_count": 0,
                "global_invalid_substitute_count": 4,
            },
        },
    )
    _write_json(
        proof_chain,
        {
            "status": "formal_gate_proof_summary_chain_consistent_blocked",
            "proof_open": True,
            "audit_issue_count": 0,
            "proof_audit_input_safety_issue_count": 0,
            "proof_audit_blockers": [],
            "next_action_guard_row_count": 3,
            "next_action_guard_consistent_row_count": 3,
            "next_required_deliverables_row_count": 3,
            "next_required_deliverables_consistent_row_count": 3,
            "handoff_single_next_action_row_count": 3,
            "handoff_single_next_action_consistent_row_count": 3,
            "runs_training": False,
            "runs_remote_preflight": False,
            "formal_claim_allowed": False,
        },
    )

    manifest = build_manifest(
        MainlineFormalGateStateAuditConfig(
            output_dir=tmp_path,
            mainline_path=mainline,
            formal_gate_status_report_path=status_report,
            proof_summary_chain_audit_path=proof_chain,
        )
    )

    assert manifest["expected_next_action_id"] is None
    assert manifest["expected_next_action_mentioned"] is False
    assert manifest["status"] == "mainline_formal_gate_state_consistent_blocked"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "status_report_next_action_guard_not_passed" not in issue_ids
    assert "status_report_unexpected_next_action" not in issue_ids
    assert "status_report_next_action_guard_execution_leak" not in issue_ids
