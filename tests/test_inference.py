from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np
import pytest

import forest_n3p.inference as inference_module
from forest_n3p.inference import (
    FeatureMaskedKnnSubgoalLibrary,
    InferenceConfig,
    KnnSubgoalLibrary,
    NeighborPrediction,
    build_knn_library,
    compose_subgoal_pose,
    run_forest_n3p,
)
from pathplan import AckermannState, GridMap, TwoCircleFootprint


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


def test_feature_masked_knn_uses_selected_columns(tmp_path) -> None:
    dataset_dir = tmp_path / "dataset"
    features = np.asarray(
        [
            [0.0, 100.0, 0.0, 0.0],
            [10.0, -100.0, 10.0, 0.0],
        ],
        dtype=np.float32,
    )
    labels = np.asarray(
        [
            [1.0, 0.0, 0.0],
            [9.0, 0.0, 0.0],
        ],
        dtype=np.float32,
    )
    _write_dataset(dataset_dir, features, labels)

    library = FeatureMaskedKnnSubgoalLibrary.from_dataset(dataset_dir, feature_indices=(0, 2))
    prediction = library.query(np.asarray([9.0, 100.0, 9.0, 0.0], dtype=np.float32), current_pose=(0.0, 0.0, 0.0), k=1)[0]

    assert library.feature_dim == 2
    assert prediction.sample_index == 1
    assert prediction.delta_body == pytest.approx((9.0, 0.0, 0.0))


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


def test_verified_rs_segment_can_be_committed_without_segment_planner(monkeypatch) -> None:
    start = (1.0, 4.0, 0.0)
    subgoal = (3.0, 4.0, 0.0)
    goal = (6.0, 4.0, 0.0)

    class FixedPredictor:
        name = "knn"

        def query(self, feature, *, current_pose, k):  # noqa: ANN001, ANN201
            return (
                NeighborPrediction(
                    rank=1,
                    sample_index=0,
                    distance=0.0,
                    delta_body=(2.0, 0.0, 0.0),
                    subgoal_pose=subgoal,
                ),
            )

    def fake_try_rs(grid_map, footprint, rs_start, rs_goal, cfg):  # noqa: ANN001, ANN202
        start_key = tuple(round(float(v), 6) for v in rs_start)
        goal_key = tuple(round(float(v), 6) for v in rs_goal)
        if start_key == start and goal_key == goal:
            return None
        if (start_key, goal_key) in ((start, subgoal), (subgoal, goal)):
            return SimpleNamespace(
                samples=(
                    AckermannState(*rs_start),
                    AckermannState(*rs_goal),
                )
            )
        return None

    monkeypatch.setattr(inference_module, "_try_rs", fake_try_rs)

    result = run_forest_n3p(
        _empty_map(),
        _footprint(),
        start,
        goal,
        FixedPredictor(),
        config=InferenceConfig(commit_verified_rs_segments=True),
    )

    assert result.success
    assert result.failure_reason is None
    assert result.used_f2 == 0
    assert result.used_f3 == 0
    assert result.total_expansions == 0
    assert result.steps[0].mode == "knn_rs_verified_segment"
    assert result.steps[0].planner_expansions == 0
    assert result.steps[1].mode == "direct_rs_goal"
    assert len(result.path) == 3
    assert result.path[0] == pytest.approx(start)
    assert result.path[1] == pytest.approx(subgoal)
    assert result.path[2] == pytest.approx(goal)


def test_disabling_f1_limits_search_to_first_prediction(monkeypatch) -> None:
    start = (1.0, 4.0, 0.0)
    bad_subgoal = (2.0, 4.0, 0.0)
    good_subgoal = (3.0, 4.0, 0.0)
    goal = (6.0, 4.0, 0.0)

    class TwoNeighborPredictor:
        name = "knn"

        def query(self, feature, *, current_pose, k):  # noqa: ANN001, ANN201
            return (
                NeighborPrediction(1, 0, 0.0, (1.0, 0.0, 0.0), bad_subgoal),
                NeighborPrediction(2, 1, 0.1, (2.0, 0.0, 0.0), good_subgoal),
            )

    def fake_try_rs(grid_map, footprint, rs_start, rs_goal, cfg):  # noqa: ANN001, ANN202
        start_key = tuple(round(float(v), 6) for v in rs_start)
        goal_key = tuple(round(float(v), 6) for v in rs_goal)
        if (start_key, goal_key) in ((start, good_subgoal), (good_subgoal, goal)):
            return SimpleNamespace(samples=(AckermannState(*rs_start), AckermannState(*rs_goal)))
        return None

    monkeypatch.setattr(inference_module, "_try_rs", fake_try_rs)

    with_f1 = run_forest_n3p(
        _empty_map(),
        _footprint(),
        start,
        goal,
        TwoNeighborPredictor(),
        config=InferenceConfig(k_neighbors=2, commit_verified_rs_segments=True, enable_f2=False, enable_f3=False),
    )
    no_f1 = run_forest_n3p(
        _empty_map(),
        _footprint(),
        start,
        goal,
        TwoNeighborPredictor(),
        config=InferenceConfig(k_neighbors=2, enable_f1=False, enable_f2=False, enable_f3=False),
    )

    assert with_f1.success
    assert with_f1.used_f1 == 1
    assert not no_f1.success
    assert no_f1.failure_reason == "f2_disabled:no_reachable_prediction;f3_disabled"
