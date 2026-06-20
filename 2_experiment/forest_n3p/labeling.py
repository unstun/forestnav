from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np

from forest_n3p.features import FeatureConfig, Pose, extract_features, wrap_pi
from forest_n3p.rs_utils import generate_reeds_shepp_path, sample_reeds_shepp_path
from forest_n3p.third_party.pathplan.geometry import Footprint, GridFootprintChecker


@dataclass(frozen=True)
class LabelingConfig:
    l_max_m: float = 8.0
    l_min_m: float = 1.5
    path_sample_step_m: float = 0.1
    turning_radius_m: float = 1.0
    wheelbase_m: float = 0.6
    rs_sample_step_m: float = 0.1
    theta_bins: int = 72
    collision_padding: float | None = None
    feature_config: FeatureConfig = field(default_factory=FeatureConfig)

    def __post_init__(self) -> None:
        for name in (
            "l_max_m",
            "l_min_m",
            "path_sample_step_m",
            "turning_radius_m",
            "wheelbase_m",
            "rs_sample_step_m",
        ):
            value = float(getattr(self, name))
            if not (math.isfinite(value) and value > 0.0):
                raise ValueError(f"{name} must be finite and positive")
        if int(self.theta_bins) <= 0:
            raise ValueError("theta_bins must be positive")


@dataclass(frozen=True)
class LabelSample:
    current_pose: Pose
    subgoal_pose: Pose
    delta_body: Pose
    feature_vector: np.ndarray
    s_start_m: float
    s_subgoal_m: float
    rs_length_m: float
    rs_sample_count: int


@dataclass(frozen=True)
class LabelingResult:
    success: bool
    subgoals: tuple[Pose, ...]
    samples: tuple[LabelSample, ...]
    failure_reason: str | None
    path_length_m: float
    candidate_checks: int


@dataclass(frozen=True)
class _RSConnection:
    length_m: float
    collision_free: bool
    sample_count: int


def _as_pose(pose: object) -> Pose:
    if hasattr(pose, "x"):
        out = (float(pose.x), float(pose.y), float(pose.theta))
    else:
        values = tuple(pose)  # type: ignore[arg-type]
        if len(values) != 3:
            raise ValueError("each pose must have three values: x, y, theta")
        out = (float(values[0]), float(values[1]), float(values[2]))
    if not all(math.isfinite(v) for v in out):
        raise ValueError(f"pose values must be finite, got {out!r}")
    return out


def body_relative_pose(current_pose: Pose, target_pose: Pose) -> Pose:
    x, y, theta = (float(v) for v in current_pose)
    tx, ty, ttheta = (float(v) for v in target_pose)
    dx = tx - x
    dy = ty - y
    c = math.cos(theta)
    s = math.sin(theta)
    local_x = c * dx + s * dy
    local_y = -s * dx + c * dy
    return (float(local_x), float(local_y), wrap_pi(ttheta - theta))


def arc_lengths_m(poses: Sequence[Pose]) -> np.ndarray:
    if len(poses) < 2:
        raise ValueError("teacher path must contain at least two poses")
    s_values = [0.0]
    total = 0.0
    for prev, cur in zip(poses[:-1], poses[1:], strict=True):
        total += math.hypot(float(cur[0]) - float(prev[0]), float(cur[1]) - float(prev[1]))
        s_values.append(total)
    if total <= 1e-12:
        raise ValueError("teacher path must have positive xy arc length")
    return np.asarray(s_values, dtype=np.float64)


def _drop_duplicate_positions(poses: Sequence[Pose]) -> tuple[Pose, ...]:
    if not poses:
        raise ValueError("teacher path must not be empty")
    out: list[Pose] = [poses[0]]
    for pose in poses[1:]:
        prev = out[-1]
        if math.hypot(float(pose[0]) - float(prev[0]), float(pose[1]) - float(prev[1])) > 1e-9:
            out.append(pose)
    if len(out) < 2:
        raise ValueError("teacher path must contain at least two distinct positions")
    return tuple(out)


