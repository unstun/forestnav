from __future__ import annotations

from dataclasses import dataclass, replace
import math


@dataclass(frozen=True)
class VehicleParams:
    length_m: float = 4.3
    width_m: float = 2.0
    wheelbase_m: float = 3.0
    max_steer_rad: float = 0.6
    max_velocity_m_s: float = 1.0
    collision_model: str = "rectangle"
    circle_radius_m: float | None = None
    circle_center_offset_m: float | None = None
    circle_center_shift_m: float = 0.0

    @property
    def max_curvature(self) -> float:
        return math.tan(float(self.max_steer_rad)) / max(float(self.wheelbase_m), 1e-9)

    @property
    def min_turn_radius_m(self) -> float:
        return 1.0 / max(float(self.max_curvature), 1e-9)


@dataclass(frozen=True)
class AlgorithmParams:
    curvature_resolution: float = 0.05
    motion_primitive_m: float = 1.5
    sigma1: float = 1.0
    sigma2: float = 1.0
    movement_weight_length: float = 1.0
    movement_weight_steering: float = 1.0
    movement_weight_switch: float = 1.0
    voronoi_alpha: float = 5.0
    voronoi_d_o_max: float = 5.0
    theta_bins: int = 72
    analytic_expansion_interval: int = 8
    heuristic_weight: float = 1.0
    use_reeds_shepp_heuristic: bool = True
    max_nodes: int = 500_000
    collision_step_m: float = 0.2
    goal_xy_tolerance_m: float = 0.3
    goal_theta_tolerance_rad: float = math.pi


def paper_vehicle_params(**overrides: float) -> VehicleParams:
    return replace(VehicleParams(), **overrides)


def paper_algorithm_params(**overrides: float | int) -> AlgorithmParams:
    return replace(AlgorithmParams(), **overrides)


def paper_table1_targets() -> dict[str, dict[str, dict[str, float]]]:
    return {
        "map_a": {
            "original": {"curvature": 0.23, "cost": 15.27, "length_m": 34.07, "time_s": 0.022},
            "improved": {"curvature": 0.15, "cost": 8.18, "length_m": 34.05, "time_s": 0.100},
        },
        "map_b": {
            "original": {"curvature": 0.23, "cost": 5.85, "length_m": 19.83, "time_s": 0.015},
            "improved": {"curvature": 0.10, "cost": 5.52, "length_m": 20.25, "time_s": 0.139},
        },
    }


def paper_table2_targets() -> dict[str, dict[str, object]]:
    return {
        "map12": {
            "turning_before": 13,
            "original": {"curvature": 0.23, "cost": 6.17, "length_m": 26.29, "time_s": 0.014},
            "improved": {"curvature": 0.15, "cost": 4.69, "length_m": 23.10, "time_s": 0.096},
            "turning_after": 10,
        },
        "den520d": {
            "turning_before": 14,
            "original": {"curvature": 0.23, "cost": 5.03, "length_m": 27.40, "time_s": 0.020},
            "improved": {"curvature": 0.15, "cost": 4.03, "length_m": 29.43, "time_s": 0.140},
            "turning_after": 9,
        },
        "ost003d": {
            "turning_before": 8,
            "original": {"curvature": 0.23, "cost": 3.89, "length_m": 24.51, "time_s": 0.018},
            "improved": {"curvature": 0.10, "cost": 3.27, "length_m": 25.26, "time_s": 0.166},
            "turning_after": 6,
        },
    }
