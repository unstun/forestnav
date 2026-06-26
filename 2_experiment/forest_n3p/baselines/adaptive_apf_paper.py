"""Adaptive APF (Kilic 2026) — 1:1 paper reproduction.

参考论文
--------
Kilic, K. I., Desoeuvres, A., Pedersen, C. B., Vasegaard, A. E., & Nielsen, P.
"Adaptive artificial potential field method for small autonomous vehicles,"
Robotics and Autonomous Systems, 105364, 2026.

参考实现
--------
GitHub: https://github.com/Glawal/APFproject/tree/paper1 (GPL-3.0)
依据 ``pathplanner.py`` 中 FAPF + FDAPF + LocalPlanner + BabyRobot +
MathHelper + Obstacle 1:1 复刻。原仓库镜像位置：
``1_survey/papers/baselines/AdaptiveAPF2026_AutonomousVehicles/repo/``。

本文件目的
--------
忠实复现原论文/原仓库的算法行为，与本项目的 grid + EDT + Ackermann 环境无关。
用于：

  - 算法 sanity check（对照原仓库 8 种变体行为）
  - 论文复现度验证
  - 与本地特化版（``adaptive_apf_local.py``）做对照

8 个 APF 变体（通过 ``version`` 参数选择）
--------
    c   classical (吸引 + 排斥)
    t   c + tangential force
    i   c + inertial force
    it  c + tangential + inertial
    dc  dynamic c (动态系数 + classical)
    dt  dynamic t
    di  dynamic i
    dit dynamic + tangential + inertial   ← 论文最完整版

依赖剥离
--------
原仓库 ``pathplanner.py`` 含 osqp / do_mpc / casadi / autograd / scipy / cProfile
等依赖（用于 MPC、A*、DWA、GA），与 APF 算法无关。本文件仅保留 ``math + time + numpy``。

源码定位
--------
原仓库行号对照（pathplanner.py @ paper1）：

    MathHelper                L28-380
    Obstacle                  L389-406
    BabyRobot                 L408-591
    LocalPlanner              L1656-1877  (仅提取 lm_detection + 工具)
    FAPF                      L1988-2208
    FDAPF                     L2210-2515
"""

# ============================================================================
# Imports
# ============================================================================
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any

import numpy as np


# ============================================================================
# MathHelper（来自原 pathplanner.py L28-380，精简到 APF 必需的 5 个函数）
# ============================================================================

class MathHelper:
    """数学工具类（无实例，仅静态方法）。"""

    @staticmethod
    def angle_diff(a1: float, a2: float) -> float:
        """计算 ``a2 - a1``，结果归一化到 [-pi, pi]。"""
        return (((a2 - a1) + math.pi) % (2 * math.pi)) - math.pi

    @staticmethod
    def angle_sum(a1: float, a2: float) -> float:
        """计算 ``a1 + a2``，结果归一化到 [-pi, pi]。"""
        return (((a2 + a1) + math.pi) % (2 * math.pi)) - math.pi

    @staticmethod
    def get_cartesian_coord(v) -> np.ndarray:
        """极坐标 (r, theta) -> 笛卡尔 (x, y)。"""
        return np.array([
            float(v[0]) * math.cos(float(v[1])),
            float(v[0]) * math.sin(float(v[1])),
        ])

    @staticmethod
    def get_polar_coord(v) -> np.ndarray:
        """笛卡尔 (x, y) -> 极坐标 (r, theta)。"""
        return np.array([
            math.hypot(float(v[0]), float(v[1])),
            math.atan2(float(v[1]), float(v[0])),
        ])

    @staticmethod
    def feed_velocity(v) -> np.ndarray:
        """(speed_norm, speed_angle) -> 笛卡尔速度向量。"""
        return np.array([
            float(v[0]) * math.cos(float(v[1])),
            float(v[0]) * math.sin(float(v[1])),
        ])

    @staticmethod
    def get_angle_vec_cart(v1, v2) -> float:
        """两个笛卡尔向量间的有符号夹角 ``angle_diff(angle(v1), angle(v2))``。"""
        a1 = math.atan2(float(v1[1]), float(v1[0]))
        a2 = math.atan2(float(v2[1]), float(v2[0]))
        return MathHelper.angle_diff(a1, a2)


# ============================================================================
# Obstacle 与 BabyRobot（来自原 pathplanner.py L389-591）
# ============================================================================

