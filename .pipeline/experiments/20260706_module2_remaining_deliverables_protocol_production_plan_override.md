---
date: 2026-07-06
status: checked
origin: ai+local
reviewed: false
topic: module2-remaining-deliverables-protocol-production-plan-override
---

# Module2 Remaining Deliverables Protocol Production Plan Override

## Scope

This record documents a read-only formal-gate correction. It does not run local
training, remote preflight, remote PPO training, remote audit, H01/H02 formal
evaluation, formal claims, or paper-result material.

## Problem

`formal_gate_next_round_requirements` already distinguishes the current failed
run from the next success attempt, but `formal_gate_remaining_deliverables`
still exposed old `post_f02_6_regeneration_plan` stage summaries directly in
its production plan. When the old plan was locally ready, readers could see
`gate3_remote_training.allowed_now=true` inside a reference-only plan even
though the current top-level gate is `protocol_lane_decision`.

That was a gate wording bug, not a training result.

## Change

- `build_module2_formal_gate_remaining_deliverables.py` now passes
  `protocol_lane_status_report` into `deliverable_production_plan`.
- When `protocol_lane_status_blocked_pending_lane_decision` is active, the
  production plan reports effective `post_plan_status` as
  `blocked_until_protocol_lane_decision`.
- Production-stage summaries now set `allowed_now=false`, add
  `protocol_lane_decision_pending` to `blocked_by`, and preserve the raw stage
  values as `original_*_before_protocol_override`.
- The synthetic complete-but-protocol-pending test now proves that even a ready
  old stage cannot open remote training while the protocol lane is pending.

## Current Gate State

- Current failed-run ledger: `training/evaluation/acceptance/formal_acceptance
  = 0/0/0/1` missing.
- Next success attempt still requires 10 fresh artifacts:
  `contract/training/evaluation/acceptance/formal_acceptance = 1/3/2/3/1`.
- Current allowed action remains `record_protocol_lane_decision`.
- Current blocked actions remain `local_training`,
  `remote_success_training`, `remote_preflight_for_new_success_attempt`,
  `formal_claim`, and `paper_result_material`.

## Verification

```text
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py
8 passed

PYTHONPATH=2_experiment python -m \
  forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables
status=formal_gate_deliverables_blocked

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_next_round_requirements.py \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py
67 passed
```

## Boundary

This change only prevents stale reference-plan readiness from being mistaken
for current authorization. The next formal-gate action is still Dr Sun's
`record_protocol_lane_decision`. New success training still requires a selected
protocol lane, an approved or frozen new/revised Research Contract, refreshed
source/remote gates, remote preflight, remote training, pullback, Gate3 audit,
and H01/H02 acceptance.
