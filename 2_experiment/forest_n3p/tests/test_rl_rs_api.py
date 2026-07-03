import math

import numpy as np
import pytest

from forest_n3p.rl_rs import AnalyticExpansionContext, AnalyticExpansionEnv, SteeringAction, rollout_constant_steer_step
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


def _empty_context(goal=(2.0, 1.0, 0.0)):
    grid_map = GridMap(np.zeros((60, 60), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)
    params = AckermannParams(wheelbase=0.5, min_turn_radius=1.0)
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=32)
    return AnalyticExpansionContext(
        grid_map=grid_map,
        footprint=footprint,
        start=AckermannState(1.0, 1.0, 0.0),
        goal=AckermannState(*goal),
        params=params,
        checker=checker,
        max_steps=4,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
        theta_bins=32,
    )


def _context_with_grid(data, *, goal=(2.0, 1.0, 0.0), max_steps=4):
    grid_map = GridMap(np.asarray(data, dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)
    params = AckermannParams(wheelbase=0.5, min_turn_radius=1.0)
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=32)
    return AnalyticExpansionContext(
        grid_map=grid_map,
        footprint=footprint,
        start=AckermannState(1.0, 1.0, 0.0),
        goal=AckermannState(*goal),
        params=params,
        checker=checker,
        max_steps=max_steps,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
        theta_bins=32,
    )


def test_rollout_step_uses_ackermann_sampling_and_checker():
    context = _empty_context()
    result = rollout_constant_steer_step(
        state=context.start,
        action=SteeringAction(0.0),
        params=context.params,
        checker=context.collision_checker(),
        action_step_m=context.action_step_m,
        collision_sample_step_m=context.collision_sample_step_m,
    )

    assert not result.collided
    assert len(result.samples) == 4
    assert math.isclose(result.next_state.x, 1.3, abs_tol=1e-9)
    assert math.isclose(result.next_state.y, 1.0, abs_tol=1e-9)


def test_env_reset_step_returns_telemetry_and_pending_reward_marker():
    env = AnalyticExpansionEnv()
    obs = env.reset(_empty_context(goal=(3.0, 1.0, 0.0)))

    assert len(obs.scalar) == 8
    step = env.step(0.0)

    assert step.reward.total == 0.0
    assert step.info["reward_status"] == "pending_e02"
    assert step.info["terminated"] == step.terminated
    assert step.info["truncated"] == step.truncated
    assert step.info["failure_reason"] == step.telemetry.failure_reason
    assert step.telemetry.sample_count == 4
    assert env.telemetry.rollout_steps == 1
    assert env.telemetry.rollout_collision_checks == 4


def test_env_step_before_reset_raises():
    env = AnalyticExpansionEnv()

    with pytest.raises(RuntimeError, match="reset"):
        env.step(0.0)


def test_env_reset_rejects_colliding_start_state():
    data = np.zeros((60, 60), dtype=np.uint8)
    data[10, 10] = 1
    env = AnalyticExpansionEnv()

    with pytest.raises(ValueError, match="start state is in collision"):
        env.reset(_context_with_grid(data))


def test_env_step_terminates_on_rollout_collision_and_blocks_followup_step():
    data = np.zeros((60, 60), dtype=np.uint8)
    data[10, 13] = 1
    env = AnalyticExpansionEnv()
    env.reset(_context_with_grid(data, goal=(3.0, 1.0, 0.0)))

    step = env.step(0.0)

    assert step.terminated
    assert not step.truncated
    assert step.telemetry.collided
    assert step.telemetry.failure_reason == "collision"
    with pytest.raises(RuntimeError, match="episode is done"):
        env.step(0.0)


def test_env_step_terminates_on_terminal_rs_success():
    env = AnalyticExpansionEnv()
    env.reset(_empty_context(goal=(1.6, 1.0, 0.0)))

    step = env.step(0.0)

    assert step.terminated
    assert not step.truncated
    assert step.terminal_rs.success
    assert step.telemetry.terminal_rs_success
    assert step.telemetry.failure_reason is None


def test_env_step_truncates_with_no_terminal_rs_when_budget_exhausted():
    data = np.zeros((60, 60), dtype=np.uint8)
    data[10, 30] = 1
    env = AnalyticExpansionEnv()
    env.reset(_context_with_grid(data, goal=(3.0, 1.0, 0.0), max_steps=1))

    step = env.step(0.0)

    assert not step.terminated
    assert step.truncated
    assert not step.terminal_rs.success
    assert step.telemetry.failure_reason.startswith("no_rs_terminal:")
