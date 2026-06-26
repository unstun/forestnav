"""Lian 2023 EHA* local baseline.

本地版使用本项目 UGV Ackermann 参数、双圆足迹和现有 Hybrid A* 段规划器。
与 ``eha_paper.py`` 的差异在于 boundary point 选取采用本地距离阈值规则，
便于在 realmap/forest 地图中作为工程参考。
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Optional, Tuple

from forest_n3p.baselines.common import PlannerResult, default_start_theta
from forest_n3p.baselines.lian2023.astar_2d import astar_2d_path
from forest_n3p.baselines.lian2023.boundary_points import select_boundary_points
from forest_n3p.baselines.lian2023.corridor import build_corridor
from forest_n3p.baselines.lian2023.eha_star import run_eha_star
from forest_n3p.baselines.lian2023.types import PlanStatus
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)


PathXYTheta = list[tuple[float, float, float]]


@dataclass(frozen=True)
class EhaInitialResult:
    success: bool
    path_states: PathXYTheta
    time_s: float
    stats: dict[str, Any]
    failure_reason: str = ""


def build_lian2023_eha_initial_path(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: Tuple[int, int],
    goal_xy: Tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: Optional[float] = None,
    timeout_s: float = 30.0,
    dl1_m: float = 1.0,
    dl2_m: float = 0.1,
    l_max_m: float = 8.0,
    l_thre_m: float = 4.5,
    n_max: int = 10,
    goal_xy_tol_m: float = 0.2,
    goal_theta_tol_rad: float = 0.15,
    eha_per_segment_timeout_s: float = 2.0,
) -> EhaInitialResult:
    """构造本地 EHA* 初始轨迹，输出世界坐标姿态序列。"""
    t0 = time.perf_counter()
    cell = float(grid_map.resolution)
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    stats: dict[str, Any] = {
        "variant": "lian2023_eha_local",
        "local_l_thre_m": float(l_thre_m),
        "local_n_max": int(n_max),
    }
    padding_cells = max(1, int(math.ceil(0.74 / 2.0 / max(cell, 1e-9))))
    path_2d = astar_2d_path(
        grid_map=grid_map,
        start_cell=(int(start_xy[0]), int(start_xy[1])),
        goal_cell=(int(goal_xy[0]), int(goal_xy[1])),
        padding_cells=padding_cells,
    )
    stats["t_astar2d_s"] = time.perf_counter() - t0
    stats["local_padding_cells"] = int(padding_cells)
    if path_2d is None:
        return _failure(time.perf_counter() - t0, stats, "astar2d_fail")

    t1 = time.perf_counter()
    corridor = build_corridor(
        grid_map=grid_map,
        path_cells=path_2d,
        dl1_m=float(dl1_m),
        dl2_m=float(dl2_m),
        l_max_m=float(l_max_m),
    )
    stats["t_corridor_s"] = time.perf_counter() - t1
    stats["local_corridor_nodes"] = len(corridor)
    if not corridor:
        return _failure(time.perf_counter() - t0, stats, "corridor_empty")

    d_last = corridor[-1].d_unit
    goal_theta_eff = math.atan2(float(d_last[1]), float(d_last[0]))
    bps = select_boundary_points(
        corridor=corridor,
        start_xy_theta=(float(start_xy[0]) * cell, float(start_xy[1]) * cell, start_theta),
        goal_xy_theta=(float(goal_xy[0]) * cell, float(goal_xy[1]) * cell, goal_theta_eff),
        L_thre_m=float(l_thre_m),
        N_max=int(n_max),
    )
    stats["local_boundary_points"] = len(bps)
    stats["local_goal_theta_input_rad"] = float(goal_theta_rad)
    stats["local_goal_theta_eff_rad"] = float(goal_theta_eff)
    if len(bps) < 2:
        return _failure(time.perf_counter() - t0, stats, "boundary_points_empty")

    t2 = time.perf_counter()
    status, path_states = run_eha_star(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        boundary_points=bps,
        per_segment_timeout_s=float(eha_per_segment_timeout_s),
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
    )
    stats["t_eha_s"] = time.perf_counter() - t2
    stats["time"] = time.perf_counter() - t0
    stats["path_states"] = path_states
    if status != PlanStatus.SUCCESS:
        return _failure(float(stats["time"]), stats, status.value)

    return EhaInitialResult(
        success=True,
        path_states=path_states,
        time_s=float(stats["time"]),
        stats=stats,
    )


def plan_lian2023_eha_local(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: Tuple[int, int],
    goal_xy: Tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: Optional[float] = None,
    goal_xy_tol_m: float = 0.5,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 30.0,
    max_nodes: int = 200_000,
    collision_padding: Optional[float] = None,
    collision_checker: Any = None,
    dl1_m: float = 1.0,
    dl2_m: float = 0.1,
    l_max_m: float = 8.0,
    l_thre_m: float = 4.5,
    n_max: int = 10,
    eha_per_segment_timeout_s: float = 2.0,
) -> PlannerResult:
    """运行本地 EHA* baseline，返回 benchmark 通用路径格式。"""
    _ = max_nodes, collision_padding, collision_checker
    cell = float(grid_map.resolution)
    initial = build_lian2023_eha_initial_path(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        start_xy=start_xy,
        goal_xy=goal_xy,
        goal_theta_rad=goal_theta_rad,
        start_theta_rad=start_theta_rad,
        timeout_s=timeout_s,
        dl1_m=dl1_m,
        dl2_m=dl2_m,
        l_max_m=l_max_m,
        l_thre_m=l_thre_m,
        n_max=n_max,
        goal_xy_tol_m=goal_xy_tol_m,
        goal_theta_tol_rad=goal_theta_tol_rad,
        eha_per_segment_timeout_s=eha_per_segment_timeout_s,
    )
    if not initial.success:
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=float(initial.time_s),
            success=False,
            stats=initial.stats,
        )
    return PlannerResult(
        path_xy_cells=[(x / cell, y / cell) for x, y, _ in initial.path_states],
        time_s=float(initial.time_s),
        success=True,
        stats=initial.stats,
    )


def _failure(time_s: float, stats: dict[str, Any], reason: str) -> EhaInitialResult:
    out = dict(stats)
    out["time"] = float(time_s)
    out["failure_reason"] = str(reason)
    return EhaInitialResult(
        success=False,
        path_states=[],
        time_s=float(time_s),
        stats=out,
        failure_reason=str(reason),
    )

