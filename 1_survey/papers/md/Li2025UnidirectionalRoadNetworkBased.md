---
citation_key: Li2025UnidirectionalRoadNetworkBased
arxiv_id: 2511.13048
arxiv_url: "https://arxiv.org/abs/2511.13048"
title: "Unidirectional-Road-Network-Based Global Path Planning for Cleaning Robots in Semi-Structured Environments"
authors_short: "Yong Li et al."
year: 2025
direction_tag: F_hybrid_astar
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:18:52Z
origin: ai+web
reviewed: false
---

# Unidirectional-Road-Network-Based Global Path Planning for Cleaning Robots in Semi-Structured Environments

Yong Li<sup>1,2,\*</sup>, Member, IEEE, and Hui Cheng<sup>2</sup>

Abstract— Practical global path planning is critical for commercializing cleaning robots working in semi-structured environments. In the literature, global path planning methods for free space usually focus on path length and neglect the traffic rule constraints of the environments, which leads to high-frequency re-planning and increases collision risks. In contrast, those for structured environments are developed mainly by strictly complying with the road network representing the traffic rule constraints, which may result in an overlong path that hinders the overall navigation efficiency. This article proposes a general and systematic approach to improve global path planning performance in semi-structured environments. A unidirectional road network is built to represent the traffic constraints in semi-structured environments and a hybrid strategy is proposed to achieve a guaranteed planning result. Cutting across the road at the starting and the goal points are allowed to achieve a shorter path. Especially, a two-layer potential map is proposed to achieve a guaranteed performance when the starting and the goal points are in complex intersections. Comparative experiments are carried out to validate the effectiveness of the proposed method. Quantitative experimental results show that, compared with the state-of-art, the proposed method guarantees a much better balance between path length and the consistency with the road network.

## I. INTRODUCTION

## A. Motivation

As a typical service robot, the cleaning robot is used to clean the solid and liquid wastes on the ground [1]. Cleaning robots in unstructured environments have been widely used, such as the household-sweeping robot [2], while the ones working in garages, construction zones, around shopping centers, and other semi-structured environments are still at an early stage [3][4]. There are still many problems to be solved, one of them is finding a practical global path.

In addition to accomplishing the cleaning task and ensuring their own safety, robots working in semi-structured environments need to interact with vehicles, non-vehicles, pedestrians, and even other kinds of robots and autonomous vehicles. So as not to cause confusion or trouble to human drivers and other agents, they should also try to comply with the traffic rules. A practical approach is building a road network that accounts for the traffic rules so that we can plan a global path with it [5]. In the fields of autonomous driving and automated valet parking, road-network-based global path planning is already a common practice [4][6][7]. The basic flow is: (1) find the nodes pair $\left\{ p _ { m s } , p _ { m g } \right\}$ closest to the starting point $p _ { s }$ and the goal point $p _ { g }$ in the road network respectively $( ~ p _ { m s }$ and $p _ { m g }$ should also satisfy the angle constraint); (2) use graph search algorithm to find the path connecting $p _ { m s }$ and $p _ { m g } ; ( 3 )$ adjust path points density and smooth the path. However, such practices may not be the best solution for robots in semi-structured environments. As Fig.1 shows, strictly following the traffic rules results in overlong paths in some situations, which results in low working efficiency for cleaning robots.

Balancing path length and the consistency with the road network is critical for commercializing cleaning robots working in semi-structured environments and is the main focus of this article.

## B. Related Work

Common algorithms for global path planning can be classified into four types[8]: graph-search-based planners, sampling-based methods, interpolating-curve-based and optimization-based ones. Detailed analysis and comparisons can be seen in review articles [8] and [9].

Currently, most of the research on global path planning is for unstructured and structured environments [7]. For the former, global path planning is viewed as a free-space-pathfinding problem. Methods in the literature are proposed mainly to shorten plan length and improve search efficiency with/without kinematics constraints [10] [11][12]. Such methods are not suitable for semi-structured environments as they do not take traffic rules and the respect for human drivers into account, which brings enormous safety risks to both the robot itself and other traffic participants.

The global path planning methods in structured environments are usually developed based on the traffic rule constraints described by unidirectional road networks [7][13] [14]. The planning results are required to strictly comply with the traffic rules such as lane following, lane changing, merging, pulling over, and so on [15]. The robot is not allowed to cut across the road or drive reversely on highways. As shown in Fig. 1, strictly complying with the traffic rules negatively impacts the robot's work efficiency.

Some research has been carried out to meet the set-out requirements in semi-structured environments. Tsiakas uses a sparse road network described by OSM to guide the global path planning process, and pathfinding is achieved by the $\mathbf { A } ^ { * }$ algorithm [16]. Klaudt combined the road network with a semantic and metric map to realize parking path planning in garages using a state-based planner [4]. The above two research work is based on the bidirectional road network. The planned global path points are usually distributed along the road center, which does not comply with the right-hand traffic (or left-hand traffic) rule, increasing the re-planning frequency and the risk of collision. Dolkov combined the free space hybrid A\* algorithm with the road network to improve the path quality in semi-structured environments [17][18]. In the nodes expansion step of the A\* search, the deviation from the road network is penalized, and the road network nodes also provide a good set of macro-actions. The algorithm ensures that the planned path points are close to the road network but can not guarantee they align with the road network in direction.

