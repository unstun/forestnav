---
status: completed
origin: ai+local+remote
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_gate3_formal_preflight.md
  - .pipeline/experiments/20260704_module2_f03_obstacle_summary_warm_start.md
  - .pipeline/experiments/20260704_module2_h01_ppo_analytic_operator_manifest.md
---

# Module2 F03 gpu3070ti-relay Remote Readiness

## 直观结论

本轮把 PPO 后续训练从“本地不能跑”推进到“远端 3070 Ti 可执行、可预检、可产出 smoke artifact”的状态。

当前事实:

- `gpu3070ti-relay` 可连, GPU 是 `NVIDIA GeForce RTX 3070 Ti Laptop GPU`, 8192 MiB。
- 远端 `.venv` 已安装 PPO 训练所需依赖: `stable-baselines3==2.9.0`, `pyarrow==24.0.0`, `torch==2.12.1+cu130`; CUDA 可用。
- 本地真源已同步到远端 `~/ForestNav` 执行副本。
- no-warm formal preflight 在远端 ready。
- obstacle-summary warm-start formal preflight 在远端被 `warm_start_decision_pending` 正确阻塞。
- 远端 warm-start CUDA smoke 可以完成 tiny train/eval 并写出 artifact, 但 audit 明确判为 `not_formal`。

这一步只证明远端执行链路已经通。它不关闭 F02.6, 不产生 H01 formal PPO checkpoint, 不支持论文性能 claim。

## 远端环境证据

SSH/GPU:

```text
alias=gpu3070ti-relay
hostname=ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
user=ubuntu
kernel=Linux 6.17.0-35-generic x86_64 GNU/Linux
gpu=NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192 MiB, 7812 MiB free
driver=595.71.05
```

Python/CUDA:

```text
Python 3.12.3
torch 2.12.1+cu130
torch.cuda.is_available()=True
torch.cuda.get_device_name(0)=NVIDIA GeForce RTX 3070 Ti Laptop GPU
stable_baselines3 2.9.0
pyarrow 24.0.0
gymnasium 1.3.0
```

数据和 checkpoint:

```text
oracle_path=0_trials/module2_oracle_shape/oracle_connector_results.parquet
oracle_bytes=1116417
oracle_rows=7860
bc_checkpoint=2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt
bc_checkpoint_bytes=119287
bc_checkpoint_sha256=3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683
```

## 预检产物

no-warm formal preflight:

```text
artifact=0_trials/module2_remote_preflight/gate3_no_warm_remote_v1/gate3_preflight_manifest.json
preflight_status=ready
formal_trial_ready=true
formal_blockers=[]
device=cuda
runner=train/eval curriculum f03, 100000 timesteps, 64 eval episodes
```

obstacle-summary warm-start formal preflight:

```text
artifact=0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json
preflight_status=blocked
formal_trial_ready=false
formal_blocker=warm_start_decision_pending
observed=2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt
expected=approved_obstacle_summary or no --bc-checkpoint
```

## 远端 smoke 产物

命令:

```bash
PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.run_rl_rs_gate3_trial \
  --smoke \
  --allow-duplicate-openmp \
  --device cuda \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --output-dir 0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke \
  --seed 20260704
```

结果:

```text
status=complete
smoke=true
formal_gate_claim=false
warm_start_status=applied_obstacle_summary_bc
train_total_timesteps=16
train_curriculum_preset=open
eval_curriculum_preset=open
eval_episodes=4
terminal_rs_success_rate=1.0
model_sha256=35c32e22a1a27e7af081e9698e249f5b22f6378bd328a25ae298579d76e9430a
```

artifact:

```text
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/train/final_model.zip
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/train/summary.json
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/train/training_manifest.json
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/train/episodes_env0.csv
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/eval/gate3_summary.json
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/eval/gate3_eval_episodes.csv
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/gate3_trial_manifest.json
0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/gate3_formal_audit.json
```

artifact hashes:

```text
35c32e22a1a27e7af081e9698e249f5b22f6378bd328a25ae298579d76e9430a  train/final_model.zip
9510fb64f26a8faaab63b3e8fec5897985a42843d452040ec03efc1df57a8c10  train/training_manifest.json
4ffa8cec44199049a12b986dbe87ee9e67eeb43f44bb4a37211b0b0969ec0af7  gate3_trial_manifest.json
c82045777749167764b8de8414d471fd7cbdeada0837ad252ce27d67d58ed15e  gate3_formal_audit.json
```

formal audit:

```text
formal_decision=not_formal
formal_claim_allowed=false
formal_blockers=[
  smoke_trial,
  train_curriculum_not_f03,
  eval_curriculum_not_f03,
  insufficient_eval_episodes,
  warm_start_decision_pending
]
```

## 执行命令记录

远端依赖安装:

```bash
ssh gpu3070ti-relay 'cd ~/ForestNav && .venv/bin/python -m pip install stable-baselines3==2.9.0 pyarrow'
```

同步命令:

```bash
rsync -az \
  --exclude '.git' \
  --exclude '.venv*' \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  --exclude '1_survey' \
  /Users/sun/tongbu/study/phdproject/ForestNav/ \
  gpu3070ti-relay:~/ForestNav/
```

注意: 曾短暂尝试带 `--delete` 的同步, 发现它会试图清理远端 `.venv_d02_cuda`, 已立即中断并改为不带 `--delete` 的保守同步。远端 `.venv` 和 `.venv_d02_cuda` 均已确认仍存在。

artifact 回传:

```bash
rsync -az gpu3070ti-relay:~/ForestNav/0_trials/module2_remote_preflight/ \
  /Users/sun/tongbu/study/phdproject/ForestNav/0_trials/module2_remote_preflight/
rsync -az gpu3070ti-relay:~/ForestNav/0_trials/module2_remote_smoke/ \
  /Users/sun/tongbu/study/phdproject/ForestNav/0_trials/module2_remote_smoke/
```

## 当前边界

- 可以 claim: 远端 3070 Ti CUDA PPO smoke train/eval 链路可运行。
- 可以 claim: no-warm formal runner/audit protocol 在远端 ready。
- 可以 claim: warm-start formal runner/audit protocol 仍被 F02.6 pending 合法阻塞。
- 不能 claim: warm-start formal Gate #3 已跑。
- 不能 claim: F02.6 已关闭。
- 不能 claim: H01 `missing_module2_rl_rs_checkpoint` 已解除。
- 不能把 `0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/train/final_model.zip` 当正式 PPO checkpoint。
