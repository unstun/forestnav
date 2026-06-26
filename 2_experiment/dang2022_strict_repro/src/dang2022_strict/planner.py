from __future__ import annotations

from dataclasses import dataclass, field
import heapq
import math
import time
from typing import Optional

import numpy as np

from .collision import GridCollisionChecker
from .config import AlgorithmParams, VehicleParams, paper_algorithm_params, paper_vehicle_params
from .grid import GridMap
from .reeds_shepp import reeds_shepp_shortest_path
from .robot import MotionPrimitive, Pose, default_primitives, heading_diff, sample_constant_steer_motion
from .voronoi import compute_voronoi_field, query_voronoi_field


@dataclass(frozen=True)
class AnalyticCandidate:
    curvature: float
    path: list[Pose]
    dense_path: list[Pose]
    actions: list[MotionPrimitive]
    voronoi_cost: float
    motion_cost: float
    total_cost: float
    path_length_m: float


@dataclass(frozen=True)
class PlanResult:
    success: bool
    path: list[Pose]
    stats: dict[str, object]
    analytic_path: list[Pose]
    dense_path: list[Pose] = field(default_factory=list)


@dataclass
class _Node:
    pose: Pose
    g: float
    h: float
    parent: Optional["_Node"]
    action: Optional[MotionPrimitive]


