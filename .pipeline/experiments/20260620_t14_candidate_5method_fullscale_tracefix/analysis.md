---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: candidate_or_smoke
---

# T14 5-method 候选主评测审计记录

## 结论

本次运行只能作为 T14 候选证据，不能作为 T14 完成依据。

原因有三点：

1. T06 难度切点补充仍为 `reviewed:false`，正式 T14 禁止基于未审核切点完成。
2. 本次只包含 5 个方法，缺少正式方法列表中的 MD-DQN。
3. Contract 判定仍失败：Complex/Extreme 桶的 F-N3P 相对 vanilla HA* 中位时间缩减为负，未达到 `>=50%`。

## 本轮修复

本轮先修复了两个评测前暴露的问题：

1. Reeds-Shepp 近零平移数值问题：`asin` 参数在浮点误差下略超 `[-1, 1]`，导致 Hybrid A* 解析扩展崩溃。
2. vanilla HA* 评测路径口径问题：`planner_run_from_path_stats` 原先只使用稀疏 planner endpoint path；现在优先使用 `stats["trace_poses"]` 作为评测路径，并在 metadata 中记录 `evaluation_path_source`。

修复后本地和远端测试均通过：`PYTHONPATH=2_experiment python -m pytest tests -q` 为 `49 passed`。

## 运行信息

- 远端机器：`gpu3070ti-relay`
- GPU：RTX 3070 Ti Laptop GPU 8GB
- 输出目录：`.pipeline/experiments/20260620_t14_candidate_5method_fullscale_tracefix/`
- 日志：`.pipeline/experiments/logs/20260620_t14_candidate_5method_fullscale_tracefix.*`
- wall time：18:19.59
- exit status：0
- record_count：1500
- query_count：300
- seed_count：5
- queries_per_bucket：Easy/Complex/Extreme 各 100
- methods：`f_n3p_knn`, `vanilla_ha`, `n3p_k1`, `voronoi_waypoint`, `bottleneck_waypoint`

核心命令：

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir .pipeline/experiments/20260620_t14_candidate_5method_fullscale_tracefix \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5 \
  --methods f_n3p_knn,vanilla_ha,n3p_k1,voronoi_waypoint,bottleneck_waypoint \
  --distance-bins 8:12,12:16,16:20,20: \
  --allow-unreviewed-cutpoints \
  --bootstrap-resamples 5000
```

## 完整性检查

| 项 | 结果 |
|---|---:|
| `record_count` | 1500 |
| `query_count` | 300 |
| `method_count` | 5 |
| `method_exception_total` | 0 |
| `collision_violation_total` | 0 |
| `formal_acceptance` | false |

`vanilla_ha` 的 `evaluation_path_source` 分布：

| source | count |
|---|---:|
| `trace_poses` | 257 |
| `planner_path` | 43 |

修复前候选目录 `.pipeline/experiments/20260620_t14_candidate_5method_fullscale/` 的
`collision_violation_total` 为 503；修复后为 0。后续分析应使用本目录结果。

## 关键结果

| method | bucket | success_rate | feasible_rate | median_time_s | median_path_inflation_ratio |
|---|---|---:|---:|---:|---:|
| `f_n3p_knn` | Easy | 0.98 | 0.98 | 0.3035 | 0.0000 |
| `f_n3p_knn` | Complex | 0.95 | 0.95 | 0.3930 | 0.0000 |
| `f_n3p_knn` | Extreme | 0.90 | 0.90 | 0.3933 | 0.0009 |
| `vanilla_ha` | Easy | 0.91 | 0.91 | 0.1949 | n/a |
| `vanilla_ha` | Complex | 0.83 | 0.83 | 0.3032 | n/a |
| `vanilla_ha` | Extreme | 0.83 | 0.83 | 0.3111 | n/a |
| `n3p_k1` | Easy | 0.97 | 0.97 | 0.3065 | 0.0000 |
| `n3p_k1` | Complex | 0.90 | 0.90 | 0.3366 | 0.0000 |
| `n3p_k1` | Extreme | 0.88 | 0.88 | 0.3659 | 0.0000 |
| `voronoi_waypoint` | Easy | 1.00 | 1.00 | 0.6192 | 0.0985 |
| `voronoi_waypoint` | Complex | 0.99 | 0.99 | 0.6183 | 0.0629 |
| `voronoi_waypoint` | Extreme | 0.99 | 0.99 | 0.6218 | 0.0624 |
| `bottleneck_waypoint` | Easy | 0.99 | 0.99 | 0.5079 | 0.0492 |
| `bottleneck_waypoint` | Complex | 1.00 | 1.00 | 0.6180 | 0.0397 |
| `bottleneck_waypoint` | Extreme | 1.00 | 1.00 | 0.6202 | 0.0363 |

Contract bucket verdicts：

| bucket | status | median_time_reduction | success_drop_pp | median_path_inflation_ratio |
|---|---|---:|---:|---:|
| Complex | fail | -0.2962 | -12.0 | 0.0000 |
| Extreme | fail | -0.2643 | -7.0 | 0.0009 |

## 后续阻塞项

1. Dr Sun 需要审核并确认 T06 cutpoint supplement；否则任何 T14 只能是 candidate/smoke。
2. 需要确认旧 `mlp-dqn.pt` / DQN10 checkpoint 是否可作为正式 MD-DQN 基线；若不能，需要补训练或重新定义 baseline。
3. 若坚持当前 Contract，F-N3P 未达到主成功判据，需要进入失败分析或重新设计，而不是直接写成正结果。
