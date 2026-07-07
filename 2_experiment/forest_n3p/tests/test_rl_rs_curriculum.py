import math

import numpy as np
import pandas as pd

from forest_n3p.rl_rs import ObservationConfig
from forest_n3p.rl_rs.curriculum import (
    CurriculumContextConfig,
    HeldoutQueryContextSampler,
    ObstacleBypassContextSampler,
    OpenConnectorContextSampler,
    OracleConnectorContextSampler,
    WeightedCurriculumContextSampler,
)
from forest_n3p.rl_rs.gym_env import GymAnalyticExpansionEnv


def _small_config():
    return CurriculumContextConfig(
        max_steps=6,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
        terminal_check_every=1,
        theta_bins=32,
        observation_config=ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True, edt_clip_m=1.0),
    )


def test_open_connector_sampler_returns_noncolliding_context_with_metadata():
    sampler = OpenConnectorContextSampler(config=_small_config())

    context = sampler(np.random.default_rng(7))

    checker = context.collision_checker()
    assert not checker.collides_pose(context.start.x, context.start.y, context.start.theta)
    assert not checker.collides_pose(context.goal.x, context.goal.y, context.goal.theta)
    assert np.count_nonzero(context.grid_map.data) == 0
    assert sampler.last_metadata is not None
    assert sampler.last_metadata.stage == "open_connector"
    assert sampler.last_metadata.source == "procedural_empty_grid"


def test_obstacle_bypass_sampler_places_obstacle_near_connector_without_colliding_start_or_goal():
    sampler = ObstacleBypassContextSampler(config=_small_config())

    context = sampler(np.random.default_rng(11))

    checker = context.collision_checker()
    assert np.count_nonzero(context.grid_map.data) > 0
    assert not checker.collides_pose(context.start.x, context.start.y, context.start.theta)
    assert not checker.collides_pose(context.goal.x, context.goal.y, context.goal.theta)
    assert sampler.last_metadata is not None
    assert sampler.last_metadata.stage == "obstacle_bypass"
    assert sampler.last_metadata.nearest_obstacle_m is not None
    assert sampler.last_metadata.nearest_obstacle_m < 1.0


def test_oracle_connector_sampler_reconstructs_profile_aware_failure_node_context(tmp_path):
    parquet_path = tmp_path / "oracle_rows.parquet"
    pd.DataFrame(
        [
            {
                "query_id": "complex_s00_q0000",
                "difficulty_bucket": "Complex",
                "profile_name": "complex_d02",
                "map_seed": 20360620,
                "query_seed": 20361620,
                "distance_bin_key": "d08_12",
                "dedup_key": "complex_s00_q0000:122:231:69",
                "expansion_idx": 0,
                "state_x": 12.2,
                "state_y": 23.1,
                "state_theta": -0.191184,
                "goal_x": 21.5,
                "goal_y": 21.3,
                "goal_theta": -0.191184,
                "nearest_obstacle_m": 1.655295,
                "oracle_connectable": True,
            }
        ]
    ).to_parquet(parquet_path)
    sampler = OracleConnectorContextSampler(parquet_path, config=_small_config())

    context = sampler(np.random.default_rng(3))

    assert math.isclose(context.start.x, 12.2, abs_tol=1e-9)
    assert math.isclose(context.goal.x, 21.5, abs_tol=1e-9)
    assert context.grid_map.data.shape == (300, 300)
    assert sampler.last_metadata is not None
    assert sampler.last_metadata.stage == "rs_failure_node"
    assert sampler.last_metadata.oracle_connectable is True
    assert sampler.last_metadata.profile_name == "complex_d02"


def test_oracle_connector_sampler_skips_rows_that_reconstruct_to_colliding_context(tmp_path):
    parquet_path = tmp_path / "oracle_rows_with_bad_goal.parquet"
    bad_goal_row = {
        "query_id": "extreme_s00_q0006",
        "difficulty_bucket": "Extreme",
        "profile_name": "extreme_d05",
        "map_seed": 20460621,
        "query_seed": 20461621,
        "distance_bin_key": "d08_12",
        "dedup_key": "extreme_s00_q0006:259:123:0",
        "expansion_idx": 0,
        "state_x": 25.9,
        "state_y": 12.3,
        "state_theta": 0.0,
        "goal_x": 9.3,
        "goal_y": 11.1,
        "goal_theta": 0.0,
        "nearest_obstacle_m": 1.0,
        "oracle_connectable": True,
    }
    good_row = {
        "query_id": "complex_s00_q0000",
        "difficulty_bucket": "Complex",
        "profile_name": "complex_d02",
        "map_seed": 20360620,
        "query_seed": 20361620,
        "distance_bin_key": "d08_12",
        "dedup_key": "complex_s00_q0000:122:231:69",
        "expansion_idx": 1,
        "state_x": 12.2,
        "state_y": 23.1,
        "state_theta": -0.191184,
        "goal_x": 21.5,
        "goal_y": 21.3,
        "goal_theta": -0.191184,
        "nearest_obstacle_m": 1.655295,
        "oracle_connectable": True,
    }
    pd.DataFrame([bad_goal_row, good_row]).to_parquet(parquet_path)
    sampler = OracleConnectorContextSampler(parquet_path, config=_small_config())

    context = sampler(np.random.default_rng(1))

    checker = context.collision_checker()
    assert not checker.collides_pose(context.start.x, context.start.y, context.start.theta)
    assert not checker.collides_pose(context.goal.x, context.goal.y, context.goal.theta)
    assert sampler.last_metadata is not None
    assert sampler.last_metadata.query_id == "complex_s00_q0000"
    assert sampler.skipped_invalid_rows == 1


def test_heldout_query_sampler_uses_heldout_seed_and_records_metadata():
    sampler = HeldoutQueryContextSampler(
        seed=20260704,
        buckets=("Complex",),
        queries_per_bucket=1,
        seed_count=1,
        queries_per_map=1,
        config=_small_config(),
    )

    context = sampler(np.random.default_rng(5))

    assert context.grid_map.data.shape == (300, 300)
    assert sampler.last_metadata is not None
    assert sampler.last_metadata.stage == "heldout_procedural"
    assert sampler.last_metadata.difficulty_bucket == "Complex"
    assert sampler.last_metadata.map_seed != 20360620


def test_heldout_query_sampler_skips_queries_that_reconstruct_to_colliding_context():
    sampler = HeldoutQueryContextSampler(seed=20260706, config=CurriculumContextConfig())

    context = sampler(np.random.default_rng(4))

    checker = context.collision_checker()
    assert not checker.collides_pose(context.start.x, context.start.y, context.start.theta)
    assert not checker.collides_pose(context.goal.x, context.goal.y, context.goal.theta)
    assert sampler.last_metadata is not None
    assert sampler.last_metadata.query_id != "extreme_s00_q0004"
    assert sampler.skipped_invalid_queries == 1


def test_weighted_curriculum_metadata_is_exposed_by_gym_reset():
    sampler = WeightedCurriculumContextSampler(
        stages=(OpenConnectorContextSampler(config=_small_config()),),
        weights=(1.0,),
    )
    env = GymAnalyticExpansionEnv(sampler, observation_config=_small_config().observation_config)

    _obs, info = env.reset(seed=19)

    assert info["curriculum"]["stage"] == "open_connector"
    assert info["curriculum"]["source"] == "procedural_empty_grid"
