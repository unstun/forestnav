from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from forest_n3p.third_party.pathplan import GridMap


Pose = tuple[float, float, float]
Point = tuple[float, float]


@dataclass(frozen=True)
class FeatureConfig:
    n_ray: int = 32
    r_max_m: float = 10.0
    density_rings_m: tuple[tuple[float, float], ...] = (
        (0.0, 2.0),
        (2.0, 5.0),
        (5.0, 10.0),
    )
    motion_flag_default: float = 0.0

    def __post_init__(self) -> None:
        if int(self.n_ray) <= 0:
            raise ValueError("n_ray must be positive")
        if not (math.isfinite(float(self.r_max_m)) and float(self.r_max_m) > 0.0):
            raise ValueError("r_max_m must be finite and positive")
        for ring in self.density_rings_m:
            if len(ring) != 2:
                raise ValueError("each density ring must be (inner, outer)")
            inner, outer = float(ring[0]), float(ring[1])
            if not (math.isfinite(inner) and math.isfinite(outer) and 0.0 <= inner < outer):
                raise ValueError("density rings must satisfy 0 <= inner < outer")


@dataclass(frozen=True)
class FeatureExtraction:
    vector: np.ndarray
    target_features: tuple[float, float, float, float, float]
    ray_distances_m: np.ndarray
    ray_angles_rad: np.ndarray
    density_ratios: np.ndarray
    motion_flag: float


def wrap_pi(angle_rad: float) -> float:
    return float(math.atan2(math.sin(float(angle_rad)), math.cos(float(angle_rad))))


def relative_goal_features(current_pose: Pose, goal_pose: Pose) -> tuple[float, float, float, float, float]:
    x, y, theta = (float(v) for v in current_pose)
    gx, gy, gtheta = (float(v) for v in goal_pose)

    dx = gx - x
    dy = gy - y
    distance = float(math.hypot(dx, dy))

    c = math.cos(theta)
    s = math.sin(theta)
    local_x = c * dx + s * dy
    local_y = -s * dx + c * dy
    bearing = math.atan2(local_y, local_x)

    heading_delta = wrap_pi(gtheta - theta)
    return (
        float(math.log1p(distance)),
        float(math.sin(bearing)),
        float(math.cos(bearing)),
        float(math.sin(heading_delta)),
        float(math.cos(heading_delta)),
    )


def ray_angles(n_ray: int) -> np.ndarray:
    if int(n_ray) <= 0:
        raise ValueError("n_ray must be positive")
    return (np.arange(int(n_ray), dtype=np.float64) * (2.0 * math.pi / float(n_ray))).astype(
        np.float64,
        copy=False,
    )


def _grid_continuous(map_: GridMap, x: float, y: float) -> tuple[float, float]:
    return (
        (float(x) - float(map_.origin[0])) / float(map_.resolution),
        (float(y) - float(map_.origin[1])) / float(map_.resolution),
    )


def _nearest_cell_index(map_: GridMap, x: float, y: float) -> tuple[int, int]:
    cx, cy = _grid_continuous(map_, x, y)
    return int(math.floor(cx + 0.5)), int(math.floor(cy + 0.5))


def _cell_is_occupied(map_: GridMap, gx: int, gy: int) -> bool:
    return bool(map_.is_occupied_index(int(gx), int(gy)))


def ray_cast_distance(
    map_: GridMap,
    origin_xy: Point,
    angle_rad: float,
    max_range_m: float,
) -> float:
    """Return distance to the first occupied cell or the map boundary.

    The traversal follows Amanatides-Woo style grid marching. Grid indices are
    treated as cell centers, matching GridMap.world_to_grid/grid_to_world.
    """
    max_range = float(max_range_m)
    if not (math.isfinite(max_range) and max_range > 0.0):
        raise ValueError("max_range_m must be finite and positive")

    resolution = float(map_.resolution)
    if not (math.isfinite(resolution) and resolution > 0.0):
        raise ValueError("GridMap resolution must be finite and positive")

    x, y = float(origin_xy[0]), float(origin_xy[1])
    cx, cy = _grid_continuous(map_, x, y)
    gx, gy = _nearest_cell_index(map_, x, y)

    if not map_.in_bounds(gx, gy):
        return 0.0
    if _cell_is_occupied(map_, gx, gy):
        return 0.0

    dx = math.cos(float(angle_rad))
    dy = math.sin(float(angle_rad))
    eps = 1e-12

    if abs(dx) < eps:
        step_x = 0
        t_max_x = math.inf
        t_delta_x = math.inf
    elif dx > 0.0:
        step_x = 1
        t_max_x = ((float(gx) + 0.5) - cx) * resolution / dx
        t_delta_x = resolution / dx
    else:
        step_x = -1
        t_max_x = (cx - (float(gx) - 0.5)) * resolution / (-dx)
        t_delta_x = resolution / (-dx)

    if abs(dy) < eps:
        step_y = 0
        t_max_y = math.inf
        t_delta_y = math.inf
    elif dy > 0.0:
        step_y = 1
        t_max_y = ((float(gy) + 0.5) - cy) * resolution / dy
        t_delta_y = resolution / dy
    else:
        step_y = -1
        t_max_y = (cy - (float(gy) - 0.5)) * resolution / (-dy)
        t_delta_y = resolution / (-dy)

    if not math.isfinite(t_max_x) and not math.isfinite(t_max_y):
        return max_range

    while True:
        if t_max_x < t_max_y:
            distance = t_max_x
            gx += step_x
            t_max_x += t_delta_x
        elif t_max_y < t_max_x:
            distance = t_max_y
            gy += step_y
            t_max_y += t_delta_y
        else:
            distance = t_max_x
            gx += step_x
            gy += step_y
            t_max_x += t_delta_x
            t_max_y += t_delta_y

        distance = max(0.0, float(distance))
        if distance >= max_range:
            return max_range
        if not map_.in_bounds(gx, gy):
            return min(max_range, distance)
        if _cell_is_occupied(map_, gx, gy):
            return min(max_range, distance)


