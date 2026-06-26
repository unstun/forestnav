"""2D A* with footprint padding (Lian 2023 设计 §3.1.1)。"""
from __future__ import annotations

import heapq
import math
from typing import List, Optional, Tuple

import numpy as np

from forest_n3p.baselines.lian2023_paper_from_scratch.types import GridSpec


# ============================================================
# 8-邻域定义：(dx, dy, cost)
# ============================================================
_NEIGHBORS_8 = [
    (-1, -1, math.sqrt(2)), (-1, 0, 1.0), (-1, 1, math.sqrt(2)),
    ( 0, -1, 1.0),                        ( 0, 1, 1.0),
    ( 1, -1, math.sqrt(2)), ( 1, 0, 1.0), ( 1, 1, math.sqrt(2)),
]


def _padded_obstacle_grid(grid: np.ndarray, padding_cells: int) -> np.ndarray:
    """对障碍 grid 做形态学膨胀 padding_cells 次。
    用 8 邻域膨胀，每次扩 1 cell。
    """
    if padding_cells <= 0:
        return grid.astype(bool)
    cur = grid.astype(bool)
    for _ in range(int(padding_cells)):
        nxt = cur.copy()
        # 横向 ±1
        nxt[:, 1:]  |= cur[:, :-1]
        nxt[:, :-1] |= cur[:, 1:]
        # 纵向 ±1
        nxt[1:, :]  |= cur[:-1, :]
        nxt[:-1, :] |= cur[1:, :]
        # 对角
        nxt[1:, 1:]   |= cur[:-1, :-1]
        nxt[:-1, :-1] |= cur[1:, 1:]
        nxt[1:, :-1]  |= cur[:-1, 1:]
        nxt[:-1, 1:]  |= cur[1:, :-1]
        cur = nxt
    return cur


def astar_2d_path(
    *,
    grid_map: GridSpec,
    start_cell: Tuple[int, int],
    goal_cell: Tuple[int, int],
    padding_cells: int = 0,
) -> Optional[List[Tuple[int, int]]]:
    """2D A* 搜索（cell 坐标，y 上 x 右）。

    Args:
        grid_map: 占据网格（data[y, x] = 1 表示障碍）。
        start_cell: (x, y) 起点 cell。
        goal_cell: (x, y) 终点 cell。
        padding_cells: 障碍向外膨胀的 cell 数。

    Returns:
        cell 序列 [(x, y), ...]，或 None（无解 / 起终点本身被 padding 占据）。
    """
    grid = grid_map.data   # GridMap 用 .data 存储占据网格（非 .grid）
    H, W = grid.shape
    obs = _padded_obstacle_grid(grid, padding_cells)

    sx, sy = int(start_cell[0]), int(start_cell[1])
    gx, gy = int(goal_cell[0]), int(goal_cell[1])

    if not (0 <= sx < W and 0 <= sy < H and 0 <= gx < W and 0 <= gy < H):
        return None
    if obs[sy, sx] or obs[gy, gx]:
        return None

    def heuristic(x, y):
        return math.hypot(gx - x, gy - y)

    open_heap: list = []
    heapq.heappush(open_heap, (heuristic(sx, sy), 0.0, sx, sy))
    came_from: dict = {}
    g_score = {(sx, sy): 0.0}
    closed: set = set()

    while open_heap:
        _, g_cur, x, y = heapq.heappop(open_heap)
        if (x, y) in closed:
            continue
        closed.add((x, y))
        if (x, y) == (gx, gy):
            path = [(x, y)]
            while (x, y) in came_from:
                x, y = came_from[(x, y)]
                path.append((x, y))
            return list(reversed(path))
        for dx, dy, c in _NEIGHBORS_8:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            if obs[ny, nx]:
                continue
            tentative = g_cur + c
            if tentative < g_score.get((nx, ny), float("inf")):
                g_score[(nx, ny)] = tentative
                came_from[(nx, ny)] = (x, y)
                heapq.heappush(open_heap, (tentative + heuristic(nx, ny), tentative, nx, ny))
    return None
