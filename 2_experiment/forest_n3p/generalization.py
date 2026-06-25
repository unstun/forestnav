from __future__ import annotations

import csv
import json
import math
import socket
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from forest_n3p.difficulty_calibration import DistanceBin, parse_distance_bins, sample_query_in_distance_bin
from forest_n3p.evaluation import (
    EvaluationConfig,
    EvaluationRecord,
    EvaluationRun,
    bootstrap_success_rate_difference,
    evaluate_run,
    paired_wilcoxon_time,
    summarize_by_method_bucket,
    write_evaluation_outputs,
)
from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _evaluate_run_with_collision_rejection,
    _generate_grid_map,
    _load_predictors,
    _run_method,
    _run_vanilla_ha,
    _stat_pairs,
    preflight_main_evaluation,
    validation_main_evaluation_profiles,
)
from forest_n3p.maps.pgm import load_pgm_yaml_map, load_ros_map_yaml
from forest_n3p.training_data import TrainingProfile
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint


@dataclass(frozen=True)
class GeneralizationConfig:
    seed: int = 20260623
    ood_queries_per_bucket: int = 20
    seed_count: int = 2
    queries_per_map: int = 5
    realmap_queries_per_map: int = 10
    include_realmap_canonical_query: bool = True
    width_cells: int = 300
    height_cells: int = 300
    resolution_m: float = 0.1
    max_query_sample_attempts: int = 800
    methods: tuple[str, ...] = ("vanilla_ha", "f_n3p_knn")
    ood_profiles: tuple[TrainingProfile, ...] = field(default_factory=lambda: default_ood_profiles())
    distance_bins: tuple[DistanceBin, ...] = field(default_factory=lambda: parse_distance_bins("8:12,12:16,16:20,20:"))
    realmap_distance_bins: tuple[DistanceBin, ...] = field(default_factory=lambda: parse_distance_bins("4:8,8:12,12:16,16:20,20:"))
    realmap_manifest_path: Path = Path("2_experiment/forest_n3p/assets/realmaps/manifest.json")
    contract_path: Path = Path(".pipeline/contracts/v9-forest-n3p.md")
    knn_library_dir: Path = Path("2_experiment/forest_n3p/models/t09_knn_library")
    knn_dataset_dir: Path = Path("2_experiment/forest_n3p/datasets/t08_training_dataset")
    knn_feature_indices: tuple[int, ...] | None = None
    teacher_timeout_s: float = 2.5
    teacher_max_nodes: int = 15_000
    segment_timeout_s: float = 1.0
    segment_max_nodes: int = 2_000
    full_fallback_timeout_s: float = 2.5
    full_fallback_max_nodes: int = 15_000
    k_neighbors: int = 20
    commit_verified_rs_segments: bool = True
    max_steps_override: int | None = None
    enable_f1: bool = True
    enable_f2: bool = True
    enable_f3: bool = True
    prediction_noise_sigma_m: float = 0.0
    prediction_noise_seed: int = 20260623
    bootstrap_resamples: int = 1_000
    bootstrap_seed: int = 20260623

    def __post_init__(self) -> None:
        if int(self.ood_queries_per_bucket) <= 0:
            raise ValueError("ood_queries_per_bucket must be positive")
        if int(self.seed_count) <= 0:
            raise ValueError("seed_count must be positive")
        if int(self.queries_per_map) <= 0:
            raise ValueError("queries_per_map must be positive")
        if int(self.realmap_queries_per_map) <= 0:
            raise ValueError("realmap_queries_per_map must be positive")
        if not self.methods:
            raise ValueError("methods must not be empty")
        if not self.ood_profiles:
            raise ValueError("ood_profiles must not be empty")
        if not self.distance_bins:
            raise ValueError("distance_bins must not be empty")
        if not self.realmap_distance_bins:
            raise ValueError("realmap_distance_bins must not be empty")
        if int(self.k_neighbors) <= 0:
            raise ValueError("k_neighbors must be positive")
        if self.max_steps_override is not None and int(self.max_steps_override) <= 0:
            raise ValueError("max_steps_override must be positive when set")
        if float(self.prediction_noise_sigma_m) < 0.0:
            raise ValueError("prediction_noise_sigma_m must be non-negative")


