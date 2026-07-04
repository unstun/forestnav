---
origin: ai+web+local
reviewed: false
created: 2026-07-03
topic: module2 RL-RS evidence source index
---

# 模块2 RL 替换 RS 证据索引

> 用途: 只保存已打开核验过的来源。搜索结果不能直接进入本表。

## 证据等级

| 等级 | 含义 | 可用场景 |
|---|---|---|
| A | 原文/代码已打开, 有行号或 section | 可进入设计依据 |
| B | 原文已打开, 但只有 section/table, 无行号 | 可进入设计线索, 写论文前需复核 |
| C | 搜索结果或二手摘要 | 只能作为后续检索入口 |
| X | 已证伪或与本任务不相干 | 只能写 negative result |

## 已核验来源

| ID | 等级 | 类型 | 来源 | 已核验锚点 | 当前用途 |
|---|---|---|---|---|---|
| S001 | A | paper | Dang et al. 2022, Improved Analytic Expansions in Hybrid A-Star Path Planning for Non-Holonomic Robots | MDPI HTML lines 330-337, 380-402, 414-419, 433-435; ResearchGate full-text lines 556-621, 758-867, 887-900, 935-960, 1082-1086, 1109-1174 | 证明 RS analytic expansion 的问题与 Dang-style multi-curvature RS baseline; 同时固定本地实现的 Eq.2 偏离 |
| S002 | A | paper | HOPE arXiv 2405.20579 | arXiv HTML lines 39-41, 113-172, 173-200, 247-267, 293-339, 340-353 | 证明 RL+RS parking planner 是强相关竞品, 但方法层级是 hybrid policy |
| S003 | A | code | jiamiya/HOPE@2accab93e8602bd7dac780078a012574cc2cb4d7 | `parking_agent.py#L2-L95`, `train_HOPE_ppo.py#L100-L208`, `car_parking_base.py#L84-L87`, `#L186-L299`, `#L413-L450`, `action_mask.py#L8-L227`, `eval_mix_scene.py#L82-L115`, `eval_utils.py#L31-L84` | 证明 HOPE 是 RL agent 与 RS planner 执行层融合, 不是 HA* analytic slot replacement |
| S004 | A | code | omron-sinicx/neural-astar | `src/neural_astar/planner/astar.py#L105-L153`, `#L182-L213` | 证明 Neural A* 是 learned cost/search guidance |
| S005 | A | code | AtsushiSakai/PythonRobotics ReedsSheppPath | `PathPlanning/ReedsSheppPath/reeds_shepp_path_planning.py#L22-L37` | RS path data structure reference |
| S006 | A | code | karlkurzer/path_planner | `src/algorithm.cpp#L165-L223` | Hybrid A* shot/fallback control-flow reference |
| S007 | A | paper | Dolgov et al. 2010, Path Planning for Autonomous Vehicles in Unknown Semi-structured Environments | PDF lines 244-272 | 原始 Hybrid A* analytic expansion 定义 |
| S008 | A | paper | Reeds and Shepp 1990, Optimal Paths for a Car That Goes Both Forwards and Backwards | PDF lines 107-143 | RS 最短路径族与倒车/cusp 理论来源 |
| S009 | A | docs | MATLAB `plannerHybridAStar` | docs lines 171-177, 184-193 | 工程接口中 analytic expansion/RS/Dubins 定义 |
| S010 | A | paper | Adapting Reinforcement Learning for Path Planning in Constrained Parking Scenarios | arXiv HTML lines 86-88, 125-130, 154-162, 166-190, 309-369 | RL drop-in replacement for whole HA* module, not internal RS slot |
| S011 | A | paper | LoHA*: Learning Local Heuristics for Search-Based Navigation Planning | arXiv HTML lines 84-88 | learned heuristic / focal search, not analytic connector |
| S012 | A | paper | SLOPE: Search with Learned Optimal Pruning-based Expansion | arXiv HTML lines 100-129 | learned pruning / node expansion, not analytic connector |
| L001 | A | local | ForestNav HybridAStarPlanner | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:204-245`, `:454-500` | 本项目真实插入点 |
| L002 | A | local | ForestNav collision checkers | `2_experiment/forest_n3p/third_party/pathplan/geometry.py:398-425`, `:449-518` | 训练/推理碰撞语义统一 |
| L003 | A | local | ForestNav evaluation | `2_experiment/forest_n3p/evaluation.py:39-84`, `:216-260` | 主实验指标地基 |

## 待核验来源

| ID | 类型 | 查询入口 | 需要核验的问题 |
|---|---|---|---|
| T001 | paper/code | learned steering function motion planning | 是否存在直接替换 goal shot / analytic connector 的学习方法 |
| T002 | paper | Adapting Reinforcement Learning for Path Planning in Constrained Environments | 是 RL planner 对比 Hybrid A*, 还是嵌入 HA* 内部 |
| T003 | paper | Hybrid Motion Planning with Deep Reinforcement Learning | 是否含 graph global search + DRL local planner, 与本任务的差异 |
| T004 | paper/code | PAIR Hybrid A* PPO Path Planner | 是否仅 2D waypoint offset, 是否无 Reeds-Shepp / non-holonomic |
| T005 | code | pkicki/neural_path_planning | 无许可证时是否只能作为概念线索 |
