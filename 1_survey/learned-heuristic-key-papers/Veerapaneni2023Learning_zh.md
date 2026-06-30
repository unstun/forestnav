---
citation_key: Veerapaneni2023Learning
arxiv_id: 2303.09477
arxiv_url: "https://arxiv.org/abs/2303.09477"
title: "Learning Local Heuristics for Search-Based Navigation Planning"
title_zh: "面向基于搜索的导航规划的局部启发函数学习"
authors_short: "Rishi Veerapaneni et al."
year: 2023
direction_tag: E_bounded_suboptimal_search
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:28:58Z
origin: ai+web
reviewed: false
translation: zh
translated_at: 2026-06-28
---

# 面向基于搜索的导航规划的局部启发函数学习

Rishi Veerapaneni, Muhammad Suhail Saleem, Maxim Likhachev

Carnegie Mellon University 机器人研究所 {rveerapa, msaleem2, mlikhach}@andrew.cmu.edu

## 摘要

用于导航的图搜索规划算法（graph search planning algorithm）通常严重依赖 heuristic（启发函数）来高效规划路径。因此，尽管这类方法无需训练阶段并能直接规划长视距路径，却往往需要精心人工设计信息量丰富的启发函数。近年来已有研究开始用机器学习来学习启发函数，以绕过手工设计的启发函数，从而引导搜索算法。然而，这些方法虽然能从原始输入学习复杂的启发函数，但 i) 需要大量训练阶段，且 ii) 在面对新地图和更长视距路径时泛化能力不足。本文的贡献在于证明：与其学习一个全局代价估计（global cost-to-go heuristic），不如定义并学习局部启发函数（local heuristic），这样能显著降低学习难度并改善泛化能力。实验表明，使用这种局部启发函数能将节点展开次数（node expansions）减少 2 至 20 倍，同时保持有界次优性（bounded suboptimality）保证，且易于训练，能泛化到新地图和长视距规划任务。

## 1 引言

运动规划（motion planning）在自动驾驶、机械臂操控和多智能体仓库自动化等领域有着广泛应用。图搜索（graph search）是一类流行的运动规划方法，其竞争性能通常依赖于精心手工设计的信息性 heuristic（启发函数，即代价到达目标的估计）(2008; 2014; 2015; 2019)。

绝大多数图搜索算法假设已知环境信息（即图结构），以计算搜索算法中有效/无效的节点和边。给定这些转移信息，启发式搜索算法可以直接在地图上工作，无需任何计算代价高昂的预训练阶段。这些方法还能开箱即用地解决长视距任务，无需任何算法改动。此外，启发式搜索算法在充足计算时间下具有完备性（completeness）和有界次优性（bounded suboptimality）的强理论保证。

现代机器学习技术，例如强化学习（reinforcement learning）或模仿学习（imitation learning），则利用来自环境的观测数据来确定路径。这些方法无需手工设计启发函数，能够直接从原始输入中学习复杂的价值函数和/或策略，并在与训练时类似的环境中表现良好。近期研究开始弥合启发式搜索与机器学习之间的鸿沟，通常的做法是学习一个神经网络，输出用于搜索算法（一般是 weighted A\*，加权 A\*）中的启发值或优先级。这些方法相比纯启发式搜索在减少节点展开次数方面有所改善，相比纯机器学习方法在成功率方面也有所提升 (2017; 2019; 2020; 2021; 2022)。然而，大多数方法需要大量训练阶段，缺乏完备性或解质量方面的保证，且难以泛化到长视距任务或新地图。

![](Veerapaneni2023Learning_figs/0768de3158953cd6bd5c283215a04c137fba988680a7e93ba52ce2d5b9d3cf9f.jpg)

![](Veerapaneni2023Learning_figs/e3024baae0f2cdada57b96e26ff2d8d07928c542854034302b6e829b1172e2bb.jpg)

![](Veerapaneni2023Learning_figs/b7412c60a6cb16bcf73d264c052ac0872ee9ddbdbc080e45a1f48ee57a459810.jpg)  
图 1：左图：从红星状态 s 到橙色目标估计全局 cost-to-go（代价到达目标）启发值，需要对大范围区域进行推理。右图：我们定义并学习以 s 为中心的局部启发函数，只对局部区域内的车辆动力学和障碍物进行推理，再将其与全局启发函数组合使用。这一规模大幅缩小的问题降低了学习难度，改善了泛化能力，并在某些场景中带来了显著的性能提升。

