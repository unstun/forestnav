"""Adaptive APF (Kilic 2026) — 本地特化版（grid + EDT + Ackermann）。

参考论文
--------
Kilic, K. I., Desoeuvres, A., Pedersen, C. B., Vasegaard, A. E., & Nielsen, P.
"Adaptive artificial potential field method for small autonomous vehicles,"
Robotics and Autonomous Systems, 105364, 2026.

本文件目的
--------
保留原论文 4 力（吸引 / 排斥 / 切向 / 惯性）+ 局部最小检测 + 动态系数调整
的核心算法，将原仓库（``adaptive_apf_paper.py``）的环境抽象**适配到本项目**：

  - 原论文 ``Obstacle list (pos + size)`` → ``GridMap + EDT 距离场``
  - 原论文 simplified bicycle (``size`` 当 wheelbase) → ``AckermannParams``
    (wheelbase=0.6m, delta_max=27°, v_max=2 m/s)
  - 原论文 ``BabyRobot.move()`` → ``simulate_forward()``（项目共享 Ackermann 积分）
  - 原论文 ``PaperPlannerResult`` → ``PlannerResult``（与其他 baseline 统一接口）

核心算法不变
--------
1. **F_attr** — 论文 Eq.2，带 ``lookahead_dist`` 限制
2. **F_rep**  — 论文 Eq.4 改用 EDT 梯度作为方向，
   幅值仍为 ``k_rep · ((1/d) − (1/k_dist)) · (1/d²)``
3. **F_tan**  — 论文 Eq.6，将 F_rep 旋转 ±90°，
   依据障碍相对机器人航向的角度选择方向
4. **F_iner** — 论文 Eq.7，历史速度向量队列均值
5. **lm 检测** — 论文 Algorithm 3，保留位姿历史 deque
6. **动态系数** — 论文 Algorithm 4，与 ``adaptive_apf_paper.FDAPF`` 完全一致

8 个变体（``c / t / i / it / dc / dt / di / dit``）通过 ``version`` 选择。
"""

# ============================================================================
# Imports
# ============================================================================
from __future__ import annotations

import math
import time
from collections import deque
from typing import Any

import numpy as np

from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.common import wrap_angle
from forest_n3p.third_party.pathplan.hybrid_a_star.obstacle_field import (
    compute_obstacle_distance_field,
    query_distance,
)
from forest_n3p.third_party.pathplan.robot import simulate_forward

from forest_n3p.baselines.common import PlannerResult, default_start_theta


# ============================================================================
# 工具：EDT 梯度（远离障碍方向的单位向量）
# ============================================================================

def _edt_unit_gradient(
    dist_field: np.ndarray,
    grid_map: GridMap,
    x: float,
    y: float,
    h: float | None = None,
) -> tuple[np.ndarray, float]:
    """中心差分估计 EDT 梯度，返回（单位梯度向量，原始距离）。

    梯度指向"距离增加最快"的方向，即**远离障碍**的方向；
    若梯度退化（如机器人正好在障碍中心或场为常数），返回零向量。
    """
    if h is None:
        h = 0.5 * float(grid_map.resolution)
    d_x_p = query_distance(dist_field, grid_map, x + h, y)
    d_x_m = query_distance(dist_field, grid_map, x - h, y)
    d_y_p = query_distance(dist_field, grid_map, x, y + h)
    d_y_m = query_distance(dist_field, grid_map, x, y - h)
    d_here = query_distance(dist_field, grid_map, x, y)

    grad = np.array([
        (d_x_p - d_x_m) / (2.0 * h),
        (d_y_p - d_y_m) / (2.0 * h),
    ], dtype=float)
    norm = float(np.linalg.norm(grad))
    if norm < 1e-9:
        return np.zeros(2, dtype=float), float(d_here)
    return grad / norm, float(d_here)


