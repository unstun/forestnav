from __future__ import annotations

from typing import Any

import gymnasium as gym
import torch
import torch.nn.functional as F
from stable_baselines3.common.policies import MultiInputActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class TanhLinearActionHead(torch.nn.Module):
    """Action head that preserves the F02 BC policy's normalized tanh output."""

    def __init__(self, in_features: int, out_features: int) -> None:
        super().__init__()
        self.linear = torch.nn.Linear(int(in_features), int(out_features))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return torch.tanh(self.linear(features))


class RlRsMultiInputPolicy(MultiInputActorCriticPolicy):
    """SB3 MultiInput policy with an optional serializable tanh action head."""

    def __init__(self, *args: Any, use_tanh_action_head: bool = False, **kwargs: Any) -> None:
        self.use_tanh_action_head = bool(use_tanh_action_head)
        super().__init__(*args, **kwargs)

    def _build(self, lr_schedule: Any) -> None:
        super()._build(lr_schedule)
        if not bool(self.use_tanh_action_head):
            return
        old_action_net = self.action_net
        self.action_net = TanhLinearActionHead(old_action_net.in_features, old_action_net.out_features).to(old_action_net.weight.device)
        self.optimizer = self.optimizer_class(self.parameters(), lr=lr_schedule(1), **self.optimizer_kwargs)


class RlRsObstacleSummaryExtractor(BaseFeaturesExtractor):
    """SB3 feature extractor aligned with the F02 obstacle-summary BC features."""

    def __init__(
        self,
        observation_space: gym.Space,
        *,
        feature_mean: list[float] | tuple[float, ...] | None = None,
        feature_std: list[float] | tuple[float, ...] | None = None,
    ) -> None:
        if not isinstance(observation_space, gym.spaces.Dict):
            raise TypeError("RlRsObstacleSummaryExtractor requires a Dict observation space")
        scalar_space = observation_space.spaces.get("scalar")
        patch_space = observation_space.spaces.get("patch")
        if scalar_space is None or patch_space is None:
            raise ValueError("observation space must contain scalar and patch entries")
        scalar_dim = int(scalar_space.shape[0])
        patch_shape = tuple(int(value) for value in patch_space.shape)
        if len(patch_shape) != 3:
            raise ValueError("patch observation must have shape (channels, cells, cells)")
        _channels, cells_y, cells_x = patch_shape
        features_dim = scalar_dim + 21
        super().__init__(observation_space, features_dim=features_dim)

        masks = _region_masks(cells_y, cells_x)
        self.register_buffer("_region_masks", masks, persistent=False)
        self.register_buffer("_region_counts", masks.sum(dim=(1, 2)).clamp_min(1.0), persistent=False)
        self._has_normalization = feature_mean is not None or feature_std is not None
        mean = _feature_vector(feature_mean, features_dim=features_dim, fill=0.0)
        std = _feature_vector(feature_std, features_dim=features_dim, fill=1.0).clamp_min(1e-6)
        self.register_buffer("_feature_mean", mean, persistent=False)
        self.register_buffer("_feature_std", std, persistent=False)

    def forward(self, observations: dict[str, torch.Tensor]) -> torch.Tensor:
        scalar = observations["scalar"].float().reshape(observations["scalar"].shape[0], -1)
        patch = observations["patch"].float()
        if patch.ndim != 4:
            raise ValueError("batched patch observation must have shape (batch, channels, cells, cells)")
        occupancy = patch[:, 0, :, :]
        edt = patch[:, 1, :, :] if patch.shape[1] > 1 else 1.0 - occupancy
        masks = self._region_masks.to(device=patch.device, dtype=patch.dtype)
        counts = self._region_counts.to(device=patch.device, dtype=patch.dtype)

        occ_mean = (occupancy[:, None, :, :] * masks[None, :, :, :]).sum(dim=(2, 3)) / counts
        edt_mean = (edt[:, None, :, :] * masks[None, :, :, :]).sum(dim=(2, 3)) / counts
        outside = torch.full_like(edt[:, None, :, :], torch.inf)
        edt_masked = torch.where(masks[None, :, :, :] > 0.0, edt[:, None, :, :], outside)
        edt_min = edt_masked.amin(dim=(2, 3))
        edt_min = torch.where(torch.isfinite(edt_min), edt_min, torch.zeros_like(edt_min))

        region_features = torch.stack((occ_mean, edt_min, edt_mean), dim=2).reshape(patch.shape[0], -1)
        features = torch.cat((scalar, region_features), dim=1)
        if bool(self._has_normalization):
            mean = self._feature_mean.to(device=features.device, dtype=features.dtype)
            std = self._feature_std.to(device=features.device, dtype=features.dtype)
            features = (features - mean) / std
        return features


