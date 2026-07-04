from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, Sequence

import numpy as np
import pandas as pd

from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _generate_grid_map,
    _profile_by_name,
    build_query_set,
    validation_main_evaluation_profiles,
)
from forest_n3p.rl_rs.env import AnalyticExpansionContext
from forest_n3p.rl_rs.obs import ObservationConfig
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class CurriculumContextConfig:
    params: AckermannParams = field(default_factory=AckermannParams)
    footprint: TwoCircleFootprint = field(
        default_factory=lambda: TwoCircleFootprint.from_box(length=0.924, width=0.740)
    )
    max_steps: int = 32
    action_step_m: float = 0.3
    collision_sample_step_m: float = 0.1
    terminal_check_every: int = 1
    theta_bins: int = 72
    observation_config: ObservationConfig = field(default_factory=ObservationConfig)


@dataclass(frozen=True)
class CurriculumSampleMetadata:
    stage: str
    source: str
    row_index: int | None = None
    query_id: str | None = None
    difficulty_bucket: str | None = None
    profile_name: str | None = None
    map_seed: int | None = None
    query_seed: int | None = None
    distance_bin_key: str | None = None
    expansion_idx: int | None = None
    nearest_obstacle_m: float | None = None
    oracle_connectable: bool | None = None

    def to_record(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "source": self.source,
            "row_index": self.row_index,
            "query_id": self.query_id,
            "difficulty_bucket": self.difficulty_bucket,
            "profile_name": self.profile_name,
            "map_seed": self.map_seed,
            "query_seed": self.query_seed,
            "distance_bin_key": self.distance_bin_key,
            "expansion_idx": self.expansion_idx,
            "nearest_obstacle_m": self.nearest_obstacle_m,
            "oracle_connectable": self.oracle_connectable,
        }


class CurriculumSampler(Protocol):
    last_metadata: CurriculumSampleMetadata | None

    def __call__(self, rng: np.random.Generator) -> AnalyticExpansionContext:
        ...


class OpenConnectorContextSampler:
    def __init__(self, *, config: CurriculumContextConfig | None = None, grid_cells: int = 80) -> None:
        self.config = config or CurriculumContextConfig()
        self.grid_cells = int(grid_cells)
        self.last_metadata: CurriculumSampleMetadata | None = None

    def __call__(self, rng: np.random.Generator) -> AnalyticExpansionContext:
        grid_map = _empty_grid(self.grid_cells)
        start, goal = _sample_open_start_goal(rng, grid_map, self.config)
        self.last_metadata = CurriculumSampleMetadata(stage="open_connector", source="procedural_empty_grid")
        return _build_context(grid_map, start, goal, self.config)


class ObstacleBypassContextSampler:
    def __init__(self, *, config: CurriculumContextConfig | None = None, grid_cells: int = 80) -> None:
        self.config = config or CurriculumContextConfig()
        self.grid_cells = int(grid_cells)
        self.last_metadata: CurriculumSampleMetadata | None = None

    def __call__(self, rng: np.random.Generator) -> AnalyticExpansionContext:
        grid_map = _empty_grid(self.grid_cells)
        y = 0.5 * self.grid_cells * float(grid_map.resolution)
        side = -1.0 if float(rng.random()) < 0.5 else 1.0
        start = AckermannState(1.5, y, 0.0)
        goal = AckermannState(6.3, y, 0.0)
        _paint_obstacle_block(
            grid_map,
            x_min_m=2.3,
            x_max_m=2.9,
            y_min_m=y + side * 0.35,
            y_max_m=y + side * 1.05,
        )
        nearest = _nearest_occupied_distance_m(grid_map, start.x, start.y)
        self.last_metadata = CurriculumSampleMetadata(
            stage="obstacle_bypass",
            source="procedural_single_side_obstacle",
            nearest_obstacle_m=nearest,
        )
        return _build_context(grid_map, start, goal, self.config)


