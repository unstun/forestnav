from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "2_experiment"))

from forest_n3p.inference import run_forest_n3p  # noqa: E402
from forest_n3p.main_evaluation import (  # noqa: E402
    MainEvaluationConfig,
    _generate_grid_map,
    _inference_config,
    _load_predictors,
    _profile_by_name,
    _run_vanilla_ha,
    build_query_set,
    validation_main_evaluation_profiles,
)
from forest_n3p.third_party.pathplan import TwoCircleFootprint  # noqa: E402


FIG_DIR = ROOT / "3_paper" / "figures"
T14_DIR = ROOT / ".pipeline" / "experiments" / "20260621_t14_formal_6method_rs_k20_collisionguard_validation_t06"
T15_DIR = ROOT / ".pipeline" / "experiments" / "20260623_t15_ablation_framework_validation_t06"
T16_DIR = ROOT / ".pipeline" / "experiments" / "20260623_t16_generalization_framework_t06"
REPRESENTATIVE_QUERY_ID = "extreme_s02_q0051"

METHOD_LABELS = {
    "vanilla_ha": "Vanilla Hybrid A*",
    "f_n3p_knn": "F-N3P",
    "n3p_k1": "N3P-style k=1",
    "voronoi_waypoint": "Voronoi",
    "bottleneck_waypoint": "Bottleneck",
    "md_dqn": "MD-DQN",
}

COLORS = {
    "vanilla_ha": "#6B7280",
    "f_n3p_knn": "#0072B2",
    "n3p_k1": "#D55E00",
    "voronoi_waypoint": "#009E73",
    "bottleneck_waypoint": "#CC79A7",
    "md_dqn": "#7F7F7F",
    "accent": "#E69F00",
    "negative": "#B23A48",
}


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "task": "T20",
        "generated_files": [],
        "sources": {
            "t14_summary": str(T14_DIR / "summary_by_method_bucket.csv"),
            "t14_records": str(T14_DIR / "records.csv"),
            "t14_queries": str(T14_DIR / "queries.csv"),
            "t15_ablation_summary": str(T15_DIR / "ablation_summary.csv"),
            "t16_summary": str(T16_DIR / "summary_by_method_bucket.csv"),
            "t16_verdict": str(T16_DIR / "verdict.json"),
        },
        "boundary": {
            "t14": "formal main evaluation",
            "t15": "framework-scale ablation snapshot",
            "t16": "framework-scale generalization snapshot; RealMap did not pass the time-benefit criterion",
        },
    }

    for stem, func in (
        ("t20_main_eval_bars", plot_main_eval_bars),
        ("t20_ablation_extreme", plot_ablation_extreme),
        ("t20_generalization_boundary", plot_generalization_boundary),
        ("t20_path_subgoals", plot_path_subgoals),
    ):
        result = func(stem)
        manifest["generated_files"].extend(result["files"])
        if "metadata" in result:
            manifest.setdefault("figure_metadata", {})[stem] = result["metadata"]

    manifest_path = FIG_DIR / "t20_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(manifest_path)
    for path in manifest["generated_files"]:
        print(path)
    return 0


def plot_main_eval_bars(stem: str) -> dict[str, Any]:
    rows = read_csv(T14_DIR / "summary_by_method_bucket.csv")
    methods = ("vanilla_ha", "f_n3p_knn", "n3p_k1", "voronoi_waypoint", "bottleneck_waypoint", "md_dqn")
    buckets = ("Easy", "Complex", "Extreme")
    lookup = {(row["method"], row["difficulty_bucket"]): row for row in rows}

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), dpi=180)
    x = np.arange(len(buckets), dtype=float)
    width = 0.12
    offsets = (np.arange(len(methods)) - (len(methods) - 1) / 2.0) * width

    for method, offset in zip(methods, offsets, strict=True):
        times = [float(lookup[(method, bucket)]["median_time_s"]) for bucket in buckets]
        rates = [100.0 * float(lookup[(method, bucket)]["feasible_rate"]) for bucket in buckets]
        label = METHOD_LABELS[method]
        axes[0].bar(x + offset, times, width=width, color=COLORS[method], label=label)
        axes[1].bar(x + offset, rates, width=width, color=COLORS[method], label=label)

    axes[0].set_yscale("log")
    axes[0].set_ylabel("Median planning time (s, log)")
    axes[1].set_ylabel("Feasible rate (%)")
    axes[1].set_ylim(0, 105)
    for ax, title in zip(axes, ("Planning time", "Feasible paths"), strict=True):
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(buckets)
        ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes[1].legend(loc="lower left", bbox_to_anchor=(1.02, 0.0), frameon=False, fontsize=8)
    fig.suptitle("Formal T14 evaluation: F-N3P is fastest without reducing feasibility", y=1.02)
    fig.tight_layout()
    return save_figure(fig, stem)


