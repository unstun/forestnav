from __future__ import annotations

import math

import numpy as np


def test_voronoi_field_is_lower_on_corridor_centerline_than_near_wall():
    from dang2022_strict.grid import GridMap
    from dang2022_strict.voronoi import compute_voronoi_field

    grid = np.zeros((11, 21), dtype=np.uint8)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    field = compute_voronoi_field(GridMap(grid, resolution=1.0), alpha=5.0, d_o_max=5.0)

    assert field[5, 10] < field[2, 10]
    assert field[5, 10] <= 1e-6


def test_multi_curvature_rs_selects_lower_cost_valid_candidate():
    from dang2022_strict.config import paper_algorithm_params, paper_vehicle_params
    from dang2022_strict.grid import GridMap
    from dang2022_strict.planner import DangHybridAStarPlanner
    from dang2022_strict.robot import Pose

    grid = np.zeros((24, 32), dtype=np.uint8)
    grid[:2, :] = 1
    grid[-2:, :] = 1
    grid[:, :2] = 1
    grid[:, -2:] = 1
    grid[12:22, 18:20] = 1

    planner = DangHybridAStarPlanner(
        GridMap(grid, resolution=1.0),
        paper_vehicle_params(),
        paper_algorithm_params(curvature_resolution=0.05),
    )
    candidates = planner.evaluate_analytic_candidates(
        Pose(5.0, 5.0, 0.0),
        Pose(25.0, 18.0, math.pi / 2.0),
    )

    assert len(candidates) >= 1
    best = min(candidates, key=lambda c: c.total_cost)
    assert math.isfinite(best.total_cost)
    assert 0.0 < best.curvature <= paper_vehicle_params().max_curvature
    assert best is candidates[0]


def test_planner_solves_small_open_scene_with_trace_stats():
    from dang2022_strict.config import paper_algorithm_params, paper_vehicle_params
    from dang2022_strict.grid import GridMap
    from dang2022_strict.planner import DangHybridAStarPlanner
    from dang2022_strict.robot import Pose

    grid = np.zeros((18, 28), dtype=np.uint8)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    planner = DangHybridAStarPlanner(
        GridMap(grid, resolution=1.0),
        paper_vehicle_params(length_m=1.5, width_m=0.7, wheelbase_m=1.0, max_steer_rad=0.6),
        paper_algorithm_params(max_nodes=20_000, motion_primitive_m=1.5),
    )
    result = planner.plan(Pose(4.0, 4.0, 0.0), Pose(21.0, 4.0, 0.0), timeout_s=5.0)

    assert result.success is True
    assert result.path
    assert result.stats["variant"] == "dang2022_strict"
    assert result.stats["motion_primitive_m"] == 1.5
    assert result.stats["curvature_resolution"] == 0.05
    assert result.stats["use_reeds_shepp_heuristic"] == "True"
    assert result.stats["path_length_m"] > 0.0
    assert result.stats["turning_points"] >= 0


def test_planner_exports_dense_sampled_path_for_analytic_expansion():
    from dang2022_strict.config import paper_algorithm_params, paper_vehicle_params
    from dang2022_strict.grid import GridMap
    from dang2022_strict.planner import DangHybridAStarPlanner
    from dang2022_strict.robot import Pose

    grid = np.zeros((18, 28), dtype=np.uint8)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    planner = DangHybridAStarPlanner(
        GridMap(grid, resolution=1.0),
        paper_vehicle_params(length_m=1.5, width_m=0.7, wheelbase_m=1.0, max_steer_rad=0.6),
        paper_algorithm_params(max_nodes=20_000, motion_primitive_m=1.5, collision_step_m=0.2),
    )
    result = planner.plan(Pose(4.0, 4.0, 0.0), Pose(21.0, 4.0, 0.0), timeout_s=5.0)

    assert result.success is True
    assert result.analytic_path
    assert result.dense_path
    assert len(result.dense_path) > len(result.path)
    max_step = max(
        math.hypot(b.x - a.x, b.y - a.y)
        for a, b in zip(result.dense_path, result.dense_path[1:])
    )
    assert max_step <= 0.25
