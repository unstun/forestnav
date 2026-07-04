from __future__ import annotations

import math
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

from forest_n3p.rl_rs.actions import SteeringAction
from forest_n3p.rl_rs.env import AnalyticExpansionContext, AnalyticExpansionEnv
from forest_n3p.rl_rs.obs import ObservationConfig, RlRsObservation
from forest_n3p.rl_rs.telemetry import RlRsEpisodeTelemetry
from forest_n3p.third_party.pathplan import AckermannState
from forest_n3p.third_party.pathplan.hybrid_a_star import AnalyticExpansionResult
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive

RlRsActionPolicy = Callable[[RlRsObservation], SteeringAction | float]


@dataclass(frozen=True)
class RlRsFunnelTelemetry:
    rollout: RlRsEpisodeTelemetry
    terminal_rs_used: bool
    terminal_rs_action_count: int
    rl_success: bool = False
    operator: str = "rl_rs_funnel"
    rollout_protocol: str = "constant_steer_grid_footprint_terminal_rs"
    collision_checker: str | None = None
    rollout_max_steps: int | None = None
    rollout_action_step_m: float | None = None
    rollout_collision_sample_step_m: float | None = None
    terminal_success_mode: str | None = None

    @property
    def failure_reason(self) -> str | None:
        record = self.rollout.to_record()
        return record.get("failure_reason") if isinstance(record.get("failure_reason"), str) else None

    def to_record(self) -> dict[str, Any]:
        rollout_record = self.rollout.to_record()
        return {
            "analytic_operator": self.operator,
            "rl_attempts": 1,
            "rl_successes": 1 if bool(self.rl_success) else 0,
            "rs_attempts": int(rollout_record.get("terminal_rs_check_count", 0) or 0),
            "nn_forward_time_s": float(rollout_record.get("nn_forward_time_s", 0.0) or 0.0),
            "fallback_to_primitives_count": 0 if bool(self.rl_success) else 1,
            "rollout_protocol": self.rollout_protocol,
            "collision_checker": self.collision_checker,
            "rollout_max_steps": self.rollout_max_steps,
            "rollout_action_step_m": self.rollout_action_step_m,
            "rollout_collision_sample_step_m": self.rollout_collision_sample_step_m,
            "terminal_success_mode": self.terminal_success_mode,
            "rl_rollout_steps": int(rollout_record.get("rollout_steps", 0) or 0),
            "rl_rollout_collision_checks": int(rollout_record.get("rollout_collision_checks", 0) or 0),
            "rl_rollout_sample_time_s": float(rollout_record.get("rollout_sample_time_s", 0.0) or 0.0),
            "rl_rollout_collision_time_s": float(rollout_record.get("rollout_collision_time_s", 0.0) or 0.0),
            "terminal_rs_time_s": float(rollout_record.get("terminal_rs_time_s", 0.0) or 0.0),
            "terminal_rs_success": bool(rollout_record.get("terminal_rs_success", False)),
            "terminal_rs_used": bool(self.terminal_rs_used),
            "terminal_rs_action_count": int(self.terminal_rs_action_count),
            "failure_reason": self.failure_reason,
        }


