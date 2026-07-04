import os
from pathlib import Path

import numpy as np
import pytest

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from forest_n3p.rl_rs import ObservationConfig, build_observation
from forest_n3p.rl_rs.checkpoint_operator import load_rl_rs_funnel_operator_from_checkpoint
from forest_n3p.rl_rs.operator import RlRsFunnelOperator
from forest_n3p.scripts.train_rl_rs_ppo import main as train_rl_rs_ppo_main
from forest_n3p.third_party.pathplan import AckermannState, GridMap


def test_missing_rl_rs_checkpoint_hard_fails_without_fallback(tmp_path):
    missing = tmp_path / "missing_rl_rs_model.zip"

    with pytest.raises(FileNotFoundError, match="RL-RS checkpoint does not exist"):
        load_rl_rs_funnel_operator_from_checkpoint(missing)


def test_rl_rs_checkpoint_operator_loads_smoke_model_and_predicts_real_observation(tmp_path):
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
    checkpoint = tmp_path / "final_model.zip"

    operator = load_rl_rs_funnel_operator_from_checkpoint(
        checkpoint,
        device="cpu",
        observation_config=ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True),
        max_steps=4,
    )
    observation = build_observation(
        AckermannState(1.0, 1.0, 0.0),
        AckermannState(1.3, 1.0, 0.0),
        remaining_steps=4,
        grid_map=GridMap(np.zeros((30, 30), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0)),
        config=ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True),
    )

    action = operator.action_policy(observation)

    assert rc == 0
    assert checkpoint.exists()
    assert isinstance(operator, RlRsFunnelOperator)
    assert operator.checkpoint_path == str(checkpoint)
    assert operator.checkpoint_sha256
    assert np.isfinite(float(action))
    assert -1.0 <= float(action) <= 1.0
