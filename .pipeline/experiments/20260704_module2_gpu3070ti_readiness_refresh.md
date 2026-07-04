---
status: completed
origin: ai+local+remote
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 gpu3070ti-relay Readiness Refresh

## 直观结论

本轮只做只读远端刷新，不训练、不同步、不安装、不运行 approved preflight。

`gpu3070ti-relay` 当前仍可连，3070 Ti CUDA 环境仍可用，formal preflight 后续依赖的 oracle parquet 和 obstacle-summary BC checkpoint 在本地/远端 hash 一致。这个结果只说明“如果 F02.6 后续被批准，远端基础资源当前没有明显漂移”；它不关闭 F02.6，也不允许写任何 formal performance claim。

## 核验结果

- SSH: `gpu3070ti-relay` 解析为 `ubuntu@127.0.0.1:23070`，`proxyjump=ubuntu-obgx`。
- jump listener: `127.0.0.1:23070 LISTEN`。
- host: `ubuntu-OMEN-by-HP-Laptop-17-ck1xxx`, user `ubuntu`, kernel `Linux 6.17.0-35-generic x86_64 GNU/Linux`。
- GPU: `NVIDIA GeForce RTX 3070 Ti Laptop GPU`, total 8192 MiB, free 7812 MiB, driver `595.71.05`。
- Python stack: Python `3.12.3`, torch `2.12.1+cu130`, CUDA available, SB3 `2.9.0`, pyarrow `24.0.0`, gymnasium `1.3.0`。
- oracle parquet: local/remote bytes `1116417`, rows `7860`, SHA-256 `1614d12de3c3436fdd2bc8088df0843f402c8425e40ca500ee0c71c70715b527`。
- obstacle-summary BC checkpoint: local/remote bytes `119287`, SHA-256 `3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683`。
- remote scripts present: preflight, runner, audit scripts all exist in `~/ForestNav`.

## 产物

- `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.md`

## 边界

- 本轮没有训练。
- 本轮没有运行 approved remote preflight。
- 本轮没有同步代码或安装依赖。
- F02.6 仍是 `pending_human_decision`。
- `remote_formal_execution_packet.status` 仍是 `blocked_until_f02_6_decision`。
- 不得把本轮 readiness refresh 写成 PPO checkpoint、H02 formal output、warm-start effect 或 formal performance result。
