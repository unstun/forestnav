from __future__ import annotations

import csv
import json
import math
import socket
from dataclasses import asdict, dataclass, field
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
    planner_run_from_path_stats,
    planner_run_from_result,
    write_evaluation_outputs,
)
from forest_n3p.maps.forest import generate_forest_grid
from forest_n3p.pilot_labeling import footprint_clearance_m
from forest_n3p.training_data import TrainingDataConfig, TrainingProfile, make_forest_params
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    LOHybridAStarPlanner,
    RRTStarPlanner,
    TwoCircleFootprint,
)


OFFICIAL_T14_METHODS = (
    "f_n3p_knn",
    "vanilla_ha",
    "n3p_k1",
    "voronoi_waypoint",
    "bottleneck_waypoint",
    "improved_ha",
    "lo_ha",
    "ss_rrt",
    "idb_rrt",
)

T15_EXTRA_METHODS = ("mlp",)

IMPLEMENTED_METHODS = frozenset((*OFFICIAL_T14_METHODS, *T15_EXTRA_METHODS))

FORMAL_HUMAN_DECISIONS = {
    "D-T14-09": ("approve_original_with_justification", "revise_to_validation_cutpoints"),
    "D-T14-10": ("approve",),
    "D-T14-12": ("approve_after_rerun_passes",),
}


@dataclass(frozen=True)
class MainEvaluationConfig:
    seed: int = 20260620
    queries_per_bucket: int = 50
    seed_count: int = 5
    queries_per_map: int = 5
    width_cells: int = 300
    height_cells: int = 300
    resolution_m: float = 0.1
    max_query_sample_attempts: int = 800
    methods: tuple[str, ...] = OFFICIAL_T14_METHODS
    profiles: tuple[TrainingProfile, ...] = field(default_factory=lambda: default_main_evaluation_profiles())
    distance_bins: tuple[DistanceBin, ...] = field(default_factory=lambda: parse_distance_bins("8:12,12:16,16:20,20:"))
    knn_library_dir: Path = Path("2_experiment/forest_n3p/models/t09_knn_library")
    knn_dataset_dir: Path = Path("2_experiment/forest_n3p/datasets/t08_training_dataset")
    knn_feature_indices: tuple[int, ...] | None = None
    mlp_model_dir: Path = Path("2_experiment/forest_n3p/models/t10_mlp_subgoal")
    mlp_device: str = "cpu"
    cutpoint_supplement_path: Path = Path(".pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md")
    t06_validation_summary_path: Path = Path(
        ".pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16/summary.json"
    )
    contract_path: Path = Path(".pipeline/contracts/v9-forest-n3p.md")
    human_review_form_path: Path = Path(
        ".pipeline/experiments/20260621_t14_formal_gate_review_packet/human_review_form.md"
    )
    allow_unreviewed_cutpoints: bool = False
    allow_unresolved_human_review: bool = False
    enforce_t14_scale: bool = True
    teacher_timeout_s: float = 2.5
    teacher_max_nodes: int = 15_000
    segment_timeout_s: float = 1.0
    segment_max_nodes: int = 2_000
    full_fallback_timeout_s: float = 2.5
    full_fallback_max_nodes: int = 15_000
    k_neighbors: int = 5
    commit_verified_rs_segments: bool = False
    max_steps_override: int | None = None
    enable_f1: bool = True
    enable_f2: bool = True
    enable_f3: bool = True
    prediction_noise_sigma_m: float = 0.0
    prediction_noise_seed: int = 20260620
    idb_rrt_binary_path: Path | None = None
    idb_rrt_dynoplan_root: Path | None = None
    idb_rrt_motion_file: Path | None = None
    idb_rrt_timeout_s: float | None = None
    bootstrap_resamples: int = 5_000
    bootstrap_seed: int = 20260620

    def __post_init__(self) -> None:
        if int(self.queries_per_bucket) <= 0:
            raise ValueError("queries_per_bucket must be positive")
        if int(self.seed_count) <= 0:
            raise ValueError("seed_count must be positive")
        if int(self.queries_per_map) <= 0:
            raise ValueError("queries_per_map must be positive")
        if not self.methods:
            raise ValueError("methods must not be empty")
        if not self.profiles:
            raise ValueError("profiles must not be empty")
        if not self.distance_bins:
            raise ValueError("distance_bins must not be empty")
        if int(self.k_neighbors) <= 0:
            raise ValueError("k_neighbors must be positive")
        if self.knn_feature_indices is not None:
            if not self.knn_feature_indices:
                raise ValueError("knn_feature_indices must not be empty when set")
            if len(set(self.knn_feature_indices)) != len(self.knn_feature_indices):
                raise ValueError("knn_feature_indices must be unique")
            if any(int(index) < 0 for index in self.knn_feature_indices):
                raise ValueError("knn_feature_indices must be non-negative")
        if self.max_steps_override is not None and int(self.max_steps_override) <= 0:
            raise ValueError("max_steps_override must be positive when set")
        if float(self.prediction_noise_sigma_m) < 0.0:
            raise ValueError("prediction_noise_sigma_m must be non-negative")
        if self.idb_rrt_timeout_s is not None and float(self.idb_rrt_timeout_s) <= 0.0:
            raise ValueError("idb_rrt_timeout_s must be positive when set")


