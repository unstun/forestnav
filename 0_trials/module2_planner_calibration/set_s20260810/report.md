# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 300
- record_count: 900
- methods: ha_single_rs, ha_dang_multi_rs, ha_rl_rs_ppo
- method_exception_total: 0
- queries_per_bucket_config: 100
- seed_count_config: 5
- human_review_satisfied: True
- profile_bucket_satisfied: True

## 预检

- blocking_issues: none
- warnings: none

## Contract 判定边界

- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。
- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。

## 输出文件

- preflight_json: `0_trials/module2_planner_calibration/set_s20260810/preflight.json`
- queries_csv: `0_trials/module2_planner_calibration/set_s20260810/queries.csv`
- records_csv: `0_trials/module2_planner_calibration/set_s20260810/records.csv`
- run_config_json: `0_trials/module2_planner_calibration/set_s20260810/run_config.json`
- summary_csv: `0_trials/module2_planner_calibration/set_s20260810/summary_by_method_bucket.csv`
- summary_json: `0_trials/module2_planner_calibration/set_s20260810/summary.json`
- verdict_json: `0_trials/module2_planner_calibration/set_s20260810/verdict.json`
