---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
---

# H01.2 Metric Protocol

## 直观结论

H01.2 已把论文主表和诊断表要用的指标冻结成机器可读协议, 并补上一个真实代码缺口: Contract 要求的 timeout failure rate 现在不再只靠后处理猜, `summary_by_method_bucket.csv` 会显式输出 `timeout_failure_count` 和 `timeout_failure_rate`。

这一步不跑 formal evaluation, 不训练 PPO, 也不解除 F02.6。

## 产物

- JSON: `0_trials/module2_metric_protocol/module2_metric_protocol.json`
- Markdown: `0_trials/module2_metric_protocol/module2_metric_protocol.md`
- 生成器: `2_experiment/forest_n3p/scripts/build_module2_metric_protocol.py`
- 测试: `2_experiment/forest_n3p/tests/test_module2_metric_protocol.py`

## 冻结指标

- `total_expansions`: Contract 主指标, 记录字段 `records.csv.total_expansions`, 聚合字段 `summary_by_method_bucket.median_expansions/p95_expansions`, 配对检验函数 `paired_wilcoxon_expansions()`。
- `total_time_s`: Contract 主指标, 记录字段 `records.csv.total_time_s`, 聚合字段 `summary_by_method_bucket.median_time_s/p95_time_s`, 配对检验函数 `paired_wilcoxon_time()`。
- `timeout_failure_rate`: Contract 主指标, 从 `records.csv.failure_reason` 中 lowercase 包含 `timeout` 的 row 派生, 聚合字段 `summary_by_method_bucket.timeout_failure_count/timeout_failure_rate`。
- `path_quality`: Contract 主指标, 包含 `path_inflation_ratio`, `mean_abs_curvature`, `min_clearance_m`。
- 诊断指标: `analytic_success_rate`, `terminal_rs_success_rate`, `nn_forward_time_s`。

## 代码改动

- `EvaluationRecord` 不变, 继续作为 `records.csv` 的字段真源。
- `GroupSummary` 新增 `timeout_failure_count` 和 `timeout_failure_rate`。
- `write_evaluation_outputs()` 新增 `paired_expansion_tests` 输出。
- `run_main_evaluation()` 现在同时计算 paired time tests 和 paired expansion tests。
- 新增 `PairedWilcoxonExpansionsResult` 与 `paired_wilcoxon_expansions()`。

## 验证

- RED timeout summary: `test_summary_exposes_timeout_failure_rate_for_contract_metric` 先失败于 `GroupSummary` 缺 `timeout_failure_count`。
- RED metric protocol: `test_module2_metric_protocol_freezes_contract_and_serialized_fields` 先失败于缺少 `build_module2_metric_protocol`。
- RED expansion Wilcoxon: `test_paired_wilcoxon_expansions_uses_paired_query_total_expansions` 先失败于缺少 `paired_wilcoxon_expansions`。
- GREEN targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py::test_summary_exposes_timeout_failure_rate_for_contract_metric 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py::test_paired_wilcoxon_expansions_uses_paired_query_total_expansions 2_experiment/forest_n3p/tests/test_module2_metric_protocol.py` -> `3 passed`。
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py 2_experiment/forest_n3p/tests/test_module2_metric_protocol.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` -> `11 passed`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/evaluation.py 2_experiment/forest_n3p/main_evaluation.py 2_experiment/forest_n3p/scripts/build_module2_metric_protocol.py`。

## 边界

- H01.2 指标冻结不等于 H01 formal-ready。
- H01 formal-ready 仍受 F02.6 pending 和缺 PPO checkpoint 阻塞。
- PPO checkpoint 必须来自 `gpu3070ti-relay` 等远端 GPU formal run, 禁止本地训练补洞。
