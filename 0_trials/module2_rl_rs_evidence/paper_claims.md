---
origin: ai+web
reviewed: false
created: 2026-07-03
topic: module2 RL-RS paper claim audit
---

# 论文 claim 审计

## C001: RS analytic expansion 快, 但在障碍附近安全性有问题

- 来源: Dang et al. 2022, Applied Sciences 12(12):5999, DOI 10.3390/app12125999。
- 锚点:
  - MDPI HTML lines 330-337: 摘要说明 Hybrid A* 有 forward search 和 analytic expansion; RS curve 在 analytic expansion phase 提高 accuracy/speed, 但 corner 附近可能贴障碍。
  - MDPI lines 380-402: Section 3 前后说明原 RS path 在角落贴墙, 改进方法生成多曲率 RS、碰撞检查、按 Eq.3 选最低成本, 无可用 RS 则继续 forward search。
  - ResearchGate full-text lines 556-621: Eq.2 Voronoi field 依赖 nearest obstacle distance `d0` 和 generalized Voronoi edge distance `dv`, 用于偏向通道中线。
  - ResearchGate lines 758-844: Eq.3/Eq.4 将 risk cost `v` 与 movement cost `m` 组合; `m` 包含 path length、steering angle、steer switching。
  - MDPI lines 414-419; ResearchGate lines 935-960: Table 1 显示 improved RS 降低 risk cost, 但 execution time 增加。
  - ResearchGate lines 1082-1086, 1109-1174: benchmark maps 上 risk reduction 与 time penalty; 结论说方法在 analytic expansion phase 内生成不同曲率 RS 并选最小 collision-risk candidate。
- 对本项目的作用:
  - 可作为问题动机。
  - 可作为 strong classical baseline, 但应写成 "Dang-style multi-curvature RS analytic expansion baseline"。
- 不能外推:
  - Dang 只在 RS 曲率集合里选 safer route, 不等于 learned obstacle-aware rollout。
  - 当前本地实现用 mean EDT clearance inverse 近似 Eq.2, 没有 generalized Voronoi edge distance `dv`; 不能 claim exact Dang Eq.2。
  - Dang 的 risk reduction 来自其仿真/benchmark maps, 不能外推为 ForestNav 森林场景性能。

## C001b: Dolgov 原始 Hybrid A* 的 analytic expansion 定义

- 来源: Dolgov et al. 2010, IJRR, DOI 10.1177/0278364909359210。
- 锚点:
  - PDF lines 244-249: forward search 因离散 control 难以精确达到连续 goal, 因此加入基于 Reed-Shepp 的 analytic expansions。
  - lines 253-263: 对某些 node 额外生成 current state 到 goal 的 RS child, 并只在 collision-free 时加入树。
  - lines 264-272: RS expansion 比普通 forward expansion 稍贵, 不适合每个 node 都做, 且越接近 goal 越频繁。
- 对本项目的作用:
  - 明确定义模块2要替换的 slot。
  - 支持 "失败后继续 forward expansion" 的控制流要求。

## C001c: MATLAB 工程接口也把 analytic expansion 视作可调 RS/Dubins connection

- 来源: MathWorks `plannerHybridAStar` documentation。
- 锚点:
  - docs lines 171-177: `AnalyticalExpansionCostFcn` 可定制 analytic expansion cost, 默认基于 RS。
  - docs lines 184-193: forward-reverse 用 RS, forward-only 用 Dubins。
- 对本项目的作用:
  - 工程接口层也支持把 analytic expansion 作为独立可配置机制。

## C002: HOPE 证明 RL+RS 组合方向有强相关先例

- 来源: HOPE arXiv 2405.20579。
- 锚点:
  - arXiv HTML lines 39-41: 摘要说明 HOPE integrates RL agent with Reeds-Shepp curves, 并包含 action mask。
  - lines 113-116: 总体框架是 agent 每步输出 action, action mask 后与环境交互。
  - lines 145-172: hybrid policy 在 RL policy 和 RS policy 间选择, RS 只在接近目标且存在 collision-free RS curve 时激活。
  - lines 173-200: action mask 估计给定 steering 下的最大 safe step velocity。
  - lines 247-267: 表 II 对比 RS、Hybrid A*、PPO、SAC、HOPE(PPO/SAC), HOPE 成功率最高。
  - lines 293-301: 单步成本拆成 network forward、action mask、RS curve calculation、simulator。
  - lines 302-339: RS threshold、action mask、transformer、BEV、AE 消融。
  - lines 340-353: 训练 difficulty 覆盖不足会导致 extreme 场景 success 下降。
  - GitHub README lines 237-238: 仓库称 planner integrates RL agent with Reeds-Shepp curves。
- 对本项目的作用:
  - 证明 reviewer 可能会问 RL+RS/HOPE 差异。
  - 可借鉴 RS-distance reward、action mask、difficulty curriculum、RS hybrid ablation 和成本拆分。
- 不能外推:
  - HOPE 不是 HA* analytic expansion operator replacement。
  - HOPE 代码 GPL-3.0, 不能直接复制。
  - HOPE 的 parking success rate 不能作为 ForestNav 森林地图或 Contract 指标证据。

## C002b: Adapting RL for Path Planning 是替换整个 HA* module, 不是替换内部 RS shot

- 来源: arXiv 2601.22545v1。
- 锚点:
  - HTML lines 86-88: 方法定位为 autonomous driving pipeline 中 Hybrid A* module 的 drop-in replacement。
  - lines 125-130: Gym-style closed-loop simulator, static obstacles, bicycle model, PPO via Stable-Baselines3。
  - lines 154-162: curriculum learning and action chunking motivation。
  - lines 166-190: 与 Hybrid A* 对比, PPO+curriculum+chunking 报告更高 success/更低 time。
  - lines 309-369: PPO + action chunking + curriculum algorithm。
- 对本项目的作用:
  - 支持闭环 PPO + bicycle model + action chunking 的可行性线索。
- 不能外推:
  - 它不是在 HA* 内部替换 analytic expansion。
  - 它的成功指标与 ForestNav Contract 不同。

## C003: Neural A* 是 learned search guidance, 不是本模块2

- 来源: Neural A* official repository / ICML 2021。
- 锚点:
  - GitHub README TL;DR: trainable encoder + differentiable A* module。
  - `astar.py#L105-L153`: encoder 输出 cost map。
  - `astar.py#L182-L213`: forward 中执行 A*。
- 对本项目的作用:
  - 作为 related work: learning to guide search。
- 不能外推:
  - 不生成 Ackermann/Reeds-Shepp style analytic edge。

## C003b: LoHA*/SLOPE 属于 search guidance / node pruning

- 来源:
  - LoHA*: arXiv 2303.09477v2。
  - SLOPE: arXiv 2406.04935。
- 锚点:
  - LoHA* lines 84-88: learned local heuristic 用于 focal search, 并在 non-holonomic car state/action 设置下实验。
  - SLOPE lines 100-129: supervised learning 生成 search pruning function。
- 对本项目的作用:
  - 作为 related work: learning to guide/prune search。
- 不能外推:
  - 它们不负责从当前 node 生成到 goal 的连续 analytic connector。

## C004: Karl Kurzer path_planner 支持 shot 成功即返回、失败继续扩展的工程语义

- 来源: karlkurzer/path_planner。
- 锚点:
  - `src/algorithm.cpp#L165-L173`: Dubins shot success returns solution。
  - `src/algorithm.cpp#L176-L223`: otherwise expand successors。
- 对本项目的作用:
  - 支持本项目保持 fallback 语义: RL operator 失败必须返回 None。
- 不能外推:
  - 它不包含 RL。

## C005: Learned local connectors exist in SBP/RRT literature, but not as HA* analytic shot replacement

- 来源:
  - S3F, Atreya & Biswas 2022。
  - RL-RRT, Chiang et al. 2019。
  - Learned Goal-Reaching Controllers, Sivaramakrishnan et al. 2021。
  - DiTree, Hassidof et al. 2025。
- 锚点:
  - S3F local PDF lines 81-100: steering function `S(xa, xb)` connects sampled states; exact steering often requires expensive NLP, S3F learns this function。
  - S3F lines 233-272: S3F-RRT* uses learned steering function, then obstacle-free validation。
  - RL-RRT lines 99-120: trains obstacle-avoiding P2P RL policy and reachability estimator, then uses the policy as local planner in RRT。
  - Learned Goal-Reaching Controllers lines 66-91, 119-146: node expansion generates local goal, learned controller outputs control, planner propagates and validates。
  - DiTree lines 196-275: diffusion policy samples action sequence inside sampling-based tree search and accepts branches after collision checking。
- 对本项目的作用:
  - 不能说 "learned local connector 没有人做过"。
  - 可以说 "learned local connector exists for SBP/RRT-style kinodynamic planning, but public evidence does not show this exact HA* analytic-expansion / terminal-RS-certified slot."。
  - ForestNav 的 novelty 应收窄到 Hybrid A* analytic expansion slot、terminal RS certificate、failure fallback 和 full telemetry/cost accounting。
- 不能外推:
  - 这些论文不是 ForestNav 森林地图结果。
  - 它们不是直接替换 `HybridAStarPlanner._try_analytic_expansion()` 的实现。
  - DiTree 等无明确 GitHub license 的代码不能复制。

## C006: MPNet-family and MPT are related, but mainly whole-planner or search-guidance methods

- 来源:
  - MPNet, Qureshi et al. 2019。
  - Dynamic MPNet, Johnson et al. 2020。
  - MPC-MPNet, Li et al. 2021。
  - Motion Planning Transformers, Johnson et al. 2022。
- 锚点:
  - MPNet local PDF lines 136-173, 195-226: neural bidirectional path generation and neural/hybrid replanning。
  - Dynamic MPNet lines 87-105: local neural planner in hierarchical navigation; lines 193-211: Dubins model/curves used for steering。
  - MPC-MPNet lines 128-180, 241-281: neural generator proposes waypoints, MPC performs local steering and tree/path expansion。
  - MPT lines 123-133, 195-214: transformer predicts path-relevant patches/search mask; classical planners search the mask。
- 对本项目的作用:
  - Related work 可放在 "learning-guided planning / neural local planning"。
  - Dynamic MPNet/MPC-MPNet 可给 non-holonomic learned planning 背景。
- 不能外推:
  - MPNet-family/MPT 不能被写成 HA* analytic connector replacement。
  - Dynamic MPNet 的 ROS local planner不是本项目的 planner-internal analytic slot。

## C007: 代码复用 claim 必须带许可证边界

- 来源:
  - `0_trials/module2_rl_rs_evidence/license_audit.md`
  - GitHub raw license/API checks on 2026-07-04。
- 可写:
  - Permissively licensed codebases were used only as implementation references where technically appropriate。
  - GPL-3.0/no-license repositories were treated as related work or clean-room design inspiration, not copied implementation。
- 不能外推:
  - 不能写 "public GitHub implementation was reused" 而不列许可证、commit 和 reuse scope。
  - 不能把 GPL/no-license code 作为 ForestNav core 的实现来源。
  - 不能把许可证允许复制的 search-guidance/whole-planner code 写成同槽 analytic connector。
