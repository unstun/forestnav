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
    assert manifest["next_handoff_action"]["action_id"] == "record_f02_6_decision"
    assert manifest["next_handoff_action"]["requires_dr_sun"] is True
    assert manifest["next_handoff_action"]["allowed_for_agent_now"] is False
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
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 4
    assert manifest["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] == 3
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
    assert manifest["remote_execution_steps"]["run_remote_training"]["allowed_now"] is True
    assert "ssh gpu3070ti-relay" in manifest["remote_execution_steps"]["run_remote_training"]["command"]
    assert manifest["safety_issue_count"] == 0

    stages = {stage["stage_id"]: stage for stage in manifest["handoff_stages"]}
    assert stages["gate3_remote_training"]["source_allowed_now"] is True
    assert stages["gate3_remote_training"]["runs_training"] is True
    assert stages["gate3_remote_training"]["host"] == "gpu3070ti-relay"


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
    assert "transition_gate_approved_allows_remote_training" in issue_ids
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
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "blocked_until_f02_6_decision"
    assert "Module2 Formal Gate Handoff Bundle" in markdown
    assert "Remote Steps" in markdown
    assert "Handoff Stages" in markdown
    assert "F02.6 Route Handoff" in markdown
    assert "source_freshness_status" in markdown
    assert "remaining deliverables gap" in markdown
    assert "responsible_stage=`gate3_remote_training`" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    return builder.FormalGateHandoffBundleConfig(
        output_dir=tmp_path,
        decision_record_path=_json(tmp_path, "decision.json", _decision(complete=complete)),
        transition_gate_audit_path=_json(tmp_path, "transition_gate.json", _transition_gate()),
        post_plan_path=_json(tmp_path, "post_plan.json", _post_plan(complete=complete)),
        status_report_path=_json(tmp_path, "status_report.json", _status_report(complete=complete)),
        remote_packet_path=_json(tmp_path, "remote_packet.json", _remote_packet(complete=complete)),
        missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts(complete=complete)),
        h02_acceptance_path=_json(tmp_path, "h02.json", _h02(complete=complete)),
        source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness(complete=complete)),
    )


def _decision(*, complete):
    return {
        "status": "approved" if complete else "pending_human_decision",
        "decider": "Dr Sun" if complete else None,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
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
