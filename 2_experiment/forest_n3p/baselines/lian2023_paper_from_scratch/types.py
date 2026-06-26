"""Lian 2023 expert planner 数据结构。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Tuple


class PlanStatus(Enum):
    """规划/执行状态码（设计 §1.3 / §2.5）。"""

    SUCCESS = "success"
    STAGE1_2D_ASTAR_FAIL = "stage1_2d_astar_fail"
    STAGE1_CORRIDOR_DEGENERATE = "stage1_corridor_degenerate"
    STAGE1_EHA_FAIL = "stage1_eha_fail"
    STAGE2_NLP_FAIL = "stage2_nlp_fail"
    RUNTIME_TIMEOUT = "runtime_timeout"
    QUANTIZATION_COLLISION = "quantization_collision"


@dataclass(frozen=True)
class GridSpec:
    """占据栅格数据，data[y, x] != 0 表示障碍。"""

    data: Any
    resolution: float


@dataclass(frozen=True)
class VehicleParams:
    """车辆运动学约束。"""

    wheelbase_m: float
    min_turn_radius_m: float
    v_max_m_s: float
    delta_max_rad: float
    a_max_m_s2: float = 1.0
    omega_max_rad_s: float = 1.0471975511965976


@dataclass(frozen=True)
class VehicleDiscs:
    """多圆覆盖车体模型。"""

    offsets_m: Tuple[float, ...]
    radius_m: float


@dataclass(frozen=True)
class TrajPoint:
    """单步状态 + 控制 + 时间戳（设计 §2.5）。"""

    px: float       # m
    py: float       # m
    theta: float    # rad
    v: float        # m/s
    delta: float    # rad（转向角）
    a: float        # m/s²（控制：加速度）
    omega: float    # rad/s（控制：转向角速率 = δ̇）
    t: float        # s（episode 内累积时间）


@dataclass(frozen=True)
class CorridorSegment:
    """走廊单段（设计 §3.1.2）。"""

    s_xy: Tuple[float, float]
    d_unit: Tuple[float, float]
    left_m: float
    right_m: float
    arc_length_m: float


@dataclass(frozen=True)
class BoundaryPoint:
    """走廊上的 BP（设计 §3.1.3）。"""

    x: float
    y: float
    theta: float    # 切向估计
    arc_s_m: float  # 沿走廊的累积里程


@dataclass(frozen=True)
class PlanResult:
    """plan() 返回值。失败时 trajectory 为空。"""

    status: PlanStatus
    trajectory: List[TrajPoint]
    stats: Dict[str, Any] = field(default_factory=dict)
