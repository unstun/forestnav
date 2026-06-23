---
citation_key: Swedeen2023Batch
arxiv_id: 2302.11670
arxiv_url: https://arxiv.org/abs/2302.11670
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:33:50Z
origin: ai+web
reviewed: false
---

# Introduction

The ability to plan paths through complex obstacles is a fundamental requirement of many mobile robot applications and is an NP-complete problem in general [@Lavalle2006]. The literature has seen an explosive growth in sampling-based motion planning algorithms [@Gammell2014; @Hussain2015; @Nasir2013; @Noreen2016; @Yang2014] that provide asymptotic guarantees for this NP-complete problem. These algorithms operate on the principles of dynamic programming, breaking the problem into many smaller problems that can each be solved individually and then combined to make the overall solution.

Many sampling-based motion planning algorithms are based on Optimal Rapidly-exploring Random trees (RRT\*) [@Karaman2011]. RRT\* iteratively samples the continuous space it plans over building a root search tree from the initial robot location to every other reachable part of the obstacle-free space. As RRT\* searches, local optimizations are performed on the search tree shortening the length of the paths through the tree. As the number of iterations RRT\* performs goes to infinity, the resulting solution path from the initial location to the target location converges to optimality [@Karaman2011]. RRT\* and its variants have been shown to solve a large range of path planning problems rapidly. However, convergence can be slow [@Gammell2014; @Nasir2013; @Jeong2019].

Fast Marching Trees (FMT\*) is a sampling-based path planning algorithm that makes use of dynamic programming principles to avoid unnecessary calculations [@Janson2015]. FMT\* builds a rooted search tree similar to RRT\*. However, instead of iteratively sampling the state space and building the search tree simultaneously, FMT\* samples a fixed number of times before starting to build a search tree. Once all of the samples have been generated, FMT\* builds a search tree with the knowledge of the location of each sample from the beginning. Using this knowledge, FMT\* is able to avoid many of the calculations that RRT\* performs while locally optimizing its search tree. This makes FMT\* faster than RRT\* at generating a solution from a set number of samples. However, FMT\* is unable to continue refining its solution after that set number of samples. RRT\*, on the other hand, is purely iterative and will continue to refine its solution path for as long as it is allowed.

Batch Informed trees (BIT\*) combines the iterative nature of RRT\* with the efficient graph searching used in FMT\* [@Gammell2020]. BIT\* iteratively samples a batch of random samples from the configuration space, then it uses a procedure similar to FMT\* to incorporate the new batch of samples into the pre-existing search tree. The performance of BIT\* varies with the size of each batch of samples. When the batch size of BIT\* was just one, BIT\* is nearly equivalent to RRT\*. When the batch size is very large, BIT\* is nearly equivalent to FMT\* except for being able to sample subsequent batches of samples after the first is used. This allows the user of the algorithm to tune BIT\* to have the performance characteristics desired for a particular application.

The rest of this work proceeds as follows. Section [2](#sec:notation){reference-type="ref" reference="sec:notation"} describes general RRT\* and BIT\* notation used throughout this work. Section [3](#sec:bit){reference-type="ref" reference="sec:bit"} gives a thorough step-by-step explanation of the BIT\* algorithm. Section [4](#sec:demonstration){reference-type="ref" reference="sec:demonstration"} provides a demonstration of how BIT\* operates, graphically, over three batches of samples. Section [5](#sec:simulation){reference-type="ref" reference="sec:simulation"} provides averaged converges results using the Open Motion Planning Library (OMPL) and making comparisons to RRT\*.

# Notation and Background {#sec:notation}

Section [2.1](#sec:nomenclature){reference-type="ref" reference="sec:nomenclature"} describes the notation used throughout this work. Section [2.2](#sec:common_procedures){reference-type="ref" reference="sec:common_procedures"} defines some general helper procedures, to be used in the description of BIT\*.

## Nomenclature {#sec:nomenclature}

RRT\* and BIT\*-based algorithms iteratively construct a rooted, out-branching tree to find a path through the state space. The tree is an acyclic directed graph denoted as $T \triangleq \mathopen{}\mathclose\bgroup\left(V,E\aftergroup\egroup\right)$, where $V$ is the set of nodes or vertices within the tree and $E \subset V \times V$ denotes the set of edges between vertices. The root vertex has no parent while all other vertices have exactly one parent. Each vertex can have multiple children. Each vertex within $V$ corresponds to a state in the $d$-dimensional state space denoted as $X \subset \mathbb{R}^d$. The tree is initialized with solely the root node, i.e. $V = \mathopen{}\mathclose\bgroup\left\{x_{r}\aftergroup\egroup\right\}$, $E = \varnothing$. Nodes are added to the tree to find a path to the target set, $X_{t} \subset X$. The path must avoid the space blocked by obstacles, $X_{obs} \subset X$, staying within the obstacle-free space, $X_{free} \triangleq X \setminus X_{obs}$.

$\mathbb{R}$ is the set of all real numbers, and $\mathbb{R}_+$ is the set of all real positive numbers. The notation $X \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{x\aftergroup\egroup\right\}$ and $X \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{x\aftergroup\egroup\right\}$ is used to compactly represent the set updating operations $X \leftarrow X \setminus \mathopen{}\mathclose\bgroup\left\{x\aftergroup\egroup\right\}$ and $X \leftarrow X \cup \mathopen{}\mathclose\bgroup\left\{x\aftergroup\egroup\right\}$ respectively.

## Common Procedures {#sec:common_procedures}

In this section, a number of primitive sub-procedures are defined for use while describing BIT\*. We now define several generic procedures that can be found in [@Gammell2020; @Swedeen2023] with notation updated to match the sequel.

::: definition
**Definition 1** ($cost \leftarrow c\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x,y\aftergroup\egroup\aftergroup\egroup\right)$). *Calculates the length of the path in $X$ that connects $x \in X$ to $y \in X$. Note that $c$ returns infinity if the path is blocked by an obstacle.*
:::

::: definition
**Definition 2** ($cost \leftarrow \hat{c}\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x,y\aftergroup\egroup\aftergroup\egroup\right)$). *Calculates a lower bounded heuristic for the cost of the path that goes from $x \in X$ to $y \in X$, i.e., $0 \leq \hat{c}\mathopen{}\mathclose\bgroup\left(x,y\aftergroup\egroup\right) \leq c\mathopen{}\mathclose\bgroup\left(x,y\aftergroup\egroup\right) \leq \infty$. Note that $\hat{c}$ typically will not consider obstacles or have to generate the edge explicitly which makes it a fast operation. In the work $\hat{c}$ is defined using Euclidean distance as $\hat{c}\mathopen{}\mathclose\bgroup\left(x,y\aftergroup\egroup\right) := \mathopen{}\mathclose\bgroup\left\|x - y\aftergroup\egroup\right\|$.*
:::

