from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .grid import GridMap
from .robot import Pose


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


def _empty_scene_grid() -> np.ndarray:
    grid = np.zeros((31, 51), dtype=np.uint8)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    return grid


def _rect(grid: np.ndarray, x0: int, y0: int, x1: int, y1: int) -> None:
    grid[int(y0) : int(y1) + 1, int(x0) : int(x1) + 1] = 1


def build_scene(name: str) -> PaperScene:
    bounds = (0.0, 50.0, 0.0, 30.0)
    cell = 1.0
    if name == "map_a":
        grid = _empty_scene_grid()
        _rect(grid, 8, 4, 13, 9)
        _rect(grid, 8, 21, 13, 26)
        _rect(grid, 21, 3, 26, 8)
        _rect(grid, 21, 22, 26, 27)
        _rect(grid, 34, 4, 39, 9)
        _rect(grid, 34, 21, 39, 26)
        return PaperScene(
            "map_a",
            bounds,
            cell,
            grid,
            (5.0, 6.0, 0.0),
            (45.0, 24.0, math.pi / 2.0),
            "Reconstructed 50 x 30 m Dang2022 Grid map A from paper figures; exact author occupancy grid is not public.",
        )
    if name == "map_b":
        grid = _empty_scene_grid()
        _rect(grid, 7, 4, 14, 8)
        _rect(grid, 7, 20, 14, 25)
        _rect(grid, 22, 4, 28, 8)
        _rect(grid, 22, 20, 28, 25)
        _rect(grid, 36, 4, 43, 8)
        _rect(grid, 36, 20, 43, 25)
        return PaperScene(
            "map_b",
            bounds,
            cell,
            grid,
            (5.0, 15.0, 0.0),
            (45.0, 6.0, -math.pi / 2.0),
            "Reconstructed 50 x 30 m Dang2022 Grid map B from paper figures; exact author occupancy grid is not public.",
        )
    raise ValueError(f"unknown Dang2022 scene: {name}")


def list_scene_names() -> tuple[str, ...]:
    return ("map_a", "map_b")
