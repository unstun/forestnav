import csv
import hashlib
import json
import zipfile
from importlib import import_module
from pathlib import Path


def test_formal_gate_proof_audit_blocks_missing_current_deliverables(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate proof audit builder: {exc}") from exc

    remaining_path = _write_json(tmp_path / "remaining_deliverables.json", _remaining_deliverables(tmp_path))

    manifest = builder.build_manifest(
        builder.FormalGateProofAuditConfig(
            output_dir=tmp_path,
            remaining_deliverables_path=remaining_path,
            workspace_root=tmp_path,
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_proof_audit"
    assert manifest["status"] == "formal_gate_proof_audit_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["proof_command_plan_id"] == "module2_formal_gate_local_read_only_proof_commands"
    assert manifest["total_matrix_rows"] == 10
    assert manifest["total_proof_command_count"] == 20
    assert manifest["passed_proof_command_count"] == 0
    assert manifest["failed_proof_command_count"] == 0
    assert manifest["blocked_proof_command_count"] == 20
    assert manifest["proof_command_summary"] == {
        "total_matrix_rows": 10,
        "total_proof_command_count": 20,
        "passed_proof_command_count": 0,
        "failed_proof_command_count": 0,
        "blocked_proof_command_count": 20,
    }
    assert manifest["formal_gate_missing_evidence_summary"]["training"] == {
        "missing_artifact_ids": [
            "train_final_model_zip",
            "train_summary_json",
            "train_training_manifest_json",
        ],
        "failed_artifact_ids": [],
    }
    assert manifest["formal_gate_missing_evidence_summary"]["evaluation"]["missing_artifact_ids"] == [
        "eval_gate3_eval_episodes_csv",
        "eval_gate3_summary_json",
    ]
    assert manifest["formal_gate_missing_evidence_summary"]["acceptance"]["missing_artifact_ids"] == [
        "gate3_trial_manifest_json",
        "gate3_formal_audit_json",
        "pulled_back_checkpoint_hash_record",
    ]
    assert manifest["current_state"]["remaining_deliverables_status"] == "formal_gate_deliverables_blocked"
    assert manifest["current_state"]["remaining_missing_deliverable_count"] == 10
    assert manifest["current_state"]["remaining_open_category_count"] == 4
    assert manifest["current_state"]["source_freshness_ready_for_remote_preflight"] is False
    assert manifest["remaining_deliverables_top_level_summary"] == {
        "present": True,
        "missing_counts_by_formal_category": {
            "training": 3,
            "evaluation": 2,
            "acceptance": 3,
            "formal_acceptance": 2,
        },
        "missing_matrix_ids_by_formal_category": {
            "training": [
                "training:train_final_model_zip",
                "training:train_summary_json",
                "training:train_training_manifest_json",
            ],
            "evaluation": [
                "evaluation:eval_gate3_eval_episodes_csv",
                "evaluation:eval_gate3_summary_json",
            ],
            "acceptance": [
                "acceptance:gate3_trial_manifest_json",
                "acceptance:gate3_formal_audit_json",
                "acceptance:pulled_back_checkpoint_hash_record",
            ],
            "formal_acceptance": [
                "formal_acceptance:h01_ready_for_formal_run",
                "formal_acceptance:h02_formal_output_acceptance",
            ],
        },
        "next_blocked_lane": "decision",
        "h01_status": "blocked_pending_decisions",
        "h02_status": "blocked_formal_output_acceptance",
        "h02_formal_output_accepted": False,
        "h02_paper_result_input_allowed": False,
    }
    assert manifest["category_status_counts"]["training"] == {
        "passed": 0,
        "failed": 0,
        "blocked_missing_artifact": 6,
    }
    assert manifest["category_status_counts"]["formal_acceptance"]["blocked_missing_artifact"] == 4
    result = manifest["proof_command_results_by_id"]["train_final_model_zip_valid_zip"]
    assert result["status"] == "blocked_missing_artifact"
    assert result["matrix_id"] == "training:train_final_model_zip"
    assert result["expected_path"].endswith("train/final_model.zip")
    assert result["command_was_executed"] is False
    assert "expected artifact is missing" in result["diagnostic"]
    assert "missing_formal_training_artifacts" in manifest["blockers"]


def test_formal_gate_proof_audit_accepts_synthetic_complete_pullback(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_audit")
    _write_complete_pullback(tmp_path)
    remaining_path = _write_json(tmp_path / "remaining_deliverables.json", _remaining_deliverables(tmp_path))

    manifest = builder.build_manifest(
        builder.FormalGateProofAuditConfig(
            output_dir=tmp_path,
            remaining_deliverables_path=remaining_path,
            workspace_root=tmp_path,
        )
    )

    assert manifest["status"] == "formal_gate_proof_audit_passed"
    assert manifest["remaining_deliverables_top_level_summary"]["missing_counts_by_formal_category"] == {
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 2,
    }
    assert manifest["total_matrix_rows"] == 10
    assert manifest["total_proof_command_count"] == 20
    assert manifest["passed_proof_command_count"] == 20
    assert manifest["blocked_proof_command_count"] == 0
    assert manifest["failed_proof_command_count"] == 0
    assert manifest["blockers"] == []
    assert all(
        not item["missing_artifact_ids"] and not item["failed_artifact_ids"]
        for item in manifest["formal_gate_missing_evidence_summary"].values()
    )
    assert manifest["proof_command_results_by_id"]["train_final_model_zip_valid_zip"]["status"] == "passed"
    assert manifest["proof_command_results_by_id"]["eval_gate3_eval_episodes_csv_schema"]["status"] == "passed"
    assert (
        manifest["proof_command_results_by_id"]["pulled_back_checkpoint_hash_record_matches_model"]["status"]
        == "passed"
    )
    assert manifest["proof_command_results_by_id"]["h02_formal_output_acceptance_status"]["status"] == "passed"


def test_formal_gate_proof_audit_catches_metadata_failures_without_running_commands(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_audit")
    _write_complete_pullback(tmp_path)
    summary_path = tmp_path / "train" / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["config"]["smoke"] = True
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    remaining_path = _write_json(tmp_path / "remaining_deliverables.json", _remaining_deliverables(tmp_path))

    manifest = builder.build_manifest(
        builder.FormalGateProofAuditConfig(
            output_dir=tmp_path,
            remaining_deliverables_path=remaining_path,
            workspace_root=tmp_path,
        )
    )

    result = manifest["proof_command_results_by_id"]["train_summary_json_formal_warm_start_metadata"]
    assert manifest["status"] == "formal_gate_proof_audit_blocked"
    assert result["status"] == "failed"
    assert result["command_was_executed"] is False
    assert "smoke=false" in result["expected_evidence"]
    assert "failed_formal_training_artifacts" in manifest["blockers"]


def test_formal_gate_proof_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_proof_audit")
    remaining_path = _write_json(tmp_path / "remaining_deliverables.json", _remaining_deliverables(tmp_path))
    manifest_path = tmp_path / "proof_audit.json"
    markdown_path = tmp_path / "proof_audit.md"

    rc = builder.main(
        [
            "--remaining-deliverables",
            str(remaining_path),
            "--workspace-root",
            str(tmp_path),
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
    assert manifest["status"] == "formal_gate_proof_audit_blocked"
    assert "Module2 Formal Gate Proof Audit" in markdown
    assert "formal_gate_proof_audit_blocked" in markdown
    assert "train_final_model_zip_valid_zip" in markdown
    assert "blocked_missing_artifact" in markdown
    assert "command_was_executed" in markdown
    assert "Current Gate State" in markdown
    assert "Remaining Deliverables Top-Level Summary" in markdown
    assert "missing_counts_by_formal_category" in markdown
    assert "formal_acceptance_missing_matrix_ids" in markdown
    assert "Missing Evidence Summary" in markdown


def _remaining_deliverables(root: Path):
    rows = _artifact_rows(root)
    return {
        "artifact_name": "module2_formal_gate_remaining_deliverables",
        "status": "formal_gate_deliverables_blocked",
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "missing_deliverable_count": 10,
        "open_category_count": 4,
        "missing_counts_by_formal_category": {
            "training": 3,
            "evaluation": 2,
            "acceptance": 3,
            "formal_acceptance": 2,
        },
        "missing_matrix_ids_by_formal_category": {
            "training": [
                "training:train_final_model_zip",
                "training:train_summary_json",
                "training:train_training_manifest_json",
            ],
            "evaluation": [
                "evaluation:eval_gate3_eval_episodes_csv",
                "evaluation:eval_gate3_summary_json",
            ],
            "acceptance": [
                "acceptance:gate3_trial_manifest_json",
                "acceptance:gate3_formal_audit_json",
                "acceptance:pulled_back_checkpoint_hash_record",
            ],
            "formal_acceptance": [
                "formal_acceptance:h01_ready_for_formal_run",
                "formal_acceptance:h02_formal_output_acceptance",
            ],
        },
        "next_blocked_lane": "decision",
        "h01_status": "blocked_pending_decisions",
        "h02_status": "blocked_formal_output_acceptance",
        "h02_formal_output_accepted": False,
        "h02_paper_result_input_allowed": False,
        "current_gate_summary": {
            "source_freshness_ready_for_remote_preflight": False,
            "source_freshness_status": "source_freshness_risks_recorded_gate_still_blocked",
        },
        "proof_command_plan": {
            "plan_id": "module2_formal_gate_local_read_only_proof_commands",
            "execution_boundary": "local_read_only_after_formal_remote_pullback",
            "not_paper_result_material": True,
            "runs_training": False,
            "runs_remote_preflight": False,
            "total_matrix_rows": len(rows),
            "total_proof_command_count": 20,
            "rows": [
                {
                    "matrix_id": row["matrix_id"],
                    "category": row["category"],
                    "artifact_id": row["artifact_id"],
                    "expected_path": row["expected_path"],
                    "proof_command_count": len(row["proof_commands"]),
                    "proof_command_ids": [command["command_id"] for command in row["proof_commands"]],
                }
                for row in rows
            ],
        },
        "deliverable_acceptance_matrix": rows,
    }


def _artifact_rows(root: Path):
    specs = [
        ("training", "train_final_model_zip", root / "train" / "final_model.zip"),
        ("training", "train_summary_json", root / "train" / "summary.json"),
        ("training", "train_training_manifest_json", root / "train" / "training_manifest.json"),
        ("evaluation", "eval_gate3_eval_episodes_csv", root / "eval" / "gate3_eval_episodes.csv"),
        ("evaluation", "eval_gate3_summary_json", root / "eval" / "gate3_summary.json"),
        ("acceptance", "gate3_trial_manifest_json", root / "audit" / "gate3_trial_manifest.json"),
        ("acceptance", "gate3_formal_audit_json", root / "audit" / "gate3_formal_audit.json"),
        ("acceptance", "pulled_back_checkpoint_hash_record", root / "train" / "checkpoint.sha256"),
        ("formal_acceptance", "h01_ready_for_formal_run", root / "h01.json"),
        ("formal_acceptance", "h02_formal_output_acceptance", root / "h02.json"),
    ]
    return [
        {
            "matrix_id": f"{category}:{artifact_id}",
            "category": category,
            "artifact_id": artifact_id,
            "expected_path": str(path),
            "proof_commands": _proof_commands(artifact_id),
        }
        for category, artifact_id, path in specs
    ]


def _proof_commands(artifact_id):
    command_ids = {
        "train_final_model_zip": [
            "train_final_model_zip_exists_nonempty",
            "train_final_model_zip_valid_zip",
        ],
        "train_summary_json": [
            "train_summary_json_exists_nonempty",
            "train_summary_json_formal_warm_start_metadata",
        ],
        "train_training_manifest_json": [
            "train_training_manifest_json_exists_nonempty",
            "train_training_manifest_json_provenance",
        ],
        "eval_gate3_eval_episodes_csv": [
            "eval_gate3_eval_episodes_csv_exists_nonempty",
            "eval_gate3_eval_episodes_csv_schema",
        ],
        "eval_gate3_summary_json": [
            "eval_gate3_summary_json_exists_nonempty",
            "eval_gate3_summary_json_formal_scope",
        ],
        "gate3_trial_manifest_json": [
            "gate3_trial_manifest_json_exists_nonempty",
            "gate3_trial_manifest_json_formal_warm_start_scope",
        ],
        "gate3_formal_audit_json": [
            "gate3_formal_audit_json_exists_nonempty",
            "gate3_formal_audit_json_accepts_formal_scope",
        ],
        "pulled_back_checkpoint_hash_record": [
            "pulled_back_checkpoint_hash_record_exists_nonempty",
            "pulled_back_checkpoint_hash_record_matches_model",
        ],
        "h01_ready_for_formal_run": [
            "h01_ready_for_formal_run_exists_nonempty",
            "h01_ready_for_formal_run_status",
        ],
        "h02_formal_output_acceptance": [
            "h02_formal_output_acceptance_exists_nonempty",
            "h02_formal_output_acceptance_status",
        ],
    }[artifact_id]
    return [
        {
            "command_id": command_id,
            "purpose": f"verify {command_id}",
            "command": f"local-read-only:{command_id}",
            "expected_evidence": _expected_evidence(command_id),
            "execution_boundary": "local_read_only_after_formal_remote_pullback",
        }
        for command_id in command_ids
    ]


def _expected_evidence(command_id):
    if command_id == "train_summary_json_formal_warm_start_metadata":
        return "status=complete, warm_start_status=applied_obstacle_summary_bc, curriculum=f03, smoke=false"
    return "exit_code=0"


def _write_complete_pullback(root: Path):
    (root / "train").mkdir()
    (root / "eval").mkdir()
    (root / "audit").mkdir()
    with zipfile.ZipFile(root / "train" / "final_model.zip", "w") as archive:
        archive.writestr("policy.pth", "synthetic formal checkpoint")
    (root / "train" / "summary.json").write_text(
        json.dumps(
            {
                "status": "complete",
                "warm_start_status": "applied_obstacle_summary_bc",
                "config": {"curriculum_preset": "f03", "smoke": False},
            }
        ),
        encoding="utf-8",
    )
    (root / "train" / "training_manifest.json").write_text(
        json.dumps(
            {
                "command": "python train.py --formal",
                "source_hashes": {"head": "abc123"},
                "config": {"curriculum_preset": "f03"},
            }
        ),
        encoding="utf-8",
    )
    with (root / "eval" / "gate3_eval_episodes.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["episode", "terminal_rs_success", "collision", "truncated", "nn_forward_time_s"],
        )
        writer.writeheader()
        for episode in range(64):
            writer.writerow(
                {
                    "episode": episode,
                    "terminal_rs_success": 1,
                    "collision": 0,
                    "truncated": 0,
                    "nn_forward_time_s": 0.001,
                }
            )
    (root / "eval" / "gate3_summary.json").write_text(
        json.dumps(
            {
                "gate_name": "module2_f03_gate3",
                "contract": ".pipeline/contracts/module2-ppo-funnel-expansion.md",
                "episodes": 64,
                "min_episodes": 64,
                "config": {"curriculum_preset": "f03"},
            }
        ),
        encoding="utf-8",
    )
    (root / "audit" / "gate3_trial_manifest.json").write_text(
        json.dumps(
            {
                "trial_name": "module2_f03_gate3_train_eval",
                "status": "complete",
                "smoke": False,
                "formal_gate_claim": False,
                "warm_start_status": "applied_obstacle_summary_bc",
            }
        ),
        encoding="utf-8",
    )
    (root / "audit" / "gate3_formal_audit.json").write_text(
        json.dumps(
            {
                "audit_name": "module2_f03_gate3_formal_audit",
                "formal_decision": "pass",
                "formal_claim_allowed": True,
                "formal_blockers": [],
            }
        ),
        encoding="utf-8",
    )
    digest = hashlib.sha256((root / "train" / "final_model.zip").read_bytes()).hexdigest()
    (root / "train" / "checkpoint.sha256").write_text(digest, encoding="utf-8")
    (root / "h01.json").write_text(json.dumps({"status": "ready_for_formal_run"}), encoding="utf-8")
    (root / "h02.json").write_text(
        json.dumps(
            {
                "status": "formal_output_accepted",
                "formal_output_accepted": True,
                "paper_result_input_allowed": True,
            }
        ),
        encoding="utf-8",
    )


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
