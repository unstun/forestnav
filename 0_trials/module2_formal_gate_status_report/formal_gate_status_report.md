# Module2 Formal Gate Status Report

This file is a read-only formal-gate status report. It does not execute commands, run remote preflight, train, evaluate, sync, audit, pull back artifacts, or write paper results.

- status: `formal_gate_status_blocked`
- source_head: `cf271f54413c216630878b4ab1a790165251a659+dirty`
- input_safety_issue_count: `0`
- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Current State

- decision_status: `pending_human_decision`
- decision_decider: `None`
- decision_remote_preflight_allowed_now: `False`
- decision_remote_training_allowed_now: `False`
- decision_intake_status: `f02_6_decision_intake_pending_clean`
- decision_intake_record_status: `pending_human_decision`
- decision_intake_next_blocked_lane: `decision`
- decision_intake_audit_issue_count: `0`
- decision_intake_valid_decision_count: `2`
- decision_intake_required_record_field_count: `3`
- decision_intake_decision_note_required: `True`
- decision_intake_record_command_template_count: `2`
- decision_intake_post_decision_non_authorization_count: `4`
- decision_intake_post_decision_route_count: `2`
- decision_intake_remote_preflight_allowed_now: `False`
- decision_intake_remote_training_allowed_now: `False`
- decision_intake_formal_claim_allowed_now: `False`
- formal_gate_status: `blocked_formal_gate_gaps_open`
- missing_artifacts_status: `formal_gate_missing_artifacts_open`
- missing_artifacts_handoff_index_status: `blocked_until_f02_6_decision`
- missing_artifacts_handoff_next_action: `record_f02_6_decision`
- missing_artifacts_handoff_open_requirement_count: `5`
- missing_artifacts_handoff_remote_training_allowed_now: `False`
- missing_artifacts_handoff_formal_result_material_allowed_now: `False`
- closure_checklist_status: `formal_gate_closure_blocked`
- closure_open_item_count: `8`
- closure_remote_preflight_allowed_now: `False`
- closure_remote_training_allowed_now: `False`
- closure_remote_audit_pullback_allowed_now: `False`
- remote_packet_status: `blocked_until_f02_6_decision`
- ready_to_run_remote_training: `False`
- remote_packet_sync_allowed_now: `False`
- remote_packet_preflight_allowed_now: `False`
- remote_packet_training_allowed_now: `False`
- remote_packet_audit_allowed_now: `False`
- remote_preflight_requirement_satisfied_count: `2`
- remote_preflight_requirement_blocked_count: `2`
- post_run_acceptance_requirement_satisfied_count: `0`
- post_run_acceptance_requirement_blocked_count: `4`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_formal_acceptance_requirement_satisfied_count: `1`
- h02_formal_acceptance_requirement_blocked_count: `3`
- claim_safety_status: `blocked_formal_performance_claims`
- claim_safety_formal_performance_claim_allowed: `False`
- paper_readiness_status: `partial_methods_ready_results_blocked`
- paper_readiness_formal_results_ready: `False`
- handoff_bundle_status: `blocked_until_f02_6_decision`
- remaining_deliverables_status: `formal_gate_deliverables_blocked`
- remaining_deliverables_missing_deliverable_count: `10`
- remaining_deliverables_acceptance_matrix_count: `10`
- remaining_deliverables_acceptance_missing_row_count: `10`
- remaining_deliverables_acceptance_blocked_category_count: `4`
- remaining_deliverables_gap_total_missing_deliverable_count: `10`
- remaining_deliverables_gap_open_category_count: `4`
- remaining_deliverables_proof_plan_present: `True`
- remaining_deliverables_proof_plan_matrix_row_count: `10`
- remaining_deliverables_proof_plan_command_count: `20`
- formal_gate_proof_audit_status: `formal_gate_proof_audit_blocked`
- formal_gate_proof_audit_command_count: `20`
- formal_gate_proof_audit_passed_count: `2`
- formal_gate_proof_audit_failed_count: `2`
- formal_gate_proof_audit_blocked_count: `16`
- formal_gate_proof_audit_missing_artifact_count: `8`
- formal_gate_proof_audit_failed_acceptance_artifact_count: `2`
- formal_gate_proof_audit_training_missing_artifact_count: `3`
- formal_gate_proof_audit_evaluation_missing_artifact_count: `2`
- formal_gate_proof_audit_acceptance_missing_artifact_count: `3`
- formal_gate_proof_audit_formal_acceptance_failed_artifact_count: `2`
- handoff_bundle_next_action: `record_f02_6_decision`
- handoff_bundle_safety_issue_count: `0`
- handoff_bundle_remote_training_allowed_now: `False`
- handoff_requirement_stage_mapped_count: `4`
- handoff_requirement_stage_unmapped_count: `0`
- formal_gate_execution_veto_present: `True`
- formal_gate_execution_veto_all_rows_consistent: `True`
- formal_gate_execution_veto_remote_training_allowed_now: `False`
- formal_gate_execution_veto_formal_claim_allowed_now: `False`
- formal_gate_gap_audit_remaining_total_missing_deliverables: `10`
- formal_gate_gap_audit_remaining_open_category_count: `4`
- remote_packet_safety_proof_summary_present: `True`
- remote_packet_safety_proof_training_missing_count: `3`
- remote_packet_safety_proof_evaluation_missing_count: `2`
- remote_packet_safety_proof_acceptance_missing_count: `3`
- remote_packet_safety_proof_formal_acceptance_missing_count: `2`
- remote_packet_safety_proof_next_blocked_lane: `decision`
- remote_packet_safety_proof_h02_paper_result_input_allowed: `False`
- remote_packet_safety_status_report_proof_summary_present: `True`
- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_non_self_changed_records: `21`
- source_freshness_self_artifact_only_lag_records: `0`
- remote_packet_safety_command_index_present: `True`
- remote_packet_safety_command_index_row_count: `21`
- remote_packet_safety_command_index_source_target_count: `21`
- remote_packet_safety_command_index_missing_target_count: `0`
- next_action_guard_status: `next_action_guard_passed`

