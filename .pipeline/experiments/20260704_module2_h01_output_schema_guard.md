---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
depends_on:
  - .pipeline/experiments/20260704_module2_a02_3_telemetry_implementation.md
  - .pipeline/experiments/20260704_module2_h02_i02_telemetry_refresh.md
  - .pipeline/experiments/20260704_module2_h01_f02_6_decision_packet_guard.md
---

# H01 Formal Output Schema Guard

## 直观结论

H01 manifest 现在不只列 methods 和 metrics, 还冻结 formal output schema。后续 H02 formal run 如果缺 A02.3 telemetry columns, 就不能被当成合格 formal output。

这仍然不解除 F02.6 pending, 不生成 PPO checkpoint, 不支持 formal performance claim。

## 实现内容

- `build_module2_evaluation_manifest.py` 新增 `required_output_schema`。
- `records_csv_required_columns` 包含 Contract 主指标、analytic telemetry、checkpoint provenance 和 A02.3 telemetry: `rl_attempts`, `rl_successes`, `rs_attempts`, `nn_forward_time_s`, `fallback_to_primitives_count`, `rollout_protocol`, `collision_checker`。
- `summary_by_method_bucket_required_columns` 包含 `mean_nn_forward_time_s`, `p95_nn_forward_time_s`, `rl_attempts_total`, `rl_successes_total`, `rs_attempts_total`, `fallback_to_primitives_total`。
- `summary_json_required_sections` 冻结 paired tests 与 bootstrap CI sections。
- Rebuilt `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json` and `.md`; status remains `blocked_pending_decisions`。

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` failed on missing `required_output_schema` before implementation.
- GREEN: same test -> `5 passed in 0.31s`。
- Schema audit: generated H01 manifest has `records_csv_required_columns=36`, `summary_by_method_bucket_required_columns=24`, required summary JSON sections include paired time/expansion tests and timeout bootstrap CI。
- Targeted regression: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py` -> `14 passed in 1.24s`。
- Full regression: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `112 passed in 11.98s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py` passed.

## 边界

- 未本地训练。
- 未远端训练。
- 未批准 F02.6。
- 未生成 PPO checkpoint。
- H01 remains blocked by F02.6 pending and missing PPO checkpoint.
