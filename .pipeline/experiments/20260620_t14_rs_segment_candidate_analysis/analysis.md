---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: rs_verified_segment_candidate_smoke
---

# T14 RS-verified Segment Candidate Smoke Analysis

## Plain Conclusion

The optional `commit_verified_rs_segments` branch is a promising speed candidate on this paired 15-query smoke. For F-N3P: Easy: median delta -0.1075s, median speedup 16.80x, feasible 5->5, collisions 0->0; Complex: median delta -0.1641s, median speedup 17.99x, feasible 5->5, collisions 0->0; Extreme: median delta -0.2099s, median speedup 18.38x, feasible 5->5, collisions 0->0.

This is not a formal T14 result: it uses 5 queries per bucket and unreviewed T06 cutpoints, and it does not include MD-DQN. It only tests whether the RS-verified segment commit branch is worth a formal rerun after Dr Sun review.

## Source Artifacts

- control smoke: `.pipeline/experiments/20260620_t14_planner_segment_control_smoke`
- candidate smoke: `.pipeline/experiments/20260620_t14_rs_segment_candidate_smoke`
- paired table: `paired_control_vs_rs_candidate.csv`
- summary table: `summary_control_vs_rs_candidate.csv`

## Summary

| method | bucket | n | faster | slower | median delta cand-control (s) | median speedup | feasible control->candidate | collisions control->candidate |
|---|---|---:|---:|---:|---:|---:|---|---|
| f_n3p_knn | Easy | 5 | 5 | 0 | -0.1075 | 16.80 | 5->5 | 0->0 |
| f_n3p_knn | Complex | 5 | 5 | 0 | -0.1641 | 17.99 | 5->5 | 0->0 |
| f_n3p_knn | Extreme | 5 | 5 | 0 | -0.2099 | 18.38 | 5->5 | 0->0 |
| n3p_k1 | Easy | 5 | 2 | 3 | 0.0016 | 1.00 | 4->4 | 0->0 |
| n3p_k1 | Complex | 5 | 3 | 2 | -0.0000 | 1.00 | 5->5 | 0->0 |
| n3p_k1 | Extreme | 5 | 3 | 2 | -0.0004 | 1.00 | 5->5 | 0->0 |
| vanilla_ha | Easy | 5 | 1 | 4 | 0.0021 | 0.99 | 4->4 | 0->0 |
| vanilla_ha | Complex | 5 | 2 | 3 | 0.0021 | 0.99 | 5->5 | 0->0 |
| vanilla_ha | Extreme | 5 | 3 | 2 | -0.0006 | 1.00 | 5->5 | 0->0 |

## Claim Boundary

- Can say: the branch is executable, traceable via `run_config.json`, and improves this paired smoke without adding collisions.
- Cannot say: T14 is complete or formally accepted.
- Cannot say: this replaces the approved method without Dr Sun review; it is a candidate for method redesign or a Contract v2 discussion.
