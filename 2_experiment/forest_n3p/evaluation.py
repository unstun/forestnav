from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

from forest_n3p.features import Pose, wrap_pi
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


TIMING_PROTOCOL_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class EvaluationConfig:
    theta_bins: int = 72
    collision_padding: float | None = None
    path_sample_step_m: float = 0.1
    bootstrap_resamples: int = 5_000
    bootstrap_confidence: float = 0.95
    bootstrap_seed: int = 20260620

    def __post_init__(self) -> None:
        if int(self.theta_bins) <= 0:
            raise ValueError("theta_bins must be positive")
        for name in ("path_sample_step_m", "bootstrap_confidence"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if not (0.0 < float(self.bootstrap_confidence) < 1.0):
            raise ValueError("bootstrap_confidence must be in (0, 1)")
        if int(self.bootstrap_resamples) <= 0:
            raise ValueError("bootstrap_resamples must be positive")


@dataclass(frozen=True)
class EvaluationRun:
    query_id: str
    method: str
    difficulty_bucket: str
    distance_bin_key: str
    success: bool
    path: tuple[Pose, ...]
    total_time_s: float
    total_expansions: int
    reference_path_length_m: float | None = None
    fallback_f1_count: int = 0
    fallback_f2_count: int = 0
    fallback_f3_count: int = 0
    subgoal_reachable_count: int | None = None
    subgoal_attempt_count: int | None = None
    failure_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationRecord:
    query_id: str
    method: str
    difficulty_bucket: str
    distance_bin_key: str
    success: bool
    feasible: bool
    total_time_s: float
    total_expansions: int
    path_length_m: float | None
    reference_path_length_m: float | None
    path_inflation_ratio: float | None
    direction_switches: int
    mean_abs_curvature: float | None
    min_clearance_m: float | None
    collision_violation_count: int
    fallback_f1_count: int
    fallback_f2_count: int
    fallback_f3_count: int
    fallback_triggered: bool
    subgoal_reachable_count: int | None
    subgoal_attempt_count: int | None
    subgoal_reachability_rate: float | None
    analytic_operator: str | None
    analytic_attempts: int | None
    analytic_successes: int | None
    analytic_failure_count: int | None
    rl_rollout_steps: int | None
    rl_rollout_collision_checks: int | None
    rl_rollout_sample_time_s: float | None
    rl_rollout_collision_time_s: float | None
    terminal_rs_time_s: float | None
    terminal_rs_success_count: int | None
    terminal_rs_used_count: int | None
    terminal_rs_action_count: int | None
    bc_checkpoint: str | None
    bc_checkpoint_sha256: str | None
    rl_rs_checkpoint: str | None
    rl_rs_checkpoint_sha256: str | None
    failure_reason: str | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GroupSummary:
    method: str
    difficulty_bucket: str
    count: int
    success_count: int
    success_rate: float
    feasible_count: int
    feasible_rate: float
    median_time_s: float | None
    p95_time_s: float | None
    min_time_s: float | None
    mean_time_s: float | None
    median_expansions: float | None
    p95_expansions: float | None
    median_path_inflation_ratio: float | None
    p95_path_inflation_ratio: float | None
    mean_direction_switches: float | None
    median_min_clearance_m: float | None
    collision_violation_total: int
    fallback_trigger_rate: float
    fallback_f1_rate: float
    fallback_f2_rate: float
    fallback_f3_rate: float
    subgoal_reachability_rate: float | None


@dataclass(frozen=True)
class PairedWilcoxonResult:
    method_a: str
    method_b: str
    paired_query_count: int
    statistic: float | None
    p_value: float | None
    median_delta_a_minus_b_s: float | None


@dataclass(frozen=True)
class BootstrapCIResult:
    method_a: str
    method_b: str
    paired_query_count: int
    observed_success_rate_diff_a_minus_b: float | None
    ci_low: float | None
    ci_high: float | None
    confidence_level: float
    n_resamples: int


def planner_run_from_result(
    result: Any,
    *,
    query_id: str,
    method: str,
    difficulty_bucket: str,
    distance_bin_key: str,
    reference_path_length_m: float | None = None,
    metadata: dict[str, Any] | None = None,
) -> EvaluationRun:
    path = tuple(_clean_pose(pose) for pose in getattr(result, "path", ()))
    success = bool(getattr(result, "success", bool(path)))
    used_f1 = int(getattr(result, "used_f1", 0))
    used_f2 = int(getattr(result, "used_f2", 0))
    used_f3 = int(getattr(result, "used_f3", 0))
    run_metadata = dict(metadata or {})
    planner_time = getattr(result, "total_planner_time_s", None)
    if planner_time is not None:
        run_metadata["total_planner_time_s"] = float(planner_time)
    run_metadata["timing_protocol"] = _timing_protocol(
        adapter="planner_run_from_result",
        total_time_source="result.total_time_s",
        planner_time_source="result.total_planner_time_s",
        planner_time_available=planner_time is not None,
        planner_time_components=(
            "direct RS collision check wall-clock",
            "predictor query plus subgoal RS validation overhead",
            "segment planner reported time",
            "F2/F3 fallback planner reported time",
        ),
    )
    subgoal_reachable_count: int | None = None
    subgoal_attempt_count: int | None = None
    steps = tuple(getattr(result, "steps", ()))
    if steps:
        prediction_steps = [step for step in steps if getattr(step, "neighbor_rank", None) is not None]
        subgoal_attempt_count = len(prediction_steps)
        subgoal_reachable_count = sum(1 for step in prediction_steps if int(step.neighbor_rank) == 1)
    return EvaluationRun(
        query_id=str(query_id),
        method=str(method),
        difficulty_bucket=str(difficulty_bucket),
        distance_bin_key=str(distance_bin_key),
        success=success,
        path=path,
        total_time_s=float(getattr(result, "total_time_s", math.nan)),
        total_expansions=int(getattr(result, "total_expansions", 0)),
        reference_path_length_m=reference_path_length_m,
        fallback_f1_count=used_f1,
        fallback_f2_count=used_f2,
        fallback_f3_count=used_f3,
        subgoal_reachable_count=subgoal_reachable_count,
        subgoal_attempt_count=subgoal_attempt_count,
        failure_reason=getattr(result, "failure_reason", None),
        metadata=run_metadata,
    )


def planner_run_from_path_stats(
    path: Iterable[Any],
    stats: dict[str, Any],
    *,
    query_id: str,
    method: str,
    difficulty_bucket: str,
    distance_bin_key: str,
    reference_path_length_m: float | None = None,
    metadata: dict[str, Any] | None = None,
) -> EvaluationRun:
    raw_path = tuple(path)
    trace_poses = tuple(stats.get("trace_poses") or ())
    if trace_poses:
        poses = tuple(_clean_pose(pose) for pose in trace_poses)
        path_source = "trace_poses"
    else:
        poses = tuple(_clean_pose(pose.as_tuple() if hasattr(pose, "as_tuple") else pose) for pose in raw_path)
        path_source = "planner_path"
    run_metadata = dict(metadata or {})
    planner_time = float(stats.get("time", math.nan))
    run_metadata.setdefault("evaluation_path_source", path_source)
    run_metadata.setdefault("planner_path_pose_count", len(raw_path))
    run_metadata.setdefault("evaluation_path_pose_count", len(poses))
    for key in (
        "analytic_operator",
        "analytic_attempts",
        "analytic_successes",
        "analytic_failure_count",
        "analytic_candidate_radius_count",
        "analytic_candidate_success_count",
        "analytic_candidate_failure_count",
        "analytic_rs_solve_time_s",
        "analytic_sample_time_s",
        "analytic_collision_check_time_s",
        "analytic_cost_eval_time_s",
        "analytic_total_time_s",
        "analytic_sample_count",
        "analytic_collision_check_count",
    ):
        if key in stats:
            run_metadata.setdefault(key, stats[key])
    if "remediations" in stats:
        run_metadata.setdefault("planner_remediations", stats["remediations"])
    _update_rl_rs_telemetry_summary(run_metadata, stats.get("analytic_telemetry_records") or ())
    run_metadata["total_planner_time_s"] = planner_time
    run_metadata["timing_protocol"] = _timing_protocol(
        adapter="planner_run_from_path_stats",
        total_time_source='stats["time"]',
        planner_time_source='stats["time"]',
        planner_time_available=True,
        planner_time_components=("planner.plan reported wall-clock",),
    )
    return EvaluationRun(
        query_id=str(query_id),
        method=str(method),
        difficulty_bucket=str(difficulty_bucket),
        distance_bin_key=str(distance_bin_key),
        success=bool(raw_path) and stats.get("failure_reason") is None,
        path=poses,
        total_time_s=planner_time,
        total_expansions=int(stats.get("expansions", 0)),
        reference_path_length_m=reference_path_length_m,
        failure_reason=stats.get("failure_reason"),
        metadata=run_metadata,
    )


def _timing_protocol(
    *,
    adapter: str,
    total_time_source: str,
    planner_time_source: str,
    planner_time_available: bool,
    planner_time_components: Sequence[str],
) -> dict[str, Any]:
    return {
        "schema_version": TIMING_PROTOCOL_SCHEMA_VERSION,
        "adapter": str(adapter),
        "total_time_s": {
            "record_field": "EvaluationRun.total_time_s / EvaluationRecord.total_time_s",
            "source": str(total_time_source),
            "semantics": "end_to_end_method_wall_clock_seconds",
        },
        "planner_time_s": {
            "record_field": "EvaluationRun.metadata.total_planner_time_s / EvaluationRecord.metadata.total_planner_time_s",
            "source": str(planner_time_source),
            "available": bool(planner_time_available),
            "semantics": "planner_scoped_wall_clock_seconds",
            "included_components": list(planner_time_components),
        },
        "comparison_rule": (
            "Use total_time_s for method comparisons; use metadata.total_planner_time_s "
            "only for timing audits and component accounting."
        ),
    }


def evaluate_run(
    run: EvaluationRun,
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    *,
    config: EvaluationConfig | None = None,
) -> EvaluationRecord:
    cfg = config or EvaluationConfig()
    samples = densify_path(run.path, step_m=float(cfg.path_sample_step_m))
    checker = GridFootprintChecker(
        grid_map,
        footprint,
        theta_bins=int(cfg.theta_bins),
        padding=cfg.collision_padding,
    )
    collision_count = sum(1 for pose in samples if checker.collides_pose(*pose))
    path_len = path_length(run.path) if run.path else None
    subgoal_rate = _safe_rate(run.subgoal_reachable_count, run.subgoal_attempt_count)
    feasible = bool(run.success and run.path and collision_count == 0)
    inflation = _path_inflation(path_len, run.reference_path_length_m, feasible)
    return EvaluationRecord(
        query_id=run.query_id,
        method=run.method,
        difficulty_bucket=run.difficulty_bucket,
        distance_bin_key=run.distance_bin_key,
        success=bool(run.success),
        feasible=feasible,
        total_time_s=float(run.total_time_s),
        total_expansions=int(run.total_expansions),
        path_length_m=path_len,
        reference_path_length_m=run.reference_path_length_m,
        path_inflation_ratio=inflation,
        direction_switches=direction_switches(run.path),
        mean_abs_curvature=mean_abs_curvature(run.path),
        min_clearance_m=min_clearance_m(grid_map, footprint, samples, collision_padding=cfg.collision_padding),
        collision_violation_count=int(collision_count),
        fallback_f1_count=int(run.fallback_f1_count),
        fallback_f2_count=int(run.fallback_f2_count),
        fallback_f3_count=int(run.fallback_f3_count),
        fallback_triggered=bool(run.fallback_f1_count or run.fallback_f2_count or run.fallback_f3_count),
        subgoal_reachable_count=run.subgoal_reachable_count,
        subgoal_attempt_count=run.subgoal_attempt_count,
        subgoal_reachability_rate=subgoal_rate,
        analytic_operator=_metadata_str(run.metadata, "analytic_operator"),
        analytic_attempts=_metadata_int(run.metadata, "analytic_attempts"),
        analytic_successes=_metadata_int(run.metadata, "analytic_successes"),
        analytic_failure_count=_metadata_int(run.metadata, "analytic_failure_count"),
        rl_rollout_steps=_metadata_int(run.metadata, "rl_rollout_steps"),
        rl_rollout_collision_checks=_metadata_int(run.metadata, "rl_rollout_collision_checks"),
        rl_rollout_sample_time_s=_metadata_float(run.metadata, "rl_rollout_sample_time_s"),
        rl_rollout_collision_time_s=_metadata_float(run.metadata, "rl_rollout_collision_time_s"),
        terminal_rs_time_s=_metadata_float(run.metadata, "terminal_rs_time_s"),
        terminal_rs_success_count=_metadata_int(run.metadata, "terminal_rs_success_count"),
        terminal_rs_used_count=_metadata_int(run.metadata, "terminal_rs_used_count"),
        terminal_rs_action_count=_metadata_int(run.metadata, "terminal_rs_action_count"),
        bc_checkpoint=_metadata_str(run.metadata, "bc_checkpoint"),
        bc_checkpoint_sha256=_metadata_str(run.metadata, "bc_checkpoint_sha256"),
        rl_rs_checkpoint=_metadata_str(run.metadata, "rl_rs_checkpoint"),
        rl_rs_checkpoint_sha256=_metadata_str(run.metadata, "rl_rs_checkpoint_sha256"),
        failure_reason=run.failure_reason,
        metadata=dict(run.metadata),
    )


def _update_rl_rs_telemetry_summary(metadata: dict[str, Any], records: Sequence[Any]) -> None:
    clean = [record for record in records if isinstance(record, dict) and _has_rl_rs_telemetry(record)]
    if not clean:
        return
    for key in ("rl_rollout_steps", "rl_rollout_collision_checks", "terminal_rs_action_count"):
        metadata.setdefault(key, sum(int(record.get(key, 0) or 0) for record in clean))
    for key in ("rl_rollout_sample_time_s", "rl_rollout_collision_time_s", "terminal_rs_time_s"):
        metadata.setdefault(key, sum(float(record.get(key, 0.0) or 0.0) for record in clean))
    metadata.setdefault("terminal_rs_success_count", sum(1 for record in clean if bool(record.get("terminal_rs_success"))))
    metadata.setdefault("terminal_rs_used_count", sum(1 for record in clean if bool(record.get("terminal_rs_used"))))


def _has_rl_rs_telemetry(record: dict[str, Any]) -> bool:
    return any(str(key).startswith("rl_rollout_") for key in record) or "terminal_rs_used" in record


def _metadata_str(metadata: dict[str, Any], key: str) -> str | None:
    value = metadata.get(key)
    if value is None:
        return None
    return str(value)


def _metadata_int(metadata: dict[str, Any], key: str) -> int | None:
    value = metadata.get(key)
    if value is None:
        return None
    return int(value)


def _metadata_float(metadata: dict[str, Any], key: str) -> float | None:
    value = metadata.get(key)
    if value is None:
        return None
    return float(value)


def summarize_by_method_bucket(records: Iterable[EvaluationRecord]) -> tuple[GroupSummary, ...]:
    rows = tuple(records)
    keys = sorted({(row.method, row.difficulty_bucket) for row in rows})
    out: list[GroupSummary] = []
    for method, bucket in keys:
        group = [row for row in rows if row.method == method and row.difficulty_bucket == bucket]
        count = len(group)
        feasible_count = sum(1 for row in group if row.feasible)
        success_count = feasible_count
        subgoal_reachable = sum(row.subgoal_reachable_count or 0 for row in group)
        subgoal_attempts = sum(row.subgoal_attempt_count or 0 for row in group)
        out.append(
            GroupSummary(
                method=method,
                difficulty_bucket=bucket,
                count=count,
                success_count=success_count,
                success_rate=_ratio(success_count, count),
                feasible_count=feasible_count,
                feasible_rate=_ratio(feasible_count, count),
                median_time_s=_percentile((row.total_time_s for row in group), 50),
                p95_time_s=_percentile((row.total_time_s for row in group), 95),
                min_time_s=_min_finite(row.total_time_s for row in group),
                mean_time_s=_mean(row.total_time_s for row in group),
                median_expansions=_percentile((row.total_expansions for row in group), 50),
                p95_expansions=_percentile((row.total_expansions for row in group), 95),
                median_path_inflation_ratio=_percentile((row.path_inflation_ratio for row in group), 50),
                p95_path_inflation_ratio=_percentile((row.path_inflation_ratio for row in group), 95),
                mean_direction_switches=_mean(row.direction_switches for row in group),
                median_min_clearance_m=_percentile((row.min_clearance_m for row in group), 50),
                collision_violation_total=sum(int(row.collision_violation_count) for row in group),
                fallback_trigger_rate=_ratio(sum(1 for row in group if row.fallback_triggered), count),
                fallback_f1_rate=_ratio(sum(1 for row in group if row.fallback_f1_count > 0), count),
                fallback_f2_rate=_ratio(sum(1 for row in group if row.fallback_f2_count > 0), count),
                fallback_f3_rate=_ratio(sum(1 for row in group if row.fallback_f3_count > 0), count),
                subgoal_reachability_rate=_safe_rate(subgoal_reachable, subgoal_attempts),
            )
        )
    return tuple(out)


def paired_wilcoxon_time(
    records: Iterable[EvaluationRecord],
    method_a: str,
    method_b: str,
    *,
    success_only: bool = False,
) -> PairedWilcoxonResult:
    pairs = _paired_records(records, method_a, method_b)
    x: list[float] = []
    y: list[float] = []
    for a, b in pairs:
        if success_only and not (a.success and b.success):
            continue
        if math.isfinite(a.total_time_s) and math.isfinite(b.total_time_s):
            x.append(float(a.total_time_s))
            y.append(float(b.total_time_s))
    if not x:
        return PairedWilcoxonResult(method_a, method_b, 0, None, None, None)
    diffs = np.asarray(x, dtype=np.float64) - np.asarray(y, dtype=np.float64)
    median_delta = float(np.median(diffs))
    if np.allclose(diffs, 0.0):
        return PairedWilcoxonResult(method_a, method_b, len(x), 0.0, 1.0, median_delta)
    from scipy.stats import wilcoxon

    result = wilcoxon(np.asarray(x, dtype=np.float64), np.asarray(y, dtype=np.float64), zero_method="wilcox")
    return PairedWilcoxonResult(
        method_a=method_a,
        method_b=method_b,
        paired_query_count=len(x),
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        median_delta_a_minus_b_s=median_delta,
    )


def bootstrap_success_rate_difference(
    records: Iterable[EvaluationRecord],
    method_a: str,
    method_b: str,
    *,
    config: EvaluationConfig | None = None,
) -> BootstrapCIResult:
    cfg = config or EvaluationConfig()
    pairs = _paired_records(records, method_a, method_b)
    diffs = np.asarray([float(a.feasible) - float(b.feasible) for a, b in pairs], dtype=np.float64)
    if diffs.size == 0:
        return BootstrapCIResult(method_a, method_b, 0, None, None, None, cfg.bootstrap_confidence, cfg.bootstrap_resamples)
    observed = float(np.mean(diffs))
    if diffs.size < 2 or np.allclose(diffs, diffs[0]):
        return BootstrapCIResult(
            method_a,
            method_b,
            int(diffs.size),
            observed,
            observed,
            observed,
            float(cfg.bootstrap_confidence),
            int(cfg.bootstrap_resamples),
        )

    def statistic(sample: np.ndarray, axis: int = 0) -> np.ndarray:
        return np.mean(sample, axis=axis)

    from scipy.stats import bootstrap

    res = bootstrap(
        (diffs,),
        statistic,
        n_resamples=int(cfg.bootstrap_resamples),
        confidence_level=float(cfg.bootstrap_confidence),
        method="percentile",
        rng=np.random.default_rng(int(cfg.bootstrap_seed)),
    )
    return BootstrapCIResult(
        method_a=method_a,
        method_b=method_b,
        paired_query_count=int(diffs.size),
        observed_success_rate_diff_a_minus_b=observed,
        ci_low=float(res.confidence_interval.low),
        ci_high=float(res.confidence_interval.high),
        confidence_level=float(cfg.bootstrap_confidence),
        n_resamples=int(cfg.bootstrap_resamples),
    )


def write_evaluation_outputs(
    records: Iterable[EvaluationRecord],
    output_dir: str | Path,
    *,
    paired_time_tests: Sequence[PairedWilcoxonResult] = (),
    success_rate_cis: Sequence[BootstrapCIResult] = (),
) -> dict[str, Path]:
    rows = tuple(records)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    records_csv = out_dir / "records.csv"
    summary_csv = out_dir / "summary_by_method_bucket.csv"
    summary_json = out_dir / "summary.json"
    _write_dataclass_csv(records_csv, rows)
    summaries = summarize_by_method_bucket(rows)
    _write_dataclass_csv(summary_csv, summaries)
    payload = {
        "record_count": len(rows),
        "summary_by_method_bucket": [asdict(item) for item in summaries],
        "paired_time_tests": [asdict(item) for item in paired_time_tests],
        "success_rate_bootstrap_ci": [asdict(item) for item in success_rate_cis],
    }
    summary_json.write_text(json.dumps(_json_safe(payload), indent=2, ensure_ascii=False), encoding="utf-8")
    return {
        "records_csv": records_csv,
        "summary_csv": summary_csv,
        "summary_json": summary_json,
    }


def path_length(path: Iterable[Pose]) -> float:
    poses = tuple(path)
    return float(
        sum(
            math.hypot(float(cur[0]) - float(prev[0]), float(cur[1]) - float(prev[1]))
            for prev, cur in zip(poses[:-1], poses[1:], strict=True)
        )
    )


def densify_path(path: Iterable[Pose], *, step_m: float = 0.1) -> tuple[Pose, ...]:
    poses = tuple(_clean_pose(pose) for pose in path)
    if len(poses) <= 1:
        return poses
    out: list[Pose] = [poses[0]]
    step = max(float(step_m), 1e-6)
    for start, end in zip(poses[:-1], poses[1:], strict=True):
        dx = float(end[0]) - float(start[0])
        dy = float(end[1]) - float(start[1])
        dist = math.hypot(dx, dy)
        n = max(1, int(math.ceil(dist / step)))
        dtheta = wrap_pi(float(end[2]) - float(start[2]))
        for i in range(1, n + 1):
            alpha = float(i) / float(n)
            out.append(
                (
                    float(start[0]) + alpha * dx,
                    float(start[1]) + alpha * dy,
                    wrap_pi(float(start[2]) + alpha * dtheta),
                )
            )
    return tuple(out)


def direction_switches(path: Iterable[Pose], *, epsilon_m: float = 1e-6) -> int:
    poses = tuple(_clean_pose(pose) for pose in path)
    prev_sign: int | None = None
    switches = 0
    for start, end in zip(poses[:-1], poses[1:], strict=True):
        dx = float(end[0]) - float(start[0])
        dy = float(end[1]) - float(start[1])
        if math.hypot(dx, dy) <= epsilon_m:
            continue
        forward_dot = math.cos(float(start[2])) * dx + math.sin(float(start[2])) * dy
        sign = 1 if forward_dot >= 0.0 else -1
        if prev_sign is not None and sign != prev_sign:
            switches += 1
        prev_sign = sign
    return int(switches)


def mean_abs_curvature(path: Iterable[Pose], *, epsilon_m: float = 1e-9) -> float | None:
    poses = tuple(_clean_pose(pose) for pose in path)
    if len(poses) < 2:
        return None
    total_abs_heading = 0.0
    total_length = 0.0
    for start, end in zip(poses[:-1], poses[1:], strict=True):
        dist = math.hypot(float(end[0]) - float(start[0]), float(end[1]) - float(start[1]))
        if dist <= epsilon_m:
            continue
        total_length += dist
        total_abs_heading += abs(wrap_pi(float(end[2]) - float(start[2])))
    if total_length <= epsilon_m:
        return None
    return float(total_abs_heading / total_length)


def min_clearance_m(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    path: Iterable[Pose],
    *,
    collision_padding: float | None = None,
) -> float | None:
    poses = tuple(_clean_pose(pose) for pose in path)
    if not poses:
        return None
    edt_m = _distance_field_m(grid_map)
    padding = 0.0 if collision_padding is None else float(collision_padding)
    values: list[float] = []
    for x, y, theta in poses:
        if isinstance(footprint, TwoCircleFootprint):
            for cx, cy in footprint.circle_centers(float(x), float(y), float(theta)):
                values.append(_dist_at_m(edt_m, grid_map, cx, cy) - float(footprint.radius) - padding)
        else:
            values.append(_dist_at_m(edt_m, grid_map, float(x), float(y)) - padding)
    if not values:
        return None
    return float(min(values))


def _distance_field_m(grid_map: GridMap) -> np.ndarray:
    from scipy.ndimage import distance_transform_edt

    free = np.asarray(grid_map.data) == 0
    padded = np.pad(free, 1, mode="constant", constant_values=False)
    return distance_transform_edt(padded)[1:-1, 1:-1] * float(grid_map.resolution)


def _dist_at_m(field: np.ndarray, grid_map: GridMap, x: float, y: float) -> float:
    xi = (float(x) - float(grid_map.origin[0])) / float(grid_map.resolution)
    yi = (float(y) - float(grid_map.origin[1])) / float(grid_map.resolution)
    h, w = field.shape
    if not (0.0 <= xi <= float(w - 1) and 0.0 <= yi <= float(h - 1)):
        return 0.0
    x0 = int(math.floor(xi))
    y0 = int(math.floor(yi))
    x1 = min(x0 + 1, w - 1)
    y1 = min(y0 + 1, h - 1)
    fx = float(xi - x0)
    fy = float(yi - y0)
    v00 = float(field[y0, x0])
    v10 = float(field[y0, x1])
    v01 = float(field[y1, x0])
    v11 = float(field[y1, x1])
    return float((1.0 - fy) * ((1.0 - fx) * v00 + fx * v10) + fy * ((1.0 - fx) * v01 + fx * v11))


def _paired_records(
    records: Iterable[EvaluationRecord],
    method_a: str,
    method_b: str,
) -> list[tuple[EvaluationRecord, EvaluationRecord]]:
    by_method_query = {(row.method, row.query_id): row for row in records}
    query_ids = sorted(
        {
            query_id
            for method, query_id in by_method_query
            if method == method_a and (method_b, query_id) in by_method_query
        }
    )
    return [(by_method_query[(method_a, query_id)], by_method_query[(method_b, query_id)]) for query_id in query_ids]


def _path_inflation(path_len: float | None, ref_len: float | None, success: bool) -> float | None:
    if not success or path_len is None or ref_len is None:
        return None
    ref = float(ref_len)
    if not (math.isfinite(ref) and ref > 0.0):
        return None
    return float(float(path_len) / ref - 1.0)


def _safe_rate(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator is None or int(denominator) <= 0:
        return None
    return float(numerator) / float(denominator)


def _ratio(numerator: int, denominator: int) -> float:
    return 0.0 if int(denominator) <= 0 else float(numerator) / float(denominator)


def _finite(values: Iterable[float | int | None]) -> list[float]:
    out: list[float] = []
    for value in values:
        if value is None:
            continue
        v = float(value)
        if math.isfinite(v):
            out.append(v)
    return out


def _percentile(values: Iterable[float | int | None], q: float) -> float | None:
    clean = _finite(values)
    if not clean:
        return None
    return float(np.percentile(np.asarray(clean, dtype=np.float64), float(q)))


def _mean(values: Iterable[float | int | None]) -> float | None:
    clean = _finite(values)
    if not clean:
        return None
    return float(np.mean(np.asarray(clean, dtype=np.float64)))


def _min_finite(values: Iterable[float | int | None]) -> float | None:
    clean = _finite(values)
    if not clean:
        return None
    return float(min(clean))


def _write_dataclass_csv(path: Path, rows: Sequence[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False) if isinstance(value, (tuple, list, dict)) else value
                    for key, value in asdict(row).items()
                }
            )


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, tuple):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    return obj


def _clean_pose(pose: Pose) -> Pose:
    out = (float(pose[0]), float(pose[1]), wrap_pi(float(pose[2])))
    if not all(math.isfinite(value) for value in out):
        raise ValueError(f"pose values must be finite, got {pose!r}")
    return out
