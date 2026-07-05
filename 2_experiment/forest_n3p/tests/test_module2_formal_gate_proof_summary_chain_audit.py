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
    assert manifest["next_action_guard_row_count"] == 3
    assert manifest["next_action_guard_consistent_row_count"] == 3
    assert manifest["next_required_deliverables_row_count"] == 3
    assert manifest["next_required_deliverables_consistent_row_count"] == 3
    assert manifest["handoff_single_next_action_row_count"] == 3
    assert manifest["handoff_single_next_action_consistent_row_count"] == 3
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
    assert manifest["next_action_guard_rows_by_id"]["paper_readiness_claim_safety_next_action_guard"][
        "signature_matches_baseline"
    ] is True
    assert manifest["next_required_deliverables_rows_by_id"][
        "paper_readiness_claim_safety_next_required_formal_deliverables"
    ]["signature_matches_baseline"] is True
    assert manifest["handoff_single_next_action_rows_by_id"][
        "paper_readiness_claim_safety_handoff_single_next_action_index"
    ]["signature_matches_baseline"] is True


def test_proof_summary_chain_audit_accepts_explicit_source_freshness_blocker(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    handoff_summary = _handoff_single_next_action_summary()
    handoff_summary["source_freshness_status"] = "source_freshness_risks_recorded_gate_still_blocked"
    handoff_summary["source_freshness_blocking_regeneration_required"] = True
    paths = _write_chain_inputs(tmp_path, handoff_single_next_action=handoff_summary)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_consistent_blocked"
    assert manifest["audit_issue_count"] == 0
    assert manifest["handoff_single_next_action_consistent_row_count"] == 3
    assert manifest["handoff_single_next_action_baseline_signature"][
        "source_freshness_blocking_regeneration_required"
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


def test_proof_summary_chain_audit_fails_proof_audit_input_safety_open(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    proof = json.loads(paths["proof"].read_text(encoding="utf-8"))
    proof["input_safety_issue_count"] = 1
    proof["input_safety_issues"] = [
        {
            "issue_id": "acceptance_matrix_training_wrong_artifact_identity_mismatch",
            "observed": {"matrix_id": "training:wrong_artifact"},
        }
    ]
    proof["blockers"] = ["proof_audit_input_safety_issues_open"]
    paths["proof"].write_text(json.dumps(proof), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    assert manifest["proof_audit_input_safety_issue_count"] == 1
    assert manifest["proof_audit_blockers"] == ["proof_audit_input_safety_issues_open"]
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "formal_gate_proof_audit_input_safety_issues_open" in issue_ids
    assert "formal_gate_proof_audit_input_safety_blocker_open" in issue_ids


def test_proof_summary_chain_audit_fails_next_action_guard_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    paper = json.loads(paths["paper"].read_text(encoding="utf-8"))
    paper["claim_safety_next_action_guard_summary"]["expected_next_action_id"] = "run_remote_training"
    paper["claim_safety_next_action_guard_summary"]["execution_leak_count"] = 1
    paths["paper"].write_text(json.dumps(paper), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "paper_readiness_claim_safety_next_action_guard_summary_mismatch" in issue_ids
    assert "paper_readiness_claim_safety_next_action_guard_execution_leak" in issue_ids


def test_proof_summary_chain_audit_fails_next_required_deliverables_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    claim = json.loads(paths["claim"].read_text(encoding="utf-8"))
    deliverables = claim["status_report_next_required_formal_deliverables"]
    deliverables["not_paper_result_material"] = False
    deliverables["runs_training"] = True
    deliverables["rows"].pop("formal_acceptance:h02_formal_output_acceptance")
    paths["claim"].write_text(json.dumps(claim), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "claim_safety_status_report_next_required_formal_deliverables_summary_mismatch" in issue_ids
    assert "claim_safety_status_report_next_required_formal_deliverables_marked_as_paper_result" in issue_ids
    assert "claim_safety_status_report_next_required_formal_deliverables_runs_training" in issue_ids


def test_proof_summary_chain_audit_fails_handoff_single_next_action_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit")
    paths = _write_chain_inputs(tmp_path)
    paper = json.loads(paths["paper"].read_text(encoding="utf-8"))
    summary = paper["claim_safety_handoff_single_next_action_index_summary"]
    summary["next_action_id"] = "run_remote_training"
    summary["current_allowed_action_ids"] = ["run_remote_training"]
    summary["remote_training_allowed_now"] = True
    summary["all_execution_disabled_now"] = False
    paths["paper"].write_text(json.dumps(paper), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "formal_gate_proof_summary_chain_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "paper_readiness_claim_safety_handoff_single_next_action_index_summary_mismatch" in issue_ids
    assert "paper_readiness_claim_safety_handoff_single_next_action_index_unexpected_next_action" in issue_ids
    assert "paper_readiness_claim_safety_handoff_single_next_action_index_unexpected_allowed_actions" in issue_ids
    assert "paper_readiness_claim_safety_handoff_single_next_action_index_execution_not_disabled" in issue_ids
    assert "paper_readiness_claim_safety_handoff_single_next_action_index_remote_training_allowed_now" in issue_ids


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
            "--formal-gate-handoff-bundle",
            str(paths["handoff"]),
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
    assert "Next-Action Guard Chain Rows" in markdown
    assert "paper_readiness_claim_safety_next_action_guard" in markdown
    assert "Next Required Formal Deliverables Chain Rows" in markdown
    assert "paper_readiness_claim_safety_next_required_formal_deliverables" in markdown
    assert "Handoff Single Next-Action Chain Rows" in markdown
    assert "paper_readiness_claim_safety_handoff_single_next_action_index" in markdown


def _config(builder, tmp_path, paths):
    return builder.FormalGateProofSummaryChainAuditConfig(
        output_dir=tmp_path,
        remaining_deliverables_path=paths["remaining"],
        formal_gate_proof_audit_path=paths["proof"],
        formal_gate_status_report_path=paths["status_report"],
        post_f02_6_plan_audit_path=paths["post_plan"],
        remote_packet_safety_audit_path=paths["remote_safety"],
        formal_gate_gap_audit_path=paths["gap"],
        formal_gate_handoff_bundle_path=paths["handoff"],
        claim_safety_path=paths["claim"],
        paper_readiness_path=paths["paper"],
    )


def _write_chain_inputs(tmp_path):
    summary = _summary()
    next_action_guard = _next_action_guard_summary()
    next_required_deliverables = _next_required_deliverables_summary()
    handoff_single_next_action = _handoff_single_next_action_summary()
    paths = {
        "remaining": tmp_path / "remaining.json",
        "proof": tmp_path / "proof.json",
        "status_report": tmp_path / "status_report.json",
        "post_plan": tmp_path / "post_plan.json",
        "remote_safety": tmp_path / "remote_safety.json",
        "gap": tmp_path / "gap.json",
        "handoff": tmp_path / "handoff.json",
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
            "next_action_guard_summary": next_action_guard,
            "next_required_formal_deliverables": _next_required_deliverables_summary(as_list=True),
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
    _write_json(paths["handoff"], {"single_next_action_index": handoff_single_next_action})
    _write_json(
        paths["claim"],
        {
            "status_report_remote_packet_safety_proof_deliverables_summary": summary,
            "status_report_remote_packet_safety_status_report_proof_deliverables_summary": summary,
            "status_report_next_action_guard_summary": next_action_guard,
            "status_report_next_required_formal_deliverables": next_required_deliverables,
            "handoff_single_next_action_index_summary": handoff_single_next_action,
        },
    )
    _write_json(
        paths["paper"],
        {
            "claim_safety_remote_packet_safety_proof_deliverables_summary": summary,
            "claim_safety_remote_packet_safety_status_report_proof_deliverables_summary": summary,
            "claim_safety_next_action_guard_summary": next_action_guard,
            "claim_safety_next_required_formal_deliverables": next_required_deliverables,
            "claim_safety_handoff_single_next_action_index_summary": handoff_single_next_action,
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


def _next_action_guard_summary():
    return {
        "present": True,
        "status": "next_action_guard_passed",
        "pending_f02_6_decision": True,
        "next_blocked_lane_id": "decision",
        "expected_next_action_id": "record_f02_6_decision",
        "handoff_next_action_id": "record_f02_6_decision",
        "handoff_next_action_requires_dr_sun": True,
        "missing_artifacts_next_action_id": "record_f02_6_decision",
        "decision_intake_next_blocked_lane": "decision",
        "all_execution_disabled_now": True,
        "execution_leak_count": 0,
        "remote_execution_allowed_count": 0,
        "remote_stage_allowed_count": 0,
        "violation_count": 0,
        "execution_leak_surface_ids": [],
    }


def _handoff_single_next_action_summary():
    return {
        "present": True,
        "index_id": "module2_formal_gate_single_next_action_index",
        "status": "awaiting_dr_sun_f02_6_decision",
        "single_current_human_entry": True,
        "next_action_id": "record_f02_6_decision",
        "decision_owner_required": "Dr Sun",
        "valid_decisions": [
            "approve_obstacle_summary_warm_start",
            "reject_obstacle_summary_warm_start",
        ],
        "required_record_fields": ["decision", "decider", "decision_note"],
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
        "record_command_template_count": 2,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "missing_deliverable_count": 10,
        "open_category_count": 4,
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


def _next_required_deliverables_summary(*, as_list=False):
    rows = {}
    categories = {
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
    for category, matrix_ids in categories.items():
        for matrix_id in matrix_ids:
            artifact_id = matrix_id.split(":", 1)[1]
            rows[matrix_id] = {
                "present": True,
                "matrix_id": matrix_id,
                "category": category,
                "artifact_id": artifact_id,
                "current_state": "missing",
                "responsible_stage_id": "gate3_remote_training"
                if category == "training"
                else "regenerate_h01_h02_formal_artifacts"
                if category == "formal_acceptance"
                else "gate3_remote_audit_pullback",
                "responsible_stage_allowed_now": False,
                "proof_command_ids": [f"{artifact_id}_exists", f"{artifact_id}_schema"],
                "invalid_substitute_count": 1,
            }
    return {
        "present": True,
        "status": "blocked_missing_formal_deliverables",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_missing_deliverables": 10,
        "blocked_category_count": 4,
        "blocked_categories": list(categories),
        "category_order": list(categories),
        "rows": list(rows.values()) if as_list else rows,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
