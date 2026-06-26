from __future__ import annotations

import math
import inspect
from dataclasses import dataclass
from typing import Any, Callable

from forest_n3p.features import Pose, wrap_pi
from forest_n3p.third_party.pathplan import AckermannParams, GridMap, TwoCircleFootprint


@dataclass(frozen=True)
class Dqn10BaselineAvailability:
    available: bool
    reason: str | None = None


@dataclass(frozen=True)
class Dqn10BaselinePlanResult:
    success: bool
    path: tuple[Pose, ...]
    total_time_s: float
    total_expansions: int
    failure_reason: str | None
    stats: dict[str, Any]


DQN10_BASELINE_ALIASES: dict[str, str] = {
    "improved_ha": "dang2022_ugv_adapted",
    "ss_rrt": "yoon2017_ugv_adapted",
    "idb_rrt": "idb_rrt_ugv_adapted",
}

DQN10_BASELINE_METHODS: tuple[str, ...] = (
    "improved_ha_local",
    "improved_ha_paper",
    "dang2022_ugv_adapted",
    "rrt_local",
    "rrt_paper",
    "yoon2017_ugv_adapted",
    "apf_local",
    "lo_ha",
    "lian2023_eha_paper",
    "lian2023_eha_local",
    "lian2023_eha_nlp_paper",
    "lian2023_eha_nlp_paper_margin005",
    "lian2023_eha_nlp_paper_only",
    "lian2023_eha_nlp_paper_from_scratch",
    "lian2023_eha_nlp_edt",
    "lian2023_ugv_adapted",
    "idb_rrt_local",
    "idb_rrt_to",
    "idb_rrt_paper",
    "idb_rrt_ugv_adapted",
)

