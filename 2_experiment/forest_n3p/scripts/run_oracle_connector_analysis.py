from __future__ import annotations

import argparse
import json
import math
import socket
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.ndimage import distance_transform_edt

from forest_n3p.baselines.voronoi_waypoint import (
    VoronoiWaypointConfig,
    build_skeleton_graph,
    place_waypoints,
)
from forest_n3p.evaluation import densify_path, direction_switches, min_clearance_m, path_length
from forest_n3p.features import Pose, wrap_pi
from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _generate_grid_map,
    _make_planner,
    _profile_by_name,
    default_main_evaluation_profiles,
    validation_main_evaluation_profiles,
)
from forest_n3p.rs_utils import check_reeds_shepp_collision, states_as_tuples
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker

MapCacheKey = tuple[str, int]


RESULT_SCHEMA = pa.schema(
    [
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("query_seed", pa.int64()),
        ("distance_bin_key", pa.string()),
        ("dedup_key", pa.string()),
        ("expansion_idx", pa.int64()),
        ("state_gx", pa.int64()),
        ("state_gy", pa.int64()),
        ("state_theta_bin", pa.int64()),
        ("duplicate_count", pa.int64()),
        ("state_x", pa.float64()),
        ("state_y", pa.float64()),
        ("state_theta", pa.float64()),
        ("goal_x", pa.float64()),
        ("goal_y", pa.float64()),
        ("goal_theta", pa.float64()),
        ("h_holo", pa.float64()),
        ("h_rs", pa.float64()),
        ("nearest_obstacle_m", pa.float64()),
        ("failed_radius_count", pa.int64()),
        ("oracle_a_success", pa.bool_()),
        ("oracle_a_failure_reason", pa.string()),
        ("oracle_a_time_s", pa.float64()),
        ("oracle_a_expansions", pa.int64()),
        ("oracle_a_path_pose_count", pa.int64()),
        ("oracle_a_path_length_m", pa.float64()),
        ("oracle_a_direction_switches", pa.int64()),
        ("oracle_a_min_clearance_m", pa.float64()),
        ("oracle_a_collision_violation_count", pa.int64()),
        ("candidate_raw_count", pa.int64()),
        ("candidate_rs_reachable_count", pa.int64()),
        ("candidate_source_counts_json", pa.string()),
        ("candidate_generation_errors_json", pa.string()),
        ("oracle_b_success", pa.bool_()),
        ("oracle_b_failure_reason", pa.string()),
        ("oracle_b_attempted_candidate_count", pa.int64()),
        ("oracle_b_selected_candidate_source", pa.string()),
        ("oracle_b_selected_candidate_x", pa.float64()),
        ("oracle_b_selected_candidate_y", pa.float64()),
        ("oracle_b_selected_candidate_theta", pa.float64()),
        ("oracle_b_selected_candidate_score", pa.float64()),
        ("oracle_b_selected_candidate_clearance_m", pa.float64()),
        ("oracle_b_prefilter_rs_length_m", pa.float64()),
        ("oracle_b_terminal_rs_length_m", pa.float64()),
        ("oracle_b_segment_time_s", pa.float64()),
        ("oracle_b_segment_expansions", pa.int64()),
        ("oracle_b_segment_path_pose_count", pa.int64()),
        ("oracle_b_total_path_pose_count", pa.int64()),
        ("oracle_b_segment_path_length_m", pa.float64()),
        ("oracle_b_total_path_length_m", pa.float64()),
        ("oracle_b_direction_switches", pa.int64()),
        ("oracle_b_min_clearance_m", pa.float64()),
        ("oracle_b_collision_violation_count", pa.int64()),
        ("oracle_connectable", pa.bool_()),
        ("best_oracle", pa.string()),
        ("source_head", pa.string()),
    ]
)


@dataclass(frozen=True)
class Candidate:
    source: str
    pose: Pose
    score: float
    clearance_m: float | None
    rs_length_m: float


