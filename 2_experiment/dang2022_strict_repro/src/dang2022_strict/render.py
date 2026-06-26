from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .planner import PlanResult
from .scenes import PaperScene


def render_scene_result(scene: PaperScene, result: PlanResult, out_path: str | Path) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.imshow(
        scene.grid,
        cmap="Greys",
        origin="lower",
        extent=(scene.bounds_m[0], scene.bounds_m[1], scene.bounds_m[2], scene.bounds_m[3]),
        interpolation="nearest",
    )
    if result.path:
        xs = [p.x for p in result.path]
        ys = [p.y for p in result.path]
        ax.plot(xs, ys, color="#1f77b4", linewidth=2.0, label="Hybrid A*")
    if result.analytic_path:
        xs = [p.x for p in result.analytic_path]
        ys = [p.y for p in result.analytic_path]
        ax.plot(xs, ys, color="#2ca02c", linewidth=2.0, label="Analytic expansion")
    ax.scatter([scene.start[0]], [scene.start[1]], c="#d62728", s=40, label="start")
    ax.scatter([scene.goal[0]], [scene.goal[1]], c="#9467bd", s=40, label="goal")
    ax.set_title(f"{scene.name}: success={result.success}")
    ax.set_aspect("equal")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
