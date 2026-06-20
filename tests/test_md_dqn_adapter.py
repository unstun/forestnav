from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from forest_n3p.baselines.md_dqn_adapter import (
    MdDqnAdapterConfig,
    check_md_dqn_adapter,
    poses_from_md_dqn_cells,
    poses_from_md_dqn_rollout,
)
from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.main_evaluation import MainEvaluationConfig, preflight_main_evaluation
from forest_n3p.third_party.pathplan import GridMap


def test_md_dqn_adapter_reports_missing_source_dir() -> None:
    availability = check_md_dqn_adapter(MdDqnAdapterConfig())

    assert not availability.available
    assert availability.reason is not None
    assert "md_dqn_source_dir is not set" in availability.reason


def test_md_dqn_adapter_normalizes_repo_root_source_dir(tmp_path: Path) -> None:
    repo_root = tmp_path / "DQN10"
    source_dir = repo_root / "2_experiment"
    (source_dir / "ugv_dqn" / "cli").mkdir(parents=True)
    (source_dir / "ugv_dqn" / "cli" / "infer.py").write_text("# test\n", encoding="utf-8")
    checkpoint = tmp_path / "model.pt"
    checkpoint.write_bytes(b"not-a-real-checkpoint")

    availability = check_md_dqn_adapter(
        MdDqnAdapterConfig(source_dir=repo_root, checkpoint_path=checkpoint)
    )

    assert availability.available
    assert availability.source_dir == source_dir.resolve()
    assert availability.checkpoint_path == checkpoint.resolve()


def test_md_dqn_cell_path_conversion_uses_grid_resolution_and_heading() -> None:
    grid_map = GridMap(data=[[0, 0, 0], [0, 0, 0]], resolution=0.5, origin=(10.0, -2.0))

    poses = poses_from_md_dqn_cells(((0.0, 0.0), (2.0, 0.0), (2.0, 1.0)), grid_map)

    assert poses[0] == pytest.approx((10.0, -2.0, 0.0))
    assert poses[1] == pytest.approx((11.0, -2.0, 1.57079632679))
    assert poses[2] == pytest.approx((11.0, -1.5, 1.57079632679))


def test_md_dqn_trace_conversion_prefers_metric_pose_trace() -> None:
    grid_map = GridMap(data=[[0]], resolution=0.1, origin=(3.0, 4.0))
    rollout = SimpleNamespace(
        trace_rows=[
            {"x_m": 1.0, "y_m": 2.0, "theta_rad": 0.25},
            {"x_m": 1.5, "y_m": 2.5, "theta_rad": 0.50},
        ],
        path_xy_cells=((0.0, 0.0),),
    )

    poses = poses_from_md_dqn_rollout(rollout, grid_map)

    assert len(poses) == 2
    assert poses[0] == pytest.approx((4.0, 6.0, 0.25))
    assert poses[1] == pytest.approx((4.5, 6.5, 0.50))


def test_main_evaluation_preflight_accepts_registered_md_dqn_adapter(tmp_path: Path) -> None:
    repo_root = tmp_path / "DQN10"
    source_dir = repo_root / "2_experiment"
    (source_dir / "ugv_dqn" / "cli").mkdir(parents=True)
    (source_dir / "ugv_dqn" / "cli" / "infer.py").write_text("# test\n", encoding="utf-8")
    checkpoint = tmp_path / "model.pt"
    checkpoint.write_bytes(b"not-a-real-checkpoint")
    contract_path = tmp_path / "contract.md"
    contract_path.write_text("---\nstatus: approved\n---\n", encoding="utf-8")
    cutpoint_path = tmp_path / "cutpoints.md"
    cutpoint_path.write_text("---\nreviewed: true\n---\n", encoding="utf-8")

    report = preflight_main_evaluation(
        MainEvaluationConfig(
            queries_per_bucket=1,
            seed_count=1,
            methods=("md_dqn",),
            distance_bins=parse_distance_bins("4:8"),
            contract_path=contract_path,
            cutpoint_supplement_path=cutpoint_path,
            md_dqn_source_dir=repo_root,
            md_dqn_checkpoint_path=checkpoint,
            enforce_t14_scale=False,
        )
    )

    assert report.ok_to_run
    assert report.available_methods == ("md_dqn",)
    assert report.unavailable_methods == {}
