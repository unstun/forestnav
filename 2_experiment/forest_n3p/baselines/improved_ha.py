from __future__ import annotations

import math

from forest_n3p.third_party.pathplan import AckermannParams, GridMap, HybridAStarPlanner, TwoCircleFootprint
from forest_n3p.third_party.pathplan.hybrid_a_star.voronoi_field import (
    compute_voronoi_field,
    path_mean_voronoi,
)
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive
from forest_n3p.third_party.pathplan.robot import AckermannState


class ImprovedHybridAStarPlanner(HybridAStarPlanner):
    """Hybrid A* adapter with Dang-style Voronoi field scoring.

    The upstream planner already implements multi-curvature Reeds-Shepp
    analytic expansion. This adapter only changes the analytic-expansion score:
    it keeps the obstacle-distance risk term and adds the GVD-based Voronoi
    field term from ``voronoi_field.py``. The implementation lives outside
    ``third_party`` so the vendored planner remains untouched.
    """

    def __init__(
        self,
        grid_map: GridMap,
        footprint: TwoCircleFootprint,
        params: AckermannParams,
        *,
        voronoi_alpha: float = 5.0,
        voronoi_d_o_max: float = 5.0,
        **kwargs,
    ) -> None:
        super().__init__(grid_map, footprint, params, **kwargs)
        self._voronoi_field = compute_voronoi_field(
            grid_map,
            alpha=float(voronoi_alpha),
            d_o_max=float(voronoi_d_o_max),
        )

    def _dang2022_cost(self, states: list[AckermannState], actions: list[MotionPrimitive]) -> float:
        # ---- v: obstacle-distance risk + GVD Voronoi field -----------------
        clearance_risk = 1.0 / max(self._path_mean_clearance(states), 0.01)
        gvd_risk = path_mean_voronoi(self._voronoi_field, self.map, states)
        v = clearance_risk + gvd_risk

        # ---- m: motion cost, matching the vendored planner's Eq. 4 shape ----
        length_cost = 0.0
        steering_cost = 0.0
        steering_switches = 0
        prev_steer_sign = 0
        for action in actions:
            length_cost += abs(float(action.step))
            steering_cost += abs(float(action.steering))
            cur_sign = 1 if action.steering > 1e-9 else (-1 if action.steering < -1e-9 else 0)
            if prev_steer_sign != 0 and cur_sign != 0 and cur_sign != prev_steer_sign:
                steering_switches += 1
            if cur_sign != 0:
                prev_steer_sign = cur_sign
        motion_cost = length_cost + steering_cost + float(steering_switches)

        return float(self.sigma1) * v + float(self.sigma2) * motion_cost


def make_improved_ha_planner(
    grid_map: GridMap,
    footprint: TwoCircleFootprint,
    *,
    theta_bins: int = 72,
) -> ImprovedHybridAStarPlanner:
    return ImprovedHybridAStarPlanner(
        grid_map,
        footprint,
        AckermannParams(wheelbase=0.6, min_turn_radius=1.0),
        analytic_expansion=True,
        collision_step=0.1,
        goal_xy_tol=0.30,
        goal_theta_tol=math.radians(15.0),
        use_holonomic_heuristic=True,
        theta_bins=int(theta_bins),
        curvature_step=0.05,
        max_curvature_ratio=2.0,
        sigma1=0.4,
        sigma2=0.6,
    )


__all__ = ["ImprovedHybridAStarPlanner", "make_improved_ha_planner"]
