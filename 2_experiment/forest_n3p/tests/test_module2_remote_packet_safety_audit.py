import copy
import json
from importlib import import_module


def test_remote_packet_safety_audit_passes_current_blocked_packet(tmp_path):
    try:
        auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing remote packet safety auditor: {exc}") from exc

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_remote_packet_safety_audit"
    assert manifest["status"] == "remote_packet_safety_audit_passed"
    assert manifest["audit_issue_count"] == 0
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["packet_summary"]["status"] == "blocked_until_f02_6_decision"
    assert manifest["packet_summary"]["embedded_preflight_status"] == "blocked"
    assert manifest["packet_summary"]["embedded_preflight_ready"] is False
    assert manifest["packet_summary"]["embedded_preflight_warm_start_decision"] == "pending"
    assert manifest["packet_summary"]["remote_training_allowed_now"] is False
    assert manifest["packet_summary"]["remote_preflight_requirement_counts"] == {"blocked_missing_preflight": 2, "satisfied": 2}
    assert manifest["packet_summary"]["post_run_acceptance_requirement_counts"] == {"blocked_until_remote_audit": 4}
    assert "requires_dr_sun_approval" in manifest["packet_summary"]["sync_blocked_by"]
    assert "remote_packet_not_ready" in manifest["packet_summary"]["remote_training_blocked_by"]
    assert manifest["packet_summary"]["pullback_artifact_count"] == 7
    assert manifest["cross_gate_summary"]["post_plan_status_report_status"] == "formal_gate_status_blocked"
    assert manifest["cross_gate_summary"]["post_plan_status_report_next_blocked_lane_id"] == "decision"
    assert manifest["cross_gate_summary"]["post_plan_status_report_handoff_summary"]["status"] == "blocked_until_f02_6_decision"
    assert manifest["cross_gate_summary"]["post_plan_status_report_handoff_summary"]["remote_training_allowed_now"] is False
    assert manifest["cross_gate_summary"]["post_plan_status_report_execution_veto_summary"]["all_rows_consistent"] is True
    assert manifest["cross_gate_summary"]["post_plan_status_report_execution_veto_summary"]["row_consensus"]["remote_training"] is False
    assert manifest["cross_gate_summary"]["post_plan_status_report_execution_veto_summary"]["row_consensus"]["formal_claim"] is False
    command_index = manifest["cross_gate_summary"]["post_plan_source_regeneration_command_index_summary"]
    assert command_index["present"] is True
    assert command_index["index_row_count"] == 23
    assert command_index["source_target_count"] == 23
    assert command_index["missing_target_ids"] == []
    assert command_index["unknown_manual_count"] == 0
    assert command_index["forbidden_command_count"] == 0
    assert command_index["rows"]["formal_gate_proof_summary_chain_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert command_index["rows"]["mainline_formal_gate_state_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert (
        "build_module2_mainline_formal_gate_state_audit"
        in command_index["rows"]["mainline_formal_gate_state_audit"]["command_template"]
    )
    assert command_index["rows"]["claim_safety"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert command_index["rows"]["paper_readiness"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert manifest["cross_gate_summary"]["post_plan_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["cross_gate_summary"]["post_plan_remaining_deliverables_gap_summary"]["open_category_count"] == 4
    assert (
        manifest["cross_gate_summary"]["post_plan_status_report_remaining_deliverables_gap_summary"][
            "total_missing_deliverables"
        ]
        == 10
    )
    proof_deliverables = manifest["cross_gate_summary"]["post_plan_proof_audit_deliverables_summary"]
    assert proof_deliverables["present"] is True
    assert proof_deliverables["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert proof_deliverables["next_blocked_lane"] == "decision"
    assert proof_deliverables["h01_status"] == "blocked_pending_decisions"
    assert proof_deliverables["h02_status"] == "blocked_formal_output_acceptance"
    assert proof_deliverables["h02_paper_result_input_allowed"] is False
    assert (
        manifest["cross_gate_summary"]["post_plan_status_report_proof_audit_deliverables_summary"][
            "missing_counts_by_formal_category"
        ]
        == proof_deliverables["missing_counts_by_formal_category"]
    )
    status_steps = manifest["cross_gate_summary"]["post_plan_status_report_remote_execution_step_summary"]
    assert status_steps["sync_to_remote"]["blocked_by"] == ["requires_dr_sun_approval"]
    assert status_steps["run_remote_training"]["blocked_by"] == ["requires_dr_sun_approval", "remote_packet_not_ready"]


def test_remote_packet_safety_audit_ignores_downstream_handoff_safety_feedback(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_summary"]["formal_gate_handoff_summary"]["safety_issue_count"] = 2

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "post_plan_handoff_safety_issues_open" not in issue_ids
    assert manifest["status"] == "remote_packet_safety_audit_passed"


def test_remote_packet_safety_audit_catches_pending_packet_that_allows_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["ready_to_run_remote_training"] = True
    packet["execution_steps"]["sync_to_remote"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_training"]["allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_packet_ready_to_train" in issue_ids
    assert "pending_decision_packet_allows_sync" in issue_ids
    assert "pending_packet_training_step_allowed" in issue_ids
    assert "decision_gate_blocks_but_packet_allows_training" in issue_ids
    assert "post_plan_blocks_but_packet_allows_training" in issue_ids
    assert "blocked_status_report_packet_ready" in issue_ids
    assert "blocked_status_report_allows_remote_sync" in issue_ids
    assert "blocked_status_report_allows_remote_training" in issue_ids


def test_remote_packet_safety_audit_requires_blocked_steps_to_explain_blockers(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["execution_steps"]["sync_to_remote"]["blocked_by"] = []
    packet["execution_steps"]["run_remote_training"]["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "sync_to_remote_missing_blocked_by" in issue_ids
    assert "sync_to_remote_missing_requires_dr_sun_approval" in issue_ids
    assert "run_remote_training_missing_blocked_by" in issue_ids
    assert "run_remote_training_missing_remote_packet_not_ready" in issue_ids


def test_remote_packet_safety_audit_catches_pending_embedded_preflight_ready(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["remote_preflight"]["preflight_status"] = "ready"
    packet["remote_preflight"]["formal_trial_ready"] = True
    packet["remote_preflight"]["warm_start_decision"] = "approved_obstacle_summary"
    packet["remote_preflight"]["blocker_codes"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_decision_preflight_ready" in issue_ids
    assert "pending_decision_preflight_status_ready" in issue_ids
    assert "pending_decision_preflight_warm_start_not_pending" in issue_ids
    assert "pending_decision_preflight_missing_pending_blocker" in issue_ids


def test_remote_packet_safety_audit_requires_remote_preflight_requirement_matrix(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet.pop("remote_preflight_requirements")
    packet.pop("remote_preflight_requirement_counts")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "packet_missing_remote_preflight_requirements" in issue_ids


def test_remote_packet_safety_audit_catches_pending_preflight_requirement_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    requirements = {item["requirement_id"]: item for item in packet["remote_preflight_requirements"]}
    requirements["f02_6_decision_closed_for_preflight"]["status"] = "satisfied"
    requirements["f02_6_decision_closed_for_preflight"]["complete"] = True
    requirements["f02_6_decision_closed_for_preflight"]["missing_artifact_ids"] = []
    requirements["approved_remote_preflight_manifest"]["execution_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_decision_requirement_satisfied" in issue_ids
    assert "approved_remote_preflight_manifest_allowed_while_packet_blocked" in issue_ids


def test_remote_packet_safety_audit_catches_ready_packet_with_unready_embedded_preflight(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["status"] = "ready_for_gpu3070ti_remote_training"
    packet["ready_to_run_remote_training"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload(record_status="approved", training_allowed=True)),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload(training_allowed=True, status_report_ready=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "ready_packet_preflight_not_ready" in issue_ids
    assert "ready_packet_preflight_status_not_ready" in issue_ids
    assert "ready_packet_preflight_warm_start_not_approved" in issue_ids


def test_remote_packet_safety_audit_requires_post_run_acceptance_requirement_matrix(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet.pop("post_run_acceptance_requirements")
    packet.pop("post_run_acceptance_requirement_counts")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "packet_missing_post_run_acceptance_requirements" in issue_ids


def test_remote_packet_safety_audit_catches_post_run_requirement_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    requirements = {item["requirement_id"]: item for item in packet["post_run_acceptance_requirements"]}
    requirements["checkpoint_hash_manifest_recorded"]["status"] = "satisfied"
    requirements["checkpoint_hash_manifest_recorded"]["complete"] = True
    requirements["gate3_formal_audit_accepts_remote_run"]["execution_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "checkpoint_hash_manifest_recorded_satisfied_before_local_audit" in issue_ids
    assert "gate3_formal_audit_accepts_remote_run_execution_allowed_now" in issue_ids


def test_remote_packet_safety_audit_requires_post_plan_status_report_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["inputs"] = {}
    plan_audit.pop("status_report_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_status_report_input" in issue_ids
    assert "post_plan_missing_status_report_summary" in issue_ids


def test_remote_packet_safety_audit_requires_post_plan_status_report_remote_step_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_summary"].pop("remote_execution_step_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_status_report_remote_step_summary" in issue_ids


def test_remote_packet_safety_audit_requires_post_plan_status_report_handoff_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_summary"].pop("formal_gate_handoff_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_status_report_handoff_summary" in issue_ids


def test_remote_packet_safety_audit_requires_post_plan_status_report_execution_veto_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_summary"].pop("formal_gate_execution_veto_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_status_report_execution_veto_summary" in issue_ids


def test_remote_packet_safety_audit_requires_post_plan_command_index_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    summary = plan_audit["source_regeneration_command_index_summary"]
    summary["missing_target_ids"] = ["paper_readiness"]
    summary["unknown_manual_count"] = 1
    summary["unknown_manual_ids"] = ["claim_safety"]
    summary["forbidden_command_count"] = 1
    summary["forbidden_command_ids"] = ["paper_readiness"]
    summary["rows"].pop("paper_readiness")
    summary["rows"]["claim_safety"]["stage_id"] = "manual_review"

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_source_regeneration_command_index_missing_targets" in issue_ids
    assert "post_plan_source_regeneration_command_index_unknown_manual_rows" in issue_ids
    assert "post_plan_source_regeneration_command_index_forbidden_commands" in issue_ids
    assert "post_plan_source_regeneration_command_index_claim_safety_wrong_stage" in issue_ids
    assert "post_plan_source_regeneration_command_index_missing_paper_readiness" in issue_ids


def test_remote_packet_safety_audit_allows_current_clean_claim_safety_omitted_from_command_index(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    summary = plan_audit["source_regeneration_command_index_summary"]
    summary["rows"].pop("claim_safety")
    summary["index_row_count"] = 21
    summary["source_target_count"] = 21

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_passed"
    assert "post_plan_source_regeneration_command_index_missing_claim_safety" not in issue_ids


def test_remote_packet_safety_audit_requires_remaining_deliverables_gap_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit.pop("remaining_deliverables_gap_summary")
    plan_audit["status_report_summary"].pop("remaining_deliverables_gap_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_remaining_deliverables_gap_summary" in issue_ids
    assert "post_plan_missing_status_report_remaining_deliverables_gap_summary" in issue_ids


def test_remote_packet_safety_audit_rejects_remaining_deliverables_gap_summary_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] = 2
    plan_audit["status_report_summary"]["formal_claim_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_status_report_remaining_deliverables_gap_summary_mismatch" in issue_ids
    assert "status_report_allows_formal_claim_with_remaining_gap_open" in issue_ids


def test_remote_packet_safety_audit_requires_proof_audit_deliverables_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit.pop("status_report_proof_audit_deliverables_summary")
    plan_audit["status_report_summary"].pop("proof_audit_deliverables_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_proof_audit_deliverables_summary" in issue_ids
    assert "post_plan_status_report_missing_proof_audit_deliverables_summary" in issue_ids


def test_remote_packet_safety_audit_rejects_proof_audit_deliverables_summary_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_summary"]["proof_audit_deliverables_summary"]["missing_counts_by_formal_category"][
        "training"
    ] = 2
    plan_audit["status_report_summary"]["formal_claim_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_status_report_proof_audit_deliverables_summary_mismatch" in issue_ids
    assert "status_report_allows_formal_claim_with_proof_deliverables_missing" in issue_ids


def test_remote_packet_safety_audit_rejects_h02_paper_input_with_missing_proof_deliverables(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_proof_audit_deliverables_summary"]["h02_paper_result_input_allowed"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_status_report_proof_audit_deliverables_summary_mismatch" in issue_ids
    assert "proof_deliverables_allow_h02_paper_input_while_missing" in issue_ids


def test_remote_packet_safety_audit_catches_status_report_execution_veto_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    veto = plan_audit["status_report_summary"]["formal_gate_execution_veto_summary"]
    veto["all_rows_consistent"] = False
    veto["mismatch_rows"] = ["remote_training"]
    veto["row_consensus"]["remote_training"] = True
    veto["rows"]["remote_training"]["consistent"] = False
    veto["rows"]["remote_training"]["consensus_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_execution_veto_rows_inconsistent" in issue_ids
    assert "post_plan_execution_veto_mismatch_rows_open" in issue_ids
    assert "blocked_status_report_execution_veto_allows_remote_training" in issue_ids
    assert "post_plan_execution_veto_remote_training_packet_mismatch" in issue_ids


def test_remote_packet_safety_audit_catches_status_report_remote_step_mismatch(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["status_report_summary"]["remote_execution_step_summary"]["run_remote_training"]["allowed_now"] = True
    plan_audit["status_report_summary"]["remote_execution_step_summary"]["run_remote_training"]["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_status_report_run_remote_training_allowed_mismatch" in issue_ids
    assert "post_plan_status_report_run_remote_training_blockers_mismatch" in issue_ids


def test_remote_packet_safety_audit_catches_status_report_handoff_mismatch(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    handoff = plan_audit["status_report_summary"]["formal_gate_handoff_summary"]
    handoff["remote_training_allowed_now"] = True
    handoff["remote_execution_steps"]["run_remote_training"]["allowed_now"] = True
    handoff["remote_execution_steps"]["run_remote_training"]["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "blocked_status_report_handoff_allows_training" in issue_ids
    assert "post_plan_handoff_run_remote_training_allowed_mismatch" in issue_ids
    assert "post_plan_handoff_run_remote_training_blockers_mismatch" in issue_ids


def test_remote_packet_safety_audit_blocks_remote_actions_when_status_report_blocked(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["status"] = "ready_for_gpu3070ti_remote_training"
    packet["ready_to_run_remote_training"] = True
    packet["execution_steps"]["sync_to_remote"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_preflight"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_training"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_audit"]["allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_decision_packet_not_blocked" in issue_ids
    assert "pending_decision_packet_allows_sync" in issue_ids
    assert "blocked_status_report_packet_ready" in issue_ids
    assert "blocked_status_report_allows_remote_sync" in issue_ids
    assert "blocked_status_report_allows_remote_preflight" in issue_ids
    assert "blocked_status_report_allows_remote_training" in issue_ids
    assert "blocked_status_report_allows_remote_audit" in issue_ids


def test_remote_packet_safety_audit_catches_host_sync_and_command_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["execution_environment"]["gpu_alias"] = "local-mac"
    packet["execution_environment"]["training_host_required"] = "local-mac"
    packet["execution_steps"]["sync_to_remote"]["command"] += " --delete"
    packet["execution_steps"]["run_remote_training"]["command"] = "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cpu"
    packet["execution_steps"]["run_remote_audit"]["command"] = "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial"

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "packet_wrong_gpu_alias" in issue_ids
    assert "packet_wrong_training_host" in issue_ids
    assert "sync_uses_delete" in issue_ids
    assert "training_not_remote_ssh" in issue_ids
    assert "training_missing_device_cuda" in issue_ids
    assert "training_missing_bc_checkpoint" in issue_ids
    assert "audit_missing_ssh_gpu3070ti_relay" in issue_ids
    assert "audit_missing_warm_start_decision_approved_obstacle_summary" in issue_ids


def test_remote_packet_safety_audit_catches_pullback_and_downstream_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["post_run_pullback"]["expected_artifacts"] = packet["post_run_pullback"]["expected_artifacts"][:2]
    packet["post_run_pullback"]["hash_manifest_required"] = False
    packet["post_run_pullback"]["pullback_command"] = "rsync -az --delete localhost:/tmp/run ./run"
    packet["downstream_after_successful_audit"]["h01_manifest_must_be_regenerated"] = False
    packet["downstream_after_successful_audit"]["formal_claim_requires"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "pullback_wrong_artifact_count" in issue_ids
    assert "pullback_hash_manifest_not_required" in issue_ids
    assert "pullback_not_from_gpu3070ti" in issue_ids
    assert "pullback_uses_delete" in issue_ids
    assert "downstream_missing_h01_manifest_must_be_regenerated" in issue_ids
    assert "claim_requirement_missing_gate3_formal_audit_formal_decision_is_pass" in issue_ids


def test_remote_packet_safety_audit_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

    rc = auditor.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--remote-packet",
            str(_json(tmp_path, "packet.json", _packet_payload())),
            "--decision-gate-audit",
            str(_json(tmp_path, "decision_gate.json", _decision_gate_payload())),
            "--post-plan-audit",
            str(_json(tmp_path, "plan_audit.json", _plan_audit_payload())),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "remote_packet_safety_audit_passed"
    assert "Module2 Remote Packet Safety Audit" in markdown
    assert "post_plan_execution_veto_remote_training_allowed_now" in markdown
    assert "post_plan_command_index_row_count" in markdown
    assert "post_plan_remaining_deliverables_gap_total_missing" in markdown
    assert "does not execute any command" in markdown


def _packet_payload():
    trial = "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1"
    return {
        "packet_name": "module2_remote_formal_execution_packet",
        "status": "blocked_until_f02_6_decision",
        "ready_to_run_remote_training": False,
        "local_training_allowed": False,
        "formal_claim_allowed_before_audit": False,
        "execution_environment": {
            "gpu_alias": "gpu3070ti-relay",
            "remote_workdir": "~/ForestNav",
            "remote_python": ".venv/bin/python",
            "training_host_required": "gpu3070ti-relay",
        },
        "remote_preflight": {
            "path": "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json",
            "exists": True,
            "preflight_status": "blocked",
            "formal_trial_ready": False,
            "warm_start_decision": "pending",
            "blocker_codes": ["warm_start_decision_pending"],
        },
        "remote_preflight_requirements": _remote_preflight_requirements_payload(),
        "remote_preflight_requirement_counts": {"blocked_missing_preflight": 2, "satisfied": 2},
        "execution_steps": {
            "sync_to_remote": {
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["requires_dr_sun_approval"],
                "command": "rsync -az --exclude .git --exclude '.venv*' --exclude __pycache__ --exclude .pytest_cache --exclude 1_survey /local/ForestNav/ 'gpu3070ti-relay:~/ForestNav/'",
            },
            "run_remote_preflight": {
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["requires_dr_sun_approval"],
                "command": "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial'",
            },
            "run_remote_training": {
                "allowed_now": False,
                "runs_training": True,
                "blocked_by": ["requires_dr_sun_approval", "remote_packet_not_ready"],
                "command": (
                    "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python "
                    "-m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda --bc-checkpoint checkpoint.pt "
                    "--eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8'"
                ),
            },
            "run_remote_audit": {
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["requires_dr_sun_approval", "remote_packet_not_ready"],
                "command": "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --warm-start-decision approved_obstacle_summary'",
            },
        },
        "post_run_pullback": {
            "required_before_local_claim": True,
            "hash_manifest_required": True,
            "expected_artifacts": [
                f"{trial}/train/final_model.zip",
                f"{trial}/train/summary.json",
                f"{trial}/train/training_manifest.json",
                f"{trial}/eval/gate3_eval_episodes.csv",
                f"{trial}/eval/gate3_summary.json",
                f"{trial}/gate3_trial_manifest.json",
                f"{trial}/gate3_formal_audit.json",
            ],
            "pullback_command": f"rsync -az 'gpu3070ti-relay:~/ForestNav/{trial}/' /local/ForestNav/{trial}/",
        },
        "post_run_acceptance_requirements": _post_run_acceptance_requirements_payload(),
        "post_run_acceptance_requirement_counts": {"blocked_until_remote_audit": 4},
        "downstream_after_successful_audit": {
            "h01_manifest_must_be_regenerated": True,
            "h02_full_smoke_must_be_regenerated": True,
            "paper_tables_must_be_regenerated_from_h02_formal_outputs": True,
            "formal_claim_requires": [
                "gate3_formal_audit.formal_decision is pass",
                "pulled-back checkpoint hash is recorded",
                "H01 manifest status becomes ready_for_formal_run with this checkpoint",
                "H02 full all-method smoke and formal evaluation outputs include required_output_schema columns",
            ],
        },
    }


def _remote_preflight_requirements_payload():
    return [
        {
            "requirement_id": "f02_6_decision_closed_for_preflight",
            "phase": "decision",
            "status": "blocked_missing_preflight",
            "complete": False,
            "execution_allowed_now": False,
            "required_before": "run_remote_preflight",
            "missing_artifact_ids": ["f02_6_decision_record_approved_by_dr_sun"],
            "blocked_by": ["requires_dr_sun_approval"],
            "acceptable_evidence": ["f02_6_decision_record.json with status=approved"],
            "invalid_substitutes": ["decision packet recommendation without Dr Sun decision record"],
        },
        {
            "requirement_id": "approved_remote_preflight_manifest",
            "phase": "remote_preflight",
            "status": "blocked_missing_preflight",
            "complete": False,
            "execution_allowed_now": False,
            "required_before": "run_remote_training",
            "missing_artifact_ids": ["approved_remote_preflight_manifest_ready"],
            "blocked_by": ["warm_start_decision_pending"],
            "acceptable_evidence": ["gate3_preflight_manifest.json with preflight_status=ready"],
            "invalid_substitutes": ["pending remote preflight manifest"],
        },
        {
            "requirement_id": "remote_preflight_protocol_contract",
            "phase": "remote_preflight",
            "status": "satisfied",
            "complete": True,
            "execution_allowed_now": False,
            "required_before": "run_remote_training",
            "missing_artifact_ids": [],
            "blocked_by": [],
            "acceptable_evidence": ["preflight protocol has device=cuda"],
            "invalid_substitutes": ["smoke protocol"],
        },
        {
            "requirement_id": "remote_preflight_command_packetized",
            "phase": "remote_preflight",
            "status": "satisfied",
            "complete": True,
            "execution_allowed_now": False,
            "required_before": "run_remote_preflight",
            "missing_artifact_ids": [],
            "blocked_by": ["requires_dr_sun_approval"],
            "acceptable_evidence": ["run_remote_preflight command is an ssh gpu3070ti-relay command"],
            "invalid_substitutes": ["bare local python preflight command"],
        },
    ]


def _post_run_acceptance_requirements_payload():
    return [
        {
            "requirement_id": "pullback_expected_artifacts_complete",
            "phase": "pullback",
            "status": "blocked_until_remote_audit",
            "complete": False,
            "remote_training_ready_now": False,
            "execution_allowed_now": False,
            "required_before": "local_gate3_formal_audit_review",
            "missing_artifact_ids": [],
            "acceptable_evidence": ["all seven expected Gate3 artifacts pulled back locally"],
            "invalid_substitutes": ["remote stdout saying files exist"],
        },
        {
            "requirement_id": "checkpoint_hash_manifest_recorded",
            "phase": "pullback",
            "status": "blocked_until_remote_audit",
            "complete": False,
            "remote_training_ready_now": False,
            "execution_allowed_now": False,
            "required_before": "h01_h02_regeneration",
            "missing_artifact_ids": [],
            "acceptable_evidence": ["SHA-256 record for train/final_model.zip"],
            "invalid_substitutes": ["checkpoint file without hash"],
        },
        {
            "requirement_id": "gate3_formal_audit_accepts_remote_run",
            "phase": "acceptance",
            "status": "blocked_until_remote_audit",
            "complete": False,
            "remote_training_ready_now": False,
            "execution_allowed_now": False,
            "required_before": "formal_claim_gate",
            "missing_artifact_ids": ["gate3_formal_audit_formal_decision_pass"],
            "acceptable_evidence": ["gate3_formal_audit.json with formal_decision=pass"],
            "invalid_substitutes": ["training completion without audit"],
        },
        {
            "requirement_id": "h01_h02_regenerated_from_audited_checkpoint",
            "phase": "evaluation_acceptance",
            "status": "blocked_until_remote_audit",
            "complete": False,
            "remote_training_ready_now": False,
            "execution_allowed_now": False,
            "required_before": "paper_result_gate",
            "missing_artifact_ids": [],
            "acceptable_evidence": ["H01 and H02 regenerated from the audited checkpoint"],
            "invalid_substitutes": ["paper table preview generated before H02 acceptance"],
        },
    ]


def _decision_gate_payload(*, record_status="pending_human_decision", training_allowed=False):
    return {
        "status": "f02_6_decision_gate_pending_clean" if record_status == "pending_human_decision" else "f02_6_decision_gate_approved_clean",
        "decision_state": {
            "record_status": record_status,
            "training_allowed_now": training_allowed,
        },
    }


def _plan_audit_payload(*, training_allowed=False, status_report_ready=False):
    step_blockers = [] if status_report_ready else ["requires_dr_sun_approval"]
    training_blockers = [] if status_report_ready else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    return {
        "status": "post_f02_6_plan_audit_passed",
        "inputs": {
            "formal_gate_status_report": "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
        },
        "current_blocking_summary": {
            "training_allowed_now": training_allowed,
            "remote_preflight_allowed_now": training_allowed,
        },
        "source_regeneration_command_index_summary": _source_regeneration_command_index_summary(),
        "remaining_deliverables_gap_summary": _gap_summary(open_gaps=not status_report_ready),
        "status_report_proof_audit_deliverables_summary": _deliverables_top_level_summary(open_gaps=not status_report_ready),
        "status_report_summary": {
            "status": "formal_gate_status_ready_for_claim_audit" if status_report_ready else "formal_gate_status_blocked",
            "formal_claim_allowed_now": status_report_ready,
            "local_training_allowed_now": False,
            "next_blocked_lane_id": None if status_report_ready else "decision",
            "remaining_deliverables_gap_summary": _gap_summary(open_gaps=not status_report_ready),
            "proof_audit_deliverables_summary": _deliverables_top_level_summary(open_gaps=not status_report_ready),
            "remote_execution_step_summary": {
                "sync_to_remote": {
                    "present": True,
                    "allowed_now": status_report_ready,
                    "runs_training": False,
                    "blocked_by": step_blockers,
                },
                "run_remote_preflight": {
                    "present": True,
                    "allowed_now": status_report_ready,
                    "runs_training": False,
                    "blocked_by": step_blockers,
                },
                "run_remote_training": {
                    "present": True,
                    "allowed_now": status_report_ready,
                    "runs_training": True,
                    "blocked_by": training_blockers,
                },
                "run_remote_audit": {
                    "present": True,
                    "allowed_now": status_report_ready,
                    "runs_training": False,
                    "blocked_by": training_blockers,
                },
            },
            "formal_gate_handoff_summary": {
                "status": "ready_for_manual_remote_execution_review" if status_report_ready else "blocked_until_f02_6_decision",
                "next_handoff_action_id": "manual_execution_review" if status_report_ready else "record_f02_6_decision",
                "safety_issue_count": 0,
                "remote_training_allowed_now": status_report_ready,
                "remote_preflight_allowed_now": status_report_ready,
                "formal_claim_allowed_now": status_report_ready,
                "remote_execution_steps": {
                    "sync_to_remote": {
                        "present": True,
                        "allowed_now": status_report_ready,
                        "runs_training": False,
                        "blocked_by": step_blockers,
                    },
                    "run_remote_preflight": {
                        "present": True,
                        "allowed_now": status_report_ready,
                        "runs_training": False,
                        "blocked_by": step_blockers,
                    },
                    "run_remote_training": {
                        "present": True,
                        "allowed_now": status_report_ready,
                        "runs_training": True,
                        "blocked_by": training_blockers,
                    },
                    "run_remote_audit": {
                        "present": True,
                        "allowed_now": status_report_ready,
                        "runs_training": False,
                        "blocked_by": training_blockers,
                    },
                },
            },
            "formal_gate_execution_veto_summary": _execution_veto_summary(ready=status_report_ready),
        },
    }


def _source_regeneration_command_index_summary():
    rows = {
        "formal_gate_proof_summary_chain_audit": {
            "required_before": "formal_claim_gate",
            "stage_id": "regenerate_claim_gate_artifacts",
            "command_kind": "known_builder",
            "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit",
        },
        "claim_safety": {
            "required_before": "formal_claim_gate",
            "stage_id": "regenerate_claim_gate_artifacts",
            "command_kind": "known_builder",
            "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety",
        },
        "mainline_formal_gate_state_audit": {
            "required_before": "formal_claim_gate",
            "stage_id": "regenerate_claim_gate_artifacts",
            "command_kind": "known_builder",
            "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit",
        },
        "paper_readiness": {
            "required_before": "formal_claim_gate",
            "stage_id": "regenerate_claim_gate_artifacts",
            "command_kind": "known_builder",
            "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness",
        },
    }
    return {
        "present": True,
        "index_row_count": 23,
        "source_target_count": 23,
        "missing_target_ids": [],
        "unknown_manual_count": 0,
        "unknown_manual_ids": [],
        "forbidden_command_count": 0,
        "forbidden_command_ids": [],
        "rows": rows,
    }


def _gap_summary(*, open_gaps):
    return {
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "total_missing_deliverables": 10 if open_gaps else 0,
        "open_category_count": 4 if open_gaps else 0,
        "category_order": ["training", "evaluation", "acceptance", "formal_acceptance"],
        "categories": {
            "training": _gap_category("training", 3 if open_gaps else 0, "gate3_remote_training", open_gaps=open_gaps),
            "evaluation": _gap_category("evaluation", 2 if open_gaps else 0, "gate3_remote_audit_pullback", open_gaps=open_gaps),
            "acceptance": _gap_category("acceptance", 3 if open_gaps else 0, "gate3_remote_audit_pullback", open_gaps=open_gaps),
            "formal_acceptance": _gap_category(
                "formal_acceptance",
                2 if open_gaps else 0,
                "regenerate_h01_h02_formal_artifacts",
                open_gaps=open_gaps,
            ),
        },
    }


def _deliverables_top_level_summary(*, open_gaps):
    counts = {
        "training": 3 if open_gaps else 0,
        "evaluation": 2 if open_gaps else 0,
        "acceptance": 3 if open_gaps else 0,
        "formal_acceptance": 2 if open_gaps else 0,
    }
    return {
        "missing_counts_by_formal_category": counts,
        "missing_matrix_ids_by_formal_category": {
            category: [f"{category}:artifact_{index}" for index in range(count)]
            for category, count in counts.items()
        },
        "next_blocked_lane": "decision" if open_gaps else None,
        "h01_status": "blocked_pending_decisions" if open_gaps else "ready_for_formal_run",
        "h02_status": "blocked_formal_output_acceptance" if open_gaps else "formal_output_accepted",
        "h02_formal_output_accepted": not open_gaps,
        "h02_paper_result_input_allowed": not open_gaps,
    }


def _gap_category(category, missing_count, stage_id, *, open_gaps):
    return {
        "missing_count": missing_count,
        "responsible_stage_id": stage_id,
        "responsible_stage_allowed_now": not open_gaps,
        "missing_artifact_matrix_ids": [f"{category}:artifact_{index}" for index in range(missing_count)],
    }


def _execution_veto_summary(*, ready):
    rows = {
        "local_training": _veto_row(
            False,
            {
                "formal_gate_gap_audit": False,
                "status_report": False,
                "handoff_bundle": False,
                "remote_packet": False,
            },
        ),
        "remote_preflight": _veto_row(
            ready,
            {
                "status_report": ready,
                "handoff_bundle": ready,
                "remote_packet": ready,
                "remote_packet_safety": ready,
            },
        ),
        "remote_training": _veto_row(
            ready,
            {
                "decision_record": ready,
                "status_report": ready,
                "handoff_bundle": ready,
                "remote_packet": ready,
                "remote_packet_safety": ready,
            },
        ),
        "remote_audit": _veto_row(
            ready,
            {
                "handoff_bundle": ready,
                "remote_packet": ready,
                "remote_packet_safety": ready,
            },
        ),
        "formal_claim": _veto_row(
            ready,
            {
                "status_report": ready,
                "handoff_bundle": ready,
            },
        ),
    }
    return {
        "present": True,
        "matrix_version": 1,
        "all_rows_consistent": True,
        "mismatch_rows": [],
        "row_count": len(rows),
        "row_consensus": {row_id: row["consensus_allowed_now"] for row_id, row in rows.items()},
        "rows": rows,
    }


def _veto_row(consensus, sources):
    return {
        "consistent": len(set(sources.values())) <= 1,
        "consensus_allowed_now": consensus,
        "allowed_now_by_source": sources,
    }


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(copy.deepcopy(payload)), encoding="utf-8")
    return path
