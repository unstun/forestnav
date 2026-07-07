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
