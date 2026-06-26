from __future__ import annotations

import argparse
import csv
import json
import math
import socket
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_ROOT = PROJECT_ROOT / "2_experiment"
if str(EXPERIMENT_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT))

from forest_n3p.difficulty_calibration import parse_distance_bins  # noqa: E402
from forest_n3p.evaluation import (  # noqa: E402
    EvaluationConfig,
    planner_run_from_result,
    summarize_by_method_bucket,
)
from forest_n3p.inference import InferenceConfig, KnnSubgoalLibrary, result_to_dict, run_forest_n3p  # noqa: E402
from forest_n3p.main_evaluation import (  # noqa: E402
    MainEvaluationConfig,
    _evaluate_run_with_collision_rejection,
    _generate_grid_map,
    _run_method,
    _run_vanilla_ha,
    default_main_evaluation_profiles,
    validation_main_evaluation_profiles,
)
from forest_n3p.training_data import TrainingProfile  # noqa: E402
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint  # noqa: E402


BUCKETS = ("Easy", "Complex", "Extreme")
METHODS = ("f_n3p_knn", "vanilla_ha", "improved_ha", "lo_ha", "ss_rrt", "idb_rrt")
RAW_JSON_NAME = "local_50trial_results.json"
SUMMARY_CSV_NAME = "local_50trial_summary.csv"

Pose = tuple[float, float, float]