class Obstacle:
    """圆形障碍物：position + radius。"""

    def __init__(self, pos, size):
        self.pos = np.asarray(pos, dtype=float)
        self.size = float(size)

    def __eq__(self, obs):
        return (
            self.pos[0] == obs.pos[0]
            and self.pos[1] == obs.pos[1]
            and self.size == obs.size
        )

    def __repr__(self):
        return f"Obstacle({tuple(self.pos)},{self.size})"


class BabyRobot(Obstacle):
    """Simplified bicycle 运动学（``size`` 当作 wheelbase）。

    更新链：``move(acc) -> feed_kinematic -> update_velocity -> update_pos``。
    """

    def __init__(
        self,
        pos,
        theta: float = 0.0,
        speed_norm: float = 0.0,
        speed_angle: float = 0.0,
        speed_max: float = 10.0,
        size: float = 1.0,
        acc_max: float = 1.0,
        brake_max: float = 1.0,
        wheel_angle_max: float = math.pi / 4.0,
        speed_min: float = -5.0,
        wheel_acc_max: float = 2 * math.pi,
    ):
        super().__init__(pos, size)
        self.pos = np.asarray(pos, dtype=float)
        self.theta = float(theta)
        self.speed_norm = float(speed_norm)
        self.speed_angle = float(speed_angle)
        self.velocity = MathHelper.feed_velocity((self.speed_norm, self.speed_angle))
        self.speed_max = float(speed_max)
        self.history_pose: list = []  # [pos, theta, speed_norm, speed_angle, velocity]
        self.acc_max = float(acc_max)
        self.brake_max = float(brake_max)
        self.wheel_angle_max = float(wheel_angle_max)
        self.speed_min = float(speed_min)
        self.wheel_acc_max = float(wheel_acc_max)
        self.wheel_angle: float = 0.0
        self.acc_engine: float = 0.0
        self.wheel_acc: float = 0.0
        self.wheel_desired: float = 0.0

    def pos_update(self, pos):
        for i in range(len(pos)):
            self.pos[i] = float(pos[i])

    def update_wheel_angle(self, dt: float = 0.1):
        self.wheel_angle = MathHelper.angle_sum(self.wheel_angle, dt * self.wheel_acc)
        if abs(self.wheel_angle) > self.wheel_angle_max:
            self.wheel_angle = math.copysign(self.wheel_angle_max, self.wheel_angle)

    def get_wheel_angle(self, dt: float = 0.1):
        need_turn = MathHelper.angle_diff(self.wheel_angle, self.wheel_desired) / dt
        if abs(need_turn) > self.wheel_acc_max:
            self.wheel_acc = math.copysign(self.wheel_acc_max, need_turn)
        else:
            self.wheel_acc = need_turn
        self.update_wheel_angle(dt)

    def feed_kinematic(self, acc: np.ndarray, dt: float = 0.1):
        acc_pol = MathHelper.get_polar_coord(acc)
        wheel_turn_desired = MathHelper.angle_diff(self.theta, acc_pol[1])
        if self.speed_norm < 0:
            wheel_turn_desired = MathHelper.angle_diff(wheel_turn_desired, 0)
        engine_push = float(acc_pol[0])
        if abs(wheel_turn_desired) > math.pi / 2.0:
            engine_push = -engine_push
        if abs(wheel_turn_desired) > abs(self.wheel_angle_max):
            self.wheel_desired = math.copysign(self.wheel_angle_max, wheel_turn_desired)
        else:
            self.wheel_desired = wheel_turn_desired
        self.get_wheel_angle(dt)
        # 注意：原仓库这里 self.brake_max 比较保留为正数语义
        if engine_push < 0 and engine_push < self.brake_max:
            self.acc_engine = -self.brake_max
        elif engine_push > 0 and engine_push > self.acc_max:
            self.acc_engine = self.acc_max
        else:
            self.acc_engine = engine_push

    def update_velocity(self, dt: float = 0.1):
        self.speed_norm = max(
            min(self.speed_norm + dt * self.acc_engine, self.speed_max),
            self.speed_min,
        )
        # Ackermann/bicycle kinematic：theta_dot = v / L * tan(delta)
        self.speed_angle = MathHelper.angle_sum(
            self.speed_angle,
            dt * (self.speed_norm / self.size) * math.tan(self.wheel_angle),
        )
        self.theta = self.speed_angle
        self.velocity = MathHelper.feed_velocity((self.speed_norm, self.speed_angle))

    def update_pos(self, dt: float = 0.1):
        for i in range(len(self.pos)):
            self.pos[i] = self.pos[i] + dt * self.velocity[i]

    def move(self, acc: np.ndarray, dt: float):
        self.feed_kinematic(acc, dt)
        self.update_velocity(dt)
        self.update_pos(dt)


