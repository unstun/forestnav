from __future__ import annotations

import csv
import json
import math
import time
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from forest_n3p.maps.forest import generate_forest_grid
from forest_n3p.pilot_labeling import (
    DifficultyProfile,
    _make_planner,
    footprint_clearance_m,
    make_forest_params,
)
from forest_n3p.third_party.pathplan import (
    AckermannState,
    GridMap,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


Pose = tuple[float, float, float]
VEHICLE_WIDTH_M = 0.740


@dataclass(frozen=True)
class DensityLevel:
    key: str
    order: int
    trunk_count: int
    trunk_gap_m: float
    trunk_gap_jitter: float = 0.25
    bush_cluster_count: int = 0

    @property
    def label(self) -> str:
        return f"{self.key}:trees={self.trunk_count},gap={self.trunk_gap_m:.2f}m"

    @property
    def gap_to_vehicle_width(self) -> float:
        return float(self.trunk_gap_m) / VEHICLE_WIDTH_M


@dataclass(frozen=True)
class DistanceBin:
    key: str
    order: int
    min_distance_m: float
    max_distance_m: float | None

    @property
    def label(self) -> str:
        if self.max_distance_m is None:
            return f"{self.min_distance_m:.1f}m+"
        return f"[{self.min_distance_m:.1f},{self.max_distance_m:.1f})m"


@dataclass(frozen=True)
class BucketRule:
    easy_success_rate_min: float = 0.85
    easy_median_time_s_max: float = 0.50
    easy_timeout_rate_max: float = 0.10
    extreme_success_rate_max: float = 0.70
    extreme_timeout_rate_min: float = 0.30
    extreme_success_rate_hard_max: float = 0.60
    extreme_timeout_rate_hard_min: float = 0.50
    min_success_rate_gap_easy_to_extreme: float = 0.20
    min_complex_to_easy_time_ratio: float = 1.50
    min_extreme_to_easy_time_ratio: float = 2.00
    min_complex_to_easy_p95_time_ratio: float = 1.50
    min_extreme_to_easy_p95_time_ratio: float = 2.00
    min_complex_to_easy_p95_expansion_ratio: float = 1.50
    min_extreme_to_easy_expansion_ratio: float = 2.00
    min_timeout_rate_gap_easy_to_complex: float = 0.10


@dataclass(frozen=True)
class CalibrationConfig:
    seed: int = 20260620
    maps_per_density: int = 3
    queries_per_map: int = 5
    distance_map_count: int = 3
    queries_per_distance_bin: int = 8
    width_cells: int = 300
    height_cells: int = 300
    resolution_m: float = 0.1
    max_query_sample_attempts: int = 800
    density_min_query_distance_m: float = 8.0
    teacher_timeout_s: float = 2.5
    teacher_max_nodes: int = 15_000
    turning_radius_m: float = 1.0
    wheelbase_m: float = 0.6
    density_levels: tuple[DensityLevel, ...] = field(default_factory=lambda: default_density_levels())
    distance_bins: tuple[DistanceBin, ...] = field(default_factory=lambda: default_distance_bins())
    distance_reference_level: DensityLevel = field(
        default_factory=lambda: DensityLevel(
            key="distance_ref",
            order=0,
            trunk_count=90,
            trunk_gap_m=1.00,
            trunk_gap_jitter=0.25,
        )
    )
    bucket_rule: BucketRule = field(default_factory=BucketRule)


@dataclass(frozen=True)
class CalibrationMapRecord:
    axis: str
    level_key: str
    level_order: int
    level_label: str
    map_id: int
    map_seed: int
    generated: bool
    generation_time_s: float
    trunk_count: int
    trunk_gap_m: float
    gap_to_vehicle_width: float
    obstacle_ratio: float
    failure_reason: str | None


@dataclass(frozen=True)
class CalibrationRecord:
    axis: str
    level_key: str
    level_order: int
    level_label: str
    map_id: int
    query_id: int
    map_seed: int
    query_seed: int
    trunk_count: int
    trunk_gap_m: float
    gap_to_vehicle_width: float
    obstacle_ratio: float
    distance_min_m: float | None
    distance_max_m: float | None
    start: Pose
    goal: Pose
    euclidean_distance_m: float
    teacher_success: bool
    teacher_failure_reason: str | None
    teacher_time_s: float
    teacher_expansions: int
    teacher_path_length_m: float
    timed_out: bool
    query_sampled: bool = True
    tree_density_per_100m2: float | None = None


@dataclass(frozen=True)
class LevelSummary:
    axis: str
    level_key: str
    level_order: int
    level_label: str
    query_count: int
    planner_attempt_count: int
    success_count: int
    success_rate: float | None
    timeout_count: int
    timeout_rate: float | None
    median_time_s: float | None
    p95_time_s: float | None
    mean_time_s: float | None
    median_expansions: float | None
    p95_expansions: float | None
    mean_expansions: float | None
    median_path_length_m: float | None
    trunk_count: int
    trunk_gap_m: float
    gap_to_vehicle_width: float
    tree_density_per_100m2: float | None
    obstacle_ratio_mean: float | None
    distance_min_m: float | None
    distance_max_m: float | None
    difficulty_bucket: str


@dataclass(frozen=True)
class CalibrationRun:
    config: CalibrationConfig
    maps: tuple[CalibrationMapRecord, ...]
    queries: tuple[CalibrationRecord, ...]
    summary: dict[str, Any]


def default_density_levels() -> tuple[DensityLevel, ...]:
    return (
        DensityLevel(key="d00", order=0, trunk_count=40, trunk_gap_m=1.35, trunk_gap_jitter=0.20),
        DensityLevel(key="d01", order=1, trunk_count=55, trunk_gap_m=1.25, trunk_gap_jitter=0.20),
        DensityLevel(key="d02", order=2, trunk_count=70, trunk_gap_m=1.15, trunk_gap_jitter=0.22),
        DensityLevel(key="d03", order=3, trunk_count=85, trunk_gap_m=1.05, trunk_gap_jitter=0.24),
        DensityLevel(key="d04", order=4, trunk_count=100, trunk_gap_m=0.95, trunk_gap_jitter=0.25),
        DensityLevel(key="d05", order=5, trunk_count=115, trunk_gap_m=0.90, trunk_gap_jitter=0.25),
        DensityLevel(key="d06", order=6, trunk_count=130, trunk_gap_m=0.85, trunk_gap_jitter=0.25),
        DensityLevel(key="d07", order=7, trunk_count=145, trunk_gap_m=0.80, trunk_gap_jitter=0.25),
    )


def default_distance_bins() -> tuple[DistanceBin, ...]:
    return parse_distance_bins("4:8,8:12,12:16,16:20,20:")


def parse_distance_bins(spec: str) -> tuple[DistanceBin, ...]:
    bins: list[DistanceBin] = []
    for order, raw_part in enumerate(part.strip() for part in spec.split(",") if part.strip()):
        if ":" not in raw_part:
            raise ValueError(f"distance bin must use min:max syntax: {raw_part!r}")
        raw_min, raw_max = raw_part.split(":", 1)
        if not raw_min:
            raise ValueError(f"distance bin has empty minimum: {raw_part!r}")
        min_distance_m = float(raw_min)
        max_distance_m = float(raw_max) if raw_max else None
        if max_distance_m is not None and max_distance_m <= min_distance_m:
            raise ValueError(f"distance bin max must exceed min: {raw_part!r}")
        max_key = "inf" if max_distance_m is None else f"{int(round(max_distance_m)):02d}"
        key = f"d{int(round(min_distance_m)):02d}_{max_key}"
        bins.append(
            DistanceBin(
                key=key,
                order=order,
                min_distance_m=min_distance_m,
                max_distance_m=max_distance_m,
            )
        )
    if not bins:
        raise ValueError("distance bin specification must not be empty")
    return tuple(bins)


def sample_query_in_distance_bin(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    *,
    rng: np.random.Generator,
    distance_bin: DistanceBin,
    max_attempts: int,
) -> tuple[Pose, Pose]:
    free = np.argwhere(np.asarray(grid_map.data) == 0)
    if len(free) < 2:
        raise RuntimeError("map has fewer than two free cells")

    checker = GridFootprintChecker(grid_map, footprint, theta_bins=72)
    for _attempt in range(int(max_attempts)):
        a_idx = int(rng.integers(0, len(free)))
        b_idx = int(rng.integers(0, len(free)))
        if a_idx == b_idx:
            continue

        ay, ax = (int(v) for v in free[a_idx])
        by, bx = (int(v) for v in free[b_idx])
        sx, sy = grid_map.grid_to_world(ax, ay)
        gx, gy = grid_map.grid_to_world(bx, by)
        dx = float(gx) - float(sx)
        dy = float(gy) - float(sy)
        distance = math.hypot(dx, dy)
        if distance < float(distance_bin.min_distance_m):
            continue
        if distance_bin.max_distance_m is not None and distance >= float(distance_bin.max_distance_m):
            continue

        heading = math.atan2(dy, dx)
        start = (float(sx), float(sy), float(heading))
        goal = (float(gx), float(gy), float(heading))
        if checker.collides_pose(*start):
            continue
        if checker.collides_pose(*goal):
            continue
        return start, goal

    raise RuntimeError(f"failed to sample a query in distance bin {distance_bin.label}")


def run_difficulty_calibration(config: CalibrationConfig) -> CalibrationRun:
    _validate_config(config)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    maps: list[CalibrationMapRecord] = []
    queries: list[CalibrationRecord] = []
    map_id = 0

    for level in config.density_levels:
        for map_rep in range(int(config.maps_per_density)):
            map_seed = int(config.seed) + 20_000 + int(level.order) * 1_000 + int(map_rep)
            grid, map_record = _generate_map(
                axis="density",
                level=level,
                map_id=map_id,
                map_seed=map_seed,
                config=config,
                footprint=footprint,
            )
            maps.append(map_record)
            if grid is not None:
                grid_map = GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0))
                planner = _make_planner(grid_map, footprint, config)
                for query_id in range(int(config.queries_per_map)):
                    query_seed = int(config.seed) + 30_000 + int(level.order) * 10_000 + map_rep * 100 + query_id
                    queries.append(
                        _run_density_query(
                            level=level,
                            map_id=map_id,
                            query_id=query_id,
                            map_seed=map_seed,
                            query_seed=query_seed,
                            grid_map=grid_map,
                            footprint=footprint,
                            planner=planner,
                            obstacle_ratio=float(map_record.obstacle_ratio),
                            config=config,
                        )
                    )
            map_id += 1

    distance_level = config.distance_reference_level
    for map_rep in range(int(config.distance_map_count)):
        map_seed = int(config.seed) + 50_000 + int(map_rep)
        grid, map_record = _generate_map(
            axis="distance",
            level=distance_level,
            map_id=map_id,
            map_seed=map_seed,
            config=config,
            footprint=footprint,
        )
        maps.append(map_record)
        if grid is not None:
            grid_map = GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0))
            planner = _make_planner(grid_map, footprint, config)
            for distance_bin in config.distance_bins:
                for query_rep in range(int(config.queries_per_distance_bin)):
                    query_id = int(distance_bin.order) * int(config.queries_per_distance_bin) + query_rep
                    query_seed = (
                        int(config.seed)
                        + 60_000
                        + map_rep * 10_000
                        + int(distance_bin.order) * 1_000
                        + query_rep
                    )
                    queries.append(
                        _run_distance_query(
                            distance_bin=distance_bin,
                            level=distance_level,
                            map_id=map_id,
                            query_id=query_id,
                            map_seed=map_seed,
                            query_seed=query_seed,
                            grid_map=grid_map,
                            footprint=footprint,
                            planner=planner,
                            obstacle_ratio=float(map_record.obstacle_ratio),
                            config=config,
                        )
                    )
        map_id += 1

    density_raw_summaries = summarize_axis(queries, axis="density", rule=config.bucket_rule)
    distance_raw_summaries = summarize_axis(queries, axis="distance", rule=config.bucket_rule)
    density_cutpoints = choose_axis_cutpoints(density_raw_summaries, config.bucket_rule)
    distance_cutpoints = choose_axis_cutpoints(distance_raw_summaries, config.bucket_rule)
    density_summaries = density_cutpoints["level_summaries"]
    distance_summaries = distance_cutpoints["level_summaries"]

    summary = {
        "map_count": len(maps),
        "generated_map_count": sum(1 for item in maps if item.generated),
        "map_generation_failure_count": sum(1 for item in maps if not item.generated),
        "total_queries": len(queries),
        "density_query_count": sum(1 for item in queries if item.axis == "density"),
        "distance_query_count": sum(1 for item in queries if item.axis == "distance"),
        "bucket_rule": asdict(config.bucket_rule),
        "density_summaries": density_summaries,
        "distance_summaries": distance_summaries,
        "density_cutpoints": density_cutpoints,
        "distance_cutpoints": distance_cutpoints,
        "bucket_separation_pass": bool(
            density_cutpoints.get("bucket_separation_pass")
            and distance_cutpoints.get("bucket_separation_pass")
        ),
    }
    return CalibrationRun(config=config, maps=tuple(maps), queries=tuple(queries), summary=summary)