# ============================================================================
# 力计算（4 个力）— 与 adaptive_apf_paper.FAPF 数学等价，但接 EDT/Ackermann
# ============================================================================

def _attractive_force(
    pos: np.ndarray,
    goal: np.ndarray,
    *,
    k_attr: float,
    lookahead_dist: float,
    attr_look: bool,
) -> np.ndarray:
    """论文 Eq.2：``F_attr = k_attr · (G - P)``，可选 lookahead 截断。"""
    a = goal - pos
    f = k_attr * a
    if attr_look:
        n = float(np.linalg.norm(f))
        if n > lookahead_dist:
            f = f * (lookahead_dist / max(n, 1e-12))
    return f


def _repulsive_and_tangential_force(
    pos: np.ndarray,
    theta: float,
    dist_field: np.ndarray,
    grid_map: GridMap,
    *,
    k_rep: float,
    k_dist: float,
    angle_detection: float,
    tangential: bool,
    linear_repulsion: bool,
    footprint_radius: float,
    n_directions: int = 16,
) -> tuple[np.ndarray, np.ndarray, float]:
    """多方向 ray casting 版 ``F_rep`` / ``F_tan`` — 恢复 paper 多障碍求和语义。

    原仓库 (paper) 做法：``for i in obstacles: rep_force += nf_i``，多个障碍共同
    贡献斥力，能在双侧障碍场景产生平衡力。本地 grid 地图无离散障碍，改造为：

    1. 在 ``[-angle_detection, +angle_detection]`` 区间均匀采样 ``n_directions`` 个方向
    2. 每个方向沿射线步进，命中第一个障碍 cell 即停（自动避免一面墙重复计数）
    3. 命中点视为虚拟障碍点 ``p_i``，按 paper Eq.4 公式贡献斥力 ``nf_i``
    4. 切向力按命中方向相对机器人航向的符号 ±90° 旋转（paper Eq.6）

    与单梯度版的关键差异：双侧障碍现在能产生方向相反的斥力对，恢复"窄通道穿越"
    所需的力平衡。

    Returns
    -------
    rep_force, tan_force, d_min : 总斥力、总切向力、机器人位置的全局最近障碍 EDT
    """
    cell_size = float(grid_map.resolution)
    detect_radius = float(k_dist) + float(footprint_radius)
    rep_force = np.zeros(2, dtype=float)
    tan_force = np.zeros(2, dtype=float)

    # d_min: 机器人位置的全局最近障碍距离（用于 stats 与 lm 检测的兼容字段）
    d_min = query_distance(dist_field, grid_map, float(pos[0]), float(pos[1]))

    # 在 [-angle_detection, +angle_detection] 区间均匀采样方向（机器人坐标系）
    if int(n_directions) <= 0:
        return rep_force, tan_force, d_min
    half_span = float(angle_detection)
    if half_span <= 0.0:
        return rep_force, tan_force, d_min
    angles_rel = np.linspace(
        -half_span, +half_span, int(n_directions), endpoint=False
    ) + (half_span / float(n_directions))  # 中心采样避免边界对称重复

    # ray casting 步长 = 半 cell；步数上限按 detect_radius / step
    step = 0.5 * cell_size
    n_steps = max(2, int(math.ceil(detect_radius / step)) + 1)
    # "命中障碍" 判据：该位置 EDT ≤ cell_size（已落入或贴近一个障碍 cell）
    hit_thresh = cell_size

    for ang_rel in angles_rel:
        ang_world = float(ang_rel) + float(theta)
        cos_a = math.cos(ang_world)
        sin_a = math.sin(ang_world)

        # ============================================================
        # ray casting：沿 (cos_a, sin_a) 步进，找第一个障碍 cell
        # ============================================================
        hit_d = 0.0
        hit_x = 0.0
        hit_y = 0.0
        found = False
        for k in range(1, n_steps):
            r = float(k) * step
            if r > detect_radius:
                break
            px = float(pos[0]) + r * cos_a
            py = float(pos[1]) + r * sin_a
            d_at_p = query_distance(dist_field, grid_map, px, py)
            if d_at_p <= hit_thresh:
                hit_d = r
                hit_x = px
                hit_y = py
                found = True
                break
        if not found:
            continue  # 这个方向上 detect_radius 内无障碍

        # ============================================================
        # paper Eq.4 / Eq.6：从虚拟障碍点 (hit_x, hit_y) 贡献斥力 / 切向力
        # ============================================================
        d = float(hit_d)
        if d <= 1e-12:
            continue  # 零距离跳过，避免除零（实际此时已碰撞，主循环会捕获）

        if linear_repulsion:
            f_mag = float(k_rep) * (
                (1.0 / max(d, 1e-6)) - (1.0 / max(float(k_dist), 1e-6))
            )
        else:
            eff_d = d - float(footprint_radius)
            if eff_d <= 0.0:
                eff_d = 1e-6
            f_mag = (
                float(k_rep)
                * ((1.0 / eff_d) - (1.0 / max(float(k_dist), 1e-6)))
                * ((1.0 / eff_d) ** 2)
                * (eff_d / max(d, 1e-6))
            )

        # 斥力方向：从障碍点指向机器人（与原仓库 robot.pos − obs.pos 一致）
        dir_x = (float(pos[0]) - hit_x) / max(d, 1e-12)
        dir_y = (float(pos[1]) - hit_y) / max(d, 1e-12)
        nf_x = f_mag * dir_x
        nf_y = f_mag * dir_y
        rep_force[0] += nf_x
        rep_force[1] += nf_y

        if tangential:
            # paper Eq.6：障碍在右（ang_rel < 0）→ 顺时针 90°；在左 → 逆时针 90°
            if float(ang_rel) < 0.0:
                tan_force[0] += +nf_y
                tan_force[1] += -nf_x
            else:
                tan_force[0] += -nf_y
                tan_force[1] += +nf_x

    return rep_force, tan_force, float(d_min)


