# Module2 Formal Gate Status Report

This file is a read-only formal-gate status report. It does not execute commands, run remote preflight, train, evaluate, sync, audit, pull back artifacts, or write paper results.

- status: `formal_gate_status_blocked`
- source_head: `9da971896cb9c2b977aaa2bc30fa749f7af4f5a5+dirty`
- input_safety_issue_count: `0`
- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Current State

- decision_status: `approved`
- decision_decider: `Dr Sun`
- decision_remote_preflight_allowed_now: `False`
- decision_remote_training_allowed_now: `False`
- decision_intake_status: `f02_6_decision_intake_closed_clean`
- decision_intake_record_status: `approved`
- decision_intake_next_blocked_lane: `remote_packet_preflight`
- decision_intake_audit_issue_count: `0`
- decision_intake_valid_decision_count: `2`
- decision_intake_required_record_field_count: `3`
- decision_intake_decision_note_required: `True`
- decision_intake_record_command_template_count: `2`
- decision_intake_post_decision_non_authorization_count: `4`
- decision_intake_post_decision_route_count: `2`
- decision_intake_remote_preflight_allowed_now: `True`
- decision_intake_remote_training_allowed_now: `True`
- decision_intake_formal_claim_allowed_now: `False`
- decision_intake_packet_authorization_status: `blocked_until_dr_sun_decision`
- decision_intake_packet_current_allowed_action_ids: `['record_f02_6_decision']`
- decision_intake_packet_current_blocked_action_ids: `['remote_preflight', 'remote_training', 'local_training', 'formal_claim', 'paper_result_material']`
- decision_intake_packet_post_decision_routes_are_current_authorization: `False`
- decision_intake_packet_remote_preflight_allowed_now: `False`
- decision_intake_packet_remote_training_allowed_now: `False`
- decision_intake_packet_paper_result_material_allowed_now: `False`
- decision_intake_record_authorization_status: `decision_recorded_not_execution_authorization`
- decision_intake_record_authorization_current_blocked_action_ids: `['remote_preflight', 'remote_training', 'local_training', 'formal_claim', 'paper_result_material']`
- decision_intake_record_authorization_post_decision_routes_are_current_authorization: `False`
- decision_intake_record_authorization_remote_preflight_allowed_now: `False`
- decision_intake_record_authorization_remote_training_allowed_now: `False`
- decision_intake_record_authorization_formal_claim_allowed_now: `False`
- decision_intake_record_authorization_paper_result_material_allowed_now: `False`
- decision_intake_record_post_decision_non_authorization_count: `4`
- decision_intake_next_request_status: `decision_recorded`
- decision_intake_next_request_current_allowed_action_ids: `['record_f02_6_decision']`
- decision_intake_next_request_current_blocked_action_ids: `['remote_preflight', 'remote_training', 'local_training', 'formal_claim', 'paper_result_material']`
- decision_intake_next_request_post_decision_routes_are_current_authorization: `False`
- decision_intake_next_request_all_execution_disabled_now: `False`
- decision_intake_decision_impact_present: `True`
- decision_intake_decision_impact_current_blocker: `remote_packet_preflight`
- decision_intake_decision_impact_missing_deliverable_count: `1`
- decision_intake_decision_record_is_not_training_authorization: `True`
- decision_intake_decision_record_is_not_paper_result_material: `True`
- decision_intake_decision_impact_remote_preflight_allowed_now: `False`
- decision_intake_decision_impact_remote_training_allowed_now: `False`
- decision_intake_decision_impact_formal_claim_allowed_now: `False`
- decision_intake_decision_impact_paper_result_material_allowed_now: `False`
- decision_intake_evidence_matrix_status: `ready_for_dr_sun_decision_not_authorization`
- decision_intake_evidence_matrix_route_count: `2`
- decision_intake_evidence_matrix_required_evidence_count: `7`
- decision_intake_evidence_matrix_missing_required_evidence_count: `0`
- decision_intake_evidence_matrix_remote_training_allowed_now: `False`
- formal_gate_status: `blocked_formal_gate_gaps_open`
- missing_artifacts_status: `formal_gate_missing_artifacts_open`
- missing_artifacts_handoff_index_status: `blocked_until_protocol_lane_decision`
- missing_artifacts_handoff_next_action: `record_protocol_lane_decision`
- missing_artifacts_handoff_open_requirement_count: `1`
- missing_artifacts_handoff_remote_training_allowed_now: `False`
- missing_artifacts_handoff_formal_result_material_allowed_now: `False`
- closure_checklist_status: `formal_gate_closure_blocked`
- closure_open_item_count: `7`
- closure_remote_preflight_allowed_now: `True`
- closure_remote_training_allowed_now: `True`
- closure_remote_audit_pullback_allowed_now: `False`
- remote_packet_status: `ready_for_gpu3070ti_remote_training`
- ready_to_run_remote_training: `True`
- remote_packet_sync_allowed_now: `True`
- remote_packet_preflight_allowed_now: `True`
- remote_packet_training_allowed_now: `True`
- remote_packet_audit_allowed_now: `False`
- remote_preflight_requirement_satisfied_count: `4`
- remote_preflight_requirement_blocked_count: `0`
- post_run_acceptance_requirement_satisfied_count: `0`
- post_run_acceptance_requirement_blocked_count: `4`
- h01_status: `ready_for_formal_run`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_formal_acceptance_requirement_satisfied_count: `1`
- h02_formal_acceptance_requirement_blocked_count: `3`
- claim_safety_status: `blocked_formal_performance_claims`
- claim_safety_formal_performance_claim_allowed: `False`
- paper_readiness_status: `partial_methods_ready_results_blocked`
- paper_readiness_formal_results_ready: `False`
- handoff_bundle_status: `blocked_until_protocol_lane_decision`
- remaining_deliverables_status: `formal_gate_deliverables_blocked`
- remaining_deliverables_missing_deliverable_count: `1`
- remaining_deliverables_acceptance_matrix_count: `10`
- remaining_deliverables_acceptance_missing_row_count: `1`
- remaining_deliverables_acceptance_blocked_category_count: `1`
- remaining_deliverables_unlock_chain_present: `True`
- remaining_deliverables_unlock_chain_row_count: `10`
- remaining_deliverables_unlock_chain_blocked_row_count: `1`
- remaining_deliverables_unlock_chain_rows_with_missing_required_blockers: `0`
- remaining_deliverables_unlock_chain_rows_allowed_while_missing: `0`
- remaining_deliverables_gap_total_missing_deliverable_count: `1`
- remaining_deliverables_gap_open_category_count: `1`
- next_required_formal_deliverable_count: `1`
- next_required_formal_deliverable_blocked_category_count: `1`
- remaining_deliverables_proof_plan_present: `True`
- remaining_deliverables_proof_plan_matrix_row_count: `10`
- remaining_deliverables_proof_plan_command_count: `20`
- remaining_deliverables_source_blocker_summary_present: `True`
- remaining_deliverables_source_blocker_count: `18`
- remaining_deliverables_source_blocker_ids: `['f02_6_decision_gate_audit', 'f02_6_decision_intake', 'f02_6_decision_record', 'f02_6_transition_gate_audit', 'f02_6_warm_start_decision_packet', 'formal_gate_closure_checklist', 'gpu3070ti_readiness_refresh', 'post_f02_6_plan_audit', 'post_f02_6_regeneration_plan', 'remote_formal_execution_packet', 'remote_packet_safety_audit', 'h01_evaluation_manifest', 'h02_formal_acceptance', 'claim_safety', 'formal_gate_proof_audit', 'formal_gate_proof_summary_chain_audit', 'mainline_formal_gate_state_audit', 'paper_readiness']`
- remaining_deliverables_remote_readiness_blocker_count: `1`
- remaining_deliverables_remote_readiness_refresh_requires_external_ssh: `True`
- remaining_deliverables_remote_readiness_refresh_allowed_now: `False`
- formal_gate_proof_audit_status: `formal_gate_proof_audit_blocked`
- formal_gate_proof_audit_command_count: `20`
- formal_gate_proof_audit_passed_count: `19`
- formal_gate_proof_audit_failed_count: `1`
- formal_gate_proof_audit_blocked_count: `0`
- formal_gate_proof_audit_missing_artifact_count: `0`
- formal_gate_proof_audit_failed_acceptance_artifact_count: `1`
- formal_gate_proof_audit_training_missing_artifact_count: `0`
- formal_gate_proof_audit_evaluation_missing_artifact_count: `0`
- formal_gate_proof_audit_acceptance_missing_artifact_count: `0`
- formal_gate_proof_audit_formal_acceptance_failed_artifact_count: `1`
- mainline_formal_gate_state_audit_status: `mainline_formal_gate_state_consistent_blocked`
- mainline_formal_gate_state_audit_issue_count: `0`
- mainline_formal_gate_state_audit_proof_summary_chain_status: `formal_gate_proof_summary_chain_consistent_blocked`
- mainline_formal_gate_state_audit_proof_summary_chain_issue_count: `0`
- mainline_formal_gate_state_audit_proof_audit_input_safety_issue_count: `0`
- handoff_bundle_next_action: `record_protocol_lane_decision`
- handoff_bundle_safety_issue_count: `0`
- handoff_bundle_remote_training_allowed_now: `False`
- handoff_requirement_stage_mapped_count: `4`
- handoff_requirement_stage_unmapped_count: `0`
- formal_gate_execution_veto_present: `True`
- formal_gate_execution_veto_all_rows_consistent: `True`
- formal_gate_execution_veto_remote_training_allowed_now: `False`
- formal_gate_execution_veto_formal_claim_allowed_now: `False`
- formal_gate_gap_audit_remaining_total_missing_deliverables: `1`
- formal_gate_gap_audit_remaining_open_category_count: `1`
- remote_packet_safety_proof_summary_present: `True`
- remote_packet_safety_proof_training_missing_count: `0`
- remote_packet_safety_proof_evaluation_missing_count: `0`
- remote_packet_safety_proof_acceptance_missing_count: `0`
- remote_packet_safety_proof_formal_acceptance_missing_count: `1`
- remote_packet_safety_proof_next_blocked_lane: `source_fresh_preflight`
- remote_packet_safety_proof_h02_paper_result_input_allowed: `False`
- remote_packet_safety_status_report_proof_summary_present: `True`
- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_blocking_regeneration_required: `True`
- source_freshness_non_self_changed_records: `23`
- source_freshness_self_artifact_only_lag_records: `0`
- remote_packet_safety_command_index_present: `True`
- remote_packet_safety_command_index_row_count: `23`
- remote_packet_safety_command_index_source_target_count: `23`
- remote_packet_safety_command_index_missing_target_count: `0`
- next_action_guard_status: `next_action_guard_not_applicable`

