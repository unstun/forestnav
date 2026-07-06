import json
import subprocess
import sys
from importlib import import_module
from pathlib import Path


def test_v2_contract_readiness_blocks_draft_contract_but_verifies_preflight_params(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_readiness_gate")
    config = _config(builder, tmp_path, status="draft")

    manifest = builder.build_manifest(config)

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_v2_contract_readiness_gate"
    assert manifest["status"] == "v2_contract_readiness_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["source_freshness_regeneration_allowed_after_contract"] is False
    assert manifest["next_action"] == "promote_or_edit_v2_contract_before_source_freshness"

    issue_ids = {issue["issue_id"] for issue in manifest["blockers"]}
    assert issue_ids == {"contract_status_not_approved_or_frozen"}

    assert manifest["contract_summary"]["status"] == "draft"
    assert manifest["contract_summary"]["selected_protocol_lane"] == "stronger_obstacle_summary_warm_start"
    assert manifest["expected_training_params"]["train_total_timesteps"] == 500000
    assert manifest["expected_training_params"]["train_n_envs"] == 4
    assert manifest["expected_training_params"]["train_learning_rate"] == 0.0001
    assert manifest["expected_training_params"]["train_ent_coef"] == 0.01
    assert manifest["runner_command_contains_v2_params"] is True

    probe = manifest["preflight_probe"]
    assert probe["preflight_status"] == "blocked"
    assert probe["contract_status"] == "draft"
    assert probe["protocol"]["contract"] == str(config.contract_path)
    assert probe["protocol"]["train_total_timesteps"] == 500000
    assert probe["protocol"]["train_n_envs"] == 4
    assert probe["protocol"]["train_learning_rate"] == 0.0001
    assert "--contract-path" in probe["runner_command"]
    assert "--train-total-timesteps 500000" in probe["runner_command"]
    assert "--train-n-envs 4" in probe["runner_command"]
    assert "--train-learning-rate 0.0001" in probe["runner_command"]
    assert "--train-ent-coef 0.01" in probe["runner_command"]


def test_v2_contract_readiness_allows_source_freshness_after_approved_contract(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_readiness_gate")
    config = _config(builder, tmp_path, status="approved")

    manifest = builder.build_manifest(config)

    assert manifest["status"] == "v2_contract_ready_for_source_freshness"
    assert manifest["source_freshness_regeneration_allowed_after_contract"] is True
    assert manifest["remote_packet_generation_allowed_after_source_freshness"] is True
    assert manifest["remote_preflight_allowed_now"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["next_action"] == "regenerate_source_freshness_then_remote_packet"
    assert manifest["blocker_count"] == 0
    assert manifest["blockers"] == []
    assert manifest["preflight_probe"]["preflight_status"] == "ready"
    assert manifest["preflight_probe"]["formal_trial_ready"] is True
    assert manifest["runner_command_contains_v2_params"] is True


def test_v2_contract_readiness_catches_missing_gap_ledger(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_readiness_gate")
    config = _config(builder, tmp_path, status="approved")
    config.gap_ledger_path.unlink()

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["blockers"]}
    assert manifest["status"] == "v2_contract_readiness_blocked"
    assert "gap_ledger_missing" in issue_ids


def test_v2_contract_readiness_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_readiness_gate")
    config = _config(builder, tmp_path, status="draft")
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
            "--contract-path",
            str(config.contract_path),
            "--gap-ledger",
            str(config.gap_ledger_path),
            "--attempt-dir",
            str(config.attempt_dir),
            "--oracle-path",
            str(config.oracle_path),
            "--bc-checkpoint",
            str(config.bc_checkpoint),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "v2_contract_readiness_blocked"
    assert "Module2 V2 Contract Readiness Gate" in markdown
    assert "not paper result material" in markdown
    assert "contract_status_not_approved_or_frozen" in markdown
    assert "local PPO training output" in markdown


def test_v2_contract_readiness_module_entrypoint_writes_outputs(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_v2_contract_readiness_gate")
    config = _config(builder, tmp_path, status="draft")
    manifest_path = tmp_path / "module_readiness.json"
    markdown_path = tmp_path / "module_readiness.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "forest_n3p.scripts.build_module2_v2_contract_readiness_gate",
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract-path",
            str(config.contract_path),
            "--gap-ledger",
            str(config.gap_ledger_path),
            "--attempt-dir",
            str(config.attempt_dir),
            "--oracle-path",
            str(config.oracle_path),
            "--bc-checkpoint",
            str(config.bc_checkpoint),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "v2_contract_readiness_blocked" in result.stdout
    assert json.loads(manifest_path.read_text(encoding="utf-8"))["status"] == "v2_contract_readiness_blocked"
    assert "Module2 V2 Contract Readiness Gate" in markdown_path.read_text(encoding="utf-8")


def _config(builder, tmp_path: Path, *, status: str):
    oracle_path = tmp_path / "oracle.parquet"
    bc_checkpoint = tmp_path / "checkpoint.pt"
    gap_ledger = tmp_path / "gap_ledger.md"
    oracle_path.write_bytes(b"fake-oracle")
    bc_checkpoint.write_bytes(b"fake-bc")
    gap_ledger.write_text("# Gap ledger\n", encoding="utf-8")
    return builder.Module2V2ContractReadinessGateConfig(
        output_dir=tmp_path / "out",
        contract_path=_write_contract(tmp_path / "contract.md", status=status),
        gap_ledger_path=gap_ledger,
        attempt_dir=tmp_path / "gate3_stronger_obstacle_summary_warm_start_v2_seed20260706",
        oracle_path=oracle_path,
        bc_checkpoint=bc_checkpoint,
    )


def _write_contract(path: Path, *, status: str) -> Path:
    path.write_text(
        f"""---
topic: module2-stronger_obstacle_summary_warm_start
status: {status}
version: v2-test
selected_protocol_lane: stronger_obstacle_summary_warm_start
contract_action: draft_new_contract
training_allowed: false
remote_training_allowed_now: false
local_training_allowed_now: false
formal_claim_allowed_now: false
paper_result_material_allowed_now: false
allowed_status_before_training:
  - approved
  - frozen
---

# Test Contract

The prior Gate3 evidence is 0.53125 against success_threshold=0.8.
The attempt path is gate3_stronger_obstacle_summary_warm_start_v2_seed20260706.
H02 must report formal_output_accepted=true before paper result material.
""",
        encoding="utf-8",
    )
    return path
