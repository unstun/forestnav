from __future__ import annotations

import numpy as np

from forest_n3p.baselines.voronoi_waypoint import (
    VoronoiWaypointConfig,
    build_skeleton_graph,
    path_length,
    place_waypoints,
    plan_voronoi_waypoint,
)
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


def _empty_map(width: int = 220, height: int = 90, resolution: float = 0.1) -> GridMap:
    return GridMap(np.zeros((height, width), dtype=np.uint8), resolution=resolution, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def _states(path: tuple[tuple[float, float, float], ...]) -> list[AckermannState]:
    return [AckermannState(float(x), float(y), float(theta)) for x, y, theta in path]


def test_skeleton_graph_connects_start_and_goal() -> None:
    grid_map = _empty_map()
    footprint = _footprint()
    cfg = VoronoiWaypointConfig(waypoint_spacing_m=4.0)

    graph = build_skeleton_graph(
        grid_map,
        (1.0, 4.5, 0.0),
        (18.0, 4.5, 0.0),
        footprint=footprint,
        config=cfg,
    )

    assert graph.skeleton_node_count > 0
    assert graph.graph_edge_count > graph.skeleton_node_count
    assert graph.connector_count > 0
    assert graph.polyline[0] == (1.0, 4.5, 0.0)
    assert graph.polyline[-1] == (18.0, 4.5, 0.0)


def test_waypoint_placement_uses_safe_polyline_poses() -> None:
    grid_map = _empty_map()
    footprint = _footprint()
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=72)
    cfg = VoronoiWaypointConfig(waypoint_spacing_m=4.0)
    graph = build_skeleton_graph(
        grid_map,
        (1.0, 4.5, 0.0),
        (18.0, 4.5, 0.0),
        footprint=footprint,
        config=cfg,
    )

    waypoints = place_waypoints(graph.polyline, checker, config=cfg)

    assert len(waypoints) >= 3
    assert all(not checker.collides_pose(*pose) for pose in waypoints)


def test_voronoi_waypoint_baseline_returns_collision_free_path() -> None:
    grid_map = _empty_map()
    footprint = _footprint()
    cfg = VoronoiWaypointConfig(
        waypoint_spacing_m=4.0,
        segment_timeout_s=1.0,
        segment_max_nodes=2_000,
        skip_window=3,
    )

    result = plan_voronoi_waypoint(
        grid_map,
        footprint,
        (1.0, 4.5, 0.0),
        (18.0, 4.5, 0.0),
        config=cfg,
    )

    checker = GridFootprintChecker(grid_map, footprint, theta_bins=cfg.theta_bins)
    assert result.success, result.failure_reason
    assert result.path
    assert len(result.waypoints) >= 3
    assert path_length(result.path) > 0.0
    assert not checker.collides_path(_states(result.path))
