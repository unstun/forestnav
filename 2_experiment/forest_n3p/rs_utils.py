"""Independent Reeds-Shepp generation and collision-checking helpers.

T02 exists because the vendored `pathplan` package exposes the low-level
Reeds-Shepp solver and the grid footprint checker separately. The F-N3P label
and inference code needs one small, explicit seam:

    SE(2) start/goal -> Reeds-Shepp curve -> sampled poses -> collision check

This module keeps that seam thin and delegates all planning math to pathplan.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, TypeAlias

from .third_party.pathplan.geometry import Footprint, GridFootprintChecker
from .third_party.pathplan.hybrid_a_star.reeds_shepp import (
    ReedsSheppPath,
    reeds_shepp_shortest_path,
)
from .third_party.pathplan.robot import AckermannParams, AckermannState, sample_constant_steer_motion

PoseLike: TypeAlias = tuple[float, float, float] | AckermannState


@dataclass(frozen=True)
class ReedsSheppCheck:
    """Result of an independent Reeds-Shepp collision check."""

    path: ReedsSheppPath
    samples: tuple[AckermannState, ...]
    collision_free: bool


def _as_state(pose: PoseLike) -> AckermannState:
    if isinstance(pose, AckermannState):
        return pose
    x, y, theta = pose
    return AckermannState(float(x), float(y), float(theta))


def generate_reeds_shepp_path(
    start: PoseLike,
    goal: PoseLike,
    *,
    turning_radius: float,
) -> ReedsSheppPath:
    """Generate the shortest Reeds-Shepp curve between two SE(2) poses."""
    start_state = _as_state(start)
    goal_state = _as_state(goal)
    path = reeds_shepp_shortest_path(
        start_state.as_tuple(),
        goal_state.as_tuple(),
        float(turning_radius),
    )
    if path is None:
        raise RuntimeError("No Reeds-Shepp candidate path was generated.")
    return path


def sample_reeds_shepp_path(
    start: PoseLike,
    path: ReedsSheppPath,
    *,
    turning_radius: float,
    wheelbase: float = 0.6,
    sample_step: float = 0.05,
) -> tuple[AckermannState, ...]:
    """Sample poses along a Reeds-Shepp curve using the bicycle model."""
    if not math.isfinite(turning_radius) or float(turning_radius) <= 0.0:
        raise ValueError("turning_radius must be finite and > 0.")
    if not math.isfinite(wheelbase) or float(wheelbase) <= 0.0:
        raise ValueError("wheelbase must be finite and > 0.")
    if not math.isfinite(sample_step) or float(sample_step) <= 0.0:
        raise ValueError("sample_step must be finite and > 0.")

    params = AckermannParams(wheelbase=float(wheelbase), min_turn_radius=float(turning_radius))
    max_steer = math.atan(float(wheelbase) / float(turning_radius))
    cur = _as_state(start)
    samples: list[AckermannState] = [cur]

    for segment_type, signed_length in zip(path.segment_types, path.segment_lengths):
        seg_len = float(signed_length)
        if abs(seg_len) <= 1e-9:
            continue
        direction = 1 if seg_len >= 0.0 else -1
        if segment_type == "S":
            steering = 0.0
        elif segment_type == "L":
            steering = max_steer
        elif segment_type == "R":
            steering = -max_steer
        else:
            raise ValueError(f"Unknown Reeds-Shepp segment type: {segment_type!r}")

        segment_samples, _ = sample_constant_steer_motion(
            cur,
            steering,
            direction,
            abs(seg_len),
            params,
            step=float(sample_step),
            footprint=None,
        )
        samples.extend(segment_samples[1:])
        cur = segment_samples[-1]

    return tuple(samples)


def check_reeds_shepp_collision(
    grid_map,
    footprint: Footprint,
    start: PoseLike,
    goal: PoseLike,
    *,
    turning_radius: float,
    wheelbase: float = 0.6,
    sample_step: float = 0.05,
    theta_bins: int = 72,
    collision_padding: float | None = None,
) -> ReedsSheppCheck:
    """Generate and collision-check a Reeds-Shepp curve on an occupancy grid."""
    path = generate_reeds_shepp_path(start, goal, turning_radius=float(turning_radius))
    samples = sample_reeds_shepp_path(
        start,
        path,
        turning_radius=float(turning_radius),
        wheelbase=float(wheelbase),
        sample_step=float(sample_step),
    )
    checker = GridFootprintChecker(
        grid_map,
        footprint,
        theta_bins=int(theta_bins),
        padding=collision_padding,
    )
    return ReedsSheppCheck(
        path=path,
        samples=samples,
        collision_free=not checker.collides_path(samples),
    )


def is_reeds_shepp_collision_free(
    grid_map,
    footprint: Footprint,
    start: PoseLike,
    goal: PoseLike,
    **kwargs,
) -> bool:
    """Return only the collision-free flag for callers that do not need samples."""
    return check_reeds_shepp_collision(grid_map, footprint, start, goal, **kwargs).collision_free


def states_as_tuples(states: Iterable[AckermannState]) -> tuple[tuple[float, float, float], ...]:
    """Convert sampled AckermannState objects to plain SE(2) tuples."""
    return tuple(state.as_tuple() for state in states)
