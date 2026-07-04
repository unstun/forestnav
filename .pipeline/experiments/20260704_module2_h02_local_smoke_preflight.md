---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
  - .pipeline/experiments/20260704_module2_h01_metric_protocol.md
  - .pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md
---

# H02.1 Local Smoke Preflight

## 直观结论

H02.1 不能完整完成, 因为 all-method smoke 需要 `ppo_analytic_operator` 和 `ppo_rs_funnel`, 而这两个方法都缺正式 RL-RS checkpoint, 且 F02.6 warm-start 决策仍是 `pending_human_decision`。

本次只做两件不会越权的事:

- 生成 H02.1 preflight, 把 full smoke blocker 写成机器可读 artifact。
- 实际跑通 available subset: `ha_no_analytic`, `ha_single_rs`, `ha_dang_multi_rs`, `mlp`, `bc_analytic_operator`。

这不能被写成 all-method smoke, 也不能被当作 formal result。

## 产物

- Preflight JSON: `0_trials/module2_h02_local_smoke/h02_local_smoke_preflight.json`
- Preflight Markdown: `0_trials/module2_h02_local_smoke/h02_local_smoke_preflight.md`
- Available subset run: `0_trials/module2_h02_local_smoke/h02_1_available_subset/`
- Builder: `2_experiment/forest_n3p/scripts/build_module2_h02_smoke_preflight.py`
- Test: `2_experiment/forest_n3p/tests/test_module2_h02_smoke_preflight.py`

## Full Smoke 阻塞

- `ppo_analytic_operator`: `missing_module2_rl_rs_checkpoint`, `f02_6_warm_start_decision_pending`, `f02_6_decision_packet_pending`
- `ppo_rs_funnel`: `missing_module2_rl_rs_checkpoint`, `f02_6_warm_start_decision_pending`, `f02_6_decision_packet_pending`

## Available Subset Smoke 结果

- Methods: `ha_no_analytic`, `ha_single_rs`, `ha_dang_multi_rs`, `mlp`, `bc_analytic_operator`
- Query count: `3`
- Record count: `15`
- Status: `candidate_or_smoke`
- Formal acceptance: `false`
- Collision violation total: `0`
- Method exception total: `0`
- BC checkpoint SHA-256: `3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683`
- Timeout metric columns present in `summary_by_method_bucket.csv`: yes
- A02.3 telemetry columns present in `records.csv`: `rl_attempts`, `rl_successes`, `rs_attempts`, `nn_forward_time_s`, `fallback_to_primitives_count`, `rollout_protocol`, `collision_checker`
- A02.3 telemetry summary columns present in `summary_by_method_bucket.csv`: `mean_nn_forward_time_s`, `p95_nn_forward_time_s`, `rl_attempts_total`, `rl_successes_total`, `rs_attempts_total`, `fallback_to_primitives_total`

## 命令

Preflight-only:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation --output-dir 0_trials/module2_h02_local_smoke/h02_1_available_subset --preflight-only --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator --queries-per-bucket 1 --seed-count 1 --queries-per-map 1 --density-profile-buckets validation_t06 --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md --allow-unresolved-human-review --no-enforce-t14-scale --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt
```

Subset smoke:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation --output-dir 0_trials/module2_h02_local_smoke/h02_1_available_subset --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator --queries-per-bucket 1 --seed-count 1 --queries-per-map 1 --density-profile-buckets validation_t06 --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md --allow-unresolved-human-review --no-enforce-t14-scale --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt
```

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_h02_smoke_preflight.py` 先失败于缺少 `build_module2_h02_smoke_preflight`。
- GREEN: 同一测试 -> `1 passed`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_h02_smoke_preflight.py`。
- Preflight-only: `ok_to_run=true`, blocking issues empty, warning 仅为 smoke scale 非 formal scale。
- Subset smoke: `record_count=15`, `query_count=3`, `status=candidate_or_smoke`, `formal_acceptance=false`。
- 2026-07-04 telemetry refresh: same available subset rerun after A02.3 P0; schema now includes runtime NN forward and RL/RS attempt telemetry. Full regression `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `112 passed in 12.15s`。

## 边界

- 本记录不关闭 H02.1 full all-method smoke。
- 本记录不生成 PPO checkpoint。
- 本记录不训练 PPO。
- 本记录不解除 F02.6 pending。
- 本记录不支持任何 formal performance claim。
