from __future__ import annotations

import math
import sys
import types
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def test_dilated_map_and_corridor_boxes_follow_algorithm1_shape():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.corridor import build_two_stage_corridor, split_wide_narrow_paths
    from lian2023_strict.grid import create_dilated_map
    from lian2023_strict.scenes import build_scene

    scene = build_scene("fig5c")
    vehicle = load_vehicle_params()
    params = load_algorithm_params()
    dilated = create_dilated_map(scene.grid, scene.cell_size_m, vehicle.disc_radius_m)
    assert np.count_nonzero(dilated) > np.count_nonzero(scene.grid)

    lead = np.array([[-15.0, -15.0], [-10.0, -8.0], [-2.0, -2.0], [8.0, 6.0], [14.5, 13.5]])
    boxes = build_two_stage_corridor(dilated, scene.bounds_m, scene.cell_size_m, lead, params)
    assert boxes
    first = boxes[0]
    assert first.left_m >= 0.0
    assert first.right_m >= 0.0
    assert first.up_m >= 0.0
    assert first.down_m >= 0.0
    assert first.min_side_m == min(first.left_m + first.right_m, first.up_m + first.down_m)

    groups = split_wide_narrow_paths(boxes)
    assert groups
    assert all(group.kind in {"wide", "narrow"} for group in groups)
    assert sum(len(group.boxes) for group in groups) == len(boxes)


