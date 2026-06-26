from __future__ import annotations

import math
import time
from collections.abc import Callable

import numpy as np

from .config import AlgorithmParams, VehicleParams
from .corridor import CorridorBox

try:
    from . import ocp_fast as _ocp_fast
except Exception:  # pragma: no cover - optional native backend
    _ocp_fast = None


CorridorProvider = Callable[[np.ndarray], list | tuple]


def _cpp_backend_enabled() -> bool:
    return _ocp_fast is not None and _ocp_fast.is_enabled()


def _ocp_backend_name() -> str:
    return "cpp" if _cpp_backend_enabled() else "python"


def lse_local_state_constraint(
    x: float,
    y: float,
    z: float,
    area: tuple[float, float, float, float],
    bounds: tuple[float, float],
    beta: float,
) -> float:
    xa, xb, ya, yb = area
    za, zb = bounds
    fx = max(-((x - xa) * (x - xb)), 0.0)
    fy = max(-((y - ya) * (y - yb)), 0.0)
    fz = (1.0 / beta) * math.log(math.exp(beta * ((z - za) * (z - zb))) + 1.0)
    return fx * fy * fz


def evaluate_kinematic_residuals(
    states: np.ndarray,
    controls: np.ndarray,
    tf: float,
    vehicle: VehicleParams,
) -> np.ndarray:
    n = len(controls)
    dt = float(tf) / max(n, 1)
    residuals = np.zeros((n, 5), dtype=float)
    for k in range(n):
        px, py, theta, v, phi = states[k]
        expected = np.array(
            [
                px + dt * v * math.cos(theta),
                py + dt * v * math.sin(theta),
                theta + dt * v * math.tan(phi) / vehicle.wheelbase_m,
                v + dt * controls[k, 0],
                phi + dt * controls[k, 1],
            ],
            dtype=float,
        )
        residuals[k] = states[k + 1] - expected
    return residuals


def evaluate_formula16_objective(states: np.ndarray, tf: float, params: AlgorithmParams) -> float:
    dv = np.diff(states[:, 3])
    dphi = np.diff(states[:, 4])
    return float(params.mu1 * tf + params.mu2 * np.dot(dv, dv) + params.mu3 * np.dot(dphi, dphi))


def disk_centers_from_states(states: np.ndarray, vehicle: VehicleParams) -> np.ndarray:
    centers = np.zeros((len(states), len(vehicle.disc_offsets_m), 2), dtype=float)
    cos_th = np.cos(states[:, 2])
    sin_th = np.sin(states[:, 2])
    for j, offset in enumerate(vehicle.disc_offsets_m):
        centers[:, j, 0] = states[:, 0] + offset * cos_th
        centers[:, j, 1] = states[:, 1] + offset * sin_th
    return centers


def evaluate_disk_geometry_penalty(states: np.ndarray, disk_centers: np.ndarray, vehicle: VehicleParams) -> float:
    expected = disk_centers_from_states(states, vehicle)
    residual = disk_centers - expected
    return float(np.sum(residual * residual))


def _corridor_boxes_for_disc(
    corridor_boxes: list | tuple,
    disc_index: int,
) -> tuple[CorridorBox, ...]:
    if not corridor_boxes:
        return tuple()
    first = corridor_boxes[0]
    if isinstance(first, CorridorBox):
        return tuple(corridor_boxes)
    nested = corridor_boxes[min(disc_index, len(corridor_boxes) - 1)]
    return tuple(nested)


def evaluate_corridor_box_penalty(disk_centers: np.ndarray, corridor_boxes: list | tuple) -> float:
    if not corridor_boxes:
        return 0.0
    penalty = 0.0
    for centers_at_k in disk_centers:
        for j, center in enumerate(centers_at_k):
            boxes_for_disc = _corridor_boxes_for_disc(corridor_boxes, j)
            if not boxes_for_disc:
                continue
            box_centers = np.asarray([box.center for box in boxes_for_disc], dtype=float)
            idx = int(np.argmin(np.sum((box_centers - center) ** 2, axis=1)))
            box = boxes_for_disc[idx]
            xmin = box.center[0] - box.left_m
            xmax = box.center[0] + box.right_m
            ymin = box.center[1] - box.down_m
            ymax = box.center[1] + box.up_m
            low_x = max(xmin - float(center[0]), 0.0)
            high_x = max(float(center[0]) - xmax, 0.0)
            low_y = max(ymin - float(center[1]), 0.0)
            high_y = max(float(center[1]) - ymax, 0.0)
            penalty += low_x * low_x + high_x * high_x + low_y * low_y + high_y * high_y
    return penalty


