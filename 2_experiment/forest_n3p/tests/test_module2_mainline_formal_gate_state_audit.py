import json
from importlib import import_module


def test_mainline_formal_gate_state_audit_accepts_current_blocked_state(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_mainline_formal_gate_state_audit"
    assert manifest["status"] == "mainline_formal_gate_state_consistent_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["expected_next_action_id"] == "record_f02_6_decision"
    assert manifest["expected_next_action_mentioned"] is True
    assert manifest["total_missing_deliverables"] == 10
    assert manifest["mainline_missing_deliverable_mention_count"] == 0
    assert manifest["proof_summary_chain_status"] == "formal_gate_proof_summary_chain_consistent_blocked"
    assert manifest["proof_summary_handoff_single_next_action_consistency"] == {
        "row_count": 3,
        "consistent_row_count": 3,
    }
    assert manifest["audit_issue_count"] == 0
    assert manifest["deliverable_rows_by_matrix_id"]["training:train_final_model_zip"]["mentioned"] is True


def test_mainline_formal_gate_state_audit_fails_missing_deliverable_mention(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, omit_artifact_id="eval_gate3_summary_json")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_missing_deliverable_evaluation_eval_gate3_summary_json" in issue_ids


def test_mainline_formal_gate_state_audit_fails_execution_leak_in_status_report(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    status = json.loads(paths["status"].read_text(encoding="utf-8"))
    status["next_action_guard_summary"]["all_execution_disabled_now"] = False
    status["next_action_guard_summary"]["execution_leak_count"] = 1
    paths["status"].write_text(json.dumps(status), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "status_report_next_action_guard_execution_leak" in issue_ids


def test_mainline_formal_gate_state_audit_fails_current_section_allowed_token(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path, extra_current_text=" remote_training_allowed=true")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "mainline_current_section_forbidden_allowed_token_remote_training_allowed_true" in issue_ids


def test_mainline_formal_gate_state_audit_fails_handoff_single_next_action_chain_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    proof = json.loads(paths["proof"].read_text(encoding="utf-8"))
    proof["handoff_single_next_action_consistent_row_count"] = 2
    paths["proof"].write_text(json.dumps(proof), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "proof_summary_chain_handoff_single_next_action_inconsistent" in issue_ids


def test_mainline_formal_gate_state_audit_fails_proof_audit_input_safety_open(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    proof = json.loads(paths["proof"].read_text(encoding="utf-8"))
    proof["proof_audit_input_safety_issue_count"] = 1
    proof["proof_audit_blockers"] = ["proof_audit_input_safety_issues_open"]
    paths["proof"].write_text(json.dumps(proof), encoding="utf-8")

    manifest = builder.build_manifest(_config(builder, tmp_path, paths))

    assert manifest["status"] == "mainline_formal_gate_state_audit_failed"
    assert manifest["proof_summary_chain_proof_audit_input_safety_issue_count"] == 1
    assert manifest["proof_summary_chain_proof_audit_blockers"] == [
        "proof_audit_input_safety_issues_open"
    ]
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "proof_summary_chain_proof_audit_input_safety_issues_open" in issue_ids
    assert "proof_summary_chain_proof_audit_input_safety_blocker_open" in issue_ids


def test_mainline_formal_gate_state_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit")
    paths = _write_inputs(tmp_path)
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--mainline",
            str(paths["mainline"]),
            "--formal-gate-status-report",
            str(paths["status"]),
            "--proof-summary-chain-audit",
            str(paths["proof"]),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "mainline_formal_gate_state_consistent_blocked"
    assert "Module2 Mainline Formal Gate State Audit" in markdown
    assert "not a training run" in markdown
    assert "training:train_final_model_zip" in markdown
    assert "record_f02_6_decision" in markdown
    assert "proof_summary_handoff_single_next_action_consistency" in markdown


def _config(builder, tmp_path, paths):
    return builder.MainlineFormalGateStateAuditConfig(
        output_dir=tmp_path,
        mainline_path=paths["mainline"],
        formal_gate_status_report_path=paths["status"],
        proof_summary_chain_audit_path=paths["proof"],
    )


def _write_inputs(tmp_path, *, omit_artifact_id=None, extra_current_text=""):
    paths = {
        "mainline": tmp_path / "mainline.md",
        "status": tmp_path / "status.json",
        "proof": tmp_path / "proof.json",
    }
    rows = _deliverable_rows()
    artifact_ids = [row["artifact_id"] for row in rows if row["artifact_id"] != omit_artifact_id]
    current_line = (
        "- 2026-07-05: 当前 formal gate 下一步清单已同步到主任务书。"
        "唯一允许动作仍是 `record_f02_6_decision`; "
        f"缺失正式交付物: {', '.join(artifact_ids)}. "
        "当前禁止 local training、remote preflight、remote training、formal claim 和 paper-result material; "
        "`gpu3070ti-relay` 只是在 F02.6 关闭后的正式训练资源。"
        "`formal_gate_proof_summary_chain_consistent_blocked`。"
        f"{extra_current_text}"
    )
    paths["mainline"].write_text("# mainline\n\n" + current_line + "\n", encoding="utf-8")
    paths["status"].write_text(
        json.dumps(
            {
                "status": "formal_gate_status_blocked",
                "next_action_guard_summary": {
                    "present": True,
                    "status": "next_action_guard_passed",
                    "expected_next_action_id": "record_f02_6_decision",
                    "all_execution_disabled_now": True,
                    "execution_leak_count": 0,
                },
                "next_required_formal_deliverables": {
                    "present": True,
                    "status": "blocked_missing_formal_deliverables",
                    "not_paper_result_material": True,
                    "runs_training": False,
                    "runs_remote_preflight": False,
                    "total_missing_deliverables": 10,
                    "blocked_category_count": 4,
                    "rows": rows,
                },
            }
        ),
        encoding="utf-8",
    )
    paths["proof"].write_text(
        json.dumps(
            {
                "status": "formal_gate_proof_summary_chain_consistent_blocked",
                "proof_open": True,
                "audit_issue_count": 0,
                "next_action_guard_row_count": 3,
                "next_action_guard_consistent_row_count": 3,
                "next_required_deliverables_row_count": 3,
                "next_required_deliverables_consistent_row_count": 3,
                "handoff_single_next_action_row_count": 3,
                "handoff_single_next_action_consistent_row_count": 3,
                "runs_training": False,
                "runs_remote_preflight": False,
                "formal_claim_allowed": False,
            }
        ),
        encoding="utf-8",
    )
    return paths


def _deliverable_rows():
    return [
        _row("training", "train_final_model_zip"),
        _row("training", "train_summary_json"),
        _row("training", "train_training_manifest_json"),
        _row("evaluation", "eval_gate3_eval_episodes_csv"),
        _row("evaluation", "eval_gate3_summary_json"),
        _row("acceptance", "gate3_trial_manifest_json"),
        _row("acceptance", "gate3_formal_audit_json"),
        _row("acceptance", "pulled_back_checkpoint_hash_record"),
        _row("formal_acceptance", "h01_ready_for_formal_run"),
        _row("formal_acceptance", "h02_formal_output_acceptance"),
    ]


def _row(category, artifact_id):
    return {
        "matrix_id": f"{category}:{artifact_id}",
        "category": category,
        "artifact_id": artifact_id,
        "responsible_stage_id": "gate3_remote_training",
        "responsible_stage_allowed_now": False,
    }