![](Li2025UnidirectionalRoadNetworkBased_figs/8cf715e43c7f006be489a8ef2dc34b8d0b5b7d4fd286f934a638b5293e8e43a8.jpg)

![](Li2025UnidirectionalRoadNetworkBased_figs/a77f83f6b406f02aeb2eb8b9c3e7db3a59e4af142856248f740756f1d5d3167e.jpg)  
(b)

![](Li2025UnidirectionalRoadNetworkBased_figs/0d92c64ee994d70e20134088ead134b53e74c56b7d52d207d21c6d9978e8af2f.jpg)  
(c)

![](Li2025UnidirectionalRoadNetworkBased_figs/7e7857bba61ce3bf75b30412cfdd03288f4d2bcce3454bd02a69b7402e0cbc95.jpg)  
(d)  
Fig. 1. Global path planning results when strictly complying with the road network that accounts for the traffic rules: (a) the starting and goal points are in the same lane and the latter is behind the former; (b) The starting and goal points are close but they are in the reverse lanes; (c) The starting and goal points are in different intersections and they are close to each other; (d) The starting and goal points are in different intersections and they are far away from each other.

## C. Contributions

This article proposes a practical global path planning algorithm for commercial cleaning robots working in semi-structured environments. The main contributions are:

(1) A general and systematic global path planning algorithm based on a unidirectional road network and twolayer potential map is proposed, which makes a better balance between path length and the consistency with the road network (both in distance and direction).

(2) A scenario-based strategy is adopted to meet the set-out requirements in semi-structured environments. The robot is allowed to cut across the road at the starting and goal points, which ensures the finding of a shorter path. Besides, the road network constraints in complex intersections are described with a two-layer potential map.

(3) Comparative experiments are carried out and quantitative performance indexes are introduced to verify the superiority of the proposed method.

The rest of the article is organized as follows: Sec. Ⅱ is about problem description, followed by Sec. Ⅲ presenting the methodology. Then comparative and field experimental results are described in Sec. Ⅳ. Conclusions are drawn in Sec. Ⅴ.

## II. PROBLEM DESCRIPTION

Without loss of generality, the descriptions in the rest of the article are based on a garage with the traffic rule of right-hand driving, and the research results can be easily extended to other semi-structured environments. Fig. 2 is a typical semantic map for the garage-cleaning robot. The passable areas include the passages (chocolate), the intersections (dark violet) and the parking areas (light green). The cleaning robot needs to complete the full coverage cleaning task in passable areas (full coverage path planning in the semi-structured environment will be carried out in our following research and this study only focuses on global path planning when the robot travels between different clean areas). Actually, appropriately cutting across the road is acceptable [19] to some extent for the following two reasons. First, when the robot executes the full coverage cleaning task, it is unavoidable that the robot cuts across the road; It is also reasonable to allow such behavior in global path planning. Second, the cleaning robot is much smaller than the vehicles. It is usually driven by differential wheels and thus has a much smaller turning radius than Ackerman-type robots. To balance safety and movement flexibility, the shortcut is only allowed at the starting and goal points in this study.

![](Li2025UnidirectionalRoadNetworkBased_figs/f1708adcd33335780866e31e2bb4edcb8ac88c6eac2932612e538d5bc768f8f4.jpg)  
Fig. 2. The passable areas for a garage-cleaning robot with passages in chocolate, intersections in dark violet and parking areas in light green.

Besides, we should map the starting and goal points to the road network to find a valid path. However, finding a suitable mapping is challenging when the starting and goal points are in complex intersections even with the allowance of the shortcut. Noticeably, the road network has two kinds of restraints to the global path planning process: distance constraint and direction constraint. Considering the complexity of intersections and the fact that intersections usually have small areas, it is reasonable and practical to only consider the distance constraint in intersections.

For a road network represented as $G = \{ V , E \}$ with ?? nodes and ?? edges, our goal is to minimize the planning cost ??(??) as follows:

$$
J (\boldsymbol {S}) = \underset {\boldsymbol {S}} {m i n} \left\{f _ {l} (\boldsymbol {S}) + \sum_ {i = 0} ^ {n} f _ {d} (s _ {i}, G) + \sum_ {i = 0} ^ {n} f _ {\theta} (s _ {i}, G) \right\}\tag{1}
$$

where $\pmb { S } = \{ s _ { i } , i = 1 , 2 , \dots , n \}$ is the global path with $s _ { i } =$ $\{ x _ { i } , y _ { i } , \theta _ { i } \}$ the ith global path point, $f _ { l } ( \pmb { S } )$ the path length cost, $f _ { d } ( s _ { i } , G )$ and $f _ { \theta } ( s _ { i } , G )$ the cost of the distance and angle between $s _ { i }$ and $G ,$ respectively. This article tries to minimize ??(??) with hybrid strategies rather than giving an analytic solution.

## III. METHODOLOGY

## A. Unidirectional road network

![](Li2025UnidirectionalRoadNetworkBased_figs/d73f7379af5e8e8339c01b192fae4993c1c1151c263b63a80f09d779b8eef3f6.jpg)  
Fig. 3. A typical semantic map for the garage-cleaning robot with the unidirectional road network in chocolate, intersection areas in dark viole and parking areas in light green. The arrows of the lanes indicate their direction.

