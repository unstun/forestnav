# Module2 Planner-Integration Diagnostic Probe Protocol

Status line: diagnostic, non-formal, no paper claims

## Scope Lock

Approved personally by Dr Sun on 2026-07-07. This is a DIAGNOSTIC probe: it
uses the Gate3-FAILED checkpoint
`0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip` as a
probe instrument. Nothing produced here is formal evidence or paper material.

No training is permitted. Inference/planning only.

## Method List

- M1 vanilla HA* (analytic operator single_rs).
- M2 Dang multi-curvature RS (dang_multi_rs).
- M3 HA* + RL-RS funnel operator (ha_rl_rs_ppo, checkpoint above,
  deterministic policy).

Execution mapping to the existing harness:

- M1 uses existing method `ha_single_rs`, the vanilla Hybrid A* planner with
  analytic operator `single_rs`.
- M2 uses existing method `ha_dang_multi_rs`, the Hybrid A* planner with
  analytic operator `dang_multi_rs`.
- M3 uses existing method `ha_rl_rs_ppo`, the Hybrid A* planner with the
  checkpoint-backed RL-RS funnel operator and terminal RS cleanup enabled.

## Query Protocol

Reuse the existing main-evaluation query generation
(`build_query_set` / `validation_t06` cutpoints) to produce 40 Complex and
40 Extreme held-out queries with fixed probe seed 20260710, disjoint from any
training/curriculum data. Record the query manifest (query ids, map seeds,
profile names) in this probe directory.

All three methods run on the same 80 queries, one run per method per query,
using the same timeout and timing protocol as the existing evaluation
framework. Timing includes NN forward, rollout, collision checks, and any
fallback-to-primitives cost; no hidden costs are excluded.

Execution host: gpu3070ti-relay, same host class as prior timing evidence.
Before running, verify remote git HEAD equals local HEAD.

## Metrics

Per bucket (Complex / Extreme) x method:

- success rate;
- timeout rate;
- median and p95 node expansions;
- median and p95 end-to-end planning time;
- path length inflation;
- collision violations, which must be 0;
- for M3, in-planner RL attempt count, RL attempt success rate,
  mean NN forward time per query, and fallback counts.

Paired per-query comparisons:

- M3 vs M1 expansions ratio;
- M3 vs M1 time ratio.

Required A02.3 telemetry columns in `records.csv`:

- `rl_attempts`;
- `rl_successes`;
- `rs_attempts`;
- `nn_forward_time_s`;
- `fallback_to_primitives_count`;
- `analytic_attempts`.

## Pre-Registered Signal Bands

- strong_signal: on Extreme, M3 vs M1 success rate +>=10pp AND median
  end-to-end time <= 110% of M1;
- weak_signal: median node expansions <= 70% of M1 but time > 110%;
- no_signal: neither.

The band verdict is computed mechanically from the Extreme-bucket result.

## Frozen Run Parameters

- Checkpoint: `0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip`
- Checkpoint SHA256: `ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2`
- Query seed: `20260710`
- Query buckets: `Complex`, `Extreme`
- Queries per bucket: `40`
- Density profile buckets: `validation_t06`
- Distance bins: existing `run_main_evaluation` default
  `8:12,12:16,16:20,20:`
- Methods: `ha_single_rs`, `ha_dang_multi_rs`, `ha_rl_rs_ppo`
- Device for M3 checkpoint inference: `cuda`
- RL-RS observation patch: existing defaults, `6.4m`, `64` cells, EDT enabled,
  EDT clip `2.0m`
- RL-RS rollout: existing defaults, max steps `32`, action step `0.3m`,
  collision sample step `0.1m`, terminal check every `1`, no-progress patience
  `3`
- Timing/timeout/node protocol: existing `MainEvaluationConfig` defaults,
  teacher timeout `2.5s`, teacher max nodes `15000`
- Bootstrap resamples for run artifacts: `5000`

## Progress

### D1 workspace and checkpoint verification

Command:

```text
git status --short
```

Output:

```text

```

Command:

```text
git rev-parse HEAD
```

