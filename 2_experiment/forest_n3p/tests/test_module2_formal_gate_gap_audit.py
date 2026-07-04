import json
from importlib import import_module


def test_formal_gate_gap_audit_blocks_current_pending_gate_and_lists_missing_artifacts(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate gap audit builder: {exc}") from exc

    manifest_path = tmp_path / "formal_gate_gap_audit.json"
    markdown_path = tmp_path / "formal_gate_gap_audit.md"
    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract",
            str(_contract(tmp_path)),
            "--decision-record",
            str(_decision_record(tmp_path, pending=True)),
            "--h01-manifest",
            str(_h01_manifest(tmp_path, ready=False)),
            "--remote-packet",
            str(_remote_packet(tmp_path, ready=False, artifacts_present=False)),
            "--h02-acceptance",
            str(_h02_acceptance(tmp_path, accepted=False)),
            "--claim-safety",
            str(_claim_safety(tmp_path, allowed=False)),
            "--readiness",
            str(_readiness(tmp_path, ready=False)),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_gap_audit"
    assert manifest["status"] == "blocked_formal_gate_gaps_open"
    assert manifest["not_paper_result_material"] is True
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"
    assert manifest["current_gate_state"]["formal_performance_claim_allowed"] is False

    gap_ids = {
        gap["gap_id"]
        for key in (
            "missing_decision_items",
            "missing_training_artifacts",
            "missing_evaluation_artifacts",
            "missing_acceptance_artifacts",
        )
        for gap in manifest[key]
    }
    assert "f02_6_warm_start_decision_pending" in gap_ids
    assert "remote_training_packet_not_ready" in gap_ids
    assert "missing_remote_pullback_artifact" in gap_ids
    assert "missing_ppo_result_rows" in gap_ids
    assert "missing_ppo_checkpoint_hash" in gap_ids
    assert "h01_manifest_not_ready" in gap_ids
    assert "h02_verdict_not_formal" in gap_ids
    assert "h02_formal_output_not_accepted" in gap_ids
    assert "claim_safety_blocks_formal_performance" in gap_ids
    assert "readiness_blocks_formal_results" in gap_ids
    assert "Formal Gate Gap Audit" in markdown
    assert "not a paper result" in markdown
    assert "runs_training=`True`, host=`gpu3070ti-relay`" in markdown


def test_formal_gate_gap_audit_can_be_clean_only_after_remote_artifacts_and_acceptance(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    remote_packet = _remote_packet(tmp_path, ready=True, artifacts_present=True)
    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=remote_packet,
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
        )
    )

    assert manifest["status"] == "formal_gate_ready_for_result_audit"
    assert manifest["local_training_allowed"] is False
    assert manifest["missing_decision_items"] == []
    assert manifest["missing_training_artifacts"] == []
    assert manifest["missing_evaluation_artifacts"] == []
    assert manifest["missing_acceptance_artifacts"] == []
    assert manifest["ordered_next_steps"][-1]["status"] == "ready"


def test_formal_gate_gap_audit_does_not_treat_expected_training_outputs_as_training_preconditions(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=False),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=False),
            claim_safety_path=_claim_safety(tmp_path, allowed=False),
            readiness_path=_readiness(tmp_path, ready=False),
        )
    )

    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["remote_preflight"]["status"] == "pending_execution"
    assert steps["gate3_remote_training"]["status"] == "pending_execution"
    assert steps["gate3_remote_training"]["blocked_by"] == []
    assert steps["gate3_remote_audit_pullback"]["status"] == "blocked"
    assert "missing_remote_pullback_artifact" in steps["gate3_remote_audit_pullback"]["blocked_by"]
    assert steps["h01_h02_regeneration"]["status"] == "blocked"
    assert "missing_ppo_result_rows" in steps["h01_h02_regeneration"]["blocked_by"]
    assert steps["claim_safety_final_gate"]["status"] == "blocked"


def test_formal_gate_gap_audit_does_not_allow_local_training_even_when_remote_is_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
        )
    )

    assert manifest["local_training_allowed"] is False
    assert "No PPO/RL-RS formal training is allowed on the local Mac." in manifest["claim_boundaries"]


