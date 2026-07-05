import json
from importlib import import_module


def test_paper_readiness_keeps_methods_ready_but_blocks_formal_results(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 paper readiness builder: {exc}") from exc

    paths = _write_inputs(tmp_path, formal=False)
    manifest_path = tmp_path / "paper_readiness.json"
    markdown_path = tmp_path / "paper_readiness.md"
    rc = builder.main(
        [
            "--method-algorithms",
            str(paths["method_algorithms"]),
            "--system-diagram",
            str(paths["system_diagram"]),
            "--paper-tables",
            str(paths["paper_tables"]),
            "--claim-safety",
            str(paths["claim_safety"]),
            "--h02-formal-acceptance",
            str(paths["h02_acceptance"]),
            "--h01-manifest",
            str(paths["h01_manifest"]),
            "--f02-6-decision-record",
            str(paths["decision_record"]),
            "--remote-execution-packet",
            str(paths["remote_packet"]),
            "--status-report",
            str(paths["status_report"]),
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_paper_readiness"
    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert manifest["manuscript_ready"] is False
    assert manifest["local_training_allowed"] is False
    assert "gpu3070ti-relay" in manifest["remote_training_resource"]
    assert "h02_formal_acceptance_not_accepted" in manifest["global_blockers"]
    assert "missing_module2_rl_rs_checkpoint" in manifest["global_blockers"]
    assert "f02_6_pending" in manifest["global_blockers"]
    assert "formal_gate_status_report_blocked" in manifest["global_blockers"]
    assert manifest["input_status"]["status_report_status"] == "formal_gate_status_blocked"
    assert manifest["input_status"]["claim_safety_handoff_status"] == "blocked_until_f02_6_decision"
    assert manifest["input_status"]["claim_safety_transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["input_status"]["claim_safety_transition_gate_audit_issue_count"] == 0
    assert manifest["input_status"]["claim_safety_handoff_safety_issue_count"] == 0
    assert manifest["input_status"]["claim_safety_missing_artifacts_handoff_status"] == "blocked_until_f02_6_decision"
    assert manifest["input_status"]["claim_safety_missing_artifacts_next_action"] == "record_f02_6_decision"
    assert manifest["input_status"]["claim_safety_missing_artifacts_open_requirement_count"] == 5
    assert manifest["input_status"]["claim_safety_missing_artifacts_remote_training_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_missing_artifacts_formal_result_material_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_requirement_stage_present"] is True
    assert manifest["input_status"]["claim_safety_requirement_stage_mapped_count"] == 4
    assert manifest["input_status"]["claim_safety_requirement_stage_unmapped_count"] == 0
    assert manifest["input_status"]["claim_safety_requirement_stage_mismatched_count"] == 0
    assert manifest["input_status"]["claim_safety_requirement_stage_blocked_stage_count"] == 4
    assert manifest["input_status"]["claim_safety_remote_preflight_requirement_present"] is True
    assert manifest["input_status"]["claim_safety_remote_preflight_requirement_satisfied_count"] == 2
    assert manifest["input_status"]["claim_safety_remote_preflight_requirement_blocked_count"] == 2
    assert manifest["input_status"]["claim_safety_post_run_acceptance_requirement_present"] is True
    assert manifest["input_status"]["claim_safety_post_run_acceptance_requirement_satisfied_count"] == 0
    assert manifest["input_status"]["claim_safety_post_run_acceptance_requirement_blocked_count"] == 4
    assert manifest["input_status"]["claim_safety_h02_formal_acceptance_requirement_present"] is True
    assert manifest["input_status"]["claim_safety_h02_formal_acceptance_requirement_satisfied_count"] == 1
    assert manifest["input_status"]["claim_safety_h02_formal_acceptance_requirement_blocked_count"] == 3
    assert manifest["input_status"]["claim_safety_decision_intake_present"] is True
    assert manifest["input_status"]["claim_safety_decision_intake_status"] == "f02_6_decision_intake_pending_clean"
    assert manifest["input_status"]["claim_safety_decision_intake_record_status"] == "pending_human_decision"
    assert manifest["input_status"]["claim_safety_decision_intake_audit_issue_count"] == 0
    assert manifest["input_status"]["claim_safety_decision_intake_decision_owner_required"] == "Dr Sun"
    assert manifest["input_status"]["claim_safety_decision_intake_valid_decision_count"] == 2
    assert manifest["input_status"]["claim_safety_decision_intake_required_record_field_count"] == 3
    assert manifest["input_status"]["claim_safety_decision_intake_decision_note_required"] is True
    assert manifest["input_status"]["claim_safety_decision_intake_invalid_input_count"] == 2
    assert manifest["input_status"]["claim_safety_decision_intake_post_decision_non_authorization_count"] == 2
    assert manifest["input_status"]["claim_safety_decision_intake_post_decision_route_count"] == 2
    assert manifest["input_status"]["claim_safety_decision_intake_approved_route_next_lane"] == "source_fresh_regeneration"
    assert manifest["input_status"]["claim_safety_decision_intake_approved_route_allows_remote_training_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_rejected_route_requires_new_protocol_contract"] is True
    assert manifest["input_status"]["claim_safety_decision_intake_next_blocked_lane"] == "decision"
    assert manifest["input_status"]["claim_safety_decision_intake_remote_preflight_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_remote_training_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_formal_claim_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_impact_present"] is True
    assert manifest["input_status"]["claim_safety_decision_evidence_matrix_status"] == "ready_for_dr_sun_decision_not_authorization"
    assert manifest["input_status"]["claim_safety_decision_evidence_matrix_route_count"] == 2
    assert manifest["input_status"]["claim_safety_decision_evidence_matrix_required_evidence_count"] == 7
    assert manifest["input_status"]["claim_safety_decision_evidence_matrix_missing_required_evidence_count"] == 0
    assert manifest["input_status"]["claim_safety_decision_evidence_matrix_remote_training_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_record_is_not_training_authorization"] is True
    assert manifest["input_status"]["claim_safety_decision_record_is_not_paper_result_material"] is True
    assert manifest["input_status"]["claim_safety_decision_impact_remote_training_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_impact_formal_claim_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_impact_paper_result_material_allowed_now"] is False
    assert manifest["claim_safety_decision_intake_summary"]["status"] == "f02_6_decision_intake_pending_clean"
    assert manifest["claim_safety_decision_intake_summary"]["post_decision_route_count"] == 2
    assert manifest["claim_safety_decision_intake_summary"]["approved_route_next_lane"] == "source_fresh_regeneration"
    assert manifest["claim_safety_decision_intake_summary"]["approved_route_allows_remote_training_now"] is False
    assert manifest["claim_safety_decision_intake_summary"]["rejected_route_requires_new_protocol_contract"] is True
    assert manifest["claim_safety_decision_intake_summary"]["decision_impact_present"] is True
    assert manifest["claim_safety_decision_intake_summary"]["decision_record_is_not_training_authorization"] is True
    assert manifest["claim_safety_decision_intake_summary"]["decision_impact_remote_training_allowed_now"] is False
    assert manifest["claim_safety_f02_6_decision_evidence_matrix_summary"]["status"] == "ready_for_dr_sun_decision_not_authorization"
    assert manifest["claim_safety_f02_6_decision_evidence_matrix_summary"]["missing_required_evidence_count"] == 0
    assert manifest["claim_safety_f02_6_decision_evidence_matrix_summary"]["remote_training_allowed_now"] is False
    assert (
        manifest["input_status"]["claim_safety_handoff_decision_evidence_matrix_status"]
        == "ready_for_dr_sun_decision_not_authorization"
    )
    assert manifest["input_status"]["claim_safety_handoff_decision_evidence_matrix_missing_required_evidence_count"] == 0
    assert manifest["input_status"]["claim_safety_handoff_decision_evidence_matrix_remote_training_allowed_now"] is False
    assert (
        manifest["claim_safety_handoff_f02_6_decision_evidence_matrix_summary"]["status"]
        == "ready_for_dr_sun_decision_not_authorization"
    )
    assert manifest["claim_safety_handoff_f02_6_decision_evidence_matrix_summary"]["missing_required_evidence_count"] == 0
    assert manifest["claim_safety_handoff_f02_6_decision_evidence_matrix_summary"]["remote_training_allowed_now"] is False
    assert "claim_safety_f02_6_decision_intake_pending" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_present"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_matrix_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_missing_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_blocked_category_count"] == 4
    assert manifest["input_status"]["claim_safety_remaining_deliverables_gap_present"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_gap_total_missing_deliverables"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_gap_open_category_count"] == 4
    assert manifest["input_status"]["claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_present"] is True
    assert (
        manifest["input_status"][
            "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables"
        ]
        == 10
    )
    assert (
        manifest["input_status"]["claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_open_category_count"]
        == 4
    )
    assert "claim_safety_remaining_deliverables_acceptance_rows_missing" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_acceptance_categories_blocked" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_gap_rows_missing" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_gap_categories_blocked" in manifest["global_blockers"]
    assert (
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_rows_missing"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_categories_blocked"
        in manifest["global_blockers"]
    )
    assert manifest["input_status"]["claim_safety_remaining_deliverables_proof_command_plan_present"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_proof_command_plan_matrix_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_proof_command_plan_command_count"] == 20
    assert (
        manifest["claim_safety_remaining_deliverables_proof_command_plan"]["rows"][
            "training:train_final_model_zip"
        ]["proof_command_ids"]
        == ["train_final_model_zip_exists_nonempty", "train_final_model_zip_valid_zip"]
    )
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_summary_present"] is True
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_training_missing_count"] == 3
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_evaluation_missing_count"] == 2
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_acceptance_missing_count"] == 3
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_formal_acceptance_missing_count"] == 2
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_next_blocked_lane"] == "decision"
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_h02_paper_result_input_allowed"] is False
    assert manifest["claim_safety_remote_packet_safety_proof_deliverables_summary"][
        "missing_counts_by_formal_category"
    ] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert manifest["input_status"]["claim_safety_remote_packet_safety_command_index_present"] is True
    assert manifest["input_status"]["claim_safety_remote_packet_safety_command_index_row_count"] == 23
    assert manifest["input_status"]["claim_safety_remote_packet_safety_command_index_source_target_count"] == 23
    assert manifest["input_status"]["claim_safety_remote_packet_safety_command_index_missing_target_count"] == 0
    assert manifest["input_status"]["claim_safety_next_action_guard_present"] is True
    assert manifest["input_status"]["claim_safety_next_action_guard_status"] == "next_action_guard_passed"
    assert (
        manifest["input_status"]["claim_safety_next_action_guard_expected_next_action_id"]
        == "record_f02_6_decision"
    )
    assert manifest["input_status"]["claim_safety_next_action_guard_all_execution_disabled_now"] is True
    assert manifest["input_status"]["claim_safety_next_action_guard_execution_leak_count"] == 0
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_present"] is True
    assert (
        manifest["input_status"]["claim_safety_handoff_single_next_action_index_status"]
        == "awaiting_dr_sun_f02_6_decision"
    )
    assert (
        manifest["input_status"]["claim_safety_handoff_single_next_action_index_next_action_id"]
        == "record_f02_6_decision"
    )
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_decision_owner_required"] == "Dr Sun"
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_all_execution_disabled_now"] is True
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_missing_deliverable_count"] == 10
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_remote_training_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_formal_claim_allowed_now"] is False
    assert (
        manifest["input_status"]["claim_safety_handoff_single_next_action_index_paper_result_material_allowed_now"]
        is False
    )
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_present"] is True
    assert (
        manifest["input_status"]["claim_safety_next_required_formal_deliverables_status"]
        == "blocked_missing_formal_deliverables"
    )
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_total_missing"] == 10
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_blocked_category_count"] == 4
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_row_count"] == 10
    assert manifest["input_status"]["claim_safety_mainline_audit_present"] is True
    assert (
        manifest["input_status"]["claim_safety_mainline_audit_status"]
        == "mainline_formal_gate_state_consistent_blocked"
    )
    assert manifest["input_status"]["claim_safety_mainline_audit_issue_count"] == 0
    assert manifest["input_status"]["claim_safety_mainline_audit_proof_summary_issue_count"] == 0
    assert manifest["input_status"]["claim_safety_mainline_audit_proof_audit_input_safety_issue_count"] == 0
    assert (
        manifest["claim_safety_mainline_formal_gate_state_audit_summary"]["proof_summary_chain_status"]
        == "formal_gate_proof_summary_chain_consistent_blocked"
    )
    assert manifest["claim_safety_remote_packet_safety_claim_gate_command_index_summary"]["claim_gate_rows"][
        "formal_gate_proof_summary_chain_audit"
    ]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert manifest["claim_safety_remote_packet_safety_claim_gate_command_index_summary"]["claim_gate_rows"][
        "mainline_formal_gate_state_audit"
    ]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert (
        "build_module2_mainline_formal_gate_state_audit"
        in manifest["claim_safety_remote_packet_safety_claim_gate_command_index_summary"]["claim_gate_rows"][
            "mainline_formal_gate_state_audit"
        ]["command_template"]
    )
    assert manifest["claim_safety_remote_packet_safety_claim_gate_command_index_summary"]["claim_gate_rows"][
        "claim_safety"
    ]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert manifest["claim_safety_remote_packet_safety_claim_gate_command_index_summary"]["claim_gate_rows"][
        "paper_readiness"
    ]["required_before"] == "formal_claim_gate"
    assert manifest["claim_safety_requirement_stage_summary"]["requirements"]["training_remote_ppo_checkpoint"][
        "responsible_stage_id"
    ] == "gate3_remote_training"
    assert manifest["claim_safety_remote_requirement_summary"]["remote_preflight_requirement_summary"]["status_counts"] == {
        "blocked_missing_preflight": 2,
        "satisfied": 2,
    }
    assert manifest["claim_safety_h02_acceptance_requirement_summary"]["status_counts"] == {
        "satisfied": 1,
        "blocked_formal_acceptance": 3,
    }

    sections = {item["section_id"]: item for item in manifest["section_readiness"]}
    assert sections["method_algorithm"]["status"] == "ready_to_write"
    assert sections["system_figure"]["status"] == "ready_to_write"
    assert sections["no_warm_failure_claim"]["status"] == "ready_with_scope_limit"
    assert sections["formal_results"]["status"] == "blocked"
    assert sections["main_results_table"]["status"] == "blocked"
    assert "h02_formal_acceptance_not_accepted" in sections["formal_results"]["blockers"]
    assert "missing_remote_pullback_artifacts" in sections["main_results_table"]["blockers"]
    assert manifest["allowed_claim_ids"] == ["method_is_ha_star_analytic_operator", "no_warm_gate3_formal_failure"]
    assert "partial_methods_ready_results_blocked" in markdown
    assert "Claim Safety Handoff Summary" in markdown
    assert "claim_safety_handoff_status" in markdown
    assert "blocked_until_f02_6_decision" in markdown
    assert "claim_safety_transition_gate_status" in markdown
    assert "f02_6_transition_gate_audit_passed" in markdown
    assert "Claim Safety Missing-Artifacts Handoff Index" in markdown
    assert "claim_safety_missing_artifacts_handoff_status" in markdown
    assert "Claim Safety Requirement Stage Summary" in markdown
    assert "claim_safety_requirement_stage_blocked_stage_count" in markdown
    assert "Claim Safety Remote Requirement Matrices" in markdown
    assert "claim_safety_remote_preflight_requirement_blocked_count" in markdown
    assert "Claim Safety H02 Acceptance Requirement Matrix" in markdown
    assert "claim_safety_h02_formal_acceptance_requirement_blocked_count" in markdown
    assert "Claim Safety F02.6 Decision Intake" in markdown
    assert "claim_safety_decision_intake_status" in markdown
    assert "f02_6_decision_intake_pending_clean" in markdown
    assert "claim_safety_decision_intake_decision_owner_required" in markdown
    assert "claim_safety_decision_intake_decision_note_required" in markdown
    assert "claim_safety_decision_intake_approved_route_next_lane" in markdown
    assert "claim_safety_decision_intake_rejected_route_requires_new_protocol_contract" in markdown
    assert "Claim Safety Remaining Deliverables Acceptance Matrix" in markdown
    assert "claim_safety_remaining_deliverables_acceptance_matrix_row_count" in markdown
    assert "Claim Safety Formal Gate Gap Audit Remaining Deliverables Gap Summary" in markdown
    assert "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables" in markdown
    assert "Claim Safety Remaining Deliverables Proof Command Plan" in markdown
    assert "claim_safety_remaining_deliverables_proof_command_plan_command_count" in markdown
    assert "Claim Safety Remote-Safety Proof Deliverables Summary" in markdown
    assert "claim_safety_remote_packet_safety_proof_training_missing_count" in markdown
    assert "claim_safety_remote_packet_safety_proof_h02_paper_result_input_allowed" in markdown
    assert "Claim Safety Remote-Safety Claim-Gate Command Index" in markdown
    assert "claim_safety_remote_packet_safety_command_index_row_count" in markdown
    assert "Claim Safety Next-Action Guard" in markdown
    assert "claim_safety_next_action_guard_expected_next_action_id" in markdown
    assert "Claim Safety Handoff Single Next-Action Index" in markdown
    assert "Claim Safety Next Required Formal Deliverables" in markdown
    assert "claim_safety_next_required_formal_deliverables_total_missing" in markdown
    assert "Claim Safety Mainline Formal Gate State Audit" in markdown
    assert "claim_safety_mainline_audit_status" in markdown


def test_paper_readiness_accepts_synthetic_complete_evidence(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "paper_evidence_ready"
    assert manifest["manuscript_ready"] is True
    assert manifest["global_blockers"] == []
    assert manifest["input_status"]["claim_safety_handoff_status"] == "ready_for_manual_remote_execution_review"
    assert manifest["input_status"]["claim_safety_transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["input_status"]["claim_safety_missing_artifacts_handoff_status"] == "formal_gate_evidence_ready_for_h01_h02_claim_gates"
    assert manifest["input_status"]["claim_safety_missing_artifacts_open_requirement_count"] == 0
    assert manifest["input_status"]["claim_safety_requirement_stage_mapped_count"] == 4
    assert manifest["input_status"]["claim_safety_requirement_stage_blocked_stage_count"] == 0
    assert manifest["input_status"]["claim_safety_remote_preflight_requirement_satisfied_count"] == 4
    assert manifest["input_status"]["claim_safety_post_run_acceptance_requirement_satisfied_count"] == 4
    assert manifest["input_status"]["claim_safety_h02_formal_acceptance_requirement_satisfied_count"] == 4
    assert manifest["input_status"]["claim_safety_decision_intake_status"] == "f02_6_decision_intake_closed_clean"
    assert manifest["input_status"]["claim_safety_decision_intake_record_status"] == "approved"
    assert manifest["input_status"]["claim_safety_decision_intake_decision_owner_required"] == "Dr Sun"
    assert manifest["input_status"]["claim_safety_decision_intake_decision_note_required"] is True
    assert manifest["input_status"]["claim_safety_decision_intake_approved_route_next_lane"] == "source_fresh_regeneration"
    assert manifest["input_status"]["claim_safety_decision_intake_approved_route_allows_remote_training_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_rejected_route_requires_new_protocol_contract"] is True
    assert manifest["input_status"]["claim_safety_decision_intake_remote_training_allowed_now"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_matrix_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_missing_row_count"] == 0
    assert manifest["input_status"]["claim_safety_remaining_deliverables_proof_command_plan_matrix_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_proof_command_plan_command_count"] == 20
    assert (
        manifest["input_status"][
            "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables"
        ]
        == 0
    )
    assert (
        manifest["input_status"]["claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_open_category_count"]
        == 0
    )
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_summary_present"] is True
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_training_missing_count"] == 0
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_evaluation_missing_count"] == 0
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_acceptance_missing_count"] == 0
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_formal_acceptance_missing_count"] == 0
    assert manifest["input_status"]["claim_safety_remote_packet_safety_proof_h02_paper_result_input_allowed"] is True
    assert manifest["claim_safety_remote_packet_safety_status_report_proof_deliverables_summary"] == manifest[
        "claim_safety_remote_packet_safety_proof_deliverables_summary"
    ]
    assert manifest["input_status"]["claim_safety_remote_packet_safety_command_index_row_count"] == 23
    assert manifest["input_status"]["claim_safety_next_action_guard_status"] == "next_action_guard_passed"
    assert manifest["input_status"]["claim_safety_next_action_guard_expected_next_action_id"] is None
    assert manifest["input_status"]["claim_safety_next_action_guard_all_execution_disabled_now"] is False
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_status"] == "formal_deliverables_ready"
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_total_missing"] == 0
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_blocked_category_count"] == 0
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_row_count"] == 10
    assert manifest["input_status"]["claim_safety_mainline_audit_status"] == "mainline_formal_gate_state_consistent_ready"
    assert manifest["input_status"]["claim_safety_mainline_audit_issue_count"] == 0
    assert all(item["status"] != "blocked" for item in manifest["section_readiness"])
    assert "formal_performance_improvement" in manifest["conditional_claim_ids"]


def test_paper_readiness_directly_blocks_on_status_report_even_if_claim_safety_is_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)
    paths["status_report"] = _write_json(
        tmp_path / "status_report_blocked.json",
        _status_report_payload(ready=False),
    )

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert manifest["formal_results_ready"] is False
    assert "formal_gate_status_report_blocked" in manifest["global_blockers"]
    sections = {item["section_id"]: item for item in manifest["section_readiness"]}
    assert "formal_gate_status_report_blocked" in sections["formal_results"]["blockers"]


def test_paper_readiness_rejects_claim_safety_without_requirement_stage_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)
    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    claim_safety_payload.pop("status_report_requirement_stage_summary")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_missing_requirement_stage_summary" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_requirement_stage_present"] is False


def test_paper_readiness_rejects_claim_safety_without_remote_requirement_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)
    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    claim_safety_payload.pop("status_report_remote_requirement_summary")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_remote_preflight_requirement_summary_missing" in manifest["global_blockers"]
    assert "claim_safety_post_run_acceptance_requirement_summary_missing" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_remote_preflight_requirement_present"] is False


def test_paper_readiness_rejects_claim_safety_without_h02_acceptance_requirement_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)
    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    claim_safety_payload.pop("status_report_h02_acceptance_requirement_summary")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_missing_h02_acceptance_requirement_summary" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_h02_formal_acceptance_requirement_present"] is False


def test_paper_readiness_rejects_claim_safety_without_clean_decision_intake_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    claim_safety_payload["status_report_decision_intake_summary"]["status"] = "f02_6_decision_intake_failed"
    claim_safety_payload["status_report_decision_intake_summary"]["audit_issue_count"] = 1
    claim_safety_payload["status_report_decision_intake_summary"]["record_decider"] = "Assistant"
    claim_safety_payload["status_report_decision_intake_summary"]["decision_owner_required"] = "Assistant"
    claim_safety_payload["status_report_decision_intake_summary"]["valid_decisions"] = [
        "approve_obstacle_summary_warm_start"
    ]
    claim_safety_payload["status_report_decision_intake_summary"]["required_record_fields"] = ["decision", "decider"]
    claim_safety_payload["status_report_decision_intake_summary"]["decision_note_required"] = False
    claim_safety_payload["status_report_decision_intake_summary"]["invalid_input_count"] = 0
    claim_safety_payload["status_report_decision_intake_summary"]["post_decision_non_authorization_count"] = 0
    matrix = claim_safety_payload["status_report_decision_intake_summary"]["decision_evidence_matrix_summary"]
    matrix["missing_required_evidence_count"] = 1
    matrix["remote_training_allowed_now"] = True
    matrix["global_invalid_substitute_count"] = 0
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert manifest["formal_results_ready"] is False
    assert "claim_safety_f02_6_decision_intake_not_clean" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_audit_issues_open" in manifest["global_blockers"]
    assert "claim_safety_closed_f02_6_intake_decider_not_dr_sun" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_decision_owner_not_dr_sun" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_valid_decisions_incomplete" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_required_fields_incomplete" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_decision_note_not_required" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_invalid_inputs_missing" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_non_authorizations_missing" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_evidence_matrix_missing_required_evidence" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_evidence_matrix_allows_remote_training" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_evidence_matrix_invalid_substitutes_missing" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_decision_intake_status"] == "f02_6_decision_intake_failed"


