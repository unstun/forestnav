---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
task: T09
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: 332db6eb6d5b1ad4d4c5530d5b9c20e9f0b9a18f
execution_host: MacBook-Pro.local
---

# T09 KNN 在线推理验收报告

## 结论

- 验收: `pass`
- 可行无碰撞路径: 5 / 5
- 验收阈值: >= 4 / 5
- F1/F2/F3 触发计数: 16 / 3 / 0

参数说明：本次继承 T08 数据集，T05 的 `L_min=1.0m` 与 T06 难度切点仍为 `reviewed:false`；因此本报告证明 T09 工程闭环可运行，不代表论文参数最终冻结。

## KNN 库

- 目录: `2_experiment/forest_n3p/models/t09_knn_library`
- 模型: `KNN-KDTree`
- 特征形状: `[100531, 41]`
- 标签形状: `[100531, 3]`
- scikit-learn: `1.9.0`

## 查询明细

| case | bucket | distance_bin | feasible | termination | F1 | F2 | F3 | time(s) | expansions | figure |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 0 | Easy | d08_12 | yes | `f2_limited_goal` | 4 | 1 | 0 | 0.236 | 245 | `.pipeline/experiments/20260620_t09_inference_verification/case_00.png` |
| 1 | Easy | d12_16 | yes | `direct_rs_goal` | 0 | 0 | 0 | 0.000 | 0 | `.pipeline/experiments/20260620_t09_inference_verification/case_01.png` |
| 2 | Complex | d16_20 | yes | `direct_rs_goal` | 4 | 1 | 0 | 0.154 | 82 | `.pipeline/experiments/20260620_t09_inference_verification/case_02.png` |
| 3 | Complex | d20_inf | yes | `direct_rs_goal` | 2 | 0 | 0 | 0.340 | 3 | `.pipeline/experiments/20260620_t09_inference_verification/case_03.png` |
| 4 | Extreme | d08_12 | yes | `direct_rs_goal` | 6 | 1 | 0 | 0.555 | 14 | `.pipeline/experiments/20260620_t09_inference_verification/case_04.png` |

## 产物

- 明细 CSV: `.pipeline/experiments/20260620_t09_inference_verification/records.csv`
- 摘要 JSON: `.pipeline/experiments/20260620_t09_inference_verification/summary.json`
- 单查询 JSON/PNG: `.pipeline/experiments/20260620_t09_inference_verification`