## Next Blocked Lane

- lane_id: `decision`
- phase: `decision`
- blocked_by: `f02_6_decision_not_approved, f02_6_warm_start_decision_pending, requires_dr_sun_approval`
- action: Record Dr Sun's F02.6 decision before any formal preflight or training.

## F02.6 Decision Intake

- present: `True`
- status: `f02_6_decision_intake_pending_clean`
- record_status: `pending_human_decision`
- record_decider: `None`
- effective_warm_start_decision: `pending`
- next_blocked_lane: `decision`
- audit_issue_count: `0`
- decision_owner_required: `Dr Sun`
- valid_decision_count: `2`
- required_record_field_count: `3`
- decision_note_required: `True`
- invalid_input_count: `5`
- post_decision_non_authorization_count: `4`
- post_decision_route_count: `2`
- post_decision_route_decisions: `approve_obstacle_summary_warm_start, reject_obstacle_summary_warm_start`
- approved_route_next_lane: `source_fresh_regeneration`
- approved_route_allows_remote_training_now: `False`
- rejected_route_next_lane: `protocol_redesign`
- rejected_route_requires_new_protocol_contract: `True`
- missing_deliverable_count: `10`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Next Action Guard

- present: `True`
- status: `next_action_guard_passed`
- pending_f02_6_decision: `True`
- expected_next_action_id: `record_f02_6_decision`
- handoff_next_action_id: `record_f02_6_decision`
- missing_artifacts_next_action_id: `record_f02_6_decision`
- all_execution_disabled_now: `True`
- execution_leak_count: `0`
- remote_execution_allowed_count: `0`
- remote_stage_allowed_count: `0`
- violations: `none`

## Formal Gate Lanes

- `decision` (decision): status=`blocked`, missing=`1`, runs_training=`False`
  - blocked_by: `f02_6_decision_not_approved, f02_6_warm_start_decision_pending, requires_dr_sun_approval`
  - completion_signal: F02.6 decision record is approved or rejected by Dr Sun.
  - action_when_blocked: Record Dr Sun's F02.6 decision before any formal preflight or training.
