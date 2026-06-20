from __future__ import annotations

import argparse
import socket
import subprocess
from pathlib import Path

from forest_n3p.difficulty_calibration import (
    BucketRule,
    CalibrationConfig,
    parse_distance_bins,
    run_difficulty_calibration,
    write_calibration_outputs,
)


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
    parser = argparse.ArgumentParser(description="Run the T06 F-N3P difficulty-axis calibration.")
    parser.add_argument("--output-dir", type=Path, default=Path(".pipeline/experiments/20260620_t06_difficulty_calibration"))
    parser.add_argument(
        "--supplement-path",
        type=Path,
        default=Path(".pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md"),
    )
    parser.add_argument("--no-contract-supplement", action="store_true")
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--maps-per-density", type=int, default=3)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--distance-map-count", type=int, default=3)
    parser.add_argument("--queries-per-distance-bin", type=int, default=8)
    parser.add_argument("--distance-bins", type=str, default="4:8,8:12,12:16,16:20,20:")
    parser.add_argument("--width-cells", type=int, default=300)
    parser.add_argument("--height-cells", type=int, default=300)
    parser.add_argument("--teacher-timeout-s", type=float, default=2.5)
    parser.add_argument("--teacher-max-nodes", type=int, default=15_000)
    parser.add_argument("--density-min-query-distance-m", type=float, default=8.0)
    parser.add_argument("--max-query-sample-attempts", type=int, default=800)
    parser.add_argument("--easy-success-rate-min", type=float, default=0.85)
    parser.add_argument("--easy-median-time-s-max", type=float, default=0.50)
    parser.add_argument("--easy-timeout-rate-max", type=float, default=0.10)
    parser.add_argument("--extreme-success-rate-max", type=float, default=0.70)
    parser.add_argument("--extreme-timeout-rate-min", type=float, default=0.30)
    parser.add_argument("--extreme-success-rate-hard-max", type=float, default=0.60)
    parser.add_argument("--extreme-timeout-rate-hard-min", type=float, default=0.50)
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--execution-host", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    rule = BucketRule(
        easy_success_rate_min=float(args.easy_success_rate_min),
        easy_median_time_s_max=float(args.easy_median_time_s_max),
        easy_timeout_rate_max=float(args.easy_timeout_rate_max),
        extreme_success_rate_max=float(args.extreme_success_rate_max),
        extreme_timeout_rate_min=float(args.extreme_timeout_rate_min),
        extreme_success_rate_hard_max=float(args.extreme_success_rate_hard_max),
        extreme_timeout_rate_hard_min=float(args.extreme_timeout_rate_hard_min),
    )
    config = CalibrationConfig(
        seed=int(args.seed),
        maps_per_density=int(args.maps_per_density),
        queries_per_map=int(args.queries_per_map),
        distance_map_count=int(args.distance_map_count),
        queries_per_distance_bin=int(args.queries_per_distance_bin),
        distance_bins=parse_distance_bins(str(args.distance_bins)),
        width_cells=int(args.width_cells),
        height_cells=int(args.height_cells),
        teacher_timeout_s=float(args.teacher_timeout_s),
        teacher_max_nodes=int(args.teacher_max_nodes),
        density_min_query_distance_m=float(args.density_min_query_distance_m),
        max_query_sample_attempts=int(args.max_query_sample_attempts),
        bucket_rule=rule,
    )
    run = run_difficulty_calibration(config)
    supplement_path = None if args.no_contract_supplement else args.supplement_path
    files = write_calibration_outputs(
        run,
        args.output_dir,
        source_head=args.source_head or _source_head(),
        execution_host=args.execution_host or socket.gethostname(),
        supplement_path=supplement_path,
    )
    print(files["report_md"])
    print(files["summary_json"])
    if files.get("supplement_path"):
        print(files["supplement_path"])
    print(f"density_bucket_separation_pass={run.summary['density_cutpoints']['bucket_separation_pass']}")
    print(f"distance_bucket_separation_pass={run.summary['distance_cutpoints']['bucket_separation_pass']}")
    print(f"bucket_separation_pass={run.summary['bucket_separation_pass']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
