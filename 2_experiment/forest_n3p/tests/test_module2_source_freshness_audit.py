import json
import subprocess
from importlib import import_module


def test_source_freshness_audit_records_stale_and_dirty_artifacts_as_regeneration_risks(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_source_freshness_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing source freshness audit builder: {exc}") from exc

    current_head = _current_head()
    dirty_path = _artifact(tmp_path, "dirty.json", status="blocked", source_head=f"{current_head}+dirty")
    missing_commit_path = _artifact(tmp_path, "missing_commit.json", status="blocked", source_head="0" * 40)
    no_head_path = _artifact(tmp_path, "no_head.json", status="blocked", source_head=None)

    manifest = builder.build_manifest(
        builder.SourceFreshnessAuditConfig(
            output_dir=tmp_path,
            artifacts=[
                builder.ArtifactTarget("current_dirty", "gate", dirty_path, "approved_remote_preflight"),
                builder.ArtifactTarget("missing_commit", "gate", missing_commit_path, "formal_h01_h02"),
                builder.ArtifactTarget("missing_source", "gate", no_head_path, "formal_claim_gate"),
            ],
        )
    )

    assert manifest["status"] == "source_freshness_risks_recorded_gate_still_blocked"
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["regeneration_required_before_remote_formal_execution"] is True
    assert manifest["risk_counts"]["current_dirty"] == 1
    assert manifest["risk_counts"]["unknown_or_missing_commit"] == 1
    assert manifest["risk_counts"]["missing_source_head"] == 1
    targets = {item["artifact_id"]: item for item in manifest["ordered_regeneration_targets"]}
    assert targets["current_dirty"]["required_before"] == "approved_remote_preflight"
    assert targets["missing_commit"]["required_before"] == "formal_h01_h02"
    assert targets["missing_source"]["required_before"] == "formal_claim_gate"
    assert "not a training run or paper result" in " ".join(manifest["claim_boundaries"])


def test_source_freshness_audit_is_clean_only_when_all_sources_match_current_head(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_source_freshness_audit")
    current_head = _current_head()
    clean_a = _artifact(tmp_path, "clean_a.json", status="ready", source_head=current_head)
    clean_b = _artifact(tmp_path, "clean_b.json", status="blocked", source_head=current_head)

    manifest = builder.build_manifest(
        builder.SourceFreshnessAuditConfig(
            output_dir=tmp_path,
            artifacts=[
                builder.ArtifactTarget("clean_a", "gate", clean_a, "approved_remote_preflight"),
                builder.ArtifactTarget("clean_b", "gate", clean_b, "formal_h01_h02"),
            ],
        )
    )

    assert manifest["status"] == "source_freshness_clean_current"
    assert manifest["risk_counts"] == {"current_clean": 2}
    assert manifest["ordered_regeneration_targets"] == []
    assert manifest["regeneration_required_before_remote_formal_execution"] is False


def test_source_freshness_audit_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_source_freshness_audit")
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["artifact_name"] == "module2_source_freshness_audit"
    assert manifest["runs_training"] is False
    artifact_ids = {record["artifact_id"] for record in manifest["artifact_records"]}
    assert "f02_6_decision_gate_audit" in artifact_ids
    assert "post_f02_6_plan_audit" in artifact_ids
    assert "remote_packet_safety_audit" in artifact_ids
    assert "formal_gate_missing_artifacts" in artifact_ids
    required_before = {target["artifact_id"]: target["required_before"] for target in manifest["ordered_regeneration_targets"]}
    assert required_before.get("f02_6_decision_gate_audit") == "approved_remote_preflight"
    assert required_before.get("post_f02_6_plan_audit") == "approved_remote_preflight"
    assert required_before.get("remote_packet_safety_audit") == "approved_remote_preflight"
    assert required_before.get("formal_gate_missing_artifacts") == "formal_claim_gate"
    assert "Module2 Source Freshness Audit" in markdown
    assert "not a training run" in markdown


def _artifact(tmp_path, name, *, status, source_head):
    path = tmp_path / name
    payload = {"status": status}
    if source_head is not None:
        payload["source_head"] = source_head
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _current_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
