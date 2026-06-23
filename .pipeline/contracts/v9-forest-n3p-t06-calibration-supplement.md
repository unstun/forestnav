---
origin: ai+experiment
reviewed: true
date: 2026-06-23
status: reviewed-for-framework
parent_contract: .pipeline/contracts/v9-forest-n3p.md
source_report: .pipeline/experiments/20260620_t06_difficulty_calibration/report.md
validation_report: .pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/report.md
validation_analysis: .pipeline/experiments/20260621_t06_review_validation_analysis/analysis.md
source_head: dc6a9d1cbd37caebfeac598d584c663e40c35907
execution_host: ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
---

# T06 难度轴预注册补充

本文件是 T06 标定产物，不修改已 approved 的父 Contract。2026-06-23 Dr Sun 确认先按放大验证切点推进整体实验框架；最终论文写作前如需更强难度论证，可追加更大规模复核。

## 固定判定规则

```json
{
  "easy_success_rate_min": 0.85,
  "easy_median_time_s_max": 0.5,
  "easy_timeout_rate_max": 0.1,
  "extreme_success_rate_max": 0.7,
  "extreme_timeout_rate_min": 0.3,
  "extreme_success_rate_hard_max": 0.6,
  "extreme_timeout_rate_hard_min": 0.5,
  "min_success_rate_gap_easy_to_extreme": 0.2,
  "min_complex_to_easy_time_ratio": 1.5,
  "min_extreme_to_easy_time_ratio": 2.0,
  "min_complex_to_easy_p95_time_ratio": 1.5,
  "min_extreme_to_easy_p95_time_ratio": 2.0,
  "min_complex_to_easy_p95_expansion_ratio": 1.5,
  "min_extreme_to_easy_expansion_ratio": 2.0,
  "min_timeout_rate_gap_easy_to_complex": 0.1
}
```

这些规则用于寻找轴向单调切点：低于 Easy 上界的级别归入 Easy，高于 Extreme 下界的级别归入 Extreme，中间归入 Complex。单个级别的偶发 timeout 不会单独推翻其所在前缀/后缀，但所有原始统计必须随报告保留。

## 密度轴切点草案

- 区分度结论：按放大验证切点先作为框架桶依据；密度轴仍保留“论文前可追加验证”的限制说明。
- Easy 上界：d01:trees=55,gap=1.25m (成功率=90.0%, 中位时间=0.212s, 中位扩展=94.000)。
- Complex 范围：d02:trees=70,gap=1.15m (成功率=86.7%, 中位时间=0.182s, 中位扩展=45.000) 到 d04:trees=100,gap=0.95m (成功率=75.0%, 中位时间=0.449s, 中位扩展=463.000)。
- Extreme 下界：d05:trees=115,gap=0.90m (成功率=61.7%, 中位时间=1.183s, 中位扩展=1566.500)。
- 分桶数量：{"Easy": 2, "Complex": 3, "Extreme": 3, "NoData": 0}。

## 起终距离轴切点草案

- 区分度结论：通过。
- Easy 上界：[8.0,12.0)m (成功率=100.0%, 中位时间=0.334s, 中位扩展=294.500)。
- Complex 范围：[12.0,16.0)m (成功率=88.9%, 中位时间=0.310s, 中位扩展=283.000) 到 [16.0,20.0)m (成功率=77.8%, 中位时间=0.252s, 中位扩展=208.500)。
- Extreme 下界：20.0m+ (成功率=66.7%, 中位时间=0.488s, 中位扩展=616.000)。
- 分桶数量：{"Easy": 2, "Complex": 2, "Extreme": 1, "NoData": 0}。

## 使用限制

- 密度轴同时改变树干数量和目标树间隙，因此 `gap/车宽` 是伴随变量，不是独立单因子实验。
- 距离轴固定在中等密度参考森林中运行，用于隔离起终欧氏距离影响。
- 本轮确认的目的优先是打通 T14/T15/T16 与论文 Results 框架；若最终论文需要强声称“Extreme 难度”，应在写作前补充更大样本或真实地图上的难度复核。
