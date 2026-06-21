from __future__ import annotations

from importlib import import_module

__all__ = [
    "BottleneckWaypointConfig",
    "BottleneckWaypointResult",
    "MdDqnAdapterAvailability",
    "MdDqnAdapterConfig",
    "MdDqnPlanResult",
    "VoronoiWaypointConfig",
    "VoronoiWaypointResult",
    "check_md_dqn_adapter",
    "plan_md_dqn",
    "plan_bottleneck_waypoint",
    "plan_voronoi_waypoint",
]

_EXPORT_MODULES = {
    "BottleneckWaypointConfig": "bottleneck_waypoint",
    "BottleneckWaypointResult": "bottleneck_waypoint",
    "MdDqnAdapterAvailability": "md_dqn_adapter",
    "MdDqnAdapterConfig": "md_dqn_adapter",
    "MdDqnPlanResult": "md_dqn_adapter",
    "VoronoiWaypointConfig": "voronoi_waypoint",
    "VoronoiWaypointResult": "voronoi_waypoint",
    "check_md_dqn_adapter": "md_dqn_adapter",
    "plan_md_dqn": "md_dqn_adapter",
    "plan_bottleneck_waypoint": "bottleneck_waypoint",
    "plan_voronoi_waypoint": "voronoi_waypoint",
}


def __getattr__(name: str):
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(f"{__name__}.{module_name}"), name)
    globals()[name] = value
    return value
