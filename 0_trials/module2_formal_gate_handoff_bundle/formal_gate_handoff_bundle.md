# Module2 Formal Gate Handoff Bundle

- status: `blocked_formal_gate_handoff`
- executes commands: `False`
- runs training: `False`
- local training allowed: `False`
- next action: `draft_new_or_revised_contract_after_lane_decision`

## Single Next Action Index

- index_id: `module2_formal_gate_single_next_action_index`
- status: `awaiting_selected_lane_contract_draft`
- single_current_human_entry: `False`
- next_action_id: `draft_new_or_revised_contract_after_lane_decision`
- decision_owner_required: `Dr Sun`
- valid_decisions: `stronger_obstacle_summary_warm_start`
- required_record_fields: `protocol_lane, hypothesis, success_signal, failure_signal, protocol_delta_from_failed_run, training_budget_and_seed_policy, evaluation_and_acceptance_plan, paper_claim_boundary`
- current_allowed_action_ids: `draft_new_or_revised_contract_after_lane_decision`
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
- after_approval_still_requires: `approved_or_frozen_new_or_revised_contract, source_freshness_audit_after_contract, remote_execution_packet_for_selected_lane, approved_remote_preflight_for_selected_lane`

## Remote Steps

- `sync_to_remote`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending, approved_or_frozen_contract_missing`
- `run_remote_preflight`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending, approved_or_frozen_contract_missing`
- `run_remote_training`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending, remote_formal_preflight_not_ready, warm_start_decision_pending, remote_packet_not_ready, approved_or_frozen_contract_missing`
- `run_remote_audit`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending, remote_formal_preflight_not_ready, warm_start_decision_pending, remote_packet_not_ready, approved_or_frozen_contract_missing`

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

- status: `protocol_lane_status_ready_for_contract_draft`
- next_blocked_lane: `new_or_revised_contract`
- decision_record_status: `protocol_lane_decision_recorded`
- selected_lane_id: `stronger_obstacle_summary_warm_start`
- allowed_next_action_ids: `draft_new_or_revised_contract_after_lane_decision`
- blocked_action_ids: `local_training, remote_success_training, remote_preflight_for_new_success_attempt, formal_claim, paper_result_material`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- next_success_attempt_artifact_ids_by_category: `{'contract': ['new_or_revised_research_contract'], 'training': ['train_final_model_zip', 'train_summary_json', 'train_training_manifest_json'], 'evaluation': ['eval_gate3_eval_episodes_csv', 'eval_gate3_summary_json'], 'acceptance': ['gate3_trial_manifest_json', 'gate3_formal_audit_json', 'pulled_back_checkpoint_hash_record'], 'formal_acceptance': ['h02_formal_output_acceptance']}`
- next_success_attempt_artifact_expected_paths_by_id: `{'new_or_revised_research_contract': '.pipeline/contracts/module2-<selected_protocol_lane>-<version>.md', 'train_final_model_zip': '0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip', 'train_summary_json': '0_trials/module2_gate3_formal/<next_attempt_id>/train/summary.json', 'train_training_manifest_json': '0_trials/module2_gate3_formal/<next_attempt_id>/train/training_manifest.json', 'eval_gate3_eval_episodes_csv': '0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_eval_episodes.csv', 'eval_gate3_summary_json': '0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_summary.json', 'gate3_trial_manifest_json': '0_trials/module2_gate3_formal/<next_attempt_id>/gate3_trial_manifest.json', 'gate3_formal_audit_json': '0_trials/module2_gate3_formal/<next_attempt_id>/gate3_formal_audit.json', 'pulled_back_checkpoint_hash_record': '0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip.sha256 or .sha256.json', 'h02_formal_output_acceptance': '0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json'}`
- next_success_attempt_artifact_proof_requirement_count: `10`
- next_success_attempt_artifact_invalid_substitutes_by_id: `{'new_or_revised_research_contract': ['chat-only approval', 'draft contract', 'editing the failed Gate3 result after seeing failure'], 'train_final_model_zip': ['local PPO training output', 'failed warm-start checkpoint', 'checkpoint without manifest or hash provenance'], 'train_summary_json': ['stdout-only training summary', 'summary from the failed Gate3 attempt', 'summary without protocol label'], 'train_training_manifest_json': ['manifest without source head', 'manifest from a different protocol lane', 'uncommitted chat note'], 'eval_gate3_eval_episodes_csv': ['H02 available-subset smoke CSV', 'no-warm failure rows reused for a warm-start claim', 'aggregate summary without per-episode rows'], 'eval_gate3_summary_json': ['summary from failed run', 'summary without timing fields', 'paper table preview'], 'gate3_trial_manifest_json': ['trial manifest from failed run', 'manifest without contract reference', 'manifest without evaluated checkpoint identity'], 'gate3_formal_audit_json': ['formal_decision=fail reinterpreted as success', 'audit marked smoke, preview, or candidate', 'audit from a different protocol lane'], 'pulled_back_checkpoint_hash_record': ['checkpoint without hash record', 'hash for a different checkpoint', 'remote stdout without local pullback'], 'h02_formal_output_acceptance': ['blocked H02 acceptance', 'formal-looking smoke table', 'PPO rows without checkpoint hash']}`
- post_decision_contract_plan_shared_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`
- post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt: `True`

## Handoff Stages

- 1. `f02_6_decision_record`: allowed_now=`False`, blocked_by=`current_decision_status_approved`
- 2. `regenerate_preflight_gate_artifacts`: allowed_now=`True`, blocked_by=`none`
- 3. `approved_remote_preflight`: allowed_now=`False`, blocked_by=`source_fresh_preflight_targets_open, approved_or_frozen_contract_missing`
- 4. `regenerate_remote_execution_packet`: allowed_now=`False`, blocked_by=`source_fresh_preflight_targets_open, approved_or_frozen_contract_missing`
- 5. `gate3_remote_training`: allowed_now=`False`, blocked_by=`source_fresh_preflight_targets_open, remote_packet_not_ready, approved_or_frozen_contract_missing`
- 6. `gate3_remote_audit_pullback`: allowed_now=`False`, blocked_by=`protocol_lane_decision_pending, remote_formal_preflight_not_ready, warm_start_decision_pending, remote_packet_not_ready, approved_or_frozen_contract_missing`
- 7. `regenerate_h01_h02_formal_artifacts`: allowed_now=`False`, blocked_by=`missing_remote_audit_pullback, source_fresh_h01_h02_targets_open, approved_or_frozen_contract_missing`
- 8. `regenerate_claim_gate_artifacts`: allowed_now=`False`, blocked_by=`h02_formal_acceptance_not_ready, source_fresh_claim_targets_open, approved_or_frozen_contract_missing`

## Requirement Summary

- remaining deliverables gap: total_missing=`1`, open_categories=`1`
  - `training`: missing=`0`, responsible_stage=`gate3_remote_training`
  - `evaluation`: missing=`0`, responsible_stage=`gate3_remote_audit_pullback`
  - `acceptance`: missing=`0`, responsible_stage=`gate3_remote_audit_pullback`
  - `formal_acceptance`: missing=`1`, responsible_stage=`regenerate_h01_h02_formal_artifacts`

## Status Report Proof-Audit Deliverables Summary

- present: `True`
- missing_counts_by_formal_category: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- next_blocked_lane: `protocol_lane_decision`
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
