from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class VehicleParams:
    front_overhang_m: float
    rear_overhang_m: float
    width_m: float
    min_turn_radius_m: float
    wheelbase_m: float | None = None
    max_velocity_m_s: float | None = None

    @property
    def length_m(self) -> float:
        return float(self.front_overhang_m) + float(self.rear_overhang_m)


@dataclass(frozen=True)
class AlgorithmParams:
    max_iterations: int = 8_000
    steer_step_m: float = 5.0
    neighbor_radius_m: float = 5.0
    goal_region_radius_m: float = 2.0
    goal_sample_rate: float = 0.05
    samples_per_segment: int = 24
    collision_step_m: float | None = None


def paper_sim_vehicle_params(**overrides: float) -> VehicleParams:
    vehicle = VehicleParams(
        front_overhang_m=3.4,
        rear_overhang_m=0.8,
        width_m=1.8,
        min_turn_radius_m=4.8,
    )
    return replace(vehicle, **overrides)


def paper_experiment_vehicle_params(**overrides: float) -> VehicleParams:
    vehicle = VehicleParams(
        front_overhang_m=3.5,
        rear_overhang_m=0.75,
        width_m=1.805,
        min_turn_radius_m=4.2,
        wheelbase_m=2.65,
    )
    return replace(vehicle, **overrides)


def paper_algorithm_params(**overrides: float | int) -> AlgorithmParams:
    params = AlgorithmParams()
    return replace(params, **overrides)


def paper_reference_values() -> dict[str, dict[str, float]]:
    return {
        "fig8": {
            "s_rrt_star_n2000_cost_m": 56.7,
            "s_rrt_star_n8000_cost_m": 55.7,
            "ss_rrt_star_n8000_cost_m": 56.1,
        },
        "fig9": {
            "narrow_passage_width_m": 3.7,
            "ss_rrt_star_cost_m": 37.5,
            "rs_rrt_star_cost_min_m": 36.5,
            "rs_rrt_star_cost_max_m": 37.3,
        },
        "fig10": {
            "rectangle_sampling_corner_spacing_m": 0.1,
        },
    }
