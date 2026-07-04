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

- MDPI HTML lines 334-337: https://www.mdpi.com/2076-3417/12/12/5999
- Hybrid A* 两阶段: lines 347, 360-371: https://www.mdpi.com/2076-3417/12/12/5999
- 论文结论说他们是在 analytic expansion phase 改进安全性: lines 433-434: https://www.mdpi.com/2076-3417/12/12/5999

可用结论:

- "RS analytic expansion 快但无视障碍/可能贴障碍" 是可引用问题。
- Dang 2022 是直接相邻 baseline, 但它仍在 RS 家族内多曲率选优, 没有学习闭环避障 steering policy。

### 3.2 HOPE 是强相关竞品, 但不是同一个插槽

HOPE 论文/仓库声称 RL 与 RS 结合, 并与 Hybrid A*、naive PPO/SAC 比较:

- arXiv HTML lines 357-360: https://arxiv.org/html/2405.20579v1
- GitHub README lines 237-238: https://github.com/jiamiya/HOPE
- 训练入口包括 PPO 和 SAC: `https://github.com/jiamiya/HOPE/blob/main/src/train/train_HOPE_ppo.py#L100-L166`, `https://github.com/jiamiya/HOPE/blob/main/src/train/train_HOPE_sac.py#L100-L166`
- `ParkingAgent` 在执行 RS 路径时直接由 `RsPlanner` 输出动作, 否则走 RL agent: `https://github.com/jiamiya/HOPE/blob/main/src/model/agent/parking_agent.py#L49-L95`
- `RsPlanner.set_rs_path()` 把 RS ctypes/lengths 转成动作序列: `https://github.com/jiamiya/HOPE/blob/main/src/model/agent/parking_agent.py#L2-L47`
- 环境动作是 `[steer, speed]`, kinematic single-track model step 更新状态: `https://github.com/jiamiya/HOPE/blob/main/src/env/vehicle.py#L69-L96`
- 环境 reward 里包含 RS distance reward: `https://github.com/jiamiya/HOPE/blob/main/src/env/car_parking_base.py#L186-L227`
- license: GPL-3.0, 不能直接复制进本项目核心代码, 只能概念借鉴或隔离参考。

可用结论:

- HOPE 支持 "RL+RS 组合比 naive RL 更稳" 这个方向。
- HOPE 不是替换 Hybrid A* 内部 analytic expansion。它是 parking env 中 RL agent 和 RS planner 的融合执行。
- 可借鉴: action mask, scene curriculum, RS distance shaping, RS action decomposition。
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
- [ ] A01.2 深读 HOPE 论文和代码。
  - 必读: arXiv method/algorithm/experiment, `parking_agent.py`, `car_parking_base.py`, `vehicle.py`, `model/action_mask.py`, `train_HOPE_ppo.py`, `eval_mix_scene.py`
  - 输出: HOPE 与 ForestNav 插槽差异表。
  - 失败条件: 只读 README 即停止。
- [ ] A01.3 深读 Dang 2022 analytic expansion。
  - 必读: Section 2.1, Section 3, Eq.2-4, experiment table。
  - 输出: 本项目已有 Dang 多曲率实现与论文公式差异。
  - 验证: 对照 `planner.py:204-280` 写逐项匹配/偏离。
- [ ] A01.4 查 "learned connector / learned goal shot / neural steering function"。
  - 查询词: `learned steering function motion planning`, `goal connect neural motion planner`, `RL local connector Hybrid A*`, `Reeds-Shepp neural planner`
  - 输出: 正例、负例、未知项。
  - 判据: 至少 10 个来源, 其中论文 >=5, 代码仓库 >=3。
- [ ] A01.5 许可证审计。
  - 输出: 可复制代码、只能读思想、不可用 三档。
  - 必查: HOPE GPL-3.0, Karl Kurzer BSD-3-Clause, PythonRobotics license, Neural A* license。

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
- [x] F02.2 BC 作为正式 baseline。
  - 目的: 证明 PPO 精调是否真的必要。
  - 失败: 若 BC 已够好, 论文叙事要改成 "imitation initialized neural analytic expansion", PPO 只作 fine-tune。
  - 已完成子项: 生成 formal-v1 corpus, 训练 scalar-observation BC lower-bound, 训练 obstacle-summary BC baseline, 并做 step-aligned 0.1m 闭环评估。
  - formal-v1 corpus: `demonstrations_formal_v1.parquet`, 85514 demo rows, 1035 source rows, Complex/Extreme 基本平衡。
  - scalar BC 结果: validation MAE 0.096 rad; 0.3m rollout success 11/259; 0.1m rollout success 45/259。
  - obstacle-summary BC 结果: validation MAE 0.100 rad; 0.1m rollout success 84/259, collision 164/259。
  - 关键发现: obstacle features 明显提升闭环行为, 但 32.4% success 仍不足以 planner insertion; action MAE 仍会误导。
  - 当前边界: F02.2 已形成正式 BC baseline 证据, 但最大实现还应补 patch+scalar CNN warm-start。
  - 记录: `.pipeline/experiments/20260703_module2_f02_formal_scalar_bc.md`。
  - 记录: `.pipeline/experiments/20260703_module2_f02_obstacle_summary_bc.md`。