## Next Blocked Lane

- lane_id: `source_fresh_preflight`
- phase: `regeneration`
- blocked_by: `source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit`
- action: After F02.6 closes, regenerate source-fresh gate artifacts before approved preflight.

## F02.6 Decision Intake

- present: `True`
- status: `f02_6_decision_intake_closed_clean`
- record_status: `approved`
- record_decider: `Dr Sun`
- effective_warm_start_decision: `approved_obstacle_summary`
- next_blocked_lane: `remote_packet_preflight`
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
- missing_deliverable_count: `1`
- remote_preflight_allowed_now: `True`
- remote_training_allowed_now: `True`
- formal_claim_allowed_now: `False`
- decision_impact_present: `True`
- decision_impact_summary_id: `module2_f02_6_formal_gate_decision_impact`
- decision_impact_current_blocker: `remote_packet_preflight`
- decision_impact_missing_deliverable_count: `1`
- decision_evidence_matrix_status: `ready_for_dr_sun_decision_not_authorization`
- decision_evidence_matrix_route_count: `2`
- decision_evidence_matrix_required_evidence_count: `7`
- decision_evidence_matrix_missing_required_evidence_count: `0`
- decision_evidence_matrix_remote_training_allowed_now: `False`
- decision_record_is_not_training_authorization: `True`
- decision_record_is_not_paper_result_material: `True`
- decision_impact_remote_preflight_allowed_now: `False`
- decision_impact_remote_training_allowed_now: `False`
- decision_impact_formal_claim_allowed_now: `False`
- decision_impact_paper_result_material_allowed_now: `False`
- decision_impact_formal_training_still_requires: `source_freshness_audit, post_f02_6_regeneration_plan, post_f02_6_plan_audit, remote_formal_execution_packet_ready, approved_remote_preflight`

