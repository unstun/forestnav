---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_g01_operator_protocol.md
  - .pipeline/experiments/20260704_module2_g01_rl_rs_funnel_operator_skeleton.md
---

# Module2 G01.4/G02.1 Custom Operator Dispatch Stub Integration 记录

## 直观结论

本次完成的是 planner 内部的 custom analytic operator dispatch 和无模型 stub integration test: `HybridAStarPlanner` 现在可以通过构造参数显式传入一个 `analytic_expansion_operator` 对象。传入后, planner 会在 analytic expansion slot 调用该 operator 的 `try_connect(state, goal, context)`; operator 成功时沿用 `AnalyticExpansionResult.to_legacy_tuple()`, operator 返回 `None` 时自然回落到普通 motion primitive expansion。

这一步没有改变默认行为。未传 `analytic_expansion_operator` 时, 仍走原来的 `analytic_operator in {disabled,single_rs,dang_multi_rs}` 路径和内置 Dang/RS 逻辑。

这一步也不是完整 CLI/config 集成。当前完成的是 constructor-level explicit operator selection; 后续还需要把实验脚本或命令行配置显式接到该参数, 并给 checkpoint-based operator 增加缺文件硬失败测试。

## 实现锚点

- `HybridAStarPlanner.__init__()` 新增 `analytic_expansion_operator=None` 参数: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:127-130`。
- planner 保存 custom operator; 若传入 operator, `self.analytic_operator` 使用 `operator.name` 或 fallback 名称, 并跳过内置 `ANALYTIC_OPERATORS` 枚举校验: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:175-188`。
- `_try_analytic_expansion()` 现在先判断 custom operator, 否则调用内置 `_try_builtin_analytic_expansion()`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:294-297`。
- `_try_custom_analytic_expansion()` 调用 `analytic_expansion_operator.try_connect(state, goal, self)`, operator 返回 `None` 时保存 `last_telemetry` 并返回 `None`; 成功时保存 result telemetry 并转回 legacy `(states, actions)`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:299-306`。
- `_analytic_telemetry_record()` 现在接受内置 `AnalyticExpansionTelemetry`, 也接受任意带 `to_record()` 的 custom telemetry object: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:415-423`。
- 失败记录会 merge custom telemetry, 因此 custom operator 的 `failure_reason` 可以进入 `analytic_failure_records`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:409-413`。
- 主循环每次 analytic attempt 后统一调用 `_analytic_telemetry_record()`, 并追加 `attempt_index`, `expansion_idx`, current state 和 goal 字段: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:724-744`。

## 测试锚点

新增测试仍在 `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py`。

- `DirectStubOperator` 返回 `AnalyticExpansionResult`, telemetry 中记录 `analytic_operator=stub_direct` 和 `stub_success=True`: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:13-43`。
- `FailingStubOperator` 返回 `None`, telemetry 中记录 `analytic_operator=stub_failing` 和 `failure_reason=stub_failure`: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:46-56`。
- `_planner(..., analytic_expansion_operator=...)` 把 custom operator 传入 `HybridAStarPlanner`: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:59-75`。
- success path 测试验证 planner 调用 custom operator 一次、`stats["analytic_operator"] == "stub_direct"`、analytic attempts/successes 为 `1/1`, telemetry record 含 `attempt_index=0` 和 `expansion_idx=0`: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:134-150`。
- failure path 测试验证 custom operator 返回 `None` 后 planner 仍能产出 path, analytic successes 为 0, 不写入 `analytic_expansion` remediation, 且 `analytic_failure_records[0]` 包含 `stub_failing` 与 `stub_failure`: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:153-172`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py -q
```

失败点:

```text
TypeError: HybridAStarPlanner.__init__() got an unexpected keyword argument 'analytic_expansion_operator'
```

GREEN targeted:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py -q
```

stdout:

```text
5 passed in 0.22s
```

相关回归:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py \
  2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py \
  2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py -q
```

stdout:

```text
12 passed in 0.49s
```

全量 `forest_n3p` 回归:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
70 passed in 9.98s
```

## 当前边界

- 可以 claim: planner 已支持 constructor-level custom analytic operator dispatch。
- 可以 claim: custom operator success 会进入 analytic expansion success path, 并写 telemetry。
- 可以 claim: custom operator failure 会返回 `None`, planner 不终止, 而是继续 primitive expansion fallback。
- 可以 claim: 默认内置 `disabled/single_rs/dang_multi_rs` 行为保持回归通过。
- 不能 claim: CLI/config/script-level symbolic operator selection 已完成。
- 不能 claim: checkpoint-based RL-RS operator 已接入 planner。
- 不能 claim: F02.6 warm-start 决策已关闭。
- 不能 claim: RL-RS funnel 有端到端性能、节点数或路径质量提升。

下一步应继续 G01.4 的 CLI/script-level explicit operator selection, 或进入 G02.2 checkpoint loader hard-failure test。G02.2 必须保证 checkpoint 缺失时报错, 不能静默退回 RS 后声称 RL 生效。
