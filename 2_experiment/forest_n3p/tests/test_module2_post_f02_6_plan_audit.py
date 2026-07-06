import copy
import json
from importlib import import_module


def test_post_f02_6_plan_audit_passes_current_pending_blocked_plan(tmp_path):
    try:
        auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing post-F02.6 plan auditor: {exc}") from exc

    plan = _plan_payload()
    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
            protocol_lane_status_report_path=_json(
                tmp_path,
                "protocol_lane_status.json",
                _protocol_lane_status_payload(),
            ),
            remaining_deliverables_path=_json(
                tmp_path,
                "remaining_deliverables.json",
                _remaining_deliverables_payload(open_gaps=True),
            ),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_post_f02_6_plan_audit"
    assert manifest["status"] == "post_f02_6_plan_audit_passed"
    assert manifest["audit_issue_count"] == 0
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["current_blocking_summary"]["training_allowed_now"] is False
    assert manifest["current_blocking_summary"]["remote_preflight_allowed_now"] is False
    decision_request = manifest["f02_6_human_decision_request_summary"]
    assert decision_request["present"] is True
    assert decision_request["status"] == "awaiting_dr_sun_decision"
    assert decision_request["decision_owner_required"] == "Dr Sun"
    assert decision_request["current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert decision_request["current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert decision_request["post_decision_routes_are_current_authorization"] is False
    assert decision_request["all_execution_disabled_now"] is True
    assert decision_request["remote_preflight_allowed_now"] is False
    assert decision_request["remote_training_allowed_now"] is False
    assert decision_request["formal_claim_allowed_now"] is False
    assert decision_request["local_training_allowed_now"] is False
    command_index = manifest["source_regeneration_command_index_summary"]
    assert command_index["present"] is True
    assert command_index["index_row_count"] == 10
    assert command_index["source_target_count"] == 10
    assert command_index["unknown_manual_count"] == 0
    assert command_index["stage_mismatch_count"] == 0
    assert command_index["command_not_in_stage_count"] == 0
    assert command_index["forbidden_command_count"] == 0
    assert command_index["stage_counts"] == {
        "regenerate_claim_gate_artifacts": 4,
        "regenerate_h01_h02_formal_artifacts": 1,
        "regenerate_preflight_gate_artifacts": 5,
    }
    assert manifest["inputs"]["formal_gate_status_report"].endswith("status_report.json")
    assert manifest["status_report_summary"]["status"] == "formal_gate_status_blocked"
    assert manifest["status_report_summary"]["formal_claim_allowed_now"] is False
    assert manifest["status_report_summary"]["next_blocked_lane_id"] == "decision"
    assert manifest["status_report_summary"]["formal_gate_handoff_summary"]["status"] == "blocked_until_f02_6_decision"
    assert manifest["status_report_summary"]["formal_gate_handoff_summary"]["remote_training_allowed_now"] is False
    assert manifest["status_report_summary"]["formal_gate_execution_veto_summary"]["present"] is True
    assert manifest["status_report_summary"]["formal_gate_execution_veto_summary"]["all_rows_consistent"] is True
    assert manifest["status_report_summary"]["formal_gate_execution_veto_summary"]["row_consensus"]["remote_training"] is False
    assert manifest["status_report_summary"]["formal_gate_execution_veto_summary"]["row_consensus"]["formal_claim"] is False
    protocol = manifest["protocol_lane_status_summary"]
    assert manifest["inputs"]["protocol_lane_status_report"].endswith("protocol_lane_status.json")
    assert protocol["status"] == "protocol_lane_status_blocked_pending_lane_decision"
    assert protocol["audit_issue_count"] == 0
    assert protocol["next_blocked_lane"] == "protocol_lane_decision"
    assert protocol["selected_lane_id"] is None
    assert protocol["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert protocol["blocked_action_ids"] == [
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    ]
    assert protocol["post_decision_contract_plan_status"] == "post_decision_contract_plan_ready_blocked_pending_lane_decision"
    assert protocol["post_decision_contract_plan_required_section_count"] == 8
    assert protocol["post_decision_contract_plan_shared_artifact_count"] == 10
    assert protocol["post_decision_contract_plan_shared_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert protocol[
        "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"
    ] is True
    assert protocol["post_decision_contract_plan_lane_count"] == 4
    assert protocol["next_success_attempt_artifact_count"] == 10
    assert protocol["next_success_attempt_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert protocol["next_success_attempt_artifact_ids_by_category"]["training"] == [
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ]
    assert protocol["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 4
    unlock_chain = manifest["remaining_deliverables_unlock_chain_summary"]
    assert unlock_chain["present"] is True
    assert unlock_chain["status"] == "blocked_missing_formal_deliverables"
    assert unlock_chain["row_count"] == 10
    assert unlock_chain["blocked_row_count"] == 10
    assert unlock_chain["rows_with_missing_required_blockers"] == 0
    assert unlock_chain["rows_allowed_while_missing"] == 0
    assert unlock_chain["categories"]["training"]["row_count"] == 3
    assert unlock_chain["categories"]["training"]["required_current_blockers"] == [
        "f02_6_decision_not_approved",
        "remote_packet_not_ready",
    ]
    assert manifest["status_report_summary"]["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    proof_deliverables = manifest["status_report_proof_audit_deliverables_summary"]
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
    steps = manifest["status_report_summary"]["remote_execution_step_summary"]
    assert steps["sync_to_remote"]["allowed_now"] is False
    assert steps["sync_to_remote"]["blocked_by"] == ["requires_dr_sun_approval"]
    assert steps["run_remote_training"]["runs_training"] is True
    assert "remote_packet_not_ready" in steps["run_remote_training"]["blocked_by"]


def test_post_f02_6_plan_audit_uses_artifact_records_for_full_command_index(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    source_freshness = _source_freshness_payload()
    artifact_records = source_freshness["ordered_regeneration_targets"]
    source_freshness["status"] = "source_freshness_tracked_artifact_lag_only_gate_ready"
    source_freshness["regeneration_required_before_remote_formal_execution"] = False
    source_freshness["artifact_records"] = artifact_records
    source_freshness["ordered_regeneration_targets"] = [
        row for row in artifact_records if row["artifact_id"] == "formal_gate_handoff_bundle"
    ]
    plan["source_regeneration_targets_by_gate"] = {
        "approved_remote_preflight": [
            {
                "artifact_id": "formal_gate_handoff_bundle",
                "path": "handoff.json",
                "freshness_state": "historical_clean",
            }
        ]
    }
    plan["current_gate_summary"]["source_freshness_status"] = "source_freshness_tracked_artifact_lag_only_gate_ready"
    plan["current_gate_summary"]["source_freshness_regeneration_required"] = False

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", source_freshness),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
            remaining_deliverables_path=_json(
                tmp_path,
                "remaining_deliverables.json",
                _remaining_deliverables_payload(open_gaps=True),
            ),
        )
    )

    summary = manifest["source_regeneration_command_index_summary"]
    assert manifest["audit_issue_count"] == 0
    assert summary["index_row_count"] == len(artifact_records)
    assert summary["source_target_count"] == len(artifact_records)
    assert summary["missing_target_ids"] == []
    assert summary["extra_index_ids"] == []
    assert summary["rows"]["formal_gate_proof_summary_chain_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert summary["rows"]["mainline_formal_gate_state_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert summary["rows"]["claim_safety"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert summary["rows"]["paper_readiness"]["stage_id"] == "regenerate_claim_gate_artifacts"


def test_post_f02_6_plan_audit_catches_training_allowed_while_f02_6_pending(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["blocking_summary"]["training_allowed_now"] = True
    training = _stage(plan, "gate3_remote_training")
    training["allowed_now"] = True
    training["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "pending_f02_6_allows_training" in issue_ids
    assert "training_stage_allowed_before_f02_6" in issue_ids
    assert "training_stage_missing_f02_6_decision_not_approved" in issue_ids
    assert "training_stage_missing_remote_packet_not_ready" in issue_ids


def test_post_f02_6_plan_audit_catches_f02_6_human_decision_request_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    request = plan["f02_6_human_decision_request_summary"]
    request["status"] = "approved"
    request["decision_owner_required"] = "automation"
    request["current_allowed_action_ids"] = ["record_f02_6_decision", "remote_preflight"]
    request["current_blocked_action_ids"] = ["remote_training"]
    request["post_decision_routes_are_current_authorization"] = True
    request["all_execution_disabled_now"] = False
    request["remote_preflight_allowed_now"] = True
    request["remote_training_allowed_now"] = True
    request["formal_claim_allowed_now"] = True
    request["local_training_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "pending_f02_6_human_decision_request_not_awaiting_dr_sun" in issue_ids
    assert "pending_f02_6_human_decision_request_owner_not_dr_sun" in issue_ids
    assert "pending_f02_6_human_decision_request_allowed_actions_not_decision_only" in issue_ids
    assert "pending_f02_6_human_decision_request_missing_blocked_actions" in issue_ids
    assert "pending_f02_6_human_decision_request_treats_routes_as_authorization" in issue_ids
    assert "pending_f02_6_human_decision_request_execution_not_disabled" in issue_ids
    assert "pending_f02_6_human_decision_request_remote_preflight_allowed_now_not_false" in issue_ids
    assert "pending_f02_6_human_decision_request_remote_training_allowed_now_not_false" in issue_ids
    assert "pending_f02_6_human_decision_request_formal_claim_allowed_now_not_false" in issue_ids
    assert "pending_f02_6_human_decision_request_local_training_allowed_now_not_false" in issue_ids


def test_post_f02_6_plan_audit_catches_remote_training_host_and_command_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["current_gate_summary"]["f02_6_decision_status"] = "approved"
    plan["status"] = "ready_for_remote_training_packet_execution"
    plan["blocking_summary"]["training_allowed_now"] = True
    training = _stage(plan, "gate3_remote_training")
    training["allowed_now"] = True
    training["blocked_by"] = []
    training["host"] = "local-mac"
    training["command_templates"] = ["python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda"]

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload(decision_status="approved")),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "training_stage_not_gpu3070ti" in issue_ids
    assert "ready_training_stage_missing_remote_ssh" in issue_ids


def test_post_f02_6_plan_audit_catches_stage_order_and_source_target_mismatch(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["ordered_stages"] = [stage for stage in plan["ordered_stages"] if stage["stage_id"] != "approved_remote_preflight"]
    plan["source_regeneration_targets_by_gate"]["approved_remote_preflight"] = plan["source_regeneration_targets_by_gate"]["approved_remote_preflight"][:1]

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "missing_stage_approved_remote_preflight" in issue_ids
    assert "plan_source_regeneration_target_counts_mismatch" in issue_ids


def test_post_f02_6_plan_audit_requires_complete_source_regeneration_command_index(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    index = plan["source_regeneration_command_index"]
    index[0]["command_kind"] = "unknown_manual"
    index[1]["stage_id"] = "regenerate_claim_gate_artifacts"
    index[2]["command_template"] = "ssh gpu3070ti-relay 'run training'"
    index[3].pop("command_template")
    index.pop()

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "source_regeneration_command_index_missing_source_targets" in issue_ids
    assert "source_regeneration_command_index_unknown_manual_rows" in issue_ids
    assert "source_regeneration_command_index_stage_mismatch" in issue_ids
    assert "source_regeneration_command_index_command_missing_from_stage" in issue_ids
    assert "source_regeneration_command_index_contains_execution_commands" in issue_ids
    assert "source_regeneration_command_index_rows_missing_required_fields" in issue_ids
    summary = manifest["source_regeneration_command_index_summary"]
    assert summary["missing_target_ids"] == ["paper_readiness"]
    assert summary["unknown_manual_count"] == 1
    assert summary["stage_mismatch_count"] == 1
    assert summary["forbidden_command_count"] == 1


def test_post_f02_6_plan_audit_requires_handoff_source_fresh_coverage(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["source_regeneration_targets_by_gate"]["approved_remote_preflight"] = [
        target
        for target in plan["source_regeneration_targets_by_gate"]["approved_remote_preflight"]
        if target["artifact_id"] != "formal_gate_handoff_bundle"
    ]
    regen = _stage(plan, "regenerate_preflight_gate_artifacts")
    regen["command_templates"] = [
        command for command in regen["command_templates"] if "build_module2_formal_gate_handoff_bundle" not in command
    ]
    source_freshness = _source_freshness_payload()
    source_freshness["ordered_regeneration_targets"] = [
        target
        for target in source_freshness["ordered_regeneration_targets"]
        if target["artifact_id"] != "formal_gate_handoff_bundle"
    ]
    status_report = _status_report_payload(ready=False)
    status_report.pop("formal_gate_handoff_summary")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", source_freshness),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "handoff_bundle_missing_from_source_freshness" in issue_ids
    assert "handoff_bundle_missing_from_plan_preflight_targets" in issue_ids
    assert "handoff_bundle_missing_regeneration_command" in issue_ids
    assert "status_report_missing_handoff_summary" in issue_ids


def test_post_f02_6_plan_audit_consumes_open_missing_artifacts_inventory_without_blocking_training_step(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    assert manifest["status"] == "post_f02_6_plan_audit_passed"
    assert manifest["missing_artifacts_summary"]["all_required_evidence_present"] is False
    assert manifest["missing_artifacts_summary"]["missing_counts_by_category"]["training"] == 3
    assert manifest["audit_issues"] == []


def test_post_f02_6_plan_audit_catches_claim_gate_ready_with_open_missing_artifacts(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["current_gate_summary"]["f02_6_decision_status"] = "approved"
    plan["status"] = "ready_for_claim_gate"
    claim_stage = _stage(plan, "regenerate_claim_gate_artifacts")
    claim_stage["allowed_now"] = True
    claim_stage["status"] = "ready"
    claim_stage["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload(decision_status="approved")),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "claim_gate_ready_before_formal_acceptance" in issue_ids
    assert "claim_gate_ready_with_missing_artifacts" in issue_ids


def test_post_f02_6_plan_audit_rejects_missing_artifacts_inventory_that_runs_or_claims(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(
                tmp_path,
                "missing_artifacts.json",
                _missing_artifacts_payload(open_inventory=False, invalid=True),
            ),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=False)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "missing_artifacts_inventory_executes_commands" in issue_ids
    assert "missing_artifacts_inventory_runs_training" in issue_ids
    assert "missing_artifacts_inventory_runs_preflight" in issue_ids
    assert "missing_artifacts_inventory_allows_local_training" in issue_ids
    assert "missing_artifacts_inventory_allows_claim" in issue_ids
    assert "missing_artifacts_inventory_has_audit_issues" in issue_ids


def test_post_f02_6_plan_audit_catches_claim_gate_ready_with_open_closure_checklist(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["current_gate_summary"]["f02_6_decision_status"] = "approved"
    plan["status"] = "ready_for_claim_gate"
    claim_stage = _stage(plan, "regenerate_claim_gate_artifacts")
    claim_stage["allowed_now"] = True
    claim_stage["status"] = "ready"
    claim_stage["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload(decision_status="approved")),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=False)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "claim_gate_ready_with_open_closure_checklist" in issue_ids


def test_post_f02_6_plan_audit_rejects_closure_checklist_that_runs_or_claims(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=False, invalid=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "closure_checklist_executes_commands" in issue_ids
    assert "closure_checklist_runs_training" in issue_ids
    assert "closure_checklist_runs_preflight" in issue_ids
    assert "closure_checklist_allows_local_training" in issue_ids
    assert "closure_checklist_allows_claim" in issue_ids
    assert "closure_checklist_has_input_safety_issues" in issue_ids


def test_post_f02_6_plan_audit_rejects_status_report_that_runs_or_claims(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False, invalid=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "formal_gate_status_report_executes_commands" in issue_ids
    assert "formal_gate_status_report_runs_training" in issue_ids
    assert "formal_gate_status_report_runs_preflight" in issue_ids
    assert "formal_gate_status_report_allows_local_training" in issue_ids
    assert "formal_gate_status_report_allows_claim" in issue_ids
    assert "formal_gate_status_report_allows_local_training_now" in issue_ids
    assert "formal_gate_status_report_claim_permission_inconsistent" in issue_ids
    assert "formal_gate_status_report_has_input_safety_issues" in issue_ids


def test_post_f02_6_plan_audit_ignores_downstream_feedback_loop_issues(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    missing_artifacts = _missing_artifacts_payload(open_inventory=True)
    missing_artifacts["audit_issue_count"] = 2
    missing_artifacts["audit_issues"] = [
        {"issue_id": "transition_gate_audit_not_passed"},
        {"issue_id": "transition_gate_audit_issues_open"},
    ]
    status_report = _status_report_payload(ready=False)
    status_report["input_safety_issue_count"] = 1
    status_report["input_safety_issues"] = [{"issue_id": "handoff_bundle_safety_issues_open"}]
    status_report["formal_gate_handoff_summary"]["safety_issue_count"] = 2

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", missing_artifacts),
            closure_checklist_path=_json(
                tmp_path,
                "closure_checklist.json",
                _closure_checklist_payload(open_checklist=True),
            ),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "missing_artifacts_inventory_has_audit_issues" not in issue_ids
    assert "formal_gate_status_report_has_input_safety_issues" not in issue_ids
    assert "status_report_handoff_safety_issues_open" not in issue_ids
    assert manifest["status"] == "post_f02_6_plan_audit_passed"


def test_post_f02_6_plan_audit_requires_status_report_remote_step_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    status_report = _status_report_payload(ready=False)
    status_report.pop("remote_execution_step_summary")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "formal_gate_status_report_missing_remote_step_summary" in issue_ids


def test_post_f02_6_plan_audit_rejects_blocked_status_report_with_allowed_remote_step(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    status_report = _status_report_payload(ready=False)
    status_report["remote_execution_step_summary"]["run_remote_training"]["allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "formal_gate_status_report_training_step_permission_mismatch" in issue_ids
    assert "formal_gate_status_report_blocked_but_run_remote_training_allowed" not in issue_ids


def test_post_f02_6_plan_audit_requires_status_report_execution_veto_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    status_report = _status_report_payload(ready=False)
    status_report.pop("formal_gate_execution_veto_summary")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "formal_gate_status_report_missing_execution_veto_summary" in issue_ids


def test_post_f02_6_plan_audit_rejects_status_report_execution_veto_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    status_report = _status_report_payload(ready=False)
    veto = status_report["formal_gate_execution_veto_summary"]
    veto["all_rows_consistent"] = False
    veto["mismatch_rows"] = ["remote_training"]
    veto["row_consensus"]["remote_training"] = True
    veto["rows"]["remote_training"]["consistent"] = False
    veto["rows"]["remote_training"]["consensus_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "formal_gate_status_report_execution_veto_inconsistent" in issue_ids
    assert "formal_gate_status_report_execution_veto_mismatch_rows_open" in issue_ids
    assert "formal_gate_status_report_blocked_veto_allows_remote_training" not in issue_ids
    assert "formal_gate_status_report_execution_veto_permission_mismatch_remote_training" in issue_ids


def test_post_f02_6_plan_audit_catches_claim_gate_ready_with_blocked_status_report(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["current_gate_summary"]["f02_6_decision_status"] = "approved"
    plan["status"] = "ready_for_claim_gate"
    claim_stage = _stage(plan, "regenerate_claim_gate_artifacts")
    claim_stage["allowed_now"] = True
    claim_stage["status"] = "ready"
    claim_stage["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload(decision_status="approved")),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=False)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=False)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "claim_gate_ready_with_blocked_status_report" in issue_ids


def test_post_f02_6_plan_audit_rejects_remaining_deliverables_gap_summary_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] = 2
    status_report = _status_report_payload(ready=False)
    status_report["remaining_deliverables_gap_summary"]["total_missing_deliverables"] = 9

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
            remaining_deliverables_path=_json(
                tmp_path,
                "remaining_deliverables.json",
                _remaining_deliverables_payload(open_gaps=True),
            ),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "plan_remaining_deliverables_gap_summary_mismatch" in issue_ids
    assert "status_report_remaining_deliverables_gap_summary_mismatch" in issue_ids


def test_post_f02_6_plan_audit_rejects_remaining_deliverables_unlock_chain_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["remaining_deliverables_unlock_chain_summary"]["rows_allowed_while_missing"] = 1
    remaining_deliverables = _remaining_deliverables_payload(open_gaps=True)
    remaining_deliverables["deliverable_unlock_chain"]["rows"][0]["missing_required_current_blockers"] = [
        "f02_6_decision_not_approved"
    ]
    remaining_deliverables["deliverable_unlock_chain"]["rows"][1]["responsible_stage_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
            remaining_deliverables_path=_json(tmp_path, "remaining_deliverables.json", remaining_deliverables),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "plan_remaining_deliverables_unlock_chain_summary_mismatch" in issue_ids
    assert "plan_remaining_deliverables_unlock_chain_rows_allowed_while_missing" in issue_ids
    assert "remaining_deliverables_unlock_chain_rows_missing_required_blockers" in issue_ids
    assert "remaining_deliverables_unlock_chain_rows_allowed_while_missing" not in issue_ids


def test_post_f02_6_plan_audit_rejects_proof_audit_deliverables_summary_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    status_report = _status_report_payload(ready=False)
    status_report["formal_gate_proof_audit_remaining_deliverables_top_level_summary"][
        "missing_counts_by_formal_category"
    ]["training"] = 2

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
            remaining_deliverables_path=_json(
                tmp_path,
                "remaining_deliverables.json",
                _remaining_deliverables_payload(open_gaps=True),
            ),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "status_report_proof_audit_deliverables_summary_mismatch" in issue_ids


def test_post_f02_6_plan_audit_requires_proof_audit_deliverables_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    status_report = _status_report_payload(ready=False)
    status_report.pop("formal_gate_proof_audit_remaining_deliverables_top_level_summary")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", status_report),
            remaining_deliverables_path=_json(
                tmp_path,
                "remaining_deliverables.json",
                _remaining_deliverables_payload(open_gaps=True),
            ),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "status_report_missing_proof_audit_deliverables_summary" in issue_ids


def test_post_f02_6_plan_audit_rejects_protocol_lane_status_post_plan_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    protocol = _protocol_lane_status_payload()
    current = protocol["current_status"]
    current["selected_lane_id"] = "full_patch_cnn_policy"
    current["allowed_next_action_ids"] = [
        "record_protocol_lane_decision",
        "remote_success_training",
    ]
    current["post_decision_contract_plan_required_section_count"] = 7
    current["post_decision_contract_plan_shared_artifact_category_counts"]["training"] = 2
    current["post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"] = False
    current["post_decision_contract_plan_runs_training"] = True
    current["next_success_attempt_artifact_count"] = 9
    current["next_success_attempt_artifact_category_counts"]["evaluation"] = 1
    current["old_failed_run_artifacts_invalid_for_next_success_attempt"] = False
    current["next_success_attempt_artifact_ids_by_category"]["evaluation"] = [
        "eval_gate3_eval_episodes_csv"
    ]
    current["remote_training_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
            closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True)),
            status_report_path=_json(tmp_path, "status_report.json", _status_report_payload(ready=False)),
            protocol_lane_status_report_path=_json(tmp_path, "protocol_lane_status.json", protocol),
            remaining_deliverables_path=_json(
                tmp_path,
                "remaining_deliverables.json",
                _remaining_deliverables_payload(open_gaps=True),
            ),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "protocol_lane_status_selected_lane_present" in issue_ids
    assert "protocol_lane_status_allowed_actions_drift" in issue_ids
    assert "protocol_lane_status_authorization_leak" in issue_ids
    assert "protocol_lane_status_post_decision_contract_plan_required_section_count_drift" in issue_ids
    assert "protocol_lane_status_post_plan_authorization_leak" in issue_ids
    assert "protocol_lane_status_next_artifact_count_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_category_counts_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_ids_missing" in issue_ids


def test_post_f02_6_plan_audit_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
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
            "--plan",
            str(_json(tmp_path, "plan.json", _plan_payload())),
            "--formal-gate",
            str(_json(tmp_path, "formal_gate.json", _formal_gate_payload())),
            "--source-freshness-audit",
            str(_json(tmp_path, "source_freshness.json", _source_freshness_payload())),
            "--missing-artifacts-audit",
            str(_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True))),
            "--closure-checklist",
            str(_json(tmp_path, "closure_checklist.json", _closure_checklist_payload(open_checklist=True))),
            "--status-report",
            str(_json(tmp_path, "status_report.json", _status_report_payload(ready=False))),
            "--protocol-lane-status-report",
            str(_json(tmp_path, "protocol_lane_status.json", _protocol_lane_status_payload())),
            "--remaining-deliverables",
            str(_json(tmp_path, "remaining_deliverables.json", _remaining_deliverables_payload(open_gaps=True))),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "post_f02_6_plan_audit_passed"
    assert "Module2 Post-F02.6 Plan Audit" in markdown
    assert "F02.6 Human Decision Request" in markdown
    assert "record_f02_6_decision" in markdown
    assert "Source Regeneration Command Index" in markdown
    assert "Remaining Deliverables Gap Summary" in markdown
    assert "Remaining Deliverables Unlock Chain" in markdown
    assert "Protocol Lane Status Report" in markdown
    assert "protocol_lane_status_blocked_pending_lane_decision" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "train_final_model_zip" in markdown
    assert "Status Report Remote Execution Steps" in markdown
    assert "Status Report Execution Veto Matrix" in markdown
    assert "does not execute the plan" in markdown


def _plan_payload():
    return {
        "schema_version": 1,
        "artifact_name": "module2_post_f02_6_regeneration_plan",
        "status": "blocked_until_f02_6_decision",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "current_gate_summary": {
            "f02_6_decision_status": "pending_human_decision",
            "formal_gate_status": "blocked_formal_gate_gaps_open",
            "source_freshness_status": "source_freshness_risks_recorded_gate_still_blocked",
            "source_freshness_regeneration_required": True,
            "remote_packet_status": "blocked_until_f02_6_decision",
            "ready_to_run_remote_training": False,
        },
        "f02_6_human_decision_request_summary": {
            "present": True,
            "status": "awaiting_dr_sun_decision",
            "decision_owner_required": "Dr Sun",
            "current_allowed_action_ids": ["record_f02_6_decision"],
            "current_blocked_action_ids": [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "post_decision_routes_are_current_authorization": False,
            "all_execution_disabled_now": True,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "local_training_allowed_now": False,
        },
        "remaining_deliverables_gap_summary": _gap_summary(open_gaps=True),
        "remaining_deliverables_unlock_chain_summary": _unlock_chain_summary(open_gaps=True),
        "source_regeneration_targets_by_gate": {
            "approved_remote_preflight": [
                {
                    "artifact_id": "f02_6_warm_start_decision_packet",
                    "path": "decision_packet.json",
                    "freshness_state": "historical_dirty",
                },
                {"artifact_id": "f02_6_decision_record", "path": "a.json", "freshness_state": "historical_dirty"},
                {"artifact_id": "formal_gate_gap_audit", "path": "b.json", "freshness_state": "historical_dirty"},
                {
                    "artifact_id": "formal_gate_handoff_bundle",
                    "path": "handoff.json",
                    "freshness_state": "historical_clean",
                },
                {
                    "artifact_id": "post_f02_6_regeneration_plan",
                    "path": "post_plan.json",
                    "freshness_state": "historical_dirty",
                },
            ],
            "formal_h01_h02": [
                {"artifact_id": "h01_evaluation_manifest", "path": "h01.json", "freshness_state": "historical_dirty"}
            ],
            "formal_claim_gate": [
                {"artifact_id": "claim_safety", "path": "claim.json", "freshness_state": "historical_clean"},
                {
                    "artifact_id": "formal_gate_proof_summary_chain_audit",
                    "path": "proof_summary_chain.json",
                    "freshness_state": "historical_dirty",
                },
                {
                    "artifact_id": "mainline_formal_gate_state_audit",
                    "path": "mainline_formal_gate_state_audit.json",
                    "freshness_state": "historical_dirty",
                },
                {
                    "artifact_id": "paper_readiness",
                    "path": "paper_readiness.json",
                    "freshness_state": "historical_dirty",
                },
            ],
        },
        "source_regeneration_command_index": [
            _command_index_row(
                "f02_6_warm_start_decision_packet",
                "approved_remote_preflight",
                "decision_packet.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_warm_start_decision_packet",
            ),
            _command_index_row(
                "f02_6_decision_record",
                "approved_remote_preflight",
                "a.json",
                "human_decision_record",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'",
            ),
            _command_index_row(
                "formal_gate_gap_audit",
                "approved_remote_preflight",
                "b.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit",
            ),
            _command_index_row(
                "formal_gate_handoff_bundle",
                "approved_remote_preflight",
                "handoff.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle",
            ),
            _command_index_row(
                "post_f02_6_regeneration_plan",
                "approved_remote_preflight",
                "post_plan.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan",
            ),
            _command_index_row(
                "h01_evaluation_manifest",
                "formal_h01_h02",
                "h01.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest --module2-rl-rs-checkpoint <pulled-back-final_model.zip>",
            ),
            _command_index_row(
                "claim_safety",
                "formal_claim_gate",
                "claim.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety",
            ),
            _command_index_row(
                "formal_gate_proof_summary_chain_audit",
                "formal_claim_gate",
                "proof_summary_chain.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit",
            ),
            _command_index_row(
                "mainline_formal_gate_state_audit",
                "formal_claim_gate",
                "mainline_formal_gate_state_audit.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit",
            ),
            _command_index_row(
                "paper_readiness",
                "formal_claim_gate",
                "paper_readiness.json",
                "known_builder",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness",
            ),
        ],
        "blocking_summary": {
            "blocked_stage_ids": [
                "regenerate_preflight_gate_artifacts",
                "approved_remote_preflight",
                "regenerate_remote_execution_packet",
                "gate3_remote_training",
                "gate3_remote_audit_pullback",
                "regenerate_h01_h02_formal_artifacts",
                "regenerate_claim_gate_artifacts",
            ],
            "ready_stage_ids": ["f02_6_decision_record"],
            "training_allowed_now": False,
            "remote_preflight_allowed_now": False,
        },
        "ordered_stages": [
            _stage_payload("f02_6_decision_record", "decision", allowed=True, human=True),
            _stage_payload(
                "regenerate_preflight_gate_artifacts",
                "regeneration",
                blocked_by=["f02_6_decision_not_approved"],
                commands=[
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_warm_start_decision_packet",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan",
                ],
            ),
            _stage_payload(
                "approved_remote_preflight",
                "remote_preflight",
                runs_remote_preflight=True,
                host="gpu3070ti-relay",
                blocked_by=["f02_6_decision_not_approved", "source_fresh_preflight_targets_open"],
            ),
            _stage_payload(
                "regenerate_remote_execution_packet",
                "regeneration",
                blocked_by=["f02_6_decision_not_approved", "source_fresh_preflight_targets_open"],
            ),
            _stage_payload(
                "gate3_remote_training",
                "training",
                runs_training=True,
                host="gpu3070ti-relay",
                blocked_by=["f02_6_decision_not_approved", "source_fresh_preflight_targets_open", "remote_packet_not_ready"],
                command="ssh gpu3070ti-relay 'cd ~/ForestNav && run train'",
            ),
            _stage_payload("gate3_remote_audit_pullback", "acceptance", host="gpu3070ti-relay", blocked_by=["remote_packet_not_ready"]),
            _stage_payload(
                "regenerate_h01_h02_formal_artifacts",
                "evaluation",
                blocked_by=["missing_remote_audit_pullback", "source_fresh_h01_h02_targets_open"],
                command="PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest --module2-rl-rs-checkpoint <pulled-back-final_model.zip>",
            ),
            _stage_payload(
                "regenerate_claim_gate_artifacts",
                "claim_gate",
                blocked_by=["h02_formal_acceptance_not_ready", "source_fresh_claim_targets_open"],
                commands=[
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit",
                    "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness",
                ],
            ),
        ],
    }


def _command_index_row(artifact_id, required_before, path, command_kind, command_template):
    if required_before == "approved_remote_preflight":
        stage_id = "regenerate_preflight_gate_artifacts"
    elif required_before == "formal_h01_h02":
        stage_id = "regenerate_h01_h02_formal_artifacts"
    elif required_before == "formal_claim_gate":
        stage_id = "regenerate_claim_gate_artifacts"
    else:
        stage_id = "manual_review"
    return {
        "artifact_id": artifact_id,
        "required_before": required_before,
        "freshness_state": "historical_dirty",
        "path": path,
        "stage_id": stage_id,
        "command_kind": command_kind,
        "command_template": command_template,
    }


def _stage_payload(
    stage_id,
    phase,
    *,
    allowed=False,
    human=False,
    runs_training=False,
    runs_remote_preflight=False,
    host=None,
    blocked_by=(),
    command="",
    commands=(),
):
    return {
        "stage_id": stage_id,
        "phase": phase,
        "status": "ready" if allowed else "blocked",
        "allowed_now": allowed,
        "blocked_by": list(blocked_by),
        "runs_training": runs_training,
        "runs_remote_preflight": runs_remote_preflight,
        "host": host,
        "requires_human_input": human,
        "action": stage_id,
        "evidence_paths": [],
        "command_templates": list(commands) if commands else ([command] if command else []),
    }


def _formal_gate_payload(*, decision_status="pending_human_decision"):
    return {
        "status": "blocked_formal_gate_gaps_open",
        "current_gate_state": {
            "f02_6_decision_status": decision_status,
            "source_freshness_regeneration_required": True,
        },
    }


def _source_freshness_payload():
    return {
        "status": "source_freshness_risks_recorded_gate_still_blocked",
        "regeneration_required_before_remote_formal_execution": True,
        "ordered_regeneration_targets": [
            {
                "artifact_id": "f02_6_warm_start_decision_packet",
                "path": "decision_packet.json",
                "required_before": "approved_remote_preflight",
            },
            {"artifact_id": "f02_6_decision_record", "path": "a.json", "required_before": "approved_remote_preflight"},
            {"artifact_id": "formal_gate_gap_audit", "path": "b.json", "required_before": "approved_remote_preflight"},
            {
                "artifact_id": "formal_gate_handoff_bundle",
                "path": "handoff.json",
                "required_before": "approved_remote_preflight",
            },
            {
                "artifact_id": "post_f02_6_regeneration_plan",
                "path": "post_plan.json",
                "required_before": "approved_remote_preflight",
            },
            {"artifact_id": "h01_evaluation_manifest", "path": "h01.json", "required_before": "formal_h01_h02"},
            {"artifact_id": "claim_safety", "path": "claim.json", "required_before": "formal_claim_gate"},
            {
                "artifact_id": "formal_gate_proof_summary_chain_audit",
                "path": "proof_summary_chain.json",
                "required_before": "formal_claim_gate",
            },
            {
                "artifact_id": "mainline_formal_gate_state_audit",
                "path": "mainline_formal_gate_state_audit.json",
                "required_before": "formal_claim_gate",
            },
            {
                "artifact_id": "paper_readiness",
                "path": "paper_readiness.json",
                "required_before": "formal_claim_gate",
            },
        ],
    }


def _missing_artifacts_payload(*, open_inventory, invalid=False):
    return {
        "status": "formal_gate_missing_artifacts_open" if open_inventory else "formal_gate_artifacts_complete",
        "executes_commands": bool(invalid),
        "runs_training": bool(invalid),
        "runs_remote_preflight": bool(invalid),
        "local_training_allowed": bool(invalid),
        "formal_claim_allowed": bool(invalid),
        "all_required_evidence_present": not open_inventory,
        "audit_issue_count": 1 if invalid else 0,
        "missing_counts_by_category": {"training": 3, "evaluation": 2, "acceptance": 3} if open_inventory else {},
    }


def _closure_checklist_payload(*, open_checklist, invalid=False):
    return {
        "status": "formal_gate_closure_blocked" if open_checklist else "formal_gate_closure_ready_for_result_audit",
        "executes_commands": bool(invalid),
        "runs_training": bool(invalid),
        "runs_remote_preflight": bool(invalid),
        "local_training_allowed": bool(invalid),
        "formal_claim_allowed": bool(invalid),
        "closure_item_count": 8,
        "open_item_count": 8 if open_checklist else 0,
        "input_safety_issue_count": 1 if invalid else 0,
    }


def _status_report_payload(*, ready, invalid=False):
    step_blockers = [] if ready else ["requires_dr_sun_approval"]
    training_blockers = [] if ready else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    return {
        "status": "formal_gate_status_ready_for_claim_audit" if ready else "formal_gate_status_blocked",
        "executes_commands": bool(invalid),
        "runs_training": bool(invalid),
        "runs_remote_preflight": bool(invalid),
        "local_training_allowed": bool(invalid),
        "formal_claim_allowed": bool(invalid),
        "permissions_now": {
            "formal_claim_allowed_now": ready or bool(invalid),
            "local_training_allowed_now": bool(invalid),
            "remote_preflight_allowed_now": ready,
            "remote_training_allowed_now": ready,
        },
        "input_safety_issue_count": 1 if invalid else 0,
        "next_blocked_lane": {} if ready else {"lane_id": "decision", "blocked_by": ["f02_6_decision_not_approved"]},
        "remote_execution_step_summary": {
            "sync_to_remote": {
                "present": True,
                "allowed_now": ready,
                "runs_training": False,
                "blocked_by": step_blockers,
            },
            "run_remote_preflight": {
                "present": True,
                "allowed_now": ready,
                "runs_training": False,
                "blocked_by": step_blockers,
            },
            "run_remote_training": {
                "present": True,
                "allowed_now": ready,
                "runs_training": True,
                "blocked_by": training_blockers,
            },
            "run_remote_audit": {
                "present": True,
                "allowed_now": ready,
                "runs_training": False,
                "blocked_by": training_blockers,
            },
        },
        "formal_gate_handoff_summary": {
            "status": "ready_for_manual_remote_execution_review" if ready else "blocked_until_f02_6_decision",
            "next_handoff_action_id": "manual_execution_review" if ready else "record_f02_6_decision",
            "safety_issue_count": 0,
            "remote_training_allowed_now": ready,
            "remote_preflight_allowed_now": ready,
            "formal_claim_allowed_now": ready,
        },
        "remaining_deliverables_gap_summary": _gap_summary(open_gaps=not ready),
        "formal_gate_proof_audit_remaining_deliverables_top_level_summary": _deliverables_top_level_summary(open_gaps=not ready),
        "formal_gate_execution_veto_summary": _execution_veto_summary(ready=ready),
    }


def _protocol_lane_status_payload():
    return {
        "status": "protocol_lane_status_blocked_pending_lane_decision",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "audit_issue_count": 0,
        "current_status": {
            "next_blocked_lane": "protocol_lane_decision",
            "selected_lane_id": None,
            "allowed_next_action_ids": ["record_protocol_lane_decision"],
            "blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
            "post_decision_contract_plan_summary_present": True,
            "post_decision_contract_plan_status": "post_decision_contract_plan_ready_blocked_pending_lane_decision",
            "post_decision_contract_plan_audit_issue_count": 0,
            "post_decision_contract_plan_required_section_count": 8,
            "post_decision_contract_plan_shared_artifact_count": 10,
            "post_decision_contract_plan_shared_artifact_category_counts": {
                "contract": 1,
                "training": 3,
                "evaluation": 2,
                "acceptance": 3,
                "formal_acceptance": 1,
            },
            "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt": True,
            "post_decision_contract_plan_lane_count": 4,
            "post_decision_contract_plan_writes_contract": False,
            "post_decision_contract_plan_approves_contract": False,
            "post_decision_contract_plan_runs_training": False,
            "post_decision_contract_plan_runs_remote_preflight": False,
            "post_decision_contract_plan_remote_training_allowed_now": False,
            "post_decision_contract_plan_formal_claim_allowed": False,
            "post_decision_contract_plan_paper_result_material_allowed": False,
            "post_decision_contract_plan_gate_contract_drafting_allowed_now": False,
            "next_success_attempt_artifact_status": "blocked_until_protocol_lane_decision_and_contract",
            "next_success_attempt_artifact_count": 10,
            "next_success_attempt_artifact_category_counts": {
                "contract": 1,
                "training": 3,
                "evaluation": 2,
                "acceptance": 3,
                "formal_acceptance": 1,
            },
            "next_success_attempt_artifact_ids_by_category": {
                "contract": ["new_or_revised_research_contract"],
                "training": [
                    "train_final_model_zip",
                    "train_summary_json",
                    "train_training_manifest_json",
                ],
                "evaluation": ["eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"],
                "acceptance": [
                    "gate3_trial_manifest_json",
                    "gate3_formal_audit_json",
                    "pulled_back_checkpoint_hash_record",
                ],
                "formal_acceptance": ["h02_formal_output_acceptance"],
            },
            "old_failed_run_artifacts_invalid_for_next_success_attempt": True,
            "contract_drafting_allowed_now": False,
            "contract_approval_allowed_now": False,
            "draft_contract_allows_training": False,
            "local_training_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "new_success_training_allowed_now": False,
        },
    }


def _remaining_deliverables_payload(*, open_gaps):
    return {
        **_deliverables_top_level_summary(open_gaps=open_gaps),
        "deliverable_gap_summary": _gap_summary(open_gaps=open_gaps),
        "deliverable_unlock_chain": _unlock_chain_ledger(open_gaps=open_gaps),
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


def _gap_summary(*, open_gaps):
    return {
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
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


def _gap_category(category, missing_count, stage_id, *, open_gaps):
    return {
        "present": True,
        "missing_count": missing_count,
        "responsible_stage_id": stage_id,
        "responsible_stage_allowed_now": not open_gaps,
        "missing_artifact_matrix_ids": [f"{category}:artifact_{index}" for index in range(missing_count)],
    }


def _unlock_chain_summary(*, open_gaps):
    categories = {
        category: _unlock_chain_category(category, count, open_gaps=open_gaps)
        for category, count in _formal_category_counts().items()
    }
    return {
        "present": True,
        "chain_id": "module2_formal_gate_missing_deliverable_unlock_chain",
        "status": "blocked_missing_formal_deliverables" if open_gaps else "formal_deliverables_complete",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "row_count": sum(_formal_category_counts().values()),
        "blocked_row_count": sum(_formal_category_counts().values()) if open_gaps else 0,
        "rows_with_missing_required_blockers": 0,
        "rows_allowed_while_missing": 0,
        "categories": categories,
    }


def _unlock_chain_ledger(*, open_gaps):
    rows = [
        _unlock_chain_row(category, index, open_gaps=open_gaps)
        for category, count in _formal_category_counts().items()
        for index in range(count)
    ]
    return {
        "chain_id": "module2_formal_gate_missing_deliverable_unlock_chain",
        "status": "blocked_missing_formal_deliverables" if open_gaps else "formal_deliverables_complete",
        "not_paper_result_material": True,
        "execution_boundary": "read_only_no_execution",
        "row_count": len(rows),
        "blocked_row_count": len(rows) if open_gaps else 0,
        "rows_with_missing_required_blockers": 0,
        "rows_allowed_while_missing": 0,
        "rows": rows,
    }


def _formal_category_counts():
    return {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }


def _unlock_chain_category(category, row_count, *, open_gaps):
    return {
        "row_count": row_count,
        "blocked_row_count": row_count if open_gaps else 0,
        "rows_with_missing_required_blockers": 0,
        "rows_allowed_while_missing": 0,
        "required_current_blockers": _unlock_required_blockers(category),
        "unlock_sequence_before_stage_allowed": _unlock_sequence(category),
    }


def _unlock_chain_row(category, index, *, open_gaps):
    return {
        "matrix_id": f"{category}:artifact_{index}",
        "category": category,
        "artifact_id": f"{category}_artifact_{index}",
        "current_state": "missing" if open_gaps else "present",
        "missing": open_gaps,
        "responsible_stage_id": _unlock_responsible_stage(category),
        "responsible_stage_allowed_now": not open_gaps,
        "required_current_blockers": _unlock_required_blockers(category),
        "missing_required_current_blockers": [],
        "unlock_sequence_before_stage_allowed": _unlock_sequence(category),
        "execution_boundary": "read_only_no_execution",
    }


def _unlock_responsible_stage(category):
    if category == "training":
        return "gate3_remote_training"
    if category in {"evaluation", "acceptance"}:
        return "gate3_remote_audit_pullback"
    return "regenerate_h01_h02_formal_artifacts"


def _unlock_required_blockers(category):
    if category == "formal_acceptance":
        return ["missing_remote_audit_pullback"]
    return ["f02_6_decision_not_approved", "remote_packet_not_ready"]


def _unlock_sequence(category):
    if category == "training":
        return [
            "record_f02_6_decision",
            "source_freshness_ready_for_remote_preflight",
            "remote_formal_execution_packet_ready",
            "approved_remote_preflight",
            "gate3_remote_training",
        ]
    if category in {"evaluation", "acceptance"}:
        return [
            "record_f02_6_decision",
            "source_freshness_ready_for_remote_preflight",
            "remote_formal_execution_packet_ready",
            "approved_remote_preflight",
            "gate3_remote_training_complete",
            "gate3_remote_audit_pullback",
        ]
    return [
        "gate3_remote_audit_pullback_complete",
        "regenerate_h01_h02_formal_artifacts",
        "h01_h02_formal_acceptance_audit",
    ]


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


def _stage(plan, stage_id):
    for stage in plan["ordered_stages"]:
        if stage["stage_id"] == stage_id:
            return stage
    raise AssertionError(f"missing stage {stage_id}")


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(copy.deepcopy(payload)), encoding="utf-8")
    return path
