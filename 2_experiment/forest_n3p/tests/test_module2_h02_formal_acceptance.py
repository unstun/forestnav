import csv
import json
from importlib import import_module


REQUIRED_RECORD_COLUMNS = [
    "query_id",
    "method",
    "difficulty_bucket",
    "success",
    "feasible",
    "total_time_s",
    "total_expansions",
    "analytic_attempts",
    "analytic_successes",
    "rl_attempts",
    "rl_successes",
    "rs_attempts",
    "nn_forward_time_s",
    "fallback_to_primitives_count",
    "rollout_protocol",
    "collision_checker",
    "rl_rs_checkpoint",
    "rl_rs_checkpoint_sha256",
    "failure_reason",
]
REQUIRED_SUMMARY_COLUMNS = [
    "method",
    "difficulty_bucket",
    "count",
    "success_rate",
    "timeout_failure_rate",
    "mean_nn_forward_time_s",
    "p95_nn_forward_time_s",
    "rl_attempts_total",
    "rl_successes_total",
    "rs_attempts_total",
    "fallback_to_primitives_total",
]
REQUIRED_SUMMARY_SECTIONS = [
    "record_count",
    "summary_by_method_bucket",
    "paired_time_tests",
    "paired_expansion_tests",
    "timeout_failure_rate_bootstrap_ci",
]


