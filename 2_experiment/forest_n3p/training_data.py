from __future__ import annotations

import csv
import json
import math
import os
import signal
import socket
import subprocess
import threading
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from forest_n3p.difficulty_calibration import DistanceBin, parse_distance_bins, sample_query_in_distance_bin
from forest_n3p.labeling import LabelingConfig, LabelSample, extract_subgoal_labels
from forest_n3p.maps.forest import ForestParams, generate_forest_grid
from forest_n3p.pilot_labeling import _make_planner, _teacher_trace, footprint_clearance_m
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint


Pose = tuple[float, float, float]


@dataclass(frozen=True)
class TrainingProfile:
    name: str
    difficulty_bucket: str
    trunk_count: int
    trunk_gap_m: float
    trunk_gap_jitter: float = 0.25
    bush_cluster_count: int = 0


@dataclass(frozen=True)
class TrainingDataConfig:
    seed: int = 20260620
    map_count: int = 2000
    queries_per_map: int = 40
    width_cells: int = 300
    height_cells: int = 300
    resolution_m: float = 0.1
    teacher_timeout_s: float = 2.5
    teacher_wall_timeout_s: float = 4.0
    teacher_max_nodes: int = 15_000
    map_generation_wall_timeout_s: float = 30.0
    map_job_wall_timeout_s: float = 240.0
    max_query_sample_attempts: int = 800
    l_max_m: float = 8.0
    l_min_m: float = 1.0
    path_sample_step_m: float = 0.2
    turning_radius_m: float = 1.0
    wheelbase_m: float = 0.6
    rs_sample_step_m: float = 0.1
    total_sample_target: int = 100_000
    total_sample_lower_bound: int = 90_000
    min_samples_per_bucket: int = 10_000
    profiles: tuple[TrainingProfile, ...] = field(default_factory=lambda: default_training_profiles())
    distance_bins: tuple[DistanceBin, ...] = field(default_factory=lambda: parse_distance_bins("8:12,12:16,16:20,20:"))


@dataclass(frozen=True)
class TrainingMapRecord:
    map_id: int
    profile_name: str
    difficulty_bucket: str
    map_seed: int
    generated: bool
    generation_time_s: float
    trunk_count: int
    trunk_gap_m: float
    trunk_gap_jitter: float
    obstacle_ratio: float
    failure_reason: str | None


@dataclass(frozen=True)
class TrainingQueryRecord:
    global_query_id: int
    map_id: int
    query_id: int
    profile_name: str
    difficulty_bucket: str
    distance_bin_key: str
    distance_min_m: float
    distance_max_m: float | None
    map_seed: int
    query_seed: int
    start: Pose
    goal: Pose
    euclidean_distance_m: float
    teacher_success: bool
    teacher_failure_reason: str | None
    teacher_time_s: float
    teacher_expansions: int
    teacher_path_length_m: float
    teacher_path_pose_count: int
    label_attempted: bool
    label_success: bool
    label_failure_reason: str | None
    label_sample_count: int
    total_segment_count: int
    label_candidate_checks: int


@dataclass(frozen=True)
class TrainingSampleRecord:
    sample_id: int
    global_query_id: int
    map_id: int
    query_id: int
    sample_index: int
    profile_name: str
    difficulty_bucket: str
    distance_bin_key: str
    current_pose: Pose
    subgoal_pose: Pose
    delta_body: Pose
    s_start_m: float
    s_subgoal_m: float
    rs_length_m: float
    rs_sample_count: int


@dataclass(frozen=True)
class _RawSample:
    global_query_id: int
    map_id: int
    query_id: int
    sample_index: int
    profile_name: str
    difficulty_bucket: str
    distance_bin_key: str
    current_pose: Pose
    subgoal_pose: Pose
    delta_body: Pose
    s_start_m: float
    s_subgoal_m: float
    rs_length_m: float
    rs_sample_count: int
    feature_vector: np.ndarray


@dataclass(frozen=True)
class _PathRecord:
    global_query_id: int
    poses: np.ndarray


@dataclass(frozen=True)
class _MapJobResult:
    map_record: TrainingMapRecord
    queries: tuple[TrainingQueryRecord, ...]
    samples: tuple[_RawSample, ...]
    paths: tuple[_PathRecord, ...]


@dataclass(frozen=True)
class TrainingDataRun:
    config: TrainingDataConfig
    maps: tuple[TrainingMapRecord, ...]
    queries: tuple[TrainingQueryRecord, ...]
    samples: tuple[TrainingSampleRecord, ...]
    feature_array: np.ndarray
    label_array: np.ndarray
    path_query_indices: np.ndarray
    path_offsets: np.ndarray
    path_poses: np.ndarray
    summary: dict[str, Any]