The road network can be designed according to the actual situation of the environment with considering the set-out requirements. For example, the unidirectional road network for the garage of Guangzhou Shiyuan Electronic Technology Co., Ltd. is designed as Fig. 3 shows. The road network is composed of unidirectional lanes $L = \left\{ L _ { i } , i = 1 , 2 , \ldots , n \right\}$ and each lane $L _ { i }$ has two nodes $p _ { i } = \{ p _ { i s } , p _ { i e } \}$ (fewer nodes improve the speed of road network construction and pathfinding process). The predecessor lanes $L _ { i } ^ { f r o m }$ and the successor lanes $L _ { i } ^ { t o } \mathrm { o f } L _ { i }$ can be expressed as:

$$
\begin{array}{r l} & L _ {i} ^ {f r o m} = \left\{L _ {j} \in L: \left| \theta_ {p _ {j e} -} \theta_ {p _ {i s}} \right| <   \alpha_ {m i n} \& \left\| p _ {j e} - p _ {i s} \right\| <   d _ {m i n} \right\} \\ & L _ {i} ^ {t o} = \left\{L _ {j} \in L: \left| \theta_ {p _ {j s} -} \theta_ {p _ {i e}} \right| <   \alpha_ {m i n} \& \left\| p _ {j s} - p _ {i e} \right\| <   d _ {m i n} \right\} \end{array}\tag{2}
$$

where $\theta _ { * }$ is the angle of node $\ast \ ( \ast = p _ { j e } , p _ { i s } , p _ { j s }$ ?????? $p _ { i e } ) $ $\alpha _ { m i n }$ the angle threshold and $d _ { m i n }$ the distance threshold. Besides, the procedure for finding the reverse lanes $L _ { i } ^ { r e v e r s e } { \mathrm { o f } }$ $L _ { i }$ can be seen in Algorithm 1. For every node in $L _ { i }$ , the algorithm tries to find its closest lane $L _ { j }$ in ?? with $L _ { j }$ no a predecessor/successor lane nor an intersection lane of $\mathrm { \Delta }$ . The founded lane and $L _ { i }$ are reverse lanes of each other. The nodes of ?? are also the nodes ?? of road network G. the edges ?? of G are represented as unidirectional edges. The predecessor node $p _ { i e } ^ { f r o m }$ of $p _ { i e }$ is $p _ { i s }$ while the successor node $p _ { i s } ^ { t o }$ of $p _ { i s }$ is $p _ { i e }$ . The predecessor nodes $p _ { i s } ^ { f r o m }$ of $p _ { i s }$ and successor nodes $p _ { i e } ^ { t o } \cot p _ { i e }$ are respectively represented as:

$$
\begin{array}{r} p _ {i s} ^ {f r o m} = \left\{p _ {j e} \colon p _ {j e} \in L _ {j}, L _ {j} \in L _ {i} ^ {f r o m} \right\} \\ p _ {i e} ^ {t o} = \left\{p _ {j s} \colon p _ {j s} \in L _ {j}, L _ {j} \in L _ {i} ^ {t o} \right\} \end{array}\tag{3}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Procedure in Finding Reverse Lane

for all $L_i \in L$ do
    for all $p_i \in L_i$ do
    $d_{min} \leftarrow +\infty$ $id \leftarrow -1$
    for all $L_j \in L$ do
    if $L_j.id != L_i.id$ then
    if $L_j \notin L_i^{from}$ then
    if $L_j \notin L_i^{to}$ then
    if $L_j$ does not intersect with $L_i$ then
    $\mathbf{P} \leftarrow \overrightarrow{p_{js}p_{je}}$ $\mathbf{P}_0 \leftarrow \overrightarrow{p_{js}p_i}$ $\mathbf{P}_1 \leftarrow \overrightarrow{p_{je}p_i}$ $d \leftarrow \frac{\mathbf{P}_0 \times \mathbf{P}}{||\mathbf{P}||}$ $\Delta\theta \leftarrow \theta_{p_i} - \theta_{\mathbf{P}}$
    if $\Delta\theta &gt; \theta_{\text{threhood}}$ then
    if ($PP_0 &gt; 0$ &amp;&amp; $PP_1 &lt; 0$) then
    if $d &lt; d_{\text{threhood}}$ then
    if $d &lt; d_{min}$ then
    $d_{min} \leftarrow d$ $id \leftarrow j$
    if $id &gt; 0$ then
    if $L_i^{reverse} \leftarrow L_i^{reverse} \cup L_{id}$
    if $L_{id}^{reverse} \leftarrow L_{id}^{reverse} \cup L_i$
</div>

Based on the above nodes and edges, the unidirectional road network $G = \{ V , E \}$ can be built.

## B. Search strategy

Case1 ： path planning with starting and goal points in passages or parking areas. When the starting and goal points are in passages or parking areas, the complete planning procedure is shown in Algorithm 2. In this study, the starting and goal points are mapped not only to the closet lane but also to the reverse lanes of their closet lane. For the planned path, the mapping rules are designed to ensure no sharp turns around the matched starting points or the matched goal ones.

