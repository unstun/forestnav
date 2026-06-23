# T16 泛化测试报告

## 人话结论

- 本次状态: candidate_or_framework；query_count=16，record_count=32。
- OOD 密度回答：训练分布外更稀/更密时，F-N3P 相对原版 HA* 的成功率跌幅是否超过 5pp。
- RealMap 回答：真实 SLAM 地图上，F-N3P 相对原版 HA* 的中位时间收益是否达到 20%。
- `candidate_or_framework` 表示框架和 CSV 已跑通，但规模还不是论文最终数字。

## Contract 判据

- 判据 ②：OOD density bucket success rate relative to original drops >5pp 记为失败。
- 判据 ④：real SLAM map time benefit <20% 记为失败。

## 当前判定

- criterion_2_pass: True
- criterion_4_pass: False
- collision_violation_total: 0
- method_exception_total: 0

## 输出文件

- preflight_json: `.pipeline/experiments/20260623_t16_generalization_framework_t06/preflight.json`
- queries_csv: `.pipeline/experiments/20260623_t16_generalization_framework_t06/queries.csv`
- records_csv: `.pipeline/experiments/20260623_t16_generalization_framework_t06/records.csv`
- run_config_json: `.pipeline/experiments/20260623_t16_generalization_framework_t06/run_config.json`
- summary_csv: `.pipeline/experiments/20260623_t16_generalization_framework_t06/summary_by_method_bucket.csv`
- summary_json: `.pipeline/experiments/20260623_t16_generalization_framework_t06/summary.json`
- verdict_json: `.pipeline/experiments/20260623_t16_generalization_framework_t06/verdict.json`

## 规模边界

- ood_queries_per_bucket_config: 5
- seed_count_config: 2
- realmap_queries_per_map_config: 3
- 论文最终数字建议按 `--ood-queries-per-bucket >=100 --seed-count >=5` 重跑。
