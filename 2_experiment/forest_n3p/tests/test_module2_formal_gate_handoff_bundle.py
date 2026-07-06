import json
from importlib import import_module


def test_formal_gate_handoff_bundle_blocks_pending_decision_without_execution(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate handoff bundle builder: {exc}") from exc

    manifest = builder.build_manifest(_config(tmp_path, complete=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_handoff_bundle"
    assert manifest["status"] == "blocked_until_f02_6_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["inputs"]["decision_intake"].endswith("decision_intake.json")
    assert manifest["next_handoff_action"]["action_id"] == "record_f02_6_decision"
    assert manifest["next_handoff_action"]["requires_dr_sun"] is True
    assert manifest["next_handoff_action"]["allowed_for_agent_now"] is False
    assert manifest["current_state"]["effective_next_action_id"] == "record_f02_6_decision"
    assert manifest["current_state"]["effective_next_action_requires_dr_sun"] is True
    assert manifest["current_state"]["legacy_f02_6_decision_action_ids"] == ["record_f02_6_decision"]
    assert manifest["current_state"]["legacy_f02_6_decision_superseded_by_protocol_lane"] is False
    single = manifest["single_next_action_index"]
    assert single["index_id"] == "module2_formal_gate_single_next_action_index"
    assert single["status"] == "awaiting_dr_sun_f02_6_decision"
    assert single["single_current_human_entry"] is True
    assert single["next_action_id"] == "record_f02_6_decision"
    assert single["decision_owner_required"] == "Dr Sun"
    assert single["valid_decisions"] == [
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    ]
    assert single["required_record_fields"] == ["decision", "decider", "decision_note"]
    assert single["current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert single["current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert single["legacy_f02_6_decision_action_ids"] == ["record_f02_6_decision"]
    assert single["legacy_f02_6_decision_superseded_by_protocol_lane"] is False
    assert single["post_decision_routes_are_current_authorization"] is False
    assert single["all_execution_disabled_now"] is True
    assert single["record_command_template_count"] == 2
    assert all("build_module2_f02_6_decision_record" in item["command"] for item in single["record_command_templates"])
    assert all("run_rl_rs_gate3_trial" not in item["command"] for item in single["record_command_templates"])
    assert all(item["execution_boundary"] == "local_decision_record_only" for item in single["record_command_templates"])
    assert all(item["allowed_for_agent_now"] is False for item in single["record_command_templates"])
    assert single["local_training_allowed_now"] is False
    assert single["remote_preflight_allowed_now"] is False
    assert single["remote_training_allowed_now"] is False
    assert single["formal_claim_allowed_now"] is False
    assert single["paper_result_material_allowed_now"] is False
    assert single["missing_deliverable_count"] == 10
    assert single["missing_by_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert single["source_freshness_status"] == "source_freshness_risks_recorded_gate_still_blocked"
    assert single["source_freshness_blocking_regeneration_required"] is True
    assert single["approved_route_next_lane"] == "source_fresh_regeneration"
    assert single["rejected_route_next_lane"] == "protocol_redesign"
    assert "approved_remote_preflight" in single["after_approval_still_requires"]
    assert manifest["current_state"]["decision_status"] == "pending_human_decision"
    assert manifest["current_state"]["transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["current_state"]["source_freshness_status"] == "source_freshness_risks_recorded_gate_still_blocked"
    assert manifest["current_state"]["source_freshness_regeneration_required"] is True
    assert manifest["current_state"]["source_freshness_non_self_changed_records"] == 18
    assert manifest["current_state"]["source_freshness_self_artifact_only_lag_records"] == 1
    assert manifest["current_state"]["next_blocked_lane"] == "decision"
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is False
    assert manifest["inputs"]["source_freshness_audit"].endswith("source_freshness.json")
    route_summary = manifest["f02_6_route_handoff_summary"]
    assert route_summary["present"] is True
    assert route_summary["post_decision_route_count"] == 2
    assert set(route_summary["post_decision_route_decisions"]) == {
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    }
    assert route_summary["approved_route_next_lane"] == "source_fresh_regeneration"
    assert route_summary["approved_route_allows_remote_training_now"] is False
    assert route_summary["rejected_route_next_lane"] == "protocol_redesign"
    assert route_summary["rejected_route_requires_new_protocol_contract"] is True
    assert route_summary["decision_impact_present"] is True
    assert route_summary["decision_record_is_not_training_authorization"] is True
    assert route_summary["decision_record_is_not_paper_result_material"] is True
    assert route_summary["decision_impact_remote_preflight_allowed_now"] is False
    assert route_summary["decision_impact_remote_training_allowed_now"] is False
    assert route_summary["decision_impact_formal_claim_allowed_now"] is False
    assert route_summary["decision_impact_paper_result_material_allowed_now"] is False
    assert "approved_remote_preflight" in route_summary["decision_impact_formal_training_still_requires"]
    matrix_summary = manifest["f02_6_decision_evidence_matrix_handoff_summary"]
    assert matrix_summary["present"] is True
    assert matrix_summary["matrix_id"] == "module2_f02_6_decision_evidence_matrix"
    assert matrix_summary["status"] == "ready_for_dr_sun_decision_not_authorization"
    assert matrix_summary["route_count"] == 2
    assert set(matrix_summary["route_decisions"]) == {
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    }
    assert matrix_summary["required_evidence_count"] == 7
    assert matrix_summary["satisfied_required_evidence_count"] == 7
    assert matrix_summary["missing_required_evidence_count"] == 0
    assert matrix_summary["global_invalid_substitute_count"] == 4
    assert matrix_summary["authorization_flags"]["remote_training_allowed_now"] is False
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 4
    assert manifest["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] == 3
    proof_summary = manifest["status_report_proof_audit_deliverables_summary"]
    assert proof_summary["present"] is True
    assert proof_summary["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert proof_summary["missing_matrix_ids_by_formal_category"]["training"] == [
        "training:train_final_model_zip",
        "training:train_summary_json",
        "training:train_training_manifest_json",
    ]
    assert proof_summary["missing_matrix_ids_by_formal_category"]["formal_acceptance"] == [
        "formal_acceptance:h01_ready_for_formal_run",
        "formal_acceptance:h02_formal_output_acceptance",
    ]
    assert proof_summary["next_blocked_lane"] == "decision"
    assert proof_summary["h01_status"] == "blocked_pending_decisions"
    assert proof_summary["h02_status"] == "blocked_formal_output_acceptance"
    assert proof_summary["h02_formal_output_accepted"] is False
    assert proof_summary["h02_paper_result_input_allowed"] is False
    assert manifest["post_plan_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["remote_execution_steps"]["sync_to_remote"]["allowed_now"] is False
    assert manifest["remote_execution_steps"]["run_remote_training"]["allowed_now"] is False
    assert "requires_dr_sun_approval" in manifest["remote_execution_steps"]["run_remote_training"]["blocked_by"]
    assert len(manifest["formal_gate_requirements"]) == 4
    formal_reqs = {req["requirement_id"]: req for req in manifest["formal_gate_requirements"]}
    assert formal_reqs["training_remote_ppo_checkpoint"]["responsible_stage_id"] == "gate3_remote_training"
    assert formal_reqs["training_remote_ppo_checkpoint"]["responsible_stage_status"] == "blocked"
    assert formal_reqs["training_remote_ppo_checkpoint"]["responsible_stage_allowed_now"] is False
    assert "remote_packet_not_ready" in formal_reqs["training_remote_ppo_checkpoint"]["responsible_stage_blocked_by"]
    assert "final_model.zip" in ";".join(formal_reqs["training_remote_ppo_checkpoint"]["responsible_stage_evidence_paths"])
    assert formal_reqs["evaluation_gate3_episode_outputs"]["responsible_stage_id"] == "gate3_remote_audit_pullback"
    assert formal_reqs["acceptance_remote_pullback_and_audit"]["responsible_stage_id"] == "gate3_remote_audit_pullback"
    assert formal_reqs["h01_h02_formal_evaluation_acceptance"]["responsible_stage_id"] == "regenerate_h01_h02_formal_artifacts"
    assert len(manifest["h02_formal_acceptance_requirements"]) == 4
    assert len(manifest["post_run_expected_artifacts"]) == 7
    assert manifest["safety_issue_count"] == 0

    stages = {stage["stage_id"]: stage for stage in manifest["handoff_stages"]}
    assert stages["f02_6_decision_record"]["source_allowed_now"] is True
    assert stages["gate3_remote_training"]["runs_training"] is True
    assert stages["gate3_remote_training"]["source_allowed_now"] is False
    assert stages["gate3_remote_training"]["host"] == "gpu3070ti-relay"
    assert "remote_packet_not_ready" in stages["gate3_remote_training"]["blocked_by"]


def test_formal_gate_handoff_bundle_marks_manual_review_when_sources_allow_remote_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")

    manifest = builder.build_manifest(_config(tmp_path, complete=True))

    assert manifest["status"] == "ready_for_manual_remote_execution_review"
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is True
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is True
    assert manifest["single_next_action_index"]["status"] == "follow_handoff_stages"
    assert manifest["single_next_action_index"]["single_current_human_entry"] is False
    assert manifest["single_next_action_index"]["record_command_templates"] == []
    assert manifest["single_next_action_index"]["remote_training_allowed_now"] is True
    assert manifest["status_report_proof_audit_deliverables_summary"][
        "missing_counts_by_formal_category"
    ] == {
        "training": 0,
        "evaluation": 0,
        "acceptance": 0,
        "formal_acceptance": 0,
    }
    assert manifest["remote_execution_steps"]["run_remote_training"]["allowed_now"] is True
    assert "ssh gpu3070ti-relay" in manifest["remote_execution_steps"]["run_remote_training"]["command"]
    assert manifest["safety_issue_count"] == 0

    stages = {stage["stage_id"]: stage for stage in manifest["handoff_stages"]}
    assert stages["gate3_remote_training"]["source_allowed_now"] is True
    assert stages["gate3_remote_training"]["runs_training"] is True
    assert stages["gate3_remote_training"]["host"] == "gpu3070ti-relay"


def test_formal_gate_handoff_bundle_blocks_remote_when_protocol_lane_pending(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=True, protocol_pending=True)
    decision_intake = json.loads(config.decision_intake_path.read_text(encoding="utf-8"))
    decision_intake["next_human_decision_request"]["current_allowed_action_ids"] = ["record_f02_6_decision"]
    config.decision_intake_path.write_text(json.dumps(decision_intake), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_until_protocol_lane_decision"
    assert manifest["current_state"]["protocol_lane_status"] == "protocol_lane_status_blocked_pending_lane_decision"
    assert manifest["current_state"]["next_blocked_lane"] == "protocol_lane_decision"
    assert manifest["current_state"]["ready_to_run_remote_training"] is False
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["next_handoff_action"]["action_id"] == "record_protocol_lane_decision"
    assert manifest["next_handoff_action"]["requires_dr_sun"] is True
    assert manifest["current_state"]["effective_next_action_id"] == "record_protocol_lane_decision"
    assert manifest["current_state"]["effective_next_action_requires_dr_sun"] is True
    assert manifest["current_state"]["legacy_f02_6_decision_action_ids"] == ["record_f02_6_decision"]
    assert manifest["current_state"]["legacy_f02_6_decision_superseded_by_protocol_lane"] is True
    protocol = manifest["protocol_lane_status_summary"]
    assert protocol["next_success_attempt_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert protocol["next_success_attempt_artifact_ids_by_category"] == {
        "contract": ["new_or_revised_research_contract"],
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
        "formal_acceptance": ["h02_formal_output_acceptance"],
    }
    assert protocol["next_success_attempt_artifact_expected_paths_by_id"]["train_final_model_zip"] == (
        "0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip"
    )
    assert protocol["next_success_attempt_artifact_expected_paths_by_id"]["h02_formal_output_acceptance"] == (
        "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json"
    )
    assert "remote-produced PPO checkpoint" in protocol[
        "next_success_attempt_artifact_proof_requirements_by_id"
    ]["train_final_model_zip"]
    assert protocol["next_success_attempt_artifact_invalid_substitutes_by_id"]["train_final_model_zip"] == [
        "local PPO training output",
        "failed warm-start checkpoint",
        "checkpoint without manifest or hash provenance",
    ]
    assert protocol["next_success_attempt_artifact_invalid_substitutes_by_id"]["h02_formal_output_acceptance"] == [
        "blocked H02 acceptance",
        "formal-looking smoke table",
        "PPO rows without checkpoint hash",
    ]
    assert protocol["post_decision_contract_plan_shared_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert protocol["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True
    assert protocol[
        "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"
    ] is True
    single = manifest["single_next_action_index"]
    assert single["status"] == "awaiting_dr_sun_protocol_lane_decision"
    assert single["single_current_human_entry"] is True
    assert single["next_action_id"] == "record_protocol_lane_decision"
    assert single["valid_decisions"] == [
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    ]
    assert single["current_allowed_action_ids"] == ["record_protocol_lane_decision"]
    assert single["current_blocked_action_ids"] == [
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    ]
    assert single["legacy_f02_6_decision_action_ids"] == ["record_f02_6_decision"]
    assert single["legacy_f02_6_decision_superseded_by_protocol_lane"] is True
    assert single["all_execution_disabled_now"] is True
    assert single["remote_preflight_allowed_now"] is False
    assert single["remote_training_allowed_now"] is False
    assert single["formal_claim_allowed_now"] is False
    assert single["paper_result_material_allowed_now"] is False
    assert manifest["remote_execution_steps"]["run_remote_training"]["allowed_now"] is False
    assert "protocol_lane_decision_pending" in manifest["remote_execution_steps"]["run_remote_training"]["blocked_by"]
    stages = {stage["stage_id"]: stage for stage in manifest["handoff_stages"]}
    assert stages["approved_remote_preflight"]["source_allowed_now"] is False
    assert stages["gate3_remote_training"]["source_allowed_now"] is False
    assert "protocol_lane_decision_pending" in stages["gate3_remote_training"]["blocked_by"]
    assert manifest["safety_issue_count"] == 0


def test_formal_gate_handoff_bundle_points_to_contract_draft_after_protocol_lane_recorded(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=True, protocol_pending=False)

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_formal_gate_handoff"
    assert manifest["current_state"]["protocol_lane_status"] == "protocol_lane_status_ready_for_contract_draft"
    assert manifest["current_state"]["next_blocked_lane"] == "new_or_revised_contract"
    assert manifest["current_state"]["protocol_lane_selected_lane_id"] == "hybrid_ppo_analytic_fallback"
    assert manifest["next_handoff_action"]["action_id"] == "draft_new_or_revised_contract_after_lane_decision"
    assert manifest["next_handoff_action"]["requires_dr_sun"] is False
    assert manifest["current_state"]["effective_next_action_id"] == "draft_new_or_revised_contract_after_lane_decision"
    assert manifest["current_state"]["legacy_f02_6_decision_superseded_by_protocol_lane"] is True

    single = manifest["single_next_action_index"]
    assert single["status"] == "awaiting_selected_lane_contract_draft"
    assert single["single_current_human_entry"] is False
    assert single["next_action_id"] == "draft_new_or_revised_contract_after_lane_decision"
    assert single["selected_lane_id"] == "hybrid_ppo_analytic_fallback"
    assert single["current_allowed_action_ids"] == ["draft_new_or_revised_contract_after_lane_decision"]
    assert single["all_execution_disabled_now"] is True
    assert single["remote_preflight_allowed_now"] is False
    assert single["remote_training_allowed_now"] is False
    assert single["formal_claim_allowed_now"] is False
    assert single["paper_result_material_allowed_now"] is False
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False
    assert manifest["safety_issue_count"] == 0


def test_formal_gate_handoff_bundle_rejects_protocol_lane_next_artifact_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=True, protocol_pending=True)
    protocol = json.loads(config.protocol_lane_status_report_path.read_text(encoding="utf-8"))
    current = protocol["current_status"]
    current["next_success_attempt_artifact_category_counts"]["training"] = 2
    current["next_success_attempt_artifact_ids_by_category"]["training"] = ["train_final_model_zip"]
    current["next_success_attempt_artifact_expected_paths_by_id"]["train_final_model_zip"] = (
        "0_trials/wrong/final_model.zip"
    )
    current["next_success_attempt_artifact_proof_requirements_by_id"]["train_summary_json"] = ""
    current["next_success_attempt_artifact_invalid_substitutes_by_id"]["train_final_model_zip"] = [
        "local PPO training output"
    ]
    current["post_decision_contract_plan_shared_artifact_category_counts"]["evaluation"] = 1
    current["old_failed_run_artifacts_invalid_for_next_success_attempt"] = False
    current["post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"] = False
    config.protocol_lane_status_report_path.write_text(json.dumps(protocol), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    assert "protocol_lane_status_next_artifact_category_counts_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_ids_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_expected_paths_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_proof_requirement_empty" in issue_ids
    assert "protocol_lane_status_next_artifact_invalid_substitutes_drift" in issue_ids
    assert "protocol_lane_status_post_plan_category_counts_drift" in issue_ids
    assert "protocol_lane_status_old_failed_invalid_flag_drift" in issue_ids
    assert "protocol_lane_status_post_plan_old_failed_invalid_flag_drift" in issue_ids


def test_formal_gate_handoff_bundle_blocks_remote_when_source_freshness_stale(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=True)
    config.source_freshness_path.write_text(json.dumps(_source_freshness(complete=False)), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "source_freshness_blocks_remote_execution" in issue_ids
    assert manifest["permissions_now"]["source_freshness_ready_for_remote_preflight"] is False
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_formal_gate_handoff_bundle_catches_pending_decision_execution_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    remote_packet = json.loads(config.remote_packet_path.read_text(encoding="utf-8"))
    remote_packet["execution_steps"]["run_remote_training"]["allowed_now"] = True
    remote_packet["execution_steps"]["run_remote_training"]["blocked_by"] = []
    config.remote_packet_path.write_text(json.dumps(remote_packet), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "pending_decision_allows_run_remote_training" in issue_ids


def test_formal_gate_handoff_bundle_consumes_transition_gate_audit(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    transition = json.loads(config.transition_gate_audit_path.read_text(encoding="utf-8"))
    transition["status"] = "f02_6_transition_gate_audit_failed"
    transition["audit_issue_count"] = 1
    approved = next(item for item in transition["scenario_summaries"] if item["scenario_id"] == "approved")
    approved["formal_gate_status_report_permissions_now"]["remote_training_allowed_now"] = True
    approved["formal_gate_status_report_permissions_now"]["formal_claim_allowed_now"] = True
    approved["post_plan_stage_summary"]["gate3_remote_training"]["allowed_now"] = True
    config.transition_gate_audit_path.write_text(json.dumps(transition), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "transition_gate_audit_not_passed" in issue_ids
    assert "transition_gate_audit_issues_open" in issue_ids
    assert "transition_gate_approved_gate3_remote_training_ready_too_early" in issue_ids
    assert "transition_gate_approved_allows_formal_claim" in issue_ids
    assert "transition_gate_approved_gate3_remote_training_ready_too_early" in issue_ids


def test_formal_gate_handoff_bundle_catches_gap_summary_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    post_plan = json.loads(config.post_plan_path.read_text(encoding="utf-8"))
    post_plan["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] = 2
    config.post_plan_path.write_text(json.dumps(post_plan), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "remaining_deliverables_gap_summary_mismatch" in issue_ids


def test_formal_gate_handoff_bundle_catches_f02_6_route_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    status_report = json.loads(config.status_report_path.read_text(encoding="utf-8"))
    status_report["f02_6_decision_intake_summary"]["approved_route_allows_remote_training_now"] = True
    status_report["f02_6_decision_intake_summary"]["rejected_route_requires_new_protocol_contract"] = False
    config.status_report_path.write_text(json.dumps(status_report), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "f02_6_approved_route_allows_remote_training" in issue_ids
    assert "f02_6_rejected_route_missing_protocol_contract" in issue_ids


def test_formal_gate_handoff_bundle_catches_f02_6_decision_impact_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    status_report = json.loads(config.status_report_path.read_text(encoding="utf-8"))
    intake = status_report["f02_6_decision_intake_summary"]
    intake["decision_impact_present"] = False
    intake["decision_record_is_not_training_authorization"] = False
    intake["decision_record_is_not_paper_result_material"] = False
    intake["decision_impact_remote_training_allowed_now"] = True
    intake["decision_impact_formal_claim_allowed_now"] = True
    intake["decision_impact_paper_result_material_allowed_now"] = True
    intake["decision_impact_formal_training_still_requires"] = []
    config.status_report_path.write_text(json.dumps(status_report), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "f02_6_decision_impact_missing" in issue_ids
    assert "f02_6_decision_record_may_authorize_training" in issue_ids
    assert "f02_6_decision_record_may_be_paper_result_material" in issue_ids
    assert "f02_6_decision_impact_allows_remote_training" in issue_ids
    assert "f02_6_decision_impact_allows_formal_claim" in issue_ids
    assert "f02_6_decision_impact_allows_paper_result_material" in issue_ids
    assert "f02_6_decision_impact_missing_required_approved_remote_preflight" in issue_ids


def test_formal_gate_handoff_bundle_catches_f02_6_decision_evidence_matrix_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    status_report = json.loads(config.status_report_path.read_text(encoding="utf-8"))
    matrix = status_report["f02_6_decision_evidence_matrix_summary"]
    matrix["missing_required_evidence_count"] = 1
    matrix["missing_required_evidence_ids"] = ["missing_basis"]
    matrix["remote_training_allowed_now"] = True
    matrix["global_invalid_substitute_count"] = 0
    matrix["invalid_substitute_counts_by_route"]["approve_obstacle_summary_warm_start"] = 0
    config.status_report_path.write_text(json.dumps(status_report), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "blocked_handoff_input_safety_issues"
    summary = manifest["f02_6_decision_evidence_matrix_handoff_summary"]
    assert summary["missing_required_evidence_count"] == 1
    assert summary["authorization_flags"]["remote_training_allowed_now"] is True
    issue_ids = {issue["issue_id"] for issue in manifest["safety_issues"]}
    assert "f02_6_decision_evidence_matrix_missing_required_evidence" in issue_ids
    assert "f02_6_decision_evidence_matrix_allows_remote_training" in issue_ids
    assert "f02_6_decision_evidence_matrix_invalid_substitutes_missing" in issue_ids
    assert (
        "f02_6_decision_evidence_matrix_approve_obstacle_summary_warm_start_invalid_substitutes_missing"
        in issue_ids
    )


def test_formal_gate_handoff_bundle_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    config = _config(tmp_path, complete=False)
    manifest_path = tmp_path / "handoff.json"
    markdown_path = tmp_path / "handoff.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--decision-record",
            str(config.decision_record_path),
            "--decision-intake",
            str(config.decision_intake_path),
            "--transition-gate-audit",
            str(config.transition_gate_audit_path),
            "--post-plan",
            str(config.post_plan_path),
            "--status-report",
            str(config.status_report_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--missing-artifacts",
            str(config.missing_artifacts_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
            "--source-freshness",
            str(config.source_freshness_path),
            "--protocol-lane-status-report",
            str(config.protocol_lane_status_report_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "blocked_until_f02_6_decision"
    assert "Module2 Formal Gate Handoff Bundle" in markdown
    assert "Single Next Action Index" in markdown
    assert "single_current_human_entry: `True`" in markdown
    assert "record template: approve_obstacle_summary_warm_start" in markdown
    assert "build_module2_f02_6_decision_record" in markdown
    assert "Remote Steps" in markdown
    assert "Handoff Stages" in markdown
    assert "F02.6 Route Handoff" in markdown
    assert "F02.6 Decision Evidence Matrix" in markdown
    assert "module2_f02_6_decision_evidence_matrix" in markdown
    assert "ready_for_dr_sun_decision_not_authorization" in markdown
    assert "decision_record_is_not_training_authorization" in markdown
    assert "source_freshness_status" in markdown
    assert "remaining deliverables gap" in markdown
    assert "Status Report Proof-Audit Deliverables Summary" in markdown
    assert "missing_counts_by_formal_category" in markdown
    assert "formal_acceptance_missing_matrix_ids" in markdown
    assert "responsible_stage=`gate3_remote_training`" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete, protocol_pending=None):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    protocol_status = {} if protocol_pending is None else _protocol_lane_status(pending=protocol_pending)
    return builder.FormalGateHandoffBundleConfig(
        output_dir=tmp_path,
        decision_record_path=_json(tmp_path, "decision.json", _decision(complete=complete)),
        decision_intake_path=_json(tmp_path, "decision_intake.json", _decision_intake(complete=complete)),
        transition_gate_audit_path=_json(tmp_path, "transition_gate.json", _transition_gate()),
        post_plan_path=_json(tmp_path, "post_plan.json", _post_plan(complete=complete)),
        status_report_path=_json(tmp_path, "status_report.json", _status_report(complete=complete)),
        remote_packet_path=_json(tmp_path, "remote_packet.json", _remote_packet(complete=complete)),
        missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts(complete=complete)),
        h02_acceptance_path=_json(tmp_path, "h02.json", _h02(complete=complete)),
        source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness(complete=complete)),
        protocol_lane_status_report_path=_json(
            tmp_path,
            "protocol_lane_status.json",
            protocol_status,
        ),
    )


def _decision(*, complete):
    return {
        "status": "approved" if complete else "pending_human_decision",
        "decider": "Dr Sun" if complete else None,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _decision_intake(*, complete):
    return {
        "status": "f02_6_decision_intake_closed" if complete else "f02_6_decision_intake_pending_clean",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "decision_intake_contract": {
            "decision_owner_required": "Dr Sun",
            "valid_decisions": [
                "approve_obstacle_summary_warm_start",
                "reject_obstacle_summary_warm_start",
            ],
            "required_record_fields_for_non_pending_decision": ["decision", "decider", "decision_note"],
            "record_command_templates": [
                {
                    "decision": "approve_obstacle_summary_warm_start",
                    "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'",
                },
                {
                    "decision": "reject_obstacle_summary_warm_start",
                    "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision reject_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun rejection note>'",
                },
            ],
        },
        "next_human_decision_request": {
            "status": "closed" if complete else "awaiting_dr_sun_decision",
            "decision_owner_required": "Dr Sun",
            "valid_decisions": [
                "approve_obstacle_summary_warm_start",
                "reject_obstacle_summary_warm_start",
            ],
            "required_record_fields": ["decision", "decider", "decision_note"],
            "current_allowed_action_ids": [] if complete else ["record_f02_6_decision"],
            "current_blocked_action_ids": [] if complete else [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "post_decision_routes_are_current_authorization": False,
            "all_execution_disabled_now": not complete,
        },
    }


def _transition_gate():
    return {
        "status": "f02_6_transition_gate_audit_passed",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "audit_issue_count": 0,
        "scenario_summaries": [
            _transition_scenario(
                "pending",
                post_plan_status="blocked_until_f02_6_decision",
                next_lane="decision",
                regeneration_allowed=False,
            ),
            _transition_scenario(
                "approved",
                post_plan_status="ready_to_execute_post_f02_6_regeneration_plan",
                next_lane="source_fresh_preflight",
                regeneration_allowed=True,
            ),
            _transition_scenario(
                "rejected",
                post_plan_status="blocked_by_f02_6_rejected",
                next_lane="source_fresh_preflight",
                regeneration_allowed=False,
            ),
        ],
    }


def _transition_scenario(scenario_id, *, post_plan_status, next_lane, regeneration_allowed):
    return {
        "scenario_id": scenario_id,
        "post_plan_status": post_plan_status,
        "formal_gate_status_report_next_blocked_lane_id": next_lane,
        "formal_gate_status_report_permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
        "post_plan_stage_summary": {
            "regenerate_preflight_gate_artifacts": {"allowed_now": regeneration_allowed},
            "approved_remote_preflight": {"allowed_now": False},
            "gate3_remote_training": {"allowed_now": False},
            "regenerate_claim_gate_artifacts": {"allowed_now": False},
        },
    }


def _post_plan(*, complete):
    blockers = [] if complete else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    return {
        "status": "ready_for_remote_training_packet_execution" if complete else "blocked_until_f02_6_decision",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "remaining_deliverables_gap_summary": _gap_summary(open_gaps=not complete),
        "ordered_stages": [
            _stage("f02_6_decision_record", "decision", allowed=not complete, blocked=[] if not complete else ["current_decision_status_approved"]),
            _stage("regenerate_preflight_gate_artifacts", "regeneration", allowed=complete, blocked=[] if complete else ["f02_6_decision_not_approved"]),
            _stage("approved_remote_preflight", "remote_preflight", allowed=complete, blocked=blockers, runs_remote_preflight=True, host="gpu3070ti-relay"),
            _stage("regenerate_remote_execution_packet", "regeneration", allowed=complete, blocked=blockers),
            _stage("gate3_remote_training", "training", allowed=complete, blocked=blockers, runs_training=True, host="gpu3070ti-relay"),
            _stage("gate3_remote_audit_pullback", "acceptance", allowed=complete, blocked=blockers, host="gpu3070ti-relay"),
            _stage("regenerate_h01_h02_formal_artifacts", "evaluation", allowed=False, blocked=["missing_remote_audit_pullback"]),
            _stage("regenerate_claim_gate_artifacts", "claim_gate", allowed=False, blocked=["h02_formal_acceptance_not_ready"]),
        ],
    }


def _stage(stage_id, phase, *, allowed, blocked, runs_training=False, runs_remote_preflight=False, host=None):
    command = "ssh gpu3070ti-relay 'PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda'"
    return {
        "stage_id": stage_id,
        "phase": phase,
        "status": "ready" if allowed else "blocked",
        "allowed_now": allowed,
        "blocked_by": blocked,
        "runs_training": runs_training,
        "runs_remote_preflight": runs_remote_preflight,
        "host": host,
        "evidence_paths": ["0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip"],
        "command_templates": [command] if runs_training else [],
    }


def _status_report(*, complete):
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
    return {
        "status": "formal_gate_status_ready_for_claim_audit" if complete else "formal_gate_status_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "permissions_now": {
            "f02_6_decision_closed": complete,
            "warm_start_formal_chain_approved": complete,
            "remote_preflight_allowed_now": complete,
            "remote_training_allowed_now": complete,
            "formal_claim_allowed_now": complete,
            "local_training_allowed_now": False,
            "source_freshness_ready_for_remote_preflight": complete,
        },
        "current_state": {
            "source_freshness_status": "source_freshness_clean_current"
            if complete
            else "source_freshness_risks_recorded_gate_still_blocked",
            "source_freshness_regeneration_required": not complete,
            "source_freshness_non_self_changed_records": 0 if complete else 18,
            "source_freshness_self_artifact_only_lag_records": 0 if complete else 1,
        },
        "next_blocked_lane": None if complete else {"lane_id": "decision"},
        "remaining_deliverables_gap_summary": _gap_summary(open_gaps=not complete),
        "formal_gate_proof_audit_remaining_deliverables_top_level_summary": {
            "present": True,
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
        },
        "f02_6_decision_intake_summary": {
            "present": True,
            "post_decision_route_count": 2,
            "post_decision_route_decisions": [
                "approve_obstacle_summary_warm_start",
                "reject_obstacle_summary_warm_start",
            ],
            "approved_route_next_lane": "source_fresh_regeneration",
            "approved_route_allows_remote_training_now": False,
            "rejected_route_next_lane": "protocol_redesign",
            "rejected_route_requires_new_protocol_contract": True,
            "decision_impact_present": True,
            "decision_record_is_not_training_authorization": True,
            "decision_record_is_not_paper_result_material": True,
            "record_authorization_status": "decision_recorded_not_execution_authorization"
            if complete
            else "blocked_until_dr_sun_decision",
            "record_authorization_current_blocked_action_ids": [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "record_authorization_post_decision_routes_are_current_authorization": False,
            "record_authorization_remote_preflight_allowed_now": False,
            "record_authorization_remote_training_allowed_now": False,
            "record_authorization_local_training_allowed_now": False,
            "record_authorization_formal_claim_allowed_now": False,
            "record_authorization_paper_result_material_allowed_now": False,
            "record_post_decision_non_authorization_count": 4,
            "record_post_decision_formal_training_still_requires": [
                "source_freshness_audit",
                "post_f02_6_regeneration_plan",
                "post_f02_6_plan_audit",
                "remote_formal_execution_packet_ready",
                "approved_remote_preflight",
            ],
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
        },
        "f02_6_decision_evidence_matrix_summary": _decision_evidence_matrix_summary(),
    }


def _decision_evidence_matrix_summary():
    return {
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
        "missing_required_evidence_ids": [],
        "current_authorization_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "source_issue_count": 0,
        "global_invalid_substitute_count": 4,
        "evidence_counts_by_route": {
            "approve_obstacle_summary_warm_start": 4,
            "reject_obstacle_summary_warm_start": 3,
        },
        "invalid_substitute_counts_by_route": {
            "approve_obstacle_summary_warm_start": 4,
            "reject_obstacle_summary_warm_start": 4,
        },
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
        "commit_lag_summary": {
            "records_with_non_self_changed_paths_since_source": 0 if complete else 18,
            "records_with_self_artifact_only_lag": 0 if complete else 1,
        },
    }


def _protocol_lane_status(*, pending):
    return {
        "status": "protocol_lane_status_blocked_pending_lane_decision"
        if pending
        else "protocol_lane_status_ready_for_contract_draft",
        "audit_issue_count": 0,
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "current_status": {
            "next_blocked_lane": "protocol_lane_decision" if pending else "new_or_revised_contract",
            "decision_record_status": "pending_protocol_lane_decision"
            if pending
            else "protocol_lane_decision_recorded",
            "selected_lane_id": None if pending else "hybrid_ppo_analytic_fallback",
            "lane_count": 4,
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
                "evaluation": [
                    "eval_gate3_eval_episodes_csv",
                    "eval_gate3_summary_json",
                ],
                "acceptance": [
                    "gate3_trial_manifest_json",
                    "gate3_formal_audit_json",
                    "pulled_back_checkpoint_hash_record",
                ],
                "formal_acceptance": ["h02_formal_output_acceptance"],
            },
            "next_success_attempt_artifact_expected_paths_by_id": _next_success_expected_paths_by_id(),
            "next_success_attempt_artifact_proof_requirements_by_id": _next_success_proof_requirements_by_id(),
            "next_success_attempt_artifact_invalid_substitutes_by_id": _next_success_invalid_substitutes_by_id(),
            "post_decision_contract_plan_shared_artifact_count": 10,
            "post_decision_contract_plan_shared_artifact_category_counts": {
                "contract": 1,
                "training": 3,
                "evaluation": 2,
                "acceptance": 3,
                "formal_acceptance": 1,
            },
            "old_failed_run_artifacts_invalid_for_next_success_attempt": True,
            "post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt": True,
            "contract_drafting_allowed_now": False if pending else True,
            "contract_approval_allowed_now": False,
            "draft_contract_allows_training": False,
            "allowed_next_action_ids": ["record_protocol_lane_decision"]
            if pending
            else ["draft_new_or_revised_contract_after_lane_decision"],
            "blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
            "local_training_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "new_success_training_allowed_now": False,
        },
    }


def _next_success_expected_paths_by_id():
    return {
        "new_or_revised_research_contract": ".pipeline/contracts/module2-<selected_protocol_lane>-<version>.md",
        "train_final_model_zip": "0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip",
        "train_summary_json": "0_trials/module2_gate3_formal/<next_attempt_id>/train/summary.json",
        "train_training_manifest_json": "0_trials/module2_gate3_formal/<next_attempt_id>/train/training_manifest.json",
        "eval_gate3_eval_episodes_csv": "0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_eval_episodes.csv",
        "eval_gate3_summary_json": "0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_summary.json",
        "gate3_trial_manifest_json": "0_trials/module2_gate3_formal/<next_attempt_id>/gate3_trial_manifest.json",
        "gate3_formal_audit_json": "0_trials/module2_gate3_formal/<next_attempt_id>/gate3_formal_audit.json",
        "pulled_back_checkpoint_hash_record": (
            "0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip.sha256 or .sha256.json"
        ),
        "h02_formal_output_acceptance": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
    }


def _next_success_proof_requirements_by_id():
    return {
        "new_or_revised_research_contract": "contract status is approved or frozen",
        "train_final_model_zip": "remote-produced PPO checkpoint pulled back from gpu3070ti-relay",
        "train_summary_json": "summary records protocol label, training budget, seed, and terminal-RS training signals",
        "train_training_manifest_json": "manifest records source head, host, command provenance, seed, and selected protocol lane",
        "eval_gate3_eval_episodes_csv": "per-episode formal Gate3 CSV with at least 64 episodes and protocol provenance",
        "eval_gate3_summary_json": "summary records terminal-RS success, collision, truncation, timing, seed, and protocol label",
        "gate3_trial_manifest_json": "trial manifest ties contract, train, eval, audit, source head, and selected protocol lane",
        "gate3_formal_audit_json": "audit records formal_decision=pass for the new approved protocol attempt",
        "pulled_back_checkpoint_hash_record": "hash record matches the pulled-back final_model.zip evaluated by Gate3",
        "h02_formal_output_acceptance": (
            "H02 records formal_output_accepted=true, paper_result_input_allowed=true, PPO rows, and accepted checkpoint hash"
        ),
    }


def _next_success_invalid_substitutes_by_id():
    return {
        "new_or_revised_research_contract": [
            "chat-only approval",
            "draft contract",
            "editing the failed Gate3 result after seeing failure",
        ],
        "train_final_model_zip": [
            "local PPO training output",
            "failed warm-start checkpoint",
            "checkpoint without manifest or hash provenance",
        ],
        "train_summary_json": [
            "stdout-only training summary",
            "summary from the failed Gate3 attempt",
            "summary without protocol label",
        ],
        "train_training_manifest_json": [
            "manifest without source head",
            "manifest from a different protocol lane",
            "uncommitted chat note",
        ],
        "eval_gate3_eval_episodes_csv": [
            "H02 available-subset smoke CSV",
            "no-warm failure rows reused for a warm-start claim",
            "aggregate summary without per-episode rows",
        ],
        "eval_gate3_summary_json": [
            "summary from failed run",
            "summary without timing fields",
            "paper table preview",
        ],
        "gate3_trial_manifest_json": [
            "trial manifest from failed run",
            "manifest without contract reference",
            "manifest without evaluated checkpoint identity",
        ],
        "gate3_formal_audit_json": [
            "formal_decision=fail reinterpreted as success",
            "audit marked smoke, preview, or candidate",
            "audit from a different protocol lane",
        ],
        "pulled_back_checkpoint_hash_record": [
            "checkpoint without hash record",
            "hash for a different checkpoint",
            "remote stdout without local pullback",
        ],
        "h02_formal_output_acceptance": [
            "blocked H02 acceptance",
            "formal-looking smoke table",
            "PPO rows without checkpoint hash",
        ],
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


def _gap_category(category, missing_count, stage_id, *, open_gaps):
    return {
        "missing_count": missing_count,
        "responsible_stage_id": stage_id,
        "responsible_stage_allowed_now": not open_gaps,
        "missing_artifact_matrix_ids": [f"{category}:artifact_{index}" for index in range(missing_count)],
    }


def _remote_packet(*, complete):
    blockers = [] if complete else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    return {
        "status": "ready_for_gpu3070ti_remote_training" if complete else "blocked_until_f02_6_decision",
        "ready_to_run_remote_training": complete,
        "post_run_pullback": {
            "expected_artifacts": [
                "train/final_model.zip",
                "train/summary.json",
                "train/training_manifest.json",
                "eval/gate3_eval_episodes.csv",
                "eval/gate3_summary.json",
                "gate3_trial_manifest.json",
                "gate3_formal_audit.json",
            ]
        },
        "execution_steps": {
            "sync_to_remote": _remote_step(complete, False, blockers),
            "run_remote_preflight": _remote_step(complete, False, blockers),
            "run_remote_training": _remote_step(complete, True, blockers),
            "run_remote_audit": _remote_step(complete, False, blockers),
        },
    }


def _remote_step(allowed, runs_training, blockers):
    return {
        "allowed_now": allowed,
        "runs_training": runs_training,
        "blocked_by": blockers,
        "command": "ssh gpu3070ti-relay 'PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda'",
    }


def _missing_artifacts(*, complete):
    return {
        "status": "formal_gate_artifacts_complete" if complete else "formal_gate_missing_artifacts_open",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "formal_gate_requirements": [
            _requirement("training_remote_ppo_checkpoint", "training", complete=complete, stage_id="gate3_remote_training"),
            _requirement("evaluation_gate3_episode_outputs", "evaluation", complete=complete, stage_id="gate3_remote_audit_pullback"),
            _requirement("acceptance_remote_pullback_and_audit", "acceptance", complete=complete, stage_id="gate3_remote_audit_pullback"),
            _requirement(
                "h01_h02_formal_evaluation_acceptance",
                "evaluation_acceptance",
                complete=complete,
                stage_id="regenerate_h01_h02_formal_artifacts",
            ),
        ],
    }


def _h02(*, complete):
    return {
        "status": "formal_output_accepted" if complete else "blocked_formal_output_acceptance",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "formal_output_accepted": complete,
        "paper_result_input_allowed": complete,
        "formal_acceptance_requirements": [
            _requirement("h01_schema_and_h02_output_schema_match", "schema", complete=True),
            _requirement("h02_formal_scope_and_scale_match_h01", "scope", complete=complete),
            _requirement("gate3_audit_and_pullback_acceptance", "acceptance", complete=complete),
            _requirement("ppo_rows_and_checkpoint_hash_present", "ppo_rows", complete=complete),
        ],
    }


def _requirement(requirement_id, phase, *, complete, stage_id=None):
    payload = {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": "satisfied" if complete else "blocked_missing_outputs",
        "complete": complete,
        "execution_allowed_now": False,
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "acceptable_evidence": [f"{requirement_id}_evidence"],
        "invalid_substitutes": [f"{requirement_id}_invalid_substitute"],
    }
    if stage_id:
        payload.update(
            {
                "responsible_stage_id": stage_id,
                "responsible_stage_status": "ready" if complete else "blocked",
                "responsible_stage_allowed_now": complete,
                "responsible_stage_blocked_by": [] if complete else ["remote_packet_not_ready"],
                "responsible_stage_evidence_paths": [
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip"
                ],
            }
        )
    return payload


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
