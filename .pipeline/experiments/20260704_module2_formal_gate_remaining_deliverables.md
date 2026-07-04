---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 formal gate remaining deliverables

## What changed

新增只读 builder:

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_remaining_deliverables.py`

新增产物:

- `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.md`

该 ledger 从现有 formal gate status report、missing-artifacts inventory、closure checklist、remote packet、H01 manifest 和 H02 acceptance 中抽取剩余交付物，只聚焦四类:

1. formal remote PPO training deliverables
2. formal Gate3 evaluation deliverables
3. remote pullback / audit / hash acceptance deliverables
4. H01/H02 formal acceptance deliverables

## Current formal-gate state

当前状态仍为 blocked:

- `formal_gate_remaining_deliverables.status=formal_gate_deliverables_blocked`
- `missing_deliverable_count=10`
- `open_category_count=4`
- `next_blocked_lane=decision`
- `local_training_allowed_now=false`
- `remote_preflight_allowed_now=false`
- `remote_training_allowed_now=false`
- `formal_claim_allowed_now=false`

## Missing deliverables

Training missing 3:

- `train_final_model_zip`
- `train_summary_json`
- `train_training_manifest_json`

Evaluation missing 2:

- `eval_gate3_eval_episodes_csv`
- `eval_gate3_summary_json`

Acceptance missing 3:

- `gate3_trial_manifest_json`
- `gate3_formal_audit_json`
- `pulled_back_checkpoint_hash_record`

Formal H01/H02 acceptance missing 2:

- `h01_ready_for_formal_run`
- `h02_formal_output_acceptance`

## Invalid substitutes preserved

The ledger keeps invalid substitutes from the formal gate requirement matrix, including:

- local training output
- available-subset smoke model
- H02 available-subset smoke CSV
- paper table preview
- no-warm formal failure eval reused as warm-start evidence
- remote command success without local pullback
- checkpoint file without hash record
- audit marked candidate, smoke, preview, or not_formal
- blocked H01 manifest
- blocked H02 acceptance audit
- formal-looking tables generated from smoke or missing PPO rows

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables
PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py
jq '{status, missing_deliverable_count, open_category_count, category_counts, next:.current_gate_summary.next_blocked_lane, permissions:.permissions_now}' 0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json
```

Observed results:

- New targeted tests: 4 passed.
- `py_compile` completed successfully.
- JSON summary confirmed training 3 missing, evaluation 2 missing, acceptance 3 missing, formal acceptance 2 missing.
- Audit issue count is 0.

## Boundary

This task did not:

- approve or reject F02.6,
- run ssh/rsync,
- run remote preflight,
- run local or remote training,
- run remote audit/pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.
