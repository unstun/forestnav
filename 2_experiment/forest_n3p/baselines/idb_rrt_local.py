"""Local iDb-RRT-style kinodynamic RRT baseline.

参考
----
Ortiz-Haro et al., "iDb-RRT: Sampling-based Kinodynamic Motion Planning
with Motion Primitives and Trajectory Optimization", arXiv:2403.10745, 2024.

说明
----
本文件提供两个 baseline：

- ``plan_idb_rrt_local``：保留 motion primitive + RRT 扩展思想，**不**含
  论文 Section IV 的 trajectory optimization repair。命名为 ``idb_rrt_local``。

- ``plan_idb_rrt_to``：在 ``plan_idb_rrt_local`` 输出之上，叠加一个**轻量**
  trajectory optimization repair（SLSQP 中间点优化）。命名为 ``idb_rrt_to``。
  ⚠️ 这是 *iDb-RRT local repair variant*，不是论文完整版本（不含 Dynoplan /
  OMPL / FCL / IPOPT 等论文级依赖）。详见
  ``.pipeline/contracts/baseline_realmap_a_v4_idb_rrt_to.md``。
"""
from __future__ import annotations

import heapq
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
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.common import clamp, wrap_angle


@dataclass(frozen=True)
class _State:
    x: float
    y: float
    theta: float
    v: float
    delta: float


@dataclass(frozen=True)
class _Node:
    state: _State
    parent: int
    segment: tuple[_State, ...]
    cost: float


def _heading_diff(a: float, b: float) -> float:
    return abs(wrap_angle(float(a) - float(b)))


def _collides_pose(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    x: float,
    y: float,
    theta: float,
) -> bool:
    if collision_checker is not None:
        return bool(collision_checker.collides_pose(float(x), float(y), float(theta)))
    return bool(footprint.collides(grid_map, float(x), float(y), float(theta)))


def _rollout(
    *,
    state: _State,
    delta_dot: float,
    accel: float,
    params: AckermannParams,
    duration_s: float,
    dt_s: float,
    v_min_m_s: float,
    v_max_m_s: float,
) -> tuple[_State, ...]:
    steps = max(1, int(math.ceil(float(duration_s) / max(float(dt_s), 1e-6))))
    dt = float(duration_s) / float(steps)
    x, y, theta = float(state.x), float(state.y), float(state.theta)
    v, delta = float(state.v), float(state.delta)
    out: list[_State] = []

    for _ in range(steps):
        delta = clamp(delta + float(delta_dot) * dt, -params.max_steer, params.max_steer)
        v = clamp(v + float(accel) * dt, float(v_min_m_s), float(v_max_m_s))
        x += v * dt * math.cos(theta)
        y += v * dt * math.sin(theta)
        theta = wrap_angle(theta + (v * dt / params.wheelbase) * math.tan(delta))
        out.append(_State(x=x, y=y, theta=theta, v=v, delta=delta))

    return tuple(out)


def _segment_is_collision_free(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    segment: tuple[_State, ...],
) -> bool:
    for s in segment:
        if _collides_pose(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            x=s.x,
            y=s.y,
            theta=s.theta,
        ):
            return False
    return True


def _astar_grid_guide(
    *,
    grid_map: GridMap,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    max_expansions: int = 80_000,
) -> list[tuple[float, float]]:
    """Return a coarse 2D guide in world coordinates for sampling bias."""
    sx, sy = int(start_xy[0]), int(start_xy[1])
    gx, gy = int(goal_xy[0]), int(goal_xy[1])
    if grid_map.is_occupied_index(sx, sy) or grid_map.is_occupied_index(gx, gy):
        return []

    neigh = [
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
        (-1, -1, math.sqrt(2.0)), (-1, 1, math.sqrt(2.0)),
        (1, -1, math.sqrt(2.0)), (1, 1, math.sqrt(2.0)),
    ]
    start = (sx, sy)
    goal = (gx, gy)
    open_heap: list[tuple[float, float, tuple[int, int]]] = []
    heapq.heappush(open_heap, (math.hypot(gx - sx, gy - sy), 0.0, start))
    came: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: dict[tuple[int, int], float] = {start: 0.0}
    closed: set[tuple[int, int]] = set()

    expansions = 0
    while open_heap and expansions < int(max_expansions):
        _f, g_now, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        if cur == goal:
            break
        closed.add(cur)
        expansions += 1
        cx, cy = cur
        for dx, dy, step_cost in neigh:
            nx, ny = cx + dx, cy + dy
            nxt = (nx, ny)
            if nxt in closed or grid_map.is_occupied_index(nx, ny):
                continue
            new_g = g_now + step_cost
            if new_g >= g_score.get(nxt, float("inf")):
                continue
            came[nxt] = cur
            g_score[nxt] = new_g
            h = math.hypot(gx - nx, gy - ny)
            heapq.heappush(open_heap, (new_g + h, new_g, nxt))

    if goal not in came and goal != start:
        return []

    cells = [goal]
    while cells[-1] != start:
        cells.append(came[cells[-1]])
    cells.reverse()
    return [grid_map.grid_to_world(x, y) for x, y in cells]