class WallTimeoutError(TimeoutError):
    pass


def default_training_profiles() -> tuple[TrainingProfile, ...]:
    """Default T08 profiles from the provisional T06 density cut points."""
    return (
        TrainingProfile("easy_d00", "Easy", trunk_count=40, trunk_gap_m=1.35, trunk_gap_jitter=0.20),
        TrainingProfile("easy_d01", "Easy", trunk_count=55, trunk_gap_m=1.25, trunk_gap_jitter=0.20),
        TrainingProfile("complex_d02", "Complex", trunk_count=70, trunk_gap_m=1.15, trunk_gap_jitter=0.22),
        TrainingProfile("extreme_d03", "Extreme", trunk_count=85, trunk_gap_m=1.05, trunk_gap_jitter=0.24),
        TrainingProfile("extreme_d04", "Extreme", trunk_count=100, trunk_gap_m=0.95, trunk_gap_jitter=0.25),
        TrainingProfile("extreme_d05", "Extreme", trunk_count=115, trunk_gap_m=0.90, trunk_gap_jitter=0.25),
    )


def build_training_schedule(
    profiles: Sequence[TrainingProfile],
    *,
    map_count: int,
) -> tuple[TrainingProfile, ...]:
    if not profiles:
        raise ValueError("profiles must not be empty")
    count = int(map_count)
    if count <= 0:
        raise ValueError("map_count must be positive")

    bucket_order = tuple(dict.fromkeys(profile.difficulty_bucket for profile in profiles))
    by_bucket = {
        bucket: [profile for profile in profiles if profile.difficulty_bucket == bucket]
        for bucket in bucket_order
    }
    base = count // len(bucket_order)
    remainder = count % len(bucket_order)
    schedule: list[TrainingProfile] = []
    for bucket_idx, bucket in enumerate(bucket_order):
        bucket_count = base + (1 if bucket_idx < remainder else 0)
        bucket_profiles = by_bucket[bucket]
        for idx in range(bucket_count):
            schedule.append(bucket_profiles[idx % len(bucket_profiles)])
    return tuple(schedule)


def make_forest_params(profile: TrainingProfile, config: TrainingDataConfig) -> ForestParams:
    return ForestParams(
        width_cells=int(config.width_cells),
        height_cells=int(config.height_cells),
        cell_size_m=float(config.resolution_m),
        trunk_count=int(profile.trunk_count),
        trunk_gap_m=float(profile.trunk_gap_m),
        trunk_gap_jitter=float(profile.trunk_gap_jitter),
        bush_cluster_count=int(profile.bush_cluster_count),
        trunk_place_tries=20_000,
        max_tries=80,
        start_frac=0.2,
        goal_frac=0.8,
    )


def _distance_bin_for_query(config: TrainingDataConfig, query_id: int) -> DistanceBin:
    bins = tuple(config.distance_bins)
    if not bins:
        raise ValueError("distance_bins must not be empty")
    return bins[int(query_id) % len(bins)]


def _global_query_id(config: TrainingDataConfig, map_id: int, query_id: int) -> int:
    return int(map_id) * int(config.queries_per_map) + int(query_id)


def _nan_pose() -> Pose:
    return (math.nan, math.nan, math.nan)


def _run_map_job(args: tuple[int, TrainingProfile, TrainingDataConfig]) -> _MapJobResult:
    map_id, profile, config = args
    try:
        return _run_with_wall_timeout(
            "map_job",
            float(config.map_job_wall_timeout_s),
            lambda: _run_map_job_impl(args),
        )
    except WallTimeoutError as exc:
        return _failed_map_job_result(
            map_id=int(map_id),
            profile=profile,
            config=config,
            failure_reason=str(exc),
        )


