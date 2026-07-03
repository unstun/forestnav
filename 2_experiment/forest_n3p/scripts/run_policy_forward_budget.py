from __future__ import annotations

import argparse
import json
import math
import os
import platform
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


MODEL_NAMES = ("tiny_mlp", "small_cnn", "compact_cnn_mlp")


AGGREGATE_SCHEMA = pa.schema(
    [
        ("model_name", pa.string()),
        ("device", pa.string()),
        ("shape_label", pa.string()),
        ("batch_size", pa.int64()),
        ("patch_cells", pa.int64()),
        ("patch_extent_m", pa.float64()),
        ("patch_channels", pa.int64()),
        ("range_bins", pa.int64()),
        ("scalar_dim", pa.int64()),
        ("action_dim", pa.int64()),
        ("parameter_count", pa.int64()),
        ("warmup_iterations", pa.int64()),
        ("timed_iterations", pa.int64()),
        ("torch_num_threads", pa.int64()),
        ("forward_mean_ms", pa.float64()),
        ("forward_p50_ms", pa.float64()),
        ("forward_p90_ms", pa.float64()),
        ("forward_p95_ms", pa.float64()),
        ("forward_p99_ms", pa.float64()),
        ("forward_max_ms", pa.float64()),
        ("per_item_p50_ms", pa.float64()),
        ("per_item_p95_ms", pa.float64()),
        ("ratio_to_d01_attempt_p50", pa.float64()),
        ("ratio_to_d01_attempt_p95", pa.float64()),
        ("source_head", pa.string()),
    ]
)


SAMPLE_SCHEMA = pa.schema(
    [
        ("model_name", pa.string()),
        ("device", pa.string()),
        ("shape_label", pa.string()),
        ("batch_size", pa.int64()),
        ("iteration", pa.int64()),
        ("forward_ms", pa.float64()),
        ("source_head", pa.string()),
    ]
)


