from __future__ import annotations

import math
from dataclasses import dataclass

from forest_n3p.third_party.pathplan import AckermannParams


@dataclass(frozen=True)
class SteeringAction:
    """RL-RS v1 动作: forward-only steering command."""

    steering_rad: float


@dataclass(frozen=True)
class ClippedSteeringAction:
    requested: float
    applied: float
    clipped: bool


def clip_steering_action(action: SteeringAction | float, params: AckermannParams) -> ClippedSteeringAction:
    requested = float(action.steering_rad if isinstance(action, SteeringAction) else action)
    if not math.isfinite(requested):
        raise ValueError("steering action must be finite")
    max_steer = float(params.max_steer)
    applied = max(-max_steer, min(max_steer, requested))
    return ClippedSteeringAction(
        requested=requested,
        applied=applied,
        clipped=not math.isclose(requested, applied, rel_tol=0.0, abs_tol=1e-12),
    )