def _run_map_job_impl(args: tuple[int, TrainingProfile, TrainingDataConfig]) -> _MapJobResult:
    map_id, profile, config = args
    map_seed = int(config.seed) + 100_000 + int(map_id)
    map_rng = np.random.default_rng(map_seed)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    started = time.perf_counter()
    grid: np.ndarray | None = None
    failure_reason: str | None = None
    generated = False
    try:
        grid, _start_xy, _goal_xy = _run_with_wall_timeout(
            "map_generation",
            float(config.map_generation_wall_timeout_s),
            lambda: generate_forest_grid(
                params=make_forest_params(profile, config),
                rng=map_rng,
                footprint_clearance_m=footprint_clearance_m(resolution_m=float(config.resolution_m)),
            ),
        )
        generated = True
    except WallTimeoutError as exc:
        failure_reason = str(exc)
    except Exception as exc:  # noqa: BLE001 - dataset inventory records map failures.
        failure_reason = f"{type(exc).__name__}: {exc}"

    generation_time_s = time.perf_counter() - started
    map_record = TrainingMapRecord(
        map_id=int(map_id),
        profile_name=profile.name,
        difficulty_bucket=profile.difficulty_bucket,
        map_seed=int(map_seed),
        generated=bool(generated),
        generation_time_s=float(generation_time_s),
        trunk_count=int(profile.trunk_count),
        trunk_gap_m=float(profile.trunk_gap_m),
        trunk_gap_jitter=float(profile.trunk_gap_jitter),
        obstacle_ratio=float(np.mean(grid)) if grid is not None else 0.0,
        failure_reason=failure_reason,
    )
    if grid is None:
        return _MapJobResult(map_record=map_record, queries=(), samples=(), paths=())

    grid_map = GridMap(grid, resolution=float(config.resolution_m), origin=(0.0, 0.0))
    planner = _make_planner(grid_map, footprint, config)
    labeling_config = LabelingConfig(
        l_max_m=float(config.l_max_m),
        l_min_m=float(config.l_min_m),
        path_sample_step_m=float(config.path_sample_step_m),
        turning_radius_m=float(config.turning_radius_m),
        wheelbase_m=float(config.wheelbase_m),
        rs_sample_step_m=float(config.rs_sample_step_m),
    )

    query_records: list[TrainingQueryRecord] = []
    sample_records: list[_RawSample] = []
    path_records: list[_PathRecord] = []
    for query_id in range(int(config.queries_per_map)):
        distance_bin = _distance_bin_for_query(config, query_id)
        query_seed = int(config.seed) + 200_000 + int(map_id) * 1_000 + int(query_id)
        query_rng = np.random.default_rng(query_seed)
        gqid = _global_query_id(config, map_id, query_id)
        try:
            start, goal = sample_query_in_distance_bin(
                grid_map,
                footprint,
                rng=query_rng,
                distance_bin=distance_bin,
                max_attempts=int(config.max_query_sample_attempts),
            )
        except Exception as exc:  # noqa: BLE001
            query_records.append(
                TrainingQueryRecord(
                    global_query_id=gqid,
                    map_id=int(map_id),
                    query_id=int(query_id),
                    profile_name=profile.name,
                    difficulty_bucket=profile.difficulty_bucket,
                    distance_bin_key=distance_bin.key,
                    distance_min_m=float(distance_bin.min_distance_m),
                    distance_max_m=distance_bin.max_distance_m,
                    map_seed=int(map_seed),
                    query_seed=int(query_seed),
                    start=_nan_pose(),
                    goal=_nan_pose(),
                    euclidean_distance_m=math.nan,
                    teacher_success=False,
                    teacher_failure_reason=f"query_sampling_failed:{type(exc).__name__}",
                    teacher_time_s=0.0,
                    teacher_expansions=0,
                    teacher_path_length_m=0.0,
                    teacher_path_pose_count=0,
                    label_attempted=False,
                    label_success=False,
                    label_failure_reason=None,
                    label_sample_count=0,
                    total_segment_count=0,
                    label_candidate_checks=0,
                )
            )
            continue

        try:
            path, stats = _run_with_wall_timeout(
                "teacher_plan",
                float(config.teacher_wall_timeout_s),
                lambda: planner.plan(
                    AckermannState(*start),
                    AckermannState(*goal),
                    timeout=float(config.teacher_timeout_s),
                    max_nodes=int(config.teacher_max_nodes),
                ),
            )
        except WallTimeoutError as exc:
            path = []
            stats = {
                "time": float(config.teacher_wall_timeout_s),
                "expansions": int(config.teacher_max_nodes),
                "path_length": 0.0,
                "failure_reason": str(exc),
            }
        teacher_success = bool(path)
        teacher_failure_reason = None if teacher_success else str(stats.get("failure_reason", "unknown"))
        trace: list[Pose] = []
        label_attempted = False
        label_success = False
        label_failure_reason: str | None = None
        label_sample_count = 0
        total_segment_count = 0
        label_candidate_checks = 0

        if teacher_success:
            trace = _teacher_trace(path, stats)
            path_records.append(
                _PathRecord(
                    global_query_id=gqid,
                    poses=np.asarray(trace, dtype=np.float32),
                )
            )
            label_attempted = True
            label_result = extract_subgoal_labels(
                grid_map,
                footprint,
                trace,
                config=labeling_config,
            )
            label_success = bool(label_result.success)
            label_failure_reason = label_result.failure_reason
            label_sample_count = len(label_result.samples)
            label_candidate_checks = int(label_result.candidate_checks)
            total_segment_count = label_sample_count + 1 if label_success else 0
            if label_success:
                for sample_index, sample in enumerate(label_result.samples):
                    sample_records.append(_raw_sample_from_label(sample, sample_index, gqid, map_id, query_id, profile, distance_bin))

        query_records.append(
            TrainingQueryRecord(
                global_query_id=gqid,
                map_id=int(map_id),
                query_id=int(query_id),
                profile_name=profile.name,
                difficulty_bucket=profile.difficulty_bucket,
                distance_bin_key=distance_bin.key,
                distance_min_m=float(distance_bin.min_distance_m),
                distance_max_m=distance_bin.max_distance_m,
                map_seed=int(map_seed),
                query_seed=int(query_seed),
                start=start,
                goal=goal,
                euclidean_distance_m=float(math.hypot(float(goal[0]) - float(start[0]), float(goal[1]) - float(start[1]))),
                teacher_success=teacher_success,
                teacher_failure_reason=teacher_failure_reason,
                teacher_time_s=float(stats.get("time", 0.0)),
                teacher_expansions=int(stats.get("expansions", 0)),
                teacher_path_length_m=float(stats.get("path_length", 0.0)),
                teacher_path_pose_count=len(trace),
                label_attempted=label_attempted,
                label_success=label_success,
                label_failure_reason=label_failure_reason,
                label_sample_count=int(label_sample_count),
                total_segment_count=int(total_segment_count),
                label_candidate_checks=int(label_candidate_checks),
            )
        )

    return _MapJobResult(
        map_record=map_record,
        queries=tuple(query_records),
        samples=tuple(sample_records),
        paths=tuple(path_records),
    )


