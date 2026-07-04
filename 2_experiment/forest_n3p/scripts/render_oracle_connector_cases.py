from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from forest_n3p.scripts.run_oracle_connector_analysis import (
    Candidate,
    CandidateSet,
    MapCacheKey,
    _append_without_duplicate,
    _distance_field_m,
    _generate_candidate_set,
    _grid_for_row,
    _metrics,
    _plan_disabled_ha,
    _pose_from_row,
    _profiles_from_bucket_mode,
    _safe_rs_check,
)
from forest_n3p.main_evaluation import MainEvaluationConfig
from forest_n3p.rs_utils import states_as_tuples
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


Pose = tuple[float, float, float]


@dataclass(frozen=True)
class RenderCase:
    case_id: str
    shape_label: str
    row: dict[str, Any]


@dataclass(frozen=True)
class BPath:
    success: bool
    selected_candidate: Candidate | None
    segment_poses: tuple[Pose, ...]
    terminal_rs_poses: tuple[Pose, ...]
    combined_poses: tuple[Pose, ...]
    failure_reason: str | None
    attempted: int


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render C02 oracle connector representative cases.")
    parser.add_argument("--results", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("0_trials/module2_oracle_shape/c02_shape_labels"))
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--source-head", default=None)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(args.results)
    df = _with_relation(df)
    cases = _select_cases(df, max_cases=int(args.max_cases))
    cfg = MainEvaluationConfig(
        seed=20260620,
        profiles=_profiles_from_bucket_mode("validation_t06"),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    oracle_args = _oracle_default_args()
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    map_cache: dict[MapCacheKey, GridMap] = {}
    records: list[dict[str, Any]] = []
    for case in cases:
        records.append(_render_case(case, cfg, oracle_args, footprint, map_cache, args.output_dir))

    summary = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": str(args.source_head) if args.source_head else None,
        "results": str(args.results),
        "output_dir": str(args.output_dir),
        "case_count": len(records),
        "cases": records,
    }
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_index_md(args.output_dir / "index.md", records)
    print(summary_path)
    print(args.output_dir / "index.md")
    for record in records:
        print(record["image"])
    return 0


