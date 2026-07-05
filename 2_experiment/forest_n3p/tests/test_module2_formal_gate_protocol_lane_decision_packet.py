import json
from importlib import import_module
from pathlib import Path


def test_protocol_lane_decision_packet_requires_lane_choice_without_authorizing_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_packet")

    manifest = builder.build_manifest(_config(tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_protocol_lane_decision_packet"
    assert manifest["status"] == "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["runs_remote_audit"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False

    gate = manifest["gate_summary"]
    assert gate["lane_matrix_status"] == "formal_gate_protocol_lane_matrix_ready"
    assert gate["contract_intake_status"] == "formal_gate_contract_intake_ready_for_dr_sun"
    assert gate["current_formal_decision"] == "fail"
    assert gate["current_failure_mode"] == "threshold_failure"
    assert gate["terminal_rs_success_rate"] == 0.53125
    assert gate["required_success_threshold"] == 0.8
    assert gate["new_success_training_allowed_now"] is False
    assert gate["remote_training_allowed_now"] is False
    assert gate["local_training_allowed_now"] is False
    assert gate["formal_claim_allowed_now"] is False
    assert gate["paper_result_material_allowed_now"] is False

    assert manifest["decision_required"] is True
    assert manifest["selected_lane"] is None
    assert manifest["valid_lane_ids"] == [
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    ]
    lanes = {lane["lane_id"]: lane for lane in manifest["lane_options"]}
    assert set(lanes) == set(manifest["valid_lane_ids"])
    assert lanes["stronger_obstacle_summary_warm_start"]["status"] == "awaiting_dr_sun_selection"
    assert lanes["stronger_obstacle_summary_warm_start"]["training_allowed_now"] is False
    assert lanes["stronger_obstacle_summary_warm_start"]["requires_new_or_revised_contract"] is True
    assert "why direct PPO replacement is still plausible under compact obstacle-summary features" in lanes["stronger_obstacle_summary_warm_start"]["required_decision_justification"]
    assert "whether the target claim changes from replacement to analytic-assisted hybrid control" in lanes["hybrid_ppo_analytic_fallback"]["required_decision_justification"]
    assert "the failed warm-start checkpoint" in lanes["stronger_obstacle_summary_warm_start"]["must_carry_into_contract"]["invalid_substitutes"]

    schema = manifest["decision_record_schema"]
    assert schema["record_id"] == "module2_protocol_lane_decision"
    assert "selected_lane_id" in schema["required_fields"]
    assert schema["valid_selected_lane_ids"] == manifest["valid_lane_ids"]
    assert schema["training_authorization_must_be"] == "not_authorized_by_this_decision_packet"
    assert "training_authorization that starts local or remote training directly" in schema["invalid_records"]

    assert manifest["current_allowed_actions"] == [
        "record_protocol_lane_decision",
        "draft_new_or_revised_contract_after_lane_decision",
    ]
    assert "remote_success_training" in manifest["current_blocked_actions"]
    assert "paper_result_material" in manifest["current_blocked_actions"]
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_protocol_lane_decision_packet_blocks_if_lane_matrix_not_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_packet")
    config = _config(tmp_path)
    lane_matrix = json.loads(config.lane_matrix_path.read_text(encoding="utf-8"))
    lane_matrix["status"] = "formal_gate_protocol_lane_matrix_blocked"
    config.lane_matrix_path.write_text(json.dumps(lane_matrix), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_protocol_lane_decision_packet_blocked"
    assert "lane_matrix_not_ready" in issue_ids


def test_protocol_lane_decision_packet_blocks_training_permissions(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_packet")
    config = _config(tmp_path)
    lane_matrix = json.loads(config.lane_matrix_path.read_text(encoding="utf-8"))
    lane_matrix["gate_summary"]["new_success_training_allowed_now"] = True
    lane_matrix["gate_summary"]["remote_training_allowed_now"] = True
    lane_matrix["gate_summary"]["local_training_allowed_now"] = True
    lane_matrix["gate_summary"]["formal_claim_allowed_now"] = True
    config.lane_matrix_path.write_text(json.dumps(lane_matrix), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_protocol_lane_decision_packet_blocked"
    assert "training_allowed_before_decision" in issue_ids
    assert "local_training_allowed" in issue_ids
    assert "claim_or_paper_result_allowed" in issue_ids


def test_protocol_lane_decision_packet_blocks_lanes_without_full_evidence_contract(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_packet")
    config = _config(tmp_path)
    lane_matrix = json.loads(config.lane_matrix_path.read_text(encoding="utf-8"))
    lane = lane_matrix["protocol_lane_evidence_matrix"][0]
    lane["required_contract_deltas"] = []
    lane["required_training_evidence"] = []
    lane["required_evaluation_evidence"] = []
    lane["required_acceptance_evidence"] = []
    lane["invalid_substitutes"] = []
    config.lane_matrix_path.write_text(json.dumps(lane_matrix), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_protocol_lane_decision_packet_blocked"
    assert "stronger_obstacle_summary_warm_start_missing_contract_deltas" in issue_ids
    assert "stronger_obstacle_summary_warm_start_missing_training_evidence" in issue_ids
    assert "stronger_obstacle_summary_warm_start_missing_evaluation_evidence" in issue_ids
    assert "stronger_obstacle_summary_warm_start_missing_acceptance_evidence" in issue_ids
    assert "stronger_obstacle_summary_warm_start_missing_invalid_substitutes" in issue_ids


def test_protocol_lane_decision_packet_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_packet")
    config = _config(tmp_path)
    manifest_path = tmp_path / "decision_packet.json"
    markdown_path = tmp_path / "decision_packet.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--lane-matrix",
            str(config.lane_matrix_path),
            "--contract-intake",
            str(config.contract_intake_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun"
    assert "Module2 Formal Gate Protocol Lane Decision Packet" in markdown
    assert "not paper result material" in markdown
    assert "stronger_obstacle_summary_warm_start" in markdown
    assert "hybrid_ppo_analytic_fallback" in markdown
    assert "training_authorization_must_be" in markdown
    assert "remote_success_training" in markdown
    assert "Lane Evidence Contracts" in markdown
    assert "required_training_evidence" in markdown
    assert "required_evaluation_evidence" in markdown
    assert "required_acceptance_evidence" in markdown
    assert "invalid_substitutes" in markdown
    assert "training evidence" in markdown
    assert "acceptance evidence" in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_packet")
    return builder.FormalGateProtocolLaneDecisionPacketConfig(
        output_dir=tmp_path,
        lane_matrix_path=_write_json(tmp_path / "lane_matrix.json", _lane_matrix()),
        contract_intake_path=_write_json(tmp_path / "contract_intake.json", _contract_intake()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _lane_matrix():
    return {
        "status": "formal_gate_protocol_lane_matrix_ready",
        "audit_issue_count": 0,
        "gate_summary": {
            "current_formal_decision": "fail",
            "current_failure_mode": "threshold_failure",
            "terminal_rs_success_rate": 0.53125,
            "required_success_threshold": 0.8,
            "new_success_training_allowed_now": False,
            "remote_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "new_or_revised_contract_required_before_training": True,
        },
        "protocol_lane_evidence_matrix": [
            _lane("stronger_obstacle_summary_warm_start", "direct PPO replacement attempt remains possible"),
            _lane("full_patch_cnn_policy", "direct PPO replacement claim changes substantially"),
            _lane("hybrid_ppo_analytic_fallback", "claim likely changes from PPO replacing RS to PPO assisting"),
            _lane("stop_or_reframe_module2_claim", "no new success-attempt training"),
        ],
    }


def _lane(lane_id, claim_scope):
    return {
        "lane_id": lane_id,
        "claim_scope": claim_scope,
        "required_contract_deltas": ["protocol delta"],
        "required_training_evidence": ["training evidence"],
        "required_evaluation_evidence": ["evaluation evidence"],
        "required_acceptance_evidence": ["acceptance evidence"],
        "invalid_substitutes": ["the failed warm-start checkpoint"],
    }


def _contract_intake():
    return {
        "status": "formal_gate_contract_intake_ready_for_dr_sun",
        "audit_issue_count": 0,
        "remote_training_allowed_now": False,
        "current_gate": {
            "new_success_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
    }