def summarize_axis(
    records: Sequence[CalibrationRecord],
    *,
    axis: str,
    rule: BucketRule | None = None,
) -> list[LevelSummary]:
    selected = [record for record in records if record.axis == axis]
    summaries: list[LevelSummary] = []
    for level_key in sorted({record.level_key for record in selected}, key=lambda k: _level_order(selected, k)):
        subset = [record for record in selected if record.level_key == level_key]
        attempted = [record for record in subset if record.query_sampled]
        success = [record for record in attempted if record.teacher_success]
        time_values = [float(record.teacher_time_s) for record in attempted]
        expansion_values = [float(record.teacher_expansions) for record in attempted]
        path_values = [float(record.teacher_path_length_m) for record in success]
        timeout_count = sum(1 for record in attempted if record.timed_out or record.teacher_failure_reason == "timeout")
        bucket = _classify_bucket(
            success_rate=_ratio(len(success), len(attempted)),
            timeout_rate=_ratio(timeout_count, len(attempted)),
            median_time_s=_percentile(time_values, 50.0),
            rule=rule or BucketRule(),
        )
        first = subset[0]
        tree_density_values = [
            float(record.tree_density_per_100m2)
            for record in subset
            if record.tree_density_per_100m2 is not None
        ]
        summaries.append(
            LevelSummary(
                axis=axis,
                level_key=level_key,
                level_order=int(first.level_order),
                level_label=str(first.level_label),
                query_count=len(subset),
                planner_attempt_count=len(attempted),
                success_count=len(success),
                success_rate=_ratio(len(success), len(attempted)),
                timeout_count=timeout_count,
                timeout_rate=_ratio(timeout_count, len(attempted)),
                median_time_s=_percentile(time_values, 50.0),
                p95_time_s=_percentile(time_values, 95.0),
                mean_time_s=_mean(time_values),
                median_expansions=_percentile(expansion_values, 50.0),
                p95_expansions=_percentile(expansion_values, 95.0),
                mean_expansions=_mean(expansion_values),
                median_path_length_m=_percentile(path_values, 50.0),
                trunk_count=int(first.trunk_count),
                trunk_gap_m=float(first.trunk_gap_m),
                gap_to_vehicle_width=float(first.gap_to_vehicle_width),
                tree_density_per_100m2=_mean(tree_density_values),
                obstacle_ratio_mean=_mean([float(record.obstacle_ratio) for record in subset]),
                distance_min_m=first.distance_min_m,
                distance_max_m=first.distance_max_m,
                difficulty_bucket=bucket,
            )
        )
    return sorted(summaries, key=lambda item: item.level_order)