# ============================================================================
# LocalPlanner 基类（来自原 pathplanner.py L1656-1877，提取 APF 必需部分）
# ============================================================================

class LocalPlanner:
    """所有 local planner 的母类。"""

    def __init__(
        self,
        robot: BabyRobot,
        start: np.ndarray,
        goal: np.ndarray,
        obstacles,
        t_start: float = 0.0,
        lookahead_dist: float = 10.0,
    ):
        self.start = np.asarray(start, dtype=float)
        self.goal = np.asarray(goal, dtype=float)
        self.robot = robot
        self.reached: list = [False, 0.0]
        # 注意：obstacles 必须可变（FDAPF 在 lm_detection 后会 append 虚拟障碍）
        self.obstacles = list(obstacles)
        self.t_start = float(t_start)
        self.lookahead_dist = float(lookahead_dist)
        self.nb_collision: list = [0, []]
        self.comp_time: float = 0.0
        self.run_count: int = 0
        self.goal_current = self.goal.copy()

    @staticmethod
    def dist(start, end) -> float:
        return math.hypot(end[0] - start[0], end[1] - start[1])

    def collision_detection(self, t: float) -> bool:
        """检测当前位置是否与任一障碍碰撞（圆-圆相交）。"""
        for j in self.obstacles:
            if (
                np.linalg.norm(self.robot.pos - j.pos) - self.robot.size - j.size
                <= 0
            ):
                self.nb_collision[0] += 1
                self.nb_collision[1].append(t)
                return True
        return False

    def local_minima_detection(
        self,
        vrange: float,
        turning: float,
        lm_time: float,
        dt: float,
        prec: float,
        t: float,
    ):
        """Algorithm 3 — 局部最小检测。

        返回 ``(in_lm: bool, vobs: Obstacle | mean_pose ndarray)``：

        - 若发现回到先前轨迹点（``d < prec`` 且 ``i < pos_end/2``）→ True，虚拟障碍 = 该旧位置
        - 否则若与历史均位置接近且累积转角 > ``turning`` → True，虚拟障碍 = 均位置
        - 都不满足 → False，``mean_pose``（不会被使用）
        """
        sumt = 0.0
        mean_pose = np.array([0.0, 0.0])
        nb_last_pose = int(lm_time / dt)
        if len(self.robot.history_pose) > nb_last_pose + 1:
            pos_start = len(self.robot.history_pose) - nb_last_pose - 1
            pos_end = len(self.robot.history_pose) - 2
            for i in range(pos_start, pos_end):
                if (
                    np.linalg.norm(self.robot.pos - self.robot.history_pose[i][0])
                    < prec
                    and i < pos_end / 2
                ):
                    return (True, Obstacle(self.robot.history_pose[i][0].copy(), 0.0))
                diff = abs(
                    MathHelper.angle_diff(
                        self.robot.history_pose[i][1],
                        self.robot.history_pose[i + 1][1],
                    )
                )
                sumt += diff
                mean_pose = mean_pose + self.robot.history_pose[i + 1][0]
            mean_pose = (1.0 / nb_last_pose) * mean_pose
            if (
                np.linalg.norm(self.robot.pos - mean_pose) < vrange
                and sumt > turning
            ):
                return (True, Obstacle(mean_pose, 0.0))
        return (False, mean_pose)


# ============================================================================
# FAPF：静态版（c / t / i / it 变体）— 原 pathplanner.py L1988-2208
# ============================================================================

