---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_gate3_formal_preflight.md
  - .pipeline/experiments/20260704_module2_f03_oracle_sampler_collision_guard.md
---

# Module2 F03.5 Gate #3 No-Warm Formal Trial 记录

## 直观结论

F03.5 的 no-warm-start 正式 trial 已经跑完并通过 formal audit。结论不是通过, 而是一个可写入研究记录的正式失败:

- `formal_decision=fail`
- `formal_claim_allowed=true`
- `formal_blockers=[]`
- 64 个 eval episodes 中 terminal-RS-success 为 29/64, 成功率 0.453125。
- 预注册阈值是 0.8, 因此 no-warm PPO 在当前 F03 预算下没有学到足够稳定的 RS-connectable funnel 行为。

这只关闭 no-warm-start 分支。F02.6 obstacle-summary warm-start 决策仍是 pending, 不能把这次失败偷偷改写成 warm-start 失败, 也不能直接 claim 整个 PPO 路线已经证伪。

## 运行边界

正式命令来自 preflight manifest, 不含 `--smoke`, train/eval curriculum 都是 `f03`, eval episodes/min episodes 都是 64。

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE python -m forest_n3p.scripts.run_rl_rs_gate3_trial \
  --output-dir 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1 \
  --seed 20260704 \
  --device auto \
  --train-curriculum-preset f03 \
  --eval-curriculum-preset f03 \
  --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --heldout-seed 20260704 \
  --train-total-timesteps 100000 \
  --train-n-envs 1 \
  --train-n-steps 128 \
  --train-batch-size 64 \
  --train-n-epochs 4 \
  --eval-episodes 64 \
  --eval-min-episodes 64 \
  --eval-success-threshold 0.8 \
  --obs-patch-size-m 6.4 \
  --obs-patch-cells 64 \
  --max-steps 32 \
  --allow-duplicate-openmp
```

审计命令:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.audit_rl_rs_gate3_trial \
  --trial-dir 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1 \
  --min-formal-episodes 64 \
  --required-success-threshold 0.8 \
  --required-train-curriculum f03 \
  --required-eval-curriculum f03 \
  --warm-start-decision pending \
  --output 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json
```

## Attempt 01: sampler collision 中断

第一次正式运行没有到达 PPO 判定阶段, 在训练 reset 中触发:

```text
ValueError: sampled curriculum goal state is in collision
```

保留产物:

- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/failed_attempt_01/run_formal_trial.log`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/failed_attempt_01/train_partial/episodes_env0.csv`

根因和修复见 `.pipeline/experiments/20260704_module2_f03_oracle_sampler_collision_guard.md`。修复后 `OracleConnectorContextSampler` 只跳过当前 profile-aware 地图重建下已经碰撞的少量 oracle rows, 不放宽 collision checker。

## Attempt 02: 正式 train/eval 完成

第二次正式运行完成并写出以下核心产物:

- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/train/final_model.zip`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/train/summary.json`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/train/training_manifest.json`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_eval_episodes.csv`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_summary.json`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_trial_manifest.json`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json`

训练摘要:

```text
status=complete
warm_start_status=not_applied_f02_6_pending
total_timesteps=100000
n_envs=1
n_steps=128
batch_size=64
n_epochs=4
checkpoint_count=11
```

Eval 摘要:

```text
decision=fail
episodes=64
terminal_rs_success=29
terminal_rs_success_rate=0.453125
collision_rate=0.359375
truncation_rate=0.1875
success_threshold=0.8
```

Formal audit 摘要:

```text
formal_decision=fail
formal_claim_allowed=true
formal_blockers=[]
formal_warnings=[]
evaluator_decision=fail
train_curriculum_preset=f03
eval_curriculum_preset=f03
warm_start_status=not_applied_f02_6_pending
warm_start_decision=pending
```

## 研究含义

这次结果命中 Contract 的 Gate #3 no-warm failure signal: 在规定 formal budget 下, 从零 PPO 的 terminal-RS-success 没有超过 80%。它说明当前 reward/curriculum/architecture 对无初始化 PPO 不够, 但没有证明 obstacle-summary warm-start 不可行。

更直观地说: policy 不是跑不起来, 也不是审计无效; 它能生成一部分可对接轨迹, 但碰撞率 35.9% 加截断率 18.8% 太高, 离 planner 插槽所需的可靠 analytic operator 还差很远。

## 当前不 claim 的内容

- 不 claim F03.5 Gate #3 通过。
- 不 claim warm-start PPO 失败。
- 不 claim planner integration 已完成。
- 不 claim PPO 路线整体证伪; 只 claim no-warm-start formal branch 在当前预注册预算下失败。
