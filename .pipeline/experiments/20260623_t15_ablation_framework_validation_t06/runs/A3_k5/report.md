# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 30
- record_count: 60
- methods: vanilla_ha, f_n3p_knn
- method_exception_total: 0
- queries_per_bucket_config: 10
- seed_count_config: 2
- human_review_satisfied: True
- profile_bucket_satisfied: True

## 预检

- blocking_issues: none
- WARNING: T14 formal scale is not satisfied: queries_per_bucket=10, seed_count=2

## Contract 判定边界

- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。
- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。

## 输出文件

- preflight_json: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/preflight.json`
- queries_csv: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/queries.csv`
- records_csv: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/records.csv`
- run_config_json: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/run_config.json`
- summary_csv: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/summary_by_method_bucket.csv`
- summary_json: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/summary.json`
- verdict_json: `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/runs/A3_k5/verdict.json`
