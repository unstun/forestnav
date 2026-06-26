from __future__ import annotations

import math

import numpy as np


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def test_new_wiring_selects_x_int_with_equal_endpoint_distances():
    from yoon2017_strict.bezier import build_biarc
    from yoon2017_strict.geometry import Pose

    start = Pose(0.0, 0.0, 0.0)
    end = Pose(6.0, 4.0, 0.0)

    edge = build_biarc(start, end, min_turn_radius_m=1.0, mode="new_wiring")

    assert edge is not None
    assert math.isclose(_dist((start.x, start.y), edge.x_int), _dist((end.x, end.y), edge.x_int))
    assert not math.isclose(edge.gamma_rad, 0.4)


def test_two_cubic_beziers_use_yang_symmetric_control_point_geometry():
    from yoon2017_strict.bezier import build_biarc
    from yoon2017_strict.geometry import Pose

    start = Pose(0.0, 0.0, 0.0)
    end = Pose(6.0, 4.0, 0.0)

    edge = build_biarc(start, end, min_turn_radius_m=1.0, mode="new_wiring")

    assert edge is not None
    assert np.allclose(edge.seg1.p3, edge.seg2.p0, atol=1e-9)
    assert edge.straight_start is not None
    assert edge.straight_end is not None

    x_int = edge.x_int
    assert math.isclose(_dist(edge.seg1.p0, x_int), edge.curve_distance_m)
    assert math.isclose(_dist(edge.seg2.p3, x_int), edge.curve_distance_m)
    assert math.isclose(edge.seg1.p0[1], x_int[1], abs_tol=1e-9)
    assert math.isclose(edge.seg1.p1[1], x_int[1], abs_tol=1e-9)
    assert math.isclose(edge.seg1.p2[1], x_int[1], abs_tol=1e-9)


def test_rewiring_selects_x_int_on_x_new_heading_line():
    from yoon2017_strict.bezier import build_biarc
    from yoon2017_strict.geometry import Pose

    x_new = Pose(0.0, 0.0, 0.0)
    x_near = Pose(5.0, 3.0, 0.0)

    edge = build_biarc(x_new, x_near, min_turn_radius_m=1.0, mode="rewiring")

    assert edge is not None
    assert math.isclose(edge.x_int[1], 0.0, abs_tol=1e-9)
    assert edge.x_int[0] > x_new.x
