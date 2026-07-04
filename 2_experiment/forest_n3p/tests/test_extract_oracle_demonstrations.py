from forest_n3p.scripts.extract_oracle_demonstrations import _csv_set, _row_matches_selection


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
