---
origin: ai+web+local
reviewed: false
created: 2026-07-04
topic: module2 A01.4 learned connector / learned goal shot / neural steering function survey
---

# A01.4 Learned Connector Survey

## 直观结论

已核验来源里, "learned connector" 这个方向是真实存在的, 不是我们凭空想象:

- S3F 学的是 sampling-based kinodynamic planner 里的 steering function。
- RL-RRT / `crl_kino` 把 RL policy 放进 RRT tree expansion, 作为 local planner/steering。
- Learned Goal-Reaching Controllers 把 RL/SAC local controller 用于 sampling-based planner 的 node expansion。
- DiTree 把 diffusion policy 生成的 action sequence 放进 RRT-style tree, 再做 simulation/collision check。

但这些仍然不是 ForestNav module2 的同槽工作。它们大多属于 RRT/SST/SBP tree expansion、whole neural planner、search-space guidance, 或 manipulator reactive planner。当前未找到已经把 learned/RL connector 精确接入 Hybrid A* analytic expansion / RS shot 槽位, 并保留 "success returns edge, failure falls back to primitive expansion" 语义的公开实现。

因此 A01.4 的结论是: 方向有外部依据, 但 novelty 空间仍在。论文叙事可以写成 "learning local steering has precedent in sampling-based kinodynamic planning; our contribution is to specialize it into the Hybrid A* analytic-expansion slot with terminal RS certification and full fallback/cost accounting."

## 判定标准

A01.4 不是泛搜 "RL path planning"。一个来源越接近本项目, 越应满足:

1. 在一个 search/tree planner 的局部扩展槽位中工作, 而不是替换整个 planner。
2. 输入 current state + local/goal target + obstacle context。
3. 输出连续 state/control trajectory, 或 action sequence, 而不是只输出 cost map / heuristic / sample mask。
4. 做碰撞验证, 失败时 tree/search 继续。
5. 面向 kinodynamic / non-holonomic / vehicle-like dynamics。
6. 可以映射到 ForestNav 的 `HybridAStarPlanner._try_analytic_expansion()` custom operator。

## 来源清单

本轮核验 15 个来源, 其中论文 8 个, 代码仓库 7 个。

| ID | 类型 | 来源 | 核验锚点 | 分类 |
|---|---|---|---|---|
| P1 | paper | Atreya & Biswas 2022, S3F | `1_survey/papers/pdf/Atreya2022S3F.pdf`, pdftotext lines 9-33, 81-100, 233-272, 317-320 | 近正例: learned steering function in RRT* |
| P2 | paper | Chiang et al. 2019, RL-RRT | `1_survey/papers/pdf/Chiang2019RLRRT.pdf`, lines 18-40, 99-120, 131-180, 198-208 | 近正例: RL policy as RRT local planner |
| P3 | paper | Sivaramakrishnan et al. 2021, Learned Goal-Reaching Controllers | `1_survey/papers/pdf/Sivaramakrishnan2021LearnedGoalReachingControllers.pdf`, lines 7-32, 66-91, 119-146, 276-283, 315-328 | 近正例: learned local goal controller in SBMP expansion |
| P4 | paper | Hassidof et al. 2025, DiTree | `1_survey/papers/pdf/Hassidof2025DiTree.pdf`, lines 6-35, 196-275, 287-334, 448-462 | 近正例: diffusion action sampler inside RRT-style SBP |
| P5 | paper | Johnson et al. 2020, Dynamic MPNet | `1_survey/papers/pdf/Johnson2020DynamicMPNet.pdf`, lines 16-25, 87-105, 138-183, 193-211 | 相邻: non-holonomic neural planner + Dubins steering, not HA* shot |
| P6 | paper | Li et al. 2021, MPC-MPNet | `1_survey/papers/pdf/Li2021MPCMPNet.pdf`, lines 20-31, 48-55, 103-109, 128-180, 241-281 | 相邻: learned waypoint generator + MPC local steering |
| P7 | paper | Johnson et al. 2022, Motion Planning Transformers | `1_survey/papers/pdf/Johnson2022MotionPlanningTransformers.pdf`, lines 9-31, 123-133, 195-214, 362-372 | 相邻/负例: learned search-space mask, not connector |
| P8 | paper | Qureshi et al. 2019, MPNet | `1_survey/papers/pdf/Qureshi2019MPNet.pdf`, lines 16-27, 136-173, 195-226, 272-306 | 相邻: whole neural planner / replanning |
| C1 | code | `sldai/crl_kino` | MIT license; `rrt_rl.py:14-63`, `rrt_rl_estimator.py:16-122`, `policy/rl_policy.py:18-39,83-109` | 近正例代码 |
| C2 | code | `MRSTechnion/DiTree` | no GitHub license; `planners/RRT.py:42-122`, `policies/fm_policy.py:53-212` | 近正例代码, license blocked |
| C3 | code | `ahq1993/MPNet` | MIT license; `MPNet/neuralplanner.py:40-86,147-181,183-235,283-338` | 相邻 code |
| C4 | code | `ucsdarclab/mpnet_local_planner` | no GitHub license; `src/mpnet_plan.cpp:244-264,286-383,385-424` | 相邻 code |
| C5 | code | `ucsdarclab/motion_planning_transformer` | no GitHub license; `eval_model_car.py:128-208,220-343`, `transformer/Models.py:89-164` | search-space guidance code |
| C6 | code | `tedhuang96/nirrt_star` | MIT license; `nirrt_star_png_2d.py:56-130,132-175`, `train_pointnet_pointnet2.py:15-18,82-108,153-190` | sample guidance code |
| C7 | code | `mihdalal/neuralmotionplanner` | no GitHub license; `neural_motion_planner.py:20-68,209-324,326-420` | manipulator reactive planner |