- `source_fresh_preflight` (regeneration): status=`blocked`, missing=`21`, runs_training=`False`
  - blocked_by: `source_freshness_regeneration_required, f02_6_warm_start_decision_pending, requires_dr_sun_approval, f02_6_decision_not_approved`
  - completion_signal: Source-fresh preflight targets are regenerated from the current head.
  - action_when_blocked: After F02.6 closes, regenerate source-fresh gate artifacts before approved preflight.
- `remote_packet_preflight` (remote_preflight): status=`blocked`, missing=`7`, runs_training=`False`
  - blocked_by: `regenerate_preflight_gate_artifacts, approved_remote_preflight, regenerate_remote_execution_packet, gate3_remote_training, gate3_remote_audit_pullback, regenerate_h01_h02_formal_artifacts, regenerate_claim_gate_artifacts, f02_6_warm_start_decision_pending, requires_dr_sun_approval, source_freshness_regeneration_required, f02_6_decision_not_approved, source_fresh_preflight_targets_open`
  - completion_signal: Approved gpu3070ti preflight passes and remote packet reports ready.
  - action_when_blocked: Run only approved remote preflight after F02.6 and source freshness close.
- `gate3_remote_training` (training): status=`blocked`, missing=`3`, runs_training=`True`, host=`gpu3070ti-relay`
  - blocked_by: `train_final_model_zip, train_summary_json, train_training_manifest_json, f02_6_warm_start_decision_pending, requires_dr_sun_approval, source_freshness_regeneration_required, remote_training_packet_not_ready, f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - completion_signal: final_model.zip, train summary, and training manifest are pulled back.
  - action_when_blocked: Run formal PPO only on gpu3070ti-relay after remote packet is ready.
- `gate3_eval_and_audit_pullback` (acceptance): status=`blocked`, missing=`5`, runs_training=`False`
  - blocked_by: `gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record, eval_gate3_eval_episodes_csv, eval_gate3_summary_json, f02_6_warm_start_decision_pending, requires_dr_sun_approval, source_freshness_regeneration_required, remote_training_packet_not_ready, missing_remote_pullback_artifact, missing_ppo_result_rows, missing_ppo_checkpoint_hash, f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - completion_signal: Gate3 eval outputs, trial manifest, formal audit, and checkpoint hash are present.
  - action_when_blocked: Audit remote trial and pull back the complete trial directory with hashes.
