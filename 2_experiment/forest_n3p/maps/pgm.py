"""加载 ROS 规范的 PGM/YAML 占据地图到 ArrayGridMapSpec。"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from forest_n3p.maps import ArrayGridMapSpec


@dataclass(frozen=True)
class RosMapYaml:
    """ROS map_server YAML metadata needed by the PGM loader."""

    yaml_path: Path
    image_path: Path
    resolution: float
    origin: tuple[float, float, float]
    occupied_thresh: float
    free_thresh: float
    negate: bool


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if value in {"", "null", "Null", "NULL"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value.strip("\"'")


def load_ros_map_yaml(yaml_path: str | Path) -> RosMapYaml:
    """读取 ROS map_server YAML。

    这里故意只支持 map_server 常用的扁平键值格式，避免为实验资产加载引入
    额外 YAML 依赖。若后续地图使用复杂 YAML，应改用 PyYAML 并补测试。
    """
    yaml_path = Path(yaml_path)
    data: dict[str, object] = {}
    for raw_line in yaml_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = _parse_scalar(value)

    missing = {
        key
        for key in ("image", "resolution", "occupied_thresh", "free_thresh", "negate")
        if key not in data
    }
    if missing:
        raise ValueError(f"ROS map YAML missing keys {sorted(missing)}: {yaml_path}")

    image_value = data["image"]
    if not isinstance(image_value, str):
        raise ValueError(f"ROS map YAML image must be a string: {yaml_path}")
    image_path = Path(image_value)
    if not image_path.is_absolute():
        image_path = yaml_path.parent / image_path

    origin_raw = data.get("origin", (0.0, 0.0, 0.0))
    if not isinstance(origin_raw, (list, tuple)) or len(origin_raw) != 3:
        raise ValueError(f"ROS map YAML origin must contain 3 values: {yaml_path}")

    return RosMapYaml(
        yaml_path=yaml_path,
        image_path=image_path,
        resolution=float(data["resolution"]),
        origin=tuple(float(v) for v in origin_raw),  # type: ignore[arg-type]
        occupied_thresh=float(data["occupied_thresh"]),
        free_thresh=float(data["free_thresh"]),
        negate=bool(int(data["negate"])),
    )


def load_pgm_map(
    pgm_path: str | Path,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    *,
    name: str = "pgm_map",
    occupied_thresh: float = 0.65,
    free_thresh: float | None = None,
    negate: bool = False,
    unknown_as_occupied: bool = False,
) -> ArrayGridMapSpec:
    """加载 ROS 规范的 PGM 占据地图到 ArrayGridMapSpec。

    ROS 规范（negate=False）：
      - 像素越亮 → 越自由（p = pixel/255，低 p = 占据）
      - pixel==0   → p=0.0 < free_thresh  → 占据
      - pixel==254 → p≈1.0 > free_thresh  → 自由

    转换为栅格（y=0 在底部，1=障碍物）：
      当 (1 - pixel/255) > occupied_thresh 时判为占据（即 pixel < (1-thresh)*255）

    Args:
        pgm_path: .pgm 文件路径
        start_xy: 栅格坐标 (x, y)（y=0 在底部）
        goal_xy:  栅格坐标 (x, y)（y=0 在底部）
        name:     地图标识符
        occupied_thresh: .yaml 中的 ROS occupied_thresh（默认 0.65）
        free_thresh: .yaml 中的 ROS free_thresh；为 None 时不单独处理 unknown
        negate:   ROS negate 标志（默认 False）
        unknown_as_occupied: True 时将 ROS unknown cell 视为障碍物
    """
    pgm_path = Path(pgm_path)
    img = cv2.imread(str(pgm_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load PGM: {pgm_path}")

    H, W = img.shape
    # 计算占据概率
    p = img.astype(np.float32) / 255.0
    if negate:
        p = 1.0 - p

    # ROS：占据概率 = 1 - p（越亮 = 越自由）
    occ_prob = 1.0 - p
    obstacle = (occ_prob > float(occupied_thresh)).astype(np.uint8)
    if unknown_as_occupied:
        if free_thresh is None:
            raise ValueError("unknown_as_occupied=True requires free_thresh")
        known_free = occ_prob < float(free_thresh)
        obstacle = np.where(known_free, obstacle, 1).astype(np.uint8)

    # 垂直翻转：图像第0行在顶部；栅格 y=0 在底部
    grid_y0_bottom = np.flipud(obstacle).copy()

    return ArrayGridMapSpec(
        name=name,
        grid_y0_bottom=grid_y0_bottom,
        start_xy=start_xy,
        goal_xy=goal_xy,
    )


def load_pgm_yaml_map(
    yaml_path: str | Path,
    start_xy: tuple[int, int],
    goal_xy: tuple[int, int],
    *,
    name: str | None = None,
    unknown_as_occupied: bool = True,
) -> ArrayGridMapSpec:
    """按 ROS YAML 元数据加载 PGM 占据地图。"""
    meta = load_ros_map_yaml(yaml_path)
    return load_pgm_map(
        meta.image_path,
        start_xy,
        goal_xy,
        name=name or meta.yaml_path.stem,
        occupied_thresh=meta.occupied_thresh,
        free_thresh=meta.free_thresh,
        negate=meta.negate,
        unknown_as_occupied=unknown_as_occupied,
    )
