"""走廊上的 boundary points 选取（Lian 2023 设计 §3.1.3）。"""
from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from forest_n3p.baselines.lian2023.types import BoundaryPoint, CorridorSegment


def select_boundary_points(
    *,
    corridor: Sequence[CorridorSegment],
    start_xy_theta: Tuple[float, float, float],
    goal_xy_theta: Tuple[float, float, float],
    L_thre_m: float = 4.5,
    N_max: int = 10,
) -> List[BoundaryPoint]:
    """沿走廊累积 arc_length，每隔 L_thre 取一个 BP。

    规则：
    - BP[0] 固定为 start
    - 沿走廊累加，每达到 L_thre 取一个 BP（θ = 切向角）
    - 最后一个总是 goal
    - 总数 ≤ N_max（中间 BP 数 ≤ N_max - 2）
    """
    sx, sy, st_th = start_xy_theta
    gx, gy, gt_th = goal_xy_theta
    bps: List[BoundaryPoint] = [BoundaryPoint(x=sx, y=sy, theta=st_th, arc_s_m=0.0)]
    if len(corridor) == 0:
        bps.append(BoundaryPoint(x=gx, y=gy, theta=gt_th, arc_s_m=0.0))
        return bps

    cum = 0.0
    last_bp_s = 0.0
    middle_budget = max(0, N_max - 2)

    for seg in corridor:
        cum += seg.arc_length_m
        if (cum - last_bp_s) >= L_thre_m and len(bps) - 1 < middle_budget:
            theta = math.atan2(seg.d_unit[1], seg.d_unit[0])
            bps.append(BoundaryPoint(
                x=seg.s_xy[0], y=seg.s_xy[1],
                theta=theta, arc_s_m=cum,
            ))
            last_bp_s = cum

    bps.append(BoundaryPoint(x=gx, y=gy, theta=gt_th, arc_s_m=cum))
    return bps
