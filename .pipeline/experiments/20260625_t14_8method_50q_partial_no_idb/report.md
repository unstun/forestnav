# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 150
- record_count: 1200
- methods: f_n3p_knn, vanilla_ha, n3p_k1, voronoi_waypoint, bottleneck_waypoint, improved_ha, lo_ha, ss_rrt
- method_exception_total: 0
- queries_per_bucket_config: 50
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

- preflight_json: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/preflight.json`
- queries_csv: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/queries.csv`
- records_csv: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/records.csv`
- run_config_json: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/run_config.json`
- summary_csv: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/summary_by_method_bucket.csv`
- summary_json: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/summary.json`
- verdict_json: `/home/ubuntu/ForestNav/.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb/verdict.json`
