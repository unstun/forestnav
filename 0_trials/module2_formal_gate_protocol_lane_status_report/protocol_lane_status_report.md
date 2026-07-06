# Module2 Formal Gate Protocol Lane Status Report

This file summarizes protocol-lane gates; it is not paper result material.

## Current Status

- next_blocked_lane: `protocol_lane_decision`
- decision_record_status: `pending_protocol_lane_decision`
- selected_lane_id: `None`
- contract_drafting_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`

## Post-Decision Contract Plan

- status: `post_decision_contract_plan_ready_blocked_pending_lane_decision`
- audit_issue_count: `0`
- required_contract_section_count: `8`
- shared_next_success_attempt_artifact_count: `10`
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

- status: `protocol_lane_status_blocked_pending_lane_decision`
- audit_issue_count: `0`