def _inertial_force(
    history_velocity: list,
    *,
    k_inertia: float,
    t_inertia: float,
    dt: float,
    pos: np.ndarray,
    goal: np.ndarray,
    lookahead_dist: float,
) -> np.ndarray:
    """论文 Eq.7：历史速度均值 × k_inertia，接近 goal 时按比例衰减。"""
    if not history_velocity:
        return np.zeros(2, dtype=float)
    nb_iner = max(1, int(t_inertia / dt))
    if len(history_velocity) > nb_iner:
        window = history_velocity[-nb_iner:-1]
    else:
        window = history_velocity[:]
    if not window:
        return np.zeros(2, dtype=float)
    inertia = np.mean(np.asarray(window, dtype=float), axis=0)
    dist_to_goal = float(np.linalg.norm(goal - pos))
    if dist_to_goal < lookahead_dist:
        return k_inertia * inertia * (dist_to_goal / max(lookahead_dist, 1e-12))
    return k_inertia * inertia


# ============================================================================
# 局部最小检测（论文 Algorithm 3）
# ============================================================================

def _local_minima_detection(
    history_pose: list,
    cur_pos: np.ndarray,
    *,
    vrange: float,
    turning: float,
    lm_time: float,
    dt: float,
    prec: float,
) -> tuple[bool, np.ndarray]:
    """论文 Algorithm 3。

    Parameters
    ----------
    history_pose : list of (pos: ndarray(2), theta: float)
    cur_pos : ndarray(2)

    Returns
    -------
    (in_lm, virtual_obs_pos)：``virtual_obs_pos`` 仅在 ``in_lm=True`` 时有意义。
    """
    nb_last = int(lm_time / dt)
    if len(history_pose) <= nb_last + 1:
        return False, np.zeros(2, dtype=float)

    pos_start = len(history_pose) - nb_last - 1
    pos_end = len(history_pose) - 2
    sumt = 0.0
    mean_pose = np.zeros(2, dtype=float)

    for i in range(pos_start, pos_end):
        prev_pos, prev_theta = history_pose[i]
        nxt_pos, nxt_theta = history_pose[i + 1]
        if (
            float(np.linalg.norm(cur_pos - prev_pos)) < prec
            and i < pos_end / 2
        ):
            return True, prev_pos.copy()
        diff = abs(wrap_angle(nxt_theta - prev_theta))
        sumt += diff
        mean_pose = mean_pose + nxt_pos
    mean_pose = mean_pose / nb_last
    if (
        float(np.linalg.norm(cur_pos - mean_pose)) < vrange
        and sumt > turning
    ):
        return True, mean_pose
    return False, mean_pose


