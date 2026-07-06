# Module2 Encoder Pilot Summary

**Scope notice:** pilot results, NOT formal, unlock no paper claims.

This report summarizes the authorized module2 encoder pilot R1-R6 under `.pipeline/contracts/module2-encoder-pilot-v3.md`. These are pilot selection results only. They do not authorize paper-result claims, paper tables, or a formal-result narrative.

## Decision

The pre-registered decision rule selects **R3 (patch_cnn + no warm-start + sparse reward)** because it is the only run at or above the `0.80` success threshold: `52/64` terminal-RS successes, success rate `81.25%`.

Decision-rule action: freeze the R3 config into a later v3 contract and run the formal attempt separately with formal seed `20260706`, fresh directory, and full provenance. The pilot seed used here was `20260707`.

## Comparison

| Run | Variant | Terminal-RS success | Success rate | Collision rate | Truncation rate | Gate decision | Decision band |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | summary + BC warm-start + sparse reward | 48/64 | 75.00% | 18.75% | 6.25% | fail | mid_band_not_above_R1 |
| R2 | summary + BC warm-start + dense reward | 40/64 | 62.50% | 20.31% | 17.19% | fail | stop_reframe_band |
| R3 | patch_cnn + no warm-start + sparse reward | 52/64 | 81.25% | 14.06% | 4.69% | pass | freeze_config_into_v3_contract |
| R4 | patch_cnn + no warm-start + dense reward | 45/64 | 70.31% | 14.06% | 15.62% | fail | mid_band_not_above_R1 |
| R5 | transformer + no warm-start + dense reward | 24/64 | 37.50% | 46.88% | 15.62% | fail | stop_reframe_band |
| R6 | transformer + no warm-start + sparse reward | 26/64 | 40.62% | 32.81% | 26.56% | fail | stop_reframe_band |

## Stage Breakdown

| Run | Stage | Episodes | Terminal-RS success | Success rate | Collision | Truncated |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | open_connector | 15 | 15/15 | 100.00% | 0 | 0 |
| R1 | obstacle_bypass | 13 | 7/13 | 53.85% | 6 | 0 |
| R1 | rs_failure_node | 23 | 19/23 | 82.61% | 3 | 1 |
| R1 | heldout_procedural | 13 | 7/13 | 53.85% | 3 | 3 |
| R2 | open_connector | 15 | 15/15 | 100.00% | 0 | 0 |
| R2 | obstacle_bypass | 13 | 7/13 | 53.85% | 6 | 0 |
| R2 | rs_failure_node | 23 | 14/23 | 60.87% | 3 | 6 |
| R2 | heldout_procedural | 13 | 4/13 | 30.77% | 4 | 5 |
| R3 | open_connector | 15 | 15/15 | 100.00% | 0 | 0 |
| R3 | obstacle_bypass | 13 | 7/13 | 53.85% | 6 | 0 |
| R3 | rs_failure_node | 23 | 20/23 | 86.96% | 1 | 2 |
| R3 | heldout_procedural | 13 | 10/13 | 76.92% | 2 | 1 |
| R4 | open_connector | 15 | 15/15 | 100.00% | 0 | 0 |
| R4 | obstacle_bypass | 13 | 7/13 | 53.85% | 6 | 0 |
| R4 | rs_failure_node | 23 | 18/23 | 78.26% | 1 | 4 |
| R4 | heldout_procedural | 13 | 5/13 | 38.46% | 2 | 6 |
| R5 | open_connector | 15 | 15/15 | 100.00% | 0 | 0 |
| R5 | obstacle_bypass | 13 | 0/13 | 0.00% | 13 | 0 |
| R5 | rs_failure_node | 23 | 7/23 | 30.43% | 11 | 5 |
| R5 | heldout_procedural | 13 | 2/13 | 15.38% | 6 | 5 |
| R6 | open_connector | 15 | 15/15 | 100.00% | 0 | 0 |
| R6 | obstacle_bypass | 13 | 7/13 | 53.85% | 6 | 0 |
| R6 | rs_failure_node | 23 | 2/23 | 8.70% | 9 | 12 |
| R6 | heldout_procedural | 13 | 2/13 | 15.38% | 6 | 5 |

## Traceability

| Run | Source head | Execution host | Model sha256 | Checkpoint count | Train real_s | Eval real_s |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | 09259640169962f54af37bfa0cac9bd0b57d7270 | ubuntu-OMEN-by-HP-Laptop-17-ck1xxx | 0af81966effd32d0... | 11 | 2228.35 | 52.20 |
| R2 | 09259640169962f54af37bfa0cac9bd0b57d7270 | ubuntu-OMEN-by-HP-Laptop-17-ck1xxx | 7c71e45c7f2ccfbe... | 11 | 2220.85 | 52.45 |
| R3 | 09259640169962f54af37bfa0cac9bd0b57d7270 | ubuntu-OMEN-by-HP-Laptop-17-ck1xxx | 97abcf8fd28beeb5... | 11 | 2090.12 | 49.82 |
| R4 | 09259640169962f54af37bfa0cac9bd0b57d7270 | ubuntu-OMEN-by-HP-Laptop-17-ck1xxx | 6fbd00117c290023... | 11 | 2053.40 | 49.65 |
| R5 | 09259640169962f54af37bfa0cac9bd0b57d7270 | ubuntu-OMEN-by-HP-Laptop-17-ck1xxx | 8fa28a42ad42b405... | 11 | 2392.59 | 52.92 |
| R6 | 09259640169962f54af37bfa0cac9bd0b57d7270 | ubuntu-OMEN-by-HP-Laptop-17-ck1xxx | 4708b7c088b0785d... | 11 | 2425.94 | 47.57 |

## Artifact Pointers

- Machine-readable summary: `0_trials/module2_encoder_pilot/pilot_summary.csv`
- Driver log: `0_trials/module2_encoder_pilot/d7_driver.log`
- Per-run training manifests: `0_trials/module2_encoder_pilot/R*/train/training_manifest.json`
- Per-run train summaries: `0_trials/module2_encoder_pilot/R*/train/summary.json`
- Per-run eval summaries: `0_trials/module2_encoder_pilot/R*/eval/gate3_summary.json`
- Per-run episode CSVs: `0_trials/module2_encoder_pilot/R*/eval/gate3_eval_episodes.csv`
