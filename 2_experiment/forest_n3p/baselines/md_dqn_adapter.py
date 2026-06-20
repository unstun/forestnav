from __future__ import annotations

import importlib
import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from forest_n3p.features import Pose, wrap_pi
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint


@dataclass(frozen=True)
class MdDqnAdapterConfig:
    source_dir: Path | None = None
    checkpoint_path: Path | None = None
    algo: str = "cnn-dqn"
    device: str = "cpu"
    seed: int = 20260620
    max_steps: int = 600
    sensor_range_m: float = 6.0
    n_sectors: int = 36
    obs_map_size: int = 12
    goal_tolerance_m: float = 0.30
    goal_speed_tol_m_s: float = 999.0
    edt_collision_margin: str = "diag"
    scalar_only: bool = False
    include_action_mask_obs: bool = False
    forest_adm_horizon: int = 15
    forest_topk: int = 10
    forest_min_od_m: float = 0.0
    forest_min_progress_m: float = 1e-4
    time_mode: str = "policy"


@dataclass(frozen=True)
class MdDqnAdapterAvailability:
    available: bool
    reason: str | None
    source_dir: Path | None
    checkpoint_path: Path | None


@dataclass(frozen=True)
class MdDqnPlanResult:
    success: bool
    path: tuple[Pose, ...]
    failure_reason: str | None
    total_time_s: float
    total_expansions: int
    rollout_steps: int
    reached: bool


def check_md_dqn_adapter(config: MdDqnAdapterConfig) -> MdDqnAdapterAvailability:
    source_dir = _resolve_source_dir(config.source_dir)
    checkpoint_path = _resolve_checkpoint_path(config.checkpoint_path)
    if source_dir is None:
        return MdDqnAdapterAvailability(
            available=False,
            reason=(
                "md_dqn_source_dir is not set and FORESTNAV_MD_DQN_SOURCE_DIR is not defined; "
                "expected a DQN10 2_experiment directory containing ugv_dqn"
            ),
            source_dir=None,
            checkpoint_path=checkpoint_path,
        )
    if not (source_dir / "ugv_dqn" / "cli" / "infer.py").exists():
        return MdDqnAdapterAvailability(
            available=False,
            reason=f"source_dir does not contain ugv_dqn/cli/infer.py: {source_dir}",
            source_dir=source_dir,
            checkpoint_path=checkpoint_path,
        )
    if checkpoint_path is None:
        return MdDqnAdapterAvailability(
            available=False,
            reason="md_dqn_checkpoint_path is not set",
            source_dir=source_dir,
            checkpoint_path=None,
        )
    if not checkpoint_path.exists():
        return MdDqnAdapterAvailability(
            available=False,
            reason=f"md_dqn checkpoint does not exist: {checkpoint_path}",
            source_dir=source_dir,
            checkpoint_path=checkpoint_path,
        )
    return MdDqnAdapterAvailability(
        available=True,
        reason=None,
        source_dir=source_dir,
        checkpoint_path=checkpoint_path,
    )


def plan_md_dqn(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    *,
    config: MdDqnAdapterConfig,
) -> MdDqnPlanResult:
    started = time.perf_counter()
    availability = check_md_dqn_adapter(config)
    if not availability.available:
        return MdDqnPlanResult(
            success=False,
            path=(),
            failure_reason=f"md_dqn_unavailable:{availability.reason}",
            total_time_s=float(time.perf_counter() - started),
            total_expansions=0,
            rollout_steps=0,
            reached=False,
        )

    try:
        modules = _import_dqn10_modules(availability.source_dir)
        map_spec = _make_array_grid_spec(modules["maps"], grid_map, start, goal)
        env = modules["env"].UGVBicycleEnv(
            map_spec,
            max_steps=int(config.max_steps),
            cell_size_m=float(grid_map.resolution),
            footprint=modules["env"].TwoCircleFootprint(),
            sensor_range_m=float(config.sensor_range_m),
            n_sectors=int(config.n_sectors),
            obs_map_size=int(config.obs_map_size),
            goal_tolerance_m=float(config.goal_tolerance_m),
            goal_speed_tol_m_s=float(config.goal_speed_tol_m_s),
            edt_collision_margin=str(config.edt_collision_margin),
            scalar_only=bool(config.scalar_only),
            include_action_mask_obs=bool(config.include_action_mask_obs),
        )
        obs_dim = int(env.observation_space.shape[0])
        n_actions = int(env.action_space.n)
        agent = modules["agents"].DQNFamilyAgent(
            str(config.algo),
            obs_dim,
            n_actions,
            config=modules["agents"].AgentConfig(),
            seed=int(config.seed),
            device=str(config.device),
        )
        agent.load(availability.checkpoint_path)
        rollout = modules["infer"].rollout_agent(
            env,
            agent,
            max_steps=int(config.max_steps),
            seed=int(config.seed),
            reset_options={
                "start_xy": _world_pose_to_cell_xy(grid_map, start),
                "goal_xy": _world_pose_to_cell_xy(grid_map, goal),
                "start_heading_rad": float(start[2]),
                "goal_heading_rad": float(goal[2]),
            },
            time_mode=str(config.time_mode),
            obs_transform=None,
            forest_adm_horizon=int(config.forest_adm_horizon),
            forest_topk=int(config.forest_topk),
            forest_min_od_m=float(config.forest_min_od_m),
            forest_min_progress_m=float(config.forest_min_progress_m),
            collect_controls=False,
            collect_trace=True,
        )
        path = poses_from_md_dqn_rollout(rollout, grid_map)
        reached = bool(getattr(rollout, "reached", False))
        return MdDqnPlanResult(
            success=bool(reached and path),
            path=path,
            failure_reason=None if bool(reached and path) else "md_dqn_not_reached",
            total_time_s=float(getattr(rollout, "compute_time_s", time.perf_counter() - started)),
            total_expansions=int(getattr(rollout, "steps", 0)),
            rollout_steps=int(getattr(rollout, "steps", 0)),
            reached=reached,
        )
    except Exception as exc:  # noqa: BLE001 - surfaced as an evaluation failure reason.
        return MdDqnPlanResult(
            success=False,
            path=(),
            failure_reason=f"md_dqn_exception:{type(exc).__name__}:{exc}",
            total_time_s=float(time.perf_counter() - started),
            total_expansions=0,
            rollout_steps=0,
            reached=False,
        )