## Next Action Guard

- present: `True`
- status: `next_action_guard_not_applicable`
- pending_f02_6_decision: `False`
- expected_next_action_id: `None`
- handoff_next_action_id: `record_protocol_lane_decision`
- missing_artifacts_next_action_id: `record_protocol_lane_decision`
- all_execution_disabled_now: `False`
- execution_leak_count: `8`
- remote_execution_allowed_count: `3`
- remote_stage_allowed_count: `2`
- violations: `none`

## Formal Gate Lanes

- `decision` (decision): status=`complete`, missing=`0`, runs_training=`False`
  - completion_signal: F02.6 decision record is approved or rejected by Dr Sun.
  - action_when_blocked: Record Dr Sun's F02.6 decision before any formal preflight or training.
- `source_fresh_preflight` (regeneration): status=`blocked`, missing=`22`, runs_training=`False`
  - blocked_by: `source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit`
  - completion_signal: Source-fresh preflight targets are regenerated from the current head.
  - action_when_blocked: After F02.6 closes, regenerate source-fresh gate artifacts before approved preflight.
- `remote_packet_preflight` (remote_preflight): status=`blocked`, missing=`4`, runs_training=`False`
  - blocked_by: `f02_6_decision_record, gate3_remote_audit_pullback, regenerate_h01_h02_formal_artifacts, regenerate_claim_gate_artifacts, source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit`
  - completion_signal: Approved gpu3070ti preflight passes and remote packet reports ready.
  - action_when_blocked: Run only approved remote preflight after F02.6 and source freshness close.
