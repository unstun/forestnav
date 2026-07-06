# Module2 Formal Gate Handoff Bundle

- status: `blocked_until_protocol_lane_decision`
- executes commands: `False`
- runs training: `False`
- local training allowed: `False`
- next action: `record_protocol_lane_decision`

## Single Next Action Index

- index_id: `module2_formal_gate_single_next_action_index`
- status: `awaiting_dr_sun_protocol_lane_decision`
- single_current_human_entry: `True`
- next_action_id: `record_protocol_lane_decision`
- decision_owner_required: `Dr Sun`
- valid_decisions: `stronger_obstacle_summary_warm_start, full_patch_cnn_policy, hybrid_ppo_analytic_fallback, stop_or_reframe_module2_claim`
- required_record_fields: `selected_lane_id, decision_note, failed_gate3_basis, contract_action, rejected_lane_rationales, evidence_artifact_basis`
- current_allowed_action_ids: `record_protocol_lane_decision`
- current_blocked_action_ids: `local_training, remote_success_training, remote_preflight_for_new_success_attempt, formal_claim, paper_result_material`
- legacy_f02_6_decision_action_ids: `record_f02_6_decision`
- legacy_f02_6_decision_superseded_by_protocol_lane: `True`
- all_execution_disabled_now: `True`
- record_command_template_count: `0`
- missing_deliverable_count: `1`
- missing_by_category: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_blocking_regeneration_required: `True`
- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`
- approved_route_next_lane: `source_fresh_regeneration`
- rejected_route_next_lane: `protocol_redesign`
- after_approval_still_requires: `record_protocol_lane_decision, approved_or_frozen_new_or_revised_contract, source_freshness_audit, remote_formal_execution_packet_ready, approved_remote_preflight`

## Remote Steps

- `sync_to_remote`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_preflight`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_training`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_audit`: allowed_now=`False`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`

## F02.6 Route Handoff

- present: `True`
- post_decision_route_count: `2`
- post_decision_route_decisions: `approve_obstacle_summary_warm_start, reject_obstacle_summary_warm_start`
- approved_route_next_lane: `source_fresh_regeneration`
- approved_route_allows_remote_training_now: `False`
- rejected_route_next_lane: `protocol_redesign`
- rejected_route_requires_new_protocol_contract: `True`
- decision_impact_present: `True`
- decision_record_is_not_training_authorization: `True`
- decision_record_is_not_paper_result_material: `True`
- decision_impact_remote_training_allowed_now: `False`
- decision_impact_formal_claim_allowed_now: `False`
- decision_impact_paper_result_material_allowed_now: `False`
- decision_impact_formal_training_still_requires: `source_freshness_audit, post_f02_6_regeneration_plan, post_f02_6_plan_audit, remote_formal_execution_packet_ready, approved_remote_preflight`

## F02.6 Decision Evidence Matrix

- present: `True`
- matrix_id: `module2_f02_6_decision_evidence_matrix`
- status: `ready_for_dr_sun_decision_not_authorization`
- route_count: `2`
- route_decisions: `approve_obstacle_summary_warm_start, reject_obstacle_summary_warm_start`
- required_evidence_count: `7`
- missing_required_evidence_count: `0`
- global_invalid_substitute_count: `4`
- authorization_flags: `{'current_authorization_allowed_now': False, 'remote_preflight_allowed_now': False, 'remote_training_allowed_now': False, 'local_training_allowed_now': False, 'formal_claim_allowed_now': False, 'paper_result_material_allowed_now': False}`

## Source Freshness Gate

- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_non_self_changed_records: `23`
- source_freshness_self_artifact_only_lag_records: `0`

## Protocol Lane Gate

- status: `protocol_lane_status_blocked_pending_lane_decision`
- next_blocked_lane: `protocol_lane_decision`
- decision_record_status: `pending_protocol_lane_decision`
- selected_lane_id: `None`
- allowed_next_action_ids: `record_protocol_lane_decision`
- blocked_action_ids: `local_training, remote_success_training, remote_preflight_for_new_success_attempt, formal_claim, paper_result_material`

## Handoff Stages

- 1. `f02_6_decision_record`: allowed_now=`False`, blocked_by=`current_decision_status_approved`
- 2. `regenerate_preflight_gate_artifacts`: allowed_now=`True`, blocked_by=`none`
- 3. `approved_remote_preflight`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- 4. `regenerate_remote_execution_packet`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- 5. `gate3_remote_training`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending`
- 6. `gate3_remote_audit_pullback`: allowed_now=`False`, blocked_by=`remote_training_not_completed, protocol_lane_decision_pending`
- 7. `regenerate_h01_h02_formal_artifacts`: allowed_now=`False`, blocked_by=`missing_remote_audit_pullback, protocol_lane_decision_pending`
- 8. `regenerate_claim_gate_artifacts`: allowed_now=`False`, blocked_by=`h02_formal_acceptance_not_ready, protocol_lane_decision_pending`

## Requirement Summary

- remaining deliverables gap: total_missing=`1`, open_categories=`1`
  - `training`: missing=`0`, responsible_stage=`gate3_remote_training`
  - `evaluation`: missing=`0`, responsible_stage=`gate3_remote_audit_pullback`
  - `acceptance`: missing=`0`, responsible_stage=`gate3_remote_audit_pullback`
  - `formal_acceptance`: missing=`1`, responsible_stage=`regenerate_h01_h02_formal_artifacts`

## Status Report Proof-Audit Deliverables Summary

- present: `True`
- missing_counts_by_formal_category: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- next_blocked_lane: `source_fresh_preflight`
- h01_status: `ready_for_formal_run`
- h02_status: `blocked_formal_output_acceptance`
- training_missing_matrix_ids: `none`
- evaluation_missing_matrix_ids: `none`
- acceptance_missing_matrix_ids: `none`
- formal_acceptance_missing_matrix_ids: `formal_acceptance:h02_formal_output_acceptance`
- formal gate requirements: `4`
  - `training_remote_ppo_checkpoint`: status=`satisfied`, responsible_stage=`gate3_remote_training`
  - `evaluation_gate3_episode_outputs`: status=`satisfied`, responsible_stage=`gate3_remote_audit_pullback`
  - `acceptance_remote_pullback_and_audit`: status=`satisfied`, responsible_stage=`gate3_remote_audit_pullback`
  - `h01_h02_formal_evaluation_acceptance`: status=`blocked_missing_outputs`, responsible_stage=`regenerate_h01_h02_formal_artifacts`
- H02 acceptance requirements: `4`
- safety issues: `0`

This artifact is read-only and does not execute commands.
