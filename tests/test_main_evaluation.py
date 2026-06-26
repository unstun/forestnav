from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from forest_n3p.evaluation import EvaluationConfig, EvaluationRun
from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _evaluate_run_with_collision_rejection,
    preflight_main_evaluation,
    run_main_evaluation,
    validation_main_evaluation_profiles,
)
from forest_n3p.scripts.run_main_evaluation import main as run_main_evaluation_cli
from forest_n3p.training_data import TrainingProfile
from pathplan import GridMap, TwoCircleFootprint


def _blocked_map(width: int = 120, height: int = 120, resolution: float = 0.1) -> GridMap:
    grid = np.zeros((height, width), dtype=np.uint8)
    grid[55:66, 50] = 1
    return GridMap(grid, resolution=resolution, origin=(0.0, 0.0))


def _footprint() -> TwoCircleFootprint:
    return TwoCircleFootprint.from_box(length=0.924, width=0.740)


def _write_frontmatter(path: Path, **values: str) -> Path:
    lines = ["---", *(f"{key}: {value}" for key, value in values.items()), "---", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _write_human_review_form(path: Path, decisions: dict[str, str]) -> Path:
    rows = [
        "# T14 Human Review Form",
        "",
        "| decision_id | decision | reviewer | date | notes |",
        "|---|---|---|---|---|",
    ]
    for decision_id in ("D-T14-09", "D-T14-10", "D-T14-11", "D-T14-12"):
        rows.append(f"| {decision_id} | {decisions.get(decision_id, '')} | Dr Sun | 2026-06-21 | unit test |")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def _write_t06_validation_summary(path: Path) -> Path:
    payload = {
        "summary": {
            "density_summaries": [
                {"level_key": "d00", "difficulty_bucket": "Easy"},
                {"level_key": "d01", "difficulty_bucket": "Easy"},
                {"level_key": "d02", "difficulty_bucket": "Complex"},
                {"level_key": "d03", "difficulty_bucket": "Complex"},
                {"level_key": "d04", "difficulty_bucket": "Complex"},
                {"level_key": "d05", "difficulty_bucket": "Extreme"},
                {"level_key": "d06", "difficulty_bucket": "Extreme"},
                {"level_key": "d07", "difficulty_bucket": "Extreme"},
            ]
        }
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _formal_human_decisions() -> dict[str, str]:
    return {
        "D-T14-09": "revise_to_validation_cutpoints",
        "D-T14-10": "approve",
        "D-T14-11": "formal_baseline",
        "D-T14-12": "approve_after_rerun_passes",
    }


def test_preflight_blocks_unreviewed_cutpoints_and_missing_human_review(tmp_path: Path) -> None:
    report = preflight_main_evaluation(
        MainEvaluationConfig(
            cutpoint_supplement_path=tmp_path / "missing_supplement.md",
            human_review_form_path=tmp_path / "missing_human_review.md",
        )
    )

    assert not report.ok_to_run
    assert any("cutpoint supplement" in item for item in report.blocking_issues)
    assert any("human review is unresolved" in item for item in report.blocking_issues)


def test_preflight_blocks_unresolved_human_review_by_default(tmp_path: Path) -> None:
    contract = _write_frontmatter(tmp_path / "contract.md", status="approved")
    supplement = _write_frontmatter(tmp_path / "supplement.md", reviewed="true")
    review_form = _write_human_review_form(tmp_path / "human_review_form.md", {})

    report = preflight_main_evaluation(
        MainEvaluationConfig(
            methods=("vanilla_ha",),
            contract_path=contract,
            cutpoint_supplement_path=supplement,
            human_review_form_path=review_form,
            enforce_t14_scale=False,
        )
    )

    assert not report.ok_to_run
    assert not report.human_review_satisfied
    assert any("D-T14-09 missing decision" in item for item in report.blocking_issues)


def test_preflight_accepts_formal_human_review_decisions(tmp_path: Path) -> None:
    contract = _write_frontmatter(tmp_path / "contract.md", status="approved")
    supplement = _write_frontmatter(tmp_path / "supplement.md", reviewed="true")
    review_form = _write_human_review_form(tmp_path / "human_review_form.md", _formal_human_decisions())
    validation_summary = _write_t06_validation_summary(tmp_path / "t06_validation_summary.json")

    report = preflight_main_evaluation(
        MainEvaluationConfig(
            methods=("vanilla_ha",),
            profiles=validation_main_evaluation_profiles(),
            contract_path=contract,
            cutpoint_supplement_path=supplement,
            t06_validation_summary_path=validation_summary,
            human_review_form_path=review_form,
            enforce_t14_scale=False,
        )
    )

    assert report.ok_to_run
    assert report.human_review_satisfied
    assert report.profile_bucket_satisfied
    assert report.human_review_decisions["D-T14-09"] == "revise_to_validation_cutpoints"


def test_preflight_accepts_t15_mlp_when_checkpoint_files_exist(tmp_path: Path) -> None:
    contract = _write_frontmatter(tmp_path / "contract.md", status="approved")
    supplement = _write_frontmatter(tmp_path / "supplement.md", reviewed="true")
    review_form = _write_human_review_form(tmp_path / "human_review_form.md", _formal_human_decisions())
    validation_summary = _write_t06_validation_summary(tmp_path / "t06_validation_summary.json")
    mlp_dir = tmp_path / "mlp"
    mlp_dir.mkdir()
    (mlp_dir / "checkpoint.pt").write_bytes(b"unit-test")
    (mlp_dir / "metadata.json").write_text("{}", encoding="utf-8")

    report = preflight_main_evaluation(
        MainEvaluationConfig(
            methods=("mlp",),
            profiles=validation_main_evaluation_profiles(),
            contract_path=contract,
            cutpoint_supplement_path=supplement,
            t06_validation_summary_path=validation_summary,
            human_review_form_path=review_form,
            mlp_model_dir=mlp_dir,
            enforce_t14_scale=False,
        )
    )

    assert report.ok_to_run
    assert report.available_methods == ("mlp",)


def test_preflight_blocks_revised_cutpoints_with_stale_profiles(tmp_path: Path) -> None:
    contract = _write_frontmatter(tmp_path / "contract.md", status="approved")
    supplement = _write_frontmatter(tmp_path / "supplement.md", reviewed="true")
    review_form = _write_human_review_form(tmp_path / "human_review_form.md", _formal_human_decisions())
    validation_summary = _write_t06_validation_summary(tmp_path / "t06_validation_summary.json")

    report = preflight_main_evaluation(
        MainEvaluationConfig(
            methods=("vanilla_ha",),
            contract_path=contract,
            cutpoint_supplement_path=supplement,
            t06_validation_summary_path=validation_summary,
            human_review_form_path=review_form,
            enforce_t14_scale=False,
        )
    )

    assert not report.ok_to_run
    assert report.human_review_satisfied
    assert not report.profile_bucket_satisfied
    assert any("d03 bucket=Extreme expected=Complex" in item for item in report.blocking_issues)


def test_preflight_blocks_original_decision_with_validation_profiles(tmp_path: Path) -> None:
    contract = _write_frontmatter(tmp_path / "contract.md", status="approved")
    supplement = _write_frontmatter(tmp_path / "supplement.md", reviewed="true")
    decisions = _formal_human_decisions()
    decisions["D-T14-09"] = "approve_original_with_justification"
    review_form = _write_human_review_form(tmp_path / "human_review_form.md", decisions)

    report = preflight_main_evaluation(
        MainEvaluationConfig(
            methods=("vanilla_ha",),
            profiles=validation_main_evaluation_profiles(),
            contract_path=contract,
            cutpoint_supplement_path=supplement,
            human_review_form_path=review_form,
            enforce_t14_scale=False,
        )
    )

    assert not report.ok_to_run
    assert not report.profile_bucket_satisfied
    assert any("d03 bucket=Complex expected=Extreme" in item for item in report.blocking_issues)


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
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
        human_review_form_path=tmp_path / "missing_human_review.md",
        teacher_timeout_s=1.0,
        teacher_max_nodes=3_000,
        bootstrap_resamples=100,
    )

    result = run_main_evaluation(tmp_path / "t14_smoke", config=config, source_head="unit-test", command="unit-test")

    assert len(result.queries) == 3
    assert len(result.records) == 3
    assert result.verdict["status"] == "candidate_or_smoke"
    assert result.verdict["method_exception_total"] == 0
    assert result.output_paths["records_csv"].exists()
    assert result.output_paths["summary_json"].exists()
    assert result.output_paths["queries_csv"].exists()
    payload = json.loads(result.output_paths["summary_json"].read_text(encoding="utf-8"))
    assert payload["record_count"] == 3


def test_collision_rejection_marks_colliding_success_as_failed() -> None:
    run = EvaluationRun(
        query_id="q_collision",
        method="n3p_k1",
        difficulty_bucket="Extreme",
        distance_bin_key="d12_16",
        success=True,
        path=((4.5, 6.0, 0.0), (5.5, 6.0, 0.0)),
        total_time_s=0.25,
        total_expansions=42,
        reference_path_length_m=1.0,
        fallback_f2_count=1,
        metadata={"profile_name": "extreme_test"},
    )

    record = _evaluate_run_with_collision_rejection(
        run,
        _blocked_map(),
        _footprint(),
        config=EvaluationConfig(path_sample_step_m=0.05),
    )

    assert not record.success
    assert not record.feasible
    assert record.collision_violation_count == 0
    assert record.path_length_m is None
    assert record.path_inflation_ratio is None
    assert record.total_time_s == 0.25
    assert record.total_expansions == 42
    assert record.fallback_f2_count == 1
    assert record.failure_reason is not None
    assert record.failure_reason.startswith("collision_violation_rejected:")
    assert record.metadata["profile_name"] == "extreme_test"
    assert record.metadata["rejected_collision_violation_count"] > 0
    assert record.metadata["rejected_collision_path_length_m"] > 0.0


def test_cli_writes_k_neighbors_and_source_head_overrides(tmp_path: Path) -> None:
    output_dir = tmp_path / "t14_cli_overrides"

    rc = run_main_evaluation_cli(
        [
            "--output-dir",
            str(output_dir),
            "--queries-per-bucket",
            "1",
            "--seed-count",
            "1",
            "--queries-per-map",
            "1",
            "--methods",
            "vanilla_ha",
            "--density-profile-buckets",
            "validation_t06",
            "--distance-bins",
            "4:8",
            "--allow-unreviewed-cutpoints",
            "--allow-unresolved-human-review",
            "--human-review-form-path",
            str(tmp_path / "missing_human_review.md"),
            "--no-enforce-t14-scale",
            "--bootstrap-resamples",
            "20",
            "--k-neighbors",
            "17",
            "--max-steps-override",
            "4",
            "--disable-f2",
            "--prediction-noise-sigma-m",
            "0.3",
            "--source-head",
            "unit-test-head",
        ]
    )

    assert rc == 0
    payload = json.loads((output_dir / "run_config.json").read_text(encoding="utf-8"))
    assert payload["source_head"] == "unit-test-head"
    assert payload["config"]["k_neighbors"] == 17
    assert payload["config"]["max_steps_override"] == 4
    assert payload["config"]["enable_f2"] is False
    assert payload["config"]["prediction_noise_sigma_m"] == 0.3
    assert any(
        item["name"] == "complex_d03" and item["difficulty_bucket"] == "Complex"
        for item in payload["config"]["profiles"]
    )


def test_cli_preflight_only_reports_blocking_issues(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "t14_preflight_only"

    rc = run_main_evaluation_cli(
        [
            "--output-dir",
            str(output_dir),
            "--queries-per-bucket",
            "1",
            "--seed-count",
            "1",
            "--methods",
            "vanilla_ha",
            "--allow-unreviewed-cutpoints",
            "--human-review-form-path",
            str(tmp_path / "missing_human_review.md"),
            "--no-enforce-t14-scale",
            "--preflight-only",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert rc == 2
    assert payload["ok_to_run"] is False
    assert payload["human_review_satisfied"] is False
    assert any("human review is unresolved" in item for item in payload["blocking_issues"])
    assert not output_dir.exists()


def test_cli_preflight_only_accepts_explicitly_degraded_config(tmp_path: Path, capsys) -> None:
    output_dir = tmp_path / "not_created_by_preflight"
    rc = run_main_evaluation_cli(
        [
            "--output-dir",
            str(output_dir),
            "--queries-per-bucket",
            "1",
            "--seed-count",
            "1",
            "--methods",
            "vanilla_ha",
            "--density-profile-buckets",
            "validation_t06",
            "--allow-unreviewed-cutpoints",
            "--allow-unresolved-human-review",
            "--no-enforce-t14-scale",
            "--preflight-only",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert rc == 0
    assert payload["ok_to_run"] is True
    assert payload["t14_scale_satisfied"] is False
    assert not output_dir.exists()