- `gate3_remote_training` (training): status=`blocked`, missing=`0`, runs_training=`True`, host=`gpu3070ti-relay`
  - blocked_by: `source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit`
  - completion_signal: final_model.zip, train summary, and training manifest are pulled back.
  - action_when_blocked: Run formal PPO only on gpu3070ti-relay after remote packet is ready.
- `gate3_eval_and_audit_pullback` (acceptance): status=`blocked`, missing=`0`, runs_training=`False`
  - blocked_by: `source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit, missing_ppo_result_rows, missing_ppo_checkpoint_hash, handoff_safety_issues_open, remote_training_not_completed`
  - completion_signal: Gate3 eval outputs, trial manifest, formal audit, and checkpoint hash are present.
  - action_when_blocked: Audit remote trial and pull back the complete trial directory with hashes.
- `h01_h02_formal_evaluation` (evaluation_acceptance): status=`blocked`, missing=`1`, runs_training=`False`
  - blocked_by: `h02_formal_output_acceptance, source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit, missing_ppo_result_rows, missing_ppo_checkpoint_hash, h02_scale_below_h01_queries_per_bucket, h02_scale_below_h01_seed_count, h02_scale_below_h01_queries_per_map, h02_verdict_not_formal, handoff_safety_issues_open, missing_remote_audit_pullback`
  - completion_signal: H01 is ready and H02 accepts formal-scale PPO outputs.
  - action_when_blocked: Regenerate H01/H02 only after audited checkpoint pullback is complete.
- `claim_gate` (claim_gate): status=`blocked`, missing=`8`, runs_training=`False`
  - blocked_by: `claim_safety, formal_gate_proof_audit, formal_gate_proof_summary_chain_audit, formal_gate_remaining_deliverables, formal_gate_status_report, mainline_formal_gate_state_audit, paper_readiness, h02_formal_acceptance_before_claim_gate, source_freshness_regeneration_required, handoff_step_allowed_mismatch_sync_to_remote, handoff_step_blockers_mismatch_sync_to_remote, handoff_step_allowed_mismatch_run_remote_preflight, handoff_step_blockers_mismatch_run_remote_preflight, handoff_step_allowed_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_training, handoff_step_blockers_mismatch_run_remote_audit, missing_ppo_result_rows, missing_ppo_checkpoint_hash, h02_scale_below_h01_queries_per_bucket, h02_scale_below_h01_seed_count, h02_scale_below_h01_queries_per_map, h02_verdict_not_formal, missing_or_failed_gate3_formal_audit, h02_formal_output_not_accepted, claim_safety_blocks_formal_performance, readiness_blocks_formal_results, formal_gate_missing_artifacts_open, formal_gate_closure_checklist_open, formal_gate_status_report_blocked, formal_gate_remaining_deliverables_open, handoff_safety_issues_open, h02_formal_acceptance_not_ready`
  - completion_signal: Claim safety and paper readiness allow formal results after H02 acceptance.
  - action_when_blocked: Regenerate claim gates only after H02 formal acceptance passes.

## Remote Execution Steps

- `sync_to_remote`: present=`True`, allowed_now=`True`, runs_training=`False`, blocked_by=`none`
- `run_remote_preflight`: present=`True`, allowed_now=`True`, runs_training=`False`, blocked_by=`none`
- `run_remote_training`: present=`True`, allowed_now=`True`, runs_training=`True`, blocked_by=`none`
- `run_remote_audit`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`remote_training_not_completed`

## Remote Preflight Requirement Matrix

- present: `True`
- status_counts: `{'satisfied': 4}`
- blocked_requirement_count: `0`
- `f02_6_decision_closed_for_preflight`: status=`satisfied`, complete=`True`, execution_allowed_now=`True`, blocked_by=`none`
- `approved_remote_preflight_manifest`: status=`satisfied`, complete=`True`, execution_allowed_now=`True`, blocked_by=`none`
- `remote_preflight_protocol_contract`: status=`satisfied`, complete=`True`, execution_allowed_now=`True`, blocked_by=`none`
- `remote_preflight_command_packetized`: status=`satisfied`, complete=`True`, execution_allowed_now=`True`, blocked_by=`none`

## Post-Run Acceptance Requirement Matrix