def _with_relation(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    relation = pd.Series("unresolved", index=out.index)
    relation[out["oracle_a_success"] & out["oracle_b_success"]] = "both_success"
    relation[out["oracle_a_success"] & ~out["oracle_b_success"]] = "a_only"
    relation[~out["oracle_a_success"] & out["oracle_b_success"]] = "b_only"
    out["_relation"] = relation
    return out


def _select_cases(df: pd.DataFrame, *, max_cases: int) -> list[RenderCase]:
    specs: list[tuple[str, str, pd.Series]] = [
        (
            "invalid_goal_complex",
            "invalid_goal_in_collision",
            (df["difficulty_bucket"] == "Complex")
            & (df["query_id"] == "complex_s00_q0007")
            & (df["oracle_a_failure_reason"] == "goal_in_collision"),
        ),
        (
            "invalid_goal_extreme",
            "invalid_goal_in_collision",
            (df["difficulty_bucket"] == "Extreme")
            & (df["query_id"] == "extreme_s00_q0006")
            & (df["oracle_a_failure_reason"] == "goal_in_collision"),
        ),
        (
            "invalid_start_extreme",
            "invalid_start_in_collision_goal_also_blocked",
            (df["difficulty_bucket"] == "Extreme")
            & (df["query_id"] == "extreme_s00_q0006")
            & (df["oracle_a_failure_reason"] == "start_in_collision"),
        ),
        (
            "b_only_complex_timeout",
            "timeout_saved_by_goal_annulus",
            (df["_relation"] == "b_only") & (df["difficulty_bucket"] == "Complex"),
        ),
        (
            "b_only_extreme_goal_annulus",
            "timeout_saved_by_goal_annulus",
            (df["_relation"] == "b_only")
            & (df["difficulty_bucket"] == "Extreme")
            & (df["query_id"] == "extreme_s00_q0003")
            & (df["oracle_b_selected_candidate_source"] == "goal_annulus"),
        ),
        (
            "a_only_complex_conservative_b",
            "oracle_b_conservative_combined_collision_rejection",
            (df["_relation"] == "a_only") & (df["difficulty_bucket"] == "Complex"),
        ),
        (
            "a_only_extreme_conservative_b",
            "oracle_b_conservative_combined_collision_rejection",
            (df["_relation"] == "a_only") & (df["difficulty_bucket"] == "Extreme"),
        ),
    ]
    cases: list[RenderCase] = []
    for case_id, label, mask in specs:
        rows = df.loc[mask].sort_values(["query_id", "expansion_idx"])
        if rows.empty:
            continue
        cases.append(RenderCase(case_id=case_id, shape_label=label, row=dict(rows.iloc[0])))
        if len(cases) >= max_cases:
            break
    return cases


def _oracle_default_args() -> argparse.Namespace:
    return argparse.Namespace(
        oracle_a_timeout_s=8.0,
        oracle_a_max_nodes=50_000,
        oracle_b_segment_timeout_s=4.0,
        oracle_b_segment_max_nodes=25_000,
        oracle_b_candidate_limit=32,
        turning_radius_m=1.0,
        wheelbase_m=0.6,
        theta_bins=72,
        rs_sample_step_m=0.05,
        collision_padding_m=None,
        goal_annulus_radii_m="1.0,1.5,2.0,2.5,3.0",
        goal_annulus_angle_count=16,
        corridor_fractions="0.30,0.45,0.60,0.75",
        corridor_offsets_m="-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0",
        edt_margin_m=4.0,
        edt_grid_stride=4,
        edt_candidate_limit=24,
        disable_voronoi=False,
        voronoi_waypoint_spacing_m=3.0,
        voronoi_max_waypoints=48,
        voronoi_connector_count=24,
    )


def _render_case(
    case: RenderCase,
    cfg: MainEvaluationConfig,
    oracle_args: argparse.Namespace,
    footprint: TwoCircleFootprint,
    map_cache: dict[MapCacheKey, GridMap],
    output_dir: Path,
) -> dict[str, Any]:
    row = case.row
    grid_map = _grid_for_row(row, cfg, footprint, map_cache)
    edt_m = _distance_field_m(grid_map)
    state = _pose_from_row(row, "state")
    goal = _pose_from_row(row, "goal")
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=72, padding=None)
    state_collides = bool(checker.collides_pose(*state))
    goal_collides = bool(checker.collides_pose(*goal))

    oracle_a_poses: tuple[Pose, ...] = ()
    oracle_a_metrics: dict[str, Any] = {}
    if bool(row["oracle_a_success"]):
        oracle_a = _plan_disabled_ha(
            grid_map,
            footprint,
            cfg,
            state,
            goal,
            float(oracle_args.oracle_a_timeout_s),
            int(oracle_args.oracle_a_max_nodes),
        )
        oracle_a_poses = oracle_a.poses
        oracle_a_metrics = _metrics(grid_map, footprint, oracle_a_poses, collision_padding=None) if oracle_a.success else {}

    candidates = _generate_candidate_set(grid_map, footprint, edt_m, oracle_args, state, goal)
    b_path = BPath(False, None, (), (), (), None, 0)
    if bool(row["oracle_b_success"]):
        b_path = _run_oracle_b_path(grid_map, footprint, cfg, oracle_args, state, goal, candidates)

    image_path = output_dir / f"{case.case_id}.png"
    _plot_case(image_path, grid_map, state, goal, oracle_a_poses, b_path, row, case.shape_label, state_collides, goal_collides)

    return {
        "case_id": case.case_id,
        "shape_label": case.shape_label,
        "image": str(image_path),
        "query_id": str(row["query_id"]),
        "difficulty_bucket": str(row["difficulty_bucket"]),
        "map_seed": int(row["map_seed"]),
        "query_seed": int(row["query_seed"]),
        "expansion_idx": int(row["expansion_idx"]),
        "state": [float(v) for v in state],
        "goal": [float(v) for v in goal],
        "state_collides": state_collides,
        "goal_collides": goal_collides,
        "oracle_a_success": bool(row["oracle_a_success"]),
        "oracle_a_failure_reason": _none_or_str(row.get("oracle_a_failure_reason")),
        "oracle_a_path_length_m": _none_or_float(oracle_a_metrics.get("path_length_m") if oracle_a_metrics else row.get("oracle_a_path_length_m")),
        "oracle_b_success": bool(row["oracle_b_success"]),
        "oracle_b_failure_reason": _none_or_str(row.get("oracle_b_failure_reason")),
        "oracle_b_selected_candidate_source": _none_or_str(row.get("oracle_b_selected_candidate_source")),
        "rendered_b_success": bool(b_path.success),
        "rendered_b_attempted": int(b_path.attempted),
        "rendered_b_candidate": None
        if b_path.selected_candidate is None
        else [float(v) for v in b_path.selected_candidate.pose],
        "candidate_raw_count": int(row["candidate_raw_count"]),
        "candidate_rs_reachable_count": int(row["candidate_rs_reachable_count"]),
    }


