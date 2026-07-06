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

    protocol = manifest["protocol_gate_summary"]
    assert protocol["protocol_status"] == "protocol_lane_status_blocked_pending_lane_decision"
    assert protocol["protocol_audit_issue_count"] == 0
    assert protocol["next_blocked_lane"] == "protocol_lane_decision"
    assert protocol["decision_record_status"] == "pending_protocol_lane_decision"
    assert protocol["selected_lane_id"] is None
    assert protocol["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert protocol["blocked_action_ids"] == [
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    ]
    assert protocol["new_success_training_allowed_now"] is False
    assert protocol["contract_drafting_allowed_now"] is False
    assert protocol["contract_approval_allowed_now"] is False
    assert protocol["post_decision_contract_plan_required_section_count"] == 8
    assert protocol["post_decision_contract_plan_shared_artifact_count"] == 10
    assert protocol["post_decision_contract_plan_lane_count"] == 4
    assert protocol["next_success_attempt_artifact_count"] == 10
    assert protocol["next_success_attempt_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert protocol["remote_safety_protocol_summary_present"] is True
    assert protocol["remote_safety_protocol_status"] == protocol["protocol_status"]
    assert protocol["remote_safety_protocol_next_blocked"] == "protocol_lane_decision"
    assert protocol["remote_safety_allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert protocol["remote_safety_new_success_training_allowed_now"] is False
    assert protocol["remote_safety_category_counts"] == protocol["next_success_attempt_artifact_category_counts"]

    reconciliation = manifest["current_vs_next_attempt_reconciliation"]
    assert reconciliation["current_failed_run_missing_counts"] == {
        "training": 0,
        "evaluation": 0,
        "acceptance": 0,
        "formal_acceptance": 1,
    }
    assert reconciliation["current_failed_run_training_eval_acceptance_closed"] is True
    assert reconciliation["current_failed_run_formal_acceptance_open"] is True
    assert reconciliation["next_success_attempt_artifact_count"] == 10
    assert reconciliation["next_success_attempt_category_counts"] == protocol["next_success_attempt_artifact_category_counts"]
    assert reconciliation["protocol_lane_artifact_counts_match_index"] is True
    assert reconciliation["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True

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

    artifact_index = manifest["next_success_attempt_artifact_index"]
    assert artifact_index["status"] == "blocked_until_protocol_lane_decision_and_contract"
    assert artifact_index["artifact_count"] == 10
    assert artifact_index["categories"] == [
        "contract",
        "training",
        "evaluation",
        "acceptance",
        "formal_acceptance",
    ]
    artifact_rows = {row["artifact_id"]: row for row in artifact_index["rows"]}
    assert set(artifact_rows) == {
        "new_or_revised_research_contract",
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
        "eval_gate3_eval_episodes_csv",
        "eval_gate3_summary_json",
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
        "h02_formal_output_acceptance",
    }
    assert artifact_rows["new_or_revised_research_contract"]["blocked_until"] == (
        "record_protocol_lane_decision"
    )
    assert artifact_rows["train_final_model_zip"]["category"] == "training"
    assert artifact_rows["train_final_model_zip"]["expected_path"] == (
        "0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip"
    )
    assert "local PPO training output" in artifact_rows["train_final_model_zip"]["invalid_substitutes"]
    assert artifact_rows["eval_gate3_eval_episodes_csv"]["category"] == "evaluation"
    assert artifact_rows["eval_gate3_eval_episodes_csv"]["blocked_until"] == (
        "new_remote_ppo_checkpoint_bundle"
    )
    assert artifact_rows["gate3_formal_audit_json"]["category"] == "acceptance"
    assert "formal_decision=pass" in artifact_rows["gate3_formal_audit_json"]["proof_requirement"]
    assert artifact_rows["h02_formal_output_acceptance"]["required_before"] == "paper_result_material"

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


def test_next_round_requirements_rejects_protocol_lane_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    config = _config(tmp_path)
    protocol = json.loads(config.protocol_lane_status_report_path.read_text(encoding="utf-8"))
    current = protocol["current_status"]
    current["next_blocked_lane"] = "remote_training"
    current["decision_record_status"] = "approved"
    current["selected_lane_id"] = "stronger_obstacle_summary_warm_start"
    current["allowed_next_action_ids"] = ["run_remote_training"]
    current["new_success_training_allowed_now"] = True
    current["contract_drafting_allowed_now"] = True
    current["next_success_attempt_artifact_category_counts"]["training"] = 1
    config.protocol_lane_status_report_path.write_text(json.dumps(protocol), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_next_round_requirements_blocked"
    assert "protocol_lane_next_blocked_drift" in issue_ids
    assert "protocol_lane_decision_record_not_pending" in issue_ids
    assert "protocol_lane_selected_before_decision" in issue_ids
    assert "protocol_lane_allowed_action_drift" in issue_ids
    assert "protocol_lane_allows_new_success_training" in issue_ids
    assert "protocol_lane_allows_contract_drafting" in issue_ids
    assert "protocol_next_attempt_category_counts_drift" in issue_ids
    assert "protocol_artifact_counts_do_not_match_index" in issue_ids


def test_next_round_requirements_requires_remote_safety_protocol_echo(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    config = _config(tmp_path)
    remote_safety = json.loads(config.remote_packet_safety_path.read_text(encoding="utf-8"))
    remote_safety["cross_gate_summary"].pop("post_plan_protocol_lane_status_summary")
    config.remote_packet_safety_path.write_text(json.dumps(remote_safety), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_next_round_requirements_blocked"
    assert "remote_safety_missing_protocol_summary" in issue_ids


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
            "--protocol-lane-status-report",
            str(config.protocol_lane_status_report_path),
            "--remote-packet-safety-audit",
            str(config.remote_packet_safety_path),
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
    assert "## Protocol Gate Summary" in markdown
    assert "protocol_status: `protocol_lane_status_blocked_pending_lane_decision`" in markdown
    assert "allowed_next_action_ids: `['record_protocol_lane_decision']`" in markdown
    assert "next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`" in markdown
    assert "## Current Vs Next Attempt Reconciliation" in markdown
    assert "current_failed_run_training_eval_acceptance_closed: `True`" in markdown
    assert "old_failed_run_artifacts_invalid_for_next_success_attempt: `True`" in markdown
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
    assert "## Next Success Attempt Artifact Index" in markdown
    assert "artifact_count: `10`" in markdown
    assert "`train_final_model_zip`" in markdown
    assert "`eval_gate3_eval_episodes_csv`" in markdown
    assert "`gate3_formal_audit_json`" in markdown
    assert "0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip" in markdown
    assert "#### `acceptance:gate3_formal_audit_json`" in markdown
    assert "audit records formal_decision=pass for the new approved protocol attempt" in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_next_round_requirements")
    return builder.FormalGateNextRoundRequirementsConfig(
        output_dir=tmp_path,
        failure_triage_path=_write_json(tmp_path / "failure_triage.json", _failure_triage()),
        remaining_deliverables_path=_write_json(tmp_path / "remaining.json", _remaining_deliverables()),
        h02_acceptance_path=_write_json(tmp_path / "h02.json", _h02_acceptance()),
        status_report_path=_write_json(tmp_path / "status_report.json", _status_report()),
        gate3_audit_path=_write_json(tmp_path / "gate3_audit.json", _gate3_audit()),
        protocol_lane_status_report_path=_write_json(tmp_path / "protocol_lane_status.json", _protocol_lane_status()),
        remote_packet_safety_path=_write_json(tmp_path / "remote_packet_safety.json", _remote_packet_safety()),
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


def _protocol_lane_status():
    return {
        "status": "protocol_lane_status_blocked_pending_lane_decision",
        "audit_issue_count": 0,
        "current_status": {
            "next_blocked_lane": "protocol_lane_decision",
            "decision_record_status": "pending_protocol_lane_decision",
            "selected_lane_id": None,
            "allowed_next_action_ids": ["record_protocol_lane_decision"],
            "blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
            "new_success_training_allowed_now": False,
            "contract_drafting_allowed_now": False,
            "contract_approval_allowed_now": False,
            "post_decision_contract_plan_status": "post_decision_contract_plan_ready_blocked_pending_lane_decision",
            "post_decision_contract_plan_required_section_count": 8,
            "post_decision_contract_plan_shared_artifact_count": 10,
            "post_decision_contract_plan_lane_count": 4,
            "next_success_attempt_artifact_status": "blocked_until_protocol_lane_decision_and_contract",
            "next_success_attempt_artifact_count": 10,
            "next_success_attempt_artifact_category_counts": {
                "contract": 1,
                "training": 3,
                "evaluation": 2,
                "acceptance": 3,
                "formal_acceptance": 1,
            },
            "next_success_attempt_artifact_ids_by_category": {
                "contract": ["new_or_revised_research_contract"],
                "training": ["train_final_model_zip", "train_summary_json", "train_training_manifest_json"],
                "evaluation": ["eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"],
                "acceptance": ["gate3_trial_manifest_json", "gate3_formal_audit_json", "pulled_back_checkpoint_hash_record"],
                "formal_acceptance": ["h02_formal_output_acceptance"],
            },
        },
    }


def _remote_packet_safety():
    protocol = _protocol_lane_status()["current_status"]
    return {
        "status": "remote_packet_safety_audit_passed",
        "audit_issue_count": 0,
        "cross_gate_summary": {
            "post_plan_protocol_lane_status_summary": {
                "status": "protocol_lane_status_blocked_pending_lane_decision",
                "next_blocked_lane": protocol["next_blocked_lane"],
                "allowed_next_action_ids": protocol["allowed_next_action_ids"],
                "new_success_training_allowed_now": protocol["new_success_training_allowed_now"],
                "next_success_attempt_artifact_category_counts": protocol[
                    "next_success_attempt_artifact_category_counts"
                ],
            }
        },
    }
