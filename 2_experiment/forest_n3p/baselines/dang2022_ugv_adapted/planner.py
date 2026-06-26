"""Dang2022-UGV adapted baseline.

该模块只做项目侧适配：把本地 benchmark 的栅格、起终点和 UGV
车辆参数转换为 `dang2022_strict` 输入。Dang2022 算法主体由
`2_experiment/dang2022_strict_repro` 提供。
"""

from __future__ import annotations

import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


_STRICT_SRC = Path(__file__).resolve().parents[3] / "dang2022_strict_repro" / "src"
if _STRICT_SRC.is_dir() and str(_STRICT_SRC) not in sys.path:
    sys.path.insert(0, str(_STRICT_SRC))

from dang2022_strict.config import AlgorithmParams, VehicleParams, paper_algorithm_params, paper_vehicle_params
from dang2022_strict.grid import GridMap
from dang2022_strict.planner import DangHybridAStarPlanner
from dang2022_strict.robot import Pose
from forest_n3p.baselines.common import PlannerResult, default_start_theta


UGV_LENGTH_M = 0.924
UGV_WIDTH_M = 0.740
UGV_WHEELBASE_M = 0.6
UGV_MAX_VELOCITY_M_S = 2.0
UGV_MAX_STEER_RAD = math.radians(27.0)


def build_ugv_vehicle_params() -> VehicleParams:
    half_length = 0.5 * UGV_LENGTH_M
    half_width = 0.5 * UGV_WIDTH_M
    circle_offset = 0.5 * half_length
    circle_radius = math.hypot(circle_offset, half_width)
    return paper_vehicle_params(
        length_m=UGV_LENGTH_M,
        width_m=UGV_WIDTH_M,
        wheelbase_m=UGV_WHEELBASE_M,
        max_steer_rad=UGV_MAX_STEER_RAD,
        max_velocity_m_s=UGV_MAX_VELOCITY_M_S,
        collision_model="two_circle",
        circle_radius_m=circle_radius,
        circle_center_offset_m=circle_offset,
        circle_center_shift_m=0.5 * UGV_WHEELBASE_M,
    )


def build_dang2022_algorithm_params(
    *,
    max_nodes: int = 500_000,
    step_length: float = 1.5,
    curvature_resolution: float = 0.05,
    sigma1: float = 1.0,
    sigma2: float = 1.0,
    voronoi_alpha: float = 5.0,
    voronoi_d_o_max: float = 5.0,
    goal_xy_tolerance_m: float | None = None,
    goal_theta_tolerance_rad: float | None = None,
) -> AlgorithmParams:
    overrides: dict[str, float | int] = {
        "max_nodes": int(max_nodes),
        "motion_primitive_m": float(step_length),
        "curvature_resolution": float(curvature_resolution),
        "sigma1": float(sigma1),
        "sigma2": float(sigma2),
        "voronoi_alpha": float(voronoi_alpha),
        "voronoi_d_o_max": float(voronoi_d_o_max),
    }
    if goal_xy_tolerance_m is not None:
        overrides["goal_xy_tolerance_m"] = float(goal_xy_tolerance_m)
    if goal_theta_tolerance_rad is not None:
        overrides["goal_theta_tolerance_rad"] = float(goal_theta_tolerance_rad)
    return paper_algorithm_params(**overrides)


def _grid_map_to_strict(grid_map: Any) -> GridMap:
    grid = np.asarray(getattr(grid_map, "data"), dtype=np.uint8).copy()
    if grid.ndim != 2:
        raise ValueError("grid_map.data must be a 2D occupancy grid")
    resolution = float(getattr(grid_map, "resolution"))
    origin = tuple(float(v) for v in getattr(grid_map, "origin", (0.0, 0.0)))
    return GridMap(grid, resolution=resolution, origin=(origin[0], origin[1]))


def _cell_to_pose(
    *,
    grid_map: Any,
    cell_xy: tuple[int, int],
    theta_rad: float,
) -> Pose:
    x_cell, y_cell = int(cell_xy[0]), int(cell_xy[1])
    if hasattr(grid_map, "grid_to_world"):
        x_m, y_m = grid_map.grid_to_world(x_cell, y_cell)
    else:
        resolution = float(getattr(grid_map, "resolution"))
        origin_x, origin_y = tuple(getattr(grid_map, "origin", (0.0, 0.0)))
        x_m = float(origin_x) + float(x_cell) * resolution
        y_m = float(origin_y) + float(y_cell) * resolution
    return Pose(float(round(float(x_m), 12)), float(round(float(y_m), 12)), float(theta_rad))