1) Starting point mapping: For starting point $p _ { s } ,$ donate its closest lane as $L _ { c }$ and $\bar { L _ { c } ^ { \mathrm { ~ \tiny ~ s ~ } } }$ reverse lane is $\bar { L } _ { c } ^ { r e v e r s e }$ . The set of $L _ { c }$ and $L _ { c } ^ { r e v e r s e } \bar { \mathrm { i } }$ s represented as ${ \cal { Y } } = \{ L _ { c } \cup L _ { c } ^ { r e v e r s e } \}$ . For ∀ $\psi _ { k } \in \psi , k = 1 , 2 , \dots , m$ with $\psi _ { k }$ composed of $p _ { k s }$ and $p _ { k e } ,$ the relative spatial relationship between $p _ { s }$ and $\psi _ { k }$ can be seen in Fig. 4 with $p _ { s 1 } , p _ { s 2 }$ ?????? $p _ { s 3 }$ three possible locations of $p _ { s } .$ . For easy of notation, let ${ \bf P _ { 0 } } = \overrightarrow { p _ { k s } p _ { s } } , { \bf P _ { 1 } } = \overrightarrow { p _ { k e } p _ { s } } , { \bf P _ { \ell } }$ $= \overrightarrow { p _ { k s } p _ { k e } }$ . The matching point $p _ { k } ^ { m a t c h }$ can be expressed as follows:

 if $\mathbf { P _ { 0 } P < } 0$ (corresponding to $p _ { s 1 }$ in Fig.4(a)), ??<sub>??</sub><sup>????????ℎ</sup> $= p _ { k s } .$

 if $\mathbf { P _ { 0 } P } > 0 \& \mathbf { P P _ { 1 } } < 0$ (corresponding to $p _ { s 2 }$ in Fig. $4 ( \mathrm { a } ) ) , p _ { k } ^ { m a t c h } = p _ { k s } + \mathbf { P _ { 0 } } \mathbf { P P } / \| \mathbf { P } \| ^ { 2 }$

 if $\mathbf { \nabla } \mathbf { P } \mathbf { P } _ { 1 } > 0$ (corresponding to $p _ { s 3 }$ in Fig. 4(a)), $p _ { k } ^ { m a t c h }$ $= \{ p _ { u s } \in L _ { u } , L _ { u } \in \bar { \psi } _ { k } ^ { t o } \}$

Then the set of the matched starting points is represented as $\pmb { P } _ { s t a r t } ^ { m a t c h } = \{ p _ { k } ^ { m a t c h } , k = 1 , 2 , \ldots , m \}$

2) Goal point mapping: Similarly, as shown in Fig $. 4 ( \mathsf { b } )$ the matching point $\bar { p } _ { k } ^ { m a t c h }$ for the goal point $p _ { g }$ can be represented as follows:

 if $\mathbf { P _ { 0 } P < 0 }$ (corresponding to $p _ { e 1 }$ in Fig.4(b)), $p _ { k } ^ { m a t c h } = \{ p _ { v s } \in L _ { v } , L _ { v } \in \varPsi _ { k } ^ { f r o m } \}$

 if $\mathbf { P _ { 0 } P } > 0 \& \mathbf { P P _ { 1 } } < 0$ (corresponding to $p _ { e 2 }$ in Fig. $4 ( \mathsf { b } ) ) , p _ { k } ^ { m a t c h } = p _ { k s } + \mathbf { P _ { 0 } } \mathbf { P } \mathbf { P } \big / | | \mathbf { P } | | ^ { 2 }$

 if ????<sub>??</sub> > 0(corresponding to ??<sub>??3</sub>in Fig. 4(b)), $p _ { k } ^ { m a t c h }$ ${ } = p _ { k e } .$

Then the set of the matched goal points is represented as $P _ { g o a l } ^ { m a t c h } \ . \ P _ { s t a r t } ^ { m a t c h }$ and $P _ { g o a l } ^ { m a t c h }$ serve as the start and goal candidates in the path searching process.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Procedure in Case 1
input : Starting point $p_s$, Goal point $p_g$, Road network $G$ output: GlobalPath $\chi(p_s, p_g)$
1 $P_{start}^{match} \leftarrow \text{FindMatchedStartPoints}(p_s, G)$
2 $P_{goal}^{match} \leftarrow \text{FindMatchedGoalPoints}(p_g, G)$
3 MaxCost $\leftarrow 2 \times G.Nodes.size()$
4 MinLength $\leftarrow +\infty$
5 SearchCost $\leftarrow 0$
6 for all $p_s^{match} \in P_{start}^{match}$ do
7    for all $p_g^{match} \in P_{goal}^{match}$ do
8    bSuccess $\leftarrow$
    BuildSearchTree($p_s^{match}, p_g^{match}$, MaxCost, G, SearchCost)
9    if bSuccess then
10    {Path, PathLength} $\leftarrow \text{getPath()}$
11    $\sqsupseteq \leftarrow \text{Path} \cup p_s \cup p_g$
12    $d_s \leftarrow \text{Distance}(p_s, p_s^{match})$
13    $d_g \leftarrow \text{Distance}(p_g, p_g^{match})$
14    TotalPathLength $\leftarrow \text{PathLength} + d_s + d_g$
15    if TotalPathLength &lt; MinLength then
16    MaxCost $\leftarrow 2 \times \text{SearchCost}$
17    $\chi(p_s, p_g) \leftarrow \sqsupseteq$
</div>

![](Li2025UnidirectionalRoadNetworkBased_figs/52174be56dbc604f43b8422ed7ff2e36069ffac45d60a67939d8de1c1359b706.jpg)

