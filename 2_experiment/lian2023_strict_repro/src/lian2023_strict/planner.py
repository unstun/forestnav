from __future__ import annotations

import enum
import time
from dataclasses import dataclass

import numpy as np

from .astar import astar_grid, shortcut_path
from .config import AlgorithmParams, VehicleParams
from .corridor import build_algorithm1_stage1, build_corridor
from .grid import create_dilated_map, grid_to_world, nearest_free, world_to_grid
from .hybrid_astar import connect_boundary_points_with_hybrid_astar
from .ocp import disk_centers_from_states, smooth_initial_guess
from .scenes import PaperScene


class PlannerMethod(str, enum.Enum):
    ASTAR_IPOPT = "astar_ipopt"
    HYBRID_ASTAR_IPOPT = "hybrid_astar_ipopt"
    FTHA_IPOPT = "ftha_ipopt"
    OURS_EHA_IPOPT = "ours_eha_ipopt"


@dataclass(frozen=True)
class TrajectoryResult:
    scene: str
    method: PlannerMethod
    success: bool
    status: str
    states: np.ndarray
    controls: np.ndarray
    coarse_path: np.ndarray
    boundary_points: np.ndarray
    stats: dict[str, float | str]


def _path_to_world(scene: PaperScene, path: list[tuple[int, int]]) -> np.ndarray:
    return np.asarray([grid_to_world(scene, ix, iy) for ix, iy in path], dtype=float)


def _initial_path(
    scene: PaperScene,
    method: PlannerMethod,
    vehicle: VehicleParams,
    params: AlgorithmParams,
    stage1_timeout_s: float = 30.0,
) -> tuple[np.ndarray, np.ndarray, list, dict[str, float | str]]:
    t0 = time.time()
    dilated = create_dilated_map(scene.grid, scene.cell_size_m, vehicle.disc_radius_m)
    start = nearest_free(dilated, world_to_grid(scene, scene.start[0], scene.start[1]))
    goal = nearest_free(dilated, world_to_grid(scene, scene.goal[0], scene.goal[1]))
    grid_path = astar_grid(dilated, start, goal)
    if not grid_path:
        return np.empty((0, 2)), np.empty((0, 3)), [], {
            "cpu_time_i_s": time.time() - t0,
            "stage1_status": "stage1_2d_astar_fail",
        }

    if method == PlannerMethod.ASTAR_IPOPT:
        world = _path_to_world(scene, grid_path)
        bps = np.empty((0, 3), dtype=float)
        boxes = []
    elif method in (PlannerMethod.HYBRID_ASTAR_IPOPT, PlannerMethod.FTHA_IPOPT):
        world = _path_to_world(scene, shortcut_path(dilated, grid_path))
        bps = np.column_stack(
            [
                world[:, 0],
                world[:, 1],
                np.r_[scene.start[2], np.arctan2(np.diff(world[:, 1]), np.diff(world[:, 0]))],
            ]
        )
        boxes = []
    else:
        world_full = _path_to_world(scene, grid_path)
        boxes = build_corridor(dilated, scene.bounds_m, scene.cell_size_m, world_full, params)
        stage1 = build_algorithm1_stage1(world_full, boxes, scene.start[2], scene.goal[2], params)
        bps = stage1.xbou_corrected
        world_pose = connect_boundary_points_with_hybrid_astar(
            grid=dilated,
            bounds_m=scene.bounds_m,
            cell_size_m=scene.cell_size_m,
            points=bps,
            vehicle=vehicle,
            params=params,
            timeout_s=stage1_timeout_s,
        )
        if len(world_pose) == 0:
            stats = {
                "corridor_boxes": float(len(boxes)),
                "boundary_points": float(len(bps)),
                "wide_boxes": float(sum(1 for box in boxes if box.is_wide)),
                "passage_groups": float(len(stage1.groups)),
                "swps_paths": float(len(stage1.swps)),
                "snps_paths": float(len(stage1.snps)),
                "wide_groups": float(sum(1 for group in stage1.groups if group.kind == "wide")),
                "narrow_groups": float(sum(1 for group in stage1.groups if group.kind == "narrow")),
                "xseq_paths": float(len(stage1.xseq)),
                "xbou_points": float(len(bps)),
                "stage1_fallback": "false",
                "cpu_time_i_s": time.time() - t0,
                "stage1_status": "stage1_eha_fail",
            }
            return np.empty((0, 2)), bps, boxes, stats
        world = world_pose
        stats = {
            "corridor_boxes": float(len(boxes)),
            "boundary_points": float(len(bps)),
            "wide_boxes": float(sum(1 for box in boxes if box.is_wide)),
            "passage_groups": float(len(stage1.groups)),
            "swps_paths": float(len(stage1.swps)),
            "snps_paths": float(len(stage1.snps)),
            "wide_groups": float(sum(1 for group in stage1.groups if group.kind == "wide")),
            "narrow_groups": float(sum(1 for group in stage1.groups if group.kind == "narrow")),
            "xseq_paths": float(len(stage1.xseq)),
            "xbou_points": float(len(bps)),
            "stage1_fallback": "false",
        }
        stats["cpu_time_i_s"] = time.time() - t0
        stats["stage1_status"] = "success"
        return world, bps, boxes, stats

    stats = {
        "cpu_time_i_s": time.time() - t0,
        "stage1_status": "success",
        "boundary_points": float(len(bps)),
        "stage1_fallback": "false",
    }
    return world, bps, boxes, stats


