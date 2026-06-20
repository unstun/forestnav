---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
task: T10
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: eb203584b6bc7f53aacad29ae063f05283733906+dirty
execution_host: MacBook-Pro.local
---

# F-N3P MLP 在线推理验收报告

## 结论

- 验收: `pass`
- 可行无碰撞路径: 5 / 5
- 验收阈值: >= 4 / 5
- F1/F2/F3 触发计数: 0 / 6 / 0

参数说明：本次继承 T08 数据集，T05 的 `L_min=1.0m` 与 T06 难度切点仍为 `reviewed:false`；因此本报告证明 `mlp` predictor 已接入在线推理循环，不代表论文参数最终冻结。

## 预测器

- predictor: `mlp`
- 目录: `2_experiment/forest_n3p/models/t10_mlp_subgoal`
- 模型: `MLP`
- 特征形状: `[100531, 41]`
- 标签形状: `[100531, 3]`
- scikit-learn: `N/A`
- torch: `2.12.1+cu130`

## 查询明细

| case | bucket | distance_bin | feasible | termination | F1 | F2 | F3 | time(s) | expansions | figure |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 0 | Easy | d08_12 | yes | `f2_limited_goal` | 0 | 1 | 0 | 1.231 | 1738 | `.pipeline/experiments/20260620_t10_mlp_inference_verification/case_00.png` |
| 1 | Easy | d12_16 | yes | `direct_rs_goal` | 0 | 0 | 0 | 0.000 | 0 | `.pipeline/experiments/20260620_t10_mlp_inference_verification/case_01.png` |
| 2 | Complex | d16_20 | yes | `direct_rs_goal` | 0 | 1 | 0 | 0.149 | 70 | `.pipeline/experiments/20260620_t10_mlp_inference_verification/case_02.png` |
| 3 | Complex | d20_inf | yes | `f2_limited_goal` | 0 | 3 | 0 | 0.674 | 542 | `.pipeline/experiments/20260620_t10_mlp_inference_verification/case_03.png` |
| 4 | Extreme | d08_12 | yes | `f2_limited_goal` | 0 | 1 | 0 | 0.300 | 178 | `.pipeline/experiments/20260620_t10_mlp_inference_verification/case_04.png` |

## 产物

- 明细 CSV: `.pipeline/experiments/20260620_t10_mlp_inference_verification/records.csv`
- 摘要 JSON: `.pipeline/experiments/20260620_t10_mlp_inference_verification/summary.json`
- 单查询 JSON/PNG: `.pipeline/experiments/20260620_t10_mlp_inference_verification`
