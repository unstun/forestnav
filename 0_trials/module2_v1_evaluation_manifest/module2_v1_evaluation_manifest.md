# Module2 v1 Evaluation Manifest

- status: `ready_for_formal_run`
- contract: `.pipeline/contracts/module2-ppo-funnel-expansion.md`
- scale: `100` queries/bucket, `5` seeds

## Methods
- `ha_no_analytic`: ready (blockers: none)
- `ha_single_rs`: ready (blockers: none)
- `ha_dang_multi_rs`: ready (blockers: none)
- `f_n3p_knn`: ready_if_preflight_passes (blockers: none)
- `mlp`: ready (blockers: none)
- `bc_analytic_operator`: ready (blockers: none)
- `ppo_analytic_operator`: ready (blockers: none)
- `ppo_rs_funnel`: ready (blockers: none)

## Blockers
- none

## F02.6 Decision Packet
- path: `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- status: `pending_human_decision`
- effective decision: `approved_obstacle_summary`

## Required Output Schema
- records.csv columns: `36` required
- summary_by_method_bucket.csv columns: `24` required
- schema status: `frozen_for_module2_v1`

## Formal Command

```bash
python -m forest_n3p.scripts.run_main_evaluation --output-dir 0_trials/module2_v1_evaluation/formal_run --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator,ppo_analytic_operator,ha_rl_rs_ppo --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --module2-rl-rs-checkpoint 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip --queries-per-bucket 100 --seed-count 5 --queries-per-map 5 --density-profile-buckets validation_t06 --distance-bins 8:12,12:16,16:20,20: --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md --bootstrap-resamples 10000
```