def _sample_state(
    *,
    rng: np.random.Generator,
    grid_map: GridMap,
    guide: list[tuple[float, float]],
    goal: _State,
    goal_sample_rate: float,
    guide_sample_rate: float,
    guide_noise_m: float,
) -> _State:
    r = float(rng.random())
    if r < float(goal_sample_rate):
        return goal

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
        return _State(x=float(x), y=float(y), theta=wrap_angle(theta), v=goal.v, delta=0.0)

    x, y, theta = grid_map.random_free_state(rng)
    return _State(x=float(x), y=float(y), theta=float(theta), v=goal.v, delta=0.0)


def _nearest_indices(
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


def _primitive_score(*, end: _State, sample: _State, theta_weight_m: float, speed_weight_m: float) -> float:
    dxy = math.hypot(float(end.x) - float(sample.x), float(end.y) - float(sample.y))
    dtheta = _heading_diff(end.theta, sample.theta)
    dv = abs(float(end.v) - float(sample.v))
    return float(dxy + float(theta_weight_m) * dtheta + float(speed_weight_m) * dv)


def _select_primitive(
    *,
    candidate_indices: np.ndarray,
    nodes: list[_Node],
    sample: _State,
    action_table: np.ndarray,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    params: AckermannParams,
    primitive_duration_s: float,
    dt_s: float,
    v_min_m_s: float,
    v_max_m_s: float,
    theta_weight_m: float,
    speed_weight_m: float,
) -> tuple[int, tuple[_State, ...], float] | None:
    best: tuple[int, tuple[_State, ...], float] | None = None
    best_score = float("inf")
    for idx in candidate_indices:
        node = nodes[int(idx)]
        for delta_dot, accel in action_table:
            segment = _rollout(
                state=node.state,
                delta_dot=float(delta_dot),
                accel=float(accel),
                params=params,
                duration_s=float(primitive_duration_s),
                dt_s=float(dt_s),
                v_min_m_s=float(v_min_m_s),
                v_max_m_s=float(v_max_m_s),
            )
            if not segment:
                continue
            end = segment[-1]
            if math.hypot(end.x - node.state.x, end.y - node.state.y) < 1e-6:
                continue
            if not _segment_is_collision_free(
                grid_map=grid_map,
                footprint=footprint,
                collision_checker=collision_checker,
                segment=segment,
            ):
                continue
            score = _primitive_score(
                end=end,
                sample=sample,
                theta_weight_m=float(theta_weight_m),
                speed_weight_m=float(speed_weight_m),
            )
            if score < best_score:
                best_score = score
                best = (int(idx), segment, float(score))
    return best


def _reconstruct_path(nodes: list[_Node], goal_idx: int) -> list[_State]:
    chain: list[int] = []
    idx = int(goal_idx)
    while idx >= 0:
        chain.append(idx)
        idx = int(nodes[idx].parent)
    chain.reverse()

    path = [nodes[chain[0]].state]
    for node_idx in chain[1:]:
        path.extend(nodes[node_idx].segment)
    return path


def plan_idb_rrt_local(
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
    goal_sample_rate: float = 0.12,
    guide_sample_rate: float = 0.50,
    guide_noise_m: float = 0.8,
    nearest_k: int = 5,
    theta_weight_m: float = 0.35,
    speed_weight_m: float = 0.05,
) -> PlannerResult:
    """Run the local iDb-RRT-style baseline on an occupancy grid."""
    _ = collision_padding
    cell_size_m = float(grid_map.resolution)
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

    t0 = time.perf_counter()
    if _collides_pose(
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=collision_checker,
        x=start.x,
        y=start.y,
        theta=start.theta,
    ):
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=float(time.perf_counter() - t0),
            success=False,
            stats={"variant": "idb_rrt_local", "termination": "start_in_collision"},
        )

    rng = np.random.default_rng(int(seed))
    guide = _astar_grid_guide(grid_map=grid_map, start_xy=start_xy, goal_xy=goal_xy)
    action_table = build_ackermann_action_table_35(
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
    )

    capacity = max(2, int(max_iter) + 1)
    xs = np.empty(capacity, dtype=np.float64)
    ys = np.empty(capacity, dtype=np.float64)
    thetas = np.empty(capacity, dtype=np.float64)
    nodes: list[_Node] = [_Node(state=start, parent=-1, segment=tuple(), cost=0.0)]
    xs[0], ys[0], thetas[0] = start.x, start.y, start.theta
    best_goal_idx = 0
    best_goal_error = math.hypot(start.x - goal.x, start.y - goal.y)
    goal_idx: int | None = None
    skipped_collision = 0
    skipped_no_primitive = 0

    for it in range(1, int(max_iter) + 1):
        if time.perf_counter() - t0 >= float(timeout_s):
            break
        if len(nodes) >= capacity:
            break

        sample = _sample_state(
            rng=rng,
            grid_map=grid_map,
            guide=guide,
            goal=goal,
            goal_sample_rate=float(goal_sample_rate),
            guide_sample_rate=float(guide_sample_rate),
            guide_noise_m=float(guide_noise_m),
        )
        candidates = _nearest_indices(
            sample=sample,
            xs=xs,
            ys=ys,
            thetas=thetas,
            n_nodes=len(nodes),
            k=int(nearest_k),
            theta_weight_m=float(theta_weight_m),
        )
        choice = _select_primitive(
            candidate_indices=candidates,
            nodes=nodes,
            sample=sample,
            action_table=action_table,
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            params=params,
            primitive_duration_s=float(primitive_duration_s),
            dt_s=float(dt_s),
            v_min_m_s=float(v_min_m_s),
            v_max_m_s=float(params.v_max),
            theta_weight_m=float(theta_weight_m),
            speed_weight_m=float(speed_weight_m),
        )
        if choice is None:
            skipped_no_primitive += 1
            continue
        parent_idx, segment, _score = choice
        end = segment[-1]
        if _collides_pose(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            x=end.x,
            y=end.y,
            theta=end.theta,
        ):
            skipped_collision += 1
            continue

        parent = nodes[parent_idx]
        edge_cost = 0.0
        prev = parent.state
        for s in segment:
            edge_cost += math.hypot(s.x - prev.x, s.y - prev.y)
            prev = s
        nodes.append(_Node(state=end, parent=parent_idx, segment=segment, cost=parent.cost + edge_cost))
        new_idx = len(nodes) - 1
        xs[new_idx], ys[new_idx], thetas[new_idx] = end.x, end.y, end.theta

        goal_error = math.hypot(end.x - goal.x, end.y - goal.y)
        if goal_error < best_goal_error:
            best_goal_error = goal_error
            best_goal_idx = new_idx
        if goal_error <= float(goal_xy_tol_m) and _heading_diff(end.theta, goal.theta) <= float(goal_theta_tol_rad):
            goal_idx = new_idx
            break

    success = goal_idx is not None
    final_idx = int(goal_idx if goal_idx is not None else best_goal_idx)
    states = _reconstruct_path(nodes, final_idx)
    path_cells = [(float(s.x) / cell_size_m, float(s.y) / cell_size_m) for s in states]
    elapsed = float(time.perf_counter() - t0)

    stats: dict[str, Any] = {
        "variant": "idb_rrt_local",
        "success": bool(success),
        "termination": "goal_reached" if success else "timeout_or_budget",
        "iterations": int(it if "it" in locals() else 0),
        "nodes": int(len(nodes)),
        "guide_waypoints": int(len(guide)),
        "best_goal_error_m": float(best_goal_error),
        "goal_xy_tol_m": float(goal_xy_tol_m),
        "primitive_duration_s": float(primitive_duration_s),
        "dt_s": float(dt_s),
        "skipped_collision": int(skipped_collision),
        "skipped_no_primitive": int(skipped_no_primitive),
        "path_states": [(float(s.x), float(s.y), float(s.theta)) for s in states],
    }
    return PlannerResult(
        path_xy_cells=path_cells,
        time_s=elapsed,
        success=bool(success),
        stats=stats,
    )