- present: `True`
- status_counts: `{'blocked_until_remote_audit': 4}`
- blocked_requirement_count: `4`
- `pullback_expected_artifacts_complete`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`True`
- `checkpoint_hash_manifest_recorded`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`True`
- `gate3_formal_audit_accepts_remote_run`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`True`
- `h01_h02_regenerated_from_audited_checkpoint`: status=`blocked_until_remote_audit`, complete=`False`, remote_training_ready_now=`True`

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
- missing_row_count: `1`
- blocked_category_count: `1`
- `training:train_final_model_zip`: missing=`False`, current_state=`present`, stage=`gate3_remote_training`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`4`, blocked_by=`protocol_lane_decision_pending, f02_6_decision_not_approved, remote_packet_not_ready`
- `training:train_summary_json`: missing=`False`, current_state=`present`, stage=`gate3_remote_training`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`4`, blocked_by=`protocol_lane_decision_pending, f02_6_decision_not_approved, remote_packet_not_ready`
- `training:train_training_manifest_json`: missing=`False`, current_state=`present`, stage=`gate3_remote_training`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`4`, blocked_by=`protocol_lane_decision_pending, f02_6_decision_not_approved, remote_packet_not_ready`
- `evaluation:eval_gate3_eval_episodes_csv`: missing=`False`, current_state=`present`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `evaluation:eval_gate3_summary_json`: missing=`False`, current_state=`present`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `acceptance:gate3_trial_manifest_json`: missing=`False`, current_state=`present`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `acceptance:gate3_formal_audit_json`: missing=`False`, current_state=`present`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `acceptance:pulled_back_checkpoint_hash_record`: missing=`False`, current_state=`present`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `formal_acceptance:h01_ready_for_formal_run`: missing=`False`, current_state=`ready_for_formal_run`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`protocol_lane_decision_pending, missing_remote_audit_pullback`
- `formal_acceptance:h02_formal_output_acceptance`: missing=`True`, current_state=`blocked_formal_output_acceptance`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, acceptance_predicate_count=`5`, proof_command_count=`2`, invalid_substitute_count=`3`, blocked_by=`protocol_lane_decision_pending, missing_remote_audit_pullback`

## Remaining Deliverables Gap Summary

- present: `True`
- summary_id: `module2_formal_gate_missing_training_eval_acceptance_summary`
- total_missing_deliverables: `1`
- open_category_count: `1`
- execution_boundary: `read_only_no_execution`
- `training`: missing_count=`0`, stage=`gate3_remote_training`, stage_allowed_now=`False`, missing_artifacts=`none`, proof_commands=`none`, blocked_by=`protocol_lane_decision_pending, f02_6_decision_not_approved, remote_packet_not_ready`
- `evaluation`: missing_count=`0`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, missing_artifacts=`none`, proof_commands=`none`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `acceptance`: missing_count=`0`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, missing_artifacts=`none`, proof_commands=`none`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `formal_acceptance`: missing_count=`1`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, missing_artifacts=`formal_acceptance:h02_formal_output_acceptance`, proof_commands=`h02_formal_output_acceptance_exists_nonempty, h02_formal_output_acceptance_status`, blocked_by=`protocol_lane_decision_pending, missing_remote_audit_pullback`

## Remaining Deliverables Unlock Chain

- present: `True`
- chain_id: `module2_formal_gate_missing_deliverable_unlock_chain`
- status: `blocked_missing_formal_deliverables`
- row_count: `10`
- blocked_row_count: `1`
- rows_with_missing_required_blockers: `0`
- rows_allowed_while_missing: `0`
- `training`: row_count=`3`, blocked_row_count=`0`, rows_with_missing_required_blockers=`0`, rows_allowed_while_missing=`0`, blockers=`f02_6_decision_not_approved, remote_packet_not_ready`
- `evaluation`: row_count=`2`, blocked_row_count=`0`, rows_with_missing_required_blockers=`0`, rows_allowed_while_missing=`0`, blockers=`remote_training_not_completed`
- `acceptance`: row_count=`3`, blocked_row_count=`0`, rows_with_missing_required_blockers=`0`, rows_allowed_while_missing=`0`, blockers=`remote_training_not_completed`
- `formal_acceptance`: row_count=`2`, blocked_row_count=`1`, rows_with_missing_required_blockers=`0`, rows_allowed_while_missing=`0`, blockers=`missing_remote_audit_pullback`

## Next Required Formal Deliverables

- status: `blocked_missing_formal_deliverables`
- execution_boundary: `read_only_no_execution`
- not_paper_result_material: `True`
- runs_training: `False`
- runs_remote_preflight: `False`
- total_missing_deliverables: `1`
- blocked_categories: `formal_acceptance`
- `formal_acceptance:h02_formal_output_acceptance`: category=`formal_acceptance`, artifact=`h02_formal_output_acceptance`, expected_path=`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`, current_state=`blocked_formal_output_acceptance`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, proof_commands=`h02_formal_output_acceptance_exists_nonempty, h02_formal_output_acceptance_status`, invalid_substitute_count=`3`, blocked_by=`protocol_lane_decision_pending, missing_remote_audit_pullback`

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

