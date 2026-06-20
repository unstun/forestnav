from __future__ import annotations

import csv
import json
import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from forest_n3p.labeling import LabelingConfig, extract_subgoal_labels
from forest_n3p.maps.forest import ForestParams, generate_forest_grid
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


Pose = tuple[float, float, float]


@dataclass(frozen=True)
class DifficultyProfile:
    name: str
    trunk_count: int
    trunk_gap_m: float
    trunk_gap_jitter: float = 0.25
    bush_cluster_count: int = 0


@dataclass(frozen=True)
class PilotConfig:
    seed: int = 20260620
    map_count: int = 20
    queries_per_map: int = 10
    width_cells: int = 300
    height_cells: int = 300
    resolution_m: float = 0.1
    min_query_distance_m: float = 8.0
    max_query_sample_attempts: int = 600
    teacher_timeout_s: float = 2.5
    teacher_max_nodes: int = 15_000
    l_max_m: float = 8.0
    l_min_m: float = 1.5
    path_sample_step_m: float = 0.2
    turning_radius_m: float = 1.0
    wheelbase_m: float = 0.6
    rs_sample_step_m: float = 0.1
    profiles: tuple[DifficultyProfile, ...] = field(default_factory=lambda: default_profiles())


@dataclass(frozen=True)
class MapRecord:
    map_id: int
    difficulty: str
    map_seed: int
    generated: bool
    generation_time_s: float
    trunk_count: int
    trunk_gap_m: float
    obstacle_ratio: float
    failure_reason: str | None


@dataclass(frozen=True)
class QueryRecord:
    map_id: int
    query_id: int
    difficulty: str
    map_seed: int
    query_seed: int
    start: Pose
    goal: Pose
    teacher_success: bool
    teacher_failure_reason: str | None
    teacher_time_s: float
    teacher_expansions: int
    teacher_path_length_m: float
    label_attempted: bool
    label_success: bool
    label_failure_reason: str | None
    label_sample_count: int
    total_segment_count: int
    segment_lengths_m: tuple[float, ...]


@dataclass(frozen=True)
class PilotRun:
    config: PilotConfig
    maps: tuple[MapRecord, ...]
    queries: tuple[QueryRecord, ...]
    summary: dict[str, Any]


def default_profiles() -> tuple[DifficultyProfile, ...]:
    return (
        DifficultyProfile(name="low", trunk_count=60, trunk_gap_m=1.20, trunk_gap_jitter=0.20),
        DifficultyProfile(name="medium", trunk_count=90, trunk_gap_m=1.00, trunk_gap_jitter=0.25),
        DifficultyProfile(name="high", trunk_count=120, trunk_gap_m=0.85, trunk_gap_jitter=0.25),
    )


def build_profile_schedule(
    profiles: Sequence[DifficultyProfile],
    *,
    map_count: int,
) -> tuple[DifficultyProfile, ...]:
    if not profiles:
        raise ValueError("profiles must not be empty")
    count = int(map_count)
    if count <= 0:
        raise ValueError("map_count must be positive")

    base = count // len(profiles)
    remainder = count % len(profiles)
    out: list[DifficultyProfile] = []
    for idx, profile in enumerate(profiles):
        copies = base + (1 if idx < remainder else 0)
        out.extend([profile] * copies)
    return tuple(out)


def footprint_clearance_m(*, resolution_m: float) -> float:
    body_radius = math.hypot(0.740 / 2.0, 0.924 / 4.0)
    return float(body_radius + math.sqrt(2.0) * 0.5 * float(resolution_m))


def make_forest_params(profile: DifficultyProfile, config: PilotConfig) -> ForestParams:
    return ForestParams(
        width_cells=int(config.width_cells),
        height_cells=int(config.height_cells),
        cell_size_m=float(config.resolution_m),
        trunk_count=int(profile.trunk_count),
        trunk_gap_m=float(profile.trunk_gap_m),
        trunk_gap_jitter=float(profile.trunk_gap_jitter),
        bush_cluster_count=int(profile.bush_cluster_count),
        trunk_place_tries=20_000,
        max_tries=80,
        start_frac=0.2,
        goal_frac=0.8,
    )


