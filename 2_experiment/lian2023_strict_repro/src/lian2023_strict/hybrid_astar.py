from __future__ import annotations

import math
import heapq
import time

import numpy as np

from .config import AlgorithmParams, VehicleParams


def _world_to_grid_raw(bounds_m: tuple[float, float, float, float], cell: float, x: float, y: float) -> tuple[int, int]:
    xmin, _xmax, ymin, _ymax = bounds_m
    return int(round((x - xmin) / cell)), int(round((y - ymin) / cell))


def _grid_to_world_raw(bounds_m: tuple[float, float, float, float], cell: float, ix: int, iy: int) -> tuple[float, float]:
    xmin, _xmax, ymin, _ymax = bounds_m
    return xmin + ix * cell, ymin + iy * cell


def _theta_bin(theta: float, resolution: float) -> int:
    return int(round(((theta + math.pi) % (2.0 * math.pi)) / resolution))


def _angle_error(a: float, b: float) -> float:
    return abs((float(a) - float(b) + math.pi) % (2.0 * math.pi) - math.pi)


def _primitive_length(vehicle: VehicleParams, params: AlgorithmParams) -> float:
    max_turn = abs(math.tan(vehicle.max_steer_rad)) / max(vehicle.wheelbase_m, 1e-6)
    if max_turn <= 1e-9:
        return float(params.iha_xy_resolution_m)
    return max(
        float(params.iha_xy_resolution_m),
        1.2 * float(params.iha_heading_resolution_rad) / max_turn,
    )


def _propagate_primitive(
    *,
    grid: np.ndarray,
    bounds_m: tuple[float, float, float, float],
    cell_size_m: float,
    pose: tuple[float, float, float],
    distance_m: float,
    steer_rad: float,
    vehicle: VehicleParams,
) -> tuple[float, float, float] | None:
    h, w = grid.shape
    steps = max(1, int(math.ceil(abs(distance_m) / max(cell_size_m, 1e-6))))
    ds = distance_m / steps
    x, y, theta = pose
    for _ in range(steps):
        x += ds * math.cos(theta)
        y += ds * math.sin(theta)
        theta = (theta + ds * math.tan(steer_rad) / vehicle.wheelbase_m + math.pi) % (2.0 * math.pi) - math.pi
        ix, iy = _world_to_grid_raw(bounds_m, cell_size_m, x, y)
        if not (0 <= ix < w and 0 <= iy < h) or grid[iy, ix] != 0:
            return None
    return (x, y, theta)


