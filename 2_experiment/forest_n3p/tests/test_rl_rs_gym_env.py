import math

import numpy as np
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from forest_n3p.rl_rs import AnalyticExpansionContext, ObservationConfig
from forest_n3p.rl_rs.gym_env import GymAnalyticExpansionEnv, StaticContextSampler
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


def _empty_context(
    *,
    goal=(3.0, 1.0, 0.0),
    max_steps=4,
    terminal_check_every=10,
    observation_config=None,
):
    grid_map = GridMap(np.zeros((100, 100), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)
    params = AckermannParams(wheelbase=0.5, min_turn_radius=1.0)
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=32)
    return AnalyticExpansionContext(
        grid_map=grid_map,
        footprint=footprint,
        start=AckermannState(1.0, 1.0, 0.0),
        goal=AckermannState(*goal),
        params=params,
        checker=checker,
        max_steps=max_steps,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
        terminal_check_every=terminal_check_every,
        observation_config=observation_config or ObservationConfig(),
        theta_bins=32,
    )


def test_gym_env_exposes_spaces_and_maps_normalized_action_to_planner_step():
    observation_config = ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True, edt_clip_m=1.0)
    context = _empty_context(observation_config=observation_config)
    env = GymAnalyticExpansionEnv(StaticContextSampler(context), observation_config=observation_config)

    obs, reset_info = env.reset(seed=123)
    assert reset_info["context"] == context
    assert set(obs) == {"scalar", "patch"}
    assert obs["scalar"].shape == (8,)
    assert obs["patch"].shape == (2, 5, 5)
    assert env.observation_space.contains(obs)
    assert env.action_space.contains(np.array([0.5], dtype=np.float32))

    next_obs, reward, terminated, truncated, info = env.step(np.array([0.5], dtype=np.float32))

    assert env.observation_space.contains(next_obs)
    assert isinstance(reward, float)
    assert not terminated
    assert not truncated
    assert info["reward_terms"]["total"] == reward
    assert math.isclose(info["telemetry"].requested_steering_rad, 0.5 * context.params.max_steer, abs_tol=1e-12)


def test_gym_env_passes_sb3_checker_and_dummy_vec_env_smoke():
    context = _empty_context(goal=(4.0, 1.0, 0.0), max_steps=3, observation_config=ObservationConfig())

    def make_env():
        return GymAnalyticExpansionEnv(StaticContextSampler(context), observation_config=context.observation_config)

    check_env(make_env(), warn=False, skip_render_check=True)

    vec_env = DummyVecEnv([make_env, make_env])
    obs = vec_env.reset()
    assert obs["scalar"].shape == (2, 8)
    assert obs["patch"].shape == (2, 2, 64, 64)

    next_obs, rewards, dones, infos = vec_env.step(np.zeros((2, 1), dtype=np.float32))

    assert next_obs["scalar"].shape == (2, 8)
    assert rewards.shape == (2,)
    assert dones.shape == (2,)
    assert len(infos) == 2
