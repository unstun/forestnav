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
            "--protocol-lane-status-report",
            str(_protocol_lane_status(tmp_path, pending=False)),
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
    assert "requires_dr_sun_approval" in packet["execution_steps"]["sync_to_remote"]["blocked_by"]
    assert "requires_dr_sun_approval" in packet["execution_steps"]["run_remote_preflight"]["blocked_by"]
    assert "--delete" not in packet["execution_steps"]["sync_to_remote"]["command"]
    assert packet["execution_steps"]["run_remote_training"]["allowed_now"] is False
    assert "remote_packet_not_ready" in packet["execution_steps"]["run_remote_training"]["blocked_by"]
    assert "remote_packet_not_ready" in packet["execution_steps"]["run_remote_audit"]["blocked_by"]
    assert packet["remote_preflight_requirement_counts"] == {"blocked_missing_preflight": 2, "satisfied": 2}
    requirements = {item["requirement_id"]: item for item in packet["remote_preflight_requirements"]}
    assert requirements["f02_6_decision_closed_for_preflight"]["status"] == "blocked_missing_preflight"
    assert requirements["approved_remote_preflight_manifest"]["status"] == "blocked_missing_preflight"
    assert requirements["remote_preflight_protocol_contract"]["status"] == "satisfied"
    assert requirements["remote_preflight_command_packetized"]["status"] == "satisfied"
    assert "local preflight output" in requirements["approved_remote_preflight_manifest"]["invalid_substitutes"]
    assert "ssh gpu3070ti-relay" in packet["execution_steps"]["run_remote_training"]["command"]
    assert "--device cuda" in packet["execution_steps"]["run_remote_training"]["command"]
    assert packet["post_run_pullback"]["required_before_local_claim"] is True
    assert "train/final_model.zip" in "\n".join(packet["post_run_pullback"]["expected_artifacts"])
    assert "gate3_formal_audit.json" in "\n".join(packet["post_run_pullback"]["expected_artifacts"])
    assert packet["post_run_acceptance_requirement_counts"] == {"blocked_until_remote_audit": 4}
    post_run = {item["requirement_id"]: item for item in packet["post_run_acceptance_requirements"]}
    assert post_run["pullback_expected_artifacts_complete"]["remote_training_ready_now"] is False
    assert post_run["pullback_expected_artifacts_complete"]["execution_allowed_now"] is False
    assert post_run["checkpoint_hash_manifest_recorded"]["status"] == "blocked_until_remote_audit"
    assert "checkpoint file without hash" in post_run["checkpoint_hash_manifest_recorded"]["invalid_substitutes"]
    assert post_run["gate3_formal_audit_accepts_remote_run"]["missing_artifact_ids"] == [
        "gate3_formal_audit_formal_decision_pass"
    ]
    assert "no-warm Gate3 audit reused as warm-start audit" in post_run["gate3_formal_audit_accepts_remote_run"]["invalid_substitutes"]
    assert "required_output_schema" in packet["h01_manifest"]["schema_checks"]
    assert "blocked_until_f02_6_decision" in markdown
    assert "Remote Preflight Requirements" in markdown
    assert "Post-Run Acceptance Requirements" in markdown
    assert "gpu3070ti-relay" in markdown


def test_remote_formal_execution_packet_allows_only_approved_ready_remote_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_remote_formal_execution_packet")

    packet = builder.build_packet(
        builder.RemoteFormalExecutionPacketConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="approved"),
            h01_manifest_path=_h01_manifest(tmp_path, h01_blockers=()),
            remote_preflight_path=_remote_preflight(tmp_path, ready=True),
            protocol_lane_status_report_path=_protocol_lane_status(tmp_path, pending=False),
        )
    )

    assert packet["status"] == "ready_for_gpu3070ti_remote_training"
    assert packet["ready_to_run_remote_training"] is True
    assert packet["local_training_allowed"] is False
    assert packet["blockers"] == []
    assert packet["execution_steps"]["sync_to_remote"]["allowed_now"] is True
    assert packet["execution_steps"]["sync_to_remote"]["blocked_by"] == []
    assert packet["execution_steps"]["run_remote_training"]["allowed_now"] is True
    assert packet["execution_steps"]["run_remote_training"]["blocked_by"] == []
    assert packet["remote_preflight_requirement_counts"] == {"satisfied": 4}
    assert all(item["status"] == "satisfied" for item in packet["remote_preflight_requirements"])
    assert packet["post_run_acceptance_requirement_counts"] == {"blocked_until_remote_audit": 4}
    assert all(item["remote_training_ready_now"] is True for item in packet["post_run_acceptance_requirements"])
    assert all(item["execution_allowed_now"] is False for item in packet["post_run_acceptance_requirements"])
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
            protocol_lane_status_report_path=_protocol_lane_status(tmp_path, pending=False),
        )
    )

    assert packet["ready_to_run_remote_training"] is False
    assert "h01_required_output_schema_missing" in packet["blockers"]
    assert packet["h01_manifest"]["schema_checks"]["required_output_schema"] == "missing"


