import json
from importlib import import_module


def test_proof_summary_chain_audit_accepts_consistent_blocked_chain(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing proof summary chain audit builder: {exc}") from exc

    paths = _write_chain_inputs(tmp_path)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_proof_summary_chain_audit"
    assert manifest["status"] == "formal_gate_proof_summary_chain_consistent_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["proof_open"] is True
    assert manifest["row_count"] == 14
    assert manifest["consistent_row_count"] == 14
    assert manifest["missing_row_count"] == 0
    assert manifest["mismatch_row_count"] == 0
    assert manifest["audit_issue_count"] == 0
    assert manifest["h02_paper_result_input_allowed"] is False
    assert manifest["baseline_summary"]["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert manifest["baseline_summary"]["next_blocked_lane"] == "decision"
    assert manifest["chain_rows_by_id"]["paper_readiness_remote_safety_proof_summary"][
        "signature_matches_baseline"
    ] is True


def test_proof_summary_chain_audit_fails_missing_downstream_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    paper = json.loads(paths["paper"].read_text(encoding="utf-8"))
    paper.pop("claim_safety_remote_packet_safety_proof_deliverables_summary")
    paths["paper"].write_text(json.dumps(paper), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    assert manifest["missing_row_count"] == 1
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "paper_readiness_remote_safety_proof_summary_missing_summary" in issue_ids


def test_proof_summary_chain_audit_fails_mismatched_summary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    claim = json.loads(paths["claim"].read_text(encoding="utf-8"))
    claim["status_report_remote_packet_safety_proof_deliverables_summary"][
        "missing_counts_by_formal_category"
    ]["training"] = 2
    paths["claim"].write_text(json.dumps(claim), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    assert manifest["mismatch_row_count"] == 1
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "claim_safety_remote_safety_proof_summary_summary_mismatch" in issue_ids


def test_proof_summary_chain_audit_fails_h02_paper_input_allowed_while_open(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    status_report = json.loads(paths["status_report"].read_text(encoding="utf-8"))
    status_report["formal_gate_proof_audit_remaining_deliverables_top_level_summary"][
        "h02_paper_result_input_allowed"
    ] = True
    paths["status_report"].write_text(json.dumps(status_report), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "formal_gate_status_report_proof_summary_summary_mismatch" in issue_ids
    assert "formal_gate_status_report_proof_summary_allows_h02_paper_input_while_proof_open" in issue_ids


def test_proof_summary_chain_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
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
            "--remaining-deliverables",
            str(paths["remaining"]),
            "--formal-gate-proof-audit",
            str(paths["proof"]),
            "--formal-gate-status-report",
            str(paths["status_report"]),
            "--post-f02-6-plan-audit",
            str(paths["post_plan"]),
            "--remote-packet-safety-audit",
            str(paths["remote_safety"]),
            "--formal-gate-gap-audit",
            str(paths["gap"]),
            "--claim-safety",
            str(paths["claim"]),
            "--paper-readiness",
            str(paths["paper"]),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_proof_summary_chain_consistent_blocked"
    assert "Module2 Formal Gate Proof Summary Chain Audit" in markdown
    assert "not a training run" in markdown
    assert "paper_readiness_remote_safety_proof_summary" in markdown
    assert "h02_paper_result_input_allowed" in markdown


def _config(builder, tmp_path, paths):
    return builder.FormalGateProofSummaryChainAuditConfig(
        output_dir=tmp_path,
        remaining_deliverables_path=paths["remaining"],
        formal_gate_proof_audit_path=paths["proof"],
        formal_gate_status_report_path=paths["status_report"],
        post_f02_6_plan_audit_path=paths["post_plan"],
        remote_packet_safety_audit_path=paths["remote_safety"],
        formal_gate_gap_audit_path=paths["gap"],
        claim_safety_path=paths["claim"],
        paper_readiness_path=paths["paper"],
    )


def _write_chain_inputs(tmp_path):
    summary = _summary()
    paths = {
        "remaining": tmp_path / "remaining.json",
        "proof": tmp_path / "proof.json",
        "status_report": tmp_path / "status_report.json",
        "post_plan": tmp_path / "post_plan.json",
        "remote_safety": tmp_path / "remote_safety.json",
        "gap": tmp_path / "gap.json",
        "claim": tmp_path / "claim.json",
        "paper": tmp_path / "paper.json",
    }
    _write_json(
        paths["remaining"],
        {
            "missing_counts_by_formal_category": summary["missing_counts_by_formal_category"],
            "missing_matrix_ids_by_formal_category": summary["missing_matrix_ids_by_formal_category"],
            "next_blocked_lane": summary["next_blocked_lane"],
            "h01_status": summary["h01_status"],
            "h02_status": summary["h02_status"],
            "h02_formal_output_accepted": summary["h02_formal_output_accepted"],
            "h02_paper_result_input_allowed": summary["h02_paper_result_input_allowed"],
        },
    )
    _write_json(paths["proof"], {"remaining_deliverables_top_level_summary": summary})
    _write_json(
        paths["status_report"],
        {
            "formal_gate_proof_audit_remaining_deliverables_top_level_summary": summary,
            "remote_packet_safety_proof_deliverables_summary": summary,
            "remote_packet_safety_status_report_proof_deliverables_summary": summary,
        },
    )
    _write_json(paths["post_plan"], {"status_report_proof_audit_deliverables_summary": summary})
    _write_json(
        paths["remote_safety"],
        {
            "cross_gate_summary": {
                "post_plan_proof_audit_deliverables_summary": summary,
                "post_plan_status_report_proof_audit_deliverables_summary": summary,
            }
        },
    )
    _write_json(
        paths["gap"],
        {
            "remote_packet_safety": {
                "proof_deliverables_summary": summary,
                "status_report_proof_deliverables_summary": summary,
            }
        },
    )
    _write_json(
        paths["claim"],
        {
            "status_report_remote_packet_safety_proof_deliverables_summary": summary,
            "status_report_remote_packet_safety_status_report_proof_deliverables_summary": summary,
        },
    )
    _write_json(
        paths["paper"],
        {
            "claim_safety_remote_packet_safety_proof_deliverables_summary": summary,
            "claim_safety_remote_packet_safety_status_report_proof_deliverables_summary": summary,
        },
    )
    return paths


def _summary():
    return {
        "present": True,
        "missing_counts_by_formal_category": {
            "training": 3,
            "evaluation": 2,
            "acceptance": 3,
            "formal_acceptance": 2,
        },
        "missing_matrix_ids_by_formal_category": {
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
        },
        "next_blocked_lane": "decision",
        "h01_status": "blocked_pending_decisions",
        "h02_status": "blocked_formal_output_acceptance",
        "h02_formal_output_accepted": False,
        "h02_paper_result_input_allowed": False,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
