import json
from importlib import import_module
from pathlib import Path


def test_protocol_lane_readiness_packet_prepares_decision_without_authorizing_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_readiness")

    manifest = builder.build_manifest(_config(tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_protocol_lane_readiness"
    assert manifest["status"] == "protocol_lane_readiness_ready_for_dr_sun_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["runs_remote_audit"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False

    gate = manifest["gate_state"]
    assert gate["next_blocked_lane"] == "protocol_lane_decision"
    assert gate["decision_owner_required"] == "Dr Sun"
    assert gate["selected_lane_id"] is None
    assert gate["next_action_ids"] == ["record_protocol_lane_decision"]
    assert gate["current_formal_decision"] == "fail"
    assert gate["current_failure_mode"] == "threshold_failure"
    assert gate["terminal_rs_success_rate"] == 0.53125
    assert gate["required_success_threshold"] == 0.8
    assert gate["agent_may_record_decision_now"] is False
    assert gate["remote_training_authorized_by_this_packet"] is False

    lanes = {row["lane_id"]: row for row in manifest["lane_readiness_rows"]}
    assert manifest["lane_count"] == 4
    assert set(lanes) == {
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    }
    assert lanes["stronger_obstacle_summary_warm_start"]["can_start_remote_training_now"] is False
    assert lanes["stronger_obstacle_summary_warm_start"]["agent_may_select_lane_now"] is False
    assert lanes["stronger_obstacle_summary_warm_start"]["new_success_training_required_if_selected"] is True
    assert "train_final_model_zip" in lanes["stronger_obstacle_summary_warm_start"]["shared_next_success_artifact_ids"]
    assert "warm-start dataset source and acceptance checks" in lanes["stronger_obstacle_summary_warm_start"]["required_contract_deltas"]
    assert "observation tensor definition" in lanes["full_patch_cnn_policy"]["required_contract_deltas"]
    assert "fallback usage metric" in lanes["hybrid_ppo_analytic_fallback"]["required_contract_deltas"]
    assert lanes["stop_or_reframe_module2_claim"]["new_success_training_required_if_selected"] is False
    assert lanes["stop_or_reframe_module2_claim"]["shared_next_success_artifact_ids"] == []
    assert "writing a positive replacement claim from failed evidence" in lanes["stop_or_reframe_module2_claim"]["invalid_substitutes"]

    assert manifest["shared_next_success_attempt_artifact_count"] == 10
    artifact_ids = {row["artifact_id"] for row in manifest["shared_next_success_attempt_artifacts"]}
    assert "new_or_revised_research_contract" in artifact_ids
    assert "gate3_formal_audit_json" in artifact_ids
    assert "h02_formal_output_acceptance" in artifact_ids
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_protocol_lane_readiness_catches_training_permission_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_readiness")
    config = _config(tmp_path)
    status = json.loads(config.protocol_status_path.read_text(encoding="utf-8"))
    status["current_status"]["remote_training_allowed_now"] = True
    config.protocol_status_path.write_text(json.dumps(status), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "protocol_lane_readiness_audit_failed"
    assert "remote_training_allowed_now_unexpectedly_true" in issue_ids


def test_protocol_lane_readiness_catches_incomplete_lane_evidence(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_readiness")
    config = _config(tmp_path)
    matrix = json.loads(config.lane_matrix_path.read_text(encoding="utf-8"))
    matrix["protocol_lane_evidence_matrix"][0]["invalid_substitutes"] = []
    config.lane_matrix_path.write_text(json.dumps(matrix), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "protocol_lane_readiness_audit_failed"
    assert "stronger_obstacle_summary_warm_start_missing_invalid_substitutes" in issue_ids


def test_protocol_lane_readiness_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_readiness")
    config = _config(tmp_path)
    manifest_path = tmp_path / "readiness.json"
    markdown_path = tmp_path / "readiness.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--protocol-status",
            str(config.protocol_status_path),
            "--decision-packet",
            str(config.decision_packet_path),
            "--decision-record",
            str(config.decision_record_path),
            "--lane-matrix",
            str(config.lane_matrix_path),
            "--next-round-requirements",
            str(config.next_round_requirements_path),
            "--remaining-deliverables",
            str(config.remaining_deliverables_path),
            "--remote-packet-safety",
            str(config.remote_packet_safety_path),
            "--claim-safety",
            str(config.claim_safety_path),
            "--paper-readiness",
            str(config.paper_readiness_path),
            "--proof-summary-chain",
            str(config.proof_summary_chain_path),
            "--mainline-audit",
            str(config.mainline_audit_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "protocol_lane_readiness_ready_for_dr_sun_decision"
    assert "Module2 Protocol Lane Readiness Packet" in markdown
    assert "not paper result material" in markdown
    assert "terminal_rs_success_rate: `0.53125`" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "stronger_obstacle_summary_warm_start" in markdown
    assert "full_patch_cnn_policy" in markdown
    assert "hybrid_ppo_analytic_fallback" in markdown
    assert "stop_or_reframe_module2_claim" in markdown
    assert "Shared Next Success Attempt Artifact Index" in markdown
    assert "train_final_model_zip" in markdown
    assert "h02_formal_output_acceptance" in markdown
    assert "This readiness packet is not a protocol-lane decision record." in markdown


def _config(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_readiness")
    return builder.FormalGateProtocolLaneReadinessConfig(
        output_dir=tmp_path,
        protocol_status_path=_write_json(tmp_path / "protocol_status.json", _protocol_status()),
        decision_packet_path=_write_json(tmp_path / "decision_packet.json", _decision_packet()),
        decision_record_path=_write_json(tmp_path / "decision_record.json", _decision_record()),
        lane_matrix_path=_write_json(tmp_path / "lane_matrix.json", _lane_matrix()),
        next_round_requirements_path=_write_json(tmp_path / "next_round.json", _next_round()),
        remaining_deliverables_path=_write_json(tmp_path / "remaining.json", _remaining()),
        remote_packet_safety_path=_write_json(tmp_path / "remote_safety.json", {"status": "remote_packet_safety_audit_passed"}),
        claim_safety_path=_write_json(tmp_path / "claim_safety.json", {"status": "blocked_formal_performance_claims"}),
        paper_readiness_path=_write_json(tmp_path / "paper_readiness.json", {"status": "partial_methods_ready_results_blocked"}),
        proof_summary_chain_path=_write_json(
            tmp_path / "proof_chain.json",
            {"status": "formal_gate_proof_summary_chain_consistent_blocked"},
        ),
        mainline_audit_path=_write_json(
            tmp_path / "mainline.json",
            {"status": "mainline_formal_gate_state_consistent_blocked"},
        ),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _protocol_status():
    return {
        "status": "protocol_lane_status_blocked_pending_lane_decision",
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "current_status": {
            "next_blocked_lane": "protocol_lane_decision",
            "selected_lane_id": None,
            "allowed_next_action_ids": ["record_protocol_lane_decision"],
            "blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
            "contract_drafting_allowed_now": False,
            "local_training_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "new_success_training_allowed_now": False,
        },
    }


def _decision_packet():
    return {
        "status": "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun",
        "decision_required": True,
        "lane_options": [
            _packet_lane("stronger_obstacle_summary_warm_start", "compact direct replacement"),
            _packet_lane("full_patch_cnn_policy", "spatial observation architecture"),
            _packet_lane("hybrid_ppo_analytic_fallback", "analytic-assisted hybrid"),
            _packet_lane("stop_or_reframe_module2_claim", "negative evidence only"),
        ],
    }


def _packet_lane(lane_id, claim_scope):
    return {
        "lane_id": lane_id,
        "status": "awaiting_dr_sun_selection",
        "claim_scope": claim_scope,
        "requires_new_or_revised_contract": True,
        "required_decision_justification": [
            "why this lane is justified after observing the failed warm-start Gate3 run",
            "which claim wording remains allowed if this lane is selected",
        ],
    }


def _decision_record():
    return {
        "status": "pending_protocol_lane_decision",
        "decision_owner_required": "Dr Sun",
        "selected_lane_id": None,
        "contract_action": "none",
        "local_training_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "current_authorization": {
            "current_allowed_action_ids": ["record_protocol_lane_decision"],
            "current_blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
        },
    }


def _lane_matrix():
    return {
        "status": "formal_gate_protocol_lane_matrix_ready",
        "lane_count": 4,
        "protocol_lane_evidence_matrix": [
            _matrix_lane(
                "stronger_obstacle_summary_warm_start",
                "direct PPO replacement attempt remains possible",
                "keep compact obstacle-summary policy family",
                ["warm-start dataset source and acceptance checks"],
                ["new remote checkpoint bundle under a new attempt directory"],
                ["new formal Gate3 eval CSV with at least 64 episodes"],
                ["formal_decision=pass in the new gate3_formal_audit.json"],
                ["the failed warm-start checkpoint"],
            ),
            _matrix_lane(
                "full_patch_cnn_policy",
                "direct PPO replacement claim changes substantially",
                "move toward a spatial patch/CNN observation policy",
                ["observation tensor definition"],
                ["checkpoint bundle with architecture metadata"],
                ["timing budget evidence for CNN inference"],
                ["audit proving formal pass under the CNN protocol"],
                ["timing-unchecked CNN results"],
            ),
            _matrix_lane(
                "hybrid_ppo_analytic_fallback",
                "claim likely changes from PPO replacing RS to PPO assisting",
                "treat PPO as a learned selector or recovery layer",
                ["fallback usage metric"],
                ["logs that expose fallback-trigger distribution"],
                ["formal eval with fallback usage columns"],
                ["H02 rows that expose fallback usage and checkpoint hash"],
                ["calling hybrid success direct PPO replacement"],
            ),
            _matrix_lane(
                "stop_or_reframe_module2_claim",
                "no new success-attempt training",
                "record the formal failure and stop pursuing PPO replacement",
                ["negative-result scope"],
                ["no new training evidence required if the contract explicitly stops success attempts"],
                ["existing failed formal Gate3 audit retained as negative evidence"],
                ["claim safety audit blocks success wording"],
                ["writing a positive replacement claim from failed evidence"],
            ),
        ],
    }


def _matrix_lane(
    lane_id,
    claim_scope,
    what_changes,
    contract_deltas,
    training_evidence,
    evaluation_evidence,
    acceptance_evidence,
    invalid_substitutes,
):
    return {
        "lane_id": lane_id,
        "status": "candidate_requires_dr_sun_decision_and_contract",
        "claim_scope": claim_scope,
        "what_changes": what_changes,
        "must_justify": ["why this lane remains valid after the 0.53125 vs 0.8 failure"],
        "required_contract_deltas": contract_deltas,
        "required_training_evidence": training_evidence,
        "required_evaluation_evidence": evaluation_evidence,
        "required_acceptance_evidence": acceptance_evidence,
        "invalid_substitutes": invalid_substitutes,
        "requires_new_or_revised_contract": True,
    }


def _next_round():
    return {
        "status": "formal_gate_next_round_requirements_ready",
        "current_failed_run": {
            "formal_decision": "fail",
            "failure_mode": "threshold_failure",
            "terminal_rs_success_rate": 0.53125,
            "required_success_threshold": 0.8,
            "threshold_deficit": 0.26875,
        },
        "permissions_now": {
            "new_or_revised_contract_required_before_new_success_training": True,
            "new_success_training_allowed_now": False,
            "local_training_allowed_now": False,
            "remote_training_allowed_now_for_existing_packet": False,
            "formal_claim_allowed_now": False,
        },
        "next_success_attempt_artifact_index": {
            "rows": [
                _artifact("contract", "new_or_revised_research_contract"),
                _artifact("training", "train_final_model_zip"),
                _artifact("training", "train_summary_json"),
                _artifact("training", "train_training_manifest_json"),
                _artifact("evaluation", "eval_gate3_eval_episodes_csv"),
                _artifact("evaluation", "eval_gate3_summary_json"),
                _artifact("acceptance", "gate3_trial_manifest_json"),
                _artifact("acceptance", "gate3_formal_audit_json"),
                _artifact("acceptance", "pulled_back_checkpoint_hash_record"),
                _artifact("formal_acceptance", "h02_formal_output_acceptance"),
            ]
        },
    }


def _artifact(category, artifact_id):
    return {
        "category": category,
        "artifact_id": artifact_id,
        "status": "not_created_for_next_success_attempt",
        "expected_path": f"0_trials/module2_gate3_formal/<next_attempt_id>/{artifact_id}",
        "required_before": "paper_result_material",
        "blocked_until": "record_protocol_lane_decision",
        "proof_requirement": "auditable artifact required",
        "invalid_substitutes": ["chat-only approval"],
    }


def _remaining():
    return {
        "status": "formal_gate_deliverables_blocked",
        "gap_summary": {"total_missing_deliverables": 1},
    }
