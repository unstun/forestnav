from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd
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


ATTEMPT_SCHEMA = pa.schema(
    [
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("query_seed", pa.int64()),
        ("distance_bin_key", pa.string()),
        ("plan_success", pa.bool_()),
        ("plan_failure_reason", pa.string()),
        ("plan_expansions", pa.int64()),
        ("plan_time_s", pa.float64()),
        ("plan_analytic_attempts", pa.int64()),
        ("plan_analytic_successes", pa.int64()),
        ("attempt_index", pa.int64()),
        ("expansion_idx", pa.int64()),
        ("analytic_operator", pa.string()),
        ("state_x", pa.float64()),
        ("state_y", pa.float64()),
        ("state_theta", pa.float64()),
        ("goal_x", pa.float64()),
        ("goal_y", pa.float64()),
        ("goal_theta", pa.float64()),
        ("analytic_candidate_radius_count", pa.int64()),
        ("analytic_candidate_success_count", pa.int64()),
        ("analytic_candidate_failure_count", pa.int64()),
        ("analytic_rs_solve_time_s", pa.float64()),
        ("analytic_sample_time_s", pa.float64()),
        ("analytic_collision_check_time_s", pa.float64()),
        ("analytic_cost_eval_time_s", pa.float64()),
        ("analytic_total_time_s", pa.float64()),
        ("analytic_sample_count", pa.int64()),
        ("analytic_collision_check_count", pa.int64()),
        ("analytic_accepted_radius_m", pa.float64()),
        ("source_head", pa.string()),
    ]
)


CANDIDATE_SCHEMA = pa.schema(
    [
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("query_seed", pa.int64()),
        ("distance_bin_key", pa.string()),
        ("attempt_index", pa.int64()),
        ("expansion_idx", pa.int64()),
        ("candidate_index", pa.int64()),
        ("analytic_operator", pa.string()),
        ("radius_m", pa.float64()),
        ("success", pa.bool_()),
        ("failure_reason", pa.string()),
        ("rs_solve_time_s", pa.float64()),
        ("sample_time_s", pa.float64()),
        ("collision_check_time_s", pa.float64()),
        ("sample_count", pa.int64()),
        ("collision_check_count", pa.int64()),
        ("source_head", pa.string()),
    ]
)


