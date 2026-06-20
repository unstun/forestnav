from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
from skimage.morphology import medial_axis

from forest_n3p.features import Pose, wrap_pi
from forest_n3p.rs_utils import states_as_tuples
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class VoronoiWaypointConfig:
    waypoint_spacing_m: float = 6.0
    connector_count: int = 24
    max_waypoints: int = 64
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
        for name in ("waypoint_spacing_m", "segment_timeout_s", "turning_radius_m", "wheelbase_m"):
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
class SkeletonGraph:
    skeleton: np.ndarray
    polyline: tuple[Pose, ...]
    skeleton_node_count: int
    graph_edge_count: int
    connector_count: int


@dataclass(frozen=True)
class VoronoiSegmentRecord:
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
class VoronoiWaypointResult:
    success: bool
    path: tuple[Pose, ...]
    waypoints: tuple[Pose, ...]
    skeleton_node_count: int
    graph_edge_count: int
    segment_records: tuple[VoronoiSegmentRecord, ...]
    failure_reason: str | None
    total_time_s: float
    total_planner_time_s: float
    total_expansions: int


def plan_voronoi_waypoint(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    *,
    config: VoronoiWaypointConfig | None = None,
) -> VoronoiWaypointResult:
    cfg = config or VoronoiWaypointConfig()
    started = time.perf_counter()
    try:
        graph = build_skeleton_graph(grid_map, start, goal, footprint=footprint, config=cfg)
        checker = GridFootprintChecker(
            grid_map,
            footprint,
            theta_bins=int(cfg.theta_bins),
            padding=cfg.collision_padding,
        )
        waypoints = place_waypoints(graph.polyline, checker, config=cfg)
    except Exception as exc:  # noqa: BLE001 - verification reports the failed planning stage.
        return VoronoiWaypointResult(
            success=False,
            path=(),
            waypoints=(),
            skeleton_node_count=0,
            graph_edge_count=0,
            segment_records=(),
            failure_reason=f"skeleton_failed:{type(exc).__name__}:{exc}",
            total_time_s=float(time.perf_counter() - started),
            total_planner_time_s=0.0,
            total_expansions=0,
        )

    planner = _make_planner(grid_map, footprint, cfg)
    targets = list(waypoints) + [_clean_pose(goal)]
    current = _clean_pose(start)
    path_out: list[Pose] = [current]
    records: list[VoronoiSegmentRecord] = []
    total_planner_time_s = 0.0
    total_expansions = 0
    target_index = 0

    while target_index < len(targets):
        best: tuple[int, _PlanAttempt] | None = None
        max_candidate = min(len(targets), target_index + int(cfg.skip_window) + 1)
        for candidate_index in range(target_index, max_candidate):
            attempt = _plan_segment(planner, current, targets[candidate_index], cfg)
            total_planner_time_s += attempt.planner_time_s
            total_expansions += attempt.expansions
            if attempt.success:
                best = (candidate_index, attempt)
                break
            records.append(
                VoronoiSegmentRecord(
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
            return VoronoiWaypointResult(
                success=False,
                path=tuple(path_out),
                waypoints=tuple(waypoints),
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
            VoronoiSegmentRecord(
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

    return VoronoiWaypointResult(
        success=True,
        path=tuple(path_out),
        waypoints=tuple(waypoints),
        skeleton_node_count=int(graph.skeleton_node_count),
        graph_edge_count=int(graph.graph_edge_count),
        segment_records=tuple(records),
        failure_reason=None,
        total_time_s=float(time.perf_counter() - started),
        total_planner_time_s=float(total_planner_time_s),
        total_expansions=int(total_expansions),
    )


def build_skeleton_graph(
    grid_map: GridMap,
    start: Pose,
    goal: Pose,
    *,
    footprint: TwoCircleFootprint | None = None,
    config: VoronoiWaypointConfig | None = None,
) -> SkeletonGraph:
    cfg = config or VoronoiWaypointConfig()
    free = _skeleton_free_mask(grid_map, footprint, cfg)
    skeleton = medial_axis(free).astype(bool)
    coords_yx = np.argwhere(skeleton)
    if coords_yx.size == 0:
        raise RuntimeError("medial_axis returned no skeleton pixels")

    node_ids = -np.ones(free.shape, dtype=np.int64)
    for node_id, (gy, gx) in enumerate(coords_yx):
        node_ids[int(gy), int(gx)] = int(node_id)

    rows: list[int] = []
    cols: list[int] = []
    weights: list[float] = []
    _add_skeleton_edges(node_ids, coords_yx, grid_map.resolution, rows, cols, weights)

    skeleton_count = int(len(coords_yx))
    start_node = skeleton_count
    goal_node = skeleton_count + 1
    start_xy = np.asarray([float(start[0]), float(start[1])], dtype=np.float64)
    goal_xy = np.asarray([float(goal[0]), float(goal[1])], dtype=np.float64)
    world_xy = _coords_to_world(grid_map, coords_yx)
    tree = cKDTree(world_xy)
    connector_total = 0
    for special_node, special_xy in ((start_node, start_xy), (goal_node, goal_xy)):
        k = min(int(cfg.connector_count), skeleton_count)
        distances, indices = tree.query(special_xy, k=k)
        indices = np.atleast_1d(indices)
        distances = np.atleast_1d(distances)
        for distance, index in zip(distances, indices, strict=True):
            idx = int(index)
            if idx < 0 or idx >= skeleton_count:
                continue
            w = max(float(distance), float(grid_map.resolution))
            rows.extend([special_node, idx])
            cols.extend([idx, special_node])
            weights.extend([w, w])
            connector_total += 1

    graph = csr_matrix(
        (np.asarray(weights, dtype=np.float64), (np.asarray(rows), np.asarray(cols))),
        shape=(skeleton_count + 2, skeleton_count + 2),
    )
    dist, pred = dijkstra(graph, directed=False, indices=start_node, return_predecessors=True)
    if not math.isfinite(float(dist[goal_node])):
        raise RuntimeError("no skeleton graph path from start to goal")
    node_path = _reconstruct_predecessor_path(pred, start_node, goal_node)
    polyline = _node_path_to_polyline(grid_map, coords_yx, node_path, start, goal, skeleton_count)
    return SkeletonGraph(
        skeleton=skeleton,
        polyline=polyline,
        skeleton_node_count=skeleton_count,
        graph_edge_count=int(len(weights) // 2),
        connector_count=int(connector_total),
    )


def _skeleton_free_mask(
    grid_map: GridMap,
    footprint: TwoCircleFootprint | None,
    cfg: VoronoiWaypointConfig,
) -> np.ndarray:
    free = np.asarray(grid_map.data) == 0
    if footprint is None:
        return free

    clearance_m = _skeleton_clearance_m(grid_map, footprint, cfg)
    if clearance_m <= 0.0:
        return free

    # Treat the known-map boundary as occupied so skeleton pixels do not hug the
    # edge where a finite-size vehicle center would place the footprint outside.
    padded_free = np.pad(free, 1, mode="constant", constant_values=False)
    edt_m = distance_transform_edt(padded_free)[1:-1, 1:-1] * float(grid_map.resolution)
    return free & (edt_m >= clearance_m)


def _skeleton_clearance_m(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: VoronoiWaypointConfig,
) -> float:
    if cfg.skeleton_clearance_m is not None:
        return float(cfg.skeleton_clearance_m)
    padding = 0.0 if cfg.collision_padding is None else float(cfg.collision_padding)
    return float(footprint.radius) + padding + 0.5 * float(grid_map.resolution)


def place_waypoints(
    polyline: Iterable[Pose],
    checker: GridFootprintChecker,
    *,
    config: VoronoiWaypointConfig | None = None,
) -> tuple[Pose, ...]:
    cfg = config or VoronoiWaypointConfig()
    poses = tuple(_clean_pose(pose) for pose in polyline)
    if len(poses) < 2:
        return ()
    cumulative = _cumulative_distances(poses)
    total = float(cumulative[-1])
    spacing = float(cfg.waypoint_spacing_m)
    targets = np.arange(spacing, max(spacing, total), spacing, dtype=np.float64)
    out: list[Pose] = []
    last_idx = 0
    for target_s in targets:
        if target_s >= total - spacing * 0.25:
            break
        idx = int(np.searchsorted(cumulative, target_s, side="left"))
        safe_idx = _nearest_safe_polyline_index(poses, idx, checker, config=cfg)
        if safe_idx is None:
            continue
        if safe_idx <= last_idx:
            continue
        heading = _polyline_heading(poses, safe_idx)
        waypoint = (float(poses[safe_idx][0]), float(poses[safe_idx][1]), heading)
        if out and _xy_distance(out[-1], waypoint) < spacing * 0.5:
            continue
        out.append(waypoint)
        last_idx = safe_idx
        if len(out) >= int(cfg.max_waypoints):
            break
    return tuple(out)


@dataclass(frozen=True)
class _PlanAttempt:
    success: bool
    poses: tuple[Pose, ...]
    failure_reason: str | None
    planner_time_s: float
    expansions: int
    start_pose: Pose


def _make_planner(grid_map: GridMap, footprint: TwoCircleFootprint, cfg: VoronoiWaypointConfig) -> HybridAStarPlanner:
    params = AckermannParams(
        wheelbase=float(cfg.wheelbase_m),
        min_turn_radius=float(cfg.turning_radius_m),
    )
    return HybridAStarPlanner(
        grid_map,
        footprint,
        params,
        analytic_expansion=True,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=math.radians(15.0),
        use_holonomic_heuristic=True,
        theta_bins=int(cfg.theta_bins),
        collision_padding=cfg.collision_padding,
    )


def _plan_segment(
    planner: HybridAStarPlanner,
    start: Pose,
    goal: Pose,
    cfg: VoronoiWaypointConfig,
) -> _PlanAttempt:
    path, stats = planner.plan(
        AckermannState(*start),
        AckermannState(*goal),
        timeout=float(cfg.segment_timeout_s),
        max_nodes=int(cfg.segment_max_nodes),
    )
    if not path:
        return _PlanAttempt(
            success=False,
            poses=(),
            failure_reason=str(stats.get("failure_reason", "unknown")),
            planner_time_s=float(stats.get("time", 0.0)),
            expansions=int(stats.get("expansions", 0)),
            start_pose=start,
        )
    trace = stats.get("trace_poses")
    poses = tuple((float(x), float(y), float(theta)) for x, y, theta in trace) if trace else states_as_tuples(path)
    return _PlanAttempt(
        success=True,
        poses=poses,
        failure_reason=None,
        planner_time_s=float(stats.get("time", 0.0)),
        expansions=int(stats.get("expansions", 0)),
        start_pose=start,
    )


def _add_skeleton_edges(
    node_ids: np.ndarray,
    coords_yx: np.ndarray,
    resolution: float,
    rows: list[int],
    cols: list[int],
    weights: list[float],
) -> None:
    h, w = node_ids.shape
    neighbors = (
        (-1, -1, math.sqrt(2.0)),
        (-1, 0, 1.0),
        (-1, 1, math.sqrt(2.0)),
        (0, -1, 1.0),
        (0, 1, 1.0),
        (1, -1, math.sqrt(2.0)),
        (1, 0, 1.0),
        (1, 1, math.sqrt(2.0)),
    )
    for gy, gx in coords_yx:
        src = int(node_ids[int(gy), int(gx)])
        for dy, dx, scale in neighbors:
            ny = int(gy) + int(dy)
            nx = int(gx) + int(dx)
            if not (0 <= ny < h and 0 <= nx < w):
                continue
            dst = int(node_ids[ny, nx])
            if dst < 0:
                continue
            rows.append(src)
            cols.append(dst)
            weights.append(float(resolution) * float(scale))


def _coords_to_world(grid_map: GridMap, coords_yx: np.ndarray) -> np.ndarray:
    out = np.empty((len(coords_yx), 2), dtype=np.float64)
    for idx, (gy, gx) in enumerate(coords_yx):
        out[idx] = grid_map.grid_to_world(int(gx), int(gy))
    return out


def _reconstruct_predecessor_path(pred: np.ndarray, start_node: int, goal_node: int) -> tuple[int, ...]:
    path = [int(goal_node)]
    cur = int(goal_node)
    for _ in range(len(pred) + 1):
        if cur == int(start_node):
            return tuple(reversed(path))
        cur = int(pred[cur])
        if cur < 0:
            break
        path.append(cur)
    raise RuntimeError("failed to reconstruct skeleton graph predecessor path")


def _node_path_to_polyline(
    grid_map: GridMap,
    coords_yx: np.ndarray,
    node_path: Iterable[int],
    start: Pose,
    goal: Pose,
    skeleton_count: int,
) -> tuple[Pose, ...]:
    out: list[Pose] = []
    start_node = int(skeleton_count)
    goal_node = int(skeleton_count) + 1
    for node in node_path:
        node_i = int(node)
        if node_i == start_node:
            out.append(_clean_pose(start))
        elif node_i == goal_node:
            out.append(_clean_pose(goal))
        else:
            gy, gx = coords_yx[node_i]
            x, y = grid_map.grid_to_world(int(gx), int(gy))
            out.append((float(x), float(y), 0.0))
    return tuple(_dedupe_polyline(out))


def _dedupe_polyline(poses: Iterable[Pose]) -> list[Pose]:
    out: list[Pose] = []
    for pose in poses:
        p = _clean_pose(pose)
        if not out or _xy_distance(out[-1], p) > 1e-9:
            out.append(p)
    return out


def _cumulative_distances(poses: tuple[Pose, ...]) -> np.ndarray:
    values = [0.0]
    total = 0.0
    for prev, cur in zip(poses[:-1], poses[1:], strict=True):
        total += _xy_distance(prev, cur)
        values.append(total)
    return np.asarray(values, dtype=np.float64)


def _nearest_safe_polyline_index(
    poses: tuple[Pose, ...],
    center_idx: int,
    checker: GridFootprintChecker,
    *,
    config: VoronoiWaypointConfig,
) -> int | None:
    n = len(poses)
    center = max(0, min(n - 1, int(center_idx)))
    window = int(config.safe_pose_search_window)
    candidates = sorted(
        range(max(0, center - window), min(n, center + window + 1)),
        key=lambda idx: abs(int(idx) - center),
    )
    for idx in candidates:
        heading = _polyline_heading(poses, idx)
        pose = (float(poses[idx][0]), float(poses[idx][1]), heading)
        if not checker.collides_pose(*pose):
            return int(idx)
    return None


def _polyline_heading(poses: tuple[Pose, ...], idx: int) -> float:
    if len(poses) < 2:
        return 0.0
    i = max(0, min(len(poses) - 1, int(idx)))
    j = min(len(poses) - 1, i + 4)
    k = max(0, i - 4)
    if j != i:
        dx = float(poses[j][0]) - float(poses[i][0])
        dy = float(poses[j][1]) - float(poses[i][1])
    else:
        dx = float(poses[i][0]) - float(poses[k][0])
        dy = float(poses[i][1]) - float(poses[k][1])
    if abs(dx) + abs(dy) <= 1e-12:
        return 0.0
    return float(math.atan2(dy, dx))


def _append_poses(path_out: list[Pose], segment: Iterable[Pose]) -> None:
    poses = tuple(_clean_pose(pose) for pose in segment)
    if not poses:
        return
    if not path_out:
        path_out.extend(poses)
        return
    start_idx = 1 if _same_pose(path_out[-1], poses[0]) else 0
    path_out.extend(poses[start_idx:])


def _clean_pose(pose: Pose) -> Pose:
    out = (float(pose[0]), float(pose[1]), wrap_pi(float(pose[2])))
    if not all(math.isfinite(v) for v in out):
        raise ValueError(f"pose values must be finite, got {pose!r}")
    return out


def _xy_distance(a: Pose, b: Pose) -> float:
    return float(math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1])))


def _same_pose(a: Pose, b: Pose, *, tol: float = 1e-6) -> bool:
    return (
        abs(float(a[0]) - float(b[0])) <= tol
        and abs(float(a[1]) - float(b[1])) <= tol
        and abs(wrap_pi(float(a[2]) - float(b[2]))) <= tol
    )


def path_length(path: Iterable[Pose]) -> float:
    poses = tuple(path)
    return float(
        sum(
            _xy_distance(prev, cur)
            for prev, cur in zip(poses[:-1], poses[1:], strict=True)
        )
    )


def result_to_dict(result: VoronoiWaypointResult) -> dict[str, Any]:
    return {
        "success": bool(result.success),
        "path": [list(pose) for pose in result.path],
        "waypoints": [list(pose) for pose in result.waypoints],
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
