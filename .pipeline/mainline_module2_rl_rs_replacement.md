---
status: active
origin: ai+web+local
reviewed: false
created: 2026-07-03
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
base_commit: 640c76bf
---

# 模块2主线: RL 替换 RS 解析扩展的论文级最大实现任务书

> 执行原则: 本文件是长期任务索引。每次会话只做第一项未完成任务。
> 完成一个有意义变更后更新本文件的状态记录, 再 git commit。

## 0. 直观结论

这条线不是把 PPO 接到现有 F-N3P 外面跑一个 demo。真正目标是:

1. 在 Hybrid A* 的 analytic expansion 槽位里, 用一个闭环 RL steering policy 生成可碰撞验证的局部连接轨迹。
2. policy 只在 RS shot 容易失败、但搜索树已经接近目标的区间出手。
3. policy 末端仍切回 RS, 用 RS 负责最后几厘米/几度的数学贴合。
4. 失败必须回落到原始基元扩展, 不能破坏 Hybrid A* 的兜底语义。
5. 所有时间统计必须包含神经网络前向、rollout、RS 收尾和碰撞检测, 不能把开销藏起来。

换句话说, 这是一个 "HA* 主导 + RL 解析算子" 的系统, 不是 "RL planner 加一点 RS"。

## 1. 信任边界

### 1.1 已批准但仍需证据化执行

- Contract 已存在且 status=approved: `.pipeline/contracts/module2-ppo-funnel-expansion.md:1-8`。
- Contract 定义的核心结构是 "中长距 PPO rollout + 最后 1-2m RS 收尾": `.pipeline/contracts/module2-ppo-funnel-expansion.md:10-17`。
- 成功信号是节点数、端到端时间、超时失败率同时改善: `.pipeline/contracts/module2-ppo-funnel-expansion.md:19-32`。
- 失败信号是计算账、oracle 无解、末端 RS 对接灾难、PPO 不收敛四个独立 gate: `.pipeline/contracts/module2-ppo-funnel-expansion.md:34-39`。
- Contract 明确要求先修计时口径: `.pipeline/contracts/module2-ppo-funnel-expansion.md:41-45`。

### 1.2 只能作为线索, 不能直接当论文依据

- 设计文档标记为 `reviewed:false` 且 `confidence: low`: `.pipeline/survey/module2-ppo-analytic-expansion-design.md:1-15`。
- 设计文档里的 "解析扩展槽" 和 "闭环 policy" 方向有 Dr Sun 拍板记录, 但仍需要代码和实验验证: `.pipeline/survey/module2-ppo-analytic-expansion-design.md:19-27`。
- 外部仓库 README 只能证明仓库声称什么, 不能证明算法可复用。任何 GitHub 依据必须读到训练脚本、环境、动作、观测、碰撞和评测代码。

### 1.3 本文件的证据规则

每个任务必须记录四类证据:

| 证据类型 | 最低要求 | 不合格例子 |
|---|---|---|
| 本地代码证据 | 文件路径 + 行号 + 相关符号 | "看起来在 planner 里" |
| 外部论文证据 | URL + section/algorithm/line | "论文摘要说有效" |
| 外部代码证据 | 仓库 URL + license + 文件路径 + 行号 | "README 说开源" |
| 验证证据 | 可复跑命令 + stdout/stderr/artifact 路径 | "应该能跑" |

## 2. 当前本地代码事实

### 2.1 当前 Hybrid A* 的 analytic expansion 插入点

- `HybridAStarPlanner._analytic_interval()` 按距离调整解析扩展触发频率: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:197-202`。
- `_try_analytic_expansion()` 当前实现是 Dang 2022 风格多曲率 RS 扫描: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:204-245`。
- 多曲率候选调用 `_try_rs_with_radius()` 生成 RS, 逐段采样并碰撞检测: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:282-340`。
- 主循环在 `expansion_idx % interval == 0` 时尝试 analytic expansion, 成功后立即拼接尾段并返回: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:454-473`。
- 失败时落回普通运动基元扩展: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:476-500`。

设计含义:

- 真实改动点是 `_try_analytic_expansion()` 的职责, 不是单独写一个离线 RL planner。
- 新 RL operator 必须返回 `List[AckermannState], List[MotionPrimitive]` 或等价结构, 否则不能无缝接入 `_trace_path()` 和 evaluation。
- rollout 失败必须返回 `None`, 保持主循环自然进入基元扩展。

### 2.2 当前运动学和碰撞语义

- Ackermann 参数给定 `wheelbase=0.6`, `min_turn_radius=1.1284`: `2_experiment/forest_n3p/third_party/pathplan/robot.py:8-16`。
- `propagate()` 使用恒曲率圆弧解析积分, 不是欧拉直线近似: `2_experiment/forest_n3p/third_party/pathplan/robot.py:29-54`。
- `sample_constant_steer_motion()` 按固定步长采样弧线, 用于碰撞检测和可视化: `2_experiment/forest_n3p/third_party/pathplan/robot.py:77-113`。
- `GridFootprintChecker.collides_path()` 逐 pose 检查碰撞: `2_experiment/forest_n3p/third_party/pathplan/geometry.py:398-406`。
- `EDTCollisionChecker` 使用 EDT + two-circle footprint, 注释写明与 DRL 环境 collision detection 对齐: `2_experiment/forest_n3p/third_party/pathplan/geometry.py:419-425`。
- EDT checker 的边界距离也并入碰撞语义, 出界等价于危险: `2_experiment/forest_n3p/third_party/pathplan/geometry.py:449-458`。

设计含义:

- RL 训练环境不能另写一套碰撞语义。训练、gate、planner 插件必须共享同一个 footprint/EDT/Grid checker。
- 动作空间建议先表达为连续曲率或转向角, 再调用 `propagate()` 或 `sample_constant_steer_motion()` 形成 planner 可解释的弧段。
- 如果训练时用 EDT checker, 推理时也要用 EDT 或明确记录 checker 差异, 否则 deployment distribution 不一致。

### 2.3 当前 F-N3P 外层推理循环

- `run_forest_n3p()` 当前先尝试 direct RS 到 final goal: `2_experiment/forest_n3p/inference.py:470-505`。
- 当前 KNN/MLP predictor 输出 subgoal, 再用 RS 验证 subgoal 可达: `2_experiment/forest_n3p/inference.py:507-525`。
- 若没有可达 prediction, 进入 F2/F3 回退: `2_experiment/forest_n3p/inference.py:527-626`。
- 若 `commit_verified_rs_segments=True`, 直接提交已验证 RS segment: `2_experiment/forest_n3p/inference.py:627-647`。
- 计时口径中间态已把 direct RS 和 verified RS 的 step wall-clock 计入 `planner_time_s`: `2_experiment/forest_n3p/inference.py:470-487`, `2_experiment/forest_n3p/inference.py:627-643`。

设计含义:

- F-N3P 是已有学习式 subgoal 分解, 不是本模块2的最终形态。
- 模块2不能只复用 `run_forest_n3p()` 外层循环然后声称替换 RS。论文级实现必须进入 Hybrid A* analytic expansion 槽位。
- `inference.py` 的计时修正仍有价值, 因为 evaluation 也要覆盖 F-N3P / baseline 对照。

### 2.4 当前数据和评测基础

- 训练数据配置已有 2000 maps、40 queries/map、100k 样本目标: `2_experiment/forest_n3p/training_data.py:41-68`。
- 难度 profile 已按 Easy/Complex/Extreme 分桶: `2_experiment/forest_n3p/training_data.py:200-209`。
- 程序化森林生成入口是 `generate_forest_grid()`: `2_experiment/forest_n3p/maps/forest.py:494-540`。
- evaluation 已记录 success、feasible、time、expansions、path inflation、curvature、clearance、collision 等字段: `2_experiment/forest_n3p/evaluation.py:39-84`。
- evaluation 已有 path densify + collision count + path quality 计算入口: `2_experiment/forest_n3p/evaluation.py:216-260`。

设计含义:

- 不要另起一个不可比较的数据/评测协议。
- RL 训练可以复用 map/query generation, 但 label 目标要从 "subgoal imitation" 变成 "RS-connectable terminal set"。
- 论文表格可以沿用现有 evaluation 字段, 但需要补 analytic expansion 细粒度 telemetry。

## 3. 外部证据矩阵

### 3.1 Hybrid A* analytic expansion 的问题是真问题

Dang et al. 2022 明确把 Hybrid A* 分成 forward search 和 analytic expansion 两阶段, 并指出 RS curve 在 analytic expansion 中提高准确性和速度, 但在角落/障碍附近可能贴障碍:

- MDPI HTML lines 330-337: https://www.mdpi.com/2076-3417/12/12/5999
- 原 RS path 贴墙/角落风险与 Section 3 改进目标: MDPI lines 380-402: https://www.mdpi.com/2076-3417/12/12/5999
- Eq.2 Voronoi field: ResearchGate full-text lines 556-621, 包含 nearest-obstacle distance `d0` 与 generalized Voronoi edge distance `dv`: https://www.researchgate.net/publication/361291293_Improved_Analytic_Expansions_in_Hybrid_A-Star_Path_Planning_for_Non-Holonomic_Robots
- Eq.3/Eq.4 cost: ResearchGate lines 758-844, `v` 为 risk cost, `m` 包含 path length / steering angle / steer switching。
- Table 1/2 和结论: MDPI lines 414-419, 433-435; ResearchGate lines 935-960, 1082-1086, 1109-1174。

可用结论:

- "RS analytic expansion 快但无视障碍/可能贴障碍" 是可引用问题。
- Dang 2022 是直接相邻 baseline, 但它仍在 RS 家族内多曲率选优, 没有学习闭环避障 steering policy。
- 本地实现应称为 Dang-style baseline: 当前 `planner.py` 匹配 multi-curvature RS + collision filtering + lowest-cost selection + fallback 语义, 但 Eq.2 risk 用 mean EDT clearance inverse 近似, 没有 generalized Voronoi edge distance `dv`。

### 3.2 HOPE 是强相关竞品, 但不是同一个插槽

HOPE 论文/仓库声称 RL 与 RS 结合, 并与 Hybrid A*、naive PPO/SAC 比较。A01.2 已深读到论文 method/experiment/ablation/cost 和代码 training/env/action-mask/eval, 固定代码版本 `jiamiya/HOPE@2accab93e8602bd7dac780078a012574cc2cb4d7`:

- arXiv HTML lines 39-41: 摘要定位为 parking planner, integrates RL agent with Reeds-Shepp curves, 并使用 action mask: https://arxiv.org/html/2405.20579v1
- arXiv HTML lines 113-172: 方法是 RL policy 与 RS policy 的 hybrid action choice, RS 只在接近目标且存在 collision-free RS curve 时激活。
- arXiv HTML lines 173-200: action mask 估计给定 steering 下最大 safe step velocity。
- arXiv HTML lines 247-267, 293-339, 340-353: success table、compute cost、RS/action-mask/curriculum ablation。
- 训练入口包括 PPO 和 SAC: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/train/train_HOPE_ppo.py#L100-L208`, `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/train/train_HOPE_sac.py#L155-L213`
- `ParkingAgent` 在执行 RS 路径时直接由 `RsPlanner` 输出动作, 否则走 RL agent: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/model/agent/parking_agent.py#L49-L95`
- `RsPlanner.set_rs_path()` 把 RS ctypes/lengths 转成动作序列: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/model/agent/parking_agent.py#L2-L47`
- 环境动作是 `[steer, speed]`, kinematic single-track model step 更新状态: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/env/car_parking_base.py#L84-L87`, `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/env/vehicle.py#L69-L96`
- 环境 reward 里包含 RS distance reward, 且 `path_to_dest` 由 env 在 RS 可行时写入: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/env/car_parking_base.py#L186-L299`
- Action mask 预计算 safe step 并影响 action sampling: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/model/action_mask.py#L8-L227`
- Evaluation 是 scenario-level policy rollout, 记录 success/reward/step/path length: `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/evaluation/eval_mix_scene.py#L82-L115`, `https://github.com/jiamiya/HOPE/blob/2accab93e8602bd7dac780078a012574cc2cb4d7/src/evaluation/eval_utils.py#L31-L84`
- license: GPL-3.0, 不能直接复制进本项目核心代码, 只能概念借鉴或隔离参考。

可用结论:

- HOPE 支持 "RL+RS 组合比 naive RL 更稳" 这个方向。
- HOPE 不是替换 Hybrid A* 内部 analytic expansion。它是 parking env 中 RL agent 和 RS planner 的融合执行。
- 可借鉴: action mask/safe-action prior, scene curriculum, RS distance shaping, RS action decomposition, RS/action-mask/curriculum ablation, compute accounting。
- 不可直接复用: GPL 代码、停车场地图/状态定义、端到端 agent 结构。

### 3.3 Neural A* 是 learned search guidance, 不是 analytic operator replacement

- Neural A* README 说它是 trainable encoder + differentiable A* module, 学习 search optimality/efficiency trade-off: https://github.com/omron-sinicx/neural-astar
- 代码 `NeuralAstar` 先 encode cost map, 再执行 differentiable A*: `https://github.com/omron-sinicx/neural-astar/blob/minimal/src/neural_astar/planner/astar.py#L105-L153`, `https://github.com/omron-sinicx/neural-astar/blob/minimal/src/neural_astar/planner/astar.py#L182-L213`
- license API 未给出 SPDX, 使用前必须人工确认。

可用结论:

- Neural A* 是模块1/learned heuristic/node expansion 的相关工作。
- 它不能证明 "learning policy 生成 analytic expansion edge" 已经被做掉。

### 3.4 PythonRobotics 和 Karl Kurzer 只能作工程参考

- PythonRobotics Reeds-Shepp 示例定义 Path.lengths/ctypes/directions: `https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/ReedsSheppPath/reeds_shepp_path_planning.py#L22-L37`
- PythonRobotics 是教学实现, API/许可需要单独确认, 不作为本项目生产依赖。
- Karl Kurzer path_planner 是 BSD-3-Clause, 可作为 Hybrid A* 工程参考。
- Karl Kurzer `Algorithm::hybridAStar()` 在节点 in range 时执行 `dubinsShot`, 成功直接返回: `https://github.com/karlkurzer/path_planner/blob/master/src/algorithm.cpp#L165-L173`
- Karl Kurzer 普通 successor expansion 紧随其后: `https://github.com/karlkurzer/path_planner/blob/master/src/algorithm.cpp#L176-L223`

可用结论:

- 这些仓库可以帮助审查本项目 Hybrid A* 插槽语义是否合理。
- 它们不能直接提供 RL 替换方案。

## 4. 禁止的假实现

