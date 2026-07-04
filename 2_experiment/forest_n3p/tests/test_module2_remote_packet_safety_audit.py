import copy
import json
from importlib import import_module


def test_remote_packet_safety_audit_passes_current_blocked_packet(tmp_path):
    try:
        auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing remote packet safety auditor: {exc}") from exc

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_remote_packet_safety_audit"
    assert manifest["status"] == "remote_packet_safety_audit_passed"
    assert manifest["audit_issue_count"] == 0
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["packet_summary"]["status"] == "blocked_until_f02_6_decision"
    assert manifest["packet_summary"]["embedded_preflight_status"] == "blocked"
    assert manifest["packet_summary"]["embedded_preflight_ready"] is False
    assert manifest["packet_summary"]["embedded_preflight_warm_start_decision"] == "pending"
    assert manifest["packet_summary"]["remote_training_allowed_now"] is False
    assert "requires_dr_sun_approval" in manifest["packet_summary"]["sync_blocked_by"]
    assert "remote_packet_not_ready" in manifest["packet_summary"]["remote_training_blocked_by"]
    assert manifest["packet_summary"]["pullback_artifact_count"] == 7
    assert manifest["cross_gate_summary"]["post_plan_status_report_status"] == "formal_gate_status_blocked"
    assert manifest["cross_gate_summary"]["post_plan_status_report_next_blocked_lane_id"] == "decision"


