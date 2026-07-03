from forest_n3p.scripts.run_policy_forward_budget import derive_observation_shapes, next_power_of_two


def test_next_power_of_two_rounds_up_positive_values():
    assert next_power_of_two(1) == 1
    assert next_power_of_two(60) == 64
    assert next_power_of_two(72) == 128


def test_d02_observation_shapes_are_derived_from_c02_budget():
    shapes = derive_observation_shapes(
        patch_cells_spec="auto,margin_auto",
        resolution_m=0.1,
        goal_annulus_max_radius_m=3.0,
        footprint_length_m=0.924,
        footprint_width_m=0.740,
        patch_channels=2,
        range_bins_mode="match_patch",
        scalar_dim=8,
        action_dim=1,
    )

    by_label = {shape.label: shape for shape in shapes}
    assert by_label["annulus_auto"].patch_cells == 64
    assert by_label["annulus_auto"].patch_extent_m == 6.4
    assert by_label["annulus_auto"].range_bins == 64
    assert by_label["footprint_margin_auto"].patch_cells == 128
    assert by_label["footprint_margin_auto"].patch_extent_m == 12.8
    assert by_label["footprint_margin_auto"].range_bins == 128
