---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md
  - .pipeline/experiments/20260704_module2_h01_f02_6_decision_packet_guard.md
  - .pipeline/experiments/20260704_module2_f03_gpu3070ti_remote_readiness.md
---

# F02.6 Decision Record Protocol

## 直观结论

本轮完成 F02.6 决策记录协议, 但没有替 Dr Sun 批准 warm-start。

现在系统里有两层对象:

- decision packet: 汇总证据并推荐 `approve_obstacle_summary_warm_start`。
- decision record: 记录 Dr Sun 是否批准或驳回, 并把人类决策映射成 H01/preflight/audit 能消费的枚举。

当前真实产物仍是 `pending_human_decision`。它明确禁止本地训练, 也不允许 formal performance claim。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_f02_6_decision_record.py`
- `2_experiment/forest_n3p/tests/test_module2_f02_6_decision_record.py`
- `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `0_trials/module2_f02_6_decision_record/f02_6_decision_record.md`

## 机器语义

当前 record:

- status: `pending_human_decision`
- effective warm-start decision: `pending`
- blocker: `requires_dr_sun_approval`
- remote_training_allowed: `false`
- local_training_allowed: `false`
- formal_claim_allowed: `false`
- observed remote warm-start preflight: `blocked`, blocker `warm_start_decision_pending`

若 Dr Sun 后续明确批准:

- 输入 decision: `approve_obstacle_summary_warm_start`
- decider 必须是 `Dr Sun`
- H01/preflight/audit 映射值: `approved_obstacle_summary`
- 允许动作: 在 `gpu3070ti-relay` 重新生成 approved warm-start preflight
- 仍不允许动作: 本地训练、论文 formal performance claim

若 Dr Sun 后续明确驳回:

- 输入 decision: `reject_obstacle_summary_warm_start`
- H01 映射值: `no_warm_only`
- preflight/audit 映射值: `not_used`
- 下一步应先做 stronger/full patch-CNN warm-start protocol, 而不是继续 obstacle-summary warm-start formal run。

## H01 消费口

`build_module2_evaluation_manifest.py` 新增 `--warm-start-decision-record`。当前 H01 manifest 已显式引用 pending record, 结果仍是:

- status: `blocked_pending_decisions`
- global blockers: `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`
- method-level blockers: `requires_dr_sun_approval`, `f02_6_decision_record_pending`, `missing_module2_rl_rs_checkpoint`
- formal command: blocked

这证明新协议没有绕过 Dr Sun 审批门, 但将来批准后有机器可读入口。

## 验证

- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact file reads.
- Targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_record.py` -> `4 passed in 0.23s`。
- Adjacent H01: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_record.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` -> `9 passed in 0.48s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_f02_6_decision_record.py 2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py`。
- Artifact generation: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record ...` -> status `pending_human_decision`。
- H01 refresh: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest ... --warm-start-decision-record 0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` -> status `blocked_pending_decisions`。

## 边界

- This does not approve F02.6.
- This does not run local training.
- This does not run remote training.
- This does not create a formal PPO checkpoint.
- This does not unlock H02 formal evaluation.
- Any formal warm-start PPO run must use `gpu3070ti-relay` or another explicitly approved remote GPU.
