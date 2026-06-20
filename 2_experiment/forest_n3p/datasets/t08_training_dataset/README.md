---
date: 2026-06-20
status: pass
origin: ai+experiment
reviewed: false
task: T08
contract: .pipeline/contracts/v9-forest-n3p.md
source_head: ffae29b102bfebf6e6580ae292507a5ff1469c6f
execution_host: ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
---

# T08 训练数据集生成报告

## 结论

- 地图数: 2000 / 2000
- 查询数: 80000
- 样本数: 100531，目标约 100000
- 标签失败率: 6.8%
- 验收状态: `pass`

参数说明：本次使用 T05 的 `L_min=1.0m` 和 T06 的密度/距离切点草案；二者 frontmatter 均为 `reviewed:false`，因此本数据集是可复现实验产物，但不是参数冻结声明。若 Dr Sun 修改 T05/T06 参数，需要用同一脚本重跑。

## 实验设置

```text
map_count=2000
queries_per_map=40
seed=20260620
map_size_cells=300x300
resolution_m=0.1
L_max_m=8.0
L_min_m=1.0
teacher_timeout_s=2.5
teacher_wall_timeout_s=4.0
teacher_max_nodes=15000
label_wall_timeout_s=4.0
query_process_wall_timeout_s=12.0
map_generation_wall_timeout_s=120.0
map_job_wall_timeout_s=480.0
distance_bins=[('d08_12', 8.0, 12.0), ('d12_16', 12.0, 16.0), ('d16_20', 16.0, 20.0), ('d20_inf', 20.0, None)]
```

## 总体统计

| 指标 | 数值 |
|---|---:|
| 教师求解成功率 | 69.5% |
| 教师 wall-time 超时数 | 0 |
| 查询子进程 wall-time 超时数 | 0 |
| 标签尝试数 | 55575 |
| 标签成功数 | 51803 |
| 标签失败率 | 6.8% |
| 标签 wall-time 超时数 | 0 |
| 特征数组形状 | [100531, 41] |
| 标签数组形状 | [100531, 3] |
| 教师路径数 | 55575 |
| 教师路径 pose 总数 | 8940545 |

## 难度桶覆盖

| 桶 | 查询数 | 教师成功率 | 标签失败率 | 样本数 | P50教师时间(s) | P95教师时间(s) |
|---|---:|---:|---:|---:|---:|---:|
| Easy | 26680 | 79.8% | 3.4% | 37386 | 0.749 | 2.505 |
| Complex | 26680 | 70.5% | 6.4% | 34183 | 0.977 | 2.505 |
| Extreme | 26640 | 58.1% | 11.9% | 28962 | 1.597 | 2.506 |

## 失败原因

### Teacher

- `timeout`: 24297
- `open_set_exhausted`: 122
- `query_child_error:ValueError:math domain error`: 6

### Label

- `short_progress`: 3513
- `no_reachable_candidate`: 259

## 产物

- `features.npy`: `2_experiment/forest_n3p/datasets/t08_training_dataset/features.npy`
- `labels.npy`: `2_experiment/forest_n3p/datasets/t08_training_dataset/labels.npy`
- `teacher_paths.npz`: `2_experiment/forest_n3p/datasets/t08_training_dataset/teacher_paths.npz`
- `samples.csv`: `2_experiment/forest_n3p/datasets/t08_training_dataset/samples.csv`
- `queries.csv`: `2_experiment/forest_n3p/datasets/t08_training_dataset/queries.csv`
- `maps.csv`: `2_experiment/forest_n3p/datasets/t08_training_dataset/maps.csv`
