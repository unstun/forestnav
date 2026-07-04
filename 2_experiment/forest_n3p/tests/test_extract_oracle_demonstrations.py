from forest_n3p.main_evaluation import MainEvaluationConfig
from forest_n3p.scripts.extract_oracle_demonstrations import _csv_set, _row_matches_selection
from forest_n3p.scripts.run_oracle_connector_analysis import _grid_for_row, _profiles_from_bucket_mode
from forest_n3p.third_party.pathplan import TwoCircleFootprint


def _row(**updates):
    row = {
        "difficulty_bucket": "Extreme",
        "oracle_connectable": True,
        "best_oracle": "oracle_b",
        "oracle_b_selected_candidate_source": "goal_annulus",
    }
    row.update(updates)
    return row


def test_csv_set_strips_empty_values():
    assert _csv_set("Complex, Extreme,,") == {"Complex", "Extreme"}
    assert _csv_set(None) == set()


def test_grid_cache_key_includes_profile_name():
    cfg = MainEvaluationConfig(
        seed=20260620,
        profiles=_profiles_from_bucket_mode("validation_t06"),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    cache = {}
    row_a = {"profile_name": "complex_d02", "map_seed": 20360620}
    row_b = {"profile_name": "complex_d03", "map_seed": 20360620}

    grid_a = _grid_for_row(row_a, cfg, footprint, cache)
    grid_b = _grid_for_row(row_b, cfg, footprint, cache)

    assert grid_a is not grid_b
    assert set(cache) == {("complex_d02", 20360620), ("complex_d03", 20360620)}


def test_row_selection_filters_bucket_and_best_oracle():
    assert _row_matches_selection(
        _row(),
        buckets={"Extreme"},
        filter_best_oracle="oracle_b",
        include_b_sources=set(),
        exclude_b_sources=set(),
    )
    assert not _row_matches_selection(
        _row(difficulty_bucket="Complex"),
        buckets={"Extreme"},
        filter_best_oracle="oracle_b",
        include_b_sources=set(),
        exclude_b_sources=set(),
    )
    assert not _row_matches_selection(
        _row(best_oracle="oracle_a"),
        buckets={"Extreme"},
        filter_best_oracle="oracle_b",
        include_b_sources=set(),
        exclude_b_sources=set(),
    )


def test_row_selection_filters_oracle_b_candidate_source():
    assert _row_matches_selection(
        _row(),
        buckets={"Extreme"},
        filter_best_oracle="oracle_b",
        include_b_sources={"goal_annulus"},
        exclude_b_sources=set(),
    )
    assert not _row_matches_selection(
        _row(oracle_b_selected_candidate_source="voronoi_skeleton"),
        buckets={"Extreme"},
        filter_best_oracle="oracle_b",
        include_b_sources={"goal_annulus"},
        exclude_b_sources=set(),
    )
    assert not _row_matches_selection(
        _row(oracle_b_selected_candidate_source="voronoi_skeleton"),
        buckets={"Extreme"},
        filter_best_oracle="oracle_b",
        include_b_sources=set(),
        exclude_b_sources={"voronoi_skeleton"},
    )
    assert _row_matches_selection(
        _row(best_oracle="oracle_a", oracle_b_selected_candidate_source="voronoi_skeleton"),
        buckets={"Extreme"},
        filter_best_oracle="any",
        include_b_sources=set(),
        exclude_b_sources={"voronoi_skeleton"},
    )