def test_remote_formal_execution_packet_blocks_protocol_lane_pending_even_after_f02_6_approval(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_remote_formal_execution_packet")

    packet = builder.build_packet(
        builder.RemoteFormalExecutionPacketConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="approved"),
            h01_manifest_path=_h01_manifest(tmp_path, h01_blockers=()),
            remote_preflight_path=_remote_preflight(tmp_path, ready=True),
            protocol_lane_status_report_path=_protocol_lane_status(tmp_path, pending=True),
        )
    )

    assert packet["status"] == "blocked_until_protocol_lane_decision"
    assert packet["ready_to_run_remote_training"] is False
    assert "protocol_lane_decision_pending" in packet["blockers"]
    assert packet["protocol_lane_status"]["pending_lane_decision"] is True
    assert packet["protocol_lane_status"]["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    for step_id in ("sync_to_remote", "run_remote_preflight", "run_remote_training", "run_remote_audit"):
        step = packet["execution_steps"][step_id]
        assert step["allowed_now"] is False
        assert "protocol_lane_decision_pending" in step["blocked_by"]


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
                        "preflight_command": (
                            "python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial "
                            "--output-dir 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1 "
                            "--manifest-out 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json "
                            "--warm-start-decision approved_obstacle_summary --bc-checkpoint "
                            "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt "
                            "--device cuda --allow-duplicate-openmp --allow-existing-output-dir"
                        ),
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


def _protocol_lane_status(tmp_path, *, pending):
    path = tmp_path / f"protocol_lane_status_{pending}.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "artifact_name": "module2_formal_gate_protocol_lane_status_report",
                "status": (
                    "protocol_lane_status_blocked_pending_lane_decision"
                    if pending
                    else "protocol_lane_status_not_pending_lane_decision"
                ),
                "current_status": {
                    "next_blocked_lane": "protocol_lane_decision" if pending else "source_fresh_preflight",
                    "selected_lane_id": None if pending else "stronger_obstacle_summary_warm_start",
                    "decision_record_status": "pending_protocol_lane_decision" if pending else "recorded_protocol_lane_decision",
                    "allowed_next_action_ids": ["record_protocol_lane_decision"] if pending else [],
                    "blocked_action_ids": [
                        "local_training",
                        "remote_success_training",
                        "remote_preflight_for_new_success_attempt",
                        "formal_claim",
                        "paper_result_material",
                    ]
                    if pending
                    else [],
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
                "command": (
                    "python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial "
                    "--output-dir 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1 "
                    "--manifest-out 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json "
                    "--warm-start-decision approved_obstacle_summary --bc-checkpoint "
                    "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt "
                    "--device cuda --allow-duplicate-openmp --allow-existing-output-dir"
                ),
                "protocol": {
                    "trial_name": "module2_f03_gate3_formal_train_eval",
                    "runner": "forest_n3p.scripts.run_rl_rs_gate3_trial",
                    "audit": "forest_n3p.scripts.audit_rl_rs_gate3_trial",
                    "smoke": False,
                    "formal_audit_required": True,
                    "seed": 20260704,
                    "device": "cuda",
                    "bc_checkpoint": "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt",
                    "train_curriculum_preset": "f03",
                    "eval_curriculum_preset": "f03",
                    "train_total_timesteps": 100000,
                    "eval_episodes": 64,
                    "eval_min_episodes": 64,
                    "eval_success_threshold": 0.8,
                },
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
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json",
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json",
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv",
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json",
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json",
                    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json",
                ],
            }
        ),
        encoding="utf-8",
    )
    return path