Output:

```text
95a6e80a0e8388414b5c712fe6e610e061cb247b
```

Command:

```text
ls -l 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip
```

Output:

```text
-rw-r--r--@ 1 sun  staff  15183390 Jul  7 06:04 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip
```

Command:

```text
ls -l 0_trials/module2_gate3_formal_v3/seed20260709/gate3_trial_manifest.json
```

Output:

```text
-rw-r--r--@ 1 sun  staff  7822 Jul  7 05:41 0_trials/module2_gate3_formal_v3/seed20260709/gate3_trial_manifest.json
```

Command:

```text
shasum -a 256 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip
```

Output:

```text
ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2  0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip
```

Command:

```text
cat 0_trials/module2_gate3_formal_v3/seed20260709/checkpoint_sha256.csv
```

Output:

```text
path,size_bytes,sha256
train/final_model.zip,15183390,ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2
train/rl_rs_ppo_100000_steps.zip,15183394,0d3e152a897201fa2bd210874faf25854c4d47b616f37583a3482813f2d2232f
train/rl_rs_ppo_150000_steps.zip,15183180,b74976bb194681bd183c8bfe0ddc9de3f50323bad9c731d553ab0f1165db99a5
train/rl_rs_ppo_200000_steps.zip,15183203,5fb12b62709013da8706386fe39f613f8a40772dc16a0c1d92b04f2385f6ba84
train/rl_rs_ppo_250000_steps.zip,15183254,5ab1cd8719d3ed78c2fa87eebbaf189fa0bad89c14e4781ae8a2e51b0841a605
train/rl_rs_ppo_300000_steps.zip,15183371,c5e2da16f2e6e6d9bd0d9c041f3d3228bef89590f0f39d9af1fcdb87b0f2ca0d
train/rl_rs_ppo_350000_steps.zip,15183434,7b12cef7607b4c07c4e929094ab45137c9ec4993d90734b739d7e438b17e61b1
train/rl_rs_ppo_400000_steps.zip,15183393,c59c0ac4f639b213d7aa3259d7966b032ecbaf101e50c0cbcab07d6886b12026
train/rl_rs_ppo_450000_steps.zip,15183254,2f26ae20a8631238f703c67c404fe98ff16c951181d93524999f3b0f606554ec
train/rl_rs_ppo_500000_steps.zip,15183270,709a781dbe196a79149ae7d77ecb4d075964cff89b340206cdcc7ce403dae237
train/rl_rs_ppo_50000_steps.zip,15183237,f26b64885074d3d070a4e355c13172c1d223b4c113f525db80e81f8894e1d7bf
```

### D2 protocol commit

Command:

```text
git commit -m "Record module2 planner probe protocol"
```

Output:

```text
[main 4ae3cee9] Record module2 planner probe protocol
 1 file changed, 188 insertions(+)
 create mode 100644 0_trials/module2_planner_probe/probe_protocol.md
```

Command:

```text
git rev-parse HEAD
```

Output:

```text
4ae3cee9ac073b30909455d900b2329d2c886ee8
```

### D3 query manifest generation

Command:

