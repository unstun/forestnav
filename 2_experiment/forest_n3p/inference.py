from __future__ import annotations

import json
import math
import pickle
import shutil
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn import __version__ as sklearn_version
from sklearn.neighbors import KDTree

from forest_n3p.features import FeatureConfig, Pose, extract_features, wrap_pi
from forest_n3p.rs_utils import check_reeds_shepp_collision, states_as_tuples
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class KnnLibraryBuildResult:
    output_dir: Path
    feature_shape: tuple[int, int]
    label_shape: tuple[int, int]
    leaf_size: int
    metadata_path: Path
    tree_path: Path


@dataclass(frozen=True)
class NeighborPrediction:
    rank: int
    sample_index: int
    distance: float
    delta_body: Pose
    subgoal_pose: Pose


@dataclass(frozen=True)
class KnnSubgoalLibrary:
    tree: KDTree
    labels: np.ndarray
    feature_mean: np.ndarray
    feature_std: np.ndarray
    metadata: dict[str, Any]
    root: Path | None = None

    @classmethod
    def load(cls, root: str | Path) -> "KnnSubgoalLibrary":
        root_path = Path(root)
        with (root_path / "knn_tree.pkl").open("rb") as f:
            tree = pickle.load(f)
        labels = np.load(root_path / "labels.npy")
        feature_mean = np.load(root_path / "feature_mean.npy")
        feature_std = np.load(root_path / "feature_std.npy")
        metadata = json.loads((root_path / "metadata.json").read_text(encoding="utf-8"))
        return cls(
            tree=tree,
            labels=np.asarray(labels, dtype=np.float32),
            feature_mean=np.asarray(feature_mean, dtype=np.float64),
            feature_std=np.asarray(feature_std, dtype=np.float64),
            metadata=metadata,
            root=root_path,
        )

    @property
    def sample_count(self) -> int:
        return int(self.labels.shape[0])

    @property
    def feature_dim(self) -> int:
        return int(self.feature_mean.shape[0])

    def normalize_feature(self, feature: np.ndarray) -> np.ndarray:
        vector = np.asarray(feature, dtype=np.float64).reshape(-1)
        if vector.shape != self.feature_mean.shape:
            raise ValueError(
                f"feature shape {vector.shape} does not match library shape {self.feature_mean.shape}"
            )
        return ((vector - self.feature_mean) / self.feature_std).astype(np.float32, copy=False)

    def query(
        self,
        feature: np.ndarray,
        *,
        current_pose: Pose,
        k: int,
    ) -> tuple[NeighborPrediction, ...]:
        if self.sample_count <= 0:
            raise ValueError("KNN library is empty")
        query_k = max(1, min(int(k), self.sample_count))
        normalized = self.normalize_feature(feature).reshape(1, -1)
        distances, indices = self.tree.query(normalized, k=query_k)
        out: list[NeighborPrediction] = []
        for rank, (distance, sample_index) in enumerate(zip(distances[0], indices[0], strict=True), start=1):
            delta = tuple(float(v) for v in self.labels[int(sample_index)])
            subgoal = compose_subgoal_pose(current_pose, delta)  # type: ignore[arg-type]
            out.append(
                NeighborPrediction(
                    rank=rank,
                    sample_index=int(sample_index),
                    distance=float(distance),
                    delta_body=subgoal_delta(delta),
                    subgoal_pose=subgoal,
                )
            )
        return tuple(out)


@dataclass(frozen=True)
class InferenceConfig:
    k_neighbors: int = 5
    l_min_m: float = 1.0
    turning_radius_m: float = 1.0
    wheelbase_m: float = 0.6
    rs_sample_step_m: float = 0.1
    theta_bins: int = 72
    collision_padding: float | None = None
    segment_timeout_s: float = 1.0
    segment_max_nodes: int = 2_000
    full_fallback_timeout_s: float = 2.5
    full_fallback_max_nodes: int = 15_000
    no_progress_patience: int = 2
    no_progress_epsilon_m: float = 0.05
    feature_config: FeatureConfig = field(default_factory=FeatureConfig)

    def __post_init__(self) -> None:
        if int(self.k_neighbors) <= 0:
            raise ValueError("k_neighbors must be positive")
        for name in (
            "l_min_m",
            "turning_radius_m",
            "wheelbase_m",
            "rs_sample_step_m",
            "segment_timeout_s",
            "full_fallback_timeout_s",
        ):
            value = float(getattr(self, name))
            if not (math.isfinite(value) and value > 0.0):
                raise ValueError(f"{name} must be finite and positive")
        if int(self.segment_max_nodes) <= 0 or int(self.full_fallback_max_nodes) <= 0:
            raise ValueError("planner node budgets must be positive")
        if int(self.no_progress_patience) <= 0:
            raise ValueError("no_progress_patience must be positive")
        if float(self.no_progress_epsilon_m) < 0.0:
            raise ValueError("no_progress_epsilon_m must be non-negative")


