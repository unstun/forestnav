"""Spline-based RRT* (Yoon 2017) — paper-faithful occupancy-grid reproduction.

参考论文
--------
Yoon, S., Lee, D., Jung, J., & Shim, D. H. "Spline-based RRT* Using Piecewise
Continuous Collision-checking Algorithm for Car-like Vehicles," J. Intell.
Robot. Syst. 90(3-4), 537-549, 2017. DOI: 10.1007/s10846-017-0693-4

本文件 vs spline_rrt_star.py（local 版）的差异
--------
local 版（third_party/pathplan/rrt/rrt_star.py + baselines/spline_rrt_star.py）
为了在小迭代预算 + grid 环境下出解，叠加了 7 个工程加速组件，与论文 Algorithm
1/2/3/4/5/6 不严格一致。本 paper 版剥离这些加速，并补齐原文 Fig. 7 的
Bezier steering 语义：

    剥离项 (location in third_party/pathplan/rrt/rrt_star.py)
    ----------------------------------------------------------------
    (1) BFS reference-path biased sampling     L200, L227-231, L428-475
    (2) try_direct_connect 起点-终点直连       L186-198
    (3) seed_steps 朝目标贪心扩树              L207-218, L575-600
    (4) RRT-Connect 风格 goal 加速循环         L236-264 (12 步连续 steer)
    (5) Steer ±2 delta 五候选 jitter           L514-523
    (6) Nearest 中的 heading-penalty           L401-410, L137-141
    (7) 三段 restart (85%/10%/5% 时间预算)     baselines/spline_rrt_star.py L62-103

    实现项 (Yoon 2017 Algorithm 1-3)
    ----------------------------------------------------------------
    Algorithm 1 refTraj          —— 修正 V_h x V_r = 0 处的端点
    Algorithm 2 chkCollTrans     —— 三类过渡放置完整车辆矩形
    Algorithm 3 ObstacleFree     —— chkCollTraj(P_f, P_r) + chkCollTrans
    GetBezierCurve                —— 闭式 biarc join x_int + 两段 cubic Bezier
    Dominant trajectories         —— P_f (front outer corner) 与 P_r
                                     (rear inner axle)，论文 Eq. 8

Grid 等价
--------
论文环境是 polygon obstacles + Minkowski distance；本项目是 occupancy grid。
等价映射：

    chkCollTraj(连续曲线)   --> 沿 t in [0,1] 步长 ~半 cell 采样为 grid 像素，
                                 逐点 ``grid_map.is_occupied_index``
    chkCollVeh(车辆矩形)    --> 复用 ``GridFootprintChecker.collides_pose``，
                                 它已对 OrientedBoxFootprint 在 grid 上做整体
                                 占据检查
    swept rectangles        --> realmap_a 是 thick occupancy grid，额外沿中心线
                                 放置整车矩形，作为点障碍 dominant trajectory
                                 语义在栅格地图上的保守补充

公开接口
--------
``plan_rrt_star_paper(...)``，签名与 ``baselines/spline_rrt_star.plan_rrt_star``
基本一致（多余的 BFS/seed/jitter/restart 参数被剥离）。
"""

# ============================================================================
# Imports
# ============================================================================
from __future__ import annotations

import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence, Tuple

import numpy as np

from forest_n3p.baselines.common import PlannerResult, default_start_theta
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


# ============================================================================
# Vehicle geometry helpers
# ----------------------------------------------------------------------------
# 论文 (Eq.1, Eq.3) 的几何参数：
#   a_w : vehicle width
#   a_f : front overhang  (rear axle  -> front bumper)
#   a_r : rear overhang   (rear axle  -> rear  bumper)
#   r_min: minimum turning radius
# 项目里 footprint.length / width 是车体几何中心的矩形尺寸；rear axle 与几何
# 中心的偏移由 wheelbase 决定。我们做最常见的中性假设：rear axle 位于几何
# 中心后方 wheelbase/2，从而：
#   a_f = length/2 + wheelbase/2
#   a_r = length/2 - wheelbase/2
# 在 wheelbase < length 的标准车上，这一假设能保证 a_f + a_r = length。
# ============================================================================


@dataclass(frozen=True)
class _VehicleGeometry:
    a_w: float          # 车宽 (m)
    a_f: float          # front overhang from rear axle (m)
    a_r: float          # rear  overhang from rear axle (m)
    r_min: float        # minimum turning radius (m)
    length: float       # 车长 (= a_f + a_r)，等于 footprint.length
    wheelbase: float

    @property
    def half_width(self) -> float:
        return 0.5 * self.a_w


def _extract_vehicle_geometry(
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
) -> _VehicleGeometry:
    """从项目 footprint + AckermannParams 抽 (a_w, a_f, a_r, r_min)。"""
    if isinstance(footprint, OrientedBoxFootprint):
        length = float(footprint.length)
        width = float(footprint.width)
    elif isinstance(footprint, TwoCircleFootprint):
        # TwoCircleFootprint.length / width 反推等效矩形尺寸
        length = float(footprint.length)
        width = float(footprint.width)
    else:
        raise TypeError(f"Unsupported footprint: {type(footprint)!r}")

    wheelbase = float(params.wheelbase)
    # 中性假设：rear axle 位于几何中心后方 wheelbase/2
    a_f = 0.5 * length + 0.5 * wheelbase
    a_r = 0.5 * length - 0.5 * wheelbase
    if a_r < 0.0:
        # wheelbase > length 的极端情况：把 rear axle 落回几何中心，避免负 overhang
        a_f = 0.5 * length
        a_r = 0.5 * length
    return _VehicleGeometry(
        a_w=width,
        a_f=a_f,
        a_r=a_r,
        r_min=float(params.min_turn_radius),
        length=length,
        wheelbase=wheelbase,
    )


