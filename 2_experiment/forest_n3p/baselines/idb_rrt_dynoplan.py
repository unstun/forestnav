"""External Dynoplan / Dynobench adapter for the iDb-RRT baseline."""
from __future__ import annotations

import json
import math
import os
import shlex
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import numpy as np

from forest_n3p.baselines.common import PlannerResult, default_start_theta


_VARIANT = "idb_rrt_dynoplan"
_EXTERNAL_IMPL = "dynoplan"
_DEFAULT_FOOTPRINT_LENGTH_M = 0.924
_DEFAULT_FOOTPRINT_WIDTH_M = 0.740
_PAYLOAD_STAT_KEYS = (
    "dynoplan_planner",
    "dynoplan_robot_type",
    "dynoplan_footprint_scale",
    "dynoplan_use_paper_defaults",
    "dynoplan_solution_stage",
    "dynoplan_to_success",
    "env_file",
    "cfg_file",
    "result_file",
    "traj_file",
)


def _env_or_arg(value: str | os.PathLike[str] | None, env_name: str) -> str:
    if value is None:
        return str(os.environ.get(env_name, "")).strip()
    return str(value).strip()


def _resolve_executable(executable: str) -> str | None:
    executable = str(executable).strip()
    if not executable:
        return None
    if os.sep in executable or (os.altsep and os.altsep in executable):
        path = Path(executable).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
        return None
    resolved = shutil.which(executable)
    return str(resolved) if resolved else None


def _vehicle_params(params: Any) -> dict[str, float]:
    wheelbase_m = float(getattr(params, "wheelbase", 0.6))
    v_max_m_s = float(getattr(params, "v_max", 2.0))
    min_turn_radius_m = float(getattr(params, "min_turn_radius", 0.0) or 0.0)

    max_steer = getattr(params, "max_steer", None)
    if max_steer is None:
        if min_turn_radius_m > 0.0:
            max_steer_rad = math.atan(wheelbase_m / min_turn_radius_m)
        else:
            max_steer_rad = math.radians(27.0)
    else:
        max_steer_rad = float(max_steer)

    if not (min_turn_radius_m > 0.0):
        min_turn_radius_m = wheelbase_m / max(1e-9, math.tan(max_steer_rad))

    return {
        "wheelbase_m": float(wheelbase_m),
        "max_steer_rad": float(max_steer_rad),
        "v_max_m_s": float(v_max_m_s),
        "min_turn_radius_m": float(min_turn_radius_m),
    }


def _footprint_size(footprint: Any) -> tuple[float, float]:
    if type(footprint).__name__ == "OrientedBoxFootprint":
        length = float(getattr(footprint, "length", _DEFAULT_FOOTPRINT_LENGTH_M))
        width = float(getattr(footprint, "width", _DEFAULT_FOOTPRINT_WIDTH_M))
        if length > 0.0 and width > 0.0:
            return length, width
    return _DEFAULT_FOOTPRINT_LENGTH_M, _DEFAULT_FOOTPRINT_WIDTH_M


def _build_problem_json(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    start_theta_rad: float | None,
    goal_theta_rad: float,
    goal_xy_tol_m: float,
    dynoplan_root: str,
) -> tuple[dict[str, Any], dict[str, float]]:
    cell_size_m = float(getattr(grid_map, "resolution", 1.0))
    vehicle = _vehicle_params(params)
    footprint_length_m, footprint_width_m = _footprint_size(footprint)
    if start_theta_rad is None:
        start_theta = default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    else:
        start_theta = float(start_theta_rad)

    grid = np.asarray(getattr(grid_map, "data"), dtype=np.uint8)
    occupancy_grid = (grid > 0).astype(int).tolist()

    start_m = [float(start_xy[0]) * cell_size_m, float(start_xy[1]) * cell_size_m]
    goal_m = [float(goal_xy[0]) * cell_size_m, float(goal_xy[1]) * cell_size_m]
    problem = {
        "adapter": {
            "variant": _VARIANT,
            "external_impl": _EXTERNAL_IMPL,
            "dynoplan_root": dynoplan_root,
        },
        "vehicle": vehicle,
        "footprint": {
            "length_m": float(footprint_length_m),
            "width_m": float(footprint_width_m),
        },
        "map": {
            "cell_size_m": cell_size_m,
            "origin": list(getattr(grid_map, "origin", (0.0, 0.0))),
            "height": int(grid.shape[0]),
            "width": int(grid.shape[1]),
            "occupancy_grid": occupancy_grid,
        },
        "start": {
            "cell": [int(start_xy[0]), int(start_xy[1])],
            "meter": start_m,
            "theta_rad": float(start_theta),
        },
        "goal": {
            "cell": [int(goal_xy[0]), int(goal_xy[1])],
            "meter": goal_m,
            "theta_rad": float(goal_theta_rad),
            "xy_tol_m": float(goal_xy_tol_m),
        },
    }
    exported = {
        **vehicle,
        "footprint_length_m": float(footprint_length_m),
        "footprint_width_m": float(footprint_width_m),
        "cell_size_m": float(cell_size_m),
    }
    return problem, exported


