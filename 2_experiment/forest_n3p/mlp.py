from __future__ import annotations

import csv
import json
import math
import random
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

Pose = tuple[float, float, float]


@dataclass(frozen=True)
class MlpNeighborPrediction:
    rank: int
    sample_index: int
    distance: float
    delta_body: Pose
    subgoal_pose: Pose


@dataclass(frozen=True)
class MlpTrainingConfig:
    seed: int = 20260620
    input_dim: int = 41
    hidden_dims: tuple[int, int, int] = (256, 256, 128)
    output_dim: int = 3
    val_fraction: float = 0.10
    batch_size: int = 2048
    epochs: int = 200
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    patience: int = 25
    min_delta: float = 1e-6
    num_workers: int = 0
    zscore_epsilon: float = 1e-6
    device: str = "auto"

    def __post_init__(self) -> None:
        if int(self.input_dim) <= 0 or int(self.output_dim) <= 0:
            raise ValueError("input_dim and output_dim must be positive")
        if len(self.hidden_dims) != 3:
            raise ValueError("T10 MLP must use exactly three hidden Linear layers plus one output Linear layer")
        if any(int(dim) <= 0 for dim in self.hidden_dims):
            raise ValueError("hidden_dims must be positive")
        if not (0.0 < float(self.val_fraction) < 0.5):
            raise ValueError("val_fraction must be in (0, 0.5)")
        if int(self.batch_size) <= 0 or int(self.epochs) <= 0:
            raise ValueError("batch_size and epochs must be positive")
        if float(self.learning_rate) <= 0.0 or float(self.weight_decay) < 0.0:
            raise ValueError("learning_rate must be positive and weight_decay non-negative")
        if int(self.patience) <= 0:
            raise ValueError("patience must be positive")


@dataclass(frozen=True)
class MlpTrainLogEntry:
    epoch: int
    train_loss: float
    val_loss: float
    val_rmse_dx_m: float
    val_rmse_dy_m: float
    val_rmse_dtheta_rad: float
    val_l2_delta_mean: float
    elapsed_s: float
    learning_rate: float


@dataclass(frozen=True)
class MlpTrainResult:
    output_dir: Path
    checkpoint_path: Path
    metadata_path: Path
    train_log_csv: Path
    split_indices_path: Path
    config: MlpTrainingConfig
    sample_count: int
    train_count: int
    val_count: int
    parameter_count: int
    best_epoch: int
    best_val_loss: float
    best_metrics: dict[str, float]
    epochs_ran: int
    device: str


class SubgoalMlp(nn.Module):
    """Four-Linear-layer MLP for T10 subgoal regression."""

    def __init__(
        self,
        *,
        input_dim: int = 41,
        hidden_dims: tuple[int, int, int] = (256, 256, 128),
        output_dim: int = 3,
    ) -> None:
        super().__init__()
        dims = (int(input_dim), *tuple(int(dim) for dim in hidden_dims), int(output_dim))
        layers: list[nn.Module] = []
        for idx in range(len(dims) - 1):
            layers.append(nn.Linear(dims[idx], dims[idx + 1]))
            if idx < len(dims) - 2:
                layers.append(nn.ReLU())
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


