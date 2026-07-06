---
date: 2026-07-06
status: checked
origin: ai+local
reviewed: false
topic: module2-contract-plan-authoring-next-success-summary-gate
---

# Module2 Contract Plan Authoring Next-Success Summary Gate

## Scope

This record documents a read-only formal-gate strengthening. It does not select
a protocol lane, write a Research Contract, approve a contract, run local
training, run remote preflight, run remote PPO training, run remote audit, allow
formal claims, or create paper-result material.

## Problem

After `protocol_lane_decision_record` began carrying the structured
next-success requirements, the downstream contract planning layer still mostly
checked only a total count of 10 artifacts. That was not enough: a broken
contract plan could keep the total count at 10 while losing the category split
or the rule that old failed-run artifacts are invalid substitutes.

## Change

- `post_decision_contract_plan` now exposes
  `shared_next_success_attempt_artifact_category_counts`.
- `post_decision_contract_plan` now exposes
  `old_failed_run_artifacts_invalid_for_next_success_attempt`.
- Its audit fails if the category split drifts away from
  `contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1` or if
  old failed-run artifacts are not marked invalid for the next success attempt.
- `contract_authoring_gate_audit` now consumes and checks the same two fields
  from `post_decision_contract_plan`.

## Current Gate State

- `post_decision_contract_plan.status`:
  `post_decision_contract_plan_ready_blocked_pending_lane_decision`
- `contract_authoring_gate_audit.status`:
  `contract_authoring_gate_blocked_pending_lane_decision`
- Shared next-success artifact count: `10`
- Category counts:
  `contract/training/evaluation/acceptance/formal_acceptance = 1/3/2/3/1`
- `old_failed_run_artifacts_invalid_for_next_success_attempt`: `true`
- Current allowed action: `record_protocol_lane_decision`
- Current blocked actions: `local_training`, `remote_success_training`,
  `remote_preflight_for_new_success_attempt`, `formal_claim`,
  `paper_result_material`

## Verification

```text
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_post_decision_contract_plan.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_contract_authoring_gate_audit.py
14 passed

PYTHONPATH=2_experiment python -m \
  forest_n3p.scripts.build_module2_formal_gate_post_decision_contract_plan
status=post_decision_contract_plan_ready_blocked_pending_lane_decision

PYTHONPATH=2_experiment python -m \
  forest_n3p.scripts.build_module2_formal_gate_contract_authoring_gate_audit
status=contract_authoring_gate_blocked_pending_lane_decision

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_post_decision_contract_plan.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_contract_authoring_gate_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_next_round_requirements.py \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py
73 passed

git diff --check
clean
```

## Boundary

The next formal-gate action is still Dr Sun's `record_protocol_lane_decision`.
Even after a lane is recorded, contract drafting is not training authorization.
New success training still requires an approved or frozen new/revised Research
Contract, refreshed source/remote gates, approved remote preflight, remote
training, pullback, Gate3 audit, and H01/H02 acceptance.
