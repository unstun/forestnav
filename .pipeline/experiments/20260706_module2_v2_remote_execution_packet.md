---
topic: module2-v2-remote-execution-packet
status: blocked_until_v2_contract_promotion
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Remote Execution Packet

## Scope

This is a remote command packetization artifact. It does not run SSH, does not
run remote preflight, does not train, does not audit, does not pull back
artifacts, and does not write paper result material.

## What Changed

- Added `2_experiment/forest_n3p/scripts/build_module2_v2_remote_execution_packet.py`.
- Added `2_experiment/forest_n3p/tests/test_module2_v2_remote_execution_packet.py`.
- Generated:
  - `0_trials/module2_v2_remote_execution_packet/v2_remote_execution_packet.json`
  - `0_trials/module2_v2_remote_execution_packet/v2_remote_execution_packet.md`

## Current Result

The generated packet reports:

- status: `blocked_until_v2_contract_promotion`
- source_head: `331231f71c06ca1e5dda670bd83d693b7aab8842`
- ready_to_run_remote_preflight: `false`
- ready_to_run_remote_training: `false`
- remote_training_allowed_now: `false`
- blockers:
  - `v2_contract_not_promoted`
  - `v2_contract_readiness_not_ready`
  - `source_freshness_not_ready`

The packet does generate command templates for the future chain:

- `sync_to_remote`
- `run_remote_preflight`
- `run_remote_training`
- `run_remote_audit`
- `pullback_after_audit`

All of those commands are currently `allowed_now=false`.

## V2 Parameter Coverage

The future remote training command contains:

- `--contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`
- `--train-total-timesteps 500000`
- `--train-n-envs 4`
- `--train-n-steps 256`
- `--train-batch-size 256`
- `--train-n-epochs 8`
- `--train-learning-rate 0.0001`
- `--train-ent-coef 0.01`
- `--train-checkpoint-freq 25000`
- `--bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt`

The future audit command contains:

- `--contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`
- `--warm-start-decision approved_obstacle_summary`
- `--required-success-threshold 0.8`
- `--required-train-curriculum f03`
- `--required-eval-curriculum f03`

## Boundary

This packet is not a training authorization. The next actual stages remain:

1. Dr Sun explicitly approves or freezes the v2 contract.
2. Apply and commit the contract promotion.
3. Re-run v2 readiness and source-freshness.
4. Regenerate this v2 remote packet.
5. Only then, if packet says allowed, run remote preflight.
6. Remote training still requires a ready remote preflight manifest.

Invalid substitutes remain invalid:

- local PPO training output;
- old v1 remote execution packet;
- failed `gate3_obstacle_summary_warm_approved_v1` checkpoint;
- remote preflight smoke;
- paper table or appendix prose.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_remote_execution_packet.py`
  -> `3 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_remote_execution_packet.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed
