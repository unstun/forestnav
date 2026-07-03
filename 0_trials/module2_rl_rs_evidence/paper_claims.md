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
  - MDPI HTML lines 334-337: 摘要说明 RS curve 在 analytic expansion phase 提高 accuracy/speed, 但 corner 附近可能贴障碍。
  - lines 347: Hybrid A* 包含 forward search 和 analytic expansion。
  - lines 368-371: analytic expansion 用 RS 到达 exact continuous goal, 发明者声称有 accuracy/search speed benefit。
  - lines 433-434: 论文方法是在 analytic expansion phase 改进 safety。
- 对本项目的作用:
  - 可作为问题动机。
  - 可作为 strong classical baseline。
- 不能外推:
  - Dang 只在 RS 曲率集合里选 safer route, 不等于 learned obstacle-aware rollout。

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
  - arXiv HTML lines 357-360: 论文声称构造 normal/complex/extreme 场景, 对比 Hybrid A*、naive PPO、SAC, 并称 rule-based + learning-based 组合有泛化能力。
  - GitHub README lines 237-238: 仓库称 planner integrates RL agent with Reeds-Shepp curves。
- 对本项目的作用:
  - 证明 reviewer 可能会问 RL+RS/HOPE 差异。
  - 可借鉴 RS-distance reward、action mask、curriculum。
- 不能外推:
  - HOPE 不是 HA* analytic expansion operator replacement。
  - HOPE 代码 GPL-3.0, 不能直接复制。

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