@dataclass(frozen=True)
class CandidateSet:
    raw_count: int
    candidates: tuple[Candidate, ...]
    source_counts: dict[str, int]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class PlanResult:
    success: bool
    poses: tuple[Pose, ...]
    failure_reason: str | None
    time_s: float
    expansions: int


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description="Run Module2 C02 oracle A/B connector checks on deduplicated RS failure nodes."
    )
    parser.add_argument("--input", type=Path, default=Path("0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet"))
    parser.add_argument("--output", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="validation_t06")
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--buckets", default="Complex,Extreme")
    parser.add_argument("--query-ids", default="")
    parser.add_argument("--row-offset", type=int, default=0)
    parser.add_argument("--max-records", type=int, default=None)
    parser.add_argument("--oracle-a-timeout-s", type=float, default=8.0)
    parser.add_argument("--oracle-a-max-nodes", type=int, default=50_000)
    parser.add_argument("--oracle-b-segment-timeout-s", type=float, default=4.0)
    parser.add_argument("--oracle-b-segment-max-nodes", type=int, default=25_000)
    parser.add_argument("--oracle-b-candidate-limit", type=int, default=32)
    parser.add_argument("--turning-radius-m", type=float, default=1.0)
    parser.add_argument("--wheelbase-m", type=float, default=0.6)
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--rs-sample-step-m", type=float, default=0.05)
    parser.add_argument("--collision-padding-m", type=float, default=None)
    parser.add_argument("--goal-annulus-radii-m", default="1.0,1.5,2.0,2.5,3.0")
    parser.add_argument("--goal-annulus-angle-count", type=int, default=16)
    parser.add_argument("--corridor-fractions", default="0.30,0.45,0.60,0.75")
    parser.add_argument("--corridor-offsets-m", default="-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0")
    parser.add_argument("--edt-margin-m", type=float, default=4.0)
    parser.add_argument("--edt-grid-stride", type=int, default=4)
    parser.add_argument("--edt-candidate-limit", type=int, default=24)
    parser.add_argument("--disable-voronoi", action="store_true")
    parser.add_argument("--voronoi-waypoint-spacing-m", type=float, default=3.0)
    parser.add_argument("--voronoi-max-waypoints", type=int, default=48)
    parser.add_argument("--voronoi-connector-count", type=int, default=24)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    _validate_args(args)
    source_head = str(args.source_head) if args.source_head else _source_head()
    rows = _selected_rows(args)
    cfg = MainEvaluationConfig(
        seed=int(args.seed),
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    map_cache: dict[MapCacheKey, GridMap] = {}
    edt_cache: dict[MapCacheKey, np.ndarray] = {}
    result_rows: list[dict[str, Any]] = []

    for idx, row in enumerate(rows):
        map_key = _map_cache_key(row)
        grid_map = _grid_for_row(row, cfg, footprint, map_cache)
        edt_m = edt_cache.get(map_key)
        if edt_m is None:
            edt_m = _distance_field_m(grid_map)
            edt_cache[map_key] = edt_m

        state = _pose_from_row(row, "state")
        goal = _pose_from_row(row, "goal")
        oracle_a = _run_oracle_a(row, grid_map, footprint, cfg, args, state, goal)
        candidates = _generate_candidate_set(grid_map, footprint, edt_m, args, state, goal)
        oracle_b = _run_oracle_b(row, grid_map, footprint, cfg, args, state, goal, candidates)
        result_rows.append(_result_row(row, oracle_a, candidates, oracle_b, source_head))
        if (idx + 1) % 25 == 0:
            print(f"processed {idx + 1}/{len(rows)} rows", file=sys.stderr, flush=True)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(result_rows, schema=RESULT_SCHEMA)
    pq.write_table(table, output)

    summary = _summary_payload(
        result_rows,
        args=args,
        raw_argv=raw_argv,
        output=output,
        source_head=source_head,
        input_row_count=len(pq.read_table(args.input)),
        selected_row_count=len(rows),
    )
    summary_path = output.with_name(output.stem + "_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _validate_args(args: argparse.Namespace) -> None:
    if args.max_records is not None and int(args.max_records) <= 0:
        raise ValueError("--max-records must be positive when set")
    if int(args.row_offset) < 0:
        raise ValueError("--row-offset must be non-negative")
    for name in (
        "oracle_a_timeout_s",
        "oracle_b_segment_timeout_s",
        "turning_radius_m",
        "wheelbase_m",
        "rs_sample_step_m",
        "edt_margin_m",
        "voronoi_waypoint_spacing_m",
    ):
        value = float(getattr(args, name))
        if not (math.isfinite(value) and value > 0.0):
            raise ValueError(f"--{name.replace('_', '-')} must be finite and positive")
    for name in (
        "oracle_a_max_nodes",
        "oracle_b_segment_max_nodes",
        "oracle_b_candidate_limit",
        "theta_bins",
        "goal_annulus_angle_count",
        "edt_grid_stride",
        "edt_candidate_limit",
        "voronoi_max_waypoints",
        "voronoi_connector_count",
    ):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")


def _selected_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows = pq.read_table(args.input).to_pylist()
    buckets = _parse_str_set(str(args.buckets))
    query_ids = _parse_str_set(str(args.query_ids))
    selected = [
        dict(row)
        for row in rows
        if (not buckets or str(row["difficulty_bucket"]) in buckets)
        and (not query_ids or str(row["query_id"]) in query_ids)
    ]
    start = int(args.row_offset)
    end = None if args.max_records is None else start + int(args.max_records)
    return selected[start:end]


def _run_oracle_a(
    row: dict[str, Any],
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    args: argparse.Namespace,
    state: Pose,
    goal: Pose,
) -> dict[str, Any]:
    plan = _plan_disabled_ha(grid_map, footprint, cfg, state, goal, float(args.oracle_a_timeout_s), int(args.oracle_a_max_nodes))
    metrics = _metrics(grid_map, footprint, plan.poses, collision_padding=args.collision_padding_m) if plan.success else {}
    return {
        "oracle_a_success": bool(plan.success),
        "oracle_a_failure_reason": plan.failure_reason,
        "oracle_a_time_s": float(plan.time_s),
        "oracle_a_expansions": int(plan.expansions),
        "oracle_a_path_pose_count": len(plan.poses),
        "oracle_a_path_length_m": metrics.get("path_length_m"),
        "oracle_a_direction_switches": metrics.get("direction_switches"),
        "oracle_a_min_clearance_m": metrics.get("min_clearance_m"),
        "oracle_a_collision_violation_count": metrics.get("collision_violation_count"),
    }


def _run_oracle_b(
    row: dict[str, Any],
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    args: argparse.Namespace,
    state: Pose,
    goal: Pose,
    candidate_set: CandidateSet,
) -> dict[str, Any]:
    attempted = 0
    failures: list[str] = []
    for candidate in candidate_set.candidates[: int(args.oracle_b_candidate_limit)]:
        attempted += 1
        segment = _plan_disabled_ha(
            grid_map,
            footprint,
            cfg,
            state,
            candidate.pose,
            float(args.oracle_b_segment_timeout_s),
            int(args.oracle_b_segment_max_nodes),
        )
        if not segment.success or not segment.poses:
            failures.append(f"{candidate.source}:segment:{segment.failure_reason}")
            continue

        terminal_start = segment.poses[-1]
        terminal_rs = _safe_rs_check(grid_map, footprint, terminal_start, goal, args)
        if terminal_rs is None:
            failures.append(f"{candidate.source}:terminal_rs:no_path")
            continue
        if not terminal_rs.collision_free:
            failures.append(f"{candidate.source}:terminal_rs:collision")
            continue

        rs_poses = states_as_tuples(terminal_rs.samples)
        combined = _append_without_duplicate(segment.poses, rs_poses[1:])
        metrics = _metrics(grid_map, footprint, combined, collision_padding=args.collision_padding_m)
        if int(metrics["collision_violation_count"]) != 0:
            failures.append(f"{candidate.source}:combined_collision:{metrics['collision_violation_count']}")
            continue

        return {
            "oracle_b_success": True,
            "oracle_b_failure_reason": None,
            "oracle_b_attempted_candidate_count": int(attempted),
            "oracle_b_selected_candidate_source": candidate.source,
            "oracle_b_selected_candidate_x": float(candidate.pose[0]),
            "oracle_b_selected_candidate_y": float(candidate.pose[1]),
            "oracle_b_selected_candidate_theta": float(candidate.pose[2]),
            "oracle_b_selected_candidate_score": float(candidate.score),
            "oracle_b_selected_candidate_clearance_m": candidate.clearance_m,
            "oracle_b_prefilter_rs_length_m": float(candidate.rs_length_m),
            "oracle_b_terminal_rs_length_m": float(terminal_rs.path.total_length),
            "oracle_b_segment_time_s": float(segment.time_s),
            "oracle_b_segment_expansions": int(segment.expansions),
            "oracle_b_segment_path_pose_count": len(segment.poses),
            "oracle_b_total_path_pose_count": len(combined),
            "oracle_b_segment_path_length_m": path_length(segment.poses),
            "oracle_b_total_path_length_m": metrics["path_length_m"],
            "oracle_b_direction_switches": metrics["direction_switches"],
            "oracle_b_min_clearance_m": metrics["min_clearance_m"],
            "oracle_b_collision_violation_count": metrics["collision_violation_count"],
        }

    reason = "no_rs_reachable_candidates" if not candidate_set.candidates else "no_candidate_connected"
    if failures:
        reason = f"{reason};" + ";".join(failures[:8])
    return {
        "oracle_b_success": False,
        "oracle_b_failure_reason": reason,
        "oracle_b_attempted_candidate_count": int(attempted),
        "oracle_b_selected_candidate_source": None,
        "oracle_b_selected_candidate_x": None,
        "oracle_b_selected_candidate_y": None,
        "oracle_b_selected_candidate_theta": None,
        "oracle_b_selected_candidate_score": None,
        "oracle_b_selected_candidate_clearance_m": None,
        "oracle_b_prefilter_rs_length_m": None,
        "oracle_b_terminal_rs_length_m": None,
        "oracle_b_segment_time_s": None,
        "oracle_b_segment_expansions": None,
        "oracle_b_segment_path_pose_count": None,
        "oracle_b_total_path_pose_count": None,
        "oracle_b_segment_path_length_m": None,
        "oracle_b_total_path_length_m": None,
        "oracle_b_direction_switches": None,
        "oracle_b_min_clearance_m": None,
        "oracle_b_collision_violation_count": None,
    }


def _generate_candidate_set(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    edt_m: np.ndarray,
    args: argparse.Namespace,
    state: Pose,
    goal: Pose,
) -> CandidateSet:
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=int(args.theta_bins), padding=args.collision_padding_m)
    candidates: dict[tuple[int, int, int], Candidate] = {}
    raw_count = 0
    errors: list[str] = []

    def add_pose(source: str, pose: Pose) -> None:
        nonlocal raw_count
        raw_count += 1
        _try_add_candidate(candidates, grid_map, footprint, checker, state, goal, pose, source, args)

    for pose in _goal_annulus_poses(args, goal):
        add_pose("goal_annulus", pose)
    for pose in _corridor_poses(args, state, goal):
        add_pose("corridor_offset", pose)
    for pose in _edt_high_clearance_poses(grid_map, edt_m, args, state, goal):
        add_pose("edt_high_clearance", pose)

    if not bool(args.disable_voronoi):
        try:
            vcfg = VoronoiWaypointConfig(
                waypoint_spacing_m=float(args.voronoi_waypoint_spacing_m),
                connector_count=int(args.voronoi_connector_count),
                max_waypoints=int(args.voronoi_max_waypoints),
                segment_timeout_s=float(args.oracle_b_segment_timeout_s),
                segment_max_nodes=int(args.oracle_b_segment_max_nodes),
                turning_radius_m=float(args.turning_radius_m),
                wheelbase_m=float(args.wheelbase_m),
                theta_bins=int(args.theta_bins),
                collision_padding=args.collision_padding_m,
            )
            graph = build_skeleton_graph(grid_map, state, goal, footprint=footprint, config=vcfg)
            waypoints = place_waypoints(graph.polyline, checker, config=vcfg)
            for waypoint in waypoints:
                add_pose("voronoi_skeleton", waypoint)
        except Exception as exc:  # noqa: BLE001 - oracle output records candidate-generation failures.
            errors.append(f"voronoi_skeleton:{type(exc).__name__}:{exc}")

    source_counts = Counter(candidate.source for candidate in candidates.values())
    ordered = tuple(sorted(candidates.values(), key=lambda item: (item.score, item.source, item.pose[0], item.pose[1])))
    return CandidateSet(
        raw_count=int(raw_count),
        candidates=ordered,
        source_counts={str(k): int(v) for k, v in source_counts.items()},
        errors=tuple(errors),
    )


def _try_add_candidate(
    out: dict[tuple[int, int, int], Candidate],
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    checker: GridFootprintChecker,
    state: Pose,
    goal: Pose,
    pose: Pose,
    source: str,
    args: argparse.Namespace,
) -> None:
    pose = _clean_pose(pose)
    if _xy_distance(state, pose) < 0.5:
        return
    if not _in_bounds_world(grid_map, pose[0], pose[1]):
        return
    if checker.collides_pose(*pose):
        return
    rs = _safe_rs_check(grid_map, footprint, pose, goal, args)
    if rs is None or not rs.collision_free:
        return
    clearance = min_clearance_m(grid_map, footprint, (pose,), collision_padding=args.collision_padding_m)
    clearance_bonus = 0.0 if clearance is None else min(float(clearance), 2.0) * 0.2
    score = _xy_distance(state, pose) + float(rs.path.total_length) - clearance_bonus
    key = _candidate_key(grid_map, pose, int(args.theta_bins))
    candidate = Candidate(
        source=str(source),
        pose=pose,
        score=float(score),
        clearance_m=clearance,
        rs_length_m=float(rs.path.total_length),
    )
    previous = out.get(key)
    if previous is None or candidate.score < previous.score:
        out[key] = candidate


def _goal_annulus_poses(args: argparse.Namespace, goal: Pose) -> Iterable[Pose]:
    radii = _parse_float_list(str(args.goal_annulus_radii_m))
    angle_count = int(args.goal_annulus_angle_count)
    for radius in radii:
        for idx in range(angle_count):
            angle = (2.0 * math.pi * float(idx)) / float(angle_count)
            x = float(goal[0]) + float(radius) * math.cos(angle)
            y = float(goal[1]) + float(radius) * math.sin(angle)
            heading_to_goal = math.atan2(float(goal[1]) - y, float(goal[0]) - x)
            for theta in _unique_angles((heading_to_goal, float(goal[2]), heading_to_goal + math.pi)):
                yield (x, y, theta)


def _corridor_poses(args: argparse.Namespace, state: Pose, goal: Pose) -> Iterable[Pose]:
    fractions = _parse_float_list(str(args.corridor_fractions))
    offsets = _parse_float_list(str(args.corridor_offsets_m))
    dx = float(goal[0]) - float(state[0])
    dy = float(goal[1]) - float(state[1])
    dist = math.hypot(dx, dy)
    if dist <= 1e-9:
        return
    ux = dx / dist
    uy = dy / dist
    nx = -uy
    ny = ux
    line_heading = math.atan2(dy, dx)
    for fraction in fractions:
        if not (0.0 < float(fraction) < 1.0):
            continue
        base_x = float(state[0]) + float(fraction) * dx
        base_y = float(state[1]) + float(fraction) * dy
        for offset in offsets:
            x = base_x + float(offset) * nx
            y = base_y + float(offset) * ny
            heading_to_goal = math.atan2(float(goal[1]) - y, float(goal[0]) - x)
            for theta in _unique_angles((line_heading, heading_to_goal, float(goal[2]))):
                yield (x, y, theta)


def _edt_high_clearance_poses(
    grid_map: GridMap,
    edt_m: np.ndarray,
    args: argparse.Namespace,
    state: Pose,
    goal: Pose,
) -> Iterable[Pose]:
    margin = float(args.edt_margin_m)
    stride = int(args.edt_grid_stride)
    h, w = grid_map.data.shape
    x0, y0 = grid_map.world_to_grid(min(float(state[0]), float(goal[0])) - margin, min(float(state[1]), float(goal[1])) - margin)
    x1, y1 = grid_map.world_to_grid(max(float(state[0]), float(goal[0])) + margin, max(float(state[1]), float(goal[1])) + margin)
    gx0 = max(0, min(x0, x1))
    gx1 = min(w - 1, max(x0, x1))
    gy0 = max(0, min(y0, y1))
    gy1 = min(h - 1, max(y0, y1))
    if gx1 <= gx0 or gy1 <= gy0:
        return

    dx = float(goal[0]) - float(state[0])
    dy = float(goal[1]) - float(state[1])
    dist2 = dx * dx + dy * dy
    if dist2 <= 1e-9:
        return
    line_heading = math.atan2(dy, dx)
    scored: list[tuple[float, float, float]] = []
    for gy in range(gy0, gy1 + 1, stride):
        for gx in range(gx0, gx1 + 1, stride):
            if grid_map.is_occupied_index(gx, gy):
                continue
            x, y = grid_map.grid_to_world(gx, gy)
            progress = ((float(x) - float(state[0])) * dx + (float(y) - float(state[1])) * dy) / dist2
            if not (0.15 <= progress <= 0.95):
                continue
            clearance = float(edt_m[gy, gx])
            lateral = abs((float(x) - float(state[0])) * (-dy) + (float(y) - float(state[1])) * dx) / math.sqrt(dist2)
            score = -clearance + 0.05 * lateral + 0.2 * abs(progress - 0.65)
            scored.append((score, float(x), float(y)))

    scored.sort(key=lambda item: item[0])
    for _score, x, y in scored[: int(args.edt_candidate_limit)]:
        heading_to_goal = math.atan2(float(goal[1]) - y, float(goal[0]) - x)
        for theta in _unique_angles((heading_to_goal, line_heading, float(goal[2]))):
            yield (x, y, theta)


def _plan_disabled_ha(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    start: Pose,
    goal: Pose,
    timeout_s: float,
    max_nodes: int,
) -> PlanResult:
    planner = _make_planner(grid_map, footprint, cfg, analytic_operator="disabled")
    states, stats = planner.plan(
        AckermannState(*start),
        AckermannState(*goal),
        timeout=float(timeout_s),
        max_nodes=int(max_nodes),
    )
    if not states or stats.get("failure_reason") is not None:
        return PlanResult(
            success=False,
            poses=(),
            failure_reason=str(stats.get("failure_reason", "unknown")),
            time_s=float(stats.get("time", 0.0)),
            expansions=int(stats.get("expansions", 0)),
        )
    trace = stats.get("trace_poses")
    poses = tuple(_clean_pose(tuple(pose)) for pose in trace) if trace else states_as_tuples(states)
    return PlanResult(
        success=True,
        poses=tuple(_clean_pose(pose) for pose in poses),
        failure_reason=None,
        time_s=float(stats.get("time", 0.0)),
        expansions=int(stats.get("expansions", 0)),
    )


def _metrics(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    path: Iterable[Pose],
    *,
    collision_padding: float | None,
) -> dict[str, Any]:
    poses = tuple(_clean_pose(pose) for pose in path)
    samples = densify_path(poses, step_m=0.1)
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=72, padding=collision_padding)
    collision_count = sum(1 for pose in samples if checker.collides_pose(*pose))
    return {
        "path_length_m": path_length(poses) if poses else None,
        "direction_switches": direction_switches(poses) if poses else None,
        "min_clearance_m": min_clearance_m(grid_map, footprint, samples, collision_padding=collision_padding),
        "collision_violation_count": int(collision_count),
    }


