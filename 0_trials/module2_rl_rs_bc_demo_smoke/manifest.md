---
date: 2026-07-03
status: f01_1_smoke_complete
origin: codex+experiment
reviewed: false
source_head: 96be287b3ab67f4899d4f2ab765c21f75c5661e8
---

# Module2 F01.1 Oracle Demonstration Extraction Smoke

## Contents

| File | Meaning |
|---|---|
| `demonstrations_smoke3.parquet` | first 3 connectable C02 rows, best oracle replay |
| `demonstrations_smoke3_summary.json` | summary for `demonstrations_smoke3.parquet` |
| `demonstrations_bonly_smoke1.parquet` | first B-only goal-annulus C02 row, best oracle replay |
| `demonstrations_bonly_smoke1_summary.json` | summary for `demonstrations_bonly_smoke1.parquet` |

## Key Checks

- `demonstrations_smoke3.parquet`: 202 rows, all `oracle_a`, all forward direction, terminal-ready samples filtered.
- `demonstrations_bonly_smoke1.parquet`: 136 rows, all `oracle_b`, all forward direction, terminal-ready samples filtered.
- Both outputs use source head `96be287b3ab67f4899d4f2ab765c21f75c5661e8`.

## Boundary

This is a replay/extraction smoke, not the final BC training corpus.