def test_paper_readiness_rejects_claim_safety_handoff_decision_evidence_matrix_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    matrix = claim_safety_payload["handoff_f02_6_decision_evidence_matrix_summary"]
    matrix["missing_required_evidence_count"] = 1
    matrix["source_issue_count"] = 1
    matrix["remote_training_allowed_now"] = True
    matrix["global_invalid_substitute_count"] = 0
    matrix["invalid_substitute_counts_by_route"]["approve_obstacle_summary_warm_start"] = 0
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    blockers = set(manifest["global_blockers"])
    assert "claim_safety_handoff_f02_6_decision_evidence_matrix_missing_required_evidence" in blockers
    assert "claim_safety_handoff_f02_6_decision_evidence_matrix_source_issues_open" in blockers
    assert "claim_safety_handoff_f02_6_decision_evidence_matrix_allows_remote_training" in blockers
    assert "claim_safety_handoff_f02_6_decision_evidence_matrix_invalid_substitutes_missing" in blockers
    assert (
        "claim_safety_handoff_f02_6_decision_evidence_matrix_approve_obstacle_summary_warm_start_invalid_substitutes_missing"
        in blockers
    )
    assert "claim_safety_handoff_f02_6_decision_evidence_matrix_claim_safety_mismatch" in blockers
    assert manifest["input_status"]["claim_safety_handoff_decision_evidence_matrix_missing_required_evidence_count"] == 1


