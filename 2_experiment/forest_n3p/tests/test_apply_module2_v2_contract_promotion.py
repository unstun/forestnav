import json
from importlib import import_module
from pathlib import Path


def test_contract_promotion_dry_run_builds_promoted_text_without_writing(tmp_path):
    applier = import_module("forest_n3p.scripts.apply_module2_v2_contract_promotion")
    contract = _write_contract(tmp_path / "contract.md")
    args = applier._parse_args(
        [
            "--contract-path",
            str(contract),
            "--promotion-packet",
            str(_write_packet(tmp_path / "packet.json")),
            "--status",
            "approved",
            "--decider",
            "Dr Sun",
            "--remote-alias",
            "gpu3070ti-relay",
            "--confirm-training-budget",
            "--confirm-unsafe-failure-thresholds",
            "--dry-run",
        ]
    )

    result = applier.build_promotion_result(args)

    assert result["status"] == "promotion_apply_ready"
    assert result["dry_run"] is True
    assert result["writes_contract"] is False
    assert result["promotion_apply_allowed"] is True
    assert result["blockers"] == []
    assert result["target_contract_status"] == "approved"
    assert "status: approved" in result["promoted_contract_text"]
    assert "promotion_decider: Dr Sun" in result["promoted_contract_text"]
    assert "approved_remote_alias: gpu3070ti-relay" in result["promoted_contract_text"]
    assert "contract_approved_for_source_freshness: true" in result["promoted_contract_text"]
    assert "status: draft" in contract.read_text(encoding="utf-8")


def test_contract_promotion_blocks_without_required_confirmations(tmp_path):
    applier = import_module("forest_n3p.scripts.apply_module2_v2_contract_promotion")
    args = applier._parse_args(
        [
            "--contract-path",
            str(_write_contract(tmp_path / "contract.md")),
            "--promotion-packet",
            str(_write_packet(tmp_path / "packet.json")),
            "--status",
            "approved",
            "--decider",
            "Agent",
            "--remote-alias",
            "gpu3070ti-reply",
            "--dry-run",
        ]
    )

    result = applier.build_promotion_result(args)

    issue_ids = {issue["issue_id"] for issue in result["blockers"]}
    assert result["status"] == "promotion_apply_blocked"
    assert "decider_not_dr_sun" in issue_ids
    assert "remote_alias_not_recommended" in issue_ids
    assert "training_budget_not_confirmed" in issue_ids
    assert "unsafe_failure_thresholds_not_confirmed" in issue_ids


def test_contract_promotion_cli_dry_run_writes_manifest_only(tmp_path):
    applier = import_module("forest_n3p.scripts.apply_module2_v2_contract_promotion")
    contract = _write_contract(tmp_path / "contract.md")
    manifest = tmp_path / "dry_run.json"

    rc = applier.main(
        [
            "--contract-path",
            str(contract),
            "--promotion-packet",
            str(_write_packet(tmp_path / "packet.json")),
            "--status",
            "approved",
            "--decider",
            "Dr Sun",
            "--remote-alias",
            "gpu3070ti-relay",
            "--confirm-training-budget",
            "--confirm-unsafe-failure-thresholds",
            "--dry-run",
            "--manifest-out",
            str(manifest),
        ]
    )

    assert rc == 0
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["status"] == "promotion_apply_ready"
    assert data["writes_contract"] is False
    assert "status: draft" in contract.read_text(encoding="utf-8")


def test_contract_promotion_apply_writes_contract_when_not_dry_run(tmp_path):
    applier = import_module("forest_n3p.scripts.apply_module2_v2_contract_promotion")
    contract = _write_contract(tmp_path / "contract.md")

    rc = applier.main(
        [
            "--contract-path",
            str(contract),
            "--promotion-packet",
            str(_write_packet(tmp_path / "packet.json")),
            "--status",
            "frozen",
            "--decider",
            "Dr Sun",
            "--remote-alias",
            "gpu3070ti-relay",
            "--confirm-training-budget",
            "--confirm-unsafe-failure-thresholds",
        ]
    )

    assert rc == 0
    text = contract.read_text(encoding="utf-8")
    assert "status: frozen" in text
    assert "promotion_decider: Dr Sun" in text


def _write_contract(path: Path) -> Path:
    path.write_text(
        """---
topic: module2-stronger_obstacle_summary_warm_start
status: draft
selected_protocol_lane: stronger_obstacle_summary_warm_start
contract_action: draft_new_contract
training_allowed: false
remote_training_allowed_now: false
local_training_allowed_now: false
allowed_status_before_training:
  - approved
  - frozen
---

# Contract
""",
        encoding="utf-8",
    )
    return path


def _write_packet(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "status": "v2_contract_promotion_packet_ready_awaiting_dr_sun",
                "audit_issue_count": 0,
                "remote_alias_evidence": {"recommended_alias": "gpu3070ti-relay"},
            }
        ),
        encoding="utf-8",
    )
    return path