| 假实现 | 为什么是假 | 允许替代 |
|---|---|---|
| 只训练一个 policy 从 start 走到 goal, 不接入 `_try_analytic_expansion()` | 这是独立 RL planner, 不是替换 RS analytic expansion | 接入 `HybridAStarPlanner` 的 analytic operator, 失败返回 None |
| 用 MLP 一次输出 subgoal, 再用 RS 连接 | 这是现有 F-N3P/KNN/MLP 范式, 不是闭环 RL steering | 每步局部观测, 每步输出曲率/steer, 虚拟 rollout |
| reward 只写距离目标变近 | 会贴树/撞障碍/打转, 无法支撑路径质量 claim | success set + collision + clearance + curvature-rate + length + timeout |
| 训练和推理用不同碰撞 checker | deployment distribution 不一致, 实验数字不可解释 | 共享 EDT/Grid footprint checker, 差异必须写入 metadata |
| 只报成功率不报时间 | Contract 成功判据包含端到端时间 | 报 wall-clock, node expansions, policy calls, NN forward, collision checks |
| 单一 seed 或单一地图出图 | 不能支撑论文 | 多 seed, Complex/Extreme, held-out procedural, real SLAM map |
| 失败后偷偷换 warm-start 或换任务定义 | 违反预注册 | 失败按 gate 收口, 需要 v2 contract 才改定义 |

## 5. 最大实现分解

状态符号:

- `[ ]` 未开始
- `[>]` 正在执行
- `[x]` 已完成
- `[?]` 等 Dr Sun 或外部条件
- `[!]` 失败或证伪, 需写原因

### Phase A: 证据硬化和任务地基

#### A00. 工作区保护与当前状态对齐

- [x] A00.1 备份本会话前相关 dirty diff。
  - 产出: commit `640c76bf 备份：模块2解析扩展分析与计时口径中间态`
  - 包含: `2_experiment/forest_n3p/inference.py`, `0_trials/hybrid_astar_code_analysis.md`, `0_trials/hybrid_astar_code_analysis.html`
- [?] A00.2 刷新热区, 关闭 "Contract 未起草" 旧状态。
  - 输入: memory-retriever 结果显示热区过期。
  - 验证: `bigmemory/热区/状态简报.md` 不再声称 module2 contract 未起草。
  - 注意: 需要走项目 archive/sync 规则, 不在本文件中手改热区。
  - 当前状态: `source-command-sync` skill 要求中途 AskUserQuestion 确认遗漏进展。为避免本 goal 停住, 暂挂到本轮归档/同步阶段处理。

#### A01. 外部证据审计

- [x] A01.1 建立 `0_trials/module2_rl_rs_evidence/` 证据目录。
  - 文件: `sources.md`, `github_repos.md`, `paper_claims.md`, `negative_results.md`
  - 每条证据必须有 URL、行号/section、trust label。
  - 验证: 所有 URL 至少打开一次; 403/付费墙标为 blocked。
- [x] A01.2 深读 HOPE 论文和代码。
  - 必读: arXiv method/algorithm/experiment, `parking_agent.py`, `car_parking_base.py`, `vehicle.py`, `model/action_mask.py`, `train_HOPE_ppo.py`, `eval_mix_scene.py`
  - 输出: HOPE 与 ForestNav 插槽差异表。
  - 失败条件: 只读 README 即停止。
  - 已完成: 新增 `0_trials/module2_rl_rs_evidence/hope_deep_read.md`, 核验 HOPE 论文 method/experiment/ablation/cost 与 PPO/SAC train、ParkingAgent、CarParking env、Vehicle dynamics、ActionMask、eval code。
  - 判定: HOPE 是 parking Gym agent execution loop 里的 RL+RS hybrid policy; RS route 来自 env `path_to_dest` 并被 `ParkingAgent` 逐步执行。它不是 HA* open-list node 上的 analytic expansion replacement。
  - 可借鉴: action mask/safe-action prior、RS-distance reward、difficulty curriculum、RS hybrid ablation、成本拆分。
  - 禁止: 直接复制 GPL-3.0 代码; 将 HOPE success rate 当 ForestNav 森林结果; 声称 HOPE 已做掉本项目 analytic slot。
  - 记录: `.pipeline/experiments/20260704_module2_a01_2_hope_deep_read.md`。
- [x] A01.3 深读 Dang 2022 analytic expansion。
  - 必读: Section 2.1, Section 3, Eq.2-4, experiment table。
  - 输出: 本项目已有 Dang 多曲率实现与论文公式差异。
  - 验证: 对照 `planner.py:204-280` 写逐项匹配/偏离。
  - 已完成: 新增 `0_trials/module2_rl_rs_evidence/dang2022_deep_read.md`, 核验 MDPI HTML 与 ResearchGate full-text 中 Section 2.1、Section 3、Eq.2-4、Table 1/2、Conclusion。
  - 判定: Dang 是 correct-slot classical baseline, 不是 RL; 本地 `dang_multi_rs` 匹配 analytic slot、multi-radius RS、collision filter、cost selection、failure fallback, 但 Eq.2 用 mean EDT clearance inverse 近似, 缺 generalized Voronoi edge distance `dv`。
  - 记录: `.pipeline/experiments/20260704_module2_a01_3_dang2022_deep_read.md`。
- [x] A01.4 查 "learned connector / learned goal shot / neural steering function"。
  - 查询词: `learned steering function motion planning`, `goal connect neural motion planner`, `RL local connector Hybrid A*`, `Reeds-Shepp neural planner`
  - 输出: 正例、负例、未知项。
  - 判据: 至少 10 个来源, 其中论文 >=5, 代码仓库 >=3。
  - 已完成: 新增 `0_trials/module2_rl_rs_evidence/learned_connector_survey.md`, 核验 15 个来源, 其中论文 8 个、代码仓库 7 个。
  - 近正例: S3F、RL-RRT/`crl_kino`、Learned Goal-Reaching Controllers、DiTree 均证明 learned steering/local connector/action sampler 可以嵌入 SBP/RRT-style planner。
  - 负面边界: 未发现公开来源直接替换 Hybrid A* analytic expansion / RS shot 并保留 ForestNav fallback + terminal RS certificate 语义。
  - 记录: `.pipeline/experiments/20260704_module2_a01_4_learned_connector_survey.md`。
- [x] A01.5 许可证审计。
  - 输出: 可复制代码、只能读思想、不可用 三档。
  - 必查: HOPE GPL-3.0, Karl Kurzer BSD-3-Clause, PythonRobotics license, Neural A* license。
  - 已完成: 新增 `0_trials/module2_rl_rs_evidence/license_audit.md`, 核验 GitHub API、raw `LICENSE`/`LICENSE.txt`、root license missing 404、GitHub no-license policy docs。
  - 判定: 可复制代码包括 Karl Kurzer BSD-3-Clause、PythonRobotics raw MIT、Neural A* raw MIT、`crl_kino`/MPNet/NIRRT*/DRL-robot-navigation MIT, 但仍需技术适配审计。
  - 判定: HOPE GPL-3.0 只能读思想; DiTree/Dynamic MPNet local planner/MPT/NeuralMP/`pkicki/neural_path_planning` 无可用 license, 不复制代码。
  - 记录: `.pipeline/experiments/20260704_module2_a01_5_license_audit.md`。

#### A02. 本地代码审计

- [x] A02.1 形成 analytic expansion 插槽 API 设计备忘。
  - 输入: `planner.py:204-245`, `planner.py:454-500`, `robot.py:29-113`
  - 输出: `0_trials/module2_rl_rs_evidence/local_slot_api.md`
  - 必含: 输入状态、goal、map、footprint、params、返回 states/actions、failure reason。
- [ ] A02.2 形成 collision checker 统一备忘。
  - 输入: `geometry.py:262-406`, `geometry.py:419-518`
  - 输出: 训练/推理共享碰撞语义方案。
- [ ] A02.3 评估当前 evaluation 字段缺口。
  - 输入: `evaluation.py:39-84`, `evaluation.py:216-260`
  - 输出: 需要新增 telemetry 字段列表。
  - 必含: analytic_attempts, rs_attempts, rl_attempts, rl_successes, terminal_rs_successes, nn_forward_time_s, rollout_collision_checks, rollout_steps, fallback_to_primitives_count。

### Phase B: 诚实计时和基线可比性

#### B01. 固化 F-N3P 计时口径修正

