from __future__ import annotations

import csv

from forest_n3p.ablation import default_t15_variants, feature_indices_for_variant
from forest_n3p.scripts.run_ablation_experiments import main as run_ablation_cli


def test_default_t15_variants_cover_all_eight_groups() -> None:
    variants = default_t15_variants()
    groups = {variant.group_id for variant in variants}
    planned = {variant.variant_id for variant in variants if not variant.runnable}

    assert groups == {"A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"}
    assert "A1_curvature_boundary_relabel_required" in planned
    assert "A4_ray64_reextract_required" in planned
    assert "A5_lmax4_relabel_required" in planned


def test_feature_indices_match_expected_dimensions() -> None:
    assert len(feature_indices_for_variant("full41")) == 41
    assert len(feature_indices_for_variant("no_density")) == 38
    assert len(feature_indices_for_variant("no_heading_delta")) == 39
    assert len(feature_indices_for_variant("ray16")) == 25


def test_ablation_cli_dry_run_writes_manifest(tmp_path) -> None:
    output_dir = tmp_path / "t15_manifest"

    rc = run_ablation_cli(["--output-dir", str(output_dir), "--dry-run-manifest"])

    assert rc == 0
    with (output_dir / "ablation_manifest.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(default_t15_variants())
    assert any(row["variant_id"] == "A8_noise05" and row["runnable"] == "True" for row in rows)