DEFAULT_DQN10_BASELINE_KWARGS: dict[str, dict[str, Any]] = {
    "improved_ha_local": {
        "max_nodes": 500_000,
        "step_length": 0.3,
        "rs_heuristic_max_dist": 15.0,
        "curvature_step": 0.05,
        "max_curvature_ratio": 2.0,
        "sigma1": 0.4,
        "sigma2": 0.6,
    },
    "improved_ha_paper": {
        "max_nodes": 500_000,
        "step_length": 1.5,
        "sigma1": 1.0,
        "sigma2": 1.0,
        "voronoi_alpha": 5.0,
        "voronoi_d_o_max": 5.0,
    },
    "dang2022_ugv_adapted": {
        "max_nodes": 500_000,
        "step_length": 1.5,
        "curvature_resolution": 0.05,
        "sigma1": 1.0,
        "sigma2": 1.0,
        "voronoi_alpha": 5.0,
        "voronoi_d_o_max": 5.0,
    },
    "rrt_local": {"max_iter": 20_000},
    "rrt_paper": {
        "max_iter": 40_000,
        "steer_step_m": 5.0,
        "neighbor_radius": 5.0,
        "goal_sample_rate": 0.1,
        "gamma": 0.4,
        "samples_per_seg": 24,
    },
    "yoon2017_ugv_adapted": {
        "max_iter": 40_000,
        "steer_step_m": 5.0,
        "neighbor_radius": 5.0,
        "goal_sample_rate": 0.05,
        "samples_per_segment": 24,
    },
    "apf_local": {
        "version": "dit",
        "dt": 0.1,
        "max_steps": 5_000,
        "k_rep": 0.5,
        "k_attr": 1.0,
        "k_dist": 1.5,
        "lookahead_dist": 2.0,
        "heading_kp": 1.5,
    },
    "lo_ha": {
        "max_nodes": 500_000,
        "lo_population": 15,
        "lo_iterations": 20,
    },
    "lian2023_eha_paper": {
        "max_nodes": 500_000,
        "dl1_m": 1.0,
        "dl2_m": 0.1,
        "l_max_m": 8.0,
        "l_thre_m": 2.0,
        "lp_thre_boxes": 2,
        "n_max": 10,
        "step_length": 0.3,
    },
    "lian2023_eha_local": {
        "max_nodes": 500_000,
        "dl1_m": 1.0,
        "dl2_m": 0.1,
        "l_max_m": 8.0,
        "l_thre_m": 4.5,
        "n_max": 10,
        "eha_per_segment_timeout_s": 2.0,
    },
    "lian2023_eha_nlp_paper": {
        "n_steps": 1000,
        "dt_s": 0.05,
        "nlp_max_iter": 500,
        "nlp_max_cpu_time_s": 90.0,
        "nlp_tol": 1e-3,
        "nlp_n_steps_max": 200,
        "nlp_dt_max": 0.3,
        "mu1": 10.0,
        "nlp_ref_xy_weight": 20.0,
        "safety_margin_m": 0.0,
    },
    "lian2023_eha_nlp_paper_margin005": {
        "n_steps": 1000,
        "dt_s": 0.05,
        "nlp_max_iter": 500,
        "nlp_max_cpu_time_s": 90.0,
        "nlp_tol": 1e-3,
        "nlp_n_steps_max": 200,
        "nlp_dt_max": 0.3,
        "mu1": 10.0,
        "nlp_ref_xy_weight": 20.0,
        "safety_margin_m": 0.05,
    },
    "lian2023_eha_nlp_paper_only": {
        "n_steps": 200,
        "dt_s": 0.25,
        "nlp_max_iter": 200,
        "nlp_max_cpu_time_s": 30.0,
        "nlp_tol": 1e-3,
    },
    "lian2023_eha_nlp_paper_from_scratch": {
        "n_steps": 200,
        "dt_s": 0.25,
        "nlp_max_iter": 200,
        "nlp_max_cpu_time_s": 30.0,
        "nlp_tol": 1e-3,
    },
    "lian2023_eha_nlp_edt": {
        "nlp_n": 2500,
        "nlp_dt_s": 0.02,
        "nlp_max_iter": 1200,
        "nlp_max_cpu_time_s": 120.0,
        "nlp_tol": 1e-3,
        "ref_weight": 0.05,
    },
    "lian2023_ugv_adapted": {
        "strict_n_elements": 200,
        "strict_max_iterations": 10,
        "strict_ipopt_max_iterations": 1000,
    },
    "idb_rrt_local": {
        "max_iter": 12_000,
        "primitive_duration_s": 0.8,
        "dt_s": 0.1,
        "start_v_m_s": 0.8,
        "target_v_m_s": 0.9,
        "goal_sample_rate": 0.12,
        "guide_sample_rate": 0.50,
        "guide_noise_m": 0.8,
        "nearest_k": 5,
    },
    "idb_rrt_to": {
        "max_iter": 12_000,
        "primitive_duration_s": 0.8,
        "dt_s": 0.1,
        "start_v_m_s": 0.8,
        "target_v_m_s": 0.9,
        "goal_sample_rate": 0.12,
        "guide_sample_rate": 0.50,
        "guide_noise_m": 0.8,
        "nearest_k": 5,
        "repair_max_iter": 100,
        "repair_w_dev": 0.01,
        "repair_w_smooth": 0.05,
        "repair_w_goal": 0.5,
        "repair_w_clearance": 10_000.0,
        "repair_clearance_target_m": 1.5,
    },
    "idb_rrt_paper": {
        "max_iter": 12_000,
        "primitive_duration_s": 0.8,
        "dt_s": 0.1,
        "start_v_m_s": 0.8,
        "target_v_m_s": 0.9,
        "goal_sample_rate": 0.14,
        "guide_sample_rate": 0.55,
        "guide_noise_m": 0.8,
        "nearest_k": 5,
        "delta_initial_m": 0.75,
        "delta_decay": 0.7,
        "delta_min_m": 0.12,
        "initial_primitive_count": 35,
        "max_primitive_count": 220,
        "primitive_growth": 1.6,
        "max_outer_iterations": 4,
        "db_rrt_iteration_chunk": 3_000,
        "to_max_iter": 60,
        "to_clearance_target_m": 0.35,
        "to_w_goal_xy": 400.0,
        "to_w_goal_theta": 10.0,
        "to_w_deviation": 1.0,
        "to_w_control": 0.005,
        "to_w_smooth": 0.02,
        "to_w_clearance": 30.0,
    },
    "idb_rrt_ugv_adapted": {
        "max_iter": 12_000,
        "primitive_duration_s": 0.8,
        "dt_s": 0.1,
        "start_v_m_s": 0.8,
        "target_v_m_s": 0.9,
        "delta_dot_max_rad_s": math.radians(60.0),
        "a_max_m_s2": 1.5,
        "goal_sample_rate": 0.14,
        "guide_sample_rate": 0.55,
        "guide_noise_m": 0.8,
        "nearest_k": 5,
        "delta_initial_m": 0.75,
        "delta_decay": 0.7,
        "delta_min_m": 0.12,
        "initial_primitive_count": 35,
        "max_primitive_count": 220,
        "primitive_growth": 1.6,
        "max_outer_iterations": 4,
        "db_rrt_iteration_chunk": 3_000,
        "to_max_iter": 60,
        "to_clearance_target_m": 0.35,
        "to_w_goal_xy": 400.0,
        "to_w_goal_theta": 10.0,
        "to_w_deviation": 1.0,
        "to_w_control": 0.005,
        "to_w_smooth": 0.02,
        "to_w_clearance": 30.0,
    },
}