def _result_row(
    row: dict[str, Any],
    oracle_a: dict[str, Any],
    candidate_set: CandidateSet,
    oracle_b: dict[str, Any],
    source_head: str,
) -> dict[str, Any]:
    connectable = bool(oracle_a["oracle_a_success"] or oracle_b["oracle_b_success"])
    best = "oracle_a" if oracle_a["oracle_a_success"] else ("oracle_b" if oracle_b["oracle_b_success"] else None)
    return {
        "query_id": str(row["query_id"]),
        "difficulty_bucket": str(row["difficulty_bucket"]),
        "profile_name": str(row["profile_name"]),
        "map_seed": int(row["map_seed"]),
        "query_seed": int(row["query_seed"]),
        "distance_bin_key": str(row["distance_bin_key"]),
        "dedup_key": row.get("dedup_key"),
        "expansion_idx": int(row["expansion_idx"]),
        "state_gx": _optional_int(row.get("state_gx")),
        "state_gy": _optional_int(row.get("state_gy")),
        "state_theta_bin": _optional_int(row.get("state_theta_bin")),
        "duplicate_count": _optional_int(row.get("duplicate_count")),
        "state_x": float(row["state_x"]),
        "state_y": float(row["state_y"]),
        "state_theta": float(row["state_theta"]),
        "goal_x": float(row["goal_x"]),
        "goal_y": float(row["goal_y"]),
        "goal_theta": float(row["goal_theta"]),
        "h_holo": _optional_float(row.get("h_holo")),
        "h_rs": _optional_float(row.get("h_rs")),
        "nearest_obstacle_m": _optional_float(row.get("nearest_obstacle_m")),
        "failed_radius_count": _optional_int(row.get("failed_radius_count")),
        **oracle_a,
        "candidate_raw_count": int(candidate_set.raw_count),
        "candidate_rs_reachable_count": len(candidate_set.candidates),
        "candidate_source_counts_json": json.dumps(candidate_set.source_counts, sort_keys=True),
        "candidate_generation_errors_json": json.dumps(list(candidate_set.errors), ensure_ascii=False),
        **oracle_b,
        "oracle_connectable": connectable,
        "best_oracle": best,
        "source_head": str(source_head),
    }