class FAPF(LocalPlanner):
    """Flexible APF：静态系数 + 4 力（吸引 / 排斥 / 切向 / 惯性）。"""

    def __init__(
        self,
        robot: BabyRobot,
        start,
        goal,
        obstacles,
        k_rep: float,
        k_attr: float,
        k_dist: float,
        angle_detection: float = math.pi,
        goal_method: str = "goal",
        tangential: bool = False,
        inertia: bool = False,
        t_inertia: float = 1.0,
        k_inertia: float = 1.0,
        linear_repulsion: bool = False,
        acts_on_speed: bool = False,
        attr_look: bool = True,
        lookahead_dist: float = 10.0,
        t_start: float = 0.0,
    ):
        super().__init__(
            robot, start, goal, obstacles,
            t_start=t_start, lookahead_dist=lookahead_dist,
        )
        self.k_rep = float(k_rep)
        self.k_attr = float(k_attr)
        self.k_dist = float(k_dist)
        self.angle_detection = float(angle_detection)
        self.goal_method = str(goal_method)
        self.tangential = bool(tangential)
        self.inertia = bool(inertia)
        self.t_inertia = float(t_inertia)
        self.k_inertia = float(k_inertia)
        self.linear_repulsion = bool(linear_repulsion)
        self.acts_on_speed = bool(acts_on_speed)
        self.attr_look = bool(attr_look)

    # -- 力计算 (Eq.4 / Eq.6) ----------------------------------------------
    def get_repulsive_force(self, obstacles):
        """同时返回排斥力 + 切向力（论文 Eq.4 + Eq.6）。"""
        rep_force = np.array([0.0, 0.0])
        tan_force = np.array([0.0, 0.0])
        for i in obstacles:
            d = float(np.linalg.norm(self.robot.pos - i.pos))
            c_dir = MathHelper.get_cartesian_coord((1.0, self.robot.theta))
            obs_angle = MathHelper.get_angle_vec_cart(c_dir, i.pos - self.robot.pos)
            # obs_angle > 0 => 障碍在机器人左侧
            if (
                d < self.k_dist + self.robot.size + i.size
                and -self.angle_detection <= obs_angle <= self.angle_detection
            ):
                if self.linear_repulsion:
                    nf = (
                        self.k_rep
                        * ((1.0 / d) - (1.0 / self.k_dist))
                        * (self.robot.pos - i.pos)
                    )
                else:
                    # classic (论文 Eq.4 修正版)：用 (d - r1 - r2) 替代 d，
                    # 让排斥力随实际间隙衰减而非中心距。
                    eff_d = d - self.robot.size - i.size
                    if eff_d <= 0.0:
                        eff_d = 1e-6  # 防除零；实际此时已在碰撞
                    nf = (
                        self.k_rep
                        * ((1.0 / eff_d) - (1.0 / self.k_dist))
                        * ((1.0 / eff_d) ** 2)
                        * (eff_d / d)
                        * (self.robot.pos - i.pos)
                    )
                if self.tangential:
                    if obs_angle < 0:
                        nt = np.array([nf[1], -nf[0]])  # 顺时针 90°
                    else:
                        nt = np.array([-nf[1], nf[0]])  # 逆时针 90°
                    tan_force = tan_force + nt
                rep_force = rep_force + nf
        return rep_force, tan_force

    def get_attractive_force(self, goal):
        """论文 Eq.2：带 lookahead 限制的吸引力。"""
        attr_force = self.k_attr * (np.asarray(goal, dtype=float) - self.robot.pos)
        if self.attr_look and np.linalg.norm(attr_force) > self.lookahead_dist:
            attr_force = attr_force / np.linalg.norm(attr_force) * self.lookahead_dist
        return attr_force

    def get_inertia(self, dt: float):
        """论文 Eq.7：历史速度均值 * k_inertia，接近 goal 时按比例衰减。"""
        inertia = np.array([0.0, 0.0])
        nb_iner = max(1, int(self.t_inertia / dt))
        if len(self.robot.history_pose) > nb_iner:
            for i in self.robot.history_pose[-nb_iner:-1]:
                inertia = inertia + i[4]
            inertia = inertia / nb_iner
        elif len(self.robot.history_pose) > 0:
            for i in self.robot.history_pose:
                inertia = inertia + i[4]
            inertia = inertia / len(self.robot.history_pose)
        dist_to_goal = float(np.linalg.norm(self.goal - self.robot.pos))
        if dist_to_goal < self.lookahead_dist:
            return self.k_inertia * inertia * (dist_to_goal / self.lookahead_dist)
        return self.k_inertia * inertia

    def plan(self, dt: float, t: float):
        """计算 4 力之和（无 lm 检测、无 dynamic 系数调整）。"""
        net_force = np.array([0.0, 0.0])
        if t >= self.t_start and not self.reached[0]:
            (rep_force, tan_force) = self.get_repulsive_force(self.obstacles)
            self.goal_current = self.goal  # FAPF 默认 goal_method="goal"
            attr_force = self.get_attractive_force(self.goal_current)
            inertia = self.get_inertia(dt) if self.inertia else np.array([0.0, 0.0])
            net_force = attr_force + rep_force + tan_force + inertia
        return net_force

    def run(self, dt: float, t: float):
        """Algorithm 2 (无 lm 版)：plan + 应用动力学 + 记录 history。"""
        s_t = time.process_time_ns()
        acc = self.plan(dt, t)
        self.robot.move(acc, dt)
        e_t = time.process_time_ns()
        self.comp_time += (e_t - s_t)
        self.run_count += 1
        self.robot.history_pose.append([
            self.robot.pos.copy(),
            self.robot.theta,
            self.robot.speed_norm,
            self.robot.speed_angle,
            self.robot.velocity.copy(),
        ])