- [x] B01.1 为 `inference.py` 计时修正补单元测试。
  - 测试点: direct RS、verified RS segment、segment planning overhead。
  - 验证命令: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q`
  - 通过标准: direct/verified RS 不再出现 `planner_time_s=0.0`, segment 分支把 prediction/RS 验证 overhead 与 planner 内部时间相加。
  - 产出: `2_experiment/forest_n3p/tests/test_inference_timing.py`
  - 当前验证: `3 passed in 0.85s`
- [x] B01.2 更新 evaluation metadata, 明确 total_time_s 与 planner_time_s 的关系。
  - 输出: `EvaluationRun.metadata["timing_protocol"]`
  - 目的: 防止后续论文表格混用 wall-clock 与 planner-internal time。
  - 实现位置: `2_experiment/forest_n3p/evaluation.py` 当前 HEAD 已写入 `timing_protocol`。
  - 本项新增验证: `2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py`
  - 当前验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `5 passed in 0.88s`
- [x] B01.3 跑 targeted smoke。
  - 数据: 3 个固定 seed 小地图, 每个 3 个 query。
  - 输出: `0_trials/module2_timing_smoke/`
  - 验证: stdout/stderr、CSV、manifest、当前 commit hash。
  - 失败预检: `0_trials/module2_timing_smoke/run_20260703_b01_3/`, 原因是 original T06 profiles 与 `D-T14-09=revise_to_validation_cutpoints` 冲突。
  - 通过运行: `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/`
  - 当前验证: `record_count=18`, `query_count=9`, `status=candidate_or_smoke`, `stderr.txt` 为空, `records.csv` 含 `timing_protocol` 与 `total_planner_time_s`。

#### B02. Vanilla HA* 与 Dang-RS baseline 拆分

- [x] B02.1 让 planner 可显式选择 analytic operator。
  - operator: `single_rs`, `dang_multi_rs`, `disabled`
  - 注意: 默认保持现状, 不破坏旧实验。
  - 验证: 三种 operator 在同一 query 上 telemetry 可区分。
  - 实现位置: `HybridAStarPlanner(..., analytic_operator=...)`, stats 字段 `analytic_operator` 当前 HEAD 已存在。
  - 本项新增验证: `2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py`
  - 当前验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `7 passed in 0.91s`
- [x] B02.2 单独记录 analytic expansion 尝试次数与成功次数。
  - 当前 stats 只有 `remediations` 和 expansions, 不够。
  - 新增 stats 字段必须由 tests 锁住。
  - 实现位置: planner stats 字段 `analytic_attempts`, `analytic_successes` 当前 HEAD 已存在。
  - 本项新增验证: 同一 query 的 disabled/single/dang 计数, 以及 analytic 失败时 `attempts=1`, `successes=0`。
  - 当前验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `8 passed in 0.97s`
- [x] B02.3 复跑小规模 baseline。
  - 方法: HA* no analytic, HA* single RS, HA* Dang multi-RS。
  - 输出: 证明 "RS slot 本身贡献多少", 否则 RL 改进无法归因。
  - 入口: `python -m forest_n3p.scripts.run_main_evaluation --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs`
  - v1 运行: `0_trials/module2_operator_baseline_smoke/run_20260703_b02_3/`, 暴露 records 缺 analytic attempt/success telemetry。
  - v2 通过: `0_trials/module2_operator_baseline_smoke/run_20260703_b02_3_v2/`, `record_count=27`, `query_count=9`, `stderr.txt` 为空。
  - telemetry: disabled `0/0`, single RS `2733/8`, Dang multi-RS `1504/8` analytic attempts/successes。
  - 边界: 这是 9-query smoke, 只证明归因入口和计数字段可用, 不是论文性能结论。

### Phase C: Oracle 形态分析 Gate #2

#### C01. 收集 RS 失败节点

- [x] C01.1 在 Complex/Extreme 查询中记录每次 analytic expansion 失败的 state。
  - 字段: query_id, expansion_idx, state, goal, h_holo, h_rs, nearest_obstacle, failure radius list。
  - 输出: `0_trials/module2_oracle_shape/rs_failure_nodes.parquet`
  - 产出: `2_experiment/forest_n3p/scripts/collect_rs_failure_nodes.py`, `0_trials/module2_oracle_shape/rs_failure_nodes.parquet`
  - 当前验证: Complex/Extreme 共 20 queries, raw failure rows `8752`, `stderr.txt` 为空。
- [x] C01.2 去重失败节点。
  - 方法: 按 `(query_id, grid cell, theta bin)` 去重。
  - 目的: 避免同一死点重复影响统计。
  - 产出: `2_experiment/forest_n3p/scripts/dedupe_rs_failure_nodes.py`, `0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet`
  - 当前验证: `8752 -> 7860`, dropped duplicates `892`, `stderr.txt` 为空。

#### C02. Oracle connector 可行性

- [x] C02.1 对每个 RS 失败节点跑局部/全图 HA* oracle。
  - oracle A: 当前 node 到 final goal, analytic disabled, 放宽 timeout/max_nodes。
  - oracle B: 当前 node 到若干中间可通行候选, 再 RS 到 goal。
  - 输出: 是否存在可行连接、连接长度、转向次数、最小 clearance。
  - 已完成: 新增 `2_experiment/forest_n3p/scripts/run_oracle_connector_analysis.py`。
  - Oracle B 候选源: `goal_annulus`, `corridor_offset`, `edt_high_clearance`, `voronoi_skeleton`。
  - Smoke 1: `0_trials/module2_oracle_shape/oracle_connector_results_smoke5.parquet`, Complex 前 5 个节点, A=5/5, B=5/5, stderr 空。
  - Smoke 2: `0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3.parquet`, Extreme 3 个节点, A=2/3, B=3/3, stderr 空。
  - 关键观察: `extreme_s00_q0001:150:45:26` 出现 A 失败但 B 成功, 说明中间候选 oracle 能捕捉非平凡连接形态。
  - 长跑执行层: 新增 `2_experiment/forest_n3p/scripts/run_oracle_connector_chunks.py`, 支持 chunk/resume/merge。
  - Runner smoke: `0_trials/module2_oracle_shape/oracle_connector_runner_smoke/`, 3 rows -> 2 chunks -> merged 3 rows, 所有 stderr 空。
  - Default-budget pilot: `0_trials/module2_oracle_shape/oracle_connector_default_budget_pilot20/`, 20 rows -> 2 chunks, A=20/20, B=20/20, 所有 stderr 空, 约 2 秒/行。
  - Full default-budget run: `0_trials/module2_oracle_shape/oracle_connector_full/summary.json`, 79 chunks, 7860/7860 rows, merged output `0_trials/module2_oracle_shape/oracle_connector_results.parquet`。
  - Full integrity: root `status=complete`, chunk four-file sets missing 0, nonzero chunk summaries 0, merged rows 7860, merged `source_head` 全部为 `1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5`。
  - Full counts: Oracle A success 6226, Oracle B success 6287, oracle connectable 6289, both success 6224, B-only 63, A-only 2, unresolved 1571。
  - Bucket counts: Complex 3368 rows, connectable 2597; Extreme 4492 rows, connectable 3692。
  - Failure triage: Oracle A failure reasons are `goal_in_collision=1182`, `start_in_collision=389`, `timeout=63`。
  - Key implication: the 1571 unresolved rows are exactly the invalid start/goal rows; after excluding `goal_in_collision/start_in_collision`, remaining non-invalid rows are 6289/6289 oracle-connectable。
  - B-only cases: all 63 are Oracle A `timeout`; selected candidate source is `goal_annulus=58`, `voronoi_skeleton=5`; detailed rows in `0_trials/module2_oracle_shape/oracle_connector_b_only_cases.csv`。
  - Analysis artifacts: `0_trials/module2_oracle_shape/oracle_connector_full_analysis.json`, `oracle_connector_b_only_cases.csv`, `oracle_connector_a_only_cases.csv`, `oracle_connector_invalid_query_counts.csv`。
  - Experiment record: `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md`。
  - 当前边界: C02.1 全量已完成, 但这不是最终 Gate #2。它把问题缩窄为 "invalid endpoint 清洗 + timeout/B-only connector 价值 + 成本账", 不能直接 claim RL 已必要或已充分。
- [x] C02.2 标注失败形态。
  - 类别: 无解死区、需绕瓶颈、需短程避障后开阔、需倒车、goal 周围不可达、checker 假阳性。
  - 验证: 每类抽样出 PNG/SVG 可视化。
  - 已完成的数字分层: invalid start/goal = 1571, non-invalid unresolved = 0, timeout/B-only = 63, A-only = 2。
  - 已完成可视化种子: 新增 `2_experiment/forest_n3p/scripts/render_oracle_connector_cases.py`。
  - 输出: `0_trials/module2_oracle_shape/c02_shape_labels/summary.json`, `index.md`, 7 张 PNG。
  - 形态标签: `invalid_goal_in_collision`, `invalid_start_in_collision_goal_also_blocked`, `timeout_saved_by_goal_annulus`, `oracle_b_conservative_combined_collision_rejection`。
  - 图像 QA: 7 张图均为 `1393 x 1292`, 颜色多样性检查通过; B-success rows 均可重放为 `rendered_b_success=true`。
  - Provenance issue: full run 中 5 个 `voronoi_skeleton` B-only rows 目前不能被当前脚本重放, 不能作为可视化正例或论文证据。
  - Experiment record: `.pipeline/experiments/20260703_module2_c02_shape_labels.md`。
  - 边界: C02.2 是视觉种子完成, 不是 Gate #2 通过。
- [x] C02.3 Gate #2 判定。
  - 判定: `gate2_not_failed_scope_narrowed`。
  - Gate #2 失败条件未命中: full oracle 显示 non-invalid rows `6289/6289` connectable, non-invalid unresolved `0`。
  - 宽 claim 被拒绝: invalid endpoint = `1571/7860`; B-only timeout = `63/6289` non-invalid rows, 不能写成 "多数 RS failure 需要 RL connector"。
  - 允许继续: D01/D02 成本账, 因为存在 narrow connector-positive signal (`goal_annulus=58`, `voronoi_skeleton=5`, 其中 visual 正例只使用可重放 `goal_annulus`)。
  - 禁止跳步: D01/D02 前不进入 RL 环境实现、PPO 训练或论文必要性 claim。
  - 输出: `.pipeline/experiments/20260703_module2_gate2_oracle_shape.md`。

### Phase D: 成本账 Gate #1

#### D01. 解析扩展开销拆分

- [x] D01.1 为 Dang multi-RS 统计每次调用的候选半径数、RS 求解时间、采样时间、碰撞检测时间。
  - 插入点: `planner.py:204-245`, `planner.py:282-340`
  - 输出: telemetry dataclass, 不污染主路径。
  - 已完成: `AnalyticCandidateTelemetry`, `AnalyticRadiusResult`, `AnalyticExpansionTelemetry`。
  - Stats 字段: `analytic_candidate_radius_count`, `analytic_candidate_success_count`, `analytic_candidate_failure_count`, `analytic_rs_solve_time_s`, `analytic_sample_time_s`, `analytic_collision_check_time_s`, `analytic_cost_eval_time_s`, `analytic_total_time_s`, `analytic_sample_count`, `analytic_collision_check_count`。
  - Evaluation metadata: 常规评测只透传 summary telemetry, 不透传 `analytic_telemetry_records` 大列表。
  - Smoke: `0_trials/module2_cost_accounting/d01_analytic_cost_telemetry_smoke/summary.json`, Dang multi-RS 空图单次 analytic attempt 扫 11 个半径, 11 个候选成功, telemetry record count 1。
  - 验证: `py_compile` pass; `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py 2_experiment/forest_n3p/tests/test_inference_timing.py -q` -> `9 passed in 1.00s`。
  - 记录: `.pipeline/experiments/20260703_module2_d01_analytic_cost_telemetry.md`。
- [x] D01.2 统计 RS 失败调用的平均成本。
  - 数据: C01 的同一 query set。
  - 输出: `rs_attempt_cost_s`, `collision_checks`, `samples_checked`。
  - 已完成: 新增 `2_experiment/forest_n3p/scripts/run_analytic_cost_distribution.py`。
  - 输出: `0_trials/module2_cost_accounting/d01_analytic_cost_distribution/summary.json`, `query_costs.parquet`, `attempt_costs.parquet`, `candidate_costs.parquet`。
  - 规模: 20 queries, 8622 analytic attempts, 94842 radius candidates。
  - 关键预算: attempt total time p50 `0.000814s`, p95 `0.002025s`, p99 `0.002829s`; total analytic time `8.215955s` / plan time `24.751256s` = `0.331941`。
  - 主要成本项: collision check mean `0.000500s`, RS solve mean `0.000255s`, sampling mean `0.000150s`。
  - 边界: D01.2 是本地成本分布, 不是 Gate #1 判定; D02 NN forward + rollout collision 仍缺。
  - 记录: `.pipeline/experiments/20260703_module2_d01_cost_distribution.md`。

#### D02. 神经 policy 前向预算

- [x] D02.1 实现三个候选网络的纯前向 microbenchmark。
  - tiny MLP: target + low-res lidar/distance vector。
  - small CNN: 2-channel egocentric patch + target pose。
  - compact CNN+MLP: patch encoder + scalar head。
  - 输入 shape 必须来自 C02 patch 需求, 不能拍脑袋。
  - 已完成: 新增 `2_experiment/forest_n3p/scripts/run_policy_forward_budget.py`。
  - Shape: `annulus_auto=64x64` 来自 `0.1m` resolution + C02 goal-annulus max radius `3.0m`; `footprint_margin_auto=128x128` 来自 two-circle footprint margin sensitivity。
  - 输出: `0_trials/module2_cost_accounting/d02_policy_forward_budget/summary.json`, `forward_budget_records.parquet`, `forward_budget_samples.parquet`。
  - 规模: CPU single-thread, 3 models x 2 shapes x 3 batch sizes, aggregate rows 18, sample rows 18000。
  - Batch=1 关键数字: `tiny_mlp` p50 `0.011ms`; `compact_cnn_mlp` p50 `0.120ms`(64) / `0.405ms`(128); `small_cnn` p50 `0.162ms`(64) / `0.520ms`(128)。
  - 参考: D01.2 Dang multi-RS attempt p50 `0.814ms`, p95 `2.025ms`。
  - 边界: 只测 NN forward; 未计 rollout collision、terminal RS、planner integration; 不构成 Gate #1 通过。
  - 环境限制: 本机 PyTorch import 需要 `--allow-duplicate-openmp`, 不能作为最终 paper timing。
  - 记录: `.pipeline/experiments/20260703_module2_d02_policy_forward_budget.md`。
- [x] D02.2 CPU 与 GPU 都测。
  - CPU: 本机或远端单线程。
  - GPU: 远端 CUDA, batch=1 和 batch=N analytic attempts。
  - 输出: p50/p95 forward ms。
  - 已完成: 本机 CPU/MPS forward, 远端 3070 Ti CUDA forward, 以及 rollout collision + terminal RS proxy 成本账。
  - 新增工具: `2_experiment/forest_n3p/scripts/run_rollout_collision_budget.py`。
  - Forward outputs: `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_local/`, `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/`。
  - Rollout outputs: `0_trials/module2_cost_accounting/d02_rollout_collision_budget/`。
  - 规模: local forward 36 aggregate / 18000 samples; CUDA forward 18 aggregate / 9000 samples; rollout collision 192 aggregate / 19200 samples。
  - CUDA evidence: 5070 Ti 当前被 Python 占用约 15.6GB, OOM; 3070 Ti 空闲并完成 run, torch `2.12.1+cu130`, driver `595.71.05`。
  - 关键 forward p50: CPU compact/small CNN 128-cell = `0.392/0.514ms`; CUDA compact/small CNN 128-cell = `0.119/0.137ms`。
  - 关键 rollout p50: Grid 32-step rollout total `0.129ms`, candidate total with terminal RS proxy `0.239ms`; EDT 32-step candidate total `0.207ms`。
  - Conservative combined p50: CPU compact CNN 128-cell + Grid 32-step candidate total = `0.631ms`, still below D01 Dang attempt p50 `0.814ms`。
  - 边界: 这是 compute plausibility, 不是 trained policy success, 也不是 Gate #1 通过。
  - 记录: `.pipeline/experiments/20260703_module2_d02_device_and_rollout_budget.md`。
- [x] D02.3 Gate #1 判定。
  - 通过: `NN forward + rollout collision` 的 p50 成本小于 "被省掉的 RS/HA* expansion 成本" 的保守估计。
  - 失败: 端到端时间无下降空间。
  - 输出: `.pipeline/experiments/YYYYMMDD_module2_gate1_cost_accounting.md`
  - 判定: `gate1_not_failed_preimplementation_compute_gate`。
  - 含义: compute 预算未触发提前失败, 允许进入 E01; 但这不是完整 Gate #1 pass, 因为 trained policy 与 planner-integrated end-to-end time 尚未测。
  - 保守证据: CPU compact CNN 128-cell forward p50 `0.392ms` + Grid 32-step candidate p50 `0.239ms` = `0.631ms`, 低于 D01 Dang attempt p50 `0.814ms`; CPU p95 组合 `0.821ms`, 低于 D01 p95 `2.025ms`。
  - 禁止 claim: RL-RS faster, PPO necessary, final architecture selected。
  - 记录: `.pipeline/experiments/20260703_module2_gate1_cost_accounting.md`。

### Phase E: RL steering 环境

#### E01. 环境 API

- [x] E01.1 新建 `2_experiment/forest_n3p/rl_rs/` 包。
  - 文件: `__init__.py`, `env.py`, `obs.py`, `actions.py`, `reward.py`, `terminal.py`, `policy.py`, `rollout.py`, `telemetry.py`
  - 说明: 这是最大实现骨架, 不是单文件 demo。
  - 已完成: 新增 `2_experiment/forest_n3p/rl_rs/` 包和 `2_experiment/forest_n3p/tests/test_rl_rs_api.py`。
  - API anchors: `AnalyticExpansionContext`, `AnalyticExpansionEnv`, `SteeringAction`, `rollout_constant_steer_step`, `check_terminal_rs_connectable`, `RlRsStepTelemetry`, `SteeringPolicy`。
  - 边界: reward 仍是 `pending_e02`; 当前只建立 planner-compatible API skeleton, 不代表 PPO/BC、reward 或 planner integration 完成。
  - 验证: `py_compile` pass; `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `2 passed in 0.22s`。
  - 记录: `.pipeline/experiments/20260703_module2_e01_rl_rs_api_skeleton.md`。
- [x] E01.2 `AnalyticExpansionEnv` 环境输入必须来自 planner state。
  - reset 输入: map, footprint, current state, final goal, params, checker, budget。
  - step 输入: continuous steer/curvature。
  - step 输出: obs, reward, terminated, truncated, info。
  - 已完成: 加固 `AnalyticExpansionEnv.reset/step` 状态机。
  - 覆盖语义: step-before-reset 报错、colliding start 拒绝、rollout collision terminated、terminal RS success terminated、budget exhausted truncated、done 后禁止继续 step、info 显式暴露 failure/status。
  - 边界: reward 仍 `pending_e02`, 观测 patch 仍属 E01.3, 未做 policy/planner integration。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `11 passed in 0.44s`。
  - 记录: `.pipeline/experiments/20260703_module2_e01_env_state_machine.md`。
- [x] E01.3 观测实现。
  - 主通道: egocentric occupancy patch。
  - 辅通道: EDT/distance field patch。
  - scalar: relative goal distance, bearing, heading error, current clearance, remaining budget。
  - 验证: patch rotate/translate invariance 通过图像测试。
  - 已完成: `RlRsObservation.patch` 现在支持 `(C,H,W)` float32 patch; 默认 config 为 `6.4m`, `64x64`, occupancy + normalized EDT 两通道。
  - 语义: robot-frame patch, forward=+x; 越界按 occupied; EDT 以米计算后按 `edt_clip_m` 裁剪归一化。
  - 测试: 前方障碍在 east/north heading 下落到同一 patch cell; 越界 occupied; occupancy/EDT channel stack 正确。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `14 passed in 0.43s`。
  - 记录: `.pipeline/experiments/20260703_module2_e01_observation_patch.md`。
- [x] E01.4 动作实现。
  - v1: forward-only continuous steering in `[-max_steer, max_steer]`。
  - v2 candidate: steering + direction gate, 用于 "需倒车" 形态。
  - 注意: v2 只有 C02 证明倒车必要时才启用。
  - 已完成: `ActionConfig`, normalized steering decode, physical steering clip, `steering_action_to_primitive`, rollout primitive telemetry。
  - v1 边界: `direction=+1` forward-only; `allow_reverse=True` 会直接报错。
  - 验证: normalized action 转 physical steering, forward `MotionPrimitive` conversion, reverse gate rejection, rollout/env telemetry direction。
  - 当前结论: reverse/direction gate 未启用, 需 C02 倒车必要性证据或 v2 contract 才能开启。
  - 记录: `.pipeline/experiments/20260703_module2_e01_action_space.md`。
- [x] E01.5 终止条件实现。
  - success: 当前 state 能通过 RS 无碰撞接到 final goal。
  - collision: 当前 rollout segment 碰撞。
  - truncated: budget exhausted 或 no progress。
  - failure metadata: collision, timeout, no_rs_terminal, oscillation。
  - 已完成: success 仍由 terminal RS checker 判定; rollout collision `terminated`; budget exhausted 且 terminal RS 失败 `truncated` 并写入 `no_rs_terminal:<detail>`; no-progress 由 `min_progress_m` + `no_progress_patience` 控制, 提前 `truncated` 并写入 `no_progress`。
  - telemetry/info: `goal_distance_m`, `progress_to_goal_m`, `no_progress_count`。
  - 边界: `oscillation` 暂不 claim 已实现, 后移到 E03.4 定义可测试信号。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `17 passed in 0.47s`。
  - 记录: `.pipeline/experiments/20260703_module2_e01_terminal_conditions.md`。

#### E02. Reward 最大实现

