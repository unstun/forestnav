---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: smoke
---

# T14 MD-DQN 远端 smoke 审计记录

## 结论

本 smoke 只证明 MD-DQN adapter 能在 `gpu3070ti-relay` 上真实导入 DQN10 源码、加载
`mlp-dqn.pt` checkpoint 并通过 T14 runner 产出记录。它不能证明旧 checkpoint 适合作为
正式 MD-DQN baseline。

## 运行信息

- execution_host: `gpu3070ti-relay`
- source_dir: `/home/ubuntu/DQN10/2_experiment`
- checkpoint: `/home/ubuntu/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt`
- algo: `mlp-dqn`
- methods: `vanilla_ha`, `md_dqn`
- queries_per_bucket: 1
- seed_count: 1
- record_count: 6
- query_count: 3
- collision_violation_total: 0
- method_exception_total: 0

核心命令：

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir .pipeline/experiments/20260620_t14_md_dqn_remote_smoke \
  --queries-per-bucket 1 \
  --seed-count 1 \
  --queries-per-map 1 \
  --methods vanilla_ha,md_dqn \
  --distance-bins 4:8 \
  --allow-unreviewed-cutpoints \
  --no-enforce-t14-scale \
  --bootstrap-resamples 100 \
  --md-dqn-source-dir ~/DQN10/2_experiment \
  --md-dqn-checkpoint ~/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt \
  --md-dqn-algo mlp-dqn \
  --md-dqn-device cpu \
  --md-dqn-max-steps 600
```

## 逐 query 结果

| query_id | method | success | feasible | failure_reason | rollout_steps |
|---|---|---:|---:|---|---:|
| `easy_s00_q0000` | `vanilla_ha` | true | true |  | n/a |
| `easy_s00_q0000` | `md_dqn` | false | false | `md_dqn_not_reached` | 600 |
| `complex_s00_q0000` | `vanilla_ha` | true | true |  | n/a |
| `complex_s00_q0000` | `md_dqn` | false | false | `md_dqn_not_reached` | 600 |
| `extreme_s00_q0000` | `vanilla_ha` | true | true |  | n/a |
| `extreme_s00_q0000` | `md_dqn` | false | false | `md_dqn_not_reached` | 495 |

## 使用限制

1. T06 cutpoint supplement 仍是 `reviewed:false`，因此本 smoke 不能支撑 T14 完成。
2. `mlp-dqn.pt` 来自 DQN10 的 realmap smoke 训练输出，不是针对 v9 ForestNav query distribution 训练的正式 baseline。
3. 本 smoke 只覆盖 3 个 query；后续 full-scale candidate 应使用同一 MD-DQN 配置并保留完整 CSV。
