---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: rs_verified_fullscale_candidate_comparison
---

# T14 RS-verified Segment Fullscale Candidate Comparison

## Plain Conclusion

The RS-verified segment candidate materially fixes the main T14 speed failure in Complex, but it still does not satisfy the approved Contract in Extreme. The new run is complete at T14 scale with 300 queries, 1800 records, 6 methods, 0 method exceptions, and 0 collision violations. It remains a candidate, not a completed T14 result, because the T06 cutpoint supplement is still `reviewed:false` and Extreme median time reduction is 42.2%, below the required 50%.

## Contract Gate Delta

| bucket | old reduction | new reduction | delta pp | gap to 50% pp | new status | success drop pp | path inflation |
|---|---:|---:|---:|---:|---|---:|---:|
| Complex | -0.2993 | 0.9081 | 120.7 | 0.0 | pass | -12.0 | 0.0000 |
| Extreme | -0.2621 | 0.4222 | 68.4 | 7.8 | fail | -7.0 | 0.0000 |

## New F-N3P vs Vanilla by Distance Bin

`median reduction` in this table is the median of paired per-query reductions inside each distance bin. The Contract gate above uses the registered bucket-level ratio of median times.

| bucket | distance bin | n | median reduction | F-N3P feasible | vanilla feasible | F3 count | median F-N3P time | median vanilla time |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Easy | d08_12 | 25 | 0.9573 | 25 | 25 | 0 | 0.0100 | 0.1545 |
| Easy | d12_16 | 25 | 0.9229 | 25 | 24 | 0 | 0.0149 | 0.1727 |
| Easy | d16_20 | 25 | 0.9376 | 25 | 23 | 2 | 0.0174 | 0.2126 |
| Easy | d20_inf | 25 | 0.9105 | 23 | 19 | 2 | 0.1787 | 0.3313 |
| Complex | d08_12 | 25 | 0.9631 | 25 | 25 | 1 | 0.0104 | 0.1635 |
| Complex | d12_16 | 25 | 0.7914 | 25 | 23 | 0 | 0.1638 | 0.2261 |
| Complex | d16_20 | 25 | 0.8766 | 21 | 19 | 4 | 0.0287 | 0.3912 |
| Complex | d20_inf | 25 | 0.8843 | 24 | 16 | 1 | 0.1834 | 1.7694 |
| Extreme | d08_12 | 25 | 0.8362 | 24 | 23 | 1 | 0.1614 | 0.2621 |
| Extreme | d12_16 | 25 | 0.9096 | 24 | 23 | 1 | 0.0206 | 0.2463 |
| Extreme | d16_20 | 25 | 0.6113 | 22 | 20 | 5 | 0.1874 | 0.2999 |
| Extreme | d20_inf | 25 | 0.0766 | 20 | 17 | 6 | 0.3625 | 0.7364 |

## Old Candidate vs RS-verified Candidate

| method | bucket | n | new faster | new slower | median delta new-old (s) | feasible old->new | collision old->new | F3 old->new |
|---|---|---:|---:|---:|---:|---|---|---|
| bottleneck_waypoint | Easy | 100 | 70 | 30 | -0.0193 | 99->99 | 0->0 | 0->0 |
| bottleneck_waypoint | Complex | 100 | 48 | 52 | 0.0002 | 100->100 | 0->0 | 0->0 |
| bottleneck_waypoint | Extreme | 100 | 50 | 50 | 0.0003 | 100->99 | 0->0 | 0->0 |
| f_n3p_knn | Easy | 100 | 91 | 9 | -0.1477 | 98->98 | 0->0 | 4->4 |
| f_n3p_knn | Complex | 100 | 83 | 17 | -0.1490 | 95->95 | 0->0 | 6->6 |
| f_n3p_knn | Extreme | 100 | 88 | 12 | -0.1545 | 90->90 | 0->0 | 13->13 |
| md_dqn | Easy | 100 | 86 | 14 | -0.0025 | 0->0 | 0->0 | 0->0 |
| md_dqn | Complex | 100 | 85 | 15 | -0.0017 | 2->2 | 0->0 | 0->0 |
| md_dqn | Extreme | 100 | 89 | 11 | -0.0016 | 1->1 | 0->0 | 0->0 |
| n3p_k1 | Easy | 100 | 85 | 15 | -0.0143 | 96->96 | 0->0 | 8->8 |
| n3p_k1 | Complex | 100 | 73 | 27 | -0.0076 | 90->90 | 0->0 | 13->13 |
| n3p_k1 | Extreme | 100 | 66 | 34 | -0.0258 | 88->88 | 0->0 | 19->19 |
| vanilla_ha | Easy | 100 | 75 | 25 | -0.0055 | 91->91 | 0->0 | 0->0 |
| vanilla_ha | Complex | 100 | 43 | 57 | 0.0004 | 83->83 | 0->0 | 0->0 |
| vanilla_ha | Extreme | 100 | 49 | 51 | 0.0001 | 82->83 | 0->0 | 0->0 |
| voronoi_waypoint | Easy | 100 | 71 | 29 | -0.0222 | 100->100 | 0->0 | 0->0 |
| voronoi_waypoint | Complex | 100 | 45 | 55 | 0.0004 | 99->99 | 0->0 | 0->0 |
| voronoi_waypoint | Extreme | 100 | 50 | 50 | 0.0001 | 99->99 | 0->0 | 0->0 |

## Source Artifacts

- old candidate: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn`
- new RS-verified candidate: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_rs_segments`
- remote logs: `.pipeline/experiments/logs/20260620_t14_candidate_6method_fullscale_rs_segments.{out,err,exit}`
- paired table: `paired_old_candidate_vs_rs_segments.csv`
- contract gate table: `contract_gate_delta.csv`
- distance-bin table: `distance_bin_contract_deltas.csv`

## Claim Boundary

- Can say: the RS-verified candidate is fullscale-complete as a diagnostic rerun and removes the Complex speed failure.
- Can say: Extreme is improved but still fails the approved speed threshold.
- Cannot say: T14 is complete, because formal acceptance is false and T06 remains unreviewed.
- Cannot say: this method change is paper-final without Dr Sun review or a documented method/Contract decision.
