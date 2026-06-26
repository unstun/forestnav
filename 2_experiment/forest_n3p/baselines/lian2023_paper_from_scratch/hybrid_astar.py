"""Package-local Hybrid A* segment solver used by the strict Lian 2023 variant."""
from __future__ import annotations

import heapq
import math
import time
from dataclasses import dataclass
from typing import Iterable

from forest_n3p.baselines.lian2023_paper_from_scratch.types import GridSpec, VehicleDiscs, VehicleParams


@dataclass(frozen=True)
class _Node:
    x: float
    y: float
    theta: float
    g: float
    parent: int


def _wrap_angle(theta: float) -> float:
    return (float(theta) + math.pi) % (2.0 * math.pi) - math.pi


def _theta_bin(theta: float, bins: int) -> int:
    return int(round(((_wrap_angle(theta) + math.pi) / (2.0 * math.pi)) * bins)) % bins


def _pose_key(x: float, y: float, theta: float, *, cell: float, theta_bins: int) -> tuple[int, int, int]:
    return (
        int(round(float(x) / cell)),
        int(round(float(y) / cell)),
        _theta_bin(theta, theta_bins),
    )


def _disc_centers(x: float, y: float, theta: float, discs: VehicleDiscs) -> Iterable[tuple[float, float]]:
    c = math.cos(theta)
    s = math.sin(theta)
    if not discs.offsets_m:
        yield x, y
        return
    for offset in discs.offsets_m:
        yield x + float(offset) * c, y + float(offset) * s


def _circle_free(grid: GridSpec, cx: float, cy: float, radius_m: float) -> bool:
    data = grid.data
    cell = float(grid.resolution)
    h, w = data.shape
    ix = int(round(cx / cell))
    iy = int(round(cy / cell))
    r_cells = max(0, int(math.ceil(float(radius_m) / max(cell, 1e-9))))
    for yy in range(iy - r_cells, iy + r_cells + 1):
        for xx in range(ix - r_cells, ix + r_cells + 1):
            if not (0 <= xx < w and 0 <= yy < h):
                return False
            px = float(xx) * cell
            py = float(yy) * cell
            if math.hypot(px - cx, py - cy) <= float(radius_m) + 0.5 * cell:
                if data[yy, xx] != 0:
                    return False
    return True


def _pose_free(grid: GridSpec, x: float, y: float, theta: float, discs: VehicleDiscs) -> bool:
    radius = max(0.0, float(discs.radius_m))
    return all(_circle_free(grid, cx, cy, radius) for cx, cy in _disc_centers(x, y, theta, discs))


def _edge_free(
    grid: GridSpec,
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    discs: VehicleDiscs,
    *,
    samples: int = 4,
) -> bool:
    for i in range(samples + 1):
        t = float(i) / float(samples)
        x = (1.0 - t) * a[0] + t * b[0]
        y = (1.0 - t) * a[1] + t * b[1]
        theta = _wrap_angle(a[2] + t * _wrap_angle(b[2] - a[2]))
        if not _pose_free(grid, x, y, theta, discs):
            return False
    return True


def _expand(
    node: _Node,
    params: VehicleParams,
    *,
    step_m: float,
) -> Iterable[tuple[float, float, float, float]]:
    steer_values = (
        -float(params.delta_max_rad),
        -0.5 * float(params.delta_max_rad),
        0.0,
        0.5 * float(params.delta_max_rad),
        float(params.delta_max_rad),
    )
    for direction in (1.0, -1.0):
        for delta in steer_values:
            ds = direction * float(step_m)
            x = node.x + ds * math.cos(node.theta)
            y = node.y + ds * math.sin(node.theta)
            theta = _wrap_angle(
                node.theta
                + ds * math.tan(delta) / max(float(params.wheelbase_m), 1e-9)
            )
            reverse_penalty = 1.25 if direction < 0.0 else 1.0
            steer_penalty = 0.08 * abs(delta) / max(float(params.delta_max_rad), 1e-9)
            yield x, y, theta, float(step_m) * (reverse_penalty + steer_penalty)


def _reconstruct(nodes: list[_Node], idx: int) -> list[tuple[float, float, float]]:
    out: list[tuple[float, float, float]] = []
    while idx >= 0:
        node = nodes[idx]
        out.append((node.x, node.y, node.theta))
        idx = node.parent
    return list(reversed(out))


def plan_segment(
    *,
    grid: GridSpec,
    params: VehicleParams,
    discs: VehicleDiscs,
    start: tuple[float, float, float],
    goal: tuple[float, float, float],
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    timeout_s: float,
    max_nodes: int = 200_000,
    step_m: float = 0.3,
    theta_bins: int = 72,
) -> list[tuple[float, float, float]]:
    """Search one boundary-point segment with bicycle-model motion primitives."""
    if not _pose_free(grid, start[0], start[1], start[2], discs):
        return []
    if not _pose_free(grid, goal[0], goal[1], goal[2], discs):
        return []

    t0 = time.time()
    start_node = _Node(float(start[0]), float(start[1]), _wrap_angle(start[2]), 0.0, -1)
    nodes = [start_node]
    start_key = _pose_key(start_node.x, start_node.y, start_node.theta, cell=float(grid.resolution), theta_bins=theta_bins)
    best_g = {start_key: 0.0}
    heap: list[tuple[float, float, int]] = []
    heapq.heappush(heap, (math.hypot(goal[0] - start[0], goal[1] - start[1]), 0.0, 0))

    while heap and len(nodes) < int(max_nodes):
        if time.time() - t0 > float(timeout_s):
            return []
        _f, _g, idx = heapq.heappop(heap)
        node = nodes[idx]
        d_goal = math.hypot(goal[0] - node.x, goal[1] - node.y)
        d_theta = abs(_wrap_angle(goal[2] - node.theta))
        if d_goal <= float(goal_xy_tol_m) and d_theta <= float(goal_theta_tol_rad):
            path = _reconstruct(nodes, idx)
            if math.hypot(path[-1][0] - goal[0], path[-1][1] - goal[1]) > 1e-9:
                path.append((float(goal[0]), float(goal[1]), float(goal[2])))
            return path

        for nx, ny, nth, step_cost in _expand(node, params, step_m=float(step_m)):
            if not _edge_free(grid, (node.x, node.y, node.theta), (nx, ny, nth), discs):
                continue
            key = _pose_key(nx, ny, nth, cell=float(grid.resolution), theta_bins=theta_bins)
            new_g = node.g + step_cost
            if new_g >= best_g.get(key, float("inf")):
                continue
            best_g[key] = new_g
            new_idx = len(nodes)
            nodes.append(_Node(nx, ny, nth, new_g, idx))
            heuristic = math.hypot(goal[0] - nx, goal[1] - ny)
            heapq.heappush(heap, (new_g + heuristic, new_g, new_idx))

    return []
