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
    assert state["packet_authorization_status"] == "blocked_until_dr_sun_decision"
    assert state["packet_current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert state["packet_current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert state["packet_post_decision_routes_are_current_authorization"] is False
    assert state["packet_remote_preflight_allowed_now"] is False
    assert state["packet_remote_training_allowed_now"] is False
    assert state["packet_local_training_allowed_now"] is False
    assert state["packet_formal_claim_allowed_now"] is False
    assert state["packet_paper_result_material_allowed_now"] is False
    assert state["missing_deliverable_count"] == 10
    assert state["missing_by_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert state["status_report_remote_training_allowed_now"] is False
    assert state["remaining_remote_training_allowed_now"] is False
    matrix = manifest["decision_evidence_matrix_summary"]
    assert matrix["present"] is True
    assert matrix["matrix_id"] == "module2_f02_6_decision_evidence_matrix"
    assert matrix["status"] == "ready_for_dr_sun_decision_not_authorization"
    assert matrix["route_count"] == 2
    assert matrix["route_decisions"] == [
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    ]
    assert matrix["required_evidence_count"] == 7
    assert matrix["satisfied_required_evidence_count"] == 7
    assert matrix["missing_required_evidence_count"] == 0
    assert matrix["global_invalid_substitute_count"] == 2
    assert matrix["current_authorization_allowed_now"] is False
    assert matrix["remote_preflight_allowed_now"] is False
    assert matrix["remote_training_allowed_now"] is False
    assert matrix["formal_claim_allowed_now"] is False
    assert manifest["decision_intake_contract"]["decision_owner_required"] == "Dr Sun"
    assert "decision_note" in manifest["decision_intake_contract"]["required_record_fields_for_non_pending_decision"]
    assert manifest["decision_intake_contract"]["decision_note_guidance"] == [
        "selected decision",
        "human rationale",
        "evidence basis",
        "risk accepted or avoided",
        "next gated action",
    ]
    request = manifest["next_human_decision_request"]
    assert request["status"] == "awaiting_dr_sun_decision"
    assert request["decision_owner_required"] == "Dr Sun"
    assert request["valid_decisions"] == [
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    ]
    assert request["required_record_fields"] == ["decision", "decider", "decision_note"]
    assert request["current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert request["current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert request["post_decision_routes_are_current_authorization"] is False
    assert request["all_execution_disabled_now"] is True
    assert request["route_effects"]["approve_obstacle_summary_warm_start"]["next_lane_after_record"] == (
        "source_fresh_regeneration"
    )
    assert request["route_effects"]["approve_obstacle_summary_warm_start"]["allows_remote_training_now"] is False
    assert request["route_effects"]["reject_obstacle_summary_warm_start"]["next_lane_after_record"] == (
        "protocol_redesign"
    )
    commands = {item["decision"]: item["command"] for item in manifest["decision_intake_contract"]["record_command_templates"]}
    assert "approve_obstacle_summary_warm_start" in commands
    assert "--decider 'Dr Sun'" in commands["approve_obstacle_summary_warm_start"]
    assert "reject_obstacle_summary_warm_start" in commands
    route_matrix = {item["decision"]: item for item in manifest["post_decision_route_matrix"]}
    approved_route = route_matrix["approve_obstacle_summary_warm_start"]
    assert approved_route["next_lane_after_record"] == "source_fresh_regeneration"
    assert approved_route["allows_local_training_now"] is False
    assert approved_route["allows_remote_preflight_now"] is False
    assert approved_route["allows_remote_training_now"] is False
    assert approved_route["allows_formal_claim_now"] is False
    assert approved_route["required_next_artifacts"] == [
        "source_freshness_audit",
        "post_f02_6_regeneration_plan",
        "post_f02_6_plan_audit",
    ]
    rejected_route = route_matrix["reject_obstacle_summary_warm_start"]
    assert rejected_route["next_lane_after_record"] == "protocol_redesign"
    assert rejected_route["requires_new_protocol_contract"] is True
    assert rejected_route["allows_remote_training_now"] is False

    impact = manifest["formal_gate_decision_impact_summary"]
    assert impact["summary_id"] == "module2_f02_6_formal_gate_decision_impact"
    assert impact["not_paper_result_material"] is True
    assert impact["current_blocker"] == "decision"
    assert impact["current_record_status"] == "pending_human_decision"
    assert impact["missing_deliverable_count"] == 10
    assert impact["missing_by_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert impact["current_allowed_action_ids"] == ["record_f02_6_decision"]
    route_impact = {item["decision"]: item for item in impact["decision_routes"]}
    assert route_impact["approve_obstacle_summary_warm_start"]["next_lane_after_record"] == (
        "source_fresh_regeneration"
    )
    assert route_impact["approve_obstacle_summary_warm_start"]["allows_remote_training_now"] is False
    assert route_impact["reject_obstacle_summary_warm_start"]["requires_new_protocol_contract"] is True
    invariants = impact["invariants_after_any_decision_record"]
    assert invariants["decision_record_is_not_training_authorization"] is True
    assert invariants["decision_record_is_not_paper_result_material"] is True
    assert invariants["local_training_allowed_now"] is False
    assert invariants["remote_preflight_allowed_now"] is False
    assert invariants["remote_training_allowed_now"] is False
    assert invariants["formal_claim_allowed_now"] is False
    assert invariants["paper_result_material_allowed_now"] is False
    assert "approved_remote_preflight" in invariants["formal_training_still_requires"]


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


def test_f02_6_decision_intake_catches_packet_current_authorization_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_intake")
    packet = _packet_payload()
    packet["current_authorization"]["current_allowed_action_ids"] = [
        "record_f02_6_decision",
        "remote_preflight",
    ]
    packet["current_authorization"]["current_blocked_action_ids"] = [
        "remote_training",
        "local_training",
        "formal_claim",
    ]
    packet["current_authorization"]["post_decision_routes_are_current_authorization"] = True
    packet["current_authorization"]["remote_preflight_allowed_now"] = True
    packet["current_authorization"]["paper_result_material_allowed_now"] = True

    manifest = builder.build_manifest(
        builder.F026DecisionIntakeConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", packet),
            decision_record_path=_json(tmp_path, "record.json", _record_payload()),
            decision_gate_audit_path=_json(tmp_path, "gate.json", _gate_audit_payload()),
            status_report_path=_json(tmp_path, "status.json", _status_report_payload()),
            remaining_deliverables_path=_json(tmp_path, "remaining.json", _remaining_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "f02_6_decision_intake_failed"
    assert "packet_current_allowed_actions_not_decision_only" in issue_ids
    assert "packet_current_authorization_missing_blocked_actions" in issue_ids
    assert "packet_treats_post_decision_routes_as_current_authorization" in issue_ids
    assert "packet_remote_preflight_allowed_now_not_false" in issue_ids
    assert "packet_paper_result_material_allowed_now_not_false" in issue_ids
    assert "packet_status_report_remote_preflight_permission_mismatch" in issue_ids


def test_f02_6_decision_intake_catches_decision_evidence_matrix_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_intake")
    packet = _packet_payload()
    matrix = packet["decision_evidence_matrix"]
    matrix["missing_required_evidence_count"] = 1
    matrix["missing_required_evidence_ids"] = ["remote_route_guarded_until_decision"]
    matrix["remote_training_allowed_now"] = True
    matrix["routes"][0]["invalid_substitutes"] = []

    manifest = builder.build_manifest(
        builder.F026DecisionIntakeConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", packet),
            decision_record_path=_json(tmp_path, "record.json", _record_payload()),
            decision_gate_audit_path=_json(tmp_path, "gate.json", _gate_audit_payload()),
            status_report_path=_json(tmp_path, "status.json", _status_report_payload()),
            remaining_deliverables_path=_json(tmp_path, "remaining.json", _remaining_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "f02_6_decision_intake_failed"
    assert "decision_evidence_matrix_missing_required_evidence" in issue_ids
    assert "decision_evidence_matrix_remote_training_allowed_now_not_false" in issue_ids
    assert "decision_evidence_matrix_approve_obstacle_summary_warm_start_missing_invalid_substitutes" in issue_ids


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
    assert "Next Human Decision Request" in markdown
    assert "Formal Gate Decision Impact" in markdown
    assert "all_execution_disabled_now" in markdown
    assert "packet_authorization_status" in markdown
    assert "Decision Evidence Matrix" in markdown
    assert "ready_for_dr_sun_decision_not_authorization" in markdown
    assert "decision_note_guidance" in markdown
    assert "evidence basis" in markdown
    assert "decision_note" in markdown
    assert "decision_record_is_not_training_authorization" in markdown


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
        "current_authorization": {
            "authorization_status": "blocked_until_dr_sun_decision",
            "current_allowed_action_ids": ["record_f02_6_decision"],
            "current_blocked_action_ids": [
                "remote_preflight",
                "remote_training",
                "local_training",
                "formal_claim",
                "paper_result_material",
            ],
            "post_decision_routes_are_current_authorization": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
        },
        "decision_evidence_matrix": {
            "matrix_id": "module2_f02_6_decision_evidence_matrix",
            "status": "ready_for_dr_sun_decision_not_authorization",
            "route_count": 2,
            "required_evidence_count": 7,
            "satisfied_required_evidence_count": 7,
            "missing_required_evidence_count": 0,
            "missing_required_evidence_ids": [],
            "current_authorization_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "source_issue_count": 0,
            "global_invalid_substitutes": [
                "smoke result used as formal PPO checkpoint or Gate #3 evidence",
                "paper appendix text used as a decision record",
            ],
            "routes": [
                {
                    "decision": "approve_obstacle_summary_warm_start",
                    "required_evidence": [
                        {"evidence_id": "no_warm_formal_gate3_failure"},
                        {"evidence_id": "obstacle_summary_bc_candidate_readiness"},
                        {"evidence_id": "bounded_candidate_comparison_against_patch_cnn"},
                        {"evidence_id": "remote_route_guarded_until_decision"},
                    ],
                    "invalid_substitutes": [
                        "remote CUDA smoke as formal evidence",
                        "local training output",
                    ],
                },
                {
                    "decision": "reject_obstacle_summary_warm_start",
                    "required_evidence": [
                        {"evidence_id": "reject_route_defined_in_decision_intake"},
                        {"evidence_id": "reject_route_does_not_relabel_no_warm_failure"},
                        {"evidence_id": "reject_route_requires_stronger_protocol_before_training"},
                    ],
                    "invalid_substitutes": [
                        "implicit rejection by inaction",
                        "protocol redesign without revised contract",
                    ],
                },
            ],
        },
    }


def _record_payload():
    return {
        "status": "pending_human_decision",
        "requested_decision": "pending",
        "decider": None,
        "effective_warm_start_decision": "pending",
        "remote_training_allowed": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
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