def canonical_dqn10_baseline_method(method: str) -> str:
    return DQN10_BASELINE_ALIASES.get(str(method), str(method))


def is_dqn10_baseline_method(method: str) -> bool:
    canonical = canonical_dqn10_baseline_method(method)
    return canonical in DQN10_BASELINE_METHODS


def check_dqn10_baseline_available(method: str) -> Dqn10BaselineAvailability:
    canonical = canonical_dqn10_baseline_method(method)
    if canonical not in DQN10_BASELINE_METHODS:
        return Dqn10BaselineAvailability(False, f"unknown DQN10 baseline method: {method}")
    try:
        _planner_fn(canonical)
    except Exception as exc:  # noqa: BLE001 - preflight should report import boundaries.
        return Dqn10BaselineAvailability(False, f"{type(exc).__name__}: {exc}")
    return Dqn10BaselineAvailability(True)


def plan_dqn10_baseline(
    method: str,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    *,
    timeout_s: float,
    max_nodes: int,
    seed: int,
    goal_xy_tol_m: float = 0.30,
    goal_theta_tol_rad: float = math.radians(15.0),
) -> Dqn10BaselinePlanResult:
    canonical = canonical_dqn10_baseline_method(method)
    if canonical not in DQN10_BASELINE_METHODS:
        raise ValueError(f"unsupported DQN10 baseline method: {method}")

    params = _default_ackermann_params()
    start_xy = grid_map.world_to_grid(float(start[0]), float(start[1]))
    goal_xy = grid_map.world_to_grid(float(goal[0]), float(goal[1]))
    kwargs: dict[str, Any] = {
        "grid_map": grid_map,
        "footprint": footprint,
        "params": params,
        "start_xy": start_xy,
        "goal_xy": goal_xy,
        "seed": int(seed),
        "goal_theta_rad": float(goal[2]),
        "start_theta_rad": float(start[2]),
        "goal_xy_tol_m": float(goal_xy_tol_m),
        "goal_theta_tol_rad": float(goal_theta_tol_rad),
        "timeout_s": float(timeout_s),
        "collision_checker": None,
    }
    kwargs.update(DEFAULT_DQN10_BASELINE_KWARGS.get(canonical, {}))
    kwargs.setdefault("max_nodes", int(max_nodes))

    planner = _planner_fn(canonical)
    raw_result = planner(**_filter_kwargs(planner, kwargs))
    stats = dict(getattr(raw_result, "stats", {}) or {})
    stats.setdefault("requested_method", str(method))
    stats.setdefault("canonical_method", canonical)
    stats.setdefault("migration_source", "DQN10")
    path = _poses_from_raw_result(raw_result, grid_map=grid_map, start_theta=float(start[2]))
    success = bool(getattr(raw_result, "success", bool(path)))
    failure_reason = None if success else _failure_reason(stats)
    return Dqn10BaselinePlanResult(
        success=success,
        path=path if success else (),
        total_time_s=float(getattr(raw_result, "time_s", stats.get("time", math.nan))),
        total_expansions=_expansions_from_stats(stats),
        failure_reason=failure_reason,
        stats=stats,
    )


