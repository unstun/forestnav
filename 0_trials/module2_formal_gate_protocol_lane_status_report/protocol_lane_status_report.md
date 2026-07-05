# Module2 Formal Gate Protocol Lane Status Report

This file summarizes protocol-lane gates; it is not paper result material.

## Current Status

- next_blocked_lane: `protocol_lane_decision`
- decision_record_status: `pending_protocol_lane_decision`
- selected_lane_id: `None`
- contract_drafting_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Allowed Next Actions
- `record_protocol_lane_decision`

## Blocked Actions
- `local_training`
- `remote_success_training`
- `remote_preflight_for_new_success_attempt`
- `formal_claim`
- `paper_result_material`

## Audit

- status: `protocol_lane_status_blocked_pending_lane_decision`
- audit_issue_count: `0`