class RlRsPatchCnnExtractor(BaseFeaturesExtractor):
    """CNN feature extractor consuming the raw occupancy/EDT patch.

    Unlike RlRsObstacleSummaryExtractor (21 hand-pooled region statistics), this
    keeps the full patch geometry: patch -> padded stride-2 conv stack ->
    cnn_output_dim features, scalar -> fixed elementwise scaling, then concat.
    The padded 3x3 convolutions stay valid down to tiny smoke patches (5x5).
    """

    def __init__(
        self,
        observation_space: gym.Space,
        *,
        cnn_output_dim: int = 256,
        scalar_scale: list[float] | tuple[float, ...] | None = None,
    ) -> None:
        if not isinstance(observation_space, gym.spaces.Dict):
            raise TypeError("RlRsPatchCnnExtractor requires a Dict observation space")
        scalar_space = observation_space.spaces.get("scalar")
        patch_space = observation_space.spaces.get("patch")
        if scalar_space is None or patch_space is None:
            raise ValueError("observation space must contain scalar and patch entries")
        scalar_dim = int(scalar_space.shape[0])
        patch_shape = tuple(int(value) for value in patch_space.shape)
        if len(patch_shape) != 3:
            raise ValueError("patch observation must have shape (channels, cells, cells)")
        if int(cnn_output_dim) <= 0:
            raise ValueError("cnn_output_dim must be positive")
        features_dim = scalar_dim + int(cnn_output_dim)
        super().__init__(observation_space, features_dim=features_dim)

        channels = patch_shape[0]
        self.cnn = torch.nn.Sequential(
            torch.nn.Conv2d(channels, 32, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
        )
        with torch.no_grad():
            n_flatten = int(self.cnn(torch.zeros((1, *patch_shape), dtype=torch.float32)).shape[1])
        self.linear = torch.nn.Sequential(
            torch.nn.Linear(n_flatten, int(cnn_output_dim)),
            torch.nn.ReLU(),
        )
        scale = _feature_vector(scalar_scale, features_dim=scalar_dim, fill=1.0)
        self.register_buffer("_scalar_scale", scale, persistent=False)

    def forward(self, observations: dict[str, torch.Tensor]) -> torch.Tensor:
        scalar = observations["scalar"].float().reshape(observations["scalar"].shape[0], -1)
        scale = self._scalar_scale.to(device=scalar.device, dtype=scalar.dtype)
        patch = observations["patch"].float()
        if patch.ndim != 4:
            raise ValueError("batched patch observation must have shape (batch, channels, cells, cells)")
        return torch.cat((scalar * scale, self.linear(self.cnn(patch))), dim=1)


class RlRsPatchTransformerExtractor(BaseFeaturesExtractor):
    """Patch-transformer extractor consuming the raw occupancy/EDT patch."""

    def __init__(
        self,
        observation_space: gym.Space,
        *,
        scalar_scale: list[float] | tuple[float, ...] | None = None,
    ) -> None:
        if not isinstance(observation_space, gym.spaces.Dict):
            raise TypeError("RlRsPatchTransformerExtractor requires a Dict observation space")
        scalar_space = observation_space.spaces.get("scalar")
        patch_space = observation_space.spaces.get("patch")
        if scalar_space is None or patch_space is None:
            raise ValueError("observation space must contain scalar and patch entries")
        scalar_dim = int(scalar_space.shape[0])
        patch_shape = tuple(int(value) for value in patch_space.shape)
        if len(patch_shape) != 3:
            raise ValueError("patch observation must have shape (channels, cells, cells)")
        output_dim = 256
        super().__init__(observation_space, features_dim=scalar_dim + output_dim)

        channels = patch_shape[0]
        embed_dim = 128
        self.patchify = torch.nn.Conv2d(channels, embed_dim, kernel_size=8, stride=8)
        self.pos_embedding = torch.nn.Parameter(torch.zeros(1, 64, embed_dim))
        encoder_layer = torch.nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=4,
            dim_feedforward=256,
            batch_first=True,
            norm_first=True,
        )
        self.transformer = torch.nn.TransformerEncoder(encoder_layer, num_layers=2)
        self.projection = torch.nn.Sequential(
            torch.nn.Linear(embed_dim, output_dim),
            torch.nn.ReLU(),
        )
        scale = _feature_vector(scalar_scale, features_dim=scalar_dim, fill=1.0)
        self.register_buffer("_scalar_scale", scale, persistent=False)

    def forward(self, observations: dict[str, torch.Tensor]) -> torch.Tensor:
        scalar = observations["scalar"].float().reshape(observations["scalar"].shape[0], -1)
        scale = self._scalar_scale.to(device=scalar.device, dtype=scalar.dtype)
        patch = observations["patch"].float()
        if patch.ndim != 4:
            raise ValueError("batched patch observation must have shape (batch, channels, cells, cells)")
        if tuple(patch.shape[-2:]) != (64, 64):
            patch = F.interpolate(patch, size=(64, 64), mode="bilinear", align_corners=False)
        tokens = self.patchify(patch).flatten(2).transpose(1, 2)
        tokens = tokens + self.pos_embedding.to(device=tokens.device, dtype=tokens.dtype)
        patch_features = self.projection(self.transformer(tokens).mean(dim=1))
        return torch.cat((scalar * scale, patch_features), dim=1)