def test_boundary_correction_uses_lpthre_cells():
    from lian2023_strict.config import load_algorithm_params
    from lian2023_strict.corridor import correct_boundary_points

    params = load_algorithm_params()
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [8.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    corrected = correct_boundary_points(points, cell_size_m=0.2, params=params)
    assert corrected.shape[0] == 3
    assert np.allclose(corrected[0], points[0])
    assert np.allclose(corrected[-1], points[-1])


def test_algorithm1_stage1_builds_explicit_wide_narrow_path_sets():
    from lian2023_strict.config import load_algorithm_params
    from lian2023_strict.corridor import CorridorBox, build_algorithm1_stage1

    params = load_algorithm_params(wide_passage_threshold_m=1.0)
    path = np.array([[float(i), 0.0] for i in range(6)], dtype=float)
    boxes = [
        CorridorBox((0.0, 0.0), (1.0, 0.0), 1.2, 1.2, 1.2, 1.2, 0.0, True),
        CorridorBox((1.0, 0.0), (1.0, 0.0), 1.2, 1.2, 1.2, 1.2, 1.0, True),
        CorridorBox((2.0, 0.0), (1.0, 0.0), 0.4, 0.4, 0.4, 0.4, 2.0, False),
        CorridorBox((3.0, 0.0), (1.0, 0.0), 0.4, 0.4, 0.4, 0.4, 3.0, False),
        CorridorBox((4.0, 0.0), (1.0, 0.0), 1.3, 1.3, 1.3, 1.3, 4.0, True),
        CorridorBox((5.0, 0.0), (1.0, 0.0), 1.3, 1.3, 1.3, 1.3, 5.0, True),
    ]

    stage1 = build_algorithm1_stage1(path, boxes, 0.0, 0.0, params)

    assert [group.kind for group in stage1.xseq] == ["wide", "narrow", "wide"]
    assert len(stage1.swps) == 2
    assert len(stage1.snps) == 1
    assert stage1.xbou[0, 0] == 0.0
    assert stage1.xbou[-1, 0] == 5.0
    assert stage1.xbou_corrected.shape == stage1.xbou.shape


def test_hybrid_astar_segment_respects_obstacle_gap():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.hybrid_astar import hybrid_astar_segment

    grid = np.zeros((41, 41), dtype=np.uint8)
    grid[:, 20] = 1
    grid[19:22, 20] = 0
    segment = hybrid_astar_segment(
        grid=grid,
        bounds_m=(-4.0, 4.0, -4.0, 4.0),
        cell_size_m=0.2,
        start=(-3.0, 0.0, 0.0),
        goal=(3.0, 0.0, 0.0),
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(),
        timeout_s=5.0,
    )
    assert len(segment) > 2
    assert np.max(np.abs(segment[:, 1])) <= 0.6
    assert np.any(np.isclose(segment[:, 0], 0.0, atol=0.25))


def test_hybrid_astar_segment_does_not_finish_on_xy_only_match():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.hybrid_astar import hybrid_astar_segment

    grid = np.zeros((81, 81), dtype=np.uint8)
    params = load_algorithm_params(iha_xy_resolution_m=0.2, iha_heading_resolution_rad=0.2)
    segment = hybrid_astar_segment(
        grid=grid,
        bounds_m=(-8.0, 8.0, -8.0, 8.0),
        cell_size_m=0.2,
        start=(0.0, 0.0, 0.0),
        goal=(0.2, 0.0, math.pi),
        vehicle=load_vehicle_params(),
        params=params,
        timeout_s=2.0,
    )

    if len(segment) > 1:
        heading_steps = np.abs(np.diff(np.unwrap(segment[:, 2])))
        assert float(np.max(heading_steps)) <= 1.5 * params.iha_heading_resolution_rad


def test_stage1_diagnostics_record_segment_and_seed_quality_for_fig5b():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.diagnostics import diagnose_stage1

    result = diagnose_stage1(
        "fig5b",
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(n_elements=40, max_iterations=1, ipopt_max_iterations=1),
        segment_timeout_s=5.0,
    )

    assert result["scene"] == "fig5b"
    assert result["grid_path_points"] > 0
    assert result["xbou_corrected_count"] >= 2
    assert result["seed"]["jinf"] >= 0.0
    assert result["seed"]["top_kinematic_residual"]["k"] >= 0
    assert result["segments"]
    assert all("pre_append_heading_error_rad" in segment for segment in result["segments"])


def test_formula_terms_match_paper_shapes_and_zero_residuals():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import (
        evaluate_formula16_objective,
        evaluate_formula23_penalty,
        evaluate_kinematic_residuals,
    )

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=4)
    tf = 4.0
    states = np.zeros((5, 5), dtype=float)
    states[:, 0] = np.arange(5, dtype=float)
    states[:, 3] = 1.0
    states[-1, 3] = 1.0
    controls = np.zeros((4, 2), dtype=float)

    residuals = evaluate_kinematic_residuals(states, controls, tf, vehicle)
    assert residuals.shape == (4, 5)
    assert np.allclose(residuals, 0.0, atol=1e-9)

    objective = evaluate_formula16_objective(states, tf, params)
    assert math.isclose(objective, params.mu1 * tf, rel_tol=1e-9)

    penalty = evaluate_formula23_penalty(
        states,
        controls,
        tf,
        vehicle,
        params,
        corridor_bounds=None,
    )
    assert penalty >= 0.0
    assert penalty < 1e-9


def test_disk_centers_follow_formula7_offsets():
    from lian2023_strict.config import load_vehicle_params
    from lian2023_strict.ocp import disk_centers_from_states

    vehicle = load_vehicle_params()
    states = np.array([[1.0, 2.0, 0.0, 0.0, 0.0]], dtype=float)

    centers = disk_centers_from_states(states, vehicle)

    expected_x = [1.0 + offset for offset in vehicle.disc_offsets_m]
    assert centers.shape == (1, 2, 2)
    assert np.allclose(centers[0, :, 0], expected_x)
    assert np.allclose(centers[0, :, 1], [2.0, 2.0])


