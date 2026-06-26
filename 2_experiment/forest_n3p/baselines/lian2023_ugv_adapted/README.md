# Lian2023-UGV adapted baseline

This package is a thin adapter around `lian2023_strict`.

It keeps the Lian2023 Algorithm 1 + OCP implementation in
`2_experiment/lian2023_strict_repro/` and replaces only the vehicle geometry
and motion limits with the local UGV parameters used by `UGVBicycleEnv`.

Use this baseline as `Lian2023-UGV` in local `realmap_a` experiments. Do not use
it as the Lian2023 original or as a Table II reproduction result.
