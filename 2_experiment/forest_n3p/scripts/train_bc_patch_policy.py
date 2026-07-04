from __future__ import annotations

import argparse
import json
import math
import os
import random
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pyarrow.parquet as pq

from forest_n3p.main_evaluation import MainEvaluationConfig
from forest_n3p.rl_rs.env import AnalyticExpansionContext, AnalyticExpansionEnv
from forest_n3p.rl_rs.obs import ObservationConfig, build_patch_observation
from forest_n3p.scripts.run_oracle_connector_analysis import _grid_for_row, _profiles_from_bucket_mode
from forest_n3p.scripts.train_bc_policy import (
    _load_torch,
    _parse_hidden_dims,
    _resolve_device,
    _set_seeds,
    _split_by_source,
)
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    if bool(args.allow_duplicate_openmp):
        os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    torch = _load_torch()
    _set_seeds(torch, int(args.seed))

    source_head = str(args.source_head) if args.source_head else _source_head()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = pq.read_table(args.dataset).to_pylist()
    if not rows:
        raise ValueError(f"dataset has no rows: {args.dataset}")
    split = _split_by_source(rows, val_fraction=float(args.val_fraction), seed=int(args.seed))
    train_rows = [row for row in rows if int(row["source_row_index"]) in split["train_sources"]]
    val_rows = [row for row in rows if int(row["source_row_index"]) in split["val_sources"]]
    train_rows = _bounded_rows(train_rows, max_rows=args.max_train_rows, seed=int(args.seed))
    val_rows = _bounded_rows(val_rows, max_rows=args.max_val_rows, seed=int(args.seed) + 1)
    if not train_rows or not val_rows:
        raise ValueError("train/val split must produce non-empty row sets")

    cfg = _evaluation_config()
    params = AckermannParams(wheelbase=float(args.wheelbase_m), min_turn_radius=float(args.turning_radius_m))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    obs_config = ObservationConfig(
        patch_size_m=float(args.obs_patch_size_m),
        patch_cells=int(args.obs_patch_cells),
        include_edt=bool(args.obs_include_edt),
        edt_clip_m=float(args.obs_edt_clip_m),
    )
    scalar_mean, scalar_std = _scalar_normalization(train_rows)

    train_ds = PatchBcDataset(train_rows, cfg=cfg, footprint=footprint, obs_config=obs_config, scalar_mean=scalar_mean, scalar_std=scalar_std)
    val_ds = PatchBcDataset(val_rows, cfg=cfg, footprint=footprint, obs_config=obs_config, scalar_mean=scalar_mean, scalar_std=scalar_std)
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=int(args.batch_size), shuffle=True, num_workers=0)
    val_loader = torch.utils.data.DataLoader(val_ds, batch_size=int(args.batch_size), shuffle=False, num_workers=0)

    model = _build_patch_scalar_cnn(
        torch=torch,
        patch_channels=2 if bool(args.obs_include_edt) else 1,
        scalar_dim=8,
        cnn_channels=_parse_hidden_dims(str(args.cnn_channels)),
        hidden_dims=_parse_hidden_dims(str(args.hidden_dims)),
        max_steer=float(params.max_steer),
    )
    device = _resolve_device(torch, str(args.device))
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.learning_rate), weight_decay=float(args.weight_decay))
    loss_fn = torch.nn.MSELoss()

    best_state: dict[str, Any] | None = None
    best_val_loss = math.inf
    best_epoch = -1
    epochs_without_improvement = 0
    history: list[dict[str, float | int]] = []
    for epoch in range(int(args.epochs)):
        model.train()
        train_losses: list[float] = []
        for patch, scalar, target in train_loader:
            patch = patch.to(device=device, dtype=torch.float32)
            scalar = scalar.to(device=device, dtype=torch.float32)
            target = target.to(device=device, dtype=torch.float32).reshape(-1, 1)
            pred = model(patch, scalar)
            loss = loss_fn(pred, target)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            train_losses.append(float(loss.detach().cpu()))

        val_loss, val_pred, val_target = _evaluate_action_loss(torch, model, val_loader, loss_fn, device)
        history.append({"epoch": int(epoch), "train_loss": float(np.mean(train_losses)), "val_loss": float(val_loss)})
        if val_loss < best_val_loss - float(args.min_delta):
            best_val_loss = val_loss
            best_epoch = int(epoch)
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
        if epochs_without_improvement >= int(args.patience):
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    _val_loss, val_pred, val_target = _evaluate_action_loss(torch, model, val_loader, loss_fn, device)
    action_metrics = _action_metric_arrays(val_pred, val_target)
    rollout_metrics = _closed_loop_metrics(
        torch=torch,
        model=model,
        val_rows=val_rows,
        scalar_mean=scalar_mean,
        scalar_std=scalar_std,
        args=args,
        params=params,
        obs_config=obs_config,
        device=device,
    )

    checkpoint_path = output_dir / "checkpoint.pt"
    torch.save(
        {
            "model_type": "patch_scalar_cnn",
            "state_dict": model.state_dict(),
            "patch_channels": 2 if bool(args.obs_include_edt) else 1,
            "scalar_dim": 8,
            "cnn_channels": _parse_hidden_dims(str(args.cnn_channels)),
            "hidden_dims": _parse_hidden_dims(str(args.hidden_dims)),
            "max_steer": float(params.max_steer),
            "scalar_mean": scalar_mean.astype(np.float32).reshape(-1).tolist(),
            "scalar_std": scalar_std.astype(np.float32).reshape(-1).tolist(),
            "observation_config": _observation_config_record(obs_config),
            "source_head": source_head,
        },
        checkpoint_path,
    )
    summary = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": " ".join(["python -m forest_n3p.scripts.train_bc_patch_policy", *raw_argv]),
        "dataset": str(args.dataset),
        "manifest": str(args.manifest),
        "output_dir": str(output_dir),
        "checkpoint": str(checkpoint_path),
        "dataset_rows": int(len(rows)),
        "train_rows": int(len(train_rows)),
        "val_rows": int(len(val_rows)),
        "train_source_rows": int(len({int(row["source_row_index"]) for row in train_rows})),
        "val_source_rows": int(len({int(row["source_row_index"]) for row in val_rows})),
        "best_epoch": int(best_epoch),
        "epochs_ran": int(len(history)),
        "best_val_mse": float(best_val_loss),
        "action_metrics": action_metrics,
        "closed_loop_metrics": rollout_metrics,
        "config": {
            "seed": int(args.seed),
            "cnn_channels": list(_parse_hidden_dims(str(args.cnn_channels))),
            "hidden_dims": list(_parse_hidden_dims(str(args.hidden_dims))),
            "batch_size": int(args.batch_size),
            "epochs": int(args.epochs),
            "learning_rate": float(args.learning_rate),
            "weight_decay": float(args.weight_decay),
            "patience": int(args.patience),
            "val_fraction": float(args.val_fraction),
            "max_train_rows": args.max_train_rows,
            "max_val_rows": args.max_val_rows,
            "rollout_max_steps": int(args.rollout_max_steps),
            "rollout_action_step_m": float(args.rollout_action_step_m),
            "collision_sample_step_m": float(args.collision_sample_step_m),
            "device": str(device),
            "allow_duplicate_openmp": bool(args.allow_duplicate_openmp),
            "observation_config": _observation_config_record(obs_config),
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (output_dir / "history.json").write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


class PatchBcDataset:
    def __init__(
        self,
        rows: list[dict[str, Any]],
        *,
        cfg: MainEvaluationConfig,
        footprint: TwoCircleFootprint,
        obs_config: ObservationConfig,
        scalar_mean: np.ndarray,
        scalar_std: np.ndarray,
    ) -> None:
        self.rows = rows
        self.cfg = cfg
        self.footprint = footprint
        self.obs_config = obs_config
        self.scalar_mean = np.asarray(scalar_mean, dtype=np.float32).reshape(-1)
        self.scalar_std = np.asarray(scalar_std, dtype=np.float32).reshape(-1)
        self.map_cache: dict[int, Any] = {}

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int):
        row = self.rows[int(index)]
        grid_map = _grid_for_row(row, self.cfg, self.footprint, self.map_cache)
        state = AckermannState(float(row["current_x"]), float(row["current_y"]), float(row["current_theta"]))
        patch = build_patch_observation(grid_map, state, self.obs_config)
        scalar = (np.asarray(row["obs_scalar"], dtype=np.float32).reshape(-1) - self.scalar_mean) / self.scalar_std
        target = np.asarray(float(row["expert_steering_rad"]), dtype=np.float32)
        return patch.astype(np.float32, copy=False), scalar.astype(np.float32, copy=False), target