@dataclass(frozen=True)
class GeneralizationQuery:
    query_id: str
    split: str
    difficulty_bucket: str
    profile_name: str
    map_id: str
    map_key: str
    map_seed: int
    query_seed: int
    seed_index: int
    map_index: int
    query_index: int
    distance_bin_key: str
    start: tuple[float, float, float]
    goal: tuple[float, float, float]


@dataclass(frozen=True)
class GeneralizationRun:
    output_dir: Path
    records: tuple[EvaluationRecord, ...]
    queries: tuple[GeneralizationQuery, ...]
    verdict: dict[str, Any]
    output_paths: dict[str, Path]


def default_ood_profiles() -> tuple[TrainingProfile, ...]:
    return (
        TrainingProfile("ood_sparse_dneg01", "OOD-Sparse", trunk_count=25, trunk_gap_m=1.55, trunk_gap_jitter=0.18),
        TrainingProfile("ood_dense_d08", "OOD-Dense", trunk_count=160, trunk_gap_m=0.75, trunk_gap_jitter=0.27),
    )


def run_generalization_evaluation(
    output_dir: str | Path,
    *,
    config: GeneralizationConfig | None = None,
    source_head: str = "unknown",
    command: str = "unknown",
) -> GeneralizationRun:
    cfg = config or GeneralizationConfig()
    main_cfg = _main_config(cfg)
    preflight = preflight_main_evaluation(main_cfg)
    if not preflight.ok_to_run:
        raise RuntimeError("T16 preflight failed:\n- " + "\n- ".join(preflight.blocking_issues))

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    queries, maps = build_generalization_queries(cfg, footprint=footprint)
    predictors = _load_predictors(main_cfg, preflight.available_methods)
    eval_cfg = EvaluationConfig(
        bootstrap_resamples=int(cfg.bootstrap_resamples),
        bootstrap_seed=int(cfg.bootstrap_seed),
    )

    records: list[EvaluationRecord] = []
    for query in queries:
        grid_map = maps[query.map_key]
        vanilla_record: EvaluationRecord | None = None
        if "vanilla_ha" in preflight.available_methods:
            vanilla_record = _run_and_record(
                "vanilla_ha",
                query,
                grid_map,
                footprint,
                main_cfg,
                predictors=predictors,
                reference_path_length_m=None,
                eval_cfg=eval_cfg,
            )
            records.append(vanilla_record)

        reference_length = vanilla_record.path_length_m if vanilla_record is not None and vanilla_record.feasible else None
        for method in preflight.available_methods:
            if method == "vanilla_ha":
                continue
            records.append(
                _run_and_record(
                    method,
                    query,
                    grid_map,
                    footprint,
                    main_cfg,
                    predictors=predictors,
                    reference_path_length_m=reference_length,
                    eval_cfg=eval_cfg,
                )
            )

    stat_pairs = _stat_pairs(preflight.available_methods)
    paired_tests = tuple(paired_wilcoxon_time(records, a, b) for a, b in stat_pairs)
    sr_cis = tuple(bootstrap_success_rate_difference(records, a, b, config=eval_cfg) for a, b in stat_pairs)
    paths = write_evaluation_outputs(records, out_dir, paired_time_tests=paired_tests, success_rate_cis=sr_cis)
    paths["queries_csv"] = _write_query_manifest(out_dir / "queries.csv", queries)
    paths["preflight_json"] = _write_json(
        out_dir / "preflight.json",
        {
            "ok_to_run": preflight.ok_to_run,
            "blocking_issues": list(preflight.blocking_issues),
            "warnings": list(preflight.warnings),
            "available_methods": list(preflight.available_methods),
            "unavailable_methods": dict(preflight.unavailable_methods),
        },
    )
    paths["run_config_json"] = _write_json(
        out_dir / "run_config.json",
        {
            "created_at_utc": datetime.now(UTC).isoformat(),
            "execution_host": socket.gethostname(),
            "source_head": source_head,
            "command": command,
            "config": _json_safe(asdict(cfg)),
        },
    )
    verdict = build_generalization_verdict(records, queries, cfg, available_methods=preflight.available_methods)
    paths["verdict_json"] = _write_json(out_dir / "verdict.json", verdict)
    paths["report_md"] = _write_report(out_dir / "report.md", cfg, verdict, paths)
    return GeneralizationRun(
        output_dir=out_dir,
        records=tuple(records),
        queries=queries,
        verdict=verdict,
        output_paths=paths,
    )


