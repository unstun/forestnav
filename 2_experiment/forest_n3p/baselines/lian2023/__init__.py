"""Lian 2023 expert planner 顶层 API。"""
from forest_n3p.baselines.lian2023.types import (
    BoundaryPoint,
    CorridorSegment,
    PlanResult,
    PlanStatus,
    TrajPoint,
)


__all__ = [
    "LianPlanner",
    "LianPlannerConfig",
    "PlanStatus",
    "PlanResult",
    "TrajPoint",
    "CorridorSegment",
    "BoundaryPoint",
    "quantize_to_action_table",
]


def __getattr__(name: str):
    if name in {"LianPlanner", "LianPlannerConfig"}:
        from forest_n3p.baselines.lian2023.planner import LianPlanner, LianPlannerConfig

        return {"LianPlanner": LianPlanner, "LianPlannerConfig": LianPlannerConfig}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def quantize_to_action_table(
    *,
    desired_a: float,
    desired_omega: float,
    action_table,
    delta_dot_max: float,
    a_max: float,
) -> int:
    """连续 (a, ω) → 35 离散动作最近邻索引。设计 §4.2。"""
    import numpy as np
    table = np.asarray(action_table)
    omega_norm = table[:, 0] / max(1e-9, delta_dot_max)
    a_norm = table[:, 1] / max(1e-9, a_max)
    target_om = float(desired_omega) / max(1e-9, delta_dot_max)
    target_a = float(desired_a) / max(1e-9, a_max)
    dist2 = (omega_norm - target_om) ** 2 + (a_norm - target_a) ** 2
    return int(np.argmin(dist2))
