from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional, Protocol, Tuple, runtime_checkable

from ..primitives import MotionPrimitive
from ..robot import AckermannState


class DangRsPlannerContext(Protocol):
    analytic_operator: str
    _last_analytic_telemetry: Any

    def _try_analytic_expansion(
        self,
        state: AckermannState,
        goal: AckermannState,
    ) -> Optional[Tuple[List[AckermannState], List[MotionPrimitive]]]:
        ...


@dataclass(frozen=True)
class AnalyticExpansionResult:
    states: List[AckermannState]
    actions: List[MotionPrimitive]
    telemetry: Any
    terminal_rs_used: bool
    operator: str

    def __post_init__(self) -> None:
        if len(self.states) != len(self.actions):
            raise ValueError("states/actions length mismatch")

    def to_legacy_tuple(self) -> Tuple[List[AckermannState], List[MotionPrimitive]]:
        return self.states, self.actions


@runtime_checkable
class AnalyticExpansionOperator(Protocol):
    name: str

    def try_connect(
        self,
        state: AckermannState,
        goal: AckermannState,
        context: DangRsPlannerContext,
    ) -> Optional[AnalyticExpansionResult]:
        ...


@dataclass(frozen=True)
class DangRsOperator:
    """Adapter exposing the current planner-owned RS analytic expansion as an operator."""

    name: str = "dang_multi_rs"

    def try_connect(
        self,
        state: AckermannState,
        goal: AckermannState,
        context: DangRsPlannerContext,
    ) -> Optional[AnalyticExpansionResult]:
        result = context._try_analytic_expansion(state, goal)
        if result is None:
            return None
        states, actions = result
        return AnalyticExpansionResult(
            states=list(states),
            actions=list(actions),
            telemetry=getattr(context, "_last_analytic_telemetry", None),
            terminal_rs_used=True,
            operator=str(getattr(context, "analytic_operator", self.name)),
        )
