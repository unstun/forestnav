from __future__ import annotations

import argparse
import json
import math
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from scipy.ndimage import distance_transform_edt

from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _generate_grid_map,
    _profile_by_name,
    validation_main_evaluation_profiles,
)
from forest_n3p.rs_utils import generate_reeds_shepp_path, sample_reeds_shepp_path
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import EDTCollisionChecker, GridFootprintChecker
from forest_n3p.third_party.pathplan.robot import sample_constant_steer_motion


AGGREGATE_SCHEMA = pa.schema(
    [
        ("source_row_index", pa.int64()),
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("expansion_idx", pa.int64()),
        ("checker_type", pa.string()),
        ("rollout_step_count", pa.int64()),
        ("action_step_m", pa.float64()),
        ("collision_sample_step_m", pa.float64()),
        ("rollout_sample_count", pa.int64()),
        ("terminal_rs_sample_count", pa.float64()),
        ("start_collides", pa.bool_()),
        ("rollout_collision_rate", pa.float64()),
        ("terminal_rs_success_rate", pa.float64()),
        ("sampling_mean_ms", pa.float64()),
        ("sampling_p50_ms", pa.float64()),
        ("sampling_p95_ms", pa.float64()),
        ("collision_mean_ms", pa.float64()),
        ("collision_p50_ms", pa.float64()),
        ("collision_p95_ms", pa.float64()),
        ("rollout_total_mean_ms", pa.float64()),
        ("rollout_total_p50_ms", pa.float64()),
        ("rollout_total_p95_ms", pa.float64()),
        ("terminal_rs_mean_ms", pa.float64()),
        ("terminal_rs_p50_ms", pa.float64()),
        ("terminal_rs_p95_ms", pa.float64()),
        ("candidate_total_mean_ms", pa.float64()),
        ("candidate_total_p50_ms", pa.float64()),
        ("candidate_total_p95_ms", pa.float64()),
        ("rollout_total_to_d01_attempt_p50", pa.float64()),
        ("candidate_total_to_d01_attempt_p50", pa.float64()),
        ("source_head", pa.string()),
    ]
)


SAMPLE_SCHEMA = pa.schema(
    [
        ("source_row_index", pa.int64()),
        ("query_id", pa.string()),
        ("checker_type", pa.string()),
        ("rollout_step_count", pa.int64()),
        ("iteration", pa.int64()),
        ("sampling_ms", pa.float64()),
        ("collision_ms", pa.float64()),
        ("rollout_total_ms", pa.float64()),
        ("terminal_rs_ms", pa.float64()),
        ("candidate_total_ms", pa.float64()),
        ("rollout_collides", pa.bool_()),
        ("terminal_rs_success", pa.bool_()),
        ("source_head", pa.string()),
    ]
)


@dataclass(frozen=True)
class TimingSeries:
    sampling_ms: tuple[float, ...]
    collision_ms: tuple[float, ...]
    rollout_total_ms: tuple[float, ...]
    terminal_rs_ms: tuple[float, ...]
    candidate_total_ms: tuple[float, ...]
    rollout_collides: tuple[bool, ...]
    terminal_rs_success: tuple[bool, ...]
    rollout_sample_count: int
    terminal_rs_sample_count: float | None


