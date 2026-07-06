# Module2 Formal Gate Next-Round Requirements

This file is a formal-gate planning artifact, not paper result material.

## Current Failed Run

- formal_decision: `fail`
- failure_mode: `threshold_failure`
- episodes: `64`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- threshold_deficit: `0.26875`

## Current Run Artifact Closure

- training_missing: `0`
- evaluation_missing: `0`
- acceptance_missing: `0`
- formal_acceptance_missing: `1`

## Blocked Formal Acceptance

- h02_status: `blocked_formal_output_acceptance`
- formal_output_accepted: `False`
- paper_result_input_allowed: `False`
- blockers: `h02_verdict_not_formal, gate3_formal_audit_not_passed, h02_scale_below_h01_manifest, missing_ppo_result_rows`

## Permissions Now

- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now_for_existing_packet: `False`
- formal_h01_evaluation_allowed_now: `False`
- formal_h02_acceptance_allowed_now: `False`
- formal_claim_allowed_now: `False`
- new_success_training_allowed_now: `False`
- new_or_revised_contract_required_before_new_success_training: `True`
- failure_triage_next_gate_status: `requires_protocol_decision_before_new_success_attempt`
- execution_veto_reason: `protocol_lane_or_contract_gate_blocks_execution`
- legacy_remote_packet_readiness:
  - remote_preflight_allowed_by_status_report: `False`
  - remote_training_allowed_by_status_report: `False`
  - formal_h01_evaluation_allowed_by_status_report: `False`
  - superseded_by_next_gate: `True`

## Protocol Gate Summary

- protocol_status: `protocol_lane_status_blocked_pending_lane_decision`
- next_blocked_lane: `protocol_lane_decision`
- decision_record_status: `pending_protocol_lane_decision`
- selected_lane_id: `None`
- allowed_next_action_ids: `['record_protocol_lane_decision']`
- blocked_action_ids: `['local_training', 'remote_success_training', 'remote_preflight_for_new_success_attempt', 'formal_claim', 'paper_result_material']`
- new_success_training_allowed_now: `False`
- post_decision_contract_plan_required_section_count: `8`
- post_decision_contract_plan_shared_artifact_count: `10`
- post_decision_contract_plan_lane_count: `4`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- remote_safety_protocol_summary_present: `True`
- remote_safety_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`

## Current Vs Next Attempt Reconciliation

- current_failed_run_missing_counts: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- current_failed_run_training_eval_acceptance_closed: `True`
- current_failed_run_formal_acceptance_open: `True`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- protocol_lane_artifact_counts_match_index: `True`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`
- explanation: The current failed-run ledger may show training/evaluation/acceptance present, but a new success attempt still requires a new/revised contract plus fresh training, evaluation, acceptance, and H02 formal acceptance artifacts under the selected protocol lane.

## Missing Current Formal Acceptance Artifacts

- `formal_acceptance:h02_formal_output_acceptance`: artifact_id=`h02_formal_output_acceptance`, expected_path=`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`, missing_reason=`h02_verdict_not_formal, gate3_formal_audit_not_passed, h02_scale_below_h01_manifest, missing_ppo_result_rows`

## Next-Round Requirements

| category | requirement | status | required_before |
|---|---|---|---|
| `contract` | `new_or_revised_research_contract` | `missing_required_before_new_training` | `new_success_training` |
| `training` | `new_remote_ppo_checkpoint_bundle` | `blocked_until_contract` | `new_gate3_formal_audit` |
| `evaluation` | `new_formal_gate3_eval_bundle` | `blocked_until_new_checkpoint` | `new_gate3_formal_audit` |
| `acceptance` | `new_gate3_audit_and_hash_acceptance` | `blocked_until_new_eval` | `h02_formal_output_acceptance` |
| `formal_acceptance` | `h02_formal_output_acceptance` | `blocked_until_new_gate3_pass` | `paper_result_material` |

## Missing Next-Round Deliverables

### `contract:new_or_revised_research_contract`

- status: `missing_required_before_new_training`
- required_before: `new_success_training`
- acceptable_evidence:
  - a new or revised .pipeline/contracts/module2-* contract
  - status is approved or frozen before the new success attempt starts
  - hypothesis, success signal, failure signal, training budget, and protocol deltas are locked before training