# ============================================================================
# 动态系数调整（论文 Algorithm 4，与 adaptive_apf_paper.FDAPF 一致）
# ============================================================================

def _set_dynamic_constants(coef: dict, *, in_lm: bool, dt: float, dist_to_goal: float):
    """就地更新 coef 字典中的 ``k_rep / k_attr / k_inertia / k_dist``。"""
    if in_lm:
        coef["k_rep"] = min(coef["k_rep"] * (1 + coef["dr_obs"] * dt), coef["k_rep_max"])
        coef["k_attr"] = max(coef["k_attr"] * (1 - coef["da_obs"] * dt), coef["k_attr_min"])
        coef["k_inertia"] = max(
            coef["k_inertia"] * (1 - coef["di_obs"] * dt), coef["k_inertia_min"]
        )
        coef["k_dist"] = min(coef["k_dist"] * (1 + coef["dd_obs"] * dt), coef["k_dist_max"])
    else:
        coef["k_rep"] = max(coef["k_rep"] * (1 - coef["dr_no"] * dt), coef["k_rep_min"])
        coef["k_attr"] = min(coef["k_attr"] * (1 + coef["da_no"] * dt), coef["k_attr_max"])
        coef["k_inertia"] = max(
            coef["k_inertia"] * (1 + coef["di_no"] * dt), coef["k_inertia_max"]
        )
        coef["k_dist"] = max(coef["k_dist"] * (1 - coef["dd_no"] * dt), coef["k_dist_min"])
    if dist_to_goal < coef["k_dist"]:
        coef["k_rep"] = coef["k_rep"] * (dist_to_goal / max(coef["k_dist"], 1e-9)) ** 2


# ============================================================================
# 力 → Ackermann 控制（v_des, steering）
# ============================================================================

def _force_to_ackermann_command(
    f_total: np.ndarray,
    state: AckermannState,
    params: AckermannParams,
    *,
    heading_kp: float = 1.5,
) -> tuple[float, float]:
    """将 APF 合力转换为 Ackermann (v, steering) 控制命令。

    策略
    ----
    - ``v_des = min(|F_total|, v_max)``，把合力幅值当作期望线速度
    - ``steering`` 由 P 控制 + ``max_steer`` 截断：
      ``steering = clip(K_p · (desired_heading − state.theta), ±max_steer)``
    - 若 ``|F_total| < eps``，输出 (0, 0) 让车原地停留
    """
    f_mag = float(np.linalg.norm(f_total))
    if f_mag < 1e-9:
        return 0.0, 0.0
    desired_heading = math.atan2(float(f_total[1]), float(f_total[0]))
    heading_err = wrap_angle(desired_heading - float(state.theta))
    steering = heading_kp * heading_err
    max_steer = params.max_steer
    steering = max(-max_steer, min(max_steer, steering))
    v_des = min(f_mag, params.v_max)
    return v_des, steering


# ============================================================================
# 顶层入口：plan_adaptive_apf
# ============================================================================

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


