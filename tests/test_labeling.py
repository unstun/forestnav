from __future__ import annotations

import math

import numpy as np
import pytest

from forest_n3p.features import FeatureConfig
from forest_n3p.labeling import (
    LabelingConfig,
    body_relative_pose,
    extract_subgoal_labels,
)
from pathplan import GridMap, TwoCircleFootprint


def _empty_map(width: int = 120, height: int = 40, resolution: float = 0.1) -> GridMap:
    return GridMap(np.zeros((height, width), dtype=np.uint8), resolution=resolution, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def _cfg(*, l_max: float, l_min: float) -> LabelingConfig:
    return LabelingConfig(
        l_max_m=l_max,
        l_min_m=l_min,
        turning_radius_m=1.0,
        wheelbase_m=0.6,
        rs_sample_step_m=0.1,
        theta_bins=72,
        feature_config=FeatureConfig(n_ray=4, r_max_m=6.0, density_rings_m=((0.0, 1.0),)),
    )


def test_body_relative_pose_uses_current_body_frame() -> None:
    delta = body_relative_pose((1.0, 2.0, math.pi / 2.0), (3.0, 5.0, math.pi))

    assert delta == pytest.approx((3.0, -2.0, math.pi / 2.0))


def test_direct_reeds_shepp_goal_produces_no_intermediate_samples() -> None:
    path = [(1.0, 2.0, 0.0), (3.0, 2.0, 0.0)]

    result = extract_subgoal_labels(
        _empty_map(),
        _footprint(),
        path,
        config=_cfg(l_max=3.0, l_min=0.5),
    )

    assert result.success
    assert result.failure_reason is None
    assert result.subgoals == ()
    assert result.samples == ()


def test_forward_greedy_selects_farthest_reachable_subgoal_and_features() -> None:
    path = [(1.0 + float(i), 2.0, 0.0) for i in range(7)]

    result = extract_subgoal_labels(
        _empty_map(width=160),
        _footprint(),
        path,
        config=_cfg(l_max=3.0, l_min=1.0),
    )

    assert result.success
    assert len(result.samples) == 1
    assert len(result.subgoals) == 1
    assert result.subgoals[0] == pytest.approx((4.0, 2.0, 0.0))

    sample = result.samples[0]
    assert sample.current_pose == pytest.approx((1.0, 2.0, 0.0))
    assert sample.subgoal_pose == pytest.approx((4.0, 2.0, 0.0))
    assert sample.delta_body == pytest.approx((3.0, 0.0, 0.0))
    assert sample.s_start_m == pytest.approx(0.0)
    assert sample.s_subgoal_m == pytest.approx(3.0)
    assert sample.rs_length_m <= 3.0 + 1e-9
    assert sample.feature_vector.shape == (11,)


def test_short_progress_discards_entire_teacher_path() -> None:
    path = [
        (1.0, 2.0, 0.0),
        (1.5, 2.0, 0.0),
        (2.0, 2.0, 0.0),
        (3.0, 2.0, 0.0),
    ]

    result = extract_subgoal_labels(
        _empty_map(),
        _footprint(),
        path,
        config=_cfg(l_max=0.6, l_min=1.0),
    )

    assert not result.success
    assert result.failure_reason == "short_progress"
    assert result.subgoals == ()
    assert result.samples == ()