## 近正例深读

### P1. S3F: learned steering function for RRT*

可用证据:

- S3F 直接定位在 steering function: paper lines 9-33 说明 RRT*/BIT* 在 kinodynamic planning 中依赖 steering function, S3F 学 time-optimal steering function。
- lines 81-100 明确 steering function `S(xa, xb)` 连接两个 sampled states; exact steering 常需 NLP solver, S3F 目标是替代这个瓶颈。
- lines 233-272 写 S3F-RRT*: 用 learned steering function 生成 connecting control trajectory, 并用 `ObstacleFree(x,T)` 检查障碍。
- lines 317-320 把 correctness 拆为 kinodynamic constraints 和 obstacle avoidance。

对 ForestNav 的意义:

- 强支持 "learned steering function can replace an expensive local connector"。
- 但它是 RRT*/SBP steering function, 不是 Hybrid A* analytic expansion shot。
- S3F 本身不是 obstacle-conditioned policy; 障碍主要通过 planner 的 `ObstacleFree` 验证处理。ForestNav 需要 obstacle-aware rollout policy + terminal RS certificate, 不能照搬为完整解。

### P2/C1. RL-RRT and crl_kino: RL policy as local planner inside RRT

可用证据:

- RL-RRT paper lines 18-40: DRL policy maps sensor observations to actions, used as local planner; reachability estimator predicts time-to-reach; RL-RRT uses both inside RRT。
- lines 99-120: training obstacle-avoiding P2P policy, supervised obstacle-aware reachability estimator, then use policy as local planner in RRT。
- lines 131-180: method overview and AutoRL local planner/reachability estimator details。
- `crl_kino/planner/rrt_rl.py:22-63`: `steer()` explicitly says "using RL policy to steer"; each rollout step calls `policy_forward()`, then `env.step(action)`, breaks on collision/reach, and adds new nodes。
- `crl_kino/planner/rrt_rl_estimator.py:26-79` uses estimator/classifier to choose parent, then `:81-122` uses same RL steering rollout。
- `crl_kino/policy/rl_policy.py:18-39` loads DDPG policy; `:83-109` maps observation to action。

对 ForestNav 的意义:

- 这是最接近 "RL local planner inside a tree expansion" 的已核代码证据。
- 可借鉴: policy rollout as edge generator, reachability estimator as parent/target selector, explicit collision/reach termination。
- 不可直接 claim 同槽: 该实现是 differential-drive RRT, 不是 HA* analytic expansion; target is sampled node, not final goal / terminal-RS-connectable set; collision checker/dynamics与 ForestNav 不同。