```text
PYTHONPATH=2_experiment python3 - <<'PY'
import csv
import json
from dataclasses import asdict
from pathlib import Path

from forest_n3p.main_evaluation import MainEvaluationConfig, build_query_set, validation_main_evaluation_profiles

out_dir = Path('0_trials/module2_planner_probe')
out_dir.mkdir(parents=True, exist_ok=True)
config = MainEvaluationConfig(
    seed=20260710,
    queries_per_bucket=40,
    seed_count=5,
    queries_per_map=5,
    profiles=validation_main_evaluation_profiles(),
    methods=('ha_single_rs', 'ha_dang_multi_rs', 'ha_rl_rs_ppo'),
    module2_rl_rs_checkpoint=Path('0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip'),
    module2_rl_rs_device='cuda',
)
all_queries = build_query_set(config)
queries = [q for q in all_queries if q.difficulty_bucket in {'Complex', 'Extreme'}]
if len(queries) != 80:
    raise SystemExit(f'expected 80 Complex/Extreme queries, got {len(queries)}')
counts = {}
for q in queries:
    counts[q.difficulty_bucket] = counts.get(q.difficulty_bucket, 0) + 1
if counts != {'Complex': 40, 'Extreme': 40}:
    raise SystemExit(f'unexpected bucket counts: {counts}')
fieldnames = list(asdict(queries[0]).keys())
manifest_csv = out_dir / 'query_manifest.csv'
with manifest_csv.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    for q in queries:
        writer.writerow(asdict(q))
manifest_json = out_dir / 'query_manifest.json'
payload = {
    'schema_version': 1,
    'status': 'diagnostic_non_formal_query_manifest',
    'source': 'forest_n3p.main_evaluation.build_query_set with validation_main_evaluation_profiles, filtered to Complex/Extreme',
    'seed': 20260710,
    'queries_per_bucket': 40,
    'seed_count': 5,
    'queries_per_map': 5,
    'bucket_counts': counts,
    'query_count': len(queries),
    'method_order': ['ha_single_rs', 'ha_dang_multi_rs', 'ha_rl_rs_ppo'],
    'queries_csv': str(manifest_csv),
    'queries': [asdict(q) for q in queries],
}
manifest_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({
    'query_count': len(queries),
    'bucket_counts': counts,
    'first_query': asdict(queries[0]),
    'last_query': asdict(queries[-1]),
    'csv': str(manifest_csv),
    'json': str(manifest_json),
}, indent=2, ensure_ascii=False))
PY
```

Output:

```text
{
  "query_count": 80,
  "bucket_counts": {
    "Complex": 40,
    "Extreme": 40
  },
  "first_query": {
    "query_id": "complex_s00_q0000",
    "difficulty_bucket": "Complex",
    "profile_name": "complex_d02",
    "map_seed": 20360710,
    "query_seed": 20361710,
    "seed_index": 0,
    "map_index": 0,
    "query_index": 0,
    "distance_bin_key": "d08_12",
    "start": [
      15.4,
      14.4,
      0.47177751118075006
    ],
    "goal": [
      25.200000000000003,
      19.400000000000002,
      0.47177751118075006
    ]
  },
  "last_query": {
    "query_id": "extreme_s04_q0039",
    "difficulty_bucket": "Extreme",
    "profile_name": "extreme_d05",
    "map_seed": 20500711,
    "query_seed": 20501713,
    "seed_index": 4,
    "map_index": 1,
    "query_index": 2,
    "distance_bin_key": "d20_inf",
    "start": [
      18.400000000000002,
      29.0,
      -2.2655346029916
    ],
    "goal": [
      4.4,
      12.200000000000001,
      -2.2655346029916
    ]
  },
  "csv": "0_trials/module2_planner_probe/query_manifest.csv",
  "json": "0_trials/module2_planner_probe/query_manifest.json"
}
```

Command:

```text
wc -l 0_trials/module2_planner_probe/query_manifest.csv
```

Output:

```text
      81 0_trials/module2_planner_probe/query_manifest.csv
```

Command:

```text
PYTHONPATH=2_experiment python3 - <<'PY'
import csv, json
from pathlib import Path
path = Path('0_trials/module2_planner_probe/query_manifest.csv')
rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
counts = {}
for row in rows:
    counts[row['difficulty_bucket']] = counts.get(row['difficulty_bucket'], 0) + 1
print(json.dumps({'rows': len(rows), 'bucket_counts': counts, 'has_easy': 'Easy' in counts}, indent=2))
PY
```

Output:

```text
{
  "rows": 80,
  "bucket_counts": {
    "Complex": 40,
    "Extreme": 40
  },
  "has_easy": false
}
```

### D4 remote HEAD and preflight verification

Command:

```text
git push origin main
```

Output:

```text
To https://github.com/unstun/forestnav.git
   95a6e80a..f2043f60  main -> main
```

Command:

