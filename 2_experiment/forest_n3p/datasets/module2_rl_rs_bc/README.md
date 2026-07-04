# Module2 RL-RS BC Dataset Preview

This directory contains a source-bound preview dataset for Module2 F01.

Current status: `preview`, not the final BC training corpus.

Files:

- `manifest.json`: dataset provenance, schema, filters, and boundaries.
- `demonstrations_preview20.parquet`: 1109 demonstrations from 20 replayed C02 oracle rows.
- `demonstrations_preview20_summary.json`: extraction summary.

Key boundary:

- No BC/PPO training has started from this dataset.
- Patch observations are reconstructable from map seed, pose, goal, and config; only scalar observations are stored inline in this preview.
- `voronoi_skeleton` B-only rows are not claimed as valid paper evidence until separately audited.
