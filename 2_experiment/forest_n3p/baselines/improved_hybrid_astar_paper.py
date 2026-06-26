"""Improved Hybrid A* (Dang 2022) — 1:1 paper reproduction.

参考论文
--------
Dang, Ahn, Lee & Lee, "Improved Analytic Expansions in Hybrid A-Star
Path Planning for Non-Holonomic Robots," Applied Sciences 12(12), 5999, 2022.
DOI: 10.3390/app12125999

vs ``improved_hybrid_astar.py`` (local 版) 的差异
--------
| 项目 | local 版 | paper 版 (本文件) |
|------|---------|-------------------|
| v(x,y) 来源 | EDT 平均距离的倒数近似 | GVD-based Voronoi field (论文 Eq.2) |
| step length | 0.3 m (项目默认) | 1.5 m (论文 §4.2 fine-tuning) |
| sigma1 / sigma2 | 0.4 / 0.6 | 1.0 / 1.0 (论文 Eq.3 默认) |
| 多曲率 RS | 已实现 (curvature_step=0.05) | 同上 (论文 §4.1 一致) |

实现策略
--------
不修改 ``planner.py``——通过 ``_VoronoiHybridAStarPlanner`` 子类化
``HybridAStarPlanner`` 并 override 两个钩子:

  - ``_path_mean_clearance`` (paper 版不再使用)
  - ``_dang2022_cost``       (改用 Voronoi field 的 *平均场值* 作为 v)

这是论文 Eq.2/Eq.3 的字面解读: v 是 path-cost 函数 (定义在每个 cell)，
按照 §3 "the cost of the Voronoi field" 的描述，对候选 RS 路径取
路径上的平均 v 是最直接的复现方式。
"""

from __future__ import annotations

import math
import time
from typing import List, Optional, Tuple

from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.hybrid_a_star.voronoi_field import (
    compute_voronoi_field,
    query_voronoi_field,
)
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive, default_primitives

from forest_n3p.baselines.common import PlannerResult, default_start_theta


# ============================================================
# Voronoi-field 化的 HybridAStarPlanner
# ============================================================