def test_paper_readiness_rejects_claim_safety_decision_intake_route_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    intake = claim_safety_payload["status_report_decision_intake_summary"]
    intake["post_decision_route_count"] = 1
    intake["post_decision_route_decisions"] = ["approve_obstacle_summary_warm_start"]
    intake["approved_route_next_lane"] = "remote_training"
    intake["approved_route_allows_remote_training_now"] = True
    intake["rejected_route_next_lane"] = "remote_training"
    intake["rejected_route_requires_new_protocol_contract"] = False
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert manifest["formal_results_ready"] is False
    assert "claim_safety_f02_6_decision_intake_route_decisions_incomplete" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_approved_route_next_lane_invalid" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_approved_route_allows_remote_training" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_rejected_route_next_lane_invalid" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_intake_rejected_route_missing_protocol_contract" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_decision_intake_approved_route_next_lane"] == "remote_training"


def test_paper_readiness_rejects_claim_safety_decision_intake_impact_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    intake = claim_safety_payload["status_report_decision_intake_summary"]
    intake["decision_impact_present"] = False
    intake["decision_record_is_not_training_authorization"] = False
    intake["decision_record_is_not_paper_result_material"] = False
    intake["decision_impact_remote_training_allowed_now"] = True
    intake["decision_impact_formal_claim_allowed_now"] = True
    intake["decision_impact_paper_result_material_allowed_now"] = True
    intake["decision_impact_formal_training_still_requires"] = []
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert manifest["formal_results_ready"] is False
    assert "claim_safety_f02_6_decision_intake_impact_missing" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_record_may_authorize_training" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_record_may_be_paper_result_material" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_impact_allows_remote_training" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_impact_allows_formal_claim" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_impact_allows_paper_result_material" in manifest["global_blockers"]
    assert "claim_safety_f02_6_decision_impact_missing_required_approved_remote_preflight" in manifest["global_blockers"]


