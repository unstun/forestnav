import json
from importlib import import_module
from pathlib import Path


def test_next_round_requirements_blocks_new_success_attempt_until_contract(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")

    manifest = builder.build_manifest(_config(tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_next_round_requirements"
    assert manifest["status"] == "formal_gate_next_round_requirements_ready"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["runs_remote_audit"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False

    failure = manifest["current_failed_run"]
    assert failure["failure_triage_status"] == "formal_gate_failure_triage_ready"
    assert failure["failure_triage_audit_issue_count"] == 0
    assert failure["formal_decision"] == "fail"
    assert failure["evaluator_decision"] == "fail"
    assert failure["failure_mode"] == "threshold_failure"
    assert failure["episodes"] == 64
    assert failure["terminal_rs_success_rate"] == 0.53125
    assert failure["required_success_threshold"] == 0.8
    assert failure["threshold_deficit"] == 0.26875
    assert failure["negative_formal_evidence_recorded"] is True
    assert failure["paper_success_claim_allowed"] is False

    current_artifacts = manifest["current_run_artifacts"]
    assert current_artifacts["training_complete_for_failed_run"] is True
    assert current_artifacts["evaluation_complete_for_failed_run"] is True
    assert current_artifacts["acceptance_complete_for_failed_run"] is True
    assert current_artifacts["formal_acceptance_complete_for_failed_run"] is False
    assert current_artifacts["missing_counts_by_formal_category"] == {
        "training": 0,
        "evaluation": 0,
        "acceptance": 0,
        "formal_acceptance": 1,
    }

    h02 = manifest["blocked_formal_acceptance"]
    assert h02["h02_status"] == "blocked_formal_output_acceptance"
    assert h02["formal_output_accepted"] is False
    assert h02["paper_result_input_allowed"] is False
    assert h02["gate3_formal_decision"] == "fail"
    assert h02["gate3_formal_audit_passed"] is False
    assert h02["scale_satisfies_h01"] is False
    assert h02["has_ppo_result_rows"] is False
    assert h02["ppo_rows_have_checkpoint_hash"] is False
    assert "gate3_formal_audit_not_passed" in h02["blockers"]
    assert h02["missing_artifacts"][0]["artifact_id"] == "h02_formal_output_acceptance"

    permissions = manifest["permissions_now"]
    assert permissions["local_training_allowed_now"] is False
    assert permissions["remote_preflight_allowed_now"] is False
    assert permissions["remote_training_allowed_now_for_existing_packet"] is False
    assert permissions["formal_h01_evaluation_allowed_now"] is False
    assert permissions["formal_claim_allowed_now"] is False
    assert permissions["source_freshness_ready_for_remote_preflight"] is False
    assert permissions["new_success_training_allowed_now"] is False
    assert permissions["new_or_revised_contract_required_before_new_success_training"] is True
    assert permissions["failure_triage_next_gate_status"] == "requires_protocol_decision_before_new_success_attempt"
    assert permissions["execution_veto_reason"] == "protocol_lane_or_contract_gate_blocks_execution"
    assert permissions["legacy_remote_packet_readiness"] == {
        "remote_preflight_allowed_by_status_report": True,
        "remote_training_allowed_by_status_report": True,
        "formal_h01_evaluation_allowed_by_status_report": True,
        "superseded_by_next_gate": True,
    }

    next_round = manifest["next_round_requirements"]
    assert next_round["status"] == "new_or_revised_contract_required_before_any_new_success_attempt"
    assert next_round["not_paper_result_material"] is True
    assert next_round["runs_training"] is False
    assert next_round["new_success_training_allowed_now"] is False
    assert next_round["categories"] == ["contract", "training", "evaluation", "acceptance", "formal_acceptance"]
    rows = {row["requirement_id"]: row for row in next_round["rows"]}
    assert rows["new_or_revised_research_contract"]["status"] == "missing_required_before_new_training"
    assert rows["new_remote_ppo_checkpoint_bundle"]["status"] == "blocked_until_contract"
    assert "the failed warm-start Gate3 checkpoint" in rows["new_remote_ppo_checkpoint_bundle"]["invalid_substitutes"]
    assert rows["new_formal_gate3_eval_bundle"]["status"] == "blocked_until_new_checkpoint"
    assert rows["new_gate3_audit_and_hash_acceptance"]["status"] == "blocked_until_new_eval"
    assert rows["h02_formal_output_acceptance"]["status"] == "blocked_until_new_gate3_pass"

    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []
    assert any("Local PPO training remains disallowed" in item for item in manifest["claim_boundaries"])


def test_next_round_requirements_rejects_not_ready_failure_triage(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    config = _config(tmp_path)
    triage = json.loads(config.failure_triage_path.read_text(encoding="utf-8"))
    triage["status"] = "formal_gate_failure_triage_blocked"
    triage["audit_issue_count"] = 1
    config.failure_triage_path.write_text(json.dumps(triage), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_next_round_requirements_blocked"
    assert "failure_triage_not_ready" in issue_ids


def test_next_round_requirements_rejects_incomplete_failed_run_artifacts(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    config = _config(tmp_path)
    remaining = json.loads(config.remaining_deliverables_path.read_text(encoding="utf-8"))
    for category in remaining["deliverable_gap_summary"]["categories"]:
        if category["category"] == "evaluation":
            category["status"] = "blocked"
            category["missing_count"] = 1
            category["present_count"] = 1
    config.remaining_deliverables_path.write_text(json.dumps(remaining), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_next_round_requirements_blocked"
    assert "failed_run_evaluation_artifacts_incomplete" in issue_ids
    assert manifest["current_run_artifacts"]["evaluation_complete_for_failed_run"] is False


def test_next_round_requirements_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    config = _config(tmp_path)
    manifest_path = tmp_path / "next_round.json"
    markdown_path = tmp_path / "next_round.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--failure-triage",
            str(config.failure_triage_path),
            "--remaining-deliverables",
            str(config.remaining_deliverables_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
            "--status-report",
            str(config.status_report_path),
            "--gate3-audit",
            str(config.gate3_audit_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_next_round_requirements_ready"
    assert "Module2 Formal Gate Next-Round Requirements" in markdown
    assert "not paper result material" in markdown
    assert "formal_decision: `fail`" in markdown
    assert "formal_acceptance_missing: `1`" in markdown
    assert "new_or_revised_research_contract" in markdown
    assert "new_remote_ppo_checkpoint_bundle" in markdown
    assert "h02_formal_output_acceptance" in markdown
    assert "## Permissions Now" in markdown
    assert "remote_preflight_allowed_now: `False`" in markdown
    assert "remote_training_allowed_now_for_existing_packet: `False`" in markdown
    assert "formal_h01_evaluation_allowed_now: `False`" in markdown
    assert "new_success_training_allowed_now: `False`" in markdown
    assert "execution_veto_reason: `protocol_lane_or_contract_gate_blocks_execution`" in markdown
    assert "legacy_remote_packet_readiness" in markdown
    assert "## Missing Current Formal Acceptance Artifacts" in markdown
    assert "h02_verdict_not_formal, gate3_formal_audit_not_passed" in markdown
    assert "## Missing Next-Round Deliverables" in markdown
    assert "### `training:new_remote_ppo_checkpoint_bundle`" in markdown
    assert "remote-produced train/final_model.zip under a new attempt directory" in markdown
    assert "local PPO training output" in markdown
    assert "### `evaluation:new_formal_gate3_eval_bundle`" in markdown
    assert "eval/gate3_eval_episodes.csv from the new approved formal run" in markdown
    assert "terminal-RS success rate, collision rate, truncation rate, timing, and seed/protocol provenance are present" in markdown
    assert "### `acceptance:new_gate3_audit_and_hash_acceptance`" in markdown
    assert "gate3_formal_audit.json for the new attempt records formal_decision=pass" in markdown
    assert "train/final_model.zip.sha256 or equivalent hash manifest matches the pulled-back checkpoint" in markdown
    assert "### `formal_acceptance:h02_formal_output_acceptance`" in markdown
    assert "formal PPO rows are present and include the accepted checkpoint hash" in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    return builder.FormalGateNextRoundRequirementsConfig(
        output_dir=tmp_path,
        failure_triage_path=_write_json(tmp_path / "failure_triage.json", _failure_triage()),
        remaining_deliverables_path=_write_json(tmp_path / "remaining.json", _remaining_deliverables()),
        h02_acceptance_path=_write_json(tmp_path / "h02.json", _h02_acceptance()),
        status_report_path=_write_json(tmp_path / "status_report.json", _status_report()),
        gate3_audit_path=_write_json(tmp_path / "gate3_audit.json", _gate3_audit()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _failure_triage():
    return {
        "status": "formal_gate_failure_triage_ready",
        "audit_issue_count": 0,
        "formal_gate_failure": {
            "formal_decision": "fail",
            "evaluator_decision": "fail",
            "failure_mode": "threshold_failure",
            "episodes": 64,
            "terminal_rs_success_rate": 0.53125,
            "required_success_threshold": 0.8,
            "threshold_deficit": 0.26875,
            "warm_start_status": "applied_obstacle_summary_bc",
            "warm_start_decision": "approved_obstacle_summary",
        },
        "next_gate": {
            "status": "requires_protocol_decision_before_new_success_attempt",
            "new_or_revised_contract_required_before_new_training": True,
        },
    }


def _remaining_deliverables():
    return {
        "status": "formal_gate_deliverables_blocked",
        "audit_issue_count": 0,
        "deliverable_gap_summary": {
            "categories": [
                _category("training", "complete", 3, 0),
                _category("evaluation", "complete", 2, 0),
                _category("acceptance", "complete", 3, 0),
                _category(
                    "formal_acceptance",
                    "blocked",
                    1,
                    1,
                    missing_artifacts=[
                        {
                            "matrix_id": "formal_acceptance:h02_formal_output_acceptance",
                            "artifact_id": "h02_formal_output_acceptance",
                            "expected_path": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                            "missing_reason": (
                                "h02_verdict_not_formal, gate3_formal_audit_not_passed, "
                                "h02_scale_below_h01_manifest, missing_ppo_result_rows"
                            ),
                        }
                    ],
                ),
            ],
        },
    }


def _category(category, status, present_count, missing_count, *, missing_artifacts=None):
    return {
        "category": category,
        "status": status,
        "present_count": present_count,
        "missing_count": missing_count,
        "missing_artifacts": missing_artifacts or [],
    }


def _h02_acceptance():
    return {
        "status": "blocked_formal_output_acceptance",
        "formal_output_accepted": False,
        "paper_result_input_allowed": False,
        "blockers": [
            "h02_verdict_not_formal",
            "gate3_formal_audit_not_passed",
            "h02_scale_below_h01_manifest",
            "missing_ppo_result_rows",
        ],
        "formal_checks": {
            "gate3_formal_decision": "fail",
            "gate3_formal_audit_passed": False,
            "scale_satisfies_h01": False,
        },
        "method_checks": {
            "has_ppo_result_rows": False,
            "ppo_rows_have_checkpoint_hash": False,
        },
    }


def _status_report():
    return {
        "status": "formal_gate_status_blocked",
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": True,
            "remote_training_allowed_now": True,
            "formal_h01_evaluation_allowed_now": True,
            "formal_h02_acceptance_allowed_now": False,
            "formal_claim_allowed_now": False,
            "source_freshness_ready_for_remote_preflight": True,
        },
    }


def _gate3_audit():
    return {
        "formal_decision": "fail",
        "evaluator_decision": "fail",
        "episodes": 64,
        "terminal_rs_success_rate": 0.53125,
        "required_success_threshold": 0.8,
        "warm_start_status": "applied_obstacle_summary_bc",
        "warm_start_decision": "approved_obstacle_summary",
    }
