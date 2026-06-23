---
citation_key: Xie2026GNNDIP
arxiv_id: 2603.12361
arxiv_url: https://arxiv.org/abs/2603.12361
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:52:01Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Motion planning in cluttered environments is a fundamental problem in robotics. Among its open challenges, narrow passages stand out as both the hardest to solve and the most valuable to exploit: in environments with tight doorways, narrow gaps between obstacles, or double enclosures, the only feasible routes pass through regions that occupy a vanishingly small fraction of the configuration space, making their reliable discovery essential for any practical planner.

Sampling-based planners, including RRT\* [@karaman2011sampling], BIT\* [@gammell2015batch], InformedRRT\* (iRRT\*) [@gammell2014informed], and their variants, provide asymptotic optimality guarantees but face a dual challenge in narrow passages. First, the probability of randomly sampling inside a passage of width $\varepsilon$ scales as $\varepsilon^d$, so narrow gaps become exponentially harder to discover in higher dimensions. Second, even when a sample lands inside a narrow passage, the straight-line segments connecting it to neighboring samples run close to obstacle boundaries, complicating collision checking at finite resolution. These two challenges compound in environments with narrow gaps and double enclosures, where increasing sampling density or collision-checking resolution provides diminishing returns.

Decomposition-based planners address both challenges structurally. By partitioning the free space $\mathcal{F}$ into convex cells and constructing a cell adjacency graph, every passage---no matter how narrow---is represented exactly as a cell boundary (portal), so no bottleneck region is missed. Moreover, any path within a convex cell is collision-free by definition, eliminating resolution-dependent collision checking entirely. The continuous planning problem thus reduces to a discrete corridor search followed by local path optimization within each corridor. In 2D, exact shortest paths within a corridor of convex polygons can be computed in linear time using the Funnel algorithm [@lee1984euclidean].

The principal limitation of decomposition-based approaches is the corridor selection problem: the number of distinct corridors from start to goal grows combinatorially with the number of cells. In environments with hundreds to thousands of cells, the $k$-shortest path search via Yen's algorithm [@yen1971finding] must be guided by accurate edge weights. The default centroid-distance heuristic $w(c_i, c_j) = \|z_i - z_j\|$ correlates poorly with actual path cost in environments with elongated cells, narrow passages, or asymmetric obstacle configurations.

Our approach. We address the corridor selection problem by training a GNN on the cell adjacency graph to predict portal-level scores. Each portal $p_{ij}$ (the shared boundary between adjacent cells $c_i$ and $c_j$) receives a score $s_{ij} \in [0,1]$ indicating the probability that it lies on a near-optimal corridor. These scores modulate edge weights via $w(c_i, c_j) = d(c_i, c_j) \cdot \exp(-\beta \cdot s_{ij})$, concentrating the $k$-shortest path search on promising regions. Importantly, the modulation is continuous---no corridors are pruned---thereby preserving completeness while improving the quality of initial corridor candidates.