(a)  
![](Li2025UnidirectionalRoadNetworkBased_figs/254c522cb082e340ae6766ebb17cfd812b97edced1000a849dd86cf67e45a132.jpg)  
(b)  
Fig. 4. (a) starting point mapping: $p _ { s 1 } , p _ { s 2 }$ an $| { p } _ { s 3 }$ represent three probable positions of starting point $p _ { s } , \psi _ { k }$ the closest lane to $p _ { s } , \psi _ { k } ^ { f r o m }$ and $\psi _ { k } ^ { t o }$ the predecessor and successor lane of $\boldsymbol { \psi } _ { k } ,$ respectively. The ends of the arrows represent the mapping results; (b) goal point mapping: $p _ { e 1 } , p _ { e 2 } , p _ { e 3 }$ are three probable positions of goal point $p _ { g } , \psi _ { k }$ the closest lane to $p _ { g } , \psi _ { k } ^ { f r o m }$ and $\psi _ { k } ^ { t o }$ the predecessor and successor lane of $\psi _ { k }$ , respectively. The ends of the arrows represent the mapping results.

3) Path searching: For every $p _ { s } ^ { m a t c h }$ in $P _ { s t a r t } ^ { m a t c h }$ and $p _ { g } ^ { m a t c h }$ in $P _ { g o a l } ^ { m a t c h }$ , the Dijkstra algorithm is adopted to find a valid path. Appending the starting point $p _ { s }$ and the goal point $p _ { g }$ to the front and back of the Dijkstra path, respectively, then we can get the total path ℶ that connects $p _ { s }$ and $p _ { g }$ Looping through $P _ { s t a r t } ^ { m a t c h }$ and $P _ { g o a l } ^ { m a t c h }$ then we can get the shorted path $\chi . \mathrm { A }$ branch-and-bound method is adopted in the cycles to improve the computation efficiency: If the length of current ℶ is shorter than the shortest path ?? ever, the total search cost of the Dijkstra process in this cycle will be used as the upper bound cost for Dijkstra in the following cycles.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: Procedure in Case 2
input : StartPose $p_s$, GoalPose $p_g$, Road network G,
Multi-level map $\Xi$
output: GlobalPath $\chi(p_s, p_g)$
1 $P_{start}^{inters} \leftarrow \text{FindIntersectedPoints}(p_s, G)$
2 $P_{goal}^{inters} \leftarrow \text{FindIntersectedPoints}(p_g, G)$
3 MaxCost $\leftarrow 2 \times G.Nodes.size()$
4 MinLength $\leftarrow +\infty$
5 StartTempPoint $p_{st} \leftarrow p_s$
6 GoalTempPoint $p_{gt} \leftarrow p_g$
7 PathLength $\leftarrow 0$
8 for all $p_s^{inters} \in P_{start}^{inters}$ do
9    for all $p_g^{inters} \in P_{goal}^{inters}$ do
10    bSuccess $\leftarrow$
BuildSearchTree($p_s^{inters}, p_g^{inters}$, MaxCost, G, SearchCost)
if bSuccess then
11    {Path, PathLength} $\leftarrow$ getPath()
12    if PathLength &lt; MinLength then
13    MaxCost $\leftarrow 2 \times SearchCost$
14    $p_{st} \leftarrow p_s^{inters}$
15    $p_{gt} \leftarrow p_s^{inters}$
16    $\chi(p_{st}, p_{gt}) \leftarrow Path$
17 $\chi(p_s, p_{st}) \leftarrow SearchWithDijkstra(\Xi, p_s, p_{st})$
18 $\chi(p_{gt}, p_g) \leftarrow SearchWithDijkstra(\Xi, p_{gt}, p_g)$
19 $\chi(p_s, p_g) \leftarrow \chi(p_s, p_{st}) \cup \chi(p_{st}, p_{gt}) \cup \chi(p_{gt}, p_g)$
</div>

Case2：path planning with starting and goal points in intersections. The procedure in Case 1 can not guarantee the quality of the generated path in Case 2 due to the complexity of intersection areas. In this article, a hybrid strategy is proposed: the sub-paths inside the intersections are obtained based on a two-layer potential map, while those outside the intersections are gained with a strategy similar to that in Case 1. Detailed procedures can be seen in Algorithm 3.

1) path planning outside the intersections: For $p _ { s }$ and $p _ { g } .$ , without loss of generality, assume they locate in intersections $S _ { m }$ and $S _ { n } \left( m \neq n \right)$ , respectively. The set of intersected points of $S _ { m } / S _ { n }$ and $G$ is represented as $P _ { s t a r t } ^ { i n t e r s } / P _ { g o a l } ^ { i n t e r s }$ Similar to the procedure in Case 1, the shortest path $\chi ( p _ { s t } , p _ { g t } )$ can be obtained with starting point candidates $P _ { s t a r t } ^ { i n t e r s }$ and goal point candidates $P _ { g o a l } ^ { i n t e r s }$ . The front and back points of $\chi ( p _ { s t } , p _ { g t } )$ are represented as $p _ { s t }$ and $p _ { g t }$ , respectively.

2) path planning within the intersections: In this step, sub-paths $\chi ( p _ { s } , p _ { s t } )$ and $\chi ( p _ { g t } , p _ { g } )$ are obtained so that we can get the complete path $\chi ( p _ { s } , p _ { g } )$ from $p _ { s }$ to $p _ { g } . \mathrm { A }$ two-layer potential map is proposed to represent the distance constraints of the road network. As can be seen in Fig.5, the first layer is a traditional static map $m _ { s t a t i c }$ with the obstacles inflated. The second layer $m _ { s e m a n t i c }$ is built based on the semantic information in Fig.3. A Gaussian potential field is generated within the passable area with the lanes reference (similar approaches can be seen in [20] and [21]). For every point $x _ { i }$ in the passable area $U _ { p } .$ , if the distance between $x _ { i }$ and the road network G is $d _ { x _ { i } } ,$ its potential value $p ( x _ { i } )$ can be computed as:

![](Li2025UnidirectionalRoadNetworkBased_figs/0bb83d1ebadee08d39d8da9924d3143d8d8d749c6d469e6fab26be38f6ac34fc.jpg)  
Fig. 5. Part of the two-layer potential map used for path planning when the starting and goal points are in intersections: (a) static metric map with obstacles inflated; (b) road network Gaussian likelihood potential maps; (c) the combined map.

$$
p (x _ {i}) = p _ {0} \big [ 1 - e x p (- d _ {x _ {i}} ^ {2} / 2 \sigma^ {2}) \big ], x _ {i} \in U _ {p}\tag{4}
$$

where $p _ { 0 }$ is the maximal potential, ?? the standard deviation. The potential value for points on the road boundary is $p _ { 0 }$ and that for points outside passable areas is 0. Combining $m _ { s t a t i c }$ and $m _ { s e m a n t i c }$ with the adoption of a larger potential value in each grid cell, we can get the map ?? used for path planning. A traditional Dijkstra planner is then adopted to get $\chi ( p _ { s } , p _ { s t } )$ and $\chi ( p _ { g t } , p _ { g } )$

It can be seen from the above procedure in Case 2 that a piece-wise planning strategy is adopted: the starting point $p _ { s t }$ and the goal point $p _ { g t }$ for the planning within the intersections are the outcomes of the planning outside the intersections; we end up with a path that may not be optimal. Considering the computation burden and the fact that the intersections often have a small area, the above sub-optimal strategy is acceptable.

It should be noted that this article only describes the path planning strategy in two typical situations, where both the starting and goal points are in the passage/parking area or in different intersections. There are much more combinations such as: the starting point in passage/parking area while the goal point in intersections, the goal point in passage/parking area while the starting point in intersections, or the starting and goal points in the same intersection. Due to space limitations, we will not elaborate on them case by case. Noticeably, they can be easily handled with the basic ideas in Case1&2.

## IV. EXPERIMENTS

## A. Comparative experiments

To verify the effectiveness of the proposed method, comparative experiments are carried out. The computing unit used in the experiments is an industrial computer with CPU i7-10700@2.9Hz×16 and RAM of 16 GB. The size of the map used in the experiment is 75m \* 128m. The following four methods are compared:

Hybrid-A\*-in-SS: Hybrid $\mathbf { A } ^ { * }$ in semi-structured environments [18], is considered the state-of-the-art. The cost coefficient $C _ { G }$ (the deviation from the road network) is set to be 1.

Dijkstra: The widely used Dijkstra algorithm in free space. The map resolution is 0.05m.

Dijkstra-in-SS: Dijkstra in semi-structured environments. In the nodes-expansion step of Dijkstra, the cost representing the distance between the current node and the road network is considered.

Ours: the method proposed in this article.

To quantify the performance of different planners, the following performance indexes are used:

$t = ( 1 / 1 0 0 ) \sum _ { \mathrm { i } = 0 } ^ { 1 0 0 } t _ { i }$ , the average planning time for 100 consecutive planning cycles, is used to evaluate the computation efficiency;

 ?? the path length, is used to evaluate the distance cost;

$\begin{array} { r } { d _ { e } = ( 1 / n ) \sum _ { i = 0 } ^ { n } | d _ { i } | } \end{array}$ with $d _ { i } = \mathbf { P _ { 0 } } \times \mathbf { P } / \| \mathbf { P } \| \ ( \mathbf { P _ { 0 } } =$ $\overrightarrow { p _ { j s } p _ { i } } , \mathbf { P } = \overrightarrow { p _ { j s } p _ { j e } } )$ the distance between the path point ?? and its closest lane $L _ { j } ~ ( L _ { j }$ is composed of points $p _ { j s }$ and $p _ { j e } ) ,$ is used to evaluate the distance deviation from the road network;

$\theta _ { e } = \left( 1 / n \right) \sum _ { i = 0 } ^ { n } \left| \Delta \theta _ { i } \right|$ with $\Delta \theta _ { i } = \theta _ { p _ { i } } - \theta _ { p _ { j s } }$ the relative angle between the path point $p _ { i }$ and its closest lane $\bar { L _ { j } ( L _ { j } }$ is composed of points $p _ { j s }$ and $p _ { j e } ) _ { : }$ , is used to evaluate the direction deviation from the road network.

TABLE I. PERFORMANCE INDEXES IN EXPERIMENT 1

<table><tr><td></td><td>HybridA*-in-SS</td><td>Dijkstra</td><td>Dijkstra-in-SS</td><td>Ours</td></tr><tr><td> $t(s)$ </td><td>11.279</td><td>0.405</td><td>0.409</td><td>0.009</td></tr><tr><td> $l(m)$ </td><td>132.514</td><td>127.172</td><td>131.158</td><td>137.599</td></tr><tr><td> $d_e(m)$ </td><td>0.039</td><td>0.625</td><td>0.085</td><td>0.028</td></tr><tr><td> $\theta_e(rad)$ </td><td>1.997</td><td>2.876</td><td>2.004</td><td>0.095</td></tr></table>