QUERY_SCHEMA = pa.schema(
    [
        ("query_id", pa.string()),
        ("difficulty_bucket", pa.string()),
        ("profile_name", pa.string()),
        ("map_seed", pa.int64()),
        ("query_seed", pa.int64()),
        ("distance_bin_key", pa.string()),
        ("plan_success", pa.bool_()),
        ("plan_failure_reason", pa.string()),
        ("plan_expansions", pa.int64()),
        ("plan_time_s", pa.float64()),
        ("plan_analytic_attempts", pa.int64()),
        ("plan_analytic_successes", pa.int64()),
        ("analytic_candidate_radius_count", pa.int64()),
        ("analytic_candidate_success_count", pa.int64()),
        ("analytic_candidate_failure_count", pa.int64()),
        ("analytic_rs_solve_time_s", pa.float64()),
        ("analytic_sample_time_s", pa.float64()),
        ("analytic_collision_check_time_s", pa.float64()),
        ("analytic_cost_eval_time_s", pa.float64()),
        ("analytic_total_time_s", pa.float64()),
        ("analytic_sample_count", pa.int64()),
        ("analytic_collision_check_count", pa.int64()),
        ("source_head", pa.string()),
    ]
)


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Run Module2 D01 analytic expansion cost distribution.")
    parser.add_argument("--output-dir", type=Path, default=Path("0_trials/module2_cost_accounting/d01_analytic_cost_distribution"))
    parser.add_argument("--queries-per-bucket", type=int, default=10)
    parser.add_argument("--seed-count", type=int, default=1)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="validation_t06")
    parser.add_argument("--buckets", default="Complex,Extreme")
    parser.add_argument("--analytic-operator", choices=("single_rs", "dang_multi_rs"), default="dang_multi_rs")
    parser.add_argument("--timeout-s", type=float, default=2.5)
    parser.add_argument("--max-nodes", type=int, default=15_000)
    parser.add_argument("--max-queries", type=int, default=None)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    source_head = str(args.source_head) if args.source_head else _source_head()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
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
    queries = [query for query in build_query_set(cfg) if query.difficulty_bucket in requested_buckets]
    if args.max_queries is not None:
        queries = queries[: int(args.max_queries)]

    query_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    map_cache = {}
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
        base = _query_base(query)
        query_rows.append(
            {
                **base,
                "plan_success": bool(states) and stats.get("failure_reason") is None,
                "plan_failure_reason": _none_or_str(stats.get("failure_reason")),
                "plan_expansions": int(stats.get("expansions", 0)),
                "plan_time_s": float(stats.get("time", 0.0)),
                "plan_analytic_attempts": int(stats.get("analytic_attempts", 0)),
                "plan_analytic_successes": int(stats.get("analytic_successes", 0)),
                "analytic_candidate_radius_count": int(stats.get("analytic_candidate_radius_count", 0)),
                "analytic_candidate_success_count": int(stats.get("analytic_candidate_success_count", 0)),
                "analytic_candidate_failure_count": int(stats.get("analytic_candidate_failure_count", 0)),
                "analytic_rs_solve_time_s": float(stats.get("analytic_rs_solve_time_s", 0.0)),
                "analytic_sample_time_s": float(stats.get("analytic_sample_time_s", 0.0)),
                "analytic_collision_check_time_s": float(stats.get("analytic_collision_check_time_s", 0.0)),
                "analytic_cost_eval_time_s": float(stats.get("analytic_cost_eval_time_s", 0.0)),
                "analytic_total_time_s": float(stats.get("analytic_total_time_s", 0.0)),
                "analytic_sample_count": int(stats.get("analytic_sample_count", 0)),
                "analytic_collision_check_count": int(stats.get("analytic_collision_check_count", 0)),
                "source_head": source_head,
            }
        )
        for attempt in stats.get("analytic_telemetry_records", ()):
            attempt_base = {
                **base,
                "plan_success": bool(states) and stats.get("failure_reason") is None,
                "plan_failure_reason": _none_or_str(stats.get("failure_reason")),
                "plan_expansions": int(stats.get("expansions", 0)),
                "plan_time_s": float(stats.get("time", 0.0)),
                "plan_analytic_attempts": int(stats.get("analytic_attempts", 0)),
                "plan_analytic_successes": int(stats.get("analytic_successes", 0)),
                "attempt_index": int(attempt["attempt_index"]),
                "expansion_idx": int(attempt["expansion_idx"]),
                "analytic_operator": str(attempt["analytic_operator"]),
                "state_x": float(attempt["state_x"]),
                "state_y": float(attempt["state_y"]),
                "state_theta": float(attempt["state_theta"]),
                "goal_x": float(attempt["goal_x"]),
                "goal_y": float(attempt["goal_y"]),
                "goal_theta": float(attempt["goal_theta"]),
                "analytic_candidate_radius_count": int(attempt["analytic_candidate_radius_count"]),
                "analytic_candidate_success_count": int(attempt["analytic_candidate_success_count"]),
                "analytic_candidate_failure_count": int(attempt["analytic_candidate_failure_count"]),
                "analytic_rs_solve_time_s": float(attempt["analytic_rs_solve_time_s"]),
                "analytic_sample_time_s": float(attempt["analytic_sample_time_s"]),
                "analytic_collision_check_time_s": float(attempt["analytic_collision_check_time_s"]),
                "analytic_cost_eval_time_s": float(attempt["analytic_cost_eval_time_s"]),
                "analytic_total_time_s": float(attempt["analytic_total_time_s"]),
                "analytic_sample_count": int(attempt["analytic_sample_count"]),
                "analytic_collision_check_count": int(attempt["analytic_collision_check_count"]),
                "analytic_accepted_radius_m": _optional_float(attempt.get("analytic_accepted_radius_m")),
                "source_head": source_head,
            }
            attempt_rows.append(attempt_base)
            for candidate_index, candidate in enumerate(attempt.get("candidate_records", ())):
                candidate_rows.append(
                    {
                        **base,
                        "attempt_index": int(attempt["attempt_index"]),
                        "expansion_idx": int(attempt["expansion_idx"]),
                        "candidate_index": int(candidate_index),
                        "analytic_operator": str(attempt["analytic_operator"]),
                        "radius_m": float(candidate["radius_m"]),
                        "success": bool(candidate["success"]),
                        "failure_reason": _none_or_str(candidate.get("failure_reason")),
                        "rs_solve_time_s": float(candidate["rs_solve_time_s"]),
                        "sample_time_s": float(candidate["sample_time_s"]),
                        "collision_check_time_s": float(candidate["collision_check_time_s"]),
                        "sample_count": int(candidate["sample_count"]),
                        "collision_check_count": int(candidate["collision_check_count"]),
                        "source_head": source_head,
                    }
                )

    query_path = output_dir / "query_costs.parquet"
    attempt_path = output_dir / "attempt_costs.parquet"
    candidate_path = output_dir / "candidate_costs.parquet"
    pq.write_table(pa.Table.from_pylist(query_rows, schema=QUERY_SCHEMA), query_path)
    pq.write_table(pa.Table.from_pylist(attempt_rows, schema=ATTEMPT_SCHEMA), attempt_path)
    pq.write_table(pa.Table.from_pylist(candidate_rows, schema=CANDIDATE_SCHEMA), candidate_path)

    summary = _build_summary(
        query_rows,
        attempt_rows,
        candidate_rows,
        output_dir=output_dir,
        source_head=source_head,
        command=" ".join(["python -m forest_n3p.scripts.run_analytic_cost_distribution", *raw_argv]),
        args=args,
        requested_buckets=requested_buckets,
        outputs={
            "query_costs": query_path,
            "attempt_costs": attempt_path,
            "candidate_costs": candidate_path,
        },
    )
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(_stdout_summary(summary), indent=2, ensure_ascii=False))
    return 0


