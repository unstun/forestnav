---
citation_key: Le2024Global
arxiv_id: 2411.19393
arxiv_url: https://arxiv.org/abs/2411.19393
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:48:00Z
origin: ai+web
reviewed: false
---

:::: titlepage
\
IEEE Copyright Notice\

::: spacing
1.2 © 2025 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
:::
::::

Le *et al.*: Global Tensor Motion Planning

::: IEEEkeywords
Motion and Path Planning, Manipulation Planning
:::

# Introduction {#sec:intro}

Motion planning with probabilistic completeness has been a foundation of robotics research, with seminal works like PRM [@kavraki1996probabilistic] and RRTConnect [@kuffner2000rrt] serving as cornerstone methods for years [@latombe2012robot]. However, as the complexity of robotic tasks increases, there is a growing demand for batch-planning methods. Several factors drive this interest: (i) the need to gather large datasets for policy learning [@carvalho2023mpd; @wang2021survey; @reuss2023goal], (ii) the inherent non-linearity of task objectives that lead to multiple viable solutions [@le2024accelerating; @mukadam2018continuous; @osa2020multimodal], and (iii) the increasing availability of powerful GPUs/TPUs for accelerated planning [@bhardwaj2022storm; @sundaralingam2023curobo]. Despite these advances, batching traditional sampling-based planners, such as RRT/PRM and their variants, remains an ongoing challenge [@pan2012gpu; @bialkowski2011massively; @blankenburg2020towards; @jacobs2012scalable]. Their underlying discretization techniques, such as the incremental graph construction of RRT/PRM or the search mechanism of A\* [@hart1968astar; @russell2016artificial], are not conducive to efficient vectorization over planning instances.

This paper revisits classical motion planning, where we plan from a single start configuration to multiple goal configurations. We introduce a simple yet effective discretization structure with layers of waypoints, which can be represented as tensors, enabling GPU/TPU utilization. We propose Global Tensor Motion Planning (GTMP), which enables highly batchable operations on multiple planning instances, such as batch collision checking and batch [vi]{acronym-label="vi" acronym-form="singular+short"}, inducing an easily vectorizable implementation with JAX [@jax2018github]. This simplicity allows for differentiable planning and rapid integration with modern frameworks, making the algorithm particularly desirable for real-time applications and scalable data collection for robot learning. Our experimental results demonstrate much better batch efficiency planning than standard baseline implementations while achieving similar smoothness and better path diversity with the spline discretization structure.

Our contributions are twofold: i) we propose a *vectorizable sampling-based planner* exhibiting probabilistic completeness, which does not require simplification routines [@sucan2012open], and ii) we extend GTMP with a spline discretization structure, enabling batch spline planning with path quality comparable to trajectory optimizers.

:::: {#fig:method .figure latex-placement="th"}
![](Le2024Global_figs/final_overview.png){width="\\textwidth"}

::: caption
GTMP can plan with multiple goals or `vmap` over goals. For clarity, we present an example of performing JAX `vmap` on GTMP (M=2, N=3) over the batch of $B=3$ seeds. **(1)** The objective is to find a batch of feasible paths from the start (red) to the goals (green). **(2, 3)** In each seed, we sample a multipartite graph and form a tensor (Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"}, Line 1). **(4)** A batch of collision checks is performed and stored into cost matrices (Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"}, Line 2). **(5)** Then, per seed, we execute finite value iterations (Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"}, Line 5-7) and trace the optimal path from the optimal value matrices (Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"}, Line 8-13). **(6)** For execution, we can select the best path in terms of exemplary shortest path criteria. More information can be found on <https://sites.google.com/view/gtmp>.
:::
::::

# Related Works {#sec:related_works}

Vectorizing motion planning has been an active research topic for decades. Here, we briefly survey the most relevant works on vectorizing either at the *algorithmic*-level (e.g., collision-checking) or *instance*-level (e.g., batch trajectory planning).

**Sampling-based Vectorization.** Recognizing the importance of planning parallelization, earliest works [@amato1999probabilistic; @plaku2005sampling; @bialkowski2011massively; @jacobs2012scalable; @pan2012gpu] propose a *vectorizable* collision-checking data structure. State-of-the-art work on leveraging CPU-based *single instruction, multiple data* [@thomason2024motions] (i.e., VAMP) has pushed collision-checking efficiency to *microseconds*. In a different vein, a body of works [@gammell2020batch; @janson2015fast; @strub2020adaptively; @wang2020neural; @yu2021reducing; @ichter2018learning] proposes a learning heuristic or batch-sampling strategies to inform or refine the search-graph with new samples, effectively reducing collision checking. Despite the hardware or algorithmic acceleration efforts, past works still resort to discretization structures such as trees for RRT variants or graphs for PRM variants [@orthey2023sampling], which are unsuitable for instance-level vectorization.

**Vectorizing Trajectory Optimization.** Vectorizing optimization-based planner with GPU-acceleration [@adajania2022multi; @lambert2020stein; @bhardwaj2022storm; @urain2022sgmpg; @le2024accelerating] gained traction recently due to their computational efficiency, the solutions' multi-modality, and their robustness to bad local-minima. However, these local methods are sensitive to initial conditions and may get stuck in large infeasible regions, thereby the need for warmstarting the sampling-based global solutions [@sundaralingam2023curobo]. GTMP addresses this issue by proposing a layerwise discretization structure, enabling vectorization in sampling and search operations while having better global solutions.

# Tensorizing Motion Planning {#sec:method}

We consider the path planning problem [@lavalle2006planning] for a configuration ${\bm{q}}$ in compact space ${\bm{q}}\in {\mathcal{C}}\subset {\mathbb{R}}^d$ having $d$-dimensions, with ${\mathcal{C}}_{\textrm{coll}}$ being the collision space such that ${\mathcal{C}}\setminus {\mathcal{C}}_{\textrm{coll}}$ is open. Let ${\mathcal{C}}_{\textrm{free}} = \mathsf{Cl}({\mathcal{C}}\setminus {\mathcal{C}}_{\textrm{coll}})$ be the free space, with $\mathsf{Cl}(\cdot)$ the set closure. Denote the start configuration ${\bm{q}}_0$ and a set of goal configurations ${\mathcal{G}}$. Let $f: [0, 1] \rightarrow {\bm{q}},\,{\bm{f}}(t) \in {\mathcal{C}}$, we can define its total variation as its arc length $$\begin{equation}
 \label{eq:path_tv}
    \textrm{TV}(f) = \sup_{M \in {\mathbb{N}},0=t_0,\ldots,t_M=1} \textstyle\sum_{i=1}^M \left\lVert{\bm{f}}(t_i) - {\bm{f}}(t_{i-1})\right\rVert,
\end{equation}$$

::: definition
**Definition 1** (Feasible Path). *The function $f: [0, 1] \rightarrow {\bm{q}}$ with $\textrm{TV}(f) < \infty$ is*

- *a path, if it is continuous.*

- *a feasible path, if and only if $\forall t \in [0, 1], {\bm{f}}(t) \in {\mathcal{C}}_{\textrm{free}},\, {\bm{f}}(0) = {\bm{q}}_0,\, {\bm{f}}(1) \in {\mathcal{G}}$.*
:::

Let ${\mathcal{F}}$ be the set of all paths. We denote ${\mathcal{F}}_{\textrm{free}}$ as the set of feasible paths for a feasible planning problem. Here, we do not consider dynamic constraints, invalid configurations that violate collision constraints, and configuration limits.

