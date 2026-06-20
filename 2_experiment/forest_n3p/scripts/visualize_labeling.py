from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from forest_n3p.labeling import LabelingConfig, extract_subgoal_labels
from forest_n3p.rs_utils import generate_reeds_shepp_path, sample_reeds_shepp_path
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    TwoCircleFootprint,
)


def build_gate_map() -> GridMap:
    grid = np.zeros((300, 300), dtype=np.uint8)
    grid[:, 100] = 1
    grid[120:180, 100] = 0
    grid[:, 200] = 1
    grid[120:180, 200] = 0
    return GridMap(grid, resolution=0.1, origin=(0.0, 0.0))


def plan_teacher_path(grid_map: GridMap, footprint: TwoCircleFootprint) -> tuple[list[AckermannState], dict]:
    params = AckermannParams(wheelbase=0.6, min_turn_radius=1.0)
    planner = HybridAStarPlanner(
        grid_map,
        footprint,
        params,
        analytic_expansion=True,
        collision_step=0.1,
        goal_xy_tol=0.3,
        goal_theta_tol=math.radians(15.0),
        use_holonomic_heuristic=True,
        theta_bins=72,
    )
    start = AckermannState(2.0, 15.0, 0.0)
    goal = AckermannState(28.0, 15.0, 0.0)
    path, stats = planner.plan(start, goal, timeout=5.0, max_nodes=20_000)
    if not path:
        raise RuntimeError(f"Hybrid A* failed: {stats}")
    return path, stats


def _pose_list(path: list[AckermannState], stats: dict) -> list[tuple[float, float, float]]:
    trace = stats.get("trace_poses")
    if trace:
        return [(float(x), float(y), float(theta)) for x, y, theta in trace]
    return [state.as_tuple() for state in path]


def draw_labeling_demo(
    grid_map: GridMap,
    teacher: list[tuple[float, float, float]],
    result,
    *,
    output_path: Path,
) -> None:
    grid = grid_map.data
    h, w = grid.shape
    res = float(grid_map.resolution)
    extent = (-0.5 * res, (w - 0.5) * res, -0.5 * res, (h - 0.5) * res)
    fig, ax = plt.subplots(figsize=(9.0, 6.8), dpi=160)
    ax.imshow(
        grid,
        origin="lower",
        extent=extent,
        cmap="gray_r",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    teacher_xy = np.asarray([(p[0], p[1]) for p in teacher], dtype=np.float64)
    ax.plot(teacher_xy[:, 0], teacher_xy[:, 1], color="#276ef1", linewidth=2.0, label="Hybrid A* teacher")

    start = teacher[0]
    goal = teacher[-1]
    ax.plot(start[0], start[1], marker="o", markersize=8, color="#1a7f37", label="start")
    ax.plot(goal[0], goal[1], marker="*", markersize=12, color="#b42318", label="goal")

    for idx, sample in enumerate(result.samples, start=1):
        sg = sample.subgoal_pose
        ax.plot(sg[0], sg[1], marker="D", markersize=6, color="#f2994a")
        ax.text(sg[0] + 0.25, sg[1] + 0.25, f"g{idx}", color="#9a3412", fontsize=9)
        rs_path = generate_reeds_shepp_path(
            sample.current_pose,
            sample.subgoal_pose,
            turning_radius=1.0,
        )
        rs_states = sample_reeds_shepp_path(
            sample.current_pose,
            rs_path,
            turning_radius=1.0,
            wheelbase=0.6,
            sample_step=0.1,
        )
        rs_xy = np.asarray([(s.x, s.y) for s in rs_states], dtype=np.float64)
        ax.plot(rs_xy[:, 0], rs_xy[:, 1], color="#f2994a", linewidth=1.2, linestyle="--")

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(
        f"T04 forward-greedy RS labels: {len(result.samples)} samples, "
        f"Lmax=8m, checks={result.candidate_checks}"
    )
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize F-N3P T04 subgoal labeling.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/t04_labeling_visual"),
        help="Directory for the labeling visualization and summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    grid_map = build_gate_map()
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    path, stats = plan_teacher_path(grid_map, footprint)
    teacher = _pose_list(path, stats)
    config = LabelingConfig(
        l_max_m=8.0,
        l_min_m=1.5,
        path_sample_step_m=0.2,
        turning_radius_m=1.0,
        wheelbase_m=0.6,
        rs_sample_step_m=0.1,
    )
    result = extract_subgoal_labels(grid_map, footprint, teacher, config=config)
    if not result.success:
        raise RuntimeError(f"Label extraction failed: {result.failure_reason}")

    image_path = args.output_dir / "labeling_demo.png"
    draw_labeling_demo(grid_map, teacher, result, output_path=image_path)

    summary = {
        "image": str(image_path),
        "planner_stats": {
            key: value
            for key, value in stats.items()
            if key not in {"trace_poses", "trace_boxes"}
        },
        "teacher_trace_count": len(teacher),
        "label_success": result.success,
        "failure_reason": result.failure_reason,
        "path_length_m": result.path_length_m,
        "candidate_checks": result.candidate_checks,
        "subgoals": [[float(v) for v in pose] for pose in result.subgoals],
        "samples": [
            {
                "current_pose": [float(v) for v in sample.current_pose],
                "subgoal_pose": [float(v) for v in sample.subgoal_pose],
                "delta_body": [float(v) for v in sample.delta_body],
                "s_start_m": float(sample.s_start_m),
                "s_subgoal_m": float(sample.s_subgoal_m),
                "rs_length_m": float(sample.rs_length_m),
                "rs_sample_count": int(sample.rs_sample_count),
                "feature_dim": int(sample.feature_vector.shape[0]),
            }
            for sample in result.samples
        ],
    }
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(image_path)
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
