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
  - .pipeline/experiments/20260704_module2_h02_statistical_ci_infra.md
  - .pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md
  - .pipeline/experiments/20260704_module2_h02_formal_acceptance_audit.md
---

# I02 Paper Table Protocol

## 直观结论

本轮没有也不能填正式论文结果表。当前 H02 只有 available subset smoke, `formal_acceptance=false`; H01 manifest 仍 `blocked_pending_decisions`; F02.6 warm-start decision pending; PPO formal checkpoint/rows 均不存在。

因此本轮完成的是 I02 表格协议和 preview 生成器: 它能从 H02 evaluation outputs 生成主表、消融计划和 failure-analysis preview, 但在当前状态下自动输出 `formal_claim_allowed=false` 和 `blocked_no_formal_h02_data`。这防止把 smoke 数字误写成论文结果。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_paper_tables.py`
- `2_experiment/forest_n3p/tests/test_module2_paper_tables.py`
- `0_trials/module2_paper_tables/module2_paper_tables.json`
- `0_trials/module2_paper_tables/module2_paper_tables.md`

## 当前 Artifact 状态

- status: `blocked_no_formal_h02_data`
- formal_claim_allowed: `false`
- local_training_allowed: `false`
- remote_training_resource: `gpu3070ti-relay`
- A02.3 telemetry refresh: `module2_paper_tables.json` now includes `telemetry_diagnostic_table` sourced from runtime/evaluation telemetry columns.
- H02 acceptance integration: `module2_paper_tables.json` now reads `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`; current `h02_formal_acceptance_status=blocked_formal_output_acceptance` and `h02_formal_acceptance_not_accepted` blocks formal tables.
- blockers:
  - `h02_verdict_not_formal`
  - `h02_formal_acceptance_not_accepted`
  - `h01_manifest_not_ready`
  - `f02_6_warm_start_decision_pending`
  - `f02_6_decision_packet_pending`
  - `missing_module2_rl_rs_checkpoint`
  - `missing_ppo_result_rows`

## 表格覆盖

- I02.1 main table preview:
  - rows: method-level aggregation from `records.csv`
  - columns: success, timeout, time p50/p95, expansions p50/p95, path inflation p50, clearance p50
  - status: `preview_not_formal`
- I02.2 ablation table:
  - planned contrasts: occupancy-only vs occupancy+EDT, BC vs PPO, terminal RS on/off, action mask on/off, forward-only vs forward+reverse if enabled
  - status: `blocked_missing_formal_data`
- I02.3 failure-analysis table:
  - failure buckets: timeout, collision, terminal_rs_fail, oscillation, oracle_no_solution, other
  - status: `preview_not_formal`
- Diagnostic telemetry table:
  - columns: RL attempts/successes, RS attempts, NN forward mean/p95, primitive fallback total, rollout protocol, collision checker
  - source: A02.3 runtime/evaluation telemetry columns
  - status: `preview_not_formal`

## 关键代码/数据锚点

- Evaluation record schema: `2_experiment/forest_n3p/evaluation.py:63`
- Group summary schema: `2_experiment/forest_n3p/evaluation.py:107`
- Paired time Wilcoxon: `2_experiment/forest_n3p/evaluation.py:480`
- Paired expansion Wilcoxon: `2_experiment/forest_n3p/evaluation.py:515`
- Timeout bootstrap CI: `2_experiment/forest_n3p/evaluation.py:616`
- Evaluation output writer: `2_experiment/forest_n3p/evaluation.py:687`
- Metric protocol primary metric anchor: `2_experiment/forest_n3p/scripts/build_module2_metric_protocol.py:94`
- H01 F02.6 guard anchor: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:322`
- Current H02 available subset verdict: `0_trials/module2_h02_local_smoke/h02_1_available_subset/verdict.json`
- Current H01 manifest: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`

## 验证

- Memory retrieval: confirmed I02 is next but formal data is absent; F02.6 and PPO checkpoint remain open.
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact file reads.
- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py` first failed on missing builder.
- GREEN targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py` -> `1 passed in 0.08s`.
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_module2_metric_protocol.py 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py` -> `10 passed in 1.08s`.
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_paper_tables.py`.
- Artifact audit: `module2_paper_tables_artifact=ok`.
- 2026-07-04 telemetry refresh: RED failed on missing `telemetry_diagnostic_table`; GREEN targeted `9 passed`; full `2_experiment/forest_n3p/tests` -> `112 passed in 12.15s`.
- 2026-07-04 H02 acceptance integration: `--h02-formal-acceptance` 已接入; synthetic formal table + blocked H02 acceptance 仍会输出 `blocked_no_formal_h02_data`; targeted `12 passed in 0.57s`; full `2_experiment/forest_n3p/tests` -> `120 passed in 12.01s`。

## 边界

- Current preview rows must not be used as paper results.
- Formal paper tables require H02 `formal_acceptance=true`, H02 formal acceptance `paper_result_input_allowed=true`, H01 formal-ready status, frozen metric protocol, and real PPO checkpoint/result rows.
- PPO formal training/checkpoint production must run on `gpu3070ti-relay`; this task did not train locally.