def _corridor_box_limits(box: CorridorBox) -> tuple[tuple[float, float], tuple[float, float]]:
    lower = (float(box.center[0] - box.left_m), float(box.center[1] - box.down_m))
    upper = (float(box.center[0] + box.right_m), float(box.center[1] + box.up_m))
    return lower, upper


def _assigned_corridor_bounds(
    disk_centers: np.ndarray,
    corridor_boxes: None | list | tuple,
) -> tuple[np.ndarray, np.ndarray]:
    lower = np.full_like(disk_centers, -np.inf, dtype=float)
    upper = np.full_like(disk_centers, np.inf, dtype=float)
    if not corridor_boxes:
        return lower, upper
    for k, centers_at_k in enumerate(disk_centers):
        for j, center in enumerate(centers_at_k):
            boxes_for_disc = _corridor_boxes_for_disc(corridor_boxes, j)
            if not boxes_for_disc:
                continue
            box_centers = np.asarray([box.center for box in boxes_for_disc], dtype=float)
            idx = int(np.argmin(np.sum((box_centers - center) ** 2, axis=1)))
            box_lower, box_upper = _corridor_box_limits(boxes_for_disc[idx])
            lower[k, j] = box_lower
            upper[k, j] = box_upper
    return lower, upper


def evaluate_formula23_components(
    states: np.ndarray,
    controls: np.ndarray,
    tf: float,
    vehicle: VehicleParams,
    params: AlgorithmParams,
    corridor_boxes: None | list[CorridorBox] | tuple[CorridorBox, ...] = None,
    disk_centers: None | np.ndarray = None,
) -> dict[str, float]:
    kin = evaluate_kinematic_residuals(states, controls, tf, vehicle)
    centers = disk_centers_from_states(states, vehicle) if disk_centers is None else disk_centers
    if params.enable_local_state_constraint:
        local = [
            lse_local_state_constraint(px, py, abs(v), params.local_area, params.local_speed_bounds_m_s, params.beta)
            for px, py, v in states[:, [0, 1, 3]]
        ]
    else:
        local = [0.0 for _ in states]
    j3 = float(np.sum(kin * kin))
    j7 = evaluate_disk_geometry_penalty(states, centers, vehicle)
    j6 = evaluate_corridor_box_penalty(centers, tuple(corridor_boxes or ()))
    j15 = float(np.sum(np.asarray(local) ** 2))
    return {
        "jpenalty3": j3,
        "jpenalty7": j7,
        "jpenalty6": j6,
        "jpenalty15": j15,
        "jinf": j3 + j7 + j15,
    }


def evaluate_formula23_penalty(
    states: np.ndarray,
    controls: np.ndarray,
    tf: float,
    vehicle: VehicleParams,
    params: AlgorithmParams,
    corridor_bounds: None | tuple[np.ndarray, np.ndarray] = None,
    corridor_boxes: None | list[CorridorBox] | tuple[CorridorBox, ...] = None,
    disk_centers: None | np.ndarray = None,
) -> float:
    if corridor_bounds is None and _cpp_backend_enabled():
        centers = disk_centers_from_states(states, vehicle) if disk_centers is None else disk_centers
        return _ocp_fast.formula23_penalty_value(
            states,
            controls,
            tf,
            vehicle,
            params,
            disk_centers=centers,
        )
    components = evaluate_formula23_components(
        states,
        controls,
        tf,
        vehicle,
        params,
        corridor_boxes=corridor_boxes,
        disk_centers=disk_centers,
    )
    penalty = components["jpenalty3"] + components["jpenalty7"] + components["jpenalty15"]
    if corridor_bounds is not None:
        lower, upper = corridor_bounds
        xy = states[:, :2]
        low_v = np.maximum(lower - xy, 0.0)
        up_v = np.maximum(xy - upper, 0.0)
        penalty += float(np.sum(low_v * low_v) + np.sum(up_v * up_v))
    return penalty


