# T14 主评测运行报告

- status: candidate_or_smoke
- formal_acceptance: False
- query_count: 3
- record_count: 15
- methods: f_n3p_knn, vanilla_ha, n3p_k1, voronoi_waypoint, bottleneck_waypoint
- method_exception_total: 0
- queries_per_bucket_config: 1
- seed_count_config: 1

## 预检

- blocking_issues: none
- WARNING: T06 cutpoint supplement is not reviewed:true: .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md
- WARNING: md_dqn skipped: md_dqn_source_dir is not set and FORESTNAV_MD_DQN_SOURCE_DIR is not defined; expected a DQN10 2_experiment directory containing ugv_dqn
- WARNING: T14 formal scale is not satisfied: queries_per_bucket=1, seed_count=1

## Contract 判定边界

- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。
- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。

## 输出文件

- preflight_json: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/preflight.json`
- queries_csv: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/queries.csv`
- records_csv: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/records.csv`
- run_config_json: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/run_config.json`
- summary_csv: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/summary_by_method_bucket.csv`
- summary_json: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/summary.json`
- verdict_json: `.pipeline/experiments/20260620_t14_md_dqn_adapter_smoke/verdict.json`