def _path_xy_m_from_payload(payload: Any) -> list[tuple[float, float]]:
    if not isinstance(payload, dict):
        raise ValueError("solution JSON must be an object")

    if "path_xy_m" in payload:
        raw_path = payload["path_xy_m"]
        return [(float(p[0]), float(p[1])) for p in raw_path]

    if "states" in payload:
        raw_states = payload["states"]
        return [(float(s["x"]), float(s["y"])) for s in raw_states]

    if "trajectory" in payload:
        raw_traj = payload["trajectory"]
        return [(float(p[0]), float(p[1])) for p in raw_traj]

    raise ValueError("solution JSON missing path_xy_m, states, or trajectory")


def _stats_base(
    *,
    dynoplan_bin: str,
    dynoplan_root: str,
    dynoplan_cmd_template: str,
    exported: dict[str, float],
) -> dict[str, Any]:
    return {
        "variant": _VARIANT,
        "external_impl": _EXTERNAL_IMPL,
        "dependency_available": False,
        "status": "missing_dynoplan",
        "dynoplan_bin": dynoplan_bin,
        "dynoplan_root": dynoplan_root,
        "dynoplan_cmd_template": dynoplan_cmd_template,
        "wheelbase_m": exported.get("wheelbase_m", ""),
        "max_steer_rad": exported.get("max_steer_rad", ""),
        "v_max_m_s": exported.get("v_max_m_s", ""),
        "min_turn_radius_m": exported.get("min_turn_radius_m", ""),
        "footprint_length_m": exported.get("footprint_length_m", ""),
        "footprint_width_m": exported.get("footprint_width_m", ""),
        "external_returncode": "",
        "external_runtime_s": 0.0,
    }


def _format_command(
    *,
    dynoplan_bin: str,
    dynoplan_cmd_template: str,
    problem_path: Path,
    output_path: Path,
    timeout_s: float,
    seed: int,
) -> tuple[list[str] | None, str | None]:
    if dynoplan_cmd_template:
        command = dynoplan_cmd_template.format(
            problem=str(problem_path),
            output=str(output_path),
            timeout=str(float(timeout_s)),
            seed=str(int(seed)),
        )
        argv = shlex.split(command)
        if not argv:
            return None, None
        resolved = _resolve_executable(argv[0])
        if resolved is None:
            return None, None
        argv[0] = resolved
        return argv, resolved

    resolved = _resolve_executable(dynoplan_bin)
    if resolved is None:
        return None, None
    return [
        resolved,
        "--problem",
        str(problem_path),
        "--output",
        str(output_path),
        "--timeout",
        str(float(timeout_s)),
        "--seed",
        str(int(seed)),
    ], resolved


def _cleanup_artifacts(problem_path: Path, output_path: Path) -> None:
    for path in (problem_path, output_path):
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def plan_idb_rrt_dynoplan(
    *,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float = 0.5,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 60.0,
    seed: int = 0,
    dynoplan_bin: str | os.PathLike[str] | None = None,
    dynoplan_cmd_template: str | None = None,
    dynoplan_root: str | os.PathLike[str] | None = None,
    work_dir: str | os.PathLike[str] | None = None,
    keep_artifacts: bool = False,
) -> PlannerResult:
    """Run external Dynoplan and convert its output into ``PlannerResult``."""
    del goal_theta_tol_rad
    started = time.perf_counter()
    dynoplan_bin_s = _env_or_arg(dynoplan_bin, "DYNOPLAN_BIN")
    dynoplan_cmd_template_s = _env_or_arg(dynoplan_cmd_template, "DYNOPLAN_CMD_TEMPLATE")
    dynoplan_root_s = _env_or_arg(dynoplan_root, "DYNOPLAN_ROOT")

    if work_dir is None and not keep_artifacts:
        with tempfile.TemporaryDirectory(prefix="idb_rrt_dynoplan_") as tmp:
            return _plan_in_work_dir(
                work_dir=Path(tmp),
                started=started,
                grid_map=grid_map,
                footprint=footprint,
                params=params,
                start_xy=start_xy,
                goal_xy=goal_xy,
                goal_theta_rad=goal_theta_rad,
                start_theta_rad=start_theta_rad,
                goal_xy_tol_m=goal_xy_tol_m,
                timeout_s=timeout_s,
                seed=seed,
                dynoplan_bin=dynoplan_bin_s,
                dynoplan_cmd_template=dynoplan_cmd_template_s,
                dynoplan_root=dynoplan_root_s,
                keep_artifacts=True,
            )

    if work_dir is None:
        work_path = Path(tempfile.mkdtemp(prefix="idb_rrt_dynoplan_"))
    else:
        work_path = Path(work_dir)

    return _plan_in_work_dir(
        work_dir=work_path,
        started=started,
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        start_xy=start_xy,
        goal_xy=goal_xy,
        goal_theta_rad=goal_theta_rad,
        start_theta_rad=start_theta_rad,
        goal_xy_tol_m=goal_xy_tol_m,
        timeout_s=timeout_s,
        seed=seed,
        dynoplan_bin=dynoplan_bin_s,
        dynoplan_cmd_template=dynoplan_cmd_template_s,
        dynoplan_root=dynoplan_root_s,
        keep_artifacts=keep_artifacts,
    )


