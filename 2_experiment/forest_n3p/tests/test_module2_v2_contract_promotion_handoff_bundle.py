import json
from importlib import import_module
from pathlib import Path


def test_v2_contract_promotion_handoff_bundle_ready_for_dr_sun(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_handoff_bundle")

    manifest = builder.build_manifest(_config(builder, tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_contract_promotion_handoff_bundle"
    assert manifest["status"] == "ready_for_dr_sun_v2_contract_promotion_handoff"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["writes_contract"] is False
    assert manifest["approves_contract"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_preflight_allowed_now"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["paper_result_material_allowed_now"] is False
    assert manifest["audit_issue_count"] == 0
    assert manifest["handoff_intent"]["selected_lane_id"] == "stronger_obstacle_summary_warm_start"
    assert manifest["handoff_intent"]["contract_action"] == "draft_new_contract"
    assert manifest["handoff_intent"]["contract_status_now"] == "draft"
    assert manifest["handoff_intent"]["decision_required_from_dr_sun"] is True
    assert manifest["handoff_intent"]["recommended_apply_command_must_not_run_now"] is True
    command = manifest["handoff_intent"]["recommended_apply_command_for_future_explicit_approval"]
    assert "apply_module2_v2_contract_promotion" in command
    assert "--status approved" in command
    assert "--decider 'Dr Sun'" in command
    assert "--remote-alias gpu3070ti-relay" in command
    assert "--confirm-training-budget" in command
    assert "--confirm-unsafe-failure-thresholds" in command
    assert {step["step_id"] for step in manifest["post_apply_required_commands"]} == {
        "rerun_v2_contract_readiness_gate",
        "rerun_source_freshness_audit",
        "regenerate_v2_remote_execution_packet",
        "refresh_v2_remaining_evidence",
        "refresh_v2_formal_gate_chain_audit",
        "refresh_post_promotion_regeneration_plan",
    }
    assert all(step["runs_training"] is False for step in manifest["post_apply_required_commands"])
    assert all(step["runs_remote_preflight"] is False for step in manifest["post_apply_required_commands"])
    assert manifest["remaining_evidence_summary"]["training_missing_or_unsatisfied"] == 3
    assert manifest["remaining_evidence_summary"]["evaluation_missing_or_unsatisfied"] == 2
    assert "promotion dry-run alone as approval" in manifest["invalid_substitutes"]


def test_v2_contract_promotion_handoff_bundle_blocks_if_dry_run_writes_contract(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_handoff_bundle")
    config = _config(builder, tmp_path)
    dry_run = json.loads(config.promotion_dry_run_path.read_text(encoding="utf-8"))
    dry_run["dry_run"] = False
    dry_run["writes_contract"] = True
    config.promotion_dry_run_path.write_text(json.dumps(dry_run), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "v2_contract_promotion_handoff_blocked"
    assert "promotion_result_not_dry_run" in issue_ids
    assert "promotion_dry_run_would_write_contract" in issue_ids


def test_v2_contract_promotion_handoff_bundle_blocks_if_readiness_is_not_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_handoff_bundle")
    config = _config(builder, tmp_path)
    readiness = json.loads(config.promotion_readiness_path.read_text(encoding="utf-8"))
    readiness["status"] = "v2_contract_promotion_readiness_audit_failed"
    readiness["decision_required_from_dr_sun"] = False
    readiness["remote_training_allowed_now"] = True
    config.promotion_readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "v2_contract_promotion_handoff_blocked"
    assert "promotion_readiness_not_ready" in issue_ids
    assert "readiness_does_not_require_dr_sun_decision" in issue_ids
    assert "remote_training_allowed_now_unexpectedly_allowed" in issue_ids


def test_v2_contract_promotion_handoff_bundle_cli_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_handoff_bundle")
    config = _config(builder, tmp_path)
    manifest_path = tmp_path / "handoff.json"
    markdown_path = tmp_path / "handoff.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path / "out"),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract-path",
            str(config.contract_path),
            "--promotion-readiness",
            str(config.promotion_readiness_path),
            "--promotion-packet",
            str(config.promotion_packet_path),
            "--promotion-dry-run",
            str(config.promotion_dry_run_path),
            "--chain-audit",
            str(config.chain_audit_path),
            "--post-promotion-plan",
            str(config.post_promotion_plan_path),
            "--remaining-evidence",
            str(config.remaining_evidence_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "ready_for_dr_sun_v2_contract_promotion_handoff"
    assert "Module2 V2 Contract Promotion Handoff Bundle" in markdown
    assert "does not approve the contract" in markdown
    assert "Future Apply Command" in markdown
    assert "remote_training_allowed_now" in markdown
    assert "audit_issue_count: `0`" in markdown


def _config(builder, tmp_path: Path):
    return builder.Module2V2ContractPromotionHandoffBundleConfig(
        output_dir=tmp_path / "out",
        contract_path=_write_contract(tmp_path / "contract.md"),
        promotion_readiness_path=_write_json(tmp_path / "readiness.json", _promotion_readiness()),
        promotion_packet_path=_write_json(tmp_path / "packet.json", _promotion_packet()),
        promotion_dry_run_path=_write_json(tmp_path / "dry_run.json", _dry_run()),
        chain_audit_path=_write_json(tmp_path / "chain.json", _chain_audit()),
        post_promotion_plan_path=_write_json(tmp_path / "post_plan.json", _post_plan()),
        remaining_evidence_path=_write_json(tmp_path / "remaining.json", _remaining_evidence()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_contract(path: Path):
    path.write_text("---\nstatus: draft\n---\n", encoding="utf-8")
    return path


def _promotion_readiness():
    return {
        "status": "ready_for_dr_sun_v2_contract_promotion_decision",
        "audit_issue_count": 0,
        "decision_required_from_dr_sun": True,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "paper_result_material_allowed_now": False,
    }


def _promotion_packet():
    return {
        "status": "v2_contract_promotion_packet_ready_awaiting_dr_sun",
        "audit_issue_count": 0,
        "remote_training_allowed_now": False,
        "approval_items": [
            {"item_id": "remote_alias", "recommended_value": "gpu3070ti-relay"},
            {"item_id": "training_budget", "recommended_value": {"train_total_timesteps": 500000}},
            {"item_id": "unsafe_failure_thresholds", "recommended_value": {"collision_rate_gte": 0.30}},
            {"item_id": "contract_status_action", "recommended_value": "approved"},
        ],
    }


def _dry_run():
    return {
        "status": "promotion_apply_ready",
        "dry_run": True,
        "writes_contract": False,
        "promotion_apply_allowed": True,
        "target_contract_status": "approved",
        "inputs": {"remote_alias": "gpu3070ti-relay"},
    }


def _chain_audit():
    return {
        "status": "blocked_until_v2_contract_promotion",
        "current_blocking_stage_id": "v2_contract_promoted",
        "audit_issue_count": 0,
    }


def _post_plan():
    return {
        "status": "blocked_until_v2_contract_promotion",
        "next_action": "await_dr_sun_before_apply_v2_contract_promotion",
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
    }


def _remaining_evidence():
    return {
        "decision_state": {
            "selected_lane_id": "stronger_obstacle_summary_warm_start",
            "contract_action": "draft_new_contract",
            "contract_status": "draft",
        },
        "permissions_now": {
            "local_training_allowed_now": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "paper_result_material_allowed_now": False,
        },
        "remaining_evidence_summary": {
            "total_required_evidence_items": 12,
            "total_missing_or_unsatisfied": 12,
            "training_missing_or_unsatisfied": 3,
            "evaluation_missing_or_unsatisfied": 2,
            "acceptance_missing_or_unsatisfied": 3,
            "formal_acceptance_missing_or_unsatisfied": 1,
        },
    }
