# Module2 v1 Evaluation Manifest

- status: `blocked_pending_decisions`
- contract: `.pipeline/contracts/module2-ppo-funnel-expansion.md`
- scale: `100` queries/bucket, `5` seeds

## Methods
- `ha_no_analytic`: ready (blockers: none)
- `ha_single_rs`: ready (blockers: none)
- `ha_dang_multi_rs`: ready (blockers: none)
- `f_n3p_knn`: ready_if_preflight_passes (blockers: none)
- `mlp`: ready (blockers: none)
- `bc_analytic_operator`: blocked (blockers: missing_module2_bc_checkpoint)
- `ppo_analytic_operator`: blocked (blockers: missing_module2_rl_rs_checkpoint, f02_6_warm_start_decision_pending)
- `ppo_rs_funnel`: blocked (blockers: missing_module2_rl_rs_checkpoint, f02_6_warm_start_decision_pending)

## Blockers
- `f02_6_warm_start_decision_pending`
- `missing_module2_bc_checkpoint`
- `missing_module2_rl_rs_checkpoint`
- `realmap_query_generation_not_frozen`

## F02.6 Decision Packet
- path: `None`
- status: `not_provided`
- effective decision: `pending`

## Required Output Schema
- records.csv columns: `36` required
- summary_by_method_bucket.csv columns: `24` required
- schema status: `frozen_for_module2_v1`

## Formal Command

```bash
# blocked: see blockers above
```
