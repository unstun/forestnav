---
citation_key: Ahmadi2025Adaptive
arxiv_id: 2509.06682
arxiv_url: https://arxiv.org/abs/2509.06682
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:31:46Z
origin: ai+web
reviewed: false
---

:::: frontmatter
[^1]

::: keyword
Coverage control, Agricultural fields, Dynamic obstacles, Time varying, Adaptive path planning.
:::
::::

# Introduction

Growing population has driven a rising demand for food, putting significant pressure on crop and livestock production. This strain often leads to environmental concerns and shortages of trained agricultural labor [@bechar2016agricultural]. In response, smart farming technologies have gained prominence and offer solutions to enhance productivity while minimizing waste and operational expenses [@singh2021agrifusion]. At the forefront of this transformation is precision agriculture (PA), which leverages advanced data analytics, autonomous systems like UAVs and UGVs, and controls/automation to optimize field operations [@monteiro2021precision].

In PA, the combination of UAVs and UGVs can make a significant impact [@mammarella2022cooperation]. UAVs are capable of detecting areas that require attention, while UGVs can incorporate the data received from UAVs into their path planning for more efficient navigation [@bechar2016agricultural; @munasinghe2024comprehensive]. Meanwhile, agricultural fields are generally subject to continuous changes, with obstacles such as moving machinery, livestock, and terrain variations - such as muddy soil patches - introducing uncertainty into path planning and coverage control [@etezadi2024comprehensive]. Traditional coverage control algorithms typically assume static environments, limiting their applicability in real-world farming conditions [@schwager2009gradient]. Similarly, existing path planning approaches such as Dijkstra's algorithm, A\*, and Hybrid A\* also rely on predefined maps and static assumptions [@dolgov2008practical]. Therefore, these methods do not adapt to moving obstacles or terrain variations in real-time. More recent approaches in multi-agent path finding (MAPF) have attempted to address dynamic environments by incorporating collision avoidance mechanisms between agents [@stern2019multi].

An algorithmic solution for persistent coverage has been proposed, where robots use fast marching methods and a coverage action controller to maintain the desired coverage level efficiently and safely [@palacios2017optimal]. Also, a coordination strategy for a hybrid UGV--UAV system in planetary exploration has been presented, in which the UGV serves as a moving charging station for the UAV to optimize target point coverage while minimizing travel distance [@ropero2019terra]. The authors introduce a terrain-aware path planning method for UGVs based on the Hybrid A\* algorithm, optimizing both traversability and distance to improve autonomous navigation in rough terrain [@thoresen2021path]. A prioritized path-planning algorithm for multi-UGV systems in agricultural environments extends MAPF by incorporating robot priorities to reduce congestion without inter-robot communication [@jo2024field]. A multi-phase approach for cooperative UAV--UGV operations in precision agriculture focuses on automated navigation and task execution in complex, unstructured environments such as sloped vineyards [@mammarella2020cooperative]. A partitioning algorithm and deployment strategy have been developed for distributing heterogeneous autonomous robots in a partially known environment, optimizing coverage and resources for applications like agricultural field monitoring [@davoodi2020heterogeneity]. Finally, a new partitioning algorithm based on a state-dependent proximity metric and a discounted cost function for robots with nonlinear dynamics has also been proposed [@davoodi2021graph].

While the aforementioned methods provide effective partitioning and tracking strategies, they often fail to dynamically account for moving obstacles or changing terrain conditions in a graph. ***The contribution and novelty of this study lies in explicitly incorporating obstacle avoidance and adaptation to terrain conditions in path planning. To this end, we propose an adaptive coverage control strategy that integrates UAV-based observations with UGV path planning. Specifically, once the UAV detects an obstacle or obtains data on the terrain conditions, the path planning for UGVs adjusts coverage paths accordingly to ensure a safe and efficient navigation***.

