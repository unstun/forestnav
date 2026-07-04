---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-04
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Remaining-Deliverables Proof Command Plan

## What Changed

This audit strengthens `module2_formal_gate_remaining_deliverables` from a missing-artifact ledger into a local read-only proof-command plan.

- Each of the 10 formal-gate missing deliverables now has `proof_commands`.
- The manifest now exposes top-level `proof_command_plan`.
- The gap summary and human-readable checklist now carry proof-command IDs, so each missing artifact has both an expected path and a concrete future verification command.
- The Markdown output now includes a `Proof Command Plan` section and per-row proof commands.

## Current Evidence

- `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
  - `status=formal_gate_deliverables_blocked`
  - `missing_deliverable_count=10`
  - `open_category_count=4`
  - `proof_command_plan.plan_id=module2_formal_gate_local_read_only_proof_commands`
  - `proof_command_plan.execution_boundary=local_read_only_after_formal_remote_pullback`
  - `proof_command_plan.total_matrix_rows=10`
  - `proof_command_plan.total_proof_command_count=20`
  - `proof_command_plan.runs_training=false`
  - `proof_command_plan.runs_remote_preflight=false`
- Representative proof-command rows:
  - `training:train_final_model_zip`
    - `train_final_model_zip_exists_nonempty`
    - `train_final_model_zip_valid_zip`
  - `evaluation:eval_gate3_eval_episodes_csv`
    - `eval_gate3_eval_episodes_csv_exists_nonempty`
    - `eval_gate3_eval_episodes_csv_schema`
  - `acceptance:gate3_formal_audit_json`
    - `gate3_formal_audit_json_exists_nonempty`
    - `gate3_formal_audit_json_accepts_formal_scope`
  - `formal_acceptance:h02_formal_output_acceptance`
    - `h02_formal_output_acceptance_exists_nonempty`
    - `h02_formal_output_acceptance_status`

## Verification

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/build_module2_formal_gate_remaining_deliverables.py

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py
```

Observed: `4 passed in 0.26s`.

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables
```

Observed:

- `status=formal_gate_deliverables_blocked`
- `total_matrix_rows=10`
- `total_proof_command_count=20`

## Boundary

No local training, remote sync, remote preflight, remote PPO training, remote audit, pullback, H01/H02 formal run, or paper result writing was performed. This record only adds future local read-only proof commands for artifacts that remain missing.
