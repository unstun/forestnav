# Module2 RL-RS BC Datasets

This directory contains source-bound behavior-cloning datasets for Module2 F01/F02.

Current highest-status dataset: `formal_v2_trainable_not_paper_final`.

Files:

- `manifest.json`: F01 preview provenance, schema, filters, and boundaries.
- `manifest_formal_v1.json`: F02 formal-v1 corpus provenance. This version is now stale after the map-cache audit.
- `manifest_formal_v2.json`: F02 formal-v2 corpus provenance, cache-fix root cause, and collision audit.
- `demonstrations_preview20.parquet`: 1109 demonstrations from 20 replayed C02 oracle rows.
- `demonstrations_preview20_summary.json`: extraction summary.
- `demonstrations_formal_v1.parquet`: 85514 demonstrations from 1035 replayed source rows.
- `demonstrations_formal_v1_summary.json`: merge summary.
- `demonstrations_formal_v2.parquet`: 83809 demonstrations from 1032 replayed source rows.
- `demonstrations_formal_v2_summary.json`: merge summary.

Formal v2 composition:

- Complex oracle-A shard: 512 source rows, 40619 demo rows.
- Extreme oracle-A shard: 512 source rows, 42428 demo rows.
- Goal-annulus oracle-B shard: 8 current-code-replayable source rows, 762 demo rows.

Key boundary:

- `demonstrations_formal_v2.parquet` is suitable for the next F02 BC baseline rerun.
- `demonstrations_formal_v1.parquet` is not clean training evidence after the map-cache audit: true-profile collision audit found 4764 colliding demo rows across 236 source rows.
- It is not a paper-final full corpus.
- Patch observations are reconstructable from map seed, pose, goal, and config; only scalar observations are stored inline in this preview.
- Historical C02 contains 58 `goal_annulus` B-only rows, but only 8 are currently replayable under the profile-aware map reconstruction and current collision semantics.
- `voronoi_skeleton` B-only rows are not claimed as valid paper evidence until separately audited.
- No PPO training or planner integration is implied by these datasets.
