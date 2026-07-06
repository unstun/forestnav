import json
from importlib import import_module
from pathlib import Path


def test_v2_remote_execution_packet_blocks_until_contract_promotion(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_remote_execution_packet")

    packet = builder.build_packet(_config(builder, tmp_path, contract_status="draft", readiness_status="v2_contract_readiness_blocked"))

    assert packet["schema_version"] == 1
    assert packet["packet_name"] == "module2_v2_remote_execution_packet"
    assert packet["status"] == "blocked_until_v2_contract_promotion"
    assert packet["not_paper_result_material"] is True
    assert packet["executes_commands"] is False
    assert packet["runs_training"] is False
    assert packet["runs_remote_preflight"] is False
    assert packet["remote_preflight_allowed_now"] is False
    assert packet["remote_training_allowed_now"] is False
    assert packet["ready_to_run_remote_training"] is False
    assert "v2_contract_not_promoted" in packet["blockers"]
    assert "v2_contract_readiness_not_ready" in packet["blockers"]
    assert packet["command_plan"]["run_remote_training"]["allowed_now"] is False
    assert packet["command_plan"]["run_remote_training"]["runs_training"] is True
    assert "--contract-path" in packet["command_plan"]["run_remote_training"]["command"]
    assert "--train-total-timesteps 500000" in packet["command_plan"]["run_remote_training"]["command"]
    assert "--train-learning-rate 0.0001" in packet["command_plan"]["run_remote_training"]["command"]
    assert "--train-ent-coef 0.01" in packet["command_plan"]["run_remote_training"]["command"]
    assert "--warm-start-decision approved_obstacle_summary" in packet["command_plan"]["run_remote_audit"]["command"]
    assert "--delete" not in packet["command_plan"]["sync_to_remote"]["command"]


def test_v2_remote_execution_packet_allows_only_preflight_after_readiness_and_source_freshness(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_remote_execution_packet")

    packet = builder.build_packet(
        _config(
            builder,
            tmp_path,
            contract_status="approved",
            readiness_status="v2_contract_ready_for_source_freshness",
            source_status="source_freshness_remote_preflight_scope_ready_with_later_risks",
        )
    )

    assert packet["status"] == "ready_for_v2_remote_preflight"
    assert packet["blockers"] == []
    assert packet["ready_to_run_remote_preflight"] is True
    assert packet["remote_preflight_allowed_now"] is True
    assert packet["ready_to_run_remote_training"] is False
    assert packet["remote_training_allowed_now"] is False
    assert packet["command_plan"]["sync_to_remote"]["allowed_now"] is True
    assert packet["command_plan"]["run_remote_preflight"]["allowed_now"] is True
    assert packet["command_plan"]["run_remote_training"]["allowed_now"] is False
    assert "cd /home/ubuntu/ForestNav" in packet["command_plan"]["run_remote_preflight"]["command"]
    assert "v2_remote_preflight_not_ready" in packet["command_plan"]["run_remote_training"]["blocked_by"]
    assert packet["expected_pullback_artifacts"][0].endswith("train/final_model.zip")


def test_v2_remote_execution_packet_cli_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_remote_execution_packet")
    config = _config(builder, tmp_path, contract_status="draft", readiness_status="v2_contract_readiness_blocked")
    packet_path = tmp_path / "packet.json"
    markdown_path = tmp_path / "packet.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--packet-out",
            str(packet_path),
            "--markdown-out",
            str(markdown_path),
            "--readiness-gate",
            str(config.readiness_gate_path),
            "--promotion-packet",
            str(config.promotion_packet_path),
            "--promotion-dry-run",
            str(config.promotion_dry_run_path),
            "--source-freshness",
            str(config.source_freshness_path),
            "--remote-readiness",
            str(config.remote_readiness_path),
            "--contract-path",
            str(config.contract_path),
            "--oracle-path",
            str(config.oracle_path),
            "--bc-checkpoint",
            str(config.bc_checkpoint),
            "--attempt-dir",
            str(config.attempt_dir),
            "--preflight-manifest",
            str(config.preflight_manifest_path),
        ]
    )

    assert rc == 0
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert packet["status"] == "blocked_until_v2_contract_promotion"
    assert "Module2 V2 Remote Execution Packet" in markdown
    assert "run_remote_training" in markdown
    assert "old v1 remote execution packet" in markdown


def _config(
    builder,
    tmp_path: Path,
    *,
    contract_status: str,
    readiness_status: str,
    source_status: str = "source_freshness_risks_recorded_gate_still_blocked",
):
    return builder.Module2V2RemoteExecutionPacketConfig(
        output_dir=tmp_path / "out",
        readiness_gate_path=_write_json(tmp_path / "readiness.json", _readiness(readiness_status)),
        promotion_packet_path=_write_json(tmp_path / "promotion.json", {"status": "v2_contract_promotion_packet_ready_awaiting_dr_sun"}),
        promotion_dry_run_path=_write_json(tmp_path / "dry_run.json", {"status": "promotion_apply_ready"}),
        source_freshness_path=_write_json(tmp_path / "source.json", {"status": source_status}),
        remote_readiness_path=_write_text(tmp_path / "remote.md", "gpu3070ti-relay RTX 3070 Ti\n"),
        contract_path=_write_contract(tmp_path / "contract.md", status=contract_status),
        oracle_path=_write_text(tmp_path / "oracle.parquet", "fake"),
        bc_checkpoint=_write_text(tmp_path / "checkpoint.pt", "fake"),
        attempt_dir=tmp_path / "gate3_stronger_obstacle_summary_warm_start_v2_seed20260706",
        preflight_manifest_path=tmp_path / "preflight.json",
        local_root=tmp_path,
    )


def _readiness(status: str):
    return {
        "status": status,
        "runner_command_contains_v2_params": True,
        "remote_training_allowed_now": False,
    }


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_text(path: Path, payload: str):
    path.write_text(payload, encoding="utf-8")
    return path


def _write_contract(path: Path, *, status: str):
    path.write_text(f"---\nstatus: {status}\n---\n", encoding="utf-8")
    return path
