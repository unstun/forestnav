import json
from importlib import import_module
from pathlib import Path


def test_protocol_lane_status_report_blocks_pending_lane_decision(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_status_report")

    manifest = builder.build_manifest(_config(tmp_path, recorded=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_protocol_lane_status_report"
    assert manifest["status"] == "protocol_lane_status_blocked_pending_lane_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False
    state = manifest["current_status"]
    assert state["next_blocked_lane"] == "protocol_lane_decision"
    assert state["decision_packet_status"] == "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun"
    assert state["decision_record_status"] == "pending_protocol_lane_decision"
    assert state["decision_gate_status"] == "protocol_lane_decision_gate_pending_clean"
    assert state["contract_authoring_gate_status"] == "contract_authoring_gate_blocked_pending_lane_decision"
    assert state["selected_lane_id"] is None
    assert state["contract_drafting_allowed_now"] is False
    assert state["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert "remote_success_training" in state["blocked_action_ids"]
    assert state["new_success_training_allowed_now"] is False
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_protocol_lane_status_report_allows_contract_draft_only_after_recorded_lane(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_status_report")

    manifest = builder.build_manifest(_config(tmp_path, recorded=True))

    assert manifest["status"] == "protocol_lane_status_ready_for_contract_draft"
    state = manifest["current_status"]
    assert state["next_blocked_lane"] == "new_or_revised_contract"
    assert state["decision_record_status"] == "protocol_lane_decision_recorded"
    assert state["decision_gate_status"] == "protocol_lane_decision_gate_recorded_clean"
    assert state["contract_authoring_gate_status"] == "contract_authoring_gate_ready_for_contract_draft"
    assert state["selected_lane_id"] == "hybrid_ppo_analytic_fallback"
    assert state["contract_drafting_allowed_now"] is True
    assert state["contract_approval_allowed_now"] is False
    assert state["draft_contract_allows_training"] is False
    assert state["allowed_next_action_ids"] == ["draft_new_or_revised_contract_after_lane_decision"]
    assert manifest["audit_issue_count"] == 0


def test_protocol_lane_status_report_catches_pending_state_that_allows_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_status_report")
    config = _config(tmp_path, recorded=False)
    record = json.loads(config.decision_record_path.read_text(encoding="utf-8"))
    record["remote_training_allowed_now"] = True
    config.decision_record_path.write_text(json.dumps(record), encoding="utf-8")
    contract_gate = json.loads(config.contract_authoring_gate_audit_path.read_text(encoding="utf-8"))
    contract_gate["contract_gate"]["blocked_action_ids"] = ["formal_claim"]
    config.contract_authoring_gate_audit_path.write_text(json.dumps(contract_gate), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "protocol_lane_status_report_audit_failed"
    assert "remote_training_allowed_now_unexpectedly_true" in issue_ids
    assert "blocked_actions_missing_safety_actions" in issue_ids


def test_protocol_lane_status_report_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_status_report")
    config = _config(tmp_path, recorded=False)
    manifest_path = tmp_path / "status.json"
    markdown_path = tmp_path / "status.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--decision-packet",
            str(config.decision_packet_path),
            "--decision-record",
            str(config.decision_record_path),
            "--decision-gate-audit",
            str(config.decision_gate_audit_path),
            "--contract-authoring-gate-audit",
            str(config.contract_authoring_gate_audit_path),
            "--lane-matrix",
            str(config.lane_matrix_path),
            "--next-round-requirements",
            str(config.next_round_requirements_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "protocol_lane_status_blocked_pending_lane_decision"
    assert "Module2 Formal Gate Protocol Lane Status Report" in markdown
    assert "not paper result material" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "remote_success_training" in markdown


def _config(tmp_path, *, recorded):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_status_report")
    return builder.FormalGateProtocolLaneStatusReportConfig(
        output_dir=tmp_path,
        decision_packet_path=_json(tmp_path, "decision_packet.json", _decision_packet()),
        decision_record_path=_json(tmp_path, "decision_record.json", _decision_record(recorded=recorded)),
        decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate(recorded=recorded)),
        contract_authoring_gate_audit_path=_json(tmp_path, "contract_gate.json", _contract_gate(recorded=recorded)),
        lane_matrix_path=_json(tmp_path, "lane_matrix.json", _lane_matrix()),
        next_round_requirements_path=_json(tmp_path, "next_round.json", _next_round()),
    )


def _json(tmp_path: Path, name: str, payload: dict):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _decision_packet():
    return {"status": "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun", "audit_issue_count": 0}


def _decision_record(*, recorded):
    return {
        "status": "protocol_lane_decision_recorded" if recorded else "pending_protocol_lane_decision",
        "audit_issue_count": 0,
        "selected_lane_id": "hybrid_ppo_analytic_fallback" if recorded else None,
        "contract_action": "draft_revised_contract" if recorded else "none",
        "local_training_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
    }


def _decision_gate(*, recorded):
    return {
        "status": "protocol_lane_decision_gate_recorded_clean" if recorded else "protocol_lane_decision_gate_pending_clean",
        "audit_issue_count": 0,
    }


def _contract_gate(*, recorded):
    return {
        "status": "contract_authoring_gate_ready_for_contract_draft" if recorded else "contract_authoring_gate_blocked_pending_lane_decision",
        "audit_issue_count": 0,
        "contract_gate": {
            "selected_lane_id": "hybrid_ppo_analytic_fallback" if recorded else None,
            "contract_drafting_allowed_now": recorded,
            "contract_approval_allowed_now": False,
            "draft_contract_allows_training": False,
            "allowed_next_action_ids": ["draft_new_or_revised_contract_after_lane_decision"] if recorded else ["record_protocol_lane_decision"],
            "blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
        },
    }


def _lane_matrix():
    return {"status": "formal_gate_protocol_lane_matrix_ready", "lane_count": 4}


def _next_round():
    return {"status": "formal_gate_next_round_requirements_ready"}
