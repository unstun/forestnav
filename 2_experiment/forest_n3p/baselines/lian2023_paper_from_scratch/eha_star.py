"""EHA*：BP 间包内 HA* + 拼接（Lian 2023 设计 §3.1.4 / §3.1.5）。

接口
----
run_eha_star(...)         对相邻 BP 调用本目录内 HA* segment solver，拼接 segment
resample_path_to_n_points 将拼接路径线性插值重采样到固定 n_points 个点

path_states 来源
----------------
本目录内使用自行实现的 bicycle-model segment 搜索器，不调用其他 baseline。
"""
from __future__ import annotations

# ===========================================================================
# 标准库
# ===========================================================================
import math
from typing import List, Sequence, Tuple

# ===========================================================================
# 内部依赖
# ===========================================================================
from forest_n3p.baselines.lian2023_paper_from_scratch.hybrid_astar import plan_segment
from forest_n3p.baselines.lian2023_paper_from_scratch.types import (
    BoundaryPoint,
    GridSpec,
    PlanStatus,
    VehicleDiscs,
    VehicleParams,
)

# ---------------------------------------------------------------------------
# 类型别名
# ---------------------------------------------------------------------------
PathXYTheta = List[Tuple[float, float, float]]


# ===========================================================================
# 公开接口
# ===========================================================================

def run_eha_star(
    *,
    grid_map: GridSpec,
    discs: VehicleDiscs,
    params: VehicleParams,
    boundary_points: Sequence[BoundaryPoint],
    per_segment_timeout_s: float = 2.0,
    goal_xy_tol_m: float = 0.2,
    goal_theta_tol_rad: float = 0.15,
) -> Tuple[PlanStatus, PathXYTheta]:
    """对相邻 BP 调用本目录内 HA* segment solver，拼接所有 segment。

    Parameters
    ----------
    grid_map:
        占据格栅地图，resolution 字段单位 m/cell。
    discs:
        多圆车体覆盖。
    params:
        Ackermann 运动学参数。
    boundary_points:
        走廊 BP 序列，至少 2 个；相邻两点构成一个 HA* segment。
        坐标单位：世界坐标 m（非 cell 索引）。
    per_segment_timeout_s:
        每个 segment 的 HA* 超时阈值（s）。
    goal_xy_tol_m:
        到达目标 XY 容忍半径（m），传给本目录内 segment solver。
    goal_theta_tol_rad:
        到达目标朝向容忍（rad）。

    Returns
    -------
    (PlanStatus, PathXYTheta)
        成功：(SUCCESS, [(x_m, y_m, theta_rad), ...])
        任一 segment 失败：(STAGE1_EHA_FAIL, [])
    """
    if len(boundary_points) < 2:
        return PlanStatus.STAGE1_EHA_FAIL, []

    cell = float(grid_map.resolution)   # m/cell
    full_path: PathXYTheta = []

    for i in range(len(boundary_points) - 1):
        a = boundary_points[i]
        b = boundary_points[i + 1]

        # ------------------------------------------------------------------
        # BP 世界坐标(m) → classic Hybrid A* segment
        # ------------------------------------------------------------------
        states = _plan_classic_segment(
            grid_map=grid_map,
            discs=discs,
            params=params,
            start=(a.x, a.y, a.theta),
            goal=(b.x, b.y, b.theta),
            start_theta_rad=a.theta,
            goal_theta_rad=b.theta,
            goal_xy_tol_m=goal_xy_tol_m,
            goal_theta_tol_rad=goal_theta_tol_rad,
            timeout_s=per_segment_timeout_s,
        )

        # ------------------------------------------------------------------
        # segment 失败 → 立即返回，不继续后续段
        # ------------------------------------------------------------------
        if not states:
            return PlanStatus.STAGE1_EHA_FAIL, []

        # ------------------------------------------------------------------
        # 拼接：首段保留起点，后续段跳过第一点（与前段末点重复）
        # ------------------------------------------------------------------
        if i == 0:
            full_path.extend(states)
        else:
            full_path.extend(states[1:])

    return PlanStatus.SUCCESS, full_path