- `h01_h02_formal_evaluation` (evaluation_acceptance): status=`blocked`, missing=`2`, runs_training=`False`
  - blocked_by: `h01_ready_for_formal_run, h02_formal_output_acceptance, f02_6_warm_start_decision_pending, requires_dr_sun_approval, source_freshness_regeneration_required, remote_training_packet_not_ready, missing_remote_pullback_artifact, missing_ppo_result_rows, missing_ppo_checkpoint_hash, h01_manifest_not_ready, formal_main_evaluation_command_missing, h02_scale_below_h01_queries_per_bucket, h02_scale_below_h01_seed_count, h02_scale_below_h01_queries_per_map, h02_verdict_not_formal, missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
  - completion_signal: H01 is ready and H02 accepts formal-scale PPO outputs.
  - action_when_blocked: Regenerate H01/H02 only after audited checkpoint pullback is complete.
- `claim_gate` (claim_gate): status=`blocked`, missing=`8`, runs_training=`False`
  - blocked_by: `claim_safety, formal_gate_missing_artifacts, formal_gate_proof_audit, formal_gate_proof_summary_chain_audit, formal_gate_remaining_deliverables, formal_gate_status_report, paper_readiness, h02_formal_acceptance_before_claim_gate, f02_6_warm_start_decision_pending, requires_dr_sun_approval, source_freshness_regeneration_required, remote_training_packet_not_ready, missing_remote_pullback_artifact, missing_ppo_result_rows, missing_ppo_checkpoint_hash, h01_manifest_not_ready, formal_main_evaluation_command_missing, h02_scale_below_h01_queries_per_bucket, h02_scale_below_h01_seed_count, h02_scale_below_h01_queries_per_map, h02_verdict_not_formal, missing_or_failed_gate3_formal_audit, h02_formal_output_not_accepted, claim_safety_blocks_formal_performance, readiness_blocks_formal_results, formal_gate_missing_artifacts_open, formal_gate_closure_checklist_open, formal_gate_status_report_blocked, formal_gate_remaining_deliverables_open, h02_formal_acceptance_not_ready, source_fresh_claim_targets_open`
  - completion_signal: Claim safety and paper readiness allow formal results after H02 acceptance.
  - action_when_blocked: Regenerate claim gates only after H02 formal acceptance passes.

## Remote Execution Steps

- `sync_to_remote`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_preflight`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_training`: present=`True`, allowed_now=`False`, runs_training=`True`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready`
- `run_remote_audit`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready`

## Remote Preflight Requirement Matrix

- present: `True`
- status_counts: `{'blocked_missing_preflight': 2, 'satisfied': 2}`
- blocked_requirement_count: `2`
- `f02_6_decision_closed_for_preflight`: status=`blocked_missing_preflight`, complete=`False`, execution_allowed_now=`False`, blocked_by=`requires_dr_sun_approval`
- `approved_remote_preflight_manifest`: status=`blocked_missing_preflight`, complete=`False`, execution_allowed_now=`False`, blocked_by=`warm_start_decision_pending`
- `remote_preflight_protocol_contract`: status=`satisfied`, complete=`True`, execution_allowed_now=`False`, blocked_by=`none`
- `remote_preflight_command_packetized`: status=`satisfied`, complete=`True`, execution_allowed_now=`False`, blocked_by=`requires_dr_sun_approval`

## Post-Run Acceptance Requirement Matrix

- present: `True`
- status_counts: `{'blocked_until_remote_audit': 4}`
- blocked_requirement_count: `4`
- `pullback_expected_artifacts_complete`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`False`
- `checkpoint_hash_manifest_recorded`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`False`
- `gate3_formal_audit_accepts_remote_run`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`False`
- `h01_h02_regenerated_from_audited_checkpoint`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`False`

## H02 Formal Acceptance Requirement Matrix

- present: `True`
- status_counts: `{'satisfied': 1, 'blocked_formal_acceptance': 3}`
- blocked_requirement_count: `3`
- `h01_schema_and_h02_output_schema_match`: status=`satisfied`, complete=`True`, paper_result_input_allowed_now=`False`
- `h02_formal_scope_and_scale_match_h01`: status=`blocked_formal_acceptance`, complete=`False`, paper_result_input_allowed_now=`False`
- `gate3_audit_and_pullback_acceptance`: status=`blocked_formal_acceptance`, complete=`False`, paper_result_input_allowed_now=`False`
- `ppo_rows_and_checkpoint_hash_present`: status=`blocked_formal_acceptance`, complete=`False`, paper_result_input_allowed_now=`False`

## Remaining Deliverables Acceptance Matrix

- present: `True`
- status: `formal_gate_deliverables_blocked`
- matrix_row_count: `10`
- missing_row_count: `10`
- blocked_category_count: `4`
- `training:train_final_model_zip`: missing=`True`, current_state=`missing`, stage=`gate3_remote_training`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`4`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `training:train_summary_json`: missing=`True`, current_state=`missing`, stage=`gate3_remote_training`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`4`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `training:train_training_manifest_json`: missing=`True`, current_state=`missing`, stage=`gate3_remote_training`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`4`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `evaluation:eval_gate3_eval_episodes_csv`: missing=`True`, current_state=`missing`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `evaluation:eval_gate3_summary_json`: missing=`True`, current_state=`missing`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `acceptance:gate3_trial_manifest_json`: missing=`True`, current_state=`missing`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `acceptance:gate3_formal_audit_json`: missing=`True`, current_state=`missing`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `acceptance:pulled_back_checkpoint_hash_record`: missing=`True`, current_state=`missing`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `formal_acceptance:h01_ready_for_formal_run`: missing=`True`, current_state=`blocked_pending_decisions`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
- `formal_acceptance:h02_formal_output_acceptance`: missing=`True`, current_state=`blocked_formal_output_acceptance`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`

