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
| S013 | A | paper | Atreya & Biswas 2022, State Supervised Steering Function for Sampling-based Kinodynamic Planning | local PDF `1_survey/papers/pdf/Atreya2022S3F.pdf`, pdftotext lines 9-33, 81-100, 233-272, 317-320 | learned steering function for RRT*, strong adjacent positive |
| S014 | A | paper | Chiang et al. 2019, RL-RRT | local PDF `1_survey/papers/pdf/Chiang2019RLRRT.pdf`, lines 18-40, 99-120, 131-180, 198-208 | RL policy as RRT local planner + reachability estimator |
| S015 | A | paper | Sivaramakrishnan et al. 2021, Learned Goal-Reaching Controllers | local PDF `1_survey/papers/pdf/Sivaramakrishnan2021LearnedGoalReachingControllers.pdf`, lines 7-32, 66-91, 119-146, 276-283, 315-328 | learned local goal controller inside sampling-based expansion |
| S016 | A | paper | Hassidof et al. 2025, Diffusion Tree / DiTree | local PDF `1_survey/papers/pdf/Hassidof2025DiTree.pdf`, lines 6-35, 196-275, 287-334, 448-462 | diffusion action sampler inside RRT-style kinodynamic planner |
| S017 | A | paper | Johnson et al. 2020, Dynamic MPNet | local PDF `1_survey/papers/pdf/Johnson2020DynamicMPNet.pdf`, lines 16-25, 87-105, 138-183, 193-211 | non-holonomic neural local planner / Dubins steering, not HA* shot |
| S018 | A | paper | Li et al. 2021, MPC-MPNet | local PDF `1_survey/papers/pdf/Li2021MPCMPNet.pdf`, lines 20-31, 48-55, 103-109, 128-180, 241-281 | neural waypoint generator + MPC local steering |
| S019 | A | paper | Johnson et al. 2022, Motion Planning Transformers | local PDF `1_survey/papers/pdf/Johnson2022MotionPlanningTransformers.pdf`, lines 9-31, 123-133, 195-214, 362-372 | learned search-space restriction, not connector |
| S020 | A | paper | Qureshi et al. 2019, MPNet | local PDF `1_survey/papers/pdf/Qureshi2019MPNet.pdf`, lines 16-27, 136-173, 195-226, 272-306 | whole neural planner / replanning baseline |
| S021 | A | code | sldai/crl_kino | GitHub API license MIT; `crl_kino/planner/rrt_rl.py#L14-L63`, `rrt_rl_estimator.py#L16-L122`, `policy/rl_policy.py#L18-L39`, `#L83-L109` | open-source RL local planner inside RRT; dynamics mismatch |
| S022 | A | code | MRSTechnion/DiTree | GitHub API no license; `planners/RRT.py#L42-L122`, `policies/fm_policy.py#L53-L212` | diffusion action sampler inside RRT-style planner; license blocked |
| S023 | A | code | ahq1993/MPNet | GitHub API license MIT; `MPNet/neuralplanner.py#L40-L86`, `#L147-L235`, `#L283-L338` | neural planner/replanning code; geometric, not HA* analytic slot |
| S024 | A | code | ucsdarclab/mpnet_local_planner | GitHub API no license; `src/mpnet_plan.cpp#L244-L264`, `#L286-L383`, `#L385-L424` | Dynamic MPNet ROS local planner; license blocked |
| S025 | A | code | ucsdarclab/motion_planning_transformer | GitHub API no license; `eval_model_car.py#L128-L208`, `#L220-L343`, `transformer/Models.py#L89-L164` | learned search mask / MPT code; not connector |
| S026 | A | code | tedhuang96/nirrt_star | GitHub API license MIT; `nirrt_star_png_2d.py#L56-L175`, `train_pointnet_pointnet2.py#L15-L18`, `#L82-L108`, `#L153-L190` | learned sampling distribution, not connector |
| S027 | A | code | mihdalal/neuralmotionplanner | GitHub API no license; `neural_motion_planner.py#L20-L68`, `#L209-L324`, `#L326-L420` | manipulator reactive planner; license blocked |
| S028 | A | docs | GitHub Docs, Licensing a repository | `https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository`, lines 161, 176-179, 240-242 | Project policy for no-license public repositories: do not copy/vendor code |
| S029 | A | code-license | jiamiya/HOPE | GitHub API `license.spdx_id=GPL-3.0`; `LICENSE#L1-L2` | GPL-3.0: idea-only for ForestNav core |
| S030 | A | code-license | karlkurzer/path_planner | GitHub API `BSD-3-Clause`; `LICENSE.txt#L1-L18` | Permissive reference for Hybrid A* shot/fallback control flow |
| S031 | A | code-license | AtsushiSakai/PythonRobotics | GitHub API `NOASSERTION/Other`; raw `LICENSE#L1-L14` is MIT text | Permissive reference, but record SPDX caveat |
| S032 | A | code-license | omron-sinicx/neural-astar | GitHub API `NOASSERTION/Other`; raw `LICENSE#L1-L17` is MIT text | Permissive search-guidance reference, not connector |
| S033 | A | code-license | sldai/crl_kino, ahq1993/MPNet, tedhuang96/nirrt_star, reiniscimurs/DRL-robot-navigation | GitHub API MIT; raw `LICENSE#L1-L13` checked for each repo | Permissive code sources, subject to technical-slot mismatch |
| S034 | A | code-license | MRSTechnion/DiTree, ucsdarclab/mpnet_local_planner, ucsdarclab/motion_planning_transformer, mihdalal/neuralmotionplanner, pkicki/neural_path_planning | GitHub API license endpoint 404; root raw `LICENSE`/`LICENSE.txt` 404 | No code copy/vendor/line-by-line porting |
| S035 | A | local-report | A01.5 license audit | `0_trials/module2_rl_rs_evidence/license_audit.md` | Three-tier code reuse decision: copyable / idea-only / not usable |
| L001 | A | local | ForestNav HybridAStarPlanner | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:204-245`, `:454-500` | 本项目真实插入点 |
| L002 | A | local | ForestNav collision checkers | `2_experiment/forest_n3p/third_party/pathplan/geometry.py:398-425`, `:449-518` | 训练/推理碰撞语义统一 |
| L003 | A | local | ForestNav evaluation | `2_experiment/forest_n3p/evaluation.py:39-84`, `:216-260` | 主实验指标地基 |
| L004 | A | local | ForestNav collision protocol audit | `0_trials/module2_rl_rs_evidence/collision_checker_unification.md`; `geometry.py:262-416`, `:419-518`; `rl_rs/env.py:86-92`, `:191-222`; `rl_rs/rollout.py:42-56`; `rl_rs/terminal.py:44-50`; `rl_rs/operator.py:133-162` | A02.2 训练/推理共享碰撞语义方案 |
| L005 | A | local | ForestNav evaluation telemetry gap audit | `0_trials/module2_rl_rs_evidence/evaluation_telemetry_gap.md`; `evaluation.py:62-103`, `:238-303`, `:336-409`, `:437-477`; `planner.py:680-831`, `:873-967`; `rl_rs/telemetry.py:6-66`; `rl_rs/operator.py:31-44`, `:76-80` | A02.3 records.csv / summary / telemetry 字段缺口清单 |

## 待核验来源

| ID | 类型 | 查询入口 | 需要核验的问题 |
|---|---|---|---|
| T001 | paper/code | learned steering function motion planning | A01.4 已核验: 存在 SBP/RRT learned steering/local planner, 未发现直接 HA* analytic-shot 替换 |
| T002 | paper | Adapting Reinforcement Learning for Path Planning in Constrained Environments | 是 RL planner 对比 Hybrid A*, 还是嵌入 HA* 内部 |
| T003 | paper | Hybrid Motion Planning with Deep Reinforcement Learning | 是否含 graph global search + DRL local planner, 与本任务的差异 |
| T004 | paper/code | PAIR Hybrid A* PPO Path Planner | 是否仅 2D waypoint offset, 是否无 Reeds-Shepp / non-holonomic |
| T005 | code | pkicki/neural_path_planning | 无许可证时是否只能作为概念线索 |
