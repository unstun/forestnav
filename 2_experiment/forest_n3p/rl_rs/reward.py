from __future__ import annotations

from dataclasses import dataclass

from forest_n3p.rl_rs.terminal import TerminalRsCheckResult


@dataclass(frozen=True)
class RewardConfig:
    terminal_rs_success: float = 1.0

    def __post_init__(self) -> None:
        if not self.terminal_rs_success >= 0.0:
            raise ValueError("terminal_rs_success must be non-negative")


@dataclass(frozen=True)
class RewardBreakdown:
    total: float
    status: str = "e02_1_terminal_rs_success"
    success: float = 0.0
    collision: float = 0.0
    progress: float = 0.0
    clearance: float = 0.0
    curvature: float = 0.0
    step: float = 0.0


def compute_terminal_success_reward(
    *,
    terminal_rs: TerminalRsCheckResult,
    collided: bool,
    config: RewardConfig,
) -> RewardBreakdown:
    success = float(config.terminal_rs_success) if terminal_rs.success and not collided else 0.0
    return RewardBreakdown(total=success, success=success)


def pending_reward_breakdown() -> RewardBreakdown:
    """E02 前的占位: API 可运行, 但不得当作最终 reward 配方。"""

    return RewardBreakdown(total=0.0, status="pending_e02")
