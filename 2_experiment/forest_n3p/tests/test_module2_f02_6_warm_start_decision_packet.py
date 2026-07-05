import json
from importlib import import_module


def test_f02_6_decision_packet_builds_evidence_bound_recommendation(tmp_path):
    try:
        packet = import_module("forest_n3p.scripts.build_module2_f02_6_warm_start_decision_packet")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing F02.6 decision packet builder: {exc}") from exc

    manifest_path = tmp_path / "f02_6_packet.json"
    markdown_path = tmp_path / "f02_6_packet.md"
    rc = packet.main(
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

    assert manifest["schema_version"] == 1
    assert manifest["packet_name"] == "module2_f02_6_warm_start_decision_packet"
    assert manifest["status"] == "pending_human_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["recommendation"]["decision"] == "approve_obstacle_summary_warm_start"
    assert manifest["recommendation"]["formal_claim_allowed"] is False
    assert "requires_dr_sun_approval" in manifest["blockers"]
    assert manifest["source_integrity_summary"]["source_count"] == 10
    assert manifest["source_integrity_summary"]["existing_source_count"] == 10
    assert manifest["source_integrity_summary"]["missing_source_count"] == 0
    assert manifest["source_integrity_summary"]["hash_record_count"] == 10
    assert manifest["source_integrity_summary"]["all_sources_present"] is True
    assert manifest["source_integrity_summary"]["all_existing_sources_hashed"] is True
    assert manifest["source_integrity_summary"]["source_issue_count"] == 0
    assert manifest["source_integrity_summary"]["missing_sources"] == []
    assert manifest["source_integrity_summary"]["unhashed_sources"] == []

    candidates = {candidate["candidate_id"]: candidate for candidate in manifest["candidates"]}
    assert set(candidates) == {"no_warm_start", "obstacle_summary_bc", "patch_scalar_cnn_bounded"}
    assert candidates["no_warm_start"]["formal_gate3"]["formal_decision"] == "fail"
    assert candidates["no_warm_start"]["formal_gate3"]["terminal_rs_success"] == 29
    assert candidates["no_warm_start"]["formal_gate3"]["episodes"] == 64
    assert candidates["obstacle_summary_bc"]["formal_v2_closed_loop"]["terminal_rs_success"] == 67
    assert candidates["obstacle_summary_bc"]["patch_bounded_closed_loop"]["terminal_rs_success"] == 101
    assert candidates["patch_scalar_cnn_bounded"]["patch_bounded_closed_loop"]["terminal_rs_success"] == 63

    remote = manifest["remote_readiness"]
    assert remote["gpu_alias"] == "gpu3070ti-relay"
    assert remote["no_warm_formal_preflight"]["formal_trial_ready"] is True
    assert remote["warm_start_formal_preflight"]["formal_trial_ready"] is False
    assert remote["warm_start_formal_preflight"]["blocker_codes"] == ["warm_start_decision_pending"]
    assert remote["warm_start_cuda_smoke"]["formal_decision"] == "not_formal"
    assert "warm_start_decision_pending" in remote["warm_start_cuda_smoke"]["blocker_codes"]

    assert manifest["next_actions"]["if_approved_obstacle_summary"]["runner_command"]
    assert "--bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt" in manifest["next_actions"]["if_approved_obstacle_summary"]["runner_command"]
    assert manifest["claim_boundaries"]
    assert "# Module2 F02.6 Warm-Start Decision Packet" in markdown
    assert "pending_human_decision" in markdown
    assert "approve_obstacle_summary_warm_start" in markdown
    assert "Source Integrity" in markdown
