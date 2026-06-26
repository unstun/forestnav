"""LianPlanner 顶层（Lian 2023 设计 §1.1 / §2.5）。

流水线
------
Stage 1: 2D A* → 走廊 → 边界点 → EHA*（分段 HA*）
Stage 2: IPOPT NLP（精确轨迹）

入口
----
LianPlanner.plan(...)  返回 PlanResult；失败也缓存，避免重复跑 NLP。
"""
from __future__ import annotations

# ===========================================================================
# 标准库
# ===========================================================================
import hashlib
import math
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# ===========================================================================
# 第三方
# ===========================================================================
import numpy as np

# ===========================================================================
# 内部依赖（各阶段模块）
# ===========================================================================
from forest_n3p.baselines.lian2023_paper_from_scratch.astar_2d import astar_2d_path
from forest_n3p.baselines.lian2023_paper_from_scratch.boundary_points import select_boundary_points
from forest_n3p.baselines.lian2023_paper_from_scratch.corridor import build_corridor, is_corridor_degenerate
from forest_n3p.baselines.lian2023_paper_from_scratch.eha_star import resample_path_to_n_points, run_eha_star
from forest_n3p.baselines.lian2023_paper_from_scratch.nlp import (
    NlpVarLayout,
    flatten_initial_guess,
    solve_nlp,
    unflatten_solution,
)
from forest_n3p.baselines.lian2023_paper_from_scratch.types import (
    CorridorSegment,
    GridSpec,
    PlanResult,
    PlanStatus,
    TrajPoint,
    VehicleDiscs,
    VehicleParams,
)


# ---------------------------------------------------------------------------
# 类型别名
# ---------------------------------------------------------------------------
State5 = Tuple[float, float, float, float, float]


# ===========================================================================
# 配置
# ===========================================================================

