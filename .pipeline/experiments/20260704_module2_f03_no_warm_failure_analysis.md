---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_gate3_no_warm_formal_trial.md
---

# Module2 F03 No-Warm Formal Failure Analysis

## 直观结论

no-warm PPO 失败不是因为最简单的连接任务都不会。它在 `open_connector` 上 15/15 成功, 但在真正代表目标插槽的复杂森林分布上失败明显:

- `rs_failure_node`: 6/24 success, success rate 0.25, collision rate 0.583333。
- `heldout_procedural`: 2/14 success, success rate 0.142857, truncation rate 0.571429。
- `Complex` 与 `Extreme` 合并看都只有 4/19 success, success rate 0.210526。

所以当前失败的核心不是 runner、audit 或基本动力学接线, 而是 no-warm policy 没有学到复杂/极端森林中的避障 funnel 行为。open/simple curriculum 抬高了整体 success rate; 真正 hard distribution 仍然远低于可插入 planner 的可靠性要求。

## 数据来源

- eval CSV: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_eval_episodes.csv`
- train CSV: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/train/episodes_env0.csv`
- eval summary: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_summary.json`
- formal audit: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json`

Eval 总体:

```text
episodes=64
success=29
collision=23
truncated=12
success_rate=0.453125
collision_rate=0.359375
truncation_rate=0.187500
```

## Eval 按 curriculum stage 分解

```text
                    episodes  success  success_rate  collision  collision_rate  truncated  truncation_rate
heldout_procedural        14        2      0.142857          4        0.285714          8         0.571429
obstacle_bypass           11        6      0.545455          5        0.454545          0         0.000000
open_connector            15       15      1.000000          0        0.000000          0         0.000000
rs_failure_node           24        6      0.250000         14        0.583333          4         0.166667
```

解释:

- `open_connector` 已经饱和成功, 说明动作解码、单步动力学、terminal RS success set 和模型加载没有整体断裂。
- `rs_failure_node` 是核心目标分布, 但 success 只有 25%, collision 超过一半。
- `heldout_procedural` 的主要失败是 no-progress truncation, 不是碰撞; 这表示 policy 在未见程序化地图上经常走不进 terminal RS 可对接域。

## Eval 按难度/profile 分解

```text
difficulty_bucket  episodes  success  success_rate  collision_rate  truncation_rate
Complex                  19        4      0.210526        0.578947         0.210526
Extreme                  19        4      0.210526        0.368421         0.421053
NaN                      26       21      0.807692        0.192308         0.000000
```

```text
profile_name  episodes  success  success_rate  collision_rate  truncation_rate
complex_d02         13        4      0.307692        0.461538         0.230769
complex_d04          6        0      0.000000        0.833333         0.166667
extreme_d05          5        0      0.000000        0.600000         0.400000
extreme_d06          7        3      0.428571        0.285714         0.285714
extreme_d07          7        1      0.142857        0.285714         0.571429
NaN                 26       21      0.807692        0.192308         0.000000
```

解释:

- `complex_d04` 与 `extreme_d05` 是最明显的 collision-heavy profiles。
- `extreme_d07` 更偏 no-progress/truncation。
- 这支持后续把失败拆成两类: clearance/collision control 不足, 以及 progress-to-terminal-RS-domain 不足。

## 训练曲线一致性

训练 CSV 共 23121 episodes。整体训练 success rate 为 0.453916, 与 formal eval 0.453125 基本一致, 因此 eval fail 不是单次抽样异常。

首 1000 episode:

```text
heldout_procedural success_rate=0.216080 collision_rate=0.643216 truncation_rate=0.140704
obstacle_bypass    success_rate=0.349515 collision_rate=0.650485 truncation_rate=0.000000
open_connector     success_rate=1.000000 collision_rate=0.000000 truncation_rate=0.000000
rs_failure_node    success_rate=0.208763 collision_rate=0.572165 truncation_rate=0.219072
```

最后 1000 episode:

```text
heldout_procedural success_rate=0.287129 collision_rate=0.405941 truncation_rate=0.306931
obstacle_bypass    success_rate=0.535885 collision_rate=0.464115 truncation_rate=0.000000
open_connector     success_rate=1.000000 collision_rate=0.000000 truncation_rate=0.000000
rs_failure_node    success_rate=0.365239 collision_rate=0.554156 truncation_rate=0.080605
```

解释:

- 有学习信号: `rs_failure_node` success 从 0.208763 到 0.365239, `obstacle_bypass` 从 0.349515 到 0.535885。
- 但学习不足: 最后 1000 episode 的 `rs_failure_node` collision 仍为 0.554156, 距离 80% terminal-RS-success 很远。
- no-warm PPO 的失败不是完全随机, 而是收敛到一个只能处理 easy/open 和部分 bypass 的弱策略。

## Timing 边界

Eval CSV 中 `nn_forward_time_s` 全部为 0.0。当前 Gate #3 formal audit 的判定只依赖 success/fail、episode 数、curriculum、artifact 完整性和 warm-start status, 不依赖计时字段。

因此本 trial 可以支持:

- no-warm PPO 在当前预算下 Gate #3 failure。
- 各 stage/profile 的 failure mode 分布。

本 trial 不能支持:

- PPO inference wall-clock 更快或更慢。
- planner 集成后的端到端时间结论。
- neural operator 与 Dang multi-RS 的完整成本对比。

这些 timing claim 必须等 planner integration 或 evaluator 额外记录 `model.predict()` wall-clock 后再写。

## 后续含义

不需要改写预注册。当前证据支持三个保守下一步:

1. 保留 no-warm formal failure 作为论文 negative result / ablation。
2. F02.6 若批准, obstacle-summary warm-start 是仍未测试的 practical branch。
3. 若暂不进入 warm-start, 则应优先补 hard-stage curriculum/reward 诊断, 而不是继续增加 open_connector 权重。

## 当前不 claim 的内容

- 不 claim warm-start branch 失败。
- 不 claim PPO 总路线失败。
- 不 claim timing 或 planner integration。
- 不 claim reward/curriculum 的唯一修复方向。
