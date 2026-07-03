from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from forest_n3p.rl_rs.actions import SteeringAction
from forest_n3p.rl_rs.obs import RlRsObservation, build_observation
from forest_n3p.rl_rs.reward import RewardBreakdown, pending_reward_breakdown
from forest_n3p.rl_rs.rollout import rollout_constant_steer_step
from forest_n3p.rl_rs.telemetry import RlRsEpisodeTelemetry, RlRsStepTelemetry
from forest_n3p.rl_rs.terminal import TerminalRsCheckResult, check_terminal_rs_connectable
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class AnalyticExpansionContext:
    grid_map: GridMap
    footprint: TwoCircleFootprint
    start: AckermannState
    goal: AckermannState
    params: AckermannParams = field(default_factory=AckermannParams)
    checker: Any | None = None
    max_steps: int = 32
    action_step_m: float = 0.3
    collision_sample_step_m: float = 0.1
    terminal_check_every: int = 1
    theta_bins: int = 72
    collision_padding_m: float | None = None

    def __post_init__(self) -> None:
        if int(self.max_steps) <= 0:
            raise ValueError("max_steps must be positive")
        for name in ("action_step_m", "collision_sample_step_m"):
            value = float(getattr(self, name))
            if not (math.isfinite(value) and value > 0.0):
                raise ValueError(f"{name} must be finite and positive")
        if int(self.terminal_check_every) <= 0:
            raise ValueError("terminal_check_every must be positive")

    def collision_checker(self):
        return self.checker or GridFootprintChecker(
            self.grid_map,
            self.footprint,
            theta_bins=int(self.theta_bins),
            padding=self.collision_padding_m,
        )


@dataclass(frozen=True)
class AnalyticExpansionStep:
    observation: RlRsObservation
    reward: RewardBreakdown
    terminated: bool
    truncated: bool
    telemetry: RlRsStepTelemetry
    terminal_rs: TerminalRsCheckResult

    @property
    def info(self) -> dict[str, object]:
        return {
            "telemetry": self.telemetry,
            "terminal_rs": self.terminal_rs,
            "reward_status": "pending_e02",
        }


class AnalyticExpansionEnv:
    """Planner-side RL-RS analytic expansion environment surface."""

    def __init__(self) -> None:
        self._context: AnalyticExpansionContext | None = None
        self._checker = None
        self._state: AckermannState | None = None
        self._steps: list[RlRsStepTelemetry] = []

    @property
    def telemetry(self) -> RlRsEpisodeTelemetry:
        return RlRsEpisodeTelemetry(steps=tuple(self._steps))

    def reset(self, context: AnalyticExpansionContext) -> RlRsObservation:
        self._context = context
        self._checker = context.collision_checker()
        self._state = context.start
        self._steps = []
        return build_observation(context.start, context.goal, remaining_steps=int(context.max_steps))

    def step(self, action: SteeringAction | float) -> AnalyticExpansionStep:
        if self._context is None or self._state is None or self._checker is None:
            raise RuntimeError("AnalyticExpansionEnv.reset() must be called before step().")
        context = self._context
        step_index = len(self._steps)
        rollout = rollout_constant_steer_step(
            state=self._state,
            action=action,
            params=context.params,
            checker=self._checker,
            action_step_m=float(context.action_step_m),
            collision_sample_step_m=float(context.collision_sample_step_m),
        )
        self._state = rollout.next_state
        should_check_terminal = (step_index + 1) % int(context.terminal_check_every) == 0
        terminal = (
            check_terminal_rs_connectable(
                grid_map=context.grid_map,
                footprint=context.footprint,
                state=rollout.next_state,
                goal=context.goal,
                turning_radius_m=float(context.params.min_turn_radius),
                wheelbase_m=float(context.params.wheelbase),
                sample_step_m=float(context.collision_sample_step_m),
                theta_bins=int(context.theta_bins),
                collision_padding_m=context.collision_padding_m,
                checker=self._checker,
            )
            if should_check_terminal and not rollout.collided
            else TerminalRsCheckResult(False, 0.0, None, 0, None)
        )
        terminated = bool(rollout.collided or terminal.success)
        truncated = bool(not terminated and (step_index + 1) >= int(context.max_steps))
        failure_reason = None
        if rollout.collided:
            failure_reason = "collision"
        elif truncated:
            failure_reason = "budget_exhausted"
        elif terminal.failure_reason is not None:
            failure_reason = terminal.failure_reason

        telemetry = RlRsStepTelemetry(
            step_index=step_index,
            requested_steering_rad=rollout.requested_steering_rad,
            applied_steering_rad=rollout.applied_steering_rad,
            action_clipped=rollout.action_clipped,
            sample_count=len(rollout.samples),
            sample_time_s=rollout.sample_time_s,
            collision_check_time_s=rollout.collision_check_time_s,
            terminal_rs_time_s=terminal.time_s,
            collided=rollout.collided,
            terminal_rs_success=terminal.success,
            failure_reason=failure_reason,
        )
        self._steps.append(telemetry)
        observation = build_observation(
            rollout.next_state,
            context.goal,
            remaining_steps=max(0, int(context.max_steps) - (step_index + 1)),
        )
        return AnalyticExpansionStep(
            observation=observation,
            reward=pending_reward_breakdown(),
            terminated=terminated,
            truncated=truncated,
            telemetry=telemetry,
            terminal_rs=terminal,
        )