- [x] E02.1 success reward 与部署使命一致。
  - 直接调用本地 RS checker, 不用任意 "离目标 < eps" 代替。
  - 已完成: `compute_terminal_success_reward` 使用 `TerminalRsCheckResult.success` 作为唯一 success signal; `RewardConfig.terminal_rs_success` 控制权重; `AnalyticExpansionContext.reward_config` 接入 env。
  - 测试锁定: terminal RS success 时 `goal_distance_m > 0.0` 仍给 success reward, 证明不是欧氏距离阈值替代。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `18 passed in 0.49s`。
  - 记录: `.pipeline/experiments/20260703_module2_e02_success_reward.md`。
- [x] E02.2 shaping 分项全部写入 info。
  - distance/RS-distance progress, clearance, curvature-rate, path length, step penalty, terminal bonus/penalty。
  - 已完成: `RewardBreakdown` 现在包含 success、terminal、collision、progress、rs_progress、clearance、curvature、path_length、step; `step.info` 暴露 `reward_total` 和 `reward_terms`。
  - 实现依据: distance progress 来自 E01.5 `progress_to_goal_m`; RS-distance progress 来自 terminal/estimated Reeds-Shepp path length; clearance 来自 `GridMap` EDT + `TwoCircleFootprint.circle_centers()`; curvature-rate 来自 `tan(steering)/wheelbase` 的变化; path length 来自 rollout samples。
  - 权重边界: progress/clearance/curvature/path-length/step shaping 已实现并可配置, 但默认不假装完成调参; E02.3 仍需显式 ablation hooks。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `19 passed in 0.48s`。
  - 记录: `.pipeline/experiments/20260703_module2_e02_reward_shaping_terms.md`。
- [x] E02.3 reward ablation hooks。
  - 每个 reward term 可开关。
  - 后续论文可做消融, 不允许写死。
  - 已完成: 新增 `RewardTermSwitches` 和 `RewardConfig.enabled_terms`; success/terminal/collision/progress/rs_progress/clearance/curvature/path_length/step 每项均可显式启停。
  - info metadata: `step.info["reward_ablation"]` 记录每项开关状态, 不再只靠权重为 0 推断消融配置。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `20 passed in 0.45s`。
  - 记录: `.pipeline/experiments/20260703_module2_e02_reward_ablation_hooks.md`。

#### E03. 环境测试

- [x] E03.1 单步运动学测试。
  - 与 `propagate()` 输出严格一致。
  - 已完成: `test_rollout_step_matches_planner_propagate_for_curved_action` 使用非零 steering, 逐项比较 `rollout.next_state`、`rollout.samples[-1]` 和 planner-source `propagate()`。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `21 passed in 0.45s`。
  - 记录: `.pipeline/experiments/20260703_module2_e03_single_step_kinematics.md`。
- [x] E03.2 碰撞测试。
  - 同一 pose/path 下 env checker 与 planner checker 一致。
  - 已完成: `test_rollout_collision_matches_planner_checker_for_free_and_blocked_paths` 覆盖 free path 与 blocked path, 逐项比较 `RolloutStepResult.collided` 和 `GridFootprintChecker.collides_path(samples)`。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `22 passed in 0.47s`。
  - 记录: `.pipeline/experiments/20260703_module2_e03_collision_consistency.md`。
- [x] E03.3 success set 测试。
  - 人工构造无障碍/有障碍 RS 对接样例。
  - 已完成: `test_terminal_rs_success_set_distinguishes_free_and_blocked_connections` 直接调用 `check_terminal_rs_connectable()`, 覆盖空图 success 和障碍阻挡 `terminal_rs_collision`。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `23 passed in 0.48s`。
  - 记录: `.pipeline/experiments/20260703_module2_e03_terminal_rs_success_set.md`。
- [x] E03.4 no progress/oscillation 测试。
  - 防止 policy 原地左右打舵拿 shaping。
  - 已完成: no-progress 已有测试继续覆盖; 新增 oscillation guard, 在短窗口内 steering 符号反复翻转且净 progress 不足阈值时 `truncated`, failure reason 为 `oscillation`。
  - telemetry/info: `oscillation_detected`。
  - reward: `RewardConfig.oscillation_penalty` 接入 terminal penalty。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `24 passed in 0.46s`。
  - 记录: `.pipeline/experiments/20260703_module2_e03_no_progress_oscillation.md`。

### Phase F: BC warm-start 与 PPO 训练

#### F01. Oracle 数据生成

- [x] F01.1 从 C02 oracle path 提取 state-action demonstrations。
  - 状态: 每个 rollout step 的 env obs。
  - 动作: oracle path 下一段曲率/steer。
  - 过滤: 碰撞、过短、terminal RS 已可达样本。
  - 已完成: 新增 `extract_oracle_demonstrations.py`, 从 C02 oracle results 重放 oracle A/B path, 提取 scalar obs + expert steering/curvature/direction, 并过滤 collision、reverse、too-short、terminal-RS-ready samples。
  - 产物: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet` 含 1109 条 preview demonstrations; `0_trials/module2_rl_rs_bc_demo_smoke/` 含 oracle A smoke 与 B-only goal-annulus smoke。
  - 边界: 这是 extraction pipeline + source-bound preview, 不是最终完整 BC corpus; `voronoi_skeleton` B-only rows 仍未纳入 claim。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `24 passed in 0.50s`。
  - 记录: `.pipeline/experiments/20260703_module2_f01_oracle_demonstration_extraction.md`。
- [x] F01.2 数据 manifest。
  - 记录 map seed, query id, oracle type, source commit, extraction config。
  - 输出: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json`
  - 已完成: 写入 `manifest.json` 和 `README.md`; manifest 包含 source input、source extractor、source hash、schema、filters、preview file hash、known boundaries。
  - 边界: dataset status 为 `preview`, 不是最终完整 BC corpus; BC/PPO training 尚未开始。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `24 passed in 0.47s`。
  - 记录: `.pipeline/experiments/20260703_module2_f01_dataset_manifest.md`。

#### F02. BC 预热

- [x] F02.1 训练 BC policy。
  - loss: steer regression + terminal classifier optional。
  - metric: rollout success to RS-connectable set, not only action MSE。
  - 已完成: 新增 `train_bc_policy.py`, 从 F01 preview demonstrations 训练 scalar-observation MLP steering regressor, 按 `source_row_index` 做 group split, 输出 checkpoint/history/summary, 并在 held-out source rows 上做闭环 terminal-RS-success rollout。
  - 产物: `2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke/`。
  - 结果: validation MAE 0.147 rad; closed-loop 5 episodes 中 terminal RS success 2、collision 3。
  - 边界: 这是 preview smoke, 不是正式 BC baseline; 结果显示 action MSE 不能替代闭环指标。
  - 验证: checkpoint 默认 `torch.load(..., map_location="cpu")` 通过; `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_policy_forward_budget.py 2_experiment/forest_n3p/tests/test_rollout_collision_budget.py 2_experiment/forest_n3p/tests/test_rl_rs_api.py -q` -> `24 passed`。
  - 记录: `.pipeline/experiments/20260703_module2_f02_bc_policy_smoke.md`。
- [!] F02.2 BC 作为正式 baseline（formal-v1 结果已失效, 需 formal-v2 重跑）。
  - 目的: 证明 PPO 精调是否真的必要。
  - 失败: 若 BC 已够好, 论文叙事要改成 "imitation initialized neural analytic expansion", PPO 只作 fine-tune。
  - 历史完成子项: 生成 formal-v1 corpus, 训练 scalar-observation BC lower-bound, 训练 obstacle-summary BC baseline, 并做 step-aligned 0.1m 闭环评估。
  - formal-v1 corpus: `demonstrations_formal_v1.parquet`, 85514 demo rows, 1035 source rows, Complex/Extreme 基本平衡。
  - scalar BC 结果: validation MAE 0.096 rad; 0.3m rollout success 11/259; 0.1m rollout success 45/259。
  - obstacle-summary BC 结果: validation MAE 0.100 rad; 0.1m rollout success 84/259, collision 164/259。
  - 关键发现: obstacle features 明显提升闭环行为, 但 32.4% success 仍不足以 planner insertion; action MAE 仍会误导。
  - 2026-07-04 更正: formal-v1 是 profile-unaware map cache 生成的数据, 在真实 profile 地图下有 4764 条 colliding demo rows; 上述 scalar/obstacle-summary 结果只能保留作历史调试记录, 不能作为当前 BC 方法排名。
  - formal-v2 corpus: `demonstrations_formal_v2.parquet`, 83809 demo rows, 1032 source rows, collision audit 为 0 current/next collision rows。
  - 当前边界: F02.2 formal baseline 必须在 formal-v2 上重跑后才可恢复。
  - 记录: `.pipeline/experiments/20260703_module2_f02_formal_scalar_bc.md`。
  - 记录: `.pipeline/experiments/20260703_module2_f02_obstacle_summary_bc.md`。
- [>] F02.3 patch+scalar CNN BC warm-start。
  - 目的: 直接使用 `(2,64,64)` occupancy/EDT patch + scalar obs, 形成 PPO 前更强的 imitation initialization。
  - metric: 0.1m rollout terminal-RS-success, collision, truncation; action MSE 只作辅助。
  - 判定: 若 CNN-BC 明显强于 obstacle-summary, 用作 PPO warm start; 若仍弱, 记录 BC ceiling 并进入 PPO/curriculum。
  - 已完成子项: 新增 `train_bc_patch_policy.py` 和 CNN forward 单测; preview smoke 与 stronger preview 均可复跑。
  - preview 结果: small CNN 0/5 success, stronger CNN 1/5 success, 均弱于 obstacle-summary preview 4/5。
  - formal bounded pilot: 4096 train rows / 1024 val rows, success 44/241, collision 185/241, runtime error 8/241。
  - 2026-07-04 更正: 修复 profile-aware cache 后, 旧 checkpoint 重评估为 success 49/241, collision 175/241, runtime error 13/241; runtime error 均为 true-profile start collision。这证明 formal-v1 pilot 数据边界失效。
  - 当前边界: patch CNN 脚本已跑通, 但 formal-v1 pilot 不可用于 PPO warm start。
  - 下一步: 在 formal-v2 上重跑 scalar、obstacle-summary、patch+scalar CNN, 再决定 PPO warm-start。
  - 记录: `.pipeline/experiments/20260703_module2_f02_patch_cnn_preview.md`。
  - 记录: `.pipeline/experiments/20260703_module2_f02_patch_cnn_formal_pilot.md`。
- [x] F02.4 修复 profile-aware map cache 并重建 formal-v2 corpus。
  - 根因: `_grid_for_row()` 曾只用 `map_seed` 缓存地图; `validation_t06` 中同一 seed 被多个 `profile_name` 复用。
  - 修复: row-derived map/EDT/checker cache 使用 `(profile_name, map_seed)`。
  - formal-v1 审计: 85514 rows 中 4764 rows current/next collision, 覆盖 236 source rows。
  - formal-v2 产物: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet`, 83809 rows, 1032 source rows。
  - formal-v2 审计: 0 current collision, 0 next collision, 0 any collision。
  - 记录: `.pipeline/experiments/20260704_module2_f02_map_cache_formal_v2_rebuild.md`。
- [x] F02.5 在 formal-v2 上重跑 BC baseline。
  - 最低重跑: scalar lower-bound、obstacle-summary、patch+scalar CNN bounded pilot。
  - 判定: 只用 formal-v2 的 0.1m closed-loop terminal-RS-success / collision / runtime_error 做 warm-start 决策; action MSE 只作辅助。
  - 禁止: 继续引用 formal-v1 模型结果作为当前方法排名。
  - 已完成子项: scalar lower-bound、obstacle-summary MLP、patch+scalar CNN bounded pilot。
  - scalar formal-v2: 0.3m success 6/258, collision 252/258; 0.1m success 38/258, collision 200/258。
  - obstacle-summary formal-v2: 0.1m success 67/258, collision 178/258, truncated 13/258, runtime_error 0。
  - patch+scalar CNN formal-v2 bounded: 0.1m success 63/242, collision 171/242, truncated 8/242, runtime_error 0。
  - 当前边界: obstacle-summary 仍强于 scalar; patch-CNN 没有明确超过 obstacle-summary; 两者均不足以 planner insertion。
  - 记录: `.pipeline/experiments/20260704_module2_f02_formal_v2_mlp_bc_baselines.md`。
- [?] F02.6 PPO warm-start 决策门。
  - 候选: obstacle-summary checkpoint, patch-CNN bounded checkpoint, 或 stronger/full patch-CNN protocol 后再决策。
  - 当前证据: patch-CNN bounded pilot 没有明确超过 obstacle-summary, 且只用 4096/1024 bounded rows; obstacle-summary 是当前 practical candidate, 但也只有 67/258 success。
  - 2026-07-04 补充同口径评估: 在 patch-CNN 同一组 `max_val_rows=1024` bounded rows / 242 source rows 上, scalar success 65/242, obstacle-summary success 101/242, patch-CNN success 63/242。
  - 推荐: 若进入 PPO, 使用 obstacle-summary checkpoint 作为 practical warm-start; 不推荐继续用 bounded patch-CNN checkpoint。
  - 工程状态: obstacle-summary checkpoint 已可通过 `train_rl_rs_ppo.py --bc-checkpoint` 注入 PPO actor, 且 deterministic action 与原 BC normalized steering 一致。
  - 2026-07-04 决策包: 新增 `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json` 和 `.md`, status=`pending_human_decision`, recommendation=`approve_obstacle_summary_warm_start`, blocker=`requires_dr_sun_approval`。
  - 决策包依据: no-warm formal Gate #3 已可审计失败 29/64=0.453125; obstacle-summary formal-v2 为 67/258, 同 bounded rows 为 101/242; patch+scalar CNN bounded 为 63/242; `gpu3070ti-relay` no-warm preflight ready, obstacle-summary warm-start preflight 仍被 `warm_start_decision_pending` 阻塞。
  - 决策包边界: 这是 evidence-bound recommendation, 不关闭 F02.6, 不开始正式 warm-start 训练, 不把远端 CUDA smoke 当 Gate #3 证据。
  - 2026-07-04 决策记录协议: 新增 `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` 和 `.md`, status=`pending_human_decision`, effective decision=`pending`, blocker=`requires_dr_sun_approval`。
  - 决策记录语义: 只有 `decider=Dr Sun` 才能记录 `approve_obstacle_summary_warm_start` 或 `reject_obstacle_summary_warm_start`; approve 映射为 H01/preflight/audit 的 `approved_obstacle_summary`, reject 映射为 H01 的 `no_warm_only` 和 preflight/audit 的 `not_used`。
  - 当前记录边界: `remote_training_allowed=false`, `local_training_allowed=false`, `formal_claim_allowed=false`; 不批准 F02.6, 不启动本地或远端训练。
  - 记录: `.pipeline/experiments/20260704_module2_f03_obstacle_summary_warm_start.md`。
  - 决策包记录: `.pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md`。
  - 决策记录协议: `.pipeline/experiments/20260704_module2_f02_6_decision_record_protocol.md`。
  - 仍需 Dr Sun 决策: 接受 obstacle-summary warm-start 进入 F03, 或明确要求先做 stronger/full patch-CNN protocol。

#### F03. PPO 最大实现

- [x] F03.1 选择 RL 库。
  - 候选: stable-baselines3, cleanrl, local minimal PPO。
  - 决策依据: continuous action, vector env, logging, checkpoint, license, reproducibility。
  - 不允许: 手写不可审计的临时 PPO。
  - 决策: 选择 Stable-Baselines3 2.9.0 + Gymnasium wrapper 作为 F03 PPO 主线。
  - 依据: SB3 支持 custom env/policy、Dict observation、TensorBoard、callback、Box continuous action 和 VecEnv; 本机 `python -m pip install stable-baselines3` 后 import smoke 通过。
  - 排除: CleanRL 只作为 PPO 细节参考, 因其 README 明确不是 modular library / not meant to be imported, 且当前 prerequisite 是 Python `<3.11`; local minimal PPO 继续禁止。
  - 适配边界: 当前 `AnalyticExpansionEnv` 不是 Gymnasium env; F03.2 要写薄 adapter, 不重写环境动力学/碰撞/reward。
  - 记录: `.pipeline/experiments/20260704_module2_f03_rl_library_selection.md`。
- [x] F03.2 vectorized env。
  - 多 map/query 并行采样。
  - 每个 episode 绑定一个 RS failure node 或 near-goal state。
  - 已完成: 新增 `GymAnalyticExpansionEnv`, 将 planner-side `AnalyticExpansionEnv` 包装成 Gymnasium env; action space 为 normalized single-steering `Box(-1, 1, shape=(1,))`, observation space 为 `Dict({"scalar": (8,), "patch": (C,H,W)})`。
  - SB3 兼容性: `stable_baselines3.common.env_checker.check_env()` 通过; 双环境 `DummyVecEnv` reset/step smoke 通过。
  - 边界: 当前 vector smoke 证明 SB3 向量接口可运行, 但真实多 map/query context sampler 与 curriculum 仍在 F03.3/F03.4。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `43 passed in 3.75s`。
  - 记录: `.pipeline/experiments/20260704_module2_f03_gymnasium_adapter.md`。
- [x] F03.3 curriculum。
  - stage 1: open/simple connector。
  - stage 2: obstacle near but one clear side。
  - stage 3: Complex/Extreme RS failure nodes。
  - stage 4: held-out procedural maps。
  - 已完成: 新增 `CurriculumContextConfig`, `CurriculumSampleMetadata`, `OpenConnectorContextSampler`, `ObstacleBypassContextSampler`, `OracleConnectorContextSampler`, `HeldoutQueryContextSampler`, `WeightedCurriculumContextSampler`。
  - 真实来源: stage 3 默认读取 `0_trials/module2_oracle_shape/oracle_connector_results.parquet` 并筛 `oracle_connectable=True`; stage 4 用 held-out seed 重新走 `build_query_set()`。
	  - Gym 接入: `GymAnalyticExpansionEnv.reset()` now exposes `info["curriculum"]`, 为 F03.4 logging 提供 stage/source/query metadata。
	  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `48 passed in 6.59s`; 真实四 stage Gym reset/step smoke 通过。
	  - 边界: F03.3 不选择 warm-start checkpoint, 不开始 PPO 训练, 不 claim Gate #3。
	  - 2026-07-04 formal trial 修复: no-warm formal trial 首次运行暴露 oracle parquet 中有少量 row 在当前 profile-aware 地图重建下 start/goal collision; 量化为 6289 candidate rows 中 start_bad=4, goal_bad=54。
	  - 修复: `OracleConnectorContextSampler` 抽样时跳过重建为 collision 的 row, 记录 `skipped_invalid_rows` 和 `last_invalid_metadata`; 超过尝试上限才报错。
	  - 回归测试: `test_oracle_connector_sampler_skips_rows_that_reconstruct_to_colliding_context`; `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py -q` -> `6 passed in 6.27s`。
	  - 失败证据: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/failed_attempt_01/`。
	  - 记录: `.pipeline/experiments/20260704_module2_f03_curriculum_sampler.md`。
	  - collision guard 记录: `.pipeline/experiments/20260704_module2_f03_oracle_sampler_collision_guard.md`。
