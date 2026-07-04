import numpy as np
import pytest

from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, HybridAStarPlanner, TwoCircleFootprint
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive
from forest_n3p.third_party.pathplan.hybrid_a_star.operators import (
    AnalyticExpansionOperator,
    AnalyticExpansionResult,
    DangRsOperator,
)


def _planner(operator="dang_multi_rs", *, blocked=False):
    data = np.zeros((80, 80), dtype=np.uint8)
    if blocked:
        data[8:13, 14:17] = 1
    grid_map = GridMap(data, resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)
    return HybridAStarPlanner(
        grid_map,
        footprint,
        AckermannParams(wheelbase=0.5, min_turn_radius=1.0),
        analytic_operator=operator,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=0.30,
        theta_bins=16,
    )


def test_dang_rs_operator_returns_common_result_contract_for_success():
    planner = _planner("dang_multi_rs")
    operator = DangRsOperator()
    start = AckermannState(1.0, 1.0, 0.0)
    goal = AckermannState(1.8, 1.0, 0.0)

    result = operator.try_connect(start, goal, planner)

    assert isinstance(operator, AnalyticExpansionOperator)
    assert isinstance(result, AnalyticExpansionResult)
    assert result.operator == "dang_multi_rs"
    assert result.terminal_rs_used is True
    assert result.states[-1] == goal
    assert len(result.states) == len(result.actions)
    assert result.to_legacy_tuple() == (result.states, result.actions)

    record = result.telemetry.to_record()
    assert record["analytic_operator"] == "dang_multi_rs"
    assert record["analytic_candidate_radius_count"] == len(planner._analytic_radii())
    assert record["analytic_candidate_success_count"] >= 1
    assert record["analytic_total_time_s"] >= 0.0
    assert record["candidate_records"]


def test_dang_rs_operator_returns_none_and_preserves_failure_telemetry():
    planner = _planner("single_rs", blocked=True)
    operator = DangRsOperator()
    start = AckermannState(1.0, 1.0, 0.0)
    goal = AckermannState(2.0, 1.0, 0.0)

    result = operator.try_connect(start, goal, planner)

    assert result is None
    telemetry = planner._last_analytic_telemetry
    assert telemetry is not None
    record = telemetry.to_record()
    assert record["analytic_operator"] == "single_rs"
    assert record["analytic_candidate_radius_count"] == 1
    assert record["analytic_candidate_success_count"] == 0
    assert record["candidate_records"][0]["failure_reason"] == "collision"


def test_analytic_expansion_result_rejects_state_action_length_mismatch():
    with pytest.raises(ValueError, match="states/actions length mismatch"):
        AnalyticExpansionResult(
            states=[AckermannState(1.0, 1.0, 0.0)],
            actions=[
                MotionPrimitive(steering=0.0, direction=1, step=0.3),
                MotionPrimitive(steering=0.0, direction=1, step=0.3),
            ],
            telemetry=None,
            terminal_rs_used=True,
            operator="test",
        )
