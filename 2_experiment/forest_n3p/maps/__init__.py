"""Map specifications and loaders for F-N3P."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class MapSpec(Protocol):
    name: str
    start_xy: tuple[int, int]
    goal_xy: tuple[int, int]

    @property
    def size(self) -> tuple[int, int]: ...

    def obstacle_grid(self) -> np.ndarray: ...


@dataclass(frozen=True)
class ArrayGridMapSpec:
    """Occupancy grid map backed by a NumPy array.

    `grid_y0_bottom` has shape `(H, W)`, uses `1` for occupied cells, and places
    the grid origin at the lower-left corner.
    """

    name: str
    grid_y0_bottom: np.ndarray
    start_xy: tuple[int, int]
    goal_xy: tuple[int, int]

    @property
    def size(self) -> tuple[int, int]:
        h, w = self.grid_y0_bottom.shape
        return int(w), int(h)

    def obstacle_grid(self) -> np.ndarray:
        return self.grid_y0_bottom.astype(np.uint8, copy=True)


__all__ = ["ArrayGridMapSpec", "MapSpec"]