@dataclass
class LianPlannerConfig:
    """规划参数（结构来自 Lian 2023 Table I，车辆限幅使用本地 UGV 约束）。

    参数说明
    --------
    dl1_m, dl2_m  : 走廊构建两级步长（粗/细）
    l_max_m       : 走廊单段最大长度
    L_thre_m      : BP 选取距离阈值
    N_max         : 最多 BP 数
    mu1/mu2/mu3   : NLP 惩罚权重（走廊/加速/角速）
    nlp_max_iter  : IPOPT 最大迭代
    nlp_max_cpu_time_s : IPOPT 最大 CPU 时间
    nlp_tol       : IPOPT 收敛容忍
    eha_per_segment_timeout_s : 单段 HA* 超时
    total_timeout_s : 全流程超时（含所有阶段）
    a_max_m_s2    : 加速度约束
    omega_max_rad_s : 转向角速率约束
    delta_max_rad : 转向角约束（default_ackermann_params 对应 27 deg）
    footprint_diameter_m : 碰撞几何直径，用于 2D A* 膨胀
    nlp_v0        : NLP 初始猜测速度
    """

    dl1_m: float = 1.0
    dl2_m: float = 0.1
    l_max_m: float = 8.0
    L_thre_m: float = 4.5
    N_max: int = 10
    mu1: float = 1.0
    mu2: float = 0.01
    mu3: float = 0.01
    nlp_ref_xy_weight: float = 0.0
    nlp_max_iter: int = 200
    nlp_max_cpu_time_s: float = 30.0
    nlp_tol: float = 1e-3
    eha_per_segment_timeout_s: float = 2.0
    total_timeout_s: float = 60.0
    a_max_m_s2: float = 1.0
    omega_max_rad_s: float = math.radians(60.0)
    # AckermannParams 未暴露 delta_max，写到 Config
    delta_max_rad: float = math.radians(27.0)
    footprint_diameter_m: float = 0.74
    nlp_v0: float = 1.0   # NLP 初值速度
    # ----------------------------------------------------------------
    # NLP 内部步数上限（Lian 2023 paper Table I: n=200）
    # ----------------------------------------------------------------
    # 当 caller 传入的 n_steps > nlp_n_steps_max 时，NLP 内部用降采样后的
    # (nlp_n, nlp_dt) 求解，再线性插值回 (n_steps, dt) 输出。这样保持
    # total_T = n_steps * dt 不变，同时避免 N=2000 级别 IPOPT 不收敛。
    # 经验：N≥1500 时 IPOPT L-BFGS Hessian 难以收敛，N=200 与论文一致。
    # 诊断溯源：debug_nlp_realmap_a.py 2026-05-07
    # ----------------------------------------------------------------
    nlp_n_steps_max: int = 200    # NLP 求解最大步数（Lian 2023 paper Table I）
    nlp_dt_max: float = 0.3       # NLP 最大 dt（防止 dt 太大丢失精度）
    # 诊断（debug_nlp_realmap_a.py 2026-05-07）实测 realmap_a (total_T=100s):
    #   nlp_dt=0.5 / N=200 → IPOPT 0 iter 立刻 Max_Iter 退出（warm-start 距可行域过远）
    #   nlp_dt=0.25/ N=400 → 失败（同 trial）
    #   nlp_dt=0.3 / N=333 → SUCCESS in 2.5s ← 当前默认
    #   nlp_dt=0.2 / N=500 → SUCCESS in 3.9s
    # ----------------------------------------------------------------
    # 与 env collision 对齐:env 用 d < r + half_cell(额外 0.05m),
    # NLP 自然遵循 d < r。在 corridor 上加 safety margin 让 NLP 解远离障碍
    # >= env buffer。实测(诊断 09:30 round): margin=0.05 时 NLP 路径满足 env
    # 检查;太大会让走廊降为 degenerate(过早触发 stage1_corridor_degenerate)。
    # ----------------------------------------------------------------
    safety_margin_m: float = 0.1   # 双倍 env half_cell：让 NLP 路径远离 env collision buffer
    # ----------------------------------------------------------------
    # 多圆车体覆盖（Lian 2023 §3.1）：disc_offsets 沿车身轴方向，disc_radius
    # 是覆盖圆半径。默认值 = 空元组 + 0，则 NLP 退化为单点 mass-point；
    # LianPlanner.plan 在 footprint 已知时会用 _disc_geometry_from_footprint 覆盖
    # 这两个字段，使 corridor LSE 约束按多圆模型工作。
    # ----------------------------------------------------------------
    disc_offsets_m: tuple[float, ...] = ()
    disc_radius_m: float = 0.0
    # ----------------------------------------------------------------
    # skip_nlp: 跳过 Stage 2 NLP，直接用 EHA* 路径做 pursuit 参考
    # EHA* 路径只含 (x, y, theta)，TrajPoint 的 v/delta/a/omega 填 0
    # pursuit tracking 只用 (px, py)，所以 skip_nlp 不影响 pursuit 质量
    # 适用场景：NLP 收敛率低 / 快速诊断 EHA* 路径质量
    # ----------------------------------------------------------------
    skip_nlp: bool = False
    use_corridor_goal_theta: bool = False


# ===========================================================================
# 内部工具：NLP 解的时间轴重映射
# ===========================================================================