def plot_ablation_extreme(stem: str) -> dict[str, Any]:
    rows = read_csv(T15_DIR / "ablation_summary.csv")
    selected = (
        ("A2_knn_k20", "KNN k=20"),
        ("A2_mlp", "MLP"),
        ("A3_k1", "KNN k=1"),
        ("A4_no_density", "No density"),
        ("A7_no_f1", "No F1"),
        ("A7_no_f2", "No F2"),
    )
    lookup = {row["variant_id"]: row for row in rows if row["difficulty_bucket"] == "Extreme"}
    labels = [label for _vid, label in selected]
    reductions = [100.0 * float(lookup[vid]["median_time_reduction_vs_vanilla"]) for vid, _label in selected]
    f2 = [100.0 * float(lookup[vid]["fallback_f2_rate"]) for vid, _label in selected]
    f3 = [100.0 * float(lookup[vid]["fallback_f3_rate"]) for vid, _label in selected]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), dpi=180)
    y = np.arange(len(labels), dtype=float)
    axes[0].barh(y, reductions, color=[COLORS["f_n3p_knn"]] + ["#9CA3AF"] * (len(labels) - 1))
    axes[0].axvline(50.0, color="#333333", linestyle="--", linewidth=1.0)
    axes[0].set_xlabel("Median time reduction vs vanilla (%)")
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(labels)
    axes[0].invert_yaxis()
    axes[0].set_title("Extreme-bucket ablation trend", loc="left", fontweight="bold")

    axes[1].barh(y, f2, color="#56B4E9", label="F2 local planner")
    axes[1].barh(y, f3, left=f2, color=COLORS["negative"], label="F3 full fallback")
    axes[1].set_xlabel("Fallback trigger rate (%)")
    axes[1].set_yticks(y)
    axes[1].set_yticklabels([])
    axes[1].invert_yaxis()
    axes[1].set_title("Fallback cost", loc="left", fontweight="bold")
    axes[1].legend(frameon=False, fontsize=8)
    for ax in axes:
        ax.grid(axis="x", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("T15 framework-scale ablation snapshot; not final paper-scale evidence", y=1.02)
    fig.tight_layout()
    return save_figure(fig, stem)


def plot_generalization_boundary(stem: str) -> dict[str, Any]:
    rows = read_csv(T16_DIR / "summary_by_method_bucket.csv")
    lookup = {(row["method"], row["difficulty_bucket"]): row for row in rows}
    splits = ("OOD-Sparse", "OOD-Dense", "RealMap")
    reductions = []
    f_rates = []
    v_rates = []
    for split in splits:
        f_row = lookup[("f_n3p_knn", split)]
        v_row = lookup[("vanilla_ha", split)]
        f_time = float(f_row["median_time_s"])
        v_time = float(v_row["median_time_s"])
        reductions.append(100.0 * (1.0 - f_time / v_time))
        f_rates.append(100.0 * float(f_row["feasible_rate"]))
        v_rates.append(100.0 * float(v_row["feasible_rate"]))

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), dpi=180)
    x = np.arange(len(splits), dtype=float)
    bar_colors = [COLORS["f_n3p_knn"], COLORS["f_n3p_knn"], COLORS["negative"]]
    axes[0].bar(x, reductions, color=bar_colors, width=0.62)
    axes[0].axhline(20.0, color="#333333", linestyle="--", linewidth=1.0, label="RealMap criterion")
    axes[0].axhline(0.0, color="#666666", linewidth=0.8)
    axes[0].set_ylabel("Median time reduction vs vanilla (%)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(splits, rotation=20, ha="right")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].set_title("Time-transfer boundary", loc="left", fontweight="bold")

    width = 0.34
    axes[1].bar(x - width / 2, f_rates, width=width, color=COLORS["f_n3p_knn"], label="F-N3P")
    axes[1].bar(x + width / 2, v_rates, width=width, color=COLORS["vanilla_ha"], label="Vanilla")
    axes[1].set_ylim(0, 105)
    axes[1].set_ylabel("Feasible rate (%)")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(splits, rotation=20, ha="right")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].set_title("Feasibility", loc="left", fontweight="bold")
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("T16 framework-scale generalization snapshot; RealMap remains unresolved", y=1.02)
    fig.tight_layout()
    return save_figure(fig, stem)


