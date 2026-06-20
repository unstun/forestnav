from __future__ import annotations

import json
import math

import numpy as np
import pytest

from forest_n3p.evaluation import (
    EvaluationConfig,
    EvaluationRun,
    bootstrap_success_rate_difference,
    direction_switches,
    evaluate_run,
    mean_abs_curvature,
    paired_wilcoxon_time,
    path_length,
    summarize_by_method_bucket,
    write_evaluation_outputs,
)
from pathplan import GridMap, TwoCircleFootprint


def _empty_map(width: int = 120, height: int = 120, resolution: float = 0.1) -> GridMap:
    return GridMap(np.zeros((height, width), dtype=np.uint8), resolution=resolution, origin=(0.0, 0.0))


def _blocked_map(width: int = 120, height: int = 120, resolution: float = 0.1) -> GridMap:
    grid = np.zeros((height, width), dtype=np.uint8)
    grid[55:66, 50] = 1
    return GridMap(grid, resolution=resolution, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def _run(query_id: str, method: str, time_s: float, success: bool, path=None) -> EvaluationRun:
    return EvaluationRun(
        query_id=query_id,
        method=method,
        difficulty_bucket="Easy",
        distance_bin_key="d08_12",
        success=success,
        path=tuple(path if path is not None else ((2.0, 6.0, 0.0), (6.0, 6.0, 0.0))),
        total_time_s=time_s,
        total_expansions=int(10 * time_s),
        reference_path_length_m=4.0,
    )


def test_path_motion_metrics_are_computed_from_pose_sequence() -> None:
    path = (
        (2.0, 6.0, 0.0),
        (4.0, 6.0, 0.0),
        (3.0, 6.0, 0.0),
        (5.0, 6.0, 0.0),
    )

    assert path_length(path) == pytest.approx(5.0)
    assert direction_switches(path) == 2
    assert mean_abs_curvature(path) == pytest.approx(0.0)


def test_evaluate_run_computes_all_record_metrics() -> None:
    path = (
        (2.0, 6.0, 0.0),
        (4.0, 6.0, 0.0),
        (3.0, 6.0, 0.0),
        (5.0, 6.0, 0.0),
    )
    run = EvaluationRun(
        query_id="q0",
        method="f_n3p_knn",
        difficulty_bucket="Easy",
        distance_bin_key="d08_12",
        success=True,
        path=path,
        total_time_s=0.25,
        total_expansions=12,
        reference_path_length_m=5.0,
        fallback_f2_count=1,
        subgoal_reachable_count=2,
        subgoal_attempt_count=3,
    )

    record = evaluate_run(run, _empty_map(), _footprint(), config=EvaluationConfig(path_sample_step_m=0.1))

    assert record.success
    assert record.feasible
    assert record.path_length_m == pytest.approx(5.0)
    assert record.path_inflation_ratio == pytest.approx(0.0)
    assert record.direction_switches == 2
    assert record.mean_abs_curvature == pytest.approx(0.0)
    assert record.min_clearance_m is not None and record.min_clearance_m > 0.0
    assert record.collision_violation_count == 0
    assert record.fallback_triggered
    assert record.subgoal_reachability_rate == pytest.approx(2.0 / 3.0)


def test_collision_violations_make_successful_run_infeasible() -> None:
    run = EvaluationRun(
        query_id="q_collision",
        method="vanilla_ha",
        difficulty_bucket="Easy",
        distance_bin_key="d08_12",
        success=True,
        path=((4.5, 6.0, 0.0), (5.5, 6.0, 0.0)),
        total_time_s=0.1,
        total_expansions=2,
    )

    record = evaluate_run(run, _blocked_map(), _footprint(), config=EvaluationConfig(path_sample_step_m=0.05))

    assert record.success
    assert not record.feasible
    assert record.collision_violation_count > 0
    assert record.min_clearance_m is not None and record.min_clearance_m < 0.0


def test_summary_and_statistical_tests_use_paired_queries(tmp_path) -> None:
    grid_map = _empty_map()
    footprint = _footprint()
    runs = [
        _run("q1", "f_n3p_knn", 1.0, True),
        _run("q2", "f_n3p_knn", 2.0, True),
        _run("q3", "f_n3p_knn", 3.0, False, path=()),
        _run("q1", "vanilla_ha", 2.0, True),
        _run("q2", "vanilla_ha", 4.0, False, path=()),
        _run("q3", "vanilla_ha", 6.0, False, path=()),
    ]
    records = tuple(evaluate_run(run, grid_map, footprint) for run in runs)

    summaries = summarize_by_method_bucket(records)
    knn = next(item for item in summaries if item.method == "f_n3p_knn")
    assert knn.count == 3
    assert knn.success_rate == pytest.approx(2.0 / 3.0)
    assert knn.p95_time_s == pytest.approx(float(np.percentile([1.0, 2.0, 3.0], 95)))

    time_test = paired_wilcoxon_time(records, "f_n3p_knn", "vanilla_ha")
    assert time_test.paired_query_count == 3
    assert time_test.p_value is not None
    assert time_test.median_delta_a_minus_b_s == pytest.approx(-2.0)

    ci = bootstrap_success_rate_difference(
        records,
        "f_n3p_knn",
        "vanilla_ha",
        config=EvaluationConfig(bootstrap_resamples=200, bootstrap_seed=7),
    )
    assert ci.paired_query_count == 3
    assert ci.observed_success_rate_diff_a_minus_b == pytest.approx(1.0 / 3.0)
    assert ci.ci_low is not None and ci.ci_high is not None
    assert ci.ci_low <= ci.observed_success_rate_diff_a_minus_b <= ci.ci_high

    outputs = write_evaluation_outputs(records, tmp_path, paired_time_tests=(time_test,), success_rate_cis=(ci,))
    assert outputs["records_csv"].exists()
    assert outputs["summary_csv"].exists()
    payload = json.loads(outputs["summary_json"].read_text(encoding="utf-8"))
    assert payload["record_count"] == 6
    assert payload["paired_time_tests"][0]["paired_query_count"] == 3
