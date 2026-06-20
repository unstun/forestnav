---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: candidate_failure_analysis
---

# T14 6-method Candidate Failure Analysis

## Plain Conclusion

The T14 6-method candidate is complete enough for diagnosis, but it fails the current Contract. The failure is not collision safety or missing data. The failure is that F-N3P is slower than vanilla Hybrid A* at the median in Complex and Extreme buckets, while the Contract requires at least 50% median time reduction.

## Source Artifacts

- source records: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/records.csv`
- source summary: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/summary.json`
- source verdict: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/verdict.json`
- human review packet: `.pipeline/experiments/20260620_t14_human_review_packet/review_packet.md`

## Contract Failure

| bucket | median_time_reduction | success_drop_pp | median_path_inflation_ratio | status |
|---|---:|---:|---:|---|
| Complex | -0.2993 | -12.0 | 0.0000 | fail |
| Extreme | -0.2621 | -8.0 | 0.0005 | fail |

Interpretation: negative `median_time_reduction` means F-N3P has a larger median runtime than vanilla HA*. Negative `success_drop_pp` means F-N3P has higher feasible success rate than vanilla HA*; that is a positive safety/reachability signal, but it does not satisfy the current speed-centered success criterion.

## Failure Mode Counts

| bucket | paired | F-N3P slower | F-N3P faster | rescue vanilla failure | regress vanilla success | fallback triggered | F3 fallback | median delta fallback | median delta no fallback |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Easy | 100 | 43 | 57 | 7 | 0 | 65 | 4 | 0.0093 | -0.1497 |
| Complex | 100 | 42 | 58 | 12 | 0 | 68 | 6 | 0.0101 | -0.1465 |
| Extreme | 100 | 60 | 40 | 8 | 0 | 84 | 13 | 0.1132 | -0.1490 |

The core pattern is visible in `failure_mode_counts.csv`: F-N3P rescues many vanilla failures, but fallback use is frequent and the median runtime delta is positive in the Contract buckets.

## MD-DQN Boundary

- MD-DQN rows: 300
- MD-DQN success: 3
- MD-DQN feasible: 3
- `md_dqn_not_reached`: 297

This supports a narrow claim only: the DQN10 adapter runs and the historical checkpoint performs poorly on this distribution. It does not prove that a properly trained RL baseline would fail.

## Generated Tables

| file | contents |
|---|---|
| `method_bucket_deltas.csv` | Per-method bucket summaries and deltas against vanilla HA* |
| `paired_f_n3p_vs_vanilla.csv` | One paired row per query for F-N3P vs vanilla HA* |
| `failure_mode_counts.csv` | Bucket-level speed/rescue/regression/fallback counts |
| `distance_bin_deltas.csv` | Distance-bin breakdown of runtime and feasibility deltas |
| `worst_cases.csv` | 20 slowest and 20 fastest F-N3P-vs-vanilla paired queries |
| `md_dqn_failure_counts.csv` | MD-DQN failure reason counts by bucket |
| `manifest.json` | Source and output provenance |

## Next Technical Questions

1. Is the speed failure mainly caused by fallback hierarchy overhead, KNN subgoal quality, or vanilla HA* being too strong on the selected cutpoints?
2. Should the method be redesigned around fewer fallback calls, cheaper local connection, or a different subgoal selection criterion?
3. Should T06 cutpoints be revised before using this run as formal evidence?
4. Should MD-DQN be retrained on the v9 ForestNav distribution before it appears as a formal baseline?

## Claim Boundary

- Can say: the current 6-method candidate is complete and collision-free, but fails the Contract speed criterion.
- Can say: F-N3P improves feasible success over vanilla HA* in Complex/Extreme in this candidate.
- Cannot say: T14 is complete.
- Cannot say: the paper has positive main Results under the current Contract.
- Cannot say: the historical MD-DQN checkpoint is a fair formal RL baseline without Dr Sun approval.
