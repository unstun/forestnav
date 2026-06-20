from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from forest_n3p.features import FeatureConfig, extract_features
from forest_n3p.third_party.pathplan import GridMap


@dataclass(frozen=True)
class MapProfile:
    name: str
    seed: int
    trunk_count: int
    trunk_gap_m: float


PROFILES = (
    MapProfile(name="low_density", seed=2026062001, trunk_count=25, trunk_gap_m=1.20),
    MapProfile(name="medium_density", seed=2026062002, trunk_count=50, trunk_gap_m=1.00),
    MapProfile(name="high_density", seed=2026062003, trunk_count=75, trunk_gap_m=0.85),
)


def _mark_disk(grid: np.ndarray, cx: float, cy: float, radius_cells: float) -> None:
    h, w = grid.shape
    x0 = max(0, int(math.floor(cx - radius_cells - 1.0)))
    x1 = min(w - 1, int(math.ceil(cx + radius_cells + 1.0)))
    y0 = max(0, int(math.floor(cy - radius_cells - 1.0)))
    y1 = min(h - 1, int(math.ceil(cy + radius_cells + 1.0)))
    if x1 < x0 or y1 < y0:
        return
    xs = np.arange(x0, x1 + 1, dtype=np.float64)
    ys = np.arange(y0, y1 + 1, dtype=np.float64)
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= radius_cells**2
    grid[y0 : y1 + 1, x0 : x1 + 1][mask] = 1


def _clear_disk(grid: np.ndarray, cx: float, cy: float, radius_cells: float) -> None:
    h, w = grid.shape
    x0 = max(0, int(math.floor(cx - radius_cells - 1.0)))
    x1 = min(w - 1, int(math.ceil(cx + radius_cells + 1.0)))
    y0 = max(0, int(math.floor(cy - radius_cells - 1.0)))
    y1 = min(h - 1, int(math.ceil(cy + radius_cells + 1.0)))
    if x1 < x0 or y1 < y0:
        return
    xs = np.arange(x0, x1 + 1, dtype=np.float64)
    ys = np.arange(y0, y1 + 1, dtype=np.float64)
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= radius_cells**2
    grid[y0 : y1 + 1, x0 : x1 + 1][mask] = 0


def _synthetic_grid(profile: MapProfile) -> tuple[np.ndarray, tuple[int, int], tuple[int, int], str]:
    rng = np.random.default_rng(profile.seed)
    h = w = 180
    grid = np.zeros((h, w), dtype=np.uint8)
    start_xy = (32, 34)
    goal_xy = (146, 144)

    for _ in range(profile.trunk_count):
        cx = float(rng.uniform(12, w - 12))
        cy = float(rng.uniform(12, h - 12))
        if (cx - start_xy[0]) ** 2 + (cy - start_xy[1]) ** 2 < 18.0**2:
            continue
        if (cx - goal_xy[0]) ** 2 + (cy - goal_xy[1]) ** 2 < 18.0**2:
            continue
        radius_cells = float(rng.uniform(1.8, 4.2))
        _mark_disk(grid, cx=cx, cy=cy, radius_cells=radius_cells)

    _clear_disk(grid, cx=float(start_xy[0]), cy=float(start_xy[1]), radius_cells=8.0)
    _clear_disk(grid, cx=float(goal_xy[0]), cy=float(goal_xy[1]), radius_cells=8.0)
    return grid, start_xy, goal_xy, "synthetic_disk_forest"


def _procedural_grid(profile: MapProfile) -> tuple[np.ndarray, tuple[int, int], tuple[int, int], str]:
    from forest_n3p.maps.forest import ForestParams, generate_forest_grid

    params = ForestParams(
        width_cells=180,
        height_cells=180,
        cell_size_m=0.1,
        trunk_count=profile.trunk_count,
        trunk_gap_m=profile.trunk_gap_m,
        trunk_gap_jitter=0.20,
        trunk_place_tries=12_000,
        max_tries=30,
        start_frac=0.18,
        goal_frac=0.82,
    )
    cell = float(params.cell_size_m)
    body_radius = math.hypot(0.740 / 2.0, 0.924 / 4.0)
    footprint_clearance_m = body_radius + math.sqrt(2.0) * 0.5 * cell
    rng = np.random.default_rng(profile.seed)
    grid, start_xy, goal_xy = generate_forest_grid(
        params=params,
        rng=rng,
        footprint_clearance_m=footprint_clearance_m,
    )
    return grid, start_xy, goal_xy, "forest_n3p.maps.forest.generate_forest_grid"


