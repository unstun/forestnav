from __future__ import annotations

import numpy as np

from forest_n3p.maps.pgm import load_pgm_yaml_map, load_ros_map_yaml


def test_load_ros_map_yaml_resolves_relative_pgm_and_thresholds(tmp_path) -> None:
    pgm_path = tmp_path / "tiny.pgm"
    pgm_path.write_bytes(
        b"P5\n4 3\n255\n"
        + bytes(
            [
                254,
                254,
                0,
                205,
                254,
                0,
                254,
                254,
                254,
                254,
                254,
                254,
            ]
        )
    )
    yaml_path = tmp_path / "tiny.yaml"
    yaml_path.write_text(
        "\n".join(
            [
                "image: tiny.pgm",
                "resolution: 0.05",
                "origin: [1.0, 2.0, 0.0]",
                "negate: 0",
                "occupied_thresh: 0.65",
                "free_thresh: 0.196",
            ]
        ),
        encoding="utf-8",
    )

    meta = load_ros_map_yaml(yaml_path)
    spec = load_pgm_yaml_map(yaml_path, (0, 0), (3, 2), name="tiny")

    assert meta.image_path == pgm_path
    assert meta.resolution == 0.05
    assert meta.origin == (1.0, 2.0, 0.0)
    assert spec.size == (4, 3)
    assert spec.start_xy == (0, 0)
    assert spec.goal_xy == (3, 2)
    assert np.array_equal(
        spec.obstacle_grid(),
        np.asarray(
            [
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 1],
            ],
            dtype=np.uint8,
        ),
    )