@dataclass(frozen=True)
class EvaluationQuery:
    query_id: str
    difficulty_bucket: str
    profile_name: str
    map_seed: int
    query_seed: int
    seed_index: int
    map_index: int
    query_index: int
    distance_bin_key: str
    start: tuple[float, float, float]
    goal: tuple[float, float, float]


@dataclass(frozen=True)
class PreflightReport:
    ok_to_run: bool
    blocking_issues: tuple[str, ...]
    warnings: tuple[str, ...]
    available_methods: tuple[str, ...]
    unavailable_methods: dict[str, str]
    cutpoint_supplement_reviewed: bool
    human_review_satisfied: bool
    human_review_decisions: dict[str, str]
    profile_bucket_satisfied: bool
    profile_bucket_issues: tuple[str, ...]
    t14_scale_satisfied: bool


@dataclass(frozen=True)
class MainEvaluationResult:
    output_dir: Path
    records: tuple[EvaluationRecord, ...]
    queries: tuple[EvaluationQuery, ...]
    preflight: PreflightReport
    verdict: dict[str, Any]
    output_paths: dict[str, Path]


def default_main_evaluation_profiles() -> tuple[TrainingProfile, ...]:
    return (
        TrainingProfile("easy_d00", "Easy", trunk_count=40, trunk_gap_m=1.35, trunk_gap_jitter=0.20),
        TrainingProfile("easy_d01", "Easy", trunk_count=55, trunk_gap_m=1.25, trunk_gap_jitter=0.20),
        TrainingProfile("complex_d02", "Complex", trunk_count=70, trunk_gap_m=1.15, trunk_gap_jitter=0.22),
        TrainingProfile("extreme_d03", "Extreme", trunk_count=85, trunk_gap_m=1.05, trunk_gap_jitter=0.24),
        TrainingProfile("extreme_d04", "Extreme", trunk_count=100, trunk_gap_m=0.95, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d05", "Extreme", trunk_count=115, trunk_gap_m=0.90, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d06", "Extreme", trunk_count=130, trunk_gap_m=0.85, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d07", "Extreme", trunk_count=145, trunk_gap_m=0.80, trunk_gap_jitter=0.25),
    )


def validation_main_evaluation_profiles() -> tuple[TrainingProfile, ...]:
    return (
        TrainingProfile("easy_d00", "Easy", trunk_count=40, trunk_gap_m=1.35, trunk_gap_jitter=0.20),
        TrainingProfile("easy_d01", "Easy", trunk_count=55, trunk_gap_m=1.25, trunk_gap_jitter=0.20),
        TrainingProfile("complex_d02", "Complex", trunk_count=70, trunk_gap_m=1.15, trunk_gap_jitter=0.22),
        TrainingProfile("complex_d03", "Complex", trunk_count=85, trunk_gap_m=1.05, trunk_gap_jitter=0.24),
        TrainingProfile("complex_d04", "Complex", trunk_count=100, trunk_gap_m=0.95, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d05", "Extreme", trunk_count=115, trunk_gap_m=0.90, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d06", "Extreme", trunk_count=130, trunk_gap_m=0.85, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d07", "Extreme", trunk_count=145, trunk_gap_m=0.80, trunk_gap_jitter=0.25),
    )


def preflight_main_evaluation(config: MainEvaluationConfig) -> PreflightReport:
    issues: list[str] = []
    warnings: list[str] = []
    unavailable: dict[str, str] = {}

    unknown = [method for method in config.methods if method not in IMPLEMENTED_METHODS]
    if unknown:
        issues.append(f"unknown evaluation methods: {', '.join(unknown)}")

    reviewed = _frontmatter_bool(config.cutpoint_supplement_path, "reviewed")
    if not reviewed:
        msg = f"T06 cutpoint supplement is not reviewed:true: {config.cutpoint_supplement_path}"
        if config.allow_unreviewed_cutpoints:
            warnings.append(msg)
        else:
            issues.append(msg)

    contract_status = _frontmatter_value(config.contract_path, "status")
    if contract_status != "approved":
        issues.append(f"contract status is not approved: {config.contract_path} status={contract_status!r}")

    if any(method in config.methods for method in ("f_n3p_knn", "n3p_k1")):
        missing = (
            _missing_knn_dataset_files(config.knn_dataset_dir)
            if config.knn_feature_indices is not None
            else _missing_knn_files(config.knn_library_dir)
        )
        if missing:
            root = config.knn_dataset_dir if config.knn_feature_indices is not None else config.knn_library_dir
            issues.append(f"KNN source is incomplete under {root}: {', '.join(missing)}")

    if "mlp" in config.methods:
        missing = _missing_mlp_files(config.mlp_model_dir)
        if missing:
            issues.append(f"MLP model is incomplete under {config.mlp_model_dir}: {', '.join(missing)}")

    if "idb_rrt" in config.methods:
        from forest_n3p.baselines.idb_rrt_adapter import check_idb_rrt_adapter

        idb_availability = check_idb_rrt_adapter(_idb_rrt_config(config))
        if not idb_availability.available:
            unavailable["idb_rrt"] = idb_availability.reason or "unknown iDb-RRT adapter availability failure"
            issues.append(f"idb_rrt unavailable: {unavailable['idb_rrt']}")

    human_decisions = _read_human_review_decisions(config.human_review_form_path)
    human_review_issues = _human_review_issues(human_decisions, form_path=config.human_review_form_path)
    if human_review_issues:
        msg = "T14 human review is unresolved: " + "; ".join(human_review_issues)
        if config.allow_unresolved_human_review:
            warnings.append(msg)
        else:
            issues.append(msg)

    profile_bucket_issues = _profile_bucket_issues(config, human_decisions)
    if profile_bucket_issues:
        issues.append("T14 profile bucket configuration is inconsistent: " + "; ".join(profile_bucket_issues))

    t14_scale = int(config.queries_per_bucket) >= 50 and int(config.seed_count) >= 5
    if not t14_scale:
        msg = (
            "T14 formal scale is not satisfied: "
            f"queries_per_bucket={config.queries_per_bucket}, seed_count={config.seed_count}"
        )
        if config.enforce_t14_scale:
            issues.append(msg)
        else:
            warnings.append(msg)

    available = tuple(method for method in config.methods if method in IMPLEMENTED_METHODS and method not in unavailable)
    return PreflightReport(
        ok_to_run=not issues,
        blocking_issues=tuple(issues),
        warnings=tuple(warnings),
        available_methods=available,
        unavailable_methods=unavailable,
        cutpoint_supplement_reviewed=reviewed,
        human_review_satisfied=not human_review_issues,
        human_review_decisions=human_decisions,
        profile_bucket_satisfied=not profile_bucket_issues,
        profile_bucket_issues=tuple(profile_bucket_issues),
        t14_scale_satisfied=t14_scale,
    )


def build_query_set(config: MainEvaluationConfig) -> tuple[EvaluationQuery, ...]:
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    buckets = _profiles_by_bucket(config.profiles)
    map_cache: dict[int, GridMap] = {}
    queries: list[EvaluationQuery] = []
    for bucket_index, bucket in enumerate(("Easy", "Complex", "Extreme")):
        bucket_profiles = buckets.get(bucket, ())
        if not bucket_profiles:
            raise ValueError(f"no profiles configured for bucket {bucket}")
        target = int(config.queries_per_bucket)
        generated = 0
        per_seed = int(math.ceil(float(target) / float(config.seed_count)))
        for seed_index in range(int(config.seed_count)):
            for local_index in range(per_seed):
                if generated >= target:
                    break
                profile = bucket_profiles[generated % len(bucket_profiles)]
                map_index = local_index // int(config.queries_per_map)
                query_index = local_index % int(config.queries_per_map)
                map_seed = int(config.seed) + 100_000 * bucket_index + 10_000 * seed_index + map_index
                query_seed = map_seed + 1_000 + query_index
                grid_map = map_cache.get(map_seed)
                if grid_map is None:
                    grid_map = _generate_grid_map(profile, map_seed, config, footprint)
                    map_cache[map_seed] = grid_map
                distance_bin = config.distance_bins[generated % len(config.distance_bins)]
                start, goal = sample_query_in_distance_bin(
                    grid_map,
                    footprint,
                    rng=np.random.default_rng(query_seed),
                    distance_bin=distance_bin,
                    max_attempts=int(config.max_query_sample_attempts),
                )
                queries.append(
                    EvaluationQuery(
                        query_id=f"{bucket.lower()}_s{seed_index:02d}_q{generated:04d}",
                        difficulty_bucket=bucket,
                        profile_name=profile.name,
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
    return tuple(queries)


def run_main_evaluation(
    output_dir: str | Path,
    *,
    config: MainEvaluationConfig | None = None,
    source_head: str = "unknown",
    command: str = "unknown",
) -> MainEvaluationResult:
    cfg = config or MainEvaluationConfig()
    preflight = preflight_main_evaluation(cfg)
    if not preflight.ok_to_run:
        raise RuntimeError("T14 preflight failed:\n- " + "\n- ".join(preflight.blocking_issues))

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    queries = build_query_set(cfg)
    predictors = _load_predictors(cfg, preflight.available_methods)
    eval_cfg = EvaluationConfig(
        bootstrap_resamples=int(cfg.bootstrap_resamples),
        bootstrap_seed=int(cfg.bootstrap_seed),
    )

    records: list[EvaluationRecord] = []
    map_cache: dict[int, GridMap] = {}
    for query in queries:
        grid_map = map_cache.get(query.map_seed)
        if grid_map is None:
            profile = _profile_by_name(cfg.profiles, query.profile_name)
            grid_map = _generate_grid_map(profile, query.map_seed, cfg, footprint)
            map_cache[query.map_seed] = grid_map

        vanilla_record: EvaluationRecord | None = None
        if "vanilla_ha" in preflight.available_methods:
            run = _run_vanilla_ha(query, grid_map, footprint, cfg, reference_path_length_m=None)
            vanilla_record = _evaluate_run_with_collision_rejection(run, grid_map, footprint, config=eval_cfg)
            records.append(vanilla_record)

        reference_length = vanilla_record.path_length_m if vanilla_record is not None and vanilla_record.feasible else None
        for method in preflight.available_methods:
            if method == "vanilla_ha":
                continue
            run = _run_method(
                method,
                query,
                grid_map,
                footprint,
                cfg,
                predictors=predictors,
                reference_path_length_m=reference_length,
            )
            records.append(_evaluate_run_with_collision_rejection(run, grid_map, footprint, config=eval_cfg))

    stat_pairs = _stat_pairs(preflight.available_methods)
    paired_tests = tuple(paired_wilcoxon_time(records, a, b) for a, b in stat_pairs)
    sr_cis = tuple(bootstrap_success_rate_difference(records, a, b, config=eval_cfg) for a, b in stat_pairs)
    paths = write_evaluation_outputs(records, out_dir, paired_time_tests=paired_tests, success_rate_cis=sr_cis)
    paths["queries_csv"] = _write_query_manifest(out_dir / "queries.csv", queries)
    paths["preflight_json"] = _write_json(out_dir / "preflight.json", asdict(preflight))
    config_payload = {
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": command,
        "config": _json_safe(asdict(cfg)),
    }
    paths["run_config_json"] = _write_json(out_dir / "run_config.json", config_payload)
    verdict = _build_verdict(records, queries, cfg, preflight)
    paths["verdict_json"] = _write_json(out_dir / "verdict.json", verdict)
    paths["report_md"] = _write_report(out_dir / "report.md", cfg, preflight, verdict, paths)
    return MainEvaluationResult(
        output_dir=out_dir,
        records=tuple(records),
        queries=queries,
        preflight=preflight,
        verdict=verdict,
        output_paths=paths,
    )


def _run_method(
    method: str,
    query: EvaluationQuery,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    *,
    predictors: dict[str, Any],
    reference_path_length_m: float | None,
):
    if method == "f_n3p_knn":
        from forest_n3p.inference import run_forest_n3p

        result = run_forest_n3p(
            grid_map,
            footprint,
            query.start,
            query.goal,
            predictors["knn"],
            config=_inference_config(cfg, k_neighbors=int(cfg.k_neighbors), query_seed=query.query_seed),
        )
        return planner_run_from_result(
            result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={"profile_name": query.profile_name, "map_seed": query.map_seed, "query_seed": query.query_seed},
        )

    if method == "n3p_k1":
        from forest_n3p.inference import run_forest_n3p

        result = run_forest_n3p(
            grid_map,
            footprint,
            query.start,
            query.goal,
            predictors["knn"],
            config=_inference_config(cfg, k_neighbors=1, query_seed=query.query_seed),
        )
        return planner_run_from_result(
            result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={"profile_name": query.profile_name, "map_seed": query.map_seed, "query_seed": query.query_seed},
        )

    if method == "voronoi_waypoint":
        from forest_n3p.baselines.voronoi_waypoint import (
            VoronoiWaypointConfig,
            plan_voronoi_waypoint,
        )

        result = plan_voronoi_waypoint(
            grid_map,
            footprint,
            query.start,
            query.goal,
            config=VoronoiWaypointConfig(
                segment_timeout_s=float(cfg.segment_timeout_s),
                segment_max_nodes=int(cfg.segment_max_nodes),
            ),
        )
        return planner_run_from_result(
            result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={
                "profile_name": query.profile_name,
                "map_seed": query.map_seed,
                "query_seed": query.query_seed,
                "waypoint_count": len(result.waypoints),
            },
        )

    if method == "bottleneck_waypoint":
        from forest_n3p.baselines.bottleneck_waypoint import (
            BottleneckWaypointConfig,
            plan_bottleneck_waypoint,
        )

        result = plan_bottleneck_waypoint(
            grid_map,
            footprint,
            query.start,
            query.goal,
            config=BottleneckWaypointConfig(
                segment_timeout_s=float(cfg.segment_timeout_s),
                segment_max_nodes=int(cfg.segment_max_nodes),
            ),
        )
        return planner_run_from_result(
            result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={
                "profile_name": query.profile_name,
                "map_seed": query.map_seed,
                "query_seed": query.query_seed,
                "waypoint_count": len(result.waypoints),
                "bottleneck_count": len(result.bottlenecks),
            },
        )

    if method == "improved_ha":
        from forest_n3p.baselines.improved_ha import make_improved_ha_planner

        planner = make_improved_ha_planner(grid_map, footprint)
        states, stats = planner.plan(
            AckermannState(*query.start),
            AckermannState(*query.goal),
            timeout=float(cfg.teacher_timeout_s),
            max_nodes=int(cfg.teacher_max_nodes),
        )
        return planner_run_from_path_stats(
            (state.as_tuple() for state in states),
            stats,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={"profile_name": query.profile_name, "map_seed": query.map_seed, "query_seed": query.query_seed},
        )

    if method == "lo_ha":
        planner = LOHybridAStarPlanner(
            grid_map,
            footprint,
            AckermannParams(wheelbase=0.6, min_turn_radius=1.0),
            analytic_expansion=True,
            collision_step=0.1,
            goal_xy_tol=0.30,
            goal_theta_tol=math.radians(15.0),
            use_holonomic_heuristic=True,
            theta_bins=72,
        )
        states, stats = planner.plan(
            AckermannState(*query.start),
            AckermannState(*query.goal),
            timeout=float(cfg.teacher_timeout_s),
            max_nodes=int(cfg.teacher_max_nodes),
        )
        return planner_run_from_path_stats(
            (state.as_tuple() for state in states),
            stats,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={"profile_name": query.profile_name, "map_seed": query.map_seed, "query_seed": query.query_seed},
        )

    if method == "ss_rrt":
        planner = RRTStarPlanner(
            grid_map,
            footprint,
            AckermannParams(wheelbase=0.6, min_turn_radius=1.0),
            goal_xy_tol=0.30,
            goal_theta_tol=math.radians(15.0),
            rng_seed=int(query.query_seed),
        )
        states, stats = planner.plan(
            AckermannState(*query.start),
            AckermannState(*query.goal),
            max_iter=3000,
            timeout=float(cfg.teacher_timeout_s),
        )
        stats = dict(stats)
        stats["expansions"] = int(stats.get("nodes", 0))
        return planner_run_from_path_stats(
            (state.as_tuple() for state in states),
            stats,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={
                "profile_name": query.profile_name,
                "map_seed": query.map_seed,
                "query_seed": query.query_seed,
                "rrt_iterations": int(stats.get("iterations", 0)),
            },
        )

    if method == "idb_rrt":
        from forest_n3p.baselines.idb_rrt_adapter import plan_idb_rrt

        result = plan_idb_rrt(
            grid_map,
            footprint,
            query.start,
            query.goal,
            config=_idb_rrt_config(cfg),
        )
        return planner_run_from_result(
            result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={
                "profile_name": query.profile_name,
                "map_seed": query.map_seed,
                "query_seed": query.query_seed,
                "idb_rrt_run_dir": result.run_dir,
                "idb_rrt_returncode": result.returncode,
                "idb_rrt_state_count": int(result.state_count),
            },
        )

    if method == "mlp":
        from forest_n3p.inference import run_forest_n3p

        result = run_forest_n3p(
            grid_map,
            footprint,
            query.start,
            query.goal,
            predictors["mlp"],
            config=_inference_config(cfg, k_neighbors=1, query_seed=query.query_seed),
        )
        return planner_run_from_result(
            result,
            query_id=query.query_id,
            method=method,
            difficulty_bucket=query.difficulty_bucket,
            distance_bin_key=query.distance_bin_key,
            reference_path_length_m=reference_path_length_m,
            metadata={
                "profile_name": query.profile_name,
                "map_seed": query.map_seed,
                "query_seed": query.query_seed,
                "mlp_model_dir": str(cfg.mlp_model_dir),
                "mlp_device": str(cfg.mlp_device),
            },
        )

    raise ValueError(f"unsupported method at runtime: {method}")


def _run_vanilla_ha(
    query: EvaluationQuery,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    cfg: MainEvaluationConfig,
    *,
    reference_path_length_m: float | None,
):
    planner = _make_planner(grid_map, footprint, cfg)
    states, stats = planner.plan(
        AckermannState(*query.start),
        AckermannState(*query.goal),
        timeout=float(cfg.teacher_timeout_s),
        max_nodes=int(cfg.teacher_max_nodes),
    )
    return planner_run_from_path_stats(
        (state.as_tuple() for state in states),
        stats,
        query_id=query.query_id,
        method="vanilla_ha",
        difficulty_bucket=query.difficulty_bucket,
        distance_bin_key=query.distance_bin_key,
        reference_path_length_m=reference_path_length_m,
        metadata={"profile_name": query.profile_name, "map_seed": query.map_seed, "query_seed": query.query_seed},
    )


def _evaluate_run_with_collision_rejection(
    run: EvaluationRun,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    *,
    config: EvaluationConfig | None = None,
) -> EvaluationRecord:
    record = evaluate_run(run, grid_map, footprint, config=config)
    if int(record.collision_violation_count) == 0:
        return record

    metadata = dict(run.metadata)
    metadata["rejected_collision_violation_count"] = int(record.collision_violation_count)
    metadata["rejected_collision_path_length_m"] = record.path_length_m
    reason = f"collision_violation_rejected:{record.collision_violation_count}"
    if run.failure_reason:
        reason = f"{reason};{run.failure_reason}"

    rejected_run = EvaluationRun(
        query_id=run.query_id,
        method=run.method,
        difficulty_bucket=run.difficulty_bucket,
        distance_bin_key=run.distance_bin_key,
        success=False,
        path=(),
        total_time_s=run.total_time_s,
        total_expansions=run.total_expansions,
        reference_path_length_m=run.reference_path_length_m,
        fallback_f1_count=run.fallback_f1_count,
        fallback_f2_count=run.fallback_f2_count,
        fallback_f3_count=run.fallback_f3_count,
        subgoal_reachable_count=run.subgoal_reachable_count,
        subgoal_attempt_count=run.subgoal_attempt_count,
        failure_reason=reason,
        metadata=metadata,
    )
    return evaluate_run(rejected_run, grid_map, footprint, config=config)


def _make_planner(grid_map: GridMap, footprint: TwoCircleFootprint, cfg: MainEvaluationConfig) -> HybridAStarPlanner:
    return HybridAStarPlanner(
        grid_map,
        footprint,
        AckermannParams(wheelbase=0.6, min_turn_radius=1.0),
        analytic_expansion=True,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=math.radians(15.0),
        use_holonomic_heuristic=True,
        theta_bins=72,
    )


def _inference_config(cfg: MainEvaluationConfig, *, k_neighbors: int, query_seed: int) -> InferenceConfig:
    from forest_n3p.inference import InferenceConfig

    return InferenceConfig(
        k_neighbors=int(k_neighbors),
        segment_timeout_s=float(cfg.segment_timeout_s),
        segment_max_nodes=int(cfg.segment_max_nodes),
        full_fallback_timeout_s=float(cfg.full_fallback_timeout_s),
        full_fallback_max_nodes=int(cfg.full_fallback_max_nodes),
        commit_verified_rs_segments=bool(cfg.commit_verified_rs_segments),
        max_steps_override=cfg.max_steps_override,
        enable_f1=bool(cfg.enable_f1),
        enable_f2=bool(cfg.enable_f2),
        enable_f3=bool(cfg.enable_f3),
        prediction_noise_sigma_m=float(cfg.prediction_noise_sigma_m),
        prediction_noise_seed=int(cfg.prediction_noise_seed) + int(query_seed),
    )


def _idb_rrt_config(cfg: MainEvaluationConfig):
    from forest_n3p.baselines.idb_rrt_adapter import IdBRrtAdapterConfig

    return IdBRrtAdapterConfig(
        binary_path=cfg.idb_rrt_binary_path,
        dynoplan_root=cfg.idb_rrt_dynoplan_root,
        motion_file=cfg.idb_rrt_motion_file,
        timeout_s=float(cfg.idb_rrt_timeout_s if cfg.idb_rrt_timeout_s is not None else cfg.teacher_timeout_s),
        seed=int(cfg.seed),
    )


def _generate_grid_map(
    profile: TrainingProfile,
    seed: int,
    config: MainEvaluationConfig,
    footprint: TwoCircleFootprint,
) -> GridMap:
    data_config = TrainingDataConfig(
        seed=int(config.seed),
        map_count=1,
        queries_per_map=1,
        width_cells=int(config.width_cells),
        height_cells=int(config.height_cells),
        resolution_m=float(config.resolution_m),
        profiles=(profile,),
    )
    params = make_forest_params(profile, data_config)
    grid, _start_xy, _goal_xy = generate_forest_grid(
        params=params,
        rng=np.random.default_rng(int(seed)),
        footprint_clearance_m=footprint_clearance_m(resolution_m=float(config.resolution_m)),
    )
    return GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0))


def _build_verdict(
    records: Sequence[EvaluationRecord],
    queries: Sequence[EvaluationQuery],
    cfg: MainEvaluationConfig,
    preflight: PreflightReport,
) -> dict[str, Any]:
    summaries = _summary_lookup(records)
    bucket_verdicts: dict[str, dict[str, Any]] = {}
    for bucket in ("Complex", "Extreme"):
        f_row = summaries.get(("f_n3p_knn", bucket))
        base_row = summaries.get(("vanilla_ha", bucket))
        if f_row is None or base_row is None:
            bucket_verdicts[bucket] = {"status": "missing", "reason": "missing f_n3p_knn or vanilla_ha summary"}
            continue
        median_time_reduction = None
        if base_row["median_time_s"] and float(base_row["median_time_s"]) > 0.0 and f_row["median_time_s"] is not None:
            median_time_reduction = 1.0 - float(f_row["median_time_s"]) / float(base_row["median_time_s"])
        success_drop_pp = 100.0 * (float(base_row["feasible_rate"]) - float(f_row["feasible_rate"]))
        median_inflation = f_row.get("median_path_inflation_ratio")
        checks = {
            "median_time_reduction_ge_50pct": median_time_reduction is not None and median_time_reduction >= 0.50,
            "success_drop_le_2pp": success_drop_pp <= 2.0,
            "median_path_inflation_le_5pct": median_inflation is not None and float(median_inflation) <= 0.05,
            "collision_violations_zero": int(f_row["collision_violation_total"]) == 0,
        }
        bucket_verdicts[bucket] = {
            "status": "pass" if all(checks.values()) else "fail",
            "median_time_reduction": median_time_reduction,
            "success_drop_pp": success_drop_pp,
            "median_path_inflation_ratio": median_inflation,
            "checks": checks,
        }

    collision_total = sum(int(row.collision_violation_count) for row in records)
    method_exception_total = sum(
        1
        for row in records
        if row.failure_reason is not None and "exception" in str(row.failure_reason).lower()
    )
    official_methods_satisfied = all(method in preflight.available_methods for method in OFFICIAL_T14_METHODS)
    expected_formal = bool(
        preflight.t14_scale_satisfied
        and not preflight.unavailable_methods
        and official_methods_satisfied
        and preflight.cutpoint_supplement_reviewed
        and preflight.human_review_satisfied
        and preflight.profile_bucket_satisfied
    )
    formal_acceptance = bool(
        expected_formal
        and collision_total == 0
        and method_exception_total == 0
        and all(item.get("status") == "pass" for item in bucket_verdicts.values())
    )
    return {
        "status": "formal_pass" if formal_acceptance else ("formal_fail" if expected_formal else "candidate_or_smoke"),
        "formal_acceptance": formal_acceptance,
        "record_count": len(records),
        "query_count": len(queries),
        "method_count": len(preflight.available_methods),
        "queries_per_bucket": _count_by_attr(queries, "difficulty_bucket"),
        "seed_count": len({query.seed_index for query in queries}),
        "collision_violation_total": collision_total,
        "method_exception_total": method_exception_total,
        "preflight_warnings": list(preflight.warnings),
        "preflight_unavailable_methods": dict(preflight.unavailable_methods),
        "official_methods_satisfied": bool(official_methods_satisfied),
        "missing_official_methods": [
            method for method in OFFICIAL_T14_METHODS if method not in preflight.available_methods
        ],
        "human_review_satisfied": bool(preflight.human_review_satisfied),
        "human_review_decisions": dict(preflight.human_review_decisions),
        "profile_bucket_satisfied": bool(preflight.profile_bucket_satisfied),
        "profile_bucket_issues": list(preflight.profile_bucket_issues),
        "bucket_verdicts": bucket_verdicts,
        "contract_thresholds": {
            "median_time_reduction_min": 0.50,
            "success_drop_pp_max": 2.0,
            "path_inflation_max": 0.05,
        },
        "note": (
            "candidate_or_smoke means this run is not sufficient for marking T14 complete; "
            "use reviewed T06 cutpoints, all official methods, >=50 queries per bucket, and >=5 seeds for formal acceptance"
        ),
    }


def _summary_lookup(records: Sequence[EvaluationRecord]) -> dict[tuple[str, str], dict[str, Any]]:
    from forest_n3p.evaluation import summarize_by_method_bucket

    return {(item.method, item.difficulty_bucket): asdict(item) for item in summarize_by_method_bucket(records)}


def _stat_pairs(methods: Sequence[str]) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for other in (
        "vanilla_ha",
        "n3p_k1",
        "mlp",
        "voronoi_waypoint",
        "bottleneck_waypoint",
        "improved_ha",
        "lo_ha",
        "ss_rrt",
        "idb_rrt",
    ):
        if "f_n3p_knn" in methods and other in methods and other != "f_n3p_knn":
            pairs.append(("f_n3p_knn", other))
    return tuple(pairs)


def _load_predictors(config: MainEvaluationConfig, methods: Sequence[str]) -> dict[str, Any]:
    predictors: dict[str, Any] = {}
    if any(method in methods for method in ("f_n3p_knn", "n3p_k1")):
        from forest_n3p.inference import FeatureMaskedKnnSubgoalLibrary, KnnSubgoalLibrary

        if config.knn_feature_indices is None:
            predictors["knn"] = KnnSubgoalLibrary.load(config.knn_library_dir)
        else:
            predictors["knn"] = FeatureMaskedKnnSubgoalLibrary.from_dataset(
                config.knn_dataset_dir,
                feature_indices=config.knn_feature_indices,
                name="masked_knn",
            )
    if "mlp" in methods:
        from forest_n3p.mlp import MlpSubgoalPredictor

        predictors["mlp"] = MlpSubgoalPredictor.load(config.mlp_model_dir, device=str(config.mlp_device))
    return predictors


def _profiles_by_bucket(profiles: Sequence[TrainingProfile]) -> dict[str, tuple[TrainingProfile, ...]]:
    out: dict[str, list[TrainingProfile]] = {}
    for profile in profiles:
        out.setdefault(profile.difficulty_bucket, []).append(profile)
    return {key: tuple(value) for key, value in out.items()}


def _profile_by_name(profiles: Sequence[TrainingProfile], name: str) -> TrainingProfile:
    for profile in profiles:
        if profile.name == name:
            return profile
    raise KeyError(name)


def _missing_knn_files(root: Path) -> list[str]:
    required = ("knn_tree.pkl", "labels.npy", "feature_mean.npy", "feature_std.npy", "metadata.json")
    return [name for name in required if not (Path(root) / name).exists()]


def _missing_knn_dataset_files(root: Path) -> list[str]:
    required = ("features.npy", "labels.npy")
    return [name for name in required if not (Path(root) / name).exists()]


def _missing_mlp_files(root: Path) -> list[str]:
    required = ("checkpoint.pt", "metadata.json")
    return [name for name in required if not (Path(root) / name).exists()]


def _read_human_review_decisions(path: Path) -> dict[str, str]:
    path = Path(path)
    if not path.exists():
        return {}

    decisions: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [part.strip() for part in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        decision_id, decision = cells[0], cells[1]
        if decision_id.startswith("D-T14-"):
            decisions[decision_id] = decision
    return decisions


def _human_review_issues(decisions: dict[str, str], *, form_path: Path) -> list[str]:
    issues: list[str] = []
    if not Path(form_path).exists():
        issues.append(f"missing human review form: {form_path}")

    for decision_id, allowed_values in FORMAL_HUMAN_DECISIONS.items():
        value = decisions.get(decision_id, "").strip()
        if not value:
            issues.append(f"{decision_id} missing decision")
            continue
        if value not in allowed_values:
            allowed = "|".join(allowed_values)
            issues.append(f"{decision_id} decision={value!r} is not formal-acceptable ({allowed})")

    return issues


def _profile_bucket_issues(config: MainEvaluationConfig, decisions: dict[str, str]) -> list[str]:
    t06_decision = decisions.get("D-T14-09")
    if t06_decision not in {"approve_original_with_justification", "revise_to_validation_cutpoints"}:
        return []

    if t06_decision == "approve_original_with_justification":
        expected, _unkeyed = _density_bucket_map_from_profiles(default_main_evaluation_profiles())
        expectation_source = "original T06 profiles"
    else:
        try:
            expected = _density_bucket_map_from_validation(config.t06_validation_summary_path)
        except Exception as exc:  # noqa: BLE001
            return [f"cannot read T06 validation cutpoints from {config.t06_validation_summary_path}: {exc}"]
        expectation_source = str(config.t06_validation_summary_path)

    actual, unkeyed = _density_bucket_map_from_profiles(config.profiles)
    issues: list[str] = []
    if unkeyed:
        issues.append(f"profiles lack density level keys: {', '.join(unkeyed)}")
    for level_key, expected_bucket in sorted(expected.items()):
        actual_bucket = actual.get(level_key)
        if actual_bucket is None:
            issues.append(f"missing profile for {level_key} expected={expected_bucket}")
        elif actual_bucket != expected_bucket:
            issues.append(f"{level_key} bucket={actual_bucket} expected={expected_bucket}")
    if issues:
        issues.insert(0, f"D-T14-09={t06_decision} expects buckets from {expectation_source}")
    return issues


def _density_bucket_map_from_validation(path: Path) -> dict[str, str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    summaries = payload.get("summary", {}).get("density_summaries", ())
    out: dict[str, str] = {}
    for item in summaries:
        level_key = str(item["level_key"])
        out[level_key] = str(item["difficulty_bucket"])
    if not out:
        raise ValueError("summary.density_summaries is empty")
    return out


def _density_bucket_map_from_profiles(profiles: Sequence[TrainingProfile]) -> tuple[dict[str, str], list[str]]:
    out: dict[str, str] = {}
    unkeyed: list[str] = []
    for profile in profiles:
        level_key = _density_level_key_from_profile_name(profile.name)
        if level_key is None:
            unkeyed.append(str(profile.name))
            continue
        out[level_key] = str(profile.difficulty_bucket)
    return out, unkeyed


def _density_level_key_from_profile_name(name: str) -> str | None:
    tail = str(name).rsplit("_", 1)[-1]
    if len(tail) == 3 and tail[0] == "d" and tail[1:].isdigit():
        return tail
    return None


def _frontmatter_bool(path: Path, key: str) -> bool:
    return _frontmatter_value(path, key) == "true"


def _frontmatter_value(path: Path, key: str) -> str | None:
    if not Path(path).exists():
        return None
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        raw_key, raw_value = line.split(":", 1)
        if raw_key.strip() == key:
            return raw_value.strip().strip('"').strip("'").lower()
    return None


def _write_query_manifest(path: Path, queries: Sequence[EvaluationQuery]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(asdict(queries[0]).keys()) if queries else list(EvaluationQuery.__dataclass_fields__.keys())
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


def _write_report(
    path: Path,
    cfg: MainEvaluationConfig,
    preflight: PreflightReport,
    verdict: dict[str, Any],
    paths: dict[str, Path],
) -> Path:
    lines = [
        "# T14 主评测运行报告",
        "",
        f"- status: {verdict['status']}",
        f"- formal_acceptance: {verdict['formal_acceptance']}",
        f"- query_count: {verdict['query_count']}",
        f"- record_count: {verdict['record_count']}",
        f"- methods: {', '.join(preflight.available_methods)}",
        f"- method_exception_total: {verdict['method_exception_total']}",
        f"- queries_per_bucket_config: {cfg.queries_per_bucket}",
        f"- seed_count_config: {cfg.seed_count}",
        f"- human_review_satisfied: {preflight.human_review_satisfied}",
        f"- profile_bucket_satisfied: {preflight.profile_bucket_satisfied}",
        "",
        "## 预检",
        "",
    ]
    if preflight.blocking_issues:
        lines.extend(f"- BLOCKING: {item}" for item in preflight.blocking_issues)
    else:
        lines.append("- blocking_issues: none")
    if preflight.warnings:
        lines.extend(f"- WARNING: {item}" for item in preflight.warnings)
    else:
        lines.append("- warnings: none")
    lines.extend(
        [
            "",
            "## Contract 判定边界",
            "",
            "- Complex/Extreme 桶要求：F-N3P 相对 vanilla HA* 中位时间缩减 >=50%，SR 下降 <=2 pp，路径膨胀 <=5%。",
            "- 本报告只有在 `formal_acceptance=true` 时才可作为 T14 完成依据；candidate/smoke 只验证 runner 和产物格式。",
            "",
            "## 输出文件",
            "",
        ]
    )
    for key, value in sorted(paths.items()):
        lines.append(f"- {key}: `{value}`")
    lines.append("")
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