def _run_oracle_b_path(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    args: argparse.Namespace,
    state: Pose,
    goal: Pose,
    candidate_set: CandidateSet,
) -> BPath:
    failures: list[str] = []
    for attempted, candidate in enumerate(candidate_set.candidates[: int(args.oracle_b_candidate_limit)], start=1):
        segment = _plan_disabled_ha(
            grid_map,
            footprint,
            cfg,
            state,
            candidate.pose,
            float(args.oracle_b_segment_timeout_s),
            int(args.oracle_b_segment_max_nodes),
        )
        if not segment.success or not segment.poses:
            failures.append(f"{candidate.source}:segment:{segment.failure_reason}")
            continue
        terminal_start = segment.poses[-1]
        terminal_rs = _safe_rs_check(grid_map, footprint, terminal_start, goal, args)
        if terminal_rs is None:
            failures.append(f"{candidate.source}:terminal_rs:no_path")
            continue
        if not terminal_rs.collision_free:
            failures.append(f"{candidate.source}:terminal_rs:collision")
            continue
        terminal_rs_poses = tuple(_clean_pose_for_render(pose) for pose in states_as_tuples(terminal_rs.samples))
        combined = _append_without_duplicate(segment.poses, terminal_rs_poses[1:])
        metrics = _metrics(grid_map, footprint, combined, collision_padding=None)
        if int(metrics["collision_violation_count"]) != 0:
            failures.append(f"{candidate.source}:combined_collision:{metrics['collision_violation_count']}")
            continue
        return BPath(
            success=True,
            selected_candidate=candidate,
            segment_poses=segment.poses,
            terminal_rs_poses=terminal_rs_poses,
            combined_poses=combined,
            failure_reason=None,
            attempted=attempted,
        )
    reason = "no_rs_reachable_candidates" if not candidate_set.candidates else "no_candidate_connected"
    if failures:
        reason = f"{reason};" + ";".join(failures[:8])
    return BPath(False, None, (), (), (), reason, min(len(candidate_set.candidates), int(args.oracle_b_candidate_limit)))


