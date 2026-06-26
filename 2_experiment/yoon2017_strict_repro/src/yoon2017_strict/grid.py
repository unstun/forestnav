from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GridMap:
    data: np.ndarray
    resolution: float = 1.0
    origin: tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        arr = np.asarray(self.data, dtype=np.uint8)
        if arr.ndim != 2:
            raise ValueError("GridMap data must be a 2D occupancy array")
        object.__setattr__(self, "data", arr)
        if not (float(self.resolution) > 0.0):
            raise ValueError("GridMap resolution must be positive")

    @property
    def shape(self) -> tuple[int, int]:
        return int(self.data.shape[0]), int(self.data.shape[1])

    @property
    def width(self) -> int:
        return int(self.data.shape[1])

    @property
    def height(self) -> int:
        return int(self.data.shape[0])

    def in_bounds(self, gx: int, gy: int) -> bool:
        return 0 <= int(gx) < self.width and 0 <= int(gy) < self.height

    def is_occupied_index(self, gx: int, gy: int) -> bool:
        if not self.in_bounds(gx, gy):
            return True
        return bool(self.data[int(gy), int(gx)] != 0)

    def world_to_grid(self, x_m: float, y_m: float) -> tuple[int, int]:
        ox, oy = self.origin
        gx = int(round((float(x_m) - float(ox)) / float(self.resolution)))
        gy = int(round((float(y_m) - float(oy)) / float(self.resolution)))
        return gx, gy

    def grid_to_world(self, gx: int, gy: int) -> tuple[float, float]:
        ox, oy = self.origin
        return (
            float(ox) + float(gx) * float(self.resolution),
            float(oy) + float(gy) * float(self.resolution),
        )

    def random_free_pose(self, rng: np.random.Generator) -> tuple[float, float, float]:
        free_y, free_x = np.nonzero(self.data == 0)
        if free_x.size == 0:
            raise ValueError("GridMap has no free cells")
        idx = int(rng.integers(0, free_x.size))
        x, y = self.grid_to_world(int(free_x[idx]), int(free_y[idx]))
        theta = float(rng.uniform(-np.pi, np.pi))
        return float(x), float(y), theta