def poses_from_md_dqn_rollout(rollout: Any, grid_map: GridMap) -> tuple[Pose, ...]:
    trace_rows = getattr(rollout, "trace_rows", None)
    if trace_rows:
        return tuple(_trace_row_to_pose(row, grid_map) for row in trace_rows)
    return poses_from_md_dqn_cells(getattr(rollout, "path_xy_cells", ()), grid_map)


def poses_from_md_dqn_cells(path_xy_cells: Sequence[Sequence[float]], grid_map: GridMap) -> tuple[Pose, ...]:
    cells = tuple((float(item[0]), float(item[1])) for item in path_xy_cells)
    if not cells:
        return ()
    poses: list[Pose] = []
    for index, (cell_x, cell_y) in enumerate(cells):
        if index + 1 < len(cells):
            nx, ny = cells[index + 1]
            theta = math.atan2(float(ny) - float(cell_y), float(nx) - float(cell_x))
        elif poses:
            theta = poses[-1][2]
        else:
            theta = 0.0
        poses.append(
            (
                float(cell_x) * float(grid_map.resolution) + float(grid_map.origin[0]),
                float(cell_y) * float(grid_map.resolution) + float(grid_map.origin[1]),
                wrap_pi(float(theta)),
            )
        )
    return tuple(poses)


def _resolve_source_dir(raw: Path | None) -> Path | None:
    value = raw
    if value is None:
        env_value = os.environ.get("FORESTNAV_MD_DQN_SOURCE_DIR", "").strip()
        value = Path(env_value) if env_value else None
    if value is None:
        return None
    path = Path(value).expanduser().resolve()
    if (path / "ugv_dqn").exists():
        return path
    if (path / "2_experiment" / "ugv_dqn").exists():
        return (path / "2_experiment").resolve()
    return path


def _resolve_checkpoint_path(raw: Path | None) -> Path | None:
    if raw is None:
        env_value = os.environ.get("FORESTNAV_MD_DQN_CHECKPOINT", "").strip()
        return Path(env_value).expanduser().resolve() if env_value else None
    return Path(raw).expanduser().resolve()


def _import_dqn10_modules(source_dir: Path | None) -> dict[str, Any]:
    if source_dir is None:
        raise RuntimeError("source_dir is required")
    source = str(Path(source_dir).resolve())
    if source not in sys.path:
        sys.path.insert(0, source)
    importlib.invalidate_caches()
    return {
        "agents": importlib.import_module("ugv_dqn.agents"),
        "env": importlib.import_module("ugv_dqn.env"),
        "infer": importlib.import_module("ugv_dqn.cli.infer"),
        "maps": importlib.import_module("ugv_dqn.maps"),
    }


def _make_array_grid_spec(maps_module: Any, grid_map: GridMap, start: Pose, goal: Pose) -> Any:
    start_xy = _world_pose_to_cell_xy(grid_map, start)
    goal_xy = _world_pose_to_cell_xy(grid_map, goal)
    data = np.asarray(grid_map.data, dtype=np.uint8)
    return maps_module.ArrayGridMapSpec(
        name="forestnav_t14_query",
        grid_y0_bottom=data.copy(),
        start_xy=start_xy,
        goal_xy=goal_xy,
    )


def _world_pose_to_cell_xy(grid_map: GridMap, pose: Pose) -> tuple[int, int]:
    gx, gy = grid_map.world_to_grid(float(pose[0]), float(pose[1]))
    if not grid_map.in_bounds(int(gx), int(gy)):
        raise ValueError(f"pose is outside grid map: ({pose[0]}, {pose[1]}) -> ({gx}, {gy})")
    return int(gx), int(gy)


def _trace_row_to_pose(row: dict[str, Any], grid_map: GridMap) -> Pose:
    return (
        float(row["x_m"]) + float(grid_map.origin[0]),
        float(row["y_m"]) + float(grid_map.origin[1]),
        wrap_pi(float(row["theta_rad"])),
    )
