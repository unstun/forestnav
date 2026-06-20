---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
task: T11
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: 9d7510fcfb3108de76ca44b9d7dcead3754725fd
execution_host: MacBook-Pro.local
---

# T11 Voronoi Waypoint Hybrid A* 基线验收报告

## 结论

- 验收: `pass`
- 可行无碰撞路径: 10 / 10
- 验收阈值: >= 10 / 10
- 平均 waypoint 数: 2.600
- 段内失败尝试数: 0
- 被跳过 waypoint 数: 0
- 参数: waypoint spacing = 6.0 m, segment budget = 1.0 s / 2000 nodes

参数说明：本次继承 T08/T09 的程序化森林、车辆尺寸、段内 Hybrid A* 配置与 T06 难度切点；T05 的 `L_min=1.0m` 与 T06 切点仍为 `reviewed:false`，因此本报告只证明 T11 基线工程闭环，不代表 T14 主评测结论。

## 方法

对车辆中心可安全放置的自由空间提取 medial-axis skeleton，沿 skeleton 图搜索 start-goal 之间的几何路径，按近似 `L_max` 的 6 m 间距放置 waypoint，再用与主方法相同的段内 Hybrid A* 逐段连接。计时包含 skeleton 提取、图搜索、waypoint 放置和所有段内规划开销。

## 查询明细

| case | bucket | distance_bin | feasible | waypoints | failed_segments | skipped | time(s) | expansions | figure |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 0 | Easy | d08_12 | yes | 1 | 0 | 0 | 0.255 | 8 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_00.png` |
| 1 | Easy | d12_16 | yes | 3 | 0 | 0 | 0.459 | 4 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_01.png` |
| 2 | Easy | d16_20 | yes | 3 | 0 | 0 | 0.981 | 886 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_02.png` |
| 3 | Easy | d20_inf | yes | 4 | 0 | 0 | 0.568 | 5 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_03.png` |
| 4 | Complex | d08_12 | yes | 1 | 0 | 0 | 0.246 | 2 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_04.png` |
| 5 | Complex | d12_16 | yes | 2 | 0 | 0 | 0.349 | 3 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_05.png` |
| 6 | Complex | d16_20 | yes | 3 | 0 | 0 | 0.462 | 4 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_06.png` |
| 7 | Extreme | d20_inf | yes | 5 | 0 | 0 | 0.688 | 20 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_07.png` |
| 8 | Extreme | d08_12 | yes | 2 | 0 | 0 | 0.348 | 11 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_08.png` |
| 9 | Extreme | d12_16 | yes | 2 | 0 | 0 | 0.478 | 243 | `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/case_09.png` |

## 产物

- 明细 CSV: `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/records.csv`
- 摘要 JSON: `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/summary.json`
- 单查询 JSON/PNG: `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification`