class DangHybridAStarPlanner:
    def __init__(
        self,
        grid_map: GridMap,
        vehicle: VehicleParams | None = None,
        params: AlgorithmParams | None = None,
    ):
        self.grid_map = grid_map
        self.vehicle = vehicle if vehicle is not None else paper_vehicle_params()
        self.params = params if params is not None else paper_algorithm_params()
        self.collision = GridCollisionChecker(grid_map, self.vehicle)
        self.primitives = default_primitives(self.vehicle, self.params.motion_primitive_m)
        self.voronoi_field = compute_voronoi_field(
            grid_map,
            alpha=self.params.voronoi_alpha,
            d_o_max=self.params.voronoi_d_o_max,
        )

    def _curvature_values(self) -> list[float]:
        max_k = float(self.vehicle.max_curvature)
        step = max(float(self.params.curvature_resolution), 1e-9)
        values: list[float] = []
        k = step
        while k < max_k - 1e-9:
            values.append(float(k))
            k += step
        values.append(float(max_k))
        return values

    def evaluate_analytic_candidates(self, start: Pose, goal: Pose) -> list[AnalyticCandidate]:
        candidates: list[AnalyticCandidate] = []
        for curvature in self._curvature_values():
            candidate = self._candidate_for_curvature(start, goal, curvature)
            if candidate is not None:
                candidates.append(candidate)
        candidates.sort(key=lambda c: c.total_cost)
        return candidates

    def _candidate_for_curvature(
        self,
        start: Pose,
        goal: Pose,
        curvature: float,
    ) -> AnalyticCandidate | None:
        if curvature <= 0.0:
            return None
        radius = 1.0 / float(curvature)
        rs = reeds_shepp_shortest_path(start.as_tuple(), goal.as_tuple(), radius)
        if rs is None:
            return None
        cur = start
        path: list[Pose] = [start]
        actions: list[MotionPrimitive] = []
        dense: list[Pose] = [start]
        for seg_type, seg_len in zip(rs.segment_types, rs.segment_lengths):
            if abs(float(seg_len)) <= 1e-9:
                continue
            direction = 1 if seg_len >= 0.0 else -1
            step_len = abs(float(seg_len))
            if seg_type == "S":
                steering = 0.0
            elif seg_type == "L":
                steering = math.atan(self.vehicle.wheelbase_m / max(radius, 1e-9))
            elif seg_type == "R":
                steering = -math.atan(self.vehicle.wheelbase_m / max(radius, 1e-9))
            else:
                raise ValueError(f"unknown Reeds-Shepp segment: {seg_type}")
            samples = sample_constant_steer_motion(
                cur,
                steering,
                direction,
                step_len,
                self.vehicle,
                sample_step_m=self.params.collision_step_m,
            )
            if self.collision.collides_path(samples):
                return None
            cur = samples[-1]
            path.append(cur)
            dense.extend(samples[1:])
            actions.append(MotionPrimitive(steering, direction, step_len))
        if not actions:
            return None
        path[-1] = goal
        dense[-1] = goal
        v = self._path_voronoi_cost(dense)
        m, path_length = self._motion_cost(actions)
        total = self.params.sigma1 * v + self.params.sigma2 * m
        return AnalyticCandidate(
            curvature=float(curvature),
            path=path,
            dense_path=dense,
            actions=actions,
            voronoi_cost=float(v),
            motion_cost=float(m),
            total_cost=float(total),
            path_length_m=float(path_length),
        )

    def _path_voronoi_cost(self, path: list[Pose]) -> float:
        if not path:
            return 0.0
        total = 0.0
        for pose in path:
            total += query_voronoi_field(self.voronoi_field, self.grid_map, pose.x, pose.y)
        return float(total / len(path))

    def _motion_cost(self, actions: list[MotionPrimitive]) -> tuple[float, float]:
        length = 0.0
        steering_sum = 0.0
        switches = 0
        prev_sign = 0
        for action in actions:
            length += abs(float(action.step_m))
            steering_sum += abs(float(action.steering))
            sign = 1 if action.steering > 1e-9 else (-1 if action.steering < -1e-9 else 0)
            if prev_sign and sign and sign != prev_sign:
                switches += 1
            if sign:
                prev_sign = sign
        cost = (
            float(self.params.movement_weight_length) * length
            + float(self.params.movement_weight_steering) * steering_sum
            + float(self.params.movement_weight_switch) * switches
        )
        return float(cost), float(length)

    def _goal_reached(self, pose: Pose, goal: Pose) -> bool:
        dist = math.hypot(goal.x - pose.x, goal.y - pose.y)
        dtheta = abs(heading_diff(goal.theta, pose.theta))
        return dist <= self.params.goal_xy_tolerance_m and dtheta <= self.params.goal_theta_tolerance_rad

    def _discretize(self, pose: Pose) -> tuple[int, int, int]:
        gx, gy = self.grid_map.world_to_grid(pose.x, pose.y)
        theta = pose.theta % (2.0 * math.pi)
        tid = int(math.floor(theta / (2.0 * math.pi) * int(self.params.theta_bins))) % int(self.params.theta_bins)
        return gx, gy, tid

    def _dijkstra_cost_to_go(self, goal: Pose) -> np.ndarray:
        occ = np.asarray(self.grid_map.data, dtype=bool)
        h, w = occ.shape
        gx, gy = self.grid_map.world_to_grid(goal.x, goal.y)
        dist = np.full((h, w), float("inf"), dtype=np.float64)
        if not self.grid_map.in_bounds(gx, gy) or occ[gy, gx]:
            return dist
        res = float(self.grid_map.resolution)
        dist[gy, gx] = 0.0
        heap: list[tuple[float, int, int]] = [(0.0, gx, gy)]
        neighbors = (
            (1, 0, res),
            (-1, 0, res),
            (0, 1, res),
            (0, -1, res),
            (1, 1, res * math.sqrt(2.0)),
            (1, -1, res * math.sqrt(2.0)),
            (-1, 1, res * math.sqrt(2.0)),
            (-1, -1, res * math.sqrt(2.0)),
        )
        while heap:
            cur, x, y = heapq.heappop(heap)
            if cur != dist[y, x]:
                continue
            for dx, dy, step in neighbors:
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h or occ[ny, nx]:
                    continue
                nd = cur + step
                if nd < dist[ny, nx]:
                    dist[ny, nx] = nd
                    heapq.heappush(heap, (nd, nx, ny))
        return dist

    def _heuristic(self, pose: Pose, goal: Pose, dist_map: np.ndarray) -> float:
        gx, gy = self.grid_map.world_to_grid(pose.x, pose.y)
        h1 = math.hypot(goal.x - pose.x, goal.y - pose.y)
        if self.grid_map.in_bounds(gx, gy) and math.isfinite(float(dist_map[gy, gx])):
            h1 = float(dist_map[gy, gx])
        h2 = 0.0
        if self.params.use_reeds_shepp_heuristic:
            rs = reeds_shepp_shortest_path(
                pose.as_tuple(),
                goal.as_tuple(),
                self.vehicle.min_turn_radius_m,
            )
            if rs is not None and math.isfinite(float(rs.total_length)):
                h2 = float(rs.total_length)
            else:
                h2 = math.hypot(goal.x - pose.x, goal.y - pose.y)
        return h1 + h2

    def _reconstruct(self, node: _Node) -> tuple[list[Pose], list[MotionPrimitive]]:
        path: list[Pose] = []
        actions: list[MotionPrimitive] = []
        cur: _Node | None = node
        while cur is not None:
            path.append(cur.pose)
            if cur.action is not None:
                actions.append(cur.action)
            cur = cur.parent
        path.reverse()
        actions.reverse()
        return path, actions

    def _dense_from_actions(self, path: list[Pose], actions: list[MotionPrimitive]) -> list[Pose]:
        if not path:
            return []
        if not actions:
            return list(path)
        dense: list[Pose] = [path[0]]
        cur = path[0]
        for action in actions:
            samples = sample_constant_steer_motion(
                cur,
                action.steering,
                action.direction,
                action.step_m,
                self.vehicle,
                sample_step_m=self.params.collision_step_m,
            )
            dense.extend(samples[1:])
            cur = samples[-1]
        if dense:
            dense[-1] = path[-1]
        return dense

    def _stats(
        self,
        *,
        path: list[Pose],
        actions: list[MotionPrimitive],
        expansions: int,
        elapsed_s: float,
        failure_reason: str | None,
        analytic: AnalyticCandidate | None,
    ) -> dict[str, object]:
        length = sum(abs(float(action.step_m)) for action in actions)
        if not actions:
            for a, b in zip(path, path[1:]):
                length += math.hypot(b.x - a.x, b.y - a.y)
        turns = 0
        prev_sign = 0
        for action in actions:
            sign = 1 if action.steering > 1e-9 else (-1 if action.steering < -1e-9 else 0)
            if prev_sign and sign and sign != prev_sign:
                turns += 1
            if sign:
                prev_sign = sign
        stats: dict[str, object] = {
            "variant": "dang2022_strict",
            "elapsed_s": float(elapsed_s),
            "expansions": int(expansions),
            "path_length_m": float(length),
            "turning_points": int(turns),
            "motion_primitive_m": float(self.params.motion_primitive_m),
            "curvature_resolution": float(self.params.curvature_resolution),
            "sigma1": float(self.params.sigma1),
            "sigma2": float(self.params.sigma2),
            "movement_weight_length": float(self.params.movement_weight_length),
            "movement_weight_steering": float(self.params.movement_weight_steering),
            "movement_weight_switch": float(self.params.movement_weight_switch),
            "voronoi_alpha": float(self.params.voronoi_alpha),
            "voronoi_d_o_max": float(self.params.voronoi_d_o_max),
            "use_reeds_shepp_heuristic": str(bool(self.params.use_reeds_shepp_heuristic)),
        }
        if failure_reason is not None:
            stats["failure_reason"] = failure_reason
        if analytic is not None:
            stats.update(
                {
                    "analytic_curvature": float(analytic.curvature),
                    "analytic_cost": float(analytic.total_cost),
                    "analytic_voronoi_cost": float(analytic.voronoi_cost),
                    "analytic_motion_cost": float(analytic.motion_cost),
                    "analytic_path_length_m": float(analytic.path_length_m),
                }
            )
        return stats

    def plan(self, start: Pose, goal: Pose, timeout_s: float = 30.0) -> PlanResult:
        t0 = time.perf_counter()
        if self.collision.collides_pose(start):
            return PlanResult(False, [start], self._stats(path=[start], actions=[], expansions=0, elapsed_s=0.0, failure_reason="start_in_collision", analytic=None), [], [start])
        if self.collision.collides_pose(goal):
            elapsed = time.perf_counter() - t0
            return PlanResult(False, [start], self._stats(path=[start], actions=[], expansions=0, elapsed_s=elapsed, failure_reason="goal_in_collision", analytic=None), [], [start])

        dist_map = self._dijkstra_cost_to_go(goal)
        start_node = _Node(start, 0.0, self._heuristic(start, goal, dist_map), None, None)
        open_nodes: dict[tuple[int, int, int], _Node] = {self._discretize(start): start_node}
        closed: dict[tuple[int, int, int], float] = {}
        heap: list[tuple[float, int, tuple[int, int, int]]] = []
        counter = 0
        heapq.heappush(heap, (start_node.g + self.params.heuristic_weight * start_node.h, counter, self._discretize(start)))
        counter += 1
        expansions = 0

        while heap and (time.perf_counter() - t0) < float(timeout_s) and expansions < int(self.params.max_nodes):
            _, _, key = heapq.heappop(heap)
            node = open_nodes.pop(key, None)
            if node is None:
                continue
            if key in closed and node.g >= closed[key] - 1e-9:
                continue
            closed[key] = node.g
            expansions += 1

            if self._goal_reached(node.pose, goal):
                path, actions = self._reconstruct(node)
                dense_path = self._dense_from_actions(path, actions)
                elapsed = time.perf_counter() - t0
                return PlanResult(True, path, self._stats(path=path, actions=actions, expansions=expansions, elapsed_s=elapsed, failure_reason=None, analytic=None), [], dense_path)

            if expansions == 1 or expansions % max(1, int(self.params.analytic_expansion_interval)) == 0:
                candidates = self.evaluate_analytic_candidates(node.pose, goal)
                if candidates:
                    best = candidates[0]
                    prefix, prefix_actions = self._reconstruct(node)
                    path = prefix + best.path[1:]
                    actions = prefix_actions + best.actions
                    prefix_dense = self._dense_from_actions(prefix, prefix_actions)
                    if prefix_dense:
                        dense_path = prefix_dense + best.dense_path[1:]
                    else:
                        dense_path = list(best.dense_path)
                    elapsed = time.perf_counter() - t0
                    return PlanResult(True, path, self._stats(path=path, actions=actions, expansions=expansions, elapsed_s=elapsed, failure_reason=None, analytic=best), best.dense_path, dense_path)

            for primitive in self.primitives:
                samples = sample_constant_steer_motion(
                    node.pose,
                    primitive.steering,
                    primitive.direction,
                    primitive.step_m,
                    self.vehicle,
                    sample_step_m=self.params.collision_step_m,
                )
                if self.collision.collides_path(samples):
                    continue
                nxt = samples[-1]
                nxt_key = self._discretize(nxt)
                new_g = node.g + abs(float(primitive.step_m))
                if nxt_key in closed and new_g >= closed[nxt_key] - 1e-9:
                    continue
                h = self._heuristic(nxt, goal, dist_map)
                nxt_node = _Node(nxt, new_g, h, node, primitive)
                existing = open_nodes.get(nxt_key)
                if existing is not None and new_g >= existing.g - 1e-9:
                    continue
                open_nodes[nxt_key] = nxt_node
                priority = new_g + self.params.heuristic_weight * h
                heapq.heappush(heap, (priority, counter, nxt_key))
                counter += 1

        elapsed = time.perf_counter() - t0
        if not heap:
            failure = "open_set_exhausted"
        elif elapsed >= float(timeout_s):
            failure = "timeout"
        else:
            failure = "node_budget_exhausted"
        return PlanResult(False, [start], self._stats(path=[start], actions=[], expansions=expansions, elapsed_s=elapsed, failure_reason=failure, analytic=None), [], [start])
