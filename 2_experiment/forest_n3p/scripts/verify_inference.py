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

from forest_n3p.difficulty_calibration import sample_query_in_distance_bin
from forest_n3p.inference import (
    InferenceConfig,
    KnnSubgoalLibrary,
    result_to_dict,
    run_forest_n3p,
)
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
class VerificationRecord:
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
    termination_reason: str | None
    used_f1: int
    used_f2: int
    used_f3: int
    step_count: int
    path_pose_count: int
    path_length_m: float
    final_distance_to_goal_m: float
    total_time_s: float
    total_planner_time_s: float
    total_expansions: int
    figure_path: str
    result_json_path: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify T09 F-N3P inference on unseen forest queries.")
    parser.add_argument(
        "--library-dir",
        type=Path,
        default=Path("2_experiment/forest_n3p/models/t09_knn_library"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(".pipeline/experiments/20260620_t09_inference_verification"),
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path(".pipeline/experiments/20260620_t09_inference_verification.md"),
    )
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--query-count", type=int, default=5)
    parser.add_argument("--min-successes", type=int, default=4)
    parser.add_argument("--width-cells", type=int, default=300)
    parser.add_argument("--height-cells", type=int, default=300)
    parser.add_argument("--map-generation-wall-timeout-s", type=float, default=30.0)
    parser.add_argument("--max-query-sample-attempts", type=int, default=800)
    parser.add_argument("--segment-timeout-s", type=float, default=1.0)
    parser.add_argument("--segment-max-nodes", type=int, default=2_000)
    parser.add_argument("--full-fallback-timeout-s", type=float, default=2.5)
    parser.add_argument("--full-fallback-max-nodes", type=int, default=15_000)
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--execution-host", type=str, default=None)
    parser.add_argument("--command", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    command = args.command or " ".join(sys.argv)
    library = KnnSubgoalLibrary.load(args.library_dir)
    records = run_verification(args, library)
    payload = write_outputs(
        records,
        args,
        library,
        source_head_value=args.source_head or source_head(),
        execution_host=args.execution_host or socket.gethostname(),
        command=command,
    )
    print(args.report_path)
    print(payload["summary_json"])
    print(f"feasible_count={payload['summary']['feasible_count']}/{payload['summary']['query_count']}")
    print(f"acceptance_pass={payload['summary']['acceptance_pass']}")
    return 0 if payload["summary"]["acceptance_pass"] else 2


def run_verification(args: argparse.Namespace, library: KnnSubgoalLibrary) -> list[VerificationRecord]:
    config = TrainingDataConfig(
        seed=int(args.seed),
        map_count=int(args.query_count),
        queries_per_map=1,
        width_cells=int(args.width_cells),
        height_cells=int(args.height_cells),
        max_query_sample_attempts=int(args.max_query_sample_attempts),
        profiles=default_training_profiles(),
    )
    inference_config = InferenceConfig(
        segment_timeout_s=float(args.segment_timeout_s),
        segment_max_nodes=int(args.segment_max_nodes),
        full_fallback_timeout_s=float(args.full_fallback_timeout_s),
        full_fallback_max_nodes=int(args.full_fallback_max_nodes),
    )
    schedule = build_training_schedule(config.profiles, map_count=int(args.query_count))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records: list[VerificationRecord] = []

    for case_id, profile in enumerate(schedule):
        grid_map, map_seed = _generate_case_map(case_id, profile, config, args, footprint)
        distance_bin = _distance_bin_for_query(config, case_id)
        query_seed = int(args.seed) + 700_000 + int(case_id)
        query_rng = np.random.default_rng(query_seed)
        start, goal = sample_query_in_distance_bin(
            grid_map,
            footprint,
            rng=query_rng,
            distance_bin=distance_bin,
            max_attempts=int(args.max_query_sample_attempts),
        )
        result = run_forest_n3p(
            grid_map,
            footprint,
            start,
            goal,
            library,
            config=inference_config,
        )
        checker = GridFootprintChecker(grid_map, footprint, theta_bins=inference_config.theta_bins)
        collision_free = bool(result.success and result.path and not checker.collides_path(_states(result.path)))
        feasible = bool(result.success and collision_free)
        result_json_path = output_dir / f"case_{case_id:02d}_result.json"
        result_json_path.write_text(json.dumps(result_to_dict(result), indent=2, ensure_ascii=False), encoding="utf-8")
        figure_path = output_dir / f"case_{case_id:02d}.png"
        _plot_case(figure_path, grid_map, start, goal, result.path, result.steps)
        records.append(
            VerificationRecord(
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
                termination_reason=result.termination_reason,
                used_f1=int(result.used_f1),
                used_f2=int(result.used_f2),
                used_f3=int(result.used_f3),
                step_count=len(result.steps),
                path_pose_count=len(result.path),
                path_length_m=_path_length(result.path),
                final_distance_to_goal_m=float(result.final_distance_to_goal_m),
                total_time_s=float(result.total_time_s),
                total_planner_time_s=float(result.total_planner_time_s),
                total_expansions=int(result.total_expansions),
                figure_path=str(figure_path),
                result_json_path=str(result_json_path),
            )
        )
    return records


def write_outputs(
    records: list[VerificationRecord],
    args: argparse.Namespace,
    library: KnnSubgoalLibrary,
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
    success_count = sum(1 for record in records if record.success)
    collision_free_count = sum(1 for record in records if record.collision_free)
    summary = {
        "task": "T09",
        "query_count": len(records),
        "success_count": int(success_count),
        "collision_free_count": int(collision_free_count),
        "feasible_count": int(feasible_count),
        "min_successes": int(args.min_successes),
        "acceptance_pass": bool(feasible_count >= int(args.min_successes)),
        "used_f1_total": int(sum(record.used_f1 for record in records)),
        "used_f2_total": int(sum(record.used_f2 for record in records)),
        "used_f3_total": int(sum(record.used_f3 for record in records)),
        "mean_time_s": _mean(record.total_time_s for record in records),
        "mean_expansions": _mean(record.total_expansions for record in records),
        "by_case": [asdict(record) for record in records],
    }
    payload = {
        "source_head": source_head_value,
        "execution_host": execution_host,
        "command": command,
        "library_dir": str(args.library_dir),
        "library_metadata": library.metadata,
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
        "task: T09",
        "contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_head: {payload['source_head']}",
        f"execution_host: {payload['execution_host']}",
        "---",
        "",
        "# T09 KNN 在线推理验收报告",
        "",
        "## 结论",
        "",
        f"- 验收: `{status}`",
        f"- 可行无碰撞路径: {summary['feasible_count']} / {summary['query_count']}",
        f"- 验收阈值: >= {summary['min_successes']} / {summary['query_count']}",
        f"- F1/F2/F3 触发计数: {summary['used_f1_total']} / {summary['used_f2_total']} / {summary['used_f3_total']}",
        "",
        "参数说明：本次继承 T08 数据集，T05 的 `L_min=1.0m` 与 T06 难度切点仍为 `reviewed:false`；因此本报告证明 T09 工程闭环可运行，不代表论文参数最终冻结。",
        "",
        "## KNN 库",
        "",
        f"- 目录: `{payload['library_dir']}`",
        f"- 模型: `{payload['library_metadata'].get('model')}`",
        f"- 特征形状: `{payload['library_metadata'].get('feature_shape')}`",
        f"- 标签形状: `{payload['library_metadata'].get('label_shape')}`",
        f"- scikit-learn: `{payload['library_metadata'].get('sklearn_version')}`",
        "",
        "## 查询明细",
        "",
        "| case | bucket | distance_bin | feasible | termination | F1 | F2 | F3 | time(s) | expansions | figure |",
        "|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for record in summary["by_case"]:
        lines.append(
            "| "
            f"{record['case_id']} | "
            f"{record['difficulty_bucket']} | "
            f"{record['distance_bin_key']} | "
            f"{'yes' if record['feasible'] else 'no'} | "
            f"`{record['termination_reason'] or record['failure_reason']}` | "
            f"{record['used_f1']} | "
            f"{record['used_f2']} | "
            f"{record['used_f3']} | "
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
        map_seed = int(args.seed) + 600_000 + int(case_id) * 1_000 + attempt
        map_rng = np.random.default_rng(map_seed)
        try:
            grid, _start_xy, _goal_xy = _run_with_wall_timeout(
                "verify_map_generation",
                float(args.map_generation_wall_timeout_s),
                lambda: generate_forest_grid(
                    params=make_forest_params(profile, config),
                    rng=map_rng,
                    footprint_clearance_m=footprint_clearance_m(resolution_m=float(config.resolution_m)),
                ),
            )
            return GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0)), map_seed
        except Exception as exc:  # noqa: BLE001 - try another seed and record the final error if all fail.
            last_error = f"{type(exc).__name__}: {exc}"
    raise RuntimeError(f"failed to generate verification map for case {case_id}: {last_error}")


def _plot_case(
    path: Path,
    grid_map: GridMap,
    start: Pose,
    goal: Pose,
    result_path: Iterable[Pose],
    steps: Iterable[Any],
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
    targets = [step.target_pose for step in steps if getattr(step, "mode", "") not in {"direct_rs_goal", "f3_full_query"}]
    if targets:
        ax.scatter([p[0] for p in targets], [p[1] for p in targets], s=42, marker="x", color="#ff7f0e", label="subgoals")
    ax.scatter([start[0]], [start[1]], s=48, color="#2ca02c", label="start")
    ax.scatter([goal[0]], [goal[1]], s=48, color="#d62728", label="goal")
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


def _path_length(path: Iterable[Pose]) -> float:
    poses = tuple(path)
    return float(
        sum(
            math.hypot(float(cur[0]) - float(prev[0]), float(cur[1]) - float(prev[1]))
            for prev, cur in zip(poses[:-1], poses[1:], strict=True)
        )
    )


def _write_csv(path: Path, rows: Iterable[VerificationRecord]) -> None:
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


def _mean(values: Iterable[float]) -> float | None:
    clean = [float(value) for value in values]
    if not clean:
        return None
    return float(np.mean(np.asarray(clean, dtype=np.float64)))


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
