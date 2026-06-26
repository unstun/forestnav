"""Baseline 规划器共享工具。

提供
--------
- PlannerResult             数据类：路径 + 耗时 + 成功标志 + 统计信息。
- default_ackermann_params  默认 Ackermann 运动学参数（轴距 0.6m，delta_max 27deg）。
- grid_map_from_obstacles   将 numpy 障碍物网格转换为规划器使用的 GridMap。
- forest_two_circle_footprint / forest_oriented_box_footprint
                            与 bicycle 环境匹配的车辆碰撞几何。
- point_footprint           最小占位碰撞足迹（用于点模型近似）。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)


@dataclass(frozen=True)
class PlannerResult:
    path_xy_cells: list[tuple[float, float]]
    time_s: float
    success: bool
    stats: dict[str, Any]


def default_ackermann_params(
    *,
    wheelbase_m: float = 0.6,
    delta_max_rad: float = math.radians(27.0),
    v_max_m_s: float = 2.0,
) -> AckermannParams:
    min_turn_radius_m = float(wheelbase_m) / max(1e-9, float(math.tan(float(delta_max_rad))))
    return AckermannParams(
        wheelbase=float(wheelbase_m),
        min_turn_radius=float(min_turn_radius_m),
        v_max=float(v_max_m_s),
    )


def grid_map_from_obstacles(*, grid_y0_bottom: np.ndarray, cell_size_m: float) -> GridMap:
    g = np.asarray(grid_y0_bottom, dtype=np.uint8)
    if g.ndim != 2:
        raise ValueError("grid_y0_bottom must be a (H,W) array")
    if not (float(cell_size_m) > 0.0):
        raise ValueError("cell_size_m must be > 0")
    return GridMap(g, resolution=float(cell_size_m), origin=(0.0, 0.0))


def point_footprint(*, cell_size_m: float) -> OrientedBoxFootprint:
    s = max(1e-3, 0.1 * float(cell_size_m))
    return OrientedBoxFootprint(length=s, width=s)


def forest_oriented_box_footprint() -> OrientedBoxFootprint:
    return OrientedBoxFootprint(length=0.924, width=0.740)


def forest_two_circle_footprint(*, wheelbase_m: float = 0.6) -> TwoCircleFootprint:
    box = forest_oriented_box_footprint()
    return TwoCircleFootprint.from_box(
        length=float(box.length),
        width=float(box.width),
        center_shift=0.5 * float(wheelbase_m),
    )


def default_start_theta(start_xy: tuple[int, int], goal_xy: tuple[int, int], *, cell_size_m: float) -> float:
    dx = float(goal_xy[0] - start_xy[0]) * float(cell_size_m)
    dy = float(goal_xy[1] - start_xy[1]) * float(cell_size_m)
    return float(math.atan2(dy, dx))


# --------------------------------------------------------------------------- #
# 35 离散动作表（转向角速率 × 加速度）                                          #
# --------------------------------------------------------------------------- #

def build_ackermann_action_table_35(
    *, delta_dot_max_rad_s: float, a_max_m_s2: float
) -> np.ndarray:
    """返回 (35, 2) 动作表，列为 [delta_dot(rad/s), a(m/s²)]。

    布局：7 delta_dot × 5 accel，外层 for d_dot, 内层 for a。
    index = d_dot_idx * 5 + a_idx。
    """
    dd = float(delta_dot_max_rad_s)
    aa = float(a_max_m_s2)
    delta_dots = np.array(
        [-dd, -(2.0 / 3.0) * dd, -(1.0 / 3.0) * dd, 0.0,
         (1.0 / 3.0) * dd, (2.0 / 3.0) * dd, dd],
        dtype=np.float32,
    )
    accels = np.array([-aa, -0.5 * aa, 0.0, 0.5 * aa, aa], dtype=np.float32)
    table = np.zeros((delta_dots.size * accels.size, 2), dtype=np.float32)
    k = 0
    for d_dot in delta_dots:
        for a in accels:
            table[k, 0] = float(d_dot)
            table[k, 1] = float(a)
            k += 1
    return table