def test_paper_readiness_rejects_claim_safety_without_remaining_deliverables_acceptance_matrix(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_remaining_deliverables_acceptance_summary"]
    summary["rows"]["training:train_final_model_zip"]["acceptance_predicate_count"] = 0
    summary["rows"].pop("formal_acceptance:h02_formal_output_acceptance")
    summary["matrix_row_count"] = 9
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_remaining_deliverables_acceptance_matrix_count_mismatch" in manifest["global_blockers"]
    assert (
        "claim_safety_remaining_deliverables_acceptance_training_train_final_model_zip_missing_predicates"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_remaining_deliverables_acceptance_missing_formal_acceptance_h02_formal_output_acceptance"
        in manifest["global_blockers"]
    )


def test_paper_readiness_rejects_claim_safety_without_remaining_deliverables_gap_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_remaining_deliverables_gap_summary"]
    summary["total_missing_deliverables"] = 1
    summary["open_category_count"] = 1
    summary["category_order"] = ["training", "evaluation"]
    summary["categories"]["training"]["missing_count"] = 1
    summary["categories"]["training"]["missing_artifact_matrix_ids"] = []
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_remaining_deliverables_gap_category_order_mismatch" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_gap_rows_missing" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_gap_categories_blocked" in manifest["global_blockers"]
    assert (
        "claim_safety_remaining_deliverables_gap_training_missing_artifact_count_mismatch"
        in manifest["global_blockers"]
    )
    assert manifest["claim_safety_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 1


def test_paper_readiness_rejects_claim_safety_without_formal_gate_gap_audit_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_formal_gate_gap_audit_remaining_deliverables_gap_summary"]
    summary["total_missing_deliverables"] = 1
    summary["open_category_count"] = 1
    summary["category_order"] = ["training", "evaluation"]
    summary["categories"]["training"]["missing_count"] = 1
    summary["categories"]["training"]["missing_artifact_matrix_ids"] = []
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert (
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_category_order_mismatch"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_rows_missing"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_categories_blocked"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_training_missing_artifact_count_mismatch"
        in manifest["global_blockers"]
    )
    assert (
        manifest["claim_safety_formal_gate_gap_audit_remaining_deliverables_gap_summary"][
            "total_missing_deliverables"
        ]
        == 1
    )


def test_paper_readiness_rejects_claim_safety_remaining_deliverables_proof_command_plan_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    plan = claim_safety_payload["status_report_remaining_deliverables_proof_command_plan"]
    plan["execution_boundary"] = "run_commands_now"
    plan["not_paper_result_material"] = False
    plan["runs_training"] = True
    plan["runs_remote_preflight"] = True
    plan["total_matrix_rows"] = 9
    plan["total_proof_command_count"] = 19
    plan["rows"]["training:train_final_model_zip"]["proof_command_count"] = 1
    plan["rows"].pop("formal_acceptance:h02_formal_output_acceptance")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert (
        "claim_safety_remaining_deliverables_proof_command_plan_wrong_execution_boundary"
        in manifest["global_blockers"]
    )
    assert "claim_safety_remaining_deliverables_proof_command_plan_result_material" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_proof_command_plan_runs_training" in manifest["global_blockers"]
    assert (
        "claim_safety_remaining_deliverables_proof_command_plan_runs_remote_preflight"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_remaining_deliverables_proof_command_plan_row_count_mismatch"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_remaining_deliverables_proof_command_plan_command_count_mismatch"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_remaining_deliverables_proof_command_plan_training_train_final_model_zip_command_count_mismatch"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_remaining_deliverables_proof_command_plan_missing_formal_acceptance_h02_formal_output_acceptance"
        in manifest["global_blockers"]
    )


def test_paper_readiness_rejects_claim_safety_remote_safety_command_index_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_remote_packet_safety_claim_gate_command_index_summary"]
    summary["missing_target_ids"] = ["paper_readiness"]
    summary["unknown_manual_count"] = 1
    summary["forbidden_command_count"] = 1
    summary["claim_gate_rows"]["claim_safety"]["stage_id"] = "regenerate_preflight_gate_artifacts"
    summary["claim_gate_rows"]["claim_safety"]["command_kind"] = "unknown_manual"
    summary["claim_gate_rows"].pop("paper_readiness")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_remote_packet_safety_command_index_missing_targets" in manifest["global_blockers"]
    assert "claim_safety_remote_packet_safety_command_index_unknown_manual_rows" in manifest["global_blockers"]
    assert "claim_safety_remote_packet_safety_command_index_forbidden_commands" in manifest["global_blockers"]
    assert "claim_safety_remote_packet_safety_command_index_claim_safety_wrong_stage" in manifest["global_blockers"]
    assert "claim_safety_remote_packet_safety_command_index_claim_safety_manual_command" in manifest["global_blockers"]
    assert "claim_safety_remote_packet_safety_command_index_missing_paper_readiness" in manifest["global_blockers"]


def test_paper_readiness_rejects_claim_safety_next_action_guard_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_next_action_guard_summary"]
    summary["status"] = "next_action_guard_failed"
    summary["violation_count"] = 1
    summary["pending_f02_6_decision"] = True
    summary["next_blocked_lane_id"] = "remote_training"
    summary["expected_next_action_id"] = "run_remote_training"
    summary["handoff_next_action_id"] = "run_remote_training"
    summary["handoff_next_action_requires_dr_sun"] = False
    summary["missing_artifacts_next_action_id"] = "run_remote_training"
    summary["decision_intake_next_blocked_lane"] = "remote_training"
    summary["all_execution_disabled_now"] = False
    summary["execution_leak_count"] = 1
    summary["remote_execution_allowed_count"] = 1
    summary["remote_stage_allowed_count"] = 1
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_next_action_guard_not_passed" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_violations_open" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_lane_not_decision" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_next_action_not_decision" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_handoff_action_not_decision" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_missing_artifacts_action_not_decision" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_intake_lane_not_decision" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_handoff_not_gated_by_dr_sun" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_execution_not_disabled" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_execution_leaks_open" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_remote_execution_allowed" in manifest["global_blockers"]
    assert "claim_safety_next_action_guard_remote_stage_allowed" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_next_action_guard_expected_next_action_id"] == "run_remote_training"


def test_paper_readiness_rejects_claim_safety_handoff_single_next_action_index_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["handoff_single_next_action_index_summary"]
    summary["status"] = "awaiting_dr_sun_f02_6_decision"
    summary["index_id"] = "wrong_index"
    summary["single_current_human_entry"] = False
    summary["next_action_id"] = "run_remote_training"
    summary["decision_owner_required"] = "Assistant"
    summary["valid_decisions"] = ["approve_obstacle_summary_warm_start"]
    summary["required_record_fields"] = ["decision"]
    summary["current_allowed_action_ids"] = ["run_remote_training"]
    summary["current_blocked_action_ids"] = ["formal_claim"]
    summary["post_decision_routes_are_current_authorization"] = True
    summary["all_execution_disabled_now"] = False
    summary["record_command_template_count"] = 1
    summary["local_training_allowed_now"] = True
    summary["remote_preflight_allowed_now"] = True
    summary["remote_training_allowed_now"] = True
    summary["formal_claim_allowed_now"] = True
    summary["paper_result_material_allowed_now"] = True
    summary["missing_deliverable_count"] = 0
    summary["open_category_count"] = 0
    summary["source_freshness_status"] = "source_freshness_stale"
    summary["source_freshness_blocking_regeneration_required"] = True
    summary["approved_route_next_lane"] = "run_remote_training"
    summary["rejected_route_next_lane"] = "continue_anyway"
    summary["after_approval_still_requires"] = []
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    blockers = set(manifest["global_blockers"])
    assert "claim_safety_handoff_single_next_action_index_id_invalid" in blockers
    assert "claim_safety_handoff_single_next_action_index_not_single_human_entry" in blockers
    assert "claim_safety_handoff_single_next_action_index_next_action_not_decision" in blockers
    assert "claim_safety_handoff_single_next_action_index_owner_not_dr_sun" in blockers
    assert "claim_safety_handoff_single_next_action_index_valid_decisions_incomplete" in blockers
    assert "claim_safety_handoff_single_next_action_index_required_fields_incomplete" in blockers
    assert "claim_safety_handoff_single_next_action_index_allowed_actions_not_decision_only" in blockers
    assert "claim_safety_handoff_single_next_action_index_missing_block_remote_preflight" in blockers
    assert "claim_safety_handoff_single_next_action_index_post_decision_routes_authorize_now" in blockers
    assert "claim_safety_handoff_single_next_action_index_execution_not_disabled" in blockers
    assert "claim_safety_handoff_single_next_action_index_record_command_count_mismatch" in blockers
    assert "claim_safety_handoff_single_next_action_index_allows_local_training" in blockers
    assert "claim_safety_handoff_single_next_action_index_allows_remote_preflight" in blockers
    assert "claim_safety_handoff_single_next_action_index_allows_remote_training" in blockers
    assert "claim_safety_handoff_single_next_action_index_allows_formal_claim" in blockers
    assert "claim_safety_handoff_single_next_action_index_allows_paper_result_material" in blockers
    assert "claim_safety_handoff_single_next_action_index_zero_missing_deliverables_while_blocked" in blockers
    assert "claim_safety_handoff_single_next_action_index_zero_open_categories_while_blocked" in blockers
    assert "claim_safety_handoff_single_next_action_index_source_freshness_not_clean" in blockers
    assert "claim_safety_handoff_single_next_action_index_source_freshness_blocks" in blockers
    assert "claim_safety_handoff_single_next_action_index_approved_route_invalid" in blockers
    assert "claim_safety_handoff_single_next_action_index_rejected_route_invalid" in blockers
    assert "claim_safety_handoff_single_next_action_index_approval_skips_remote_preflight" in blockers
    assert manifest["input_status"]["claim_safety_handoff_single_next_action_index_next_action_id"] == "run_remote_training"


def test_paper_readiness_rejects_claim_safety_next_required_formal_deliverables_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_next_required_formal_deliverables"]
    summary["not_paper_result_material"] = False
    summary["runs_training"] = True
    summary["runs_remote_preflight"] = True
    summary["total_missing_deliverables"] = 1
    summary["blocked_category_count"] = 1
    summary["blocked_categories"] = ["training"]
    summary["category_order"] = ["training", "evaluation"]
    summary["rows"]["training:train_final_model_zip"]["proof_command_ids"] = []
    summary["rows"]["training:train_final_model_zip"]["invalid_substitute_count"] = 0
    summary["rows"].pop("formal_acceptance:h02_formal_output_acceptance")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_next_required_formal_deliverables_marked_as_paper_result" in manifest["global_blockers"]
    assert "claim_safety_next_required_formal_deliverables_runs_training" in manifest["global_blockers"]
    assert "claim_safety_next_required_formal_deliverables_runs_remote_preflight" in manifest["global_blockers"]
    assert "claim_safety_next_required_formal_deliverables_category_order_mismatch" in manifest["global_blockers"]
    assert "claim_safety_next_required_formal_deliverables_row_count_mismatch" in manifest["global_blockers"]
    assert (
        "claim_safety_next_required_formal_deliverables_missing_formal_acceptance_h02_formal_output_acceptance"
        in manifest["global_blockers"]
    )
    assert "claim_safety_next_required_formal_deliverables_missing_while_claim_ready" in manifest["global_blockers"]
    assert (
        "claim_safety_next_required_formal_deliverables_categories_blocked_while_claim_ready"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_next_required_formal_deliverables_training_train_final_model_zip_missing_proof_commands"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_next_required_formal_deliverables_training_train_final_model_zip_missing_invalid_substitutes"
        in manifest["global_blockers"]
    )
    assert manifest["input_status"]["claim_safety_next_required_formal_deliverables_row_count"] == 9


def test_paper_readiness_rejects_claim_safety_mainline_audit_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    summary = claim_safety_payload["status_report_mainline_formal_gate_state_audit_summary"]
    summary["status"] = "mainline_formal_gate_state_audit_failed"
    summary["not_paper_result_material"] = False
    summary["executes_commands"] = True
    summary["runs_training"] = True
    summary["runs_remote_preflight"] = True
    summary["local_training_allowed"] = True
    summary["formal_claim_allowed"] = True
    summary["audit_issue_count"] = 1
    summary["proof_summary_chain_audit_issue_count"] = 1
    summary["proof_summary_chain_proof_audit_input_safety_issue_count"] = 1
    summary["proof_summary_chain_proof_audit_blockers"] = ["proof_audit_input_safety_issues_open"]
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    blockers = set(manifest["global_blockers"])
    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_mainline_formal_gate_state_audit_failed" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_marked_as_paper_result" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_executes_commands" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_runs_training" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_runs_remote_preflight" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_allows_local_training" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_allows_formal_claim" in blockers
    assert "claim_safety_mainline_formal_gate_state_audit_issues_open" in blockers
    assert "claim_safety_mainline_proof_summary_issues_open" in blockers
    assert "claim_safety_mainline_proof_audit_input_safety_issues_open" in blockers
    assert "claim_safety_mainline_proof_audit_input_safety_blocker_open" in blockers
    assert manifest["input_status"]["claim_safety_mainline_audit_issue_count"] == 1


def test_paper_readiness_rejects_missing_claim_safety_remote_safety_proof_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    claim_safety_payload.pop("status_report_remote_packet_safety_proof_deliverables_summary")
    claim_safety_payload.pop("status_report_remote_packet_safety_status_report_proof_deliverables_summary")
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_missing_remote_packet_safety_proof_deliverables_summary" in manifest["global_blockers"]
    assert (
        "claim_safety_missing_remote_packet_safety_status_report_proof_deliverables_summary"
        in manifest["global_blockers"]
    )
    assert manifest["claim_safety_remote_packet_safety_proof_deliverables_summary"]["present"] is False


def test_paper_readiness_rejects_claim_safety_remote_safety_proof_summary_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_readiness")
    paths = _write_inputs(tmp_path, formal=True)

    claim_safety_payload = json.loads(paths["claim_safety"].read_text(encoding="utf-8"))
    proof = claim_safety_payload["status_report_remote_packet_safety_proof_deliverables_summary"]
    proof["missing_counts_by_formal_category"]["training"] = 1
    proof["missing_matrix_ids_by_formal_category"]["training"] = ["training:train_final_model_zip"]
    paths["claim_safety"].write_text(json.dumps(claim_safety_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        builder.PaperReadinessConfig(
            output_dir=tmp_path,
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            paper_tables_path=paths["paper_tables"],
            claim_safety_path=paths["claim_safety"],
            h02_formal_acceptance_path=paths["h02_acceptance"],
            h01_manifest_path=paths["h01_manifest"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
            status_report_path=paths["status_report"],
        )
    )

    assert manifest["status"] == "partial_methods_ready_results_blocked"
    assert "claim_safety_remote_packet_safety_proof_deliverables_summary_mismatch" in manifest["global_blockers"]
    assert (
        "claim_safety_remote_packet_safety_proof_deliverables_summary_drifted_from_gap"
        in manifest["global_blockers"]
    )
    assert (
        "claim_safety_remote_packet_safety_proof_allows_paper_results_with_missing_deliverables"
        in manifest["global_blockers"]
    )


def _write_inputs(tmp_path, *, formal):
    proof_summary = _claim_safety_remote_safety_proof_summary_payload(formal=formal)
    paths = {}
    paths["method_algorithms"] = _write_json(
        tmp_path / "method_algorithms.json",
        {"artifact_name": "module2_method_algorithms", "status": "code_anchored"},
    )
    paths["system_diagram"] = _write_json(
        tmp_path / "system_diagram.json",
        {"artifact_name": "module2_system_diagram", "status": "code_anchored_drawio"},
    )
    paths["paper_tables"] = _write_json(
        tmp_path / "paper_tables.json",
        {
            "artifact_name": "module2_paper_tables",
            "status": "formal_ready" if formal else "blocked_no_formal_h02_data",
            "formal_claim_allowed": formal,
            "blockers": [] if formal else ["h02_formal_acceptance_not_accepted", "missing_remote_pullback_artifacts"],
        },
    )
    paths["claim_safety"] = _write_json(
        tmp_path / "claim_safety.json",
        {
            "artifact_name": "module2_claim_safety",
            "status": "formal_performance_claims_allowed" if formal else "blocked_formal_performance_claims",
            "formal_performance_claim_allowed": formal,
            "formal_performance_blockers": [] if formal else ["h02_formal_acceptance_not_accepted", "f02_6_pending"],
            "status_report_handoff_summary": {
                "present": True,
                "status": "ready_for_manual_remote_execution_review" if formal else "blocked_until_f02_6_decision",
                "transition_gate_status": "f02_6_transition_gate_audit_passed",
                "transition_gate_audit_issue_count": 0,
                "safety_issue_count": 0,
                "remote_training_allowed_now": formal,
                "remote_preflight_allowed_now": formal,
                "formal_claim_allowed_now": formal,
            },
            "status_report_missing_artifacts_handoff_summary": {
                "present": True,
                "status": "formal_gate_evidence_ready_for_h01_h02_claim_gates"
                if formal
                else "blocked_until_f02_6_decision",
                "next_action_id": None if formal else "record_f02_6_decision",
                "next_action_requires_dr_sun": not formal,
                "open_requirement_count": 0 if formal else 5,
                "local_training_allowed_now": False,
                "remote_training_allowed_now": formal,
                "formal_result_material_allowed_now": False,
            },
            "status_report_requirement_stage_summary": _claim_safety_requirement_stage_summary_payload(formal=formal),
            "status_report_remote_requirement_summary": _claim_safety_remote_requirement_summary_payload(formal=formal),
            "status_report_h02_acceptance_requirement_summary": _claim_safety_h02_acceptance_requirement_summary_payload(
                formal=formal
            ),
            "status_report_decision_intake_summary": {
                "present": True,
                "status": "f02_6_decision_intake_closed_clean" if formal else "f02_6_decision_intake_pending_clean",
                "audit_issue_count": 0,
                "record_status": "approved" if formal else "pending_human_decision",
                "record_decider": "Dr Sun" if formal else None,
                "next_blocked_lane": None if formal else "decision",
                "decision_owner_required": "Dr Sun",
                "valid_decisions": [
                    "approve_obstacle_summary_warm_start",
                    "reject_obstacle_summary_warm_start",
                ],
                "valid_decision_count": 2,
                "required_record_fields": ["decision", "decider", "decision_note"],
                "required_record_field_count": 3,
                "decision_note_required": True,
                "invalid_input_count": 2,
                "post_decision_non_authorization_count": 2,
                "post_decision_route_count": 2,
                "post_decision_route_decisions": [
                    "approve_obstacle_summary_warm_start",
                    "reject_obstacle_summary_warm_start",
                ],
                "approved_route_next_lane": "source_fresh_regeneration",
                "approved_route_allows_remote_training_now": False,
                "rejected_route_next_lane": "protocol_redesign",
                "rejected_route_requires_new_protocol_contract": True,
                "remote_preflight_allowed_now": formal,
                "remote_training_allowed_now": formal,
                "formal_claim_allowed_now": formal,
                "decision_impact_present": True,
                "decision_impact_not_paper_result_material": True,
                "decision_record_is_not_training_authorization": True,
                "decision_record_is_not_paper_result_material": True,
                "decision_impact_remote_preflight_allowed_now": False,
                "decision_impact_remote_training_allowed_now": False,
                "decision_impact_formal_claim_allowed_now": False,
                "decision_impact_paper_result_material_allowed_now": False,
                "decision_impact_formal_training_still_requires": [
                    "source_freshness_audit",
                    "post_f02_6_regeneration_plan",
                    "post_f02_6_plan_audit",
                    "remote_formal_execution_packet_ready",
                    "approved_remote_preflight",
                ],
                "decision_evidence_matrix_summary": {
                    "present": True,
                    "matrix_id": "module2_f02_6_decision_evidence_matrix",
                    "status": "ready_for_dr_sun_decision_not_authorization",
                    "route_count": 2,
                    "route_decisions": [
                        "approve_obstacle_summary_warm_start",
                        "reject_obstacle_summary_warm_start",
                    ],
                    "required_evidence_count": 7,
                    "satisfied_required_evidence_count": 7,
                    "missing_required_evidence_count": 0,
                    "global_invalid_substitute_count": 2,
                    "current_authorization_allowed_now": False,
                    "remote_preflight_allowed_now": False,
                    "remote_training_allowed_now": False,
                    "local_training_allowed_now": False,
                    "formal_claim_allowed_now": False,
                    "paper_result_material_allowed_now": False,
                },
            },
            "status_report_remaining_deliverables_acceptance_summary": _claim_safety_remaining_deliverables_acceptance_summary_payload(
                formal=formal
            ),
            "status_report_remaining_deliverables_gap_summary": _claim_safety_remaining_deliverables_gap_summary_payload(
                formal=formal
            ),
            "status_report_formal_gate_gap_audit_remaining_deliverables_gap_summary": _claim_safety_remaining_deliverables_gap_summary_payload(
                formal=formal
            ),
            "status_report_remaining_deliverables_proof_command_plan": _claim_safety_remaining_deliverables_proof_command_plan_payload(),
            "status_report_remote_packet_safety_proof_deliverables_summary": proof_summary,
            "status_report_remote_packet_safety_status_report_proof_deliverables_summary": json.loads(
                json.dumps(proof_summary)
            ),
            "status_report_remote_packet_safety_claim_gate_command_index_summary": _claim_safety_command_index_summary_payload(),
            "status_report_next_action_guard_summary": _claim_safety_next_action_guard_summary_payload(
                formal=formal
            ),
            "handoff_single_next_action_index_summary": _claim_safety_handoff_single_next_action_index_payload(
                formal=formal
            ),
            "status_report_next_required_formal_deliverables": _claim_safety_next_required_formal_deliverables_payload(
                formal=formal
            ),
            "status_report_mainline_formal_gate_state_audit_summary": (
                _claim_safety_mainline_formal_gate_state_audit_summary_payload(formal=formal)
            ),
            "allowed_claims": [
                {"claim_id": "method_is_ha_star_analytic_operator", "scope": "method_structure"},
                {"claim_id": "no_warm_gate3_formal_failure", "scope": "no_warm_only"},
            ],
            "conditional_claims": [
                {
                    "claim_id": "formal_performance_improvement",
                    "status": "ready" if formal else "blocked_until_formal_h02",
                }
            ],
        },
    )
    paths["h02_acceptance"] = _write_json(
        tmp_path / "h02_acceptance.json",
        {
            "artifact_name": "module2_h02_formal_acceptance",
            "status": "formal_output_accepted" if formal else "blocked_formal_output_acceptance",
            "formal_output_accepted": formal,
            "paper_result_input_allowed": formal,
            "blockers": [] if formal else ["h02_formal_acceptance_not_accepted", "missing_remote_pullback_artifacts"],
        },
    )
    paths["h01_manifest"] = _write_json(
        tmp_path / "h01.json",
        {
            "manifest_name": "module2_v1_evaluation",
            "status": "ready_for_formal_run" if formal else "blocked_pending_decisions",
            "blockers": [] if formal else ["missing_module2_rl_rs_checkpoint"],
        },
    )
    paths["decision_record"] = _write_json(
        tmp_path / "decision_record.json",
        {
            "record_name": "module2_f02_6_decision_record",
            "status": "approved" if formal else "pending_human_decision",
            "remote_training_allowed": formal,
            "blockers": [] if formal else ["requires_dr_sun_approval"],
        },
    )
    paths["remote_packet"] = _write_json(
        tmp_path / "remote_packet.json",
        {
            "packet_name": "module2_remote_formal_execution_packet",
            "status": "ready_for_gpu3070ti_remote_training" if formal else "blocked_until_f02_6_decision",
            "ready_to_run_remote_training": formal,
            "blockers": [] if formal else ["missing_module2_rl_rs_checkpoint"],
        },
    )
    paths["status_report"] = _write_json(
        tmp_path / "status_report.json",
        _status_report_payload(ready=formal),
    )
    return paths


def _status_report_payload(*, ready, invalid=False):
    return {
        "status": "formal_gate_status_ready_for_claim_audit" if ready else "formal_gate_status_blocked",
        "executes_commands": bool(invalid),
        "runs_training": bool(invalid),
        "runs_remote_preflight": bool(invalid),
        "local_training_allowed": bool(invalid),
        "formal_claim_allowed": bool(invalid),
        "input_safety_issue_count": 1 if invalid else 0,
        "permissions_now": {
            "local_training_allowed_now": bool(invalid),
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_h01_evaluation_allowed_now": bool(ready),
            "formal_h02_acceptance_allowed_now": bool(ready),
            "formal_claim_allowed_now": bool(ready),
        },
        "next_blocked_lane": None if ready else {"lane_id": "decision"},
    }


def _claim_safety_mainline_formal_gate_state_audit_summary_payload(*, formal):
    return {
        "present": True,
        "status": "mainline_formal_gate_state_consistent_ready"
        if formal
        else "mainline_formal_gate_state_consistent_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "audit_issue_count": 0,
        "proof_summary_chain_status": "formal_gate_proof_summary_chain_consistent_ready"
        if formal
        else "formal_gate_proof_summary_chain_consistent_blocked",
        "proof_summary_chain_audit_issue_count": 0,
        "proof_summary_chain_proof_audit_input_safety_issue_count": 0,
        "proof_summary_chain_proof_audit_blockers": [],
    }


def _claim_safety_requirement_stage_summary_payload(*, formal):
    requirements = {
        "training_remote_ppo_checkpoint": _claim_safety_requirement_stage_row(
            requirement_id="training_remote_ppo_checkpoint",
            responsible_stage_id="gate3_remote_training",
            formal=formal,
        ),
        "evaluation_gate3_episode_outputs": _claim_safety_requirement_stage_row(
            requirement_id="evaluation_gate3_episode_outputs",
            responsible_stage_id="gate3_remote_audit_pullback",
            formal=formal,
        ),
        "acceptance_remote_pullback_and_audit": _claim_safety_requirement_stage_row(
            requirement_id="acceptance_remote_pullback_and_audit",
            responsible_stage_id="gate3_remote_audit_pullback",
            formal=formal,
        ),
        "h01_h02_formal_evaluation_acceptance": _claim_safety_requirement_stage_row(
            requirement_id="h01_h02_formal_evaluation_acceptance",
            responsible_stage_id="regenerate_h01_h02_formal_artifacts",
            formal=formal,
        ),
    }
    return {
        "present": True,
        "mapped_requirement_count": len(requirements),
        "unmapped_requirement_count": 0,
        "mismatched_requirement_count": 0,
        "blocked_stage_count": 0 if formal else len(requirements),
        "requirements": requirements,
    }


def _claim_safety_requirement_stage_row(*, requirement_id, responsible_stage_id, formal):
    return {
        "requirement_id": requirement_id,
        "present": True,
        "status": "satisfied" if formal else "blocked_missing_outputs",
        "responsible_stage_id": responsible_stage_id,
        "responsible_stage_status": "ready" if formal else "blocked",
        "responsible_stage_allowed_now": formal,
        "mapping_present": True,
        "mapping_matches_expected": True,
    }


def _claim_safety_remote_requirement_summary_payload(*, formal):
    return {
        "remote_preflight_requirement_summary": _claim_safety_remote_requirement_matrix_payload(
            requirements={
                "f02_6_decision_closed_for_preflight": _claim_safety_remote_requirement_row(
                    requirement_id="f02_6_decision_closed_for_preflight",
                    status="satisfied" if formal else "blocked_missing_preflight",
                    complete=formal,
                    execution_allowed_now=formal,
                ),
                "approved_remote_preflight_manifest": _claim_safety_remote_requirement_row(
                    requirement_id="approved_remote_preflight_manifest",
                    status="satisfied" if formal else "blocked_missing_preflight",
                    complete=formal,
                    execution_allowed_now=formal,
                ),
                "remote_preflight_protocol_contract": _claim_safety_remote_requirement_row(
                    requirement_id="remote_preflight_protocol_contract",
                    status="satisfied",
                    complete=True,
                    execution_allowed_now=formal,
                ),
                "remote_preflight_command_packetized": _claim_safety_remote_requirement_row(
                    requirement_id="remote_preflight_command_packetized",
                    status="satisfied",
                    complete=True,
                    execution_allowed_now=formal,
                ),
            },
            status_counts={"satisfied": 4} if formal else {"blocked_missing_preflight": 2, "satisfied": 2},
        ),
        "post_run_acceptance_requirement_summary": _claim_safety_remote_requirement_matrix_payload(
            requirements={
                "pullback_expected_artifacts_complete": _claim_safety_remote_requirement_row(
                    requirement_id="pullback_expected_artifacts_complete",
                    status="satisfied" if formal else "blocked_until_remote_audit",
                    complete=formal,
                    execution_allowed_now=False,
                    remote_training_ready_now=formal,
                ),
                "checkpoint_hash_manifest_recorded": _claim_safety_remote_requirement_row(
                    requirement_id="checkpoint_hash_manifest_recorded",
                    status="satisfied" if formal else "blocked_until_remote_audit",
                    complete=formal,
                    execution_allowed_now=False,
                    remote_training_ready_now=formal,
                ),
                "gate3_formal_audit_accepts_remote_run": _claim_safety_remote_requirement_row(
                    requirement_id="gate3_formal_audit_accepts_remote_run",
                    status="satisfied" if formal else "blocked_until_remote_audit",
                    complete=formal,
                    execution_allowed_now=False,
                    remote_training_ready_now=formal,
                ),
                "h01_h02_regenerated_from_audited_checkpoint": _claim_safety_remote_requirement_row(
                    requirement_id="h01_h02_regenerated_from_audited_checkpoint",
                    status="satisfied" if formal else "blocked_until_remote_audit",
                    complete=formal,
                    execution_allowed_now=False,
                    remote_training_ready_now=formal,
                ),
            },
            status_counts={"satisfied": 4} if formal else {"blocked_until_remote_audit": 4},
        ),
    }


def _claim_safety_remote_requirement_matrix_payload(*, requirements, status_counts):
    return {
        "present": True,
        "required_requirement_count": len(requirements),
        "present_requirement_count": len(requirements),
        "blocked_requirement_count": sum(1 for row in requirements.values() if row["status"] != "satisfied"),
        "status_counts": status_counts,
        "missing_requirement_ids": [],
        "requirements": requirements,
    }


def _claim_safety_h02_acceptance_requirement_summary_payload(*, formal):
    requirements = {
        "h01_schema_and_h02_output_schema_match": _claim_safety_h02_acceptance_requirement_row(
            requirement_id="h01_schema_and_h02_output_schema_match",
            status="satisfied",
            complete=True,
            paper_result_input_allowed_now=formal,
        ),
        "h02_formal_scope_and_scale_match_h01": _claim_safety_h02_acceptance_requirement_row(
            requirement_id="h02_formal_scope_and_scale_match_h01",
            status="satisfied" if formal else "blocked_formal_acceptance",
            complete=formal,
            paper_result_input_allowed_now=formal,
        ),
        "gate3_audit_and_pullback_acceptance": _claim_safety_h02_acceptance_requirement_row(
            requirement_id="gate3_audit_and_pullback_acceptance",
            status="satisfied" if formal else "blocked_formal_acceptance",
            complete=formal,
            paper_result_input_allowed_now=formal,
        ),
        "ppo_rows_and_checkpoint_hash_present": _claim_safety_h02_acceptance_requirement_row(
            requirement_id="ppo_rows_and_checkpoint_hash_present",
            status="satisfied" if formal else "blocked_formal_acceptance",
            complete=formal,
            paper_result_input_allowed_now=formal,
        ),
    }
    return {
        "present": True,
        "required_requirement_count": len(requirements),
        "present_requirement_count": len(requirements),
        "blocked_requirement_count": sum(1 for row in requirements.values() if row["status"] != "satisfied"),
        "status_counts": {"satisfied": 4} if formal else {"satisfied": 1, "blocked_formal_acceptance": 3},
        "missing_requirement_ids": [],
        "requirements": requirements,
    }


def _claim_safety_h02_acceptance_requirement_row(
    *,
    requirement_id,
    status,
    complete,
    paper_result_input_allowed_now,
):
    return {
        "requirement_id": requirement_id,
        "present": True,
        "status": status,
        "complete": complete,
        "paper_result_input_allowed_now": paper_result_input_allowed_now,
    }


def _claim_safety_remaining_deliverables_acceptance_summary_payload(*, formal):
    matrix_ids = [
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
    ]
    rows = {}
    for matrix_id in matrix_ids:
        category, artifact_id = matrix_id.split(":", 1)
        rows[matrix_id] = {
            "present": True,
            "category": category,
            "artifact_id": artifact_id,
            "missing": not formal,
            "responsible_stage_id": "gate3_remote_training"
            if category == "training"
            else "regenerate_h01_h02_formal_artifacts"
            if category == "formal_acceptance"
            else "gate3_remote_audit_pullback",
            "responsible_stage_allowed_now": formal,
            "acceptance_predicate_count": 1,
            "invalid_substitute_count": 1,
        }
    return {
        "present": True,
        "status": "formal_gate_deliverables_ready_for_claim_audit" if formal else "formal_gate_deliverables_blocked",
        "missing_deliverable_count": 0 if formal else len(matrix_ids),
        "matrix_row_count": len(matrix_ids),
        "expected_matrix_row_count": len(matrix_ids),
        "missing_row_count": 0 if formal else len(matrix_ids),
        "blocked_category_count": 0 if formal else 4,
        "missing_expected_matrix_ids": [],
        "rows": rows,
    }


def _claim_safety_remaining_deliverables_gap_summary_payload(*, formal):
    category_artifacts = {
        "training": [
            "training:train_final_model_zip",
            "training:train_summary_json",
            "training:train_training_manifest_json",
        ],
        "evaluation": [
            "evaluation:eval_gate3_eval_episodes_csv",
            "evaluation:eval_gate3_summary_json",
        ],
        "acceptance": [
            "acceptance:gate3_trial_manifest_json",
            "acceptance:gate3_formal_audit_json",
            "acceptance:pulled_back_checkpoint_hash_record",
        ],
        "formal_acceptance": [
            "formal_acceptance:h01_ready_for_formal_run",
            "formal_acceptance:h02_formal_output_acceptance",
        ],
    }
    categories = {}
    for category, matrix_ids in category_artifacts.items():
        categories[category] = {
            "present": True,
            "missing_count": 0 if formal else len(matrix_ids),
            "responsible_stage_id": "gate3_remote_training"
            if category == "training"
            else "regenerate_h01_h02_formal_artifacts"
            if category == "formal_acceptance"
            else "gate3_remote_audit_pullback",
            "responsible_stage_allowed_now": formal,
            "missing_artifact_matrix_ids": [] if formal else matrix_ids,
        }
    return {
        "present": True,
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "total_missing_deliverables": 0 if formal else sum(len(ids) for ids in category_artifacts.values()),
        "open_category_count": 0 if formal else len(category_artifacts),
        "category_order": list(category_artifacts),
        "categories": categories,
    }


def _claim_safety_remaining_deliverables_proof_command_plan_payload():
    rows = {
        "training:train_final_model_zip": [
            "train_final_model_zip_exists_nonempty",
            "train_final_model_zip_valid_zip",
        ],
        "training:train_summary_json": [
            "train_summary_json_exists_nonempty",
            "train_summary_json_formal_warm_start_metadata",
        ],
        "training:train_training_manifest_json": [
            "train_training_manifest_json_exists_nonempty",
            "train_training_manifest_json_provenance",
        ],
        "evaluation:eval_gate3_eval_episodes_csv": [
            "eval_gate3_eval_episodes_csv_exists_nonempty",
            "eval_gate3_eval_episodes_csv_schema",
        ],
        "evaluation:eval_gate3_summary_json": [
            "eval_gate3_summary_json_exists_nonempty",
            "eval_gate3_summary_json_formal_scope",
        ],
        "acceptance:gate3_trial_manifest_json": [
            "gate3_trial_manifest_json_exists_nonempty",
            "gate3_trial_manifest_json_formal_warm_start_scope",
        ],
        "acceptance:gate3_formal_audit_json": [
            "gate3_formal_audit_json_exists_nonempty",
            "gate3_formal_audit_json_accepts_formal_scope",
        ],
        "acceptance:pulled_back_checkpoint_hash_record": [
            "pulled_back_checkpoint_hash_record_exists_nonempty",
            "pulled_back_checkpoint_hash_record_matches_model",
        ],
        "formal_acceptance:h01_ready_for_formal_run": [
            "h01_ready_for_formal_run_exists_nonempty",
            "h01_ready_for_formal_run_status",
        ],
        "formal_acceptance:h02_formal_output_acceptance": [
            "h02_formal_output_acceptance_exists_nonempty",
            "h02_formal_output_acceptance_status",
        ],
    }
    return {
        "present": True,
        "plan_id": "module2_formal_gate_local_read_only_proof_commands",
        "execution_boundary": "local_read_only_after_formal_remote_pullback",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_matrix_rows": len(rows),
        "total_proof_command_count": sum(len(command_ids) for command_ids in rows.values()),
        "rows": {
            matrix_id: {
                "present": True,
                "proof_command_count": len(command_ids),
                "proof_command_ids": command_ids,
            }
            for matrix_id, command_ids in rows.items()
        },
    }


def _claim_safety_remote_safety_proof_summary_payload(*, formal):
    gap = _claim_safety_remaining_deliverables_gap_summary_payload(formal=formal)
    return {
        "present": True,
        "missing_counts_by_formal_category": {
            category: payload["missing_count"]
            for category, payload in gap["categories"].items()
        },
        "missing_matrix_ids_by_formal_category": {
            category: list(payload["missing_artifact_matrix_ids"])
            for category, payload in gap["categories"].items()
        },
        "next_blocked_lane": None if formal else "decision",
        "h01_status": "ready_for_formal_run" if formal else "blocked_pending_decisions",
        "h02_status": "formal_output_accepted" if formal else "blocked_formal_output_acceptance",
        "h02_formal_output_accepted": bool(formal),
        "h02_paper_result_input_allowed": bool(formal),
    }


def _claim_safety_next_action_guard_summary_payload(*, formal):
    return {
        "present": True,
        "status": "next_action_guard_passed",
        "pending_f02_6_decision": not formal,
        "next_blocked_lane_id": None if formal else "decision",
        "expected_next_action_id": None if formal else "record_f02_6_decision",
        "handoff_next_action_id": None if formal else "record_f02_6_decision",
        "handoff_next_action_requires_dr_sun": not formal,
        "missing_artifacts_next_action_id": None if formal else "record_f02_6_decision",
        "decision_intake_next_blocked_lane": None if formal else "decision",
        "all_execution_disabled_now": not formal,
        "execution_leak_count": 0,
        "remote_execution_allowed_count": 0,
        "remote_stage_allowed_count": 0,
        "violation_count": 0,
        "execution_leak_surface_ids": [],
    }


def _claim_safety_handoff_single_next_action_index_payload(*, formal):
    return {
        "present": True,
        "index_id": "module2_formal_gate_single_next_action_index",
        "status": "f02_6_decision_recorded" if formal else "awaiting_dr_sun_f02_6_decision",
        "single_current_human_entry": not formal,
        "next_action_id": None if formal else "record_f02_6_decision",
        "decision_owner_required": "Dr Sun",
        "valid_decisions": [
            "approve_obstacle_summary_warm_start",
            "reject_obstacle_summary_warm_start",
        ],
        "required_record_fields": ["decision", "decider", "decision_note"],
        "current_allowed_action_ids": [] if formal else ["record_f02_6_decision"],
        "current_blocked_action_ids": []
        if formal
        else [
            "remote_preflight",
            "remote_training",
            "local_training",
            "formal_claim",
            "paper_result_material",
        ],
        "post_decision_routes_are_current_authorization": False,
        "all_execution_disabled_now": not formal,
        "record_command_template_count": 2,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False if not formal else True,
        "remote_training_allowed_now": False if not formal else True,
        "formal_claim_allowed_now": False if not formal else True,
        "paper_result_material_allowed_now": False,
        "missing_deliverable_count": 0 if formal else 10,
        "open_category_count": 0 if formal else 4,
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


def _claim_safety_next_required_formal_deliverables_payload(*, formal):
    acceptance = _claim_safety_remaining_deliverables_acceptance_summary_payload(formal=formal)
    gap = _claim_safety_remaining_deliverables_gap_summary_payload(formal=formal)
    rows = {}
    for matrix_id, row in acceptance["rows"].items():
        category, artifact_id = matrix_id.split(":", 1)
        rows[matrix_id] = {
            "present": True,
            "category": category,
            "artifact_id": artifact_id,
            "expected_path": f"expected/{matrix_id.replace(':', '/')}",
            "current_state": "missing" if row["missing"] else "present",
            "missing_reason": "required formal gate artifact" if row["missing"] else None,
            "responsible_stage_id": row["responsible_stage_id"],
            "responsible_stage_allowed_now": row["responsible_stage_allowed_now"],
            "responsible_stage_blocked_by": []
            if formal
            else ["f02_6_decision_not_approved", "remote_packet_not_ready"],
            "proof_command_ids": [f"{artifact_id}_exists", f"{artifact_id}_schema"],
            "invalid_substitute_count": row["invalid_substitute_count"],
        }
    return {
        "present": True,
        "status": "formal_deliverables_ready" if formal else "blocked_missing_formal_deliverables",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_missing_deliverables": gap["total_missing_deliverables"],
        "blocked_category_count": gap["open_category_count"],
        "blocked_categories": [] if formal else ["training", "evaluation", "acceptance", "formal_acceptance"],
        "category_order": ["training", "evaluation", "acceptance", "formal_acceptance"],
        "rows": rows,
    }


def _claim_safety_command_index_summary_payload():
    rows = {
        f"source_target_{index}": {
            "stage_id": "regenerate_preflight_gate_artifacts",
            "required_before": "approved_remote_preflight",
            "command_kind": "known_builder",
            "command_template": f"PYTHONPATH=2_experiment python -m builder_{index}",
        }
        for index in range(17)
    }
    rows["claim_safety"] = {
        "stage_id": "regenerate_claim_gate_artifacts",
        "required_before": "formal_claim_gate",
        "command_kind": "known_builder",
        "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety",
    }
    rows["formal_gate_proof_summary_chain_audit"] = {
        "stage_id": "regenerate_claim_gate_artifacts",
        "required_before": "formal_claim_gate",
        "command_kind": "known_builder",
        "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit",
    }
    rows["mainline_formal_gate_state_audit"] = {
        "stage_id": "regenerate_claim_gate_artifacts",
        "required_before": "formal_claim_gate",
        "command_kind": "known_builder",
        "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit",
    }
    rows["paper_readiness"] = {
        "stage_id": "regenerate_claim_gate_artifacts",
        "required_before": "formal_claim_gate",
        "command_kind": "known_builder",
        "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness",
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
        "claim_gate_rows": {
            "formal_gate_proof_summary_chain_audit": {
                "present": True,
                "stage_id": rows["formal_gate_proof_summary_chain_audit"]["stage_id"],
                "required_before": rows["formal_gate_proof_summary_chain_audit"]["required_before"],
                "command_kind": rows["formal_gate_proof_summary_chain_audit"]["command_kind"],
                "command_template": rows["formal_gate_proof_summary_chain_audit"]["command_template"],
            },
            "mainline_formal_gate_state_audit": {
                "present": True,
                "stage_id": rows["mainline_formal_gate_state_audit"]["stage_id"],
                "required_before": rows["mainline_formal_gate_state_audit"]["required_before"],
                "command_kind": rows["mainline_formal_gate_state_audit"]["command_kind"],
                "command_template": rows["mainline_formal_gate_state_audit"]["command_template"],
            },
            "claim_safety": {
                "present": True,
                "stage_id": rows["claim_safety"]["stage_id"],
                "required_before": rows["claim_safety"]["required_before"],
                "command_kind": rows["claim_safety"]["command_kind"],
                "command_template": rows["claim_safety"]["command_template"],
            },
            "paper_readiness": {
                "present": True,
                "stage_id": rows["paper_readiness"]["stage_id"],
                "required_before": rows["paper_readiness"]["required_before"],
                "command_kind": rows["paper_readiness"]["command_kind"],
                "command_template": rows["paper_readiness"]["command_template"],
            },
        },
    }


def _claim_safety_remote_requirement_row(
    *,
    requirement_id,
    status,
    complete,
    execution_allowed_now,
    remote_training_ready_now=None,
):
    return {
        "requirement_id": requirement_id,
        "present": True,
        "status": status,
        "complete": complete,
        "execution_allowed_now": execution_allowed_now,
        "remote_training_ready_now": remote_training_ready_now,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
