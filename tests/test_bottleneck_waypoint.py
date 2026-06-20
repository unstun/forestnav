from __future__ import annotations

import numpy as np

from forest_n3p.baselines.bottleneck_waypoint import (
    BottleneckWaypointConfig,
    place_bottleneck_waypoints,
    plan_bottleneck_waypoint,
)
from forest_n3p.baselines.voronoi_waypoint import VoronoiWaypointConfig, build_skeleton_graph, path_length
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


def _gap_map(width: int = 140, height: int = 120, resolution: float = 0.1) -> GridMap:
    grid = np.zeros((height, width), dtype=np.uint8)
    wall_x = width // 2
    grid[:, wall_x] = 1
    grid[50:71, wall_x] = 0
    return GridMap(grid, resolution=resolution, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def _states(path: tuple[tuple[float, float, float], ...]) -> list[AckermannState]:
    return [AckermannState(float(x), float(y), float(theta)) for x, y, theta in path]


def test_bottleneck_waypoints_select_gap_center() -> None:
    grid_map = _gap_map()
    footprint = _footprint()
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=72)
    cfg = BottleneckWaypointConfig(
        min_bottleneck_separation_m=2.0,
        min_bottleneck_prominence_m=0.05,
        max_segment_arc_m=12.0,
    )
    graph = build_skeleton_graph(
        grid_map,
        (1.0, 6.0, 0.0),
        (12.0, 6.0, 0.0),
        footprint=footprint,
        config=VoronoiWaypointConfig(
            waypoint_spacing_m=cfg.max_segment_arc_m,
            connector_count=cfg.connector_count,
            safe_pose_search_window=cfg.safe_pose_search_window,
            segment_timeout_s=cfg.segment_timeout_s,
            segment_max_nodes=cfg.segment_max_nodes,
            skip_window=cfg.skip_window,
        ),
    )

    waypoints = place_bottleneck_waypoints(grid_map, graph.polyline, checker, config=cfg)

    assert waypoints
    narrowest = min(waypoints, key=lambda item: item.clearance_m)
    assert 6.0 <= narrowest.pose[0] <= 8.0
    assert 5.0 <= narrowest.pose[1] <= 7.0
    assert narrowest.kind in {"local_minimum", "long_gap_minimum"}
    assert not checker.collides_pose(*narrowest.pose)


def test_bottleneck_waypoint_baseline_returns_collision_free_path() -> None:
    grid_map = _gap_map()
    footprint = _footprint()
    cfg = BottleneckWaypointConfig(
        min_bottleneck_separation_m=2.0,
        min_bottleneck_prominence_m=0.05,
        max_segment_arc_m=8.0,
        segment_timeout_s=1.0,
        segment_max_nodes=2_000,
    )

    result = plan_bottleneck_waypoint(
        grid_map,
        footprint,
        (1.0, 6.0, 0.0),
        (12.0, 6.0, 0.0),
        config=cfg,
    )

    checker = GridFootprintChecker(grid_map, footprint, theta_bins=cfg.theta_bins)
    assert result.success, result.failure_reason
    assert result.path
    assert result.waypoints
    assert path_length(result.path) > 0.0
    assert not checker.collides_path(_states(result.path))
