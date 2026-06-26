from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .config import AlgorithmParams


@dataclass(frozen=True)
class CorridorBox:
    center: tuple[float, float]
    tangent: tuple[float, float]
    left_m: float
    right_m: float
    up_m: float
    down_m: float
    arc_m: float
    is_wide: bool

    @property
    def min_side_m(self) -> float:
        return min(self.left_m + self.right_m, self.up_m + self.down_m)


@dataclass(frozen=True)
class PassageGroup:
    kind: str
    boxes: tuple[CorridorBox, ...]
    nodes: np.ndarray | None = None
    start_index: int = 0
    end_index: int = 0


@dataclass(frozen=True)
class Algorithm1Stage1:
    boxes: tuple[CorridorBox, ...]
    groups: tuple[PassageGroup, ...]
    swps: tuple[PassageGroup, ...]
    snps: tuple[PassageGroup, ...]
    xseq: tuple[PassageGroup, ...]
    xbou: np.ndarray
    xbou_corrected: np.ndarray


def _free(scene_grid: np.ndarray, scene_bounds: tuple[float, float, float, float], cell: float, x: float, y: float) -> bool:
    xmin, _xmax, ymin, _ymax = scene_bounds
    ix = int(round((x - xmin) / cell))
    iy = int(round((y - ymin) / cell))
    if not (0 <= iy < scene_grid.shape[0] and 0 <= ix < scene_grid.shape[1]):
        return False
    return scene_grid[iy, ix] == 0


def _expand_side(
    grid: np.ndarray,
    bounds: tuple[float, float, float, float],
    cell: float,
    center: np.ndarray,
    normal: np.ndarray,
    sign: float,
    params: AlgorithmParams,
) -> float:
    dist = 0.0
    while dist + params.dl2_m <= params.max_box_side_m:
        candidate = center + normal * sign * (dist + params.dl2_m)
        if not _free(grid, bounds, cell, float(candidate[0]), float(candidate[1])):
            break
        dist += params.dl2_m
    return dist


def build_two_stage_corridor(
    grid: np.ndarray,
    bounds: tuple[float, float, float, float],
    cell: float,
    path_xy: np.ndarray,
    params: AlgorithmParams,
) -> list[CorridorBox]:
    if len(path_xy) < 2:
        return []
    samples: list[CorridorBox] = []
    carry = 0.0
    arc = 0.0
    last_sample = path_xy[0]
    for idx in range(len(path_xy) - 1):
        a = path_xy[idx]
        b = path_xy[idx + 1]
        seg = b - a
        seg_len = float(np.linalg.norm(seg))
        if seg_len <= 1e-9:
            continue
        tangent = seg / seg_len
        normal = np.array([-tangent[1], tangent[0]], dtype=float)
        dist = params.dl1_m - carry
        while dist <= seg_len + 1e-9:
            center = a + tangent * dist
            arc += float(np.linalg.norm(center - last_sample))
            left = _expand_side(grid, bounds, cell, center, np.array([1.0, 0.0]), -1.0, params)
            right = _expand_side(grid, bounds, cell, center, np.array([1.0, 0.0]), +1.0, params)
            up = _expand_side(grid, bounds, cell, center, np.array([0.0, 1.0]), +1.0, params)
            down = _expand_side(grid, bounds, cell, center, np.array([0.0, 1.0]), -1.0, params)
            min_side = min(left + right, up + down)
            samples.append(
                CorridorBox(
                    center=(float(center[0]), float(center[1])),
                    tangent=(float(tangent[0]), float(tangent[1])),
                    left_m=float(left),
                    right_m=float(right),
                    up_m=float(up),
                    down_m=float(down),
                    arc_m=float(arc),
                    is_wide=min_side >= params.wide_passage_threshold_m,
                )
            )
            last_sample = center
            dist += params.dl1_m
        carry = max(0.0, seg_len - (dist - params.dl1_m))
    return samples


