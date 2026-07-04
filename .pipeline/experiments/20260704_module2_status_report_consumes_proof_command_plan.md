---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-04
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Status Report Consumes Remaining-Deliverables Proof Command Plan

## What Changed

`formal_gate_status_report` now consumes the remaining-deliverables proof-command plan.

- Status report exposes `remaining_deliverables_proof_command_plan`.
- `current_state` exposes proof-plan presence, matrix row count, and proof command count.
- Remaining-deliverables acceptance rows carry `proof_command_count` and `proof_command_ids`.
- Remaining-deliverables gap summary preserves proof-command IDs for missing artifacts.
- Status report now raises input safety issues when the proof plan is missing, has the wrong boundary, claims to run training/preflight, has row/count drift, or drops proof commands for an acceptance-matrix row.
- Markdown status report includes a `Remaining Deliverables Proof Command Plan` section.

## Current Evidence

- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
  - `status=formal_gate_status_blocked`
  - `input_safety_issue_count=0`
  - `current_state.remaining_deliverables_status=formal_gate_deliverables_blocked`
  - `current_state.remaining_deliverables_proof_plan_present=true`
  - `current_state.remaining_deliverables_proof_plan_matrix_row_count=10`
  - `current_state.remaining_deliverables_proof_plan_command_count=20`
  - `remaining_deliverables_proof_command_plan.plan_id=module2_formal_gate_local_read_only_proof_commands`
  - `remaining_deliverables_proof_command_plan.execution_boundary=local_read_only_after_formal_remote_pullback`
  - `remaining_deliverables_proof_command_plan.total_matrix_rows=10`
  - `remaining_deliverables_proof_command_plan.total_proof_command_count=20`
  - `remaining_deliverables_proof_command_plan.runs_training=false`
  - `remaining_deliverables_proof_command_plan.runs_remote_preflight=false`
- `permissions_now`
  - `local_training_allowed_now=false`
  - `remote_training_allowed_now=false`
  - `formal_claim_allowed_now=false`

## Verification

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py
```

Observed: `24 passed in 1.26s`.

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report
```

Observed:

- `status=formal_gate_status_blocked`
- `input_safety_issue_count=0`
- `proof plan rows=10`
- `proof command count=20`

## Boundary

No local training, remote sync, remote preflight, remote PPO training, remote audit, pullback, H01/H02 formal run, or paper result writing was performed. This record only propagates future local read-only proof-command metadata into the formal gate status report.
