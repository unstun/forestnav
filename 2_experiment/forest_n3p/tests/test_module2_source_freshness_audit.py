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
    assert targets["current_dirty"]["source_head"] == f"{current_head}+dirty"
    assert targets["current_dirty"]["source_commit"] == current_head
    assert targets["current_dirty"]["source_head_dirty"] is True
    assert targets["current_dirty"]["source_commit_exists"] is True
    assert targets["current_dirty"]["matches_current_head"] is True
    assert targets["current_dirty"]["current_head"] == current_head
    assert targets["missing_commit"]["required_before"] == "formal_h01_h02"
    assert targets["missing_commit"]["source_commit_exists"] is False
    assert targets["missing_source"]["required_before"] == "formal_claim_gate"
    assert targets["missing_source"]["source_head"] is None
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


def test_source_freshness_audit_records_commit_lag_diagnostics(tmp_path, monkeypatch):
    builder = import_module("forest_n3p.scripts.build_module2_source_freshness_audit")
    stale_head = "a" * 40
    current_head = "b" * 40
    stale_path = _artifact(tmp_path, "stale.json", status="blocked", source_head=stale_head)

    monkeypatch.setattr(builder, "_current_head", lambda: current_head)
    monkeypatch.setattr(builder, "_commit_exists", lambda commit: commit in {stale_head, current_head})
    monkeypatch.setattr(builder, "_commits_since_source", lambda source, current: 3, raising=False)
    monkeypatch.setattr(
        builder,
        "_changed_paths_since_source",
        lambda source, current: [str(stale_path), "2_experiment/forest_n3p/example.py"],
        raising=False,
    )

    manifest = builder.build_manifest(
        builder.SourceFreshnessAuditConfig(
            output_dir=tmp_path,
            artifacts=[
                builder.ArtifactTarget("stale_gate", "gate", stale_path, "approved_remote_preflight"),
            ],
        )
    )

    assert manifest["commit_lag_summary"] == {
        "records_with_commit_lag": 1,
        "records_with_unknown_commit_lag": 0,
        "records_with_changed_paths_since_source": 1,
        "records_with_artifact_path_changed_since_source": 1,
        "records_with_non_self_changed_paths_since_source": 1,
        "records_with_self_artifact_only_lag": 0,
        "max_commits_since_source": 3,
        "max_non_self_changed_path_count_since_source": 1,
        "changed_path_sample_limit": 12,
    }
    record = manifest["artifact_records"][0]
    assert record["freshness_state"] == "historical_clean"
    assert record["commits_since_source"] == 3
    assert record["changed_path_count_since_source"] == 2
    assert record["artifact_path_changed_since_source"] is True
    assert record["self_artifact_changed_path_count_since_source"] == 1
    assert record["non_self_changed_path_count_since_source"] == 1
    assert record["self_artifact_only_lag"] is False
    assert record["non_self_changed_paths_since_source_sample"] == ["2_experiment/forest_n3p/example.py"]
    assert record["changed_paths_since_source_sample"] == [str(stale_path), "2_experiment/forest_n3p/example.py"]
    target = manifest["ordered_regeneration_targets"][0]
    assert target["commits_since_source"] == 3
    assert target["changed_path_count_since_source"] == 2
    assert target["artifact_path_changed_since_source"] is True
    assert target["non_self_changed_path_count_since_source"] == 1
    assert target["self_artifact_only_lag"] is False