def build_corridor(
    grid: np.ndarray,
    bounds: tuple[float, float, float, float],
    cell: float,
    path_xy: np.ndarray,
    params: AlgorithmParams,
) -> list[CorridorBox]:
    return build_two_stage_corridor(grid, bounds, cell, path_xy, params)


def split_wide_narrow_paths(boxes: list[CorridorBox]) -> list[PassageGroup]:
    if not boxes:
        return []
    groups: list[PassageGroup] = []
    current_kind = "wide" if boxes[0].is_wide else "narrow"
    current: list[CorridorBox] = []
    for box in boxes:
        kind = "wide" if box.is_wide else "narrow"
        if kind != current_kind and current:
            groups.append(PassageGroup(kind=current_kind, boxes=tuple(current)))
            current = []
            current_kind = kind
        current.append(box)
    if current:
        groups.append(PassageGroup(kind=current_kind, boxes=tuple(current)))
    return groups


def _nearest_box_indices(path_xy: np.ndarray, boxes: list[CorridorBox]) -> np.ndarray:
    centers = np.asarray([box.center for box in boxes], dtype=float)
    indices = np.zeros(len(path_xy), dtype=int)
    for idx, point in enumerate(path_xy):
        indices[idx] = int(np.argmin(np.sum((centers - point) ** 2, axis=1)))
    return indices


def _judge_node_kind(box: CorridorBox, params: AlgorithmParams) -> str:
    return "wide" if box.min_side_m >= params.wide_passage_threshold_m else "narrow"


def _build_node_passage_sets(
    path_xy: np.ndarray,
    boxes: list[CorridorBox],
    params: AlgorithmParams,
) -> tuple[tuple[PassageGroup, ...], tuple[PassageGroup, ...], tuple[PassageGroup, ...]]:
    if len(path_xy) == 0 or not boxes:
        return tuple(), tuple(), tuple()
    box_indices = _nearest_box_indices(path_xy, boxes)
    groups: list[PassageGroup] = []
    current_kind = _judge_node_kind(boxes[int(box_indices[0])], params)
    current_start = 0
    for node_idx in range(1, len(path_xy)):
        kind = _judge_node_kind(boxes[int(box_indices[node_idx])], params)
        if kind == current_kind:
            continue
        groups.append(
            _passage_group_from_node_span(
                current_kind,
                path_xy,
                boxes,
                box_indices,
                current_start,
                node_idx - 1,
            )
        )
        current_kind = kind
        current_start = node_idx
    groups.append(
        _passage_group_from_node_span(
            current_kind,
            path_xy,
            boxes,
            box_indices,
            current_start,
            len(path_xy) - 1,
        )
    )
    swps = tuple(group for group in groups if group.kind == "wide")
    snps = tuple(group for group in groups if group.kind == "narrow")
    return swps, snps, tuple(groups)


def _passage_group_from_node_span(
    kind: str,
    path_xy: np.ndarray,
    boxes: list[CorridorBox],
    box_indices: np.ndarray,
    start_index: int,
    end_index: int,
) -> PassageGroup:
    span_indices = box_indices[start_index : end_index + 1]
    unique_box_indices = np.unique(span_indices)
    return PassageGroup(
        kind=kind,
        boxes=tuple(boxes[int(idx)] for idx in unique_box_indices),
        nodes=np.asarray(path_xy[start_index : end_index + 1], dtype=float),
        start_index=int(start_index),
        end_index=int(end_index),
    )


