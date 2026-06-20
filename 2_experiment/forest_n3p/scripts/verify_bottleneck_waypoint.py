from __future__ import annotations

import argparse
import csv
import json
import math
import socket
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
import numpy as np

from forest_n3p.baselines.bottleneck_waypoint import (
    BottleneckWaypointConfig,
    plan_bottleneck_waypoint,
    result_to_dict,
)
from forest_n3p.baselines.voronoi_waypoint import path_length
from forest_n3p.difficulty_calibration import sample_query_in_distance_bin
from forest_n3p.maps.forest import generate_forest_grid
from forest_n3p.pilot_labeling import footprint_clearance_m
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker
from forest_n3p.training_data import (
    TrainingDataConfig,
    _distance_bin_for_query,
    _run_with_wall_timeout,
    build_training_schedule,
    default_training_profiles,
    make_forest_params,
    source_head,
)


Pose = tuple[float, float, float]


@dataclass(frozen=True)
class BottleneckVerificationRecord:
    case_id: int
    profile_name: str
    difficulty_bucket: str
    distance_bin_key: str
    map_seed: int
    query_seed: int
    start: Pose
    goal: Pose
    euclidean_distance_m: float
    success: bool
    collision_free: bool
    feasible: bool
    failure_reason: str | None
    waypoint_count: int
    local_minimum_count: int
    long_gap_minimum_count: int
    mean_bottleneck_clearance_m: float | None
    min_bottleneck_clearance_m: float | None
    skeleton_node_count: int
    graph_edge_count: int
    segment_count: int
    failed_segment_count: int
    skipped_waypoint_total: int
    path_pose_count: int
    path_length_m: float
    total_time_s: float
    total_planner_time_s: float
    total_expansions: int
    figure_path: str
    result_json_path: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the T12 bottleneck waypoint Hybrid A* baseline.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(".pipeline/experiments/20260620_t12_bottleneck_waypoint_verification"),
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path(".pipeline/experiments/20260620_t12_bottleneck_waypoint_verification.md"),
    )
    parser.add_argument("--seed", type=int, default=20260623)
    parser.add_argument("--query-count", type=int, default=10)
    parser.add_argument("--min-successes", type=int, default=10)
    parser.add_argument("--width-cells", type=int, default=300)
    parser.add_argument("--height-cells", type=int, default=300)
    parser.add_argument("--map-generation-wall-timeout-s", type=float, default=30.0)
    parser.add_argument("--max-query-sample-attempts", type=int, default=800)
    parser.add_argument("--min-bottleneck-separation-m", type=float, default=3.0)
    parser.add_argument("--min-bottleneck-prominence-m", type=float, default=0.10)
    parser.add_argument("--max-segment-arc-m", type=float, default=10.0)
    parser.add_argument("--segment-timeout-s", type=float, default=1.0)
    parser.add_argument("--segment-max-nodes", type=int, default=2_000)
    parser.add_argument("--skip-window", type=int, default=3)
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--execution-host", type=str, default=None)
    parser.add_argument("--command", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    command = args.command or " ".join(sys.argv)
    records = run_verification(args)
    payload = write_outputs(
        records,
        args,
        source_head_value=args.source_head or source_head(),
        execution_host=args.execution_host or socket.gethostname(),
        command=command,
    )
    print(args.report_path)
    print(payload["summary_json"])
    print(f"feasible_count={payload['summary']['feasible_count']}/{payload['summary']['query_count']}")
    print(f"acceptance_pass={payload['summary']['acceptance_pass']}")
    return 0 if payload["summary"]["acceptance_pass"] else 2


def run_verification(args: argparse.Namespace) -> list[BottleneckVerificationRecord]:
    data_config = TrainingDataConfig(
        seed=int(args.seed),
        map_count=int(args.query_count),
        queries_per_map=1,
        width_cells=int(args.width_cells),
        height_cells=int(args.height_cells),
        max_query_sample_attempts=int(args.max_query_sample_attempts),
        profiles=default_training_profiles(),
    )
    baseline_config = BottleneckWaypointConfig(
        min_bottleneck_separation_m=float(args.min_bottleneck_separation_m),
        min_bottleneck_prominence_m=float(args.min_bottleneck_prominence_m),
        max_segment_arc_m=float(args.max_segment_arc_m),
        segment_timeout_s=float(args.segment_timeout_s),
        segment_max_nodes=int(args.segment_max_nodes),
        skip_window=int(args.skip_window),
    )
    schedule = build_training_schedule(data_config.profiles, map_count=int(args.query_count))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records: list[BottleneckVerificationRecord] = []

    for case_id, profile in enumerate(schedule):
        grid_map, map_seed = _generate_case_map(case_id, profile, data_config, args, footprint)
        distance_bin = _distance_bin_for_query(data_config, case_id)
        query_seed = int(args.seed) + 720_000 + int(case_id)
        query_rng = np.random.default_rng(query_seed)
        start, goal = sample_query_in_distance_bin(
            grid_map,
            footprint,
            rng=query_rng,
            distance_bin=distance_bin,
            max_attempts=int(args.max_query_sample_attempts),
        )
        result = plan_bottleneck_waypoint(
            grid_map,
            footprint,
            start,
            goal,
            config=baseline_config,
        )
        checker = GridFootprintChecker(grid_map, footprint, theta_bins=baseline_config.theta_bins)
        collision_free = bool(result.success and result.path and not checker.collides_path(_states(result.path)))
        feasible = bool(result.success and collision_free)
        result_json_path = output_dir / f"case_{case_id:02d}_result.json"
        result_json_path.write_text(json.dumps(result_to_dict(result), indent=2, ensure_ascii=False), encoding="utf-8")
        figure_path = output_dir / f"case_{case_id:02d}.png"
        _plot_case(figure_path, grid_map, start, goal, result.path, result.bottlenecks)
        clearances = [item.clearance_m for item in result.bottlenecks]
        records.append(
            BottleneckVerificationRecord(
                case_id=int(case_id),
                profile_name=profile.name,
                difficulty_bucket=profile.difficulty_bucket,
                distance_bin_key=distance_bin.key,
                map_seed=int(map_seed),
                query_seed=int(query_seed),
                start=start,
                goal=goal,
                euclidean_distance_m=float(math.hypot(goal[0] - start[0], goal[1] - start[1])),
                success=bool(result.success),
                collision_free=bool(collision_free),
                feasible=bool(feasible),
                failure_reason=result.failure_reason,
                waypoint_count=len(result.waypoints),
                local_minimum_count=sum(1 for item in result.bottlenecks if item.kind == "local_minimum"),
                long_gap_minimum_count=sum(1 for item in result.bottlenecks if item.kind == "long_gap_minimum"),
                mean_bottleneck_clearance_m=_mean(clearances),
                min_bottleneck_clearance_m=min(clearances) if clearances else None,
                skeleton_node_count=int(result.skeleton_node_count),
                graph_edge_count=int(result.graph_edge_count),
                segment_count=len(result.segment_records),
                failed_segment_count=sum(1 for item in result.segment_records if not item.success),
                skipped_waypoint_total=sum(int(item.skipped_waypoints) for item in result.segment_records if item.success),
                path_pose_count=len(result.path),
                path_length_m=path_length(result.path),
                total_time_s=float(result.total_time_s),
                total_planner_time_s=float(result.total_planner_time_s),
                total_expansions=int(result.total_expansions),
                figure_path=str(figure_path),
                result_json_path=str(result_json_path),
            )
        )
    return records


def write_outputs(
    records: list[BottleneckVerificationRecord],
    args: argparse.Namespace,
    *,
    source_head_value: str,
    execution_host: str,
    command: str,
) -> dict[str, Any]:
    output_dir = Path(args.output_dir)
    report_path = Path(args.report_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    records_csv = output_dir / "records.csv"
    summary_json = output_dir / "summary.json"
    _write_csv(records_csv, records)
    feasible_count = sum(1 for record in records if record.feasible)
    summary = {
        "task": "T12",
        "query_count": len(records),
        "success_count": sum(1 for record in records if record.success),
        "collision_free_count": sum(1 for record in records if record.collision_free),
        "feasible_count": int(feasible_count),
        "min_successes": int(args.min_successes),
        "acceptance_pass": bool(feasible_count >= int(args.min_successes)),
        "total_failed_segments": int(sum(record.failed_segment_count for record in records)),
        "total_skipped_waypoints": int(sum(record.skipped_waypoint_total for record in records)),
        "total_local_minima": int(sum(record.local_minimum_count for record in records)),
        "total_long_gap_minima": int(sum(record.long_gap_minimum_count for record in records)),
        "mean_waypoint_count": _mean(record.waypoint_count for record in records),
        "mean_time_s": _mean(record.total_time_s for record in records),
        "mean_expansions": _mean(record.total_expansions for record in records),
        "by_case": [asdict(record) for record in records],
    }
    payload = {
        "source_head": source_head_value,
        "execution_host": execution_host,
        "command": command,
        "config": vars(args),
        "summary": summary,
        "records_csv": str(records_csv),
        "summary_json": str(summary_json),
        "report_path": str(report_path),
    }
    summary_json.write_text(json.dumps(_json_safe(payload), indent=2, ensure_ascii=False), encoding="utf-8")
    report_path.write_text(render_report(payload), encoding="utf-8")
    return payload


def render_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    status = "pass" if summary["acceptance_pass"] else "needs_review"
    lines = [
        "---",
        "date: 2026-06-20",
        f"status: {status}",
        "origin: ai+experiment",
        "reviewed: false",
        "task: T12",
        "contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_head: {payload['source_head']}",
        f"execution_host: {payload['execution_host']}",
        "---",
        "",
        "# T12 Bottleneck Waypoint Hybrid A* 基线验收报告",
        "",
        "## 结论",
        "",
        f"- 验收: `{status}`",
        f"- 可行无碰撞路径: {summary['feasible_count']} / {summary['query_count']}",
        f"- 验收阈值: >= {summary['min_successes']} / {summary['query_count']}",
        f"- 平均 waypoint 数: {_fmt_number(summary['mean_waypoint_count'])}",
        f"- 局部低谷 waypoint 数: {summary['total_local_minima']}",
        f"- 长段守卫 waypoint 数: {summary['total_long_gap_minima']}",
        f"- 段内失败尝试数: {summary['total_failed_segments']}",
        f"- 被跳过 waypoint 数: {summary['total_skipped_waypoints']}",
        f"- 参数: bottleneck separation = {float(payload['config']['min_bottleneck_separation_m']):.1f} m, "
        f"prominence = {float(payload['config']['min_bottleneck_prominence_m']):.2f} m, "
        f"max segment arc = {float(payload['config']['max_segment_arc_m']):.1f} m, "
        f"segment budget = {float(payload['config']['segment_timeout_s']):.1f} s / "
        f"{int(payload['config']['segment_max_nodes'])} nodes",
        "",
        "参数说明：本次继承 T08/T09 的程序化森林、车辆尺寸、段内 Hybrid A* 配置与 T06 难度切点；T05 的 `L_min=1.0m` 与 T06 切点仍为 `reviewed:false`，因此本报告只证明 T12 手工瓶颈规则基线工程闭环，不代表 T14 主评测结论。",
        "",
        "## 方法",
        "",
        "先对车辆中心可安全放置的自由空间提取 medial-axis skeleton，并沿 start-goal skeleton 路径读取 EDT 安全裕量；瓶颈定义为该一维安全裕量曲线的局部低谷（对 `-clearance` 用 prominence/distance 约束找峰）。相邻瓶颈间若 skeleton 弧长超过上限，则在该区间取最窄点作为长段守卫 waypoint。所有相邻 waypoint 再用与主方法一致的段内 Hybrid A* 连接，计时包含中轴、EDT、瓶颈检测和所有段内规划开销。",
        "",
        "## 查询明细",
        "",
        "| case | bucket | distance_bin | feasible | waypoints | local_min | guard | failed_segments | time(s) | expansions | figure |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for record in summary["by_case"]:
        lines.append(
            "| "
            f"{record['case_id']} | "
            f"{record['difficulty_bucket']} | "
            f"{record['distance_bin_key']} | "
            f"{'yes' if record['feasible'] else 'no'} | "
            f"{record['waypoint_count']} | "
            f"{record['local_minimum_count']} | "
            f"{record['long_gap_minimum_count']} | "
            f"{record['failed_segment_count']} | "
            f"{float(record['total_time_s']):.3f} | "
            f"{record['total_expansions']} | "
            f"`{record['figure_path']}` |"
        )
    lines.extend(
        [
            "",
            "## 产物",
            "",
            f"- 明细 CSV: `{payload['records_csv']}`",
            f"- 摘要 JSON: `{payload['summary_json']}`",
            f"- 单查询 JSON/PNG: `{Path(payload['records_csv']).parent}`",
            "",
        ]
    )
    return "\n".join(lines)


def _generate_case_map(
    case_id: int,
    profile: Any,
    config: TrainingDataConfig,
    args: argparse.Namespace,
    footprint: TwoCircleFootprint,
) -> tuple[GridMap, int]:
    last_error: str | None = None
    for attempt in range(20):
        map_seed = int(args.seed) + 630_000 + int(case_id) * 1_000 + attempt
        map_rng = np.random.default_rng(map_seed)
        try:
            grid, _start_xy, _goal_xy = _run_with_wall_timeout(
                "verify_bottleneck_map_generation",
                float(args.map_generation_wall_timeout_s),
                lambda: generate_forest_grid(
                    params=make_forest_params(profile, config),
                    rng=map_rng,
                    footprint_clearance_m=footprint_clearance_m(resolution_m=float(config.resolution_m)),
                ),
            )
            return GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0)), map_seed
        except Exception as exc:  # noqa: BLE001
            last_error = f"{type(exc).__name__}: {exc}"
    raise RuntimeError(f"failed to generate verification map for case {case_id}: {last_error}")


def _plot_case(
    path: Path,
    grid_map: GridMap,
    start: Pose,
    goal: Pose,
    result_path: Iterable[Pose],
    waypoints: Iterable[Any],
) -> None:
    grid = np.asarray(grid_map.data)
    extent = (
        float(grid_map.origin[0]),
        float(grid_map.origin[0]) + grid.shape[1] * float(grid_map.resolution),
        float(grid_map.origin[1]),
        float(grid_map.origin[1]) + grid.shape[0] * float(grid_map.resolution),
    )
    fig, ax = plt.subplots(figsize=(7, 7), dpi=140)
    ax.imshow(1 - grid, cmap="gray", origin="lower", extent=extent)
    poses = tuple(result_path)
    if poses:
        ax.plot([p[0] for p in poses], [p[1] for p in poses], color="#1f77b4", linewidth=2.0, label="path")
    waypoint_seq = tuple(waypoints)
    if waypoint_seq:
        local = [item for item in waypoint_seq if item.kind == "local_minimum"]
        guard = [item for item in waypoint_seq if item.kind != "local_minimum"]
        if local:
            ax.scatter([p.pose[0] for p in local], [p.pose[1] for p in local], s=52, marker="x", color="#d62728", label="bottleneck")
        if guard:
            ax.scatter([p.pose[0] for p in guard], [p.pose[1] for p in guard], s=42, marker="+", color="#ff7f0e", label="guard")
    ax.scatter([start[0]], [start[1]], s=48, color="#2ca02c", label="start")
    ax.scatter([goal[0]], [goal[1]], s=48, color="#9467bd", label="goal")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title(path.stem)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _states(path: Iterable[Pose]) -> list[AckermannState]:
    return [AckermannState(float(x), float(y), float(theta)) for x, y, theta in path]


def _write_csv(path: Path, rows: Iterable[BottleneckVerificationRecord]) -> None:
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
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False) if isinstance(value, (tuple, list, dict)) else value
                    for key, value in asdict(row).items()
                }
            )


def _mean(values: Iterable[float | None]) -> float | None:
    clean = [float(value) for value in values if value is not None]
    if not clean:
        return None
    return float(np.mean(np.asarray(clean, dtype=np.float64)))


def _fmt_number(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.3f}"


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, tuple):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    raise SystemExit(main())
