"""Lian 2023 EHA* + local EDT-safety NLP baseline.

该版本保留 EHA* 初值与本地 Ackermann 动力学，第二阶段安全约束改为本项目
EDT 双圆碰撞模型，用于得到与本地碰撞检查一致的优化轨迹。
"""
from __future__ import annotations

import math
import time
from typing import Any, Optional, Tuple

import numpy as np

from forest_n3p.baselines.common import PlannerResult
from forest_n3p.baselines.lian2023.eha_local import build_lian2023_eha_initial_path
from forest_n3p.baselines.lian2023.types import TrajPoint
from forest_n3p.third_party.pathplan import (
    AckermannParams,
    GridMap,
    OrientedBoxFootprint,
    TwoCircleFootprint,
)
from forest_n3p.third_party.pathplan.geometry import EDTCollisionChecker
from forest_n3p.third_party.pathplan.hybrid_a_star.obstacle_field import (
    compute_obstacle_distance_field,
)


class _EdtNlpProblem:
    """cyipopt callback：动力学等式 + 前后圆心 EDT 不等式。"""

    def __init__(
        self,
        *,
        layout: Any,
        dt: float,
        wheelbase_m: float,
        start_state: tuple[float, float, float, float, float],
        goal_state: tuple[float, float, float, float, float],
        edt_dist_m: np.ndarray,
        cell_size_m: float,
        collision_radius_m: float,
        circle_alphas_m: tuple[float, float],
        z_ref: np.ndarray,
        ref_weight: float,
        mu2: float = 0.01,
        mu3: float = 0.01,
    ) -> None:
        from forest_n3p.baselines.lian2023.nlp import _dynamics_jacobian_structure

        self.layout = layout
        self.dt = float(dt)
        self.wheelbase_m = float(wheelbase_m)
        self.start_state = np.asarray(start_state, dtype=np.float64)
        self.goal_state = np.asarray(goal_state, dtype=np.float64)
        self.edt_dist_m = np.asarray(edt_dist_m, dtype=np.float64)
        self.cell_size_m = float(cell_size_m)
        self.collision_radius_m = float(collision_radius_m)
        self.circle_alphas_m = tuple(float(v) for v in circle_alphas_m)
        self.z_ref = np.asarray(z_ref, dtype=np.float64)
        self.ref_weight = float(ref_weight)
        self.mu2 = float(mu2)
        self.mu3 = float(mu3)
        self.height, self.width = self.edt_dist_m.shape

        n_steps = layout.n_steps
        n_states = layout.n_states
        dyn_rows, dyn_cols = _dynamics_jacobian_structure(layout)
        bc_start_rows = np.array([5 * n_steps + d for d in range(5)], dtype=np.int64)
        bc_start_cols = np.array([layout.state_index(0, d) for d in range(5)], dtype=np.int64)
        bc_goal_rows = np.array([5 * n_steps + 5 + d for d in range(5)], dtype=np.int64)
        bc_goal_cols = np.array([layout.state_index(n_states - 1, d) for d in range(5)], dtype=np.int64)

        edt_rows: list[int] = []
        edt_cols: list[int] = []
        edt_offset = 5 * n_steps + 10
        for k in range(n_states):
            for circle_i in range(2):
                row = edt_offset + 2 * k + circle_i
                edt_rows.extend([row, row, row])
                edt_cols.extend([
                    layout.state_index(k, 0),
                    layout.state_index(k, 1),
                    layout.state_index(k, 2),
                ])

        self._jac_rows = np.concatenate([
            dyn_rows,
            bc_start_rows,
            bc_goal_rows,
            np.asarray(edt_rows, dtype=np.int64),
        ])
        self._jac_cols = np.concatenate([
            dyn_cols,
            bc_start_cols,
            bc_goal_cols,
            np.asarray(edt_cols, dtype=np.int64),
        ])

    def _dist_and_grad(self, x_m: float, y_m: float) -> tuple[float, float, float]:
        xi = float(x_m) / self.cell_size_m
        yi = float(y_m) / self.cell_size_m
        if not (0.0 <= xi <= self.width - 1 and 0.0 <= yi <= self.height - 1):
            return 0.0, 0.0, 0.0

        x0 = int(math.floor(xi))
        y0 = int(math.floor(yi))
        x1 = min(x0 + 1, self.width - 1)
        y1 = min(y0 + 1, self.height - 1)
        fx = xi - x0
        fy = yi - y0
        v00 = float(self.edt_dist_m[y0, x0])
        v10 = float(self.edt_dist_m[y0, x1])
        v01 = float(self.edt_dist_m[y1, x0])
        v11 = float(self.edt_dist_m[y1, x1])
        value = ((v00 * (1.0 - fx) + v10 * fx) * (1.0 - fy)) + (
            (v01 * (1.0 - fx) + v11 * fx) * fy
        )
        grad_xi = (1.0 - fy) * (v10 - v00) + fy * (v11 - v01)
        grad_yi = (1.0 - fx) * (v01 - v00) + fx * (v11 - v10)
        return (
            float(value),
            float(grad_xi / self.cell_size_m),
            float(grad_yi / self.cell_size_m),
        )

    def objective(self, flat: np.ndarray) -> float:
        from forest_n3p.baselines.lian2023.nlp import unflatten_solution

        z, u = unflatten_solution(flat, self.layout)
        control = (
            self.mu2 * float(np.sum(u[:, 0] ** 2)) * self.dt
            + self.mu3 * float(np.sum(u[:, 1] ** 2)) * self.dt
        )
        ref = self.ref_weight * float(
            np.sum((z[:, 0] - self.z_ref[:, 0]) ** 2 + (z[:, 1] - self.z_ref[:, 1]) ** 2)
        ) * self.dt
        return control + ref

    def gradient(self, flat: np.ndarray) -> np.ndarray:
        from forest_n3p.baselines.lian2023.nlp import unflatten_solution

        z, u = unflatten_solution(flat, self.layout)
        grad = np.zeros_like(flat)
        for k in range(self.layout.n_steps):
            grad[self.layout.control_index(k, 0)] = 2.0 * self.mu2 * u[k, 0] * self.dt
            grad[self.layout.control_index(k, 1)] = 2.0 * self.mu3 * u[k, 1] * self.dt
        for k in range(self.layout.n_states):
            grad[self.layout.state_index(k, 0)] += (
                2.0 * self.ref_weight * (z[k, 0] - self.z_ref[k, 0]) * self.dt
            )
            grad[self.layout.state_index(k, 1)] += (
                2.0 * self.ref_weight * (z[k, 1] - self.z_ref[k, 1]) * self.dt
            )
        return grad

    def _edt_constraints(self, flat: np.ndarray) -> np.ndarray:
        from forest_n3p.baselines.lian2023.nlp import unflatten_solution

        z, _ = unflatten_solution(flat, self.layout)
        out = np.zeros((2 * self.layout.n_states,), dtype=np.float64)
        ptr = 0
        for k in range(self.layout.n_states):
            px, py, theta = float(z[k, 0]), float(z[k, 1]), float(z[k, 2])
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            for alpha in self.circle_alphas_m:
                dist, _, _ = self._dist_and_grad(px + alpha * cos_t, py + alpha * sin_t)
                out[ptr] = self.collision_radius_m - dist
                ptr += 1
        return out

    def constraints(self, flat: np.ndarray) -> np.ndarray:
        from forest_n3p.baselines.lian2023.nlp import dynamics_residual, unflatten_solution

        dyn = dynamics_residual(
            flat,
            self.layout,
            dt=self.dt,
            wheelbase_m=self.wheelbase_m,
        )
        z, _ = unflatten_solution(flat, self.layout)
        return np.concatenate([
            dyn,
            z[0] - self.start_state,
            z[-1] - self.goal_state,
            self._edt_constraints(flat),
        ])

    def jacobianstructure(self) -> tuple[np.ndarray, np.ndarray]:
        return self._jac_rows, self._jac_cols

    def jacobian(self, flat: np.ndarray) -> np.ndarray:
        from forest_n3p.baselines.lian2023.nlp import (
            _dynamics_jacobian_values,
            unflatten_solution,
        )

        dyn_vals = _dynamics_jacobian_values(
            flat,
            self.layout,
            dt=self.dt,
            wheelbase_m=self.wheelbase_m,
        )
        z, _ = unflatten_solution(flat, self.layout)
        vals: list[float] = []
        for k in range(self.layout.n_states):
            px, py, theta = float(z[k, 0]), float(z[k, 1]), float(z[k, 2])
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            for alpha in self.circle_alphas_m:
                _, grad_x, grad_y = self._dist_and_grad(px + alpha * cos_t, py + alpha * sin_t)
                vals.extend([
                    -grad_x,
                    -grad_y,
                    -(grad_x * (-alpha * sin_t) + grad_y * (alpha * cos_t)),
                ])
        return np.concatenate([
            dyn_vals,
            np.ones((10,), dtype=np.float64),
            np.asarray(vals, dtype=np.float64),
        ])


