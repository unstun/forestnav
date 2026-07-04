import numpy as np
import pytest

from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, HybridAStarPlanner, TwoCircleFootprint
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive
from forest_n3p.third_party.pathplan.hybrid_a_star.operators import (
    AnalyticExpansionOperator,
    AnalyticExpansionResult,
    DangRsOperator,
)


class StubTelemetry:
    def __init__(self, *, operator, success=True, failure_reason=None):
        self.operator = str(operator)
        self.success = bool(success)
        self.failure_reason = failure_reason

    def to_record(self):
        return {
            "analytic_operator": self.operator,
            "stub_success": self.success,
            "failure_reason": self.failure_reason,
        }


class DirectStubOperator:
    name = "stub_direct"

    def __init__(self):
        self.calls = []
        self.last_telemetry = None

    def try_connect(self, state, goal, context):
        self.calls.append((state, goal, context))
        self.last_telemetry = StubTelemetry(operator=self.name, success=True)
        return AnalyticExpansionResult(
            states=[goal],
            actions=[MotionPrimitive(steering=0.0, direction=1, step=abs(goal.x - state.x))],
            telemetry=self.last_telemetry,
            terminal_rs_used=False,
            operator=self.name,
        )


class FailingStubOperator:
    name = "stub_failing"

    def __init__(self):
        self.calls = []
        self.last_telemetry = None

    def try_connect(self, state, goal, context):
        self.calls.append((state, goal, context))
        self.last_telemetry = StubTelemetry(operator=self.name, success=False, failure_reason="stub_failure")
        return None


def _planner(operator="dang_multi_rs", *, blocked=False, analytic_expansion_operator=None, max_nodes=2_000):
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
        analytic_expansion_operator=analytic_expansion_operator,
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


def test_planner_dispatches_to_custom_analytic_operator():
    operator = DirectStubOperator()
    planner = _planner(analytic_expansion_operator=operator)

    path, stats = planner.plan(AckermannState(1.0, 1.0, 0.0), AckermannState(1.8, 1.0, 0.0), timeout=1.0)

    assert path[-1] == AckermannState(1.8, 1.0, 0.0)
    assert len(operator.calls) == 1
    assert stats["analytic_operator"] == "stub_direct"
    assert stats["analytic_attempts"] == 1
    assert stats["analytic_successes"] == 1
    assert "analytic_operator:stub_direct" in stats["remediations"]
    record = stats["analytic_telemetry_records"][0]
    assert record["analytic_operator"] == "stub_direct"
    assert record["stub_success"] is True
    assert record["attempt_index"] == 0
    assert record["expansion_idx"] == 0


def test_planner_falls_back_to_primitives_when_custom_operator_returns_none():
    operator = FailingStubOperator()
    planner = _planner(analytic_expansion_operator=operator)

    path, stats = planner.plan(
        AckermannState(1.0, 1.0, 0.0),
        AckermannState(1.6, 1.0, 0.0),
        timeout=1.0,
        max_nodes=2_000,
    )

    assert path
    assert len(operator.calls) >= 1
    assert stats["analytic_operator"] == "stub_failing"
    assert stats["analytic_attempts"] >= 1
    assert stats["analytic_successes"] == 0
    assert "analytic_expansion" not in stats.get("remediations", [])
    record = stats["analytic_failure_records"][0]
    assert record["analytic_operator"] == "stub_failing"
    assert record["failure_reason"] == "stub_failure"
