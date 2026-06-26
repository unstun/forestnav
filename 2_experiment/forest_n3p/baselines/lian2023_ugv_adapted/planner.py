"""Lian2023-UGV adapted baseline.

该模块只做项目侧适配：把 `forest_n3p` 的地图、起终点和本地 UGV
车辆参数转换为 `lian2023_strict` 可接收的输入。算法主体仍由
`2_experiment/lian2023_strict_repro` 提供。
"""

from __future__ import annotations

import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


_STRICT_SRC = Path(__file__).resolve().parents[3] / "lian2023_strict_repro" / "src"
if _STRICT_SRC.is_dir() and str(_STRICT_SRC) not in sys.path:
    sys.path.insert(0, str(_STRICT_SRC))

from lian2023_strict.config import AlgorithmParams, VehicleParams, load_algorithm_params, load_vehicle_params
from lian2023_strict.planner import PlannerMethod, plan_scene
from lian2023_strict.scenes import PaperScene
from forest_n3p.baselines.common import PlannerResult, default_start_theta


UGV_LENGTH_M = 0.924
UGV_WIDTH_M = 0.740
UGV_WHEELBASE_M = 0.6
UGV_OVERHANG_M = 0.162
UGV_MAX_VELOCITY_M_S = 2.0
UGV_MAX_ACCEL_M_S2 = 1.5
UGV_MAX_STEER_RAD = math.radians(27.0)
UGV_MAX_STEERING_RATE_RAD_S = math.radians(60.0)


def build_ugv_vehicle_params() -> VehicleParams:
    """返回与 `UGVBicycleEnv` 一致的本地 UGV 车辆参数。"""
    return load_vehicle_params(
        length_m=UGV_LENGTH_M,
        front_overhang_m=UGV_OVERHANG_M,
        wheelbase_m=UGV_WHEELBASE_M,
        rear_overhang_m=UGV_OVERHANG_M,
        width_m=UGV_WIDTH_M,
        max_accel_m_s2=UGV_MAX_ACCEL_M_S2,
        max_omega_rad_s=UGV_MAX_STEERING_RATE_RAD_S,
        max_velocity_m_s=UGV_MAX_VELOCITY_M_S,
        max_steer_rad=UGV_MAX_STEER_RAD,
    )


def build_lian2023_algorithm_params(
    *,
    strict_n_elements: int = 200,
    strict_max_iterations: int = 10,
    strict_ipopt_max_iterations: int = 1000,
) -> AlgorithmParams:
    """返回 Lian2023 paper-size 算法参数。"""
    return load_algorithm_params(
        n_elements=int(strict_n_elements),
        max_iterations=int(strict_max_iterations),
        ipopt_max_iterations=int(strict_ipopt_max_iterations),
    )


def _grid_map_to_scene(
    *,
    grid_map: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    start_theta_rad: float,
    goal_theta_rad: float,
) -> PaperScene:
    grid = np.asarray(getattr(grid_map, "data"), dtype=np.uint8).copy()
    if grid.ndim != 2:
        raise ValueError("grid_map.data must be a 2D occupancy grid")
    cell = float(getattr(grid_map, "resolution"))
    if not (cell > 0.0):
        raise ValueError("grid_map.resolution must be > 0")
    origin_x, origin_y = tuple(getattr(grid_map, "origin", (0.0, 0.0)))
    height, width = grid.shape
    bounds = (
        float(origin_x),
        float(origin_x) + float(width - 1) * cell,
        float(origin_y),
        float(origin_y) + float(height - 1) * cell,
    )

    def to_world(cell_xy: tuple[int, int]) -> tuple[float, float]:
        x_cell, y_cell = cell_xy
        if hasattr(grid_map, "grid_to_world"):
            return tuple(float(v) for v in grid_map.grid_to_world(int(x_cell), int(y_cell)))
        return float(origin_x) + float(x_cell) * cell, float(origin_y) + float(y_cell) * cell

    start_x, start_y = to_world(start_xy)
    goal_x, goal_y = to_world(goal_xy)
    return PaperScene(
        name="realmap_lian2023_ugv_adapted",
        bounds_m=bounds,
        cell_size_m=cell,
        grid=grid,
        obstacles=tuple(),
        start=(float(start_x), float(start_y), float(start_theta_rad), 0.0, 0.0),
        goal=(float(goal_x), float(goal_y), float(goal_theta_rad), 0.0, 0.0),
        note="UGV realmap scene adapted for Lian2023 strict planner; obstacles are represented by occupancy grid.",
    )


