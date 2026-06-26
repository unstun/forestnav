from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def _build_cpp_backend() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_ocp_fast.py")],
        cwd=str(ROOT),
        check=True,
    )


def test_cpp_formula23_backend_matches_python_value_and_gradient(monkeypatch):
    _build_cpp_backend()

    monkeypatch.setenv("LIAN2023_STRICT_DISABLE_CPP", "1")
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.ocp import (
        _formula23_penalty_gradient as python_gradient,
        disk_centers_from_states,
        evaluate_formula23_penalty as python_penalty,
    )

    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=2, enable_local_state_constraint=True)
    states = np.array(
        [
            [-5.0, -6.15, 0.1, 3.0, 0.05],
            [-4.5, -6.12, 0.15, 2.8, 0.04],
            [-4.1, -6.08, 0.18, 2.4, 0.02],
        ],
        dtype=float,
    )
    controls = np.array([[0.1, -0.02], [-0.05, 0.03]], dtype=float)
    disks = disk_centers_from_states(states, vehicle)
    disks[1, 0, 0] += 0.03
    tf = 2.0

    expected_value = python_penalty(states, controls, tf, vehicle, params, disk_centers=disks)
    expected_gradient = python_gradient(states, controls, disks, tf, vehicle, params)

    monkeypatch.setenv("LIAN2023_STRICT_DISABLE_CPP", "0")
    monkeypatch.setenv("LIAN2023_STRICT_USE_CPP", "1")
    from lian2023_strict import ocp_fast
    import lian2023_strict.ocp as ocp

    assert ocp_fast.is_available()
    actual_value = ocp.evaluate_formula23_penalty(states, controls, tf, vehicle, params, disk_centers=disks)
    actual_gradient = ocp._formula23_penalty_gradient(states, controls, disks, tf, vehicle, params)

    assert math.isclose(actual_value, expected_value, rel_tol=1e-11, abs_tol=1e-11)
    for actual, expected in zip(actual_gradient, expected_gradient, strict=True):
        assert np.allclose(actual, expected, rtol=1e-10, atol=1e-10)


def test_cpp_packed_objective_and_gradient_match_python(monkeypatch):
    _build_cpp_backend()

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
    from lian2023_strict import ocp_fast

    monkeypatch.setenv("LIAN2023_STRICT_USE_CPP", "1")
    vehicle = load_vehicle_params()
    params = load_algorithm_params(n_elements=2, enable_local_state_constraint=True)
    states = np.array(
        [
            [-5.0, -6.15, 0.1, 3.0, 0.05],
            [-4.5, -6.12, 0.15, 2.8, 0.04],
            [-4.1, -6.08, 0.18, 2.4, 0.02],
        ],
        dtype=float,
    )
    controls = np.array([[0.1, -0.02], [-0.05, 0.03]], dtype=float)
    disks = disk_centers_from_states(states, vehicle)
    disks[1, 0, 0] += 0.03
    tf = 2.0
    weight = 11.0
    q = _pack(states, controls, disks, tf)

    def python_objective(q_arr: np.ndarray) -> float:
        s, u, d, t = _unpack(q_arr, 2, 2)
        return evaluate_formula16_objective(s, t, params) + weight * evaluate_formula23_penalty(
            s,
            u,
            t,
            vehicle,
            params,
            disk_centers=d,
        )

    g16_s, g16_u, g16_tf = _formula16_gradient(states, controls, tf, params)
    g23_s, g23_u, g23_d, g23_tf = _formula23_penalty_gradient(states, controls, disks, tf, vehicle, params)
    python_gradient = _pack(g16_s + weight * g23_s, g16_u + weight * g23_u, weight * g23_d, g16_tf + weight * g23_tf)

    assert math.isclose(
        ocp_fast.packed_objective(q, n_controls=2, disc_count=2, vehicle=vehicle, params=params, penalty_weight=weight),
        python_objective(q),
        rel_tol=1e-11,
        abs_tol=1e-11,
    )
    assert np.allclose(
        ocp_fast.packed_gradient(q, n_controls=2, disc_count=2, vehicle=vehicle, params=params, penalty_weight=weight),
        python_gradient,
        rtol=1e-10,
        atol=1e-10,
    )