- invalid_substitutes:
  - editing the previous formal result after seeing failure
  - changing threshold, reward, curriculum, architecture, or observation without a new contract
  - chat-only approval without a committed contract artifact

### `training:new_remote_ppo_checkpoint_bundle`

- status: `blocked_until_contract`
- required_before: `new_gate3_formal_audit`
- acceptable_evidence:
  - remote-produced train/final_model.zip under a new attempt directory
  - train/summary.json records protocol label, training budget, seed, and terminal-RS training signals
  - train/training_manifest.json records source head, host, command provenance, and warm-start decision
- invalid_substitutes:
  - local PPO training output
  - the failed warm-start Gate3 checkpoint
  - checkpoint file without summary, manifest, or hash provenance

### `evaluation:new_formal_gate3_eval_bundle`

- status: `blocked_until_new_checkpoint`
- required_before: `new_gate3_formal_audit`
- acceptable_evidence:
  - eval/gate3_eval_episodes.csv from the new approved formal run
  - eval/gate3_summary.json with at least 64 formal episodes
  - terminal-RS success rate, collision rate, truncation rate, timing, and seed/protocol provenance are present
- invalid_substitutes:
  - H02 available-subset smoke CSV
  - no-warm failure rows for a warm-start claim
  - summary without per-episode CSV

### `acceptance:new_gate3_audit_and_hash_acceptance`

- status: `blocked_until_new_eval`
- required_before: `h02_formal_output_acceptance`
- acceptable_evidence:
  - gate3_formal_audit.json for the new attempt records formal_decision=pass
  - gate3_trial_manifest.json ties train/eval/audit to the approved contract
  - train/final_model.zip.sha256 or equivalent hash manifest matches the pulled-back checkpoint
- invalid_substitutes:
  - formal_decision=fail reinterpreted as success
  - remote stdout without local pullback
  - checkpoint hash not tied to the evaluated checkpoint

### `formal_acceptance:h02_formal_output_acceptance`

- status: `blocked_until_new_gate3_pass`
- required_before: `paper_result_material`
- acceptable_evidence:
  - h02_formal_acceptance.json records formal_output_accepted=true
  - paper_result_input_allowed=true
  - formal PPO rows are present and include the accepted checkpoint hash
  - H02 scale satisfies the frozen H01 manifest
- invalid_substitutes:
  - blocked H02 acceptance
  - formal-looking tables generated from smoke scale
  - PPO rows without checkpoint hash

## Next Success Attempt Artifact Index

- status: `blocked_until_protocol_lane_decision_and_contract`
- artifact_count: `10`

| category | artifact_id | status | expected_path | blocked_until |
|---|---|---|---|---|
| `contract` | `new_or_revised_research_contract` | `missing_required_before_new_success_training` | `.pipeline/contracts/module2-<selected_protocol_lane>-<version>.md` | `record_protocol_lane_decision` |
| `training` | `train_final_model_zip` | `not_created_for_next_success_attempt` | `0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip` | `approved_or_frozen_new_or_revised_contract` |
| `training` | `train_summary_json` | `not_created_for_next_success_attempt` | `0_trials/module2_gate3_formal/<next_attempt_id>/train/summary.json` | `approved_or_frozen_new_or_revised_contract` |
| `training` | `train_training_manifest_json` | `not_created_for_next_success_attempt` | `0_trials/module2_gate3_formal/<next_attempt_id>/train/training_manifest.json` | `approved_or_frozen_new_or_revised_contract` |
| `evaluation` | `eval_gate3_eval_episodes_csv` | `blocked_until_new_checkpoint` | `0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_eval_episodes.csv` | `new_remote_ppo_checkpoint_bundle` |
| `evaluation` | `eval_gate3_summary_json` | `blocked_until_new_checkpoint` | `0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_summary.json` | `new_remote_ppo_checkpoint_bundle` |
| `acceptance` | `gate3_trial_manifest_json` | `blocked_until_new_eval` | `0_trials/module2_gate3_formal/<next_attempt_id>/gate3_trial_manifest.json` | `new_formal_gate3_eval_bundle` |
| `acceptance` | `gate3_formal_audit_json` | `blocked_until_new_eval` | `0_trials/module2_gate3_formal/<next_attempt_id>/gate3_formal_audit.json` | `new_formal_gate3_eval_bundle` |
| `acceptance` | `pulled_back_checkpoint_hash_record` | `blocked_until_new_eval` | `0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip.sha256 or .sha256.json` | `new_formal_gate3_eval_bundle` |
| `formal_acceptance` | `h02_formal_output_acceptance` | `blocked_until_new_gate3_pass` | `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` | `new_gate3_audit_and_hash_acceptance` |

