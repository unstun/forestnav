from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

from forest_n3p.rl_rs.actions import SteeringAction
from forest_n3p.rl_rs.env import AnalyticExpansionContext, AnalyticExpansionEnv
from forest_n3p.rl_rs.obs import RlRsObservation
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
    operator: str = "rl_rs_funnel"

    @property
    def failure_reason(self) -> str | None:
        record = self.rollout.to_record()
        return record.get("failure_reason") if isinstance(record.get("failure_reason"), str) else None

    def to_record(self) -> dict[str, Any]:
        rollout_record = self.rollout.to_record()
        return {
            "analytic_operator": self.operator,
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
    name: str = "rl_rs_funnel"
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
            step = env.step(self.action_policy(observation))
            rollout_states.append(step.next_state)
            rollout_actions.append(step.primitive)
            observation = step.observation
            if not (step.terminated or step.truncated):
                continue
            terminal_states: list[AckermannState] = []
            terminal_actions: list[MotionPrimitive] = []
            if step.terminal_rs.success:
                terminal = self._terminal_rs_segments(step.next_state, goal, context)
                if terminal is None:
                    telemetry = RlRsFunnelTelemetry(env.telemetry, terminal_rs_used=False, terminal_rs_action_count=0)
                    self.last_telemetry = telemetry
                    return None
                terminal_states, terminal_actions = terminal
                terminal_used = True
                terminal_action_count = len(terminal_actions)
            telemetry = RlRsFunnelTelemetry(
                env.telemetry,
                terminal_rs_used=terminal_used,
                terminal_rs_action_count=terminal_action_count,
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