@dataclass(frozen=True)
class MlpSubgoalPredictor:
    model: SubgoalMlp
    feature_mean: np.ndarray
    feature_std: np.ndarray
    label_mean: np.ndarray
    label_std: np.ndarray
    metadata: dict[str, Any]
    device: torch.device
    root: Path | None = None
    name: str = "mlp"

    @classmethod
    def load(cls, root: str | Path, *, device: str = "cpu") -> "MlpSubgoalPredictor":
        root_path = Path(root)
        checkpoint_path = root_path / "checkpoint.pt"
        target_device = torch.device(device)
        checkpoint = torch.load(checkpoint_path, map_location=target_device, weights_only=False)
        model = SubgoalMlp(
            input_dim=int(checkpoint["input_dim"]),
            hidden_dims=tuple(int(v) for v in checkpoint["hidden_dims"]),
            output_dim=int(checkpoint["output_dim"]),
        )
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(target_device)
        model.eval()
        metadata = json.loads((root_path / "metadata.json").read_text(encoding="utf-8"))
        return cls(
            model=model,
            feature_mean=_tensor_to_numpy(checkpoint["feature_mean"]),
            feature_std=_tensor_to_numpy(checkpoint["feature_std"]),
            label_mean=_tensor_to_numpy(checkpoint["label_mean"]),
            label_std=_tensor_to_numpy(checkpoint["label_std"]),
            metadata=metadata,
            device=target_device,
            root=root_path,
        )

    def normalize_feature(self, feature: np.ndarray) -> np.ndarray:
        vector = np.asarray(feature, dtype=np.float32).reshape(-1)
        if vector.shape != self.feature_mean.shape:
            raise ValueError(
                f"feature shape {vector.shape} does not match MLP feature shape {self.feature_mean.shape}"
            )
        return ((vector - self.feature_mean) / self.feature_std).astype(np.float32, copy=False)

    def query(
        self,
        feature: np.ndarray,
        *,
        current_pose: Pose,
        k: int,
    ) -> tuple[MlpNeighborPrediction, ...]:
        del k
        normalized = self.normalize_feature(feature)
        with torch.inference_mode():
            x = torch.from_numpy(normalized.reshape(1, -1)).to(self.device)
            pred_norm = self.model(x).detach().cpu().numpy().reshape(-1)
        delta = pred_norm * self.label_std + self.label_mean
        delta_pose = _subgoal_delta(delta)
        subgoal = _compose_subgoal_pose(current_pose, delta_pose)
        return (
            MlpNeighborPrediction(
                rank=1,
                sample_index=-1,
                distance=float("nan"),
                delta_body=delta_pose,
                subgoal_pose=subgoal,
            ),
        )


