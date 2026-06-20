from __future__ import annotations

import json
import socket
import sys
from pathlib import Path
from typing import Any

import numpy as np

from forest_n3p.evaluation import (
    EvaluationConfig,
    EvaluationRun,
    bootstrap_success_rate_difference,
    evaluate_run,
    paired_wilcoxon_time,
    summarize_by_method_bucket,
    write_evaluation_outputs,
)
from forest_n3p.training_data import source_head
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint


def main() -> int:
    output_dir = Path(".pipeline/experiments/20260620_t13_evaluation_framework_verification")
    report_path = Path(".pipeline/experiments/20260620_t13_evaluation_framework_verification.md")
    output_dir.mkdir(parents=True, exist_ok=True)
    cfg = EvaluationConfig(bootstrap_resamples=500, bootstrap_seed=20260620)
    grid_map = GridMap(np.zeros((120, 120), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    records = tuple(evaluate_run(run, grid_map, footprint, config=cfg) for run in _synthetic_runs())
    time_test = paired_wilcoxon_time(records, "f_n3p_knn", "vanilla_ha")
    success_ci = bootstrap_success_rate_difference(records, "f_n3p_knn", "vanilla_ha", config=cfg)
    outputs = write_evaluation_outputs(
        records,
        output_dir,
        paired_time_tests=(time_test,),
        success_rate_cis=(success_ci,),
    )
    payload = {
        "source_head": source_head(),
        "execution_host": socket.gethostname(),
        "command": " ".join(sys.argv),
        "record_count": len(records),
        "summary": [item.__dict__ for item in summarize_by_method_bucket(records)],
        "time_test": time_test.__dict__,
        "success_ci": success_ci.__dict__,
        "outputs": {key: str(value) for key, value in outputs.items()},
    }
    (output_dir / "verification_summary.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    report_path.write_text(render_report(payload), encoding="utf-8")
    print(report_path)
    print(outputs["records_csv"])
    print(outputs["summary_json"])
    print(f"record_count={len(records)}")
    return 0


def _synthetic_runs() -> tuple[EvaluationRun, ...]:
    rows: list[EvaluationRun] = []
    for idx, (knn_t, vanilla_t, knn_success, vanilla_success) in enumerate(
        (
            (0.8, 1.6, True, True),
            (1.1, 2.4, True, True),
            (1.4, 3.1, True, False),
            (2.0, 4.2, False, False),
        ),
        start=1,
    ):
        qid = f"synthetic_q{idx}"
        bucket = "Easy" if idx <= 2 else "Complex"
        rows.append(
            EvaluationRun(
                query_id=qid,
                method="f_n3p_knn",
                difficulty_bucket=bucket,
                distance_bin_key="d08_12",
                success=knn_success,
                path=((2.0, 6.0, 0.0), (6.0, 6.0, 0.0)) if knn_success else (),
                total_time_s=knn_t,
                total_expansions=10 + idx,
                reference_path_length_m=4.0,
                fallback_f1_count=1 if idx == 2 else 0,
                fallback_f2_count=1 if idx == 3 else 0,
                subgoal_reachable_count=1,
                subgoal_attempt_count=1,
            )
        )
        rows.append(
            EvaluationRun(
                query_id=qid,
                method="vanilla_ha",
                difficulty_bucket=bucket,
                distance_bin_key="d08_12",
                success=vanilla_success,
                path=((2.0, 6.0, 0.0), (6.0, 6.0, 0.0)) if vanilla_success else (),
                total_time_s=vanilla_t,
                total_expansions=40 + idx,
                reference_path_length_m=4.0,
            )
        )
    return tuple(rows)


def render_report(payload: dict[str, Any]) -> str:
    time_test = payload["time_test"]
    success_ci = payload["success_ci"]
    lines = [
        "---",
        "date: 2026-06-20",
        "status: pass",
        "origin: ai+unit",
        "reviewed: false",
        "task: T13",
        "contract: .pipeline/contracts/v9-forest-n3p.md",
        f"source_head: {payload['source_head']}",
        f"execution_host: {payload['execution_host']}",
        "---",
        "",
        "# T13 Evaluation Framework 验证报告",
        "",
        "## 结论",
        "",
        f"- 合成评测记录数: {payload['record_count']}",
        "- 已生成 per-query CSV、按 method/bucket 汇总 CSV 与 JSON summary",
        f"- Wilcoxon paired query 数: {time_test['paired_query_count']}, p={time_test['p_value']}",
        f"- Bootstrap SR diff: {success_ci['observed_success_rate_diff_a_minus_b']}, "
        f"CI=[{success_ci['ci_low']}, {success_ci['ci_high']}]",
        "",
        "说明：本报告只验证 T13 评测框架的指标、分组输出和统计检验能落盘；不替代 T14 主评测。T06 难度切点仍为 reviewed:false。",
        "",
        "## 产物",
        "",
    ]
    for key, value in payload["outputs"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("- verification_summary: `.pipeline/experiments/20260620_t13_evaluation_framework_verification/verification_summary.json`")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
