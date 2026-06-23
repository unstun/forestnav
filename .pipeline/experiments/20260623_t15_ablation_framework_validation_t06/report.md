# T15 消融实验框架报告

## 人话结论

- 本次登记 30 个消融变体，其中 25 个已真实运行，5 个只登记为后续重切数据/重提特征任务。
- 已运行部分覆盖 A1/A2/A3/A4/A5/A6/A7/A8 的主框架；A1 曲率边界标签、A4 64-ray、A5 非 8m L_max 仍不能当成论文最终数字。
- 所有已运行变体都复用 T14 query/evaluation 逻辑；差别只来自模型、特征、k、序列、回退或噪声开关。

## 输出文件

- `ablation_manifest.csv`: 所有 A1-A8 变体与是否可运行。
- `ablation_summary.csv`: 每个已运行变体按 Easy/Complex/Extreme 汇总。
- `ablation_run_index.csv`: 每个变体对应的子目录和报告。

## 需要后续补强

- A1_curvature_boundary_relabel_required: planned_relabel_required；需要从 teacher path 重切曲率边界标签并重建 KNN/MLP；本次框架先登记，不伪造结果。
- A4_ray64_reextract_required: planned_feature_reextract_required；T08 特征文件只有 32 rays；64 rays 需要从地图和样本位姿重提特征。
- A5_lmax4_relabel_required: planned_relabel_required；需要从 teacher path 以 L_max=4m 重切标签并重建模型。
- A5_lmax6_relabel_required: planned_relabel_required；需要从 teacher path 以 L_max=6m 重切标签并重建模型。
- A5_lmax12_relabel_required: planned_relabel_required；需要从 teacher path 以 L_max=12m 重切标签并重建模型。

## Extreme 快速查看

| group | variant | feasible | median_time_s | reduction_vs_vanilla | f2 | f3 |
|---|---|---:|---:|---:|---:|---:|
| A1 | A1_greedy_rs_current | 0.9000 | 0.3604 | 0.6092 | 0.7000 | 0.1000 |
| A1 | A1_bottleneck_waypoint_proxy | 0.9000 | 0.8805 | 0.0379 | 0.0000 | 0.0000 |
| A1 | A1_voronoi_waypoint_proxy | 1.0000 | 0.6859 | 0.2529 | 0.0000 | 0.0000 |
| A2 | A2_knn_k20 | 0.9000 | 0.3568 | 0.6155 | 0.7000 | 0.1000 |
| A2 | A2_mlp | 0.9000 | 0.5994 | 0.3475 | 0.9000 | 0.4000 |
| A3 | A3_k1 | 0.9000 | 0.4378 | 0.5004 | 0.9000 | 0.2000 |
| A3 | A3_k3 | 0.9000 | 0.3593 | 0.5907 | 0.9000 | 0.1000 |
| A3 | A3_k5 | 0.9000 | 0.3572 | 0.6031 | 0.9000 | 0.1000 |
| A3 | A3_k20 | 0.9000 | 0.3433 | 0.6072 | 0.7000 | 0.1000 |
| A4 | A4_full41 | 0.9000 | 0.3420 | 0.6088 | 0.7000 | 0.1000 |
| A4 | A4_no_density | 0.9000 | 0.4633 | 0.4706 | 0.7000 | 0.1000 |
| A4 | A4_no_heading_delta | 0.9000 | 0.3236 | 0.6310 | 0.6000 | 0.1000 |
| A4 | A4_ray16 | 0.9000 | 0.3196 | 0.6355 | 0.7000 | 0.3000 |
| A5 | A5_lmax8_current | 0.9000 | 0.3423 | 0.6105 | 0.7000 | 0.1000 |
| A6 | A6_adaptive | 0.9000 | 0.3410 | 0.6117 | 0.7000 | 0.1000 |
| A6 | A6_fixed4 | 0.9000 | 0.4893 | 0.4571 | 0.5000 | 0.4000 |
| A6 | A6_fixed8 | 0.9000 | 0.3418 | 0.6100 | 0.7000 | 0.1000 |
| A7 | A7_full_fallback | 0.9000 | 0.3418 | 0.6107 | 0.7000 | 0.1000 |
| A7 | A7_no_f1 | 0.9000 | 0.4404 | 0.4979 | 0.9000 | 0.2000 |
| A7 | A7_no_f2 | 0.9000 | 0.5875 | 0.3292 | 0.0000 | 0.7000 |
| A7 | A7_no_f3 | 0.9000 | 0.3585 | 0.6180 | 0.7000 | 0.0000 |
| A8 | A8_noise0 | 0.9000 | 0.3583 | 0.6118 | 0.7000 | 0.1000 |
| A8 | A8_noise01 | 0.9000 | 0.3667 | 0.6018 | 0.6000 | 0.2000 |
| A8 | A8_noise03 | 0.9000 | 0.1341 | 0.8468 | 0.5000 | 0.1000 |
| A8 | A8_noise05 | 1.0000 | 0.1174 | 0.8655 | 0.5000 | 0.0000 |
