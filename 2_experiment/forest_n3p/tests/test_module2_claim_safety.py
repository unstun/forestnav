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
    assert manifest["formal_performance_blockers"] == ["formal_gate_status_report_blocked"]
    assert manifest["input_status"]["status_report_status"] == "formal_gate_status_blocked"
    assert manifest["input_status"]["status_report_next_blocked_lane_id"] == "decision"
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
