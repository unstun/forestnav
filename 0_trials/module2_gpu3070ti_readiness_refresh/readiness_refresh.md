# Module2 gpu3070ti-relay Readiness Refresh

This is a read-only formal-gate readiness refresh. It is not a training run, not an approved preflight, and not paper result material.

## Status

- status: `remote_readiness_refreshed_f02_6_still_blocked`
- source_head: `7ed00f0967f72f24c8827bb6c19773bbdbf1ea23`
- runs_training: `False`
- runs_remote_preflight: `False`
- local_training_allowed: `False`
- remote_training_resource: `gpu3070ti-relay`
- formal_claim_allowed: `False`

## What Was Checked

- SSH alias still resolves to `ubuntu@127.0.0.1:23070` through `ubuntu-obgx`.
- Jump host listener for `127.0.0.1:23070` is present.
- Remote host is `ubuntu-OMEN-by-HP-Laptop-17-ck1xxx`.
- Remote GPU is `NVIDIA GeForce RTX 3070 Ti Laptop GPU`, 8192 MiB total, 7812 MiB free.
- Remote Python stack is present: Python `3.12.3`, torch `2.12.1+cu130`, CUDA available `True`, SB3 `2.9.0`, pyarrow `24.0.0`, gymnasium `1.3.0`.
- Remote scripts exist: `preflight_rl_rs_gate3_formal_trial.py`, `run_rl_rs_gate3_trial.py`, `audit_rl_rs_gate3_trial.py`.
- Oracle connector parquet exists both locally and remotely with 7860 rows and matching SHA-256 `True`.
- Obstacle-summary BC checkpoint exists both locally and remotely with matching SHA-256 `True`.

## Critical Hashes

```text
oracle_connector_results.parquet
local_sha256=1614d12de3c3436fdd2bc8088df0843f402c8425e40ca500ee0c71c70715b527
remote_sha256=1614d12de3c3436fdd2bc8088df0843f402c8425e40ca500ee0c71c70715b527
rows=7860

obstacle_summary_bc_checkpoint
local_sha256=3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683
remote_sha256=3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683
```

## Gate Boundary

F02.6 is still `pending_human_decision`. This refresh does not approve warm-start, does not run approved remote preflight, and does not unlock formal PPO training. The next formal step remains Dr Sun's F02.6 decision.