def _summary_payload(
    rows: Sequence[dict[str, Any]],
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    output: Path,
    source_head: str,
    input_row_count: int,
    selected_row_count: int,
) -> dict[str, Any]:
    by_bucket: dict[str, dict[str, Any]] = defaultdict(lambda: {"record_count": 0, "oracle_a_success": 0, "oracle_b_success": 0, "oracle_connectable": 0})
    failure_reasons = Counter()
    for row in rows:
        bucket = str(row["difficulty_bucket"])
        item = by_bucket[bucket]
        item["record_count"] += 1
        item["oracle_a_success"] += int(bool(row["oracle_a_success"]))
        item["oracle_b_success"] += int(bool(row["oracle_b_success"]))
        item["oracle_connectable"] += int(bool(row["oracle_connectable"]))
        if not row["oracle_connectable"]:
            reason = row.get("oracle_b_failure_reason") or row.get("oracle_a_failure_reason") or "unknown"
            failure_reasons[str(reason).split(";")[0]] += 1

    total = len(rows)
    return {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": str(source_head),
        "command": " ".join(["python -m forest_n3p.scripts.run_oracle_connector_analysis", *raw_argv]),
        "input": str(args.input),
        "output": str(output),
        "input_row_count": int(input_row_count),
        "selected_row_count": int(selected_row_count),
        "result_row_count": int(total),
        "oracle_a_success_count": sum(int(row["oracle_a_success"]) for row in rows),
        "oracle_b_success_count": sum(int(row["oracle_b_success"]) for row in rows),
        "oracle_connectable_count": sum(int(row["oracle_connectable"]) for row in rows),
        "oracle_connectable_rate": _safe_ratio(sum(int(row["oracle_connectable"]) for row in rows), total),
        "by_bucket": dict(by_bucket),
        "top_failure_reasons": dict(failure_reasons.most_common(20)),
        "config": {
            "density_profile_buckets": str(args.density_profile_buckets),
            "buckets": str(args.buckets),
            "query_ids": str(args.query_ids),
            "row_offset": int(args.row_offset),
            "max_records": args.max_records,
            "oracle_a_timeout_s": float(args.oracle_a_timeout_s),
            "oracle_a_max_nodes": int(args.oracle_a_max_nodes),
            "oracle_b_segment_timeout_s": float(args.oracle_b_segment_timeout_s),
            "oracle_b_segment_max_nodes": int(args.oracle_b_segment_max_nodes),
            "oracle_b_candidate_limit": int(args.oracle_b_candidate_limit),
            "disable_voronoi": bool(args.disable_voronoi),
        },
    }


