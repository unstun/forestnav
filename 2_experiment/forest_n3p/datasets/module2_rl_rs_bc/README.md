# Module2 RL-RS BC Datasets

This directory contains source-bound behavior-cloning datasets for Module2 F01/F02.

Current highest-status dataset: `formal_v1_trainable_not_paper_final`.

Files:

- `manifest.json`: F01 preview provenance, schema, filters, and boundaries.
- `manifest_formal_v1.json`: F02 trainable formal-v1 corpus provenance and boundaries.
- `demonstrations_preview20.parquet`: 1109 demonstrations from 20 replayed C02 oracle rows.
- `demonstrations_preview20_summary.json`: extraction summary.
- `demonstrations_formal_v1.parquet`: 85514 demonstrations from 1035 replayed source rows.
- `demonstrations_formal_v1_summary.json`: merge summary.

Formal v1 composition:

- Complex oracle-A shard: 512 source rows, 42293 demo rows.
- Extreme oracle-A shard: 512 source rows, 42209 demo rows.
- Goal-annulus oracle-B shard: 11 current-code-replayable source rows, 1012 demo rows.

Key boundary:

- `demonstrations_formal_v1.parquet` is suitable for F02.2 BC baseline training.
- It is not a paper-final full corpus.
- Patch observations are reconstructable from map seed, pose, goal, and config; only scalar observations are stored inline in this preview.
- Historical C02 contains 58 `goal_annulus` B-only rows, but only 11 are currently replayable under the current code/collision semantics.
- `voronoi_skeleton` B-only rows are not claimed as valid paper evidence until separately audited.
- No PPO training or planner integration is implied by these datasets.
