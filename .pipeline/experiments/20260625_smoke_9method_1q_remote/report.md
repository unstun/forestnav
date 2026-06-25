# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 3
- record_count: 27
- methods: f_n3p_knn, vanilla_ha, n3p_k1, voronoi_waypoint, bottleneck_waypoint, improved_ha, lo_ha, ss_rrt, idb_rrt
- method_exception_total: 0
- queries_per_bucket_config: 1
- seed_count_config: 5
- human_review_satisfied: True
- profile_bucket_satisfied: True

## 预检

- blocking_issues: none
- WARNING: T14 formal scale is not satisfied: queries_per_bucket=1, seed_count=5

## Contract 判定边界

- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。
- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。

## 输出文件

- preflight_json: `.pipeline/experiments/20260625_smoke_9method_1q_remote/preflight.json`
- queries_csv: `.pipeline/experiments/20260625_smoke_9method_1q_remote/queries.csv`
- records_csv: `.pipeline/experiments/20260625_smoke_9method_1q_remote/records.csv`
- run_config_json: `.pipeline/experiments/20260625_smoke_9method_1q_remote/run_config.json`
- summary_csv: `.pipeline/experiments/20260625_smoke_9method_1q_remote/summary_by_method_bucket.csv`
- summary_json: `.pipeline/experiments/20260625_smoke_9method_1q_remote/summary.json`
- verdict_json: `.pipeline/experiments/20260625_smoke_9method_1q_remote/verdict.json`
