from __future__ import annotations

import time

import numpy as np
import pytest

from forest_n3p.training_data import (
    TrainingDataConfig,
    TrainingMapRecord,
    TrainingProfile,
    TrainingQueryRecord,
    TrainingSampleRecord,
    WallTimeoutError,
    build_training_schedule,
    _run_with_wall_timeout,
    summarize_training_data,
)
from forest_n3p.scripts.run_training_data_collection import parse_args


def _map_record(map_id: int, bucket: str) -> TrainingMapRecord:
    return TrainingMapRecord(
        map_id=map_id,
        profile_name=f"{bucket.lower()}_profile",
        difficulty_bucket=bucket,
        map_seed=100 + map_id,
        generated=True,
        generation_time_s=0.01,
        trunk_count=40,
        trunk_gap_m=1.2,
        trunk_gap_jitter=0.2,
        obstacle_ratio=0.1,
        failure_reason=None,
    )


def _query_record(query_id: int, bucket: str, label_success: bool) -> TrainingQueryRecord:
    return TrainingQueryRecord(
        global_query_id=query_id,
        map_id=query_id,
        query_id=0,
        profile_name=f"{bucket.lower()}_profile",
        difficulty_bucket=bucket,
        distance_bin_key="d08_12",
        distance_min_m=8.0,
        distance_max_m=12.0,
        map_seed=100 + query_id,
        query_seed=200 + query_id,
        start=(1.0, 1.0, 0.0),
        goal=(10.0, 1.0, 0.0),
        euclidean_distance_m=9.0,
        teacher_success=True,
        teacher_failure_reason=None,
        teacher_time_s=0.1,
        teacher_expansions=20,
        teacher_path_length_m=9.0,
        teacher_path_pose_count=4,
        label_attempted=True,
        label_success=label_success,
        label_failure_reason=None if label_success else "short_progress",
        label_sample_count=1 if label_success else 0,
        total_segment_count=2 if label_success else 0,
        label_candidate_checks=5,
    )


def _sample_record(sample_id: int, query_id: int, bucket: str) -> TrainingSampleRecord:
    return TrainingSampleRecord(
        sample_id=sample_id,
        global_query_id=query_id,
        map_id=query_id,
        query_id=0,
        sample_index=0,
        profile_name=f"{bucket.lower()}_profile",
        difficulty_bucket=bucket,
        distance_bin_key="d08_12",
        current_pose=(1.0, 1.0, 0.0),
        subgoal_pose=(4.0, 1.0, 0.0),
        delta_body=(3.0, 0.0, 0.0),
        s_start_m=0.0,
        s_subgoal_m=3.0,
        rs_length_m=3.0,
        rs_sample_count=30,
    )


def test_build_training_schedule_balances_buckets_and_cycles_profiles() -> None:
    profiles = (
        TrainingProfile("easy_a", "Easy", trunk_count=40, trunk_gap_m=1.35),
        TrainingProfile("easy_b", "Easy", trunk_count=55, trunk_gap_m=1.25),
        TrainingProfile("complex", "Complex", trunk_count=70, trunk_gap_m=1.15),
        TrainingProfile("extreme", "Extreme", trunk_count=85, trunk_gap_m=1.05),
    )

    schedule = build_training_schedule(profiles, map_count=7)

    assert [profile.difficulty_bucket for profile in schedule].count("Easy") == 3
    assert [profile.difficulty_bucket for profile in schedule].count("Complex") == 2
    assert [profile.difficulty_bucket for profile in schedule].count("Extreme") == 2
    assert [profile.name for profile in schedule[:3]] == ["easy_a", "easy_b", "easy_a"]


def test_summarize_training_data_requires_total_and_bucket_coverage() -> None:
    config = TrainingDataConfig(
        map_count=3,
        queries_per_map=1,
        total_sample_target=3,
        total_sample_lower_bound=3,
        min_samples_per_bucket=1,
    )
    buckets = ("Easy", "Complex", "Extreme")
    maps = tuple(_map_record(idx, bucket) for idx, bucket in enumerate(buckets))
    queries = tuple(_query_record(idx, bucket, label_success=True) for idx, bucket in enumerate(buckets))
    samples = tuple(_sample_record(idx, idx, bucket) for idx, bucket in enumerate(buckets))

    summary = summarize_training_data(
        config=config,
        maps=maps,
        queries=queries,
        samples=samples,
        feature_array=np.zeros((3, 41), dtype=np.float32),
        label_array=np.zeros((3, 3), dtype=np.float32),
        paths=(),
    )

    assert summary["acceptance_pass"] is True
    assert summary["total_sample_pass"] is True
    assert summary["bucket_coverage_pass"] is True
    assert summary["sample_count_by_bucket"] == {"Easy": 1, "Complex": 1, "Extreme": 1}


def test_summarize_training_data_fails_when_extreme_bucket_is_empty() -> None:
    config = TrainingDataConfig(
        map_count=3,
        queries_per_map=1,
        total_sample_target=2,
        total_sample_lower_bound=2,
        min_samples_per_bucket=1,
    )
    maps = (
        _map_record(0, "Easy"),
        _map_record(1, "Complex"),
        _map_record(2, "Extreme"),
    )
    queries = (
        _query_record(0, "Easy", label_success=True),
        _query_record(1, "Complex", label_success=True),
        _query_record(2, "Extreme", label_success=False),
    )
    samples = (
        _sample_record(0, 0, "Easy"),
        _sample_record(1, 1, "Complex"),
    )

    summary = summarize_training_data(
        config=config,
        maps=maps,
        queries=queries,
        samples=samples,
        feature_array=np.zeros((2, 41), dtype=np.float32),
        label_array=np.zeros((2, 3), dtype=np.float32),
        paths=(),
    )

    assert summary["acceptance_pass"] is False
    assert summary["bucket_coverage_pass"] is False
    assert summary["sample_count_by_bucket"]["Extreme"] == 0


def test_run_training_data_cli_accepts_scale_overrides() -> None:
    args = parse_args(
        [
            "--map-count",
            "4",
            "--queries-per-map",
            "2",
            "--distance-bins",
            "4:8,8:12",
            "--workers",
            "1",
            "--teacher-wall-timeout-s",
            "7.5",
            "--map-generation-wall-timeout-s",
            "12",
            "--map-job-wall-timeout-s",
            "60",
            "--total-sample-lower-bound",
            "5",
            "--min-samples-per-bucket",
            "1",
        ]
    )

    assert args.map_count == 4
    assert args.queries_per_map == 2
    assert args.distance_bins == "4:8,8:12"
    assert args.workers == 1
    assert args.teacher_wall_timeout_s == 7.5
    assert args.map_generation_wall_timeout_s == 12
    assert args.map_job_wall_timeout_s == 60
    assert args.total_sample_lower_bound == 5
    assert args.min_samples_per_bucket == 1


def test_wall_timeout_interrupts_slow_call() -> None:
    with pytest.raises(WallTimeoutError, match="unit_slow_call_wall_timeout"):
        _run_with_wall_timeout("unit_slow_call", 0.01, lambda: time.sleep(0.2))