def choose_axis_cutpoints(summaries: Sequence[LevelSummary], rule: BucketRule | None = None) -> dict[str, Any]:
    rule = rule or BucketRule()
    ordered = sorted(summaries, key=lambda item: item.level_order)
    easy_candidates = [item for item in ordered if _summary_meets_easy(item, rule)]
    easy_ref = easy_candidates[-1] if easy_candidates else None
    after_easy = [item for item in ordered if easy_ref is None or item.level_order > easy_ref.level_order]
    extreme_candidates = [item for item in after_easy if _summary_meets_extreme(item, rule)]
    extreme_ref = extreme_candidates[0] if extreme_candidates else None

    bucketed = _assign_monotonic_buckets(ordered, easy_ref=easy_ref, extreme_ref=extreme_ref, rule=rule)
    easy = [item for item in bucketed if item.difficulty_bucket == "Easy"]
    complex_items = [item for item in bucketed if item.difficulty_bucket == "Complex"]
    extreme = [item for item in bucketed if item.difficulty_bucket == "Extreme"]
    easy_ref = easy[-1] if easy else None
    complex_min = complex_items[0] if complex_items else None
    complex_max = complex_items[-1] if complex_items else None
    extreme_ref = extreme[0] if extreme else None

    order_pass = bool(
        easy_ref is not None
        and complex_min is not None
        and extreme_ref is not None
        and easy_ref.level_order < complex_min.level_order <= complex_max.level_order < extreme_ref.level_order
    )
    metrics = _separation_metrics(easy_ref, complex_min, extreme_ref)
    metric_pass = bool(
        metrics["success_rate_gap_easy_to_extreme"] is not None
        and metrics["success_rate_gap_easy_to_extreme"] >= rule.min_success_rate_gap_easy_to_extreme
        and (
            (
                metrics["complex_to_easy_median_time_ratio"] is not None
                and metrics["complex_to_easy_median_time_ratio"] >= rule.min_complex_to_easy_time_ratio
            )
            or (
                metrics["complex_to_easy_median_expansion_ratio"] is not None
                and metrics["complex_to_easy_median_expansion_ratio"] >= rule.min_complex_to_easy_time_ratio
            )
            or (
                metrics["complex_to_easy_p95_time_ratio"] is not None
                and metrics["complex_to_easy_p95_time_ratio"] >= rule.min_complex_to_easy_p95_time_ratio
            )
            or (
                metrics["complex_to_easy_p95_expansion_ratio"] is not None
                and metrics["complex_to_easy_p95_expansion_ratio"] >= rule.min_complex_to_easy_p95_expansion_ratio
            )
            or (
                metrics["timeout_rate_gap_complex_to_easy"] is not None
                and metrics["timeout_rate_gap_complex_to_easy"] >= rule.min_timeout_rate_gap_easy_to_complex
            )
        )
        and (
            (
                metrics["extreme_to_easy_median_time_ratio"] is not None
                and metrics["extreme_to_easy_median_time_ratio"] >= rule.min_extreme_to_easy_time_ratio
            )
            or (
                metrics["extreme_to_easy_median_expansion_ratio"] is not None
                and metrics["extreme_to_easy_median_expansion_ratio"] >= rule.min_extreme_to_easy_expansion_ratio
            )
            or (
                metrics["extreme_to_easy_p95_time_ratio"] is not None
                and metrics["extreme_to_easy_p95_time_ratio"] >= rule.min_extreme_to_easy_p95_time_ratio
            )
            or (
                metrics["extreme_to_easy_p95_expansion_ratio"] is not None
                and metrics["extreme_to_easy_p95_expansion_ratio"] >= rule.min_extreme_to_easy_expansion_ratio
            )
        )
    )

    return {
        "axis": ordered[0].axis if ordered else "unknown",
        "bucket_separation_pass": bool(order_pass and metric_pass),
        "order_pass": order_pass,
        "metric_pass": metric_pass,
        "easy_max": asdict(easy_ref) if easy_ref is not None else None,
        "complex_range": {
            "min": asdict(complex_min) if complex_min is not None else None,
            "max": asdict(complex_max) if complex_max is not None else None,
        },
        "extreme_min": asdict(extreme_ref) if extreme_ref is not None else None,
        "bucket_counts": {
            "Easy": len(easy),
            "Complex": len(complex_items),
            "Extreme": len(extreme),
            "NoData": len([item for item in ordered if item.difficulty_bucket == "NoData"]),
        },
        "separation_metrics": metrics,
        "level_summaries": [asdict(item) for item in bucketed],
    }


