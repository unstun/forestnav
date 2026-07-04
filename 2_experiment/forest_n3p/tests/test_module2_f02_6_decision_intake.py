import json
from importlib import import_module


def test_f02_6_decision_intake_pending_clean_lists_required_human_fields(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_intake")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing F02.6 decision intake builder: {exc}") from exc

    manifest = builder.build_manifest(
        builder.F026DecisionIntakeConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", _record_payload()),
            decision_gate_audit_path=_json(tmp_path, "gate.json", _gate_audit_payload()),
            status_report_path=_json(tmp_path, "status.json", _status_report_payload()),
            remaining_deliverables_path=_json(tmp_path, "remaining.json", _remaining_payload()),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_f02_6_decision_intake"
    assert manifest["status"] == "f02_6_decision_intake_pending_clean"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["audit_issue_count"] == 0

    state = manifest["current_state"]
    assert state["record_status"] == "pending_human_decision"
    assert state["next_blocked_lane"] == "decision"
    assert state["missing_deliverable_count"] == 10
    assert state["missing_by_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert state["status_report_remote_training_allowed_now"] is False
    assert state["remaining_remote_training_allowed_now"] is False
    assert manifest["decision_intake_contract"]["decision_owner_required"] == "Dr Sun"
    assert "decision_note" in manifest["decision_intake_contract"]["required_record_fields_for_non_pending_decision"]
    commands = {item["decision"]: item["command"] for item in manifest["decision_intake_contract"]["record_command_templates"]}
    assert "approve_obstacle_summary_warm_start" in commands
    assert "--decider 'Dr Sun'" in commands["approve_obstacle_summary_warm_start"]
    assert "reject_obstacle_summary_warm_start" in commands


def test_f02_6_decision_intake_catches_pending_gate_permission_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_intake")
    status_report = _status_report_payload()
    status_report["permissions_now"]["remote_training_allowed_now"] = True
    remaining = _remaining_payload()
    remaining["permissions_now"]["formal_claim_allowed_now"] = True

    manifest = builder.build_manifest(
        builder.F026DecisionIntakeConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", _record_payload()),
            decision_gate_audit_path=_json(tmp_path, "gate.json", _gate_audit_payload()),
            status_report_path=_json(tmp_path, "status.json", status_report),
            remaining_deliverables_path=_json(tmp_path, "remaining.json", remaining),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "f02_6_decision_intake_failed"
    assert "status_report_remote_training_allowed_now_not_false" in issue_ids
    assert "remaining_formal_claim_allowed_now_not_false" in issue_ids


def test_f02_6_decision_intake_catches_invalid_decider_and_gate_issues(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_intake")
    record = _record_payload()
    record["status"] = "approved"
    record["requested_decision"] = "approve_obstacle_summary_warm_start"
    record["decider"] = "Assistant"
    gate = _gate_audit_payload()
    gate["status"] = "f02_6_decision_gate_audit_failed"
    gate["audit_issue_count"] = 1

    manifest = builder.build_manifest(
        builder.F026DecisionIntakeConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", record),
            decision_gate_audit_path=_json(tmp_path, "gate.json", gate),
            status_report_path=_json(tmp_path, "status.json", _status_report_payload()),
            remaining_deliverables_path=_json(tmp_path, "remaining.json", _remaining_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "f02_6_decision_intake_failed"
    assert "closed_record_decider_not_dr_sun" in issue_ids
    assert "decision_gate_has_issues" in issue_ids
    assert "decision_gate_failed" in issue_ids


def test_f02_6_decision_intake_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_intake")
    manifest_path = tmp_path / "intake.json"
    markdown_path = tmp_path / "intake.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--packet",
            str(_json(tmp_path, "packet.json", _packet_payload())),
            "--decision-record",
            str(_json(tmp_path, "record.json", _record_payload())),
            "--decision-gate-audit",
            str(_json(tmp_path, "gate.json", _gate_audit_payload())),
            "--status-report",
            str(_json(tmp_path, "status.json", _status_report_payload())),
            "--remaining-deliverables",
            str(_json(tmp_path, "remaining.json", _remaining_payload())),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "f02_6_decision_intake_pending_clean"
    assert "Module2 F02.6 Decision Intake" in markdown
    assert "does not record a decision" in markdown
    assert "decision_note" in markdown


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _packet_payload():
    return {
        "status": "pending_human_decision",
        "recommendation": {
            "decision": "approve_obstacle_summary_warm_start",
            "decision_owner": "Dr Sun",
            "formal_claim_allowed": False,
        },
    }


def _record_payload():
    return {
        "status": "pending_human_decision",
        "requested_decision": "pending",
        "decider": None,
        "effective_warm_start_decision": "pending",
        "remote_training_allowed": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _gate_audit_payload():
    return {
        "status": "f02_6_decision_gate_pending_clean",
        "audit_issue_count": 0,
        "allowed_next_human_actions": [
            {
                "decision": "approve_obstacle_summary_warm_start",
                "effect": "Allows source-fresh regeneration and approved remote preflight regeneration; does not allow paper claims.",
            },
            {
                "decision": "reject_obstacle_summary_warm_start",
                "effect": "Keeps obstacle-summary warm-start formal training blocked.",
            },
        ],
    }


def _status_report_payload():
    return {
        "status": "formal_gate_status_blocked",
        "next_blocked_lane": {
            "lane_id": "decision",
            "phase": "decision",
            "blocked_by": [
                "f02_6_decision_not_approved",
                "f02_6_warm_start_decision_pending",
                "requires_dr_sun_approval",
            ],
        },
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
    }


def _remaining_payload():
    return {
        "status": "formal_gate_deliverables_blocked",
        "missing_deliverable_count": 10,
        "open_category_count": 4,
        "category_counts": {
            "training": {"missing_count": 3},
            "evaluation": {"missing_count": 2},
            "acceptance": {"missing_count": 3},
            "formal_acceptance": {"missing_count": 2},
        },
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
    }
