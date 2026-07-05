# Module2 Formal Gate Protocol Lane Status Report

This file summarizes protocol-lane gates; it is not paper result material.

## Current Status

- next_blocked_lane: `protocol_lane_decision`
- decision_record_status: `pending_protocol_lane_decision`
- selected_lane_id: `None`
- contract_drafting_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

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