### P3. Learned Goal-Reaching Controllers

可用证据:

- paper lines 7-32: RL process trained offline to return low-cost control to reach local goal state without obstacles; online planner generates local goals via medial axis/wavefront/random strategy。
- lines 66-91: proposed node expansion generates local goal, learned controller outputs control, then planner uses propagated edge。
- lines 119-146: controller `π(x,xG)` trained to reach goal set; local goal selection can maximize clearance from obstacles。
- lines 276-283 report RLC finds lower-cost solutions/fewer iterations in tested systems。
- lines 315-328 conclude learned controller + local goal selection improves sampling-based kinodynamic planning; inference time can be further optimized。

对 ForestNav 的意义:

- Supports our "local goal / terminal set + learned controller" framing。
- Not enough as direct solution: controller is trained in obstacle-free environment; obstacle handling is in local goal generation and planner validation, not necessarily in the controller observation。
- Systems are differential-drive/Segway, not Ackermann Hybrid A* analytic shot。

### P4/C2. DiTree

可用证据:

- paper lines 6-35: DiTree combines diffusion policies with sampling-based planners; implementation combines RRT with diffusion-policy action sampler; dynamic car included。
- lines 196-275: DiTree algorithm samples action sequence from policy conditioned on current state/goal/local map, simulates, collision-checks, and preserves probabilistic completeness under full support。
- lines 287-334: implemented in Python with RRT backbone; evaluated on CarMaze and AntMaze。
- lines 448-462: real-world car experiment and conclusion on collision-free planning via tree+diffusion。
- code `planners/RRT.py:42-122`: each iteration samples node, nearest node, creates local map, calls sampler, propagates action sequence, rejects collisions, adds new node, returns when goal reached。
- code `policies/fm_policy.py:53-212`: sampler conditions on state history, previous actions, relative goal, local map; runs diffusion/flow-matching iterations and returns action sequence。

对 ForestNav 的意义:

- Very strong modern evidence for "learned generative action sampler + classical tree/collision verification"。
- Still not exact slot: no Hybrid A*/RS analytic expansion; planner backbone is RRT-style SBP; license is not available through GitHub API, so code is not reusable without manual permission check。

## 相邻但非本插槽

### P5/C4. Dynamic MPNet

- paper lines 16-25: neural planning for non-holonomic robots and Dubins-car indoor experiment。
- lines 87-105: Dynamic MPNet is an iterative neural planner that takes sub-goals from a global C-space planner and finds feasible local paths。
- lines 138-183: training tuple and NeuralPlanner/Steer algorithm; `Steer(x1,x2)` checks feasible path if it exists。
- lines 193-211: Dubins model and Dubins curves used as steering function; ROS navigation-stack integration。
- code `mpnet_plan.cpp:244-264` runs TorchScript model to get target point; `:286-383` iteratively predicts target pose, validates OMPL path segments, simplifies trajectory; `:385-424` has RRT* fallback。

Use: strong related work for non-holonomic neural local planning. Boundary: it is a ROS local planner/whole local path generator, not HA* analytic expansion replacement; repository lacks license metadata。

### P6. MPC-MPNet

- lines 20-31: neural generator/discriminator + MPC; generator outputs informed states, discriminator selects subset, MPC connects states under kinodynamic constraints。
- lines 48-55: local steering function is central to KMP and often requires BVP/trajectory optimization。
- lines 103-109: MPC-MPNet iteratively generates waypoints and local steering trajectories。
- lines 128-180 and 241-281: neural generator predicts waypoints; MPC performs kinodynamic steering, invalid/collision trajectories are rejected or tree expansion continues。

Use: relevant for neural waypoint + classical local steering hybrid design. Boundary: MPC does the actual local connector, not a learned/RL analytic shot; not tied to HA* fallback semantics。

### P7/C5. Motion Planning Transformers

