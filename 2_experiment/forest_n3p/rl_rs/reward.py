from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from scipy.ndimage import distance_transform_edt

from forest_n3p.rl_rs.terminal import TerminalRsCheckResult
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint


@dataclass(frozen=True)
class RewardConfig:
    terminal_rs_success: float = 1.0
    collision_penalty: float = -1.0
    terminal_rs_failure_penalty: float = -0.25
    no_progress_penalty: float = -0.25
    distance_progress_scale: float = 0.0
    rs_distance_progress_scale: float = 0.0
    clearance_scale: float = 0.0
    clearance_target_m: float = 0.5
    curvature_rate_penalty_scale: float = 0.0
    path_length_penalty_scale: float = 0.0
    step_penalty: float = 0.0

    def __post_init__(self) -> None:
        _validate_non_negative("terminal_rs_success", self.terminal_rs_success)
        _validate_non_positive("collision_penalty", self.collision_penalty)
        _validate_non_positive("terminal_rs_failure_penalty", self.terminal_rs_failure_penalty)
        _validate_non_positive("no_progress_penalty", self.no_progress_penalty)
        _validate_non_negative("distance_progress_scale", self.distance_progress_scale)
        _validate_non_negative("rs_distance_progress_scale", self.rs_distance_progress_scale)
        _validate_non_negative("clearance_scale", self.clearance_scale)
        _validate_positive("clearance_target_m", self.clearance_target_m)
        _validate_non_negative("curvature_rate_penalty_scale", self.curvature_rate_penalty_scale)
        _validate_non_negative("path_length_penalty_scale", self.path_length_penalty_scale)
        _validate_non_positive("step_penalty", self.step_penalty)


@dataclass(frozen=True)
class RewardBreakdown:
    total: float
    status: str = "e02_2_decomposed_shaping"
    success: float = 0.0
    terminal: float = 0.0
    collision: float = 0.0
    progress: float = 0.0
    rs_progress: float = 0.0
    clearance: float = 0.0
    curvature: float = 0.0
    path_length: float = 0.0
    step: float = 0.0

    def to_record(self) -> dict[str, float | str]:
        return asdict(self)


def compute_terminal_success_reward(
    *,
    terminal_rs: TerminalRsCheckResult,
    collided: bool,
    config: RewardConfig,
) -> RewardBreakdown:
    success = _success_reward(terminal_rs=terminal_rs, collided=collided, config=config)
    return RewardBreakdown(total=success, success=success)


def compute_decomposed_reward(
    *,
    terminal_rs: TerminalRsCheckResult,
    collided: bool,
    failure_reason: str | None,
    progress_to_goal_m: float,
    rs_distance_progress_m: float | None,
    min_clearance_m: float | None,
    curvature_delta_abs: float,
    rollout_path_length_m: float,
    config: RewardConfig,
) -> RewardBreakdown:
    success = _success_reward(terminal_rs=terminal_rs, collided=collided, config=config)
    terminal = _terminal_penalty(failure_reason=failure_reason, config=config)
    collision = float(config.collision_penalty) if collided else 0.0
    progress = float(config.distance_progress_scale) * float(progress_to_goal_m)
    rs_progress = 0.0 if rs_distance_progress_m is None else float(config.rs_distance_progress_scale) * float(rs_distance_progress_m)
    clearance = _clearance_reward(min_clearance_m=min_clearance_m, config=config)
    curvature = -float(config.curvature_rate_penalty_scale) * abs(float(curvature_delta_abs))
    path_length = -float(config.path_length_penalty_scale) * max(0.0, float(rollout_path_length_m))
    step = float(config.step_penalty)
    total = success + terminal + collision + progress + rs_progress + clearance + curvature + path_length + step
    return RewardBreakdown(
        total=float(total),
        success=success,
        terminal=terminal,
        collision=collision,
        progress=progress,
        rs_progress=rs_progress,
        clearance=clearance,
        curvature=curvature,
        path_length=path_length,
        step=step,
    )


def build_clearance_distance_field(grid_map: GridMap) -> np.ndarray:
    edt_m = distance_transform_edt(np.asarray(grid_map.data) == 0).astype(np.float32) * float(grid_map.resolution)
    h, w = edt_m.shape
    xs = (np.arange(w, dtype=np.float32) * float(grid_map.resolution)).reshape(1, -1)
    ys = (np.arange(h, dtype=np.float32) * float(grid_map.resolution)).reshape(-1, 1)
    max_x = float(w - 1) * float(grid_map.resolution)
    max_y = float(h - 1) * float(grid_map.resolution)
    boundary = np.minimum(np.minimum(xs, max_x - xs), np.minimum(ys, max_y - ys))
    return np.minimum(edt_m, boundary).astype(np.float32, copy=False)


def min_rollout_clearance_m(
    samples: tuple[AckermannState, ...],
    *,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    clearance_field_m: np.ndarray,
    padding_m: float = 0.0,
) -> float | None:
    if not samples:
        return None
    radius = float(footprint.radius) + max(0.0, float(padding_m))
    min_clearance = math.inf
    for state in samples:
        for cx, cy in footprint.circle_centers(float(state.x), float(state.y), float(state.theta)):
            dist = _nearest_field_value(clearance_field_m, grid_map, cx, cy)
            min_clearance = min(min_clearance, dist - radius)
    return float(min_clearance) if math.isfinite(min_clearance) else None


def pending_reward_breakdown() -> RewardBreakdown:
    """E02 前的占位: API 可运行, 但不得当作最终 reward 配方。"""

    return RewardBreakdown(total=0.0, status="pending_e02")


def _success_reward(*, terminal_rs: TerminalRsCheckResult, collided: bool, config: RewardConfig) -> float:
    return float(config.terminal_rs_success) if terminal_rs.success and not collided else 0.0


def _terminal_penalty(*, failure_reason: str | None, config: RewardConfig) -> float:
    if failure_reason == "no_progress":
        return float(config.no_progress_penalty)
    if failure_reason is not None and failure_reason.startswith("no_rs_terminal:"):
        return float(config.terminal_rs_failure_penalty)
    return 0.0


def _clearance_reward(*, min_clearance_m: float | None, config: RewardConfig) -> float:
    if min_clearance_m is None or not math.isfinite(float(min_clearance_m)):
        return 0.0
    target = float(config.clearance_target_m)
    normalized = min(max(float(min_clearance_m), 0.0), target) / target
    return float(config.clearance_scale) * normalized


def _nearest_field_value(field_m: np.ndarray, grid_map: GridMap, x: float, y: float) -> float:
    gx, gy = grid_map.world_to_grid(float(x), float(y))
    if not grid_map.in_bounds(gx, gy):
        return 0.0
    return float(np.asarray(field_m)[gy, gx])


def _validate_positive(name: str, value: Any) -> None:
    number = float(value)
    if not (math.isfinite(number) and number > 0.0):
        raise ValueError(f"{name} must be finite and positive")


def _validate_non_negative(name: str, value: Any) -> None:
    number = float(value)
    if not (math.isfinite(number) and number >= 0.0):
        raise ValueError(f"{name} must be finite and non-negative")


def _validate_non_positive(name: str, value: Any) -> None:
    number = float(value)
    if not (math.isfinite(number) and number <= 0.0):
        raise ValueError(f"{name} must be finite and non-positive")