# ============================================================================
# FDAPF：动态版（dc / dt / di / dit 变体）— 原 pathplanner.py L2210-2515
# ============================================================================

class FDAPF(LocalPlanner):
    """Flexible Dynamic APF：4 力 + 局部最小检测 + 动态系数调整。"""

    def __init__(
        self,
        robot: BabyRobot,
        start,
        goal,
        obstacles,
        k_rep_min: float,
        k_rep_max: float,
        k_attr_min: float,
        k_attr_max: float,
        k_dist_min: float,
        k_dist_max: float,
        angle_detection: float = math.pi,
        goal_method: str = "goal",
        tangential: bool = False,
        inertia: bool = False,
        t_inertia: float = 1.0,
        k_inertia_min: float = 0.0,
        k_inertia_max: float = 1.0,
        k_inertia: float | None = None,
        linear_repulsion: bool = False,
        acts_on_speed: bool = False,
        k_inertia_change_obs: float = 0.02,
        k_attr_change_obs: float = 0.1,
        k_rep_change_obs: float = 0.5,
        k_dist_change_obs: float = 0.1,
        k_inertia_change_no_obs: float = 0.02,
        k_attr_change_no_obs: float = 0.5,
        k_rep_change_no_obs: float = 0.5,
        k_dist_change_no_obs: float = 1.0,
        attr_look: bool = True,
        lookahead_dist: float = 10.0,
        t_start: float = 0.0,
    ):
        super().__init__(
            robot, start, goal, obstacles,
            t_start=t_start, lookahead_dist=lookahead_dist,
        )
        self.k_rep_min = float(k_rep_min)
        self.k_rep_max = float(k_rep_max)
        self.k_rep = self.k_rep_min  # 原仓库初值
        self.k_attr_min = float(k_attr_min)
        self.k_attr_max = float(k_attr_max)
        self.k_attr = self.k_attr_max  # 原仓库初值
        self.k_dist_min = float(k_dist_min)
        self.k_dist_max = float(k_dist_max)
        self.k_dist = self.k_dist_min
        self.recent_lm: float = 0.0  # lm 计时器（秒）
        self.n_vobs: list = []       # 待加入的虚拟障碍 buffer

        self.angle_detection = float(angle_detection)
        self.goal_method = str(goal_method)
        self.tangential = bool(tangential)
        self.inertia = bool(inertia)
        self.t_inertia = float(t_inertia)
        self.k_inertia_min = float(k_inertia_min)
        self.k_inertia_max = float(k_inertia_max)
        if k_inertia is None:
            self.k_inertia = (self.k_inertia_min + self.k_inertia_max) / 2.0
        else:
            self.k_inertia = float(k_inertia)
        self.linear_repulsion = bool(linear_repulsion)
        self.acts_on_speed = bool(acts_on_speed)
        self.k_inertia_change_obs = float(k_inertia_change_obs)
        self.k_attr_change_obs = float(k_attr_change_obs)
        self.k_rep_change_obs = float(k_rep_change_obs)
        self.k_dist_change_obs = float(k_dist_change_obs)
        self.k_inertia_change_no_obs = float(k_inertia_change_no_obs)
        self.k_attr_change_no_obs = float(k_attr_change_no_obs)
        self.k_rep_change_no_obs = float(k_rep_change_no_obs)
        self.k_dist_change_no_obs = float(k_dist_change_no_obs)
        self.attr_look = bool(attr_look)

    def set_dynamic_constant_forces(self, in_lm: bool, dt: float):
        """Algorithm 4 — 根据是否处于近期 lm 调整 4 个系数 + 接近 goal 时衰减 k_rep。"""
        if in_lm:
            self.k_rep = min(self.k_rep * (1 + self.k_rep_change_obs * dt), self.k_rep_max)
            self.k_attr = max(self.k_attr * (1 - self.k_attr_change_obs * dt), self.k_attr_min)
            self.k_inertia = max(
                self.k_inertia * (1 - self.k_inertia_change_obs * dt), self.k_inertia_min
            )
            self.k_dist = min(self.k_dist * (1 + self.k_dist_change_obs * dt), self.k_dist_max)
        else:
            self.k_rep = max(self.k_rep * (1 - self.k_rep_change_no_obs * dt), self.k_rep_min)
            self.k_attr = min(self.k_attr * (1 + self.k_attr_change_no_obs * dt), self.k_attr_max)
            self.k_inertia = max(
                self.k_inertia * (1 + self.k_inertia_change_no_obs * dt), self.k_inertia_max
            )
            self.k_dist = max(self.k_dist * (1 - self.k_dist_change_no_obs * dt), self.k_dist_min)
        # 接近 goal：抑制排斥力以便能停在 goal 附近
        dist_to_goal = float(np.linalg.norm(self.robot.pos - self.goal))
        if dist_to_goal < self.k_dist:
            self.k_rep = self.k_rep * (dist_to_goal / self.k_dist) ** 2

    # -- 力计算（与 FAPF 等价，因为原仓库两个类各自独立维护）-----------------
    def get_repulsive_force(self, obstacles):
        rep_force = np.array([0.0, 0.0])
        tan_force = np.array([0.0, 0.0])
        for i in obstacles:
            d = float(np.linalg.norm(self.robot.pos - i.pos))
            c_dir = MathHelper.get_cartesian_coord((1.0, self.robot.theta))
            obs_angle = MathHelper.get_angle_vec_cart(c_dir, i.pos - self.robot.pos)
            if (
                d < self.k_dist + self.robot.size + i.size
                and -self.angle_detection <= obs_angle <= self.angle_detection
            ):
                if self.linear_repulsion:
                    nf = (
                        self.k_rep
                        * ((1.0 / d) - (1.0 / self.k_dist))
                        * (self.robot.pos - i.pos)
                    )
                else:
                    eff_d = d - self.robot.size - i.size
                    if eff_d <= 0.0:
                        eff_d = 1e-6
                    nf = (
                        self.k_rep
                        * ((1.0 / eff_d) - (1.0 / self.k_dist))
                        * ((1.0 / eff_d) ** 2)
                        * (eff_d / d)
                        * (self.robot.pos - i.pos)
                    )
                if self.tangential:
                    if obs_angle < 0:
                        nt = np.array([nf[1], -nf[0]])
                    else:
                        nt = np.array([-nf[1], nf[0]])
                    tan_force = tan_force + nt
                rep_force = rep_force + nf
        return rep_force, tan_force

    def get_attractive_force(self, goal):
        attr_force = self.k_attr * (np.asarray(goal, dtype=float) - self.robot.pos)
        if self.attr_look and np.linalg.norm(attr_force) > self.lookahead_dist:
            attr_force = attr_force / np.linalg.norm(attr_force) * self.lookahead_dist
        return attr_force

    def get_inertia(self, dt: float):
        inertia = np.array([0.0, 0.0])
        nb_iner = max(1, int(self.t_inertia / dt))
        if len(self.robot.history_pose) > nb_iner:
            for i in self.robot.history_pose[-nb_iner:-1]:
                inertia = inertia + i[4]
            inertia = inertia / nb_iner
        elif len(self.robot.history_pose) > 0:
            for i in self.robot.history_pose:
                inertia = inertia + i[4]
            inertia = inertia / len(self.robot.history_pose)
        dist_to_goal = float(np.linalg.norm(self.goal - self.robot.pos))
        if dist_to_goal < self.lookahead_dist:
            return self.k_inertia * inertia * (dist_to_goal / self.lookahead_dist)
        return self.k_inertia * inertia

    def plan(self, dt: float, t: float):
        """Algorithm 2（完整版）：lm 检测 + 动态系数调整 + 4 力。"""
        net_force = np.array([0.0, 0.0])
        if t >= self.t_start and not self.reached[0]:
            in_lm = False
            if abs(self.recent_lm) < dt:
                # lm 计时器到期：尝试将之前缓存的虚拟障碍真正注入 obstacles
                while len(self.n_vobs) >= 1:
                    self.obstacles.append(self.n_vobs.pop())
                (in_lm, n_pos) = self.local_minima_detection(
                    vrange=self.robot.speed_max * 2.0,
                    turning=2 * math.pi,
                    lm_time=6.0,
                    dt=dt,
                    prec=0.1,
                    t=t,
                )
                if in_lm:
                    self.recent_lm = 2.0  # 进入 lm 状态 2 秒
                    self.n_vobs.append(n_pos)
            else:
                self.recent_lm -= dt
            # 仅在 dt < recent_lm <= 2 秒窗口内，按 in_lm 模式调整
            self.set_dynamic_constant_forces(dt < self.recent_lm <= 2.0, dt)
            (rep_force, tan_force) = self.get_repulsive_force(self.obstacles)
            self.goal_current = self.goal
            attr_force = self.get_attractive_force(self.goal_current)
            inertia = self.get_inertia(dt) if self.inertia else np.array([0.0, 0.0])
            net_force = attr_force + rep_force + tan_force + inertia
        return net_force

    def run(self, dt: float, t: float):
        s_t = time.process_time_ns()
        acc = self.plan(dt, t)
        self.robot.move(acc, dt)
        e_t = time.process_time_ns()
        self.comp_time += (e_t - s_t)
        self.run_count += 1
        self.robot.history_pose.append([
            self.robot.pos.copy(),
            self.robot.theta,
            self.robot.speed_norm,
            self.robot.speed_angle,
            self.robot.velocity.copy(),
        ])