- paper lines 9-31: goal is to restrict search space and reduce nodes, including non-holonomic robots and Nav2 plugin。
- lines 123-133: transformer classifies path-relevant patches; patches create a mask。
- lines 195-214: planner searches masked regions; for Dubins car samples oriented patches and uses RRT*/SST edge connectors。
- lines 362-372: Nav2 plugin and Hybrid A* final plan context。
- code `eval_model_car.py:220-343` predicts anchor patches and passes patch map to SST; `transformer/Models.py:89-164` encoder turns map into patch embeddings。

Use: learned search-space restriction related work. Boundary: not connector/shot; it guides where classical planners search。

### P8/C3. MPNet

- paper lines 16-27: neural planner produces end-to-end collision-free paths from workspace encoding, start, goal。
- lines 136-173: offline encoder/planning network; online incremental bidirectional path generation; `steerTo` only checks whether line segment/path is collision-free。
- lines 195-226: neural/hybrid replanning for non-connectable path segments。
- code `neuralplanner.py:40-86` uses straight-line discretized `steerTo`; `:147-235` replanning calls MLP bidirectionally; `:283-338` main loop generates path and repairs infeasible segments。

Use: foundational neural planner baseline. Boundary: geometric/end-to-end neural path generation, no Ackermann/RS/HA* analytic operator。

### C6. NIRRT*

- code `nirrt_star_png_2d.py:56-130`: RRT* samples from learned point-cloud prediction; `:132-175` classifies path points and updates point cloud。
- `train_pointnet_pointnet2.py:15-18,82-108,153-190`: supervised segmentation of "optimal path points" vs other free points。

Use: learned sampling/search guidance. Boundary: no local connector; 2D/3D point sampling, not vehicle analytic shot。

### C7. NeuralMP

- code `neural_motion_planner.py:20-68`: generalist policy setup for Franka environment。
- `:209-324`: reactive rollout policy generates joint trajectory; success checked by end-effector pose。
- `:326-420`: batched rollout with test-time optimization, collision-count selection。

Use: learned reactive motion planner related work. Boundary: manipulator policy, not tree/HA* connector; no repository license metadata。

## A01.4 对 ForestNav 的具体影响

1. Related work section should not say "no one learns local connectors"; S3F, RL-RRT, Learned Goal-Reaching Controllers, DiTree are direct counterexamples at the SBP/RRT level。
2. Our novelty should be scoped more precisely: learned/RL local connector specialized into Hybrid A* analytic expansion, with terminal RS certificate, failure-to-primitive fallback, and full timing/collision telemetry。
3. Implementation design remains defensible: policy rollout should return a validated edge or `None`; this mirrors tree-expansion learned local planner literature while preserving HA* semantics。
4. A reachability/success estimator is a plausible future extension: RL-RRT and crl_kino use estimator/classifier to bias parent choice; ForestNav could later learn "terminal-RS-connectable likelihood" but A01.4 does not approve that change。
5. DiTree suggests a strong alternative to PPO: diffusion/flow-matching action sampler inside a tree. This is a possible future v2 idea, not a change to the approved PPO contract。
6. License risk is real: crl_kino/MPNet/NIRRT* are MIT, but DiTree/Dynamic MPNet/MPT/NeuralMP have no detected GitHub license; code cannot be copied without manual license confirmation。

## 不可 claim

- 不能 claim A01.4 found an exact public implementation of RL replacing Hybrid A* RS analytic expansion。
- 不能 claim Dynamic MPNet / MPT / MPNet are analytic connectors; they are local planners/search-space guidance/whole neural planners。
- 不能 copy DiTree, mpnet_local_planner, motion_planning_transformer, or NeuralMP code until license is resolved。
- 不能 use any downloaded paper result as ForestNav performance evidence。
- 不能 start training from this survey; F02.6 remains pending and formal training is restricted to `gpu3070ti-relay` after approval。

## A01.4 判定

A01.4 可以标为完成: 已核验至少 10 个来源, 其中论文 8 个、代码仓库 7 个。结论是 learned connector 方向有充分外部依据, 但公开证据中尚未发现与 ForestNav 完全同槽的 "HA* analytic expansion / RS shot replacement"。

下一项应进入 A01.5 license audit, 因为 A01.4 识别出多个无明确许可证但技术上有价值的仓库。