```text
ssh -o BatchMode=yes -o ConnectTimeout=20 gpu3070ti-relay 'export PATH=/home/ubuntu/.local/git-user/root/usr/bin:$PATH; export GIT_EXEC_PATH=/home/ubuntu/.local/git-user/root/usr/lib/git-core; cd /home/ubuntu/ForestNav && git pull --ff-only origin main && printf "HEAD=" && git rev-parse HEAD && printf "STATUS_START\n" && git status --short && printf "STATUS_END\n"'
```

Output excerpt:

```text
Updating b4b73606..f2043f60
Fast-forward
HEAD=f2043f60b0c46bea3d90ac27b0afc59e7af80ffa
STATUS_START
STATUS_END
```

Command:

```text
ssh -o BatchMode=yes -o ConnectTimeout=20 gpu3070ti-relay 'cd /home/ubuntu/ForestNav && PYTHONPATH=2_experiment python3 -m forest_n3p.scripts.run_main_evaluation --output-dir 0_trials/module2_planner_probe/preflight_check --preflight-only --methods ha_single_rs,ha_dang_multi_rs,ha_rl_rs_ppo --module2-rl-rs-checkpoint 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip --module2-rl-rs-device cuda --queries-per-bucket 40 --seed-count 5 --queries-per-map 5 --seed 20260710 --density-profile-buckets validation_t06 --allow-unresolved-human-review --no-enforce-t14-scale'
```

Output:

```text
{
  "ok_to_run": true,
  "blocking_issues": [],
  "warnings": [
    "T14 formal scale is not satisfied: queries_per_bucket=40, seed_count=5"
  ],
  "available_methods": [
    "ha_single_rs",
    "ha_dang_multi_rs",
    "ha_rl_rs_ppo"
  ],
  "unavailable_methods": {},
  "cutpoint_supplement_reviewed": true,
  "human_review_satisfied": true,
  "human_review_decisions": {
    "D-T14-09": "revise_to_validation_cutpoints",
    "D-T14-10": "approve",
    "D-T14-11": "formal_baseline",
    "D-T14-12": "approve_after_rerun_passes"
  },
  "profile_bucket_satisfied": true,
  "profile_bucket_issues": [],
  "t14_scale_satisfied": false
}
```

### D4 method runs

Initial runner guard attempts stopped before producing any query result rows:

```text
preflight failed: T14 formal scale is not satisfied: queries_per_bucket=40, seed_count=5
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
remote worktree is dirty before M2: ?? 0_trials/module2_planner_probe/M1/
```

The final method runner kept the frozen query/method protocol, set the
non-formal preflight flags, parsed tuple-form poses with `ast.literal_eval`,
and allowed existing probe artifacts under `0_trials/module2_planner_probe/`.

M1 output:

```text
{
  "event": "first10_projection",
  "method_label": "M1",
  "elapsed_first10_s": 12.289196567959152,
  "projected_total_probe_wall_clock_s": 294.94071763101965,
  "hard_cap_s": 21600,
  "decision": "continue"
}
{
  "event": "method_complete",
  "method_label": "M1",
  "method": "ha_single_rs",
  "record_count": 80,
  "elapsed_s": 117.7670694119297,
  "records_csv": "0_trials/module2_planner_probe/M1/records.csv",
  "summary_csv": "0_trials/module2_planner_probe/M1/summary_by_method_bucket.csv"
}
```

M2 output:

```text
{
  "event": "first10_projection",
  "method_label": "M2",
  "elapsed_first10_s": 12.209671729011461,
  "projected_total_probe_wall_clock_s": 313.1218170761131,
  "hard_cap_s": 21600,
  "decision": "continue"
}
{
  "event": "method_complete",
  "method_label": "M2",
  "method": "ha_dang_multi_rs",
  "record_count": 80,
  "elapsed_s": 110.61274681705981,
  "records_csv": "0_trials/module2_planner_probe/M2/records.csv",
  "summary_csv": "0_trials/module2_planner_probe/M2/summary_by_method_bucket.csv"
}
```

M3 output:

```text
{
  "event": "first10_projection",
  "method_label": "M3",
  "elapsed_first10_s": 3.0660314100096002,
  "projected_total_probe_wall_clock_s": 252.9080675090663,
  "hard_cap_s": 21600,
  "decision": "continue"
}
{
  "event": "method_complete",
  "method_label": "M3",
  "method": "ha_rl_rs_ppo",
  "record_count": 80,
  "elapsed_s": 27.378519446006976,
  "records_csv": "0_trials/module2_planner_probe/M3/records.csv",
  "summary_csv": "0_trials/module2_planner_probe/M3/summary_by_method_bucket.csv"
}
```

Artifact row-count and summary check:

```text
===M1===
81 0_trials/module2_planner_probe/M1/records.csv
method,difficulty_bucket,count,success_count,success_rate,feasible_count,feasible_rate,median_time_s,p95_time_s,min_time_s,mean_time_s,median_expansions,p95_expansions,median_path_inflation_ratio,p95_path_inflation_ratio,mean_direction_switches,median_min_clearance_m,collision_violation_total,timeout_failure_count,timeout_failure_rate,mean_nn_forward_time_s,p95_nn_forward_time_s,rl_attempts_total,rl_successes_total,rs_attempts_total,fallback_to_primitives_total,fallback_trigger_rate,fallback_f1_rate,fallback_f2_rate,fallback_f3_rate,subgoal_reachability_rate
ha_single_rs,Complex,40,27,0.675,27,0.675,0.5061970949172974,2.500512087345123,0.14861249923706055,1.1294766902923583,737.5,6537.9,,,0.075,0.07471674501239656,0,13,0.325,,,0,0,15895,15868,0.0,0.0,0.0,0.0,
ha_single_rs,Extreme,40,29,0.725,29,0.725,0.5843369960784912,2.5004774808883665,0.14948225021362305,1.1290342509746552,870.0,6195.599999999997,,,0.05,0.0740610045356227,0,11,0.275,,,0,0,15040,15011,0.0,0.0,0.0,0.0,
===M2===
81 0_trials/module2_planner_probe/M2/records.csv
method,difficulty_bucket,count,success_count,success_rate,feasible_count,feasible_rate,median_time_s,p95_time_s,min_time_s,mean_time_s,median_expansions,p95_expansions,median_path_inflation_ratio,p95_path_inflation_ratio,mean_direction_switches,median_min_clearance_m,collision_violation_total,timeout_failure_count,timeout_failure_rate,mean_nn_forward_time_s,p95_nn_forward_time_s,rl_attempts_total,rl_successes_total,rs_attempts_total,fallback_to_primitives_total,fallback_trigger_rate,fallback_f1_rate,fallback_f2_rate,fallback_f3_rate,subgoal_reachability_rate
ha_dang_multi_rs,Complex,40,30,0.75,30,0.75,0.3686326742172241,2.5014402508735656,0.14766359329223633,1.0043807864189147,355.5,3977.4,0.0008847975238512884,0.010603501449517981,0.225,0.07612920516718086,0,10,0.25,,,0,0,94622,8572,0.0,0.0,0.0,0.0,
ha_dang_multi_rs,Extreme,40,27,0.675,27,0.675,0.49147212505340576,2.5012007355690002,0.14449572563171387,1.1186229050159455,562.5,4613.249999999997,0.0021408187306177773,0.0130081350906569,0.05,0.07392835269278875,0,13,0.325,,,0,0,113421,10284,0.0,0.0,0.0,0.0,
===M3===
81 0_trials/module2_planner_probe/M3/records.csv
method,difficulty_bucket,count,success_count,success_rate,feasible_count,feasible_rate,median_time_s,p95_time_s,min_time_s,mean_time_s,median_expansions,p95_expansions,median_path_inflation_ratio,p95_path_inflation_ratio,mean_direction_switches,median_min_clearance_m,collision_violation_total,timeout_failure_count,timeout_failure_rate,mean_nn_forward_time_s,p95_nn_forward_time_s,rl_attempts_total,rl_successes_total,rs_attempts_total,fallback_to_primitives_total,fallback_trigger_rate,fallback_f1_rate,fallback_f2_rate,fallback_f3_rate,subgoal_reachability_rate
ha_rl_rs_ppo,Complex,40,0,0.0,0,0.0,7.185591232031584,10.730790820019319,0.3090991040226072,5.927807051729178,0.0,0.0,,,0.0,,0,0,0.0,,,0,0,0,0,0.0,0.0,0.0,0.0,
ha_rl_rs_ppo,Extreme,40,0,0.0,0,0.0,20.34174762101611,27.373118291120043,11.613336240989156,20.071489422384182,0.0,0.0,,,0.0,,0,0,0.0,,,0,0,0,0,0.0,0.0,0.0,0.0,
```

