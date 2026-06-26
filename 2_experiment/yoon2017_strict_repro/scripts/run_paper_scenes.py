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

from yoon2017_strict.config import paper_algorithm_params, paper_sim_vehicle_params
from yoon2017_strict.planner import YoonSplineRRTStarPlanner
from yoon2017_strict.render import render_scene_result
from yoon2017_strict.scenes import build_scene, list_scene_names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--timeout-s", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    vehicle = paper_sim_vehicle_params()
    rows: list[dict[str, object]] = []
    figure_data = []
    for idx, name in enumerate(list_scene_names()):
        scene = build_scene(name)
        params = paper_algorithm_params(max_iterations=8_000)
        planner = YoonSplineRRTStarPlanner(scene.grid_map(), vehicle, params)
        result = planner.plan(scene.start_pose(), scene.goal_pose(), seed=int(args.seed) + idx, timeout_s=float(args.timeout_s))
        render_scene_result(scene, result, vehicle, out_dir / f"{name}.png")
        figure_data.append((scene, result))
        rows.append(
            {
                "scene": name,
                "success": result.success,
                "elapsed_s": result.stats.get("elapsed_s", 0.0),
                "iterations": result.stats.get("iterations", 0),
                "nodes": result.stats.get("nodes", 0),
                "path_length_m": result.stats.get("path_length_m", 0.0),
                "failure_reason": result.stats.get("failure_reason", ""),
            }
        )

    with (out_dir / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (out_dir / "summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=("n_total", "n_success", "success_rate"))
        writer.writeheader()
        writer.writerow({"n_total": len(rows), "n_success": sum(bool(r["success"]) for r in rows), "success_rate": sum(bool(r["success"]) for r in rows) / max(1, len(rows))})

    fig, axes = plt.subplots(1, len(figure_data), figsize=(10, 3.6), squeeze=False)
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
        ax.scatter([scene.start[0]], [scene.start[1]], c="#d62728", s=35)
        ax.scatter([scene.goal[0]], [scene.goal[1]], c="#9467bd", s=45, marker="*")
        ax.set_title(f"{scene.name}: success={result.success}")
        ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(out_dir / "paths.png", dpi=150)
    plt.close(fig)

    with (out_dir / "RUN.md").open("w", encoding="utf-8") as f:
        f.write("# Yoon2017 strict paper-scene smoke\n\n")
        f.write("This run uses reconstructed smoke scenes. The author MATLAB source and exact simulation maps are not public in the paper bundle.\n\n")
        f.write("## Command\n\n")
        f.write("```bash\n")
        f.write(" ".join(["python", *sys.argv]) + "\n")
        f.write("```\n\n")
        f.write("## Vehicle\n\n")
        f.write("- `a_f=3.4 m`, `a_r=0.8 m`, `a_w=1.8 m`, `r_min=4.8 m`\n\n")
        f.write("## Result\n\n")
        for row in rows:
            f.write(f"- `{row['scene']}`: success `{row['success']}`, elapsed `{float(row['elapsed_s']):.4f} s`, path length `{float(row['path_length_m']):.4f} m`\n")
        f.write("\n## Outputs\n\n")
        f.write("- `results.csv`\n- `summary.csv`\n- `paths.png`\n")
        for name in list_scene_names():
            f.write(f"- `{name}.png`\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