## Remaining Deliverables Gap Summary

- present: `True`
- summary_id: `module2_formal_gate_missing_training_eval_acceptance_summary`
- total_missing_deliverables: `10`
- open_category_count: `4`
- execution_boundary: `read_only_no_execution`
- `training`: missing_count=`3`, stage=`gate3_remote_training`, stage_allowed_now=`False`, missing_artifacts=`training:train_final_model_zip, training:train_summary_json, training:train_training_manifest_json`, proof_commands=`train_final_model_zip_exists_nonempty, train_final_model_zip_valid_zip, train_summary_json_exists_nonempty, train_summary_json_formal_warm_start_metadata, train_training_manifest_json_exists_nonempty, train_training_manifest_json_provenance`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `evaluation`: missing_count=`2`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, missing_artifacts=`evaluation:eval_gate3_eval_episodes_csv, evaluation:eval_gate3_summary_json`, proof_commands=`eval_gate3_eval_episodes_csv_exists_nonempty, eval_gate3_eval_episodes_csv_schema, eval_gate3_summary_json_exists_nonempty, eval_gate3_summary_json_formal_scope`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `acceptance`: missing_count=`3`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, missing_artifacts=`acceptance:gate3_trial_manifest_json, acceptance:gate3_formal_audit_json, acceptance:pulled_back_checkpoint_hash_record`, proof_commands=`gate3_trial_manifest_json_exists_nonempty, gate3_trial_manifest_json_formal_warm_start_scope, gate3_formal_audit_json_exists_nonempty, gate3_formal_audit_json_accepts_formal_scope, pulled_back_checkpoint_hash_record_exists_nonempty, pulled_back_checkpoint_hash_record_matches_model`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `formal_acceptance`: missing_count=`2`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, missing_artifacts=`formal_acceptance:h01_ready_for_formal_run, formal_acceptance:h02_formal_output_acceptance`, proof_commands=`h01_ready_for_formal_run_exists_nonempty, h01_ready_for_formal_run_status, h02_formal_output_acceptance_exists_nonempty, h02_formal_output_acceptance_status`, blocked_by=`missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`

## Remaining Deliverables Proof Command Plan

- present: `True`
- plan_id: `module2_formal_gate_local_read_only_proof_commands`
- execution_boundary: `local_read_only_after_formal_remote_pullback`
- total_matrix_rows: `10`
- total_proof_command_count: `20`
- runs_training: `False`
- runs_remote_preflight: `False`
- `training:train_final_model_zip`: proof_command_count=`2`, command_ids=`train_final_model_zip_exists_nonempty, train_final_model_zip_valid_zip`
- `training:train_summary_json`: proof_command_count=`2`, command_ids=`train_summary_json_exists_nonempty, train_summary_json_formal_warm_start_metadata`
- `training:train_training_manifest_json`: proof_command_count=`2`, command_ids=`train_training_manifest_json_exists_nonempty, train_training_manifest_json_provenance`
- `evaluation:eval_gate3_eval_episodes_csv`: proof_command_count=`2`, command_ids=`eval_gate3_eval_episodes_csv_exists_nonempty, eval_gate3_eval_episodes_csv_schema`
- `evaluation:eval_gate3_summary_json`: proof_command_count=`2`, command_ids=`eval_gate3_summary_json_exists_nonempty, eval_gate3_summary_json_formal_scope`
- `acceptance:gate3_trial_manifest_json`: proof_command_count=`2`, command_ids=`gate3_trial_manifest_json_exists_nonempty, gate3_trial_manifest_json_formal_warm_start_scope`
- `acceptance:gate3_formal_audit_json`: proof_command_count=`2`, command_ids=`gate3_formal_audit_json_exists_nonempty, gate3_formal_audit_json_accepts_formal_scope`
- `acceptance:pulled_back_checkpoint_hash_record`: proof_command_count=`2`, command_ids=`pulled_back_checkpoint_hash_record_exists_nonempty, pulled_back_checkpoint_hash_record_matches_model`
- `formal_acceptance:h01_ready_for_formal_run`: proof_command_count=`2`, command_ids=`h01_ready_for_formal_run_exists_nonempty, h01_ready_for_formal_run_status`
- `formal_acceptance:h02_formal_output_acceptance`: proof_command_count=`2`, command_ids=`h02_formal_output_acceptance_exists_nonempty, h02_formal_output_acceptance_status`

