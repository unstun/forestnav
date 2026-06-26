"""Lian 2023 EHA*-NLP paper-only baseline entry point.

This wrapper keeps the project benchmark adapter thin: map, start, goal and
vehicle dimensions enter as numeric parameters, while local rollout, action
masking, DQN demo conversion and grid-safety margin patches stay outside the
planner.
"""
from __future__ import annotations

import math
from typing import Any, Optional, Tuple

from forest_n3p.baselines.common import (
    PlannerResult,
    default_start_theta,
)
from forest_n3p.baselines.lian2023_paper_only.types import PlanStatus
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)


def plan_lian2023_eha_nlp_paper_only(
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
    n_steps: int = 200,
    dt_s: float = 0.25,
    nlp_max_iter: int = 200,
    nlp_max_cpu_time_s: float = 30.0,
    nlp_tol: float = 1e-3,
    **ignored_local_overrides: Any,
) -> PlannerResult:
    """Run a paper-parameter Lian 2023 EHA*-NLP planner.

    Deliberately fixed to paper-style settings:
    ``mu1=1.0``, ``mu2=mu3=0.01``, no local safety margin, no reference
    trajectory attraction term, no corridor-tangent goal heading override.
    Extra local override keys are accepted for CLI compatibility and recorded
    in stats, but they are not applied.
    """
    _ = goal_xy_tol_m, goal_theta_tol_rad, max_nodes, collision_padding, collision_checker
    from forest_n3p.baselines.lian2023_paper_only.planner import (
        LianPlanner,
        LianPlannerConfig,
        _disc_geometry_from_footprint,
    )

    disc_offsets_m, disc_radius_m = _disc_geometry_from_footprint(footprint)
    cell = float(grid_map.resolution)
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
        params=params,
        footprint=footprint,
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
            footprint_diameter_m=2.0 * float(disc_radius_m),
            disc_offsets_m=tuple(float(o) for o in disc_offsets_m),
            disc_radius_m=float(disc_radius_m),
            use_corridor_goal_theta=False,
        ),
    )
    result = planner.plan(
        grid_map=grid_map,
        start_state=start_state,
        goal_state=goal_state,
        n_steps=int(n_steps),
        dt=float(dt_s),
    )
    stats = dict(result.stats)
    stats["variant"] = "lian2023_eha_nlp_paper_only"
    stats["architecture_scope"] = "paper_only"
    plan_status = str(getattr(result.status, "value", result.status))
    stats["plan_status"] = plan_status
    stats["local_safety_margin_applied"] = False
    stats["safety_margin_m"] = 0.0
    stats["paper_mu1"] = 1.0
    stats["paper_mu2"] = 0.01
    stats["paper_mu3"] = 0.01
    stats["paper_L_thre_m"] = 5.0
    stats["paper_ref_xy_weight"] = 0.0
    stats["ignored_local_override_keys"] = sorted(str(k) for k in ignored_local_overrides)

    if plan_status != PlanStatus.SUCCESS.value or not result.trajectory:
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=float(stats.get("t_total_s", stats.get("t_nlp_s", 0.0))),
            success=False,
            stats=stats,
        )

    stats["path_states"] = [
        (p.px, p.py, p.theta, p.v, p.delta) for p in result.trajectory
    ]
    stats["path_controls"] = [
        (p.omega, p.a) for p in result.trajectory[:-1]
    ]
    stats["dt_s"] = float(dt_s)
    stats["control_source"] = "lian2023_nlp_trajectory"
    stats["control_semantics"] = "(delta_dot_rad_s, a_m_s2)"

    return PlannerResult(
        path_xy_cells=[(p.px / cell, p.py / cell) for p in result.trajectory],
        time_s=float(stats.get("t_total_s", 0.0)),
        success=True,
        stats=stats,
    )
