---
origin: ai+web+local
reviewed: false
created: 2026-07-03
topic: module2 RL-RS negative results
---

# 负面结果与证伪记录

> 用途: 防止后续重复把相邻工作误写成 "已经替换 analytic expansion"。

## N001: 只做端到端 RL planner 不能算模块2完成

- 本地依据: 真实插入点是 `HybridAStarPlanner._try_analytic_expansion()`, 主循环在 analytic 成功时拼接并返回, 失败才扩展 primitives。
- 锚点: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:204-245`, `:454-500`。
- 结论: 任何不接入这个槽位的 RL demo 都不能声称替换 RS。

## N002: HOPE 不是 HA* analytic expansion slot replacement

- 外部代码依据:
  - `src/model/agent/parking_agent.py#L90-L95`: `ParkingAgent.choose_action()` 在 RS route 执行期取 `RsPlanner` 动作, 否则取 RL agent 动作。
  - `src/train/train_HOPE_ppo.py#L192-L208`: train loop 先执行 `parking_agent.choose_action(obs)`, env step 后若 `info['path_to_dest']` 存在才把 RS path 注入 agent。
  - `src/env/car_parking_base.py#L291-L299`: 接近目标且 `find_rs_path()` 成功时 env 写入 `path_to_dest`。
  - `src/env/car_parking_base.py#L413-L450`: RS path 在 parking env 内枚举和碰撞验证。
- 结论: HOPE 是强相关竞品和设计线索, 但不能作为 "本任务已有人直接做过" 的证据。

## N003: Neural A* 不是 local analytic connector

- 外部代码依据:
  - `NeuralAstar.encode()` 输出 cost map。
  - forward 调用 A* 搜索。
- 结论: 它是 learned heuristic/search guidance 相关工作, 不是 RS shot 替代。

## N003b: LoHA*/SLOPE 不是 analytic connector

- 外部依据:
  - LoHA* 学 local heuristic 并放入 focal search。
  - SLOPE 学距离 optimal path 的函数, 用于 prune unfavorable nodes。
- 结论: 都是 search guidance/node pruning 层, 不是生成当前 node 到 goal 的连续连接边。

## N004: F-N3P/KNN/MLP 不是 RL 替换 RS

- 本地依据:
  - `run_forest_n3p()` 使用 predictor 预测 subgoal, 再用 RS 验证 subgoal 可达。
  - 这属于 learned subgoal decomposition, 不是在 HA* analytic expansion 里闭环 rollout。
- 结论: 可保留为 baseline 或消融, 不能作为模块2最终主方法。

## N005: Adapting RL for Path Planning 不是内部 RS shot replacement

- 外部依据:
  - 论文 lines 86-88 自述是 autonomous driving pipeline 中 Hybrid A* module 的 drop-in replacement。
  - lines 125-130, 154-162 显示它使用 closed-loop PPO + curriculum/action chunking 生成整条路径。
- 结论: 可借 PPO/chunking/curriculum 设计, 但不是 ForestNav module2 的 HA* analytic operator。

## N006: Dang 2022 不是 learned analytic connector

- 外部依据:
  - Dang Section 3 生成的是不同 curvature values 下的 multiple RS curves, 再按 objective function 选择最低成本曲线。
  - 若没有可用 RS curve, 算法继续 forward search; 没有 neural policy、RL rollout 或 learned steering function。
- 本地依据:
  - ForestNav `dang_multi_rs` 只调用 `reeds_shepp_shortest_path()`、采样、碰撞检查和 `_dang2022_cost()`。
  - 本地 risk cost 还是 Eq.2 的 EDT 近似, 不是 learned obstacle-aware policy。
- 结论: Dang 是强 classical baseline 和问题动机, 不能作为 "已有学习式 RS 替换" 的证据。
