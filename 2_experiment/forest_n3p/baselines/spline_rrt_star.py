"""Spline-based RRT* baseline 规划器。

参考论文
--------
Yoon, Lee, Jung & Shim, "Spline-based RRT* Using Piecewise Continuous
Collision-checking Algorithm for Car-like Vehicles," J. Intell. Robot. Syst.
90(3-4), 537-549, 2017. DOI: 10.1007/s10846-017-0693-4

已实现
--------
- 两段拼接三次 Bezier 曲线（biarc）运动基元，保证 G1 连续性。
- Ackermann 最小转弯半径约束。
- 标准 RRT* 框架（nearest / neighbor / extend / rewire）。

碰撞检测说明
--------
原论文的核心贡献（dominant trajectories + transition rectangles 碰撞检测）
针对 polygon 环境设计，不适用于本项目的 occupancy grid + EDT 环境。
本实现使用与 DRL 环境相同的 EDT 双圆碰撞检测器，保证公平对比。
"""

from __future__ import annotations

import math
import time
from typing import Any

from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    OrientedBoxFootprint,
    RRTStarPlanner,
    TwoCircleFootprint,
)

from forest_n3p.baselines.common import PlannerResult, default_start_theta


def plan_rrt_star(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    seed: int = 0,
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float = 0.1,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 5.0,
    max_iter: int = 5_000,
    collision_padding: float | None = None,
    collision_checker=None,
) -> PlannerResult:
    cell_size_m = float(grid_map.resolution)
    st = float(start_theta_rad) if start_theta_rad is not None else default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    start = AckermannState(float(start_xy[0]) * cell_size_m, float(start_xy[1]) * cell_size_m, st)
    goal = AckermannState(float(goal_xy[0]) * cell_size_m, float(goal_xy[1]) * cell_size_m, float(goal_theta_rad))

    base_seed = int(seed)
    max_restarts = 2
    time_fracs = (0.85, 0.10, 0.05)
    iter_fracs = (0.85, 0.10, 0.05)

    start_time = time.perf_counter()
    last_stats: dict[str, Any] = {}
    for attempt in range(1 + int(max_restarts)):
        remaining_time = float(timeout_s) - float(time.perf_counter() - start_time)
        if remaining_time <= 0.0:
            break
        if int(max_iter) <= 0:
            break

        attempt_timeout = min(float(remaining_time), float(timeout_s) * float(time_fracs[int(attempt)]))
        attempt_max_iter = max(1, int(round(float(max_iter) * float(iter_fracs[int(attempt)]))))

        planner = RRTStarPlanner(
            grid_map,
            footprint,
            params,
            rng_seed=base_seed + 1_000_003 * int(attempt),
            goal_xy_tol=float(goal_xy_tol_m),
            goal_theta_tol=float(goal_theta_tol_rad),
            collision_padding=collision_padding,
            collision_checker=collision_checker,
        )

        path, stats = planner.plan(
            start,
            goal,
            timeout=float(attempt_timeout),
            max_iter=int(attempt_max_iter),
            self_check=False,
        )
        last_stats = dict(stats)
        last_stats["attempt"] = int(attempt) + 1
        last_stats["attempt_seed"] = base_seed + 1_000_003 * int(attempt)
        last_stats["attempt_timeout_s"] = float(attempt_timeout)
        last_stats["attempt_max_iter"] = int(attempt_max_iter)

        success = bool(stats.get("success", bool(path)))
        if success and path:
            trace_poses = stats.get("trace_poses")
            if trace_poses and len(trace_poses) >= 2:
                pts = [(float(x) / cell_size_m, float(y) / cell_size_m) for x, y, _th in trace_poses]
            else:
                pts = [(float(s.x) / cell_size_m, float(s.y) / cell_size_m) for s in path]
            return PlannerResult(
                path_xy_cells=pts,
                time_s=float(time.perf_counter() - start_time),
                success=True,
                stats=last_stats,
            )

    return PlannerResult(
        path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
        time_s=float(time.perf_counter() - start_time),
        success=False,
        stats=last_stats,
    )
