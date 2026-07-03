from __future__ import annotations

import math
from dataclasses import dataclass

from forest_n3p.features import wrap_pi
from forest_n3p.third_party.pathplan import AckermannState


@dataclass(frozen=True)
class ObservationConfig:
    patch_size_m: float = 6.4
    patch_cells: int = 64
    include_edt: bool = True


@dataclass(frozen=True)
class RlRsObservation:
    state: AckermannState
    goal: AckermannState
    scalar: tuple[float, ...]


def build_scalar_observation(state: AckermannState, goal: AckermannState, *, remaining_steps: int) -> tuple[float, ...]:
    dx = float(goal.x - state.x)
    dy = float(goal.y - state.y)
    distance = math.hypot(dx, dy)
    bearing = math.atan2(dy, dx)
    heading_error = wrap_pi(float(goal.theta - state.theta))
    bearing_error = wrap_pi(bearing - float(state.theta))
    return (
        dx,
        dy,
        distance,
        math.sin(heading_error),
        math.cos(heading_error),
        math.sin(bearing_error),
        math.cos(bearing_error),
        float(remaining_steps),
    )


def build_observation(state: AckermannState, goal: AckermannState, *, remaining_steps: int) -> RlRsObservation:
    return RlRsObservation(
        state=state,
        goal=goal,
        scalar=build_scalar_observation(state, goal, remaining_steps=int(remaining_steps)),
    )