def _world_path_to_cells(states: np.ndarray, *, grid_map: Any) -> list[tuple[float, float]]:
    if states.size == 0:
        return []
    cell = float(getattr(grid_map, "resolution"))
    origin_x, origin_y = tuple(getattr(grid_map, "origin", (0.0, 0.0)))
    out: list[tuple[float, float]] = []
    for row in np.asarray(states, dtype=float):
        out.append(((float(row[0]) - float(origin_x)) / cell, (float(row[1]) - float(origin_y)) / cell))
    return out


def _controls_to_benchmark_order(controls: np.ndarray) -> list[tuple[float, float]]:
    """Convert strict controls `(a, delta_dot)` to benchmark `(delta_dot, a)`."""
    out: list[tuple[float, float]] = []
    for row in np.asarray(controls, dtype=float):
        out.append((float(row[1]), float(row[0])))
    return out


def plan_lian2023_ugv_adapted(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    timeout_s: float = 1200.0,
    strict_n_elements: int = 200,
    strict_max_iterations: int = 10,
    strict_ipopt_max_iterations: int = 1000,
    **ignored_local_overrides: Any,
) -> PlannerResult:
    """运行 Lian2023 方法的本地 UGV 车辆参数适配版。"""
    _ = footprint, params
    cell = float(getattr(grid_map, "resolution"))
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    scene = _grid_map_to_scene(
        grid_map=grid_map,
        start_xy=start_xy,
        goal_xy=goal_xy,
        start_theta_rad=start_theta,
        goal_theta_rad=float(goal_theta_rad),
    )
    vehicle = build_ugv_vehicle_params()
    algorithm = build_lian2023_algorithm_params(
        strict_n_elements=int(strict_n_elements),
        strict_max_iterations=int(strict_max_iterations),
        strict_ipopt_max_iterations=int(strict_ipopt_max_iterations),
    )
    result = plan_scene(
        scene,
        method=PlannerMethod.OURS_EHA_IPOPT,
        vehicle=vehicle,
        params=algorithm,
        timeout_s=float(timeout_s),
    )
    path_cells = _world_path_to_cells(result.states, grid_map=grid_map)
    if not path_cells and getattr(result, "coarse_path", np.empty((0, 2))).size:
        path_cells = _world_path_to_cells(np.asarray(result.coarse_path, dtype=float), grid_map=grid_map)
    if not path_cells:
        path_cells = [(float(start_xy[0]), float(start_xy[1]))]

    stats = dict(result.stats)
    stats.update(
        {
            "variant": "lian2023_ugv_adapted",
            "architecture_scope": "lian2023_strict_algorithm_with_local_ugv_vehicle",
            "plan_status": str(result.status),
            "vehicle_source": "forest_n3p.env.BicycleModelParams + forest_two_circle_footprint",
            "vehicle_length_m": UGV_LENGTH_M,
            "vehicle_width_m": UGV_WIDTH_M,
            "vehicle_wheelbase_m": UGV_WHEELBASE_M,
            "vehicle_front_overhang_m": UGV_OVERHANG_M,
            "vehicle_rear_overhang_m": UGV_OVERHANG_M,
            "vehicle_max_velocity_m_s": UGV_MAX_VELOCITY_M_S,
            "vehicle_max_accel_m_s2": UGV_MAX_ACCEL_M_S2,
            "vehicle_max_steer_rad": UGV_MAX_STEER_RAD,
            "vehicle_max_omega_rad_s": UGV_MAX_STEERING_RATE_RAD_S,
            "paper_mu1": algorithm.mu1,
            "paper_mu2": algorithm.mu2,
            "paper_mu3": algorithm.mu3,
            "paper_L_thre_m": algorithm.wide_passage_threshold_m,
            "strict_n_elements": float(algorithm.n_elements),
            "strict_max_iterations": float(algorithm.max_iterations),
            "strict_ipopt_max_iterations": float(algorithm.ipopt_max_iterations),
            "ignored_local_override_keys": sorted(str(k) for k in ignored_local_overrides),
        }
    )
    if result.states.size:
        stats["path_states"] = [tuple(float(v) for v in row) for row in np.asarray(result.states, dtype=float)]
    if result.controls.size:
        stats["path_controls"] = _controls_to_benchmark_order(result.controls)
        if "tf_s" in stats and len(result.controls) > 0:
            stats["dt_s"] = float(stats["tf_s"]) / float(len(result.controls))
        stats["control_source"] = "lian2023_ugv_adapted_strict_ocp_trajectory"
        stats["control_semantics"] = "(delta_dot_rad_s, a_m_s2)"
        stats["delta_dot_max_rad_s"] = UGV_MAX_STEERING_RATE_RAD_S
        stats["a_max_m_s2"] = UGV_MAX_ACCEL_M_S2

    return PlannerResult(
        path_xy_cells=path_cells,
        time_s=float(stats.get("total_time_s", stats.get("cpu_time_i_s", 0.0))),
        success=bool(result.success),
        stats=stats,
    )