@dataclass(frozen=True)
class InferenceStepRecord:
    step_index: int
    mode: str
    current_pose: Pose
    target_pose: Pose
    neighbor_rank: int | None
    neighbor_distance: float | None
    segment_success: bool
    segment_failure_reason: str | None
    planner_time_s: float
    planner_expansions: int
    distance_to_goal_m: float


@dataclass(frozen=True)
class InferenceResult:
    success: bool
    path: tuple[Pose, ...]
    steps: tuple[InferenceStepRecord, ...]
    failure_reason: str | None
    termination_reason: str | None
    used_f1: int
    used_f2: int
    used_f3: int
    total_time_s: float
    total_planner_time_s: float
    total_expansions: int
    final_distance_to_goal_m: float


def subgoal_delta(values: Iterable[float]) -> Pose:
    raw = tuple(float(v) for v in values)
    if len(raw) != 3:
        raise ValueError("subgoal delta must have exactly three values")
    return raw  # type: ignore[return-value]


def compose_subgoal_pose(current_pose: Pose, delta_body: Pose) -> Pose:
    x, y, theta = (float(v) for v in current_pose)
    dx, dy, dtheta = (float(v) for v in delta_body)
    c = math.cos(theta)
    s = math.sin(theta)
    return (
        float(x + c * dx - s * dy),
        float(y + s * dx + c * dy),
        wrap_pi(theta + dtheta),
    )


def build_knn_library(
    dataset_dir: str | Path,
    output_dir: str | Path,
    *,
    leaf_size: int = 40,
    zscore_epsilon: float = 1e-6,
    source_head: str = "unknown",
    command: str = "unknown",
) -> KnnLibraryBuildResult:
    dataset_path = Path(dataset_dir)
    output_path = Path(output_dir)
    features = np.load(dataset_path / "features.npy").astype(np.float64, copy=False)
    labels = np.load(dataset_path / "labels.npy").astype(np.float32, copy=False)
    if features.ndim != 2 or labels.ndim != 2:
        raise ValueError("features.npy and labels.npy must be 2D arrays")
    if features.shape[0] != labels.shape[0]:
        raise ValueError("features and labels must have the same row count")
    if labels.shape[1] != 3:
        raise ValueError("labels.npy must have shape (N, 3)")
    if features.shape[0] <= 0:
        raise ValueError("training dataset is empty")

    eps = float(zscore_epsilon)
    if not (math.isfinite(eps) and eps > 0.0):
        raise ValueError("zscore_epsilon must be finite and positive")

    output_path.mkdir(parents=True, exist_ok=True)
    feature_mean = np.mean(features, axis=0, dtype=np.float64)
    feature_std = np.std(features, axis=0, dtype=np.float64)
    feature_std = np.where(feature_std < eps, 1.0, feature_std)
    normalized = ((features - feature_mean) / feature_std).astype(np.float32, copy=False)

    tree = KDTree(normalized, leaf_size=int(leaf_size))
    tree_path = output_path / "knn_tree.pkl"
    with tree_path.open("wb") as f:
        pickle.dump(tree, f, protocol=pickle.HIGHEST_PROTOCOL)

    np.save(output_path / "feature_mean.npy", feature_mean.astype(np.float64, copy=False))
    np.save(output_path / "feature_std.npy", feature_std.astype(np.float64, copy=False))
    np.save(output_path / "labels.npy", labels.astype(np.float32, copy=False))
    sample_indices = dataset_path / "sample_query_indices.npy"
    if sample_indices.exists():
        shutil.copy2(sample_indices, output_path / "sample_query_indices.npy")

    source_summary: dict[str, Any] = {}
    summary_path = dataset_path / "summary.json"
    if summary_path.exists():
        source_summary = json.loads(summary_path.read_text(encoding="utf-8"))

    metadata = {
        "task": "T09",
        "model": "KNN-KDTree",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": source_head,
        "command": command,
        "source_dataset_dir": str(dataset_path),
        "feature_shape": list(features.shape),
        "label_shape": list(labels.shape),
        "leaf_size": int(leaf_size),
        "zscore_epsilon": eps,
        "feature_mean_dtype": "float64",
        "feature_std_dtype": "float64",
        "normalized_training_dtype": "float32",
        "sklearn_version": sklearn_version,
        "source_summary": source_summary.get("summary", source_summary),
        "files": {
            "knn_tree": str(tree_path),
            "feature_mean": str(output_path / "feature_mean.npy"),
            "feature_std": str(output_path / "feature_std.npy"),
            "labels": str(output_path / "labels.npy"),
            "sample_query_indices": str(output_path / "sample_query_indices.npy"),
        },
    }
    metadata_path = output_path / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    return KnnLibraryBuildResult(
        output_dir=output_path,
        feature_shape=(int(features.shape[0]), int(features.shape[1])),
        label_shape=(int(labels.shape[0]), int(labels.shape[1])),
        leaf_size=int(leaf_size),
        metadata_path=metadata_path,
        tree_path=tree_path,
    )


