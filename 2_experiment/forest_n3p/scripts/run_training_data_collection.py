from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.training_data import (
    TrainingDataConfig,
    default_workers,
    run_training_data_collection,
    source_head,
    write_training_data_outputs,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the T08 F-N3P training dataset collection.")
    parser.add_argument("--output-dir", type=Path, default=Path("2_experiment/forest_n3p/datasets/t08_training_dataset"))
    parser.add_argument("--report-path", type=Path, default=Path(".pipeline/experiments/20260620_t08_training_dataset.md"))
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--map-count", type=int, default=2000)
    parser.add_argument("--queries-per-map", type=int, default=40)
    parser.add_argument("--width-cells", type=int, default=300)
    parser.add_argument("--height-cells", type=int, default=300)
    parser.add_argument("--teacher-timeout-s", type=float, default=2.5)
    parser.add_argument("--teacher-wall-timeout-s", type=float, default=10.0)
    parser.add_argument("--teacher-max-nodes", type=int, default=15_000)
    parser.add_argument("--map-generation-wall-timeout-s", type=float, default=30.0)
    parser.add_argument("--max-query-sample-attempts", type=int, default=800)
    parser.add_argument("--distance-bins", type=str, default="8:12,12:16,16:20,20:")
    parser.add_argument("--path-sample-step-m", type=float, default=0.2)
    parser.add_argument("--l-min-m", type=float, default=1.0)
    parser.add_argument("--l-max-m", type=float, default=8.0)
    parser.add_argument("--total-sample-target", type=int, default=100_000)
    parser.add_argument("--total-sample-lower-bound", type=int, default=90_000)
    parser.add_argument("--min-samples-per-bucket", type=int, default=10_000)
    parser.add_argument("--workers", type=int, default=default_workers())
    parser.add_argument("--progress-every", type=int, default=50)
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--execution-host", type=str, default=None)
    parser.add_argument("--command", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    config = TrainingDataConfig(
        seed=int(args.seed),
        map_count=int(args.map_count),
        queries_per_map=int(args.queries_per_map),
        width_cells=int(args.width_cells),
        height_cells=int(args.height_cells),
        teacher_timeout_s=float(args.teacher_timeout_s),
        teacher_wall_timeout_s=float(args.teacher_wall_timeout_s),
        teacher_max_nodes=int(args.teacher_max_nodes),
        map_generation_wall_timeout_s=float(args.map_generation_wall_timeout_s),
        max_query_sample_attempts=int(args.max_query_sample_attempts),
        distance_bins=parse_distance_bins(args.distance_bins),
        path_sample_step_m=float(args.path_sample_step_m),
        l_min_m=float(args.l_min_m),
        l_max_m=float(args.l_max_m),
        total_sample_target=int(args.total_sample_target),
        total_sample_lower_bound=int(args.total_sample_lower_bound),
        min_samples_per_bucket=int(args.min_samples_per_bucket),
    )
    run = run_training_data_collection(
        config,
        workers=int(args.workers),
        progress_every=int(args.progress_every),
    )
    command = args.command or " ".join(sys.argv)
    files = write_training_data_outputs(
        run,
        args.output_dir,
        report_path=args.report_path,
        source_head=args.source_head or source_head(),
        execution_host=args.execution_host or socket.gethostname(),
        command=command,
    )
    print(files["report_md"])
    print(files["summary_json"])
    print(f"total_samples={run.summary['total_samples']}")
    print(f"sample_count_by_bucket={run.summary['sample_count_by_bucket']}")
    print(f"label_failure_rate={run.summary['label_failure_rate']}")
    print(f"acceptance_pass={run.summary['acceptance_pass']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
