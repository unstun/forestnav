from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .config import AlgorithmParams
from .ocp import lse_local_state_constraint
from .planner import TrajectoryResult
from .scenes import PaperScene


def render_scene_result(scene: PaperScene, result: TrajectoryResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    for obstacle in scene.obstacles:
        closed = np.vstack([obstacle, obstacle[0]])
        ax.fill(closed[:, 0], closed[:, 1], color="0.45", edgecolor="0.1", linewidth=0.8)
    if len(result.coarse_path):
        ax.plot(result.coarse_path[:, 0], result.coarse_path[:, 1], color="#ff4cc3", linewidth=1.2, label="coarse")
    if len(result.boundary_points):
        ax.scatter(result.boundary_points[:, 0], result.boundary_points[:, 1], color="#00a65a", s=24, label="BP")
    if len(result.states):
        ax.plot(result.states[:, 0], result.states[:, 1], color="#d7191c", linewidth=2.0, label="optimized")
    ax.scatter([scene.start[0], scene.goal[0]], [scene.start[1], scene.goal[1]], c=["black", "blue"], s=30)
    ax.set_xlim(scene.bounds_m[0], scene.bounds_m[1])
    ax.set_ylim(scene.bounds_m[2], scene.bounds_m[3])
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x / m")
    ax.set_ylabel("y / m")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def render_velocity_profile(result: TrajectoryResult, path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    n = np.arange(len(result.states))
    axes[0, 0].plot(n, result.states[:, 3])
    axes[0, 0].set_ylabel("v / m/s")
    axes[0, 1].plot(n[:-1], result.controls[:, 1])
    axes[0, 1].set_ylabel("omega / rad/s")
    axes[1, 0].plot(n[:-1], result.controls[:, 0])
    axes[1, 0].set_ylabel("a / m/s^2")
    axes[1, 1].plot(n, result.states[:, 4])
    axes[1, 1].set_ylabel("phi / rad")
    for ax in axes.ravel():
        ax.set_xlabel("n")
        ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def render_local_constraint(scene: PaperScene, results: list[TrajectoryResult], params: AlgorithmParams, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for obstacle in scene.obstacles:
        closed = np.vstack([obstacle, obstacle[0]])
        axes[0].fill(closed[:, 0], closed[:, 1], color="0.5", edgecolor="0.2", linewidth=0.5)
    xa, xb, ya, yb = params.local_area
    axes[0].fill([xa, xb, xb, xa], [ya, ya, yb, yb], color="#ffd54f", alpha=0.45)
    for result in results:
        axes[0].plot(result.states[:, 0], result.states[:, 1], label=result.method.value)
        penalty = [
            lse_local_state_constraint(px, py, abs(v), params.local_area, params.local_speed_bounds_m_s, params.beta)
            for px, py, v in result.states[:, [0, 1, 3]]
        ]
        axes[1].plot(penalty, label=result.method.value)
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].set_xlim(scene.bounds_m[0], scene.bounds_m[1])
    axes[0].set_ylim(scene.bounds_m[2], scene.bounds_m[3])
    axes[0].set_xlabel("x / m")
    axes[0].set_ylabel("y / m")
    axes[1].set_xlabel("n")
    axes[1].set_ylabel("local constraint surrogate")
    axes[0].legend(fontsize=7)
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)