def plan_scene(
    scene: PaperScene,
    *,
    method: PlannerMethod,
    vehicle: VehicleParams,
    params: AlgorithmParams,
    timeout_s: float = 30.0,
) -> TrajectoryResult:
    t0 = time.time()
    coarse_xy, bps, corridor_boxes, stage1_stats = _initial_path(
        scene,
        method,
        vehicle,
        params,
        stage1_timeout_s=timeout_s,
    )
    stage1_stats["ipopt_max_iterations"] = float(params.ipopt_max_iterations)
    if len(coarse_xy) == 0:
        return TrajectoryResult(
            scene=scene.name,
            method=method,
            success=False,
            status=str(stage1_stats["stage1_status"]),
            states=np.empty((0, 5), dtype=float),
            controls=np.empty((0, 2), dtype=float),
            coarse_path=coarse_xy,
            boundary_points=bps,
            stats=stage1_stats,
        )
    if time.time() - t0 > timeout_s:
        return TrajectoryResult(
            scene=scene.name,
            method=method,
            success=False,
            status="runtime_timeout",
            states=np.empty((0, 5), dtype=float),
            controls=np.empty((0, 2), dtype=float),
            coarse_path=coarse_xy,
            boundary_points=bps,
            stats=stage1_stats,
        )

    if len(coarse_xy) == 1:
        poses = np.array([[coarse_xy[0, 0], coarse_xy[0, 1], scene.start[2]]], dtype=float)
    elif coarse_xy.shape[1] >= 3:
        poses = coarse_xy[:, :3].copy()
        poses[0, 2] = scene.start[2]
        poses[-1, 2] = scene.goal[2]
    else:
        headings = np.r_[
            scene.start[2],
            np.arctan2(np.diff(coarse_xy[:, 1]), np.diff(coarse_xy[:, 0])),
        ]
        headings[-1] = scene.goal[2]
        poses = np.column_stack([coarse_xy, headings])
    disc_corridor_boxes = _disc_corridors_for_poses(scene, poses, vehicle, params)
    states, controls, stage2_stats = smooth_initial_guess(
        poses,
        scene.start,
        scene.goal,
        vehicle,
        params,
        corridor_boxes=disc_corridor_boxes,
        corridor_provider=lambda states_for_corridor: _disc_corridors_for_states(
            scene,
            states_for_corridor,
            vehicle,
            params,
        ),
    )
    stats: dict[str, float | str] = {
        **stage1_stats,
        **stage2_stats,
        "total_time_s": time.time() - t0,
        "method": method.value,
    }
    terminal_error = float(np.linalg.norm(states[-1, :2] - np.asarray(scene.goal[:2], dtype=float)))
    ipopt_status = str(stage2_stats.get("ipopt_status", ""))
    jinf = float(stage2_stats.get("jinf", float("inf")))
    jinf_ok = jinf <= float(params.etol)
    constraint_ok = (
        np.max(np.abs(states[:, 3])) <= vehicle.max_velocity_m_s + 1e-6
        and np.max(np.abs(states[:, 4])) <= vehicle.max_steer_rad + 1e-6
        and np.max(np.abs(controls[:, 0])) <= vehicle.max_accel_m_s2 + 1e-6
        and np.max(np.abs(controls[:, 1])) <= vehicle.max_omega_rad_s + 1e-6
    )
    success = (
        terminal_error <= 0.5
        and ipopt_status.startswith("ipopt:")
        and "fallback" not in ipopt_status
        and constraint_ok
        and jinf_ok
    )
    stats["terminal_error_m"] = terminal_error
    stats["constraint_ok"] = str(constraint_ok)
    stats["jinf_ok"] = str(jinf_ok)
    stats["disc_corridors"] = float(sum(1 for boxes in disc_corridor_boxes if boxes))
    if terminal_error > 0.5 or not constraint_ok:
        status = "stage2_validation_fail"
    elif not jinf_ok:
        status = "stage2_infeasible"
    else:
        status = "success"
    return TrajectoryResult(
        scene=scene.name,
        method=method,
        success=success,
        status=status,
        states=states,
        controls=controls,
        coarse_path=coarse_xy,
        boundary_points=bps,
        stats=stats,
    )


def _disc_corridors_for_poses(
    scene: PaperScene,
    poses: np.ndarray,
    vehicle: VehicleParams,
    params: AlgorithmParams,
) -> tuple[tuple, ...]:
    if len(poses) == 0:
        return tuple()
    states = np.zeros((len(poses), 5), dtype=float)
    states[:, :3] = poses[:, :3]
    return _disc_corridors_for_states(scene, states, vehicle, params)


def _disc_corridors_for_states(
    scene: PaperScene,
    states: np.ndarray,
    vehicle: VehicleParams,
    params: AlgorithmParams,
) -> tuple[tuple, ...]:
    if len(states) == 0:
        return tuple()
    centers = disk_centers_from_states(states, vehicle)
    dilated = create_dilated_map(scene.grid, scene.cell_size_m, vehicle.disc_radius_m)
    out = []
    for j in range(centers.shape[1]):
        boxes = build_corridor(dilated, scene.bounds_m, scene.cell_size_m, centers[:, j, :], params)
        out.append(tuple(boxes))
    return tuple(out)