def _plot_case(
    output_path: Path,
    grid_map: GridMap,
    state: Pose,
    goal: Pose,
    oracle_a_poses: tuple[Pose, ...],
    b_path: BPath,
    row: dict[str, Any],
    shape_label: str,
    state_collides: bool,
    goal_collides: bool,
) -> None:
    grid = np.asarray(grid_map.data)
    res = float(grid_map.resolution)
    extent = (
        float(grid_map.origin[0]),
        float(grid_map.origin[0]) + grid.shape[1] * res,
        float(grid_map.origin[1]),
        float(grid_map.origin[1]) + grid.shape[0] * res,
    )
    fig, ax = plt.subplots(figsize=(8.2, 7.6), dpi=170)
    ax.imshow(grid, origin="lower", extent=extent, cmap="gray_r", interpolation="nearest", vmin=0, vmax=1)

    if oracle_a_poses:
        _plot_path(ax, oracle_a_poses, "#276ef1", "Oracle A HA* disabled", linewidth=2.0)
    if b_path.segment_poses:
        _plot_path(ax, b_path.segment_poses, "#f97316", "Oracle B segment", linewidth=2.0)
    if b_path.terminal_rs_poses:
        _plot_path(ax, b_path.terminal_rs_poses, "#c2410c", "Oracle B terminal RS", linewidth=1.7, linestyle="--")

    if b_path.selected_candidate is not None:
        cx, cy, _theta = b_path.selected_candidate.pose
        ax.scatter([cx], [cy], s=54, marker="D", color="#f59e0b", edgecolor="black", linewidth=0.5, label="B candidate")

    ax.scatter([state[0]], [state[1]], s=64, marker="o", color="#15803d", edgecolor="white", linewidth=0.8, label="failed node")
    ax.scatter([goal[0]], [goal[1]], s=104, marker="*", color="#dc2626", edgecolor="white", linewidth=0.8, label="goal")
    _draw_heading(ax, state, "#15803d")
    _draw_heading(ax, goal, "#dc2626")
    if state_collides:
        ax.scatter([state[0]], [state[1]], s=130, marker="x", color="#991b1b", linewidth=2.4, label="state collision")
    if goal_collides:
        ax.scatter([goal[0]], [goal[1]], s=150, marker="x", color="#7f1d1d", linewidth=2.6, label="goal collision")

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    title = (
        f"{shape_label} | {row['difficulty_bucket']} {row['query_id']} exp={int(row['expansion_idx'])}\n"
        f"A={bool(row['oracle_a_success'])}:{row.get('oracle_a_failure_reason')} "
        f"B={bool(row['oracle_b_success'])}:{row.get('oracle_b_selected_candidate_source')}"
    )
    ax.set_title(title, fontsize=9.5)
    _set_crop(ax, extent, (state, goal), oracle_a_poses, b_path.combined_poses)
    ax.legend(loc="upper right", fontsize=7.5, framealpha=0.88)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def _plot_path(ax: plt.Axes, poses: Iterable[Pose], color: str, label: str, *, linewidth: float, linestyle: str = "-") -> None:
    pts = tuple(poses)
    if not pts:
        return
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, linewidth=linewidth, linestyle=linestyle, label=label)


def _draw_heading(ax: plt.Axes, pose: Pose, color: str) -> None:
    ax.arrow(
        float(pose[0]),
        float(pose[1]),
        0.6 * math.cos(float(pose[2])),
        0.6 * math.sin(float(pose[2])),
        width=0.025,
        head_width=0.18,
        head_length=0.22,
        color=color,
        length_includes_head=True,
        alpha=0.9,
    )


def _set_crop(
    ax: plt.Axes,
    extent: tuple[float, float, float, float],
    anchors: tuple[Pose, Pose],
    oracle_a_poses: tuple[Pose, ...],
    oracle_b_poses: tuple[Pose, ...],
) -> None:
    points = list(anchors)
    points.extend(oracle_a_poses)
    points.extend(oracle_b_poses)
    xs = [float(p[0]) for p in points]
    ys = [float(p[1]) for p in points]
    margin = 3.0
    ax.set_xlim(max(extent[0], min(xs) - margin), min(extent[1], max(xs) + margin))
    ax.set_ylim(max(extent[2], min(ys) - margin), min(extent[3], max(ys) + margin))


def _write_index_md(path: Path, records: Sequence[dict[str, Any]]) -> None:
    lines = [
        "# C02 Oracle Shape Labels",
        "",
        "本目录保存 C02.2 的首批代表样本可视化。它只标注 full oracle 中的关键机械类别, 还不是最终 Gate #2 判定。",
        "",
        "| Case | Shape label | Query | Collides | A | B | Rendered B | Image |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for item in records:
        image = Path(str(item["image"])).name
        lines.append(
            "| {case_id} | `{shape_label}` | `{query_id}` exp={expansion_idx} | state={state_collides}, goal={goal_collides} | {a}:{ar} | {b}:{bs} | {rendered_b} | `{image}` |".format(
                case_id=item["case_id"],
                shape_label=item["shape_label"],
                query_id=item["query_id"],
                expansion_idx=item["expansion_idx"],
                state_collides=item["state_collides"],
                goal_collides=item["goal_collides"],
                a=item["oracle_a_success"],
                ar=item["oracle_a_failure_reason"],
                b=item["oracle_b_success"],
                bs=item["oracle_b_selected_candidate_source"],
                rendered_b=item["rendered_b_success"],
                image=image,
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _clean_pose_for_render(pose: Any) -> Pose:
    return (float(pose[0]), float(pose[1]), float(pose[2]))


def _none_or_str(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return str(value)


def _none_or_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


if __name__ == "__main__":
    raise SystemExit(main())
