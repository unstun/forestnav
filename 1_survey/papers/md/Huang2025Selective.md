---
citation_key: Huang2025Selective
arxiv_id: 2507.15710
arxiv_url: https://arxiv.org/abs/2507.15710
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:20:18Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Robotics, motion planning, path planning, sampling-based motion planning, high-dimensional motion planning, manipulator motion planning
:::

# Introduction

:::: {#fig:Visualization .figure}
::: caption
The search results of (a)(c) FMT$^*$ and (b)(d) MRFMT$^*$ in the Bug Trap problem and a 7-DoF manipulation problem are presented. In the 7-DoF manipulation problem, the Franka Emika Panda robot is requested to move its end effector across the small hole in the wall. Both planners probe the free state space with the same number of uniform random samples. However, MRFMT$^*$ selectively densifies the search tree near narrow regions of the state space, enabling it to find a solution with a significantly sparser search tree.
:::
::::

Sampling-based algorithms, such as Probabilistic Roadmap (PRM) [@PRM], Expansive Space Trees (EST) [@EST], and Rapidly-Exploring Random Tree (RRT) [@RRT], which probabilistically probe state spaces using uniform random samples, have proven to be highly effective in addressing motion planning tasks for high DoF robots under kinematic or dynamic constraints. RRT$^*$ [@RRTstar] and its variants [@RRTsharp; @RRTX] have shown enhancements in solution completeness and optimality. Fast Marching Tree (FMT$^*$) [@FMT] further improves efficiency by decoupling the search from the order of random samples. It employs forward dynamic programming recursion on a batch of random samples in order of heuristically estimated solution cost, resulting in more efficient exploration of problem domains. However, for robotic systems operating within a restricted subset of the configuration space, influenced by factors such as environmental layout (e.g., initial and goal configurations, tight corridors), dynamic constraints (e.g., torque limitations), or implicit restrictions (e.g., loop closures), a large number of random samples is required to ensure the connectivity of the underlying search graph, as the probability of placing a random sample inside narrow passageways is minimal, resulting in extensive search cost and degraded performance of sampling-based planners.

Some approaches strike a balance between completeness and efficiency by biasing samples towards narrow passageways or regions that could improve search efficiency. Some perform geometric analysis on workspaces or configuration spaces to identify narrow passageways, which can be computationally expensive, especially for robots with complex dynamic or implicit constraints [@MediaAxis; @WorkspaceImportance; @DDRRT; @VolumnRRT; @Entropy; @Utility; @InformedRRT]. Others avoid explicit geometric description by learning implicit representation of configuration spaces through past planning instances [@WeightingFeature; @HybridSampling; @Bayesian; @Learning; @LEGO; @MDP; @CVAE; @LocalPremitive; @SPARKandFLAME]. However, these strategies often encounter limitations in generalizing to diverse problems or require laborious offline training to ascertain the model parameters.

Recently, multi-resolution planning has been proposed [@MRA; @SelectiveDensification; @MultilevelSparseRoadmap], which approximates configuration spaces using roadmaps with varying densities. This method enables fast performance by primarily exploring sparser roadmaps and only densifying them when necessary (e.g., navigating through narrow state spaces). Although the existing approaches bypass the need for prior environmental knowledge or offline training, they still require advanced discretization of configuration spaces or well-crafted heuristic functions to guide exploration effectively, making them impractical for online motion planning in complex problem domains.

We aim to develop a general, efficient approach for fast online motion planning in high-dimensional restricted configuration spaces. To this end, we propose the Multi-Resolution FMT$^*$ (MRFMT$^*$) algorithm, which performs biased exploration of configuration spaces online without a prior discretization of configuration spaces or problem-specific heuristics by combining the advantages of random samples with different resolutions. Specifically, MRFMT$^*$ applies multiple FMT$^*$ searches running on uniformly random samples with different resolutions simultaneously. It searches for solution paths mainly over sparse random samples and shifts to denser samples only in areas where the underlying search graph of sparse samples does not contain a feasible path. This selective densification scheme ensures that the planner efficiently navigates the broader landscape and spends most computational efforts in challenging regions. Moreover, we introduce a bidirectional version of this approach, Bidirectional MRFMT$^*$ (BMRFMT$^*$), to further improve planning speed in high-dimensional state spaces. We visualize the search results in the Bug Trap problem in Fig.[1](#fig:Visualization){reference-type="ref" reference="fig:Visualization"}.

This paper is structured as follows. In section [2](#Section:RelatedWorks){reference-type="ref" reference="Section:RelatedWorks"}, we review related works. We present background introductions and detailed descriptions for the proposed methods in Section [3](#Section:Algorithm){reference-type="ref" reference="Section:Algorithm"}. We prove the completeness and asymptotic optimality of MRFMT$^*$ in Section [4](#Section:Analysis){reference-type="ref" reference="Section:Analysis"}. Section [5](#Section:Simulation){reference-type="ref" reference="Section:Simulation"} presents simulation results comparing the proposed method with various state-of-the-art planners to verify the advantages of our method numerically. In Section [6](#Section:Experiment){reference-type="ref" reference="Section:Experiment"}, we further illustrate the superiority of the proposed method in practical applications by applying it to the manipulation task of the Franka Emika Panda robot operating in a highly constrained workspace. Section [7](#Section:Discussions){reference-type="ref" reference="Section:Discussions"} discusses the extension of the proposed algorithms to planning under differential constraints and examines the effects of the algorithm parameters on performance. At the end of this paper, we discuss the results and make conclusions.

# Related Works {#Section:RelatedWorks}

## Biased Sampling

Over the past few decades, biased sampling strategies have been the subject of extensive research. Several geometric methods focus on analyzing the medial axis [@MediaAxis] or performing tetrahedralization [@WorkspaceImportance] of the workspace. These techniques help identify constrained areas and construct probability distributions to sample them preferentially [@DynamicRegionRRT]. In [@Entropy; @Utility], the informativeness of new samples is assessed using geometry-based utility functions designed to maximize roadmap coverage and connectivity. Some approaches employ biased sampling based on the structure of the search tree. For instance, Dynamic-Domain RRT biases samples towards obstacle boundaries and tree nodes [@DDRRT], while the Ball Tree algorithm approximates the free state space using size-varying balls around the search tree [@VolumnRRT]. Instead of relying on uniform sampling to ensure solution completeness, Informed RRT$^*$ [@InformedRRT] takes a different approach by deterministic sampling from a prolate hyperspheroid defined by the current solution cost, thus encompassing all potential samples that could improve the solution.

Geometric analysis of high-dimensional configuration spaces can be computationally intensive, particularly for robotic systems with complex dynamic constraints or implicit limitations. To address this challenge, various learning-based approaches have been explored. Zucker et al. [@WeightingFeature] propose a method for learning a locally optimal weighting of workspace features, thereby adjusting the significance of different features when sampling. Hsu et al. introduce a hybrid sampling strategy combining multiple samplers, each selectively activated based on probabilities learned from experience [@HybridSampling]. Similarly, Lai et al. frame the sequential sampling problem as a Markov process and apply sequential Bayesian updating to refine the local proposal distribution of sampling points based on past observations [@Bayesian]. Rather than relying on past experience, in [@Vonasek], the extension of the search tree is guided by a solution of a relaxed version of the original problem.

Recent advancements in deep learning have led to efforts focused on learning latent representations of configuration spaces and inferring efficient sampling distributions using neural networks. In particular, the robot state and environment are mapped to a distribution over paths, as demonstrated in [@Learning; @NeuralRRT]. Ichter et al. [@CVAE] train a Conditional Variational AutoEncoder (CVAE) to transform a uniform Gaussian distribution into a biased sampling distribution that favors the predicted shortest path based on the environmental layout. The LEGO framework [@LEGO] alleviates the learning burden by training a CVAE to generate bottleneck samples through which a near-optimal path must pass. Additionally, in [@LocalPremitive; @SPARKandFLAME], a batch of local samplers is trained to capture workspace features that create \"challenging regions\" within the configuration space. These local samplers are combined to generate a biased global sampler, enabling effective planning in workspaces of arbitrary sizes.

Some research approaches view biased sampling as a decision-making process and employ reinforcement learning methods to learn the optimal policy online. For instance, in [@MDP], the optimal sampling distribution is converted into a sample rejection procedure and framed as a Markov Decision Process (MDP), which is modeled using a fully connected neural network. RRF$^*$ [@RRF] expands multiple local search trees simultaneously from different roots and learns the optimal tree expansion sequences through a Multi-Armed Bandit (MAB) formulation. Faroni and Berenson enhance kinodynamic RRT by applying the MAB algorithm to learn the optimal transition sequence [@MAB_kinoRRT].

While learning-based techniques show promise in integrating environmental and system knowledge to enhance sampling-based motion planning, their substantial offline training requirements may limit their practicality for tasks that demand a plug-and-play planner. Moreover, many of these approaches necessitate high-performance computing platforms, which can significantly increase overall system costs.

## Multi-resolution Planning

Multi-resolution planning was initially adopted by some graph-based approaches [@Likhachev; @Smooth], which discretizes the configuration space to a multi-resolution lattice tailored to specific environments and problems in prior in order to accelerate online planning speed. The Multilevel Sparse Roadmap algorithm[@MultilevelSparseRoadmap] adapts multi-resolution planning for online use by combining roadmaps at various resolutions. It precomputes a sequence of roadmaps with an increasing number of evenly distributed edges and iteratively searches for the shortest path from the sparsest to the densest roadmap. This approach enables a robot to quickly find an initial path, which can then be refined to yield a more optimal solution. Nonetheless, a significant drawback is that the search expense can be particularly high if no path exists in the sparse roadmaps, even though the dense roadmaps are only crucial in limited regions.

Search efficiency can be improved by making the sparse and dense roadmaps complementary. Several approaches selectively densify specific regions while primarily searching over sparse roadmaps [@MRA; @SelectiveDensification]. The MRA$^*$ algorithm [@MRA] employs multiple searches across different roadmaps. When the search on coarser roadmaps is inadmissible, MRA$^*$ switches to the finest resolution for further exploration. However, this reliance on the finest resolution can dominate the planning process, even when it can not significantly enhance the solution quality. In contrast, the Selective Densification algorithm [@SelectiveDensification] connects roadmaps using zero-cost cross-layer edges and searches the combined graph with the Weighted A$^*$ algorithm [@WA]. The heuristics for each layer are scaled by an inflation factor proportional to the layer's density, which biases the search toward sparser layers unless the solution path requires traversing denser roadmap samples. Nonetheless, the inflation parameters must be carefully chosen beforehand to ensure optimal performance, as a too-small parameter leads to costly searches over the entire layered graph, while a too-large one results in a search being overly dominated by heuristics.

As a multi-resolution motion planner, our approach does not require offline training or prior knowledge of the environment. Distinguished from the existing schemes, ours avoids the need for in prior configuration space discretization or roadmap construction. Instead, it probes the configuration space probabilistically by random samples and constructs a search graph over the random samples online. Furthermore, our approach eliminates the need for manually tuned parameters to guide the search across different resolutions, enhancing its practicality for real-world applications. Ours also adopts a lazy collision check scheme when expanding the search graph, which significantly reduces the number of edge evaluations during the whole planning procedure, cutting down the overall search time for a feasible solution compared with the previous approaches.

# Multi-resolution Sampling-based Planners {#Section:Algorithm}

Let $\mathcal{X}$ be a $d$-dimensional configuration space ($d\geq 2$) with free space $\mathcal{X}_{free}$ and configurationspace obstacles $\mathcal{X}_{obs} = cl(\mathcal{X}\backslash \mathcal{X}_{free})$. A path planning problem can then be characterized by a triplet $(\mathcal{X}_{free}, x_{init}, \mathcal{X}_{goal})$. A feasible solution path $\pi$ for the planning problem $(\mathcal{X}_{free}, x_{init}, \mathcal{X}_{goal})$ is an ordered set of collision-free configurations from the initial condition $x_{init}\in\mathcal{X}_{free}$ to the goal region $\mathcal{X}_{goal}\subset\mathcal{X}_{free}$, i.e., $\pi(0) = x_{init}$ and $\pi(1)\in \mathcal{X}_{goal}$. Denote the set of all paths by $\Sigma$. A cost function for the planning problem is $c: \Sigma\rightarrow \mathbb{R}_{\geq 0}$. Let $\Pi$ be the set of all feasible solutions. The optimal solution $\pi^*$ is the one with $c(\pi^*) = min_{\pi\in \Pi}c(\pi)$. Our goal is to find a feasible solution path with a cost close to $\pi^*$. The motion planner should report failure to the user if no feasible path exists.

## High-level description

MRFMT$^*$ stands out in its approach to approximating configuration spaces. It does so at the beginning of planning using uniform random samples generated at multiple resolutions, a unique method that distinguishes it from traditional sampling-based planners. Traditional sampling-based planners either employ an incremental sampler that generates one sample [@RRT; @PRM; @RRTstar] or a batch of samples [@BIT; @Densification] at a time during planning to refine their approximation of the configuration space. Alternatively, some planners approximate the configuration space in advance using a predetermined number of random samples [@FMT]. One of the key challenges faced by traditional planners is the significant increase in average neighboring size and overall search cost as the total number of samples in the graph increases. This is particularly problematic for problems where a dense underlying graph is necessary for covering narrow passages. MRFMT$^*$ addresses this challenge by conducting a multi-resolution search, simultaneously exploring samples at different resolutions. It prioritizes searching the coarsest samples during the planning procedure, transitioning to finer resolution samples only when the coarsest samples fail to produce a feasible solution. The concept of prioritizing coarsest samples to mitigate the complexity of high-resolution graph searches was also adopted by EIRM$^*$ [@EIRM], a multi-query sampling-based planner that resets to the coarsest samples at the start of each new query. However, EIRM$^*$ still relies on incrementally densifying the graph to find feasible solutions during queries.

MRFMT$^*$ performs local planning from the initial sample to iteratively identify a solution path. In particular, it applies the forward dynamic programming recursion proposed by FMT$^*$ [@FMT] across the multi-resolution samples to generate a tree of paths that gradually expand in cost-to-come space. This recursion expands the sample with the lowest estimated solution cost and selectively establishes locally optimal connections for its neighboring samples. If a locally optimal connection (assuming no obstacles) intersects an obstacle, that neighboring sample is skipped and revisited later instead of seeking alternative locally optimal connections in the vicinity like RRT$^*$. Since the forward dynamic programming recursion evaluates only the edges with locally optimal solution costs, the overall number of edge evaluations of FMT$^*$ is significantly reduced while ensuring asymptotically optimal solutions. The difference from FMT$^*$ is that MRFMT$^*$ constrains expansion to the samples with the same resolution, which further reduces the number of neighboring queries and edge evaluations. The forward dynamic programming recursion enables MRFMT$^*$ to simultaneously conduct fast graph construction and solution search, in contrast to previous multi-resolution planners [@MultilevelSparseRoadmap; @MRA; @SelectiveDensification] that must either separate these phases or perform numerous expensive edge evaluations.

Bidirectional search is a widely used technique to enhance the performance of motion planners and has demonstrated its efficiency in various applications [@RRTconnect; @BFMT; @SelectiveDensification]. The idea of bidirectional search is to simultaneously propagate two search wavefronts initiated from the start and the goal samples, aiming to meet in between. BMRFMT$^*$ combines the bidirectional search strategy with the proposed multi-resolution sampling-based planner to enhance planning efficiency in high-dimensional configuration spaces.

## Multi-resolution Random Samples {#RandomSampleSetDef}

Consider a sequence of $N$ unique configurations uniformly sampled from $\mathcal{X}$, denoted as $(x_1, x_2, \cdots, x_N)$, along with a strictly increasing sequence of $L$ positive constants, $(0<n_1 < n_2 < \cdots <n_L = N)$, where $L<<N$. The random sample set with the $l^{th}$ dense sparsity level, denoted as $X_l$, consists of the samples representing the first $n_l$ configurations. Additionally, we include the goal and initial configuration samples $x_{goal}$ and $x_{init}$ in every sample set. For each sample set $X_l$, we calculate the sample connection radius $r_l$ or the number of neighbors $k_l$ as a function of the sample set size $n_l$ by following the same principles as Rapidly-Exploring Random Graph (RRG) or kPRM [@RRTstar]. Let $x_i^l$ represent a sample from $X_l$. The counterpart samples $x_i^{l-1}$ and $x_i^{l+1}$ correspond to samples with the same configuration but in adjacent resolutions. Note that $x_i^{l-1}$ does not always exist as $n_{l-1} < n_l$. We define zero-cost edges between these counterparts, allowing MRFMT$^*$ to traverse among samples with different resolutions. The neighbors of a sample $x_i^l$, therefore, contain (i) the samples within the same resolution that are either within a distance $r_l$ from $x_i^l$ in an r-disk underlying search graph or among the $k_l$ nearest neighbors in a k-nearest underlying search graph; (ii) the counterpart samples $x_i^{l-1}$ (for $l > 1$) and $x_i^{l+1}$ (for $l < L$).

## MRFMT$^*$ - Detailed Description {#MRFMT_detail}

:::: {#fig:2D_narrow_corridor .figure}
::: caption
The search results of FMT$^*$ over (a) sparse, (b) medium, and (c) dense approximations of a 2D environment with a narrow corridor. Over the sparse and medium approximations, FMT$^*$ fails to find a solution due to the disconnectedness of the underlying search graphs.
:::
::::

::: algorithm
**Input:** $(\mathcal{X}_{free}, x_{init}, \mathcal{X}_{goal})$, $c(\cdot)$, $L$, $\mathbf{X}=\{X_l\}_{l=1,\cdots,L}$

$\mathcal{T}\leftarrow$ []{#initialize label="initialize"}

$z\leftarrow$ $x_{init}^1$ []{#initialize_z label="initialize_z"} $p\leftarrow 1$ []{#initialize_pointer label="initialize_pointer"}

[]{#checkExpansionSuccessful label="checkExpansionSuccessful"} break []{#break label="break"} $z\leftarrow \arg\min_{x\in V_{open, p}}\{\Cost(\mathcal{T}, x)\}$ []{#MAIN:updateZ label="MAIN:updateZ"}

[]{#Track_Path label="Track_Path"} []{#Report_Failure label="Report_Failure"}

------------------------------------------------------------------------

height .2pt

, $V_{unvisited}$, $\{V_{open,l}\}_{l=1,\cdots, L}$)
:::

::: algorithm
**Input:** $(\mathcal{X}_{free}$, $x_{init}$, $\mathcal{X}_{goal})$, $c(\cdot)$, $L$, $\mathbf{X}=\{X_l\}_{l=1,\cdots,L}$ $\mathcal{T}\leftarrow$ []{#BMRFMT:initialize label="BMRFMT:initialize"} $\mathcal{T}'\leftarrow$ []{#BMRFMT:initialize_ label="BMRFMT:initialize_"}

$z\leftarrow$ $x_{init}^1$ , $x_{meet}\leftarrow \phi$ []{#BMRFMT:initialize_z label="BMRFMT:initialize_z"} $p\leftarrow 1$ , $p'\leftarrow 1$ []{#BMRFMT:initialize_pointer label="BMRFMT:initialize_pointer"} []{#BMRFMT:checkExpansionSuccessful label="BMRFMT:checkExpansionSuccessful"} []{#BMRFMT:SwapTreeIfCurrentFailsBegins label="BMRFMT:SwapTreeIfCurrentFailsBegins"} []{#BMRFMT:SwapTreeIfCurrentFailsEnds label="BMRFMT:SwapTreeIfCurrentFailsEnds"} break []{#BMRFMT:break label="BMRFMT:break"} []{#BMRFMT:SwapIfTheOtherTreeIsNotEmptyBegins label="BMRFMT:SwapIfTheOtherTreeIsNotEmptyBegins"} []{#BMRFMT:SwapIfTheOtherTreeIsNotEmptyEnds label="BMRFMT:SwapIfTheOtherTreeIsNotEmptyEnds"} $z\leftarrow \arg\min_{x\in V_{open, p}}\{\Cost(\mathcal{T}, x)\}$ []{#BMRFMT:updateZ label="BMRFMT:updateZ"}
:::

::: algorithm
$V_{new}\leftarrow\phi$ // A node set for saving updated nodes $Z_{near}\leftarrow$$\cap V_{unvisited}$ []{#unvisited label="unvisited"} $X_{near}\leftarrow Neighbor(x)\cap V_{open, p}$ []{#find_X_near label="find_X_near"} $x_{min}\leftarrow \arg\min_{x'\in X_{near}}\{$ $+\hat{c}(x',x)\}$ []{#find_x_min label="find_x_min"} []{#edge_evaluation label="edge_evaluation"} []{#addnode label="addnode"} []{#Expand:UpdateXmeetEnd label="Expand:UpdateXmeetEnd"} $V_{open,p}\leftarrow V_{open,p} \backslash \{z\}$ []{#remove_z_from_open label="remove_z_from_open"}

[]{#Add_update_to_open_begin label="Add_update_to_open_begin"} $l\leftarrow$

$V_{open,l}\leftarrow V_{open,l} \cup \{ v \}$ []{#Add_update_to_open label="Add_update_to_open"}

**if** $l<p$ **then** $p\leftarrow l$ []{#Decrease_Pointer label="Decrease_Pointer"}

------------------------------------------------------------------------

height .2pt
:::

The main algorithm of MRFMT$^*$ is presented in Algorithm [\[MRFMT\]](#MRFMT){reference-type="ref" reference="MRFMT"}. Throughout the search, the algorithm maintains a tree $\mathcal{T}$. It stores successful connections in a sample set $V$, storing the samples connected to the tree, and an edge set $E$, storing pairs of tree samples with feasible motions between them. MRFMT$^*$ associates each sample set with a priority queue $V_{open,l}$ where $l$ is the sparsity level of the sample set, to track the search wavefront of $\mathcal{T}$ in sorted order of estimated solution cost (e.g., cost-to-come). The set $V_{unvisited}$ contains all unvisited samples. To simplify notation, $\mathcal{T}$ is referred to as a quaternion $(V, E, V_{unvisited}, \{V_{open, l}\}_{l=1,\cdots, L})$.

Before diving into the algorithm details, we briefly list the functions employed by the algorithm. The function returns a set of $N$ i.i.d. random samples from $X_{free}$. returns the sparsity level of $x$. $\hat{c}(x,y)$ returns the solution cost from $x$ to $y$ in the assumption that the motion between $x$ and $y$ is collision-free. returns the neighboring samples of $x$ as defined in Section [3.2](#RandomSampleSetDef){reference-type="ref" reference="RandomSampleSetDef"}. returns the unique path in $\mathcal{T}$ from its root to sample $x$, and returns the cost of the path. is a boolean function returning true if the movement between configurations $x$ and $y$ is collision-free. swaps the two trees $\mathcal{T}$ and $\mathcal{T}'$. represents the problem termination criterion (e.g., the search time runs out, a solution from $x_{init}$ to $\mathcal{X}_{goal}$ is found, etc.).

We are now ready to explain the algorithm in detail. MRFMT$^*$ starts by initializing a search tree $\mathcal{T}$ rooted at $x_{init}^1$ using the procedure (line [\[initialize\]](#initialize){reference-type="ref" reference="initialize"}, Algorithm [\[MRFMT\]](#MRFMT){reference-type="ref" reference="MRFMT"}), where $x_{init}^1$ is the sample of $X_1$ which corresponds to the initial configuration. is inserted into $V_{open, 1}$ for expansion. Once initialization is complete, MRFMT$^*$ begins expanding $\mathcal{T}$ using the procedure. We denote $p$ as the sparsity level over which MRFMT$^*$ is searching for expansion, which is initialized to be 1 (line [\[initialize_pointer\]](#initialize_pointer){reference-type="ref" reference="initialize_pointer"}, Algorithm [\[MRFMT\]](#MRFMT){reference-type="ref" reference="MRFMT"}). The procedure finds the locally optimal connection for the unvisited neighboring samples of $z$, which is the lowest-cost open sample at the current sparsity level $p$ and is initially set to $x_{init}^1$ for the first search (line [\[initialize_z\]](#initialize_z){reference-type="ref" reference="initialize_z"}, Algorithm [\[MRFMT\]](#MRFMT){reference-type="ref" reference="MRFMT"}). For each unvisited neighboring sample $x\in Z_{near}$, the procedure firstly searches its neighboring samples with sparsity level $p$ and in the open set (line [\[find_X_near\]](#find_X_near){reference-type="ref" reference="find_X_near"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). The edge between $x$ and the open sample with the minimal heuristically-estimated solution cost, $x_{min}$, is evaluated (line [\[edge_evaluation\]](#edge_evaluation){reference-type="ref" reference="edge_evaluation"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). If the edge is collision-free, $x$ is added to the search tree and removed from $V_{unvisited}$ (line [\[addnode\]](#addnode){reference-type="ref" reference="addnode"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}); otherwise, $x$ is skipped. Any updated sample is opened and inserted into its associated priority queues (line [\[Add_update_to_open_begin\]](#Add_update_to_open_begin){reference-type="ref" reference="Add_update_to_open_begin"}-[\[Add_update_to_open\]](#Add_update_to_open){reference-type="ref" reference="Add_update_to_open"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). If there is an updated sample with a sparser resolution, $p$ is then decreased (line [\[Decrease_Pointer\]](#Decrease_Pointer){reference-type="ref" reference="Decrease_Pointer"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}), and therefore, the next procedure will traverse to the sparser resolution. If $V_{open, p}$ is empty after an expansion, indicating that there are no open samples for expansion at the current sparsity level, MRFMT$^*$ will turn to the denser resolution by increasing $p$ by 1 (line [\[Increase_Pointer\]](#Increase_Pointer){reference-type="ref" reference="Increase_Pointer"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). If there is no wavefront node, i.e., $V_{open, l}$ is empty for all $l=1,\cdots,L$, the search will terminate (line [\[terminate\]](#terminate){reference-type="ref" reference="terminate"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). A solution path can be traced back from $z$ if $z \in \mathcal{X}_{goal}$ (line [\[Track_Path\]](#Track_Path){reference-type="ref" reference="Track_Path"}, Algorithm [\[MRFMT\]](#MRFMT){reference-type="ref" reference="MRFMT"}).

:::: {#fig:Steps .figure}
::: caption
Visualization of the step-by-step planning process of MRFMT$^*$ for the motion planning problem in Fig.[2](#fig:2D_narrow_corridor){reference-type="ref" reference="fig:2D_narrow_corridor"}. The black, green, and yellow dots represent unvisited, open, and closed samples. The dashed grey lines depict the edges of the underlying search graph. Specifically, the vertical edges are the zero-cost edges connecting samples in adjacent layers representing the same configuration. The blue lines represent the edges of the search tree. The sample to expand, $z$, is highlighted by red rectangles.
:::
::::

The search process of MRFMT$^*$ for the narrow-corridor motion planning problem presented in Fig.[2](#fig:2D_narrow_corridor){reference-type="ref" reference="fig:2D_narrow_corridor"} is visualized in Fig.[3](#fig:Steps){reference-type="ref" reference="fig:Steps"}. MRFMT$^*$ is initialized with three random sample sets. Each random sample set forms an underlying search graph, as shown in Fig.[2](#fig:2D_narrow_corridor){reference-type="ref" reference="fig:2D_narrow_corridor"}. Thanks to the defined zero-cost edges between samples representing the same configuration, we can visualize the underlying search graph of MRFMT$^*$ as a three-layered graph. The vertical edges have samples with the same configuration at the ends and, therefore, can be lazily skipped for edge evaluation during the planning procedure. Compared with the search result of FMT$^*$ as shown in Fig.[2](#fig:2D_narrow_corridor){reference-type="ref" reference="fig:2D_narrow_corridor"}, MRFMT$^*$ finds a solution with much fewer edge evaluations (MRFMT$^*$ evaluates 16 edges during the planning, while FMT$^*$ evaluates 24 edges.) and neighbor queries (Because MRFMT$^*$ searches neighboring samples mainly among sparse random sample sets, while FMT$^*$ constantly searches among the densest random sample set.), showing significant benefits in search cost reduction.

## Bidirectional Version - BMRFMT$^*$ {#BMRFMT_detail}

BMRFMT$^*$ is presented in Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"} as simple modifications of MRFMT$^*$, with changes highlighted in blue. Instead of constructing only one search tree, BMRFMT$^*$ constructs a forward search tree $\mathcal{T} = (V, E, V_{unvisited}, \{V_{open, l}\}_{l=1,\cdots,L})$ rooted at $x_{init}^1$ and a backward search tree $\mathcal{T}' = (V', E', V_{unvisited}', \{V_{open, l}'\}_{l=1,\cdots,L})$ rooted at $x_{goal}^1 \in \mathcal{X}_{goal}$ (line [\[initialize\]](#initialize){reference-type="ref" reference="initialize"}-[\[BMRFMT:initialize\_\]](#BMRFMT:initialize_){reference-type="ref" reference="BMRFMT:initialize_"}, Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"}), which are expanded simultaneously during planning. We use $z$ and $z'$ as the pointers to the wavefront node of $\mathcal{T}$ and $\mathcal{T}'$, respectively, and $p$ and $p'$ as the sparsity level of $z$ and $z'$, respectively. $x_{meet}$ is the lowest-cost candidate sample for tree connection, which is updated in the procedure (lines [\[Expand:UpdateXmeetBegin\]](#Expand:UpdateXmeetBegin){reference-type="ref" reference="Expand:UpdateXmeetBegin"}-[\[Expand:UpdateXmeetEnd\]](#Expand:UpdateXmeetEnd){reference-type="ref" reference="Expand:UpdateXmeetEnd"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). BMRFMT$^*$ checks whether the expansion is successful at each iteration in line [\[BMRFMT:checkExpansionSuccessful\]](#BMRFMT:checkExpansionSuccessful){reference-type="ref" reference="BMRFMT:checkExpansionSuccessful"}, Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"}. If the expansion of the current tree fails, it swaps the search trees if the other tree has at least one sample in its search wavefront (line [\[BMRFMT:SwapTreeIfCurrentFailsBegins\]](#BMRFMT:SwapTreeIfCurrentFailsBegins){reference-type="ref" reference="BMRFMT:SwapTreeIfCurrentFailsBegins"}-[\[BMRFMT:SwapTreeIfCurrentFailsEnds\]](#BMRFMT:SwapTreeIfCurrentFailsEnds){reference-type="ref" reference="BMRFMT:SwapTreeIfCurrentFailsEnds"}, Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"}), or breaks if the other tree has no wavefront nodes either (line [\[BMRFMT:break\]](#BMRFMT:break){reference-type="ref" reference="BMRFMT:break"}, Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"}). In the opposite case, i.e., the expansion is successful, it swaps the search tree if the other tree has at least one sample in its search wavefront (line [\[BMRFMT:SwapIfTheOtherTreeIsNotEmptyBegins\]](#BMRFMT:SwapIfTheOtherTreeIsNotEmptyBegins){reference-type="ref" reference="BMRFMT:SwapIfTheOtherTreeIsNotEmptyBegins"}-[\[BMRFMT:SwapIfTheOtherTreeIsNotEmptyEnds\]](#BMRFMT:SwapIfTheOtherTreeIsNotEmptyEnds){reference-type="ref" reference="BMRFMT:SwapIfTheOtherTreeIsNotEmptyEnds"}, Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"}) or continues expanding the current tree until all samples are closed. A solution path can be found by tracing along $\mathcal{T}$ and $\mathcal{T}'$ from $x_{meet}$, provided $x_{meet}$ is not a null pointer (line [\[BMRFMT:track_solution_path_begins\]](#BMRFMT:track_solution_path_begins){reference-type="ref" reference="BMRFMT:track_solution_path_begins"}-[\[BMRFMT:track_solution_path_ends\]](#BMRFMT:track_solution_path_ends){reference-type="ref" reference="BMRFMT:track_solution_path_ends"}, Algorithm [\[BMRFMT\]](#BMRFMT){reference-type="ref" reference="BMRFMT"}).

# Analysis {#Section:Analysis}

This section provides a thorough analysis of the critical properties of the MRFMT$^*$ algorithm, demonstrating its correctness in Theorem [1](#correctness){reference-type="ref" reference="correctness"} and asymptotic optimality in Theorem [2](#AO){reference-type="ref" reference="AO"}.

::: {#ExpandOnce .lemma}
**Lemma 1**. *MRFMT$^*$ expands a sample at most once throughout the entire planning procedure.*
:::

::: proof
*Proof.* By construction, any sample to expand except for $x_{init}$ must be in the unvisited neighboring sample set of the lowest-cost open sample $z$, $Z_{near}$ (line [\[unvisited\]](#unvisited){reference-type="ref" reference="unvisited"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}). Upon expansion, a successfully expanded sample is removed from $V_{unvisited}$ (line [\[remove_z_from_open\]](#remove_z_from_open){reference-type="ref" reference="remove_z_from_open"}, Algorithm [\[Expand\]](#Expand){reference-type="ref" reference="Expand"}), and therefore will never be included in $Z_{near}$ in future expansions. Consequently, each sample can be expanded at most once before MRFMT$^*$ finds a solution. ◻
:::

::: {#correctness .theorem}
**Theorem 1** (Probability Completeness of MRFMT$^*$). *[Let $(\mathcal{X}_{free}, x_{init}, \mathcal{X}_{goal})$ be a robustly feasible path planning problem. Let $n_L$ denote the number of samples in the finest resolution layer of MRFMT$^*$. Then, as $n_L \to \infty$, the probability that MRFMT$^*$ finds a feasible path converges to one:]{style="color: black"} $$\begin{equation}
\lim_{n_L \to \infty} \mathbb{P} \left( V\cap \mathcal{X}_{goal}\right) = 1,
\end{equation}$$ where $V$ is the set of samples connected to the search tree $\mathcal{T}$.*
:::

::: proof
*Proof.* From Lemma [1](#ExpandOnce){reference-type="ref" reference="ExpandOnce"}, we can infer that MRFMT$^*$ either terminates with at least one expanded sample in $\mathcal{X}_{goal}$ and returns a solution path, or exits the search iteration without a solution after exhausting all $V_{open, l}$ for $l=1,\cdots, L$ In the worst case, where all random sample sets with lower resolutions do not contain a solution, MRFMT$^*$ performs an FMT$^*$ search over the finest resolution. Hence, the probability that MRFMT$^*$ returns a feasible solution is lower bounded by the probability that FMT$^*$ finds a feasible solution by searching over the finest resolution sample set. According to [@FMT], when the number of random samples is sufficiently large, the probability that FMT$^*$ finds a feasible solution approaches 1. Therefore, as the number of samples at the finest resolution $n_L\rightarrow\infty$, the probability that MRFMT$^*$ finds a feasible solution also approaches 1, making it probabilistically complete with respect to the finest resolution samples. ◻
:::

[Therefore, to ensure a high planning success rate, a sufficiently large random sample set should be initialized, albeit at the expense of increased search cost.]{style="color: black"}

::: {#AO .theorem}
**Theorem 2** (Asymptotical Optimality of MRFMT$^*$). *Let $(\mathcal{X}_{free}, x_{init}, \mathcal{X}_{goal}, c)$ be a $\xi$-robustly feasible path planning problem in d dimensions, where $\xi>0$, $\mathcal{X}_{goal}$ is $\xi$-regular, and the cost function $c$ admits a robustly optimal solution with finite cost. [Then, as $n_1 \to \infty$, the probability that MRFMT$^*$ returns a path with cost arbitrarily close to $c^*$ converges to one: $$\begin{equation}
\lim_{n_1 \to \infty} \mathbb{P} \left( c(\pi_{n_1}) \to c^* \right) = 1,
\end{equation}$$ where $\pi_{n_1}$ denotes the solution returned by MRFMT$^*$ using $n_1$ samples.]{style="color: black"}*
:::

::: proof
*Proof.* Let $c^*$ denote the cost of the optimal solution, and $c^{ALG}$ denote the cost of the path returned by a motion planning algorithm . To solve the motion planning problem, MRFMT$^*$ applies an FMT$^*$ search over the coarsest resolution sample set until the coarsest resolution sample set has no samples to expand. From Theorem 4.1 in [@FMT], the cost of the path returned by FMT$^*$ with $n$ random samples using the radius in Equation 3 of [@FMT], denoted as $c^{FMT^*}$, satisfies $\mathbb{P}(c^{FMT^*}>(1+\varepsilon)c^*)=0$ as $n\rightarrow\infty$ for all $\varepsilon>0$. Thus, the probability that MRFMT$^*$ biases towards denser resolution sample sets approaches 0 as $n_1$ approaches $\infty$ when MRFMT$^*$ is equivalent to FMT$^*$. Therefore, $$\mathbb{P}(c^{MRFMT^*}>(1+\varepsilon)c^*)=0$$ as $n_1\rightarrow\infty$ for all $\varepsilon>0$, proving that MRFMT$^*$ is asymptotically optimal. ◻
:::

[ Therefore, when the sparser random sample set is sufficiently large, the solution cost improves, albeit at the expense of higher search cost. ]{style="color: black"}

:::: {#fig:SimulationScene .figure}
::: caption
Descriptions of the $\mathbb{SE}(2)$, $\mathbb{SE}(3)$, and $\mathbb{R}^{14}$ rigid-body motion planning problems.
:::
::::

# Simulations {#Section:Simulation}

## Simulation Setup

In this section, we compare MRFMT$^*$ and BMRFMT$^*$ with several sampling-based motion planning algorithms, specifically PRM$^*$[@PRM], RRT$^*$[@RRTstar], BIT$^*$[@BIT], SPARS2[@SPARS2], FMT$^*$[@FMT], and BFMT$^*$[@BFMT], to numerically investigate the advantages of MRFMT$^*$ and BMRFMT$^*$. To ensure a fair comparison, each planning algorithm was tested using the Open Motion Planning Library (OMPL) v1.6.0 [@OMPL]. We considered three motion planning problems from the OMPL's test suite:

- the bug trap problem in $\mathbb{SE}(2)$ as shown in Fig.[4](#fig:SimulationScene){reference-type="ref" reference="fig:SimulationScene"}(a);

- the piano movers' problem in $\mathbb{SE}(3)$ as shown in Fig.[4](#fig:SimulationScene){reference-type="ref" reference="fig:SimulationScene"}.

Besides, we also consider the following problem to investigate the planners' performance in very high-dimensional configuration spaces:

- the movable link robot problem in $\mathbb{R}^{14}$ as shown in Fig.[4](#fig:SimulationScene){reference-type="ref" reference="fig:SimulationScene"}.

The link robot has 12 links and can move freely in the x-y plane. In each case, dynamic constraints were neglected, and arc length was used as the solution cost for all problems.

For the benchmarking algorithms, we used the default OMPL settings, except that we used heuristics for all algorithms and did not extend the graph of FMT$^*$ and BFMT$^*$. We ensured that MRFMT$^*$ and BMRFMT$^*$ used the same tuning parameters and configurations as the benchmarking algorithms whenever possible. To compare the quality between incremental or \"anytime\" planners (i.e., RRT$^*$, SPARS2, PRM$^*$, and BIT$^*$) and non-incremental planners (i.e., FMT$^*$, BFMT$^*$, MRFMT$^*$, and BMRFMT$^*$, which generate solutions via sample batches), we varied the number of free configuration samples $N$ taken during initialization for the non-incremental planners. This variation serves as a proxy for execution time. Specifically, $N$ ranged from 200 to 10,000 for the $\mathbb{SE}(2)$ problems, from 1,000 to 30,000 for the piano movers' problem, and from 4,000 to 40,000 for the movable link robot problem. For MRFMT$^*$ and BMRFMT$^*$, we used a linearly increasing sequence to allocate the number of samples for each random sample set. Specifically, the number of nodes in the $l$th random sample set is given by $n_l = \lfloor lN/L \rfloor$. We used $L=4$ for the $\mathbb{SE}(2)$ problems and $L=6$ for the $\mathbb{SE}(3)$ and the $\mathbb{R}^{14}$ problems as empirically the chosen parameters fit comfortably in memory and was able to solve our scenarios. The maximum memory was limited to 4096 MB for all planners.

## Simulation Results and Discussions

:::: {#fig:ResultVersusTime .figure latex-placement="h"}
::: caption
Planner performance versus time. Each planner was run 50 different times. The median path length is plotted versus run time/sample count for each planner, with unsuccessful trials assigned infinite cost. [The median values are plotted with error bars denoting a non-parametric 95$\%$ confidence interval on the median. The dashed lines are regression lines fitted to the points associated with a given planner.]{style="color: black"}
:::
::::

:::: {#fig:ResultVersusSample .figure latex-placement="h"}
::: caption
Planner performance versus sample count. Each planner was run 50 different times. The median path length is plotted versus run time/sample count for each planner, with unsuccessful trials assigned infinite cost. [The median values are plotted with error bars denoting a non-parametric 95$\%$ confidence interval on the median. The dashed lines are regression lines fitted to the points associated with a given planner.]{style="color: black"}
:::
::::

We present the simulation results for success rate and solution cost versus time in Fig. [5](#fig:ResultVersusTime){reference-type="ref" reference="fig:ResultVersusTime"}. Each point of a non-incremental planner represents the results of 50 simulations with the exact sample count. Since sample count is the primary parameter for non-incremental planners, we also examine its impact on planning performance in Fig. [6](#fig:ResultVersusSample){reference-type="ref" reference="fig:ResultVersusSample"}, which illustrates the simulation results as a function of sample count for non-incremental planners and as a function of planning iteration for incremental planners.

The simulation results in Fig. [5](#fig:ResultVersusTime){reference-type="ref" reference="fig:ResultVersusTime"} indicate that MRFMT$^*$ and BMRFMT$^*$ are the fastest in achieving high success rates across all problems, indicating an improved convergence rate. [Their success rates converge to 1 given larger planning time, validating their probability completeness.]{style="color: black"} Regarding solution cost, they converge to the optimal solution more quickly than all other planners, except for FMT$^*$ and BFMT$^*$. This is because they prioritize searching through sparser graph layers as long as they remain connected in free space, sacrificing optimality for increased efficiency. [ However, for simple problems such as the bug trap problem, MRFMT$^*$ and BMRFMT$^*$ converge to the optimal solution rapidly, even when compared with FMT$^*$ and BFMT$^*$.]{style="color: black"} The success rate and time versus sample count in Fig.[6](#fig:ResultVersusSample){reference-type="ref" reference="fig:ResultVersusSample"} demonstrate that MRFMT$^*$ and BMRFMT$^*$ achieve higher success rates with lower time costs compared to FMT$^*$ and BFMT$^*$ at a given sample count. The higher success rate is attributed to their ability to simultaneously search through multiple graphs with varying densities and combine cross-layer subpaths in free space. The speed advantage arises from the fact that FMT$^*$ and BFMT$^*$ perform a full expansion of every node, whereas MRFMT$^*$ and BMRFMT$^*$ primarily expand nodes on sparse graph layers when navigating through free space to quickly escape local minima, resorting to dense graph layers only when navigating through narrow passages.

Note that MRFMT$^*$ and BMRFMT$^*$ generate nearly identical cost-time curves in 2D problems. However, BMRFMT$^*$ outperforms MRFMT$^*$ in both solution cost and success rate in the Piano Mover's problem in $\mathbb{SE}(3)$ and the movable link robot problem in $\mathbb{R}^{14}$, where the volume of *reachable configurations* around the goal is relatively small. It suggests that the volume of reachable configurations significantly influences execution time. The relatively small volume implies that the backward tree of BMRFMT$^*$ expands its wavefront through fewer states than the forward tree of MRFMT$^*$. Additionally, the tree interconnection in the bidirectional case prevents the forward tree of BMRFMT$^*$ from growing too large compared to the unidirectional search of MRFMT$^*$, resulting in substantial computational cost savings in high-dimensional configuration spaces.

# Experiments {#Section:Experiment}

## Experiment Setup

:::: {#fig:Franka_Problem .figure}
::: caption
Descriptions and results of a 7-DoF manipulation planning problem on the Franka Emika Panda robot. The robot arm is requested to grasp the red cylinder without removing the green cylinders, which is very challenging for traditional methods.
:::
::::

We conducted experiments on the Franka Emika Panda robot equipped with a gripper to validate our proposed method in a realistic environment. In this experiment, the Franka robot was tasked with moving its gripper to retrieve a targeted red bottle located deep inside a shelf, while avoiding the green bottles positioned closely in front of it (see Fig.[7](#fig:Franka_Problem){reference-type="ref" reference="fig:Franka_Problem"}(a)(b)). This scenario is particularly challenging due to the narrow passage available for the robot arm to maneuver. We compare MRFMT$^*$ and BMRFMT$^*$ with several OMPL benchmark planners. The sample count for non-incremental planners was varied from 1,000 to 9,400. An r-disk graph with a radius of 3 was used as the underlying graph for all planners. Both MRFMT$^*$ and BMRFMT$^*$ were evaluated with 4 resolutions.

## Experiment Results and Discussions

A solution provided by MRFMT$^*$ is displayed in Fig.[7](#fig:Franka_Problem){reference-type="ref" reference="fig:Franka_Problem"}(c). The numerical results from the 7-DoF manipulation experiments are summarized in Fig.[7](#fig:Franka_Problem){reference-type="ref" reference="fig:Franka_Problem"}(d). Several planners are not displayed due to their low success rates within the allotted time. The figure presents statistics over 50 runs for each planner. Notably, MRFMT$^*$ and BMRFMT$^*$ achieved the best performance among all planners, with BMRFMT$^*$ demonstrating reduced time to find feasible solutions.

# Discussions {#Section:Discussions}

## Planning under Differential Constraints

Motion planning for Driftless Control-Affine (DCA) systems is a classic problem in robotics. Some examples of DCA systems include mobile robots with wheels that roll without slipping, Unmanned Aerial Vehicle (UAV) whose dynamics involve control inputs for thrust and moment generation, and humanoid Robotoid robots, like ASIMO or Atlas, when focusing on their walking and manipulation capabilities. In [@DFMT], a theoretical framework is proposed to assess optimality guarantees of sampling-based algorithms for planning under differential constraints. We can exploit the framework to extend MRFMT$^*$ and BMRFMT$^*$ to address the motion planning problem for DCA systems by

- finding the neighboring samples with the same resolution by searching for the samples lying within the privileged coordinate box $Box^w(x, \gamma\left(\frac{\log{|n_l|}}{n_l}\right)^{\frac{1}{d}})$, where $Box^w(x, \epsilon)$ denotes the weighted box of size $\epsilon$ centered at $x\in\mathcal{X}$, $w={w_1,w_2,\cdots,w_d}$ denotes the weight vector at $x$, $\gamma$ is a constant defined by the user [^3], and

- connecting samples by edges that are trajectories satisfying the differential constraints.

We show the planning results of MRFMT$^*$ in the Reeds-Sheep experiment conducted in the bug trap environment in Fig.[8](#fig:reedsheep_car){reference-type="ref" reference="fig:reedsheep_car"}. Admittedly, as FMT$^*$ and most other sampling-based algorithms, MRFMT$^*$ is not suitable for systems without direct access to the two-point boundary value solver. We leave this problem to future research.

:::: {#fig:reedsheep_car .figure}
![image](Huang2025Selective_figs/reedsheep_car_MRFMT.png){width="48%"} ![image](Huang2025Selective_figs/reeds_shepp_MRFMT_env13.png){width="48%"}

::: caption
The planning results of MRFMT$^*$ for a Reeds-Shepp car in different 2D environments with narrow passages.
:::
::::

## Effects of the multi-resolution parameters

Theorems [1](#correctness){reference-type="ref" reference="correctness"} and [2](#AO){reference-type="ref" reference="AO"}, proved in Section [4](#Section:Analysis){reference-type="ref" reference="Section:Analysis"}, indicate that the structure of the underlying multi-layer graph significantly influences the performance of the proposed multi-resolution motion planners. To numerically investigate how performance varies with the underlying structure, we consider two types of graphs: one with linearly increasing layer density and another with exponentially increasing layer density. Specifically, for the graph with linearly increasing layer density, the number of nodes in the $l$-th layer is given by $n_l = \lfloor \frac{l}{L}N \rfloor$. In contrast, for the graph with exponentially increasing layer density, it is given by $n_l = \lfloor \frac{1}{2^{L-l}}N \rfloor$.

We compare MRFMT$^*$ across different graph structures, using FMT$^*$ as the benchmark for performance in solving motion planning problems in $\mathbb{SE}(2)$ and $\mathbb{SE}(3)$, as illustrated in Fig.[9](#fig:results_of_layered_graph){reference-type="ref" reference="fig:results_of_layered_graph"}. To ensure consistency, we fixed the neighbor radius and used the same random seed when generating the search graphs, which allows the densest layer of MRFMT$^*$ to match the search graph of FMT$^*$. Our results demonstrate that MRFMT$^*$ achieves the same success rate as FMT$^*$ across various graph structures, which proves the solution completeness property of MRFMT$^*$. Notably, MRFMT$^*$ with linearly increasing layer density yields the lowest solution cost. Conversely, although MRFMT$^*$ with exponentially increasing layer density incurs a higher solution cost due to its sparse graph structure, it requires less time to find a feasible solution. These findings suggest that the multi-resolution parameters controlling sample density across different layers should be carefully selected to balance solution cost and planning time based on task requirements. However, the determination of optimal parameters is beyond the scope of this paper.

:::: {#fig:results_of_layered_graph .figure latex-placement="h"}
::: caption
Planner performance versus sample count. Each planner was run 50 different times. The median values are plotted with error bars denoting a non-parametric 95$\%$ confidence interval on the median. [The lines in the success rate vs. sample count plot overlap.]{style="color: black"}
:::
::::

# Conclusion {#Section:Conclusion}

We proposed MRFMT$^*$, an asymptotically optimal sampling-based planner with the selective densification strategy. MRFMT$^*$ is able to seamlessly transition between sparse and dense probabilistic approximations of configuration spaces, enabling it to achieve fast performance by searching over sparser approximations to navigate through large free state space and only densifying when tackling narrow passages. The bidirectional version of MRFMT$^*$ further reduces search cost by simultaneously propagating search wavefront from two sources. We present a theoretical analysis for MRFMT$^*$ regarding its completeness and optimality. The simulation and experiment results show that MRFMT$^*$ and its bidirectional version can perform rapid online planning in high-dimensional state spaces with narrow passages by combining the advantages of planners with various granularities. With their adaptability, the proposed planners can be easily implemented as a plug-and-play solution for diverse robotic systems, such as humanoid robots and robotic arms, enabling them to perform tasks automatically and efficiently in unstructured environments.

::: thebibliography
00 L. E. Kavraki, P. ˇSvestka, J. C. Latombe, and M. H. Overmars, "Probabilistic roadmaps for path planning in high-dimensional spaces," IEEE Transactions on Robotics and Automation, vol. 12, no. 4, pp.566--580, 1996.

D. Hsu, J.-C. Latombe, and R. Motwani, "Path planning in expansive configuration spaces," International Journal of Computational Geometry and Applications, vol. 9, no. 4, pp. 495--512, 1999.

S. M. LaValle and J. J. Kuffner, "Randomized kinodynamic planning," The International Journal of Robotics Research (IJRR), vol. 20, no. 5, pp. 378--400, 2001.

S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," The International Journal of Robotics Research (IJRR), vol. 30, no. 7, pp. 846--894, 2011.

O. Arslan and P. Tsiotras, "Use of relaxation methods in sampling-based algorithms for optimal motion planning," in IEEE International Conference on Robotics and Automation (ICRA), 2013.

M. Otte and E. Frazzoli, "RRTx: Asymptotically optimal single-query sampling-based motion planning with quick replanning," The International Journal of Robotics Research (IJRR), vol. 35, no. 7, pp. 797--822, 2015.

L. Janson, E. Schmerling, A. Clark, and M. Pavone, "Fast marching tree: A fast marching sampling-based method for optimal motion planning in many dimensions," The International Journal of Robotics Research (IJRR), vol. 34, no. 7, pp. 883--921, 2015.

H. Kurniawati and D. Hsu, \"Workspace importance sampling for probabilistic roadmap planning,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2004.

Yuandong Yang and O. Brock, \"Adapting the sampling distribution in PRM planners based on an approximated medial axis,\" in IEEE International Conference on Robotics and Automation (ICRA), 2004

J. Denny, R. Sandström, A. Bregger, and N. M. Amato, "Dynamic region-biased rapidly-exploring random trees," Springer Proceedings in Advanced Robotics, pp. 640--655, 2020.

A. Yershova, L. Jaillet, T. Simeon, and S. M. LaValle, \"Dynamic-domain RRTs: Efficient exploration by controlling the sampling domain,\" in IEEE International Conference on Robotics and Automation (ICRA), 2005.

Shkolnik, Alexander, and Russ Tedrake, \"Sample-based planning with volumes in configuration space,\" arXiv preprint arXiv:1109.3145, 2011.

B. Burns and O. Brock, \"Information theoretic construction of probabilistic roadmaps,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2003.

B. Burns and O. Brock, \"Toward Optimal Configuration Space Sampling,\" in Robotics: Science and Systems (RSS), 2005.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic," in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2014.

M. Zucker, J. Kuffner, and J. Andrew Bagnell, \"Adaptive workspace biasing for sampling-based planners,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2008.

D. Hsu, G. Sanchez-Ante, and Z. Sun, "Hybrid PRM Sampling with a Cost-Sensitive Adaptive Strategy," in IEEE International Conference on Robotics and Automation (ICRA), 2005.

T. Lai, Philippe Morere, F. Ramos, and G. Francis, "Bayesian Local Sampling-Based Planning," IEEE robotics and automation letters (RAL), vol. 5, no. 2, pp. 1954--1961, Apr. 2020.

V. Vonasek, "Motion Planning of 3D Objects Using Rapidly Exploring Random Tree Guided by Approximate Solutions," in 2018 IEEE 23rd International Conference on Emerging Technologies and Factory Automation (ETFA), 2018.

R. Cheng, K. Shankar, and J. W. Burdick, "Learning an Optimal Sampling Distribution for Efficient Motion Planning," in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020.

J. Wang, W. Chi, C. Li, C. Wang, and M. Q.-H. . Meng, "Neural RRT\*: Learning-Based Optimal Path Planning," IEEE Transactions on Automation Science and Engineering, vol. 17, no. 4, pp. 1748--1758, Oct. 2020, doi: https://doi.org/10.1109/TASE.2020.2976560.

B. Ichter, J. Harrison, and M. Pavone, \"Learning sampling distributions for robot motion planning,\" in IEEE International Conference on Robotics and Automation (ICRA), 2018.

R. Kumar, A. Mandalika, S. Choudhury, and S. Srinivasa, \"LEGO: Leveraging experience in roadmap generation for sampling-based planning,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2019.

C. Chamzas, A. Shrivastava, and L. E. Kavraki, \"Using local experiences for global motion planning\", in IEEE International Conference on Robotics and Automation (ICRA), 2019.

C. Chamzas et al., \"Learning sampling distributions using local 3d workspace decompositions for motion planning in high dimensions\" in IEEE International Conference on Robotics and Automation (ICRA), 2021.

C. Zhang, J. Huh, and D. D. Lee, \"Learning implicit sampling distributions for motion planning,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2018.

T. Lai and F. Ramos, "Adaptively Exploits Local Structure With Generalised Multi-Trees Motion Planning," IEEE Robotics and Automation Letters (RAL), vol. 7, no. 2, pp. 1111--1117, Apr. 2022.

M. Faroni and D. Berenson, "Motion Planning as Online Learning: A Multi-Armed Bandit Approach to Kinodynamic Sampling-Based Planning," IEEE Robotics and Automation Letters (RAL), vol. 8, no. 10, pp. 6651--6658, Oct. 2023.

M. Likhachev and D. Ferguson, "Planning Long Dynamically Feasible Maneuvers for Autonomous Vehicles," The International Journal of Robotics Research (IJRR), vol. 28, no. 8, pp. 933--945, Jun. 2009.

M. Rufli, D. Ferguson, and R. Siegwart, \"Smooth path planning in constrained environments,\" in IEEE International Conference on Robotics and Automation (ICRA), 2009.

J. Ichnowski, R. Alterovitz, \"Multilevel incremental roadmap spanners for reactive motion planning,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2019.

V. N. Hartmann, et al. \"Effort informed roadmaps (EIRM$^*$): Efficient asymptotically optimal multiquery planning by actively reusing validation effort,\" The International Symposium of Robotics Research. Cham: Springer Nature Switzerland, 2022.

W. Du, F. Islam, and M. Likhachev, \"Multi-resolution A,\" Proceedings of the International Symposium on Combinatorial Search. Vol. 11. No. 1. 2020.

B. Saund and D. Berenson, "Fast planning over roadmaps via selective densification," IEEE Robotics and Automation Letters (RAL), vol. 5, no. 2, pp. 2873--2880, 2020.

J. A. Starek et al., \"An asymptotically-optimal sampling-based algorithm for bi-directional motion planning,\" in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2015.

J. J. Kuffner and S. M. LaValle, \"RRT-connect: An efficient approach to single-query path planning,\" in IEEE International Conference on Robotics and Automation (ICRA), 2000.

I. Pohl, "Heuristic search viewed as path finding in a graph," Artificial Intelligence, vol. 1, no. 3--4, pp. 193--204, Jan. 1970.

J. D. Gammell, T. D. Barfoot, and S. S. Srinivasa, "Batch Informed Trees (BIT\*): Informed asymptotically optimal anytime search," The International Journal of Robotics Research (IJRR), vol. 39, no. 5, pp. 543--567, Jan. 2020.

S. Choudhury, O. Salzman, S. Choudhury, and S. S. Srinivasa, "Densification strategies for anytime motion planning over large dense roadmaps," in IEEE International Conference on Robotics and Automation (ICRA), 2017.

A. Dobson and K. E. Bekris, "Sparse roadmap spanners for asymptotically near-optimal motion planning," The International Journal of Robotics Research (IJRR), vol. 33, no. 1, pp. 18--47, Jan. 2014.

I. A. Sucan, M. Moll, and L. E. Kavraki, "The Open Motion Planning Library," IEEE Robotics $\&$ Automation Magazine, vol. 19, no. 4, pp. 72--82, Dec. 2012.

E. Szczerbicki, L. Janson, and M. Pavone, "Optimal sampling-based motion planning under differential constraints: The driftless case," Europe PMC (PubMed Central), May 2015.

S. Karaman and E. Frazzoli, "Sampling-based optimal motion planning for non-holonomic dynamical systems," 2013 IEEE International Conference on Robotics and Automation, May 2013.
:::

[^1]: $^{1}$Lu Huang and Xingjian Jing are with the Department of Mechanical Engineering, City University of Hongkong, Tat Chee Avenue, Kowloon, Hong Kong SAR. `(e-mail: {lhuang98-c@my., xingjing@}cityu.edu.hk)`

[^2]: $^{2}$Lingxiao Meng and Jiankun Wang are with the Department of Electronic and Electrical Engineering, Southern University of Science and Technology, Shen Zhen, China. `(e-mail: {menglx2021@mail.,wangjk@}sustech.edu.cn)`

[^3]: For more detailed descriptions of the privileged coordinate box, please refer to [@DFMT; @KinodynamicRRTstar].
