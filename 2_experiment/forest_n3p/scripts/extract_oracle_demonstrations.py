from __future__ import annotations

import argparse
import json
import math
import socket
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pyarrow as pa
import pyarrow.parquet as pq

from forest_n3p.features import wrap_pi
from forest_n3p.rl_rs.obs import ObservationConfig, build_scalar_observation
from forest_n3p.rl_rs.terminal import check_terminal_rs_connectable
from forest_n3p.scripts.run_oracle_connector_analysis import (
    _append_without_duplicate,
    _grid_for_row,
    _plan_disabled_ha,
    _profiles_from_bucket_mode,
    _safe_rs_check,
)
from forest_n3p.main_evaluation import MainEvaluationConfig
from forest_n3p.rs_utils import states_as_tuples
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


Pose = tuple[float, float, float]


DEMO_SCHEMA = pa.schema(
    [
        ("sample_id", pa.int64()),
        ("source_row_index", pa.int64()),
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("query_seed", pa.int64()),
        ("distance_bin_key", pa.string()),
        ("dedup_key", pa.string()),
        ("expansion_idx", pa.int64()),
        ("oracle_type", pa.string()),
        ("path_step_index", pa.int64()),
        ("remaining_oracle_steps", pa.int64()),
        ("current_x", pa.float64()),
        ("current_y", pa.float64()),
        ("current_theta", pa.float64()),
        ("next_x", pa.float64()),
        ("next_y", pa.float64()),
        ("next_theta", pa.float64()),
        ("goal_x", pa.float64()),
        ("goal_y", pa.float64()),
        ("goal_theta", pa.float64()),
        ("expert_steering_rad", pa.float64()),
        ("expert_curvature", pa.float64()),
        ("expert_direction", pa.int64()),
        ("step_length_m", pa.float64()),
        ("obs_scalar", pa.list_(pa.float32())),
        ("terminal_rs_checked", pa.bool_()),
        ("terminal_rs_success", pa.bool_()),
        ("terminal_rs_path_length_m", pa.float64()),
        ("source_head", pa.string()),
    ]
)


