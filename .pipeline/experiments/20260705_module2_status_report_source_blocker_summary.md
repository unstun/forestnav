---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Status Report Source-Blocker Summary

## Scope

This record covers a local read-only formal-gate status-report guard.

It does not approve or reject F02.6, run local training, run SSH, run remote
preflight, run remote PPO training, run remote audit/pullback, regenerate
H01/H02 from a new checkpoint, or write paper-result material.

## Problem

`formal_gate_remaining_deliverables` now exposes the exact source-freshness
blocking target summary. The higher-level `formal_gate_status_report` still
consumed remaining-deliverables acceptance/gap/proof/unlock summaries, but not
the new source-blocker summary.

That left one review path too indirect: the top formal status report did not
directly say that the current source-freshness blocker is
`gpu3070ti_readiness_refresh`, whose refresh requires external SSH and is not
allowed before the current gate closes.

## Action

`build_module2_formal_gate_status_report.py` now consumes
`remaining_deliverables.source_freshness_blocking_targets_summary`.

It now:

- exposes `remaining_deliverables_source_blocker_summary`
- writes source blocker fields into `current_state`
- checks that target IDs match `source_freshness_audit.blocking_ordered_regeneration_targets`
- checks that remote-readiness blocker IDs match the readiness/gpu target subset
- rejects summaries that claim remote readiness refresh, remote preflight,
  remote training, or formal claim are currently allowed
- rejects non-read-only or paper-result-material source blocker summaries

## Current Evidence

`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
now reports:

- status: `formal_gate_status_blocked`
- `remaining_deliverables_source_blocker_summary.summary_id=module2_source_freshness_blocking_targets_summary`
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
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
```

Observed: `103 passed in 9.19s`.

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

This change only strengthens local gate bookkeeping. It is not PPO-vs-RS
performance evidence and does not unlock remote execution.
