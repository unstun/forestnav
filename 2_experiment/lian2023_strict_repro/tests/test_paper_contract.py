from __future__ import annotations

import ast
import csv
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_paper_params_match_table_i():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params

    vehicle = load_vehicle_params()
    params = load_algorithm_params()

    assert vehicle.length_m == 4.8
    assert vehicle.front_overhang_m == 0.95
    assert vehicle.wheelbase_m == 2.8
    assert vehicle.rear_overhang_m == 1.05
    assert vehicle.width_m == 1.9
    assert vehicle.max_accel_m_s2 == 2.0
    assert vehicle.max_omega_rad_s == 0.85
    assert vehicle.max_velocity_m_s == 5.0
    assert vehicle.max_steer_rad == 0.85
    assert params.mu1 == 1.0
    assert params.mu2 == 0.01
    assert params.mu3 == 0.01
    assert params.initial_penalty == 1e6
    assert params.n_elements == 200
    assert params.disc_count == 2
    assert params.max_iterations == 10
    assert params.penalty_growth == 5.0
    assert params.etol == 1e-4
    assert params.dl1_m == 1.0
    assert params.dl2_m == 0.1
    assert params.max_box_side_m == 8.0
    assert params.boundary_point_passage_threshold_cells == 30
    assert params.wide_passage_threshold_m == 4.5
    assert params.iha_xy_resolution_m == 0.2
    assert params.iha_heading_resolution_rad == 0.2
    assert params.beta == 10.0


