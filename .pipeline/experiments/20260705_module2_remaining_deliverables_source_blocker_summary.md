---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Remaining-Deliverables Source-Blocker Summary

## Scope

This record covers a local read-only ledger improvement for the Module2 formal
gate.

It does not approve or reject F02.6, run local training, run SSH, run remote
preflight, run remote PPO training, run remote audit/pullback, regenerate
H01/H02 from a new checkpoint, or write paper-result material.

## Problem

`source_freshness_audit.json` already listed the exact source-freshness
regeneration targets. The human-facing remaining-deliverables ledger only
surfaced counts, so a reviewer had to open the source-freshness JSON to see
which target was blocking remote preflight.

That was too indirect for the formal gate because the current blocking target is
the stale `gpu3070ti_readiness_refresh` artifact. Refreshing that artifact would
require SSH to the relay host, and this session is not authorized to perform
remote preflight/readiness work before F02.6 closes.

## Action

`build_module2_formal_gate_remaining_deliverables.py` now emits
`source_freshness_blocking_targets_summary`.

The summary exposes:

- the source-freshness status
- blocking target count
- blocking target IDs
- remote-readiness blocking target IDs
- whether remote-readiness refresh requires external SSH
- current remote-readiness/preflight/training/claim authorization flags
- one row per blocking source-freshness target

The Markdown ledger now includes a `Source-Freshness Blocking Targets` section.

## Current Evidence

`0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
now reports:

- status: `formal_gate_deliverables_blocked`
- `source_freshness_blocking_targets_summary.summary_id=module2_source_freshness_blocking_targets_summary`
- blocking target IDs include `gpu3070ti_readiness_refresh`
- `remote_readiness_refresh_requires_external_ssh=true`
- `remote_readiness_refresh_allowed_now=false`
- `remote_preflight_allowed_now=false`
- `remote_training_allowed_now=false`
- `formal_claim_allowed_now=false`

The formal deliverable gap is unchanged:

- training missing: `3`
- evaluation missing: `2`
- acceptance missing: `3`
- formal acceptance missing: `2`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
```

Observed: `108 passed in 9.32s`.

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

This change only makes a local ledger more explicit. It is not PPO-vs-RS
performance evidence and does not unlock remote execution.
