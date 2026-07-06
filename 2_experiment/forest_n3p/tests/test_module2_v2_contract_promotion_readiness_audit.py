import json
from importlib import import_module
from pathlib import Path


def test_v2_contract_promotion_readiness_audit_ready_for_dr_sun(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_readiness_audit")

    manifest = builder.build_manifest(_config(builder, tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_contract_promotion_readiness_audit"
    assert manifest["status"] == "ready_for_dr_sun_v2_contract_promotion_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["writes_contract"] is False
    assert manifest["approves_contract"] is False
    assert manifest["runs_training"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["decision_required_from_dr_sun"] is True
    assert manifest["audit_issue_count"] == 0
    assert manifest["readiness_summary"]["approval_item_ids"] == [
        "remote_alias",
        "training_budget",
        "unsafe_failure_thresholds",
        "contract_status_action",
    ]
    assert manifest["recommended_decision_payload"]["target_status"] == "approved"
    assert manifest["recommended_decision_payload"]["remote_alias"] == "gpu3070ti-relay"
    assert "promotion dry-run alone as approval" in manifest["invalid_substitutes"]


def test_v2_contract_promotion_readiness_audit_rejects_non_dry_run_or_bad_chain(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_readiness_audit")
    config = _config(builder, tmp_path)
    dry_run = json.loads(config.promotion_dry_run_path.read_text(encoding="utf-8"))
    dry_run["dry_run"] = False
    dry_run["writes_contract"] = True
    config.promotion_dry_run_path.write_text(json.dumps(dry_run), encoding="utf-8")
    chain = json.loads(config.chain_audit_path.read_text(encoding="utf-8"))
    chain["current_blocking_stage_id"] = "source_freshness_ready"
    config.chain_audit_path.write_text(json.dumps(chain), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "v2_contract_promotion_readiness_audit_failed"
    assert "promotion_result_not_dry_run" in issue_ids
    assert "promotion_dry_run_would_write_contract" in issue_ids
    assert "chain_audit_not_blocked_at_contract_promotion" in issue_ids


def test_v2_contract_promotion_readiness_audit_rejects_missing_approval_item(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_readiness_audit")
    config = _config(builder, tmp_path)
    packet = json.loads(config.promotion_packet_path.read_text(encoding="utf-8"))
    packet["approval_items"] = packet["approval_items"][:-1]
    config.promotion_packet_path.write_text(json.dumps(packet), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "v2_contract_promotion_readiness_audit_failed"
    assert "promotion_packet_approval_items_incomplete" in issue_ids


def test_v2_contract_promotion_readiness_audit_cli_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_readiness_audit")
    config = _config(builder, tmp_path)
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

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
            "--promotion-packet",
            str(config.promotion_packet_path),
            "--promotion-dry-run",
            str(config.promotion_dry_run_path),
            "--chain-audit",
            str(config.chain_audit_path),
            "--post-promotion-plan",
            str(config.post_promotion_plan_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "ready_for_dr_sun_v2_contract_promotion_decision"
    assert "Module2 V2 Contract Promotion Readiness Audit" in markdown
    assert "does not approve the contract" in markdown
    assert "remote_training_allowed_now" in markdown


def _config(builder, tmp_path: Path):
    return builder.Module2V2ContractPromotionReadinessAuditConfig(
        output_dir=tmp_path / "out",
        contract_path=_write_contract(tmp_path / "contract.md"),
        promotion_packet_path=_write_json(tmp_path / "packet.json", _promotion_packet()),
        promotion_dry_run_path=_write_json(tmp_path / "dry_run.json", _dry_run()),
        chain_audit_path=_write_json(tmp_path / "chain.json", _chain_audit()),
        post_promotion_plan_path=_write_json(tmp_path / "post_plan.json", _post_plan()),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_contract(path: Path):
    path.write_text("---\nstatus: draft\n---\n", encoding="utf-8")
    return path


def _promotion_packet():
    return {
        "status": "v2_contract_promotion_packet_ready_awaiting_dr_sun",
        "audit_issue_count": 0,
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
        "blocker_count": 0,
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
        "remote_training_allowed_now": False,
    }
