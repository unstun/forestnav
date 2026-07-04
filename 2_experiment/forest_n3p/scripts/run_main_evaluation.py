from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    default_main_evaluation_profiles,
    preflight_main_evaluation,
    run_main_evaluation,
    validation_main_evaluation_profiles,
)


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Run ForestNav T14 main evaluation.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--queries-per-bucket", type=int, default=50)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--methods", default=",".join(MainEvaluationConfig().methods))
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="original_t06")
    parser.add_argument("--distance-bins", default="8:12,12:16,16:20,20:")
    parser.add_argument("--knn-dataset-dir", type=Path, default=MainEvaluationConfig().knn_dataset_dir)
    parser.add_argument("--knn-feature-indices", default=None)
    parser.add_argument("--mlp-model-dir", type=Path, default=MainEvaluationConfig().mlp_model_dir)
    parser.add_argument("--mlp-device", default=MainEvaluationConfig().mlp_device)
    parser.add_argument("--cutpoint-supplement-path", type=Path, default=MainEvaluationConfig().cutpoint_supplement_path)
    parser.add_argument("--t06-validation-summary-path", type=Path, default=MainEvaluationConfig().t06_validation_summary_path)
    parser.add_argument("--contract-path", type=Path, default=MainEvaluationConfig().contract_path)
    parser.add_argument("--human-review-form-path", type=Path, default=MainEvaluationConfig().human_review_form_path)
    parser.add_argument("--bootstrap-resamples", type=int, default=5_000)
    parser.add_argument("--idb-rrt-binary-path", type=Path, default=None)
    parser.add_argument("--idb-rrt-dynoplan-root", type=Path, default=None)
    parser.add_argument("--idb-rrt-motion-file", type=Path, default=None)
    parser.add_argument("--idb-rrt-timeout-s", type=float, default=None)
    parser.add_argument("--module2-rl-rs-checkpoint", type=Path, default=None)
    parser.add_argument("--module2-rl-rs-device", default=MainEvaluationConfig().module2_rl_rs_device)
    parser.add_argument("--module2-rl-rs-obs-patch-size-m", type=float, default=MainEvaluationConfig().module2_rl_rs_obs_patch_size_m)
    parser.add_argument("--module2-rl-rs-obs-patch-cells", type=int, default=MainEvaluationConfig().module2_rl_rs_obs_patch_cells)
    parser.add_argument("--module2-rl-rs-obs-include-edt", action=argparse.BooleanOptionalAction, default=MainEvaluationConfig().module2_rl_rs_obs_include_edt)
    parser.add_argument("--module2-rl-rs-obs-edt-clip-m", type=float, default=MainEvaluationConfig().module2_rl_rs_obs_edt_clip_m)
    parser.add_argument("--module2-rl-rs-max-steps", type=int, default=MainEvaluationConfig().module2_rl_rs_max_steps)
    parser.add_argument("--module2-rl-rs-action-step-m", type=float, default=MainEvaluationConfig().module2_rl_rs_action_step_m)
    parser.add_argument("--module2-rl-rs-collision-sample-step-m", type=float, default=MainEvaluationConfig().module2_rl_rs_collision_sample_step_m)
    parser.add_argument("--module2-rl-rs-terminal-check-every", type=int, default=MainEvaluationConfig().module2_rl_rs_terminal_check_every)
    parser.add_argument("--module2-rl-rs-no-progress-patience", type=int, default=MainEvaluationConfig().module2_rl_rs_no_progress_patience)
    parser.add_argument("--k-neighbors", type=int, default=MainEvaluationConfig().k_neighbors)
    parser.add_argument("--commit-verified-rs-segments", action="store_true")
    parser.add_argument("--max-steps-override", type=int, default=None)
    parser.add_argument("--disable-f1", action="store_true")
    parser.add_argument("--disable-f2", action="store_true")
    parser.add_argument("--disable-f3", action="store_true")
    parser.add_argument("--prediction-noise-sigma-m", type=float, default=0.0)
    parser.add_argument("--prediction-noise-seed", type=int, default=MainEvaluationConfig().prediction_noise_seed)
    parser.add_argument("--allow-unreviewed-cutpoints", action="store_true")
    parser.add_argument("--allow-unresolved-human-review", action="store_true")
    parser.add_argument("--no-enforce-t14-scale", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    config = MainEvaluationConfig(
        seed=int(args.seed),
        queries_per_bucket=int(args.queries_per_bucket),
        seed_count=int(args.seed_count),
        queries_per_map=int(args.queries_per_map),
        methods=tuple(part.strip() for part in str(args.methods).split(",") if part.strip()),
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        distance_bins=parse_distance_bins(str(args.distance_bins)),
        knn_dataset_dir=args.knn_dataset_dir,
        knn_feature_indices=_parse_int_tuple(args.knn_feature_indices),
        mlp_model_dir=args.mlp_model_dir,
        mlp_device=str(args.mlp_device),
        cutpoint_supplement_path=args.cutpoint_supplement_path,
        t06_validation_summary_path=args.t06_validation_summary_path,
        contract_path=args.contract_path,
        human_review_form_path=args.human_review_form_path,
        idb_rrt_binary_path=args.idb_rrt_binary_path,
        idb_rrt_dynoplan_root=args.idb_rrt_dynoplan_root,
        idb_rrt_motion_file=args.idb_rrt_motion_file,
        idb_rrt_timeout_s=args.idb_rrt_timeout_s,
        module2_rl_rs_checkpoint=args.module2_rl_rs_checkpoint,
        module2_rl_rs_device=str(args.module2_rl_rs_device),
        module2_rl_rs_obs_patch_size_m=float(args.module2_rl_rs_obs_patch_size_m),
        module2_rl_rs_obs_patch_cells=int(args.module2_rl_rs_obs_patch_cells),
        module2_rl_rs_obs_include_edt=bool(args.module2_rl_rs_obs_include_edt),
        module2_rl_rs_obs_edt_clip_m=float(args.module2_rl_rs_obs_edt_clip_m),
        module2_rl_rs_max_steps=int(args.module2_rl_rs_max_steps),
        module2_rl_rs_action_step_m=float(args.module2_rl_rs_action_step_m),
        module2_rl_rs_collision_sample_step_m=float(args.module2_rl_rs_collision_sample_step_m),
        module2_rl_rs_terminal_check_every=int(args.module2_rl_rs_terminal_check_every),
        module2_rl_rs_no_progress_patience=int(args.module2_rl_rs_no_progress_patience),
        k_neighbors=int(args.k_neighbors),
        commit_verified_rs_segments=bool(args.commit_verified_rs_segments),
        max_steps_override=args.max_steps_override,
        enable_f1=not bool(args.disable_f1),
        enable_f2=not bool(args.disable_f2),
        enable_f3=not bool(args.disable_f3),
        prediction_noise_sigma_m=float(args.prediction_noise_sigma_m),
        prediction_noise_seed=int(args.prediction_noise_seed),
        allow_unreviewed_cutpoints=bool(args.allow_unreviewed_cutpoints),
        allow_unresolved_human_review=bool(args.allow_unresolved_human_review),
        enforce_t14_scale=not bool(args.no_enforce_t14_scale),
        bootstrap_resamples=int(args.bootstrap_resamples),
    )
    if args.preflight_only:
        report = preflight_main_evaluation(config)
        print(
            json.dumps(
                {
                    "ok_to_run": report.ok_to_run,
                    "blocking_issues": list(report.blocking_issues),
                    "warnings": list(report.warnings),
                    "available_methods": list(report.available_methods),
                    "unavailable_methods": dict(report.unavailable_methods),
                    "cutpoint_supplement_reviewed": report.cutpoint_supplement_reviewed,
                    "human_review_satisfied": report.human_review_satisfied,
                    "human_review_decisions": dict(report.human_review_decisions),
                    "profile_bucket_satisfied": report.profile_bucket_satisfied,
                    "profile_bucket_issues": list(report.profile_bucket_issues),
                    "t14_scale_satisfied": report.t14_scale_satisfied,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0 if report.ok_to_run else 2

    result = run_main_evaluation(
        args.output_dir,
        config=config,
        source_head=str(args.source_head) if args.source_head else _source_head(),
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


def _parse_int_tuple(raw: str | None) -> tuple[int, ...] | None:
    if raw is None or not str(raw).strip():
        return None
    return tuple(int(part.strip()) for part in str(raw).split(",") if part.strip())


def _profiles_from_bucket_mode(mode: str):
    if mode == "original_t06":
        return default_main_evaluation_profiles()
    if mode == "validation_t06":
        return validation_main_evaluation_profiles()
    raise ValueError(f"unsupported density profile bucket mode: {mode}")


if __name__ == "__main__":
    raise SystemExit(main())
