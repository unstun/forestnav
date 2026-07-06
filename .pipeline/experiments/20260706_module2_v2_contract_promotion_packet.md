---
topic: module2-v2-contract-promotion-packet
status: v2_contract_promotion_packet_ready_awaiting_dr_sun
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Contract Promotion Packet

## Scope

This is a formal-gate approval packet for Dr Sun. It does not approve the
contract, edit the contract to `approved` or `frozen`, run remote preflight, run
remote PPO training, or write paper result material.

## What Changed

- Added `2_experiment/forest_n3p/scripts/build_module2_v2_contract_promotion_packet.py`.
- Added `2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_packet.py`.
- Generated:
  - `0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.json`
  - `0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.md`

## Current Result

The generated packet reports:

- status: `v2_contract_promotion_packet_ready_awaiting_dr_sun`
- source_head: `d29e2d84c68e04cd9b680adcfeba186ac82f93f7`
- audit_issue_count: `0`
- remote_training_allowed_now: `false`
- recommended_alias: `gpu3070ti-relay`
- approval_items:
  - `remote_alias`
  - `training_budget`
  - `unsafe_failure_thresholds`
  - `contract_status_action`

Local SSH config evidence:

- `gpu3070ti-relay` resolves as `ubuntu@127.0.0.1:23070` through
  `ubuntu-obgx`.
- `gpu3070ti-reply` resolves as direct hostname `gpu3070ti-reply` with port
  `22`, so it is not the currently evidenced 3070 Ti relay route.

## Dr Sun Approval Items

Before the contract can be promoted, Dr Sun must explicitly decide:

1. remote alias: packet recommends `gpu3070ti-relay`;
2. training budget: seed `20260706`, `500000` timesteps, `4` envs, `256`
   rollout steps, batch `256`, `8` epochs, learning rate `0.0001`, entropy
   coefficient `0.01`, checkpoint frequency `25000`;
3. unsafe failure thresholds: `collision_rate >= 0.30` and
   `truncation_rate >= 0.20`;
4. contract status action: `approved` or `frozen`.

The packet recommends `approved`, because the contract may still need future
revision if the next formal attempt fails. `frozen` remains a valid stricter
choice if Dr Sun wants no edits without a successor contract.

## Boundary

Even after Dr Sun approves one of the status actions, the next stage is only:

1. commit the contract status promotion;
2. re-run v2 contract readiness gate and require
   `v2_contract_ready_for_source_freshness`;
3. regenerate source-freshness artifacts;
4. generate the v2 remote execution packet;
5. run remote preflight only after the regenerated packet allows it.

The packet itself does not authorize remote preflight or training.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_packet.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_readiness_gate.py`
  -> `8 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_contract_promotion_packet.py 2_experiment/forest_n3p/scripts/build_module2_v2_contract_readiness_gate.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed
