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
- remote_preflight_allowed_now: `True`
- remote_training_allowed_now_for_existing_packet: `True`
- formal_h01_evaluation_allowed_now: `True`
- formal_h02_acceptance_allowed_now: `False`
- formal_claim_allowed_now: `False`
- new_success_training_allowed_now: `False`
- new_or_revised_contract_required_before_new_success_training: `True`
- failure_triage_next_gate_status: `requires_protocol_decision_before_new_success_attempt`

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

## Boundaries
- This artifact is a formal-gate planning artifact, not a paper result table or appendix.
- The failed warm-start PPO Gate3 checkpoint is negative formal evidence, not a successful PPO replacement for RS.
- The failed checkpoint, failed audit, and smoke H02 rows are invalid substitutes for the next success-attempt evidence.
- Any new remote training intended to overturn this failure requires a new or revised Research Contract first.
- Local PPO training remains disallowed.

## Audit

- status: `formal_gate_next_round_requirements_ready`
- audit_issue_count: `0`
