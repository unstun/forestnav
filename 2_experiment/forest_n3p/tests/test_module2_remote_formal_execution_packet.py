import json
from importlib import import_module


def test_remote_formal_execution_packet_blocks_pending_decision_and_freezes_pullback_contract(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_remote_formal_execution_packet")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing remote formal execution packet builder: {exc}") from exc

    packet_path = tmp_path / "remote_execution_packet.json"
    markdown_path = tmp_path / "remote_execution_packet.md"
    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--packet-out",
            str(packet_path),
            "--markdown-out",
            str(markdown_path),
            "--decision-record",
            str(_decision_record(tmp_path, status="pending_human_decision")),
            "--h01-manifest",
            str(_h01_manifest(tmp_path)),
            "--remote-preflight",
            str(_remote_preflight(tmp_path, ready=False)),
        ]
    )

    assert rc == 0
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert packet["schema_version"] == 1
    assert packet["packet_name"] == "module2_remote_formal_execution_packet"
    assert packet["status"] == "blocked_until_f02_6_decision"
    assert packet["ready_to_run_remote_training"] is False
    assert packet["local_training_allowed"] is False
    assert packet["formal_claim_allowed_before_audit"] is False
    assert "requires_dr_sun_approval" in packet["blockers"]
    assert "missing_module2_rl_rs_checkpoint" in packet["blockers"]
    assert packet["execution_environment"]["gpu_alias"] == "gpu3070ti-relay"
    assert packet["execution_environment"]["remote_workdir"] == "~/ForestNav"
    assert packet["execution_steps"]["sync_to_remote"]["allowed_now"] is False
    assert "--delete" not in packet["execution_steps"]["sync_to_remote"]["command"]
    assert packet["execution_steps"]["run_remote_training"]["allowed_now"] is False
    assert "ssh gpu3070ti-relay" in packet["execution_steps"]["run_remote_training"]["command"]
    assert "--device cuda" in packet["execution_steps"]["run_remote_training"]["command"]
    assert packet["post_run_pullback"]["required_before_local_claim"] is True
    assert "train/final_model.zip" in "\n".join(packet["post_run_pullback"]["expected_artifacts"])
    assert "gate3_formal_audit.json" in "\n".join(packet["post_run_pullback"]["expected_artifacts"])
    assert "required_output_schema" in packet["h01_manifest"]["schema_checks"]
    assert "blocked_until_f02_6_decision" in markdown
    assert "gpu3070ti-relay" in markdown


def test_remote_formal_execution_packet_allows_only_approved_ready_remote_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_remote_formal_execution_packet")

    packet = builder.build_packet(
        builder.RemoteFormalExecutionPacketConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="approved"),
            h01_manifest_path=_h01_manifest(tmp_path, h01_blockers=()),
            remote_preflight_path=_remote_preflight(tmp_path, ready=True),
        )
    )

    assert packet["status"] == "ready_for_gpu3070ti_remote_training"
    assert packet["ready_to_run_remote_training"] is True
    assert packet["local_training_allowed"] is False
    assert packet["blockers"] == []
    assert packet["execution_steps"]["sync_to_remote"]["allowed_now"] is True
    assert packet["execution_steps"]["run_remote_training"]["allowed_now"] is True
    runner_command = packet["execution_steps"]["run_remote_training"]["command"]
    assert runner_command.startswith("ssh gpu3070ti-relay")
    assert "run_rl_rs_gate3_trial" in runner_command
    assert "--bc-checkpoint" in runner_command
    assert "--device cuda" in runner_command
    audit_command = packet["execution_steps"]["run_remote_audit"]["command"]
    assert "audit_rl_rs_gate3_trial" in audit_command
    assert "--warm-start-decision approved_obstacle_summary" in audit_command
    assert packet["downstream_after_successful_audit"]["h01_manifest_must_be_regenerated"] is True
    assert packet["downstream_after_successful_audit"]["h02_full_smoke_must_be_regenerated"] is True


def test_remote_formal_execution_packet_blocks_if_h01_schema_guard_is_missing(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_remote_formal_execution_packet")

    packet = builder.build_packet(
        builder.RemoteFormalExecutionPacketConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="approved"),
            h01_manifest_path=_h01_manifest(tmp_path, include_schema=False, h01_blockers=()),
            remote_preflight_path=_remote_preflight(tmp_path, ready=True),
        )
    )

    assert packet["ready_to_run_remote_training"] is False
    assert "h01_required_output_schema_missing" in packet["blockers"]
    assert packet["h01_manifest"]["schema_checks"]["required_output_schema"] == "missing"


def _decision_record(tmp_path, *, status):
    path = tmp_path / f"decision_record_{status}.json"
    approved = status == "approved"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "record_name": "module2_f02_6_decision_record",
                "status": status,
                "effective_warm_start_decision": "approved_obstacle_summary" if approved else "pending",
                "remote_training_allowed": approved,
                "local_training_allowed": False,
                "formal_claim_allowed": False,
                "blockers": [] if approved else ["requires_dr_sun_approval"],
                "conditional_actions": {
                    "if_approved_obstacle_summary": {
                        "host": "gpu3070ti-relay",
                        "runner_command_after_ready_preflight": (
                            "python -m forest_n3p.scripts.run_rl_rs_gate3_trial "
                            "--output-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 "
                            "--seed 20260704 --device cuda --train-curriculum-preset f03 "
                            "--eval-curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet "
                            "--heldout-seed 20260704 --train-total-timesteps 100000 --eval-episodes 64 "
                            "--allow-duplicate-openmp --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt"
                        ),
                        "audit_command_after_ready_preflight": (
                            "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial "
                            "--trial-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 "
                            "--min-formal-episodes 64 --required-success-threshold 0.8 "
                            "--required-train-curriculum f03 --required-eval-curriculum f03 "
                            "--warm-start-decision approved_obstacle_summary"
                        ),
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _h01_manifest(tmp_path, *, include_schema=True, h01_blockers=("missing_module2_rl_rs_checkpoint",)):
    path = tmp_path / f"h01_manifest_{include_schema}.json"
    payload = {
        "schema_version": 1,
        "manifest_name": "module2_v1_evaluation",
        "status": "blocked_pending_decisions" if h01_blockers else "ready_for_formal_run",
        "blockers": list(h01_blockers),
    }
    if include_schema:
        payload["required_output_schema"] = {
            "schema_status": "frozen_for_module2_v1",
            "records_csv_required_columns": ["query_id", "method", "rl_attempts", "nn_forward_time_s"],
            "summary_by_method_bucket_required_columns": ["method", "difficulty_bucket", "rl_attempts_total"],
            "summary_json_required_sections": ["summary_by_method_bucket", "paired_time_tests"],
        }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _remote_preflight(tmp_path, *, ready):
    path = tmp_path / f"remote_preflight_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "preflight_name": "module2_f03_gate3_formal_trial_preflight",
                "preflight_status": "ready" if ready else "blocked",
                "formal_trial_ready": ready,
                "warm_start_decision": "approved_obstacle_summary" if ready else "pending",
                "formal_blockers": [] if ready else [{"code": "warm_start_decision_pending"}],
                "runner_command": (
                    "python -m forest_n3p.scripts.run_rl_rs_gate3_trial "
                    "--output-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 "
                    "--seed 20260704 --device cuda --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt"
                ),
                "audit_command": (
                    "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial "
                    "--trial-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 "
                    "--warm-start-decision approved_obstacle_summary"
                ),
                "expected_artifacts": [
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip",
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json",
                ],
            }
        ),
        encoding="utf-8",
    )
    return path