def train_mlp_model(
    dataset_dir: str | Path,
    output_dir: str | Path,
    *,
    config: MlpTrainingConfig | None = None,
    source_head: str = "unknown",
    execution_host: str = "unknown",
    command: str = "unknown",
) -> MlpTrainResult:
    cfg = config or MlpTrainingConfig()
    _seed_everything(int(cfg.seed))
    dataset_path = Path(dataset_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    features = np.load(dataset_path / "features.npy").astype(np.float32, copy=False)
    labels = np.load(dataset_path / "labels.npy").astype(np.float32, copy=False)
    _validate_arrays(features, labels, cfg)

    train_idx, val_idx = _split_indices(features.shape[0], seed=int(cfg.seed), val_fraction=float(cfg.val_fraction))
    split_indices_path = output_path / "split_indices.npz"
    np.savez_compressed(split_indices_path, train_indices=train_idx, val_indices=val_idx)

    feature_mean, feature_std = _zscore_stats(features[train_idx], eps=float(cfg.zscore_epsilon))
    label_mean, label_std = _zscore_stats(labels[train_idx], eps=float(cfg.zscore_epsilon))
    x_train = ((features[train_idx] - feature_mean) / feature_std).astype(np.float32, copy=False)
    y_train = ((labels[train_idx] - label_mean) / label_std).astype(np.float32, copy=False)
    x_val = ((features[val_idx] - feature_mean) / feature_std).astype(np.float32, copy=False)
    y_val = ((labels[val_idx] - label_mean) / label_std).astype(np.float32, copy=False)

    device = _resolve_device(cfg.device)
    model = SubgoalMlp(input_dim=int(cfg.input_dim), hidden_dims=cfg.hidden_dims, output_dim=int(cfg.output_dim)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=float(cfg.learning_rate), weight_decay=float(cfg.weight_decay))
    loss_fn = nn.MSELoss()
    train_loader = _data_loader(x_train, y_train, cfg, shuffle=True)
    val_loader = _data_loader(x_val, y_val, cfg, shuffle=False)

    log_entries: list[MlpTrainLogEntry] = []
    best_state: dict[str, torch.Tensor] | None = None
    best_epoch = 0
    best_val_loss = float("inf")
    best_metrics: dict[str, float] = {}
    stale_epochs = 0
    started = time.perf_counter()

    for epoch in range(1, int(cfg.epochs) + 1):
        train_loss = _train_epoch(model, train_loader, optimizer, loss_fn, device)
        val_loss, metrics = _evaluate(
            model,
            val_loader,
            loss_fn,
            device,
            label_mean=label_mean,
            label_std=label_std,
        )
        elapsed = time.perf_counter() - started
        log_entries.append(
            MlpTrainLogEntry(
                epoch=epoch,
                train_loss=float(train_loss),
                val_loss=float(val_loss),
                val_rmse_dx_m=float(metrics["val_rmse_dx_m"]),
                val_rmse_dy_m=float(metrics["val_rmse_dy_m"]),
                val_rmse_dtheta_rad=float(metrics["val_rmse_dtheta_rad"]),
                val_l2_delta_mean=float(metrics["val_l2_delta_mean"]),
                elapsed_s=float(elapsed),
                learning_rate=float(optimizer.param_groups[0]["lr"]),
            )
        )
        if val_loss < best_val_loss - float(cfg.min_delta):
            best_val_loss = float(val_loss)
            best_epoch = int(epoch)
            best_metrics = {key: float(value) for key, value in metrics.items()}
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            stale_epochs = 0
        else:
            stale_epochs += 1
            if stale_epochs >= int(cfg.patience):
                break

    if best_state is None:
        best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        best_epoch = len(log_entries)
        best_val_loss = float(log_entries[-1].val_loss)
        best_metrics = {
            "val_rmse_dx_m": float(log_entries[-1].val_rmse_dx_m),
            "val_rmse_dy_m": float(log_entries[-1].val_rmse_dy_m),
            "val_rmse_dtheta_rad": float(log_entries[-1].val_rmse_dtheta_rad),
            "val_l2_delta_mean": float(log_entries[-1].val_l2_delta_mean),
        }

    checkpoint_path = output_path / "checkpoint.pt"
    torch.save(
        {
            "task": "T10",
            "model": "SubgoalMlp",
            "input_dim": int(cfg.input_dim),
            "hidden_dims": list(int(v) for v in cfg.hidden_dims),
            "output_dim": int(cfg.output_dim),
            "model_state_dict": best_state,
            "feature_mean": torch.from_numpy(feature_mean.astype(np.float32, copy=False)),
            "feature_std": torch.from_numpy(feature_std.astype(np.float32, copy=False)),
            "label_mean": torch.from_numpy(label_mean.astype(np.float32, copy=False)),
            "label_std": torch.from_numpy(label_std.astype(np.float32, copy=False)),
            "best_epoch": int(best_epoch),
            "best_val_loss": float(best_val_loss),
            "best_metrics": best_metrics,
            "config": asdict(cfg),
        },
        checkpoint_path,
    )
    np.save(output_path / "feature_mean.npy", feature_mean.astype(np.float32, copy=False))
    np.save(output_path / "feature_std.npy", feature_std.astype(np.float32, copy=False))
    np.save(output_path / "label_mean.npy", label_mean.astype(np.float32, copy=False))
    np.save(output_path / "label_std.npy", label_std.astype(np.float32, copy=False))

    train_log_csv = output_path / "train_log.csv"
    _write_log_csv(train_log_csv, log_entries)
    parameter_count = count_parameters(model)
    metadata = {
        "task": "T10",
        "model": "MLP",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": source_head,
        "execution_host": execution_host,
        "command": command,
        "source_dataset_dir": str(dataset_path),
        "feature_shape": list(features.shape),
        "label_shape": list(labels.shape),
        "train_count": int(len(train_idx)),
        "val_count": int(len(val_idx)),
        "parameter_count": int(parameter_count),
        "best_epoch": int(best_epoch),
        "best_val_loss": float(best_val_loss),
        "best_metrics": best_metrics,
        "epochs_ran": int(len(log_entries)),
        "device": str(device),
        "torch_version": torch.__version__,
        "config": asdict(cfg),
        "files": {
            "checkpoint": str(checkpoint_path),
            "train_log_csv": str(train_log_csv),
            "split_indices_npz": str(split_indices_path),
            "feature_mean": str(output_path / "feature_mean.npy"),
            "feature_std": str(output_path / "feature_std.npy"),
            "label_mean": str(output_path / "label_mean.npy"),
            "label_std": str(output_path / "label_std.npy"),
        },
    }
    metadata_path = output_path / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    return MlpTrainResult(
        output_dir=output_path,
        checkpoint_path=checkpoint_path,
        metadata_path=metadata_path,
        train_log_csv=train_log_csv,
        split_indices_path=split_indices_path,
        config=cfg,
        sample_count=int(features.shape[0]),
        train_count=int(len(train_idx)),
        val_count=int(len(val_idx)),
        parameter_count=int(parameter_count),
        best_epoch=int(best_epoch),
        best_val_loss=float(best_val_loss),
        best_metrics=best_metrics,
        epochs_ran=int(len(log_entries)),
        device=str(device),
    )


def count_parameters(model: nn.Module) -> int:
    return int(sum(param.numel() for param in model.parameters() if param.requires_grad))


def render_training_report(result: MlpTrainResult, *, source_head: str, execution_host: str) -> str:
    status = "pass" if math.isfinite(result.best_val_loss) else "needs_review"
    metrics = result.best_metrics
    lines = [
        "---",
        "date: 2026-06-20",
        f"status: {status}",
        "origin: ai+experiment",
        "reviewed: false",
        "task: T10",
        "contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_head: {source_head}",
        f"execution_host: {execution_host}",
        "---",
        "",
        "# T10 MLP 消融模型训练报告",
        "",
        "## 结论",
        "",
        f"- 训练状态: `{status}`",
        f"- 样本数: {result.sample_count}",
        f"- 训练/验证划分: {result.train_count} / {result.val_count}",
        f"- 结构: 41 -> {result.config.hidden_dims[0]} -> {result.config.hidden_dims[1]} -> {result.config.hidden_dims[2]} -> 3",
        f"- 参数量: {result.parameter_count}",
        f"- best_epoch: {result.best_epoch} / epochs_ran: {result.epochs_ran}",
        f"- best_val_loss(normalized MSE): {result.best_val_loss:.6f}",
        f"- val RMSE: dx={metrics.get('val_rmse_dx_m', math.nan):.3f} m, dy={metrics.get('val_rmse_dy_m', math.nan):.3f} m, dtheta={metrics.get('val_rmse_dtheta_rad', math.nan):.3f} rad",
        "",
        "参数说明：本次继承 T08 数据集，T05 的 `L_min=1.0m` 与 T06 难度切点仍为 `reviewed:false`；因此该 checkpoint 是可复现实验产物，不代表论文参数冻结。",
        "",
        "## 训练设置",
        "",
        "```text",
        f"seed={result.config.seed}",
        f"batch_size={result.config.batch_size}",
        f"epochs={result.config.epochs}",
        f"learning_rate={result.config.learning_rate}",
        f"weight_decay={result.config.weight_decay}",
        f"patience={result.config.patience}",
        f"device={result.device}",
        "loss=PyTorch nn.MSELoss",
        "optimizer=Adam",
        "feature_normalization=train-split z-score",
        "label_normalization=train-split z-score",
        "```",
        "",
        "## 产物",
        "",
        f"- checkpoint: `{result.checkpoint_path}`",
        f"- metadata: `{result.metadata_path}`",
        f"- train log: `{result.train_log_csv}`",
        f"- split indices: `{result.split_indices_path}`",
        "",
    ]
    return "\n".join(lines)


def _validate_arrays(features: np.ndarray, labels: np.ndarray, cfg: MlpTrainingConfig) -> None:
    if features.ndim != 2 or labels.ndim != 2:
        raise ValueError("features.npy and labels.npy must be 2D arrays")
    if features.shape[0] != labels.shape[0]:
        raise ValueError("features and labels row counts must match")
    if features.shape[1] != int(cfg.input_dim):
        raise ValueError(f"expected feature dimension {cfg.input_dim}, got {features.shape[1]}")
    if labels.shape[1] != int(cfg.output_dim):
        raise ValueError(f"expected label dimension {cfg.output_dim}, got {labels.shape[1]}")
    if features.shape[0] < 10:
        raise ValueError("MLP training requires at least 10 samples")


def _seed_everything(seed: int) -> None:
    random.seed(int(seed))
    np.random.seed(int(seed))
    torch.manual_seed(int(seed))
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(int(seed))


def _resolve_device(device: str) -> torch.device:
    raw = str(device)
    if raw == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    resolved = torch.device(raw)
    if resolved.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA device requested but torch.cuda.is_available() is false")
    return resolved


def _split_indices(sample_count: int, *, seed: int, val_fraction: float) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(int(seed))
    indices = np.arange(int(sample_count), dtype=np.int64)
    rng.shuffle(indices)
    val_count = max(1, int(round(int(sample_count) * float(val_fraction))))
    train_count = int(sample_count) - val_count
    if train_count <= 0:
        raise ValueError("validation split leaves no training samples")
    return np.sort(indices[:train_count]), np.sort(indices[train_count:])


def _zscore_stats(array: np.ndarray, *, eps: float) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(array, axis=0, dtype=np.float64).astype(np.float32)
    std = np.std(array, axis=0, dtype=np.float64).astype(np.float32)
    std = np.where(std < float(eps), 1.0, std).astype(np.float32)
    return mean, std


def _data_loader(x: np.ndarray, y: np.ndarray, cfg: MlpTrainingConfig, *, shuffle: bool) -> DataLoader:
    dataset = TensorDataset(torch.from_numpy(x), torch.from_numpy(y))
    generator = torch.Generator()
    generator.manual_seed(int(cfg.seed))
    return DataLoader(
        dataset,
        batch_size=int(cfg.batch_size),
        shuffle=bool(shuffle),
        num_workers=int(cfg.num_workers),
        pin_memory=torch.cuda.is_available(),
        generator=generator if shuffle else None,
    )


def _train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_fn: nn.Module,
    device: torch.device,
) -> float:
    model.train()
    total_loss = 0.0
    total_count = 0
    for x, y in loader:
        x = x.to(device, non_blocking=True)
        y = y.to(device, non_blocking=True)
        optimizer.zero_grad(set_to_none=True)
        pred = model(x)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
        count = int(x.shape[0])
        total_loss += float(loss.detach().cpu()) * count
        total_count += count
    return total_loss / max(1, total_count)


