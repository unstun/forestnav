# Module2 F02 Formal Corpus Speed Probe

## 直观结论

This directory records a 1-row extraction probe for the F02.2 formal BC corpus.

The full candidate set is 6284 C02 rows after selecting all best-A rows and
excluding `voronoi_skeleton` best-B rows. A 1-row replay took about 2.1 seconds
on the local Mac and produced 81 demonstration rows. That means a naive
single-process full extraction is likely hour-scale on this machine.

## Command

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --filter-best-oracle any \
  --exclude-oracle-b-candidate-sources voronoi_skeleton \
  --oracle-types best \
  --progress-every 1 \
  --max-records 1 \
  --source-head f5cffe9696df8d05b0f81d685f036cd71e718c0c \
  --output 0_trials/module2_rl_rs_bc_formal_speed/demonstrations_formal_v1_max1.parquet
```

## Artifacts

| File | SHA-256 |
|---|---|
| `demonstrations_formal_v1_max1.parquet` | `be830658b474843c04b7aaf2e25219a6d3eabc3db033515a21a09d17b3c2687d` |
| `demonstrations_formal_v1_max1_summary.json` | `52a1d3f3ef3b92b38fa70848805eb0319bfc9fe214f61a300f7fcad9110d90b5` |

## Result

- selected rows: 1
- replay success rows: 1
- demonstration rows: 81
- skipped terminal-RS-ready rows: 15
- skipped collision/reverse/short rows: 0/0/0

## Boundary

This is only a speed probe and extractor smoke. It is not a training dataset and
must not be reported as a BC baseline.
