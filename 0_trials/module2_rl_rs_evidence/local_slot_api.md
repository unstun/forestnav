---
origin: ai+local
reviewed: false
created: 2026-07-03
topic: ForestNav analytic expansion slot API
---

# 本地 analytic expansion 插槽 API 备忘

## 直观结论

模块2要替换的是一个很具体的职责:

> 当前搜索弹出一个 HA* node 后, 尝试生成一条从该 node 到最终 goal 的连续可行连接边。如果成功, 直接把这条边拼到搜索树尾部并返回整条路径。如果失败, 什么都不改变, 继续普通 motion primitive expansion。

因此, RL 版本不是 planner 外面的独立 agent, 也不是 F-N3P 式 subgoal predictor。它必须像 RS analytic expansion 一样, 成为 HA* 主循环里的一个可失败 operator。

## 1. 当前调用点

本地代码:

- `_analytic_interval(state, goal)`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:197-202`
- `_try_analytic_expansion(state, goal)`: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:204-245`
- 主循环调用: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:454-473`
- 普通 primitive fallback: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:476-500`

当前控制流:

```text
pop lowest-cost node
  -> if goal reached: return tree path
  -> if analytic interval hit:
       analytic = _try_analytic_expansion(current.state, goal)
       if analytic is not None:
           path, actions = reconstruct tree
           path.extend(extra_states)
           actions.extend(extra_actions)
           return path/stats
  -> for primitive in primitives:
       evaluate primitive, collision check, push successor
```

## 2. 当前 operator 的隐含接口

`_try_analytic_expansion()` 目前返回:

```python
Optional[Tuple[List[AckermannState], List[MotionPrimitive]]]
```

语义:

- `None`: analytic expansion 失败。调用方继续 primitive expansion。
- `extra_states`: 从当前 node 后面追加到路径里的连续状态段端点。
- `extra_actions`: 与 `extra_states` 一一对应的动作段。后续 `_trace_path()` 会用 action 把 path densify。

强约束:

- `len(extra_states) == len(extra_actions)`。
- 最后一个 state 必须能满足 `_goal_reached(..., goal)` 或被设置为 `goal`。
- 所有 states/actions 对应的 dense samples 必须无碰撞。
- 失败不能修改 open/closed/search state。

## 3. RL-RS operator 建议显式接口

建议新增 protocol, 不直接把神经逻辑塞进 `HybridAStarPlanner`:

```python
class AnalyticExpansionOperator(Protocol):
    name: str

    def try_connect(
        self,
        state: AckermannState,
        goal: AckermannState,
        context: AnalyticExpansionContext,
    ) -> AnalyticExpansionResult | None:
        ...
```

`AnalyticExpansionContext` 应包含:

```python
@dataclass(frozen=True)
class AnalyticExpansionContext:
    grid_map: GridMap
    footprint: Footprint
    params: AckermannParams
    collision_checker: object
    collision_step: float
    goal_xy_tol: float
    goal_theta_tol: float
    theta_bins: int
    rng: np.random.Generator | None
    telemetry_enabled: bool
```

`AnalyticExpansionResult` 应包含:

```python
@dataclass(frozen=True)
class AnalyticExpansionResult:
    states: tuple[AckermannState, ...]
    actions: tuple[MotionPrimitive, ...]
    dense_samples: tuple[AckermannState, ...]
    terminal_rs_used: bool
    telemetry: AnalyticExpansionTelemetry
```

`AnalyticExpansionTelemetry` 最少字段:

```python
@dataclass(frozen=True)
class AnalyticExpansionTelemetry:
    operator: str
    attempted: bool
    success: bool
    failure_reason: str | None
    elapsed_s: float
    rollout_steps: int
    nn_forward_time_s: float
    collision_check_time_s: float
    rs_check_time_s: float
    terminal_rs_success: bool
    min_clearance_m: float | None
```

## 4. Dang-RS operator 适配

第一步不要直接上 RL。应先把当前 Dang 多曲率 RS 包装成 operator:

```text
HybridAStarPlanner
  analytic_operator = DangRsOperator(...)
```

价值:

- 新 telemetry 可以先在旧方法上跑通。
- 后续 RL operator 与 Dang operator 共用 evaluation 字段。
- 能避免 "新方法快/慢" 是因为统计口径变了。

## 5. RL-RS funnel operator 控制流

建议流程:

```text
try_connect(state, goal, context):
  start timer
  cur = state
  path_states = []
  path_actions = []
  for t in range(max_rollout_steps):
      if terminal_rs(cur, goal) succeeds:
          append terminal RS samples/actions
          return success result
      obs = build_egocentric_obs(cur, goal, map, EDT)
      steer = policy(obs)
      arc = sample_constant_steer_motion(cur, steer, +1, step_m, params)
      if collision_checker.collides_path(arc):
          return None with telemetry
      append arc endpoint/action
      cur = arc[-1]
      if no_progress:
          return None with telemetry
  final terminal_rs attempt
  if succeeds: return success result
  return None
```

必须保留的性质:

- policy 失败不影响 HA* 搜索。
- terminal RS 是 success 判据, 不是可选美化。
- dense samples 必须可供 evaluation 和 debug 可视化。
- 不能静默 fallback 到 Dang-RS 后还把结果标成 RL。

## 6. 与外部证据的对齐

- Dolgov 原文定义 analytic expansion: 额外生成当前 state 到 goal 的 Reed-Shepp child, 再碰撞检测; 远离 goal 不宜每个节点都做。见 `sources.md` S007。
- MATLAB `plannerHybridAStar` 工程文档同样把 analytic expansion 定义为周期性尝试 RS connection, 失败继续 motion primitive cycle。见 `sources.md` S009。
- HOPE 是 RL/RS action switch, 不在 HA* open-list node 上实现 operator。见 `sources.md` S002/S003。

## 7. 验收测试建议

最小测试集不是 "跑一个图成功"。需要:

1. `DangRsOperator` 与旧 `_try_analytic_expansion()` 在固定 query 上返回等价 path/action。
2. mock `RlRsFunnelOperator` 成功时, planner 的 `remediations` 或 telemetry 标出 RL analytic expansion。
3. mock `RlRsFunnelOperator` 返回 None 时, planner 继续 primitive expansion。
4. checkpoint 缺失时, RL operator 报错, 不允许静默退回 Dang-RS。
5. telemetry 中 `elapsed_s`, `nn_forward_time_s`, `collision_check_time_s`, `terminal_rs_success` 全部可读。
