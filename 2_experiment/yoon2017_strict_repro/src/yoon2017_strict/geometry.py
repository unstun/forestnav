from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Pose:
    x: float
    y: float
    theta: float

    def as_tuple(self) -> tuple[float, float, float]:
        return float(self.x), float(self.y), float(self.theta)


def wrap_angle(angle: float) -> float:
    return (float(angle) + math.pi) % (2.0 * math.pi) - math.pi


def heading_diff(a: float, b: float) -> float:
    return wrap_angle(float(a) - float(b))