class OracleConnectorContextSampler:
    def __init__(
        self,
        path: str | Path,
        *,
        config: CurriculumContextConfig | None = None,
        buckets: Sequence[str] = ("Complex", "Extreme"),
        stage: str = "rs_failure_node",
        only_connectable: bool = True,
        max_rows: int | None = None,
    ) -> None:
        self.path = Path(path)
        self.config = config or CurriculumContextConfig()
        self.stage = str(stage)
        self.rows = _load_oracle_rows(self.path, buckets=tuple(buckets), only_connectable=bool(only_connectable))
        if max_rows is not None:
            self.rows = self.rows.head(int(max_rows)).copy()
        if self.rows.empty:
            raise ValueError(f"no oracle connector rows available from {self.path}")
        self.eval_config = _evaluation_config()
        self._map_cache: dict[tuple[str, int], GridMap] = {}
        self.last_metadata: CurriculumSampleMetadata | None = None
        self.skipped_invalid_rows = 0
        self.last_invalid_metadata: CurriculumSampleMetadata | None = None

    def __call__(self, rng: np.random.Generator) -> AnalyticExpansionContext:
        max_attempts = max(32, 2 * len(self.rows))
        for _ in range(max_attempts):
            position = int(rng.integers(0, len(self.rows)))
            row = self.rows.iloc[position]
            grid_map = self._grid_for_row(row)
            start = AckermannState(
                float(_row_value(row, "state_x", "current_x")),
                float(_row_value(row, "state_y", "current_y")),
                float(_row_value(row, "state_theta", "current_theta")),
            )
            goal = AckermannState(float(row["goal_x"]), float(row["goal_y"]), float(row["goal_theta"]))
            metadata = _metadata_from_row(
                row,
                stage=self.stage,
                source=str(self.path),
                row_index=int(row.name),
            )
            try:
                context = _build_context(grid_map, start, goal, self.config)
            except ValueError as exc:
                if "sampled curriculum" not in str(exc):
                    raise
                self.skipped_invalid_rows += 1
                self.last_invalid_metadata = metadata
                continue
            self.last_metadata = metadata
            return context
        raise RuntimeError(f"failed to sample valid oracle connector context after {max_attempts} attempts")

    def _grid_for_row(self, row: Any) -> GridMap:
        key = (str(row["profile_name"]), int(row["map_seed"]))
        cached = self._map_cache.get(key)
        if cached is not None:
            return cached
        profile = _profile_by_name(self.eval_config.profiles, key[0])
        grid_map = _generate_grid_map(profile, key[1], self.eval_config, self.config.footprint)
        self._map_cache[key] = grid_map
        return grid_map


class HeldoutQueryContextSampler:
    def __init__(
        self,
        *,
        seed: int,
        config: CurriculumContextConfig | None = None,
        buckets: Sequence[str] = ("Complex", "Extreme"),
        queries_per_bucket: int = 10,
        seed_count: int = 1,
        queries_per_map: int = 5,
    ) -> None:
        self.config = config or CurriculumContextConfig()
        self.eval_config = _evaluation_config(
            seed=int(seed),
            queries_per_bucket=int(queries_per_bucket),
            seed_count=int(seed_count),
            queries_per_map=int(queries_per_map),
        )
        requested = {str(bucket) for bucket in buckets}
        self.queries = tuple(query for query in build_query_set(self.eval_config) if query.difficulty_bucket in requested)
        if not self.queries:
            raise ValueError("heldout query sampler has no queries after bucket filtering")
        self._map_cache: dict[tuple[str, int], GridMap] = {}
        self.last_metadata: CurriculumSampleMetadata | None = None

    def __call__(self, rng: np.random.Generator) -> AnalyticExpansionContext:
        query = self.queries[int(rng.integers(0, len(self.queries)))]
        grid_map = self._grid_for_query(query)
        self.last_metadata = CurriculumSampleMetadata(
            stage="heldout_procedural",
            source="main_evaluation_build_query_set",
            query_id=query.query_id,
            difficulty_bucket=query.difficulty_bucket,
            profile_name=query.profile_name,
            map_seed=int(query.map_seed),
            query_seed=int(query.query_seed),
            distance_bin_key=query.distance_bin_key,
        )
        return _build_context(
            grid_map,
            AckermannState(*query.start),
            AckermannState(*query.goal),
            self.config,
        )

    def _grid_for_query(self, query: Any) -> GridMap:
        key = (str(query.profile_name), int(query.map_seed))
        cached = self._map_cache.get(key)
        if cached is not None:
            return cached
        profile = _profile_by_name(self.eval_config.profiles, key[0])
        grid_map = _generate_grid_map(profile, key[1], self.eval_config, self.config.footprint)
        self._map_cache[key] = grid_map
        return grid_map


