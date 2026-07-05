import json
from importlib import import_module
from pathlib import Path


def test_protocol_lane_matrix_expands_lane_specific_evidence_without_authorizing_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_matrix")

    manifest = builder.build_manifest(_config(tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_protocol_lane_matrix"
    assert manifest["status"] == "formal_gate_protocol_lane_matrix_ready"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["runs_remote_audit"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False

    gate = manifest["gate_summary"]
    assert gate["contract_intake_status"] == "formal_gate_contract_intake_ready_for_dr_sun"
    assert gate["next_round_requirements_status"] == "formal_gate_next_round_requirements_ready"
    assert gate["current_formal_decision"] == "fail"
    assert gate["current_failure_mode"] == "threshold_failure"
    assert gate["terminal_rs_success_rate"] == 0.53125
    assert gate["required_success_threshold"] == 0.8
    assert gate["new_success_training_allowed_now"] is False
    assert gate["remote_training_allowed_now"] is False
    assert gate["local_training_allowed_now"] is False
    assert gate["formal_claim_allowed_now"] is False
    assert gate["paper_result_material_allowed_now"] is False

    lanes = {row["lane_id"]: row for row in manifest["protocol_lane_evidence_matrix"]}
    assert manifest["lane_count"] == 4
    assert set(lanes) == {
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    }
    assert lanes["stronger_obstacle_summary_warm_start"]["status"] == "candidate_requires_dr_sun_decision_and_contract"
    assert lanes["stronger_obstacle_summary_warm_start"]["training_allowed_now"] is False
    assert "the failed warm-start checkpoint" in lanes["stronger_obstacle_summary_warm_start"]["invalid_substitutes"]
    assert "warm-start dataset source and acceptance checks" in lanes["stronger_obstacle_summary_warm_start"]["required_contract_deltas"]
    assert "observation tensor definition" in lanes["full_patch_cnn_policy"]["required_contract_deltas"]
    assert "timing-unchecked CNN results" in lanes["full_patch_cnn_policy"]["invalid_substitutes"]
    assert lanes["hybrid_ppo_analytic_fallback"]["claim_scope"].startswith("claim likely changes")
    assert "fallback usage metric" in lanes["hybrid_ppo_analytic_fallback"]["required_contract_deltas"]
    assert "calling hybrid success direct PPO replacement" in lanes["hybrid_ppo_analytic_fallback"]["invalid_substitutes"]
    assert lanes["stop_or_reframe_module2_claim"]["claim_scope"].startswith("no new success-attempt training")
    assert "no new training evidence required if the contract explicitly stops success attempts" in lanes["stop_or_reframe_module2_claim"]["required_training_evidence"]

    invariants = {row["invariant_id"]: row for row in manifest["cross_lane_invariants"]}
    assert set(invariants) == {
        "no_local_training",
        "contract_before_new_success_training",
        "failed_checkpoint_not_success_evidence",
        "h02_before_paper_results",
    }
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_protocol_lane_matrix_blocks_if_contract_intake_not_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_matrix")
    config = _config(tmp_path)
    intake = json.loads(config.contract_intake_path.read_text(encoding="utf-8"))
    intake["status"] = "formal_gate_contract_intake_blocked"
    config.contract_intake_path.write_text(json.dumps(intake), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_protocol_lane_matrix_blocked"
    assert "contract_intake_not_ready" in issue_ids


def test_protocol_lane_matrix_blocks_training_permissions(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_matrix")
    config = _config(tmp_path)
    intake = json.loads(config.contract_intake_path.read_text(encoding="utf-8"))
    intake["current_gate"]["new_success_training_allowed_now"] = True
    intake["remote_training_allowed_now"] = True
    intake["current_gate"]["local_training_allowed_now"] = True
    intake["current_gate"]["formal_claim_allowed_now"] = True
    config.contract_intake_path.write_text(json.dumps(intake), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "formal_gate_protocol_lane_matrix_blocked"
    assert "training_allowed_before_lane_decision" in issue_ids
    assert "local_training_allowed" in issue_ids
    assert "claim_or_paper_result_allowed" in issue_ids


def test_protocol_lane_matrix_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_matrix")
    config = _config(tmp_path)
    manifest_path = tmp_path / "lane_matrix.json"
    markdown_path = tmp_path / "lane_matrix.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract-intake",
            str(config.contract_intake_path),
            "--next-round-requirements",
            str(config.next_round_requirements_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_protocol_lane_matrix_ready"
    assert "Module2 Formal Gate Protocol Lane Matrix" in markdown
    assert "not paper result material" in markdown
    assert "stronger_obstacle_summary_warm_start" in markdown
    assert "full_patch_cnn_policy" in markdown
    assert "hybrid_ppo_analytic_fallback" in markdown
    assert "stop_or_reframe_module2_claim" in markdown
    assert "contract_before_new_success_training" in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_matrix")
    return builder.FormalGateProtocolLaneMatrixConfig(
        output_dir=tmp_path,
        contract_intake_path=_write_json(tmp_path / "contract_intake.json", _contract_intake()),
        next_round_requirements_path=_write_json(tmp_path / "next_round.json", _next_round()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _contract_intake():
    return {
        "status": "formal_gate_contract_intake_ready_for_dr_sun",
        "audit_issue_count": 0,
        "remote_training_allowed_now": False,
        "paper_result_material_allowed": False,
        "current_failed_run": {
            "formal_decision": "fail",
            "failure_mode": "threshold_failure",
            "terminal_rs_success_rate": 0.53125,
            "required_success_threshold": 0.8,
            "threshold_deficit": 0.26875,
        },
        "current_gate": {
            "new_success_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "new_or_revised_contract_required_before_new_success_training": True,
        },
        "candidate_protocol_lanes": [
            {
                "lane_id": "stronger_obstacle_summary_warm_start",
                "status": "candidate_requires_contract",
                "what_changes": "keep compact obstacle-summary policy family but strengthen warm-start dataset",
                "must_justify": ["why the 0.53125 formal success rate is expected to improve"],
            },
            {
                "lane_id": "full_patch_cnn_policy",
                "status": "candidate_requires_contract",
                "what_changes": "move from compact summary features toward a spatial patch/CNN observation policy",
                "must_justify": ["why spatial structure is necessary"],
            },
            {
                "lane_id": "hybrid_ppo_analytic_fallback",
                "status": "candidate_requires_contract",
                "what_changes": "treat PPO as a learned selector or recovery layer",
                "must_justify": ["whether the claim changes from replacement to hybrid assistance"],
            },
            {
                "lane_id": "stop_or_reframe_module2_claim",
                "status": "candidate_requires_contract",
                "what_changes": "record the formal failure and stop pursuing PPO replacement",
                "must_justify": ["which negative evidence is sufficient to stop"],
            },
        ],
    }


def _next_round():
    return {
        "status": "formal_gate_next_round_requirements_ready",
        "audit_issue_count": 0,
        "permissions_now": {
            "new_success_training_allowed_now": False,
            "local_training_allowed_now": False,
            "formal_claim_allowed_now": False,
        },
    }
