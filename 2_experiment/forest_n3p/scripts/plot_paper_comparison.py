from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np

try:
    import seaborn as sns
except ModuleNotFoundError:  # pragma: no cover - 本地轻量环境允许退回 matplotlib 样式。
    sns = None


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIGURE_DIR = PROJECT_ROOT / "2_experiment" / "forest_n3p" / "figures"
BUCKETS = ("Easy", "Complex", "Extreme")
METHODS = ("f_n3p_knn", "vanilla_ha", "improved_ha", "lo_ha", "ss_rrt", "idb_rrt")
METHOD_LABELS = {
    "f_n3p_knn": "F-N3P",
    "vanilla_ha": "HA*",
    "improved_ha": "Imp-HA*",
    "lo_ha": "LO-HA*",
    "ss_rrt": "SS-RRT*",
    "idb_rrt": "IDB-RRT",
}
COLORS = {
    "f_n3p_knn": "#D55E00",
    "vanilla_ha": "#0072B2",
    "improved_ha": "#009E73",
    "lo_ha": "#E69F00",
    "ss_rrt": "#CC79A7",
    "idb_rrt": "#56B4E9",
}
LINESTYLES = {
    "f_n3p_knn": "-",
    "vanilla_ha": "--",
    "improved_ha": "-.",
    "lo_ha": ":",
    "ss_rrt": (0, (5, 1.5)),
    "idb_rrt": (0, (3, 1.2, 1, 1.2)),
}
FALLBACK_COLORS = {
    "Primary": "#009E73",
    "F1": "#E69F00",
    "F2": "#CC79A7",
    "F3": "#4D4D4D",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot paper-style F-N3P vs vanilla HA* comparison figures from local_50trial JSON."
    )
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--format", choices=("png", "pdf"), default="png")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    _configure_style()

    runs = _runs_by_query_method(payload.get("runs", ()))
    maps = _decode_maps(payload.get("maps", {}))

    figure1 = output_dir / f"figure1_trajectory_overlay.{args.format}"
    figure2 = output_dir / f"figure2_grouped_metrics.{args.format}"
    figure3 = output_dir / f"figure3_fallback_stack.{args.format}"
    table1 = output_dir / "table1_quantitative_comparison.tex"

    plot_trajectory_overlay(figure1, runs, maps, dpi=int(args.dpi))
    plot_grouped_metrics(figure2, payload.get("runs", ()), dpi=int(args.dpi))
    plot_fallback_stack(figure3, payload.get("runs", ()), dpi=int(args.dpi))
    table1.write_text(render_latex_table(payload.get("runs", ())), encoding="utf-8")

    print(
        json.dumps(
            {
                "figure1": str(figure1),
                "figure2": str(figure2),
                "figure3": str(figure3),
                "table1": str(table1),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def plot_trajectory_overlay(
    output_path: Path,
    runs: dict[tuple[str, str], dict[str, Any]],
    maps: dict[str, dict[str, Any]],
    *,
    dpi: int,
) -> None:
    cases = _select_representative_cases(runs)
    if len(cases) < 6:
        raise RuntimeError(f"need 6 representative paired cases, found {len(cases)}")

    fig, axes = plt.subplots(2, 3, figsize=(7.2, 5.1), dpi=dpi, constrained_layout=True)
    for ax, query_id in zip(axes.flat, cases, strict=True):
        fn3p = runs[(query_id, "f_n3p_knn")]
        map_info = maps.get(str(fn3p["map_seed"]))
        if map_info is None:
            raise KeyError(f"missing map payload for map_seed={fn3p['map_seed']}")
        _plot_map_background(ax, map_info)
        for method in METHODS:
            run = runs.get((query_id, method))
            if run is None:
                continue
            _plot_path(
                ax,
                run.get("path", ()),
                method=method,
                linestyle=LINESTYLES[method],
                linewidth=1.9 if method == "f_n3p_knn" else 1.05,
            )
        subgoals = fn3p.get("subgoals", ())
        if subgoals:
            xs = [float(pose[0]) for pose in subgoals]
            ys = [float(pose[1]) for pose in subgoals]
            ax.scatter(xs, ys, s=15, marker="o", color=COLORS["f_n3p_knn"], edgecolors="white", linewidths=0.35, zorder=5)
        start = fn3p["start"]
        goal = fn3p["goal"]
        ax.scatter([start[0]], [start[1]], s=42, marker="^", color="#009E73", edgecolors="white", linewidths=0.45, zorder=6)
        ax.scatter([goal[0]], [goal[1]], s=54, marker="*", color=COLORS["f_n3p_knn"], edgecolors="white", linewidths=0.45, zorder=6)
        fn_time = _metric(fn3p, "planning_time_s")
        ha_time = _metric(runs.get((query_id, "vanilla_ha"), {}), "planning_time_s")
        ax.set_title(f"{fn3p['difficulty_bucket']} | F-N3P {fn_time:.2f}s / HA* {ha_time:.2f}s")
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.tick_params(labelsize=7)

    handles = [
        *[
            plt.Line2D(
                [0],
                [0],
                color=COLORS[method],
                lw=1.9 if method == "f_n3p_knn" else 1.05,
                ls=LINESTYLES[method],
                label=METHOD_LABELS[method],
            )
            for method in METHODS
        ],
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["f_n3p_knn"], markeredgecolor="white", label="Subgoal", markersize=5),
        plt.Line2D([0], [0], marker="^", color="none", markerfacecolor="#009E73", markeredgecolor="white", label="Start", markersize=6),
        plt.Line2D([0], [0], marker="*", color="none", markerfacecolor=COLORS["f_n3p_knn"], markeredgecolor="white", label="Goal", markersize=7),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.08))
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def plot_grouped_metrics(output_path: Path, runs: Sequence[dict[str, Any]], *, dpi: int) -> None:
    metrics = (
        ("success_rate", "Success rate (%)", "mean_std"),
        ("planning_time_s", "Median planning time (s)", "median_iqr"),
        ("path_length", "Path length (m)", "mean_std"),
        ("mean_abs_curvature", "Mean abs. curvature (rad/m)", "mean_std"),
    )
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2), dpi=dpi, constrained_layout=True)
    for ax, (metric, title, mode) in zip(axes.flat, metrics, strict=True):
        x = np.arange(len(BUCKETS), dtype=np.float64)
        width = min(0.12, 0.78 / float(len(METHODS)))
        offsets = (np.arange(len(METHODS), dtype=np.float64) - (len(METHODS) - 1) / 2.0) * width
        for offset, method in zip(offsets, METHODS, strict=True):
            centers = x + offset
            heights: list[float] = []
            yerrs: list[Any] = []
            for bucket in BUCKETS:
                values = _values(runs, method=method, bucket=bucket, metric=metric)
                if mode == "median_iqr":
                    center, err = _median_iqr(values)
                else:
                    center, err = _mean_std(values)
                heights.append(0.0 if center is None else center)
                yerrs.append(err)
            yerr = _format_yerr(yerrs)
            ax.bar(
                centers,
                heights,
                width=width,
                color=COLORS[method],
                edgecolor="black",
                linewidth=0.35,
                label=METHOD_LABELS[method],
                yerr=yerr,
                capsize=2.5,
                error_kw={"linewidth": 0.7},
            )
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(BUCKETS)
        ax.set_ylabel(title)
        ax.grid(axis="y", color="#D0D0D0", linewidth=0.5, alpha=0.8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes.flat[0].legend(frameon=False, loc="best")
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def plot_fallback_stack(output_path: Path, runs: Sequence[dict[str, Any]], *, dpi: int) -> None:
    fig, ax = plt.subplots(figsize=(5.0, 3.1), dpi=dpi, constrained_layout=True)
    levels = ("Primary", "F1", "F2", "F3")
    bottom = np.zeros(len(BUCKETS), dtype=np.float64)
    x = np.arange(len(BUCKETS), dtype=np.float64)
    for level in levels:
        values = np.asarray([_fallback_pct(runs, bucket, level) for bucket in BUCKETS], dtype=np.float64)
        ax.bar(
            x,
            values,
            bottom=bottom,
            color=FALLBACK_COLORS[level],
            edgecolor="black",
            linewidth=0.35,
            label=level,
            width=0.58,
        )
        bottom += values
    ax.set_xticks(x)
    ax.set_xticklabels(BUCKETS)
    ax.set_ylim(0, 100)
    ax.set_ylabel("F-N3P query share (%)")
    ax.set_title("Fallback usage by difficulty")
    ax.grid(axis="y", color="#D0D0D0", linewidth=0.5, alpha=0.8)
    ax.legend(frameon=False, loc="upper right", ncol=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def render_latex_table(runs: Sequence[dict[str, Any]]) -> str:
    rows = _table_rows(runs)
    lines = [
        "% Auto-generated by plot_paper_comparison.py",
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Quantitative comparison by difficulty bucket.}",
        "\\label{tab:forest_n3p_quantitative}",
        "\\begin{tabular}{llrrrrrr}",
        "\\toprule",
        "Difficulty & Method & Success (\\%) & Time med. (s) & Time P95 (s) & Path (m) & Inflation (\\%) & Curvature (rad/m) \\\\",
        "\\midrule",
    ]
    for bucket in BUCKETS:
        bucket_rows = [row for row in rows if row["difficulty_bucket"] == bucket]
        best = _best_values(bucket_rows)
        for row in bucket_rows:
            values = [
                bucket,
                METHOD_LABELS[row["method"]],
                _latex_metric(row["success_rate"], best["success_rate"], higher_is_better=True, fmt="{:.1f}"),
                _latex_metric(row["time_median_s"], best["time_median_s"], higher_is_better=False, fmt="{:.3f}"),
                _latex_metric(row["time_p95_s"], best["time_p95_s"], higher_is_better=False, fmt="{:.3f}"),
                _latex_metric(row["path_length_m"], best["path_length_m"], higher_is_better=False, fmt="{:.2f}"),
                _latex_metric(row["path_inflation_pct"], best["path_inflation_pct"], higher_is_better=False, fmt="{:.2f}"),
                _latex_metric(row["mean_abs_curvature"], best["mean_abs_curvature"], higher_is_better=False, fmt="{:.4f}"),
            ]
            lines.append(" & ".join(values) + " \\\\")
        if bucket != BUCKETS[-1]:
            lines.append("\\midrule")
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


def _table_rows(runs: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bucket in BUCKETS:
        for method in METHODS:
            group = [run for run in runs if run.get("difficulty_bucket") == bucket and run.get("method") == method]
            rows.append(
                {
                    "difficulty_bucket": bucket,
                    "method": method,
                    "success_rate": _mean(_values(group, method=None, bucket=None, metric="success_rate")),
                    "time_median_s": _percentile(_values(group, method=None, bucket=None, metric="planning_time_s"), 50.0),
                    "time_p95_s": _percentile(_values(group, method=None, bucket=None, metric="planning_time_s"), 95.0),
                    "path_length_m": _mean(_values(group, method=None, bucket=None, metric="path_length")),
                    "path_inflation_pct": _mean(_values(group, method=None, bucket=None, metric="path_inflation_pct")),
                    "mean_abs_curvature": _mean(_values(group, method=None, bucket=None, metric="mean_abs_curvature")),
                }
            )
    return rows


def _select_representative_cases(runs: dict[tuple[str, str], dict[str, Any]]) -> list[str]:
    selected: list[str] = []
    for bucket in BUCKETS:
        candidates: list[tuple[float, str]] = []
        for query_id, method in sorted(runs):
            if method != "f_n3p_knn":
                continue
            fn3p = runs[(query_id, method)]
            vanilla = runs.get((query_id, "vanilla_ha"))
            if vanilla is None:
                continue
            if fn3p.get("difficulty_bucket") != bucket:
                continue
            if not fn3p.get("path") or not vanilla.get("path"):
                continue
            time_value = _metric(fn3p, "planning_time_s")
            if math.isfinite(time_value):
                candidates.append((time_value, query_id))
        if len(candidates) < 2:
            raise RuntimeError(f"need at least two paired drawable cases for bucket={bucket}")
        candidates.sort()
        idx_a = max(0, int(round(0.35 * (len(candidates) - 1))))
        idx_b = min(len(candidates) - 1, int(round(0.65 * (len(candidates) - 1))))
        picks = [candidates[idx_a][1], candidates[idx_b][1]]
        if picks[0] == picks[1]:
            picks[1] = candidates[min(len(candidates) - 1, idx_b + 1)][1]
        selected.extend(picks)
    return selected


def _plot_map_background(ax: plt.Axes, map_info: dict[str, Any]) -> None:
    grid = np.asarray(map_info["grid"], dtype=np.uint8)
    resolution = float(map_info["resolution_m"])
    origin = map_info["origin"]
    extent = (
        float(origin[0]),
        float(origin[0]) + grid.shape[1] * resolution,
        float(origin[1]),
        float(origin[1]) + grid.shape[0] * resolution,
    )
    # free=white, occupied=light gray，路径颜色保持最高对比。
    image = np.where(grid > 0, 0.62, 1.0)
    ax.imshow(image, cmap="gray", origin="lower", vmin=0.0, vmax=1.0, extent=extent, interpolation="nearest")


def _plot_path(
    ax: plt.Axes,
    path: Iterable[Sequence[float]],
    *,
    method: str,
    linestyle: str,
    linewidth: float,
) -> None:
    poses = list(path)
    if len(poses) < 2:
        return
    ax.plot(
        [float(pose[0]) for pose in poses],
        [float(pose[1]) for pose in poses],
        color=COLORS[method],
        linestyle=linestyle,
        linewidth=linewidth,
        solid_capstyle="round",
        zorder=4,
    )


def _runs_by_query_method(runs: Sequence[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(str(run["query_id"]), str(run["method"])): run for run in runs}


def _decode_maps(raw_maps: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for key, item in raw_maps.items():
        shape = tuple(int(v) for v in item["shape"])
        out[str(key)] = {
            **item,
            "grid": _rle_decode(item["occupancy_rle"], shape=shape),
        }
    return out


def _rle_decode(rle: Sequence[Sequence[int]], *, shape: tuple[int, int]) -> np.ndarray:
    values: list[int] = []
    for value, count in rle:
        values.extend([int(value)] * int(count))
    arr = np.asarray(values, dtype=np.uint8)
    expected = int(shape[0]) * int(shape[1])
    if arr.size != expected:
        raise ValueError(f"RLE size mismatch: got {arr.size}, expected {expected}")
    return arr.reshape(shape)


def _values(
    runs: Sequence[dict[str, Any]],
    *,
    method: str | None,
    bucket: str | None,
    metric: str,
) -> list[float]:
    out: list[float] = []
    for run in runs:
        if method is not None and run.get("method") != method:
            continue
        if bucket is not None and run.get("difficulty_bucket") != bucket:
            continue
        value = run.get("metrics", {}).get(metric)
        if value is None:
            continue
        number = float(value)
        if math.isfinite(number):
            out.append(number)
    return out


def _metric(run: dict[str, Any], metric: str) -> float:
    value = run.get("metrics", {}).get(metric)
    if value is None:
        return float("nan")
    return float(value)


def _fallback_pct(runs: Sequence[dict[str, Any]], bucket: str, level: str) -> float:
    group = [run for run in runs if run.get("method") == "f_n3p_knn" and run.get("difficulty_bucket") == bucket]
    if not group:
        return 0.0
    return 100.0 * sum(1 for run in group if run.get("fallback", {}).get("level") == level) / float(len(group))


def _mean_std(values: Sequence[float]) -> tuple[float | None, float]:
    if not values:
        return None, 0.0
    arr = np.asarray(values, dtype=np.float64)
    std = float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0
    return float(np.mean(arr)), std


def _median_iqr(values: Sequence[float]) -> tuple[float | None, tuple[float, float]]:
    if not values:
        return None, (0.0, 0.0)
    arr = np.asarray(values, dtype=np.float64)
    median = float(np.percentile(arr, 50.0))
    q25 = float(np.percentile(arr, 25.0))
    q75 = float(np.percentile(arr, 75.0))
    return median, (max(0.0, median - q25), max(0.0, q75 - median))


def _format_yerr(errors: Sequence[Any]) -> np.ndarray:
    if not errors:
        return np.zeros((2, 0), dtype=np.float64)
    if isinstance(errors[0], tuple):
        lower = [float(item[0]) for item in errors]
        upper = [float(item[1]) for item in errors]
        return np.asarray([lower, upper], dtype=np.float64)
    return np.asarray([float(item) for item in errors], dtype=np.float64)


def _mean(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return float(np.mean(np.asarray(values, dtype=np.float64)))


def _percentile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.percentile(np.asarray(values, dtype=np.float64), float(q)))


def _best_values(rows: Sequence[dict[str, Any]]) -> dict[str, float | None]:
    return {
        "success_rate": _best(rows, "success_rate", higher_is_better=True),
        "time_median_s": _best(rows, "time_median_s", higher_is_better=False),
        "time_p95_s": _best(rows, "time_p95_s", higher_is_better=False),
        "path_length_m": _best(rows, "path_length_m", higher_is_better=False),
        "path_inflation_pct": _best(rows, "path_inflation_pct", higher_is_better=False),
        "mean_abs_curvature": _best(rows, "mean_abs_curvature", higher_is_better=False),
    }


def _best(rows: Sequence[dict[str, Any]], key: str, *, higher_is_better: bool) -> float | None:
    values = [float(row[key]) for row in rows if row.get(key) is not None and math.isfinite(float(row[key]))]
    if not values:
        return None
    return max(values) if higher_is_better else min(values)


def _latex_metric(
    value: float | None,
    best: float | None,
    *,
    higher_is_better: bool,
    fmt: str,
) -> str:
    if value is None or not math.isfinite(float(value)):
        return "--"
    text = fmt.format(float(value))
    if best is None:
        return text
    is_best = math.isclose(float(value), float(best), rel_tol=1e-9, abs_tol=1e-9)
    if is_best:
        return f"\\textbf{{{text}}}"
    return text


def _configure_style() -> None:
    rc = {
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    if sns is not None:
        sns.set_theme(context="paper", style="whitegrid", rc=rc)
    else:
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
        plt.rcParams.update(rc)


if __name__ == "__main__":
    raise SystemExit(main())
