from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RewardBreakdown:
    total: float
    success: float = 0.0
    collision: float = 0.0
    progress: float = 0.0
    clearance: float = 0.0
    curvature: float = 0.0
    step: float = 0.0


def pending_reward_breakdown() -> RewardBreakdown:
    """E02 前的占位: API 可运行, 但不得当作最终 reward 配方。"""

    return RewardBreakdown(total=0.0)
