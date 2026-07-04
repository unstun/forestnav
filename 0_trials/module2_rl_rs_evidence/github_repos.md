---
origin: ai+web
reviewed: false
created: 2026-07-03
topic: module2 RL-RS GitHub evidence
---

# GitHub 仓库证据表

## jiamiya/HOPE

- URL: https://github.com/jiamiya/HOPE
- Pinned HEAD: `2accab93e8602bd7dac780078a012574cc2cb4d7`
- License: GPL-3.0
- 当前判断: 可借鉴, 不能直接复制核心代码。
- 关键代码:
  - `src/train/train_HOPE_ppo.py#L100-L166`: PPO 训练入口, 创建 `CarParkingWrapper`, `PPO`, `RsPlanner`, `ParkingAgent`。
  - `src/train/train_HOPE_ppo.py#L176-L208`: 训练 loop 每步调用 `parking_agent.choose_action`, env 返回 `path_to_dest` 后再 `set_planner_path()`。
  - `src/train/train_HOPE_sac.py#L155-L166`, `#L191-L213`: SAC 训练使用同一 `RsPlanner`/`ParkingAgent` hybrid 框架。
  - `src/model/agent/parking_agent.py#L2-L47`: `RsPlanner` 将 RS path 的 ctypes/lengths 转为动作序列。
  - `src/model/agent/parking_agent.py#L49-L95`: `ParkingAgent` 在执行 RS 时返回 planner action, 否则调用 RL agent。
  - `src/env/vehicle.py#L69-L96`: kinematic single-track model step。
  - `src/env/car_parking_base.py#L84-L87`: action space 是 `[steer, speed]`。
  - `src/env/car_parking_base.py#L186-L227`: reward 含 RS distance progress。
  - `src/env/car_parking_base.py#L291-L299`: 接近目标且 RS path 存在时, `info['path_to_dest']` 被写入。
  - `src/env/car_parking_base.py#L413-L450`: 枚举 RS paths, 按 path length priority 取 collision-free path。
  - `src/model/action_mask.py#L8-L20`, `#L114-L184`, `#L199-L227`: action mask 预计算 safe step 并影响 action sampling。
  - `src/evaluation/eval_mix_scene.py#L82-L115`, `src/evaluation/eval_utils.py#L31-L84`: evaluation 是 scenario-level agent rollout。
- 与 ForestNav 相容点:
  - 连续 steering action。
  - RS 作为学习过程中的结构化辅助。
  - curriculum/difficulty scene 设计。
  - action mask / safe-action prior 和 RS-distance shaping 可作为重新实现的思路。
- 不相容点:
  - GPL-3.0 许可不适合直接并入。
  - 环境是 parking, 不是 HA* 内部 analytic expansion。
  - 它在 agent 执行层融合 RS, 不是 planner open-list 节点上的 operator。
  - 评测输出是 success/reward/step/path length, 不包含 ForestNav Contract 所需 expansions、planner wall-clock、analytic telemetry。

## omron-sinicx/neural-astar

- URL: https://github.com/omron-sinicx/neural-astar
- License: GitHub API 未返回 SPDX, 需继续核验。
- 当前判断: 相关工作/模块1线索, 不是模块2可复用实现。
- 关键代码:
  - `src/neural_astar/planner/astar.py#L105-L153`: `NeuralAstar` 构造 encoder + differentiable A*。
  - `src/neural_astar/planner/astar.py#L182-L213`: forward 中 encode cost map 后执行 A*。
- 与 ForestNav 相容点:
  - learned search guidance 可用于 related work 和模块1。
- 不相容点:
  - 2D grid cost map guidance, 不生成 non-holonomic analytic edge。

## karlkurzer/path_planner

- URL: https://github.com/karlkurzer/path_planner
- License: BSD-3-Clause
- 当前判断: 可作为 Hybrid A* 工程语义参考。
- 关键代码:
  - `src/algorithm.cpp#L165-L173`: 在节点范围内尝试 Dubins shot, 成功直接返回。
  - `src/algorithm.cpp#L176-L223`: shot 未成功后继续 forward simulation successor expansion。
- 与 ForestNav 相容点:
  - shot/fallback 控制流与本项目 `_try_analytic_expansion()` 语义一致。
