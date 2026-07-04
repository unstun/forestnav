from dataclasses import dataclass
import csv
import json

import numpy as np
import pytest

from forest_n3p.evaluation import (
    EvaluationRecord,
    bootstrap_timeout_failure_rate_difference,
    evaluate_run,
    paired_wilcoxon_expansions,
    planner_run_from_path_stats,
    planner_run_from_result,
    summarize_by_method_bucket,
    write_evaluation_outputs,
)
from forest_n3p.main_evaluation import _stat_pairs
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
                    "nn_forward_time_s": 0.004,
                    "rl_attempts": 1,
                    "rl_successes": 1,
                    "rs_attempts": 2,
                    "terminal_rs_time_s": 0.003,
                    "terminal_rs_success": True,
                    "terminal_rs_used": True,
                    "terminal_rs_action_count": 2,
                    "fallback_to_primitives_count": 0,
                    "rollout_protocol": "constant_steer_grid_footprint_terminal_rs",
                    "collision_checker": "GridFootprintChecker",
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
    assert record.rl_attempts == 1
    assert record.rl_successes == 1
    assert record.rs_attempts == 2
    assert record.nn_forward_time_s == pytest.approx(0.004)
    assert record.fallback_to_primitives_count == 1
    assert record.rollout_protocol == "constant_steer_grid_footprint_terminal_rs"
    assert record.collision_checker == "GridFootprintChecker"
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
    assert rows[0]["rl_attempts"] == "1"
    assert rows[0]["rl_successes"] == "1"
    assert rows[0]["rs_attempts"] == "2"
    assert float(rows[0]["nn_forward_time_s"]) == pytest.approx(0.004)
    assert rows[0]["fallback_to_primitives_count"] == "1"
    assert rows[0]["rollout_protocol"] == "constant_steer_grid_footprint_terminal_rs"
    assert rows[0]["collision_checker"] == "GridFootprintChecker"
    assert rows[0]["rl_rollout_steps"] == "3"
    assert rows[0]["terminal_rs_success_count"] == "1"
    assert rows[0]["terminal_rs_used_count"] == "1"
    assert rows[0]["rl_rs_checkpoint"] == "models/final_model.zip"
    assert rows[0]["rl_rs_checkpoint_sha256"] == "abc123"

    summary_rows = list(csv.DictReader(paths["summary_csv"].open(newline="", encoding="utf-8")))
    assert float(summary_rows[0]["mean_nn_forward_time_s"]) == pytest.approx(0.004)
    assert float(summary_rows[0]["p95_nn_forward_time_s"]) == pytest.approx(0.004)


def test_evaluation_outputs_expose_bc_operator_checkpoint_columns(tmp_path):
    run = planner_run_from_path_stats(
        ((1.0, 1.0, 0.0), (1.3, 1.0, 0.0)),
        {
            "time": 0.19,
            "expansions": 5,
            "analytic_operator": "rl_rs_funnel_bc",
            "analytic_attempts": 2,
            "analytic_successes": 1,
            "analytic_failure_count": 1,
            "analytic_telemetry_records": [
                {
                    "analytic_operator": "rl_rs_funnel_bc",
                    "rl_rollout_steps": 4,
                    "terminal_rs_success": True,
                    "terminal_rs_used": True,
                    "terminal_rs_action_count": 2,
                }
            ],
        },
        query_id="q_bc",
        method="bc_analytic_operator",
        difficulty_bucket="Complex",
        distance_bin_key="1:2",
        metadata={
            "bc_checkpoint": "models/bc_checkpoint.pt",
            "bc_checkpoint_sha256": "bc123",
        },
    )
    record = evaluate_run(
        run,
        GridMap(np.zeros((40, 40), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0)),
        TwoCircleFootprint.from_box(length=0.4, width=0.2),
    )

    assert record.analytic_operator == "rl_rs_funnel_bc"
    assert record.rl_rollout_steps == 4
    assert record.bc_checkpoint == "models/bc_checkpoint.pt"
    assert record.bc_checkpoint_sha256 == "bc123"

    paths = write_evaluation_outputs([record], tmp_path)
    rows = list(csv.DictReader(paths["records_csv"].open(newline="", encoding="utf-8")))

    assert rows[0]["analytic_operator"] == "rl_rs_funnel_bc"
    assert rows[0]["rl_rollout_steps"] == "4"
    assert rows[0]["bc_checkpoint"] == "models/bc_checkpoint.pt"
    assert rows[0]["bc_checkpoint_sha256"] == "bc123"


def test_summary_exposes_timeout_failure_rate_for_contract_metric():
    rows = [
        _record("q0", method="ha_dang_multi_rs", success=True, feasible=True, failure_reason=None),
        _record("q1", method="ha_dang_multi_rs", success=False, feasible=False, failure_reason="timeout"),
        _record("q2", method="ha_dang_multi_rs", success=False, feasible=False, failure_reason="collision"),
    ]

    summary = summarize_by_method_bucket(rows)[0]

    assert summary.timeout_failure_count == 1
    assert summary.timeout_failure_rate == pytest.approx(1.0 / 3.0)