# ============================================================================
# Trajectory Optimization (TO) repair —— `plan_idb_rrt_to`
#
# 在 ``plan_idb_rrt_local`` 输出基础上叠加一个 SLSQP 中间点优化 repair：
# 优化变量为原始路径中间点 + 末点的 (x, y) 坐标，首点固定为 start。目标函数 = 与
# 原路径偏离 + 二阶差分平滑 + 终点误差 + 可选 clearance penalty。
# 任一安全条件不满足则 fallback 到原始路径并在 stats 中记录原因。
# 详见 .pipeline/contracts/baseline_realmap_a_v4_idb_rrt_to.md
# ============================================================================


def _repair_minimize(
    *,
    objective: Callable[[np.ndarray], float],
    x0: np.ndarray,
    max_iter: int,
) -> Any:
    """SLSQP 默认 repair 优化器；测试可 monkeypatch 模块级符号注入劣化解。"""
    # 延迟 import：让 `plan_idb_rrt_local` 在 scipy 缺席时仍可用
    from scipy.optimize import minimize

    return minimize(
        objective,
        np.asarray(x0, dtype=np.float64),
        method="SLSQP",
        options={"maxiter": int(max_iter), "ftol": 1e-6, "disp": False},
    )


def _estimate_thetas_from_xy(
    *,
    points_m: list[tuple[float, float]],
    start_theta: float,
) -> list[float]:
    """根据相邻点中心差分估计 theta；首点用 start_theta，末点用倒数前向差分。"""
    n = len(points_m)
    if n == 0:
        return []
    if n == 1:
        return [float(start_theta)]
    out: list[float] = [float(start_theta)]
    for i in range(1, n - 1):
        nx, ny = points_m[i + 1]
        px, py = points_m[i - 1]
        out.append(float(math.atan2(ny - py, nx - px)))
    last_x, last_y = points_m[-1]
    prev_x, prev_y = points_m[-2]
    out.append(float(math.atan2(last_y - prev_y, last_x - prev_x)))
    return [wrap_angle(t) for t in out]