def sample_query(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    *,
    rng: np.random.Generator,
    min_distance_m: float,
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
        if distance < float(min_distance_m):
            continue

        heading = math.atan2(dy, dx)
        start = (float(sx), float(sy), float(heading))
        goal = (float(gx), float(gy), float(heading))
        if checker.collides_pose(*start):
            continue
        if checker.collides_pose(*goal):
            continue
        return start, goal

    raise RuntimeError("failed to sample a collision-free start/goal pair")


def _make_planner(grid_map: GridMap, footprint: TwoCircleFootprint, config: PilotConfig) -> HybridAStarPlanner:
    params = AckermannParams(
        wheelbase=float(config.wheelbase_m),
        min_turn_radius=float(config.turning_radius_m),
    )
    return HybridAStarPlanner(
        grid_map,
        footprint,
        params,
        analytic_expansion=True,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=math.radians(15.0),
        use_holonomic_heuristic=True,
        theta_bins=72,
    )


def _teacher_trace(path: list[AckermannState], stats: dict[str, Any]) -> list[Pose]:
    trace = stats.get("trace_poses")
    if trace:
        return [(float(x), float(y), float(theta)) for x, y, theta in trace]
    return [state.as_tuple() for state in path]


def run_label_pilot(config: PilotConfig) -> PilotRun:
    schedule = build_profile_schedule(config.profiles, map_count=int(config.map_count))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    maps: list[MapRecord] = []
    queries: list[QueryRecord] = []

    for map_id, profile in enumerate(schedule):
        map_seed = int(config.seed) + 10_000 + map_id
        map_rng = np.random.default_rng(map_seed)
        started = time.perf_counter()
        grid = None
        failure_reason = None
        try:
            params = make_forest_params(profile, config)
            grid, _start_xy, _goal_xy = generate_forest_grid(
                params=params,
                rng=map_rng,
                footprint_clearance_m=footprint_clearance_m(resolution_m=float(config.resolution_m)),
            )
            generated = True
        except Exception as exc:  # noqa: BLE001 - record map-generation failures in pilot CSV.
            generated = False
            failure_reason = f"{type(exc).__name__}: {exc}"

        generation_time_s = time.perf_counter() - started
        obstacle_ratio = float(np.mean(grid)) if grid is not None else 0.0
        maps.append(
            MapRecord(
                map_id=map_id,
                difficulty=profile.name,
                map_seed=map_seed,
                generated=generated,
                generation_time_s=float(generation_time_s),
                trunk_count=int(profile.trunk_count),
                trunk_gap_m=float(profile.trunk_gap_m),
                obstacle_ratio=obstacle_ratio,
                failure_reason=failure_reason,
            )
        )
        if grid is None:
            continue

        grid_map = GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0))
        planner = _make_planner(grid_map, footprint, config)
        labeling_config = LabelingConfig(
            l_max_m=float(config.l_max_m),
            l_min_m=float(config.l_min_m),
            path_sample_step_m=float(config.path_sample_step_m),
            turning_radius_m=float(config.turning_radius_m),
            wheelbase_m=float(config.wheelbase_m),
            rs_sample_step_m=float(config.rs_sample_step_m),
        )

        for query_id in range(int(config.queries_per_map)):
            query_seed = int(config.seed) + (map_id * 1_000) + query_id
            query_rng = np.random.default_rng(query_seed)
            start: Pose
            goal: Pose
            try:
                start, goal = sample_query(
                    grid_map,
                    footprint,
                    rng=query_rng,
                    min_distance_m=float(config.min_query_distance_m),
                    max_attempts=int(config.max_query_sample_attempts),
                )
            except Exception as exc:  # noqa: BLE001
                queries.append(
                    QueryRecord(
                        map_id=map_id,
                        query_id=query_id,
                        difficulty=profile.name,
                        map_seed=map_seed,
                        query_seed=query_seed,
                        start=(math.nan, math.nan, math.nan),
                        goal=(math.nan, math.nan, math.nan),
                        teacher_success=False,
                        teacher_failure_reason=f"query_sampling_failed:{type(exc).__name__}",
                        teacher_time_s=0.0,
                        teacher_expansions=0,
                        teacher_path_length_m=0.0,
                        label_attempted=False,
                        label_success=False,
                        label_failure_reason=None,
                        label_sample_count=0,
                        total_segment_count=0,
                        segment_lengths_m=(),
                    )
                )
                continue

            path, stats = planner.plan(
                AckermannState(*start),
                AckermannState(*goal),
                timeout=float(config.teacher_timeout_s),
                max_nodes=int(config.teacher_max_nodes),
            )
            teacher_success = bool(path)
            teacher_failure_reason = None if teacher_success else str(stats.get("failure_reason", "unknown"))
            label_attempted = False
            label_success = False
            label_failure_reason = None
            label_sample_count = 0
            total_segment_count = 0
            segment_lengths_m: tuple[float, ...] = ()

            if teacher_success:
                label_attempted = True
                label_result = extract_subgoal_labels(
                    grid_map,
                    footprint,
                    _teacher_trace(path, stats),
                    config=labeling_config,
                )
                label_success = bool(label_result.success)
                label_failure_reason = label_result.failure_reason
                label_sample_count = len(label_result.samples)
                total_segment_count = label_sample_count + 1 if label_success else 0
                segment_lengths_m = tuple(
                    float(sample.s_subgoal_m - sample.s_start_m)
                    for sample in label_result.samples
                )

            queries.append(
                QueryRecord(
                    map_id=map_id,
                    query_id=query_id,
                    difficulty=profile.name,
                    map_seed=map_seed,
                    query_seed=query_seed,
                    start=start,
                    goal=goal,
                    teacher_success=teacher_success,
                    teacher_failure_reason=teacher_failure_reason,
                    teacher_time_s=float(stats.get("time", 0.0)),
                    teacher_expansions=int(stats.get("expansions", 0)),
                    teacher_path_length_m=float(stats.get("path_length", 0.0)),
                    label_attempted=label_attempted,
                    label_success=label_success,
                    label_failure_reason=label_failure_reason,
                    label_sample_count=int(label_sample_count),
                    total_segment_count=int(total_segment_count),
                    segment_lengths_m=segment_lengths_m,
                )
            )

    summary = summarize_query_records(queries)
    summary["map_count"] = len(maps)
    summary["generated_map_count"] = sum(1 for item in maps if item.generated)
    summary["map_generation_failure_count"] = sum(1 for item in maps if not item.generated)
    summary["label_failure_threshold"] = 0.20
    failure_rate = summary.get("label_failure_rate")
    summary["label_failure_rate_pass"] = (
        failure_rate is not None and float(failure_rate) < float(summary["label_failure_threshold"])
    )
    return PilotRun(config=config, maps=tuple(maps), queries=tuple(queries), summary=summary)


