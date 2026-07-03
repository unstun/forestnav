from dataclasses import dataclass

import pytest

from forest_n3p.evaluation import planner_run_from_path_stats, planner_run_from_result


@dataclass(frozen=True)
class PlannerResult:
    path: tuple[tuple[float, float, float], ...]
    success: bool
    total_time_s: float
    total_planner_time_s: float
    total_expansions: int
    failure_reason: str | None = None
    used_f1: int = 0
    used_f2: int = 0
    used_f3: int = 0
    steps: tuple = ()


def test_planner_run_from_result_records_timing_protocol():
    run = planner_run_from_result(
        PlannerResult(
            path=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
            success=True,
            total_time_s=1.25,
            total_planner_time_s=0.75,
            total_expansions=4,
        ),
        query_id="q0",
        method="f_n3p_knn",
        difficulty_bucket="Complex",
        distance_bin_key="8:12",
        metadata={"profile_name": "complex_d02"},
    )

    assert run.total_time_s == pytest.approx(1.25)
    assert run.metadata["profile_name"] == "complex_d02"
    assert run.metadata["total_planner_time_s"] == pytest.approx(0.75)

    protocol = run.metadata["timing_protocol"]
    assert protocol["adapter"] == "planner_run_from_result"
    assert protocol["total_time_s"]["source"] == "result.total_time_s"
    assert protocol["planner_time_s"]["source"] == "result.total_planner_time_s"
    assert protocol["planner_time_s"]["available"] is True
    assert "predictor query plus subgoal RS validation overhead" in protocol["planner_time_s"]["included_components"]


def test_planner_run_from_path_stats_records_timing_protocol():
    run = planner_run_from_path_stats(
        ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        {
            "time": 0.42,
            "expansions": 9,
            "analytic_operator": "single_rs",
            "analytic_attempts": 3,
            "analytic_successes": 1,
            "remediations": ["analytic_expansion", "analytic_operator:single_rs"],
        },
        query_id="q1",
        method="vanilla_ha",
        difficulty_bucket="Extreme",
        distance_bin_key="12:16",
    )

    assert run.total_time_s == pytest.approx(0.42)
    assert run.metadata["total_planner_time_s"] == pytest.approx(0.42)
    assert run.metadata["analytic_operator"] == "single_rs"
    assert run.metadata["analytic_attempts"] == 3
    assert run.metadata["analytic_successes"] == 1
    assert run.metadata["planner_remediations"] == ["analytic_expansion", "analytic_operator:single_rs"]

    protocol = run.metadata["timing_protocol"]
    assert protocol["adapter"] == "planner_run_from_path_stats"
    assert protocol["total_time_s"]["source"] == 'stats["time"]'
    assert protocol["planner_time_s"]["source"] == 'stats["time"]'
    assert protocol["planner_time_s"]["available"] is True
    assert protocol["planner_time_s"]["included_components"] == ["planner.plan reported wall-clock"]
