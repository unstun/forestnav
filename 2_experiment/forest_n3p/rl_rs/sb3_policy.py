from __future__ import annotations

from typing import Any

import gymnasium as gym
import torch
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


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
