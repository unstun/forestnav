---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 F02.6 Packet Remote Training Veto

## What Changed

The F02.6 warm-start decision packet now exposes a top-level
`remote_training_allowed=false` field.

This closes a safety ambiguity in the packet itself: the packet can still list
the post-approval remote command route, but the same artifact now explicitly
states that remote training is not currently authorized.

The packet Markdown also prints `remote training allowed now: False`, and the
claim boundaries now state that the listed remote command is a post-approval
route, not current authorization to train.

## Current Evidence

Refreshed `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
reports:

- `status=pending_human_decision`
- `not_paper_result_material=true`
- `executes_commands=false`
- `runs_training=false`
- `runs_remote_preflight=false`
- `local_training_allowed=false`
- `remote_training_allowed=false`
- `formal_claim_allowed=false`
- `source_issue_count=0`

The downstream formal gate remains blocked:

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `decision_status=pending_human_decision`
- `remote_packet_status=blocked_until_f02_6_decision`
- `remaining_deliverables_missing_deliverable_count=10`
- `remote_training_allowed_now=false`
- `local_training_allowed_now=false`
- `formal_claim_allowed_now=false`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

Observed: `145 passed in 6.90s`.

## Boundary

This task did not approve or reject F02.6, did not run local training, did not
run remote preflight, did not run remote PPO training, did not pull back a
checkpoint, did not run H01/H02 formal evaluation, and did not write paper
result material.