def _contract(tmp_path):
    path = tmp_path / "contract.md"
    path.write_text(
        "\n".join(
            [
                "---",
                "status: approved",
                "version: v1",
                "approved_by: Dr Sun",
                "approved_date: 2026-07-02",
                "---",
                "",
                "# Contract",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _decision_record(tmp_path, *, pending):
    path = tmp_path / f"decision_{pending}.json"
    path.write_text(
        json.dumps(
            {
                "status": "pending_human_decision" if pending else "approved",
                "effective_warm_start_decision": "pending" if pending else "approved_obstacle_summary",
                "remote_training_allowed": not pending,
                "local_training_allowed": False,
                "blockers": ["requires_dr_sun_approval"] if pending else [],
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
                "run_command": {
                    "formal_main_evaluation": "python -m forest_n3p.scripts.run_main_evaluation --methods ha_rl_rs_ppo"
                    if ready
                    else None
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _remote_packet(tmp_path, *, ready, artifacts_present):
    artifact_dir = tmp_path / f"remote_artifacts_{ready}_{artifacts_present}"
    expected = [
        artifact_dir / "train" / "final_model.zip",
        artifact_dir / "train" / "summary.json",
        artifact_dir / "train" / "training_manifest.json",
        artifact_dir / "eval" / "gate3_eval_episodes.csv",
        artifact_dir / "eval" / "gate3_summary.json",
        artifact_dir / "gate3_trial_manifest.json",
        artifact_dir / "gate3_formal_audit.json",
    ]
    if artifacts_present:
        for path in expected:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ok\n", encoding="utf-8")
    path = tmp_path / f"remote_packet_{ready}_{artifacts_present}.json"
    path.write_text(
        json.dumps(
            {
                "status": "ready_for_gpu3070ti_remote_training" if ready else "blocked_until_f02_6_decision",
                "ready_to_run_remote_training": ready,
                "local_training_allowed": False,
                "blockers": [] if ready else ["requires_dr_sun_approval", "f02_6_warm_start_decision_pending"],
                "execution_environment": {
                    "gpu_alias": "gpu3070ti-relay",
                    "training_host_required": "gpu3070ti-relay",
                },
                "post_run_pullback": {
                    "required_before_local_claim": True,
                    "expected_artifacts": [str(item) for item in expected],
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _h02_acceptance(tmp_path, *, accepted):
    path = tmp_path / f"h02_{accepted}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_output_accepted" if accepted else "blocked_formal_output_acceptance",
                "formal_output_accepted": accepted,
                "paper_result_input_allowed": accepted,
                "formal_checks": {
                    "h02_verdict_status": "formal_accepted" if accepted else "candidate_or_smoke",
                    "h02_verdict_formal_acceptance": accepted,
                    "gate3_audit_path": str(tmp_path / "gate3_formal_audit.json"),
                    "gate3_formal_audit_passed": accepted,
                    "scale_checks": {
                        "queries_per_bucket": {"observed": 100, "required": 100, "satisfied": accepted},
                        "seed_count": {"observed": 5, "required": 5, "satisfied": accepted},
                        "queries_per_map": {"observed": 5, "required": 5, "satisfied": accepted},
                    },
                },
                "method_checks": {
                    "ppo_row_count": 2 if accepted else 0,
                    "has_ppo_result_rows": accepted,
                    "ppo_checkpoint_hashes": ["abc123"] if accepted else [],
                    "ppo_rows_have_checkpoint_hash": accepted,
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _claim_safety(tmp_path, *, allowed):
    path = tmp_path / f"claim_safety_{allowed}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_performance_claims_allowed" if allowed else "blocked_formal_performance_claims",
                "formal_performance_claim_allowed": allowed,
            }
        ),
        encoding="utf-8",
    )
    return path


def _readiness(tmp_path, *, ready):
    path = tmp_path / f"readiness_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_results_ready" if ready else "partial_methods_ready_results_blocked",
                "formal_results_ready": ready,
            }
        ),
        encoding="utf-8",
    )
    return path
