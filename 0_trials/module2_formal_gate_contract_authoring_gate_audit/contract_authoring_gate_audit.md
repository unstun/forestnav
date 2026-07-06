# Module2 Formal Gate Contract Authoring Gate Audit

This file audits whether contract authoring may proceed; it is not paper result material.

## Contract Gate

- decision_record_status: `protocol_lane_decision_recorded`
- selected_lane_id: `stronger_obstacle_summary_warm_start`
- contract_action: `draft_new_contract`
- contract_drafting_allowed_now: `True`
- contract_approval_allowed_now: `False`
- draft_contract_allows_training: `False`

## Allowed Next Actions

- allowed_next_action_ids:
  - `draft_new_or_revised_contract_after_lane_decision`

## Blocked Actions

- blocked_action_ids:
  - `local_training`
  - `remote_success_training`
  - `remote_preflight_for_new_success_attempt`
  - `formal_claim`
  - `paper_result_material`

## Existing Contract

- status: `approved`
- version: `v1`
- usable_for_new_success_attempt: `False`

## Post-Decision Contract Plan

- status: `post_decision_contract_plan_ready_blocked_pending_lane_decision`
- audit_issue_count: `0`
- required_contract_section_count: `8`
- shared_next_success_attempt_artifact_count: `10`
- shared_next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`
- lane_count: `4`
- gate_selected_lane_id: `None`
- gate_contract_drafting_allowed_now: `False`

## Required Contract Sections
- `protocol_lane`
- `hypothesis`
- `success_signal`
- `failure_signal`
- `protocol_delta_from_failed_run`
- `training_budget_and_seed_policy`
- `evaluation_and_acceptance_plan`
- `paper_claim_boundary`

## Claim Boundaries
- This audit gates contract authoring after the protocol-lane decision; it does not draft or approve a contract.
- The approved v1 contract is historical input only and cannot authorize a new success attempt after the failed warm-start Gate3 run.
- A clean pending audit still blocks contract drafting, remote training, formal claims, and paper result material.
- A recorded lane decision can only open contract drafting, not training; training still requires an approved/frozen new or revised contract plus later gates.

## Audit

- status: `contract_authoring_gate_audit_failed`
- audit_issue_count: `1`