## Remaining Deliverables Source Blocker Summary

- present: `True`
- summary_id: `module2_source_freshness_blocking_targets_summary`
- blocking_target_count: `18`
- blocking_target_ids: `f02_6_decision_gate_audit, f02_6_decision_intake, f02_6_decision_record, f02_6_transition_gate_audit, f02_6_warm_start_decision_packet, formal_gate_closure_checklist, gpu3070ti_readiness_refresh, post_f02_6_plan_audit, post_f02_6_regeneration_plan, remote_formal_execution_packet, remote_packet_safety_audit, h01_evaluation_manifest, h02_formal_acceptance, claim_safety, formal_gate_proof_audit, formal_gate_proof_summary_chain_audit, mainline_formal_gate_state_audit, paper_readiness`
- remote_readiness_blocking_target_count: `1`
- remote_readiness_refresh_requires_external_ssh: `True`
- remote_readiness_refresh_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- `f02_6_decision_gate_audit`: path=`0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `f02_6_decision_intake`: path=`0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `f02_6_decision_record`: path=`0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `f02_6_transition_gate_audit`: path=`0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`10`
- `f02_6_warm_start_decision_packet`: path=`0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `formal_gate_closure_checklist`: path=`0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `gpu3070ti_readiness_refresh`: path=`0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `post_f02_6_plan_audit`: path=`0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `post_f02_6_regeneration_plan`: path=`0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `remote_formal_execution_packet`: path=`0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `remote_packet_safety_audit`: path=`0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`, freshness_state=`historical_clean`, required_before=`approved_remote_preflight`, blocking_changed_path_count_since_source=`43`
- `h01_evaluation_manifest`: path=`0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`, freshness_state=`historical_clean`, required_before=`formal_h01_h02`, blocking_changed_path_count_since_source=`43`
- `h02_formal_acceptance`: path=`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`, freshness_state=`historical_clean`, required_before=`formal_h01_h02`, blocking_changed_path_count_since_source=`43`
- `claim_safety`: path=`0_trials/module2_claim_safety/module2_claim_safety.json`, freshness_state=`historical_clean`, required_before=`formal_claim_gate`, blocking_changed_path_count_since_source=`43`
- `formal_gate_proof_audit`: path=`0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`, freshness_state=`historical_clean`, required_before=`formal_claim_gate`, blocking_changed_path_count_since_source=`43`
- `formal_gate_proof_summary_chain_audit`: path=`0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`, freshness_state=`historical_clean`, required_before=`formal_claim_gate`, blocking_changed_path_count_since_source=`43`
- `mainline_formal_gate_state_audit`: path=`0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`, freshness_state=`historical_clean`, required_before=`formal_claim_gate`, blocking_changed_path_count_since_source=`11`
- `paper_readiness`: path=`0_trials/module2_paper_readiness/module2_paper_readiness.json`, freshness_state=`historical_clean`, required_before=`formal_claim_gate`, blocking_changed_path_count_since_source=`43`

## Formal Gate Proof Audit Gap Summary

- present: `True`
- status: `formal_gate_proof_audit_blocked`
- missing_artifact_count=`0`
- failed_acceptance_artifact_count=`1`
- `training`: missing_artifact_count=`0`, failed_acceptance_artifact_count=`0`, blocked_proof_command_count=`0`, failed_proof_command_count=`0`, missing_artifacts=`none`, failed_artifacts=`none`, blocked_commands=`none`, failed_commands=`none`
- `evaluation`: missing_artifact_count=`0`, failed_acceptance_artifact_count=`0`, blocked_proof_command_count=`0`, failed_proof_command_count=`0`, missing_artifacts=`none`, failed_artifacts=`none`, blocked_commands=`none`, failed_commands=`none`
- `acceptance`: missing_artifact_count=`0`, failed_acceptance_artifact_count=`0`, blocked_proof_command_count=`0`, failed_proof_command_count=`0`, missing_artifacts=`none`, failed_artifacts=`none`, blocked_commands=`none`, failed_commands=`none`
- `formal_acceptance`: missing_artifact_count=`0`, failed_acceptance_artifact_count=`1`, blocked_proof_command_count=`0`, failed_proof_command_count=`1`, missing_artifacts=`none`, failed_artifacts=`h02_formal_output_acceptance`, blocked_commands=`none`, failed_commands=`h02_formal_output_acceptance_status`

## Formal Gate Proof Audit