def _failed_map_job_result(
    *,
    map_id: int,
    profile: TrainingProfile,
    config: TrainingDataConfig,
    failure_reason: str,
) -> _MapJobResult:
    map_seed = int(config.seed) + 100_000 + int(map_id)
    map_record = TrainingMapRecord(
        map_id=int(map_id),
        profile_name=profile.name,
        difficulty_bucket=profile.difficulty_bucket,
        map_seed=int(map_seed),
        generated=False,
        generation_time_s=float(config.map_job_wall_timeout_s),
        trunk_count=int(profile.trunk_count),
        trunk_gap_m=float(profile.trunk_gap_m),
        trunk_gap_jitter=float(profile.trunk_gap_jitter),
        obstacle_ratio=0.0,
        failure_reason=failure_reason,
    )
    return _MapJobResult(map_record=map_record, queries=(), samples=(), paths=())


def _raw_sample_from_label(
    sample: LabelSample,
    sample_index: int,
    global_query_id: int,
    map_id: int,
    query_id: int,
    profile: TrainingProfile,
    distance_bin: DistanceBin,
) -> _RawSample:
    return _RawSample(
        global_query_id=int(global_query_id),
        map_id=int(map_id),
        query_id=int(query_id),
        sample_index=int(sample_index),
        profile_name=profile.name,
        difficulty_bucket=profile.difficulty_bucket,
        distance_bin_key=distance_bin.key,
        current_pose=sample.current_pose,
        subgoal_pose=sample.subgoal_pose,
        delta_body=sample.delta_body,
        s_start_m=float(sample.s_start_m),
        s_subgoal_m=float(sample.s_subgoal_m),
        rs_length_m=float(sample.rs_length_m),
        rs_sample_count=int(sample.rs_sample_count),
        feature_vector=sample.feature_vector.astype(np.float32, copy=True),
    )


