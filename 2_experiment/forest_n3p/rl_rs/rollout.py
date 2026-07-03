from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from forest_n3p.rl_rs.actions import SteeringAction, clip_steering_action
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState
from forest_n3p.third_party.pathplan.robot import sample_constant_steer_motion


@dataclass(frozen=True)
class RolloutStepResult:
    next_state: AckermannState
    samples: tuple[AckermannState, ...]
    collided: bool
    requested_steering_rad: float
    applied_steering_rad: float
    action_clipped: bool
    sample_time_s: float
    collision_check_time_s: float


def rollout_constant_steer_step(
    *,
    state: AckermannState,
    action: SteeringAction | float,
    params: AckermannParams,
    checker: Any,
    action_step_m: float,
    collision_sample_step_m: float,
) -> RolloutStepResult:
    clipped = clip_steering_action(action, params)

    sample_start = time.perf_counter_ns()
    samples, _boxes = sample_constant_steer_motion(
        state,
        clipped.applied,
        1,
        float(action_step_m),
        params,
        step=float(collision_sample_step_m),
        footprint=None,
    )
    sample_time_s = _elapsed_s(sample_start)

    collision_start = time.perf_counter_ns()
    collided = bool(checker.collides_path(samples))
    collision_time_s = _elapsed_s(collision_start)

    return RolloutStepResult(
        next_state=samples[-1],
        samples=tuple(samples),
        collided=collided,
        requested_steering_rad=clipped.requested,
        applied_steering_rad=clipped.applied,
        action_clipped=clipped.clipped,
        sample_time_s=sample_time_s,
        collision_check_time_s=collision_time_s,
    )


def _elapsed_s(start_ns: int) -> float:
    return float(time.perf_counter_ns() - start_ns) / 1_000_000_000.0