def _ratio(num: int, den: int) -> float | None:
    if den <= 0:
        return None
    return float(num) / float(den)


def _numeric_stats(values: Sequence[float]) -> dict[str, float | None]:
    if not values:
        return {"min": None, "mean": None, "max": None}
    arr = np.asarray(values, dtype=np.float64)
    return {
        "min": float(np.min(arr)),
        "mean": float(np.mean(arr)),
        "max": float(np.max(arr)),
    }


def summarize_query_records(records: Sequence[QueryRecord]) -> dict[str, Any]:
    total = len(records)
    teacher_success = sum(1 for record in records if record.teacher_success)
    label_attempt = sum(1 for record in records if record.label_attempted)
    label_success = sum(1 for record in records if record.label_success)
    label_failure = label_attempt - label_success
    total_samples = sum(int(record.label_sample_count) for record in records)
    segment_lengths = [
        float(length)
        for record in records
        for length in record.segment_lengths_m
    ]
    successful_segment_counts = [
        float(record.total_segment_count)
        for record in records
        if record.label_success
    ]

    by_difficulty: dict[str, Any] = {}
    for difficulty in sorted({record.difficulty for record in records}):
        subset = [record for record in records if record.difficulty == difficulty]
        by_difficulty[difficulty] = _summarize_subset(subset)

    return {
        "total_queries": total,
        "teacher_success_count": teacher_success,
        "teacher_success_rate": _ratio(teacher_success, total),
        "label_attempt_count": label_attempt,
        "label_success_count": label_success,
        "label_failure_count": label_failure,
        "label_failure_rate": _ratio(label_failure, label_attempt),
        "average_total_segments_per_successful_labeled_path": (
            float(np.mean(successful_segment_counts)) if successful_segment_counts else None
        ),
        "segment_length_m": _numeric_stats(segment_lengths),
        "total_samples": total_samples,
        "by_difficulty": by_difficulty,
    }


def _summarize_subset(records: Sequence[QueryRecord]) -> dict[str, Any]:
    total = len(records)
    teacher_success = sum(1 for record in records if record.teacher_success)
    label_attempt = sum(1 for record in records if record.label_attempted)
    label_success = sum(1 for record in records if record.label_success)
    label_failure = label_attempt - label_success
    segment_lengths = [
        float(length)
        for record in records
        for length in record.segment_lengths_m
    ]
    segment_counts = [
        float(record.total_segment_count)
        for record in records
        if record.label_success
    ]
    return {
        "total_queries": total,
        "teacher_success_count": teacher_success,
        "teacher_success_rate": _ratio(teacher_success, total),
        "label_attempt_count": label_attempt,
        "label_success_count": label_success,
        "label_failure_count": label_failure,
        "label_failure_rate": _ratio(label_failure, label_attempt),
        "average_total_segments_per_successful_labeled_path": (
            float(np.mean(segment_counts)) if segment_counts else None
        ),
        "segment_length_m": _numeric_stats(segment_lengths),
        "total_samples": sum(int(record.label_sample_count) for record in records),
    }


def _json_safe_dict(obj: Any) -> Any:
    if isinstance(obj, tuple):
        return [_json_safe_dict(v) for v in obj]
    if isinstance(obj, list):
        return [_json_safe_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): _json_safe_dict(v) for k, v in obj.items()}
    return obj


