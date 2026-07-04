import copy
import json
from importlib import import_module


def test_f02_6_decision_gate_audit_passes_current_pending_gate_without_decision(tmp_path):
    try:
        auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing F02.6 decision gate auditor: {exc}") from exc

    manifest = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", _record_payload(status="pending_human_decision")),
            post_plan_path=_json(tmp_path, "plan.json", _plan_payload(status="pending_human_decision")),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_f02_6_decision_gate_audit"
    assert manifest["status"] == "f02_6_decision_gate_pending_clean"
    assert manifest["audit_issue_count"] == 0
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["decision_state"]["record_status"] == "pending_human_decision"
    assert manifest["decision_state"]["packet_recommendation"] == "approve_obstacle_summary_warm_start"
    assert manifest["decision_state"]["training_allowed_now"] is False
    assert manifest["decision_state"]["remote_preflight_allowed_now"] is False
    assert manifest["decision_state"]["remote_training_allowed_now"] is False
    actions = {item["decision"]: item for item in manifest["allowed_next_human_actions"]}
    assert set(actions) == {"approve_obstacle_summary_warm_start", "reject_obstacle_summary_warm_start"}


def test_f02_6_decision_gate_audit_catches_pending_record_that_allows_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    record = _record_payload(status="pending_human_decision")
    record["remote_training_allowed"] = True
    record["blockers"] = []
    plan = _plan_payload(status="pending_human_decision")
    plan["blocking_summary"]["training_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", record),
            post_plan_path=_json(tmp_path, "plan.json", plan),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "f02_6_decision_gate_audit_failed"
    assert "pending_record_allows_remote_training" in issue_ids
    assert "pending_record_missing_dr_sun_blocker" in issue_ids
    assert "pending_plan_allows_training" in issue_ids


def test_f02_6_decision_gate_audit_catches_packet_branch_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    packet = _packet_payload()
    packet["recommendation"]["decision_owner"] = "Assistant"
    packet["recommendation"]["formal_claim_allowed"] = True
    packet["next_actions"]["if_approved_obstacle_summary"]["host"] = "local-mac"
    packet["next_actions"]["if_approved_obstacle_summary"]["runner_command"] = "python -m train_without_checkpoint"
    packet["next_actions"]["if_rejected_obstacle_summary"]["next_protocol"] = "run the same obstacle-summary protocol"

    manifest = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", packet),
            decision_record_path=_json(tmp_path, "record.json", _record_payload(status="pending_human_decision")),
            post_plan_path=_json(tmp_path, "plan.json", _plan_payload(status="pending_human_decision")),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "packet_wrong_decision_owner" in issue_ids
    assert "packet_allows_formal_claim" in issue_ids
    assert "packet_approved_branch_wrong_host" in issue_ids
    assert "packet_approved_runner_missing_bc_checkpoint" in issue_ids
    assert "packet_approved_runner_missing_cuda" in issue_ids
    assert "packet_reject_branch_missing_stronger_protocol" in issue_ids


def test_f02_6_decision_gate_audit_catches_record_current_permission_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    record = _record_payload(status="approved")
    record["remote_preflight_allowed_now"] = True
    record["remote_training_allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", record),
            post_plan_path=_json(tmp_path, "plan.json", _plan_payload(status="approved")),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "f02_6_decision_gate_audit_failed"
    assert "record_allows_remote_preflight_now" in issue_ids
    assert "record_allows_remote_training_now" in issue_ids


def test_f02_6_decision_gate_audit_accepts_approved_record_only_when_decider_is_dr_sun(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    record = _record_payload(status="approved")
    plan = _plan_payload(status="approved")

    manifest = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", record),
            post_plan_path=_json(tmp_path, "plan.json", plan),
        )
    )

    assert manifest["status"] == "f02_6_decision_gate_audit_passed"
    assert manifest["audit_issue_count"] == 0
    assert manifest["allowed_next_human_actions"] == []

    record_bad = _record_payload(status="approved")
    record_bad["decider"] = "Assistant"
    bad = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet_bad.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record_bad.json", record_bad),
            post_plan_path=_json(tmp_path, "plan_bad.json", plan),
        )
    )
    issue_ids = {issue["issue_id"] for issue in bad["audit_issues"]}
    assert "approved_record_decider_not_dr_sun" in issue_ids


def test_f02_6_decision_gate_audit_requires_decision_note_after_closure(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    approved = _record_payload(status="approved")
    approved["decision_note"] = ""
    rejected = _record_payload(status="rejected")
    rejected.pop("decision_note")

    approved_bad = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet_approved.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record_approved.json", approved),
            post_plan_path=_json(tmp_path, "plan_approved.json", _plan_payload(status="approved")),
        )
    )
    rejected_bad = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet_rejected.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record_rejected.json", rejected),
            post_plan_path=_json(tmp_path, "plan_rejected.json", _plan_payload(status="rejected")),
        )
    )

    approved_issues = {issue["issue_id"] for issue in approved_bad["audit_issues"]}
    rejected_issues = {issue["issue_id"] for issue in rejected_bad["audit_issues"]}
    assert "approved_record_missing_decision_note" in approved_issues
    assert "rejected_record_missing_decision_note" in rejected_issues


