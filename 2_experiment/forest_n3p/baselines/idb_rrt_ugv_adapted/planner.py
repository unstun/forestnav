"""iDb-RRT-UGV adapted baseline.

该模块只做项目侧适配：算法主体调用 `idb_rrt_paper.plan_idb_rrt_paper`，
车辆尺寸、运动限幅和最终碰撞复核固定为本地 UGV 模型。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from forest_n3p.baselines.common import (
    PlannerResult,
    default_ackermann_params,
    forest_two_circle_footprint,
)
from forest_n3p.baselines.idb_rrt_paper import (
    _paper_path_collision_free,
    plan_idb_rrt_paper,
)


UGV_LENGTH_M = 0.924
UGV_WIDTH_M = 0.740
UGV_WHEELBASE_M = 0.6
UGV_OVERHANG_M = 0.162
UGV_MAX_VELOCITY_M_S = 2.0
UGV_MAX_ACCEL_M_S2 = 1.5
UGV_MAX_STEER_RAD = math.radians(27.0)
UGV_MAX_DELTA_DOT_RAD_S = math.radians(60.0)


@dataclass(frozen=True)
class UGVVehicleParams:
    length_m: float
    width_m: float
    wheelbase_m: float
    front_overhang_m: float
    rear_overhang_m: float
    max_velocity_m_s: float
    max_accel_m_s2: float
    max_steer_rad: float
    max_delta_dot_rad_s: float


def build_ugv_vehicle_params() -> UGVVehicleParams:
    """返回本地 UGV 几何和运动限幅。"""
    return UGVVehicleParams(
        length_m=UGV_LENGTH_M,
        width_m=UGV_WIDTH_M,
        wheelbase_m=UGV_WHEELBASE_M,
        front_overhang_m=UGV_OVERHANG_M,
        rear_overhang_m=UGV_OVERHANG_M,
        max_velocity_m_s=UGV_MAX_VELOCITY_M_S,
        max_accel_m_s2=UGV_MAX_ACCEL_M_S2,
        max_steer_rad=UGV_MAX_STEER_RAD,
        max_delta_dot_rad_s=UGV_MAX_DELTA_DOT_RAD_S,
    )


def build_ugv_ackermann_params():
    """返回与本地 UGV 匹配的 Ackermann 运动学参数。"""
    vehicle = build_ugv_vehicle_params()
    return default_ackermann_params(
        wheelbase_m=vehicle.wheelbase_m,
        delta_max_rad=vehicle.max_steer_rad,
        v_max_m_s=vehicle.max_velocity_m_s,
    )


def build_ugv_footprint():
    """返回本地 UGV two-circle footprint，并保留 rear-axle 到车体中心偏移。"""
    return forest_two_circle_footprint(wheelbase_m=UGV_WHEELBASE_M)


def _extract_path_xy_theta(stats: dict[str, Any]) -> tuple[list[tuple[float, float]], list[float]]:
    states_raw = stats.get("path_states")
    if not isinstance(states_raw, list) or not states_raw:
        return [], []
    points_m: list[tuple[float, float]] = []
    thetas: list[float] = []
    for row in states_raw:
        if not isinstance(row, (list, tuple)) or len(row) < 3:
            return [], []
        points_m.append((float(row[0]), float(row[1])))
        thetas.append(float(row[2]))
    return points_m, thetas


def _audit_ugv_rectangle_collision(
    *,
    grid_map: Any,
    stats: dict[str, Any],
    interp_step_m: float | None = None,
) -> dict[str, Any]:
    points_m, thetas = _extract_path_xy_theta(stats)
    if not points_m:
        return {
            "ugv_collision_checked": False,
            "ugv_collision_free": False,
            "ugv_collision_model": "shifted_oriented_rectangle_0.924x0.740m",
            "ugv_collision_state_count": 0,
        }
    footprint = build_ugv_footprint()
    collision_free = _paper_path_collision_free(
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=None,
        points_m=points_m,
        thetas=thetas,
        interp_step_m=interp_step_m,
    )
    return {
        "ugv_collision_checked": True,
        "ugv_collision_free": bool(collision_free),
        "ugv_collision_model": "shifted_oriented_rectangle_0.924x0.740m",
        "ugv_collision_state_count": len(points_m),
    }


def _adapt_stats(
    *,
    base: PlannerResult,
    grid_map: Any,
    ignored_local_overrides: dict[str, Any],
) -> dict[str, Any]:
    vehicle = build_ugv_vehicle_params()
    base_stats = dict(base.stats)
    base_variant = str(base_stats.get("variant", "idb_rrt_paper"))
    audit = _audit_ugv_rectangle_collision(grid_map=grid_map, stats=base_stats)
    stats = dict(base_stats)
    stats.update(
        {
            "variant": "idb_rrt_ugv_adapted",
            "base_variant": base_variant,
            "base_success": bool(base.success),
            "base_termination": str(base_stats.get("termination", "")),
            "architecture_scope": "idb_rrt_paper_algorithm_with_local_ugv_vehicle",
            "vehicle_source": "local_ugv_fixed_params",
            "vehicle_length_m": vehicle.length_m,
            "vehicle_width_m": vehicle.width_m,
            "vehicle_wheelbase_m": vehicle.wheelbase_m,
            "vehicle_front_overhang_m": vehicle.front_overhang_m,
            "vehicle_rear_overhang_m": vehicle.rear_overhang_m,
            "vehicle_max_velocity_m_s": vehicle.max_velocity_m_s,
            "vehicle_max_accel_m_s2": vehicle.max_accel_m_s2,
            "vehicle_max_steer_rad": vehicle.max_steer_rad,
            "vehicle_max_omega_rad_s": vehicle.max_delta_dot_rad_s,
            "ignored_local_override_keys": sorted(str(k) for k in ignored_local_overrides),
            **audit,
        }
    )
    stats["success"] = bool(base.success and audit["ugv_collision_checked"] and audit["ugv_collision_free"])
    if bool(base.success) and not bool(audit["ugv_collision_checked"]):
        stats["termination"] = "ugv_collision_check_missing_path_states"
    elif bool(base.success) and not bool(audit["ugv_collision_free"]):
        stats["termination"] = "ugv_collision_check_failed"
    else:
        stats["termination"] = str(base_stats.get("termination", "success" if base.success else "failed"))
    return stats


def plan_idb_rrt_ugv_adapted(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    seed: int = 0,
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float = 0.5,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 60.0,
    max_iter: int = 12_000,
    collision_padding: float | None = None,
    collision_checker=None,
    primitive_duration_s: float = 0.8,
    dt_s: float = 0.1,
    start_v_m_s: float = 0.8,
    target_v_m_s: float = 0.9,
    v_min_m_s: float = 0.05,
    goal_sample_rate: float = 0.14,
    guide_sample_rate: float = 0.55,
    guide_noise_m: float = 0.8,
    nearest_k: int = 5,
    theta_weight_m: float = 0.35,
    speed_weight_m: float = 0.15,
    steer_weight_m: float = 0.25,
    delta_initial_m: float = 0.75,
    delta_decay: float = 0.7,
    delta_min_m: float = 0.12,
    initial_primitive_count: int = 35,
    max_primitive_count: int = 220,
    primitive_growth: float = 1.6,
    max_outer_iterations: int = 4,
    db_rrt_iteration_chunk: int = 3_000,
    to_max_iter: int = 60,
    to_clearance_target_m: float = 0.35,
    to_w_goal_xy: float = 400.0,
    to_w_goal_theta: float = 10.0,
    to_w_deviation: float = 1.0,
    to_w_control: float = 0.005,
    to_w_smooth: float = 0.02,
    to_w_clearance: float = 30.0,
    **ignored_local_overrides: Any,
) -> PlannerResult:
    """运行 iDb-RRT 方法的本地 UGV 参数适配版。

    外部传入的 `footprint`、`params`、`collision_checker` 只用于保持 benchmark
    统一接口；实际规划和最终碰撞复核均使用本地 UGV 固定参数。
    """
    _ = footprint, params, collision_padding, collision_checker
    ugv_params = build_ugv_ackermann_params()
    ugv_footprint = build_ugv_footprint()
    base = plan_idb_rrt_paper(
        grid_map=grid_map,
        footprint=ugv_footprint,
        params=ugv_params,
        start_xy=start_xy,
        goal_xy=goal_xy,
        seed=int(seed),
        goal_theta_rad=float(goal_theta_rad),
        start_theta_rad=start_theta_rad,
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
        timeout_s=float(timeout_s),
        max_iter=int(max_iter),
        collision_padding=None,
        collision_checker=None,
        primitive_duration_s=float(primitive_duration_s),
        dt_s=float(dt_s),
        start_v_m_s=float(start_v_m_s),
        target_v_m_s=float(target_v_m_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=UGV_MAX_DELTA_DOT_RAD_S,
        a_max_m_s2=UGV_MAX_ACCEL_M_S2,
        goal_sample_rate=float(goal_sample_rate),
        guide_sample_rate=float(guide_sample_rate),
        guide_noise_m=float(guide_noise_m),
        nearest_k=int(nearest_k),
        theta_weight_m=float(theta_weight_m),
        speed_weight_m=float(speed_weight_m),
        steer_weight_m=float(steer_weight_m),
        delta_initial_m=float(delta_initial_m),
        delta_decay=float(delta_decay),
        delta_min_m=float(delta_min_m),
        initial_primitive_count=int(initial_primitive_count),
        max_primitive_count=int(max_primitive_count),
        primitive_growth=float(primitive_growth),
        max_outer_iterations=int(max_outer_iterations),
        db_rrt_iteration_chunk=int(db_rrt_iteration_chunk),
        to_max_iter=int(to_max_iter),
        to_clearance_target_m=float(to_clearance_target_m),
        to_w_goal_xy=float(to_w_goal_xy),
        to_w_goal_theta=float(to_w_goal_theta),
        to_w_deviation=float(to_w_deviation),
        to_w_control=float(to_w_control),
        to_w_smooth=float(to_w_smooth),
        to_w_clearance=float(to_w_clearance),
    )
    stats = _adapt_stats(
        base=base,
        grid_map=grid_map,
        ignored_local_overrides=ignored_local_overrides,
    )
    success = bool(stats["success"])
    return PlannerResult(
        path_xy_cells=list(base.path_xy_cells) if success else [],
        time_s=float(base.time_s),
        success=success,
        stats=stats,
    )
