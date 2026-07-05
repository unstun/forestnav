---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Remaining Deliverables Top-Level Summary

## What Changed

Locked the existing top-level formal-gate summary fields in `formal_gate_remaining_deliverables` with regression tests, then regenerated the ledger and source freshness audit from clean source heads.

This is a gate-ledger readability and machine-consumption step. It does not approve F02.6, does not start local or remote training, does not run remote preflight, does not pull back formal outputs, and does not write paper-result material.

## Current Top-Level Fields

`0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json` now exposes the fields that a later handoff or audit can read without traversing the full acceptance matrix:

- `missing_counts_by_formal_category`: training `3`, evaluation `2`, acceptance `3`, formal_acceptance `2`.
- `missing_matrix_ids_by_formal_category`: the 10 missing training/evaluation/acceptance/H01-H02 matrix IDs.
- `next_blocked_lane`: `decision`.
- `h01_status`: `blocked_pending_decisions`.
- `h02_status`: `blocked_formal_output_acceptance`.
- `h02_formal_output_accepted`: `false`.
- `h02_paper_result_input_allowed`: `false`.

The full acceptance matrix and proof command plan remain unchanged in meaning: 10 rows, 20 local read-only proof commands, and no training/preflight/result-claim permission.

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py

PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit
```

Observed:

- Remaining-deliverables tests: `4 passed`.
- Source-freshness plus remaining-deliverables tests: `10 passed`.
- Regenerated remaining-deliverables status: `formal_gate_deliverables_blocked`.
- Regenerated source-freshness status: `source_freshness_risks_recorded_gate_still_blocked`.

## Boundary

This record only makes the blocked formal gate easier to inspect. The next formal action remains `record_f02_6_decision`; formal PPO training and H01/H02 formal evaluation remain blocked until Dr Sun closes F02.6 and the remote chain produces the missing artifacts.
