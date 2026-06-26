from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class VehicleParams:
    length_m: float = 4.8
    front_overhang_m: float = 0.95
    wheelbase_m: float = 2.8
    rear_overhang_m: float = 1.05
    width_m: float = 1.9
    max_accel_m_s2: float = 2.0
    max_omega_rad_s: float = 0.85
    max_velocity_m_s: float = 5.0
    max_steer_rad: float = 0.85

    @property
    def disc_radius_m(self) -> float:
        return 0.5 * ((self.length_m / 2.0) ** 2 + self.width_m**2) ** 0.5

    @property
    def disc_offsets_m(self) -> tuple[float, float]:
        body = self.front_overhang_m + self.wheelbase_m + self.rear_overhang_m
        return tuple(
            ((2.0 * j - 1.0) / 4.0) * body - self.rear_overhang_m
            for j in (1.0, 2.0)
        )


@dataclass(frozen=True)
class AlgorithmParams:
    mu1: float = 1.0
    mu2: float = 0.01
    mu3: float = 0.01
    initial_penalty: float = 1e6
    n_elements: int = 200
    disc_count: int = 2
    max_iterations: int = 10
    ipopt_max_iterations: int = 30
    penalty_growth: float = 5.0
    etol: float = 1e-4
    dl1_m: float = 1.0
    dl2_m: float = 0.1
    max_box_side_m: float = 8.0
    boundary_point_passage_threshold_cells: int = 30
    wide_passage_threshold_m: float = 4.5
    iha_xy_resolution_m: float = 0.2
    iha_heading_resolution_rad: float = 0.2
    beta: float = 10.0
    enable_local_state_constraint: bool = True
    local_area: tuple[float, float, float, float] = (-9.0, -2.0, -6.3, -6.0)
    local_speed_bounds_m_s: tuple[float, float] = (0.0, 2.0)


def load_vehicle_params(**overrides: float) -> VehicleParams:
    return replace(VehicleParams(), **overrides)


def load_algorithm_params(**overrides: float | int | bool) -> AlgorithmParams:
    return replace(AlgorithmParams(), **overrides)
