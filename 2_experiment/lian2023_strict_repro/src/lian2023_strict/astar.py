from __future__ import annotations

import heapq
import math

import numpy as np


def astar_grid(
    grid: np.ndarray,
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    h, w = grid.shape
    sx, sy = start
    gx, gy = goal
    if grid[sy, sx] != 0 or grid[gy, gx] != 0:
        return []

    moves = (
        (1, 0, 1.0),
        (-1, 0, 1.0),
        (0, 1, 1.0),
        (0, -1, 1.0),
        (1, 1, math.sqrt(2.0)),
        (1, -1, math.sqrt(2.0)),
        (-1, 1, math.sqrt(2.0)),
        (-1, -1, math.sqrt(2.0)),
    )
    heap: list[tuple[float, float, tuple[int, int]]] = []
    heapq.heappush(heap, (math.hypot(gx - sx, gy - sy), 0.0, (sx, sy)))
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    best = {(sx, sy): 0.0}

    while heap:
        _f, g, (x, y) = heapq.heappop(heap)
        if (x, y) == (gx, gy):
            out = [(x, y)]
            while out[-1] in parent:
                out.append(parent[out[-1]])
            return list(reversed(out))
        if g > best.get((x, y), float("inf")):
            continue
        for dx, dy, cost in moves:
            xx = x + dx
            yy = y + dy
            if not (0 <= xx < w and 0 <= yy < h):
                continue
            if grid[yy, xx] != 0:
                continue
            new_g = g + cost
            key = (xx, yy)
            if new_g >= best.get(key, float("inf")):
                continue
            best[key] = new_g
            parent[key] = (x, y)
            h_cost = math.hypot(gx - xx, gy - yy)
            heapq.heappush(heap, (new_g + h_cost, new_g, key))

    return []


def shortcut_path(grid: np.ndarray, path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    from .grid import sample_line_is_free

    if len(path) <= 2:
        return path
    out = [path[0]]
    i = 0
    while i < len(path) - 1:
        j = len(path) - 1
        while j > i + 1:
            if sample_line_is_free(grid, path[i], path[j]):
                break
            j -= 1
        out.append(path[j])
        i = j
    return out