def run_training_data_collection(
    config: TrainingDataConfig,
    *,
    workers: int = 1,
    progress_every: int = 50,
) -> TrainingDataRun:
    _validate_config(config)
    schedule = build_training_schedule(config.profiles, map_count=int(config.map_count))
    jobs = [(map_id, profile, config) for map_id, profile in enumerate(schedule)]
    results: list[_MapJobResult] = []

    if int(workers) <= 1:
        for job in jobs:
            results.append(_run_map_job(job))
            _maybe_print_progress(len(results), len(jobs), progress_every)
    else:
        with ProcessPoolExecutor(max_workers=int(workers)) as executor:
            futures = [executor.submit(_run_map_job, job) for job in jobs]
            for done_count, future in enumerate(as_completed(futures), start=1):
                results.append(future.result())
                _maybe_print_progress(done_count, len(jobs), progress_every)

    results.sort(key=lambda item: item.map_record.map_id)
    maps = tuple(item.map_record for item in results)
    queries = tuple(query for item in results for query in item.queries)
    raw_samples = tuple(sample for item in results for sample in item.samples)
    paths = tuple(path for item in results for path in item.paths)

    sample_records: list[TrainingSampleRecord] = []
    features: list[np.ndarray] = []
    labels: list[tuple[float, float, float]] = []
    for sample_id, raw in enumerate(raw_samples):
        sample_records.append(
            TrainingSampleRecord(
                sample_id=int(sample_id),
                global_query_id=raw.global_query_id,
                map_id=raw.map_id,
                query_id=raw.query_id,
                sample_index=raw.sample_index,
                profile_name=raw.profile_name,
                difficulty_bucket=raw.difficulty_bucket,
                distance_bin_key=raw.distance_bin_key,
                current_pose=raw.current_pose,
                subgoal_pose=raw.subgoal_pose,
                delta_body=raw.delta_body,
                s_start_m=raw.s_start_m,
                s_subgoal_m=raw.s_subgoal_m,
                rs_length_m=raw.rs_length_m,
                rs_sample_count=raw.rs_sample_count,
            )
        )
        features.append(raw.feature_vector)
        labels.append(raw.delta_body)

    feature_dim = 41
    feature_array = (
        np.asarray(features, dtype=np.float32).reshape((len(features), feature_dim))
        if features
        else np.empty((0, feature_dim), dtype=np.float32)
    )
    label_array = (
        np.asarray(labels, dtype=np.float32).reshape((len(labels), 3))
        if labels
        else np.empty((0, 3), dtype=np.float32)
    )
    path_query_indices, path_offsets, path_poses = _pack_paths(paths)
    summary = summarize_training_data(
        config=config,
        maps=maps,
        queries=queries,
        samples=tuple(sample_records),
        feature_array=feature_array,
        label_array=label_array,
        paths=paths,
    )
    return TrainingDataRun(
        config=config,
        maps=maps,
        queries=queries,
        samples=tuple(sample_records),
        feature_array=feature_array,
        label_array=label_array,
        path_query_indices=path_query_indices,
        path_offsets=path_offsets,
        path_poses=path_poses,
        summary=summary,
    )


def _maybe_print_progress(done_count: int, total_count: int, progress_every: int) -> None:
    if int(progress_every) <= 0:
        return
    if done_count == total_count or done_count % int(progress_every) == 0:
        print(f"[training-data] maps_done={done_count}/{total_count}", flush=True)


def _pack_paths(paths: Sequence[_PathRecord]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ordered = sorted(paths, key=lambda item: item.global_query_id)
    query_indices = np.asarray([item.global_query_id for item in ordered], dtype=np.int64)
    offsets = [0]
    chunks: list[np.ndarray] = []
    for item in ordered:
        poses = np.asarray(item.poses, dtype=np.float32).reshape((-1, 3))
        chunks.append(poses)
        offsets.append(offsets[-1] + int(poses.shape[0]))
    path_poses = np.concatenate(chunks, axis=0) if chunks else np.empty((0, 3), dtype=np.float32)
    return query_indices, np.asarray(offsets, dtype=np.int64), path_poses


def _validate_config(config: TrainingDataConfig) -> None:
    if int(config.map_count) <= 0:
        raise ValueError("map_count must be positive")
    if int(config.queries_per_map) <= 0:
        raise ValueError("queries_per_map must be positive")
    if int(config.width_cells) <= 4 or int(config.height_cells) <= 4:
        raise ValueError("map size is too small")
    if len(config.profiles) < 3:
        raise ValueError("profiles must cover at least Easy, Complex, and Extreme")
    buckets = {profile.difficulty_bucket for profile in config.profiles}
    if not {"Easy", "Complex", "Extreme"}.issubset(buckets):
        raise ValueError("profiles must include Easy, Complex, and Extreme buckets")
    if not config.distance_bins:
        raise ValueError("distance_bins must not be empty")
    if int(config.total_sample_lower_bound) > int(config.total_sample_target):
        raise ValueError("total_sample_lower_bound must not exceed total_sample_target")
    if float(config.teacher_wall_timeout_s) <= float(config.teacher_timeout_s):
        raise ValueError("teacher_wall_timeout_s must exceed teacher_timeout_s")
    if float(config.map_generation_wall_timeout_s) <= 0.0:
        raise ValueError("map_generation_wall_timeout_s must be positive")
    if float(config.map_job_wall_timeout_s) <= float(config.map_generation_wall_timeout_s):
        raise ValueError("map_job_wall_timeout_s must exceed map_generation_wall_timeout_s")


def _run_with_wall_timeout(label: str, timeout_s: float, fn: Any) -> Any:
    timeout = float(timeout_s)
    if timeout <= 0.0:
        return fn()
    if threading.current_thread() is not threading.main_thread():
        return fn()

    old_handler = signal.getsignal(signal.SIGALRM)
    old_timer = signal.getitimer(signal.ITIMER_REAL)

    def _handle_timeout(_signum: int, _frame: Any) -> None:
        raise WallTimeoutError(f"{label}_wall_timeout:{timeout:.3f}s")

    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        return fn()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, old_handler)
        if old_timer[0] > 0.0:
            signal.setitimer(signal.ITIMER_REAL, old_timer[0], old_timer[1])


