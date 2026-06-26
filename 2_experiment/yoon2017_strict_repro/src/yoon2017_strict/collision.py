from __future__ import annotations

import math
from typing import Sequence

from .bezier import BiarcEdge, CubicBezier
from .config import VehicleParams
from .grid import GridMap


def _vh_vr_kappa(seg: CubicBezier, t: float) -> tuple[tuple[float, float], tuple[float, float], float, float]:
    dx, dy = seg.deriv(t)
    speed = math.hypot(dx, dy)
    if speed <= 1e-12:
        return (1.0, 0.0), (0.0, 1.0), 0.0, 0.0
    vh = (dx / speed, dy / speed)
    d2x, d2y = seg.deriv2(t)
    cross_b = dx * d2y - dy * d2x
    kappa = abs(cross_b) / (speed ** 3 + 1e-18)
    if kappa <= 1e-9 or abs(cross_b) <= 1e-12:
        return vh, (-vh[1], vh[0]), 0.0, 0.0
    bdotbb = dx * d2x + dy * d2y
    speed2 = speed * speed
    nx = speed2 * d2x - bdotbb * dx
    ny = speed2 * d2y - bdotbb * dy
    nn = math.hypot(nx, ny)
    if nn <= 1e-12:
        return vh, (-vh[1], vh[0]), kappa, 0.0
    vr = (-nx / nn, -ny / nn)
    cross_z = vh[0] * vr[1] - vh[1] * vr[0]
    return vh, vr, float(kappa), float(cross_z)


def _corner_pf_right(vh: tuple[float, float], vehicle: VehicleParams) -> tuple[float, float]:
    perp = (vh[1], -vh[0])
    return (
        0.5 * vehicle.width_m * perp[0] + vehicle.front_overhang_m * vh[0],
        0.5 * vehicle.width_m * perp[1] + vehicle.front_overhang_m * vh[1],
    )


def _corner_pf_left(vh: tuple[float, float], vehicle: VehicleParams) -> tuple[float, float]:
    perp = (-vh[1], vh[0])
    return (
        0.5 * vehicle.width_m * perp[0] + vehicle.front_overhang_m * vh[0],
        0.5 * vehicle.width_m * perp[1] + vehicle.front_overhang_m * vh[1],
    )


def _corner_pr_right(vh: tuple[float, float], vehicle: VehicleParams) -> tuple[float, float]:
    return (0.5 * vehicle.width_m * vh[1], -0.5 * vehicle.width_m * vh[0])


def _corner_pr_left(vh: tuple[float, float], vehicle: VehicleParams) -> tuple[float, float]:
    return (-0.5 * vehicle.width_m * vh[1], 0.5 * vehicle.width_m * vh[0])


