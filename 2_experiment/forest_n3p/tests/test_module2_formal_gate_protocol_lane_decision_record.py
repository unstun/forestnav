import json
from importlib import import_module
from pathlib import Path

import pytest


def test_protocol_lane_decision_record_defaults_to_pending_and_blocks_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record")
    manifest_path = tmp_path / "record.json"
    markdown_path = tmp_path / "record.md"

    rc = builder.main(
        [
            "--decision-packet",
            str(_decision_packet(tmp_path)),
            "--next-round-requirements",
            str(_next_round_requirements(tmp_path)),
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
        ]
    )

    assert rc == 0
    record = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert record["schema_version"] == 1
    assert record["record_name"] == "module2_formal_gate_protocol_lane_decision_record"
    assert record["status"] == "pending_protocol_lane_decision"
    assert record["not_paper_result_material"] is True
    assert record["executes_commands"] is False
    assert record["runs_training"] is False
    assert record["runs_remote_preflight"] is False
    assert record["requested_selected_lane"] == "pending"
    assert record["selected_lane_id"] is None
    assert record["decider"] is None
    assert record["decision_note"] is None
    assert record["contract_action"] == "none"
    assert record["training_authorization"] == "not_authorized_by_this_decision_record"
    assert record["decision_record_is_not_training_authorization"] is True
    assert record["decision_record_is_not_paper_result_material"] is True
    assert record["remote_training_allowed_now"] is False
    assert record["local_training_allowed_now"] is False
    assert record["formal_claim_allowed_now"] is False
    assert record["paper_result_material_allowed_now"] is False
    assert record["decision_note_audit"]["required_for_non_pending_decision"] is False
    assert record["current_authorization"]["authorization_status"] == "blocked_until_dr_sun_lane_decision"
    assert record["current_authorization"]["current_allowed_action_ids"] == ["record_protocol_lane_decision"]
    assert "remote_success_training" in record["current_authorization"]["current_blocked_action_ids"]
    assert record["post_decision_requirements"]["new_or_revised_contract_required"] is False
    assert record["next_success_attempt_requirements"]["source_status"] == "formal_gate_next_round_requirements_ready"
    assert record["next_success_attempt_requirements"]["next_success_attempt_artifact_count"] == 10
    assert record["next_success_attempt_requirements"]["next_success_attempt_artifact_category_counts"] == {
        "contract": 1,
        "training": 3,
        "evaluation": 2,
        "acceptance": 3,
        "formal_acceptance": 1,
    }
    assert record["next_success_attempt_requirements"]["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True
    assert record["post_decision_requirements"]["next_success_attempt_artifact_count"] == 10
    assert record["post_decision_requirements"]["next_success_attempt_artifact_ids_by_category"]["contract"] == [
        "new_or_revised_research_contract"
    ]
    assert len(record["record_command_templates"]) == 4
    assert all(template["allowed_for_agent_now"] is False for template in record["record_command_templates"])
    assert all(template["runs_training"] is False for template in record["record_command_templates"])
    assert all("0.53125" in template["template"] for template in record["record_command_templates"])
    assert all("0.8" in template["template"] for template in record["record_command_templates"])
    assert all("does not authorize local training" in template["template"] for template in record["record_command_templates"])
    assert "pending_protocol_lane_decision" in markdown
    assert "decision_record_is_not_training_authorization: `True`" in markdown
    assert "Record Command Templates" in markdown
    assert "full_patch_cnn_policy" in markdown
    assert "allowed_for_agent_now: `False`" in markdown
    assert "runs_training: `False`" in markdown
    assert "Post-Decision Requirements" in markdown
    assert "Next Success Attempt Requirements" in markdown
    assert "next_success_attempt_artifact_count: `10`" in markdown
    assert "approved_or_frozen_contract" in markdown
    assert "paper_result_input_allowed_true" in markdown


def test_protocol_lane_decision_record_records_dr_sun_lane_choice_without_authorizing_training(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record")

    record = builder.build_record(
        builder.FormalGateProtocolLaneDecisionRecordConfig(
            output_dir=tmp_path,
            decision_packet_path=_decision_packet(tmp_path),
            next_round_requirements_path=_next_round_requirements(tmp_path),
            selected_lane="hybrid_ppo_analytic_fallback",
            decider="Dr Sun",
            contract_action="draft_revised_contract",
            decision_note=(
                "Select hybrid_ppo_analytic_fallback because the failed Gate3 0.53125 result is below "
                "the 0.8 threshold and suggests direct replacement is weak; reject stronger_obstacle_summary_warm_start, "
                "full_patch_cnn_policy, and stop_or_reframe_module2_claim for this round; "
                "use protocol_lane_matrix and gate3_formal_audit artifacts as the evidence basis; "
                "draft revised contract before any training."
            ),
        )
    )

    assert record["status"] == "protocol_lane_decision_recorded"
    assert record["selected_lane_id"] == "hybrid_ppo_analytic_fallback"
    assert record["decider"] == "Dr Sun"
    assert record["contract_action"] == "draft_revised_contract"
    assert record["training_authorization"] == "not_authorized_by_this_decision_record"
    assert record["remote_training_allowed_now"] is False
    assert record["local_training_allowed_now"] is False
    assert record["formal_claim_allowed_now"] is False
    assert record["decision_note_audit"]["quality_warning"] is None
    assert record["decision_note_audit"]["mentions_selected_lane"] is True
    assert record["decision_note_audit"]["mentions_failed_gate3"] is True
    assert record["decision_note_audit"]["mentions_contract_action"] is True
    assert record["decision_note_audit"]["mentions_rejected_lanes"] is True
    assert record["decision_note_audit"]["mentions_evidence_artifacts"] is True
    assert record["selected_lane_summary"]["lane_id"] == "hybrid_ppo_analytic_fallback"
    assert record["selected_lane_summary"]["requires_new_or_revised_contract"] is True
    assert record["current_authorization"]["authorization_status"] == "decision_recorded_not_execution_authorization"
    assert record["current_authorization"]["current_allowed_action_ids"] == [
        "draft_new_or_revised_contract_after_lane_decision"
    ]
    assert record["post_decision_requirements"]["new_or_revised_contract_required"] is True
    assert "approved_or_frozen_contract" in record["post_decision_requirements"]["formal_training_still_requires"]
    assert record["post_decision_requirements"]["next_success_attempt_artifact_count"] == 10
    assert record["post_decision_requirements"]["old_failed_run_artifacts_invalid_for_next_success_attempt"] is True


def test_protocol_lane_decision_record_rejects_incomplete_decision_note_quality(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record")

    with pytest.raises(ValueError, match="decision note is incomplete"):
        builder.build_record(
            builder.FormalGateProtocolLaneDecisionRecordConfig(
                output_dir=tmp_path,
                decision_packet_path=_decision_packet(tmp_path),
                next_round_requirements_path=_next_round_requirements(tmp_path),
                selected_lane="hybrid_ppo_analytic_fallback",
                decider="Dr Sun",
                contract_action="draft_revised_contract",
                decision_note="Select hybrid_ppo_analytic_fallback because Gate3 failed. Draft revised contract.",
            )
        )


def test_protocol_lane_decision_record_rejects_non_dr_sun_decider(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record")

    with pytest.raises(ValueError, match="decider='Dr Sun'"):
        builder.build_record(
            builder.FormalGateProtocolLaneDecisionRecordConfig(
                output_dir=tmp_path,
                decision_packet_path=_decision_packet(tmp_path),
                next_round_requirements_path=_next_round_requirements(tmp_path),
                selected_lane="full_patch_cnn_policy",
                decider="Assistant",
                contract_action="draft_new_contract",
                decision_note="Assistant cannot choose full_patch_cnn_policy.",
            )
        )


def test_protocol_lane_decision_record_requires_note_and_contract_action(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record")

    with pytest.raises(ValueError, match="non-empty --decision-note"):
        builder.build_record(
            builder.FormalGateProtocolLaneDecisionRecordConfig(
                output_dir=tmp_path,
                decision_packet_path=_decision_packet(tmp_path),
                next_round_requirements_path=_next_round_requirements(tmp_path),
                selected_lane="full_patch_cnn_policy",
                decider="Dr Sun",
                contract_action="draft_new_contract",
            )
        )
    with pytest.raises(ValueError, match="unsupported contract action"):
        builder.build_record(
            builder.FormalGateProtocolLaneDecisionRecordConfig(
                output_dir=tmp_path,
                decision_packet_path=_decision_packet(tmp_path),
                next_round_requirements_path=_next_round_requirements(tmp_path),
                selected_lane="full_patch_cnn_policy",
                decider="Dr Sun",
                contract_action="start_training",
                decision_note="Select full_patch_cnn_policy after failed Gate3 and draft contract.",
            )
        )


def test_protocol_lane_decision_record_rejects_invalid_lane(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record")

    with pytest.raises(ValueError, match="unsupported protocol lane"):
        builder.build_record(
            builder.FormalGateProtocolLaneDecisionRecordConfig(
                output_dir=tmp_path,
                decision_packet_path=_decision_packet(tmp_path),
                next_round_requirements_path=_next_round_requirements(tmp_path),
                selected_lane="secret_lane",
            )
        )


def _decision_packet(tmp_path):
    path = tmp_path / "decision_packet.json"
    lane_ids = [
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    ]
    path.write_text(
        json.dumps(
            {
                "status": "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun",
                "runs_training": False,
                "remote_training_allowed_now": False,
                "decision_required": True,
                "selected_lane": None,
                "valid_lane_ids": lane_ids,
                "current_allowed_actions": [
                    "record_protocol_lane_decision",
                    "draft_new_or_revised_contract_after_lane_decision",
                ],
                "current_blocked_actions": [
                    "local_training",
                    "remote_success_training",
                    "remote_preflight_for_new_success_attempt",
                    "formal_claim",
                    "paper_result_material",
                ],
                "decision_record_schema": {
                    "allowed_contract_actions": [
                        "draft_new_contract",
                        "draft_revised_contract",
                        "stop_success_attempts_and_record_negative_evidence",
                    ],
                    "training_authorization_must_be": "not_authorized_by_this_decision_packet",
                },
                "lane_options": [
                    {
                        "lane_id": lane_id,
                        "claim_scope": f"claim scope for {lane_id}",
                        "requires_new_or_revised_contract": True,
                        "required_decision_justification": ["justify after failed Gate3"],
                        "must_carry_into_contract": {"invalid_substitutes": ["failed checkpoint"]},
                    }
                    for lane_id in lane_ids
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _next_round_requirements(tmp_path):
    path = tmp_path / "next_round_requirements.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_gate_next_round_requirements_ready",
                "protocol_gate_summary": {
                    "protocol_status": "protocol_lane_status_blocked_pending_lane_decision",
                    "decision_record_status": "pending_protocol_lane_decision",
                    "selected_lane_id": None,
                    "next_blocked_lane": "protocol_lane_decision",
                    "allowed_next_action_ids": ["record_protocol_lane_decision"],
                    "blocked_action_ids": [
                        "local_training",
                        "remote_success_training",
                        "remote_preflight_for_new_success_attempt",
                        "formal_claim",
                        "paper_result_material",
                    ],
                    "new_success_training_allowed_now": False,
                    "contract_drafting_allowed_now": False,
                    "contract_approval_allowed_now": False,
                    "next_success_attempt_artifact_status": "blocked_until_protocol_lane_decision_and_contract",
                    "next_success_attempt_artifact_count": 10,
                    "next_success_attempt_artifact_category_counts": {
                        "contract": 1,
                        "training": 3,
                        "evaluation": 2,
                        "acceptance": 3,
                        "formal_acceptance": 1,
                    },
                    "next_success_attempt_artifact_ids_by_category": {
                        "contract": ["new_or_revised_research_contract"],
                        "training": [
                            "train_final_model_zip",
                            "train_summary_json",
                            "train_training_manifest_json",
                        ],
                        "evaluation": ["eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"],
                        "acceptance": [
                            "gate3_trial_manifest_json",
                            "gate3_formal_audit_json",
                            "pulled_back_checkpoint_hash_record",
                        ],
                        "formal_acceptance": ["h02_formal_output_acceptance"],
                    },
                },
                "current_vs_next_attempt_reconciliation": {
                    "current_failed_run_missing_counts": {
                        "training": 0,
                        "evaluation": 0,
                        "acceptance": 0,
                        "formal_acceptance": 1,
                    },
                    "old_failed_run_artifacts_invalid_for_next_success_attempt": True,
                    "next_success_attempt_requires_protocol_lane_decision": True,
                },
            }
        ),
        encoding="utf-8",
    )
    return path