- present: `True`
- status: `formal_gate_proof_audit_blocked`
- total_matrix_rows: `10`
- total_proof_command_count: `20`
- passed_proof_command_count: `19`
- failed_proof_command_count: `1`
- blocked_proof_command_count: `0`
- remaining_deliverables_summary_present: `True`
- remaining_missing_counts_by_formal_category: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- remaining_next_blocked_lane: `source_fresh_preflight`
- remaining_h01_status: `ready_for_formal_run`
- remaining_h02_status: `blocked_formal_output_acceptance`
- remaining_training_missing_matrix_ids: `none`
- remaining_evaluation_missing_matrix_ids: `none`
- remaining_acceptance_missing_matrix_ids: `none`
- remaining_formal_acceptance_missing_matrix_ids: `formal_acceptance:h02_formal_output_acceptance`
- `train_final_model_zip_exists_nonempty`: status=`passed`, matrix_id=`training:train_final_model_zip`
- `train_final_model_zip_valid_zip`: status=`passed`, matrix_id=`training:train_final_model_zip`
- `train_summary_json_exists_nonempty`: status=`passed`, matrix_id=`training:train_summary_json`
- `train_summary_json_formal_warm_start_metadata`: status=`passed`, matrix_id=`training:train_summary_json`
- `train_training_manifest_json_exists_nonempty`: status=`passed`, matrix_id=`training:train_training_manifest_json`
- `train_training_manifest_json_provenance`: status=`passed`, matrix_id=`training:train_training_manifest_json`
- `eval_gate3_eval_episodes_csv_exists_nonempty`: status=`passed`, matrix_id=`evaluation:eval_gate3_eval_episodes_csv`
- `eval_gate3_eval_episodes_csv_schema`: status=`passed`, matrix_id=`evaluation:eval_gate3_eval_episodes_csv`
- `eval_gate3_summary_json_exists_nonempty`: status=`passed`, matrix_id=`evaluation:eval_gate3_summary_json`
- `eval_gate3_summary_json_formal_scope`: status=`passed`, matrix_id=`evaluation:eval_gate3_summary_json`
- `gate3_trial_manifest_json_exists_nonempty`: status=`passed`, matrix_id=`acceptance:gate3_trial_manifest_json`
- `gate3_trial_manifest_json_formal_warm_start_scope`: status=`passed`, matrix_id=`acceptance:gate3_trial_manifest_json`
- `gate3_formal_audit_json_exists_nonempty`: status=`passed`, matrix_id=`acceptance:gate3_formal_audit_json`
- `gate3_formal_audit_json_accepts_formal_scope`: status=`passed`, matrix_id=`acceptance:gate3_formal_audit_json`
- `pulled_back_checkpoint_hash_record_exists_nonempty`: status=`passed`, matrix_id=`acceptance:pulled_back_checkpoint_hash_record`
- `pulled_back_checkpoint_hash_record_matches_model`: status=`passed`, matrix_id=`acceptance:pulled_back_checkpoint_hash_record`
- `h01_ready_for_formal_run_exists_nonempty`: status=`passed`, matrix_id=`formal_acceptance:h01_ready_for_formal_run`
- `h01_ready_for_formal_run_status`: status=`passed`, matrix_id=`formal_acceptance:h01_ready_for_formal_run`
- `h02_formal_output_acceptance_exists_nonempty`: status=`passed`, matrix_id=`formal_acceptance:h02_formal_output_acceptance`
- `h02_formal_output_acceptance_status`: status=`failed`, matrix_id=`formal_acceptance:h02_formal_output_acceptance`

## Mainline Formal Gate State Audit

- present: `True`
- status: `mainline_formal_gate_state_consistent_blocked`
- audit_issue_count: `0`
- proof_summary_chain_status: `formal_gate_proof_summary_chain_consistent_blocked`
- proof_summary_chain_audit_issue_count: `0`
- proof_summary_chain_proof_audit_input_safety_issue_count: `0`
- proof_summary_chain_proof_audit_blockers: `failed_formal_h01_h02_acceptance_artifacts`

## Formal Gate Gap Audit Remaining Deliverables Gap Summary

- present: `True`
- summary_id: `module2_formal_gate_missing_training_eval_acceptance_summary`
- total_missing_deliverables: `1`
- open_category_count: `1`
- matches_ledger_signature: `True`

## Remote Packet Safety Proof Deliverables Summary

