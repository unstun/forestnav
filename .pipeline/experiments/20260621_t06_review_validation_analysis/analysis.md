---
origin: ai+local+remote
reviewed: false
created_at_utc: 2026-06-21T02:09:36+00:00
task: T14
scope: T06 validation for T14 formal gate
---

# T06 Review Validation Analysis for T14

## 直观结论

这次放大验证不是在补一个小瑕疵，而是发现 T14 正式验收前的 T06 密度轴定义还不稳。距离轴保持稳定；密度轴从原报告的“通过”变成“需复核”，Extreme 下界从 `d03` 后移到 `d05`，并且 `bucket_separation_pass=false`。

因此，T14 现在不应继续硬跑成正式验收。当前正确状态是：保留 k=20 collisionguard 全量结果作为强候选证据，但在 Dr Sun 对 T06 切点做人工确认、修订或追加验证前，不标记 T14 完成。

## 输入证据

| 项 | 原 T06 | 放大验证 |
|---|---|---|
| 目录 | `.pipeline/experiments/20260620_t06_difficulty_calibration` | `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16` |
| density queries | 120 | 480 |
| distance queries | 90 | 480 |
| total queries | 210 | 960 |
| source_head | `37d3a262b9414a20c38b3ddd016a153c73406332+uncommitted-t06-rsync` | `dc6a9d1cbd37caebfeac598d584c663e40c35907` |
| execution_host | `ubuntu-OMEN-by-HP-Laptop-17-ck1xxx` | `ubuntu-OMEN-by-HP-Laptop-17-ck1xxx` |

## 切点变化

| 轴 | 原状态 | 验证状态 | 原 Easy 上界 | 验证 Easy 上界 | 原 Complex | 验证 Complex | 原 Extreme 下界 | 验证 Extreme 下界 |
|---|---|---|---|---|---|---|---|---|
| density | pass | fail | `d01` | `d01` | `d02`-`d02` | `d02`-`d04` | `d03` | `d05` |
| distance | pass | pass | `d08_12` | `d08_12` | `d12_16`-`d16_20` | `d12_16`-`d16_20` | `d20_inf` | `d20_inf` |

## 密度轴风险

放大验证后，密度轴的排序仍然满足切点顺序，但指标区分度失败：`order_pass=true`，`metric_pass=false`。这说明问题不是程序无法分桶，而是 Easy/Complex/Extreme 三桶之间的实测规划难度差异在当前随机森林生成与查询采样下不够稳。

关键变化：

- `d03` 从原 T06 的 Extreme 变成 Complex。
- `d04` 从原 T06 的 Extreme 变成 Complex。
- Extreme 下界从 `d03` 移到 `d05`。
- `d00` 在放大验证中超时率为 15.0%，高于 Easy 规则中的 10.0% 上限；但单调前缀规则仍将 `d00`/`d01` 作为 Easy 前缀处理。

## 距离轴判断

距离轴在放大验证中保持稳定：Easy 上界仍是 `[8.0,12.0)m`，Complex 仍是 `[12.0,16.0)m` 到 `[16.0,20.0)m`，Extreme 仍是 `20.0m+`。这支持距离轴可进入人工审查，但不能单独解除 T06 整体 reviewed:false 的门槛。

## 对 T14 的影响

| 门槛 | 当前判断 | 原因 |
|---|---|---|
| T06 supplement reviewed | not ready | 原 supplement 仍为 reviewed:false，且放大验证推翻了密度轴的原通过结论。 |
| T14 formal acceptance rerun | hold | 正式主评测依赖已接受的难度桶定义；密度桶未定前，继续长跑会制造不可正式引用的结果。 |
| k=20 collisionguard fullscale | candidate evidence only | 该 run 的核心指标通过，但它不是基于人工确认后的 T06 正式切点。 |
| 是否勾选 T14 | no | 主线 T14 明确需人工确认；目前缺 T06 人工确认和 formal_acceptance=true rerun。 |

## 建议给 Dr Sun 的确认项

1. 接受原 T06 小样本切点作为正式桶定义，并记录为什么放大验证不改变该决策。
2. 按放大验证修订 T06 supplement：密度 Easy=`d00-d01`，Complex=`d02-d04`，Extreme=`d05-d07`，然后重新跑 T14 正式评测。
3. 再跑更大规模或更严格种子覆盖的 T06 确认实验，先不修订 supplement。

当前最保守、最适合写论文的做法是第 2 或第 3 项；第 1 项需要非常强的人工理由，否则审稿时容易被质疑难度桶是小样本偶然结果。

## 产物索引

- `cutpoint_delta.csv`: 原 T06 与放大验证的切点变化。
- `density_level_comparison.csv`: 密度轴逐级指标对照。
- `distance_level_comparison.csv`: 距离轴逐级指标对照。
- `formal_gate_implications.csv`: 对 T14 正式门槛的影响表。
- `manifest.json`: 输入、输出和关键结论清单。