def _upsample_trajectory(
    *,
    z_nlp: np.ndarray,    # (nlp_n+1, 5)
    u_nlp: np.ndarray,    # (nlp_n,   2)
    nlp_n: int,
    nlp_dt: float,
    target_n: int,
    target_dt: float,
) -> List[TrajPoint]:
    """把 NLP 解 (nlp_n+1 状态 + nlp_n 控制) 线性插值到 target_n+1 点。

    设计要点
    --------
    1. 保持 total_T = nlp_n * nlp_dt = target_n * target_dt 不变。
    2. 状态 z 用线性插值；theta 做 wrap-safe 处理（差分先归一到 [-pi, pi]）。
    3. 控制 u 用 zero-order hold：u_nlp[i] 在 [i*nlp_dt, (i+1)*nlp_dt) 期间生效。
       target step k 落在该区间 → 用 u_nlp[i]。最后一个状态 (k = target_n)
       不再发出控制（按惯例置 0）。
    4. 当 target_n == nlp_n 且 target_dt == nlp_dt 时退化为直拷贝（alpha 全 0）。
    """
    out: List[TrajPoint] = []
    nlp_total_T = float(nlp_n) * float(nlp_dt)
    for k in range(target_n + 1):
        t_target = float(k) * float(target_dt)
        # 在 NLP 时间轴上的位置（边界 clip 防越界）
        t_nlp = min(t_target, nlp_total_T)
        # 浮点 segment index in [0, nlp_n]
        nlp_seg_t = t_nlp / float(nlp_dt)
        i = min(int(math.floor(nlp_seg_t)), nlp_n - 1)
        alpha = nlp_seg_t - i  # ∈ [0, 1]

        # ---- 状态线性插值（px, py, v, delta 直接 lerp）----
        z_a = z_nlp[i]
        z_b = z_nlp[i + 1]
        px = (1.0 - alpha) * z_a[0] + alpha * z_b[0]
        py = (1.0 - alpha) * z_a[1] + alpha * z_b[1]
        v  = (1.0 - alpha) * z_a[3] + alpha * z_b[3]
        de = (1.0 - alpha) * z_a[4] + alpha * z_b[4]

        # ---- theta wrap-safe 插值 ----
        # NLP 解的 theta 通常平滑（无 wrap），但稳妥起见把差分归到 [-pi, pi]
        theta_diff = z_b[2] - z_a[2]
        if theta_diff > math.pi:
            theta_diff -= 2.0 * math.pi
        elif theta_diff < -math.pi:
            theta_diff += 2.0 * math.pi
        th = z_a[2] + alpha * theta_diff

        # ---- 控制：ZOH，最后一个 sample (k == target_n) 置 0 ----
        if k < target_n and i < nlp_n:
            ak = float(u_nlp[i, 0])
            omk = float(u_nlp[i, 1])
        else:
            ak = 0.0
            omk = 0.0

        out.append(TrajPoint(
            px=float(px), py=float(py),
            theta=float(th),
            v=float(v), delta=float(de),
            a=ak, omega=omk,
            t=t_target,
        ))
    return out


# ===========================================================================
# 顶层规划器
# ===========================================================================