def run_forest_n3p(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    library: KnnSubgoalLibrary,
    *,
    config: InferenceConfig | None = None,
) -> InferenceResult:
    cfg = config or InferenceConfig()
    started = time.perf_counter()
    planner = _make_planner(grid_map, footprint, cfg)
    checker = GridFootprintChecker(
        grid_map,
        footprint,
        theta_bins=int(cfg.theta_bins),
        padding=cfg.collision_padding,
    )
    current = _clean_pose(start)
    final_goal = _clean_pose(goal)
    path_out: list[Pose] = [current]
    steps: list[InferenceStepRecord] = []
    total_expansions = 0
    total_planner_time_s = 0.0
    used_f1 = 0
    used_f2 = 0
    used_f3 = 0
    previous_distance = _xy_distance(current, final_goal)
    stall_count = 0
    max_steps = max(1, int(math.ceil((2.0 * previous_distance) / max(float(cfg.l_min_m), 1e-9))))

    for step_index in range(max_steps):
        direct = _try_rs(grid_map, footprint, current, final_goal, cfg)
        if direct is not None:
            _append_poses(path_out, states_as_tuples(direct.samples))
            steps.append(
                InferenceStepRecord(
                    step_index=step_index,
                    mode="direct_rs_goal",
                    current_pose=current,
                    target_pose=final_goal,
                    neighbor_rank=None,
                    neighbor_distance=None,
                    segment_success=True,
                    segment_failure_reason=None,
                    planner_time_s=0.0,
                    planner_expansions=0,
                    distance_to_goal_m=0.0,
                )
            )
            return _result(
                True,
                path_out,
                steps,
                None,
                "direct_rs_goal",
                used_f1,
                used_f2,
                used_f3,
                started,
                total_planner_time_s,
                total_expansions,
                final_goal,
            )

        feature = extract_features(grid_map, current, final_goal, config=cfg.feature_config).vector
        neighbors = library.query(feature, current_pose=current, k=int(cfg.k_neighbors))
        chosen: NeighborPrediction | None = None
        first_prediction = neighbors[0] if neighbors else None
        for candidate in neighbors:
            if candidate.rank > 1:
                used_f1 += 1
            if checker.collides_pose(*candidate.subgoal_pose):
                continue
            candidate_rs = _try_rs(grid_map, footprint, current, candidate.subgoal_pose, cfg)
            if candidate_rs is None:
                continue
            chosen = candidate
            break

        if chosen is None:
            used_f2 += 1
            f2 = _try_f2(
                planner,
                current,
                final_goal,
                first_prediction.subgoal_pose if first_prediction is not None else None,
                path_out,
                step_index,
                steps,
                cfg,
            )
            total_expansions += f2.expansions
            total_planner_time_s += f2.planner_time_s
            if f2.success:
                if f2.reached_goal:
                    return _result(
                        True,
                        path_out,
                        steps,
                        None,
                        f2.mode,
                        used_f1,
                        used_f2,
                        used_f3,
                        started,
                        total_planner_time_s,
                        total_expansions,
                        final_goal,
                    )
                current = path_out[-1]
            else:
                used_f3 += 1
                return _run_f3(
                    planner,
                    start,
                    final_goal,
                    path_out,
                    steps,
                    step_index,
                    cfg,
                    started,
                    total_planner_time_s,
                    total_expansions,
                    used_f1,
                    used_f2,
                    used_f3,
                    f"f2_failed:{f2.failure_reason}",
                )
        else:
            segment = _plan_segment(
                planner,
                current,
                chosen.subgoal_pose,
                timeout_s=float(cfg.segment_timeout_s),
                max_nodes=int(cfg.segment_max_nodes),
            )
            total_expansions += segment.expansions
            total_planner_time_s += segment.planner_time_s
            steps.append(
                InferenceStepRecord(
                    step_index=step_index,
                    mode="knn_segment",
                    current_pose=current,
                    target_pose=chosen.subgoal_pose,
                    neighbor_rank=int(chosen.rank),
                    neighbor_distance=float(chosen.distance),
                    segment_success=bool(segment.success),
                    segment_failure_reason=segment.failure_reason,
                    planner_time_s=float(segment.planner_time_s),
                    planner_expansions=int(segment.expansions),
                    distance_to_goal_m=_xy_distance(chosen.subgoal_pose, final_goal),
                )
            )
            if not segment.success:
                used_f2 += 1
                f2 = _try_f2(
                    planner,
                    current,
                    final_goal,
                    chosen.subgoal_pose,
                    path_out,
                    step_index,
                    steps,
                    cfg,
                )
                total_expansions += f2.expansions
                total_planner_time_s += f2.planner_time_s
                if f2.success:
                    if f2.reached_goal:
                        return _result(
                            True,
                            path_out,
                            steps,
                            None,
                            f2.mode,
                            used_f1,
                            used_f2,
                            used_f3,
                            started,
                            total_planner_time_s,
                            total_expansions,
                            final_goal,
                        )
                    current = path_out[-1]
                else:
                    used_f3 += 1
                    return _run_f3(
                        planner,
                        start,
                        final_goal,
                        path_out,
                        steps,
                        step_index,
                        cfg,
                        started,
                        total_planner_time_s,
                        total_expansions,
                        used_f1,
                        used_f2,
                        used_f3,
                        f"segment_failed:{segment.failure_reason};f2_failed:{f2.failure_reason}",
                    )
            else:
                _append_poses(path_out, segment.poses)
                current = path_out[-1]

        new_distance = _xy_distance(current, final_goal)
        if new_distance < previous_distance - float(cfg.no_progress_epsilon_m):
            stall_count = 0
        else:
            stall_count += 1
        previous_distance = new_distance
        if stall_count >= int(cfg.no_progress_patience):
            used_f3 += 1
            return _run_f3(
                planner,
                start,
                final_goal,
                path_out,
                steps,
                step_index,
                cfg,
                started,
                total_planner_time_s,
                total_expansions,
                used_f1,
                used_f2,
                used_f3,
                "no_progress_sentinel",
            )

    used_f3 += 1
    return _run_f3(
        planner,
        start,
        final_goal,
        path_out,
        steps,
        max_steps,
        cfg,
        started,
        total_planner_time_s,
        total_expansions,
        used_f1,
        used_f2,
        used_f3,
        "max_step_budget",
    )


