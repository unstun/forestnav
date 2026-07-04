from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from forest_n3p.rl_rs.obs import ObservationConfig, RlRsObservation
from forest_n3p.rl_rs.operator import RlRsFunnelOperator
from forest_n3p.rl_rs.training_logging import file_sha256


@dataclass(frozen=True)
class Sb3RlRsActionPolicy:
    model: Any
    checkpoint_path: str
    checkpoint_sha256: str
    deterministic: bool = True

    def __call__(self, observation: RlRsObservation) -> float:
        if observation.patch is None:
            raise RuntimeError("RL-RS checkpoint policy requires patch observations")
        obs = {
            "scalar": np.asarray(observation.scalar, dtype=np.float32),
            "patch": np.asarray(observation.patch, dtype=np.float32),
        }
        action, _state = self.model.predict(obs, deterministic=bool(self.deterministic))
        return _single_normalized_action(action)


def load_rl_rs_funnel_operator_from_checkpoint(
    checkpoint_path: str | Path,
    *,
    device: str = "auto",
    deterministic: bool = True,
    observation_config: ObservationConfig | None = None,
    max_steps: int = 32,
    action_step_m: float = 0.3,
    collision_sample_step_m: float | None = None,
    terminal_check_every: int = 1,
    no_progress_patience: int = 3,
    name: str = "rl_rs_funnel_ppo",
) -> RlRsFunnelOperator:
    path = Path(checkpoint_path)
    if not path.exists():
        raise FileNotFoundError(f"RL-RS checkpoint does not exist: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"RL-RS checkpoint is not a file: {path}")

    from stable_baselines3 import PPO

    sha256 = file_sha256(path)
    model = PPO.load(path, device=str(device))
    policy = Sb3RlRsActionPolicy(
        model=model,
        checkpoint_path=str(path),
        checkpoint_sha256=sha256,
        deterministic=bool(deterministic),
    )
    return RlRsFunnelOperator(
        action_policy=policy,
        max_steps=int(max_steps),
        action_step_m=float(action_step_m),
        collision_sample_step_m=collision_sample_step_m,
        terminal_check_every=int(terminal_check_every),
        no_progress_patience=int(no_progress_patience),
        observation_config=observation_config or ObservationConfig(),
        name=str(name),
        checkpoint_path=str(path),
        checkpoint_sha256=sha256,
    )


def _single_normalized_action(action: Any) -> float:
    array = np.asarray(action, dtype=np.float32)
    if array.shape == ():
        value = float(array.item())
    else:
        flat = array.reshape(-1)
        if flat.shape != (1,):
            raise ValueError("RL-RS checkpoint policy must emit exactly one steering action")
        value = float(flat[0])
    return max(-1.0, min(1.0, value))