# ============================================================================
# CubicBezierBiarc：两段拼接的三次 Bezier (motion primitive)
# ----------------------------------------------------------------------------
# 论文 §5.3 + Fig.7：S-RRT* 用两段三次 Bezier 串成 motion primitive。控制点
# 关系（Yang & Sukkarieh 2010 / S-RRT* [11]）：
#   - x_int 选在 ||x_near - x_int|| = ||x_new - x_int|| 处（new wiring 用法），
#     或者沿 x_new heading 方向选取（rewiring 用法）。
#   - P_{0,1} = x_near, P_{3,1} = P_{0,2} = x_int, P_{3,2} = x_new。
#   - 内控制点 P_{1,*}, P_{2,*} 沿端点 heading 用 gamma * |chord| 偏移，
#     保证 G1 连续与曲率有界。
# 这里使用闭式 biarc join 解出 x_int，再把两段圆弧转为 cubic Bezier。这样
# x_int 由两端位姿关系决定，避免退化成弦中点近似；同时按本地 Ackermann
# r_min 过滤不可行小半径边。
# ============================================================================


@dataclass(frozen=True)
class _CubicBezier:
    p0: Tuple[float, float]
    p1: Tuple[float, float]
    p2: Tuple[float, float]
    p3: Tuple[float, float]

    def point(self, t: float) -> Tuple[float, float]:
        u = 1.0 - t
        b0 = u * u * u
        b1 = 3.0 * u * u * t
        b2 = 3.0 * u * t * t
        b3 = t * t * t
        x = b0 * self.p0[0] + b1 * self.p1[0] + b2 * self.p2[0] + b3 * self.p3[0]
        y = b0 * self.p0[1] + b1 * self.p1[1] + b2 * self.p2[1] + b3 * self.p3[1]
        return x, y

    def deriv(self, t: float) -> Tuple[float, float]:
        u = 1.0 - t
        dx = (
            3.0 * u * u * (self.p1[0] - self.p0[0])
            + 6.0 * u * t * (self.p2[0] - self.p1[0])
            + 3.0 * t * t * (self.p3[0] - self.p2[0])
        )
        dy = (
            3.0 * u * u * (self.p1[1] - self.p0[1])
            + 6.0 * u * t * (self.p2[1] - self.p1[1])
            + 3.0 * t * t * (self.p3[1] - self.p2[1])
        )
        return dx, dy

    def deriv2(self, t: float) -> Tuple[float, float]:
        u = 1.0 - t
        d2x = (
            6.0 * u * (self.p2[0] - 2.0 * self.p1[0] + self.p0[0])
            + 6.0 * t * (self.p3[0] - 2.0 * self.p2[0] + self.p1[0])
        )
        d2y = (
            6.0 * u * (self.p2[1] - 2.0 * self.p1[1] + self.p0[1])
            + 6.0 * t * (self.p3[1] - 2.0 * self.p2[1] + self.p1[1])
        )
        return d2x, d2y

    def control_polygon_length(self) -> float:
        return (
            math.hypot(self.p1[0] - self.p0[0], self.p1[1] - self.p0[1])
            + math.hypot(self.p2[0] - self.p1[0], self.p2[1] - self.p1[1])
            + math.hypot(self.p3[0] - self.p2[0], self.p3[1] - self.p2[1])
        )


@dataclass(frozen=True)
class _BiarcEdge:
    """两段拼接的三次 Bezier (论文 §5.3 motion primitive)。"""
    seg1: _CubicBezier
    seg2: _CubicBezier


def _build_biarc(
    start: AckermannState,
    end: AckermannState,
    *,
    gamma: float,
    min_turn_radius_m: float = 0.0,
) -> Optional[_BiarcEdge]:
    """构造 S-RRT* 风格的两段拼接 cubic Bezier，G1 连续。

    Parameters
    ----------
    gamma : float
        保留 S-RRT* 参数名；闭式 biarc join 由两端位姿和曲率约束决定。
    """
    _ = gamma
    eps = 1e-9
    p1x, p1y = float(start.x), float(start.y)
    p2x, p2y = float(end.x), float(end.y)
    t1x, t1y = math.cos(float(start.theta)), math.sin(float(start.theta))
    t2x, t2y = math.cos(float(end.theta)), math.sin(float(end.theta))

    vx = p2x - p1x
    vy = p2y - p1y
    v_dot_v = vx * vx + vy * vy
    if v_dot_v <= eps:
        return None

    # Closed-form biarc join. This is the same construction used by S-RRT-style
    # steering: solve the tangent distance d, then place x_int so both arcs meet
    # with a shared tangent.
    tx = t1x + t2x
    ty = t1y + t2y
    v_dot_t = vx * tx + vy * ty
    t1_dot_t2 = t1x * t2x + t1y * t2y
    denom = 2.0 * (1.0 - t1_dot_t2)

    if abs(denom) <= 1e-6:
        v_dot_t2 = vx * t2x + vy * t2y
        if abs(v_dot_t2) <= 1e-6:
            return None
        d = v_dot_v / (4.0 * v_dot_t2)
    else:
        discriminant = v_dot_t * v_dot_t + denom * v_dot_v
        if discriminant < 0.0:
            return None
        d = (-v_dot_t + math.sqrt(discriminant)) / denom

    if not math.isfinite(d):
        return None

    pmx = 0.5 * (p1x + p2x + d * (t1x - t2x))
    pmy = 0.5 * (p1y + p2y + d * (t1y - t2y))

    c1, r1, a1 = _biarc_compute_arc(
        (p1x, p1y), (t1x, t1y), (pmx - p1x, pmy - p1y)
    )
    c2, r2, a2 = _biarc_compute_arc(
        (p2x, p2y), (t2x, t2y), (pmx - p2x, pmy - p2y)
    )

    if d < 0.0:
        two_pi = 2.0 * math.pi
        a1 = (two_pi - abs(a1)) * (1.0 if a1 >= 0.0 else -1.0)
        a2 = (two_pi - abs(a2)) * (1.0 if a2 >= 0.0 else -1.0)

    r_min = max(0.0, float(min_turn_radius_m))
    if r_min > 0.0:
        if (r1 > 0.0 and r1 + eps < r_min) or (r2 > 0.0 and r2 + eps < r_min):
            return None

    seg1 = _arc_to_cubic_bezier((p1x, p1y), (pmx, pmy), c1, r1, a1)
    seg2 = _arc_to_cubic_bezier((pmx, pmy), (p2x, p2y), c2, r2, -a2)
    return _BiarcEdge(seg1=seg1, seg2=seg2)


