# Dang2022 Strict Reproduction

This directory is an independent Python reproduction workspace for:

Dang, Ahn, Lee, and Lee, "Improved Analytic Expansions in Hybrid A-Star Path Planning for Non-Holonomic Robots," Applied Sciences, 2022.

The package implements the paper-level Hybrid A* baseline with multi-curvature Reeds-Shepp analytic expansion, Dang2022 Eq.2 Voronoi field cost, and Eq.3/Eq.4 candidate selection. It does not import the local UGV benchmark package.

`PlanResult.path` stores sparse key poses. `PlanResult.dense_path` stores the
same route sampled at `collision_step_m` resolution for plotting and downstream
trace export. The dense export is an observation/output fix only; it does not
change the search, candidate selection, or collision logic.

## Scope

The paper reports Grid map A/B and benchmark maps, but the exact author occupancy grids and scripts are not included in the paper bundle. The local strict smoke therefore uses reconstructed 50 x 30 m Map A/B scenes and records this gap in every run note.

## Smoke Command

```bash
PYTHONPATH=2_experiment/dang2022_strict_repro/src \
python 2_experiment/dang2022_strict_repro/scripts/run_paper_scenes.py \
  --out-dir 2_experiment/dang2022_strict_repro/outputs/2026-05-14_dang2022_strict_smoke
```
