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

    evidence_matrix = manifest["decision_evidence_matrix"]
    assert evidence_matrix["schema_version"] == 1
    assert evidence_matrix["matrix_id"] == "module2_f02_6_decision_evidence_matrix"
    assert evidence_matrix["status"] == "ready_for_dr_sun_decision_not_authorization"
    assert evidence_matrix["current_authorization_allowed_now"] is False
    assert evidence_matrix["remote_preflight_allowed_now"] is False
    assert evidence_matrix["remote_training_allowed_now"] is False
    assert evidence_matrix["local_training_allowed_now"] is False
    assert evidence_matrix["formal_claim_allowed_now"] is False
    assert evidence_matrix["paper_result_material_allowed_now"] is False
    assert evidence_matrix["source_issue_count"] == 0
    assert evidence_matrix["route_count"] == 2
    assert evidence_matrix["required_evidence_count"] == 7
    assert evidence_matrix["satisfied_required_evidence_count"] == 7
    assert evidence_matrix["missing_required_evidence_count"] == 0
    assert evidence_matrix["missing_required_evidence_ids"] == []
    assert "smoke result used as formal PPO checkpoint or Gate #3 evidence" in evidence_matrix["global_invalid_substitutes"]

    evidence_routes = {route["decision"]: route for route in evidence_matrix["routes"]}
    assert set(evidence_routes) == {
        "approve_obstacle_summary_warm_start",
        "reject_obstacle_summary_warm_start",
    }
    approve_route = evidence_routes["approve_obstacle_summary_warm_start"]
    assert approve_route["route_status"] == "decision_supported_not_authorized"
    assert approve_route["next_lane_after_record"] == "source_fresh_regeneration"
    assert approve_route["current_authorization_allowed_now"] is False
    assert approve_route["allows_remote_training_now"] is False
    assert approve_route["allows_formal_claim_now"] is False
    assert "remote CUDA smoke as formal evidence" in approve_route["invalid_substitutes"]
    approve_evidence = {item["evidence_id"]: item for item in approve_route["required_evidence"]}
    assert set(approve_evidence) == {
        "no_warm_formal_gate3_failure",
        "obstacle_summary_bc_candidate_readiness",
        "bounded_candidate_comparison_against_patch_cnn",
        "remote_route_guarded_until_decision",
    }
    assert approve_evidence["no_warm_formal_gate3_failure"]["observed"]["terminal_rs_success"] == 29
    assert approve_evidence["no_warm_formal_gate3_failure"]["satisfied"] is True
    assert "remote CUDA smoke audit" in approve_evidence["no_warm_formal_gate3_failure"]["invalid_substitutes"]
    assert approve_evidence["obstacle_summary_bc_candidate_readiness"]["observed"]["checkpoint_sha256"]
    assert "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt" in approve_evidence[
        "obstacle_summary_bc_candidate_readiness"
    ]["required_artifact_paths"]
    assert approve_evidence["bounded_candidate_comparison_against_patch_cnn"]["observed"]["obstacle_summary_terminal_rs_success"] == 101
    assert approve_evidence["bounded_candidate_comparison_against_patch_cnn"]["observed"]["patch_scalar_cnn_terminal_rs_success"] == 63
    assert approve_evidence["remote_route_guarded_until_decision"]["observed"]["warm_start_formal_trial_ready"] is False
    assert "warm_start_decision_pending" in approve_evidence["remote_route_guarded_until_decision"]["observed"]["warm_start_blocker_codes"]
    for route in evidence_routes.values():
        assert route["current_authorization_allowed_now"] is False
        assert route["allows_local_training_now"] is False
        assert route["allows_remote_preflight_now"] is False
        assert route["allows_remote_training_now"] is False
        assert route["allows_formal_claim_now"] is False
        assert route["missing_required_evidence_ids"] == []
        assert route["invalid_substitutes"]
        for evidence in route["required_evidence"]:
            assert evidence["required_artifact_paths"]
            assert evidence["invalid_substitutes"]
            assert evidence["satisfied"] is True

    reject_route = evidence_routes["reject_obstacle_summary_warm_start"]
    assert reject_route["route_status"] == "redesign_route_defined_not_authorized"
    assert reject_route["next_lane_after_record"] == "protocol_redesign"
    assert reject_route["next_protocol"] == "stronger/full patch-CNN warm-start protocol"
    assert "new_or_revised_research_contract" in reject_route["required_next_artifacts"]
    assert "protocol redesign without revised contract" in reject_route["invalid_substitutes"]
    reject_evidence = {item["evidence_id"]: item for item in reject_route["required_evidence"]}
    assert set(reject_evidence) == {
        "reject_route_defined_in_decision_intake",
        "reject_route_does_not_relabel_no_warm_failure",
        "reject_route_requires_stronger_protocol_before_training",
    }

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
    assert "Decision Evidence Matrix" in markdown
    assert "matrix_status: `ready_for_dr_sun_decision_not_authorization`" in markdown
    assert "approve_obstacle_summary_warm_start" in markdown
    assert "reject_obstacle_summary_warm_start" in markdown
    assert "evidence_id: `remote_route_guarded_until_decision`" in markdown
    assert "invalid_substitutes" in markdown
    assert "Source Integrity" in markdown
    assert "Post-Approval Remote-Only Command Candidate" in markdown
    assert "current_authorization_allowed_now: `False`" in markdown
    assert "execution_host_required: `gpu3070ti-relay`" in markdown
    assert "local_execution_allowed: `False`" in markdown
    assert "requires_approved_remote_preflight: `True`" in markdown
    assert "ssh gpu3070ti-relay" in markdown
    assert "Next Command If Approved" not in markdown
