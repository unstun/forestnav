# Module2 Formal Gate Handoff Bundle

- status: `blocked_until_f02_6_decision`
- executes commands: `False`
- runs training: `False`
- local training allowed: `False`
- next action: `record_f02_6_decision`

## Remote Steps

- `sync_to_remote`: allowed_now=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_preflight`: allowed_now=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_training`: allowed_now=`False`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_bc_checkpoint, missing_module2_rl_rs_checkpoint, realmap_query_generation_not_frozen, remote_packet_not_ready`
- `run_remote_audit`: allowed_now=`False`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_bc_checkpoint, missing_module2_rl_rs_checkpoint, realmap_query_generation_not_frozen, remote_packet_not_ready`

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

## Source Freshness Gate

- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_non_self_changed_records: `13`
- source_freshness_self_artifact_only_lag_records: `0`

## Handoff Stages

- 1. `f02_6_decision_record`: allowed_now=`True`, blocked_by=`none`
- 2. `regenerate_preflight_gate_artifacts`: allowed_now=`False`, blocked_by=`f02_6_decision_not_approved`
- 3. `approved_remote_preflight`: allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open`
- 4. `regenerate_remote_execution_packet`: allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open`
- 5. `gate3_remote_training`: allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- 6. `gate3_remote_audit_pullback`: allowed_now=`False`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- 7. `regenerate_h01_h02_formal_artifacts`: allowed_now=`False`, blocked_by=`missing_remote_audit_pullback`
- 8. `regenerate_claim_gate_artifacts`: allowed_now=`False`, blocked_by=`h02_formal_acceptance_not_ready, source_fresh_claim_targets_open`

## Requirement Summary

- remaining deliverables gap: total_missing=`10`, open_categories=`4`
  - `training`: missing=`3`, responsible_stage=`gate3_remote_training`
  - `evaluation`: missing=`2`, responsible_stage=`gate3_remote_audit_pullback`
  - `acceptance`: missing=`3`, responsible_stage=`gate3_remote_audit_pullback`
  - `formal_acceptance`: missing=`2`, responsible_stage=`regenerate_h01_h02_formal_artifacts`

## Status Report Proof-Audit Deliverables Summary

- present: `True`
- missing_counts_by_formal_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- next_blocked_lane: `decision`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- training_missing_matrix_ids: `training:train_final_model_zip, training:train_summary_json, training:train_training_manifest_json`
- evaluation_missing_matrix_ids: `evaluation:eval_gate3_eval_episodes_csv, evaluation:eval_gate3_summary_json`
- acceptance_missing_matrix_ids: `acceptance:gate3_trial_manifest_json, acceptance:gate3_formal_audit_json, acceptance:pulled_back_checkpoint_hash_record`
- formal_acceptance_missing_matrix_ids: `formal_acceptance:h01_ready_for_formal_run, formal_acceptance:h02_formal_output_acceptance`
- formal gate requirements: `4`
  - `training_remote_ppo_checkpoint`: status=`blocked_missing_outputs`, responsible_stage=`gate3_remote_training`
  - `evaluation_gate3_episode_outputs`: status=`blocked_missing_outputs`, responsible_stage=`gate3_remote_audit_pullback`
  - `acceptance_remote_pullback_and_audit`: status=`blocked_missing_outputs`, responsible_stage=`gate3_remote_audit_pullback`
  - `h01_h02_formal_evaluation_acceptance`: status=`blocked_missing_outputs`, responsible_stage=`regenerate_h01_h02_formal_artifacts`
- H02 acceptance requirements: `4`
- safety issues: `0`

This artifact is read-only and does not execute commands.
