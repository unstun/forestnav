from __future__ import annotations

import math

import numpy as np


def test_dominant_trajectories_and_transition_checks_on_open_grid():
    from yoon2017_strict.bezier import build_biarc
    from yoon2017_strict.collision import obstacle_free, refine_dominant_trajectories
    from yoon2017_strict.config import paper_algorithm_params, paper_sim_vehicle_params
    from yoon2017_strict.grid import GridMap
    from yoon2017_strict.geometry import Pose

    vehicle = paper_sim_vehicle_params()
    params = paper_algorithm_params()
    grid = GridMap(np.zeros((80, 80), dtype=np.uint8), resolution=0.5, origin=(0.0, 0.0))
    edge = build_biarc(
        Pose(5.0, 5.0, 0.0),
        Pose(20.0, 15.0, math.pi / 4.0),
        min_turn_radius_m=vehicle.min_turn_radius_m,
    )

    assert edge is not None
    pf, pr, vhs, vrs, crosses, pts = refine_dominant_trajectories(
        edge.seg1,
        vehicle,
        n_samples=params.samples_per_segment,
    )
    assert len(pf) == params.samples_per_segment + 1
    assert len(pr) == params.samples_per_segment + 1
    assert len(vhs) == len(vrs) == len(crosses) == len(pts)
    assert obstacle_free(
        edge,
        vehicle,
        grid,
        samples_per_segment=params.samples_per_segment,
        collision_step_m=0.25,
    )


def test_obstacle_free_rejects_blocking_obstacle():
    from yoon2017_strict.bezier import build_biarc
    from yoon2017_strict.collision import obstacle_free
    from yoon2017_strict.config import paper_algorithm_params, paper_sim_vehicle_params
    from yoon2017_strict.grid import GridMap
    from yoon2017_strict.geometry import Pose

    vehicle = paper_sim_vehicle_params()
    params = paper_algorithm_params()
    data = np.zeros((80, 80), dtype=np.uint8)
    data[8:14, 18:24] = 1
    grid = GridMap(data, resolution=0.5, origin=(0.0, 0.0))
    edge = build_biarc(
        Pose(5.0, 5.0, 0.0),
        Pose(20.0, 5.0, 0.0),
        min_turn_radius_m=vehicle.min_turn_radius_m,
    )

    assert edge is not None
    assert not obstacle_free(
        edge,
        vehicle,
        grid,
        samples_per_segment=params.samples_per_segment,
        collision_step_m=0.25,
    )