def test_formula6_is_measured_separately_from_formula23_penalty():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.corridor import CorridorBox
    from lian2023_strict.ocp import evaluate_formula23_components, evaluate_formula23_penalty

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=1)
    states = np.zeros((2, 5), dtype=float)
    controls = np.zeros((1, 2), dtype=float)
    box = CorridorBox(
        center=(0.0, 0.0),
        tangent=(1.0, 0.0),
        left_m=0.5,
        right_m=0.5,
        up_m=0.5,
        down_m=0.5,
        arc_m=0.0,
        is_wide=False,
    )

    components = evaluate_formula23_components(states, controls, 1.0, vehicle, params, corridor_boxes=[box])
    penalty = evaluate_formula23_penalty(states, controls, 1.0, vehicle, params, corridor_boxes=[box])

    assert components["jpenalty6"] > 0.0
    assert components["jinf"] == components["jpenalty3"] + components["jpenalty7"] + components["jpenalty15"]
    assert penalty == components["jinf"]


def test_formula6_hard_bounds_apply_to_k_zero_to_n_minus_one(monkeypatch):
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.corridor import CorridorBox
    from lian2023_strict.ocp import _pack, _state_control_ipopt, disk_centers_from_states

    captured: dict[str, list[tuple[float, float]]] = {}

    def fake_minimize_ipopt(objective, q0, jac, bounds, options):
        captured["bounds"] = bounds
        objective(q0)
        jac(q0)
        return types.SimpleNamespace(x=q0.copy(), message="fake", nit=0)

    monkeypatch.setitem(sys.modules, "cyipopt", types.SimpleNamespace(minimize_ipopt=fake_minimize_ipopt))

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=1, max_iterations=1, ipopt_max_iterations=1)
    states = np.array([[0.0, 0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0, 0.0]], dtype=float)
    controls = np.zeros((1, 2), dtype=float)
    box = CorridorBox((0.0, 0.0), (1.0, 0.0), 0.1, 0.1, 0.1, 0.1, 0.0, False)

    _state_control_ipopt(
        states_ref=states,
        controls_ref=controls,
        tf_ref=1.0,
        start=tuple(states[0]),
        goal=tuple(states[-1]),
        vehicle=vehicle,
        params=params,
        corridor_boxes=(box,),
    )

    q = _pack(states, controls, disk_centers_from_states(states, vehicle), 1.0)
    disk_start = states.size + controls.size
    disk_bounds = captured["bounds"][disk_start : len(q) - 1]
    first_k = disk_bounds[:4]
    terminal_k = disk_bounds[4:]
    assert all(math.isfinite(lo) and math.isfinite(hi) for lo, hi in first_k)
    assert all(math.isinf(lo) and math.isinf(hi) for lo, hi in terminal_k)


def test_formula6_hard_bounds_apply_to_all_nonterminal_knots(monkeypatch):
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.corridor import CorridorBox
    from lian2023_strict.ocp import _state_control_ipopt

    captured: dict[str, list[tuple[float, float]]] = {}

    def fake_minimize_ipopt(objective, q0, jac, bounds, options):
        captured["bounds"] = bounds
        objective(q0)
        jac(q0)
        return types.SimpleNamespace(x=q0.copy(), message="fake", nit=0)

    monkeypatch.setitem(sys.modules, "cyipopt", types.SimpleNamespace(minimize_ipopt=fake_minimize_ipopt))

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=3, max_iterations=1, ipopt_max_iterations=1)
    states = np.zeros((4, 5), dtype=float)
    states[:, 0] = np.arange(4, dtype=float)
    controls = np.zeros((3, 2), dtype=float)
    box = CorridorBox((1.0, 0.0), (1.0, 0.0), 2.0, 2.0, 2.0, 2.0, 0.0, True)

    _state_control_ipopt(
        states_ref=states,
        controls_ref=controls,
        tf_ref=1.0,
        start=tuple(states[0]),
        goal=tuple(states[-1]),
        vehicle=vehicle,
        params=params,
        corridor_boxes=(box,),
    )

    state_len = states.size
    control_len = controls.size
    disk_bounds = captured["bounds"][state_len + control_len : -1]
    bounds_by_k = [disk_bounds[i * 4 : (i + 1) * 4] for i in range(4)]
    assert all(all(math.isfinite(lo) and math.isfinite(hi) for lo, hi in bounds) for bounds in bounds_by_k[:-1])
    assert all(math.isinf(lo) and math.isinf(hi) for lo, hi in bounds_by_k[-1])


