from __future__ import annotations

import argparse
import socket
import subprocess
import sys
from pathlib import Path

from forest_n3p.mlp import MlpTrainingConfig, render_training_report, train_mlp_model


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the T10 F-N3P MLP subgoal ablation model.")
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("2_experiment/forest_n3p/datasets/t08_training_dataset"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("2_experiment/forest_n3p/models/t10_mlp_subgoal"),
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path(".pipeline/experiments/20260620_t10_mlp_training.md"),
    )
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--hidden-dims", type=str, default="256,256,128")
    parser.add_argument("--val-fraction", type=float, default=0.10)
    parser.add_argument("--batch-size", type=int, default=2048)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--patience", type=int, default=25)
    parser.add_argument("--min-delta", type=float, default=1e-6)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--device", type=str, default="auto")
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--execution-host", type=str, default=None)
    parser.add_argument("--command", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    source_head_value = args.source_head or _source_head()
    execution_host = args.execution_host or socket.gethostname()
    command = args.command or " ".join(sys.argv)
    result = train_mlp_model(
        args.dataset_dir,
        args.output_dir,
        config=MlpTrainingConfig(
            seed=int(args.seed),
            hidden_dims=_parse_hidden_dims(args.hidden_dims),
            val_fraction=float(args.val_fraction),
            batch_size=int(args.batch_size),
            epochs=int(args.epochs),
            learning_rate=float(args.learning_rate),
            weight_decay=float(args.weight_decay),
            patience=int(args.patience),
            min_delta=float(args.min_delta),
            num_workers=int(args.num_workers),
            device=str(args.device),
        ),
        source_head=source_head_value,
        execution_host=execution_host,
        command=command,
    )
    args.report_path.parent.mkdir(parents=True, exist_ok=True)
    args.report_path.write_text(
        render_training_report(result, source_head=source_head_value, execution_host=execution_host),
        encoding="utf-8",
    )
    print(args.report_path)
    print(result.metadata_path)
    print(result.checkpoint_path)
    print(f"best_epoch={result.best_epoch}")
    print(f"best_val_loss={result.best_val_loss:.8f}")
    print(f"epochs_ran={result.epochs_ran}")
    print(f"device={result.device}")
    return 0


def _parse_hidden_dims(raw: str) -> tuple[int, int, int]:
    dims = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if len(dims) != 3:
        raise ValueError("--hidden-dims must contain exactly three comma-separated integers")
    return dims  # type: ignore[return-value]


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        diff = subprocess.check_output(["git", "diff", "--stat"], text=True, stderr=subprocess.DEVNULL).strip()
        staged = subprocess.check_output(["git", "diff", "--cached", "--stat"], text=True, stderr=subprocess.DEVNULL).strip()
        suffix = "+dirty" if diff or staged else ""
        return f"{head}{suffix}"
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
