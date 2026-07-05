# Module2 Formal Gate Protocol Lane Decision Packet

This file is a formal-gate decision packet, not paper result material.

## Gate Summary

- current_formal_decision: `fail`
- current_failure_mode: `threshold_failure`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- new_success_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- local_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Valid Lane Decisions

| lane | status | training_allowed_now |
|---|---|---:|
| `stronger_obstacle_summary_warm_start` | `awaiting_dr_sun_selection` | `False` |
| `full_patch_cnn_policy` | `awaiting_dr_sun_selection` | `False` |
| `hybrid_ppo_analytic_fallback` | `awaiting_dr_sun_selection` | `False` |
| `stop_or_reframe_module2_claim` | `awaiting_dr_sun_selection` | `False` |

## Decision Record Schema

- required_fields: `decider, decision_timestamp_utc, selected_lane_id, decision_summary, justification_against_failed_gate3, claim_scope_after_decision, contract_action, training_authorization`
- training_authorization_must_be: `not_authorized_by_this_decision_packet`

## Current Blocked Actions
- `local_training`
- `remote_success_training`
- `remote_preflight_for_new_success_attempt`
- `formal_claim`
- `paper_result_material`

## Audit

- status: `formal_gate_protocol_lane_decision_packet_ready_for_dr_sun`
- audit_issue_count: `0`
