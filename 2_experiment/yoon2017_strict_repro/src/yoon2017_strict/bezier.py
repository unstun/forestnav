from __future__ import annotations

from dataclasses import dataclass
import math

from .geometry import Pose


@dataclass(frozen=True)
class CubicBezier:
    p0: tuple[float, float]
    p1: tuple[float, float]
    p2: tuple[float, float]
    p3: tuple[float, float]

    def point(self, t: float) -> tuple[float, float]:
        u = 1.0 - float(t)
        tt = float(t)
        b0 = u * u * u
        b1 = 3.0 * u * u * tt
        b2 = 3.0 * u * tt * tt
        b3 = tt * tt * tt
        x = b0 * self.p0[0] + b1 * self.p1[0] + b2 * self.p2[0] + b3 * self.p3[0]
        y = b0 * self.p0[1] + b1 * self.p1[1] + b2 * self.p2[1] + b3 * self.p3[1]
        return float(x), float(y)

    def deriv(self, t: float) -> tuple[float, float]:
        u = 1.0 - float(t)
        tt = float(t)
        dx = (
            3.0 * u * u * (self.p1[0] - self.p0[0])
            + 6.0 * u * tt * (self.p2[0] - self.p1[0])
            + 3.0 * tt * tt * (self.p3[0] - self.p2[0])
        )
        dy = (
            3.0 * u * u * (self.p1[1] - self.p0[1])
            + 6.0 * u * tt * (self.p2[1] - self.p1[1])
            + 3.0 * tt * tt * (self.p3[1] - self.p2[1])
        )
        return float(dx), float(dy)

    def deriv2(self, t: float) -> tuple[float, float]:
        u = 1.0 - float(t)
        tt = float(t)
        d2x = (
            6.0 * u * (self.p2[0] - 2.0 * self.p1[0] + self.p0[0])
            + 6.0 * tt * (self.p3[0] - 2.0 * self.p2[0] + self.p1[0])
        )
        d2y = (
            6.0 * u * (self.p2[1] - 2.0 * self.p1[1] + self.p0[1])
            + 6.0 * tt * (self.p3[1] - 2.0 * self.p2[1] + self.p1[1])
        )
        return float(d2x), float(d2y)

    def control_polygon_length(self) -> float:
        return (
            math.hypot(self.p1[0] - self.p0[0], self.p1[1] - self.p0[1])
            + math.hypot(self.p2[0] - self.p1[0], self.p2[1] - self.p1[1])
            + math.hypot(self.p3[0] - self.p2[0], self.p3[1] - self.p2[1])
        )


@dataclass(frozen=True)
class BiarcEdge:
    seg1: CubicBezier
    seg2: CubicBezier
    start_pose: Pose
    end_pose: Pose
    x_int: tuple[float, float]
    gamma_rad: float
    curve_distance_m: float
    straight_start: tuple[Pose, Pose] | None = None
    straight_end: tuple[Pose, Pose] | None = None


