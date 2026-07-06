import json
from importlib import import_module


def test_mainline_formal_gate_state_audit_accepts_current_blocked_state(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_mainline_formal_gate_state_audit"
    assert manifest["status"] == "mainline_formal_gate_state_consistent_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["expected_next_action_id"] == "record_f02_6_decision"
    assert manifest["expected_next_action_mentioned"] is True
    protocol = manifest["protocol_lane_status_summary"]
    assert protocol["status"] == "protocol_lane_status_blocked_pending_lane_decision"
    assert protocol["audit_issue_count"] == 0
    assert protocol["next_blocked_lane"] == "protocol_lane_decision"
    assert protocol["decision_record_status"] == "pending_protocol_lane_decision"
    assert protocol["selected_lane_id"] is None
    assert protocol["lane_count"] == 4
    assert protocol["post_decision_contract_plan_summary_present"] is True
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
    assert protocol["next_success_attempt_artifact_ids_by_category"]["formal_acceptance"] == [
        "h02_formal_output_acceptance"
    ]
    assert protocol["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True
    assert protocol["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert protocol["blocked_action_ids"] == [
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    ]
    assert manifest["protocol_lane_status_mentioned"] is True
    assert manifest["protocol_lane_next_blocked_mentioned"] is True
    assert manifest["protocol_lane_next_action_mentioned"] is True
    assert manifest["protocol_lane_decision_record_status_mentioned"] is True
    assert manifest["protocol_lane_lane_mentions"] == [
        {"lane_id": "stronger_obstacle_summary_warm_start", "mentioned": True},
        {"lane_id": "full_patch_cnn_policy", "mentioned": True},
        {"lane_id": "hybrid_ppo_analytic_fallback", "mentioned": True},
        {"lane_id": "stop_or_reframe_module2_claim", "mentioned": True},
    ]
    assert manifest["protocol_lane_blocked_action_mentions"] == [
        {"action_id": "local_training", "mentioned": True},
        {"action_id": "remote_success_training", "mentioned": True},
        {"action_id": "remote_preflight_for_new_success_attempt", "mentioned": True},
        {"action_id": "formal_claim", "mentioned": True},
        {"action_id": "paper_result_material", "mentioned": True},
    ]
    assert manifest["protocol_lane_status_post_plan_summary_mentioned"] is True
    assert manifest["protocol_lane_status_next_artifact_category_counts_mentioned"] is True
    assert manifest["protocol_lane_status_old_failed_invalid_mentioned"] is True
    readiness = manifest["protocol_lane_readiness_summary"]
    assert readiness["artifact_name"] == "module2_formal_gate_protocol_lane_readiness"
    assert readiness["status"] == "protocol_lane_readiness_ready_for_dr_sun_decision"
    assert readiness["audit_issue_count"] == 0
    assert readiness["shared_next_success_attempt_artifact_count"] == 10
    assert readiness["gate_next_blocked_lane"] == "protocol_lane_decision"
    assert readiness["gate_selected_lane_id"] is None
    assert readiness["gate_remote_training_allowed_now"] is False
    assert manifest["protocol_lane_readiness_artifact_mentioned"] is True
    assert manifest["protocol_lane_readiness_status_mentioned"] is True
    assert manifest["protocol_lane_readiness_shared_artifact_count_mentioned"] is True
    post_plan = manifest["post_decision_contract_plan_summary"]
    assert post_plan["artifact_name"] == "module2_formal_gate_post_decision_contract_plan"
    assert post_plan["status"] == "post_decision_contract_plan_ready_blocked_pending_lane_decision"
    assert post_plan["audit_issue_count"] == 0
    assert post_plan["required_contract_section_count"] == 8
    assert post_plan["shared_next_success_attempt_artifact_count"] == 10
    assert post_plan["shared_next_success_attempt_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert post_plan["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True
    assert post_plan["lane_count"] == 4
    assert post_plan["gate_selected_lane_id"] is None
    assert post_plan["gate_contract_drafting_allowed_now"] is False
    assert post_plan["gate_remote_training_allowed_now"] is False
    assert manifest["post_decision_contract_plan_artifact_mentioned"] is True
    assert manifest["post_decision_contract_plan_status_mentioned"] is True
    assert manifest["post_decision_contract_plan_required_section_count_mentioned"] is True
    assert manifest["post_decision_contract_plan_shared_artifact_count_mentioned"] is True
    assert manifest["post_decision_contract_plan_lane_count_mentioned"] is True
    assert manifest["post_decision_contract_plan_old_failed_invalid_mentioned"] is True
    assert manifest["total_missing_deliverables"] == 10
    assert manifest["mainline_missing_deliverable_mention_count"] == 0
    matrix = manifest["f02_6_decision_evidence_matrix_summary"]
    assert matrix["matrix_id"] == "module2_f02_6_decision_evidence_matrix"
    assert matrix["status"] == "ready_for_dr_sun_decision_not_authorization"
    assert matrix["route_count"] == 2
    assert matrix["required_evidence_count"] == 7
    assert matrix["missing_required_evidence_count"] == 0
    assert matrix["authorization_flags"]["remote_training_allowed_now"] is False
    assert manifest["f02_6_decision_evidence_matrix_mentioned"] is True
    assert manifest["f02_6_decision_evidence_matrix_status_mentioned"] is True
    assert manifest["f02_6_decision_evidence_matrix_route_mentions"] == [
        {"route_decision": "approve_obstacle_summary_warm_start", "mentioned": True},
        {"route_decision": "reject_obstacle_summary_warm_start", "mentioned": True},
    ]
    assert manifest["proof_summary_chain_status"] == "formal_gate_proof_summary_chain_consistent_blocked"
    assert manifest["proof_summary_handoff_single_next_action_consistency"] == {
        "row_count": 3,
        "consistent_row_count": 3,
    }
    assert manifest["audit_issue_count"] == 0
    assert manifest["deliverable_rows_by_matrix_id"]["training:train_final_model_zip"]["mentioned"] is True


def test_mainline_formal_gate_state_audit_fails_missing_deliverable_mention(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_artifact_id="eval_gate3_summary_json")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_missing_deliverable_evaluation_eval_gate3_summary_json" in issue_ids


def test_mainline_formal_gate_state_audit_fails_execution_leak_in_status_report(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    status = json.loads(paths["status"].read_text(encoding="utf-8"))
    status["next_action_guard_summary"]["all_execution_disabled_now"] = False
    status["next_action_guard_summary"]["execution_leak_count"] = 1
    paths["status"].write_text(json.dumps(status), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "status_report_next_action_guard_execution_leak" in issue_ids


def test_mainline_formal_gate_state_audit_fails_decision_evidence_matrix_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    status = json.loads(paths["status"].read_text(encoding="utf-8"))
    matrix = status["f02_6_decision_evidence_matrix_summary"]
    matrix["missing_required_evidence_count"] = 1
    matrix["missing_required_evidence_ids"] = ["route_observed_fact_missing"]
    matrix["remote_training_allowed_now"] = True
    paths["status"].write_text(json.dumps(status), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["f02_6_decision_evidence_matrix_summary"]["missing_required_evidence_count"] == 1
    assert manifest["f02_6_decision_evidence_matrix_summary"]["authorization_flags"][
        "remote_training_allowed_now"
    ] is True
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "status_report_decision_evidence_matrix_missing_required_evidence" in issue_ids
    assert "status_report_decision_evidence_matrix_authorization_leak" in issue_ids


def test_mainline_formal_gate_state_audit_fails_missing_decision_matrix_mainline_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_decision_matrix_boundary=True)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["f02_6_decision_evidence_matrix_mentioned"] is False
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_missing_decision_evidence_matrix" in issue_ids
    assert "mainline_current_section_missing_decision_evidence_matrix_status" in issue_ids
    assert "mainline_current_section_missing_invalid_substitutes_boundary" in issue_ids


def test_mainline_formal_gate_state_audit_fails_missing_protocol_lane_mainline_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_protocol_lane_boundary=True)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["protocol_lane_status_mentioned"] is False
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_missing_protocol_lane_status" in issue_ids
    assert "mainline_current_section_missing_protocol_lane_next_blocked" in issue_ids
    assert "mainline_current_section_missing_protocol_lane_next_action" in issue_ids
    assert "mainline_current_section_missing_protocol_lane_full_patch_cnn_policy" in issue_ids


def test_mainline_formal_gate_state_audit_fails_protocol_lane_authorization_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    protocol = json.loads(paths["protocol"].read_text(encoding="utf-8"))
    protocol["current_status"]["remote_training_allowed_now"] = True
    protocol["current_status"]["allowed_next_action_ids"] = [
        "record_protocol_lane_decision",
        "remote_success_training",
    ]
    paths["protocol"].write_text(json.dumps(protocol), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["protocol_lane_status_summary"]["remote_training_allowed_now"] is True
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "protocol_lane_status_authorization_leak" in issue_ids
    assert "protocol_lane_status_allowed_actions_drift" in issue_ids


def test_mainline_formal_gate_state_audit_fails_protocol_status_post_plan_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    protocol = json.loads(paths["protocol"].read_text(encoding="utf-8"))
    current = protocol["current_status"]
    current["post_decision_contract_plan_required_section_count"] = 7
    current["post_decision_contract_plan_shared_artifact_category_counts"]["training"] = 2
    current["post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt"] = False
    current["post_decision_contract_plan_runs_training"] = True
    current["post_decision_contract_plan_selected_lane_id"] = "full_patch_cnn_policy"
    current["next_success_attempt_artifact_ids_by_category"]["evaluation"] = [
        "eval_gate3_eval_episodes_csv"
    ]
    current["next_success_attempt_artifact_count"] = 9
    current["next_success_attempt_artifact_category_counts"]["evaluation"] = 1
    current["old_failed_run_artifacts_invalid_for_next_success_attempt"] = False
    paths["protocol"].write_text(json.dumps(protocol), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "protocol_lane_status_post_decision_contract_plan_required_section_count_drift" in issue_ids
    assert "protocol_lane_status_post_plan_shared_artifact_category_counts_drift" in issue_ids
    assert "protocol_lane_status_post_plan_old_failed_invalid_flag_drift" in issue_ids
    assert "protocol_lane_status_post_plan_authorization_leak" in issue_ids
    assert "protocol_lane_status_post_plan_selected_lane_present" in issue_ids
    assert "protocol_lane_status_next_artifact_count_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_category_counts_drift" in issue_ids
    assert "protocol_lane_status_old_failed_invalid_flag_drift" in issue_ids
    assert "protocol_lane_status_next_artifact_ids_missing" in issue_ids


def test_mainline_formal_gate_state_audit_fails_missing_protocol_status_post_plan_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_protocol_lane_status_post_plan_boundary=True)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["protocol_lane_status_post_plan_summary_mentioned"] is False
    assert manifest["protocol_lane_status_next_artifact_category_counts_mentioned"] is False
    assert manifest["protocol_lane_status_old_failed_invalid_mentioned"] is False
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_missing_protocol_status_post_plan_section_count" in issue_ids
    assert "mainline_current_section_missing_protocol_status_post_plan_artifact_count" in issue_ids
    assert "mainline_current_section_missing_protocol_status_post_plan_lane_count" in issue_ids
    assert "mainline_current_section_missing_protocol_status_next_artifact_category_counts" in issue_ids


def test_mainline_formal_gate_state_audit_fails_missing_old_failed_invalid_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    mainline = paths["mainline"].read_text(encoding="utf-8")
    paths["mainline"].write_text(
        mainline.replace("old_failed_run_artifacts_invalid_for_next_success_attempt=true", ""),
        encoding="utf-8",
    )

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_missing_old_failed_invalid_boundary" in issue_ids


def test_mainline_formal_gate_state_audit_fails_missing_protocol_lane_readiness_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_protocol_lane_readiness_boundary=True)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["protocol_lane_readiness_artifact_mentioned"] is False
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_missing_protocol_lane_readiness_artifact" in issue_ids
    assert "mainline_current_section_missing_protocol_lane_readiness_status" in issue_ids
    assert "mainline_current_section_missing_protocol_lane_readiness_shared_artifact_count" in issue_ids


def test_mainline_formal_gate_state_audit_fails_protocol_lane_readiness_authorization_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    readiness = json.loads(paths["readiness"].read_text(encoding="utf-8"))
    readiness["runs_training"] = True
    readiness["gate_state"]["remote_training_allowed_now"] = True
    paths["readiness"].write_text(json.dumps(readiness), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["protocol_lane_readiness_summary"]["runs_training"] is True
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "protocol_lane_readiness_authorization_leak" in issue_ids


def test_mainline_formal_gate_state_audit_fails_missing_post_decision_contract_plan_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_post_decision_contract_plan_boundary=True)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["post_decision_contract_plan_artifact_mentioned"] is False
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_missing_post_decision_contract_plan_artifact" in issue_ids
    assert "mainline_current_section_missing_post_decision_contract_plan_status" in issue_ids
    assert "mainline_current_section_missing_post_decision_contract_section_count" in issue_ids
    assert "mainline_current_section_missing_post_decision_contract_shared_artifact_count" in issue_ids
    assert "mainline_current_section_missing_post_decision_contract_lane_count" in issue_ids


def test_mainline_formal_gate_state_audit_fails_post_decision_contract_plan_authorization_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    plan = json.loads(paths["post_plan"].read_text(encoding="utf-8"))
    plan["writes_contract"] = True
    plan["gate_state"]["remote_training_allowed_now"] = True
    paths["post_plan"].write_text(json.dumps(plan), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["post_decision_contract_plan_summary"]["writes_contract"] is True
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "post_decision_contract_plan_authorization_leak" in issue_ids


def test_mainline_formal_gate_state_audit_fails_current_section_allowed_token(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, extra_current_text=" remote_training_allowed=true")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_forbidden_allowed_token_remote_training_allowed_true" in issue_ids


def test_mainline_formal_gate_state_audit_fails_handoff_single_next_action_chain_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    proof = json.loads(paths["proof"].read_text(encoding="utf-8"))
    proof["handoff_single_next_action_consistent_row_count"] = 2
    paths["proof"].write_text(json.dumps(proof), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "proof_summary_chain_handoff_single_next_action_inconsistent" in issue_ids


def test_mainline_formal_gate_state_audit_fails_proof_audit_input_safety_open(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    proof = json.loads(paths["proof"].read_text(encoding="utf-8"))
    proof["proof_audit_input_safety_issue_count"] = 1
    proof["proof_audit_blockers"] = ["proof_audit_input_safety_issues_open"]
    paths["proof"].write_text(json.dumps(proof), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["proof_summary_chain_proof_audit_input_safety_issue_count"] == 1
    assert manifest["proof_summary_chain_proof_audit_blockers"] == [
        "proof_audit_input_safety_issues_open"
    ]
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "proof_summary_chain_proof_audit_input_safety_issues_open" in issue_ids
    assert "proof_summary_chain_proof_audit_input_safety_blocker_open" in issue_ids


def test_mainline_formal_gate_state_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--mainline",
            str(paths["mainline"]),
            "--formal-gate-status-report",
            str(paths["status"]),
            "--proof-summary-chain-audit",
            str(paths["proof"]),
            "--protocol-lane-status-report",
            str(paths["protocol"]),
            "--protocol-lane-readiness",
            str(paths["readiness"]),
            "--post-decision-contract-plan",
            str(paths["post_plan"]),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "mainline_formal_gate_state_consistent_blocked"
    assert "Module2 Mainline Formal Gate State Audit" in markdown
    assert "not a training run" in markdown
    assert "training:train_final_model_zip" in markdown
    assert "record_f02_6_decision" in markdown
    assert "proof_summary_handoff_single_next_action_consistency" in markdown
    assert "F02.6 Decision Evidence Matrix" in markdown
    assert "module2_f02_6_decision_evidence_matrix" in markdown
    assert "ready_for_dr_sun_decision_not_authorization" in markdown
    assert "Protocol Lane Status" in markdown
    assert "protocol_lane_status_blocked_pending_lane_decision" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "full_patch_cnn_policy" in markdown
    assert "Protocol Lane Readiness" in markdown
    assert "module2_formal_gate_protocol_lane_readiness" in markdown
    assert "protocol_lane_readiness_ready_for_dr_sun_decision" in markdown
    assert "Post-Decision Contract Plan" in markdown
    assert "module2_formal_gate_post_decision_contract_plan" in markdown
    assert "post_decision_contract_plan_ready_blocked_pending_lane_decision" in markdown


def _config(builder, tmp_path, paths):
    return builder.MainlineFormalGateStateAuditConfig(
        output_dir=tmp_path,
        mainline_path=paths["mainline"],
        formal_gate_status_report_path=paths["status"],
        proof_summary_chain_audit_path=paths["proof"],
        protocol_lane_status_report_path=paths["protocol"],
        protocol_lane_readiness_path=paths["readiness"],
        post_decision_contract_plan_path=paths["post_plan"],
    )


def _write_inputs(
    tmp_path,
    *,
    omit_artifact_id=None,
    extra_current_text="",
    omit_decision_matrix_boundary=False,
    omit_protocol_lane_boundary=False,
    omit_protocol_lane_status_post_plan_boundary=False,
    omit_protocol_lane_readiness_boundary=False,
    omit_post_decision_contract_plan_boundary=False,
):
    paths = {
        "mainline": tmp_path / "mainline.md",
        "status": tmp_path / "status.json",
        "proof": tmp_path / "proof.json",
        "protocol": tmp_path / "protocol.json",
        "readiness": tmp_path / "readiness.json",
        "post_plan": tmp_path / "post_plan.json",
    }
    rows = _deliverable_rows()
    artifact_ids = [row["artifact_id"] for row in rows if row["artifact_id"] != omit_artifact_id]
    protocol_lane_text = (
        ""
        if omit_protocol_lane_boundary
        else (
            "Protocol-lane status report 当前为 "
            "`protocol_lane_status_blocked_pending_lane_decision`, "
            "`next_blocked_lane=protocol_lane_decision`, "
            "`decision_record_status=pending_protocol_lane_decision`, "
            "唯一允许动作是 `record_protocol_lane_decision`; "
            "候选 lane 为 `stronger_obstacle_summary_warm_start`, `full_patch_cnn_policy`, "
            "`hybrid_ppo_analytic_fallback`, `stop_or_reframe_module2_claim`; "
            "blocked_action_ids 包括 `local_training`, `remote_success_training`, "
            "`remote_preflight_for_new_success_attempt`, `formal_claim`, `paper_result_material`; "
            "selected_lane_id 仍为 None, lane_count=4。"
            + (
                ""
                if omit_protocol_lane_status_post_plan_boundary
                else (
                    "`protocol_lane_status_report` 继承 post-decision contract plan summary, "
                    "required_contract_section_count=8, shared_next_success_attempt_artifact_count=10, "
                    "lane_count=4, 下一轮 artifact 类别分布 "
                    "`contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1`, "
                    "`old_failed_run_artifacts_invalid_for_next_success_attempt=true`。"
                )
            )
        )
    )
    readiness_text = (
        ""
        if omit_protocol_lane_readiness_boundary
        else (
            "Protocol-lane readiness packet `module2_formal_gate_protocol_lane_readiness` 当前为 "
            "`protocol_lane_readiness_ready_for_dr_sun_decision`, audit_issue_count=0, "
            "shared_next_success_attempt_artifact_count=10; readiness 只准备 Dr Sun 决策, "
            "不是训练、远端预检、formal claim 或论文结果授权。"
        )
    )
    post_plan_text = (
        ""
        if omit_post_decision_contract_plan_boundary
        else (
            "Post-decision contract plan `module2_formal_gate_post_decision_contract_plan` 当前为 "
            "`post_decision_contract_plan_ready_blocked_pending_lane_decision`, audit_issue_count=0, "
            "required_contract_section_count=8, shared_next_success_attempt_artifact_count=10, lane_count=4; "
            "`old_failed_run_artifacts_invalid_for_next_success_attempt=true`; "
            "plan 不写 contract、不批准 contract、不训练、不远端预检、不写 formal claim 或论文结果授权。"
        )
    )
    current_line = (
        "- 2026-07-05: 当前 formal gate 下一步清单已同步到主任务书。"
        "唯一允许动作仍是 `record_f02_6_decision`; "
        f"缺失正式交付物: {', '.join(artifact_ids)}. "
        "当前禁止 local training、remote preflight、remote training、formal claim 和 paper-result material; "
        "`gpu3070ti-relay` 只是在 F02.6 关闭后的正式训练资源。"
        "`formal_gate_proof_summary_chain_consistent_blocked`。"
        + (
            ""
            if omit_decision_matrix_boundary
            else (
                "F02.6 decision evidence matrix `module2_f02_6_decision_evidence_matrix` 当前为 "
                "`ready_for_dr_sun_decision_not_authorization`, 覆盖 "
                "`approve_obstacle_summary_warm_start` 与 `reject_obstacle_summary_warm_start` 两条路线, "
                "并列出 invalid substitutes; matrix 不是训练、远端预检、claim 或论文结果授权。"
            )
        )
        + protocol_lane_text
        + readiness_text
        + post_plan_text
        + f"{extra_current_text}"
    )
    paths["mainline"].write_text("# mainline\n\n" + current_line + "\n", encoding="utf-8")
    paths["status"].write_text(
        json.dumps(
            {
                "status": "formal_gate_status_blocked",
                "next_action_guard_summary": {
                    "present": True,
                    "status": "next_action_guard_passed",
                    "expected_next_action_id": "record_f02_6_decision",
                    "all_execution_disabled_now": True,
                    "execution_leak_count": 0,
                },
                "next_required_formal_deliverables": {
                    "present": True,
                    "status": "blocked_missing_formal_deliverables",
                    "not_paper_result_material": True,
                    "runs_training": False,
                    "runs_remote_preflight": False,
                    "total_missing_deliverables": 10,
                    "blocked_category_count": 4,
                    "rows": rows,
                },
                "f02_6_decision_evidence_matrix_summary": {
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
                },
            }
        ),
        encoding="utf-8",
    )
    paths["proof"].write_text(
        json.dumps(
            {
                "status": "formal_gate_proof_summary_chain_consistent_blocked",
                "proof_open": True,
                "audit_issue_count": 0,
                "next_action_guard_row_count": 3,
                "next_action_guard_consistent_row_count": 3,
                "next_required_deliverables_row_count": 3,
                "next_required_deliverables_consistent_row_count": 3,
                "handoff_single_next_action_row_count": 3,
                "handoff_single_next_action_consistent_row_count": 3,
                "runs_training": False,
                "runs_remote_preflight": False,
                "formal_claim_allowed": False,
            }
        ),
        encoding="utf-8",
    )
    paths["protocol"].write_text(json.dumps(_protocol_lane_status()), encoding="utf-8")
    paths["readiness"].write_text(json.dumps(_protocol_lane_readiness()), encoding="utf-8")
    paths["post_plan"].write_text(json.dumps(_post_decision_contract_plan()), encoding="utf-8")
    return paths


def _deliverable_rows():
    return [
        _row("training", "train_final_model_zip"),
        _row("training", "train_summary_json"),
        _row("training", "train_training_manifest_json"),
        _row("evaluation", "eval_gate3_eval_episodes_csv"),
        _row("evaluation", "eval_gate3_summary_json"),
        _row("acceptance", "gate3_trial_manifest_json"),
        _row("acceptance", "gate3_formal_audit_json"),
        _row("acceptance", "pulled_back_checkpoint_hash_record"),
        _row("formal_acceptance", "h01_ready_for_formal_run"),
        _row("formal_acceptance", "h02_formal_output_acceptance"),
    ]


def _row(category, artifact_id):
    return {
        "matrix_id": f"{category}:{artifact_id}",
        "category": category,
        "artifact_id": artifact_id,
        "responsible_stage_id": "gate3_remote_training",
        "responsible_stage_allowed_now": False,
    }


def _protocol_lane_status():
    return {
        "status": "protocol_lane_status_blocked_pending_lane_decision",
        "audit_issue_count": 0,
        "current_status": {
            "next_blocked_lane": "protocol_lane_decision",
            "decision_packet_status": "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun",
            "decision_record_status": "pending_protocol_lane_decision",
            "decision_gate_status": "protocol_lane_decision_gate_pending_clean",
            "contract_authoring_gate_status": "contract_authoring_gate_blocked_pending_lane_decision",
            "lane_matrix_status": "formal_gate_protocol_lane_matrix_ready",
            "lane_count": 4,
            "next_round_requirements_status": "formal_gate_next_round_requirements_ready",
            "selected_lane_id": None,
            "contract_action": "none",
            "contract_drafting_allowed_now": False,
            "contract_approval_allowed_now": False,
            "draft_contract_allows_training": False,
            "allowed_next_action_ids": ["record_protocol_lane_decision"],
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
            "post_decision_contract_plan_selected_lane_id": None,
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
        },
    }


def _protocol_lane_readiness():
    return {
        "artifact_name": "module2_formal_gate_protocol_lane_readiness",
        "status": "protocol_lane_readiness_ready_for_dr_sun_decision",
        "audit_issue_count": 0,
        "lane_count": 4,
        "shared_next_success_attempt_artifact_count": 10,
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "gate_state": {
            "next_blocked_lane": "protocol_lane_decision",
            "selected_lane_id": None,
            "decision_owner_required": "Dr Sun",
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
        },
    }


def _post_decision_contract_plan():
    return {
        "artifact_name": "module2_formal_gate_post_decision_contract_plan",
        "status": "post_decision_contract_plan_ready_blocked_pending_lane_decision",
        "audit_issue_count": 0,
        "required_contract_section_count": 8,
        "shared_next_success_attempt_artifact_count": 10,
        "shared_next_success_attempt_artifact_category_counts": {
            "contract": 1,
            "training": 3,
            "evaluation": 2,
            "acceptance": 3,
            "formal_acceptance": 1,
        },
        "old_failed_run_artifacts_invalid_for_next_success_attempt": True,
        "lane_count": 4,
        "not_paper_result_material": True,
        "executes_commands": False,
        "writes_contract": False,
        "approves_contract": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "gate_state": {
            "next_blocked_lane": "protocol_lane_decision",
            "selected_lane_id": None,
            "contract_drafting_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
    }
