import json
from importlib import import_module


def test_claim_safety_blocks_overclaims_and_keeps_no_warm_failure_claim(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 claim safety builder: {exc}") from exc

    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(
        json.dumps(
            {
                "status": "blocked_no_formal_h02_data",
                "formal_claim_allowed": False,
                "blockers": ["h02_verdict_not_formal", "missing_module2_rl_rs_checkpoint"],
            }
        ),
        encoding="utf-8",
    )
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(
        json.dumps(
            {
                "status": "blocked_formal_output_acceptance",
                "formal_output_accepted": False,
                "paper_result_input_allowed": False,
                "blockers": ["h02_verdict_not_formal", "missing_ppo_result_rows"],
            }
        ),
        encoding="utf-8",
    )
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(
        json.dumps(
            {
                "status": "blocked_pending_decisions",
                "blockers": ["f02_6_decision_packet_pending", "missing_module2_rl_rs_checkpoint"],
            }
        ),
        encoding="utf-8",
    )
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(
        json.dumps(
            {
                "status": "pending_human_decision",
                "recommendation": {"decision": "approve_obstacle_summary_warm_start"},
                "blockers": ["requires_dr_sun_approval"],
            }
        ),
        encoding="utf-8",
    )
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(
        json.dumps(
            {
                "formal_decision": "fail",
                "formal_claim_allowed": True,
                "formal_blockers": [],
                "terminal_rs_success_rate": 0.453125,
                "episodes": 64,
                "success_threshold": 0.8,
                "warm_start_status": "not_applied_f02_6_pending",
            }
        ),
        encoding="utf-8",
    )
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=True)), encoding="utf-8")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(_status_report_payload(ready=True)), encoding="utf-8")
    draft = tmp_path / "draft.md"
    draft.write_text(
        "Our method is globally optimal. RL replaces Hybrid A*. No-warm Gate #3 formal failed.",
        encoding="utf-8",
    )
    manifest_path = tmp_path / "claim_safety.json"
    markdown_path = tmp_path / "claim_safety.md"

    rc = builder.main(
        [
            "--paper-tables",
            str(paper_tables),
            "--h02-formal-acceptance",
            str(h02_formal_acceptance),
            "--h01-manifest",
            str(h01_manifest),
            "--f02-6-packet",
            str(f02_6_packet),
            "--gate3-audit",
            str(gate3_audit),
            "--method-algorithms",
            str(method_algorithms),
            "--system-diagram",
            str(system_diagram),
            "--closure-checklist",
            str(closure_checklist),
            "--status-report",
            str(status_report),
            "--draft-text",
            str(draft),
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
    assert manifest["artifact_name"] == "module2_claim_safety"
    assert manifest["status"] == "blocked_formal_performance_claims"
    assert manifest["formal_performance_claim_allowed"] is False
    assert manifest["input_status"]["h02_formal_acceptance_status"] == "blocked_formal_output_acceptance"
    assert "h02_formal_acceptance_not_accepted" in manifest["formal_performance_blockers"]
    assert "missing_ppo_result_rows" in manifest["formal_performance_blockers"]
    assert "missing_module2_rl_rs_checkpoint" in manifest["formal_performance_blockers"]
    assert "f02_6_pending" in manifest["formal_performance_blockers"]
    assert "formal_gate_closure_checklist_open" in manifest["formal_performance_blockers"]
    assert manifest["input_status"]["closure_checklist_status"] == "formal_gate_closure_blocked"
    assert manifest["input_status"]["status_report_status"] == "formal_gate_status_ready_for_claim_audit"
    assert manifest["input_status"]["status_report_next_blocked_lane_id"] is None
    assert manifest["input_status"]["status_report_decision_intake_status"] == "f02_6_decision_intake_closed_clean"
    assert manifest["input_status"]["status_report_decision_intake_record_status"] == "approved"
    assert manifest["input_status"]["status_report_decision_intake_audit_issue_count"] == 0
    assert manifest["input_status"]["status_report_decision_intake_decision_owner_required"] == "Dr Sun"
    assert manifest["input_status"]["status_report_decision_intake_valid_decision_count"] == 2
    assert manifest["input_status"]["status_report_decision_intake_required_record_field_count"] == 3
    assert manifest["input_status"]["status_report_decision_intake_decision_note_required"] is True
    assert manifest["input_status"]["status_report_decision_intake_invalid_input_count"] == 2
    assert manifest["input_status"]["status_report_decision_intake_post_decision_non_authorization_count"] == 2
    assert manifest["input_status"]["status_report_decision_intake_post_decision_route_count"] == 2
    assert manifest["input_status"]["status_report_decision_intake_approved_route_next_lane"] == "source_fresh_regeneration"
    assert manifest["input_status"]["status_report_decision_intake_approved_route_allows_remote_training_now"] is False
    assert manifest["input_status"]["status_report_decision_intake_rejected_route_requires_new_protocol_contract"] is True
    assert manifest["input_status"]["status_report_handoff_status"] == "ready_for_manual_remote_execution_review"
    assert manifest["input_status"]["status_report_transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["input_status"]["status_report_transition_gate_audit_issue_count"] == 0
    assert manifest["input_status"]["status_report_handoff_safety_issue_count"] == 0
    assert manifest["input_status"]["status_report_missing_artifacts_handoff_status"] == "formal_gate_evidence_ready_for_h01_h02_claim_gates"
    assert manifest["input_status"]["status_report_missing_artifacts_open_requirement_count"] == 0
    assert manifest["input_status"]["status_report_missing_artifacts_remote_training_allowed_now"] is True
    assert manifest["input_status"]["status_report_missing_artifacts_formal_result_material_allowed_now"] is False
    assert manifest["input_status"]["status_report_requirement_stage_mapped_count"] == 4
    assert manifest["input_status"]["status_report_requirement_stage_unmapped_count"] == 0
    assert manifest["input_status"]["status_report_requirement_stage_mismatched_count"] == 0
    assert manifest["input_status"]["status_report_requirement_stage_blocked_stage_count"] == 0
    assert manifest["input_status"]["status_report_closure_remote_training_allowed_now"] is True
    assert manifest["input_status"]["status_report_remote_packet_training_allowed_now"] is True
    assert manifest["input_status"]["status_report_remote_preflight_requirement_present"] is True
    assert manifest["input_status"]["status_report_remote_preflight_requirement_satisfied_count"] == 4
    assert manifest["input_status"]["status_report_remote_preflight_requirement_blocked_count"] == 0
    assert manifest["input_status"]["status_report_post_run_acceptance_requirement_present"] is True
    assert manifest["input_status"]["status_report_post_run_acceptance_requirement_satisfied_count"] == 4
    assert manifest["input_status"]["status_report_post_run_acceptance_requirement_blocked_count"] == 0
    assert manifest["input_status"]["status_report_h02_formal_acceptance_requirement_present"] is True
    assert manifest["input_status"]["status_report_h02_formal_acceptance_requirement_satisfied_count"] == 4
    assert manifest["input_status"]["status_report_h02_formal_acceptance_requirement_blocked_count"] == 0
    assert manifest["input_status"]["status_report_remaining_deliverables_acceptance_present"] is True
    assert manifest["input_status"]["status_report_remaining_deliverables_acceptance_matrix_row_count"] == 10
    assert manifest["input_status"]["status_report_remaining_deliverables_acceptance_missing_row_count"] == 0
    assert manifest["input_status"]["status_report_remaining_deliverables_acceptance_blocked_category_count"] == 0
    assert manifest["input_status"]["status_report_remaining_deliverables_gap_present"] is True
    assert manifest["input_status"]["status_report_remaining_deliverables_gap_total_missing_deliverables"] == 0
    assert manifest["input_status"]["status_report_remaining_deliverables_gap_open_category_count"] == 0
    assert manifest["input_status"]["status_report_formal_gate_gap_audit_remaining_deliverables_gap_present"] is True
    assert manifest["input_status"]["status_report_formal_gate_gap_audit_remaining_deliverables_gap_total_missing_deliverables"] == 0
    assert manifest["input_status"]["status_report_formal_gate_gap_audit_remaining_deliverables_gap_open_category_count"] == 0
    assert manifest["input_status"]["status_report_remaining_deliverables_proof_plan_present"] is True
    assert manifest["input_status"]["status_report_remaining_deliverables_proof_plan_matrix_row_count"] == 10
    assert manifest["input_status"]["status_report_remaining_deliverables_proof_plan_command_count"] == 20
    assert manifest["status_report_handoff_summary"]["transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["status_report_missing_artifacts_handoff_summary"]["status"] == "formal_gate_evidence_ready_for_h01_h02_claim_gates"
    assert manifest["status_report_requirement_stage_summary"]["mapped_requirement_count"] == 4
    assert manifest["status_report_requirement_stage_summary"]["requirements"]["training_remote_ppo_checkpoint"][
        "responsible_stage_id"
    ] == "gate3_remote_training"
    assert manifest["status_report_remote_gate_summary"]["closure_remote_stage_summary"]["gate3_remote_training"] == {
        "present": True,
        "status": "ready",
        "allowed_now": True,
        "runs_training": True,
        "runs_remote_preflight": False,
        "host": "gpu3070ti-relay",
        "blocked_by": [],
    }
    assert manifest["status_report_remote_gate_summary"]["remote_execution_step_summary"]["run_remote_training"] == {
        "present": True,
        "status": None,
        "allowed_now": True,
        "runs_training": True,
        "runs_remote_preflight": None,
        "host": None,
        "blocked_by": [],
    }
    assert manifest["status_report_h02_acceptance_requirement_summary"]["status_counts"] == {"satisfied": 4}
    assert manifest["status_report_remaining_deliverables_acceptance_summary"]["matrix_row_count"] == 10
    assert manifest["status_report_remaining_deliverables_acceptance_summary"]["missing_row_count"] == 0
    assert manifest["status_report_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 0
    assert manifest["status_report_remaining_deliverables_gap_summary"]["open_category_count"] == 0
    assert manifest["status_report_formal_gate_gap_audit_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 0
    assert manifest["status_report_formal_gate_gap_audit_remaining_deliverables_gap_summary"]["open_category_count"] == 0
    proof_plan = manifest["status_report_remaining_deliverables_proof_command_plan"]
    assert proof_plan["present"] is True
    assert proof_plan["plan_id"] == "module2_formal_gate_local_read_only_proof_commands"
    assert proof_plan["execution_boundary"] == "local_read_only_after_formal_remote_pullback"
    assert proof_plan["total_matrix_rows"] == 10
    assert proof_plan["total_proof_command_count"] == 20
    assert proof_plan["rows"]["training:train_final_model_zip"]["proof_command_ids"] == [
        "train_final_model_zip_exists",
        "train_final_model_zip_schema",
    ]
    command_index = manifest["status_report_remote_packet_safety_claim_gate_command_index_summary"]
    assert command_index["present"] is True
    assert command_index["index_row_count"] == 18
    assert command_index["source_target_count"] == 18
    assert command_index["missing_target_ids"] == []
    assert command_index["claim_gate_rows"]["claim_safety"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert command_index["claim_gate_rows"]["paper_readiness"]["required_before"] == "formal_claim_gate"
    assert manifest["input_status"]["status_report_remote_packet_safety_command_index_present"] is True
    assert manifest["input_status"]["status_report_remote_packet_safety_command_index_row_count"] == 18
    assert manifest["status_report_decision_intake_summary"]["status"] == "f02_6_decision_intake_closed_clean"
    assert manifest["status_report_decision_intake_summary"]["record_status"] == "approved"
    assert manifest["status_report_decision_intake_summary"]["decision_owner_required"] == "Dr Sun"
    assert manifest["status_report_decision_intake_summary"]["decision_note_required"] is True
    assert manifest["status_report_decision_intake_summary"]["post_decision_route_count"] == 2
    assert manifest["status_report_decision_intake_summary"]["approved_route_next_lane"] == "source_fresh_regeneration"
    assert manifest["status_report_decision_intake_summary"]["approved_route_allows_remote_training_now"] is False
    assert manifest["status_report_decision_intake_summary"]["rejected_route_requires_new_protocol_contract"] is True

    allowed_ids = {item["claim_id"] for item in manifest["allowed_claims"]}
    assert "method_is_ha_star_analytic_operator" in allowed_ids
    assert "no_warm_gate3_formal_failure" in allowed_ids
    no_warm = next(item for item in manifest["allowed_claims"] if item["claim_id"] == "no_warm_gate3_formal_failure")
    assert no_warm["scope"] == "no_warm_only"
    assert "0.453125" in no_warm["claim_text"]

    prohibited_ids = {item["claim_id"] for item in manifest["prohibited_claims"]}
    assert {"global_optimality", "completeness_enhancement", "rl_replaces_hybrid_astar", "universal_generalization"} <= prohibited_ids

    violations = manifest["draft_audit"]["violations"]
    assert {item["claim_id"] for item in violations} >= {"global_optimality", "rl_replaces_hybrid_astar"}
    assert manifest["draft_audit"]["status"] == "violations_found"

    assert "# Module2 Claim Safety" in markdown
    assert "not allowed" in markdown
    assert "no-warm" in markdown
    assert "decision_owner_required" in markdown
    assert "decision_note_required" in markdown


def test_claim_safety_refuses_formal_claim_when_h02_acceptance_is_blocked_even_if_tables_are_formal(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(
        json.dumps(
            {
                "status": "blocked_formal_output_acceptance",
                "formal_output_accepted": False,
                "paper_result_input_allowed": False,
                "blockers": ["missing_remote_pullback_artifacts"],
            }
        ),
        encoding="utf-8",
    )
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(_status_report_payload(ready=True)), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    assert manifest["status"] == "blocked_formal_performance_claims"
    assert manifest["formal_performance_claim_allowed"] is False
    assert manifest["formal_performance_blockers"] == [
        "h02_formal_acceptance_not_accepted",
        "missing_remote_pullback_artifacts",
    ]


def test_claim_safety_blocks_formal_claim_when_closure_checklist_is_open(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(
        json.dumps(
            {
                "status": "formal_output_accepted",
                "formal_output_accepted": True,
                "paper_result_input_allowed": True,
                "blockers": [],
            }
        ),
        encoding="utf-8",
    )
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=True)), encoding="utf-8")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(_status_report_payload(ready=True)), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    assert manifest["status"] == "blocked_formal_performance_claims"
    assert manifest["formal_performance_claim_allowed"] is False
    assert manifest["formal_performance_blockers"] == ["formal_gate_closure_checklist_open"]


def test_claim_safety_rejects_closure_checklist_that_runs_or_claims(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False, invalid=True)), encoding="utf-8")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(_status_report_payload(ready=True)), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "closure_checklist_executes_commands" in blockers
    assert "closure_checklist_runs_training" in blockers
    assert "closure_checklist_runs_remote_preflight" in blockers
    assert "closure_checklist_allows_local_training" in blockers
    assert "closure_checklist_allows_formal_claim" in blockers
    assert "closure_checklist_input_safety_issues_open" in blockers


def test_claim_safety_blocks_formal_claim_when_status_report_is_blocked(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(_status_report_payload(ready=False)), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    assert manifest["status"] == "blocked_formal_performance_claims"
    assert manifest["formal_performance_claim_allowed"] is False
    assert "formal_gate_status_report_blocked" in manifest["formal_performance_blockers"]
    assert "status_report_remaining_deliverables_gap_rows_missing" in manifest["formal_performance_blockers"]
    assert "status_report_remaining_deliverables_gap_categories_blocked" in manifest["formal_performance_blockers"]
    assert "status_report_formal_gate_gap_audit_remaining_deliverables_gap_rows_missing" in manifest["formal_performance_blockers"]
    assert "status_report_formal_gate_gap_audit_remaining_deliverables_gap_categories_blocked" in manifest["formal_performance_blockers"]
    assert manifest["input_status"]["status_report_status"] == "formal_gate_status_blocked"
    assert manifest["input_status"]["status_report_next_blocked_lane_id"] == "decision"
    assert manifest["input_status"]["status_report_decision_intake_status"] == "f02_6_decision_intake_pending_clean"
    assert manifest["input_status"]["status_report_decision_intake_record_status"] == "pending_human_decision"
    assert manifest["input_status"]["status_report_decision_intake_audit_issue_count"] == 0
    assert manifest["input_status"]["status_report_decision_intake_remote_training_allowed_now"] is False
    assert manifest["input_status"]["status_report_decision_intake_formal_claim_allowed_now"] is False
    assert manifest["input_status"]["status_report_closure_remote_training_allowed_now"] is False
    assert manifest["input_status"]["status_report_remote_packet_training_allowed_now"] is False
    assert manifest["status_report_remote_gate_summary"]["closure_remote_stage_summary"]["gate3_remote_training"][
        "blocked_by"
    ] == ["f02_6_decision_not_approved", "source_fresh_preflight_targets_open", "remote_packet_not_ready"]
    assert manifest["status_report_remote_gate_summary"]["remote_execution_step_summary"]["run_remote_training"][
        "blocked_by"
    ] == [
        "requires_dr_sun_approval",
        "f02_6_warm_start_decision_pending",
        "missing_module2_rl_rs_checkpoint",
        "remote_packet_not_ready",
    ]


def test_claim_safety_rejects_status_report_remote_safety_command_index_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    summary = status_payload["remote_packet_safety_claim_gate_command_index_summary"]
    summary["missing_target_ids"] = ["paper_readiness"]
    summary["unknown_manual_count"] = 1
    summary["forbidden_command_count"] = 1
    summary["claim_gate_rows"]["claim_safety"]["stage_id"] = "regenerate_preflight_gate_artifacts"
    summary["claim_gate_rows"]["claim_safety"]["command_kind"] = "unknown_manual"
    summary["claim_gate_rows"].pop("paper_readiness")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert manifest["status"] == "blocked_formal_performance_claims"
    assert "status_report_remote_packet_safety_command_index_missing_targets" in blockers
    assert "status_report_remote_packet_safety_command_index_unknown_manual_rows" in blockers
    assert "status_report_remote_packet_safety_command_index_forbidden_commands" in blockers
    assert "status_report_remote_packet_safety_command_index_claim_safety_wrong_stage" in blockers
    assert "status_report_remote_packet_safety_command_index_claim_safety_manual_command" in blockers
    assert "status_report_remote_packet_safety_command_index_missing_paper_readiness" in blockers


def test_claim_safety_rejects_status_report_without_remote_gate_summaries(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    status_payload.pop("closure_remote_stage_summary")
    status_payload.pop("remote_execution_step_summary")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_missing_closure_remote_stage_summary" in blockers
    assert "status_report_missing_remote_execution_step_summary" in blockers
    assert "status_report_missing_gate3_remote_training" in blockers
    assert "status_report_missing_run_remote_training" in blockers
    assert "status_report_closure_training_stage_not_marked_training" in blockers
    assert "status_report_remote_training_step_not_marked_training" in blockers


def test_claim_safety_rejects_status_report_without_clean_decision_intake_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    status_payload["f02_6_decision_intake_summary"]["status"] = "f02_6_decision_intake_failed"
    status_payload["f02_6_decision_intake_summary"]["audit_issue_count"] = 1
    status_payload["f02_6_decision_intake_summary"]["record_decider"] = "Assistant"
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_f02_6_decision_intake_not_clean" in blockers
    assert "status_report_f02_6_decision_intake_audit_issues_open" in blockers
    assert "status_report_closed_f02_6_intake_decider_not_dr_sun" in blockers


def test_claim_safety_rejects_status_report_without_handoff_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    status_payload.pop("formal_gate_handoff_summary")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    assert manifest["status"] == "blocked_formal_performance_claims"
    assert "status_report_missing_formal_gate_handoff_summary" in manifest["formal_performance_blockers"]


def test_claim_safety_rejects_status_report_without_missing_artifacts_handoff_index(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    status_payload.pop("missing_artifacts_handoff_index_summary")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    assert "status_report_missing_artifacts_handoff_index_missing" in manifest["formal_performance_blockers"]
    assert manifest["status_report_missing_artifacts_handoff_summary"]["present"] is False


def test_claim_safety_rejects_status_report_requirement_stage_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(
        json.dumps(
            {
                "status": "formal_output_accepted",
                "formal_output_accepted": True,
                "paper_result_input_allowed": True,
                "blockers": [],
            }
        ),
        encoding="utf-8",
    )
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=False)
    stage_summary = status_payload["formal_gate_requirement_stage_summary"]
    stage_summary["unmapped_requirement_count"] = 1
    stage_summary["mismatched_requirement_count"] = 1
    stage_summary["requirements"]["training_remote_ppo_checkpoint"]["responsible_stage_id"] = None
    stage_summary["requirements"]["training_remote_ppo_checkpoint"]["mapping_present"] = False
    stage_summary["requirements"]["evaluation_gate3_episode_outputs"]["responsible_stage_id"] = "wrong_stage"
    stage_summary["requirements"]["evaluation_gate3_episode_outputs"]["mapping_matches_expected"] = False
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_requirement_stage_unmapped" in blockers
    assert "status_report_requirement_stage_mismatched" in blockers
    assert "status_report_training_remote_ppo_checkpoint_missing_responsible_stage" in blockers
    assert "status_report_evaluation_gate3_episode_outputs_wrong_responsible_stage" in blockers
    assert manifest["status_report_requirement_stage_summary"]["unmapped_requirement_count"] == 1
    assert manifest["status_report_requirement_stage_summary"]["mismatched_requirement_count"] == 1


def test_claim_safety_rejects_status_report_with_bad_transition_or_handoff_safety(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=False)
    handoff = status_payload["formal_gate_handoff_summary"]
    handoff["transition_gate_status"] = "f02_6_transition_gate_audit_failed"
    handoff["transition_gate_audit_issue_count"] = 1
    handoff["safety_issue_count"] = 1
    handoff["remote_preflight_allowed_now"] = True
    handoff["remote_training_allowed_now"] = True
    handoff["formal_claim_allowed_now"] = True
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_transition_gate_not_passed" in blockers
    assert "status_report_transition_gate_issues_open" in blockers
    assert "status_report_handoff_safety_issues_open" in blockers
    assert "status_report_blocked_but_handoff_remote_preflight_allowed" in blockers
    assert "status_report_blocked_but_handoff_remote_training_allowed" in blockers
    assert "status_report_blocked_but_handoff_formal_claim_allowed" in blockers


def test_claim_safety_rejects_blocked_status_report_that_allows_remote_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=False)
    status_payload["closure_remote_stage_summary"]["gate3_remote_training"]["allowed_now"] = True
    status_payload["remote_execution_step_summary"]["run_remote_training"]["allowed_now"] = True
    status_payload["missing_artifacts_handoff_index_summary"]["remote_training_allowed_now"] = True
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "formal_gate_status_report_blocked" in blockers
    assert "status_report_blocked_but_gate3_remote_training_allowed" in blockers
    assert "status_report_blocked_but_run_remote_training_allowed" in blockers
    assert "status_report_blocked_but_missing_artifacts_handoff_remote_training_allowed" in blockers


def test_claim_safety_rejects_status_report_remote_requirement_matrix_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=False)
    status_payload.pop("remote_preflight_requirement_summary")
    post_run = status_payload["post_run_acceptance_requirement_summary"]["requirements"]
    post_run["checkpoint_hash_manifest_recorded"]["acceptable_evidence_count"] = 0
    post_run["gate3_formal_audit_accepts_remote_run"]["execution_allowed_now"] = True
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_remote_preflight_requirement_summary_missing" in blockers
    assert (
        "status_report_post_run_acceptance_requirement_checkpoint_hash_manifest_recorded_missing_acceptable_evidence"
        in blockers
    )
    assert (
        "status_report_post_run_acceptance_requirement_gate3_formal_audit_accepts_remote_run_allowed_while_status_blocked"
        in blockers
    )
    assert manifest["status_report_remote_requirement_summary"]["remote_preflight_requirement_summary"]["present"] is False


def test_claim_safety_rejects_status_report_h02_acceptance_requirement_matrix_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=False)
    h02_summary = status_payload["h02_formal_acceptance_requirement_summary"]
    h02_summary["requirements"]["h02_formal_scope_and_scale_match_h01"]["paper_result_input_allowed_now"] = True
    h02_summary["requirements"]["gate3_audit_and_pullback_acceptance"]["acceptable_evidence_count"] = 0
    h02_summary["missing_requirement_ids"] = ["ppo_rows_and_checkpoint_hash_present"]
    h02_summary["requirements"].pop("ppo_rows_and_checkpoint_hash_present")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert (
        "status_report_h02_formal_acceptance_requirement_h02_formal_scope_and_scale_match_h01_allows_paper_result_while_status_blocked"
        in blockers
    )
    assert (
        "status_report_h02_formal_acceptance_requirement_gate3_audit_and_pullback_acceptance_missing_acceptable_evidence"
        in blockers
    )
    assert "status_report_h02_formal_acceptance_requirement_missing_ppo_rows_and_checkpoint_hash_present" in blockers
    assert manifest["status_report_h02_acceptance_requirement_summary"]["requirements"][
        "ppo_rows_and_checkpoint_hash_present"
    ]["present"] is False


def test_claim_safety_rejects_status_report_remaining_deliverables_acceptance_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    summary = status_payload["remaining_deliverables_acceptance_summary"]
    summary["rows"]["training:train_final_model_zip"]["acceptance_predicate_count"] = 0
    summary["rows"]["training:train_final_model_zip"]["proof_command_count"] = 0
    summary["rows"]["training:train_final_model_zip"]["proof_command_ids"] = []
    summary["rows"]["training:train_summary_json"]["responsible_stage_allowed_now"] = True
    summary["rows"].pop("formal_acceptance:h02_formal_output_acceptance")
    summary["matrix_row_count"] = 9
    proof_plan = status_payload["remaining_deliverables_proof_command_plan"]
    proof_plan["total_matrix_rows"] = 8
    proof_plan["total_proof_command_count"] = 17
    proof_plan["rows"].pop("formal_acceptance:h02_formal_output_acceptance")
    proof_plan["runs_training"] = True
    gap_summary = status_payload["remaining_deliverables_gap_summary"]
    gap_summary["total_missing_deliverables"] = 1
    gap_summary["open_category_count"] = 1
    gap_summary["category_order"] = ["training", "evaluation"]
    gap_summary["categories"]["training"]["missing_count"] = 1
    gap_summary["categories"]["training"]["missing_artifact_matrix_ids"] = []
    gap_summary["categories"]["training"]["proof_command_ids"] = []
    formal_gate_gap_summary = status_payload["formal_gate_gap_audit_remaining_deliverables_gap_summary"]
    formal_gate_gap_summary["total_missing_deliverables"] = 2
    formal_gate_gap_summary["open_category_count"] = 1
    formal_gate_gap_summary["categories"]["training"]["missing_count"] = 2
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_remaining_deliverables_acceptance_matrix_count_mismatch" in blockers
    assert "status_report_remaining_deliverables_acceptance_training_train_final_model_zip_missing_predicates" in blockers
    assert "status_report_remaining_deliverables_acceptance_training_train_final_model_zip_missing_proof_commands" in blockers
    assert "status_report_remaining_deliverables_acceptance_missing_formal_acceptance_h02_formal_output_acceptance" in blockers
    assert "status_report_remaining_deliverables_proof_command_plan_runs_training" in blockers
    assert "status_report_remaining_deliverables_proof_command_plan_matrix_count_mismatch" in blockers
    assert "status_report_remaining_deliverables_proof_command_plan_command_count_mismatch" in blockers
    assert "status_report_remaining_deliverables_proof_command_plan_missing_formal_acceptance_h02_formal_output_acceptance" in blockers
    assert "status_report_remaining_deliverables_gap_category_order_mismatch" in blockers
    assert "status_report_remaining_deliverables_gap_rows_missing_while_status_ready" in blockers
    assert "status_report_remaining_deliverables_gap_categories_blocked_while_status_ready" in blockers
    assert "status_report_remaining_deliverables_gap_training_missing_artifact_count_mismatch" in blockers
    assert "status_report_formal_gate_gap_audit_remaining_deliverables_gap_mismatch" in blockers
    assert "status_report_formal_gate_gap_audit_remaining_deliverables_gap_rows_missing" in blockers
    assert "status_report_formal_gate_gap_audit_remaining_deliverables_gap_categories_blocked" in blockers
    assert manifest["status_report_remaining_deliverables_acceptance_summary"]["matrix_row_count"] == 9
    assert manifest["status_report_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 1
    assert manifest["status_report_formal_gate_gap_audit_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 2
    assert manifest["status_report_remaining_deliverables_proof_command_plan"]["total_matrix_rows"] == 8


def test_claim_safety_rejects_status_report_decision_intake_contract_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=True)
    intake = status_payload["f02_6_decision_intake_summary"]
    intake["decision_owner_required"] = "Assistant"
    intake["valid_decisions"] = ["approve_obstacle_summary_warm_start"]
    intake["required_record_fields"] = ["decision", "decider"]
    intake["decision_note_required"] = False
    intake["invalid_input_count"] = 0
    intake["post_decision_non_authorization_count"] = 0
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_f02_6_decision_intake_decision_owner_not_dr_sun" in blockers
    assert "status_report_f02_6_decision_intake_valid_decisions_incomplete" in blockers
    assert "status_report_f02_6_decision_intake_required_fields_incomplete" in blockers
    assert "status_report_f02_6_decision_intake_decision_note_not_required" in blockers
    assert "status_report_f02_6_decision_intake_invalid_inputs_missing" in blockers
    assert "status_report_f02_6_decision_intake_non_authorizations_missing" in blockers
    assert manifest["status_report_decision_intake_summary"]["decision_owner_required"] == "Assistant"


def test_claim_safety_rejects_status_report_decision_intake_route_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_payload = _status_report_payload(ready=False)
    intake = status_payload["f02_6_decision_intake_summary"]
    intake["post_decision_route_count"] = 1
    intake["post_decision_route_decisions"] = ["approve_obstacle_summary_warm_start"]
    intake["approved_route_next_lane"] = "remote_training"
    intake["approved_route_allows_remote_training_now"] = True
    intake["rejected_route_requires_new_protocol_contract"] = False
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(status_payload), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_f02_6_decision_intake_route_decisions_incomplete" in blockers
    assert "status_report_f02_6_decision_intake_approved_route_next_lane_invalid" in blockers
    assert "status_report_f02_6_decision_intake_approved_route_allows_remote_training" in blockers
    assert "status_report_f02_6_decision_intake_rejected_route_missing_protocol_contract" in blockers


def test_claim_safety_rejects_status_report_that_runs_or_claims(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_claim_safety")
    paper_tables = tmp_path / "paper_tables.json"
    paper_tables.write_text(json.dumps({"status": "formal_ready", "formal_claim_allowed": True, "blockers": []}), encoding="utf-8")
    h02_formal_acceptance = tmp_path / "h02_formal_acceptance.json"
    h02_formal_acceptance.write_text(json.dumps({"status": "formal_output_accepted", "formal_output_accepted": True, "paper_result_input_allowed": True, "blockers": []}), encoding="utf-8")
    h01_manifest = tmp_path / "h01.json"
    h01_manifest.write_text(json.dumps({"status": "ready_for_formal_evaluation", "blockers": []}), encoding="utf-8")
    f02_6_packet = tmp_path / "f02_6.json"
    f02_6_packet.write_text(json.dumps({"status": "approved", "blockers": []}), encoding="utf-8")
    gate3_audit = tmp_path / "gate3_audit.json"
    gate3_audit.write_text(json.dumps({"formal_decision": "pass", "formal_claim_allowed": True}), encoding="utf-8")
    method_algorithms = tmp_path / "method_algorithms.json"
    method_algorithms.write_text(json.dumps({"status": "code_anchored"}), encoding="utf-8")
    system_diagram = tmp_path / "system_diagram.json"
    system_diagram.write_text(json.dumps({"status": "code_anchored_drawio"}), encoding="utf-8")
    closure_checklist = tmp_path / "closure_checklist.json"
    closure_checklist.write_text(json.dumps(_closure_checklist_payload(open_checklist=False)), encoding="utf-8")
    status_report = tmp_path / "status_report.json"
    status_report.write_text(json.dumps(_status_report_payload(ready=True, invalid=True)), encoding="utf-8")

    manifest = builder.build_manifest(
        repo_root=builder._repo_root(),
        paper_tables_path=paper_tables,
        h02_formal_acceptance_path=h02_formal_acceptance,
        h01_manifest_path=h01_manifest,
        f02_6_packet_path=f02_6_packet,
        gate3_audit_path=gate3_audit,
        method_algorithms_path=method_algorithms,
        system_diagram_path=system_diagram,
        closure_checklist_path=closure_checklist,
        status_report_path=status_report,
    )

    blockers = set(manifest["formal_performance_blockers"])
    assert "status_report_executes_commands" in blockers
    assert "status_report_runs_training" in blockers
    assert "status_report_runs_remote_preflight" in blockers
    assert "status_report_allows_local_training" in blockers
    assert "status_report_allows_formal_claim" in blockers
    assert "status_report_allows_local_training_now" in blockers
    assert "status_report_input_safety_issues_open" in blockers


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
    status = "ready" if ready else "blocked"
    training_blockers = [] if ready else ["f02_6_decision_not_approved", "source_fresh_preflight_targets_open", "remote_packet_not_ready"]
    proof_summary = _status_report_remote_safety_proof_summary_payload(ready=ready)
    remote_training_blockers = (
        []
        if ready
        else [
            "requires_dr_sun_approval",
            "f02_6_warm_start_decision_pending",
            "missing_module2_rl_rs_checkpoint",
            "remote_packet_not_ready",
        ]
    )
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
        "formal_gate_handoff_summary": {
            "present": True,
            "status": "ready_for_manual_remote_execution_review" if ready else "blocked_until_f02_6_decision",
            "transition_gate_status": "f02_6_transition_gate_audit_passed",
            "transition_gate_audit_issue_count": 0,
            "next_handoff_action_id": None if ready else "record_f02_6_decision",
            "next_action_requires_dr_sun": not ready,
            "safety_issue_count": 0,
            "remote_training_allowed_now": bool(ready),
            "remote_preflight_allowed_now": bool(ready),
            "formal_claim_allowed_now": bool(ready),
        },
        "f02_6_decision_intake_summary": {
            "present": True,
            "status": "f02_6_decision_intake_closed_clean" if ready else "f02_6_decision_intake_pending_clean",
            "audit_issue_count": 0,
            "record_status": "approved" if ready else "pending_human_decision",
            "record_decider": "Dr Sun" if ready else None,
            "next_blocked_lane": None if ready else "decision",
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
            "remote_preflight_allowed_now": bool(ready),
            "remote_training_allowed_now": bool(ready),
            "formal_claim_allowed_now": bool(ready),
        },
        "missing_artifacts_handoff_index_summary": {
            "present": True,
            "status": "formal_gate_evidence_ready_for_h01_h02_claim_gates"
            if ready
            else "blocked_until_f02_6_decision",
            "next_action_id": None if ready else "record_f02_6_decision",
            "next_action_requires_dr_sun": not ready,
            "next_action_allowed_for_agent_now": False,
            "open_requirement_count": 0 if ready else 5,
            "local_training_allowed_now": False,
            "remote_training_allowed_now": bool(ready),
            "formal_result_material_allowed_now": False,
        },
        "formal_gate_requirement_stage_summary": _status_report_requirement_stage_summary_payload(ready=ready),
        "remote_preflight_requirement_summary": _status_report_remote_preflight_requirement_summary_payload(ready=ready),
        "post_run_acceptance_requirement_summary": _status_report_post_run_acceptance_requirement_summary_payload(
            ready=ready
        ),
        "h02_formal_acceptance_requirement_summary": _status_report_h02_acceptance_requirement_summary_payload(
            ready=ready
        ),
        "remaining_deliverables_acceptance_summary": _status_report_remaining_deliverables_acceptance_summary_payload(
            ready=ready
        ),
        "remaining_deliverables_gap_summary": _status_report_remaining_deliverables_gap_summary_payload(ready=ready),
        "formal_gate_gap_audit_remaining_deliverables_gap_summary": _status_report_remaining_deliverables_gap_summary_payload(
            ready=ready
        ),
        "remaining_deliverables_proof_command_plan": _status_report_remaining_deliverables_proof_command_plan_payload(
            ready=ready
        ),
        "remote_packet_safety_proof_deliverables_summary": proof_summary,
        "remote_packet_safety_status_report_proof_deliverables_summary": json.loads(json.dumps(proof_summary)),
        "remote_packet_safety_claim_gate_command_index_summary": _status_report_command_index_summary(),
        "closure_remote_stage_summary": {
            "approved_remote_preflight": {
                "present": True,
                "status": status,
                "allowed_now": bool(ready),
                "runs_training": False,
                "runs_remote_preflight": True,
                "host": "gpu3070ti-relay",
                "blocked_by": [] if ready else ["f02_6_decision_not_approved", "source_fresh_preflight_targets_open"],
            },
            "gate3_remote_training": {
                "present": True,
                "status": status,
                "allowed_now": bool(ready),
                "runs_training": True,
                "runs_remote_preflight": False,
                "host": "gpu3070ti-relay",
                "blocked_by": training_blockers,
            },
            "gate3_remote_audit_pullback": {
                "present": True,
                "status": status,
                "allowed_now": bool(ready),
                "runs_training": False,
                "runs_remote_preflight": False,
                "host": "gpu3070ti-relay",
                "blocked_by": training_blockers,
            },
        },
        "remote_execution_step_summary": {
            "sync_to_remote": {
                "present": True,
                "allowed_now": bool(ready),
                "runs_training": False,
                "blocked_by": [] if ready else ["requires_dr_sun_approval"],
            },
            "run_remote_preflight": {
                "present": True,
                "allowed_now": bool(ready),
                "runs_training": False,
                "blocked_by": [] if ready else ["requires_dr_sun_approval"],
            },
            "run_remote_training": {
                "present": True,
                "allowed_now": bool(ready),
                "runs_training": True,
                "blocked_by": remote_training_blockers,
            },
            "run_remote_audit": {
                "present": True,
                "allowed_now": bool(ready),
                "runs_training": False,
                "blocked_by": remote_training_blockers,
            },
        },
    }


def _status_report_command_index_summary():
    rows = {
        f"source_target_{index}": {
            "stage_id": "regenerate_preflight_gate_artifacts",
            "required_before": "approved_remote_preflight",
            "command_kind": "known_builder",
            "command_template": f"PYTHONPATH=2_experiment python -m builder_{index}",
        }
        for index in range(16)
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
        "index_row_count": 18,
        "source_target_count": 18,
        "missing_target_ids": [],
        "unknown_manual_count": 0,
        "unknown_manual_ids": [],
        "forbidden_command_count": 0,
        "forbidden_command_ids": [],
        "claim_gate_rows": {
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


def _status_report_remote_safety_proof_summary_payload(*, ready):
    gap = _status_report_remaining_deliverables_gap_summary_payload(ready=ready)
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
        "next_blocked_lane": None if ready else "decision",
        "h01_status": "ready_for_formal_run" if ready else "blocked_pending_decisions",
        "h02_status": "formal_output_accepted" if ready else "blocked_formal_output_acceptance",
        "h02_formal_output_accepted": bool(ready),
        "h02_paper_result_input_allowed": bool(ready),
    }


def _status_report_remote_preflight_requirement_summary_payload(*, ready):
    requirements = {
        "f02_6_decision_closed_for_preflight": _status_report_remote_requirement_row(
            requirement_id="f02_6_decision_closed_for_preflight",
            phase="decision",
            status="satisfied" if ready else "blocked_missing_preflight",
            complete=ready,
            execution_allowed_now=ready,
            blocked_by=[] if ready else ["requires_dr_sun_approval"],
        ),
        "approved_remote_preflight_manifest": _status_report_remote_requirement_row(
            requirement_id="approved_remote_preflight_manifest",
            phase="remote_preflight",
            status="satisfied" if ready else "blocked_missing_preflight",
            complete=ready,
            execution_allowed_now=ready,
            blocked_by=[] if ready else ["warm_start_decision_pending"],
        ),
        "remote_preflight_protocol_contract": _status_report_remote_requirement_row(
            requirement_id="remote_preflight_protocol_contract",
            phase="remote_preflight",
            status="satisfied",
            complete=True,
            execution_allowed_now=ready,
        ),
        "remote_preflight_command_packetized": _status_report_remote_requirement_row(
            requirement_id="remote_preflight_command_packetized",
            phase="remote_preflight",
            status="satisfied",
            complete=True,
            execution_allowed_now=ready,
            blocked_by=[] if ready else ["requires_dr_sun_approval"],
        ),
    }
    return _status_report_remote_requirement_summary(
        requirements=requirements,
        status_counts={"satisfied": 4} if ready else {"blocked_missing_preflight": 2, "satisfied": 2},
    )


def _status_report_post_run_acceptance_requirement_summary_payload(*, ready):
    status = "satisfied" if ready else "blocked_until_remote_audit"
    requirements = {
        "pullback_expected_artifacts_complete": _status_report_remote_requirement_row(
            requirement_id="pullback_expected_artifacts_complete",
            phase="pullback",
            status=status,
            complete=ready,
            execution_allowed_now=False,
            remote_training_ready_now=ready,
        ),
        "checkpoint_hash_manifest_recorded": _status_report_remote_requirement_row(
            requirement_id="checkpoint_hash_manifest_recorded",
            phase="pullback",
            status=status,
            complete=ready,
            execution_allowed_now=False,
            remote_training_ready_now=ready,
        ),
        "gate3_formal_audit_accepts_remote_run": _status_report_remote_requirement_row(
            requirement_id="gate3_formal_audit_accepts_remote_run",
            phase="acceptance",
            status=status,
            complete=ready,
            execution_allowed_now=False,
            remote_training_ready_now=ready,
        ),
        "h01_h02_regenerated_from_audited_checkpoint": _status_report_remote_requirement_row(
            requirement_id="h01_h02_regenerated_from_audited_checkpoint",
            phase="evaluation_acceptance",
            status=status,
            complete=ready,
            execution_allowed_now=False,
            remote_training_ready_now=ready,
        ),
    }
    return _status_report_remote_requirement_summary(
        requirements=requirements,
        status_counts={"satisfied": 4} if ready else {"blocked_until_remote_audit": 4},
    )


def _status_report_h02_acceptance_requirement_summary_payload(*, ready):
    requirements = {
        "h01_schema_and_h02_output_schema_match": _status_report_h02_acceptance_requirement_row(
            requirement_id="h01_schema_and_h02_output_schema_match",
            phase="schema_acceptance",
            status="satisfied",
            complete=True,
            paper_result_input_allowed_now=ready,
        ),
        "h02_formal_scope_and_scale_match_h01": _status_report_h02_acceptance_requirement_row(
            requirement_id="h02_formal_scope_and_scale_match_h01",
            phase="formal_scope",
            status="satisfied" if ready else "blocked_formal_acceptance",
            complete=ready,
            paper_result_input_allowed_now=ready,
        ),
        "gate3_audit_and_pullback_acceptance": _status_report_h02_acceptance_requirement_row(
            requirement_id="gate3_audit_and_pullback_acceptance",
            phase="remote_acceptance",
            status="satisfied" if ready else "blocked_formal_acceptance",
            complete=ready,
            paper_result_input_allowed_now=ready,
        ),
        "ppo_rows_and_checkpoint_hash_present": _status_report_h02_acceptance_requirement_row(
            requirement_id="ppo_rows_and_checkpoint_hash_present",
            phase="result_rows",
            status="satisfied" if ready else "blocked_formal_acceptance",
            complete=ready,
            paper_result_input_allowed_now=ready,
        ),
    }
    return {
        "present": True,
        "required_requirement_count": len(requirements),
        "present_requirement_count": len(requirements),
        "blocked_requirement_count": sum(1 for row in requirements.values() if row["status"] != "satisfied"),
        "status_counts": {"satisfied": 4} if ready else {"satisfied": 1, "blocked_formal_acceptance": 3},
        "missing_requirement_ids": [],
        "requirements": requirements,
    }


def _status_report_h02_acceptance_requirement_row(
    *,
    requirement_id,
    phase,
    status,
    complete,
    paper_result_input_allowed_now,
):
    return {
        "requirement_id": requirement_id,
        "present": True,
        "status": status,
        "phase": phase,
        "complete": complete,
        "paper_result_input_allowed_now": paper_result_input_allowed_now,
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "acceptable_evidence_count": 1,
        "invalid_substitute_count": 1,
    }


def _status_report_remaining_deliverables_acceptance_summary_payload(*, ready):
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
            "missing": not ready,
            "responsible_stage_id": "gate3_remote_training"
            if category == "training"
            else "regenerate_h01_h02_formal_artifacts"
            if category == "formal_acceptance"
            else "gate3_remote_audit_pullback",
            "responsible_stage_allowed_now": ready,
            "acceptance_predicate_count": 1,
            "proof_command_count": 2,
            "proof_command_ids": [f"{artifact_id}_exists", f"{artifact_id}_schema"],
            "invalid_substitute_count": 1,
        }
    return {
        "present": True,
        "status": "formal_gate_deliverables_ready_for_claim_audit" if ready else "formal_gate_deliverables_blocked",
        "missing_deliverable_count": 0 if ready else len(matrix_ids),
        "matrix_row_count": len(matrix_ids),
        "expected_matrix_row_count": len(matrix_ids),
        "missing_row_count": 0 if ready else len(matrix_ids),
        "blocked_category_count": 0 if ready else 4,
        "missing_expected_matrix_ids": [],
        "rows": rows,
    }


def _status_report_remaining_deliverables_gap_summary_payload(*, ready):
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
            "missing_count": 0 if ready else len(matrix_ids),
            "responsible_stage_id": "gate3_remote_training"
            if category == "training"
            else "regenerate_h01_h02_formal_artifacts"
            if category == "formal_acceptance"
            else "gate3_remote_audit_pullback",
            "responsible_stage_allowed_now": ready,
            "missing_artifact_matrix_ids": [] if ready else matrix_ids,
            "proof_command_ids": []
            if ready
            else [
                command_id
                for matrix_id in matrix_ids
                for command_id in (
                    f"{matrix_id.split(':', 1)[1]}_exists",
                    f"{matrix_id.split(':', 1)[1]}_schema",
                )
            ],
        }
    return {
        "present": True,
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "total_missing_deliverables": 0 if ready else sum(len(ids) for ids in category_artifacts.values()),
        "open_category_count": 0 if ready else len(category_artifacts),
        "category_order": list(category_artifacts),
        "categories": categories,
    }


def _status_report_remaining_deliverables_proof_command_plan_payload(*, ready):
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
            "proof_command_count": 2,
            "proof_command_ids": [f"{artifact_id}_exists", f"{artifact_id}_schema"],
        }
    return {
        "present": True,
        "plan_id": "module2_formal_gate_local_read_only_proof_commands",
        "execution_boundary": "local_read_only_after_formal_remote_pullback",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_matrix_rows": len(matrix_ids),
        "total_proof_command_count": sum(row["proof_command_count"] for row in rows.values()),
        "rows": rows,
    }


def _status_report_remote_requirement_summary(*, requirements, status_counts):
    return {
        "present": True,
        "required_requirement_count": len(requirements),
        "present_requirement_count": len(requirements),
        "blocked_requirement_count": sum(1 for row in requirements.values() if row["status"] != "satisfied"),
        "status_counts": status_counts,
        "missing_requirement_ids": [],
        "requirements": requirements,
    }


def _status_report_remote_requirement_row(
    *,
    requirement_id,
    phase,
    status,
    complete,
    execution_allowed_now,
    blocked_by=None,
    remote_training_ready_now=None,
):
    return {
        "requirement_id": requirement_id,
        "present": True,
        "status": status,
        "phase": phase,
        "complete": complete,
        "execution_allowed_now": execution_allowed_now,
        "remote_training_ready_now": remote_training_ready_now,
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "blocked_by": [] if blocked_by is None else blocked_by,
        "acceptable_evidence_count": 1,
        "invalid_substitute_count": 1,
    }


def _status_report_requirement_stage_summary_payload(*, ready):
    requirements = {
        "training_remote_ppo_checkpoint": _status_report_requirement_stage_row(
            requirement_id="training_remote_ppo_checkpoint",
            expected_stage_id="gate3_remote_training",
            ready=ready,
        ),
        "evaluation_gate3_episode_outputs": _status_report_requirement_stage_row(
            requirement_id="evaluation_gate3_episode_outputs",
            expected_stage_id="gate3_remote_audit_pullback",
            ready=ready,
        ),
        "acceptance_remote_pullback_and_audit": _status_report_requirement_stage_row(
            requirement_id="acceptance_remote_pullback_and_audit",
            expected_stage_id="gate3_remote_audit_pullback",
            ready=ready,
        ),
        "h01_h02_formal_evaluation_acceptance": _status_report_requirement_stage_row(
            requirement_id="h01_h02_formal_evaluation_acceptance",
            expected_stage_id="regenerate_h01_h02_formal_artifacts",
            ready=ready,
        ),
    }
    return {
        "present_requirement_count": len(requirements),
        "mapped_requirement_count": len(requirements),
        "unmapped_requirement_count": 0,
        "mismatched_requirement_count": 0,
        "blocked_stage_count": 0 if ready else len(requirements),
        "unmapped_requirement_ids": [],
        "mismatched_requirement_ids": [],
        "requirements": requirements,
    }


def _status_report_requirement_stage_row(*, requirement_id, expected_stage_id, ready):
    return {
        "requirement_id": requirement_id,
        "present": True,
        "status": "satisfied" if ready else "blocked_missing_outputs",
        "expected_stage_id": expected_stage_id,
        "responsible_stage_id": expected_stage_id,
        "responsible_stage_status": "ready" if ready else "blocked",
        "responsible_stage_allowed_now": bool(ready),
        "responsible_stage_blocked_by": [] if ready else ["remote_packet_not_ready"],
        "mapping_present": True,
        "mapping_matches_expected": True,
    }
