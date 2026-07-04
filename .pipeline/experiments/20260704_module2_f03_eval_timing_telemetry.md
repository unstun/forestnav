---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_no_warm_failure_analysis.md
---

# Module2 F03 Gate #3 Eval Timing Telemetry 修复记录

## 直观结论

Gate #3 evaluator 原来把 `nn_forward_time_s` 写成 0.0, 不是因为 PPO 前向免费, 而是因为 `model.predict()` 在 evaluator 脚本外层执行, planner env 的 telemetry 根本看不到神经网络前向边界。

现在 `eval_rl_rs_gate3.py` 在每次 `model.predict()` 周围用 `perf_counter()` 计时, 并把耗时交给 `RlRsEpisodeLoggingWrapper.record_nn_forward_time()`。episode CSV 和 `gate3_summary.json` 都会记录非零 neural forward time。

这修复的是 eval telemetry, 不改变 Gate #3 success/failure 判定, 不改变 reward/curriculum/policy, 也不把 no-warm formal fail 改写成 pass。

## 根因证据

- evaluator 原循环直接 `model.predict(obs, deterministic=True)` 后 `env.step(action)`, 没有任何计时代码: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:42-46`。
- logging wrapper 从 planner telemetry 取 `nn_forward_time_s`: `2_experiment/forest_n3p/rl_rs/training_logging.py:153`。
- planner telemetry 的 `RlRsEpisodeTelemetry.nn_forward_time_s` 固定为 0.0, 因为 planner env 只知道 rollout/collision/terminal-RS 耗时: `2_experiment/forest_n3p/rl_rs/telemetry.py:24-27`。

## 实现锚点

- `eval_rl_rs_gate3.py` 导入 `perf_counter`, 在 `model.predict()` 前后计时, 然后调用 `env.record_nn_forward_time(...)`: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:10`, `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:43-45`。
- `RlRsEpisodeLoggingWrapper` 新增 `_nn_forward_time_s` episode accumulator, reset 时清零: `2_experiment/forest_n3p/rl_rs/training_logging.py:65`, `2_experiment/forest_n3p/rl_rs/training_logging.py:73`。
- `record_nn_forward_time()` 拒绝非有限或负数, 只累加合法外部前向耗时: `2_experiment/forest_n3p/rl_rs/training_logging.py:76-80`。
- CSV episode record 现在把外部 accumulator 与 planner telemetry 合并写入 `nn_forward_time_s`: `2_experiment/forest_n3p/rl_rs/training_logging.py:153`。
- TensorBoard 也新增 `timing/nn_forward_time_s`: `2_experiment/forest_n3p/rl_rs/training_logging.py:194`。
- `gate3_summary.json` 汇总 CSV 中的 `nn_forward_time_s`, 并写出 `mean_nn_forward_time_s`: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:133`, `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:153-154`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py -q
```

失败点:

```text
AssertionError: assert 0.0 > 0.0
where 0.0 = float('0.0')
```

新增测试锚点:

- eval smoke test 要求 `gate3_summary.json` 的 `nn_forward_time_s` 和 `mean_nn_forward_time_s` 都大于 0: `2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py:60-61`。
- eval episode CSV 第一行 `nn_forward_time_s` 必须大于 0: `2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py:66`。

GREEN:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py -q
```

stdout:

```text
1 passed in 1.59s
```

相关回归:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py \
  2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py \
  2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py -q
```

stdout:

```text
7 passed in 1.65s
```

## 项目内 smoke 证据

命令:

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE python -m forest_n3p.scripts.run_rl_rs_gate3_trial \
  --smoke \
  --output-dir 0_trials/module2_ppo_smoke/f03_gate3_eval_timing_smoke \
  --seed 20260704 \
  --allow-duplicate-openmp
```

产物:

- `0_trials/module2_ppo_smoke/f03_gate3_eval_timing_smoke/eval/gate3_summary.json`
- `0_trials/module2_ppo_smoke/f03_gate3_eval_timing_smoke/eval/gate3_eval_episodes.csv`

关键字段:

```text
decision=pass
episodes=4
terminal_rs_success_rate=1.0
nn_forward_time_s=0.000748333000956336
mean_nn_forward_time_s=0.000187083250239084
```

CSV 四行 `nn_forward_time_s` 全部非零:

```text
0.00030862499988870695
0.00017250000018975697
0.00013558300270233303
0.00013162499817553908
```

## No-Warm Formal Model 补充 eval timing

为了不覆盖原 formal audit, 使用同一个 no-warm `final_model.zip` 单独重跑 eval 到 `eval_timing_v2/`:

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE python -m forest_n3p.scripts.eval_rl_rs_gate3 \
  --model 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/train/final_model.zip \
  --output-dir 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval_timing_v2 \
  --seed 20260704 \
  --device auto \
  --curriculum-preset f03 \
  --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --heldout-seed 20260704 \
  --episodes 64 \
  --min-episodes 64 \
  --success-threshold 0.8 \
  --obs-patch-size-m 6.4 \
  --obs-patch-cells 64 \
  --obs-edt-clip-m 2.0 \
  --max-steps 32 \
  --action-step-m 0.3 \
  --collision-sample-step-m 0.1 \
  --terminal-check-every 1 \
  --theta-bins 72 \
  --allow-duplicate-openmp
```

与原 formal eval 完全一致的字段:

```text
decision=fail
episodes=64
terminal_rs_success=29
terminal_rs_success_rate=0.453125
collision=23
collision_rate=0.359375
truncated=12
truncation_rate=0.1875
model_sha256=3b34c57b41ad304bfecf31c6eaf1a327432aee79f409a3a669d9f27607acbd82
```

新增 timing 字段:

```text
nn_forward_time_s=0.050569629958772566
mean_nn_forward_time_s=0.0007901504681058213
nonzero_episode_rows=64/64
min_episode_nn_forward_time_s=0.00013991699961479753
max_episode_nn_forward_time_s=0.004592457004036987
```

补充产物:

- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval_timing_v2/gate3_summary.json`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval_timing_v2/gate3_eval_episodes.csv`

## 边界

- 可以 claim: Gate #3 evaluator 现在记录 `model.predict()` wall-clock; no-warm formal model 的补充 eval timing 可复查。
- 不能 claim: planner integration 端到端时间, Hybrid A* 总规划时间下降, neural operator 已经接入 analytic expansion。
- no-warm formal failure 仍然是 failure; 本修复没有改变 `29/64` 的成功率。