def _query_base(query) -> dict[str, Any]:
    return {
        "query_id": query.query_id,
        "difficulty_bucket": query.difficulty_bucket,
        "profile_name": query.profile_name,
        "map_seed": int(query.map_seed),
        "query_seed": int(query.query_seed),
        "distance_bin_key": query.distance_bin_key,
    }


def _build_summary(
    query_rows: list[dict[str, Any]],
    attempt_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    *,
    output_dir: Path,
    source_head: str,
    command: str,
    args: argparse.Namespace,
    requested_buckets: set[str],
    outputs: dict[str, Path],
) -> dict[str, Any]:
    query_df = pd.DataFrame(query_rows)
    attempt_df = pd.DataFrame(attempt_rows)
    candidate_df = pd.DataFrame(candidate_rows)
    return {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": command,
        "output_dir": str(output_dir),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "config": {
            "queries_per_bucket": int(args.queries_per_bucket),
            "seed_count": int(args.seed_count),
            "queries_per_map": int(args.queries_per_map),
            "seed": int(args.seed),
            "density_profile_buckets": str(args.density_profile_buckets),
            "buckets": sorted(requested_buckets),
            "analytic_operator": str(args.analytic_operator),
            "timeout_s": float(args.timeout_s),
            "max_nodes": int(args.max_nodes),
            "max_queries": None if args.max_queries is None else int(args.max_queries),
        },
        "counts": {
            "query_count": int(len(query_rows)),
            "attempt_count": int(len(attempt_rows)),
            "candidate_count": int(len(candidate_rows)),
            "plan_success_count": int(query_df["plan_success"].sum()) if not query_df.empty else 0,
            "plan_failure_count": int((~query_df["plan_success"]).sum()) if not query_df.empty else 0,
            "attempt_success_count": int((attempt_df["analytic_candidate_success_count"] > 0).sum()) if not attempt_df.empty else 0,
            "attempt_all_failed_count": int((attempt_df["analytic_candidate_success_count"] == 0).sum()) if not attempt_df.empty else 0,
            "candidate_success_count": int(candidate_df["success"].sum()) if not candidate_df.empty else 0,
            "candidate_failure_count": int((~candidate_df["success"]).sum()) if not candidate_df.empty else 0,
        },
        "failure_reason_counts": {
            "plan": _value_counts(query_df, "plan_failure_reason"),
            "candidate": _value_counts(candidate_df, "failure_reason"),
        },
        "time_budget_totals": _time_budget_totals(query_df, attempt_df),
        "overall": _distribution_block(attempt_df),
        "by_bucket": {
            str(bucket): _distribution_block(attempt_df[attempt_df["difficulty_bucket"] == bucket])
            for bucket in sorted(attempt_df["difficulty_bucket"].unique()) if not attempt_df.empty
        },
        "query_by_bucket": _query_bucket_block(query_df),
    }