class LianPlanner:
    """Lian 2023 顶层规划器。

    使用方法
    --------
    planner = LianPlanner(params=..., footprint=...)
    result  = planner.plan(grid_map=..., start_state=..., goal_state=...,
                           n_steps=80, dt=0.1)
    """

    def __init__(
        self,
        *,
        params: VehicleParams,
        discs: VehicleDiscs,
        config: Optional[LianPlannerConfig] = None,
    ):
        self.params = params
        self.discs = discs
        self.config = config or LianPlannerConfig()
        # 失败结果也缓存：同一不可解任务不重复跑 NLP
        self._cache: Dict[bytes, PlanResult] = {}

    # -----------------------------------------------------------------------
    # 公开入口
    # -----------------------------------------------------------------------

    def plan(
        self,
        *,
        grid_map: GridSpec,
        start_state: State5,
        goal_state: State5,
        n_steps: int,
        dt: float,
    ) -> PlanResult:
        """执行完整规划流水线，返回 PlanResult。

        Parameters
        ----------
        grid_map     : 占据网格地图（data 字段）
        start_state  : (px, py, theta, v, delta)
        goal_state   : (px, py, theta, v, delta)
        n_steps      : 轨迹控制步数 N；返回 trajectory 长度 = N+1
        dt           : 仿真时间步长（s）
        """
        # ----------------------------------------------------------------
        # 缓存查找：同样输入直接返回（r1 is r2 引用相等）
        # ----------------------------------------------------------------
        cache_key = self._cache_key(grid_map, start_state, goal_state, n_steps, dt)
        if cache_key in self._cache:
            return self._cache[cache_key]

        t0 = time.time()
        stats: Dict[str, Any] = {}
        cfg = self.config
        cell = float(grid_map.resolution)   # m/cell

        # ----------------------------------------------------------------
        # 退化情况：start == goal（§1.2 review I2）
        # ----------------------------------------------------------------
        sx, sy = start_state[0], start_state[1]
        gx, gy = goal_state[0], goal_state[1]
        if math.hypot(sx - gx, sy - gy) < cell:
            stats["t_total_s"] = time.time() - t0
            tp = TrajPoint(
                px=sx, py=sy, theta=start_state[2], v=0.0, delta=0.0,
                a=0.0, omega=0.0, t=0.0,
            )
            return self._cache_and_return(
                cache_key, PlanStatus.SUCCESS, [tp] * (n_steps + 1), stats
            )

        # ================================================================
        # Stage 1.1: 2D A* (CreateDilatedMap 用 Rd 膨胀，Lian 2023 §3.1 line 419)
        # ================================================================
        sx_c = int(round(start_state[0] / cell))
        sy_c = int(round(start_state[1] / cell))
        gx_c = int(round(goal_state[0] / cell))
        gy_c = int(round(goal_state[1] / cell))
        # 仅当 caller 显式启用多圆覆盖 (cfg.disc_offsets_m 非空 + cfg.disc_radius_m>0)
        # 时按 Lian §3.1 "CreateDilatedMap with radius Rd" 用 Rd 膨胀；否则维持
        # 旧行为 footprint_diameter_m/2。Why: 多圆 + 大 Rd 在 realmap_a 上让
        # EHA* 走更外围、NLP 初值更难收敛；保留 caller 选择权。
        if cfg.disc_offsets_m and cfg.disc_radius_m > 0:
            astar_padding_m = float(cfg.disc_radius_m)
        else:
            astar_padding_m = float(cfg.footprint_diameter_m) / 2
        padding_cells = max(1, int(math.ceil(astar_padding_m / max(cell, 1e-9))))
        stats["astar2d_padding_cells"] = int(padding_cells)
        stats["astar2d_padding_m"] = float(astar_padding_m)
        path = astar_2d_path(
            grid_map=grid_map,
            start_cell=(sx_c, sy_c),
            goal_cell=(gx_c, gy_c),
            padding_cells=padding_cells,
        )
        stats["t_astar2d_s"] = time.time() - t0
        if path is None:
            return self._cache_and_return(
                cache_key, PlanStatus.STAGE1_2D_ASTAR_FAIL, [], stats
            )

        # ================================================================
        # Stage 1.2: 走廊构建
        # ================================================================
        t1 = time.time()
        corridor = build_corridor(
            grid_map=grid_map, path_cells=path,
            dl1_m=cfg.dl1_m, dl2_m=cfg.dl2_m, l_max_m=cfg.l_max_m,
        )
        stats["t_corridor_s"] = time.time() - t1

        # ================================================================
        # Stage 1.2.5: 与 env collision 对齐,加 safety margin
        # ----------------------------------------------------------------
        # env collision 用 d < r + half_cell,而 NLP 走廊约束自然遵循 d < r。
        # 收缩每段 left/right 让 NLP 解远离障碍 >= safety margin,从而满足 env。
        # 收缩后再做 degenerate 检查 + BP 选取 + NLP,各阶段视图一致。
        # ================================================================
        if cfg.safety_margin_m > 0 and corridor:
            margin = float(cfg.safety_margin_m)
            corridor = [
                CorridorSegment(
                    s_xy=s.s_xy,
                    d_unit=s.d_unit,
                    left_m=max(0.0, s.left_m - margin),
                    right_m=max(0.0, s.right_m - margin),
                    arc_length_m=s.arc_length_m,
                )
                for s in corridor
            ]

        if is_corridor_degenerate(
            corridor, footprint_diameter_m=cfg.footprint_diameter_m
        ):
            return self._cache_and_return(
                cache_key, PlanStatus.STAGE1_CORRIDOR_DEGENERATE, [], stats
            )

        # ================================================================
        # Stage 1.3: 边界点选取
        # ----------------------------------------------------------------
        # from-scratch 默认保留 caller 提供的目标航向。
        # corridor tangent 仅作为显式 adapter 开关，不作为本目录默认行为。
        # ================================================================
        if cfg.use_corridor_goal_theta and len(corridor) > 0:
            d_last = corridor[-1].d_unit
            goal_theta_eff = math.atan2(d_last[1], d_last[0])
            stats["goal_theta_policy"] = "corridor_tangent"
        else:
            goal_theta_eff = goal_state[2]
            stats["goal_theta_policy"] = "caller_goal_state"
        bps = select_boundary_points(
            corridor=corridor,
            start_xy_theta=(start_state[0], start_state[1], start_state[2]),
            goal_xy_theta=(goal_state[0], goal_state[1], goal_theta_eff),
            L_thre_m=cfg.L_thre_m,
            N_max=cfg.N_max,
        )

        # ================================================================
        # Stage 1.4: EHA*（分段 HA*）
        # ================================================================
        t2 = time.time()
        eha_status, raw_path = run_eha_star(
            grid_map=grid_map,
            discs=self.discs,
            params=self.params,
            boundary_points=bps,
            per_segment_timeout_s=cfg.eha_per_segment_timeout_s,
        )
        stats["t_eha_s"] = time.time() - t2
        if eha_status != PlanStatus.SUCCESS:
            return self._cache_and_return(cache_key, eha_status, [], stats)

        # ================================================================
        # Stage 1.5 skip_nlp 快路径
        # ----------------------------------------------------------------
        # skip_nlp=True 时跳过 IPOPT NLP，直接把 EHA* raw_path 重采样到
        # n_steps+1 点，构造 TrajPoint 返回（v/delta/a/omega 填 0）。
        # pursuit tracking 只读 px/py，所以这些零字段不影响跟踪质量。
        # ================================================================
        if cfg.skip_nlp:
            resampled_full = resample_path_to_n_points(raw_path, n_points=n_steps + 1)
            trajectory = [
                TrajPoint(
                    px=float(xp), py=float(yp), theta=float(th),
                    v=0.0, delta=0.0, a=0.0, omega=0.0,
                    t=float(k) * dt,
                )
                for k, (xp, yp, th) in enumerate(resampled_full)
            ]
            stats["t_total_s"] = time.time() - t0
            return self._cache_and_return(cache_key, PlanStatus.SUCCESS, trajectory, stats)

        # ================================================================
        # Stage 1.5: 决定 NLP 内部 (nlp_n, nlp_dt)
        # ----------------------------------------------------------------
        # 目标:
        #   1) 保持 total_T = n_steps * dt 不变 (NLP 解的物理时长与 env 一致)
        #   2) NLP 步数 ≤ cfg.nlp_n_steps_max (paper Table I: n=200)
        #   3) NLP dt ≤ cfg.nlp_dt_max (避免 dt 过大丢失精度)
        # 求解后线性插值升采样回 (n_steps+1) 输出，env 不感知降采样。
        # ================================================================
        total_T = n_steps * dt
        nlp_n = min(int(n_steps), int(cfg.nlp_n_steps_max))
        nlp_dt = total_T / nlp_n
        # 防止 dt 过大丢失精度 → 退而求其次扩大 nlp_n
        if nlp_dt > cfg.nlp_dt_max:
            nlp_dt = cfg.nlp_dt_max
            nlp_n = max(1, int(round(total_T / nlp_dt)))
            # nlp_dt 重新校准，保持 nlp_n * nlp_dt = total_T
            nlp_dt = total_T / nlp_n
        stats["nlp_n"] = int(nlp_n)
        stats["nlp_dt_s"] = float(nlp_dt)
        stats["nlp_mu1"] = float(cfg.mu1)
        stats["nlp_ref_xy_weight"] = float(cfg.nlp_ref_xy_weight)

        # ----------------------------------------------------------------
        # 重采样 EHA* 路径到 nlp_n+1 点（NLP 需固定长度）
        # ----------------------------------------------------------------
        resampled = resample_path_to_n_points(raw_path, n_points=nlp_n + 1)

        # ================================================================
        # Stage 2: IPOPT NLP
        # ================================================================

        # 全局超时检查
        if (time.time() - t0) > cfg.total_timeout_s:
            return self._cache_and_return(
                cache_key, PlanStatus.RUNTIME_TIMEOUT, [], stats
            )

        t3 = time.time()
        layout = NlpVarLayout(n_steps=nlp_n)

        # NLP 初始猜测：用重采样路径填位姿，速度/转向角设常数初值
        z0 = np.zeros((nlp_n + 1, 5))
        for k, (x, y, th) in enumerate(resampled):
            z0[k, 0] = x
            z0[k, 1] = y
            z0[k, 2] = th
            z0[k, 3] = cfg.nlp_v0    # v 初值
            z0[k, 4] = 0.0           # delta 初值
        u0 = np.zeros((nlp_n, 2))
        flat0 = flatten_initial_guess(z0, u0, layout)

        # IPOPT CPU 时间 = min(config 上限, 剩余全局时间)
        remaining = cfg.total_timeout_s - (time.time() - t0)
        nlp_max_cpu = max(1.0, min(cfg.nlp_max_cpu_time_s, remaining))

        # ----------------------------------------------------------------
        # 多圆车体覆盖：仅在 caller 显式提供 cfg.disc_offsets_m 时启用。
        # paper-faithful 多圆版本由上层 wrapper（如 plan_lian2023_eha_nlp_paper）
        # 通过 disc_offsets_m=footprint.center_shift±center_offset, disc_radius_m=
        # footprint.radius 显式传入；不显式传则保持 §3.2.3 单点 mass-point 模式
        # （= legacy 行为，对 realmap_a 等紧凑场景 IPOPT 收敛更稳定）。
        # 校验：footprint 默认 vs Config 是否一致（仅在显式启用时输出 stats）。
        # ----------------------------------------------------------------
        if cfg.disc_offsets_m:
            disc_offsets = tuple(float(o) for o in cfg.disc_offsets_m)
            disc_radius = float(cfg.disc_radius_m)
        else:
            disc_offsets = ()
            disc_radius = 0.0
        stats["disc_offsets_m"] = list(disc_offsets)
        stats["disc_radius_m"] = float(disc_radius)
        nlp_res = solve_nlp(
            flat0=flat0,
            layout=layout,
            corridor=corridor,
            start_state=start_state,
            goal_state=goal_state,
            dt=nlp_dt,                         # ← NLP 内部用降采样后的 dt
            wheelbase_m=self.params.wheelbase_m,
            v_max=self.params.v_max_m_s,
            delta_max=cfg.delta_max_rad,
            a_max=cfg.a_max_m_s2,
            omega_max=cfg.omega_max_rad_s,
            mu1=cfg.mu1,
            mu2=cfg.mu2,
            mu3=cfg.mu3,
            max_iter=cfg.nlp_max_iter,
            max_cpu_time_s=nlp_max_cpu,
            tol=cfg.nlp_tol,
            disc_offsets=disc_offsets,
            disc_radius=disc_radius,
            z_ref_xy=z0[:, :2],
            ref_xy_weight=cfg.nlp_ref_xy_weight,
        )
        stats["t_nlp_s"] = time.time() - t3
        stats["nlp_iters"] = nlp_res.iters
        stats["nlp_status"] = nlp_res.status

        if not nlp_res.success:
            return self._cache_and_return(
                cache_key, PlanStatus.STAGE2_NLP_FAIL, [], stats
            )

        # ----------------------------------------------------------------
        # 构造 trajectory: NLP 解 (nlp_n+1 状态 + nlp_n 控制) → (n_steps+1) 点
        # 当 nlp_n == n_steps 时 _upsample_trajectory 退化为零开销直拷贝。
        # ----------------------------------------------------------------
        z_nlp, u_nlp = unflatten_solution(nlp_res.flat_solution, layout)
        trajectory = _upsample_trajectory(
            z_nlp=z_nlp,
            u_nlp=u_nlp,
            nlp_n=nlp_n,
            nlp_dt=nlp_dt,
            target_n=int(n_steps),
            target_dt=float(dt),
        )

        stats["t_total_s"] = time.time() - t0
        return self._cache_and_return(
            cache_key, PlanStatus.SUCCESS, trajectory, stats
        )

    # -----------------------------------------------------------------------
    # 内部工具
    # -----------------------------------------------------------------------

    def _cache_key(
        self,
        grid_map: GridSpec,
        start: State5,
        goal: State5,
        n_steps: int,
        dt: float,
    ) -> bytes:
        """SHA-1 over (map.data, start, goal, n_steps, dt)。"""
        h = hashlib.sha1()
        h.update(grid_map.data.tobytes())           # 正确字段：.data（非 .grid）
        h.update(np.asarray(start, dtype=np.float64).tobytes())
        h.update(np.asarray(goal,  dtype=np.float64).tobytes())
        h.update(np.asarray([n_steps, dt], dtype=np.float64).tobytes())
        return h.digest()

    def _cache_and_return(
        self,
        key: bytes,
        status: PlanStatus,
        traj,
        stats: Dict[str, Any],
    ) -> PlanResult:
        """构造 PlanResult，写入缓存并返回。失败结果同样缓存。"""
        result = PlanResult(
            status=status,
            trajectory=list(traj),
            stats=dict(stats),
        )
        self._cache[key] = result
        return result
