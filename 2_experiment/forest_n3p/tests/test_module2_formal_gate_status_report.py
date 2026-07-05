import json
from importlib import import_module


def test_formal_gate_status_report_blocks_pending_chain(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate status report builder: {exc}") from exc

    manifest = builder.build_manifest(_config(tmp_path, complete=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_status_report"
    assert manifest["status"] == "formal_gate_status_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["permissions_now"]["local_training_allowed_now"] is False
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is False
    assert manifest["inputs"]["source_freshness_audit"].endswith("source_freshness.json")
    assert manifest["current_state"]["decision_status"] == "pending_human_decision"
    assert manifest["current_state"]["decision_remote_preflight_allowed_now"] is False
    assert manifest["current_state"]["decision_remote_training_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_status"] == "f02_6_decision_intake_pending_clean"
    assert manifest["current_state"]["decision_intake_record_status"] == "pending_human_decision"
    assert manifest["current_state"]["decision_intake_next_blocked_lane"] == "decision"
    assert manifest["current_state"]["decision_intake_audit_issue_count"] == 0
    assert manifest["current_state"]["decision_intake_valid_decision_count"] == 2
    assert manifest["current_state"]["decision_intake_required_record_field_count"] == 3
    assert manifest["current_state"]["decision_intake_decision_note_required"] is True
    assert manifest["current_state"]["decision_intake_record_command_template_count"] == 2
    assert manifest["current_state"]["decision_intake_post_decision_non_authorization_count"] == 2
    assert manifest["current_state"]["decision_intake_post_decision_route_count"] == 2
    assert manifest["current_state"]["decision_intake_remote_preflight_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_remote_training_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_formal_claim_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_packet_authorization_status"] == "blocked_until_dr_sun_decision"
    assert manifest["current_state"]["decision_intake_packet_current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert manifest["current_state"]["decision_intake_packet_current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert manifest["current_state"]["decision_intake_packet_post_decision_routes_are_current_authorization"] is False
    assert manifest["current_state"]["decision_intake_packet_remote_preflight_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_packet_remote_training_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_packet_paper_result_material_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_next_request_status"] == "awaiting_dr_sun_decision"
    assert manifest["current_state"]["decision_intake_next_request_current_allowed_action_ids"] == [
        "record_f02_6_decision"
    ]
    assert manifest["current_state"]["decision_intake_next_request_current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert manifest["current_state"]["decision_intake_next_request_post_decision_routes_are_current_authorization"] is False
    assert manifest["current_state"]["decision_intake_next_request_all_execution_disabled_now"] is True
    assert manifest["current_state"]["decision_intake_decision_impact_present"] is True
    assert manifest["current_state"]["decision_intake_decision_impact_current_blocker"] == "decision"
    assert manifest["current_state"]["decision_intake_decision_impact_missing_deliverable_count"] == 10
    assert manifest["current_state"]["decision_intake_decision_record_is_not_training_authorization"] is True
    assert manifest["current_state"]["decision_intake_decision_record_is_not_paper_result_material"] is True
    assert manifest["current_state"]["decision_intake_decision_impact_remote_preflight_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_decision_impact_remote_training_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_decision_impact_formal_claim_allowed_now"] is False
    assert manifest["current_state"]["decision_intake_decision_impact_paper_result_material_allowed_now"] is False
    assert manifest["current_state"]["missing_artifacts_handoff_index_status"] == "blocked_until_f02_6_decision"
    assert manifest["current_state"]["missing_artifacts_handoff_next_action"] == "record_f02_6_decision"
    assert manifest["current_state"]["missing_artifacts_handoff_open_requirement_count"] == 5
    assert manifest["current_state"]["missing_artifacts_handoff_remote_training_allowed_now"] is False
    assert manifest["current_state"]["missing_artifacts_handoff_formal_result_material_allowed_now"] is False
    assert manifest["current_state"]["closure_open_item_count"] == 8
    assert manifest["current_state"]["closure_remote_preflight_allowed_now"] is False
    assert manifest["current_state"]["closure_remote_training_allowed_now"] is False
    assert manifest["current_state"]["closure_remote_audit_pullback_allowed_now"] is False
    assert manifest["current_state"]["remote_packet_sync_allowed_now"] is False
    assert manifest["current_state"]["remote_packet_preflight_allowed_now"] is False
    assert manifest["current_state"]["remote_packet_training_allowed_now"] is False
    assert manifest["current_state"]["remote_packet_audit_allowed_now"] is False
    assert manifest["current_state"]["handoff_bundle_status"] == "blocked_until_f02_6_decision"
    assert manifest["current_state"]["handoff_bundle_next_action"] == "record_f02_6_decision"
    assert manifest["current_state"]["handoff_bundle_safety_issue_count"] == 0
    assert manifest["current_state"]["handoff_bundle_remote_training_allowed_now"] is False
    assert manifest["current_state"]["handoff_requirement_stage_mapped_count"] == 4
    assert manifest["current_state"]["handoff_requirement_stage_unmapped_count"] == 0
    assert manifest["current_state"]["formal_gate_execution_veto_present"] is True
    assert manifest["current_state"]["formal_gate_execution_veto_all_rows_consistent"] is True
    assert manifest["current_state"]["formal_gate_execution_veto_remote_training_allowed_now"] is False
    assert manifest["current_state"]["formal_gate_execution_veto_formal_claim_allowed_now"] is False
    assert manifest["current_state"]["formal_gate_gap_audit_remaining_total_missing_deliverables"] == 10
    assert manifest["current_state"]["formal_gate_gap_audit_remaining_open_category_count"] == 4
    assert manifest["current_state"]["remote_packet_safety_proof_summary_present"] is True
    assert manifest["current_state"]["remote_packet_safety_proof_training_missing_count"] == 3
    assert manifest["current_state"]["remote_packet_safety_proof_evaluation_missing_count"] == 2
    assert manifest["current_state"]["remote_packet_safety_proof_acceptance_missing_count"] == 3
    assert manifest["current_state"]["remote_packet_safety_proof_formal_acceptance_missing_count"] == 2
    assert manifest["current_state"]["remote_packet_safety_proof_next_blocked_lane"] == "decision"
    assert manifest["current_state"]["remote_packet_safety_proof_h02_paper_result_input_allowed"] is False
    assert manifest["current_state"]["remote_packet_safety_status_report_proof_summary_present"] is True
    assert manifest["current_state"]["source_freshness_status"] == "source_freshness_risks_recorded_gate_still_blocked"
    assert manifest["current_state"]["source_freshness_regeneration_required"] is True
    assert manifest["current_state"]["source_freshness_non_self_changed_records"] == 19
    assert manifest["current_state"]["source_freshness_self_artifact_only_lag_records"] == 0
    assert manifest["current_state"]["remaining_deliverables_status"] == "formal_gate_deliverables_blocked"
    assert manifest["current_state"]["remaining_deliverables_missing_deliverable_count"] == 10
    assert manifest["current_state"]["remaining_deliverables_acceptance_matrix_count"] == 10
    assert manifest["current_state"]["remaining_deliverables_acceptance_missing_row_count"] == 10
    assert manifest["current_state"]["remaining_deliverables_acceptance_blocked_category_count"] == 4
    assert manifest["current_state"]["remaining_deliverables_unlock_chain_present"] is True
    assert manifest["current_state"]["remaining_deliverables_unlock_chain_row_count"] == 10
    assert manifest["current_state"]["remaining_deliverables_unlock_chain_blocked_row_count"] == 10
    assert manifest["current_state"]["remaining_deliverables_unlock_chain_rows_with_missing_required_blockers"] == 0
    assert manifest["current_state"]["remaining_deliverables_unlock_chain_rows_allowed_while_missing"] == 0
    assert manifest["current_state"]["remaining_deliverables_proof_plan_present"] is True
    assert manifest["current_state"]["remaining_deliverables_proof_plan_matrix_row_count"] == 10
    assert manifest["current_state"]["remaining_deliverables_proof_plan_command_count"] == 20
    assert manifest["current_state"]["formal_gate_proof_audit_status"] == "formal_gate_proof_audit_blocked"
    assert manifest["current_state"]["formal_gate_proof_audit_command_count"] == 20
    assert manifest["current_state"]["formal_gate_proof_audit_passed_count"] == 2
    assert manifest["current_state"]["formal_gate_proof_audit_failed_count"] == 2
    assert manifest["current_state"]["formal_gate_proof_audit_blocked_count"] == 16
    assert manifest["current_state"]["formal_gate_proof_audit_missing_artifact_count"] == 8
    assert manifest["current_state"]["formal_gate_proof_audit_failed_acceptance_artifact_count"] == 2
    assert manifest["current_state"]["formal_gate_proof_audit_training_missing_artifact_count"] == 3
    assert manifest["current_state"]["formal_gate_proof_audit_evaluation_missing_artifact_count"] == 2
    assert manifest["current_state"]["formal_gate_proof_audit_acceptance_missing_artifact_count"] == 3
    assert manifest["current_state"]["formal_gate_proof_audit_formal_acceptance_failed_artifact_count"] == 2
    assert manifest["missing_counts_by_category"]["training"] == 3
    assert len(manifest["training_artifacts_required"]) == 3
    assert len(manifest["evaluation_artifacts_required"]) == 2
    assert len(manifest["acceptance_artifacts_required"]) == 3
    assert manifest["next_blocked_lane"]["lane_id"] == "decision"
    steps = manifest["remote_execution_step_summary"]
    assert steps["sync_to_remote"]["allowed_now"] is False
    assert steps["sync_to_remote"]["runs_training"] is False
    assert steps["sync_to_remote"]["blocked_by"] == ["requires_dr_sun_approval"]
    assert steps["run_remote_training"]["allowed_now"] is False
    assert steps["run_remote_training"]["runs_training"] is True
    assert "remote_packet_not_ready" in steps["run_remote_training"]["blocked_by"]
    preflight_requirements = manifest["remote_preflight_requirement_summary"]
    assert preflight_requirements["present"] is True
    assert preflight_requirements["required_requirement_count"] == 4
    assert preflight_requirements["status_counts"] == {"blocked_missing_preflight": 2, "satisfied": 2}
    assert preflight_requirements["blocked_requirement_count"] == 2
    assert preflight_requirements["requirements"]["f02_6_decision_closed_for_preflight"]["status"] == "blocked_missing_preflight"
    assert preflight_requirements["requirements"]["remote_preflight_command_packetized"]["status"] == "satisfied"
    post_run_requirements = manifest["post_run_acceptance_requirement_summary"]
    assert post_run_requirements["present"] is True
    assert post_run_requirements["required_requirement_count"] == 4
    assert post_run_requirements["status_counts"] == {"blocked_until_remote_audit": 4}
    assert post_run_requirements["blocked_requirement_count"] == 4
    assert post_run_requirements["requirements"]["checkpoint_hash_manifest_recorded"]["status"] == "blocked_until_remote_audit"
    intake = manifest["f02_6_decision_intake_summary"]
    assert intake["present"] is True
    assert intake["status"] == "f02_6_decision_intake_pending_clean"
    assert intake["record_status"] == "pending_human_decision"
    assert intake["next_blocked_lane"] == "decision"
    assert intake["remote_preflight_allowed_now"] is False
    assert intake["remote_training_allowed_now"] is False
    assert intake["formal_claim_allowed_now"] is False
    assert intake["packet_authorization_status"] == "blocked_until_dr_sun_decision"
    assert intake["packet_current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert intake["packet_post_decision_routes_are_current_authorization"] is False
    assert intake["packet_remote_preflight_allowed_now"] is False
    assert intake["packet_remote_training_allowed_now"] is False
    assert intake["packet_paper_result_material_allowed_now"] is False
    assert intake["next_request_status"] == "awaiting_dr_sun_decision"
    assert intake["next_request_decision_owner_required"] == "Dr Sun"
    assert intake["next_request_current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert intake["next_request_all_execution_disabled_now"] is True
    assert intake["decision_owner_required"] == "Dr Sun"
    assert intake["valid_decision_count"] == 2
    assert set(intake["valid_decisions"]) == {
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    }
    assert intake["required_record_field_count"] == 3
    assert set(intake["required_record_fields"]) == {"decision", "decider", "decision_note"}
    assert intake["decision_note_required"] is True
    assert intake["invalid_input_count"] == 2
    assert intake["post_decision_non_authorization_count"] == 2
    assert intake["post_decision_route_count"] == 2
    assert set(intake["post_decision_route_decisions"]) == {
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    }
    assert intake["approved_route_next_lane"] == "source_fresh_regeneration"
    assert intake["approved_route_allows_remote_training_now"] is False
    assert intake["rejected_route_requires_new_protocol_contract"] is True
    assert intake["decision_impact_present"] is True
    assert intake["decision_impact_summary_id"] == "module2_f02_6_formal_gate_decision_impact"
    assert intake["decision_impact_not_paper_result_material"] is True
    assert intake["decision_impact_current_blocker"] == "decision"
    assert intake["decision_impact_current_record_status"] == "pending_human_decision"
    assert intake["decision_impact_missing_deliverable_count"] == 10
    assert intake["decision_impact_current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert set(intake["decision_impact_current_blocked_action_ids"]) == {
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    }
    assert set(intake["decision_impact_route_decisions"]) == {
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    }
    assert intake["decision_impact_approved_route_next_lane"] == "source_fresh_regeneration"
    assert intake["decision_impact_approved_route_allows_remote_training_now"] is False
    assert intake["decision_impact_rejected_route_next_lane"] == "protocol_redesign"
    assert intake["decision_impact_rejected_route_requires_new_protocol_contract"] is True
    assert intake["decision_record_is_not_training_authorization"] is True
    assert intake["decision_record_is_not_paper_result_material"] is True
    assert intake["decision_impact_local_training_allowed_now"] is False
    assert intake["decision_impact_remote_preflight_allowed_now"] is False
    assert intake["decision_impact_remote_training_allowed_now"] is False
    assert intake["decision_impact_formal_claim_allowed_now"] is False
    assert intake["decision_impact_paper_result_material_allowed_now"] is False
    assert "approved_remote_preflight" in intake["decision_impact_formal_training_still_requires"]
    h02_requirements = manifest["h02_formal_acceptance_requirement_summary"]
    assert h02_requirements["present"] is True
    assert h02_requirements["required_requirement_count"] == 4
    assert h02_requirements["status_counts"] == {"satisfied": 1, "blocked_formal_acceptance": 3}
    assert h02_requirements["blocked_requirement_count"] == 3
    assert manifest["current_state"]["h02_formal_acceptance_requirement_satisfied_count"] == 1
    assert manifest["current_state"]["h02_formal_acceptance_requirement_blocked_count"] == 3
    assert (
        h02_requirements["requirements"]["ppo_rows_and_checkpoint_hash_present"]["status"]
        == "blocked_formal_acceptance"
    )
    assert (
        h02_requirements["requirements"]["ppo_rows_and_checkpoint_hash_present"]["paper_result_input_allowed_now"]
        is False
    )
    closure_stages = manifest["closure_remote_stage_summary"]
    assert closure_stages["approved_remote_preflight"]["allowed_now"] is False
    assert closure_stages["approved_remote_preflight"]["runs_remote_preflight"] is True
    assert closure_stages["approved_remote_preflight"]["host"] == "gpu3070ti-relay"
    assert "source_fresh_preflight_targets_open" in closure_stages["approved_remote_preflight"]["blocked_by"]
    assert closure_stages["gate3_remote_training"]["allowed_now"] is False
    assert closure_stages["gate3_remote_training"]["runs_training"] is True
    assert "remote_packet_not_ready" in closure_stages["gate3_remote_training"]["blocked_by"]
    handoff = manifest["formal_gate_handoff_summary"]
    assert handoff["status"] == "blocked_until_f02_6_decision"
    assert handoff["transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert handoff["transition_gate_audit_issue_count"] == 0
    assert handoff["next_handoff_action_id"] == "record_f02_6_decision"
    assert handoff["remote_training_allowed_now"] is False
    assert handoff["remote_execution_steps"]["run_remote_training"]["allowed_now"] is False
    assert "remote_packet_not_ready" in handoff["remote_execution_steps"]["run_remote_training"]["blocked_by"]
    requirement_stage_summary = manifest["formal_gate_requirement_stage_summary"]
    assert requirement_stage_summary["mapped_requirement_count"] == 4
    assert requirement_stage_summary["unmapped_requirement_count"] == 0
    assert requirement_stage_summary["mismatched_requirement_count"] == 0
    req_stages = requirement_stage_summary["requirements"]
    assert req_stages["training_remote_ppo_checkpoint"]["responsible_stage_id"] == "gate3_remote_training"
    assert req_stages["training_remote_ppo_checkpoint"]["responsible_stage_allowed_now"] is False
    assert "remote_packet_not_ready" in req_stages["training_remote_ppo_checkpoint"]["responsible_stage_blocked_by"]
    assert req_stages["evaluation_gate3_episode_outputs"]["responsible_stage_id"] == "gate3_remote_audit_pullback"
    assert req_stages["acceptance_remote_pullback_and_audit"]["responsible_stage_id"] == "gate3_remote_audit_pullback"
    assert req_stages["h01_h02_formal_evaluation_acceptance"]["responsible_stage_id"] == "regenerate_h01_h02_formal_artifacts"
    missing_handoff = manifest["missing_artifacts_handoff_index_summary"]
    assert missing_handoff["present"] is True
    assert missing_handoff["status"] == "blocked_until_f02_6_decision"
    assert missing_handoff["next_action_id"] == "record_f02_6_decision"
    assert missing_handoff["next_action_requires_dr_sun"] is True
    assert missing_handoff["open_requirement_count"] == 5
    assert missing_handoff["local_training_allowed_now"] is False
    assert missing_handoff["remote_training_allowed_now"] is False
    assert missing_handoff["formal_result_material_allowed_now"] is False
    veto = manifest["formal_gate_execution_veto_summary"]
    assert veto["present"] is True
    assert veto["all_rows_consistent"] is True
    assert veto["row_consensus"]["remote_training"] is False
    assert veto["row_consensus"]["formal_claim"] is False
    remaining = manifest["remaining_deliverables_acceptance_summary"]
    assert remaining["present"] is True
    assert remaining["matrix_row_count"] == 10
    assert remaining["missing_row_count"] == 10
    assert remaining["blocked_category_count"] == 4
    assert remaining["rows"]["training:train_final_model_zip"]["responsible_stage_id"] == "gate3_remote_training"
    assert remaining["rows"]["training:train_final_model_zip"]["acceptance_predicate_count"] > 0
    assert remaining["rows"]["training:train_final_model_zip"]["proof_command_count"] == 2
    assert "train_final_model_zip_schema" in remaining["rows"]["training:train_final_model_zip"]["proof_command_ids"]
    assert remaining["rows"]["training:train_final_model_zip"]["invalid_substitute_count"] > 0
    remaining_gap = manifest["remaining_deliverables_gap_summary"]
    assert remaining_gap["present"] is True
    assert remaining_gap["summary_id"] == "module2_formal_gate_missing_training_eval_acceptance_summary"
    assert remaining_gap["total_missing_deliverables"] == 10
    assert remaining_gap["open_category_count"] == 4
    assert remaining_gap["category_order"] == ["training", "evaluation", "acceptance", "formal_acceptance"]
    assert remaining_gap["categories"]["training"]["missing_count"] == 3
    assert remaining_gap["categories"]["training"]["responsible_stage_id"] == "gate3_remote_training"
    assert remaining_gap["categories"]["training"]["responsible_stage_allowed_now"] is False
    assert remaining_gap["categories"]["training"]["missing_artifact_matrix_ids"] == [
        "training:train_final_model_zip",
        "training:train_summary_json",
        "training:train_training_manifest_json",
    ]
    assert "train_final_model_zip_schema" in remaining_gap["categories"]["training"]["proof_command_ids"]
    assert remaining_gap["categories"]["formal_acceptance"]["missing_count"] == 2
    unlock_chain = manifest["remaining_deliverables_unlock_chain_summary"]
    assert unlock_chain["present"] is True
    assert unlock_chain["chain_id"] == "module2_formal_gate_missing_deliverable_unlock_chain"
    assert unlock_chain["row_count"] == 10
    assert unlock_chain["blocked_row_count"] == 10
    assert unlock_chain["rows_with_missing_required_blockers"] == 0
    assert unlock_chain["rows_allowed_while_missing"] == 0
    assert unlock_chain["categories"]["training"]["row_count"] == 3
    assert unlock_chain["categories"]["training"]["required_current_blockers"] == [
        "f02_6_decision_not_approved",
        "remote_packet_not_ready",
    ]
    next_deliverables = manifest["next_required_formal_deliverables"]
    assert next_deliverables["status"] == "blocked_missing_formal_deliverables"
    assert next_deliverables["execution_boundary"] == "read_only_no_execution"
    assert next_deliverables["not_paper_result_material"] is True
    assert next_deliverables["runs_training"] is False
    assert next_deliverables["runs_remote_preflight"] is False
    assert next_deliverables["total_missing_deliverables"] == 10
    assert next_deliverables["blocked_category_count"] == 4
    assert next_deliverables["blocked_categories"] == [
        "training",
        "evaluation",
        "acceptance",
        "formal_acceptance",
    ]
    assert next_deliverables["rows"][0]["matrix_id"] == "training:train_final_model_zip"
    assert next_deliverables["rows"][0]["responsible_stage_id"] == "gate3_remote_training"
    assert next_deliverables["rows"][0]["responsible_stage_allowed_now"] is False
    assert "train_final_model_zip_schema" in next_deliverables["rows"][0]["proof_command_ids"]
    proof_plan = manifest["remaining_deliverables_proof_command_plan"]
    assert proof_plan["present"] is True
    assert proof_plan["plan_id"] == "module2_formal_gate_local_read_only_proof_commands"
    assert proof_plan["execution_boundary"] == "local_read_only_after_formal_remote_pullback"
    assert proof_plan["not_paper_result_material"] is True
    assert proof_plan["runs_training"] is False
    assert proof_plan["runs_remote_preflight"] is False
    assert proof_plan["total_matrix_rows"] == 10
    assert proof_plan["total_proof_command_count"] == 20
    assert proof_plan["rows"]["training:train_final_model_zip"]["proof_command_count"] == 2
    proof_audit = manifest["formal_gate_proof_audit_summary"]
    assert proof_audit["present"] is True
    assert proof_audit["status"] == "formal_gate_proof_audit_blocked"
    assert proof_audit["total_proof_command_count"] == 20
    assert proof_audit["passed_proof_command_count"] == 2
    assert proof_audit["failed_proof_command_count"] == 2
    assert proof_audit["blocked_proof_command_count"] == 16
    assert proof_audit["category_status_counts"]["training"]["blocked_missing_artifact"] == 6
    assert proof_audit["category_status_counts"]["formal_acceptance"]["failed"] == 2
    assert proof_audit["results_by_id"]["h02_formal_output_acceptance_schema"]["status"] == "failed"
    assert proof_audit["remaining_deliverables_top_level_summary"]["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    proof_deliverables = manifest["formal_gate_proof_audit_remaining_deliverables_top_level_summary"]
    assert proof_deliverables["present"] is True
    assert proof_deliverables["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert proof_deliverables["missing_matrix_ids_by_formal_category"]["training"] == [
        "training:train_final_model_zip",
        "training:train_summary_json",
        "training:train_training_manifest_json",
    ]
    assert proof_deliverables["next_blocked_lane"] == "decision"
    assert proof_deliverables["h01_status"] == "blocked_pending_decisions"
    assert proof_deliverables["h02_status"] == "blocked_formal_output_acceptance"
    assert proof_deliverables["h02_formal_output_accepted"] is False
    assert proof_deliverables["h02_paper_result_input_allowed"] is False
    proof_gap = manifest["formal_gate_proof_audit_gap_summary"]
    assert proof_gap["present"] is True
    assert proof_gap["status"] == "formal_gate_proof_audit_blocked"
    assert proof_gap["missing_artifact_count"] == 8
    assert proof_gap["failed_acceptance_artifact_count"] == 2
    assert proof_gap["categories"]["training"]["missing_artifact_ids"] == [
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ]
    assert proof_gap["categories"]["training"]["blocked_proof_command_count"] == 6
    assert proof_gap["categories"]["evaluation"]["missing_artifact_ids"] == [
        "eval_gate3_eval_episodes_csv",
        "eval_gate3_summary_json",
    ]
    assert proof_gap["categories"]["acceptance"]["missing_artifact_ids"] == [
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
    ]
    assert proof_gap["categories"]["formal_acceptance"]["failed_artifact_ids"] == [
        "h01_ready_for_formal_run",
        "h02_formal_output_acceptance",
    ]
    assert proof_gap["categories"]["formal_acceptance"]["failed_proof_command_ids"] == [
        "h01_ready_for_formal_run_schema",
        "h02_formal_output_acceptance_schema",
    ]
    proof_missing = manifest["formal_gate_proof_audit_missing_evidence_summary"]
    assert proof_missing["training"]["missing_artifact_ids"] == [
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ]
    assert proof_missing["evaluation"]["missing_artifact_ids"] == [
        "eval_gate3_eval_episodes_csv",
        "eval_gate3_summary_json",
    ]
    assert proof_missing["acceptance"]["missing_artifact_ids"] == [
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
    ]
    assert proof_missing["formal_acceptance"]["failed_artifact_ids"] == [
        "h01_ready_for_formal_run",
        "h02_formal_output_acceptance",
    ]
    formal_gate_gap = manifest["formal_gate_gap_audit_remaining_deliverables_gap_summary"]
    assert formal_gate_gap["present"] is True
    assert formal_gate_gap["total_missing_deliverables"] == 10
    assert formal_gate_gap["open_category_count"] == 4
    assert formal_gate_gap["categories"]["training"]["missing_artifact_matrix_ids"] == [
        "training:train_final_model_zip",
        "training:train_summary_json",
        "training:train_training_manifest_json",
    ]
    remote_proof = manifest["remote_packet_safety_proof_deliverables_summary"]
    assert remote_proof["present"] is True
    assert remote_proof["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert remote_proof["missing_matrix_ids_by_formal_category"]["acceptance"] == [
        "acceptance:gate3_trial_manifest_json",
        "acceptance:gate3_formal_audit_json",
        "acceptance:pulled_back_checkpoint_hash_record",
    ]
    assert remote_proof["next_blocked_lane"] == "decision"
    assert remote_proof["h01_status"] == "blocked_pending_decisions"
    assert remote_proof["h02_status"] == "blocked_formal_output_acceptance"
    assert remote_proof["h02_formal_output_accepted"] is False
    assert remote_proof["h02_paper_result_input_allowed"] is False
    remote_status_proof = manifest["remote_packet_safety_status_report_proof_deliverables_summary"]
    assert remote_status_proof == remote_proof
    command_index = manifest["remote_packet_safety_claim_gate_command_index_summary"]
    assert command_index["present"] is True
    assert command_index["index_row_count"] == 23
    assert command_index["source_target_count"] == 23
    assert command_index["missing_target_ids"] == []
    assert command_index["claim_gate_rows"]["formal_gate_proof_summary_chain_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert command_index["claim_gate_rows"]["mainline_formal_gate_state_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert (
        "build_module2_mainline_formal_gate_state_audit"
        in command_index["claim_gate_rows"]["mainline_formal_gate_state_audit"]["command_template"]
    )
    assert command_index["claim_gate_rows"]["claim_safety"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert command_index["claim_gate_rows"]["paper_readiness"]["required_before"] == "formal_claim_gate"
    assert manifest["current_state"]["remote_packet_safety_command_index_present"] is True
    assert manifest["current_state"]["remote_packet_safety_command_index_row_count"] == 23
    assert manifest["current_state"]["next_action_guard_status"] == "next_action_guard_passed"
    next_guard = manifest["next_action_guard_summary"]
    assert next_guard["present"] is True
    assert next_guard["status"] == "next_action_guard_passed"
    assert next_guard["next_blocked_lane_id"] == "decision"
    assert next_guard["expected_next_action_id"] == "record_f02_6_decision"
    assert next_guard["handoff_next_action_id"] == "record_f02_6_decision"
    assert next_guard["decision_intake_next_blocked_lane"] == "decision"
    assert next_guard["all_execution_disabled_now"] is True
    assert next_guard["execution_leak_count"] == 0
    assert next_guard["remote_execution_allowed_count"] == 0
    assert next_guard["remote_stage_allowed_count"] == 0

    lanes = {lane["lane_id"]: lane for lane in manifest["formal_gate_lanes"]}
    assert lanes["gate3_remote_training"]["runs_training"] is True
    assert lanes["gate3_remote_training"]["host"] == "gpu3070ti-relay"
    assert lanes["claim_gate"]["status"] == "blocked"


def test_formal_gate_status_report_accepts_synthetic_complete_chain(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")

    manifest = builder.build_manifest(_config(tmp_path, complete=True))

    assert manifest["status"] == "formal_gate_status_ready_for_claim_audit"
    assert manifest["permissions_now"]["f02_6_decision_closed"] is True
    assert manifest["permissions_now"]["warm_start_formal_chain_approved"] is True
    assert manifest["permissions_now"]["remote_training_allowed_now"] is True
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is True
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is True
    assert manifest["permissions_now"]["local_training_allowed_now"] is False
    assert manifest["input_safety_issue_count"] == 0
    assert all(lane["status"] == "complete" for lane in manifest["formal_gate_lanes"])
    assert manifest["next_blocked_lane"] is None
    assert all(step["allowed_now"] is True for step in manifest["remote_execution_step_summary"].values())
    assert all(step["blocked_by"] == [] for step in manifest["remote_execution_step_summary"].values())
    assert all(stage["allowed_now"] is True for stage in manifest["closure_remote_stage_summary"].values())
    assert all(stage["blocked_by"] == [] for stage in manifest["closure_remote_stage_summary"].values())
    assert manifest["formal_gate_execution_veto_summary"]["all_rows_consistent"] is True
    assert manifest["formal_gate_execution_veto_summary"]["row_consensus"]["remote_training"] is True
    assert manifest["missing_artifacts_handoff_index_summary"]["status"] == "formal_gate_evidence_ready_for_h01_h02_claim_gates"
    assert manifest["missing_artifacts_handoff_index_summary"]["open_requirement_count"] == 0
    assert manifest["formal_gate_requirement_stage_summary"]["mapped_requirement_count"] == 4
    assert manifest["f02_6_decision_intake_summary"]["status"] == "f02_6_decision_intake_closed_clean"
    assert manifest["f02_6_decision_intake_summary"]["record_status"] == "approved"
    assert manifest["f02_6_decision_intake_summary"]["record_decider"] == "Dr Sun"
    assert manifest["f02_6_decision_intake_summary"]["decision_owner_required"] == "Dr Sun"
    assert manifest["current_state"]["decision_intake_valid_decision_count"] == 2
    assert manifest["current_state"]["decision_intake_required_record_field_count"] == 3
    assert manifest["current_state"]["decision_intake_record_command_template_count"] == 2
    assert manifest["current_state"]["decision_intake_post_decision_route_count"] == 2
    assert manifest["f02_6_decision_intake_summary"]["decision_note_required"] is True
    assert manifest["f02_6_decision_intake_summary"]["decision_impact_present"] is True
    assert manifest["f02_6_decision_intake_summary"]["decision_record_is_not_training_authorization"] is True
    assert manifest["f02_6_decision_intake_summary"]["decision_impact_remote_training_allowed_now"] is False
    assert manifest["remote_preflight_requirement_summary"]["status_counts"] == {"satisfied": 4}
    assert manifest["post_run_acceptance_requirement_summary"]["status_counts"] == {"satisfied": 4}
    assert manifest["h02_formal_acceptance_requirement_summary"]["status_counts"] == {"satisfied": 4}
    assert manifest["remaining_deliverables_acceptance_summary"]["matrix_row_count"] == 10
    assert manifest["remaining_deliverables_acceptance_summary"]["missing_row_count"] == 0
    assert manifest["remaining_deliverables_proof_command_plan"]["total_matrix_rows"] == 10
    assert manifest["remote_packet_safety_proof_deliverables_summary"]["present"] is True
    assert manifest["remote_packet_safety_proof_deliverables_summary"][
        "missing_counts_by_formal_category"
    ] == {
        "training": 0,
        "evaluation": 0,
        "acceptance": 0,
        "formal_acceptance": 0,
    }
    assert manifest["remote_packet_safety_status_report_proof_deliverables_summary"] == manifest[
        "remote_packet_safety_proof_deliverables_summary"
    ]
    assert manifest["remaining_deliverables_proof_command_plan"]["total_proof_command_count"] == 20
    assert manifest["formal_gate_proof_audit_summary"]["status"] == "formal_gate_proof_audit_passed"
    assert manifest["formal_gate_proof_audit_summary"]["passed_proof_command_count"] == 20
    assert manifest["formal_gate_proof_audit_summary"]["blocked_proof_command_count"] == 0
    assert manifest["formal_gate_proof_audit_remaining_deliverables_top_level_summary"][
        "missing_counts_by_formal_category"
    ] == {
        "training": 0,
        "evaluation": 0,
        "acceptance": 0,
        "formal_acceptance": 0,
    }
    assert manifest["formal_gate_proof_audit_gap_summary"]["missing_artifact_count"] == 0
    assert manifest["formal_gate_proof_audit_gap_summary"]["failed_acceptance_artifact_count"] == 0
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 0
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 0
    assert manifest["formal_gate_gap_audit_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 0
    assert manifest["formal_gate_gap_audit_remaining_deliverables_gap_summary"]["open_category_count"] == 0
    assert manifest["remote_packet_safety_claim_gate_command_index_summary"]["index_row_count"] == 23
    assert all(
        category["missing_artifact_matrix_ids"] == []
        for category in manifest["remaining_deliverables_gap_summary"]["categories"].values()
    )
    assert manifest["current_state"]["source_freshness_status"] == "source_freshness_clean_current"
    assert manifest["current_state"]["source_freshness_regeneration_required"] is False


def test_formal_gate_status_report_blocks_remote_when_source_freshness_is_stale(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=True)
    config.source_freshness_path.write_text(json.dumps(_source_freshness(complete=False)), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "source_freshness_blocks_remote_execution" in issue_ids
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is False
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_accepts_source_freshness_self_lag_only(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=True)
    source_freshness = _source_freshness(complete=True)
    source_freshness["status"] = "source_freshness_tracked_artifact_lag_only_gate_ready"
    source_freshness["regeneration_required_before_remote_formal_execution"] = True
    source_freshness["blocking_regeneration_required_before_remote_formal_execution"] = False
    source_freshness["blocking_regeneration_target_count"] = 0
    source_freshness["commit_lag_summary"]["records_with_self_artifact_only_lag"] = 1
    config.source_freshness_path.write_text(json.dumps(source_freshness), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["current_state"]["source_freshness_regeneration_required"] is True
    assert manifest["current_state"]["source_freshness_blocking_regeneration_required"] is False
    assert manifest["current_state"]["source_freshness_self_artifact_only_lag_records"] == 1
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is True
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is True
    assert manifest["permissions_now"]["remote_training_allowed_now"] is True
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is True


def test_formal_gate_status_report_catches_status_input_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")

    manifest = builder.build_manifest(_config(tmp_path, complete=False, drift=True))

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "closure_checklist_executes_commands" in issue_ids
    assert "remote_packet_allows_claim_before_audit" in issue_ids
    assert "claim_safety_allows_formal_claim" in issue_ids
    assert "missing_artifacts_handoff_allows_remote_training_while_open" in issue_ids
    assert "missing_artifacts_handoff_allows_result_material" in issue_ids
    assert "handoff_bundle_safety_issues_open" in issue_ids
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_requires_clean_decision_intake(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    intake = json.loads(config.decision_intake_path.read_text(encoding="utf-8"))
    intake["status"] = "f02_6_decision_intake_failed"
    intake["audit_issue_count"] = 1
    intake["current_state"]["status_report_remote_training_allowed_now"] = True
    intake["current_state"]["packet_current_allowed_action_ids"] = [
        "record_f02_6_decision",
        "remote_preflight",
    ]
    intake["current_state"]["packet_current_blocked_action_ids"] = [
        "remote_training",
        "local_training",
        "formal_claim",
    ]
    intake["current_state"]["packet_post_decision_routes_are_current_authorization"] = True
    intake["current_state"]["packet_remote_preflight_allowed_now"] = True
    intake["current_state"]["packet_paper_result_material_allowed_now"] = True
    intake["next_human_decision_request"]["decision_owner_required"] = "Assistant"
    intake["next_human_decision_request"]["current_allowed_action_ids"] = [
        "record_f02_6_decision",
        "remote_training",
    ]
    intake["next_human_decision_request"]["current_blocked_action_ids"] = [
        "remote_preflight",
        "local_training",
        "formal_claim",
    ]
    intake["next_human_decision_request"]["post_decision_routes_are_current_authorization"] = True
    intake["next_human_decision_request"]["all_execution_disabled_now"] = False
    config.decision_intake_path.write_text(json.dumps(intake), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "decision_intake_not_clean" in issue_ids
    assert "decision_intake_audit_issues_open" in issue_ids
    assert "decision_intake_remote_training_allowed_now_not_false" in issue_ids
    assert "decision_intake_packet_allowed_actions_not_decision_only" in issue_ids
    assert "decision_intake_packet_missing_blocked_actions" in issue_ids
    assert "decision_intake_next_request_owner_not_dr_sun" in issue_ids
    assert "decision_intake_next_request_allowed_actions_not_decision_only" in issue_ids
    assert "decision_intake_next_request_missing_blocked_actions" in issue_ids
    assert "decision_intake_next_request_treats_routes_as_authorization" in issue_ids
    assert "decision_intake_next_request_execution_not_disabled" in issue_ids
    assert "decision_intake_packet_treats_routes_as_authorization" in issue_ids
    assert "decision_intake_packet_remote_preflight_allowed_now_not_false" in issue_ids
    assert "decision_intake_packet_paper_result_material_allowed_now_not_false" in issue_ids
    assert "decision_intake_packet_status_report_remote_preflight_mismatch" in issue_ids
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_status_report_rejects_decision_record_current_permission_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    decision_record = json.loads(config.decision_record_path.read_text(encoding="utf-8"))
    decision_record["remote_preflight_allowed_now"] = True
    decision_record["remote_training_allowed_now"] = True
    config.decision_record_path.write_text(json.dumps(decision_record), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "decision_record_allows_remote_preflight_now" in issue_ids
    assert "decision_record_allows_remote_training_now" in issue_ids
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_status_report_rejects_closed_decision_record_without_note(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=True)
    decision_record = json.loads(config.decision_record_path.read_text(encoding="utf-8"))
    decision_record["decision_note"] = ""
    config.decision_record_path.write_text(json.dumps(decision_record), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "decision_record_closed_missing_decision_note" in issue_ids
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_requires_decision_intake_contract(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    intake = json.loads(config.decision_intake_path.read_text(encoding="utf-8"))
    intake["decision_intake_contract"]["decision_owner_required"] = "Assistant"
    intake["decision_intake_contract"]["valid_decisions"] = ["approve_obstacle_summary_warm_start"]
    intake["decision_intake_contract"]["required_record_fields_for_non_pending_decision"] = ["decision", "decider"]
    intake["invalid_inputs"] = []
    intake["post_decision_non_authorizations"] = []
    intake["post_decision_route_matrix"] = []
    config.decision_intake_path.write_text(json.dumps(intake), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "decision_intake_contract_decision_owner_not_dr_sun" in issue_ids
    assert "decision_intake_contract_missing_valid_decisions" in issue_ids
    assert "decision_intake_contract_missing_required_record_fields" in issue_ids
    assert "decision_intake_invalid_inputs_missing" in issue_ids
    assert "decision_intake_post_decision_non_authorizations_missing" in issue_ids
    assert "decision_intake_post_decision_route_matrix_missing" in issue_ids
    summary = manifest["f02_6_decision_intake_summary"]
    assert summary["decision_owner_required"] == "Assistant"
    assert summary["decision_note_required"] is False


def test_formal_gate_status_report_requires_decision_intake_impact_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    intake = json.loads(config.decision_intake_path.read_text(encoding="utf-8"))
    intake.pop("formal_gate_decision_impact_summary")
    config.decision_intake_path.write_text(json.dumps(intake), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "decision_intake_impact_summary_missing" in issue_ids
    assert "decision_intake_impact_decision_record_is_not_training_authorization_not_true" in issue_ids
    assert manifest["f02_6_decision_intake_summary"]["decision_impact_present"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_requires_missing_artifacts_handoff_index(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    missing_artifacts = json.loads(config.missing_artifacts_path.read_text(encoding="utf-8"))
    missing_artifacts.pop("formal_gate_handoff_index")
    config.missing_artifacts_path.write_text(json.dumps(missing_artifacts), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "missing_artifacts_handoff_index_missing" in issue_ids
    assert manifest["missing_artifacts_handoff_index_summary"]["present"] is False


def test_formal_gate_status_report_requires_remote_step_blockers(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    remote_packet = json.loads(config.remote_packet_path.read_text(encoding="utf-8"))
    remote_packet["execution_steps"]["sync_to_remote"]["blocked_by"] = []
    remote_packet["execution_steps"]["run_remote_training"]["blocked_by"] = []
    config.remote_packet_path.write_text(json.dumps(remote_packet), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "remote_packet_sync_to_remote_missing_blocked_by" in issue_ids
    assert "remote_packet_run_remote_training_missing_blocked_by" in issue_ids
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_status_report_requires_remote_requirement_matrices(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    remote_packet = json.loads(config.remote_packet_path.read_text(encoding="utf-8"))
    remote_packet.pop("remote_preflight_requirements")
    remote_packet.pop("remote_preflight_requirement_counts")
    remote_packet["post_run_acceptance_requirements"][0].pop("acceptable_evidence")
    remote_packet["post_run_acceptance_requirements"][1]["execution_allowed_now"] = True
    config.remote_packet_path.write_text(json.dumps(remote_packet), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "remote_preflight_requirement_matrix_missing" in issue_ids
    assert "post_run_acceptance_requirement_pullback_expected_artifacts_complete_missing_acceptable_evidence" in issue_ids
    assert "post_run_acceptance_requirement_checkpoint_hash_manifest_recorded_allowed_while_packet_blocked" in issue_ids
    assert manifest["remote_preflight_requirement_summary"]["present"] is False
    assert manifest["post_run_acceptance_requirement_summary"]["blocked_requirement_count"] == 4


def test_formal_gate_status_report_requires_h02_acceptance_requirement_matrix(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    h02 = json.loads(config.h02_acceptance_path.read_text(encoding="utf-8"))
    h02.pop("formal_acceptance_requirement_counts")
    h02["formal_acceptance_requirements"][0].pop("acceptable_evidence")
    h02["formal_acceptance_requirements"][1]["paper_result_input_allowed_now"] = True
    h02["formal_acceptance_requirements"] = h02["formal_acceptance_requirements"][:-1]
    config.h02_acceptance_path.write_text(json.dumps(h02), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "h02_formal_acceptance_requirement_counts_missing" in issue_ids
    assert (
        "h02_formal_acceptance_requirement_h01_schema_and_h02_output_schema_match_missing_acceptable_evidence"
        in issue_ids
    )
    assert (
        "h02_formal_acceptance_requirement_h02_formal_scope_and_scale_match_h01_allows_paper_result_while_h02_blocked"
        in issue_ids
    )
    assert "h02_formal_acceptance_requirement_missing_ppo_rows_and_checkpoint_hash_present" in issue_ids
    assert manifest["h02_formal_acceptance_requirement_summary"]["missing_requirement_ids"] == [
        "ppo_rows_and_checkpoint_hash_present"
    ]


def test_formal_gate_status_report_requires_remaining_deliverables_acceptance_matrix(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    remaining = json.loads(config.remaining_deliverables_path.read_text(encoding="utf-8"))
    remaining["deliverable_acceptance_matrix"][0].pop("acceptance_predicates")
    remaining["deliverable_acceptance_matrix"][1]["responsible_stage_allowed_now"] = True
    remaining["deliverable_acceptance_matrix"] = remaining["deliverable_acceptance_matrix"][:-1]
    config.remaining_deliverables_path.write_text(json.dumps(remaining), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "remaining_deliverables_acceptance_matrix_count_mismatch" in issue_ids
    assert "remaining_deliverables_training_train_final_model_zip_missing_acceptance_predicates" in issue_ids
    assert "remaining_deliverables_training_train_summary_json_stage_allowed_while_blocked" in issue_ids
    assert "remaining_deliverables_acceptance_missing_formal_acceptance_h02_formal_output_acceptance" in issue_ids
    assert manifest["remaining_deliverables_acceptance_summary"]["matrix_row_count"] == 9


def test_formal_gate_status_report_requires_remaining_deliverables_gap_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    remaining = json.loads(config.remaining_deliverables_path.read_text(encoding="utf-8"))
    remaining["deliverable_gap_summary"]["total_missing_deliverables"] = 9
    remaining["deliverable_gap_summary"]["open_category_count"] = 3
    remaining["deliverable_gap_summary"]["category_order"] = ["training", "evaluation"]
    remaining["deliverable_gap_summary"]["categories"][0]["responsible_stage_allowed_now"] = True
    remaining["deliverable_gap_summary"]["categories"][0]["missing_artifacts"] = remaining["deliverable_gap_summary"][
        "categories"
    ][0]["missing_artifacts"][:-1]
    remaining["deliverable_gap_summary"]["categories"][1]["missing_count"] = 1
    remaining["deliverable_gap_summary"]["categories"][2]["responsible_stage_id"] = "wrong_stage"
    remaining["deliverable_gap_summary"]["categories"][3]["missing_artifacts"][0]["acceptance_predicate_count"] = 0
    config.remaining_deliverables_path.write_text(json.dumps(remaining), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "remaining_deliverables_gap_total_missing_mismatch" in issue_ids
    assert "remaining_deliverables_gap_open_category_mismatch" in issue_ids
    assert "remaining_deliverables_gap_category_order_mismatch" in issue_ids
    assert "remaining_deliverables_gap_training_stage_allowed_while_blocked" in issue_ids
    assert "remaining_deliverables_gap_training_missing_artifact_ids_mismatch" in issue_ids
    assert "remaining_deliverables_gap_evaluation_missing_count_mismatch" in issue_ids
    assert "remaining_deliverables_gap_acceptance_wrong_responsible_stage" in issue_ids
    assert "remaining_deliverables_gap_formal_acceptance_h01_ready_for_formal_run_missing_predicates" in issue_ids
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 9


def test_formal_gate_status_report_requires_remaining_deliverables_unlock_chain(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    remaining = json.loads(config.remaining_deliverables_path.read_text(encoding="utf-8"))
    chain = remaining["deliverable_unlock_chain"]
    chain["row_count"] = 9
    chain["blocked_row_count"] = 9
    chain["rows"][0]["missing_required_current_blockers"] = ["f02_6_decision_not_approved"]
    chain["rows"][1]["responsible_stage_allowed_now"] = True
    config.remaining_deliverables_path.write_text(json.dumps(remaining), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "remaining_deliverables_unlock_chain_row_count_mismatch" in issue_ids
    assert "remaining_deliverables_unlock_chain_blocked_row_count_mismatch" in issue_ids
    assert "remaining_deliverables_unlock_chain_rows_missing_required_blockers" in issue_ids
    assert "remaining_deliverables_unlock_chain_rows_allowed_while_missing" in issue_ids
    assert manifest["remaining_deliverables_unlock_chain_summary"]["rows_with_missing_required_blockers"] == 1
    assert manifest["remaining_deliverables_unlock_chain_summary"]["rows_allowed_while_missing"] == 1
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_requires_remaining_deliverables_proof_command_plan(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    remaining = json.loads(config.remaining_deliverables_path.read_text(encoding="utf-8"))
    remaining["proof_command_plan"]["total_matrix_rows"] = 9
    remaining["proof_command_plan"]["total_proof_command_count"] = 17
    remaining["proof_command_plan"]["rows"] = remaining["proof_command_plan"]["rows"][:-1]
    remaining["proof_command_plan"]["runs_training"] = True
    remaining["deliverable_acceptance_matrix"][0]["proof_commands"] = []
    remaining["deliverable_gap_summary"]["categories"][0]["missing_artifacts"][0]["proof_command_count"] = 0
    remaining["deliverable_gap_summary"]["categories"][0]["missing_artifacts"][0]["proof_command_ids"] = []
    config.remaining_deliverables_path.write_text(json.dumps(remaining), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "remaining_deliverables_proof_command_plan_runs_training" in issue_ids
    assert "remaining_deliverables_proof_command_plan_matrix_count_mismatch" in issue_ids
    assert "remaining_deliverables_proof_command_plan_command_count_mismatch" in issue_ids
    assert "remaining_deliverables_training_train_final_model_zip_missing_proof_commands" in issue_ids
    assert "remaining_deliverables_gap_training_train_final_model_zip_missing_proof_commands" in issue_ids
    assert "remaining_deliverables_proof_command_plan_missing_formal_acceptance_h02_formal_output_acceptance" in issue_ids
    assert manifest["remaining_deliverables_proof_command_plan"]["total_matrix_rows"] == 9


def test_formal_gate_status_report_requires_formal_gate_proof_audit_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=True)
    proof_audit = json.loads(config.formal_gate_proof_audit_path.read_text(encoding="utf-8"))
    proof_audit["executes_commands"] = True
    proof_audit["runs_training"] = True
    proof_audit["runs_remote_preflight"] = True
    proof_audit["total_matrix_rows"] = 9
    proof_audit["total_proof_command_count"] = 19
    proof_audit["passed_proof_command_count"] = 19
    proof_audit["proof_command_results"].pop()
    proof_audit["proof_command_results_by_id"].pop("h02_formal_output_acceptance_schema")
    config.formal_gate_proof_audit_path.write_text(json.dumps(proof_audit), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_proof_audit_executes_commands" in issue_ids
    assert "formal_gate_proof_audit_runs_training" in issue_ids
    assert "formal_gate_proof_audit_runs_remote_preflight" in issue_ids
    assert "formal_gate_proof_audit_matrix_count_mismatch" in issue_ids
    assert "formal_gate_proof_audit_command_count_mismatch" in issue_ids
    assert "formal_gate_proof_audit_missing_h02_formal_output_acceptance_schema" in issue_ids
    assert manifest["formal_gate_proof_audit_summary"]["total_matrix_rows"] == 9


def test_formal_gate_status_report_consumes_handoff_bundle_safety(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    handoff = json.loads(config.handoff_bundle_path.read_text(encoding="utf-8"))
    handoff["remote_execution_steps"]["run_remote_training"]["allowed_now"] = True
    handoff["remote_execution_steps"]["run_remote_training"]["blocked_by"] = []
    config.handoff_bundle_path.write_text(json.dumps(handoff), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "handoff_bundle_pending_allows_run_remote_training" in issue_ids
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_status_report_next_action_guard_rejects_execution_handoff(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    handoff = json.loads(config.handoff_bundle_path.read_text(encoding="utf-8"))
    handoff["next_handoff_action"]["action_id"] = "run_remote_training"
    handoff["next_handoff_action"]["requires_dr_sun"] = False
    config.handoff_bundle_path.write_text(json.dumps(handoff), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["next_action_guard_summary"]["status"] == "next_action_guard_failed"
    assert "next_action_guard_unexpected_handoff_action" in issue_ids
    assert "next_action_guard_handoff_action_not_dr_sun_gated" in issue_ids
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_status_report_requires_handoff_requirement_stage_mapping(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    handoff = json.loads(config.handoff_bundle_path.read_text(encoding="utf-8"))
    handoff["formal_gate_requirements"][0].pop("responsible_stage_id")
    handoff["formal_gate_requirements"][1]["responsible_stage_id"] = "wrong_stage"
    config.handoff_bundle_path.write_text(json.dumps(handoff), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "handoff_bundle_training_remote_ppo_checkpoint_missing_responsible_stage" in issue_ids
    assert "handoff_bundle_evaluation_gate3_episode_outputs_wrong_responsible_stage" in issue_ids
    assert manifest["formal_gate_requirement_stage_summary"]["unmapped_requirement_count"] == 1
    assert manifest["formal_gate_requirement_stage_summary"]["mismatched_requirement_count"] == 1


def test_formal_gate_status_report_consumes_execution_veto_matrix(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate["execution_veto_matrix"]["all_rows_consistent"] = False
    formal_gate["execution_veto_matrix"]["mismatch_rows"] = ["remote_training"]
    for row in formal_gate["execution_veto_matrix"]["rows"]:
        if row["row_id"] == "remote_training":
            row["consistent"] = False
            row["consensus_allowed_now"] = True
            row["allowed_now_by_source"]["remote_packet"] = True
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "formal_gate_execution_veto_rows_inconsistent" in issue_ids
    assert "formal_gate_execution_veto_mismatch_rows_open" in issue_ids
    assert "blocked_formal_gate_execution_veto_allows_remote_training" in issue_ids
    assert manifest["formal_gate_execution_veto_summary"]["all_rows_consistent"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_status_report_requires_execution_veto_matrix(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate.pop("execution_veto_matrix")
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_missing_execution_veto_matrix" in issue_ids
    assert manifest["formal_gate_execution_veto_summary"]["present"] is False


def test_formal_gate_status_report_requires_formal_gate_gap_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate.pop("remaining_deliverables_gap_summary", None)
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_gap_audit_missing_remaining_deliverables_gap_summary" in issue_ids
    assert manifest["formal_gate_gap_audit_remaining_deliverables_gap_summary"]["present"] is False


def test_formal_gate_status_report_rejects_formal_gate_gap_summary_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate["remaining_deliverables_gap_summary"]["categories"][0]["missing_count"] = 2
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_gap_audit_remaining_deliverables_gap_summary_mismatch" in issue_ids
    assert manifest["formal_gate_gap_audit_remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] == 2


def test_formal_gate_status_report_rejects_remote_safety_command_index_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=True)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    summary = formal_gate["remote_packet_safety"]["claim_gate_command_index_summary"]
    summary["missing_target_ids"] = ["paper_readiness"]
    summary["unknown_manual_count"] = 1
    summary["forbidden_command_count"] = 1
    summary["claim_gate_rows"]["claim_safety"]["stage_id"] = "regenerate_preflight_gate_artifacts"
    summary["claim_gate_rows"]["claim_safety"]["command_kind"] = "unknown_manual"
    summary["claim_gate_rows"].pop("paper_readiness")
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "formal_gate_remote_packet_safety_command_index_missing_targets" in issue_ids
    assert "formal_gate_remote_packet_safety_command_index_unknown_manual_rows" in issue_ids
    assert "formal_gate_remote_packet_safety_command_index_forbidden_commands" in issue_ids
    assert "formal_gate_remote_packet_safety_command_index_claim_safety_wrong_stage" in issue_ids
    assert "formal_gate_remote_packet_safety_command_index_claim_safety_manual_command" in issue_ids
    assert "formal_gate_remote_packet_safety_command_index_missing_paper_readiness" in issue_ids
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_allows_current_clean_claim_safety_omitted_from_command_index(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=True)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    summary = formal_gate["remote_packet_safety"]["claim_gate_command_index_summary"]
    summary["claim_gate_rows"].pop("claim_safety")
    summary["index_row_count"] = 21
    summary["source_target_count"] = 21
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_remote_packet_safety_command_index_missing_claim_safety" not in issue_ids
    assert manifest["remote_packet_safety_claim_gate_command_index_summary"]["claim_gate_rows"]["claim_safety"][
        "present"
    ] is False


def test_formal_gate_status_report_requires_remote_safety_proof_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate["remote_packet_safety"].pop("proof_deliverables_summary")
    formal_gate["remote_packet_safety"].pop("status_report_proof_deliverables_summary")
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_remote_packet_safety_missing_proof_deliverables_summary" in issue_ids
    assert "formal_gate_remote_packet_safety_missing_status_report_proof_deliverables_summary" in issue_ids
    assert manifest["remote_packet_safety_proof_deliverables_summary"]["present"] is False
    assert manifest["remote_packet_safety_status_report_proof_deliverables_summary"]["present"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_rejects_remote_safety_proof_summary_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate["remote_packet_safety"]["proof_deliverables_summary"][
        "missing_counts_by_formal_category"
    ]["training"] = 2
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert "formal_gate_remote_packet_safety_proof_deliverables_summary_mismatch" in issue_ids
    assert "formal_gate_remote_packet_safety_proof_deliverables_summary_drifted_from_proof_audit" in issue_ids
    assert manifest["remote_packet_safety_proof_deliverables_summary"][
        "missing_counts_by_formal_category"
    ]["training"] == 2
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_rejects_remote_safety_proof_allowing_results_while_missing(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    formal_gate = json.loads(config.formal_gate_path.read_text(encoding="utf-8"))
    formal_gate["remote_packet_safety"]["proof_deliverables_summary"][
        "h02_paper_result_input_allowed"
    ] = True
    formal_gate["remote_packet_safety"]["status_report_proof_deliverables_summary"][
        "h02_paper_result_input_allowed"
    ] = True
    config.formal_gate_path.write_text(json.dumps(formal_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert (
        "formal_gate_remote_packet_safety_proof_allows_paper_results_with_missing_deliverables"
        in issue_ids
    )
    assert (
        "formal_gate_remote_packet_safety_status_report_proof_allows_paper_results_with_missing_deliverables"
        in issue_ids
    )
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


def test_formal_gate_status_report_requires_closure_remote_stage_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    closure = json.loads(config.closure_checklist_path.read_text(encoding="utf-8"))
    closure.pop("post_plan_remote_stage_summary")
    config.closure_checklist_path.write_text(json.dumps(closure), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "closure_checklist_missing_remote_stage_summary" in issue_ids


def test_formal_gate_status_report_requires_closure_remote_stage_blockers(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    closure = json.loads(config.closure_checklist_path.read_text(encoding="utf-8"))
    closure["post_plan_remote_stage_summary"]["approved_remote_preflight"]["blocked_by"] = []
    closure["post_plan_remote_stage_summary"]["gate3_remote_training"]["blocked_by"] = []
    config.closure_checklist_path.write_text(json.dumps(closure), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "closure_checklist_approved_remote_preflight_missing_blocked_by" in issue_ids
    assert "closure_checklist_gate3_remote_training_missing_blocked_by" in issue_ids


def test_formal_gate_status_report_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    config = _config(tmp_path, complete=False)
    manifest_path = tmp_path / "formal_gate_status_report.json"
    markdown_path = tmp_path / "formal_gate_status_report.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--formal-gate",
            str(config.formal_gate_path),
            "--missing-artifacts",
            str(config.missing_artifacts_path),
            "--closure-checklist",
            str(config.closure_checklist_path),
            "--decision-record",
            str(config.decision_record_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--h01-manifest",
            str(config.h01_manifest_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
            "--claim-safety",
            str(config.claim_safety_path),
            "--paper-readiness",
            str(config.paper_readiness_path),
            "--handoff-bundle",
            str(config.handoff_bundle_path),
            "--remaining-deliverables",
            str(config.remaining_deliverables_path),
            "--formal-gate-proof-audit",
            str(config.formal_gate_proof_audit_path),
            "--decision-intake",
            str(config.decision_intake_path),
            "--source-freshness",
            str(config.source_freshness_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "Module2 Formal Gate Status Report" in markdown
    assert "gate3_remote_training" in markdown
    assert "Remote Execution Steps" in markdown
    assert "Closure Remote Stages" in markdown
    assert "Formal Gate Handoff Bundle" in markdown
    assert "Formal Gate Requirement Stage Summary" in markdown
    assert "H02 Formal Acceptance Requirement Matrix" in markdown
    assert "ppo_rows_and_checkpoint_hash_present" in markdown
    assert "training_remote_ppo_checkpoint" in markdown
    assert "Missing-Artifacts Handoff Index" in markdown
    assert "record_f02_6_decision" in markdown
    assert "Formal Gate Execution Veto Matrix" in markdown
    assert "Remote Packet Safety Claim-Gate Command Index" in markdown
    assert "Remaining Deliverables Acceptance Matrix" in markdown
    assert "Next Required Formal Deliverables" in markdown
    assert "Formal Gate Proof Audit" in markdown
    assert "Formal Gate Proof Audit Gap Summary" in markdown
    assert "source_freshness_status" in markdown
    assert "missing_artifact_count=`8`" in markdown
    assert "formal_gate_proof_audit_blocked" in markdown
    assert "remaining_missing_counts_by_formal_category" in markdown
    assert "remaining_formal_acceptance_missing_matrix_ids" in markdown
    assert "Remote Packet Safety Proof Deliverables Summary" in markdown
    assert "proof_missing_counts_by_formal_category" in markdown
    assert "proof_h02_paper_result_input_allowed" in markdown
    assert "remote_proof_matches_proof_audit" in markdown
    assert "training:train_final_model_zip" in markdown
    assert "decision_owner_required" in markdown
    assert "decision_note_required" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete, drift=False):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    return builder.FormalGateStatusReportConfig(
        output_dir=tmp_path,
        formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate(complete=complete)),
        missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts(complete=complete, drift=drift)),
        closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist(complete=complete, drift=drift)),
        decision_record_path=_json(tmp_path, "decision_record.json", _decision_record(complete=complete)),
        decision_intake_path=_json(tmp_path, "decision_intake.json", _decision_intake(complete=complete)),
        remote_packet_path=_json(tmp_path, "remote_packet.json", _remote_packet(complete=complete, drift=drift)),
        h01_manifest_path=_json(tmp_path, "h01_manifest.json", _h01_manifest(complete=complete)),
        h02_acceptance_path=_json(tmp_path, "h02_acceptance.json", _h02_acceptance(complete=complete)),
        claim_safety_path=_json(tmp_path, "claim_safety.json", _claim_safety(complete=complete, drift=drift)),
        paper_readiness_path=_json(tmp_path, "paper_readiness.json", _paper_readiness(complete=complete)),
        handoff_bundle_path=_json(tmp_path, "handoff_bundle.json", _handoff_bundle(complete=complete, drift=drift)),
        remaining_deliverables_path=_json(
            tmp_path,
            "remaining_deliverables.json",
            _remaining_deliverables(complete=complete),
        ),
        source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness(complete=complete)),
        formal_gate_proof_audit_path=_json(
            tmp_path,
            "formal_gate_proof_audit.json",
            _formal_gate_proof_audit(complete=complete),
        ),
    )


def _formal_gate(*, complete):
    remaining = _remaining_deliverables(complete=complete)
    proof_summary = {
        "present": True,
        "missing_counts_by_formal_category": remaining["missing_counts_by_formal_category"],
        "missing_matrix_ids_by_formal_category": remaining["missing_matrix_ids_by_formal_category"],
        "next_blocked_lane": remaining["next_blocked_lane"],
        "h01_status": remaining["h01_status"],
        "h02_status": remaining["h02_status"],
        "h02_formal_output_accepted": remaining["h02_formal_output_accepted"],
        "h02_paper_result_input_allowed": remaining["h02_paper_result_input_allowed"],
    }
    return {
        "status": "formal_gate_ready_for_result_audit" if complete else "blocked_formal_gate_gaps_open",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "execution_veto_matrix": _execution_veto_matrix(complete=complete),
        "remaining_deliverables_gap_summary": remaining["deliverable_gap_summary"],
        "remote_packet_safety": {
            "claim_gate_command_index_summary": _command_index_summary(),
            "proof_deliverables_summary": proof_summary,
            "status_report_proof_deliverables_summary": json.loads(json.dumps(proof_summary)),
        },
        "ordered_next_steps": [
            {"step_id": "F02.6", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["f02_6_decision_not_approved"]},
            {"step_id": "remote_preflight", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["source_freshness_regeneration_required"]},
            {"step_id": "gate3_remote_training", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["remote_training_packet_not_ready"]},
            {"step_id": "gate3_remote_audit_pullback", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["missing_remote_pullback_artifact"]},
            {"step_id": "h01_h02_regeneration", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["h01_manifest_not_ready"]},
            {"step_id": "claim_safety_final_gate", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["h02_formal_acceptance_not_ready"]},
        ],
    }


def _command_index_summary():
    rows = {
        f"source_target_{index}": {
            "stage_id": "regenerate_preflight_gate_artifacts",
            "required_before": "approved_remote_preflight",
            "command_kind": "known_builder",
            "command_template": f"PYTHONPATH=2_experiment python -m builder_{index}",
        }
        for index in range(17)
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
    rows["claim_safety"] = {
        "stage_id": "regenerate_claim_gate_artifacts",
        "required_before": "formal_claim_gate",
        "command_kind": "known_builder",
        "command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety",
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


def _execution_veto_matrix(*, complete):
    rows = [
        _veto_row(
            "local_training",
            {
                "formal_gate_gap_audit": False,
                "status_report": False,
                "handoff_bundle": False,
                "remote_packet": False,
            },
        ),
        _veto_row(
            "remote_preflight",
            {
                "status_report": complete,
                "handoff_bundle": complete,
                "remote_packet": complete,
                "remote_packet_safety": complete,
            },
        ),
        _veto_row(
            "remote_training",
            {
                "decision_record": complete,
                "status_report": complete,
                "handoff_bundle": complete,
                "remote_packet": complete,
                "remote_packet_safety": complete,
            },
        ),
        _veto_row(
            "remote_audit",
            {
                "handoff_bundle": complete,
                "remote_packet": complete,
                "remote_packet_safety": complete,
            },
        ),
        _veto_row(
            "formal_claim",
            {
                "status_report": complete,
                "handoff_bundle": complete,
            },
        ),
    ]
    return {
        "matrix_version": 1,
        "f02_6_decision_status": "approved" if complete else "pending_human_decision",
        "all_rows_consistent": True,
        "mismatch_rows": [],
        "rows": rows,
    }


def _veto_row(row_id, sources):
    observed = list(sources.values())
    return {
        "row_id": row_id,
        "allowed_now_by_source": sources,
        "consistent": len(set(observed)) <= 1,
        "consensus_allowed_now": bool(observed) and set(observed) == {True},
    }


def _missing_artifacts(*, complete, drift=False):
    groups = [
        _group("f02_6_decision_record", "decision", ["f02_6_decision_record"], complete=complete),
        _group("source_fresh_regeneration_targets", "regeneration", ["formal_gate_gap_audit"], complete=complete),
        _group("post_f02_6_ordered_stages", "gate_sequence", ["approved_remote_preflight"], complete=complete),
        _group("remote_training_outputs", "training", ["train_final_model_zip", "train_summary_json", "train_training_manifest_json"], complete=complete),
        _group("gate3_evaluation_outputs", "evaluation", ["eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"], complete=complete),
        _group("gate3_acceptance_pullback", "acceptance", ["gate3_trial_manifest_json", "gate3_formal_audit_json", "pulled_back_checkpoint_hash_record"], complete=complete),
        _group("h01_h02_formal_evaluation_acceptance", "evaluation_acceptance", ["h01_ready_for_formal_run", "h02_formal_output_acceptance"], complete=complete),
        _group("claim_gate_regeneration", "claim_gate", ["claim_safety", "paper_readiness"], complete=complete),
    ]
    counts = {}
    for group in groups:
        counts[group["category"]] = sum(1 for item in group["items"] if item["missing"])
    return {
        "status": "formal_gate_artifacts_complete" if complete else "formal_gate_missing_artifacts_open",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "current_gate_summary": {
            "source_freshness_status": "source_freshness_clean" if complete else "source_freshness_risks_recorded_gate_still_blocked",
        },
        "formal_gate_handoff_index": _missing_artifacts_handoff_index(complete=complete, drift=drift),
        "missing_counts_by_category": counts,
        "missing_evidence_groups": groups,
    }


def _missing_artifacts_handoff_index(*, complete, drift=False):
    status = "formal_gate_evidence_ready_for_h01_h02_claim_gates" if complete else "blocked_until_f02_6_decision"
    next_action_id = "no_open_formal_gate_handoff_requirements" if complete else "record_f02_6_decision"
    return {
        "status": status,
        "next_action": {
            "action_id": next_action_id,
            "requires_dr_sun": not complete,
            "allowed_for_agent_now": False,
        },
        "local_training_allowed_now": False,
        "remote_training_allowed_now": complete or drift,
        "formal_result_material_allowed_now": bool(drift),
        "requirement_count": 5,
        "open_requirement_count": 0 if complete else 5,
    }


def _closure_checklist(*, complete, drift=False):
    ids = [
        "F02.6_decision",
        "preflight_source_fresh_regeneration",
        "approved_remote_preflight_and_packet",
        "gate3_remote_training_outputs",
        "gate3_formal_eval_outputs",
        "gate3_audit_pullback_hashes",
        "h01_h02_formal_acceptance",
        "claim_gate_regeneration",
    ]
    stage_blockers = [] if complete else ["requires_dr_sun_approval", "source_fresh_preflight_targets_open"]
    training_blockers = [] if complete else ["requires_dr_sun_approval", "source_fresh_preflight_targets_open", "remote_packet_not_ready"]
    payload = {
        "status": "formal_gate_closure_ready_for_result_audit" if complete else "formal_gate_closure_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "open_item_count": 0 if complete else len(ids),
        "training_artifacts_required": _artifacts(["train_final_model_zip", "train_summary_json", "train_training_manifest_json"], complete=complete),
        "evaluation_artifacts_required": _artifacts(["eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"], complete=complete),
        "acceptance_artifacts_required": _artifacts(["gate3_trial_manifest_json", "gate3_formal_audit_json", "pulled_back_checkpoint_hash_record"], complete=complete),
        "evaluation_acceptance_required": _artifacts(["h01_ready_for_formal_run", "h02_formal_output_acceptance"], complete=complete),
        "claim_gate_artifacts_required": _artifacts(["claim_safety", "paper_readiness"], complete=complete),
        "post_plan_remote_stage_summary": {
            "approved_remote_preflight": {
                "present": True,
                "status": "complete" if complete else "blocked",
                "allowed_now": complete,
                "runs_training": False,
                "runs_remote_preflight": True,
                "host": "gpu3070ti-relay",
                "blocked_by": stage_blockers,
            },
            "gate3_remote_training": {
                "present": True,
                "status": "complete" if complete else "blocked",
                "allowed_now": complete,
                "runs_training": True,
                "runs_remote_preflight": False,
                "host": "gpu3070ti-relay",
                "blocked_by": training_blockers,
            },
            "gate3_remote_audit_pullback": {
                "present": True,
                "status": "complete" if complete else "blocked",
                "allowed_now": complete,
                "runs_training": False,
                "runs_remote_preflight": False,
                "host": "gpu3070ti-relay",
                "blocked_by": training_blockers,
            },
        },
        "closure_checklist": [
            {
                "checklist_id": item,
                "complete": complete,
                "status": "complete" if complete else "blocked",
                "blocked_by": [] if complete else [f"{item}_blocked"],
            }
            for item in ids
        ],
    }
    if drift:
        payload["executes_commands"] = True
    return payload


def _decision_record(*, complete):
    return {
        "status": "approved" if complete else "pending_human_decision",
        "decider": "Dr Sun" if complete else None,
        "decision_note": "Approve obstacle-summary warm-start for source-fresh regeneration." if complete else None,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _decision_intake(*, complete):
    return {
        "status": "f02_6_decision_intake_closed_clean" if complete else "f02_6_decision_intake_pending_clean",
        "audit_issue_count": 0,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "current_state": {
            "record_status": "approved" if complete else "pending_human_decision",
            "record_decider": "Dr Sun" if complete else None,
            "effective_warm_start_decision": "approved_obstacle_summary" if complete else "pending",
            "next_blocked_lane": None if complete else "decision",
            "missing_deliverable_count": 0 if complete else 10,
            "status_report_local_training_allowed_now": False,
            "status_report_remote_preflight_allowed_now": complete,
            "status_report_remote_training_allowed_now": complete,
            "status_report_formal_claim_allowed_now": complete,
            "packet_authorization_status": "closed_dr_sun_decision" if complete else "blocked_until_dr_sun_decision",
            "packet_current_allowed_action_ids": [] if complete else ["record_f02_6_decision"],
            "packet_current_blocked_action_ids": []
            if complete
            else [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "packet_post_decision_routes_are_current_authorization": False,
            "packet_remote_preflight_allowed_now": complete,
            "packet_remote_training_allowed_now": complete,
            "packet_local_training_allowed_now": False,
            "packet_formal_claim_allowed_now": complete,
            "packet_paper_result_material_allowed_now": False,
        },
        "next_human_decision_request": {
            "status": "decision_recorded" if complete else "awaiting_dr_sun_decision",
            "decision_owner_required": "Dr Sun",
            "valid_decisions": [
                "approve_obstacle_summary_warm_start",
                "reject_obstacle_summary_warm_start",
            ],
            "required_record_fields": ["decision", "decider", "decision_note"],
            "current_allowed_action_ids": [] if complete else ["record_f02_6_decision"],
            "current_blocked_action_ids": []
            if complete
            else [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "post_decision_routes_are_current_authorization": False,
            "all_execution_disabled_now": not complete,
        },
        "decision_intake_contract": {
            "decision_owner_required": "Dr Sun",
            "valid_decisions": [
                "approve_obstacle_summary_warm_start",
                "reject_obstacle_summary_warm_start",
            ],
            "required_record_fields_for_non_pending_decision": [
                "decision",
                "decider",
                "decision_note",
            ],
            "record_command_templates": [
                {"decision": "approve_obstacle_summary_warm_start"},
                {"decision": "reject_obstacle_summary_warm_start"},
            ],
            "allowed_next_human_actions_from_gate_audit": [
                {"decision": "approve_obstacle_summary_warm_start"},
                {"decision": "reject_obstacle_summary_warm_start"},
            ],
        },
        "invalid_inputs": [
            {"input": "decider other than Dr Sun"},
            {"input": "local training output"},
        ],
        "post_decision_non_authorizations": [
            {"action": "local_training", "allowed_after_decision_record": False},
            {"action": "paper_formal_result_claim", "allowed_after_decision_record": False},
        ],
        "post_decision_route_matrix": [
            {
                "decision": "approve_obstacle_summary_warm_start",
                "next_lane_after_record": "source_fresh_regeneration",
                "allows_local_training_now": False,
                "allows_remote_preflight_now": False,
                "allows_remote_training_now": False,
                "allows_formal_claim_now": False,
                "requires_new_protocol_contract": False,
            },
            {
                "decision": "reject_obstacle_summary_warm_start",
                "next_lane_after_record": "protocol_redesign",
                "allows_local_training_now": False,
                "allows_remote_preflight_now": False,
                "allows_remote_training_now": False,
                "allows_formal_claim_now": False,
                "requires_new_protocol_contract": True,
            },
        ],
        "formal_gate_decision_impact_summary": {
            "summary_id": "module2_f02_6_formal_gate_decision_impact",
            "not_paper_result_material": True,
            "current_blocker": None if complete else "decision",
            "current_record_status": "approved" if complete else "pending_human_decision",
            "missing_deliverable_count": 0 if complete else 10,
            "current_allowed_action_ids": [] if complete else ["record_f02_6_decision"],
            "current_blocked_action_ids": []
            if complete
            else [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "decision_routes": [
                {
                    "decision": "approve_obstacle_summary_warm_start",
                    "next_lane_after_record": "source_fresh_regeneration",
                    "allows_local_training_now": False,
                    "allows_remote_preflight_now": False,
                    "allows_remote_training_now": False,
                    "allows_formal_claim_now": False,
                    "requires_new_protocol_contract": False,
                },
                {
                    "decision": "reject_obstacle_summary_warm_start",
                    "next_lane_after_record": "protocol_redesign",
                    "allows_local_training_now": False,
                    "allows_remote_preflight_now": False,
                    "allows_remote_training_now": False,
                    "allows_formal_claim_now": False,
                    "requires_new_protocol_contract": True,
                },
            ],
            "invariants_after_any_decision_record": {
                "decision_record_is_not_training_authorization": True,
                "decision_record_is_not_paper_result_material": True,
                "local_training_allowed_now": False,
                "remote_preflight_allowed_now": False,
                "remote_training_allowed_now": False,
                "formal_claim_allowed_now": False,
                "paper_result_material_allowed_now": False,
                "formal_training_still_requires": [
                    "source_freshness_audit",
                    "post_f02_6_regeneration_plan",
                    "post_f02_6_plan_audit",
                    "remote_formal_execution_packet_ready",
                    "approved_remote_preflight",
                ],
            },
        },
    }


def _remote_packet(*, complete, drift=False):
    step_blockers = [] if complete else ["requires_dr_sun_approval"]
    training_blockers = [] if complete else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    payload = {
        "status": "ready_for_remote_training_packet_execution" if complete else "blocked_until_f02_6_decision",
        "ready_to_run_remote_training": complete,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "formal_claim_allowed_before_audit": False,
        "execution_steps": {
            "sync_to_remote": {
                "allowed_now": complete,
                "runs_training": False,
                "blocked_by": step_blockers,
            },
            "run_remote_preflight": {
                "allowed_now": complete,
                "runs_training": False,
                "blocked_by": step_blockers,
            },
            "run_remote_training": {
                "allowed_now": complete,
                "runs_training": True,
                "blocked_by": training_blockers,
            },
            "run_remote_audit": {
                "allowed_now": complete,
                "runs_training": False,
                "blocked_by": training_blockers,
            },
        },
        "remote_preflight_requirements": _remote_preflight_requirements(complete=complete),
        "remote_preflight_requirement_counts": {"satisfied": 4} if complete else {"blocked_missing_preflight": 2, "satisfied": 2},
        "post_run_acceptance_requirements": _post_run_acceptance_requirements(complete=complete),
        "post_run_acceptance_requirement_counts": {"satisfied": 4} if complete else {"blocked_until_remote_audit": 4},
    }
    if drift:
        payload["formal_claim_allowed_before_audit"] = True
    return payload


def _remote_preflight_requirements(*, complete):
    return [
        _remote_requirement(
            "f02_6_decision_closed_for_preflight",
            "decision",
            "satisfied" if complete else "blocked_missing_preflight",
            complete=complete,
            execution_allowed_now=complete,
            blocked_by=[] if complete else ["requires_dr_sun_approval"],
        ),
        _remote_requirement(
            "approved_remote_preflight_manifest",
            "remote_preflight",
            "satisfied" if complete else "blocked_missing_preflight",
            complete=complete,
            execution_allowed_now=complete,
            blocked_by=[] if complete else ["warm_start_decision_pending"],
        ),
        _remote_requirement(
            "remote_preflight_protocol_contract",
            "remote_preflight",
            "satisfied",
            complete=True,
            execution_allowed_now=complete,
            blocked_by=[],
        ),
        _remote_requirement(
            "remote_preflight_command_packetized",
            "remote_preflight",
            "satisfied",
            complete=True,
            execution_allowed_now=complete,
            blocked_by=[] if complete else ["requires_dr_sun_approval"],
        ),
    ]


def _post_run_acceptance_requirements(*, complete):
    status = "satisfied" if complete else "blocked_until_remote_audit"
    return [
        _remote_requirement(
            "pullback_expected_artifacts_complete",
            "pullback",
            status,
            complete=complete,
            execution_allowed_now=False,
            remote_training_ready_now=complete,
        ),
        _remote_requirement(
            "checkpoint_hash_manifest_recorded",
            "pullback",
            status,
            complete=complete,
            execution_allowed_now=False,
            remote_training_ready_now=complete,
        ),
        _remote_requirement(
            "gate3_formal_audit_accepts_remote_run",
            "acceptance",
            status,
            complete=complete,
            execution_allowed_now=False,
            remote_training_ready_now=complete,
        ),
        _remote_requirement(
            "h01_h02_regenerated_from_audited_checkpoint",
            "evaluation_acceptance",
            status,
            complete=complete,
            execution_allowed_now=False,
            remote_training_ready_now=complete,
        ),
    ]


def _remote_requirement(
    requirement_id,
    phase,
    status,
    *,
    complete,
    execution_allowed_now,
    blocked_by=None,
    remote_training_ready_now=None,
):
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": status,
        "complete": complete,
        "execution_allowed_now": execution_allowed_now,
        "remote_training_ready_now": remote_training_ready_now,
        "required_before": "formal_gate_close",
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "blocked_by": [] if blocked_by is None else blocked_by,
        "acceptable_evidence": [f"{requirement_id}_acceptable_evidence"],
        "invalid_substitutes": [f"{requirement_id}_invalid_substitute"],
    }


def _h01_manifest(*, complete):
    return {
        "status": "ready_for_formal_run" if complete else "blocked_pending_decisions",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _h02_acceptance(*, complete):
    requirements = _h02_formal_acceptance_requirements(complete=complete)
    status_counts = {"satisfied": 4} if complete else {"satisfied": 1, "blocked_formal_acceptance": 3}
    return {
        "status": "formal_output_accepted" if complete else "blocked_formal_output_acceptance",
        "formal_output_accepted": complete,
        "paper_result_input_allowed": complete,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "formal_acceptance_requirements": requirements,
        "formal_acceptance_requirement_counts": status_counts,
    }


def _h02_formal_acceptance_requirements(*, complete):
    return [
        _h02_formal_acceptance_requirement(
            "h01_schema_and_h02_output_schema_match",
            "schema_acceptance",
            complete=True,
            status="satisfied",
            paper_result_input_allowed_now=complete,
        ),
        _h02_formal_acceptance_requirement(
            "h02_formal_scope_and_scale_match_h01",
            "formal_scope",
            complete=complete,
            status="satisfied" if complete else "blocked_formal_acceptance",
            paper_result_input_allowed_now=complete,
        ),
        _h02_formal_acceptance_requirement(
            "gate3_audit_and_pullback_acceptance",
            "remote_acceptance",
            complete=complete,
            status="satisfied" if complete else "blocked_formal_acceptance",
            paper_result_input_allowed_now=complete,
        ),
        _h02_formal_acceptance_requirement(
            "ppo_rows_and_checkpoint_hash_present",
            "result_rows",
            complete=complete,
            status="satisfied" if complete else "blocked_formal_acceptance",
            paper_result_input_allowed_now=complete,
        ),
    ]


def _h02_formal_acceptance_requirement(
    requirement_id,
    phase,
    *,
    complete,
    status,
    paper_result_input_allowed_now,
):
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": status,
        "complete": complete,
        "paper_result_input_allowed_now": paper_result_input_allowed_now,
        "required_before": "paper_result_gate",
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "acceptable_evidence": [f"{requirement_id}_acceptable_evidence"],
        "invalid_substitutes": [f"{requirement_id}_invalid_substitute"],
    }


def _claim_safety(*, complete, drift=False):
    return {
        "status": "formal_performance_claims_allowed" if complete else "blocked_formal_performance_claims",
        "formal_performance_claim_allowed": complete,
        "local_training_allowed": False,
        "formal_claim_allowed": bool(drift),
    }


def _paper_readiness(*, complete):
    return {
        "status": "formal_results_ready" if complete else "partial_methods_ready_results_blocked",
        "formal_results_ready": complete,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _remaining_deliverables(*, complete):
    category_artifacts = {
        "training": [
            "train_final_model_zip",
            "train_summary_json",
            "train_training_manifest_json",
        ],
        "evaluation": [
            "eval_gate3_eval_episodes_csv",
            "eval_gate3_summary_json",
        ],
        "acceptance": [
            "gate3_trial_manifest_json",
            "gate3_formal_audit_json",
            "pulled_back_checkpoint_hash_record",
        ],
        "formal_acceptance": [
            "h01_ready_for_formal_run",
            "h02_formal_output_acceptance",
        ],
    }
    matrix = [
        _remaining_deliverable_row(category, artifact_id, complete=complete)
        for category, artifact_ids in category_artifacts.items()
        for artifact_id in artifact_ids
    ]
    category_counts = {
        category: {
            "item_count": len(artifact_ids),
            "missing_count": 0 if complete else len(artifact_ids),
            "present_count": len(artifact_ids) if complete else 0,
        }
        for category, artifact_ids in category_artifacts.items()
    }
    return {
        "status": "formal_gate_deliverables_ready_for_claim_audit" if complete else "formal_gate_deliverables_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "missing_deliverable_count": 0 if complete else len(matrix),
        "category_counts": category_counts,
        "missing_counts_by_formal_category": {
            category: 0 if complete else len(artifact_ids)
            for category, artifact_ids in category_artifacts.items()
        },
        "missing_matrix_ids_by_formal_category": {
            category: []
            if complete
            else [f"{category}:{artifact_id}" for artifact_id in artifact_ids]
            for category, artifact_ids in category_artifacts.items()
        },
        "next_blocked_lane": None if complete else "decision",
        "h01_status": "ready_for_formal_run" if complete else "blocked_pending_decisions",
        "h02_status": "formal_output_accepted" if complete else "blocked_formal_output_acceptance",
        "h02_formal_output_accepted": complete,
        "h02_paper_result_input_allowed": complete,
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": complete,
            "remote_training_allowed_now": complete,
            "formal_h01_evaluation_allowed_now": complete,
            "formal_h02_acceptance_allowed_now": complete,
            "formal_claim_allowed_now": complete,
        },
        "deliverable_acceptance_matrix": matrix,
        "deliverable_gap_summary": _remaining_deliverable_gap_summary(
            category_artifacts=category_artifacts,
            matrix=matrix,
            complete=complete,
        ),
        "deliverable_unlock_chain": _remaining_deliverable_unlock_chain(matrix, complete=complete),
        "proof_command_plan": _remaining_deliverable_proof_command_plan(matrix),
    }


def _source_freshness(*, complete):
    return {
        "status": "source_freshness_clean_current" if complete else "source_freshness_risks_recorded_gate_still_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "regeneration_required_before_remote_formal_execution": not complete,
        "blocking_regeneration_required_before_remote_formal_execution": not complete,
        "commit_lag_summary": {
            "records_with_non_self_changed_paths_since_source": 0 if complete else 19,
            "records_with_self_artifact_only_lag": 0,
        },
    }


def _remaining_deliverable_proof_command_plan(matrix):
    return {
        "plan_id": "module2_formal_gate_local_read_only_proof_commands",
        "execution_boundary": "local_read_only_after_formal_remote_pullback",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_matrix_rows": len(matrix),
        "total_proof_command_count": sum(len(row["proof_commands"]) for row in matrix),
        "rows": [
            {
                "matrix_id": row["matrix_id"],
                "category": row["category"],
                "artifact_id": row["artifact_id"],
                "expected_path": row["expected_path"],
                "proof_command_count": len(row["proof_commands"]),
                "proof_command_ids": [command["command_id"] for command in row["proof_commands"]],
            }
            for row in matrix
        ],
    }


def _formal_gate_proof_audit(*, complete):
    matrix = _remaining_deliverables(complete=complete)["deliverable_acceptance_matrix"]
    remaining = _remaining_deliverables(complete=complete)
    results = []
    for row in matrix:
        for command in row["proof_commands"]:
            if complete:
                status = "passed"
            elif row["category"] == "formal_acceptance" and command["command_id"].endswith("_exists"):
                status = "passed"
            elif row["category"] == "formal_acceptance":
                status = "failed"
            else:
                status = "blocked_missing_artifact"
            results.append(
                {
                    "matrix_id": row["matrix_id"],
                    "category": row["category"],
                    "artifact_id": row["artifact_id"],
                    "command_id": command["command_id"],
                    "status": status,
                    "expected_path": row["expected_path"],
                    "expected_evidence": command.get("expected_evidence", "exit_code=0"),
                    "command_was_executed": False,
                    "diagnostic": f"{command['command_id']} {status}",
                }
            )
    category_status_counts = {}
    for result in results:
        counts = category_status_counts.setdefault(
            result["category"],
            {"passed": 0, "failed": 0, "blocked_missing_artifact": 0},
        )
        counts[result["status"]] += 1
    return {
        "artifact_name": "module2_formal_gate_proof_audit",
        "status": "formal_gate_proof_audit_passed" if complete else "formal_gate_proof_audit_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "proof_command_plan_id": "module2_formal_gate_local_read_only_proof_commands",
        "execution_boundary": "local_read_only_after_formal_remote_pullback",
        "total_matrix_rows": len(matrix),
        "total_proof_command_count": len(results),
        "declared_total_proof_command_count": len(results),
        "passed_proof_command_count": sum(1 for result in results if result["status"] == "passed"),
        "failed_proof_command_count": sum(1 for result in results if result["status"] == "failed"),
        "blocked_proof_command_count": sum(
            1 for result in results if result["status"] == "blocked_missing_artifact"
        ),
        "category_status_counts": category_status_counts,
        "blockers": []
        if complete
        else [
            "missing_formal_training_artifacts",
            "missing_formal_evaluation_artifacts",
            "missing_formal_acceptance_artifacts",
            "failed_formal_h01_h02_acceptance_artifacts",
        ],
        "input_safety_issue_count": 0,
        "input_safety_issues": [],
        "remaining_deliverables_top_level_summary": {
            "present": True,
            "missing_counts_by_formal_category": remaining["missing_counts_by_formal_category"],
            "missing_matrix_ids_by_formal_category": remaining["missing_matrix_ids_by_formal_category"],
            "next_blocked_lane": remaining["next_blocked_lane"],
            "h01_status": remaining["h01_status"],
            "h02_status": remaining["h02_status"],
            "h02_formal_output_accepted": remaining["h02_formal_output_accepted"],
            "h02_paper_result_input_allowed": remaining["h02_paper_result_input_allowed"],
        },
        "proof_command_results": results,
        "proof_command_results_by_id": {result["command_id"]: result for result in results},
        "formal_gate_missing_evidence_summary": _formal_gate_missing_evidence_summary(results),
    }


def _formal_gate_missing_evidence_summary(results):
    summary = {
        "training": {"missing_artifact_ids": [], "failed_artifact_ids": []},
        "evaluation": {"missing_artifact_ids": [], "failed_artifact_ids": []},
        "acceptance": {"missing_artifact_ids": [], "failed_artifact_ids": []},
        "formal_acceptance": {"missing_artifact_ids": [], "failed_artifact_ids": []},
    }
    for result in results:
        payload = summary[result["category"]]
        if result["status"] == "blocked_missing_artifact":
            if result["artifact_id"] not in payload["missing_artifact_ids"]:
                payload["missing_artifact_ids"].append(result["artifact_id"])
        elif result["status"] == "failed":
            if result["artifact_id"] not in payload["failed_artifact_ids"]:
                payload["failed_artifact_ids"].append(result["artifact_id"])
    return summary


def _remaining_deliverable_gap_summary(*, category_artifacts, matrix, complete):
    stage_by_category = {
        "training": "gate3_remote_training",
        "evaluation": "gate3_remote_audit_pullback",
        "acceptance": "gate3_remote_audit_pullback",
        "formal_acceptance": "regenerate_h01_h02_formal_artifacts",
    }
    rows_by_category = {}
    for row in matrix:
        rows_by_category.setdefault(row["category"], []).append(row)
    categories = []
    for category, artifact_ids in category_artifacts.items():
        rows = rows_by_category[category]
        missing_rows = [row for row in rows if row["missing"]]
        categories.append(
            {
                "category": category,
                "status": "complete" if complete else "blocked",
                "missing_count": 0 if complete else len(artifact_ids),
                "present_count": len(artifact_ids) if complete else 0,
                "responsible_stage_id": stage_by_category[category],
                "responsible_stage_allowed_now": complete,
                "responsible_stage_blocked_by": [] if complete else ["remote_packet_not_ready"],
                "next_required_evidence": [f"{category}_acceptable_evidence"],
                "missing_artifacts": [
                    {
                        "matrix_id": row["matrix_id"],
                        "artifact_id": row["artifact_id"],
                        "expected_path": row["expected_path"],
                        "current_state": row["current_state"],
                        "missing_reason": row["missing_reason"],
                        "acceptance_predicate_count": len(row["acceptance_predicates"]),
                        "proof_command_count": len(row["proof_commands"]),
                        "proof_command_ids": [command["command_id"] for command in row["proof_commands"]],
                        "invalid_substitutes": row["invalid_substitutes"],
                    }
                    for row in missing_rows
                ],
            }
        )
    return {
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "total_missing_deliverables": 0 if complete else len(matrix),
        "open_category_count": 0 if complete else len(category_artifacts),
        "category_order": list(category_artifacts),
        "categories": categories,
    }


def _remaining_deliverable_row(category, artifact_id, *, complete):
    stage_by_category = {
        "training": "gate3_remote_training",
        "evaluation": "gate3_remote_audit_pullback",
        "acceptance": "gate3_remote_audit_pullback",
        "formal_acceptance": "regenerate_h01_h02_formal_artifacts",
    }
    return {
        "matrix_id": f"{category}:{artifact_id}",
        "category": category,
        "artifact_id": artifact_id,
        "expected_path": f"0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/{artifact_id}",
        "current_exists": complete,
        "current_state": "present" if complete else "missing",
        "missing": not complete,
        "missing_reason": "" if complete else "required formal-gate deliverable",
        "responsible_stage_id": stage_by_category[category],
        "responsible_stage_status": "ready" if complete else "blocked",
        "responsible_stage_allowed_now": complete,
        "responsible_stage_blocked_by": [] if complete else ["remote_packet_not_ready"],
        "acceptance_predicates": [f"{artifact_id}_acceptance_predicate"],
        "proof_commands": [
            {
                "command_id": f"{artifact_id}_exists",
                "command": f"python -c \"from pathlib import Path; assert Path('{artifact_id}').exists()\"",
                "execution_boundary": "local_read_only_after_formal_remote_pullback",
            },
            {
                "command_id": f"{artifact_id}_schema",
                "command": f"python -c \"print('{artifact_id}_schema')\"",
                "execution_boundary": "local_read_only_after_formal_remote_pullback",
            },
        ],
        "acceptable_evidence": [f"{artifact_id}_acceptable_evidence"],
        "invalid_substitutes": [f"{artifact_id}_invalid_substitute"],
        "execution_boundary": "read_only_no_execution",
    }


def _handoff_bundle(*, complete, drift=False):
    step_blockers = [] if complete else ["requires_dr_sun_approval"]
    training_blockers = [] if complete else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    payload = {
        "status": "ready_for_manual_remote_execution_review" if complete else "blocked_until_f02_6_decision",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "current_state": {
            "decision_status": "approved" if complete else "pending_human_decision",
            "ready_to_run_remote_training": complete,
            "transition_gate_status": "f02_6_transition_gate_audit_passed",
            "transition_gate_audit_issue_count": 0,
        },
        "permissions_now": {
            "remote_preflight_allowed_now": complete,
            "remote_training_allowed_now": complete,
            "formal_claim_allowed_now": complete,
            "local_training_allowed_now": False,
        },
        "next_handoff_action": {
            "action_id": "manual_execution_review" if complete else "record_f02_6_decision",
            "requires_dr_sun": not complete,
            "allowed_for_agent_now": False,
        },
        "remote_execution_steps": {
            "sync_to_remote": _handoff_step(complete, False, step_blockers),
            "run_remote_preflight": _handoff_step(complete, False, step_blockers),
            "run_remote_training": _handoff_step(complete, True, training_blockers),
            "run_remote_audit": _handoff_step(complete, False, training_blockers),
        },
        "formal_gate_requirements": [
            _handoff_requirement("training_remote_ppo_checkpoint", "training", complete=complete, stage_id="gate3_remote_training"),
            _handoff_requirement("evaluation_gate3_episode_outputs", "evaluation", complete=complete, stage_id="gate3_remote_audit_pullback"),
            _handoff_requirement("acceptance_remote_pullback_and_audit", "acceptance", complete=complete, stage_id="gate3_remote_audit_pullback"),
            _handoff_requirement(
                "h01_h02_formal_evaluation_acceptance",
                "evaluation_acceptance",
                complete=complete,
                stage_id="regenerate_h01_h02_formal_artifacts",
            ),
        ],
        "safety_issue_count": 0,
        "safety_issues": [],
    }
    if drift:
        payload["safety_issue_count"] = 1
        payload["safety_issues"] = [{"issue_id": "synthetic_handoff_drift"}]
    return payload


def _handoff_step(allowed, runs_training, blockers):
    return {
        "allowed_now": allowed,
        "runs_training": runs_training,
        "blocked_by": blockers,
    }


def _handoff_requirement(requirement_id, phase, *, complete, stage_id):
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": "satisfied" if complete else "blocked_missing_outputs",
        "complete": complete,
        "execution_allowed_now": False,
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "responsible_stage_id": stage_id,
        "responsible_stage_status": "ready" if complete else "blocked",
        "responsible_stage_allowed_now": complete,
        "responsible_stage_blocked_by": [] if complete else ["remote_packet_not_ready"],
        "responsible_stage_evidence_paths": [
            "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip"
        ],
    }


def _group(group_id, category, artifact_ids, *, complete):
    return {
        "group_id": group_id,
        "category": category,
        "complete": complete,
        "blocked_by": [] if complete else artifact_ids,
        "items": [
            {
                "artifact_id": artifact_id,
                "path": f"0_trials/module2/{artifact_id}.json",
                "exists": complete,
                "state": "present" if complete else "missing",
                "missing": not complete,
                "reason": "" if complete else "required before formal status can close",
            }
            for artifact_id in artifact_ids
        ],
    }


def _artifacts(artifact_ids, *, complete):
    return [
        {
            "artifact_id": artifact_id,
            "path": f"0_trials/module2/{artifact_id}.json",
            "exists": complete,
            "state": "present" if complete else "missing",
            "missing": not complete,
            "reason": "" if complete else "required before formal status can close",
        }
        for artifact_id in artifact_ids
    ]


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
