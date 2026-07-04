---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 status report consumes formal gate gap summary

## What changed

`build_module2_formal_gate_status_report.py` now consumes `formal_gate_remaining_deliverables.deliverable_gap_summary`.

The status report now exposes:

- `current_state.remaining_deliverables_gap_total_missing_deliverable_count`
- `current_state.remaining_deliverables_gap_open_category_count`
- top-level `remaining_deliverables_gap_summary`

It also rejects gap-summary drift, including:

- missing `deliverable_gap_summary`,
- wrong summary id,
- non-read-only execution boundary,
- missing `not_paper_result_material`,
- total missing deliverables inconsistent with the acceptance matrix,
- open category count inconsistent with blocked categories,
- category order mismatch,
- category missing-count mismatch,
- wrong responsible stage,
- blocked stage marked allowed,
- missing artifact ids inconsistent with the acceptance matrix,
- missing acceptance predicate count,
- missing invalid-substitute count.

## Current generated state

`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json` remains blocked:

- `status=formal_gate_status_blocked`
- `current_state.decision_status=pending_human_decision`
- `current_state.remaining_deliverables_gap_total_missing_deliverable_count=10`
- `current_state.remaining_deliverables_gap_open_category_count=4`
- `permissions_now.local_training_allowed_now=false`
- `permissions_now.remote_preflight_allowed_now=false`
- `permissions_now.remote_training_allowed_now=false`
- `permissions_now.formal_claim_allowed_now=false`
- `input_safety_issue_count=0`

The inherited gap categories remain:

- training: 3 missing, stage `gate3_remote_training`, not allowed now,
- evaluation: 2 missing, stage `gate3_remote_audit_pullback`, not allowed now,
- acceptance: 3 missing, stage `gate3_remote_audit_pullback`, not allowed now,
- formal_acceptance: 2 missing, stage `regenerate_h01_h02_formal_artifacts`, not allowed now.

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py 2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report
jq -c '{status,current_state:{decision:.current_state.decision_status,remaining:.current_state.remaining_deliverables_status,missing:.current_state.remaining_deliverables_missing_deliverable_count,gap_missing:.current_state.remaining_deliverables_gap_total_missing_deliverable_count,gap_open:.current_state.remaining_deliverables_gap_open_category_count},gap:.remaining_deliverables_gap_summary | {present,total_missing_deliverables,open_category_count,category_order,categories:(.categories|to_entries|map({category:.key,missing_count:.value.missing_count,stage:.value.responsible_stage_id,allowed:.value.responsible_stage_allowed_now}))},permissions_now,input_safety_issue_count,next_blocked_lane}' 0_trials/module2_formal_gate_status_report/formal_gate_status_report.json
```

Observed results:

- Status report tests: 20 passed.
- Status/claim/readiness related tests: 45 passed.
- Refreshed status report still has `formal_gate_status_blocked`.

## Boundary

This change did not:

- approve or reject F02.6,
- run local training,
- run remote sync, preflight, training, audit, or pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.
