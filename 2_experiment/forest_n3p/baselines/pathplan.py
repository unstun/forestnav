"""Baseline 规划器统一入口（向后兼容）。

各 baseline 已拆分到独立文件：
- improved_hybrid_astar.py   Improved Hybrid A* (Dang 2022)
- spline_rrt_star.py         Spline-based RRT* (Yoon 2017)

本文件保留 plan_lo_hybrid_astar() 和向后兼容 re-export，
cli/infer.py 的 import 无需修改。
"""

from __future__ import annotations

import math
import time
from typing import Any

import numpy as np

from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    LOHybridAStarPlanner,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.primitives import default_primitives

# -- 从 common.py re-export 共享工具 --
from forest_n3p.baselines.common import (  # noqa: F401
    PlannerResult,
    default_ackermann_params,
    default_start_theta as _default_start_theta,
    forest_oriented_box_footprint,
    forest_two_circle_footprint,
    grid_map_from_obstacles,
    point_footprint,
)

# -- 从独立文件 re-export 规划器 --
from forest_n3p.baselines.improved_hybrid_astar import plan_hybrid_astar  # noqa: F401
from forest_n3p.baselines.spline_rrt_star import plan_rrt_star  # noqa: F401


def plan_lo_hybrid_astar(
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
    # LOA 优化开关（lo_iterations=0 则跳过 LOA，直接用默认参数）
    lo_population: int = 20,
    lo_iterations: int = 0,
    lo_seed: int | None = None,
    collision_padding: float | None = None,
    collision_checker=None,
) -> PlannerResult:
    """运行 LO-Hybrid A*（论文 Chen et al. 2025，Applied Sciences 15(14) 7734，
    "Improved Hybrid A* Algorithm Based on Lemming Optimization for Path Planning
    of Autonomous Vehicles"）。

    内层：八分距离启发式（Eq.20）+ 航向变化惩罚（Eq.22）。
    外层：LOA 搜索最优 (min_r, step, P_θ)，适应度按 Eq.26 计算。

    参数搜索范围（论文 Section 4.2.1）：
        min_r  ∈ [0.8, 1.2]  （最小转弯半径，m）
        step   ∈ [0.4, 0.6]  （运动基元步长，m）
        P_θ    ∈ [0.005, 0.015]  （航向变化惩罚系数）

    适应度函数（Eq.26）：
        f = ω₁·(L/L_ref) + ω₂·max|κ| + ω₃·Σe^{-d_k/σ}
        ω₁=0.6, ω₂=0.3, ω₃=0.1, σ=0.5

    LOA 默认配置（论文 Table 6）：N=25 (population), T=40 (max_iterations)。
    论文 Table 11 simple-scenario 推荐 N∈[10,20], T∈[20,30]。

    lo_iterations=0 时为快速模式：仅启用内层改进，参数使用默认值。
    """
    from forest_n3p.third_party.pathplan.hybrid_a_star.lemming_optimizer import LemmingOptimizer
    from forest_n3p.third_party.pathplan.hybrid_a_star.obstacle_field import (
        compute_obstacle_distance_field,
        query_distance,
    )
    from forest_n3p.third_party.pathplan.primitives import default_primitives

    # 论文 Eq.26 权重与平滑参数
    _W1, _W2, _W3 = 0.6, 0.3, 0.1
    _SIGMA = 0.5  # 障碍排斥衰减距离（m）

    cell_size_m = float(grid_map.resolution)
    st = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else _default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
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

    # 预先运行标准 HA* 获取参考路径长度 L_ref（Eq.26 归一化用）
    _ref_planner = HybridAStarPlanner(
        grid_map, footprint, params,
        goal_xy_tol=float(goal_xy_tol_m),
        goal_theta_tol=float(goal_theta_tol_rad),
        collision_padding=collision_padding,
        collision_checker=collision_checker,
        curvature_step=0.0,  # 参考路径: 禁用多曲率扫描以加速
    )
    _ref_path, _ref_stats = _ref_planner.plan(start, goal, timeout=2.0, max_nodes=50_000, self_check=False)
    L_ref = float(_ref_stats.get("path_length", 0.0)) if _ref_path else 0.0
    if L_ref <= 0.0:
        L_ref = 1.0  # 防止除零（参考失败则退化为无归一化）

    # 预计算障碍距离场（Eq.26 第三项 Σe^{-d_k/σ} 所需）
    _dist_field = compute_obstacle_distance_field(grid_map)

    def _run_planner(r_min: float, step_len: float, p_theta: float, budget_s: float):
        """构造 LOHybridAStarPlanner 并运行，返回 (path, stats)。"""
        p = AckermannParams(
            wheelbase=params.wheelbase,
            min_turn_radius=r_min,
            v_max=params.v_max,
        )
        prims = default_primitives(p, step_length=step_len)
        planner = LOHybridAStarPlanner(
            grid_map, footprint, p,
            primitives=prims,
            goal_xy_tol=float(goal_xy_tol_m),
            goal_theta_tol=float(goal_theta_tol_rad),
            heading_change_penalty=p_theta,
            collision_padding=collision_padding,
            collision_checker=collision_checker,
        )
        return planner.plan(start, goal, timeout=budget_s, max_nodes=int(max_nodes), self_check=False)

    def _eq26_fitness(path_states, stats_i: dict) -> float:
        """论文 Eq.26 适应度计算。

        f = ω₁·(L/L_ref) + ω₂·max|κ| + ω₃·Σe^{-d_k/σ}

        max|κ| = 1/min_turn_radius（弧率最大值）
        Σe^{-d_k/σ}：路径各点障碍抵近度累和
        """
        L = float(stats_i.get("path_length", 0.0))
        if L <= 0.0:
            return float("inf")

        # 第一项：归一化路径长度
        term1 = _W1 * (L / L_ref)

        # 第二项：最大曲率（用 stats 中的 min_turn_radius 替代）
        kappa_max = float(stats_i.get("max_curvature", 0.0))
        if kappa_max <= 0.0:
            # 若 stats 未报告，退而取 1/路径步数 作占位（保守估计）
            kappa_max = 0.0
        term2 = _W2 * kappa_max

        # 第三项：障碍排斥项 Σe^{-d_k/σ}
        proximity_sum = 0.0
        for s in path_states:
            d = query_distance(_dist_field, grid_map, s.x, s.y)
            proximity_sum += math.exp(-d / _SIGMA)
        term3 = _W3 * proximity_sum

        return term1 + term2 + term3

    start_time = time.perf_counter()

    if lo_iterations <= 0:
        # 快速模式：仅内层改进，默认参数（论文表 III 推荐值中间点）
        path, stats = _run_planner(
            r_min=params.min_turn_radius,
            step_len=0.5,
            p_theta=0.01,
            budget_s=float(timeout_s),
        )
    else:
        # LOA 外层参数优化模式
        # 预算分配：80% 给 LOA 搜索，20% 给最终最优参数跑一次
        # NOTE: per_eval_budget 上限 30s 是为高分辨率地图 (cell_size≤0.1m) 适配
        # —— 论文 1m cell 单次 HA*<1s，但 0.1m cell 上单次 HA* 5-25s。
        lo_budget = float(timeout_s) * 0.8
        per_eval_budget = lo_budget / max(1, lo_population * lo_iterations) * 3.0
        per_eval_budget = max(0.2, min(per_eval_budget, 30.0))

        def fitness(x: np.ndarray) -> float:
            r_min, step_len, p_theta = float(x[0]), float(x[1]), float(x[2])
            elapsed = time.perf_counter() - start_time
            remaining = lo_budget - elapsed
            if remaining <= 0.1:
                return float("inf")
            budget = min(per_eval_budget, remaining)
            path_i, stats_i = _run_planner(r_min, step_len, p_theta, budget)
            if not path_i:
                return float("inf")
            return _eq26_fitness(path_i, stats_i)

        # LOA 搜索范围（论文参数范围）
        bounds = [
            (0.8, 1.2),      # min_r（最小转弯半径，m）
            (0.4, 0.6),      # step（运动基元步长，m）
            (0.005, 0.015),  # P_θ（航向变化惩罚系数）
        ]
        seed_vec = np.array([
            min(max(params.min_turn_radius, 0.8), 1.2),
            0.5,
            0.01,
        ])
        opt = LemmingOptimizer(
            population_size=lo_population,
            max_iterations=lo_iterations,
            seed=lo_seed,
        )
        best = opt.optimize(
            fitness_fn=fitness,
            bounds=bounds,
            seed_params=seed_vec,
        )
        remaining = float(timeout_s) - (time.perf_counter() - start_time)
        path, stats = _run_planner(
            r_min=float(best[0]),
            step_len=float(best[1]),
            p_theta=float(best[2]),
            budget_s=max(0.5, remaining),
        )
        stats["lo_best_params"] = {
            "min_turn_radius": float(best[0]),
            "step_length": float(best[1]),
            "heading_change_penalty": float(best[2]),
        }

    dt = time.perf_counter() - start_time
    if path:
        trace_poses = stats.get("trace_poses")
        if trace_poses and len(trace_poses) >= 2:
            pts = [(float(x) / cell_size_m, float(y) / cell_size_m) for x, y, _th in trace_poses]
        else:
            pts = [(float(s.x) / cell_size_m, float(s.y) / cell_size_m) for s in path]
        return PlannerResult(path_xy_cells=pts, time_s=dt, success=True, stats=stats)
    return PlannerResult(
        path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
        time_s=dt,
        success=False,
        stats=stats,
    )