def _path_collision_free(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    collision_checker,
    points_m: list[tuple[float, float]],
    thetas: list[float],
    interp_step_m: float | None = None,
) -> bool:
    """逐点 + 线段插值碰撞检查。

    端点：用各自 theta 检查；
    线段内部：步长 ≤ ``interp_step_m``（默认 = ``grid_map.resolution * 0.5``），
    内部点的 theta 用相邻端点角度的最短路 wrap_angle 线性插值。这样能识别
    "端点安全但线段穿墙" 的反例。
    """
    if not points_m:
        return True
    step = (
        float(interp_step_m)
        if interp_step_m is not None
        else 0.5 * float(grid_map.resolution)
    )
    if not (step > 0.0):
        step = 0.5 * float(grid_map.resolution)

    # ------------------------------ 端点 ------------------------------- #
    for (x, y), theta in zip(points_m, thetas):
        if _collides_pose(
            grid_map=grid_map,
            footprint=footprint,
            collision_checker=collision_checker,
            x=float(x),
            y=float(y),
            theta=float(theta),
        ):
            return False

    # ------------------------------ 线段内部 --------------------------- #
    for i in range(len(points_m) - 1):
        x0, y0 = points_m[i]
        x1, y1 = points_m[i + 1]
        t0, t1 = float(thetas[i]), float(thetas[i + 1])
        dx, dy = float(x1) - float(x0), float(y1) - float(y0)
        seg_len = math.hypot(dx, dy)
        if seg_len <= step:
            continue
        n_sub = int(math.ceil(seg_len / step))
        # 端点（k=0, k=n_sub）已在外层检查，仅扫内部 k=1..n_sub-1
        # theta 走最短弧线性插值：t1 - t0 先 wrap_angle 再 lerp
        d_theta = wrap_angle(t1 - t0)
        for k in range(1, n_sub):
            tt = float(k) / float(n_sub)
            x = float(x0) + tt * dx
            y = float(y0) + tt * dy
            theta = wrap_angle(t0 + tt * d_theta)
            if _collides_pose(
                grid_map=grid_map,
                footprint=footprint,
                collision_checker=collision_checker,
                x=x,
                y=y,
                theta=theta,
            ):
                return False
    return True


