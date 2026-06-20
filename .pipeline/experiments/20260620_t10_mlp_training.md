---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
task: T10
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: eb20358+dirty
execution_host: ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
---

# T10 MLP 消融模型训练报告

## 结论

- 训练状态: `pass`
- 样本数: 100531
- 训练/验证划分: 90478 / 10053
- 结构: 41 -> 256 -> 256 -> 128 -> 3
- 参数量: 109827
- best_epoch: 31 / epochs_ran: 61
- best_val_loss(normalized MSE): 0.401576
- val RMSE: dx=1.352 m, dy=0.666 m, dtheta=0.181 rad

参数说明：本次继承 T08 数据集，T05 的 `L_min=1.0m` 与 T06 难度切点仍为 `reviewed:false`；因此该 checkpoint 是可复现实验产物，不代表论文参数冻结。

## 训练设置

```text
seed=20260620
batch_size=4096
epochs=200
learning_rate=0.001
weight_decay=1e-05
patience=30
device=cuda
loss=PyTorch nn.MSELoss
optimizer=Adam
feature_normalization=train-split z-score
label_normalization=train-split z-score
```

## 产物

- checkpoint: `2_experiment/forest_n3p/models/t10_mlp_subgoal/checkpoint.pt`
- metadata: `2_experiment/forest_n3p/models/t10_mlp_subgoal/metadata.json`
- train log: `2_experiment/forest_n3p/models/t10_mlp_subgoal/train_log.csv`
- split indices: `2_experiment/forest_n3p/models/t10_mlp_subgoal/split_indices.npz`