def _biarc_compute_arc(
    point: Tuple[float, float],
    tangent: Tuple[float, float],
    point_to_mid: Tuple[float, float],
) -> Tuple[Tuple[float, float], float, float]:
    """计算由端点、切向和 join 点定义的圆弧。radius==0 表示直线。"""
    px, py = point
    tx, ty = tangent
    dx, dy = point_to_mid
    eps = 1e-9

    normal_z = dx * ty - dy * tx
    perp_x = ty * normal_z
    perp_y = -tx * normal_z

    denom = 2.0 * (perp_x * dx + perp_y * dy)
    if abs(denom) <= 1e-6:
        center = (px + 0.5 * dx, py + 0.5 * dy)
        return center, 0.0, 0.0

    center_dist = (dx * dx + dy * dy) / denom
    cx = px + perp_x * center_dist
    cy = py + perp_y * center_dist

    perp_mag = math.hypot(perp_x, perp_y)
    radius = abs(center_dist * perp_mag)
    if radius <= eps:
        return (cx, cy), 0.0, 0.0

    inv_r = 1.0 / radius
    center_to_start = (px - cx, py - cy)
    center_to_mid = (center_to_start[0] + dx, center_to_start[1] + dy)
    start_dir = (center_to_start[0] * inv_r, center_to_start[1] * inv_r)
    mid_dir = (center_to_mid[0] * inv_r, center_to_mid[1] * inv_r)

    dot = max(-1.0, min(1.0, start_dir[0] * mid_dir[0] + start_dir[1] * mid_dir[1]))
    twist = perp_x * dx + perp_y * dy
    angle = math.acos(dot) * (1.0 if twist >= 0.0 else -1.0)
    return (cx, cy), radius, angle


def _arc_to_cubic_bezier(
    start_xy: Tuple[float, float],
    end_xy: Tuple[float, float],
    center_xy: Tuple[float, float],
    radius: float,
    sweep: float,
) -> _CubicBezier:
    """把圆弧或直线转换为 cubic Bezier。"""
    if radius <= 1e-9 or abs(sweep) <= 1e-9:
        x0, y0 = start_xy
        x3, y3 = end_xy
        p1 = (x0 + (x3 - x0) / 3.0, y0 + (y3 - y0) / 3.0)
        p2 = (x0 + 2.0 * (x3 - x0) / 3.0, y0 + 2.0 * (y3 - y0) / 3.0)
        return _CubicBezier(p0=start_xy, p1=p1, p2=p2, p3=end_xy)

    cx, cy = center_xy
    r0x, r0y = start_xy[0] - cx, start_xy[1] - cy
    r1x, r1y = end_xy[0] - cx, end_xy[1] - cy

    if sweep >= 0.0:
        t0 = (-r0y / radius, r0x / radius)
        t1 = (-r1y / radius, r1x / radius)
    else:
        t0 = (r0y / radius, -r0x / radius)
        t1 = (r1y / radius, -r1x / radius)

    k = (4.0 / 3.0) * math.tan(abs(sweep) / 4.0) * radius
    p1 = (start_xy[0] + t0[0] * k, start_xy[1] + t0[1] * k)
    p2 = (end_xy[0] - t1[0] * k, end_xy[1] - t1[1] * k)
    return _CubicBezier(p0=start_xy, p1=p1, p2=p2, p3=end_xy)


# ============================================================================
# Bezier kinematic quantities (论文 Eq.5 - Eq.8)
# ----------------------------------------------------------------------------
# V_h(t)  : tangential unit vector
# V_r(t)  : normal unit vector (from B(t) toward turning center C(t))
# kappa(t): curvature
# C(t)    : center of curvature
# V_h x V_r 的 z 分量符号 == 转向方向 (>0 左转, <0 右转, 0 直线)
# ============================================================================


def _vh_vr_kappa(
    seg: _CubicBezier, t: float
) -> Tuple[Tuple[float, float], Tuple[float, float], float, float]:
    """Compute (V_h, V_r, kappa, cross_z) at parameter ``t``.

    - V_h = B'/|B'|  (Eq.5a)
    - kappa = |B' x B''| / |B'|^3  (Eq.7)
    - V_r = -(B' x B'' x B') / |...|  (Eq.5b)，方向指向曲率中心
    - cross_z = V_h.x * V_r.y - V_h.y * V_r.x (二维叉积 z 分量；直线段时 0)
    """
    dx, dy = seg.deriv(t)
    speed = math.hypot(dx, dy)
    if speed <= 1e-12:
        return (1.0, 0.0), (0.0, 1.0), 0.0, 0.0

    vh = (dx / speed, dy / speed)
    d2x, d2y = seg.deriv2(t)
    # B' x B'' (二维 -> 标量 z 分量)
    cross_b = dx * d2y - dy * d2x
    kappa = abs(cross_b) / (speed ** 3 + 1e-18)
    if kappa <= 1e-9 or abs(cross_b) <= 1e-12:
        # 直线段：V_r 任意取 V_h 左法线；cross_z = 0
        vr = (-vh[1], vh[0])
        return vh, vr, 0.0, 0.0

    # V_r 方向：(B' x B'') x B' 给出 |B'|^2 * B'' - (B'.B'') * B'，再归一化
    bdotbb = dx * d2x + dy * d2y
    speed2 = speed * speed
    nx = speed2 * d2x - bdotbb * dx
    ny = speed2 * d2y - bdotbb * dy
    nn = math.hypot(nx, ny)
    if nn <= 1e-12:
        vr = (-vh[1], vh[0])
        return vh, vr, kappa, 0.0
    # 论文 Eq.5b 取负号：V_r 指向 turning center（内侧）
    vr = (-nx / nn, -ny / nn)
    cross_z = vh[0] * vr[1] - vh[1] * vr[0]
    return vh, vr, kappa, cross_z


