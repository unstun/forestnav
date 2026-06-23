from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.generalization import GeneralizationConfig, run_generalization_evaluation


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Run ForestNav T16 OOD-density and RealMap generalization evaluation.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ood-queries-per-bucket", type=int, default=20)
    parser.add_argument("--realmap-queries-per-map", type=int, default=10)
    parser.add_argument("--seed-count", type=int, default=2)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260623)
    parser.add_argument("--methods", default="vanilla_ha,f_n3p_knn")
    parser.add_argument("--distance-bins", default="8:12,12:16,16:20,20:")
    parser.add_argument("--realmap-distance-bins", default="4:8,8:12,12:16,16:20,20:")
    parser.add_argument("--realmap-manifest-path", type=Path, default=GeneralizationConfig().realmap_manifest_path)
    parser.add_argument("--contract-path", type=Path, default=GeneralizationConfig().contract_path)
    parser.add_argument("--knn-library-dir", type=Path, default=GeneralizationConfig().knn_library_dir)
    parser.add_argument("--knn-dataset-dir", type=Path, default=GeneralizationConfig().knn_dataset_dir)
    parser.add_argument("--knn-feature-indices", default=None)
    parser.add_argument("--k-neighbors", type=int, default=20)
    parser.add_argument("--teacher-timeout-s", type=float, default=2.5)
    parser.add_argument("--teacher-max-nodes", type=int, default=15_000)
    parser.add_argument("--segment-timeout-s", type=float, default=1.0)
    parser.add_argument("--segment-max-nodes", type=int, default=2_000)
    parser.add_argument("--full-fallback-timeout-s", type=float, default=2.5)
    parser.add_argument("--full-fallback-max-nodes", type=int, default=15_000)
    parser.add_argument("--no-commit-verified-rs-segments", action="store_true")
    parser.add_argument("--max-steps-override", type=int, default=None)
    parser.add_argument("--disable-f1", action="store_true")
    parser.add_argument("--disable-f2", action="store_true")
    parser.add_argument("--disable-f3", action="store_true")
    parser.add_argument("--prediction-noise-sigma-m", type=float, default=0.0)
    parser.add_argument("--prediction-noise-seed", type=int, default=20260623)
    parser.add_argument("--bootstrap-resamples", type=int, default=1_000)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    cfg = GeneralizationConfig(
        seed=int(args.seed),
        ood_queries_per_bucket=int(args.ood_queries_per_bucket),
        realmap_queries_per_map=int(args.realmap_queries_per_map),
        seed_count=int(args.seed_count),
        queries_per_map=int(args.queries_per_map),
        methods=tuple(part.strip() for part in str(args.methods).split(",") if part.strip()),
        distance_bins=parse_distance_bins(str(args.distance_bins)),
        realmap_distance_bins=parse_distance_bins(str(args.realmap_distance_bins)),
        realmap_manifest_path=args.realmap_manifest_path,
        contract_path=args.contract_path,
        knn_library_dir=args.knn_library_dir,
        knn_dataset_dir=args.knn_dataset_dir,
        knn_feature_indices=_parse_int_tuple(args.knn_feature_indices),
        k_neighbors=int(args.k_neighbors),
        teacher_timeout_s=float(args.teacher_timeout_s),
        teacher_max_nodes=int(args.teacher_max_nodes),
        segment_timeout_s=float(args.segment_timeout_s),
        segment_max_nodes=int(args.segment_max_nodes),
        full_fallback_timeout_s=float(args.full_fallback_timeout_s),
        full_fallback_max_nodes=int(args.full_fallback_max_nodes),
        commit_verified_rs_segments=not bool(args.no_commit_verified_rs_segments),
        max_steps_override=args.max_steps_override,
        enable_f1=not bool(args.disable_f1),
        enable_f2=not bool(args.disable_f2),
        enable_f3=not bool(args.disable_f3),
        prediction_noise_sigma_m=float(args.prediction_noise_sigma_m),
        prediction_noise_seed=int(args.prediction_noise_seed),
        bootstrap_resamples=int(args.bootstrap_resamples),
    )
    result = run_generalization_evaluation(
        args.output_dir,
        config=cfg,
        source_head=str(args.source_head) if args.source_head else _source_head(),
        command=" ".join(["python -m forest_n3p.scripts.run_generalization_evaluation", *_quote_args(raw_argv)]),
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


def _parse_int_tuple(raw: str | None) -> tuple[int, ...] | None:
    if raw is None or not str(raw).strip():
        return None
    return tuple(int(part.strip()) for part in str(raw).split(",") if part.strip())


if __name__ == "__main__":
    raise SystemExit(main())
