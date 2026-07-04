---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_eval_timing_telemetry.md
---

# Module2 G01 Analytic Expansion Operator Protocol 记录

## 直观结论

G01.1/G01.2 已经完成第一层接口化: 现在有显式 `AnalyticExpansionOperator` protocol、统一 `AnalyticExpansionResult`, 以及 `DangRsOperator` adapter, 可以把现有 Dang multi-RS analytic expansion 用同一套 result contract 暴露给后续 RL-RS funnel operator。

这一步没有改 Hybrid A* 主循环, 默认 planner 行为不变。它不是 planner integration 完成, 也不是 RL-RS operator 已接入; 它只是把旧 RS analytic expansion 的返回结构先固定成后续可替换的接口。

## 实现锚点

- 新增 operator 模块: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py`。
- `DangRsPlannerContext` 显式声明 adapter 依赖的旧 planner 私有边界: `analytic_operator`, `_last_analytic_telemetry`, `_try_analytic_expansion(...)`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py:10-19`。
- `AnalyticExpansionResult` 固定 result contract: `states`, `actions`, `telemetry`, `terminal_rs_used`, `operator`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py:22-28`。
- Result 不变量: `states/actions` 长度必须一致, 否则抛 `ValueError`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py:30-32`。
- `to_legacy_tuple()` 保留与当前 `_try_analytic_expansion()` 返回 `(states, actions)` 的兼容面: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py:34-35`。
- `AnalyticExpansionOperator` protocol 固定 `try_connect(state, goal, context) -> AnalyticExpansionResult | None`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py:38-48`。
- `DangRsOperator` 当前是 adapter, 委托 planner-owned `_try_analytic_expansion()`, 成功时把 planner `_last_analytic_telemetry` 放入 result: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/operators.py:51-73`。
- subpackage 导出 `AnalyticExpansionOperator`, `AnalyticExpansionResult`, `DangRsOperator`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/__init__.py:1-12`。

## 测试锚点

- 新增测试文件: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py`。
- 成功路径测试验证 `DangRsOperator` 是 `AnalyticExpansionOperator`, 返回 `AnalyticExpansionResult`, `terminal_rs_used=True`, 最后 state 是 goal, `states/actions` 长度一致, telemetry 中有 Dang candidate records: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:31-52`。
- 失败路径测试验证 blocked single-RS 返回 `None`, 但 planner `_last_analytic_telemetry` 保留 collision failure record: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:55-70`。
- result contract 测试验证 `states/actions` 长度不一致会拒绝: `2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py:73-84`。

## TDD 记录

RED 1:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py -q
```

失败点:

```text
ModuleNotFoundError: No module named 'forest_n3p.third_party.pathplan.hybrid_a_star.operators'
```

GREEN 1:

```text
2 passed in 0.20s
```

RED 2:

```text
Failed: DID NOT RAISE <class 'ValueError'>
```

GREEN 2:

```text
3 passed in 0.22s
```

相关回归:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py -q
```

stdout:

```text
7 passed in 0.26s
```

## 当前边界

- 可以 claim: G01.1 operator protocol 和 G01.2 DangRsOperator adapter 已存在并有测试。
- 不能 claim: planner 主循环已通过 operator dispatch 调用。
- 不能 claim: RL-RS funnel operator 已实现。
- 不能 claim: F02.6 warm-start 决策已关闭。
- 不能 claim: planner integration 或端到端性能已有新结果。

下一步应进入 G01.3/G01.4: 在不改变默认 planner 行为的前提下实现 `RlRsFunnelOperator` 的失败返回/telemetry skeleton, 然后再增加显式 config/CLI 选择 operator。