def _grid_for_row(
    row: dict[str, Any],
    cfg: MainEvaluationConfig,
    footprint: TwoCircleFootprint,
    cache: dict[MapCacheKey, GridMap],
) -> GridMap:
    cache_key = _map_cache_key(row)
    map_seed = int(row["map_seed"])
    grid_map = cache.get(cache_key)
    if grid_map is not None:
        return grid_map
    profile = _profile_by_name(cfg.profiles, str(row["profile_name"]))
    grid_map = _generate_grid_map(profile, map_seed, cfg, footprint)
    cache[cache_key] = grid_map
    return grid_map


def _map_cache_key(row: dict[str, Any]) -> MapCacheKey:
    return (str(row["profile_name"]), int(row["map_seed"]))


def _safe_rs_check(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    args: argparse.Namespace,
):
    try:
        return check_reeds_shepp_collision(
            grid_map,
            footprint,
            start,
            goal,
            turning_radius=float(args.turning_radius_m),
            wheelbase=float(args.wheelbase_m),
            sample_step=float(args.rs_sample_step_m),
            theta_bins=int(args.theta_bins),
            collision_padding=args.collision_padding_m,
        )
    except Exception:  # noqa: BLE001 - no RS candidate is a data outcome here.
        return None


def _distance_field_m(grid_map: GridMap) -> np.ndarray:
    free = np.asarray(grid_map.data) == 0
    padded = np.pad(free, 1, mode="constant", constant_values=False)
    return distance_transform_edt(padded)[1:-1, 1:-1] * float(grid_map.resolution)


