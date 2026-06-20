from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.signal import find_peaks

from forest_n3p.baselines.voronoi_waypoint import (
    VoronoiWaypointConfig,
    _append_poses,
    _clean_pose,
    _cumulative_distances,
    _make_planner,
    _nearest_safe_polyline_index,
    _plan_segment,
    _polyline_heading,
    _xy_distance,
    build_skeleton_graph,
    path_length,
)
from forest_n3p.features import Pose
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class BottleneckWaypointConfig:
    min_bottleneck_separation_m: float = 3.0
    min_bottleneck_prominence_m: float = 0.10
    endpoint_margin_m: float = 1.5
    max_segment_arc_m: float = 10.0
    smoothing_window_m: float = 0.5
    connector_count: int = 24
    max_waypoints: int = 32
    safe_pose_search_window: int = 80
    segment_timeout_s: float = 1.0
    segment_max_nodes: int = 2_000
    skip_window: int = 3
    turning_radius_m: float = 1.0
    wheelbase_m: float = 0.6
    theta_bins: int = 72
    collision_padding: float | None = None
    skeleton_clearance_m: float | None = None

    def __post_init__(self) -> None:
        for name in (
            "min_bottleneck_separation_m",
            "min_bottleneck_prominence_m",
            "endpoint_margin_m",
            "max_segment_arc_m",
            "smoothing_window_m",
            "segment_timeout_s",
            "turning_radius_m",
            "wheelbase_m",
        ):
            value = float(getattr(self, name))
            if not (math.isfinite(value) and value > 0.0):
                raise ValueError(f"{name} must be finite and positive")
        for name in ("connector_count", "max_waypoints", "safe_pose_search_window", "segment_max_nodes", "skip_window"):
            if int(getattr(self, name)) <= 0:
                raise ValueError(f"{name} must be positive")
        if int(self.theta_bins) <= 0:
            raise ValueError("theta_bins must be positive")
        if self.skeleton_clearance_m is not None:
            value = float(self.skeleton_clearance_m)
            if not (math.isfinite(value) and value >= 0.0):
                raise ValueError("skeleton_clearance_m must be finite and non-negative")


@dataclass(frozen=True)
class BottleneckWaypoint:
    waypoint_index: int
    polyline_index: int
    pose: Pose
    clearance_m: float
    prominence_m: float
    kind: str


@dataclass(frozen=True)
class BottleneckSegmentRecord:
    segment_index: int
    start_pose: Pose
    target_pose: Pose
    target_waypoint_index: int
    success: bool
    failure_reason: str | None
    skipped_waypoints: int
    planner_time_s: float
    planner_expansions: int
    path_pose_count: int


@dataclass(frozen=True)
class BottleneckWaypointResult:
    success: bool
    path: tuple[Pose, ...]
    waypoints: tuple[Pose, ...]
    bottlenecks: tuple[BottleneckWaypoint, ...]
    skeleton_node_count: int
    graph_edge_count: int
    segment_records: tuple[BottleneckSegmentRecord, ...]
    failure_reason: str | None
    total_time_s: float
    total_planner_time_s: float
    total_expansions: int


