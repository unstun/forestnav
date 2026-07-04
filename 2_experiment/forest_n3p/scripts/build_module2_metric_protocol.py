from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.evaluation import (
    BootstrapCIResult,
    EvaluationRecord,
    GroupSummary,
    PairedWilcoxonExpansionsResult,
    PairedWilcoxonResult,
)


DEFAULT_CONTRACT_PATH = Path(".pipeline/contracts/module2-ppo-funnel-expansion.md")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    manifest = build_metric_protocol(contract_path=args.contract_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.manifest_out or output_dir / "module2_metric_protocol.json"
    markdown_path = args.markdown_out or output_dir / "module2_metric_protocol.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "markdown": str(markdown_path), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_metric_protocol(*, contract_path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    record_columns = _dataclass_fields(EvaluationRecord)
    summary_columns = _dataclass_fields(GroupSummary)
    paired_time_columns = _dataclass_fields(PairedWilcoxonResult)
    paired_expansion_columns = _dataclass_fields(PairedWilcoxonExpansionsResult)
    bootstrap_columns = _dataclass_fields(BootstrapCIResult)
    metrics = _metric_records()
    blockers = _protocol_blockers(metrics=metrics, record_columns=record_columns, summary_columns=summary_columns)
    return {
        "schema_version": 1,
        "protocol_name": "module2_h01_metric_protocol",
        "status": "frozen" if not blockers else "blocked_metric_gap",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "contract": {
            "path": str(contract_path),
            "status": _frontmatter_value(contract_path, "status"),
            "primary_metric_anchor": ".pipeline/contracts/module2-ppo-funnel-expansion.md:19-32",
            "statistical_test_anchor": ".pipeline/contracts/module2-ppo-funnel-expansion.md:41-45",
        },
        "metrics": metrics,
        "serialized_outputs": {
            "records_csv_columns": record_columns,
            "summary_by_method_bucket_columns": summary_columns,
            "paired_time_tests_columns": paired_time_columns,
            "paired_expansion_tests_columns": paired_expansion_columns,
            "success_rate_bootstrap_ci_columns": bootstrap_columns,
        },
        "blockers": blockers,
        "claim_boundaries": [
            "Use records.csv.total_time_s, not planner_time_s, for cross-method timing claims.",
            "Use timeout_failure_rate only when failure_reason contains timeout; other failures stay separate.",
            "Use paired Wilcoxon p<0.05 for total_time_s and total_expansions comparisons where paired queries exist.",
            "Use bootstrap CI for success/timeout/failure rate differences.",
            "Path quality claims must report path_inflation_ratio plus curvature or clearance, not success alone.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Freeze Module2 H01.2 metrics without running evaluation.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    return parser.parse_args(list(argv) if argv is not None else None)


def _metric_records() -> list[dict[str, Any]]:
    return [
        {
            "metric_id": "total_expansions",
            "role": "contract_primary",
            "hypothesis": "median reduction >= 50%",
            "record_field": "records.csv.total_expansions",
            "summary_fields": [
                "summary_by_method_bucket.median_expansions",
                "summary_by_method_bucket.p95_expansions",
            ],
            "statistical_test": {
                "name": "paired_wilcoxon_signed_rank",
                "function": "forest_n3p.evaluation.paired_wilcoxon_expansions",
                "p_threshold": 0.05,
            },
        },
        {
            "metric_id": "total_time_s",
            "role": "contract_primary",
            "hypothesis": "median reduction >= 30%",
            "record_field": "records.csv.total_time_s",
            "summary_fields": [
                "summary_by_method_bucket.median_time_s",
                "summary_by_method_bucket.p95_time_s",
            ],
            "statistical_test": {
                "name": "paired_wilcoxon_signed_rank",
                "function": "forest_n3p.evaluation.paired_wilcoxon_time",
                "p_threshold": 0.05,
            },
        },
        {
            "metric_id": "timeout_failure_rate",
            "role": "contract_primary",
            "hypothesis": "absolute reduction >= 20 percentage points",
            "record_derivation": {
                "source_field": "records.csv.failure_reason",
                "rule": "count a timeout failure when lowercase failure_reason contains 'timeout'",
            },
            "summary_fields": [
                "summary_by_method_bucket.timeout_failure_count",
                "summary_by_method_bucket.timeout_failure_rate",
            ],
            "statistical_test": {
                "name": "paired_bootstrap_ci",
                "function": "bootstrap over paired timeout indicator differences",
                "confidence_level": 0.95,
            },
        },
        {
            "metric_id": "path_quality",
            "role": "contract_primary",
            "hypothesis": "path inflation <= 5% and smoothness/clearance not worse",
            "submetrics": [
                {
                    "record_field": "path_inflation_ratio",
                    "summary_fields": [
                        "summary_by_method_bucket.median_path_inflation_ratio",
                        "summary_by_method_bucket.p95_path_inflation_ratio",
                    ],
                },
                {
                    "record_field": "mean_abs_curvature",
                    "summary_fields": ["summary_by_method_bucket.mean_direction_switches"],
                },
                {
                    "record_field": "min_clearance_m",
                    "summary_fields": ["summary_by_method_bucket.median_min_clearance_m"],
                },
            ],
        },
        {
            "metric_id": "analytic_success_rate",
            "role": "diagnostic",
            "record_derivation": {
                "numerator": "records.csv.analytic_successes",
                "denominator": "records.csv.analytic_attempts",
            },
        },
        {
            "metric_id": "terminal_rs_success_rate",
            "role": "diagnostic",
            "record_derivation": {
                "numerator": "records.csv.terminal_rs_success_count",
                "denominator": "records.csv.analytic_attempts",
            },
        },
        {
            "metric_id": "nn_forward_time_s",
            "role": "diagnostic",
            "external_artifact_fields": [
                "Gate #3 eval summary nn_forward_time_s",
                "Gate #3 eval summary mean_nn_forward_time_s",
                "records.csv metadata.nn_forward_time_s when a runner explicitly flattens it",
            ],
        },
    ]


def _protocol_blockers(
    *,
    metrics: Sequence[dict[str, Any]],
    record_columns: Sequence[str],
    summary_columns: Sequence[str],
) -> list[str]:
    blockers: list[str] = []
    for metric in metrics:
        _check_record_field(metric.get("record_field"), record_columns, blockers)
        derivation = metric.get("record_derivation")
        if isinstance(derivation, dict):
            _check_record_field(derivation.get("source_field"), record_columns, blockers)
            _check_record_field(derivation.get("numerator"), record_columns, blockers)
            _check_record_field(derivation.get("denominator"), record_columns, blockers)
        for field in metric.get("summary_fields", ()):
            _check_summary_field(field, summary_columns, blockers)
        for submetric in metric.get("submetrics", ()):
            if not isinstance(submetric, dict):
                continue
            _check_record_field(submetric.get("record_field"), record_columns, blockers)
            for field in submetric.get("summary_fields", ()):
                _check_summary_field(field, summary_columns, blockers)
    return sorted(set(blockers))


def _check_record_field(field: Any, record_columns: Sequence[str], blockers: list[str]) -> None:
    if not isinstance(field, str) or not field.startswith("records.csv."):
        return
    column = field.split(".", 2)[2]
    if column not in record_columns:
        blockers.append(f"missing_records_csv_column:{column}")


def _check_summary_field(field: Any, summary_columns: Sequence[str], blockers: list[str]) -> None:
    if not isinstance(field, str) or not field.startswith("summary_by_method_bucket."):
        return
    column = field.split(".", 1)[1]
    if column not in summary_columns:
        blockers.append(f"missing_summary_by_method_bucket_column:{column}")


def _dataclass_fields(cls: type[Any]) -> list[str]:
    return [item.name for item in fields(cls)]


def _frontmatter_value(path: Path, key: str) -> str | None:
    if not Path(path).is_file():
        return None
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        if name.strip() == key:
            return value.strip().strip('"').strip("'")
    return None


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop protocol generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 H01.2 Metric Protocol",
        "",
        f"- status: `{manifest['status']}`",
        f"- contract: `{manifest['contract']['path']}`",
        "",
        "## Metrics",
    ]
    for metric in manifest["metrics"]:
        lines.append(f"- `{metric['metric_id']}`: {metric['role']}")
    lines.extend(["", "## Serialized Outputs"])
    lines.append(f"- records.csv columns: `{len(manifest['serialized_outputs']['records_csv_columns'])}`")
    lines.append(f"- summary_by_method_bucket columns: `{len(manifest['serialized_outputs']['summary_by_method_bucket_columns'])}`")
    lines.extend(["", "## Blockers"])
    if manifest["blockers"]:
        lines.extend(f"- `{blocker}`" for blocker in manifest["blockers"])
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
