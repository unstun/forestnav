from dataclasses import dataclass
import csv

import numpy as np
import pytest

from forest_n3p.evaluation import evaluate_run, planner_run_from_path_stats, planner_run_from_result, write_evaluation_outputs
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint


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
            "analytic_candidate_radius_count": 12,
            "analytic_candidate_success_count": 4,
            "analytic_candidate_failure_count": 8,
            "analytic_rs_solve_time_s": 0.11,
            "analytic_sample_time_s": 0.07,
            "analytic_collision_check_time_s": 0.05,
            "analytic_cost_eval_time_s": 0.02,
            "analytic_total_time_s": 0.25,
            "analytic_sample_count": 120,
            "analytic_collision_check_count": 12,
            "remediations": ["analytic_expansion", "analytic_operator:single_rs"],
            "analytic_telemetry_records": [{"too_large_for_regular_metadata": True}],
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
    assert run.metadata["analytic_candidate_radius_count"] == 12
    assert run.metadata["analytic_candidate_success_count"] == 4
    assert run.metadata["analytic_candidate_failure_count"] == 8
    assert run.metadata["analytic_rs_solve_time_s"] == pytest.approx(0.11)
    assert run.metadata["analytic_sample_time_s"] == pytest.approx(0.07)
    assert run.metadata["analytic_collision_check_time_s"] == pytest.approx(0.05)
    assert run.metadata["analytic_cost_eval_time_s"] == pytest.approx(0.02)
    assert run.metadata["analytic_total_time_s"] == pytest.approx(0.25)
    assert run.metadata["analytic_sample_count"] == 120
    assert run.metadata["analytic_collision_check_count"] == 12
    assert "analytic_telemetry_records" not in run.metadata
    assert run.metadata["planner_remediations"] == ["analytic_expansion", "analytic_operator:single_rs"]

    protocol = run.metadata["timing_protocol"]
    assert protocol["adapter"] == "planner_run_from_path_stats"
    assert protocol["total_time_s"]["source"] == 'stats["time"]'
    assert protocol["planner_time_s"]["source"] == 'stats["time"]'
    assert protocol["planner_time_s"]["available"] is True
    assert protocol["planner_time_s"]["included_components"] == ["planner.plan reported wall-clock"]


def test_evaluation_outputs_expose_rl_rs_analytic_telemetry_columns(tmp_path):
    run = planner_run_from_path_stats(
        ((1.0, 1.0, 0.0), (1.3, 1.0, 0.0)),
        {
            "time": 0.21,
            "expansions": 4,
            "analytic_operator": "rl_rs_funnel_ppo",
            "analytic_attempts": 2,
            "analytic_successes": 1,
            "analytic_failure_count": 1,
            "analytic_telemetry_records": [
                {
                    "analytic_operator": "rl_rs_funnel_ppo",
                    "rl_rollout_steps": 3,
                    "rl_rollout_collision_checks": 9,
                    "rl_rollout_sample_time_s": 0.001,
                    "rl_rollout_collision_time_s": 0.002,
                    "terminal_rs_time_s": 0.003,
                    "terminal_rs_success": True,
                    "terminal_rs_used": True,
                    "terminal_rs_action_count": 2,
                }
            ],
        },
        query_id="q_rl",
        method="ha_rl_rs_ppo",
        difficulty_bucket="Complex",
        distance_bin_key="1:2",
        metadata={
            "rl_rs_checkpoint": "models/final_model.zip",
            "rl_rs_checkpoint_sha256": "abc123",
        },
    )
    record = evaluate_run(
        run,
        GridMap(np.zeros((40, 40), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0)),
        TwoCircleFootprint.from_box(length=0.4, width=0.2),
    )

    assert record.analytic_operator == "rl_rs_funnel_ppo"
    assert record.analytic_attempts == 2
    assert record.analytic_successes == 1
    assert record.analytic_failure_count == 1
    assert record.rl_rollout_steps == 3
    assert record.terminal_rs_success_count == 1
    assert record.terminal_rs_used_count == 1
    assert record.rl_rs_checkpoint == "models/final_model.zip"
    assert record.rl_rs_checkpoint_sha256 == "abc123"

    paths = write_evaluation_outputs([record], tmp_path)
    rows = list(csv.DictReader(paths["records_csv"].open(newline="", encoding="utf-8")))

    assert rows[0]["analytic_operator"] == "rl_rs_funnel_ppo"
    assert rows[0]["analytic_attempts"] == "2"
    assert rows[0]["analytic_successes"] == "1"
    assert rows[0]["analytic_failure_count"] == "1"
    assert rows[0]["rl_rollout_steps"] == "3"
    assert rows[0]["terminal_rs_success_count"] == "1"
    assert rows[0]["terminal_rs_used_count"] == "1"
    assert rows[0]["rl_rs_checkpoint"] == "models/final_model.zip"
    assert rows[0]["rl_rs_checkpoint_sha256"] == "abc123"
