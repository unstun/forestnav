from __future__ import annotations

import argparse
import socket
import subprocess
from pathlib import Path

from forest_n3p.pilot_labeling import PilotConfig, run_label_pilot, write_pilot_outputs


def _source_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the T05 F-N3P label pilot experiment.")
    parser.add_argument("--output-dir", type=Path, default=Path(".pipeline/experiments/20260620_t05_label_pilot"))
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--map-count", type=int, default=20)
    parser.add_argument("--queries-per-map", type=int, default=10)
    parser.add_argument("--width-cells", type=int, default=300)
    parser.add_argument("--height-cells", type=int, default=300)
    parser.add_argument("--teacher-timeout-s", type=float, default=2.5)
    parser.add_argument("--teacher-max-nodes", type=int, default=15_000)
    parser.add_argument("--min-query-distance-m", type=float, default=8.0)
    parser.add_argument("--path-sample-step-m", type=float, default=0.2)
    parser.add_argument("--l-min-m", type=float, default=1.5)
    parser.add_argument("--l-max-m", type=float, default=8.0)
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--execution-host", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    config = PilotConfig(
        seed=int(args.seed),
        map_count=int(args.map_count),
        queries_per_map=int(args.queries_per_map),
        width_cells=int(args.width_cells),
        height_cells=int(args.height_cells),
        teacher_timeout_s=float(args.teacher_timeout_s),
        teacher_max_nodes=int(args.teacher_max_nodes),
        min_query_distance_m=float(args.min_query_distance_m),
        path_sample_step_m=float(args.path_sample_step_m),
        l_min_m=float(args.l_min_m),
        l_max_m=float(args.l_max_m),
    )
    run = run_label_pilot(config)
    files = write_pilot_outputs(
        run,
        args.output_dir,
        source_head=args.source_head or _source_head(),
        execution_host=args.execution_host or socket.gethostname(),
    )
    print(files["report_md"])
    print(files["summary_json"])
    print(f"teacher_success_rate={run.summary['teacher_success_rate']}")
    print(f"label_failure_rate={run.summary['label_failure_rate']}")
    print(f"label_failure_rate_pass={run.summary['label_failure_rate_pass']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