def _append_without_duplicate(left: Iterable[Pose], right: Iterable[Pose]) -> tuple[Pose, ...]:
    out = [_clean_pose(pose) for pose in left]
    for pose in right:
        clean = _clean_pose(pose)
        if out and _same_pose(out[-1], clean):
            continue
        out.append(clean)
    return tuple(out)


def _profiles_from_bucket_mode(mode: str):
    if mode == "original_t06":
        return default_main_evaluation_profiles()
    if mode == "validation_t06":
        return validation_main_evaluation_profiles()
    raise ValueError(f"unsupported density profile bucket mode: {mode}")


def _parse_float_list(value: str) -> tuple[float, ...]:
    return tuple(float(part.strip()) for part in value.split(",") if part.strip())


def _parse_str_set(value: str) -> set[str]:
    return {part.strip() for part in value.split(",") if part.strip()}


def _pose_from_row(row: dict[str, Any], prefix: str) -> Pose:
    return _clean_pose((float(row[f"{prefix}_x"]), float(row[f"{prefix}_y"]), float(row[f"{prefix}_theta"])))


def _clean_pose(pose: Pose) -> Pose:
    out = (float(pose[0]), float(pose[1]), wrap_pi(float(pose[2])))
    if not all(math.isfinite(value) for value in out):
        raise ValueError(f"pose values must be finite, got {pose!r}")
    return out