Experiment 1: both the starting and goal points are in the passage. As can be seen in Fig.6 and Table 1, The traditional Dijkstra algorithm has the shortest path. Due to the neglect of the road network constraints, it has the worst performance in $d _ { e }$ and $\theta _ { e } .$ Compared with Dijkstra, $H y b r i d – A ^ { * } – i n – S S$ and Dijkstra-in-SS both have improved performance in $d _ { e }$ due to the introduction of the road-network-distance-derivation penalty. However, they can not guarantee a small $\theta _ { e }$ in nature. The path length of the proposed method is 3.8% longer than that of the Hybrid-A\*-in-SS mainly due to the shortcut at the goal point. However, the proposed method has better performance in the consistency with the road network, especially in terms of the direction deviation $\theta _ { e }$ , which significantly improves the navigation safety of the robot. Besides, due to the adoption of the sparse unidirectional road network in Sec. Ⅲ. A, our method has better performance in planning time than those grid-map-based planners.

Experiment 2: the starting and goal points are in different intersections. Experimental results and performance indexes for Experiment 2 are shown in Fig. 7 and Table $^ { 2 , }$ respectively. Compared with other planners, our method has similar performance in path length but with shorter planning

![](Li2025UnidirectionalRoadNetworkBased_figs/fb11c95a1ad5e9679e22e2724ca438c8ccc30faa4777a084e5be8cff9df42e30.jpg)

![](Li2025UnidirectionalRoadNetworkBased_figs/e2de50d4e899f5e8c9e34c79f9b92eb9edd56262ce3fb9ab47a832795572c461.jpg)

![](Li2025UnidirectionalRoadNetworkBased_figs/08aac7fc443d1a7d91a4d77235ce9eb9209e15e03cfe947f885313bd44f9f4c7.jpg)

![](Li2025UnidirectionalRoadNetworkBased_figs/8f56779e46c6803f2be9b9facd83d21a9556da07d4553dbd8101f6e0cf2f9585.jpg)

Fig. 6. Planning results in Experiment 1 with $\theta _ { e }$ representing the angle error between the path point and its closest lane.  
![](Li2025UnidirectionalRoadNetworkBased_figs/2a805771abec6eef75c53c15ccf72a32a8d686f14ebe18ed72dc7969dcf3b108.jpg)  
Fig. 7. Planning results in Experiment 2 with ?? representing the angle error between the path point and its closest lane.

TABLE II. PERFORMANCE INDEXES IN EXPERIMENT 2

<table><tr><td></td><td>Hybrid A*-in-SS</td><td>Dijkstra</td><td>Dijkstra-in-SS</td><td>Ours</td></tr><tr><td> $t(s)$ </td><td>8.534</td><td>0.349</td><td>0.351</td><td>0.101</td></tr><tr><td> $l(m)$ </td><td>91.7328</td><td>88.023</td><td>88.479</td><td>91.280</td></tr><tr><td> $d_{e}(m)$ </td><td>0.035</td><td>0.606</td><td>0.063</td><td>0.027</td></tr><tr><td> $\theta_{e}(rad)$ </td><td>2.542</td><td>2.725</td><td>3.029</td><td>0.220</td></tr></table>

![](Li2025UnidirectionalRoadNetworkBased_figs/ad495e7066a81bca4b8cfdbf73dcf84b5346362b266564c945e5c2937d7d41f0.jpg)

![](Li2025UnidirectionalRoadNetworkBased_figs/25d357771bdaaad184574d40f3a3a2e8df394dcf6877a28341f8ab9d4b71b93e.jpg)

![](Li2025UnidirectionalRoadNetworkBased_figs/e479a6addb4b440fd78aa4463d8dd1869df4da0be678546ef4efc9cc5ac3b266.jpg)  
(b)  
(c)  
Fig. 8. An instance of the field experiment with the proposed global path planner in the garage of Guangzhou Shiyuan Electronic Technology Co., Ltd.

time. Due to the adoption of the two-layer-map based hybrid planning strategy in Algorithm 2, compared with Hybrid-A\*- in-SS, 22.86% and 91.35% improvement in $d _ { e }$ and $\theta _ { e }$ can be obtained, respectively. It means that with the proposed method, a much better balance between path length and the consistency with the road network has been achieved, which is vital for path planning in semi-structured environments.

## B. Experiments with robots

Field experiments are carried out in the garage shown in Fig.8(a) with the semantic map in Fig.8(b). The starting and goal points in Fig.8(c) are the same as those in Experiment 1. The robot used in the experiment is a commercial garagecleaning robot produced by Guangzhou Shiyuan Electronic Technology Co., Ltd. with RK3399 the computation unit. The global path planner proposed in this article provides a reference line to the local path planner module, which is a lightweight state lattice planner. The video of the experiment is submitted as a supplementary material.

## V. CONCLUSION

This article proposes a general and systematic global path planning method for robots in semi-structured environments. Comparative experimental results show that it achieves a much better balance between path length and the consistency with the road network, which distinguishes our work from the ones in the literature. The proposed method has been widely used in the commercial garage-cleaning robot produced by Guangzhou Shiyuan Electronic Technology Co., Ltd.

Our research focuses on solving the critical motion planning problems that prevent the commercializing robots in semi-structured environments. Research on full coverage path planning and local path planning for robots in semistructured environments will be carried out in the future.

## REFERENCES

