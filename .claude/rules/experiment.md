---
paths: ["2_experiment/**"]
---

# 实验规则

## 硬规则

- MUST:所有训练/推理参数通过 `2_experiment/configs/*.json` 管理,代码改动须新增配置文件。
- MUST:消融实验结束后记录到 `.pipeline/experiments/`。
- MUST:远端训练前必须完整同步代码,严禁未同步就启动远端训练。
- MUST:推理前必须确认 checkpoint 文件正确,不能依赖"默认最新"。
- MUST:SSH 远程执行 conda 必须 `conda run --cwd <项目绝对路径>/2_experiment -n <env> python ...`。

## 环境

| 平台 | 用途 | 说明 |
| ---- | ---- | ---- |
| Mac (Apple Silicon) | 代码开发 / 论文写作 | PyTorch CPU 版,`KMP_DUPLICATE_LIB_OK=TRUE` 已设 |
| Ubuntu (远程 GPU) | 训练 + 推理 | RTX 4090 |

## 常用命令

```bash
PROJ=$HOME/ForestNav; EXP=$PROJ/2_experiment; ENV=<conda_env>

# 训练(后台)
nohup conda run --cwd $EXP -n $ENV python train.py --profile $PROFILE \
  > $EXP/runs/${PROFILE}_$(date +%Y%m%d_%H%M%S).log 2>&1 &

# 推理
conda run --cwd $EXP -n $ENV python infer.py --profile $PROFILE
```

## 阶段顺序

实验推进严格按以下顺序，不可跳步：

1. **Baseline 复现** → 建立可靠锚点
2. **Research Contract** → 锁定 hypothesis + success/failure signals（硬规则 #20）
3. **实验执行** → 对照 Contract 判定结果

## Baseline 复现

- MUST:实验前检查已有数据集和环境文档，不盲目重新下载。
- MUST:复现工作走 sub-agent 执行，主 session 只收结果摘要。
- MUST:复现成功后记录到 .pipeline/experiments/，成为后续实验的锚点。

## 实验前检查

- 检查阶段顺序：baseline 已复现 → Contract 已提交
- 检查 .pipeline/contracts/ 是否有对应的 Research Contract（硬规则 #20）
- 检查数据集是否已存在于已知路径
- 检查环境是否已搭建完成

## Baseline 时效约束

- MUST：每个长期项目须在内部技术文档中显式声明 `baseline_runs` 字段。判定"组件采用/舍弃""最佳结果""超参事实"等下游决策一律以该 baseline 为唯一锚点。
- MUST：一旦新 baseline runs 出现，**当场**作废当前 baseline，**当场**更新内部技术文档（baseline_runs / 组件矩阵 / 最佳结果 / changelog 全套），禁止"等下次归档统一刷"。Why: 延迟更新会导致用旧基线做实验决策、写论文 claim、写报告，产出全部无效需重做。
- MUST：baseline 切换的触发信号——任一即触发：(1) 新建 `2_experiment/runs<YYYYMMDD>_*` 目录且日期晚于当前 baseline；(2) Dr Sun 显式宣告切换；(3) 新 ckpt 时间戳晚于当前 baseline。
- MUST：当场切换的 6 步动作：
  1. 更新 frontmatter `baseline_runs`
  2. 重跑判定流程，组件矩阵 / 最佳结果全表重写
  3. 旧 baseline 已采用清单移入 changelog
  4. v 号递增（patch 或 minor），changelog 记变更摘要
  5. `reviewed: false`，提交 Dr Sun 复核
  6. 同步 `bigmemory/热区/未关闭决策.md` 中的 baseline 决策条目
- MUST：6 步**全部**完成才允许使用新 baseline 做下游决策。Why: 漏任一步即等于"半切换"，下游基于不一致的视图做判断，比不切换更危险。
