import json
from importlib import import_module


def test_remaining_deliverables_blocks_pending_formal_gate(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables")

    manifest = builder.build_manifest(_config(tmp_path, complete=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_remaining_deliverables"
    assert manifest["status"] == "formal_gate_deliverables_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["permissions_now"]["local_training_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["current_gate_summary"]["next_blocked_lane"] == "decision"
    assert manifest["current_gate_summary"]["h02_status"] == "blocked_formal_output_acceptance"
    assert manifest["missing_deliverable_count"] == 10
    assert manifest["open_category_count"] == 4
    assert manifest["category_counts"]["training"] == {"item_count": 3, "missing_count": 3, "present_count": 0}
    assert manifest["category_counts"]["evaluation"] == {"item_count": 2, "missing_count": 2, "present_count": 0}
    assert manifest["category_counts"]["acceptance"] == {"item_count": 3, "missing_count": 3, "present_count": 0}
    assert manifest["category_counts"]["formal_acceptance"] == {"item_count": 2, "missing_count": 2, "present_count": 0}

    groups = {group["category"]: group for group in manifest["deliverable_groups"]}
    assert groups["training"]["responsible_stage_id"] == "gate3_remote_training"
    assert groups["training"]["responsible_stage_allowed_now"] is False
    assert "remote_packet_not_ready" in groups["training"]["responsible_stage_blocked_by"]
    assert [item["artifact_id"] for item in groups["training"]["items"]] == [
        "train_final_model_zip",
        "train_summary_json",
        "train_training_manifest_json",
    ]
    assert "local training output" in groups["training"]["invalid_substitutes"]
    assert groups["evaluation"]["responsible_stage_id"] == "gate3_remote_audit_pullback"
    assert "H02 available-subset smoke CSV" in groups["evaluation"]["invalid_substitutes"]
    assert groups["acceptance"]["responsible_stage_id"] == "gate3_remote_audit_pullback"
    assert "checkpoint file without hash record" in groups["acceptance"]["invalid_substitutes"]
    assert groups["formal_acceptance"]["responsible_stage_id"] == "regenerate_h01_h02_formal_artifacts"
    assert "blocked H02 acceptance audit" in groups["formal_acceptance"]["invalid_substitutes"]
    assert manifest["audit_issue_count"] == 0


def test_remaining_deliverables_accepts_synthetic_complete_gate(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables")

    manifest = builder.build_manifest(_config(tmp_path, complete=True))

    assert manifest["status"] == "formal_gate_deliverables_ready_for_claim_audit"
    assert manifest["missing_deliverable_count"] == 0
    assert manifest["open_category_count"] == 0
    assert manifest["audit_issue_count"] == 0
    assert all(group["status"] == "complete" for group in manifest["deliverable_groups"])
    assert manifest["permissions_now"]["remote_training_allowed_now"] is True
    assert manifest["permissions_now"]["formal_claim_allowed_now"] is True


def test_remaining_deliverables_catches_unsafe_or_incomplete_inputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables")
    config = _config(tmp_path, complete=False)
    status_report = json.loads(config.status_report_path.read_text(encoding="utf-8"))
    status_report["runs_training"] = True
    status_report["training_artifacts_required"][0]["missing"] = False
    status_report["training_artifacts_required"][0]["exists"] = True
    status_report_path = config.status_report_path
    status_report_path.write_text(json.dumps(status_report), encoding="utf-8")
    missing_artifacts = json.loads(config.missing_artifacts_path.read_text(encoding="utf-8"))
    missing_artifacts["formal_claim_allowed"] = True
    for requirement in missing_artifacts["formal_gate_requirements"]:
        if requirement["phase"] == "training":
            requirement["responsible_stage_allowed_now"] = True
            requirement["invalid_substitutes"] = []
    config.missing_artifacts_path.write_text(json.dumps(missing_artifacts), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "status_report_runs_training" in issue_ids
    assert "missing_artifacts_allows_formal_claim" in issue_ids
    assert "training_allowed_while_status_report_blocked" in issue_ids
    assert "training_missing_invalid_substitutes" in issue_ids
    assert manifest["category_counts"]["training"]["present_count"] == 1
    assert manifest["category_counts"]["training"]["missing_count"] == 2


def test_remaining_deliverables_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables")
    config = _config(tmp_path, complete=False)
    manifest_path = tmp_path / "remaining.json"
    markdown_path = tmp_path / "remaining.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--status-report",
            str(config.status_report_path),
            "--missing-artifacts",
            str(config.missing_artifacts_path),
            "--closure-checklist",
            str(config.closure_checklist_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--h01-manifest",
            str(config.h01_manifest_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_deliverables_blocked"
    assert "Module2 Formal Gate Remaining Deliverables" in markdown
    assert "train_final_model_zip" in markdown
    assert "eval_gate3_eval_episodes_csv" in markdown
    assert "gate3_formal_audit_json" in markdown
    assert "h02_formal_output_acceptance" in markdown
    assert "invalid_substitutes" in markdown


def _config(tmp_path, *, complete):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables")
    return builder.FormalGateRemainingDeliverablesConfig(
        output_dir=tmp_path,
        status_report_path=_write_json(tmp_path / "status_report.json", _status_report(complete=complete)),
        missing_artifacts_path=_write_json(tmp_path / "missing_artifacts.json", _missing_artifacts(complete=complete)),
        closure_checklist_path=_write_json(tmp_path / "closure_checklist.json", _closure_checklist(complete=complete)),
        remote_packet_path=_write_json(tmp_path / "remote_packet.json", _remote_packet(complete=complete)),
        h01_manifest_path=_write_json(tmp_path / "h01.json", _h01(complete=complete)),
        h02_acceptance_path=_write_json(tmp_path / "h02.json", _h02(complete=complete)),
    )


def _status_report(*, complete):
    status = "present" if complete else "missing"
    return {
        "status": "formal_gate_status_ready_for_claim_audit" if complete else "formal_gate_status_blocked",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "permissions_now": {
            "remote_preflight_allowed_now": complete,
            "remote_training_allowed_now": complete,
            "formal_h01_evaluation_allowed_now": complete,
            "formal_h02_acceptance_allowed_now": complete,
            "formal_claim_allowed_now": complete,
        },
        "next_blocked_lane": None if complete else {"lane_id": "decision"},
        "missing_counts_by_category": {
            "training": 0 if complete else 3,
            "evaluation": 0 if complete else 2,
            "acceptance": 0 if complete else 3,
            "evaluation_acceptance": 0 if complete else 2,
        },
        "training_artifacts_required": [
            _artifact("train_final_model_zip", "train/final_model.zip", complete=complete, state=status),
            _artifact("train_summary_json", "train/summary.json", complete=complete, state=status),
            _artifact("train_training_manifest_json", "train/training_manifest.json", complete=complete, state=status),
        ],
        "evaluation_artifacts_required": [
            _artifact("eval_gate3_eval_episodes_csv", "eval/gate3_eval_episodes.csv", complete=complete, state=status),
            _artifact("eval_gate3_summary_json", "eval/gate3_summary.json", complete=complete, state=status),
        ],
        "acceptance_artifacts_required": [
            _artifact("gate3_trial_manifest_json", "gate3_trial_manifest.json", complete=complete, state=status),
            _artifact("gate3_formal_audit_json", "gate3_formal_audit.json", complete=complete, state=status),
            _artifact("pulled_back_checkpoint_hash_record", "train/final_model.zip.sha256", complete=complete, state=status),
        ],
        "evaluation_acceptance_required": [
            _artifact("h01_ready_for_formal_run", "module2_v1_evaluation_manifest.json", complete=complete, state="ready_for_formal_run" if complete else "blocked_pending_decisions"),
            _artifact("h02_formal_output_acceptance", "h02_formal_acceptance.json", complete=complete, state="formal_output_accepted" if complete else "blocked_formal_output_acceptance"),
        ],
    }


def _missing_artifacts(*, complete):
    return {
        "status": "formal_gate_artifacts_complete" if complete else "formal_gate_missing_artifacts_open",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "formal_gate_requirements": [
            _requirement(
                "training_remote_ppo_checkpoint",
                "training",
                stage_id="gate3_remote_training",
                complete=complete,
                invalid_substitutes=["local training output", "available-subset smoke model"],
            ),
            _requirement(
                "evaluation_gate3_episode_outputs",
                "evaluation",
                stage_id="gate3_remote_audit_pullback",
                complete=complete,
                invalid_substitutes=["H02 available-subset smoke CSV", "paper table preview"],
            ),
            _requirement(
                "acceptance_remote_pullback_and_audit",
                "acceptance",
                stage_id="gate3_remote_audit_pullback",
                complete=complete,
                invalid_substitutes=["remote command success without local pullback", "checkpoint file without hash record"],
            ),
            _requirement(
                "h01_h02_formal_evaluation_acceptance",
                "evaluation_acceptance",
                stage_id="regenerate_h01_h02_formal_artifacts",
                complete=complete,
                invalid_substitutes=["blocked H01 manifest", "blocked H02 acceptance audit"],
            ),
        ],
    }


def _closure_checklist(*, complete):
    payload = _status_report(complete=complete)
    return {
        "status": "formal_gate_closure_ready_for_result_audit" if complete else "formal_gate_closure_blocked",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "training_artifacts_required": payload["training_artifacts_required"],
        "evaluation_artifacts_required": payload["evaluation_artifacts_required"],
        "acceptance_artifacts_required": payload["acceptance_artifacts_required"],
        "evaluation_acceptance_required": payload["evaluation_acceptance_required"],
    }


def _remote_packet(*, complete):
    return {
        "status": "ready_for_remote_training_packet_execution" if complete else "blocked_until_f02_6_decision",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "ready_to_run_remote_training": complete,
    }


def _h01(*, complete):
    return {
        "status": "ready_for_formal_run" if complete else "blocked_pending_decisions",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _h02(*, complete):
    return {
        "status": "formal_output_accepted" if complete else "blocked_formal_output_acceptance",
        "formal_output_accepted": complete,
        "paper_result_input_allowed": complete,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
    }


def _artifact(artifact_id, path, *, complete, state):
    return {
        "artifact_id": artifact_id,
        "path": f"0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/{path}",
        "exists": complete,
        "state": state,
        "missing": not complete,
        "reason": "" if complete else f"{artifact_id} missing",
    }


def _requirement(requirement_id, phase, *, stage_id, complete, invalid_substitutes):
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": "satisfied" if complete else "blocked_missing_outputs",
        "responsible_stage_id": stage_id,
        "responsible_stage_status": "ready" if complete else "blocked",
        "responsible_stage_allowed_now": complete,
        "responsible_stage_blocked_by": [] if complete else ["remote_packet_not_ready"],
        "acceptable_evidence": [f"{requirement_id}_acceptable_evidence"],
        "invalid_substitutes": invalid_substitutes,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
