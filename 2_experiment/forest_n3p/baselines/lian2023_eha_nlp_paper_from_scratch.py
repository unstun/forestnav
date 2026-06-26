"""Strict Lian 2023 EHA*-NLP baseline entry point.

The benchmark-facing adapter converts project map and vehicle objects into
plain data structures. All planning stages live inside
``lian2023_paper_from_scratch``.
"""
from __future__ import annotations

import math
from typing import Any, Optional, Tuple

import numpy as np

from forest_n3p.baselines.common import PlannerResult, default_start_theta
from forest_n3p.baselines.lian2023_paper_from_scratch.planner import (
    LianPlanner,
    LianPlannerConfig,
)
from forest_n3p.baselines.lian2023_paper_from_scratch.types import (
    GridSpec,
    PlanStatus,
    VehicleDiscs,
    VehicleParams,
)


def _vehicle_params_from_project_params(params: Any) -> VehicleParams:
    wheelbase = float(getattr(params, "wheelbase", 0.6))
    min_turn = float(getattr(params, "min_turn_radius", wheelbase / math.tan(math.radians(27.0))))
    v_max = float(getattr(params, "v_max", 2.0))
    delta_max = math.atan2(wheelbase, max(min_turn, 1e-9))
    return VehicleParams(
        wheelbase_m=wheelbase,
        min_turn_radius_m=min_turn,
        v_max_m_s=v_max,
        delta_max_rad=float(delta_max),
    )


def _vehicle_discs_from_project_footprint(footprint: Any) -> VehicleDiscs:
    if all(hasattr(footprint, name) for name in ("center_shift", "center_offset", "radius")):
        shift = float(getattr(footprint, "center_shift"))
        offset = float(getattr(footprint, "center_offset"))
        return VehicleDiscs(
            offsets_m=(shift + offset, shift - offset),
            radius_m=float(getattr(footprint, "radius")),
        )
    if all(hasattr(footprint, name) for name in ("half_length", "half_width")):
        half_l = float(getattr(footprint, "half_length"))
        half_w = float(getattr(footprint, "half_width"))
        offset = 0.5 * half_l
        return VehicleDiscs(
            offsets_m=(+offset, -offset),
            radius_m=float(math.hypot(offset, half_w)),
        )
    if all(hasattr(footprint, name) for name in ("length", "width")):
        half_l = 0.5 * float(getattr(footprint, "length"))
        half_w = 0.5 * float(getattr(footprint, "width"))
        offset = 0.5 * half_l
        return VehicleDiscs(
            offsets_m=(+offset, -offset),
            radius_m=float(math.hypot(offset, half_w)),
        )
    return VehicleDiscs(offsets_m=(), radius_m=0.0)


def plan_lian2023_eha_nlp_paper_from_scratch(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
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
    n_steps: int = 200,
    dt_s: float = 0.25,
    nlp_max_iter: int = 200,
    nlp_max_cpu_time_s: float = 30.0,
    nlp_tol: float = 1e-3,
    **ignored_local_overrides: Any,
) -> PlannerResult:
    """Run the package-local Lian 2023 EHA*-NLP planner."""
    _ = goal_xy_tol_m, goal_theta_tol_rad, max_nodes, collision_padding, collision_checker
    cell = float(getattr(grid_map, "resolution"))
    grid = GridSpec(data=np.asarray(getattr(grid_map, "data"), dtype=np.uint8), resolution=cell)
    vehicle = _vehicle_params_from_project_params(params)
    discs = _vehicle_discs_from_project_footprint(footprint)

    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    start_state = (
        float(start_xy[0]) * cell,
        float(start_xy[1]) * cell,
        float(start_theta),
        0.0,
        0.0,
    )
    goal_state = (
        float(goal_xy[0]) * cell,
        float(goal_xy[1]) * cell,
        float(goal_theta_rad),
        0.0,
        0.0,
    )

    planner = LianPlanner(
        params=vehicle,
        discs=discs,
        config=LianPlannerConfig(
            skip_nlp=False,
            total_timeout_s=float(timeout_s),
            nlp_max_cpu_time_s=float(nlp_max_cpu_time_s),
            nlp_max_iter=int(nlp_max_iter),
            nlp_tol=float(nlp_tol),
            L_thre_m=5.0,
            nlp_n_steps_max=200,
            nlp_dt_max=0.3,
            mu1=1.0,
            mu2=0.01,
            mu3=0.01,
            nlp_ref_xy_weight=0.0,
            safety_margin_m=0.0,
            footprint_diameter_m=2.0 * float(discs.radius_m),
            disc_offsets_m=tuple(float(o) for o in discs.offsets_m),
            disc_radius_m=float(discs.radius_m),
            delta_max_rad=float(vehicle.delta_max_rad),
            a_max_m_s2=float(vehicle.a_max_m_s2),
            omega_max_rad_s=float(vehicle.omega_max_rad_s),
            use_corridor_goal_theta=False,
        ),
    )
    result = planner.plan(
        grid_map=grid,
        start_state=start_state,
        goal_state=goal_state,
        n_steps=int(n_steps),
        dt=float(dt_s),
    )

    stats = dict(result.stats)
    plan_status = str(getattr(result.status, "value", result.status))
    stats["variant"] = "lian2023_eha_nlp_paper_from_scratch"
    stats["architecture_scope"] = "paper_from_scratch"
    stats["plan_status"] = plan_status
    stats["goal_theta_policy"] = stats.get("goal_theta_policy", "caller_goal_state")
    stats["local_safety_margin_applied"] = False
    stats["safety_margin_m"] = 0.0
    stats["paper_mu1"] = 1.0
    stats["paper_mu2"] = 0.01
    stats["paper_mu3"] = 0.01
    stats["paper_L_thre_m"] = 5.0
    stats["paper_ref_xy_weight"] = 0.0
    stats["disc_offsets_m"] = list(discs.offsets_m)
    stats["disc_radius_m"] = float(discs.radius_m)
    stats["ignored_local_override_keys"] = sorted(str(k) for k in ignored_local_overrides)

    if plan_status != PlanStatus.SUCCESS.value or not result.trajectory:
        elapsed = float(stats.get("t_total_s", 0.0))
        if elapsed <= 0.0:
            elapsed = float(
                stats.get(
                    "t_nlp_s",
                    stats.get(
                        "t_eha_s",
                        stats.get("t_corridor_s", stats.get("t_astar2d_s", 0.0)),
                    ),
                )
            )
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=elapsed,
            success=False,
            stats=stats,
        )

    stats["path_states"] = [
        (p.px, p.py, p.theta, p.v, p.delta) for p in result.trajectory
    ]
    stats["path_controls"] = [(p.omega, p.a) for p in result.trajectory[:-1]]
    stats["dt_s"] = float(dt_s)
    stats["control_source"] = "lian2023_from_scratch_nlp_trajectory"
    stats["control_semantics"] = "(delta_dot_rad_s, a_m_s2)"

    return PlannerResult(
        path_xy_cells=[(p.px / cell, p.py / cell) for p in result.trajectory],
        time_s=float(stats.get("t_total_s", 0.0)),
        success=True,
        stats=stats,
    )