def plan_adaptive_apf(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float = 0.5,
    timeout_s: float = 5.0,
    # APF version + 步长
    version: str = "dit",
    dt: float = 0.1,
    max_steps: int = 1000,
    # APF 静态参数（FAPF 用 / FDAPF 用作动态范围中值）
    k_rep: float = 0.5,
    k_attr: float = 1.0,
    k_dist: float = 1.5,         # 单位 m，影响半径
    lookahead_dist: float = 2.0,  # 单位 m
    # FDAPF 动态范围（不传则用 k_* 中值展开）
    k_rep_min: float | None = None,
    k_rep_max: float | None = None,
    k_attr_min: float | None = None,
    k_attr_max: float | None = None,
    k_dist_min: float | None = None,
    k_dist_max: float | None = None,
    # FDAPF 调整速率（默认值与原仓库一致）
    k_rep_change_obs: float = 0.5,
    k_rep_change_no_obs: float = 0.5,
    k_attr_change_obs: float = 0.1,
    k_attr_change_no_obs: float = 0.5,
    k_dist_change_obs: float = 0.1,
    k_dist_change_no_obs: float = 1.0,
    k_inertia_change_obs: float = 0.02,
    k_inertia_change_no_obs: float = 0.02,
    # 行为参数
    angle_detection: float = math.pi,
    attr_look: bool = True,
    linear_repulsion: bool = False,
    t_inertia: float = 1.0,
    k_inertia_min: float = 0.0,
    k_inertia_max: float = 1.0,
    k_inertia_init: float = 0.5,
    # lm detection 参数
    lm_time: float = 6.0,
    lm_prec: float = 0.1,
    lm_turning: float = 2 * math.pi,
    lm_vrange_factor: float = 2.0,
    lm_active_window: float = 2.0,
    # 控制
    heading_kp: float = 1.5,
    footprint_radius: float | None = None,
    # 诊断模式：开启后每步把力分量+系数+双圆 EDT 距离写入 result.stats["force_trace"]
    log_force_trace: bool = False,
    # 兼容其他 baseline 的占位（不使用）
    collision_padding: float | None = None,
    collision_checker=None,
) -> PlannerResult:
    """运行 Adaptive APF (Kilic 2026) — 本地特化版（grid + EDT + Ackermann）。

    Parameters
    ----------
    grid_map, footprint, params : 与其他 baseline 完全一致
    start_xy, goal_xy : cell 坐标 (int, int)
    version : 8 个变体之一，默认 ``"dit"`` 论文最完整版
    dt : APF 仿真步长（秒）
    max_steps : 最大仿真步数

    Returns
    -------
    PlannerResult — 与 ``plan_hybrid_astar`` / ``plan_rrt_star`` 同接口

    Notes
    -----
    碰撞检测：若传入 ``collision_checker``（如 ``EDTCollisionChecker``），优先调用
    ``collides_pose(x, y, theta)`` 双圆心检测，与 HA*/RRT* 完全一致；
    未传则回退到 ``EDT(state) <= footprint_radius`` 单点检测（更宽松，仅作 fallback）。
    超时同时受 ``timeout_s`` 和 ``max_steps`` 双重限制。
    """
    if version not in VARIANT_KWARGS:
        raise ValueError(
            f"version must be one of {list(VARIANT_KWARGS)}, got {version!r}"
        )
    cfg = VARIANT_KWARGS[version]

    cell_size_m = float(grid_map.resolution)
    st = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    )
    state = AckermannState(
        x=float(start_xy[0]) * cell_size_m,
        y=float(start_xy[1]) * cell_size_m,
        theta=st,
    )
    goal_world = np.array([
        float(goal_xy[0]) * cell_size_m,
        float(goal_xy[1]) * cell_size_m,
    ], dtype=float)

    # footprint 半径（用于排斥力 eff_d 和碰撞检测）
    if footprint_radius is None:
        try:
            # TwoCircleFootprint：两圆半径相同
            footprint_radius = float(footprint.radius)
        except AttributeError:
            try:
                box: OrientedBoxFootprint = footprint  # type: ignore
                footprint_radius = 0.5 * math.hypot(float(box.length), float(box.width))
            except Exception:
                footprint_radius = 0.5

    # EDT 距离场预计算（单次 O(N²) 摊销到所有 step）
    dist_field = compute_obstacle_distance_field(grid_map)

    # APF 系数 dict（FAPF 与 FDAPF 共用接口；FAPF 时 ``dynamic=False`` 不调 set_dynamic）
    coef: dict = {
        "k_rep": float(k_rep),
        "k_attr": float(k_attr),
        "k_dist": float(k_dist),
        "k_inertia": float(k_inertia_init),
        "k_rep_min": float(k_rep_min) if k_rep_min is not None else float(k_rep) * 0.5,
        "k_rep_max": float(k_rep_max) if k_rep_max is not None else float(k_rep) * 5.0,
        "k_attr_min": float(k_attr_min) if k_attr_min is not None else float(k_attr) * 0.5,
        "k_attr_max": float(k_attr_max) if k_attr_max is not None else float(k_attr) * 1.5,
        "k_dist_min": float(k_dist_min) if k_dist_min is not None else float(k_dist) * 1.0,
        "k_dist_max": float(k_dist_max) if k_dist_max is not None else float(k_dist) * 3.0,
        "k_inertia_min": float(k_inertia_min),
        "k_inertia_max": float(k_inertia_max),
        # 调整速率
        "dr_obs": float(k_rep_change_obs),
        "dr_no": float(k_rep_change_no_obs),
        "da_obs": float(k_attr_change_obs),
        "da_no": float(k_attr_change_no_obs),
        "dd_obs": float(k_dist_change_obs),
        "dd_no": float(k_dist_change_no_obs),
        "di_obs": float(k_inertia_change_obs),
        "di_no": float(k_inertia_change_no_obs),
    }
    # FDAPF 初值：原仓库设 k_rep=k_rep_min, k_attr=k_attr_max, k_dist=k_dist_min
    if cfg["dynamic"]:
        coef["k_rep"] = coef["k_rep_min"]
        coef["k_attr"] = coef["k_attr_max"]
        coef["k_dist"] = coef["k_dist_min"]

    # 历史与状态
    history_pose: list = []        # [(pos: ndarray, theta: float), ...]
    history_velocity: list = []    # [velocity_xy: ndarray, ...]
    virtual_obs: list = []         # 虚拟障碍：APF 中通过 k_rep 增加而非添加 obs（local 版用 obs proxy）
    recent_lm: float = 0.0         # lm 计时器（秒）
    n_collisions = 0
    success = False
    end_reason = "max_steps"

    # 输出轨迹（始终用 cell 坐标，与其他 baseline 一致）
    trace_states: list[AckermannState] = [
        AckermannState(state.x, state.y, state.theta)
    ]

    # 诊断模式：每步记录力分量 + 动态系数 + 双圆 EDT
    force_trace_records: list[dict] | None = [] if log_force_trace else None

    # 双圆心 EDT 查询（仅在 log_force_trace 时使用，避免增加正式 run 开销）
    def _two_circle_edt(s_x: float, s_y: float, s_theta: float) -> tuple[float, float, float]:
        """Returns (d_center, d_circle_front, d_circle_rear) in meters."""
        d_center = query_distance(dist_field, grid_map, s_x, s_y)
        try:
            tc: TwoCircleFootprint = footprint  # type: ignore
            (front, rear) = tc.circle_centers(s_x, s_y, s_theta)
            d_front = query_distance(dist_field, grid_map, front[0], front[1])
            d_rear = query_distance(dist_field, grid_map, rear[0], rear[1])
        except Exception:
            d_front = float("nan")
            d_rear = float("nan")
        return float(d_center), float(d_front), float(d_rear)

    t_wall_start = time.perf_counter()
    t_sim = 0.0

    for step in range(int(max_steps)):
        elapsed = time.perf_counter() - t_wall_start
        if elapsed >= float(timeout_s):
            end_reason = "timeout"
            break

        cur_pos = np.array([state.x, state.y], dtype=float)

        # 到达检测
        if float(np.linalg.norm(cur_pos - goal_world)) <= float(goal_xy_tol_m):
            success = True
            end_reason = "reached"
            break

        # 碰撞检测：优先用 collision_checker（双圆心，与 HA*/RRT* 一致），
        # 未传则回退到单点 EDT（更宽松，仅作 fallback）。
        if collision_checker is not None:
            collided = bool(
                collision_checker.collides_pose(state.x, state.y, state.theta)
            )
        else:
            d_here = query_distance(dist_field, grid_map, state.x, state.y)
            collided = bool(d_here <= float(footprint_radius))
        if collided:
            n_collisions += 1
            end_reason = "collision"
            break

        # ---- lm 检测 (Algorithm 3) + 动态系数 (Algorithm 4) — 仅 dynamic 变体 ----
        if cfg["dynamic"]:
            in_lm = False
            if abs(recent_lm) < dt:
                # 计时器到期：检测 lm
                in_lm, vobs_pos = _local_minima_detection(
                    history_pose=history_pose,
                    cur_pos=cur_pos,
                    vrange=params.v_max * float(lm_vrange_factor),
                    turning=float(lm_turning),
                    lm_time=float(lm_time),
                    dt=float(dt),
                    prec=float(lm_prec),
                )
                if in_lm:
                    recent_lm = float(lm_active_window)
                    virtual_obs.append(vobs_pos.copy())
            else:
                recent_lm = max(0.0, recent_lm - dt)
            dist_to_goal = float(np.linalg.norm(cur_pos - goal_world))
            _set_dynamic_constants(
                coef,
                in_lm=(dt < recent_lm <= float(lm_active_window)),
                dt=float(dt),
                dist_to_goal=dist_to_goal,
            )

        # ---- 4 力计算 ----
        f_attr = _attractive_force(
            cur_pos, goal_world,
            k_attr=coef["k_attr"],
            lookahead_dist=float(lookahead_dist),
            attr_look=bool(attr_look),
        )
        f_rep, f_tan, _d_obs = _repulsive_and_tangential_force(
            cur_pos, state.theta,
            dist_field, grid_map,
            k_rep=coef["k_rep"],
            k_dist=coef["k_dist"],
            angle_detection=float(angle_detection),
            tangential=bool(cfg["tangential"]),
            linear_repulsion=bool(linear_repulsion),
            footprint_radius=float(footprint_radius),
        )
        if cfg["inertia"]:
            f_iner = _inertial_force(
                history_velocity,
                k_inertia=coef["k_inertia"],
                t_inertia=float(t_inertia),
                dt=float(dt),
                pos=cur_pos,
                goal=goal_world,
                lookahead_dist=float(lookahead_dist),
            )
        else:
            f_iner = np.zeros(2, dtype=float)

        # 虚拟障碍贡献（dynamic 变体专用）：
        # 论文/原仓库做法是把 vobs 加入 obstacles 列表参与 F_rep 计算；
        # local 版改为对每个 vobs 直接施加点状排斥（同 Eq.4 修正版）
        for vob in virtual_obs:
            r = cur_pos - vob
            d = float(np.linalg.norm(r))
            if 0.0 < d < coef["k_dist"]:
                eff_d = max(d - float(footprint_radius), 1e-6)
                mag = (
                    coef["k_rep"]
                    * ((1.0 / eff_d) - (1.0 / max(coef["k_dist"], 1e-6)))
                    * ((1.0 / eff_d) ** 2)
                    * (eff_d / d)
                )
                direction = r / d
                f_rep = f_rep + mag * direction

        f_total = f_attr + f_rep + f_tan + f_iner

        # ---- 诊断模式：记录每步 4 力分量 + 动态系数 + 双圆 EDT ----
        if force_trace_records is not None:
            d_center, d_front, d_rear = _two_circle_edt(state.x, state.y, state.theta)
            force_trace_records.append({
                "step": int(step),
                "t_sim": float(t_sim),
                "x_m": float(state.x),
                "y_m": float(state.y),
                "theta_rad": float(state.theta),
                "d_center_m": d_center,
                "d_front_m": d_front,
                "d_rear_m": d_rear,
                "f_attr_x": float(f_attr[0]),
                "f_attr_y": float(f_attr[1]),
                "f_rep_x": float(f_rep[0]),
                "f_rep_y": float(f_rep[1]),
                "f_tan_x": float(f_tan[0]),
                "f_tan_y": float(f_tan[1]),
                "f_iner_x": float(f_iner[0]),
                "f_iner_y": float(f_iner[1]),
                "f_total_x": float(f_total[0]),
                "f_total_y": float(f_total[1]),
                "k_rep_eff": float(coef["k_rep"]),
                "k_attr_eff": float(coef["k_attr"]),
                "k_dist_eff": float(coef["k_dist"]),
                "k_inertia_eff": float(coef["k_inertia"]),
                "n_virtual_obs": int(len(virtual_obs)),
            })

        # ---- 力 → Ackermann 控制 ----
        v_des, steering = _force_to_ackermann_command(
            f_total, state, params, heading_kp=float(heading_kp)
        )

        # ---- 一步 Ackermann 积分 ----
        # simulate_forward 内部子步 dt=0.05；这里 duration=dt，使总步长可控
        new_state = simulate_forward(
            state=state,
            steering=steering,
            velocity=v_des,
            duration=float(dt),
            params=params,
            dt=min(0.05, float(dt)),
        )

        # 更新历史
        history_pose.append((cur_pos.copy(), float(state.theta)))
        # 用实际位移作为速度向量（与原仓库 BabyRobot.velocity 等价）
        actual_velocity = np.array([
            (new_state.x - state.x) / float(dt),
            (new_state.y - state.y) / float(dt),
        ], dtype=float)
        history_velocity.append(actual_velocity)

        # 修剪历史长度（避免无限增长）
        max_hist = max(int(lm_time / dt) + 5, int(t_inertia / dt) + 5)
        if len(history_pose) > max_hist * 4:
            history_pose = history_pose[-max_hist * 2:]
            history_velocity = history_velocity[-max_hist * 2:]

        state = new_state
        trace_states.append(AckermannState(state.x, state.y, state.theta))
        t_sim += float(dt)

    elapsed_total = time.perf_counter() - t_wall_start

    # 输出 cell 坐标轨迹（与其他 baseline 一致）
    pts = [(s.x / cell_size_m, s.y / cell_size_m) for s in trace_states]

    stats: dict[str, Any] = {
        "version": version,
        "end_reason": end_reason,
        "n_collisions": int(n_collisions),
        "n_steps": int(len(trace_states) - 1),
        "t_simulated_s": float(t_sim),
        "k_rep_final": float(coef["k_rep"]),
        "k_attr_final": float(coef["k_attr"]),
        "k_dist_final": float(coef["k_dist"]),
        "k_inertia_final": float(coef["k_inertia"]),
        "n_virtual_obs": int(len(virtual_obs)),
        "footprint_radius_m": float(footprint_radius),
    }
    if force_trace_records is not None:
        stats["force_trace"] = force_trace_records

    if success:
        return PlannerResult(
            path_xy_cells=pts,
            time_s=float(elapsed_total),
            success=True,
            stats=stats,
        )
    return PlannerResult(
        path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))] if not pts else pts,
        time_s=float(elapsed_total),
        success=False,
        stats=stats,
    )
