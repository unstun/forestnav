---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_remaining_deliverables_top_level_gate_permissions
trust_level: audit_record
---

# Module2 Remaining Deliverables Top-Level Gate Permissions

## Scope

This record covers a read-only schema clarification in the Module2 formal-gate remaining-deliverables ledger.

It does not approve F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_remaining_deliverables` already exposed current gate permissions inside `permissions_now`, and its Markdown checklist showed selected values. A reviewer or downstream checker still had to inspect nested fields to confirm whether remote preflight, remote training, formal H01/H02 acceptance, formal claim, or paper-result material were currently allowed.

For the formal PPO-vs-RS gate, these permissions should be explicit at the top level next to `missing_deliverable_count`, because the ledger is the main human-readable list of missing training, evaluation, and acceptance artifacts.

## Change

`build_module2_formal_gate_remaining_deliverables.py` now writes top-level:

- `local_training_allowed_now`
- `remote_preflight_allowed_now`
- `remote_training_allowed_now`
- `formal_h01_evaluation_allowed_now`
- `formal_h02_acceptance_allowed_now`
- `formal_claim_allowed_now`
- `paper_result_material_allowed_now`

The Markdown summary now prints these fields directly. Existing artifact-boundary fields remain unchanged: the ledger itself is still read-only and does not execute commands, run training, or authorize claims.

## Current Gate State

The current real gate remains blocked. F02.6 remains pending, and formal PPO checkpoint/evaluation/acceptance outputs remain missing.

The missing formal deliverables remain:

- training: `train_final_model_zip`, `train_summary_json`, `train_training_manifest_json`
- evaluation: `eval_gate3_eval_episodes_csv`, `eval_gate3_summary_json`
- acceptance: `gate3_trial_manifest_json`, `gate3_formal_audit_json`, `pulled_back_checkpoint_hash_record`
- formal acceptance: `h01_ready_for_formal_run`, `h02_formal_output_acceptance`

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py`
  - Result: `5 passed`.

## Boundary

This is a gate-ledger readability and machine-readability improvement. It is not evidence that PPO has replaced RS in formal evaluation, and it does not satisfy any missing training, evaluation, acceptance, or H01/H02 formal acceptance artifact.
