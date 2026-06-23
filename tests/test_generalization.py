from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.evaluation import EvaluationRecord
from forest_n3p.generalization import (
    GeneralizationConfig,
    GeneralizationQuery,
    build_generalization_verdict,
    default_ood_profiles,
    run_generalization_evaluation,
)
from forest_n3p.training_data import TrainingProfile


def _write_frontmatter(path: Path, **values: str) -> Path:
    lines = ["---", *(f"{key}: {value}" for key, value in values.items()), "---", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _write_synthetic_realmap(tmp_path: Path) -> Path:
    root = tmp_path / "realmaps" / "open_room"
    root.mkdir(parents=True)
    image = np.full((96, 96), 254, dtype=np.uint8)
    image[:2, :] = 0
    image[-2:, :] = 0
    image[:, :2] = 0
    image[:, -2:] = 0
    assert cv2.imwrite(str(root / "map.pgm"), image)
    (root / "map.yaml").write_text(
        "\n".join(
            [
                "image: map.pgm",
                "resolution: 0.1",
                "origin: [0.0, 0.0, 0.0]",
                "negate: 0",
                "occupied_thresh: 0.65",
                "free_thresh: 0.196",
                "",
            ]
        ),
        encoding="utf-8",
    )
    manifest = {
        "schema": "unit_test_realmap_manifest",
        "usable_map_count": 1,
        "maps": [
            {
                "id": "open_room",
                "yaml": str(root / "map.yaml"),
                "pgm": str(root / "map.pgm"),
                "start_xy": [10, 10],
                "goal_xy": [80, 80],
            }
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def _query(query_id: str, split: str, bucket: str, map_id: str = "map_a") -> GeneralizationQuery:
    return GeneralizationQuery(
        query_id=query_id,
        split=split,
        difficulty_bucket=bucket,
        profile_name=map_id,
        map_id=map_id,
        map_key=map_id,
        map_seed=1,
        query_seed=2,
        seed_index=0,
        map_index=0,
        query_index=0,
        distance_bin_key="d04_08",
        start=(1.0, 1.0, 0.0),
        goal=(5.0, 1.0, 0.0),
    )


def _record(
    query_id: str,
    method: str,
    bucket: str,
    *,
    feasible: bool,
    total_time_s: float,
    map_id: str = "map_a",
) -> EvaluationRecord:
    return EvaluationRecord(
        query_id=query_id,
        method=method,
        difficulty_bucket=bucket,
        distance_bin_key="d04_08",
        success=feasible,
        feasible=feasible,
        total_time_s=total_time_s,
        total_expansions=10,
        path_length_m=4.0 if feasible else None,
        reference_path_length_m=4.0,
        path_inflation_ratio=0.0 if feasible else None,
        direction_switches=0,
        mean_abs_curvature=0.0,
        min_clearance_m=1.0 if feasible else None,
        collision_violation_count=0,
        fallback_f1_count=0,
        fallback_f2_count=0,
        fallback_f3_count=0,
        fallback_triggered=False,
        subgoal_reachable_count=1 if method == "f_n3p_knn" else None,
        subgoal_attempt_count=1 if method == "f_n3p_knn" else None,
        subgoal_reachability_rate=1.0 if method == "f_n3p_knn" else None,
        failure_reason=None if feasible else "unit_test_failure",
        metadata={"map_id": map_id},
    )


def test_default_ood_profiles_are_outside_t06_training_density_range() -> None:
    profiles = default_ood_profiles()

    assert any(item.trunk_count < 40 for item in profiles)
    assert any(item.trunk_count > 145 for item in profiles)
    assert {item.difficulty_bucket for item in profiles} == {"OOD-Sparse", "OOD-Dense"}


def test_generalization_verdict_encodes_contract_criteria() -> None:
    queries = (
        _query("ood_q0", "ood_density", "OOD-Dense"),
        _query("real_q0", "realmap", "RealMap"),
    )
    records = (
        _record("ood_q0", "vanilla_ha", "OOD-Dense", feasible=True, total_time_s=10.0),
        _record("ood_q0", "f_n3p_knn", "OOD-Dense", feasible=True, total_time_s=4.0),
        _record("real_q0", "vanilla_ha", "RealMap", feasible=True, total_time_s=10.0),
        _record("real_q0", "f_n3p_knn", "RealMap", feasible=True, total_time_s=7.0),
    )

    verdict = build_generalization_verdict(
        records,
        queries,
        GeneralizationConfig(),
        available_methods=("vanilla_ha", "f_n3p_knn"),
    )

    assert verdict["criteria"]["failure_criterion_2_ood_success_drop_le_5pp"] is True
    assert verdict["criteria"]["failure_criterion_4_realmap_time_reduction_ge_20pct"] is True
    assert verdict["ood_bucket_verdicts"]["OOD-Dense"]["success_drop_pp"] == 0.0
    assert verdict["realmap_aggregate_verdict"]["median_time_reduction"] == 0.30000000000000004


def test_smoke_generalization_evaluation_writes_outputs(tmp_path: Path) -> None:
    manifest_path = _write_synthetic_realmap(tmp_path)
    contract = _write_frontmatter(tmp_path / "contract.md", status="approved")
    config = GeneralizationConfig(
        methods=("vanilla_ha",),
        ood_queries_per_bucket=1,
        realmap_queries_per_map=1,
        seed_count=1,
        queries_per_map=1,
        width_cells=180,
        height_cells=180,
        distance_bins=parse_distance_bins("4:8"),
        realmap_distance_bins=parse_distance_bins("4:8"),
        realmap_manifest_path=manifest_path,
        contract_path=contract,
        ood_profiles=(
            TrainingProfile("ood_sparse_test", "OOD-Sparse", trunk_count=8, trunk_gap_m=1.8, trunk_gap_jitter=0.10),
            TrainingProfile("ood_dense_test", "OOD-Dense", trunk_count=10, trunk_gap_m=1.6, trunk_gap_jitter=0.10),
        ),
        teacher_timeout_s=1.0,
        teacher_max_nodes=3_000,
        bootstrap_resamples=20,
    )

    result = run_generalization_evaluation(tmp_path / "t16_smoke", config=config, source_head="unit-test", command="unit-test")

    assert len(result.queries) == 3
    assert len(result.records) == 3
    assert result.verdict["status"] == "candidate_or_framework"
    assert result.output_paths["records_csv"].exists()
    assert result.output_paths["summary_json"].exists()
    assert result.output_paths["queries_csv"].exists()
    assert result.output_paths["verdict_json"].exists()
    payload = json.loads(result.output_paths["summary_json"].read_text(encoding="utf-8"))
    assert payload["record_count"] == 3