def test_remote_packet_safety_audit_catches_pending_packet_that_allows_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["ready_to_run_remote_training"] = True
    packet["execution_steps"]["sync_to_remote"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_training"]["allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_packet_ready_to_train" in issue_ids
    assert "pending_decision_packet_allows_sync" in issue_ids
    assert "pending_packet_training_step_allowed" in issue_ids
    assert "decision_gate_blocks_but_packet_allows_training" in issue_ids
    assert "post_plan_blocks_but_packet_allows_training" in issue_ids
    assert "blocked_status_report_packet_ready" in issue_ids
    assert "blocked_status_report_allows_remote_sync" in issue_ids
    assert "blocked_status_report_allows_remote_training" in issue_ids


def test_remote_packet_safety_audit_requires_blocked_steps_to_explain_blockers(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["execution_steps"]["sync_to_remote"]["blocked_by"] = []
    packet["execution_steps"]["run_remote_training"]["blocked_by"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "sync_to_remote_missing_blocked_by" in issue_ids
    assert "sync_to_remote_missing_requires_dr_sun_approval" in issue_ids
    assert "run_remote_training_missing_blocked_by" in issue_ids
    assert "run_remote_training_missing_remote_packet_not_ready" in issue_ids


def test_remote_packet_safety_audit_catches_pending_embedded_preflight_ready(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["remote_preflight"]["preflight_status"] = "ready"
    packet["remote_preflight"]["formal_trial_ready"] = True
    packet["remote_preflight"]["warm_start_decision"] = "approved_obstacle_summary"
    packet["remote_preflight"]["blocker_codes"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_decision_preflight_ready" in issue_ids
    assert "pending_decision_preflight_status_ready" in issue_ids
    assert "pending_decision_preflight_warm_start_not_pending" in issue_ids
    assert "pending_decision_preflight_missing_pending_blocker" in issue_ids


def test_remote_packet_safety_audit_catches_ready_packet_with_unready_embedded_preflight(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["status"] = "ready_for_gpu3070ti_remote_training"
    packet["ready_to_run_remote_training"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload(record_status="approved", training_allowed=True)),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload(training_allowed=True, status_report_ready=True)),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "ready_packet_preflight_not_ready" in issue_ids
    assert "ready_packet_preflight_status_not_ready" in issue_ids
    assert "ready_packet_preflight_warm_start_not_approved" in issue_ids


def test_remote_packet_safety_audit_requires_post_plan_status_report_summary(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    plan_audit = _plan_audit_payload()
    plan_audit["inputs"] = {}
    plan_audit.pop("status_report_summary")

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", _packet_payload()),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", plan_audit),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "post_plan_missing_status_report_input" in issue_ids
    assert "post_plan_missing_status_report_summary" in issue_ids


def test_remote_packet_safety_audit_blocks_remote_actions_when_status_report_blocked(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["status"] = "ready_for_gpu3070ti_remote_training"
    packet["ready_to_run_remote_training"] = True
    packet["execution_steps"]["sync_to_remote"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_preflight"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_training"]["allowed_now"] = True
    packet["execution_steps"]["run_remote_audit"]["allowed_now"] = True

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "remote_packet_safety_audit_failed"
    assert "pending_decision_packet_not_blocked" in issue_ids
    assert "pending_decision_packet_allows_sync" in issue_ids
    assert "blocked_status_report_packet_ready" in issue_ids
    assert "blocked_status_report_allows_remote_sync" in issue_ids
    assert "blocked_status_report_allows_remote_preflight" in issue_ids
    assert "blocked_status_report_allows_remote_training" in issue_ids
    assert "blocked_status_report_allows_remote_audit" in issue_ids


def test_remote_packet_safety_audit_catches_host_sync_and_command_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["execution_environment"]["gpu_alias"] = "local-mac"
    packet["execution_environment"]["training_host_required"] = "local-mac"
    packet["execution_steps"]["sync_to_remote"]["command"] += " --delete"
    packet["execution_steps"]["run_remote_training"]["command"] = "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cpu"
    packet["execution_steps"]["run_remote_audit"]["command"] = "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial"

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "packet_wrong_gpu_alias" in issue_ids
    assert "packet_wrong_training_host" in issue_ids
    assert "sync_uses_delete" in issue_ids
    assert "training_not_remote_ssh" in issue_ids
    assert "training_missing_device_cuda" in issue_ids
    assert "training_missing_bc_checkpoint" in issue_ids
    assert "audit_missing_ssh_gpu3070ti_relay" in issue_ids
    assert "audit_missing_warm_start_decision_approved_obstacle_summary" in issue_ids


def test_remote_packet_safety_audit_catches_pullback_and_downstream_drift(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
    packet = _packet_payload()
    packet["post_run_pullback"]["expected_artifacts"] = packet["post_run_pullback"]["expected_artifacts"][:2]
    packet["post_run_pullback"]["hash_manifest_required"] = False
    packet["post_run_pullback"]["pullback_command"] = "rsync -az --delete localhost:/tmp/run ./run"
    packet["downstream_after_successful_audit"]["h01_manifest_must_be_regenerated"] = False
    packet["downstream_after_successful_audit"]["formal_claim_requires"] = []

    manifest = auditor.build_manifest(
        auditor.RemotePacketSafetyAuditConfig(
            output_dir=tmp_path,
            remote_packet_path=_json(tmp_path, "packet.json", packet),
            decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate_payload()),
            post_plan_audit_path=_json(tmp_path, "plan_audit.json", _plan_audit_payload()),
        )
    )

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "pullback_wrong_artifact_count" in issue_ids
    assert "pullback_hash_manifest_not_required" in issue_ids
    assert "pullback_not_from_gpu3070ti" in issue_ids
    assert "pullback_uses_delete" in issue_ids
    assert "downstream_missing_h01_manifest_must_be_regenerated" in issue_ids
    assert "claim_requirement_missing_gate3_formal_audit_formal_decision_is_pass" in issue_ids


def test_remote_packet_safety_audit_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_remote_packet_safety_audit")
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
            "--remote-packet",
            str(_json(tmp_path, "packet.json", _packet_payload())),
            "--decision-gate-audit",
            str(_json(tmp_path, "decision_gate.json", _decision_gate_payload())),
            "--post-plan-audit",
            str(_json(tmp_path, "plan_audit.json", _plan_audit_payload())),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "remote_packet_safety_audit_passed"
    assert "Module2 Remote Packet Safety Audit" in markdown
    assert "does not execute any command" in markdown


def _packet_payload():
    trial = "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1"
    return {
        "packet_name": "module2_remote_formal_execution_packet",
        "status": "blocked_until_f02_6_decision",
        "ready_to_run_remote_training": False,
        "local_training_allowed": False,
        "formal_claim_allowed_before_audit": False,
        "execution_environment": {
            "gpu_alias": "gpu3070ti-relay",
            "remote_workdir": "~/ForestNav",
            "remote_python": ".venv/bin/python",
            "training_host_required": "gpu3070ti-relay",
        },
        "remote_preflight": {
            "path": "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json",
            "exists": True,
            "preflight_status": "blocked",
            "formal_trial_ready": False,
            "warm_start_decision": "pending",
            "blocker_codes": ["warm_start_decision_pending"],
        },
        "execution_steps": {
            "sync_to_remote": {
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["requires_dr_sun_approval"],
                "command": "rsync -az --exclude .git --exclude '.venv*' --exclude __pycache__ --exclude .pytest_cache --exclude 1_survey /local/ForestNav/ 'gpu3070ti-relay:~/ForestNav/'",
            },
            "run_remote_preflight": {
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["requires_dr_sun_approval"],
                "command": "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial'",
            },
            "run_remote_training": {
                "allowed_now": False,
                "runs_training": True,
                "blocked_by": ["requires_dr_sun_approval", "remote_packet_not_ready"],
                "command": (
                    "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python "
                    "-m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda --bc-checkpoint checkpoint.pt "
                    "--eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8'"
                ),
            },
            "run_remote_audit": {
                "allowed_now": False,
                "runs_training": False,
                "blocked_by": ["requires_dr_sun_approval", "remote_packet_not_ready"],
                "command": "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --warm-start-decision approved_obstacle_summary'",
            },
        },
        "post_run_pullback": {
            "required_before_local_claim": True,
            "hash_manifest_required": True,
            "expected_artifacts": [
                f"{trial}/train/final_model.zip",
                f"{trial}/train/summary.json",
                f"{trial}/train/training_manifest.json",
                f"{trial}/eval/gate3_eval_episodes.csv",
                f"{trial}/eval/gate3_summary.json",
                f"{trial}/gate3_trial_manifest.json",
                f"{trial}/gate3_formal_audit.json",
            ],
            "pullback_command": f"rsync -az 'gpu3070ti-relay:~/ForestNav/{trial}/' /local/ForestNav/{trial}/",
        },
        "downstream_after_successful_audit": {
            "h01_manifest_must_be_regenerated": True,
            "h02_full_smoke_must_be_regenerated": True,
            "paper_tables_must_be_regenerated_from_h02_formal_outputs": True,
            "formal_claim_requires": [
                "gate3_formal_audit.formal_decision is pass",
                "pulled-back checkpoint hash is recorded",
                "H01 manifest status becomes ready_for_formal_run with this checkpoint",
                "H02 full all-method smoke and formal evaluation outputs include required_output_schema columns",
            ],
        },
    }


def _decision_gate_payload(*, record_status="pending_human_decision", training_allowed=False):
    return {
        "status": "f02_6_decision_gate_pending_clean" if record_status == "pending_human_decision" else "f02_6_decision_gate_approved_clean",
        "decision_state": {
            "record_status": record_status,
            "training_allowed_now": training_allowed,
        },
    }


def _plan_audit_payload(*, training_allowed=False, status_report_ready=False):
    return {
        "status": "post_f02_6_plan_audit_passed",
        "inputs": {
            "formal_gate_status_report": "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
        },
        "current_blocking_summary": {
            "training_allowed_now": training_allowed,
            "remote_preflight_allowed_now": training_allowed,
        },
        "status_report_summary": {
            "status": "formal_gate_status_ready_for_claim_audit" if status_report_ready else "formal_gate_status_blocked",
            "formal_claim_allowed_now": status_report_ready,
            "local_training_allowed_now": False,
            "next_blocked_lane_id": None if status_report_ready else "decision",
        },
    }


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(copy.deepcopy(payload)), encoding="utf-8")
    return path