# ============================================================================
# 顶层入口：plan_apf_paper（Algorithm 1 simulate 主循环）
# ============================================================================

@dataclass
class PaperPlannerResult:
    """Paper 版规划结果（与项目 ``PlannerResult`` 解耦）。"""

    path_xy: list           # [(x, y), ...] — 全程轨迹
    time_s: float           # wall-clock 耗时（秒）
    success: bool           # = reached
    reached: bool
    collided: bool
    n_collisions: int
    n_steps: int
    final_pos: tuple = (0.0, 0.0)
    stats: dict = field(default_factory=dict)


VARIANT_KWARGS: dict = {
    "c":   {"tangential": False, "inertia": False, "dynamic": False},
    "t":   {"tangential": True,  "inertia": False, "dynamic": False},
    "i":   {"tangential": False, "inertia": True,  "dynamic": False},
    "it":  {"tangential": True,  "inertia": True,  "dynamic": False},
    "dc":  {"tangential": False, "inertia": False, "dynamic": True},
    "dt":  {"tangential": True,  "inertia": False, "dynamic": True},
    "di":  {"tangential": False, "inertia": True,  "dynamic": True},
    "dit": {"tangential": True,  "inertia": True,  "dynamic": True},
}


def plan_apf_paper(
    *,
    obstacles,
    start,
    goal,
    version: str = "dit",
    dt: float = 0.1,
    t_lim: float = 30.0,
    goal_tolerance: float = 1.0,
    # robot kinematic
    speed_max: float = 10.0,
    size: float = 1.0,
    wheel_angle_max: float = math.pi / 4.0,
    speed_min: float = -5.0,
    acc_max: float = 1.0,
    brake_max: float = 1.0,
    # APF static params
    k_rep: float = 1.0,
    k_attr: float = 1.0,
    k_dist: float = 5.0,
    lookahead_dist: float = 10.0,
    # FDAPF dynamic ranges (only used when version is dynamic)
    k_rep_min: float | None = None,
    k_rep_max: float | None = None,
    k_attr_min: float | None = None,
    k_attr_max: float | None = None,
    k_dist_min: float | None = None,
    k_dist_max: float | None = None,
    **planner_kwargs,
) -> PaperPlannerResult:
    """运行 Adaptive APF（Kilic 2026）— Algorithm 1 simulate 主循环。

    Parameters
    ----------
    obstacles : iterable of Obstacle
        障碍物列表，每个 ``Obstacle(pos=(x,y), size=radius)``。
    start, goal : tuple/array of (x, y)
        起点、终点（实数坐标，与 obstacles 同坐标系）。
    version : str
        ``c / t / i / it / dc / dt / di / dit`` 之一，默认 ``"dit"``。
    dt : float
        仿真时间步长（秒），默认 0.1。
    t_lim : float
        最大仿真时间（秒）。
    goal_tolerance : float
        到达判定半径。

    Returns
    -------
    PaperPlannerResult

    Notes
    -----
    1:1 复刻自 https://github.com/Glawal/APFproject/tree/paper1。
    动态系数变体若未传 ``k_*_min/max``，按 ``k_rep / k_attr / k_dist`` 中值
    展开为 [0.5x, 5x] / [0.5x, 1.5x] / [1x, 3x] 默认范围（不在原仓库，仅为
    便利）；如需严格对照原仓库默认参数表，请显式传入。
    """
    if version not in VARIANT_KWARGS:
        raise ValueError(
            f"version must be one of {list(VARIANT_KWARGS)}, got {version!r}"
        )
    cfg = VARIANT_KWARGS[version]

    start_arr = np.asarray(start, dtype=float)
    goal_arr = np.asarray(goal, dtype=float)
    init_theta = math.atan2(goal_arr[1] - start_arr[1], goal_arr[0] - start_arr[0])
    robot = BabyRobot(
        pos=start_arr.copy(),
        theta=init_theta,
        speed_norm=0.0,
        speed_angle=init_theta,
        speed_max=speed_max,
        size=size,
        acc_max=acc_max,
        brake_max=brake_max,
        wheel_angle_max=wheel_angle_max,
        speed_min=speed_min,
    )

    obs_list = list(obstacles)
    if cfg["dynamic"]:
        # 动态版默认参数范围（仅当用户未显式提供时生效）
        _kr_min = float(k_rep_min) if k_rep_min is not None else k_rep * 0.5
        _kr_max = float(k_rep_max) if k_rep_max is not None else k_rep * 5.0
        _ka_min = float(k_attr_min) if k_attr_min is not None else k_attr * 0.5
        _ka_max = float(k_attr_max) if k_attr_max is not None else k_attr * 1.5
        _kd_min = float(k_dist_min) if k_dist_min is not None else k_dist * 1.0
        _kd_max = float(k_dist_max) if k_dist_max is not None else k_dist * 3.0
        planner = FDAPF(
            robot=robot,
            start=start_arr,
            goal=goal_arr,
            obstacles=obs_list,
            k_rep_min=_kr_min, k_rep_max=_kr_max,
            k_attr_min=_ka_min, k_attr_max=_ka_max,
            k_dist_min=_kd_min, k_dist_max=_kd_max,
            tangential=cfg["tangential"],
            inertia=cfg["inertia"],
            lookahead_dist=lookahead_dist,
            **planner_kwargs,
        )
    else:
        planner = FAPF(
            robot=robot,
            start=start_arr,
            goal=goal_arr,
            obstacles=obs_list,
            k_rep=k_rep, k_attr=k_attr, k_dist=k_dist,
            tangential=cfg["tangential"],
            inertia=cfg["inertia"],
            lookahead_dist=lookahead_dist,
            **planner_kwargs,
        )

    t = 0.0
    t_start_wall = time.perf_counter()
    n_steps = 0
    path_xy: list = [tuple(robot.pos.copy())]

    # Algorithm 1: 外层 simulate 主循环
    while t < t_lim:
        if np.linalg.norm(robot.pos - goal_arr) <= goal_tolerance:
            planner.reached[0] = True
            planner.reached[1] = t
            break
        if planner.collision_detection(t):
            break
        planner.run(dt, t)
        path_xy.append(tuple(robot.pos.copy()))
        t += dt
        n_steps += 1

    elapsed = time.perf_counter() - t_start_wall
    return PaperPlannerResult(
        path_xy=path_xy,
        time_s=elapsed,
        success=bool(planner.reached[0]),
        reached=bool(planner.reached[0]),
        collided=bool(planner.nb_collision[0] > 0),
        n_collisions=int(planner.nb_collision[0]),
        n_steps=n_steps,
        final_pos=tuple(robot.pos),
        stats={
            "version": version,
            "comp_time_ns": int(planner.comp_time),
            "run_count": int(planner.run_count),
            "t_simulated": float(t),
            "t_lim": float(t_lim),
            "k_rep_final": float(planner.k_rep),
            "k_attr_final": float(planner.k_attr),
            "k_dist_final": float(planner.k_dist),
        },
    )