::: problem
**Problem 1** (Batch Path Planning). *Given a planning problem $({\mathcal{C}}_{\textrm{free}}, {\bm{q}}_0, {\mathcal{G}})$ and cost function $c: {\mathcal{F}}\rightarrow {\mathbb{R}}_{>0}$, find a batch of $B > 0$ feasible path $f$ and report failure if no feasible path exists.*
:::

This problem definition is standard for several robotic settings, such as serial manipulators with joint limits. We propose to solve Problem 1 with probabilistic completeness, striving to discover multiple solution modes.

**Practical Motivation.** In essence, GTMP leverages a fixed discretization structure over the whole search space, represented by fixed-shape tensors, to enable efficient planning vectorization with JAX `vmap` operation [@jax2018github]. This approach contrasts with the incremental discretization structures of classical motion planning algorithms, which procedurally expand the search space during planning.

## Discretization Structure

We introduce the random multipartite graph as a novel configuration discretization structure designed to represent planning problems as tensors.

::: {#def:graph .definition}
**Definition 2** (Random Multipartite Graph Discretization). *Consider a geometric graph $G = ({\mathcal{V}}, {\mathcal{E}})$ on configuration space ${\mathcal{C}}$, the node set ${\mathcal{V}}$ is represented by $\{{\bm{q}}_{\textrm{s}}, {\mathcal{M}}, {\mathcal{G}}\}$, where ${\mathcal{M}}= \{{\mathcal{L}}_m\}_{m=1}^M$ is a set of $M$ layers. Each layer ${\mathcal{L}}_m = \{{\bm{q}}_i \in {\mathcal{C}}\mid {\bm{q}}_i \sim p_m\}_{i=1}^N$ contains $N$ waypoints sampled by an associated proposal distribution $p_m$ on ${\mathcal{C}}$. The edge set ${\mathcal{E}}$ is defined by the union of (forward) pair-wise connections between the start and first layer $\{ ({\bm{q}}_{\textrm{s}}, {\bm{q}}) \mid \forall{\bm{q}}\in {\mathcal{L}}_1 \},$ between layers in ${\mathcal{M}}$ $$\begin{equation}
        \{ ({\bm{q}}_m, {\bm{q}}_{m+1}) \mid \forall {\bm{q}}_m \in {\mathcal{L}}_m,\ {\bm{q}}_{m+1} \in {\mathcal{L}}_{m + 1},\, 1 \leq m < M \}, \nonumber
\end{equation}$$ and between the last layer and goals $\{ ({\bm{q}}, {\bm{q}}_{\textrm{g}}) \mid \forall {\bm{q}}\in {\mathcal{L}}_M,\ {\bm{q}}_{\textrm{g}} \in {\mathcal{G}}\},$ leading to a complete $(M+2)$-partite directed graph.*
:::

We typically set $p_m = {\mathcal{U}}({\mathcal{C}})$ as uniform distributions over configuration space (bounded by configuration limits cf. [1](#fig:method){reference-type="ref+label" reference="fig:method"}). Consequently, the graph nodes are represented as the waypoint tensors for all layers ${\bm{Q}}\in {\mathbb{R}}^{M \times N \times d}$ and the goal configuration ${\bm{G}}\in {\mathbb{R}}^{|{\mathcal{G}}| \times d}$ from ${\mathcal{G}}$, within the state limits. Extending [2](#def:graph){reference-type="ref+label" reference="def:graph"} to *spline discretization structure* by replacing the straight line with the cubic polynomials, representing any edge $({\bm{q}}, {\bm{q}}') \in {\mathcal{E}}$, is straightforward with Akima spline [@akima1974method] (cf. [6](#sec:akima){reference-type="ref+label" reference="sec:akima"}).

::: definition
**Definition 3** (Path In $G$). *A path $f: [0, 1] \rightarrow {\bm{q}}$ in $G$ exists if it ${\bm{f}}(0) = {\bm{q}}_0,\, {\bm{f}}(1) \in {\mathcal{G}}$ and its piecewise linear segments correspond to edges connecting ${\bm{q}}_0$ and ${\bm{q}}_g \in {\mathcal{G}}$.*
:::

## State Machine On Graph

The graph $G$ is represented by the state machine $({\mathcal{V}}, {\mathcal{E}}, c, t)$ [@puterman2014markov], where the state set is the node set of $G$, the action set is equivalent to the edge set ${\mathcal{E}}$, the transition cost function $c: {\mathcal{V}}\times {\mathcal{E}}\rightarrow {\mathbb{R}}$, deterministic state transition $t({\bm{q}}' \mid {\bm{q}}, ({\bm{q}}, {\bm{q}}')) = 1,\, ({\bm{q}}, {\bm{q}}') \in {\mathcal{E}}$. The goal set ${\mathcal{G}}\subset {\mathcal{V}}$ is the terminal set with terminal costs $c_g({\bm{q}}),\,{\bm{q}}\in {\mathcal{G}}$. A policy $\pi: {\mathcal{V}}\rightarrow {\mathcal{E}}$ depicts the decision to transition to the next layer, given the current state at the current layer.

We use unbounded occupancy collision costs $$\begin{equation}
 \label{eq:cost_coll}
    c_{\textrm{coll}}({\bm{q}}) = 0 \textrm{ if } {\bm{q}}\in \textrm{int}_{\delta}({\mathcal{C}}_{\textrm{free}}) \textrm{, else } \infty,
\end{equation}$$ which merges the planning and verification steps (cf. Proposition [2](#prop:feasible){reference-type="ref" reference="prop:feasible"}). Then, the transition cost function can be defined $$\begin{equation}
 \label{eq:cost}
   c({\bm{q}}, ({\bm{q}}, {\bm{q}}')) = \underbrace{\int_{a}^{b} c_{\textrm{coll}}({\bm{f}}(t)) f' d t}_{\textrm{collision}} + \underbrace{\left\lVert{\bm{q}}- {\bm{q}}'\right\rVert}_{\textrm{smoothness}},
\end{equation}$$ where the collision term is a straight-line integral with $f' = 1 / \left\lVert{\bm{q}}' - {\bm{q}}\right\rVert$ between ${\bm{f}}(a) = {\bm{q}}$ and ${\bm{f}}(b) = {\bm{q}}'$. Finding the optimal value function on $G$ is straightforward by iterating the Bellman optimality operator $$\begin{align}
 \label{eq:bellman}
    v_G({\bm{q}}) \leftarrow &\min_{({\bm{q}}, {\bm{q}}')} \sum_{{\bm{q}}'} t({\bm{q}}' \mid {\bm{q}}, ({\bm{q}}, {\bm{q}}')) \left(c({\bm{q}}, ({\bm{q}}, {\bm{q}}')) + v_G({\bm{q}}') \right) \nonumber \\
   \leftarrow &\min_{({\bm{q}}, {\bm{q}}')} \left(c({\bm{q}}, ({\bm{q}}, {\bm{q}}')) + v_G({\bm{q}}') \right)
\end{align}$$ with a finite number of iterations $K = M + 1$. The optimal policy is extracted by tracing the optimal value function $$\begin{equation}
 \label{eq:trace}
    \pi^*({\bm{q}}) = \mathop{\mathrm{\arg\!\min}}_{({\bm{q}}, {\bm{q}}')} \left(c({\bm{q}}, ({\bm{q}}, {\bm{q}}')) + v_G^*({\bm{q}}') \right),
\end{equation}$$ from ${\bm{q}}_0$ until ${\bm{q}}' \in {\mathcal{G}}$ [@puterman2014markov]. This produces a sequence of edges ${{\mathcal{P}}= \{({\bm{q}}_0, {\bm{q}}_1), \ldots, ({\bm{q}}_M, {\bm{q}}_g) \mid {\bm{q}}_g \in {\mathcal{G}}\}}$.

::: {#prop:clen .proposition}
**Proposition 1**. *By following any policy on $({\mathcal{V}}, {\mathcal{E}}, c, t)$ from ${\bm{q}}_0$, ${\mathcal{P}}$ has a constant cardinality of $M + 1$.*
:::

By construction of graph $G$, each application of [\[eq:trace\]](#eq:trace){reference-type="ref+label" reference="eq:trace"} increases the layer number $m$ strictly monotonically, since $t({\bm{q}}_{m+1} \mid {\bm{q}}_m, \pi({\bm{q}}_m)) = t({\bm{q}}_{m+1} \mid {\bm{q}}_m, ({\bm{q}}_m, {\bm{q}}_{m+1})) = 1,\, ({\bm{q}}_m, {\bm{q}}_{m+1}) \in {\mathcal{E}}$. Hence, $|{\mathcal{P}}| = M + 1$. Finding optimal paths by finite [vi]{acronym-label="vi" acronym-form="singular+short"} over a discretization structure has been a common practice and widely applied in different settings [@bertsekas2012dynamic]. However, to our knowledge, applying [vi]{acronym-label="vi" acronym-form="singular+short"} over a random multipartite graph, enabling batching mechanisms over planning instances, is novel, as we present in the next section.

## Batching The Planner

In practice, we do not need to construct an explicit graph data structure due to $G$'s multipartite structure. Observing the deterministic state transition and the equal cardinality of layers, we just need to compute and maintain the transition cost matrices ${\bm{C}}_s \in {\mathbb{R}}^N,\, {\bm{C}}_h \in {\mathbb{R}}^{(M - 1) \times N \times N},\, {\bm{C}}_l^{N \times |{\mathcal{G}}|}$ and value matrices $V_s \in {\mathbb{R}},\, {\bm{V}}_h \in {\mathbb{R}}^{M \times N},\, {\bm{V}}_g \in {\mathbb{R}}^{|{\mathcal{G}}|}$, where ${\bm{C}}_s$ is the transition costs from ${\bm{q}}_0$ to the first layer; ${\bm{C}}_h, {\bm{C}}_l$ hold transition costs between middle layers and last layer to goals; $V_s, {\bm{V}}_h, {\bm{V}}_g = {\bm{C}}_g$ hold values of start, layers costs and terminal goal costs. Given the uniformly-sampled waypoint tensors ${\bm{Q}}\in {\mathbb{R}}^{M \times N \times d}$ and the goals ${\bm{G}}\in {\mathbb{R}}^{|{\mathcal{G}}| \times d}$, the cost-to-go term of the transition costs [\[eq:cost\]](#eq:cost){reference-type="ref+label" reference="eq:cost"} is approximately computed by first probing an $H$ number of equidistant points on all edges, evaluating them in batches, and taking the mean values over the probing dimension. We assume all cost functions are batch-wise computable.

The GTMP algorithm is compactly presented in Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"}. Note that Line 6 is a matrix-reduced `min` operation on the last dimension, while the `sum` is broadcasted to the middle dimension of the cost matrix ${\bm{C}}_h \in {\mathbb{R}}^{(M - 1) \times N \times N}$ from the value matrix ${\bm{V}}_h \in {\mathbb{R}}^{M \times 1 \times N}$. After $M + 1$ Bellman iterations (Line 5-7), given the converged value matrix ${\bm{V}}_h^*$, a sequence of waypoints is traced over the layers to the goals (Line 11-13). Notice that all component matrices can be straightforwardly vectorized by adding the batch dimension $B$ for all matrices, and the whole algorithm can be JAX `vmap` over sampling seeds on line 1. Note that [@pan2012gpu; @bialkowski2011massively; @blankenburg2020towards; @thomason2024motions] focus on vectorizing collision checking or forward kinematics in a single planning instance, while we can ensure that Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"} can be vectorized at the instance-level [@le2024accelerating] by [1](#prop:clen){reference-type="ref+label" reference="prop:clen"}.

::::: {#alg:gtmp .figure latex-placement="b"}
::: algorithm
Uniformly sample ${\bm{Q}}\in {\mathbb{R}}^{M \times N \times d}$\
Compute cost matrices ${\bm{C}}_s, {\bm{C}}_h, {\bm{C}}_l$ as [\[eq:cost\]](#eq:cost){reference-type="ref+label" reference="eq:cost"}\
Init $V_s \in {\mathbb{R}},\, {\bm{V}}_h \in {\mathbb{R}}^{M \times N},\, {\bm{V}}_g \in {\mathbb{R}}^{|{\mathcal{G}}|}$ $i \leftarrow \mathop{\mathrm{\arg\!\min}}({\bm{C}}_s + {\bm{V}}_h^*[0])$ ${\mathcal{P}}= \{i\}$\
$i \leftarrow \mathop{\mathrm{\arg\!\min}}({\bm{C}}_l[i] + {\bm{V}}_g)$ and append ${\bm{G}}[i]$ to ${\mathcal{P}}$\
:::

::: caption
Global Tensor Motion Planning
:::
:::::

**Complexity Analysis.** The Bellman matrix update (Line 5-7) is an asynchronous update in batches (i.e., updates based on values of previous iteration) and also known to converge [@bertsekas2015parallel]. Considering the layer number $M$, waypoint number per layer $N$, and probing number $H$, we assume that the Bellman matrix update is executed on $P$ processor units, an estimate of time complexity per [vi]{acronym-label="vi" acronym-form="singular+short"} iteration is ${\mathcal{O}}(MN^2 / P)$ due to the broadcasted `sum` and `min` operator on Line 6 Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"}. Hence, the overall worst-case time complexity is ${\mathcal{O}}(M^2N^2/P)$, with a fixed number of $M+1$ [vi]{acronym-label="vi" acronym-form="singular+short"} iterations. The collision-checking time complexity is ${\mathcal{O}}(MN^2H/P)$, and thus, the overall time complexity is ${\mathcal{O}}(MN^2(H + M)/P)$. The space complexity is ${\mathcal{O}}(MN^2H)$ due to the collision checking. Theoretical investigations regarding GTMP probabilistic completeness are presented in [7](#sec:theory){reference-type="ref+label" reference="sec:theory"}.

# Experiment Results {#sec:experiments}

We assess the performance of GTMP and its smooth extension on batch planning and single planning capability compared to popular baselines and collision-checking mechanisms. Hence, we investigate the following questions for batch trajectory generation, or for finding the global solution: i) how does GTMP with JAX/GPU-implementation compare to highly optimized probabilistic-complete planners implemented in PyBullet/OMPL [@sucan2012open; @coumans2019] or in VAMP [@thomason2024motions]?, ii) how does GTMP-Akima compare to popular gradient-based smooth trajectory optimizers such as CHOMP [@zucker2013chomp] or GPMP [@mukadam2018continuous]?, and iii) Are the empirical results consistent with the theoretical guarantees ([1](#thm:prob){reference-type="ref+label" reference="thm:prob"})?

**Settings.** We run all CPU-based planners (RRTC, BKPIECE) on AMD Ryzen 5900X clocked at 3.7GHz and GPU-based planners (GTMP, CHOMP, GPMP, cuRobo) on a single Nvidia RTX 3090. Note that GTMP, CHOMP, and GPMP are implemented in JAX [@jax2018github], and the planning times are measured after JIT. We use cuRobo's official PyTorch implementation. We initialize CHOMP and GPMP with samples from a high-variance Gaussian process prior [@urain2022sgmpg] connecting from the start to the goals. We set a default probing $H=10$ and used uniform sampling for all GTMP runs. For all CPU-based planners, we give a timeout of one minute and report metrics after simplification routines. Planning time per task is the sum of all planning instances, which includes simplification time for CPU-based planners, while GTMP does not need path simplification.

**Metrics.** The metrics are chosen for comparing across probabilistically-complete planners and trajectory optimizers: (i) *Planning Time (s)* in seconds of a batch of paths given a task, (ii) *Collision Free (CF %)* percentage of paths in a batch (failure cases are either in collision or timeout), (iii) *Minimum Cosine Similarities (Min Cosim)* over consecutively path segments and averaging over the batch of paths in a task, (iv) *Paths Diversity (PD)* as the mean of pairwise Sinkhorn [@cuturi2013sinkhorn] distances in a batch having $B$ paths $$\begin{equation}
    PD = \frac{1}{B (B - 1)}{\textrm{OT}_\lambda ({\mathcal{P}}_i, {\mathcal{P}}_j)},\, i,j \in \{1, \ldots, B\},
\end{equation}$$ where we treat the path ${\mathcal{P}}= \{{\bm{q}}_0, \ldots {\bm{q}}_T\}$ as empirical distribution with uniform weights, and different paths can have different horizons $T$. The entropic scalar $\lambda=5e^{-3}$ is constant. The metric *Min Cosim* measures the worst/average rough turns over path segments, which represents worst-case jerks since baselines plan different trajectory dynamic orders. The PD measures the spread of solution paths correlating to solutions' modes discovery.

## Batch Planning Comparison {#subsec:batch_exp}

Fig. [3](#fig:exp){reference-type="ref" reference="fig:exp"} (top-row) compares GTMP and GTMP-Akima with OMPL implementation of (single-query) RRTConnect [@kuffner2000rrt] and BKPIECE [@csucan2009kinodynamic]. The environments are planar occupancy maps of Intel Lab, ACES3 Austin, Orebro, Freiburg Campus, and Seattle UW Campus generated from the Radish dataset [@radish]. The maps are chosen to include narrow passages, large spaces, and noisy occupancies (cf. [1](#fig:method){reference-type="ref+label" reference="fig:method"}). We randomly sample $100$ start-goal pairs as tasks on each map and plan $100$ paths per task. We clearly see a comparable Min Cosim (i.e., similar statistics of rough turns) and PD of GTMP (M=200, N=4) compared to baselines across maps and in aggregated statistics over maps. With JIT and GPU utilization, GTMP consistently produces batch paths with a fixed number of segments and x10000 less wall-clock time compared to baselines across maps.

:::: {#fig:exp .figure latex-placement="t"}
![](Le2024Global_figs/real_mbm_exp.png){width="\\linewidth"}

::: caption
Aggregated statistics of comparison experiments on Planar Occupancy (top-row) and Panda MBM dataset (bottom-row). We note the log scale on the Planning Time axes. The batch planning time is the sum of instance time for sequential planners (last column). All plotted data points are based on successful path statistics.
:::
::::

::: {#tab:mpinet_exp}
  **Algorithms**                       **PT $\downarrow$** (ms)   **Success $\uparrow$** (%)   **Path Length $\downarrow$**   **Min Cosim $\uparrow$**   **PD $\uparrow$**
  ----------------------------------- -------------------------- ---------------------------- ------------------------------ -------------------------- -------------------
  GTMP (N=30, M=2)                              $0.11$                      $99.6$                        $4.8$                        $-0.3$                  $7.7$
  GTMP-Akima (N=30, M=2)                        $0.10$                      $97.1$                        $7.3$                        $-0.1$             $\mathbf{7.8}$
  VAMP/RRTC [@thomason2024motions]         $\mathbf{0.09}$             $\mathbf{100.0}$                   $3.6$                    $\mathbf{0.1}$               \-
  cuRobo [@sundaralingam2023curobo]             $43.1$                      $99.7$                    $\mathbf{2.8}$                   $0.0$                    \-

  : Aggregated Statistics Of M$\pi$Nets Dataset
:::

We choose the [MotionBenchMaker]{.smallcaps} (MBM) dataset [@chamzas2021motionbenchmaker] of $7$-DoF Franka Emika Panda tasks such as table-top manipulation (*table pick and table under pick*), reaching (*bookshelf small, tall and thin*), and highly-constrained reaching (*box and cage*). Each task is pre-generated with $100$ problems available publicly. We implement our collision-checking in JAX via primitive shape approximation, such as a Panda spherized model, oriented cubes, and cylinders representing tasks in MBM. The default hyperparameters and compilation configurations for VAMP/RRTC, OMPL/RRTC, and OMPL/BKPIECE are also adopted following [@thomason2024motions][^6]. CHOMP and GPMP plan first-order trajectories having a horizon of $T=32$. All algorithms are compared on the planning performance of a batch of $B=50$ paths for all tasks.

Fig. [3](#fig:exp){reference-type="ref" reference="fig:exp"} (bottom-row) shows the planning performance comparisons between GTMP (N=30, M=2) and baseline probabilistically-complete planners and gradient-based trajectory optimizers. We see that GTMP consistently has the best diversity (PD) and worst rough turn statistics (Min Cosim) in all tasks. This is due to the maximum exploration behavior of GTMP by sampling uniformly over configuration space, which increases the risk of rough paths. In principle, increasing points per layer $N$ while having minimum solving layers $M$ would improve Min Cosim due to having more chances to discover smoother paths with fewer segments, as long as GPU memory allows (cf. [4](#fig:sweep_exp){reference-type="ref+label" reference="fig:sweep_exp"}). Compared with gradient-based optimizers, GTMP-Akima with spline discretization construction has a similar Min Cosim to cuRobo while not requiring gradients from the planning costs. Note that cuRobo additionally considers dynamical constraints, which increases planning time but improves metrics such as maximum model jerk. On batch planning efficiency, GTMP and GTMP-Akima achieve x50 faster than state-of-the-art VAMP/RRTC implementation while being x2500 faster than CHOMP/GPMP/cuRobo and x100000 faster than the OMPL implementation with PyBullet collision checking. We leave the investigation of combining GTMP with the VAMP collision checking for future work.

Fig [3](#fig:exp){reference-type="ref" reference="fig:exp"} (first-column) shows the distributions of single-instance planning time versus number of path segments, reflecting inherent algorithmic differences between GTMP and RRTC implementations. RRTC blobs are spread due to differences in randomized graph explorations between planning instances and are separated due to differences in collision-checking efficiency [@thomason2024motions]. GTMP vectorizes planning via layered structure, resulting in predictable narrow distribution due to fixed-segment path planning.

## Single Plan Comparison {#subsec:mpinet_exp}

We compare GTMP and GTMP to the strong baselines such as VAMP/RRTC [@thomason2024motions] and cuRobo [@sundaralingam2023curobo], in terms of single planning for execution, on the M$\pi$Nets dataset [@fishman2023motion] of diverse $7$-DoF Franka Emika Panda tasks. We set $B=50$ for GTMP/GTMP-Akima and select the lowest path length for execution. We plan a single instance for VAMP/RRTC and cuRobo.  [1](#tab:mpinet_exp){reference-type="ref+label" reference="tab:mpinet_exp"} shows that GTMP achieves a similar success rate to the baselines (i.e., at least one successful path in the batch) while having similar planning time to the state-of-the-art VAMP/RRTC. However, due to the maximum exploration nature, GTMP performs worse regarding path quality. Future works on better sampling strategy per layer could improve GTMP path quality while increasing the sample efficiency on $M, N$ for low-memory planning.

## Ablation Study {#subsec:ablation}

This section explores various aspects of GTMP by sweeping the number of layer $M$ and number of points per layer $N$. [4](#fig:sweep_exp){reference-type="ref+label" reference="fig:sweep_exp"} shows the sweeping statistics of $M \in \{2, 3, \ldots, 80\}, N\in \{10, 11, \ldots, 100\}$ on the Intel Lab occupancy map with a fixed start-goal pair to experimentally confirm the probabilistic completeness [1](#thm:prob){reference-type="ref+label" reference="thm:prob"}. In Fig. [4](#fig:sweep_exp){reference-type="ref" reference="fig:sweep_exp"}, Planning Time heatmap shows an experimentally infinitesimal increase in polynomial planning time-complexity over increasing $M,N$ (due to JIT-ing finite VI loops and efficient batch collision-checking, cf. [3](#sec:method){reference-type="ref+label" reference="sec:method"}). Then, the CF(%) heatmap directly reflects the path existence probability [\[eq:probc\]](#eq:probc){reference-type="ref+label" reference="eq:probc"}. Notice that the minimum layer $M_m = 3$ must be set for collision-free paths in the batch. Interestingly, $M_m$ is also the optimal number of layers to achieve non-zero CF(%) with a minimal point per layer $N$ (red star), which confirms the observation in [7](#sec:theory){reference-type="ref+label" reference="sec:theory"}. Next, further observations on Min Cosim also confirm that with less $M$, the paths are smoother. Finally, higher path diversity is induced by having higher CF(%), corresponding to the top-right heatmap.

:::: {#fig:sweep_exp .figure latex-placement="t"}
![](Le2024Global_figs/benchmark_plot.png){width="\\columnwidth"}

::: caption
For each $M$ (y-axis), $N$ (x-axis), we set the number of probing $H=30$ and plan the batch of $B=200$ paths. The red star denotes the minimum number of layers $M_m$, corresponding to the minimum requirement of $N$ to discover some solutions experimentally.
:::
::::

# Discussion & Conclusions {#sec:conclusion}

GTMP offers several advantages algorithmically, as it is *vectorizable* over a large number of planning instances, it does not require *joint-limit enforcement* (i.e., sampling points in the limits), *gradients* or *simplification routines*. On the practical side, GTMP is *easy to implement* (i.e., only tensor manipulation), *easy to tune* (i.e., hyperparameter $M, N, H$), and *easy to incorporate* motion planning objectives in [\[eq:cost_akima\]](#eq:cost_akima){reference-type="ref+label" reference="eq:cost_akima"}.

GTMP is designed to be efficient in batch planning representing multiple instances of the same planning problem. The batch dimension representing the multiple GTMP planning instances can be interpreted as multiple replanning attempts. Indeed, Theorem [1](#thm:prob){reference-type="ref" reference="thm:prob"} depicts probabilistic completeness over the batch dimension and $M, N$, contrasting with probabilistic completeness over exploration nodes as in RRT\* [@karaman2011sampling]. Beyond GTMP, since Algorithm [2](#alg:gtmp){reference-type="ref" reference="alg:gtmp"} is cheap in common case, we could also derive an outer loop gradually increasing $M, N$ until some solutions in the batch are found.

GTMP addresses global exploration challenges but comes with memory requirements, especially for GPU acceleration. In contrast, local methods such as CHOMP or GPMP leverage gradient-based, more memory-efficient trajectory optimization. GTMP-Akima, for instance, avoids the need for gradients while delivering smooth velocity trajectories by a *spline discretization structure*, making it a viable initialization for methods like GPMP, potentially combining the strengths of both approaches.

Variants of GTMP emphasize maximum exploration while maintaining smooth trajectory structures. Exploring further smooth discretization structures for higher-order planning is exciting, as the current Akima discretization structure only provides a $C^1$ spline grid. Furthermore, we are eager to adopt the efficient collision-checking of VAMP [@thomason2024motions] for GTMP, when the VAMP batching configuration collision-checking becomes available, extending GTMP to CPU-based vectorization. Lastly, GTMP suggests the direction of probabilistically-complete batch planners, serving as a differentiable global planner or a competent oracle for learning.

# APPENDIX {#app:akima .unnumbered}

# Extension: Akima Spline {#sec:akima}

The Akima spline [@akima1974method] is a piecewise cubic interpolation method that exhibits $C^1$ smoothness by using local points to construct the spline, avoiding oscillations or overshooting in other interpolation methods, such as cubic splines or B-splines.

::: {#def:akima .definition}
**Definition 4** (Akima Spline). *Given a point set $\{ {\bm{q}}_i | {\bm{q}}\in {\mathcal{C}}\}_{i=1}^P$, the Akima spline constructs a piecewise cubic polynomial $f(t)$ for each interval $[t_i, t_{i+1}]$ $$\begin{equation}
 \label{eq:poly_akima}
    f_i(t) = {\bm{d}}_i (t - t_i)^3 + {\bm{c}}_i (t - t_i)^2 + {\bm{b}}_i (t - t_i) + {\bm{a}}_i,
\end{equation}$$*

*where the coefficients ${\bm{a}}_i, {\bm{b}}_i, {\bm{c}}_i, {\bm{d}}_i \in {\mathcal{C}}$ are determined from the conditions of smoothness and interpolation. Let ${\bm{m}}_i = ({\bm{q}}_{i + 1} - {\bm{q}}_{i}) / (t_{i+1} - t_i)$ at $t_i$, the spline slope is computed from $m_{i-1}, m_{i+1}$*

*$$\begin{equation}
{\bm{s}}_i = \frac{|{\bm{m}}_{i+1} - {\bm{m}}_i | {\bm{m}}_{i-1} + |{\bm{m}}_{i-1} - {\bm{m}}_{i-2} | {\bm{m}}_{i}}{|{\bm{m}}_{i+1} - {\bm{m}}_i| + |{\bm{m}}_{i-1} - {\bm{m}}_{i-2}|}.
\end{equation}$$*

*The spline slopes for the first two points at both ends are ${\bm{s}}_1 = {\bm{m}}_1, {\bm{s}}_2 = ({\bm{m}}_1 + {\bm{m}}_2) / 2, {\bm{s}}_{P-1} = ({\bm{m}}_{P-1} + {\bm{m}}_{P-2}) / 2, {\bm{s}}_P = {\bm{m}}_{P-1}$. Then, the polynomial coefficients are uniquely defined $$\begin{align}
 \label{eq:akima_coeff}
&{\bm{a}}_i = {\bm{q}}_i, \quad {\bm{b}}_i = {\bm{s}}_i, \nonumber\\
&{\bm{c}}_i = (3{\bm{m}}_i - 2{\bm{s}}_i - {\bm{s}}_{i+1}) / (t_{i+1} - t_i),\\
&{\bm{d}}_i = ({\bm{s}}_i + {\bm{s}}_{i+1} - 2{\bm{m}}_{i}) / (t_{i+1} - t_i)^2. \nonumber
\end{align}$$*
:::

The Akima spline slope is determined by the local behavior of the data points, preventing oscillations that can occur when using global information. Interpolating with Akima spline does not require solving large systems of linear equations, making it computationally efficient as an ideal extension to [2](#def:graph){reference-type="ref+label" reference="def:graph"} to *a spline discretization structure*.

::: definition
**Definition 5** (Akima Spline Graph). *Given a geometric graph $G = ({\mathcal{V}}, {\mathcal{E}})$ (cf. [2](#def:graph){reference-type="ref+label" reference="def:graph"}), the Akima Spline graph $G_A$ has the edge set ${\mathcal{E}}$ geometrically augmented by cubic polynomials. In particular, consider an edge $({\bm{q}}_{m, i}, {\bm{q}}_{m+1, j}) \in {\mathcal{E}}$ with $i, j$ are respective indices of points at layers ${\mathcal{L}}_m, {\mathcal{L}}_{m+1}$, the spline slope is defined with ${\bm{m}}_{m, i, j} = ({\bm{q}}_{m+1, j} - {\bm{q}}_{m, i}) / (t_{i+1} - t_i)$ as Modified Akima interpolation [@akima1974method] $$\begin{align}
        {\bm{s}}_{m, i, j} &= \frac{{\bm{w}}_{m, i, j} {\bm{m}}_{m-1, i, j} +  {\bm{w}}_{m-1, i, j} {\bm{m}}_{m, i, j}}{{\bm{w}}_{m, i, j} + {\bm{w}}_{m-1, i, j}} \nonumber\\ 
        {\bm{w}}_{m, i, j} &= \left|\frac{1}{N^2} \sum_{i, j} {\bm{m}}_{m+1, i, j} - {\bm{m}}_{m, i, j} \right| \\
        &+ \frac{1}{2} \left|\frac{1}{N^2} \sum_{i, j} {\bm{m}}_{m+1, i, j} + {\bm{m}}_{m, i, j} \right| \nonumber\\
        {\bm{w}}_{m-1, i, j} &= \left|{\bm{m}}_{m - 1, i, j} -  \frac{1}{N^2} \sum_{i, j} {\bm{m}}_{m - 2, i, j} \right| \nonumber\\
        &+ \frac{1}{2} \left|{\bm{m}}_{m - 1, i, j} + \frac{1}{N^2} \sum_{i, j} {\bm{m}}_{m - 2, i, j} \right| \nonumber.
\end{align}$$ Then, the augmented cubic polynomial $f_{i, j}(t),\, t \in [t_m, t_{m+1}]$ is computed following [\[eq:akima_coeff\]](#eq:akima_coeff){reference-type="ref+label" reference="eq:akima_coeff"} $$\begin{align}
 \label{eq:akima_segment}
    &{\bm{s}}_m = \frac{1}{N^2} \sum_{i, j} {\bm{s}}_{m, i, j},\,{\bm{a}}_{m, i, j} = {\bm{q}}_{m, i},\, {\bm{b}}_{m, i, j} = {\bm{s}}_m,\\
    &{\bm{c}}_{m, i, j} = (3{\bm{m}}_{m, i, j} - 2{\bm{s}}_m - {\bm{s}}_{m+1}) / (t_{m+1} - t_m), \nonumber\\
    &{\bm{d}}_{m, i, j} = ({\bm{s}}_m + {\bm{s}}_{m+1} - 2{\bm{m}}_{m, i, j}) / (t_{m+1} - t_m)^2. \nonumber
\end{align}$$*
:::

The original Akima interpolation computes equal weight to the points on both sides, evenly dividing an undulation. When two flat regions with different slopes meet, this modified Akima interpolation [@akima1974method] gives more weight to the side where the slope is closer to zero, thus giving priority to the side that is closer to horizontal, which avoids overshoot. Notice that after pre-computing ${\bm{m}}_{m, i, j}$ for every edge in $G_A$, every polynomial segment [\[eq:akima_segment\]](#eq:akima_segment){reference-type="ref+label" reference="eq:akima_segment"} can be computed in batch for $G_A$. Furthermore, given a batch of graphs $G_A$, adding a batch dimension for these equations is straightforward. The transition cost is then defined $$\begin{equation}
 \label{eq:cost_akima}
   c({\bm{q}}, {\bm{q}}') = \int_{a}^{b} \left(c_{\textrm{coll}}(f(t)) + 1 \right) \left\lVert f'(t)\right\rVert dt,
\end{equation}$$ where $f(t)$ is the cubic polynomial representing the edge $({\bm{q}}, {\bm{q}}') \in G_A$.

::: remark
**Remark 1**. *With some algebra derivations, one can verify the cubic polynomial $f_{i, j}(t),\, t \in [t_m, t_{m+1}]$ representing any edge $({\bm{q}}_{m, i}, {\bm{q}}_{m+1, j}) \in G_A$ satisfying four conditions of continuity $$\begin{align}
        &{\bm{f}}_{i,j}(t_m) = {\bm{q}}_{m, i},\,{\bm{f}}_{i,j}(t_{m+1}) = {\bm{q}}_{m+1, j}, \\
        &{\bm{f}}_{i,j}'(t_m) = {\bm{s}}_{m},\,{\bm{f}}_{i,j}'(t_{m+1}) = {\bm{s}}_{m+1}, \nonumber
\end{align}$$ for any $m \in \{0, \ldots, M+1\},\, i, j \in \{1, \ldots, N\}$. Hence, any path $f \in G_A$ is an Akima spline.*
:::

The Akima spline provides $C^1$-continuity for first-order planning; however, the second derivative is not necessarily continuous. Note that [1](#thm:prob){reference-type="ref+label" reference="thm:prob"} does not necessarily hold for Akima Spline Graph $G_A$ and is left for future work.

# Theoretical Analysis {#sec:theory}

**Notation.** Let ${\mathcal{R}}$ be the set of all paths in $G$. The path cost is the sum of straight-line integrals over the edges $c(g) = \sum_{m=0}^M c({\bm{q}}_m, {\bm{q}}_{m+1}) + c_g({\bm{g}}(1)),\, g \in {\mathcal{R}}$.

::: {#asm:uniform .assumption}
**Assumption 1**. *We assume that all associated proposal distributions at each layer are uniformly distributed on the configuration space $\forall 1 \leq m \leq M,\, p_m \;{:=}\;{\mathcal{U}}({\mathcal{C}})$.*
:::

::: {#asm:maximum .assumption}
**Assumption 2**. *Consider a feasible planning problem, there exists a feasible path $f: [0, 1] \rightarrow {\mathcal{C}}_{\textrm{free}}$ having margin $r = \inf_{t \in [0, 1]} \left\lVert{\bm{f}}(t) - {\bm{q}}\right\rVert,{\bm{q}}\in {\mathcal{C}}_{\textrm{coll}}$, such that $r > 0$.*
:::

These assumptions are common in path planning applications, where the free-path set is not zero-measure $\mu({\mathcal{F}}_{\textrm{free}}) \neq 0$.

::: {#prop:feasible .proposition}
**Proposition 2** (Feasibility Check). *For any planning problem, $v^*_{G}({\bm{q}}_0) < \infty$ if and only if there exists a feasible path in $G$.*
:::

According to Bellman optimality, $v_G^*({\bm{q}}_0) = \min_{g} \{c(g) \mid g \in {\mathcal{R}}\}$ is the minimum path cost reaching the goals. By definition, the smoothness term in [\[eq:cost\]](#eq:cost){reference-type="ref+label" reference="eq:cost"} is bounded with $\forall {\bm{q}}\in {\mathcal{C}}$, since $\textrm{TV}(g) < \infty$. Thus, any unbounded path cost $c({\mathcal{P}}) = \infty$ occurs, if and only if $\exists t,\,{\bm{f}}(t) \in {\mathcal{C}}_{\textrm{coll}}$. Hence, $v^*_{G}({\bm{q}}_0) =  \min_{{\mathcal{P}}}  \{c({\mathcal{P}}) \mid {\mathcal{P}}\in {\mathcal{R}}\} < \infty$, if and only if $\exists {\mathcal{P}}\in {\mathcal{R}},\, c({\mathcal{P}}) < \infty$. Proposition [2](#prop:feasible){reference-type="ref" reference="prop:feasible"} is useful to filter collided paths after VI.

::: {#lemma:solve .lemma}
**Lemma 1** (Solvability In Finite Path Segments). *If Assumption [2](#asm:maximum){reference-type="ref" reference="asm:maximum"} holds, there exists a minimum number of segments $M_m \in {\mathbb{N}}_{>0}$ for piecewise linear paths to be feasible.*
:::

We first show that there exists a piecewise linear path $g: [0, 1] \rightarrow {\mathcal{C}}$ such that $\left\lVert f - g\right\rVert_{\infty} < r$, where $\left\lVert f - g\right\rVert_{\infty} = \sup_{t \in [0, 1]} \left\lVert{\bm{f}}(t) - {\bm{g}}(t)\right\rVert$. We construct $g$ by dividing the interval $[0, 1]$ into $M$ subintervals with length less than $\delta > 0$, i.e., $[t_0, t_1], \ldots, [t_{M-1}, t_{M}]$ with $0 = t_0 < t_1 < \ldots < t_M = 1$. On each subinterval $[t_m, t_{m+1}]$, we define the corresponding segment of $g$ to approximate $f$ $$\begin{equation}
 \label{eq:segment}
    {\bm{g}}(t) = {\bm{f}}(t_m) + \frac{{\bm{f}}(t_{m+1}) - {\bm{f}}(t_m)}{t_{m+1} - t_m} (t - t_m),\, t \in [t_m, t_{m+1}].
\end{equation}$$ Since by definition the path $f$ is continuous on a compact interval $[0, 1]$, then by Heine-Cantor theorem, $f$ is also uniformly continuous, i.e., $\exists \delta > 0$ for any $a, b \in [0, 1]$, $|a - b| < \delta$, then $\left\lVert{\bm{f}}(a) - {\bm{f}}(b)\right\rVert_{\infty} < r$. Then, by the construction of $g$ and uniform continuity of $f$, we can choose a $\delta$ sufficiently small such that $\left\lVert f - g\right\rVert_{\infty} < r$. This implies that there exists a sufficiently large number of segments $M_m$ such that $\delta$ is sufficiently small, hence, $g$ is a feasible path.

Lemma [1](#lemma:solve){reference-type="ref" reference="lemma:solve"} implies that any path planning algorithm producing a piecewise linear feasible path, then it must have a minimum number of segments.

::: {#lemma:path_bound .lemma}
**Lemma 2**. *Let piecewise linear path $g: [0, 1] \rightarrow {\mathcal{C}}$ having $n$ equal subintervals approximating a path $f: [0, 1] \rightarrow {\mathcal{C}}$. The error lowerbound is $\left\lVert f - g\right\rVert_{\infty} > L / n$, where $L = \textrm{TV}(f)$ is the total variation of $f$.*
:::

Denoting the subinterval length $u = 1 / n$ and reusing the notations from [1](#lemma:solve){reference-type="ref+label" reference="lemma:solve"} proof, we define $g$ as a piecewise linear function [\[eq:segment\]](#eq:segment){reference-type="ref" reference="eq:segment"}. Since $f,g$ are uniformly continuous, the linear interpolation error lower bound can be expressed using the modulus of continuity on a segment $t \in [t_m, t_{m+1}]$ $$\begin{equation}
        \left\lVert{\bm{f}}(t) - {\bm{g}}(t)\right\rVert > \omega_f (u),\, \omega_f (u) = \sup_{|a - b| \leq u} \left\lVert{\bm{f}}(a) - {\bm{f}}(b)\right\rVert. \nonumber
\end{equation}$$ And, the global error over all segments is $$\begin{equation}
        \left\lVert{\bm{f}}(t) - {\bm{g}}(t)\right\rVert_{\infty} = \max_{0 \leq m \leq n-1} \sup_{t \in [t_m, t_{m+1}]} \left\lVert{\bm{f}}(t) - {\bm{g}}(t)\right\rVert \nonumber
\end{equation}$$ By definition, $f$ is uniformly continuous and of bounded variation, the modulus of continuity $\omega_f(u)$ provides a lower bound for the error on each segment. Therefore, $\left\lVert f - g\right\rVert_{\infty} > \omega_f (1 / n)$ on $[0, 1]$. For functions of bounded variation, the modulus of continuity can be bounded in terms of the total variation $\omega_f (1 / n) > L / n$ on $[0, 1]$. Hence, $\left\lVert f - g\right\rVert_{\infty} > L / n$.

::: {#lemma:path .lemma}
**Lemma 3**. *Let $g_1, g_2$ be a piecewise linear function having the same number of partition points $\{{\bm{g}}_1(t_m)\}_{m=0}^M,\{{\bm{g}}_2(t_m)\}_{m=0}^M$ with $0 = t_0 < \ldots, t_M = 1$, $\left\lVert g_1 - g_2\right\rVert_{\infty} < \delta$, if and only if $\left\lVert{\bm{g}}_1(t_m) - {\bm{g}}_2(t_m)\right\rVert < \delta,\, 0 \leq m \leq M$.*
:::

**Sufficiency.** Given $\left\lVert{\bm{g}}_1(t_m) - {\bm{g}}_2(t_m)\right\rVert < \delta,\,\forall 1 \leq m \leq M$, since $g_1, g_2$ are piecewise linear functions, the linear interpolation between partition points $t_m,t_{m+1}$ ensures that the difference between $g_1,g_2$ is maximized at the partition points. Consider $g_1,g_2$ on a segment $[t_m, t_{m+1}]$ $$\begin{align}
    \begin{split}
        \left\lVert{\bm{g}}_1(t) - {\bm{g}}_2(t)\right\rVert \leq &\max \{ \left\lVert{\bm{g}}_1(t_m) - {\bm{g}}_2(t_m)\right\rVert, \\
        &\left\lVert{\bm{g}}_1(t_{m+1}) - {\bm{g}}_2(t_{m+1})\right\rVert \} < \delta
    \end{split}
\end{align}$$ Hence, $\left\lVert g_1 - g_2\right\rVert_{\infty} = \max_{t \in [0, 1]} \left\lVert{\bm{g}}_1(t) - {\bm{g}}_2(t)\right\rVert < \delta$.

**Necessity.** Given $\left\lVert g_1 - g_2\right\rVert_{\infty} < \delta$, then $\left\lVert{\bm{g}}_1(t_m) - {\bm{g}}_2(t_m)\right\rVert < \delta,\, 0 \leq m \leq M$.

::: {#thm:prob .theorem}
**Theorem 1** (Probabilistic Completeness).

*If Assumption [1](#asm:uniform){reference-type="ref" reference="asm:uniform"} and Assumption [2](#asm:maximum){reference-type="ref" reference="asm:maximum"} hold, for a feasible planning problem $({\mathcal{C}}_{\textrm{free}}, {\bm{q}}_0, {\mathcal{G}})$, with $G$ having $M \geq M_m$ layers, there exist constants $a, R, L > 0$ depending only on ${\mathcal{C}}_{\textrm{free}}$ and ${\mathcal{G}}$, such that $$\begin{equation}
\label{eq:probc}
    {\mathbb{P}}\left( v_G^*({\bm{q}}_0) < \infty \right) > 1 - M\exp \left(- a\left(R - \frac{L}{M+1} \right)^d N \right).
\end{equation}$$*
:::

From Lemma [1](#lemma:solve){reference-type="ref" reference="lemma:solve"}, if $M \geq M_m$, there exists a feasible piecewise linear path $g$ having $M + 1$ segments with $0 = t_0 < \ldots < t_{M + 1} = 1$ approximating a feasible path $f$. Let $R = \inf_{t \in [0, 1]} \left\{ \left\lVert{\bm{f}}(t) - {\bm{q}}\right\rVert,{\bm{q}}\in {\mathcal{C}}_{\textrm{coll}} 
 \right\}, r = \inf_{t \in [0, 1]} \left\{ \left\lVert{\bm{g}}(t) - {\bm{q}}\right\rVert,{\bm{q}}\in {\mathcal{C}}_{\textrm{coll}} \right\}$ be collision margins of $f,g$, ${\mathcal{B}}_{\delta}({\bm{q}}) = \{ \left\lVert{\bm{q}}' - {\bm{q}}\right\rVert < \delta,\, \delta > 0\}$ is an open $\delta$-ball around ${\bm{q}}$. Now, let $g$ have equal subinterval.

First, we compute the probability of the event that a sampled graph $G$ has at least a piecewise linear path $h$ with $M+1$ segments such that $h$ is approximating $g$. $h$ is feasible when $\left\lVert h - g\right\rVert_{\infty} < r$. We have $$\begin{align}
    \begin{split}
    r &= \inf_{t \in [0, 1]} \left\{ \left\lVert{\bm{g}}(t) - {\bm{q}}\right\rVert,{\bm{q}}\in {\mathcal{C}}_{\textrm{coll}} \right\} \\
    &\leq \inf_{t \in [0, 1]} \left\{ \left\lVert{\bm{f}}(t) - {\bm{q}}\right\rVert,{\bm{q}}\in {\mathcal{C}}_{\textrm{coll}} \right\} + \inf_{t \in [0, 1]} \left\lVert{\bm{g}}(t) - {\bm{f}}(t)\right\rVert \\
    &= \inf_{t \in [0, 1]} \left\{ \left\lVert{\bm{f}}(t) - {\bm{q}}\right\rVert,{\bm{q}}\in {\mathcal{C}}_{\textrm{coll}} \right\} - \sup_{t \in [0, 1]} \left\lVert{\bm{g}}(t) - {\bm{f}}(t)\right\rVert \\
    &< R - \frac{L}{M + 1},
    \end{split}
    \nonumber
\end{align}$$ where the first inequality due to ${\mathcal{C}}\subset {\mathbb{R}}^d$, and last inequality from Lemma [2](#lemma:path_bound){reference-type="ref" reference="lemma:path_bound"} and $L = \textrm{TV}(f)$.

From Lemma [3](#lemma:path){reference-type="ref" reference="lemma:path"}, since by definition $h, g$ has the same number of segments, the event $\left\lVert h - g\right\rVert_{\infty} < r < r_h = R - \frac{L}{M + 1}$ is the event that, given start and goals fixed, for each layer $1 \leq m \leq M$, there is at least one point ${\bm{h}}(t_m)$ is sampled inside the ball ${\mathcal{B}}_{r_h}({\bm{g}}(t_m))$. Then, by sampling $N$ points uniformly over ${\mathcal{C}}$ per layer (Assumption [1](#asm:uniform){reference-type="ref" reference="asm:uniform"}), and the fact that there are pairwise connections between layers, we have the failing probability $$\begin{align}
    \begin{split}
    {\mathbb{P}}(\left\lVert h - g\right\rVert_{\infty} \geq r_h) &\leq \sum_{m=1}^M \left(1 - \frac{\mu({\mathcal{B}}_{r_h}({\bm{g}}(t_m))))}{\mu({\mathcal{C}})} \right)^N \\
    &\leq M\exp \left(- \frac{\alpha_d }{\mu({\mathcal{C}})} \left(R - \frac{L}{M+1} \right)^d N \right)
    \end{split}\nonumber
\end{align}$$ where we use the inequality $1 - x \leq e^{-x},\,x \geq 0$, and $a = \alpha_d / \mu({\mathcal{C}})$, where $\alpha_d$ is the constant term computing volume of a $d$-ball.

The event of $h$ approximating $g$ having equal intervals is a subset of the event of $h$ approximating $g$ having arbitrary intervals. The event that at least a path $h$ in $G$ having $\left\lVert h - g\right\rVert_{\infty} < r_h$ is a subset of the event $\exists \textrm{a feasible path in } G$, since there might exist multiple feasible paths and their corresponding piecewise linear approximations have $M+1$ segments. From Proposition [2](#prop:feasible){reference-type="ref" reference="prop:feasible"}, $v^*_G({\bm{q}}_0) < \infty$ is equivalent to $\exists \textrm{ a feasible path in }G$. We have $$\begin{align}
\begin{split}
    {\mathbb{P}}(v_G^*({\bm{q}}_0) < \infty) &\geq {\mathbb{P}}(\left\lVert h - g\right\rVert_{\infty} < r_h) \\
    &> 1 - M\exp \left(- a\left(R - \frac{L}{M+1} \right)^d N \right).
\end{split} \nonumber
\end{align}$$ The lower bound is intuitive since it directly implies a minimum number of layers $M > [L / R] - 1$ (cf. Lemma [1](#lemma:solve){reference-type="ref" reference="lemma:solve"}) for the exponent coefficient to be strictly positive. It also implies the existence of an optimal number $M^*$; increasing $M$ helps then harms $N$ sample efficiency, depending on the planning problem (cf. Fig. [4](#fig:sweep_exp){reference-type="ref" reference="fig:sweep_exp"}).

# ACKNOWLEDGMENT {#acknowledgment .unnumbered}

An T. Le was funded by the German Research Foundation project METRIC4IMITATION (PE 2315/11-1). Kay Pompetzki received funding from the German Research Foundation project CHIRON (PE 2315/8-1).

[^1]: Manuscript received: 31.12.2024; Revised 10.04.2025; Accepted 20.05.2025.

[^2]: This paper was recommended for publication by Editor Júlia Borràs Sol upon evaluation and Reviewers' comments.

[^3]: Corresponding author: An T. Le, [an@robot-learning.de](an@robot-learning.de)

[^4]: $^{1}$Intelligent Autonomous Systems Lab, TU Darmstadt, Germany; $^{2}$German Research Center for AI (DFKI); $^{3}$Hessian.AI; $^{4}$Centre for Cognitive Science. $^{5}$Interactive Robot Perception & Learning Lab, TU Darmstadt, Germany

[^5]: Digital Object Identifier (DOI): 10.1109/LRA.2025.3575307

[^6]: We use default *shortcut* simplification for OMPL planners while using default *shortcut and B-spline smoothing* for VAMP/RRTC.