def _build_patch_scalar_cnn(
    *,
    torch: Any,
    patch_channels: int,
    scalar_dim: int,
    cnn_channels: tuple[int, ...],
    hidden_dims: tuple[int, ...],
    max_steer: float,
):
    class PatchScalarCnn(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            conv_layers: list[Any] = []
            in_channels = int(patch_channels)
            for out_channels in cnn_channels:
                conv_layers.append(torch.nn.Conv2d(in_channels, int(out_channels), kernel_size=5, stride=2, padding=2))
                conv_layers.append(torch.nn.ReLU())
                in_channels = int(out_channels)
            self.patch_net = torch.nn.Sequential(*conv_layers, torch.nn.AdaptiveAvgPool2d((1, 1)), torch.nn.Flatten())
            self.scalar_net = torch.nn.Sequential(torch.nn.Linear(int(scalar_dim), 32), torch.nn.ReLU())
            head_layers: list[Any] = []
            last = int(cnn_channels[-1]) + 32
            for hidden in hidden_dims:
                head_layers.append(torch.nn.Linear(last, int(hidden)))
                head_layers.append(torch.nn.ReLU())
                last = int(hidden)
            head_layers.append(torch.nn.Linear(last, 1))
            self.head = torch.nn.Sequential(*head_layers)
            self.max_steer = float(max_steer)

        def forward(self, patch, scalar):
            features = torch.cat((self.patch_net(patch), self.scalar_net(scalar)), dim=1)
            return self.max_steer * torch.tanh(self.head(features))

    if not cnn_channels:
        raise ValueError("cnn_channels must not be empty")
    return PatchScalarCnn()


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a Module2 RL-RS patch+scalar CNN BC steering policy.")
    parser.add_argument("--dataset", type=Path, default=Path("2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet"))
    parser.add_argument("--manifest", type=Path, default=Path("2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview"))
    parser.add_argument("--seed", type=int, default=20260703)
    parser.add_argument("--cnn-channels", default="16,32,64")
    parser.add_argument("--hidden-dims", default="128,64")
    parser.add_argument("--val-fraction", type=float, default=0.25)
    parser.add_argument("--max-train-rows", type=int, default=None)
    parser.add_argument("--max-val-rows", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--patience", type=int, default=8)
    parser.add_argument("--min-delta", type=float, default=1e-7)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--rollout-max-steps", type=int, default=96)
    parser.add_argument("--rollout-action-step-m", type=float, default=0.1)
    parser.add_argument("--collision-sample-step-m", type=float, default=0.05)
    parser.add_argument("--turning-radius-m", type=float, default=1.0)
    parser.add_argument("--wheelbase-m", type=float, default=0.6)
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--obs-patch-size-m", type=float, default=6.4)
    parser.add_argument("--obs-patch-cells", type=int, default=64)
    parser.add_argument("--obs-edt-clip-m", type=float, default=3.0)
    parser.add_argument("--no-obs-include-edt", dest="obs_include_edt", action="store_false")
    parser.set_defaults(obs_include_edt=True)
    parser.add_argument("--source-head", default=None)
    parser.add_argument("--allow-duplicate-openmp", action="store_true")
    args = parser.parse_args(argv)
    _validate_args(args)
    return args


def _validate_args(args: argparse.Namespace) -> None:
    if not (0.0 < float(args.val_fraction) < 1.0):
        raise ValueError("--val-fraction must be in (0, 1)")
    for name in ("batch_size", "epochs", "patience", "rollout_max_steps", "theta_bins", "obs_patch_cells"):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    for name in (
        "learning_rate",
        "rollout_action_step_m",
        "collision_sample_step_m",
        "turning_radius_m",
        "wheelbase_m",
        "obs_patch_size_m",
        "obs_edt_clip_m",
    ):
        value = float(getattr(args, name))
        if not (math.isfinite(value) and value > 0.0):
            raise ValueError(f"--{name.replace('_', '-')} must be finite and positive")
    for name in ("max_train_rows", "max_val_rows"):
        value = getattr(args, name)
        if value is not None and int(value) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive when set")


def _bounded_rows(rows: list[dict[str, Any]], *, max_rows: int | None, seed: int) -> list[dict[str, Any]]:
    if max_rows is None or int(max_rows) >= len(rows):
        return rows
    rng = random.Random(int(seed))
    indices = sorted(rng.sample(range(len(rows)), int(max_rows)))
    return [rows[index] for index in indices]


def _scalar_normalization(rows: list[dict[str, Any]]) -> tuple[np.ndarray, np.ndarray]:
    scalars = np.asarray([row["obs_scalar"] for row in rows], dtype=np.float32)
    mean = scalars.mean(axis=0)
    std = np.maximum(scalars.std(axis=0), 1e-6)
    return mean.astype(np.float32, copy=False), std.astype(np.float32, copy=False)


def _evaluate_action_loss(torch: Any, model: Any, loader: Any, loss_fn: Any, device: Any) -> tuple[float, np.ndarray, np.ndarray]:
    model.eval()
    losses: list[float] = []
    preds: list[np.ndarray] = []
    targets: list[np.ndarray] = []
    with torch.no_grad():
        for patch, scalar, target in loader:
            patch = patch.to(device=device, dtype=torch.float32)
            scalar = scalar.to(device=device, dtype=torch.float32)
            target_t = target.to(device=device, dtype=torch.float32).reshape(-1, 1)
            pred = model(patch, scalar)
            losses.append(float(loss_fn(pred, target_t).detach().cpu()))
            preds.append(pred.detach().cpu().numpy().reshape(-1))
            targets.append(target_t.detach().cpu().numpy().reshape(-1))
    return float(np.mean(losses)), np.concatenate(preds), np.concatenate(targets)


def _action_metric_arrays(pred: np.ndarray, target: np.ndarray) -> dict[str, float]:
    error = np.asarray(pred, dtype=np.float32) - np.asarray(target, dtype=np.float32)
    return {
        "val_mse": float(np.mean(error * error)),
        "val_mae_rad": float(np.mean(np.abs(error))),
        "val_max_abs_error_rad": float(np.max(np.abs(error))),
        "prediction_mean_rad": float(np.mean(pred)),
        "target_mean_rad": float(np.mean(target)),
    }


def _closed_loop_metrics(
    *,
    torch: Any,
    model: Any,
    val_rows: list[dict[str, Any]],
    scalar_mean: np.ndarray,
    scalar_std: np.ndarray,
    args: argparse.Namespace,
    params: AckermannParams,
    obs_config: ObservationConfig,
    device: Any,
) -> dict[str, Any]:
    cfg = _evaluation_config()
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    map_cache: dict[int, Any] = {}
    first_by_source: dict[int, dict[str, Any]] = {}
    for row in val_rows:
        first_by_source.setdefault(int(row["source_row_index"]), row)

    counts = {"episodes": 0, "terminal_rs_success": 0, "collision": 0, "truncated": 0, "runtime_error": 0}
    episode_rows: list[dict[str, Any]] = []
    for source_row, row in sorted(first_by_source.items()):
        counts["episodes"] += 1
        grid_map = _grid_for_row(row, cfg, footprint, map_cache)
        checker = GridFootprintChecker(grid_map, footprint, theta_bins=int(args.theta_bins))
        env = AnalyticExpansionEnv()
        try:
            obs = env.reset(
                AnalyticExpansionContext(
                    grid_map=grid_map,
                    footprint=footprint,
                    start=AckermannState(float(row["current_x"]), float(row["current_y"]), float(row["current_theta"])),
                    goal=AckermannState(float(row["goal_x"]), float(row["goal_y"]), float(row["goal_theta"])),
                    params=params,
                    checker=checker,
                    max_steps=int(args.rollout_max_steps),
                    action_step_m=float(args.rollout_action_step_m),
                    collision_sample_step_m=float(args.collision_sample_step_m),
                    terminal_check_every=1,
                    theta_bins=int(args.theta_bins),
                    observation_config=obs_config,
                )
            )
            final_step = None
            for _ in range(int(args.rollout_max_steps)):
                patch = torch.as_tensor(obs.patch.reshape(1, *obs.patch.shape), dtype=torch.float32, device=device)
                scalar = (np.asarray(obs.scalar, dtype=np.float32).reshape(-1) - scalar_mean) / scalar_std
                scalar_t = torch.as_tensor(scalar.reshape(1, -1), dtype=torch.float32, device=device)
                with torch.no_grad():
                    action = float(model(patch, scalar_t).detach().cpu().numpy()[0, 0])
                final_step = env.step(action)
                obs = final_step.observation
                if final_step.terminated or final_step.truncated:
                    break
            success = bool(final_step is not None and final_step.telemetry.terminal_rs_success)
            collision = bool(final_step is not None and final_step.telemetry.collided)
            truncated = bool(final_step is not None and final_step.truncated)
            counts["terminal_rs_success"] += int(success)
            counts["collision"] += int(collision)
            counts["truncated"] += int(truncated)
            episode_rows.append(
                {
                    "source_row_index": int(source_row),
                    "query_id": str(row["query_id"]),
                    "success": success,
                    "collision": collision,
                    "truncated": truncated,
                    "steps": int(env.telemetry.rollout_steps),
                    "failure_reason": None if final_step is None else final_step.telemetry.failure_reason,
                }
            )
        except Exception as exc:  # noqa: BLE001 - evaluation should record failures.
            counts["runtime_error"] += 1
            episode_rows.append(
                {
                    "source_row_index": int(source_row),
                    "query_id": str(row["query_id"]),
                    "success": False,
                    "collision": False,
                    "truncated": False,
                    "steps": 0,
                    "failure_reason": _runtime_error_reason(exc),
                }
            )
    episodes = max(1, int(counts["episodes"]))
    return {
        **counts,
        "terminal_rs_success_rate": float(counts["terminal_rs_success"]) / float(episodes),
        "collision_rate": float(counts["collision"]) / float(episodes),
        "truncation_rate": float(counts["truncated"]) / float(episodes),
        "episodes_detail": episode_rows,
    }


def _evaluation_config() -> MainEvaluationConfig:
    return MainEvaluationConfig(
        seed=20260620,
        profiles=_profiles_from_bucket_mode("validation_t06"),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )


def _observation_config_record(config: ObservationConfig) -> dict[str, Any]:
    return {
        "patch_size_m": float(config.patch_size_m),
        "patch_cells": int(config.patch_cells),
        "include_edt": bool(config.include_edt),
        "edt_clip_m": float(config.edt_clip_m),
    }


def _runtime_error_reason(exc: Exception) -> str:
    message = str(exc).replace("\n", " ").strip()
    if len(message) > 200:
        message = message[:197] + "..."
    return f"runtime_error:{type(exc).__name__}:{message}" if message else f"runtime_error:{type(exc).__name__}"


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop training.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
