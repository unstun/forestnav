# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 3
- record_count: 15
- methods: ha_no_analytic, ha_single_rs, ha_dang_multi_rs, mlp, bc_analytic_operator
- method_exception_total: 0
- queries_per_bucket_config: 1
- seed_count_config: 1
- human_review_satisfied: True
- profile_bucket_satisfied: True

## 预检

- blocking_issues: none
- WARNING: T14 formal scale is not satisfied: queries_per_bucket=1, seed_count=1

## Contract 判定边界

- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。
- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。

## 输出文件

- preflight_json: `0_trials/module2_h02_local_smoke/h02_1_available_subset/preflight.json`
- queries_csv: `0_trials/module2_h02_local_smoke/h02_1_available_subset/queries.csv`
- records_csv: `0_trials/module2_h02_local_smoke/h02_1_available_subset/records.csv`
- run_config_json: `0_trials/module2_h02_local_smoke/h02_1_available_subset/run_config.json`
- summary_csv: `0_trials/module2_h02_local_smoke/h02_1_available_subset/summary_by_method_bucket.csv`
- summary_json: `0_trials/module2_h02_local_smoke/h02_1_available_subset/summary.json`
- verdict_json: `0_trials/module2_h02_local_smoke/h02_1_available_subset/verdict.json`
