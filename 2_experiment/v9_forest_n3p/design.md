---
origin: ai+local
reviewed: false
date: 2026-06-12
version: v1.1
status: draft-for-review（待 Dr Sun 审阅，审完后立 Contract v9-forest-n3p）
codename: F-N3P（森林版 N3P，工作名，禁入论文正文）
changelog:
  - v1 (2026-06-12 21:16) 设计会话产出
  - v1.1 (2026-06-12) 信息量增强：问题形式化 / 算法伪代码 / 特征与度量定义 /
    完备性论证 / 指标精确口径 / 相关工作划界 / 术语库对齐。
    D1–D6 决策、红线、Contract 草案数字一字未动。
upstream:
  - 1_survey/2026-06-12_learning-as-planner/n3p-deep-read-notes.md
  - 1_survey/2026-06-12_learning-as-planner/gptpro-novelty-check.md（含主会话核验附注）
  - .pipeline/survey/learning-as-planner.md
  - .pipeline/terminology/terminology.md（F-N3P 术语章节，写作全程对照）
---

# F-N3P 设计文档 v1.1：学习预测子目标序列加速密林 Hybrid A* 全局规划

## 1. 任务定位与红线

- **任务（红线，不可动）**：阿克曼小车（轴距约 0.6 m）在密林先验占据图
  （0.1 m 分辨率，约 30×30 m）上做离线全局规划——整图 + 起终点输入，
  输出整条满足最小转弯半径与完整车体碰撞约束的无碰撞路径。
- **痛点（实测）**：vanilla Hybrid A* 长距离、密障碍下节点扩展数急剧增大，经常超时。
- **方法（本设计）**：学习模块逐步预测"下一个中间位姿"，Hybrid A* 只做
  相邻位姿间的短段搜索并拼接；学习承担长程分解决策，搜索保证段内运动学可行。
- **论文主 claim（查重后收窄）**：面向密集森林先验占据图的 Ackermann 全局规划，
  提出 oracle-supervised subgoal decomposition——预测有序 SE(2) 子目标序列，
  Hybrid A* 在相邻子目标间保证段内运动学与车体碰撞可行性。
  禁写"首次学习子目标 / 首次学习加速 HA* / 首次 waypoint 引导 HA* /
  首次森林 learned subgoal"（均有反例，见查重报告 §5）。

## 2. 设计决策记录（2026-06-12，Dr Sun 拍板）

| # | 决策点 | 选定 | 备注 |
|---|--------|------|------|
| D1 | 序列机制 | **逐步预测**：每步预测下一个连续 SE(2) 子目标，从实际到达位置重新预测 | 放弃缝枚举（A+C 混合）；AI 曾推荐 A+C 并指出 ② 配法的学习难度风险，Dr Sun 知情后选择 N3P 忠实路线 |
| D2 | 输入表示 | **手工特征 + KNN/MLP** | KNN(k=1) 为主模型（返回库中真实位姿，保留 N3P 可行性优点）；MLP 进 ablation |
| D3 | v1 实验范围 | **程序化森林训练 + 未见图 + 真实地图泛化测试** | 查重报告警告"只覆盖程序化森林→增量风险偏高" |
| D4 | 标签主规则 | **解析扩展成功点（N3P 原版规则的序列化）** | 瓶颈规则、曲率边界进 ablation |
| D5 | 旧 DQN 去向 | RL 基线（承接旧代码，对应 N3P 打 HOPE 的角色） | 2026-06-12 方向转换时已定 |
| D6 | learned heuristic HA* baseline | **降为 optional** | 核验发现 GPT Pro 所引 Takahashi ICAPS19 疑似张冠李戴（原文只做 2D grid A*/D*），文献支点待重查 |

## 3. 方法总览与问题形式化

### 3.1 系统流程

```
离线（一次性）                          在线（每个查询）
─────────────────────────────          ─────────────────────────────
①程序化森林批量生成                      当前位姿 p ← 起点
   ↓ (maps/forest.py)                     │
②HA*+RS 全程求解，留成功路径               ├─ 停止判据：RS(p→终点) 无碰可达？
   ↓ (third_party/pathplan)               │     是 → RS 直连终点，拼接输出 ✓
③前向贪心 RS 分段 → 子目标真值串           │     否 ↓
   ↓ (§4.2 标签规则)                      ├─ 特征提取 f(p; 终点, 局部图) (§4.3)
④特征化 → (特征, Δ位姿) 样本库             ├─ KNN 查库 → 下一子目标 g (§4.4)
   ↓                                      ├─ 可行性校验：RS(p→g) 无碰？
⑤KNN 库构建 / MLP 训练                    │     否 → fallback 阶梯 (§4.6)
                                          ├─ 段内 HA*（解析扩展优先）连 p→g
                                          └─ p ← g，逐步循环（步数上限 K_max）
```

学习模块只回答一个问题："站在当前位姿、目标在那边、局部树障长这样——
**下一个该到达的中间位姿在哪**"。与 N3P 的"预测一个准备位姿"逻辑一致，
区别是逐步调用形成序列。

### 3.2 问题形式化

