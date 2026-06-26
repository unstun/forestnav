"""EHA*：BP 间 HA* + 拼接（Lian 2023 设计 §3.1.4 / §3.1.5）。

接口
----
run_eha_star(...)         对相邻 BP 调用 plan_hybrid_astar，拼接所有 segment
resample_path_to_n_points 将拼接路径线性插值重采样到固定 n_points 个点

path_states 来源
----------------
优先使用 improved_hybrid_astar 在 result.stats['path_states'] 中暴露的
(x_m, y_m, theta_rad) 密集轨迹（方案 a），该字段由 trace_poses 直接
得到，theta 由规划器内部圆弧积分精确给出，无需后估。
若该字段缺失（旧版规划器、单点 fallback），则退化为
_cells_to_xytheta 用相邻差分估算 theta（方案 b，精度稍低但不阻塞流程）。
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
from forest_n3p.baselines.improved_hybrid_astar import plan_hybrid_astar
from forest_n3p.baselines.lian2023.types import BoundaryPoint, PlanStatus
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
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
    grid_map: GridMap,
    footprint: OrientedBoxFootprint | TwoCircleFootprint,
    params: AckermannParams,
    boundary_points: Sequence[BoundaryPoint],
    per_segment_timeout_s: float = 2.0,
    goal_xy_tol_m: float = 0.2,
    goal_theta_tol_rad: float = 0.15,
) -> Tuple[PlanStatus, PathXYTheta]:
    """对相邻 BP 调用 plan_hybrid_astar，拼接所有 segment。

    Parameters
    ----------
    grid_map:
        占据格栅地图，resolution 字段单位 m/cell。
    footprint:
        车辆碰撞足迹。
    params:
        Ackermann 运动学参数。
    boundary_points:
        走廊 BP 序列，至少 2 个；相邻两点构成一个 HA* segment。
        坐标单位：世界坐标 m（非 cell 索引）。
    per_segment_timeout_s:
        每个 segment 的 HA* 超时阈值（s）。
    goal_xy_tol_m:
        到达目标 XY 容忍半径（m），传给 plan_hybrid_astar。
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
        # BP 世界坐标(m) → cell 索引（plan_hybrid_astar 使用 cell 单位）
        # ------------------------------------------------------------------
        sxc = int(round(a.x / cell))
        syc = int(round(a.y / cell))
        gxc = int(round(b.x / cell))
        gyc = int(round(b.y / cell))

        result = plan_hybrid_astar(
            grid_map=grid_map,
            footprint=footprint,
            params=params,
            start_xy=(sxc, syc),
            goal_xy=(gxc, gyc),
            start_theta_rad=a.theta,
            goal_theta_rad=b.theta,
            goal_xy_tol_m=goal_xy_tol_m,
            goal_theta_tol_rad=goal_theta_tol_rad,
            timeout_s=per_segment_timeout_s,
        )

        # ------------------------------------------------------------------
        # segment 失败 → 立即返回，不继续后续段
        # ------------------------------------------------------------------
        if not result.success or len(result.path_xy_cells) == 0:
            return PlanStatus.STAGE1_EHA_FAIL, []

        # ------------------------------------------------------------------
        # 提取 (x_m, y_m, theta_rad) 序列
        # 优先方案(a): stats['path_states'] 由规划器精确圆弧积分给出
        # 退化方案(b): 若 path_states 缺失，用 cells 差分估算 theta
        # ------------------------------------------------------------------
        states: PathXYTheta = result.stats.get("path_states")  # type: ignore[assignment]
        if not states:
            states = _cells_to_xytheta(result.path_xy_cells, cell, a.theta, b.theta)

        # ------------------------------------------------------------------
        # 拼接：首段保留起点，后续段跳过第一点（与前段末点重复）
        # ------------------------------------------------------------------
        if i == 0:
            full_path.extend(states)
        else:
            full_path.extend(states[1:])

    return PlanStatus.SUCCESS, full_path


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