def _unique_angles(angles: Iterable[float]) -> tuple[float, ...]:
    out: list[float] = []
    for angle in angles:
        wrapped = wrap_pi(float(angle))
        if all(abs(wrap_pi(wrapped - existing)) > math.radians(2.5) for existing in out):
            out.append(wrapped)
    return tuple(out)


def _candidate_key(grid_map: GridMap, pose: Pose, theta_bins: int) -> tuple[int, int, int]:
    gx, gy = grid_map.world_to_grid(float(pose[0]), float(pose[1]))
    theta_bin = int(math.floor(((float(pose[2]) % (2.0 * math.pi)) / (2.0 * math.pi)) * int(theta_bins))) % int(theta_bins)
    return int(gx), int(gy), int(theta_bin)


def _in_bounds_world(grid_map: GridMap, x: float, y: float) -> bool:
    gx, gy = grid_map.world_to_grid(float(x), float(y))
    return grid_map.in_bounds(gx, gy)


def _xy_distance(a: Pose, b: Pose) -> float:
    return float(math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1])))


def _same_pose(a: Pose, b: Pose, *, tol: float = 1e-6) -> bool:
    return (
        abs(float(a[0]) - float(b[0])) <= tol
        and abs(float(a[1]) - float(b[1])) <= tol
        and abs(wrap_pi(float(a[2]) - float(b[2]))) <= tol
    )


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)


def _optional_int(value: Any) -> int | None:
    return None if value is None else int(value)


def _safe_ratio(numerator: int, denominator: int) -> float | None:
    return None if int(denominator) <= 0 else float(numerator) / float(denominator)


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop oracle analysis.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