**环境**。工作区 $W \subset \mathbb{R}^2$ 按分辨率 $r = 0.1$ m 离散为栅格集 $G$，
先验占据图为 $\mathcal{M}: G \to \{0,1\}$，取 1 表示树障占据；
占据区域记 $\mathrm{Occ}(\mathcal{M}) \subset W$。地图约 30×30 m，离线已知。
"先验"是与 LSP 一类 unknown-environment 工作划界的关键属性（§7.1）。

**车辆**。状态 $\mathbf{x} = (\mathbf{p}, \theta) \in SE(2)$，$\mathbf{p} \in W$。
阿克曼底盘，路径曲率约束 $|\kappa| \le 1/\rho_{\min}$
（$\rho_{\min}$ 由 pathplan 配置锁定，文中不出现裸数字）；
车体足迹 $B(\mathbf{x}) \subset \mathbb{R}^2$ 以双圆模型覆盖（轴距约 0.6 m）。

**自由空间与可行路径**。
$X_{\mathrm{free}} = \{\mathbf{x} \in SE(2) : B(\mathbf{x}) \cap \mathrm{Occ}(\mathcal{M}) = \emptyset\}$。
可行路径 $\tau: [0,1] \to X_{\mathrm{free}}$，分段光滑、曲率处处合规、
允许有限次方向切换。

**规划查询**。$q = (\mathcal{M}, \mathbf{x}_s, \mathbf{x}_g)$，
求可行 $\tau$ 使 $\tau(0)=\mathbf{x}_s$、$\tau(1)=\mathbf{x}_g$。
求解质量两维：搜索代价（规划时间 $T$、节点扩展数 $E$）与
路径质量（长度、方向切换、最小净空）。痛点：vanilla HA* 的 $E$
随距离与障碍密度急剧增长（实测，§1）。

