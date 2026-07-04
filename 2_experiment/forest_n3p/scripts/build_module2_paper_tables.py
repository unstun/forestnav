from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import median
from typing import Any, Sequence


DEFAULT_EVALUATION_DIR = Path("0_trials/module2_h02_local_smoke/h02_1_available_subset")
DEFAULT_VERDICT = DEFAULT_EVALUATION_DIR / "verdict.json"
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_METRIC_PROTOCOL = Path("0_trials/module2_metric_protocol/module2_metric_protocol.json")
DEFAULT_OUTPUT_DIR = Path("0_trials/module2_paper_tables")
READY_H01_STATUSES = {"ready", "formal_ready", "ready_for_formal_evaluation"}
MAIN_TABLE_COLUMNS = (
    "method",
    "record_count",
    "success_rate",
    "timeout_failure_rate",
    "time_p50_s",
    "time_p95_s",
    "expansions_p50",
    "expansions_p95",
    "path_inflation_p50",
    "clearance_p50_m",
)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _repo_root()
    manifest = build_manifest(
        repo_root=repo_root,
        evaluation_dir=args.evaluation_dir,
        verdict_path=args.verdict,
        h01_manifest_path=args.h01_manifest,
        metric_protocol_path=args.metric_protocol,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = args.manifest_out or output_dir / "module2_paper_tables.json"
    markdown_out = args.markdown_out or output_dir / "module2_paper_tables.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(
        json.dumps(
            {"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(
    *,
    repo_root: Path,
    evaluation_dir: Path,
    verdict_path: Path,
    h01_manifest_path: Path,
    metric_protocol_path: Path,
) -> dict[str, Any]:
    evaluation_dir = Path(evaluation_dir)
    summary_path = evaluation_dir / "summary.json"
    records_path = evaluation_dir / "records.csv"
    summary = _read_json(summary_path) if summary_path.is_file() else {}
    verdict = _read_json(verdict_path) if Path(verdict_path).is_file() else {}
    h01_manifest = _read_json(h01_manifest_path) if Path(h01_manifest_path).is_file() else {}
    metric_protocol = _read_json(metric_protocol_path) if Path(metric_protocol_path).is_file() else {}
    records = _read_records(records_path) if records_path.is_file() else []

    blockers = _blockers(
        verdict=verdict,
        h01_manifest=h01_manifest,
        metric_protocol=metric_protocol,
        records=records,
        summary=summary,
    )
    formal_claim_allowed = not blockers
    table_status = "formal_ready" if formal_claim_allowed else "preview_not_formal"
    return {
        "schema_version": 1,
        "artifact_name": "module2_paper_tables",
        "status": "formal_ready" if formal_claim_allowed else "blocked_no_formal_h02_data",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(repo_root),
        "formal_claim_allowed": formal_claim_allowed,
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "inputs": {
            "evaluation_dir": str(evaluation_dir),
            "records_csv": str(records_path),
            "summary_json": str(summary_path),
            "verdict_json": str(verdict_path),
            "h01_manifest": str(h01_manifest_path),
            "metric_protocol": str(metric_protocol_path),
        },
        "input_status": {
            "record_count": len(records),
            "summary_record_count": summary.get("record_count"),
            "h02_verdict_status": verdict.get("status"),
            "h02_formal_acceptance": verdict.get("formal_acceptance"),
            "h01_manifest_status": h01_manifest.get("status"),
            "metric_protocol_status": metric_protocol.get("status"),
        },
        "blockers": blockers,
        "tables": {
            "main_table": {
                "i02_item": "I02.1",
                "status": table_status,
                "columns": list(MAIN_TABLE_COLUMNS),
                "rows": _main_table_rows(records),
                "source": "records.csv method-level aggregation",
            },
            "ablation_table": {
                "i02_item": "I02.2",
                "status": "formal_ready" if formal_claim_allowed and _has_ablation_methods(records) else "blocked_missing_formal_data",
                "planned_contrasts": [
                    "occupancy_only_vs_occupancy_plus_edt",
                    "bc_vs_ppo",
                    "terminal_rs_on_vs_off",
                    "action_mask_on_vs_off",
                    "forward_only_vs_forward_reverse_if_enabled",
                ],
                "available_method_families": sorted(_method_families(row.get("method", "")) for row in records),
                "rows": _ablation_preview_rows(records),
            },
            "failure_analysis_table": {
                "i02_item": "I02.3",
                "status": table_status,
                "columns": ["method", "record_count", "failure_count", "timeout", "collision", "terminal_rs_fail", "oscillation", "oracle_no_solution", "other"],
                "rows": _failure_rows(records),
                "source": "records.csv failure_reason aggregation",
            },
        },
        "statistics": {
            "paired_time_tests": summary.get("paired_time_tests", []),
            "paired_expansion_tests": summary.get("paired_expansion_tests", []),
            "success_rate_bootstrap_ci": summary.get("success_rate_bootstrap_ci", []),
            "failure_rate_bootstrap_ci": summary.get("failure_rate_bootstrap_ci", []),
            "timeout_failure_rate_bootstrap_ci": summary.get("timeout_failure_rate_bootstrap_ci", []),
        },
        "code_anchors": _code_anchors(repo_root),
        "claim_boundaries": [
            "Do not use preview_not_formal rows as paper results.",
            "Main paper claims require H02 formal_acceptance=true, H01 formal-ready status, frozen metric protocol, and no missing PPO checkpoint blocker.",
            "Use records.csv.total_time_s for timing claims; planner_time_s is diagnostic only.",
            "Use paired Wilcoxon for total_time_s and total_expansions and bootstrap CI for success/failure/timeout-rate differences.",
            "PPO formal training and checkpoint production must run on gpu3070ti-relay or another explicitly approved remote GPU, not locally.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 paper table protocol/preview without running training.")
    parser.add_argument("--evaluation-dir", type=Path, default=DEFAULT_EVALUATION_DIR)
    parser.add_argument("--verdict", type=Path, default=DEFAULT_VERDICT)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--metric-protocol", type=Path, default=DEFAULT_METRIC_PROTOCOL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _blockers(
    *,
    verdict: dict[str, Any],
    h01_manifest: dict[str, Any],
    metric_protocol: dict[str, Any],
    records: Sequence[dict[str, str]],
    summary: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if not records:
        blockers.append("missing_records_csv_rows")
    if not summary:
        blockers.append("missing_summary_json")
    if verdict.get("formal_acceptance") is not True:
        blockers.append("h02_verdict_not_formal")
    if str(h01_manifest.get("status")) not in READY_H01_STATUSES:
        blockers.append("h01_manifest_not_ready")
    for blocker in h01_manifest.get("blockers") or ():
        blocker_text = str(blocker)
        if blocker_text not in blockers:
            blockers.append(blocker_text)
    if str(metric_protocol.get("status")) != "frozen":
        blockers.append("metric_protocol_not_frozen")
    methods = {str(row.get("method", "")) for row in records}
    if not any(method in methods for method in ("ha_rl_rs_ppo", "ppo_analytic_operator")):
        blockers.append("missing_ppo_result_rows")
    return blockers


def _main_table_rows(records: Sequence[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for method in sorted({str(row.get("method", "")) for row in records if row.get("method")}):
        group = [row for row in records if str(row.get("method")) == method]
        count = len(group)
        feasible = sum(1 for row in group if _parse_bool(row.get("feasible")))
        time_values = [_parse_float(row.get("total_time_s")) for row in group]
        expansion_values = [_parse_float(row.get("total_expansions")) for row in group]
        inflation_values = [_parse_float(row.get("path_inflation_ratio")) for row in group]
        clearance_values = [_parse_float(row.get("min_clearance_m")) for row in group]
        rows.append(
            {
                "method": method,
                "record_count": count,
                "success_rate": _safe_rate(feasible, count),
                "timeout_failure_rate": _safe_rate(sum(1 for row in group if _failure_bucket(row.get("failure_reason")) == "timeout"), count),
                "time_p50_s": _percentile(time_values, 50),
                "time_p95_s": _percentile(time_values, 95),
                "expansions_p50": _percentile(expansion_values, 50),
                "expansions_p95": _percentile(expansion_values, 95),
                "path_inflation_p50": _percentile(inflation_values, 50),
                "clearance_p50_m": _percentile(clearance_values, 50),
            }
        )
    return rows


def _failure_rows(records: Sequence[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for method in sorted({str(row.get("method", "")) for row in records if row.get("method")}):
        group = [row for row in records if str(row.get("method")) == method]
        counts = Counter(_failure_bucket(row.get("failure_reason")) for row in group if not _parse_bool(row.get("feasible")))
        failure_count = sum(counts.values())
        rows.append(
            {
                "method": method,
                "record_count": len(group),
                "failure_count": failure_count,
                "timeout": counts.get("timeout", 0),
                "collision": counts.get("collision", 0),
                "terminal_rs_fail": counts.get("terminal_rs_fail", 0),
                "oscillation": counts.get("oscillation", 0),
                "oracle_no_solution": counts.get("oracle_no_solution", 0),
                "other": counts.get("other", 0),
            }
        )
    return rows


def _ablation_preview_rows(records: Sequence[dict[str, str]]) -> list[dict[str, Any]]:
    family_counts: dict[str, int] = defaultdict(int)
    for row in records:
        family_counts[_method_families(str(row.get("method", "")))] += 1
    return [{"family": family, "record_count": count} for family, count in sorted(family_counts.items())]


def _has_ablation_methods(records: Sequence[dict[str, str]]) -> bool:
    methods = {str(row.get("method", "")) for row in records}
    return bool({"bc_analytic_operator", "ha_rl_rs_ppo", "ppo_analytic_operator"} <= methods)


def _method_families(method: str) -> str:
    if method in {"ha_rl_rs_ppo", "ppo_analytic_operator"}:
        return "ppo"
    if method == "bc_analytic_operator":
        return "bc"
    if "rs" in method:
        return "rs_baseline"
    if method in {"mlp", "f_n3p_knn"}:
        return "f_n3p"
    return "other"


def _failure_bucket(value: str | None) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return "none"
    if "timeout" in text:
        return "timeout"
    if "collision" in text:
        return "collision"
    if "terminal_rs" in text or "no_rs_terminal" in text:
        return "terminal_rs_fail"
    if "oscillation" in text:
        return "oscillation"
    if "oracle" in text or "no_solution" in text:
        return "oracle_no_solution"
    return "other"


def _read_records(path: Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def _parse_float(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _safe_rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return float(numerator) / float(denominator)


def _percentile(values: Sequence[float | None], percentile: float) -> float | None:
    clean = sorted(float(value) for value in values if value is not None and math.isfinite(float(value)))
    if not clean:
        return None
    if len(clean) == 1:
        return clean[0]
    rank = (float(percentile) / 100.0) * (len(clean) - 1)
    lower = int(math.floor(rank))
    upper = int(math.ceil(rank))
    if lower == upper:
        return clean[lower]
    alpha = rank - lower
    return float(clean[lower] * (1.0 - alpha) + clean[upper] * alpha)


def _code_anchors(repo_root: Path) -> list[dict[str, Any]]:
    return [
        _anchor(repo_root, "2_experiment/forest_n3p/evaluation.py", "class EvaluationRecord", "EvaluationRecord"),
        _anchor(repo_root, "2_experiment/forest_n3p/evaluation.py", "class GroupSummary", "GroupSummary"),
        _anchor(repo_root, "2_experiment/forest_n3p/evaluation.py", "def paired_wilcoxon_time", "paired_wilcoxon_time"),
        _anchor(repo_root, "2_experiment/forest_n3p/evaluation.py", "def paired_wilcoxon_expansions", "paired_wilcoxon_expansions"),
        _anchor(repo_root, "2_experiment/forest_n3p/evaluation.py", "def bootstrap_timeout_failure_rate_difference", "bootstrap_timeout_failure_rate_difference"),
        _anchor(repo_root, "2_experiment/forest_n3p/evaluation.py", "def write_evaluation_outputs", "write_evaluation_outputs"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_metric_protocol.py", '"metric_id": "total_expansions"', "module2_metric_protocol.total_expansions"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py", "f02_6_decision_packet_pending", "module2_evaluation_manifest.F02.6_guard"),
    ]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _anchor(repo_root: Path, path: str, pattern: str, symbol: str) -> dict[str, Any]:
    lines = (repo_root / path).read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        if pattern in line:
            return {"path": path, "line": index, "symbol": symbol, "pattern": pattern}
    raise RuntimeError(f"Could not find pattern {pattern!r} in {path}")


def _source_head(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - provenance is best-effort for generated artifacts.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Paper Tables Protocol",
        "",
        f"- Status: `{manifest['status']}`",
        f"- Formal claim allowed: `{manifest['formal_claim_allowed']}`",
        f"- Local training allowed: `{manifest['local_training_allowed']}`",
        f"- Remote training resource: `{manifest['remote_training_resource']}`",
        "",
        "This artifact is not formal unless `formal_claim_allowed=true`.",
        "",
        "## Blockers",
        "",
    ]
    if manifest["blockers"]:
        for blocker in manifest["blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")

    main_table = manifest["tables"]["main_table"]
    lines.extend(
        [
            "",
            "## I02.1 Main Table Preview",
            "",
            f"- status: `{main_table['status']}`",
            "",
            "| method | success | timeout | time p50/p95 | expansions p50/p95 | path inflation p50 | clearance p50 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in main_table["rows"]:
        lines.append(
            "| {method} | {success} | {timeout} | {time_p50}/{time_p95} | {exp_p50}/{exp_p95} | {inflation} | {clearance} |".format(
                method=row["method"],
                success=_fmt(row["success_rate"]),
                timeout=_fmt(row["timeout_failure_rate"]),
                time_p50=_fmt(row["time_p50_s"]),
                time_p95=_fmt(row["time_p95_s"]),
                exp_p50=_fmt(row["expansions_p50"]),
                exp_p95=_fmt(row["expansions_p95"]),
                inflation=_fmt(row["path_inflation_p50"]),
                clearance=_fmt(row["clearance_p50_m"]),
            )
        )

    lines.extend(["", "## I02.2 Ablation Table", "", f"- status: `{manifest['tables']['ablation_table']['status']}`"])
    for contrast in manifest["tables"]["ablation_table"]["planned_contrasts"]:
        lines.append(f"- planned: `{contrast}`")

    lines.extend(
        [
            "",
            "## I02.3 Failure Analysis Preview",
            "",
            f"- status: `{manifest['tables']['failure_analysis_table']['status']}`",
            "",
            "| method | failures | timeout | collision | terminal RS | oscillation | oracle no-solution | other |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in manifest["tables"]["failure_analysis_table"]["rows"]:
        lines.append(
            f"| {row['method']} | {row['failure_count']} | {row['timeout']} | {row['collision']} | {row['terminal_rs_fail']} | {row['oscillation']} | {row['oracle_no_solution']} | {row['other']} |"
        )

    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines)


def _fmt(value: Any) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
