---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: superseded_candidate
---

# T14 5-method 候选主评测审计记录（已被替代）

本目录是修复 `planner_run_from_path_stats` 评测路径口径之前的候选运行结果。

该运行本身 exit status 为 0，输出文件完整，但不应作为后续分析依据。原因是
vanilla HA* 的公共转换函数当时只使用稀疏 planner endpoint path，而没有优先使用
Hybrid A* stats 中的 `trace_poses`。这会让路径长度、安全裕量、碰撞违例等指标与
实际稠密轨迹不一致。

已替代目录：

- `.pipeline/experiments/20260620_t14_candidate_5method_fullscale_tracefix/`

关键差异：

| 项 | 本目录 | tracefix 目录 |
|---|---:|---:|
| `record_count` | 1500 | 1500 |
| `method_exception_total` | 0 | 0 |
| `collision_violation_total` | 503 | 0 |
| `formal_acceptance` | false | false |

后续 T14 候选分析应使用 tracefix 目录。本目录只保留为问题定位和审计证据。
