from __future__ import annotations

import pytest

from forest_n3p.pilot_labeling import (
    QueryRecord,
    build_profile_schedule,
    default_profiles,
    summarize_query_records,
)
from forest_n3p.scripts.run_label_pilot import parse_args


def test_default_profile_schedule_allocates_twenty_maps_across_density_buckets() -> None:
    schedule = build_profile_schedule(default_profiles(), map_count=20)

    assert len(schedule) == 20
    counts = {profile.name: sum(1 for item in schedule if item.name == profile.name) for profile in default_profiles()}
    assert counts == {"low": 7, "medium": 7, "high": 6}


def test_summarize_query_records_reports_teacher_and_label_rates() -> None:
    records = [
        QueryRecord(
            map_id=0,
            query_id=0,
            difficulty="low",
            map_seed=11,
            query_seed=101,
            start=(1.0, 1.0, 0.0),
            goal=(5.0, 1.0, 0.0),
            teacher_success=True,
            teacher_failure_reason=None,
            teacher_time_s=0.2,
            teacher_expansions=5,
            teacher_path_length_m=4.0,
            label_attempted=True,
            label_success=True,
            label_failure_reason=None,
            label_sample_count=1,
            total_segment_count=2,
            segment_lengths_m=(4.0,),
        ),
        QueryRecord(
            map_id=0,
            query_id=1,
            difficulty="low",
            map_seed=11,
            query_seed=102,
            start=(1.0, 2.0, 0.0),
            goal=(5.0, 2.0, 0.0),
            teacher_success=True,
            teacher_failure_reason=None,
            teacher_time_s=0.3,
            teacher_expansions=8,
            teacher_path_length_m=4.2,
            label_attempted=True,
            label_success=False,
            label_failure_reason="short_progress",
            label_sample_count=0,
            total_segment_count=0,
            segment_lengths_m=(),
        ),
        QueryRecord(
            map_id=1,
            query_id=0,
            difficulty="high",
            map_seed=12,
            query_seed=201,
            start=(2.0, 2.0, 0.0),
            goal=(6.0, 2.0, 0.0),
            teacher_success=False,
            teacher_failure_reason="timeout",
            teacher_time_s=1.0,
            teacher_expansions=120,
            teacher_path_length_m=0.0,
            label_attempted=False,
            label_success=False,
            label_failure_reason=None,
            label_sample_count=0,
            total_segment_count=0,
            segment_lengths_m=(),
        ),
    ]

    summary = summarize_query_records(records)

    assert summary["total_queries"] == 3
    assert summary["teacher_success_count"] == 2
    assert summary["teacher_success_rate"] == pytest.approx(2.0 / 3.0)
    assert summary["label_attempt_count"] == 2
    assert summary["label_success_count"] == 1
    assert summary["label_failure_rate"] == pytest.approx(0.5)
    assert summary["total_samples"] == 1
    assert summary["segment_length_m"]["mean"] == pytest.approx(4.0)
    assert summary["by_difficulty"]["low"]["label_failure_count"] == 1


def test_run_label_pilot_cli_accepts_lmin_lmax_overrides() -> None:
    args = parse_args(["--l-min-m", "1.0", "--l-max-m", "9.0"])

    assert args.l_min_m == pytest.approx(1.0)
    assert args.l_max_m == pytest.approx(9.0)