@dataclass(frozen=True)
class ObservationShape:
    label: str
    resolution_m: float
    goal_annulus_max_radius_m: float
    footprint_length_m: float
    footprint_width_m: float
    patch_cells: int
    patch_extent_m: float
    patch_channels: int
    range_bins: int
    scalar_dim: int
    action_dim: int
    rationale: tuple[str, ...]


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    if bool(args.allow_duplicate_openmp):
        os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

    torch = _load_torch()
    source_head = str(args.source_head) if args.source_head else _source_head()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if int(args.threads) > 0:
        torch.set_num_threads(int(args.threads))

    d01_reference = _load_d01_reference(Path(args.d01_summary))
    shapes = _observation_shapes_from_args(args)
    model_names = _parse_choice_list(str(args.models), MODEL_NAMES)
    devices = _resolve_devices(torch, str(args.devices))
    batch_sizes = _parse_positive_int_list(str(args.batch_sizes), name="batch-sizes")

    aggregate_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    for device_name in devices:
        device = torch.device(device_name)
        for shape in shapes:
            for model_name in model_names:
                model = _build_model(torch, model_name, shape).to(device)
                model.eval()
                parameter_count = _parameter_count(model)
                for batch_size in batch_sizes:
                    inputs = _make_inputs(torch, model_name, shape, batch_size, device)
                    timings = _measure_forward_ms(
                        torch,
                        model,
                        inputs,
                        device_name=device_name,
                        warmup_iterations=int(args.warmup_iterations),
                        timed_iterations=int(args.timed_iterations),
                    )
                    stats = _series_stats(timings)
                    row = {
                        "model_name": model_name,
                        "device": device_name,
                        "shape_label": shape.label,
                        "batch_size": int(batch_size),
                        "patch_cells": int(shape.patch_cells),
                        "patch_extent_m": float(shape.patch_extent_m),
                        "patch_channels": int(shape.patch_channels),
                        "range_bins": int(shape.range_bins),
                        "scalar_dim": int(shape.scalar_dim),
                        "action_dim": int(shape.action_dim),
                        "parameter_count": int(parameter_count),
                        "warmup_iterations": int(args.warmup_iterations),
                        "timed_iterations": int(args.timed_iterations),
                        "torch_num_threads": int(torch.get_num_threads()),
                        "forward_mean_ms": stats["mean"],
                        "forward_p50_ms": stats["p50"],
                        "forward_p90_ms": stats["p90"],
                        "forward_p95_ms": stats["p95"],
                        "forward_p99_ms": stats["p99"],
                        "forward_max_ms": stats["max"],
                        "per_item_p50_ms": stats["p50"] / float(batch_size),
                        "per_item_p95_ms": stats["p95"] / float(batch_size),
                        "ratio_to_d01_attempt_p50": _ratio(stats["p50"], d01_reference["attempt_total_time_p50_ms"]),
                        "ratio_to_d01_attempt_p95": _ratio(stats["p95"], d01_reference["attempt_total_time_p95_ms"]),
                        "source_head": source_head,
                    }
                    aggregate_rows.append(row)
                    for iteration, forward_ms in enumerate(timings):
                        sample_rows.append(
                            {
                                "model_name": model_name,
                                "device": device_name,
                                "shape_label": shape.label,
                                "batch_size": int(batch_size),
                                "iteration": int(iteration),
                                "forward_ms": float(forward_ms),
                                "source_head": source_head,
                            }
                        )

    aggregate_path = output_dir / "forward_budget_records.parquet"
    sample_path = output_dir / "forward_budget_samples.parquet"
    pq.write_table(pa.Table.from_pylist(aggregate_rows, schema=AGGREGATE_SCHEMA), aggregate_path)
    pq.write_table(pa.Table.from_pylist(sample_rows, schema=SAMPLE_SCHEMA), sample_path)

    summary = _summary_payload(
        args=args,
        raw_argv=raw_argv,
        source_head=source_head,
        output_dir=output_dir,
        aggregate_path=aggregate_path,
        sample_path=sample_path,
        aggregate_rows=aggregate_rows,
        shapes=shapes,
        d01_reference=d01_reference,
        torch=torch,
        devices=devices,
    )
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(_stdout_summary(summary), indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Module2 D02 neural policy forward-pass budget benchmark.")
    parser.add_argument("--output-dir", type=Path, default=Path("0_trials/module2_cost_accounting/d02_policy_forward_budget"))
    parser.add_argument("--d01-summary", type=Path, default=Path("0_trials/module2_cost_accounting/d01_analytic_cost_distribution/summary.json"))
    parser.add_argument("--devices", default="cpu", help="Comma list of cpu,cuda,mps, or auto.")
    parser.add_argument("--models", default="tiny_mlp,small_cnn,compact_cnn_mlp")
    parser.add_argument("--batch-sizes", default="1,8,32,128")
    parser.add_argument("--patch-cells", default="auto,128", help="Comma list of positive ints or auto.")
    parser.add_argument("--resolution-m", type=float, default=0.1)
    parser.add_argument("--goal-annulus-max-radius-m", type=float, default=3.0)
    parser.add_argument("--footprint-length-m", type=float, default=0.924)
    parser.add_argument("--footprint-width-m", type=float, default=0.740)
    parser.add_argument("--patch-channels", type=int, default=2)
    parser.add_argument("--range-bins-mode", choices=("match_patch", "fixed64"), default="match_patch")
    parser.add_argument("--scalar-dim", type=int, default=8)
    parser.add_argument("--action-dim", type=int, default=1)
    parser.add_argument("--warmup-iterations", type=int, default=200)
    parser.add_argument("--timed-iterations", type=int, default=1500)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260703)
    parser.add_argument("--source-head", default=None)
    parser.add_argument(
        "--allow-duplicate-openmp",
        action="store_true",
        help="Set KMP_DUPLICATE_LIB_OK=TRUE before importing torch. Use only for local Mac import conflicts.",
    )
    args = parser.parse_args(argv)
    _validate_args(args)
    return args


def _validate_args(args: argparse.Namespace) -> None:
    for name in ("resolution_m", "goal_annulus_max_radius_m", "footprint_length_m", "footprint_width_m"):
        value = float(getattr(args, name))
        if not (math.isfinite(value) and value > 0.0):
            raise ValueError(f"--{name.replace('_', '-')} must be finite and positive")
    for name in ("patch_channels", "scalar_dim", "action_dim", "warmup_iterations", "timed_iterations"):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    if int(args.threads) < 0:
        raise ValueError("--threads must be non-negative")