def _plan_classic_segment(
    *,
    grid_map: GridSpec,
    discs: VehicleDiscs,
    params: VehicleParams,
    start: tuple[float, float, float],
    goal: tuple[float, float, float],
    start_theta_rad: float,
    goal_theta_rad: float,
    goal_xy_tol_m: float,
    goal_theta_tol_rad: float,
    timeout_s: float,
) -> PathXYTheta:
    """包内 bicycle-model segment search used inside Lian 2023 EHA*."""
    _ = start_theta_rad, goal_theta_rad
    return plan_segment(
        grid=grid_map,
        params=params,
        discs=discs,
        start=(float(start[0]), float(start[1]), float(start[2])),
        goal=(float(goal[0]), float(goal[1]), float(goal[2])),
        goal_xy_tol_m=float(goal_xy_tol_m),
        goal_theta_tol_rad=float(goal_theta_tol_rad),
        timeout_s=float(timeout_s),
        max_nodes=200_000,
    )


def resample_path_to_n_points(
    path: PathXYTheta,
    n_points: int,
) -> PathXYTheta:
    """将 EHA* 拼接路径线性插值重采样到固定 n_points 个点。

    Parameters
    ----------
    path:
        输入路径，[(x_m, y_m, theta_rad), ...]，至少 1 个点。
    n_points:
        目标点数，≥1。

    Returns
    -------
    PathXYTheta，长度恰好为 n_points；theta 用最近分段端点值（离散最近邻插值）。
    """
    if len(path) < 2:
        # 长度契约：返回必须是 n_points 个点（NLP 等下游依赖固定长度）
        if not path:
            return []
        return [path[0]] * n_points

    # ------------------------------------------------------------------
    # 累积弧长
    # ------------------------------------------------------------------
    cum = [0.0]
    for i in range(1, len(path)):
        d = math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
        cum.append(cum[-1] + d)
    total = cum[-1]

    if total <= 0:
        return [path[0]] * n_points

    # ------------------------------------------------------------------
    # 等间距重采样
    # ------------------------------------------------------------------
    out: PathXYTheta = []
    for k in range(n_points):
        s = k * total / (n_points - 1) if n_points > 1 else 0.0
        s = min(s, total)   # 浮点溢出保护

        # 找当前弧长所在分段
        seg_i = 0
        for idx in range(len(cum) - 1):
            if cum[idx] <= s <= cum[idx + 1]:
                seg_i = idx
                break

        seg_len = cum[seg_i + 1] - cum[seg_i]
        t = (s - cum[seg_i]) / seg_len if seg_len > 1e-9 else 0.0

        x = path[seg_i][0] + t * (path[seg_i + 1][0] - path[seg_i][0])
        y = path[seg_i][1] + t * (path[seg_i + 1][1] - path[seg_i][1])
        # theta 取最近端点（离散最近邻，避免角度线性插值的 ±π 跳变问题）
        theta = path[seg_i][2] if t < 0.5 else path[seg_i + 1][2]
        out.append((x, y, theta))

    return out


# ===========================================================================
# 内部工具
# ===========================================================================

def _cells_to_xytheta(
    cells: Sequence[Tuple[float, float]],
    cell_size_m: float,
    start_theta: float,
    goal_theta: float,
) -> PathXYTheta:
    """fallback：cell (x, y) 序列 → (x_m, y_m, theta_rad)，theta 用相邻点切向估算。

    精度低于 path_states 方案，但在规划器不返回 path_states 时提供不阻塞的降级。
    端点 theta 使用调用方传入的 start_theta / goal_theta 以保证一致性。
    """
    pts = [(c[0] * cell_size_m, c[1] * cell_size_m) for c in cells]
    out: PathXYTheta = []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            theta = start_theta
        elif i == len(pts) - 1:
            theta = goal_theta
        else:
            dx = pts[i + 1][0] - pts[i - 1][0]
            dy = pts[i + 1][1] - pts[i - 1][1]
            theta = math.atan2(dy, dx)
        out.append((x, y, theta))
    return out