[1] R. Bormann, F. Jordan, J. Hampp and M. Hägele, "Indoor Coverage Path Planning: Survey, Implementation, Analysis," in 2018 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2018, pp. 1718-1725.

[2] L. Sui and L. Lin, "Design of Household Cleaning Robot Based on Low-cost 2D LIDAR SLAM," in 2020 International Symposium on Autonomous Systems (ISAS).IEEE, 2020, pp. 223-227.

[3] A. C. Magalhães, M. Prado, V. Grassi and D. F. Wolf, "Autonomous vehicle navigation in semi-structured urban environment", IFAC Proceedings Volumes, vol. 46, no. 10, pp. 42-47, 2013.

[4] S. Klaudt, A. Zlocki and L. Eckstein, "A-priori map information and path planning for automated valet-parking," in 2017 IEEE Intelligent Vehicles Symposium (IV).IEEE, 2017, pp. 1770-1775.

[5] F. Poggenhans et al., "Lanelet2: A high-definition map framework for the future of automated driving," in 2018 21st International Conference on Intelligent Transportation Systems (ITSC).IEEE, 2018, pp. 1672-1679.

[6] K. Tsiakas, I. Kostavelis, A. Gasteratos and D. Tzovaras, "Autonomous Vehicle Navigation in Semi-structured Environments Based on Sparse Waypoints and LiDAR Road-tracking," in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).IEEE, 2021, pp. 1244-1250.

[7] Hatem Darweesh, Eijiro Takeuchi, Kazuya Takeda, Yoshiki Ninomiya, Adi Sujiwo, Y. Morales, et al., "Open Source Integrated Planner for Autonomous Navigation in Highly Dynamic Environments", Journal of Robotics and Mechatronics, vol. 29, pp. 668-684, 2017.

[8] D. González, J. Pérez, V. Milanés and F. Nashashibi, "A review of motion planning techniques for automated vehicles", IEEE Transactions on Intelligent Transportation Systems, vol. 17, no. 4, pp. 1135-1145, 2016.

[9] H. Banzhaf, D. Nienhüser, S. Knoop and J. M. Zöllner, "The future of parking: A survey on automated valet parking with an outlook on high density parking," in 2017 IEEE Intelligent Vehicles Symposium (IV).IEEE, 2017, pp. 1827-1834.

[10] S. Klemm et al., "RRT-Connect: Faster, asymptotically optimal motion planning," in 2015 IEEE International Conference on Robotics and Biomimetics (ROBIO).IEEE, 2015, pp. 1670-1677.

[11] D. M. Saxena, T. Kusnur and M. Likhachev, "AMRA\*: Anytime Multi-Resolution Multi-Heuristic A\*," in 2022 International Conference on Robotics and Automation (ICRA). IEEE, 2022, pp. 3371-3377.

[12] D. Khalidi, D. Gujarathi and I. Saha, "T: A Heuristic Search Based Path Planning Algorithm for Temporal Logic Specifications," in 2020 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2020, pp. 8476-8482.

[13] J. Kim, K. Jo, K. Chu and M. Sunwoo, "Road-model-based and graph-structure-based hierarchical path-planning approach for autonomous vehicles", Proceedings of the Institution of Mechanical Engineers Part D: Journal of Automobile Engineering, vol. 228, no. 8, pp. 909-928, 2014.

[14] W. Cheng, T. Gao, Z. Liu, S. Li, N. Li and C. Lu, "A Distributed Motion Planning Method based on Routing and Local Dynamic Programming," in 2020 3rd International Conference on Unmanned Systems (ICUS).IEEE, 2020, pp. 418-422.

[15] C. Urmson, J. Anhalt, D. Bagnell, C. Baker, R. Bittner, MN Clark, J. Dolan, D. Duggins, T. Galatali, C. Geyer et al., "Autonomous driving in urban environments: Boss and the Urban Challenge", Journal of Field Robotics, vol. 25, no. 8, 2008.

[16] K. Tsiakas, I. Kostavelis, A. Gasteratos and D. Tzovaras, "Autonomous Vehicle Navigation in Semi-structured Environments Based on Sparse Waypoints and LiDAR Road-tracking," in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).IEEE, 2021, pp. 1244-1250.

[17] D. Dolgov and S. Thrun, "Autonomous driving in semi-structured environments: Mapping and planning," in 2009 IEEE International Conference on Robotics and Automation (ICRA).IEEE, 2009, pp. 3407-3414.

[18] D. Dolgov, S. Thrun, M. Montemerlo, and J. Diebel, “Path planning for autonomous vehicles in unknown semi-structured environments,” The international journal of robotics research, vol. 29, no. 5, pp. 485– 501, 2010.

[19] F. Yang, D. -H. Lee, J. Keller and S. Scherer, "Graph-based Topological Exploration Planning in Large-scale 3D Environments," in 2021 IEEE International Conference on Robotics and Automation (ICRA).IEEE, 2021, pp. 12730-12736.

[20] K. Narula, S. Worrall and E. Nebot, "Two-Level Hierarchical Planning in a Known Semi-Structured Environment," in 2020 IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC).IEEE, 2020, pp. 1-6.

[21] D. Kim, H. Kim and K. Huh, "Trajectory Planning for Autonomous Highway Driving Using the Adaptive Potential Field," in 2018 21st International Conference on Intelligent Transportation Systems (ITSC).IEEE, 2018, pp. 1069-1074.