class WeightedCurriculumContextSampler:
    def __init__(self, *, stages: Sequence[CurriculumSampler], weights: Sequence[float]) -> None:
        if len(stages) != len(weights):
            raise ValueError("stages and weights must have the same length")
        if not stages:
            raise ValueError("at least one curriculum stage is required")
        weight_array = np.asarray(weights, dtype=np.float64)
        if (
            not np.all(np.isfinite(weight_array))
            or np.any(weight_array < 0.0)
            or float(np.sum(weight_array)) <= 0.0
        ):
            raise ValueError("curriculum weights must be finite non-negative values with positive sum")
        self.stages = tuple(stages)
        self.weights = weight_array / float(np.sum(weight_array))
        self.last_metadata: CurriculumSampleMetadata | None = None

    def __call__(self, rng: np.random.Generator) -> AnalyticExpansionContext:
        index = int(rng.choice(len(self.stages), p=self.weights))
        sampler = self.stages[index]
        context = sampler(rng)
        self.last_metadata = sampler.last_metadata
        return context


def make_f03_curriculum_sampler(
    *,
    oracle_path: str | Path = "0_trials/module2_oracle_shape/oracle_connector_results.parquet",
    heldout_seed: int = 20260704,
    config: CurriculumContextConfig | None = None,
) -> WeightedCurriculumContextSampler:
    cfg = config or CurriculumContextConfig()
    return WeightedCurriculumContextSampler(
        stages=(
            OpenConnectorContextSampler(config=cfg),
            ObstacleBypassContextSampler(config=cfg),
            OracleConnectorContextSampler(oracle_path, config=cfg),
            HeldoutQueryContextSampler(seed=int(heldout_seed), config=cfg),
        ),
        weights=(1.0, 1.0, 2.0, 1.0),
    )


def _evaluation_config(
    *,
    seed: int = 20260620,
    queries_per_bucket: int = 10,
    seed_count: int = 1,
    queries_per_map: int = 5,
) -> MainEvaluationConfig:
    return MainEvaluationConfig(
        seed=int(seed),
        queries_per_bucket=int(queries_per_bucket),
        seed_count=int(seed_count),
        queries_per_map=int(queries_per_map),
        profiles=validation_main_evaluation_profiles(),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )


def _build_context(
    grid_map: GridMap,
    start: AckermannState,
    goal: AckermannState,
    config: CurriculumContextConfig,
) -> AnalyticExpansionContext:
    checker = GridFootprintChecker(grid_map, config.footprint, theta_bins=int(config.theta_bins))
    if checker.collides_pose(start.x, start.y, start.theta):
        raise ValueError("sampled curriculum start state is in collision")
    if checker.collides_pose(goal.x, goal.y, goal.theta):
        raise ValueError("sampled curriculum goal state is in collision")
    return AnalyticExpansionContext(
        grid_map=grid_map,
        footprint=config.footprint,
        start=start,
        goal=goal,
        params=config.params,
        checker=checker,
        max_steps=int(config.max_steps),
        action_step_m=float(config.action_step_m),
        collision_sample_step_m=float(config.collision_sample_step_m),
        terminal_check_every=int(config.terminal_check_every),
        theta_bins=int(config.theta_bins),
        observation_config=config.observation_config,
    )


def _empty_grid(cells: int) -> GridMap:
    return GridMap(np.zeros((int(cells), int(cells)), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))