def ray_cast_profile(
    map_: GridMap,
    current_pose: Pose,
    *,
    n_ray: int,
    r_max_m: float,
) -> tuple[np.ndarray, np.ndarray]:
    x, y, theta = (float(v) for v in current_pose)
    rel_angles = ray_angles(int(n_ray))
    world_angles = rel_angles + theta
    distances = np.array(
        [
            ray_cast_distance(
                map_,
                origin_xy=(x, y),
                angle_rad=float(angle),
                max_range_m=float(r_max_m),
            )
            for angle in world_angles
        ],
        dtype=np.float64,
    )
    return distances, rel_angles


def ring_occupancy_ratio(
    map_: GridMap,
    center_xy: Point,
    r_inner_m: float,
    r_outer_m: float,
) -> float:
    inner = float(r_inner_m)
    outer = float(r_outer_m)
    if not (math.isfinite(inner) and math.isfinite(outer) and 0.0 <= inner < outer):
        raise ValueError("ring radii must satisfy 0 <= inner < outer")

    cx, cy = float(center_xy[0]), float(center_xy[1])
    resolution = float(map_.resolution)
    h, w = map_.data.shape

    gx0 = max(0, int(math.ceil(((cx - outer) - float(map_.origin[0])) / resolution - 0.5)))
    gx1 = min(w - 1, int(math.floor(((cx + outer) - float(map_.origin[0])) / resolution + 0.5)))
    gy0 = max(0, int(math.ceil(((cy - outer) - float(map_.origin[1])) / resolution - 0.5)))
    gy1 = min(h - 1, int(math.floor(((cy + outer) - float(map_.origin[1])) / resolution + 0.5)))
    if gx1 < gx0 or gy1 < gy0:
        return 0.0

    xs = np.arange(gx0, gx1 + 1, dtype=np.float64) * resolution + float(map_.origin[0])
    ys = np.arange(gy0, gy1 + 1, dtype=np.float64) * resolution + float(map_.origin[1])
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    radius = np.hypot(xx - cx, yy - cy)
    mask = (radius >= inner) & (radius < outer)
    total = int(np.count_nonzero(mask))
    if total == 0:
        return 0.0

    occupied = np.asarray(map_.data[gy0 : gy1 + 1, gx0 : gx1 + 1], dtype=bool)
    return float(np.count_nonzero(occupied & mask) / float(total))


def density_profile(map_: GridMap, center_xy: Point, rings_m: Sequence[tuple[float, float]]) -> np.ndarray:
    return np.array(
        [
            ring_occupancy_ratio(
                map_,
                center_xy=center_xy,
                r_inner_m=float(inner),
                r_outer_m=float(outer),
            )
            for inner, outer in rings_m
        ],
        dtype=np.float64,
    )


def extract_features(
    map_: GridMap,
    current_pose: Pose,
    goal_pose: Pose,
    *,
    config: FeatureConfig | None = None,
) -> FeatureExtraction:
    cfg = config or FeatureConfig()
    target = relative_goal_features(current_pose, goal_pose)
    ray_distances, rel_angles = ray_cast_profile(
        map_,
        current_pose,
        n_ray=int(cfg.n_ray),
        r_max_m=float(cfg.r_max_m),
    )
    density = density_profile(
        map_,
        center_xy=(float(current_pose[0]), float(current_pose[1])),
        rings_m=cfg.density_rings_m,
    )
    motion_flag = float(cfg.motion_flag_default)

    vector = np.concatenate(
        [
            np.asarray(target, dtype=np.float64),
            np.log1p(ray_distances),
            density,
            np.asarray([motion_flag], dtype=np.float64),
        ]
    )
    return FeatureExtraction(
        vector=vector,
        target_features=target,
        ray_distances_m=ray_distances,
        ray_angles_rad=rel_angles,
        density_ratios=density,
        motion_flag=motion_flag,
    )
