"""Improved Hybrid A* baseline 规划器。

参考论文
--------
Dang, Ahn, Lee & Lee, "Improved Analytic Expansions in Hybrid A-Star
Path Planning for Non-Holonomic Robots," Applied Sciences 12(12), 5999, 2022.
DOI: 10.3390/app12125999

核心改进
--------
- 多曲率 Reeds-Shepp 解析展开：等步长扫描曲率区间 [kappa_min, kappa_max]。
- 代价函数 Eq.3: G = sigma1 * v + sigma2 * m
  v = 碰撞风险（EDT 距离倒数近似 Voronoi 场）
  m = 运动代价 Eq.4: w1*lp + w2*sp + w3*cp
"""

from __future__ import annotations

import math
import time

from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.primitives import default_primitives

from forest_n3p.baselines.common import PlannerResult, default_start_theta


def plan_hybrid_astar(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float = 0.1,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 5.0,
    max_nodes: int = 200_000,
    collision_padding: float | None = None,
    collision_checker=None,
    rs_heuristic_max_dist: float = 15.0,
    xy_resolution: float = 0.0,
    step_length: float = 0.3,
    # -- Dang 2022 多曲率 RS 解析扩展参数 --
    curvature_step: float = 0.05,
    max_curvature_ratio: float = 2.0,
    sigma1: float = 0.4,
    sigma2: float = 0.6,
) -> PlannerResult:
    """运行 Improved Hybrid A*（Dang 2022）。

    注意：不含 Dolgov CG 轨迹平滑——该后处理不在 Dang 2022 原论文中。
    """
    cell_size_m = float(grid_map.resolution)
    st = float(start_theta_rad) if start_theta_rad is not None else default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    start = AckermannState(float(start_xy[0]) * cell_size_m, float(start_xy[1]) * cell_size_m, st)
    goal = AckermannState(float(goal_xy[0]) * cell_size_m, float(goal_xy[1]) * cell_size_m, float(goal_theta_rad))

    effective_xy_res = float(xy_resolution) if float(xy_resolution) > 0 else None
    prims = default_primitives(params, step_length=float(step_length)) if float(step_length) != 0.3 else None

    planner = HybridAStarPlanner(
        grid_map,
        footprint,
        params,
        primitives=prims,
        xy_resolution=effective_xy_res,
        goal_xy_tol=float(goal_xy_tol_m),
        goal_theta_tol=float(goal_theta_tol_rad),
        reeds_shepp_heuristic_max_dist=float(rs_heuristic_max_dist),
        collision_padding=collision_padding,
        collision_checker=collision_checker,
        curvature_step=float(curvature_step),
        max_curvature_ratio=float(max_curvature_ratio),
        sigma1=float(sigma1),
        sigma2=float(sigma2),
    )

    t0 = time.perf_counter()
    path, stats = planner.plan(start, goal, timeout=float(timeout_s), max_nodes=int(max_nodes), self_check=False)
    dt = float(stats.get("time", time.perf_counter() - t0))

    if path:
        trace_poses = stats.get("trace_poses")
        if trace_poses and len(trace_poses) >= 2:
            pts = [(float(x) / cell_size_m, float(y) / cell_size_m) for x, y, _th in trace_poses]
            # path_states: (x_m, y_m, theta_rad) — 直接暴露带角度的密集轨迹点，
            # 供 eha_star 等下游消费者使用，无需重新估算 theta。
            path_states: list[tuple[float, float, float]] = [
                (float(x), float(y), float(th)) for x, y, th in trace_poses
            ]
        else:
            pts = [(float(s.x) / cell_size_m, float(s.y) / cell_size_m) for s in path]
            path_states = [(float(s.x), float(s.y), float(s.theta)) for s in path]
        stats = dict(stats)           # 避免修改 planner 内部 stats 字典
        stats["path_states"] = path_states
        return PlannerResult(path_xy_cells=pts, time_s=dt, success=True, stats=stats)
    return PlannerResult(
        path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
        time_s=dt,
        success=False,
        stats=dict(stats),     # 失败路径同样浅拷贝，与成功路径对齐
    )