- proof_summary_present: `True`
- proof_missing_counts_by_formal_category: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- proof_next_blocked_lane: `source_fresh_preflight`
- proof_h01_status: `ready_for_formal_run`
- proof_h02_status: `blocked_formal_output_acceptance`
- proof_h02_paper_result_input_allowed: `False`
- status_report_proof_summary_present: `True`
- status_report_proof_matches_remote_proof: `True`
- remote_proof_matches_proof_audit: `True`
- remote_proof_training_missing_matrix_ids: `none`
- remote_proof_evaluation_missing_matrix_ids: `none`
- remote_proof_acceptance_missing_matrix_ids: `none`
- remote_proof_formal_acceptance_missing_matrix_ids: `formal_acceptance:h02_formal_output_acceptance`

## Remote Packet Safety Claim-Gate Command Index

- present: `True`
- index_row_count: `23`
- source_target_count: `23`
- missing_target_ids: `[]`
- unknown_manual_count: `0`
- forbidden_command_count: `0`
- `formal_gate_proof_summary_chain_audit`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`
- `mainline_formal_gate_state_audit`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`
- `claim_safety`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`
- `paper_readiness`: present=`True`, stage=`regenerate_claim_gate_artifacts`, required_before=`formal_claim_gate`, command_kind=`known_builder`

## Closure Remote Stages

- `approved_remote_preflight`: present=`True`, allowed_now=`True`, runs_training=`False`, runs_remote_preflight=`True`, host=`gpu3070ti-relay`, blocked_by=`none`
- `gate3_remote_training`: present=`True`, allowed_now=`True`, runs_training=`True`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`, blocked_by=`none`
- `gate3_remote_audit_pullback`: present=`True`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`, blocked_by=`remote_training_not_completed`

## Missing-Artifacts Handoff Index

- present: `True`
- status: `blocked_until_protocol_lane_decision`
- next_action: `record_protocol_lane_decision`
- next_action_requires_dr_sun: `True`
- open_requirement_count: `1`
- local_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_result_material_allowed_now: `False`

## Formal Gate Handoff Bundle

- present: `True`
- status: `blocked_until_protocol_lane_decision`
- next_handoff_action: `record_protocol_lane_decision`
- safety_issue_count: `0`
- remote_training_allowed_now: `False`
- `sync_to_remote`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_preflight`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_training`: present=`True`, allowed_now=`False`, runs_training=`True`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_audit`: present=`True`, allowed_now=`False`, runs_training=`False`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`

## Formal Gate Requirement Stage Summary

- mapped_requirement_count: `4`
- unmapped_requirement_count: `0`
- mismatched_requirement_count: `0`
- `training_remote_ppo_checkpoint`: expected_stage=`gate3_remote_training`, responsible_stage=`gate3_remote_training`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- `evaluation_gate3_episode_outputs`: expected_stage=`gate3_remote_audit_pullback`, responsible_stage=`gate3_remote_audit_pullback`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `acceptance_remote_pullback_and_audit`: expected_stage=`gate3_remote_audit_pullback`, responsible_stage=`gate3_remote_audit_pullback`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- `h01_h02_formal_evaluation_acceptance`: expected_stage=`regenerate_h01_h02_formal_artifacts`, responsible_stage=`regenerate_h01_h02_formal_artifacts`, stage_status=`blocked`, stage_allowed_now=`False`, blocked_by=`missing_remote_audit_pullback`

## Formal Gate Execution Veto Matrix

- present: `True`
- all_rows_consistent: `True`
- mismatch_rows: `[]`
- `local_training`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'formal_gate_gap_audit': False, 'protocol_lane_status': False, 'status_report': False, 'handoff_bundle': False}`
- `remote_preflight`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'protocol_lane_status': False, 'status_report': False, 'handoff_bundle': False, 'remote_packet_superseded_by_protocol_lane': None, 'remote_packet_safety_superseded_by_protocol_lane': None}`
- `remote_training`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'protocol_lane_status': False, 'decision_record_superseded_by_protocol_lane': None, 'status_report': False, 'handoff_bundle': False, 'remote_packet_superseded_by_protocol_lane': None, 'remote_packet_safety_superseded_by_protocol_lane': None}`
- `remote_audit`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'protocol_lane_status': False, 'handoff_bundle': False, 'remote_packet_superseded_by_protocol_lane': None, 'remote_packet_safety_superseded_by_protocol_lane': None}`
- `formal_claim`: consistent=`True`, consensus_allowed_now=`False`, sources=`{'protocol_lane_status': False, 'status_report': False, 'handoff_bundle': False}`

## Required Training Artifacts

- `train_final_model_zip`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
- `train_summary_json`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
- `train_training_manifest_json`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`

## Required Evaluation Artifacts

- `eval_gate3_eval_episodes_csv`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
- `eval_gate3_summary_json`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`

## Required Acceptance Artifacts

- `gate3_trial_manifest_json`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
- `gate3_formal_audit_json`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- `pulled_back_checkpoint_hash_record`: missing=`False`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`

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