def test_source_freshness_audit_separates_self_artifact_write_lag(tmp_path, monkeypatch):
    builder = import_module("forest_n3p.scripts.build_module2_source_freshness_audit")
    stale_head = "a" * 40
    current_head = "b" * 40
    artifact_path = _artifact(tmp_path, "audit.json", status="blocked", source_head=stale_head)
    artifact_markdown = artifact_path.with_suffix(".md")

    monkeypatch.setattr(builder, "_current_head", lambda: current_head)
    monkeypatch.setattr(builder, "_commit_exists", lambda commit: commit in {stale_head, current_head})
    monkeypatch.setattr(builder, "_commits_since_source", lambda source, current: 1, raising=False)
    monkeypatch.setattr(
        builder,
        "_changed_paths_since_source",
        lambda source, current: [str(artifact_path), str(artifact_markdown)],
        raising=False,
    )

    manifest = builder.build_manifest(
        builder.SourceFreshnessAuditConfig(
            output_dir=tmp_path,
            artifacts=[
                builder.ArtifactTarget("self_written_audit", "gate", artifact_path, "approved_remote_preflight"),
            ],
        )
    )

    assert manifest["commit_lag_summary"]["records_with_self_artifact_only_lag"] == 1
    assert manifest["commit_lag_summary"]["records_with_non_self_changed_paths_since_source"] == 0
    assert manifest["commit_lag_summary"]["max_non_self_changed_path_count_since_source"] == 0
    record = manifest["artifact_records"][0]
    assert record["commits_since_source"] == 1
    assert record["changed_path_count_since_source"] == 2
    assert record["artifact_path_changed_since_source"] is True
    assert record["self_artifact_changed_path_count_since_source"] == 2
    assert record["non_self_changed_path_count_since_source"] == 0
    assert record["self_artifact_only_lag"] is True
    assert record["non_self_changed_paths_since_source_sample"] == []