def _formula16_gradient(states: np.ndarray, controls: np.ndarray, tf: float, params: AlgorithmParams) -> tuple[np.ndarray, np.ndarray, float]:
    grad_states = np.zeros_like(states)
    grad_controls = np.zeros_like(controls)
    grad_tf = float(params.mu1)
    dv = np.diff(states[:, 3])
    dphi = np.diff(states[:, 4])
    grad_states[:-1, 3] -= 2.0 * params.mu2 * dv
    grad_states[1:, 3] += 2.0 * params.mu2 * dv
    grad_states[:-1, 4] -= 2.0 * params.mu3 * dphi
    grad_states[1:, 4] += 2.0 * params.mu3 * dphi
    return grad_states, grad_controls, grad_tf


def _formula23_penalty_gradient(
    states: np.ndarray,
    controls: np.ndarray,
    disk_centers: np.ndarray,
    tf: float,
    vehicle: VehicleParams,
    params: AlgorithmParams,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    if _cpp_backend_enabled():
        return _ocp_fast.formula23_penalty_gradient(states, controls, disk_centers, tf, vehicle, params)
    n = len(controls)
    dt = float(tf) / max(n, 1)
    grad_states = np.zeros_like(states)
    grad_controls = np.zeros_like(controls)
    grad_disks = np.zeros_like(disk_centers)
    grad_tf = 0.0

    for k in range(n):
        x, y, theta, v, phi = states[k]
        a, omega = controls[k]
        cos_th = math.cos(theta)
        sin_th = math.sin(theta)
        tan_phi = math.tan(phi)
        cos_phi = math.cos(phi)
        sec2_phi = 1.0 / max(cos_phi * cos_phi, 1e-12)
        residual = np.array(
            [
                states[k + 1, 0] - x - dt * v * cos_th,
                states[k + 1, 1] - y - dt * v * sin_th,
                states[k + 1, 2] - theta - dt * v * tan_phi / vehicle.wheelbase_m,
                states[k + 1, 3] - v - dt * a,
                states[k + 1, 4] - phi - dt * omega,
            ],
            dtype=float,
        )
        scaled = 2.0 * residual

        grad_states[k + 1, 0] += scaled[0]
        grad_states[k, 0] -= scaled[0]
        grad_states[k, 2] += scaled[0] * dt * v * sin_th
        grad_states[k, 3] -= scaled[0] * dt * cos_th
        grad_tf -= scaled[0] * (v * cos_th / max(n, 1))

        grad_states[k + 1, 1] += scaled[1]
        grad_states[k, 1] -= scaled[1]
        grad_states[k, 2] -= scaled[1] * dt * v * cos_th
        grad_states[k, 3] -= scaled[1] * dt * sin_th
        grad_tf -= scaled[1] * (v * sin_th / max(n, 1))

        grad_states[k + 1, 2] += scaled[2]
        grad_states[k, 2] -= scaled[2]
        grad_states[k, 3] -= scaled[2] * dt * tan_phi / vehicle.wheelbase_m
        grad_states[k, 4] -= scaled[2] * dt * v * sec2_phi / vehicle.wheelbase_m
        grad_tf -= scaled[2] * (v * tan_phi / (max(n, 1) * vehicle.wheelbase_m))

        grad_states[k + 1, 3] += scaled[3]
        grad_states[k, 3] -= scaled[3]
        grad_controls[k, 0] -= scaled[3] * dt
        grad_tf -= scaled[3] * (a / max(n, 1))

        grad_states[k + 1, 4] += scaled[4]
        grad_states[k, 4] -= scaled[4]
        grad_controls[k, 1] -= scaled[4] * dt
        grad_tf -= scaled[4] * (omega / max(n, 1))

    expected = disk_centers_from_states(states, vehicle)
    disk_residual = disk_centers - expected
    grad_disks += 2.0 * disk_residual
    for j, offset in enumerate(vehicle.disc_offsets_m):
        cos_th = np.cos(states[:, 2])
        sin_th = np.sin(states[:, 2])
        rx = disk_residual[:, j, 0]
        ry = disk_residual[:, j, 1]
        grad_states[:, 0] -= 2.0 * rx
        grad_states[:, 1] -= 2.0 * ry
        grad_states[:, 2] += 2.0 * offset * rx * sin_th
        grad_states[:, 2] -= 2.0 * offset * ry * cos_th

    if params.enable_local_state_constraint:
        _add_local_state_constraint_gradient(grad_states, states, params)

    return grad_states, grad_controls, grad_disks, grad_tf


def _add_local_state_constraint_gradient(
    grad_states: np.ndarray,
    states: np.ndarray,
    params: AlgorithmParams,
) -> None:
    xa, xb, ya, yb = params.local_area
    za, zb = params.local_speed_bounds_m_s
    beta = float(params.beta)
    for k, (x, y, _theta, v, _phi) in enumerate(states):
        raw_x = -((x - xa) * (x - xb))
        raw_y = -((y - ya) * (y - yb))
        fx = max(raw_x, 0.0)
        fy = max(raw_y, 0.0)
        if fx <= 0.0 or fy <= 0.0:
            continue
        z = abs(float(v))
        g = (z - za) * (z - zb)
        bz = beta * g
        if bz >= 0.0:
            fz = (bz + math.log1p(math.exp(-bz))) / beta
            sigmoid = 1.0 / (1.0 + math.exp(-bz))
        else:
            fz = math.log1p(math.exp(bz)) / beta
            sigmoid = math.exp(bz) / (1.0 + math.exp(bz))
        local = fx * fy * fz
        scale = 2.0 * local
        grad_states[k, 0] += scale * (xa + xb - 2.0 * x) * fy * fz
        grad_states[k, 1] += scale * fx * (ya + yb - 2.0 * y) * fz
        if v != 0.0:
            dz_dv = 1.0 if v > 0.0 else -1.0
            dfz_dv = sigmoid * (2.0 * z - za - zb) * dz_dv
            grad_states[k, 3] += scale * fx * fy * dfz_dv


def smooth_initial_guess(
    poses: np.ndarray,
    start: tuple[float, float, float, float, float],
    goal: tuple[float, float, float, float, float],
    vehicle: VehicleParams,
    params: AlgorithmParams,
    corridor_boxes: None | list[CorridorBox] | tuple[CorridorBox, ...] = None,
    corridor_provider: None | CorridorProvider = None,
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    t0 = time.time()
    n = int(params.n_elements)
    states_seed, controls_seed, tf_seed = _initial_guess_from_poses(poses, start, goal, vehicle, n)
    states = states_seed
    controls = controls_seed
    tf = tf_seed
    ipopt_status = "ipopt:not_run"
    ipopt_iterations = 0
    try:
        (
            states,
            controls,
            disk_centers,
            tf,
            ipopt_status,
            ipopt_iterations,
            outer_iterations,
            final_penalty_weight,
            current_corridor_boxes,
        ) = _state_control_ipopt(
            states_ref=states_seed,
            controls_ref=controls_seed,
            tf_ref=tf_seed,
            start=start,
            goal=goal,
            vehicle=vehicle,
            params=params,
            corridor_boxes=corridor_boxes,
            corridor_provider=corridor_provider,
        )
    except Exception as exc:  # pragma: no cover - fallback only for missing native solver
        ipopt_status = f"ipopt:fallback:{type(exc).__name__}:{exc}"
        disk_centers = disk_centers_from_states(states, vehicle)
        outer_iterations = 0
        final_penalty_weight = float(params.initial_penalty)
        current_corridor_boxes = corridor_boxes

    components = evaluate_formula23_components(
        states,
        controls,
        tf,
        vehicle,
        params,
        corridor_boxes=current_corridor_boxes,
        disk_centers=disk_centers,
    )
    stats = {
        "cpu_time_ii_s": time.time() - t0,
        "tf_s": tf,
        "ipopt_status": ipopt_status,
        "ipopt_iterations": float(ipopt_iterations),
        "outer_iterations": float(outer_iterations),
        "final_penalty_weight": float(final_penalty_weight),
        "ocp_backend": _ocp_backend_name(),
        **components,
    }
    return states, controls, stats


def _initial_guess_from_poses(
    poses: np.ndarray,
    start: tuple[float, float, float, float, float],
    goal: tuple[float, float, float, float, float],
    vehicle: VehicleParams,
    n: int,
) -> tuple[np.ndarray, np.ndarray, float]:
    if len(poses) < 2:
        poses = np.array([[start[0], start[1], start[2]], [goal[0], goal[1], goal[2]]], dtype=float)
    poses = np.asarray(poses, dtype=float)
    if poses.shape[1] < 3:
        seg_heading = np.r_[start[2], np.arctan2(np.diff(poses[:, 1]), np.diff(poses[:, 0]))]
        poses = np.column_stack([poses[:, :2], seg_heading])
    seg = np.linalg.norm(np.diff(poses[:, :2], axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    keep = np.r_[True, np.diff(s) > 1e-9]
    poses = poses[keep]
    s = s[keep]
    if len(poses) < 2 or s[-1] <= 1e-9:
        x = np.linspace(start[0], goal[0], n + 1)
        y = np.linspace(start[1], goal[1], n + 1)
        theta = np.linspace(start[2], goal[2], n + 1)
    else:
        target = np.linspace(0.0, s[-1], n + 1)
        x = np.interp(target, s, poses[:, 0])
        y = np.interp(target, s, poses[:, 1])
        theta = np.interp(target, s, np.unwrap(poses[:, 2]))
        x[0], y[0], theta[0] = start[0], start[1], start[2]
        x[-1], y[-1], theta[-1] = goal[0], goal[1], goal[2]
    states = np.zeros((n + 1, 5), dtype=float)
    states[:, 0] = x
    states[:, 1] = y
    states[:, 2] = theta
    tf = _tf_from_xy(x, y, vehicle)
    dt = tf / max(n, 1)
    delta_xy = np.diff(states[:, :2], axis=0)
    heading_vec = np.column_stack([np.cos(states[:-1, 2]), np.sin(states[:-1, 2])])
    signed_ds = np.sum(delta_xy * heading_vec, axis=1)
    segment_v = signed_ds / max(dt, 1e-6)
    states[:-1, 3] = np.clip(segment_v, -vehicle.max_velocity_m_s, vehicle.max_velocity_m_s)
    states[0, 3] = start[3]
    states[-1, 3] = goal[3]
    dtheta = np.diff(np.unwrap(states[:, 2]))
    denominator = np.where(np.abs(signed_ds) > 1e-6, signed_ds, np.sign(signed_ds + 1e-12) * 1e-6)
    segment_phi = np.arctan2(vehicle.wheelbase_m * dtheta, denominator)
    states[:-1, 4] = np.clip(segment_phi, -vehicle.max_steer_rad, vehicle.max_steer_rad)
    states[0, 4] = start[4]
    states[-1, 4] = goal[4]
    controls = _controls_from_states(states, tf, vehicle)
    return states, controls, tf


def _tf_from_xy(x: np.ndarray, y: np.ndarray, vehicle: VehicleParams) -> float:
    total_length = float(np.sum(np.hypot(np.diff(x), np.diff(y))))
    return max(total_length / max(vehicle.max_velocity_m_s * 0.65, 1e-6), 1.0)


def _states_from_xy(
    *,
    start: tuple[float, float, float, float, float],
    goal: tuple[float, float, float, float, float],
    vehicle: VehicleParams,
    x: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    tf = _tf_from_xy(x, y, vehicle)
    dt = tf / max(len(x) - 1, 1)
    dx = np.gradient(x)
    dy = np.gradient(y)
    theta = np.unwrap(np.arctan2(dy, dx))
    theta[0] = start[2]
    theta[-1] = goal[2]
    ds = np.hypot(dx, dy)
    v = np.clip(ds / max(dt, 1e-6), -vehicle.max_velocity_m_s, vehicle.max_velocity_m_s)
    v[0] = start[3]
    v[-1] = goal[3]
    dtheta = np.gradient(theta)
    delta = np.clip(
        np.arctan2(vehicle.wheelbase_m * dtheta, np.maximum(ds, 1e-6)),
        -vehicle.max_steer_rad,
        vehicle.max_steer_rad,
    )
    delta[0] = start[4]
    delta[-1] = goal[4]
    return np.column_stack([x, y, theta, v, delta]).astype(float)


def _controls_from_states(states: np.ndarray, tf: float, vehicle: VehicleParams) -> np.ndarray:
    dt = tf / max(len(states) - 1, 1)
    controls = np.zeros((len(states) - 1, 2), dtype=float)
    controls[:, 0] = np.clip(np.diff(states[:, 3]) / max(dt, 1e-6), -vehicle.max_accel_m_s2, vehicle.max_accel_m_s2)
    controls[:, 1] = np.clip(np.diff(states[:, 4]) / max(dt, 1e-6), -vehicle.max_omega_rad_s, vehicle.max_omega_rad_s)
    return controls


def _pack(states: np.ndarray, controls: np.ndarray, disk_centers: np.ndarray, tf: float) -> np.ndarray:
    return np.r_[states.ravel(), controls.ravel(), disk_centers.ravel(), [tf]]


def _unpack(q: np.ndarray, n: int, disc_count: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    state_len = (n + 1) * 5
    control_len = n * 2
    disk_len = (n + 1) * disc_count * 2
    disk_start = state_len + control_len
    return (
        q[:state_len].reshape((n + 1, 5)),
        q[state_len : state_len + control_len].reshape((n, 2)),
        q[disk_start : disk_start + disk_len].reshape((n + 1, disc_count, 2)),
        float(q[-1]),
    )


def _state_control_ipopt(
    *,
    states_ref: np.ndarray,
    controls_ref: np.ndarray,
    tf_ref: float,
    start: tuple[float, float, float, float, float],
    goal: tuple[float, float, float, float, float],
    vehicle: VehicleParams,
    params: AlgorithmParams,
    corridor_boxes: None | list[CorridorBox] | tuple[CorridorBox, ...] = None,
    corridor_provider: None | CorridorProvider = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, str, int, int, float, list | tuple | None]:
    from cyipopt import minimize_ipopt

    n = len(controls_ref)
    disk_ref = disk_centers_from_states(states_ref, vehicle)
    q0 = _pack(states_ref, controls_ref, disk_ref, tf_ref)
    base_lower = np.full_like(q0, -np.inf, dtype=float)
    base_upper = np.full_like(q0, np.inf, dtype=float)
    states_lower = base_lower[: (n + 1) * 5].reshape((n + 1, 5))
    states_upper = base_upper[: (n + 1) * 5].reshape((n + 1, 5))
    controls_lower = base_lower[(n + 1) * 5 : (n + 1) * 5 + n * 2].reshape((n, 2))
    controls_upper = base_upper[(n + 1) * 5 : (n + 1) * 5 + n * 2].reshape((n, 2))
    states_lower[:, 3] = -vehicle.max_velocity_m_s
    states_upper[:, 3] = vehicle.max_velocity_m_s
    states_lower[:, 4] = -vehicle.max_steer_rad
    states_upper[:, 4] = vehicle.max_steer_rad
    controls_lower[:, 0] = -vehicle.max_accel_m_s2
    controls_upper[:, 0] = vehicle.max_accel_m_s2
    controls_lower[:, 1] = -vehicle.max_omega_rad_s
    controls_upper[:, 1] = vehicle.max_omega_rad_s
    states_lower[0] = states_upper[0] = np.asarray(start, dtype=float)
    states_lower[-1] = states_upper[-1] = np.asarray(goal, dtype=float)
    disk_start = (n + 1) * 5 + n * 2
    disk_stop = disk_start + disk_ref.size
    base_lower[-1] = 0.5
    base_upper[-1] = 200.0
    penalty_weight = float(params.initial_penalty)
    q_current = q0.copy()
    total_ipopt_iterations = 0
    outer_iterations = 0
    final_penalty_weight = penalty_weight
    message = "not_run"
    states, controls, disk_centers, tf = _unpack(q_current, n, len(vehicle.disc_offsets_m))
    current_corridor_boxes = corridor_boxes

    for outer in range(max(1, int(params.max_iterations))):
        current_weight = penalty_weight
        final_penalty_weight = current_weight
        use_cpp_packed = _cpp_backend_enabled()
        if corridor_provider is not None:
            current_corridor_boxes = corridor_provider(states)
        lower = base_lower.copy()
        upper = base_upper.copy()
        disk_lower = lower[disk_start:disk_stop].reshape(disk_ref.shape)
        disk_upper = upper[disk_start:disk_stop].reshape(disk_ref.shape)
        assigned_lower, assigned_upper = _assigned_corridor_bounds(
            disk_centers_from_states(states, vehicle),
            current_corridor_boxes,
        )
        disk_lower[:-1] = assigned_lower[:-1]
        disk_upper[:-1] = assigned_upper[:-1]
        q_current = np.minimum(np.maximum(q_current, lower), upper)

        def objective(q: np.ndarray) -> float:
            if use_cpp_packed:
                return _ocp_fast.packed_objective(
                    q,
                    n_controls=n,
                    disc_count=len(vehicle.disc_offsets_m),
                    vehicle=vehicle,
                    params=params,
                    penalty_weight=current_weight,
                )
            states_obj, controls_obj, disk_centers_obj, tf_obj = _unpack(q, n, len(vehicle.disc_offsets_m))
            return float(
                evaluate_formula16_objective(states_obj, tf_obj, params)
                + current_weight
                * evaluate_formula23_penalty(
                    states_obj,
                    controls_obj,
                    tf_obj,
                    vehicle,
                    params,
                    corridor_boxes=current_corridor_boxes,
                    disk_centers=disk_centers_obj,
                )
            )

        def gradient(q: np.ndarray) -> np.ndarray:
            if use_cpp_packed:
                return _ocp_fast.packed_gradient(
                    q,
                    n_controls=n,
                    disc_count=len(vehicle.disc_offsets_m),
                    vehicle=vehicle,
                    params=params,
                    penalty_weight=current_weight,
                )
            states_obj, controls_obj, disk_centers_obj, tf_obj = _unpack(q, n, len(vehicle.disc_offsets_m))
            grad16_states, grad16_controls, grad16_tf = _formula16_gradient(states_obj, controls_obj, tf_obj, params)
            grad23_states, grad23_controls, grad23_disks, grad23_tf = _formula23_penalty_gradient(
                states_obj,
                controls_obj,
                disk_centers_obj,
                tf_obj,
                vehicle,
                params,
            )
            return _pack(
                grad16_states + current_weight * grad23_states,
                grad16_controls + current_weight * grad23_controls,
                current_weight * grad23_disks,
                grad16_tf + current_weight * grad23_tf,
            )

        result = minimize_ipopt(
            objective,
            q_current,
            jac=gradient,
            bounds=list(zip(lower, upper)),
            options={
                "print_level": 0,
                "max_iter": max(1, int(params.ipopt_max_iterations)),
                "tol": 1e-6,
                "hessian_approximation": "limited-memory",
            },
        )
        q_current = np.asarray(result.x, dtype=float)
        states, controls, disk_centers, tf = _unpack(q_current, n, len(vehicle.disc_offsets_m))
        raw_message = result.message.decode("utf-8", errors="replace") if isinstance(result.message, bytes) else str(result.message)
        message = raw_message
        total_ipopt_iterations += int(result.nit)
        outer_iterations = outer + 1
        components = evaluate_formula23_components(
            states,
            controls,
            tf,
            vehicle,
            params,
            corridor_boxes=current_corridor_boxes,
            disk_centers=disk_centers,
        )
        if components["jinf"] <= float(params.etol):
            break
        penalty_weight *= float(params.penalty_growth)

    return (
        states,
        controls,
        disk_centers,
        tf,
        f"ipopt:{message}",
        total_ipopt_iterations,
        outer_iterations,
        final_penalty_weight,
        current_corridor_boxes,
    )
