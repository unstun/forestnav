"""Yoon2017-UGV adapted baseline.

该模块只做项目侧适配：把本地 benchmark 的栅格、起终点和 UGV
车辆参数转换为 `yoon2017_strict` 输入。Yoon2017 SS-RRT* 算法主体由
`2_experiment/yoon2017_strict_repro` 提供。
"""

from __future__ import annotations

import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


_STRICT_SRC = Path(__file__).resolve().parents[3] / "yoon2017_strict_repro" / "src"
if _STRICT_SRC.is_dir() and str(_STRICT_SRC) not in sys.path:
    sys.path.insert(0, str(_STRICT_SRC))

from forest_n3p.baselines.common import PlannerResult, default_start_theta
from yoon2017_strict.config import AlgorithmParams, VehicleParams, paper_algorithm_params
from yoon2017_strict.geometry import Pose
from yoon2017_strict.grid import GridMap
from yoon2017_strict.planner import YoonSplineRRTStarPlanner


UGV_LENGTH_M = 0.924
UGV_WIDTH_M = 0.740
UGV_WHEELBASE_M = 0.6
UGV_MAX_VELOCITY_M_S = 2.0
UGV_MAX_STEER_RAD = math.radians(27.0)


def build_ugv_vehicle_params() -> VehicleParams:
    rear_overhang = max(0.0, 0.5 * UGV_LENGTH_M - 0.5 * UGV_WHEELBASE_M)
    front_overhang = UGV_LENGTH_M - rear_overhang
    min_turn_radius = UGV_WHEELBASE_M / max(math.tan(UGV_MAX_STEER_RAD), 1e-9)
    return VehicleParams(
        front_overhang_m=float(front_overhang),
        rear_overhang_m=float(rear_overhang),
        width_m=UGV_WIDTH_M,
        min_turn_radius_m=float(min_turn_radius),
        wheelbase_m=UGV_WHEELBASE_M,
        max_velocity_m_s=UGV_MAX_VELOCITY_M_S,
    )


def build_yoon2017_algorithm_params(
    *,
    max_iter: int = 40_000,
    steer_step_m: float = 5.0,
    neighbor_radius: float = 5.0,
    goal_sample_rate: float = 0.05,
    samples_per_segment: int = 24,
    goal_xy_tolerance_m: float | None = None,
) -> AlgorithmParams:
    overrides: dict[str, float | int] = {
        "max_iterations": int(max_iter),
        "steer_step_m": float(steer_step_m),
        "neighbor_radius_m": float(neighbor_radius),
        "goal_sample_rate": float(goal_sample_rate),
        "samples_per_segment": int(samples_per_segment),
    }
    if goal_xy_tolerance_m is not None:
        overrides["goal_region_radius_m"] = float(goal_xy_tolerance_m)
    return paper_algorithm_params(**overrides)


def _grid_map_to_strict(grid_map: Any) -> GridMap:
    grid = np.asarray(getattr(grid_map, "data"), dtype=np.uint8).copy()
    if grid.ndim != 2:
        raise ValueError("grid_map.data must be a 2D occupancy grid")
    resolution = float(getattr(grid_map, "resolution"))
    origin = tuple(float(v) for v in getattr(grid_map, "origin", (0.0, 0.0)))
    return GridMap(grid, resolution=resolution, origin=(origin[0], origin[1]))


def _cell_to_pose(*, grid_map: Any, cell_xy: tuple[int, int], theta_rad: float) -> Pose:
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
    return [((float(p.x) - origin_x) / resolution, (float(p.y) - origin_y) / resolution) for p in path]


def plan_yoon2017_ugv_adapted(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    seed: int = 0,
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float | None = None,
    goal_theta_tol_rad: float | None = None,
    timeout_s: float = 30.0,
    max_iter: int = 40_000,
    steer_step_m: float = 5.0,
    neighbor_radius: float = 5.0,
    goal_sample_rate: float = 0.05,
    samples_per_segment: int = 24,
    gamma: float | None = None,
    **ignored_local_overrides: Any,
) -> PlannerResult:
    _ = footprint, params, goal_theta_tol_rad
    cell = float(getattr(grid_map, "resolution"))
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    strict_grid = _grid_map_to_strict(grid_map)
    vehicle = build_ugv_vehicle_params()
    algorithm = build_yoon2017_algorithm_params(
        max_iter=int(max_iter),
        steer_step_m=float(steer_step_m),
        neighbor_radius=float(neighbor_radius),
        goal_sample_rate=float(goal_sample_rate),
        samples_per_segment=int(samples_per_segment),
        goal_xy_tolerance_m=goal_xy_tol_m,
    )
    planner = YoonSplineRRTStarPlanner(strict_grid, vehicle, algorithm)
    result = planner.plan(
        _cell_to_pose(grid_map=grid_map, cell_xy=start_xy, theta_rad=start_theta),
        _cell_to_pose(grid_map=grid_map, cell_xy=goal_xy, theta_rad=float(goal_theta_rad)),
        seed=int(seed),
        timeout_s=float(timeout_s),
    )
    path_cells = _world_path_to_cells(result.path, grid_map=grid_map)
    if not path_cells:
        path_cells = [(float(start_xy[0]), float(start_xy[1]))]
    stats = dict(result.stats)
    stats.update(
        {
            "variant": "yoon2017_ugv_adapted",
            "architecture_scope": "yoon2017_strict_algorithm_with_local_ugv_vehicle",
            "vehicle_source": "forest_n3p.env.BicycleModelParams + forest_two_circle_footprint",
            "vehicle_length_m": UGV_LENGTH_M,
            "vehicle_width_m": UGV_WIDTH_M,
            "vehicle_wheelbase_m": UGV_WHEELBASE_M,
            "vehicle_front_overhang_m": vehicle.front_overhang_m,
            "vehicle_rear_overhang_m": vehicle.rear_overhang_m,
            "vehicle_max_velocity_m_s": UGV_MAX_VELOCITY_M_S,
            "vehicle_max_steer_rad": UGV_MAX_STEER_RAD,
            "paper_steer_step_m": float(algorithm.steer_step_m),
            "paper_goal_sample_rate": float(algorithm.goal_sample_rate),
            "implementation_neighbor_radius_m": float(algorithm.neighbor_radius_m),
            "bezier_gamma_source": "computed_from_x_near_x_int_x_new",
            "ignored_legacy_gamma": None if gamma is None else float(gamma),
            "implementation_samples_per_segment": int(algorithm.samples_per_segment),
            "ignored_local_override_keys": sorted(str(k) for k in ignored_local_overrides),
        }
    )
    return PlannerResult(
        path_xy_cells=path_cells,
        time_s=float(stats.get("elapsed_s", 0.0)),
        success=bool(result.success),
        stats=stats,
    )
