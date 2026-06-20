from __future__ import annotations

import math

import numpy as np
import pytest

from forest_n3p.inference import (
    InferenceConfig,
    KnnSubgoalLibrary,
    build_knn_library,
    compose_subgoal_pose,
    run_forest_n3p,
)
from pathplan import GridMap, TwoCircleFootprint


def _empty_map(width: int = 120, height: int = 80, resolution: float = 0.1) -> GridMap:
    return GridMap(np.zeros((height, width), dtype=np.uint8), resolution=resolution, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def _write_dataset(root, features: np.ndarray, labels: np.ndarray) -> None:
    root.mkdir(parents=True, exist_ok=True)
    np.save(root / "features.npy", features.astype(np.float32))
    np.save(root / "labels.npy", labels.astype(np.float32))
    np.save(root / "sample_query_indices.npy", np.arange(features.shape[0], dtype=np.int64))


def test_compose_subgoal_pose_uses_body_frame_delta() -> None:
    pose = compose_subgoal_pose((1.0, 2.0, math.pi / 2.0), (3.0, -2.0, math.pi / 4.0))

    assert pose == pytest.approx((3.0, 5.0, 3.0 * math.pi / 4.0))


def test_build_knn_library_applies_zscore_and_returns_nearest_label(tmp_path) -> None:
    dataset_dir = tmp_path / "dataset"
    library_dir = tmp_path / "library"
    features = np.asarray(
        [
            [1.0, 10.0, 0.0],
            [2.0, 10.0, 0.0],
            [9.0, 30.0, 0.0],
        ],
        dtype=np.float32,
    )
    labels = np.asarray(
        [
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [9.0, 0.0, 0.0],
        ],
        dtype=np.float32,
    )
    _write_dataset(dataset_dir, features, labels)

    build_knn_library(dataset_dir, library_dir, source_head="unit-test", command="unit-test")
    library = KnnSubgoalLibrary.load(library_dir)
    prediction = library.query(features[1], current_pose=(0.0, 0.0, 0.0), k=1)[0]

    assert library.feature_dim == 3
    assert library.sample_count == 3
    assert np.all(library.feature_std > 0.0)
    assert prediction.sample_index == 1
    assert prediction.delta_body == pytest.approx((2.0, 0.0, 0.0))
    assert prediction.subgoal_pose == pytest.approx((2.0, 0.0, 0.0))


def test_direct_rs_goal_short_circuits_before_knn_segment(tmp_path) -> None:
    dataset_dir = tmp_path / "dataset"
    library_dir = tmp_path / "library"
    _write_dataset(
        dataset_dir,
        np.zeros((1, 41), dtype=np.float32),
        np.asarray([[1.0, 0.0, 0.0]], dtype=np.float32),
    )
    build_knn_library(dataset_dir, library_dir, source_head="unit-test", command="unit-test")
    library = KnnSubgoalLibrary.load(library_dir)

    result = run_forest_n3p(
        _empty_map(),
        _footprint(),
        (1.0, 4.0, 0.0),
        (7.0, 4.0, 0.0),
        library,
        config=InferenceConfig(rs_sample_step_m=0.1),
    )

    assert result.success
    assert result.failure_reason is None
    assert result.termination_reason == "direct_rs_goal"
    assert result.used_f1 == 0
    assert result.used_f2 == 0
    assert result.used_f3 == 0
    assert len(result.path) > 2
    assert result.path[-1] == pytest.approx((7.0, 4.0, 0.0))