# ============================================================================
# Algorithm 1 — refTraj (论文 §4.3, Algorithm 1)
# ----------------------------------------------------------------------------
# 在 V_h x V_r = 0 (直线段) 与转弯交界处，把动态计算的 P_f / P_r 替换成由
# Eq.9 给出的固定矩形角点偏移：
#   P_{fR}(V_h) = a_w/2 * Rot(-pi/2) V_h + a_f V_h    (右前角)
#   P_{fL}(V_h) = a_w/2 * Rot(+pi/2) V_h + a_f V_h    (左前角)
#   P_{rR}(V_h) = a_w/2 * Rot(-pi/2) V_h              (右后轴)
#   P_{rL}(V_h) = a_w/2 * Rot(+pi/2) V_h              (左后轴)
# 转向方向通过相邻样本的 cross_z 符号确定。
# ============================================================================


def _corner_pfR(vh: Tuple[float, float], geom: _VehicleGeometry) -> Tuple[float, float]:
    # Rot(-pi/2) (vx, vy) = (vy, -vx)
    perp = (vh[1], -vh[0])
    return (
        0.5 * geom.a_w * perp[0] + geom.a_f * vh[0],
        0.5 * geom.a_w * perp[1] + geom.a_f * vh[1],
    )


def _corner_pfL(vh: Tuple[float, float], geom: _VehicleGeometry) -> Tuple[float, float]:
    perp = (-vh[1], vh[0])
    return (
        0.5 * geom.a_w * perp[0] + geom.a_f * vh[0],
        0.5 * geom.a_w * perp[1] + geom.a_f * vh[1],
    )


def _corner_prR(vh: Tuple[float, float], geom: _VehicleGeometry) -> Tuple[float, float]:
    return (0.5 * geom.a_w * vh[1], -0.5 * geom.a_w * vh[0])


def _corner_prL(vh: Tuple[float, float], geom: _VehicleGeometry) -> Tuple[float, float]:
    return (-0.5 * geom.a_w * vh[1], 0.5 * geom.a_w * vh[0])


def _ref_traj(
    seg: _CubicBezier,
    geom: _VehicleGeometry,
    n_samples: int,
) -> Tuple[
    List[Tuple[float, float]],          # P_f(t)
    List[Tuple[float, float]],          # P_r(t)
    List[Tuple[float, float]],          # V_h(t) 缓存（给 chkCollTrans 用）
    List[Tuple[float, float]],          # V_r(t)
    List[float],                        # cross_z(t)
    List[Tuple[float, float]],          # B(t)
]:
    """Algorithm 1: refine endpoints at curvature transitions.

    返回离散化好的 P_f / P_r / V_h / V_r / cross_z / B 数组（与 t 同步）。
    """
    n = max(8, int(n_samples))
    pf: List[Tuple[float, float]] = []
    pr: List[Tuple[float, float]] = []
    vhs: List[Tuple[float, float]] = []
    vrs: List[Tuple[float, float]] = []
    crosses: List[float] = []
    pts: List[Tuple[float, float]] = []

    # 先计算所有点的 (V_h, V_r, kappa, cross_z) 并存动态 dominant trajectory
    samples = []
    for i in range(n + 1):
        t = i / n
        bx, by = seg.point(t)
        vh, vr, kappa, cz = _vh_vr_kappa(seg, t)
        samples.append((t, (bx, by), vh, vr, kappa, cz))

    # 论文 Eq.8：动态 P_f / P_r
    for t, (bx, by), vh, vr, kappa, cz in samples:
        if kappa <= 1e-9:
            # 直线段：dominant trajectory 暂用 B(t)（Algorithm 1 会覆盖到角点）
            pf.append((bx, by))
            pr.append((bx, by))
        else:
            # C(t) = B(t) - (1/kappa) * V_r(t)
            inv_k = 1.0 / kappa
            cx = bx - inv_k * vr[0]
            cy = by - inv_k * vr[1]
            # r_out = sqrt((1/k + 0.5 a_w)^2 + a_f^2)
            r_out = math.hypot(inv_k + 0.5 * geom.a_w, geom.a_f)
            # V_f = (a_f V_h + (1/k + 0.5 a_w) V_r) / |...|
            vfx = geom.a_f * vh[0] + (inv_k + 0.5 * geom.a_w) * vr[0]
            vfy = geom.a_f * vh[1] + (inv_k + 0.5 * geom.a_w) * vr[1]
            vf_mag = math.hypot(vfx, vfy)
            if vf_mag <= 1e-12:
                pf.append((bx, by))
            else:
                vfx /= vf_mag
                vfy /= vf_mag
                pf.append((cx + r_out * vfx, cy + r_out * vfy))
            # r_in = 1/k - 0.5 a_w （内侧；可能为负，按论文 |.| 处理）
            r_in = inv_k - 0.5 * geom.a_w
            pr.append((cx + r_in * vr[0], cy + r_in * vr[1]))

        vhs.append(vh)
        vrs.append(vr)
        crosses.append(cz)
        pts.append((bx, by))

    # Algorithm 1 — 修正 V_h x V_r = 0 处的 P_f / P_r
    # 用 cross_z 是否近 0 判定直线，相邻点 cross_z 的符号给出转向方向；论文里
    # 用 (V_h x V_r) . N，二维直接看 cross_z 符号即可。
    eps_zero = 1e-6
    for i, (t, b, vh, vr, kappa, cz) in enumerate(samples):
        if abs(cz) > eps_zero:
            continue  # 当前点不是直线 -> 跳过
        # case A: 直 -> 转 (前向相邻点是转弯)
        if i + 1 <= n:
            cz_next = samples[i + 1][5]
            if abs(cz_next) > eps_zero:
                if cz_next > 0.0:
                    # straight -> left turn (cross_z > 0)
                    pf[i] = (b[0] + _corner_pfR(vh, geom)[0], b[1] + _corner_pfR(vh, geom)[1])
                    pr[i] = (b[0] + _corner_prL(vh, geom)[0], b[1] + _corner_prL(vh, geom)[1])
                else:
                    # straight -> right turn
                    pf[i] = (b[0] + _corner_pfL(vh, geom)[0], b[1] + _corner_pfL(vh, geom)[1])
                    pr[i] = (b[0] + _corner_prR(vh, geom)[0], b[1] + _corner_prR(vh, geom)[1])
                continue
        # case B: 转 -> 直 (后向相邻点是转弯)
        if i - 1 >= 0:
            cz_prev = samples[i - 1][5]
            if abs(cz_prev) > eps_zero:
                if cz_prev > 0.0:
                    # left turn -> straight
                    pf[i] = (b[0] + _corner_pfR(vh, geom)[0], b[1] + _corner_pfR(vh, geom)[1])
                    pr[i] = (b[0] + _corner_prL(vh, geom)[0], b[1] + _corner_prL(vh, geom)[1])
                else:
                    # right turn -> straight
                    pf[i] = (b[0] + _corner_pfL(vh, geom)[0], b[1] + _corner_pfL(vh, geom)[1])
                    pr[i] = (b[0] + _corner_prR(vh, geom)[0], b[1] + _corner_prR(vh, geom)[1])

    return pf, pr, vhs, vrs, crosses, pts


