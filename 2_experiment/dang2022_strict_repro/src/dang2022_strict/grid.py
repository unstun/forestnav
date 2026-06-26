from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class GridMap:
    data: np.ndarray
    resolution: float = 1.0
    origin: Tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        data = np.asarray(self.data, dtype=np.uint8)
        if data.ndim != 2:
            raise ValueError("data must be a 2D occupancy grid")
        if not (float(self.resolution) > 0.0):
            raise ValueError("resolution must be > 0")
        object.__setattr__(self, "data", data)
        object.__setattr__(self, "resolution", float(self.resolution))

    @property
    def height(self) -> int:
        return int(self.data.shape[0])

    @property
    def width(self) -> int:
        return int(self.data.shape[1])

    def in_bounds(self, gx: int, gy: int) -> bool:
        return 0 <= int(gx) < self.width and 0 <= int(gy) < self.height

    def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        gx = int(round((float(x) - self.origin[0]) / self.resolution))
        gy = int(round((float(y) - self.origin[1]) / self.resolution))
        return gx, gy

    def grid_to_world(self, gx: int, gy: int) -> tuple[float, float]:
        return (
            float(self.origin[0]) + int(gx) * self.resolution,
            float(self.origin[1]) + int(gy) * self.resolution,
        )

    def is_occupied_index(self, gx: int, gy: int) -> bool:
        if not self.in_bounds(gx, gy):
            return True
        return bool(self.data[int(gy), int(gx)])
