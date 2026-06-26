"""IPOPT NLP 求解（Lian 2023 设计 §3.2）。

变量布局：
  flat[0 : 5*(N+1)]              = 状态序列 z (按 (k, dim) → k * 5 + dim)
  flat[5*(N+1) : 5*(N+1) + 2*N]  = 控制序列 u (按 (k, dim) → 5*(N+1) + k*2 + dim)

状态维度: (px, py, theta, v, delta)
控制维度: (a, omega = δ̇)

注：此文件将在 Task 4.2-4.4 逐步增补 dynamics / corridor / IPOPT solve。
本 Task 4.1 仅实现 NlpVarLayout + flatten/unflatten + variable_bounds。
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence, Tuple

import numpy as np

from forest_n3p.baselines.lian2023.types import CorridorSegment


STATE_DIM = 5
CONTROL_DIM = 2


@dataclass(frozen=True)
class NlpVarLayout:
    """决策变量在 flat 向量中的布局。"""

    n_steps: int   # N: 控制步数；状态共 N+1 个

    @property
    def state_dim(self) -> int:
        return STATE_DIM

    @property
    def control_dim(self) -> int:
        return CONTROL_DIM

    @property
    def n_states(self) -> int:
        return self.n_steps + 1

    @property
    def state_offset(self) -> int:
        return 0

    @property
    def control_offset(self) -> int:
        return STATE_DIM * self.n_states

    @property
    def n_vars(self) -> int:
        return STATE_DIM * self.n_states + CONTROL_DIM * self.n_steps

    def state_index(self, k: int, dim: int) -> int:
        return self.state_offset + k * STATE_DIM + dim

    def control_index(self, k: int, dim: int) -> int:
        return self.control_offset + k * CONTROL_DIM + dim

    def state_indices_of(self, dim: int) -> np.ndarray:
        return np.array(
            [self.state_index(k, dim) for k in range(self.n_states)],
            dtype=np.int64,
        )

    def control_indices_of(self, dim: int) -> np.ndarray:
        return np.array(
            [self.control_index(k, dim) for k in range(self.n_steps)],
            dtype=np.int64,
        )

    def variable_bounds(
        self,
        *,
        v_max: float,
        delta_max: float,
        a_max: float,
        omega_max: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        lb = np.full((self.n_vars,), -1e20, dtype=np.float64)
        ub = np.full((self.n_vars,), +1e20, dtype=np.float64)
        # v
        idx = self.state_indices_of(3)
        lb[idx], ub[idx] = -v_max, v_max
        # delta
        idx = self.state_indices_of(4)
        lb[idx], ub[idx] = -delta_max, delta_max
        # a
        idx = self.control_indices_of(0)
        lb[idx], ub[idx] = -a_max, a_max
        # omega
        idx = self.control_indices_of(1)
        lb[idx], ub[idx] = -omega_max, omega_max
        return lb, ub


def flatten_initial_guess(
    z: np.ndarray,
    u: np.ndarray,
    layout: NlpVarLayout,
) -> np.ndarray:
    """将 (N+1, 5) 状态 + (N, 2) 控制摊平为 flat 向量。"""
    if z.shape != (layout.n_states, STATE_DIM):
        raise ValueError(f"z shape {z.shape} != ({layout.n_states}, {STATE_DIM})")
    if u.shape != (layout.n_steps, CONTROL_DIM):
        raise ValueError(f"u shape {u.shape} != ({layout.n_steps}, {CONTROL_DIM})")
    flat = np.zeros((layout.n_vars,), dtype=np.float64)
    flat[layout.state_offset : layout.state_offset + STATE_DIM * layout.n_states] = z.reshape(-1)
    flat[layout.control_offset : layout.control_offset + CONTROL_DIM * layout.n_steps] = u.reshape(-1)
    return flat


def unflatten_solution(
    flat: np.ndarray,
    layout: NlpVarLayout,
) -> Tuple[np.ndarray, np.ndarray]:
    """反向：flat → (z, u)。"""
    z = flat[layout.state_offset : layout.state_offset + STATE_DIM * layout.n_states].reshape(layout.n_states, STATE_DIM)
    u = flat[layout.control_offset : layout.control_offset + CONTROL_DIM * layout.n_steps].reshape(layout.n_states - 1, CONTROL_DIM)
    return z, u


def dynamics_residual(
    flat: np.ndarray,
    layout: NlpVarLayout,
    *,
    dt: float,
    wheelbase_m: float,
) -> np.ndarray:
    """计算动力学等式残差，长度 = 5N。"""
    z, u = unflatten_solution(flat, layout)
    N = layout.n_steps
    L = float(wheelbase_m)
    res = np.zeros((5 * N,), dtype=np.float64)
    for k in range(N):
        zk = z[k]
        zk1 = z[k + 1]
        ak, omk = u[k, 0], u[k, 1]
        # 5 个等式
        res[5 * k + 0] = zk1[0] - zk[0] - dt * zk[3] * np.cos(zk[2])
        res[5 * k + 1] = zk1[1] - zk[1] - dt * zk[3] * np.sin(zk[2])
        res[5 * k + 2] = zk1[2] - zk[2] - dt * zk[3] * np.tan(zk[4]) / L
        res[5 * k + 3] = zk1[3] - zk[3] - dt * ak
        res[5 * k + 4] = zk1[4] - zk[4] - dt * omk
    return res


def dynamics_jacobian(
    flat: np.ndarray,
    layout: NlpVarLayout,
    *,
    dt: float,
    wheelbase_m: float,
) -> np.ndarray:
    """解析 Jacobian (5N × n_vars)，密集形式（小问题可用；大 N 应转 sparse）。"""
    z, _u = unflatten_solution(flat, layout)
    N = layout.n_steps
    L = float(wheelbase_m)
    J = np.zeros((5 * N, layout.n_vars), dtype=np.float64)
    for k in range(N):
        idx_zk = layout.state_offset + k * STATE_DIM
        idx_zk1 = layout.state_offset + (k + 1) * STATE_DIM
        idx_uk = layout.control_offset + k * CONTROL_DIM
        v_k = z[k, 3]
        th_k = z[k, 2]
        de_k = z[k, 4]
        # eq 0: px_{k+1} - px_k - dt*v_k*cos(th_k)
        J[5 * k + 0, idx_zk + 0] = -1.0
        J[5 * k + 0, idx_zk + 2] = +dt * v_k * np.sin(th_k)
        J[5 * k + 0, idx_zk + 3] = -dt * np.cos(th_k)
        J[5 * k + 0, idx_zk1 + 0] = +1.0
        # eq 1: py_{k+1} - py_k - dt*v_k*sin(th_k)
        J[5 * k + 1, idx_zk + 1] = -1.0
        J[5 * k + 1, idx_zk + 2] = -dt * v_k * np.cos(th_k)
        J[5 * k + 1, idx_zk + 3] = -dt * np.sin(th_k)
        J[5 * k + 1, idx_zk1 + 1] = +1.0
        # eq 2: theta_{k+1} - theta_k - dt*v_k*tan(de_k)/L
        sec2 = 1.0 / (np.cos(de_k) ** 2)
        J[5 * k + 2, idx_zk + 2] = -1.0
        J[5 * k + 2, idx_zk + 3] = -dt * np.tan(de_k) / L
        J[5 * k + 2, idx_zk + 4] = -dt * v_k * sec2 / L
        J[5 * k + 2, idx_zk1 + 2] = +1.0
        # eq 3: v_{k+1} - v_k - dt*a_k
        J[5 * k + 3, idx_zk + 3] = -1.0
        J[5 * k + 3, idx_zk1 + 3] = +1.0
        J[5 * k + 3, idx_uk + 0] = -dt
        # eq 4: delta_{k+1} - delta_k - dt*omega_k
        J[5 * k + 4, idx_zk + 4] = -1.0
        J[5 * k + 4, idx_zk1 + 4] = +1.0
        J[5 * k + 4, idx_uk + 1] = -dt
    return J


# ============================================================
# 解析 dynamics Jacobian — sparse triplet 版本（与 dense 等价）
#
# 每步 k 的 nonzero 结构（共 18 个）：
#   eq 0 (px): zk+0, zk+2, zk+3, zk1+0
#   eq 1 (py): zk+1, zk+2, zk+3, zk1+1
#   eq 2 (θ):  zk+2, zk+3, zk+4, zk1+2
#   eq 3 (v):  zk+3, zk1+3, uk+0
#   eq 4 (δ):  zk+4, zk1+4, uk+1
#
# 总 nonzero = 18*N。N=600 时 = 10800（vs dense 5N*n_vars = 12.6M，~1170× 稀疏）。
# ============================================================


def _dynamics_jacobian_structure(layout: NlpVarLayout) -> Tuple[np.ndarray, np.ndarray]:
    """返回 dynamics Jacobian 的 (rows, cols) 索引（不依赖 flat 值）。"""
    N = layout.n_steps
    nnz = 18 * N
    rows = np.empty((nnz,), dtype=np.int64)
    cols = np.empty((nnz,), dtype=np.int64)
    ptr = 0
    for k in range(N):
        idx_zk = layout.state_offset + k * STATE_DIM
        idx_zk1 = layout.state_offset + (k + 1) * STATE_DIM
        idx_uk = layout.control_offset + k * CONTROL_DIM
        # eq 0 (px): zk+0, zk+2, zk+3, zk1+0
        rows[ptr : ptr + 4] = 5 * k + 0
        cols[ptr : ptr + 4] = [idx_zk + 0, idx_zk + 2, idx_zk + 3, idx_zk1 + 0]
        ptr += 4
        # eq 1 (py): zk+1, zk+2, zk+3, zk1+1
        rows[ptr : ptr + 4] = 5 * k + 1
        cols[ptr : ptr + 4] = [idx_zk + 1, idx_zk + 2, idx_zk + 3, idx_zk1 + 1]
        ptr += 4
        # eq 2 (θ): zk+2, zk+3, zk+4, zk1+2
        rows[ptr : ptr + 4] = 5 * k + 2
        cols[ptr : ptr + 4] = [idx_zk + 2, idx_zk + 3, idx_zk + 4, idx_zk1 + 2]
        ptr += 4
        # eq 3 (v): zk+3, zk1+3, uk+0
        rows[ptr : ptr + 3] = 5 * k + 3
        cols[ptr : ptr + 3] = [idx_zk + 3, idx_zk1 + 3, idx_uk + 0]
        ptr += 3
        # eq 4 (δ): zk+4, zk1+4, uk+1
        rows[ptr : ptr + 3] = 5 * k + 4
        cols[ptr : ptr + 3] = [idx_zk + 4, idx_zk1 + 4, idx_uk + 1]
        ptr += 3
    return rows, cols


def _dynamics_jacobian_values(
    flat: np.ndarray,
    layout: NlpVarLayout,
    *,
    dt: float,
    wheelbase_m: float,
) -> np.ndarray:
    """返回 dynamics Jacobian 的 vals（顺序须与 _dynamics_jacobian_structure 一致）。"""
    z, _u = unflatten_solution(flat, layout)
    N = layout.n_steps
    L = float(wheelbase_m)
    nnz = 18 * N
    vals = np.empty((nnz,), dtype=np.float64)
    ptr = 0
    for k in range(N):
        v_k = z[k, 3]
        th_k = z[k, 2]
        de_k = z[k, 4]
        sin_th = np.sin(th_k)
        cos_th = np.cos(th_k)
        sec2 = 1.0 / (np.cos(de_k) ** 2)
        tan_de = np.tan(de_k)
        # eq 0: zk+0, zk+2, zk+3, zk1+0  → -1, +dt*v*sin, -dt*cos, +1
        vals[ptr + 0] = -1.0
        vals[ptr + 1] = +dt * v_k * sin_th
        vals[ptr + 2] = -dt * cos_th
        vals[ptr + 3] = +1.0
        ptr += 4
        # eq 1: zk+1, zk+2, zk+3, zk1+1  → -1, -dt*v*cos, -dt*sin, +1
        vals[ptr + 0] = -1.0
        vals[ptr + 1] = -dt * v_k * cos_th
        vals[ptr + 2] = -dt * sin_th
        vals[ptr + 3] = +1.0
        ptr += 4
        # eq 2: zk+2, zk+3, zk+4, zk1+2  → -1, -dt*tan(δ)/L, -dt*v*sec²/L, +1
        vals[ptr + 0] = -1.0
        vals[ptr + 1] = -dt * tan_de / L
        vals[ptr + 2] = -dt * v_k * sec2 / L
        vals[ptr + 3] = +1.0
        ptr += 4
        # eq 3: zk+3, zk1+3, uk+0  → -1, +1, -dt
        vals[ptr + 0] = -1.0
        vals[ptr + 1] = +1.0
        vals[ptr + 2] = -dt
        ptr += 3
        # eq 4: zk+4, zk1+4, uk+1  → -1, +1, -dt
        vals[ptr + 0] = -1.0
        vals[ptr + 1] = +1.0
        vals[ptr + 2] = -dt
        ptr += 3
    return vals


# ============================================================
# Task 4.3: 走廊 LSE 不等式约束（设计 §3.2.3）
#
# 数学背景：
#   - max(d_i) 不可微，IPOPT 要求 C¹ → 用 LSE = (1/μ₁)*log(Σ exp(μ₁*d_i))
#   - LSE 是 max 的 C¹ 上界，μ₁=1 时余量适中、避免 exp 溢出
#   - 数值稳定形式：LSE = m/μ + log(Σ exp(μ*d_i - m))/μ，其中 m = max(μ*d_i)
#
# 距离约定：
#   - d_i > 0  →  state 在边界外（违反走廊）
#   - d_i ≤ 0  →  state 在走廊内
#   - 段内：d_left = lateral - left_m, d_right = -lateral - right_m
#   - 段端点之外：fallback 为 best_d - max(left_m, right_m)（plan 规定）
# ============================================================


def _signed_distances_to_corridor(
    px: float,
    py: float,
    corridor: Sequence[CorridorSegment],
) -> np.ndarray:
    """对 (px, py) 计算到所有走廊段的左右边界有向距离。

    返回 d_i 数组：d_i > 0 表示在边界外侧（违反走廊）。
    每段贡献 2 个 d_i（左外、右外）。

    简化模型：找最近段（沿 d_unit 投影最接近 [0, arc_length] 的那段），
    用其法向计算 lateral，d_left = lateral - left_m, d_right = -lateral - right_m。
    """
    if len(corridor) == 0:
        return np.array([0.0, 0.0])
    best = None
    best_d = float("inf")
    for seg in corridor:
        sx, sy = seg.s_xy
        dxu, dyu = seg.d_unit
        rel_x = px - sx
        rel_y = py - sy
        proj = rel_x * dxu + rel_y * dyu
        # 左侧法向 n = (-dyu, dxu)；lateral = rel · n（左侧为正）
        lateral = -rel_x * dyu + rel_y * dxu
        # 候选距离：clamp proj to [0, arc_length]
        if proj < 0:
            d = math.hypot(rel_x, rel_y)
            in_seg = False
        elif proj > seg.arc_length_m:
            tail_x = rel_x - seg.arc_length_m * dxu
            tail_y = rel_y - seg.arc_length_m * dyu
            d = math.hypot(tail_x, tail_y)
            in_seg = False
        else:
            d = abs(lateral)
            in_seg = True
        if d < best_d:
            best_d = d
            best = (seg, in_seg, lateral)
    if best is None:
        return np.array([0.0, 0.0])
    seg, in_seg, lateral = best
    if not in_seg:
        # 端点之外 → 把"超出最长 left/right"作为惩罚
        return np.array([best_d - max(seg.left_m, seg.right_m)] * 2)
    d_left = lateral - seg.left_m
    d_right = -lateral - seg.right_m
    return np.array([d_left, d_right])


def corridor_lse_constraints(
    flat: np.ndarray,
    layout: NlpVarLayout,
    *,
    corridor: Sequence[CorridorSegment],
    mu1: float = 1.0,
    disc_offsets: Sequence[float] = (),
    disc_radius: float = 0.0,
) -> np.ndarray:
    """对每个 state 输出一个 LSE 软化 max。

    单点模式 (disc_offsets 为空)：直接评估 (px_k, py_k) 到走廊左右边界的有向距离，
    LSE 软化 max。返回长度 = N+1 的数组：g_k = (1/mu1)*log(sum exp(mu1 * d_i(z_k)))。

    多圆模式 (Lian 2023 §3.1 + §3.2.3)：用多个圆覆盖车体，每个圆心位置
    `(p_k + α_i [cosθ_k, sinθ_k])` 都视作 mass point，LSE 在所有 (n_disc × 2)
    距离上软化。等价于 CreateDilatedMap 后单点 mass point 模型——这里通过
    在每个 d_i 上加 disc_radius 偏移实现，corridor 不重新构建。

    约束 g_k ≤ 0（IPOPT 不等式 cu = 0, cl = -inf）。
    数值稳定：用 max-shift 形式
        LSE = m/μ + log(Σ exp(μ*d_i - m))/μ,  m = max(μ*d_i)
    避免 exp(大正数) 溢出。
    """
    z, _ = unflatten_solution(flat, layout)
    out = np.zeros((layout.n_states,), dtype=np.float64)
    offsets = tuple(float(o) for o in disc_offsets)
    Rd = float(disc_radius)
    if not offsets:
        # 单点模式：与原文 §3.2.3 公式一致，便于回归测试。
        for k in range(layout.n_states):
            d_arr = _signed_distances_to_corridor(z[k, 0], z[k, 1], corridor)
            scaled = mu1 * d_arr
            m = float(np.max(scaled))
            out[k] = m / mu1 + math.log(float(np.sum(np.exp(scaled - m)))) / mu1
        return out

    # 多圆模式：每个状态收集 (n_disc × 2) 个 d_i，统一 LSE。
    n_disc = len(offsets)
    for k in range(layout.n_states):
        px = float(z[k, 0])
        py = float(z[k, 1])
        cos_t = math.cos(float(z[k, 2]))
        sin_t = math.sin(float(z[k, 2]))
        d_full = np.empty((2 * n_disc,), dtype=np.float64)
        for i, alpha in enumerate(offsets):
            cx = px + alpha * cos_t
            cy = py + alpha * sin_t
            d_arr = _signed_distances_to_corridor(cx, cy, corridor)
            d_full[2 * i + 0] = d_arr[0] + Rd
            d_full[2 * i + 1] = d_arr[1] + Rd
        scaled = mu1 * d_full
        m = float(np.max(scaled))
        out[k] = m / mu1 + math.log(float(np.sum(np.exp(scaled - m)))) / mu1
    return out


# ============================================================
# 解析 LSE Jacobian（替换 FD，N=600 时 ~50× 加速）
#
# 数学要点：
#   LSE_k 仅依赖 (px_k, py_k)。控制变量与其他状态变量贡献为 0
#   → lse_J 极稀疏，每行仅 2 个 nonzero (列 = state_index(k,0), state_index(k,1))。
#   总 nonzero = 2 * n_states，相比 dense (n_states * n_vars) 节省 50× 计算量。
#
# 偏导推导：
#   LSE_k = (1/μ) * log(Σ_i exp(μ * d_i))
#   ∂LSE_k/∂px = Σ_i [softmax_i * ∂d_i/∂px]
#   softmax_i = exp(μ * d_i) / Σ_j exp(μ * d_j)
#
#   d_i 由 _signed_distances_to_corridor 计算，跟随 best segment 选择。
#   - in-segment 情况 (proj ∈ [0, arc_length])：
#       lateral = -rel_x * dyu + rel_y * dxu
#       d_left  =  lateral - left_m   →  ∂/∂px = -dyu, ∂/∂py = +dxu
#       d_right = -lateral - right_m  →  ∂/∂px = +dyu, ∂/∂py = -dxu
#   - 段端点之外 (proj < 0 或 proj > arc_length)：
#       d = sqrt(rel_x²+rel_y²)（端点距离），两个 d_i 等同（含 -max(left,right) 偏移）
#       ∂d/∂px = rel_x/d, ∂d/∂py = rel_y/d   （d=0 奇异 → clamp ≥ 1e-9）
#
# Math edge cases：
#   1. softmax 数值稳定 → max-shift (m = max(μ*d_i))
#   2. d→0（state 在端点） → clamp denom ≥ 1e-9 防奇异
#   3. best segment 切换不连续 → IPOPT 已忍受 FD 版本的同样问题
# ============================================================


def _signed_distances_and_partials(
    px: float,
    py: float,
    corridor: Sequence[CorridorSegment],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """扩展 _signed_distances_to_corridor，同时返回 ∂d_i/∂px, ∂d_i/∂py。

    返回 (d_arr, dpx_arr, dpy_arr)，每个长度 = 2 (与 _signed_distances 一致)。
    """
    if len(corridor) == 0:
        return (
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
        )
    best = None
    best_d = float("inf")
    for seg in corridor:
        sx, sy = seg.s_xy
        dxu, dyu = seg.d_unit
        rel_x = px - sx
        rel_y = py - sy
        proj = rel_x * dxu + rel_y * dyu
        lateral = -rel_x * dyu + rel_y * dxu
        if proj < 0:
            d = math.hypot(rel_x, rel_y)
            in_seg = False
            # 端点偏导：∂(sqrt(x²+y²))/∂x = x/sqrt
            d_safe = max(d, 1e-9)
            ddx, ddy = rel_x / d_safe, rel_y / d_safe
        elif proj > seg.arc_length_m:
            tail_x = rel_x - seg.arc_length_m * dxu
            tail_y = rel_y - seg.arc_length_m * dyu
            d = math.hypot(tail_x, tail_y)
            in_seg = False
            d_safe = max(d, 1e-9)
            ddx, ddy = tail_x / d_safe, tail_y / d_safe
        else:
            d = abs(lateral)
            in_seg = True
            ddx, ddy = 0.0, 0.0  # 占位，in_seg 分支用 lateral 偏导
        if d < best_d:
            best_d = d
            best = (seg, in_seg, lateral, ddx, ddy)
    if best is None:
        return (
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
            np.array([0.0, 0.0]),
        )
    seg, in_seg, lateral, ddx_outside, ddy_outside = best
    dxu, dyu = seg.d_unit
    if not in_seg:
        # 端点之外：两个 d_i 都是 best_d - max(left,right)
        # ∂d_i/∂px = ddx_outside (端点距离的偏导)
        d_val = best_d - max(seg.left_m, seg.right_m)
        return (
            np.array([d_val, d_val]),
            np.array([ddx_outside, ddx_outside]),
            np.array([ddy_outside, ddy_outside]),
        )
    # in-segment：lateral = -rel_x * dyu + rel_y * dxu
    #   ∂lateral/∂px = -dyu, ∂lateral/∂py = +dxu
    d_left = lateral - seg.left_m
    d_right = -lateral - seg.right_m
    return (
        np.array([d_left, d_right]),
        np.array([-dyu, +dyu]),
        np.array([+dxu, -dxu]),
    )


def corridor_lse_jacobian_sparse(
    flat: np.ndarray,
    layout: NlpVarLayout,
    *,
    corridor: Sequence[CorridorSegment],
    mu1: float = 1.0,
    disc_offsets: Sequence[float] = (),
    disc_radius: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """解析 LSE Jacobian，sparse triplet (rows, cols, vals)。

    单点模式 (disc_offsets 空)：每个 state 仅依赖 (px, py)，nnz = 2 * n_states。
    多圆模式：disc 中心 = (px + α cosθ, py + α sinθ)，依赖 (px, py, θ)，
    nnz = 3 * n_states。
    """
    z, _ = unflatten_solution(flat, layout)
    n_states = layout.n_states
    offsets = tuple(float(o) for o in disc_offsets)
    Rd = float(disc_radius)
    mu = float(mu1)

    if not offsets:
        rows = np.empty((2 * n_states,), dtype=np.int64)
        cols = np.empty((2 * n_states,), dtype=np.int64)
        vals = np.empty((2 * n_states,), dtype=np.float64)
        for k in range(n_states):
            px, py = float(z[k, 0]), float(z[k, 1])
            d_arr, dpx_arr, dpy_arr = _signed_distances_and_partials(px, py, corridor)
            scaled = mu * d_arr
            m = float(np.max(scaled))
            ex = np.exp(scaled - m)
            sm = ex / float(np.sum(ex))
            d_lse_dpx = float(np.dot(sm, dpx_arr))
            d_lse_dpy = float(np.dot(sm, dpy_arr))
            rows[2 * k + 0] = k
            rows[2 * k + 1] = k
            cols[2 * k + 0] = layout.state_index(k, 0)
            cols[2 * k + 1] = layout.state_index(k, 1)
            vals[2 * k + 0] = d_lse_dpx
            vals[2 * k + 1] = d_lse_dpy
        return rows, cols, vals

    # 多圆模式：每行 3 nnz (px, py, θ)。
    n_disc = len(offsets)
    rows = np.empty((3 * n_states,), dtype=np.int64)
    cols = np.empty((3 * n_states,), dtype=np.int64)
    vals = np.empty((3 * n_states,), dtype=np.float64)
    for k in range(n_states):
        px = float(z[k, 0])
        py = float(z[k, 1])
        theta = float(z[k, 2])
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        d_full = np.empty((2 * n_disc,), dtype=np.float64)
        dpx_full = np.empty((2 * n_disc,), dtype=np.float64)
        dpy_full = np.empty((2 * n_disc,), dtype=np.float64)
        dth_full = np.empty((2 * n_disc,), dtype=np.float64)
        for i, alpha in enumerate(offsets):
            cx = px + alpha * cos_t
            cy = py + alpha * sin_t
            d_arr, dcx_arr, dcy_arr = _signed_distances_and_partials(cx, cy, corridor)
            base = 2 * i
            d_full[base:base + 2] = d_arr + Rd
            dpx_full[base:base + 2] = dcx_arr
            dpy_full[base:base + 2] = dcy_arr
            # ∂cx/∂θ = -α sinθ, ∂cy/∂θ = +α cosθ
            dth_full[base:base + 2] = (
                dcx_arr * (-alpha * sin_t) + dcy_arr * (alpha * cos_t)
            )
        scaled = mu * d_full
        m = float(np.max(scaled))
        ex = np.exp(scaled - m)
        sm = ex / float(np.sum(ex))
        d_lse_dpx = float(np.dot(sm, dpx_full))
        d_lse_dpy = float(np.dot(sm, dpy_full))
        d_lse_dth = float(np.dot(sm, dth_full))
        rows[3 * k + 0] = k
        rows[3 * k + 1] = k
        rows[3 * k + 2] = k
        cols[3 * k + 0] = layout.state_index(k, 0)
        cols[3 * k + 1] = layout.state_index(k, 1)
        cols[3 * k + 2] = layout.state_index(k, 2)
        vals[3 * k + 0] = d_lse_dpx
        vals[3 * k + 1] = d_lse_dpy
        vals[3 * k + 2] = d_lse_dth
    return rows, cols, vals


# ============================================================
# Task 4.4: IPOPT 端到端求解（设计 §3.2.5 + §3.2.6）
#
# 集成思路：
#   - 目标函数：J = mu2 * Σ a_k² * dt + mu3 * Σ omega_k² * dt（控制能量）
#   - 等式约束：动力学残差 (5N) + 起点 BC (5) + 终点 BC (5) = 5N + 10
#   - 不等式约束：走廊 LSE (N+1)，cl=-inf, cu=0
#   - 总约束数：6N + 11；变量数：5(N+1) + 2N = 7N + 5
#
# Jacobian 拼接顺序与 constraints() 必须一致：
#   [dyn_J (5N×n) ; bc_start_J (5×n) ; bc_goal_J (5×n) ; lse_J (N+1)×n]
# 走廊 LSE Jacobian 用有限差分（小 N 可接受；生产应改解析）。
#
# IPOPT 选项：
#   - hessian_approximation = limited-memory（quasi-Newton, 不需手写 Hessian）
#   - print_level = 0 + sb=yes（静默 banner）
#   - status_msg 在不同 cyipopt 版本可能是 bytes，须 defensive 处理。
# ============================================================
from dataclasses import dataclass
from typing import Tuple as _Tuple

import cyipopt


@dataclass
class NlpResult:
    success: bool
    status: str
    flat_solution: np.ndarray
    iters: int
    obj: float
    info: dict


class _NlpProblem:
    """cyipopt.Problem 的回调集合。"""

    def __init__(
        self, layout, corridor, dt, L, v_max, delta_max, a_max, omega_max,
        mu1, mu2, mu3, start_state, goal_state,
        disc_offsets: Sequence[float] = (),
        disc_radius: float = 0.0,
        z_ref_xy: np.ndarray | None = None,
        ref_xy_weight: float = 0.0,
    ):
        self.layout = layout
        self.corridor = corridor
        self.dt = float(dt)
        self.L = float(L)
        self.v_max = float(v_max)
        self.delta_max = float(delta_max)
        self.a_max = float(a_max)
        self.omega_max = float(omega_max)
        self.mu1 = float(mu1)
        self.mu2 = float(mu2)
        self.mu3 = float(mu3)
        self.start = np.asarray(start_state, dtype=np.float64)
        self.goal = np.asarray(goal_state, dtype=np.float64)
        self.disc_offsets = tuple(float(o) for o in disc_offsets)
        self.disc_radius = float(disc_radius)
        self.ref_xy_weight = float(ref_xy_weight)
        if z_ref_xy is None or self.ref_xy_weight <= 0.0:
            self.z_ref_xy = None
        else:
            ref = np.asarray(z_ref_xy, dtype=np.float64)
            if ref.shape != (layout.n_states, 2):
                raise ValueError(
                    "z_ref_xy must have shape "
                    f"({layout.n_states}, 2), got {ref.shape}"
                )
            self.z_ref_xy = ref
        # 多圆模式：disc 中心位置依赖 (px, py, θ)，jacobian 每行 3 nnz；
        # 单点模式：仅依赖 (px, py)，每行 2 nnz。
        self._has_disc_theta = bool(self.disc_offsets)
        # ----------------------------------------------------------------
        # 预计算稀疏 Jacobian structure（与 flat 值无关，只跟 layout/n_states 有关）。
        # 拼接顺序：dyn (5N, 18*N nnz) | bc_start (5, 5 nnz) | bc_goal (5, 5 nnz)
        #          | lse (N+1, k*(N+1) nnz, k=2 单点 / 3 多圆)
        # cyipopt 把 (rows, cols) 视作 COO，jacobian() 返回值须按同顺序排列。
        # ----------------------------------------------------------------
        N = layout.n_steps
        n_states = layout.n_states
        # dyn block
        dyn_rows, dyn_cols = _dynamics_jacobian_structure(layout)
        # bc_start: 5 行 (offset = 5N)，列 = state_index(0, d)
        bc_start_rows = np.array([5 * N + d for d in range(5)], dtype=np.int64)
        bc_start_cols = np.array(
            [layout.state_index(0, d) for d in range(5)], dtype=np.int64
        )
        # bc_goal: 5 行 (offset = 5N + 5)
        bc_goal_rows = np.array([5 * N + 5 + d for d in range(5)], dtype=np.int64)
        bc_goal_cols = np.array(
            [layout.state_index(n_states - 1, d) for d in range(5)], dtype=np.int64
        )
        # lse: 每行 k 对应 row offset = 5N + 10 + k，nonzero cols 取决于模式
        lse_offset = 5 * N + 10
        nnz_per_state = 3 if self._has_disc_theta else 2
        lse_rows = np.empty((nnz_per_state * n_states,), dtype=np.int64)
        lse_cols = np.empty((nnz_per_state * n_states,), dtype=np.int64)
        for k in range(n_states):
            base = nnz_per_state * k
            lse_rows[base + 0] = lse_offset + k
            lse_rows[base + 1] = lse_offset + k
            lse_cols[base + 0] = layout.state_index(k, 0)
            lse_cols[base + 1] = layout.state_index(k, 1)
            if self._has_disc_theta:
                lse_rows[base + 2] = lse_offset + k
                lse_cols[base + 2] = layout.state_index(k, 2)
        self._jac_rows = np.concatenate([dyn_rows, bc_start_rows, bc_goal_rows, lse_rows])
        self._jac_cols = np.concatenate([dyn_cols, bc_start_cols, bc_goal_cols, lse_cols])
        self._dyn_nnz = dyn_rows.size
        self._bc_start_nnz = 5
        self._bc_goal_nnz = 5
        self._lse_nnz = nnz_per_state * n_states

    def objective(self, flat: np.ndarray) -> float:
        z, u = unflatten_solution(flat, self.layout)
        control = (
            self.mu2 * np.sum(u[:, 0] ** 2) * self.dt
            + self.mu3 * np.sum(u[:, 1] ** 2) * self.dt
        )
        if self.z_ref_xy is None:
            return float(control)
        ref = self.ref_xy_weight * np.sum(
            (z[:, 0] - self.z_ref_xy[:, 0]) ** 2
            + (z[:, 1] - self.z_ref_xy[:, 1]) ** 2
        ) * self.dt
        return float(control + ref)

    def gradient(self, flat: np.ndarray) -> np.ndarray:
        z, u = unflatten_solution(flat, self.layout)
        g = np.zeros_like(flat)
        for k in range(self.layout.n_steps):
            ia = self.layout.control_index(k, 0)
            iom = self.layout.control_index(k, 1)
            g[ia] = 2.0 * self.mu2 * u[k, 0] * self.dt
            g[iom] = 2.0 * self.mu3 * u[k, 1] * self.dt
        if self.z_ref_xy is not None:
            w = 2.0 * self.ref_xy_weight * self.dt
            for k in range(self.layout.n_states):
                g[self.layout.state_index(k, 0)] += w * (z[k, 0] - self.z_ref_xy[k, 0])
                g[self.layout.state_index(k, 1)] += w * (z[k, 1] - self.z_ref_xy[k, 1])
        return g

    def constraints(self, flat: np.ndarray) -> np.ndarray:
        # [动力学等式 5N] + [起点 5] + [终点 5] + [走廊 LSE N+1]
        dyn = dynamics_residual(flat, self.layout, dt=self.dt, wheelbase_m=self.L)
        z, _ = unflatten_solution(flat, self.layout)
        bc_start = z[0] - self.start
        bc_goal = z[-1] - self.goal
        lse = corridor_lse_constraints(
            flat, self.layout,
            corridor=self.corridor, mu1=self.mu1,
            disc_offsets=self.disc_offsets, disc_radius=self.disc_radius,
        )
        return np.concatenate([dyn, bc_start, bc_goal, lse])

    def jacobianstructure(self) -> Tuple[np.ndarray, np.ndarray]:
        """声明 sparse Jacobian 的 (rows, cols) 索引给 IPOPT。

        cyipopt 一旦看到此方法，便切到 sparse mode：
        - jacobian() 返回值数组与 (rows, cols) 一一对应（不是 dense flatten）
        - IPOPT 复用此 structure 不重复探测稀疏模式 → 大 N 时关键加速
        """
        return self._jac_rows, self._jac_cols

    def jacobian(self, flat: np.ndarray) -> np.ndarray:
        # ----------------------------------------------------------------
        # Sparse Jacobian values，按 jacobianstructure() 顺序排列：
        #   [dyn_vals (18*N) | bc_start_vals (5) | bc_goal_vals (5) | lse_vals (2*(N+1))]
        # bc_start/bc_goal 的所有非零项均为 +1（state diff = z[0/-1] - target）。
        # LSE vals 由 corridor_lse_jacobian_sparse 提供。
        # 加速点：N=600 时 nnz ≈ 12k（vs dense 15M），IPOPT 仅看 12k 个 entry。
        # ----------------------------------------------------------------
        dyn_vals = _dynamics_jacobian_values(
            flat, self.layout, dt=self.dt, wheelbase_m=self.L
        )
        bc_start_vals = np.ones((5,), dtype=np.float64)
        bc_goal_vals = np.ones((5,), dtype=np.float64)
        _, _, lse_vals = corridor_lse_jacobian_sparse(
            flat, self.layout,
            corridor=self.corridor, mu1=self.mu1,
            disc_offsets=self.disc_offsets, disc_radius=self.disc_radius,
        )
        return np.concatenate([dyn_vals, bc_start_vals, bc_goal_vals, lse_vals])


def solve_nlp(
    *,
    flat0: np.ndarray,
    layout: NlpVarLayout,
    corridor,
    start_state: _Tuple[float, float, float, float, float],
    goal_state: _Tuple[float, float, float, float, float],
    dt: float,
    wheelbase_m: float,
    v_max: float,
    delta_max: float,
    a_max: float,
    omega_max: float,
    mu1: float = 1.0,
    mu2: float = 0.01,
    mu3: float = 0.01,
    max_iter: int = 200,
    max_cpu_time_s: float = 30.0,
    tol: float = 1e-3,
    disc_offsets: Sequence[float] = (),
    disc_radius: float = 0.0,
    z_ref_xy: np.ndarray | None = None,
    ref_xy_weight: float = 0.0,
) -> NlpResult:
    """构造 + 解 IPOPT NLP。

    disc_offsets / disc_radius 控制 Lian 2023 多圆车体覆盖（§3.1 + §3.2.3）：
    传入空 = 单点 mass-point 模式（向后兼容旧测试）；
    传入 (α₁, α₂, ...) + Rd = 每个 disc 中心都作为 mass point 在走廊 LSE 中
    单独约束，等价于 CreateDilatedMap 后多 mass point 模型。
    """
    prob = _NlpProblem(
        layout, corridor, dt, wheelbase_m,
        v_max, delta_max, a_max, omega_max,
        mu1, mu2, mu3, start_state, goal_state,
        disc_offsets=disc_offsets, disc_radius=disc_radius,
        z_ref_xy=z_ref_xy, ref_xy_weight=ref_xy_weight,
    )
    n = layout.n_vars
    n_dyn = 5 * layout.n_steps
    n_bc = 10
    n_lse = layout.n_states
    n_cons = n_dyn + n_bc + n_lse
    cl = np.zeros((n_cons,))
    cu = np.zeros((n_cons,))
    cl[n_dyn + n_bc :] = -1e20  # 走廊 LSE: cl=-inf, cu=0

    lb, ub = layout.variable_bounds(v_max=v_max, delta_max=delta_max, a_max=a_max, omega_max=omega_max)

    nlp = cyipopt.Problem(
        n=n, m=n_cons,
        problem_obj=prob,
        lb=lb, ub=ub,
        cl=cl, cu=cu,
    )
    nlp.add_option("max_iter", int(max_iter))
    nlp.add_option("max_cpu_time", float(max_cpu_time_s))
    nlp.add_option("tol", float(tol))
    nlp.add_option("hessian_approximation", "limited-memory")
    nlp.add_option("print_level", 0)
    nlp.add_option("sb", "yes")  # 静默 banner
    # 多圆 / 大 corridor 起始点常常违反 LSE，但实测 (2026-05-10) 在 realmap_a
    # 上启用 mu_strategy=adaptive / constr_viol_tol 反而让 IPOPT 提前 fallback
    # 到 restoration phase 而非寻可行步，导致 single-point 也收敛失败；保持
    # paper §3.2.5 默认 monotone barrier 流程。
    nlp.add_option("acceptable_tol", 1e-2)
    nlp.add_option("acceptable_iter", 5)

    x_opt, info = nlp.solve(flat0)
    # ----------------------------------------------------------------
    # cyipopt 在不同版本/平台下，info["status_msg"] 可能是：
    #   - 完整英文句子（bytes/str，cyipopt 1.7+）
    #   - 短 enum 名（"Solve_Succeeded" 等，旧版 / 部分构建）
    # 这里以 info["status"] 整数为准，按官方 IPOPT ApplicationReturnStatus
    # 枚举映射回符号名，提供稳定接口。
    # ----------------------------------------------------------------
    _IPOPT_STATUS_MAP = {
        0: "Solve_Succeeded",
        1: "Solved_To_Acceptable_Level",
        2: "Infeasible_Problem_Detected",
        3: "Search_Direction_Becomes_Too_Small",
        4: "Diverging_Iterates",
        5: "User_Requested_Stop",
        6: "Feasible_Point_Found",
        -1: "Maximum_Iterations_Exceeded",
        -2: "Restoration_Failed",
        -3: "Error_In_Step_Computation",
        -4: "Maximum_CpuTime_Exceeded",
        -10: "Not_Enough_Degrees_Of_Freedom",
        -11: "Invalid_Problem_Definition",
        -12: "Invalid_Option",
        -13: "Invalid_Number_Detected",
        -100: "Unrecoverable_Exception",
        -101: "NonIpopt_Exception_Thrown",
        -102: "Insufficient_Memory",
        -199: "Internal_Error",
    }
    status_int = int(info.get("status", -999))
    status_str = _IPOPT_STATUS_MAP.get(status_int, f"Unknown_Status_{status_int}")
    success = status_int in (0, 1)
    return NlpResult(
        success=success,
        status=status_str,
        flat_solution=np.asarray(x_opt),
        iters=int(info.get("iter_count", 0)),
        obj=float(info.get("obj_val", 0.0)),
        info=info,
    )
