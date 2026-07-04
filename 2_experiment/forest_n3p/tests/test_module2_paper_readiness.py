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
    assert manifest["input_status"]["claim_safety_decision_intake_next_blocked_lane"] == "decision"
    assert manifest["input_status"]["claim_safety_decision_intake_remote_preflight_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_remote_training_allowed_now"] is False
    assert manifest["input_status"]["claim_safety_decision_intake_formal_claim_allowed_now"] is False
    assert manifest["claim_safety_decision_intake_summary"]["status"] == "f02_6_decision_intake_pending_clean"
    assert "claim_safety_f02_6_decision_intake_pending" in manifest["global_blockers"]
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_present"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_matrix_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_missing_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_blocked_category_count"] == 4
    assert manifest["input_status"]["claim_safety_remaining_deliverables_gap_present"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_gap_total_missing_deliverables"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_gap_open_category_count"] == 4
    assert "claim_safety_remaining_deliverables_acceptance_rows_missing" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_acceptance_categories_blocked" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_gap_rows_missing" in manifest["global_blockers"]
    assert "claim_safety_remaining_deliverables_gap_categories_blocked" in manifest["global_blockers"]
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
    assert "Claim Safety Remaining Deliverables Acceptance Matrix" in markdown
    assert "claim_safety_remaining_deliverables_acceptance_matrix_row_count" in markdown


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
    assert manifest["input_status"]["claim_safety_decision_intake_remote_training_allowed_now"] is True
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_matrix_row_count"] == 10
    assert manifest["input_status"]["claim_safety_remaining_deliverables_acceptance_missing_row_count"] == 0
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
    assert manifest["input_status"]["claim_safety_decision_intake_status"] == "f02_6_decision_intake_failed"


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


def _write_inputs(tmp_path, *, formal):
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
                "remote_preflight_allowed_now": formal,
                "remote_training_allowed_now": formal,
                "formal_claim_allowed_now": formal,
            },
            "status_report_remaining_deliverables_acceptance_summary": _claim_safety_remaining_deliverables_acceptance_summary_payload(
                formal=formal
            ),
            "status_report_remaining_deliverables_gap_summary": _claim_safety_remaining_deliverables_gap_summary_payload(
                formal=formal
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
