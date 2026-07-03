from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from forest_n3p.rs_utils import generate_reeds_shepp_path
from forest_n3p.rl_rs.actions import ActionConfig, SteeringAction
from forest_n3p.rl_rs.obs import ObservationConfig, RlRsObservation, build_observation
from forest_n3p.rl_rs.reward import (
    RewardBreakdown,
    RewardConfig,
    build_clearance_distance_field,
    compute_decomposed_reward,
    min_rollout_clearance_m,
)
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
    observation_config: ObservationConfig = field(default_factory=ObservationConfig)
    action_config: ActionConfig = field(default_factory=ActionConfig)
    reward_config: RewardConfig = field(default_factory=RewardConfig)
    min_progress_m: float = 1e-3
    no_progress_patience: int = 3

    def __post_init__(self) -> None:
        _validate_state("start", self.start)
        _validate_state("goal", self.goal)
        if int(self.max_steps) <= 0:
            raise ValueError("max_steps must be positive")
        for name in ("action_step_m", "collision_sample_step_m"):
            value = float(getattr(self, name))
            if not (math.isfinite(value) and value > 0.0):
                raise ValueError(f"{name} must be finite and positive")
        if int(self.terminal_check_every) <= 0:
            raise ValueError("terminal_check_every must be positive")
        if float(self.min_progress_m) < 0.0:
            raise ValueError("min_progress_m must be non-negative")
        if int(self.no_progress_patience) < 0:
            raise ValueError("no_progress_patience must be non-negative")

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
            "reward_status": self.reward.status,
            "reward_total": self.reward.total,
            "reward_terms": self.reward.to_record(),
            "terminated": bool(self.terminated),
            "truncated": bool(self.truncated),
            "failure_reason": self.telemetry.failure_reason,
            "goal_distance_m": self.telemetry.goal_distance_m,
            "progress_to_goal_m": self.telemetry.progress_to_goal_m,
            "no_progress_count": self.telemetry.no_progress_count,
        }


