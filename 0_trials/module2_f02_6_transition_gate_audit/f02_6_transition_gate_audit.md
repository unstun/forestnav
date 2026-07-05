# Module2 F02.6 Transition Gate Audit

This file audits synthetic pending/approved/rejected F02.6 gate transitions. It does not record a decision, run preflight, train, audit, pull back artifacts, or write paper results.

- status: `f02_6_transition_gate_audit_passed`
- audit_issue_count: `0`
- scenario_count: `3`
- synthetic_inputs_persisted: `False`

## Scenario Summary

### pending

- record_status: `pending_human_decision`
- post_plan_status: `blocked_until_f02_6_decision`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_pending_clean`
- post_plan_audit_status: `post_f02_6_plan_audit_passed`
- remote_packet_safety_status: `remote_packet_safety_audit_passed`
- next_blocked_lane_id: `decision`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `False`
- approved_remote_preflight_allowed: `False`
- gate3_remote_training_allowed: `False`

### approved

- record_status: `approved`
- post_plan_status: `ready_to_execute_post_f02_6_regeneration_plan`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_audit_passed`
- post_plan_audit_status: `post_f02_6_plan_audit_passed`
- remote_packet_safety_status: `remote_packet_safety_audit_passed`
- next_blocked_lane_id: `source_fresh_preflight`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `True`
- approved_remote_preflight_allowed: `False`
- gate3_remote_training_allowed: `False`

### rejected

- record_status: `rejected`
- post_plan_status: `blocked_by_f02_6_rejected`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_audit_passed`
- post_plan_audit_status: `post_f02_6_plan_audit_passed`
- remote_packet_safety_status: `remote_packet_safety_audit_passed`
- next_blocked_lane_id: `source_fresh_preflight`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `False`
- approved_remote_preflight_allowed: `False`
- gate3_remote_training_allowed: `False`

## Audit Issues

- none

## Claim Boundaries

- This audit is a transition-safety check, not Dr Sun's F02.6 decision record.
- A passing approved synthetic scenario is not permission to train; it only proves the post-decision gates do not accidentally open claim or remote training.
- Formal PPO remains gpu3070ti-relay-only after F02.6, source freshness, remote packet readiness, audit, pullback, H01/H02, and claim gates close.
