import numpy as np

from forest_n3p.scripts.train_bc_policy import (
    _obstacle_summary_features,
    _policy_features_from_scalar_and_patch,
)


def test_obstacle_summary_features_have_region_triplets():
    patch = np.zeros((2, 5, 5), dtype=np.float32)
    patch[1] = 1.0

    features = _obstacle_summary_features(patch)

    assert features.shape == (21,)
    assert np.all(np.isfinite(features))
    assert np.allclose(features[0::3], 0.0)
    assert np.allclose(features[1::3], 1.0)
    assert np.allclose(features[2::3], 1.0)


def test_obstacle_summary_features_change_with_front_obstacle():
    scalar = np.arange(8, dtype=np.float32)
    free_patch = np.zeros((2, 5, 5), dtype=np.float32)
    free_patch[1] = 1.0
    blocked_patch = free_patch.copy()
    blocked_patch[0, 2, 4] = 1.0
    blocked_patch[1, 2, 4] = 0.0

    free = _policy_features_from_scalar_and_patch(scalar, free_patch, feature_mode="obstacle_summary")
    blocked = _policy_features_from_scalar_and_patch(scalar, blocked_patch, feature_mode="obstacle_summary")

    assert free.shape == (29,)
    assert np.allclose(free[:8], scalar)
    assert blocked[8] > free[8]
    assert blocked[9] < free[9]