class AnalyticExpansionEnv:
    """Planner-side RL-RS analytic expansion environment surface."""

    def __init__(self) -> None:
        self._context: AnalyticExpansionContext | None = None
        self._checker = None
        self._state: AckermannState | None = None
        self._steps: list[RlRsStepTelemetry] = []
        self._done = False
        self._last_goal_distance_m: float | None = None
        self._last_terminal_rs_path_length_m: float | None = None
        self._last_curvature: float = 0.0
        self._no_progress_count = 0
        self._clearance_field_m = None

    @property
    def telemetry(self) -> RlRsEpisodeTelemetry:
        return RlRsEpisodeTelemetry(steps=tuple(self._steps))

    def reset(self, context: AnalyticExpansionContext) -> RlRsObservation:
        self._context = context
        self._checker = context.collision_checker()
        if _collides_pose(self._checker, context.start):
            raise ValueError("AnalyticExpansionContext start state is in collision.")
        self._state = context.start
        self._steps = []
        self._done = False
        self._last_goal_distance_m = _distance_to_goal(context.start, context.goal)
        self._last_terminal_rs_path_length_m = _estimate_rs_path_length(context.start, context.goal, context.params)
        self._last_curvature = 0.0
        self._no_progress_count = 0
        self._clearance_field_m = build_clearance_distance_field(context.grid_map)
        return build_observation(
            context.start,
            context.goal,
            remaining_steps=int(context.max_steps),
            grid_map=context.grid_map,
            config=context.observation_config,
        )

    def step(self, action: SteeringAction | float) -> AnalyticExpansionStep:
        if self._context is None or self._state is None or self._checker is None:
            raise RuntimeError("AnalyticExpansionEnv.reset() must be called before step().")
        if self._done:
            raise RuntimeError("AnalyticExpansionEnv episode is done; call reset() before step().")
        context = self._context
        step_index = len(self._steps)
        previous_goal_distance = (
            _distance_to_goal(self._state, context.goal)
            if self._last_goal_distance_m is None
            else float(self._last_goal_distance_m)
        )
        rollout = rollout_constant_steer_step(
            state=self._state,
            action=action,
            params=context.params,
            checker=self._checker,
            action_step_m=float(context.action_step_m),
            collision_sample_step_m=float(context.collision_sample_step_m),
            action_config=context.action_config,
        )
        self._state = rollout.next_state
        goal_distance = _distance_to_goal(rollout.next_state, context.goal)
        progress_to_goal = previous_goal_distance - goal_distance
        if progress_to_goal < float(context.min_progress_m):
            self._no_progress_count += 1
        else:
            self._no_progress_count = 0
        self._last_goal_distance_m = goal_distance
        budget_exhausted = (step_index + 1) >= int(context.max_steps)
        should_check_terminal = budget_exhausted or (step_index + 1) % int(context.terminal_check_every) == 0
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
        current_rs_path_length_m = terminal.path_length_m
        rs_distance_progress_m = (
            float(self._last_terminal_rs_path_length_m) - float(current_rs_path_length_m)
            if self._last_terminal_rs_path_length_m is not None and current_rs_path_length_m is not None
            else None
        )
        terminated = bool(rollout.collided or terminal.success)
        no_progress = (
            int(context.no_progress_patience) > 0
            and self._no_progress_count >= int(context.no_progress_patience)
        )
        truncated = bool(not terminated and (budget_exhausted or no_progress))
        failure_reason = None
        if rollout.collided:
            failure_reason = "collision"
        elif no_progress and truncated:
            failure_reason = "no_progress"
        elif truncated:
            detail = terminal.failure_reason or "terminal_rs_not_checked"
            failure_reason = f"no_rs_terminal:{detail}"
        rollout_path_length_m = _path_length(rollout.samples)
        min_clearance_m = min_rollout_clearance_m(
            rollout.samples,
            grid_map=context.grid_map,
            footprint=context.footprint,
            clearance_field_m=self._clearance_field_m,
            padding_m=0.0 if context.collision_padding_m is None else float(context.collision_padding_m),
        )
        curvature = math.tan(float(rollout.applied_steering_rad)) / float(context.params.wheelbase)
        curvature_delta_abs = abs(curvature - float(self._last_curvature))

        telemetry = RlRsStepTelemetry(
            step_index=step_index,
            requested_steering_rad=rollout.requested_steering_rad,
            applied_steering_rad=rollout.applied_steering_rad,
            primitive_direction=int(rollout.primitive.direction),
            action_clipped=rollout.action_clipped,
            sample_count=len(rollout.samples),
            goal_distance_m=goal_distance,
            progress_to_goal_m=progress_to_goal,
            no_progress_count=int(self._no_progress_count),
            sample_time_s=rollout.sample_time_s,
            collision_check_time_s=rollout.collision_check_time_s,
            terminal_rs_time_s=terminal.time_s,
            collided=rollout.collided,
            terminal_rs_success=terminal.success,
            failure_reason=failure_reason,
        )
        self._steps.append(telemetry)
        self._done = bool(terminated or truncated)
        if current_rs_path_length_m is not None:
            self._last_terminal_rs_path_length_m = float(current_rs_path_length_m)
        self._last_curvature = float(curvature)
        observation = build_observation(
            rollout.next_state,
            context.goal,
            remaining_steps=max(0, int(context.max_steps) - (step_index + 1)),
            grid_map=context.grid_map,
            config=context.observation_config,
        )
        return AnalyticExpansionStep(
            observation=observation,
            reward=compute_decomposed_reward(
                terminal_rs=terminal,
                collided=rollout.collided,
                failure_reason=failure_reason,
                progress_to_goal_m=progress_to_goal,
                rs_distance_progress_m=rs_distance_progress_m,
                min_clearance_m=min_clearance_m,
                curvature_delta_abs=curvature_delta_abs,
                rollout_path_length_m=rollout_path_length_m,
                config=context.reward_config,
            ),
            terminated=terminated,
            truncated=truncated,
            telemetry=telemetry,
            terminal_rs=terminal,
        )


def _validate_state(name: str, state: AckermannState) -> None:
    for field_name, value in (("x", state.x), ("y", state.y), ("theta", state.theta)):
        if not math.isfinite(float(value)):
            raise ValueError(f"{name}.{field_name} must be finite")


def _collides_pose(checker, state: AckermannState) -> bool:
    if hasattr(checker, "collides_pose"):
        return bool(checker.collides_pose(state.x, state.y, state.theta))
    return bool(checker.collides_path((state,)))


def _distance_to_goal(state: AckermannState, goal: AckermannState) -> float:
    return float(math.hypot(float(goal.x) - float(state.x), float(goal.y) - float(state.y)))


def _estimate_rs_path_length(state: AckermannState, goal: AckermannState, params: AckermannParams) -> float | None:
    try:
        path = generate_reeds_shepp_path(state, goal, turning_radius=float(params.min_turn_radius))
    except Exception:  # noqa: BLE001 - reward shaping must not make reset fail.
        return None
    return float(path.total_length)


def _path_length(samples: tuple[AckermannState, ...]) -> float:
    total = 0.0
    for start, end in zip(samples[:-1], samples[1:]):
        total += math.hypot(float(end.x) - float(start.x), float(end.y) - float(start.y))
    return float(total)
