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

### 2026-07-08 D4/D5 M3-only rerun under training venv

Remote git note: `git` is available on gpu3070ti-relay via
`/home/ubuntu/.local/git-user/root/usr/bin/git`. The remote worktree was
fast-forwarded after moving prior untracked probe directories to
`/home/ubuntu/ForestNav_module2_planner_probe_untracked_backup_20260708T073253Z/`.

Command:

```text
git push origin main
```

Output:

```text
To https://github.com/unstun/forestnav.git
   9e4ef60b..0de18b9b  main -> main
```

Remote sync output:

```text
moved 0_trials/module2_planner_probe/M1 -> /home/ubuntu/ForestNav_module2_planner_probe_untracked_backup_20260708T073253Z/0_trials/module2_planner_probe/M1
moved 0_trials/module2_planner_probe/M2 -> /home/ubuntu/ForestNav_module2_planner_probe_untracked_backup_20260708T073253Z/0_trials/module2_planner_probe/M2
moved 0_trials/module2_planner_probe/M3 -> /home/ubuntu/ForestNav_module2_planner_probe_untracked_backup_20260708T073253Z/0_trials/module2_planner_probe/M3
pull_start
From https://github.com/unstun/forestnav
 * branch              main       -> FETCH_HEAD
   f2043f60..0de18b9b  main       -> origin/main
Updating f2043f60..0de18b9b
Fast-forward
pull_end
remote_head=0de18b9b3c73a9407fab57876056b49b35b4f79a
remote_status_start
remote_status_end
```

Command:

```text
LOCAL_HEAD=$(git rev-parse HEAD); ssh -o BatchMode=yes -o ConnectTimeout=20 gpu3070ti-relay "export PATH=/home/ubuntu/.local/git-user/root/usr/bin:\$PATH; export GIT_EXEC_PATH=/home/ubuntu/.local/git-user/root/usr/lib/git-core; cd /home/ubuntu/ForestNav && REMOTE_HEAD=\$(git rev-parse HEAD) && echo local_head=$LOCAL_HEAD && echo remote_head=\$REMOTE_HEAD && test \"\$REMOTE_HEAD\" = \"$LOCAL_HEAD\" && echo head_match=true && printf 'remote_status_start\n' && git status --short && printf 'remote_status_end\n'"
```

Output:

```text
local_head=0de18b9b3c73a9407fab57876056b49b35b4f79a
remote_head=0de18b9b3c73a9407fab57876056b49b35b4f79a
head_match=true
remote_status_start
remote_status_end
```

Command:

```text
ssh -o BatchMode=yes -o ConnectTimeout=20 gpu3070ti-relay
# In /home/ubuntu/ForestNav:
# env -u FORESTNAV_SOURCE_HEAD PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
#   /home/ubuntu/ForestNav.pre_git_20260707T101154Z/.venv/bin/python <M3-only manifest runner>
#
# The runner reads 0_trials/module2_planner_probe/query_manifest.csv verbatim,
# uses M1 records only for reference_path_length_m, calls the existing
# forest_n3p.main_evaluation ha_rl_rs_ppo path, and overwrites only
# 0_trials/module2_planner_probe/M3/.
```

Output:

```text
{
  "event": "preflight",
  "ok_to_run": true,
  "blocking_issues": [],
  "warnings": [
    "T14 formal scale is not satisfied: queries_per_bucket=40, seed_count=5"
  ],
  "available_methods": [
    "ha_rl_rs_ppo"
  ]
}
{
  "event": "first10_projection",
  "method_label": "M3",
  "elapsed_first10_s": 11.754736175062135,
  "projected_total_probe_wall_clock_s": 94.03788940049708,
  "hard_cap_s": 21600,
  "decision": "continue"
}
{
  "event": "method_complete",
  "method_label": "M3",
  "method": "ha_rl_rs_ppo",
  "record_count": 80,
  "elapsed_s": 96.26055181701668,
  "records_csv": "0_trials/module2_planner_probe/M3/records.csv",
  "summary_csv": "0_trials/module2_planner_probe/M3/summary_by_method_bucket.csv",
  "failure_reasons": {
    "": 67,
    "timeout": 13
  }
}
```