def _ratio(num: int, den: int) -> float | None:
    if den <= 0:
        return None
    return float(num) / float(den)


def summarize_training_data(
    *,
    config: TrainingDataConfig,
    maps: Sequence[TrainingMapRecord],
    queries: Sequence[TrainingQueryRecord],
    samples: Sequence[TrainingSampleRecord],
    feature_array: np.ndarray,
    label_array: np.ndarray,
    paths: Sequence[_PathRecord],
) -> dict[str, Any]:
    total_queries = len(queries)
    teacher_success = sum(1 for item in queries if item.teacher_success)
    label_attempt = sum(1 for item in queries if item.label_attempted)
    label_success = sum(1 for item in queries if item.label_success)
    label_failure = label_attempt - label_success
    by_bucket = {
        bucket: _summarize_subset(
            [query for query in queries if query.difficulty_bucket == bucket],
            [sample for sample in samples if sample.difficulty_bucket == bucket],
        )
        for bucket in ("Easy", "Complex", "Extreme")
    }
    by_distance_bin = {
        key: _summarize_subset(
            [query for query in queries if query.distance_bin_key == key],
            [sample for sample in samples if sample.distance_bin_key == key],
        )
        for key in sorted({item.distance_bin_key for item in queries})
    }
    sample_count_by_bucket = {bucket: int(item["sample_count"]) for bucket, item in by_bucket.items()}
    enough_bucket_coverage = all(
        count >= int(config.min_samples_per_bucket)
        for count in sample_count_by_bucket.values()
    )
    total_sample_pass = len(samples) >= int(config.total_sample_lower_bound)
    shape_pass = (
        feature_array.ndim == 2
        and label_array.ndim == 2
        and feature_array.shape[0] == label_array.shape[0] == len(samples)
        and feature_array.shape[1] == 41
        and label_array.shape[1] == 3
    )
    return {
        "map_count": len(maps),
        "generated_map_count": sum(1 for item in maps if item.generated),
        "map_generation_failure_count": sum(1 for item in maps if not item.generated),
        "map_generation_failure_reasons": _count_reasons(item.failure_reason for item in maps if not item.generated),
        "queries_per_map": int(config.queries_per_map),
        "total_queries": total_queries,
        "teacher_success_count": teacher_success,
        "teacher_success_rate": _ratio(teacher_success, total_queries),
        "teacher_failure_reasons": _count_reasons(item.teacher_failure_reason for item in queries if not item.teacher_success),
        "teacher_wall_timeout_count": sum(
            1
            for item in queries
            if item.teacher_failure_reason and item.teacher_failure_reason.startswith("teacher_plan_wall_timeout")
        ),
        "label_attempt_count": label_attempt,
        "label_success_count": label_success,
        "label_failure_count": label_failure,
        "label_failure_rate": _ratio(label_failure, label_attempt),
        "label_failure_reasons": _count_reasons(item.label_failure_reason for item in queries if item.label_attempted and not item.label_success),
        "total_samples": len(samples),
        "total_sample_target": int(config.total_sample_target),
        "total_sample_lower_bound": int(config.total_sample_lower_bound),
        "total_sample_pass": bool(total_sample_pass),
        "min_samples_per_bucket": int(config.min_samples_per_bucket),
        "sample_count_by_bucket": sample_count_by_bucket,
        "bucket_coverage_pass": bool(enough_bucket_coverage),
        "feature_shape": list(feature_array.shape),
        "label_shape": list(label_array.shape),
        "array_shape_pass": bool(shape_pass),
        "teacher_path_count": len(paths),
        "teacher_path_pose_count": int(sum(int(path.poses.shape[0]) for path in paths)),
        "acceptance_pass": bool(
            len(maps) >= int(config.map_count)
            and sum(1 for item in maps if item.generated) == len(maps)
            and total_sample_pass
            and enough_bucket_coverage
            and shape_pass
        ),
        "by_bucket": by_bucket,
        "by_distance_bin": by_distance_bin,
        "parameter_status": "provisional_from_reviewed_false_T05_T06",
    }