def write_calibration_outputs(
    run: CalibrationRun,
    output_dir: Path,
    *,
    source_head: str,
    execution_host: str,
    supplement_path: Path | None = None,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    maps_csv = output_dir / "maps.csv"
    queries_csv = output_dir / "queries.csv"
    density_summary_csv = output_dir / "density_summary.csv"
    distance_summary_csv = output_dir / "distance_summary.csv"
    summary_json = output_dir / "summary.json"
    report_md = output_dir / "report.md"
    local_supplement_md = output_dir / "contract_supplement.md"

    write_csv(maps_csv, run.maps)
    write_csv(queries_csv, run.queries)
    write_csv(
        density_summary_csv,
        [LevelSummary(**item) for item in run.summary["density_summaries"]],
    )
    write_csv(
        distance_summary_csv,
        [LevelSummary(**item) for item in run.summary["distance_summaries"]],
    )

    summary_payload = {
        "source_head": source_head,
        "execution_host": execution_host,
        "config": _json_safe_dict(asdict(run.config)),
        "summary": _json_safe_dict(run.summary),
        "files": {
            "maps_csv": str(maps_csv),
            "queries_csv": str(queries_csv),
            "density_summary_csv": str(density_summary_csv),
            "distance_summary_csv": str(distance_summary_csv),
            "summary_json": str(summary_json),
            "report_md": str(report_md),
            "contract_supplement_md": str(local_supplement_md),
        },
    }
    if supplement_path is not None:
        summary_payload["files"]["supplement_path"] = str(supplement_path)

    summary_json.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    report_text = render_report(summary_payload)
    report_md.write_text(report_text, encoding="utf-8")
    supplement_text = render_contract_supplement(summary_payload)
    local_supplement_md.write_text(supplement_text, encoding="utf-8")
    if supplement_path is not None:
        supplement_path.parent.mkdir(parents=True, exist_ok=True)
        supplement_path.write_text(supplement_text, encoding="utf-8")

    return {
        "maps_csv": str(maps_csv),
        "queries_csv": str(queries_csv),
        "density_summary_csv": str(density_summary_csv),
        "distance_summary_csv": str(distance_summary_csv),
        "summary_json": str(summary_json),
        "report_md": str(report_md),
        "contract_supplement_md": str(local_supplement_md),
        "supplement_path": str(supplement_path) if supplement_path is not None else "",
    }


def write_csv(path: Path, rows: Iterable[Any]) -> None:
    rows = tuple(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            raw = asdict(row)
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False) if isinstance(value, (tuple, list, dict)) else value
                    for key, value in raw.items()
                }
            )


