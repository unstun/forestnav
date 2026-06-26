from __future__ import annotations

import numpy as np
from scipy.ndimage import distance_transform_edt, maximum_filter

from .grid import GridMap


def _compute_gvd_distance(grid_map: GridMap) -> np.ndarray:
    free_mask = grid_map.data == 0
    if not np.any(free_mask):
        return np.full(grid_map.data.shape, np.inf, dtype=np.float32)
    obstacle_distance = distance_transform_edt(free_mask)
    local_max = obstacle_distance >= maximum_filter(obstacle_distance, size=3, mode="nearest")
    skeleton = local_max & free_mask & (obstacle_distance > 0.0)
    if not np.any(skeleton):
        return np.zeros(grid_map.data.shape, dtype=np.float32)
    return (distance_transform_edt(~skeleton) * grid_map.resolution).astype(np.float32)


def compute_voronoi_field(grid_map: GridMap, alpha: float = 5.0, d_o_max: float = 5.0) -> np.ndarray:
    if float(alpha) <= 0.0:
        raise ValueError("alpha must be > 0")
    if float(d_o_max) <= 0.0:
        raise ValueError("d_o_max must be > 0")
    free_mask = grid_map.data == 0
    d_o = (distance_transform_edt(free_mask) * grid_map.resolution).astype(np.float32)
    d_v = _compute_gvd_distance(grid_map)
    factor_a = float(alpha) / (float(alpha) + d_o)
    denom = d_o + d_v
    factor_b = np.where(denom > 1e-12, d_v / np.maximum(denom, 1e-12), 0.0)
    falloff = np.clip((float(d_o_max) - d_o) / float(d_o_max), 0.0, 1.0)
    field = factor_a * factor_b * falloff * falloff
    field[~free_mask] = 0.0
    return field.astype(np.float32)


def query_voronoi_field(field: np.ndarray, grid_map: GridMap, x: float, y: float) -> float:
    gx, gy = grid_map.world_to_grid(x, y)
    if not grid_map.in_bounds(gx, gy):
        return 0.0
    return float(field[gy, gx])