@dataclass(frozen=True)
class _PlanSegmentResult:
    success: bool
    poses: tuple[Pose, ...]
    failure_reason: str | None
    planner_time_s: float
    expansions: int


@dataclass(frozen=True)
class _F2Result:
    success: bool
    reached_goal: bool
    mode: str
    failure_reason: str | None
    planner_time_s: float
    expansions: int


def _make_planner(grid_map: GridMap, footprint: TwoCircleFootprint, cfg: InferenceConfig) -> HybridAStarPlanner:
    params = AckermannParams(
        wheelbase=float(cfg.wheelbase_m),
        min_turn_radius=float(cfg.turning_radius_m),
    )
    return HybridAStarPlanner(
        grid_map,
        footprint,
        params,
        analytic_expansion=True,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=math.radians(15.0),
        use_holonomic_heuristic=True,
        theta_bins=int(cfg.theta_bins),
        collision_padding=cfg.collision_padding,
    )


def _try_rs(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    cfg: InferenceConfig,
):
    try:
        result = check_reeds_shepp_collision(
            grid_map,
            footprint,
            start,
            goal,
            turning_radius=float(cfg.turning_radius_m),
            wheelbase=float(cfg.wheelbase_m),
            sample_step=float(cfg.rs_sample_step_m),
            theta_bins=int(cfg.theta_bins),
            collision_padding=cfg.collision_padding,
        )
    except RuntimeError:
        return None
    return result if result.collision_free else None