## Formal Gate Proof Audit Gap Summary

- present: `True`
- status: `formal_gate_proof_audit_blocked`
- missing_artifact_count=`8`
- failed_acceptance_artifact_count=`2`
- `training`: missing_artifact_count=`3`, failed_acceptance_artifact_count=`0`, blocked_proof_command_count=`6`, failed_proof_command_count=`0`, missing_artifacts=`train_final_model_zip, train_summary_json, train_training_manifest_json`, failed_artifacts=`none`, blocked_commands=`train_final_model_zip_exists_nonempty, train_final_model_zip_valid_zip, train_summary_json_exists_nonempty, train_summary_json_formal_warm_start_metadata, train_training_manifest_json_exists_nonempty, train_training_manifest_json_provenance`, failed_commands=`none`
- `evaluation`: missing_artifact_count=`2`, failed_acceptance_artifact_count=`0`, blocked_proof_command_count=`4`, failed_proof_command_count=`0`, missing_artifacts=`eval_gate3_eval_episodes_csv, eval_gate3_summary_json`, failed_artifacts=`none`, blocked_commands=`eval_gate3_eval_episodes_csv_exists_nonempty, eval_gate3_eval_episodes_csv_schema, eval_gate3_summary_json_exists_nonempty, eval_gate3_summary_json_formal_scope`, failed_commands=`none`
- `acceptance`: missing_artifact_count=`3`, failed_acceptance_artifact_count=`0`, blocked_proof_command_count=`6`, failed_proof_command_count=`0`, missing_artifacts=`gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record`, failed_artifacts=`none`, blocked_commands=`gate3_trial_manifest_json_exists_nonempty, gate3_trial_manifest_json_formal_warm_start_scope, gate3_formal_audit_json_exists_nonempty, gate3_formal_audit_json_accepts_formal_scope, pulled_back_checkpoint_hash_record_exists_nonempty, pulled_back_checkpoint_hash_record_matches_model`, failed_commands=`none`
- `formal_acceptance`: missing_artifact_count=`0`, failed_acceptance_artifact_count=`2`, blocked_proof_command_count=`0`, failed_proof_command_count=`2`, missing_artifacts=`none`, failed_artifacts=`h01_ready_for_formal_run, h02_formal_output_acceptance`, blocked_commands=`none`, failed_commands=`h01_ready_for_formal_run_status, h02_formal_output_acceptance_status`

## Formal Gate Proof Audit