def render_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    config = payload["config"]
    density_pass = bool(summary["density_cutpoints"]["bucket_separation_pass"])
    distance_pass = bool(summary["distance_cutpoints"]["bucket_separation_pass"])
    status = "pass" if density_pass and distance_pass else "needs_review"
    lines = [
        "---",
        "date: 2026-06-20",
        f"status: {status}",
        "origin: ai+experiment",
        "reviewed: false",
        "contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_head: {payload['source_head']}",
        f"execution_host: {payload['execution_host']}",
        "---",
        "",
        "# T06 难度轴标定报告",
        "",
        "## 目的",
        "",
        "用原版 Hybrid A* 在程序化森林中标定 Easy/Complex/Extreme 难度桶。密度轴至少覆盖 8 个级别；距离轴在中等密度参考森林中单独改变起终欧氏距离。统计口径为规划器实测时间、节点扩展数、成功率和超时率。",
        "",
        "## 实验设置",
        "",
        "```text",
        f"seed={config['seed']}",
        f"map_size_cells={config['width_cells']}x{config['height_cells']}",
        f"resolution_m={config['resolution_m']}",
        f"maps_per_density={config['maps_per_density']}",
        f"queries_per_map={config['queries_per_map']}",
        f"distance_map_count={config['distance_map_count']}",
        f"queries_per_distance_bin={config['queries_per_distance_bin']}",
        f"teacher_timeout_s={config['teacher_timeout_s']}",
        f"teacher_max_nodes={config['teacher_max_nodes']}",
        f"easy_success_rate_min={config['bucket_rule']['easy_success_rate_min']}",
        f"easy_median_time_s_max={config['bucket_rule']['easy_median_time_s_max']}",
        f"easy_timeout_rate_max={config['bucket_rule']['easy_timeout_rate_max']}",
        f"extreme_success_rate_max={config['bucket_rule']['extreme_success_rate_max']}",
        f"extreme_timeout_rate_min={config['bucket_rule']['extreme_timeout_rate_min']}",
        f"extreme_success_rate_hard_max={config['bucket_rule']['extreme_success_rate_hard_max']}",
        f"extreme_timeout_rate_hard_min={config['bucket_rule']['extreme_timeout_rate_hard_min']}",
        "```",
        "",
        "分桶采用轴向单调切点，而不是逐级独立标签：先用固定规则寻找 Easy 前缀上界和 Extreme 后缀下界，然后将两者之间的级别归为 Complex。这样可以降低有限随机查询造成的非单调噪声，但所有原始级别统计仍完整保留在表格和 CSV 中。",
        "",
        "## 密度轴结果",
        "",
        "| 级别 | 桶 | 树数 | 约树密度(/100m²) | gap/车宽 | 查询 | 成功率 | 超时率 | 中位时间(s) | P95时间(s) | 中位扩展 | P95扩展 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in summary["density_summaries"]:
        lines.append(_summary_row(item))

    lines.extend(
        [
            "",
            "## 距离轴结果",
            "",
            "| 距离桶 | 桶 | 树数 | 约树密度(/100m²) | gap/车宽 | 查询 | 成功率 | 超时率 | 中位时间(s) | P95时间(s) | 中位扩展 | P95扩展 |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in summary["distance_summaries"]:
        lines.append(_summary_row(item))

    lines.extend(
        [
            "",
            "## 切点草案",
            "",
            "### 密度轴",
            "",
            _cutpoint_text(summary["density_cutpoints"]),
            "",
            "### 距离轴",
            "",
            _cutpoint_text(summary["distance_cutpoints"]),
            "",
            "## 验收判断",
            "",
            f"- 密度轴三桶区分度：{'通过' if density_pass else '需复核'}。",
            f"- 距离轴三桶区分度：{'通过' if distance_pass else '需复核'}。",
            "- 本报告给出预注册补充草案；由于父 Contract 已 approved，本次不直接改写父 Contract。",
            "",
            "## 产物",
            "",
            f"- `maps.csv`: `{payload['files']['maps_csv']}`",
            f"- `queries.csv`: `{payload['files']['queries_csv']}`",
            f"- `density_summary.csv`: `{payload['files']['density_summary_csv']}`",
            f"- `distance_summary.csv`: `{payload['files']['distance_summary_csv']}`",
            f"- `summary.json`: `{payload['files']['summary_json']}`",
            f"- `contract_supplement.md`: `{payload['files']['contract_supplement_md']}`",
        ]
    )
    if payload["files"].get("supplement_path"):
        lines.append(f"- 预注册补充草案: `{payload['files']['supplement_path']}`")
    return "\n".join(lines) + "\n"


def render_contract_supplement(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    density = summary["density_cutpoints"]
    distance = summary["distance_cutpoints"]
    lines = [
        "---",
        "origin: ai+experiment",
        "reviewed: false",
        "date: 2026-06-20",
        "status: draft-for-review",
        "parent_contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_report: {payload['files']['report_md']}",
        f"source_head: {payload['source_head']}",
        f"execution_host: {payload['execution_host']}",
        "---",
        "",
        "# T06 难度轴预注册补充草案",
        "",
        "本文件是 T06 标定产物，不修改已 approved 的父 Contract。只有 Dr Sun 人工确认后，后续 T08/T14 才应把这些切点作为正式难度桶依据。",
        "",
        "## 固定判定规则",
        "",
        "```json",
        json.dumps(summary["bucket_rule"], indent=2, ensure_ascii=False),
        "```",
        "",
        "这些规则用于寻找轴向单调切点：低于 Easy 上界的级别归入 Easy，高于 Extreme 下界的级别归入 Extreme，中间归入 Complex。单个级别的偶发 timeout 不会单独推翻其所在前缀/后缀，但所有原始统计必须随报告保留。",
        "",
        "## 密度轴切点草案",
        "",
        _cutpoint_text(density),
        "",
        "## 起终距离轴切点草案",
        "",
        _cutpoint_text(distance),
        "",
        "## 使用限制",
        "",
        "- 密度轴同时改变树干数量和目标树间隙，因此 `gap/车宽` 是伴随变量，不是独立单因子实验。",
        "- 距离轴固定在中等密度参考森林中运行，用于隔离起终欧氏距离影响。",
        "- `reviewed:false` 期间只能作为实验线索，不能作为论文 claim 的已确认依据。",
    ]
    return "\n".join(lines) + "\n"


def _run_density_query(
    *,
    level: DensityLevel,
    map_id: int,
    query_id: int,
    map_seed: int,
    query_seed: int,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    planner: Any,
    obstacle_ratio: float,
    config: CalibrationConfig,
) -> CalibrationRecord:
    rng = np.random.default_rng(query_seed)
    try:
        start, goal = _sample_min_distance_query(
            grid_map,
            footprint,
            rng=rng,
            min_distance_m=float(config.density_min_query_distance_m),
            max_attempts=int(config.max_query_sample_attempts),
        )
    except Exception as exc:  # noqa: BLE001
        return _sampling_failure_record(
            axis="density",
            level=level,
            map_id=map_id,
            query_id=query_id,
            map_seed=map_seed,
            query_seed=query_seed,
            obstacle_ratio=obstacle_ratio,
            distance_min_m=float(config.density_min_query_distance_m),
            distance_max_m=None,
            failure_reason=f"query_sampling_failed:{type(exc).__name__}",
            config=config,
        )
    return _plan_record(
        axis="density",
        level_key=level.key,
        level_order=level.order,
        level_label=level.label,
        level=level,
        map_id=map_id,
        query_id=query_id,
        map_seed=map_seed,
        query_seed=query_seed,
        obstacle_ratio=obstacle_ratio,
        distance_min_m=float(config.density_min_query_distance_m),
        distance_max_m=None,
        start=start,
        goal=goal,
        planner=planner,
        config=config,
    )


def _run_distance_query(
    *,
    distance_bin: DistanceBin,
    level: DensityLevel,
    map_id: int,
    query_id: int,
    map_seed: int,
    query_seed: int,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    planner: Any,
    obstacle_ratio: float,
    config: CalibrationConfig,
) -> CalibrationRecord:
    rng = np.random.default_rng(query_seed)
    try:
        start, goal = sample_query_in_distance_bin(
            grid_map,
            footprint,
            rng=rng,
            distance_bin=distance_bin,
            max_attempts=int(config.max_query_sample_attempts),
        )
    except Exception as exc:  # noqa: BLE001
        return _sampling_failure_record(
            axis="distance",
            level=level,
            map_id=map_id,
            query_id=query_id,
            map_seed=map_seed,
            query_seed=query_seed,
            obstacle_ratio=obstacle_ratio,
            distance_min_m=float(distance_bin.min_distance_m),
            distance_max_m=distance_bin.max_distance_m,
            failure_reason=f"query_sampling_failed:{type(exc).__name__}",
            config=config,
            level_key=distance_bin.key,
            level_order=distance_bin.order,
            level_label=distance_bin.label,
        )
    return _plan_record(
        axis="distance",
        level_key=distance_bin.key,
        level_order=distance_bin.order,
        level_label=distance_bin.label,
        level=level,
        map_id=map_id,
        query_id=query_id,
        map_seed=map_seed,
        query_seed=query_seed,
        obstacle_ratio=obstacle_ratio,
        distance_min_m=float(distance_bin.min_distance_m),
        distance_max_m=distance_bin.max_distance_m,
        start=start,
        goal=goal,
        planner=planner,
        config=config,
    )


def _generate_map(
    *,
    axis: str,
    level: DensityLevel,
    map_id: int,
    map_seed: int,
    config: CalibrationConfig,
    footprint: TwoCircleFootprint,
) -> tuple[np.ndarray | None, CalibrationMapRecord]:
    rng = np.random.default_rng(map_seed)
    started = time.perf_counter()
    grid = None
    failure_reason = None
    try:
        profile = DifficultyProfile(
            name=level.key,
            trunk_count=int(level.trunk_count),
            trunk_gap_m=float(level.trunk_gap_m),
            trunk_gap_jitter=float(level.trunk_gap_jitter),
            bush_cluster_count=int(level.bush_cluster_count),
        )
        params = make_forest_params(profile, config)
        grid, _start_xy, _goal_xy = generate_forest_grid(
            params=params,
            rng=rng,
            footprint_clearance_m=footprint_clearance_m(resolution_m=float(config.resolution_m)),
        )
        generated = True
    except Exception as exc:  # noqa: BLE001
        generated = False
        failure_reason = f"{type(exc).__name__}: {exc}"

    generation_time_s = time.perf_counter() - started
    obstacle_ratio = float(np.mean(grid)) if grid is not None else 0.0
    return grid, CalibrationMapRecord(
        axis=axis,
        level_key=level.key,
        level_order=int(level.order),
        level_label=level.label,
        map_id=map_id,
        map_seed=map_seed,
        generated=generated,
        generation_time_s=float(generation_time_s),
        trunk_count=int(level.trunk_count),
        trunk_gap_m=float(level.trunk_gap_m),
        gap_to_vehicle_width=float(level.gap_to_vehicle_width),
        obstacle_ratio=obstacle_ratio,
        failure_reason=failure_reason,
    )


def _sample_min_distance_query(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    *,
    rng: np.random.Generator,
    min_distance_m: float,
    max_attempts: int,
) -> tuple[Pose, Pose]:
    return sample_query_in_distance_bin(
        grid_map,
        footprint,
        rng=rng,
        distance_bin=DistanceBin(key="density_min_distance", order=0, min_distance_m=min_distance_m, max_distance_m=None),
        max_attempts=max_attempts,
    )


def _plan_record(
    *,
    axis: str,
    level_key: str,
    level_order: int,
    level_label: str,
    level: DensityLevel,
    map_id: int,
    query_id: int,
    map_seed: int,
    query_seed: int,
    obstacle_ratio: float,
    distance_min_m: float | None,
    distance_max_m: float | None,
    start: Pose,
    goal: Pose,
    planner: Any,
    config: CalibrationConfig,
) -> CalibrationRecord:
    path, stats = planner.plan(
        AckermannState(*start),
        AckermannState(*goal),
        timeout=float(config.teacher_timeout_s),
        max_nodes=int(config.teacher_max_nodes),
    )
    teacher_success = bool(path)
    teacher_failure_reason = None if teacher_success else str(stats.get("failure_reason", "unknown"))
    return CalibrationRecord(
        axis=axis,
        level_key=level_key,
        level_order=int(level_order),
        level_label=level_label,
        map_id=map_id,
        query_id=query_id,
        map_seed=map_seed,
        query_seed=query_seed,
        trunk_count=int(level.trunk_count),
        trunk_gap_m=float(level.trunk_gap_m),
        gap_to_vehicle_width=float(level.gap_to_vehicle_width),
        obstacle_ratio=float(obstacle_ratio),
        distance_min_m=distance_min_m,
        distance_max_m=distance_max_m,
        start=start,
        goal=goal,
        euclidean_distance_m=math.hypot(float(goal[0]) - float(start[0]), float(goal[1]) - float(start[1])),
        teacher_success=teacher_success,
        teacher_failure_reason=teacher_failure_reason,
        teacher_time_s=float(stats.get("time", 0.0)),
        teacher_expansions=int(stats.get("expansions", 0)),
        teacher_path_length_m=float(stats.get("path_length", 0.0)),
        timed_out=bool(stats.get("timed_out", False)),
        query_sampled=True,
        tree_density_per_100m2=_tree_density_per_100m2(level.trunk_count, config),
    )


def _sampling_failure_record(
    *,
    axis: str,
    level: DensityLevel,
    map_id: int,
    query_id: int,
    map_seed: int,
    query_seed: int,
    obstacle_ratio: float,
    distance_min_m: float | None,
    distance_max_m: float | None,
    failure_reason: str,
    config: CalibrationConfig,
    level_key: str | None = None,
    level_order: int | None = None,
    level_label: str | None = None,
) -> CalibrationRecord:
    return CalibrationRecord(
        axis=axis,
        level_key=level_key or level.key,
        level_order=int(level.order if level_order is None else level_order),
        level_label=level_label or level.label,
        map_id=map_id,
        query_id=query_id,
        map_seed=map_seed,
        query_seed=query_seed,
        trunk_count=int(level.trunk_count),
        trunk_gap_m=float(level.trunk_gap_m),
        gap_to_vehicle_width=float(level.gap_to_vehicle_width),
        obstacle_ratio=float(obstacle_ratio),
        distance_min_m=distance_min_m,
        distance_max_m=distance_max_m,
        start=(math.nan, math.nan, math.nan),
        goal=(math.nan, math.nan, math.nan),
        euclidean_distance_m=math.nan,
        teacher_success=False,
        teacher_failure_reason=failure_reason,
        teacher_time_s=0.0,
        teacher_expansions=0,
        teacher_path_length_m=0.0,
        timed_out=False,
        query_sampled=False,
        tree_density_per_100m2=_tree_density_per_100m2(level.trunk_count, config),
    )


def _classify_bucket(
    *,
    success_rate: float | None,
    timeout_rate: float | None,
    median_time_s: float | None,
    rule: BucketRule,
) -> str:
    if success_rate is None or timeout_rate is None or median_time_s is None:
        return "NoData"
    if (
        success_rate >= rule.easy_success_rate_min
        and median_time_s <= rule.easy_median_time_s_max
        and timeout_rate <= rule.easy_timeout_rate_max
    ):
        return "Easy"
    if (
        (success_rate <= rule.extreme_success_rate_max and timeout_rate >= rule.extreme_timeout_rate_min)
        or success_rate <= rule.extreme_success_rate_hard_max
        or timeout_rate >= rule.extreme_timeout_rate_hard_min
    ):
        return "Extreme"
    return "Complex"


def _summary_meets_easy(item: LevelSummary, rule: BucketRule) -> bool:
    return _classify_bucket(
        success_rate=item.success_rate,
        timeout_rate=item.timeout_rate,
        median_time_s=item.median_time_s,
        rule=rule,
    ) == "Easy"


def _summary_meets_extreme(item: LevelSummary, rule: BucketRule) -> bool:
    return _classify_bucket(
        success_rate=item.success_rate,
        timeout_rate=item.timeout_rate,
        median_time_s=item.median_time_s,
        rule=rule,
    ) == "Extreme"


def _assign_monotonic_buckets(
    ordered: Sequence[LevelSummary],
    *,
    easy_ref: LevelSummary | None,
    extreme_ref: LevelSummary | None,
    rule: BucketRule,
) -> list[LevelSummary]:
    out: list[LevelSummary] = []
    for item in ordered:
        if item.planner_attempt_count <= 0:
            bucket = "NoData"
        elif easy_ref is not None and item.level_order <= easy_ref.level_order:
            bucket = "Easy"
        elif extreme_ref is not None and item.level_order >= extreme_ref.level_order:
            bucket = "Extreme"
        elif easy_ref is not None and extreme_ref is not None and easy_ref.level_order < item.level_order < extreme_ref.level_order:
            bucket = "Complex"
        else:
            bucket = _classify_bucket(
                success_rate=item.success_rate,
                timeout_rate=item.timeout_rate,
                median_time_s=item.median_time_s,
                rule=rule,
            )
        out.append(replace(item, difficulty_bucket=bucket))
    return out


def _separation_metrics(
    easy_ref: LevelSummary | None,
    complex_ref: LevelSummary | None,
    extreme_ref: LevelSummary | None,
) -> dict[str, float | None]:
    if easy_ref is None or complex_ref is None or extreme_ref is None:
        return {
            "success_rate_gap_easy_to_extreme": None,
            "timeout_rate_gap_complex_to_easy": None,
            "complex_to_easy_median_time_ratio": None,
            "extreme_to_easy_median_time_ratio": None,
            "complex_to_easy_p95_time_ratio": None,
            "extreme_to_easy_p95_time_ratio": None,
            "complex_to_easy_median_expansion_ratio": None,
            "complex_to_easy_p95_expansion_ratio": None,
            "extreme_to_easy_median_expansion_ratio": None,
            "extreme_to_easy_p95_expansion_ratio": None,
        }
    return {
        "success_rate_gap_easy_to_extreme": _safe_gap(easy_ref.success_rate, extreme_ref.success_rate),
        "timeout_rate_gap_complex_to_easy": _safe_gap(complex_ref.timeout_rate, easy_ref.timeout_rate),
        "complex_to_easy_median_time_ratio": _safe_ratio(complex_ref.median_time_s, easy_ref.median_time_s),
        "extreme_to_easy_median_time_ratio": _safe_ratio(extreme_ref.median_time_s, easy_ref.median_time_s),
        "complex_to_easy_p95_time_ratio": _safe_ratio(complex_ref.p95_time_s, easy_ref.p95_time_s),
        "extreme_to_easy_p95_time_ratio": _safe_ratio(extreme_ref.p95_time_s, easy_ref.p95_time_s),
        "complex_to_easy_median_expansion_ratio": _safe_ratio(complex_ref.median_expansions, easy_ref.median_expansions),
        "complex_to_easy_p95_expansion_ratio": _safe_ratio(complex_ref.p95_expansions, easy_ref.p95_expansions),
        "extreme_to_easy_median_expansion_ratio": _safe_ratio(extreme_ref.median_expansions, easy_ref.median_expansions),
        "extreme_to_easy_p95_expansion_ratio": _safe_ratio(extreme_ref.p95_expansions, easy_ref.p95_expansions),
    }


def _summary_row(item: dict[str, Any]) -> str:
    return (
        "| "
        f"{item['level_label']} | "
        f"{item['difficulty_bucket']} | "
        f"{item['trunk_count']} | "
        f"{_fmt_number(item['tree_density_per_100m2'])} | "
        f"{_fmt_number(item['gap_to_vehicle_width'])} | "
        f"{item['planner_attempt_count']} | "
        f"{_fmt_rate(item['success_rate'])} | "
        f"{_fmt_rate(item['timeout_rate'])} | "
        f"{_fmt_number(item['median_time_s'])} | "
        f"{_fmt_number(item['p95_time_s'])} | "
        f"{_fmt_number(item['median_expansions'])} | "
        f"{_fmt_number(item['p95_expansions'])} |"
    )


def _cutpoint_text(cutpoints: dict[str, Any]) -> str:
    easy = cutpoints.get("easy_max")
    complex_range = cutpoints.get("complex_range", {})
    extreme = cutpoints.get("extreme_min")
    lines = [
        f"- 区分度结论：{'通过' if cutpoints.get('bucket_separation_pass') else '需复核'}。",
        f"- Easy 上界：{_brief_level(easy)}。",
        f"- Complex 范围：{_brief_level(complex_range.get('min'))} 到 {_brief_level(complex_range.get('max'))}。",
        f"- Extreme 下界：{_brief_level(extreme)}。",
        f"- 分桶数量：{json.dumps(cutpoints.get('bucket_counts', {}), ensure_ascii=False)}。",
    ]
    return "\n".join(lines)


def _brief_level(item: dict[str, Any] | None) -> str:
    if item is None:
        return "N/A"
    return (
        f"{item['level_label']} "
        f"(成功率={_fmt_rate(item['success_rate'])}, "
        f"中位时间={_fmt_number(item['median_time_s'])}s, "
        f"中位扩展={_fmt_number(item['median_expansions'])})"
    )


def _validate_config(config: CalibrationConfig) -> None:
    if len(config.density_levels) < 8:
        raise ValueError("T06 requires at least 8 density levels")
    if config.maps_per_density <= 0:
        raise ValueError("maps_per_density must be positive")
    if config.queries_per_map <= 0:
        raise ValueError("queries_per_map must be positive")
    if config.distance_map_count <= 0:
        raise ValueError("distance_map_count must be positive")
    if config.queries_per_distance_bin <= 0:
        raise ValueError("queries_per_distance_bin must be positive")
    if not config.distance_bins:
        raise ValueError("distance_bins must not be empty")


def _level_order(records: Sequence[CalibrationRecord], level_key: str) -> int:
    return min(record.level_order for record in records if record.level_key == level_key)


def _ratio(num: int, den: int) -> float | None:
    if den <= 0:
        return None
    return float(num) / float(den)


def _mean(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return float(np.mean(np.asarray(values, dtype=np.float64)))


def _percentile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.percentile(np.asarray(values, dtype=np.float64), q))


def _safe_ratio(num: float | None, den: float | None) -> float | None:
    if num is None or den is None or abs(float(den)) <= 1e-12:
        return None
    return float(num) / float(den)


def _safe_gap(high: float | None, low: float | None) -> float | None:
    if high is None or low is None:
        return None
    return float(high) - float(low)


def _tree_density_per_100m2(trunk_count: int, config: CalibrationConfig) -> float:
    area_m2 = float(config.width_cells) * float(config.height_cells) * float(config.resolution_m) ** 2
    return 100.0 * float(trunk_count) / max(area_m2, 1e-9)


def _json_safe_dict(obj: Any) -> Any:
    if isinstance(obj, tuple):
        return [_json_safe_dict(v) for v in obj]
    if isinstance(obj, list):
        return [_json_safe_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): _json_safe_dict(v) for k, v in obj.items()}
    return obj


def _fmt_rate(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{100.0 * float(value):.1f}%"


def _fmt_number(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.3f}"
