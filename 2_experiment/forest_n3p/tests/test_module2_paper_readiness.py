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


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
