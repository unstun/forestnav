---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: knn_k_sweep_candidate_analysis
---

# T14 KNN k Sweep Candidate Analysis

## Plain Conclusion

Increasing KNN candidate count is the first single-variable change that pushes the Extreme speed gate over the approved 50% threshold in the two-method diagnostic sweep. k=20 is the best current candidate: it raises Extreme median time reduction from 42.2% at k=5 to 91.0%, raises Extreme F-N3P feasible rate from 90% to 98%, and cuts F2/F3 fallback rates from 46%/9% at k=10 to 21%/2%. This is still not a formal T14 pass because the sweep only runs F-N3P and vanilla HA*, and T06 remains `reviewed:false`.

## Bucket Summary

| k | bucket | methods | reduction | F-N3P median t | vanilla median t | F-N3P feasible | fallback F2 | fallback F3 | collisions |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | Easy | 6 | 0.9122 | 0.0169 | 0.1920 | 0.9800 | 0.3400 | 0.0400 | 0 |
| 5 | Complex | 6 | 0.9081 | 0.0291 | 0.3166 | 0.9500 | 0.4400 | 0.0600 | 0 |
| 5 | Extreme | 6 | 0.4222 | 0.1834 | 0.3174 | 0.9000 | 0.6000 | 0.1300 | 0 |
| 10 | Easy | 2 | 0.9413 | 0.0112 | 0.1905 | 1.0000 | 0.1800 | 0.0200 | 0 |
| 10 | Complex | 2 | 0.9147 | 0.0258 | 0.3024 | 0.9700 | 0.3000 | 0.0300 | 0 |
| 10 | Extreme | 2 | 0.8747 | 0.0388 | 0.3097 | 0.9300 | 0.4600 | 0.0900 | 0 |
| 20 | Easy | 2 | 0.9411 | 0.0112 | 0.1905 | 1.0000 | 0.0800 | 0.0100 | 0 |
| 20 | Complex | 2 | 0.9194 | 0.0245 | 0.3035 | 0.9900 | 0.1900 | 0.0200 | 0 |
| 20 | Extreme | 2 | 0.9103 | 0.0278 | 0.3095 | 0.9800 | 0.2100 | 0.0200 | 0 |
| 40 | Easy | 2 | 0.9388 | 0.0116 | 0.1902 | 1.0000 | 0.0400 | 0.0100 | 0 |
| 40 | Complex | 2 | 0.9260 | 0.0225 | 0.3041 | 1.0000 | 0.1000 | 0.0000 | 0 |
| 40 | Extreme | 2 | 0.9102 | 0.0278 | 0.3095 | 0.9800 | 0.1300 | 0.0300 | 0 |

## Extreme Long-distance Check

| k | distance bin | n | paired reduction | F-N3P feasible | vanilla feasible | F3 count | F-N3P median t | vanilla median t |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 5 | d08_12 | 25 | 0.8362 | 24 | 23 | 1 | 0.1614 | 0.2621 |
| 5 | d12_16 | 25 | 0.9096 | 24 | 23 | 1 | 0.0206 | 0.2463 |
| 5 | d16_20 | 25 | 0.6113 | 22 | 20 | 5 | 0.1874 | 0.2999 |
| 5 | d20_inf | 25 | 0.0766 | 20 | 17 | 6 | 0.3625 | 0.7364 |
| 10 | d08_12 | 25 | 0.9278 | 24 | 23 | 1 | 0.0212 | 0.2604 |
| 10 | d12_16 | 25 | 0.9231 | 24 | 23 | 2 | 0.0200 | 0.2401 |
| 10 | d16_20 | 25 | 0.8768 | 22 | 20 | 3 | 0.0288 | 0.2972 |
| 10 | d20_inf | 25 | 0.5715 | 23 | 17 | 3 | 0.2242 | 0.7000 |
| 20 | d08_12 | 25 | 0.9322 | 25 | 23 | 0 | 0.0208 | 0.2617 |
| 20 | d12_16 | 25 | 0.9213 | 25 | 23 | 0 | 0.0209 | 0.2387 |
| 20 | d16_20 | 25 | 0.9257 | 25 | 20 | 0 | 0.0285 | 0.2983 |
| 20 | d20_inf | 25 | 0.9103 | 23 | 17 | 2 | 0.0381 | 0.7028 |
| 40 | d08_12 | 25 | 0.9416 | 25 | 23 | 0 | 0.0208 | 0.2591 |
| 40 | d12_16 | 25 | 0.9321 | 25 | 23 | 1 | 0.0207 | 0.2384 |
| 40 | d16_20 | 25 | 0.9285 | 25 | 20 | 0 | 0.0290 | 0.2988 |
| 40 | d20_inf | 25 | 0.9184 | 23 | 17 | 2 | 0.0385 | 0.7025 |

## Interpretation

The k sweep supports the hypothesis that the k=5 failure was mostly neighbor-selection limited: many Extreme queries entered F2 after the first five neighbors failed RS feasibility, while larger k found a valid RS-verifiable subgoal before paying the F2/F3 planning cost.

## Claim Boundary

- Can say: k=20 is a strong candidate for the next full 6-method rerun.
- Cannot say: T14 is complete; this sweep excludes four official methods and T06 remains unreviewed.
- Cannot say: k=20 is paper-final without Dr Sun review of D-T14-05/D-T14-06.
