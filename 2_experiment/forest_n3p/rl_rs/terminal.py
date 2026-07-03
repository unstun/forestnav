from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from forest_n3p.rs_utils import generate_reeds_shepp_path, sample_reeds_shepp_path
from forest_n3p.third_party.pathplan import AckermannState, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class TerminalRsCheckResult:
    success: bool
    time_s: float
    path_length_m: float | None
    sample_count: int
    failure_reason: str | None


def check_terminal_rs_connectable(
    *,
    grid_map: Any,
    footprint: TwoCircleFootprint,
    state: AckermannState,
    goal: AckermannState,
    turning_radius_m: float,
    wheelbase_m: float,
    sample_step_m: float,
    theta_bins: int = 72,
    collision_padding_m: float | None = None,
    checker: Any | None = None,
) -> TerminalRsCheckResult:
    start_ns = time.perf_counter_ns()
    try:
        path = generate_reeds_shepp_path(state, goal, turning_radius=float(turning_radius_m))
        samples = sample_reeds_shepp_path(
            state,
            path,
            turning_radius=float(turning_radius_m),
            wheelbase=float(wheelbase_m),
            sample_step=float(sample_step_m),
        )
        collision_checker = checker or GridFootprintChecker(
            grid_map,
            footprint,
            theta_bins=int(theta_bins),
            padding=collision_padding_m,
        )
        collides = bool(collision_checker.collides_path(samples))
        failure_reason = "terminal_rs_collision" if collides else None
        return TerminalRsCheckResult(
            success=not collides,
            time_s=_elapsed_s(start_ns),
            path_length_m=float(path.total_length),
            sample_count=int(len(samples)),
            failure_reason=failure_reason,
        )
    except Exception as exc:  # noqa: BLE001 - terminal failure must be recorded, not hidden.
        return TerminalRsCheckResult(
            success=False,
            time_s=_elapsed_s(start_ns),
            path_length_m=None,
            sample_count=0,
            failure_reason=f"terminal_rs_error:{type(exc).__name__}",
        )


def _elapsed_s(start_ns: int) -> float:
    return float(time.perf_counter_ns() - start_ns) / 1_000_000_000.0