def _states_to_xytheta(stats: dict[str, Any], expected_len: int) -> list[tuple[float, float, float]] | None:
    """从 PlannerResult.stats 提取内部真实轨迹姿态；长度不匹配则放弃。"""
    raw = stats.get("path_states")
    if not isinstance(raw, list) or len(raw) != int(expected_len):
        return None
    out: list[tuple[float, float, float]] = []
    try:
        for item in raw:
            x, y, theta = item[:3]
            out.append((float(x), float(y), wrap_angle(float(theta))))
    except (TypeError, ValueError):
        return None
    return out


def _repair_thetas(
    *,
    new_points_m: list[tuple[float, float]],
    base_xytheta: list[tuple[float, float, float]] | None,
    start_theta: float,
) -> list[float]:
    """为 repair 候选轨迹构造碰撞检查 heading。

    如果 RRT 阶段提供了 motion primitive 积分得到的真实 theta，则优先沿用。TO 第一版
    只优化 (x, y)，没有重新优化 delta / theta；沿用原始 theta 比从折线差分重估更贴近
    本地 Ackermann rollout，也能避免窄通道处因差分 heading 抖动造成误判。
    """
    if base_xytheta is not None and len(base_xytheta) == len(new_points_m):
        return [float(theta) for _, _, theta in base_xytheta]
    return _estimate_thetas_from_xy(points_m=new_points_m, start_theta=start_theta)


def _lock_first_segment_heading(
    *,
    points_m: list[tuple[float, float]],
    start_theta: float,
) -> list[tuple[float, float]]:
    """把第一段投影到起点航向线上，同时保留第一段长度自由度。"""
    if len(points_m) < 2:
        return list(points_m)
    p0 = points_m[0]
    p1 = points_m[1]
    dx = float(p1[0]) - float(p0[0])
    dy = float(p1[1]) - float(p0[1])
    c = math.cos(float(start_theta))
    s = math.sin(float(start_theta))
    along = dx * c + dy * s
    if along <= 1e-6:
        along = math.hypot(dx, dy)
    if along <= 1e-6:
        return list(points_m)
    out = list(points_m)
    out[1] = (float(p0[0]) + along * c, float(p0[1]) + along * s)
    return out


def _build_repair_objective(
    *,
    pre_path_m: list[tuple[float, float]],
    goal_xy_m: tuple[float, float],
    w_dev: float,
    w_smooth: float,
    w_goal: float,
    w_clearance: float,
    clearance_target_m: float,
    clearance_query: Callable[[float, float], float] | None,
    fixed_prefix_count: int = 1,
) -> Callable[[np.ndarray], float]:
    """构造 SLSQP objective J(z)。

    前 ``fixed_prefix_count`` 个点固定，变量为后续点的 ``(x, y)``。默认只固定
    start；``idb_rrt_to`` 会固定 start 和第一个 rollout 点，从而保留起点航向。
    """
    n = len(pre_path_m)
    pre_xy = np.asarray(pre_path_m, dtype=np.float64)
    prefix_count = min(max(1, int(fixed_prefix_count)), max(1, n - 1))
    fixed_prefix = pre_xy[:prefix_count].copy()
    pre_var = pre_xy[prefix_count:].reshape(-1)
    gx, gy = float(goal_xy_m[0]), float(goal_xy_m[1])

    def objective(z: np.ndarray) -> float:
        var = np.asarray(z, dtype=np.float64).reshape(-1, 2)
        full = np.empty((n, 2), dtype=np.float64)
        full[:prefix_count] = fixed_prefix
        full[prefix_count:] = var

        # ------------------------------ deviation term --------------------- #
        dev = float(np.sum((var.reshape(-1) - pre_var) ** 2))

        # ------------------------------ smoothness term -------------------- #
        if n >= 3:
            d2 = full[2:] - 2.0 * full[1:-1] + full[:-2]
            smooth = float(np.sum(d2 * d2))
        else:
            smooth = 0.0

        # ------------------------------ goal-error term -------------------- #
        last = full[-1]
        gerr = float((last[0] - gx) ** 2 + (last[1] - gy) ** 2)

        # ------------------------------ clearance penalty ------------------ #
        clear_pen = 0.0
        if w_clearance > 0.0 and clearance_query is not None:
            for i in range(1, n):
                d = float(clearance_query(float(full[i, 0]), float(full[i, 1])))
                deficit = float(clearance_target_m) - d
                if deficit > 0.0:
                    clear_pen += deficit * deficit

        return (
            float(w_dev) * dev
            + float(w_smooth) * smooth
            + float(w_goal) * gerr
            + float(w_clearance) * clear_pen
        )

    return objective


