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
- `bc_analytic_operator`: blocked (blockers: missing_main_evaluation_method, bc_operator_loader_not_implemented)
- `ppo_analytic_operator`: blocked (blockers: missing_main_evaluation_method, outside_current_funnel_contract_until_explicitly_added)
- `ppo_rs_funnel`: blocked (blockers: missing_module2_rl_rs_checkpoint, f02_6_warm_start_decision_pending)

## Blockers
- `f02_6_warm_start_decision_pending`
- `missing_required_method_implementation`
- `realmap_query_generation_not_frozen`

## Formal Command

```bash
# blocked: see blockers above
```
