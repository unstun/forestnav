import json
from importlib import import_module


def test_post_f02_6_regeneration_plan_blocks_current_pending_decision_without_execution(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing post-F02.6 regeneration plan builder: {exc}") from exc

    manifest = builder.build_manifest(
        builder.PostF026RegenerationPlanConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="pending_human_decision"),
            formal_gate_path=_formal_gate(tmp_path, decision_status="pending_human_decision"),
            source_freshness_path=_source_freshness(tmp_path, required=True),
            remote_packet_path=_remote_packet(tmp_path, ready=False),
            remaining_deliverables_path=_remaining_deliverables(tmp_path, open_gaps=True),
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_post_f02_6_regeneration_plan"
    assert manifest["status"] == "blocked_until_f02_6_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["blocking_summary"]["training_allowed_now"] is False
    assert manifest["blocking_summary"]["remote_preflight_allowed_now"] is False
    assert manifest["remaining_deliverables_gap_summary"]["present"] is True
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 4
    assert manifest["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] == 3

    stages = {stage["stage_id"]: stage for stage in manifest["ordered_stages"]}
    assert stages["f02_6_decision_record"]["requires_human_input"] is True
    assert stages["f02_6_decision_record"]["allowed_now"] is True
    assert stages["approved_remote_preflight"]["allowed_now"] is False
    assert "f02_6_decision_not_approved" in stages["approved_remote_preflight"]["blocked_by"]
    assert "source_fresh_preflight_targets_open" in stages["approved_remote_preflight"]["blocked_by"]
    assert stages["gate3_remote_training"]["runs_training"] is True
    assert stages["gate3_remote_training"]["allowed_now"] is False
    assert "f02_6_decision_not_approved" in stages["gate3_remote_training"]["blocked_by"]
    assert "source_fresh_preflight_targets_open" in stages["gate3_remote_training"]["blocked_by"]
    assert "remote_packet_not_ready" in stages["gate3_remote_training"]["blocked_by"]


def test_post_f02_6_regeneration_plan_allows_only_regeneration_after_approval_when_source_is_stale(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan")

    manifest = builder.build_manifest(
        builder.PostF026RegenerationPlanConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="approved"),
            formal_gate_path=_formal_gate(tmp_path, decision_status="approved"),
            source_freshness_path=_source_freshness(tmp_path, required=True),
            remote_packet_path=_remote_packet(tmp_path, ready=False),
            remaining_deliverables_path=_remaining_deliverables(tmp_path, open_gaps=True),
        )
    )

    assert manifest["status"] == "ready_to_execute_post_f02_6_regeneration_plan"
    stages = {stage["stage_id"]: stage for stage in manifest["ordered_stages"]}
    assert stages["regenerate_preflight_gate_artifacts"]["allowed_now"] is True
    assert stages["regenerate_preflight_gate_artifacts"]["runs_training"] is False
    joined_commands = "\n".join(stages["regenerate_preflight_gate_artifacts"]["command_templates"])
    assert "build_module2_f02_6_warm_start_decision_packet" in joined_commands
    assert "build_module2_f02_6_decision_gate_audit" in joined_commands
    assert "build_module2_f02_6_transition_gate_audit" in joined_commands
    assert "build_module2_formal_gate_closure_checklist" in joined_commands
    assert "build_module2_formal_gate_gap_audit" in joined_commands
    assert "build_module2_remote_formal_execution_packet" in joined_commands
    assert "build_module2_remote_packet_safety_audit" in joined_commands
    assert "build_module2_formal_gate_handoff_bundle" in joined_commands
    assert "build_module2_f02_6_decision_intake" in joined_commands
    assert "build_module2_post_f02_6_regeneration_plan" in joined_commands
    assert "build_module2_post_f02_6_plan_audit" in joined_commands
    assert "manual read-only gpu3070ti readiness refresh" in joined_commands
    command_index = {entry["artifact_id"]: entry for entry in manifest["source_regeneration_command_index"]}
    assert command_index["f02_6_warm_start_decision_packet"]["stage_id"] == "regenerate_preflight_gate_artifacts"
    assert (
        "build_module2_f02_6_warm_start_decision_packet"
        in command_index["f02_6_warm_start_decision_packet"]["command_template"]
    )
    assert command_index["f02_6_decision_intake"]["stage_id"] == "regenerate_preflight_gate_artifacts"
    assert "build_module2_f02_6_decision_intake" in command_index["f02_6_decision_intake"]["command_template"]
    assert command_index["post_f02_6_regeneration_plan"]["stage_id"] == "regenerate_preflight_gate_artifacts"
    assert "build_module2_post_f02_6_regeneration_plan" in command_index["post_f02_6_regeneration_plan"]["command_template"]
    assert command_index["formal_gate_status_report"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert "build_module2_formal_gate_status_report" in command_index["formal_gate_status_report"]["command_template"]
    assert command_index["formal_gate_remaining_deliverables"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert "build_module2_formal_gate_remaining_deliverables" in command_index["formal_gate_remaining_deliverables"]["command_template"]
    assert command_index["formal_gate_proof_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert "build_module2_formal_gate_proof_audit" in command_index["formal_gate_proof_audit"]["command_template"]
    assert command_index["formal_gate_proof_summary_chain_audit"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert (
        "build_module2_formal_gate_proof_summary_chain_audit"
        in command_index["formal_gate_proof_summary_chain_audit"]["command_template"]
    )
    assert command_index["h02_formal_acceptance"]["stage_id"] == "regenerate_h01_h02_formal_artifacts"
    assert "build_module2_h02_formal_acceptance" in command_index["h02_formal_acceptance"]["command_template"]
    assert command_index["paper_readiness"]["stage_id"] == "regenerate_claim_gate_artifacts"
    assert "build_module2_paper_readiness" in command_index["paper_readiness"]["command_template"]
    assert all(entry["command_kind"] != "unknown_manual" for entry in command_index.values())
    assert stages["approved_remote_preflight"]["allowed_now"] is False
    assert stages["approved_remote_preflight"]["runs_remote_preflight"] is True
    assert "source_fresh_preflight_targets_open" in stages["approved_remote_preflight"]["blocked_by"]
    assert stages["gate3_remote_training"]["allowed_now"] is False
    assert "source_fresh_preflight_targets_open" in stages["gate3_remote_training"]["blocked_by"]


def test_post_f02_6_regeneration_plan_marks_remote_training_ready_only_from_ready_packet_and_clean_sources(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan")

    manifest = builder.build_manifest(
        builder.PostF026RegenerationPlanConfig(
            output_dir=tmp_path,
            decision_record_path=_decision_record(tmp_path, status="approved"),
            formal_gate_path=_formal_gate(tmp_path, decision_status="approved"),
            source_freshness_path=_source_freshness(tmp_path, required=False),
            remote_packet_path=_remote_packet(tmp_path, ready=True),
            remaining_deliverables_path=_remaining_deliverables(tmp_path, open_gaps=False),
        )
    )

    assert manifest["status"] == "ready_for_remote_training_packet_execution"
    assert manifest["runs_training"] is False
    stages = {stage["stage_id"]: stage for stage in manifest["ordered_stages"]}
    assert stages["approved_remote_preflight"]["allowed_now"] is True
    assert stages["gate3_remote_training"]["allowed_now"] is True
    assert stages["gate3_remote_training"]["runs_training"] is True
    assert stages["gate3_remote_training"]["host"] == "gpu3070ti-relay"
    assert "ssh gpu3070ti-relay" in "\n".join(stages["gate3_remote_training"]["command_templates"])
    assert manifest["blocking_summary"]["training_allowed_now"] is True


def test_post_f02_6_regeneration_plan_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan")
    manifest_path = tmp_path / "plan.json"
    markdown_path = tmp_path / "plan.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--decision-record",
            str(_decision_record(tmp_path, status="pending_human_decision")),
            "--formal-gate",
            str(_formal_gate(tmp_path, decision_status="pending_human_decision")),
            "--source-freshness-audit",
            str(_source_freshness(tmp_path, required=True)),
            "--remote-packet",
            str(_remote_packet(tmp_path, ready=False)),
            "--remaining-deliverables",
            str(_remaining_deliverables(tmp_path, open_gaps=True)),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["artifact_name"] == "module2_post_f02_6_regeneration_plan"
    assert manifest["status"] == "blocked_until_f02_6_decision"
    assert "Module2 Post-F02.6 Regeneration Plan" in markdown
    assert "Source Regeneration Command Index" in markdown
    assert "Remaining Deliverables Gap Summary" in markdown
    assert "build_module2_f02_6_decision_intake" in markdown
    assert "does not execute commands" in markdown


def _decision_record(tmp_path, *, status):
    path = tmp_path / f"decision_{status}.json"
    approved = status == "approved"
    path.write_text(
        json.dumps(
            {
                "status": status,
                "effective_warm_start_decision": "approved_obstacle_summary" if approved else "pending",
                "remote_training_allowed": approved,
                "local_training_allowed": False,
                "formal_claim_allowed": False,
                "blockers": [] if approved else ["requires_dr_sun_approval"],
                "conditional_actions": {
                    "if_approved_obstacle_summary": {
                        "host": "gpu3070ti-relay",
                        "preflight_command": (
                            "python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial "
                            "--output-dir 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1 "
                            "--warm-start-decision approved_obstacle_summary --device cuda"
                        ),
                        "runner_command_after_ready_preflight": "python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda",
                        "audit_command_after_ready_preflight": "python -m forest_n3p.scripts.audit_rl_rs_gate3_trial",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _remaining_deliverables(tmp_path, *, open_gaps):
    path = tmp_path / f"remaining_deliverables_{open_gaps}.json"
    categories = [
        _gap_category("training", 3, "gate3_remote_training"),
        _gap_category("evaluation", 2, "gate3_remote_audit_pullback"),
        _gap_category("acceptance", 3, "gate3_remote_audit_pullback"),
        _gap_category("formal_acceptance", 2, "regenerate_h01_h02_formal_artifacts"),
    ]
    if not open_gaps:
        categories = [_gap_category(item["category"], 0, item["responsible_stage_id"], allowed=True) for item in categories]
    path.write_text(
        json.dumps(
            {
                "deliverable_gap_summary": {
                    "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
                    "execution_boundary": "read_only_no_execution",
                    "not_paper_result_material": True,
                    "total_missing_deliverables": 10 if open_gaps else 0,
                    "open_category_count": 4 if open_gaps else 0,
                    "category_order": ["training", "evaluation", "acceptance", "formal_acceptance"],
                    "categories": categories,
                }
            }
        ),
        encoding="utf-8",
    )
    return path


def _gap_category(category, missing_count, stage_id, *, allowed=False):
    return {
        "category": category,
        "status": "blocked" if missing_count else "complete",
        "missing_count": missing_count,
        "present_count": 0,
        "responsible_stage_id": stage_id,
        "responsible_stage_allowed_now": allowed,
        "responsible_stage_blocked_by": [] if allowed else ["f02_6_decision_not_approved"],
        "missing_artifacts": [
            {"matrix_id": f"{category}:artifact_{index}", "artifact_id": f"artifact_{index}"}
            for index in range(missing_count)
        ],
    }


def _formal_gate(tmp_path, *, decision_status):
    path = tmp_path / f"formal_gate_{decision_status}.json"
    path.write_text(
        json.dumps(
            {
                "status": "blocked_formal_gate_gaps_open",
                "current_gate_state": {
                    "f02_6_decision_status": decision_status,
                    "formal_performance_claim_allowed": False,
                },
                "ordered_next_steps": [
                    {
                        "step_id": "remote_preflight",
                        "blocked_by": ["source_freshness_regeneration_required"],
                    },
                    {
                        "step_id": "gate3_remote_training",
                        "blocked_by": ["source_freshness_regeneration_required", "remote_training_packet_not_ready"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _source_freshness(tmp_path, *, required):
    path = tmp_path / f"source_freshness_{required}.json"
    targets = [
        {
            "artifact_id": "f02_6_warm_start_decision_packet",
            "path": "0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "f02_6_decision_record",
            "path": "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "f02_6_decision_intake",
            "path": "0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "f02_6_decision_gate_audit",
            "path": "0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "f02_6_transition_gate_audit",
            "path": "0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "formal_gate_gap_audit",
            "path": "0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "formal_gate_closure_checklist",
            "path": "0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "gpu3070ti_readiness_refresh",
            "path": "0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json",
            "freshness_state": "historical_clean",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "remote_formal_execution_packet",
            "path": "0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "remote_packet_safety_audit",
            "path": "0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "post_f02_6_regeneration_plan",
            "path": "0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "post_f02_6_plan_audit",
            "path": "0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "formal_gate_handoff_bundle",
            "path": "0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json",
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "h01_evaluation_manifest",
            "path": "0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_h01_h02",
        },
        {
            "artifact_id": "h02_formal_acceptance",
            "path": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_h01_h02",
        },
        {
            "artifact_id": "claim_safety",
            "path": "0_trials/module2_claim_safety/module2_claim_safety.json",
            "freshness_state": "historical_clean",
            "required_before": "formal_claim_gate",
        },
        {
            "artifact_id": "formal_gate_status_report",
            "path": "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_claim_gate",
        },
        {
            "artifact_id": "formal_gate_remaining_deliverables",
            "path": "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_claim_gate",
        },
        {
            "artifact_id": "formal_gate_proof_audit",
            "path": "0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_claim_gate",
        },
        {
            "artifact_id": "formal_gate_proof_summary_chain_audit",
            "path": "0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_claim_gate",
        },
        {
            "artifact_id": "paper_readiness",
            "path": "0_trials/module2_paper_readiness/module2_paper_readiness.json",
            "freshness_state": "historical_dirty",
            "required_before": "formal_claim_gate",
        },
    ]
    path.write_text(
        json.dumps(
            {
                "status": "source_freshness_risks_recorded_gate_still_blocked" if required else "source_freshness_clean_current",
                "runs_training": False,
                "runs_remote_preflight": False,
                "local_training_allowed": False,
                "formal_claim_allowed": False,
                "regeneration_required_before_remote_formal_execution": required,
                "ordered_regeneration_targets": targets if required else [],
            }
        ),
        encoding="utf-8",
    )
    return path


def _remote_packet(tmp_path, *, ready):
    path = tmp_path / f"remote_packet_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "status": "ready_for_gpu3070ti_remote_training" if ready else "blocked_until_f02_6_decision",
                "ready_to_run_remote_training": ready,
                "execution_environment": {
                    "gpu_alias": "gpu3070ti-relay",
                    "training_host_required": "gpu3070ti-relay",
                },
                "execution_steps": {
                    "run_remote_training": {
                        "allowed_now": ready,
                        "runs_training": True,
                        "command": "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.run_rl_rs_gate3_trial --device cuda'",
                    },
                    "run_remote_audit": {
                        "allowed_now": ready,
                        "runs_training": False,
                        "command": "ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.audit_rl_rs_gate3_trial'",
                    },
                },
                "post_run_pullback": {
                    "expected_artifacts": [
                        "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip",
                        "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json",
                    ],
                    "pullback_command": "rsync -az gpu3070ti-relay:~/ForestNav/0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/ 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/",
                },
            }
        ),
        encoding="utf-8",
    )
    return path