def build_generalization_queries(
    config: GeneralizationConfig,
    *,
    footprint: TwoCircleFootprint | None = None,
) -> tuple[tuple[GeneralizationQuery, ...], dict[str, GridMap]]:
    cfg = config
    fp = footprint or TwoCircleFootprint.from_box(length=0.924, width=0.740)
    main_cfg = _main_config(cfg)
    maps: dict[str, GridMap] = {}
    queries: list[GeneralizationQuery] = []
    _append_ood_queries(queries, maps, cfg, main_cfg, fp)
    _append_realmap_queries(queries, maps, cfg, fp)
    return tuple(queries), maps


def build_generalization_verdict(
    records: Sequence[EvaluationRecord],
    queries: Sequence[GeneralizationQuery],
    cfg: GeneralizationConfig,
    *,
    available_methods: Sequence[str],
) -> dict[str, Any]:
    summaries = {(item.method, item.difficulty_bucket): asdict(item) for item in summarize_by_method_bucket(records)}
    ood_buckets = sorted({query.difficulty_bucket for query in queries if query.split == "ood_density"})
    ood_verdicts = {
        bucket: _bucket_success_drop_verdict(summaries, bucket, max_drop_pp=5.0)
        for bucket in ood_buckets
    }
    realmap_aggregate = _bucket_time_reduction_verdict(summaries, "RealMap", min_reduction=0.20)
    realmap_by_map: dict[str, dict[str, Any]] = {}
    for map_id in sorted({query.map_id for query in queries if query.split == "realmap"}):
        subset = [row for row in records if row.metadata.get("map_id") == map_id]
        map_summaries = {
            (item.method, item.difficulty_bucket): asdict(item)
            for item in summarize_by_method_bucket(subset)
        }
        realmap_by_map[map_id] = _bucket_time_reduction_verdict(map_summaries, "RealMap", min_reduction=0.20)

    collision_total = sum(int(row.collision_violation_count) for row in records)
    method_exception_total = sum(
        1 for row in records if row.failure_reason is not None and "exception" in str(row.failure_reason).lower()
    )
    scale = _scale_report(queries, cfg)
    criteria = {
        "failure_criterion_2_ood_success_drop_le_5pp": bool(
            ood_verdicts and all(item["status"] == "pass" for item in ood_verdicts.values())
        ),
        "failure_criterion_4_realmap_time_reduction_ge_20pct": bool(realmap_aggregate["status"] == "pass"),
        "collision_violations_zero": int(collision_total) == 0,
        "method_exceptions_zero": int(method_exception_total) == 0,
    }
    formal_ready = bool(scale["formal_scale_satisfied"] and "f_n3p_knn" in available_methods and "vanilla_ha" in available_methods)
    acceptance = bool(formal_ready and all(criteria.values()))
    status = "formal_pass" if acceptance else ("formal_fail" if formal_ready else "candidate_or_framework")
    return {
        "status": status,
        "formal_acceptance": acceptance,
        "record_count": len(records),
        "query_count": len(queries),
        "method_count": len(tuple(available_methods)),
        "available_methods": list(available_methods),
        "query_count_by_split": _count_by_attr(queries, "split"),
        "query_count_by_bucket": _count_by_attr(queries, "difficulty_bucket"),
        "query_count_by_map": _count_by_attr(queries, "map_id"),
        "collision_violation_total": collision_total,
        "method_exception_total": method_exception_total,
        "scale": scale,
        "criteria": criteria,
        "ood_bucket_verdicts": ood_verdicts,
        "realmap_aggregate_verdict": realmap_aggregate,
        "realmap_by_map_verdicts": realmap_by_map,
        "contract_failure_thresholds": {
            "criterion_2_ood_success_drop_pp_max": 5.0,
            "criterion_4_realmap_time_reduction_min": 0.20,
        },
        "note": (
            "candidate_or_framework means the runner and output schema are valid, but the run is below "
            "the configured formal scale. Use >=100 OOD queries per bucket and >=5 seeds for paper-grade OOD evidence."
        ),
    }