def plan_bottleneck_waypoint(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    *,
    config: BottleneckWaypointConfig | None = None,
) -> BottleneckWaypointResult:
    cfg = config or BottleneckWaypointConfig()
    started = time.perf_counter()
    vcfg = _to_voronoi_config(cfg)
    try:
        graph = build_skeleton_graph(grid_map, start, goal, footprint=footprint, config=vcfg)
        checker = GridFootprintChecker(
            grid_map,
            footprint,
            theta_bins=int(cfg.theta_bins),
            padding=cfg.collision_padding,
        )
        bottlenecks = place_bottleneck_waypoints(grid_map, graph.polyline, checker, config=cfg)
    except Exception as exc:  # noqa: BLE001 - verification reports the failed planning stage.
        return BottleneckWaypointResult(
            success=False,
            path=(),
            waypoints=(),
            bottlenecks=(),
            skeleton_node_count=0,
            graph_edge_count=0,
            segment_records=(),
            failure_reason=f"bottleneck_failed:{type(exc).__name__}:{exc}",
            total_time_s=float(time.perf_counter() - started),
            total_planner_time_s=0.0,
            total_expansions=0,
        )

    planner = _make_planner(grid_map, footprint, vcfg)
    targets = [item.pose for item in bottlenecks] + [_clean_pose(goal)]
    current = _clean_pose(start)
    path_out: list[Pose] = [current]
    records: list[BottleneckSegmentRecord] = []
    total_planner_time_s = 0.0
    total_expansions = 0
    target_index = 0

    while target_index < len(targets):
        best: tuple[int, Any] | None = None
        max_candidate = min(len(targets), target_index + int(cfg.skip_window) + 1)
        for candidate_index in range(target_index, max_candidate):
            attempt = _plan_segment(planner, current, targets[candidate_index], vcfg)
            total_planner_time_s += attempt.planner_time_s
            total_expansions += attempt.expansions
            if attempt.success:
                best = (candidate_index, attempt)
                break
            records.append(
                BottleneckSegmentRecord(
                    segment_index=len(records),
                    start_pose=current,
                    target_pose=targets[candidate_index],
                    target_waypoint_index=int(candidate_index),
                    success=False,
                    failure_reason=attempt.failure_reason,
                    skipped_waypoints=max(0, int(candidate_index) - int(target_index)),
                    planner_time_s=float(attempt.planner_time_s),
                    planner_expansions=int(attempt.expansions),
                    path_pose_count=0,
                )
            )

        if best is None:
            reason = records[-1].failure_reason if records else "no_candidate_segment"
            return BottleneckWaypointResult(
                success=False,
                path=tuple(path_out),
                waypoints=tuple(item.pose for item in bottlenecks),
                bottlenecks=tuple(bottlenecks),
                skeleton_node_count=int(graph.skeleton_node_count),
                graph_edge_count=int(graph.graph_edge_count),
                segment_records=tuple(records),
                failure_reason=f"segment_failed:{reason}",
                total_time_s=float(time.perf_counter() - started),
                total_planner_time_s=float(total_planner_time_s),
                total_expansions=int(total_expansions),
            )

        candidate_index, attempt = best
        _append_poses(path_out, attempt.poses)
        current = path_out[-1]
        records.append(
            BottleneckSegmentRecord(
                segment_index=len(records),
                start_pose=_clean_pose(attempt.start_pose),
                target_pose=targets[candidate_index],
                target_waypoint_index=int(candidate_index),
                success=True,
                failure_reason=None,
                skipped_waypoints=max(0, int(candidate_index) - int(target_index)),
                planner_time_s=float(attempt.planner_time_s),
                planner_expansions=int(attempt.expansions),
                path_pose_count=len(attempt.poses),
            )
        )
        target_index = candidate_index + 1

    return BottleneckWaypointResult(
        success=True,
        path=tuple(path_out),
        waypoints=tuple(item.pose for item in bottlenecks),
        bottlenecks=tuple(bottlenecks),
        skeleton_node_count=int(graph.skeleton_node_count),
        graph_edge_count=int(graph.graph_edge_count),
        segment_records=tuple(records),
        failure_reason=None,
        total_time_s=float(time.perf_counter() - started),
        total_planner_time_s=float(total_planner_time_s),
        total_expansions=int(total_expansions),
    )


def place_bottleneck_waypoints(
    grid_map: GridMap,
    polyline: Iterable[Pose],
    checker: GridFootprintChecker,
    *,
    config: BottleneckWaypointConfig | None = None,
) -> tuple[BottleneckWaypoint, ...]:
    cfg = config or BottleneckWaypointConfig()
    poses = tuple(_clean_pose(pose) for pose in polyline)
    if len(poses) < 2:
        return ()

    cumulative = _cumulative_distances(poses)
    if float(cumulative[-1]) <= 2.0 * float(cfg.endpoint_margin_m):
        return ()

    clearance = _clearance_profile_m(grid_map, poses)
    smooth = _smooth_profile(clearance, _window_samples(cumulative, cfg.smoothing_window_m))
    local_minima = _local_clearance_minima(cumulative, smooth, cfg)
    selected = _add_long_gap_minima(local_minima, cumulative, smooth, cfg)
    return _indices_to_waypoints(poses, selected, clearance, smooth, checker, cfg)


