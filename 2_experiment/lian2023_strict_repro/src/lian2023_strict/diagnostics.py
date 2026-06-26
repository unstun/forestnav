from __future__ import annotations

import math

import numpy as np

from .astar import astar_grid
from .config import AlgorithmParams, VehicleParams
from .corridor import build_algorithm1_stage1, build_corridor
from .grid import create_dilated_map, grid_to_world, nearest_free, world_to_grid
from .hybrid_astar import hybrid_astar_segment
from .ocp import (
    _initial_guess_from_poses,
    evaluate_formula23_components,
    evaluate_kinematic_residuals,
)
from .scenes import build_scene


def _angle_error(a: float, b: float) -> float:
    return abs((float(a) - float(b) + math.pi) % (2.0 * math.pi) - math.pi)


def _round_pose_array(values: np.ndarray) -> list[list[float]]:
    return [[float(v) for v in row] for row in np.round(values, 6)]


def _seed_diagnostics(
    poses: np.ndarray,
    start: tuple[float, float, float, float, float],
    goal: tuple[float, float, float, float, float],
    vehicle: VehicleParams,
    params: AlgorithmParams,
) -> dict:
    states, controls, tf = _initial_guess_from_poses(poses, start, goal, vehicle, int(params.n_elements))
    residuals = evaluate_kinematic_residuals(states, controls, tf, vehicle)
    residual_norms = np.linalg.norm(residuals, axis=1)
    top_k = int(np.argmax(residual_norms)) if len(residual_norms) else 0
    components = evaluate_formula23_components(states, controls, tf, vehicle, params)
    theta_steps = np.abs(np.diff(np.unwrap(states[:, 2])))
    xy_steps = np.linalg.norm(np.diff(states[:, :2], axis=0), axis=1)
    return {
        **{key: float(value) for key, value in components.items()},
        "tf_s": float(tf),
        "max_step_m": float(np.max(xy_steps)) if len(xy_steps) else 0.0,
        "max_dtheta_rad": float(np.max(theta_steps)) if len(theta_steps) else 0.0,
        "max_abs_v": float(np.max(np.abs(states[:, 3]))) if len(states) else 0.0,
        "max_abs_phi": float(np.max(np.abs(states[:, 4]))) if len(states) else 0.0,
        "max_abs_a": float(np.max(np.abs(controls[:, 0]))) if len(controls) else 0.0,
        "max_abs_omega": float(np.max(np.abs(controls[:, 1]))) if len(controls) else 0.0,
        "top_kinematic_residual": {
            "k": top_k,
            "norm": float(residual_norms[top_k]) if len(residual_norms) else 0.0,
            "state_xy": [float(v) for v in states[top_k, :2]] if len(states) else [0.0, 0.0],
            "residual": [float(v) for v in residuals[top_k]] if len(residuals) else [0.0] * 5,
        },
    }


def diagnose_stage1(
    scene_name: str,
    *,
    vehicle: VehicleParams,
    params: AlgorithmParams,
    segment_timeout_s: float = 30.0,
) -> dict:
    scene = build_scene(scene_name)
    dilated = create_dilated_map(scene.grid, scene.cell_size_m, vehicle.disc_radius_m)
    start = nearest_free(dilated, world_to_grid(scene, scene.start[0], scene.start[1]))
    goal = nearest_free(dilated, world_to_grid(scene, scene.goal[0], scene.goal[1]))
    grid_path = astar_grid(dilated, start, goal)
    if not grid_path:
        return {
            "scene": scene_name,
            "stage1_status": "stage1_2d_astar_fail",
            "grid_path_points": 0,
            "segments": [],
        }

    world_full = np.asarray([grid_to_world(scene, ix, iy) for ix, iy in grid_path], dtype=float)
    boxes = build_corridor(dilated, scene.bounds_m, scene.cell_size_m, world_full, params)
    stage1 = build_algorithm1_stage1(world_full, boxes, scene.start[2], scene.goal[2], params)
    segments = []
    connected: list[np.ndarray] = []
    for idx in range(max(0, len(stage1.xbou_corrected) - 1)):
        start_pose = stage1.xbou_corrected[idx]
        goal_pose = stage1.xbou_corrected[idx + 1]
        segment = hybrid_astar_segment(
            grid=dilated,
            bounds_m=scene.bounds_m,
            cell_size_m=scene.cell_size_m,
            start=tuple(start_pose),
            goal=tuple(goal_pose),
            vehicle=vehicle,
            params=params,
            timeout_s=segment_timeout_s,
        )
        if len(segment) == 0:
            segments.append(
                {
                    "index": idx,
                    "status": "fail",
                    "points": 0,
                    "goal_pose": [float(v) for v in goal_pose],
                }
            )
            continue
        actual_end = segment[-2] if len(segment) >= 2 else segment[-1]
        if connected:
            connected.append(segment[1:])
        else:
            connected.append(segment)
        segments.append(
            {
                "index": idx,
                "status": "success",
                "points": int(len(segment)),
                "goal_pose": [float(v) for v in goal_pose],
                "pre_append_xy_error_m": float(np.linalg.norm(actual_end[:2] - goal_pose[:2])),
                "pre_append_heading_error_rad": float(_angle_error(actual_end[2], goal_pose[2])),
                "append_xy_jump_m": float(np.linalg.norm(segment[-1, :2] - segment[-2, :2])) if len(segment) >= 2 else 0.0,
                "append_heading_jump_rad": float(_angle_error(segment[-1, 2], segment[-2, 2])) if len(segment) >= 2 else 0.0,
            }
        )
    connected_path = np.vstack(connected) if connected and all(len(part) for part in connected) else np.empty((0, 3), dtype=float)
    seed = (
        _seed_diagnostics(connected_path, scene.start, scene.goal, vehicle, params)
        if len(connected_path) > 0
        else {}
    )
    return {
        "scene": scene_name,
        "stage1_status": "success" if len(connected_path) > 0 else "stage1_eha_fail",
        "grid_path_points": int(len(grid_path)),
        "corridor_boxes": int(len(boxes)),
        "wide_boxes": int(sum(1 for box in boxes if box.is_wide)),
        "groups": [
            {
                "index": idx,
                "kind": group.kind,
                "node_count": int(len(group.nodes)) if group.nodes is not None else 0,
                "box_count": int(len(group.boxes)),
                "start_index": int(group.start_index),
                "end_index": int(group.end_index),
                "min_side_m": float(min((box.min_side_m for box in group.boxes), default=0.0)),
            }
            for idx, group in enumerate(stage1.groups)
        ],
        "xbou_raw_count": int(len(stage1.xbou)),
        "xbou_corrected_count": int(len(stage1.xbou_corrected)),
        "xbou_raw": _round_pose_array(stage1.xbou),
        "xbou_corrected": _round_pose_array(stage1.xbou_corrected),
        "segments": segments,
        "seed": seed,
    }
