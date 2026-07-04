import json
from importlib import import_module
from pathlib import Path


def test_missing_artifacts_audit_blocks_pending_formal_chain(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate missing-artifacts auditor: {exc}") from exc

    manifest = builder.build_manifest(_config(tmp_path, complete=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_missing_artifacts_audit"
    assert manifest["status"] == "formal_gate_missing_artifacts_open"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["all_required_evidence_present"] is False
    assert manifest["current_gate_summary"]["f02_6_decision_record_status"] == "pending_human_decision"
    assert manifest["current_gate_summary"]["f02_6_transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["current_gate_summary"]["f02_6_transition_gate_audit_issue_count"] == 0
    assert manifest["current_gate_summary"]["ready_to_run_remote_training"] is False
    assert manifest["missing_counts_by_category"]["training"] == 3
    assert manifest["missing_counts_by_category"]["evaluation"] == 2
    assert manifest["missing_counts_by_category"]["acceptance"] == 3
    assert manifest["formal_gate_requirement_counts"] == {"blocked_missing_outputs": 4}

    handoff = manifest["formal_gate_handoff_index"]
    assert handoff["status"] == "blocked_until_f02_6_decision"
    assert handoff["next_action"]["action_id"] == "record_f02_6_decision"
    assert handoff["next_action"]["requires_dr_sun"] is True
    assert handoff["next_action"]["allowed_for_agent_now"] is False
    assert handoff["local_training_allowed_now"] is False
    assert handoff["remote_training_allowed_now"] is False
    assert handoff["formal_result_material_allowed_now"] is False
    assert handoff["open_requirement_count"] == 5
    assert handoff["authority_artifacts"]["remote_formal_execution_packet"].endswith("remote_packet.json")
    handoff_requirements = {item["requirement_id"]: item for item in handoff["requirements"]}
    assert handoff_requirements["f02_6_human_decision"]["missing_artifact_count"] == 1
    assert handoff_requirements["f02_6_human_decision"]["source_artifacts"] == [
        str(config.decision_record_path),
        str(config.transition_gate_audit_path),
    ]
    assert handoff_requirements["training_remote_ppo_checkpoint"]["missing_artifact_count"] == 3
    assert str(config.remote_packet_path) in handoff_requirements["training_remote_ppo_checkpoint"]["source_artifacts"]
    assert str(config.h02_acceptance_path) in handoff_requirements["acceptance_remote_pullback_and_audit"]["downstream_consumers"]

    requirements = {item["requirement_id"]: item for item in manifest["formal_gate_requirements"]}
    assert requirements["training_remote_ppo_checkpoint"]["phase"] == "training"
    assert requirements["training_remote_ppo_checkpoint"]["status"] == "blocked_missing_outputs"
    assert requirements["training_remote_ppo_checkpoint"]["execution_allowed_now"] is False
    assert requirements["training_remote_ppo_checkpoint"]["missing_artifact_ids"] == [
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ]
    assert "local training output" in requirements["training_remote_ppo_checkpoint"]["invalid_substitutes"]
    assert requirements["evaluation_gate3_episode_outputs"]["missing_artifact_ids"] == [
        "eval_gate3_eval_episodes_csv",
        "eval_gate3_summary_json",
    ]
    assert "H02 available-subset smoke CSV" in requirements["evaluation_gate3_episode_outputs"]["invalid_substitutes"]
    assert requirements["acceptance_remote_pullback_and_audit"]["missing_artifact_ids"] == [
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
    ]
    assert "checkpoint file without hash record" in requirements["acceptance_remote_pullback_and_audit"]["invalid_substitutes"]

    groups = {group["group_id"]: group for group in manifest["missing_evidence_groups"]}
    assert groups["f02_6_decision_record"]["complete"] is False
    assert "f02_6_decision_not_approved" in groups["f02_6_decision_record"]["blocked_by"]
    assert groups["f02_6_transition_gate_audit"]["complete"] is True
    assert groups["remote_training_outputs"]["blocked_by"] == [
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ]
    assert groups["h01_h02_formal_evaluation_acceptance"]["complete"] is False


def test_missing_artifacts_audit_accepts_synthetic_complete_formal_chain(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit")
    config = _config(tmp_path, complete=True)

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "formal_gate_artifacts_complete"
    assert manifest["all_required_evidence_present"] is True
    assert manifest["audit_issue_count"] == 0
    assert all(count == 0 for count in manifest["missing_counts_by_category"].values())
    assert manifest["formal_gate_requirement_counts"] == {"satisfied": 4}
    assert all(item["status"] == "satisfied" for item in manifest["formal_gate_requirements"])
    assert manifest["formal_gate_handoff_index"]["status"] == "formal_gate_evidence_ready_for_h01_h02_claim_gates"
    assert manifest["formal_gate_handoff_index"]["open_requirement_count"] == 0
    assert manifest["formal_gate_handoff_index"]["next_action"]["action_id"] == "no_open_formal_gate_handoff_requirements"
    assert manifest["current_gate_summary"]["f02_6_transition_gate_status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["current_gate_summary"]["h01_manifest_status"] == "ready_for_formal_run"
    assert manifest["current_gate_summary"]["h02_acceptance_status"] == "formal_output_accepted"


def test_missing_artifacts_audit_catches_dangerous_gate_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit")
    config = _config(tmp_path, complete=False, drift=True)

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_missing_artifacts_open"
    assert "decision_allows_local_training" in issue_ids
    assert "transition_gate_runs_training" in issue_ids
    assert "transition_gate_audit_not_passed" in issue_ids
    assert "transition_gate_audit_issues_open" in issue_ids
    assert "remote_packet_allows_formal_claim" in issue_ids
    assert "pending_decision_remote_packet_ready" in issue_ids
    assert "h02_accepts_missing_pullback_artifacts" in issue_ids


def test_missing_artifacts_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit")
    config = _config(tmp_path, complete=False)
    manifest_path = tmp_path / "formal_gate_missing_artifacts.json"
    markdown_path = tmp_path / "formal_gate_missing_artifacts.md"

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
            "--decision-gate-audit",
            str(config.decision_gate_audit_path),
            "--transition-gate-audit",
            str(config.transition_gate_audit_path),
            "--post-plan",
            str(config.post_plan_path),
            "--source-freshness-audit",
            str(config.source_freshness_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--remote-packet-audit",
            str(config.remote_packet_audit_path),
            "--h01-manifest",
            str(config.h01_manifest_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_missing_artifacts_open"
    assert "Module2 Formal Gate Missing Artifacts Audit" in markdown
    assert "Formal Gate Handoff Index" in markdown
    assert "record_f02_6_decision" in markdown
    assert "Authority Artifacts" in markdown
    assert "Formal Gate Requirements" in markdown
    assert "f02_6_transition_gate_status" in markdown
    assert "training_remote_ppo_checkpoint" in markdown
    assert "invalid_substitutes" in markdown
    assert "remote_training_outputs" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete, drift=False):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit")
    trial_dir = tmp_path / "gate3_obstacle_summary_warm_approved_v1"
    artifacts = _artifact_paths(trial_dir)
    if complete:
        for path in artifacts:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("artifact\n", encoding="utf-8")
        Path(f"{artifacts[0]}.sha256").write_text("abc123  final_model.zip\n", encoding="utf-8")

    return builder.FormalGateMissingArtifactsAuditConfig(
        output_dir=tmp_path,
        decision_record_path=_json(tmp_path, "decision_record.json", _decision_record(complete=complete, drift=drift)),
        decision_gate_audit_path=_json(tmp_path, "decision_gate_audit.json", _decision_gate(complete=complete)),
        transition_gate_audit_path=_json(tmp_path, "transition_gate_audit.json", _transition_gate(drift=drift)),
        post_plan_path=_json(tmp_path, "post_plan.json", _post_plan(complete=complete)),
        source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness(complete=complete)),
        remote_packet_path=_json(tmp_path, "remote_packet.json", _remote_packet(artifacts=artifacts, complete=complete, drift=drift)),
        remote_packet_audit_path=_json(tmp_path, "remote_packet_audit.json", _remote_packet_audit()),
        h01_manifest_path=_json(tmp_path, "h01_manifest.json", _h01_manifest(complete=complete)),
        h02_acceptance_path=_json(tmp_path, "h02_acceptance.json", _h02_acceptance(complete=complete, drift=drift)),
    )


def _artifact_paths(trial_dir):
    return [
        trial_dir / "train/final_model.zip",
        trial_dir / "train/summary.json",
        trial_dir / "train/training_manifest.json",
        trial_dir / "eval/gate3_eval_episodes.csv",
        trial_dir / "eval/gate3_summary.json",
        trial_dir / "gate3_trial_manifest.json",
        trial_dir / "gate3_formal_audit.json",
    ]


def _decision_record(*, complete, drift=False):
    payload = {
        "status": "approved" if complete else "pending_human_decision",
        "decider": "Dr Sun" if complete else None,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }
    if drift:
        payload["local_training_allowed"] = True
    return payload


def _decision_gate(*, complete):
    return {
        "status": "f02_6_decision_gate_approved_clean" if complete else "f02_6_decision_gate_pending_clean",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _transition_gate(*, drift=False):
    payload = {
        "status": "f02_6_transition_gate_audit_passed",
        "audit_issue_count": 0,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }
    if drift:
        payload["status"] = "f02_6_transition_gate_audit_failed"
        payload["audit_issue_count"] = 1
        payload["runs_training"] = True
    return payload


def _post_plan(*, complete):
    stages = [
        {
            "stage_id": "f02_6_decision_record",
            "status": "ready" if not complete else "complete",
            "blocked_by": [],
            "evidence_paths": ["decision_record.json"],
        },
        {
            "stage_id": "gate3_remote_training",
            "status": "complete" if complete else "blocked",
            "blocked_by": [] if complete else ["remote_packet_not_ready"],
            "evidence_paths": ["final_model.zip"],
        },
    ]
    return {
        "status": "formal_chain_complete" if complete else "blocked_until_f02_6_decision",
        "runs_training": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "blocking_summary": {
            "training_allowed_now": complete,
            "remote_preflight_allowed_now": complete,
        },
        "ordered_stages": stages,
    }


def _source_freshness(*, complete):
    targets = [] if complete else [
        {
            "artifact_id": "formal_gate_gap_audit",
            "path": "0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "h02_formal_acceptance",
            "path": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_h01_h02",
        },
        {
            "artifact_id": "paper_readiness",
            "path": "0_trials/module2_paper_readiness/module2_paper_readiness.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_claim_gate",
        },
    ]
    return {
        "status": "source_freshness_clean" if complete else "source_freshness_risks_recorded_gate_still_blocked",
        "regeneration_required_before_remote_formal_execution": not complete,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "ordered_regeneration_targets": targets,
    }


def _remote_packet(*, artifacts, complete, drift=False):
    payload = {
        "status": "ready_for_remote_training_packet_execution" if complete else "blocked_until_f02_6_decision",
        "ready_to_run_remote_training": complete,
        "local_training_allowed": False,
        "formal_claim_allowed_before_audit": False,
        "post_run_pullback": {
            "required_before_local_claim": True,
            "hash_manifest_required": True,
            "expected_artifacts": [str(path) for path in artifacts],
        },
    }
    if drift:
        payload["ready_to_run_remote_training"] = True
        payload["formal_claim_allowed_before_audit"] = True
    return payload


def _remote_packet_audit():
    return {
        "status": "remote_packet_safety_audit_passed",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _h01_manifest(*, complete):
    return {
        "status": "ready_for_formal_run" if complete else "blocked_pending_decisions",
        "blockers": [] if complete else ["f02_6_warm_start_decision_pending", "missing_module2_rl_rs_checkpoint"],
    }


def _h02_acceptance(*, complete, drift=False):
    accepted = complete or drift
    return {
        "status": "formal_output_accepted" if accepted else "blocked_formal_output_acceptance",
        "formal_output_accepted": accepted,
        "paper_result_input_allowed": accepted,
        "local_training_allowed": False,
        "blockers": [] if accepted else ["missing_remote_pullback_artifacts", "missing_ppo_result_rows"],
    }


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
