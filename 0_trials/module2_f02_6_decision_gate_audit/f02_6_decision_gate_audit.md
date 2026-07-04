# Module2 F02.6 Decision Gate Audit

This file audits the human decision gate. It does not record a decision, train, preflight, or claim results.

- status: `f02_6_decision_gate_pending_clean`
- audit_issue_count: `0`
- record_status: `pending_human_decision`
- packet_recommendation: `approve_obstacle_summary_warm_start`
- training_allowed_now: `False`
- remote_preflight_allowed_now: `False`

## Audit Issues

- none

## Allowed Human Actions

- `approve_obstacle_summary_warm_start`: Allows source-fresh regeneration and approved remote preflight regeneration; does not allow paper claims.
- `reject_obstacle_summary_warm_start`: Keeps obstacle-summary warm-start formal training blocked and routes to stronger/full patch-CNN protocol.

## Claim Boundaries

- This audit validates the F02.6 decision gate; it does not record Dr Sun's decision.
- A passing pending audit is not approval for warm-start training.
- Approval can only unlock source-fresh regeneration and approved remote preflight, not a paper claim.
- Formal PPO warm-start training remains remote-only on gpu3070ti-relay after all upstream gates pass.