Failure-reason check:

```text
{
  "label": "M1",
  "rows": 80,
  "failure_reasons": {
    "": 56,
    "timeout": 24
  }
}
{
  "label": "M2",
  "rows": 80,
  "failure_reasons": {
    "": 57,
    "timeout": 23
  }
}
{
  "label": "M3",
  "rows": 80,
  "failure_reasons": {
    "m3_exception:ModuleNotFoundError": 80
  }
}
```

### D5 probe summary generation

Command:

```text
PYTHONPATH=2_experiment python3 - <<'PY'
# Aggregate M1/M2/M3 records into probe_summary.md, probe_summary.csv,
# paired_m3_vs_m1.csv, and probe_band_verdict.json.
PY
```

Output:

```text
{
  "reported_band": "no_signal",
  "raw_numeric_band": "weak_signal",
  "success_delta_pp_m3_minus_m1_extreme": -72.5,
  "time_ratio_m3_over_m1_extreme": 34.811671616773175,
  "expansions_ratio_m3_over_m1_extreme": 0.0,
  "m3_exception_count": 80,
  "probe_summary_md": "0_trials/module2_planner_probe/probe_summary.md",
  "probe_summary_csv": "0_trials/module2_planner_probe/probe_summary.csv",
  "paired_csv": "0_trials/module2_planner_probe/paired_m3_vs_m1.csv"
}
```

Artifact/schema verification command:

```text
PYTHONPATH=2_experiment python3 - <<'PY'
# Check 80 records per method, two summary rows per method, required A02.3
# telemetry columns, zero collision violations, summary files, and band JSON.
PY
```

Output:

```text
{
  "M1": {
    "collision_violation_total": 0,
    "failure_reasons": {
      "": 56,
      "timeout": 24
    },
    "missing_record_cols": [],
    "missing_summary_cols": [],
    "records_rows": 80,
    "summary_rows": 2
  },
  "M2": {
    "collision_violation_total": 0,
    "failure_reasons": {
      "": 57,
      "timeout": 23
    },
    "missing_record_cols": [],
    "missing_summary_cols": [],
    "records_rows": 80,
    "summary_rows": 2
  },
  "M3": {
    "collision_violation_total": 0,
    "failure_reasons": {
      "m3_exception:ModuleNotFoundError": 80
    },
    "missing_record_cols": [],
    "missing_summary_cols": [],
    "records_rows": 80,
    "summary_rows": 2
  },
  "paired_m3_vs_m1.csv": {
    "bytes": 11478,
    "exists": true
  },
  "probe_band_verdict.json": {
    "bytes": 467,
    "exists": true
  },
  "probe_summary.csv": {
    "bytes": 1577,
    "exists": true
  },
  "probe_summary.md": {
    "bytes": 3224,
    "exists": true
  },
  "verdict": {
    "expansions_ratio_m3_over_m1_extreme": 0.0,
    "m3_exception_count": 80,
    "paired_csv": "0_trials/module2_planner_probe/paired_m3_vs_m1.csv",
    "probe_summary_csv": "0_trials/module2_planner_probe/probe_summary.csv",
    "probe_summary_md": "0_trials/module2_planner_probe/probe_summary.md",
    "raw_numeric_band": "weak_signal",
    "reported_band": "no_signal",
    "success_delta_pp_m3_minus_m1_extreme": -72.5,
    "time_ratio_m3_over_m1_extreme": 34.811671616773175
  }
}
```