- [x] F03.4 logging。
  - TensorBoard/CSV: reward terms, success, terminal RS success, collision, truncation, rollout length, clearance, curvature rate。
  - 每个 checkpoint 存 config + source hash。
  - 已完成: 新增 `RlRsEpisodeLoggingWrapper`, episode CSV 字段覆盖 curriculum、reward terms、terminal/collision/truncation、rollout length、clearance、curvature rate、timing。
  - TensorBoard: 支持显式注入 writer, 并提供 `create_tensorboard_writer()` helper; wrapper import 不强制加载 TensorBoard。
  - Manifest: 新增 `file_sha256()` 与 `write_training_manifest()`, 用于记录 config、source hashes、checkpoint list、command。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `52 passed in 6.71s`; `KMP_DUPLICATE_LIB_OK=TRUE` TensorBoard writer smoke 通过。
  - 边界: F03.4 不开始 PPO 训练, 不关闭 F02.6 warm-start 决策, 不 claim Gate #3。
  - 记录: `.pipeline/experiments/20260704_module2_f03_training_logging.md`。
- [>] F03.5 Gate #3 判定。
  - 通过: 小规模单一密度地图中 RS-connectable terminal success > 80%。
  - 失败: 按 Contract 记录 PPO 不收敛, 不改任务定义。
  - 入口基础设施已完成: 新增 `RlRsObstacleSummaryExtractor` 与 `train_rl_rs_ppo.py`, 使用 SB3 `MultiInputPolicy`, F03 curriculum, episode CSV, SB3 model zip, training manifest。
  - smoke 产物: `0_trials/module2_ppo_smoke/f03_train_entry_smoke/`。
  - 验证: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `54 passed in 7.17s`; `train_rl_rs_ppo --smoke` 通过。
  - warm-start 接线: `--bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt` smoke 通过, 产物在 `0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/`, manifest 记录 `warm_start_status=applied_obstacle_summary_bc`。
  - warm-start 验证: PPO deterministic action 与 F02 obstacle-summary BC normalized action 一致; `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `55 passed in 6.97s`。
  - Gate evaluator: 新增 `eval_rl_rs_gate3.py`, 加载 SB3 model 后跑 deterministic eval episodes, 输出 `gate3_eval_episodes.csv` 与 `gate3_summary.json`。
  - checkpoint reload 修复: warm-start model 现在使用可序列化 `RlRsMultiInputPolicy` + `TanhLinearActionHead`, 并持久化 feature normalization; save/load roundtrip 已测试。
  - eval smoke 产物: `0_trials/module2_ppo_smoke/f03_gate3_eval_entry_smoke/`; open-connector 4 episodes eval smoke 输出 `terminal_rs_success_rate=1.0`。
  - evaluator 验证: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `56 passed in 7.28s`。
  - Gate trial runner: 新增 `run_rl_rs_gate3_trial.py`, 一条命令串起 PPO train -> deterministic Gate #3 eval -> 顶层 `gate3_trial_manifest.json`。
  - trial runner smoke 产物: `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/`; manifest 写明 `warm_start_status=applied_obstacle_summary_bc`, `formal_gate_claim=false`, `terminal_rs_success_rate=1.0`。
  - trial runner 验证: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `57 passed in 7.41s`; 项目内 warm-start runner smoke 通过。
  - Formal audit: 新增 `audit_rl_rs_gate3_trial.py`, 读取 trial manifest 并检查 smoke、episode 数、train/eval curriculum、warm-start 决策和 artifact 完整性后才允许 formal pass/fail。
  - audit smoke 产物: `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/gate3_formal_audit.json`; 当前审计为 `formal_decision=not_formal`, blockers 包含 `smoke_trial`, `insufficient_eval_episodes`, `train_curriculum_not_f03`, `eval_curriculum_not_f03`, `warm_start_decision_pending`。
  - audit 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py -q` -> `2 passed in 0.17s`。
  - Formal preflight: 新增 `preflight_rl_rs_gate3_formal_trial.py`, 不跑训练, 只冻结 formal runner/audit 命令、参数、expected artifacts 和 blockers。
  - preflight 产物: no-warm-start `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_preflight_manifest.json` 为 `preflight_status=ready`; obstacle-summary warm-start `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_pending_v1/gate3_preflight_manifest.json` 因 `warm_start_decision_pending` 为 `blocked`。
  - preflight 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py -q` -> `2 passed in 0.19s`。
  - 边界: 三个 smoke 都是 open-connector 极小训练/评估; 无 warm-start smoke 写明 `not_applied_f02_6_pending`, warm-start smoke 写明 `applied_obstacle_summary_bc`; runner manifest 也固定 `formal_gate_claim=false`; audit 明确把 smoke pass 判为 `not_formal`; preflight 只冻结正式运行协议, 不 claim F03.5 Gate 结果。
  - 记录: `.pipeline/experiments/20260704_module2_f03_ppo_training_entry.md`。
  - warm-start 记录: `.pipeline/experiments/20260704_module2_f03_obstacle_summary_warm_start.md`。
  - evaluator 记录: `.pipeline/experiments/20260704_module2_f03_gate3_evaluator.md`。
  - trial runner 记录: `.pipeline/experiments/20260704_module2_f03_gate3_trial_runner.md`。
  - formal audit 记录: `.pipeline/experiments/20260704_module2_f03_gate3_formal_audit.md`。
  - formal preflight 记录: `.pipeline/experiments/20260704_module2_f03_gate3_formal_preflight.md`。
  - no-warm formal trial: attempt 01 暴露 oracle sampler collision row 后已按 F03.3 修复; attempt 02 完成 100000 timesteps PPO train + 64 episode deterministic eval。
  - no-warm formal 结果: `formal_decision=fail`, `formal_claim_allowed=true`, `formal_blockers=[]`; eval `terminal_rs_success=29/64`, `terminal_rs_success_rate=0.453125`, `collision_rate=0.359375`, `truncation_rate=0.1875`, 阈值 `0.8`。
  - no-warm 解释: 这是可审计的 no-warm-start Gate #3 失败, 不是 smoke, 不是运行崩溃; 但 F02.6 obstacle-summary warm-start 决策仍 pending, 不能把 no-warm 失败偷换成 warm-start 失败。
  - no-warm formal 产物: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/`。
  - no-warm formal 记录: `.pipeline/experiments/20260704_module2_f03_gate3_no_warm_formal_trial.md`。
  - no-warm failure analysis: open_connector 15/15 success, 但 `rs_failure_node` 6/24 success、collision rate 0.583333, `heldout_procedural` 2/14 success、truncation rate 0.571429; 训练末 1000 episode 的 `rs_failure_node` success 仍只有 0.365239。
  - timing telemetry 修复: evaluator 现在在 `model.predict()` 周围记录 `nn_forward_time_s`, summary 写出 `nn_forward_time_s` 和 `mean_nn_forward_time_s`; eval timing smoke 为 4/4 open success 且总 forward time 0.000748333s。
  - no-warm formal model 补充 eval timing: `eval_timing_v2/` 使用同一 `final_model.zip` 和同一 64 episode 协议, success/collision/truncation 与原 formal eval 完全一致; 新增 `nn_forward_time_s=0.050569629958772566`, `mean_nn_forward_time_s=0.0007901504681058213`, 64/64 episode rows 非零。
  - timing 边界: 这只补齐 evaluator 的 `model.predict()` wall-clock, 仍不能支持 planner integration 端到端 timing claim。
  - no-warm failure analysis 记录: `.pipeline/experiments/20260704_module2_f03_no_warm_failure_analysis.md`。
  - timing telemetry 记录: `.pipeline/experiments/20260704_module2_f03_eval_timing_telemetry.md`。
  - remote 3070 Ti readiness: `gpu3070ti-relay` 已验证为 `NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192 MiB`; 远端 `.venv` 安装 `stable-baselines3==2.9.0`, `pyarrow==24.0.0`, `torch==2.12.1+cu130`, CUDA 可用。
  - remote preflight: no-warm formal protocol 在 `0_trials/module2_remote_preflight/gate3_no_warm_remote_v1/gate3_preflight_manifest.json` 为 `formal_trial_ready=true`; obstacle-summary warm-start formal protocol 在 `0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json` 被 `warm_start_decision_pending` 正确阻塞。
  - remote smoke: `0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/` 完成 16 timesteps CUDA warm-start train + 4 episode eval, `warm_start_status=applied_obstacle_summary_bc`, `formal_gate_claim=false`, audit `formal_decision=not_formal`, blockers 包含 `smoke_trial`, `train_curriculum_not_f03`, `eval_curriculum_not_f03`, `insufficient_eval_episodes`, `warm_start_decision_pending`。
  - remote 边界: 这是远端训练链路 smoke, 不是 formal Gate #3, 不能用其 `final_model.zip` 填 H01 `missing_module2_rl_rs_checkpoint`。
  - remote 记录: `.pipeline/experiments/20260704_module2_f03_gpu3070ti_remote_readiness.md`。

### Phase G: Planner 集成

#### G01. Operator 接口

- [x] G01.1 定义 `AnalyticExpansionOperator` protocol。
  - `try_connect(state, goal, context) -> AnalyticExpansionResult | None`
  - result 必含: states, actions, telemetry, terminal_rs_used。
- [x] G01.2 实现 `DangRsOperator` 适配当前代码。
  - 目的: 新旧 operator 共用 telemetry/evaluation。
  - 已完成: 新增 `hybrid_a_star/operators.py`, 包含 `AnalyticExpansionOperator`, `AnalyticExpansionResult`, `DangRsPlannerContext`, `DangRsOperator`。
  - DangRsOperator 边界: 当前 adapter 仍委托 planner-owned `_try_analytic_expansion()`, 不改变主循环行为; 成功时输出 `states/actions/telemetry/terminal_rs_used/operator`, 失败时返回 `None` 并保留 planner `_last_analytic_telemetry`。
  - 不变量: `AnalyticExpansionResult` 拒绝 `states/actions` 长度不一致, 防止后续 planner trace path 无法解释。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py 2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py -q` -> `7 passed in 0.26s`。
  - 记录: `.pipeline/experiments/20260704_module2_g01_operator_protocol.md`。
- [x] G01.3 实现 `RlRsFunnelOperator`。
  - 流程: RL rollout -> terminal RS check -> return states/actions。
  - 失败: 返回 None, 不抛异常终止 HA*。
  - 已完成: 新增 `forest_n3p.rl_rs.operator.RlRsFunnelOperator`, action source 为显式 `RlRsObservation -> SteeringAction | float` callable, 用真实 `AnalyticExpansionEnv` rollout, terminal success 后通过 planner `_try_rs_with_radius()` 追加 RS 收尾段。
  - telemetry: 新增 `RlRsFunnelTelemetry`, 记录 `rl_rollout_steps`, collision/sample/terminal timing, `terminal_rs_success`, `terminal_rs_used`, `terminal_rs_action_count`, `failure_reason`。
  - env 暴露: `AnalyticExpansionStep` 公开已有内部 `next_state` 和 `primitive`, 用于构造 planner 可解释 `states/actions`。
  - 失败语义: rollout collision 和 no-progress truncation 均返回 `None`, 不抛异常终止 HA*。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_api.py 2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py 2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py 2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py 2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py -q` -> `32 passed in 0.93s`。
  - 边界: 尚未切换 Hybrid A* 主循环, 尚未加载正式 checkpoint, 不关闭 F02.6 warm-start 决策。
  - 记录: `.pipeline/experiments/20260704_module2_g01_rl_rs_funnel_operator_skeleton.md`。
