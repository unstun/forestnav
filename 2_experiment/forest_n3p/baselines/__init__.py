from __future__ import annotations

from importlib import import_module

__all__ = [
    "BottleneckWaypointConfig",
    "BottleneckWaypointResult",
    "DQN10_BASELINE_METHODS",
    "Dqn10BaselinePlanResult",
    "IdBRrtAdapterAvailability",
    "IdBRrtAdapterConfig",
    "IdBRrtPlanResult",
    "ImprovedHybridAStarPlanner",
    "VoronoiWaypointConfig",
    "VoronoiWaypointResult",
    "check_idb_rrt_adapter",
    "compact_dqn10_stats",
    "plan_dqn10_baseline",
    "make_improved_ha_planner",
    "plan_bottleneck_waypoint",
    "plan_idb_rrt",
    "plan_voronoi_waypoint",
]

_EXPORT_MODULES = {
    "BottleneckWaypointConfig": "bottleneck_waypoint",
    "BottleneckWaypointResult": "bottleneck_waypoint",
    "DQN10_BASELINE_METHODS": "dqn10_full",
    "Dqn10BaselinePlanResult": "dqn10_full",
    "IdBRrtAdapterAvailability": "idb_rrt_adapter",
    "IdBRrtAdapterConfig": "idb_rrt_adapter",
    "IdBRrtPlanResult": "idb_rrt_adapter",
    "ImprovedHybridAStarPlanner": "improved_ha",
    "VoronoiWaypointConfig": "voronoi_waypoint",
    "VoronoiWaypointResult": "voronoi_waypoint",
    "check_idb_rrt_adapter": "idb_rrt_adapter",
    "compact_dqn10_stats": "dqn10_full",
    "plan_dqn10_baseline": "dqn10_full",
    "make_improved_ha_planner": "improved_ha",
    "plan_bottleneck_waypoint": "bottleneck_waypoint",
    "plan_idb_rrt": "idb_rrt_adapter",
    "plan_voronoi_waypoint": "voronoi_waypoint",
}


def __getattr__(name: str):
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(f"{__name__}.{module_name}"), name)
    globals()[name] = value
    return value