def _plan_segment(
    planner: HybridAStarPlanner,
    start: Pose,
    goal: Pose,
    *,
    timeout_s: float,
    max_nodes: int,
) -> _PlanSegmentResult:
    path, stats = planner.plan(
        AckermannState(*start),
        AckermannState(*goal),
        timeout=float(timeout_s),
        max_nodes=int(max_nodes),
    )
    if not path:
        return _PlanSegmentResult(
            success=False,
            poses=(),
            failure_reason=str(stats.get("failure_reason", "unknown")),
            planner_time_s=float(stats.get("time", 0.0)),
            expansions=int(stats.get("expansions", 0)),
        )
    trace = stats.get("trace_poses")
    poses = tuple((float(x), float(y), float(theta)) for x, y, theta in trace) if trace else states_as_tuples(path)
    return _PlanSegmentResult(
        success=True,
        poses=poses,
        failure_reason=None,
        planner_time_s=float(stats.get("time", 0.0)),
        expansions=int(stats.get("expansions", 0)),
    )


def _try_f2(
    planner: HybridAStarPlanner,
    current: Pose,
    goal: Pose,
    predicted: Pose | None,
    path_out: list[Pose],
    step_index: int,
    steps: list[InferenceStepRecord],
    cfg: InferenceConfig,
) -> _F2Result:
    total_time = 0.0
    total_expansions = 0
    failures: list[str] = []
    if predicted is not None and _xy_distance(current, predicted) > 1e-6:
        segment = _plan_segment(
            planner,
            current,
            predicted,
            timeout_s=float(cfg.segment_timeout_s),
            max_nodes=int(cfg.segment_max_nodes),
        )
        total_time += segment.planner_time_s
        total_expansions += segment.expansions
        steps.append(
            InferenceStepRecord(
                step_index=step_index,
                mode="f2_segment_to_prediction",
                current_pose=current,
                target_pose=predicted,
                neighbor_rank=None,
                neighbor_distance=None,
                segment_success=bool(segment.success),
                segment_failure_reason=segment.failure_reason,
                planner_time_s=float(segment.planner_time_s),
                planner_expansions=int(segment.expansions),
                distance_to_goal_m=_xy_distance(predicted, goal),
            )
        )
        if segment.success:
            _append_poses(path_out, segment.poses)
            return _F2Result(True, False, "f2_segment_to_prediction", None, total_time, total_expansions)
        failures.append(f"prediction:{segment.failure_reason}")

    segment_goal = _plan_segment(
        planner,
        current,
        goal,
        timeout_s=float(cfg.segment_timeout_s),
        max_nodes=int(cfg.segment_max_nodes),
    )
    total_time += segment_goal.planner_time_s
    total_expansions += segment_goal.expansions
    steps.append(
        InferenceStepRecord(
            step_index=step_index,
            mode="f2_limited_goal",
            current_pose=current,
            target_pose=goal,
            neighbor_rank=None,
            neighbor_distance=None,
            segment_success=bool(segment_goal.success),
            segment_failure_reason=segment_goal.failure_reason,
            planner_time_s=float(segment_goal.planner_time_s),
            planner_expansions=int(segment_goal.expansions),
            distance_to_goal_m=0.0 if segment_goal.success else _xy_distance(current, goal),
        )
    )
    if segment_goal.success:
        _append_poses(path_out, segment_goal.poses)
        return _F2Result(True, True, "f2_limited_goal", None, total_time, total_expansions)
    failures.append(f"goal:{segment_goal.failure_reason}")
    return _F2Result(False, False, "f2_failed", ";".join(failures), total_time, total_expansions)


