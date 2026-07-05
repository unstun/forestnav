import json
from importlib import import_module
from pathlib import Path


def test_failure_triage_records_threshold_failure_without_paper_claim(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_failure_triage")

    manifest = builder.build_manifest(_config(tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_failure_triage"
    assert manifest["status"] == "formal_gate_failure_triage_ready"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["runs_remote_audit"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False

    failure = manifest["formal_gate_failure"]
    assert failure["formal_decision"] == "fail"
    assert failure["evaluator_decision"] == "fail"
    assert failure["failure_mode"] == "threshold_failure"
    assert failure["episodes"] == 64
    assert failure["terminal_rs_success_rate"] == 0.53125
    assert failure["required_success_threshold"] == 0.8
    assert failure["threshold_deficit"] == 0.26875
    assert failure["warm_start_status"] == "applied_obstacle_summary_bc"
    assert failure["warm_start_decision"] == "approved_obstacle_summary"
    assert failure["paper_success_claim_allowed"] is False

    deliverables = manifest["training_evaluation_acceptance_artifacts"]
    assert deliverables["training_complete"] is True
    assert deliverables["evaluation_complete"] is True
    assert deliverables["acceptance_complete"] is True
    assert deliverables["formal_acceptance_complete"] is False
    assert deliverables["missing_counts_by_category"] == {
        "training": 0,
        "evaluation": 0,
        "acceptance": 0,
        "formal_acceptance": 1,
    }
    assert deliverables["missing_artifacts"] == [
        {
            "category": "formal_acceptance",
            "artifact_id": "h02_formal_output_acceptance",
            "expected_path": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
            "missing_reason": (
                "h02_verdict_not_formal, gate3_formal_audit_not_passed, "
                "h02_scale_below_h01_manifest, missing_ppo_result_rows"
            ),
        }
    ]

    h02 = manifest["h02_formal_acceptance_summary"]
    assert h02["status"] == "blocked_formal_output_acceptance"
    assert h02["formal_output_accepted"] is False
    assert h02["paper_result_input_allowed"] is False
    assert "gate3_formal_audit_not_passed" in h02["blockers"]
    assert h02["gate3_formal_decision"] == "fail"
    assert h02["gate3_formal_audit_passed"] is False
    assert h02["remote_pullback_artifacts_present"] is True

    permissions = manifest["permissions_now"]
    assert permissions["local_training_allowed_now"] is False
    assert permissions["remote_preflight_allowed_now"] is True
    assert permissions["remote_training_allowed_now"] is True
    assert permissions["formal_h01_evaluation_allowed_now"] is True
    assert permissions["formal_h02_acceptance_allowed_now"] is False
    assert permissions["formal_claim_allowed_now"] is False
    assert permissions["source_freshness_ready_for_remote_preflight"] is True

    next_gate = manifest["next_gate"]
    assert next_gate["status"] == "requires_protocol_decision_before_new_success_attempt"
    assert next_gate["current_failure_can_be_recorded_as_negative_formal_evidence"] is True
    assert next_gate["same_contract_success_rerun_allowed"] is False
    assert next_gate["new_or_revised_contract_required_before_new_training"] is True
    assert next_gate["remaining_formal_blocker"]["artifact_id"] == "h02_formal_output_acceptance"
    assert next_gate["remaining_formal_blocker"]["missing"] is True
    assert "local PPO training" in next_gate["explicitly_disallowed_now"]

    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []
    assert any("must not be reframed" in item for item in manifest["claim_boundaries"])


def test_failure_triage_rejects_passing_gate3_audit(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_failure_triage")
    config = _config(tmp_path)
    gate3 = json.loads(config.gate3_audit_path.read_text(encoding="utf-8"))
    gate3["formal_decision"] = "pass"
    gate3["evaluator_decision"] = "pass"
    gate3["terminal_rs_success_rate"] = 0.875
    config.gate3_audit_path.write_text(json.dumps(gate3), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_failure_triage_blocked"
    assert "gate3_passed_not_failure_triage" in issue_ids
    assert "gate3_failure_not_proven_by_threshold" in issue_ids
    assert manifest["formal_gate_failure"]["failure_mode"] == "not_failure"


def test_failure_triage_blocks_when_core_deliverables_are_incomplete(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_failure_triage")
    config = _config(tmp_path)
    remaining = json.loads(config.remaining_deliverables_path.read_text(encoding="utf-8"))
    for category in remaining["deliverable_gap_summary"]["categories"]:
        if category["category"] == "training":
            category["status"] = "blocked"
            category["missing_count"] = 1
            category["present_count"] = 2
            category["missing_artifacts"] = [
                {
                    "artifact_id": "train_summary_json",
                    "expected_path": "train/summary.json",
                    "missing_reason": "missing",
                }
            ]
    config.remaining_deliverables_path.write_text(json.dumps(remaining), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_failure_triage_blocked"
    assert "training_deliverables_not_complete" in issue_ids
    assert manifest["training_evaluation_acceptance_artifacts"]["training_complete"] is False


def test_failure_triage_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_failure_triage")
    config = _config(tmp_path)
    manifest_path = tmp_path / "triage.json"
    markdown_path = tmp_path / "triage.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--gate3-audit",
            str(config.gate3_audit_path),
            "--gate3-eval-summary",
            str(config.gate3_eval_summary_path),
            "--remaining-deliverables",
            str(config.remaining_deliverables_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
            "--status-report",
            str(config.status_report_path),
            "--remote-packet-safety",
            str(config.remote_packet_safety_path),
            "--source-freshness",
            str(config.source_freshness_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_failure_triage_ready"
    assert "Module2 Formal Gate Failure Triage" in markdown
    assert "not paper result material" in markdown
    assert "formal_decision: `fail`" in markdown
    assert "terminal_rs_success_rate: `0.53125`" in markdown
    assert "h02_formal_output_acceptance" in markdown
    assert "new_or_revised_contract_required_before_new_training" in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_failure_triage")
    return builder.FormalGateFailureTriageConfig(
        output_dir=tmp_path,
        gate3_audit_path=_write_json(tmp_path / "gate3_formal_audit.json", _gate3_audit()),
        gate3_eval_summary_path=_write_json(tmp_path / "gate3_summary.json", _gate3_eval_summary()),
        remaining_deliverables_path=_write_json(tmp_path / "remaining_deliverables.json", _remaining_deliverables()),
        h02_acceptance_path=_write_json(tmp_path / "h02_acceptance.json", _h02_acceptance()),
        status_report_path=_write_json(tmp_path / "status_report.json", _status_report()),
        remote_packet_safety_path=_write_json(tmp_path / "remote_packet_safety.json", _remote_packet_safety()),
        source_freshness_path=_write_json(tmp_path / "source_freshness.json", _source_freshness()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _gate3_audit():
    return {
        "audit_name": "module2_gate3_formal_audit",
        "formal_decision": "fail",
        "evaluator_decision": "fail",
        "episodes": 64,
        "terminal_rs_success_rate": 0.53125,
        "required_success_threshold": 0.8,
        "warm_start_status": "applied_obstacle_summary_bc",
        "warm_start_decision": "approved_obstacle_summary",
        "formal_blockers": ["terminal_rs_success_rate_below_threshold"],
        "formal_claim_allowed": False,
    }


def _gate3_eval_summary():
    return {
        "episodes": 64,
        "terminal_rs_success_rate": 0.53125,
        "collision_rate": 0.34375,
        "truncation_rate": 0.125,
    }


def _remaining_deliverables():
    return {
        "status": "formal_gate_deliverables_blocked",
        "audit_issue_count": 0,
        "deliverable_gap_summary": {
            "total_missing_deliverables": 1,
            "open_category_count": 1,
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
        "responsible_stage_id": f"{category}_stage",
        "responsible_stage_allowed_now": missing_count == 0,
        "responsible_stage_blocked_by": [] if missing_count == 0 else ["blocked"],
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
            "remote_pullback_artifacts_present": True,
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


def _remote_packet_safety():
    return {
        "status": "remote_packet_safety_audit_passed",
        "audit_issue_count": 0,
    }


def _source_freshness():
    return {
        "status": "source_freshness_clean_current",
        "blocking_regeneration_required_before_remote_formal_execution": False,
    }