def test_source_freshness_audit_documents_self_artifact_lag_policy(tmp_path, monkeypatch):
    builder = import_module("forest_n3p.scripts.build_module2_source_freshness_audit")
    current_head = "c" * 40
    clean_path = _artifact(tmp_path, "clean.json", status="ready", source_head=current_head)

    monkeypatch.setattr(builder, "_current_head", lambda: current_head)
    monkeypatch.setattr(builder, "_source_head", lambda: current_head)
    monkeypatch.setattr(builder, "_commit_exists", lambda commit: commit == current_head)

    manifest = builder.build_manifest(
        builder.SourceFreshnessAuditConfig(
            output_dir=tmp_path,
            manifest_out=tmp_path / "audit.json",
            markdown_out=tmp_path / "audit.md",
            artifacts=[
                builder.ArtifactTarget("clean_gate", "gate", clean_path, "approved_remote_preflight"),
            ],
        )
    )

    policy = manifest["audit_self_reference_policy"]
    assert policy == {
        "source_head_scope": "generation_time_repository_head",
        "commit_storing_this_audit_known_at_generation": False,
        "expected_post_commit_self_lag": True,
        "self_lag_is_formal_gate_blocker": False,
        "manifest_path": str(tmp_path / "audit.json"),
        "markdown_path": str(tmp_path / "audit.md"),
    }
    assert manifest["status"] == "source_freshness_clean_current"
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
    records = {record["artifact_id"]: record for record in manifest["artifact_records"]}
    artifact_ids = set(records)
    assert "f02_6_warm_start_decision_packet" in artifact_ids
    assert "f02_6_decision_intake" in artifact_ids
    assert "f02_6_decision_gate_audit" in artifact_ids
    assert "f02_6_transition_gate_audit" in artifact_ids
    assert "formal_gate_closure_checklist" in artifact_ids
    assert "post_f02_6_regeneration_plan" in artifact_ids
    assert "post_f02_6_plan_audit" in artifact_ids
    assert "remote_packet_safety_audit" in artifact_ids
    assert "claim_safety" in artifact_ids
    assert "paper_readiness" in artifact_ids
    assert "formal_gate_missing_artifacts" in artifact_ids
    assert "formal_gate_status_report" in artifact_ids
    assert "formal_gate_remaining_deliverables" in artifact_ids
    assert "formal_gate_proof_audit" in artifact_ids
    assert "formal_gate_proof_summary_chain_audit" in artifact_ids
    assert "formal_gate_handoff_bundle" in artifact_ids
    assert records["f02_6_warm_start_decision_packet"]["required_before"] == "approved_remote_preflight"
    assert records["f02_6_decision_intake"]["required_before"] == "approved_remote_preflight"
    assert records["f02_6_transition_gate_audit"]["required_before"] == "approved_remote_preflight"
    assert records["formal_gate_closure_checklist"]["required_before"] == "approved_remote_preflight"
    assert records["post_f02_6_regeneration_plan"]["required_before"] == "approved_remote_preflight"
    assert records["post_f02_6_plan_audit"]["required_before"] == "approved_remote_preflight"
    assert records["remote_packet_safety_audit"]["required_before"] == "approved_remote_preflight"
    assert records["formal_gate_handoff_bundle"]["required_before"] == "approved_remote_preflight"
    assert records["claim_safety"]["required_before"] == "formal_claim_gate"
    assert records["paper_readiness"]["required_before"] == "formal_claim_gate"
    assert records["formal_gate_status_report"]["required_before"] == "formal_claim_gate"
    assert records["formal_gate_remaining_deliverables"]["required_before"] == "formal_claim_gate"
    assert records["formal_gate_proof_audit"]["required_before"] == "formal_claim_gate"
    assert records["formal_gate_proof_summary_chain_audit"]["required_before"] == "formal_claim_gate"
    required_before = {target["artifact_id"]: target["required_before"] for target in manifest["ordered_regeneration_targets"]}
    if records["f02_6_warm_start_decision_packet"]["freshness_state"] != "current_clean":
        assert required_before.get("f02_6_warm_start_decision_packet") == "approved_remote_preflight"
    assert required_before.get("f02_6_decision_intake") == "approved_remote_preflight"
    assert required_before.get("f02_6_decision_gate_audit") == "approved_remote_preflight"
    assert required_before.get("f02_6_transition_gate_audit") == "approved_remote_preflight"
    if records["formal_gate_closure_checklist"]["freshness_state"] != "current_clean":
        assert required_before.get("formal_gate_closure_checklist") == "approved_remote_preflight"
    if records["post_f02_6_regeneration_plan"]["freshness_state"] != "current_clean":
        assert required_before.get("post_f02_6_regeneration_plan") == "approved_remote_preflight"
    if records["post_f02_6_plan_audit"]["freshness_state"] != "current_clean":
        assert required_before.get("post_f02_6_plan_audit") == "approved_remote_preflight"
    if records["remote_packet_safety_audit"]["freshness_state"] != "current_clean":
        assert required_before.get("remote_packet_safety_audit") == "approved_remote_preflight"
    assert required_before.get("formal_gate_handoff_bundle") == "approved_remote_preflight"
    if records["claim_safety"]["freshness_state"] != "current_clean":
        assert required_before.get("claim_safety") == "formal_claim_gate"
    if records["paper_readiness"]["freshness_state"] != "current_clean":
        assert required_before.get("paper_readiness") == "formal_claim_gate"
    assert required_before.get("formal_gate_missing_artifacts") == "formal_claim_gate"
    assert required_before.get("formal_gate_remaining_deliverables") == "formal_claim_gate"
    assert required_before.get("formal_gate_proof_audit") == "formal_claim_gate"
    assert required_before.get("formal_gate_proof_summary_chain_audit") == "formal_claim_gate"
    if records["formal_gate_status_report"]["freshness_state"] != "current_clean":
        assert required_before.get("formal_gate_status_report") == "formal_claim_gate"
    assert "Module2 Source Freshness Audit" in markdown
    assert "not a training run" in markdown
    assert "source_head=" in markdown
    assert "current_head=" in markdown


def _artifact(tmp_path, name, *, status, source_head):
    path = tmp_path / name
    payload = {"status": status}
    if source_head is not None:
        payload["source_head"] = source_head
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _current_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
