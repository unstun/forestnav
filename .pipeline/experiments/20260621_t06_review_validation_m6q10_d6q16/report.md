---
date: 2026-06-20
status: needs_review
origin: ai+experiment
reviewed: false
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: dc6a9d1cbd37caebfeac598d584c663e40c35907
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
maps_per_density=6
queries_per_map=10
distance_map_count=6
queries_per_distance_bin=16
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
| d00:trees=40,gap=1.35m | Easy | 40 | 4.444 | 1.824 | 60 | 85.0% | 15.0% | 0.169 | 2.501 | 25.000 | 3430.600 |
| d01:trees=55,gap=1.25m | Easy | 55 | 6.111 | 1.689 | 60 | 90.0% | 10.0% | 0.212 | 2.500 | 94.000 | 3364.200 |
| d02:trees=70,gap=1.15m | Complex | 70 | 7.778 | 1.554 | 60 | 86.7% | 13.3% | 0.182 | 2.501 | 45.000 | 3914.600 |
| d03:trees=85,gap=1.05m | Complex | 85 | 9.444 | 1.419 | 60 | 76.7% | 23.3% | 0.358 | 2.500 | 342.500 | 3982.350 |
| d04:trees=100,gap=0.95m | Complex | 100 | 11.111 | 1.284 | 60 | 75.0% | 23.3% | 0.449 | 2.502 | 463.000 | 3986.400 |
| d05:trees=115,gap=0.90m | Extreme | 115 | 12.778 | 1.216 | 60 | 61.7% | 38.3% | 1.183 | 2.502 | 1566.500 | 5173.750 |
| d06:trees=130,gap=0.85m | Extreme | 130 | 14.444 | 1.149 | 60 | 68.3% | 31.7% | 0.628 | 2.501 | 662.000 | 4817.450 |
| d07:trees=145,gap=0.80m | Extreme | 145 | 16.111 | 1.081 | 60 | 55.0% | 45.0% | 2.192 | 2.501 | 2666.000 | 5788.350 |

## 距离轴结果

| 距离桶 | 桶 | 树数 | 约树密度(/100m²) | gap/车宽 | 查询 | 成功率 | 超时率 | 中位时间(s) | P95时间(s) | 中位扩展 | P95扩展 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [4.0,8.0)m | Easy | 90 | 10.000 | 1.351 | 96 | 99.0% | 1.0% | 0.144 | 1.225 | 1.000 | 1233.250 |
| [8.0,12.0)m | Easy | 90 | 10.000 | 1.351 | 96 | 99.0% | 1.0% | 0.195 | 1.428 | 79.000 | 1772.500 |
| [12.0,16.0)m | Complex | 90 | 10.000 | 1.351 | 96 | 87.5% | 12.5% | 0.319 | 2.500 | 301.000 | 3367.750 |
| [16.0,20.0)m | Complex | 90 | 10.000 | 1.351 | 96 | 78.1% | 21.9% | 0.344 | 2.501 | 348.000 | 3917.750 |
| 20.0m+ | Extreme | 90 | 10.000 | 1.351 | 96 | 64.6% | 35.4% | 0.439 | 2.502 | 562.500 | 4928.750 |

## 切点草案

### 密度轴

- 区分度结论：需复核。
- Easy 上界：d01:trees=55,gap=1.25m (成功率=90.0%, 中位时间=0.212s, 中位扩展=94.000)。
- Complex 范围：d02:trees=70,gap=1.15m (成功率=86.7%, 中位时间=0.182s, 中位扩展=45.000) 到 d04:trees=100,gap=0.95m (成功率=75.0%, 中位时间=0.449s, 中位扩展=463.000)。
- Extreme 下界：d05:trees=115,gap=0.90m (成功率=61.7%, 中位时间=1.183s, 中位扩展=1566.500)。
- 分桶数量：{"Easy": 2, "Complex": 3, "Extreme": 3, "NoData": 0}。

### 距离轴

- 区分度结论：通过。
- Easy 上界：[8.0,12.0)m (成功率=99.0%, 中位时间=0.195s, 中位扩展=79.000)。
- Complex 范围：[12.0,16.0)m (成功率=87.5%, 中位时间=0.319s, 中位扩展=301.000) 到 [16.0,20.0)m (成功率=78.1%, 中位时间=0.344s, 中位扩展=348.000)。
- Extreme 下界：20.0m+ (成功率=64.6%, 中位时间=0.439s, 中位扩展=562.500)。
- 分桶数量：{"Easy": 2, "Complex": 2, "Extreme": 1, "NoData": 0}。

## 验收判断

- 密度轴三桶区分度：需复核。
- 距离轴三桶区分度：通过。
- 本报告给出预注册补充草案；由于父 Contract 已 approved，本次不直接改写父 Contract。

## 产物

- `maps.csv`: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/maps.csv`
- `queries.csv`: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/queries.csv`
- `density_summary.csv`: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/density_summary.csv`
- `distance_summary.csv`: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/distance_summary.csv`
- `summary.json`: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/summary.json`
- `contract_supplement.md`: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/contract_supplement.md`