def test_h02_formal_acceptance_blocks_current_smoke_and_pending_remote_packet(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_h02_formal_acceptance")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing H02 formal acceptance builder: {exc}") from exc

    evaluation_dir = _evaluation_dir(tmp_path, formal=False)
    manifest_path = tmp_path / "h02_acceptance.json"
    markdown_path = tmp_path / "h02_acceptance.md"
    rc = builder.main(
        [
            "--evaluation-dir",
            str(evaluation_dir),
            "--h01-manifest",
            str(_h01_manifest(tmp_path, ready=False)),
            "--remote-execution-packet",
            str(_remote_packet(tmp_path, ready=False, artifact_dir=evaluation_dir)),
            "--gate3-audit",
            str(tmp_path / "missing_gate3_formal_audit.json"),
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
    assert manifest["artifact_name"] == "module2_h02_formal_acceptance"
    assert manifest["status"] == "blocked_formal_output_acceptance"
    assert manifest["formal_output_accepted"] is False
    assert manifest["paper_result_input_allowed"] is False
    assert "h02_verdict_not_formal" in manifest["blockers"]
    assert "h01_manifest_not_ready" in manifest["blockers"]
    assert "remote_execution_packet_not_ready" in manifest["blockers"]
    assert "missing_gate3_formal_audit" in manifest["blockers"]
    assert "h02_scale_below_h01_manifest" in manifest["blockers"]
    assert "missing_ppo_result_rows" in manifest["blockers"]
    assert manifest["schema_checks"]["records_csv"]["missing_columns"] == []
    assert manifest["schema_checks"]["summary_by_method_bucket_csv"]["missing_columns"] == []
    assert manifest["schema_checks"]["summary_json"]["missing_sections"] == []
    assert manifest["formal_acceptance_requirement_counts"] == {
        "satisfied": 1,
        "blocked_formal_acceptance": 3,
    }
    requirements = {item["requirement_id"]: item for item in manifest["formal_acceptance_requirements"]}
    assert requirements["h01_schema_and_h02_output_schema_match"]["status"] == "satisfied"
    assert requirements["h01_schema_and_h02_output_schema_match"]["paper_result_input_allowed_now"] is False
    assert requirements["h02_formal_scope_and_scale_match_h01"]["status"] == "blocked_formal_acceptance"
    assert "candidate_or_smoke verdict" in requirements["h02_formal_scope_and_scale_match_h01"]["invalid_substitutes"]
    assert requirements["gate3_audit_and_pullback_acceptance"]["status"] == "blocked_formal_acceptance"
    assert "remote stdout without local pullback" in requirements["gate3_audit_and_pullback_acceptance"]["invalid_substitutes"]
    assert requirements["ppo_rows_and_checkpoint_hash_present"]["status"] == "blocked_formal_acceptance"
    assert "BC analytic rows used as PPO result rows" in requirements["ppo_rows_and_checkpoint_hash_present"]["invalid_substitutes"]
    assert "blocked_formal_output_acceptance" in markdown
    assert "Formal Acceptance Requirements" in markdown


def test_h02_formal_acceptance_accepts_synthetic_formal_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_h02_formal_acceptance")
    evaluation_dir = _evaluation_dir(tmp_path, formal=True)
    remote_packet = _remote_packet(tmp_path, ready=True, artifact_dir=evaluation_dir)
    gate3_audit = _gate3_audit(tmp_path, pass_audit=True)

    manifest = builder.build_manifest(
        builder.H02FormalAcceptanceConfig(
            output_dir=tmp_path,
            evaluation_dir=evaluation_dir,
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_execution_packet_path=remote_packet,
            gate3_audit_path=gate3_audit,
        )
    )

    assert manifest["status"] == "formal_output_accepted"
    assert manifest["formal_output_accepted"] is True
    assert manifest["paper_result_input_allowed"] is True
    assert manifest["blockers"] == []
    assert manifest["formal_checks"]["h02_verdict_formal_acceptance"] is True
    assert manifest["formal_checks"]["gate3_formal_audit_passed"] is True
    assert manifest["formal_checks"]["remote_pullback_artifacts_present"] is True
    assert manifest["method_checks"]["has_ppo_result_rows"] is True
    assert manifest["method_checks"]["ppo_checkpoint_hashes"] == ["abc123"]
    assert manifest["formal_acceptance_requirement_counts"] == {"satisfied": 4}
    assert all(item["status"] == "satisfied" for item in manifest["formal_acceptance_requirements"])
    assert all(item["paper_result_input_allowed_now"] is True for item in manifest["formal_acceptance_requirements"])


def test_h02_formal_acceptance_blocks_missing_required_schema(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_h02_formal_acceptance")
    evaluation_dir = _evaluation_dir(tmp_path, formal=True, omit_record_column="nn_forward_time_s")

    manifest = builder.build_manifest(
        builder.H02FormalAcceptanceConfig(
            output_dir=tmp_path,
            evaluation_dir=evaluation_dir,
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_execution_packet_path=_remote_packet(tmp_path, ready=True, artifact_dir=evaluation_dir),
            gate3_audit_path=_gate3_audit(tmp_path, pass_audit=True),
        )
    )

    assert manifest["status"] == "blocked_formal_output_acceptance"
    assert "records_csv_missing_required_columns" in manifest["blockers"]
    assert manifest["schema_checks"]["records_csv"]["missing_columns"] == ["nn_forward_time_s"]
    requirements = {item["requirement_id"]: item for item in manifest["formal_acceptance_requirements"]}
    assert requirements["h01_schema_and_h02_output_schema_match"]["status"] == "blocked_formal_acceptance"
    assert "records_csv_column_nn_forward_time_s" in requirements["h01_schema_and_h02_output_schema_match"]["missing_artifact_ids"]


def _evaluation_dir(tmp_path, *, formal, omit_record_column=None):
    path = tmp_path / ("formal_eval" if formal else "smoke_eval")
    path.mkdir()
    columns = [col for col in REQUIRED_RECORD_COLUMNS if col != omit_record_column]
    rows = [
        {
            "query_id": "q0",
            "method": "ha_dang_multi_rs",
            "difficulty_bucket": "Easy",
            "success": "True",
            "feasible": "True",
            "total_time_s": "1.0",
            "total_expansions": "10",
            "analytic_attempts": "10",
            "analytic_successes": "1",
            "rl_attempts": "",
            "rl_successes": "",
            "rs_attempts": "10",
            "nn_forward_time_s": "",
            "fallback_to_primitives_count": "9",
            "rollout_protocol": "",
            "collision_checker": "",
            "rl_rs_checkpoint": "",
            "rl_rs_checkpoint_sha256": "",
            "failure_reason": "",
        },
        {
            "query_id": "q0",
            "method": "ha_rl_rs_ppo" if formal else "bc_analytic_operator",
            "difficulty_bucket": "Easy",
            "success": "True",
            "feasible": "True",
            "total_time_s": "0.5",
            "total_expansions": "5",
            "analytic_attempts": "5",
            "analytic_successes": "1",
            "rl_attempts": "5",
            "rl_successes": "1",
            "rs_attempts": "5",
            "nn_forward_time_s": "0.01",
            "fallback_to_primitives_count": "4",
            "rollout_protocol": "ppo_f03",
            "collision_checker": "grid_segment_sample_v1",
            "rl_rs_checkpoint": "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip",
            "rl_rs_checkpoint_sha256": "abc123" if formal else "",
            "failure_reason": "",
        },
    ]
    with (path / "records.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row[col] for col in columns})
    with (path / "summary_by_method_bucket.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerow(
            {
                "method": "ha_rl_rs_ppo" if formal else "bc_analytic_operator",
                "difficulty_bucket": "Easy",
                "count": "1",
                "success_rate": "1.0",
                "timeout_failure_rate": "0.0",
                "mean_nn_forward_time_s": "0.01",
                "p95_nn_forward_time_s": "0.01",
                "rl_attempts_total": "5",
                "rl_successes_total": "1",
                "rs_attempts_total": "5",
                "fallback_to_primitives_total": "4",
            }
        )
    (path / "summary.json").write_text(
        json.dumps(
            {
                "record_count": len(rows),
                "summary_by_method_bucket": [],
                "paired_time_tests": [],
                "paired_expansion_tests": [],
                "success_rate_bootstrap_ci": [],
                "failure_rate_bootstrap_ci": [],
                "timeout_failure_rate_bootstrap_ci": [],
            }
        ),
        encoding="utf-8",
    )
    (path / "verdict.json").write_text(
        json.dumps(
            {
                "status": "formal_accepted" if formal else "candidate_or_smoke",
                "formal_acceptance": formal,
                "record_count": len(rows),
            }
        ),
        encoding="utf-8",
    )
    (path / "run_config.json").write_text(
        json.dumps(
            {
                "config": {
                    "queries_per_bucket": 100 if formal else 1,
                    "seed_count": 5 if formal else 1,
                    "queries_per_map": 5 if formal else 1,
                    "methods": ["ha_dang_multi_rs", "ha_rl_rs_ppo" if formal else "bc_analytic_operator"],
                    "module2_rl_rs_checkpoint": "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip"
                    if formal
                    else None,
                }
            }
        ),
        encoding="utf-8",
    )
    return path


def _h01_manifest(tmp_path, *, ready):
    path = tmp_path / f"h01_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "status": "ready_for_formal_run" if ready else "blocked_pending_decisions",
                "blockers": [] if ready else ["f02_6_warm_start_decision_pending", "missing_module2_rl_rs_checkpoint"],
                "scale": {"queries_per_bucket": 100, "seed_count": 5, "queries_per_map": 5},
                "required_output_schema": {
                    "schema_status": "frozen_for_module2_v1",
                    "records_csv_required_columns": REQUIRED_RECORD_COLUMNS,
                    "summary_by_method_bucket_required_columns": REQUIRED_SUMMARY_COLUMNS,
                    "summary_json_required_sections": REQUIRED_SUMMARY_SECTIONS,
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _remote_packet(tmp_path, *, ready, artifact_dir):
    artifact_dir = artifact_dir.resolve()
    for rel in [
        "train/final_model.zip",
        "train/summary.json",
        "train/training_manifest.json",
        "eval/gate3_eval_episodes.csv",
        "eval/gate3_summary.json",
        "gate3_trial_manifest.json",
        "gate3_formal_audit.json",
    ]:
        target = artifact_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("stub", encoding="utf-8")
    path = tmp_path / f"remote_packet_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "status": "ready_for_gpu3070ti_remote_training" if ready else "blocked_until_f02_6_decision",
                "ready_to_run_remote_training": ready,
                "local_training_allowed": False,
                "blockers": [] if ready else ["requires_dr_sun_approval"],
                "post_run_pullback": {
                    "required_before_local_claim": True,
                    "expected_artifacts": [str(artifact_dir / rel) for rel in [
                        "train/final_model.zip",
                        "train/summary.json",
                        "train/training_manifest.json",
                        "eval/gate3_eval_episodes.csv",
                        "eval/gate3_summary.json",
                        "gate3_trial_manifest.json",
                        "gate3_formal_audit.json",
                    ]],
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _gate3_audit(tmp_path, *, pass_audit):
    path = tmp_path / f"gate3_audit_{pass_audit}.json"
    path.write_text(
        json.dumps(
            {
                "formal_decision": "pass" if pass_audit else "fail",
                "formal_claim_allowed": pass_audit,
                "formal_blockers": [] if pass_audit else ["success_rate_below_threshold"],
                "warm_start_decision": "approved_obstacle_summary",
            }
        ),
        encoding="utf-8",
    )
    return path
