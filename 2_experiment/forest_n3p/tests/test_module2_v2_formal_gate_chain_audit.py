import json
from importlib import import_module
from pathlib import Path


def test_v2_formal_gate_chain_audit_blocks_at_contract_promotion(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit")

    manifest = builder.build_manifest(_config(builder, tmp_path, contract_status="draft"))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_formal_gate_chain_audit"
    assert manifest["status"] == "blocked_until_v2_contract_promotion"
    assert manifest["current_blocking_stage_id"] == "v2_contract_promoted"
    assert manifest["next_allowed_action"] == "await_dr_sun_explicit_contract_promotion_then_apply_promotion"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["remote_preflight_allowed_now"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["audit_issue_count"] == 0
    assert _stage(manifest, "protocol_lane_decision_recorded")["satisfied"] is True
    assert _stage(manifest, "promotion_packet_ready")["satisfied"] is True
    assert _stage(manifest, "promotion_dry_run_ready")["satisfied"] is True
    assert _stage(manifest, "v2_contract_promoted")["satisfied"] is False
    assert "promotion dry-run treated as approval" in manifest["invalid_substitutes"]


def test_v2_formal_gate_chain_audit_blocks_at_preflight_after_promoted_remote_packet(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit")

    manifest = builder.build_manifest(
        _config(
            builder,
            tmp_path,
            contract_status="approved",
            readiness_status="v2_contract_ready_for_source_freshness",
            source_status="source_freshness_clean_current",
            remote_packet_status="ready_for_v2_remote_preflight",
            remote_preflight_allowed=True,
        )
    )

    assert manifest["status"] == "blocked_until_v2_remote_preflight"
    assert manifest["current_blocking_stage_id"] == "v2_remote_preflight_ready"
    assert manifest["remote_preflight_allowed_now"] is True
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["audit_issue_count"] == 0
    assert _stage(manifest, "v2_remote_packet_ready")["satisfied"] is True
    assert _stage(manifest, "v2_remote_preflight_ready")["satisfied"] is False


def test_v2_formal_gate_chain_audit_rejects_downstream_stage_skip(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit")

    manifest = builder.build_manifest(
        _config(
            builder,
            tmp_path,
            contract_status="draft",
            readiness_status="v2_contract_ready_for_source_freshness",
            source_status="source_freshness_clean_current",
            remote_packet_status="ready_for_v2_remote_preflight",
            remote_preflight_allowed=True,
        )
    )

    assert manifest["status"] == "v2_formal_gate_chain_inconsistent"
    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert "downstream_stage_satisfied_before_upstream_gate" in issue_ids
    assert manifest["current_blocking_stage_id"] == "v2_contract_promoted"
    assert manifest["remote_preflight_allowed_now"] is False


def test_v2_formal_gate_chain_audit_cli_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit")
    config = _config(builder, tmp_path, contract_status="draft")
    manifest_path = tmp_path / "chain.json"
    markdown_path = tmp_path / "chain.md"

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
            "--decision-record",
            str(config.decision_record_path),
            "--promotion-packet",
            str(config.promotion_packet_path),
            "--promotion-dry-run",
            str(config.promotion_dry_run_path),
            "--readiness-gate",
            str(config.readiness_gate_path),
            "--source-freshness",
            str(config.source_freshness_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--preflight-manifest",
            str(config.preflight_manifest_path),
            "--remaining-evidence",
            str(config.remaining_evidence_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "blocked_until_v2_contract_promotion"
    assert "Module2 V2 Formal Gate Chain Audit" in markdown
    assert "v2_contract_promoted" in markdown
    assert "paper-result writing" in markdown


def _config(
    builder,
    tmp_path: Path,
    *,
    contract_status: str,
    readiness_status: str = "v2_contract_readiness_blocked",
    source_status: str = "source_freshness_risks_recorded_gate_still_blocked",
    remote_packet_status: str = "blocked_until_v2_contract_promotion",
    remote_preflight_allowed: bool = False,
):
    return builder.Module2V2FormalGateChainAuditConfig(
        output_dir=tmp_path / "out",
        contract_path=_write_contract(tmp_path / "contract.md", contract_status),
        decision_record_path=_write_json(
            tmp_path / "decision.json",
            {
                "status": "protocol_lane_decision_recorded",
                "selected_lane_id": "stronger_obstacle_summary_warm_start",
                "contract_action": "draft_new_contract",
            },
        ),
        promotion_packet_path=_write_json(
            tmp_path / "promotion.json",
            {"status": "v2_contract_promotion_packet_ready_awaiting_dr_sun"},
        ),
        promotion_dry_run_path=_write_json(tmp_path / "dry_run.json", {"status": "promotion_apply_ready"}),
        readiness_gate_path=_write_json(tmp_path / "readiness.json", {"status": readiness_status}),
        source_freshness_path=_write_json(tmp_path / "source.json", {"status": source_status}),
        remote_packet_path=_write_json(
            tmp_path / "remote_packet.json",
            {
                "status": remote_packet_status,
                "remote_preflight_allowed_now": remote_preflight_allowed,
                "remote_training_allowed_now": False,
                "local_training_allowed_now": False,
                "paper_result_material_allowed_now": False,
            },
        ),
        preflight_manifest_path=tmp_path / "missing_preflight.json",
        remaining_evidence_path=_write_json(
            tmp_path / "remaining.json",
            {
                "status": "blocked_until_v2_contract_promotion",
                "remote_training_allowed_now": False,
                "local_training_allowed_now": False,
                "paper_result_material_allowed_now": False,
                "remaining_evidence_summary": {
                    "training_missing_or_unsatisfied": 3,
                    "evaluation_missing_or_unsatisfied": 2,
                    "acceptance_missing_or_unsatisfied": 3,
                    "formal_acceptance_missing_or_unsatisfied": 1,
                },
            },
        ),
        h02_acceptance_path=_write_json(
            tmp_path / "h02.json",
            {
                "status": "blocked_formal_output_acceptance",
                "formal_output_accepted": False,
                "paper_result_input_allowed": False,
            },
        ),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_contract(path: Path, status: str):
    path.write_text(f"---\nstatus: {status}\n---\n", encoding="utf-8")
    return path


def _stage(manifest, stage_id):
    return next(stage for stage in manifest["stages"] if stage["stage_id"] == stage_id)