- [x] G01.4 CLI/config 选择 operator。
  - 默认不变。
  - 实验脚本显式写 operator 名称。
  - 已完成子项: planner constructor-level custom operator dispatch, 参数为 `HybridAStarPlanner(..., analytic_expansion_operator=...)`。
  - 当前实现: 传入 custom operator 时, planner 使用 `operator.name` 作为 `stats["analytic_operator"]`, 并调用 `operator.try_connect(state, goal, planner_context)`。
  - 默认边界: 未传 custom operator 时, 内置 `disabled/single_rs/dang_multi_rs` 路径保持不变。
  - 已完成子项: `main_evaluation` 新增显式方法名 `ha_rl_rs_ppo`; `run_main_evaluation.py` 新增 `--module2-rl-rs-checkpoint` 及 RL-RS observation/env 参数。
  - preflight: `ha_rl_rs_ppo` 缺 checkpoint 或 checkpoint 路径不存在时阻塞, 不会静默回退 RS。
  - 记录: `.pipeline/experiments/20260704_module2_g01_operator_dispatch_stub_integration.md`。
  - 记录: `.pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md`。

#### G02. 集成测试

- [x] G02.1 无模型 stub operator 测试。
  - 用 deterministic steering mock 验证 planner 调用和 fallback。
  - 已完成: `DirectStubOperator` success path 验证 planner 会调用 custom operator, stats/telemetry 写入 `stub_direct`, analytic attempts/successes 为 `1/1`。
  - 已完成: `FailingStubOperator` failure path 验证 operator 返回 `None` 后 planner 继续 primitive fallback, 不写入 `analytic_expansion` remediation, `analytic_failure_records` 写入 `stub_failing` 与 `stub_failure`。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py -q` -> `5 passed in 0.22s`。
  - 回归: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q` -> `70 passed in 9.98s`。
  - 记录: `.pipeline/experiments/20260704_module2_g01_operator_dispatch_stub_integration.md`。
- [x] G02.2 加载 checkpoint 测试。
  - 缺 checkpoint 必须报错, 不能静默退回 RS 并声称 RL 生效。
  - 已完成: 新增 `load_rl_rs_funnel_operator_from_checkpoint()`, 缺 checkpoint 抛 `FileNotFoundError`, 真实 SB3 smoke checkpoint 可加载并对真实 `RlRsObservation` 产生 finite normalized steering。
  - 已完成: main evaluation preflight 对 `ha_rl_rs_ppo` 要求 checkpoint; `_run_hybrid_a_operator("ha_rl_rs_ppo", ...)` 会加载 checkpoint-backed operator 并写 checkpoint metadata。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py 2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py -q` -> `6 passed in 1.68s`。
  - 记录: `.pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md`。
- [x] G02.3 telemetry 测试。
  - RL attempts/successes/failures 数字可被 evaluation 读取。
  - 已完成: `EvaluationRecord` 和 `records.csv` 直接导出 `analytic_operator`, `analytic_attempts`, `analytic_successes`, `analytic_failure_count`, `rl_rollout_steps`, `terminal_rs_success_count`, `terminal_rs_used_count`, `rl_rs_checkpoint`, `rl_rs_checkpoint_sha256` 等 flat columns。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py -q` -> `3 passed in 0.20s`。
  - CLI smoke: `0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/eval/records.csv` 3/3 rows 含 `ha_rl_rs_ppo`, `rl_rs_funnel_ppo`, checkpoint path/hash, analytic attempts/successes/failure count。
  - 记录: `.pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md`。
- [x] G02.4 BC checkpoint-backed analytic operator main evaluation 接入。
  - 已完成: `bc_analytic_operator` 成为 main evaluation 显式方法名, 缺 `--module2-bc-checkpoint` 或 checkpoint 不存在时 preflight hard-fail。
  - 语义: formal-v2 obstacle-summary BC checkpoint 输出 steering, 复用 `RlRsFunnelOperator` 进入 Hybrid A* analytic expansion slot, 并用 terminal RS 完成连接判定。
  - telemetry: `records.csv` 现在直接导出 `bc_checkpoint`, `bc_checkpoint_sha256` flat columns。
  - 不训练 smoke: `0_trials/module2_operator_integration_smoke/bc_operator_smoke/`, `record_count=3`, `status=candidate_or_smoke`, `formal_acceptance=false`, 3/3 rows `analytic_operator=rl_rs_funnel_bc`, checkpoint hash `3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683`。
  - 验证: `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py -q` -> `4 passed in 0.19s`; `PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py 2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py -k "bc or module2_manifest" -q` -> `8 passed, 6 deselected in 1.16s`。
  - 记录: `.pipeline/experiments/20260704_module2_h01_bc_operator_main_eval.md`。

### Phase H: 主实验

#### H01. 评测协议冻结

- [>] H01.1 生成 module2 v1 evaluation manifest。
  - 方法: HA* no analytic, HA* single RS, HA* Dang multi-RS, F-N3P KNN, F-N3P MLP, BC analytic operator, PPO analytic operator, PPO+RS funnel。
  - 地图: Easy/Complex/Extreme held-out, real SLAM maps。
  - seeds: >=5。
  - queries: 每桶 >=100。
  - 已完成子项: 新增 `build_module2_evaluation_manifest.py`, 生成机器可读 JSON + Markdown manifest。
  - 当前产物: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`, status=`blocked_pending_decisions`; 已传入 BC formal-v2 checkpoint, `bc_analytic_operator=ready`; `ppo_analytic_operator` 已映射到同名 main evaluation method, 但因缺 PPO checkpoint 和 F02.6 pending 仍 blocked。
  - RealMap protocol: 新增 `0_trials/module2_realmap_query_protocol/module2_realmap_query_protocol.json`; status=`frozen`, 两张真实地图各 5 queries, endpoint collision audit 0/0, CSV hash=`36f80e9e69cd41d3658d4d9858b04aee874c93933c85188254c7731565764b59`。
  - F02.6 packet/record guard: H01 manifest 现在可读取 `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json` 和 `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`; 当前 record status=`pending_human_decision`, effective decision=`pending`, 因此即使 CLI 误传 `approved_obstacle_summary`, manifest 仍保持 blocked。
  - 当前 global blockers: `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`。
  - 当前 method-level blockers: `requires_dr_sun_approval`, `f02_6_decision_record_pending`, `missing_module2_rl_rs_checkpoint`。
  - 边界: H01.1 已有可审计 manifest, BC operator、PPO without-terminal-RS operator method 和 realmap query protocol 已解除工程实现 blocker, 但还不是 formal-ready evaluation protocol, 因此标为 `[>]`。PPO checkpoint 必须在 `gpu3070ti-relay` 等远端 GPU 上训练/导出, 禁止本地训练。
  - 记录: `.pipeline/experiments/20260704_module2_h01_evaluation_manifest.md`。
  - 更新记录: `.pipeline/experiments/20260704_module2_h01_bc_operator_main_eval.md`。
  - 更新记录: `.pipeline/experiments/20260704_module2_h01_realmap_query_protocol.md`。
  - 更新记录: `.pipeline/experiments/20260704_module2_h01_ppo_analytic_operator_manifest.md`。
  - 更新记录: `.pipeline/experiments/20260704_module2_h01_f02_6_decision_packet_guard.md`。
  - 更新记录: `.pipeline/experiments/20260704_module2_f02_6_decision_record_protocol.md`。
- [x] H01.2 指标冻结。
  - Contract 主指标: expansions, total wall-clock, timeout failure rate, path quality。
  - 诊断指标: analytic success, terminal RS success, collision checks, fallback count, clearance。
  - 已完成: 新增 `build_module2_metric_protocol.py`, 产出 `0_trials/module2_metric_protocol/module2_metric_protocol.json` 和 `.md`, status=`frozen`。
  - 输出口径: `records.csv.total_time_s` 用于跨方法 wall-clock claim; `summary_by_method_bucket.timeout_failure_count/timeout_failure_rate` 现在显式导出 Contract 的 timeout failure rate; `paired_wilcoxon_expansions()` 与 `paired_wilcoxon_time()` 分别支撑 expansions/time 的配对检验。
  - 边界: 指标已冻结但不代表 formal evaluation 已可运行; H01 formal-ready 仍受 F02.6 pending 和缺 PPO checkpoint 阻塞。
  - 验证: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py 2_experiment/forest_n3p/tests/test_module2_metric_protocol.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` -> `11 passed in 0.80s`。
  - 记录: `.pipeline/experiments/20260704_module2_h01_metric_protocol.md`。

#### H02. 正式评测

- [>] H02.1 本地 targeted smoke。
  - 每方法 3 query, 检查输出格式和无碰撞。
  - preflight: 新增 `build_module2_h02_smoke_preflight.py`, 产出 `0_trials/module2_h02_local_smoke/h02_local_smoke_preflight.json` 和 `.md`; status=`blocked_full_smoke_missing_required_methods`。
  - full-smoke blockers: `ppo_analytic_operator` 和 `ppo_rs_funnel` 均缺 `missing_module2_rl_rs_checkpoint`, 且 F02.6 decision packet 仍 pending。
  - available subset smoke: 已本地跑 `ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator` x 3 queries, 产出 `0_trials/module2_h02_local_smoke/h02_1_available_subset/`; record_count=15, query_count=3, status=`candidate_or_smoke`, formal_acceptance=false, collision_violation_total=0, method_exception_total=0。
  - 统计输出更新: available subset summary 现在包含 `bc_analytic_operator` vs `ha_dang_multi_rs` 的 paired time/expansions tests, 以及 success/failure/timeout bootstrap CI slots; 这只是 runner/stat output smoke, 不是性能 claim。
  - 边界: 这不是 all-method H02.1 完成, 不能填补 PPO 缺 checkpoint, 不能作为 formal 结果; full smoke 仍等待 F02.6 决策和远端 PPO checkpoint。
  - 记录: `.pipeline/experiments/20260704_module2_h02_local_smoke_preflight.md`。
- [ ] H02.2 远端完整运行。
  - 必须同步回本地: stdout/stderr, CSV, manifest, config, checkpoints, source hash。
- [>] H02.3 统计检验。
  - Wilcoxon signed-rank for paired time/expansions。
  - Bootstrap CI for success/failure rate。
  - 已完成基础设施: `write_evaluation_outputs()` 现在写出 `paired_time_tests`, `paired_expansion_tests`, `success_rate_bootstrap_ci`, `failure_rate_bootstrap_ci`, `timeout_failure_rate_bootstrap_ci`。
  - module2 pair: `_stat_pairs()` 现在为 `bc_analytic_operator`, `ppo_analytic_operator`, `ha_rl_rs_ppo` 相对 `ha_dang_multi_rs` 生成配对统计项。
  - 边界: H02.3 formal statistical analysis 仍未完成, 因为 H02.2 远端完整 all-method run 尚未产出正式数据。
  - 记录: `.pipeline/experiments/20260704_module2_h02_statistical_ci_infra.md`。
- [ ] H02.4 Contract 判定。
  - 严格按 `.pipeline/contracts/module2-ppo-funnel-expansion.md:19-39`。
  - 不允许事后改成功定义。

### Phase I: 论文材料

#### I01. Method 图和算法伪代码

- [x] I01.1 画系统图。
  - 必含: HA* open loop, analytic trigger, RL rollout, terminal RS, fallback primitives。
  - 已完成: 新增 code-anchored Draw.io 系统图, 覆盖 HA* search loop、analytic trigger、custom operator dispatch、RL-RS funnel operator、planner-side rollout env、terminal RS certificate、accept shortcut、fallback primitives、Gym training env、checkpointed policy variants、formal evaluation boundary。
  - 产物: `0_trials/module2_system_diagram/module2_system_diagram.drawio`, `0_trials/module2_system_diagram/module2_system_diagram.json`, `0_trials/module2_system_diagram/module2_system_diagram.md`。
  - 验证: Draw.io XML 可解析; manifest 内每个 node 的 code anchor 均反查源码 line/pattern 成功; I01 系统图 + 方法算法测试 2 passed。
  - 边界: 这是论文方法图, 不是 formal result; F02.6 pending 和 PPO checkpoint missing 仍在图中显式标注; PPO formal training 只能走 `gpu3070ti-relay`。
  - 记录: `.pipeline/experiments/20260704_module2_i01_system_diagram.md`。
- [x] I01.2 写 Algorithm 1: RL-RS Funnel Analytic Expansion。
  - 输入/输出对齐代码 protocol。
  - 每一步引用代码实现文件。
  - 已完成: 新增 code-anchored method artifact, Algorithm 1 覆盖 custom analytic operator dispatch、checkpoint policy loading、env reset/step、terminal RS certificate、`None` fallback 语义、terminal-RS on/off 两个方法变体。
  - 产物: `0_trials/module2_method_algorithms/module2_method_algorithms.json`, `0_trials/module2_method_algorithms/module2_method_algorithms.md`。
  - 验证: artifact 内每个 code anchor 均反查源码行和 pattern 成功; 相关 operator/Gym/main-evaluation 单测 19 passed。
  - 边界: 这是论文方法材料, 不是 formal result; PPO formal checkpoint 仍缺, 训练必须走 `gpu3070ti-relay`, 禁止本地训练。
  - 记录: `.pipeline/experiments/20260704_module2_i01_method_algorithms.md`。
- [x] I01.3 写 Algorithm 2: Training Environment。
  - reset, obs, action, terminal, reward。
  - 已完成: Algorithm 2 覆盖 `GymAnalyticExpansionEnv.reset/step`, `ObservationConfig`, scalar+occupancy/EDT patch, continuous steering action, no-progress/oscillation truncation, terminal RS reachability, decomposed reward 和 Gymnasium return tuple。
  - 产物: `0_trials/module2_method_algorithms/module2_method_algorithms.json`, `0_trials/module2_method_algorithms/module2_method_algorithms.md`。
  - 边界: 本项只冻结训练环境方法描述; 不代表 F02.6 已批准, 不代表 PPO 已完成, 不触发本地训练。
  - 记录: `.pipeline/experiments/20260704_module2_i01_method_algorithms.md`。

#### I02. 实验表格

- [>] I02.1 主表。
  - rows: methods。
  - columns: success, timeout, time p50/p95, expansions p50/p95, path inflation, clearance。
  - 已完成子项: 新增 `build_module2_paper_tables.py`, 可从 `records.csv`/`summary.json` 生成 method-level paper table preview。
  - 当前产物: `0_trials/module2_paper_tables/module2_paper_tables.json`, `0_trials/module2_paper_tables/module2_paper_tables.md`。
  - 当前状态: `blocked_no_formal_h02_data`, `formal_claim_allowed=false`; blockers 包含 `h02_verdict_not_formal`, `h01_manifest_not_ready`, `missing_module2_rl_rs_checkpoint`, `missing_ppo_result_rows`。
  - 边界: 当前表只验证 schema 和渲染口径, 不能作为论文结果表; formal 主表必须等 H02.2 all-method formal run。
  - 记录: `.pipeline/experiments/20260704_module2_i02_paper_table_protocol.md`。