def test_table2_rows_record_ipopt_max_iterations():
    from lian2023_strict.scripts.run_table2 import TABLE2_FIELDS, _row_from_result
    from lian2023_strict.planner import PlannerMethod

    result = types.SimpleNamespace(
        success=True,
        status="success",
        stats={
            "cpu_time_i_s": 0.0,
            "ipopt_max_iterations": 1000,
        },
    )

    row = _row_from_result("fig5a", PlannerMethod.OURS_EHA_IPOPT, result)

    assert "ipopt_max_iterations" in TABLE2_FIELDS
    assert row["ipopt_max_iterations"] == "1000"


def test_jpenalty7_positive_for_inconsistent_disk_centers():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import disk_centers_from_states, evaluate_formula23_components

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=1)
    states = np.zeros((2, 5), dtype=float)
    controls = np.zeros((1, 2), dtype=float)
    centers = disk_centers_from_states(states, vehicle)
    centers[:, :, 0] += 0.25

    components = evaluate_formula23_components(
        states,
        controls,
        1.0,
        vehicle,
        params,
        disk_centers=centers,
    )

    assert components["jpenalty7"] > 0.0


def test_state_control_ipopt_objective_includes_jpenalty7(monkeypatch):
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import _state_control_ipopt

    captured: dict[str, float] = {}

    def fake_minimize_ipopt(objective, q0, jac, bounds, options):
        q_bad = q0.copy()
        disk_start = 2 * 5 + 1 * 2
        q_bad[disk_start] += 0.25
        captured["base"] = float(objective(q0))
        captured["bad"] = float(objective(q_bad))
        jac(q_bad)
        return types.SimpleNamespace(x=q0.copy(), message="fake", nit=0)

    monkeypatch.setitem(sys.modules, "cyipopt", types.SimpleNamespace(minimize_ipopt=fake_minimize_ipopt))

    vehicle = load_vehicle_params()
    params = load_algorithm_params(
        n_elements=1,
        max_iterations=1,
        ipopt_max_iterations=1,
        initial_penalty=11.0,
        enable_local_state_constraint=False,
    )
    states = np.array([[0.0, 0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0, 0.0]], dtype=float)
    controls = np.zeros((1, 2), dtype=float)

    _state_control_ipopt(
        states_ref=states,
        controls_ref=controls,
        tf_ref=1.0,
        start=tuple(states[0]),
        goal=tuple(states[-1]),
        vehicle=vehicle,
        params=params,
    )

    assert math.isclose(captured["bad"] - captured["base"], 11.0 * 0.25 * 0.25, rel_tol=1e-9)


def test_formula16_and_formula23_gradient_matches_finite_difference():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import (
        _formula16_gradient,
        _formula23_penalty_gradient,
        _pack,
        _unpack,
        disk_centers_from_states,
        evaluate_formula16_objective,
        evaluate_formula23_penalty,
    )

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=2)
    states = np.array(
        [
            [0.0, 0.0, 0.1, 0.7, 0.05],
            [0.5, 0.1, 0.15, 0.8, 0.04],
            [1.1, 0.3, 0.18, 0.6, 0.02],
        ],
        dtype=float,
    )
    controls = np.array([[0.1, -0.02], [-0.05, 0.03]], dtype=float)
    disks = disk_centers_from_states(states, vehicle)
    disks[1, 0, 0] += 0.03
    tf = 2.0
    weight = 7.0

    def objective(q: np.ndarray) -> float:
        s, u, d, t = _unpack(q, 2, 2)
        return evaluate_formula16_objective(s, t, params) + weight * evaluate_formula23_penalty(
            s,
            u,
            t,
            vehicle,
            params,
            disk_centers=d,
        )

    q = _pack(states, controls, disks, tf)
    g16_s, g16_u, g16_tf = _formula16_gradient(states, controls, tf, params)
    g23_s, g23_u, g23_d, g23_tf = _formula23_penalty_gradient(states, controls, disks, tf, vehicle, params)
    analytic = _pack(g16_s + weight * g23_s, g16_u + weight * g23_u, weight * g23_d, g16_tf + weight * g23_tf)

    for idx in (0, 4, 7, 12, 16, 20, len(q) - 1):
        step = 1e-6
        direction = np.zeros_like(q)
        direction[idx] = step
        numeric = (objective(q + direction) - objective(q - direction)) / (2.0 * step)
        assert math.isclose(analytic[idx], numeric, rel_tol=1e-4, abs_tol=1e-4)


