---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 formal gate gap summary

## What changed

`formal_gate_remaining_deliverables` now emits a direct `deliverable_gap_summary` alongside the detailed acceptance matrix.

The summary is intentionally redundant with the matrix. Its purpose is to make the current PPO-vs-RS formal gate gaps easy to inspect without reconstructing them from long rows:

- total missing deliverables,
- open category count,
- category order,
- per-category responsible stage,
- per-category `allowed_now`,
- per-category blockers,
- exact missing artifact paths.

## Current formal gate state

Current generated state remains blocked:

- `formal_gate_remaining_deliverables.status=formal_gate_deliverables_blocked`
- `deliverable_gap_summary.total_missing_deliverables=10`
- `deliverable_gap_summary.open_category_count=4`
- `permissions_now.local_training_allowed_now=false`
- `permissions_now.remote_preflight_allowed_now=false`
- `permissions_now.remote_training_allowed_now=false`
- `permissions_now.formal_claim_allowed_now=false`

## Missing deliverables now exposed by summary

Training missing 3:

- `training:train_final_model_zip`
- `training:train_summary_json`
- `training:train_training_manifest_json`

Evaluation missing 2:

- `evaluation:eval_gate3_eval_episodes_csv`
- `evaluation:eval_gate3_summary_json`

Acceptance missing 3:

- `acceptance:gate3_trial_manifest_json`
- `acceptance:gate3_formal_audit_json`
- `acceptance:pulled_back_checkpoint_hash_record`

Formal H01/H02 acceptance missing 2:

- `formal_acceptance:h01_ready_for_formal_run`
- `formal_acceptance:h02_formal_output_acceptance`

## Boundary

This change is a formal-gate readability and auditability change only. It did not:

- approve or reject F02.6,
- run local training,
- run remote sync, preflight, training, audit, or pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_remaining_deliverables.py
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables
jq '.deliverable_gap_summary | {summary_id,total_missing_deliverables,open_category_count,category_order,categories: [.categories[] | {category,missing_count,responsible_stage_id,responsible_stage_allowed_now}]}' 0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json
```

Observed results:

- Targeted tests: 4 passed.
- Builder refreshed `formal_gate_remaining_deliverables.json` and `.md`.
- Summary confirms 10 missing deliverables across 4 blocked categories.