我们的目标是融合两种方法的优势：启发式搜索解决长视距任务的能力，以及机器学习利用环境数据的能力。具体来说，我们希望方法能够：1. 利用环境数据提升性能；2. 易于训练；3. 能够泛化到新地图和长视距规划；4. 保持解的完备性和有界次优性保证。我们的核心洞察是：与其学习一个随任务变长而愈发难以训练的全局 cost-to-go 启发函数，不如定义并学习一个局部启发函数。不同于已知所有相关文献（据我们所知）直接预测整个 cost-to-goal 启发值的做法，我们仅预测从当前机器人状态为中心的小区域中逃离所需的代价，使神经网络的学习变得容易（见图 1）。该局部估计与全局启发函数叠加，提供更准确、信息量更丰富的 cost-to-go 估计。我们采用 focal search（焦点搜索，Pearl and Kim 1982），即 $\mathbf{A}^{*}$ 的一个变体，以有界次优性保证的方式使用这一信息性启发函数。我们将这一框架称为 Local Heuristic A\*（局部启发 A\*，简称 LoHA\*），并展示 LoHA\* 如何有效地泛化并提升性能。

![](Veerapaneni2023Learning_figs/89b142312dce9d4d506aa721ed3046b9e8623f07bc485620e2f9a9701f63ba1f.jpg)  
图 2：展示了计算局部启发函数并将其与全局启发函数相加得到组合更强信息性启发函数的效果。全局启发函数 $h_g$ 是忽略障碍物的到目标曼哈顿距离（Manhattan distance），而局部启发函数则对窗口 $K=3$ 内的障碍物进行推理，并对死胡同（cul-de-sac）区域的启发值进行惩罚增大。使用 $h_g + h_k$ 从起点运行 weighted $\mathbf{A}^{*}$，相比仅使用 $h_g$ 会跳过死胡同区域。

简而言之，本文主要贡献如下：

1. 定义独立于全尺度规划问题的局部启发函数 $h_k$，并使用神经网络高效估计其值。

2. 将局部启发函数与全局启发函数组合，并使用 focal search 保持有界次优性。

3. 通过实验证明，在 1024×1024 的大型地图上，学习得到的 9×9 局部启发函数相比普通 weighted $\mathbf{A}^{*}$ 搜索可减少多达 20 倍的节点展开次数，且 LoHA\* 能有效泛化到新地图。

## 2 相关工作

大多数将机器学习与基于搜索的规划相结合的已有工作，都试图直接学习到目标状态的 cost-to-go 启发函数。Agostinelli 等人 (2019, 2021) 使用强化学习在魔方（Rubik's Cube）及其他组合任务（如 24 格拼图、Sokoban）上学习这类函数。Kim 和 An (2020) 在同一张地图上训练和测试全局启发函数。Li 等人 (2022) 付出额外工程代价，令人印象深刻地学习到了一个 admissible（可采纳的）CNN 启发函数，能为格块（tile）和 TopSpin 问题找到最优解。Jabbari Arfaee、Zilles 和 Holte (2011) 是一项早期工作，使用 curriculum learning（课程学习）和小型神经网络在不同经典组合问题（如 3×3 魔方、24 格拼图）上学习全局启发函数。对于所有这些方法，其学习到的启发函数在更长视距的问题或训练分布以外的类似场景（如不同目标状态的魔方，或类似结构但更大的地图）上的表现尚不清晰。本文旨在以可泛化到新地图的方式，通过机器学习加速搜索。

另有一些工作尝试通过学习不同度量指标来加速搜索。Bhardwaj、Choudhury 和 Scherer (2017) 学习搜索状态特征的全局优先级值，以确定展开策略。而我们学习的是基于局部特征的局部启发函数，使我们的方法可跨不同搜索实例（如不同权重）使用。Kaur、Chatterjee 和 Likhachev (2021) 学习了一种 expansion delay heuristic（展开延迟启发函数），能加速搜索，但需要针对新地图重新训练。

我们通过将学习问题限制在"局部"子问题上来实现跨地图的泛化。我们的局部子问题与最优优先搜索（best-first search）中的前瞻（lookahead）（Stern et al. 2010）有些许联系——后者使用固定深度的 DFS 前瞻在 $\mathbf{A}^{*}$ 搜索中更新启发值——但我们的局部启发函数定义以及神经网络的使用方式完全不同。我们的局部定义极大地简化了学习问题，显著减少了所需的训练数据集大小、训练时间和神经网络模型规模，同时使其能够有效泛化到不同地图。

