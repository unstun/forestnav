from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from forest_n3p.ablation import AblationVariant, default_t15_variants
from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.evaluation import GroupSummary, summarize_by_method_bucket
from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    default_main_evaluation_profiles,
    run_main_evaluation,
    validation_main_evaluation_profiles,
)


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Run the ForestNav T15 ablation framework.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--queries-per-bucket", type=int, default=20)
    parser.add_argument("--seed-count", type=int, default=3)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260623)
    parser.add_argument("--density-profile-buckets", choices=("original_t06", "validation_t06"), default="validation_t06")
    parser.add_argument("--distance-bins", default="8:12,12:16,16:20,20:")
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--group", action="append", default=[])
    parser.add_argument("--bootstrap-resamples", type=int, default=1_000)
    parser.add_argument("--mlp-device", default=MainEvaluationConfig().mlp_device)
    parser.add_argument("--prediction-noise-seed", type=int, default=20260623)
    parser.add_argument("--no-commit-verified-rs-segments", action="store_true")
    parser.add_argument("--allow-unreviewed-cutpoints", action="store_true")
    parser.add_argument("--allow-unresolved-human-review", action="store_true")
    parser.add_argument("--dry-run-manifest", action="store_true")
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source_head = str(args.source_head) if args.source_head else _source_head()
    variants = _select_variants(default_t15_variants(), variant_ids=args.variant_id, groups=args.group)
    command = " ".join(["python -m forest_n3p.scripts.run_ablation_experiments", *_quote_args(raw_argv)])

    manifest_path = output_dir / "ablation_manifest.csv"
    _write_dict_csv(manifest_path, [variant.manifest_row() for variant in variants])
    if args.dry_run_manifest:
        print(json.dumps({"manifest": str(manifest_path), "variant_count": len(variants)}, indent=2, ensure_ascii=False))
        return 0

    summary_rows: list[dict[str, Any]] = []
    run_index_rows: list[dict[str, Any]] = []
    for variant in variants:
        if not variant.runnable:
            run_index_rows.append(_not_run_index_row(variant))
            summary_rows.extend(_not_run_summary_rows(variant))
            continue

        variant_dir = output_dir / "runs" / variant.variant_id
        cfg = MainEvaluationConfig(
            seed=int(args.seed),
            queries_per_bucket=int(args.queries_per_bucket),
            seed_count=int(args.seed_count),
            queries_per_map=int(args.queries_per_map),
            methods=_methods_for_variant(variant),
            profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
            distance_bins=parse_distance_bins(str(args.distance_bins)),
            k_neighbors=int(variant.k_neighbors),
            knn_feature_indices=variant.knn_feature_indices,
            mlp_device=str(args.mlp_device),
            commit_verified_rs_segments=not bool(args.no_commit_verified_rs_segments),
            max_steps_override=variant.max_steps_override,
            enable_f1=bool(variant.enable_f1),
            enable_f2=bool(variant.enable_f2),
            enable_f3=bool(variant.enable_f3),
            prediction_noise_sigma_m=float(variant.prediction_noise_sigma_m),
            prediction_noise_seed=int(args.prediction_noise_seed),
            allow_unreviewed_cutpoints=bool(args.allow_unreviewed_cutpoints),
            allow_unresolved_human_review=bool(args.allow_unresolved_human_review),
            enforce_t14_scale=False,
            bootstrap_resamples=int(args.bootstrap_resamples),
        )
        result = run_main_evaluation(
            variant_dir,
            config=cfg,
            source_head=source_head,
            command=f"{command} [variant={variant.variant_id}]",
        )
        run_index_rows.append(
            {
                **_variant_identity(variant),
                "status": result.verdict["status"],
                "record_count": len(result.records),
                "query_count": len(result.queries),
                "method_count": result.verdict["method_count"],
                "run_dir": str(variant_dir),
                "report": str(result.output_paths["report_md"]),
            }
        )
        summary_rows.extend(_summary_rows_for_variant(variant, tuple(summarize_by_method_bucket(result.records)), variant_dir))

    summary_path = output_dir / "ablation_summary.csv"
    run_index_path = output_dir / "ablation_run_index.csv"
    config_path = output_dir / "run_config.json"
    report_path = output_dir / "report.md"
    _write_dict_csv(summary_path, summary_rows)
    _write_dict_csv(run_index_path, run_index_rows)
    config_path.write_text(
        json.dumps(
            {
                "created_at_utc": datetime.now(UTC).isoformat(),
                "source_head": source_head,
                "command": command,
                "config": {
                    "queries_per_bucket": int(args.queries_per_bucket),
                    "seed_count": int(args.seed_count),
                    "queries_per_map": int(args.queries_per_map),
                    "seed": int(args.seed),
                    "density_profile_buckets": str(args.density_profile_buckets),
                    "distance_bins": str(args.distance_bins),
                    "bootstrap_resamples": int(args.bootstrap_resamples),
                    "commit_verified_rs_segments": not bool(args.no_commit_verified_rs_segments),
                },
                "outputs": {
                    "manifest_csv": str(manifest_path),
                    "summary_csv": str(summary_path),
                    "run_index_csv": str(run_index_path),
                    "report_md": str(report_path),
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    report_path.write_text(_render_report(variants, summary_rows, run_index_rows), encoding="utf-8")
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "variant_count": len(variants),
                "runnable_variant_count": sum(1 for item in variants if item.runnable),
                "summary": str(summary_path),
                "report": str(report_path),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def _select_variants(
    variants: Iterable[AblationVariant],
    *,
    variant_ids: Iterable[str],
    groups: Iterable[str],
) -> tuple[AblationVariant, ...]:
    selected = tuple(variants)
    wanted_ids = {str(item) for item in variant_ids if str(item).strip()}
    wanted_groups = {str(item) for item in groups if str(item).strip()}
    if wanted_ids:
        selected = tuple(item for item in selected if item.variant_id in wanted_ids)
    if wanted_groups:
        selected = tuple(item for item in selected if item.group_id in wanted_groups)
    if not selected:
        raise ValueError("no ablation variants selected")
    return selected


def _methods_for_variant(variant: AblationVariant) -> tuple[str, ...]:
    if variant.method == "vanilla_ha":
        return ("vanilla_ha",)
    return ("vanilla_ha", variant.method)


def _summary_rows_for_variant(
    variant: AblationVariant,
    summaries: tuple[GroupSummary, ...],
    variant_dir: Path,
) -> list[dict[str, Any]]:
    by_key = {(item.method, item.difficulty_bucket): item for item in summaries}
    out: list[dict[str, Any]] = []
    for bucket in ("Easy", "Complex", "Extreme"):
        method_row = by_key.get((variant.method, bucket))
        vanilla_row = by_key.get(("vanilla_ha", bucket))
        if method_row is None:
            continue
        out.append(_metric_row(variant, method_row, vanilla_row, variant_dir))
    return out


def _metric_row(
    variant: AblationVariant,
    row: GroupSummary,
    vanilla_row: GroupSummary | None,
    variant_dir: Path,
) -> dict[str, Any]:
    median_time_reduction = None
    success_drop_pp = None
    if vanilla_row is not None:
        if _positive(vanilla_row.median_time_s) and row.median_time_s is not None:
            median_time_reduction = 1.0 - float(row.median_time_s) / float(vanilla_row.median_time_s)
        success_drop_pp = 100.0 * (float(vanilla_row.feasible_rate) - float(row.feasible_rate))
    return {
        **_variant_identity(variant),
        "status": "run",
        "difficulty_bucket": row.difficulty_bucket,
        "method": row.method,
        "count": row.count,
        "feasible_rate": row.feasible_rate,
        "median_time_s": row.median_time_s,
        "p95_time_s": row.p95_time_s,
        "median_expansions": row.median_expansions,
        "median_path_inflation_ratio": row.median_path_inflation_ratio,
        "fallback_trigger_rate": row.fallback_trigger_rate,
        "fallback_f1_rate": row.fallback_f1_rate,
        "fallback_f2_rate": row.fallback_f2_rate,
        "fallback_f3_rate": row.fallback_f3_rate,
        "subgoal_reachability_rate": row.subgoal_reachability_rate,
        "collision_violation_total": row.collision_violation_total,
        "vanilla_feasible_rate": None if vanilla_row is None else vanilla_row.feasible_rate,
        "vanilla_median_time_s": None if vanilla_row is None else vanilla_row.median_time_s,
        "median_time_reduction_vs_vanilla": median_time_reduction,
        "success_drop_pp_vs_vanilla": success_drop_pp,
        "run_dir": str(variant_dir),
    }


def _not_run_index_row(variant: AblationVariant) -> dict[str, Any]:
    return {
        **_variant_identity(variant),
        "status": variant.status,
        "record_count": 0,
        "query_count": 0,
        "method_count": 0,
        "run_dir": "",
        "report": "",
    }


def _not_run_summary_rows(variant: AblationVariant) -> list[dict[str, Any]]:
    return [
        {
            **_variant_identity(variant),
            "status": variant.status,
            "difficulty_bucket": bucket,
            "method": variant.method,
            "count": 0,
            "feasible_rate": None,
            "median_time_s": None,
            "p95_time_s": None,
            "median_expansions": None,
            "median_path_inflation_ratio": None,
            "fallback_trigger_rate": None,
            "fallback_f1_rate": None,
            "fallback_f2_rate": None,
            "fallback_f3_rate": None,
            "subgoal_reachability_rate": None,
            "collision_violation_total": None,
            "vanilla_feasible_rate": None,
            "vanilla_median_time_s": None,
            "median_time_reduction_vs_vanilla": None,
            "success_drop_pp_vs_vanilla": None,
            "run_dir": "",
        }
        for bucket in ("Easy", "Complex", "Extreme")
    ]


def _variant_identity(variant: AblationVariant) -> dict[str, Any]:
    return {
        "group_id": variant.group_id,
        "group_name": variant.group_name,
        "variant_id": variant.variant_id,
        "variant_name": variant.variant_name,
        "evidence_level": variant.evidence_level,
        "notes": variant.notes,
    }


def _render_report(
    variants: tuple[AblationVariant, ...],
    summary_rows: list[dict[str, Any]],
    run_index_rows: list[dict[str, Any]],
) -> str:
    runnable = sum(1 for item in variants if item.runnable)
    planned = len(variants) - runnable
    selected_groups = "/".join(sorted({item.group_id for item in variants}))
    lines = [
        "# T15 消融实验框架报告",
        "",
        "## 人话结论",
        "",
        f"- 本次登记 {len(variants)} 个消融变体，其中 {runnable} 个已真实运行，{planned} 个只登记为后续重切数据/重提特征任务。",
        f"- 已运行部分覆盖 {selected_groups} 的主框架；A1 曲率边界标签、A4 64-ray、A5 非 8m L_max 仍不能当成论文最终数字。",
        "- 所有已运行变体都复用 T14 query/evaluation 逻辑；差别只来自模型、特征、k、序列、回退或噪声开关。",
        "",
        "## 输出文件",
        "",
        "- `ablation_manifest.csv`: 所有 A1-A8 变体与是否可运行。",
        "- `ablation_summary.csv`: 每个已运行变体按 Easy/Complex/Extreme 汇总。",
        "- `ablation_run_index.csv`: 每个变体对应的子目录和报告。",
        "",
        "## 需要后续补强",
        "",
    ]
    planned_rows = [item for item in run_index_rows if int(item.get("record_count", 0)) == 0]
    if planned_rows:
        for item in planned_rows:
            lines.append(f"- {item['variant_id']}: {item['status']}；{item['notes']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Extreme 快速查看", ""])
    extreme_rows = [
        row for row in summary_rows if row.get("status") == "run" and row.get("difficulty_bucket") == "Extreme"
    ]
    if not extreme_rows:
        lines.append("- no Extreme rows")
    else:
        lines.append("| group | variant | feasible | median_time_s | reduction_vs_vanilla | f2 | f3 |")
        lines.append("|---|---|---:|---:|---:|---:|---:|")
        for row in extreme_rows:
            lines.append(
                "| {group_id} | {variant_id} | {feasible_rate} | {median_time_s} | {reduction} | {f2} | {f3} |".format(
                    group_id=row["group_id"],
                    variant_id=row["variant_id"],
                    feasible_rate=_fmt(row.get("feasible_rate")),
                    median_time_s=_fmt(row.get("median_time_s")),
                    reduction=_fmt(row.get("median_time_reduction_vs_vanilla")),
                    f2=_fmt(row.get("fallback_f2_rate")),
                    f3=_fmt(row.get("fallback_f3_rate")),
                )
            )
    return "\n".join(lines) + "\n"


def _write_dict_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(row.get(key)) for key in fieldnames})


def _csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False)
    return value


def _positive(value: float | None) -> bool:
    return value is not None and math.isfinite(float(value)) and float(value) > 0.0


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return ""
    return f"{number:.4f}"


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop the run.
        return "unknown"


def _quote_args(argv: list[str] | None) -> list[str]:
    if argv is None:
        return []
    return [str(item) for item in argv]


def _profiles_from_bucket_mode(mode: str):
    if mode == "original_t06":
        return default_main_evaluation_profiles()
    if mode == "validation_t06":
        return validation_main_evaluation_profiles()
    raise ValueError(f"unsupported density profile bucket mode: {mode}")


if __name__ == "__main__":
    raise SystemExit(main())