def derive_observation_shapes(
    *,
    patch_cells_spec: str,
    resolution_m: float,
    goal_annulus_max_radius_m: float,
    footprint_length_m: float,
    footprint_width_m: float,
    patch_channels: int,
    range_bins_mode: str,
    scalar_dim: int,
    action_dim: int,
) -> tuple[ObservationShape, ...]:
    base_cells = next_power_of_two(math.ceil((2.0 * goal_annulus_max_radius_m) / resolution_m))
    footprint_radius = 0.5 * math.hypot(float(footprint_length_m), float(footprint_width_m))
    margin_cells = next_power_of_two(math.ceil((2.0 * (goal_annulus_max_radius_m + footprint_radius)) / resolution_m))
    specs: list[tuple[str, int, tuple[str, ...]]] = []
    for token in _parse_str_list(patch_cells_spec):
        if token == "auto":
            specs.append(
                (
                    "annulus_auto",
                    base_cells,
                    (
                        f"resolution_m={resolution_m} from MainEvaluationConfig",
                        f"goal_annulus_max_radius_m={goal_annulus_max_radius_m} from C02 oracle B candidate defaults",
                        "patch_cells is the next power of two covering the 2R goal-annulus diameter",
                    ),
                )
            )
        elif token == "margin_auto":
            specs.append(
                (
                    "footprint_margin_auto",
                    margin_cells,
                    (
                        f"resolution_m={resolution_m} from MainEvaluationConfig",
                        f"goal_annulus_max_radius_m={goal_annulus_max_radius_m} plus two-circle footprint radius {footprint_radius:.3f}m",
                        "patch_cells is the next power of two covering the conservative footprint-margin diameter",
                    ),
                )
            )
        else:
            cells = int(token)
            specs.append(
                (
                    f"manual_{cells}",
                    cells,
                    (
                        f"manual patch_cells={cells}; included as an explicit sensitivity setting",
                        f"resolution_m={resolution_m}; extent_m={cells * resolution_m:.3f}",
                    ),
                )
            )

    out: list[ObservationShape] = []
    seen: set[tuple[str, int]] = set()
    for label, cells, rationale in specs:
        if cells <= 0:
            raise ValueError("patch cells must be positive")
        key = (label, cells)
        if key in seen:
            continue
        seen.add(key)
        range_bins = 64 if range_bins_mode == "fixed64" else int(cells)
        out.append(
            ObservationShape(
                label=label,
                resolution_m=float(resolution_m),
                goal_annulus_max_radius_m=float(goal_annulus_max_radius_m),
                footprint_length_m=float(footprint_length_m),
                footprint_width_m=float(footprint_width_m),
                patch_cells=int(cells),
                patch_extent_m=float(cells) * float(resolution_m),
                patch_channels=int(patch_channels),
                range_bins=int(range_bins),
                scalar_dim=int(scalar_dim),
                action_dim=int(action_dim),
                rationale=tuple(rationale),
            )
        )
    return tuple(out)


def next_power_of_two(value: int) -> int:
    if int(value) <= 0:
        raise ValueError("value must be positive")
    return 1 << (int(value) - 1).bit_length()


def _observation_shapes_from_args(args: argparse.Namespace) -> tuple[ObservationShape, ...]:
    return derive_observation_shapes(
        patch_cells_spec=str(args.patch_cells),
        resolution_m=float(args.resolution_m),
        goal_annulus_max_radius_m=float(args.goal_annulus_max_radius_m),
        footprint_length_m=float(args.footprint_length_m),
        footprint_width_m=float(args.footprint_width_m),
        patch_channels=int(args.patch_channels),
        range_bins_mode=str(args.range_bins_mode),
        scalar_dim=int(args.scalar_dim),
        action_dim=int(args.action_dim),
    )


def _load_torch():
    try:
        import torch
        from torch import nn
    except Exception as exc:  # noqa: BLE001 - dependency error should be explicit to the runner.
        raise RuntimeError(
            "PyTorch is required for D02.1 forward budget. "
            "If this Mac hits OpenMP duplicate runtime during import, rerun with --allow-duplicate-openmp "
            "and record the limitation in the artifact."
        ) from exc
    torch.nn = nn
    return torch


def _build_model(torch, model_name: str, shape: ObservationShape):
    nn = torch.nn
    if model_name == "tiny_mlp":
        return nn.Sequential(
            nn.Linear(shape.range_bins + shape.scalar_dim, 64),
            nn.SiLU(),
            nn.Linear(64, 64),
            nn.SiLU(),
            nn.Linear(64, shape.action_dim),
        )
    if model_name == "small_cnn":
        return SmallCnnPolicy(torch, nn, shape)
    if model_name == "compact_cnn_mlp":
        return CompactCnnMlpPolicy(torch, nn, shape)
    raise ValueError(f"unknown model: {model_name}")


