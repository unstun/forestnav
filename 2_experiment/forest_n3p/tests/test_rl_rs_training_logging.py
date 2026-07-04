import csv
import json

import numpy as np

from forest_n3p.rl_rs import ObservationConfig
from forest_n3p.rl_rs.curriculum import CurriculumContextConfig, OpenConnectorContextSampler
from forest_n3p.rl_rs.gym_env import GymAnalyticExpansionEnv
from forest_n3p.rl_rs.training_logging import RlRsEpisodeLoggingWrapper, file_sha256, write_training_manifest


class FakeSummaryWriter:
    def __init__(self):
        self.scalars = []
        self.closed = False

    def add_scalar(self, tag, scalar_value, global_step):
        self.scalars.append((tag, float(scalar_value), int(global_step)))

    def close(self):
        self.closed = True


def _small_config():
    return CurriculumContextConfig(
        max_steps=4,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
        terminal_check_every=1,
        theta_bins=32,
        observation_config=ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True, edt_clip_m=1.0),
    )


def _open_logging_env(csv_path, writer=None):
    cfg = _small_config()
    sampler = OpenConnectorContextSampler(config=cfg)
    env = GymAnalyticExpansionEnv(sampler, observation_config=cfg.observation_config)
    return RlRsEpisodeLoggingWrapper(env, csv_path=csv_path, tensorboard_writer=writer)


def test_env_step_info_exposes_raw_metrics_needed_for_episode_logging(tmp_path):
    env = _open_logging_env(tmp_path / "episodes.csv")

    env.reset(seed=7)
    _obs, _reward, _terminated, _truncated, info = env.step(np.array([0.0], dtype=np.float32))

    assert info["rollout_path_length_m"] > 0.0
    assert info["min_clearance_m"] is not None
    assert info["curvature_delta_abs"] == 0.0


def test_episode_logging_wrapper_writes_csv_with_curriculum_reward_and_outcome_fields(tmp_path):
    csv_path = tmp_path / "episodes.csv"
    env = _open_logging_env(csv_path)

    env.reset(seed=3)
    done = False
    while not done:
        _obs, _reward, terminated, truncated, _info = env.step(np.array([0.0], dtype=np.float32))
        done = bool(terminated or truncated)
    env.close()

    rows = list(csv.DictReader(csv_path.open(newline="", encoding="utf-8")))
    assert len(rows) == 1
    row = rows[0]
    assert row["episode_index"] == "0"
    assert row["curriculum_stage"] == "open_connector"
    assert row["curriculum_source"] == "procedural_empty_grid"
    assert row["terminal_rs_success"] == "True"
    assert row["collision"] == "False"
    assert float(row["reward_total"]) > 0.0
    assert float(row["reward_term_success"]) > 0.0
    assert float(row["rollout_length_m"]) > 0.0
    assert float(row["mean_abs_curvature_rate"]) == 0.0
    assert row["failure_reason"] == ""


def test_episode_logging_wrapper_emits_tensorboard_scalars_when_writer_is_supplied(tmp_path):
    writer = FakeSummaryWriter()
    env = _open_logging_env(tmp_path / "episodes.csv", writer=writer)

    env.reset(seed=5)
    done = False
    while not done:
        _obs, _reward, terminated, truncated, _info = env.step(np.array([0.0], dtype=np.float32))
        done = bool(terminated or truncated)
    env.close()

    tags = {tag for tag, _value, _step in writer.scalars}
    assert "episode/reward_total" in tags
    assert "episode/terminal_rs_success" in tags
    assert "episode/rollout_length_m" in tags
    assert "episode/reward_term_success" in tags
    assert writer.closed


def test_training_manifest_records_config_source_hashes_and_checkpoints(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("rl-rs logging source\n", encoding="utf-8")

    manifest_path = write_training_manifest(
        tmp_path,
        config={"algo": "ppo", "seed": 20260704},
        source_hashes={"source.txt": file_sha256(source)},
        checkpoints=[{"path": "checkpoint_0001.zip", "step": 1}],
        command="python -m forest_n3p.scripts.train_rl_rs_ppo --smoke",
    )

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["config"]["algo"] == "ppo"
    assert payload["source_hashes"]["source.txt"] == file_sha256(source)
    assert payload["checkpoints"][0]["path"] == "checkpoint_0001.zip"
    assert payload["command"].startswith("python -m")