- [>] F02.3 patch+scalar CNN BC warm-start。
  - 目的: 直接使用 `(2,64,64)` occupancy/EDT patch + scalar obs, 形成 PPO 前更强的 imitation initialization。
  - metric: 0.1m rollout terminal-RS-success, collision, truncation; action MSE 只作辅助。
  - 判定: 若 CNN-BC 明显强于 obstacle-summary, 用作 PPO warm start; 若仍弱, 记录 BC ceiling 并进入 PPO/curriculum。
  - 已完成子项: 新增 `train_bc_patch_policy.py` 和 CNN forward 单测; preview smoke 与 stronger preview 均可复跑。
  - preview 结果: small CNN 0/5 success, stronger CNN 1/5 success, 均弱于 obstacle-summary preview 4/5。
  - 当前边界: patch CNN 脚本已跑通, 但 formal baseline 未完成, 不可用于 PPO warm start。
  - 下一步: formal-v1 bounded pilot 或修正 CNN 训练协议。
  - 记录: `.pipeline/experiments/20260703_module2_f02_patch_cnn_preview.md`。

#### F03. PPO 最大实现

- [ ] F03.1 选择 RL 库。
  - 候选: stable-baselines3, cleanrl, local minimal PPO。
  - 决策依据: continuous action, vector env, logging, checkpoint, license, reproducibility。
  - 不允许: 手写不可审计的临时 PPO。
- [ ] F03.2 vectorized env。
  - 多 map/query 并行采样。
  - 每个 episode 绑定一个 RS failure node 或 near-goal state。
- [ ] F03.3 curriculum。
  - stage 1: open/simple connector。
  - stage 2: obstacle near but one clear side。
  - stage 3: Complex/Extreme RS failure nodes。
  - stage 4: held-out procedural maps。
- [ ] F03.4 logging。
  - TensorBoard/CSV: reward terms, success, terminal RS success, collision, truncation, rollout length, clearance, curvature rate。
  - 每个 checkpoint 存 config + source hash。
- [ ] F03.5 Gate #3 判定。
  - 通过: 小规模单一密度地图中 RS-connectable terminal success > 80%。
  - 失败: 按 Contract 记录 PPO 不收敛, 不改任务定义。

### Phase G: Planner 集成

#### G01. Operator 接口

- [ ] G01.1 定义 `AnalyticExpansionOperator` protocol。
  - `try_connect(state, goal, context) -> AnalyticExpansionResult | None`
  - result 必含: states, actions, telemetry, terminal_rs_used。
- [ ] G01.2 实现 `DangRsOperator` 适配当前代码。
  - 目的: 新旧 operator 共用 telemetry/evaluation。
- [ ] G01.3 实现 `RlRsFunnelOperator`。
  - 流程: RL rollout -> terminal RS check -> return states/actions。
  - 失败: 返回 None, 不抛异常终止 HA*。
- [ ] G01.4 CLI/config 选择 operator。
  - 默认不变。
  - 实验脚本显式写 operator 名称。

#### G02. 集成测试

- [ ] G02.1 无模型 stub operator 测试。
  - 用 deterministic steering mock 验证 planner 调用和 fallback。
- [ ] G02.2 加载 checkpoint 测试。
  - 缺 checkpoint 必须报错, 不能静默退回 RS 并声称 RL 生效。
- [ ] G02.3 telemetry 测试。
  - RL attempts/successes/failures 数字可被 evaluation 读取。

### Phase H: 主实验

#### H01. 评测协议冻结

- [ ] H01.1 生成 module2 v1 evaluation manifest。
  - 方法: HA* no analytic, HA* single RS, HA* Dang multi-RS, F-N3P KNN, F-N3P MLP, BC analytic operator, PPO analytic operator, PPO+RS funnel。
  - 地图: Easy/Complex/Extreme held-out, real SLAM maps。
  - seeds: >=5。
  - queries: 每桶 >=100。
- [ ] H01.2 指标冻结。
  - Contract 主指标: expansions, total wall-clock, timeout failure rate, path quality。
  - 诊断指标: analytic success, terminal RS success, collision checks, fallback count, clearance。

#### H02. 正式评测

- [ ] H02.1 本地 targeted smoke。
  - 每方法 3 query, 检查输出格式和无碰撞。
- [ ] H02.2 远端完整运行。
  - 必须同步回本地: stdout/stderr, CSV, manifest, config, checkpoints, source hash。
- [ ] H02.3 统计检验。
  - Wilcoxon signed-rank for paired time/expansions。
  - Bootstrap CI for success/failure rate。
- [ ] H02.4 Contract 判定。
  - 严格按 `.pipeline/contracts/module2-ppo-funnel-expansion.md:19-39`。
  - 不允许事后改成功定义。

### Phase I: 论文材料

#### I01. Method 图和算法伪代码

- [ ] I01.1 画系统图。
  - 必含: HA* open loop, analytic trigger, RL rollout, terminal RS, fallback primitives。
- [ ] I01.2 写 Algorithm 1: RL-RS Funnel Analytic Expansion。
  - 输入/输出对齐代码 protocol。
  - 每一步引用代码实现文件。
- [ ] I01.3 写 Algorithm 2: Training Environment。
  - reset, obs, action, terminal, reward。

#### I02. 实验表格

- [ ] I02.1 主表。
  - rows: methods。
  - columns: success, timeout, time p50/p95, expansions p50/p95, path inflation, clearance。
- [ ] I02.2 消融表。
  - occupancy only vs occupancy+EDT。
  - BC vs PPO。
  - terminal RS on/off。
  - action mask on/off。
  - forward-only vs forward+reverse if enabled。
- [ ] I02.3 失败分析表。
  - oracle no-solution, terminal RS fail, collision, oscillation, compute-overhead fail。

#### I03. 论文 claim 安全线

- [ ] I03.1 可 claim。
  - "在本项目森林程序化地图和指定真实地图上, RL-RS funnel operator 相对 RS analytic expansion 降低..."
  - 必须附对应统计检验。
- [ ] I03.2 不可 claim。
  - "全局最优"。
  - "完备性增强"。
  - "RL 替代 Hybrid A*"。
  - "泛化到所有森林环境"。

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
19. [ ] F02.1 训练 BC policy。

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