@dataclass(frozen=True)
class ExtractionStats:
    selected_rows: int = 0
    replay_success_rows: int = 0
    demo_rows: int = 0
    skipped_not_connectable: int = 0
    skipped_oracle_replay_failed: int = 0
    skipped_terminal_rs_ready: int = 0
    skipped_collision: int = 0
    skipped_reverse: int = 0
    skipped_short: int = 0

    def add(self, **updates: int) -> "ExtractionStats":
        values = self.__dict__.copy()
        for key, value in updates.items():
            values[key] = int(values[key]) + int(value)
        return ExtractionStats(**values)


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description="Replay C02 oracle connectors and extract source-bound RL-RS behavior-cloning demonstrations."
    )
    parser.add_argument("--input", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--output", type=Path, default=Path("2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations.parquet"))
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="validation_t06")
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--buckets", default="Complex,Extreme")
    parser.add_argument("--oracle-types", choices=("best", "oracle_a", "oracle_b"), default="best")
    parser.add_argument("--filter-best-oracle", choices=("any", "oracle_a", "oracle_b"), default="any")
    parser.add_argument("--oracle-b-candidate-sources", default=None)
    parser.add_argument("--exclude-oracle-b-candidate-sources", default=None)
    parser.add_argument("--max-records", type=int, default=None)
    parser.add_argument("--row-offset", type=int, default=0)
    parser.add_argument("--oracle-a-timeout-s", type=float, default=8.0)
    parser.add_argument("--oracle-a-max-nodes", type=int, default=50_000)
    parser.add_argument("--oracle-b-segment-timeout-s", type=float, default=4.0)
    parser.add_argument("--oracle-b-segment-max-nodes", type=int, default=25_000)
    parser.add_argument("--turning-radius-m", type=float, default=1.0)
    parser.add_argument("--wheelbase-m", type=float, default=0.6)
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--rs-sample-step-m", type=float, default=0.05)
    parser.add_argument("--collision-padding-m", type=float, default=None)
    parser.add_argument("--min-step-length-m", type=float, default=1e-4)
    parser.add_argument("--stop-at-terminal-rs", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--obs-patch-size-m", type=float, default=6.4)
    parser.add_argument("--obs-patch-cells", type=int, default=64)
    parser.add_argument("--obs-edt-clip-m", type=float, default=3.0)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    _validate_args(args)
    source_head = str(args.source_head) if args.source_head else _source_head()
    rows_with_index = _selected_rows(args)
    cfg = MainEvaluationConfig(
        seed=int(args.seed),
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    params = AckermannParams(wheelbase=float(args.wheelbase_m), min_turn_radius=float(args.turning_radius_m))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    obs_config = ObservationConfig(
        patch_size_m=float(args.obs_patch_size_m),
        patch_cells=int(args.obs_patch_cells),
        include_edt=True,
        edt_clip_m=float(args.obs_edt_clip_m),
    )
    map_cache: dict[int, Any] = {}
    demo_rows: list[dict[str, Any]] = []
    stats = ExtractionStats(selected_rows=len(rows_with_index))

    for source_row_index, row in rows_with_index:
        if not bool(row.get("oracle_connectable")):
            stats = stats.add(skipped_not_connectable=1)
            continue
        grid_map = _grid_for_row(row, cfg, footprint, map_cache)
        checker = GridFootprintChecker(grid_map, footprint, theta_bins=int(args.theta_bins), padding=args.collision_padding_m)
        oracle_type = _choose_oracle(row, str(args.oracle_types))
        path = _replay_oracle_path(row, oracle_type, grid_map, footprint, cfg, args)
        if not path:
            stats = stats.add(skipped_oracle_replay_failed=1)
            continue
        stats = stats.add(replay_success_rows=1)
        extracted, path_stats = _extract_path_rows(
            path,
            row=row,
            source_row_index=source_row_index,
            oracle_type=oracle_type,
            grid_map=grid_map,
            checker=checker,
            footprint=footprint,
            params=params,
            obs_config=obs_config,
            args=args,
            source_head=source_head,
            sample_id_start=len(demo_rows),
        )
        demo_rows.extend(extracted)
        stats = stats.add(demo_rows=len(extracted), **path_stats)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(demo_rows, schema=DEMO_SCHEMA)
    pq.write_table(table, output)
    summary = _summary_payload(
        args=args,
        raw_argv=raw_argv,
        output=output,
        source_head=source_head,
        stats=stats,
        input_row_count=pq.read_table(args.input).num_rows,
        obs_config=obs_config,
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
        "min_step_length_m",
        "obs_patch_size_m",
        "obs_edt_clip_m",
    ):
        value = float(getattr(args, name))
        if not (math.isfinite(value) and value > 0.0):
            raise ValueError(f"--{name.replace('_', '-')} must be finite and positive")
    for name in ("oracle_a_max_nodes", "oracle_b_segment_max_nodes", "theta_bins", "obs_patch_cells"):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")


def _selected_rows(args: argparse.Namespace) -> list[tuple[int, dict[str, Any]]]:
    rows = pq.read_table(args.input).to_pylist()
    buckets = _csv_set(str(args.buckets))
    include_b_sources = _csv_set(args.oracle_b_candidate_sources)
    exclude_b_sources = _csv_set(args.exclude_oracle_b_candidate_sources)
    filter_best_oracle = str(args.filter_best_oracle)
    selected = [
        (idx, dict(row))
        for idx, row in enumerate(rows)
        if _row_matches_selection(
            row,
            buckets=buckets,
            filter_best_oracle=filter_best_oracle,
            include_b_sources=include_b_sources,
            exclude_b_sources=exclude_b_sources,
        )
    ]
    start = int(args.row_offset)
    end = None if args.max_records is None else start + int(args.max_records)
    return selected[start:end]


def _csv_set(raw: str | None) -> set[str]:
    if raw is None:
        return set()
    return {part.strip() for part in str(raw).split(",") if part.strip()}


def _row_matches_selection(
    row: dict[str, Any],
    *,
    buckets: set[str],
    filter_best_oracle: str,
    include_b_sources: set[str],
    exclude_b_sources: set[str],
) -> bool:
    if buckets and str(row["difficulty_bucket"]) not in buckets:
        return False
    if not bool(row.get("oracle_connectable")):
        return False
    best_oracle = str(row.get("best_oracle"))
    if filter_best_oracle != "any" and best_oracle != filter_best_oracle:
        return False
    b_source = str(row.get("oracle_b_selected_candidate_source"))
    if include_b_sources and b_source not in include_b_sources:
        return False
    if exclude_b_sources and b_source in exclude_b_sources:
        return False
    return True


def _choose_oracle(row: dict[str, Any], mode: str) -> str:
    if mode == "oracle_a":
        return "oracle_a"
    if mode == "oracle_b":
        return "oracle_b"
    best = row.get("best_oracle")
    if best in {"oracle_a", "oracle_b"}:
        return str(best)
    return "oracle_a" if bool(row.get("oracle_a_success")) else "oracle_b"


def _replay_oracle_path(row: dict[str, Any], oracle_type: str, grid_map: Any, footprint: TwoCircleFootprint, cfg: MainEvaluationConfig, args: argparse.Namespace) -> tuple[Pose, ...]:
    state = _pose_from_row(row, "state")
    goal = _pose_from_row(row, "goal")
    if oracle_type == "oracle_a":
        if not bool(row.get("oracle_a_success")):
            return ()
        plan = _plan_disabled_ha(grid_map, footprint, cfg, state, goal, float(args.oracle_a_timeout_s), int(args.oracle_a_max_nodes))
        return tuple(plan.poses) if plan.success else ()
    if oracle_type != "oracle_b" or not bool(row.get("oracle_b_success")):
        return ()
    candidate = (
        _required_float(row, "oracle_b_selected_candidate_x"),
        _required_float(row, "oracle_b_selected_candidate_y"),
        _required_float(row, "oracle_b_selected_candidate_theta"),
    )
    segment = _plan_disabled_ha(
        grid_map,
        footprint,
        cfg,
        state,
        candidate,
        float(args.oracle_b_segment_timeout_s),
        int(args.oracle_b_segment_max_nodes),
    )
    if not segment.success or not segment.poses:
        return ()
    terminal_rs = _safe_rs_check(grid_map, footprint, segment.poses[-1], goal, args)
    if terminal_rs is None or not terminal_rs.collision_free:
        return ()
    rs_poses = states_as_tuples(terminal_rs.samples)
    return _append_without_duplicate(segment.poses, rs_poses[1:])


def _extract_path_rows(
    path: tuple[Pose, ...],
    *,
    row: dict[str, Any],
    source_row_index: int,
    oracle_type: str,
    grid_map: Any,
    checker: GridFootprintChecker,
    footprint: TwoCircleFootprint,
    params: AckermannParams,
    obs_config: ObservationConfig,
    args: argparse.Namespace,
    source_head: str,
    sample_id_start: int,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    out: list[dict[str, Any]] = []
    skipped = {
        "skipped_terminal_rs_ready": 0,
        "skipped_collision": 0,
        "skipped_reverse": 0,
        "skipped_short": 0,
    }
    goal = AckermannState(float(row["goal_x"]), float(row["goal_y"]), float(row["goal_theta"]))
    for step_index, (current_pose, next_pose) in enumerate(zip(path[:-1], path[1:])):
        current = AckermannState(*current_pose)
        nxt = AckermannState(*next_pose)
        if checker.collides_pose(current.x, current.y, current.theta) or checker.collides_pose(nxt.x, nxt.y, nxt.theta):
            skipped["skipped_collision"] += 1
            continue
        terminal = check_terminal_rs_connectable(
            grid_map=grid_map,
            footprint=footprint,
            state=current,
            goal=goal,
            turning_radius_m=float(args.turning_radius_m),
            wheelbase_m=float(args.wheelbase_m),
            sample_step_m=float(args.rs_sample_step_m),
            theta_bins=int(args.theta_bins),
            collision_padding_m=args.collision_padding_m,
            checker=checker,
        )
        if bool(args.stop_at_terminal_rs) and terminal.success:
            skipped["skipped_terminal_rs_ready"] += max(1, len(path) - step_index - 1)
            break
        action = _estimate_action(current, nxt, params, min_step_length_m=float(args.min_step_length_m))
        if action is None:
            skipped["skipped_short"] += 1
            continue
        steering, curvature, direction, step_length = action
        if direction < 0:
            skipped["skipped_reverse"] += 1
            continue
        obs_scalar = build_scalar_observation(current, goal, remaining_steps=max(0, len(path) - step_index - 1))
        out.append(
            {
                "sample_id": int(sample_id_start + len(out)),
                "source_row_index": int(source_row_index),
                "query_id": str(row["query_id"]),
                "difficulty_bucket": str(row["difficulty_bucket"]),
                "profile_name": str(row["profile_name"]),
                "map_seed": int(row["map_seed"]),
                "query_seed": int(row["query_seed"]),
                "distance_bin_key": str(row["distance_bin_key"]),
                "dedup_key": None if row.get("dedup_key") is None else str(row.get("dedup_key")),
                "expansion_idx": int(row["expansion_idx"]),
                "oracle_type": str(oracle_type),
                "path_step_index": int(step_index),
                "remaining_oracle_steps": int(max(0, len(path) - step_index - 1)),
                "current_x": float(current.x),
                "current_y": float(current.y),
                "current_theta": float(current.theta),
                "next_x": float(nxt.x),
                "next_y": float(nxt.y),
                "next_theta": float(nxt.theta),
                "goal_x": float(goal.x),
                "goal_y": float(goal.y),
                "goal_theta": float(goal.theta),
                "expert_steering_rad": float(steering),
                "expert_curvature": float(curvature),
                "expert_direction": int(direction),
                "step_length_m": float(step_length),
                "obs_scalar": [float(value) for value in obs_scalar],
                "terminal_rs_checked": True,
                "terminal_rs_success": bool(terminal.success),
                "terminal_rs_path_length_m": terminal.path_length_m,
                "source_head": str(source_head),
            }
        )
    return out, skipped


def _estimate_action(
    current: AckermannState,
    nxt: AckermannState,
    params: AckermannParams,
    *,
    min_step_length_m: float,
) -> tuple[float, float, int, float] | None:
    dx = float(nxt.x) - float(current.x)
    dy = float(nxt.y) - float(current.y)
    step_length = math.hypot(dx, dy)
    if step_length < float(min_step_length_m):
        return None
    forward_projection = dx * math.cos(float(current.theta)) + dy * math.sin(float(current.theta))
    direction = 1 if forward_projection >= 0.0 else -1
    signed_step = step_length * float(direction)
    curvature = wrap_pi(float(nxt.theta) - float(current.theta)) / signed_step
    steering = math.atan(float(curvature) * float(params.wheelbase))
    steering = max(-float(params.max_steer), min(float(params.max_steer), steering))
    return float(steering), float(curvature), int(direction), float(step_length)


def _summary_payload(
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    output: Path,
    source_head: str,
    stats: ExtractionStats,
    input_row_count: int,
    obs_config: ObservationConfig,
) -> dict[str, Any]:
    return {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": str(source_head),
        "command": " ".join(["python -m forest_n3p.scripts.extract_oracle_demonstrations", *raw_argv]),
        "input": str(args.input),
        "output": str(output),
        "input_row_count": int(input_row_count),
        **{key: int(value) for key, value in stats.__dict__.items()},
        "config": {
            "density_profile_buckets": str(args.density_profile_buckets),
            "buckets": str(args.buckets),
            "oracle_types": str(args.oracle_types),
            "filter_best_oracle": str(args.filter_best_oracle),
            "oracle_b_candidate_sources": args.oracle_b_candidate_sources,
            "exclude_oracle_b_candidate_sources": args.exclude_oracle_b_candidate_sources,
            "max_records": args.max_records,
            "row_offset": int(args.row_offset),
            "stop_at_terminal_rs": bool(args.stop_at_terminal_rs),
            "min_step_length_m": float(args.min_step_length_m),
            "turning_radius_m": float(args.turning_radius_m),
            "wheelbase_m": float(args.wheelbase_m),
            "theta_bins": int(args.theta_bins),
            "rs_sample_step_m": float(args.rs_sample_step_m),
            "obs_config": {
                "patch_storage": "reconstructable_from_map_seed_pose_goal_not_inlined",
                "patch_size_m": float(obs_config.patch_size_m),
                "patch_cells": int(obs_config.patch_cells),
                "include_edt": bool(obs_config.include_edt),
                "edt_clip_m": float(obs_config.edt_clip_m),
            },
        },
    }


def _pose_from_row(row: dict[str, Any], prefix: str) -> Pose:
    return (float(row[f"{prefix}_x"]), float(row[f"{prefix}_y"]), wrap_pi(float(row[f"{prefix}_theta"])))


def _required_float(row: dict[str, Any], key: str) -> float:
    value = row.get(key)
    if value is None:
        raise ValueError(f"missing required value {key!r}")
    return float(value)


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop extraction.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
