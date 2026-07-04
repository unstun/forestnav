import copy
import json
from importlib import import_module


def test_f02_6_transition_gate_audit_passes_current_formal_gate_chain(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_f02_6_transition_gate_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing F02.6 transition gate auditor: {exc}") from exc

    manifest = builder.build_manifest(builder.F026TransitionGateAuditConfig(output_dir=tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_f02_6_transition_gate_audit"
    assert manifest["status"] == "f02_6_transition_gate_audit_passed"
    assert manifest["audit_issue_count"] == 0
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["synthetic_inputs_persisted"] is False

    scenarios = {item["scenario_id"]: item for item in manifest["scenario_summaries"]}
    assert set(scenarios) == {"pending", "approved", "rejected"}

    pending = scenarios["pending"]
    assert pending["record_status"] == "pending_human_decision"
    assert pending["post_plan_status"] == "blocked_until_f02_6_decision"
    assert pending["formal_gate_status_report_next_blocked_lane_id"] == "decision"
    assert pending["formal_gate_status_report_permissions_now"]["remote_preflight_allowed_now"] is False
    assert pending["formal_gate_status_report_permissions_now"]["remote_training_allowed_now"] is False
    assert pending["formal_gate_status_report_permissions_now"]["formal_claim_allowed_now"] is False

    approved = scenarios["approved"]
    assert approved["record_status"] == "approved"
    assert approved["post_plan_status"] == "ready_to_execute_post_f02_6_regeneration_plan"
    assert approved["formal_gate_status_report_next_blocked_lane_id"] == "source_fresh_preflight"
    assert approved["post_plan_stage_summary"]["regenerate_preflight_gate_artifacts"]["allowed_now"] is True
    assert approved["post_plan_stage_summary"]["approved_remote_preflight"]["allowed_now"] is False
    assert approved["post_plan_stage_summary"]["gate3_remote_training"]["allowed_now"] is False
    assert approved["formal_gate_status_report_permissions_now"]["remote_preflight_allowed_now"] is False
    assert approved["formal_gate_status_report_permissions_now"]["remote_training_allowed_now"] is False
    assert approved["formal_gate_status_report_permissions_now"]["formal_claim_allowed_now"] is False

    rejected = scenarios["rejected"]
    assert rejected["record_status"] == "rejected"
    assert rejected["post_plan_status"] == "blocked_by_f02_6_rejected"
    assert rejected["post_plan_stage_summary"]["regenerate_preflight_gate_artifacts"]["allowed_now"] is False
    assert rejected["post_plan_stage_summary"]["gate3_remote_training"]["allowed_now"] is False
    assert rejected["formal_gate_status_report_permissions_now"]["formal_claim_allowed_now"] is False


def test_f02_6_transition_gate_audit_catches_approved_short_circuit_to_execution_or_claim(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_transition_gate_audit")

    manifest = builder.build_manifest(builder.F026TransitionGateAuditConfig(output_dir=tmp_path))
    approved = next(item for item in manifest["scenario_summaries"] if item["scenario_id"] == "approved")
    drifted = copy.deepcopy(approved)
    drifted["formal_gate_status_report_permissions_now"]["remote_preflight_allowed_now"] = True
    drifted["formal_gate_status_report_permissions_now"]["remote_training_allowed_now"] = True
    drifted["formal_gate_status_report_permissions_now"]["formal_claim_allowed_now"] = True
    drifted["post_plan_stage_summary"]["approved_remote_preflight"]["allowed_now"] = True
    drifted["post_plan_stage_summary"]["gate3_remote_training"]["allowed_now"] = True
    drifted["post_plan_stage_summary"]["regenerate_claim_gate_artifacts"]["allowed_now"] = True
    drifted["formal_gate_status_report_next_blocked_lane_id"] = "decision"

    issue_ids = {issue["issue_id"] for issue in builder._scenario_issues(drifted)}

    assert "status_report_allows_remote_training" in issue_ids
    assert "status_report_allows_formal_claim" in issue_ids
    assert "approved_status_report_allows_remote_preflight_too_early" in issue_ids
    assert "approved_remote_preflight_ready_too_early" in issue_ids
    assert "approved_training_ready_too_early" in issue_ids
    assert "approved_claim_gate_ready_too_early" in issue_ids
    assert "approved_still_reports_decision_lane" in issue_ids


def test_f02_6_transition_gate_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_transition_gate_audit")
    manifest_path = tmp_path / "transition_gate.json"
    markdown_path = tmp_path / "transition_gate.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "f02_6_transition_gate_audit_passed"
    assert "Module2 F02.6 Transition Gate Audit" in markdown
    assert "approved" in markdown
    assert "not permission to train" in markdown
