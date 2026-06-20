---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: a66d4b24292381f252c93c2119e1bc0d678a382c+working-tree-t05
execution_host: gpu3070ti-relay
---

# T05 标签预实验报告

## 目的

验证前向贪心 Reeds-Shepp 子目标标签管线在小规模程序化森林地图上的质量，重点检查教师求解成功率、标签提取失败率、段数分布和样本量。

## 实验设置

```text
map_count=20
queries_per_map=10
seed=20260620
map_size_cells=300x300
resolution_m=0.1
L_max_m=8.0
L_min_m=1.0
teacher_timeout_s=2.5
teacher_max_nodes=15000
```

## 参数调整记录

同一随机种子和查询设置下，先用默认 `L_min=1.5m, L_max=8.0m` 做筛查运行：
教师求解成功率为 74.0%，标签失败率为 23.6%，未达到 `<20%` 验收线。
失败原因以 `short_progress` 为主（35 个标签失败中 34 个为推进距离 `< L_min`，
1 个为 `no_reachable_candidate`），因此本次只降低 `L_min` 到 1.0m，
保持 `L_max=8.0m` 不变。

该调整是 T05 技术预实验结论，不等同于冻结论文参数；T05 标记“需人工确认”，
后续是否把 `L_min=1.0m` 写入正式实验配置，需要 Dr Sun 审阅后决定。

## 总体结果

| 指标 | 数值 |
|---|---:|
| 地图生成成功数 | 20 / 20 |
| 查询总数 | 200 |
| 教师求解成功率 | 74.0% |
| 标签尝试数 | 148 |
| 标签成功数 | 124 |
| 标签失败率 | 16.2% |
| 每条成功标签路径平均总段数 | 3.234 |
| 总样本数 | 277 |

## 分桶结果

| 难度 | 查询数 | 教师成功率 | 标签失败率 | 平均总段数 | 样本数 |
|---|---:|---:|---:|---:|---:|
| high | 60 | 53.3% | 34.4% | 3.238 | 47 |
| low | 70 | 87.1% | 6.6% | 3.123 | 121 |
| medium | 70 | 78.6% | 16.4% | 3.370 | 109 |

## 段长分布

| min | mean | max |
|---:|---:|---:|
| 1.000 | 5.885 | 8.400 |

## 验收判断

- 标签失败率 `< 20%`：通过。
- 注意：high 桶标签失败率仍为 34.4%，说明高密度设置下标签规则仍脆弱；
  T06 难度轴标定时需要重点检查 high/Extreme 桶是否需要单独参数或重新划桶。

## 产物

- `maps.csv`: `.pipeline/experiments/20260620_t05_label_pilot_lmin1p0/maps.csv`
- `queries.csv`: `.pipeline/experiments/20260620_t05_label_pilot_lmin1p0/queries.csv`
- `summary.json`: `.pipeline/experiments/20260620_t05_label_pilot_lmin1p0/summary.json`