The remainder of this paper is structured as follows. Section [2](#sec:2){reference-type="ref" reference="sec:2"} defines the problem and formalizes the environment modeling. Section [3](#sec:3){reference-type="ref" reference="sec:3"} introduces our adaptive graph-based coverage control strategy, including Voronoi partitioning and dynamic path updating. Section [4](#sec:4){reference-type="ref" reference="sec:4"} presents simulation results, and Section [5](#sec:5){reference-type="ref" reference="sec:5"} gives concluding remarks.

# Problem Statement and Preliminaries {#sec:2}

The primary objective of this paper is to address the problem of autonomous monitoring of an agricultural field, represented as a partially known environment $Q$, using a group of UGVs. This environment may contain both dynamic obstacles (e.g., moving vehicles) and static obstacles (e.g., muddy regions). This section explains the process of modeling the agricultural field as a weighted directed graph and defines the problem.

## Environment Modeling

The environment, representing the robots' workspace, is modeled as a weighted directed graph $\mathcal{G}(\mathcal{V}, \mathcal{E}, \mathcal{C})$ that consists of a node set $\mathcal{V} = \{v_1,v_2, \ldots, v_m\}$, an edge set $\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V}$, and associated weights $\mathcal{C} \in \mathbb{R}^{m \times m}$. The set of neighboring nodes for a given node $x$ in the graph is denoted by $\mathcal{N}_{\mathcal{G}}(x) =\{y \in \mathcal{V} \mid \overrightarrow{x y} \in \mathcal{E}\}$.

Assuming that an image of the agricultural field is provided by the UAV, plant rows are represented by bounding boxes (rectangles) using image detection (see Fig. [4](#fig:detection){reference-type="ref" reference="fig:detection"}(a)). Each corner of these rectangles is used to define nodes for the graph, indicated by red circles in Fig. [4](#fig:detection){reference-type="ref" reference="fig:detection"}(b). Node numbering begins from the top left of the field, moving row by row, then column by column. These nodes are connected to each other with directed straight lines, as shown in Fig. [4](#fig:detection){reference-type="ref" reference="fig:detection"}(c), to construct the graph. In this study, nodes are viewed as specific points within the environment, acting as predefined destinations for robots departing from their current positions, while edges represent the paths for robot movement between nodes. Although robot movement is restricted to straight lines along the edges, this approach can also be extended to more complex movements. Furthermore, the weights associated with these edges are described in Section [3.1](#sec:edge_update){reference-type="ref" reference="sec:edge_update"}.

:::: {#fig:detection .figure latex-placement="h!"}
![](Ahmadi2025Adaptive_figs/1.png){#fig:detection_a width="\\linewidth"}

![](Ahmadi2025Adaptive_figs/2.png){#fig:detection_b width="\\linewidth"}

![](Ahmadi2025Adaptive_figs/3.png){#fig:detection_c width="\\linewidth"}

::: caption
Illustration of plant detection and graph construction: (a) detected plant rows represented as bounding rectangles, (b) graph nodes generated at the corners of the rectangles, and (c) directed edges added to form a complete graph structure.
:::
::::

Once the field is represented as a graph, a density function $\phi(v): \mathcal{V} \rightarrow \mathbb{R}^{+}$ is introduced over $\mathcal{G}$ to highlight regions of interest, meaning nodes with higher priority for servicing. In agricultural applications, these regions of interest may correspond to areas containing plants affected by biotic or abiotic stresses or exhibiting specific phenotypic traits, such as flowering or water accumulation in the crop field, among others. The density function $\phi(v)$ is derived from a continuous function defined over the original environment. Essentially, $\phi(v)$ is assigned larger values for nodes near the center, while nodes farther from the center receive smaller values.

## Problem Formulation

Consider a team of $n$ UGVs, denoted as $r^k$, $k \in \mathcal{K} = \{1, \ldots, n\}$, with initial positions given by $v_i^k = \left(x_i^k, y_i^k\right) \in \mathcal{V}$. Also, Each UGV is equipped with the necessary sensors, cameras, or actuators to perform its tasks.

Assumption 1: All UGVs have access to the graph $\mathcal{G}$ and possess complete knowledge of the density function $\phi: \mathcal{V} \rightarrow \mathbb{R}^{+}$.

**Problem:** *Develop a graph-based distributed coverage control strategy to deploy a team of UGVs for monitoring critical regions within the environment $Q$ while avoiding muddy patches or dynamic obstacles.*

**Practical value of the work:** Let us consider a fleet of autonomous UGVs equipped with a targeted-spray boom for pesticide application. A UAV first surveys the field (from above the canopy) to identify pest hotspots and communicates obstacle and terrain data (e.g., moving harvesters, irrigation machinery, muddy patches) to the UGVs. An adaptive coverage algorithm should allow the UGVs to dynamically adjust their path---avoiding obstacles in real time, ensuring complete, efficient coverage of the affected zones while reducing chemical use and labor. This scenario exemplifies just one of many practical applications that can benefit from our proposed methodology.

# Methodology {#sec:3}

The main results of this work are provided in this section. The subsequent subsections provide detailed descriptions of the edge weight assignment, partitioning strategy, and optimization framework that enable robust and adaptive coverage control. Also, the control strategy for an individual UGV and reference trajectory generation are adopted from [@davoodi2020heterogeneity].

## Edge Weight Assignment in the Graph {#sec:edge_update}

Consider the graph $\mathcal{G}(\mathcal{V}, \mathcal{E}, \mathcal{C})$. Initially, each edge $e_{ij} \in \mathcal{E}$ (connecting node $v_i$ to node $v_j$) is assigned a weight of $c_{ij}$ that is the Euclidean distance between the $v_i$ and $v_j$ in the agricultural field (see Fig. [4](#fig:detection){reference-type="ref" reference="fig:detection"}). Also, it is assumed that the UAV is capable of perceiving obstacle positions, velocities, and terrain conditions.

If an obstacle is detected on the edge connecting nodes $v_m$ and $v_n$ (i.e., $e_{mn}$), the weight corresponding to that edge is increased to reflect the obstacle's impact as $$\begin{equation}
\label{eq:obstacle}
    c_{mn} \leftarrow c_{mn} + \alpha .\exp({v_{\text{obs}}^2}/{v^2_{0}}),
\end{equation}$$ where $\alpha$ and $v_{0}$ are scaling factors modulating the influence of the obstacle, and $v_{\text{obs}}$ denotes the velocity of the detected obstacle.

Furthermore, to discourage paths that intersect with the predicted obstacle trajectory, the weights of edges along the obstacle's motion direction are penalized. The affected edges are selected based on the obstacle's velocity and graph connectivity, ensuring they align with the predicted path. Specifically, if an obstacle moves along an edge $e_{mn}$, the weights of $N$ subsequent edges in its motion direction are modified as $$\begin{equation}
\label{eq:sub_obstacle}
    c_{ij} \leftarrow c_{ij} + \alpha \exp({v_{\text{obs}}^2}/{v^2_{0}}) \cdot \exp(-{d_{edge}(e_{ij}, e_{mn})}/{d_0}),
\end{equation}$$

where $c_{ij}$ is the weight of the $ij$-th affected edge, $d_{edge}(e_{ij}, e_{mn})$ is computed as the sum of edge weights along the obstacle path connecting them, including $e_{mn}$ and $e_{ij}$ themselves. And, $d_0$ is a scaling factor that controls the decay rate of the penalty with distance.

Furthermore, to account for variations in terrain conditions, such as muddy areas, the weight of each edge of those areas is adjusted as $$\begin{equation}
\label{eq:muddy}
    c_{mn} \leftarrow c_{mn} + \beta . \exp(T_{mn}),
\end{equation}$$ where $\beta$ is a scaling factor, and $T_{mn}$ represents the terrain condition of the edge. The UAV will assess the condition and provide $T_{mn}$.

::: Remark
**Remark 1**. *The graph $\mathcal{G}$ is dynamically updated as obstacles move or terrain conditions change, ensuring that the edge weights reflect the latest environmental changes.*
:::

## Graph Partitioning and Cost Function

[]{#sec:graph_partitioning label="sec:graph_partitioning"} After updating the graph $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{C})$, consider a set of $n$ UGVs positioned at designated nodes $\{v_1, v_2, \dots, v_n\} \subset \mathcal{V}$. The goal is to partition $\mathcal{G}$ into $k$ disjoint subgraphs, denoted as $\{\mathcal{V}_1, \mathcal{V}_2, \dots, \mathcal{V}_n\}$, where each subgraph $\mathcal{V}_k$ represents a Voronoi-like cell assigned to agent $k$.

Next, we define a quantity $J^k_{v_i^k , v_j}(P^k)$ for each robot $r_k$ going from node $v^k_i$ to $v_j$ through path $P^k$. This function is designed to favor paths that minimize both distance and turning effort, ensuring a cost efficient movement. Formally, it is expressed as $$\begin{equation}
    J^k_{v_i^k , v_j} = \min_{P^k \in \mathcal{P}_{k}} \sum_{e_{ab} \in P^k} \Big(c_{ab} + \lambda C_{\text{turn}}(P^k)\Big)
    \label{eq:Jij}
\end{equation}$$ where $\mathcal{P}_k$ is the set of all the paths between the robot position node $v_i^k$ and node $v_j$ for robot $k$. The term $c_{ab}$ represents the weight associated with edge $e_{ab}$, and the summation accumulates these weights over all edges in the selected path. Additionally, $C_{\text{turn}}(P^k)$ is defined as $$\begin{equation}
    C_{\text{turn}}(P^k) = \sum_{j=1}^{k-1} \mathbb{I}(\theta_j \geq 90^\circ),
\end{equation}$$ where $\mathbb{I}(\theta_j \geq 90^\circ)$ is an indicator function that returns 1 if the turning angle $(\theta_j)$ between consecutive edges $e_{ij}$ and $e_{jk}$ is greater than or equal to 90 degrees, and 0 otherwise. The weighting parameter $\lambda$ in ([\[eq:Jij\]](#eq:Jij){reference-type="ref" reference="eq:Jij"}) allows for a trade-off between path length and smoothness, effectively controlling the preference for minimizing turns while maintaining efficiency in path selection.

Building upon this framework, as well as the results from [@yun2014distributed], the Voronoi-like partitions $\mathcal{V}_k$ generated by robot $k$ are defined as $$\begin{equation}
\label{eq:voronoi}
    \mathcal{V}_k = \left\{\mathcal{V}_k \in \mathcal{V} | J_{v_i^k , v_j^k} < J_{v_{i}^{k^{'}} , v_{j}^{k^{'}}}  \right\},
\end{equation}$$ where $k^{'}$ represents all robots in $\mathcal{K}$ except for the robot $k$. Note that the robot $k$ is responsible for monitoring all the events occurring within its assigned region $\mathcal{V}_k$. Then, the general deployment problem is formulated as minimizing the following cost function $$\begin{equation}
\label{eq:cost_function}
    \mathcal{H}(v_i, \mathcal{G})=\sum_{k=1}^n \sum_{v_j \in \mathcal{V}_i} J^k_{v_i^k, v_j} \tilde{\phi}\left(v_i^k, v_j\right),
\end{equation}$$ where $$\begin{equation}
\label{eq:density}
    \tilde{\phi}\left(v_i^k, v_j\right)= \begin{cases}\phi(v_j) & \text { if } v_i^k \neq v_j, \\ 0 & \text { if } v_i^k=v_j.\end{cases}
\end{equation}$$

It is noted that the function $\tilde{\phi}\left(v_i^k, v_j\right)$ prevents repetitive monitoring of the regions of interest by reducing their importance to zero after they are visited by one of the robots.

Next, an iterative approach is proposed to navigate the robots between the nodes, ensuring a continuous reduction in the locational optimization cost, $\mathcal{H}$, until all nodes with a nonzero value in $\phi$ have been visited. After each movement, the graph edge weights ($\mathcal{C}$) and partitions are updated. Subsequently, for each robot, the cost at its current position is evaluated and compared with the costs at its neighboring nodes. The robot moves to the neighboring node with the lowest cost if it offers a reduction in $\mathcal{H}$. If no neighboring node provides a lower cost, the robot remains in place until changes in the environment---such as the removal of an obstacle---allow for further movement. Also, if a robot reaches a node with a nonzero value in $\phi$, the value of $\phi$ at that node is set to zero.

The detailed methodology is presented in Algorithm [\[alg:template\]](#alg:template){reference-type="ref" reference="alg:template"}.

:::: algorithm
::: algorithmic
**Inputs:** 1. $\mathcal{G}(\mathcal{V}, \mathcal{E}, \mathcal{C})$ 2. $\{v_i^1, \dots, v_i^n\}$ 3. $\phi$ 4. $\alpha, \beta, v_{obs}, v_0, d_0, \lambda, N$

**Output:** Compute next best point for each robot.

$iter \gets 1$ Update the UGV's location, obstacles' positions and velocities, and directions. Update edges' weights (Eqs. [\[eq:obstacle\]](#eq:obstacle){reference-type="eqref" reference="eq:obstacle"}--[\[eq:muddy\]](#eq:muddy){reference-type="eqref" reference="eq:muddy"}). Update Voronoi-like partitioning (Eq. [\[eq:voronoi\]](#eq:voronoi){reference-type="eqref" reference="eq:voronoi"}). $\mathcal{H}^{iter}_k \gets$ compute cost function for current position of each UGV $k$. Compute the cost function for $v_i^k$'s neighbor nodes $\mathcal{N}_{\mathcal{G}}(v_i^k)$. $\mathcal{H}_a \gets$ minimum cost between neighboring nodes ($v_i^k$). $v_i^k \gets \text{corresponding node for } \mathcal{H}_a$ $\phi(v_i^k) \gets 0$ $iter \gets iter + 1$
:::
::::

# Simulation Results and Analysis {#sec:4}

As previously discussed, the proposed coverage control method accounts for dynamic (time varying) and static obstacles such as moving machinery and/or muddy soil patches. This section examines various aspects and capabilities of the developed approach through different case studies. The first case study analyzes a dynamic obstacle in the field and its impact on navigation. It includes a scenario for "regular dynamic obstacle," where obstacles are detected since entering the field and a "sudden dynamic obstacle" scenario, where they fail to be detected from the beginning. The second case investigates muddy soil patches and their effect on navigation accuracy. The scalars used throughout our simulation studies are $\alpha = 5m, \beta=1m, |v_{obs}|= 3 m/s, v_0 = 1 m/s, \lambda =0.1m, d_0 =1m$, and $N=3$.

## UGV Path Planning with Dynamic Obstacle Avoidance

The path planning strategy for the UGVs dynamically adapts to environmental changes by leveraging real-time data from the UAV. The UAV continuously tracks moving obstacles, providing their positions and velocities to the UGV, which integrates this information into a graph-based path-planning algorithm. The UGV continuously updates its trajectory to ensure collision-free navigation while maintaining efficiency. This is why we refer to it as adaptive. This adaptive mechanism enables safe and effective operation in dynamic agricultural environments. Figure [5](#fig:obs1_a){reference-type="ref" reference="fig:obs1_a"} shows the UGVs' trajectories when there is no obstacle , while Figure [8](#fig:no_obstacle_cost){reference-type="ref" reference="fig:no_obstacle_cost"} shows the coverage cost associated with it. These results serve as a baseline for comparison with other scenarios.

Figure [6](#fig:obs1_b){reference-type="ref" reference="fig:obs1_b"} illustrates UGV paths with obstacles, emphasizing the necessity of adaptive planning, while Fig. [9](#fig:with_obstacle_cost){reference-type="ref" reference="fig:with_obstacle_cost"} presents the corresponding cost analysis, demonstrating the impact of obstacle-induced deviations on path efficiency. The initial cost is higher than in the baseline (no-obstacle) scenario, since the early presence of obstacles increases the corresponding edge weights. Also, for clarity, Figure [13](#fig:regular_3D){reference-type="ref" reference="fig:regular_3D"} overlays the UGV and obstacle paths over time, confirming collision-free operation.

:::: {#fig:obs1 .figure latex-placement="h!"}
![Without obstacle](Ahmadi2025Adaptive_figs/No_obstacle.png){#fig:obs1_a width="\\linewidth"}

![With obstacle](Ahmadi2025Adaptive_figs/with_obstacle.png){#fig:obs1_b width="\\linewidth"}

::: caption
Comparison of UGV paths with and without the (moving) obstacles, indicating the impact of dynamic obstacle avoidance. See Fig. [13](#fig:regular_3D){reference-type="ref" reference="fig:regular_3D"} for the overlap between the UGV and obstacle trajectories.
:::
::::

:::: {#fig:obs1_cost .figure latex-placement="h!"}
![Without obstacle](Ahmadi2025Adaptive_figs/No_obstacle_cost.png){#fig:no_obstacle_cost width="\\linewidth"}

![With obstacle](Ahmadi2025Adaptive_figs/with_obstacle_cost.png){#fig:with_obstacle_cost width="\\linewidth"}

::: caption
Impact of dynamic obstacles on UGVs' coverage cost. Comparing the two plots clearly shows an increase in the cost due to the deviation of the UGVs from their optimal path to avoid dynamic obstacles; this also leads to longer time for the cost to converge to zero.
:::
::::

Now, in a more complicated scenario, if the UAV fails to detect an obstacle initially and a dynamic obstacle appears unexpectedly in the UGV's planned trajectory, the system must promptly find an alternative path to adapt to environmental changes. This rapid adjustment helps prevent potential collisions and operational disruptions. Such a capability is crucial for ensuring uninterrupted and reliable field coverage, particularly in dynamic agricultural environments (see Fig. [11](#fig:sudden_obs){reference-type="ref" reference="fig:sudden_obs"}). Also, as shown in Fig. [12](#fig:sudden_obs_cost){reference-type="ref" reference="fig:sudden_obs_cost"}, when obstacles are detected in $Iteration=10$ and $Iteration=16$, the coverage cost spikes but subsequently reduces. Figure [14](#fig:sudden_3D){reference-type="ref" reference="fig:sudden_3D"} overlays the UGV and obstacle trajectories over time, confirming collision-free operation. These results emphasize the robustness of the proposed approach in handling both predictable and unexpected changes in the environment.

![UGV trajectory adjustments in response to a sudden obstacle detected in the field, showcasing real-time re-planning capability. See Fig. [14](#fig:sudden_3D){reference-type="ref" reference="fig:sudden_3D"} for the overlap between the UGV and obstacle trajectories.](figs/Sudden_obstacle.png){#fig:sudden_obs width=".20 \\textwidth"}

![Coverage cost corresponding to sudden obstacles (Fig. [11](#fig:sudden_obs){reference-type="ref" reference="fig:sudden_obs"}), demonstrating the impact of sudden obstacles on path efficiency. Note that the cost spikes at obstacle detection instants (iterations 10 and 16) and gradually decreases as adaptive navigation adjusts the path.](figs/Sudden_obstacle_cost.eps){#fig:sudden_obs_cost width=".24 \\textwidth"}

:::: {#fig:3D_view .figure latex-placement="h!"}
![Regular dynamic obstacle](Ahmadi2025Adaptive_figs/with_obstacle_3D.png){#fig:regular_3D width="\\linewidth"}

![Sudden dynamic obstacle](Ahmadi2025Adaptive_figs/Sudden_obstacle_3D.png){#fig:sudden_3D width="\\linewidth"}

::: caption
Visualization of UGVs and obstacle trajectories over iterations, demonstrating successful dynamic obstacle avoidance. (a) Regular obstacle movement scenario. (b) Sudden obstacle appearance scenario.
:::
::::

![UGVs navigation in an environment with muddy soil patches, where terrain conditions influence path planning decisions. To avoid the muddy areas, UGVs needed to choose a longer path.](Ahmadi2025Adaptive_figs/Muddy_2.png){#fig:muddy_2 width=".25 \\textwidth"}

![Coverage cost for muddy scenario (Fig. [16](#fig:muddy_2){reference-type="ref" reference="fig:muddy_2"}). As observed, the cost (and paths' length) is increased when compared to the simple (no-obstacle) scenario in Fig. 2(a).](figs/Muddy_2_cost.eps){#fig:muddy_2_cost width=".27 \\textwidth"}

## UGV Path Planning for Muddy Areas

To improve navigation in muddy areas, the UGV path planning employs a weighted graph approach that adjusts for varying terrain conditions. Muddy regions, which hinder UGVs movement, are identified through image analysis or pre-existing field data. These regions are represented as higher-weighted edges in the graph, reflecting increased traversal costs (Figure [16](#fig:muddy_2){reference-type="ref" reference="fig:muddy_2"}). The algorithm prioritizes paths with lower cumulative weights, steering UGVs away from muddy regions whenever possible. This strategy enhances navigation efficiency and reliability by reducing the risk of immobilization and optimizing route selection for smooth field traversal. The impact of muddy terrain on cost function is showed in Figure [17](#fig:muddy_2_cost){reference-type="ref" reference="fig:muddy_2_cost"}. Cost and trajectory can be compared to Figure [5](#fig:obs1_a){reference-type="ref" reference="fig:obs1_a"} and Figure [8](#fig:no_obstacle_cost){reference-type="ref" reference="fig:no_obstacle_cost"} when there is no obstacle and muddy region in the field.

# Conclusion and Future Work {#sec:5}

In this paper, we proposed a coverage control method for autonomous field navigation that dynamically adapts to obstacles and environmental changes. Our approach combines UAV-based (remote) sensing with UGV path planning in a weighted graph framework, enabling real-time obstacle avoidance and efficient terrain-aware navigation. By leveraging Voronoi-based node assignment, adaptive edge weight updates, and cost-based optimization, our method ensures robust coverage in dynamic environments. Simulation results demonstrated the effectiveness of the proposed approach in handling moving obstacles, adapting to muddy terrains, and re-planning paths efficiently in response to sudden environmental changes. The results confirmed that our strategy significantly improves path planning efficiency while minimizing traversal cost and unnecessary detours.

Future research includes extending the framework to multi-UGV coordination with decentralized decision-making, incorporating machine learning for predictive obstacle modeling, and conducting real-world field experiments to validate the system's performance in practical agricultural scenarios. By further enhancing adaptability and scalability, this approach can contribute to more efficient and autonomous precision agriculture solutions.

[^1]: This work is supported by the Data Science for Food and Agricultural Systems (DSFAS) program, award no. 2020-67021-40004, from the U.S. Department of Agriculture's National Institute of Food and Agriculture (NIFA).
