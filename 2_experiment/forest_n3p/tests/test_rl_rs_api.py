import math
from dataclasses import replace

import numpy as np
import pytest

from forest_n3p.rl_rs import (
    ActionConfig,
    AnalyticExpansionContext,
    AnalyticExpansionEnv,
    ObservationConfig,
    RewardConfig,
    RewardTermSwitches,
    SteeringAction,
    build_egocentric_edt_patch,
    build_egocentric_occupancy_patch,
    build_patch_observation,
    clip_steering_action,
    rollout_constant_steer_step,
    steering_action_to_primitive,
)
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker
from forest_n3p.third_party.pathplan.robot import propagate


def _empty_context(goal=(2.0, 1.0, 0.0), *, max_steps=4, terminal_check_every=1, no_progress_patience=3):
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
        max_steps=max_steps,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
        terminal_check_every=terminal_check_every,
        observation_config=ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True, edt_clip_m=1.0),
        no_progress_patience=no_progress_patience,
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
    assert result.primitive.direction == 1


def test_rollout_step_matches_planner_propagate_for_curved_action():
    context = _empty_context()
    result = rollout_constant_steer_step(
        state=context.start,
        action=SteeringAction(0.2),
        params=context.params,
        checker=context.collision_checker(),
        action_step_m=context.action_step_m,
        collision_sample_step_m=context.collision_sample_step_m,
    )
    expected = propagate(
        context.start,
        result.applied_steering_rad,
        result.primitive.direction,
        context.action_step_m,
        context.params,
    )

    assert not result.collided
    assert math.isclose(result.next_state.x, expected.x, abs_tol=1e-12)
    assert math.isclose(result.next_state.y, expected.y, abs_tol=1e-12)
    assert math.isclose(result.next_state.theta, expected.theta, abs_tol=1e-12)
    assert math.isclose(result.samples[-1].x, expected.x, abs_tol=1e-12)
    assert math.isclose(result.samples[-1].y, expected.y, abs_tol=1e-12)
    assert math.isclose(result.samples[-1].theta, expected.theta, abs_tol=1e-12)


def test_env_reset_step_returns_telemetry_and_reward_marker():
    env = AnalyticExpansionEnv()
    obs = env.reset(_empty_context(goal=(3.0, 1.0, 0.0), terminal_check_every=10))

    assert len(obs.scalar) == 8
    assert obs.patch.shape == (2, 5, 5)
    step = env.step(0.0)

    assert step.reward.total == 0.0
    assert step.reward.success == 0.0
    assert step.info["reward_status"] == "e02_3_reward_ablation_hooks"
    assert step.info["reward_total"] == step.reward.total
    assert step.info["reward_ablation"]["success"]
    assert step.info["reward_ablation"]["progress"]
    assert step.info["reward_terms"]["progress"] == step.reward.progress
    assert step.info["reward_terms"]["rs_progress"] == step.reward.rs_progress
    assert step.info["reward_terms"]["clearance"] == step.reward.clearance
    assert step.info["reward_terms"]["curvature"] == step.reward.curvature
    assert step.info["reward_terms"]["path_length"] == step.reward.path_length
    assert step.info["reward_terms"]["step"] == step.reward.step
    assert step.info["terminated"] == step.terminated
    assert step.info["truncated"] == step.truncated
    assert step.info["failure_reason"] == step.telemetry.failure_reason
    assert step.info["no_progress_count"] == step.telemetry.no_progress_count
    assert step.telemetry.sample_count == 4
    assert step.telemetry.primitive_direction == 1
    assert env.telemetry.rollout_steps == 1
    assert env.telemetry.rollout_collision_checks == 4


def test_action_config_is_forward_only_and_rejects_reverse_gate():
    with pytest.raises(ValueError, match="forward-only"):
        ActionConfig(allow_reverse=True)

    context = _empty_context()
    with pytest.raises(ValueError, match="forward direction"):
        clip_steering_action(SteeringAction(0.0, direction=-1), context.params)


def test_normalized_steering_action_decodes_and_converts_to_primitive():
    context = _empty_context()
    action = SteeringAction(0.5, normalized=True)

    clipped = clip_steering_action(action, context.params)
    primitive = steering_action_to_primitive(action, context.params, step_m=context.action_step_m)

    assert math.isclose(clipped.applied, 0.5 * context.params.max_steer, abs_tol=1e-12)
    assert primitive.direction == 1
    assert math.isclose(primitive.step, context.action_step_m, abs_tol=1e-12)
    assert math.isclose(primitive.steering, clipped.applied, abs_tol=1e-12)


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
    assert step.reward.collision == -1.0
    assert step.reward.total == -1.0
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
    assert step.telemetry.goal_distance_m > 0.0
    assert step.reward.success == 1.0
    assert step.reward.total == 1.0


def test_reward_config_controls_terminal_rs_success_reward():
    env = AnalyticExpansionEnv()
    context = _empty_context(goal=(1.6, 1.0, 0.0))
    context = replace(context, reward_config=RewardConfig(terminal_rs_success=2.5))
    env.reset(context)

    step = env.step(0.0)

    assert step.terminal_rs.success
    assert step.reward.success == 2.5
    assert step.reward.total == 2.5