# ============================================================================
# chkCollTraj：把 dominant trajectory 上的稠密像素逐点查 grid
# ----------------------------------------------------------------------------
# 论文里的 chkCollTraj 接受 (P_f, P_r) 两条折线，与 polygon obstacle 求交。
# 项目 grid 等价：把折线沿 t 离散化为像素，逐点 ``is_occupied_index``。
# 注意：dominant trajectory 已经体现了"车辆所占空间"的最外侧（front outer
# corner）+ 最内侧（rear inner axle），所以对每个像素单点查询即可。
# ============================================================================


def _chk_coll_traj(
    pf: Sequence[Tuple[float, float]],
    pr: Sequence[Tuple[float, float]],
    grid_map: GridMap,
    *,
    coll_step_m: float,
) -> bool:
    """对 P_f / P_r 折线密集采样后逐点查 occupancy grid。返回 True 表示有碰撞。"""

    def _polyline_collides(points: Sequence[Tuple[float, float]]) -> bool:
        if not points:
            return False
        # 沿折线段重新插值到 coll_step_m 以下
        for i in range(len(points) - 1):
            ax, ay = points[i]
            bx, by = points[i + 1]
            seg_len = math.hypot(bx - ax, by - ay)
            n_sub = max(1, int(math.ceil(seg_len / max(coll_step_m, 1e-6))))
            for k in range(n_sub + 1):
                s = k / n_sub
                x = ax + (bx - ax) * s
                y = ay + (by - ay) * s
                gx, gy = grid_map.world_to_grid(x, y)
                if not grid_map.in_bounds(gx, gy):
                    return True
                if grid_map.is_occupied_index(gx, gy):
                    return True
        return False

    if _polyline_collides(pf):
        return True
    if _polyline_collides(pr):
        return True
    return False


# ============================================================================
# Algorithm 2 — chkCollTrans (论文 §4.3, Algorithm 2)
# ----------------------------------------------------------------------------
# 对三类过渡 (i)/(ii)/(iii) 在过渡处放置完整车辆矩形，逐个调用 chkCollVeh。
#   (i)  起/止转弯：t == 0 或 t == 1 时一律放矩形（line 5-10）
#   (ii) 两段拼接：seg1 末端 + seg2 起点 (这里在外层函数 ObstacleFree 处理：
#        我们对每段独立调用 chkCollTrans，而 t=0/t=1 已覆盖段端点)
#   (iii) 段内变向：cross_z 异号点 (V1 . V2 < 0 在二维 = cross_z 符号反转)
# ============================================================================


def _chk_coll_veh(
    grid_map: GridMap,
    rect_checker: GridFootprintChecker,
    pose_xy: Tuple[float, float],
    heading_vec: Tuple[float, float],
) -> bool:
    """放置完整车辆矩形并查 grid 占据。True = 碰撞。"""
    theta = math.atan2(heading_vec[1], heading_vec[0])
    return rect_checker.collides_pose(pose_xy[0], pose_xy[1], theta)


def _chk_coll_trans(
    pts: Sequence[Tuple[float, float]],
    vhs: Sequence[Tuple[float, float]],
    crosses: Sequence[float],
    grid_map: GridMap,
    rect_checker: GridFootprintChecker,
) -> bool:
    """Algorithm 2：在三类过渡处放完整车辆矩形检测碰撞。True=碰。"""
    if not pts:
        return False
    n = len(pts) - 1
    eps_zero = 1e-6

    # case (i)：t = 0 与 t = 1 一律放矩形
    if _chk_coll_veh(grid_map, rect_checker, pts[0], vhs[0]):
        return True
    if _chk_coll_veh(grid_map, rect_checker, pts[n], vhs[n]):
        return True

    # case (iii)：段内 cross_z 符号变化（V1 . V2 < 0），按论文在 t / t-step
    # 两个相邻位置都放矩形
    for i in range(1, n + 1):
        v1 = crosses[i]
        v2 = crosses[i - 1]
        if v1 * v2 < -eps_zero * eps_zero:
            if _chk_coll_veh(grid_map, rect_checker, pts[i], vhs[i]):
                return True
            if _chk_coll_veh(grid_map, rect_checker, pts[i - 1], vhs[i - 1]):
                return True
    return False


def _chk_coll_swept_rects(
    pts: Sequence[Tuple[float, float]],
    vhs: Sequence[Tuple[float, float]],
    grid_map: GridMap,
    rect_checker: GridFootprintChecker,
) -> bool:
    """grid 地图补充检查：沿中心曲线放置整车矩形，防止栅格厚障碍漏检。"""
    if not pts:
        return False
    for pt, vh in zip(pts, vhs):
        if _chk_coll_veh(grid_map, rect_checker, pt, vh):
            return True
    return False


# ============================================================================
# Algorithm 3 — ObstacleFree (论文 §4.3, Algorithm 3)
# ----------------------------------------------------------------------------
#   1. (V_h, V_r) <- getVect(B)   (Eq.5)
#   2. (P_f, P_r) <- refTraj(...) (Algorithm 1)
#   3. chkColl <- chkCollTraj(P_f, P_r)
#   4. if free: chkColl <- chkCollTrans(...)  (Algorithm 2)
#   5. else:    chkColl <- Collision
# ============================================================================