def _region_masks(cells_y: int, cells_x: int) -> torch.Tensor:
    x_axis = _normalized_axis(cells_x)
    y_axis = _normalized_axis(cells_y)
    yy, xx = torch.meshgrid(y_axis, x_axis, indexing="ij")
    masks = (
        torch.ones_like(xx, dtype=torch.bool),
        xx >= 0.0,
        (xx >= 0.0) & (xx <= 0.5) & (torch.abs(yy) <= 0.35),
        (xx > 0.5) & (torch.abs(yy) <= 0.5),
        (xx >= 0.0) & (yy > 0.0),
        (xx >= 0.0) & (yy < 0.0),
        (xx >= 0.0) & (torch.abs(yy) <= 0.15),
    )
    return torch.stack([mask.to(dtype=torch.float32) for mask in masks], dim=0)


def _normalized_axis(size: int) -> torch.Tensor:
    if int(size) <= 1:
        return torch.zeros((int(size),), dtype=torch.float32)
    center = (float(size) - 1.0) / 2.0
    return ((torch.arange(int(size), dtype=torch.float32) - center) / max(center, 1.0)).to(dtype=torch.float32)


def _feature_vector(values: Any, *, features_dim: int, fill: float) -> torch.Tensor:
    if values is None:
        return torch.full((int(features_dim),), float(fill), dtype=torch.float32)
    tensor = torch.as_tensor(values, dtype=torch.float32).reshape(-1)
    if int(tensor.numel()) != int(features_dim):
        raise ValueError(f"feature normalization vector must have {features_dim} values")
    return tensor
