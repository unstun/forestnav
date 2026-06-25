from __future__ import annotations

import argparse
import csv
import importlib
import math
import sys
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


def _find_project_root(start: Path) -> Path:
    for path in (start, *start.parents):
        if (path / "2_experiment" / "forest_n3p").is_dir():
            return path
    raise RuntimeError(f"cannot locate ForestNav project root from {start}")


PROJECT_ROOT = _find_project_root(Path(__file__).resolve())
sys.path.insert(0, str(PROJECT_ROOT / "2_experiment"))


def _install_numpy_pickle_aliases() -> None:
    try:
        import numpy.core as numpy_core
    except Exception:
        return

    sys.modules.setdefault("numpy._core", numpy_core)
    for name in ("multiarray", "numeric", "umath", "_multiarray_umath"):
        try:
            module = importlib.import_module(f"numpy.core.{name}")
        except Exception:
            continue
        sys.modules.setdefault(f"numpy._core.{name}", module)


_install_numpy_pickle_aliases()

from forest_n3p.evaluation import EvaluationConfig, EvaluationRecord  # noqa: E402
from forest_n3p.features import Pose  # noqa: E402
from forest_n3p.main_evaluation import (  # noqa: E402
    EvaluationQuery,
    MainEvaluationConfig,
    _evaluate_run_with_collision_rejection,
    _generate_grid_map,
    _load_predictors,
    _profile_by_name,
    _run_method,
    _run_vanilla_ha,
    build_query_set,
    validation_main_evaluation_profiles,
)
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint  # noqa: E402


BUCKETS = ("Easy", "Complex", "Extreme")
METHODS = ("vanilla_ha", "f_n3p_knn")


def _trial_config(args: argparse.Namespace) -> MainEvaluationConfig:
    return MainEvaluationConfig(
        seed=int(args.seed),
        queries_per_bucket=int(args.queries_per_bucket),
        seed_count=5,
        queries_per_map=5,
        methods=METHODS,
        profiles=validation_main_evaluation_profiles(),
        knn_library_dir=PROJECT_ROOT / "2_experiment" / "forest_n3p" / "models" / "t09_knn_library",
        knn_dataset_dir=PROJECT_ROOT / "2_experiment" / "forest_n3p" / "datasets" / "t08_training_dataset",
        enforce_t14_scale=False,
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
    )


def _record_row(
    query: EvaluationQuery,
    record: EvaluationRecord,
    *,
    vanilla_reference_length_m: float | None,
) -> dict[str, Any]:
    inflation = record.path_inflation_ratio
    if record.method == "vanilla_ha" and record.feasible and vanilla_reference_length_m is not None:
        inflation = 0.0
    return {
        "bucket": query.difficulty_bucket,
        "query_id": query.query_id,
        "method": record.method,
        "total_time_s": _float_or_blank(record.total_time_s),
        "total_expansions": int(record.total_expansions),
        "success": bool(record.feasible),
        "path_length_m": _float_or_blank(record.path_length_m),
        "path_inflation_ratio": _float_or_blank(inflation),
        "direction_switches": int(record.direction_switches),
        "mean_abs_curvature": _float_or_blank(record.mean_abs_curvature),
        "min_clearance_m": _float_or_blank(record.min_clearance_m),
        "fallback_f1": int(record.fallback_f1_count),
        "fallback_f2": int(record.fallback_f2_count),
        "fallback_f3": int(record.fallback_f3_count),
        "profile_name": query.profile_name,
        "distance_bin": query.distance_bin_key,
        "map_seed": int(query.map_seed),
        "query_seed": int(query.query_seed),
        "failure_reason": record.failure_reason or "",
    }


def _float_or_blank(value: float | int | None) -> str:
    if value is None:
        return ""
    val = float(value)
    if not math.isfinite(val):
        return ""
    return f"{val:.9g}"