def correct_boundary_points(points: np.ndarray, *, cell_size_m: float, params: AlgorithmParams) -> np.ndarray:
    """LPthre clustering helper for standalone probes, not Algorithm 1's main route."""
    if len(points) <= 2:
        return points.copy()
    threshold_m = float(params.boundary_point_passage_threshold_cells) * float(cell_size_m)
    out = [points[0]]
    cluster: list[np.ndarray] = []
    for point in points[1:-1]:
        if np.linalg.norm(point[:2] - out[-1][:2]) < threshold_m:
            cluster.append(point)
            continue
        if cluster:
            out.append(cluster[len(cluster) // 2])
            cluster = []
        out.append(point)
    if cluster:
        out.append(cluster[len(cluster) // 2])
    out.append(points[-1])
    return np.asarray(out, dtype=float)


def boundary_points(
    path_xy: np.ndarray,
    boxes: list[CorridorBox],
    start_theta: float,
    goal_theta: float,
    params: AlgorithmParams,
) -> np.ndarray:
    return build_algorithm1_stage1(path_xy, boxes, start_theta, goal_theta, params).xbou_corrected


def build_algorithm1_stage1(
    path_xy: np.ndarray,
    boxes: list[CorridorBox],
    start_theta: float,
    goal_theta: float,
    params: AlgorithmParams,
) -> Algorithm1Stage1:
    if len(path_xy) < 2 or not boxes:
        empty = np.empty((0, 3), dtype=float)
        return Algorithm1Stage1(tuple(boxes), tuple(), tuple(), tuple(), tuple(), empty, empty)
    swps, snps, groups = _build_node_passage_sets(path_xy, boxes, params)
    points = _extract_boundary_points_from_xseq(groups, start_theta, goal_theta)
    if len(points) == 0:
        points = np.asarray(
            [
                (float(path_xy[0, 0]), float(path_xy[0, 1]), float(start_theta)),
                (float(path_xy[-1, 0]), float(path_xy[-1, 1]), float(goal_theta)),
            ],
            dtype=float,
        )
    xbou = np.asarray(points, dtype=float)
    corrected = _correct_boundary_points_from_xseq(xbou, groups, params)
    corrected[0, 2] = start_theta
    corrected[-1, 2] = goal_theta
    return Algorithm1Stage1(tuple(boxes), groups, swps, snps, groups, xbou, corrected)


def _extract_boundary_points_from_xseq(
    xseq: tuple[PassageGroup, ...],
    start_theta: float,
    goal_theta: float,
) -> np.ndarray:
    if not xseq:
        return np.empty((0, 3), dtype=float)
    points: list[tuple[float, float, float]] = []
    for idx, group in enumerate(xseq):
        nodes = group.nodes
        if nodes is None or len(nodes) == 0:
            continue
        start_heading = start_theta if idx == 0 else _path_start_heading(nodes, start_theta)
        end_heading = goal_theta if idx == len(xseq) - 1 else _path_end_heading(nodes, start_heading)
        points.append((float(nodes[0, 0]), float(nodes[0, 1]), float(start_heading)))
        points.append((float(nodes[-1, 0]), float(nodes[-1, 1]), float(end_heading)))
    xbou = np.asarray(points, dtype=float)
    keep = [0]
    for idx in range(1, len(xbou)):
        if np.linalg.norm(xbou[idx, :2] - xbou[keep[-1], :2]) > 1e-6:
            keep.append(idx)
    return xbou[keep]


def _correct_boundary_points_from_xseq(
    xbou: np.ndarray,
    xseq: tuple[PassageGroup, ...],
    params: AlgorithmParams,
) -> np.ndarray:
    """Deduplicate repeated transition endpoints while preserving passage-boundary nodes."""
    if len(xbou) <= 2:
        return xbou.copy()
    keep = [0]
    for idx in range(1, len(xbou)):
        if np.linalg.norm(xbou[idx, :2] - xbou[keep[-1], :2]) > 1e-6:
            keep.append(idx)
    return xbou[keep].copy()


def _path_start_heading(nodes: np.ndarray, fallback: float) -> float:
    if len(nodes) < 2:
        return float(fallback)
    delta = nodes[1] - nodes[0]
    if np.linalg.norm(delta) <= 1e-9:
        return float(fallback)
    return float(math.atan2(delta[1], delta[0]))


def _path_end_heading(nodes: np.ndarray, fallback: float) -> float:
    if len(nodes) < 2:
        return float(fallback)
    delta = nodes[-1] - nodes[-2]
    if np.linalg.norm(delta) <= 1e-9:
        return float(fallback)
    return float(math.atan2(delta[1], delta[0]))
