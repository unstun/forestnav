from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.ndimage import distance_transform_edt

from forest_n3p.features import wrap_pi
from forest_n3p.third_party.pathplan import AckermannState, GridMap


@dataclass(frozen=True)
class ObservationConfig:
    patch_size_m: float = 6.4
    patch_cells: int = 64
    include_edt: bool = True
    edt_clip_m: float = 3.0

    def __post_init__(self) -> None:
        if not (math.isfinite(float(self.patch_size_m)) and float(self.patch_size_m) > 0.0):
            raise ValueError("patch_size_m must be finite and positive")
        if int(self.patch_cells) <= 0:
            raise ValueError("patch_cells must be positive")
        if not (math.isfinite(float(self.edt_clip_m)) and float(self.edt_clip_m) > 0.0):
            raise ValueError("edt_clip_m must be finite and positive")


@dataclass(frozen=True)
class RlRsObservation:
    state: AckermannState
    goal: AckermannState
    scalar: tuple[float, ...]
    patch: np.ndarray | None = None


def build_scalar_observation(state: AckermannState, goal: AckermannState, *, remaining_steps: int) -> tuple[float, ...]:
    dx = float(goal.x - state.x)
    dy = float(goal.y - state.y)
    distance = math.hypot(dx, dy)
    bearing = math.atan2(dy, dx)
    heading_error = wrap_pi(float(goal.theta - state.theta))
    bearing_error = wrap_pi(bearing - float(state.theta))
    return (
        dx,
        dy,
        distance,
        math.sin(heading_error),
        math.cos(heading_error),
        math.sin(bearing_error),
        math.cos(bearing_error),
        float(remaining_steps),
    )


def build_egocentric_occupancy_patch(
    grid_map: GridMap,
    state: AckermannState,
    config: ObservationConfig,
) -> np.ndarray:
    gx, gy, in_bounds = _egocentric_grid_indices(grid_map, state, config)
    patch = np.ones((int(config.patch_cells), int(config.patch_cells)), dtype=np.float32)
    if np.any(in_bounds):
        patch[in_bounds] = grid_map.data[gy[in_bounds], gx[in_bounds]].astype(np.float32)
    return patch


def build_egocentric_edt_patch(
    grid_map: GridMap,
    state: AckermannState,
    config: ObservationConfig,
    *,
    edt_m: np.ndarray | None = None,
) -> np.ndarray:
    if edt_m is None:
        edt_m = distance_transform_edt(grid_map.data == 0).astype(np.float32) * float(grid_map.resolution)
    gx, gy, in_bounds = _egocentric_grid_indices(grid_map, state, config)
    patch = np.zeros((int(config.patch_cells), int(config.patch_cells)), dtype=np.float32)
    if np.any(in_bounds):
        values = np.asarray(edt_m, dtype=np.float32)[gy[in_bounds], gx[in_bounds]]
        patch[in_bounds] = np.clip(values, 0.0, float(config.edt_clip_m)) / float(config.edt_clip_m)
    return patch


def build_patch_observation(
    grid_map: GridMap,
    state: AckermannState,
    config: ObservationConfig | None = None,
    *,
    edt_m: np.ndarray | None = None,
) -> np.ndarray:
    cfg = config or ObservationConfig()
    occupancy = build_egocentric_occupancy_patch(grid_map, state, cfg)
    if not bool(cfg.include_edt):
        return occupancy.reshape(1, int(cfg.patch_cells), int(cfg.patch_cells)).astype(np.float32, copy=False)
    edt = build_egocentric_edt_patch(grid_map, state, cfg, edt_m=edt_m)
    return np.stack((occupancy, edt), axis=0).astype(np.float32, copy=False)


def build_observation(
    state: AckermannState,
    goal: AckermannState,
    *,
    remaining_steps: int,
    grid_map: GridMap | None = None,
    config: ObservationConfig | None = None,
) -> RlRsObservation:
    return RlRsObservation(
        state=state,
        goal=goal,
        scalar=build_scalar_observation(state, goal, remaining_steps=int(remaining_steps)),
        patch=build_patch_observation(grid_map, state, config) if grid_map is not None else None,
    )


def _egocentric_grid_indices(
    grid_map: GridMap,
    state: AckermannState,
    config: ObservationConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    half = float(config.patch_size_m) / 2.0
    cells = int(config.patch_cells)
    lin = np.linspace(-half, half, cells, dtype=np.float32)
    xs, ys = np.meshgrid(lin, lin, indexing="xy")
    cos_t = math.cos(float(state.theta))
    sin_t = math.sin(float(state.theta))
    world_x = float(state.x) + cos_t * xs - sin_t * ys
    world_y = float(state.y) + sin_t * xs + cos_t * ys
    gx = np.rint((world_x - float(grid_map.origin[0])) / float(grid_map.resolution)).astype(np.int64)
    gy = np.rint((world_y - float(grid_map.origin[1])) / float(grid_map.resolution)).astype(np.int64)
    h, w = grid_map.data.shape
    in_bounds = (gx >= 0) & (gx < w) & (gy >= 0) & (gy < h)
    return np.clip(gx, 0, w - 1), np.clip(gy, 0, h - 1), in_bounds