## 3 方法

我们的核心动机直接明了：简化学习问题。学习估计全局 cost-to-go 的启发函数需要对整张地图进行复杂推理。我们的核心洞察是：与其求解完整的最短路径问题，不如定义一个规模小得多的局部子问题，并证明在启发式搜索中利用该局部子问题的解，能够大幅减少整体的节点展开次数。

## 定义局部启发函数

像 $\mathbf{A}^{*}$ 这样的启发式搜索方法对状态进行最优优先搜索，每个状态的优先级 $f(s)$ 等于 cost-to-come（已到达代价）$g(s)$ 与 cost-to-go 估计 $h_g(s)$ 之和。关键在于，$h_g(s)$ 是从状态 s 到达目标状态 $s_g$ 的最优代价的（下界）估计，我们称之为全局启发函数 $h_g(s)$，以区别于我们的局部启发函数 $h_k(s)$。这意味着随着规划问题变得更长/更大，获得准确的 $h_g(s)$ 估计也越来越困难。

我们转而提出学习一个局部启发函数 $h_k(s)$，它充分考虑以 s 为中心、大小为 K 的局部区域内的机器人动力学和环境障碍物信息。从概念上讲，$h_k$ 试图预测逃离该局部区域所需的额外代价。在搜索过程中，我们使用 $h_{gk}(s) = h_g(s) + h_k(s)$（见图 2）。

从数学上讲，给定状态 $\boldsymbol{s} = (x, y, \Omega)$，其中 $x, y$ 是位置，$\Omega$ 是其他状态参数（如航向、速度），我们定义局部区域 $LR(s)$ 为以 $x, y$ 为中心、窗口大小为 K 内的所有状态，即 $LR(s) \stackrel{}{=} \{s' \mid K \geq |s.x - s'.x|, K \geq |s.y - s'.y|\}$。设 $LRB(s)$ 为该区域的边界，即 $\{s' \mid K = |s.x - s'.x| \lor K = |s.y - s'.y|\}$。从概念上讲，假设动作步长为单位长度，任何从 s 到 $s_g$ 的路径都必须包含 $LRB(s)$ 中的某个状态，或者直接在局部区域 $LR(s)$ 内到达目标。如果两者均不可行，则 s 无法离开 $LR(s)$，处于死路中，其启发值应为无穷大。因此，我们的目标值 $h_{gk}(s)$ 为