- [>] I02.2 消融表。
  - occupancy only vs occupancy+EDT。
  - BC vs PPO。
  - terminal RS on/off。
  - action mask on/off。
  - forward-only vs forward+reverse if enabled。
  - 已完成子项: table protocol 已冻结 planned contrasts, 当前因缺 PPO formal rows 标记 `blocked_missing_formal_data`。
  - 边界: 不能用 available subset smoke 代替 BC vs PPO / terminal-RS on/off 消融。
  - 记录: `.pipeline/experiments/20260704_module2_i02_paper_table_protocol.md`。
- [>] I02.3 失败分析表。
  - oracle no-solution, terminal RS fail, collision, oscillation, compute-overhead fail。
  - 已完成子项: 从 `records.csv.failure_reason` 生成 failure-analysis preview, 分类 timeout/collision/terminal_rs_fail/oscillation/oracle_no_solution/other。
  - 当前状态: `preview_not_formal`; H02 available subset 无 failure rows, 不支持论文 failure claim。
  - 记录: `.pipeline/experiments/20260704_module2_i02_paper_table_protocol.md`。

#### I03. 论文 claim 安全线

- [>] I03.1 可 claim。
  - "在本项目森林程序化地图和指定真实地图上, RL-RS funnel operator 相对 RS analytic expansion 降低..."
  - 必须附对应统计检验。
  - 已完成子项: 新增 `build_module2_claim_safety.py`, 生成 allowed/conditional/prohibited claim guard。
  - 当前允许 claim: Module2 是 HA* 内部 learned analytic-expansion operator, 不是 standalone RL planner; no-warm Gate #3 formal branch 失败, terminal-RS success 29/64=0.453125, 低于 0.8。
  - 当前阻塞: formal performance claim 仍为 `blocked_formal_performance_claims`, blockers 包含 H02 非 formal、H01 未 ready、F02.6 pending、缺 PPO checkpoint/rows。
  - 产物: `0_trials/module2_claim_safety/module2_claim_safety.json`, `0_trials/module2_claim_safety/module2_claim_safety.md`。
  - 记录: `.pipeline/experiments/20260704_module2_i03_claim_safety.md`。
- [x] I03.2 不可 claim。
  - "全局最优"。
  - "完备性增强"。
  - "RL 替代 Hybrid A*"。
  - "泛化到所有森林环境"。
  - 已完成: claim safety artifact 将 `global_optimality`, `completeness_enhancement`, `rl_replaces_hybrid_astar`, `universal_generalization`, `warm_start_approved` 标为 hard-block/prohibited, 并支持 draft-text audit。
  - 边界: 除非后续新 Contract 和 formal evidence 明确证明, 这些 claim 不得进入论文。
  - 记录: `.pipeline/experiments/20260704_module2_i03_claim_safety.md`。

## 6. 当前第一批执行队列

优先级从上到下。每次只拿第一项 `[ ]`。

1. [?] A00.2 刷新项目状态记忆, 关闭旧热区状态。
2. [x] D02.1 基于 C02 patch/connector 需求做神经 policy 前向预算。
3. [x] D02.2 加入干净 CPU/GPU forward 对比与 rollout collision 成本账。
4. [x] D02.3 Gate #1 成本账判定。
5. [x] E01.1 新建 `2_experiment/forest_n3p/rl_rs/` 包和环境 API skeleton。
6. [x] E01.2 harden `AnalyticExpansionEnv.reset/step` around real planner-state context。
7. [x] E01.3 实现 egocentric occupancy/EDT observation patch。
8. [x] E01.4 动作实现。
9. [x] E01.5 终止条件实现。
10. [x] E02.1 success reward 与部署使命一致。
11. [x] E02.2 shaping 分项全部写入 info。
12. [x] E02.3 reward ablation hooks。
13. [x] E03.1 单步运动学测试。
14. [x] E03.2 碰撞测试。
15. [x] E03.3 success set 测试。
16. [x] E03.4 no progress/oscillation 测试。
17. [x] F01.1 从 C02 oracle path 提取 state-action demonstrations。
18. [x] F01.2 数据 manifest。
19. [x] F02.1 训练 BC policy。
20. [!] F02.2 formal-v1 BC baseline 已被 map-cache audit 失效。
21. [!] F02.3 formal-v1 patch-CNN pilot 已被 map-cache audit 失效。
22. [x] F02.4 修复 profile-aware map cache 并重建 formal-v2 corpus。
23. [x] F02.5 在 formal-v2 上重跑 BC baseline。
24. [?] F02.6 PPO warm-start 决策门: evidence-bound decision packet 和 machine-readable decision record 已生成, record 仍为 pending, 仍需 Dr Sun 批准或驳回。
25. [!] F03.5 no-warm formal Gate #3 已失败: `formal_decision=fail`, terminal-RS-success 29/64=0.453125; F02.6 warm-start 决策仍未关闭。
26. [x] G01.4 constructor-level + CLI/script `ha_rl_rs_ppo` operator selection 已完成。
27. [x] G02.1 无模型 stub operator planner integration/fallback 测试。
28. [x] G02.2 checkpoint-backed RL-RS operator loader hard-fail 测试。
29. [x] G02.3 evaluation flat telemetry export 测试。
30. [>] H01.1 module2 v1 evaluation manifest 已生成 blocked/preflight 版本; BC operator、PPO without-terminal-RS operator method、realmap query protocol 和 F02.6 decision-record consumption 已接入, formal-ready 仍受 F02.6 pending 和缺 PPO checkpoint 阻塞。
31. [x] G02.4/H01.1a BC checkpoint-backed analytic operator 已接入 main evaluation, 并完成不训练 3-query smoke。
32. [x] H01.1b RealMap query generation protocol 已冻结, 10 queries / 2 maps, endpoint audit pass。
33. [x] H01.2 指标冻结: metric protocol status=`frozen`, timeout failure rate 已显式输出, expansions/time paired Wilcoxon 统计函数已具备。
34. [>] H02.1 local targeted smoke: available subset 5 methods x 3 queries 已跑通; full all-method smoke 仍受 F02.6 pending 和缺 PPO checkpoint 阻塞。
35. [>] H02.3 统计检验基础设施: success/failure/timeout bootstrap CI 和 module2-vs-Dang paired stats 已接入; formal analysis 等 H02.2 数据。
36. [x] I01.2/I01.3 code-anchored method algorithms 已生成: Algorithm 1 覆盖 RL-RS funnel analytic expansion, Algorithm 2 覆盖 PPO training environment; 仍不代表 formal result 或可本地训练。
37. [x] I01.1 code-anchored Draw.io system diagram 已生成: 图中显式覆盖 HA* loop、analytic trigger、RL rollout、terminal RS certificate 和 fallback primitives, 并标注 F02.6 pending / PPO checkpoint missing / gpu3070ti-relay 训练边界。
38. [>] I02 paper table protocol/preview 已生成: 可从 H02 evaluation outputs 生成主表、消融计划和失败分析 preview; 当前因 H02 非 formal、H01 blocked 和缺 PPO checkpoint 正确阻塞 formal claim。
39. [>] I03 claim safety guard 已生成: 允许方法结构 claim 和 no-warm Gate #3 formal failure claim; formal performance improvement 继续 blocked; 全局最优/完备性增强/RL替代HA*/泛化所有森林等 claim 已 hard-block。

## 7. 完成记录