def _obstacle_free(
    edge: _BiarcEdge,
    geom: _VehicleGeometry,
    grid_map: GridMap,
    rect_checker: GridFootprintChecker,
    *,
    samples_per_seg: int,
    coll_step_m: float,
) -> bool:
    """Algorithm 3：返回 True 表示无碰撞。"""
    for seg in (edge.seg1, edge.seg2):
        pf, pr, vhs, vrs, crosses, pts = _ref_traj(seg, geom, n_samples=samples_per_seg)
        # Step 3: chkCollTraj(P_f, P_r)
        if _chk_coll_traj(pf, pr, grid_map, coll_step_m=coll_step_m):
            return False
        # Step 5: chkCollTrans (内部包含起/止矩形与段内变向矩形)
        if _chk_coll_trans(pts, vhs, crosses, grid_map, rect_checker):
            return False
        # Yoon 2017 的 P_f / P_r dominant trajectories 面向点障碍。realmap_a 是
        # thick occupancy grid；这里补充整车矩形逐样本检查，保持 grid 适配下的
        # 保守碰撞语义。
        if _chk_coll_swept_rects(pts, vhs, grid_map, rect_checker):
            return False
    # 段间拼接 (case ii)：在 seg1.t=1 与 seg2.t=0 处放矩形 — 两段都已分别放过
    # 端点矩形，自动覆盖该过渡。
    return True


# ============================================================================
# Edge poses for path reconstruction & length
# ============================================================================


def _edge_poses_and_length(
    edge: _BiarcEdge, *, step_m: float
) -> Tuple[List[Tuple[float, float, float]], float]:
    """沿 biarc 重建 (x, y, theta) 序列并累计弧长。"""
    poses: List[Tuple[float, float, float]] = []
    length = 0.0
    prev_xy: Optional[Tuple[float, float]] = None
    for seg_idx, seg in enumerate((edge.seg1, edge.seg2)):
        approx = max(1e-6, seg.control_polygon_length())
        n = max(2, int(math.ceil(approx / max(step_m, 1e-6))))
        n = min(n, 4000)
        for i in range(n + 1):
            if seg_idx > 0 and i == 0:
                continue
            t = i / n
            x, y = seg.point(t)
            dx, dy = seg.deriv(t)
            theta = math.atan2(dy, dx) if dx * dx + dy * dy > 1e-18 else (
                poses[-1][2] if poses else 0.0
            )
            poses.append((x, y, theta))
            if prev_xy is not None:
                length += math.hypot(x - prev_xy[0], y - prev_xy[1])
            prev_xy = (x, y)
    return poses, length


# ============================================================================
# Tree node
# ============================================================================


@dataclass
class _TreeNode:
    state: AckermannState
    parent: int                # -1 for root
    cost: float
    edge: Optional[_BiarcEdge] = None


# ============================================================================
# RRTStarPaperPlanner — 严格论文 Algorithm 4 / 5 / 6
# ----------------------------------------------------------------------------
# 1. Sample(i)              : uniform free + goal 偏置
# 2. Nearest(G, x)          : 纯欧氏距离 (无 heading penalty)
# 3. Steer(x_nearest, x)    : 单点 steer，单段 cubic Bezier biarc 到目标方向
# 4. Near(G, x_new)         : 半径 r_near 范围内邻居
# 5. ObstacleFree(...)      : Algorithm 3
# 6. New wiring + Rewire    : Algorithm 6
# 主循环 max_iter 或 timeout 截止
# ============================================================================


