---
date: 2026-06-20
status: pass
origin: ai+unit
reviewed: false
task: T13
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: d1f0a5566861af32b9376e7b8e953ce4a06a82c0+dirty
execution_host: MacBook-Pro.local
---

# T13 Evaluation Framework 验证报告

## 结论

- 合成评测记录数: 8
- 已生成 per-query CSV、按 method/bucket 汇总 CSV 与 JSON summary
- Wilcoxon paired query 数: 4, p=0.125
- Bootstrap SR diff: 0.25, CI=[0.0, 0.75]

说明：本报告只验证 T13 评测框架的指标、分组输出和统计检验能落盘；不替代 T14 主评测。T06 难度切点仍为 reviewed:false。

## 产物

- records_csv: `.pipeline/experiments/20260620_t13_evaluation_framework_verification/records.csv`
- summary_csv: `.pipeline/experiments/20260620_t13_evaluation_framework_verification/summary_by_method_bucket.csv`
- summary_json: `.pipeline/experiments/20260620_t13_evaluation_framework_verification/summary.json`
- verification_summary: `.pipeline/experiments/20260620_t13_evaluation_framework_verification/verification_summary.json`
