---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: candidate_or_smoke
---

# T14 6-method 候选主评测审计记录（含 MD-DQN）

## 结论

本次运行补齐了 T14 方法列表中的 MD-DQN，因此比上一轮 5-method candidate 更接近正式
T14。但它仍不能作为 T14 完成依据。

不能完成的原因：

1. T06 难度切点补充仍为 `reviewed:false`。
2. `mlp-dqn.pt` 是 DQN10 realmap smoke checkpoint，尚未经 Dr Sun 确认可作为正式 MD-DQN baseline。
3. Contract 判定仍失败：Complex/Extreme 桶中 F-N3P 相对 vanilla HA* 的中位时间缩减为负，未达到 `>=50%`。

## 运行信息

- execution_host: `gpu3070ti-relay`
- output_dir: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/`
- logs: `.pipeline/experiments/logs/20260620_t14_candidate_6method_fullscale_md_dqn.*`
- wall time: 20:40.54
- exit status: 0
- record_count: 1800
- query_count: 300
- seed_count: 5
- queries_per_bucket: Easy/Complex/Extreme 各 100
- methods: `f_n3p_knn`, `vanilla_ha`, `n3p_k1`, `voronoi_waypoint`, `bottleneck_waypoint`, `md_dqn`
- MD-DQN source_dir: `/home/ubuntu/DQN10/2_experiment`
- MD-DQN checkpoint: `/home/ubuntu/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt`

核心命令：

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir .pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5 \
  --methods f_n3p_knn,vanilla_ha,n3p_k1,voronoi_waypoint,bottleneck_waypoint,md_dqn \
  --distance-bins 8:12,12:16,16:20,20: \
  --allow-unreviewed-cutpoints \
  --bootstrap-resamples 5000 \
  --md-dqn-source-dir ~/DQN10/2_experiment \
  --md-dqn-checkpoint ~/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt \
  --md-dqn-algo mlp-dqn \
  --md-dqn-device cpu \
  --md-dqn-max-steps 600
```

## 完整性检查

| 项 | 结果 |
|---|---:|
| `record_count` | 1800 |
| `query_count` | 300 |
| `method_count` | 6 |
| `method_exception_total` | 0 |
| `collision_violation_total` | 0 |
| `t14_scale_satisfied` | true |
| `cutpoint_supplement_reviewed` | false |
| `formal_acceptance` | false |

## 关键结果

| method | bucket | success_rate | feasible_rate | median_time_s | median_path_inflation_ratio |
|---|---|---:|---:|---:|---:|
| `f_n3p_knn` | Easy | 0.98 | 0.98 | 0.3084 | 0.0000 |
| `f_n3p_knn` | Complex | 0.95 | 0.95 | 0.4077 | 0.0000 |
| `f_n3p_knn` | Extreme | 0.90 | 0.90 | 0.3925 | 0.0005 |
| `vanilla_ha` | Easy | 0.91 | 0.91 | 0.1944 | n/a |
| `vanilla_ha` | Complex | 0.83 | 0.83 | 0.3138 | n/a |
| `vanilla_ha` | Extreme | 0.82 | 0.82 | 0.3110 | n/a |
| `n3p_k1` | Easy | 0.96 | 0.96 | 0.3081 | 0.0000 |
| `n3p_k1` | Complex | 0.90 | 0.90 | 0.3432 | 0.0000 |
| `n3p_k1` | Extreme | 0.88 | 0.88 | 0.3781 | 0.0000 |
| `voronoi_waypoint` | Easy | 1.00 | 1.00 | 0.6260 | 0.0973 |
| `voronoi_waypoint` | Complex | 0.99 | 0.99 | 0.6210 | 0.0706 |
| `voronoi_waypoint` | Extreme | 0.99 | 0.99 | 0.6233 | 0.0594 |
| `bottleneck_waypoint` | Easy | 0.99 | 0.99 | 0.5131 | 0.0488 |
| `bottleneck_waypoint` | Complex | 1.00 | 1.00 | 0.6194 | 0.0411 |
| `bottleneck_waypoint` | Extreme | 1.00 | 1.00 | 0.6184 | 0.0367 |
| `md_dqn` | Easy | 0.00 | 0.00 | 0.1727 | n/a |
| `md_dqn` | Complex | 0.02 | 0.02 | 0.1712 | 0.6995 |
| `md_dqn` | Extreme | 0.01 | 0.01 | 0.1701 | 0.1733 |

MD-DQN 汇总：

| 项 | 数值 |
|---|---:|
| rows | 300 |
| success | 3 |
| feasible | 3 |
| `md_dqn_not_reached` | 297 |
| rollout_steps min/median/max | 1 / 600 / 600 |

## Contract 判定

| bucket | status | median_time_reduction | success_drop_pp | median_path_inflation_ratio |
|---|---|---:|---:|---:|
| Complex | fail | -0.2993 | -12.0 | 0.0000 |
| Extreme | fail | -0.2621 | -8.0 | 0.0005 |

失败原因不是碰撞或异常，而是主成功判据中的时间缩减没有达到。F-N3P 在 Complex/Extreme
比 vanilla HA* 中位时间更慢；虽然成功率更高、碰撞为 0，但不满足当前 Contract。

## 后续阻塞项

1. Dr Sun 审核 T06 cutpoint supplement。
2. Dr Sun 决定旧 DQN10 `mlp-dqn.pt` 是否可作为正式 MD-DQN baseline；从本候选结果看，它在 v9 ForestNav 分布上成功率仅 1%。
3. 若当前 Contract 不变，T14 的下一步应进入失败分析或方法重设计，而不是直接进入论文正结果写作。
