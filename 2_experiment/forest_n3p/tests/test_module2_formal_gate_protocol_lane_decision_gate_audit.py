import json
from importlib import import_module
from pathlib import Path


def test_protocol_lane_decision_gate_audit_accepts_pending_record_without_authorizing_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_gate_audit")

    manifest = auditor.build_manifest(
        auditor.FormalGateProtocolLaneDecisionGateAuditConfig(
            output_dir=tmp_path,
            decision_packet_path=_json(tmp_path, "packet.json", _packet()),
            decision_record_path=_json(tmp_path, "record.json", _record(status="pending_protocol_lane_decision")),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_protocol_lane_decision_gate_audit"
    assert manifest["status"] == "protocol_lane_decision_gate_pending_clean"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False
    assert manifest["decision_state"]["packet_status"] == "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun"
    assert manifest["decision_state"]["record_status"] == "pending_protocol_lane_decision"
    assert manifest["decision_state"]["selected_lane_id"] is None
    assert manifest["decision_state"]["training_authorization"] == "not_authorized_by_this_decision_record"
    assert manifest["decision_state"]["remote_training_allowed_now"] is False
    assert manifest["decision_state"]["formal_claim_allowed_now"] is False
    assert manifest["decision_note_audit_summary"]["gate_review_status"] == "not_required_while_pending"
    assert manifest["decision_note_audit_summary"]["gate_requires_note_quality"] is False
    assert manifest["allowed_next_human_actions"][0]["action_id"] == "record_protocol_lane_decision"
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_protocol_lane_decision_gate_audit_accepts_recorded_lane_without_execution_authorization(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_gate_audit")

    manifest = auditor.build_manifest(
        auditor.FormalGateProtocolLaneDecisionGateAuditConfig(
            output_dir=tmp_path,
            decision_packet_path=_json(tmp_path, "packet.json", _packet()),
            decision_record_path=_json(tmp_path, "record.json", _record(status="protocol_lane_decision_recorded")),
        )
    )

    assert manifest["status"] == "protocol_lane_decision_gate_recorded_clean"
    assert manifest["audit_issue_count"] == 0
    assert manifest["decision_state"]["selected_lane_id"] == "hybrid_ppo_analytic_fallback"
    assert manifest["decision_note_audit_summary"]["gate_review_status"] == "recorded_decision_note_audit_clean"
    assert manifest["allowed_next_human_actions"] == [
        {
            "action_id": "draft_new_or_revised_contract_after_lane_decision",
            "requires_dr_sun": False,
            "runs_training": False,
            "runs_remote_preflight": False,
            "selected_lane_id": "hybrid_ppo_analytic_fallback",
        }
    ]
    assert manifest["post_decision_gate_requirements"]["new_or_revised_contract_required"] is True
    assert "approved_or_frozen_contract" in manifest["post_decision_gate_requirements"]["formal_training_still_requires"]


def test_protocol_lane_decision_gate_audit_catches_pending_record_that_opens_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_gate_audit")
    record = _record(status="pending_protocol_lane_decision")
    record["remote_training_allowed_now"] = True
    record["current_authorization"]["remote_training_allowed_now"] = True
    record["current_authorization"]["current_blocked_action_ids"] = ["formal_claim"]

    manifest = auditor.build_manifest(
        auditor.FormalGateProtocolLaneDecisionGateAuditConfig(
            output_dir=tmp_path,
            decision_packet_path=_json(tmp_path, "packet.json", _packet()),
            decision_record_path=_json(tmp_path, "record.json", record),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "protocol_lane_decision_gate_audit_failed"
    assert "record_remote_training_allowed_now_not_false" in issue_ids
    assert "record_authorization_missing_blocked_actions" in issue_ids
    assert "record_authorization_remote_training_allowed_now_not_false" in issue_ids


def test_protocol_lane_decision_gate_audit_catches_recorded_note_and_decider_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_gate_audit")
    record = _record(status="protocol_lane_decision_recorded")
    record["decider"] = "Assistant"
    record["decision_note_audit"]["mentions_failed_gate3"] = False
    record["decision_note_audit"]["quality_warning"] = "decision_note_should_mention_failed_gate3_basis"
    record["contract_action"] = "none"

    manifest = auditor.build_manifest(
        auditor.FormalGateProtocolLaneDecisionGateAuditConfig(
            output_dir=tmp_path,
            decision_packet_path=_json(tmp_path, "packet.json", _packet()),
            decision_record_path=_json(tmp_path, "record.json", record),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "recorded_decider_not_dr_sun" in issue_ids
    assert "recorded_note_missing_mentions_failed_gate3" in issue_ids
    assert "recorded_note_quality_warning" in issue_ids
    assert "recorded_contract_action_missing" in issue_ids


def test_protocol_lane_decision_gate_audit_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_gate_audit")
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
            "--decision-packet",
            str(_json(tmp_path, "packet.json", _packet())),
            "--decision-record",
            str(_json(tmp_path, "record.json", _record(status="pending_protocol_lane_decision"))),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "protocol_lane_decision_gate_pending_clean"
    assert "Module2 Formal Gate Protocol Lane Decision Gate Audit" in markdown
    assert "not paper result material" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "pending_protocol_lane_decision" in markdown


def _json(tmp_path: Path, name: str, payload: dict):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _packet():
    lane_ids = [
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    ]
    return {
        "status": "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "decision_required": True,
        "valid_lane_ids": lane_ids,
        "current_allowed_actions": ["record_protocol_lane_decision", "draft_new_or_revised_contract_after_lane_decision"],
        "current_blocked_actions": [
            "local_training",
            "remote_success_training",
            "remote_preflight_for_new_success_attempt",
            "formal_claim",
            "paper_result_material",
        ],
    }


def _record(*, status: str):
    lane_ids = [
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    ]
    pending = status == "pending_protocol_lane_decision"
    selected_lane = None if pending else "hybrid_ppo_analytic_fallback"
    return {
        "status": status,
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "decision_owner_required": "Dr Sun",
        "requested_selected_lane": "pending" if pending else selected_lane,
        "selected_lane_id": selected_lane,
        "valid_lane_ids": lane_ids,
        "decider": None if pending else "Dr Sun",
        "decision_note": None if pending else "Select hybrid_ppo_analytic_fallback because failed Gate3 0.53125 needs revised contract.",
        "decision_note_audit": {
            "required_for_non_pending_decision": not pending,
            "present": not pending,
            "mentions_selected_lane": True,
            "mentions_failed_gate3": True,
            "mentions_contract_action": True,
            "quality_warning": None,
        },
        "contract_action": "none" if pending else "draft_revised_contract",
        "training_authorization": "not_authorized_by_this_decision_record",
        "decision_record_is_not_training_authorization": True,
        "decision_record_is_not_paper_result_material": True,
        "current_authorization": {
            "authorization_status": "blocked_until_dr_sun_lane_decision" if pending else "decision_recorded_not_execution_authorization",
            "current_allowed_action_ids": ["record_protocol_lane_decision"] if pending else ["draft_new_or_revised_contract_after_lane_decision"],
            "current_blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
            "remote_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
        },
        "post_decision_requirements": {
            "new_or_revised_contract_required": not pending,
            "contract_status_required_before_training": ["approved", "frozen"],
            "draft_contract_allows_training": False,
            "formal_training_still_requires": [
                "approved_or_frozen_contract",
                "source_freshness_audit_after_contract",
            ],
            "paper_result_still_requires": ["h02_formal_output_accepted_true"],
        },
    }
