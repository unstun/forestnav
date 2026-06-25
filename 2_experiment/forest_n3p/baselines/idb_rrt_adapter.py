from __future__ import annotations

import ast
import math
import os
import shutil
import subprocess
import time
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from forest_n3p.features import Pose, wrap_pi
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint


@dataclass(frozen=True)
class IdBRrtAdapterAvailability:
    available: bool
    reason: str | None
    binary_path: Path | None = None
    dynoplan_root: Path | None = None
    motion_file: Path | None = None


@dataclass(frozen=True)
class IdBRrtAdapterConfig:
    binary_path: Path | None = None
    dynoplan_root: Path | None = None
    motion_file: Path | None = None
    timeout_s: float = 2.5
    seed: int = 20260620
    artifact_root: Path | None = None
    max_obstacle_boxes: int = 12_000


@dataclass(frozen=True)
class IdBRrtPlanResult:
    success: bool
    path: tuple[Pose, ...]
    failure_reason: str | None
    total_time_s: float
    total_expansions: int
    command: tuple[str, ...] = ()
    run_dir: str | None = None
    returncode: int | None = None
    state_count: int = 0


def check_idb_rrt_adapter(config: IdBRrtAdapterConfig | None = None) -> IdBRrtAdapterAvailability:
    cfg = config or IdBRrtAdapterConfig()
    binary = _find_binary(cfg)
    if binary is None:
        return IdBRrtAdapterAvailability(False, "Dynoplan main_idbastar binary not found")

    dynoplan_root = _find_dynoplan_root(cfg)
    if dynoplan_root is None:
        return IdBRrtAdapterAvailability(False, "Dynoplan root not found", binary_path=binary)

    models_dir = dynoplan_root / "dynobench" / "models"
    if not models_dir.is_dir():
        return IdBRrtAdapterAvailability(
            False,
            f"Dynobench models dir not found: {models_dir}",
            binary_path=binary,
            dynoplan_root=dynoplan_root,
        )

    motion_file = _find_motion_file(cfg, dynoplan_root)
    if motion_file is None:
        return IdBRrtAdapterAvailability(
            False,
            "car1_v0 motion primitive file not found",
            binary_path=binary,
            dynoplan_root=dynoplan_root,
        )
    return IdBRrtAdapterAvailability(True, None, binary_path=binary, dynoplan_root=dynoplan_root, motion_file=motion_file)


def plan_idb_rrt(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    start: Pose,
    goal: Pose,
    *,
    config: IdBRrtAdapterConfig | None = None,
) -> IdBRrtPlanResult:
    cfg = config or IdBRrtAdapterConfig()
    started = time.perf_counter()
    availability = check_idb_rrt_adapter(cfg)
    if not availability.available:
        return IdBRrtPlanResult(
            success=False,
            path=(),
            failure_reason=f"idb_rrt_unavailable:{availability.reason}",
            total_time_s=float(time.perf_counter() - started),
            total_expansions=0,
        )

    assert availability.binary_path is not None
    assert availability.dynoplan_root is not None
    assert availability.motion_file is not None

    run_dir = _run_dir(cfg)
    run_dir.mkdir(parents=True, exist_ok=True)
    env_file = run_dir / "forestnav_car1_v0.yaml"
    cfg_file = run_dir / "idbastar.cfg.yaml"
    result_file = run_dir / "idbastar_result.yaml"
    stdout_file = run_dir / "stdout.txt"
    stderr_file = run_dir / "stderr.txt"

    obstacle_boxes = _occupied_boxes(grid_map, max_boxes=int(cfg.max_obstacle_boxes))
    _write_env_yaml(env_file, grid_map, start, goal, obstacle_boxes)
    _write_cfg_yaml(
        cfg_file,
        motion_file=availability.motion_file,
        timelimit_s=float(cfg.timeout_s),
        seed=int(cfg.seed),
    )

    cmd = (
        str(availability.binary_path),
        "--env_file",
        str(env_file),
        "--models_base_path",
        str(availability.dynoplan_root / "dynobench" / "models") + "/",
        "--results_file",
        str(result_file),
        "--cfg_file",
        str(cfg_file),
    )
    try:
        completed = subprocess.run(
            list(cmd),
            cwd=str(availability.binary_path.parent),
            check=False,
            capture_output=True,
            text=True,
            timeout=max(10.0, float(cfg.timeout_s) + 15.0),
        )
    except subprocess.TimeoutExpired as exc:
        stdout_file.write_text(exc.stdout or "", encoding="utf-8")
        stderr_file.write_text(exc.stderr or "", encoding="utf-8")
        return IdBRrtPlanResult(
            success=False,
            path=(),
            failure_reason="idb_rrt_timeout",
            total_time_s=float(time.perf_counter() - started),
            total_expansions=0,
            command=cmd,
            run_dir=str(run_dir),
        )

    stdout_file.write_text(completed.stdout, encoding="utf-8")
    stderr_file.write_text(completed.stderr, encoding="utf-8")

    traj_file = Path(str(result_file) + ".traj-sol.yaml")
    path: tuple[Pose, ...] = ()
    parse_error: str | None = None
    if traj_file.is_file():
        try:
            path = _parse_traj_solution(traj_file)
        except Exception as exc:  # noqa: BLE001 - recorded in the result.
            parse_error = f"{type(exc).__name__}:{exc}"

    success = bool(completed.returncode == 0 and path)
    if success:
        failure_reason = None
    elif parse_error is not None:
        failure_reason = f"idb_rrt_parse_failed:{parse_error}"
    else:
        failure_reason = f"idb_rrt_failed:returncode={completed.returncode}"
    return IdBRrtPlanResult(
        success=success,
        path=path,
        failure_reason=failure_reason,
        total_time_s=float(time.perf_counter() - started),
        total_expansions=len(path),
        command=cmd,
        run_dir=str(run_dir),
        returncode=int(completed.returncode),
        state_count=len(path),
    )


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_dynoplan_root() -> Path:
    return _project_root() / "2_experiment" / "idb_rrt_strict_repro" / "upstream" / "dynoplan"


