from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


TARGET_INDICES = tuple(range(0, 5))
RAY32_INDICES = tuple(range(5, 37))
DENSITY_INDICES = tuple(range(37, 40))
MOTION_INDICES = (40,)
FULL41_INDICES = tuple(range(41))


@dataclass(frozen=True)
class AblationVariant:
    group_id: str
    group_name: str
    variant_id: str
    variant_name: str
    method: str
    status: str = "implemented"
    evidence_level: str = "framework_run"
    k_neighbors: int = 20
    knn_feature_indices: tuple[int, ...] | None = None
    max_steps_override: int | None = None
    enable_f1: bool = True
    enable_f2: bool = True
    enable_f3: bool = True
    prediction_noise_sigma_m: float = 0.0
    notes: str = ""

    @property
    def runnable(self) -> bool:
        return self.status == "implemented"

    def manifest_row(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["knn_feature_indices"] = (
            ",".join(str(index) for index in self.knn_feature_indices)
            if self.knn_feature_indices is not None
            else ""
        )
        payload["runnable"] = self.runnable
        return payload


def feature_indices_for_variant(name: str) -> tuple[int, ...]:
    if name == "full41":
        return FULL41_INDICES
    if name == "no_density":
        return (*TARGET_INDICES, *RAY32_INDICES, *MOTION_INDICES)
    if name == "no_heading_delta":
        return (0, 1, 2, *RAY32_INDICES, *DENSITY_INDICES, *MOTION_INDICES)
    if name == "ray16":
        return (*TARGET_INDICES, *(5 + 2 * idx for idx in range(16)), *DENSITY_INDICES, *MOTION_INDICES)
    raise ValueError(f"unsupported feature variant: {name}")


def default_t15_variants() -> tuple[AblationVariant, ...]:
    return (
        AblationVariant(
            "A1",
            "标签规则",
            "A1_greedy_rs_current",
            "当前贪心 RS 分段标签",
            "f_n3p_knn",
            notes="T08/T09 当前主库，标签来自 greedy reachable RS segmentation。",
        ),
        AblationVariant(
            "A1",
            "标签规则",
            "A1_bottleneck_waypoint_proxy",
            "瓶颈位姿几何代理",
            "bottleneck_waypoint",
            evidence_level="proxy_framework_run",
            notes="几何瓶颈 waypoint 代理，不等价于用瓶颈标签重训 KNN。",
        ),
        AblationVariant(
            "A1",
            "标签规则",
            "A1_voronoi_waypoint_proxy",
            "Voronoi/边界几何代理",
            "voronoi_waypoint",
            evidence_level="proxy_framework_run",
            notes="现有 Voronoi waypoint 代理曲率/边界类几何规则；论文最终需单独实现 curvature-boundary labels。",
        ),
        AblationVariant(
            "A1",
            "标签规则",
            "A1_curvature_boundary_relabel_required",
            "曲率边界标签",
            "",
            status="planned_relabel_required",
            evidence_level="manifest_only",
            notes="需要从 teacher path 重切曲率边界标签并重建 KNN/MLP；本次框架先登记，不伪造结果。",
        ),
        AblationVariant("A2", "模型", "A2_knn_k20", "KNN k=20", "f_n3p_knn"),
        AblationVariant("A2", "模型", "A2_mlp", "MLP 回归器", "mlp", k_neighbors=1),
        AblationVariant("A3", "KNN k 值", "A3_k1", "KNN k=1", "f_n3p_knn", k_neighbors=1),
        AblationVariant("A3", "KNN k 值", "A3_k3", "KNN k=3", "f_n3p_knn", k_neighbors=3),
        AblationVariant("A3", "KNN k 值", "A3_k5", "KNN k=5", "f_n3p_knn", k_neighbors=5),
        AblationVariant("A3", "KNN k 值", "A3_k20", "KNN k=20", "f_n3p_knn", k_neighbors=20),
        AblationVariant(
            "A4",
            "特征组",
            "A4_full41",
            "完整 41 维特征",
            "f_n3p_knn",
            notes="使用预建 T09 KNN 库。",
        ),
        AblationVariant(
            "A4",
            "特征组",
            "A4_no_density",
            "去掉密度统计",
            "f_n3p_knn",
            knn_feature_indices=feature_indices_for_variant("no_density"),
        ),
        AblationVariant(
            "A4",
            "特征组",
            "A4_no_heading_delta",
            "去掉终点朝向差",
            "f_n3p_knn",
            knn_feature_indices=feature_indices_for_variant("no_heading_delta"),
        ),
        AblationVariant(
            "A4",
            "特征组",
            "A4_ray16",
            "16 条射线距离剖面",
            "f_n3p_knn",
            knn_feature_indices=feature_indices_for_variant("ray16"),
        ),
        AblationVariant(
            "A4",
            "特征组",
            "A4_ray64_reextract_required",
            "64 条射线距离剖面",
            "",
            status="planned_feature_reextract_required",
            evidence_level="manifest_only",
            notes="T08 特征文件只有 32 rays；64 rays 需要从地图和样本位姿重提特征。",
        ),
        AblationVariant(
            "A5",
            "段长 L_max",
            "A5_lmax8_current",
            "L_max=8m 当前标签库",
            "f_n3p_knn",
            notes="T08 当前库的标签参数为 L_max=8m。",
        ),
        AblationVariant(
            "A5",
            "段长 L_max",
            "A5_lmax4_relabel_required",
            "L_max=4m",
            "",
            status="planned_relabel_required",
            evidence_level="manifest_only",
            notes="需要从 teacher path 以 L_max=4m 重切标签并重建模型。",
        ),
        AblationVariant(
            "A5",
            "段长 L_max",
            "A5_lmax6_relabel_required",
            "L_max=6m",
            "",
            status="planned_relabel_required",
            evidence_level="manifest_only",
            notes="需要从 teacher path 以 L_max=6m 重切标签并重建模型。",
        ),
        AblationVariant(
            "A5",
            "段长 L_max",
            "A5_lmax12_relabel_required",
            "L_max=12m",
            "",
            status="planned_relabel_required",
            evidence_level="manifest_only",
            notes="需要从 teacher path 以 L_max=12m 重切标签并重建模型。",
        ),
        AblationVariant("A6", "序列策略", "A6_adaptive", "自适应子目标步数", "f_n3p_knn"),
        AblationVariant(
            "A6",
            "序列策略",
            "A6_fixed4",
            "固定最多 4 个子目标步",
            "f_n3p_knn",
            max_steps_override=4,
        ),
        AblationVariant(
            "A6",
            "序列策略",
            "A6_fixed8",
            "固定最多 8 个子目标步",
            "f_n3p_knn",
            max_steps_override=8,
        ),
        AblationVariant("A7", "回退阶梯", "A7_full_fallback", "F1+F2+F3 全回退", "f_n3p_knn"),
        AblationVariant(
            "A7",
            "回退阶梯",
            "A7_no_f1",
            "关闭 F1 邻居递补",
            "f_n3p_knn",
            enable_f1=False,
        ),
        AblationVariant(
            "A7",
            "回退阶梯",
            "A7_no_f2",
            "关闭 F2 局部 Hybrid A* 补救",
            "f_n3p_knn",
            enable_f2=False,
        ),
        AblationVariant(
            "A7",
            "回退阶梯",
            "A7_no_f3",
            "关闭 F3 全局 Hybrid A* 回退",
            "f_n3p_knn",
            enable_f3=False,
        ),
        AblationVariant("A8", "鲁棒性", "A8_noise0", "预测噪声 sigma=0.0m", "f_n3p_knn"),
        AblationVariant(
            "A8",
            "鲁棒性",
            "A8_noise01",
            "预测噪声 sigma=0.1m",
            "f_n3p_knn",
            prediction_noise_sigma_m=0.1,
        ),
        AblationVariant(
            "A8",
            "鲁棒性",
            "A8_noise03",
            "预测噪声 sigma=0.3m",
            "f_n3p_knn",
            prediction_noise_sigma_m=0.3,
        ),
        AblationVariant(
            "A8",
            "鲁棒性",
            "A8_noise05",
            "预测噪声 sigma=0.5m",
            "f_n3p_knn",
            prediction_noise_sigma_m=0.5,
        ),
    )
