"""Generalized Voronoi Diagram + Dang 2022 Voronoi field.

参考文献
--------
Dang, Ahn, Lee & Lee, "Improved Analytic Expansions in Hybrid A-Star
Path Planning for Non-Holonomic Robots," Applied Sciences 12(12), 5999, 2022.
DOI: 10.3390/app12125999

Eq.2:
    v(x, y) = (alpha / (alpha + d_o))
            * (d_v / (d_o + d_v))
            * ((d_o^max - d_o) / d_o^max)^2

其中:
    d_o(x, y) = 距最近障碍的欧氏距离 (米)
    d_v(x, y) = 距 GVD 最近边的欧氏距离 (米)
    d_o^max   = 影响半径阈值 (米)，d_o > d_o^max 时 v=0
    alpha     = 平滑参数 (>0)

特性 (Dang 2022 §2.1 行 71)
    - 障碍处 v -> 大 (高代价)
    - GVD 中线上 (d_v = 0) v = 0   ← 与 EDT 不同的关键
    - d_o > d_o^max 时 v = 0 (论文写法的副作用)

简化与近似
----------
1. GVD 在栅格地图上用 *medial axis* 近似——即 free 空间的中轴变换。
   对于多边形障碍的精确 GVD 而言这是栅格分辨率级近似，但与 Dang 2022
   的应用场景 (栅格占用图，1 m/cell 量级) 一致。
2. 不维护拓扑或 Voronoi 边对应关系，仅保留 d_v 距离场。
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import distance_transform_edt
from skimage.morphology import medial_axis

from ..map_utils import GridMap


# ============================================================
# GVD 提取 + d_v 距离场
# ============================================================

def _compute_gvd_distance(grid_map: GridMap) -> np.ndarray:
    """对 free 空间逐 cell 计算到 GVD 边的最近欧氏距离 (米)。

    实现
    ----
    1. 用 ``skimage.morphology.medial_axis`` 提取 free 空间中轴 (GVD 在
       栅格上的近似)。Why medial_axis 而非 skeletonize: medial_axis 保留
       中轴上每点到背景的距离 (与 GVD 等距点定义一致)，且不会过度剪枝
       分支；skeletonize 会把分支砍掉，丢失通道连接信息。
    2. 对中轴二值图取反，再做 ``distance_transform_edt`` —— 得到每个
       cell 到最近中轴像素的欧氏距离 (像素单位)，乘以 ``resolution``
       转为米。
    3. 障碍 cell 与无中轴的退化情况由 ``distance_transform_edt`` 自动
       处理 (无前景时返回 +inf)。
    """
    free_mask = grid_map.data == 0
    if not np.any(free_mask):
        h, w = grid_map.data.shape
        return np.full((h, w), np.inf, dtype=np.float32)

    # ── 1. medial_axis 提取 GVD ──
    skel = medial_axis(free_mask)

    # ── 2. 距 GVD 距离场 (像素 → 米) ──
    if not np.any(skel):
        # 退化：地图太小或无中轴 (例如全 free 单 cell)
        h, w = grid_map.data.shape
        return np.zeros((h, w), dtype=np.float32)

    # distance_transform_edt: 计算到 *零值像素* 的距离，所以传 ~skel
    dist_cells = distance_transform_edt(~skel)
    return (dist_cells * grid_map.resolution).astype(np.float32)


# ============================================================
# Dang 2022 Eq.2: v(x, y) 计算
# ============================================================

def compute_voronoi_field(
    grid_map: GridMap,
    alpha: float = 5.0,
    d_o_max: float = 5.0,
) -> np.ndarray:
    """Dang 2022 Eq.2 计算 Voronoi field v(x, y)。

    Parameters
    ----------
    grid_map
        占用栅格地图 (1=障碍, 0=自由)。
    alpha
        平滑参数 (>0)，控制 v 在 d_o 上的衰减率。论文未给具体值，
        典型值 5~10。
    d_o_max
        影响半径阈值 (米)，d_o > d_o_max 时 v = 0。

    Returns
    -------
    np.ndarray
        ``(H, W) float32`` Voronoi field。每个 free cell 的值满足:
            - 障碍处 (d_o = 0) v 大
            - GVD 中线 (d_v = 0) v = 0
            - d_o > d_o_max 处 v = 0
            - 单调衰减
    """
    if alpha <= 0:
        raise ValueError(f"alpha must be > 0, got {alpha}")
    if d_o_max <= 0:
        raise ValueError(f"d_o_max must be > 0, got {d_o_max}")

    # ── d_o: 距最近障碍距离 (米) ──
    free_mask = grid_map.data == 0
    d_o_cells = distance_transform_edt(free_mask)
    d_o = (d_o_cells * grid_map.resolution).astype(np.float32)

    # ── d_v: 距 GVD 距离 (米) ──
    d_v = _compute_gvd_distance(grid_map)

    # ── Eq.2 三因子 ──
    # 因子 A: alpha / (alpha + d_o)         → 障碍越近越大
    # 因子 B: d_v / (d_o + d_v)             → GVD 中线 (d_v=0) 处为 0
    # 因子 C: ((d_o_max - d_o) / d_o_max)^2 → d_o > d_o_max 时为 0 (clip)
    factor_a = alpha / (alpha + d_o)
    denom_b = d_o + d_v
    factor_b = np.where(denom_b > 1e-12, d_v / np.maximum(denom_b, 1e-12), 0.0)
    falloff = np.clip((d_o_max - d_o) / d_o_max, 0.0, 1.0)
    factor_c = falloff * falloff

    field = factor_a * factor_b * factor_c

    # ── 障碍 cell 强制为 0 (论文 Eq.2 仅在 free 上定义) ──
    field[~free_mask] = 0.0

    return field.astype(np.float32)


# ============================================================
# 世界坐标查询
# ============================================================

def query_voronoi_field(
    field: np.ndarray,
    grid_map: GridMap,
    x: float,
    y: float,
) -> float:
    """与 ``obstacle_field.query_distance`` 同签名。世界坐标 → field 值。

    越界返回 0.0 (无代价) — 与 ``query_distance`` 的"远离障碍"语义对齐:
    Voronoi field 在远离障碍时本就为 0，越界视为"安全"。
    """
    gx, gy = grid_map.world_to_grid(x, y)
    if not grid_map.in_bounds(gx, gy):
        return 0.0
    return float(field[gy, gx])


# ============================================================
# 路径平均场值 (用于 Dang 2022 Eq.3 的 v 项)
# ============================================================

def path_mean_voronoi(
    field: np.ndarray,
    grid_map: GridMap,
    poses,
) -> float:
    """沿一组位姿求平均 Voronoi field 值。

    参数
    ----
    field
        ``compute_voronoi_field`` 的输出。
    grid_map
        与 ``field`` 对应的栅格地图。
    poses
        可迭代位姿，元素须有 ``.x`` / ``.y`` 属性 (``AckermannState``)，
        或为 ``(x, y, ...)`` 元组。

    返回
    ----
    float
        路径上 v 的算术平均；空路径返回 0.0。
    """
    poses = list(poses)
    if not poses:
        return 0.0
    total = 0.0
    n = 0
    for p in poses:
        if hasattr(p, "x") and hasattr(p, "y"):
            x, y = p.x, p.y
        else:
            x, y = p[0], p[1]
        total += query_voronoi_field(field, grid_map, float(x), float(y))
        n += 1
    return total / max(n, 1)
