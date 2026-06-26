from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .geometry import Pose
from .grid import GridMap


@dataclass(frozen=True)
class PaperScene:
    name: str
    bounds_m: tuple[float, float, float, float]
    cell_size_m: float
    grid: np.ndarray
    start: tuple[float, float, float]
    goal: tuple[float, float, float]
    note: str

    def grid_map(self) -> GridMap:
        return GridMap(self.grid, resolution=self.cell_size_m, origin=(self.bounds_m[0], self.bounds_m[2]))

    def start_pose(self) -> Pose:
        return Pose(*self.start)

    def goal_pose(self) -> Pose:
        return Pose(*self.goal)


def _empty_grid(width: int, height: int) -> np.ndarray:
    grid = np.zeros((height, width), dtype=np.uint8)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    return grid


def _rect(grid: np.ndarray, x0: int, y0: int, x1: int, y1: int) -> None:
    grid[int(y0) : int(y1) + 1, int(x0) : int(x1) + 1] = 1


def build_scene(name: str) -> PaperScene:
    if name == "narrow_passage":
        grid = _empty_grid(80, 50)
        _rect(grid, 1, 1, 35, 19)
        _rect(grid, 1, 31, 35, 48)
        _rect(grid, 45, 1, 78, 19)
        _rect(grid, 45, 31, 78, 48)
        return PaperScene(
            "narrow_passage",
            (0.0, 40.0, 0.0, 25.0),
            0.5,
            grid,
            (5.0, 12.5, 0.0),
            (35.0, 12.5, 0.0),
            "Reconstructed Yoon2017 narrow-passage style smoke scene; exact MATLAB scene is not public.",
        )
    if name == "open_turn":
        grid = _empty_grid(70, 50)
        return PaperScene(
            "open_turn",
            (0.0, 35.0, 0.0, 25.0),
            0.5,
            grid,
            (5.0, 5.0, math.radians(20.0)),
            (30.0, 20.0, math.radians(80.0)),
            "Reconstructed open-turn smoke scene for SS-RRT* geometry checks.",
        )
    raise ValueError(f"unknown Yoon2017 scene: {name}")


def list_scene_names() -> tuple[str, ...]:
    return ("narrow_passage", "open_turn")
