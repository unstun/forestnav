---
date: 2026-07-06
status: checked
origin: ai+local
reviewed: false
topic: module2-protocol-decision-record-next-success-requirements-gate
---

# Module2 Protocol Decision Record Next-Success Requirements Gate

## Scope

This record documents a read-only formal-gate strengthening. It does not record
a protocol lane, run local training, run remote preflight, run remote PPO
training, run remote audit, run H01/H02 formal evaluation, allow formal claims,
or create paper-result material.

## Problem

`protocol_lane_decision_record` already required a decision note to mention the
selected lane, failed Gate3 basis, rejected lanes, evidence artifacts, and
contract action. That was useful but too text-dependent: the record itself did
not structurally carry the next-success-attempt artifact contract.

That made a future recorded lane easier to misread as "the old failed-run
training/evaluation/acceptance artifacts are enough for the next success
attempt."

## Change

- `build_module2_formal_gate_protocol_lane_decision_record.py` now consumes
  `formal_gate_next_round_requirements`.
- The decision record now exposes `next_success_attempt_requirements` with:
  - source status `formal_gate_next_round_requirements_ready`;
  - `next_success_attempt_status=blocked_until_protocol_lane_decision_and_contract`;
  - artifact count `10`;
  - category counts
    `contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1`;
  - artifact ids by category;
  - current failed-run missing counts;
  - `old_failed_run_artifacts_invalid_for_next_success_attempt=true`.
- `post_decision_requirements` now mirrors the 10-artifact summary so that a
  recorded lane only opens contract drafting, not training or claim gates.
- `protocol_lane_decision_gate_audit` now fails if the decision record omits or
  drifts from this next-success-attempt summary.

## Current Gate State

- `protocol_lane_decision_record.status`: `pending_protocol_lane_decision`
- `protocol_lane_decision_gate_audit.status`:
  `protocol_lane_decision_gate_pending_clean`
- `selected_lane_id`: `null`
- Current allowed action: `record_protocol_lane_decision`
- Current blocked actions: `local_training`, `remote_success_training`,
  `remote_preflight_for_new_success_attempt`, `formal_claim`,
  `paper_result_material`
- Current failed-run ledger:
  `training/evaluation/acceptance/formal_acceptance = 0/0/0/1`
- Next success attempt:
  `contract/training/evaluation/acceptance/formal_acceptance = 1/3/2/3/1`

## Verification

```text
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_decision_record.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_decision_gate_audit.py
12 passed

PYTHONPATH=2_experiment python -m \
  forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record
status=pending_protocol_lane_decision

PYTHONPATH=2_experiment python -m \
  forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_gate_audit
status=protocol_lane_decision_gate_pending_clean

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_decision_record.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_decision_gate_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_next_round_requirements.py \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py
71 passed

git diff --check
clean
```

## Boundary

The next formal-gate action is still Dr Sun's `record_protocol_lane_decision`.
Recording a lane only opens new/revised Research Contract drafting. New success
training remains blocked until the selected lane has an approved or frozen
contract, refreshed source/remote gates, approved remote preflight, remote
training, pullback, Gate3 audit, and H01/H02 acceptance.
