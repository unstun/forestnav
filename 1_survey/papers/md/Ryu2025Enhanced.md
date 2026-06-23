---
citation_key: Ryu2025Enhanced
arxiv_id: 2505.21968
arxiv_url: https://arxiv.org/abs/2505.21968
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:18:12Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

Global path planning is fundamental for autonomous mobile robot navigation, enabling robots to find collision-free paths from a start to a goal location within known environments. Among various approaches, sampling-based planners, particularly Rapidly-exploring Random Trees (RRT) and its optimal variant RRT\*, have been widely adopted due to their effectiveness in handling complex obstacles and kinematic constraints.

RRT rapidly constructs a feasible path by incrementally expanding a tree from the start state toward randomly sampled states [@karaman2011anytime; @kuffner2000rrt]. However, a major limitation of RRT is its lack of optimality guarantees. To address this, RRT\* [@karaman2011sampling] connects newly sampled states to multiple neighboring nodes and performs path rewiring to minimize path cost.

Despite theoretical asymptotic optimality, RRT\* often suffers from slow convergence, especially in environments containing narrow passages or large open spaces. To mitigate this, informed sampling methods have been proposed, restricting sample generation to promising regions once an initial feasible solution is found [@gammell2021asymptotically]. However, these methods still depend heavily on random sampling, thus failing to fully exploit structural information inherent in the environment. Consequently, delayed initial solutions frequently lead to slower overall optimization.

Skeletonization-Informed RRT\* (SIRRT\*) [@ryu2019improved] addresses this issue by leveraging the deterministic structure of the medial axis (skeleton) extracted from a 2D grid map. SIRRT\* constructs an initial tree and path via a minimum spanning tree (MST) built upon the skeleton. This deterministic approach quickly generates reliable initial solutions with significantly reduced variance compared to random-sampling-based methods such as Informed-RRT\* (IRRT\*) [@gammell2014informed]. Nonetheless, the initial MST-derived solutions may deviate from optimal trajectories, indicating potential for further improvement.

To overcome these limitations, we propose Enhanced SIRRT\* (E-SIRRT\*), which improves both initial solution quality and tree connectivity prior to informed optimization. Specifically, we introduce: (i) a hybrid path smoothing method that first generates a splined initial path via cubic interpolation and then applies collision-aware correction to produce a collision-free smoothed initial path, and (ii) a bidirectional rewiring mechanism that further improves the tree structure around this path to yield a refined initial path. These enhancements support more effective informed sampling and promote faster, more stable convergence toward high-quality solutions.

