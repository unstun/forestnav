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
    assert manifest["current_state"]["decision_status"] == "pending_human_decision"
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
    assert manifest["current_state"]["formal_gate_execution_veto_present"] is True
    assert manifest["current_state"]["formal_gate_execution_veto_all_rows_consistent"] is True
    assert manifest["current_state"]["formal_gate_execution_veto_remote_training_allowed_now"] is False
    assert manifest["current_state"]["formal_gate_execution_veto_formal_claim_allowed_now"] is False
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
    veto = manifest["formal_gate_execution_veto_summary"]
    assert veto["present"] is True
    assert veto["all_rows_consistent"] is True
    assert veto["row_consensus"]["remote_training"] is False
    assert veto["row_consensus"]["formal_claim"] is False

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


def test_formal_gate_status_report_catches_status_input_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")

    manifest = builder.build_manifest(_config(tmp_path, complete=False, drift=True))

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_status_blocked"
    assert "closure_checklist_executes_commands" in issue_ids
    assert "remote_packet_allows_claim_before_audit" in issue_ids
    assert "claim_safety_allows_formal_claim" in issue_ids
    assert "handoff_bundle_safety_issues_open" in issue_ids
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is False


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
    assert "Formal Gate Execution Veto Matrix" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete, drift=False):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_status_report")
    return builder.FormalGateStatusReportConfig(
        output_dir=tmp_path,
        formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate(complete=complete)),
        missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts(complete=complete)),
        closure_checklist_path=_json(tmp_path, "closure_checklist.json", _closure_checklist(complete=complete, drift=drift)),
        decision_record_path=_json(tmp_path, "decision_record.json", _decision_record(complete=complete)),
        remote_packet_path=_json(tmp_path, "remote_packet.json", _remote_packet(complete=complete, drift=drift)),
        h01_manifest_path=_json(tmp_path, "h01_manifest.json", _h01_manifest(complete=complete)),
        h02_acceptance_path=_json(tmp_path, "h02_acceptance.json", _h02_acceptance(complete=complete)),
        claim_safety_path=_json(tmp_path, "claim_safety.json", _claim_safety(complete=complete, drift=drift)),
        paper_readiness_path=_json(tmp_path, "paper_readiness.json", _paper_readiness(complete=complete)),
        handoff_bundle_path=_json(tmp_path, "handoff_bundle.json", _handoff_bundle(complete=complete, drift=drift)),
    )


def _formal_gate(*, complete):
    return {
        "status": "formal_gate_ready_for_result_audit" if complete else "blocked_formal_gate_gaps_open",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "execution_veto_matrix": _execution_veto_matrix(complete=complete),
        "ordered_next_steps": [
            {"step_id": "F02.6", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["f02_6_decision_not_approved"]},
            {"step_id": "remote_preflight", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["source_freshness_regeneration_required"]},
            {"step_id": "gate3_remote_training", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["remote_training_packet_not_ready"]},
            {"step_id": "gate3_remote_audit_pullback", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["missing_remote_pullback_artifact"]},
            {"step_id": "h01_h02_regeneration", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["h01_manifest_not_ready"]},
            {"step_id": "claim_safety_final_gate", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["h02_formal_acceptance_not_ready"]},
        ],
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


def _missing_artifacts(*, complete):
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
        "missing_counts_by_category": counts,
        "missing_evidence_groups": groups,
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
        "local_training_allowed": False,
        "formal_claim_allowed": False,
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
    }
    if drift:
        payload["formal_claim_allowed_before_audit"] = True
    return payload


def _h01_manifest(*, complete):
    return {
        "status": "ready_for_formal_run" if complete else "blocked_pending_decisions",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _h02_acceptance(*, complete):
    return {
        "status": "formal_output_accepted" if complete else "blocked_formal_output_acceptance",
        "formal_output_accepted": complete,
        "paper_result_input_allowed": complete,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
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
