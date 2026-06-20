---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
task: T12
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: 962b3bb49a461d83d2f12898dbc0f3bd67ae8eae+dirty
execution_host: MacBook-Pro.local
---

# T12 Bottleneck Waypoint Hybrid A* 基线验收报告

## 结论

- 验收: `pass`
- 可行无碰撞路径: 10 / 10
- 验收阈值: >= 10 / 10
- 平均 waypoint 数: 2.800
- 局部低谷 waypoint 数: 21
- 长段守卫 waypoint 数: 7
- 段内失败尝试数: 0
- 被跳过 waypoint 数: 0
- 参数: bottleneck separation = 3.0 m, prominence = 0.10 m, max segment arc = 10.0 m, segment budget = 1.0 s / 2000 nodes

参数说明：本次继承 T08/T09 的程序化森林、车辆尺寸、段内 Hybrid A* 配置与 T06 难度切点；T05 的 `L_min=1.0m` 与 T06 切点仍为 `reviewed:false`，因此本报告只证明 T12 手工瓶颈规则基线工程闭环，不代表 T14 主评测结论。

## 方法

先对车辆中心可安全放置的自由空间提取 medial-axis skeleton，并沿 start-goal skeleton 路径读取 EDT 安全裕量；瓶颈定义为该一维安全裕量曲线的局部低谷（对 `-clearance` 用 prominence/distance 约束找峰）。相邻瓶颈间若 skeleton 弧长超过上限，则在该区间取最窄点作为长段守卫 waypoint。所有相邻 waypoint 再用与主方法一致的段内 Hybrid A* 连接，计时包含中轴、EDT、瓶颈检测和所有段内规划开销。

## 查询明细

| case | bucket | distance_bin | feasible | waypoints | local_min | guard | failed_segments | time(s) | expansions | figure |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | Easy | d08_12 | yes | 1 | 0 | 1 | 0 | 0.257 | 2 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_00.png` |
| 1 | Easy | d12_16 | yes | 2 | 2 | 0 | 0 | 0.356 | 3 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_01.png` |
| 2 | Easy | d16_20 | yes | 3 | 2 | 1 | 0 | 0.456 | 4 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_02.png` |
| 3 | Easy | d20_inf | yes | 5 | 3 | 2 | 0 | 0.667 | 6 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_03.png` |
| 4 | Complex | d08_12 | yes | 1 | 1 | 0 | 0 | 0.246 | 2 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_04.png` |
| 5 | Complex | d12_16 | yes | 3 | 3 | 0 | 0 | 0.457 | 4 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_05.png` |
| 6 | Complex | d16_20 | yes | 4 | 3 | 1 | 0 | 0.569 | 5 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_06.png` |
| 7 | Extreme | d20_inf | yes | 5 | 3 | 2 | 0 | 0.666 | 6 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_07.png` |
| 8 | Extreme | d08_12 | yes | 1 | 1 | 0 | 0 | 0.245 | 2 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_08.png` |
| 9 | Extreme | d12_16 | yes | 3 | 3 | 0 | 0 | 0.458 | 4 | `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/case_09.png` |

## 产物

- 明细 CSV: `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/records.csv`
- 摘要 JSON: `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/summary.json`
- 单查询 JSON/PNG: `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification`
