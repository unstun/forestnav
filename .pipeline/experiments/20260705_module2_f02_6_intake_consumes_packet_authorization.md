---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 F02.6 Intake Consumes Packet Authorization

## What Changed

`f02_6_decision_intake` now consumes the decision packet's
`current_authorization` summary and checks it against the current gate state.

The intake now fails if the packet:

- does not report `authorization_status=blocked_until_dr_sun_decision`
- allows anything other than `record_f02_6_decision`
- omits any blocked current action among `remote_preflight`,
  `remote_training`, `local_training`, `formal_claim`, and
  `paper_result_material`
- treats post-decision routes as current authorization
- allows remote preflight, remote training, local training, formal claims, or
  paper result material
- disagrees with the formal gate status report on remote preflight or remote
  training permission while F02.6 is pending

## Current Evidence

Refreshed `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
reports:

- `status=f02_6_decision_intake_pending_clean`
- `packet_authorization_status=blocked_until_dr_sun_decision`
- `packet_current_allowed_action_ids=["record_f02_6_decision"]`
- `packet_current_blocked_action_ids=["remote_preflight","remote_training","local_training","formal_claim","paper_result_material"]`
- `packet_post_decision_routes_are_current_authorization=false`
- `packet_remote_preflight_allowed_now=false`
- `packet_remote_training_allowed_now=false`
- `packet_paper_result_material_allowed_now=false`
- `status_report_remote_preflight_allowed_now=false`
- `status_report_remote_training_allowed_now=false`
- `audit_issue_count=0`

The downstream formal gate remains blocked:

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `decision_status=pending_human_decision`
- `remote_packet_status=blocked_until_f02_6_decision`
- `remaining_deliverables_missing_deliverable_count=10`
- `remote_preflight_allowed_now=false`
- `remote_training_allowed_now=false`
- `formal_claim_allowed_now=false`
- `local_training_allowed_now=false`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_f02_6_decision_intake.py \
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

Observed: `150 passed in 6.39s`.

## Boundary

This task did not approve or reject F02.6, did not run local training, did not
run remote preflight, did not run remote PPO training, did not pull back a
checkpoint, did not run H01/H02 formal evaluation, and did not write paper
result material.
