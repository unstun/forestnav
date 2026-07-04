---
origin: ai+local
reviewed: false
created: 2026-07-04
topic: module2 A02.3 evaluation telemetry field gap audit
---

# A02.3 Evaluation Telemetry 字段缺口审计

## 直观结论

当前 evaluation 已经比最初强很多: `records.csv` 能平铺输出 `analytic_attempts`, `analytic_successes`, `analytic_failure_count`, `rl_rollout_steps`, `rl_rollout_collision_checks`, `terminal_rs_success_count`, checkpoint path/hash 等字段。

但它还不能支撑论文级完整 claim。主要缺口有四类:

1. **命名缺口**: A02.3 要求的 `rs_attempts`, `rl_attempts`, `rl_successes`, `fallback_to_primitives_count` 没有直接字段, 只能部分从 analytic/operator 字段推断。
2. **NN forward 缺口**: `RlRsEpisodeTelemetry.nn_forward_time_s` 现在硬返回 `0.0`, operator 调 policy 没有计时; 这不能支撑 "端到端时间含神经网络前向" 的分量账。
3. **协议字段缺口**: run-level `run_config.json` 有 RL-RS 参数, 但 `records.csv`/record metadata 没有 checker protocol / rollout protocol manifest link。
4. **聚合缺口**: `summary_by_method_bucket.csv` 目前聚合时间、扩展、失败率、fallback F1/F2/F3 等, 但不聚合 analytic success rate、terminal RS success rate、NN forward time。

因此 A02.3 的结论是: current evaluation is partially paper-ready for classical timing/expansion comparisons, but not paper-ready for learned analytic operator diagnostics.

## 必需字段逐项判定

| 字段 | 当前状态 | 证据 | 判定 | 后续动作 |
|---|---|---|---|---|
| `analytic_attempts` | 已平铺到 `EvaluationRecord` | `evaluation.py:86-90`, `:379-382`; planner stats `planner.py:680-683`, `:917-920` | 可用于 records.csv | 保留, 后续聚合为 success rate |
| `analytic_successes` | 已平铺 | `evaluation.py:86-90`, `:379-382`; planner success path `planner.py:745-766` | 可用于 records.csv | 保留 |
| `analytic_failure_count` | 已平铺 | `evaluation.py:86-90`, `:379-382`; planner stats `planner.py:920-926` | 可用于 records.csv | 保留 |
| `rs_attempts` | 无直接字段 | RS builtin telemetry 有 candidate radius count/time, terminal RS 只有 success/used count | 缺失/命名不清 | 新增 `rs_candidate_attempts` 和 `terminal_rs_attempts`; 不要用 `analytic_attempts` 冒充 |
| `rl_attempts` | 无直接字段 | RL operator 每次 analytic attempt 会产生 telemetry record, 但 records 只汇总 rollout steps | 缺失/可派生但不稳 | 新增 `rl_attempts` = RL telemetry records count |
| `rl_successes` | 无直接字段 | `analytic_successes` 可代表 operator accepted edge, `terminal_rs_success_count` 代表 terminal check 成功次数 | 缺失/语义需拆分 | 新增 `rl_operator_successes`; 保留 `terminal_rs_success_count` |
| `terminal_rs_successes` | 已有但命名为 `terminal_rs_success_count` | `evaluation.py:94-97`, `:387-390`, `:408-409` | 可用, 但字段名与 A02.3 原名不同 | 后续可加 alias 或在 protocol 中固定 canonical name |
| `nn_forward_time_s` | 形式存在但值恒为 0, 且未进 EvaluationRecord | `telemetry.py:30-33`, `operator.py:76-80`, `evaluation.py:62-103` | 关键缺口 | operator policy call 必须计时, 并平铺到 record/summary |
| `rollout_collision_checks` | 已有但命名为 `rl_rollout_collision_checks` | `evaluation.py:90-93`, `:383-386`, `operator.py:31-44`; telemetry source `telemetry.py:50-62` | 可用, 需确认其语义是 sample count 而非 checker call count | 字段说明写清; 若需要 call count, 另增 `rl_rollout_collision_check_calls` |
| `rollout_steps` | 已有但命名为 `rl_rollout_steps` | `evaluation.py:90-93`, `:383-386`, `operator.py:31-44` | 可用 | 保留 |
| `fallback_to_primitives_count` | 无直接字段 | `analytic_failure_count` 表示 failed analytic attempts, 但不等于 primitive fallback count; F-N3P fallback F1/F2/F3 是另一套 | 缺失 | 新增 planner-level `primitive_fallback_count` 或 `analytic_failed_then_primitive_expanded_count` |

缺失或不够审计字段: `rs_attempts`, `rl_attempts`, `rl_successes`, `nn_forward_time_s`, `fallback_to_primitives_count`, checker/rollout protocol manifest。

## 当前数据链路

### 1. Planner stats 已有 analytic 尝试/成功/失败

- planner 初始化 `analytic_attempts`, `analytic_successes`, `analytic_failure_records`, `analytic_telemetry_records`: `planner.py:680-683`。
- analytic trigger 时递增 `analytic_attempts`: `planner.py:724-728`。
- analytic 成功时递增 `analytic_successes`, 并返回拼接路径: `planner.py:745-766`。
- analytic 失败时追加 failure record, 后续仍进入 primitive expansion: `planner.py:767-783`。
- `_stats()` 输出 `analytic_operator`, `analytic_attempts`, `analytic_successes`, `analytic_failure_count`: `planner.py:910-921`。
- `_analytic_telemetry_summary()` 汇总 candidate radius/time/sample/collision check: `planner.py:937-967`。

缺口:

