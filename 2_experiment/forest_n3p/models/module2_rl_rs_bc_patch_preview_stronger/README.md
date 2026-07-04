# Module2 F02.3 Patch-Scalar CNN Preview Stronger Run

This directory records a stronger preview run for the patch+scalar CNN policy.

It uses the same preview20 dataset as the smoke run, with larger CNN channels
and more epochs. The action loss improves, but closed-loop behavior is still
weak.

## Metrics

| Metric | Value |
|---|---:|
| dataset rows | 1109 |
| best epoch | 45 |
| epochs ran | 58 |
| validation MAE rad | 0.13033735752105713 |
| held-out episodes | 5 |
| terminal RS success | 1 |
| collision | 4 |
| success rate | 0.2 |

For comparison, the obstacle-summary preview smoke achieved 4/5 terminal RS
success. This means "uses a CNN over patches" is not automatically stronger
under the current protocol.

## Artifacts

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `008c1e7ca964419296e593bf291f4e03305009a9db58de2e36dc057943de0d56` |
| `history.json` | `aba9402a230657bdbfbca1f5d9a352b6899ead99fe4dcab6aee8c7999d104177` |
| `summary.json` | `7536536e967436108ace0228e5af273d5343dedad52810e89958763acd24548d` |

## Boundary

This is a preview result, not a formal-v1 CNN baseline. F02.3 remains open.