def _local_clearance_minima(
    cumulative: np.ndarray,
    smooth: np.ndarray,
    cfg: BottleneckWaypointConfig,
) -> list[tuple[int, float, str]]:
    valid = _valid_profile_mask(cumulative, cfg)
    if not bool(valid.any()):
        return []
    distance_samples = _window_samples(cumulative, cfg.min_bottleneck_separation_m)
    peaks, props = find_peaks(
        -smooth,
        distance=distance_samples,
        prominence=float(cfg.min_bottleneck_prominence_m),
    )
    candidates: list[tuple[int, float, str]] = []
    prominences = props.get("prominences", np.zeros(len(peaks), dtype=np.float64))
    for idx, prominence in zip(peaks, prominences, strict=True):
        idx_i = int(idx)
        if bool(valid[idx_i]) and math.isfinite(float(smooth[idx_i])):
            candidates.append((idx_i, float(prominence), "local_minimum"))
    candidates.sort(key=lambda item: (float(smooth[item[0]]), -float(item[1]), int(item[0])))
    return candidates[: int(cfg.max_waypoints)]


def _add_long_gap_minima(
    selected: list[tuple[int, float, str]],
    cumulative: np.ndarray,
    smooth: np.ndarray,
    cfg: BottleneckWaypointConfig,
) -> list[tuple[int, float, str]]:
    items = list(selected)
    for _ in range(int(cfg.max_waypoints)):
        ordered = [0] + sorted({idx for idx, _prom, _kind in items}) + [len(cumulative) - 1]
        gap: tuple[float, int, int] | None = None
        for left, right in zip(ordered[:-1], ordered[1:], strict=True):
            length = float(cumulative[right] - cumulative[left])
            if length > float(cfg.max_segment_arc_m) and (gap is None or length > gap[0]):
                gap = (length, int(left), int(right))
        if gap is None or len(items) >= int(cfg.max_waypoints):
            break
        _length, left, right = gap
        idx = _tightest_index_between(left, right, cumulative, smooth, cfg)
        if idx is None or idx in {item[0] for item in items}:
            break
        items.append((idx, 0.0, "long_gap_minimum"))
    items.sort(key=lambda item: int(item[0]))
    return items[: int(cfg.max_waypoints)]


def _tightest_index_between(
    left: int,
    right: int,
    cumulative: np.ndarray,
    smooth: np.ndarray,
    cfg: BottleneckWaypointConfig,
) -> int | None:
    lo = int(left) + 1
    hi = int(right)
    if hi <= lo:
        return None
    margin = min(float(cfg.min_bottleneck_separation_m) * 0.5, float(cumulative[right] - cumulative[left]) * 0.25)
    low_s = float(cumulative[left]) + margin
    high_s = float(cumulative[right]) - margin
    indices = np.arange(lo, hi, dtype=np.int64)
    mask = (cumulative[indices] >= low_s) & (cumulative[indices] <= high_s)
    indices = indices[mask]
    if indices.size == 0:
        return None
    values = smooth[indices]
    min_value = float(np.nanmin(values))
    tied = indices[np.isclose(values, min_value, atol=0.05)]
    mid_s = 0.5 * (float(cumulative[left]) + float(cumulative[right]))
    return int(tied[np.argmin(np.abs(cumulative[tied] - mid_s))])


def _indices_to_waypoints(
    poses: tuple[Pose, ...],
    selected: list[tuple[int, float, str]],
    clearance: np.ndarray,
    smooth: np.ndarray,
    checker: GridFootprintChecker,
    cfg: BottleneckWaypointConfig,
) -> tuple[BottleneckWaypoint, ...]:
    out: list[BottleneckWaypoint] = []
    used: set[int] = set()
    for raw_idx, prominence, kind in selected:
        safe_idx = _nearest_safe_polyline_index(poses, int(raw_idx), checker, config=_to_voronoi_config(cfg))
        if safe_idx is None or safe_idx in used:
            continue
        if out and _xy_distance(out[-1].pose, poses[safe_idx]) < float(cfg.min_bottleneck_separation_m) * 0.5:
            continue
        heading = _polyline_heading(poses, safe_idx)
        pose = (float(poses[safe_idx][0]), float(poses[safe_idx][1]), heading)
        out.append(
            BottleneckWaypoint(
                waypoint_index=len(out),
                polyline_index=int(safe_idx),
                pose=pose,
                clearance_m=float(clearance[safe_idx]),
                prominence_m=float(prominence),
                kind=str(kind),
            )
        )
        used.add(int(safe_idx))
        if len(out) >= int(cfg.max_waypoints):
            break
    return tuple(out)


