from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    PROJECT_ROOT
    / "2_experiment"
    / "idb_rrt_strict_repro"
    / "scripts"
    / "run_official_car1_smoke.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("run_official_car1_smoke", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_find_car1_motion_file_prefers_official_small5000_bundle(tmp_path):
    mod = _load_module()
    root = tmp_path / "dynoplan"
    small = root / "dynomotions" / "car1_v0_all.bin.sp.bin.small5000.msgpack"
    fallback = root / "dynobench" / "envs" / "car1_v0" / "motions" / "car1_v0_all.bin.sp.bin.small.msgpack"
    fallback.parent.mkdir(parents=True)
    fallback.write_bytes(b"fallback")
    small.parent.mkdir(parents=True)
    small.write_bytes(b"small5000")

    assert mod.find_car1_motion_file(root) == small


def test_build_idbastar_cfg_keeps_official_car1_search_defaults(tmp_path):
    mod = _load_module()
    motion_file = tmp_path / "car1_v0_all.bin.sp.bin.small5000.msgpack"
    motion_file.write_bytes(b"motion")

    cfg = mod.build_idbastar_cfg(motion_file=motion_file, timelimit_s=7.5, seed=11)

    assert cfg["motionsFile"] == str(motion_file)
    assert cfg["num_primitives_0"] == 400
    assert cfg["delta_0"] == 0.5
    assert cfg["max_motions_primitives"] == 20_000
    assert cfg["search_timelimit"] == 7500
    assert cfg["seed"] == 11


def test_parse_traj_solution_reads_xy_and_duration(tmp_path):
    mod = _load_module()
    traj_file = tmp_path / "result.yaml.traj-sol.yaml"
    traj_file.write_text(
        yaml.safe_dump(
            {
                "states": [
                    [0.7, 0.6, 0.0, 0.0],
                    [1.0, 0.4, 0.0, 0.0],
                    [1.9, 0.2, 0.0, 0.0],
                ],
                "times": [0.0, 0.4, 1.1],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    parsed = mod.parse_traj_solution(traj_file)

    assert parsed.xy == [(0.7, 0.6), (1.0, 0.4), (1.9, 0.2)]
    assert parsed.duration_s == 1.1
    assert parsed.state_count == 3


def test_parse_traj_solution_uses_official_cost_when_times_are_absent(tmp_path):
    mod = _load_module()
    traj_file = tmp_path / "idbastar_v0_solution_v0.yaml"
    traj_file.write_text(
        yaml.safe_dump(
            {
                "cost": 14.3,
                "states": [
                    [0.7, 0.6, 0.0, 0.0],
                    [1.0, 0.4, 0.0, 0.0],
                    [1.9, 0.2, 0.0, 0.0],
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    parsed = mod.parse_traj_solution(traj_file)

    assert parsed.duration_s == 14.3
    assert parsed.state_count == 3


def test_render_problem_plot_writes_png(tmp_path):
    mod = _load_module()
    env_file = tmp_path / "parallelpark_0.yaml"
    env_file.write_text(
        yaml.safe_dump(
            {
                "name": "car-parallel",
                "environment": {
                    "min": [0.0, -0.5],
                    "max": [3.5, 2.5],
                    "obstacles": [
                        {"type": "box", "center": [0.7, 0.2], "size": [0.5, 0.25]},
                        {"type": "box", "center": [2.7, 0.2], "size": [0.5, 0.25]},
                    ],
                },
                "robots": [
                    {
                        "type": "car1_v0",
                        "start": [0.7, 0.6, 0.0, 0.0],
                        "goal": [1.9, 0.2, 0.0, 0.0],
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    png_file = tmp_path / "plot.png"

    mod.render_problem_plot(
        env_file=env_file,
        xy=[(0.7, 0.6), (1.0, 0.4), (1.9, 0.2)],
        output_png=png_file,
        title="car1 parallelpark smoke",
    )

    assert png_file.is_file()
    assert png_file.stat().st_size > 1000
