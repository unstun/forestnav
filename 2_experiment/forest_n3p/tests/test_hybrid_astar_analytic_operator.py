import numpy as np

from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, HybridAStarPlanner, TwoCircleFootprint


def _planner(operator):
    grid_map = GridMap(np.zeros((80, 80), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    return _planner_for_grid(operator, grid_map)


def _planner_for_grid(operator, grid_map):
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)
    return HybridAStarPlanner(
        grid_map,
        footprint,
        AckermannParams(wheelbase=0.5, min_turn_radius=1.0),
        analytic_operator=operator,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=0.30,
        theta_bins=16,
    )


def test_analytic_operator_is_reported_for_same_query():
    start = AckermannState(1.0, 1.0, 0.0)
    goal = AckermannState(1.8, 1.0, 0.0)
    stats_by_operator = {}

    for operator in ("disabled", "single_rs", "dang_multi_rs"):
        path, stats = _planner(operator).plan(start, goal, timeout=1.0, max_nodes=2_000)
        assert path
        assert stats["analytic_operator"] == operator
        stats_by_operator[operator] = stats

    assert "remediations" not in stats_by_operator["disabled"]
    assert stats_by_operator["disabled"]["analytic_attempts"] == 0
    assert stats_by_operator["disabled"]["analytic_successes"] == 0
    assert "analytic_expansion" in stats_by_operator["single_rs"]["remediations"]
    assert "analytic_operator:single_rs" in stats_by_operator["single_rs"]["remediations"]
    assert stats_by_operator["single_rs"]["analytic_attempts"] == 1
    assert stats_by_operator["single_rs"]["analytic_successes"] == 1
    assert "analytic_expansion" in stats_by_operator["dang_multi_rs"]["remediations"]
    assert "analytic_operator:dang_multi_rs" in stats_by_operator["dang_multi_rs"]["remediations"]
    assert stats_by_operator["dang_multi_rs"]["analytic_attempts"] == 1
    assert stats_by_operator["dang_multi_rs"]["analytic_successes"] == 1


def test_legacy_analytic_expansion_false_selects_disabled_operator():
    planner = HybridAStarPlanner(
        GridMap(np.zeros((40, 40), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0)),
        TwoCircleFootprint.from_box(length=0.4, width=0.2),
        AckermannParams(wheelbase=0.5, min_turn_radius=1.0),
        analytic_expansion=False,
        theta_bins=16,
    )

    assert planner.analytic_operator == "disabled"
    assert not planner.analytic_expansion


def test_failed_analytic_operator_attempt_is_counted_without_success():
    data = np.zeros((80, 80), dtype=np.uint8)
    data[8:13, 14:17] = 1
    planner = _planner_for_grid("single_rs", GridMap(data, resolution=0.1, origin=(0.0, 0.0)))

    path, stats = planner.plan(
        AckermannState(1.0, 1.0, 0.0),
        AckermannState(2.0, 1.0, 0.0),
        timeout=1.0,
        max_nodes=1,
    )

    assert not path
    assert stats["failure_reason"] == "node_budget_exhausted"
    assert stats["analytic_operator"] == "single_rs"
    assert stats["analytic_attempts"] == 1
    assert stats["analytic_successes"] == 0
