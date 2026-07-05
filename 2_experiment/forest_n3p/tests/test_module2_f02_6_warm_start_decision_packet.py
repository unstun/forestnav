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
    assert manifest["remote_preflight_allowed"] is False
    assert manifest["remote_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["recommendation"]["decision"] == "approve_obstacle_summary_warm_start"
    assert manifest["recommendation"]["formal_claim_allowed"] is False
    assert "requires_dr_sun_approval" in manifest["blockers"]
    authorization = manifest["current_authorization"]
    assert authorization["authorization_status"] == "blocked_until_dr_sun_decision"
    assert authorization["decision_owner_required"] == "Dr Sun"
    assert authorization["decision_record"]["status"] == "pending_human_decision"
    assert authorization["decision_record"]["requested_decision"] == "pending"
    assert authorization["decision_record"]["effective_warm_start_decision"] == "pending"
    assert authorization["decision_record"]["decider"] is None
    assert authorization["decision_record"]["decision_note_present"] is False
    assert authorization["decision_intake"]["status"] == "f02_6_decision_intake_pending_clean"
    assert authorization["decision_intake"]["next_blocked_lane"] == "decision"
    assert authorization["decision_intake"]["audit_issue_count"] == 0
    assert authorization["decision_intake"]["valid_decision_count"] == 2
    assert authorization["decision_intake"]["required_record_field_count"] == 3
    assert authorization["decision_intake"]["post_decision_route_count"] == 2
    assert authorization["decision_intake"]["post_decision_non_authorization_count"] == 4
    assert authorization["current_allowed_action_ids"] == ["record_f02_6_decision"]
    assert authorization["current_blocked_action_ids"] == [
        "remote_preflight",
        "remote_training",
        "local_training",
        "formal_claim",
        "paper_result_material",
    ]
    assert authorization["post_decision_routes_are_current_authorization"] is False
    assert authorization["remote_preflight_allowed_now"] is False
    assert authorization["remote_training_allowed_now"] is False
    assert authorization["local_training_allowed_now"] is False
    assert authorization["formal_claim_allowed_now"] is False
    assert authorization["paper_result_material_allowed_now"] is False
    assert manifest["source_integrity_summary"]["source_count"] == 12
    assert manifest["source_integrity_summary"]["existing_source_count"] == 12
    assert manifest["source_integrity_summary"]["missing_source_count"] == 0
    assert manifest["source_integrity_summary"]["hash_record_count"] == 12
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

    approved_action = manifest["next_actions"]["if_approved_obstacle_summary"]
    assert approved_action["command_kind"] == "post_approval_remote_training_candidate"
    assert approved_action["host"] == "gpu3070ti-relay"
    assert approved_action["remote_cwd"] == "~/ForestNav"
    assert approved_action["runner_command"]
    assert approved_action["remote_runner_command"].startswith("ssh gpu3070ti-relay ")
    assert "cd ~/ForestNav && python -m forest_n3p.scripts.run_rl_rs_gate3_trial" in approved_action["remote_runner_command"]
    assert "--bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt" in approved_action["runner_command"]
    assert approved_action["current_authorization_allowed_now"] is False
    assert approved_action["local_execution_allowed"] is False
    assert approved_action["remote_preflight_allowed_now"] is False
    assert approved_action["remote_training_allowed_now"] is False
    assert approved_action["formal_claim_allowed_now"] is False
    assert approved_action["requires_dr_sun_decision_record"] is True
    assert approved_action["requires_source_fresh_regeneration"] is True
    assert approved_action["requires_post_f02_6_plan_audit"] is True
    assert approved_action["requires_approved_remote_preflight"] is True
    assert manifest["claim_boundaries"]
    assert any("must not be run on the local Mac" in boundary for boundary in manifest["claim_boundaries"])
    assert "# Module2 F02.6 Warm-Start Decision Packet" in markdown
    assert "pending_human_decision" in markdown
    assert "approve_obstacle_summary_warm_start" in markdown
    assert "Current Authorization" in markdown
    assert "authorization_status: `blocked_until_dr_sun_decision`" in markdown
    assert "allowed_now: `record_f02_6_decision`" in markdown
    assert "blocked_now: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`" in markdown
    assert "remote preflight allowed now: `False`" in markdown
    assert "remote training allowed now: `False`" in markdown
    assert "Source Integrity" in markdown
    assert "Post-Approval Remote-Only Command Candidate" in markdown
    assert "current_authorization_allowed_now: `False`" in markdown
    assert "execution_host_required: `gpu3070ti-relay`" in markdown
    assert "local_execution_allowed: `False`" in markdown
    assert "requires_approved_remote_preflight: `True`" in markdown
    assert "ssh gpu3070ti-relay" in markdown
    assert "Next Command If Approved" not in markdown