class _RRTStarPaperPlanner:
    """剥离工程加速、严格按 Yoon 2017 Algorithm 4/5/6 实现的 SS-RRT*。"""

    def __init__(
        self,
        *,
        grid_map: GridMap,
        footprint: OrientedBoxFootprint | TwoCircleFootprint,
        params: AckermannParams,
        rng_seed: int = 0,
        # Algorithm 4 hyperparameters. Yoon 2017 §5.1 uses alpha=5 m and
        # goal-region diameter=4 m; the radius is therefore 2 m.
        steer_step_m: float = 5.0,
        neighbor_radius: float = 5.0,
        goal_xy_tol: float = 2.0,
        goal_theta_tol: float = math.pi,
        goal_sample_rate: float = 0.1,
        # Bezier biarc gamma (S-RRT* topological property)
        gamma: float = 0.4,
        # Algorithm 1/2 sampling density
        samples_per_seg: int = 24,
        # chkCollTraj 像素步长 (默认 = 半 cell)
        coll_step_m: Optional[float] = None,
        collision_padding: Optional[float] = None,
        rect_theta_bins: int = 72,
    ):
        self.map = grid_map
        self.footprint = footprint
        self.params = params
        self.geom = _extract_vehicle_geometry(footprint, params)

        self.rng = np.random.default_rng(int(rng_seed))
        self.steer_step_m = float(steer_step_m)
        self.neighbor_radius = float(neighbor_radius)
        self.goal_xy_tol = float(goal_xy_tol)
        self.goal_theta_tol = float(goal_theta_tol)
        self.goal_sample_rate = float(goal_sample_rate)
        self.gamma = float(gamma)
        self.samples_per_seg = int(samples_per_seg)

        cell = float(grid_map.resolution)
        self.coll_step_m = float(coll_step_m) if coll_step_m is not None else 0.5 * cell

        # 论文 chkCollVeh 用整车矩形 -> 复用 GridFootprintChecker，paper 严格语义
        # 是 OrientedBox；TwoCircleFootprint 时退化为外接矩形（保守）。
        rect_fp: OrientedBoxFootprint
        if isinstance(footprint, OrientedBoxFootprint):
            rect_fp = footprint
        else:
            rect_fp = OrientedBoxFootprint(length=self.geom.length, width=self.geom.a_w)
        self.rect_checker = GridFootprintChecker(
            grid_map, rect_fp, theta_bins=int(rect_theta_bins),
            padding=collision_padding,
        )

    # ----- Algorithm 5 line 1 : Sample(i) -----------------------------------
    def _sample(self, goal: AckermannState) -> AckermannState:
        if self.rng.random() < self.goal_sample_rate:
            return goal
        x, y, theta = self.map.random_free_state(self.rng)
        return AckermannState(x, y, theta)

    # ----- Algorithm 5 line 2 : Nearest -------------------------------------
    @staticmethod
    def _euclid(a: AckermannState, b: AckermannState) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)

    def _nearest(self, tree: List[_TreeNode], target: AckermannState) -> int:
        best_idx = 0
        best_d = float("inf")
        for i, node in enumerate(tree):
            d = self._euclid(node.state, target)
            if d < best_d:
                best_d = d
                best_idx = i
        return best_idx

    # ----- Algorithm 5 line 3 : Steer ---------------------------------------
    def _steer(self, x_nearest: AckermannState, x_rand: AckermannState) -> AckermannState:
        """单点 steer：把 x_rand 投影到 ||x_new - x_nearest|| <= alpha 球内。"""
        dx = x_rand.x - x_nearest.x
        dy = x_rand.y - x_nearest.y
        d = math.hypot(dx, dy)
        if d <= 1e-9:
            return x_rand
        if d <= self.steer_step_m:
            new_xy = (x_rand.x, x_rand.y)
            new_theta = x_rand.theta
        else:
            s = self.steer_step_m / d
            nx = x_nearest.x + dx * s
            ny = x_nearest.y + dy * s
            # heading：对齐弦方向
            new_xy = (nx, ny)
            new_theta = math.atan2(dy, dx)
        return AckermannState(new_xy[0], new_xy[1], new_theta)

    # ----- Algorithm 6 : Near (邻居半径) ------------------------------------
    def _near(self, tree: List[_TreeNode], x_new: AckermannState) -> List[int]:
        out: List[int] = []
        r = self.neighbor_radius
        for i, node in enumerate(tree):
            if self._euclid(node.state, x_new) <= r:
                out.append(i)
        return out

    # ----- ObstacleFree: 论文 Algorithm 3 -----------------------------------
    def _obstacle_free(self, edge: _BiarcEdge) -> bool:
        return _obstacle_free(
            edge,
            self.geom,
            self.map,
            self.rect_checker,
            samples_per_seg=self.samples_per_seg,
            coll_step_m=self.coll_step_m,
        )

    # ----- 单点姿态 grid 占据快查 ------------------------------------------
    def _pose_collides(self, x: float, y: float, theta: float) -> bool:
        return self.rect_checker.collides_pose(x, y, theta)

    # ----- 终点判定 ---------------------------------------------------------
    def _goal_reached(self, state: AckermannState, goal: AckermannState) -> bool:
        d = math.hypot(goal.x - state.x, goal.y - state.y)
        return d <= self.goal_xy_tol

    # ----- 主循环：Algorithm 4 + Algorithm 6 -------------------------------
    def plan(
        self,
        start: AckermannState,
        goal: AckermannState,
        *,
        max_iter: int,
        timeout_s: float,
    ) -> Tuple[List[Tuple[float, float, float]], dict]:
        wall_t0 = time.perf_counter()
        if self._pose_collides(start.x, start.y, start.theta):
            return [], {
                "success": False, "failure_reason": "start_in_collision",
                "nodes": 1, "iterations": 0,
                "time_s": time.perf_counter() - wall_t0,
            }
        if self._pose_collides(goal.x, goal.y, goal.theta):
            return [], {
                "success": False, "failure_reason": "goal_in_collision",
                "nodes": 1, "iterations": 0,
                "time_s": time.perf_counter() - wall_t0,
            }

        tree: List[_TreeNode] = [_TreeNode(state=start, parent=-1, cost=0.0, edge=None)]
        children: List[set[int]] = [set()]
        best_goal_idx: Optional[int] = None
        iterations = 0

        for it in range(int(max_iter)):
            if (time.perf_counter() - wall_t0) > float(timeout_s):
                break
            iterations = it + 1

            # 1. Sample
            x_rand = self._sample(goal)

            # 2. Nearest
            nearest_idx = self._nearest(tree, x_rand)
            x_nearest = tree[nearest_idx].state

            # 3. Steer
            x_new = self._steer(x_nearest, x_rand)
            gx, gy = self.map.world_to_grid(x_new.x, x_new.y)
            if not self.map.in_bounds(gx, gy):
                continue

            # 4. Near (邻居)
            x_near_indices = self._near(tree, x_new)
            if nearest_idx not in x_near_indices:
                x_near_indices.append(nearest_idx)

            # 5. New wiring: choose x_min minimizing Cost(x_near) + CurveLength(B)
            best_parent: Optional[int] = None
            best_cost = float("inf")
            best_edge: Optional[_BiarcEdge] = None

            for cand_idx in x_near_indices:
                cand_state = tree[cand_idx].state
                edge = _build_biarc(
                    cand_state,
                    x_new,
                    gamma=self.gamma,
                    min_turn_radius_m=self.params.min_turn_radius,
                )
                if edge is None:
                    continue
                if not self._obstacle_free(edge):
                    continue
                _poses, edge_len = _edge_poses_and_length(edge, step_m=self.coll_step_m * 2.0)
                c = tree[cand_idx].cost + edge_len
                if c < best_cost:
                    best_cost = c
                    best_parent = cand_idx
                    best_edge = edge

            if best_parent is None or best_edge is None:
                continue

            # 6. 加入树
            tree.append(_TreeNode(
                state=x_new, parent=int(best_parent),
                cost=float(best_cost), edge=best_edge,
            ))
            children.append(set())
            new_idx = len(tree) - 1
            children[best_parent].add(new_idx)

            # 7. Rewiring：x_near \ {x_min}
            for near_idx in x_near_indices:
                if near_idx == best_parent or near_idx == new_idx:
                    continue
                edge = _build_biarc(
                    tree[new_idx].state,
                    tree[near_idx].state,
                    gamma=self.gamma,
                    min_turn_radius_m=self.params.min_turn_radius,
                )
                if edge is None:
                    continue
                if not self._obstacle_free(edge):
                    continue
                _poses, edge_len = _edge_poses_and_length(edge, step_m=self.coll_step_m * 2.0)
                proposed = tree[new_idx].cost + edge_len
                if proposed + 1e-9 < tree[near_idx].cost:
                    self._rewire_one(tree, children, near_idx, new_idx, edge, proposed)

            # 8. Goal check (仅当落入 goal region)
            if self._goal_reached(tree[new_idx].state, goal):
                if best_goal_idx is None or tree[new_idx].cost < tree[best_goal_idx].cost:
                    best_goal_idx = new_idx

        elapsed = time.perf_counter() - wall_t0
        if best_goal_idx is None:
            failure_reason = (
                "timeout" if elapsed >= float(timeout_s) else "iteration_budget_exhausted"
            )
            return [], {
                "success": False, "failure_reason": failure_reason,
                "nodes": len(tree), "iterations": iterations, "time_s": elapsed,
            }

        exact_goal_appended = False
        final_goal_idx = best_goal_idx
        goal_edge = _build_biarc(
            tree[best_goal_idx].state,
            goal,
            gamma=self.gamma,
            min_turn_radius_m=self.params.min_turn_radius,
        )
        if goal_edge is not None and self._obstacle_free(goal_edge):
            _poses, edge_len = _edge_poses_and_length(goal_edge, step_m=self.coll_step_m)
            tree.append(_TreeNode(
                state=goal,
                parent=int(best_goal_idx),
                cost=float(tree[best_goal_idx].cost + edge_len),
                edge=goal_edge,
            ))
            children.append(set())
            children[best_goal_idx].add(len(tree) - 1)
            final_goal_idx = len(tree) - 1
            exact_goal_appended = True

        path = self._reconstruct(tree, final_goal_idx)
        return path, {
            "success": True, "failure_reason": None,
            "nodes": len(tree), "iterations": iterations, "time_s": elapsed,
            "path_cost": tree[final_goal_idx].cost,
            "goal_region_idx": int(best_goal_idx),
            "exact_goal_appended": bool(exact_goal_appended),
        }

    def _rewire_one(
        self,
        tree: List[_TreeNode],
        children: List[set[int]],
        near_idx: int,
        new_parent: int,
        new_edge: _BiarcEdge,
        new_cost: float,
    ) -> None:
        old_parent = tree[near_idx].parent
        old_cost = tree[near_idx].cost
        if old_parent >= 0:
            children[old_parent].discard(near_idx)
        tree[near_idx].parent = int(new_parent)
        tree[near_idx].edge = new_edge
        tree[near_idx].cost = float(new_cost)
        children[new_parent].add(near_idx)
        delta = new_cost - old_cost
        if abs(delta) <= 1e-12:
            return
        q = deque(children[near_idx])
        while q:
            idx = q.popleft()
            tree[idx].cost += delta
            for ci in children[idx]:
                q.append(ci)

    def _reconstruct(
        self, tree: List[_TreeNode], goal_idx: int
    ) -> List[Tuple[float, float, float]]:
        chain: List[int] = []
        cur = goal_idx
        while cur >= 0:
            chain.append(cur)
            cur = tree[cur].parent
        chain.reverse()
        if not chain:
            return []
        path: List[Tuple[float, float, float]] = []
        # 第一个节点 (start)
        first = tree[chain[0]].state
        path.append((float(first.x), float(first.y), float(first.theta)))
        for idx in chain[1:]:
            edge = tree[idx].edge
            if edge is None:
                s = tree[idx].state
                path.append((float(s.x), float(s.y), float(s.theta)))
                continue
            poses, _ = _edge_poses_and_length(edge, step_m=self.coll_step_m)
            if poses:
                path.extend(poses[1:])
        return path


