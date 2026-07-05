import json
from importlib import import_module
from pathlib import Path


def test_contract_intake_requires_dr_sun_decisions_before_new_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_intake")

    manifest = builder.build_manifest(_config(tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_contract_intake"
    assert manifest["status"] == "formal_gate_contract_intake_ready_for_dr_sun"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["runs_remote_audit"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False
    assert manifest["contract_status_required_before_training"] == ["approved", "frozen"]
    assert manifest["contract_draft_is_not_execution_authorization"] is True

    failure = manifest["current_failed_run"]
    assert failure["formal_decision"] == "fail"
    assert failure["failure_mode"] == "threshold_failure"
    assert failure["terminal_rs_success_rate"] == 0.53125
    assert failure["required_success_threshold"] == 0.8
    assert failure["threshold_deficit"] == 0.26875

    gate = manifest["current_gate"]
    assert gate["new_success_training_allowed_now"] is False
    assert gate["local_training_allowed_now"] is False
    assert gate["formal_claim_allowed_now"] is False
    assert gate["new_or_revised_contract_required_before_new_success_training"] is True
    assert gate["h02_status"] == "blocked_formal_output_acceptance"
    assert gate["formal_output_accepted"] is False
    assert gate["paper_result_input_allowed"] is False
    assert "gate3_formal_audit_not_passed" in gate["h02_blockers"]

    assert manifest["required_field_count"] == 7
    assert manifest["required_fields_missing"] == []
    fields = {field["field_id"]: field for field in manifest["decision_fields_required_for_contract"]}
    assert fields["protocol_lane"]["status"] == "awaiting_dr_sun_decision"
    assert "explicit lane name" in fields["protocol_lane"]["required_evidence"]
    assert fields["failure_signal"]["status"] == "awaiting_dr_sun_decision"
    assert "criteria for stopping rather than extending budget after seeing weak results" in fields["failure_signal"]["required_evidence"]
    assert fields["h01_h02_acceptance_plan"]["status"] == "awaiting_dr_sun_decision"

    lanes = {lane["lane_id"]: lane for lane in manifest["candidate_protocol_lanes"]}
    assert lanes["stronger_obstacle_summary_warm_start"]["status"] == "candidate_requires_contract"
    assert lanes["full_patch_cnn_policy"]["status"] == "candidate_requires_contract"
    assert lanes["hybrid_ppo_analytic_fallback"]["status"] == "candidate_requires_contract"
    assert lanes["stop_or_reframe_module2_claim"]["status"] == "candidate_requires_contract"
    assert "whether the claim changes from replacement to hybrid assistance" in lanes["hybrid_ppo_analytic_fallback"]["must_justify"]

    output = manifest["contract_output_requirements"]
    assert output["required_location_pattern"] == ".pipeline/contracts/module2-*.md"
    assert output["allowed_status_before_training"] == ["approved", "frozen"]
    assert output["draft_status_allows_training"] is False
    assert "protocol_lane" in output["required_sections"]
    assert "failure_signal" in output["required_sections"]
    assert "H02 formal output acceptance" in output["post_contract_next_artifacts"]

    assert "use local PPO training output as formal gate evidence" in manifest["invalid_shortcuts"]
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_contract_intake_rejects_missing_next_round_requirements(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_intake")
    config = _config(tmp_path)
    next_round = json.loads(config.next_round_requirements_path.read_text(encoding="utf-8"))
    next_round["status"] = "formal_gate_next_round_requirements_blocked"
    config.next_round_requirements_path.write_text(json.dumps(next_round), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_contract_intake_blocked"
    assert "next_round_requirements_not_ready" in issue_ids


def test_contract_intake_rejects_training_or_claim_permissions(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_intake")
    config = _config(tmp_path)
    next_round = json.loads(config.next_round_requirements_path.read_text(encoding="utf-8"))
    next_round["permissions_now"]["new_success_training_allowed_now"] = True
    next_round["permissions_now"]["local_training_allowed_now"] = True
    next_round["permissions_now"]["formal_claim_allowed_now"] = True
    config.next_round_requirements_path.write_text(json.dumps(next_round), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_contract_intake_blocked"
    assert "new_success_training_allowed_before_contract" in issue_ids
    assert "local_training_allowed" in issue_ids
    assert "formal_claim_allowed" in issue_ids


def test_contract_intake_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_intake")
    config = _config(tmp_path)
    manifest_path = tmp_path / "contract_intake.json"
    markdown_path = tmp_path / "contract_intake.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--next-round-requirements",
            str(config.next_round_requirements_path),
            "--failure-triage",
            str(config.failure_triage_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_contract_intake_ready_for_dr_sun"
    assert "Module2 Formal Gate Contract Intake" in markdown
    assert "not paper result material" in markdown
    assert "protocol_lane" in markdown
    assert "failure_signal" in markdown
    assert "hybrid_ppo_analytic_fallback" in markdown
    assert "local_training_allowed_now: `False`" in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_intake")
    return builder.FormalGateContractIntakeConfig(
        output_dir=tmp_path,
        next_round_requirements_path=_write_json(tmp_path / "next_round.json", _next_round()),
        failure_triage_path=_write_json(tmp_path / "failure_triage.json", _failure_triage()),
        h02_acceptance_path=_write_json(tmp_path / "h02.json", _h02()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _next_round():
    return {
        "status": "formal_gate_next_round_requirements_ready",
        "current_failed_run": {
            "formal_decision": "fail",
            "failure_mode": "threshold_failure",
            "episodes": 64,
            "terminal_rs_success_rate": 0.53125,
            "required_success_threshold": 0.8,
            "threshold_deficit": 0.26875,
            "negative_formal_evidence_recorded": True,
        },
        "blocked_formal_acceptance": {
            "h02_status": "blocked_formal_output_acceptance",
            "formal_output_accepted": False,
            "paper_result_input_allowed": False,
            "blockers": [
                "h02_verdict_not_formal",
                "gate3_formal_audit_not_passed",
                "h02_scale_below_h01_manifest",
                "missing_ppo_result_rows",
            ],
        },
        "permissions_now": {
            "new_success_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "new_or_revised_contract_required_before_new_success_training": True,
        },
    }


def _failure_triage():
    return {
        "status": "formal_gate_failure_triage_ready",
        "formal_gate_failure": {
            "formal_decision": "fail",
            "failure_mode": "threshold_failure",
            "episodes": 64,
            "terminal_rs_success_rate": 0.53125,
            "required_success_threshold": 0.8,
            "threshold_deficit": 0.26875,
        },
    }


def _h02():
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
    }