- 没有 `fallback_to_primitives_count`。当前可近似为 `analytic_failure_count`, 但这只是 failed analytic attempts, 不是 "after failure, primitive expansion actually generated successors" 的计数。
- 没有把 RS candidate attempts 与 RL attempts 拆成同一字段体系。

### 2. EvaluationRun metadata 会接收大部分 analytic stats

- `planner_run_from_path_stats()` 复制 analytic key 到 metadata: `evaluation.py:262-279`。
- 它主动丢弃原始 `analytic_telemetry_records`, 只保留聚合字段: `evaluation.py:280-283`; 测试也锁定不保留原始 records: `test_evaluation_timing_protocol.py:64-108`。
- `_update_rl_rs_telemetry_summary()` 从 analytic telemetry records 汇总 RL rollout/terminal RS 字段: `evaluation.py:400-409`。

缺口:

- 原始 per-attempt telemetry 不进入 record metadata, 因此后处理无法重新计算更细字段。
- 如果要 paper-grade 诊断, 需要保存 compact per-attempt artifact 或至少记录 `rl_attempts`, `rl_successes`, `terminal_rs_attempts` 这些不可逆聚合。

### 3. EvaluationRecord 已平铺一部分字段

已有 flat columns:

- `analytic_operator`, `analytic_attempts`, `analytic_successes`, `analytic_failure_count`: `evaluation.py:86-90`, `:379-382`。
- `rl_rollout_steps`, `rl_rollout_collision_checks`, `rl_rollout_sample_time_s`, `rl_rollout_collision_time_s`: `evaluation.py:90-94`, `:383-386`。
- `terminal_rs_time_s`, `terminal_rs_success_count`, `terminal_rs_used_count`, `terminal_rs_action_count`: `evaluation.py:94-97`, `:387-390`。
- `bc_checkpoint`, `bc_checkpoint_sha256`, `rl_rs_checkpoint`, `rl_rs_checkpoint_sha256`: `evaluation.py:98-101`, `:391-394`。

缺口:

- `nn_forward_time_s` 不在 `EvaluationRecord`。
- `rl_attempts`, `rl_successes`, `rs_attempts`, `fallback_to_primitives_count` 不在 `EvaluationRecord`。
- checker/rollout protocol 不在 `EvaluationRecord`; 只在 `run_config.json` 有部分配置。

### 4. Summary 聚合还没覆盖 learned operator 诊断

- `summarize_by_method_bucket()` 聚合 success/time/expansions/path/fallback F1-F3/subgoal reachability: `evaluation.py:437-477`。
- H01.2 metric protocol 写明 diagnostic metrics 包括 `analytic_success_rate`, `terminal_rs_success_rate`, `nn_forward_time_s`: `.pipeline/experiments/20260704_module2_h01_metric_protocol.md`。

缺口:

- summary 没有 `analytic_success_rate`。
- summary 没有 `terminal_rs_success_rate`。
- summary 没有 `nn_forward_time_s` 聚合。
- summary 的 `fallback_trigger_rate` 是 F-N3P F1/F2/F3 fallback, 不是 analytic operator fallback-to-primitives。

### 5. NN forward budget 与 evaluation telemetry 脱节

- 独立 forward budget 脚本会写 `forward_mean_ms`, `forward_p50_ms`, `forward_p95_ms` 等: `scripts/run_policy_forward_budget.py:25-52`, `:124-150`。
- 但 runtime `RlRsEpisodeTelemetry.nn_forward_time_s` 当前恒为 `0.0`: `rl_rs/telemetry.py:30-33`。
- `RlRsFunnelOperator.try_connect()` 没有在 `self.action_policy(observation)` 外计时: `rl_rs/operator.py:76-80`。
- `RlRsFunnelTelemetry.to_record()` 也没有输出 `nn_forward_time_s`: `rl_rs/operator.py:31-44`。

结论:

- D02 forward budget 可作为离线成本上界/先验, 不能替代 formal evaluation 中每条 query 的 runtime NN forward time。
- 后续必须在 operator 层真实计时, 进入 telemetry record, 再进入 `EvaluationRecord`。

## 后续实现优先级

### P0: 论文 claim 阻塞项

1. 给 `RlRsFunnelOperator.try_connect()` 的 action policy call 加真实 wall-clock 计时。
2. 将 `nn_forward_time_s` 写入 `RlRsEpisodeTelemetry`/`RlRsFunnelTelemetry.to_record()`。
3. 在 `EvaluationRecord` 增加 `nn_forward_time_s` flat column, summary 增加 median/p95/mean。
4. 增加 `rl_attempts`, `rl_successes`, `terminal_rs_attempts`, `rs_candidate_attempts`。
5. 增加 `fallback_to_primitives_count` 或明确命名为 `analytic_failed_then_primitive_expanded_count`。

### P1: 审计和可复现项

1. 给 records 或 companion manifest 写入 collision protocol: checker class、footprint、theta bins、collision step、padding。
2. 记录 RL rollout protocol: max steps、action step、terminal check interval、no-progress patience、append terminal RS。
3. 保留 compact per-attempt telemetry artifact, 不把全部 JSON 塞进 records.csv。

### P2: 论文表格便利项

1. `summary_by_method_bucket.csv` 增加 analytic success rate、terminal RS success rate、RL operator success rate。
2. `summary.json` 增加 learned-operator diagnostic section。
3. 把 H01 manifest 的 diagnostic metric 名称与 `EvaluationRecord` canonical fields 对齐。

## A02.3 判定

A02.3 可以标为完成: 当前 evaluation 字段缺口已逐项审计, 并形成后续实现字段清单。它不等于这些字段已经实现; 它明确指出当前 records.csv 还不能支撑完整 learned analytic operator 论文诊断表。

This is a gap audit, not implementation of the missing telemetry columns.