def _run_and_record(
    method: str,
    query: GeneralizationQuery,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    *,
    predictors: dict[str, Any],
    reference_path_length_m: float | None,
    eval_cfg: EvaluationConfig,
) -> EvaluationRecord:
    try:
        if method == "vanilla_ha":
            run = _run_vanilla_ha(query, grid_map, footprint, cfg, reference_path_length_m=reference_path_length_m)
        else:
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
    except Exception as exc:  # noqa: BLE001 - one bad query should become an auditable row.
        run = EvaluationRun(
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            success=False,
            path=(),
            total_time_s=math.nan,
            total_expansions=0,
            reference_path_length_m=reference_path_length_m,
            failure_reason=f"exception:{type(exc).__name__}:{exc}",
            metadata=_query_metadata(query),
        )
        record = evaluate_run(run, grid_map, footprint, config=eval_cfg)
    return replace(record, metadata={**record.metadata, **_query_metadata(query)})


def _append_ood_queries(
    queries: list[GeneralizationQuery],
    maps: dict[str, GridMap],
    cfg: GeneralizationConfig,
    main_cfg: MainEvaluationConfig,
    footprint: TwoCircleFootprint,
) -> None:
    buckets = _profiles_by_bucket(cfg.ood_profiles)
    for bucket_index, bucket in enumerate(sorted(buckets)):
        bucket_profiles = buckets[bucket]
        target = int(cfg.ood_queries_per_bucket)
        generated = 0
        attempts = 0
        per_seed = int(math.ceil(float(target) / float(cfg.seed_count)))
        max_attempts = max(target * 20, 20)
        while generated < target and attempts < max_attempts:
            seed_index = min(generated // per_seed, int(cfg.seed_count) - 1)
            local_index = generated % per_seed
            profile = bucket_profiles[generated % len(bucket_profiles)]
            map_index = local_index // int(cfg.queries_per_map)
            query_index = local_index % int(cfg.queries_per_map)
            map_seed = int(cfg.seed) + 300_000 + 100_000 * bucket_index + 10_000 * seed_index + attempts
            query_seed = int(cfg.seed) + 310_000 + 100_000 * bucket_index + 10_000 * seed_index + attempts * 100 + generated
            map_key = f"ood:{bucket}:{map_seed}"
            attempts += 1
            grid_map = maps.get(map_key)
            if grid_map is None:
                try:
                    grid_map = _generate_grid_map(profile, map_seed, main_cfg, footprint)
                except RuntimeError:
                    continue
                maps[map_key] = grid_map
            distance_bin = cfg.distance_bins[generated % len(cfg.distance_bins)]
            try:
                start, goal = sample_query_in_distance_bin(
                    grid_map,
                    footprint,
                    rng=np.random.default_rng(query_seed),
                    distance_bin=distance_bin,
                    max_attempts=int(cfg.max_query_sample_attempts),
                )
            except RuntimeError:
                continue
            safe_bucket = bucket.lower().replace("-", "_")
            queries.append(
                GeneralizationQuery(
                    query_id=f"{safe_bucket}_s{seed_index:02d}_q{generated:04d}",
                    split="ood_density",
                    difficulty_bucket=bucket,
                    profile_name=profile.name,
                    map_id=profile.name,
                    map_key=map_key,
                    map_seed=int(map_seed),
                    query_seed=int(query_seed),
                    seed_index=int(seed_index),
                    map_index=int(map_index),
                    query_index=int(query_index),
                    distance_bin_key=distance_bin.key,
                    start=_clean_pose(start),
                    goal=_clean_pose(goal),
                )
            )
            generated += 1
        if generated < target:
            raise RuntimeError(f"failed to generate {target} OOD queries for bucket {bucket}; got {generated}")


def _append_realmap_queries(
    queries: list[GeneralizationQuery],
    maps: dict[str, GridMap],
    cfg: GeneralizationConfig,
    footprint: TwoCircleFootprint,
) -> None:
    manifest = _read_realmap_manifest(cfg.realmap_manifest_path)
    for map_index, item in enumerate(manifest["maps"]):
        map_id = str(item["id"])
        yaml_path = Path(str(item["yaml"]))
        if not yaml_path.is_absolute():
            yaml_path = _repo_root() / yaml_path
        start_xy = _xy_tuple(item["start_xy"])
        goal_xy = _xy_tuple(item["goal_xy"])
        meta = load_ros_map_yaml(yaml_path)
        spec = load_pgm_yaml_map(yaml_path, start_xy, goal_xy, name=map_id, unknown_as_occupied=True)
        grid_map = GridMap(spec.obstacle_grid(), resolution=float(meta.resolution), origin=(float(meta.origin[0]), float(meta.origin[1])))
        map_key = f"realmap:{map_id}"
        maps[map_key] = grid_map

        generated = 0
        if cfg.include_realmap_canonical_query:
            start, goal = _poses_from_grid_pair(grid_map, start_xy, goal_xy)
            queries.append(
                _realmap_query(
                    cfg,
                    map_id=map_id,
                    map_key=map_key,
                    map_index=map_index,
                    query_index=generated,
                    distance_bin_key="manifest_canonical",
                    start=start,
                    goal=goal,
                )
            )
            generated += 1

        attempts = 0
        target = int(cfg.realmap_queries_per_map)
        max_attempts = max(target * 30, 30)
        while generated < target and attempts < max_attempts:
            distance_bin = cfg.realmap_distance_bins[generated % len(cfg.realmap_distance_bins)]
            query_seed = int(cfg.seed) + 710_000 + map_index * 10_000 + generated * 1_000 + attempts
            attempts += 1
            try:
                start, goal = sample_query_in_distance_bin(
                    grid_map,
                    footprint,
                    rng=np.random.default_rng(query_seed),
                    distance_bin=distance_bin,
                    max_attempts=int(cfg.max_query_sample_attempts),
                )
            except RuntimeError:
                continue
            queries.append(
                _realmap_query(
                    cfg,
                    map_id=map_id,
                    map_key=map_key,
                    map_index=map_index,
                    query_index=generated,
                    distance_bin_key=distance_bin.key,
                    start=start,
                    goal=goal,
                    query_seed=query_seed,
                )
            )
            generated += 1
        if generated < target:
            raise RuntimeError(f"failed to generate {target} realmap queries for {map_id}; got {generated}")


def _realmap_query(
    cfg: GeneralizationConfig,
    *,
    map_id: str,
    map_key: str,
    map_index: int,
    query_index: int,
    distance_bin_key: str,
    start: tuple[float, float, float],
    goal: tuple[float, float, float],
    query_seed: int | None = None,
) -> GeneralizationQuery:
    seed = int(cfg.seed) + 700_000 + int(map_index) * 10_000 + int(query_index) if query_seed is None else int(query_seed)
    return GeneralizationQuery(
        query_id=f"realmap_{map_id}_q{query_index:04d}",
        split="realmap",
        difficulty_bucket="RealMap",
        profile_name=map_id,
        map_id=map_id,
        map_key=map_key,
        map_seed=int(cfg.seed) + 600_000 + int(map_index),
        query_seed=seed,
        seed_index=0,
        map_index=int(map_index),
        query_index=int(query_index),
        distance_bin_key=distance_bin_key,
        start=_clean_pose(start),
        goal=_clean_pose(goal),
    )


def _main_config(cfg: GeneralizationConfig) -> MainEvaluationConfig:
    return MainEvaluationConfig(
        seed=int(cfg.seed),
        queries_per_bucket=int(cfg.ood_queries_per_bucket),
        seed_count=int(cfg.seed_count),
        queries_per_map=int(cfg.queries_per_map),
        width_cells=int(cfg.width_cells),
        height_cells=int(cfg.height_cells),
        resolution_m=float(cfg.resolution_m),
        max_query_sample_attempts=int(cfg.max_query_sample_attempts),
        methods=tuple(cfg.methods),
        profiles=validation_main_evaluation_profiles(),
        distance_bins=tuple(cfg.distance_bins),
        knn_library_dir=cfg.knn_library_dir,
        knn_dataset_dir=cfg.knn_dataset_dir,
        knn_feature_indices=cfg.knn_feature_indices,
        contract_path=cfg.contract_path,
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
        teacher_timeout_s=float(cfg.teacher_timeout_s),
        teacher_max_nodes=int(cfg.teacher_max_nodes),
        segment_timeout_s=float(cfg.segment_timeout_s),
        segment_max_nodes=int(cfg.segment_max_nodes),
        full_fallback_timeout_s=float(cfg.full_fallback_timeout_s),
        full_fallback_max_nodes=int(cfg.full_fallback_max_nodes),
        k_neighbors=int(cfg.k_neighbors),
        commit_verified_rs_segments=bool(cfg.commit_verified_rs_segments),
        max_steps_override=cfg.max_steps_override,
        enable_f1=bool(cfg.enable_f1),
        enable_f2=bool(cfg.enable_f2),
        enable_f3=bool(cfg.enable_f3),
        prediction_noise_sigma_m=float(cfg.prediction_noise_sigma_m),
        prediction_noise_seed=int(cfg.prediction_noise_seed),
        bootstrap_resamples=int(cfg.bootstrap_resamples),
        bootstrap_seed=int(cfg.bootstrap_seed),
    )


def _bucket_success_drop_verdict(
    summaries: dict[tuple[str, str], dict[str, Any]],
    bucket: str,
    *,
    max_drop_pp: float,
) -> dict[str, Any]:
    f_row = summaries.get(("f_n3p_knn", bucket))
    base_row = summaries.get(("vanilla_ha", bucket))
    if f_row is None or base_row is None:
        return {"status": "missing", "reason": "missing f_n3p_knn or vanilla_ha summary"}
    success_drop_pp = 100.0 * (float(base_row["feasible_rate"]) - float(f_row["feasible_rate"]))
    return {
        "status": "pass" if success_drop_pp <= float(max_drop_pp) else "fail",
        "f_n3p_feasible_rate": float(f_row["feasible_rate"]),
        "vanilla_feasible_rate": float(base_row["feasible_rate"]),
        "success_drop_pp": success_drop_pp,
        "threshold_success_drop_pp_max": float(max_drop_pp),
        "count": int(f_row["count"]),
    }


def _bucket_time_reduction_verdict(
    summaries: dict[tuple[str, str], dict[str, Any]],
    bucket: str,
    *,
    min_reduction: float,
) -> dict[str, Any]:
    f_row = summaries.get(("f_n3p_knn", bucket))
    base_row = summaries.get(("vanilla_ha", bucket))
    if f_row is None or base_row is None:
        return {"status": "missing", "reason": "missing f_n3p_knn or vanilla_ha summary"}
    reduction = None
    if base_row["median_time_s"] and float(base_row["median_time_s"]) > 0.0 and f_row["median_time_s"] is not None:
        reduction = 1.0 - float(f_row["median_time_s"]) / float(base_row["median_time_s"])
    status = "pass" if reduction is not None and reduction >= float(min_reduction) else "fail"
    return {
        "status": status,
        "median_time_reduction": reduction,
        "f_n3p_median_time_s": f_row["median_time_s"],
        "vanilla_median_time_s": base_row["median_time_s"],
        "threshold_median_time_reduction_min": float(min_reduction),
        "f_n3p_feasible_rate": float(f_row["feasible_rate"]),
        "vanilla_feasible_rate": float(base_row["feasible_rate"]),
        "count": int(f_row["count"]),
    }


def _scale_report(queries: Sequence[GeneralizationQuery], cfg: GeneralizationConfig) -> dict[str, Any]:
    by_bucket = _count_by_attr([query for query in queries if query.split == "ood_density"], "difficulty_bucket")
    realmap_count = sum(1 for query in queries if query.split == "realmap")
    return {
        "ood_queries_per_bucket_config": int(cfg.ood_queries_per_bucket),
        "seed_count_config": int(cfg.seed_count),
        "realmap_queries_per_map_config": int(cfg.realmap_queries_per_map),
        "ood_query_count_by_bucket": by_bucket,
        "realmap_query_count": int(realmap_count),
        "formal_scale_satisfied": bool(
            by_bucket
            and min(by_bucket.values()) >= 100
            and int(cfg.seed_count) >= 5
            and int(realmap_count) > 0
        ),
    }


def _query_metadata(query: GeneralizationQuery) -> dict[str, Any]:
    return {
        "split": query.split,
        "profile_name": query.profile_name,
        "map_id": query.map_id,
        "map_key": query.map_key,
        "map_seed": query.map_seed,
        "query_seed": query.query_seed,
        "seed_index": query.seed_index,
        "map_index": query.map_index,
        "query_index": query.query_index,
    }


def _read_realmap_manifest(path: Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise FileNotFoundError(f"realmap manifest not found: {manifest_path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    maps = payload.get("maps")
    if not isinstance(maps, list) or not maps:
        raise ValueError(f"realmap manifest has no maps: {manifest_path}")
    return payload


def _poses_from_grid_pair(
    grid_map: GridMap,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    sx, sy = grid_map.grid_to_world(int(start_xy[0]), int(start_xy[1]))
    gx, gy = grid_map.grid_to_world(int(goal_xy[0]), int(goal_xy[1]))
    heading = math.atan2(float(gy) - float(sy), float(gx) - float(sx))
    return (float(sx), float(sy), float(heading)), (float(gx), float(gy), float(heading))


def _profiles_by_bucket(profiles: Sequence[TrainingProfile]) -> dict[str, tuple[TrainingProfile, ...]]:
    out: dict[str, list[TrainingProfile]] = {}
    for profile in profiles:
        out.setdefault(profile.difficulty_bucket, []).append(profile)
    return {key: tuple(value) for key, value in out.items()}


def _xy_tuple(value: Any) -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"expected [x, y] map coordinate, got: {value!r}")
    return int(value[0]), int(value[1])


def _write_query_manifest(path: Path, queries: Sequence[GeneralizationQuery]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(asdict(queries[0]).keys()) if queries else list(GeneralizationQuery.__dataclass_fields__.keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for query in queries:
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False) if isinstance(value, (tuple, list, dict)) else value
                    for key, value in asdict(query).items()
                }
            )
    return path


def _write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(payload), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _write_report(path: Path, cfg: GeneralizationConfig, verdict: dict[str, Any], paths: dict[str, Path]) -> Path:
    lines = [
        "# T16 泛化测试报告",
        "",
        "## 人话结论",
        "",
        f"- 本次状态: {verdict['status']}；query_count={verdict['query_count']}，record_count={verdict['record_count']}。",
        "- OOD 密度回答：训练分布外更稀/更密时，F-N3P 相对原版 HA* 的成功率跌幅是否超过 5pp。",
        "- RealMap 回答：真实 SLAM 地图上，F-N3P 相对原版 HA* 的中位时间收益是否达到 20%。",
        "- `candidate_or_framework` 表示框架和 CSV 已跑通，但规模还不是论文最终数字。",
        "",
        "## Contract 判据",
        "",
        "- 判据 ②：OOD density bucket success rate relative to original drops >5pp 记为失败。",
        "- 判据 ④：real SLAM map time benefit <20% 记为失败。",
        "",
        "## 当前判定",
        "",
        f"- criterion_2_pass: {verdict['criteria']['failure_criterion_2_ood_success_drop_le_5pp']}",
        f"- criterion_4_pass: {verdict['criteria']['failure_criterion_4_realmap_time_reduction_ge_20pct']}",
        f"- collision_violation_total: {verdict['collision_violation_total']}",
        f"- method_exception_total: {verdict['method_exception_total']}",
        "",
        "## 输出文件",
        "",
    ]
    for key, value in sorted(paths.items()):
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## 规模边界",
            "",
            f"- ood_queries_per_bucket_config: {cfg.ood_queries_per_bucket}",
            f"- seed_count_config: {cfg.seed_count}",
            f"- realmap_queries_per_map_config: {cfg.realmap_queries_per_map}",
            "- 论文最终数字建议按 `--ood-queries-per-bucket >=100 --seed-count >=5` 重跑。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _count_by_attr(items: Iterable[Any], attr: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        key = str(getattr(item, attr))
        out[key] = out.get(key, 0) + 1
    return out


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, tuple):
        return [_json_safe(value) for value in obj]
    if isinstance(obj, list):
        return [_json_safe(value) for value in obj]
    if isinstance(obj, dict):
        return {str(key): _json_safe(value) for key, value in obj.items()}
    return obj


def _clean_pose(pose: Sequence[float]) -> tuple[float, float, float]:
    if len(pose) != 3:
        raise ValueError("pose must have exactly three elements")
    return (float(pose[0]), float(pose[1]), float(pose[2]))


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]
