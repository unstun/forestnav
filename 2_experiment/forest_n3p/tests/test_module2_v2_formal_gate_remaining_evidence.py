import json
from importlib import import_module
from pathlib import Path


def test_v2_formal_gate_remaining_evidence_blocks_on_draft_contract(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence")

    manifest = builder.build_manifest(_config(builder, tmp_path, contract_status="draft"))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_formal_gate_remaining_evidence"
    assert manifest["status"] == "blocked_until_v2_contract_promotion"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["permissions_now"]["local_training_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False
    assert manifest["failed_gate3_basis"]["terminal_rs_success_rate"] == 0.53125
    assert manifest["failed_gate3_basis"]["terminal_rs_successes"] == 34
    assert manifest["failed_gate3_basis"]["required_success_threshold"] == 0.8
    assert manifest["failed_gate3_basis"]["usable_as_success_evidence"] is False
    assert "v2_contract_not_promoted" in _issue_ids(manifest)
    assert manifest["remaining_evidence_summary"]["training_missing_or_unsatisfied"] == 3
    assert manifest["remaining_evidence_summary"]["evaluation_missing_or_unsatisfied"] == 2
    assert manifest["remaining_evidence_summary"]["acceptance_missing_or_unsatisfied"] == 3
    assert manifest["remaining_evidence_summary"]["formal_acceptance_missing_or_unsatisfied"] == 1
    assert any(row["artifact_id"] == "train_final_model_zip" for row in manifest["deliverables"])
    assert any("failed gate3_obstacle_summary" in item for item in manifest["invalid_substitutes"])


def test_v2_formal_gate_remaining_evidence_reaches_preflight_block_after_promoted_inputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence")

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
    assert "v2_contract_not_promoted" not in _issue_ids(manifest)
    assert "source_freshness_not_ready" not in _issue_ids(manifest)
    assert "v2_remote_preflight_manifest_not_ready" in _issue_ids(manifest)
    assert manifest["permissions_now"]["remote_preflight_allowed_now"] is False
    assert manifest["permissions_now"]["remote_training_allowed_now"] is False


def test_v2_formal_gate_remaining_evidence_cli_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence")
    config = _config(builder, tmp_path, contract_status="draft")
    manifest_path = tmp_path / "ledger.json"
    markdown_path = tmp_path / "ledger.md"

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
            "--readiness-gate",
            str(config.readiness_gate_path),
            "--promotion-packet",
            str(config.promotion_packet_path),
            "--promotion-dry-run",
            str(config.promotion_dry_run_path),
            "--source-freshness",
            str(config.source_freshness_path),
            "--remote-packet",
            str(config.remote_packet_path),
            "--preflight-manifest",
            str(config.preflight_manifest_path),
            "--failed-gate3-summary",
            str(config.failed_gate3_summary_path),
            "--h02-acceptance",
            str(config.h02_acceptance_path),
            "--attempt-dir",
            str(config.attempt_dir),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "blocked_until_v2_contract_promotion"
    assert "Module2 V2 Formal Gate Remaining Evidence" in markdown
    assert "train_final_model_zip" in markdown
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
    return builder.Module2V2FormalGateRemainingEvidenceConfig(
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
        readiness_gate_path=_write_json(tmp_path / "readiness.json", {"status": readiness_status}),
        promotion_packet_path=_write_json(
            tmp_path / "promotion.json",
            {"status": "v2_contract_promotion_packet_ready_awaiting_dr_sun"},
        ),
        promotion_dry_run_path=_write_json(tmp_path / "dry_run.json", {"status": "promotion_apply_ready"}),
        source_freshness_path=_write_json(tmp_path / "source.json", {"status": source_status}),
        remote_packet_path=_write_json(
            tmp_path / "remote_packet.json",
            {"status": remote_packet_status, "remote_preflight_allowed_now": remote_preflight_allowed},
        ),
        preflight_manifest_path=tmp_path / "missing_preflight.json",
        failed_gate3_summary_path=_write_json(
            tmp_path / "failed_summary.json",
            {
                "decision": "fail",
                "episodes": 64,
                "terminal_rs_successes": 34,
                "terminal_rs_success_rate": 0.53125,
                "success_threshold": 0.8,
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
        attempt_dir=tmp_path / "gate3_stronger_obstacle_summary_warm_start_v2_seed20260706",
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_contract(path: Path, status: str):
    path.write_text(
        f"---\nstatus: {status}\nselected_protocol_lane: stronger_obstacle_summary_warm_start\ncontract_action: draft_new_contract\n---\n",
        encoding="utf-8",
    )
    return path


def _issue_ids(manifest):
    return {item["issue_id"] for item in manifest["gate_blockers"]}