def test_local_state_constraint_gradient_matches_finite_difference():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import (
        _formula23_penalty_gradient,
        _pack,
        _unpack,
        disk_centers_from_states,
        evaluate_formula23_penalty,
    )

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=1, enable_local_state_constraint=True)
    states = np.array(
        [
            [-5.0, -6.15, 0.0, 3.0, 0.0],
            [-4.5, -6.12, 0.0, 2.8, 0.0],
        ],
        dtype=float,
    )
    controls = np.zeros((1, 2), dtype=float)
    disks = disk_centers_from_states(states, vehicle)
    tf = 1.0

    def objective(q: np.ndarray) -> float:
        s, u, d, t = _unpack(q, 1, 2)
        return evaluate_formula23_penalty(s, u, t, vehicle, params, disk_centers=d)

    q = _pack(states, controls, disks, tf)
    g_s, g_u, g_d, g_tf = _formula23_penalty_gradient(states, controls, disks, tf, vehicle, params)
    analytic = _pack(g_s, g_u, g_d, g_tf)

    for idx in (0, 1, 3, 5, 6, 8):
        step = 1e-6
        direction = np.zeros_like(q)
        direction[idx] = step
        numeric = (objective(q + direction) - objective(q - direction)) / (2.0 * step)
        assert math.isclose(analytic[idx], numeric, rel_tol=1e-4, abs_tol=1e-4)


def test_initial_guess_preserves_reverse_hybrid_astar_heading():
    from lian2023_strict.config import load_vehicle_params
    from lian2023_strict.ocp import _initial_guess_from_poses

    vehicle = load_vehicle_params()
    poses = np.array(
        [
            [0.0, 0.0, math.pi / 2.0],
            [0.0, -1.0, math.pi / 2.0],
            [0.0, -2.0, math.pi / 2.0],
        ],
        dtype=float,
    )
    states, _controls, _tf = _initial_guess_from_poses(
        poses,
        (0.0, 0.0, math.pi / 2.0, 0.0, 0.0),
        (0.0, -2.0, math.pi / 2.0, 0.0, 0.0),
        vehicle,
        8,
    )

    assert np.max(np.abs(states[:, 2] - math.pi / 2.0)) < 1e-9
    assert np.min(states[1:-1, 3]) < 0.0


def test_second_stage_rebuilds_corridor_each_outer_iteration():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import smooth_initial_guess

    calls: list[np.ndarray] = []

    def corridor_provider(states: np.ndarray) -> tuple:
        calls.append(states.copy())
        return tuple()

    params = load_algorithm_params(
        n_elements=3,
        max_iterations=2,
        ipopt_max_iterations=1,
        etol=-1.0,
    )

    _states, _controls, stats = smooth_initial_guess(
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=float),
        (0.0, 0.0, 0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0, 0.0),
        load_vehicle_params(),
        params,
        corridor_provider=corridor_provider,
    )

    assert len(calls) == 2
    assert calls[0].shape == calls[1].shape == (4, 5)
    assert not np.allclose(calls[0], calls[1])
    assert stats["outer_iterations"] == 2.0
    assert stats["final_penalty_weight"] == params.initial_penalty * params.penalty_growth
