from __future__ import annotations

from dataclasses import dataclass
import math

from .config import VehicleParams


def wrap_angle(angle: float) -> float:
    return (float(angle) + math.pi) % (2.0 * math.pi) - math.pi


def heading_diff(a: float, b: float) -> float:
    return wrap_angle(float(a) - float(b))


@dataclass(frozen=True)
class Pose:
    x: float
    y: float
    theta: float

    def as_tuple(self) -> tuple[float, float, float]:
        return float(self.x), float(self.y), float(self.theta)


@dataclass(frozen=True)
class MotionPrimitive:
    steering: float
    direction: int
    step_m: float


def propagate(pose: Pose, steering: float, direction: int, step_m: float, vehicle: VehicleParams) -> Pose:
    steering = max(-vehicle.max_steer_rad, min(vehicle.max_steer_rad, float(steering)))
    ds = float(step_m) * float(direction)
    kappa = math.tan(steering) / max(vehicle.wheelbase_m, 1e-9)
    if abs(kappa) < 1e-10:
        x = pose.x + ds * math.cos(pose.theta)
        y = pose.y + ds * math.sin(pose.theta)
        theta = wrap_angle(pose.theta)
    else:
        dtheta = ds * kappa
        x = pose.x + (math.sin(pose.theta + dtheta) - math.sin(pose.theta)) / kappa
        y = pose.y - (math.cos(pose.theta + dtheta) - math.cos(pose.theta)) / kappa
        theta = wrap_angle(pose.theta + dtheta)
    return Pose(float(x), float(y), float(theta))


def sample_constant_steer_motion(
    pose: Pose,
    steering: float,
    direction: int,
    step_m: float,
    vehicle: VehicleParams,
    *,
    sample_step_m: float,
) -> list[Pose]:
    total = abs(float(step_m))
    n = max(1, int(math.ceil(total / max(float(sample_step_m), 1e-6))))
    out: list[Pose] = []
    for i in range(n + 1):
        out.append(propagate(pose, steering, direction, total * (i / n), vehicle))
    return out


def default_primitives(vehicle: VehicleParams, step_m: float) -> list[MotionPrimitive]:
    s = float(vehicle.max_steer_rad)
    steering_values = (-s, -0.5 * s, 0.0, 0.5 * s, s)
    out: list[MotionPrimitive] = []
    for steering in steering_values:
        out.append(MotionPrimitive(steering, 1, float(step_m)))
    for steering in steering_values:
        out.append(MotionPrimitive(steering, -1, float(step_m)))
    return out