def build_biarc(
    start: Pose,
    end: Pose,
    *,
    min_turn_radius_m: float,
    gamma: float | None = None,
    mode: str = "new_wiring",
) -> BiarcEdge | None:
    """Build Yoon2017 Fig. 7 / Yang-Sukkarieh two-Bezier primitive.

    The public paper uses the symbol gamma for the corner angle at x_int. It
    is therefore derived from each edge geometry here, not treated as a global
    tuning parameter. The optional gamma argument is retained only for old
    adapter calls and is deliberately unused.
    """
    _ = gamma
    x_int = _select_x_int(start, end, mode=mode)
    if x_int is None:
        return None

    p_start = (float(start.x), float(start.y))
    p_end = (float(end.x), float(end.y))
    v_back = (p_start[0] - x_int[0], p_start[1] - x_int[1])
    v_fwd = (p_end[0] - x_int[0], p_end[1] - x_int[1])
    len_back = math.hypot(v_back[0], v_back[1])
    len_fwd = math.hypot(v_fwd[0], v_fwd[1])
    if len_back <= 1e-9 or len_fwd <= 1e-9:
        return None

    u_back = (v_back[0] / len_back, v_back[1] / len_back)
    u_fwd = (v_fwd[0] / len_fwd, v_fwd[1] / len_fwd)
    incoming = (-u_back[0], -u_back[1])
    dot = max(-1.0, min(1.0, incoming[0] * u_fwd[0] + incoming[1] * u_fwd[1]))
    gamma_rad = math.acos(dot)
    if gamma_rad <= 1e-6:
        return _build_degenerate_straight_edge(start, end, x_int=x_int, gamma_rad=0.0)

    alpha = 0.5 * gamma_rad
    cos_alpha = math.cos(alpha)
    if abs(cos_alpha) <= 1e-9:
        return None
    kappa_max = 1.0 / max(float(min_turn_radius_m), 1e-9)
    c1 = 7.2364
    c2 = (2.0 / 5.0) * (math.sqrt(6.0) - 1.0)
    c3 = (c2 + 4.0) / (c1 + 6.0)
    c4 = ((c2 + 4.0) ** 2) / (54.0 * c3)
    d = c4 * math.sin(alpha) / (kappa_max * cos_alpha * cos_alpha)
    if not math.isfinite(d) or d <= 1e-9:
        return None
    if d > len_back + 1e-9 or d > len_fwd + 1e-9:
        return None

    q = c3 * d
    p = c2 * q
    f = (6.0 * c3 * cos_alpha / (c2 + 4.0)) * d

    b0 = _add(x_int, _scale(u_back, d))
    b1 = _add(b0, _scale(u_back, -p))
    b2 = _add(b1, _scale(u_back, -q))
    a0 = _add(x_int, _scale(u_fwd, d))
    a1 = _add(a0, _scale(u_fwd, -p))
    a2 = _add(a1, _scale(u_fwd, -q))
    ud = _unit((a2[0] - b2[0], a2[1] - b2[1]))
    if ud is None:
        return None
    b3 = _add(b2, _scale(ud, f))
    a3 = _add(a2, _scale(ud, -f))
    joint = (0.5 * (b3[0] + a3[0]), 0.5 * (b3[1] + a3[1]))

    start_theta = math.atan2(b0[1] - p_start[1], b0[0] - p_start[0])
    end_theta = math.atan2(p_end[1] - a0[1], p_end[0] - a0[0])
    pre = None
    if math.hypot(b0[0] - p_start[0], b0[1] - p_start[1]) > 1e-9:
        pre = (Pose(p_start[0], p_start[1], start_theta), Pose(b0[0], b0[1], start_theta))
    post = None
    if math.hypot(p_end[0] - a0[0], p_end[1] - a0[1]) > 1e-9:
        post = (Pose(a0[0], a0[1], end_theta), Pose(p_end[0], p_end[1], end_theta))

    return BiarcEdge(
        seg1=CubicBezier(p0=b0, p1=b1, p2=b2, p3=joint),
        seg2=CubicBezier(p0=joint, p1=a2, p2=a1, p3=a0),
        start_pose=pre[0] if pre is not None else Pose(b0[0], b0[1], start_theta),
        end_pose=post[1] if post is not None else Pose(a0[0], a0[1], end_theta),
        x_int=x_int,
        gamma_rad=float(gamma_rad),
        curve_distance_m=float(d),
        straight_start=pre,
        straight_end=post,
    )


def _select_x_int(start: Pose, end: Pose, *, mode: str) -> tuple[float, float] | None:
    sx, sy = float(start.x), float(start.y)
    ex, ey = float(end.x), float(end.y)
    hx, hy = math.cos(float(start.theta)), math.sin(float(start.theta))
    dx, dy = ex - sx, ey - sy
    eps = 1e-9
    if mode == "new_wiring":
        denom = 2.0 * (dx * hx + dy * hy)
        if abs(denom) <= eps:
            return None
        t = (dx * dx + dy * dy) / denom
    elif mode == "rewiring":
        t = dx * hx + dy * hy
    else:
        raise ValueError(f"unknown Bezier primitive mode: {mode}")
    if not math.isfinite(t) or t <= eps:
        return None
    return sx + t * hx, sy + t * hy


