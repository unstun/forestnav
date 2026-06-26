from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math
import time

import numpy as np

from .bezier import BiarcEdge, build_biarc, edge_poses_and_length
from .collision import obstacle_free, vehicle_rectangle_collides
from .config import AlgorithmParams, VehicleParams, paper_algorithm_params, paper_sim_vehicle_params
from .geometry import Pose
from .grid import GridMap


@dataclass(frozen=True)
class PlanResult:
    success: bool
    path: list[Pose]
    stats: dict[str, object]


@dataclass
class _TreeNode:
    pose: Pose
    parent: int
    cost: float
    edge: BiarcEdge | None = None


class YoonSplineRRTStarPlanner:
    def __init__(
        self,
        grid_map: GridMap,
        vehicle: VehicleParams | None = None,
        params: AlgorithmParams | None = None,
    ):
        self.grid_map = grid_map
        self.vehicle = vehicle if vehicle is not None else paper_sim_vehicle_params()
        self.params = params if params is not None else paper_algorithm_params()
        self.collision_step_m = (
            float(self.params.collision_step_m)
            if self.params.collision_step_m is not None
            else 0.5 * float(self.grid_map.resolution)
        )

    def _pose_collides(self, pose: Pose) -> bool:
        return vehicle_rectangle_collides(self.grid_map, self.vehicle, pose.x, pose.y, pose.theta)

    @staticmethod
    def _euclid(a: Pose, b: Pose) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)

    def _sample(self, rng: np.random.Generator, goal: Pose) -> Pose:
        if float(rng.random()) < float(self.params.goal_sample_rate):
            return goal
        x, y, theta = self.grid_map.random_free_pose(rng)
        return Pose(x, y, theta)

    def _nearest(self, tree: list[_TreeNode], target: Pose) -> int:
        best_idx = 0
        best_dist = float("inf")
        for idx, node in enumerate(tree):
            dist = self._euclid(node.pose, target)
            if dist < best_dist:
                best_idx = idx
                best_dist = dist
        return best_idx

    def _steer(self, nearest: Pose, target: Pose) -> Pose:
        dx = target.x - nearest.x
        dy = target.y - nearest.y
        dist = math.hypot(dx, dy)
        if dist <= 1e-9:
            return target
        if dist <= float(self.params.steer_step_m):
            return target
        scale = float(self.params.steer_step_m) / dist
        x = nearest.x + dx * scale
        y = nearest.y + dy * scale
        theta = math.atan2(dy, dx)
        return Pose(float(x), float(y), float(theta))

    def _near(self, tree: list[_TreeNode], pose: Pose) -> list[int]:
        radius = float(self.params.neighbor_radius_m)
        return [idx for idx, node in enumerate(tree) if self._euclid(node.pose, pose) <= radius]

    def _edge_free(self, edge: BiarcEdge) -> bool:
        return obstacle_free(
            edge,
            self.vehicle,
            self.grid_map,
            samples_per_segment=int(self.params.samples_per_segment),
            collision_step_m=float(self.collision_step_m),
        )

    def _goal_reached(self, pose: Pose, goal: Pose) -> bool:
        return self._euclid(pose, goal) <= float(self.params.goal_region_radius_m)

    def _stats(
        self,
        *,
        success: bool,
        failure_reason: str | None,
        elapsed_s: float,
        iterations: int,
        nodes: int,
        path: list[Pose],
        exact_goal_appended: bool = False,
    ) -> dict[str, object]:
        length = 0.0
        for a, b in zip(path, path[1:]):
            length += math.hypot(b.x - a.x, b.y - a.y)
        out: dict[str, object] = {
            "variant": "yoon2017_strict",
            "paper_algorithm": "SS-RRT*",
            "success": bool(success),
            "elapsed_s": float(elapsed_s),
            "iterations": int(iterations),
            "nodes": int(nodes),
            "path_length_m": float(length),
            "steer_step_m": float(self.params.steer_step_m),
            "neighbor_radius_m": float(self.params.neighbor_radius_m),
            "goal_sample_rate": float(self.params.goal_sample_rate),
            "bezier_gamma_source": "computed_from_x_near_x_int_x_new",
            "samples_per_segment": int(self.params.samples_per_segment),
            "vehicle_front_overhang_m": float(self.vehicle.front_overhang_m),
            "vehicle_rear_overhang_m": float(self.vehicle.rear_overhang_m),
            "vehicle_width_m": float(self.vehicle.width_m),
            "vehicle_min_turn_radius_m": float(self.vehicle.min_turn_radius_m),
            "exact_goal_appended": bool(exact_goal_appended),
        }
        if failure_reason:
            out["failure_reason"] = failure_reason
        return out

    def plan(self, start: Pose, goal: Pose, *, seed: int = 0, timeout_s: float = 30.0) -> PlanResult:
        t0 = time.perf_counter()
        if self._pose_collides(start):
            return PlanResult(False, [start], self._stats(success=False, failure_reason="start_in_collision", elapsed_s=0.0, iterations=0, nodes=1, path=[start]))
        if self._pose_collides(goal):
            elapsed = time.perf_counter() - t0
            return PlanResult(False, [start], self._stats(success=False, failure_reason="goal_in_collision", elapsed_s=elapsed, iterations=0, nodes=1, path=[start]))

        rng = np.random.default_rng(int(seed))
        tree: list[_TreeNode] = [_TreeNode(start, -1, 0.0, None)]
        children: list[set[int]] = [set()]
        best_goal_idx: int | None = None
        iterations = 0

        for iteration in range(int(self.params.max_iterations)):
            if time.perf_counter() - t0 >= float(timeout_s):
                break
            iterations = iteration + 1
            sample = self._sample(rng, goal)
            nearest_idx = self._nearest(tree, sample)
            new_pose = self._steer(tree[nearest_idx].pose, sample)
            gx, gy = self.grid_map.world_to_grid(new_pose.x, new_pose.y)
            if not self.grid_map.in_bounds(gx, gy) or self._pose_collides(new_pose):
                continue
            near_indices = self._near(tree, new_pose)
            if nearest_idx not in near_indices:
                near_indices.append(nearest_idx)

            best_parent: int | None = None
            best_edge: BiarcEdge | None = None
            best_cost = float("inf")
            for candidate_idx in near_indices:
                candidate_pose = tree[candidate_idx].pose
                edge = build_biarc(
                    candidate_pose,
                    new_pose,
                    min_turn_radius_m=float(self.vehicle.min_turn_radius_m),
                    mode="new_wiring",
                )
                if edge is None or not self._edge_free(edge):
                    continue
                _poses, edge_len = edge_poses_and_length(edge, step_m=float(self.collision_step_m) * 2.0)
                cost = tree[candidate_idx].cost + edge_len
                if cost < best_cost:
                    best_parent = candidate_idx
                    best_edge = edge
                    best_cost = cost
            if best_parent is None or best_edge is None:
                continue

            tree.append(_TreeNode(new_pose, int(best_parent), float(best_cost), best_edge))
            children.append(set())
            new_idx = len(tree) - 1
            children[best_parent].add(new_idx)

            for near_idx in near_indices:
                if near_idx in (best_parent, new_idx):
                    continue
                edge = build_biarc(
                    tree[new_idx].pose,
                    tree[near_idx].pose,
                    min_turn_radius_m=float(self.vehicle.min_turn_radius_m),
                    mode="rewiring",
                )
                if edge is None or not self._edge_free(edge):
                    continue
                _poses, edge_len = edge_poses_and_length(edge, step_m=float(self.collision_step_m) * 2.0)
                proposed = tree[new_idx].cost + edge_len
                if proposed + 1e-9 < tree[near_idx].cost:
                    self._rewire_one(tree, children, near_idx, new_idx, edge, proposed)

            if self._goal_reached(new_pose, goal):
                if best_goal_idx is None or tree[new_idx].cost < tree[best_goal_idx].cost:
                    best_goal_idx = new_idx

        elapsed = time.perf_counter() - t0
        if best_goal_idx is None:
            failure = "timeout" if elapsed >= float(timeout_s) else "iteration_budget_exhausted"
            return PlanResult(False, [start], self._stats(success=False, failure_reason=failure, elapsed_s=elapsed, iterations=iterations, nodes=len(tree), path=[start]))

        exact_goal_appended = False
        final_goal_idx = best_goal_idx
        goal_edge = build_biarc(
            tree[best_goal_idx].pose,
            goal,
            min_turn_radius_m=float(self.vehicle.min_turn_radius_m),
            mode="new_wiring",
        )
        if goal_edge is not None and self._edge_free(goal_edge):
            _poses, edge_len = edge_poses_and_length(goal_edge, step_m=float(self.collision_step_m))
            tree.append(_TreeNode(goal, int(best_goal_idx), float(tree[best_goal_idx].cost + edge_len), goal_edge))
            children.append(set())
            children[best_goal_idx].add(len(tree) - 1)
            final_goal_idx = len(tree) - 1
            exact_goal_appended = True

        path = self._reconstruct(tree, final_goal_idx)
        elapsed = time.perf_counter() - t0
        return PlanResult(True, path, self._stats(success=True, failure_reason=None, elapsed_s=elapsed, iterations=iterations, nodes=len(tree), path=path, exact_goal_appended=exact_goal_appended))

    def _rewire_one(
        self,
        tree: list[_TreeNode],
        children: list[set[int]],
        near_idx: int,
        new_parent: int,
        new_edge: BiarcEdge,
        new_cost: float,
    ) -> None:
        old_parent = tree[near_idx].parent
        old_cost = tree[near_idx].cost
        if old_parent >= 0:
            children[old_parent].discard(near_idx)
        tree[near_idx].parent = int(new_parent)
        tree[near_idx].edge = new_edge
        tree[near_idx].cost = float(new_cost)
        children[new_parent].add(near_idx)
        delta = float(new_cost) - float(old_cost)
        if abs(delta) <= 1e-12:
            return
        q = deque(children[near_idx])
        while q:
            idx = q.popleft()
            tree[idx].cost += delta
            for child_idx in children[idx]:
                q.append(child_idx)

    def _reconstruct(self, tree: list[_TreeNode], goal_idx: int) -> list[Pose]:
        chain: list[int] = []
        cur = int(goal_idx)
        while cur >= 0:
            chain.append(cur)
            cur = tree[cur].parent
        chain.reverse()
        if not chain:
            return []
        path = [tree[chain[0]].pose]
        for idx in chain[1:]:
            edge = tree[idx].edge
            if edge is None:
                path.append(tree[idx].pose)
                continue
            poses, _length = edge_poses_and_length(edge, step_m=float(self.collision_step_m))
            path.extend(poses[1:])
        return path
