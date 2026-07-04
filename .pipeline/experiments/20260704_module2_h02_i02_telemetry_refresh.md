---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
depends_on:
  - .pipeline/experiments/20260704_module2_a02_3_telemetry_implementation.md
  - .pipeline/experiments/20260704_module2_h02_local_smoke_preflight.md
  - .pipeline/experiments/20260704_module2_i02_paper_table_protocol.md
---

# H02/I02 Telemetry Refresh After A02.3

## 直观结论

A02.3 P0 telemetry 不是只停在代码层。本轮重跑 H02.1 available-subset local smoke, 并刷新 I02 paper table artifact, 证明新 telemetry columns 已进入 `records.csv`, `summary_by_method_bucket.csv` 和 paper-table preview。

这仍然不是 formal result: H02 full all-method smoke 和 H02.2 formal remote run 仍被 F02.6 pending 与缺 PPO checkpoint 阻塞。

## 产物

- H02 refreshed smoke: `0_trials/module2_h02_local_smoke/h02_1_available_subset/`
- I02 refreshed tables: `0_trials/module2_paper_tables/module2_paper_tables.json`, `0_trials/module2_paper_tables/module2_paper_tables.md`
- Builder: `2_experiment/forest_n3p/scripts/build_module2_paper_tables.py`
- Test: `2_experiment/forest_n3p/tests/test_module2_paper_tables.py`

## 关键观察

- `records.csv` now includes: `rl_attempts`, `rl_successes`, `rs_attempts`, `nn_forward_time_s`, `fallback_to_primitives_count`, `rollout_protocol`, `collision_checker`。
- `summary_by_method_bucket.csv` now includes: `mean_nn_forward_time_s`, `p95_nn_forward_time_s`, `rl_attempts_total`, `rl_successes_total`, `rs_attempts_total`, `fallback_to_primitives_total`。
- I02 artifact now includes `telemetry_diagnostic_table`, separate from the Contract main table.
- In the 3-query BC analytic smoke, `bc_analytic_operator` shows `rl_attempts_total=126`, `rl_successes_total=3`, `rs_attempts_total=527`, `fallback_to_primitives_total=123`, `rollout_protocol=constant_steer_grid_footprint_terminal_rs`, `collision_checker=GridFootprintChecker`。

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py` failed with `KeyError: 'telemetry_diagnostic_table'` before builder implementation.
- GREEN: same test -> `1 passed in 0.08s`。
- Targeted regression: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py` -> `9 passed in 1.10s`。
- H02 refresh command: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation --output-dir 0_trials/module2_h02_local_smoke/h02_1_available_subset --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator --queries-per-bucket 1 --seed-count 1 --queries-per-map 1 --density-profile-buckets validation_t06 --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md --allow-unresolved-human-review --no-enforce-t14-scale --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt` -> `record_count=15`, `query_count=3`, `status=candidate_or_smoke`, `formal_acceptance=false`。
- Full regression: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `112 passed in 12.15s`。

## 边界

- 未本地训练。
- 未远端训练。
- 未批准 F02.6。
- 未生成 PPO checkpoint。
- `telemetry_diagnostic_table` 是 preview/schema proof, 不能作为 formal performance table。