def _build_degenerate_straight_edge(
    start: Pose,
    end: Pose,
    *,
    x_int: tuple[float, float],
    gamma_rad: float,
) -> BiarcEdge | None:
    sx, sy = float(start.x), float(start.y)
    ex, ey = float(end.x), float(end.y)
    dist = math.hypot(ex - sx, ey - sy)
    if dist <= 1e-9:
        return None
    theta = math.atan2(ey - sy, ex - sx)
    mid = (0.5 * (sx + ex), 0.5 * (sy + ey))
    seg1 = _line_cubic((sx, sy), mid)
    seg2 = _line_cubic(mid, (ex, ey))
    return BiarcEdge(
        seg1=seg1,
        seg2=seg2,
        start_pose=Pose(sx, sy, theta),
        end_pose=Pose(ex, ey, theta),
        x_int=x_int,
        gamma_rad=float(gamma_rad),
        curve_distance_m=0.0,
    )


def _line_cubic(start_xy: tuple[float, float], end_xy: tuple[float, float]) -> CubicBezier:
    x0, y0 = start_xy
    x3, y3 = end_xy
    return CubicBezier(
        p0=start_xy,
        p1=(x0 + (x3 - x0) / 3.0, y0 + (y3 - y0) / 3.0),
        p2=(x0 + 2.0 * (x3 - x0) / 3.0, y0 + 2.0 * (y3 - y0) / 3.0),
        p3=end_xy,
    )


def _scale(v: tuple[float, float], s: float) -> tuple[float, float]:
    return float(v[0]) * float(s), float(v[1]) * float(s)


def _add(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return float(a[0]) + float(b[0]), float(a[1]) + float(b[1])


def _unit(v: tuple[float, float]) -> tuple[float, float] | None:
    n = math.hypot(v[0], v[1])
    if n <= 1e-12:
        return None
    return v[0] / n, v[1] / n


def edge_poses_and_length(edge: BiarcEdge, *, step_m: float) -> tuple[list[Pose], float]:
    poses: list[Pose] = []
    length = 0.0
    prev_xy: tuple[float, float] | None = None
    if edge.straight_start is not None:
        prev_xy, length = _append_line_poses(
            poses,
            edge.straight_start[0],
            edge.straight_start[1],
            step_m=step_m,
            prev_xy=prev_xy,
            length=length,
        )
    for seg_idx, seg in enumerate((edge.seg1, edge.seg2)):
        approx = max(1e-6, seg.control_polygon_length())
        n = max(2, int(math.ceil(approx / max(float(step_m), 1e-6))))
        n = min(n, 4000)
        for i in range(n + 1):
            if (seg_idx > 0 or poses) and i == 0:
                continue
            t = i / n
            x, y = seg.point(t)
            dx, dy = seg.deriv(t)
            theta = math.atan2(dy, dx) if dx * dx + dy * dy > 1e-18 else (poses[-1].theta if poses else 0.0)
            poses.append(Pose(float(x), float(y), float(theta)))
            if prev_xy is not None:
                length += math.hypot(x - prev_xy[0], y - prev_xy[1])
            prev_xy = (x, y)
    if edge.straight_end is not None:
        prev_xy, length = _append_line_poses(
            poses,
            edge.straight_end[0],
            edge.straight_end[1],
            step_m=step_m,
            prev_xy=prev_xy,
            length=length,
        )
    return poses, float(length)


def _append_line_poses(
    poses: list[Pose],
    start: Pose,
    end: Pose,
    *,
    step_m: float,
    prev_xy: tuple[float, float] | None,
    length: float,
) -> tuple[tuple[float, float] | None, float]:
    sx, sy = float(start.x), float(start.y)
    ex, ey = float(end.x), float(end.y)
    seg_len = math.hypot(ex - sx, ey - sy)
    if seg_len <= 1e-12:
        return prev_xy, length
    theta = math.atan2(ey - sy, ex - sx)
    n = max(1, int(math.ceil(seg_len / max(float(step_m), 1e-6))))
    for i in range(n + 1):
        if poses and i == 0:
            continue
        s = i / n
        x = sx + (ex - sx) * s
        y = sy + (ey - sy) * s
        poses.append(Pose(float(x), float(y), float(theta)))
        if prev_xy is not None:
            length += math.hypot(x - prev_xy[0], y - prev_xy[1])
        prev_xy = (x, y)
    return prev_xy, length
