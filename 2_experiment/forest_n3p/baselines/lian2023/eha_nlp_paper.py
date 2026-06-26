"""Lian 2023 EHA* + corridor-LSE NLP baseline.

该文件保留论文结构的第二阶段：EHA* 初值进入 ``nlp.py`` 中的 corridor
LSE 约束优化。当前 realmap_a 上该版本可能返回 NLP failure；失败状态会
通过 ``PlannerResult.stats`` 记录，benchmark 中作为独立 baseline 观察。
"""
from __future__ import annotations

import math
from typing import Any, Optional, Tuple

from forest_n3p.baselines.common import PlannerResult, default_start_theta
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)


def plan_lian2023_eha_nlp_paper(
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
    n_steps: int = 1000,
    dt_s: float = 0.05,
    nlp_max_iter: int = 500,
    nlp_max_cpu_time_s: float = 90.0,
    nlp_tol: float = 1e-3,
    nlp_n_steps_max: int = 200,
    nlp_dt_max: float = 0.3,
    mu1: float = 10.0,
    nlp_ref_xy_weight: float = 20.0,
    safety_margin_m: float = 0.0,
    disc_offsets_m: Tuple[float, ...] | None = None,
    disc_radius_m: float | None = None,
) -> PlannerResult:
    """运行论文结构 EHA* + corridor-LSE NLP，返回 benchmark 通用路径格式。

    多圆车体（Lian 2023 §3.1 + §3.2.3）：
    - ``disc_offsets_m`` / ``disc_radius_m`` 留 ``None`` 时本函数会从 ``footprint``
      自动推得 paper-faithful 多圆参数（``TwoCircleFootprint`` → 前/后圆 α =
      ``center_shift ± center_offset``，半径 = ``footprint.radius``；
      ``OrientedBoxFootprint`` → 沿体心 ±length/4 两个圆）。
    - 显式传 ``()`` / ``0`` 关闭多圆（退回 §3.2.3 单点 mass-point，便于敏感性
      对照实验）。
    - ``safety_margin_m`` 默认取 0，保持 paper baseline 参数语义；需要离散栅格
      边界余量时应在本地安全性试验中显式传入。
    """
    _ = goal_xy_tol_m, goal_theta_tol_rad, max_nodes, collision_padding, collision_checker
    from forest_n3p.baselines.lian2023.planner import (
        LianPlanner, LianPlannerConfig, _disc_geometry_from_footprint,
    )
    from forest_n3p.baselines.lian2023.types import PlanStatus

    # 自动从 footprint 推 paper-faithful 多圆几何（仅在 caller 未显式传时）。
    if disc_offsets_m is None or disc_radius_m is None:
        auto_off, auto_r = _disc_geometry_from_footprint(footprint)
        if disc_offsets_m is None:
            disc_offsets_m = auto_off
        if disc_radius_m is None:
            disc_radius_m = auto_r

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
            nlp_n_steps_max=int(nlp_n_steps_max),
            nlp_dt_max=float(nlp_dt_max),
            mu1=float(mu1),
            nlp_ref_xy_weight=float(nlp_ref_xy_weight),
            safety_margin_m=float(safety_margin_m),
            disc_offsets_m=tuple(float(o) for o in disc_offsets_m),
            disc_radius_m=float(disc_radius_m),
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
    stats["variant"] = "lian2023_eha_nlp_paper"
    stats["plan_status"] = result.status.value
    if result.status != PlanStatus.SUCCESS or not result.trajectory:
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
