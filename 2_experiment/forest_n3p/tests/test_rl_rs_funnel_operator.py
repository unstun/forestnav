import numpy as np

from forest_n3p.rl_rs import SteeringAction
from forest_n3p.rl_rs.operator import RlRsFunnelOperator
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, HybridAStarPlanner, TwoCircleFootprint
from forest_n3p.third_party.pathplan.hybrid_a_star import AnalyticExpansionOperator, AnalyticExpansionResult


def _planner(*, blocked=False):
    data = np.zeros((80, 80), dtype=np.uint8)
    if blocked:
        data[8:13, 14:17] = 1
    grid_map = GridMap(data, resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)
    return HybridAStarPlanner(
        grid_map,
        footprint,
        AckermannParams(wheelbase=0.5, min_turn_radius=1.0),
        analytic_operator="disabled",
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=0.30,
        theta_bins=16,
    )


def test_rl_rs_funnel_operator_rolls_out_then_appends_terminal_rs_success():
    operator = RlRsFunnelOperator(
        action_policy=lambda _obs: SteeringAction(0.0),
        max_steps=4,
        action_step_m=0.3,
        terminal_check_every=1,
    )
    planner = _planner()
    start = AckermannState(1.0, 1.0, 0.0)
    goal = AckermannState(1.8, 1.0, 0.0)

    result = operator.try_connect(start, goal, planner)

    assert isinstance(operator, AnalyticExpansionOperator)
    assert isinstance(result, AnalyticExpansionResult)
    assert result.operator == "rl_rs_funnel"
    assert result.terminal_rs_used is True
    assert result.states[-1] == goal
    assert len(result.states) == len(result.actions)
    assert result.actions[0].direction == 1
    assert result.actions[0].step == 0.3

    record = result.telemetry.to_record()
    assert record["analytic_operator"] == "rl_rs_funnel"
    assert record["rl_rollout_steps"] == 1
    assert record["terminal_rs_success"] is True
    assert record["failure_reason"] is None
    assert record["terminal_rs_used"] is True
    assert record["rl_attempts"] == 1
    assert record["rl_successes"] == 1
    assert record["rs_attempts"] >= 1
    assert record["nn_forward_time_s"] >= 0.0
    assert record["rollout_protocol"] == "constant_steer_grid_footprint_terminal_rs"
    assert record["collision_checker"] == "GridFootprintChecker"


def test_rl_rs_funnel_operator_records_policy_forward_time():
    def policy(_obs):
        # Use a tiny deterministic loop so the wall-clock timer has measurable work
        # without adding sleeps or external timing dependencies.
        acc = 0
        for value in range(1024):
            acc += value
        assert acc > 0
        return SteeringAction(0.0)

    operator = RlRsFunnelOperator(
        action_policy=policy,
        max_steps=4,
        action_step_m=0.3,
        terminal_check_every=1,
    )

    result = operator.try_connect(AckermannState(1.0, 1.0, 0.0), AckermannState(1.8, 1.0, 0.0), _planner())

    assert result is not None
    record = result.telemetry.to_record()
    assert record["nn_forward_time_s"] > 0.0
    assert record["rl_attempts"] == 1
    assert record["rl_successes"] == 1


def test_rl_rs_operator_without_terminal_rs_requires_goal_tolerance_success():
    operator = RlRsFunnelOperator(
        action_policy=lambda _obs: SteeringAction(0.0),
        max_steps=4,
        action_step_m=0.3,
        terminal_check_every=1,
        append_terminal_rs=False,
        name="rl_rs_ppo_no_terminal_rs",
    )
    planner = _planner()
    start = AckermannState(1.0, 1.0, 0.0)
    goal = AckermannState(1.8, 1.0, 0.0)

    result = operator.try_connect(start, goal, planner)

    assert isinstance(result, AnalyticExpansionResult)
    assert result.operator == "rl_rs_ppo_no_terminal_rs"
    assert result.terminal_rs_used is False
    assert result.states[-1] != goal
    assert abs(result.states[-1].x - goal.x) <= planner.goal_xy_tol
    assert len(result.states) == 2
    assert len(result.actions) == 2

    record = result.telemetry.to_record()
    assert record["analytic_operator"] == "rl_rs_ppo_no_terminal_rs"
    assert record["rl_rollout_steps"] == 2
    assert record["terminal_rs_success"] is True
    assert record["terminal_rs_used"] is False
    assert record["terminal_rs_action_count"] == 0
    assert record["failure_reason"] is None


def test_rl_rs_operator_without_terminal_rs_rejects_rs_connectable_non_goal_rollout():
    operator = RlRsFunnelOperator(
        action_policy=lambda _obs: SteeringAction(0.0),
        max_steps=1,
        action_step_m=0.3,
        terminal_check_every=1,
        append_terminal_rs=False,
        name="rl_rs_ppo_no_terminal_rs",
    )

    result = operator.try_connect(AckermannState(1.0, 1.0, 0.0), AckermannState(1.8, 1.0, 0.0), _planner())

    assert result is None
    assert operator.last_telemetry is not None
    record = operator.last_telemetry.to_record()
    assert record["analytic_operator"] == "rl_rs_ppo_no_terminal_rs"
    assert record["rl_rollout_steps"] == 1
    assert record["terminal_rs_success"] is True
    assert record["terminal_rs_used"] is False
    assert record["rl_attempts"] == 1
    assert record["rl_successes"] == 0
    assert record["failure_reason"] == "goal_tolerance_not_reached"


def test_rl_rs_funnel_operator_returns_none_on_rollout_collision_with_telemetry():
    operator = RlRsFunnelOperator(
        action_policy=lambda _obs: SteeringAction(0.0),
        max_steps=4,
        action_step_m=0.3,
        terminal_check_every=1,
    )
    result = operator.try_connect(AckermannState(1.0, 1.0, 0.0), AckermannState(1.8, 1.0, 0.0), _planner(blocked=True))

    assert result is None
    assert operator.last_telemetry is not None
    record = operator.last_telemetry.to_record()
    assert record["analytic_operator"] == "rl_rs_funnel"
    assert record["rl_rollout_steps"] == 1
    assert record["terminal_rs_success"] is False
    assert record["failure_reason"] == "collision"
    assert record["terminal_rs_used"] is False


def test_rl_rs_funnel_operator_returns_none_on_no_progress_truncation():
    operator = RlRsFunnelOperator(
        action_policy=lambda _obs: SteeringAction(0.0),
        max_steps=4,
        action_step_m=0.3,
        terminal_check_every=10,
        no_progress_patience=1,
    )

    result = operator.try_connect(AckermannState(1.0, 1.0, 0.0), AckermannState(0.5, 1.0, 0.0), _planner())

    assert result is None
    assert operator.last_telemetry is not None
    record = operator.last_telemetry.to_record()
    assert record["failure_reason"] == "no_progress"
    assert record["terminal_rs_used"] is False
