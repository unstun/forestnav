import copy
import json
from importlib import import_module


def test_post_f02_6_plan_audit_passes_current_pending_blocked_plan(tmp_path):
    try:
        auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing post-F02.6 plan auditor: {exc}") from exc

    plan = _plan_payload()
    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_post_f02_6_plan_audit"
    assert manifest["status"] == "post_f02_6_plan_audit_passed"
    assert manifest["audit_issue_count"] == 0
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["current_blocking_summary"]["training_allowed_now"] is False
    assert manifest["current_blocking_summary"]["remote_preflight_allowed_now"] is False


def test_post_f02_6_plan_audit_catches_training_allowed_while_f02_6_pending(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["blocking_summary"]["training_allowed_now"] = True
    training = _stage(plan, "gate3_remote_training")
    training["allowed_now"] = True
    training["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "pending_f02_6_allows_training" in issue_ids
    assert "training_stage_allowed_before_f02_6" in issue_ids
    assert "training_stage_missing_f02_6_decision_not_approved" in issue_ids
    assert "training_stage_missing_remote_packet_not_ready" in issue_ids


def test_post_f02_6_plan_audit_catches_remote_training_host_and_command_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["current_gate_summary"]["f02_6_decision_status"] = "approved"
    plan["status"] = "ready_for_remote_training_packet_execution"
    plan["blocking_summary"]["training_allowed_now"] = True
    training = _stage(plan, "gate3_remote_training")
    training["allowed_now"] = True
    training["blocked_by"] = []
    training["host"] = "local-mac"
    training["command_templates"] = ["python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda"]

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload(decision_status="approved")),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "training_stage_not_gpu3070ti" in issue_ids
    assert "ready_training_stage_missing_remote_ssh" in issue_ids


def test_post_f02_6_plan_audit_catches_stage_order_and_source_target_mismatch(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["ordered_stages"] = [stage for stage in plan["ordered_stages"] if stage["stage_id"] != "approved_remote_preflight"]
    plan["source_regeneration_targets_by_gate"]["approved_remote_preflight"] = plan["source_regeneration_targets_by_gate"]["approved_remote_preflight"][:1]

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "missing_stage_approved_remote_preflight" in issue_ids
    assert "plan_source_regeneration_target_counts_mismatch" in issue_ids


def test_post_f02_6_plan_audit_consumes_open_missing_artifacts_inventory_without_blocking_training_step(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
        )
    )

    assert manifest["status"] == "post_f02_6_plan_audit_passed"
    assert manifest["missing_artifacts_summary"]["all_required_evidence_present"] is False
    assert manifest["missing_artifacts_summary"]["missing_counts_by_category"]["training"] == 3
    assert manifest["audit_issues"] == []


def test_post_f02_6_plan_audit_catches_claim_gate_ready_with_open_missing_artifacts(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    plan = _plan_payload()
    plan["current_gate_summary"]["f02_6_decision_status"] = "approved"
    plan["status"] = "ready_for_claim_gate"
    claim_stage = _stage(plan, "regenerate_claim_gate_artifacts")
    claim_stage["allowed_now"] = True
    claim_stage["status"] = "ready"
    claim_stage["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", plan),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload(decision_status="approved")),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "post_f02_6_plan_audit_failed"
    assert "claim_gate_ready_before_formal_acceptance" in issue_ids
    assert "claim_gate_ready_with_missing_artifacts" in issue_ids


def test_post_f02_6_plan_audit_rejects_missing_artifacts_inventory_that_runs_or_claims(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")

    manifest = auditor.build_manifest(
        auditor.PostF026PlanAuditConfig(
            output_dir=tmp_path,
            plan_path=_json(tmp_path, "plan.json", _plan_payload()),
            formal_gate_path=_json(tmp_path, "formal_gate.json", _formal_gate_payload()),
            source_freshness_path=_json(tmp_path, "source_freshness.json", _source_freshness_payload()),
            missing_artifacts_path=_json(
                tmp_path,
                "missing_artifacts.json",
                _missing_artifacts_payload(open_inventory=False, invalid=True),
            ),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "missing_artifacts_inventory_executes_commands" in issue_ids
    assert "missing_artifacts_inventory_runs_training" in issue_ids
    assert "missing_artifacts_inventory_runs_preflight" in issue_ids
    assert "missing_artifacts_inventory_allows_local_training" in issue_ids
    assert "missing_artifacts_inventory_allows_claim" in issue_ids
    assert "missing_artifacts_inventory_has_audit_issues" in issue_ids


def test_post_f02_6_plan_audit_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_post_f02_6_plan_audit")
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

    rc = auditor.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--plan",
            str(_json(tmp_path, "plan.json", _plan_payload())),
            "--formal-gate",
            str(_json(tmp_path, "formal_gate.json", _formal_gate_payload())),
            "--source-freshness-audit",
            str(_json(tmp_path, "source_freshness.json", _source_freshness_payload())),
            "--missing-artifacts-audit",
            str(_json(tmp_path, "missing_artifacts.json", _missing_artifacts_payload(open_inventory=True))),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "post_f02_6_plan_audit_passed"
    assert "Module2 Post-F02.6 Plan Audit" in markdown
    assert "does not execute the plan" in markdown


def _plan_payload():
    return {
        "schema_version": 1,
        "artifact_name": "module2_post_f02_6_regeneration_plan",
        "status": "blocked_until_f02_6_decision",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "current_gate_summary": {
            "f02_6_decision_status": "pending_human_decision",
            "formal_gate_status": "blocked_formal_gate_gaps_open",
            "source_freshness_status": "source_freshness_risks_recorded_gate_still_blocked",
            "source_freshness_regeneration_required": True,
            "remote_packet_status": "blocked_until_f02_6_decision",
            "ready_to_run_remote_training": False,
        },
        "source_regeneration_targets_by_gate": {
            "approved_remote_preflight": [
                {"artifact_id": "f02_6_decision_record", "path": "a.json", "freshness_state": "historical_dirty"},
                {"artifact_id": "formal_gate_gap_audit", "path": "b.json", "freshness_state": "historical_dirty"},
            ],
            "formal_h01_h02": [
                {"artifact_id": "h01_evaluation_manifest", "path": "h01.json", "freshness_state": "historical_dirty"}
            ],
            "formal_claim_gate": [
                {"artifact_id": "claim_safety", "path": "claim.json", "freshness_state": "historical_clean"}
            ],
        },
        "blocking_summary": {
            "blocked_stage_ids": [
                "regenerate_preflight_gate_artifacts",
                "approved_remote_preflight",
                "regenerate_remote_execution_packet",
                "gate3_remote_training",
                "gate3_remote_audit_pullback",
                "regenerate_h01_h02_formal_artifacts",
                "regenerate_claim_gate_artifacts",
            ],
            "ready_stage_ids": ["f02_6_decision_record"],
            "training_allowed_now": False,
            "remote_preflight_allowed_now": False,
        },
        "ordered_stages": [
            _stage_payload("f02_6_decision_record", "decision", allowed=True, human=True),
            _stage_payload("regenerate_preflight_gate_artifacts", "regeneration", blocked_by=["f02_6_decision_not_approved"]),
            _stage_payload(
                "approved_remote_preflight",
                "remote_preflight",
                runs_remote_preflight=True,
                host="gpu3070ti-relay",
                blocked_by=["f02_6_decision_not_approved", "source_fresh_preflight_targets_open"],
            ),
            _stage_payload(
                "regenerate_remote_execution_packet",
                "regeneration",
                blocked_by=["f02_6_decision_not_approved", "source_fresh_preflight_targets_open"],
            ),
            _stage_payload(
                "gate3_remote_training",
                "training",
                runs_training=True,
                host="gpu3070ti-relay",
                blocked_by=["f02_6_decision_not_approved", "source_fresh_preflight_targets_open", "remote_packet_not_ready"],
                command="ssh gpu3070ti-relay 'cd ~/ForestNav && run train'",
            ),
            _stage_payload("gate3_remote_audit_pullback", "acceptance", host="gpu3070ti-relay", blocked_by=["remote_packet_not_ready"]),
            _stage_payload(
                "regenerate_h01_h02_formal_artifacts",
                "evaluation",
                blocked_by=["missing_remote_audit_pullback", "source_fresh_h01_h02_targets_open"],
            ),
            _stage_payload(
                "regenerate_claim_gate_artifacts",
                "claim_gate",
                blocked_by=["h02_formal_acceptance_not_ready", "source_fresh_claim_targets_open"],
            ),
        ],
    }


def _stage_payload(
    stage_id,
    phase,
    *,
    allowed=False,
    human=False,
    runs_training=False,
    runs_remote_preflight=False,
    host=None,
    blocked_by=(),
    command="",
):
    return {
        "stage_id": stage_id,
        "phase": phase,
        "status": "ready" if allowed else "blocked",
        "allowed_now": allowed,
        "blocked_by": list(blocked_by),
        "runs_training": runs_training,
        "runs_remote_preflight": runs_remote_preflight,
        "host": host,
        "requires_human_input": human,
        "action": stage_id,
        "evidence_paths": [],
        "command_templates": [command] if command else [],
    }


def _formal_gate_payload(*, decision_status="pending_human_decision"):
    return {
        "status": "blocked_formal_gate_gaps_open",
        "current_gate_state": {
            "f02_6_decision_status": decision_status,
            "source_freshness_regeneration_required": True,
        },
    }


def _source_freshness_payload():
    return {
        "status": "source_freshness_risks_recorded_gate_still_blocked",
        "regeneration_required_before_remote_formal_execution": True,
        "ordered_regeneration_targets": [
            {"artifact_id": "f02_6_decision_record", "path": "a.json", "required_before": "approved_remote_preflight"},
            {"artifact_id": "formal_gate_gap_audit", "path": "b.json", "required_before": "approved_remote_preflight"},
            {"artifact_id": "h01_evaluation_manifest", "path": "h01.json", "required_before": "formal_h01_h02"},
            {"artifact_id": "claim_safety", "path": "claim.json", "required_before": "formal_claim_gate"},
        ],
    }


def _stage(plan, stage_id):
    for stage in plan["ordered_stages"]:
        if stage["stage_id"] == stage_id:
            return stage
    raise AssertionError(f"missing stage {stage_id}")


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(copy.deepcopy(payload)), encoding="utf-8")
    return path