::: definition
**Definition 3** ($cost \leftarrow g_T\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\aftergroup\egroup\right)$). *Calculates the cost-to-come from the root node to $x \in X$ through the tree, $T$. Note that if $x$ is not in the tree then $g_T\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) = \infty$.*
:::

::: definition
**Definition 4** ($cost \leftarrow \hat{g}\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\aftergroup\egroup\right)$). *Calculates a lower bounded heuristic for the cost-to-come of $x \in X$, i.e., $0 \leq \hat{g}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) \leq g_T\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right)$. In this work $\hat{g}$ is defined using the edge cost heuristic as $\hat{g}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) := \hat{c}\mathopen{}\mathclose\bgroup\left(x_r, x\aftergroup\egroup\right)$, where $x_r$ is the initial state of the path planning problem.*
:::

::: {#def:h_hat .definition}
**Definition 5** ($cost \leftarrow \hat{h}\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\aftergroup\egroup\right)$). *Calculates a lower bounded heuristic for the cost-to-go of $x \in X$. In this work $\hat{h}$ is again defined using edge cost heuristic as $\hat{h}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) := \hat{c}\mathopen{}\mathclose\bgroup\left(x, x_t\aftergroup\egroup\right)$, where $x_t \in V$ is the end of the best solution that has been found by the planner so far.*
:::

::: definition
**Definition 6** ($X_{rand} \leftarrow Sample\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(m\aftergroup\egroup\aftergroup\egroup\right)$). *Generates a set of $m \in \mathbb{R}_+$ random samples of the obstacle-free state set, $X_{free}$[^1]. The sampling is an independent, identically, and uniformly distributed (i.i.u.d.) sample of $X_{free}$[^2].*
:::

::: definition
**Definition 7** ($X_{near} \leftarrow Near_{\rho}\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x,X_{search}\aftergroup\egroup\aftergroup\egroup\right)$). *Finds all vertices in $X_{search}$ that are within a given edge cost radius[^3], $\rho \in \mathbb{R}_+$, of the point $x \in X$, i.e. $$\begin{equation*}
          Near_{\rho}\mathopen{}\mathclose\bgroup\left(x,X_{search}\aftergroup\egroup\right) := \mathopen{}\mathclose\bgroup\left\{ v \in X_{search} \middle| c\mathopen{}\mathclose\bgroup\left(x, v\aftergroup\egroup\right) \leq \rho \aftergroup\egroup\right\}.
\end{equation*}$$*
:::

::: definition
**Definition 8** ($X_{sol} \leftarrow Solution\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\aftergroup\egroup\right)$). *Finds the path through $T\triangleq\mathopen{}\mathclose\bgroup\left(V,E\aftergroup\egroup\right)$, $X_{sol} \subset V$, that leads from the root node to $x \in V$.*
:::

::: definition
**Definition 9** ($x_{p} \leftarrow Par\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x_{c}\aftergroup\egroup\aftergroup\egroup\right)$). *Returns the parent node of $x_{c} \in V$ in the tree $T\triangleq\mathopen{}\mathclose\bgroup\left(V,E\aftergroup\egroup\right)$, or $\varnothing$ if $x_{c}$ is the root node.*
:::

::: definition
**Definition 10** ($X_{children} \leftarrow Children\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(x_{p}\aftergroup\egroup\aftergroup\egroup\right)$). *Returns every node from the set $V$ in $T\triangleq\mathopen{}\mathclose\bgroup\left(V,E\aftergroup\egroup\right)$ that has $x_{p}$ as its parent.*
:::

::: definition
**Definition 11** ($cost \leftarrow BestValue\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(\mathcal{Q}_i\aftergroup\egroup\aftergroup\egroup\right)$). *Finds the element in $\mathcal{Q}_i$ with the lowest queue cost and returns the queue cost of that element.*
:::

::: definition
**Definition 12** ($x \leftarrow PopBest\mathopen{}\mathclose\bgroup\mathopen{}\mathclose\bgroup\left(\mathcal{Q}_i\aftergroup\egroup\aftergroup\egroup\right)$). *Finds the element in $\mathcal{Q}_i$ with the lowest queue cost, removes it from the queue, and returns that element.*
:::

# Batch Informed Trees {#sec:bit}