# ============================================================================
# 顶层接口：plan_rrt_star_paper
# ----------------------------------------------------------------------------
# 与 baselines/spline_rrt_star.plan_rrt_star 签名兼容（少量 local-only kwargs
# 自然不再需要）。返回 PlannerResult，path_xy_cells 用 grid 坐标。
# ============================================================================


def plan_rrt_star_paper(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: Tuple[int, int],
    goal_xy: Tuple[int, int],
    seed: int = 0,
    goal_theta_rad: float = 0.0,
    start_theta_rad: Optional[float] = None,
    goal_xy_tol_m: float = 0.1,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 5.0,
    max_iter: int = 5_000,
    collision_padding: Optional[float] = None,
    collision_checker: Any = None,  # 兼容签名；paper 版只用 grid + footprint
    steer_step_m: float = 5.0,
    neighbor_radius: float = 5.0,
    goal_sample_rate: float = 0.1,
    gamma: float = 0.4,
    samples_per_seg: int = 24,
) -> PlannerResult:
    """Yoon 2017 SS-RRT* 1:1 复现版。

    Notes
    -----
    - ``collision_checker`` 仅为签名兼容；论文 Algorithm 3 严格使用 dominant
      trajectory + transition rectangle，本实现不接受外部 checker 替换。
    - 三段 restart / direct connect / seed steps / heading penalty / steer
      jitter / RRT-Connect goal 加速 / BFS reference bias **全部不启用**。
    """
    cell = float(grid_map.resolution)
    st = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    start = AckermannState(float(start_xy[0]) * cell, float(start_xy[1]) * cell, st)
    goal = AckermannState(
        float(goal_xy[0]) * cell, float(goal_xy[1]) * cell, float(goal_theta_rad)
    )

    planner = _RRTStarPaperPlanner(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        rng_seed=int(seed),
        goal_xy_tol=float(goal_xy_tol_m),
        goal_theta_tol=float(goal_theta_tol_rad),
        collision_padding=collision_padding,
        steer_step_m=float(steer_step_m),
        neighbor_radius=float(neighbor_radius),
        goal_sample_rate=float(goal_sample_rate),
        gamma=float(gamma),
        samples_per_seg=int(samples_per_seg),
    )

    wall_t0 = time.perf_counter()
    path_poses, stats = planner.plan(
        start, goal, max_iter=int(max_iter), timeout_s=float(timeout_s)
    )
    elapsed = time.perf_counter() - wall_t0

    if not stats.get("success", False) or not path_poses:
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=float(elapsed),
            success=False,
            stats=dict(stats),
        )

    path_xy_cells = [(float(x) / cell, float(y) / cell) for (x, y, _th) in path_poses]
    return PlannerResult(
        path_xy_cells=path_xy_cells,
        time_s=float(elapsed),
        success=True,
        stats=dict(stats),
    )


__all__ = ["plan_rrt_star_paper"]