def refine_dominant_trajectories(
    seg: CubicBezier,
    vehicle: VehicleParams,
    *,
    n_samples: int,
) -> tuple[
    list[tuple[float, float]],
    list[tuple[float, float]],
    list[tuple[float, float]],
    list[tuple[float, float]],
    list[float],
    list[tuple[float, float]],
]:
    n = max(8, int(n_samples))
    pf: list[tuple[float, float]] = []
    pr: list[tuple[float, float]] = []
    vhs: list[tuple[float, float]] = []
    vrs: list[tuple[float, float]] = []
    crosses: list[float] = []
    pts: list[tuple[float, float]] = []
    samples = []
    for i in range(n + 1):
        t = i / n
        bx, by = seg.point(t)
        vh, vr, kappa, cross_z = _vh_vr_kappa(seg, t)
        samples.append((t, (bx, by), vh, vr, kappa, cross_z))

    for _t, (bx, by), vh, vr, kappa, cross_z in samples:
        if kappa <= 1e-9:
            pf.append((bx, by))
            pr.append((bx, by))
        else:
            inv_k = 1.0 / kappa
            cx = bx - inv_k * vr[0]
            cy = by - inv_k * vr[1]
            r_out = math.hypot(inv_k + 0.5 * vehicle.width_m, vehicle.front_overhang_m)
            vfx = vehicle.front_overhang_m * vh[0] + (inv_k + 0.5 * vehicle.width_m) * vr[0]
            vfy = vehicle.front_overhang_m * vh[1] + (inv_k + 0.5 * vehicle.width_m) * vr[1]
            vf_mag = math.hypot(vfx, vfy)
            if vf_mag <= 1e-12:
                pf.append((bx, by))
            else:
                pf.append((cx + r_out * vfx / vf_mag, cy + r_out * vfy / vf_mag))
            r_in = inv_k - 0.5 * vehicle.width_m
            pr.append((cx + r_in * vr[0], cy + r_in * vr[1]))
        vhs.append(vh)
        vrs.append(vr)
        crosses.append(cross_z)
        pts.append((bx, by))

    eps_zero = 1e-6
    for i, (_t, base, vh, _vr, _kappa, cross_z) in enumerate(samples):
        if abs(cross_z) > eps_zero:
            continue
        if i + 1 <= n and abs(samples[i + 1][5]) > eps_zero:
            next_cross = samples[i + 1][5]
            if next_cross > 0.0:
                pf[i] = (base[0] + _corner_pf_right(vh, vehicle)[0], base[1] + _corner_pf_right(vh, vehicle)[1])
                pr[i] = (base[0] + _corner_pr_left(vh, vehicle)[0], base[1] + _corner_pr_left(vh, vehicle)[1])
            else:
                pf[i] = (base[0] + _corner_pf_left(vh, vehicle)[0], base[1] + _corner_pf_left(vh, vehicle)[1])
                pr[i] = (base[0] + _corner_pr_right(vh, vehicle)[0], base[1] + _corner_pr_right(vh, vehicle)[1])
            continue
        if i - 1 >= 0 and abs(samples[i - 1][5]) > eps_zero:
            prev_cross = samples[i - 1][5]
            if prev_cross > 0.0:
                pf[i] = (base[0] + _corner_pf_right(vh, vehicle)[0], base[1] + _corner_pf_right(vh, vehicle)[1])
                pr[i] = (base[0] + _corner_pr_left(vh, vehicle)[0], base[1] + _corner_pr_left(vh, vehicle)[1])
            else:
                pf[i] = (base[0] + _corner_pf_left(vh, vehicle)[0], base[1] + _corner_pf_left(vh, vehicle)[1])
                pr[i] = (base[0] + _corner_pr_right(vh, vehicle)[0], base[1] + _corner_pr_right(vh, vehicle)[1])
    return pf, pr, vhs, vrs, crosses, pts


def _point_collides(grid_map: GridMap, x_m: float, y_m: float) -> bool:
    gx, gy = grid_map.world_to_grid(x_m, y_m)
    if not grid_map.in_bounds(gx, gy):
        return True
    return grid_map.is_occupied_index(gx, gy)


def _polyline_collides(points: Sequence[tuple[float, float]], grid_map: GridMap, *, collision_step_m: float) -> bool:
    for a, b in zip(points, points[1:]):
        seg_len = math.hypot(b[0] - a[0], b[1] - a[1])
        n_sub = max(1, int(math.ceil(seg_len / max(float(collision_step_m), 1e-6))))
        for k in range(n_sub + 1):
            s = k / n_sub
            x = a[0] + (b[0] - a[0]) * s
            y = a[1] + (b[1] - a[1]) * s
            if _point_collides(grid_map, x, y):
                return True
    return False


def _dominant_trajectories_collide(
    pf: Sequence[tuple[float, float]],
    pr: Sequence[tuple[float, float]],
    grid_map: GridMap,
    *,
    collision_step_m: float,
) -> bool:
    return _polyline_collides(pf, grid_map, collision_step_m=collision_step_m) or _polyline_collides(
        pr,
        grid_map,
        collision_step_m=collision_step_m,
    )


