from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.main_evaluation import MainEvaluationConfig, run_main_evaluation


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Run ForestNav T14 main evaluation.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--queries-per-bucket", type=int, default=100)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--methods", default=",".join(MainEvaluationConfig().methods))
    parser.add_argument("--distance-bins", default="8:12,12:16,16:20,20:")
    parser.add_argument("--bootstrap-resamples", type=int, default=5_000)
    parser.add_argument("--md-dqn-source-dir", type=Path, default=None)
    parser.add_argument("--md-dqn-checkpoint", type=Path, default=None)
    parser.add_argument("--md-dqn-algo", default="cnn-dqn")
    parser.add_argument("--md-dqn-device", default="cpu")
    parser.add_argument("--md-dqn-max-steps", type=int, default=600)
    parser.add_argument("--allow-unreviewed-cutpoints", action="store_true")
    parser.add_argument("--allow-missing-md-dqn", action="store_true")
    parser.add_argument("--no-enforce-t14-scale", action="store_true")
    args = parser.parse_args(argv)

    config = MainEvaluationConfig(
        seed=int(args.seed),
        queries_per_bucket=int(args.queries_per_bucket),
        seed_count=int(args.seed_count),
        queries_per_map=int(args.queries_per_map),
        methods=tuple(part.strip() for part in str(args.methods).split(",") if part.strip()),
        distance_bins=parse_distance_bins(str(args.distance_bins)),
        md_dqn_source_dir=args.md_dqn_source_dir,
        md_dqn_checkpoint_path=args.md_dqn_checkpoint,
        md_dqn_algo=str(args.md_dqn_algo),
        md_dqn_device=str(args.md_dqn_device),
        md_dqn_max_steps=int(args.md_dqn_max_steps),
        allow_unreviewed_cutpoints=bool(args.allow_unreviewed_cutpoints),
        allow_missing_md_dqn=bool(args.allow_missing_md_dqn),
        enforce_t14_scale=not bool(args.no_enforce_t14_scale),
        bootstrap_resamples=int(args.bootstrap_resamples),
    )
    result = run_main_evaluation(
        args.output_dir,
        config=config,
        source_head=_source_head(),
        command=" ".join(["python -m forest_n3p.scripts.run_main_evaluation", *_quote_args(raw_argv)]),
    )
    print(
        json.dumps(
            {
                "output_dir": str(result.output_dir),
                "record_count": len(result.records),
                "query_count": len(result.queries),
                "status": result.verdict["status"],
                "formal_acceptance": result.verdict["formal_acceptance"],
                "report": str(result.output_paths["report_md"]),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop the run.
        return "unknown"


def _quote_args(argv: list[str] | None) -> list[str]:
    if argv is None:
        return []
    return [str(item) for item in argv]


if __name__ == "__main__":
    raise SystemExit(main())