The remainder of this paper is organized as follows. Section [2](#related_works){reference-type="ref" reference="related_works"} reviews informed sampling-based RRT planners. Section [3](#preliminaries){reference-type="ref" reference="preliminaries"} briefly explains the original SIRRT\* algorithm. Section [4](#esirrt){reference-type="ref" reference="esirrt"} presents the proposed E-SIRRT\*, detailing the hybrid path smoothing and bidirectional rewiring procedures. Section [5](#exp_result){reference-type="ref" reference="exp_result"} provides experimental results and comparative analyses. Finally, Section [6](#conclusion){reference-type="ref" reference="conclusion"} concludes the paper and suggests directions for future research.

# Related Works {#related_works}

IRRT\* enhances the convergence of RRT by sampling within an ellipsoidal informed set, defined using the current best solution cost and heuristic bounds. However, informed sampling in IRRT\* commences only after an initial feasible solution is acquired, typically via uniform random sampling. This dependency can significantly delay convergence, particularly in complex environments with narrow passages.

To mitigate this limitation, IRRT\*-Connect [@mashayekhi2020informed] integrates informed sampling into the bidirectional RRT\*-Connect framework [@klemm2015rrt]. It simultaneously grows trees from the start and goal states, restricting sampling to the informed region after an initial connection is established. Subsequent improvements, including bias extension and node pruning [@wang2024improved], have further accelerated convergence and improved reliability in cluttered environments.

Recent approaches have also incorporated task-specific knowledge or learned representations into informed sampling strategies. Neural-Informed RRT [@huang2024neural] leverages deep neural networks to derive informative sampling distributions from environmental point clouds. Risk-Informed RRT [@chi2018risk] integrates human-centric risk metrics to promote safer navigation in human-shared environments. RBI-RRT [@chen2024rbi] explicitly reconstructs and reuses previously explored tree structures to guide future expansion. AM-RRT [@armstrong2021rrt] improves robustness under uncertainty by augmenting heuristic guidance with metrics such as diffusion distance.

Batch Informed Trees (BIT\*) [@gammell2020batch] reformulate sampling-based planning as incremental graph search over batch-sampled random geometric graphs. BIT\* prioritizes edge evaluations based on estimated path costs and reuses search effort across batches. Advanced BIT\* (ABIT\*) [@strub2020advanced] further enhances BIT\* with graph-search techniques such as heuristic inflation and search truncation, accelerating initial solution discovery while preserving asymptotic optimality even in high-dimensional spaces.

SIRRT\* [@ryu2019improved] introduces a structure-aware variant of IRRT\* that leverages environmental skeletonization to deterministically generate an initial path via an MST. This approach reduces variance in initialization and accelerates convergence compared to sampling-based methods. However, the MST-derived path is not geometrically refined, and the resulting tree structure does not support cost-efficient propagation, motivating the enhancements proposed in this paper.

To address these limitations, we propose E-SIRRT\*, extending the SIRRT\* framework with key improvements. Unlike the original SIRRT\*, which produces suboptimal initial paths and tree connectivity, our enhanced version significantly improves initial path quality through hybrid path smoothing and refines tree connectivity using bidirectional rewiring.

# Overview of SIRRT\* {#preliminaries}

The SIRRT\* algorithm [@ryu2019improved] leverages deterministic structural information extracted from a 2D grid map to efficiently generate initial solutions, addressing the limitations of purely random sampling methods. It begins by computing the medial axis (skeleton) of the free space using morphological thinning, which effectively captures the topological structure of the environment. Harris corner detection is then applied to the skeleton to identify salient points that represent meaningful structural features (Fig. [\[fig:ske_sirrt\]](#fig:ske_sirrt){reference-type="ref" reference="fig:ske_sirrt"}).

Using these skeleton-derived nodes, along with the start and goal positions, an MST is constructed via Prim's algorithm [@cormen2009introduction]. This tree captures the connectivity of the environment, and an initial path is extracted by tracing the MST from the goal node back to the start node (Fig. [\[fig:initial_sirrt\]](#fig:initial_sirrt){reference-type="ref" reference="fig:initial_sirrt"}). This deterministic initialization significantly reduces computation time and solution variance compared to stochastic methods such as IRRT\* [@gammell2014informed]. Furthermore, the initial solution defines a focused ellipsoidal sampling region for subsequent informed optimization (Fig. [\[fig:final_sirrt\]](#fig:final_sirrt){reference-type="ref" reference="fig:final_sirrt"}).

However, the MST-derived path often contains unnatural turns and geometric irregularities, which may hinder efficient cost propagation during the optimization phase. These limitations motivate the enhancements proposed in the next section.

:::: {#fig:sirrt .figure latex-placement="t"}
::: caption
Overview of the SIRRT\* algorithm: (a) Skeletonization of the binary occupancy grid map via morphological thinning; Harris corner nodes are marked in yellow. (b) Initial tree (blue nodes and lines) and initial path (cyan line) constructed using an MST over the extracted corner nodes, start (yellow dot), and goal (red dot) positions. (c) Optimization phase via informed sampling within an ellipsoidal region (green ellipse); the final optimized path is shown in red.
:::
::::

# Proposed Method: Enhanced SIRRT\* {#esirrt}

E-SIRRT\* introduces two improvements to the original SIRRT\* algorithm: hybrid path smoothing and bidirectional rewiring. These improvements are applied prior to informed optimization and support more accurate cost propagation and faster, more stable convergence.

## Initial Path Enhancement by Hybrid Path Smoothing {#hybrid_path_smoothing}

Although the MST-derived path connects the start and goal nodes deterministically and efficiently, it often lacks geometric smoothness due to the sparse and piecewise nature of the skeleton and the greedy structure of MST construction. Such irregularities can reduce the path?s suitability for real-world execution, where curvature continuity is often required, and impede optimization convergence.

To address this, we apply a hybrid path smoothing procedure to refine the MST-derived path. This process consists of two stages: (i) spline fitting to generate a splined initial path with improved geometric continuity, and (ii) collision-aware correction to ensure feasibility, yielding a smoothed initial path. The full procedure is summarized in Algorithm [\[alg:hybrid_path_smoothing\]](#alg:hybrid_path_smoothing){reference-type="ref" reference="alg:hybrid_path_smoothing"}.

### Hybrid Path Smoothing

In the first stage, the initial MST path $\mathcal{P}_{\text{init}}$ is sparsely subsampled using a fixed interval $d$ to eliminate unnecessary waypoints (line 2). The resulting control point sequence is denoted by $\mathcal{P}_{\text{sub}} = \{\mathbf{p}_i\}_{i=0}^{m}$, where each point $\mathbf{p}_i = [x_i, y_i]^T$, and the normalized parameter values are given by $u_i = i/m$, with $m = |\mathcal{P}_{\text{sub}}| - 1$ denoting the number of intervals between subsampled points.

Next, we fit two independent cubic spline functions to the $x$ and $y$ coordinate sequences over the domain $[0, 1]$ using the subroutine [CubicSplineFit]{.smallcaps} (lines 4--5; see Algorithm [\[alg:cubic_spline_fit\]](#alg:cubic_spline_fit){reference-type="ref" reference="alg:cubic_spline_fit"}). This routine computes the spline coefficients $a_i$, $b_i$, $c_i$, and $d_i$ for each segment over $[u_i, u_{i+1}]$, such that $$\begin{equation}
\label{eq_spline}
    s_i(u) = a_i + b_i(u - u_i) + c_i(u - u_i)^2 + d_i(u - u_i)^3,
\end{equation}$$ for $i = 0, \dots, m-1$.

Once the spline coefficients are obtained, the path is evaluated at $N + 1$ uniformly spaced parameter values $u_k = \frac{k}{N}$, for $k = 0, \dots, N$ (lines 6--13). Each $u_k$ is used to compute interpolated coordinates $[x(u_k), y(u_k)]$ within the corresponding segment. This yields a densely sampled splined initial path $\mathcal{P}_{\text{spline}}$ that smoothly interpolates the original control points.

In the second stage (line 14), the spline-fitted path is validated for collision. Although geometrically smooth, it may contain segments that are infeasible due to obstacles. To ensure feasibility, we apply the subroutine [CollisionAwareCorrection]{.smallcaps} (Algorithm [\[alg:collision_correction\]](#alg:collision_correction){reference-type="ref" reference="alg:collision_correction"}), which replaces invalid segments with safe alternatives drawn from the original MST-derived path. The result is a collision-free smoothed initial path $\mathcal{P}_{\text{smooth}}$, which is used to update the initial tree structure in the next phase.

::: algorithm
:::

::: algorithm
:::

### Cubic Spline Fit

The subroutine [CubicSplineFit]{.smallcaps} (Algorithm [\[alg:cubic_spline_fit\]](#alg:cubic_spline_fit){reference-type="ref" reference="alg:cubic_spline_fit"}) computes the coefficients of a natural cubic spline that interpolates a sequence of scalar values $\{z_0, z_1, \dots, z_m\}$ over a uniformly spaced parameter domain $\{u_0, u_1, \dots, u_m\}$. The objective is to compute segment-wise spline coefficients, as defined in ([\[eq_spline\]](#eq_spline){reference-type="ref" reference="eq_spline"}), to ensure smooth interpolation across all subintervals $[u_i, u_{i+1}]$.

Assuming uniform spacing $h = u_{i+1} - u_i$ (line 2), the method constructs a tridiagonal linear system $A \mathbf{M} = \mathbf{b}$ to solve for the second derivatives $\mathbf{M} = [M_0, \dots, M_m]^T$ at the knots (lines 3--4). Natural boundary conditions are imposed by setting $M_0 = M_m = 0$, enforcing zero curvature at the endpoints.

The matrix $A$ is symmetric and tridiagonal, with size $(m{-}1) \times (m{-}1)$, derived from continuity constraints on the second derivatives of adjacent spline segments. Under uniform spacing, its structure is given by $$\begin{equation}
    A = \frac{1}{h}
    \begin{bmatrix}
        4 & 1 & 0 & \cdots & 0 \\
        1 & 4 & 1 & \cdots & 0 \\
        0 & 1 & 4 & \ddots & \vdots \\
        \vdots & \ddots & \ddots & \ddots & 1 \\
        0 & \cdots & 0 & 1 & 4
    \end{bmatrix},
\end{equation}$$ where each row enforces a second-derivative continuity constraint at an interior knot. The first and last rows are excluded due to the imposed boundary conditions. This system can be efficiently solved using the Thomas algorithm [@quarteroni2007scientific].

Once the second derivatives are obtained, the spline coefficients $\{a_i, b_i, c_i, d_i\}_{i=0}^{m-1}$ for each segment are computed analytically (lines 7--11). These coefficients ensure $\mathcal{C}^2$ continuity across the domain and define a smooth, twice-differentiable interpolant over $[0, 1]$.

::: algorithm
:::

### Collision-Aware Correction

The subroutine [CollisionAwareCorrection]{.smallcaps} (Algorithm [\[alg:collision_correction\]](#alg:collision_correction){reference-type="ref" reference="alg:collision_correction"}) refines the splined initial path to ensure that all segments are collision-free. While spline interpolation improves geometric continuity, it does not account for obstacles and may generate infeasible segments. This subroutine performs segment-wise validation and applies fallback corrections using points from the original MST-derived path $\mathcal{P}_{\text{init}}$.

The corrected path $\mathcal{P}_{\text{smooth}}$ is initialized with the first point of $\mathcal{P}_{\text{spline}}$ (lines 2--3). The algorithm then iterates over the remaining spline points (lines 4--9), checking whether the segment from the last valid point to the current point is obstacle-free. If the segment is valid, the current point is appended to $\mathcal{P}_{\text{smooth}}$ (line 7); otherwise, a fallback procedure is triggered (lines 10--17).

During fallback, the algorithm searches for the nearest point $f \in \mathcal{P}_{\text{init}}$ that forms a collision-free segment with the last valid point. Among all feasible candidates, the one with the smallest Euclidean distance to the current spline point is selected and appended (lines 13--16), provided it differs from the previous point (line 17). Finally, the function returns the collision-free smoothed initial path $\mathcal{P}_{\text{smooth}}$ (line 18), which preserves the geometry of the spline wherever feasible and applies minimal corrections only when necessary.

::: algorithm
:::

## Initial Tree Refinement by Bidirectional Rewiring {#sec:bidirectional_rewiring}

Although the smoothed initial path $\mathcal{P}_{\text{smooth}}$ improves geometric quality by eliminating jagged turns, the initial tree $\mathcal{T}$ constructed from the MST does not reflect this improvement in either connectivity or cost structure. As a result, the tree may be misaligned with the smoothed path and may not support effective cost propagation. To resolve this, we refine the tree around $\mathcal{P}_{\text{smooth}}$ using a bidirectional rewiring strategy, which updates parent-child relationships and path costs based on proximity and feasibility. The full procedure is summarized in Algorithm [\[alg:bidirectional_rewiring\]](#alg:bidirectional_rewiring){reference-type="ref" reference="alg:bidirectional_rewiring"}.

The algorithm iterates over each point $p \in \mathcal{P}_{\text{smooth}}$ (line 2), and identifies nearby nodes $\mathcal{N}_{\text{near}}$ using a radius-based neighbor search (line 3). For each such node, rewiring is applied in two directions: *forward rewiring* and *reverse rewiring*. These procedures are illustrated in Fig. [2](#fig:rewiring){reference-type="ref" reference="fig:rewiring"}.

:::: {#fig:rewiring .figure latex-placement="t"}
::: caption
Illustration of bidirectional rewiring around a smoothed path node $p$. (a) In forward rewiring, the parent of a neighbor $q$ is updated to $p$ if it yields a lower cost and the edge is collision-free. (b) In reverse rewiring, $p$ adopts $q$ as its new parent under similar conditions. Solid arrows indicate parent-to-child direction, red arrows show newly rewired edges, and dashed circles represent the rewiring radius.
:::
::::

In the *forward rewiring* phase (lines 4--7), the algorithm checks whether $p$ can provide a lower-cost path to any neighbor $q \in \mathcal{N}_{\text{near}}$. If the cost-to-come to $p$ plus the edge cost $\text{Cost}(p, q)$ is less than the current cost-to-come to $q$, and the edge $(p, q)$ is obstacle-free (line 5), then $p$ becomes the new parent of $q$, and cost values are updated for $q$ and its descendants (lines 6--7).

In the *reverse rewiring* phase (lines 8--11), the algorithm evaluates whether any neighbor $q$ offers a better connection to $p$. If connecting $p$ through $q$ lowers its cost-to-come and the segment $(q, p)$ is collision-free (line 9), then $q$ becomes the new parent of $p$, and cost updates propagate through the affected subtree (lines 10--11). This step allows not only downstream nodes but also those on the smoothed path itself to benefit from improved connections.

By applying both rewiring directions at each point along $\mathcal{P}_{\text{smooth}}$, the algorithm aligns the tree with the geometry of the smoothed path and improves cost consistency. The resulting structure supports more efficient informed optimization in the subsequent phase.

::: algorithm
$I_{\text{skel}} \leftarrow \textsc{Skeletonization}(I_{\text{grid}})$ $P_{\text{corner}} \leftarrow \textsc{HarrisCornerDetection}(I_{\text{skel}})$ $\mathcal{T} \leftarrow \textsc{GenerateInitialTree}(P_{\text{corner}}, p_{\text{start}}, p_{\text{goal}})$ $\mathcal{P}_{\text{init}} \leftarrow \textsc{ExtractPath}(\mathcal{T}, p_{\text{start}}, p_{\text{goal}})$ [$\mathcal{P}_{\text{smooth}} \leftarrow \textsc{HybridPathSmoothing}(\mathcal{P}_{\text{init}})$]{style="color: blue"} [$\mathcal{T} \leftarrow \textsc{InsertSmoothedPath}(\mathcal{T}, \mathcal{P}_{\text{smooth}})$]{style="color: blue"} [$\mathcal{T} \leftarrow \textsc{BidirectionalRewiring}(\mathcal{T}, \mathcal{P}_{\text{smooth}})$]{style="color: blue"} $p_{\text{rand}} \leftarrow \textsc{InformedSample}(i, \mathcal{T})$ $p_{\text{near}} \leftarrow \textsc{Nearest}(\mathcal{T}, p_{\text{rand}})$ $p_{\text{new}} \leftarrow \textsc{Steer}(p_{\text{near}}, p_{\text{rand}})$
:::

## Enhanced SIRRT\* Using Hybrid Path Smoothing and Bidirectional Rewiring {#sec:enhanced_sirrt}

Algorithm [\[alg:enhanced_sirrt\]](#alg:enhanced_sirrt){reference-type="ref" reference="alg:enhanced_sirrt"} summarizes the complete pipeline of the proposed Enhanced SIRRT\* planner. The algorithm consists of two main phases: initial path generation based on grid map skeletonization (lines 2--8), followed by informed optimization using sampling-based RRT\* (lines 9--17).

A skeleton of the input grid map $I_{\text{grid}}$ is computed using morphological thinning (line 2), followed by Harris corner detection to extract salient structural features (line 3). These points, along with the start and goal locations, are used to construct an MST $\mathcal{T}$ via Prim's algorithm (line 4). An initial path $\mathcal{P}_{\text{init}}$ is then extracted from the MST by tracing from the goal node back to the start node (line 5).

Next, the initial path and tree are refined by the proposed enhancements (lines 6--8). To improve geometric quality, the path is updated using the [HybridPathSmoothing]{.smallcaps} procedure (Algorithm [\[alg:hybrid_path_smoothing\]](#alg:hybrid_path_smoothing){reference-type="ref" reference="alg:hybrid_path_smoothing"}, line 6), which performs cubic spline fitting to generate a splined initial path, followed by collision-aware correction to yield a smoothed initial path. This smoothed path $\mathcal{P}_{\text{smooth}}$ is then merged into the initial tree (line 7) by sequentially inserting its nodes while preserving continuity and parent-child relationships.

The tree is subsequently refined using the [BidirectionalRewiring]{.smallcaps} procedure (Algorithm [\[alg:bidirectional_rewiring\]](#alg:bidirectional_rewiring){reference-type="ref" reference="alg:bidirectional_rewiring"}, line 8), which rewires connections between the smoothed path and nearby nodes in both directions. This improves cost propagation and results in a refined initial path embedded in an updated tree structure.

Following tree refinement, the algorithm proceeds with informed sampling-based optimization (lines 9--17). At each iteration, a sample is drawn from the informed ellipsoidal region (line 10), extended toward its nearest neighbor (line 11), and added to the tree if valid (lines 12--17). Parent selection and local rewiring follow the standard RRT\* framework, allowing the solution to incrementally improve while preserving asymptotic optimality.

:::: {#fig:esirrt .figure}
::: caption
Initial tree refinement and optimization result in E-SIRRT\*. (a) Initial tree (blue nodes and edges) constructed via grid map skeletonization, with the smoothed initial path (cyan) merged into the tree. The magenta line shows the splined initial path before collision-aware correction, and corrected segments are highlighted with grey dotted rectangles. (b) Tree after forward rewiring around the smoothed path; rewired regions are highlighted with grey dotted rectangles. (c) Tree after bidirectional rewiring, further enhancing local connectivity. (d) Refined initial tree and path (green). (e) Final optimized path (red) obtained through informed sampling within the ellipsoidal sampling region (green ellipse). Blue lines show the expanded tree generated during the optimization phase.
:::
::::

Figure [3](#fig:esirrt){reference-type="ref" reference="fig:esirrt"} presents key stages of the E-SIRRT\* pipeline. Figure [\[fig:tree_merged\]](#fig:tree_merged){reference-type="ref" reference="fig:tree_merged"} shows the initial tree constructed from the grid map skeleton, along with the splined initial path (magenta) and the smoothed initial path obtained after collision-aware correction (cyan). Figures [\[fig:tree_rewired_forward\]](#fig:tree_rewired_forward){reference-type="ref" reference="fig:tree_rewired_forward"} and [\[fig:tree_rewired_both\]](#fig:tree_rewired_both){reference-type="ref" reference="fig:tree_rewired_both"} depict the tree after forward and bidirectional rewiring, respectively, with rewired regions highlighted by dotted rectangles. Figure [\[fig:tree_final_path\]](#fig:tree_final_path){reference-type="ref" reference="fig:tree_final_path"} shows the refined initial path (green), extracted from the rewired tree and used as the starting point for informed optimization. Finally, Figure [\[fig:result_path\]](#fig:result_path){reference-type="ref" reference="fig:result_path"} presents the final result after informed optimization, including the optimized path (red), the ellipsoidal sampling region (green ellipse), and the expanded tree structure (blue lines).

# Experimental Results and Analysis {#exp_result}

## Experimental Setup

To evaluate the performance of the proposed E-SIRRT\* planner, we conducted experiments in two 2D grid map environments. The first environment, shown in Fig. [3](#fig:esirrt){reference-type="ref" reference="fig:esirrt"}, is a modified version of the publicly available benchmark map *Freiburg-079*[@mrpt_fr079], featuring multiple rooms connected by corridors. The second environment, illustrated in Fig. [4](#fig:exp03){reference-type="ref" reference="fig:exp03"}, is a simulated scenario designed specifically to include a narrow passage, which poses a significant challenge to sampling efficiency.

We compared E-SIRRT\* against two baselines: the original SIRRT\* and IRRT\*. Each planner was evaluated over 100 independent trials in both environments. During each trial, we recorded the solution cost at every iteration and analyzed convergence behavior over a fixed number of post-initial iterations. The number of informed optimization iterations after the initial solution was fixed at 20,000 in the first environment and 2,000 in the second. These values were selected to be sufficiently large to allow each planner to approach convergence.

Since IRRT\* relies on random sampling to compute its initial solution, the number of iterations required before entering the informed optimization phase varies by trial. Therefore, we also recorded the number of iterations needed to obtain the initial solution in IRRT\* as part of the comparative analysis.

All experiments were implemented in C++ and executed on an Intel Core i9-14900K CPU running at 6.0 GHz with 128 GB of RAM. Grid maps were represented as binary occupancy images, and collision checking was performed using OpenCV-based line tracing.

## Quantitative Comparison

::: {#tab:convergence-benchmark_1}
  -------------------- -- -- --
                             
  Iteration                  
  $\pm$ 1291.09              
  (356--7162)                
                             
  Cost                       
  $\pm$ 106.61               
  (1391.97--1793.91)         
  $\pm$ 0.00                 
  $\pm$ 0.00                 
                             
  Cost                       
  $\pm$ 1.76                 
  (1272.85--1283.36)         
  $\pm$ 1.62                 
  (1273.81--1282.24)         
  $\pm$ 1.38                 
  (1272.96--1279.49)         
  -------------------- -- -- --

  : Convergence Results Experiment #1
:::

The convergence characteristics of IRRT\*, SIRRT\*, and the proposed E-SIRRT\* are summarized in Tables [1](#tab:convergence-benchmark_1){reference-type="ref" reference="tab:convergence-benchmark_1"} and [2](#tab:convergence-benchmark_3){reference-type="ref" reference="tab:convergence-benchmark_3"}, and visualized in Figs.[5](#fig:cost1){reference-type="ref" reference="fig:cost1"} and [6](#fig:cost3){reference-type="ref" reference="fig:cost3"}. Performance is evaluated in terms of initial iteration count (for IRRT\*), initial and final path costs, and consistency across 100 independent trials in each environment.

**Experiment #1.** IRRT\* exhibits substantial variability in computing an initial solution, with iteration counts ranging from 356 to 7162 (mean: 1922.38, std: 1291.09). This high trial-to-trial variance arises despite identical start and goal positions, highlighting IRRT\*'s sensitivity to random sampling. Such unpredictability is particularly problematic in practical applications where robustness and repeatability are essential. In contrast, both SIRRT\* and E-SIRRT\* deterministically generate initial solutions from the grid map skeleton, resulting in zero variance.

E-SIRRT achieves the best initial path quality, with an initial cost of 1301.84, markedly lower than that of SIRRT\* (1484.38) and IRRT\* (1531.91). After 20,000 post-initial iterations, E-SIRRT\* achieves the lowest final cost (1276.05) with the smallest variance ($\pm$`<!-- -->`{=html}1.38), demonstrating both faster convergence and higher consistency. As shown in Fig. [5](#fig:cost1){reference-type="ref" reference="fig:cost1"}, E-SIRRT\* consistently outperforms IRRT\* and SIRRT\* across best-, median-, and worst-case trials. IRRT\* converges more slowly and exhibits large fluctuations in the worst case (Fig. [5](#fig:cost1){reference-type="ref" reference="fig:cost1"}c), while SIRRT\* shows stable but less efficient performance due to the lack of geometric refinement.

::: {#tab:convergence-benchmark_3}
  ------------------ -- -- --
                           
  Iteration                
  $\pm$ 65.20              
  (36--497)                
                           
  Cost                     
  $\pm$ 43.77              
  (150.68--308.71)         
  $\pm$ 0.00               
  $\pm$ 0.00               
                           
  Cost                     
  $\pm$ 0.64               
  (144.41--147.68)         
  $\pm$ 0.50               
  (144.43--146.41)         
  $\pm$ 0.52               
  (144.31--146.78)         
  ------------------ -- -- --

  : Convergence Results Experiment #2
:::

**Experiment #2.** This experiment introduces a narrow passage to evaluate sampling efficiency in constrained settings. IRRT\* again shows considerable variation in initial iteration count (mean: 118.79, std: 65.20), reinforcing its unreliability. E-SIRRT\* yields an initial cost (213.17) slightly higher than the IRRT\* mean (209.11) but with zero variance due to its deterministic initialization. This makes E-SIRRT\* significantly more consistent and dependable, especially in early iterations.

Despite similar final costs ($\approx$`<!-- -->`{=html}145) across methods, E-SIRRT\* converges with lower variance and smoother progression, as seen in Fig. [6](#fig:cost3){reference-type="ref" reference="fig:cost3"}. IRRT\* occasionally achieves competitive performance but suffers from high trial variability. SIRRT\* remains consistent but lacks the geometric refinement needed for accelerated convergence.

A representative result from E-SIRRT\* in Experiment #2 is shown in Fig. [4](#fig:exp03){reference-type="ref" reference="fig:exp03"}. Fig. [\[fig:esirrt_initial_03\]](#fig:esirrt_initial_03){reference-type="ref" reference="fig:esirrt_initial_03"} shows the initial tree along with the MST-derived initial path (cyan) and its hybrid-smoothed version (magenta). Although the smoothed path may visually appear less smooth due to collision-aware adjustments, it significantly reduces the path length compared to the initial MST-derived path. Fig.[\[fig:tree_rewired_03\]](#fig:tree_rewired_03){reference-type="ref" reference="fig:tree_rewired_03"} shows the tree after bidirectional rewiring, where the refined initial path (green) is embedded. Fig.[\[fig:esirrt_03\]](#fig:esirrt_03){reference-type="ref" reference="fig:esirrt_03"} presents the final optimized path (red) obtained through informed sampling within the ellipsoidal sampling region.

:::: {#fig:exp03 .figure latex-placement="t"}
::: caption
E-SIRRT\* result from **Experiment #2**. (a) Initial tree structure (blue nodes and edges) with the extracted MST path (cyan line) and its hybrid-smoothed version (magenta line). (b) Rewired tree structure and the refined initial path (green line) after bidirectional rewiring. (c) Final optimized path (red line) after informed sampling, along with the sampling ellipse (green) used during optimization.
:::
::::

:::: {#fig:cost1 .figure latex-placement="t"}
::: caption
Convergence of path cost over post-initial iterations for IRRT\*, SIRRT\*, and Enhanced SIRRT\* (E-SIRRT\*) in Experiment #1. Each plot shows the path cost after the initial solution is obtained. (a) Best-case performance. (b) Median-case performance. (c) Worst-case performance.
:::
::::

:::: {#fig:cost3 .figure latex-placement="t"}
::: caption
Convergence of path cost over post-initial iterations for IRRT\*, SIRRT\*, and Enhanced SIRRT\* (E-SIRRT\*) in Experiment #2. Each plot shows the path cost after the initial solution is obtained. (a) Best-case performance. (b) Median-case performance. (c) Worst-case performance.
:::
::::

In summary, these experimental results confirm the motivation of the proposed method: traditional random-sampling-based planners such as IRRT\* exhibit high variance and delayed convergence, whereas structure-aware methods provide improved reliability. While SIRRT\* achieves robustness through deterministic tree initialization, it lacks geometric refinement capabilities. E-SIRRT\* addresses this shortcoming by incorporating hybrid path smoothing and bidirectional rewiring, resulting in high-quality initial paths and trees with consistent cost propagation.

# Conclusion

This paper introduced E-SIRRT\*, an advanced structure-aware path-planning algorithm extending the original SIRRT\* through hybrid path smoothing and bidirectional rewiring. These enhancements refine the geometry of the initial path and improve tree connectivity, effectively overcoming limitations of existing sampling-based planners related to initialization quality and convergence speed. Comprehensive experiments conducted in structured and constrained grid-based environments showed that E-SIRRT\* consistently delivers faster convergence and more stable performance compared to IRRT\* and SIRRT\*, while preserving deterministic behavior. The findings validate that combining skeleton-based initialization with principled geometric and structural refinements results in reliable and high-quality motion plans.

Future research will focus on extending E-SIRRT\* to higher-dimensional planning scenarios and exploring its integration with task-informed or learning-based sampling strategies to further improve scalability and adaptability.

[^1]: This research was supported by the National Research Foundation of Korea grant funded by the Korea government, Ministry of Science and ICT (No. NRF-2022R1C1C1010931).

[^2]: $^{1}$Hyejeong Ryu is with Faculty of Mechatronics Engineering, Kangwon National University, Gangwon 24341, South Korea `hjryu@kangwon.ac.kr`
