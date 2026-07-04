---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_g01_operator_protocol.md
---

# Module2 G01.3 RL-RS Funnel Operator Skeleton 记录

## 直观结论

G01.3 已完成 skeleton: `RlRsFunnelOperator` 可以执行真实 RL-RS rollout, 在 terminal RS success 时追加 Reeds-Shepp 收尾段, 并返回统一 `AnalyticExpansionResult`。如果 rollout 碰撞或 no-progress truncation, 它返回 `None`, 同时保留 `last_telemetry`。

这一步仍不是 planner integration 完成。Hybrid A* 主循环还没有切到 operator dispatch, 也没有加载任何正式 PPO/BC checkpoint。当前 action source 是显式传入的 callable, 用于 stub / 后续模型 wrapper 测试; F02.6 warm-start 决策仍未关闭。

## 实现锚点

- 新增 `forest_n3p.rl_rs.operator`: `2_experiment/forest_n3p/rl_rs/operator.py`。
- `RlRsActionPolicy` 是 `RlRsObservation -> SteeringAction | float` 的 callable contract: `2_experiment/forest_n3p/rl_rs/operator.py:15`。
- `RlRsFunnelTelemetry` 聚合 rollout telemetry、terminal RS 是否使用、terminal RS action 数, 并输出 `analytic_operator=rl_rs_funnel`, `rl_rollout_steps`, collision/sample/terminal timing, terminal success 和 failure reason: `2_experiment/forest_n3p/rl_rs/operator.py:18-43`。
- `RlRsFunnelOperator.try_connect()` 构建真实 `AnalyticExpansionEnv`, 每步调用 `action_policy(observation)`, 记录 rollout endpoint/action, terminal success 时通过 planner context `_try_rs_with_radius(...)` 追加 terminal RS states/actions: `2_experiment/forest_n3p/rl_rs/operator.py:46-103`。
- `_env_context()` 从 planner context 读取 map/footprint/params/collision_checker/collision_step/theta_bins, 保持训练环境与 planner collision checker 一致: `2_experiment/forest_n3p/rl_rs/operator.py:105-119`。
- `_terminal_rs_segments()` 复用现有 planner RS segment conversion, 避免重新写一套 RS-to-MotionPrimitive 逻辑: `2_experiment/forest_n3p/rl_rs/operator.py:121-130`。
- `AnalyticExpansionStep` 现在公开已有内部 `next_state` 和 `primitive`, 让 operator 可以构造 planner 可解释的 `states/actions`: `2_experiment/forest_n3p/rl_rs/env.py:90-91`, `2_experiment/forest_n3p/rl_rs/env.py:303-304`。
- `rl_rs.__init__` 导出 `RlRsFunnelOperator` 与 `RlRsFunnelTelemetry`: `2_experiment/forest_n3p/rl_rs/__init__.py:30`, `2_experiment/forest_n3p/rl_rs/__init__.py:69-70`。

## 测试锚点

新增测试文件: `2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py`。

- success path: zero-steer stub policy 先 rollout 0.3m, 再 append terminal RS; result 是 `AnalyticExpansionResult`, `states[-1] == goal`, `states/actions` 长度一致, `terminal_rs_used=True`, telemetry 中 `rl_rollout_steps=1`: `2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py:27-54`。
- collision path: 前方障碍导致 rollout collision; operator 返回 `None`, `last_telemetry.failure_reason=collision`, `terminal_rs_used=False`: `2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py:57-73`。
- no-progress path: goal 在后方、stub policy 直行, no-progress truncation 后返回 `None`, `failure_reason=no_progress`: `2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py:76-91`。

## TDD 记录

RED 1:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py -q
```

失败点:

```text
ModuleNotFoundError: No module named 'forest_n3p.rl_rs.operator'
```

GREEN 1:

```text
2 passed in 0.42s
```

RED 2:

```text
TypeError: RlRsFunnelOperator.__init__() got an unexpected keyword argument 'no_progress_patience'
```

GREEN 2:

```text
3 passed in 0.43s
```

相关回归:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py \
  2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py \
  2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py \
  2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py -q
```

stdout:

```text
32 passed in 0.93s
```

## 当前边界

- 可以 claim: `RlRsFunnelOperator` skeleton 已能用 stub policy 走真实 env rollout、terminal RS append、failure return 和 telemetry。
- 不能 claim: Hybrid A* 主循环已经调用 `RlRsFunnelOperator`。
- 不能 claim: PPO checkpoint 或 obstacle-summary warm-start 已成为正式 operator。
- 不能 claim: planner integration、端到端时间、节点数或路径质量有新结果。
- G02.2 仍要求后续 checkpoint loader 缺文件时硬失败, 不能静默回退 RS。

下一步应进入 G01.4/G02.1: 增加显式 operator selection/config 或无模型 stub integration test, 仍保持默认 planner 行为不变。
