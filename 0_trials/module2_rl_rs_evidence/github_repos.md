---
origin: ai+web
reviewed: false
created: 2026-07-03
topic: module2 RL-RS GitHub evidence
---

# GitHub 仓库证据表

## jiamiya/HOPE

- URL: https://github.com/jiamiya/HOPE
- License: GPL-3.0
- 当前判断: 可借鉴, 不能直接复制核心代码。
- 关键代码:
  - `src/train/train_HOPE_ppo.py#L100-L166`: PPO 训练入口, 创建 `CarParkingWrapper`, `PPO`, `RsPlanner`, `ParkingAgent`。
  - `src/model/agent/parking_agent.py#L2-L47`: `RsPlanner` 将 RS path 的 ctypes/lengths 转为动作序列。
  - `src/model/agent/parking_agent.py#L49-L95`: `ParkingAgent` 在执行 RS 时返回 planner action, 否则调用 RL agent。
  - `src/env/vehicle.py#L69-L96`: kinematic single-track model step。
  - `src/env/car_parking_base.py#L186-L227`: reward 含 RS distance progress。
- 与 ForestNav 相容点:
  - 连续 steering action。
  - RS 作为学习过程中的结构化辅助。
  - curriculum/difficulty scene 设计。
- 不相容点:
  - GPL-3.0 许可不适合直接并入。
  - 环境是 parking, 不是 HA* 内部 analytic expansion。
  - 它在 agent 执行层融合 RS, 不是 planner open-list 节点上的 operator。

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
