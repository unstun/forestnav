# Forest Bucket Visualization Trial

这是 `0_trials/` 下的一次性可视化试跑，非正式实验，不进 `.pipeline`，不可作为 claim 依据。

| bucket | f_n3p speedup vs vanilla | success f/vanilla | path_inflation mean+max | mean direction_switches | F1 trigger rate |
|---|---:|---:|---:|---:|---:|
| Easy | 41.138x | 1.00/1.00 | 0.037+0.202 | 0.500 | 0.60 |
| Complex | 24.013x | 0.90/0.70 | 0.002+0.034 | 0.600 | 0.80 |
| Extreme | 0.867x | 0.80/0.70 | 0.092+0.306 | 1.200 | 0.90 |

按 f_n3p 的平均方向切换次数优先、最大绕路比例次之看，本次倒车/绕路最重的是 Extreme 桶。

## 源码改动清单

本次未修改 `2_experiment/` 源码。
