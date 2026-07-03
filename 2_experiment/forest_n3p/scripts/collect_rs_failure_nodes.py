from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pyarrow as pa
import pyarrow.parquet as pq

from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _generate_grid_map,
    _make_planner,
    _profile_by_name,
    build_query_set,
    default_main_evaluation_profiles,
    validation_main_evaluation_profiles,
)
from forest_n3p.third_party.pathplan import AckermannState, TwoCircleFootprint


SCHEMA = pa.schema(
    [
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("query_seed", pa.int64()),
        ("distance_bin_key", pa.string()),
        ("expansion_idx", pa.int64()),
        ("analytic_operator", pa.string()),
        ("state_x", pa.float64()),
        ("state_y", pa.float64()),
        ("state_theta", pa.float64()),
        ("goal_x", pa.float64()),
        ("goal_y", pa.float64()),
        ("goal_theta", pa.float64()),
        ("h_holo", pa.float64()),
        ("h_rs", pa.float64()),
        ("nearest_obstacle_m", pa.float64()),
        ("failed_radii", pa.list_(pa.float64())),
        ("failed_radius_count", pa.int64()),
        ("plan_success", pa.bool_()),
        ("plan_failure_reason", pa.string()),
        ("plan_expansions", pa.int64()),
        ("plan_time_s", pa.float64()),
        ("plan_analytic_attempts", pa.int64()),
        ("plan_analytic_successes", pa.int64()),
        ("source_head", pa.string()),
    ]
)


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Collect failed analytic expansion nodes for Module2 oracle analysis.")
    parser.add_argument("--output", type=Path, default=Path("0_trials/module2_oracle_shape/rs_failure_nodes.parquet"))
    parser.add_argument("--queries-per-bucket", type=int, default=10)
    parser.add_argument("--seed-count", type=int, default=1)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="validation_t06")
    parser.add_argument("--buckets", default="Complex,Extreme")
    parser.add_argument("--analytic-operator", choices=("single_rs", "dang_multi_rs"), default="dang_multi_rs")
    parser.add_argument("--timeout-s", type=float, default=2.5)
    parser.add_argument("--max-nodes", type=int, default=15_000)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    source_head = str(args.source_head) if args.source_head else _source_head()
    cfg = MainEvaluationConfig(
        seed=int(args.seed),
        queries_per_bucket=int(args.queries_per_bucket),
        seed_count=int(args.seed_count),
        queries_per_map=int(args.queries_per_map),
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        methods=("ha_dang_multi_rs",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    requested_buckets = {part.strip() for part in str(args.buckets).split(",") if part.strip()}
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    queries = tuple(query for query in build_query_set(cfg) if query.difficulty_bucket in requested_buckets)
    map_cache = {}
    rows: list[dict[str, Any]] = []

    for query in queries:
        grid_map = map_cache.get(query.map_seed)
        if grid_map is None:
            profile = _profile_by_name(cfg.profiles, query.profile_name)
            grid_map = _generate_grid_map(profile, query.map_seed, cfg, footprint)
            map_cache[query.map_seed] = grid_map

        planner = _make_planner(grid_map, footprint, cfg, analytic_operator=str(args.analytic_operator))
        states, stats = planner.plan(
            AckermannState(*query.start),
            AckermannState(*query.goal),
            timeout=float(args.timeout_s),
            max_nodes=int(args.max_nodes),
        )
        records = stats.get("analytic_failure_records", ())
        for record in records:
            rows.append(
                {
                    "query_id": query.query_id,
                    "difficulty_bucket": query.difficulty_bucket,
                    "profile_name": query.profile_name,
                    "map_seed": int(query.map_seed),
                    "query_seed": int(query.query_seed),
                    "distance_bin_key": query.distance_bin_key,
                    "expansion_idx": int(record["expansion_idx"]),
                    "analytic_operator": str(record["analytic_operator"]),
                    "state_x": float(record["state_x"]),
                    "state_y": float(record["state_y"]),
                    "state_theta": float(record["state_theta"]),
                    "goal_x": float(record["goal_x"]),
                    "goal_y": float(record["goal_y"]),
                    "goal_theta": float(record["goal_theta"]),
                    "h_holo": _optional_float(record.get("h_holo")),
                    "h_rs": _optional_float(record.get("h_rs")),
                    "nearest_obstacle_m": float(record["nearest_obstacle_m"]),
                    "failed_radii": [float(radius) for radius in record.get("failed_radii", ())],
                    "failed_radius_count": int(record["failed_radius_count"]),
                    "plan_success": bool(states) and stats.get("failure_reason") is None,
                    "plan_failure_reason": stats.get("failure_reason"),
                    "plan_expansions": int(stats.get("expansions", 0)),
                    "plan_time_s": float(stats.get("time", 0.0)),
                    "plan_analytic_attempts": int(stats.get("analytic_attempts", 0)),
                    "plan_analytic_successes": int(stats.get("analytic_successes", 0)),
                    "source_head": source_head,
                }
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    pq.write_table(table, output)

    summary = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": " ".join(["python -m forest_n3p.scripts.collect_rs_failure_nodes", *raw_argv]),
        "output": str(output),
        "row_count": len(rows),
        "query_count": len(queries),
        "buckets": sorted(requested_buckets),
        "analytic_operator": str(args.analytic_operator),
        "queries_per_bucket": int(args.queries_per_bucket),
        "seed_count": int(args.seed_count),
        "queries_per_map": int(args.queries_per_map),
    }
    summary_path = output.with_name(output.stem + "_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _profiles_from_bucket_mode(mode: str):
    if mode == "original_t06":
        return default_main_evaluation_profiles()
    if mode == "validation_t06":
        return validation_main_evaluation_profiles()
    raise ValueError(f"unsupported density profile bucket mode: {mode}")


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop collection.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
