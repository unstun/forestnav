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


@dataclass(frozen=True)
class BcRlRsActionPolicy:
    model: Any
    torch: Any
    device: Any
    feature_mean: np.ndarray
    feature_std: np.ndarray
    feature_mode: str
    max_steer: float
    checkpoint_path: str
    checkpoint_sha256: str

    def __call__(self, observation: RlRsObservation) -> float:
        from forest_n3p.scripts.train_bc_policy import _policy_features_from_observation

        features = _policy_features_from_observation(observation, feature_mode=str(self.feature_mode)).reshape(1, -1)
        normalized = (features - self.feature_mean.reshape(1, -1)) / self.feature_std.reshape(1, -1)
        with self.torch.no_grad():
            action = self.model(self.torch.as_tensor(normalized, dtype=self.torch.float32, device=self.device))
        physical = float(action.detach().cpu().numpy().reshape(-1)[0])
        return _single_normalized_action(physical / float(self.max_steer))


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


def load_bc_funnel_operator_from_checkpoint(
    checkpoint_path: str | Path,
    *,
    device: str = "auto",
    observation_config: ObservationConfig | None = None,
    max_steps: int = 32,
    action_step_m: float = 0.3,
    collision_sample_step_m: float | None = None,
    terminal_check_every: int = 1,
    no_progress_patience: int = 3,
    name: str = "rl_rs_funnel_bc",
) -> RlRsFunnelOperator:
    path = Path(checkpoint_path)
    if not path.exists():
        raise FileNotFoundError(f"BC checkpoint does not exist: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"BC checkpoint is not a file: {path}")

    from forest_n3p.scripts.train_bc_policy import _build_scalar_steering_mlp, _load_torch, _resolve_device

    torch = _load_torch()
    target_device = _resolve_device(torch, str(device))
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    feature_mode = str(checkpoint["feature_mode"])
    max_steer = float(checkpoint["max_steer"])
    model = _build_scalar_steering_mlp(
        torch=torch,
        input_dim=int(checkpoint["input_dim"]),
        hidden_dims=tuple(int(value) for value in checkpoint["hidden_dims"]),
        max_steer=max_steer,
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.to(target_device)
    model.eval()

    sha256 = file_sha256(path)
    policy = BcRlRsActionPolicy(
        model=model,
        torch=torch,
        device=target_device,
        feature_mean=np.asarray(checkpoint["feature_mean"], dtype=np.float32),
        feature_std=np.asarray(checkpoint["feature_std"], dtype=np.float32),
        feature_mode=feature_mode,
        max_steer=max_steer,
        checkpoint_path=str(path),
        checkpoint_sha256=sha256,
    )
    return RlRsFunnelOperator(
        action_policy=policy,
        max_steps=int(max_steps),
        action_step_m=float(action_step_m),
        collision_sample_step_m=collision_sample_step_m,
        terminal_check_every=int(terminal_check_every),
        no_progress_patience=int(no_progress_patience),
        observation_config=observation_config or _bc_observation_config(checkpoint),
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


def _bc_observation_config(checkpoint: dict[str, Any]) -> ObservationConfig:
    raw = dict(checkpoint.get("observation_config") or {})
    return ObservationConfig(
        patch_size_m=float(raw.get("patch_size_m", 6.4)),
        patch_cells=int(raw.get("patch_cells", 64)),
        include_edt=bool(raw.get("include_edt", True)),
        edt_clip_m=float(raw.get("edt_clip_m", 3.0)),
    )
