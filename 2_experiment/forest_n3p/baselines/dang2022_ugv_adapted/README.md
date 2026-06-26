# Dang2022-UGV adapted baseline

This package is a thin adapter around `dang2022_strict`.

It keeps the Dang2022 Improved Hybrid A* implementation in
`2_experiment/dang2022_strict_repro/` and replaces only the vehicle geometry,
two-circle collision footprint, and kinematic limits with the local UGV
parameters used by `UGVBicycleEnv`.

When the strict planner succeeds through Reeds-Shepp analytic expansion, this
adapter exports the dense RS connection as `stats["analytic_path_cells"]`, with
`analytic_path_cell_count` and `analytic_path_source` for plotting/audit.

The adapter writes `result.dense_path` to benchmark traces when available, and
falls back to the sparse key poses only for older strict results. This avoids
plotting curved Hybrid A* / RS motions as misleading straight endpoint chords.

Use this baseline as `Dang2022-UGV` in local `realmap_a` experiments. It is not
the Dang2022 original result from Table 1 or Table 2.
