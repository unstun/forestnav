from __future__ import annotations

import pytest

from forest_n3p.difficulty_calibration import (
    CalibrationRecord,
    BucketRule,
    choose_axis_cutpoints,
    default_density_levels,
    parse_distance_bins,
    summarize_axis,
)
from forest_n3p.scripts.run_difficulty_calibration import parse_args


def _record(
    *,
    axis: str,
    level_key: str,
    level_order: int,
    success: bool,
    time_s: float,
    expansions: int,
    timed_out: bool = False,
) -> CalibrationRecord:
    return CalibrationRecord(
        axis=axis,
        level_key=level_key,
        level_order=level_order,
        level_label=level_key,
        map_id=0,
        query_id=0,
        map_seed=11,
        query_seed=101,
        trunk_count=60 + 20 * level_order,
        trunk_gap_m=1.2 - 0.1 * level_order,
        gap_to_vehicle_width=1.0,
        obstacle_ratio=0.1,
        distance_min_m=None,
        distance_max_m=None,
        start=(1.0, 1.0, 0.0),
        goal=(5.0, 1.0, 0.0),
        euclidean_distance_m=4.0,
        teacher_success=success,
        teacher_failure_reason=None if success else ("timeout" if timed_out else "search_failed"),
        teacher_time_s=time_s,
        teacher_expansions=expansions,
        teacher_path_length_m=4.0 if success else 0.0,
        timed_out=timed_out,
    )


def test_default_density_levels_cover_at_least_eight_monotonic_levels() -> None:
    levels = default_density_levels()

    assert len(levels) >= 8
    assert [level.order for level in levels] == list(range(len(levels)))
    assert [level.trunk_count for level in levels] == sorted(level.trunk_count for level in levels)
    assert [level.trunk_gap_m for level in levels] == sorted(
        (level.trunk_gap_m for level in levels),
        reverse=True,
    )


def test_parse_distance_bins_uses_ordered_half_open_ranges() -> None:
    bins = parse_distance_bins("4:8,8:12,12:")

    assert [item.key for item in bins] == ["d04_08", "d08_12", "d12_inf"]
    assert bins[0].min_distance_m == pytest.approx(4.0)
    assert bins[0].max_distance_m == pytest.approx(8.0)
    assert bins[-1].max_distance_m is None


def test_summarize_axis_reports_rates_and_percentiles() -> None:
    records = [
        _record(axis="density", level_key="d00", level_order=0, success=True, time_s=0.10, expansions=10),
        _record(axis="density", level_key="d00", level_order=0, success=True, time_s=0.20, expansions=20),
        _record(axis="density", level_key="d01", level_order=1, success=False, time_s=2.50, expansions=300, timed_out=True),
    ]

    summaries = summarize_axis(records, axis="density")

    assert len(summaries) == 2
    assert summaries[0].level_key == "d00"
    assert summaries[0].success_rate == pytest.approx(1.0)
    assert summaries[0].median_time_s == pytest.approx(0.15)
    assert summaries[1].timeout_rate == pytest.approx(1.0)


def test_choose_axis_cutpoints_requires_separated_easy_complex_extreme() -> None:
    records: list[CalibrationRecord] = []
    for _ in range(10):
        records.append(_record(axis="density", level_key="d00", level_order=0, success=True, time_s=0.12, expansions=20))
    for idx in range(10):
        records.append(
            _record(
                axis="density",
                level_key="d01",
                level_order=1,
                success=idx < 8,
                time_s=0.80,
                expansions=220,
            )
        )
    for idx in range(10):
        records.append(
            _record(
                axis="density",
                level_key="d02",
                level_order=2,
                success=idx < 4,
                time_s=2.50,
                expansions=800,
                timed_out=idx >= 4,
            )
        )

    summaries = summarize_axis(records, axis="density")
    result = choose_axis_cutpoints(summaries, BucketRule(easy_median_time_s_max=0.5))

    assert result["bucket_separation_pass"] is True
    assert result["easy_max"]["level_key"] == "d00"
    assert result["complex_range"]["min"]["level_key"] == "d01"
    assert result["extreme_min"]["level_key"] == "d02"


def test_run_difficulty_calibration_cli_accepts_scale_overrides() -> None:
    args = parse_args(
        [
            "--maps-per-density",
            "2",
            "--queries-per-map",
            "3",
            "--distance-bins",
            "6:10,10:14",
            "--queries-per-distance-bin",
            "4",
        ]
    )

    assert args.maps_per_density == 2
    assert args.queries_per_map == 3
    assert args.distance_bins == "6:10,10:14"
    assert args.queries_per_distance_bin == 4