def test_paired_wilcoxon_expansions_uses_paired_query_total_expansions():
    rows = [
        _record("q0", method="ha_dang_multi_rs", success=True, feasible=True, failure_reason=None, total_expansions=100),
        _record("q0", method="ha_rl_rs_ppo", success=True, feasible=True, failure_reason=None, total_expansions=40),
        _record("q1", method="ha_dang_multi_rs", success=True, feasible=True, failure_reason=None, total_expansions=80),
        _record("q1", method="ha_rl_rs_ppo", success=True, feasible=True, failure_reason=None, total_expansions=50),
    ]

    result = paired_wilcoxon_expansions(rows, "ha_rl_rs_ppo", "ha_dang_multi_rs")

    assert result.method_a == "ha_rl_rs_ppo"
    assert result.method_b == "ha_dang_multi_rs"
    assert result.paired_query_count == 2
    assert result.median_delta_a_minus_b_expansions == pytest.approx(-45.0)


def test_bootstrap_timeout_failure_rate_difference_uses_paired_timeout_indicators(tmp_path):
    rows = [
        _record("q0", method="ha_rl_rs_ppo", success=False, feasible=False, failure_reason="timeout", total_expansions=10),
        _record("q0", method="ha_dang_multi_rs", success=True, feasible=True, failure_reason=None, total_expansions=20),
        _record("q1", method="ha_rl_rs_ppo", success=True, feasible=True, failure_reason=None, total_expansions=10),
        _record("q1", method="ha_dang_multi_rs", success=False, feasible=False, failure_reason="planner_timeout", total_expansions=20),
        _record("q2", method="ha_rl_rs_ppo", success=False, feasible=False, failure_reason="timeout:max_nodes", total_expansions=10),
        _record("q2", method="ha_dang_multi_rs", success=True, feasible=True, failure_reason=None, total_expansions=20),
    ]

    result = bootstrap_timeout_failure_rate_difference(rows, "ha_rl_rs_ppo", "ha_dang_multi_rs")

    assert result.metric_id == "timeout_failure_rate"
    assert result.method_a == "ha_rl_rs_ppo"
    assert result.method_b == "ha_dang_multi_rs"
    assert result.paired_query_count == 3
    assert result.observed_rate_diff_a_minus_b == pytest.approx(1.0 / 3.0)
    assert result.ci_low is not None
    assert result.ci_high is not None

    paths = write_evaluation_outputs(rows, tmp_path, timeout_failure_rate_cis=(result,))
    payload = json.loads(paths["summary_json"].read_text(encoding="utf-8"))

    assert payload["timeout_failure_rate_bootstrap_ci"][0]["metric_id"] == "timeout_failure_rate"
    assert payload["timeout_failure_rate_bootstrap_ci"][0]["observed_rate_diff_a_minus_b"] == pytest.approx(1.0 / 3.0)


def test_stat_pairs_include_module2_operator_against_dang_rs_baseline():
    pairs = _stat_pairs(
        (
            "ha_no_analytic",
            "ha_single_rs",
            "ha_dang_multi_rs",
            "bc_analytic_operator",
            "ppo_analytic_operator",
            "ha_rl_rs_ppo",
        )
    )

    assert ("bc_analytic_operator", "ha_dang_multi_rs") in pairs
    assert ("ppo_analytic_operator", "ha_dang_multi_rs") in pairs
    assert ("ha_rl_rs_ppo", "ha_dang_multi_rs") in pairs


def _record(
    query_id: str,
    *,
    method: str,
    success: bool,
    feasible: bool,
    failure_reason: str | None,
    total_expansions: int = 10,
) -> EvaluationRecord:
    return EvaluationRecord(
        query_id=query_id,
        method=method,
        difficulty_bucket="Complex",
        distance_bin_key="8:12",
        success=success,
        feasible=feasible,
        total_time_s=1.0,
        total_expansions=total_expansions,
        path_length_m=None,
        reference_path_length_m=None,
        path_inflation_ratio=None,
        direction_switches=0,
        mean_abs_curvature=None,
        min_clearance_m=None,
        collision_violation_count=0,
        fallback_f1_count=0,
        fallback_f2_count=0,
        fallback_f3_count=0,
        fallback_triggered=False,
        subgoal_reachable_count=None,
        subgoal_attempt_count=None,
        subgoal_reachability_rate=None,
        analytic_operator=None,
        analytic_attempts=None,
        analytic_successes=None,
        analytic_failure_count=None,
        rl_attempts=None,
        rl_successes=None,
        rs_attempts=None,
        nn_forward_time_s=None,
        fallback_to_primitives_count=None,
        rollout_protocol=None,
        collision_checker=None,
        rl_rollout_steps=None,
        rl_rollout_collision_checks=None,
        rl_rollout_sample_time_s=None,
        rl_rollout_collision_time_s=None,
        terminal_rs_time_s=None,
        terminal_rs_success_count=None,
        terminal_rs_used_count=None,
        terminal_rs_action_count=None,
        bc_checkpoint=None,
        bc_checkpoint_sha256=None,
        rl_rs_checkpoint=None,
        rl_rs_checkpoint_sha256=None,
        failure_reason=failure_reason,
    )