def _world_path_to_cells(path: list[Pose], *, grid_map: Any) -> list[tuple[float, float]]:
    resolution = float(getattr(grid_map, "resolution"))
    origin_x, origin_y = tuple(float(v) for v in getattr(grid_map, "origin", (0.0, 0.0)))
    out: list[tuple[float, float]] = []
    for pose in path:
        out.append(((float(pose.x) - origin_x) / resolution, (float(pose.y) - origin_y) / resolution))
    return out


def plan_dang2022_ugv_adapted(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    timeout_s: float = 30.0,
    max_nodes: int = 500_000,
    step_length: float = 1.5,
    curvature_resolution: float = 0.05,
    sigma1: float = 1.0,
    sigma2: float = 1.0,
    voronoi_alpha: float = 5.0,
    voronoi_d_o_max: float = 5.0,
    goal_xy_tol_m: float | None = None,
    goal_theta_tol_rad: float | None = None,
    **ignored_local_overrides: Any,
) -> PlannerResult:
    _ = footprint, params
    cell = float(getattr(grid_map, "resolution"))
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    strict_grid = _grid_map_to_strict(grid_map)
    vehicle = build_ugv_vehicle_params()
    algorithm = build_dang2022_algorithm_params(
        max_nodes=int(max_nodes),
        step_length=float(step_length),
        curvature_resolution=float(curvature_resolution),
        sigma1=float(sigma1),
        sigma2=float(sigma2),
        voronoi_alpha=float(voronoi_alpha),
        voronoi_d_o_max=float(voronoi_d_o_max),
        goal_xy_tolerance_m=goal_xy_tol_m,
        goal_theta_tolerance_rad=goal_theta_tol_rad,
    )
    planner = DangHybridAStarPlanner(strict_grid, vehicle, algorithm)
    result = planner.plan(
        _cell_to_pose(grid_map=grid_map, cell_xy=start_xy, theta_rad=start_theta),
        _cell_to_pose(grid_map=grid_map, cell_xy=goal_xy, theta_rad=float(goal_theta_rad)),
        timeout_s=float(timeout_s),
    )
    sparse_path_cells = _world_path_to_cells(result.path, grid_map=grid_map)
    dense_path = list(getattr(result, "dense_path", []) or [])
    dense_path_cells = _world_path_to_cells(dense_path, grid_map=grid_map) if dense_path else []
    path_cells = dense_path_cells if dense_path_cells else sparse_path_cells
    if not path_cells:
        path_cells = [(float(start_xy[0]), float(start_xy[1]))]
    analytic_path = list(getattr(result, "analytic_path", []) or [])
    analytic_path_cells = _world_path_to_cells(analytic_path, grid_map=grid_map) if analytic_path else []
    stats = dict(result.stats)
    stats.update(
        {
            "variant": "dang2022_ugv_adapted",
            "architecture_scope": "dang2022_strict_algorithm_with_local_ugv_vehicle",
            "vehicle_source": "forest_n3p.env.BicycleModelParams + encoded_two_circle_footprint",
            "collision_model": vehicle.collision_model,
            "circle_radius_m": vehicle.circle_radius_m,
            "circle_center_offset_m": vehicle.circle_center_offset_m,
            "circle_center_shift_m": vehicle.circle_center_shift_m,
            "vehicle_length_m": UGV_LENGTH_M,
            "vehicle_width_m": UGV_WIDTH_M,
            "vehicle_wheelbase_m": UGV_WHEELBASE_M,
            "vehicle_max_velocity_m_s": UGV_MAX_VELOCITY_M_S,
            "vehicle_max_steer_rad": UGV_MAX_STEER_RAD,
            "paper_step_length": float(algorithm.motion_primitive_m),
            "paper_curvature_resolution": float(algorithm.curvature_resolution),
            "trace_source": "dang2022_strict.dense_path" if dense_path_cells else "dang2022_strict.sparse_path",
            "sparse_path_cell_count": len(sparse_path_cells),
            "dense_path_cell_count": len(dense_path_cells),
            "ignored_local_override_keys": sorted(str(k) for k in ignored_local_overrides),
        }
    )
    if analytic_path_cells:
        stats["analytic_path_cells"] = analytic_path_cells
        stats["analytic_path_cell_count"] = len(analytic_path_cells)
        stats["analytic_path_source"] = "dang2022_strict.reeds_shepp"
    return PlannerResult(
        path_xy_cells=path_cells,
        time_s=float(stats.get("elapsed_s", 0.0)),
        success=bool(result.success),
        stats=stats,
    )
