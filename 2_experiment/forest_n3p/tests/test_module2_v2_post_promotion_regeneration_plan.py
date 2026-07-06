import json
from importlib import import_module
from pathlib import Path


def test_v2_post_promotion_regeneration_plan_waits_for_contract_promotion(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_post_promotion_regeneration_plan")

    manifest = builder.build_manifest(_config(builder, tmp_path, contract_status="draft"))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_post_promotion_regeneration_plan"
    assert manifest["status"] == "blocked_until_v2_contract_promotion"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["remote_preflight_allowed_now"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["next_action"] == "await_dr_sun_before_apply_v2_contract_promotion"
    promotion = _target(manifest, "apply_v2_contract_promotion")
    assert promotion["requires_dr_sun"] is True
    assert promotion["writes_files"] is True
    assert promotion["satisfied_now"] is False
    readiness = _target(manifest, "rerun_v2_contract_readiness_gate")
    assert readiness["allowed_now"] is False
    assert "v2_contract_not_promoted" in readiness["blocked_by"]
    assert "promotion dry-run treated as approval" in manifest["invalid_substitutes"]


def test_v2_post_promotion_regeneration_plan_opens_readiness_after_approval(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_post_promotion_regeneration_plan")

    manifest = builder.build_manifest(_config(builder, tmp_path, contract_status="approved"))

    assert manifest["status"] == "ready_for_rerun_v2_contract_readiness_gate"
    assert manifest["next_action"] == "rerun_v2_contract_readiness_gate"
    readiness = _target(manifest, "rerun_v2_contract_readiness_gate")
    assert readiness["allowed_now"] is True
    assert readiness["satisfied_now"] is False
    assert readiness["runs_training"] is False
    assert manifest["remote_training_allowed_now"] is False


def test_v2_post_promotion_regeneration_plan_allows_only_preflight_target_after_packet_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_post_promotion_regeneration_plan")

    manifest = builder.build_manifest(
        _config(
            builder,
            tmp_path,
            contract_status="approved",
            readiness_status="v2_contract_ready_for_source_freshness",
            source_status="source_freshness_clean_current",
            remote_packet_status="ready_for_v2_remote_preflight",
            remote_preflight_allowed=True,
            chain_blocking_stage="v2_remote_preflight_ready",
        )
    )

    assert manifest["status"] == "ready_for_run_remote_preflight_only"
    preflight = _target(manifest, "run_remote_preflight_only")
    assert preflight["allowed_now"] is True
    assert preflight["runs_remote_preflight"] is True
    training = _target(manifest, "run_remote_training_after_preflight")
    assert training["allowed_now"] is False
    assert training["runs_training"] is True
    assert "v2_remote_preflight_not_ready" in training["blocked_by"]
    assert manifest["remote_training_allowed_now"] is False


def test_v2_post_promotion_regeneration_plan_cli_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_post_promotion_regeneration_plan")
    config = _config(builder, tmp_path, contract_status="draft")
    manifest_path = tmp_path / "plan.json"
    markdown_path = tmp_path / "plan.md"

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
            "--chain-audit",
            str(config.chain_audit_path),
            "--readiness-gate",
            str(config.readiness_gate_path),
            "--source-freshness",
            str(config.source_freshness_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--remaining-evidence",
            str(config.remaining_evidence_path),
            "--promotion-dry-run",
            str(config.promotion_dry_run_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "blocked_until_v2_contract_promotion"
    assert "Module2 V2 Post-Promotion Regeneration Plan" in markdown
    assert "rerun_v2_contract_readiness_gate" in markdown
    assert "remote_training_allowed_now" in markdown


def _config(
    builder,
    tmp_path: Path,
    *,
    contract_status: str,
    readiness_status: str = "v2_contract_readiness_blocked",
    source_status: str = "source_freshness_risks_recorded_gate_still_blocked",
    remote_packet_status: str = "blocked_until_v2_contract_promotion",
    remote_preflight_allowed: bool = False,
    chain_blocking_stage: str = "v2_contract_promoted",
):
    return builder.Module2V2PostPromotionRegenerationPlanConfig(
        output_dir=tmp_path / "out",
        contract_path=_write_contract(tmp_path / "contract.md", contract_status),
        chain_audit_path=_write_json(
            tmp_path / "chain.json",
            {
                "status": "blocked_until_v2_contract_promotion",
                "current_blocking_stage_id": chain_blocking_stage,
                "next_allowed_action": "await_dr_sun_explicit_contract_promotion_then_apply_promotion",
                "audit_issue_count": 0,
            },
        ),
        readiness_gate_path=_write_json(tmp_path / "readiness.json", {"status": readiness_status}),
        source_freshness_path=_write_json(tmp_path / "source.json", {"status": source_status}),
        remote_packet_path=_write_json(
            tmp_path / "remote_packet.json",
            {
                "status": remote_packet_status,
                "remote_preflight_allowed_now": remote_preflight_allowed,
                "remote_training_allowed_now": False,
                "command_plan": {
                    "run_remote_preflight": {"command": "ssh gpu3070ti-relay preflight"},
                    "run_remote_training": {"command": "ssh gpu3070ti-relay train"},
                },
            },
        ),
        remaining_evidence_path=_write_json(
            tmp_path / "remaining.json",
            {
                "status": "blocked_until_v2_contract_promotion",
                "remaining_evidence_summary": {
                    "training_missing_or_unsatisfied": 3,
                    "evaluation_missing_or_unsatisfied": 2,
                    "acceptance_missing_or_unsatisfied": 3,
                    "formal_acceptance_missing_or_unsatisfied": 1,
                },
            },
        ),
        promotion_dry_run_path=_write_json(tmp_path / "dry_run.json", {"status": "promotion_apply_ready"}),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_contract(path: Path, status: str):
    path.write_text(f"---\nstatus: {status}\n---\n", encoding="utf-8")
    return path


def _target(manifest, target_id):
    return next(target for target in manifest["ordered_targets"] if target["target_id"] == target_id)