@dataclass
class RlRsFunnelOperator:
    action_policy: RlRsActionPolicy
    max_steps: int = 32
    action_step_m: float = 0.3
    collision_sample_step_m: float | None = None
    terminal_check_every: int = 1
    no_progress_patience: int = 3
    observation_config: ObservationConfig = ObservationConfig()
    append_terminal_rs: bool = True
    name: str = "rl_rs_funnel"
    checkpoint_path: str | None = None
    checkpoint_sha256: str | None = None
    last_telemetry: RlRsFunnelTelemetry | None = None

    def try_connect(
        self,
        state: AckermannState,
        goal: AckermannState,
        context: Any,
    ) -> Optional[AnalyticExpansionResult]:
        env_context = self._env_context(state, goal, context)
        env = AnalyticExpansionEnv()
        observation = env.reset(env_context)
        rollout_states: list[AckermannState] = []
        rollout_actions: list[MotionPrimitive] = []
        terminal_used = False
        terminal_action_count = 0

        while True:
            policy_started_at = time.perf_counter()
            action = self.action_policy(observation)
            policy_elapsed = time.perf_counter() - policy_started_at
            step = env.step(action, nn_forward_time_s=policy_elapsed)
            rollout_states.append(step.next_state)
            rollout_actions.append(step.primitive)
            observation = step.observation
            if not (step.terminated or step.truncated):
                continue
            if not bool(self.append_terminal_rs):
                telemetry = RlRsFunnelTelemetry(
                    env.telemetry,
                    terminal_rs_used=False,
                    terminal_rs_action_count=0,
                    rl_success=bool(step.terminated and not step.telemetry.collided and step.goal_tolerance_reached),
                    operator=self.name,
                    **self._telemetry_protocol_fields(env_context),
                )
                self.last_telemetry = telemetry
                if step.terminated and not step.telemetry.collided and step.goal_tolerance_reached:
                    return AnalyticExpansionResult(
                        states=rollout_states,
                        actions=rollout_actions,
                        telemetry=telemetry,
                        terminal_rs_used=False,
                        operator=self.name,
                    )
                return None
            terminal_states: list[AckermannState] = []
            terminal_actions: list[MotionPrimitive] = []
            if step.terminal_rs.success:
                terminal = self._terminal_rs_segments(step.next_state, goal, context)
                if terminal is None:
                    telemetry = RlRsFunnelTelemetry(
                        env.telemetry,
                        terminal_rs_used=False,
                        terminal_rs_action_count=0,
                        rl_success=False,
                        operator=self.name,
                        **self._telemetry_protocol_fields(env_context),
                    )
                    self.last_telemetry = telemetry
                    return None
                terminal_states, terminal_actions = terminal
                terminal_used = True
                terminal_action_count = len(terminal_actions)
            telemetry = RlRsFunnelTelemetry(
                env.telemetry,
                terminal_rs_used=terminal_used,
                terminal_rs_action_count=terminal_action_count,
                rl_success=bool(terminal_used),
                operator=self.name,
                **self._telemetry_protocol_fields(env_context),
            )
            self.last_telemetry = telemetry
            if not terminal_used:
                return None
            return AnalyticExpansionResult(
                states=rollout_states + terminal_states,
                actions=rollout_actions + terminal_actions,
                telemetry=telemetry,
                terminal_rs_used=True,
                operator=self.name,
            )

    def _env_context(self, state: AckermannState, goal: AckermannState, context: Any) -> AnalyticExpansionContext:
        return AnalyticExpansionContext(
            grid_map=context.map,
            footprint=context.footprint,
            start=state,
            goal=goal,
            params=context.params,
            checker=context.collision_checker,
            max_steps=int(self.max_steps),
            action_step_m=float(self.action_step_m),
            collision_sample_step_m=float(self.collision_sample_step_m or context.collision_step),
            terminal_check_every=int(self.terminal_check_every),
            theta_bins=int(context.theta_bins),
            no_progress_patience=int(self.no_progress_patience),
            observation_config=self.observation_config,
            terminal_success_mode="terminal_rs" if bool(self.append_terminal_rs) else "goal_tolerance",
            goal_xy_tolerance_m=float(getattr(context, "goal_xy_tol", 0.30)),
            goal_theta_tolerance_rad=float(getattr(context, "goal_theta_tol", math.radians(15.0))),
        )

    def _terminal_rs_segments(
        self,
        state: AckermannState,
        goal: AckermannState,
        context: Any,
    ) -> tuple[list[AckermannState], list[MotionPrimitive]] | None:
        result, _telemetry = context._try_rs_with_radius(state, goal, float(context.params.min_turn_radius))
        if result is None:
            return None
        return list(result.endpoints), list(result.actions)

    @staticmethod
    def _telemetry_protocol_fields(context: AnalyticExpansionContext) -> dict[str, Any]:
        checker = context.collision_checker()
        return {
            "collision_checker": type(checker).__name__,
            "rollout_max_steps": int(context.max_steps),
            "rollout_action_step_m": float(context.action_step_m),
            "rollout_collision_sample_step_m": float(context.collision_sample_step_m),
            "terminal_success_mode": str(context.terminal_success_mode),
        }