def test_f02_6_decision_gate_audit_accepts_rejected_record_only_when_remote_training_stays_blocked(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
    record = _record_payload(status="rejected")
    plan = _plan_payload(status="rejected")

    manifest = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record.json", record),
            post_plan_path=_json(tmp_path, "plan.json", plan),
        )
    )

    assert manifest["status"] == "f02_6_decision_gate_audit_passed"
    assert manifest["audit_issue_count"] == 0

    record_bad = _record_payload(status="rejected")
    record_bad["remote_training_allowed"] = True
    record_bad["blockers"] = []
    bad = auditor.build_manifest(
        auditor.F026DecisionGateAuditConfig(
            output_dir=tmp_path,
            packet_path=_json(tmp_path, "packet_bad.json", _packet_payload()),
            decision_record_path=_json(tmp_path, "record_bad.json", record_bad),
            post_plan_path=_json(tmp_path, "plan_bad.json", plan),
        )
    )
    issue_ids = {issue["issue_id"] for issue in bad["audit_issues"]}
    assert "rejected_record_allows_remote_training" in issue_ids
    assert "rejected_record_missing_rejection_blocker" in issue_ids


def test_f02_6_decision_gate_audit_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_f02_6_decision_gate_audit")
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
            "--packet",
            str(_json(tmp_path, "packet.json", _packet_payload())),
            "--decision-record",
            str(_json(tmp_path, "record.json", _record_payload(status="pending_human_decision"))),
            "--post-plan",
            str(_json(tmp_path, "plan.json", _plan_payload(status="pending_human_decision"))),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "f02_6_decision_gate_pending_clean"
    assert "Module2 F02.6 Decision Gate Audit" in markdown
    assert "does not record a decision" in markdown


def _packet_payload():
    return {
        "packet_name": "module2_f02_6_warm_start_decision_packet",
        "status": "pending_human_decision",
        "blockers": ["requires_dr_sun_approval"],
        "recommendation": {
            "decision": "approve_obstacle_summary_warm_start",
            "decision_owner": "Dr Sun",
            "formal_claim_allowed": False,
        },
        "next_actions": {
            "if_approved_obstacle_summary": {
                "host": "gpu3070ti-relay",
                "runner_command": (
                    "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda "
                    "--bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt"
                ),
                "audit_command": "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --warm-start-decision approved_obstacle_summary",
            },
            "if_rejected_obstacle_summary": {
                "next_protocol": "run a stronger/full patch-CNN warm-start protocol before any warm-start PPO formal trial"
            },
        },
    }


def _record_payload(*, status):
    if status == "pending_human_decision":
        return {
            "record_name": "module2_f02_6_decision_record",
            "status": "pending_human_decision",
            "decision_owner_required": "Dr Sun",
            "requested_decision": "pending",
            "decider": None,
            "decision_note": None,
            "effective_warm_start_decision": "pending",
            "remote_training_allowed": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "local_training_allowed": False,
            "formal_claim_allowed": False,
            "blockers": ["requires_dr_sun_approval"],
        }
    if status == "approved":
        return {
            "record_name": "module2_f02_6_decision_record",
            "status": "approved",
            "decision_owner_required": "Dr Sun",
            "requested_decision": "approve_obstacle_summary_warm_start",
            "decider": "Dr Sun",
            "decision_note": "Approve obstacle-summary warm-start for source-fresh regeneration.",
            "effective_warm_start_decision": "approved_obstacle_summary",
            "remote_training_allowed": True,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "local_training_allowed": False,
            "formal_claim_allowed": False,
            "blockers": [],
            "conditional_actions": {
                "if_approved_obstacle_summary": {
                    "host": "gpu3070ti-relay",
                    "runs_training": False,
                }
            },
        }
    if status == "rejected":
        return {
            "record_name": "module2_f02_6_decision_record",
            "status": "rejected",
            "decision_owner_required": "Dr Sun",
            "requested_decision": "reject_obstacle_summary_warm_start",
            "decider": "Dr Sun",
            "decision_note": "Reject obstacle-summary warm-start and require stronger/full patch-CNN protocol.",
            "effective_warm_start_decision": "no_warm_only",
            "remote_training_allowed": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "local_training_allowed": False,
            "formal_claim_allowed": False,
            "blockers": ["obstacle_summary_warm_start_rejected"],
        }
    raise AssertionError(status)


def _plan_payload(*, status):
    if status == "pending_human_decision":
        return {
            "status": "blocked_until_f02_6_decision",
            "current_gate_summary": {"f02_6_decision_status": "pending_human_decision"},
            "blocking_summary": {
                "training_allowed_now": False,
                "remote_preflight_allowed_now": False,
            },
            "ordered_stages": [
                {"stage_id": "f02_6_decision_record", "requires_human_input": True},
            ],
        }
    if status == "approved":
        return {
            "status": "ready_to_execute_post_f02_6_regeneration_plan",
            "current_gate_summary": {"f02_6_decision_status": "approved"},
            "blocking_summary": {
                "training_allowed_now": False,
                "remote_preflight_allowed_now": False,
            },
            "ordered_stages": [
                {"stage_id": "f02_6_decision_record", "requires_human_input": False},
            ],
        }
    if status == "rejected":
        return {
            "status": "blocked_by_f02_6_rejected",
            "current_gate_summary": {"f02_6_decision_status": "rejected"},
            "blocking_summary": {
                "training_allowed_now": False,
                "remote_preflight_allowed_now": False,
            },
            "ordered_stages": [
                {"stage_id": "f02_6_decision_record", "requires_human_input": False},
            ],
        }
    raise AssertionError(status)


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(copy.deepcopy(payload)), encoding="utf-8")
    return path
