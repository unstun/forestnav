# Module2 F02.3 Patch-Scalar CNN Formal V1 Pilot

This directory records a bounded formal-v1 pilot for the patch+scalar CNN
policy.

The pilot uses a random bounded subset of the formal-v1 corpus:

- max train rows: 4096
- max validation rows: 1024
- validation source rows: 241

## Metrics

| Metric | Value |
|---|---:|
| dataset rows | 85514 |
| train rows | 4096 |
| validation rows | 1024 |
| train source rows | 740 |
| validation source rows | 241 |
| best epoch | 10 |
| epochs ran | 19 |
| validation MAE rad | 0.1442122608423233 |
| terminal RS success | 44 |
| collision | 185 |
| truncated | 4 |
| runtime error | 8 |
| success rate | 0.1825726141078838 |
| collision rate | 0.7676348547717843 |

For comparison, formal obstacle-summary BC reached 84/259 success with no
runtime errors. This pilot is therefore not suitable as a warm-start checkpoint.

## Artifacts

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `a49d1869928569ca79e82ebd5265102aadd6685c44581583797ea03833d48ab1` |
| `history.json` | `4e81d585fe970344bc55c05c40d8a42b300a54b7a209b731a4fd18d6993b6e5e` |
| `summary.json` | `a95b50355b628557017a7a4fe07eb2e49b8d882c85c1fb0c8335e7da0d6c33c3` |

## Boundary

- This is a bounded pilot, not a full formal CNN baseline.
- The run used source head `866b6a825613311c8aea7c21e83eb73ef532a59d`.
- Runtime error messages were not recorded in this run; the script was improved
  afterward to retain exception messages.
- Do not use this checkpoint for PPO warm start.
