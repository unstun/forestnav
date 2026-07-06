---
topic: module2-v2-contract-promotion-dry-run
status: promotion_apply_ready
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Contract Promotion Dry-Run

## Scope

This is a dry-run of the v2 contract promotion application path. It does not
modify `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`,
does not approve the contract, does not run remote preflight, does not run
remote PPO training, and does not write paper result material.

## What Changed

- Added `2_experiment/forest_n3p/scripts/apply_module2_v2_contract_promotion.py`.
- Added `2_experiment/forest_n3p/tests/test_apply_module2_v2_contract_promotion.py`.
- Generated:
  - `0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json`

## Current Dry-Run Result

Command used:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.apply_module2_v2_contract_promotion \
  --status approved \
  --decider 'Dr Sun' \
  --remote-alias gpu3070ti-relay \
  --confirm-training-budget \
  --confirm-unsafe-failure-thresholds \
  --dry-run \
  --manifest-out 0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json
```

The generated dry-run manifest reports:

- status: `promotion_apply_ready`
- source_head: `cca4cba1707732b49216e8cc0fc2b64704059097`
- dry_run: `true`
- writes_contract: `false`
- blocker_count: `0`
- target_contract_status: `approved`
- promoted_contract_text contains `status: approved`

The real contract file was checked after the dry-run and remains:

- `status: draft`

## Boundary

This dry-run only proves that the promotion application path is ready if Dr Sun
explicitly approves the packet values. It is not itself an approval.

The next real approval action still requires Dr Sun to explicitly confirm:

- target status: `approved` or `frozen`;
- remote alias: recommended `gpu3070ti-relay`;
- training budget: `500000` timesteps, `4` envs, seed `20260706`;
- unsafe failure thresholds: `collision_rate >= 0.30`,
  `truncation_rate >= 0.20`.

After a real promotion, the next stage remains source-freshness regeneration,
not remote training.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_apply_module2_v2_contract_promotion.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_packet.py`
  -> `7 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/apply_module2_v2_contract_promotion.py 2_experiment/forest_n3p/scripts/build_module2_v2_contract_promotion_packet.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed
