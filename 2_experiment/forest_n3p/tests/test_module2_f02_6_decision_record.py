import json
from importlib import import_module

import pytest


def test_f02_6_decision_record_defaults_to_pending_and_blocks_training(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_record")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing F02.6 decision record builder: {exc}") from exc

    manifest_path = tmp_path / "decision_record.json"
    markdown_path = tmp_path / "decision_record.md"
    rc = builder.main(
        [
            "--packet",
            str(_decision_packet(tmp_path)),
            "--remote-warm-preflight",
            str(_pending_warm_preflight(tmp_path)),
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

    assert manifest["schema_version"] == 1
    assert manifest["record_name"] == "module2_f02_6_decision_record"
    assert manifest["status"] == "pending_human_decision"
    assert manifest["effective_warm_start_decision"] == "pending"
    assert manifest["remote_training_allowed"] is False
    assert manifest["remote_preflight_allowed_now"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["next_remote_preflight_status"] == "blocked_until_decision"
    assert "requires_dr_sun_approval" in manifest["blockers"]
    assert manifest["packet"]["recommendation"] == "approve_obstacle_summary_warm_start"
    assert manifest["remote_preflight_observed"]["blocker_codes"] == ["warm_start_decision_pending"]
    assert manifest["downstream_consumption"]["record_is_sufficient_to_claim_performance"] is False
    assert manifest["downstream_consumption"]["record_is_sufficient_to_run_remote_preflight_now"] is False
    assert manifest["downstream_consumption"]["record_is_sufficient_to_run_remote_training_now"] is False
    assert "gpu3070ti-relay" in markdown
    assert "blocked_until_decision" in markdown


def test_f02_6_decision_record_approval_requires_dr_sun_and_only_unlocks_remote_preflight(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_record")

    record = builder.build_record(
        builder.F026DecisionRecordConfig(
            output_dir=tmp_path,
            packet_path=_decision_packet(tmp_path),
            remote_warm_preflight_path=_pending_warm_preflight(tmp_path),
            decision="approve_obstacle_summary_warm_start",
            decider="Dr Sun",
            decision_note="Approve obstacle-summary warm-start for source-fresh regeneration.",
        )
    )

    assert record["status"] == "approved"
    assert record["decision_note"] == "Approve obstacle-summary warm-start for source-fresh regeneration."
    assert record["effective_warm_start_decision"] == "approved_obstacle_summary"
    assert record["remote_training_allowed"] is True
    assert record["remote_preflight_allowed_now"] is False
    assert record["remote_training_allowed_now"] is False
    assert record["local_training_allowed"] is False
    assert record["formal_claim_allowed"] is False
    assert record["blockers"] == []
    assert record["next_remote_preflight_status"] == "ready_to_regenerate_approved_warm_start_preflight"
    assert record["downstream_consumption"]["h01_manifest_decision_value"] == "approved_obstacle_summary"
    assert record["downstream_consumption"]["preflight_warm_start_decision_value"] == "approved_obstacle_summary"
    approved_action = record["conditional_actions"]["if_approved_obstacle_summary"]
    assert approved_action["host"] == "gpu3070ti-relay"
    assert "--warm-start-decision approved_obstacle_summary" in approved_action["preflight_command"]
    assert "--device cuda" in approved_action["preflight_command"]
    assert approved_action["runs_training"] is False


def test_f02_6_decision_record_rejects_non_dr_sun_decider(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_record")

    with pytest.raises(ValueError, match="decider='Dr Sun'"):
        builder.build_record(
            builder.F026DecisionRecordConfig(
                output_dir=tmp_path,
                packet_path=_decision_packet(tmp_path),
                remote_warm_preflight_path=_pending_warm_preflight(tmp_path),
                decision="approve_obstacle_summary_warm_start",
                decider="Assistant",
                decision_note="Assistant cannot decide F02.6.",
            )
        )


def test_f02_6_decision_record_requires_note_for_non_pending_decision(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_record")

    with pytest.raises(ValueError, match="non-empty --decision-note"):
        builder.build_record(
            builder.F026DecisionRecordConfig(
                output_dir=tmp_path,
                packet_path=_decision_packet(tmp_path),
                remote_warm_preflight_path=_pending_warm_preflight(tmp_path),
                decision="approve_obstacle_summary_warm_start",
                decider="Dr Sun",
            )
        )


def test_f02_6_decision_record_rejection_keeps_warm_start_blocked(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_f02_6_decision_record")

    record = builder.build_record(
        builder.F026DecisionRecordConfig(
            output_dir=tmp_path,
            packet_path=_decision_packet(tmp_path),
            remote_warm_preflight_path=_pending_warm_preflight(tmp_path),
            decision="reject_obstacle_summary_warm_start",
            decider="Dr Sun",
            decision_note="Use a stronger patch-CNN protocol first.",
        )
    )

    assert record["status"] == "rejected"
    assert record["effective_warm_start_decision"] == "no_warm_only"
    assert record["remote_training_allowed"] is False
    assert record["remote_preflight_allowed_now"] is False
    assert record["remote_training_allowed_now"] is False
    assert record["formal_claim_allowed"] is False
    assert "obstacle_summary_warm_start_rejected" in record["blockers"]
    assert record["downstream_consumption"]["preflight_warm_start_decision_value"] == "not_used"
    assert "stronger/full patch-CNN" in record["conditional_actions"]["if_rejected_obstacle_summary"]["next_protocol"]


def _decision_packet(tmp_path):
    path = tmp_path / "f02_6_packet.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
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
                        "runner_command": "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda --bc-checkpoint checkpoint.pt",
                        "audit_command": "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --warm-start-decision approved_obstacle_summary",
                        "host": "gpu3070ti-relay",
                    },
                    "if_rejected_obstacle_summary": {
                        "next_protocol": "run a stronger/full patch-CNN warm-start protocol before any warm-start PPO formal trial"
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _pending_warm_preflight(tmp_path):
    path = tmp_path / "gate3_preflight_manifest.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "preflight_status": "blocked",
                "formal_trial_ready": False,
                "warm_start_decision": "pending",
                "formal_blockers": [{"code": "warm_start_decision_pending"}],
                "runner_command": "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda",
                "audit_command": "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --warm-start-decision pending",
            }
        ),
        encoding="utf-8",
    )
    return path
