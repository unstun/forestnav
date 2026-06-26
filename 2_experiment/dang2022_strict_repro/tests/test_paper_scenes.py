from __future__ import annotations

import numpy as np


def test_reconstructed_paper_scenes_have_dang2022_map_scale_and_notes():
    from dang2022_strict.scenes import build_scene, list_scene_names

    assert list_scene_names() == ("map_a", "map_b")
    for name in list_scene_names():
        scene = build_scene(name)
        assert scene.name == name
        assert scene.bounds_m == (0.0, 50.0, 0.0, 30.0)
        assert scene.cell_size_m == 1.0
        assert scene.grid.shape == (31, 51)
        assert np.count_nonzero(scene.grid) > 50
        assert "reconstructed" in scene.note.lower()
        assert len(scene.start) == 3
        assert len(scene.goal) == 3


def test_scene_start_and_goal_cells_are_free():
    from dang2022_strict.scenes import build_scene, list_scene_names

    for name in list_scene_names():
        scene = build_scene(name)
        for pose in (scene.start, scene.goal):
            gx = int(round(pose[0] / scene.cell_size_m))
            gy = int(round(pose[1] / scene.cell_size_m))
            assert scene.grid[gy, gx] == 0
