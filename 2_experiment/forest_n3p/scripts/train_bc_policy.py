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

from forest_n3p.rl_rs.env import AnalyticExpansionContext, AnalyticExpansionEnv
from forest_n3p.rl_rs.obs import ObservationConfig, RlRsObservation, build_patch_observation
from forest_n3p.scripts.run_oracle_connector_analysis import MapCacheKey, _grid_for_row, _profiles_from_bucket_mode
from forest_n3p.main_evaluation import MainEvaluationConfig
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
    if not train_rows or not val_rows:
        raise ValueError("train/val split must produce non-empty row sets")

    cfg = MainEvaluationConfig(
        seed=20260620,
        profiles=_profiles_from_bucket_mode("validation_t06"),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    params = AckermannParams(wheelbase=float(args.wheelbase_m), min_turn_radius=float(args.turning_radius_m))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    obs_config = ObservationConfig(
        patch_size_m=float(args.obs_patch_size_m),
        patch_cells=int(args.obs_patch_cells),
        include_edt=bool(args.obs_include_edt),
        edt_clip_m=float(args.obs_edt_clip_m),
    )

    x_train = _feature_matrix(train_rows, feature_mode=str(args.feature_mode), cfg=cfg, footprint=footprint, obs_config=obs_config)
    y_train = _target_vector(train_rows)
    x_val = _feature_matrix(val_rows, feature_mode=str(args.feature_mode), cfg=cfg, footprint=footprint, obs_config=obs_config)
    y_val = _target_vector(val_rows)
    mean = x_train.mean(axis=0, keepdims=True)
    std = np.maximum(x_train.std(axis=0, keepdims=True), 1e-6)
    x_train_n = (x_train - mean) / std
    x_val_n = (x_val - mean) / std

    model = _build_scalar_steering_mlp(
        torch=torch,
        input_dim=x_train.shape[1],
        hidden_dims=_parse_hidden_dims(str(args.hidden_dims)),
        max_steer=float(params.max_steer),
    )
    device = _resolve_device(torch, str(args.device))
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.learning_rate), weight_decay=float(args.weight_decay))
    loss_fn = torch.nn.MSELoss()
    train_x_t = torch.as_tensor(x_train_n, dtype=torch.float32, device=device)
    train_y_t = torch.as_tensor(y_train, dtype=torch.float32, device=device).reshape(-1, 1)
    val_x_t = torch.as_tensor(x_val_n, dtype=torch.float32, device=device)
    val_y_t = torch.as_tensor(y_val, dtype=torch.float32, device=device).reshape(-1, 1)

    best_state: dict[str, Any] | None = None
    best_val_loss = math.inf
    best_epoch = -1
    epochs_without_improvement = 0
    history: list[dict[str, float | int]] = []
    for epoch in range(int(args.epochs)):
        model.train()
        permutation = torch.randperm(train_x_t.shape[0], device=device)
        batch_losses: list[float] = []
        for start in range(0, int(train_x_t.shape[0]), int(args.batch_size)):
            idx = permutation[start : start + int(args.batch_size)]
            pred = model(train_x_t[idx])
            loss = loss_fn(pred, train_y_t[idx])
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            batch_losses.append(float(loss.detach().cpu()))

        model.eval()
        with torch.no_grad():
            val_pred = model(val_x_t)
            val_loss = float(loss_fn(val_pred, val_y_t).detach().cpu())
        train_loss = float(np.mean(batch_losses)) if batch_losses else math.inf
        history.append({"epoch": int(epoch), "train_loss": train_loss, "val_loss": val_loss})
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
    action_metrics = _action_metrics(torch, model, val_x_t, val_y_t)
    rollout_metrics = _closed_loop_metrics(
        torch=torch,
        model=model,
        val_rows=val_rows,
        mean=mean,
        std=std,
        args=args,
        params=params,
        feature_mode=str(args.feature_mode),
        obs_config=obs_config,
        device=device,
    )

    checkpoint_path = output_dir / "checkpoint.pt"
    torch.save(
        {
            "model_type": f"{args.feature_mode}_steering_mlp",
            "state_dict": model.state_dict(),
            "input_dim": int(x_train.shape[1]),
            "hidden_dims": _parse_hidden_dims(str(args.hidden_dims)),
            "max_steer": float(params.max_steer),
            "feature_mode": str(args.feature_mode),
            "feature_mean": mean.astype(np.float32).reshape(-1).tolist(),
            "feature_std": std.astype(np.float32).reshape(-1).tolist(),
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
        "command": " ".join(["python -m forest_n3p.scripts.train_bc_policy", *raw_argv]),
        "dataset": str(args.dataset),
        "manifest": str(args.manifest),
        "output_dir": str(output_dir),
        "checkpoint": str(checkpoint_path),
        "dataset_rows": int(len(rows)),
        "train_rows": int(len(train_rows)),
        "val_rows": int(len(val_rows)),
        "train_source_rows": int(len(split["train_sources"])),
        "val_source_rows": int(len(split["val_sources"])),
        "best_epoch": int(best_epoch),
        "epochs_ran": int(len(history)),
        "best_val_mse": float(best_val_loss),
        "action_metrics": action_metrics,
        "closed_loop_metrics": rollout_metrics,
        "config": {
            "seed": int(args.seed),
            "feature_mode": str(args.feature_mode),
            "hidden_dims": list(_parse_hidden_dims(str(args.hidden_dims))),
            "batch_size": int(args.batch_size),
            "epochs": int(args.epochs),
            "learning_rate": float(args.learning_rate),
            "weight_decay": float(args.weight_decay),
            "patience": int(args.patience),
            "val_fraction": float(args.val_fraction),
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


def _build_scalar_steering_mlp(*, torch: Any, input_dim: int, hidden_dims: tuple[int, ...], max_steer: float):
    class ScalarSteeringMlp(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            layers: list[Any] = []
            last = int(input_dim)
            for hidden in hidden_dims:
                layers.append(torch.nn.Linear(last, int(hidden)))
                layers.append(torch.nn.ReLU())
                last = int(hidden)
            layers.append(torch.nn.Linear(last, 1))
            self.net = torch.nn.Sequential(*layers)
            self.max_steer = float(max_steer)

        def forward(self, scalar_obs):
            return self.max_steer * torch.tanh(self.net(scalar_obs))

    return ScalarSteeringMlp()


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a Module2 RL-RS BC steering policy.")
    parser.add_argument("--dataset", type=Path, default=Path("2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet"))
    parser.add_argument("--manifest", type=Path, default=Path("2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_preview"))
    parser.add_argument("--seed", type=int, default=20260703)
    parser.add_argument("--feature-mode", choices=("scalar", "obstacle_summary"), default="scalar")
    parser.add_argument("--hidden-dims", default="64,64")
    parser.add_argument("--val-fraction", type=float, default=0.25)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--patience", type=int, default=12)
    parser.add_argument("--min-delta", type=float, default=1e-7)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--rollout-max-steps", type=int, default=32)
    parser.add_argument("--rollout-action-step-m", type=float, default=0.3)
    parser.add_argument("--collision-sample-step-m", type=float, default=0.1)
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
    for name in ("batch_size", "epochs", "patience", "rollout_max_steps", "theta_bins"):
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
    if int(args.obs_patch_cells) <= 0:
        raise ValueError("--obs-patch-cells must be positive")


def _load_torch():
    try:
        import torch
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("PyTorch is required for BC training. On local Mac, pass --allow-duplicate-openmp if libomp conflicts.") from exc
    return torch


def _set_seeds(torch: Any, seed: int) -> None:
    random.seed(int(seed))
    np.random.seed(int(seed))
    torch.manual_seed(int(seed))


def _parse_hidden_dims(raw: str) -> tuple[int, ...]:
    dims = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if not dims or any(dim <= 0 for dim in dims):
        raise ValueError("--hidden-dims must be positive comma-separated integers")
    return dims


def _resolve_device(torch: Any, spec: str):
    if spec == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    return torch.device(spec)


def _split_by_source(rows: list[dict[str, Any]], *, val_fraction: float, seed: int) -> dict[str, set[int]]:
    sources = sorted({int(row["source_row_index"]) for row in rows})
    rng = random.Random(int(seed))
    rng.shuffle(sources)
    val_count = max(1, int(round(len(sources) * float(val_fraction))))
    val_count = min(val_count, len(sources) - 1)
    val_sources = set(sources[:val_count])
    train_sources = set(sources[val_count:])
    return {"train_sources": train_sources, "val_sources": val_sources}


def _feature_matrix(
    rows: list[dict[str, Any]],
    *,
    feature_mode: str,
    cfg: MainEvaluationConfig | None = None,
    footprint: TwoCircleFootprint | None = None,
    obs_config: ObservationConfig | None = None,
) -> np.ndarray:
    if str(feature_mode) == "scalar":
        return np.asarray([_policy_features_from_scalar_and_patch(row["obs_scalar"], None, feature_mode="scalar") for row in rows], dtype=np.float32)
    if str(feature_mode) != "obstacle_summary":
        raise ValueError(f"unsupported feature_mode: {feature_mode}")
    if cfg is None or footprint is None or obs_config is None:
        raise ValueError("cfg, footprint, and obs_config are required for obstacle_summary features")
    map_cache: dict[MapCacheKey, Any] = {}
    features: list[np.ndarray] = []
    for row in rows:
        grid_map = _grid_for_row(row, cfg, footprint, map_cache)
        state = AckermannState(float(row["current_x"]), float(row["current_y"]), float(row["current_theta"]))
        patch = build_patch_observation(grid_map, state, obs_config)
        features.append(_policy_features_from_scalar_and_patch(row["obs_scalar"], patch, feature_mode="obstacle_summary"))
    return np.asarray(features, dtype=np.float32)


def _policy_features_from_observation(obs: RlRsObservation, *, feature_mode: str) -> np.ndarray:
    return _policy_features_from_scalar_and_patch(obs.scalar, obs.patch, feature_mode=feature_mode)


def _policy_features_from_scalar_and_patch(scalar: Sequence[float], patch: np.ndarray | None, *, feature_mode: str) -> np.ndarray:
    scalar_arr = np.asarray(scalar, dtype=np.float32).reshape(-1)
    if str(feature_mode) == "scalar":
        return scalar_arr
    if str(feature_mode) == "obstacle_summary":
        if patch is None:
            raise ValueError("obstacle_summary features require a patch observation")
        return np.concatenate((scalar_arr, _obstacle_summary_features(patch)), axis=0).astype(np.float32, copy=False)
    raise ValueError(f"unsupported feature_mode: {feature_mode}")


def _obstacle_summary_features(patch: np.ndarray) -> np.ndarray:
    patch_arr = np.asarray(patch, dtype=np.float32)
    if patch_arr.ndim != 3:
        raise ValueError("patch must have shape (channels, cells, cells)")
    occupancy = patch_arr[0]
    edt = patch_arr[1] if patch_arr.shape[0] > 1 else 1.0 - occupancy
    cells_y, cells_x = occupancy.shape
    x_axis = _normalized_axis(cells_x)
    y_axis = _normalized_axis(cells_y)
    xx, yy = np.meshgrid(x_axis, y_axis, indexing="xy")
    masks = (
        np.ones_like(occupancy, dtype=bool),
        xx >= 0.0,
        (xx >= 0.0) & (xx <= 0.5) & (np.abs(yy) <= 0.35),
        (xx > 0.5) & (np.abs(yy) <= 0.5),
        (xx >= 0.0) & (yy > 0.0),
        (xx >= 0.0) & (yy < 0.0),
        (xx >= 0.0) & (np.abs(yy) <= 0.15),
    )
    out: list[float] = []
    for mask in masks:
        out.extend(_region_features(occupancy, edt, mask))
    return np.asarray(out, dtype=np.float32)


def _normalized_axis(size: int) -> np.ndarray:
    if int(size) <= 1:
        return np.zeros((int(size),), dtype=np.float32)
    center = (float(size) - 1.0) / 2.0
    return ((np.arange(int(size), dtype=np.float32) - center) / max(center, 1.0)).astype(np.float32, copy=False)


def _region_features(occupancy: np.ndarray, edt: np.ndarray, mask: np.ndarray) -> tuple[float, float, float]:
    if not bool(np.any(mask)):
        return 0.0, 0.0, 0.0
    occ_values = occupancy[mask]
    edt_values = edt[mask]
    return (
        float(np.mean(occ_values)),
        float(np.min(edt_values)),
        float(np.mean(edt_values)),
    )


def _target_vector(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.asarray([float(row["expert_steering_rad"]) for row in rows], dtype=np.float32)


def _action_metrics(torch: Any, model: Any, val_x_t: Any, val_y_t: Any) -> dict[str, float]:
    model.eval()
    with torch.no_grad():
        pred = model(val_x_t).detach().cpu().numpy().reshape(-1)
    target = val_y_t.detach().cpu().numpy().reshape(-1)
    error = pred - target
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
    mean: np.ndarray,
    std: np.ndarray,
    args: argparse.Namespace,
    params: AckermannParams,
    feature_mode: str,
    obs_config: ObservationConfig,
    device: Any,
) -> dict[str, Any]:
    cfg = MainEvaluationConfig(
        seed=20260620,
        profiles=_profiles_from_bucket_mode("validation_t06"),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    map_cache: dict[MapCacheKey, Any] = {}
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
                features = _policy_features_from_observation(obs, feature_mode=str(feature_mode)).reshape(1, -1)
                scalar = (features - mean) / std
                with torch.no_grad():
                    action = float(model(torch.as_tensor(scalar, dtype=torch.float32, device=device)).detach().cpu().numpy()[0, 0])
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
        except Exception as exc:  # noqa: BLE001 - smoke metric should record failures.
            counts["runtime_error"] += 1
            episode_rows.append(
                {
                    "source_row_index": int(source_row),
                    "query_id": str(row["query_id"]),
                    "success": False,
                    "collision": False,
                    "truncated": False,
                    "steps": 0,
                    "failure_reason": f"runtime_error:{type(exc).__name__}",
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


def _observation_config_record(config: ObservationConfig) -> dict[str, Any]:
    return {
        "patch_size_m": float(config.patch_size_m),
        "patch_cells": int(config.patch_cells),
        "include_edt": bool(config.include_edt),
        "edt_clip_m": float(config.edt_clip_m),
    }


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop training.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
