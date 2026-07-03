from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RlRsStepTelemetry:
    step_index: int
    requested_steering_rad: float
    applied_steering_rad: float
    primitive_direction: int
    action_clipped: bool
    sample_count: int
    sample_time_s: float
    collision_check_time_s: float
    terminal_rs_time_s: float
    collided: bool
    terminal_rs_success: bool
    failure_reason: str | None


@dataclass(frozen=True)
class RlRsEpisodeTelemetry:
    steps: tuple[RlRsStepTelemetry, ...]

    @property
    def nn_forward_time_s(self) -> float:
        return 0.0

    @property
    def rollout_collision_time_s(self) -> float:
        return float(sum(step.collision_check_time_s for step in self.steps))

    @property
    def rollout_sample_time_s(self) -> float:
        return float(sum(step.sample_time_s for step in self.steps))

    @property
    def terminal_rs_time_s(self) -> float:
        return float(sum(step.terminal_rs_time_s for step in self.steps))

    @property
    def rollout_steps(self) -> int:
        return int(len(self.steps))

    @property
    def rollout_collision_checks(self) -> int:
        return int(sum(step.sample_count for step in self.steps))

    def to_record(self) -> dict[str, float | int | bool | str | None]:
        last = self.steps[-1] if self.steps else None
        return {
            "nn_forward_time_s": self.nn_forward_time_s,
            "rollout_sample_time_s": self.rollout_sample_time_s,
            "rollout_collision_time_s": self.rollout_collision_time_s,
            "terminal_rs_time_s": self.terminal_rs_time_s,
            "rollout_steps": self.rollout_steps,
            "rollout_collision_checks": self.rollout_collision_checks,
            "collided": bool(last.collided) if last is not None else False,
            "terminal_rs_success": bool(last.terminal_rs_success) if last is not None else False,
            "failure_reason": None if last is None else last.failure_reason,
        }