- 2026-07-03: 创建本文件。依据本地 contract、当前 Hybrid A* 代码、F-N3P inference/evaluation/data 代码、Dang 2022、HOPE、Neural A*、PythonRobotics、Karl Kurzer path_planner 建立最大实现任务分解。
- 2026-07-03: 会话前相关中间态已备份到 commit `640c76bf`。
- 2026-07-03: 完成 A01.1, 新建 `0_trials/module2_rl_rs_evidence/` 证据目录与四个模板/初始证据文件。
- 2026-07-03: 完成 A02.1, 新建 `local_slot_api.md`, 把模块2 API 从 "RL planner" 收紧到 "HA* analytic expansion operator"。
- 2026-07-03: 完成 C02.1 全量 oracle connector, 7860/7860 dedup RS failure nodes 覆盖完成。Full run: Oracle A 6226, Oracle B 6287, connectable 6289; unresolved 1571 全部是 invalid start/goal; non-invalid 6289/6289 connectable; B-only timeout 63。记录见 `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md`。
- 2026-07-03: 完成 C02.2 首批 shape label visual seed, 7 张代表样本 PNG 覆盖 invalid endpoint、goal-annulus B-only timeout rescue、A-only conservative B rejection。记录见 `.pipeline/experiments/20260703_module2_c02_shape_labels.md`。注意: 5 个 `voronoi_skeleton` B-only rows 当前重放失败, 暂不能作为论文证据。
- 2026-07-03: 完成 C02.3 Gate #2 oracle shape 判定。结果是 `gate2_not_failed_scope_narrowed`: "多数节点 oracle 也无解" 失败条件未命中, 但 RL 目标范围被压窄到 invalid endpoint 清洗 + timeout/operator-cost cases。D01/D02 成本账是进入 RL-RS 实现前的必要下一步。记录见 `.pipeline/experiments/20260703_module2_gate2_oracle_shape.md`。
- 2026-07-03: 完成 D01.1 Dang multi-RS analytic cost telemetry。Planner stats 现在能拆分候选半径数、RS solve、sampling、collision check、Dang cost eval、sample/check counts; 常规 evaluation metadata 透传 summary。Smoke artifact 见 `0_trials/module2_cost_accounting/d01_analytic_cost_telemetry_smoke/summary.json`, 记录见 `.pipeline/experiments/20260703_module2_d01_analytic_cost_telemetry.md`。
- 2026-07-03: 完成 D01.2 C01/C02 query-set analytic cost distribution。当前 source-bound run 覆盖 20 queries、8622 analytic attempts、94842 radius candidates; attempt p50/p95/p99 total time 为 0.814/2.025/2.829 ms; analytic expansion 占总 plan time 约 33.2%。记录见 `.pipeline/experiments/20260703_module2_d01_cost_distribution.md`。下一步进入 D02.1, 不可直接跳到 RL 环境或 PPO 训练。
- 2026-07-03: 完成 D02.1 neural policy pure forward budget。新增 `run_policy_forward_budget.py` 和 shape 推导测试; 本机 CPU single-thread 跑 3 models x 2 shapes x 3 batch sizes, 18 aggregate rows / 18000 sample rows。Batch=1 下 64-cell CNN p50 为 0.120/0.162 ms, 128-cell CNN p50 为 0.405/0.520 ms, tiny MLP p50 约 0.011 ms。结论仅限 forward-only: 网络前向暂不是第一堵墙, 但 Gate #1 仍缺 rollout collision + terminal RS + clean CPU/GPU。记录见 `.pipeline/experiments/20260703_module2_d02_policy_forward_budget.md`。
- 2026-07-03: 完成 D02.2 device forward + rollout collision 成本账。新增 `run_rollout_collision_budget.py`; 本机 CPU/MPS、远端 3070 Ti CUDA 跑 forward, C01 dedup failure nodes 跑 deterministic rollout collision + terminal RS proxy。保守组合成本示例: CPU compact CNN 128-cell forward p50 0.392ms + Grid 32-step candidate p50 0.239ms = 0.631ms, 低于 D01 attempt p50 0.814ms; 但这只说明 compute 不应直接杀死方向, 不说明 trained policy 能减少 search。记录见 `.pipeline/experiments/20260703_module2_d02_device_and_rollout_budget.md`。
- 2026-07-03: 完成 D02.3 Gate #1 pre-implementation 成本判定。结果为 `gate1_not_failed_preimplementation_compute_gate`: compute 预算不提前杀死方向, 允许进入 E01 环境 API; 但完整 Gate #1 仍需 trained/integrated operator 的端到端配对评测。记录见 `.pipeline/experiments/20260703_module2_gate1_cost_accounting.md`。
- 2026-07-03: 完成 E01.1 RL-RS API skeleton。新增 `2_experiment/forest_n3p/rl_rs/` 包, 覆盖 actions/env/obs/policy/reward/rollout/telemetry/terminal 九个模块和 API 测试。边界: reward 标为 `pending_e02`, 尚未完成 E01.2/E01.3、BC/PPO 或 planner integration。记录见 `.pipeline/experiments/20260703_module2_e01_rl_rs_api_skeleton.md`。
- 2026-07-03: 完成 E01.2 RL-RS 环境状态机加固。`AnalyticExpansionEnv` 现在测试覆盖 reset/step、碰撞起点拒绝、rollout collision、terminal RS success、budget truncation、done 后继续 step 报错和 info failure/status 字段。记录见 `.pipeline/experiments/20260703_module2_e01_env_state_machine.md`。
- 2026-07-03: 完成 E01.3 egocentric observation patch。`RlRsObservation` 现在包含 occupancy + normalized EDT patch; robot-frame forward alignment、越界 occupied 和 channel stack 均有测试。记录见 `.pipeline/experiments/20260703_module2_e01_observation_patch.md`。
- 2026-07-03: 完成 E01.4 forward-only action space。新增 normalized steering decode、physical clip、forward MotionPrimitive conversion 和 reverse gate 禁止测试; reverse/direction gate 保持未启用。记录见 `.pipeline/experiments/20260703_module2_e01_action_space.md`。
- 2026-07-03: 完成 E01.5 terminal conditions。`AnalyticExpansionEnv` 现在区分 terminal RS success、rollout collision、budget/no-RS truncation、no-progress truncation, 并在 telemetry/info 中记录 `goal_distance_m`, `progress_to_goal_m`, `no_progress_count`。`oscillation` 未 claim 已实现, 后移到 E03.4 定义测试信号。记录见 `.pipeline/experiments/20260703_module2_e01_terminal_conditions.md`。
- 2026-07-03: 完成 E02.1 terminal-RS success reward。`RewardConfig` 与 `compute_terminal_success_reward` 已接入 env; success reward 只由 terminal RS-connectability 触发, 不使用距离阈值替代。记录见 `.pipeline/experiments/20260703_module2_e02_success_reward.md`。
- 2026-07-03: 完成 E02.2 reward shaping terms。`RewardBreakdown` 和 `step.info["reward_terms"]` 现在暴露 terminal/collision/progress/RS-progress/clearance/curvature/path-length/step 分项; 权重仍属待校准, E02.3 ablation hooks 未完成。记录见 `.pipeline/experiments/20260703_module2_e02_reward_shaping_terms.md`。
- 2026-07-03: 完成 E02.3 reward ablation hooks。`RewardTermSwitches` 让每个 reward term 显式可开关, `step.info["reward_ablation"]` 暴露消融状态; 尚未运行 ablation 实验或调权重。记录见 `.pipeline/experiments/20260703_module2_e02_reward_ablation_hooks.md`。
- 2026-07-03: 完成 E03.1 single-step kinematics test。非零 steering rollout 的 `next_state` 和最后一个 sample 已严格对齐 planner `propagate()`。记录见 `.pipeline/experiments/20260703_module2_e03_single_step_kinematics.md`。
- 2026-07-03: 完成 E03.2 collision consistency test。free/blocked rollout path 的 collision flag 已与 shared `GridFootprintChecker.collides_path(samples)` 对齐。记录见 `.pipeline/experiments/20260703_module2_e03_collision_consistency.md`。
- 2026-07-03: 完成 E03.3 terminal RS success set test。直接测试 `check_terminal_rs_connectable()` 在空图和障碍阻挡样例中的 success/failure 语义。记录见 `.pipeline/experiments/20260703_module2_e03_terminal_rs_success_set.md`。
- 2026-07-03: 完成 E03.4 no-progress/oscillation tests。新增 oscillation guard 与 telemetry/reward 连接, 原先未实现的 `oscillation` failure label 已变成可测终止语义。记录见 `.pipeline/experiments/20260703_module2_e03_no_progress_oscillation.md`。
- 2026-07-03: 完成 F01.1 oracle demonstration extraction pipeline。新增 C02 oracle replay extractor, 已产出 oracle A smoke、B-only smoke 和 20-row preview dataset; 尚未声明完整 BC corpus。记录见 `.pipeline/experiments/20260703_module2_f01_oracle_demonstration_extraction.md`。
- 2026-07-03: 完成 F01.2 dataset manifest。`module2_rl_rs_bc/manifest.json` 记录 preview dataset 的 source hash、schema、filters、file hash 和边界; 尚未开始 BC/PPO 训练。记录见 `.pipeline/experiments/20260703_module2_f01_dataset_manifest.md`。
- 2026-07-04: 完成 F02.4 profile-aware map cache 修复与 formal-v2 corpus 重建。formal-v1 在真实 profile 地图下有 4764 colliding demo rows, 因此 F02.2/F02.3 formal-v1 结果失效; formal-v2 产出 83809 demo rows / 1032 source rows, current/next collision audit 均为 0。记录见 `.pipeline/experiments/20260704_module2_f02_map_cache_formal_v2_rebuild.md`。
- 2026-07-04: 完成 F02.5 formal-v2 BC baseline rerun。scalar 0.1m success 38/258; obstacle-summary 0.1m success 67/258; patch+scalar CNN bounded success 63/242; 同口径 bounded eval 下 obstacle-summary 101/242 明显强于 patch-CNN 63/242, 推荐 obstacle-summary 作为 PPO practical warm-start。记录见 `.pipeline/experiments/20260704_module2_f02_formal_v2_mlp_bc_baselines.md`。
- 2026-07-04: 完成 F03.5 no-warm-start formal Gate #3 trial。attempt 01 因 oracle sampler 抽到 profile-aware 重建后碰撞 row 中断, 已修复为跳过无效 rows; attempt 02 完成 100000 timesteps PPO train 和 64 episode eval。formal audit 输出 `formal_decision=fail`, `formal_claim_allowed=true`, `formal_blockers=[]`; terminal-RS-success 29/64=0.453125, 低于 0.8 阈值。记录见 `.pipeline/experiments/20260704_module2_f03_gate3_no_warm_formal_trial.md`。
- 2026-07-04: 完成 F03 no-warm failure analysis。失败主要集中在 hard distribution: `rs_failure_node` 6/24 success、collision 14/24, `heldout_procedural` 2/14 success、truncation 8/14; open_connector 15/15 成功说明基础接线没有整体断裂。训练末 1000 episode 的 `rs_failure_node` success 仍只有 0.365239, 与 formal eval fail 一致。记录见 `.pipeline/experiments/20260704_module2_f03_no_warm_failure_analysis.md`。
- 2026-07-04: 修复 Gate #3 evaluator neural forward timing telemetry。`eval_rl_rs_gate3.py` 现在记录 `model.predict()` wall-clock; smoke summary 写出 `nn_forward_time_s=0.000748333000956336`。同一 no-warm formal model 的 `eval_timing_v2/` 保持 `29/64=0.453125` fail 不变, 并补出 `nn_forward_time_s=0.050569629958772566`。记录见 `.pipeline/experiments/20260704_module2_f03_eval_timing_telemetry.md`。
- 2026-07-04: 完成 G01.1/G01.2 analytic expansion operator protocol 和 DangRsOperator adapter。当前 adapter 暴露统一 `AnalyticExpansionResult` contract, 但仍委托 planner-owned `_try_analytic_expansion()` 且未切换 planner 主循环; 这是后续 RL-RS funnel operator 的接口地基, 不是 planner integration 完成。记录见 `.pipeline/experiments/20260704_module2_g01_operator_protocol.md`。
- 2026-07-04: 完成 G01.3 RL-RS funnel operator skeleton。`RlRsFunnelOperator` 已能用显式 stub policy 执行真实 env rollout, terminal RS success 时追加 planner RS 收尾段, collision/no-progress 时返回 `None` 并保留 telemetry。当前仍未切换 Hybrid A* 主循环、未加载正式 checkpoint、未关闭 F02.6。记录见 `.pipeline/experiments/20260704_module2_g01_rl_rs_funnel_operator_skeleton.md`。
- 2026-07-04: 完成 G02.1 无模型 stub operator planner integration 测试, 并完成 G01.4 的 constructor-level custom operator dispatch 子项。`HybridAStarPlanner(..., analytic_expansion_operator=...)` 现在可调用 custom operator; success path 写入 `stub_direct` telemetry, failure path 返回 `None` 后继续 primitive fallback 并写入 `stub_failing/stub_failure` failure record。CLI/script symbolic operator selection 仍未完成, F02.6 warm-start 决策仍 pending。记录见 `.pipeline/experiments/20260704_module2_g01_operator_dispatch_stub_integration.md`。
- 2026-07-04: 完成 G01.4/G02.2/G02.3 checkpoint-backed RL-RS operator CLI 与 telemetry 闭环。`ha_rl_rs_ppo` 已成为 main evaluation 显式方法; `--module2-rl-rs-checkpoint` 缺失/不存在会 hard-fail; checkpoint loader 可加载 SB3 smoke model; `records.csv` 直接导出 analytic/RL-RS telemetry flat columns。Tiny smoke artifact 在 `0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/`, `record_count=3`, `status=candidate_or_smoke`, `formal_acceptance=false`。F02.6 warm-start 决策仍 pending, 本 smoke 不作性能 claim。记录见 `.pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md`。
- 2026-07-04: 推进 H01.1 module2 v1 evaluation manifest。新增 `build_module2_evaluation_manifest.py`, 产出 `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json` 和 `.md`; status=`blocked_pending_decisions`, scale=`100` queries/bucket、`5` seeds, methods 覆盖 HA* no analytic/single RS/Dang multi-RS、F-N3P KNN/MLP、BC analytic、PPO analytic、PPO+RS funnel。当前 blockers 为 F02.6 pending、BC/PPO analytic operator 未实现、realmap query protocol 未冻结; 因此 H01.1 仍标 `[>]`, 不能 claim formal-ready。记录见 `.pipeline/experiments/20260704_module2_h01_evaluation_manifest.md`。
- 2026-07-04: 完成 BC checkpoint-backed analytic operator main evaluation 接入。`bc_analytic_operator` 已成为显式方法名; `--module2-bc-checkpoint` 缺失/不存在会 hard-fail; formal-v2 obstacle-summary BC checkpoint 可加载成 `rl_rs_funnel_bc`; `records.csv` flat columns 导出 `bc_checkpoint` 和 `bc_checkpoint_sha256`。不训练 smoke 在 `0_trials/module2_operator_integration_smoke/bc_operator_smoke/`, `record_count=3`, `status=candidate_or_smoke`, `formal_acceptance=false`, 3/3 rows 含 checkpoint hash。H01 manifest 已更新为 `bc_analytic_operator=ready`; formal-ready 仍受 F02.6、pure PPO analytic operator、realmap protocol 阻塞。记录见 `.pipeline/experiments/20260704_module2_h01_bc_operator_main_eval.md`。
- 2026-07-04: 完成 RealMap query generation protocol 冻结。新增 `build_module2_realmap_query_protocol.py`, 产出 `0_trials/module2_realmap_query_protocol/module2_realmap_query_protocol.json`、`module2_realmap_queries.csv` 和 `.md`; 两张真实地图各 5 queries, 每图第 0 个为 manifest canonical start/goal, endpoint collision audit 0/0, CSV SHA-256 为 `36f80e9e69cd41d3658d4d9858b04aee874c93933c85188254c7731565764b59`。H01 manifest 已引用该 frozen protocol, `realmap_query_generation_not_frozen` blocker 已移除; formal-ready 仍受 F02.6 和 pure PPO analytic operator 阻塞。记录见 `.pipeline/experiments/20260704_module2_h01_realmap_query_protocol.md`。
- 2026-07-04: 完成 `ppo_analytic_operator` without terminal RS 的 main evaluation 接入和 H01 manifest 状态刷新。实现边界是 PPO rollout 不追加 terminal RS, 只有进入 planner `goal_xy_tol/goal_theta_tol` 才返回 `AnalyticExpansionResult`; 若只是 terminal-RS-connectable 但未到 goal tolerance, 返回 `None`, 防止假成功路径。H01 manifest 已重新生成: `ppo_analytic_operator.main_evaluation_method=ppo_analytic_operator`, global blockers 从 `missing_required_method_implementation` 改为 `missing_module2_rl_rs_checkpoint`; formal-ready 仍受 F02.6 和缺 PPO checkpoint 阻塞。测试: targeted 19 passed, 相邻 operator/env/timing 35 passed。记录见 `.pipeline/experiments/20260704_module2_h01_ppo_analytic_operator_manifest.md`。
- 2026-07-04: 完成 `gpu3070ti-relay` 远端 PPO 执行链路预检。远端 GPU/CUDA/SB3/pyarrow 可用; no-warm formal preflight ready; obstacle-summary warm-start formal preflight 仍按 F02.6 pending 阻塞; 远端 warm-start CUDA smoke 产物已同步回本地并被 audit 判为 `not_formal`。记录见 `.pipeline/experiments/20260704_module2_f03_gpu3070ti_remote_readiness.md`。
- 2026-07-04: 完成 F02.6 warm-start 决策包生成器与证据包。新增 `build_module2_f02_6_warm_start_decision_packet.py`, 输出 JSON/Markdown 决策包, 推荐 obstacle-summary warm-start 但状态保持 `pending_human_decision`; 下一步若 Dr Sun 批准, 正式训练必须走 `gpu3070ti-relay`, 不在本地训练。记录见 `.pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md`。
- 2026-07-04: 完成 H01 manifest 的 F02.6 decision-packet guard。`build_module2_evaluation_manifest.py` 新增 `--warm-start-decision-packet`, 读取 packet 后计算 effective warm-start decision; 当前 pending packet 会把 H01 manifest 维持在 `blocked_pending_decisions`, 并加入 `f02_6_decision_packet_pending` blocker, 防止用 CLI 字符串绕过 Dr Sun 审批门。记录见 `.pipeline/experiments/20260704_module2_h01_f02_6_decision_packet_guard.md`。
- 2026-07-04: 完成 F02.6 decision-record protocol 和 H01 消费入口。新增 `build_module2_f02_6_decision_record.py`, 产出 pending decision record; `build_module2_evaluation_manifest.py` 新增 `--warm-start-decision-record`, 只信任 `decider=Dr Sun` 的 approved/rejected record。当前 H01 manifest 仍为 `blocked_pending_decisions`, formal command 仍 blocked, 本轮未批准 F02.6 且未本地训练。记录见 `.pipeline/experiments/20260704_module2_f02_6_decision_record_protocol.md`。
- 2026-07-04: 完成 H01.2 metric protocol。新增 `build_module2_metric_protocol.py`, 冻结 Contract 主指标与诊断指标; `GroupSummary` 新增 `timeout_failure_count/timeout_failure_rate`; `paired_wilcoxon_expansions()` 与现有 `paired_wilcoxon_time()` 分别支撑 expansions/time 的配对检验; H01.2 artifact status=`frozen` 且 blockers=[]。记录见 `.pipeline/experiments/20260704_module2_h01_metric_protocol.md`。
- 2026-07-04: 推进 H02.1 local targeted smoke。新增 H02.1 preflight artifact, 明确 full all-method smoke 因缺 PPO checkpoint/F02.6 pending 阻塞; 同时实际跑通 available subset 5 methods x 3 queries, `record_count=15`, `collision_violation_total=0`, `method_exception_total=0`, status=`candidate_or_smoke`。记录见 `.pipeline/experiments/20260704_module2_h02_local_smoke_preflight.md`。
- 2026-07-04: 推进 H02.3 statistical CI infrastructure。新增 failure/timeout paired bootstrap CI, module2 operator vs Dang multi-RS paired stat pairs, 并重跑 H02.1 available subset smoke 以确认 summary.json 输出 paired time/expansions 和 success/failure/timeout CI slots。记录见 `.pipeline/experiments/20260704_module2_h02_statistical_ci_infra.md`。
- 2026-07-04: 完成 I01.2/I01.3 code-anchored method algorithms。新增 `build_module2_method_algorithms.py`, 输出 Algorithm 1 RL-RS funnel analytic expansion 和 Algorithm 2 PPO training environment 的 JSON/Markdown, 每个步骤均带本地源码行号锚点; artifact 明确 `local_training_allowed=false`, `remote_training_resource=gpu3070ti-relay`, F02.6 pending 和缺 PPO checkpoint 仍阻塞 formal claim。记录见 `.pipeline/experiments/20260704_module2_i01_method_algorithms.md`。
- 2026-07-04: 完成 I01.1 code-anchored system diagram。新增 `build_module2_system_diagram.py`, 输出 Draw.io/JSON/Markdown 系统图 artifact, 展示 HA* analytic expansion 槽内的 RL-RS operator、terminal RS certificate 和 primitive fallback; artifact 明确 `local_training_allowed=false`, `remote_training_resource=gpu3070ti-relay`, F02.6 pending 和缺 PPO checkpoint 仍阻塞 formal claim。记录见 `.pipeline/experiments/20260704_module2_i01_system_diagram.md`。
- 2026-07-04: 推进 I02 paper table protocol/preview。新增 `build_module2_paper_tables.py`, 从 H02 evaluation outputs 生成 I02.1 主表 preview、I02.2 消融计划和 I02.3 failure-analysis preview; 当前 artifact status=`blocked_no_formal_h02_data`, 明确阻塞项为 H02 非 formal、H01 未 ready、F02.6 pending、缺 PPO checkpoint/rows, 因此不能作为论文结果表。记录见 `.pipeline/experiments/20260704_module2_i02_paper_table_protocol.md`。
- 2026-07-04: 推进 I03 claim safety。新增 `build_module2_claim_safety.py`, 汇总 I01/I02/H01/F02.6/Gate3 audit 生成 allowed/conditional/prohibited claim guard; 当前 formal performance claim blocked, no-warm Gate #3 failure claim allowed only in no-warm scope, 全局最优/完备性增强/RL替代HA*/泛化所有森林/warm-start approved 均 hard-block。记录见 `.pipeline/experiments/20260704_module2_i03_claim_safety.md`。
