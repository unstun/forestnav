---
origin: ai+local-source
reviewed: false
date: 2026-07-06
status: draft_contract_created
scope: module2 stronger obstacle-summary warm-start contract draft
---

# Module2 Stronger Obstacle-Summary Warm-Start Contract Draft

## What Changed

Created `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`
as a draft Research Contract for the protocol lane selected by Dr Sun:
`stronger_obstacle_summary_warm_start` with `contract_action=draft_new_contract`.

## Boundary

This is not paper result material. It does not approve a contract, does not run
local training, does not run remote preflight, does not run remote PPO training,
does not run H01/H02 formal evaluation, and does not allow a formal claim.

The old failed warm-start Gate3 result remains negative formal evidence:

- episodes: `64`
- terminal-RS success rate: `0.53125`
- required threshold: `0.8`
- collision rate: `0.34375`
- truncation rate: `0.125`

## Fresh Artifacts Still Missing

The next success attempt still requires all fresh artifacts below:

- `new_or_revised_research_contract`
- `train_final_model_zip`
- `train_summary_json`
- `train_training_manifest_json`
- `eval_gate3_eval_episodes_csv`
- `eval_gate3_summary_json`
- `gate3_trial_manifest_json`
- `gate3_formal_audit_json`
- `pulled_back_checkpoint_hash_record`
- `h02_formal_output_acceptance`

## Important Draft Gap

The current formal audit code still hard-codes the old v1 contract path. Before
any v2 formal run can be accepted, the runner/evaluator/audit chain must record
the approved v2 contract path in training, evaluation, trial, and audit
artifacts.

## Verification Plan For This Draft

- Markdown/file creation is the only intended change.
- Targeted formal-gate tests should still pass because this draft does not
  unlock training or alter gate JSON semantics.
