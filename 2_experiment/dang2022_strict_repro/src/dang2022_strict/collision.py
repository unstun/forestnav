from __future__ import annotations

import math

from .config import VehicleParams
from .grid import GridMap
from .robot import Pose


class GridCollisionChecker:
    def __init__(self, grid_map: GridMap, vehicle: VehicleParams):
        self.grid_map = grid_map
        self.vehicle = vehicle

    def collides_pose(self, pose: Pose) -> bool:
        if self.vehicle.collision_model == "two_circle":
            return self._collides_two_circle_pose(pose)
        gx, gy = self.grid_map.world_to_grid(pose.x, pose.y)
        if not self.grid_map.in_bounds(gx, gy):
            return True
        length = float(self.vehicle.length_m)
        width = float(self.vehicle.width_m)
        res = float(self.grid_map.resolution)
        radius = 0.5 * math.hypot(length, width)
        cells = int(math.ceil((radius + res) / res))
        c = math.cos(pose.theta)
        s = math.sin(pose.theta)
        for yy in range(gy - cells, gy + cells + 1):
            for xx in range(gx - cells, gx + cells + 1):
                if not self.grid_map.in_bounds(xx, yy):
                    return True
                if not self.grid_map.is_occupied_index(xx, yy):
                    continue
                wx, wy = self.grid_map.grid_to_world(xx, yy)
                dx = wx - pose.x
                dy = wy - pose.y
                rx = c * dx + s * dy
                ry = -s * dx + c * dy
                if abs(rx) <= 0.5 * length + 0.5 * res and abs(ry) <= 0.5 * width + 0.5 * res:
                    return True
        return False

    def _collides_circle(self, x_m: float, y_m: float, radius_m: float) -> bool:
        grid = self.grid_map
        reach = float(radius_m) + 0.5 * float(grid.resolution)
        gx, gy = grid.world_to_grid(x_m, y_m)
        cells = int(math.ceil(reach / float(grid.resolution))) + 1
        half = 0.5 * float(grid.resolution)
        radius_sq = float(radius_m) * float(radius_m) + 1e-12
        for yy in range(gy - cells, gy + cells + 1):
            for xx in range(gx - cells, gx + cells + 1):
                if not grid.in_bounds(xx, yy):
                    return True
                if not grid.is_occupied_index(xx, yy):
                    continue
                wx, wy = grid.grid_to_world(xx, yy)
                dx = max(abs(float(wx) - float(x_m)) - half, 0.0)
                dy = max(abs(float(wy) - float(y_m)) - half, 0.0)
                if dx * dx + dy * dy <= radius_sq:
                    return True
        return False

    def _collides_two_circle_pose(self, pose: Pose) -> bool:
        radius = self.vehicle.circle_radius_m
        offset = self.vehicle.circle_center_offset_m
        if radius is None or offset is None:
            raise ValueError("two_circle collision model requires circle radius and offset")
        shift = float(self.vehicle.circle_center_shift_m)
        c = math.cos(pose.theta)
        s = math.sin(pose.theta)
        mid_x = pose.x + c * shift
        mid_y = pose.y + s * shift
        for sign in (1.0, -1.0):
            cx = mid_x + sign * c * float(offset)
            cy = mid_y + sign * s * float(offset)
            if self._collides_circle(cx, cy, float(radius)):
                return True
        return False

    def collides_path(self, poses: list[Pose]) -> bool:
        return any(self.collides_pose(pose) for pose in poses)