- present: `True`
- status: `formal_gate_proof_audit_blocked`
- total_matrix_rows: `10`
- total_proof_command_count: `20`
- passed_proof_command_count: `2`
- failed_proof_command_count: `2`
- blocked_proof_command_count: `16`
- remaining_deliverables_summary_present: `True`
- remaining_missing_counts_by_formal_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- remaining_next_blocked_lane: `decision`
- remaining_h01_status: `blocked_pending_decisions`
- remaining_h02_status: `blocked_formal_output_acceptance`
- remaining_training_missing_matrix_ids: `training:train_final_model_zip, training:train_summary_json, training:train_training_manifest_json`
- remaining_evaluation_missing_matrix_ids: `evaluation:eval_gate3_eval_episodes_csv, evaluation:eval_gate3_summary_json`
- remaining_acceptance_missing_matrix_ids: `acceptance:gate3_trial_manifest_json, acceptance:gate3_formal_audit_json, acceptance:pulled_back_checkpoint_hash_record`
- remaining_formal_acceptance_missing_matrix_ids: `formal_acceptance:h01_ready_for_formal_run, formal_acceptance:h02_formal_output_acceptance`
- `train_final_model_zip_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`training:train_final_model_zip`
- `train_final_model_zip_valid_zip`: status=`blocked_missing_artifact`, matrix_id=`training:train_final_model_zip`
- `train_summary_json_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`training:train_summary_json`
- `train_summary_json_formal_warm_start_metadata`: status=`blocked_missing_artifact`, matrix_id=`training:train_summary_json`
- `train_training_manifest_json_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`training:train_training_manifest_json`
- `train_training_manifest_json_provenance`: status=`blocked_missing_artifact`, matrix_id=`training:train_training_manifest_json`
- `eval_gate3_eval_episodes_csv_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`evaluation:eval_gate3_eval_episodes_csv`
- `eval_gate3_eval_episodes_csv_schema`: status=`blocked_missing_artifact`, matrix_id=`evaluation:eval_gate3_eval_episodes_csv`
- `eval_gate3_summary_json_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`evaluation:eval_gate3_summary_json`
- `eval_gate3_summary_json_formal_scope`: status=`blocked_missing_artifact`, matrix_id=`evaluation:eval_gate3_summary_json`
- `gate3_trial_manifest_json_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`acceptance:gate3_trial_manifest_json`
- `gate3_trial_manifest_json_formal_warm_start_scope`: status=`blocked_missing_artifact`, matrix_id=`acceptance:gate3_trial_manifest_json`
- `gate3_formal_audit_json_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`acceptance:gate3_formal_audit_json`
- `gate3_formal_audit_json_accepts_formal_scope`: status=`blocked_missing_artifact`, matrix_id=`acceptance:gate3_formal_audit_json`
- `pulled_back_checkpoint_hash_record_exists_nonempty`: status=`blocked_missing_artifact`, matrix_id=`acceptance:pulled_back_checkpoint_hash_record`
- `pulled_back_checkpoint_hash_record_matches_model`: status=`blocked_missing_artifact`, matrix_id=`acceptance:pulled_back_checkpoint_hash_record`
- `h01_ready_for_formal_run_exists_nonempty`: status=`passed`, matrix_id=`formal_acceptance:h01_ready_for_formal_run`
- `h01_ready_for_formal_run_status`: status=`failed`, matrix_id=`formal_acceptance:h01_ready_for_formal_run`
- `h02_formal_output_acceptance_exists_nonempty`: status=`passed`, matrix_id=`formal_acceptance:h02_formal_output_acceptance`
- `h02_formal_output_acceptance_status`: status=`failed`, matrix_id=`formal_acceptance:h02_formal_output_acceptance`

## Formal Gate Gap Audit Remaining Deliverables Gap Summary

- present: `True`
- summary_id: `module2_formal_gate_missing_training_eval_acceptance_summary`
- total_missing_deliverables: `10`
- open_category_count: `4`
- matches_ledger_signature: `True`

## Remote Packet Safety Proof Deliverables Summary

- proof_summary_present: `True`
- proof_missing_counts_by_formal_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- proof_next_blocked_lane: `decision`
- proof_h01_status: `blocked_pending_decisions`
- proof_h02_status: `blocked_formal_output_acceptance`
- proof_h02_paper_result_input_allowed: `False`
- status_report_proof_summary_present: `True`
- status_report_proof_matches_remote_proof: `True`
- remote_proof_matches_proof_audit: `True`
- remote_proof_training_missing_matrix_ids: `training:train_final_model_zip, training:train_summary_json, training:train_training_manifest_json`
- remote_proof_evaluation_missing_matrix_ids: `evaluation:eval_gate3_eval_episodes_csv, evaluation:eval_gate3_summary_json`
- remote_proof_acceptance_missing_matrix_ids: `acceptance:gate3_trial_manifest_json, acceptance:gate3_formal_audit_json, acceptance:pulled_back_checkpoint_hash_record`
- remote_proof_formal_acceptance_missing_matrix_ids: `formal_acceptance:h01_ready_for_formal_run, formal_acceptance:h02_formal_output_acceptance`

## Remote Packet Safety Claim-Gate Command Index

- present: `True`
- index_row_count: `21`
- source_target_count: `21`
- missing_target_ids: `[]`
- unknown_manual_count: `0`
- forbidden_command_count: `0`
- `formal_gate_proof_summary_chain_audit`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`
- `claim_safety`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`
- `paper_readiness`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`