def make_grid(profile: MapProfile) -> tuple[np.ndarray, tuple[int, int], tuple[int, int], str]:
    try:
        return _procedural_grid(profile)
    except Exception as exc:
        grid, start_xy, goal_xy, source = _synthetic_grid(profile)
        return grid, start_xy, goal_xy, f"{source}; procedural_fallback_reason={type(exc).__name__}"


def draw_feature_map(
    grid: np.ndarray,
    *,
    resolution_m: float,
    start_pose: tuple[float, float, float],
    goal_pose: tuple[float, float, float],
    profile_name: str,
    source: str,
    output_path: Path,
) -> dict[str, object]:
    grid_map = GridMap(grid, resolution=resolution_m, origin=(0.0, 0.0))
    cfg = FeatureConfig()
    result = extract_features(grid_map, start_pose, goal_pose, config=cfg)

    h, w = grid.shape
    extent = (
        -0.5 * resolution_m,
        (float(w) - 0.5) * resolution_m,
        -0.5 * resolution_m,
        (float(h) - 0.5) * resolution_m,
    )

    fig, ax = plt.subplots(figsize=(8.0, 8.0), dpi=160)
    ax.imshow(
        grid,
        origin="lower",
        extent=extent,
        cmap="gray_r",
        interpolation="nearest",
        vmin=0,
        vmax=1,
    )

    x, y, theta = start_pose
    world_angles = result.ray_angles_rad + theta
    for idx, (angle, dist) in enumerate(zip(world_angles, result.ray_distances_m, strict=True)):
        end_x = x + float(dist) * math.cos(float(angle))
        end_y = y + float(dist) * math.sin(float(angle))
        color = "#2d9cdb" if float(dist) >= cfg.r_max_m - 1e-9 else "#f2994a"
        line_width = 1.2 if idx % 4 == 0 else 0.8
        ax.plot([x, end_x], [y, end_y], color=color, linewidth=line_width, alpha=0.85)
        if float(dist) < cfg.r_max_m - 1e-9:
            ax.plot(end_x, end_y, marker="o", markersize=2.6, color="#d84f2a", alpha=0.9)

    ax.plot(start_pose[0], start_pose[1], marker="o", markersize=7, color="#1a7f37", label="start")
    ax.arrow(
        start_pose[0],
        start_pose[1],
        0.8 * math.cos(start_pose[2]),
        0.8 * math.sin(start_pose[2]),
        width=0.035,
        head_width=0.22,
        head_length=0.28,
        color="#1a7f37",
        length_includes_head=True,
    )
    ax.plot(goal_pose[0], goal_pose[1], marker="*", markersize=11, color="#b42318", label="goal")
    ax.arrow(
        goal_pose[0],
        goal_pose[1],
        0.8 * math.cos(goal_pose[2]),
        0.8 * math.sin(goal_pose[2]),
        width=0.035,
        head_width=0.22,
        head_length=0.28,
        color="#b42318",
        length_includes_head=True,
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(
        f"{profile_name}: 32-ray profile, dim={result.vector.shape[0]}\n"
        f"density={np.round(result.density_ratios, 3).tolist()} source={source.split(';')[0]}",
        fontsize=10,
    )
    ax.legend(loc="upper left", framealpha=0.85)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    return {
        "profile": profile_name,
        "source": source,
        "image": str(output_path),
        "feature_dim": int(result.vector.shape[0]),
        "start_pose": [float(v) for v in start_pose],
        "goal_pose": [float(v) for v in goal_pose],
        "density_ratios": [float(v) for v in result.density_ratios],
        "ray_distances_m": [float(v) for v in result.ray_distances_m],
        "feature_vector": [float(v) for v in result.vector],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize F-N3P T03 ray-cast clearance features.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/t03_feature_visuals"),
        help="Directory for PNG images and summary JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []

    for profile in PROFILES:
        grid, start_xy, goal_xy, source = make_grid(profile)
        resolution_m = 0.1
        start_x = float(start_xy[0]) * resolution_m
        start_y = float(start_xy[1]) * resolution_m
        goal_x = float(goal_xy[0]) * resolution_m
        goal_y = float(goal_xy[1]) * resolution_m
        heading = math.atan2(goal_y - start_y, goal_x - start_x)
        start_pose = (start_x, start_y, heading)
        goal_pose = (goal_x, goal_y, heading)
        output_path = output_dir / f"{profile.name}.png"
        records.append(
            draw_feature_map(
                grid,
                resolution_m=resolution_m,
                start_pose=start_pose,
                goal_pose=goal_pose,
                profile_name=profile.name,
                source=source,
                output_path=output_path,
            )
        )

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    for record in records:
        print(record["image"])
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