::: algorithm
$V \leftarrow \mathopen{}\mathclose\bgroup\left\{x_r\aftergroup\egroup\right\}$; []{#alg:bit:start_init label="alg:bit:start_init"} $E \leftarrow \varnothing$; $T \triangleq \mathopen{}\mathclose\bgroup\left(V,E\aftergroup\egroup\right)$ $\mathcal{Q}_V \leftarrow V$; $\mathcal{Q}_E \leftarrow \varnothing$; $\mathcal{Q} \triangleq \mathopen{}\mathclose\bgroup\left(\mathcal{Q}_V,\mathcal{Q}_E\aftergroup\egroup\right)$ []{#alg:bit:init_queues label="alg:bit:init_queues"} $X_{ncon} \leftarrow X_{goal}$; []{#alg:bit:start_init_flags label="alg:bit:start_init_flags"} $X_{new} \leftarrow X_{ncon}$ $V_{exp} \leftarrow \varnothing$; $V_{rewire} \leftarrow \varnothing$; $V_{sol} \leftarrow V \cap X_t$ $X_{flags} \triangleq \mathopen{}\mathclose\bgroup\left(X_{new},V_{exp},V_{rewire},V_{sol},c_{sol}\aftergroup\egroup\right)$ []{#alg:bit:end_init label="alg:bit:end_init"}

[]{#alg:bit:start_loop label="alg:bit:start_loop"} ()$\mathcal{Q}_V = \varnothing \land \mathcal{Q}_E = \varnothing$ []{#alg:bit:end_batch label="alg:bit:end_batch"} $\mathopen{}\mathclose\bgroup\left\{X_{reuse},T,X_{ncon},X_{flags}\aftergroup\egroup\right\} \leftarrow Prune\mathopen{}\mathclose\bgroup\left(T,X_{ncon},X_{flags}\aftergroup\egroup\right)$ []{#alg:bit:call_prune label="alg:bit:call_prune"} $X_{new} \leftarrow Sample\mathopen{}\mathclose\bgroup\left(m\aftergroup\egroup\right)$ []{#alg:bit:sample label="alg:bit:sample"} $X_{ncon} \xleftarrow{+} X_{new} \cup X_{reuse}$ []{#alg:bit:start_add_samples label="alg:bit:start_add_samples"} $\mathcal{Q}_V \leftarrow V$ []{#alg:bit:update_vert_queue label="alg:bit:update_vert_queue"} []{#alg:bit:queues_cond label="alg:bit:queues_cond"} $\mathopen{}\mathclose\bgroup\left\{\mathcal{Q},X_{flags}\aftergroup\egroup\right\} \leftarrow ExpVertex\mathopen{}\mathclose\bgroup\left(T,\mathcal{Q},X_{ncon},X_{flags}\aftergroup\egroup\right)$ []{#alg:bit:exp_vert label="alg:bit:exp_vert"} () $\mathopen{}\mathclose\bgroup\left\{T,\mathcal{Q},X_{ncon},X_{flags}\aftergroup\egroup\right\} \leftarrow ExpEdge\mathopen{}\mathclose\bgroup\left(T,\mathcal{Q},X_{ncon},X_{flags},X_t\aftergroup\egroup\right)$ []{#alg:bit:end_loop label="alg:bit:end_loop"}

$Solution\mathopen{}\mathclose\bgroup\left(\mathop{\mathrm{arg\,min}}_{v_t \in V_{sol}} g_T\mathopen{}\mathclose\bgroup\left(v_t\aftergroup\egroup\right)\aftergroup\egroup\right)$;
:::

BIT\* functions by iteratively generating batches of samples from the state space and incorporating those new samples into the pre-existing search tree. To achieve this BIT\* defines two sorted queues, the vertex queue and the edge queue. At the beginning of each batch, the vertex queue is populated with all of the nodes that are currently in the search tree. Vertices are then iteratively removed from the vertex queue and all potential edges that start from that vertex are added to the edge queue. Once all potential edges between samples of the state space have been found the search tree is updated to include them if doing so will shorten the length of the resulting path. Once both of the queues are empty a new batch is sampled and the process begins again.

Algorithm [\[alg:bit\]](#alg:bit){reference-type="ref" reference="alg:bit"} shows the BIT\* algorithm. The inputs are the root node, $x_r$, a sampling of the target set, $X_{goal} \subset X_t$, and the target set, $X_t \subset X_{free}$. Line [\[alg:bit:start_init\]](#alg:bit:start_init){reference-type="ref" reference="alg:bit:start_init"} initializes the search tree, $T$, with the root node, $x_r$, in its vertex set, $V$, and no edges in its edge set, $E$. Line [\[alg:bit:init_queues\]](#alg:bit:init_queues){reference-type="ref" reference="alg:bit:init_queues"} initializes the vertex queue, $\mathcal{Q}_V$, and the edge queue, $\mathcal{Q}_E$. $\mathcal{Q}_V$ is used to keep track of vertices that are under consideration for making potential edges and is organized in terms of the current cost-to-come plus the heuristic cost-to-go of the vertices, i.e., $$\begin{align}
      g_T\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right), v \in \mathcal{Q}_V.
\end{align}$$ $\mathcal{Q}_E$ is used to keep track of edges that are under consideration for addition to $T$. $\mathcal{Q}_E$ is organized in terms of the sum of the current cost-to-come of the source vertex of the edge, the heuristic cost of the edge, and the heuristic cost-to-go of the target vertex of the edge, i.e., $$\begin{align}
      g_T\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) + \hat{c}\mathopen{}\mathclose\bgroup\left(v,x\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right), \mathopen{}\mathclose\bgroup\left(v,x\aftergroup\egroup\right) \in \mathcal{Q}_E.
\end{align}$$ Lines [\[alg:bit:start_init_flags\]](#alg:bit:start_init_flags){reference-type="ref" reference="alg:bit:start_init_flags"} through [\[alg:bit:end_init\]](#alg:bit:end_init){reference-type="ref" reference="alg:bit:end_init"} initialize a few sets that are needed to keep track of the state of each vertex. $X_{ncon} \subset X$ is the set of all samples that are not connected to the search tree. Note that $X_{ncon}$ is initialized with the provided samples of the target set, $X_{goal}$. $V_{sol} = V \cap X_t$ is the set of vertices in $V$ that are also in the target set $X_t$. $X_{new} \subset X_{ncon}$ is the set of samples that are from the most recent batch of samples. $V_{nexp} \subset V$ is the set of vertices that have not been considered for expansion. $V_{nrewire} \subset V$ is the set of vertices that have not been considered for rewiring. $c_i$ is the cost of the current best solution.

The loop on lines [\[alg:bit:start_loop\]](#alg:bit:start_loop){reference-type="ref" reference="alg:bit:start_loop"} through [\[alg:bit:end_loop\]](#alg:bit:end_loop){reference-type="ref" reference="alg:bit:end_loop"} performs the rest of the planning process and ends when a user-defined stopping condition is met[^4]. The conditionals on lines [\[alg:bit:end_batch\]](#alg:bit:end_batch){reference-type="ref" reference="alg:bit:end_batch"} and [\[alg:bit:queues_cond\]](#alg:bit:queues_cond){reference-type="ref" reference="alg:bit:queues_cond"} determine if the batch has ended and whether to process a vertex from $\mathcal{Q}_V$ or an edge from $\mathcal{Q}_E$, respectively. Each case is discussed below.

## Generating New Batches

::: algorithm
$X_{reuse} \leftarrow \varnothing$ $X_{ncon} \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{x \in X_{ncon} \middle| \hat{g}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) \geq c_{sol}\aftergroup\egroup\right\}$ []{#alg:prune:ncon label="alg:prune:ncon"} []{#alg:prune:tree_loop label="alg:prune:tree_loop"} []{#alg:prune:cur_tree label="alg:prune:cur_tree"} $V \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{v\aftergroup\egroup\right\}$; $E \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{\mathopen{}\mathclose\bgroup\left(Par\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right),v\aftergroup\egroup\right)\aftergroup\egroup\right\}$ $X_t \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{v\aftergroup\egroup\right\}$; $X_{exp} \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{v\aftergroup\egroup\right\}$; $X_{rewire} \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{v\aftergroup\egroup\right\}$ []{#alg:prune:final_con label="alg:prune:final_con"} $X_{reuse} \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{v\aftergroup\egroup\right\}$ []{#alg:prune:tree_loop_end label="alg:prune:tree_loop_end"}

$\mathopen{}\mathclose\bgroup\left\{X_{reuse},T,X_{ncon},X_{flags}\aftergroup\egroup\right\}$;
:::

When $\mathcal{Q}_V$ and $\mathcal{Q}_E$ are both empty it signifies the end of the batch, see line [\[alg:bit:end_batch\]](#alg:bit:end_batch){reference-type="ref" reference="alg:bit:end_batch"} of Algorithm [\[alg:bit\]](#alg:bit){reference-type="ref" reference="alg:bit"}. When that happens, all vertices that cannot contribute to the optimal solution are removed from the search tree, $T$, by calling the $Prune$ procedure on line [\[alg:bit:call_prune\]](#alg:bit:call_prune){reference-type="ref" reference="alg:bit:call_prune"}.

The $Prune$ procedure is given in Algorithm [\[alg:prune\]](#alg:prune){reference-type="ref" reference="alg:prune"}. Line [\[alg:prune:ncon\]](#alg:prune:ncon){reference-type="ref" reference="alg:prune:ncon"} of Algorithm [\[alg:prune\]](#alg:prune){reference-type="ref" reference="alg:prune"} removes all unconnected samples with heuristic cost-to-come plus heuristic cost-to-go value greater than the current best solution. Note that this can be thought of as removing all nodes that fall outside of the "informed set" that Informed RRT\* (I-RRT\*) defines[@Gammell2014] and as such provably cannot contribute to the optimal solution. The loop on lines [\[alg:prune:tree_loop\]](#alg:prune:tree_loop){reference-type="ref" reference="alg:prune:tree_loop"} though [\[alg:prune:tree_loop_end\]](#alg:prune:tree_loop_end){reference-type="ref" reference="alg:prune:tree_loop_end"} removes any vertices in the search tree that cannot contribute to the optimal solution. Line [\[alg:prune:cur_tree\]](#alg:prune:cur_tree){reference-type="ref" reference="alg:prune:cur_tree"} checks if each vertex in the tree has the potential to contribute to the optimal solution given its current connection to the search tree. If this check fails, the vertex is removed from the search tree. Line [\[alg:prune:final_con\]](#alg:prune:final_con){reference-type="ref" reference="alg:prune:final_con"} checks if the vertex has the potential to contribute to the optimal solution given the ideal cost-to-come. This is effectively the same condition that is used on line [\[alg:prune:ncon\]](#alg:prune:ncon){reference-type="ref" reference="alg:prune:ncon"}. If there is a chance of the sample contributing to the optimal solution, the vertex is added to $X_{reuse}$ to be reused as an unconnected sample in the next batch. $X_{reuse}$ is added to the algorithm to maintain uniform sample density in the "informed set".

After $Prune$ is finished, line [\[alg:bit:sample\]](#alg:bit:sample){reference-type="ref" reference="alg:bit:sample"} of Algorithm [\[alg:bit\]](#alg:bit){reference-type="ref" reference="alg:bit"} generates $m$ *new* samples of the obstacle-free state space, $X_{free}$. Line [\[alg:bit:start_add_samples\]](#alg:bit:start_add_samples){reference-type="ref" reference="alg:bit:start_add_samples"} adds the new samples and reused vertices to $X_{ncon}$. Line [\[alg:bit:update_vert_queue\]](#alg:bit:update_vert_queue){reference-type="ref" reference="alg:bit:update_vert_queue"} adds all vertices in the search tree to the vertex queue. This insures all vertices in the search tree will be considered when looking for ways to connect the new samples to the search tree.

## Expanding Vertices

::: algorithm
$v_b \leftarrow PopBest\mathopen{}\mathclose\bgroup\left(\mathcal{Q}_V\aftergroup\egroup\right)$ []{#alg:exp_v:pop label="alg:exp_v:pop"} []{#alg:exp_v:first_time_cond label="alg:exp_v:first_time_cond"} $V_{exp} \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{v_b\aftergroup\egroup\right\}$ $X_{near} \leftarrow Near_{\rho}\mathopen{}\mathclose\bgroup\left(v_b,X_{ncon}\aftergroup\egroup\right)$ []{#alg:exp_v:all_uncon_search label="alg:exp_v:all_uncon_search"} () $X_{near} \leftarrow Near_{\rho}\mathopen{}\mathclose\bgroup\left(v_b,X_{new} \cap X_{ncon}\aftergroup\egroup\right)$ []{#alg:exp_v:new_uncon_search label="alg:exp_v:new_uncon_search"} $\mathcal{Q}_E \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{\mathopen{}\mathclose\bgroup\left(v_b,x\aftergroup\egroup\right), x \in X_{near} \middle| \hat{g}\mathopen{}\mathclose\bgroup\left(v_b\aftergroup\egroup\right) + \hat{c}\mathopen{}\mathclose\bgroup\left(v_b,x\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right) < c_{sol}\aftergroup\egroup\right\}$ []{#alg:exp_v:exp_edges label="alg:exp_v:exp_edges"} []{#alg:exp_v:rewire_cond label="alg:exp_v:rewire_cond"} $V_{rewire} \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{v_b\aftergroup\egroup\right\}$ $V_{near} \leftarrow Near_{\rho}\mathopen{}\mathclose\bgroup\left(v_b,V\aftergroup\egroup\right)$ []{#alg:exp_v:in_tree_search label="alg:exp_v:in_tree_search"} $\begin{aligned}
            \mathcal{Q}_E \xleftarrow{+}
              &\mathopen{}\mathclose\bgroup\left\{
                \mathopen{}\mathclose\bgroup\left(v_b,w\aftergroup\egroup\right), w \in V_{near} \middle| \aftergroup\egroup\right.
                   \mathopen{}\mathclose\bgroup\left(v_b,w\aftergroup\egroup\right) \not\in E, \\
                  &\hat{g}\mathopen{}\mathclose\bgroup\left(v_b\aftergroup\egroup\right) + \hat{c}\mathopen{}\mathclose\bgroup\left(v_b,w\aftergroup\egroup\right) < g_T\mathopen{}\mathclose\bgroup\left(w\aftergroup\egroup\right), \\
                  &\mathopen{}\mathclose\bgroup\left. \hat{g}\mathopen{}\mathclose\bgroup\left(v_b\aftergroup\egroup\right) + \hat{c}\mathopen{}\mathclose\bgroup\left(v_b,w\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(w\aftergroup\egroup\right) < c_{sol}
              \aftergroup\egroup\right\};
          \end{aligned}$ []{#alg:exp_v:rewire_edges label="alg:exp_v:rewire_edges"}

$\mathopen{}\mathclose\bgroup\left\{\mathcal{Q},V_{flags}\aftergroup\egroup\right\}$;
:::

Lines [\[alg:bit:queues_cond\]](#alg:bit:queues_cond){reference-type="ref" reference="alg:bit:queues_cond"} and [\[alg:bit:exp_vert\]](#alg:bit:exp_vert){reference-type="ref" reference="alg:bit:exp_vert"} of Algorithm [\[alg:bit\]](#alg:bit){reference-type="ref" reference="alg:bit"} find potential edges to add to $\mathcal{Q}_E$ from the vertices in $\mathcal{Q}_V$. The condition on line [\[alg:bit:queues_cond\]](#alg:bit:queues_cond){reference-type="ref" reference="alg:bit:queues_cond"} evaluates to true until it is impossible for the best vertex in $\mathcal{Q}_V$ to produce an edge of lower heuristic cost then the best edge in $\mathcal{Q}_E$. This can be seen by noting that $$\begin{align}
        \forall v \in \mathcal{Q}_V, \forall x \in X, g_T\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) \leq g_T\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) + \hat{c}\mathopen{}\mathclose\bgroup\left(v,x\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right)
\end{align}$$ as $\hat{h}\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right)$ is an under estimate of the true cost-to-go of vertex $v$. Thus, the vertex queue cost, $g_T\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right)$, is a lower bound on the edge queue cost, $g_T\mathopen{}\mathclose\bgroup\left(v\aftergroup\egroup\right) + \hat{c}\mathopen{}\mathclose\bgroup\left(v,x\aftergroup\egroup\right) + \hat{h}\mathopen{}\mathclose\bgroup\left(x\aftergroup\egroup\right)$ of any edge that can be made from that vertex.

$ExpVertex$ removes the lowest cost vertex in $\mathcal{Q}_V$ and adds edges to $\mathcal{Q}_E$ for every neighbor that might be part of the optimal solution. The $ExpVertex$ procedure is given in Algorithm [\[alg:exp_v\]](#alg:exp_v){reference-type="ref" reference="alg:exp_v"}. Line [\[alg:exp_v:pop\]](#alg:exp_v:pop){reference-type="ref" reference="alg:exp_v:pop"} of Algorithm [\[alg:exp_v\]](#alg:exp_v){reference-type="ref" reference="alg:exp_v"} pops the lowest cost vertex in $\mathcal{Q}_V$. Lines [\[alg:exp_v:first_time_cond\]](#alg:exp_v:first_time_cond){reference-type="ref" reference="alg:exp_v:first_time_cond"} through [\[alg:exp_v:exp_edges\]](#alg:exp_v:exp_edges){reference-type="ref" reference="alg:exp_v:exp_edges"} adds edges to $\mathcal{Q}_E$ that start from $v_b$ and go to samples that are not connected to the tree. The condition on line [\[alg:exp_v:first_time_cond\]](#alg:exp_v:first_time_cond){reference-type="ref" reference="alg:exp_v:first_time_cond"} checks if this is the first time $v_b$ has been considered for expansion. In that case, all unconnected samples are considered for connection to $v_b$, see line [\[alg:exp_v:all_uncon_search\]](#alg:exp_v:all_uncon_search){reference-type="ref" reference="alg:exp_v:all_uncon_search"}. If it is not the first time $v_b$ has been considered for expansion, only the samples that are new this batch are considered for connection, see line [\[alg:exp_v:new_uncon_search\]](#alg:exp_v:new_uncon_search){reference-type="ref" reference="alg:exp_v:new_uncon_search"}. This prevents redundant calculations as the samples that are not new this batch have already been considered for connection to $v_b$. Once $X_{near}$ has been found, line [\[alg:exp_v:exp_edges\]](#alg:exp_v:exp_edges){reference-type="ref" reference="alg:exp_v:exp_edges"} adds all edges in the set $\mathopen{}\mathclose\bgroup\left\{\mathopen{}\mathclose\bgroup\left(v_b,x\aftergroup\egroup\right), x \in X_{near}\aftergroup\egroup\right\}$ that have potential to improve the current solution to $\mathcal{Q}_E$.

Lines [\[alg:exp_v:rewire_cond\]](#alg:exp_v:rewire_cond){reference-type="ref" reference="alg:exp_v:rewire_cond"} through [\[alg:exp_v:rewire_edges\]](#alg:exp_v:rewire_edges){reference-type="ref" reference="alg:exp_v:rewire_edges"} handle the case when $v_b$ might be a better parent for its neighbors then their current parent, i.e., rewiring. Note that if BIT\* has not found a solution the condition on line [\[alg:exp_v:rewire_cond\]](#alg:exp_v:rewire_cond){reference-type="ref" reference="alg:exp_v:rewire_cond"} will always evaluate to false. This is done to reduce the time it takes to find an initial solution to the problem by skipping any potential tree rewirings. Once the first solution is found, all rewirings that were skipped previously are considered. The condition on line [\[alg:exp_v:rewire_cond\]](#alg:exp_v:rewire_cond){reference-type="ref" reference="alg:exp_v:rewire_cond"} also evaluates to false if this is not the first time $v_b$ has been considered for rewiring. This prevents redundant calculations as the potential to perform rewirings around $v_b$ has already been considered. Line [\[alg:exp_v:in_tree_search\]](#alg:exp_v:in_tree_search){reference-type="ref" reference="alg:exp_v:in_tree_search"} finds all vertices in the search tree that are near $v_b$. Line [\[alg:exp_v:rewire_edges\]](#alg:exp_v:rewire_edges){reference-type="ref" reference="alg:exp_v:rewire_edges"} adds all edges from $v_b$ to $V_{near}$ that are not already part of the tree, have the potential to improve the cost of the neighbor, and have the potential to improve the current solution.

Note that everything done in $ExpVertex$ is done completely with heuristic values and without obstacle checking. This keeps the procedure computationally lightweight and fast.

## Evaluating Possible Edges

::: algorithm
$\mathopen{}\mathclose\bgroup\left(v_b,x_b\aftergroup\egroup\right) \leftarrow PopBest\mathopen{}\mathclose\bgroup\left(\mathcal{Q}_E\aftergroup\egroup\right)$ []{#alg:exp_e:pop label="alg:exp_e:pop"} []{#alg:exp_e:has_any_hope label="alg:exp_e:has_any_hope"} $\mathcal{Q}_E \leftarrow \varnothing$; $\mathcal{Q}_V \leftarrow \varnothing$ []{#alg:exp_e:clear label="alg:exp_e:clear"} $\mathopen{}\mathclose\bgroup\left\{T,\mathcal{Q},X_{ncon},X_{flags}\aftergroup\egroup\right\}$; ()$x_b \in X_{ncon}$ []{#alg:exp_e:rewire_cond label="alg:exp_e:rewire_cond"} []{#alg:exp_e:add_vert_cond label="alg:exp_e:add_vert_cond"} $X_{ncon} \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{x_b\aftergroup\egroup\right\}$; $V \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{x_b\aftergroup\egroup\right\}$; $E \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{\mathopen{}\mathclose\bgroup\left(v_b,x_b\aftergroup\egroup\right)\aftergroup\egroup\right\}$ $\mathcal{Q}_V \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{x_b\aftergroup\egroup\right\}$ []{#alg:exp_e:check_targ label="alg:exp_e:check_targ"} $V_{sol} \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{x_b\aftergroup\egroup\right\}$; []{#alg:exp_e:add_targ label="alg:exp_e:add_targ"} $c_{sol} \leftarrow \min_{v_{sol} \in V_{sol}} g_T\mathopen{}\mathclose\bgroup\left(v_{sol}\aftergroup\egroup\right)$ () []{#alg:exp_e:hur_imp_neih label="alg:exp_e:hur_imp_neih"} []{#alg:exp_e:help_sol_cond label="alg:exp_e:help_sol_cond"} []{#alg:exp_e:imp_neih label="alg:exp_e:imp_neih"} $E \xleftarrow{-} \mathopen{}\mathclose\bgroup\left\{\mathopen{}\mathclose\bgroup\left(Par\mathopen{}\mathclose\bgroup\left(x_b\aftergroup\egroup\right),x_b\aftergroup\egroup\right)\aftergroup\egroup\right\}$; $E \xleftarrow{+} \mathopen{}\mathclose\bgroup\left\{\mathopen{}\mathclose\bgroup\left(v_b,x_b\aftergroup\egroup\right)\aftergroup\egroup\right\}$ $c_{sol} \leftarrow \min_{v_{sol} \in V_{sol}} g_T\mathopen{}\mathclose\bgroup\left(v_{sol}\aftergroup\egroup\right)$

$\mathopen{}\mathclose\bgroup\left\{T,\mathcal{Q},X_{ncon},X_{flags}\aftergroup\egroup\right\}$;
:::

In the case that the best heuristic cost edge possible has been generated from $\mathcal{Q}_V$, the condition on line [\[alg:bit:queues_cond\]](#alg:bit:queues_cond){reference-type="ref" reference="alg:bit:queues_cond"} of Algorithm [\[alg:bit\]](#alg:bit){reference-type="ref" reference="alg:bit"} evaluates to false and $ExpEdge$ is called. $ExpEdge$ removes the most promising edge from $\mathcal{Q}_E$ and considers it for addition to the search tree.

The $ExpEdge$ procedure is given in Algorithm [\[alg:exp_e\]](#alg:exp_e){reference-type="ref" reference="alg:exp_e"}. Line [\[alg:exp_e:pop\]](#alg:exp_e:pop){reference-type="ref" reference="alg:exp_e:pop"} removes the lowest queue cost edge from $\mathcal{Q}_E$. Line [\[alg:exp_e:has_any_hope\]](#alg:exp_e:has_any_hope){reference-type="ref" reference="alg:exp_e:has_any_hope"} checks if there is a chance that the edge under consideration will improve the current solution. Note that this condition is true only if the most promising edge in $\mathcal{Q}_E$, and by extension all of the edges in $\mathcal{Q}_E$, cannot contribute to the optimal solution. For this reason $\mathcal{Q}_E$ and $\mathcal{Q}_V$ are cleared on line [\[alg:exp_e:clear\]](#alg:exp_e:clear){reference-type="ref" reference="alg:exp_e:clear"}.

Line [\[alg:exp_e:rewire_cond\]](#alg:exp_e:rewire_cond){reference-type="ref" reference="alg:exp_e:rewire_cond"} checks if $x_b$ is already in the tree. If $x_b$ is not part of the search tree, line [\[alg:exp_e:add_vert_cond\]](#alg:exp_e:add_vert_cond){reference-type="ref" reference="alg:exp_e:add_vert_cond"} checks if connecting $x_b$ to the tree through $v_b$ can improve the current solution. If it can, $x_b$ is added to the search tree with $v_b$ as its parent. Lines [\[alg:exp_e:check_targ\]](#alg:exp_e:check_targ){reference-type="ref" reference="alg:exp_e:check_targ"} and [\[alg:exp_e:add_targ\]](#alg:exp_e:add_targ){reference-type="ref" reference="alg:exp_e:add_targ"} check if $x_b$ is in the target set and adds $x_b$ to $V_{sol}$ if so. If $x_b$ is already part of the search tree at line [\[alg:exp_e:rewire_cond\]](#alg:exp_e:rewire_cond){reference-type="ref" reference="alg:exp_e:rewire_cond"}, extra checks are performed before adding the edge under consideration to the tree. Line [\[alg:exp_e:hur_imp_neih\]](#alg:exp_e:hur_imp_neih){reference-type="ref" reference="alg:exp_e:hur_imp_neih"} checks if connecting $x_b$ through $v_b$ can improve the cost of $x_b$. Line [\[alg:exp_e:help_sol_cond\]](#alg:exp_e:help_sol_cond){reference-type="ref" reference="alg:exp_e:help_sol_cond"} checks that the edge under consideration can improve the current solution. Line [\[alg:exp_e:imp_neih\]](#alg:exp_e:imp_neih){reference-type="ref" reference="alg:exp_e:imp_neih"} checks that connecting $x_b$ through $v_b$ will improve the cost of $x_b$. If all checks pass, $x_b$ is rewired to have $v_b$ as its parent and the current solution cost is updated if needed.

# Demonstration {#sec:demonstration}

=\[circle, draw=black!100, thick\] =\[circle, draw=black!100, fill=black!25,thick\] =\[circle, draw=green!100, fill=black!25,thick\] =\[regular polygon,regular polygon sides=4,draw=black!100, fill=black!25,thick\] =\[regular polygon,regular polygon sides=5,draw=black!100, fill=black!25,thick\] =\[regular polygon,regular polygon sides=4,draw=green!100, fill=black!25,thick\] =\[regular polygon,regular polygon sides=5,draw=green!100, fill=black!25,thick\] =\[circle, draw=green!100, thick\] =\[circle, draw=red!100, fill=black!25,thick\] =\[regular polygon,regular polygon sides=4,draw=red!100, fill=black!25,thick\] =\[cross out, draw=black!100, thick\]

:::: {#fig:bit_demo:batch0 .figure latex-placement="b"}
:::: {#fig:bit_demo:batch0:suba .figure}
::: caption
Lines [\[alg:bit:start_init\]](#alg:bit:start_init){reference-type="ref" reference="alg:bit:start_init"} through [\[alg:bit:end_init\]](#alg:bit:end_init){reference-type="ref" reference="alg:bit:end_init"} of Algorithm [\[alg:bit\]](#alg:bit){reference-type="ref" reference="alg:bit"} initialize the sets to have only the root node in $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch0:subb .figure}
::: caption
$x_r$ is the vertex with the lowest cost in $Q_V$ so it is removed from the queue and considered for expansion. $x_r$ does not have any neighbors so no edges are added to $Q_E$.
:::
::::

::: caption
Batch 0 of BIT\*.
:::
::::

:::: {#fig:bit_demo:batch1 .figure latex-placement="p"}
:::: {#fig:bit_demo:batch1:suba .figure}
::: caption
$Q_E$ and $Q_V$ are empty so a new batch of samples is made. Pruning is performed but has no effect until a solution is found. Samples A through E are generated. $Q_V$ is filled with all connected nodes.
:::
::::

:::: {#fig:bit_demo:batch1:subb .figure}
::: caption
The lowest cost vertex, $x_r$, is removed from $Q_V$ and used for expansion in $ExpVertex$. Edges $\alpha$ and $\beta$ pass the heuristic cost tests and are added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch1:subc .figure}
::: caption
The vertex queue is empty so the $ExpEdge$ procedure starts. $\alpha$ is the lowest cost edge in $Q_E$ so it is removed from $Q_E$ and, after passing all validity and cost tests, added to the tree. B is now connected to the tree and as such added to $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch1:subd .figure}
::: caption
The cost of B is less then the cost of $\beta$ so the $ExpVertex$ procedure is called. B is removed from $Q_V$ and edges $\gamma$ and $\delta$ are added to $Q_E$. Note that an edge is not made from B to $x_r$ because that edge fails the heuristic cost tests.
:::
::::

:::: {#fig:bit_demo:batch1:sube .figure}
::: caption
$Q_V$ is empty so we move to $ExpEdge$. Edge $\delta$ is removed from $Q_E$. $\delta$ passes the heuristic cost tests but fails the true cost tests because of the obstacle it passes through. $\delta$ is not added to the tree.
:::
::::

:::: {#fig:bit_demo:batch1:subf .figure}
::: caption
Edge $\beta$ is removed from $Q_E$ and, after passing all tests, added to the tree. Node D is now connected to the tree and added to $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch1:subg .figure}
::: caption
The cost of node D is less then $\gamma$ so $ExpVertex$ begins. Node D is removed from $Q_V$ and used for expansion. However, a solution has not been found so connected neighbors are not considered and D has no unconnected neighbors.
:::
::::

:::: {#fig:bit_demo:batch1:subh .figure}
::: caption
With $Q_V$ empty we move back $ExpEdge$. Edge $\gamma$ is removed from $Q_E$ but fails the heuristic cost tests so is not added to the tree.
:::
::::

::: caption
Batch 1 of BIT\*.
:::
::::

:::: {#fig:bit_demo:batch2 .figure latex-placement="p"}
:::: {#fig:bit_demo:batch2:suba .figure}
::: caption
$Q_E$ and $Q_V$ are empty so a new batch of samples is made. Samples F through J are generated. $Q_V$ is filled with all connected nodes.
:::
::::

:::: {#fig:bit_demo:batch2:subb .figure}
::: caption
In $ExpVertex$, $x_r$ is removed from $Q_V$. Because $x_r$ is still part of the expanded set from last batch, we only search over the new nodes for neighbors. Edge $\epsilon$ is added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch2:subc .figure}
::: caption
Node B is removed from $Q_V$. Node B has already been expanded so only edges to new nodes are considered. Edges $\eta$ and $\zeta$ are added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch2:subd .figure}
::: caption
Edge $\zeta$ has a lower heuristic cost then node D so $ExpEdge$ starts. Edge $\zeta$ is removed from $Q_E$ and, after passing all tests, added to the tree. Node F is now connected to the tree and added to $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch2:sube .figure}
::: caption
In $ExpVertex$, node F is removed from $Q_V$. Node F has not been expanded so edges to all unconnected nodes are considered. Edges $\lambda$, $\kappa$, $\theta$, and $\iota$ are added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch2:subf .figure}
::: caption
Edge $\theta$ has a lower heuristic cost then node D so $ExpEdge$ is called. Edge $\theta$ is removed from $Q_E$ and, after passing all tests, added to the tree. Node $x_t$ is now part of the tree and added to $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch2:subg .figure}
::: caption
Node $x_t$ has a lower heuristic cost then edge $\epsilon$ so $ExpVertex$ is used. Node $x_t$ is removed from $Q_V$. Node $x_t$ has not been expanded so edges to all near nodes are considered. Edges from $x_t$ to nodes A and H fail to pass the heuristic cost test and as such can not improve the current solution, and are not added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch2:subh .figure}
::: caption
In $ExpEdge$, edge $\epsilon$ is removed from $Q_E$ and considered for addition to the tree. Edge $\epsilon$ fails the primary heuristic cost check, meaning that $\epsilon$ has no chance of improving the solution. The rest of the nodes and edges in $Q_V$ and $Q_E$ also can not help the solution so both queues are cleared. Note the orange ellipse that shows the informed set of states, and how G falls outside of the ellipse. This is a visual way of seeing why node G was not added to the tree.
:::
::::

:::: {#fig:bit_demo:batch2:subi .figure}
::: caption
Before generating batch 3, all nodes in the tree or unconnected are checked to make sure they fall within the informed ellipse. All that fall outside of the ellipse are pruned and not considered moving forward.
:::
::::

::: caption
Batch 2 of BIT\*.
:::
::::

:::: {#fig:bit_demo:batch3 .figure latex-placement="p"}
:::: {#fig:bit_demo:batch3:suba .figure}
::: caption
Nodes K through O are sampled from the informed ellipse. All connected nodes are added to $Q_V$. Note that node F is before $x_t$ because ties are broken based on true cost-to-come through the tree.
:::
::::

:::: {#fig:bit_demo:batch3:subb .figure}
::: caption
In $ExpVertex$, node $x_r$ is removed from $Q_V$. Node $x_r$ has been expanded but not rewired so only edges to new and connected nodes are considered. Edges $\mu$ and $\nu$ are added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch3:subc .figure}
::: caption
Edge $\mu$ has a lower heuristic cost then node B so we move to $ExpEdge$. Edge $\mu$ is removed from $Q_E$ and, after passing all tests added to the tree. Node L is now part of the tree and added to $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch3:subd .figure}
::: caption
In $ExpNode$, node L is removed from $Q_V$. The is the first time Node L is used for expansion so all non-pruned nodes are under consideration. Edges $\xi$, $\o$, and $\pi$ are added to $Q_E$. Edges from L to M, B, and A fail the heuristic cost test and are not added to $Q_E$.
:::
::::

:::: {#fig:bit_demo:batch3:sube .figure}
::: caption
Edge $\xi$ has a lower heuristic cost then node B so we move to $ExpEdge$. Edge $\xi$ is removed from $Q_E$ and, after passing all tests, added to the tree. Node N is now a part of the tree and added to $Q_V$.
:::
::::

:::: {#fig:bit_demo:batch3:subf .figure}
::: caption
In $ExpNode$, node N is removed from $Q_V$. Edges $\rho$, $\sigma$, and $\tau$ are added to $Q_E$. Edges from node N to nodes A, K, and B fail their heuristic cost tests. Note that $\sigma$ comes before $\rho$ because ties are broken based on true cost-to-come.
:::
::::

:::: {#fig:bit_demo:batch3:subg .figure}
::: caption
In $ExpEdge$, edge $\tau$ is removed from $Q_E$ and, after passing all tests, added to the tree. In order for node $x_t$ to only have one parent, edge $\theta$ is removed from the tree. Note that this changes the current solution cost and the informed ellipse.
:::
::::

:::: {#fig:bit_demo:batch3:subh .figure}
::: caption
Edge $\o$ is removed from $Q_E$ and considered for addition to the tree. Edge $\o$ fails the primary heuristic cost tests and is not added to the tree. $Q_V$ and $Q_E$ cleared and batch 2 ends.
:::
::::

:::: {#fig:bit_demo:batch3:subi .figure}
::: caption
Before generating batch 4, all nodes either in the tree or unconnected are checked to make sure they fall within the informed ellipse. All that fall outside of the ellipse are pruned and not considered moving forward.
:::
::::

::: caption
Batch 3 of BIT\*.
:::
::::

Figures [3](#fig:bit_demo:batch0){reference-type="ref" reference="fig:bit_demo:batch0"} through [32](#fig:bit_demo:batch3){reference-type="ref" reference="fig:bit_demo:batch3"} graphically show how BIT\* operates over three batches of samples. In this example, each batch consists of five samples, i.e., $m = 5$.

Figure [3](#fig:bit_demo:batch0){reference-type="ref" reference="fig:bit_demo:batch0"} shows what we call batch 0. This is the part of the planning process where the only node in $\mathcal{Q}_V$ is the root node and no samples have been made from the state space. This part of the algorithm checks for the trivial case where it is possible to directly connect the root node to the target set.

Figure [12](#fig:bit_demo:batch1){reference-type="ref" reference="fig:bit_demo:batch1"} shows the process of generating the first batch of samples and starting to build a search tree. Note that when batch 1 completes a path to the target set has not been found. This is a common occurrence in BIT\* where the search tree is unable to grow much until the sample density in $X_{free}$ grows for a few batches.

Figure [22](#fig:bit_demo:batch2){reference-type="ref" reference="fig:bit_demo:batch2"} shows how the second batch of samples is incorporated into the search tree. By the end of the batch a path to the target set has been found and the "informed ellipse" is defined. This enables pruning to be performed before batch 3 begins.

Figure [32](#fig:bit_demo:batch3){reference-type="ref" reference="fig:bit_demo:batch3"} shows how a new batch of samples is generated within the informed ellipse and used to refine the current solution. Note that as the solution length reduces in the third batch, the size of the informed ellipse also shrinks. This leads to more nodes being pruned and the search process becoming more focused on the area that can improve the current solution.

# Simulation {#sec:simulation}

Simulation results are now presented to demonstrate the effectiveness of the BIT\* algorithm. Comparisons are made between BIT\* and RRT\* planning with straight-lines.

## Simulation Details

:::: {#fig:uav_sim .figure latex-placement="tbh"}
![](Swedeen2023Batch_figs/uav_sim.png){width="80%"}

::: caption
The UAV simulation with Manhattan's buildings shown in red.
:::
::::

:::: {#fig:all_worlds .figure latex-placement="tbh"}
::: figure
:::

::: caption
The resulting paths from running BIT\* in the Manhattan world. The Path from BIT\* is shown in red.
:::
::::

To test the capabilities of BIT\*, it is used to plan paths for a simulated UAV through an urban environment. The UAV simulation is shown in Figure [33](#fig:uav_sim){reference-type="ref" reference="fig:uav_sim"}. The buildings in the UAV simulation are modeled off of the real buildings in Manhattan, New York. The placement and height of the buildings are from New York's Open Data project [@NycOpenData2016]. The initial position of the UAV is located in Central park. Maintaining an altitude of $10$ meters, the UAV plans a path through the buildings to the goal location on Governors Island.

While planning a path, obstacles are represented with an occupancy grid with each pixel corresponding to ten square centimeters. Every building that is taller than $10 m$ is considered an obstacle in the occupancy grid. Figure [34](#fig:all_worlds){reference-type="ref" reference="fig:all_worlds"} shows the resulting occupancy grid with black representing obstacles. The occupancy grid covers a $10.7 km \times 5.65 km$ area of Manhattan. The initial location of the UAV in the coordinate frame used for this problem is $x_r = \begin{bmatrix} 0 & 0 \end{bmatrix} km$, with the UAV orientation defined in the direction of the target set. The target set, $X_{t}$, is a circle of radius $0.001m$ centered at $\begin{bmatrix} -9 & -3.8 \end{bmatrix} km$. The samples of the target set that are provided to BIT\*, $X_{goal}$, is the singleton set of the center of $X_t$. The neighborhood search radius, $\rho$, is $500 m$. Paths are generated and checked for obstacles four times per every meter of path length. When using BIT\*, the batch size, $m$, is set to $1500$ samples.

When using RRT\* there are three additional parameters, $\eta$, $\alpha$, and $b_t$, that are described in [@Swedeen2023] but only given values here for brevity. The steering constant, $\eta$, is $500 m$. The max number of neighbors to search, $\alpha$, is $100$ neighbors. The check target period, $b_t$, is $1$ out of every $50$ samples.

Results are gathered using the Open Motion Planning Library (OMPL) [@Moll2015]. As the sampling is random, each simulation consists of over 100 individual simulations with the average results being presented. The results were gathered on an AMD Ryzen Threadripper 3970X processor. Convergence plots were made by fitting a 15^th^-order polynomial using a least-squares fitting algorithm as described in [@Venables2002].

A least-squares approach is used as the sampling times for path length are not uniform across all simulations and not all simulations find the initial path at the same time. Note that while the path length for any one run will be monotonically decreasing with time, the least squares fitted plot does not always have the same monotonic property. The reason is that a particular run may not find a solution until well after other runs and the initial solution it finds may be much larger than the current solution of the other runs, effectively causing the average to increase at the time the run first produces path length data.

Simulation code can be found in our open-source repository <https://gitlab.com/utahstate/robotics/fillet-rrt-star> .

## Results

:::: {#fig:transients .figure latex-placement="tbh"}
::: caption
The convergence plots of the Manhattan world over 5 minutes. RRT\* and BIT\* planning with straight-line motion primitives are shown in blue and red respectively.
:::
::::

The convergence results from benchmarking RRT\* and BIT\* in the Manhattan environment are shown in Figure [35](#fig:transients){reference-type="ref" reference="fig:transients"}. RRT\* and BIT\* are shown in blue and red respectively. Clearly BIT\* outperforms RRT\* in terms of converging to a near optimal-value rapidly. BIT\* initially finds a solution much shorter than RRT\* and proceeds to converge to near optimality by the time 30 seconds have passed. This comes from BIT\*'s use of cost-to-come and cost-to-go heuristics to focus their search efforts in directions that are most likely to improve the solution cost. RRT\* on the other hand starts with a long initial solution. Despite converging for five minutes, the solution that RRT\* produces is still substantially longer than that of BIT\*.

[^1]: *Because it is computationally expensive to uniformly sample an arbitrary set, all of $X$ is sampled instead and the sample is discarded and re-sampled if it happens to be in the obstacle set.*

[^2]: *It is important that the sampling of $X_{free}$ is i.i.u.d. to guarantee asymptotic optimality [@Karaman2011].*

[^3]: *In this work $\rho$ is held constant, but many sampling-based algorithms vary $\rho$ as the algorithm runs [@Karaman2011].*

[^4]: Common stopping conditions include achieving a desirable solution cost or expending the extent of the planning time given.
