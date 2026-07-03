from __future__ import annotations

from typing import Protocol

from forest_n3p.rl_rs.actions import SteeringAction
from forest_n3p.rl_rs.obs import RlRsObservation


class SteeringPolicy(Protocol):
    def act(self, observation: RlRsObservation) -> SteeringAction:
        """Return one forward-only steering action for the current observation."""