def vehicle_rectangle_collides(
    grid_map: GridMap,
    vehicle: VehicleParams,
    x_m: float,
    y_m: float,
    theta_rad: float,
) -> bool:
    gx, gy = grid_map.world_to_grid(x_m, y_m)
    if not grid_map.in_bounds(gx, gy):
        return True
    res = float(grid_map.resolution)
    reach = max(float(vehicle.front_overhang_m), float(vehicle.rear_overhang_m)) + 0.5 * float(vehicle.width_m) + res
    cells = int(math.ceil(reach / res)) + 1
    c = math.cos(float(theta_rad))
    s = math.sin(float(theta_rad))
    half_width = 0.5 * float(vehicle.width_m)
    for rx in (-float(vehicle.rear_overhang_m), float(vehicle.front_overhang_m)):
        for ry in (-half_width, half_width):
            wx = float(x_m) + c * rx - s * ry
            wy = float(y_m) + s * rx + c * ry
            cgx, cgy = grid_map.world_to_grid(wx, wy)
            if not grid_map.in_bounds(cgx, cgy):
                return True
    for yy in range(gy - cells, gy + cells + 1):
        for xx in range(gx - cells, gx + cells + 1):
            if not grid_map.in_bounds(xx, yy):
                continue
            if not grid_map.is_occupied_index(xx, yy):
                continue
            wx, wy = grid_map.grid_to_world(xx, yy)
            dx = wx - float(x_m)
            dy = wy - float(y_m)
            rx = c * dx + s * dy
            ry = -s * dx + c * dy
            if (-vehicle.rear_overhang_m - 0.5 * res) <= rx <= (vehicle.front_overhang_m + 0.5 * res):
                if abs(ry) <= half_width + 0.5 * res:
                    return True
    return False


def _transition_rectangles_collide(
    pts: Sequence[tuple[float, float]],
    vhs: Sequence[tuple[float, float]],
    crosses: Sequence[float],
    grid_map: GridMap,
    vehicle: VehicleParams,
) -> bool:
    if not pts:
        return False
    checks: list[int] = [0, len(pts) - 1]
    eps_zero = 1e-6
    for i in range(1, len(pts)):
        if crosses[i] * crosses[i - 1] < -eps_zero * eps_zero:
            checks.extend([i - 1, i])
    for i in sorted(set(checks)):
        vh = vhs[i]
        if vehicle_rectangle_collides(grid_map, vehicle, pts[i][0], pts[i][1], math.atan2(vh[1], vh[0])):
            return True
    return False


def _sampled_rectangles_collide(
    pts: Sequence[tuple[float, float]],
    vhs: Sequence[tuple[float, float]],
    grid_map: GridMap,
    vehicle: VehicleParams,
) -> bool:
    for pt, vh in zip(pts, vhs):
        if vehicle_rectangle_collides(grid_map, vehicle, pt[0], pt[1], math.atan2(vh[1], vh[0])):
            return True
    return False


def _straight_segment_rectangles_collide(
    line: tuple[object, object] | None,
    grid_map: GridMap,
    vehicle: VehicleParams,
    *,
    collision_step_m: float,
) -> bool:
    if line is None:
        return False
    start, end = line
    sx, sy = float(start.x), float(start.y)
    ex, ey = float(end.x), float(end.y)
    seg_len = math.hypot(ex - sx, ey - sy)
    if seg_len <= 1e-12:
        return vehicle_rectangle_collides(grid_map, vehicle, sx, sy, float(start.theta))
    theta = math.atan2(ey - sy, ex - sx)
    n = max(1, int(math.ceil(seg_len / max(float(collision_step_m), 1e-6))))
    for i in range(n + 1):
        s = i / n
        x = sx + (ex - sx) * s
        y = sy + (ey - sy) * s
        if vehicle_rectangle_collides(grid_map, vehicle, x, y, theta):
            return True
    return False


def obstacle_free(
    edge: BiarcEdge,
    vehicle: VehicleParams,
    grid_map: GridMap,
    *,
    samples_per_segment: int,
    collision_step_m: float,
) -> bool:
    if _straight_segment_rectangles_collide(
        edge.straight_start,
        grid_map,
        vehicle,
        collision_step_m=collision_step_m,
    ):
        return False
    for seg in (edge.seg1, edge.seg2):
        pf, pr, vhs, _vrs, crosses, pts = refine_dominant_trajectories(seg, vehicle, n_samples=samples_per_segment)
        if _dominant_trajectories_collide(pf, pr, grid_map, collision_step_m=collision_step_m):
            return False
        if _transition_rectangles_collide(pts, vhs, crosses, grid_map, vehicle):
            return False
        if _sampled_rectangles_collide(pts, vhs, grid_map, vehicle):
            return False
    if _straight_segment_rectangles_collide(
        edge.straight_end,
        grid_map,
        vehicle,
        collision_step_m=collision_step_m,
    ):
        return False
    return True