class SmallCnnPolicy:
    def __new__(cls, torch, nn, shape: ObservationShape):
        class _SmallCnnPolicy(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Conv2d(shape.patch_channels, 16, kernel_size=5, stride=2, padding=2),
                    nn.SiLU(),
                    nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
                    nn.SiLU(),
                    nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
                    nn.SiLU(),
                    nn.AdaptiveAvgPool2d((4, 4)),
                    nn.Flatten(),
                )
                self.head = nn.Sequential(
                    nn.Linear(64 * 4 * 4 + shape.scalar_dim, 128),
                    nn.SiLU(),
                    nn.Linear(128, 64),
                    nn.SiLU(),
                    nn.Linear(64, shape.action_dim),
                )

            def forward(self, patch, scalar):
                latent = self.encoder(patch)
                return self.head(torch.cat((latent, scalar), dim=1))

        return _SmallCnnPolicy()


class CompactCnnMlpPolicy:
    def __new__(cls, torch, nn, shape: ObservationShape):
        class _CompactCnnMlpPolicy(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Conv2d(shape.patch_channels, 8, kernel_size=5, stride=2, padding=2),
                    nn.SiLU(),
                    nn.Conv2d(8, 16, kernel_size=3, stride=2, padding=1),
                    nn.SiLU(),
                    nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
                    nn.SiLU(),
                    nn.AdaptiveAvgPool2d((2, 2)),
                    nn.Flatten(),
                )
                self.head = nn.Sequential(
                    nn.Linear(32 * 2 * 2 + shape.scalar_dim, 64),
                    nn.SiLU(),
                    nn.Linear(64, shape.action_dim),
                )

            def forward(self, patch, scalar):
                latent = self.encoder(patch)
                return self.head(torch.cat((latent, scalar), dim=1))

        return _CompactCnnMlpPolicy()


def _make_inputs(torch, model_name: str, shape: ObservationShape, batch_size: int, device):
    generator = torch.Generator(device=device)
    generator.manual_seed(20260703 + int(batch_size) + int(shape.patch_cells))
    if model_name == "tiny_mlp":
        return (torch.randn((batch_size, shape.range_bins + shape.scalar_dim), device=device, generator=generator),)
    patch = torch.randn(
        (batch_size, shape.patch_channels, shape.patch_cells, shape.patch_cells),
        device=device,
        generator=generator,
    )
    scalar = torch.randn((batch_size, shape.scalar_dim), device=device, generator=generator)
    return (patch, scalar)


def _measure_forward_ms(
    torch,
    model,
    inputs: tuple[Any, ...],
    *,
    device_name: str,
    warmup_iterations: int,
    timed_iterations: int,
) -> list[float]:
    timings: list[float] = []
    with torch.inference_mode():
        for _ in range(warmup_iterations):
            _ = model(*inputs)
        _synchronize(torch, device_name)
        for _ in range(timed_iterations):
            start_ns = time.perf_counter_ns()
            _ = model(*inputs)
            _synchronize(torch, device_name)
            end_ns = time.perf_counter_ns()
            timings.append((float(end_ns - start_ns)) / 1_000_000.0)
    return timings


def _synchronize(torch, device_name: str) -> None:
    if device_name.startswith("cuda"):
        torch.cuda.synchronize()
    elif device_name == "mps" and hasattr(torch, "mps") and hasattr(torch.mps, "synchronize"):
        torch.mps.synchronize()


def _parameter_count(model) -> int:
    return int(sum(parameter.numel() for parameter in model.parameters()))


def _resolve_devices(torch, devices_spec: str) -> tuple[str, ...]:
    requested = _parse_str_list(devices_spec)
    if requested == ("auto",):
        devices = ["cpu"]
        if torch.cuda.is_available():
            devices.append("cuda")
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            devices.append("mps")
        return tuple(devices)
    out: list[str] = []
    for device in requested:
        if device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("requested cuda but torch.cuda.is_available() is false")
        if device == "mps" and not (hasattr(torch.backends, "mps") and torch.backends.mps.is_available()):
            raise RuntimeError("requested mps but torch.backends.mps.is_available() is false")
        if device not in {"cpu", "cuda", "mps"}:
            raise ValueError(f"unsupported device: {device}")
        out.append(device)
    return tuple(dict.fromkeys(out))


