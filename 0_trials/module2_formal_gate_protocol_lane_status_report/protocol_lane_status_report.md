# Module2 Formal Gate Protocol Lane Status Report

This file summarizes protocol-lane gates; it is not paper result material.

## Current Status

- next_blocked_lane: `new_or_revised_contract`
- decision_record_status: `protocol_lane_decision_recorded`
- selected_lane_id: `stronger_obstacle_summary_warm_start`
- contract_drafting_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- next_success_attempt_artifact_expected_paths_by_id: `{'new_or_revised_research_contract': '.pipeline/contracts/module2-<selected_protocol_lane>-<version>.md', 'train_final_model_zip': '0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip', 'train_summary_json': '0_trials/module2_gate3_formal/<next_attempt_id>/train/summary.json', 'train_training_manifest_json': '0_trials/module2_gate3_formal/<next_attempt_id>/train/training_manifest.json', 'eval_gate3_eval_episodes_csv': '0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_eval_episodes.csv', 'eval_gate3_summary_json': '0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_summary.json', 'gate3_trial_manifest_json': '0_trials/module2_gate3_formal/<next_attempt_id>/gate3_trial_manifest.json', 'gate3_formal_audit_json': '0_trials/module2_gate3_formal/<next_attempt_id>/gate3_formal_audit.json', 'pulled_back_checkpoint_hash_record': '0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip.sha256 or .sha256.json', 'h02_formal_output_acceptance': '0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json'}`
- next_success_attempt_artifact_proof_requirement_count: `10`
- next_success_attempt_artifact_invalid_substitutes_by_id: `{'new_or_revised_research_contract': ['chat-only approval', 'draft contract', 'editing the failed Gate3 result after seeing failure'], 'train_final_model_zip': ['local PPO training output', 'failed warm-start checkpoint', 'checkpoint without manifest or hash provenance'], 'train_summary_json': ['stdout-only training summary', 'summary from the failed Gate3 attempt', 'summary without protocol label'], 'train_training_manifest_json': ['manifest without source head', 'manifest from a different protocol lane', 'uncommitted chat note'], 'eval_gate3_eval_episodes_csv': ['H02 available-subset smoke CSV', 'no-warm failure rows reused for a warm-start claim', 'aggregate summary without per-episode rows'], 'eval_gate3_summary_json': ['summary from failed run', 'summary without timing fields', 'paper table preview'], 'gate3_trial_manifest_json': ['trial manifest from failed run', 'manifest without contract reference', 'manifest without evaluated checkpoint identity'], 'gate3_formal_audit_json': ['formal_decision=fail reinterpreted as success', 'audit marked smoke, preview, or candidate', 'audit from a different protocol lane'], 'pulled_back_checkpoint_hash_record': ['checkpoint without hash record', 'hash for a different checkpoint', 'remote stdout without local pullback'], 'h02_formal_output_acceptance': ['blocked H02 acceptance', 'formal-looking smoke table', 'PPO rows without checkpoint hash']}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`

## Post-Decision Contract Plan

- status: `post_decision_contract_plan_ready_blocked_pending_lane_decision`
- audit_issue_count: `0`
- required_contract_section_count: `8`
- shared_next_success_attempt_artifact_count: `10`
- shared_next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`
- lane_count: `4`
- selected_lane_id: `None`
- writes_contract: `False`
- approves_contract: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- paper_result_material_allowed: `False`

## Missing Next-Attempt Artifacts

- index_status: `blocked_until_protocol_lane_decision_and_contract`
- contract: `new_or_revised_research_contract`
- training: `train_final_model_zip`, `train_summary_json`, `train_training_manifest_json`
- evaluation: `eval_gate3_eval_episodes_csv`, `eval_gate3_summary_json`
- acceptance: `gate3_trial_manifest_json`, `gate3_formal_audit_json`, `pulled_back_checkpoint_hash_record`
- formal_acceptance: `h02_formal_output_acceptance`

## Safety Flags

- local_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`
- new_success_training_allowed_now: `False`
- contract_approval_allowed_now: `False`
- draft_contract_allows_training: `False`

## Allowed Next Actions
- `record_protocol_lane_decision`

## Blocked Actions
- `local_training`
- `remote_success_training`
- `remote_preflight_for_new_success_attempt`
- `formal_claim`
- `paper_result_material`

## Claim Boundaries
- This report summarizes protocol-lane gates; it does not record a lane decision.
- The old remote execution packet may remain ready, but it is not authorization for a new success attempt.
- Current allowed actions do not include local training, remote training, formal claims, or paper result material.
- New success training still requires a recorded protocol lane decision and an approved/frozen new or revised contract.

## Audit

- status: `protocol_lane_status_report_audit_failed`
- audit_issue_count: `3`