- 不相容点:
  - C++/ROS 实现, 不是 RL operator。

## AtsushiSakai/PythonRobotics

- URL: https://github.com/AtsushiSakai/PythonRobotics
- License: MIT, 已打开 `LICENSE` 文件核验。
- 当前判断: 可直接复用少量 MIT 参考实现或作为 baseline, 但本项目已有 RS/HA* 实现, 不应无必要替换。
- 关键代码:
  - `PathPlanning/ReedsSheppPath/reeds_shepp_path_planning.py#L22-L37`: RS Path 数据结构含 lengths/ctypes/directions。
  - `PathPlanning/HybridAStar/hybrid_a_star.py`: 可作为 Python HA* baseline 参考, 需另行行级核验后才可引用。
- 与 ForestNav 相容点:
  - 可辅助检查 RS path 表达。
- 不相容点:
  - 本项目已有 vendored RS 和 wrapper, 不需要替换。

## pkicki/neural_path_planning

- URL: https://github.com/pkicki/neural_path_planning
- License: 未发现 LICENSE, 不能直接复用。
- 当前判断: 只能作为概念线索。
- 关键文件:
  - `models/planner.py`
  - `experiments/planner.py`
  - `ompl_planners/dubins.py`
- 可能价值:
  - 学习多段连续曲线参数, 形态上接近 "learned local maneuver"。
- 当前阻塞:
  - 无许可证。
  - TensorFlow/自定义数据格式。
  - 需进一步确认是否支持 obstacle-aware closed-loop rollout。

## reiniscimurs/DRL-robot-navigation

- URL: https://github.com/reiniscimurs/DRL-robot-navigation
- License: MIT。
- 当前判断: 可借 reward/logging/laser+goal observation 训练套路, 不适合作为模块2代码。
- 关键文件:
  - `TD3/train_velodyne_td3.py`
  - `TD3/velodyne_env.py`
- 不相容点:
  - 差速/ROS/Gazebo navigation。
  - 不含 Ackermann、Reeds-Shepp、HA* analytic expansion。

## sldai/crl_kino

- URL: https://github.com/sldai/crl_kino
- Pinned HEAD: `bb27caae17b6c52b26400bb7697e0d6f07191c34` (`master`)
- License: MIT, `LICENSE:1-21`
- 当前判断: 近正例代码; 可读可借鉴, 但 dynamics/planner slot 不同。
- 关键代码:
  - `crl_kino/planner/rrt_rl.py#L14-L63`: `RRT_RL.steer()` 用 RL policy 从 `from_node` roll out 到 `to_node`, 每步 `env.step(action)`, collision/reach 后停止并加入 tree node。
  - `crl_kino/planner/rrt_rl_estimator.py#L16-L79`: estimator/classifier 影响 parent selection。
  - `crl_kino/planner/rrt_rl_estimator.py#L81-L122`: estimator variant 也用 RL policy 执行 steering rollout。
  - `crl_kino/policy/rl_policy.py#L18-L39`: 加载 DDPG policy。
  - `crl_kino/policy/rl_policy.py#L83-L109`: observation -> action inference。
- 与 ForestNav 相容点:
  - 直接证明 "RL policy as local planner inside RRT tree expansion" 可编码实现。
  - estimator/classifier 思路可映射为未来 terminal-RS-connectable likelihood。
- 不相容点:
  - differential-drive RRT, 不是 Ackermann Hybrid A* analytic expansion。
  - target 是 sampled node, 不是 final goal/terminal RS certificate。

## MRSTechnion/DiTree

- URL: https://github.com/MRSTechnion/DiTree
- Pinned HEAD: `150d0932c13e3edc4fe9144fb822486894418838` (`main`)
- License: GitHub API 未发现 license, 暂不可复制。
- 当前判断: 技术上强相关, 许可证阻塞。
- 关键代码:
  - `planners/RRT.py#L42-L122`: RRT loop 选 node、构造 local map、调用 diffusion sampler、propagate action sequence, collision 后丢弃, success 后返回 path/actions。
  - `policies/fm_policy.py#L53-L212`: sampler 条件化 state/action history、relative goal、local map, 执行 diffusion/flow-matching 迭代, 输出 action sequence。