def _sample_open_start_goal(
    rng: np.random.Generator,
    grid_map: GridMap,
    config: CurriculumContextConfig,
) -> tuple[AckermannState, AckermannState]:
    checker = GridFootprintChecker(grid_map, config.footprint, theta_bins=int(config.theta_bins))
    max_x = float(grid_map.data.shape[1] - 1) * float(grid_map.resolution)
    max_y = float(grid_map.data.shape[0] - 1) * float(grid_map.resolution)
    margin = 1.5
    for _ in range(100):
        theta = float(rng.uniform(-math.pi, math.pi))
        distance = float(rng.uniform(1.2, 3.0))
        start = AckermannState(
            float(rng.uniform(margin, max_x - margin)),
            float(rng.uniform(margin, max_y - margin)),
            theta,
        )
        goal = AckermannState(
            float(start.x + distance * math.cos(theta)),
            float(start.y + distance * math.sin(theta)),
            theta,
        )
        if (
            margin <= goal.x <= max_x - margin
            and margin <= goal.y <= max_y - margin
            and not checker.collides_pose(start.x, start.y, start.theta)
            and not checker.collides_pose(goal.x, goal.y, goal.theta)
        ):
            return start, goal
    raise RuntimeError("failed to sample open connector context")


def _paint_obstacle_block(
    grid_map: GridMap,
    *,
    x_min_m: float,
    x_max_m: float,
    y_min_m: float,
    y_max_m: float,
) -> None:
    x0, y0 = grid_map.world_to_grid(float(x_min_m), min(float(y_min_m), float(y_max_m)))
    x1, y1 = grid_map.world_to_grid(float(x_max_m), max(float(y_min_m), float(y_max_m)))
    h, w = grid_map.data.shape
    grid_map.data[max(0, y0) : min(h, y1 + 1), max(0, x0) : min(w, x1 + 1)] = 1


def _nearest_occupied_distance_m(grid_map: GridMap, x: float, y: float) -> float | None:
    occupied = np.argwhere(np.asarray(grid_map.data) > 0)
    if occupied.size == 0:
        return None
    gx, gy = grid_map.world_to_grid(float(x), float(y))
    dx = (occupied[:, 1].astype(np.float64) - float(gx)) * float(grid_map.resolution)
    dy = (occupied[:, 0].astype(np.float64) - float(gy)) * float(grid_map.resolution)
    return float(np.min(np.hypot(dx, dy)))


def _load_oracle_rows(
    path: Path,
    *,
    buckets: tuple[str, ...],
    only_connectable: bool,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = pd.read_parquet(path)
    if "difficulty_bucket" in rows.columns:
        rows = rows[rows["difficulty_bucket"].isin(buckets)]
    if only_connectable and "oracle_connectable" in rows.columns:
        rows = rows[rows["oracle_connectable"].astype(bool)]
    return rows.reset_index(drop=True)


def _row_value(row: Any, primary: str, fallback: str) -> Any:
    if primary in row.index:
        return row[primary]
    return row[fallback]


def _metadata_from_row(row: Any, *, stage: str, source: str, row_index: int) -> CurriculumSampleMetadata:
    return CurriculumSampleMetadata(
        stage=stage,
        source=source,
        row_index=int(row_index),
        query_id=None if "query_id" not in row.index else str(row["query_id"]),
        difficulty_bucket=None if "difficulty_bucket" not in row.index else str(row["difficulty_bucket"]),
        profile_name=None if "profile_name" not in row.index else str(row["profile_name"]),
        map_seed=None if "map_seed" not in row.index else int(row["map_seed"]),
        query_seed=None if "query_seed" not in row.index else int(row["query_seed"]),
        distance_bin_key=None if "distance_bin_key" not in row.index else str(row["distance_bin_key"]),
        expansion_idx=None if "expansion_idx" not in row.index else int(row["expansion_idx"]),
        nearest_obstacle_m=None if "nearest_obstacle_m" not in row.index else float(row["nearest_obstacle_m"]),
        oracle_connectable=None if "oracle_connectable" not in row.index else bool(row["oracle_connectable"]),
    )
