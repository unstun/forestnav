---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md
---

# Module2 H01.1 Evaluation Manifest 记录

## 后续更新

2026-07-04 后续任务已解除 `bc_analytic_operator` 的 main evaluation method blocker。当前 H01 manifest 已重新生成, `bc_analytic_operator` 映射到同名 main evaluation method, 并指向 `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt`。更新记录见 `.pipeline/experiments/20260704_module2_h01_bc_operator_main_eval.md`。

2026-07-04 后续任务也已冻结 RealMap query generation protocol。当前 H01 manifest 引用 `0_trials/module2_realmap_query_protocol/module2_realmap_query_protocol.json`, 该 protocol 为 `status=frozen`, endpoint audit pass, 10 queries / 2 maps。更新记录见 `.pipeline/experiments/20260704_module2_h01_realmap_query_protocol.md`。

因此本文件下方关于 "BC analytic operator 还没有 main evaluation method" 和 "realmap query protocol 未冻结" 的表述只描述本记录创建时的历史状态, 不代表当前最新状态。当前仍未关闭的 H01 blockers 是 F02.6 warm-start decision、`ppo_analytic_operator` without terminal RS 未实现。

## 直观结论

H01.1 已推进到可审计的 manifest/preflight 形态, 但不能 claim formal-ready。当前产物明确写出 module2 v1 评测所需方法、正式规模、指标、realmap inventory 和 run command blocker。

核心状态是 `blocked_pending_decisions`, 不是 `ready_for_formal_run`。原因有三类:

1. F02.6 warm-start 决策仍未关闭。
2. H01.1 要求的 `BC analytic operator` 和 `PPO analytic operator without terminal RS` 还没有 main evaluation method。
3. real SLAM map inventory 已有, 但 realmap query generation/evaluation protocol 未冻结。

这一步的价值是把 H01 的“该怎么正式评测”从口头计划变成机器可生成、可 diff、可审计的 manifest, 同时阻止 AI 在 blockers 未清时直接跑大实验并声称 formal evaluation。

## 实现锚点

- 新增 manifest builder: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py`。
- `Module2EvaluationManifestConfig` 固定输入: output paths, contract, cutpoint supplement, realmap manifest, warm-start decision, RL-RS checkpoint, formal scale: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:12-26`。
- `build_manifest()` 输出 schema/status/source_head/contract/scale/methods/metrics/real_maps/blockers/run_command/claim_boundaries: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:58-92`。
- methods 覆盖 H01.1 要求的三类 baseline 和三类 learned analytic operator:
  - HA* no analytic / single RS / Dang multi-RS
  - F-N3P KNN / F-N3P MLP
  - BC analytic operator / PPO analytic operator / PPO+RS funnel
  代码位置: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:116-165`。
- `ppo_rs_funnel` 映射到已实现的 `main_evaluation` 方法 `ha_rl_rs_ppo`, 但在缺 checkpoint 或 F02.6 pending 时标为 blocked: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:144-164`。
- metrics 覆盖 Contract 主指标和诊断指标: `total_expansions`, `total_time_s`, `timeout_failure_rate`, `path_inflation_ratio`, `analytic_success_rate`, `terminal_rs_success_rate`, `fallback_count`, `nn_forward_time_s`: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:188-200`。
- realmap inventory 读取 `2_experiment/forest_n3p/assets/realmaps/manifest.json`, 但 `_realmap_queries_frozen()` 当前返回 `False`, 因此 manifest 明确 block realmap formal protocol: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:245-264`, `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:299-300`。
- formal command 只在 `ppo_rs_funnel` ready 时生成; pending 状态下 command 为 `None`: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:218-243`。

## 测试锚点

新增测试文件: `2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py`。

- pending F02.6 + missing checkpoint 时, manifest status 为 `blocked_pending_decisions`, scale 为 `100` queries/bucket 和 `5` seeds, 并列出 H01.1 所有方法: `2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py:11-61`。
- 测试锁定 `ppo_rs_funnel` blockers: `missing_module2_rl_rs_checkpoint`, `f02_6_warm_start_decision_pending`: `2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py:44-47`。
- 测试锁定 `bc_analytic_operator` / `ppo_analytic_operator` 均为 `missing_main_evaluation_method`: `2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py:48-49`。
- 测试锁定 primary/diagnostic metrics 和 realmap inventory: `2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py:51-58`。
- CLI 写出 JSON + Markdown; 当传入 checkpoint 且 warm-start decision 非 pending 时, `ppo_rs_funnel` 不再有 checkpoint/F02.6 blockers, 并生成 formal command: `2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py:62-102`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py -q
```

失败点:

```text
ModuleNotFoundError: No module named 'forest_n3p.scripts.build_module2_evaluation_manifest'
```

GREEN:

```text
2 passed in 0.17s
```

## 产物

命令:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest \
  --output-dir 0_trials/module2_v1_evaluation_manifest \
  --manifest-out 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json \
  --markdown-out 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.md \
  --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md \
  --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md \
  --warm-start-decision pending \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5
```

输出:

```text
status=blocked_pending_decisions
manifest=0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json
markdown=0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.md
```

抽查:

- global blockers: `f02_6_warm_start_decision_pending`, `missing_required_method_implementation`, `realmap_query_generation_not_frozen`。
- methods: `ha_no_analytic`, `ha_single_rs`, `ha_dang_multi_rs`, `f_n3p_knn`, `mlp`, `bc_analytic_operator`, `ppo_analytic_operator`, `ppo_rs_funnel`。
- realmaps: usable map count `2`, ids `dqn_realmap_a`, `willow_garage_0p10`。
- formal command: `None`, 因 blockers 未清。

## 当前边界

- 可以 claim: H01.1 manifest/preflight 产物已生成, 并能暴露 pending decisions / missing methods / realmap protocol gap。
- 可以 claim: H01.1 方法和指标已被机器可读地枚举。
- 不能 claim: H01 evaluation protocol 已 formal-ready。
- 不能 claim: BC analytic operator 或 pure PPO analytic operator 已实现。
- 不能 claim: real SLAM maps 已有 frozen query protocol。
- 不能 claim: F02.6 warm-start 决策已关闭。

下一步可选:

1. 关闭 F02.6 warm-start 决策后, 用正式 checkpoint 重新生成 manifest。
2. 实现 BC analytic operator loader/method, 解除 `bc_analytic_operator` blocker。
3. 冻结 realmap query generation/evaluation protocol。
