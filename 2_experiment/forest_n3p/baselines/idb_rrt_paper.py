"""Paper-oriented iDb-RRT baseline.

参考 Ortiz-Haro et al. (IROS 2024) Algorithm 1--4 和 Section IV-E。此实现
保留论文中的 Db-RRT + TO 结构，同时使用本项目已有 Ackermann 运动学、footprint
和 EDT collision checker。
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np

from forest_n3p.baselines.common import (
    PlannerResult,
    build_ackermann_action_table_35,
    default_start_theta,
)
from forest_n3p.baselines.idb_rrt_local import (
    _astar_grid_guide,
    _rollout,
)
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker
from forest_n3p.third_party.pathplan.common import clamp, wrap_angle
from forest_n3p.third_party.pathplan.hybrid_a_star.obstacle_field import (
    compute_obstacle_distance_field,
    query_distance,
)


@dataclass(frozen=True)
class _State:
    x: float
    y: float
    theta: float
    v: float
    delta: float


@dataclass(frozen=True)
class _MotionPrimitive:
    states: tuple[_State, ...]
    controls: tuple[tuple[float, float], ...]
    cost: float


@dataclass(frozen=True)
class _BoxSpec:
    length: float
    width: float
    center_shift: float


class _ShiftedBoxGridChecker:
    def __init__(
        self,
        *,
        grid_map: GridMap,
        footprint: OrientedBoxFootprint | TwoCircleFootprint,
        theta_bins: int = 144,
    ) -> None:
        self._box = _box_spec_from_footprint(footprint)
        self._checker = GridFootprintChecker(
            grid_map,
            OrientedBoxFootprint(length=float(self._box.length), width=float(self._box.width)),
            theta_bins=int(theta_bins),
            padding=math.sqrt(2.0) * 0.5 * float(grid_map.resolution),
        )

    def collides_pose(self, x: float, y: float, theta: float) -> bool:
        cx = float(x) + float(self._box.center_shift) * math.cos(float(theta))
        cy = float(y) + float(self._box.center_shift) * math.sin(float(theta))
        return bool(self._checker.collides_pose(cx, cy, float(theta)))


@dataclass(frozen=True)
class _Node:
    state: _State
    parent: int
    segment: tuple[_State, ...]
    controls: tuple[tuple[float, float], ...]
    cost: float


@dataclass(frozen=True)
class _DbRRTResult:
    success: bool
    states: list[_State]
    controls: list[tuple[float, float]]
    iterations: int
    nodes: int
    best_goal_error_m: float
    termination: str
    skipped_collision: int
    skipped_no_primitive: int
    skipped_near_existing: int


def _box_spec_from_footprint(footprint: OrientedBoxFootprint | TwoCircleFootprint) -> _BoxSpec:
    if isinstance(footprint, OrientedBoxFootprint):
        return _BoxSpec(length=float(footprint.length), width=float(footprint.width), center_shift=0.0)
    if isinstance(footprint, TwoCircleFootprint):
        # TwoCircleFootprint.from_box uses center_offset = length / 4 and
        # radius^2 = center_offset^2 + (width / 2)^2.  Reversing that mapping
        # recovers the actual local UGV rectangle while preserving rear-axle
        # center_shift.
        length = 4.0 * float(footprint.center_offset)
        half_width_sq = max(0.0, float(footprint.radius) ** 2 - float(footprint.center_offset) ** 2)
        width = 2.0 * math.sqrt(half_width_sq)
        return _BoxSpec(length=float(length), width=float(width), center_shift=float(footprint.center_shift))
    raise TypeError(f"Unsupported footprint type: {type(footprint)!r}")


def _box_corners_m(x: float, y: float, theta: float, box: _BoxSpec) -> np.ndarray:
    cx = float(x) + float(box.center_shift) * math.cos(float(theta))
    cy = float(y) + float(box.center_shift) * math.sin(float(theta))
    half_l = 0.5 * float(box.length)
    half_w = 0.5 * float(box.width)
    local = np.array(
        [[+half_l, +half_w], [+half_l, -half_w], [-half_l, -half_w], [-half_l, +half_w]],
        dtype=np.float64,
    )
    c = math.cos(float(theta))
    s = math.sin(float(theta))
    rot = np.array([[c, -s], [s, c]], dtype=np.float64)
    return (local @ rot.T) + np.array([cx, cy], dtype=np.float64)


def _sat_project(poly: np.ndarray, axis: tuple[float, float]) -> tuple[float, float]:
    vals = poly[:, 0] * axis[0] + poly[:, 1] * axis[1]
    return float(np.min(vals)), float(np.max(vals))


def _sat_overlap(poly_a: np.ndarray, poly_b: np.ndarray, axes: tuple[tuple[float, float], ...]) -> bool:
    for axis in axes:
        a_min, a_max = _sat_project(poly_a, axis)
        b_min, b_max = _sat_project(poly_b, axis)
        if a_max < b_min - 1e-12 or b_max < a_min - 1e-12:
            return False
    return True


def _occupied_cell_square_m(grid_map: GridMap, gx: int, gy: int) -> np.ndarray:
    cx, cy = grid_map.grid_to_world(int(gx), int(gy))
    half = 0.5 * float(grid_map.resolution)
    return np.array(
        [[cx - half, cy - half], [cx + half, cy - half], [cx + half, cy + half], [cx - half, cy + half]],
        dtype=np.float64,
    )


def _rectangle_collides_grid(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    x: float,
    y: float,
    theta: float,
) -> bool:
    box = _box_spec_from_footprint(footprint)
    corners = _box_corners_m(float(x), float(y), float(theta), box)
    res = float(grid_map.resolution)
    ox, oy = float(grid_map.origin[0]), float(grid_map.origin[1])
    h, w = grid_map.data.shape
    xs = corners[:, 0]
    ys = corners[:, 1]
    x_min, x_max = float(np.min(xs)), float(np.max(xs))
    y_min, y_max = float(np.min(ys)), float(np.max(ys))
    if (
        x_min < ox - 0.5 * res
        or x_max > ox + (w - 1) * res + 0.5 * res
        or y_min < oy - 0.5 * res
        or y_max > oy + (h - 1) * res + 0.5 * res
    ):
        return True

    edge0 = corners[1] - corners[0]
    edge1 = corners[3] - corners[0]
    axes = (
        (float(edge0[0]), float(edge0[1])),
        (float(edge1[0]), float(edge1[1])),
        (1.0, 0.0),
        (0.0, 1.0),
    )
    gx_min = max(0, int(math.floor((x_min - ox) / res - 0.5)))
    gx_max = min(w - 1, int(math.ceil((x_max - ox) / res + 0.5)))
    gy_min = max(0, int(math.floor((y_min - oy) / res - 0.5)))
    gy_max = min(h - 1, int(math.ceil((y_max - oy) / res + 0.5)))
    for gy in range(gy_min, gy_max + 1):
        for gx in range(gx_min, gx_max + 1):
            if not grid_map.is_occupied_index(gx, gy):
                continue
            if _sat_overlap(corners, _occupied_cell_square_m(grid_map, gx, gy), axes):
                return True
    return False


def _paper_collides_pose(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    x: float,
    y: float,
    theta: float,
) -> bool:
    if isinstance(collision_checker, _ShiftedBoxGridChecker):
        return bool(collision_checker.collides_pose(float(x), float(y), float(theta)))
    return _rectangle_collides_grid(
        grid_map=grid_map,
        footprint=footprint,
        x=float(x),
        y=float(y),
        theta=float(theta),
    )


def _paper_path_collision_free(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    points_m: list[tuple[float, float]],
    thetas: list[float],
    interp_step_m: float | None = None,
) -> bool:
    if not points_m:
        return True
    step = float(interp_step_m) if interp_step_m is not None else 0.5 * float(grid_map.resolution)
    if not (step > 0.0):
        step = 0.5 * float(grid_map.resolution)

    for (x, y), theta in zip(points_m, thetas):
        if _paper_collides_pose(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            x=float(x),
            y=float(y),
            theta=float(theta),
        ):
            return False

    for i in range(len(points_m) - 1):
        x0, y0 = points_m[i]
        x1, y1 = points_m[i + 1]
        t0, t1 = float(thetas[i]), float(thetas[i + 1])
        dx = float(x1) - float(x0)
        dy = float(y1) - float(y0)
        seg_len = math.hypot(dx, dy)
        if seg_len <= step:
            continue
        n_sub = int(math.ceil(seg_len / step))
        d_theta = wrap_angle(t1 - t0)
        for k in range(1, n_sub):
            tt = float(k) / float(n_sub)
            if _paper_collides_pose(
                grid_map=grid_map,
                footprint=footprint,
                collision_checker=collision_checker,
                x=float(x0) + tt * dx,
                y=float(y0) + tt * dy,
                theta=wrap_angle(t0 + tt * d_theta),
            ):
                return False
    return True


def _heading_diff(a: float, b: float) -> float:
    return abs(wrap_angle(float(a) - float(b)))


def _state_distance(
    a: _State,
    b: _State,
    *,
    theta_weight_m: float,
    speed_weight_m: float,
    steer_weight_m: float,
) -> float:
    dxy2 = (float(a.x) - float(b.x)) ** 2 + (float(a.y) - float(b.y)) ** 2
    dtheta = float(theta_weight_m) * _heading_diff(a.theta, b.theta)
    dv = float(speed_weight_m) * (float(a.v) - float(b.v))
    dd = float(steer_weight_m) * _heading_diff(a.delta, b.delta)
    return float(math.sqrt(dxy2 + dtheta * dtheta + dv * dv + dd * dd))


def _local_to_paper_state(s: Any) -> _State:
    return _State(
        x=float(s.x),
        y=float(s.y),
        theta=float(s.theta),
        v=float(s.v),
        delta=float(s.delta),
    )


def _generate_motion_primitive_library(
    *,
    params: AckermannParams,
    target_v_m_s: float,
    v_min_m_s: float,
    delta_dot_max_rad_s: float,
    a_max_m_s2: float,
    primitive_duration_s: float,
    dt_s: float,
) -> list[_MotionPrimitive]:
    """生成可复用 motion primitive 集合 M_L。"""
    action_table = build_ackermann_action_table_35(
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
    )
    durations = (
        0.5 * float(primitive_duration_s),
        float(primitive_duration_s),
        1.5 * float(primitive_duration_s),
    )
    start_vs = (
        clamp(float(target_v_m_s), float(v_min_m_s), float(params.v_max)),
        clamp(float(target_v_m_s) * 0.8, float(v_min_m_s), float(params.v_max)),
        clamp(float(target_v_m_s) * 1.1, float(v_min_m_s), float(params.v_max)),
    )
    start_deltas = (
        0.0,
        -0.35 * float(params.max_steer),
        0.35 * float(params.max_steer),
    )

    def make_primitive(*, duration: float, start_v: float, start_delta: float, delta_dot: float, accel: float) -> _MotionPrimitive | None:
        start = _State(
            x=0.0,
            y=0.0,
            theta=0.0,
            v=float(start_v),
            delta=float(start_delta),
        )
        rolled = _rollout(
            state=start,
            delta_dot=float(delta_dot),
            accel=float(accel),
            params=params,
            duration_s=float(duration),
            dt_s=float(dt_s),
            v_min_m_s=float(v_min_m_s),
            v_max_m_s=float(params.v_max),
        )
        states = (start,) + tuple(_local_to_paper_state(s) for s in rolled)
        if len(states) < 2:
            return None
        controls = tuple((float(delta_dot), float(accel)) for _ in range(len(states) - 1))
        cost = 0.0
        prev = states[0]
        for s in states[1:]:
            cost += math.hypot(float(s.x) - float(prev.x), float(s.y) - float(prev.y))
            prev = s
        if cost <= 1e-6:
            return None
        return _MotionPrimitive(states=states, controls=controls, cost=float(cost))

    primitives: list[_MotionPrimitive] = []
    primary_v = start_vs[0]
    primary_actions = sorted(
        [(float(delta_dot), float(accel)) for delta_dot, accel in action_table],
        key=lambda u: (abs(u[0]), abs(u[1]), u[0], u[1]),
    )
    for delta_dot, accel in primary_actions:
        primitive = make_primitive(
            duration=float(primitive_duration_s),
            start_v=float(primary_v),
            start_delta=0.0,
            delta_dot=float(delta_dot),
            accel=float(accel),
        )
        if primitive is not None:
            primitives.append(primitive)

    seen = {
        (
            round(float(p.states[0].v), 6),
            round(float(p.states[0].delta), 6),
            len(p.controls),
            round(float(p.controls[0][0]), 6),
            round(float(p.controls[0][1]), 6),
        )
        for p in primitives
    }
    for duration in durations:
        for start_v in start_vs:
            for start_delta in start_deltas:
                for delta_dot, accel in action_table:
                    primitive = make_primitive(
                        duration=float(duration),
                        start_v=float(start_v),
                        start_delta=float(start_delta),
                        delta_dot=float(delta_dot),
                        accel=float(accel),
                    )
                    if primitive is None:
                        continue
                    key = (
                        round(float(primitive.states[0].v), 6),
                        round(float(primitive.states[0].delta), 6),
                        len(primitive.controls),
                        round(float(primitive.controls[0][0]), 6),
                        round(float(primitive.controls[0][1]), 6),
                    )
                    if key in seen:
                        continue
                    seen.add(key)
                    primitives.append(primitive)
    return primitives


def _transform_primitive(primitive: _MotionPrimitive, node: _State) -> tuple[_State, ...]:
    p0 = primitive.states[0]
    rot = wrap_angle(float(node.theta) - float(p0.theta))
    c = math.cos(rot)
    s = math.sin(rot)
    out: list[_State] = []
    for ps in primitive.states:
        dx = float(ps.x) - float(p0.x)
        dy = float(ps.y) - float(p0.y)
        out.append(
            _State(
                x=float(node.x) + c * dx - s * dy,
                y=float(node.y) + s * dx + c * dy,
                theta=wrap_angle(float(node.theta) + wrap_angle(float(ps.theta) - float(p0.theta))),
                v=float(ps.v),
                delta=float(ps.delta),
            )
        )
    return tuple(out)


def _segment_is_collision_free(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    segment: tuple[_State, ...],
) -> bool:
    for s in segment:
        if _paper_collides_pose(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            x=float(s.x),
            y=float(s.y),
            theta=float(s.theta),
        ):
            return False
    return True


def _nearest_node_indices(
    *,
    sample: _State,
    xs: np.ndarray,
    ys: np.ndarray,
    thetas: np.ndarray,
    n_nodes: int,
    k: int,
    theta_weight_m: float,
) -> np.ndarray:
    dx = xs[:n_nodes] - float(sample.x)
    dy = ys[:n_nodes] - float(sample.y)
    dtheta = np.arctan2(
        np.sin(thetas[:n_nodes] - float(sample.theta)),
        np.cos(thetas[:n_nodes] - float(sample.theta)),
    )
    score = dx * dx + dy * dy + (float(theta_weight_m) * dtheta) ** 2
    kk = min(max(1, int(k)), int(n_nodes))
    if kk == 1:
        return np.array([int(np.argmin(score))], dtype=np.int64)
    idx = np.argpartition(score, kk - 1)[:kk]
    return idx[np.argsort(score[idx])]


def _nearest_tree_distance(
    *,
    state: _State,
    xs: np.ndarray,
    ys: np.ndarray,
    n_nodes: int,
    skip_idx: int,
) -> float:
    if n_nodes <= 1:
        return float("inf")
    dx = xs[:n_nodes] - float(state.x)
    dy = ys[:n_nodes] - float(state.y)
    dist2 = dx * dx + dy * dy
    if 0 <= int(skip_idx) < int(n_nodes):
        dist2[int(skip_idx)] = float("inf")
    return float(math.sqrt(float(np.min(dist2))))


def _sample_target(
    *,
    rng: np.random.Generator,
    grid_map: GridMap,
    guide: list[tuple[float, float]],
    goal: _State,
    goal_sample_rate: float,
    guide_sample_rate: float,
    guide_noise_m: float,
) -> tuple[_State, bool]:
    r = float(rng.random())
    if r < float(goal_sample_rate):
        return goal, True

    if guide and r < float(goal_sample_rate) + float(guide_sample_rate):
        idx = int(rng.integers(0, len(guide)))
        x, y = guide[idx]
        x += float(rng.normal(0.0, float(guide_noise_m)))
        y += float(rng.normal(0.0, float(guide_noise_m)))
        if idx + 1 < len(guide):
            nx, ny = guide[idx + 1]
            theta = math.atan2(ny - guide[idx][1], nx - guide[idx][0])
        elif idx > 0:
            px, py = guide[idx - 1]
            theta = math.atan2(guide[idx][1] - py, guide[idx][0] - px)
        else:
            theta = goal.theta
        return _State(x=float(x), y=float(y), theta=wrap_angle(theta), v=goal.v, delta=0.0), True

    x, y, theta = grid_map.random_free_state(rng)
    return _State(x=float(x), y=float(y), theta=float(theta), v=goal.v, delta=0.0), False


def _select_applicable_primitive(
    *,
    node: _Node,
    sample: _State,
    primitives: list[_MotionPrimitive],
    delta_m: float,
    focused: bool,
    rng: np.random.Generator,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    params: AckermannParams,
    dt_s: float,
    v_min_m_s: float,
    theta_weight_m: float,
    speed_weight_m: float,
    steer_weight_m: float,
) -> tuple[tuple[_State, ...], _MotionPrimitive] | None:
    order = range(len(primitives)) if focused else rng.permutation(len(primitives))
    best: tuple[tuple[_State, ...], _MotionPrimitive] | None = None
    best_score = float("inf")
    for raw_idx in order:
        primitive = primitives[int(raw_idx)]
        transformed = _transform_primitive(primitive, node.state)
        discontinuity = _state_distance(
            node.state,
            transformed[0],
            theta_weight_m=float(theta_weight_m),
            speed_weight_m=float(speed_weight_m),
            steer_weight_m=float(steer_weight_m),
        )
        if discontinuity > float(delta_m):
            continue
        segment = tuple(transformed)
        if not segment:
            continue
        if not _segment_is_collision_free(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            segment=segment,
        ):
            continue
        if not focused:
            return segment, primitive
        end = segment[-1]
        score = _state_distance(
            end,
            sample,
            theta_weight_m=float(theta_weight_m),
            speed_weight_m=float(speed_weight_m),
            steer_weight_m=float(steer_weight_m),
        )
        if score < best_score:
            best_score = float(score)
            best = (segment, primitive)
    return best


def _reconstruct(nodes: list[_Node], goal_idx: int) -> tuple[list[_State], list[tuple[float, float]]]:
    chain: list[int] = []
    idx = int(goal_idx)
    while idx >= 0:
        chain.append(idx)
        idx = int(nodes[idx].parent)
    chain.reverse()

    states = [nodes[chain[0]].state]
    controls: list[tuple[float, float]] = []
    for node_idx in chain[1:]:
        node = nodes[node_idx]
        states.extend(node.segment)
        controls.extend(node.controls)
    return states, controls


def _db_rrt_search(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    params: AckermannParams,
    start: _State,
    goal: _State,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    rng: np.random.Generator,
    primitives: list[_MotionPrimitive],
    delta_m: float,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    iteration_budget: int,
    deadline_s: float,
    goal_sample_rate: float,
    guide_sample_rate: float,
    guide_noise_m: float,
    nearest_k: int,
    dt_s: float,
    v_min_m_s: float,
    theta_weight_m: float,
    speed_weight_m: float,
    steer_weight_m: float,
) -> _DbRRTResult:
    guide = _astar_grid_guide(grid_map=grid_map, start_xy=start_xy, goal_xy=goal_xy)
    capacity = max(2, int(iteration_budget) + 2)
    xs = np.empty(capacity, dtype=np.float64)
    ys = np.empty(capacity, dtype=np.float64)
    thetas = np.empty(capacity, dtype=np.float64)
    nodes: list[_Node] = [_Node(state=start, parent=-1, segment=tuple(), controls=tuple(), cost=0.0)]
    xs[0], ys[0], thetas[0] = start.x, start.y, start.theta

    best_goal_idx = 0
    best_goal_error = math.hypot(float(start.x) - float(goal.x), float(start.y) - float(goal.y))
    goal_idx: int | None = None
    skipped_collision = 0
    skipped_no_primitive = 0
    skipped_near_existing = 0
    it = 0

    for it in range(1, int(iteration_budget) + 1):
        if time.perf_counter() >= float(deadline_s) or len(nodes) >= capacity:
            break

        sample, focused = _sample_target(
            rng=rng,
            grid_map=grid_map,
            guide=guide,
            goal=goal,
            goal_sample_rate=float(goal_sample_rate),
            guide_sample_rate=float(guide_sample_rate),
            guide_noise_m=float(guide_noise_m),
        )
        candidates = _nearest_node_indices(
            sample=sample,
            xs=xs,
            ys=ys,
            thetas=thetas,
            n_nodes=len(nodes),
            k=int(nearest_k),
            theta_weight_m=float(theta_weight_m),
        )
        added = False
        for parent_idx in candidates:
            parent = nodes[int(parent_idx)]
            selected = _select_applicable_primitive(
                node=parent,
                sample=sample,
                primitives=primitives,
                delta_m=float(delta_m),
                focused=bool(focused),
                rng=rng,
                grid_map=grid_map,
                footprint=footprint,
                collision_checker=collision_checker,
                params=params,
                dt_s=float(dt_s),
                v_min_m_s=float(v_min_m_s),
                theta_weight_m=float(theta_weight_m),
                speed_weight_m=float(speed_weight_m),
                steer_weight_m=float(steer_weight_m),
            )
            if selected is None:
                continue
            segment, primitive = selected
            end = segment[-1]
            if _paper_collides_pose(
                grid_map=grid_map,
                footprint=footprint,
                collision_checker=collision_checker,
                x=end.x,
                y=end.y,
                theta=end.theta,
            ):
                skipped_collision += 1
                continue
            min_dist = _nearest_tree_distance(
                state=end,
                xs=xs,
                ys=ys,
                n_nodes=len(nodes),
                skip_idx=int(parent_idx),
            )
            goal_error = math.hypot(float(end.x) - float(goal.x), float(end.y) - float(goal.y))
            reaches_goal = (
                goal_error <= max(float(goal_xy_tol_m), min(float(delta_m), 0.75))
                and _heading_diff(end.theta, goal.theta) <= float(goal_theta_tol_rad)
            )
            if not reaches_goal and min_dist <= max(0.2, 0.5 * float(delta_m)):
                skipped_near_existing += 1
                continue

            nodes.append(
                _Node(
                    state=end,
                    parent=int(parent_idx),
                    segment=segment,
                    controls=primitive.controls,
                    cost=float(parent.cost) + float(primitive.cost),
                )
            )
            new_idx = len(nodes) - 1
            xs[new_idx], ys[new_idx], thetas[new_idx] = end.x, end.y, end.theta
            if goal_error < best_goal_error:
                best_goal_error = float(goal_error)
                best_goal_idx = new_idx
            if reaches_goal:
                goal_idx = new_idx
            added = True
            break

        if not added:
            skipped_no_primitive += 1
        if goal_idx is not None:
            break

    success = goal_idx is not None
    states, controls = _reconstruct(nodes, int(goal_idx if goal_idx is not None else best_goal_idx))
    return _DbRRTResult(
        success=bool(success),
        states=states,
        controls=controls,
        iterations=int(it),
        nodes=int(len(nodes)),
        best_goal_error_m=float(best_goal_error),
        termination="goal_reached" if success else "timeout_or_budget",
        skipped_collision=int(skipped_collision),
        skipped_no_primitive=int(skipped_no_primitive),
        skipped_near_existing=int(skipped_near_existing),
    )


def _simulate_controls(
    *,
    start: _State,
    controls: list[tuple[float, float]],
    params: AckermannParams,
    dt_s: float,
    v_min_m_s: float,
) -> list[_State]:
    x, y, theta = float(start.x), float(start.y), float(start.theta)
    v, delta = float(start.v), float(start.delta)
    out = [start]
    dt = float(dt_s)
    for delta_dot, accel in controls:
        delta = clamp(delta + float(delta_dot) * dt, -params.max_steer, params.max_steer)
        v = clamp(v + float(accel) * dt, float(v_min_m_s), float(params.v_max))
        x += v * dt * math.cos(theta)
        y += v * dt * math.sin(theta)
        theta = wrap_angle(theta + (v * dt / params.wheelbase) * math.tan(delta))
        out.append(_State(x=float(x), y=float(y), theta=float(theta), v=float(v), delta=float(delta)))
    return out


def _continuous_guess_for_control_horizon(states: list[_State], *, control_count: int) -> list[_State]:
    """移除 Db-RRT discontinuity anchor，使猜测状态数匹配控制时域。"""
    if not states:
        return []
    expected = max(1, int(control_count) + 1)
    if len(states) <= expected:
        return list(states)

    filtered: list[_State] = []
    for state in states:
        if filtered:
            prev = filtered[-1]
            same_pose = (
                math.hypot(float(state.x) - float(prev.x), float(state.y) - float(prev.y)) <= 1e-9
                and _heading_diff(state.theta, prev.theta) <= 1e-9
            )
            if same_pose:
                continue
        filtered.append(state)

    if len(filtered) <= expected:
        return filtered

    idxs = np.linspace(0, len(filtered) - 1, expected)
    return [filtered[int(round(i))] for i in idxs]


def _controls_from_state_guess(
    *,
    states: list[_State],
    start: _State,
    params: AckermannParams,
    dt_s: float,
    v_min_m_s: float,
    delta_dot_max_rad_s: float,
    a_max_m_s2: float,
) -> list[tuple[float, float]]:
    """从 Db-RRT 状态猜测反推 control-shooting 初值。"""
    if len(states) < 2:
        return []
    controls: list[tuple[float, float]] = []
    current_v = float(start.v)
    current_delta = float(start.delta)
    dt = float(dt_s)
    for prev, nxt in zip(states[:-1], states[1:]):
        dx = float(nxt.x) - float(prev.x)
        dy = float(nxt.y) - float(prev.y)
        desired_v = clamp(math.hypot(dx, dy) / max(dt, 1e-6), float(v_min_m_s), float(params.v_max))
        dtheta = wrap_angle(float(nxt.theta) - float(prev.theta))
        desired_delta = math.atan2(float(params.wheelbase) * dtheta, max(desired_v * dt, 1e-6))
        desired_delta = clamp(desired_delta, -float(params.max_steer), float(params.max_steer))
        accel = clamp((desired_v - current_v) / max(dt, 1e-6), -float(a_max_m_s2), float(a_max_m_s2))
        delta_dot = clamp(
            (desired_delta - current_delta) / max(dt, 1e-6),
            -float(delta_dot_max_rad_s),
            float(delta_dot_max_rad_s),
        )
        controls.append((float(delta_dot), float(accel)))
        current_delta = clamp(current_delta + float(delta_dot) * dt, -float(params.max_steer), float(params.max_steer))
        current_v = clamp(current_v + float(accel) * dt, float(v_min_m_s), float(params.v_max))
    return controls


def _states_are_valid_solution(
    *,
    states: list[_State],
    goal: _State,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
) -> bool:
    if not states:
        return False
    final = states[-1]
    goal_error = math.hypot(float(final.x) - float(goal.x), float(final.y) - float(goal.y))
    if goal_error > float(goal_xy_tol_m):
        return False
    if _heading_diff(final.theta, goal.theta) > float(goal_theta_tol_rad):
        return False
    points_m = [(float(s.x), float(s.y)) for s in states]
    thetas = [float(s.theta) for s in states]
    return _paper_path_collision_free(
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=None,
        points_m=points_m,
        thetas=thetas,
    )


def _tracking_shooting_candidate(
    *,
    guess_states: list[_State],
    start: _State,
    goal: _State,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    params: AckermannParams,
    dt_s: float,
    v_min_m_s: float,
    delta_dot_max_rad_s: float,
    a_max_m_s2: float,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
) -> tuple[bool, list[_State], list[tuple[float, float]]]:
    if len(guess_states) < 2:
        return False, [start], []
    dt = float(dt_s)
    state = start
    states = [start]
    controls: list[tuple[float, float]] = []
    target_idx = 1
    max_steps = min(1_200, max(400, 3 * len(guess_states)))
    lookahead_m = max(0.45, 4.0 * float(grid_map.resolution))

    for _ in range(int(max_steps)):
        while target_idx < len(guess_states) - 1:
            target = guess_states[target_idx]
            if math.hypot(float(target.x) - float(state.x), float(target.y) - float(state.y)) >= lookahead_m:
                break
            target_idx += 1
        if math.hypot(float(goal.x) - float(state.x), float(goal.y) - float(state.y)) <= 2.0 * float(goal_xy_tol_m):
            target = goal
        else:
            target = guess_states[target_idx]

        dx = float(target.x) - float(state.x)
        dy = float(target.y) - float(state.y)
        target_dist = max(math.hypot(dx, dy), 1e-6)
        alpha = wrap_angle(math.atan2(dy, dx) - float(state.theta))
        desired_delta = math.atan2(2.0 * float(params.wheelbase) * math.sin(alpha), target_dist)
        desired_delta = clamp(desired_delta, -float(params.max_steer), float(params.max_steer))
        desired_v = min(float(params.v_max), max(float(v_min_m_s), 1.0))
        if target is goal and target_dist < 1.0:
            desired_v = max(float(v_min_m_s), min(desired_v, target_dist / max(dt, 1e-6)))

        delta_dot = clamp(
            (desired_delta - float(state.delta)) / max(dt, 1e-6),
            -float(delta_dot_max_rad_s),
            float(delta_dot_max_rad_s),
        )
        accel = clamp(
            (desired_v - float(state.v)) / max(dt, 1e-6),
            -float(a_max_m_s2),
            float(a_max_m_s2),
        )
        nxt = _simulate_controls(
            start=state,
            controls=[(float(delta_dot), float(accel))],
            params=params,
            dt_s=dt,
            v_min_m_s=float(v_min_m_s),
        )[-1]
        if _paper_collides_pose(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            x=nxt.x,
            y=nxt.y,
            theta=nxt.theta,
        ):
            return False, states, controls
        controls.append((float(delta_dot), float(accel)))
        states.append(nxt)
        state = nxt
        if _states_are_valid_solution(
            states=states,
            goal=goal,
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            goal_xy_tol_m=float(goal_xy_tol_m),
            goal_theta_tol_rad=float(goal_theta_tol_rad),
        ):
            return True, states, controls
    return False, states, controls


def _guided_control_shooting_repair(
    *,
    guide_states: list[_State],
    start: _State,
    goal: _State,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    params: AckermannParams,
    dt_s: float,
    primitive_duration_s: float,
    v_min_m_s: float,
    delta_dot_max_rad_s: float,
    a_max_m_s2: float,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    theta_weight_m: float,
    speed_weight_m: float,
    steer_weight_m: float,
    deadline_s: float,
) -> tuple[bool, list[_State], list[tuple[float, float]]]:
    """用 Db-RRT 状态链作 guide，从真实起点重新做 control shooting。"""
    if time.perf_counter() >= float(deadline_s):
        return False, [start], []
    db_guide = [(float(s.x), float(s.y)) for s in guide_states]
    start_xy = (
        int(round(float(start.x) / float(grid_map.resolution))),
        int(round(float(start.y) / float(grid_map.resolution))),
    )
    goal_xy = (
        int(round(float(goal.x) / float(grid_map.resolution))),
        int(round(float(goal.y) / float(grid_map.resolution))),
    )
    astar_guide = _astar_grid_guide(grid_map=grid_map, start_xy=start_xy, goal_xy=goal_xy)
    guide = astar_guide if astar_guide else db_guide
    action_table = build_ackermann_action_table_35(
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
    )
    actions = [(float(delta_dot), float(accel)) for delta_dot, accel in action_table]
    iteration_budget = 12_000
    capacity = int(iteration_budget) + 2
    xs = np.empty(capacity, dtype=np.float64)
    ys = np.empty(capacity, dtype=np.float64)
    thetas = np.empty(capacity, dtype=np.float64)
    nodes: list[_Node] = [_Node(state=start, parent=-1, segment=tuple(), controls=tuple(), cost=0.0)]
    xs[0], ys[0], thetas[0] = start.x, start.y, start.theta
    best_goal_idx = 0
    best_goal_error = math.hypot(float(start.x) - float(goal.x), float(start.y) - float(goal.y))
    goal_idx: int | None = None
    rng = np.random.default_rng(0)

    for _it in range(1, int(iteration_budget) + 1):
        if time.perf_counter() >= float(deadline_s) or len(nodes) >= capacity:
            break
        sample, _focused = _sample_target(
            rng=rng,
            grid_map=grid_map,
            guide=guide,
            goal=goal,
            goal_sample_rate=0.12,
            guide_sample_rate=0.50,
            guide_noise_m=max(0.8, 8.0 * float(grid_map.resolution)),
        )
        candidates = _nearest_node_indices(
            sample=sample,
            xs=xs,
            ys=ys,
            thetas=thetas,
            n_nodes=len(nodes),
            k=5,
            theta_weight_m=float(theta_weight_m),
        )
        best_choice: tuple[int, tuple[_State, ...], tuple[tuple[float, float], ...], float] | None = None
        best_score = float("inf")
        for parent_idx in candidates:
            if time.perf_counter() >= float(deadline_s):
                return False, [start], []
            parent = nodes[int(parent_idx)]
            for delta_dot, accel in actions:
                if time.perf_counter() >= float(deadline_s):
                    return False, [start], []
                rolled = _rollout(
                    state=parent.state,
                    delta_dot=float(delta_dot),
                    accel=float(accel),
                    params=params,
                    duration_s=float(primitive_duration_s),
                    dt_s=float(dt_s),
                    v_min_m_s=float(v_min_m_s),
                    v_max_m_s=float(params.v_max),
                )
                segment = tuple(_local_to_paper_state(s) for s in rolled)
                if not segment:
                    continue
                if not _segment_is_collision_free(
                    grid_map=grid_map,
                    footprint=footprint,
                    collision_checker=collision_checker,
                    segment=segment,
                ):
                    continue
                end = segment[-1]
                score = _state_distance(
                    end,
                    sample,
                    theta_weight_m=float(theta_weight_m),
                    speed_weight_m=float(speed_weight_m),
                    steer_weight_m=float(steer_weight_m),
                )
                if score < best_score:
                    controls = tuple((float(delta_dot), float(accel)) for _ in segment)
                    best_choice = (int(parent_idx), segment, controls, float(score))
                    best_score = float(score)
        if best_choice is None:
            continue

        parent_idx, segment, controls, _score = best_choice
        parent = nodes[int(parent_idx)]
        end = segment[-1]
        edge_cost = 0.0
        prev = parent.state
        for state in segment:
            edge_cost += math.hypot(float(state.x) - float(prev.x), float(state.y) - float(prev.y))
            prev = state
        nodes.append(
            _Node(
                state=end,
                parent=int(parent_idx),
                segment=segment,
                controls=controls,
                cost=float(parent.cost) + float(edge_cost),
            )
        )
        new_idx = len(nodes) - 1
        xs[new_idx], ys[new_idx], thetas[new_idx] = end.x, end.y, end.theta
        goal_error = math.hypot(float(end.x) - float(goal.x), float(end.y) - float(goal.y))
        if goal_error < best_goal_error:
            best_goal_error = float(goal_error)
            best_goal_idx = new_idx
        if goal_error <= float(goal_xy_tol_m) and _heading_diff(end.theta, goal.theta) <= float(goal_theta_tol_rad):
            goal_idx = new_idx
            break

    if time.perf_counter() >= float(deadline_s):
        return False, [start], []
    states, controls = _reconstruct(nodes, int(goal_idx if goal_idx is not None else best_goal_idx))
    ok = _states_are_valid_solution(
        states=states,
        goal=goal,
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=collision_checker,
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
    )
    return bool(ok), states, controls


def _build_control_objective(
    *,
    start: _State,
    goal: _State,
    guess_states: list[_State],
    params: AckermannParams,
    dt_s: float,
    v_min_m_s: float,
    dist_field: np.ndarray,
    grid_map: GridMap,
    clearance_target_m: float,
    w_goal_xy: float,
    w_goal_theta: float,
    w_deviation: float,
    w_control: float,
    w_smooth: float,
    w_clearance: float,
) -> Callable[[np.ndarray], float]:
    guess_xy = np.asarray([(s.x, s.y) for s in guess_states], dtype=np.float64)
    n_guess = int(len(guess_xy))

    def objective(z: np.ndarray) -> float:
        controls = np.asarray(z, dtype=np.float64).reshape(-1, 2)
        states = _simulate_controls(
            start=start,
            controls=[(float(a), float(b)) for a, b in controls],
            params=params,
            dt_s=float(dt_s),
            v_min_m_s=float(v_min_m_s),
        )
        last = states[-1]
        gxy = (float(last.x) - float(goal.x)) ** 2 + (float(last.y) - float(goal.y)) ** 2
        gtheta = _heading_diff(last.theta, goal.theta) ** 2

        sim_xy = np.asarray([(s.x, s.y) for s in states[:n_guess]], dtype=np.float64)
        dev = 0.0
        if len(sim_xy) == n_guess:
            dev = float(np.mean((sim_xy - guess_xy) ** 2))

        effort = float(np.mean(controls * controls)) if controls.size else 0.0
        smooth = 0.0
        if len(controls) >= 2:
            dc = controls[1:] - controls[:-1]
            smooth = float(np.mean(dc * dc))

        clearance_pen = 0.0
        if float(w_clearance) > 0.0:
            for s in states[1:]:
                d = float(query_distance(dist_field, grid_map, float(s.x), float(s.y)))
                deficit = float(clearance_target_m) - d
                if deficit > 0.0:
                    clearance_pen += deficit * deficit
            clearance_pen /= max(1, len(states) - 1)

        return float(
            float(w_goal_xy) * gxy
            + float(w_goal_theta) * gtheta
            + float(w_deviation) * dev
            + float(w_control) * effort
            + float(w_smooth) * smooth
            + float(w_clearance) * clearance_pen
        )

    return objective


def _repair_minimize(
    *,
    objective: Callable[[np.ndarray], float],
    x0: np.ndarray,
    bounds: list[tuple[float, float]],
    max_iter: int,
) -> Any:
    from scipy.optimize import minimize

    return minimize(
        objective,
        np.asarray(x0, dtype=np.float64),
        method="SLSQP",
        bounds=bounds,
        options={"maxiter": int(max_iter), "ftol": 1e-5, "disp": False},
    )


def _to_repair_controls(
    *,
    db_states: list[_State],
    db_controls: list[tuple[float, float]],
    start: _State,
    goal: _State,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    params: AckermannParams,
    dt_s: float,
    primitive_duration_s: float,
    v_min_m_s: float,
    delta_dot_max_rad_s: float,
    a_max_m_s2: float,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    to_max_iter: int,
    to_clearance_target_m: float,
    to_w_goal_xy: float,
    to_w_goal_theta: float,
    to_w_deviation: float,
    to_w_control: float,
    to_w_smooth: float,
    to_w_clearance: float,
    deadline_s: float,
) -> tuple[bool, list[_State], list[tuple[float, float]], str, str, float, float]:
    if not db_controls:
        return False, db_states, [], "skipped_no_controls", "none", 0.0, float("nan")

    control_guess_states = _continuous_guess_for_control_horizon(
        db_states,
        control_count=len(db_controls),
    )
    dist_field = compute_obstacle_distance_field(grid_map)
    raw_objective = _build_control_objective(
        start=start,
        goal=goal,
        guess_states=control_guess_states,
        params=params,
        dt_s=float(dt_s),
        v_min_m_s=float(v_min_m_s),
        dist_field=dist_field,
        grid_map=grid_map,
        clearance_target_m=float(to_clearance_target_m),
        w_goal_xy=float(to_w_goal_xy),
        w_goal_theta=float(to_w_goal_theta),
        w_deviation=float(to_w_deviation),
        w_control=float(to_w_control),
        w_smooth=float(to_w_smooth),
        w_clearance=float(to_w_clearance),
    )

    optimizer_deadline_s = min(float(deadline_s), time.perf_counter() + 8.0)

    def objective(z: np.ndarray) -> float:
        if time.perf_counter() >= float(optimizer_deadline_s):
            raise TimeoutError("idb_rrt_paper TO exceeded timeout budget")
        return raw_objective(z)

    tracked_ok, tracked_states, tracked_controls = _tracking_shooting_candidate(
        guess_states=control_guess_states,
        start=start,
        goal=goal,
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=collision_checker,
        params=params,
        dt_s=float(dt_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
    )
    if tracked_ok:
        obj_track = float(raw_objective(np.asarray(tracked_controls, dtype=np.float64).reshape(-1)))
        return True, tracked_states, tracked_controls, "success_tracking_shooting", "tracking_shooting", 0.0, obj_track
    if time.perf_counter() >= float(deadline_s):
        return False, db_states, [], "timeout_after_tracking_shooting", "none", 0.0, float("nan")

    guided_ok, guided_states, guided_controls = _guided_control_shooting_repair(
        guide_states=control_guess_states,
        start=start,
        goal=goal,
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=collision_checker,
        params=params,
        dt_s=float(dt_s),
        primitive_duration_s=float(primitive_duration_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
        theta_weight_m=0.35,
        speed_weight_m=0.05,
        steer_weight_m=0.0,
        deadline_s=min(float(deadline_s), time.perf_counter() + 12.0),
    )
    if guided_ok:
        obj_guided = float(raw_objective(np.asarray(guided_controls, dtype=np.float64).reshape(-1)))
        return True, guided_states, guided_controls, "success_guided_control_shooting", "guided_control_shooting", 0.0, obj_guided
    if time.perf_counter() >= float(deadline_s):
        return False, db_states, [], "timeout_after_guided_control_shooting", "none", 0.0, float("nan")

    initial_controls = _controls_from_state_guess(
        states=control_guess_states,
        start=start,
        params=params,
        dt_s=float(dt_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
    )
    if len(initial_controls) != len(db_controls):
        initial_controls = list(db_controls)
    initial_states = _simulate_controls(
        start=start,
        controls=initial_controls,
        params=params,
        dt_s=float(dt_s),
        v_min_m_s=float(v_min_m_s),
    )
    if _states_are_valid_solution(
        states=initial_states,
        goal=goal,
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=collision_checker,
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
    ):
        obj0 = float(raw_objective(np.asarray(initial_controls, dtype=np.float64).reshape(-1)))
        return True, initial_states, initial_controls, "success_initial_shooting", "initial_shooting", 0.0, obj0
    if time.perf_counter() >= float(deadline_s):
        return False, db_states, [], "timeout_after_initial_shooting", "none", 0.0, float("nan")

    x0 = np.asarray(initial_controls, dtype=np.float64).reshape(-1)
    bounds: list[tuple[float, float]] = []
    for _ in db_controls:
        bounds.append((-float(delta_dot_max_rad_s), float(delta_dot_max_rad_s)))
        bounds.append((-float(a_max_m_s2), float(a_max_m_s2)))

    t0 = time.perf_counter()
    try:
        opt_res = _repair_minimize(
            objective=objective,
            x0=x0,
            bounds=bounds,
            max_iter=int(to_max_iter),
        )
        opt_x = np.asarray(getattr(opt_res, "x", x0), dtype=np.float64)
        opt_fun = float(getattr(opt_res, "fun", float("nan")))
    except Exception:  # noqa: BLE001
        repair_time_s = float(time.perf_counter() - t0)
        return False, db_states, [], "optimizer_failed", "none", repair_time_s, float("nan")
    repair_time_s = float(time.perf_counter() - t0)

    controls = [(float(a), float(b)) for a, b in opt_x.reshape(-1, 2)]
    states = _simulate_controls(
        start=start,
        controls=controls,
        params=params,
        dt_s=float(dt_s),
        v_min_m_s=float(v_min_m_s),
    )
    final = states[-1]
    goal_error = math.hypot(float(final.x) - float(goal.x), float(final.y) - float(goal.y))
    if goal_error > float(goal_xy_tol_m):
        return False, states, [], "goal_tol_failed", "none", repair_time_s, opt_fun
    if _heading_diff(final.theta, goal.theta) > float(goal_theta_tol_rad):
        return False, states, [], "heading_tol_failed", "none", repair_time_s, opt_fun

    points_m = [(float(s.x), float(s.y)) for s in states]
    thetas = [float(s.theta) for s in states]
    if not _paper_path_collision_free(
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=None,
        points_m=points_m,
        thetas=thetas,
    ):
        return False, states, [], "collision_failed", "none", repair_time_s, opt_fun
    return True, states, controls, "success", "to_optimized", repair_time_s, opt_fun


def _stats(
    *,
    success: bool,
    termination: str,
    delta_initial_m: float,
    delta_final_m: float,
    primitive_library_size: int,
    primitive_count_final: int,
    outer_iterations: int,
    db_rrt_success: bool,
    to_attempted: bool,
    to_success: bool,
    to_status: str,
    to_time_s: float,
    to_objective: float,
    db_result: _DbRRTResult | None,
    states: list[_State],
    controls: list[tuple[float, float]],
    goal: _State,
    dt_s: float,
    v_min_m_s: float,
    delta_dot_max_rad_s: float,
    a_max_m_s2: float,
    control_source: str,
    model_note: str,
) -> dict[str, Any]:
    final_goal_error = (
        math.hypot(float(states[-1].x) - float(goal.x), float(states[-1].y) - float(goal.y))
        if states
        else float("nan")
    )
    return {
        "variant": "idb_rrt_paper",
        "success": bool(success),
        "termination": str(termination),
        "delta_initial_m": float(delta_initial_m),
        "delta_final_m": float(delta_final_m),
        "primitive_library_size": int(primitive_library_size),
        "primitive_count_final": int(primitive_count_final),
        "outer_iterations": int(outer_iterations),
        "db_rrt_success": bool(db_rrt_success),
        "to_attempted": bool(to_attempted),
        "to_success": bool(to_success),
        "to_status": str(to_status),
        "to_time_s": float(to_time_s),
        "to_objective": float(to_objective),
        "bidirectional": False,
        "model_note": str(model_note),
        "dt_s": float(dt_s),
        "v_min_m_s": float(v_min_m_s),
        "delta_dot_max_rad_s": float(delta_dot_max_rad_s),
        "a_max_m_s2": float(a_max_m_s2),
        "control_source": str(control_source),
        "control_semantics": "(delta_dot_rad_s, a_m_s2)",
        "db_rrt_iterations": int(db_result.iterations if db_result else 0),
        "db_rrt_nodes": int(db_result.nodes if db_result else 0),
        "db_rrt_best_goal_error_m": float(db_result.best_goal_error_m if db_result else final_goal_error),
        "goal_error_m": float(final_goal_error),
        "path_states": [
            (float(s.x), float(s.y), float(s.theta), float(s.v), float(s.delta)) for s in states
        ],
        "path_controls": [
            (float(delta_dot), float(accel)) for delta_dot, accel in controls
        ] if len(controls) + 1 == len(states) else [],
        "skipped_collision": int(db_result.skipped_collision if db_result else 0),
        "skipped_no_primitive": int(db_result.skipped_no_primitive if db_result else 0),
        "skipped_near_existing": int(db_result.skipped_near_existing if db_result else 0),
    }


def plan_idb_rrt_paper(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    seed: int = 0,
    goal_theta_rad: float = 0.0,
    start_theta_rad: float | None = None,
    goal_xy_tol_m: float = 0.5,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 60.0,
    max_iter: int = 12_000,
    collision_padding: float | None = None,
    collision_checker=None,
    primitive_duration_s: float = 0.8,
    dt_s: float = 0.1,
    start_v_m_s: float = 0.8,
    target_v_m_s: float = 0.9,
    v_min_m_s: float = 0.05,
    delta_dot_max_rad_s: float = math.radians(60.0),
    a_max_m_s2: float = 1.0,
    goal_sample_rate: float = 0.14,
    guide_sample_rate: float = 0.55,
    guide_noise_m: float = 0.8,
    nearest_k: int = 5,
    theta_weight_m: float = 0.35,
    speed_weight_m: float = 0.15,
    steer_weight_m: float = 0.25,
    delta_initial_m: float = 0.75,
    delta_decay: float = 0.7,
    delta_min_m: float = 0.12,
    initial_primitive_count: int = 35,
    max_primitive_count: int = 220,
    primitive_growth: float = 1.6,
    max_outer_iterations: int = 4,
    db_rrt_iteration_chunk: int = 3_000,
    to_max_iter: int = 60,
    to_clearance_target_m: float = 0.35,
    to_w_goal_xy: float = 400.0,
    to_w_goal_theta: float = 10.0,
    to_w_deviation: float = 1.0,
    to_w_control: float = 0.005,
    to_w_smooth: float = 0.02,
    to_w_clearance: float = 30.0,
) -> PlannerResult:
    """Run paper-oriented iDb-RRT on an occupancy grid."""
    _ = collision_padding
    cell_size_m = float(grid_map.resolution)
    t0 = time.perf_counter()
    deadline_s = t0 + float(timeout_s)
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    )
    start = _State(
        x=float(start_xy[0]) * cell_size_m,
        y=float(start_xy[1]) * cell_size_m,
        theta=wrap_angle(start_theta),
        v=clamp(float(start_v_m_s), float(v_min_m_s), float(params.v_max)),
        delta=0.0,
    )
    goal = _State(
        x=float(goal_xy[0]) * cell_size_m,
        y=float(goal_xy[1]) * cell_size_m,
        theta=wrap_angle(float(goal_theta_rad)),
        v=clamp(float(target_v_m_s), float(v_min_m_s), float(params.v_max)),
        delta=0.0,
    )
    paper_collision_checker = _ShiftedBoxGridChecker(grid_map=grid_map, footprint=footprint)

    if _paper_collides_pose(
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=None,
        x=start.x,
        y=start.y,
        theta=start.theta,
    ):
        elapsed = float(time.perf_counter() - t0)
        stats = _stats(
            success=False,
            termination="start_in_collision",
            delta_initial_m=float(delta_initial_m),
            delta_final_m=float(delta_initial_m),
            primitive_library_size=0,
            primitive_count_final=0,
            outer_iterations=0,
            db_rrt_success=False,
            to_attempted=False,
            to_success=False,
            to_status="skipped_start_in_collision",
            to_time_s=0.0,
            to_objective=float("nan"),
            db_result=None,
            states=[start],
            controls=[],
            goal=goal,
            dt_s=float(dt_s),
            v_min_m_s=float(v_min_m_s),
            delta_dot_max_rad_s=float(delta_dot_max_rad_s),
            a_max_m_s2=float(a_max_m_s2),
            control_source="none",
            model_note="local Ackermann dynamics; no Dynoplan/Dynobench dependency",
        )
        return PlannerResult(path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))], time_s=elapsed, success=False, stats=stats)

    primitive_library = _generate_motion_primitive_library(
        params=params,
        target_v_m_s=float(target_v_m_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
        primitive_duration_s=float(primitive_duration_s),
        dt_s=float(dt_s),
    )
    rng = np.random.default_rng(int(seed))
    delta_m = float(delta_initial_m)
    primitive_count = min(max(1, int(initial_primitive_count)), len(primitive_library), int(max_primitive_count))
    best_states: list[_State] = [start]
    best_controls: list[tuple[float, float]] = []
    best_control_source = "none"
    best_db: _DbRRTResult | None = None
    db_success = False
    to_attempted = False
    to_success = False
    to_status = "not_attempted"
    to_time_s = 0.0
    to_objective = float("nan")
    outer_done = 0
    iteration_total = 0

    for outer in range(1, int(max_outer_iterations) + 1):
        if time.perf_counter() >= deadline_s:
            break
        outer_done = int(outer)
        remaining_iter = max(1, int(max_iter) - int(iteration_total))
        iter_budget = min(int(db_rrt_iteration_chunk), remaining_iter)
        active_primitives = primitive_library[:primitive_count]
        db_result = _db_rrt_search(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=paper_collision_checker,
            params=params,
            start=start,
            goal=goal,
            start_xy=start_xy,
            goal_xy=goal_xy,
            rng=rng,
            primitives=active_primitives,
            delta_m=float(delta_m),
            goal_xy_tol_m=float(goal_xy_tol_m),
            goal_theta_tol_rad=float(goal_theta_tol_rad),
            iteration_budget=int(iter_budget),
            deadline_s=float(deadline_s),
            goal_sample_rate=float(goal_sample_rate),
            guide_sample_rate=float(guide_sample_rate),
            guide_noise_m=float(guide_noise_m),
            nearest_k=int(nearest_k),
            dt_s=float(dt_s),
            v_min_m_s=float(v_min_m_s),
            theta_weight_m=float(theta_weight_m),
            speed_weight_m=float(speed_weight_m),
            steer_weight_m=float(steer_weight_m),
        )
        iteration_total += int(db_result.iterations)
        best_db = db_result
        best_states = db_result.states if db_result.states else [start]
        if not db_result.success:
            delta_m = max(float(delta_min_m), float(delta_m) * float(delta_decay))
            primitive_count = min(
                len(primitive_library),
                int(max_primitive_count),
                max(primitive_count + 1, int(math.ceil(float(primitive_count) * float(primitive_growth)))),
            )
            if iteration_total >= int(max_iter):
                break
            continue

        db_success = True
        to_attempted = True
        ok, repaired_states, repaired_controls, status, control_source, repair_time_s, objective_value = _to_repair_controls(
            db_states=db_result.states,
            db_controls=db_result.controls,
            start=start,
            goal=goal,
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=paper_collision_checker,
            params=params,
            dt_s=float(dt_s),
            primitive_duration_s=float(primitive_duration_s),
            v_min_m_s=float(v_min_m_s),
            delta_dot_max_rad_s=float(delta_dot_max_rad_s),
            a_max_m_s2=float(a_max_m_s2),
            goal_xy_tol_m=float(goal_xy_tol_m),
            goal_theta_tol_rad=float(goal_theta_tol_rad),
            to_max_iter=int(to_max_iter),
            to_clearance_target_m=float(to_clearance_target_m),
            to_w_goal_xy=float(to_w_goal_xy),
            to_w_goal_theta=float(to_w_goal_theta),
            to_w_deviation=float(to_w_deviation),
            to_w_control=float(to_w_control),
            to_w_smooth=float(to_w_smooth),
            to_w_clearance=float(to_w_clearance),
            deadline_s=float(deadline_s),
        )
        to_time_s += float(repair_time_s)
        to_status = str(status)
        to_objective = float(objective_value)
        if ok:
            to_success = True
            best_states = repaired_states
            best_controls = repaired_controls
            best_control_source = str(control_source)
            break
        # Rejected TO candidates may violate collision or goal constraints.
        # Keep only the Db-RRT seed when the repair stage fails.
        best_states = db_result.states
        best_controls = []
        best_control_source = "none"
        delta_m = max(float(delta_min_m), float(delta_m) * float(delta_decay))
        if time.perf_counter() >= deadline_s or iteration_total >= int(max_iter):
            break

    success = bool(to_success)
    termination = "success" if success else ("db_rrt_failed" if not db_success else f"to_{to_status}")
    path_cells = (
        [(float(s.x) / cell_size_m, float(s.y) / cell_size_m) for s in best_states]
        if success
        else []
    )
    elapsed = float(time.perf_counter() - t0)
    stats = _stats(
        success=success,
        termination=termination,
        delta_initial_m=float(delta_initial_m),
        delta_final_m=float(delta_m),
        primitive_library_size=len(primitive_library),
        primitive_count_final=int(primitive_count),
        outer_iterations=int(outer_done),
        db_rrt_success=bool(db_success),
        to_attempted=bool(to_attempted),
        to_success=bool(to_success),
        to_status=str(to_status),
        to_time_s=float(to_time_s),
        to_objective=float(to_objective),
        db_result=best_db,
        states=best_states,
        controls=best_controls,
        goal=goal,
        dt_s=float(dt_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
        control_source=str(best_control_source if success else "none"),
        model_note="local Ackermann dynamics; no Dynoplan/Dynobench dependency",
    )
    return PlannerResult(
        path_xy_cells=path_cells,
        time_s=elapsed,
        success=success,
        stats=stats,
    )