def _plan_in_work_dir(
    *,
    work_dir: Path,
    started: float,
    grid_map: Any,
    footprint: Any,
    params: Any,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    goal_theta_rad: float,
    start_theta_rad: float | None,
    goal_xy_tol_m: float,
    timeout_s: float,
    seed: int,
    dynoplan_bin: str,
    dynoplan_cmd_template: str,
    dynoplan_root: str,
    keep_artifacts: bool,
) -> PlannerResult:
    work_dir.mkdir(parents=True, exist_ok=True)
    problem_path = work_dir / "problem.json"
    output_path = work_dir / "solution.json"
    problem, exported = _build_problem_json(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        start_xy=start_xy,
        goal_xy=goal_xy,
        start_theta_rad=start_theta_rad,
        goal_theta_rad=goal_theta_rad,
        goal_xy_tol_m=goal_xy_tol_m,
        dynoplan_root=dynoplan_root,
    )
    stats = _stats_base(
        dynoplan_bin=dynoplan_bin,
        dynoplan_root=dynoplan_root,
        dynoplan_cmd_template=dynoplan_cmd_template,
        exported=exported,
    )

    command, resolved_bin = _format_command(
        dynoplan_bin=dynoplan_bin,
        dynoplan_cmd_template=dynoplan_cmd_template,
        problem_path=problem_path,
        output_path=output_path,
        timeout_s=timeout_s,
        seed=seed,
    )
    if command is None or resolved_bin is None:
        return PlannerResult(
            path_xy_cells=[],
            time_s=float(time.perf_counter() - started),
            success=False,
            stats=stats,
        )

    stats["dependency_available"] = True
    stats["dynoplan_bin"] = str(resolved_bin)
    problem_path.write_text(json.dumps(problem, indent=2, sort_keys=True), encoding="utf-8")

    try:
        ext_started = time.perf_counter()
        completed = subprocess.run(
            command,
            cwd=str(work_dir),
            check=False,
            capture_output=True,
            text=True,
            timeout=max(1.0, float(timeout_s) + 1.0),
        )
        external_runtime_s = float(time.perf_counter() - ext_started)
    except subprocess.TimeoutExpired:
        stats["status"] = "timeout"
        stats["external_runtime_s"] = float(time.perf_counter() - started)
        if not keep_artifacts:
            _cleanup_artifacts(problem_path, output_path)
        return PlannerResult(
            path_xy_cells=[],
            time_s=float(time.perf_counter() - started),
            success=False,
            stats=stats,
        )

    stats["external_returncode"] = int(completed.returncode)
    stats["external_runtime_s"] = external_runtime_s
    if completed.returncode != 0:
        stats["status"] = "external_failed"
        if not keep_artifacts:
            _cleanup_artifacts(problem_path, output_path)
        return PlannerResult(
            path_xy_cells=[],
            time_s=float(time.perf_counter() - started),
            success=False,
            stats=stats,
        )

    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        path_xy_m = _path_xy_m_from_payload(payload)
        cell_size_m = float(exported["cell_size_m"])
        path_cells = [(float(x) / cell_size_m, float(y) / cell_size_m) for x, y in path_xy_m]
    except Exception as exc:
        stats["status"] = "parse_failed"
        stats["parse_error"] = f"{type(exc).__name__}: {exc}"
        if not keep_artifacts:
            _cleanup_artifacts(problem_path, output_path)
        return PlannerResult(
            path_xy_cells=[],
            time_s=float(time.perf_counter() - started),
            success=False,
            stats=stats,
        )

    for key in _PAYLOAD_STAT_KEYS:
        if key in payload:
            stats[key] = payload[key]
    solution_stage = str(payload.get("dynoplan_solution_stage", ""))
    dynoplan_to_success = payload.get("dynoplan_to_success")
    is_raw_fallback = solution_stage == "raw_geometric_fallback"
    external_success = bool(
        payload.get("success") is not False
        and not is_raw_fallback
        and dynoplan_to_success is not False
    )
    if path_cells:
        last_x, last_y = path_cells[-1]
        goal_error_m = math.hypot(
            (float(last_x) - float(goal_xy[0])) * float(exported["cell_size_m"]),
            (float(last_y) - float(goal_xy[1])) * float(exported["cell_size_m"]),
        )
    else:
        goal_error_m = float("inf")
    success = bool(external_success and goal_error_m <= float(goal_xy_tol_m))
    stats["status"] = "success" if success else ("external_failed" if not external_success else "goal_not_reached")
    stats["goal_error_m"] = float(goal_error_m)

    if not keep_artifacts:
        _cleanup_artifacts(problem_path, output_path)
    return PlannerResult(
        path_xy_cells=path_cells if success else [],
        time_s=float(time.perf_counter() - started),
        success=success,
        stats=stats,
    )
