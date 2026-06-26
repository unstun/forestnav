"""Lian 2023 原文版 EHA* 第一阶段。

该模块对应 Algorithm 1 的第一阶段：

1. CreateDilatedMap + SearchAStarPath
2. GenerateFirstStageCor + GenerateSecondStageCor
3. JudgeNode + IntegrateWideNarrowPath
4. ExtractBoundaryPointsOfEachPath + CorrectBoundaryPoints
5. SetInitialOrientationAngle
6. SearchHybridAStarEachAdjacentNode

车辆几何、Ackermann 运动学和碰撞检测沿用本项目 UGV 模型。
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Tuple

from forest_n3p.baselines.common import PlannerResult, default_start_theta
from forest_n3p.baselines.lian2023.astar_2d import astar_2d_path
from forest_n3p.baselines.lian2023.corridor import build_corridor
from forest_n3p.baselines.lian2023.types import BoundaryPoint, CorridorSegment
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    AckermannState,
    GridMap,
    HybridAStarPlanner,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.primitives import default_primitives


PathXYTheta = List[Tuple[float, float, float]]


@dataclass(frozen=True)
class Passage:
    """Algorithm 1 中的 wide/narrow 连续节点段。"""

    kind: str
    start_index: int
    end_index: int

    @property
    def n_boxes(self) -> int:
        return self.end_index - self.start_index + 1


def classify_passages(
    corridor: Sequence[CorridorSegment],
    *,
    l_thre_m: float,
) -> List[Passage]:
    """按 Lian 2023 JudgeNode 规则把 corridor 节点分成 wide/narrow passage。

    原文 T2 记录 box 的四个边长，并用最小边长与 ``Lthre`` 比较。当前项目
    corridor 是局部有向条带，使用左右净空的较小值作为等价宽度判据。
    """
    if not corridor:
        return []

    def _kind(seg: CorridorSegment) -> str:
        side = min(float(seg.left_m), float(seg.right_m))
        return "wide" if side >= float(l_thre_m) else "narrow"

    out: List[Passage] = []
    start = 0
    cur = _kind(corridor[0])
    for i in range(1, len(corridor)):
        nxt = _kind(corridor[i])
        if nxt == cur:
            continue
        out.append(Passage(kind=cur, start_index=start, end_index=i - 1))
        start = i
        cur = nxt
    out.append(Passage(kind=cur, start_index=start, end_index=len(corridor) - 1))
    return out


def extract_paper_boundary_points(
    *,
    corridor: Sequence[CorridorSegment],
    start_xy_theta: Tuple[float, float, float],
    goal_xy_theta: Tuple[float, float, float],
    l_thre_m: float = 5.0,
    lp_thre_boxes: int = 0,
    n_max: Optional[int] = None,
) -> List[BoundaryPoint]:
    """按 Algorithm 1 lines 31-34 从 wide/narrow passage 提取边界点。

    ``lp_thre_boxes`` 对应原文 CorrectBoundaryPoints 中的 ``LPthre``：当某个
    passage 的 box 数少于该阈值，删除该 passage 的左边界点，减少过密切分。
    """
    sx, sy, sth = start_xy_theta
    gx, gy, gth = goal_xy_theta
    if not corridor:
        return [
            BoundaryPoint(float(sx), float(sy), float(sth), 0.0),
            BoundaryPoint(float(gx), float(gy), float(gth), 0.0),
        ]

    passages = classify_passages(corridor, l_thre_m=float(l_thre_m))
    raw_indices = [0]
    raw_indices.extend(p.end_index for p in passages)
    raw_indices[-1] = len(corridor) - 1

    remove_positions: set[int] = set()
    if int(lp_thre_boxes) > 0:
        for passage_i, passage in enumerate(passages):
            if passage.n_boxes >= int(lp_thre_boxes):
                continue
            # raw_indices[passage_i] 是该 passage 的左边界。
            if 0 < passage_i < len(raw_indices) - 1:
                remove_positions.add(passage_i)

    indices: List[int] = []
    for pos, idx in enumerate(raw_indices):
        if pos in remove_positions:
            continue
        if not indices or idx != indices[-1]:
            indices.append(idx)

    if n_max is not None and int(n_max) >= 2 and len(indices) > int(n_max):
        indices = _thin_indices(indices, int(n_max))

    arc_starts = _corridor_arc_starts(corridor)
    bps: List[BoundaryPoint] = []
    for out_i, idx in enumerate(indices):
        idx = max(0, min(idx, len(corridor) - 1))
        if out_i == 0:
            bps.append(BoundaryPoint(float(sx), float(sy), float(sth), 0.0))
            continue
        if out_i == len(indices) - 1:
            bps.append(
                BoundaryPoint(
                    float(gx),
                    float(gy),
                    float(gth),
                    float(arc_starts[-1] + corridor[-1].arc_length_m),
                )
            )
            continue
        seg = corridor[idx]
        theta = math.atan2(float(seg.d_unit[1]), float(seg.d_unit[0]))
        bps.append(
            BoundaryPoint(
                float(seg.s_xy[0]),
                float(seg.s_xy[1]),
                float(theta),
                float(arc_starts[idx]),
            )
        )
    return bps


def plan_lian2023_eha_paper(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start_xy: Tuple[int, int],
    goal_xy: Tuple[int, int],
    goal_theta_rad: float = 0.0,
    start_theta_rad: Optional[float] = None,
    goal_xy_tol_m: float = 0.5,
    goal_theta_tol_rad: float = math.pi,
    timeout_s: float = 30.0,
    max_nodes: int = 200_000,
    collision_padding: Optional[float] = None,
    collision_checker: Any = None,
    dl1_m: float = 1.0,
    dl2_m: float = 0.1,
    l_max_m: float = 8.0,
    l_thre_m: float = 5.0,
    lp_thre_boxes: int = 0,
    n_max: Optional[int] = 10,
    step_length: float = 0.3,
) -> PlannerResult:
    """运行 Lian 2023 原文版 EHA* 第一阶段，返回 plan-only 路径。

    返回的 ``path_xy_cells`` 使用 benchmark 统一的 cell 坐标；``stats`` 中保留
    ``path_states`` 供需要姿态序列的调用方使用。
    """
    t0 = time.perf_counter()
    cell = float(grid_map.resolution)
    start_theta = (
        float(start_theta_rad)
        if start_theta_rad is not None
        else default_start_theta(start_xy, goal_xy, cell_size_m=cell)
    )
    stats: dict[str, Any] = {
        "paper_eha_l_thre_m": float(l_thre_m),
        "paper_eha_lp_thre_boxes": int(lp_thre_boxes),
    }

    rd_m = _dilation_radius_m(footprint)
    padding_cells = max(1, int(math.ceil(rd_m / max(cell, 1e-9))))
    path_cells = astar_2d_path(
        grid_map=grid_map,
        start_cell=(int(start_xy[0]), int(start_xy[1])),
        goal_cell=(int(goal_xy[0]), int(goal_xy[1])),
        padding_cells=padding_cells,
    )
    stats["paper_eha_dilation_radius_m"] = float(rd_m)
    stats["paper_eha_padding_cells"] = int(padding_cells)
    stats["t_astar2d_s"] = time.perf_counter() - t0
    if path_cells is None:
        return _failure(start_xy, time.perf_counter() - t0, stats, "astar2d_fail")

    t1 = time.perf_counter()
    corridor = build_corridor(
        grid_map=grid_map,
        path_cells=path_cells,
        dl1_m=float(dl1_m),
        dl2_m=float(dl2_m),
        l_max_m=float(l_max_m),
    )
    stats["t_corridor_s"] = time.perf_counter() - t1
    stats["paper_eha_corridor_nodes"] = len(corridor)
    if not corridor:
        return _failure(start_xy, time.perf_counter() - t0, stats, "corridor_empty")

    passages = classify_passages(corridor, l_thre_m=float(l_thre_m))
    stats["paper_eha_passages"] = len(passages)
    stats["paper_eha_wide_passages"] = sum(1 for p in passages if p.kind == "wide")
    stats["paper_eha_narrow_passages"] = sum(1 for p in passages if p.kind == "narrow")

    bps = extract_paper_boundary_points(
        corridor=corridor,
        start_xy_theta=(start_xy[0] * cell, start_xy[1] * cell, start_theta),
        goal_xy_theta=(goal_xy[0] * cell, goal_xy[1] * cell, float(goal_theta_rad)),
        l_thre_m=float(l_thre_m),
        lp_thre_boxes=int(lp_thre_boxes),
        n_max=n_max,
    )
    stats["paper_eha_boundary_points"] = len(bps)
    stats["paper_eha_boundary_xy"] = [(bp.x, bp.y) for bp in bps]
    if len(bps) < 2:
        return _failure(start_xy, time.perf_counter() - t0, stats, "boundary_points_empty")

    t2 = time.perf_counter()
    status, path_states, seg_stats = run_classic_hybrid_astar_between_boundary_points(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        boundary_points=bps,
        timeout_s=max(0.1, float(timeout_s) - (time.perf_counter() - t0)),
        max_nodes=int(max_nodes),
        collision_padding=collision_padding,
        collision_checker=collision_checker,
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
        step_length=float(step_length),
    )
    stats.update(seg_stats)
    stats["t_eha_s"] = time.perf_counter() - t2
    stats["time"] = time.perf_counter() - t0
    if status != "success":
        return _failure(start_xy, stats["time"], stats, status)

    path_xy_cells = [(x / cell, y / cell) for x, y, _th in path_states]
    stats["path_states"] = path_states
    return PlannerResult(
        path_xy_cells=path_xy_cells,
        time_s=float(stats["time"]),
        success=True,
        stats=stats,
    )


def run_classic_hybrid_astar_between_boundary_points(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    boundary_points: Sequence[BoundaryPoint],
    timeout_s: float,
    max_nodes: int,
    collision_padding: Optional[float],
    collision_checker: Any,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    step_length: float,
) -> Tuple[str, PathXYTheta, dict[str, Any]]:
    """对相邻 boundary point 运行 classic Hybrid A* 并拼接。"""
    if len(boundary_points) < 2:
        return "boundary_points_empty", [], {}

    deadline = time.perf_counter() + max(0.0, float(timeout_s))
    all_states: PathXYTheta = []
    segment_failures: list[str] = []

    for i in range(len(boundary_points) - 1):
        remain = deadline - time.perf_counter()
        if remain <= 0:
            return "timeout", [], {
                "paper_eha_segments_done": i,
                "paper_eha_segment_failures": segment_failures,
            }
        a = boundary_points[i]
        b = boundary_points[i + 1]
        states, stats = _plan_classic_segment(
            grid_map=grid_map,
            footprint=footprint,
            params=params,
            start=(a.x, a.y, a.theta),
            goal=(b.x, b.y, b.theta),
            timeout_s=remain,
            max_nodes=int(max_nodes),
            collision_padding=collision_padding,
            collision_checker=collision_checker,
            goal_xy_tol_m=float(goal_xy_tol_m),
            goal_theta_tol_rad=float(goal_theta_tol_rad),
            step_length=float(step_length),
        )
        if not states:
            reason = str(stats.get("failure_reason", "segment_fail"))
            segment_failures.append(f"{i}:{reason}")
            return "segment_fail", [], {
                "paper_eha_segments_done": i,
                "paper_eha_segment_failures": segment_failures,
            }
        if not all_states:
            all_states.extend(states)
        else:
            all_states.extend(states[1:])

    return "success", all_states, {
        "paper_eha_segments_done": max(0, len(boundary_points) - 1),
        "paper_eha_segment_failures": segment_failures,
    }


def _plan_classic_segment(
    *,
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    start: Tuple[float, float, float],
    goal: Tuple[float, float, float],
    timeout_s: float,
    max_nodes: int,
    collision_padding: Optional[float],
    collision_checker: Any,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    step_length: float,
) -> Tuple[PathXYTheta, dict[str, Any]]:
    """Classic Hybrid A* 段规划；关闭 Dang 2022 多曲率扫描。"""
    planner = HybridAStarPlanner(
        grid_map,
        footprint,
        params,
        primitives=default_primitives(params, step_length=float(step_length)),
        goal_xy_tol=float(goal_xy_tol_m),
        goal_theta_tol=float(goal_theta_tol_rad),
        collision_padding=collision_padding,
        collision_checker=collision_checker,
        curvature_step=0.0,
        max_curvature_ratio=1.0,
        sigma1=0.0,
        sigma2=1.0,
    )
    path, stats = planner.plan(
        AckermannState(float(start[0]), float(start[1]), float(start[2])),
        AckermannState(float(goal[0]), float(goal[1]), float(goal[2])),
        timeout=float(timeout_s),
        max_nodes=int(max_nodes),
        self_check=False,
    )
    stats = dict(stats)
    stats["classic_hybrid_astar"] = True
    if not path:
        return [], stats
    trace = stats.get("trace_poses")
    if trace and len(trace) >= 2:
        return [(float(x), float(y), float(th)) for x, y, th in trace], stats
    return [(float(s.x), float(s.y), float(s.theta)) for s in path], stats


def _corridor_arc_starts(corridor: Sequence[CorridorSegment]) -> List[float]:
    arc = [0.0]
    for seg in corridor[:-1]:
        arc.append(arc[-1] + float(seg.arc_length_m))
    return arc


def _thin_indices(indices: Sequence[int], n_max: int) -> List[int]:
    if len(indices) <= n_max:
        return list(indices)
    out = []
    for k in range(n_max):
        pos = round(k * (len(indices) - 1) / (n_max - 1))
        out.append(indices[int(pos)])
    compact: List[int] = []
    for idx in out:
        if not compact or compact[-1] != idx:
            compact.append(idx)
    return compact


def _dilation_radius_m(footprint: OrientedBoxFootprint | TwoCircleFootprint) -> float:
    if isinstance(footprint, TwoCircleFootprint):
        return float(footprint.radius)
    return math.hypot(float(footprint.half_length), float(footprint.half_width))


def _failure(
    start_xy: Tuple[int, int],
    time_s: float,
    stats: dict[str, Any],
    reason: str,
) -> PlannerResult:
    out = dict(stats)
    out["time"] = float(time_s)
    out["failure_reason"] = str(reason)
    return PlannerResult(
        path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
        time_s=float(time_s),
        success=False,
        stats=out,
    )
