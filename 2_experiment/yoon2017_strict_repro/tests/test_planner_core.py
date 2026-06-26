from __future__ import annotations


def test_planner_runs_reconstructed_narrow_passage_scene():
    from yoon2017_strict.config import paper_algorithm_params, paper_sim_vehicle_params
    from yoon2017_strict.planner import YoonSplineRRTStarPlanner
    from yoon2017_strict.scenes import build_scene

    scene = build_scene("narrow_passage")
    params = paper_algorithm_params(max_iterations=800, goal_sample_rate=0.2)
    planner = YoonSplineRRTStarPlanner(scene.grid_map(), paper_sim_vehicle_params(), params)
    result = planner.plan(scene.start_pose(), scene.goal_pose(), seed=0, timeout_s=10.0)

    assert result.stats["variant"] == "yoon2017_strict"
    assert result.stats["paper_algorithm"] == "SS-RRT*"
    assert result.stats["steer_step_m"] == 5.0
    assert isinstance(result.success, bool)
    assert result.path