def _find_dynoplan_root(config: IdBRrtAdapterConfig) -> Path | None:
    candidates = [
        config.dynoplan_root,
        Path(os.environ["FORESTNAV_DYNOPLAN_ROOT"]) if os.environ.get("FORESTNAV_DYNOPLAN_ROOT") else None,
        _default_dynoplan_root(),
    ]
    for candidate in candidates:
        if candidate is not None and Path(candidate).is_dir():
            return Path(candidate).resolve()
    return None


def _find_binary(config: IdBRrtAdapterConfig) -> Path | None:
    explicit = config.binary_path or (
        Path(os.environ["FORESTNAV_IDB_RRT_BINARY"]) if os.environ.get("FORESTNAV_IDB_RRT_BINARY") else None
    )
    candidates: list[Path | None] = [explicit]
    for name in ("main_idbastar", "dynoplan_main"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    root = _find_dynoplan_root(config) or _default_dynoplan_root()
    candidates.extend(
        [
            root / "build" / "main_idbastar",
            root / "build-release" / "main_idbastar",
            root / "build-macos-conda-link-rpath" / "main_idbastar",
        ]
    )
    for candidate in candidates:
        if candidate is not None and Path(candidate).is_file():
            return Path(candidate).resolve()
    return None


def _find_motion_file(config: IdBRrtAdapterConfig, dynoplan_root: Path) -> Path | None:
    candidates = [
        config.motion_file,
        Path(os.environ["FORESTNAV_IDB_RRT_MOTION_FILE"]) if os.environ.get("FORESTNAV_IDB_RRT_MOTION_FILE") else None,
        dynoplan_root / "dynomotions" / "car1_v0_all.bin.sp.bin.small5000.msgpack",
        dynoplan_root / "dynomotions_full" / "car1_v0_all.bin.sp.bin.msgpack",
        dynoplan_root / "dynobench" / "envs" / "car1_v0" / "motions" / "car1_v0_all.bin.sp.bin.small.msgpack",
    ]
    for candidate in candidates:
        if candidate is not None and Path(candidate).is_file():
            return Path(candidate).resolve()
    return None


def _run_dir(config: IdBRrtAdapterConfig) -> Path:
    root = config.artifact_root or _project_root() / "2_experiment" / "idb_rrt_strict_repro" / "runs" / "forestnav_adapter"
    return Path(root) / f"run_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"


def _write_cfg_yaml(path: Path, *, motion_file: Path, timelimit_s: float, seed: int) -> None:
    payload = {
        "solver_id": 1,
        "search_timelimit": int(round(float(timelimit_s) * 1000.0)),
        "timelimit": float(timelimit_s),
        "use_nigh_nn": True,
        "cost_delta_factor": 1,
        "smooth_traj": True,
        "motionsFile": str(motion_file),
        "num_primitives_0": 400,
        "delta_0": 0.5,
        "delta": 0.5,
        "max_motions_primitives": 20_000,
        "max_it": 3,
        "new_schedule": True,
        "add_primitives_opt": True,
        "max_iter": 100,
        "weight_goal": 200,
        "control_bounds": True,
        "use_warmstart": True,
        "fix_seed": True,
        "seed": int(seed),
    }
    path.write_text(_yaml_mapping(payload), encoding="utf-8")


def _write_env_yaml(
    path: Path,
    grid_map: GridMap,
    start: Pose,
    goal: Pose,
    obstacle_boxes: Sequence[tuple[float, float, float, float]],
) -> None:
    h, w = grid_map.data.shape
    half = 0.5 * float(grid_map.resolution)
    x_min = float(grid_map.origin[0]) - half
    y_min = float(grid_map.origin[1]) - half
    x_max = float(grid_map.origin[0]) + (w - 1) * float(grid_map.resolution) + half
    y_max = float(grid_map.origin[1]) + (h - 1) * float(grid_map.resolution) + half
    lines = [
        "name: forestnav-grid",
        "environment:",
        f"  min: [{x_min:.6f}, {y_min:.6f}]",
        f"  max: [{x_max:.6f}, {y_max:.6f}]",
    ]
    if obstacle_boxes:
        lines.append("  obstacles:")
        for cx, cy, sx, sy in obstacle_boxes:
            lines.extend(
                [
                    "    - type: box",
                    f"      center: [{cx:.6f}, {cy:.6f}]",
                    f"      size: [{sx:.6f}, {sy:.6f}]",
                ]
            )
    else:
        lines.append("  obstacles: []")
    lines.extend(
        [
            "robots:",
            "  - type: car1_v0",
            f"    start: [{float(start[0]):.6f}, {float(start[1]):.6f}, {wrap_pi(float(start[2])):.6f}, {wrap_pi(float(start[2])):.6f}]",
            f"    goal: [{float(goal[0]):.6f}, {float(goal[1]):.6f}, {wrap_pi(float(goal[2])):.6f}, {wrap_pi(float(goal[2])):.6f}]",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _occupied_boxes(grid_map: GridMap, *, max_boxes: int) -> tuple[tuple[float, float, float, float], ...]:
    data = grid_map.data
    h, w = data.shape
    active: dict[tuple[int, int], list[int]] = {}
    finished: list[tuple[int, int, int, int]] = []

    for gy in range(h):
        row_runs = set()
        gx = 0
        while gx < w:
            if not bool(data[gy, gx]):
                gx += 1
                continue
            start_x = gx
            while gx + 1 < w and bool(data[gy, gx + 1]):
                gx += 1
            end_x = gx
            row_runs.add((start_x, end_x))
            if (start_x, end_x) in active and active[(start_x, end_x)][1] == gy - 1:
                active[(start_x, end_x)][1] = gy
            else:
                active[(start_x, end_x)] = [gy, gy]
            gx += 1

        stale = [key for key, span in active.items() if key not in row_runs and span[1] < gy]
        for key in stale:
            y0, y1 = active.pop(key)
            finished.append((key[0], key[1], y0, y1))

    for key, span in active.items():
        finished.append((key[0], key[1], span[0], span[1]))

    if len(finished) > max_boxes:
        finished = finished[:max_boxes]

    boxes = []
    res = float(grid_map.resolution)
    ox, oy = float(grid_map.origin[0]), float(grid_map.origin[1])
    for x0, x1, y0, y1 in finished:
        cx = ox + 0.5 * (float(x0) + float(x1)) * res
        cy = oy + 0.5 * (float(y0) + float(y1)) * res
        sx = max(res, (int(x1) - int(x0) + 1) * res)
        sy = max(res, (int(y1) - int(y0) + 1) * res)
        boxes.append((cx, cy, sx, sy))
    return tuple(boxes)


def _parse_traj_solution(path: Path) -> tuple[Pose, ...]:
    try:
        import yaml  # type: ignore

        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        states = payload.get("states", ()) if isinstance(payload, dict) else ()
        poses = [_state_to_pose(state) for state in states]
        return tuple(pose for pose in poses if pose is not None)
    except ModuleNotFoundError:
        return _parse_traj_solution_without_yaml(path)


def _parse_traj_solution_without_yaml(path: Path) -> tuple[Pose, ...]:
    poses: list[Pose] = []
    in_states = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "states:":
            in_states = True
            continue
        if in_states and stripped and not stripped.startswith("-"):
            break
        if not in_states or not stripped.startswith("-"):
            continue
        raw = stripped[1:].strip()
        state = ast.literal_eval(raw)
        pose = _state_to_pose(state)
        if pose is not None:
            poses.append(pose)
    return tuple(poses)


def _state_to_pose(state: Any) -> Pose | None:
    if not isinstance(state, Sequence) or len(state) < 3:
        return None
    return (float(state[0]), float(state[1]), wrap_pi(float(state[2])))


def _yaml_mapping(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in payload.items():
        if isinstance(value, bool):
            raw = "true" if value else "false"
        elif isinstance(value, str):
            raw = str(value)
        else:
            raw = str(value)
        lines.append(f"{key}: {raw}")
    return "\n".join(lines) + "\n"


__all__ = [
    "IdBRrtAdapterAvailability",
    "IdBRrtAdapterConfig",
    "IdBRrtPlanResult",
    "check_idb_rrt_adapter",
    "plan_idb_rrt",
]
