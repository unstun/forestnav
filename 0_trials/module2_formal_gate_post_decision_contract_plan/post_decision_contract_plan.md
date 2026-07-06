# Module2 Post-Decision Contract Plan

This file is a read-only planning index. It is not a contract draft, training run, remote preflight, formal evaluation, or paper result.

## Gate State

- status: `post_decision_contract_plan_ready_for_contract_draft`
- next_blocked_lane: `new_or_revised_contract`
- selected_lane_id: `stronger_obstacle_summary_warm_start`
- decision_owner_required: `Dr Sun`
- allowed_next_action_ids: `['draft_new_or_revised_contract_after_lane_decision']`
- contract_drafting_allowed_now: `True`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Required Contract Sections

- `protocol_lane`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `hypothesis`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `success_signal`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `failure_signal`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `protocol_delta_from_failed_run`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `training_budget_and_seed_policy`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `evaluation_and_acceptance_plan`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`
- `paper_claim_boundary`: status=`awaiting_dr_sun_decision`, must_lock_before_training=`True`

## Lane Contract Plans

### stronger_obstacle_summary_warm_start

- expected_contract_path_template: `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`
- new_success_training_required_if_selected: `True`
- contract_write_allowed_now: `False`
- remote_training_allowed_now: `False`
- next_success_attempt_artifact_ids: `['new_or_revised_research_contract', 'train_final_model_zip', 'train_summary_json', 'train_training_manifest_json', 'eval_gate3_eval_episodes_csv', 'eval_gate3_summary_json', 'gate3_trial_manifest_json', 'gate3_formal_audit_json', 'pulled_back_checkpoint_hash_record', 'h02_formal_output_acceptance']`
- required_contract_deltas:
  - warm-start dataset source and acceptance checks
  - PPO stabilization changes
  - curriculum and reward deltas
  - budget and seed policy
- invalid_substitutes:
  - the failed warm-start checkpoint
  - more prose explaining the failed result
  - local PPO training output
  - H02 smoke rows without formal PPO rows

### full_patch_cnn_policy

- expected_contract_path_template: `.pipeline/contracts/module2-full_patch_cnn_policy-v2.md`
- new_success_training_required_if_selected: `True`
- contract_write_allowed_now: `False`
- remote_training_allowed_now: `False`
- next_success_attempt_artifact_ids: `['new_or_revised_research_contract', 'train_final_model_zip', 'train_summary_json', 'train_training_manifest_json', 'eval_gate3_eval_episodes_csv', 'eval_gate3_summary_json', 'gate3_trial_manifest_json', 'gate3_formal_audit_json', 'pulled_back_checkpoint_hash_record', 'h02_formal_output_acceptance']`
- required_contract_deltas:
  - observation tensor definition
  - CNN architecture and inference budget
  - comparison fairness against RS/analytic baselines
  - new H01/H02 schema fields if telemetry changes
- invalid_substitutes:
  - using compact-policy failure as CNN success evidence
  - architecture change without revised contract
  - timing-unchecked CNN results
  - paper table without method/schema distinction

### hybrid_ppo_analytic_fallback

- expected_contract_path_template: `.pipeline/contracts/module2-hybrid_ppo_analytic_fallback-v2.md`
- new_success_training_required_if_selected: `True`
- contract_write_allowed_now: `False`
- remote_training_allowed_now: `False`
- next_success_attempt_artifact_ids: `['new_or_revised_research_contract', 'train_final_model_zip', 'train_summary_json', 'train_training_manifest_json', 'eval_gate3_eval_episodes_csv', 'eval_gate3_summary_json', 'gate3_trial_manifest_json', 'gate3_formal_audit_json', 'pulled_back_checkpoint_hash_record', 'h02_formal_output_acceptance']`
- required_contract_deltas:
  - hybrid control handoff rule
  - fallback usage metric
  - success signal that separates PPO-only from analytic-assisted success
  - paper claim boundary for hybrid assistance
- invalid_substitutes:
  - calling hybrid success direct PPO replacement
  - hiding RS/analytic fallback calls inside aggregate success
  - using direct-replacement threshold without a hybrid contract
  - paper prose that omits fallback usage

### stop_or_reframe_module2_claim

- expected_contract_path_template: `.pipeline/contracts/module2-stop_or_reframe_module2_claim-v2.md`
- new_success_training_required_if_selected: `False`
- contract_write_allowed_now: `False`
- remote_training_allowed_now: `False`
- next_success_attempt_artifact_ids: `[]`
- required_contract_deltas:
  - stop criterion
  - negative-result scope
  - allowed paper claim after failure
  - archival requirements for failed checkpoint and audit
- invalid_substitutes:
  - quietly dropping failed PPO without recording the stop decision
  - writing a positive replacement claim from failed evidence
  - running new training while pretending the lane was stop/reframe

## Shared Next Success Attempt Artifacts

- shared_next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`
- `new_or_revised_research_contract` (contract): status=`missing_required_before_new_success_training`, blocked_until=`record_protocol_lane_decision`
- `train_final_model_zip` (training): status=`not_created_for_next_success_attempt`, blocked_until=`approved_or_frozen_new_or_revised_contract`
- `train_summary_json` (training): status=`not_created_for_next_success_attempt`, blocked_until=`approved_or_frozen_new_or_revised_contract`
- `train_training_manifest_json` (training): status=`not_created_for_next_success_attempt`, blocked_until=`approved_or_frozen_new_or_revised_contract`
- `eval_gate3_eval_episodes_csv` (evaluation): status=`blocked_until_new_checkpoint`, blocked_until=`new_remote_ppo_checkpoint_bundle`
- `eval_gate3_summary_json` (evaluation): status=`blocked_until_new_checkpoint`, blocked_until=`new_remote_ppo_checkpoint_bundle`
- `gate3_trial_manifest_json` (acceptance): status=`blocked_until_new_eval`, blocked_until=`new_formal_gate3_eval_bundle`
- `gate3_formal_audit_json` (acceptance): status=`blocked_until_new_eval`, blocked_until=`new_formal_gate3_eval_bundle`
- `pulled_back_checkpoint_hash_record` (acceptance): status=`blocked_until_new_eval`, blocked_until=`new_formal_gate3_eval_bundle`
- `h02_formal_output_acceptance` (formal_acceptance): status=`blocked_until_new_gate3_pass`, blocked_until=`new_gate3_audit_and_hash_acceptance`

## Audit

- audit_issue_count: `0`
- no audit issues

## Claim Boundaries
- This artifact is a post-decision contract planning index, not a contract draft.
- It may carry the recorded protocol lane context, but it does not write or approve a contract.
- It does not authorize local training, remote preflight, remote training, formal claims, or paper result material.
- Any success lane still needs a selected lane, an approved/frozen new or revised contract, remote training artifacts, formal Gate3 pass, checkpoint hash, and H02 acceptance.