@dataclass(frozen=True)
class RolloutBudgetConfig:
    action_step_m: float
    collision_sample_step_m: float
    rollout_step_counts: tuple[int, ...]
    checker_types: tuple[str, ...]
    timed_iterations: int
    max_records: int
    skip_colliding_starts: bool


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    source_head = str(args.source_head) if args.source_head else _source_head()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    d01_reference = _load_d01_reference(Path(args.d01_summary))
    budget_config = RolloutBudgetConfig(
        action_step_m=float(args.action_step_m),
        collision_sample_step_m=float(args.collision_sample_step_m),
        rollout_step_counts=_parse_positive_int_list(str(args.rollout_step_counts), name="rollout-step-counts"),
        checker_types=_parse_checker_types(str(args.checker_types)),
        timed_iterations=int(args.timed_iterations),
        max_records=int(args.max_records),
        skip_colliding_starts=bool(args.skip_colliding_starts),
    )

    cfg = MainEvaluationConfig(
        seed=int(args.seed),
        profiles=validation_main_evaluation_profiles(),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    params = AckermannParams(wheelbase=float(args.wheelbase_m), min_turn_radius=float(args.turning_radius_m))
    source_rows = _selected_source_rows(args, cfg, footprint)

    map_cache: dict[int, GridMap] = {}
    checker_cache: dict[tuple[int, str], Any] = {}
    aggregate_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    skipped_colliding = 0
    measured_sources = 0

    for source_index, row in source_rows:
        grid_map = _grid_for_row(row, cfg, footprint, map_cache)
        grid_checker = _checker_for_row(row, grid_map, footprint, checker_cache, "grid", args)
        start = _state_from_row(row)
        start_collides = bool(grid_checker.collides_pose(start.x, start.y, start.theta))
        if start_collides and bool(args.skip_colliding_starts):
            skipped_colliding += 1
            continue
        measured_sources += 1
        for checker_type in budget_config.checker_types:
            checker = _checker_for_row(row, grid_map, footprint, checker_cache, checker_type, args)
            for rollout_step_count in budget_config.rollout_step_counts:
                series = _measure_one_config(
                    params=params,
                    checker=checker,
                    row=row,
                    rollout_step_count=int(rollout_step_count),
                    action_step_m=float(args.action_step_m),
                    collision_sample_step_m=float(args.collision_sample_step_m),
                    timed_iterations=int(args.timed_iterations),
                    include_terminal_rs=bool(args.include_terminal_rs),
                    terminal_checker=grid_checker,
                    turning_radius_m=float(args.turning_radius_m),
                    wheelbase_m=float(args.wheelbase_m),
                )
                aggregate_rows.append(
                    _aggregate_row(
                        source_index=source_index,
                        row=row,
                        checker_type=checker_type,
                        rollout_step_count=int(rollout_step_count),
                        args=args,
                        source_head=source_head,
                        start_collides=start_collides,
                        series=series,
                        d01_reference=d01_reference,
                    )
                )
                for iteration in range(int(args.timed_iterations)):
                    sample_rows.append(
                        {
                            "source_row_index": int(source_index),
                            "query_id": str(row["query_id"]),
                            "checker_type": str(checker_type),
                            "rollout_step_count": int(rollout_step_count),
                            "iteration": int(iteration),
                            "sampling_ms": float(series.sampling_ms[iteration]),
                            "collision_ms": float(series.collision_ms[iteration]),
                            "rollout_total_ms": float(series.rollout_total_ms[iteration]),
                            "terminal_rs_ms": float(series.terminal_rs_ms[iteration]),
                            "candidate_total_ms": float(series.candidate_total_ms[iteration]),
                            "rollout_collides": bool(series.rollout_collides[iteration]),
                            "terminal_rs_success": bool(series.terminal_rs_success[iteration]),
                            "source_head": source_head,
                        }
                    )
        if measured_sources >= int(args.max_records):
            break

    aggregate_path = output_dir / "rollout_collision_records.parquet"
    sample_path = output_dir / "rollout_collision_samples.parquet"
    pq.write_table(pa.Table.from_pylist(aggregate_rows, schema=AGGREGATE_SCHEMA), aggregate_path)
    pq.write_table(pa.Table.from_pylist(sample_rows, schema=SAMPLE_SCHEMA), sample_path)

    summary = _summary_payload(
        args=args,
        raw_argv=raw_argv,
        output_dir=output_dir,
        aggregate_path=aggregate_path,
        sample_path=sample_path,
        source_head=source_head,
        budget_config=budget_config,
        d01_reference=d01_reference,
        aggregate_rows=aggregate_rows,
        source_row_count=len(source_rows),
        measured_source_count=measured_sources,
        skipped_colliding_start_count=skipped_colliding,
    )
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(_stdout_summary(summary), indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Module2 D02 rollout collision-checking budget benchmark.")
    parser.add_argument("--input", type=Path, default=Path("0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("0_trials/module2_cost_accounting/d02_rollout_collision_budget"))
    parser.add_argument("--d01-summary", type=Path, default=Path("0_trials/module2_cost_accounting/d01_analytic_cost_distribution/summary.json"))
    parser.add_argument("--buckets", default="Complex,Extreme")
    parser.add_argument("--max-records", type=int, default=24)
    parser.add_argument("--row-offset", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--turning-radius-m", type=float, default=1.1284)
    parser.add_argument("--wheelbase-m", type=float, default=0.6)
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--collision-padding-m", type=float, default=None)
    parser.add_argument("--action-step-m", type=float, default=0.3)
    parser.add_argument("--collision-sample-step-m", type=float, default=0.1)
    parser.add_argument("--rollout-step-counts", default="1,8,16,32")
    parser.add_argument("--checker-types", default="grid,edt")
    parser.add_argument("--timed-iterations", type=int, default=100)
    parser.add_argument("--include-terminal-rs", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--skip-colliding-starts", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)
    _validate_args(args)
    return args


def _validate_args(args: argparse.Namespace) -> None:
    for name in ("turning_radius_m", "wheelbase_m", "action_step_m", "collision_sample_step_m"):
        value = float(getattr(args, name))
        if not (math.isfinite(value) and value > 0.0):
            raise ValueError(f"--{name.replace('_', '-')} must be finite and positive")
    for name in ("max_records", "theta_bins", "timed_iterations"):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    if int(args.row_offset) < 0:
        raise ValueError("--row-offset must be non-negative")


def _selected_source_rows(
    args: argparse.Namespace,
    cfg: MainEvaluationConfig,
    footprint: TwoCircleFootprint,
) -> list[tuple[int, dict[str, Any]]]:
    rows = pq.read_table(args.input).to_pylist()
    buckets = set(_parse_str_list(str(args.buckets)))
    out: list[tuple[int, dict[str, Any]]] = []
    for idx, row in enumerate(rows):
        if buckets and str(row["difficulty_bucket"]) not in buckets:
            continue
        # Validate that the map profile still exists before the expensive run.
        _profile_by_name(cfg.profiles, str(row["profile_name"]))
        out.append((int(idx), dict(row)))
    start = int(args.row_offset)
    return out[start:]


def _grid_for_row(
    row: dict[str, Any],
    cfg: MainEvaluationConfig,
    footprint: TwoCircleFootprint,
    map_cache: dict[int, GridMap],
) -> GridMap:
    map_seed = int(row["map_seed"])
    grid_map = map_cache.get(map_seed)
    if grid_map is not None:
        return grid_map
    profile = _profile_by_name(cfg.profiles, str(row["profile_name"]))
    grid_map = _generate_grid_map(profile, map_seed, cfg, footprint)
    map_cache[map_seed] = grid_map
    return grid_map


def _checker_for_row(
    row: dict[str, Any],
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    checker_cache: dict[tuple[int, str], Any],
    checker_type: str,
    args: argparse.Namespace,
):
    key = (int(row["map_seed"]), str(checker_type))
    cached = checker_cache.get(key)
    if cached is not None:
        return cached
    if checker_type == "grid":
        checker = GridFootprintChecker(
            grid_map,
            footprint,
            theta_bins=int(args.theta_bins),
            padding=args.collision_padding_m,
        )
    elif checker_type == "edt":
        edt_m = distance_transform_edt(grid_map.data == 0).astype(np.float32) * float(grid_map.resolution)
        checker = EDTCollisionChecker(
            edt_m,
            cell_size_m=float(grid_map.resolution),
            footprint=footprint,
        )
    else:
        raise ValueError(f"unsupported checker_type: {checker_type}")
    checker_cache[key] = checker
    return checker


def _state_from_row(row: dict[str, Any]) -> AckermannState:
    return AckermannState(float(row["state_x"]), float(row["state_y"]), float(row["state_theta"]))


def _goal_from_row(row: dict[str, Any]) -> AckermannState:
    return AckermannState(float(row["goal_x"]), float(row["goal_y"]), float(row["goal_theta"]))


def steering_fraction_sequence(step_count: int) -> tuple[float, ...]:
    """Deterministic steering pattern for a policy-like rollout budget proxy."""
    if int(step_count) <= 0:
        raise ValueError("step_count must be positive")
    base = (-0.65, -0.25, 0.0, 0.35, 0.70, 0.25, -0.35, 0.0)
    return tuple(float(base[idx % len(base)]) for idx in range(int(step_count)))


def sample_policy_like_rollout(
    *,
    start: AckermannState,
    params: AckermannParams,
    rollout_step_count: int,
    action_step_m: float,
    collision_sample_step_m: float,
) -> tuple[tuple[AckermannState, ...], AckermannState]:
    samples: list[AckermannState] = []
    current = start
    max_steer = float(params.max_steer)
    for fraction in steering_fraction_sequence(int(rollout_step_count)):
        segment, _ = sample_constant_steer_motion(
            current,
            float(fraction) * max_steer,
            1,
            float(action_step_m),
            params,
            step=float(collision_sample_step_m),
            footprint=None,
        )
        if samples:
            samples.extend(segment[1:])
        else:
            samples.extend(segment)
        current = segment[-1]
    return tuple(samples), current


def _measure_one_config(
    *,
    params: AckermannParams,
    checker,
    row: dict[str, Any],
    rollout_step_count: int,
    action_step_m: float,
    collision_sample_step_m: float,
    timed_iterations: int,
    include_terminal_rs: bool,
    terminal_checker: GridFootprintChecker,
    turning_radius_m: float,
    wheelbase_m: float,
) -> TimingSeries:
    start_state = _state_from_row(row)
    goal_state = _goal_from_row(row)
    sampling_ms: list[float] = []
    collision_ms: list[float] = []
    rollout_total_ms: list[float] = []
    terminal_rs_ms: list[float] = []
    candidate_total_ms: list[float] = []
    rollout_collides: list[bool] = []
    terminal_rs_success: list[bool] = []
    rollout_sample_count = 0
    terminal_rs_sample_count: float | None = None

    for _ in range(int(timed_iterations)):
        sample_start = time.perf_counter_ns()
        samples, final_state = sample_policy_like_rollout(
            start=start_state,
            params=params,
            rollout_step_count=int(rollout_step_count),
            action_step_m=float(action_step_m),
            collision_sample_step_m=float(collision_sample_step_m),
        )
        sample_end = time.perf_counter_ns()
        coll_start = time.perf_counter_ns()
        collides = bool(checker.collides_path(samples))
        coll_end = time.perf_counter_ns()
        rs_ms, rs_success, rs_sample_count = _measure_terminal_rs(
            final_state,
            goal_state,
            terminal_checker,
            include_terminal_rs=include_terminal_rs,
            turning_radius_m=float(turning_radius_m),
            wheelbase_m=float(wheelbase_m),
            sample_step=float(collision_sample_step_m),
        )
        sampling_value = _ns_to_ms(sample_end - sample_start)
        collision_value = _ns_to_ms(coll_end - coll_start)
        rollout_value = sampling_value + collision_value
        sampling_ms.append(sampling_value)
        collision_ms.append(collision_value)
        rollout_total_ms.append(rollout_value)
        terminal_rs_ms.append(rs_ms)
        candidate_total_ms.append(rollout_value + rs_ms)
        rollout_collides.append(collides)
        terminal_rs_success.append(rs_success)
        rollout_sample_count = int(len(samples))
        terminal_rs_sample_count = rs_sample_count

    return TimingSeries(
        sampling_ms=tuple(sampling_ms),
        collision_ms=tuple(collision_ms),
        rollout_total_ms=tuple(rollout_total_ms),
        terminal_rs_ms=tuple(terminal_rs_ms),
        candidate_total_ms=tuple(candidate_total_ms),
        rollout_collides=tuple(rollout_collides),
        terminal_rs_success=tuple(terminal_rs_success),
        rollout_sample_count=int(rollout_sample_count),
        terminal_rs_sample_count=terminal_rs_sample_count,
    )


def _measure_terminal_rs(
    start: AckermannState,
    goal: AckermannState,
    checker: GridFootprintChecker,
    *,
    include_terminal_rs: bool,
    turning_radius_m: float,
    wheelbase_m: float,
    sample_step: float,
) -> tuple[float, bool, float | None]:
    if not include_terminal_rs:
        return 0.0, False, None
    start_ns = time.perf_counter_ns()
    try:
        path = generate_reeds_shepp_path(start, goal, turning_radius=float(turning_radius_m))
        samples = sample_reeds_shepp_path(
            start,
            path,
            turning_radius=float(turning_radius_m),
            wheelbase=float(wheelbase_m),
            sample_step=float(sample_step),
        )
        success = not checker.collides_path(samples)
        sample_count: float | None = float(len(samples))
    except Exception:  # noqa: BLE001 - failed terminal RS is part of the budget distribution.
        success = False
        sample_count = None
    end_ns = time.perf_counter_ns()
    return _ns_to_ms(end_ns - start_ns), bool(success), sample_count


def _aggregate_row(
    *,
    source_index: int,
    row: dict[str, Any],
    checker_type: str,
    rollout_step_count: int,
    args: argparse.Namespace,
    source_head: str,
    start_collides: bool,
    series: TimingSeries,
    d01_reference: dict[str, float | str],
) -> dict[str, Any]:
    sampling = _series_stats(series.sampling_ms)
    collision = _series_stats(series.collision_ms)
    rollout = _series_stats(series.rollout_total_ms)
    terminal = _series_stats(series.terminal_rs_ms)
    candidate = _series_stats(series.candidate_total_ms)
    return {
        "source_row_index": int(source_index),
        "query_id": str(row["query_id"]),
        "difficulty_bucket": str(row["difficulty_bucket"]),
        "profile_name": str(row["profile_name"]),
        "map_seed": int(row["map_seed"]),
        "expansion_idx": int(row["expansion_idx"]),
        "checker_type": str(checker_type),
        "rollout_step_count": int(rollout_step_count),
        "action_step_m": float(args.action_step_m),
        "collision_sample_step_m": float(args.collision_sample_step_m),
        "rollout_sample_count": int(series.rollout_sample_count),
        "terminal_rs_sample_count": series.terminal_rs_sample_count,
        "start_collides": bool(start_collides),
        "rollout_collision_rate": _mean_bool(series.rollout_collides),
        "terminal_rs_success_rate": _mean_bool(series.terminal_rs_success),
        "sampling_mean_ms": sampling["mean"],
        "sampling_p50_ms": sampling["p50"],
        "sampling_p95_ms": sampling["p95"],
        "collision_mean_ms": collision["mean"],
        "collision_p50_ms": collision["p50"],
        "collision_p95_ms": collision["p95"],
        "rollout_total_mean_ms": rollout["mean"],
        "rollout_total_p50_ms": rollout["p50"],
        "rollout_total_p95_ms": rollout["p95"],
        "terminal_rs_mean_ms": terminal["mean"],
        "terminal_rs_p50_ms": terminal["p50"],
        "terminal_rs_p95_ms": terminal["p95"],
        "candidate_total_mean_ms": candidate["mean"],
        "candidate_total_p50_ms": candidate["p50"],
        "candidate_total_p95_ms": candidate["p95"],
        "rollout_total_to_d01_attempt_p50": _ratio(rollout["p50"], float(d01_reference["attempt_total_time_p50_ms"])),
        "candidate_total_to_d01_attempt_p50": _ratio(candidate["p50"], float(d01_reference["attempt_total_time_p50_ms"])),
        "source_head": str(source_head),
    }


def _summary_payload(
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    output_dir: Path,
    aggregate_path: Path,
    sample_path: Path,
    source_head: str,
    budget_config: RolloutBudgetConfig,
    d01_reference: dict[str, Any],
    aggregate_rows: list[dict[str, Any]],
    source_row_count: int,
    measured_source_count: int,
    skipped_colliding_start_count: int,
) -> dict[str, Any]:
    df = pd.DataFrame(aggregate_rows)
    return {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": " ".join(["python -m forest_n3p.scripts.run_rollout_collision_budget", *raw_argv]),
        "output_dir": str(output_dir),
        "outputs": {
            "aggregate_records": str(aggregate_path),
            "sample_records": str(sample_path),
        },
        "config": asdict(budget_config),
        "source": {
            "input": str(args.input),
            "source_row_count_after_bucket_filter": int(source_row_count),
            "measured_source_count": int(measured_source_count),
            "skipped_colliding_start_count": int(skipped_colliding_start_count),
        },
        "d01_reference": d01_reference,
        "aggregate_record_count": int(len(aggregate_rows)),
        "sample_record_count": int(len(aggregate_rows) * int(args.timed_iterations)),
        "overall": _overall_summary(df),
        "by_checker_and_steps": _by_checker_steps(df),
        "boundary": {
            "allowed": (
                "This artifact measures policy-like rollout sampling plus collision-checking overhead.",
                "candidate_total_ms also includes a terminal Reeds-Shepp generate/sample/collision-check proxy.",
                "Rows are sourced from deduplicated RS failure nodes and skip colliding starts by default.",
            ),
            "not_included": (
                "trained policy quality",
                "planner open-list integration overhead",
                "fallback primitive expansion after failed rollout",
                "CUDA neural forward timing",
            ),
        },
    }


def _overall_summary(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {}
    return {
        "rollout_total_p50_ms": _series_stats(df["rollout_total_p50_ms"])["p50"],
        "candidate_total_p50_ms": _series_stats(df["candidate_total_p50_ms"])["p50"],
        "max_candidate_total_p95_ms": float(df["candidate_total_p95_ms"].max()),
        "max_rollout_total_p95_ms": float(df["rollout_total_p95_ms"].max()),
    }


def _by_checker_steps(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {}
    out: dict[str, Any] = {}
    for (checker_type, steps), group in df.groupby(["checker_type", "rollout_step_count"]):
        out[f"{checker_type}:steps_{int(steps)}"] = {
            "record_count": int(len(group)),
            "rollout_total_p50_ms_mean": float(group["rollout_total_p50_ms"].mean()),
            "rollout_total_p95_ms_mean": float(group["rollout_total_p95_ms"].mean()),
            "candidate_total_p50_ms_mean": float(group["candidate_total_p50_ms"].mean()),
            "candidate_total_p95_ms_mean": float(group["candidate_total_p95_ms"].mean()),
            "rollout_collision_rate_mean": float(group["rollout_collision_rate"].mean()),
            "terminal_rs_success_rate_mean": float(group["terminal_rs_success_rate"].mean()),
        }
    return out


def _stdout_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": summary["status"],
        "output_dir": summary["output_dir"],
        "aggregate_record_count": summary["aggregate_record_count"],
        "sample_record_count": summary["sample_record_count"],
        "measured_source_count": summary["source"]["measured_source_count"],
        "skipped_colliding_start_count": summary["source"]["skipped_colliding_start_count"],
        "overall": summary["overall"],
        "by_checker_and_steps": summary["by_checker_and_steps"],
    }


def _load_d01_reference(path: Path) -> dict[str, float | str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    fields = payload["overall"]["fields"]["analytic_total_time_s"]
    collision_fields = payload["overall"]["fields"]["analytic_collision_check_time_s"]
    return {
        "path": str(path),
        "source_head": str(payload.get("source_head", "unknown")),
        "attempt_total_time_p50_ms": float(fields["p50"]) * 1000.0,
        "attempt_total_time_p95_ms": float(fields["p95"]) * 1000.0,
        "collision_time_p50_ms": float(collision_fields["p50"]) * 1000.0,
        "collision_time_p95_ms": float(collision_fields["p95"]) * 1000.0,
    }


def _series_stats(values: Sequence[float] | pd.Series) -> dict[str, float]:
    series = pd.Series([float(value) for value in values])
    if series.empty:
        return {"mean": 0.0, "p50": 0.0, "p95": 0.0}
    return {
        "mean": float(series.mean()),
        "p50": float(series.quantile(0.50)),
        "p95": float(series.quantile(0.95)),
    }


def _mean_bool(values: Sequence[bool]) -> float:
    return float(sum(bool(value) for value in values)) / float(len(values)) if values else 0.0


def _ratio(value: float, reference: float) -> float:
    return float(value) / float(reference) if float(reference) > 0.0 else float("nan")


def _ns_to_ms(value: int) -> float:
    return float(value) / 1_000_000.0


def _parse_checker_types(spec: str) -> tuple[str, ...]:
    values = _parse_str_list(spec)
    allowed = {"grid", "edt"}
    unknown = [value for value in values if value not in allowed]
    if unknown:
        raise ValueError(f"unsupported checker types: {unknown}")
    return values


def _parse_str_list(spec: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in str(spec).split(",") if part.strip())
    if not values:
        raise ValueError("list argument must not be empty")
    return values


def _parse_positive_int_list(spec: str, *, name: str) -> tuple[int, ...]:
    values = tuple(int(part) for part in _parse_str_list(spec))
    if any(value <= 0 for value in values):
        raise ValueError(f"--{name} values must be positive")
    return values


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop the benchmark.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