@dataclass(frozen=True)
class QuerySpec:
    query_id: str
    difficulty_bucket: str
    profile_name: str
    map_seed: int
    query_seed: int
    seed_index: int
    map_index: int
    query_index: int
    distance_bin_key: str
    start: Pose
    goal: Pose
    source: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    today = datetime.now(UTC).strftime("%Y%m%d")
    parser = argparse.ArgumentParser(
        description="Run a local 50-trial F-N3P KNN vs vanilla HA* comparison."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / ".pipeline" / "experiments" / f"{today}_local_50trial_fn3p_vs_vanilla_ha",
    )
    parser.add_argument("--query-count", type=int, default=50)
    parser.add_argument("--query-source", choices=("auto", "t14", "dataset", "generated"), default="auto")
    parser.add_argument("--t14-root", type=Path, default=PROJECT_ROOT / ".pipeline" / "experiments")
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=PROJECT_ROOT / "2_experiment" / "forest_n3p" / "datasets" / "t08_training_dataset",
    )
    parser.add_argument(
        "--knn-library-dir",
        type=Path,
        default=PROJECT_ROOT / "2_experiment" / "forest_n3p" / "models" / "t09_knn_library",
    )
    parser.add_argument("--seed", type=int, default=20260626)
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="original_t06")
    parser.add_argument("--distance-bins", default="8:12,12:16,16:20,20:")
    parser.add_argument("--k-neighbors", type=int, default=5)
    parser.add_argument("--teacher-timeout-s", type=float, default=2.5)
    parser.add_argument("--teacher-max-nodes", type=int, default=15_000)
    parser.add_argument("--segment-timeout-s", type=float, default=1.0)
    parser.add_argument("--segment-max-nodes", type=int, default=2_000)
    parser.add_argument("--full-fallback-timeout-s", type=float, default=2.5)
    parser.add_argument("--full-fallback-max-nodes", type=int, default=15_000)
    parser.add_argument("--commit-verified-rs-segments", action="store_true")
    parser.add_argument("--max-steps-override", type=int, default=None)
    parser.add_argument("--disable-f1", action="store_true")
    parser.add_argument("--disable-f2", action="store_true")
    parser.add_argument("--disable-f3", action="store_true")
    parser.add_argument("--progress-every", type=int, default=5)
    parser.add_argument("--source-head", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = parse_args(argv)
    if int(args.query_count) <= 0:
        raise ValueError("--query-count must be positive")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_queries, selected_queries, query_source, query_source_path = load_query_specs(args)
    map_profile_by_seed = _first_profile_by_map_seed(all_queries)
    cfg = _evaluation_config(args)
    eval_cfg = EvaluationConfig()
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    predictor = KnnSubgoalLibrary.load(args.knn_library_dir)
    predictors = {"knn": predictor}

    records_payload: list[dict[str, Any]] = []
    summary_records = []
    query_payloads: list[dict[str, Any]] = []
    maps_payload: dict[str, dict[str, Any]] = {}
    map_cache: dict[int, GridMap] = {}
    profile_lookup = _profile_lookup(args)

    for index, query in enumerate(selected_queries, start=1):
        grid_map = map_cache.get(query.map_seed)
        if grid_map is None:
            map_profile_name = map_profile_by_seed.get(query.map_seed, query.profile_name)
            profile = profile_lookup.get(map_profile_name)
            if profile is None:
                raise KeyError(f"unknown profile_name={map_profile_name!r} for map_seed={query.map_seed}")
            grid_map = _generate_grid_map(profile, query.map_seed, cfg, footprint)
            map_cache[query.map_seed] = grid_map
            maps_payload[str(query.map_seed)] = _map_to_payload(grid_map, map_profile_name)

        vanilla_run = _run_vanilla_ha(query, grid_map, footprint, cfg, reference_path_length_m=None)
        vanilla_record = _evaluate_run_with_collision_rejection(vanilla_run, grid_map, footprint, config=eval_cfg)
        reference_length = vanilla_record.path_length_m if vanilla_record.feasible else None

        for method in METHODS:
            run, record, raw_result = _run_one_method(
                method,
                query,
                grid_map,
                footprint,
                cfg,
                eval_cfg,
                args,
                predictors=predictors,
                vanilla_run=vanilla_run,
                vanilla_record=vanilla_record,
                reference_path_length_m=reference_length,
            )
            summary_records.append(record)
            records_payload.append(
                _run_payload(
                    query,
                    method,
                    record,
                    path=run.path,
                    subgoals=_subgoals_from_steps(raw_result.steps) if raw_result is not None else (),
                    fallback_events=_fallback_events_from_result(raw_result) if raw_result is not None else (),
                    raw_result=result_to_dict(raw_result) if raw_result is not None else None,
                )
            )

        query_payloads.append(_query_payload(query))
        if int(args.progress_every) > 0 and (index == 1 or index % int(args.progress_every) == 0):
            print(f"[local_50trial] {index}/{len(selected_queries)} queries finished", flush=True)

    summary_rows = _summary_rows(records_payload)
    summary_csv = output_dir / SUMMARY_CSV_NAME
    _write_dict_csv(summary_csv, summary_rows)
    raw_json = output_dir / RAW_JSON_NAME
    payload = {
        "schema_version": 1,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": str(args.source_head) if args.source_head else _source_head(),
        "command": " ".join(["python", str(Path(__file__).as_posix()), *_quote_args(raw_argv)]),
        "query_source": query_source,
        "query_source_path": str(query_source_path) if query_source_path is not None else None,
        "query_count": len(selected_queries),
        "methods": list(METHODS),
        "metrics": [
            "success_rate",
            "planning_time_s",
            "path_length",
            "path_inflation_pct",
            "mean_abs_curvature",
        ],
        "config": _json_safe(vars(args)),
        "queries": query_payloads,
        "maps": maps_payload,
        "runs": records_payload,
        "summary_by_method_bucket": summary_rows,
        "compat_summary_by_method_bucket": [asdict(item) for item in summarize_by_method_bucket(summary_records)],
        "outputs": {
            "raw_json": str(raw_json),
            "summary_csv": str(summary_csv),
        },
    }
    raw_json.write_text(json.dumps(_json_safe(payload), indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "raw_json": str(raw_json),
                "summary_csv": str(summary_csv),
                "query_count": len(selected_queries),
                "query_source": query_source,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def _run_one_method(
    method: str,
    query: QuerySpec,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    eval_cfg: EvaluationConfig,
    args: argparse.Namespace,
    *,
    predictors: dict[str, Any],
    vanilla_run: Any,
    vanilla_record: Any,
    reference_path_length_m: float | None,
) -> tuple[Any, Any, Any | None]:
    if method == "vanilla_ha":
        return vanilla_run, vanilla_record, None

    if method == "f_n3p_knn":
        raw_result = run_forest_n3p(
            grid_map,
            footprint,
            query.start,
            query.goal,
            predictors["knn"],
            config=_inference_config(args, query.query_seed),
        )
        run = planner_run_from_result(
            raw_result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={
                "profile_name": query.profile_name,
                "map_seed": query.map_seed,
                "query_seed": query.query_seed,
            },
        )
        record = _evaluate_run_with_collision_rejection(run, grid_map, footprint, config=eval_cfg)
        return run, record, raw_result

    run = _run_method(
        method,
        query,
        grid_map,
        footprint,
        cfg,
        predictors=predictors,
        reference_path_length_m=reference_path_length_m,
    )
    record = _evaluate_run_with_collision_rejection(run, grid_map, footprint, config=eval_cfg)
    return run, record, None


def load_query_specs(args: argparse.Namespace) -> tuple[tuple[QuerySpec, ...], tuple[QuerySpec, ...], str, Path | None]:
    requested = str(args.query_source)
    errors: list[str] = []

    if requested in {"auto", "t14"}:
        t14_dir = _latest_t14_query_dir(Path(args.t14_root))
        if t14_dir is not None:
            specs = _query_specs_from_t14(t14_dir / "queries.csv")
            return specs, _select_balanced(specs, int(args.query_count)), "t14", t14_dir
        errors.append(f"no t14 query manifest under {args.t14_root}")
        if requested == "t14":
            raise FileNotFoundError(errors[-1])

    if requested in {"auto", "dataset"}:
        dataset_queries = Path(args.dataset_dir) / "queries.csv"
        if dataset_queries.exists():
            specs = _query_specs_from_dataset(dataset_queries)
            return specs, _select_balanced(specs, int(args.query_count)), "dataset", dataset_queries
        errors.append(f"no dataset query manifest: {dataset_queries}")
        if requested == "dataset":
            raise FileNotFoundError(errors[-1])

    if requested in {"auto", "generated"}:
        specs = _generated_query_specs(args)
        return specs, _select_balanced(specs, int(args.query_count)), "generated", None

    raise RuntimeError("; ".join(errors) or f"unsupported query_source={requested!r}")


def _latest_t14_query_dir(root: Path) -> Path | None:
    root = Path(root)
    if not root.exists():
        return None
    candidates = [
        path
        for path in root.iterdir()
        if path.is_dir() and "t14" in path.name.lower() and (path / "queries.csv").exists()
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: item.name)[-1]


def _query_specs_from_t14(path: Path) -> tuple[QuerySpec, ...]:
    specs: list[QuerySpec] = []
    for row in _read_dict_csv(path):
        specs.append(
            QuerySpec(
                query_id=str(row["query_id"]),
                difficulty_bucket=str(row["difficulty_bucket"]),
                profile_name=str(row["profile_name"]),
                map_seed=_int_field(row, "map_seed"),
                query_seed=_int_field(row, "query_seed"),
                seed_index=_int_field(row, "seed_index", default=0),
                map_index=_int_field(row, "map_index", default=0),
                query_index=_int_field(row, "query_index", default=0),
                distance_bin_key=str(row["distance_bin_key"]),
                start=_parse_pose(row["start"]),
                goal=_parse_pose(row["goal"]),
                source=str(path),
            )
        )
    return tuple(specs)


def _query_specs_from_dataset(path: Path) -> tuple[QuerySpec, ...]:
    specs: list[QuerySpec] = []
    for row in _read_dict_csv(path):
        global_query_id = _int_field(row, "global_query_id")
        specs.append(
            QuerySpec(
                query_id=f"dataset_g{global_query_id:06d}",
                difficulty_bucket=str(row["difficulty_bucket"]),
                profile_name=str(row["profile_name"]),
                map_seed=_int_field(row, "map_seed"),
                query_seed=_int_field(row, "query_seed"),
                seed_index=0,
                map_index=_int_field(row, "map_id", default=0),
                query_index=_int_field(row, "query_id", default=0),
                distance_bin_key=str(row["distance_bin_key"]),
                start=_parse_pose(row["start"]),
                goal=_parse_pose(row["goal"]),
                source=str(path),
            )
        )
    return tuple(specs)


def _generated_query_specs(args: argparse.Namespace) -> tuple[QuerySpec, ...]:
    from forest_n3p.main_evaluation import build_query_set

    per_bucket = int(math.ceil(int(args.query_count) / float(len(BUCKETS))))
    cfg = MainEvaluationConfig(
        seed=int(args.seed),
        queries_per_bucket=per_bucket,
        seed_count=1,
        queries_per_map=5,
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        distance_bins=parse_distance_bins(str(args.distance_bins)),
        enforce_t14_scale=False,
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
    )
    return tuple(
        QuerySpec(
            query_id=query.query_id,
            difficulty_bucket=query.difficulty_bucket,
            profile_name=query.profile_name,
            map_seed=query.map_seed,
            query_seed=query.query_seed,
            seed_index=query.seed_index,
            map_index=query.map_index,
            query_index=query.query_index,
            distance_bin_key=query.distance_bin_key,
            start=query.start,
            goal=query.goal,
            source="generated",
        )
        for query in build_query_set(cfg)
    )


def _select_balanced(specs: Sequence[QuerySpec], total: int) -> tuple[QuerySpec, ...]:
    by_bucket = {bucket: [item for item in specs if item.difficulty_bucket == bucket] for bucket in BUCKETS}
    base = int(total) // len(BUCKETS)
    remainder = int(total) % len(BUCKETS)
    selected: list[QuerySpec] = []
    selected_ids: set[str] = set()
    for bucket_index, bucket in enumerate(BUCKETS):
        target = base + (1 if bucket_index < remainder else 0)
        picks = _pick_evenly(by_bucket[bucket], target)
        selected.extend(picks)
        selected_ids.update(item.query_id for item in picks)

    if len(selected) < int(total):
        for item in specs:
            if item.query_id in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(item.query_id)
            if len(selected) >= int(total):
                break
    if len(selected) < int(total):
        raise RuntimeError(f"only selected {len(selected)} queries from {len(specs)} available rows")
    return tuple(selected[: int(total)])


def _pick_evenly(items: Sequence[QuerySpec], target: int) -> tuple[QuerySpec, ...]:
    if int(target) <= 0:
        return ()
    if len(items) <= int(target):
        return tuple(items)
    raw = np.linspace(0, len(items) - 1, int(target))
    indices: list[int] = []
    for value in raw:
        index = int(round(float(value)))
        if index not in indices:
            indices.append(index)
    cursor = 0
    while len(indices) < int(target):
        if cursor not in indices:
            indices.append(cursor)
        cursor += 1
    return tuple(items[index] for index in sorted(indices[: int(target)]))


def _evaluation_config(args: argparse.Namespace) -> MainEvaluationConfig:
    return MainEvaluationConfig(
        seed=int(args.seed),
        queries_per_bucket=1,
        seed_count=1,
        queries_per_map=1,
        methods=METHODS,
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        distance_bins=parse_distance_bins(str(args.distance_bins)),
        knn_library_dir=Path(args.knn_library_dir),
        teacher_timeout_s=float(args.teacher_timeout_s),
        teacher_max_nodes=int(args.teacher_max_nodes),
        segment_timeout_s=float(args.segment_timeout_s),
        segment_max_nodes=int(args.segment_max_nodes),
        full_fallback_timeout_s=float(args.full_fallback_timeout_s),
        full_fallback_max_nodes=int(args.full_fallback_max_nodes),
        k_neighbors=int(args.k_neighbors),
        commit_verified_rs_segments=bool(args.commit_verified_rs_segments),
        max_steps_override=args.max_steps_override,
        enable_f1=not bool(args.disable_f1),
        enable_f2=not bool(args.disable_f2),
        enable_f3=not bool(args.disable_f3),
        prediction_noise_sigma_m=0.0,
        prediction_noise_seed=int(args.seed),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
        bootstrap_resamples=500,
    )


def _inference_config(args: argparse.Namespace, query_seed: int) -> InferenceConfig:
    return InferenceConfig(
        k_neighbors=int(args.k_neighbors),
        segment_timeout_s=float(args.segment_timeout_s),
        segment_max_nodes=int(args.segment_max_nodes),
        full_fallback_timeout_s=float(args.full_fallback_timeout_s),
        full_fallback_max_nodes=int(args.full_fallback_max_nodes),
        commit_verified_rs_segments=bool(args.commit_verified_rs_segments),
        max_steps_override=args.max_steps_override,
        enable_f1=not bool(args.disable_f1),
        enable_f2=not bool(args.disable_f2),
        enable_f3=not bool(args.disable_f3),
        prediction_noise_sigma_m=0.0,
        prediction_noise_seed=int(args.seed) + int(query_seed),
    )


def _profiles_from_bucket_mode(mode: str) -> tuple[TrainingProfile, ...]:
    if mode == "original_t06":
        return default_main_evaluation_profiles()
    if mode == "validation_t06":
        return validation_main_evaluation_profiles()
    raise ValueError(f"unsupported density profile bucket mode: {mode}")


def _profile_lookup(args: argparse.Namespace) -> dict[str, TrainingProfile]:
    profiles: dict[str, TrainingProfile] = {}
    for profile in (*default_main_evaluation_profiles(), *validation_main_evaluation_profiles()):
        profiles.setdefault(profile.name, profile)
    dataset_summary = Path(args.dataset_dir) / "summary.json"
    if dataset_summary.exists():
        payload = json.loads(dataset_summary.read_text(encoding="utf-8"))
        for item in payload.get("config", {}).get("profiles", ()):
            profile = TrainingProfile(
                name=str(item["name"]),
                difficulty_bucket=str(item["difficulty_bucket"]),
                trunk_count=int(item["trunk_count"]),
                trunk_gap_m=float(item["trunk_gap_m"]),
                trunk_gap_jitter=float(item.get("trunk_gap_jitter", 0.25)),
                bush_cluster_count=int(item.get("bush_cluster_count", 0)),
            )
            profiles.setdefault(profile.name, profile)
    return profiles


def _run_payload(
    query: QuerySpec,
    method: str,
    record: Any,
    *,
    path: Iterable[Pose],
    subgoals: Iterable[Pose],
    fallback_events: Iterable[dict[str, Any]],
    raw_result: dict[str, Any] | None,
) -> dict[str, Any]:
    path_tuple = tuple(path)
    subgoal_tuple = tuple(subgoals)
    fallback = {
        "level": _fallback_level(record.fallback_f1_count, record.fallback_f2_count, record.fallback_f3_count),
        "triggered": bool(record.fallback_triggered),
        "f1_count": int(record.fallback_f1_count),
        "f2_count": int(record.fallback_f2_count),
        "f3_count": int(record.fallback_f3_count),
        "events": list(fallback_events),
    }
    return {
        "query_id": query.query_id,
        "method": method,
        "difficulty_bucket": query.difficulty_bucket,
        "distance_bin_key": query.distance_bin_key,
        "profile_name": query.profile_name,
        "map_seed": int(query.map_seed),
        "query_seed": int(query.query_seed),
        "start": list(query.start),
        "goal": list(query.goal),
        "status": {
            "success": bool(record.success),
            "feasible": bool(record.feasible),
            "collision_violation_count": int(record.collision_violation_count),
            "failure_reason": record.failure_reason,
        },
        "metrics": {
            "success_rate": 100.0 if bool(record.feasible) else 0.0,
            "planning_time_s": _finite_or_none(record.total_time_s),
            "path_length": _finite_or_none(record.path_length_m),
            "path_inflation_pct": _path_inflation_pct(method, record),
            "mean_abs_curvature": _finite_or_none(record.mean_abs_curvature),
        },
        "path": [list(pose) for pose in path_tuple],
        "path_pose_count": len(path_tuple),
        "subgoals": [list(pose) for pose in subgoal_tuple] if method == "f_n3p_knn" else [],
        "fallback": fallback if method == "f_n3p_knn" else _empty_fallback(),
        "raw_fn3p_result": raw_result,
    }


def _empty_fallback() -> dict[str, Any]:
    return {
        "level": "Primary",
        "triggered": False,
        "f1_count": 0,
        "f2_count": 0,
        "f3_count": 0,
        "events": [],
    }


def _subgoals_from_steps(steps: Iterable[Any]) -> tuple[Pose, ...]:
    out: list[Pose] = []
    for step in steps:
        if getattr(step, "neighbor_rank", None) is None:
            continue
        if str(getattr(step, "mode", "")).startswith("f"):
            continue
        out.append(_clean_pose(getattr(step, "target_pose")))
    return tuple(out)


def _fallback_events_from_result(result: Any) -> tuple[dict[str, Any], ...]:
    events: list[dict[str, Any]] = []
    for step in getattr(result, "steps", ()):
        mode = str(getattr(step, "mode", ""))
        neighbor_rank = getattr(step, "neighbor_rank", None)
        if neighbor_rank is not None and int(neighbor_rank) > 1:
            level = "F1"
        elif mode.startswith("f2_"):
            level = "F2"
        elif mode == "f3_full_query":
            level = "F3"
        else:
            continue
        events.append(
            {
                "level": level,
                "step_index": int(getattr(step, "step_index", -1)),
                "mode": mode,
                "target_pose": list(_clean_pose(getattr(step, "target_pose"))),
                "neighbor_rank": None if neighbor_rank is None else int(neighbor_rank),
                "segment_success": bool(getattr(step, "segment_success", False)),
                "segment_failure_reason": getattr(step, "segment_failure_reason", None),
            }
        )
    return tuple(events)


def _summary_rows(runs: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bucket in BUCKETS:
        for method in METHODS:
            group = [run for run in runs if run["difficulty_bucket"] == bucket and run["method"] == method]
            row = {
                "difficulty_bucket": bucket,
                "method": method,
                "count": len(group),
                **_metric_stats(group, "success_rate", precision=1, suffix="_pct"),
                **_metric_stats(group, "planning_time_s", precision=3),
                "planning_time_s_median": _percentile(_metric_values(group, "planning_time_s"), 50.0),
                "planning_time_s_p95": _percentile(_metric_values(group, "planning_time_s"), 95.0),
                **_metric_stats(group, "path_length", precision=3, suffix="_m"),
                **_metric_stats(group, "path_inflation_pct", precision=2),
                **_metric_stats(group, "mean_abs_curvature", precision=4),
            }
            if method == "f_n3p_knn":
                row.update(_fallback_distribution(group))
            rows.append(row)
    return rows


def _metric_stats(
    group: Sequence[dict[str, Any]],
    metric: str,
    *,
    precision: int,
    suffix: str = "",
) -> dict[str, Any]:
    values = _metric_values(group, metric)
    mean_value = _mean(values)
    std_value = _std(values)
    key = f"{metric}{suffix}"
    return {
        f"{key}_mean": mean_value,
        f"{key}_std": std_value,
        f"{key}_mean_std": _format_mean_std(mean_value, std_value, precision=precision),
    }


def _fallback_distribution(group: Sequence[dict[str, Any]]) -> dict[str, Any]:
    count = len(group)
    levels = ("Primary", "F1", "F2", "F3")
    out: dict[str, Any] = {}
    for level in levels:
        value = sum(1 for run in group if run["fallback"]["level"] == level)
        out[f"fallback_{level.lower()}_pct"] = None if count <= 0 else 100.0 * float(value) / float(count)
    return out


def _map_to_payload(grid_map: GridMap, profile_name: str) -> dict[str, Any]:
    grid = np.asarray(grid_map.data, dtype=np.uint8)
    return {
        "profile_name": profile_name,
        "resolution_m": float(grid_map.resolution),
        "origin": [float(grid_map.origin[0]), float(grid_map.origin[1])],
        "shape": [int(grid.shape[0]), int(grid.shape[1])],
        "obstacle_ratio": float(np.mean(grid > 0)),
        "occupancy_rle": _rle_encode(grid),
    }


def _rle_encode(grid: np.ndarray) -> list[list[int]]:
    flat = np.asarray(grid, dtype=np.uint8).reshape(-1)
    if flat.size == 0:
        return []
    out: list[list[int]] = []
    current = int(flat[0])
    count = 1
    for value in flat[1:]:
        v = int(value)
        if v == current:
            count += 1
            continue
        out.append([current, count])
        current = v
        count = 1
    out.append([current, count])
    return out


def _query_payload(query: QuerySpec) -> dict[str, Any]:
    return {
        "query_id": query.query_id,
        "difficulty_bucket": query.difficulty_bucket,
        "profile_name": query.profile_name,
        "map_key": str(query.map_seed),
        "map_seed": int(query.map_seed),
        "query_seed": int(query.query_seed),
        "distance_bin_key": query.distance_bin_key,
        "start": list(query.start),
        "goal": list(query.goal),
        "source": query.source,
    }


def _first_profile_by_map_seed(specs: Sequence[QuerySpec]) -> dict[int, str]:
    out: dict[int, str] = {}
    for query in specs:
        out.setdefault(int(query.map_seed), query.profile_name)
    return out


def _read_dict_csv(path: Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_dict_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(value) for key, value in row.items()})


def _csv_value(value: Any) -> Any:
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def _parse_pose(raw: Any) -> Pose:
    value = json.loads(raw) if isinstance(raw, str) else raw
    if len(value) != 3:
        raise ValueError(f"pose must have exactly three values: {raw!r}")
    return (float(value[0]), float(value[1]), float(value[2]))


def _clean_pose(raw: Any) -> Pose:
    value = tuple(float(v) for v in raw)
    if len(value) != 3:
        raise ValueError(f"pose must have exactly three values: {raw!r}")
    return value  # type: ignore[return-value]


def _int_field(row: dict[str, str], key: str, *, default: int | None = None) -> int:
    value = row.get(key)
    if value is None or value == "":
        if default is None:
            raise KeyError(key)
        return int(default)
    return int(value)


def _fallback_level(f1_count: int, f2_count: int, f3_count: int) -> str:
    if int(f3_count) > 0:
        return "F3"
    if int(f2_count) > 0:
        return "F2"
    if int(f1_count) > 0:
        return "F1"
    return "Primary"


def _path_inflation_pct(method: str, record: Any) -> float | None:
    if method == "vanilla_ha":
        return 0.0 if bool(record.feasible) and record.path_length_m is not None else None
    ratio = record.path_inflation_ratio
    if ratio is None:
        return None
    value = float(ratio)
    if not math.isfinite(value):
        return None
    return 100.0 * value


def _metric_values(group: Sequence[dict[str, Any]], metric: str) -> list[float]:
    values: list[float] = []
    for run in group:
        value = run["metrics"].get(metric)
        if value is None:
            continue
        number = float(value)
        if math.isfinite(number):
            values.append(number)
    return values


def _mean(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return float(np.mean(np.asarray(values, dtype=np.float64)))


def _std(values: Sequence[float]) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return 0.0
    return float(np.std(np.asarray(values, dtype=np.float64), ddof=1))


def _percentile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.percentile(np.asarray(values, dtype=np.float64), float(q)))


def _format_mean_std(mean_value: float | None, std_value: float | None, *, precision: int) -> str:
    if mean_value is None or std_value is None:
        return ""
    return f"{mean_value:.{precision}f}±{std_value:.{precision}f}"


def _finite_or_none(value: Any) -> float | None:
    if value is None:
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], cwd=PROJECT_ROOT, text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance must not stop the local runner.
        return "unknown"


def _quote_args(argv: list[str] | None) -> list[str]:
    return [] if argv is None else [str(item) for item in argv]


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, tuple):
        return [_json_safe(value) for value in obj]
    if isinstance(obj, list):
        return [_json_safe(value) for value in obj]
    if isinstance(obj, dict):
        return {str(key): _json_safe(value) for key, value in obj.items()}
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


if __name__ == "__main__":
    raise SystemExit(main())
