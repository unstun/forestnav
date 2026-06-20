from __future__ import annotations

import json
from pathlib import Path

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.main_evaluation import MainEvaluationConfig, preflight_main_evaluation, run_main_evaluation
from forest_n3p.training_data import TrainingProfile


def test_preflight_blocks_unreviewed_cutpoints_and_missing_md_dqn() -> None:
    report = preflight_main_evaluation(MainEvaluationConfig())

    assert not report.ok_to_run
    assert any("cutpoint supplement" in item for item in report.blocking_issues)
    assert any("md_dqn unavailable" in item for item in report.blocking_issues)


def test_smoke_main_evaluation_writes_outputs(tmp_path: Path) -> None:
    config = MainEvaluationConfig(
        queries_per_bucket=1,
        seed_count=1,
        queries_per_map=1,
        width_cells=180,
        height_cells=180,
        methods=("vanilla_ha",),
        profiles=(
            TrainingProfile("easy_test", "Easy", trunk_count=8, trunk_gap_m=1.80, trunk_gap_jitter=0.10),
            TrainingProfile("complex_test", "Complex", trunk_count=10, trunk_gap_m=1.60, trunk_gap_jitter=0.10),
            TrainingProfile("extreme_test", "Extreme", trunk_count=12, trunk_gap_m=1.45, trunk_gap_jitter=0.10),
        ),
        distance_bins=parse_distance_bins("4:8"),
        allow_unreviewed_cutpoints=True,
        allow_missing_md_dqn=True,
        enforce_t14_scale=False,
        teacher_timeout_s=1.0,
        teacher_max_nodes=3_000,
        bootstrap_resamples=100,
    )

    result = run_main_evaluation(tmp_path / "t14_smoke", config=config, source_head="unit-test", command="unit-test")

    assert len(result.queries) == 3
    assert len(result.records) == 3
    assert result.verdict["status"] == "candidate_or_smoke"
    assert result.output_paths["records_csv"].exists()
    assert result.output_paths["summary_json"].exists()
    assert result.output_paths["queries_csv"].exists()
    payload = json.loads(result.output_paths["summary_json"].read_text(encoding="utf-8"))
    assert payload["record_count"] == 3