def _distribution_block(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {"attempt_count": 0}
    fields = (
        "analytic_total_time_s",
        "analytic_rs_solve_time_s",
        "analytic_sample_time_s",
        "analytic_collision_check_time_s",
        "analytic_cost_eval_time_s",
        "analytic_candidate_radius_count",
        "analytic_candidate_success_count",
        "analytic_sample_count",
        "analytic_collision_check_count",
    )
    return {
        "attempt_count": int(len(df)),
        "success_candidate_attempt_count": int((df["analytic_candidate_success_count"] > 0).sum()),
        "all_failed_candidate_attempt_count": int((df["analytic_candidate_success_count"] == 0).sum()),
        "fields": {field: _series_stats(df[field]) for field in fields},
    }


def _query_bucket_block(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {}
    out: dict[str, Any] = {}
    for bucket, group in df.groupby("difficulty_bucket"):
        out[str(bucket)] = {
            "query_count": int(len(group)),
            "plan_success_count": int(group["plan_success"].sum()),
            "plan_failure_count": int((~group["plan_success"]).sum()),
            "analytic_attempts_total": int(group["plan_analytic_attempts"].sum()),
            "analytic_successes_total": int(group["plan_analytic_successes"].sum()),
        }
    return out


def _time_budget_totals(query_df: pd.DataFrame, attempt_df: pd.DataFrame) -> dict[str, float]:
    if query_df.empty:
        return {
            "plan_time_s": 0.0,
            "analytic_total_time_s": 0.0,
            "analytic_to_plan_time_ratio": 0.0,
        }
    plan_time = float(query_df["plan_time_s"].sum())
    analytic_time = float(attempt_df["analytic_total_time_s"].sum()) if not attempt_df.empty else 0.0
    ratio = analytic_time / plan_time if plan_time > 0.0 else 0.0
    return {
        "plan_time_s": plan_time,
        "analytic_total_time_s": analytic_time,
        "analytic_to_plan_time_ratio": ratio,
    }


def _value_counts(df: pd.DataFrame, column: str) -> dict[str, int]:
    if df.empty or column not in df:
        return {}
    counts = df[column].fillna("None").value_counts(dropna=False)
    return {str(key): int(value) for key, value in counts.items()}


def _series_stats(series: pd.Series) -> dict[str, float]:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return {"count": 0}
    return {
        "count": int(values.size),
        "mean": float(values.mean()),
        "p50": float(values.quantile(0.50)),
        "p90": float(values.quantile(0.90)),
        "p95": float(values.quantile(0.95)),
        "p99": float(values.quantile(0.99)),
        "max": float(values.max()),
    }


def _stdout_summary(summary: dict[str, Any]) -> dict[str, Any]:
    overall = summary["overall"]
    return {
        "status": summary["status"],
        "output_dir": summary["output_dir"],
        "query_count": summary["counts"]["query_count"],
        "attempt_count": summary["counts"]["attempt_count"],
        "candidate_count": summary["counts"]["candidate_count"],
        "attempt_total_time_p50": overall.get("fields", {}).get("analytic_total_time_s", {}).get("p50"),
        "attempt_total_time_p95": overall.get("fields", {}).get("analytic_total_time_s", {}).get("p95"),
        "candidate_radius_count_p50": overall.get("fields", {}).get("analytic_candidate_radius_count", {}).get("p50"),
    }


def _profiles_from_bucket_mode(mode: str):
    if mode == "original_t06":
        return default_main_evaluation_profiles()
    if mode == "validation_t06":
        return validation_main_evaluation_profiles()
    raise ValueError(f"unsupported density profile bucket mode: {mode}")


def _none_or_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    out = float(value)
    return out if pd.notna(out) else None


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop collection.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
