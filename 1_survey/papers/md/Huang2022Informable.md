---
citation_key: Huang2022Informable
arxiv_id: 2205.14853
arxiv_url: https://arxiv.org/abs/2205.14853
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:22:41Z
origin: ai+web
reviewed: false
---

# Introduction and Contributions {#sec:Intro}

Multi-objective or multi-destination path planning is a key enabler of applications such as data collection [@faigl2014unifying; @hu2020aoi; @samir2019uav], traditional Traveling Salesman Problem (TSP) [@junger1995traveling; @applegate2011traveling], and electric vehicle charging for long trips. More recently, autonomous "Mobility as a Service" (e.g., autonomous shuttles or other local transport between user-selected points) has become another important application of multi-objective planning such as car-pooling [@ma2018path; @huang2018multimodal; @al2019deeppool; @hulagu2020electric] Therefore, being able to efficiently find paths connecting multiple destinations and to determine the visiting order of the destinations (essentially, a relaxed TSP) is critical for modern navigation systems deployed by autonomous vehicles and robots. This paper seeks to solve these two problems by developing a system composed of a sampling-based anytime path planning algorithm and a relaxed-TSP solver.

Another application of multi-objective path planning is robotics inspection, where a list of inspection waypoints is often provided so that the robot can preferentially examine certain equipment or areas of interest or avoid certain areas in a factory, for example. The pre-defined waypoints can be considered as prior knowledge for the overall inspection path the robot needs to construct for task completion. We show that the proposed system can inherently incorporate such knowledge.

