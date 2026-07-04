---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_h01_metric_protocol.md
  - .pipeline/experiments/20260704_module2_h02_local_smoke_preflight.md
---

# H02.3 Statistical CI Infrastructure

## 直观结论

H02.3 的正式统计分析还不能做, 因为 H02.2 远端完整 all-method run 还没有正式数据。但统计基础设施现在补齐了一个关键缺口: 不只支持 success-rate bootstrap, 也支持 failure-rate 和 timeout-failure-rate bootstrap CI。

同时, main evaluation 的 `_stat_pairs()` 现在会为 module2 operator 相对 Dang multi-RS 生成配对统计项, 避免后续 summary 只比较旧 F-N3P 方法。

## 代码改动

- 新增 `BootstrapRateCIResult`。
- 新增 `bootstrap_failure_rate_difference()`。
- 新增 `bootstrap_timeout_failure_rate_difference()`。
- `write_evaluation_outputs()` 新增:
  - `failure_rate_bootstrap_ci`
  - `timeout_failure_rate_bootstrap_ci`
- `run_main_evaluation()` 现在同时输出 success/failure/timeout 三类 paired bootstrap CI。
- `_stat_pairs()` 现在包含:
  - `bc_analytic_operator` vs `ha_dang_multi_rs`
  - `ppo_analytic_operator` vs `ha_dang_multi_rs`
  - `ha_rl_rs_ppo` vs `ha_dang_multi_rs`
- `build_module2_metric_protocol.py` 已更新 metric protocol, 将 `timeout_failure_rate` 的统计函数锚定为 `forest_n3p.evaluation.bootstrap_timeout_failure_rate_difference`, 并新增 diagnostic `failure_rate`。

## H02.1 Available Subset 验证

重跑 `0_trials/module2_h02_local_smoke/h02_1_available_subset/`:

- Record count: `15`
- Query count: `3`
- Status: `candidate_or_smoke`
- Formal acceptance: `false`
- Collision violation total: `0`
- Method exception total: `0`
- Paired time tests: includes `bc_analytic_operator` vs `ha_dang_multi_rs`
- Paired expansion tests: includes `bc_analytic_operator` vs `ha_dang_multi_rs`
- Bootstrap CI slots: `success_rate_bootstrap_ci`, `failure_rate_bootstrap_ci`, `timeout_failure_rate_bootstrap_ci`

当前 subset 中没有 PPO 方法, 因此不会产生 PPO pair; 这是预期边界。

## 验证

- RED timeout CI: `test_bootstrap_timeout_failure_rate_difference_uses_paired_timeout_indicators` 先失败于缺少 `bootstrap_timeout_failure_rate_difference`。
- RED module2 pair: `test_stat_pairs_include_module2_operator_against_dang_rs_baseline` 先失败于 `_stat_pairs()` 为空。
- GREEN targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py::test_stat_pairs_include_module2_operator_against_dang_rs_baseline 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py::test_bootstrap_timeout_failure_rate_difference_uses_paired_timeout_indicators` -> `2 passed`。
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py 2_experiment/forest_n3p/tests/test_module2_metric_protocol.py 2_experiment/forest_n3p/tests/test_module2_h02_smoke_preflight.py` -> `10 passed`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/evaluation.py 2_experiment/forest_n3p/main_evaluation.py 2_experiment/forest_n3p/scripts/build_module2_metric_protocol.py`。

## 边界

- H02.3 formal analysis 仍未完成。
- 本记录不声称任何方法优劣。
- H02.2 远端完整运行和 F02.6 决策仍是正式统计前置条件。
- PPO formal training/checkpoint 仍必须在 `gpu3070ti-relay` 执行, 禁止本地训练补洞。
