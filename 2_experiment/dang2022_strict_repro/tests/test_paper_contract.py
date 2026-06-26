from __future__ import annotations

import ast
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_paper_reported_params_match_dang2022_section_4_1_and_4_2():
    from dang2022_strict.config import paper_algorithm_params, paper_vehicle_params

    vehicle = paper_vehicle_params()
    params = paper_algorithm_params()

    assert math.isclose(vehicle.length_m, 4.3)
    assert math.isclose(vehicle.width_m, 2.0)
    assert math.isclose(vehicle.wheelbase_m, 3.0)
    assert math.isclose(vehicle.max_steer_rad, 0.6)
    assert math.isclose(vehicle.max_curvature, math.tan(0.6) / 3.0)
    assert math.isclose(vehicle.min_turn_radius_m, 1.0 / vehicle.max_curvature)

    assert math.isclose(params.curvature_resolution, 0.05)
    assert math.isclose(params.motion_primitive_m, 1.5)


def test_unreported_cost_params_are_explicit_implementation_defaults():
    from dang2022_strict.config import paper_algorithm_params

    params = paper_algorithm_params()

    assert math.isclose(params.sigma1, 1.0)
    assert math.isclose(params.sigma2, 1.0)
    assert math.isclose(params.movement_weight_length, 1.0)
    assert math.isclose(params.movement_weight_steering, 1.0)
    assert math.isclose(params.movement_weight_switch, 1.0)
    assert math.isclose(params.voronoi_alpha, 5.0)
    assert math.isclose(params.voronoi_d_o_max, 5.0)


def test_table_targets_are_recorded_as_reference_not_acceptance_thresholds():
    from dang2022_strict.config import paper_table1_targets, paper_table2_targets

    table1 = paper_table1_targets()
    table2 = paper_table2_targets()

    assert table1["map_a"]["original"]["curvature"] == 0.23
    assert table1["map_a"]["improved"]["curvature"] == 0.15
    assert table1["map_b"]["improved"]["cost"] == 5.52
    assert table2["map12"]["turning_before"] == 13
    assert table2["den520d"]["improved"]["time_s"] == 0.140
    assert table2["ost003d"]["turning_after"] == 6


def test_strict_package_does_not_import_ugv_dqn_or_project_baselines():
    package_dir = SRC / "dang2022_strict"
    assert package_dir.is_dir()
    forbidden_terms = (
        "ugv_dqn",
        "improved_hybrid_astar",
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