:::: {#fig:FirstImg .figure latex-placement="!t"}
     

::: {.caption short-caption=""}
Illustration of the proposed informable multi-objective and multi-directional RRT$^\ast$ ($\text{IMOMD-RRT}^*$) system evaluated on OpenStreetMap of Chicago, containing $866,089$ nodes and $1,038,414$ edges. The green, red, and orange dots are the source, target, and objectives, respectively. shows the initial stage of the tree expansion of each destination. shows the trees from each destination form a connected graph. shows the first path and visiting order from the $\text{IMOMD-RRT}^*$. Given more computation time, shows that $\text{IMOMD-RRT}^*$ returns a better path and order.
:::
::::

To represent multiple destinations, graphs composed of nodes and edges stand out for their sparse representations. In particular, graphs are a popular representation of topological landscape features, such as terrain contour, lane markers, or intersections [@OpenStreetMap]. Topological features do not change often; thus, they are maintainable and suitable for long-term support compared to high-definition (HD) maps. Graph-based maps such as OpenStreetMap [@OpenStreetMap] have been developed over the past two decades to describe topological features and are readily available worldwide. Therefore, we concentrate on developing the proposed informable multi-objective and multi-directional rapidly-exploring random trees (RRT$^\ast$) system for path planning on large and complex graphs.

A multi-objective path planning system is charged with two tasks: **1)** find weighted paths (i.e., paths and traversal costs), if they exist, that connect the various destinations. This operation results in an undirected and weighted graph where nodes and edges correspond to destinations and paths connecting destinations, respectively. **2)** determine the visiting order of destinations that minimizes total travel cost. The second task, called relaxed TSP, differs from standard TSP in that we are allowed to (or sometimes have to) visit a node multiple times; see Sec. [2.3](#sec:MO-TSP){reference-type="ref" reference="sec:MO-TSP"} for a detailed discussion. Several approaches [@janovs2021multi; @devaurs2014multi; @vonasek2019space; @englot2011multi] have been developed to solve each of these tasks separately, assuming either the visiting order of the destinations is given, or a cyclic/complete graph is constructed and the weights of edges are provided. However, in real-time applications, the connectivity of the destinations and the weights of the paths between destinations (task 1) as well as the visiting order of the destinations (task 2) are often unknown. It is crucial that we are able to solve these two tasks concurrently in an anytime manner, meaning that the system can provide suboptimal but monotonically improving solutions at any time throughout the path cost minimization process.

In this paper, we seek to develop an anytime iterative system to provide paths between multiple objectives and to determine the visiting order of destinations; moreover, the system should be informable meaning it can accommodate prior knowledge of intermediate nodes, if available. The proposed system consists of two components: **1)** an anytime informable multi-objective and multi-directional RRT$^*$ ($\text{IMOMD-RRT}^*$) algorithm to form a connected weighted-undirected graph, and **2)** a relaxed TSP solver that consists of an enhanced version of the cheapest insertion algorithm [@rosenkrantz1977analysis] and a genetic algorithm [@potvin1996genetic; @moon2002efficient; @braun1990solving; @ahmed2010genetic], which together we call ECI-Gen. The proposed system is evaluated on large-complex graphs built for real-world driving applications, such as the OpenStreetMap of Chicago containing $866,089$ nodes and $1,038,414$ edges that is shown in Fig. [1](#fig:FirstImg){reference-type="ref" reference="fig:FirstImg"}.

:::: {#fig:SystemDiagram .figure latex-placement="t"}
![](Huang2022Informable_figs/system_diagram.png){width="1\\columnwidth"}

::: caption
Illustration of the proposed $\text{IMOMD-RRT}^*$ system. It consists of an anytime informable multi-objective and multi-directional RRT$^*$ ($\text{IMOMD-RRT}^*$) algorithm to construct a connected weighted-undirected graph, and a polynomial-time solver to solve the relaxed TSP. The solver consists of an enhanced version of the cheapest insertion algorithm [@rosenkrantz1977analysis] and a genetic algorithm [@potvin1996genetic; @moon2002efficient; @braun1990solving], called ECI-Gen solver. The full system (the blue box) will continue to run to further improve the solution over time.
:::
::::

The overall system is shown in Fig. [2](#fig:SystemDiagram){reference-type="ref" reference="fig:SystemDiagram"} includes the following contributions:

1.  An anytime informable multi-objective and multi-directional RRT$^*$ ($\text{IMOMD-RRT}^*$) system that functions on large-complex graphs. The anytime features means that the system quickly constructs a path on a large-scale undirected weighted graph that meets the existence constraint (the solution path must passes by all the objectives at least once), and the order constraint (with fixed starting point and end point). Therefore, the resulting weighted reduced graph containing the objectives, source, and target is connected.

2.  The problem of determining the visiting order of destinations of the connected graph is a relaxed TSP (R-TSP) with fixed start and end nodes, though intermediate nodes can be (or sometimes must be) visited more than once. We introduce the ECI-Gen solver, which is based on an enhancement of the cheapest insertion algorithm [@rosenkrantz1977analysis] and a genetic algorithm [@potvin1996genetic; @moon2002efficient; @braun1990solving; @ahmed2010genetic] to solve the R-TSP in polynomial time.

3.  We show that prior knowledge (such as a reference path) for robotics inspection of a pipe or factory can be readily and inherently integrated into the $\text{IMOMD-RRT}^*$. In addition, providing the prior knowledge to the planner can help navigate through challenging topology.

4.  We evaluate the system comprised of $\text{IMOMD-RRT}^*$ and the ECI-Gen solver on large-scale graphs built for real world driving applications, where the large number of intermediate destinations precludes solving the ordering by brute force. We show that the proposed IMOMD-RRT$^\ast$ outperforms bi-directional A$^*$ [@BiAstar] and ANA$^*$ [@ANAstar] in terms of speed and memory usage in large and complex graphs. We also demonstrate by providing a reference path, the $\text{IMOMD-RRT}^*$ escapes from bug traps (e.g., single entry neighborhoods) in complex graphs.

5.  We open-source the multi-threaded C++ implementation of the system at\
    <https://github.com/UMich-BipedLab/IMOMD-RRTStar>.

The remainder of this paper is organized as follows. Section [2](#sec:RelatedWork){reference-type="ref" reference="sec:RelatedWork"} summarizes the related work. Section [3](#sec:IMOMDRRT){reference-type="ref" reference="sec:IMOMDRRT"} explains the proposed anytime informable multi-objective and multi-directional RRT$^*$ to construct a simple connected graph. The ECI-Gen solver to determine the ordering of destinations in the connected graph is discussed in Sec. [4](#sec:WIBSFRTSP){reference-type="ref" reference="sec:WIBSFRTSP"}. Experimental evaluations of the proposed system on large-complex graphs are presented in Sec. [5](#sec:Experiments){reference-type="ref" reference="sec:Experiments"}. Finally, Sec. [6](#sec:Conclusion){reference-type="ref" reference="sec:Conclusion"} concludes the paper and provides suggestions for future work.

# Related Work {#sec:RelatedWork}

Path planning is an essential component of robot autonomy. In this section, we review several types of path planning algorithms and techniques to improve their efficiency. Furthermore, we compare the proposed system with existing literature on car-pooling/ride-sharing and the traveling salesman problem.

## Common Path Planners {#sec:CommonPathPlanners}

Path planners are algorithms to find the shortest path from a single source to a single target. Graph-based and sampling-based algorithms are the two prominent categories.

Graph-based algorithms [@AStar; @BiAstar; @dijkstra; @Rstar; @ARAstar; @ANAstar; @JPS] such as Dijkstra[@dijkstra] and $\text{A}^*$ [@AStar] discretize a continuous space to an undirected graph composed of nodes and weighted edges. They are popular for their efficiency on low-dimensional configuration spaces and small graphs. There are many techniques[@BiAstar; @Rstar; @ARAstar; @ANAstar; @JPS] to improve their computation efficiency on large graphs. Inflating the heuristic value makes the $\text{A}^*$ algorithm likely to expand the nodes that are close to the goal and results in sacrificing the quality of solution. Anytime Repairing $\text{A}^*$ (ARA$^*$) [@ARAstar] utilizes weighted $\text{A}^*$ and keeps decreasing the weight parameter at each iteration, and therefore leads to a better solution. Anytime Non-parametric $\text{A}^*$ (ANA$^*$) [@ANAstar] is as efficient as ARA$^*$ and spends less time between solution improvements. R$^*$ [@Rstar] is a randomized version of $\text{A}^*$ to improve performance. Algorithms such as Jumping Point Search [@JPS] to improve exploration efficiency only work for grid maps. However, graph-based algorithms inherently suffer from bug traps, whereas sampling-based methods can overcome bug traps more easily via informed sampling; see Sec. [5](#sec:Experiments){reference-type="ref" reference="sec:Experiments"} for a detailed discussion.

Sampling-based algorithms such as rapidly-exploring random trees (RRT) [@VanillaRRT] stand out for their low complexity and high efficiency in exploring higher-dimensional, continuous configuration spaces. Its asymptotically optimal version -- $\text{RRT}^*$ [@RRTStar; @RRTStarICRA; @huang2021efficient] -- has also gained much attention and has contributed to the spread of the RRT family. More recently, sampling-based algorithms on discrete spaces such as RRLT and d-RRT$^*$ have been applied to multi-robot motion planning[@morgan2004sampling; @branicky2003rrts; @dRRT; @dRRTstar]. We seek to leverage $\text{RRT}^*$ to construct a simple connected graph that contains multiple destinations from a large-complex map, as well as to accommodate prior knowledge of a reference path.

## Car-Pooling and ride-sharing

Problems such as car-pooling, ride-sharing, food delivery, or combining public transportation and car-pooling handle different types of constraints such as maximum seats, time window, battery charge, number of served requests along with multiple destinations [@ma2018path; @huang2018multimodal; @al2019deeppool; @huang2018ant; @duan2018optimizing; @tamannaei2019carpooling; @hulagu2020electric; @suman2019improvement; @lyu2019cb; @simoni2020optimization; @naccache2018multi; @nazari2018reinforcement; @lu2019hybrid]. These problems are usually solved by Genetic Algorithms [@ma2018path], Ant Colony Optimization [@huang2018ant; @lu2019hybrid], Dynamic Programming [@lyu2019cb; @simoni2020optimization] or reinforcement learning [@al2019deeppool; @nazari2018reinforcement]. These methods assume, however, that weighted paths between destinations in the graph are already known[@ma2018path; @huang2018ant; @lu2019hybrid; @simoni2020optimization; @al2019deeppool; @duan2018optimizing; @suman2019improvement], while in practice, the connecting paths and their weights are unknown and must be constructed.

:::: {#fig:Hamiltonian .figure latex-placement="t"}
::: {.caption short-caption=""}
shows a *simple connected graph* where the objectives have to be visited twice to visit all destinations. shows the case where revisiting the source $v_{\text{s}}$ allows a shorter path when triangular inequality does not hold.
:::
::::

## Multi-objective Path Planners and Traveling Salesman Problem {#sec:MO-TSP}

Determining the travel order of nodes in an undirected graph with known edge weights is referred to as a Traveling Salesman Problem (TSP). The TSP is a classic NP-hard problem about finding a shortest possible cycle that visits every node exactly once and returns to the start node [@applegate2011traveling; @junger1995traveling]. Another variant of TSP, called the shortest Hamiltonian path problem[@junger1995traveling], is to find the shortest path that visits all nodes exactly once between a fixed starting node ($v_s$) and a fixed terminating node ($v_t$). The problem can be solved as a standard TSP problem by assigning sufficiently large negative cost to the edge between $v_s$ and $v_t$ [@junger1995traveling; @applegate2011traveling].

We are inspired by the work of [@vonasek2019space; @janovs2021multi], where the authors propose to solve the problem through a single-phase algorithm in simulated continuous configuration spaces. They first leverage multiple random trees to solve the multi-goal path planning problem and then solve the TSP via an open-source solver. In particular, they assume that the paths between nodes in the continuous spaces can be constructed in single pass and that the resulting graph can always form a cycle in their simulation environment. Thus, the problem can then be solved by a traditional TSP solver. In practice, however, the graph might not form a cycle (e.g., an acyclic graph or a forest) as shown in Fig. [\[subfig:Acyclic\]](#subfig:Acyclic){reference-type="ref" reference="subfig:Acyclic"}, and even if the graph is cyclic or there exists a Hamiltonian path, there is no guarantee the path is the shortest. In Fig. [\[subfig:BadHamiltonian\]](#subfig:BadHamiltonian){reference-type="ref" reference="subfig:BadHamiltonian"}, the Hamiltonian path simply is $v_s\rightarrow o_1\rightarrow v_t$, and the traversed distance is $12$. However, another shorter path exists if we are allowed to traverse a node ($v_s$ in this case) more than once: $v_s\rightarrow o_1\rightarrow v_s\rightarrow v_t$ and the distance is $7$. We therefore propose a polynomial-time solver for this relaxed TSP problem; see Sec. [4](#sec:WIBSFRTSP){reference-type="ref" reference="sec:WIBSFRTSP"} for further discussion.

# Informable Multi-objecticve and Multi-directional RRT$^\ast$ {#sec:IMOMDRRT}

This section introduces an anytime informable multi-objective and multi-directional Rapidly-exploring Random Tree$^*$ ($\text{IMOMD-RRT}^*$) algorithm as a real-time means to quickly construct from a large-scale map a weighted undirected graph that meets the existence constraint (the solution trajectory must pass by all the objectives at least once), and the order constraint (with fixed starting point and end point). In other words, the $\text{IMOMD-RRT}^*$ forms a simple[^1] connected graph containing the objectives, source, and target.

## Standard $\text{RRT}^*$ Algorithm

The original $\text{RRT}^*$ [@RRTStar] is a sampling-based planner with guaranteed asymptotic optimality in continuous configuration spaces. In general, $\text{RRT}^*$  grows a tree where nodes are connected by edges of linear path segments. Additionally, $\text{RRT}^*$ considers nearby nodes of a newly extended node when choosing the best parent node and when rewiring the graph to find shorter paths for asymptotic optimality.

## Multi-objective and Multi-directional $\text{RRT}^*$ on Graphs {#sec:RRTOnGraphs}

In this paper, we use *map* to refer to the input graph, which might contain millions of nodes, and use *graph* to refer to the graph composed of only the destinations including the source and target node. The proposed $\text{IMOMD-RRT}^*$ differs from the original $\text{RRT}^*$ in six aspects when growing a tree. First, the sampling is performed by picking a random $v_\text{rand}$ in the map, and not from an underlying continuous space. The goal bias is not only applied to the target but also the source and all the objectives. Second, a steering function directly finds the closest expandable node as $v_\text{new}$ to the random node $v_\text{rand}$, without finding the nearest node in the tree, as shown in Fig. [\[subfig:expandable\]](#subfig:expandable){reference-type="ref" reference="subfig:expandable"}. Note that instead of directly sampling from the set of expandable nodes, sampling from the map ameliorates the bias of sampling on the explored area. Third, the parent node is chosen from the nodes connected with the new node $v_\text{new}$, called the neighbor nodes. Among the neighbor nodes, the node that yields the lowest path cost from the root becomes the new node's parent. Fourth, the jumping point search algorithm [@JPS] is also leveraged to speed up tree exploration. Fifth, the $\text{IMOMD-RRT}^*$ rewires the neighborhood nodes to minimize the accumulated cost from the root of a tree to $v_\text{new}$, as shown in Fig. [\[subfig:rewiring\]](#subfig:rewiring){reference-type="ref" reference="subfig:rewiring"}. Lastly, if $v_\text{new}$ belongs to more than one tree, this node is considered a connection node, which connects the path between destinations, as shown in Fig. [5](#fig:UpdateConnection){reference-type="ref" reference="fig:UpdateConnection"}.

:::: {#fig:expandable .figure latex-placement="t"}
 

::: {.caption short-caption=""}
Illustration of tree expansion and connection nodes of a tree. The unexplored paths in the graph and the spanning tree are represented by the gray and yellow lines, respectively. The green-dashed circles are the expandable nodes. shows the tree $\mathcal{T}_i$ extends to the $v_\text{rand}$ by growing a node $v_\text{new}$ to the closest expandable node. shows the updated set $\mathcal{X}_i$ of expandable nodes and the tree is rewired around the $v_\text{new}$. The rewired nodes $v_\text{near}$ are represented as the blue dots.
:::
::::

:::: {#fig:UpdateConnection .figure latex-placement="t"}
   

::: {.caption short-caption=""}
Illustration of better connection nodes resulting in a better path. Two trees rooted at $d_i$ and $d_k$ are marked in yellow and green, respectively. The highlighted purple line shows the shortest path between $d_i$ and $d_k$. The newly extended node $v_\text{new}$ (dashed-red circles) is added to a set of connection nodes $\mathcal{C}_{ik}$. The element of the distance matrix, $A_{ik}$, and the connection node $c_{ik}^{*}$ that generates the shortest path between the destination $d_i$ and $d_k$ are updated as a shorter path is found.
:::
::::

Our proposed graph-based $\text{RRT}^*$ modification is summarized below with notation that generally follows graph theory [@bondy1976graph]. A graph $\mathcal{G}$ is an ordered triple $(\mathcal{V}(\mathcal{G}), \mathcal{E}(\mathcal{G}), \Phi_\mathcal{G})$, where $\mathcal{V}(\mathcal{G}) = \{v\in\zeta\}$ is a set of nodes in the robot state space $\zeta$, $\mathcal{E}(\mathcal{G})$ is a set of edges (disjoint from $\mathcal{V}(\mathcal{G})$), and an indication function $\Phi_\mathcal{G}$ that associates each edge of $\mathcal{G}$ with an unordered pair (not necessarily distinct) of nodes of $\mathcal{G}$.

Given a set of destinations $\mathcal{D}= \{d_i|d_i\in\{v_s, v_t\} \cup \mathcal{O}\}_{i=1}^{m+2}$, where $v_s\in\mathcal{V}(\mathcal{G})$ is the source node, $v_t\in\mathcal{V}(\mathcal{G})$ is the target node, and $\mathcal{O}\subseteq\mathcal{V}(\mathcal{G})$ is the set of $m$ objectives, the $\text{IMOMD-RRT}^*$ solves the multi-objective planning problem by growing a tree $\mathcal{T}_i = (V, E)$, where $V\subseteq\mathcal{V}(\mathcal{G})$ is a set of nodes connected by edges $E\subseteq\mathcal{E}(\mathcal{G})$, at each of the destinations $d_i\in\mathcal{D}$. Thus, it leads to a family of trees $\mathcal{T}
= \{\mathcal{T}_1, \cdots, \mathcal{T}_m, \mathcal{T}_{m+1}, \mathcal{T}_{m+2} \}$.

The proposed $\text{IMOMD-RRT}^*$ explores the graph $\mathcal{G}$ by random sampling from $\mathcal{V}(\mathcal{G})$ and extending nodes to grow each tree. We explain a few important functions of IMOMD-RRT$^\ast$ below.

### Tree Expansion

Let ${\mathcal{N}(v)}$ be the set of nodes directly connected with a node, i.e., the neighborhood of a node $v$ [@bondy1976graph]. A node is expandable if there exists at least one unvisited node connected and at least one node of the tree connected, shown as the dashed-green circles in Fig [\[subfig:expandable\]](#subfig:expandable){reference-type="ref" reference="subfig:expandable"}. Let $\mathcal{X}_i$ be the set of expandable nodes of the tree $\mathcal{T}_i$. A random node $v_\text{rand}$ is sampled from the nodes of the graph $\mathcal{V}(\mathcal{G})$. Next, find the nearest node $v_\text{new}$ in the set of expandable nodes $\mathcal{X}_i$: $$\begin{equation}
\label{eq:NearestNode}
    v_\text{new} = \underset{v \in  \mathcal{X}_i }{\mathop{\mathrm{arg\,min}}} \, \mathtt{Dist}(v, v_\text{rand}),
\end{equation}$$ where $\mathtt{Dist(\cdot, \cdot)}$ is the distance between two states. Next, the jumping point search algorithm[@JPS] is utilized to speed up the tree expansion. If the current $v_\text{new}$ has only one neighbor that is not already in the tree, $v_\text{new}$ is added to the tree and that one neighbor is selected as the new $v_\text{new}$. This process continues until $v_\text{new}$ has at least two neighbors that are not in tree, or it reaches $v_\text{rand}$.

### Parent Selection

Let the set $\mathcal{N}_i({v_\text{new})}$ be the neighborhood of the $v_\text{new}$ in the tree $\mathcal{T}_i$. The node $v_\text{near}$ in $\mathcal{N}_i({v_\text{new})}$ that results in the smallest cost-to-come, $\mathtt{Cost(\cdot,
\cdot)}$, is the parent of the $v_\text{new}$ and is determined by: $$\begin{equation}
 v_\text{parent} =
\underset{v_\text{near} \in \mathcal{N}_i({v_\text{new})}}{\mathop{\mathrm{arg\,min}}} \{
\mathtt{Cost}(\mathcal{T}_i, v_\text{near}) + \mathtt{Dist}(v_\text{near}, v_\text{new})
\}.
\end{equation}$$ Next, all the unvisted nodes in $\mathcal{N}_i({v_\text{new})}$ are added to the set of expandable nodes $\mathcal{X}_i$.

### Tree Rewiring

After the parent node is chosen, the nearby nodes are rewired if a shorter path reaching the node through the $v_\text{new}$ is found, as shown in Fig. [\[subfig:rewiring\]](#subfig:rewiring){reference-type="ref" reference="subfig:rewiring"}. The rewiring step guarantees asymptotic optimality, as with the classic algorithm.

### Update of Tree Connection

A node is a connection node if it belongs to more than one tree. Let $\mathcal{C}_{ik}$ be the set of connection nodes between $\mathcal{T}_i$ and $\mathcal{T}_k$, and let $c_{ik}^*$ denote the node that connects $\mathcal{T}_i$ and $\mathcal{T}_k$ with the shortest distance $$\begin{equation}
    c_{ik}^{*} = \underset{c \in \mathcal{C}_{ik}}{\mathop{\mathrm{arg\,min}}}~\{ \mathtt{Cost}(\mathcal{T}_i, c) + \mathtt{Cost}(\mathcal{T}_k, c) \}.
\end{equation}$$ Let $A_{(m+2)\times (m+2)}$ be a distance matrix that represents pairwise distances between the destinations, where $m$ is the number of objectives. The element $A_{i,k}$ indicates the shortest path between destinations $d_i$ and $d_k$, as shown in Fig. [\[subfig:update_connection\]](#subfig:update_connection){reference-type="ref" reference="subfig:update_connection"}. $A_{i,k}$ is computed as $$\begin{equation}
     A_{i,k} = \mathtt{Cost}(\mathcal{T}_i, c_{ik}^{*}) + \mathtt{Cost}(\mathcal{T}_k, c_{ik}^{*}).
\end{equation}$$

## Discussion of Informability {#sec:Informable}

As mentioned in Sec. [1](#sec:Intro){reference-type="ref" reference="sec:Intro"}, applications such as robotic inspection or vehicle routing might consider prior knowledge of the path, so that the robot can examine certain equipment or area of interests or avoid certain areas in a factory. The prior knowledge can be naturally provided as a number of "pseudo destinations" or samples in the $\text{IMOMD-RRT}^*$. A pseudo destination is an artificial destination to help $\text{IMOMD-RRT}^*$ to form a connected graph. However, unlike *true* destinations that will always be visited, a pseudo destination might not be visited after rewiring, as shown in Fig. [6](#fig:informability){reference-type="ref" reference="fig:informability"}. Prior knowledge through pseudo destinations can also be leveraged to traverse challenging topology, such as bug-traps; see Sec. [5](#sec:Experiments){reference-type="ref" reference="sec:Experiments"}.

::: remark
One can decide if the order of the pseudo destinations should be fixed or even the pseudo destinations should be objectives (i.e., they will not be removed in the rewiring process.).
:::

:::: {#fig:informability .figure latex-placement="t"}
::: {.caption short-caption=""}
Illustration of the rewired path of pseudo-destinations. $d_1-d_4$ are the destinations and marked in different colors. The dashed-red circles are the connection nodes between two trees. The thick purple line is the final path. shows the resulting path as if $d_1-d_4$ are "true" destinations, and is the resulting path as if $d_2-d_3$ are "pseudo" destinations. The real destinations have to be visited as shown in , whereas pseudo destinations are artificial destinations to help form a connected graph, and might no longer be visited after rewiring
:::
::::

# Enhanced Cheapest Insertion and Genetic Algorithm {#sec:WIBSFRTSP}

This section introduces a polynomial-time solver for the relaxed traveling salesman problem (R-TSP).

## Relaxed Traveling Salesman Problem {#sec:RelaxedTSP}

The R-TSP differs from standard TSP[@applegate2011traveling; @junger1995traveling; @punnen2007traveling] in two perspectives. First, nodes are allowed to be visited more than once, as mentioned in Sec. [2.3](#sec:MO-TSP){reference-type="ref" reference="sec:MO-TSP"}. Second, we have a source node where we start and a target node where we end. Therefore, the R-TSP can also be considered a relaxed Hamiltonian path problem[@junger1995traveling; @punnen2007traveling]. We propose the ECI-Gen solver, which consists of an enhanced version of the cheapest insertion algorithm [@rosenkrantz1977analysis] and a genetic algorithm [@potvin1996genetic; @moon2002efficient; @braun1990solving] to solve the R-TSP. The complexity of the proposed solver is $O(N^3)$, where $N$ is the cardinality of the destination set $\mathcal{D}$.

## Graph Definitions and Connectivity

In graph theory [@west2001introduction; @bondy1976graph], a graph is simple or strict if it has no loops and no two edges join the same pair of nodes. In addition, a path is a sequence of nodes in the graph, where consecutive nodes in the sequence are adjacent, and no node appears more than once in the sequence. A graph is connected if and only if there is a path between each pair of destinations. Once all the destinations form a simple-connected graph, there exists at least one path $\pi$ that passes all destinations $\mathcal{D}$. We can then consider the problem as an R-TSP (see Sec. [4.1](#sec:RelaxedTSP){reference-type="ref" reference="sec:RelaxedTSP"}), where we have a source and target node as well as several objectives to be visited. Therefore, we impose the graph connectivity and simplicity as sufficient conditions to solve the R-TSP. The disjoint-set data structure [@cormen2022introduction; @galil1991data] is implemented to verify the connectivity of a graph.

## Enhanced Cheapest Insertion Algorithm {#sec:WIBFS}

The regular cheapest insertion algorithm[@rosenkrantz1977analysis] provides an efficient means to find a sub-optimal sequence that guarantees less than twice the optimal sequence cost. However, it does not handle the case where revisiting the same node makes a shorter sequence. Therefore, we propose an enhanced version of the cheapest insertion algorithm, which comprises of a set of actions: **1)** in-sequence insertion, $\lambda_\text{in-sequence}$, which is the regular cheapest insertion; **2)** in-place insertion, $\lambda_\text{in-place}$, to allow the algorithm to revisit existing nodes; and **3)** swapping insertion, $\lambda_\text{swapping}$, which is inspired by genetic algorithms. Finally, sequence refinement is performed at the end of the algorithm.

:::: {#fig:insertion .figure latex-placement="t"}
     

::: {.caption short-caption=""}
Illustration of the insertion cost. shows the in-place insertion and the resulting sequence contains duplicated $s_i$. shows the in-sequence insertion without a duplicated element.
:::
::::

Let the current sequence be $\mathcal{S}_{\text{current}} = \{ v_{s},s_{1}, \cdots,
s_{i},s_{i+1},\cdots, s_{n}, v_{t}\}$ to indicate the visiting order of destinations, where $s_{\{\cdot\}}\in\mathcal{D}$ and $(n+2)$ is the number of destinations in the sequence. The travel cost $\theta(\cdot,\cdot)$ is the path distance between two destinations provided by the $\text{IMOMD-RRT}^*$. The $\mathcal{S}_{\text{current}}$ is constructed by Dijkstra's algorithm on the graph.

::: remark
$\mathcal{S}_{\text{current}}$ possibly contains duplicated elements and $s_i$ is not necessary $d_i$. Therefore, the number of destinations in the sequence $n$ may be larger than the actual number of destinations $m$. Fig. [\[fig:inplace\]](#fig:inplace){reference-type="ref" reference="fig:inplace"} shows the duplicated case with $\mathcal{S}_{\text{current}} = \{ v_s, s_1, \cdots, s_i,
    d_k, s_i, s_{i+1}, \cdots, s_n, v_t\}$, where $s_i$ is duplicated. Figure [\[fig:insequence\]](#fig:insequence){reference-type="ref" reference="fig:insequence"} illustrates an unduplicated case where $\mathcal{S}_{\text{current}} = \{ v_s, s_1, \cdots,s_i, d_k, s_{i+1},$\
$\cdots, s_n, v_t\}$.
:::

Let $\mathcal{K}$ denote the set of destinations to be inserted, and let the to-be-inserted destination be $d_k$ and its ancestor be $s_i$, where $d_k\in\mathcal{K}$ and $s_i\in\mathcal{S}_\text{current}$. Given a current sequence $\mathcal{S}_{\text{current}}$, the location to insert $s^*$, and the action of insertion $\lambda^*$ are determined by $$\begin{equation}
\label{eq:bestInsertionPlan}
    \lambda^*, s^* =
    \mathop{\mathrm{arg\,min}}_{\substack{\lambda_j\in\Lambda \\ 
                    s_i\in \mathcal{S}_\text{current}
              }
          }\lambda_j(s_i,d_k),
\end{equation}$$ where $\Lambda = \{\lambda_\text{in-sequence}, \lambda_\text{in-place}, \lambda_\text{swapping}\}$ is the set of the insertion actions.

### In-place Insertion $\lambda_\text{in-place}$

This step detours from $s_{i}$ to $d_{k}$, and the resulting sequence is $\mathcal{S}_{\text{modified}} = \{ v_{s}, s_1 \cdots, s_{i}, d_{k}, s_{i}, s_{i+1},
\cdots, s_{n}, v_{t}\}$, as shown in Fig. [\[fig:inplace\]](#fig:inplace){reference-type="ref" reference="fig:inplace"}. The insertion distance is $$\begin{equation}
    \lambda_\text{in-place}(s_i,d_k)=2\theta(s_i,d_k).
\end{equation}$$

### In-sequence Insertion $\lambda_\text{in-sequence}$

This step inserts $d_{k}$ between $s_{i}$ and $s_{i+1}$ ($\forall s_i\in\{\mathcal{S}_\text{current}/(v_t)\}$), and the resulting sequence is $\mathcal{S}_{\text{modified}} = \{ v_{s}, s_{1}, \cdots, s_{i}, d_{k}, s_{i+1},
    \cdots, s_{n}, v_{t}\}$, as shown in Fig. [\[fig:insequence\]](#fig:insequence){reference-type="ref" reference="fig:insequence"}. The insertion distance is $$\begin{equation}
    \begin{aligned}
        \lambda_\text{in-sequence}(s_i,d_k) = \theta(s_i,d_k) + \theta(d_k, s_{i+1}) - \theta(s_i,s_{i+1}).
    \end{aligned}
\end{equation}$$

### Swapping Insertion $\lambda_\text{swapping}$

The swapping insertion changes the order of nodes right next to the newly inserted node. There are three cases in swapping insertion: swapping left, right, or both. For the case of swapping left, the modified sequence is $\mathcal{S}_\text{modified} = \{ v_{s}, s_1 \cdots, s_{i-2}, s_{i}, s_{i-1},
    d_{k}, s_{i+1}, \cdots, s_n,$\
$v_{t}\}$ by inserting $d_{k}$ between $s_{i}$ and $s_{i+1}$ ($\forall s_i\in\{\mathcal{S}_\text{current}/(v_s, s_1)\}$), and then swapping $s_{i}$ and $s_{i-1}$. The insertion distance of swapping left is $$\begin{equation}
        \begin{aligned}
            \lambda_\text{swapping (left)}(s_i,d_k) &= \theta(d_k, s_{i+1}) - \theta(s_i,s_{i+1}) \\ 
                                                    &+ \theta(s_{i-1}, d_k) + \theta(s_{i-2}, s_i) \\
                                                    &- \theta(s_{i-2}, s_{i-1}).
        \end{aligned}
\end{equation}$$

The right swap is a similar operation except that it swaps $s_{i+1}$ and $s_{i+2}$ instead. Lastly, the case of swapping both does a left swap ($s_{i}$ and $s_{i+1}$) and then a right swap ($s_{i+1}$ and $s_{i+2}$).

### Sequence Refinement

In-place insertion occurs when the graph is not cyclic or the triangular inequality does not hold on the graph. The in-place insertion could generate redundant revisited nodes in the final result and lead to a longer sequence. We further refine the sequence by skipping revisited destination when the previous destination and the next destination are connected. The refined sequence of destinations, $\mathcal{S}_\text{ECI}$, with cardinality $r\leq n$ is the input to the genetic algorithm.

## Genetic Algorithm

We further leverage a genetic algorithm [@potvin1996genetic; @moon2002efficient; @braun1990solving] to refine the sequence from the enhanced cheapest insertion algorithm. The genetic algorithm selects a parent[^2] sequence and then generates a new offspring sequence from it by either a mutation or crossover process.

In brief, we first take the ordered sequence $\mathcal{S}_\text{ECI}$ from the enhanced cheapest insertion as our first and only parent for the mutation process, which produces multiple offspring. Only the offspring with a lower cost than the parent are considered the parents for the crossover process.

*1) Mutation:* There are three steps for each mutation process, as described in Fig. [\[fig:Mutation\]](#fig:Mutation){reference-type="ref" reference="fig:Mutation"}. First, the ordered sequence $\mathcal{S}_\text{ECI}$ from the enhanced cheapest insertion is randomly divided into $k$ segments. Second, random inversion[^3] is executed for each segment except the first and last segments, which contain the source and the target. Lastly, the segments in the middle are randomly reordered and spliced together. Let the resulting offspring sequence be $\psi = \{v_s, p_1,
p_2,\cdots, p_r, v_t\}$, where $v_s$ is the source node, $v_t$ is the target node, $(r+2)$ is the number of destinations in the sequence (the same cardinality of $S_\text{ECI}$), and $\{p_i\}_{i=1}^r$ is the re-ordered destinations, which could possibly contain the start and end. The cost $\Theta$ of the offspring is computed as $$\begin{equation}
\label{eq:MulationCost}
    \Theta = \theta(v_s, p_1) + \sum_{i=1}^r \theta(p_i, p_{i+1}) + \theta(p_n, v_t),
\end{equation}$$ where $\theta(\cdot, \cdot)$ is the path distance between two destinations provided by the $\text{IMOMD-RRT}^*$.

We perform the mutation process thousands of times, resulting in thousands of offspring. Note that only the offspring with a lower cost than the cost of the parent are kept for the crossover process.

:::: {.figure latex-placement="t"}
  

::: {.caption short-caption=""}
Illustration of the mutation and crossover in the Genetic Algorithm. In mutation, the sequence is randomly cut into five segments and each segment is randomly reversed except Segment A and Segment E. In this case, Segment B and C are reversed and D does not. Finally, the modified segments are spliced in random order and resulting an offspring ACDBE. In crossover, two sequences (Parent A and Parent B) are picked from the offspring from the mutation process. A sub-sequence of one of the two sequences is randomly selected (Sub-sequence A in this case). Next, random inversion is performed on Sub-sequence A and the resulting segment is randomly placed inside an empty sequence of the offspring. Lastly, the remaining elements of the offspring are filled by the order of the other sequence (Parent B) except the elements that are already in the offspring sequence.
:::
::::

*2) Crossover:* Let the set of mutated sequences from the mutation process be $\Psi=\{\psi_i\}_{i=1}^{h}$, where $h$ is the number of offspring kept after the mutation process. For each generation, the crossover process is performed thousands of times and only the offspring with a lower cost than the previous generation are kept. Each crossover process combines sub-sequences of any two sequences ($\psi_i,
\psi_j\in\Psi$) to generate a new offspring, as described in Fig.[\[fig:Crossover\]](#fig:Crossover){reference-type="ref" reference="fig:Crossover"}. The probability of a sequence $\psi_i$ being picked is defined as: $$\begin{equation}
    P_{\psi}(\psi = \psi_i) = \frac{\rho_i}{\sum_{i=1}^{w}\rho_i}, ~~ \rho_i = \frac{1}{\Theta_i},
\end{equation}$$ where $w$ is the number of the remaining offspring from each generation after the $(i-1)^{\text{th}}$ generation and $\rho_i$ is the fitness of the sequence $\psi_i$.

Given the two selected sequences and an empty to-be-filled offspring, a segment of one of the two sequences is randomly selected, and random inversion is performed on the segment. The resulting segment is randomly placed inside the empty sequence of the offspring. Lastly, the remaining elements of the offspring are filled by the order of the other sequence except the elements that are already in the offspring sequence. After a few generations, the offspring with the lowest cost, $\psi^*$, is the final sequence $\mathcal{S}_\text{ECI-Gen}$ of the destinations.

::: remark
Whenever the IMOMD-RRT$^\ast$ provides a better path (due to its asymptotic optimality), the ECI-Gen solver will be executed to solve for a better visiting order of the destinations. Therefore, the full system provides paths with monotonically improving path cost in an anytime fashion.
:::

## Discussion of time complexity

As mentioned in Sec. [4.3](#sec:WIBFS){reference-type="ref" reference="sec:WIBFS"}, the first sequence $\mathcal{S}_{\text{current}}$ is constructed by Dijkstra's algorithm, which is an $O(N^2)$ process, where $N$ is the cardinality of the destination set $\mathcal{D}$. We then pass the sequence to the enhanced cheapest insertion algorithm, whose time complexity is $O(N^3)$, to generate a set of parents for the genetic algorithm, which is also an $O(N^3)$ process. Therefore, the overall time complexity of the proposed ECI-Gen solver is $O(N^3)$, and indeed a polynomial solver.

# Experimental Results {#sec:Experiments}

This section presents extensive evaluations of the $\text{IMOMD-RRT}^*$ system applied to two complex vehicle routing scenarios. The robot state $\zeta$ is defined as latitude and longitude. The distance between robot states $\mathtt{Dist}(\cdot, \cdot)$ in [\[eq:NearestNode\]](#eq:NearestNode){reference-type="eqref" reference="eq:NearestNode"} is defined as the haversine distance[@van2012heavenly]. We implemented the bi-directional A$^*$ [@BiAstar] and ANA$^*$ [@ANAstar] as our baselines to compare the speed and memory usage (the number of explored nodes). We evaluate the IMOMD-RRT$^\ast$ system (IMOMD-RRT$^\ast$ and the ECI-Gen solver) on a large and complex map of Seattle, USA. The map contains $1,054,372$ nodes and $1,173,514$ edges, and is downloaded from OpenStreetMap (OSM), which is a public map service built for real applications[^4]. We then place $25$ destinations in the map. We demonstrate that the $\text{IMOMD-RRT}^*$ system is able to concurrently find paths connecting destinations and determine the order of destinations. We also show that the system escapes from a bug trap by inherently receiving prior knowledge. The algorithm runs on a laptop equipped with Intel$^\text{\textregistered}$ Core$^{\text{TM}}$ i7-1185G7 CPU @ 3.00 GHz.

To show the performance and ability of multi-objective and determining the visiting order, we randomly set $25$ destinations in the Seattle map. There are 25! possible combinations of visiting orders and therefore it is intractable to solve the visiting order by brute force. The results are shown in Fig. [8](#fig:OSMSeattle){reference-type="ref" reference="fig:OSMSeattle"}, where $\text{IMOMD-RRT}^*$ finds the first path faster than both Bi-A$^\ast$ and ANA$^\ast$ with a lower cost and then also spends less time between solution improvements. Additionally, the memory usage of $\text{IMOMD-RRT}^*$ is less than ANA\* and much less than bi-A$^\ast$. As shown in Table [4](#tab:ExpResults){reference-type="ref" reference="tab:ExpResults"}, the proposed system provides the first solution 10 times faster than bi-A$^\ast$ and four time faster than ANA$^\ast$. In addition, the proposed system also consumes 65 times less memory than bi-A$^\ast$ and 4.7 times less memory usage than ANA$^\ast$.

::: {#tab:ExpResults}
+---------------+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|               |                  | ::: {#tab:ExpResults}                                                                                                                                                                                                                                            | ::: {#tab:ExpResults}                                                                                                                                                                                                                                            | ::: {#tab:ExpResults}                                                                                                                                                                                                                                            |
|               |                  |   -----------------------                                                                                                                                                                                                                                        |   -------------------                                                                                                                                                                                                                                            |   -----------------------                                                                                                                                                                                                                                        |
|               |                  |    Initial Solution Time                                                                                                                                                                                                                                         |    Initial Path Cost                                                                                                                                                                                                                                             |     Final Memory Usage                                                                                                                                                                                                                                           |
|               |                  |         \[seconds\]                                                                                                                                                                                                                                              |     \[kilometers\]                                                                                                                                                                                                                                               |    \[\# explored nodes\]                                                                                                                                                                                                                                         |
|               |                  |   -----------------------                                                                                                                                                                                                                                        |   -------------------                                                                                                                                                                                                                                            |   -----------------------                                                                                                                                                                                                                                        |
|               |                  |                                                                                                                                                                                                                                                                  |                                                                                                                                                                                                                                                                  |                                                                                                                                                                                                                                                                  |
|               |                  |   : Quantitative results of the proposed $\text{IMOMD-RRT}^*$ system on two large maps (both graphs contain more than one million nodes and edges) built for real robotics and vehicle applications. The proposed system outperforms bi-A$^\ast$ and ANA$^\ast$. |   : Quantitative results of the proposed $\text{IMOMD-RRT}^*$ system on two large maps (both graphs contain more than one million nodes and edges) built for real robotics and vehicle applications. The proposed system outperforms bi-A$^\ast$ and ANA$^\ast$. |   : Quantitative results of the proposed $\text{IMOMD-RRT}^*$ system on two large maps (both graphs contain more than one million nodes and edges) built for real robotics and vehicle applications. The proposed system outperforms bi-A$^\ast$ and ANA$^\ast$. |
|               |                  | :::                                                                                                                                                                                                                                                              | :::                                                                                                                                                                                                                                                              | :::                                                                                                                                                                                                                                                              |
+:=============:+:================:+=================================================================================================================================================================================================================================================================:+=================================================================================================================================================================================================================================================================:+=================================================================================================================================================================================================================================================================:+
| Seattle       | IMOMD-RRT$^\ast$ | **0.44**                                                                                                                                                                                                                                                         | **501,342**                                                                                                                                                                                                                                                      | **49,768**                                                                                                                                                                                                                                                       |
|               +------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|               | Bi-A$^\ast$      | 4.40                                                                                                                                                                                                                                                             | 808,416                                                                                                                                                                                                                                                          | 3,240,515                                                                                                                                                                                                                                                        |
|               +------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|               | ANA$^\ast$       | 1.70                                                                                                                                                                                                                                                             | 1,089,873                                                                                                                                                                                                                                                        | 234,457                                                                                                                                                                                                                                                          |
+---------------+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| San Francisco | IMOMD-RRT$^\ast$ | **1.10**                                                                                                                                                                                                                                                         | **156,807**                                                                                                                                                                                                                                                      | **61,785**                                                                                                                                                                                                                                                       |
|               +------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|               | Bi-A$^\ast$      | 9.93                                                                                                                                                                                                                                                             | 315,061                                                                                                                                                                                                                                                          | 3,640,863                                                                                                                                                                                                                                                        |
|               +------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|               | ANA$^\ast$       | Failed                                                                                                                                                                                                                                                           | Failed                                                                                                                                                                                                                                                           | Failed                                                                                                                                                                                                                                                           |
+---------------+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

: Quantitative results of the proposed $\text{IMOMD-RRT}^*$ system on two large maps (both graphs contain more than one million nodes and edges) built for real robotics and vehicle applications. The proposed system outperforms bi-A$^\ast$ and ANA$^\ast$.
:::

Prior knowledge through pseudo destinations can also be leveraged to traverse challenging topology, such as bug-traps[@Lav06]. This problem is commonly seen in man-made environments such as a neighborhood with a single entry or cities separated by a body of water, as in Fig. [9](#fig:InformBugTrapOSM){reference-type="ref" reference="fig:InformBugTrapOSM"}. As mentioned in Remark [3.3](#sec:Informable){reference-type="ref" reference="sec:Informable"}, prior knowledge is provided as a number of pseudo destinations in the $\text{IMOMD-RRT}^*$ as a prior collision-free path in the graph for robotics inspection or vehicle routing. Next, the prior path is then being rewired by the $\text{IMOMD-RRT}^*$ to improve the path. We demonstrate this feature by providing the prior knowledge to escape the bug trap in San Francisco, as shown in Fig. [9](#fig:InformBugTrapOSM){reference-type="ref" reference="fig:InformBugTrapOSM"}. The map contains $1,277,702$ nodes and $1,437,713$ edges. As shown in Table [4](#tab:ExpResults){reference-type="ref" reference="tab:ExpResults"}, the proposed system escapes from the trap nine times faster than bi-A$^\ast$, whereas ANA$^\ast$ failed to provide a path within the given time frame. The proposed system also consumes 58.9 times less memory than bi-A$^\ast$.

In summary, we developed an anytime iterative system to provide paths between multiple objectives by the $\text{IMOMD-RRT}^*$ and to determine the visiting order of the objectives by the ECI-Gen solver solver in polynomial time. We also demonstrate that the proposed system is able to inherently accommodate prior information to escape from challenging topology.

:::: {#fig:OSMSeattle .figure latex-placement="t"}
  

::: {.caption short-caption=""}
Quantitative and qualitative results for an OSM of Seattle, where we have 25 destinations to be visited. The proposed $\text{IMOMD-RRT}^*$ outperforms Bi-A$^\ast$ and ANA$^\ast$ in term of speed and memory usage (the number of explored nodes).
:::
::::

:::: {#fig:InformBugTrapOSM .figure latex-placement="t"}
 

::: {.caption short-caption=""}
Providing prior knowledge to the proposed $\text{IMOMD-RRT}^*$ system to avoid bug traps. The left and the right are the qualitative and quantitative results for a bug trap in San Francisco, respectively. We have eight pseudo destinations to help escape the challenging topology, where the source and target are separated by a body of water. Note that ANA$^\ast$ failed to provide a solution in the given time.
:::
::::

# Conclusion and Future Work {#sec:Conclusion}

We presented an anytime iterative system on large-complex graphs to solve the multi-objective path planning problem, to decide the visiting order of the objectives, and to incorporate prior knowledge of the potential trajectory. The system is comprised of an anytime informable multi-objective and multi-directional RRT$^*$ to connect the destinations to form a connected graph and the ECI-Gen solver to determine the visiting order (via a relaxed Traveling Salesman Problem) in polynomial time.

The system was extensively evaluated on OpenStreetMap (OSM), built for autonomous vehicles and robots in practice. In particular, the system solved a path planning problem and the visiting order with $25$ destinations ($25!$ possible combinations of visiting orders) on an OSM of Seattle, containing more than a million nodes and edges, in 0.44 seconds. In addition, we demonstrated the system is able to leverage a reference path (prior knowledge) to navigate challenging topology for robotics inspection or vehicle routing applications. All the evaluations show that our proposed method outperforms the Bi-A$^\ast$ and ANA$^\ast$ algorithm in terms of speed and memory usage.

In the future, we shall use the developed system within autonomy systems[@rehder2016extending; @furgale2013unified; @oth2013rolling; @huang2020improvements; @huang2021lidartag; @huang2021optimal; @huang2020intinsic; @Hartley-RSS-18; @hartley2019contact; @huang2021efficient; @gong2021zero; @gong2020angular; @gong2019feedback] on a robot to perform point-to-point tomometric navigation in graph-based maps while locally avoiding obstacles and uneven terrain. It would also be interesting to deploy the system with multi-layered graphs and maps [@Fankhauser2018ProbabilisticTerrainMapping; @Fankhauser2014RobotCentricElevationMapping; @Lu2020BKI] to incorporate different types of information.

# Acknowledgment {#acknowledgment .unnumbered}

The first author conceptualized and initiated the research problem, designed the components of the system, determined the evaluation metrics, interpreted the results, and led the project. The first, third, fourth, and last author wrote this manuscript. The second author consolidated the initial version of the enhanced cheapest insertion algorithm, and implemented the initial version of the system. The third author helped conceptualize the entire current $\text{IMOMD-RRT}^*$ system including the $\text{IMOMD-RRT}^*$ and the ECI-Gen solver, provided perceptive literature review, implemented the components of the system and all the baselines, and ran the system on various of maps. The fourth and the last author provided insightful knowledge to the full system, suggested practical improvement to the system, and guided the direction of the project as well as supported the work. The first author would like to thank all the authors for assisting the research and for all of the conversations. Toyota Research Institute provided funds to support this work. Funding for J. Grizzle was in part provided by NSF Award No. 2118818. This article solely reflects the opinions and conclusions of its authors and not the funding entities.The first author thanks Wonhui Kim for useful conversations.

[^1]: A simple graph, also called a strict graph, is an unweighted and undirected graph that contains no graph loops or multiple edges between two nodes[@bondy1976graph].

[^2]: Note that the parent in the genetic algorithm is a different concept from the parent node in the $\text{RRT}^*$ tree, mentioned in Sec. [3.2](#sec:RRTOnGraphs){reference-type="ref" reference="sec:RRTOnGraphs"}. The terminology is kept so that it follows the literature consistently.

[^3]: A random inversion of a segment is reversing the order of destinations in the segment.

[^4]: Apple Map$^\text{\textregistered}$ actually uses OpenStreetMap as their foundation.
