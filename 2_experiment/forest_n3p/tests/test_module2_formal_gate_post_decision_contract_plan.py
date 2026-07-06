import json
from importlib import import_module
from pathlib import Path


def test_post_decision_contract_plan_prepares_contract_without_authorization(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan")

    manifest = builder.build_manifest(_config(builder, tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_post_decision_contract_plan"
    assert manifest["status"] == "post_decision_contract_plan_ready_blocked_pending_lane_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["writes_contract"] is False
    assert manifest["approves_contract"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False

    gate = manifest["gate_state"]
    assert gate["next_blocked_lane"] == "protocol_lane_decision"
    assert gate["selected_lane_id"] is None
    assert gate["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert gate["contract_drafting_allowed_now"] is False
    assert gate["remote_training_allowed_now"] is False
    assert gate["post_decision_plan_authorizes_contract_write"] is False
    assert gate["post_decision_plan_authorizes_training"] is False

    assert manifest["required_contract_section_count"] == 8
    assert {row["section_id"] for row in manifest["required_contract_sections"]} == {
        "protocol_lane",
        "hypothesis",
        "success_signal",
        "failure_signal",
        "protocol_delta_from_failed_run",
        "training_budget_and_seed_policy",
        "evaluation_and_acceptance_plan",
        "paper_claim_boundary",
    }
    assert manifest["shared_next_success_attempt_artifact_count"] == 10
    assert manifest["shared_next_success_attempt_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert manifest["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True
    lanes = {row["lane_id"]: row for row in manifest["lane_contract_plans"]}
    assert set(lanes) == {
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    }
    assert lanes["stronger_obstacle_summary_warm_start"]["expected_contract_path_template"] == (
        ".pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md"
    )
    assert len(lanes["stronger_obstacle_summary_warm_start"]["next_success_attempt_artifact_ids"]) == 10
    assert "train_final_model_zip" in lanes["stronger_obstacle_summary_warm_start"]["next_success_attempt_artifact_ids"]
    assert "gate3_formal_audit_json" in lanes["hybrid_ppo_analytic_fallback"]["next_success_attempt_artifact_ids"]
    assert lanes["stop_or_reframe_module2_claim"]["new_success_training_required_if_selected"] is False
    assert lanes["stop_or_reframe_module2_claim"]["next_success_attempt_artifact_ids"] == []
    assert any(
        row["section_id"] == "protocol_lane" and row["must_reference_failed_gate3"] is True
        for row in lanes["full_patch_cnn_policy"]["section_plan"]
    )
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_post_decision_contract_plan_catches_training_authorization_leak(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan")
    config = _config(builder, tmp_path)
    readiness = json.loads(config.protocol_lane_readiness_path.read_text(encoding="utf-8"))
    readiness["gate_state"]["remote_training_allowed_now"] = True
    config.protocol_lane_readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "post_decision_contract_plan_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "remote_training_allowed_now_unexpectedly_true" in issue_ids


def test_post_decision_contract_plan_catches_missing_lane_evidence(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan")
    config = _config(builder, tmp_path)
    readiness = json.loads(config.protocol_lane_readiness_path.read_text(encoding="utf-8"))
    readiness["lane_readiness_rows"][0]["invalid_substitutes"] = []
    readiness["lane_readiness_rows"][1]["required_training_evidence"] = []
    config.protocol_lane_readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "post_decision_contract_plan_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "stronger_obstacle_summary_warm_start_missing_invalid_substitutes" in issue_ids
    assert "full_patch_cnn_policy_required_training_evidence_missing" in issue_ids


def test_post_decision_contract_plan_catches_next_success_summary_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan")
    config = _config(builder, tmp_path)
    next_round = json.loads(config.next_round_requirements_path.read_text(encoding="utf-8"))
    next_round["protocol_gate_summary"]["next_success_attempt_artifact_category_counts"]["training"] = 2
    next_round["current_vs_next_attempt_reconciliation"][
        "old_failed_run_artifacts_invalid_for_next_success_attempt"
    ] = False
    config.next_round_requirements_path.write_text(json.dumps(next_round), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "post_decision_contract_plan_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "shared_artifact_category_counts_invalid" in issue_ids
    assert "old_failed_run_artifacts_not_marked_invalid" in issue_ids


def test_post_decision_contract_plan_catches_missing_contract_section(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan")
    config = _config(builder, tmp_path)
    contract = json.loads(config.contract_intake_path.read_text(encoding="utf-8"))
    contract["contract_output_requirements"]["required_sections"].remove("failure_signal")
    config.contract_intake_path.write_text(json.dumps(contract), encoding="utf-8")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "post_decision_contract_plan_audit_failed"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "required_contract_section_missing_failure_signal" in issue_ids


def test_post_decision_contract_plan_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan")
    config = _config(builder, tmp_path)
    manifest_path = tmp_path / "post_decision_contract_plan.json"
    markdown_path = tmp_path / "post_decision_contract_plan.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--protocol-lane-readiness",
            str(config.protocol_lane_readiness_path),
            "--contract-intake",
            str(config.contract_intake_path),
            "--contract-authoring-gate",
            str(config.contract_authoring_gate_path),
            "--next-round-requirements",
            str(config.next_round_requirements_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "post_decision_contract_plan_ready_blocked_pending_lane_decision"
    assert "Module2 Post-Decision Contract Plan" in markdown
    assert "not a contract draft" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "stronger_obstacle_summary_warm_start" in markdown
    assert "full_patch_cnn_policy" in markdown
    assert "hybrid_ppo_analytic_fallback" in markdown
    assert "stop_or_reframe_module2_claim" in markdown
    assert "train_final_model_zip" in markdown
    assert "h02_formal_output_acceptance" in markdown
    assert "shared_next_success_attempt_artifact_category_counts" in markdown
    assert "old_failed_run_artifacts_invalid_for_next_success_attempt: `True`" in markdown


def _config(builder, tmp_path):
    return builder.FormalGatePostDecisionContractPlanConfig(
        output_dir=tmp_path,
        protocol_lane_readiness_path=_write_json(tmp_path / "readiness.json", _readiness()),
        contract_intake_path=_write_json(tmp_path / "contract_intake.json", _contract_intake()),
        contract_authoring_gate_path=_write_json(tmp_path / "contract_gate.json", _contract_gate()),
        next_round_requirements_path=_write_json(tmp_path / "next_round.json", _next_round()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _readiness():
    return {
        "status": "protocol_lane_readiness_ready_for_dr_sun_decision",
        "audit_issue_count": 0,
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "gate_state": {
            "next_blocked_lane": "protocol_lane_decision",
            "selected_lane_id": None,
            "decision_owner_required": "Dr Sun",
            "next_action_ids": ["record_protocol_lane_decision"],
            "blocked_action_ids": [
                "local_training",
                "remote_success_training",
                "remote_preflight_for_new_success_attempt",
                "formal_claim",
                "paper_result_material",
            ],
            "local_training_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "paper_result_material_allowed_now": False,
        },
        "shared_next_success_attempt_artifacts": _shared_artifacts(),
        "lane_readiness_rows": [
            _lane("stronger_obstacle_summary_warm_start", True, "direct compact warm-start"),
            _lane("full_patch_cnn_policy", True, "spatial patch CNN"),
            _lane("hybrid_ppo_analytic_fallback", True, "analytic-assisted hybrid"),
            _lane("stop_or_reframe_module2_claim", False, "negative evidence only"),
        ],
    }


def _lane(lane_id, success_training_required, claim_scope):
    return {
        "lane_id": lane_id,
        "claim_scope": claim_scope,
        "new_success_training_required_if_selected": success_training_required,
        "next_action_after_selection": (
            "draft_new_or_revised_contract_then_remote_training_packet"
            if success_training_required
            else "draft_stop_or_reframe_contract"
        ),
        "required_decision_justification": [
            "why this lane is justified after observing the failed warm-start Gate3 run",
            "which claim wording remains allowed if this lane is selected",
        ],
        "required_contract_deltas": [
            "protocol lane delta",
            "budget and seed policy",
        ],
        "required_training_evidence": (
            ["new remote checkpoint bundle", "new training_manifest.json"]
            if success_training_required
            else ["no new training evidence required if the contract explicitly stops success attempts"]
        ),
        "required_evaluation_evidence": [
            "new formal Gate3 eval CSV" if success_training_required else "retain failed Gate3 as negative evidence"
        ],
        "required_acceptance_evidence": [
            "new formal audit pass" if success_training_required else "claim safety blocks success wording"
        ],
        "invalid_substitutes": [
            "failed warm-start checkpoint",
            "local PPO training output",
        ],
    }


def _shared_artifacts():
    ids = [
        ("contract", "new_or_revised_research_contract"),
        ("training", "train_final_model_zip"),
        ("training", "train_summary_json"),
        ("training", "train_training_manifest_json"),
        ("evaluation", "eval_gate3_eval_episodes_csv"),
        ("evaluation", "eval_gate3_summary_json"),
        ("acceptance", "gate3_trial_manifest_json"),
        ("acceptance", "gate3_formal_audit_json"),
        ("acceptance", "pulled_back_checkpoint_hash_record"),
        ("formal_acceptance", "h02_formal_output_acceptance"),
    ]
    return [
        {
            "category": category,
            "artifact_id": artifact_id,
            "status": "blocked",
            "expected_path": f"expected/{artifact_id}",
            "required_before": "paper_result_material",
            "blocked_until": "approved_or_frozen_new_or_revised_contract",
            "proof_requirement": "proof required",
            "invalid_substitutes": ["smoke output"],
        }
        for category, artifact_id in ids
    ]


def _contract_intake():
    return {
        "status": "formal_gate_contract_intake_ready_for_dr_sun",
        "decision_fields_required_for_contract": [
            {"field": "protocol_lane", "status": "awaiting_dr_sun_decision", "prompt": "choose lane"},
            {"field": "hypothesis", "status": "awaiting_dr_sun_decision", "prompt": "lock hypothesis"},
            {"field": "success_signal", "status": "awaiting_dr_sun_decision", "prompt": "lock success"},
            {"field": "failure_signal", "status": "awaiting_dr_sun_decision", "prompt": "lock failure"},
            {"field": "protocol_delta_from_failed_run", "status": "awaiting_dr_sun_decision", "prompt": "lock delta"},
            {"field": "training_budget_and_seed_policy", "status": "awaiting_dr_sun_decision", "prompt": "lock budget"},
            {"field": "evaluation_and_acceptance_plan", "status": "awaiting_dr_sun_decision", "prompt": "lock eval"},
            {"field": "paper_claim_boundary", "status": "awaiting_dr_sun_decision", "prompt": "lock claim"},
        ],
        "contract_output_requirements": {
            "required_sections": [
                "protocol_lane",
                "hypothesis",
                "success_signal",
                "failure_signal",
                "protocol_delta_from_failed_run",
                "training_budget_and_seed_policy",
                "evaluation_and_acceptance_plan",
                "paper_claim_boundary",
            ]
        },
    }


def _contract_gate():
    return {
        "status": "contract_authoring_gate_blocked_pending_lane_decision",
        "contract_gate": {
            "decision_record_status": "pending_protocol_lane_decision",
            "contract_drafting_allowed_now": False,
            "contract_approval_allowed_now": False,
            "draft_contract_allows_training": False,
        },
    }


def _next_round():
    return {
        "status": "formal_gate_next_round_requirements_ready",
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now_for_existing_packet": False,
            "formal_claim_allowed_now": False,
            "new_or_revised_contract_required_before_new_success_training": True,
        },
        "protocol_gate_summary": {
            "next_success_attempt_artifact_count": 10,
            "next_success_attempt_artifact_category_counts": {
                "contract": 1,
                "training": 3,
                "evaluation": 2,
                "acceptance": 3,
                "formal_acceptance": 1,
            },
        },
        "current_vs_next_attempt_reconciliation": {
            "old_failed_run_artifacts_invalid_for_next_success_attempt": True,
        },
        "next_success_attempt_artifact_index": {"rows": _shared_artifacts()},
    }
