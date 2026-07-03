# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 9
- record_count: 18
- methods: vanilla_ha, f_n3p_knn
- method_exception_total: 0
- queries_per_bucket_config: 3
- seed_count_config: 1
- human_review_satisfied: True
- profile_bucket_satisfied: True

## 预检

- blocking_issues: none
- WARNING: T14 formal scale is not satisfied: queries_per_bucket=3, seed_count=1

## Contract 判定边界

- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。
- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。

## 输出文件

- preflight_json: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/preflight.json`
- queries_csv: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/queries.csv`
- records_csv: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/records.csv`
- run_config_json: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/run_config.json`
- summary_csv: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/summary_by_method_bucket.csv`
- summary_json: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/summary.json`
- verdict_json: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/verdict.json`
