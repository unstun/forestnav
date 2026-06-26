from __future__ import annotations

import math
from collections import deque

import numpy as np

from .scenes import PaperScene


def world_to_grid(scene: PaperScene, x: float, y: float) -> tuple[int, int]:
    xmin, _xmax, ymin, _ymax = scene.bounds_m
    ix = int(round((x - xmin) / scene.cell_size_m))
    iy = int(round((y - ymin) / scene.cell_size_m))
    return ix, iy


def grid_to_world(scene: PaperScene, ix: int, iy: int) -> tuple[float, float]:
    xmin, _xmax, ymin, _ymax = scene.bounds_m
    return xmin + ix * scene.cell_size_m, ymin + iy * scene.cell_size_m


def inflate_grid(grid: np.ndarray, radius_cells: int) -> np.ndarray:
    if radius_cells <= 0:
        return grid.copy()
    out = grid.copy().astype(np.uint8)
    ys, xs = np.nonzero(grid)
    h, w = grid.shape
    offsets: list[tuple[int, int]] = []
    for dy in range(-radius_cells, radius_cells + 1):
        for dx in range(-radius_cells, radius_cells + 1):
            if dx * dx + dy * dy <= radius_cells * radius_cells:
                offsets.append((dx, dy))
    for y, x in zip(ys, xs):
        for dx, dy in offsets:
            xx = x + dx
            yy = y + dy
            if 0 <= xx < w and 0 <= yy < h:
                out[yy, xx] = 1
    return out


def create_dilated_map(grid: np.ndarray, cell_size_m: float, radius_m: float) -> np.ndarray:
    radius_cells = int(math.ceil(float(radius_m) / max(float(cell_size_m), 1e-9)))
    return inflate_grid(grid, radius_cells)


def nearest_free(grid: np.ndarray, start: tuple[int, int]) -> tuple[int, int]:
    h, w = grid.shape
    sx, sy = start
    sx = min(max(sx, 0), w - 1)
    sy = min(max(sy, 0), h - 1)
    if grid[sy, sx] == 0:
        return sx, sy
    queue: deque[tuple[int, int]] = deque([(sx, sy)])
    seen = {(sx, sy)}
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            xx = x + dx
            yy = y + dy
            if not (0 <= xx < w and 0 <= yy < h) or (xx, yy) in seen:
                continue
            if grid[yy, xx] == 0:
                return xx, yy
            seen.add((xx, yy))
            queue.append((xx, yy))
    return sx, sy


def sample_line_is_free(grid: np.ndarray, a: tuple[int, int], b: tuple[int, int]) -> bool:
    ax, ay = a
    bx, by = b
    steps = max(abs(bx - ax), abs(by - ay), 1)
    for i in range(steps + 1):
        t = i / steps
        x = int(round((1.0 - t) * ax + t * bx))
        y = int(round((1.0 - t) * ay + t * by))
        if not (0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]):
            return False
        if grid[y, x] != 0:
            return False
    return True


def polyline_length(points: np.ndarray) -> float:
    if len(points) < 2:
        return 0.0
    diffs = np.diff(points[:, :2], axis=0)
    return float(np.sum(np.linalg.norm(diffs, axis=1)))


def angle_of_segment(a: np.ndarray, b: np.ndarray) -> float:
    return math.atan2(float(b[1] - a[1]), float(b[0] - a[0]))
