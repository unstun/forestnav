from __future__ import annotations

import ast
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_paper_reported_simulation_vehicle_and_algorithm_params():
    from yoon2017_strict.config import paper_algorithm_params, paper_sim_vehicle_params

    vehicle = paper_sim_vehicle_params()
    params = paper_algorithm_params()

    assert math.isclose(vehicle.front_overhang_m, 3.4)
    assert math.isclose(vehicle.rear_overhang_m, 0.8)
    assert math.isclose(vehicle.width_m, 1.8)
    assert math.isclose(vehicle.min_turn_radius_m, 4.8)
    assert math.isclose(vehicle.length_m, 4.2)

    assert math.isclose(params.steer_step_m, 5.0)
    assert math.isclose(params.goal_region_radius_m, 2.0)


def test_unreported_rrt_star_params_are_explicit_implementation_defaults():
    from yoon2017_strict.config import paper_algorithm_params

    params = paper_algorithm_params()

    assert math.isclose(params.neighbor_radius_m, 5.0)
    assert math.isclose(params.goal_sample_rate, 0.05)
    assert params.samples_per_segment == 24


def test_paper_table_targets_are_reference_values_not_acceptance_thresholds():
    from yoon2017_strict.config import paper_reference_values

    refs = paper_reference_values()

    assert refs["fig8"]["ss_rrt_star_n8000_cost_m"] == 56.1
    assert refs["fig9"]["narrow_passage_width_m"] == 3.7
    assert refs["fig9"]["ss_rrt_star_cost_m"] == 37.5
    assert refs["fig10"]["rectangle_sampling_corner_spacing_m"] == 0.1


def test_strict_package_does_not_import_ugv_dqn_or_project_baselines():
    package_dir = SRC / "yoon2017_strict"
    assert package_dir.is_dir()
    forbidden_terms = (
        "ugv_dqn",
        "spline_rrt_star",
        "benchmark_baselines",
        "realmap",
    )
    violations: list[str] = []
    for path in sorted(package_dir.rglob("*.py")):
        src = path.read_text(encoding="utf-8")
        for term in forbidden_terms:
            if term in src:
                violations.append(f"{path}:{term}")
        tree = ast.parse(src, filename=str(path))
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


def test_package_metadata_lists_runtime_dependencies():
    pyproject = ROOT / "pyproject.toml"
    assert pyproject.is_file()
    text = pyproject.read_text(encoding="utf-8")
    for dep in ("numpy", "scipy", "matplotlib", "pytest"):
        assert dep in text