### Artifact Proof Requirements

#### `contract:new_or_revised_research_contract`
- required_before: `new_success_training`
- proof_requirement: contract status is approved or frozen and locks hypothesis, success signal, failure signal, budget, and protocol deltas
- invalid_substitutes:
  - chat-only approval
  - draft contract
  - editing the failed Gate3 result after seeing failure

#### `training:train_final_model_zip`
- required_before: `new_gate3_formal_audit`
- proof_requirement: remote-produced PPO checkpoint pulled back from gpu3070ti-relay
- invalid_substitutes:
  - local PPO training output
  - failed warm-start checkpoint
  - checkpoint without manifest or hash provenance

#### `training:train_summary_json`
- required_before: `new_gate3_formal_audit`
- proof_requirement: summary records protocol label, training budget, seed, and terminal-RS training signals
- invalid_substitutes:
  - stdout-only training summary
  - summary from the failed Gate3 attempt
  - summary without protocol label

#### `training:train_training_manifest_json`
- required_before: `new_gate3_formal_audit`
- proof_requirement: manifest records source head, host, command provenance, seed, and selected protocol lane
- invalid_substitutes:
  - manifest without source head
  - manifest from a different protocol lane
  - uncommitted chat note

#### `evaluation:eval_gate3_eval_episodes_csv`
- required_before: `new_gate3_formal_audit`
- proof_requirement: per-episode formal Gate3 CSV with at least 64 episodes and protocol provenance
- invalid_substitutes:
  - H02 available-subset smoke CSV
  - no-warm failure rows reused for a warm-start claim
  - aggregate summary without per-episode rows

#### `evaluation:eval_gate3_summary_json`
- required_before: `new_gate3_formal_audit`
- proof_requirement: summary records terminal-RS success, collision, truncation, timing, seed, and protocol label
- invalid_substitutes:
  - summary from failed run
  - summary without timing fields
  - paper table preview

#### `acceptance:gate3_trial_manifest_json`
- required_before: `h02_formal_output_acceptance`
- proof_requirement: trial manifest ties contract, train, eval, audit, source head, and selected protocol lane
- invalid_substitutes:
  - trial manifest from failed run
  - manifest without contract reference
  - manifest without evaluated checkpoint identity

#### `acceptance:gate3_formal_audit_json`
- required_before: `h02_formal_output_acceptance`
- proof_requirement: audit records formal_decision=pass for the new approved protocol attempt
- invalid_substitutes:
  - formal_decision=fail reinterpreted as success
  - audit marked smoke, preview, or candidate
  - audit from a different protocol lane

#### `acceptance:pulled_back_checkpoint_hash_record`
- required_before: `h02_formal_output_acceptance`
- proof_requirement: hash record matches the pulled-back final_model.zip evaluated by Gate3
- invalid_substitutes:
  - checkpoint without hash record
  - hash for a different checkpoint
  - remote stdout without local pullback

#### `formal_acceptance:h02_formal_output_acceptance`
- required_before: `paper_result_material`
- proof_requirement: H02 records formal_output_accepted=true, paper_result_input_allowed=true, PPO rows, and accepted checkpoint hash
- invalid_substitutes:
  - blocked H02 acceptance
  - formal-looking smoke table
  - PPO rows without checkpoint hash

## Boundaries
- This artifact is a formal-gate planning artifact, not a paper result table or appendix.
- The failed warm-start PPO Gate3 checkpoint is negative formal evidence, not a successful PPO replacement for RS.
- The failed checkpoint, failed audit, and smoke H02 rows are invalid substitutes for the next success-attempt evidence.
- Any new remote training intended to overturn this failure requires a new or revised Research Contract first.
- Local PPO training remains disallowed.

## Audit

- status: `formal_gate_next_round_requirements_ready`
- audit_issue_count: `0`