def _summarize_subset(
    queries: Sequence[TrainingQueryRecord],
    samples: Sequence[TrainingSampleRecord],
) -> dict[str, Any]:
    total_queries = len(queries)
    teacher_success = sum(1 for item in queries if item.teacher_success)
    label_attempt = sum(1 for item in queries if item.label_attempted)
    label_success = sum(1 for item in queries if item.label_success)
    label_failure = label_attempt - label_success
    times = [float(item.teacher_time_s) for item in queries]
    expansions = [float(item.teacher_expansions) for item in queries]
    return {
        "query_count": total_queries,
        "teacher_success_count": teacher_success,
        "teacher_success_rate": _ratio(teacher_success, total_queries),
        "teacher_wall_timeout_count": sum(
            1
            for item in queries
            if item.teacher_failure_reason and item.teacher_failure_reason.startswith("teacher_plan_wall_timeout")
        ),
        "label_attempt_count": label_attempt,
        "label_success_count": label_success,
        "label_failure_count": label_failure,
        "label_failure_rate": _ratio(label_failure, label_attempt),
        "sample_count": len(samples),
        "median_teacher_time_s": _percentile(times, 50.0),
        "p95_teacher_time_s": _percentile(times, 95.0),
        "median_teacher_expansions": _percentile(expansions, 50.0),
        "p95_teacher_expansions": _percentile(expansions, 95.0),
    }


def _count_reasons(reasons: Iterable[str | None]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for reason in reasons:
        key = str(reason or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _percentile(values: Sequence[float], pct: float) -> float | None:
    clean = [float(v) for v in values if math.isfinite(float(v))]
    if not clean:
        return None
    return float(np.percentile(np.asarray(clean, dtype=np.float64), float(pct)))


def write_training_data_outputs(
    run: TrainingDataRun,
    output_dir: Path,
    *,
    report_path: Path,
    source_head: str,
    execution_host: str,
    command: str,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    features_path = output_dir / "features.npy"
    labels_path = output_dir / "labels.npy"
    sample_query_indices_path = output_dir / "sample_query_indices.npy"
    paths_npz = output_dir / "teacher_paths.npz"
    maps_csv = output_dir / "maps.csv"
    queries_csv = output_dir / "queries.csv"
    samples_csv = output_dir / "samples.csv"
    summary_json = output_dir / "summary.json"
    readme_md = output_dir / "README.md"

    np.save(features_path, run.feature_array.astype(np.float32, copy=False))
    np.save(labels_path, run.label_array.astype(np.float32, copy=False))
    np.save(
        sample_query_indices_path,
        np.asarray([sample.global_query_id for sample in run.samples], dtype=np.int64),
    )
    np.savez_compressed(
        paths_npz,
        query_indices=run.path_query_indices,
        offsets=run.path_offsets,
        poses=run.path_poses.astype(np.float32, copy=False),
    )
    write_csv(maps_csv, run.maps)
    write_csv(queries_csv, run.queries)
    write_csv(samples_csv, run.samples)

    files = {
        "features_npy": str(features_path),
        "labels_npy": str(labels_path),
        "sample_query_indices_npy": str(sample_query_indices_path),
        "teacher_paths_npz": str(paths_npz),
        "maps_csv": str(maps_csv),
        "queries_csv": str(queries_csv),
        "samples_csv": str(samples_csv),
        "summary_json": str(summary_json),
        "report_md": str(report_path),
        "readme_md": str(readme_md),
    }
    payload = {
        "source_head": source_head,
        "execution_host": execution_host,
        "command": command,
        "config": _json_safe_dict(asdict(run.config)),
        "summary": _json_safe_dict(run.summary),
        "files": files,
    }
    summary_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    report = render_training_data_report(payload)
    report_path.write_text(report, encoding="utf-8")
    readme_md.write_text(report, encoding="utf-8")
    return files


def write_csv(path: Path, rows: Iterable[Any]) -> None:
    rows = tuple(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            raw = asdict(row)
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False) if isinstance(value, (tuple, list, dict)) else value
                    for key, value in raw.items()
                }
            )


def _json_safe_dict(obj: Any) -> Any:
    if isinstance(obj, tuple):
        return [_json_safe_dict(v) for v in obj]
    if isinstance(obj, list):
        return [_json_safe_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): _json_safe_dict(v) for k, v in obj.items()}
    return obj


