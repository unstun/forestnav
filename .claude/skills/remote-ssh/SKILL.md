---
name: remote-ssh
description: Use when connecting to GPU training hosts for ForestNav, checking remote resources, syncing code, or diagnosing relay SSH access
---

# ForestNav Remote SSH

## Overview

ForestNav uses local Mac files as the code source of truth. GPU hosts are execution
copies for training, evaluation, and resource checks. Any remote-only edit must
be copied back to the same local project path before it is treated as project
state.

Use fixed SSH aliases instead of raw IPs:

```bash
ssh gpu3070ti-relay
ssh gpu5070ti-relay
```

## Hosts

| alias | user | role | relay |
|---|---|---|---|
| `gpu3070ti-relay` | `ubuntu` | RTX 3070 Ti Laptop GPU host, 8 GiB VRAM | `ubuntu-obgx` -> `127.0.0.1:23070` |
| `gpu5070ti-relay` | `sun` | RTX 5070 Ti host, 16 GiB VRAM | `ubuntu-obgx` -> `127.0.0.1:2222` |

`gpu3070ti-relay` is a reverse SSH relay because the 3070 Ti host has no public
IP. The 3070 Ti host initiates an outbound SSH connection to `ubuntu-obgx`;
the Mac connects through `ProxyJump ubuntu-obgx`.

## Verified Signals

3070 Ti, verified on 2026-06-05:

```text
hostname: ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
user: ubuntu
system: Linux 6.17.0-35-generic x86_64 GNU/Linux
GPU: NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192 MiB total
driver: 595.71.05
```

5070 Ti, verified on 2026-05-29:

```text
hostname: ubuntu
user: sun
GPU: NVIDIA GeForce RTX 5070 Ti, 16303 MiB total
```

## Quick Checks

Run these from the Mac:

```bash
ssh -G gpu3070ti-relay | rg '^(user|hostname|port|proxyjump|hostkeyalias) '
ssh -o BatchMode=yes -o ConnectTimeout=8 gpu3070ti-relay \
  'hostname; whoami; uname -srmo; nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader'

ssh -o BatchMode=yes -o ConnectTimeout=8 gpu5070ti-relay \
  'hostname; whoami; nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader'
```

Expected `gpu3070ti-relay` SSH resolution:

```text
user ubuntu
hostname 127.0.0.1
port 23070
proxyjump ubuntu-obgx
hostkeyalias gpu3070ti-relay
```

Check the jump host listener:

```bash
ssh ubuntu-obgx 'ss -ltnp | grep -E "127\\.0\\.0\\.1:23070" || true'
```

Expected listener:

```text
127.0.0.1:23070 LISTEN
```

## ForestNav Sync Rule

Local repo:

```text
/Users/sun/tongbu/study/phdproject/ForestNav
```

Default remote working copy:

```text
$HOME/ForestNav
```

Before remote execution, sync from local to the chosen host. Keep generated
heavy outputs out of the command unless they are needed for the run.

Example:

```bash
rsync -az --delete \
  --exclude .git \
  --exclude .venv \
  --exclude __pycache__ \
  --exclude '2_experiment/outputs' \
  /Users/sun/tongbu/study/phdproject/ForestNav/ \
  gpu3070ti-relay:~/ForestNav/
```

After remote diagnostics or temporary edits, sync the edited files back and
inspect local `git diff` before making claims about code state.

## Training Session Pattern

Start long jobs inside `tmux`:

```bash
ssh gpu3070ti-relay
tmux new -s dqn10
cd ~/ForestNav
nvidia-smi
```

For 8 GiB VRAM on 3070 Ti, prefer smoke tests and smaller training batches.
Use 5070 Ti for heavier runs when the same code and data are available there.

## Troubleshooting

If `gpu3070ti-relay` returns `Permission denied` for `sun@127.0.0.1`, the local
SSH config is using the wrong account. `gpu3070ti-relay` must use `User ubuntu`.

If `Connection closed by UNKNOWN port 65535` appears before authentication, the
relay reached the 3070 Ti side but the local SSH server did not complete the
handshake. On the 3070 Ti host, check:

```bash
sudo systemctl status ssh 2>/dev/null || sudo systemctl status sshd 2>/dev/null
ss -ltnp | grep -E '(:22\\s)' || true
```

If the jump host listener is missing, restart the 3070 Ti reverse relay service
on the 3070 Ti host:

```bash
systemctl --user restart gpu3070ti-relay.service
systemctl --user status gpu3070ti-relay.service --no-pager
```

If user systemd is unavailable, check the fallback log:

```bash
tail -n 80 ~/.ssh/gpu3070ti-relay.log
```
