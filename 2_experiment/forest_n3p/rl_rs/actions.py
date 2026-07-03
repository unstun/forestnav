from __future__ import annotations

import math
from dataclasses import dataclass

from forest_n3p.third_party.pathplan import AckermannParams
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive


@dataclass(frozen=True)
class SteeringAction:
    """RL-RS v1 动作: forward-only steering command."""

    steering_rad: float
    normalized: bool = False
    direction: int = 1


@dataclass(frozen=True)
class ActionConfig:
    """RL-RS action-space contract.

    v1 is deliberately forward-only. Reverse/direction-gated actions are a
    separate v2 decision and require C02 evidence before being enabled.
    """

    allow_reverse: bool = False
    primitive_weight: float = 1.0

    def __post_init__(self) -> None:
        if bool(self.allow_reverse):
            raise ValueError("RL-RS v1 action space is forward-only; reverse is not enabled.")
        if not (math.isfinite(float(self.primitive_weight)) and float(self.primitive_weight) > 0.0):
            raise ValueError("primitive_weight must be finite and positive")


@dataclass(frozen=True)
class ClippedSteeringAction:
    requested: float
    applied: float
    clipped: bool
    direction: int = 1


def decode_steering_action(action: SteeringAction | float, params: AckermannParams) -> SteeringAction:
    if isinstance(action, SteeringAction):
        requested = float(action.steering_rad)
        if not math.isfinite(requested):
            raise ValueError("steering action must be finite")
        if int(action.direction) != 1:
            raise ValueError("RL-RS v1 only supports forward direction=1")
        if bool(action.normalized):
            return SteeringAction(requested * float(params.max_steer), normalized=False, direction=1)
        return SteeringAction(requested, normalized=False, direction=1)
    requested = float(action)
    if not math.isfinite(requested):
        raise ValueError("steering action must be finite")
    return SteeringAction(requested, normalized=False, direction=1)


def clip_steering_action(action: SteeringAction | float, params: AckermannParams) -> ClippedSteeringAction:
    decoded = decode_steering_action(action, params)
    requested = float(decoded.steering_rad)
    max_steer = float(params.max_steer)
    applied = max(-max_steer, min(max_steer, requested))
    return ClippedSteeringAction(
        requested=requested,
        applied=applied,
        clipped=not math.isclose(requested, applied, rel_tol=0.0, abs_tol=1e-12),
        direction=1,
    )


def steering_action_to_primitive(
    action: SteeringAction | float,
    params: AckermannParams,
    *,
    step_m: float,
    config: ActionConfig | None = None,
) -> MotionPrimitive:
    cfg = config or ActionConfig()
    clipped = clip_steering_action(action, params)
    if int(clipped.direction) != 1:
        raise ValueError("RL-RS v1 only emits forward MotionPrimitive direction=1")
    if not (math.isfinite(float(step_m)) and float(step_m) > 0.0):
        raise ValueError("step_m must be finite and positive")
    return MotionPrimitive(
        steering=float(clipped.applied),
        direction=1,
        step=float(step_m),
        weight=float(cfg.primitive_weight),
    )
