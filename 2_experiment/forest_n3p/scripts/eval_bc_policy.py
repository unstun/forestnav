from __future__ import annotations

import argparse
import json
import random
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pyarrow.parquet as pq

from forest_n3p.rl_rs.obs import ObservationConfig
from forest_n3p.scripts.train_bc_policy import (
    _build_scalar_steering_mlp,
    _closed_loop_metrics,
    _load_torch,
    _resolve_device,
    _split_by_source,
)
from forest_n3p.third_party.pathplan import AckermannParams


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    torch = _load_torch()
    device = _resolve_device(torch, str(args.device))
    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    feature_mode = str(checkpoint["feature_mode"])
    model = _build_scalar_steering_mlp(
        torch=torch,
        input_dim=int(checkpoint["input_dim"]),
        hidden_dims=tuple(int(x) for x in checkpoint["hidden_dims"]),
        max_steer=float(checkpoint["max_steer"]),
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.to(device)
    model.eval()

    rows = pq.read_table(args.dataset).to_pylist()
    split = _split_by_source(rows, val_fraction=float(args.val_fraction), seed=int(args.seed))
    val_rows = [row for row in rows if int(row["source_row_index"]) in split["val_sources"]]
    full_val_rows = list(val_rows)
    val_rows = _bounded_rows(val_rows, max_rows=args.max_val_rows, seed=int(args.seed) + 1)
    params = AckermannParams(wheelbase=float(args.wheelbase_m), min_turn_radius=float(args.turning_radius_m))
    obs_config = _observation_config_from_checkpoint(checkpoint)
    eval_args = argparse.Namespace(
        rollout_max_steps=int(args.rollout_max_steps),
        rollout_action_step_m=float(args.rollout_action_step_m),
        collision_sample_step_m=float(args.collision_sample_step_m),
        theta_bins=int(args.theta_bins),
    )
    metrics = _closed_loop_metrics(
        torch=torch,
        model=model,
        val_rows=val_rows,
        mean=np.asarray(checkpoint["feature_mean"], dtype=np.float32),
        std=np.asarray(checkpoint["feature_std"], dtype=np.float32),
        args=eval_args,
        params=params,
        feature_mode=feature_mode,
        obs_config=obs_config,
        device=device,
    )
    payload = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": str(args.source_head) if args.source_head else _source_head(),
        "command": " ".join(["python -m forest_n3p.scripts.eval_bc_policy", *raw_argv]),
        "checkpoint": str(args.checkpoint),
        "dataset": str(args.dataset),
        "dataset_rows": int(len(rows)),
        "full_val_rows": int(len(full_val_rows)),
        "full_val_source_rows": int(len(split["val_sources"])),
        "val_rows": int(len(val_rows)),
        "val_source_rows": int(len({int(row["source_row_index"]) for row in val_rows})),
        "feature_mode": feature_mode,
        "config": {
            "seed": int(args.seed),
            "val_fraction": float(args.val_fraction),
            "max_val_rows": args.max_val_rows if args.max_val_rows is None else int(args.max_val_rows),
            "rollout_max_steps": int(args.rollout_max_steps),
            "rollout_action_step_m": float(args.rollout_action_step_m),
            "collision_sample_step_m": float(args.collision_sample_step_m),
            "device": str(device),
            "theta_bins": int(args.theta_bins),
            "observation_config": _observation_config_record(obs_config),
        },
        "metrics": metrics,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Posthoc closed-loop evaluation for Module2 BC checkpoints.")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260703)
    parser.add_argument("--val-fraction", type=float, default=0.25)
    parser.add_argument("--max-val-rows", type=int, default=None)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--rollout-max-steps", type=int, default=96)
    parser.add_argument("--rollout-action-step-m", type=float, default=0.1)
    parser.add_argument("--collision-sample-step-m", type=float, default=0.05)
    parser.add_argument("--turning-radius-m", type=float, default=1.0)
    parser.add_argument("--wheelbase-m", type=float, default=0.6)
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)
    _validate_args(args)
    return args


def _validate_args(args: argparse.Namespace) -> None:
    if not args.checkpoint.exists():
        raise FileNotFoundError(args.checkpoint)
    if not args.dataset.exists():
        raise FileNotFoundError(args.dataset)
    if not (0.0 < float(args.val_fraction) < 1.0):
        raise ValueError("--val-fraction must be in (0, 1)")
    if args.max_val_rows is not None and int(args.max_val_rows) <= 0:
        raise ValueError("--max-val-rows must be positive when set")
    for name in ("rollout_max_steps", "theta_bins"):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    for name in ("rollout_action_step_m", "collision_sample_step_m", "turning_radius_m", "wheelbase_m"):
        if float(getattr(args, name)) <= 0.0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")


def _observation_config_from_checkpoint(checkpoint: dict[str, Any]) -> ObservationConfig:
    raw = dict(checkpoint.get("observation_config") or {})
    return ObservationConfig(
        patch_size_m=float(raw.get("patch_size_m", 6.4)),
        patch_cells=int(raw.get("patch_cells", 64)),
        include_edt=bool(raw.get("include_edt", True)),
        edt_clip_m=float(raw.get("edt_clip_m", 3.0)),
    )


def _bounded_rows(rows: list[dict[str, Any]], *, max_rows: int | None, seed: int) -> list[dict[str, Any]]:
    if max_rows is None or int(max_rows) >= len(rows):
        return rows
    rng = random.Random(int(seed))
    indices = sorted(rng.sample(range(len(rows)), int(max_rows)))
    return [rows[index] for index in indices]


def _observation_config_record(obs_config: ObservationConfig) -> dict[str, Any]:
    return {
        "patch_size_m": float(obs_config.patch_size_m),
        "patch_cells": int(obs_config.patch_cells),
        "include_edt": bool(obs_config.include_edt),
        "edt_clip_m": float(obs_config.edt_clip_m),
    }


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - eval provenance should not stop evaluation.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