def plan_idb_rrt_to(
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
    goal_sample_rate: float = 0.12,
    guide_sample_rate: float = 0.50,
    guide_noise_m: float = 0.8,
    nearest_k: int = 5,
    theta_weight_m: float = 0.35,
    speed_weight_m: float = 0.05,
    # ---- repair-only (v4) ---------------------------------------------------
    repair_max_iter: int = 100,
    repair_w_dev: float = 0.01,
    repair_w_smooth: float = 0.05,
    repair_w_goal: float = 0.5,
    repair_w_clearance: float = 10_000.0,
    repair_clearance_target_m: float = 1.5,
) -> PlannerResult:
    """iDb-RRT *local repair variant*：``idb_rrt_local`` 输出 + SLSQP TO repair。

    ⚠️ 命名约束：本函数实现的不是论文完整版 iDb-RRT。论文 baseline section 描述时
    必须标注为 *iDb-RRT local repair variant*。详见 v4 contract。
    """
    cell_size_m = float(grid_map.resolution)
    base = plan_idb_rrt_local(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        start_xy=start_xy,
        goal_xy=goal_xy,
        seed=int(seed),
        goal_theta_rad=float(goal_theta_rad),
        start_theta_rad=start_theta_rad,
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
        timeout_s=float(timeout_s),
        max_iter=int(max_iter),
        collision_padding=collision_padding,
        collision_checker=collision_checker,
        primitive_duration_s=float(primitive_duration_s),
        dt_s=float(dt_s),
        start_v_m_s=float(start_v_m_s),
        target_v_m_s=float(target_v_m_s),
        v_min_m_s=float(v_min_m_s),
        delta_dot_max_rad_s=float(delta_dot_max_rad_s),
        a_max_m_s2=float(a_max_m_s2),
        goal_sample_rate=float(goal_sample_rate),
        guide_sample_rate=float(guide_sample_rate),
        guide_noise_m=float(guide_noise_m),
        nearest_k=int(nearest_k),
        theta_weight_m=float(theta_weight_m),
        speed_weight_m=float(speed_weight_m),
    )

    base_stats: dict[str, Any] = dict(base.stats)
    public_base_stats = {k: v for k, v in base_stats.items() if k != "path_states"}
    goal_xy_m = (
        float(goal_xy[0]) * cell_size_m,
        float(goal_xy[1]) * cell_size_m,
    )
    base_path_m: list[tuple[float, float]] = [
        (float(x) * cell_size_m, float(y) * cell_size_m) for x, y in base.path_xy_cells
    ]
    base_xytheta = _states_to_xytheta(base_stats, expected_len=len(base_path_m))
    fixed_prefix_count = 1

    pre_goal_error_m = (
        math.hypot(base_path_m[-1][0] - goal_xy_m[0], base_path_m[-1][1] - goal_xy_m[1])
        if base_path_m
        else float("nan")
    )

    def _result_with_repair(
        *,
        path_cells: list[tuple[float, float]],
        success: bool,
        repair_attempted: bool,
        repair_success: bool,
        repair_status: str,
        repair_time_s: float,
        repair_objective: float,
        candidate_goal_error_m: float,
        extra_time_s: float = 0.0,
        path_thetas: list[float] | None = None,
    ) -> PlannerResult:
        # ------------------------------------------------------------------ #
        # post_repair_goal_error_m 必须反映**最终输出轨迹**的 goal error：    #
        #   - repair_success=True   → 用候选（候选已成为输出）                #
        #   - 其他（fallback / skip）→ 用 pre（输出 = 原始路径）              #
        # candidate_goal_error_m 反映**优化候选**的 goal error，用于诊断。    #
        # ------------------------------------------------------------------ #
        post_goal_error_m = (
            float(candidate_goal_error_m)
            if bool(repair_success)
            else float(pre_goal_error_m)
        )
        stats: dict[str, Any] = {
            **public_base_stats,
            "variant": "idb_rrt_to",
            "repair_attempted": bool(repair_attempted),
            "repair_success": bool(repair_success),
            "repair_status": str(repair_status),
            "repair_time_s": float(repair_time_s),
            "repair_objective": float(repair_objective),
            "pre_repair_goal_error_m": float(pre_goal_error_m),
            "post_repair_goal_error_m": float(post_goal_error_m),
            "candidate_goal_error_m": float(candidate_goal_error_m),
            "repair_fixed_prefix_count": int(fixed_prefix_count),
            "repair_start_heading_locked": bool(repair_success),
            "goal_xy_tol_m": float(goal_xy_tol_m),
        }
        if path_thetas is not None and len(path_thetas) == len(path_cells):
            stats["output_path_states"] = [
                (
                    float(x) * cell_size_m,
                    float(y) * cell_size_m,
                    wrap_angle(float(theta)),
                )
                for (x, y), theta in zip(path_cells, path_thetas)
            ]
        return PlannerResult(
            path_xy_cells=list(path_cells),
            time_s=float(base.time_s) + float(extra_time_s),
            success=bool(success),
            stats=stats,
        )

    # ------------------------------------------------------------------ #
    # Skip-cases：local 失败 / 路径过短，不进入 SLSQP                     #
    # ------------------------------------------------------------------ #
    if not base.success:
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=False,
            repair_attempted=False,
            repair_success=False,
            repair_status="skipped_local_failed",
            repair_time_s=0.0,
            repair_objective=float("nan"),
            candidate_goal_error_m=float("nan"),
        )

    n_path = len(base_path_m)
    if n_path < 3:
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=True,
            repair_attempted=False,
            repair_success=False,
            repair_status="skipped_path_too_short",
            repair_time_s=0.0,
            repair_objective=float("nan"),
            candidate_goal_error_m=float("nan"),
        )

    remaining_time_s = max(0.0, float(timeout_s) - float(base.time_s))
    if remaining_time_s <= 1e-3:
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=True,
            repair_attempted=False,
            repair_success=False,
            repair_status="skipped_timeout",
            repair_time_s=0.0,
            repair_objective=float("nan"),
            candidate_goal_error_m=float("nan"),
        )

    # ------------------------------------------------------------------ #
    # 构造 objective 与初始解                                            #
    # ------------------------------------------------------------------ #
    clearance_query: Callable[[float, float], float] | None = None
    if float(repair_w_clearance) > 0.0:
        from forest_n3p.third_party.pathplan.hybrid_a_star.obstacle_field import (
            compute_obstacle_distance_field,
            query_distance,
        )

        dist_field = compute_obstacle_distance_field(grid_map)

        def _q(x: float, y: float) -> float:
            return float(query_distance(dist_field, grid_map, float(x), float(y)))

        clearance_query = _q

    raw_objective = _build_repair_objective(
        pre_path_m=base_path_m,
        goal_xy_m=goal_xy_m,
        w_dev=float(repair_w_dev),
        w_smooth=float(repair_w_smooth),
        w_goal=float(repair_w_goal),
        w_clearance=float(repair_w_clearance),
        clearance_target_m=float(repair_clearance_target_m),
        clearance_query=clearance_query,
        fixed_prefix_count=int(fixed_prefix_count),
    )

    repair_deadline = time.perf_counter() + float(remaining_time_s)

    def objective(z: np.ndarray) -> float:
        if time.perf_counter() >= repair_deadline:
            raise TimeoutError("idb_rrt_to repair exceeded remaining timeout budget")
        return raw_objective(z)

    x0 = np.asarray(base_path_m[int(fixed_prefix_count):], dtype=np.float64).reshape(-1)

    # ------------------------------------------------------------------ #
    # SLSQP 优化（异常一律 fallback）                                     #
    # ------------------------------------------------------------------ #
    t_repair0 = time.perf_counter()
    try:
        opt_res = _repair_minimize(
            objective=objective,
            x0=x0,
            max_iter=int(repair_max_iter),
        )
        opt_ok = bool(getattr(opt_res, "success", False))
        opt_x = np.asarray(getattr(opt_res, "x", x0), dtype=np.float64)
        opt_fun = float(getattr(opt_res, "fun", float("nan")))
    except Exception:  # noqa: BLE001 — 优化器崩溃/超时也走 fallback
        opt_ok = False
        opt_x = x0
        opt_fun = float("nan")
    repair_time_s = float(time.perf_counter() - t_repair0)

    if not opt_ok:
        # 优化器失败或超时：candidate 视为无效（NaN），输出原路径
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=True,
            repair_attempted=True,
            repair_success=False,
            repair_status="fallback_optimizer_failed",
            repair_time_s=repair_time_s,
            repair_objective=opt_fun,
            candidate_goal_error_m=float("nan"),
            extra_time_s=repair_time_s,
        )

    # ------------------------------------------------------------------ #
    # 重建轨迹 + theta，按 R1..R4 验收                                    #
    # ------------------------------------------------------------------ #
    new_xy_var = opt_x.reshape(-1, 2).tolist()
    new_path_m: list[tuple[float, float]] = list(base_path_m[: int(fixed_prefix_count)]) + [
        (float(p[0]), float(p[1])) for p in new_xy_var
    ]
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell_size_m)
    )
    new_path_m = _lock_first_segment_heading(
        points_m=new_path_m,
        start_theta=start_theta,
    )

    candidate_goal_error_m = float(
        math.hypot(new_path_m[-1][0] - goal_xy_m[0], new_path_m[-1][1] - goal_xy_m[1])
    )

    if candidate_goal_error_m > float(goal_xy_tol_m):
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=True,
            repair_attempted=True,
            repair_success=False,
            repair_status="fallback_goal_tol",
            repair_time_s=repair_time_s,
            repair_objective=opt_fun,
            candidate_goal_error_m=candidate_goal_error_m,
            extra_time_s=repair_time_s,
        )

    if candidate_goal_error_m > float(pre_goal_error_m):
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=True,
            repair_attempted=True,
            repair_success=False,
            repair_status="fallback_goal_worse",
            repair_time_s=repair_time_s,
            repair_objective=opt_fun,
            candidate_goal_error_m=candidate_goal_error_m,
            extra_time_s=repair_time_s,
        )

    new_thetas = _repair_thetas(
        new_points_m=new_path_m,
        base_xytheta=base_xytheta,
        start_theta=start_theta,
    )

    if not _path_collision_free(
        grid_map=grid_map,
        footprint=footprint,
        collision_checker=collision_checker,
        points_m=new_path_m,
        thetas=new_thetas,
    ):
        return _result_with_repair(
            path_cells=list(base.path_xy_cells),
            success=True,
            repair_attempted=True,
            repair_success=False,
            repair_status="fallback_collision",
            repair_time_s=repair_time_s,
            repair_objective=opt_fun,
            candidate_goal_error_m=candidate_goal_error_m,
            extra_time_s=repair_time_s,
        )

    new_path_cells = [
        (float(x) / cell_size_m, float(y) / cell_size_m) for x, y in new_path_m
    ]
    return _result_with_repair(
        path_cells=new_path_cells,
        success=True,
        repair_attempted=True,
        repair_success=True,
        repair_status="success",
        repair_time_s=repair_time_s,
        repair_objective=opt_fun,
        candidate_goal_error_m=candidate_goal_error_m,
        extra_time_s=repair_time_s,
        path_thetas=new_thetas,
    )
