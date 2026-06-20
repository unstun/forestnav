from __future__ import annotations

import math

import numpy as np
import pytest

from forest_n3p.features import (
    FeatureConfig,
    extract_features,
    ray_cast_distance,
    ring_occupancy_ratio,
)
from pathplan import GridMap


def _grid_map(data: np.ndarray, resolution: float = 1.0) -> GridMap:
    return GridMap(np.asarray(data, dtype=np.uint8), resolution=resolution, origin=(0.0, 0.0))


def test_target_relative_features_use_body_frame_and_angle_sincos() -> None:
    grid = _grid_map(np.zeros((12, 12), dtype=np.uint8))
    cfg = FeatureConfig(n_ray=4, r_max_m=8.0, density_rings_m=((0.0, 1.0),))

    result = extract_features(
        grid,
        current_pose=(0.0, 0.0, 0.0),
        goal_pose=(3.0, 4.0, math.pi / 2.0),
        config=cfg,
    )

    assert result.vector.shape == (5 + 4 + 1 + 1,)
    assert result.target_features == pytest.approx(
        (
            math.log1p(5.0),
            4.0 / 5.0,
            3.0 / 5.0,
            1.0,
            0.0,
        ),
        abs=1e-7,
    )


def test_ray_cast_distance_returns_first_occupied_cell_boundary() -> None:
    grid = np.zeros((9, 9), dtype=np.uint8)
    grid[4, 4] = 1

    distance = ray_cast_distance(
        _grid_map(grid),
        origin_xy=(1.0, 4.0),
        angle_rad=0.0,
        max_range_m=8.0,
    )

    assert distance == pytest.approx(2.5)


def test_ray_cast_distance_caps_at_known_map_boundary() -> None:
    grid = np.zeros((9, 9), dtype=np.uint8)

    distance = ray_cast_distance(
        _grid_map(grid),
        origin_xy=(1.0, 4.0),
        angle_rad=0.0,
        max_range_m=8.0,
    )

    assert distance == pytest.approx(7.5)


def test_ring_occupancy_ratio_counts_cell_centers_in_annulus() -> None:
    grid = np.zeros((5, 5), dtype=np.uint8)
    grid[2, 3] = 1
    grid[3, 2] = 1

    ratio = ring_occupancy_ratio(
        _grid_map(grid),
        center_xy=(2.0, 2.0),
        r_inner_m=0.0,
        r_outer_m=1.5,
    )

    assert ratio == pytest.approx(2.0 / 9.0)


def test_extract_features_uses_expected_41_dimensional_order() -> None:
    grid = np.zeros((40, 40), dtype=np.uint8)
    grid[20, 25] = 1
    cfg = FeatureConfig(
        n_ray=32,
        r_max_m=10.0,
        density_rings_m=((0.0, 2.0), (2.0, 5.0), (5.0, 10.0)),
        motion_flag_default=0.0,
    )

    result = extract_features(
        _grid_map(grid),
        current_pose=(20.0, 20.0, 0.0),
        goal_pose=(23.0, 24.0, math.pi / 2.0),
        config=cfg,
    )

    assert result.vector.shape == (41,)
    assert result.ray_distances_m.shape == (32,)
    assert result.density_ratios.shape == (3,)
    assert result.vector[:5] == pytest.approx(result.target_features)
    assert result.vector[5:37] == pytest.approx(np.log1p(result.ray_distances_m))
    assert result.vector[37:40] == pytest.approx(result.density_ratios)
    assert result.vector[40] == pytest.approx(0.0)
    assert result.ray_distances_m[0] == pytest.approx(4.5)