Fig. [1](#fig:pipeline){reference-type="ref" reference="fig:pipeline"} illustrates the GNN-DIP ($\mathcal{G}$-DIP) pipeline on a labyrinth environment with 50 polygon obstacles of varying shapes. CDT produces 385 triangular cells (panel b), creating a combinatorial corridor search space that grows exponentially with cell count. The GNN identifies a narrow corridor of 73 cells (panel c, light blue) containing the near-optimal path, reducing the effective search space by ${\sim}81\%$. Parallel corridor evaluation via the Funnel algorithm then yields the initial solution in under 20 ms. Phase 2 refines the solution within a shrinking informed ellipsoid (panel d).

:::: {#fig:pipeline .figure latex-placement="t"}
![](Xie2026GNNDIP_figs/pipeline_figure.png){width="95%"}

::: caption
GNN-DIP pipeline on a labyrinth with polygon obstacles. (a) Planning problem with start ($\star$) and goal ($\circ$). (b) CDT decomposes the free space into 385 triangular cells. (c) The GNN selects a corridor of 73 cells (light blue), and the Funnel algorithm computes the initial path (green) in parallel across corridor candidates. (d) Phase 2 refines the solution within a shrinking informed ellipsoid (orange dashed $\to$ red solid).
:::
::::

The contributions of this paper are:

1.  A GNN-based portal scoring framework on cell adjacency graphs, with feature engineering for node/edge representations and a training pipeline using focal loss, multi-label generation, and stratified train-validation splitting (Section [3](#sec:gnn){reference-type="ref" reference="sec:gnn"}).

2.  A two-phase Decomposition-Informed Planner (DIP) combining GNN-guided corridor search, informed ellipsoid pruning, and Funnel-based corridor evaluation, with proofs of completeness and convergence (Section [4](#sec:dip){reference-type="ref" reference="sec:dip"}).

3.  Comprehensive experiments spanning 2D (310 maps, 18 scenarios), 3D bottleneck environments (4 scenarios, 50 PDT runs each), and dynamic 2D environments (100 planning instances), demonstrating 2--280$\times$ speedup, 99--100% success rates, and collision safety by construction (Section [5](#sec:experiments){reference-type="ref" reference="sec:experiments"}).

# Preliminaries and Related Work {#sec:related_work}

## Decomposition-Based Motion Planning

Cell decomposition methods partition the free space into simple regions and plan over the resulting adjacency graph. Exact cell decomposition [@latombe1991robot] constructs cells whose union equals the free space, whereas approximate methods employ regular grids or adaptive subdivisions. Constrained Delaunay Triangulation (CDT) [@shewchuk1996triangle] with parity-based face classification provides a well-studied 2D decomposition with robust implementations in CGAL [@cgal2024]. The Funnel algorithm [@lee1984euclidean] computes the exact Euclidean shortest path through a sequence of adjacent convex polygons in $O(n)$ time, where $n$ is the total number of portal endpoints.

In 3D, exact convex decomposition of general polyhedral free space is computationally expensive. For environments with axis-aligned box (AABB) obstacles, a Slab decomposition exploits obstacle face alignment to produce an exact convex decomposition in near-linear time. Strub and Gammell [@strub2020pdt] introduced AIT\* and EIT\*, which integrate lazy search and informed sampling. The Planner Developer Tools (PDT) framework provides standardized benchmarking infrastructure for OMPL-compatible planners [@sucan2012ompl].

## Learning and GNNs for Motion Planning

Neural approaches to motion planning include learned samplers [@ichter2018learning; @wang2020neural], conditional generative models [@ichter2020learned], and reinforcement learning [@chen2020learning], all operating in continuous configuration space without exploiting cell decomposition structure. GNNs have been applied to roadmap graphs for collision prediction [@yu2021reducing], neural planning [@qureshi2021nerp], and edge cost learning [@zang2023graphmp]. These operate on roadmap graphs (nodes = configurations, edges = local paths), whereas our GNN operates on the cell adjacency graph (nodes = free-space cells, edges = portals)---a fundamentally different and more compact representation. Informed approaches exploit ellipsoidal [@gammell2014informed] or zonotope [@xie2025informed] subsets; our GNN guidance is complementary, biasing corridor search before any solution is found.

## Problem Formulation {#sec:preliminaries}

This section formalizes the key components of the proposed framework. Throughout, $\mathcal{W} \subseteq \mathbb{R}^d$ ($d \in \{2,3\}$) denotes the workspace.

::: {#def:mpp .definition}
**Definition 1** (Motion Planning Problem). *Given a workspace $\mathcal{W}$ with obstacles $\mathcal{O} = \{O_1, \ldots, O_m\}$ (arbitrary simple polygons in 2D, axis-aligned boxes in 3D), the free space is $\mathcal{F} = \mathcal{W} \setminus \bigcup_{i=1}^{m} O_i$. Given start and goal configurations $q_s, q_g \in \mathcal{F}$, the *optimal motion planning problem* seeks a continuous path $\sigma^* : [0,1] \to \mathcal{F}$ with $\sigma(0) = q_s$, $\sigma(1) = q_g$, minimizing the path length $\ell(\sigma) = \int_0^1 \|\dot{\sigma}(t)\| \, dt$: $$\begin{equation}
\sigma^* = \arg\min_{\sigma} \; \ell(\sigma).
\end{equation}$$*
:::

::: {#def:decomp .definition}
**Definition 2** (Free-Space Decomposition). *A *free-space decomposition* of $\mathcal{F}$ is a finite collection of closed convex cells $\mathcal{C} = \{c_1, \ldots, c_n\}$ such that:*

1.  *$\bigcup_{i=1}^{n} c_i = \overline{\mathcal{F}}$ (coverage),*

2.  *$\mathrm{int}(c_i) \cap \mathrm{int}(c_j) = \emptyset$ for $i \neq j$ (non-overlapping interiors),*

3.  *Each $c_i$ is convex.*

*In 2D, we use Constrained Delaunay Triangulation (CDT) with obstacle edges as constraints and parity-based classification to identify free faces. In 3D with axis-aligned box obstacles, we employ a *Slab convex decomposition*: obstacle face coordinates define axis-aligned splitting planes; obstacle cells are removed and adjacent free cells are greedily merged, producing a compact set of convex boxes.*
:::

::: {#def:cag .definition}
**Definition 3** (Cell Adjacency Graph). *The *cell adjacency graph* $G = (\mathcal{C}, \mathcal{P})$ is defined over the free-space cells of Definition [2](#def:decomp){reference-type="ref" reference="def:decomp"}, with cells as nodes and portals as edges. A *portal* $p_{ij} \in \mathcal{P}$ exists between cells $c_i$ and $c_j$ if they share a $(d{-}1)$-dimensional face (an edge segment in 2D, a rectangular face in 3D). Each portal $p_{ij}$ is characterized by its geometric attributes: endpoints $\{a_{ij}, b_{ij}\}$ and midpoint $m_{ij}$, with size measure $\lambda_{ij}$ defined as the segment length $\|a_{ij} - b_{ij}\|$ in 2D or the face area in 3D.*
:::

::: {#def:corridor .definition}
**Definition 4** (Corridor). *A *corridor* $\pi = (c_{i_1}, c_{i_2}, \ldots, c_{i_L})$ is a path in $G$ from the cell containing $q_s$ to the cell containing $q_g$. The corridor defines a connected region $\mathcal{R}_\pi = \bigcup_{\ell=1}^{L} c_{i_\ell}$ through which a collision-free path must pass. The *corridor cost* $\ell(\pi)$ is the length of the shortest path in $\mathcal{F}$ that traverses the cells of $\pi$ in order.*
:::

# GNN Portal Scoring {#sec:gnn}

The corridor selection problem can be formulated as an edge classification task on the cell adjacency graph: for each portal $p_{ij}$, predict whether it lies on a near-optimal corridor. A GNN is trained to solve this classification problem, and the predicted scores are used to bias edge weights in the corridor search.

## Graph Representation and Feature Engineering {#sec:features}

The cell adjacency graph $G = (\mathcal{C}, \mathcal{P})$ is represented as a directed graph with bidirectional edges (each portal appears as two directed edges). Each cell $c_i$ is associated with a node feature vector $\mathbf{x}_i \in \mathbb{R}^{d_n}$, and each portal $p_{ij}$ with an edge feature vector $\mathbf{e}_{ij} \in \mathbb{R}^{d_e}$.

### Node Features ($d_n = 11$ in 2D) and Edge Features ($d_e = 9$ in 2D)

Table [1](#tab:features){reference-type="ref" reference="tab:features"} lists the complete 2D feature set. Node features encode cell geometry (area, aspect ratio $\rho_i = e_{\max}/e_{\min}$), spatial relationships to the query (distances to start, goal, and the start--goal line $d_\perp$), and role indicators. Edge features encode portal geometry, spatial context, and inter-cell relationships. The relative angle $\theta_{ij} = \angle(p_{ij}) - \angle(\overrightarrow{q_s q_g})$ captures alignment between the portal and the global query direction. For the 3D Slab decomposition, features are extended to $d_n{=}14$ and $d_e{=}13$ by adding volumetric cell descriptors (volume, size along each axis, clearance) and 3D portal attributes (face area, portal height, normal axis).

::: {#tab:features}
+---------------------------------------------------------+------------------------------------------------------------+
| **Node features** ($d_n = 11$)                          | **Edge features** ($d_e = 9$)                              |
+:==================================:+:==================:+:=====================================:+:==================:+
| $A_i$                              | Cell area          | $\lambda_{ij}$                        | Portal length      |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $z_i^x, z_i^y$                     | Centroid coords    | $m_{ij}^x, m_{ij}^y$                  | Midpoint coords    |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $d(z_i, q_s)$                      | Dist. to start     | $d(m_{ij}, q_s)$                      | Dist. to start     |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $d(z_i, q_g)$                      | Dist. to goal      | $d(m_{ij}, q_g)$                      | Dist. to goal      |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $d_\perp(z_i, \overline{q_s q_g})$ | Dist. to $sg$-line | $d_\perp(m_{ij}, \overline{q_s q_g})$ | Dist. to $sg$-line |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $\rho_i$                           | Aspect ratio       | $\theta_{ij}$                         | Relative angle     |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $\mathbb{1}[i{=}i_s]$              | Start cell flag    | $\|z_i - z_j\|$                       | Cell--cell dist.   |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $\mathbb{1}[i{=}i_g]$              | Goal cell flag     | $\kappa_{ij}$                         | Portal clearance   |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $|\mathcal{N}(i)|$                 | Neighbor count     |                                       |                    |
+------------------------------------+--------------------+---------------------------------------+--------------------+
| $\kappa_i$                         | Obstacle clearance |                                       |                    |
+------------------------------------+--------------------+---------------------------------------+--------------------+

: GNN input features: node (cell) and edge (portal).
:::

## GNN Architecture {#sec:architecture}

The architecture follows an encode--process--decode pattern. Raw node features are projected to hidden dimension $h=128$ via a linear layer with batch normalization (BN) and ReLU. In 2D, three GCN layers [@kipf2017semi] with symmetric normalization, BN, and dropout ($p{=}0.15$) process the node embeddings; layers 2--3 use two-layer-skip residual connections. For 3D, GCN is replaced by GATv2 (3 layers, 4 attention heads) to better capture the irregular connectivity of Slab cells; the remaining architecture is identical.

For each portal $p_{ij}$, the score is predicted by an MLP ($\mathbb{R}^{2h+d_e} \to h \to 32 \to 1$, ReLU activations) on the concatenation of endpoint embeddings and edge features: $$\begin{equation}
\hat{s}_{ij} = \mathrm{sigm}\!\left(\text{MLP}\!\left([\mathbf{h}_i^{(3)} \| \mathbf{h}_j^{(3)} \| \text{BN}_e(\mathbf{e}_{ij})]\right)\right),
\label{eq:edge_score}
\end{equation}$$ where $\mathrm{sigm}(\cdot) = 1/(1+e^{-x})$ is the sigmoid function (distinguished from path $\sigma$).

## Training {#sec:training}

### Label Generation

Training labels are generated from OMPL baseline planners (iRRT\*, AIT\*, BIT\*, RRT\*) run on each map with a sufficient time budget. All solution paths are collected and portals on near-optimal corridors are identified. Let $\sigma_\text{ref}$ denote the shortest path found across all baseline runs: $$\begin{equation}
y_{ij} = \begin{cases} 1 & \exists\, \sigma : \ell(\sigma) \leq (1{+}\epsilon)\,\ell(\sigma_\text{ref}),\; p_{ij} \in \sigma \\ 0 & \text{otherwise} \end{cases}
\end{equation}$$ where $\epsilon = 0.1$ (10% suboptimality threshold). Since $\sigma_\text{ref}$ is the best solution found rather than the true optimum $\sigma^*$, label noise may arise when baselines have not converged; in practice, running four planners with a 10 s budget per map yields near-optimal references. This multi-label scheme assigns positive labels to portals on any near-optimal corridor, capturing the multiplicity of good solutions. The resulting label distribution is severely imbalanced: typically less than 5% of portals are positive.

### Focal Loss

To address the extreme class imbalance, focal loss [@lin2017focal] is adopted: $$\begin{equation}
\mathcal{L}_\text{FL}(\hat{s}, y) = -\alpha_t (1 - p_t)^\gamma \log(p_t),
\label{eq:focal}
\end{equation}$$ where $p_t = \hat{s} \cdot y + (1 - \hat{s})(1 - y)$ is the model's estimated probability for the true class, $\alpha_t = \alpha y + (1-\alpha)(1-y)$ balances positive/negative contributions, and $\gamma$ is the focusing parameter. We use $\alpha = 0.85$ and $\gamma = 2.0$. The $(1-p_t)^\gamma$ factor down-weights well-classified negatives, focusing gradient updates on hard positives---the critical portals that the model initially misclassifies.

### Optimization

Training employs Adam [@kingma2015adam] (initial learning rate $10^{-3}$, weight decay $10^{-4}$) with cosine annealing and early stopping based on validation F1 score (patience 30 epochs). Data are split using stratified sampling (20% validation ratio). The model contains approximately 150K parameters with hidden dimension $h = 128$ and trains in under 5 minutes on a single GPU.

# Decomposition-Informed Planner {#sec:dip}

The Decomposition-Informed Planner (DIP) operates in two phases on the cell adjacency graph $G$. Phase 1 performs GNN-guided $k$-shortest corridor search with corridor evaluation; Phase 2 refines the search using an informed ellipsoid derived from the current best solution.

## GNN-Guided Edge Weight Integration

Given GNN-predicted portal scores $\{\hat{s}_{ij}\}$, we define modified edge weights: $$\begin{equation}
w_\text{GNN}(c_i, c_j) = d(c_i, c_j) \cdot \exp(-\beta \cdot \hat{s}_{ij}),
\label{eq:gnn_weight}
\end{equation}$$ where $d(c_i, c_j) = \|z_i - z_j\|$ is the centroid distance and $\beta > 0$ is a temperature parameter (we use $\beta = 3.0$).

::: {#prop:weights .proposition}
**Proposition 1** (Properties of GNN Edge Weights). *The weight [\[eq:gnn_weight\]](#eq:gnn_weight){reference-type="eqref" reference="eq:gnn_weight"} is strictly positive and continuous; it recovers the centroid-distance baseline when $\hat{s}_{ij} = 0$ (graceful degradation); and higher scores yield lower weights, concentrating the $k$-shortest search on predicted near-optimal portals.*
:::

## Phase 1: $k$-Shortest Corridor Search

Phase 1 applies Yen's algorithm [@yen1971finding] to find $k$ shortest paths in $G$ from the start cell $c_s$ to the goal cell $c_g$, using edge weights $w_\text{GNN}$ when available and centroid distances $d(\cdot, \cdot)$ otherwise. Each corridor is evaluated using the Funnel algorithm (2D) or portal-face sampling with layered-graph DP (3D).

The best solution from Phase 1 provides an initial cost bound $c_\text{best}^{(1)}$ that seeds the refinement in Phase 2.

## Phase 2: Informed Ellipsoid Corridor Refinement

::: {#def:ellipsoid .definition}
**Definition 5** (Informed Ellipsoid). *Given the current best cost $c_\text{best}$, the *informed ellipsoid* is: $$\begin{equation}
\mathcal{E}(c_\text{best}) = \{x \in \mathbb{R}^d : \|x - q_s\| + \|x - q_g\| \leq c_\text{best}\}.
\end{equation}$$ A portal $p_{ij}$ is *informative* if it intersects the ellipsoid, i.e., $p_{ij} \cap \mathcal{E}(c_\text{best}) \neq \emptyset$, or equivalently $\min_{x \in p_{ij}} (\|x - q_s\| + \|x - q_g\|) \leq c_\text{best}$.*
:::

Phase 2 iteratively re-runs the $k$-shortest path search on $G$, restricted to portals inside $\mathcal{E}(c_\text{best})$. Only corridors not yet contained in the evaluated set $\mathcal{S}$ are passed to the corridor evaluator (Funnel in 2D, portal-face sampling in 3D). When a better corridor is found, the ellipsoid shrinks accordingly; otherwise, the corridor budget $k'$ is doubled up to $4k$, after which the loop terminates.

:::: algorithm
::: algorithmic
**Input:**$\mathcal{W}$, $q_s$, $q_g$, GNN model $f_\theta$, corridor budget $k$, timeout $T$

**Output:**Best path $\sigma^*$ and cost $c^*$ Decompose $\mathcal{F}$ into cells; build $G = (\mathcal{C}, \mathcal{P})$ $\{\hat{s}_{ij}\} \leftarrow f_\theta(G)$ $w_{ij} \leftarrow d(c_i, c_j) \cdot \exp(-\beta \cdot \hat{s}_{ij})$,  $\forall\, (c_i, c_j) \in \mathcal{P}$ $c^* \leftarrow \infty$;  $\mathcal{S} \leftarrow \emptyset$ $\Pi_k \leftarrow \text{Yen}(G, c_s, c_g, k, w)$ $(\ell_\pi, \sigma_\pi) \leftarrow \text{Eval}(\pi, q_s, q_g)$;  $\mathcal{S} \leftarrow \mathcal{S} \cup \{\pi\}$ $c^* \leftarrow \ell_\pi$;  $\sigma^* \leftarrow \sigma_\pi$

$k' \leftarrow k$ $\mathcal{P}' \leftarrow \{p_{ij} \in \mathcal{P} : \min_{x \in p_{ij}} (\|x - q_s\| + \|x - q_g\|) \leq c^*\}$ $\Pi' \leftarrow \text{Yen}(G|_{\mathcal{P}'}, c_s, c_g, k', w)$ $\text{improved} \leftarrow \text{false}$ $(\ell_\pi, \sigma_\pi) \leftarrow \text{Eval}(\pi, q_s, q_g)$;  $\mathcal{S} \leftarrow \mathcal{S} \cup \{\pi\}$ $c^* \leftarrow \ell_\pi$;  $\sigma^* \leftarrow \sigma_\pi$;  $\text{improved} \leftarrow \text{true}$ $k' \leftarrow \min(2k', 4k)$ **break** $(\sigma^*, c^*)$
:::
::::

## Theoretical Properties

::: {#thm:complete .theorem}
**Theorem 1** (Completeness of DIP). *If a collision-free path from $q_s$ to $q_g$ exists in $\mathcal{F}$, and the decomposition $\mathcal{C}$ covers $\mathcal{F}$ with $q_s, q_g$ contained in cells of $G$, then DIP (Algorithm [\[alg:dip\]](#alg:dip){reference-type="ref" reference="alg:dip"}) finds a solution path.*
:::

::: proof
*Proof sketch.* GNN weights [\[eq:gnn_weight\]](#eq:gnn_weight){reference-type="eqref" reference="eq:gnn_weight"} preserve graph topology (all edges remain with positive weights), so Yen's algorithm can discover any reachable corridor. For Phase 2, any portal on an optimal corridor satisfies the ellipsoid condition by the triangle inequality, so it is never pruned. ◻
:::

::: {#thm:converge .theorem}
**Theorem 2** (Convergence of DIP). *The Phase 2 loop of Algorithm [\[alg:dip\]](#alg:dip){reference-type="ref" reference="alg:dip"} terminates in finite iterations. Moreover, each iteration either discovers a strictly better corridor (decreasing $c^*$) or explores no new corridors.*
:::

::: proof
*Proof sketch.* The number of distinct corridors is finite; each is evaluated at most once. Each iteration either discovers a new corridor or triggers termination, so the loop terminates. ◻
:::

## Corridor Evaluation {#sec:funnel}

In 2D, the Funnel algorithm [@lee1984euclidean] computes the exact shortest path through a corridor of $L$ convex polygons in $O(L)$ time via string-pulling. In 3D, we employ portal-face sampling: $N_s$ points are sampled uniformly on each portal face, forming a layered DAG from $q_s$ through portal samples to $q_g$. A forward DP sweep finds the shortest path in $O(L \cdot N_s^2)$ time---collision-free by convexity. Adaptive Gaussian re-sampling refines the path for up to $r=3$ iterations.

## Complexity and System Design {#sec:system}

Decomposition is $O(n \log n)$ (CDT in 2D) or $O(N_x N_y N_z + M)$ (Slab in 3D). Phase 1 runs Yen's $k$-shortest paths [@yen1971finding] in $O(k \cdot |\mathcal{C}| \cdot (|\mathcal{P}| + |\mathcal{C}| \log |\mathcal{C}|))$; each Funnel evaluation is $O(L)$. Phase 2 operates on progressively smaller ellipsoid-filtered subgraphs. GNN inference is $O(L_\text{GNN} \cdot (|\mathcal{P}| \cdot h + |\mathcal{C}| \cdot h^2))$ with $L_\text{GNN}=3$, $h=128$.

The system comprises a C++ planning core ($\sim$`<!-- -->`{=html}5K LOC, OMPL-integrated [@sucan2012ompl]) and a Python GNN module (PyTorch [@paszke2019pytorch] + PyG [@fey2019fast], $\sim$`<!-- -->`{=html}150K parameters). GNN inference adds 10--50 ms latency. Default corridor budget: $k=8$ in 2D, $k=16$ ($\mathcal{G}$-DIP) or $k=32$ (unguided DIP) in 3D; 3D portal-face sampling uses $N_s=16$, refinement iterations $r=3$.

# Experiments {#sec:experiments}

GNN-DIP is evaluated against unguided DIP and OMPL baselines (best result among iRRT\*, AIT\*, BIT\*, EIT\*, RRT\*) in both 2D and 3D environments. All experiments are executed on a single thread of an Intel i7 processor.

## 2D Evaluation

The 2D benchmark uses 310 polygon maps across 18 scenarios in four complexity tiers by CDT cell count: simple (14--74), medium (80--164), hard (280--672), and very hard (764--2372 cells). DIP uses $k=8$ with Funnel evaluation. DIP achieves an 89.5% win rate against OMPL at 10 ms on simple--hard maps but only 33% on very hard maps (1000+ cells) due to combinatorial corridor explosion. GNN guidance addresses this: on mega forest (1074 cells), unguided DIP fails while GNN-DIP succeeds with cost 1.295 (vs. 1.293 for OMPL); on tight labyrinth (1046 cells), both DIP methods achieve cost 1.737, outperforming OMPL's 1.799.

#### Decomposition Guarantees Full Reliability on 2D Narrow Passages

Table [\[tab:benchmark\]](#tab:benchmark){reference-type="ref" reference="tab:benchmark"} reports PDT [@strub2020pdt] results (100 runs, 2 s budget) on four very hard 2D scenarios. DIP and $\mathcal{G}$-DIP achieve 100% success on all scenarios. On Bottleneck, all four sampling-based baselines fall below 3% success; on Tight Labyrinth, only EIT\* reaches 47%. On Mega Forest, EIT\* attains 99% success but at a median cost of 1.51---17% higher than $\mathcal{G}$-DIP's 1.29.

#### GNN Scoring Provides Targeted Speedup on Combinatorially Hard Maps

$\mathcal{G}$-DIP reduces initial solve time by 4.6$\times$ on Mega Forest (48 ms vs. 223 ms) and 3.3$\times$ on Bottleneck (158 ms vs. 516 ms). On Bottleneck, $\mathcal{G}$-DIP also reduces median cost from 1.52 to 1.33 (12.5%), indicating that GNN-selected corridors are closer to optimal. On Tight Labyrinth and Cluttered Field, where DIP already solves in 16 ms and 35 ms, $\mathcal{G}$-DIP matches both cost and latency.

Fig. [2](#fig:convergence){reference-type="ref" reference="fig:convergence"} shows the convergence plots.

## 3D Bottleneck Benchmark {#sec:complex3d}

To stress-test narrow-passage planning in 3D, we design four bottleneck scenarios where all feasible paths traverse walls with a single narrow door (width 0.035--0.05 in a unit cube). The probability of hitting a passage of width $\varepsilon$ scales as $\varepsilon^3$, making sampling-based discovery exponentially harder. Slab cells exactly represent free space regardless of passage width, and paths within convex cells are collision-free by construction.

- Bottleneck Office: $4\!\times\!4$ rooms separated by walls with one narrow door each, a horizontal floor partition, and 30 clutter boxes (181--190 obstacles).

- Bottleneck Maze: Recursive-division maze with single-door walls, two vertical zones, one floor partition, and 25 clutter boxes (129--175 obstacles).

- Bottleneck Layers: Three layers of $3\!\times\!3$ rooms with narrow doors and narrow floor holes (radius 0.04--0.05), plus 30 clutter boxes (239--246 obstacles).

- Dense BN Office: BN Office augmented with 120 extra clutter boxes, yielding $\sim$`<!-- -->`{=html}600 cells and $\sim$`<!-- -->`{=html}1600 portals (vs. $\sim$`<!-- -->`{=html}200 cells originally)---a search space where unguided $k$-shortest enumeration becomes a bottleneck.

Six planners (DIP, $\mathcal{G}$-DIP, BIT\*, AIT\*, iRRT\*, EIT\*) are evaluated via PDT over 50 runs with a 20 s budget on the most challenging map per scenario.

#### DIP Maintains Perfect Reliability Across All 3D Scenarios

Table [\[tab:benchmark\]](#tab:benchmark){reference-type="ref" reference="tab:benchmark"} reports all results. DIP and $\mathcal{G}$-DIP maintain 100% success on all four scenarios, including the dense variant with $\sim$`<!-- -->`{=html}600 cells. AIT\* fails entirely on BN Layers and the dense variant (0%), iRRT\* drops to 78% on BN Layers, and BIT\* to 98% on BN Office. EIT\* sustains 100% across all scenarios but requires the full 20 s budget.

#### Speed--Quality Tradeoff Between DIP and Asymptotic Planners

DIP produces initial solutions in 18--48 ms, compared to 110--470 ms for BIT\* (4--26$\times$ slower) and 73--100 ms for EIT\*. EIT\* achieves lower median costs (1.78--1.90 vs. DIP's 2.02--2.34) through asymptotic refinement; DIP trades this for immediate availability. On the dense variant, $\mathcal{G}$-DIP solves in 0.12 s---2.2$\times$ faster than DIP (0.26 s) and 3.6$\times$ faster than BIT\* (0.43 s); convergence plots (Fig. [2](#fig:convergence){reference-type="ref" reference="fig:convergence"}) confirm $\mathcal{G}$-DIP converges 2$\times$ faster on this variant.

#### Neural Corridor Scoring Reduces the Effective Branching Factor

The $k$-sweep ablation (Table [2](#tab:ksweep){reference-type="ref" reference="tab:ksweep"}) confirms that $\mathcal{G}$-DIP at $k{=}8$ achieves cost 2.369, closely matching DIP $k{=}32$ at 2.346---a 3.5$\times$ total speedup (2011 ms vs. 6940 ms) at only 1.0% cost increase. The initialization gap is even larger: 64 ms vs. 419 ms (6.5$\times$), showing that GNN scores reduce the number of corridors that must be enumerated by a factor of four.

::: {#tab:ksweep}
+-----------+---------------------------+-----------+------------+-------+
| Scenario  | Config                    | Init (ms) | Total (ms) | Cost  |
+:==========+:==========================+==========:+===========:+======:+
| D-BN Ofc. | DIP $k{=}32$              | 419       | 6940       | 2.346 |
|           +---------------------------+-----------+------------+-------+
|           | $\mathcal{G}$-DIP $k{=}8$ | **64**    | **2011**   | 2.369 |
+-----------+---------------------------+-----------+------------+-------+

: $k$-sweep ablation on Dense BN Office (5 maps $\times$ 5 seeds). $\mathcal{G}$-DIP at $k{=}8$ matches DIP $k{=}32$ quality at 3.5$\times$ speedup.
:::

Fig. [2](#fig:convergence){reference-type="ref" reference="fig:convergence"} presents the convergence plots.

:::: {#fig:convergence .figure latex-placement="!t"}
![Mega Forest (2D)](Xie2026GNNDIP_figs/megaForest2D_convergence_standalone.png){width="\\textwidth"}

![Bottleneck (2D)](Xie2026GNNDIP_figs/bottleneck2D_convergence_standalone.png){width="\\textwidth"}

![Tight Labyrinth (2D)](Xie2026GNNDIP_figs/tightLabyrinth2D_convergence_standalone.png){width="\\textwidth"}

![Cluttered Field (2D)](Xie2026GNNDIP_figs/clutteredField2D_convergence_standalone.png){width="\\textwidth"}

\

![BN Office (3D)](Xie2026GNNDIP_figs/bottleneckOffice3D_convergence_standalone.png){width="\\textwidth"}

![BN Maze (3D)](Xie2026GNNDIP_figs/bottleneckMaze3D_convergence_standalone.png){width="\\textwidth"}

![BN Layers (3D)](Xie2026GNNDIP_figs/bottleneckLayers3D_convergence_standalone.png){width="\\textwidth"}

![Dense BN Ofc. (3D)](Xie2026GNNDIP_figs/denseBottleneckOffice3D_convergence_standalone.png){width="\\textwidth"}

::: caption
PDT convergence plots: success rate (top) and median cost (bottom) vs. time. *Top row*: 2D very hard scenarios (100 runs, 2 s). *Bottom row*: 3D bottleneck scenarios (50 runs, 20 s) and Dense BN Office ($\sim$`<!-- -->`{=html}600 cells); $\mathcal{G}$-DIP converges 2$\times$ faster than DIP on the dense variant.
:::
::::

## Cross-Scenario Generalization {#sec:generalization}

To evaluate whether GNN portal scoring generalizes beyond its training distribution, we conduct two transfer experiments on seven 3D bottleneck scenarios---the four from Sec. [5.2](#sec:complex3d){reference-type="ref" reference="sec:complex3d"} plus Dense BN Maze ($\sim$`<!-- -->`{=html}450 cells) and two individual unseen maps (BN Office #15, BN Maze #20). Each is tested with 50 runs and a 20 s budget.

#### Leave-One-Type-Out (LOTO)

Training data spans four scenario families: office, maze, layers, and warehouse (261 samples across 14 subtypes). For each family $f$, we train a LOTO model $\mathcal{G}_{\neg f}$ on all data *excluding* family $f$ and evaluate it on scenarios from $f$. This directly measures cross-family transfer.

#### Simple-to-Complex Transfer

A model $\mathcal{G}_\text{sim}$ is trained exclusively on four basic scenario types (forest, narrow passage, multi-room, cluttered)---none containing bottleneck structures---and tested on all complex bottleneck scenarios.

Table [\[tab:generalization\]](#tab:generalization){reference-type="ref" reference="tab:generalization"} shows that LOTO models match the full model within 0.1% cost in 6 of 7 scenarios with equivalent or faster solve times. The single degradation is Dense BN Maze (+13% cost when maze data is excluded), localizable to maze-specific structural knowledge. $\mathcal{G}_\text{sim}$ matches or improves DIP solve times on all bottleneck scenarios (up to 2.3$\times$ speedup on dense variants) despite never encountering bottleneck structures during training, confirming that spatial features (distance, clearance, connectivity) transfer effectively to complex layouts.

## Dynamic 2D Evaluation {#sec:dynamic2d}

We evaluate GNN-DIP for high-frequency replanning in dynamic 2D environments. Ten scenarios each consist of 10 time steps (100 instances total), with $\sim$`<!-- -->`{=html}50% static, 30% moving, and 20% toggling obstacles (15--58 per step, 96--358 CDT cells). GNN-DIP executes the full pipeline (CDT + GNN + DIP) per step; OMPL runs five planners and selects the best valid result. Both use a 0.5 s budget. OMPL paths are post-validated via dense collision checking (200 samples/unit); only collision-free paths count as successes.

#### GNN-DIP Dominates Dynamic Replanning in Reliability, Latency, and Cost

GNN-DIP achieves 99% success (99/100, with the single failure being genuinely unsolvable) compared to OMPL's 40% after collision post-validation. GNN-DIP solves each step in 1.8--44 ms (50--280$\times$ speedup). Fig. [3](#fig:dynamic_summary){reference-type="ref" reference="fig:dynamic_summary"} shows consistently lower path costs across all 10 scenarios, with the largest margins on multi-room environments (6--8% reduction), and solve times under 50 ms including the pipeline overhead (CDT $\sim$`<!-- -->`{=html}10 ms + GNN $\sim$`<!-- -->`{=html}5 ms).

:::: {#fig:dynamic_summary .figure latex-placement="t"}
![](Xie2026GNNDIP_figs/dynamic_summary_3panel.png){width="95%"}

::: caption
Dynamic 2D benchmark summary across 10 scenarios. (a) Average path cost: GNN-DIP achieves lower cost on all scenarios, especially multi-room (6--8% reduction). (b) Average solve time: GNN-DIP solves in 1.8--44 ms vs. OMPL's 500 ms budget (50--280$\times$ speedup). (c) Success rate: GNN-DIP achieves 99% vs. OMPL's 40% after collision post-validation.
:::
::::

#### Collision Safety by Construction

The success gap reflects a fundamental architectural difference. To quantify this, we measure OMPL's pre-validation success rate (planner finds *any* path) and post-validation rate (path survives dense collision checking) at two motion-validation resolutions: the default (${\sim}1\%$ of space extent) and $2{\times}$ ($0.5\%$, which doubles the per-edge checking cost). Within the same 0.5 s budget, pre-validation success is unchanged (489/500 vs. 488/500 individual planner runs), confirming that the planning algorithms succeed and the overhead is negligible. However, post-validation success rises from 36% to 79%---yet 21% of steps still contain paths that penetrate thin walls. Further increasing resolution would continue to reduce violations at the cost of exploring fewer edges per time budget. In contrast, DIP's collision safety is an *architectural guarantee*: CDT cells exactly partition free space along obstacle boundaries, so any path within a corridor is collision-free by construction, independent of resolution parameters.

# Discussion and Conclusion {#sec:discussion}

DIP exploits geometric structure for deterministic, fast initial solutions with 100% success on all scenarios, while sampling-based planners offer asymptotic optimality but suffer reduced reliability in narrow passages ($\varepsilon^3$ sampling probability in 3D). GNN guidance bridges the speed--quality gap: on small decompositions ($\sim$`<!-- -->`{=html}200 cells) the benefit is modest, but as complexity grows ($\sim$`<!-- -->`{=html}600+ cells) GNN scoring reduces the effective branching factor by $4\times$. Cross-scenario generalization (Table [\[tab:generalization\]](#tab:generalization){reference-type="ref" reference="tab:generalization"}) confirms that learned spatial features transfer across scenario families and from simple to complex environments. Python-based inference adds 10--50 ms; ONNX Runtime integration would reduce this to sub-millisecond levels.

## Extension: CBF-Guarded Execution {#sec:cbf}

DIP produces collision-free *point* paths; for a disk robot of radius $r$, wall clearance must be enforced at runtime. Rather than inflating obstacles (requiring re-decomposition) or shrinking portals (over-conservative), we define a CBF [@ames2017cbf] on each corridor wall with endpoints $(w_1, w_2)$: $$\begin{equation}
h(q) = \operatorname{dist}\bigl((x,y),\; \overline{w_1 w_2}\bigr) - r,
\label{eq:barrier}
\end{equation}$$ where $\{q : h(q) \geq 0\}$ is the safe region. The DIP corridor structure is naturally suited for CBF integration because of two properties. First, *sparse constraints*: the filter monitors only walls of the current and neighboring corridor cells (${\leq}\,4$ constraints per step), far fewer than whole-space CBF formulations that check all obstacle boundaries. Second, *mostly-passive monitoring*: as Fig. [4](#fig:cbf_triangle){reference-type="ref" reference="fig:cbf_triangle"}(a) illustrates, in a typical CDT cell the path traverses a convex interior where $h(q) \gg 0$---the CBF constraint is trivially satisfied and the nominal controller runs unmodified. CBF intervention activates only in the few narrow cells near bottlenecks where $h \approx r$ (Fig. [4](#fig:cbf_triangle){reference-type="ref" reference="fig:cbf_triangle"}(b)), making the filter effectively a lightweight *portal guard*. The resulting filter clamps forward speed to $v \leq \gamma h / |a|$ when heading toward a wall, preserving forward invariance without a QP solver.

:::: {#fig:cbf_triangle .figure latex-placement="t"}
![](Xie2026GNNDIP_figs/cbf_triangle.png){width="\\columnwidth"}

::: caption
CBF behavior within CDT cells. (a) Typical cell: path traverses the convex interior far from the wall, $h(q) \gg 0$, CBF inactive. (b) Narrow cell near a bottleneck: path forced close to wall, $h \approx r$, CBF activates to enforce clearance.
:::
::::

:::: {#fig:cbf_portal .figure latex-placement="t"}
![](Xie2026GNNDIP_figs/cbf_portal_cspace.png){width="\\columnwidth"}

::: caption
CBF-guarded passage tube. Safe swept volume (green) clipped to free space; tube constricts at the narrow door where the robot maintains wall clearance.
:::
::::

## Concluding Remarks

GNN-DIP integrates GNN portal scoring with a two-phase decomposition-informed planner, with formal completeness and convergence guarantees. Key findings: (1) DIP achieves 89.5% win rate over OMPL at 10 ms in 2D, with GNN guidance solving tight labyrinths in under 20 ms; (2) in 3D bottleneck environments (129--246 obstacles, narrow doors of width 0.035--0.05), DIP achieves 100% success vs. 0--100% for sampling-based planners, with 3--20$\times$ speed advantage over BIT\*; (3) $\mathcal{G}$-DIP at $k{=}8$ matches DIP $k{=}32$ at 3.5$\times$ speedup on dense 3D ($\sim$`<!-- -->`{=html}600 cells); (4) in dynamic 2D, GNN-DIP achieves 99% vs. 40% success with 50--280$\times$ speedup.

Future work will address improving 3D path quality via gradient-based refinement within convex corridors, extending Slab decomposition to non-axis-aligned obstacles, C++ GNN integration via ONNX Runtime for sub-millisecond inference, and experimental validation of the CBF execution layer for finite-size robots navigating narrow passages.

::: thebibliography
25

S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *Int. J. Robot. Res.*, vol. 30, no. 7, pp. 846--894, 2011.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Batch informed trees (BIT\*): Sampling-based optimal planning via the heuristically guided search of implicit random geometric graphs," in *Proc. IEEE Int. Conf. Robot. Autom. (ICRA)*, 2015, pp. 3067--3074.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic," in *Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)*, 2014, pp. 2997--3004.

J. Y. Yen, "Finding the K shortest loopless paths in a network," *Management Science*, vol. 17, no. 11, pp. 712--716, 1971.

D. T. Lee and F. P. Preparata, "Euclidean shortest paths in the presence of rectilinear barriers," *Networks*, vol. 14, no. 3, pp. 393--410, 1984.

J.-C. Latombe, *Robot Motion Planning*, vol. 124 of *The Springer International Series in Engineering and Computer Science*. Springer Science & Business Media, 2012.

J. R. Shewchuk, "Triangle: Engineering a 2D quality mesh generator and Delaunay triangulator," in *Proc. 1st Workshop Appl. Comput. Geom.*, 1996, pp. 203--222.

The CGAL Project, *CGAL User and Reference Manual*, 6.0.1 ed. CGAL Editorial Board, 2024.

M. P. Strub and J. D. Gammell, "Adaptively Informed Trees (AIT\*) and Effort Informed Trees (EIT\*): Asymmetric bidirectional sampling-based path planning," *Int. J. Robot. Res.*, vol. 41, no. 4, pp. 390--417, 2022.

I. A. Şucan, M. Moll, and L. E. Kavraki, "The Open Motion Planning Library," *IEEE Robot. Autom. Mag.*, vol. 19, no. 4, pp. 72--82, 2012.

B. Ichter, J. Harrison, and M. Pavone, "Learning sampling distributions for robot motion planning," in *Proc. IEEE Int. Conf. Robot. Autom. (ICRA)*, 2018, pp. 7087--7094.

J. Wang, W. Chi, C. Li, C. Wang, and M. Q.-H. Meng, "Neural RRT\*: Learning-based optimal path planning," *IEEE Trans. Autom. Sci. Eng.*, vol. 17, no. 4, pp. 1748--1758, 2020.

B. Chen, B. Dai, Q. Lin, G. Ye, H. Liu, and L. Song, "Learning to plan in high dimensions via neural exploration-exploitation trees," in *Proc. Int. Conf. Learn. Representations (ICLR)*, 2020.

B. Ichter and M. Pavone, "Robot motion planning in learned latent spaces," *IEEE Robot. Autom. Lett.*, vol. 4, no. 3, pp. 2407--2414, 2019.

C. Yu and S. Gao, "Reducing collision checking for sampling-based motion planning using graph neural networks," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 34, 2021, pp. 4274--4289.

A. H. Qureshi, Y. Miao, A. Simeonov, and M. C. Yip, "Motion planning networks: Bridging the gap between learning-based and classical motion planners," *IEEE Trans. Robot.*, vol. 37, no. 1, pp. 48--66, 2021.

X. Zang, M. Yin, J. Xiao, S. Zonouz, and B. Yuan, "GraphMP: Graph neural network-based motion planning with efficient graph search," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 36, 2023, pp. 3131--3142.

T. N. Kipf and M. Welling, "Semi-supervised classification with graph convolutional networks," in *Proc. Int. Conf. Learn. Representations (ICLR)*, 2017.

T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, "Focal loss for dense object detection," in *Proc. IEEE Int. Conf. Comput. Vision (ICCV)*, 2017, pp. 2999--3007.

D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *Proc. Int. Conf. Learn. Representations (ICLR)*, 2015.

A. Paszke *et al.*, "PyTorch: An imperative style, high-performance deep learning library," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2019, pp. 8024--8035.

M. Fey and J. E. Lenssen, "Fast graph representation learning with PyTorch Geometric," in *ICLR Workshop on Representation Learning on Graphs and Manifolds*, 2019.

P. Xie, J. Betz, and A. Alanwar, "Informed hybrid zonotope-based motion planning algorithm," *arXiv preprint arXiv:2507.09309*, 2025.

A. D. Ames, X. Xu, J. W. Grizzle, and P. Tabuada, "Control barrier function based quadratic programs for safety critical systems," *IEEE Trans. Autom. Control*, vol. 62, no. 8, pp. 3861--3876, 2017.
:::

[^1]: Peng Xie, Yanlinag Huang, Wenyuan Wu and Amr Alanwar are with the TUM School of Computation, Information and Technology, Department of Computer Engineering, Technical University of Munich, 74076 Heilbronn, Germany. `(e-mail: p.xie@tum.de, yanlinag.huang@tum.de, wenyuan.wu@tum.de, alanwar@tum.de)`
