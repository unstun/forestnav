---
origin: ai+local
reviewed: false
created_at: 2026-07-05
topic: module2_mainline_consumes_protocol_status_post_plan
trust_level: audit_record
parent: .pipeline/mainline_module2_rl_rs_replacement.md
---

# Module2 Mainline Consumes Protocol Status Post-Plan

## Scope

This record covers a read-only formal-gate audit update. It makes `mainline_formal_gate_state_audit` consume the post-decision contract plan summary that is now exposed by `protocol_lane_status_report`.

It does not select a protocol lane, write or approve a contract, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, or write paper-result material.

## Change

- `build_module2_mainline_formal_gate_state_audit.py` now normalizes these fields from `protocol_lane_status_report.current_status`:
  - `post_decision_contract_plan_status`
  - `post_decision_contract_plan_required_section_count`
  - `post_decision_contract_plan_shared_artifact_count`
  - `post_decision_contract_plan_lane_count`
  - `next_success_attempt_artifact_count`
  - `next_success_attempt_artifact_category_counts`
  - `next_success_attempt_artifact_ids_by_category`
- The audit now fails if protocol status no longer exposes the inherited post-plan summary, if the 8/10/4 counts drift, if post-plan authorization leaks into the protocol status, or if the 10 next-attempt artifact IDs/categories drift.
- The audit now requires the current mainline section to explicitly mention that `protocol_lane_status_report` inherits the post-decision contract plan summary and the artifact category distribution `contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1`.

## Current State

- `mainline_formal_gate_state_audit.status`: `mainline_formal_gate_state_consistent_blocked`
- `mainline_formal_gate_state_audit.audit_issue_count`: `0`
- `protocol_lane_status_report.status`: `protocol_lane_status_blocked_pending_lane_decision`
- `selected_lane_id`: `None`
- `allowed_next_action_ids`: `record_protocol_lane_decision`
- missing next-attempt artifact category counts: `contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1`

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py` -> `17 passed`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit` -> `mainline_formal_gate_state_consistent_blocked`

## Boundary

This update only tightens downstream audit propagation. The only current formal-gate action remains `record_protocol_lane_decision`, owned by Dr Sun. That action can open contract drafting only after a lane is recorded; it does not approve a contract, train, launch remote preflight, unlock formal claims, or unlock paper-result material.
