import csv
import json
import os

import numpy as np

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
from gymnasium import spaces

from forest_n3p.rl_rs.sb3_policy import RlRsObstacleSummaryExtractor
from forest_n3p.scripts.train_bc_policy import _policy_features_from_scalar_and_patch
from forest_n3p.scripts.train_rl_rs_ppo import main as train_rl_rs_ppo_main


def test_obstacle_summary_extractor_matches_bc_feature_semantics():
    observation_space = spaces.Dict(
        {
            "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
            "patch": spaces.Box(low=0.0, high=1.0, shape=(2, 5, 5), dtype=np.float32),
        }
    )
    extractor = RlRsObstacleSummaryExtractor(observation_space)
    scalar = np.arange(8, dtype=np.float32)
    patch = np.zeros((2, 5, 5), dtype=np.float32)
    patch[1] = 1.0
    patch[0, 2, 4] = 1.0
    patch[1, 2, 4] = 0.0

    with torch.no_grad():
        features = extractor(
            {
                "scalar": torch.as_tensor(scalar.reshape(1, -1), dtype=torch.float32),
                "patch": torch.as_tensor(patch.reshape(1, 2, 5, 5), dtype=torch.float32),
            }
        ).detach().cpu().numpy()[0]

    expected = _policy_features_from_scalar_and_patch(scalar, patch, feature_mode="obstacle_summary")
    assert features.shape == (29,)
    assert np.allclose(features, expected, atol=1e-6)


def test_train_rl_rs_ppo_smoke_writes_model_manifest_and_episode_csv(tmp_path):
    rc = train_rl_rs_ppo_main(
        [
            "--allow-duplicate-openmp",
            "--smoke",
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )

    assert rc == 0
    assert (tmp_path / "final_model.zip").exists()
    assert (tmp_path / "training_manifest.json").exists()
    assert (tmp_path / "summary.json").exists()

    manifest = json.loads((tmp_path / "training_manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["config"]["smoke"] is True
    assert manifest["config"]["policy"] == "MultiInputPolicy"
    assert "2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py" in manifest["source_hashes"]
    assert any(checkpoint["path"] == "final_model.zip" for checkpoint in manifest["checkpoints"])

    episode_csv = tmp_path / "episodes_env0.csv"
    rows = list(csv.DictReader(episode_csv.open(newline="", encoding="utf-8")))
    assert rows
    assert {"reward_total", "terminal_rs_success", "rollout_length_m"}.issubset(rows[0])