def resample_teacher_path(
    teacher_path: Iterable[object],
    *,
    step_m: float,
) -> tuple[tuple[Pose, ...], np.ndarray]:
    poses = _drop_duplicate_positions(tuple(_as_pose(pose) for pose in teacher_path))
    s_values = arc_lengths_m(poses)
    step = float(step_m)
    if not (math.isfinite(step) and step > 0.0):
        raise ValueError("step_m must be finite and positive")

    total = float(s_values[-1])
    if total <= step:
        return poses, s_values

    targets = list(np.arange(0.0, total, step, dtype=np.float64))
    if not targets or targets[-1] < total - 1e-9:
        targets.append(total)
    else:
        targets[-1] = total
    target_s = np.asarray(targets, dtype=np.float64)

    xs = np.asarray([p[0] for p in poses], dtype=np.float64)
    ys = np.asarray([p[1] for p in poses], dtype=np.float64)
    thetas = np.unwrap(np.asarray([p[2] for p in poses], dtype=np.float64))
    interp_x = np.interp(target_s, s_values, xs)
    interp_y = np.interp(target_s, s_values, ys)
    interp_theta = np.interp(target_s, s_values, thetas)
    resampled = tuple(
        (float(x), float(y), wrap_pi(float(theta)))
        for x, y, theta in zip(interp_x, interp_y, interp_theta, strict=True)
    )
    return resampled, target_s


def _check_rs_connection(
    checker: GridFootprintChecker,
    start: Pose,
    goal: Pose,
    *,
    config: LabelingConfig,
) -> _RSConnection | None:
    try:
        path = generate_reeds_shepp_path(
            start,
            goal,
            turning_radius=float(config.turning_radius_m),
        )
    except RuntimeError:
        return None

    samples = sample_reeds_shepp_path(
        start,
        path,
        turning_radius=float(config.turning_radius_m),
        wheelbase=float(config.wheelbase_m),
        sample_step=float(config.rs_sample_step_m),
    )
    return _RSConnection(
        length_m=float(path.total_length),
        collision_free=not checker.collides_path(samples),
        sample_count=len(samples),
    )


def extract_subgoal_labels(
    grid_map,
    footprint: Footprint,
    teacher_path: Iterable[object],
    *,
    config: LabelingConfig | None = None,
) -> LabelingResult:
    cfg = config or LabelingConfig()
    poses, s_values = resample_teacher_path(teacher_path, step_m=float(cfg.path_sample_step_m))
    goal_pose = poses[-1]
    checker = GridFootprintChecker(
        grid_map,
        footprint,
        theta_bins=int(cfg.theta_bins),
        padding=cfg.collision_padding,
    )

    subgoals: list[Pose] = []
    samples: list[LabelSample] = []
    candidate_checks = 0
    current_idx = 0
    max_iterations = len(poses)

    for _iteration in range(max_iterations):
        current_pose = poses[current_idx]
        direct = _check_rs_connection(checker, current_pose, goal_pose, config=cfg)
        candidate_checks += 1
        if (
            direct is not None
            and direct.collision_free
            and direct.length_m <= float(cfg.l_max_m) + 1e-9
        ):
            return LabelingResult(
                success=True,
                subgoals=tuple(subgoals),
                samples=tuple(samples),
                failure_reason=None,
                path_length_m=float(s_values[-1]),
                candidate_checks=candidate_checks,
            )

        best_idx: int | None = None
        best_connection: _RSConnection | None = None
        for idx in range(len(poses) - 1, current_idx, -1):
            connection = _check_rs_connection(checker, current_pose, poses[idx], config=cfg)
            candidate_checks += 1
            if connection is None:
                continue
            if connection.length_m > float(cfg.l_max_m) + 1e-9:
                continue
            if not connection.collision_free:
                continue
            best_idx = idx
            best_connection = connection
            break

        if best_idx is None or best_connection is None:
            return LabelingResult(
                success=False,
                subgoals=(),
                samples=(),
                failure_reason="no_reachable_candidate",
                path_length_m=float(s_values[-1]),
                candidate_checks=candidate_checks,
            )

        progress = float(s_values[best_idx] - s_values[current_idx])
        if progress < float(cfg.l_min_m) - 1e-9:
            return LabelingResult(
                success=False,
                subgoals=(),
                samples=(),
                failure_reason="short_progress",
                path_length_m=float(s_values[-1]),
                candidate_checks=candidate_checks,
            )

        subgoal_pose = poses[best_idx]
        feature = extract_features(
            grid_map,
            current_pose,
            goal_pose,
            config=cfg.feature_config,
        )
        subgoals.append(subgoal_pose)
        samples.append(
            LabelSample(
                current_pose=current_pose,
                subgoal_pose=subgoal_pose,
                delta_body=body_relative_pose(current_pose, subgoal_pose),
                feature_vector=feature.vector.copy(),
                s_start_m=float(s_values[current_idx]),
                s_subgoal_m=float(s_values[best_idx]),
                rs_length_m=float(best_connection.length_m),
                rs_sample_count=int(best_connection.sample_count),
            )
        )
        current_idx = best_idx

    return LabelingResult(
        success=False,
        subgoals=(),
        samples=(),
        failure_reason="iteration_limit",
        path_length_m=float(s_values[-1]),
        candidate_checks=candidate_checks,
    )