def _write_records_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "bucket",
        "query_id",
        "method",
        "total_time_s",
        "total_expansions",
        "success",
        "path_length_m",
        "path_inflation_ratio",
        "direction_switches",
        "mean_abs_curvature",
        "min_clearance_m",
        "fallback_f1",
        "fallback_f2",
        "fallback_f3",
        "profile_name",
        "distance_bin",
        "map_seed",
        "query_seed",
        "failure_reason",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _segment_sign(start: Pose, end: Pose, *, epsilon_m: float = 1e-6) -> int | None:
    dx = float(end[0]) - float(start[0])
    dy = float(end[1]) - float(start[1])
    if math.hypot(dx, dy) <= epsilon_m:
        return None
    forward_dot = math.cos(float(start[2])) * dx + math.sin(float(start[2])) * dy
    return 1 if forward_dot >= 0.0 else -1


def _switch_points(path: Iterable[Pose]) -> list[Pose]:
    poses = tuple(path)
    points: list[Pose] = []
    prev_sign: int | None = None
    for start, end in zip(poses[:-1], poses[1:], strict=True):
        sign = _segment_sign(start, end)
        if sign is None:
            continue
        if prev_sign is not None and sign != prev_sign:
            points.append(start)
        prev_sign = sign
    return points


def _plot_path_pair(
    *,
    output_path: Path,
    bucket: str,
    query_index: int,
    query: EvaluationQuery,
    grid_map: GridMap,
    vanilla_path: tuple[Pose, ...],
    fn3p_path: tuple[Pose, ...],
    vanilla_record: EvaluationRecord,
    fn3p_record: EvaluationRecord,
) -> None:
    grid = np.asarray(grid_map.data)
    height, width = grid.shape
    resolution = float(grid_map.resolution)
    extent = (
        float(grid_map.origin[0]),
        float(grid_map.origin[0]) + float(width) * resolution,
        float(grid_map.origin[1]),
        float(grid_map.origin[1]) + float(height) * resolution,
    )

    fig, ax = plt.subplots(figsize=(8.0, 8.0), dpi=150)
    ax.imshow(
        grid,
        origin="lower",
        extent=extent,
        cmap="gray_r",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    _plot_polyline(ax, vanilla_path, color="#1f77b4", linewidth=1.8)
    _plot_fn3p_segments(ax, fn3p_path)
    _plot_switch_markers(ax, _switch_points(fn3p_path))

    start = query.start
    goal = query.goal
    ax.scatter([start[0]], [start[1]], s=52, marker="o", color="#1a7f37", edgecolors="white", linewidths=0.7, zorder=5)
    ax.scatter([goal[0]], [goal[1]], s=70, marker="*", color="#b42318", edgecolors="white", linewidths=0.7, zorder=5)

    inflation = _format_metric(fn3p_record.path_inflation_ratio, suffix="")
    ax.set_title(
        (
            f"{bucket} q{query_index:02d} | infl {inflation} | "
            f"switch {fn3p_record.direction_switches} | "
            f"t f/v {fn3p_record.total_time_s:.2f}/{vanilla_record.total_time_s:.2f}s | "
            f"F1 {fn3p_record.fallback_f1_count}"
        ),
        fontsize=10,
    )
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.legend(handles=_legend_handles(), loc="upper right", framealpha=0.92, fontsize=8)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def _plot_polyline(ax: plt.Axes, path: Iterable[Pose], *, color: str, linewidth: float) -> None:
    points = np.asarray([(float(p[0]), float(p[1])) for p in path], dtype=np.float64)
    if points.shape[0] < 2:
        return
    ax.plot(points[:, 0], points[:, 1], color=color, linewidth=linewidth, zorder=3)


def _plot_fn3p_segments(ax: plt.Axes, path: Iterable[Pose]) -> None:
    poses = tuple(path)
    if len(poses) < 2:
        return
    _plot_polyline(ax, poses, color="#ff9f1c", linewidth=1.4)
    for start, end in zip(poses[:-1], poses[1:], strict=True):
        sign = _segment_sign(start, end)
        if sign is None:
            continue
        if sign < 0:
            ax.plot(
                [start[0], end[0]],
                [start[1], end[1]],
                color="#d62728",
                linewidth=2.7,
                alpha=0.95,
                zorder=4,
            )
    reverse_points = [
        start for start, end in zip(poses[:-1], poses[1:], strict=True) if _segment_sign(start, end) == -1
    ]
    if reverse_points:
        stride = max(1, len(reverse_points) // 20)
        xs = [float(p[0]) for p in reverse_points[::stride]]
        ys = [float(p[1]) for p in reverse_points[::stride]]
        us = [-0.35 * math.cos(float(p[2])) for p in reverse_points[::stride]]
        vs = [-0.35 * math.sin(float(p[2])) for p in reverse_points[::stride]]
        ax.quiver(xs, ys, us, vs, color="#d62728", angles="xy", scale_units="xy", scale=1.0, width=0.004, zorder=5)


def _plot_switch_markers(ax: plt.Axes, points: Iterable[Pose]) -> None:
    pts = tuple(points)
    if not pts:
        return
    ax.scatter(
        [float(p[0]) for p in pts],
        [float(p[1]) for p in pts],
        s=42,
        marker="D",
        color="#ffd166",
        edgecolors="#111111",
        linewidths=0.6,
        zorder=6,
    )


def _legend_handles() -> list[Line2D]:
    return [
        Line2D([0], [0], color="#1f77b4", linewidth=1.8, label="vanilla_ha"),
        Line2D([0], [0], color="#ff9f1c", linewidth=1.8, label="f_n3p_knn"),
        Line2D([0], [0], color="#d62728", linewidth=2.6, label="f_n3p reverse"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor="#ffd166", markeredgecolor="#111111", label="switch"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#1a7f37", markeredgecolor="white", label="start"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor="#b42318", markeredgecolor="white", label="goal"),
    ]


def _format_metric(value: float | int | None, *, suffix: str = "") -> str:
    if value is None:
        return "NA"
    val = float(value)
    if not math.isfinite(val):
        return "NA"
    return f"{val:.3f}{suffix}"


def _write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Forest Bucket Visualization Trial",
        "",
        "这是 `0_trials/` 下的一次性可视化试跑，非正式实验，不进 `.pipeline`，不可作为 claim 依据。",
        "",
        "| bucket | f_n3p speedup vs vanilla | success f/vanilla | path_inflation mean+max | mean direction_switches | F1 trigger rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    summary = _bucket_summary(rows)
    for bucket in BUCKETS:
        item = summary[bucket]
        lines.append(
            "| {bucket} | {speedup} | {success} | {inflation} | {switches} | {f1_rate} |".format(
                bucket=bucket,
                speedup=_format_metric(item["speedup"], suffix="x"),
                success=f"{item['fn3p_success_rate']:.2f}/{item['vanilla_success_rate']:.2f}",
                inflation=f"{_format_metric(item['inflation_mean'])}+{_format_metric(item['inflation_max'])}",
                switches=_format_metric(item["mean_direction_switches"]),
                f1_rate=f"{item['f1_trigger_rate']:.2f}",
            )
        )

    heavy_bucket = max(
        BUCKETS,
        key=lambda bucket: (
            summary[bucket]["mean_direction_switches"] if summary[bucket]["mean_direction_switches"] is not None else -1.0,
            summary[bucket]["inflation_max"] if summary[bucket]["inflation_max"] is not None else -1.0,
        ),
    )
    lines.extend(
        [
            "",
            (
                f"按 f_n3p 的平均方向切换次数优先、最大绕路比例次之看，"
                f"本次倒车/绕路最重的是 {heavy_bucket} 桶。"
            ),
            "",
            "## 源码改动清单",
            "",
            "本次未修改 `2_experiment/` 源码。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _bucket_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | None]]:
    out: dict[str, dict[str, float | None]] = {}
    for bucket in BUCKETS:
        f_rows = [row for row in rows if row["bucket"] == bucket and row["method"] == "f_n3p_knn"]
        v_rows = [row for row in rows if row["bucket"] == bucket and row["method"] == "vanilla_ha"]
        v_by_query = {row["query_id"]: row for row in v_rows}
        speedups: list[float] = []
        for f_row in f_rows:
            v_row = v_by_query.get(f_row["query_id"])
            f_time = _parse_float(f_row["total_time_s"])
            v_time = _parse_float(v_row["total_time_s"]) if v_row is not None else None
            if f_time is not None and v_time is not None and f_time > 0.0:
                speedups.append(v_time / f_time)
        inflations = [_parse_float(row["path_inflation_ratio"]) for row in f_rows]
        inflations = [value for value in inflations if value is not None]
        out[bucket] = {
            "speedup": _mean(speedups),
            "fn3p_success_rate": _success_rate(f_rows),
            "vanilla_success_rate": _success_rate(v_rows),
            "inflation_mean": _mean(inflations),
            "inflation_max": max(inflations) if inflations else None,
            "mean_direction_switches": _mean([float(row["direction_switches"]) for row in f_rows]),
            "f1_trigger_rate": _ratio(sum(1 for row in f_rows if int(row["fallback_f1"]) > 0), len(f_rows)),
        }
    return out


def _parse_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    val = float(value)
    return val if math.isfinite(val) else None


def _mean(values: Iterable[float]) -> float | None:
    vals = [float(value) for value in values if math.isfinite(float(value))]
    if not vals:
        return None
    return float(np.mean(np.asarray(vals, dtype=np.float64)))


def _success_rate(rows: list[dict[str, Any]]) -> float:
    return _ratio(sum(1 for row in rows if bool(row["success"])), len(rows))


def _ratio(numerator: int, denominator: int) -> float:
    return 0.0 if int(denominator) <= 0 else float(numerator) / float(denominator)


def _write_readme(path: Path) -> None:
    path.write_text(
        "这是 `0_trials/` 下的一次性森林场景可视化试跑，非正式实验，不进 `.pipeline`，不可作为 claim 依据。\n",
        encoding="utf-8",
    )


def run_trial(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir).resolve()
    figs_dir = output_dir / "figs"
    output_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    cfg = _trial_config(args)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    queries = build_query_set(cfg)
    predictors = _load_predictors(cfg, ("f_n3p_knn",))
    eval_cfg = EvaluationConfig()
    map_cache: dict[int, GridMap] = {}
    bucket_counts = {bucket: 0 for bucket in BUCKETS}
    rows: list[dict[str, Any]] = []

    for query in queries:
        grid_map = map_cache.get(query.map_seed)
        if grid_map is None:
            profile = _profile_by_name(cfg.profiles, query.profile_name)
            grid_map = _generate_grid_map(profile, query.map_seed, cfg, footprint)
            map_cache[query.map_seed] = grid_map

        vanilla_run = _run_vanilla_ha(query, grid_map, footprint, cfg, reference_path_length_m=None)
        vanilla_record = _evaluate_run_with_collision_rejection(vanilla_run, grid_map, footprint, config=eval_cfg)
        reference_length = vanilla_record.path_length_m if vanilla_record.feasible else None

        fn3p_run = _run_method(
            "f_n3p_knn",
            query,
            grid_map,
            footprint,
            cfg,
            predictors=predictors,
            reference_path_length_m=reference_length,
        )
        fn3p_record = _evaluate_run_with_collision_rejection(fn3p_run, grid_map, footprint, config=eval_cfg)

        rows.append(_record_row(query, vanilla_record, vanilla_reference_length_m=reference_length))
        rows.append(_record_row(query, fn3p_record, vanilla_reference_length_m=reference_length))

        query_index = bucket_counts[query.difficulty_bucket]
        bucket_counts[query.difficulty_bucket] += 1
        _plot_path_pair(
            output_path=figs_dir / f"{query.difficulty_bucket}_q{query_index:02d}.png",
            bucket=query.difficulty_bucket,
            query_index=query_index,
            query=query,
            grid_map=grid_map,
            vanilla_path=tuple(vanilla_run.path),
            fn3p_path=tuple(fn3p_run.path),
            vanilla_record=vanilla_record,
            fn3p_record=fn3p_record,
        )

        print(
            f"{query.difficulty_bucket} q{query_index:02d}: "
            f"vanilla_success={vanilla_record.feasible} fn3p_success={fn3p_record.feasible} "
            f"fn3p_switch={fn3p_record.direction_switches} f1={fn3p_record.fallback_f1_count}",
            flush=True,
        )

    _write_records_csv(output_dir / "trial_records.csv", rows)
    _write_summary(output_dir / "summary.md", rows)
    _write_readme(output_dir / "README.md")
    print(f"wrote {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a one-off ForestNav bucket visualization trial.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Trial output directory. Defaults to the directory containing this script.",
    )
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--queries-per-bucket", type=int, default=10)
    return parser.parse_args()


if __name__ == "__main__":
    run_trial(parse_args())
