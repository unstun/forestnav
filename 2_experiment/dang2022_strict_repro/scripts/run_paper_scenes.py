#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dang2022_strict.config import paper_algorithm_params, paper_vehicle_params
from dang2022_strict.planner import DangHybridAStarPlanner
from dang2022_strict.render import render_scene_result
from dang2022_strict.scenes import build_scene, list_scene_names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--timeout-s", type=float, default=30.0)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    figure_data = []
    for name in list_scene_names():
        scene = build_scene(name)
        planner = DangHybridAStarPlanner(scene.grid_map(), paper_vehicle_params(), paper_algorithm_params())
        result = planner.plan(scene.start_pose(), scene.goal_pose(), timeout_s=float(args.timeout_s))
        render_scene_result(scene, result, out_dir / f"{name}.png")
        figure_data.append((scene, result))
        row = {
            "scene": name,
            "success": result.success,
            "elapsed_s": result.stats.get("elapsed_s", 0.0),
            "path_length_m": result.stats.get("path_length_m", 0.0),
            "turning_points": result.stats.get("turning_points", 0),
            "analytic_curvature": result.stats.get("analytic_curvature", ""),
            "analytic_cost": result.stats.get("analytic_cost", ""),
            "analytic_path_length_m": result.stats.get("analytic_path_length_m", ""),
            "failure_reason": result.stats.get("failure_reason", ""),
        }
        rows.append(row)

    with (out_dir / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    success = sum(1 for row in rows if bool(row["success"]))
    avg_time = sum(float(row["elapsed_s"]) for row in rows) / max(total, 1)
    avg_len = sum(float(row["path_length_m"]) for row in rows) / max(total, 1)
    with (out_dir / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=("n_total", "n_success", "success_rate", "elapsed_s_mean", "path_length_m_mean"),
        )
        writer.writeheader()
        writer.writerow(
            {
                "n_total": total,
                "n_success": success,
                "success_rate": success / max(total, 1),
                "elapsed_s_mean": avg_time,
                "path_length_m_mean": avg_len,
            }
        )

    fig, axes = plt.subplots(1, len(figure_data), figsize=(10, 3.4), squeeze=False)
    for ax, (scene, result) in zip(axes.ravel(), figure_data):
        ax.imshow(
            scene.grid,
            cmap="Greys",
            origin="lower",
            extent=(scene.bounds_m[0], scene.bounds_m[1], scene.bounds_m[2], scene.bounds_m[3]),
            interpolation="nearest",
        )
        if result.path:
            ax.plot([p.x for p in result.path], [p.y for p in result.path], color="#1f77b4", linewidth=2.0)
        if result.analytic_path:
            ax.plot([p.x for p in result.analytic_path], [p.y for p in result.analytic_path], color="#2ca02c", linewidth=2.0)
        ax.scatter([scene.start[0]], [scene.start[1]], c="#d62728", s=30)
        ax.scatter([scene.goal[0]], [scene.goal[1]], c="#9467bd", s=30)
        ax.set_title(f"{scene.name}: success={result.success}")
        ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(out_dir / "paths.png", dpi=150)
    plt.close(fig)

    with (out_dir / "RUN.md").open("w", encoding="utf-8") as f:
        f.write("# Dang2022 strict paper-scene smoke\n\n")
        f.write("This run uses reconstructed Map A/B occupancy grids from the paper figures. ")
        f.write("The exact author grids and Python scripts are not public in the paper bundle.\n\n")
        f.write("## Command\n\n")
        f.write("```bash\n")
        f.write(" ".join(["python", *sys.argv]) + "\n")
        f.write("```\n\n")
        f.write("## Result\n\n")
        for row in rows:
            f.write(
                f"- `{row['scene']}`: success `{row['success']}`, "
                f"elapsed `{float(row['elapsed_s']):.4f} s`, "
                f"path length `{float(row['path_length_m']):.4f} m`, "
                f"analytic curvature `{row['analytic_curvature']}`\n"
            )
        f.write("\n")
        f.write("## Outputs\n\n")
        for name in list_scene_names():
            f.write(f"- `{name}.png`\n")
        f.write("- `results.csv`\n")
        f.write("- `summary.csv`\n")
        f.write("- `paths.png`\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