def _load_d01_reference(path: Path) -> dict[str, float | str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    fields = payload["overall"]["fields"]["analytic_total_time_s"]
    return {
        "path": str(path),
        "source_head": str(payload.get("source_head", "unknown")),
        "attempt_total_time_p50_ms": float(fields["p50"]) * 1000.0,
        "attempt_total_time_p95_ms": float(fields["p95"]) * 1000.0,
        "attempt_total_time_p99_ms": float(fields["p99"]) * 1000.0,
    }


def _summary_payload(
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    source_head: str,
    output_dir: Path,
    aggregate_path: Path,
    sample_path: Path,
    aggregate_rows: list[dict[str, Any]],
    shapes: tuple[ObservationShape, ...],
    d01_reference: dict[str, Any],
    torch,
    devices: tuple[str, ...],
) -> dict[str, Any]:
    best_by_model = {}
    for model_name in sorted({str(row["model_name"]) for row in aggregate_rows}):
        rows = [row for row in aggregate_rows if row["model_name"] == model_name and row["batch_size"] == 1]
        best = min(rows, key=lambda row: float(row["forward_p50_ms"])) if rows else None
        best_by_model[model_name] = best
    return {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python": sys.version,
        },
        "source_head": source_head,
        "command": " ".join(["python -m forest_n3p.scripts.run_policy_forward_budget", *raw_argv]),
        "output_dir": str(output_dir),
        "outputs": {
            "aggregate_records": str(aggregate_path),
            "sample_records": str(sample_path),
        },
        "torch": {
            "version": str(torch.__version__),
            "num_threads": int(torch.get_num_threads()),
            "cuda_available": bool(torch.cuda.is_available()),
            "mps_available": bool(hasattr(torch.backends, "mps") and torch.backends.mps.is_available()),
            "devices_benchmarked": list(devices),
        },
        "environment_flags": {
            "allow_duplicate_openmp": bool(args.allow_duplicate_openmp),
            "KMP_DUPLICATE_LIB_OK": os.environ.get("KMP_DUPLICATE_LIB_OK"),
        },
        "config": {
            "models": _parse_str_list(str(args.models)),
            "batch_sizes": _parse_positive_int_list(str(args.batch_sizes), name="batch-sizes"),
            "warmup_iterations": int(args.warmup_iterations),
            "timed_iterations": int(args.timed_iterations),
            "threads": int(args.threads),
            "range_bins_mode": str(args.range_bins_mode),
        },
        "shape_rationale": [asdict(shape) for shape in shapes],
        "d01_reference": d01_reference,
        "aggregate_record_count": int(len(aggregate_rows)),
        "sample_record_count": int(sum(int(row["timed_iterations"]) for row in aggregate_rows)),
        "best_batch1_by_model": best_by_model,
        "boundary": {
            "allowed": (
                "This artifact measures neural policy forward-pass latency only.",
                "Batch=1 numbers are the relevant direct comparator for one analytic expansion call.",
                "Batched numbers are only a throughput hint for later vectorized evaluation.",
            ),
            "not_included": (
                "rollout collision checking",
                "terminal Reeds-Shepp check",
                "planner integration overhead",
                "trained policy quality",
            ),
            "next_gate_input": "D02.2/D02.3 must add rollout collision and terminal RS costs before Gate #1.",
        },
    }


def _stdout_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": summary["status"],
        "output_dir": summary["output_dir"],
        "aggregate_record_count": summary["aggregate_record_count"],
        "sample_record_count": summary["sample_record_count"],
        "d01_attempt_p50_ms": summary["d01_reference"]["attempt_total_time_p50_ms"],
        "best_batch1_by_model": {
            key: {
                "device": value["device"],
                "shape_label": value["shape_label"],
                "p50_ms": value["forward_p50_ms"],
                "p95_ms": value["forward_p95_ms"],
                "ratio_to_d01_p50": value["ratio_to_d01_attempt_p50"],
            }
            for key, value in summary["best_batch1_by_model"].items()
            if value is not None
        },
    }


def _series_stats(values: Sequence[float]) -> dict[str, float]:
    series = pd.Series([float(value) for value in values])
    return {
        "mean": float(series.mean()),
        "p50": float(series.quantile(0.50)),
        "p90": float(series.quantile(0.90)),
        "p95": float(series.quantile(0.95)),
        "p99": float(series.quantile(0.99)),
        "max": float(series.max()),
    }


def _ratio(value: float, reference: float) -> float:
    return float(value) / float(reference) if float(reference) > 0.0 else float("nan")


def _parse_choice_list(spec: str, choices: tuple[str, ...]) -> tuple[str, ...]:
    values = _parse_str_list(spec)
    unknown = [value for value in values if value not in choices]
    if unknown:
        raise ValueError(f"unsupported values {unknown}; choices={choices}")
    return values


def _parse_str_list(spec: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in str(spec).split(",") if part.strip())
    if not values:
        raise ValueError("list argument must not be empty")
    return values


def _parse_positive_int_list(spec: str, *, name: str) -> tuple[int, ...]:
    values = tuple(int(part) for part in _parse_str_list(spec))
    if any(value <= 0 for value in values):
        raise ValueError(f"--{name} values must be positive")
    return values


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop the benchmark.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
