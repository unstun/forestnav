---
topic: module2-v2-contract-readiness-gate
status: v2_contract_readiness_blocked
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Contract Readiness Gate

## Scope

This is a formal-gate infrastructure update. It does not run local training,
remote preflight, remote PPO training, H01/H02 formal evaluation, or paper-result
writing.

## What Changed

- Added `2_experiment/forest_n3p/scripts/build_module2_v2_contract_readiness_gate.py`.
- Added `2_experiment/forest_n3p/tests/test_module2_v2_contract_readiness_gate.py`.
- Generated:
  - `0_trials/module2_v2_contract_readiness_gate/v2_contract_readiness_gate.json`
  - `0_trials/module2_v2_contract_readiness_gate/v2_contract_readiness_gate.md`

## Current Result

The generated readiness gate reports:

- status: `v2_contract_readiness_blocked`
- source_head: `21a4f99885461c99d3b97ba3c9ad39551ac3803d`
- next_action: `promote_or_edit_v2_contract_before_source_freshness`
- blocker_count: `1`
- blocker: `contract_status_not_approved_or_frozen`
- runner_command_contains_v2_params: `true`

This means the current blocker is not hidden PPO parameter drift, missing oracle
path, missing BC checkpoint, or failed preflight packetization. The blocker is
the intentional one: `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`
is still `draft`.

## Gate Semantics

The gate can only move from `v2_contract_readiness_blocked` to
`v2_contract_ready_for_source_freshness` when:

- the v2 contract status is `approved` or `frozen`;
- selected lane remains `stronger_obstacle_summary_warm_start`;
- contract action remains `draft_new_contract`;
- preflight still carries the v2 contract path;
- stronger PPO parameters still match the v2 draft:
  - `train_total_timesteps=500000`
  - `train_n_envs=4`
  - `train_n_steps=256`
  - `train_batch_size=256`
  - `train_n_epochs=8`
  - `train_learning_rate=0.0001`
  - `train_ent_coef=0.01`
  - `train_checkpoint_freq=25000`

Even if the gate becomes ready, it only allows the next non-training stage:
source-freshness regeneration and remote-packet generation. It still does not
directly authorize remote preflight or remote PPO training.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_contract_readiness_gate.py`
  -> `5 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_contract_readiness_gate.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed

## Boundary

Invalid substitutes remain invalid:

- local PPO training output;
- failed `gate3_obstacle_summary_warm_approved_v1` checkpoint;
- old v1 contract audit;
- H02 smoke rows;
- paper table or appendix prose.