$$
h_{gk}(s) = \min_{s'} \left\{ \begin{array}{ll} c(s, s') + h_g(s'), & s' \in LRB(s) \\ c(s, s') + 0, & s' = s_g \in LR(s) \\ \infty, & \text{otherwise} \end{array} \right.\tag{1}
$$

注意，计算 $c(s, s')$（从 s 到 $s'$ 路径的最小代价）需要将机器人的动力学/运动学约束以及 $LR(s)$ 中的局部障碍物/环境数据纳入考虑。我们可以通过在给定状态 s 处运行遵循公式 1 的 $\mathbf{A}^{*}$ 来计算 $h_{gk}(s)$，但随着 $LR(s)$ 尺寸增大，这会变得很慢。我们可以改为训练一个神经网络（NN，neural network）来近似估计该值。输入 $s$、$LR(s)$ 中的环境数据和启发值数据，预测 $h_{gk}(s)$。

这种方法的一个关键问题是：尽管我们的问题是局部的，但输入 s 和 $h_g(s')$ 并不是尺度不变的（scale-invariant）。例如，如果我们在小地图上训练，但在更大的地图上评估，神经网络将无法泛化到遇到的更大 s 值和 $h_g$ 值。一个关键观察是，我们可以使输入对此类变化保持不变。状态 $\boldsymbol{s} = (x, y, \Omega)$ 可以简化为只有 $\Omega$，因为局部区域 $LR(s)$ 以 $x, y$ 为中心。我们通过减去 $h_g(s)$ 来消除 $LR(s)$ 中 $s' \in LR(s)$ 的 $h_g(s')$ 对全局尺度的依赖。因此，我们的局部不变启发函数变为

$$
h_k(s) = \min_{s'} \left\{ \begin{array}{ll} (c(s, s') + h_g(s')) - h_g(s), & s' \in LRB(s) \\ (c(s, s') + 0 - h_g(s)), & s' = s_g \in LR(s) \\ \infty, & \text{otherwise} \end{array} \right.\tag{2}
$$

因此，输入神经网络的不再是 $h_g$ 的绝对值，而只需要局部区域内的相对信息 $h_g(s') - h_g(s), s' \in LR(s)$。

对于非单位步长动作，我们可以将此定义推广为预测逃离 $LR(s)$ 所需的额外代价。出于简洁起见，我们省略数学定义，但注意我们的实验使用的正是这个更通用的版本。

## 计算真值 $\mathbf{h_k}$

公式 2 定义了 $LR(s)$ 内的一个多目标搜索问题，目标是最小化 $c(s, s') + h_g(s') - h_g(s)$。我们直接从 s 出发运行 $\mathbf{A}^{*}$ 搜索，直到满足前两个条件之一，或者返回无解（对应第三种 $\infty$ 的情况）。在高维状态空间中，$LR(s)$ 内的状态数量很大，局部搜索可能需要极长时间才能终止。我们可以设置最大展开次数来缓解这一问题，当达到上限时返回队列中 $g(s') + h(s')$ 最小的状态值，这仍然是 $h_k(s)$ 的下估计（underestimate）。

## 训练过程

**神经网络输入：** 如前所述，我们希望向神经网络输入局部不变版本的 s 和 $LR(s)$。$LR(s)$ 包含以 s 为中心、窗口大小为 K 的障碍物信息和不变启发值。

**数据收集：** 我们使用监督学习（supervised learning）来训练模型学习 $h_k$。一种朴素的数据收集方式是随机采样状态 s，但这可能会过度采样运行时不相关的状态空间区域，从而影响性能。因此，我们通过运行使用真值局部启发函数的 weighted $\mathbf{A}^{*}$，并记录搜索过程中遇到的状态 s 对应的输入 $s, LR(s)$ 和真值 $h_k(s)$ 来收集训练数据。

**神经网络输出：** 局部启发函数值 $h_k(s)$。

**损失函数：** 训练神经网络时我们发现，直接回归 $h_k$ 会出现问题，因为均方误差（MSE）目标函数会优先优化大值样本，降低对众多小值样本的预测质量。我们发现一个有效的替代方案是回归 $\log(h_k + 1)$，这是一种相对误差的度量，但比相对误差或其他替代方案有更好的统计性质 (Tofallis 2015)。+1 在数值上是必要的，因为 $h_k$ 可以等于 0。此外，对于 $h_k = \infty$ 的死路情况，我们选择回归到 $h_k = 2K$，实验发现这个值足够大。

## 在搜索中使用局部启发函数

我们使用 $h_{gk}(s) = h_g(s) + h_k(s)$ 作为我们的启发函数。从概念上讲，$h_k$ 用局部动力学和障碍物信息对 $h_g$ 进行增强。如果 $h_k(s)$ 计算准确（例如通过局部搜索），则 $h_{gk}(s)$ 保证是 admissible（可采纳的），可以在 $\mathbf{A}^{*}$ 中使用并保证最优性。然而，如果 $h_k$ 是学习得到的，它可能是任意次优的。因此，我们采用 focal search，将 $h_g$ 作为 OPEN 列表中的 consistent heuristic（一致启发函数），将 $h_{gk}(s)$ 作为 FOCAL 列表中的 inadmissible heuristic（不可采纳启发函数），从而保证我们的解是有界次优的。我们将这一框架——学习局部启发函数、与全局启发函数组合、在 focal search 中使用——称为 Local Heuristic $\mathbf{A}^{*}$，简写为 LoHA\*。

## 4 局部启发函数实验

我们在自定义随机障碍物地图和来自 (Sturtevant 2012) 的 6 张城市地图上进行实验，目标是最小化起点-终点对之间的行驶时间。我们模拟一辆具有状态 $(x, y, \theta, v)$ 的非完整约束（non-holonomic）小车，其中位置 $x, y$ 以 0.5 为步长离散化，航向 $\theta$ 以 30 度为步长离散化，速度 $v \in \{-1, 0, 1, 2, 3\}$。小车遵循 Ackermann（阿克曼）动力学约束，每个状态的单位代价动作包括 $\Delta v \in \{-1, 0, 1\}$ 和转向角 $\in \{-60, -30, 0, 30, 60\}$（度）。由于最大速度为 3，全局启发函数为 $h_g = L_2(s, s_{goal}) / 3$。这一设置的目的是展示局部启发函数在复杂状态空间和动作空间中的帮助，不同于很多将搜索与机器学习结合的现有工作中使用的 4/8 连通网格。我们报告局部启发函数大小 $K=4$ 的实验结果。实验在一台配有 32GB 内存、第 11 代 Intel Core i7-11800H@2.30GHz×16 的 Ubuntu 20.04 机器上运行。

## 训练

**局部状态输入：** 我们将 $LR(s)$ 以以 $(\lfloor x \rfloor, \lfloor y \rfloor)$ 为中心的大小为 $2K+1 \times 2K+1$ 的双通道图像输入。第一通道是二值障碍物地图，第二通道是局部不变启发值 $h_g(s') - h_g(s)$。我们还额外输入包含 $(x - \lfloor x \rfloor, y - \lfloor y \rfloor, \theta, v)$ 的局部不变状态。

**训练数据：** 我们在一组训练地图的随机起点-终点位置上使用带局部启发函数的 weighted $\mathbf{A}^{*}$ 进行搜索，收集遇到过的状态数据。我们将局部启发函数展开上限设为 100 以加快数据收集速度。整个流程速度很快：使用未优化的 C++ 代码，每秒可收集约 5000 个样本。我们在 200,000 个状态上训练（可在几分钟内收集完毕）。需要强调的是，这与学习全局启发函数形成对比——后者的每个训练样本都需要求解整个规划问题，因此数据收集耗时更长。

<table><tr><td rowspan="2">地图类型</td><td rowspan="2">数据集</td><td rowspan="2">方法</td><td colspan="4">节点展开次数减少倍数</td></tr><tr><td>w2</td><td>w8</td><td>w32</td><td>w128</td></tr><tr><td rowspan="4">random20</td><td rowspan="2">训练集</td><td>A* w/TL</td><td>6.76</td><td>10.88</td><td>12.78</td><td>14.7</td></tr><tr><td>LoHA*</td><td>3.53</td><td>7.92</td><td>10.33</td><td>11.6</td></tr><tr><td rowspan="2">测试集</td><td>A* w/TL</td><td>6.6</td><td>10.42</td><td>14.45</td><td>15.75</td></tr><tr><td>LoHA*</td><td>3.57</td><td>6.94</td><td>10.46</td><td>12.67</td></tr><tr><td rowspan="4">random30</td><td rowspan="2">训练集</td><td>A* w/TL</td><td>12.21</td><td>26.3</td><td>40.38</td><td>44.02</td></tr><tr><td>LoHA*</td><td>2.16</td><td>12.07</td><td>18.08</td><td>20.51</td></tr><tr><td rowspan="2">测试集</td><td>A* w/TL</td><td>10.36</td><td>28.58</td><td>43.57</td><td>44.3</td></tr><tr><td>LoHA*</td><td>1.68</td><td>7.71</td><td>13.59</td><td>16.55</td></tr><tr><td rowspan="4">Denver_256</td><td rowspan="2">训练集</td><td>A* w/TL</td><td>2.43</td><td>6.45</td><td>5.92</td><td>7.13</td></tr><tr><td>LoHA*</td><td>1.22</td><td>5.15</td><td>3.98</td><td>6.37</td></tr><tr><td rowspan="2">测试集</td><td>A* w/TL</td><td>4.54</td><td>16.37</td><td>30.73</td><td>29.21</td></tr><tr><td>LoHA*</td><td>1.43</td><td>8.43</td><td>28.16</td><td>30.73</td></tr></table>

表 1：LoHA\* 实验结果——报告相比 weighted A\* 的节点展开次数中位数倍数减少量。可以看出，随着权重 w 增大，LoHA\* 能获得更大的减少倍数，且能够有效泛化到不同地图。

**神经网络架构：** 对 $LR(s)$ 应用卷积层，将潜在向量展平，拼接局部不变状态 s，再经过两个大小为 100 的中间 MLP 层。

**训练时间：** 在 CPU 上以 batch size 32 对 200,000 个样本训练 100 个 epoch，大约需要 20-30 分钟。我们没有专门优化训练速度，但再次强调：局部问题设定使模型更小，对应更低的计算需求（即使用 CPU 而非 GPU，训练耗时分钟级而非小时级）。训练完成后，平方相对损失（squared relative loss）稳定在约 0.03，对应约 18% 的绝对相对误差。

## 实验结果

表 1 报告了在多个加权（weighted）运行下，使用真值局部启发函数的 $\mathbf{A}^{*}$（$\mathbf{A}^{*}$ w/TL）和使用神经网络近似的 LoHA\* 在训练地图和测试地图上的中位数加速倍数。"randomN" 地图是 1024×1024 的地图，其中 N% 的位置随机生成障碍物，分为 7 张训练地图和 3 张测试地图。Denver 地图是 256×256 的地图，分为 2 张训练地图和 1 张测试地图。总体来看，训练/测试集各有约 40/20 个起点-终点对，每个配置运行 3 个随机种子。我们报告相比对应 weighted $\mathbf{A}^{*}$ 基线的节点展开次数中位数减少倍数，例如数值 6.76 表示该方法展开的节点数量是 weighted A\* 的 1/6.76。

"$\mathbf{A}^{*}$ w/TL"的结果揭示了局部启发函数在减少节点展开总量上的价值，根据地图和启发权重 w 的不同，减少倍数在 2 至 40 倍之间。我们看到 $h_{gk}$ 在更大的 w 下更有效；这是因为较大 w 下的节点展开更可能发生在局部最优（local optima）区域，而 $h_{gk}$ 对这些区域的惩罚更大。此外，运行 $\mathbf{A}^{*}$ w/TL 为我们提供了 LoHA\* 所能达到的估计上界，并帮助确定 LoHA\* 不适用的情形。这一能力对实践者很有价值，他们可以事先轻松判断 LoHA\* 对其应用场景是否有效。

LoHA\* 的性能大体上能与真值局部启发函数的量级相匹配。我们注意到，由于 LoHA\* 的神经网络是对真值局部启发函数的噪声近似，一定程度的性能下降是可以预期的，但我们发现这种有噪声的近似在减少节点展开次数方面仍然有效。重要的是，LoHA\* 能够有效泛化到训练时未见过的测试地图。图 3 展示了随着 K 增大，神经网络越来越难以泛化到测试地图，这验证了我们使用局部而非全局启发函数来实现泛化的动机。

![](Veerapaneni2023Learning_figs/6f1957bfbb87eea9b453fd6a2c7e4db61b594e0f3040844d9bbd7aa04f4f9a79.jpg)  
图 3：纵轴为对数相对损失目标；损失值 0.2 大致对应 $\geq 50\%$ 的绝对相对误差，0.1 对应 $\geq 35\%$。随着 K 增大，神经网络越来越难以泛化到测试地图。这支持了我们的动机：学习局部启发函数能简化学习问题并改善泛化能力。

LoHA\* 的一个关键局限性在于：尽管它能显著减少节点展开次数，但其整体运行时间比基线 $\mathbf{A}^{*}$ 更长。这是因为在搜索中运行神经网络速度较慢：LoHA\* 每秒展开约 4,500 个节点（神经网络推理时间占主导），而使用 $h_g$ 的 $\mathbf{A}^{*}$ 每秒展开约 140,000 个节点。我们预计在节点展开代价更高的场景中，或通过在 focal search 中使用 batch expansions（批量展开）或 GPU 优化 (Greco et al. 2022; Li et al. 2022; Veerapaneni and Likhachev 2022)，LoHA\* 能带来实际的运行时收益。这与我们的核心贡献无关，留待未来工作解决。

## 5 未来工作与结论

我们的关键假设是能够围绕智能体状态 s 的物理区域定义一个局部区域，这在导航任务中成立。将其扩展到其他领域，例如机械臂操控，将是有趣的未来工作方向——在那里定义 $LR(s)$ 可能并不简单。如上一节所述，未来工作也可以解决在启发式搜索循环中使用神经网络带来的运行时问题。

本文提出了一个在导航规划的启发式搜索中提取、学习和使用局部启发函数的框架。在 focal $\mathbf{A}^{*}$ 搜索中使用局部启发函数，相比普通 $\mathbf{A}^{*}$ 能显著减少节点展开次数，同时保持有界次优性保证。我们展示了学习局部启发函数能够极大地简化数据收集、学习过程并改善泛化能力，同时将节点展开次数减少 2 至 20 倍。

**致谢** 本研究部分由美国国家科学基金会研究生研究奖学金（Grant No. DGE1745016 和 DGE2140739）资助。

## 参考文献

Agostinelli, F.; McAleer, S.; Shmakov, A.; and Baldi, P. 2019. Solving the Rubik's cube with deep reinforcement learning and search. Nature Machine Intelligence, 1–8.

Agostinelli, F.; Shmakov, A.; McAleer, S.; Fox, R.; and Baldi, P. 2021. A\* Search Without Expansions: Learning Heuristic Functions with Deep Q-Networks. CoRR, abs/2102.04518.

Aine, S.; Swaminathan, S.; Narayanan, V.; Hwang, V.; and Likhachev, M. 2014. Multi-Heuristic A. In Fox, D.; Kavraki, L. E.; and Kurniawati, H., eds., Robotics: Science and Systems X, University of California, Berkeley, USA, July 12-16, 2014.

Bhardwaj, M.; Choudhury, S.; and Scherer, S. A. 2017. Learning Heuristic Search via Imitation. CoRR, abs/1707.03034.

Ferguson, D.; Howard, T. M.; and Likhachev, M. 2008. Motion planning in urban environments: Part II. In 2008 IEEE/RSJ International Conference on Intelligent Robots and Systems, September 22-26, 2008, Acropolis Convention Center, Nice, France, 1070–1076. IEEE.

Greco, M.; Toro, J.; Ulloa, C. H.; and Baier, J. A. 2022. K-Focal Search for Slow Learned Heuristics (Extended Abstract). In Chrpa, L.; and Saetti, A., eds., Proceedings of the Fifteenth International Symposium on Combinatorial Search, SOCS 2022, Vienna, Austria, July 21-23, 2022, 279–281. AAAI Press.

Jabbari Arfaee, S.; Zilles, S.; and Holte, R. C. 2011. Learning heuristic functions for large state spaces. Artificial Intelligence, 175(16): 2075–2098.

Kaur, J.; Chatterjee, I.; and Likhachev, M. 2021. Speeding Up Search-Based Motion Planning using Expansion Delay Heuristics. Proceedings of the International Conference on Automated Planning and Scheduling, 31(1): 528–532.

Kim, S.; and An, B. 2020. Learning Heuristic A: Efficient Graph Search using Neural Network. In 2020 IEEE International Conference on Robotics and Automation (ICRA), 9542–9547.

Li, J.; Felner, A.; Boyarski, E.; Ma, H.; and Koenig, S. 2019. Improved Heuristics for Multi-Agent Path Finding with Conflict-Based Search. In Kraus, S., ed., Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI 2019, Macao, China, August 10-16, 2019, 442–449. ijcai.org.

Li, T.; Chen, R.; Mavrin, B.; Sturtevant, N. R.; Nadav, D.; and Felner, A. 2022. Optimal Search with Neural Networks: Challenges and Approaches. In Chrpa, L.; and Saetti, A., eds., Proceedings of the Fifteenth International Symposium on Combinatorial Search, SOCS 2022, Vienna, Austria, July 21-23, 2022, 109–117. AAAI Press.

Narayanan, V.; Aine, S.; and Likhachev, M. 2015. Improved Multi-Heuristic A\* for Searching with Uncalibrated Heuristics. In Lelis, L.; and Stern, R., eds., Proceedings of the Eighth Annual Symposium on Combinatorial Search, SOCS 2015, 11-13 June 2015, Ein Gedi, the Dead Sea, Israel, 78–86. AAAI Press.

Pearl, J.; and Kim, J. H. 1982. Studies in Semi-Admissible Heuristics. IEEE Transactions on Pattern Analysis and Machine Intelligence, PAMI-4(4): 392–399.

Stern, R.; Kulberis, T.; Felner, A.; and Holte, R. 2010. Using Lookaheads with Optimal Best-First Search. In Fox, M.; and Poole, D., eds., Proceedings of the Twenty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2010, Atlanta, Georgia, USA, July 11-15, 2010. AAAI Press.

Sturtevant, N. 2012. Benchmarks for Grid-Based Pathfinding. Transactions on Computational Intelligence and AI in Games, 4(2): 144–148.

Tofallis, C. 2015. A better measure of relative prediction accuracy for model selection and model estimation. J. Oper. Res. Soc., 66(3): 524.

Veerapaneni, R.; and Likhachev, M. 2022. Non-Blocking Batch A\* (Technical Report).