def compact_dqn10_stats(stats: dict[str, Any]) -> dict[str, Any]:
    large_keys = {
        "path_states",
        "path_controls",
        "analytic_path_cells",
        "coarse_path",
        "dense_path",
        "trace_poses",
    }
    out: dict[str, Any] = {}
    for key, value in stats.items():
        if key in large_keys:
            if isinstance(value, (list, tuple)):
                out[f"{key}_count"] = len(value)
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            out[key] = value
    return out


def _planner_fn(method: str) -> Callable[..., Any]:
    if method == "improved_ha_local":
        from forest_n3p.baselines.improved_hybrid_astar import plan_hybrid_astar

        return plan_hybrid_astar
    if method == "improved_ha_paper":
        from forest_n3p.baselines.improved_hybrid_astar_paper import plan_hybrid_astar_paper

        return plan_hybrid_astar_paper
    if method == "dang2022_ugv_adapted":
        from forest_n3p.baselines.dang2022_ugv_adapted import plan_dang2022_ugv_adapted

        return plan_dang2022_ugv_adapted
    if method == "rrt_local":
        from forest_n3p.baselines.spline_rrt_star import plan_rrt_star

        return plan_rrt_star
    if method == "rrt_paper":
        from forest_n3p.baselines.spline_rrt_star_paper import plan_rrt_star_paper

        return plan_rrt_star_paper
    if method == "yoon2017_ugv_adapted":
        from forest_n3p.baselines.yoon2017_ugv_adapted import plan_yoon2017_ugv_adapted

        return plan_yoon2017_ugv_adapted
    if method == "apf_local":
        from forest_n3p.baselines.adaptive_apf_local import plan_adaptive_apf

        return plan_adaptive_apf
    if method == "lo_ha":
        from forest_n3p.baselines.pathplan import plan_lo_hybrid_astar

        return plan_lo_hybrid_astar
    if method == "lian2023_eha_paper":
        from forest_n3p.baselines.lian2023.eha_paper import plan_lian2023_eha_paper

        return plan_lian2023_eha_paper
    if method == "lian2023_eha_local":
        from forest_n3p.baselines.lian2023.eha_local import plan_lian2023_eha_local

        return plan_lian2023_eha_local
    if method == "lian2023_eha_nlp_paper":
        from forest_n3p.baselines.lian2023.eha_nlp_paper import plan_lian2023_eha_nlp_paper

        return plan_lian2023_eha_nlp_paper
    if method == "lian2023_eha_nlp_paper_margin005":
        from forest_n3p.baselines.lian2023_eha_nlp_paper_margin005 import (
            plan_lian2023_eha_nlp_paper_margin005,
        )

        return plan_lian2023_eha_nlp_paper_margin005
    if method == "lian2023_eha_nlp_paper_only":
        from forest_n3p.baselines.lian2023_eha_nlp_paper_only import plan_lian2023_eha_nlp_paper_only

        return plan_lian2023_eha_nlp_paper_only
    if method == "lian2023_eha_nlp_paper_from_scratch":
        from forest_n3p.baselines.lian2023_eha_nlp_paper_from_scratch import (
            plan_lian2023_eha_nlp_paper_from_scratch,
        )

        return plan_lian2023_eha_nlp_paper_from_scratch
    if method == "lian2023_eha_nlp_edt":
        from forest_n3p.baselines.lian2023_eha_nlp_edt import plan_lian2023_eha_nlp_edt

        return plan_lian2023_eha_nlp_edt
    if method == "lian2023_ugv_adapted":
        from forest_n3p.baselines.lian2023_ugv_adapted import plan_lian2023_ugv_adapted

        return plan_lian2023_ugv_adapted
    if method == "idb_rrt_local":
        from forest_n3p.baselines.idb_rrt_local import plan_idb_rrt_local

        return plan_idb_rrt_local
    if method == "idb_rrt_to":
        from forest_n3p.baselines.idb_rrt_to import plan_idb_rrt_to

        return plan_idb_rrt_to
    if method == "idb_rrt_paper":
        from forest_n3p.baselines.idb_rrt_paper import plan_idb_rrt_paper

        return plan_idb_rrt_paper
    if method == "idb_rrt_ugv_adapted":
        from forest_n3p.baselines.idb_rrt_ugv_adapted import plan_idb_rrt_ugv_adapted

        return plan_idb_rrt_ugv_adapted
    raise ValueError(f"unsupported DQN10 baseline method: {method}")