def hybrid_astar_segment(
    *,
    grid: np.ndarray,
    bounds_m: tuple[float, float, float, float],
    cell_size_m: float,
    start: tuple[float, float, float],
    goal: tuple[float, float, float],
    vehicle: VehicleParams,
    params: AlgorithmParams,
    timeout_s: float = 5.0,
) -> np.ndarray:
    start_cell = _world_to_grid_raw(bounds_m, cell_size_m, start[0], start[1])
    goal_cell = _world_to_grid_raw(bounds_m, cell_size_m, goal[0], goal[1])
    h, w = grid.shape
    if not (0 <= start_cell[0] < w and 0 <= start_cell[1] < h):
        return np.empty((0, 3), dtype=float)
    if not (0 <= goal_cell[0] < w and 0 <= goal_cell[1] < h):
        return np.empty((0, 3), dtype=float)
    if grid[start_cell[1], start_cell[0]] or grid[goal_cell[1], goal_cell[0]]:
        return np.empty((0, 3), dtype=float)

    t0 = time.time()
    steer_values = (-vehicle.max_steer_rad, -0.5 * vehicle.max_steer_rad, 0.0, 0.5 * vehicle.max_steer_rad, vehicle.max_steer_rad)
    primitive_m = _primitive_length(vehicle, params)
    start_key = (start_cell[0], start_cell[1], _theta_bin(start[2], params.iha_heading_resolution_rad))
    heap: list[tuple[float, float, tuple[int, int, int], tuple[float, float, float]]] = []
    heapq.heappush(heap, (0.0, 0.0, start_key, start))
    parent: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    pose_by_key: dict[tuple[int, int, int], tuple[float, float, float]] = {start_key: start}
    best = {start_key: 0.0}

    while heap:
        if time.time() - t0 > timeout_s:
            return np.empty((0, 3), dtype=float)
        _f, g, key, pose = heapq.heappop(heap)
        if g > best.get(key, float("inf")):
            continue
        x, y, theta = pose
        xy_tol = max(params.iha_xy_resolution_m * 1.5, primitive_m * 0.75)
        heading_tol = max(float(params.iha_heading_resolution_rad), 1e-6)
        if math.hypot(x - goal[0], y - goal[1]) <= xy_tol and _angle_error(theta, goal[2]) <= heading_tol:
            path_keys = [key]
            while path_keys[-1] in parent:
                path_keys.append(parent[path_keys[-1]])
            path = [pose_by_key[k] for k in reversed(path_keys)]
            path.append(goal)
            return np.asarray(path, dtype=float)
        for direction in (1.0, -1.0):
            for delta in steer_values:
                next_pose = _propagate_primitive(
                    grid=grid,
                    bounds_m=bounds_m,
                    cell_size_m=cell_size_m,
                    pose=(x, y, theta),
                    distance_m=direction * primitive_m,
                    steer_rad=delta,
                    vehicle=vehicle,
                )
                if next_pose is None:
                    continue
                nx, ny, nth = next_pose
                ix, iy = _world_to_grid_raw(bounds_m, cell_size_m, nx, ny)
                nkey = (ix, iy, _theta_bin(nth, params.iha_heading_resolution_rad))
                cost = primitive_m * (1.2 if direction < 0.0 else 1.0) + 0.02 * abs(delta)
                ng = g + cost
                if ng >= best.get(nkey, float("inf")):
                    continue
                best[nkey] = ng
                parent[nkey] = key
                pose_by_key[nkey] = (nx, ny, nth)
                heuristic = math.hypot(nx - goal[0], ny - goal[1])
                heapq.heappush(heap, (ng + heuristic, ng, nkey, (nx, ny, nth)))
    return np.empty((0, 3), dtype=float)


def connect_boundary_points_with_hybrid_astar(
    *,
    grid: np.ndarray,
    bounds_m: tuple[float, float, float, float],
    cell_size_m: float,
    points: np.ndarray,
    vehicle: VehicleParams,
    params: AlgorithmParams,
    timeout_s: float = 5.0,
) -> np.ndarray:
    if len(points) < 2:
        return points.copy()
    out: list[np.ndarray] = []
    for idx in range(len(points) - 1):
        segment = hybrid_astar_segment(
            grid=grid,
            bounds_m=bounds_m,
            cell_size_m=cell_size_m,
            start=tuple(points[idx]),
            goal=tuple(points[idx + 1]),
            vehicle=vehicle,
            params=params,
            timeout_s=timeout_s,
        )
        if len(segment) == 0:
            return np.empty((0, 3), dtype=float)
        if out:
            segment = segment[1:]
        out.append(segment)
    return np.vstack(out)


def resample_pose_path(path: np.ndarray, n_elements: int) -> np.ndarray:
    if len(path) == 0:
        return np.empty((0, 3), dtype=float)
    if len(path) == 1:
        return np.repeat(path, n_elements + 1, axis=0)
    seg = np.linalg.norm(np.diff(path[:, :2], axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    if s[-1] <= 1e-9:
        return np.repeat(path[:1], n_elements + 1, axis=0)
    target = np.linspace(0.0, s[-1], n_elements + 1)
    x = np.interp(target, s, path[:, 0])
    y = np.interp(target, s, path[:, 1])
    theta = np.unwrap(path[:, 2])
    th = np.interp(target, s, theta)
    return np.column_stack([x, y, th])
