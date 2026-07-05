---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Remaining-Deliverables Source-Freshness Alignment

## Scope

This record covers a local read-only formal-gate bookkeeping fix.

It does not approve or reject F02.6, run local training, run remote preflight,
run remote PPO training, run remote audit/pullback, regenerate H01/H02 from a
new checkpoint, or write paper-result material.

## Problem

After the handoff-matrix gate refresh, `formal_gate_status_report` and
`source_freshness_audit` correctly reported source freshness as blocked for
remote preflight. However, the older
`formal_gate_remaining_deliverables.json` still exposed:

- `permissions_now.source_freshness_ready_for_remote_preflight=true`
- `current_gate_summary.source_freshness_status=source_freshness_clean_current`
- `current_gate_summary.source_freshness_blocking_regeneration_required=false`

That was stale bookkeeping. It did not authorize training, but it made one
formal-gate ledger disagree with the current source-freshness gate.

## Action

Refreshed the remaining-deliverables ledger and its downstream local consumers:

- `formal_gate_remaining_deliverables`
- `formal_gate_proof_audit`
- `formal_gate_status_report`
- `claim_safety`
- `paper_readiness`
- `formal_gate_proof_summary_chain_audit`
- `mainline_formal_gate_state_audit`
- `source_freshness_audit`

## Current Evidence

`0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
now reports:

- status: `formal_gate_deliverables_blocked`
- `permissions_now.source_freshness_ready_for_remote_preflight=false`
- `current_gate_summary.source_freshness_status=source_freshness_risks_recorded_gate_still_blocked`
- `current_gate_summary.source_freshness_blocking_regeneration_required=true`
- missing deliverables remain training/evaluation/acceptance/formal_acceptance
  = `3/2/3/2`

`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
still reports:

- status: `formal_gate_status_blocked`
- input safety issue count: `0`
- `permissions_now.source_freshness_ready_for_remote_preflight=false`

`0_trials/module2_source_freshness_audit/source_freshness_audit.json` reports:

- status: `source_freshness_risks_recorded_gate_still_blocked`
- source head: `c1d5cf4b57116b17aaf00a6af4c7b8983feda0b8`
- current head: `c1d5cf4b57116b17aaf00a6af4c7b8983feda0b8`
- risk counts: `historical_dirty=4`, `historical_clean=12`,
  `current_clean=7`
- blocking regeneration target count: `12`

The current-clean set includes the refreshed claim/status/readiness/proof
ledgers:

- `claim_safety`
- `paper_readiness`
- `formal_gate_status_report`
- `formal_gate_remaining_deliverables`
- `formal_gate_proof_audit`
- `formal_gate_proof_summary_chain_audit`
- `mainline_formal_gate_state_audit`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
```

Observed: `124 passed in 10.05s`.

## Remaining Gate

The real formal gate remains blocked:

- F02.6 warm-start decision is pending.
- formal training deliverables are missing: `train_final_model_zip`,
  `train_summary_json`, `train_training_manifest_json`
- formal evaluation deliverables are missing: `eval_gate3_eval_episodes_csv`,
  `eval_gate3_summary_json`
- formal acceptance/pullback deliverables are missing:
  `gate3_trial_manifest_json`, `gate3_formal_audit_json`,
  `pulled_back_checkpoint_hash_record`
- H01/H02 formal acceptance remains blocked:
  `h01_ready_for_formal_run`, `h02_formal_output_acceptance`

This change only aligns gate bookkeeping. It is not PPO-vs-RS performance
evidence and does not unlock remote execution.