Command:

```text
rsync -av --delete gpu3070ti-relay:/home/ubuntu/ForestNav/0_trials/module2_planner_probe/M3/ 0_trials/module2_planner_probe/M3/
```

Output:

```text
Transfer starting: 7 files
./
first10_projection.json
queries.csv
records.csv
run_config.json
summary.json
summary_by_method_bucket.csv

sent 1510 bytes  received 240787 bytes  2422970000 bytes/sec
total size is 254678  speedup is 1.05
```

Command:

```text
python3 - <<'PY'
import csv, json
from collections import Counter
from pathlib import Path
required=['rl_attempts','rl_successes','rs_attempts','nn_forward_time_s','fallback_to_primitives_count','analytic_attempts']
records=Path('0_trials/module2_planner_probe/M3/records.csv')
rows=list(csv.DictReader(records.open(newline='', encoding='utf-8')))
missing=[c for c in required if c not in (rows[0].keys() if rows else [])]
fails=Counter(row.get('failure_reason') or '' for row in rows)
exceptions={k:v for k,v in fails.items() if k.startswith('m3_exception:')}
buckets=Counter(row['difficulty_bucket'] for row in rows)
summary=list(csv.DictReader(Path('0_trials/module2_planner_probe/M3/summary_by_method_bucket.csv').open(newline='', encoding='utf-8')))
print(json.dumps({
  'records_rows': len(rows),
  'bucket_counts': dict(buckets),
  'missing_required_telemetry_columns': missing,
  'failure_reasons': dict(fails),
  'exception_failure_reasons': exceptions,
  'same_exception_over_50pct': any(v > len(rows)/2 for v in exceptions.values()),
  'summary_rows': len(summary),
  'summary_success_rates': [{k: row[k] for k in ['method','difficulty_bucket','count','success_count','success_rate','rl_attempts_total','rl_successes_total','rs_attempts_total','fallback_to_primitives_total']} for row in summary],
}, indent=2))
if len(rows)!=80 or missing or any(v > len(rows)/2 for v in exceptions.values()) or len(summary)!=2:
    raise SystemExit(1)
PY
```

Output:

```text
{
  "records_rows": 80,
  "bucket_counts": {
    "Complex": 40,
    "Extreme": 40
  },
  "missing_required_telemetry_columns": [],
  "failure_reasons": {
    "": 67,
    "timeout": 13
  },
  "exception_failure_reasons": {},
  "same_exception_over_50pct": false,
  "summary_rows": 2,
  "summary_success_rates": [
    {
      "method": "ha_rl_rs_ppo",
      "difficulty_bucket": "Complex",
      "count": "40",
      "success_count": "36",
      "success_rate": "0.9",
      "rl_attempts_total": "233",
      "rl_successes_total": "36",
      "rs_attempts_total": "5174",
      "fallback_to_primitives_total": "197"
    },
    {
      "method": "ha_rl_rs_ppo",
      "difficulty_bucket": "Extreme",
      "count": "40",
      "success_count": "31",
      "success_rate": "0.775",
      "rl_attempts_total": "555",
      "rl_successes_total": "31",
      "rs_attempts_total": "8688",
      "fallback_to_primitives_total": "524"
    }
  ]
}
```

Command:

```text
cmp -s 0_trials/module2_planner_probe/query_manifest.csv 0_trials/module2_planner_probe/M3/queries.csv && echo query_manifest_reused_verbatim=true
```

Output:

```text
query_manifest_reused_verbatim=true
```

Command:

```text
git diff --exit-code -- 0_trials/module2_planner_probe/M1 0_trials/module2_planner_probe/M2 && echo m1_m2_diff_after_m3=clean
```

Output:

```text
m1_m2_diff_after_m3=clean
```

### 2026-07-08 D6 combined summary and mechanical band regeneration

Command:

```text
PYTHONPATH=2_experiment python3 - <<'PY'
# Regenerate probe_summary.md, probe_summary.csv, paired_m3_vs_m1.csv,
# and probe_band_verdict.json from unchanged M1/M2 artifacts and rerun M3.
PY
```

Output:

```text
{
  "reported_band": "no_signal",
  "success_delta_pp_m3_minus_m1_extreme": 5.000000000000004,
  "time_ratio_m3_over_m1_extreme": 0.7927760439383782,
  "expansions_ratio_m3_over_m1_extreme": 0.04252873563218391,
  "m3_failure_reasons": {
    "": 67,
    "timeout": 13
  },
  "outputs": {
    "probe_summary_md": "0_trials/module2_planner_probe/probe_summary.md",
    "probe_summary_csv": "0_trials/module2_planner_probe/probe_summary.csv",
    "paired_csv": "0_trials/module2_planner_probe/paired_m3_vs_m1.csv",
    "probe_band_verdict_json": "0_trials/module2_planner_probe/probe_band_verdict.json"
  }
}
```

Command:

```text
python3 - <<'PY'
import csv, json
from pathlib import Path
root=Path('0_trials/module2_planner_probe')
summary=list(csv.DictReader((root/'probe_summary.csv').open(newline='', encoding='utf-8')))
paired=list(csv.DictReader((root/'paired_m3_vs_m1.csv').open(newline='', encoding='utf-8')))
verdict=json.loads((root/'probe_band_verdict.json').read_text())
required_summary={'method_label','method','method_name','difficulty_bucket','query_count','success_rate','timeout_rate','median_expansions','p95_expansions','median_time_s','p95_time_s','collision_violation_total','rl_attempts_total','rl_successes_total','rs_attempts_total','rl_attempt_success_rate','mean_nn_forward_time_s','fallback_to_primitives_total','failure_reasons'}
print(json.dumps({
  'probe_summary_rows': len(summary),
  'probe_summary_missing_cols': sorted(required_summary-set(summary[0])) if summary else sorted(required_summary),
  'paired_rows': len(paired),
  'verdict_reported_band': verdict.get('reported_band'),
  'verdict_success_delta_pp': verdict.get('success_delta_pp_m3_minus_m1_extreme'),
  'verdict_time_ratio': verdict.get('time_ratio_m3_over_m1_extreme'),
  'verdict_expansions_ratio': verdict.get('expansions_ratio_m3_over_m1_extreme'),
  'm3_exception_count': verdict.get('m3_exception_count'),
}, indent=2))
if len(summary)!=6 or len(paired)!=80 or verdict.get('reported_band') not in {'strong_signal','weak_signal','no_signal'} or verdict.get('m3_exception_count') != 0:
    raise SystemExit(1)
PY
```

Output:

```text
{
  "probe_summary_rows": 6,
  "probe_summary_missing_cols": [],
  "paired_rows": 80,
  "verdict_reported_band": "no_signal",
  "verdict_success_delta_pp": 5.000000000000004,
  "verdict_time_ratio": 0.7927760439383782,
  "verdict_expansions_ratio": 0.04252873563218391,
  "m3_exception_count": 0
}
```

### 2026-07-08 D1 rerun-only M1/M2 artifact verification

Command:

```text
git status --short -- 0_trials/module2_planner_probe/M1 0_trials/module2_planner_probe/M2 && git diff --exit-code --stat -- 0_trials/module2_planner_probe/M1 0_trials/module2_planner_probe/M2
```

Output:

```text

```

Interpretation: no output and exit status 0; existing M1/M2 tracked artifacts
are unchanged before the M3-only rerun.

Command:

```text
python3 - <<'PY'
from pathlib import Path
for d in [Path('0_trials/module2_planner_probe/M1'), Path('0_trials/module2_planner_probe/M2')]:
    print(f'[{d}]')
    for p in sorted(d.iterdir()):
        if p.is_file():
            print(f'{p.name}\t{p.stat().st_size}')
PY
```

Output:

```text
[0_trials/module2_planner_probe/M1]
first10_projection.json	235
queries.csv	12931
records.csv	151937
run_config.json	1337
summary.json	2474
summary_by_method_bucket.csv	985
[0_trials/module2_planner_probe/M2]
first10_projection.json	252
queries.csv	12931
records.csv	155369
run_config.json	1345
summary.json	2546
summary_by_method_bucket.csv	1073
```

Command:

```text
python3 - <<'PY'
import csv
from pathlib import Path
for method_dir in ['M1','M2']:
    path=Path('0_trials/module2_planner_probe')/method_dir/'summary_by_method_bucket.csv'
    print(f'[{method_dir}] {path}')
    with path.open(newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        for row in reader:
            bucket=row.get('difficulty_bucket') or row.get('bucket')
            method=row.get('method')
            success=row.get('success_rate')
            n=row.get('queries') or row.get('n') or row.get('query_count')
            print(f'{method_dir} method={method} bucket={bucket} n={n} success_rate={success}')
PY
```

Output:

```text
[M1] 0_trials/module2_planner_probe/M1/summary_by_method_bucket.csv
M1 method=ha_single_rs bucket=Complex n=None success_rate=0.675
M1 method=ha_single_rs bucket=Extreme n=None success_rate=0.725
[M2] 0_trials/module2_planner_probe/M2/summary_by_method_bucket.csv
M2 method=ha_dang_multi_rs bucket=Complex n=None success_rate=0.75
M2 method=ha_dang_multi_rs bucket=Extreme n=None success_rate=0.675
```

Command:

```text
python3 - <<'PY'
import hashlib
from pathlib import Path
for method_dir in ['M1','M2']:
    print(f'[{method_dir} sha256]')
    for p in sorted((Path('0_trials/module2_planner_probe')/method_dir).iterdir()):
        if p.is_file():
            print(f'{p.name}\t{hashlib.sha256(p.read_bytes()).hexdigest()}')
PY
```

Output:

```text
[M1 sha256]
first10_projection.json	ef534714615d5b8e4c6820fa35656af42fa4a83c62ea661973662e4f2130190b
queries.csv	b2ee56574bd10b975c390b14cfaca2ae443b892016b54bc81fded503d9a0c78a
records.csv	07c4b0384c5faaee0c0f044ffee5f7724eeade82f16bb18c8e14a7fe76847485
run_config.json	d034fe72350186b0c07fe97db17350a8642c1158bda7dc4eeeb14ba2a1ad2de7
summary.json	3f7603ce6791d1decfbf8a00709e945e1b9489cea71ffe31a76a605809d4e7f8
summary_by_method_bucket.csv	bcce11b1f30ace5fe29cf6d05cfc92dc375c821d0c6ba317eef6a2374fa46db4
[M2 sha256]
first10_projection.json	5126960aef6d440033a9ee58713eff74b0e95c41fac15e4a51990034163d56c2
queries.csv	b2ee56574bd10b975c390b14cfaca2ae443b892016b54bc81fded503d9a0c78a
records.csv	3fc164cb21196df4d22fddc8f57155104fefc6d42af95e97e0d603acf6deb550
run_config.json	c39b7836362727657b4a7153c8802fe0d2d5d6307c5a115e3292dba67bf1b032
summary.json	9d7e78efcc338e6fdcc99c571ca6b7506849551eac799225007f5a1518619618
summary_by_method_bucket.csv	aa3fbc95a39402544e6411acbba3d4a18e7f702764de678a62ef858cc24e0d9b
```

### 2026-07-08 D2 gpu3070ti-relay training interpreter verification

Command:

```text
ssh -o BatchMode=yes gpu3070ti-relay <<'SH'
set -eu
PY=/home/ubuntu/ForestNav.pre_git_20260707T101154Z/.venv/bin/python
cd "$HOME/ForestNav"
echo "train_command_seed20260709"
sed -n '1p' 0_trials/module2_gate3_formal_v3/seed20260709/train_command.txt
echo "python_path=$PY"
ls -l "$PY"
"$PY" --version
echo "exact_import_smoke_start"
"$PY" -c "import gymnasium, stable_baselines3"
echo "exact_import_smoke_ok"
echo "version_smoke_start"
"$PY" - <<'PY'
import gymnasium, stable_baselines3, torch, sys
print(f'executable={sys.executable}')
print(f'gymnasium={gymnasium.__version__}')
print(f'stable_baselines3={stable_baselines3.__version__}')
print(f'torch={torch.__version__}')
print(f'cuda_available={torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'cuda_device={torch.cuda.get_device_name(0)}')
PY
echo "version_smoke_end"
SH
```

Output:

```text
train_command_seed20260709
env -u FORESTNAV_SOURCE_HEAD PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE /home/ubuntu/ForestNav.pre_git_20260707T101154Z/.venv/bin/python -m forest_n3p.scripts.train_rl_rs_ppo --allow-duplicate-openmp --contract-path .pipeline/contracts/module2-rl-rs-gate3-formal-v3.md --seed 20260709 --device cuda --curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260709 --n-envs 8 --total-timesteps 500000 --n-steps 256 --batch-size 256 --n-epochs 10 --gamma 0.98 --gae-lambda 0.95 --clip-range 0.2 --ent-coef 0.01 --max-grad-norm 0.5 --lr-schedule linear --checkpoint-freq 50000 --obs-patch-size-m 6.4 --obs-patch-cells 64 --max-steps 32 --output-dir 0_trials/module2_gate3_formal_v3/seed20260709/train --features-extractor patch_cnn --cnn-output-dim 256 --learning-rate 0.0003 --value-pretrain-timesteps 0
python_path=/home/ubuntu/ForestNav.pre_git_20260707T101154Z/.venv/bin/python
lrwxrwxrwx 1 ubuntu ubuntu 7 Jun 20 16:36 /home/ubuntu/ForestNav.pre_git_20260707T101154Z/.venv/bin/python -> python3
Python 3.12.3
exact_import_smoke_start
exact_import_smoke_ok
version_smoke_start
executable=/home/ubuntu/ForestNav.pre_git_20260707T101154Z/.venv/bin/python
gymnasium=1.3.0
stable_baselines3=2.9.0
torch=2.12.1+cu130
cuda_available=True
cuda_device=NVIDIA GeForce RTX 3070 Ti Laptop GPU
version_smoke_end
```

### 2026-07-08 D3 local checkpoint SHA256 verification

Command:

```text
ls -l 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip 0_trials/module2_gate3_formal_v3/seed20260709/gate3_trial_manifest.json
```

Output:

```text
-rw-r--r--@ 1 sun  staff      7822 Jul  7 05:41 0_trials/module2_gate3_formal_v3/seed20260709/gate3_trial_manifest.json
-rw-r--r--@ 1 sun  staff  15183390 Jul  7 06:04 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip
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
python3 - <<'PY'
import json, hashlib
from pathlib import Path
manifest_path=Path('0_trials/module2_gate3_formal_v3/seed20260709/gate3_trial_manifest.json')
model_path=Path('0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip')
manifest=json.loads(manifest_path.read_text())
needle='final_model.zip'
found=[]
def walk(obj,path=''):
    if isinstance(obj,dict):
        for k,v in obj.items():
            walk(v, f'{path}.{k}' if path else str(k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            walk(v, f'{path}[{i}]')
    elif isinstance(obj,str) and (needle in obj or 'ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2' in obj):
        found.append((path,obj))
walk(manifest)
actual=hashlib.sha256(model_path.read_bytes()).hexdigest()
expected=None
for path,value in found:
    if value == actual:
        expected=value
print(f'manifest={manifest_path}')
print(f'model={model_path}')
print(f'actual_sha256={actual}')
for path,value in found:
    print(f'manifest_match_candidate {path}={value}')
print(f'match={expected == actual}')
if expected != actual:
    raise SystemExit(1)
PY
```

Output:

```text
manifest=0_trials/module2_gate3_formal_v3/seed20260709/gate3_trial_manifest.json
model=0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip
actual_sha256=ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2
manifest_match_candidate train_model=train/final_model.zip
manifest_match_candidate eval_config.command=python -m forest_n3p.scripts.eval_rl_rs_gate3 --allow-duplicate-openmp --contract-path .pipeline/contracts/module2-rl-rs-gate3-formal-v3.md --model 0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip --output-dir 0_trials/module2_gate3_formal_v3/seed20260709/eval --seed 20260709 --device cuda --curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260709 --episodes 256 --min-episodes 256 --success-threshold 0.8 --obs-patch-size-m 6.4 --obs-patch-cells 64 --max-steps 32
manifest_match_candidate checkpoints[0].path=train/final_model.zip
manifest_match_candidate checkpoints[0].sha256=ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2
match=True
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
