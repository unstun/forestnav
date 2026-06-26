"""两阶段走廊扩展（Lian 2023 设计 §3.1.2）。"""
from __future__ import annotations

import math
from typing import List, Sequence, Tuple

import numpy as np

from forest_n3p.baselines.lian2023_paper_from_scratch.types import CorridorSegment, GridSpec


# ============================================================
# 内部工具：路径重采样
# ============================================================

def _resample_path_with_arc(
    path_cells: Sequence[Tuple[int, int]],
    cell_size_m: float,
    step_m: float,
) -> List[Tuple[float, float, float, float]]:
    """沿路径以 step_m 等距重采样。

    参数
    ----
    path_cells  : (col, row) 格点序列
    cell_size_m : 每格物理尺寸 (m)
    step_m      : 重采样间距 (m)

    返回
    ----
    [(x_m, y_m, theta_rad, arc_s_m), ...]
    """
    if len(path_cells) < 2:
        return []

    # ---------- 格点 → 物理坐标 ----------
    pts_m = [(p[0] * cell_size_m, p[1] * cell_size_m) for p in path_cells]

    # ---------- 累积弧长 ----------
    cum = [0.0]
    for i in range(1, len(pts_m)):
        d = math.hypot(
            pts_m[i][0] - pts_m[i - 1][0],
            pts_m[i][1] - pts_m[i - 1][1],
        )
        cum.append(cum[-1] + d)

    total = cum[-1]
    if total <= 0:
        return []

    # ---------- 均匀采样 ----------
    out: List[Tuple[float, float, float, float]] = []
    n = max(2, int(total / step_m) + 1)
    for k in range(n):
        s = k * total / (n - 1) if n > 1 else 0.0
        s = min(s, total)   # 浮点溢出保护：k=n-1 时可能产生 total+ε，
                            # 导致搜索段失败、seg_i 默认取 0（首段），末端坐标/方向错误

        # 找所在折线段
        seg_i = 0
        for i in range(len(cum) - 1):
            if cum[i] <= s <= cum[i + 1]:
                seg_i = i
                break

        seg_len = cum[seg_i + 1] - cum[seg_i]
        t = (s - cum[seg_i]) / seg_len if seg_len > 1e-9 else 0.0

        x = pts_m[seg_i][0] + t * (pts_m[seg_i + 1][0] - pts_m[seg_i][0])
        y = pts_m[seg_i][1] + t * (pts_m[seg_i + 1][1] - pts_m[seg_i][1])

        dx = pts_m[seg_i + 1][0] - pts_m[seg_i][0]
        dy = pts_m[seg_i + 1][1] - pts_m[seg_i][1]
        theta = math.atan2(dy, dx)

        out.append((x, y, theta, s))

    return out


# ============================================================
# 内部工具：单侧横向净空
# ============================================================

def _max_lateral_clearance(
    grid: np.ndarray,
    cell_size_m: float,
    x_m: float,
    y_m: float,
    nx: float,
    ny: float,
    step_m: float,
    l_max_m: float,
) -> float:
    """从 (x_m, y_m) 沿 (nx, ny) 单位方向步进，返回首次碰障前的距离。

    - OOB（越出地图边界）立即终止，返回当前距离。
    - 精度为 step_m（Lian 2023 精扩阶段用 dl2_m=0.1m）。
    """
    H, W = grid.shape
    d = 0.0
    while d < l_max_m:
        d_test = d + step_m
        tx = x_m + d_test * nx
        ty = y_m + d_test * ny

        # ---------- 物理坐标 → 格点索引 ----------
        cx = int(tx / cell_size_m)
        cy = int(ty / cell_size_m)

        # 越界 → 停止
        if not (0 <= cx < W and 0 <= cy < H):
            return d

        # 碰障 → 停止
        if grid[cy, cx] != 0:
            return d

        d = d_test

    return l_max_m


# ============================================================
# 公开接口
# ============================================================

def build_corridor(
    *,
    grid_map: GridSpec,
    path_cells: Sequence[Tuple[int, int]],
    dl1_m: float = 1.0,
    dl2_m: float = 0.1,
    l_max_m: float = 8.0,
) -> List[CorridorSegment]:
    """两阶段走廊构建：粗扩 dl1_m 间距采样 + 精扩 dl2_m 步长测距。

    算法（Lian 2023 §3.1.2）
    -----------------------
    1. 以 dl1_m 沿路径等距重采样，得到一组方向向量。
    2. 每个采样点上，向左右各沿垂直方向以 dl2_m 步长步进，
       直至碰障或超出 l_max_m，得到左/右净空距离。
    3. 记录 arc_length_m（到下一采样点的弧长差）。

    参数
    ----
    grid_map   : 占据栅格（GridMap.data 存储障碍，1 = 占据）
    path_cells : (col, row) 格点序列
    dl1_m      : 粗扩采样间距 (m)，默认 1m
    dl2_m      : 精扩步长 (m)，默认 0.1m
    l_max_m    : 走廊最大半宽 (m)，默认 8m

    返回
    ----
    CorridorSegment 列表（每段对应一个采样点）
    """
    cell_size = float(grid_map.resolution)
    grid = grid_map.data

    samples = _resample_path_with_arc(path_cells, cell_size, dl1_m)
    if len(samples) < 2:
        return []

    segs: List[CorridorSegment] = []
    for i, (x, y, theta, s) in enumerate(samples):
        # ---------- 切向单位向量 → 法向量（左/右） ----------
        dxu = math.cos(theta)
        dyu = math.sin(theta)
        nx_l, ny_l = -dyu,  dxu   # 左法向（CCW 旋转 90°）
        nx_r, ny_r =  dyu, -dxu   # 右法向（CW 旋转 90°）

        # ---------- 精扩：测量左右净空 ----------
        left  = _max_lateral_clearance(grid, cell_size, x, y, nx_l, ny_l, dl2_m, l_max_m)
        right = _max_lateral_clearance(grid, cell_size, x, y, nx_r, ny_r, dl2_m, l_max_m)

        # ---------- 弧长差（最后一段为 0） ----------
        arc = samples[i + 1][3] - s if i + 1 < len(samples) else 0.0

        segs.append(CorridorSegment(
            s_xy=(x, y),
            d_unit=(dxu, dyu),
            left_m=float(left),
            right_m=float(right),
            arc_length_m=float(arc),
        ))

    return segs


def is_corridor_degenerate(
    segs: Sequence[CorridorSegment],
    *,
    footprint_diameter_m: float,
) -> bool:
    """任一段总宽 (left + right) < footprint 直径 → 退化走廊。

    退化条件：机器人在该段无法横向通过（宽度不足车身直径）。
    """
    for s in segs:
        if (s.left_m + s.right_m) < footprint_diameter_m:
            return True
    return False