def write_csv(path: Path, rows: Iterable[Any]) -> None:
    rows = tuple(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            raw = asdict(row)
            cooked = {
                key: json.dumps(value, ensure_ascii=False) if isinstance(value, (tuple, list, dict)) else value
                for key, value in raw.items()
            }
            writer.writerow(cooked)


def write_pilot_outputs(
    run: PilotRun,
    output_dir: Path,
    *,
    source_head: str,
    execution_host: str,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    maps_csv = output_dir / "maps.csv"
    queries_csv = output_dir / "queries.csv"
    summary_json = output_dir / "summary.json"
    report_md = output_dir / "report.md"

    write_csv(maps_csv, run.maps)
    write_csv(queries_csv, run.queries)
    summary_payload = {
        "source_head": source_head,
        "execution_host": execution_host,
        "config": _json_safe_dict(asdict(run.config)),
        "summary": run.summary,
        "files": {
            "maps_csv": str(maps_csv),
            "queries_csv": str(queries_csv),
            "summary_json": str(summary_json),
            "report_md": str(report_md),
        },
    }
    summary_json.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    report_md.write_text(
        render_report(summary_payload),
        encoding="utf-8",
    )
    return {
        "maps_csv": str(maps_csv),
        "queries_csv": str(queries_csv),
        "summary_json": str(summary_json),
        "report_md": str(report_md),
    }


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


def render_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    config = payload["config"]
    status = "pass" if summary.get("label_failure_rate_pass") else "needs_review"
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
        "# T05 标签预实验报告",
        "",
        "## 目的",
        "",
        "验证前向贪心 Reeds-Shepp 子目标标签管线在小规模程序化森林地图上的质量，重点检查教师求解成功率、标签提取失败率、段数分布和样本量。",
        "",
        "## 实验设置",
        "",
        "```text",
        f"map_count={config['map_count']}",
        f"queries_per_map={config['queries_per_map']}",
        f"seed={config['seed']}",
        f"map_size_cells={config['width_cells']}x{config['height_cells']}",
        f"resolution_m={config['resolution_m']}",
        f"L_max_m={config['l_max_m']}",
        f"L_min_m={config['l_min_m']}",
        f"teacher_timeout_s={config['teacher_timeout_s']}",
        f"teacher_max_nodes={config['teacher_max_nodes']}",
        "```",
        "",
        "## 总体结果",
        "",
        "| 指标 | 数值 |",
        "|---|---:|",
        f"| 地图生成成功数 | {summary['generated_map_count']} / {summary['map_count']} |",
        f"| 查询总数 | {summary['total_queries']} |",
        f"| 教师求解成功率 | {_fmt_rate(summary['teacher_success_rate'])} |",
        f"| 标签尝试数 | {summary['label_attempt_count']} |",
        f"| 标签成功数 | {summary['label_success_count']} |",
        f"| 标签失败率 | {_fmt_rate(summary['label_failure_rate'])} |",
        f"| 每条成功标签路径平均总段数 | {_fmt_number(summary['average_total_segments_per_successful_labeled_path'])} |",
        f"| 总样本数 | {summary['total_samples']} |",
        "",
        "## 分桶结果",
        "",
        "| 难度 | 查询数 | 教师成功率 | 标签失败率 | 平均总段数 | 样本数 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for difficulty, item in summary["by_difficulty"].items():
        lines.append(
            "| "
            f"{difficulty} | "
            f"{item['total_queries']} | "
            f"{_fmt_rate(item['teacher_success_rate'])} | "
            f"{_fmt_rate(item['label_failure_rate'])} | "
            f"{_fmt_number(item['average_total_segments_per_successful_labeled_path'])} | "
            f"{item['total_samples']} |"
        )

    seg = summary["segment_length_m"]
    lines.extend(
        [
            "",
            "## 段长分布",
            "",
            "| min | mean | max |",
            "|---:|---:|---:|",
            f"| {_fmt_number(seg['min'])} | {_fmt_number(seg['mean'])} | {_fmt_number(seg['max'])} |",
            "",
            "## 验收判断",
            "",
            (
                "- 标签失败率 `< 20%`：通过。"
                if summary.get("label_failure_rate_pass")
                else "- 标签失败率未达 `< 20%` 或无可判定标签样本：需要 Dr Sun 审阅是否调整 `L_min/L_max`。"
            ),
            "",
            "## 产物",
            "",
            f"- `maps.csv`: `{payload['files']['maps_csv']}`",
            f"- `queries.csv`: `{payload['files']['queries_csv']}`",
            f"- `summary.json`: `{payload['files']['summary_json']}`",
        ]
    )
    return "\n".join(lines) + "\n"
