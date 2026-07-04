---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 status report consumes formal-gate gap-audit gap summary

## What changed

`build_module2_formal_gate_status_report.py` now consumes the top-level
`formal_gate_gap_audit.remaining_deliverables_gap_summary`, in addition to the
remaining-deliverables ledger summary.

The status report now exposes:

- `formal_gate_gap_audit_remaining_deliverables_gap_summary`
- `current_state.formal_gate_gap_audit_remaining_total_missing_deliverables`
- `current_state.formal_gate_gap_audit_remaining_open_category_count`

The status report now produces an input safety issue when:

- the formal gate gap audit is missing the remaining-deliverables gap summary,
- the formal gate gap-audit summary is not read-only,
- the formal gate gap-audit summary is marked as paper-result material,
- the formal gate gap-audit summary drifts from the remaining-deliverables ledger
  on summary id, total missing deliverables, open categories, category order,
  responsible stages, missing counts, or missing artifact matrix ids,
- the formal gate is blocked but its top-level gap summary claims zero remaining
  deliverables.

## Current generated state

`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
remains blocked:

- `status=formal_gate_status_blocked`
- `input_safety_issue_count=0`
- `remaining_deliverables_gap_summary.total_missing_deliverables=10`
- `formal_gate_gap_audit_remaining_deliverables_gap_summary.total_missing_deliverables=10`
- `remaining_deliverables_gap_summary.open_category_count=4`
- `formal_gate_gap_audit_remaining_deliverables_gap_summary.open_category_count=4`
- `permissions_now.remote_training_allowed_now=false`
- `permissions_now.formal_claim_allowed_now=false`

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report
jq '{status,input_safety_issue_count,ledger_total:.remaining_deliverables_gap_summary.total_missing_deliverables,formal_gate_total:.formal_gate_gap_audit_remaining_deliverables_gap_summary.total_missing_deliverables,ledger_categories:.remaining_deliverables_gap_summary.open_category_count,formal_gate_categories:.formal_gate_gap_audit_remaining_deliverables_gap_summary.open_category_count,claim_allowed:.permissions_now.formal_claim_allowed_now,remote_training_allowed:.permissions_now.remote_training_allowed_now}' 0_trials/module2_formal_gate_status_report/formal_gate_status_report.json
```

Observed results:

- Status report tests: 22 passed.
- Refreshed status report remains blocked.
- Ledger and formal gate gap-audit summaries both report 10 missing deliverables
  across 4 open categories.
- Remote training and formal claims remain disallowed.

## Boundary

This change did not:

- approve or reject F02.6,
- run local training,
- run remote sync, preflight, training, audit, or pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.
