import itertools

import numpy as np
import pytest

from forest_n3p import inference
from forest_n3p.inference import InferenceConfig, NeighborPrediction
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint


class RejectingPredictor:
    def query(self, feature, *, current_pose, k):
        raise AssertionError("direct RS should terminate before predictor.query()")


class StaticPredictor:
    name = "static"

    def __init__(self, predictions):
        self._predictions = tuple(predictions)

    def query(self, feature, *, current_pose, k):
        return self._predictions[:k]


def _fixed_clock(monkeypatch, *, start=100.0, step=0.25):
    ticks = itertools.count()

    def perf_counter():
        return start + step * next(ticks)

    monkeypatch.setattr(inference.time, "perf_counter", perf_counter)


def _empty_grid():
    return GridMap(np.zeros((80, 80), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))


def _blocked_goal_grid():
    data = np.zeros((80, 80), dtype=np.uint8)
    data[8:13, 21:24] = 1
    return GridMap(data, resolution=0.1, origin=(0.0, 0.0))


def _footprint():
    return TwoCircleFootprint.from_box(length=0.4, width=0.2)


def _config(*, commit_verified_rs_segments=True):
    return InferenceConfig(
        k_neighbors=1,
        turning_radius_m=1.0,
        wheelbase_m=0.5,
        rs_sample_step_m=0.05,
        theta_bins=16,
        collision_padding=0.0,
        max_steps_override=1,
        enable_f2=False,
        enable_f3=False,
        commit_verified_rs_segments=commit_verified_rs_segments,
    )


def test_direct_rs_goal_counts_direct_collision_check_time(monkeypatch):
    _fixed_clock(monkeypatch)

    result = inference.run_forest_n3p(
        _empty_grid(),
        _footprint(),
        start=(1.0, 1.0, 0.0),
        goal=(1.8, 1.0, 0.0),
        predictor=RejectingPredictor(),
        config=_config(),
    )

    assert result.success
    assert result.termination_reason == "direct_rs_goal"
    assert result.total_planner_time_s == pytest.approx(0.25)
    assert result.total_time_s == pytest.approx(0.75)
    assert len(result.steps) == 1
    assert result.steps[0].mode == "direct_rs_goal"
    assert result.steps[0].planner_time_s == pytest.approx(0.25)
    assert result.steps[0].planner_expansions == 0


def test_verified_rs_subgoal_counts_prediction_and_validation_time(monkeypatch):
    _fixed_clock(monkeypatch)
    prediction = NeighborPrediction(
        rank=1,
        sample_index=0,
        distance=0.0,
        delta_body=(0.4, 0.0, 0.0),
        subgoal_pose=(1.4, 1.0, 0.0),
    )

    result = inference.run_forest_n3p(
        _blocked_goal_grid(),
        _footprint(),
        start=(1.0, 1.0, 0.0),
        goal=(3.0, 1.0, 0.0),
        predictor=StaticPredictor([prediction]),
        config=_config(),
    )

    assert not result.success
    assert result.failure_reason == "max_step_budget;f3_disabled"
    assert result.total_planner_time_s == pytest.approx(0.25)
    assert result.total_time_s == pytest.approx(0.75)
    assert len(result.steps) == 1

    step = result.steps[0]
    assert step.mode == "static_rs_verified_segment"
    assert step.target_pose == pytest.approx((1.4, 1.0, 0.0))
    assert step.segment_success
    assert step.segment_failure_reason is None
    assert step.planner_time_s == pytest.approx(0.25)
    assert step.planner_expansions == 0
    assert step.distance_to_goal_m == pytest.approx(1.6)


def test_segment_planning_counts_prediction_overhead(monkeypatch):
    _fixed_clock(monkeypatch)
    prediction = NeighborPrediction(
        rank=1,
        sample_index=0,
        distance=0.0,
        delta_body=(0.4, 0.0, 0.0),
        subgoal_pose=(1.4, 1.0, 0.0),
    )

    def fake_plan_segment(planner, start, goal, *, timeout_s, max_nodes):
        assert start == pytest.approx((1.0, 1.0, 0.0))
        assert goal == pytest.approx((1.4, 1.0, 0.0))
        return inference._PlanSegmentResult(
            success=True,
            poses=(start, goal),
            failure_reason=None,
            planner_time_s=0.50,
            expansions=7,
        )

    monkeypatch.setattr(inference, "_plan_segment", fake_plan_segment)

    result = inference.run_forest_n3p(
        _blocked_goal_grid(),
        _footprint(),
        start=(1.0, 1.0, 0.0),
        goal=(3.0, 1.0, 0.0),
        predictor=StaticPredictor([prediction]),
        config=_config(commit_verified_rs_segments=False),
    )

    assert not result.success
    assert result.failure_reason == "max_step_budget;f3_disabled"
    assert result.total_planner_time_s == pytest.approx(0.75)
    assert result.total_expansions == 7
    assert len(result.steps) == 1

    step = result.steps[0]
    assert step.mode == "static_segment"
    assert step.segment_success
    assert step.planner_time_s == pytest.approx(0.75)
    assert step.planner_expansions == 7