def _run_f3(
    planner: HybridAStarPlanner,
    start: Pose,
    goal: Pose,
    _partial_path: list[Pose],
    steps: list[InferenceStepRecord],
    step_index: int,
    cfg: InferenceConfig,
    started: float,
    total_planner_time_s: float,
    total_expansions: int,
    used_f1: int,
    used_f2: int,
    used_f3: int,
    trigger_reason: str,
) -> InferenceResult:
    segment = _plan_segment(
        planner,
        _clean_pose(start),
        goal,
        timeout_s=float(cfg.full_fallback_timeout_s),
        max_nodes=int(cfg.full_fallback_max_nodes),
    )
    total_planner_time_s += segment.planner_time_s
    total_expansions += segment.expansions
    steps.append(
        InferenceStepRecord(
            step_index=step_index,
            mode="f3_full_query",
            current_pose=_clean_pose(start),
            target_pose=goal,
            neighbor_rank=None,
            neighbor_distance=None,
            segment_success=bool(segment.success),
            segment_failure_reason=segment.failure_reason,
            planner_time_s=float(segment.planner_time_s),
            planner_expansions=int(segment.expansions),
            distance_to_goal_m=0.0 if segment.success else _xy_distance(start, goal),
        )
    )
    if segment.success:
        return _result(
            True,
            list(segment.poses),
            steps,
            None,
            f"f3_full_query:{trigger_reason}",
            used_f1,
            used_f2,
            used_f3,
            started,
            total_planner_time_s,
            total_expansions,
            goal,
        )
    return _result(
        False,
        [],
        steps,
        f"{trigger_reason};f3_failed:{segment.failure_reason}",
        None,
        used_f1,
        used_f2,
        used_f3,
        started,
        total_planner_time_s,
        total_expansions,
        goal,
    )


def _append_poses(path_out: list[Pose], segment: Iterable[Pose]) -> None:
    poses = tuple(_clean_pose(pose) for pose in segment)
    if not poses:
        return
    if not path_out:
        path_out.extend(poses)
        return
    start_idx = 1 if _same_pose(path_out[-1], poses[0]) else 0
    path_out.extend(poses[start_idx:])


def _result(
    success: bool,
    path_out: list[Pose],
    steps: list[InferenceStepRecord],
    failure_reason: str | None,
    termination_reason: str | None,
    used_f1: int,
    used_f2: int,
    used_f3: int,
    started: float,
    total_planner_time_s: float,
    total_expansions: int,
    goal: Pose,
) -> InferenceResult:
    final_pose = path_out[-1] if path_out else (math.nan, math.nan, math.nan)
    return InferenceResult(
        success=bool(success),
        path=tuple(path_out),
        steps=tuple(steps),
        failure_reason=failure_reason,
        termination_reason=termination_reason,
        used_f1=int(used_f1),
        used_f2=int(used_f2),
        used_f3=int(used_f3),
        total_time_s=float(time.perf_counter() - started),
        total_planner_time_s=float(total_planner_time_s),
        total_expansions=int(total_expansions),
        final_distance_to_goal_m=_xy_distance(final_pose, goal),
    )


def _clean_pose(pose: Pose) -> Pose:
    out = (float(pose[0]), float(pose[1]), wrap_pi(float(pose[2])))
    if not all(math.isfinite(v) for v in out):
        raise ValueError(f"pose values must be finite, got {pose!r}")
    return out


def _xy_distance(a: Pose, b: Pose) -> float:
    return float(math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1])))


def _same_pose(a: Pose, b: Pose, *, tol: float = 1e-6) -> bool:
    return (
        abs(float(a[0]) - float(b[0])) <= tol
        and abs(float(a[1]) - float(b[1])) <= tol
        and abs(wrap_pi(float(a[2]) - float(b[2]))) <= tol
    )


def result_to_dict(result: InferenceResult) -> dict[str, Any]:
    payload = asdict(result)
    payload["path"] = [list(pose) for pose in result.path]
    payload["steps"] = [asdict(step) for step in result.steps]
    return payload