def plot_path_subgoals(stem: str) -> dict[str, Any]:
    cfg = MainEvaluationConfig(
        methods=("vanilla_ha", "f_n3p_knn", "n3p_k1"),
        profiles=validation_main_evaluation_profiles(),
        k_neighbors=20,
        commit_verified_rs_segments=True,
        teacher_timeout_s=2.5,
        teacher_max_nodes=15_000,
        segment_timeout_s=1.0,
        segment_max_nodes=2_000,
        full_fallback_timeout_s=2.5,
        full_fallback_max_nodes=15_000,
    )
    query = next(item for item in build_query_set(cfg) if item.query_id == REPRESENTATIVE_QUERY_ID)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    profile = _profile_by_name(cfg.profiles, query.profile_name)
    grid_map = _generate_grid_map(profile, query.map_seed, cfg, footprint)
    predictors = _load_predictors(cfg, ("f_n3p_knn", "n3p_k1"))
    vanilla = _run_vanilla_ha(query, grid_map, footprint, cfg, reference_path_length_m=None)
    f_result = run_forest_n3p(
        grid_map,
        footprint,
        query.start,
        query.goal,
        predictors["knn"],
        config=_inference_config(cfg, k_neighbors=20, query_seed=query.query_seed),
    )
    k1_result = run_forest_n3p(
        grid_map,
        footprint,
        query.start,
        query.goal,
        predictors["knn"],
        config=_inference_config(cfg, k_neighbors=1, query_seed=query.query_seed),
    )

    grid = np.asarray(grid_map.data)
    extent = (
        float(grid_map.origin[0]),
        float(grid_map.origin[0]) + grid.shape[1] * float(grid_map.resolution),
        float(grid_map.origin[1]),
        float(grid_map.origin[1]) + grid.shape[0] * float(grid_map.resolution),
    )
    fig, ax = plt.subplots(figsize=(7.4, 7.1), dpi=180)
    ax.imshow(1 - grid, cmap="gray", origin="lower", extent=extent, alpha=0.95)
    draw_path(ax, vanilla.path, COLORS["vanilla_ha"], "Vanilla Hybrid A*", linestyle="--", linewidth=1.8)
    draw_path(ax, k1_result.path, COLORS["n3p_k1"], "N3P-style k=1", linestyle="-.", linewidth=1.6)
    draw_path(ax, f_result.path, COLORS["f_n3p_knn"], "F-N3P", linestyle="-", linewidth=2.2)

    subgoals = [step.target_pose for step in f_result.steps if step.neighbor_rank is not None]
    if subgoals:
        ax.scatter(
            [pose[0] for pose in subgoals],
            [pose[1] for pose in subgoals],
            marker="o",
            s=38,
            facecolors="white",
            edgecolors=COLORS["accent"],
            linewidths=1.5,
            label="F-N3P SE(2) subgoals",
            zorder=5,
        )
        for idx, pose in enumerate(subgoals[:12], start=1):
            ax.text(pose[0], pose[1], str(idx), fontsize=7, color="#111111", ha="center", va="center", zorder=6)

    ax.scatter([query.start[0]], [query.start[1]], s=70, color="#009E73", marker="s", label="start", zorder=7)
    ax.scatter([query.goal[0]], [query.goal[1]], s=80, color="#B23A48", marker="*", label="goal", zorder=7)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Representative Extreme query: {query.query_id}", loc="left", fontweight="bold")
    ax.text(
        0.01,
        0.01,
        (
            f"F-N3P: success={f_result.success}, steps={len(f_result.steps)}, "
            f"F1/F2/F3={f_result.used_f1}/{f_result.used_f2}/{f_result.used_f3}\n"
            f"Vanilla time={vanilla.total_time_s:.3f}s; F-N3P time={f_result.total_time_s:.3f}s"
        ),
        transform=ax.transAxes,
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#DDDDDD", "alpha": 0.9},
    )
    ax.legend(loc="upper right", fontsize=8, frameon=True)
    fig.tight_layout()

    out = save_figure(fig, stem)
    out["metadata"] = {
        "query": asdict(query),
        "vanilla": {
            "success": bool(vanilla.success),
            "time_s": float(vanilla.total_time_s),
            "expansions": int(vanilla.total_expansions),
            "path_pose_count": len(vanilla.path),
        },
        "f_n3p": {
            "success": bool(f_result.success),
            "time_s": float(f_result.total_time_s),
            "expansions": int(f_result.total_expansions),
            "used_f1": int(f_result.used_f1),
            "used_f2": int(f_result.used_f2),
            "used_f3": int(f_result.used_f3),
            "path_pose_count": len(f_result.path),
            "subgoal_count": len(subgoals),
        },
        "n3p_k1": {
            "success": bool(k1_result.success),
            "time_s": float(k1_result.total_time_s),
            "expansions": int(k1_result.total_expansions),
            "path_pose_count": len(k1_result.path),
        },
    }
    return out


def draw_path(ax: Any, poses: Iterable[tuple[float, float, float]], color: str, label: str, **kwargs: Any) -> None:
    points = tuple(poses)
    if not points:
        return
    ax.plot([pose[0] for pose in points], [pose[1] for pose in points], color=color, label=label, **kwargs)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_figure(fig: Any, stem: str) -> dict[str, Any]:
    pdf = FIG_DIR / f"{stem}.pdf"
    png = FIG_DIR / f"{stem}.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return {"files": [str(pdf.relative_to(ROOT)), str(png.relative_to(ROOT))]}


if __name__ == "__main__":
    raise SystemExit(main())
