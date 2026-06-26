from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from matplotlib.path import Path as MplPath


Bounds = tuple[float, float, float, float]
Obstacle = np.ndarray


@dataclass(frozen=True)
class PaperScene:
    name: str
    bounds_m: Bounds
    cell_size_m: float
    grid: np.ndarray
    obstacles: tuple[Obstacle, ...]
    start: tuple[float, float, float, float, float]
    goal: tuple[float, float, float, float, float]
    note: str

    @property
    def origin_xy(self) -> tuple[float, float]:
        return self.bounds_m[0], self.bounds_m[2]


def _rot_rect(cx: float, cy: float, length: float, width: float, theta: float) -> Obstacle:
    c = math.cos(theta)
    s = math.sin(theta)
    pts = np.array(
        [
            [-length / 2.0, -width / 2.0],
            [length / 2.0, -width / 2.0],
            [length / 2.0, width / 2.0],
            [-length / 2.0, width / 2.0],
        ],
        dtype=float,
    )
    rot = np.array([[c, -s], [s, c]])
    return pts @ rot.T + np.array([cx, cy])


def _poly(points: Iterable[tuple[float, float]]) -> Obstacle:
    return np.asarray(list(points), dtype=float)


def _rasterize(bounds: Bounds, cell: float, obstacles: tuple[Obstacle, ...]) -> np.ndarray:
    xmin, xmax, ymin, ymax = bounds
    xs = np.arange(xmin, xmax + 0.5 * cell, cell)
    ys = np.arange(ymin, ymax + 0.5 * cell, cell)
    xx, yy = np.meshgrid(xs, ys)
    pts = np.column_stack([xx.ravel(), yy.ravel()])
    grid = np.zeros(xx.shape, dtype=np.uint8)
    occ = np.zeros(pts.shape[0], dtype=bool)
    for obstacle in obstacles:
        occ |= MplPath(obstacle).contains_points(pts)
    grid.ravel()[occ] = 1
    return grid


def _make_scene(
    name: str,
    obstacles: tuple[Obstacle, ...],
    start: tuple[float, float, float, float, float],
    goal: tuple[float, float, float, float, float],
) -> PaperScene:
    bounds = (-20.0, 20.0, -20.0, 20.0)
    cell = 0.2
    return PaperScene(
        name=name,
        bounds_m=bounds,
        cell_size_m=cell,
        grid=_rasterize(bounds, cell, obstacles),
        obstacles=obstacles,
        start=start,
        goal=goal,
        note="Figure-reconstructed scene from Lian et al. 2023 Fig. 5.",
    )


def build_scene(name: str) -> PaperScene:
    if name == "fig5a":
        obstacles = (
            _rot_rect(-10.5, 8.0, 5.6, 3.4, -0.75),
            _rot_rect(-9.0, -4.0, 6.0, 2.2, 1.05),
            _rot_rect(-0.5, -2.0, 5.5, 3.0, 0.35),
            _rot_rect(5.5, -11.0, 6.0, 2.6, 0.35),
            _rot_rect(9.5, 9.0, 5.2, 2.6, -0.55),
            _rot_rect(16.5, 6.5, 5.0, 3.0, 0.3),
        )
        return _make_scene("fig5a", obstacles, (-14.5, 16.0, -1.05, 0.0, 0.0), (10.8, -1.7, 0.0, 0.0, 0.0))

    if name == "fig5b":
        obstacles = (
            _rot_rect(-19.0, 7.5, 28.0, 2.0, math.pi / 2),
            _rot_rect(18.5, 7.5, 28.0, 2.0, math.pi / 2),
            _rot_rect(0.0, 3.0, 17.0, 2.1, math.pi / 2),
            _rot_rect(-11.0, 15.5, 4.8, 1.8, 0.0),
            _rot_rect(11.0, 15.5, 4.8, 1.8, 0.0),
            _rot_rect(-11.5, 8.5, 4.8, 1.8, 0.0),
            _rot_rect(11.5, 8.5, 4.8, 1.8, 0.0),
            _rot_rect(-11.5, 1.0, 4.8, 1.8, 0.0),
            _rot_rect(11.5, 1.0, 4.8, 1.8, 0.0),
            _rot_rect(-11.5, -5.0, 4.8, 1.8, 0.0),
            _rot_rect(11.5, -5.0, 4.8, 1.8, 0.0),
        )
        return _make_scene("fig5b", obstacles, (-15.0, -15.0, 0.0, 0.0, 0.0), (12.0, 6.0, 0.0, 0.0, 0.0))

    if name == "fig5c":
        obstacles = (
            _rot_rect(-15.0, 1.0, 10.0, 3.0, 1.28),
            _rot_rect(-7.5, 3.0, 2.0, 32.0, 0.0),
            _poly([(-1.8, -10.0), (1.2, -10.0), (1.2, -3.0), (2.4, -2.0), (1.4, 0.5), (-1.4, 0.5), (-2.5, -1.0)]),
            _rot_rect(1.0, 15.0, 3.0, 12.0, 0.0),
            _rot_rect(8.5, -2.0, 12.0, 1.5, 1.75),
            _rot_rect(14.5, -15.0, 4.0, 2.0, -0.45),
        )
        return _make_scene("fig5c", obstacles, (-15.0, -15.0, 0.0, 0.0, 0.0), (14.5, 13.5, math.pi / 2.0, 0.0, 0.0))

    if name == "fig5d":
        obstacles = (
            _rot_rect(-17.5, 1.0, 36.0, 1.2, math.pi / 2),
            _rot_rect(-5.5, 2.0, 32.0, 1.2, math.pi / 2),
            _rot_rect(6.5, 2.0, 32.0, 1.2, math.pi / 2),
            _rot_rect(18.0, 1.0, 36.0, 1.2, math.pi / 2),
            _rot_rect(-10.5, 10.0, 10.0, 1.5, math.pi / 2),
            _rot_rect(11.5, 10.0, 7.0, 1.5, 0.0),
            _rot_rect(11.5, -4.5, 7.0, 1.5, 0.0),
        )
        return _make_scene("fig5d", obstacles, (-14.5, -14.5, math.pi / 2.0, 0.0, 0.0), (14.0, -12.5, 0.0, 0.0, 0.0))

    raise ValueError(f"unknown scene: {name}")


def list_scene_names() -> tuple[str, ...]:
    return ("fig5a", "fig5b", "fig5c", "fig5d")