def plan_lian2023_eha_nlp_edt(
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
    nlp_n: int = 2500,
    nlp_dt_s: float = 0.02,
    nlp_max_iter: int = 1200,
    nlp_max_cpu_time_s: float = 120.0,
    nlp_tol: float = 1e-3,
    ref_weight: float = 0.05,
) -> PlannerResult:
    """运行本地 EDT 安全约束 EHA*-NLP baseline。"""
    _ = max_nodes, collision_padding
    import cyipopt
    from forest_n3p.baselines.lian2023.eha_star import resample_path_to_n_points
    from forest_n3p.baselines.lian2023.nlp import (
        NlpVarLayout,
        flatten_initial_guess,
        unflatten_solution,
    )

    t0 = time.perf_counter()
    cell = float(grid_map.resolution)
    initial = build_lian2023_eha_initial_path(
        grid_map=grid_map,
        footprint=footprint,
        params=params,
        start_xy=start_xy,
        goal_xy=goal_xy,
        goal_theta_rad=goal_theta_rad,
        start_theta_rad=start_theta_rad,
        timeout_s=timeout_s,
        goal_xy_tol_m=goal_xy_tol_m,
        goal_theta_tol_rad=goal_theta_tol_rad,
    )
    if not initial.success:
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=float(initial.time_s),
            success=False,
            stats=initial.stats,
        )

    dist_field = compute_obstacle_distance_field(grid_map)
    checker = collision_checker
    if not isinstance(checker, EDTCollisionChecker):
        checker = EDTCollisionChecker(
            edt_dist_m=dist_field,
            cell_size_m=cell,
            footprint=footprint,
            edt_collision_margin="diag",
        )

    start_state = (
        float(start_xy[0]) * cell,
        float(start_xy[1]) * cell,
        float(initial.path_states[0][2]),
        0.0,
        0.0,
    )
    goal_state = (
        float(goal_xy[0]) * cell,
        float(goal_xy[1]) * cell,
        float(goal_theta_rad),
        0.0,
        0.0,
    )

    layout = NlpVarLayout(n_steps=int(nlp_n))
    resampled = resample_path_to_n_points(initial.path_states, n_points=int(nlp_n) + 1)
    z0 = np.zeros((int(nlp_n) + 1, 5), dtype=np.float64)
    for k, (x_m, y_m, theta) in enumerate(resampled):
        z0[k, 0] = float(x_m)
        z0[k, 1] = float(y_m)
        z0[k, 2] = float(theta)
        z0[k, 3] = 1.0
        z0[k, 4] = 0.0
    z0[0, 3] = 0.0
    z0[-1, 3] = 0.0
    u0 = np.zeros((int(nlp_n), 2), dtype=np.float64)
    flat0 = flatten_initial_guess(z0, u0, layout)

    circle_alphas = (
        float(footprint.center_shift + footprint.center_offset),
        float(footprint.center_shift - footprint.center_offset),
    )
    problem = _EdtNlpProblem(
        layout=layout,
        dt=float(nlp_dt_s),
        wheelbase_m=float(params.wheelbase),
        start_state=start_state,
        goal_state=goal_state,
        edt_dist_m=dist_field,
        cell_size_m=cell,
        collision_radius_m=float(checker._r_col),  # noqa: SLF001
        circle_alphas_m=circle_alphas,
        z_ref=z0,
        ref_weight=float(ref_weight),
    )
    n_constraints = 5 * layout.n_steps + 10 + 2 * layout.n_states
    cl = np.zeros((n_constraints,), dtype=np.float64)
    cu = np.zeros((n_constraints,), dtype=np.float64)
    cl[5 * layout.n_steps + 10 :] = -1e20
    lb, ub = layout.variable_bounds(
        v_max=float(params.v_max),
        delta_max=float(params.max_steer),
        a_max=1.0,
        omega_max=1.5,
    )
    nlp = cyipopt.Problem(
        n=layout.n_vars,
        m=n_constraints,
        problem_obj=problem,
        lb=lb,
        ub=ub,
        cl=cl,
        cu=cu,
    )
    nlp.add_option("max_iter", int(nlp_max_iter))
    nlp.add_option("max_cpu_time", float(nlp_max_cpu_time_s))
    nlp.add_option("tol", float(nlp_tol))
    nlp.add_option("acceptable_tol", 1e-2)
    nlp.add_option("hessian_approximation", "limited-memory")
    nlp.add_option("print_level", 0)
    nlp.add_option("sb", "yes")

    t_nlp0 = time.perf_counter()
    x_opt, info = nlp.solve(flat0)
    t_nlp_s = time.perf_counter() - t_nlp0
    status_int = int(info.get("status", -999))
    status_map = {
        0: "Solve_Succeeded",
        1: "Solved_To_Acceptable_Level",
        2: "Infeasible_Problem_Detected",
        6: "Feasible_Point_Found",
        -1: "Maximum_Iterations_Exceeded",
        -2: "Restoration_Failed",
        -4: "Maximum_CpuTime_Exceeded",
    }
    nlp_status = status_map.get(status_int, f"Unknown_Status_{status_int}")
    stats: dict[str, Any] = {
        **initial.stats,
        "variant": "lian2023_eha_nlp_edt",
        "nlp_status": nlp_status,
        "nlp_n": int(nlp_n),
        "nlp_dt_s": float(nlp_dt_s),
        "t_nlp_s": float(t_nlp_s),
        "nlp_objective": float(info.get("obj_val", float("nan"))),
        "edt_constraint_max": float(np.max(problem.constraints(np.asarray(x_opt))[5 * layout.n_steps + 10 :])),
        "edt_ref_weight": float(ref_weight),
        "time": float(time.perf_counter() - t0),
    }
    if status_int not in (0, 1):
        return PlannerResult(
            path_xy_cells=[(float(start_xy[0]), float(start_xy[1]))],
            time_s=float(stats["time"]),
            success=False,
            stats=stats,
        )

    z_opt, u_opt = unflatten_solution(np.asarray(x_opt), layout)
    trajectory = [
        TrajPoint(
            px=float(z_opt[k, 0]),
            py=float(z_opt[k, 1]),
            theta=float(z_opt[k, 2]),
            v=float(z_opt[k, 3]),
            delta=float(z_opt[k, 4]),
            a=float(u_opt[k, 0]) if k < int(nlp_n) else 0.0,
            omega=float(u_opt[k, 1]) if k < int(nlp_n) else 0.0,
            t=float(k) * float(nlp_dt_s),
        )
        for k in range(int(nlp_n) + 1)
    ]
    stats["trajectory"] = trajectory
    return PlannerResult(
        path_xy_cells=[(p.px / cell, p.py / cell) for p in trajectory],
        time_s=float(stats["time"]),
        success=True,
        stats=stats,
    )

