---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: 37d3a262b9414a20c38b3ddd016a153c73406332+uncommitted-t06-rsync
execution_host: ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
---

# T06 难度轴标定报告

## 目的

用原版 Hybrid A* 在程序化森林中标定 Easy/Complex/Extreme 难度桶。密度轴至少覆盖 8 个级别；距离轴在中等密度参考森林中单独改变起终欧氏距离。统计口径为规划器实测时间、节点扩展数、成功率和超时率。

## 实验设置

```text
seed=20260620
map_size_cells=300x300
resolution_m=0.1
maps_per_density=3
queries_per_map=5
distance_map_count=3
queries_per_distance_bin=6
teacher_timeout_s=2.5
teacher_max_nodes=15000
easy_success_rate_min=0.85
easy_median_time_s_max=0.5
easy_timeout_rate_max=0.1
extreme_success_rate_max=0.7
extreme_timeout_rate_min=0.3
extreme_success_rate_hard_max=0.6
extreme_timeout_rate_hard_min=0.5
```

分桶采用轴向单调切点，而不是逐级独立标签：先用固定规则寻找 Easy 前缀上界和 Extreme 后缀下界，然后将两者之间的级别归为 Complex。这样可以降低有限随机查询造成的非单调噪声，但所有原始级别统计仍完整保留在表格和 CSV 中。

## 密度轴结果

| 级别 | 桶 | 树数 | 约树密度(/100m²) | gap/车宽 | 查询 | 成功率 | 超时率 | 中位时间(s) | P95时间(s) | 中位扩展 | P95扩展 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d00:trees=40,gap=1.35m | Easy | 40 | 4.444 | 1.824 | 15 | 86.7% | 13.3% | 0.174 | 2.501 | 57.000 | 3735.600 |
| d01:trees=55,gap=1.25m | Easy | 55 | 6.111 | 1.689 | 15 | 100.0% | 0.0% | 0.180 | 1.262 | 64.000 | 1699.600 |
| d02:trees=70,gap=1.15m | Complex | 70 | 7.778 | 1.554 | 15 | 80.0% | 20.0% | 0.163 | 2.501 | 33.000 | 4137.800 |
| d03:trees=85,gap=1.05m | Extreme | 85 | 9.444 | 1.419 | 15 | 66.7% | 33.3% | 0.394 | 2.502 | 427.000 | 4781.800 |
| d04:trees=100,gap=0.95m | Extreme | 100 | 11.111 | 1.284 | 15 | 60.0% | 33.3% | 0.775 | 2.501 | 1031.000 | 4209.600 |
| d05:trees=115,gap=0.90m | Extreme | 115 | 12.778 | 1.216 | 15 | 46.7% | 53.3% | 2.500 | 2.502 | 3425.000 | 4128.100 |
| d06:trees=130,gap=0.85m | Extreme | 130 | 14.444 | 1.149 | 15 | 73.3% | 26.7% | 0.624 | 2.501 | 575.000 | 4924.400 |
| d07:trees=145,gap=0.80m | Extreme | 145 | 16.111 | 1.081 | 15 | 46.7% | 53.3% | 2.500 | 2.501 | 3283.000 | 5919.400 |

## 距离轴结果

| 距离桶 | 桶 | 树数 | 约树密度(/100m²) | gap/车宽 | 查询 | 成功率 | 超时率 | 中位时间(s) | P95时间(s) | 中位扩展 | P95扩展 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [4.0,8.0)m | Easy | 90 | 10.000 | 1.351 | 18 | 100.0% | 0.0% | 0.144 | 0.400 | 1.000 | 353.500 |
| [8.0,12.0)m | Easy | 90 | 10.000 | 1.351 | 18 | 100.0% | 0.0% | 0.334 | 1.508 | 294.500 | 1528.250 |
| [12.0,16.0)m | Complex | 90 | 10.000 | 1.351 | 18 | 88.9% | 11.1% | 0.310 | 2.500 | 283.000 | 2749.250 |
| [16.0,20.0)m | Complex | 90 | 10.000 | 1.351 | 18 | 77.8% | 22.2% | 0.252 | 2.500 | 208.500 | 3818.350 |
| 20.0m+ | Extreme | 90 | 10.000 | 1.351 | 18 | 66.7% | 33.3% | 0.488 | 2.502 | 616.000 | 5019.700 |

## 切点草案

### 密度轴

- 区分度结论：通过。
- Easy 上界：d01:trees=55,gap=1.25m (成功率=100.0%, 中位时间=0.180s, 中位扩展=64.000)。
- Complex 范围：d02:trees=70,gap=1.15m (成功率=80.0%, 中位时间=0.163s, 中位扩展=33.000) 到 d02:trees=70,gap=1.15m (成功率=80.0%, 中位时间=0.163s, 中位扩展=33.000)。
- Extreme 下界：d03:trees=85,gap=1.05m (成功率=66.7%, 中位时间=0.394s, 中位扩展=427.000)。
- 分桶数量：{"Easy": 2, "Complex": 1, "Extreme": 5, "NoData": 0}。

### 距离轴

- 区分度结论：通过。
- Easy 上界：[8.0,12.0)m (成功率=100.0%, 中位时间=0.334s, 中位扩展=294.500)。
- Complex 范围：[12.0,16.0)m (成功率=88.9%, 中位时间=0.310s, 中位扩展=283.000) 到 [16.0,20.0)m (成功率=77.8%, 中位时间=0.252s, 中位扩展=208.500)。
- Extreme 下界：20.0m+ (成功率=66.7%, 中位时间=0.488s, 中位扩展=616.000)。
- 分桶数量：{"Easy": 2, "Complex": 2, "Extreme": 1, "NoData": 0}。

## 验收判断

- 密度轴三桶区分度：通过。
- 距离轴三桶区分度：通过。
- 本报告给出预注册补充草案；由于父 Contract 已 approved，本次不直接改写父 Contract。

## 产物

- `maps.csv`: `.pipeline/experiments/20260620_t06_difficulty_calibration/maps.csv`
- `queries.csv`: `.pipeline/experiments/20260620_t06_difficulty_calibration/queries.csv`
- `density_summary.csv`: `.pipeline/experiments/20260620_t06_difficulty_calibration/density_summary.csv`
- `distance_summary.csv`: `.pipeline/experiments/20260620_t06_difficulty_calibration/distance_summary.csv`
- `summary.json`: `.pipeline/experiments/20260620_t06_difficulty_calibration/summary.json`
- `contract_supplement.md`: `.pipeline/experiments/20260620_t06_difficulty_calibration/contract_supplement.md`
- 预注册补充草案: `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md`
