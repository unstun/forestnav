# Module2 H02.1 Local Smoke Preflight

- status: `blocked_full_smoke_missing_required_methods`
- full method smoke ready: `False`
- local training allowed: `False`

## Blocked Methods
- `ppo_analytic_operator`: missing_module2_rl_rs_checkpoint, f02_6_warm_start_decision_pending, f02_6_decision_packet_pending
- `ppo_rs_funnel`: missing_module2_rl_rs_checkpoint, f02_6_warm_start_decision_pending, f02_6_decision_packet_pending

## Available Subset Command

```bash
python -m forest_n3p.scripts.run_main_evaluation --output-dir 0_trials/module2_h02_local_smoke/h02_1_available_subset --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator --queries-per-bucket 1 --seed-count 1 --queries-per-map 1 --density-profile-buckets validation_t06 --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md --allow-unresolved-human-review --no-enforce-t14-scale --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt
```