def render_training_data_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    config = payload["config"]
    status = "pass" if summary.get("acceptance_pass") else "needs_review"
    lines = [
        "---",
        "date: 2026-06-20",
        f"status: {status}",
        "origin: ai+experiment",
        "reviewed: false",
        "task: T08",
        "contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_head: {payload['source_head']}",
        f"execution_host: {payload['execution_host']}",
        "---",
        "",
        "# T08 训练数据集生成报告",
        "",
        "## 结论",
        "",
        f"- 地图数: {summary['generated_map_count']} / {summary['map_count']}",
        f"- 查询数: {summary['total_queries']}",
        f"- 样本数: {summary['total_samples']}，目标约 {summary['total_sample_target']}",
        f"- 标签失败率: {_fmt_rate(summary['label_failure_rate'])}",
        f"- 验收状态: `{status}`",
        "",
        "参数说明：本次使用 T05 的 `L_min=1.0m` 和 T06 的密度/距离切点草案；二者 frontmatter 均为 `reviewed:false`，因此本数据集是可复现实验产物，但不是参数冻结声明。若 Dr Sun 修改 T05/T06 参数，需要用同一脚本重跑。",
        "",
        "## 实验设置",
        "",
        "```text",
        f"map_count={config['map_count']}",
        f"queries_per_map={config['queries_per_map']}",
        f"seed={config['seed']}",
        f"map_size_cells={config['width_cells']}x{config['height_cells']}",
        f"resolution_m={config['resolution_m']}",
        f"L_max_m={config['l_max_m']}",
        f"L_min_m={config['l_min_m']}",
        f"teacher_timeout_s={config['teacher_timeout_s']}",
        f"teacher_wall_timeout_s={config['teacher_wall_timeout_s']}",
        f"teacher_max_nodes={config['teacher_max_nodes']}",
        f"map_generation_wall_timeout_s={config['map_generation_wall_timeout_s']}",
        f"map_job_wall_timeout_s={config['map_job_wall_timeout_s']}",
        f"distance_bins={[(item['key'], item['min_distance_m'], item['max_distance_m']) for item in config['distance_bins']]}",
        "```",
        "",
        "## 总体统计",
        "",
        "| 指标 | 数值 |",
        "|---|---:|",
        f"| 教师求解成功率 | {_fmt_rate(summary['teacher_success_rate'])} |",
        f"| 教师 wall-time 超时数 | {summary['teacher_wall_timeout_count']} |",
        f"| 标签尝试数 | {summary['label_attempt_count']} |",
        f"| 标签成功数 | {summary['label_success_count']} |",
        f"| 标签失败率 | {_fmt_rate(summary['label_failure_rate'])} |",
        f"| 特征数组形状 | {summary['feature_shape']} |",
        f"| 标签数组形状 | {summary['label_shape']} |",
        f"| 教师路径数 | {summary['teacher_path_count']} |",
        f"| 教师路径 pose 总数 | {summary['teacher_path_pose_count']} |",
        "",
        "## 难度桶覆盖",
        "",
        "| 桶 | 查询数 | 教师成功率 | 标签失败率 | 样本数 | P50教师时间(s) | P95教师时间(s) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for bucket in ("Easy", "Complex", "Extreme"):
        item = summary["by_bucket"][bucket]
        lines.append(
            "| "
            f"{bucket} | "
            f"{item['query_count']} | "
            f"{_fmt_rate(item['teacher_success_rate'])} | "
            f"{_fmt_rate(item['label_failure_rate'])} | "
            f"{item['sample_count']} | "
            f"{_fmt_number(item['median_teacher_time_s'])} | "
            f"{_fmt_number(item['p95_teacher_time_s'])} |"
        )
    lines.extend(
        [
            "",
            "## 失败原因",
            "",
            "### Teacher",
            "",
            *(_format_reason_counts(summary["teacher_failure_reasons"]) or ["- 无"]),
            "",
            "### Label",
            "",
            *(_format_reason_counts(summary["label_failure_reasons"]) or ["- 无"]),
            "",
            "## 产物",
            "",
            f"- `features.npy`: `{payload['files']['features_npy']}`",
            f"- `labels.npy`: `{payload['files']['labels_npy']}`",
            f"- `teacher_paths.npz`: `{payload['files']['teacher_paths_npz']}`",
            f"- `samples.csv`: `{payload['files']['samples_csv']}`",
            f"- `queries.csv`: `{payload['files']['queries_csv']}`",
            f"- `maps.csv`: `{payload['files']['maps_csv']}`",
            "",
        ]
    )
    return "\n".join(lines)


def _fmt_rate(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{100.0 * float(value):.1f}%"


def _fmt_number(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.3f}"


def _format_reason_counts(counts: dict[str, int]) -> list[str]:
    return [f"- `{reason}`: {count}" for reason, count in counts.items()]


def source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        diff = subprocess.check_output(["git", "diff", "--stat"], text=True, stderr=subprocess.DEVNULL).strip()
        staged = subprocess.check_output(["git", "diff", "--cached", "--stat"], text=True, stderr=subprocess.DEVNULL).strip()
        suffix = "+dirty" if diff or staged else ""
        return f"{head}{suffix}"
    except Exception:
        return "unknown"


def execution_host() -> str:
    return socket.gethostname()


def default_workers() -> int:
    return max(1, min(8, (os.cpu_count() or 2) - 1))