- 与 ForestNav 相容点:
  - "learned action sampler + classical tree/collision verification" 是强相关设计线索。
- 不相容点:
  - RRT-style planner, 不是 HA* analytic expansion。
  - 无明确 license, 不能复制代码。

## ahq1993/MPNet

- URL: https://github.com/ahq1993/MPNet
- License: MIT, `LICENSE:1-21`
- 当前判断: foundational neural planner, 但不是模块2同槽代码。
- 关键代码:
  - `MPNet/neuralplanner.py#L40-L86`: straight-line discretized `steerTo` / feasibility check。
  - `MPNet/neuralplanner.py#L147-L235`: MLP bidirectional replanning between non-connectable path states。
  - `MPNet/neuralplanner.py#L283-L338`: main loop alternates MLP expansion from start/goal and repairs infeasible path。
- 与 ForestNav 相容点:
  - learned waypoint/path generation 和 hybrid neural/classical repair。
- 不相容点:
  - geometric path planner, not Ackermann/RS/HA* analytic operator。

## ucsdarclab/mpnet_local_planner

- URL: https://github.com/ucsdarclab/mpnet_local_planner
- Pinned branch: `suppl`-related Dynamic MPNet code; repo default `master`
- License: GitHub API 未发现 license。
- 当前判断: non-holonomic neural local planner 代码, license blocked。
- 关键代码:
  - `src/mpnet_plan.cpp#L244-L264`: TorchScript model predicts target point from start/goal/costmap。
  - `src/mpnet_plan.cpp#L286-L383`: iterative path generation checks OMPL path from current to predicted target, appends valid targets, simplifies final path。
  - `src/mpnet_plan.cpp#L385-L424`: RRT* fallback path generation。
- 不相容点:
  - ROS local planner, not ForestNav HA* analytic expansion。
  - license missing。

## ucsdarclab/motion_planning_transformer

- URL: https://github.com/ucsdarclab/motion_planning_transformer
- Pinned HEAD: `70d8973c15f3bfd3bec26aab0b591c7e298d755f` (`suppl`)
- License: GitHub API 未发现 license。
- 当前判断: search-space guidance code, not connector。
- 关键代码:
  - `eval_model_car.py#L128-L208`: OMPL SST setup for car model。
  - `eval_model_car.py#L220-L343`: transformer predicts anchor patches/mask; SST plans with mask。
  - `transformer/Models.py#L89-L164`: map encoder creates patch embeddings。
- 不相容点:
  - outputs search mask, not local trajectory edge。

## tedhuang96/nirrt_star

- URL: https://github.com/tedhuang96/nirrt_star
- Pinned HEAD: `285dd248b7e9c0c23e4b6362fcd6bdc8166457e7` (`main`)
- License: MIT, `LICENSE:1-21`
- 当前判断: learned sampling guidance, not connector。
- 关键代码:
  - `path_planning_classes/nirrt_star_png_2d.py#L56-L130`: RRT* loop samples from learned point cloud with probability `pc_sample_rate`。
  - `path_planning_classes/nirrt_star_png_2d.py#L132-L175`: point cloud classified as path/non-path to bias sampling。
  - `train_pointnet_pointnet2.py#L15-L18`, `#L82-L108`, `#L153-L190`: supervised segmentation classes are optimal path points vs other free points。
- 不相容点:
  - guides sample distribution, does not generate Ackermann/RS connector。

## mihdalal/neuralmotionplanner

- URL: https://github.com/mihdalal/neuralmotionplanner
- Pinned HEAD: `5b1e7095c8031b4f011806ac2a58bbe80a2292e6` (`main`)
- License: GitHub API 未发现 license。
- 当前判断: learned reactive motion planner for Franka; related but not module2 code。
- 关键代码:
  - `neural_mp/real_utils/neural_motion_planner.py#L20-L68`: initializes NeuralMP policy/env。
  - `neural_mp/real_utils/neural_motion_planner.py#L209-L324`: rollout policy accumulates joint trajectory and checks goal pose。
  - `neural_mp/real_utils/neural_motion_planner.py#L326-L420`: batched rollout with test-time optimization and collision count selection。
- 不相容点:
  - manipulator planner, not vehicle Hybrid A* analytic expansion。
