---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on: .pipeline/experiments/20260704_module2_f03_curriculum_sampler.md
---

# Module2 F03.4 Training Logging / Manifest 记录

## 直观结论

F03.4 已补齐 PPO 训练前的 episode logging 和 manifest 地基。现在每个 RL-RS Gym episode 能落到 CSV，并可通过显式传入 writer 写 TensorBoard scalar；训练产物也有 `training_manifest.json` 写入 config、source hash、checkpoint 列表和命令。

这一步仍然不 claim PPO 已经开始训练，也不 claim warm-start 决策已关闭。它解决的是“之后跑训练时能不能审计每个 episode 和每个 checkpoint”的问题。

## 实现锚点

- 每步 raw metrics 出口: `2_experiment/forest_n3p/rl_rs/env.py:81-112`。
- `AnalyticExpansionStep` 构造时保留 rollout length / clearance / curvature delta: `2_experiment/forest_n3p/rl_rs/env.py:281-301`。
- 新模块: `2_experiment/forest_n3p/rl_rs/training_logging.py`。
- CSV 字段覆盖 curriculum、reward terms、terminal/collision/truncation、rollout length、clearance、curvature rate、timing: `2_experiment/forest_n3p/rl_rs/training_logging.py:16-50`。
- `RlRsEpisodeLoggingWrapper` reset/step/close 和 episode 写入流程: `2_experiment/forest_n3p/rl_rs/training_logging.py:53-91`。
- episode record 聚合 reward、curriculum、telemetry、clearance、curvature: `2_experiment/forest_n3p/rl_rs/training_logging.py:99-158`。
- TensorBoard scalar 写入: `2_experiment/forest_n3p/rl_rs/training_logging.py:169-192`。
- 显式创建 TensorBoard writer helper: `2_experiment/forest_n3p/rl_rs/training_logging.py:195-202`。
- source hash 与 manifest: `2_experiment/forest_n3p/rl_rs/training_logging.py:205-233`。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py`。
- env step info 暴露 raw logging 指标: `2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py:42-50`。
- CSV 写入 curriculum/reward/outcome 字段: `2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py:53-76`。
- TensorBoard writer 注入与 scalar tags: `2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py:79-95`。
- manifest/source hash/checkpoint/command: `2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py:98-115`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py -q
```

失败原因:

```text
ModuleNotFoundError: No module named 'forest_n3p.rl_rs.training_logging'
```

GREEN:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py -q
```

stdout:

```text
4 passed in 0.46s
```

相关测试:

```bash
python -m py_compile \
  2_experiment/forest_n3p/rl_rs/training_logging.py \
  2_experiment/forest_n3p/rl_rs/env.py \
  2_experiment/forest_n3p/rl_rs/__init__.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py \
  2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py \
  2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py -q
```

stdout:

```text
31 passed in 4.03s
```

全量小测试:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
52 passed in 6.71s
```

TensorBoard 真实 writer smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory
from forest_n3p.rl_rs.training_logging import create_tensorboard_writer
with TemporaryDirectory() as tmp:
    writer = create_tensorboard_writer(Path(tmp) / 'tb')
    writer.add_scalar('smoke/value', 1.0, 0)
    writer.close()
    print('tensorboard_smoke_ok')
PY
```

stdout:

```text
tensorboard_smoke_ok
```

## 环境注意

本机 `torch.utils.tensorboard` 直接 import 曾触发 OpenMP runtime 冲突；本次真实 writer smoke 使用 `KMP_DUPLICATE_LIB_OK=TRUE` 后通过。代码层面没有在 wrapper import 时强制 import TensorBoard，只有调用 `create_tensorboard_writer()` 或外部显式传入 writer 时才进入 TensorBoard 路径。这样 CSV logging 是强依赖，TensorBoard 是显式可选依赖。

## 当前不 claim 的内容

- 不 claim PPO 已训练。
- 不 claim F02.6 warm-start checkpoint 已选定。
- 不 claim Gate #3 已通过。
- 不 claim checkpoint 保存 callback 已完成；F03.4 只提供 manifest 写入函数，真正训练脚本/callback 需要 F03.5 或后续 PPO 训练任务接入。
