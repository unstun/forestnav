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
- post_plan_audit_status: `post_f02_6_plan_audit_failed`
- remote_packet_safety_status: `remote_packet_safety_audit_failed`
- next_blocked_lane_id: `remote_packet_preflight`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `False`
- approved_remote_preflight_allowed: `False`
- gate3_remote_training_allowed: `False`

### approved

- record_status: `approved`
- post_plan_status: `ready_for_remote_training_packet_execution`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_audit_passed`
- post_plan_audit_status: `post_f02_6_plan_audit_failed`
- remote_packet_safety_status: `remote_packet_safety_audit_failed`
- next_blocked_lane_id: `remote_packet_preflight`
- remote_preflight_allowed_now: `True`
- remote_training_allowed_now: `True`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `True`
- approved_remote_preflight_allowed: `True`
- gate3_remote_training_allowed: `True`

### rejected

- record_status: `rejected`
- post_plan_status: `blocked_by_f02_6_rejected`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_audit_passed`
- post_plan_audit_status: `post_f02_6_plan_audit_failed`
- remote_packet_safety_status: `remote_packet_safety_audit_failed`
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
- A passing approved synthetic scenario is not a result claim; it only proves the post-decision gates expose the correct remote-training entry without opening audit, H01/H02, or claim lanes.
- Formal PPO remains gpu3070ti-relay-only; local training, formal claims, and paper-result material stay blocked until remote audit, pullback, H01/H02, and claim gates close.