def _evaluate(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: nn.Module,
    device: torch.device,
    *,
    label_mean: np.ndarray,
    label_std: np.ndarray,
) -> tuple[float, dict[str, float]]:
    model.eval()
    total_loss = 0.0
    total_count = 0
    err_sq = np.zeros((3,), dtype=np.float64)
    l2_delta_sum = 0.0
    label_mean_t = torch.from_numpy(label_mean).to(device)
    label_std_t = torch.from_numpy(label_std).to(device)
    with torch.inference_mode():
        for x, y in loader:
            x = x.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)
            pred_norm = model(x)
            loss = loss_fn(pred_norm, y)
            pred = pred_norm * label_std_t + label_mean_t
            target = y * label_std_t + label_mean_t
            err = (pred - target).detach().cpu().numpy().astype(np.float64, copy=False)
            count = int(x.shape[0])
            total_loss += float(loss.detach().cpu()) * count
            total_count += count
            err_sq += np.sum(np.square(err), axis=0)
            l2_delta_sum += float(np.sum(np.linalg.norm(err, axis=1)))
    denom = max(1, total_count)
    rmse = np.sqrt(err_sq / float(denom))
    return total_loss / denom, {
        "val_rmse_dx_m": float(rmse[0]),
        "val_rmse_dy_m": float(rmse[1]),
        "val_rmse_dtheta_rad": float(rmse[2]),
        "val_l2_delta_mean": float(l2_delta_sum / float(denom)),
    }


def _write_log_csv(path: Path, rows: Iterable[MlpTrainLogEntry]) -> None:
    rows = tuple(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _tensor_to_numpy(value: Any) -> np.ndarray:
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().numpy().astype(np.float32, copy=False)
    return np.asarray(value, dtype=np.float32)


def _subgoal_delta(values: Iterable[float]) -> Pose:
    raw = tuple(float(v) for v in values)
    if len(raw) != 3:
        raise ValueError("subgoal delta must have exactly three values")
    return raw  # type: ignore[return-value]


def _compose_subgoal_pose(current_pose: Pose, delta_body: Pose) -> Pose:
    x, y, theta = (float(v) for v in current_pose)
    dx, dy, dtheta = (float(v) for v in delta_body)
    c = math.cos(theta)
    s = math.sin(theta)
    return (
        float(x + c * dx - s * dy),
        float(y + s * dx + c * dy),
        _wrap_pi(theta + dtheta),
    )


def _wrap_pi(angle_rad: float) -> float:
    return float(math.atan2(math.sin(float(angle_rad)), math.cos(float(angle_rad))))
