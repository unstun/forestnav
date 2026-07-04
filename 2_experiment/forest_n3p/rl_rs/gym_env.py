from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from forest_n3p.rl_rs.actions import SteeringAction
from forest_n3p.rl_rs.env import AnalyticExpansionContext, AnalyticExpansionEnv
from forest_n3p.rl_rs.obs import ObservationConfig, RlRsObservation

ContextSampler = Callable[[np.random.Generator], AnalyticExpansionContext]


@dataclass(frozen=True)
class StaticContextSampler:
    context: AnalyticExpansionContext

    def __call__(self, _rng: np.random.Generator) -> AnalyticExpansionContext:
        return self.context


class GymAnalyticExpansionEnv(gym.Env):
    """Gymnasium adapter for the planner-side RL-RS analytic expansion env."""

    metadata = {"render_modes": []}

    def __init__(
        self,
        context_sampler: ContextSampler,
        *,
        observation_config: ObservationConfig | None = None,
    ) -> None:
        super().__init__()
        self.context_sampler = context_sampler
        self.observation_config = observation_config or ObservationConfig()
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Dict(
            {
                "scalar": spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32),
                "patch": spaces.Box(
                    low=0.0,
                    high=1.0,
                    shape=_patch_shape(self.observation_config),
                    dtype=np.float32,
                ),
            }
        )
        self._planner_env = AnalyticExpansionEnv()
        self._context: AnalyticExpansionContext | None = None

    @property
    def planner_env(self) -> AnalyticExpansionEnv:
        return self._planner_env

    @property
    def context(self) -> AnalyticExpansionContext | None:
        return self._context

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
        super().reset(seed=seed)
        context = _context_from_options(options) or self.context_sampler(self.np_random)
        context = replace(context, observation_config=self.observation_config)
        self._context = context
        observation = self._planner_env.reset(context)
        info: dict[str, Any] = {"context": context}
        curriculum = _sampler_curriculum_record(self.context_sampler)
        if curriculum is not None:
            info["curriculum"] = curriculum
        return _observation_to_dict(observation), info

    def step(self, action: np.ndarray | list[float] | tuple[float, ...] | float):
        normalized_steering = _single_action_value(action)
        step = self._planner_env.step(SteeringAction(normalized_steering, normalized=True))
        observation = _observation_to_dict(step.observation)
        reward = float(step.reward.total)
        terminated = bool(step.terminated)
        truncated = bool(step.truncated)
        info = dict(step.info)
        return observation, reward, terminated, truncated, info


def _context_from_options(options: dict[str, Any] | None) -> AnalyticExpansionContext | None:
    if not options:
        return None
    context = options.get("context")
    if context is None:
        return None
    if not isinstance(context, AnalyticExpansionContext):
        raise TypeError("reset options['context'] must be an AnalyticExpansionContext")
    return context


def _sampler_curriculum_record(context_sampler: Any) -> dict[str, Any] | None:
    metadata = getattr(context_sampler, "last_metadata", None)
    if metadata is None:
        return None
    to_record = getattr(metadata, "to_record", None)
    if callable(to_record):
        return dict(to_record())
    return None


def _single_action_value(action: np.ndarray | list[float] | tuple[float, ...] | float) -> float:
    array = np.asarray(action, dtype=np.float32)
    if array.shape == ():
        return float(array.item())
    flat = array.reshape(-1)
    if flat.shape != (1,):
        raise ValueError("GymAnalyticExpansionEnv action must contain exactly one steering value")
    return float(flat[0])


def _observation_to_dict(observation: RlRsObservation) -> dict[str, np.ndarray]:
    if observation.patch is None:
        raise RuntimeError("GymAnalyticExpansionEnv requires patch observations")
    return {
        "scalar": np.asarray(observation.scalar, dtype=np.float32),
        "patch": np.asarray(observation.patch, dtype=np.float32),
    }


def _patch_shape(config: ObservationConfig) -> tuple[int, int, int]:
    channels = 2 if bool(config.include_edt) else 1
    cells = int(config.patch_cells)
    return (channels, cells, cells)
