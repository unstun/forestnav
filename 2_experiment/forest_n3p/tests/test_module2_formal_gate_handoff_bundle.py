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
    assert manifest["current_state"]["next_blocked_lane"] == "decision"
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["remote_execution_steps"]["sync_to_remote"]["allowed_now"] is False
    assert manifest["remote_execution_steps"]["run_remote_training"]["allowed_now"] is False
    assert "requires_dr_sun_approval" in manifest["remote_execution_steps"]["run_remote_training"]["blocked_by"]
    assert len(manifest["formal_gate_requirements"]) == 4
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
    assert manifest["remote_execution_steps"]["run_remote_training"]["allowed_now"] is True
    assert "ssh gpu3070ti-relay" in manifest["remote_execution_steps"]["run_remote_training"]["command"]
    assert manifest["safety_issue_count"] == 0

    stages = {stage["stage_id"]: stage for stage in manifest["handoff_stages"]}
    assert stages["gate3_remote_training"]["source_allowed_now"] is True
    assert stages["gate3_remote_training"]["runs_training"] is True
    assert stages["gate3_remote_training"]["host"] == "gpu3070ti-relay"


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
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "blocked_until_f02_6_decision"
    assert "Module2 Formal Gate Handoff Bundle" in markdown
    assert "Remote Steps" in markdown
    assert "Handoff Stages" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_handoff_bundle")
    return builder.FormalGateHandoffBundleConfig(
        output_dir=tmp_path,
        decision_record_path=_json(tmp_path, "decision.json", _decision(complete=complete)),
        post_plan_path=_json(tmp_path, "post_plan.json", _post_plan(complete=complete)),
        status_report_path=_json(tmp_path, "status_report.json", _status_report(complete=complete)),
        remote_packet_path=_json(tmp_path, "remote_packet.json", _remote_packet(complete=complete)),
        missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts(complete=complete)),
        h02_acceptance_path=_json(tmp_path, "h02.json", _h02(complete=complete)),
    )


def _decision(*, complete):
    return {
        "status": "approved" if complete else "pending_human_decision",
        "decider": "Dr Sun" if complete else None,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
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
        },
        "next_blocked_lane": None if complete else {"lane_id": "decision"},
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
            _requirement("training_remote_ppo_checkpoint", "training", complete=complete),
            _requirement("evaluation_gate3_episode_outputs", "evaluation", complete=complete),
            _requirement("acceptance_remote_pullback_and_audit", "acceptance", complete=complete),
            _requirement("h01_h02_formal_evaluation_acceptance", "evaluation_acceptance", complete=complete),
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


def _requirement(requirement_id, phase, *, complete):
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": "satisfied" if complete else "blocked_missing_outputs",
        "complete": complete,
        "execution_allowed_now": False,
        "missing_artifact_ids": [] if complete else [f"{requirement_id}_missing"],
        "acceptable_evidence": [f"{requirement_id}_evidence"],
        "invalid_substitutes": [f"{requirement_id}_invalid_substitute"],
    }


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
