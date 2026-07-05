# Module2 F02.6 Transition Gate Audit

This file audits synthetic pending/approved/rejected F02.6 gate transitions. It does not record a decision, run preflight, train, audit, pull back artifacts, or write paper results.

- status: `f02_6_transition_gate_audit_failed`
- audit_issue_count: `21`
- scenario_count: `3`
- synthetic_inputs_persisted: `False`

## Scenario Summary

### pending

- record_status: `pending_human_decision`
- post_plan_status: `blocked_until_f02_6_decision`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_audit_failed`
- post_plan_audit_status: `post_f02_6_plan_audit_failed`
- remote_packet_safety_status: `remote_packet_safety_audit_failed`
- next_blocked_lane_id: `decision`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `False`
- approved_remote_preflight_allowed: `False`
- gate3_remote_training_allowed: `True`

### approved

- record_status: `approved`
- post_plan_status: `ready_for_remote_training_packet_execution`
- status_report_status: `formal_gate_status_blocked`
- decision_gate_status: `f02_6_decision_gate_audit_passed`
- post_plan_audit_status: `post_f02_6_plan_audit_failed`
- remote_packet_safety_status: `remote_packet_safety_audit_failed`
- next_blocked_lane_id: `source_fresh_preflight`
- remote_preflight_allowed_now: `True`
- remote_training_allowed_now: `True`
- formal_claim_allowed_now: `False`
- regenerate_preflight_gate_artifacts_allowed: `True`
- approved_remote_preflight_allowed: `False`
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
- gate3_remote_training_allowed: `True`

## Audit Issues

- `pending.decision_gate_audit_issue_count`: decision_gate_audit_issue_count must be zero.
- `pending.post_plan_audit_issue_count`: post_plan_audit_issue_count must be zero.
- `pending.remote_packet_safety_issue_count`: remote_packet_safety_issue_count must be zero.
- `pending.unexpected_decision_gate_status`: Decision gate status drifted.
- `pending.post_plan_audit_not_passed`: Post-plan audit must remain internally safe.
- `pending.remote_packet_safety_not_passed`: Remote packet safety must remain internally safe.
- `pending.pending_plan_allows_training`: Pending post-plan must not allow training.
- `pending.pending_ready_stages_drift`: Only the human decision stage should be ready while pending.
- `approved.status_report_allows_remote_training`: Synthetic transition must not directly allow formal PPO training.
- `approved.post_plan_audit_issue_count`: post_plan_audit_issue_count must be zero.
- `approved.remote_packet_safety_issue_count`: remote_packet_safety_issue_count must be zero.
- `approved.post_plan_audit_not_passed`: Post-plan audit must remain internally safe.
- `approved.remote_packet_safety_not_passed`: Remote packet safety must remain internally safe.
- `approved.approved_post_plan_wrong_status`: Approved scenario should advance only to local gate regeneration or remain blocked by formal gate preconditions.
- `approved.approved_status_report_allows_remote_preflight_too_early`: Approved decision alone must not bypass remote packet/source freshness.
- `approved.approved_training_ready_too_early`: Approved scenario must still block formal PPO training.
- `rejected.post_plan_audit_issue_count`: post_plan_audit_issue_count must be zero.
- `rejected.remote_packet_safety_issue_count`: remote_packet_safety_issue_count must be zero.
- `rejected.post_plan_audit_not_passed`: Post-plan audit must remain internally safe.
- `rejected.remote_packet_safety_not_passed`: Remote packet safety must remain internally safe.
- `rejected.rejected_training_ready`: Rejected scenario must not allow warm-start formal PPO training.

## Claim Boundaries

- This audit is a transition-safety check, not Dr Sun's F02.6 decision record.
- A passing approved synthetic scenario is not permission to train; it only proves the post-decision gates do not accidentally open claim or remote training.
- Formal PPO remains gpu3070ti-relay-only after F02.6, source freshness, remote packet readiness, audit, pullback, H01/H02, and claim gates close.
