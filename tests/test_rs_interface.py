from __future__ import annotations

import math

import numpy as np

from forest_n3p.rs_utils import (
    check_reeds_shepp_collision,
    generate_reeds_shepp_path,
    sample_reeds_shepp_path,
)
from forest_n3p.third_party.pathplan.hybrid_a_star.reeds_shepp import reeds_shepp_shortest_path
from pathplan import GridMap, TwoCircleFootprint


def _simple_map(*, blocked: bool) -> GridMap:
    grid = np.zeros((80, 100), dtype=np.uint8)
    if blocked:
        grid[20:61, 40] = 1
    return GridMap(grid, resolution=0.1, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def test_reeds_shepp_generation_samples_to_goal() -> None:
    start = (1.0, 4.0, 0.0)
    goal = (7.0, 4.0, 0.0)
    path = generate_reeds_shepp_path(start, goal, turning_radius=1.0)
    samples = sample_reeds_shepp_path(start, path, turning_radius=1.0, sample_step=0.1)

    assert path.total_length > 0.0
    assert len(samples) > 2
    assert math.isclose(samples[0].x, start[0], abs_tol=1e-9)
    assert math.isclose(samples[0].y, start[1], abs_tol=1e-9)
    assert math.isclose(samples[-1].x, goal[0], abs_tol=1e-6)
    assert math.isclose(samples[-1].y, goal[1], abs_tol=1e-6)
    assert math.isclose(samples[-1].theta, goal[2], abs_tol=1e-6)


def test_reeds_shepp_handles_near_zero_translation() -> None:
    path = reeds_shepp_shortest_path((0.0, 0.0, 0.0), (1e-6, 0.0, 0.0), 1.0)

    assert path is not None
    assert math.isclose(path.total_length, 1e-6, rel_tol=1e-6, abs_tol=1e-9)


def test_reeds_shepp_collision_free_on_empty_map() -> None:
    result = check_reeds_shepp_collision(
        _simple_map(blocked=False),
        _footprint(),
        (1.0, 4.0, 0.0),
        (7.0, 4.0, 0.0),
        turning_radius=1.0,
        sample_step=0.1,
    )

    assert result.collision_free
    assert result.samples


def test_reeds_shepp_collision_detects_blocking_obstacle() -> None:
    result = check_reeds_shepp_collision(
        _simple_map(blocked=True),
        _footprint(),
        (1.0, 4.0, 0.0),
        (7.0, 4.0, 0.0),
        turning_radius=1.0,
        sample_step=0.1,
    )

    assert not result.collision_free


if __name__ == "__main__":
    test_reeds_shepp_generation_samples_to_goal()
    test_reeds_shepp_collision_free_on_empty_map()
    test_reeds_shepp_collision_detects_blocking_obstacle()
    print("RS interface OK")