**RS 记号**。$RS(\mathbf{x}, \mathbf{x}')$ 为连接两位姿的最短 Reeds-Shepp 曲线，
按构造满足曲率约束，可行性只剩无碰一项：
$RS_{\mathrm{free}}(\mathbf{x}, \mathbf{x}') \Leftrightarrow$ 该曲线全程位于
$X_{\mathrm{free}}$（实现为沿曲线按 $r$ 级步长采样做双圆碰撞检查）。

### 3.3 子目标分解与学习目标

**子目标分解**。给定 $q$，求有序子目标序列 $(g_1, \dots, g_K)$，$g_i \in X_{\mathrm{free}}$，
使相邻对 $(g_i, g_{i+1})$ 段内可被低代价连接（理想情形 $RS_{\mathrm{free}}$ 直连，
一般情形预算 $N_{\mathrm{seg}}$ 内的短段 HA*）。整条路径
$\tau = \tau_0 \oplus \tau_1 \oplus \cdots \oplus \tau_K$（$\oplus$ 为拼接）。

**学习目标**。一步预测器 $\pi: \mathbb{R}^{41} \to \mathbb{R}^3$（实现为 KNN 查表）：
输入特征 $\mathbf{f}(\mathbf{x}; \mathbf{x}_g, \mathcal{M})$，
输出车体系相对位姿 $\hat{\Delta} = (\Delta x, \Delta y, \Delta\theta)$；
世界系子目标 $\hat{g} = \mathbf{x} \oplus \hat{\Delta}$（$\oplus$ 此处为 SE(2) 复合）。
序列由逐步展开生成：$g_{i+1} = g_i \oplus \pi(\mathbf{f}(g_i))$。

**监督来源**。教师路径（vanilla HA*+RS 成功解）经 Algorithm 1 切分出
$(\mathbf{f}(g_i), \Delta_i)$ 样本对——标签由规划器自产、零人工标注，
这是主 claim 中 oracle-supervised 限定语的全部含义，不引申。

### 3.4 符号表

| 符号 | 含义 | 取值/默认 |
|---|---|---|
| $\mathcal{M}, r, W$ | 占据图 / 分辨率 / 工作区 | $r=0.1$ m，约 30×30 m |
| $\mathbf{x}=(\mathbf{p},\theta)$ | SE(2) 状态 | — |
| $\rho_{\min}$ | 最小转弯半径 | pathplan 配置（spike 锁定） |
| $B(\mathbf{x})$ | 车体足迹（双圆模型） | 轴距约 0.6 m |
| $X_{\mathrm{free}}$ | 自由位形空间 | — |
| $RS(\cdot,\cdot),\ RS_{\mathrm{free}}$ | 最短 RS 曲线 / 无碰判定 | — |
| $P, S$ | 教师路径（弧长参数化）/ 总弧长 | — |
| $g_i, K$ | 子目标 / 子目标数 | — |
| $L_{\max}, L_{\min}$ | 段长上界 / 单步推进下界 | 8 m / 1.5 m（pilot 调） |
| $\mathbf{f} \in \mathbb{R}^{41}$ | 手工特征 | §4.3 |
| $\pi, \hat{\Delta}$ | 预测器 / 车体系相对位姿 | KNN(k=1) |
| $\mathcal{D}, N$ | 样本库 / 库规模 | 估算 $1.2 \times 10^5$ |
| $K_{\max}$ | 逐步预测步数上限 | $\lceil 2\|\mathbf{p}_s-\mathbf{p}_g\|/L_{\min} \rceil$ |
| $N_{\mathrm{seg}}$ | 段内节点预算 | 2 000（pilot 调） |
| $R_{\max}, n_{\mathrm{ray}}$ | ray 截断半径 / 方向数 | 10 m / 32 |
| $E, T$ | 节点扩展数 / 规划时间 | 指标（§5.4） |

## 4. 模块详设

### 4.1 场景与教师数据（复用清单，路径已核实存在）

| 组件 | 位置 | 用法 |
|------|------|------|
| 森林场景生成 | `2_experiment/ugv_dqn/maps/forest.py` | 多密度/多种子程序化生成，难度分档见 §5.1 |
| HA*+RS 规划本体（含解析扩展） | `2_experiment/ugv_dqn/third_party/pathplan` | 教师求解 + 在线段内连接，同一实现保证公平 |
| 批量示教管线 | `2_experiment/ugv_dqn/cli/build_baseline_demo_dataset.py`、`forest_expert_dual_baseline.py` | 改造为"成功路径 + 搜索元数据"采集 |
| 真实地图载入 | `2_experiment/ugv_dqn/maps/pgm.py` + 既有 RealMap 资产 | 仅测试，不进训练 |
| 评估框架 | `2_experiment/ugv_dqn/cli/benchmark_baselines.py`、`metrics.py` | 扩展指标列 |
| 双圆碰撞 + 前向仿真 | `2_experiment/ugv_dqn/forest_policy.py` | RS 曲线碰撞校验复用 |
| 旧 MD-DQN | `2_experiment/ugv_dqn/agents.py` | RL 基线 rollout |

**采集协议**（v1.1 细化）：每条教师求解记录
{地图种子与难度参数, $\mathbf{x}_s, \mathbf{x}_g$, 成功标志, 路径 $P$,
节点扩展数, 求解时间, 解析扩展命中位置}。
失败查询保留计数（教师成功率本身是场景难度的校准量），但不产标签。

**工程确认项（实现前 spike）**：pathplan 是否暴露独立的 RS steer + 碰撞检查接口
（标签提取与可行性校验需要脱离完整 HA* 调用）。

### 4.2 标签提取：前向贪心 RS 可达分段（D4 规则的序列化定义）

N3P 原版：成功路径中"解析 RS 段的起点"= 准备位姿真值（单瓶颈，一个标签）。
森林长距离有多瓶颈，序列化定义如下：

```
Algorithm 1  前向贪心 RS 可达分段（标签提取）
输入: 教师路径 P:[0,S]→X_free（弧长参数化, P(0)=x_s, P(S)=x_g）
输出: 子目标真值串 (g_1,…,g_K) 与样本集 {(f(g_i), Δ_i)}
 1: g_0 ← P(0);  s_0 ← 0;  i ← 0
 2: while ¬( RS_free(g_i, x_g) ∧ len(RS(g_i, x_g)) ≤ L_max ):
 3:     S_i ← { s ∈ (s_i, S] : RS_free(g_i, P(s)) ∧ len(RS(g_i, P(s))) ≤ L_max }
 4:     if S_i = ∅ 或 max(S_i) − s_i < L_min:                ▷ 标签失败分支
 5:         失败计数 +1；丢弃整条 P；return ∅
 6:     s_{i+1} ← max(S_i);   g_{i+1} ← P(s_{i+1})           ▷ 取最远 RS 可达点
 7:     Δ_i ← g_{i+1} ⊖ g_i                                  ▷ g_i 车体系下表达
 8:     emit 样本 (f(g_i), Δ_i);   i ← i+1
 9: K ← i      ▷ 终止时剩余段 RS 直连，不产样本（与在线停止判据条件一致）
```

$\ominus$ 表示 SE(2) 相对位姿。逐条说明：

- **语义**：每个子目标都是"从上一子目标出发**一条解析曲线就能到**"的最远点——
  与 N3P"从此处可便宜解"语义一致。
- **构造性质**：对每个 $i$，$RS_{\mathrm{free}}(g_i, g_{i+1})$ 按构造成立。
  推论：教师分布内、静态同图条件下，在线段内连接的解析扩展首次即可命中，
  HA* 仅作保险。逐步预测使实际位姿偏离 $g_i$ 后该性质退化为近似，
  退化程度由子目标可达率量化（§5.4），由可行性校验 + fallback 兜底（§4.6）。
- **$L_{\max}$（默认 8 m）**：防开阔区单段过长、预测任务超出局部特征视距
  $R_{\max}$ 的可见范围。**$L_{\min}$（默认 1.5 m）**：v1.1 起形式化为
  "单步推进下界"（第 4 行）——推进不足即判标签失败，防密集区碎段。
  失败处理策略（弃图 vs 局部放宽 $L_{\max}$ vs 回退瓶颈规则）是开放项（§8.6），
  标签失败率为 pilot 监测指标。
- **样本量**：每条教师路径产出 $K$ 个样本 $(\mathbf{f}(g_i), \Delta_i)$，
  $\Delta_i$ 在 $g_i$ 车体系下表达——特征与标签同系，
  样本对对全局 SE(2) 变换不变，跨地图泛化的前提。
- **复杂度（离线一次性）**：第 3 行的 max 谓词非单调，不能直接二分；
  实现按"自 $s_i$ 起以 $L_{\max}$ 弧长为初始窗口、向远端扫描+按需细化"。
  单条路径成本 $O((S/\Delta s) \cdot c_{RS})$，$\Delta s$ 为扫描步长、
  $c_{RS}$ 为一次 RS 生成 + 碰撞校验成本（约 $\mathrm{len}/r$ 个采样点）；
  可按地图并行。
- **ablation 对照规则**：最窄净空/瓶颈位姿、曲率/换向边界（查重报告 §6 要求的
  teacher label 来源对比，兼做 ablation）。

**已知风险（AI 异议存档，D1 备注）**：此规则的标签落点常在开阔地、由求解器
副产物决定，与局部几何特征的关联弱于瓶颈规则——若 KNN 学不动，
合同内的标签 ablation 会暴露该问题，届时按数据切换主规则（须 Contract v2）。

### 4.3 特征设计（环境抽象——森林版必须重造的部分）

泊车的 4 参数抽象在森林不存在（瓶颈不规则、分布全程）。v1 特征向量
$\mathbf{f} \in \mathbb{R}^{41}$，全部在当前位姿车体系定义，逐维如下：

| 组 | 定义 | 维度 | 说明 |
|----|------|------|------|
| 终点距离 | $f_1 = \log(1 + \|\mathbf{p}_g - \mathbf{p}\|)$ | 1 | log 压缩长程距离 |
| 终点方位 | $(\sin\alpha, \cos\alpha)$，$\alpha$ 为目标在车体系的方位角 | 2 | sin/cos 表示回避角度回绕不连续 |
| 终点朝向差 | $(\sin\Delta\theta_g, \cos\Delta\theta_g)$，$\Delta\theta_g = \theta_g - \theta$ 取主值 | 2 | 终段姿态对齐信号 |
| 净空轮廓 | $f_{5+j} = \log(1+\rho_j)$，$\rho_j = \min(R_{\max},\ \text{自 } \mathbf{p} \text{ 沿车体系方向 } \varphi_j = 2\pi j/n_{\mathrm{ray}} \text{ 至首个占据栅格的距离})$，$j = 0..31$ | 32 | 局部障碍布局的通用描述 |
| 密度统计 | 环带 $[0,2), [2,5), [5,10)$ m 内占据栅格比例 | 3 | 粗粒度拥挤度 |
| 运动学 | 倒车标志 $b \in \{0,1\}$（v1 置 0） | 1 | 预留 |

- **设计依据**：ray-cast 净空轮廓是"无缝枚举版"的局部几何描述——不显式检测
  树缝，但缝在轮廓上表现为相邻方向间的距离峰，KNN 度量可感知。
  这组特征向量就是我方的"环境抽象"（对应 N3P 的 4 参数闭式抽象），
  也是贡献点之一。注意：ray-cast 是先验图上的几何查询，与传感器无关
  （术语库 C-10，黑话高发区）。
- **度量**：训练集逐维 z-score 标准化（$\mu_l, \sigma_l$），
  $d(\mathbf{f}, \mathbf{f}') = \|(\mathbf{f} - \mathbf{f}') \oslash \boldsymbol{\sigma}\|_2$；
  v1 权重均匀，pilot 可上调终点组权重。
- **已知局限**（与 §8.1 风险耦合）：$R_{\max}$ 视距外结构不可见——
  若标签落点超出视距相关性，KNN 召回退化；轮廓对位姿小角度抖动敏感，
  由 log 压缩与标准化部分缓解，由误差容忍 ablation（§5.3）实证。
- **ablation**：±密度组、±终点朝向差、ray 数 16/32/64。

### 4.4 学习模块

- **主模型 KNN(k=1)**：库 $\mathcal{D} = \{(\mathbf{f}_n, \Delta_n)\}_{n=1}^{N}$；
  查询 $\pi(\mathbf{f}) = \Delta_{n^*}$，$n^* = \arg\min_n d(\mathbf{f}, \mathbf{f}_n)$；
  反变换 $\hat{g} = \mathbf{x} \oplus \hat{\Delta}$。
  输出永远是教师数据里真实出现过的相对位姿（保留了 N3P 的特性：KNN 不会产生训练集中不存在的位姿）；
  注意它**不**保证在当前图无碰（样本可能来自他图），在线仍需可行性校验。
- **规模与开销**：库规模估算 2 000 张图 × ~10 查询 × ~6 段 ≈ $1.2 \times 10^5$
  样本，41 维 float32 ≈ 20 MB（N3P 的 KNN 47.8 MB，同量级）。
  KD-tree 构建 $O(N \log N)$；41 维下 KD-tree 查询增益有限（高维退化），
  但即便退化为线性扫描，$1.2 \times 10^5$ 次 41 维距离计算仍在毫秒级，
  不构成瓶颈，实测值进 §5.4 计时。
- **MLP（ablation）**：4 层全连接、~$10^5$ 参数，回归 $\Delta$；已知风险是
  多模态平均——两条可行树缝的样本均值落在缝间树干上——靠可行性校验 +
  fallback 兜底。这与 N3P 中 MLP 偶发不可行的现象相同，论文可对比验证。
- **DQN 打分器不进 v1**（旧偏好已由 Dr Sun 授权放弃，红线只在任务级）。

### 4.5 在线推理循环

```
Algorithm 2  在线逐步推理
输入: 查询 q=(M, x_s, x_g)，样本库 D
输出: 可行路径 τ（方法解或 F3 回退解）
 1: p ← x_s;  τ ← ∅;  K_max ← ⌈2‖p_s−p_g‖/L_min⌉
 2: for step = 1..K_max:
 3:     if RS_free(p, x_g):  return τ ⊕ RS(p, x_g)          ▷ 停止判据
 4:     ĝ ← p ⊕ π(f(p))                                     ▷ KNN 预测 + 反变换
 5:     if ¬RS_free(p, ĝ):  ĝ ← F1(p)                       ▷ 第 2..k 近邻重试
 6:     if F1 全失败:  转 F2/F3（§4.6）
 7:     τ_seg ← HA*(p → ĝ | 解析扩展优先, 预算 N_seg)        ▷ 段内连接
 8:     if τ_seg 失败:  转 F2/F3（§4.6）
 9:     τ ← τ ⊕ τ_seg;   p ← ĝ
10:     if ‖p − p_g‖ 连续 2 步不降:  转 F3                   ▷ 无进展哨
11: 转 F3（步数超限）
```

停止判据与标签终止条件一致（都是"RS 可直达"）。
v1 不做输出平滑后处理，与基线公平。

**单查询开销分解**（机制级，实测值由 §5.4 计时给出）：

| 环节 | 次数上界 | 单次成本 |
|---|---|---|
| 特征提取 | $K_{\max}$ | $n_{\mathrm{ray}}$ 次栅格步进 $O(R_{\max}/r)$ + 环带统计 $O((R_{\max}/r)^2)$ |
| KNN 查询 | $K_{\max}$ | 上界 $O(d \cdot N)$，实测毫秒级（§4.4） |
| RS 可行性校验 | $k \cdot K_{\max}$ | $O(\mathrm{len}/r)$ 采样碰撞检查 |
| 段内 HA* | $K_{\max}$ | $\le N_{\mathrm{seg}}$ 次扩展；教师分布内典型为解析扩展直中 |
| 末段 RS 直连 | 1 | $O(\mathrm{len}/r)$ |

**与 vanilla 的对照机制**：vanilla HA* 的扩展数随距离与密度急剧增长（实测痛点）；
F-N3P 将其分解为"$K$ 段 × 每段预算 $N_{\mathrm{seg}}$ 的搜索 + 常数级学习开销"。
时间收益来源是这一结构替换——此为机制陈述，不作先验断言，
由 §5.4 指标矩阵实证检验。

### 4.6 Fallback 阶梯（完备性保障 + 论文叙事）

| 级 | 触发 | 动作 |
|----|------|------|
| F1 | RS(p→g) 碰撞 | 取 KNN 第 2…k 近邻重试（k≤5） |
| F2 | F1 全失败 | 段内直接跑 HA*(p→g)，预算 N_seg；仍失败则 HA*(p→goal) 限预算试探 |
| F3 | F2 失败 / 步数超限 / 无进展（到 goal 直线距离连续 2 步不降） | **整题回退 vanilla HA***（N3P 同款兜底，方法退化但不失完备性） |

**完备性论证（v1.1 显式化）**：记预算内 vanilla HA* 可解的查询集为 $Q_v$。
F3 规定方法失败时对原查询整题运行同配置 vanilla HA*，
故 F-N3P 的成功集 $\supseteq Q_v$（前提：F3 的 vanilla 预算与单独运行一致）。
即方法继承 vanilla HA* 的完备性级别——HA* 本身受分辨率与预算限制，
我们不声称更强的完备性，也不声称最优性。

**最坏情况开销**：$T_{\text{F-N3P}} \le T_{\text{overhead}} + T_{\text{vanilla}}$，
其中 $T_{\text{overhead}}$ 为逐步预测阶段全部特征/查询/校验/段内搜索耗时，
受 $K_{\max}$ 与各环节预算约束、有限且可控（§4.5 表）。
代价显式化的意义：fallback 触发率高 ⇒ 时间收益消失 ⇒ 恰为 Contract
失败信号①。

fallback 触发率是正式指标（查重报告 §6 要求），也是 Contract 失败信号之一。

## 5. 实验设计（v1 范围，D3）

### 5.1 场景矩阵与数据划分

- **难度三轴（形式化）**：树密度 $\lambda$（单位面积树数）、
  最窄缝宽与车宽之比 $w_{\min}/w_{\mathrm{veh}}$、起终欧氏距离 $d_{sg}$。
  对应 N3P 的 Easy/Complex/Extreme 难度精神，至少 3×3 桶有效覆盖；
  **各轴切点数值待 pilot 标定**（开放项 §8.7），标定后写入 Contract，
  此处不预设数字。
- **数据划分**：训练 = 程序化森林 ~2 000 张（多密度多种子）；
  验证 = 同分布新种子；
  测试 = ①未见程序化图（同分布）②OOD 密度桶（外推）③真实 SLAM 占据图
  （既有 RealMap 资产，仅测试不训练）。
- **种子纪律**：学习模块 ≥5 训练种子；每桶 ≥100 评测场景；
  报 min/mean/median/P95（N3P 口径）。

### 5.2 Baseline（查重报告底线 + 核验修正）

| Baseline | 角色 | 状态 |
|----------|------|------|
| vanilla HA*+RS | 主对照（含 2D 启发式 DP 预计算计时，N3P 公平口径） | 已有 |
| N3P-style 单中间位姿 | 证明"序列"必要性（K=1 退化版，同特征同模型） | 本方法退化版 |
| Voronoi/skeleton waypoint HA* | 规则分解对照（查重点名：缺它即判增量） | 需实现 |
| hand-crafted 瓶颈规则 waypoint | 证明"学习"必要性（medial-axis 窄道提取） | 需实现 |
| 旧 MD-DQN rollout | RL 基线（对应 N3P 打 HOPE） | 已有，需在 v9 场景分布复评 |
| learned heuristic HA* | optional（文献支点核验失败，D6） | 待文献重查 |

**公平性条款（v1.1 显式化）**：
全部基线共用同一份 pathplan 实现、同一双圆碰撞模型、同一计时协议（§5.5）；
规则 waypoint 基线的 waypoint 间连接同样使用段内 HA*——
把"分解点来自哪里"隔离为唯一自变量；
RL 基线计时口径单独定义（沿 N3P：逐步出动作直到可接 RS）。

### 5.3 Ablation

标签规则（解析分段 vs 瓶颈 vs 曲率边界）；KNN vs MLP；k 值；
特征组消融（±密度组、±终点朝向差、ray 数 16/32/64）；$L_{\max}$；
子目标数固定 vs 可变；fallback 阶梯逐级关闭；
误差容忍（对 $\hat{g}$ 加噪声看鲁棒性）。

### 5.4 指标精确定义（查重报告 §6 全集）

| 指标 | 定义与口径 | 出处 |
|---|---|---|
| 规划总时间 $T$ | 收到查询至返回路径的 wall-clock，含 2D 启发式 DP 预计算、特征提取、KNN 查询、可行性校验、全部搜索与 fallback | N3P 公平口径 |
| 节点扩展数 $E$ | 该查询全部 HA* 调用的扩展数之和（含 F2/F3） | N3P 口径 |
| 成功率 SR | 预算内返回无碰可行路径的查询比例 | 查重 §6 |
| 路径长度 | $\mathrm{len}(\tau)$；膨胀率 $= \mathrm{len}(\tau)/\mathrm{len}(\tau_{\mathrm{vanilla}}) - 1$，**仅在双方均成功的查询集上比较**，并同时报告各自 SR | 查重 §6 |
| 曲率/方向切换 | 方向切换次数（N3P 口径）+ 平均绝对曲率 | N3P |
| 最小净空 | $\min_{\mathbf{x} \in \tau} \mathrm{dist}(B(\mathbf{x}), \mathrm{Occ})$ | 查重 §6 |
| 碰撞违例 | 返回路径上的双圆碰撞计数，应恒 0（sanity check，非比较指标） | 查重 §6 |
| fallback 触发率 | 触发 F1 / F2 / F3 的查询比例，分级报告 | 查重 §6；Contract 失败信号① |
| 子目标可达率 | 逐步预测各步 $RS_{\mathrm{free}}(\mathbf{p}, \hat{g})$ 首验通过的比例（按步统计） | 查重 §6 |
| OOD / 真实图性能 | 上述全部指标在 OOD 密度桶与真实 SLAM 图上的复测 | 查重 §6 |

### 5.5 计时与统计协议（v1.1 新增）

- **计时**：单线程、同机、负载隔离；2D 启发式 DP 预计算按 N3P 口径
  计入每次查询总时长；学习方开销（特征/KNN/校验）全部计入——
  不允许出现"裸搜索时间"对比。
- **统计**：≥5 学习种子 × 每桶 ≥100 场景；主表报 median 与 P95，
  附 min/mean；种子间报中位数与极差。
- **显著性检验（建议项，草案）**：逐查询配对 Wilcoxon 符号秩检验（时间），
  bootstrap 置信区间（成功率差）——是否纳入由 Dr Sun 立约时定夺，
  不在 v1.1 锁定。

## 6. 与 N3P 逐项对比

| 维度 | N3P（泊车，ITSC 2026） | F-N3P（本设计） | 同/异 |
|------|------------------------|-----------------|-------|
| 任务 | 泊车：终点附近单瓶颈机动 | 密林长距离全局规划：全程多瓶颈 | **异（任务结构）** |
| 学习预测什么 | 1 个准备位姿 | 有序 SE(2) 子目标串（逐步预测） | **异（结构扩展）** |
| 规划本体 | Hybrid A* + RS | 同（同一份实现） | 同 |
| 标签来源 | 成功路径中解析 RS 段起点 | 同语义的序列化：前向贪心 RS 可达分段 | 同源，**序列化是新定义** |
| 环境抽象 | 4 参数（车道宽/位宽/死端深/类型） | 41 维手工特征（ray-cast 净空轮廓+终点+密度） | **异（森林无低维闭式抽象，必须重造）** |
| 模型 | KNN(k=1) / 4 层 MLP，6 维输入 | KNN(k=1) 主 / MLP ablation，~41 维 | 同哲学 |
| 训练环境 | 简化抽象环境，靠抽象桥接真实 | 直接在程序化森林训练（特征即抽象），真实地图仅测试 | **异（offline-to-online 桥不同）** |
| 可行性保障 | KNN 输出必为真实位姿；MLP 失败回退 HA* | 同 + 三级 fallback 阶梯（F1 近邻重试/F2 段内 HA*/F3 整题回退） | 同源，扩展 |
| 停止/终段 | 固定三阶段，终段解析入位 | RS 可直达即收尾（与标签终止条件一致） | 同语义 |
| 实验纪律 | 公平计时、3 难度×3 任务、多指标、双版本 RL 基线 | 全盘继承 + 多种子 + OOD 桶 + 真实地图 + 规则分解基线 | 同 + 加严 |
| 已知短板 | 未报多种子/方差；抽象斜死端次优 | 多种子补上；特征抽象的失效模式靠 ablation 暴露 | 我们做得更满 |
| 审稿防线 | —— | 必引划界：N3P、Waypoints Hybrid B*（Bonetti）、LSP（Stein）、Banzhaf；禁五类"首次" claim | 查重报告 §5/§7 |

一句话：**规划本体、标签哲学、简单模型、fallback 全部继承 N3P；
"单位姿→序列"的机制、森林环境抽象、分段标签的序列化定义、
以及面向审稿的基线/泛化矩阵是我们的增量。**

## 7. 相关工作与引用划界（v1.1 新增；来源：查重报告 + 主会话核验附注 + 文献库）

> 核验状态标记：✅ 已核验（实开网页/已精读）；⚠️ 存在性已核验但细节未读，
> 论文引用前必须走引用核查四步（paper-writing.md）；❌ 支点失效。
> 本节内容只可作为写作线索，引用以核验后的原文为准（硬规则 #8/#19）。

### 7.1 三角防线（最危险近邻，必引必划界）

**N3P**（xue2026n3p，✅ 已精读，本地 PDF/MD）。
学习单个 preparatory pose，把泊车分解为准备—接近—入位三阶段，HA* 消费；
其摘要口径报告超过 80% 的计算提速。
划界三点：单位姿 → 有序序列；泊车终点附近单瓶颈 → 森林全程多瓶颈；
4 参数闭式抽象 → 41 维手工特征。
引用姿态是"继承并扩展"——标签自监督、KNN 哲学、公平计时纪律均承自该文，
不回避、不贬低。

**Waypoints Hybrid B* / Roadmap Hybrid A***（Bonetti2023_WaypointsHybrid，
✅ 存在性核验，PDF 待读）。
topological map 生成 waypoints 引导搜索，car-like 车辆、工业窄通道。
划界两点：waypoint 来自规则/拓扑图 vs 我方学习预测；
结构化通道 vs 非结构化树缝。
注意：算法名是 Waypoints Hybrid **B\***（查重报告正文笔误为 A*，核验附注已纠）。
该文同时是"规则分解基线"（§5.2 第 3 行）的文献依据。

**LSP, Learned Subgoal Planner**（Stein2018_LearnedSubgoal，
✅ 存在性核验：CoRL 2018, PMLR v87；⚠️ "random forests / RC car"实验细节
未核验，引用前须精读正文）。
学习 subgoal/frontier 属性（dead-end 概率），服务 unknown-environment
高层导航决策。
划界三点：未知环境探索决策 vs 已知先验图全局运动规划；
二分类可达性估计 vs SE(2) 连续回归序列；无 HA* 段内运动学连接。

### 7.2 相邻家族（一句话划界，建议引用）

- **Banzhaf2019_LearnedPoses**（✅ spot-check 通过，摘要原文
  "reduces the computation time by up to an order of magnitude"）：
  学 pose samples 喂 Bi-RRT*——informed sampling vs 我方有序子目标分解，
  消费方也不是 HA*。
- **Ichter2017_LearnedSampling**（✅ 已入库，PDF 待读）：CVAE 学采样分布——
  回答"在哪采样"，我方回答"按什么顺序去哪"。
- **MPNet / Dynamic MPNet / MPC-MPNet、Sub-Goal Trees**（⚠️ 未入库，
  报告级线索）：神经网络出整条路径或递归中间状态——连接器是 sampling/MPC
  而非 HA*，不面向森林 tree-gap。引用前须核验入库。
- **learned heuristic 路线**（SaIL / Neural A* ⚠️ 未入库；
  Takahashi ICAPS19 ❌ 支点失效，D6）：改启发式让单次全局搜索更准 vs
  我方把长问题分解成多段短问题。D6：optional baseline，文献支点重查后再定。
- **Traversability HA***（Mujahed2019_TraversabilityHybridAStar，
  ⚠️ venue/作者未核验）："HA* 进越野"本身不是新点——
  我方贡献不在场景而在 learned decomposition，引用作背景区分。
- **HRL subgoal（HIRO/HAC）**（⚠️ 未入库）：术语相邻而已——
  policy 学习的内部机制 vs 规划器消费的显式子目标；简短提及，不作 baseline。

### 7.3 经典背景与引用缺口

- **Hybrid A* 原始文献**（Dolgov2010_HybridAStar，✅ CrossRef 核验 +
  主会话 spot-check：IJRR 29(5):485-501, DOI 10.1177/0278364909359210；
  另有 2008 AAAI Workshop 版 WS-08-10，无独立 DOI）与
  **Reeds & Shepp 1990**（Reeds1990_OptimalPaths，✅ MSP+CrossRef 双源核验：
  Pacific J. Math. 145(2):367-393, DOI 10.2140/pjm.1990.145.367）：
  已入 `.pipeline/literature/index.md`，PDF 待下载。
- **五禁 claim 重申**（查重报告 §5）：首次学习子目标 / 首次学习加速 HA* /
  首次 waypoint 引导 HA* / 首次森林 learned subgoal / 首次越野农业 HA*——
  均有反例，论文任何位置不得出现。
- **引用纪律**：本节所有 ⚠️ 条目进论文前必须走引用核查四步；
  失败标 `[CITATION NEEDED]`，严禁凭记忆生成 BibTeX。

## 8. 风险与开放问题

1. **标签-特征关联弱（最大技术风险，D1/D4 已知情接受）**：解析分段点落在
   开阔地，局部特征区分度可能不足 → KNN 近邻召回的 Δ位姿不适配当前局面。
   监测指标：训练集内 leave-one-map-out 的子目标可达率 <80% 即预警。
2. **逐步预测的分布漂移**：预测偏差使后续状态偏离教师分布。缓解：F1-F3 兜底 +
   可达率指标；恶化时考虑 DAgger 式二轮采集（v2，不进 v1）。
3. **稀疏图退化**：瓶颈少时方法收益趋零（RS 直达即收尾）——诚实边界，
   论文按密度分桶呈现而非掩盖。
4. **真实地图域差**：程序化树障 vs SLAM 噪声栅格。v1 仅测试不训练，
   差距过大时上数据增强（噪声/膨胀扰动，v2）。
5. **工程确认项**：pathplan 的 RS steer 独立接口；RealMap 资产清点。
6. **$L_{\min}$ 失败分支策略（v1.1 形式化引出）**：Algorithm 1 第 4–5 行
   当前定义为"弃整条教师路径"；备选（局部放宽 $L_{\max}$、该段回退瓶颈规则）
   由 pilot 的标签失败率数据决定。
7. **难度分桶切点（v1.1 显式化）**：$\lambda$、$w_{\min}/w_{\mathrm{veh}}$、
   $d_{sg}$ 的档位数值待 pilot 标定，标定结果写入 Contract 后冻结。

## 9. Contract 草案要素（待设计稿过审后正式立约 .pipeline/contracts/v9-forest-n3p.md）

- **Hypothesis（草案）**：在 Complex/Extreme 难度桶，F-N3P 相对 vanilla HA*
  median 规划时间缩减 ≥50%、成功率不降（≥-2 pp）、路径长度膨胀 ≤5%；
  且相对最强规则分解基线（Voronoi waypoint HA*）在 hard 桶帕累托不劣。
- **Success signal（草案）**：上述三条在未见程序化图与真实地图上同时成立，
  ≥5 种子中位数达标。
- **Failure signal（独立定义，草案）**：任一成立——
  ①fallback 触发率 >30% 且时间收益消失；
  ②OOD 桶成功率相对 vanilla HA* 跌 >5 pp；
  ③与 hand-crafted 瓶颈规则 waypoint 无显著差异（学习模块不必要）；
  ④真实地图时间收益 <20%。
- 数字均为草案，由 Dr Sun 在立约时锁定。

## 10. 下一步

1. Dr Sun 审 v1.1 设计稿（HTML）→ 修订 → 设计定稿
2. 立 Contract v9-forest-n3p（status: approved 后才动实验代码）
3. 阶段 0：工程 spike（RS 接口 + 标签管线 + 标签质量 pilot + 难度切点标定）
4. 写作期全程对照 `.pipeline/terminology/terminology.md`（F-N3P 章节）

## 附录 A. 高危术语速查（完整表见 .pipeline/terminology/terminology.md）

| 一旦写出 | 改为 | 错误性质 |
|---|---|---|
| 随机森林（指场景） | 程序化生成森林 | 撞 random forest 分类器名 |
| 激光雷达/LiDAR（指特征） | ray-cast 净空轮廓 | 无传感器环节，事实错误 |
| 检索增强/RAG | KNN(k=1) 回归 | 机制描述错误 |
| 滚动时域/receding horizon/自回归滚动预测 | 逐步子目标预测 | 撞 MPC 专名 / AI 造词 |
| waypoint（指我方输出） | SE(2) 子目标 | subgoal/waypoint/preparatory pose 三分 |
| Dubins 曲线 | Reeds-Shepp 曲线 | 不含倒车，另一种曲线 |
| Waypoints Hybrid A* | Waypoints Hybrid B* | 引用名错误（核验附注） |
| 概率完备 | 完备性（继承 vanilla 级别） | sampling planner 专义 |
| 语义特征/嵌入/表征 | 手工特征 | 无语义模块 |
| 首次…（五类） | 删除，改具体差异陈述 | 查重 §5 五禁 |