class _VoronoiHybridAStarPlanner(HybridAStarPlanner):
    """子类化以注入 Voronoi field，避免修改 ``planner.py``。

    覆盖 ``_dang2022_cost``: 用 Voronoi field 的路径平均值替代 EDT
    距离倒数。其余 (多曲率 RS、Eq.4 m 计算、search loop) 完全继承父类。
    """

    def __init__(
        self,
        *args,
        voronoi_field=None,
        voronoi_alpha: float = 5.0,
        voronoi_d_o_max: float = 5.0,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # 预计算 Voronoi field (避免每次 _dang2022_cost 重复算)
        if voronoi_field is None:
            self._voronoi_field = compute_voronoi_field(
                self.map, alpha=voronoi_alpha, d_o_max=voronoi_d_o_max
            )
        else:
            self._voronoi_field = voronoi_field
        self._voronoi_alpha = float(voronoi_alpha)
        self._voronoi_d_o_max = float(voronoi_d_o_max)

    # ── 覆写: Eq.3 G = sigma1 * v + sigma2 * m (v 来源于 GVD field) ──
    def _dang2022_cost(
        self,
        states: List[AckermannState],
        actions: List[MotionPrimitive],
    ) -> float:
        # ── v: 路径上 Voronoi field 的算术平均 (Eq.2) ──
        if not states:
            v = 0.0
        else:
            v_total = 0.0
            for s in states:
                v_total += query_voronoi_field(
                    self._voronoi_field, self.map, s.x, s.y
                )
            v = v_total / len(states)

        # ── m: 运动代价 (Eq.4) m = w1*lp + w2*sp + w3*cp ──
        l_p = 0.0
        s_p = 0.0
        c_p = 0
        prev_steer_sign = 0
        for a in actions:
            l_p += abs(a.step)
            s_p += abs(a.steering)
            cur_sign = (
                1 if a.steering > 1e-9 else (-1 if a.steering < -1e-9 else 0)
            )
            if prev_steer_sign != 0 and cur_sign != 0 and cur_sign != prev_steer_sign:
                c_p += 1
            if cur_sign != 0:
                prev_steer_sign = cur_sign
        # 论文 Eq.4 未指定 w1/w2/w3，与 local 版一致取 1.0
        _w1, _w2, _w3 = 1.0, 1.0, 1.0
        m = _w1 * l_p + _w2 * s_p + _w3 * float(c_p)

        return self.sigma1 * v + self.sigma2 * m


# ============================================================
# 顶层入口: plan_hybrid_astar_paper
# ============================================================

def plan_hybrid_astar_paper(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: Tuple[int, int],
    goal_xy: Tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: Optional[float] = None,
    goal_xy_tol_m: float = 0.1,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 5.0,
    max_nodes: int = 200_000,
    collision_padding: Optional[float] = None,
    collision_checker=None,
    rs_heuristic_max_dist: float = 15.0,
    xy_resolution: float = 0.0,
    # ── 论文 §4.2: motion primitive step length 锁定 1.5 m ──
    step_length: float = 1.5,
    # ── 论文 §4.1: 曲率步长 0.05 ──
    curvature_step: float = 0.05,
    max_curvature_ratio: float = 2.0,
    # ── 论文 Eq.3: sigma1 = sigma2 = 1.0 ──
    sigma1: float = 1.0,
    sigma2: float = 1.0,
    # ── 论文 Eq.2: alpha + d_o^max ──
    voronoi_alpha: float = 5.0,
    voronoi_d_o_max: float = 5.0,
) -> PlannerResult:
    """运行 Improved Hybrid A* (Dang 2022) — 1:1 paper reproduction。

    与 ``plan_hybrid_astar`` (local 版) 接口对齐，差异仅在内部:
      1. 使用 GVD-based Voronoi field (论文 Eq.2) 计算碰撞代价 v；
      2. 默认 step_length=1.5 m (论文 §4.2 fine-tuning 报告值)；
      3. 默认 sigma1=sigma2=1.0 (论文 Eq.3 等权)。

    Returns
    -------
    PlannerResult
        与 local 版字段完全相同。``stats`` 额外包含
        ``voronoi_alpha`` / ``voronoi_d_o_max``。
    """
    cell_size_m = float(grid_map.resolution)
    st = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    )
    start = AckermannState(
        float(start_xy[0]) * cell_size_m,
        float(start_xy[1]) * cell_size_m,
        st,
    )
    goal = AckermannState(
        float(goal_xy[0]) * cell_size_m,
        float(goal_xy[1]) * cell_size_m,
        float(goal_theta_rad),
    )

    effective_xy_res = float(xy_resolution) if float(xy_resolution) > 0 else None
    # 论文 §4.2 motion primitive 锁定 1.5 m
    prims = default_primitives(params, step_length=float(step_length))

    planner = _VoronoiHybridAStarPlanner(
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
        voronoi_alpha=float(voronoi_alpha),
        voronoi_d_o_max=float(voronoi_d_o_max),
    )

    t0 = time.perf_counter()
    path, stats = planner.plan(
        start,
        goal,
        timeout=float(timeout_s),
        max_nodes=int(max_nodes),
        self_check=False,
    )
    dt = float(stats.get("time", time.perf_counter() - t0))

    # 让消费方知道这是 paper 版 + 用了哪组 Voronoi 参数
    stats = dict(stats)
    stats.setdefault("variant", "dang2022_paper")
    stats.setdefault("voronoi_alpha", float(voronoi_alpha))
    stats.setdefault("voronoi_d_o_max", float(voronoi_d_o_max))
    stats.setdefault("step_length", float(step_length))

    if path:
        trace_poses = stats.get("trace_poses")
        if trace_poses and len(trace_poses) >= 2:
            pts = [
                (float(x) / cell_size_m, float(y) / cell_size_m)
                for x, y, _th in trace_poses
            ]
        else:
            pts = [(float(s.x) / cell_size_m, float(s.y) / cell_size_m) for s in path]
        return PlannerResult(
            path_xy_cells=pts,
            time_s=dt,
            success=True,
            stats=stats,
        )
    return PlannerResult(
        path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
        time_s=dt,
        success=False,
        stats=stats,
    )