def _clearance_profile_m(grid_map: GridMap, poses: tuple[Pose, ...]) -> np.ndarray:
    free = np.asarray(grid_map.data) == 0
    padded_free = np.pad(free, 1, mode="constant", constant_values=False)
    edt_m = distance_transform_edt(padded_free)[1:-1, 1:-1] * float(grid_map.resolution)
    out = np.zeros(len(poses), dtype=np.float64)
    for idx, pose in enumerate(poses):
        gx, gy = grid_map.world_to_grid(float(pose[0]), float(pose[1]))
        if grid_map.in_bounds(gx, gy):
            out[idx] = float(edt_m[int(gy), int(gx)])
    return out


def _smooth_profile(values: np.ndarray, window: int) -> np.ndarray:
    clean = np.asarray(values, dtype=np.float64)
    width = max(1, int(window))
    if width <= 1 or clean.size <= 2:
        return clean.copy()
    if width % 2 == 0:
        width += 1
    pad = width // 2
    padded = np.pad(clean, pad, mode="edge")
    kernel = np.ones(width, dtype=np.float64) / float(width)
    return np.convolve(padded, kernel, mode="valid")


def _window_samples(cumulative: np.ndarray, window_m: float) -> int:
    diffs = np.diff(cumulative)
    diffs = diffs[diffs > 1e-9]
    if diffs.size == 0:
        return 1
    median_step = float(np.median(diffs))
    return max(1, int(round(float(window_m) / max(median_step, 1e-9))))


def _valid_profile_mask(cumulative: np.ndarray, cfg: BottleneckWaypointConfig) -> np.ndarray:
    total = float(cumulative[-1])
    return (cumulative >= float(cfg.endpoint_margin_m)) & (cumulative <= total - float(cfg.endpoint_margin_m))


def _to_voronoi_config(cfg: BottleneckWaypointConfig) -> VoronoiWaypointConfig:
    return VoronoiWaypointConfig(
        waypoint_spacing_m=max(float(cfg.max_segment_arc_m), 1e-6),
        connector_count=int(cfg.connector_count),
        max_waypoints=int(cfg.max_waypoints),
        safe_pose_search_window=int(cfg.safe_pose_search_window),
        segment_timeout_s=float(cfg.segment_timeout_s),
        segment_max_nodes=int(cfg.segment_max_nodes),
        skip_window=int(cfg.skip_window),
        turning_radius_m=float(cfg.turning_radius_m),
        wheelbase_m=float(cfg.wheelbase_m),
        theta_bins=int(cfg.theta_bins),
        collision_padding=cfg.collision_padding,
        skeleton_clearance_m=cfg.skeleton_clearance_m,
    )


def result_to_dict(result: BottleneckWaypointResult) -> dict[str, Any]:
    return {
        "success": bool(result.success),
        "path": [list(pose) for pose in result.path],
        "waypoints": [list(pose) for pose in result.waypoints],
        "bottlenecks": [
            {
                "waypoint_index": int(item.waypoint_index),
                "polyline_index": int(item.polyline_index),
                "pose": list(item.pose),
                "clearance_m": float(item.clearance_m),
                "prominence_m": float(item.prominence_m),
                "kind": item.kind,
            }
            for item in result.bottlenecks
        ],
        "skeleton_node_count": int(result.skeleton_node_count),
        "graph_edge_count": int(result.graph_edge_count),
        "segment_records": [
            {
                "segment_index": int(record.segment_index),
                "start_pose": list(record.start_pose),
                "target_pose": list(record.target_pose),
                "target_waypoint_index": int(record.target_waypoint_index),
                "success": bool(record.success),
                "failure_reason": record.failure_reason,
                "skipped_waypoints": int(record.skipped_waypoints),
                "planner_time_s": float(record.planner_time_s),
                "planner_expansions": int(record.planner_expansions),
                "path_pose_count": int(record.path_pose_count),
            }
            for record in result.segment_records
        ],
        "failure_reason": result.failure_reason,
        "total_time_s": float(result.total_time_s),
        "total_planner_time_s": float(result.total_planner_time_s),
        "total_expansions": int(result.total_expansions),
        "path_length_m": path_length(result.path),
    }