def _filter_kwargs(fn: Callable[..., Any], kwargs: dict[str, Any]) -> dict[str, Any]:
    signature = inspect.signature(fn)
    params = signature.parameters
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params.values()):
        return dict(kwargs)
    return {key: value for key, value in kwargs.items() if key in params}


def _default_ackermann_params() -> AckermannParams:
    wheelbase_m = 0.6
    delta_max_rad = math.radians(27.0)
    min_turn_radius_m = wheelbase_m / max(1e-9, math.tan(delta_max_rad))
    return AckermannParams(wheelbase=wheelbase_m, min_turn_radius=min_turn_radius_m, v_max=2.0)


def _poses_from_raw_result(raw_result: Any, *, grid_map: GridMap, start_theta: float) -> tuple[Pose, ...]:
    stats = dict(getattr(raw_result, "stats", {}) or {})
    path_states = stats.get("path_states")
    if isinstance(path_states, list) and path_states:
        poses: list[Pose] = []
        for row in path_states:
            if not isinstance(row, (list, tuple)) or len(row) < 3:
                break
            poses.append((float(row[0]), float(row[1]), wrap_pi(float(row[2]))))
        if len(poses) >= 2:
            return tuple(poses)
    return _poses_from_cell_path(getattr(raw_result, "path_xy_cells", ()), grid_map=grid_map, start_theta=start_theta)


def _poses_from_cell_path(
    path_xy_cells: Any,
    *,
    grid_map: GridMap,
    start_theta: float,
) -> tuple[Pose, ...]:
    cells = tuple(path_xy_cells or ())
    if not cells:
        return ()
    points: list[tuple[float, float]] = []
    for raw in cells:
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            return ()
        x = float(grid_map.origin[0]) + float(raw[0]) * float(grid_map.resolution)
        y = float(grid_map.origin[1]) + float(raw[1]) * float(grid_map.resolution)
        points.append((x, y))
    if len(points) == 1:
        return ((points[0][0], points[0][1], wrap_pi(start_theta)),)

    poses: list[Pose] = []
    last_theta = wrap_pi(start_theta)
    for idx, (x, y) in enumerate(points):
        if idx + 1 < len(points):
            nx, ny = points[idx + 1]
            if math.hypot(nx - x, ny - y) > 1e-9:
                last_theta = math.atan2(ny - y, nx - x)
        poses.append((float(x), float(y), wrap_pi(last_theta)))
    return tuple(poses)


def _expansions_from_stats(stats: dict[str, Any]) -> int:
    for key in ("expansions", "expanded_nodes", "nodes", "iterations", "max_iter"):
        value = stats.get(key)
        try:
            if value is not None:
                return int(value)
        except (TypeError, ValueError):
            continue
    return 0


def _failure_reason(stats: dict[str, Any]) -> str:
    for key in ("failure_reason", "termination", "status", "plan_status"):
        value = stats.get(key)
        if value:
            return str(value)
    return "dqn10_baseline_failed"
