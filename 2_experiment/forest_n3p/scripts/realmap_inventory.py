"""T07 RealMap asset inventory and validation.

The script copies auditable ROS PGM/YAML maps into the F-N3P package, validates
that the package loader can read them, and writes a manifest plus preview
images for paper-facing provenance.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import urlopen

import cv2
import numpy as np

from forest_n3p.maps.pgm import load_pgm_yaml_map, load_ros_map_yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
ASSET_ROOT = REPO_ROOT / "2_experiment" / "forest_n3p" / "assets" / "realmaps"
REPORT_PATH = REPO_ROOT / ".pipeline" / "experiments" / "20260620_t07_realmap_inventory.md"

DQN9_REALMAP_DIR = Path("/Users/sun/tongbu/study/phdproject/dqn/DQN9/realmap")
DQN10_ROOT = Path("/Users/sun/tongbu/study/phdproject/dqn/DQN10")
DQN10_FALLBACK_MAPS = (
    DQN10_ROOT
    / "3_paper"
    / "results"
    / "exp1.2_core_comparison"
    / "final_t10_sr_long.2"
    / "20260316_135403"
    / "maps"
)
DQN_CANONICAL_START = (34, 29)
DQN_CANONICAL_GOAL = (371, 109)

WILLOW_YAML_URL = (
    "https://raw.githubusercontent.com/turtlebot/turtlebot_apps/indigo/"
    "turtlebot_navigation/maps/willow-2010-02-18-0.10.yaml"
)
WILLOW_PGM_URL = (
    "https://raw.githubusercontent.com/turtlebot/turtlebot_apps/indigo/"
    "turtlebot_navigation/maps/willow-2010-02-18-0.10.pgm"
)
WILLOW_SOURCE_PAGE = (
    "https://github.com/turtlebot/turtlebot_apps/tree/indigo/"
    "turtlebot_navigation/maps"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_raw_ros_classes(yaml_path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return occupied/free/unknown masks in y=0-bottom grid convention."""
    meta = load_ros_map_yaml(yaml_path)
    img = cv2.imread(str(meta.image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(meta.image_path)
    p = img.astype(np.float32) / 255.0
    if meta.negate:
        p = 1.0 - p
    occ_prob = 1.0 - p
    occupied = occ_prob > meta.occupied_thresh
    free = occ_prob < meta.free_thresh
    unknown = ~(occupied | free)
    return np.flipud(occupied), np.flipud(free), np.flipud(unknown)


def write_normalized_yaml(source_yaml: Path, dest_yaml: Path) -> None:
    meta = load_ros_map_yaml(source_yaml)
    dest_yaml.write_text(
        "\n".join(
            [
                "image: map.pgm",
                f"resolution: {meta.resolution:g}",
                (
                    "origin: "
                    f"[{meta.origin[0]:g}, {meta.origin[1]:g}, {meta.origin[2]:g}]"
                ),
                f"negate: {int(meta.negate)}",
                f"occupied_thresh: {meta.occupied_thresh:g}",
                f"free_thresh: {meta.free_thresh:g}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def download(url: str, dest: Path) -> None:
    with urlopen(url, timeout=30) as response:
        dest.write_bytes(response.read())


def copy_dqn_realmap() -> Path:
    source_pgm = DQN9_REALMAP_DIR / "map_a.pgm"
    source_yaml = DQN9_REALMAP_DIR / "map_a.yaml"
    if not source_pgm.is_file() or not source_yaml.is_file():
        raise FileNotFoundError(f"missing DQN9 RealMap source: {DQN9_REALMAP_DIR}")

    dest = ASSET_ROOT / "dqn_realmap_a"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_pgm, dest / "map.pgm")
    write_normalized_yaml(source_yaml, dest / "map.yaml")
    return dest / "map.yaml"


def copy_willow_map() -> Path:
    dest = ASSET_ROOT / "willow_garage_0p10"
    dest.mkdir(parents=True, exist_ok=True)
    raw_yaml = dest / "_source_willow.yaml"
    download(WILLOW_PGM_URL, dest / "map.pgm")
    download(WILLOW_YAML_URL, raw_yaml)
    write_normalized_yaml(raw_yaml, dest / "map.yaml")
    raw_yaml.unlink()
    return dest / "map.yaml"


def connected_component_pair(
    free_mask: np.ndarray,
    resolution_m: float,
    *,
    min_clearance_m: float = 0.8,
) -> tuple[tuple[int, int], tuple[int, int], float]:
    """Pick two far-apart known-free cells from the largest clearance component."""
    clearance = cv2.distanceTransform(free_mask.astype(np.uint8), cv2.DIST_L2, 5)
    min_clearance_cells = max(1.0, min_clearance_m / resolution_m)
    traversable = clearance >= min_clearance_cells
    if int(traversable.sum()) < 2:
        traversable = free_mask.astype(bool)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        traversable.astype(np.uint8),
        connectivity=8,
    )
    if num_labels <= 1:
        raise ValueError("no traversable component found")

    largest_label = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    cells_yx = np.argwhere(labels == largest_label)
    if cells_yx.shape[0] < 2:
        raise ValueError("largest traversable component is too small")

    anchor = cells_yx[np.argmin(cells_yx[:, 1])]
    d0 = np.sum((cells_yx - anchor) ** 2, axis=1)
    start_yx = cells_yx[int(np.argmax(d0))]
    d1 = np.sum((cells_yx - start_yx) ** 2, axis=1)
    goal_yx = cells_yx[int(np.argmax(d1))]

    start = (int(start_yx[1]), int(start_yx[0]))
    goal = (int(goal_yx[1]), int(goal_yx[0]))
    clearance_m = float(
        min(clearance[start_yx[0], start_yx[1]], clearance[goal_yx[0], goal_yx[1]])
        * resolution_m
    )
    return start, goal, clearance_m


def dqn10_duplicate_summary() -> dict[str, object]:
    paths = sorted(
        DQN10_ROOT.glob(
            "3_paper/results/exp1.2_core_comparison/*/*/maps/"
            "realmap_a__grid_y0_bottom.npz"
        )
    )
    hashes: dict[str, int] = {}
    examples: dict[str, str] = {}
    for path in paths:
        with np.load(path) as data:
            if "obstacle_grid" not in data.files:
                continue
            grid = data["obstacle_grid"].astype(np.uint8, copy=False)
        digest = hashlib.sha256(grid.tobytes()).hexdigest()
        hashes[digest] = hashes.get(digest, 0) + 1
        examples.setdefault(digest, str(path))
    return {
        "npz_count": len(paths),
        "unique_array_hashes": len(hashes),
        "hash_counts": hashes,
        "examples": examples,
    }


def render_preview(
    map_id: str,
    grid: np.ndarray,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    dest: Path,
) -> None:
    image = np.repeat((1 - np.flipud(grid)).astype(np.uint8)[:, :, None] * 255, 3, axis=2)
    h, w, _ = image.shape
    start_px = (int(start_xy[0]), int(h - 1 - start_xy[1]))
    goal_px = (int(goal_xy[0]), int(h - 1 - goal_xy[1]))
    radius = max(3, min(image.shape[:2]) // 80)
    cv2.circle(image, start_px, radius, (0, 180, 0), thickness=-1)
    cv2.circle(image, goal_px, radius, (0, 0, 220), thickness=-1)
    font_scale = max(0.35, min(0.7, min(h, w) / 500.0))
    thickness = 1 if font_scale < 0.55 else 2
    cv2.putText(
        image,
        map_id,
        (8, 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (30, 30, 200),
        thickness,
        cv2.LINE_AA,
    )
    cv2.imwrite(str(dest), image)


def render_overview(previews: list[Path], dest: Path) -> None:
    images = [cv2.imread(str(path), cv2.IMREAD_COLOR) for path in previews]
    images = [img for img in images if img is not None]
    if not images:
        return
    target_h = 360
    resized = []
    for img in images:
        scale = target_h / img.shape[0]
        resized.append(cv2.resize(img, (max(1, int(img.shape[1] * scale)), target_h)))
    gap = np.full((target_h, 16, 3), 240, dtype=np.uint8)
    canvas = resized[0]
    for img in resized[1:]:
        canvas = np.concatenate([canvas, gap, img], axis=1)
    cv2.imwrite(str(dest), canvas)


def validate_map(
    map_id: str,
    yaml_path: Path,
    *,
    source: dict[str, object],
    start_xy: tuple[int, int] | None = None,
    goal_xy: tuple[int, int] | None = None,
) -> dict[str, object]:
    meta = load_ros_map_yaml(yaml_path)
    occupied_raw, free_raw, unknown_raw = load_raw_ros_classes(yaml_path)
    if start_xy is None or goal_xy is None:
        start_xy, goal_xy, clearance_m = connected_component_pair(
            free_raw,
            meta.resolution,
        )
    else:
        clearance_m = None

    spec = load_pgm_yaml_map(yaml_path, start_xy, goal_xy, name=map_id)
    grid = spec.obstacle_grid()
    h, w = grid.shape
    for label, xy in (("start", start_xy), ("goal", goal_xy)):
        x, y = xy
        if not (0 <= x < w and 0 <= y < h):
            raise ValueError(f"{map_id} {label} out of bounds: {xy}, size={(w, h)}")
        if grid[y, x] != 0:
            raise ValueError(f"{map_id} {label} is occupied under loader grid: {xy}")
        if not free_raw[y, x]:
            raise ValueError(f"{map_id} {label} is not known-free under ROS YAML: {xy}")

    preview = yaml_path.parent / "preview.png"
    render_preview(map_id, grid, start_xy, goal_xy, preview)
    return {
        "id": map_id,
        "pgm": str((yaml_path.parent / "map.pgm").relative_to(REPO_ROOT)),
        "yaml": str(yaml_path.relative_to(REPO_ROOT)),
        "preview": str(preview.relative_to(REPO_ROOT)),
        "source": source,
        "resolution_m": meta.resolution,
        "origin": list(meta.origin),
        "width_cells": w,
        "height_cells": h,
        "loader_obstacle_cells": int(grid.sum()),
        "loader_free_cells": int(grid.size - grid.sum()),
        "ros_known_free_cells": int(free_raw.sum()),
        "ros_occupied_cells": int(occupied_raw.sum()),
        "ros_unknown_cells": int(unknown_raw.sum()),
        "start_xy": list(start_xy),
        "goal_xy": list(goal_xy),
        "endpoint_clearance_m": clearance_m,
        "pgm_sha256": sha256_file(yaml_path.parent / "map.pgm"),
        "loader_grid_sha256": hashlib.sha256(grid.tobytes()).hexdigest(),
        "load_check": "ok",
    }


def write_readme(manifest: dict[str, object]) -> None:
    lines = [
        "# F-N3P RealMap Assets",
        "",
        "These maps are the T07 validated ROS PGM/YAML assets for ForestNav.",
        "They are intended as real-map evaluation inputs, not as procedural forest scenes.",
        "",
        "| id | source | size | resolution | preview |",
        "|---|---|---:|---:|---|",
    ]
    for item in manifest["maps"]:  # type: ignore[index]
        row = item  # type: ignore[assignment]
        source = row["source"]["label"]  # type: ignore[index]
        lines.append(
            "| {id} | {source} | {width}x{height} | {resolution:g} m/cell | {preview} |".format(
                id=row["id"],  # type: ignore[index]
                source=source,
                width=row["width_cells"],  # type: ignore[index]
                height=row["height_cells"],  # type: ignore[index]
                resolution=row["resolution_m"],  # type: ignore[index]
                preview=row["preview"],  # type: ignore[index]
            )
        )
    lines.extend(
        [
            "",
            "Notes:",
            "- `dqn_realmap_a` is the local DQN RealMap source; DQN10 keeps this map as",
            "  NPZ fallback snapshots, while DQN9 preserves the original PGM/YAML pair.",
            "- `willow_garage_0p10` is copied from the BSD-licensed TurtleBot navigation",
            "  map package to satisfy the T07 two-map loading/display gate without",
            "  counting repeated DQN10 snapshots as independent maps.",
            "",
        ]
    )
    (ASSET_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_report(manifest: dict[str, object]) -> None:
    maps = manifest["maps"]  # type: ignore[index]
    duplicate = manifest["dqn10_duplicate_check"]  # type: ignore[index]
    rows = []
    for item in maps:  # type: ignore[assignment]
        rows.append(
            "| {id} | {source} | {size} | {resolution:g} | {start} | {goal} | ok |".format(
                id=item["id"],
                source=item["source"]["label"],
                size=f"{item['width_cells']}x{item['height_cells']}",
                resolution=item["resolution_m"],
                start=item["start_xy"],
                goal=item["goal_xy"],
            )
        )
    REPORT_PATH.write_text(
        "\n".join(
            [
                "---",
                "origin: ai_only",
                "reviewed: false",
                "task: T07",
                "created: 2026-06-20",
                "---",
                "",
                "# T07 RealMap 资产清点",
                "",
                "## 结论",
                "",
                "- DQN10 历史结果目录中找到了 `realmap_a` NPZ fallback，但 20 个快照只有 1 个唯一数组哈希，不能算作 2 张独立地图。",
                "- DQN9 保留了同一张 RealMap 的原始 `map_a.pgm` / `map_a.yaml`，已复制为 `dqn_realmap_a`。",
                "- 为满足 T07 至少 2 张地图加载/显示验收，补入 BSD 许可的 TurtleBot Willow Garage ROS 地图 `willow_garage_0p10`，并在 manifest 中标记为外部开源来源。",
                "",
                "## 可用地图",
                "",
                "| id | source | size | resolution(m/cell) | start_xy | goal_xy | load |",
                "|---|---|---:|---:|---:|---:|---|",
                *rows,
                "",
                "## DQN10 重复快照核查",
                "",
                f"- NPZ 快照数量: {duplicate['npz_count']}",
                f"- 唯一数组哈希数量: {duplicate['unique_array_hashes']}",
                f"- hash_counts: `{duplicate['hash_counts']}`",
                "",
                "## 产物",
                "",
                f"- Manifest: `{(ASSET_ROOT / 'manifest.json').relative_to(REPO_ROOT)}`",
                f"- Overview preview: `{(ASSET_ROOT / 'preview_overview.png').relative_to(REPO_ROOT)}`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    dqn_yaml = copy_dqn_realmap()
    willow_yaml = copy_willow_map()

    maps = [
        validate_map(
            "dqn_realmap_a",
            dqn_yaml,
            source={
                "label": "DQN9 original PGM/YAML + DQN10 realmap_a lineage",
                "local_source_pgm": str((DQN9_REALMAP_DIR / "map_a.pgm")),
                "local_source_yaml": str((DQN9_REALMAP_DIR / "map_a.yaml")),
                "dqn10_fallback_maps": str(DQN10_FALLBACK_MAPS),
            },
            start_xy=DQN_CANONICAL_START,
            goal_xy=DQN_CANONICAL_GOAL,
        ),
        validate_map(
            "willow_garage_0p10",
            willow_yaml,
            source={
                "label": "TurtleBot navigation Willow Garage map",
                "source_page": WILLOW_SOURCE_PAGE,
                "pgm_url": WILLOW_PGM_URL,
                "yaml_url": WILLOW_YAML_URL,
                "license": "BSD per turtlebot_navigation/package.xml",
            },
        ),
    ]

    render_overview(
        [ASSET_ROOT / item["id"] / "preview.png" for item in maps],
        ASSET_ROOT / "preview_overview.png",
    )
    manifest = {
        "schema": "forest_n3p_realmap_inventory_v1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "usable_map_count": len(maps),
        "acceptance": "pass_two_maps_load_and_preview",
        "loader": "forest_n3p.maps.pgm.load_pgm_yaml_map",
        "maps": maps,
        "dqn10_duplicate_check": dqn10_duplicate_summary(),
    }
    (ASSET_ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_readme(manifest)
    write_report(manifest)
    print(json.dumps({"usable_map_count": len(maps), "asset_root": str(ASSET_ROOT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
