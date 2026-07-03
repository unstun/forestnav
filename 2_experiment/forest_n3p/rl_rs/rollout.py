from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from forest_n3p.rl_rs.actions import ActionConfig, SteeringAction, steering_action_to_primitive
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive
from forest_n3p.third_party.pathplan.robot import sample_constant_steer_motion


@dataclass(frozen=True)
class RolloutStepResult:
    next_state: AckermannState
    samples: tuple[AckermannState, ...]
    collided: bool
    requested_steering_rad: float
    applied_steering_rad: float
    primitive: MotionPrimitive
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
    action_config: ActionConfig | None = None,
) -> RolloutStepResult:
    primitive = steering_action_to_primitive(action, params, step_m=float(action_step_m), config=action_config)
    requested = action.steering_rad if isinstance(action, SteeringAction) else float(action)
    if isinstance(action, SteeringAction) and action.normalized:
        requested = float(action.steering_rad) * float(params.max_steer)

    sample_start = time.perf_counter_ns()
    samples, _boxes = sample_constant_steer_motion(
        state,
        primitive.steering,
        primitive.direction,
        primitive.step,
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
        requested_steering_rad=float(requested),
        applied_steering_rad=float(primitive.steering),
        primitive=primitive,
        action_clipped=not math.isclose(float(requested), float(primitive.steering), rel_tol=0.0, abs_tol=1e-12),
        sample_time_s=sample_time_s,
        collision_check_time_s=collision_time_s,
    )


def _elapsed_s(start_ns: int) -> float:
    return float(time.perf_counter_ns() - start_ns) / 1_000_000_000.0