def test_strict_package_does_not_import_ugv_dqn():
    package_dir = SRC / "lian2023_strict"
    assert package_dir.is_dir()
    violations: list[str] = []
    forbidden_terms = (
        "ugv_dqn",
        "realmap",
        "benchmark_baselines",
        "lian2023_paper_only",
        "lian2023_paper_from_scratch",
    )
    for path in sorted(package_dir.rglob("*.py")):
        src = path.read_text(encoding="utf-8")
        for term in forbidden_terms:
            assert term not in src, f"{path}:{term}"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "ugv_dqn" or alias.name.startswith("ugv_dqn."):
                        violations.append(f"{path.name}:{node.lineno}:{alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module == "ugv_dqn" or module.startswith("ugv_dqn."):
                    violations.append(f"{path.name}:{node.lineno}:{module}")
    assert violations == []


def test_project_has_package_metadata_and_dependencies():
    pyproject = ROOT / "pyproject.toml"
    assert pyproject.is_file()
    text = pyproject.read_text(encoding="utf-8")
    for dep in ("numpy", "scipy", "matplotlib", "cyipopt"):
        assert dep in text


def test_figure_reconstructed_scene_fig5c_has_obstacles_and_local_units():
    from lian2023_strict.scenes import build_scene

    scene = build_scene("fig5c")
    assert scene.name == "fig5c"
    assert scene.cell_size_m == 0.2
    assert scene.grid.shape == (201, 201)
    assert np.count_nonzero(scene.grid) > 500
    assert scene.start[:2] == (-15.0, -15.0)
    assert scene.goal[0] > 10.0
    assert scene.bounds_m == (-20.0, 20.0, -20.0, 20.0)


def test_ours_eha_ipopt_smoke_runs_without_nonpaper_fallback(tmp_path):
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.planner import PlannerMethod, plan_scene
    from lian2023_strict.scenes import build_scene

    scene = build_scene("fig5a")
    result = plan_scene(
        scene,
        method=PlannerMethod.OURS_EHA_IPOPT,
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(n_elements=20, max_iterations=1, ipopt_max_iterations=5, etol=1e12),
        timeout_s=20.0,
    )

    assert result.status in {"success", "stage1_eha_fail", "stage2_infeasible"}
    assert result.stats["stage1_fallback"] == "false"
    assert result.stats["cpu_time_i_s"] >= 0.0
    if len(result.states) > 0:
        assert result.states.shape == (21, 5)
        assert result.controls.shape == (20, 2)
        assert np.isfinite(result.states).all()
        assert np.isfinite(result.controls).all()
        assert result.stats["cpu_time_ii_s"] >= 0.0
        assert str(result.stats["ipopt_status"]).startswith("ipopt:")


def test_ours_stage1_reports_algorithm1_sets():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.planner import PlannerMethod, plan_scene
    from lian2023_strict.scenes import build_scene

    result = plan_scene(
        build_scene("fig5a"),
        method=PlannerMethod.OURS_EHA_IPOPT,
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(n_elements=30, max_iterations=1, ipopt_max_iterations=5),
        timeout_s=20.0,
    )

    assert float(result.stats["passage_groups"]) >= 1.0
    assert float(result.stats["swps_paths"]) + float(result.stats["snps_paths"]) == float(result.stats["passage_groups"])
    assert float(result.stats["xseq_paths"]) >= 1.0
    assert float(result.stats["xbou_points"]) == len(result.boundary_points)
    assert result.stats["stage1_fallback"] == "false"


def test_stage1_hybrid_astar_uses_plan_timeout(monkeypatch):
    from lian2023_strict import planner
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.planner import PlannerMethod, plan_scene
    from lian2023_strict.scenes import build_scene

    captured: dict[str, float] = {}
    scene = build_scene("fig5c")

    def fake_connect_boundary_points_with_hybrid_astar(**kwargs):
        captured["timeout_s"] = float(kwargs["timeout_s"])
        return kwargs["points"].copy()

    def fake_smooth_initial_guess(*args, **kwargs):
        states = np.asarray([scene.start, scene.goal], dtype=float)
        controls = np.zeros((1, 2), dtype=float)
        return states, controls, {
            "cpu_time_ii_s": 0.0,
            "ipopt_status": "ipopt:test",
            "jinf": 0.0,
            "jinf_ok": "True",
        }

    monkeypatch.setattr(planner, "connect_boundary_points_with_hybrid_astar", fake_connect_boundary_points_with_hybrid_astar)
    monkeypatch.setattr(planner, "smooth_initial_guess", fake_smooth_initial_guess)

    result = plan_scene(
        scene,
        method=PlannerMethod.OURS_EHA_IPOPT,
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(n_elements=2, max_iterations=1, ipopt_max_iterations=1),
        timeout_s=123.0,
    )

    assert captured["timeout_s"] == 123.0
    assert result.status == "success"


def test_ours_success_requires_paper_infeasibility_threshold():
    from lian2023_strict.config import load_algorithm_params, load_vehicle_params
    from lian2023_strict.planner import PlannerMethod, plan_scene
    from lian2023_strict.scenes import build_scene

    result = plan_scene(
        build_scene("fig5a"),
        method=PlannerMethod.OURS_EHA_IPOPT,
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(n_elements=10, max_iterations=1, ipopt_max_iterations=5, etol=0.0),
        timeout_s=20.0,
    )

    assert not result.success
    if len(result.states) > 0:
        assert result.status == "stage2_infeasible"
        assert float(result.stats["jinf"]) > 0.0
    else:
        assert result.status == "stage1_eha_fail"


def test_table2_runner_writes_csv_and_run_md(tmp_path):
    from lian2023_strict.scripts.run_table2 import run_table2

    out_dir = tmp_path / "table2"
    run_table2(out_dir=out_dir, n_elements=10, max_iterations=1, ipopt_max_iterations=3, timeout_s=10.0)

    rows = list(csv.DictReader((out_dir / "table2_local.csv").open()))
    assert {row["scene"] for row in rows} == {"fig5a", "fig5b", "fig5c", "fig5d"}
    assert {
        "astar_ipopt",
        "hybrid_astar_ipopt",
        "ftha_ipopt",
        "ours_eha_ipopt",
    }.issubset({row["method"] for row in rows})
    assert (out_dir / "RUN.md").is_file()
