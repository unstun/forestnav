import json
from importlib import import_module
from pathlib import Path


def test_v2_contract_promotion_packet_waits_for_dr_sun_with_clean_inputs(tmp_path, monkeypatch):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_packet")
    monkeypatch.setattr(builder, "_ssh_config_records", _fake_alias_records)

    manifest = builder.build_manifest(_config(builder, tmp_path))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_contract_promotion_packet"
    assert manifest["status"] == "v2_contract_promotion_packet_ready_awaiting_dr_sun"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["writes_contract"] is False
    assert manifest["approves_contract"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["contract_promotion_allowed_by_packet"] is False
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []

    gate = manifest["current_gate"]
    assert gate["status"] == "v2_contract_readiness_blocked"
    assert gate["blockers"] == ["contract_status_not_approved_or_frozen"]
    assert gate["runner_command_contains_v2_params"] is True

    alias = manifest["remote_alias_evidence"]
    assert alias["recommended_alias"] == "gpu3070ti-relay"
    assert alias["ssh_config_records"]["gpu3070ti-relay"]["proxyjump"] == "ubuntu-obgx"
    assert alias["ssh_config_records"]["gpu3070ti-reply"]["hostname"] == "gpu3070ti-reply"

    items = {item["item_id"]: item for item in manifest["approval_items"]}
    assert set(items) == {
        "remote_alias",
        "training_budget",
        "unsafe_failure_thresholds",
        "contract_status_action",
    }
    assert items["remote_alias"]["status"] == "awaiting_dr_sun_confirmation"
    assert items["remote_alias"]["recommended_value"] == "gpu3070ti-relay"
    assert items["training_budget"]["recommended_value"]["train_total_timesteps"] == 500000
    assert items["training_budget"]["recommended_value"]["train_n_envs"] == 4
    assert items["unsafe_failure_thresholds"]["recommended_value"]["collision_rate_gte"] == 0.30
    assert items["contract_status_action"]["options"] == ["approved", "frozen"]


def test_v2_contract_promotion_packet_fails_if_runner_params_are_not_verified(tmp_path, monkeypatch):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_packet")
    monkeypatch.setattr(builder, "_ssh_config_records", _fake_alias_records)
    config = _config(builder, tmp_path)
    readiness = json.loads(config.readiness_gate_path.read_text(encoding="utf-8"))
    readiness["runner_command_contains_v2_params"] = False
    config.readiness_gate_path.write_text(json.dumps(readiness), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "v2_contract_promotion_packet_audit_failed"
    assert "runner_command_v2_params_not_verified" in issue_ids


def test_v2_contract_promotion_packet_cli_writes_json_and_markdown(tmp_path, monkeypatch):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_promotion_packet")
    monkeypatch.setattr(builder, "_ssh_config_records", _fake_alias_records)
    config = _config(builder, tmp_path)
    manifest_path = tmp_path / "promotion.json"
    markdown_path = tmp_path / "promotion.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract-path",
            str(config.contract_path),
            "--readiness-gate",
            str(config.readiness_gate_path),
            "--gap-ledger",
            str(config.gap_ledger_path),
            "--remote-readiness",
            str(config.remote_readiness_path),
            "--oracle-path",
            str(config.oracle_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "v2_contract_promotion_packet_ready_awaiting_dr_sun"
    assert "Module2 V2 Contract Promotion Packet" in markdown
    assert "does not approve the contract" in markdown
    assert "remote_alias" in markdown
    assert "training_budget" in markdown
    assert "audit_issue_count: `0`" in markdown


def _fake_alias_records(_aliases):
    return {
        "gpu3070ti-relay": {
            "alias": "gpu3070ti-relay",
            "user": "ubuntu",
            "hostname": "127.0.0.1",
            "port": "23070",
            "proxyjump": "ubuntu-obgx",
        },
        "gpu3070ti-reply": {
            "alias": "gpu3070ti-reply",
            "user": "sun",
            "hostname": "gpu3070ti-reply",
            "port": "22",
        },
    }


def _config(builder, tmp_path: Path):
    return builder.Module2V2ContractPromotionPacketConfig(
        output_dir=tmp_path / "out",
        contract_path=_write_contract(tmp_path / "contract.md"),
        readiness_gate_path=_write_json(tmp_path / "readiness.json", _readiness_gate()),
        gap_ledger_path=_write_text(tmp_path / "gap.md", "# gap\n"),
        remote_readiness_path=_write_text(tmp_path / "remote.md", "gpu3070ti-relay RTX 3070 Ti\n"),
        oracle_path=_write_text(tmp_path / "oracle.parquet", "fake"),
    )


def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _write_text(path: Path, payload: str):
    path.write_text(payload, encoding="utf-8")
    return path


def _write_contract(path: Path):
    path.write_text(
        """---
topic: module2-stronger_obstacle_summary_warm_start
status: draft
selected_protocol_lane: stronger_obstacle_summary_warm_start
contract_action: draft_new_contract
allowed_status_before_training:
  - approved
  - frozen
---

# Contract

Selected lane: stronger_obstacle_summary_warm_start.
Budget: 500000 timesteps.
Failure thresholds: collision_rate >= 0.30 and truncation_rate >= 0.20.
Allowed statuses: approved or frozen.
""",
        encoding="utf-8",
    )
    return path


def _readiness_gate():
    return {
        "status": "v2_contract_readiness_blocked",
        "source_head": "abc123",
        "next_action": "promote_or_edit_v2_contract_before_source_freshness",
        "blocker_count": 1,
        "blockers": [{"issue_id": "contract_status_not_approved_or_frozen"}],
        "runner_command_contains_v2_params": True,
        "remote_training_allowed_now": False,
    }
