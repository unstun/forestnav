from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

from .config import VehicleParams
from .planner import PlanResult
from .scenes import PaperScene


def render_scene_result(scene: PaperScene, result: PlanResult, vehicle: VehicleParams, out_path: str | Path) -> None:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
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
        ax.plot(xs, ys, color="#1f77b4", linewidth=2.0, label="SS-RRT*")
        stride = max(1, len(result.path) // 10)
        for pose in result.path[::stride]:
            rect = Rectangle(
                (-vehicle.rear_overhang_m, -0.5 * vehicle.width_m),
                vehicle.length_m,
                vehicle.width_m,
                facecolor="#1f77b4",
                edgecolor="#0b3358",
                alpha=0.14,
                linewidth=0.8,
            )
            rect.set_transform(Affine2D().rotate(pose.theta).translate(pose.x, pose.y) + ax.transData)
            ax.add_patch(rect)
    ax.scatter([scene.start[0]], [scene.start[1]], c="#d62728", s=45, label="start")
    ax.scatter([scene.goal[0]], [scene.goal[1]], c="#9467bd", s=55, marker="*", label="goal")
    ax.set_aspect("equal")
    ax.set_title(f"{scene.name}: success={result.success}")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