def test_reward_breakdown_records_configured_shaping_terms():
    env = AnalyticExpansionEnv()
    context = replace(
        _empty_context(goal=(1.6, 1.0, 0.0)),
        reward_config=RewardConfig(
            terminal_rs_success=0.0,
            collision_penalty=0.0,
            terminal_rs_failure_penalty=0.0,
            no_progress_penalty=0.0,
            distance_progress_scale=1.0,
            rs_distance_progress_scale=1.0,
            clearance_scale=1.0,
            clearance_target_m=0.5,
            curvature_rate_penalty_scale=1.0,
            path_length_penalty_scale=1.0,
            step_penalty=-0.1,
        ),
    )
    env.reset(context)

    step = env.step(SteeringAction(0.1))
    terms = step.info["reward_terms"]

    assert step.reward.progress > 0.0
    assert step.reward.rs_progress > 0.0
    assert step.reward.clearance >= 0.0
    assert step.reward.curvature < 0.0
    assert step.reward.path_length < 0.0
    assert step.reward.step == -0.1
    assert terms["total"] == step.reward.total
    assert terms["success"] == 0.0
    assert terms["terminal"] == 0.0


def test_reward_ablation_switches_disable_selected_terms():
    env = AnalyticExpansionEnv()
    context = replace(
        _empty_context(goal=(1.6, 1.0, 0.0)),
        reward_config=RewardConfig(
            enabled_terms=RewardTermSwitches(
                success=False,
                progress=False,
                rs_progress=False,
                clearance=False,
                curvature=False,
                path_length=False,
            ),
            terminal_rs_success=3.0,
            collision_penalty=0.0,
            terminal_rs_failure_penalty=0.0,
            no_progress_penalty=0.0,
            distance_progress_scale=1.0,
            rs_distance_progress_scale=1.0,
            clearance_scale=1.0,
            curvature_rate_penalty_scale=1.0,
            path_length_penalty_scale=1.0,
            step_penalty=-0.1,
        ),
    )
    env.reset(context)

    step = env.step(SteeringAction(0.1))
    ablation = step.info["reward_ablation"]

    assert step.terminal_rs.success
    assert step.telemetry.progress_to_goal_m > 0.0
    assert not ablation["success"]
    assert not ablation["progress"]
    assert not ablation["rs_progress"]
    assert not ablation["clearance"]
    assert not ablation["curvature"]
    assert not ablation["path_length"]
    assert ablation["step"]
    assert step.reward.success == 0.0
    assert step.reward.progress == 0.0
    assert step.reward.rs_progress == 0.0
    assert step.reward.clearance == 0.0
    assert step.reward.curvature == 0.0
    assert step.reward.path_length == 0.0
    assert step.reward.step == -0.1
    assert step.reward.total == -0.1


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
    assert step.reward.terminal == -0.25
    assert step.reward.total == -0.25


def test_env_step_truncates_on_no_progress_before_budget_exhausted():
    env = AnalyticExpansionEnv()
    env.reset(
        _empty_context(
            goal=(0.0, 1.0, math.pi),
            max_steps=5,
            terminal_check_every=10,
            no_progress_patience=2,
        )
    )

    first = env.step(0.0)
    second = env.step(0.0)

    assert not first.terminated
    assert not first.truncated
    assert second.truncated
    assert second.telemetry.failure_reason == "no_progress"
    assert second.telemetry.no_progress_count == 2
    assert second.telemetry.progress_to_goal_m < 0.0
    assert second.reward.terminal == -0.25


def test_egocentric_occupancy_patch_aligns_obstacle_in_robot_frame():
    config = ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=False)
    data_east = np.zeros((40, 40), dtype=np.uint8)
    data_east[10, 12] = 1
    east_map = GridMap(data_east, resolution=0.1, origin=(0.0, 0.0))

    data_north = np.zeros((40, 40), dtype=np.uint8)
    data_north[12, 10] = 1
    north_map = GridMap(data_north, resolution=0.1, origin=(0.0, 0.0))

    east_patch = build_egocentric_occupancy_patch(east_map, AckermannState(1.0, 1.0, 0.0), config)
    north_patch = build_egocentric_occupancy_patch(north_map, AckermannState(1.0, 1.0, math.pi / 2.0), config)

    assert east_patch[2, 4] == 1.0
    assert north_patch[2, 4] == 1.0
    np.testing.assert_array_equal(east_patch, north_patch)


def test_egocentric_patch_marks_out_of_bounds_as_occupied():
    config = ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=False)
    grid_map = GridMap(np.zeros((10, 10), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))

    patch = build_egocentric_occupancy_patch(grid_map, AckermannState(0.0, 0.0, 0.0), config)

    assert patch[0, 0] == 1.0
    assert patch[2, 2] == 0.0


def test_patch_observation_stacks_occupancy_and_normalized_edt_channels():
    config = ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True, edt_clip_m=1.0)
    data = np.zeros((40, 40), dtype=np.uint8)
    data[10, 12] = 1
    grid_map = GridMap(data, resolution=0.1, origin=(0.0, 0.0))

    patch = build_patch_observation(grid_map, AckermannState(1.0, 1.0, 0.0), config)
    edt = build_egocentric_edt_patch(grid_map, AckermannState(1.0, 1.0, 0.0), config)

    assert patch.shape == (2, 5, 5)
    assert patch.dtype == np.float32
    assert patch[0, 2, 4] == 1.0
    assert patch[1, 2, 4] == 0.0
    assert edt[2, 2] > edt[2, 4]