## Closure Remote Stages

- `approved_remote_preflight`: present=`True`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`True`, host=`gpu3070ti-relay`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open`
- `gate3_remote_training`: present=`True`, allowed_now=`False`, runs_training=`True`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `gate3_remote_audit_pullback`: present=`True`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`

## Missing-Artifacts Handoff Index

- present: `True`
- status: `blocked_until_f02_6_decision`
- next_action: `record_f02_6_decision`
- next_action_requires_dr_sun: `True`
- open_requirement_count: `5`
- local_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_result_material_allowed_now: `False`

## Formal Gate Handoff Bundle

- present: `True`
- status: `blocked_until_f02_6_decision`
- next_handoff_action: `record_f02_6_decision`
- safety_issue_count: `0`
- remote_training_allowed_now: `False`
- `sync_to_remote`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_preflight`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_training`: present=`True`, allowed_now=`False`, runs_training=`True`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready`
- `run_remote_audit`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready`

## Formal Gate Requirement Stage Summary

- mapped_requirement_count: `4`
- unmapped_requirement_count: `0`
- mismatched_requirement_count: `0`
- `training_remote_ppo_checkpoint`: expected_stage=`gate3_remote_training`, responsible_stage=`gate3_remote_training`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `evaluation_gate3_episode_outputs`: expected_stage=`gate3_remote_audit_pullback`, responsible_stage=`gate3_remote_audit_pullback`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `acceptance_remote_pullback_and_audit`: expected_stage=`gate3_remote_audit_pullback`, responsible_stage=`gate3_remote_audit_pullback`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `h01_h02_formal_evaluation_acceptance`: expected_stage=`regenerate_h01_h02_formal_artifacts`, responsible_stage=`regenerate_h01_h02_formal_artifacts`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`

## Formal Gate Execution Veto Matrix

- present: `True`
- all_rows_consistent: `True`
- mismatch_rows: `[]`
- `local_training`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'formal_gate_gap_audit': False, 'status_report': False, 'handoff_bundle': False, 'remote_packet': False}`
- `remote_preflight`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'status_report': False, 'handoff_bundle': False, 'remote_packet': False, 'remote_packet_safety': False}`
- `remote_training`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'decision_record': False, 'status_report': False, 'handoff_bundle': False, 'remote_packet': False, 'remote_packet_safety': False}`
- `remote_audit`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'handoff_bundle': False, 'remote_packet': False, 'remote_packet_safety': False}`
- `formal_claim`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'status_report': False, 'handoff_bundle': False}`

## Required Training Artifacts

- `train_final_model_zip`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
- `train_summary_json`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
- `train_training_manifest_json`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`

## Required Evaluation Artifacts

- `eval_gate3_eval_episodes_csv`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
- `eval_gate3_summary_json`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`

## Required Acceptance Artifacts

- `gate3_trial_manifest_json`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
- `gate3_formal_audit_json`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- `pulled_back_checkpoint_hash_record`: missing=`True`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`

## Input Safety Issues

- none

## Safe Work Without F02.6 Decision

- Maintain or harden read-only gate artifacts.
- Add tests for gate ordering, artifact inventory, and claim blocking.
- Do not run approved remote preflight, formal PPO training, H02 formal evaluation, pullback, or result-claim writing.

## Claim Boundaries

- This status report is an execution-orientation artifact, not a result table or paper appendix.
- It does not execute commands, remote preflight, training, evaluation, sync, audit, or pullback.
- It must not be used to approve F02.6; only Dr Sun's decision record can do that.
- Formal PPO training remains gpu3070ti-relay-only and blocked until F02.6, source freshness, and remote packet gates close.
- Formal result writing remains blocked until H02 acceptance, claim safety, paper readiness, and the closure checklist all pass after audited pullback hashes.
- The formal gate execution veto matrix must agree across status, handoff, remote packet, and remote packet safety before this report can become claim-ready.
