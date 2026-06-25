---
citation_key: Salzman2013Asymptotically
arxiv_id: 1308.0189
arxiv_url: https://arxiv.org/abs/1308.0189
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:21:41Z
origin: ai+web
reviewed: false
---

# Introduction and related work

Motion planning is a fundamental research topic in robotics with applications in diverse domains such as surgical planning, computational biology, autonomous exploration, search-and-rescue, and warehouse management. Sampling-based planners such as PRM [@KSLO96], RRT [@KL00] and their many variants enabled solving motion-planning problems that had been previously considered infeasible [@CBHKKLT05 C.7]. Recently, there is growing interest in the robotics community in finding *high-quality* paths, which turns out to be a non-trivial problem [@KF11; @NRH10]. Quality can be measured in terms of, for example, length, clearance, smoothness, energy, to mention a few criteria, or some combination of the above.

## High-quality planning with sampling-based algorithms

Unfortunately, planners such as RRT and PRM produce solutions that may be far from optimal [@KF11; @NRH10]. Thus, many variants of these algorithms and heuristics were proposed in order to produce high-quality paths.

**Post-processing existing paths:** Post-processing an existing path by applying *shortcutting* is a common, effective, approach to increase path quality; see, e.g., [@GO07]. Typically, two non-consecutive configurations are chosen randomly along the path. If the two configurations can be connected using a straight-line segment in the configuration space and this connection improves the quality of the original path, the segment replaces the original path that connected the two configurations. The process is continued iteratively until a termination condition holds.

**Path hybridization:** An inherent problem with path post-processing is that it is local in nature. A path that was post-processed using shortcutting often remains in the same homotopy class of the original path. Carefully combining even a small number of different paths (that may be of low quality) often enables the construction of a higher-quality path [@REH11].

**Online optimization:** Changing the sampling strategy [@ABDJV98; @LTA03; @US03; @SWT09], or the connection scheme to a new milestone [@US03; @SLN00] are examples of heuristics proposed to create higher-quality solutions. Additional approaches include, among others, useful cycles [@GO07] and random restarts [@WB08].

**Asymptotically optimal and near-optimal solutions:** In their seminal work, Karaman and Frazzoli [@KF11] give a rigorous analysis of the performance of the RRT and PRM algorithms. They show that with probability one, the algorithms will not produce the optimal path. By modifying the connection scheme of a new sample to the existing data structure, they propose the PRM\* and the RRG and RRT\* algorithms (variants of the PRM and RRT algorithms, respectively) all of which are shown to be *asymptotically optimal*. Namely, as the number of samples tends to infinity, the solution obtained by these algorithms converges to the optimal solution with probability one. To ensure asymptotic optimality, the number of nodes each new sample is connected to is proportional to $\log (n)$ (here $n$ is the number of free samples).

As PRM\* may produce prohibitively large graphs, recent work has focused on sparsifying these graphs. This can be done as a post-processing stage of the PRM\* [@SSAH14; @MB11-IROS], or as a modification of PRM\* [@MB11-ISRR; @MB12; @DB14].

The performance of RRT\* can be improved using several heuristics that bear resemblance to the lazy approach used in this work [@PKSFTW11]. Additional heuristics to speed up the convergence rate of RRT\* were presented in RRT\*-SMART [@INMAH13]. Recently, RRT$^\#$ [@AT13] was suggested as an asymptotically-optimal algorithm with a faster convergence rate when compared to RRT\*. RRT$^\#$ extends its roadmap in a similar fashion to RRT\* but adds a replanning procedure. This procedure ensures that the tree rooted at the initial state contains lowest-cost path information for vertices which have the potential to be part of the optimal solution. Thus, in contrast to RRT\* which only performs *local* rewiring of the search tree, RRT$^\#$ efficiently propagates changes to *all* the relevant parts of the roadmap. Janson and Pavone [@JP13] introduced the asymptotically-optimal Fast Marching Tree algorithm (FMT\*). The single-query asymptotically-optimal algorithm maintains a tree as its roadmap. Similarly to PRM\*, FMT\* samples $n$ collision-free nodes. It then builds a minimum-cost spanning tree rooted at the initial configuration over this set of nodes (see Section [\[sec:fmt\]](#sec:fmt){reference-type="ref" reference="sec:fmt"} for further details). Lazy variants have been proposed both for PRM\* and RRG [@LH14] and for FMT\* [@SH14-arxiv].

An alternative approach to improve the running times of these algorithms is to relax the asymptotic optimality to *asymptotic near-optimality*. An algorithm is said to be asymptotically near-optimal if, given an *approximation factor* $\varepsilon$, the solution obtained by the algorithm converges to within a factor of $(1+\varepsilon)$ of the optimal solution with probability one, as the number of samples tends to infinity. Similar to this work, yet using different methods, Littlefield et al. [@LLB13] recently presented an asymptotic near-optimal variant of RRT\* for systems with dynamics. Their approach however, requires setting different parameters used by their algorithm.

**Anytime and online solutions:** An interesting variant of the basic motion-planning problem is anytime motion-planning: In this problem, the time to plan is not known in advance, and the algorithm may be terminated at any stage. Clearly, any solution should be found as fast as possible and if time permits, it should be refined to yield a higher-quality solution.

Ferguson and Stentz [@FS06] suggest iteratively running RRT while considering only areas that may potentially improve the existing solution. Alterovitz et al. [@APD11] suggest the Rapidly-exploring Roadmap Algorithm (RRM), which finds an initial path similar to RRT. Once such a path is found, RRM either explores further the configuration space or refines the explored space. Luna et al. [@LSMK13] suggest alternating between path shortcutting and path hybridization in an anytime fashion.

RRT\* was also adapted for online motion planning [@KWPFT11]. Here, an initial path is computed and the robot begins its execution. While the robot moves along this path, the algorithm refines the part that the robot has not yet moved along.

## Contribution

We present LBT-RRT, a single-query sampling-based algorithm that is *asymptotically near-optimal*. Namely, the solution extracted from LBT-RRT converges to a solution that is within a factor of $(1+\varepsilon)$ of the optimal solution. LBT-RRT allows for interpolating between the fast, yet sub-optimal, RRT algorithm and the asymptotically-optimal RRG algorithm. By choosing $\varepsilon = 0$ no approximation is allowed and LBT-RRT maintains a roadmap identical to the one maintained by RRG. Choosing $\varepsilon = \infty$ allows for any approximation and LBT-RRT maintains a tree identical to the tree maintained by RRT.

The asymptotic near-optimality of LBT-RRT is achieved by simultaneously maintaining two roadmaps. Both roadmaps are defined over the same set of vertices but each consists of a different set of edges. On the one hand, a path in the first roadmaps may not be feasible, but its cost is always a *lower bound* on the cost of paths extracted from RRG (using the same sequence of random nodes). On the other hand, a path extracted from the second roadmap is always feasible and its cost is within a factor of $(1+\varepsilon)$ from the lower bound provided by the first roadmap.

We suggest to use LBT-RRT for high-quality, anytime motion planning. We demonstrate its performance on scenarios ranging from 3 to 12 degrees of freedom (DoF) and show that the algorithm produces high-quality solutions (comparable to RRG and RRT\*) with little running-time overhead when compared to RRT.

This paper is a modified and extended version of a publication presented at the 2014 IEEE International Conference on Robotics and Automation [@SH14]. In this paper we present additional experiments and extensions of the original algorithmic framework. Finally, we note that the conference version of this paper contained an oversight with regard to the roadmap that is used for the lower bound. We explain the problem and its fix in detail in Section [3](#sec:alg){reference-type="ref" reference="sec:alg"} after providing all the necessary technical background.

## Outline

In Section [2](#sec:background){reference-type="ref" reference="sec:background"} we review the RRT, RRG and RRT\* algorithms. In Section [3](#sec:alg){reference-type="ref" reference="sec:alg"} we present our algorithm LBT-RRT and a proof of its asymptotic near-optimality. We continue in Section [4](#sec:eval){reference-type="ref" reference="sec:eval"} to demonstrate in simulations its favorable characteristics on several scenarios. In Section [5](#sec:extensions){reference-type="ref" reference="sec:extensions"} we discuss a modification of the framework to further speed up the convergence to high-quality solutions. We conclude in Section [6](#sec:con){reference-type="ref" reference="sec:con"} by describing possible directions for future work.

# Terminology and algorithmic background {#sec:background}

We begin this section by formally stating the motion-planning problem and introducing several standard procedures used by sampling-based algorithms. We continue by reviewing the RRT, RRG and RRT\* algorithms.

## Problem definition and terminology

We follow the formulation of the motion-planning problem as presented by Karaman and Frazzoli [@KF11]. Let $\ensuremath{\mathcal{X}}$ denote the configuration space (C-space), $\ensuremath{\mathcal{X}}_{\text{free}}$ and $\ensuremath{\mathcal{X}}_{\text{forb}}$ denote the free and forbidden spaces, respectively. Let $(\ensuremath{\ensuremath{\mathcal{X}}_{\text{free}}}, x_{\text{init}}, \ensuremath{\mathcal{X}}_{goal})$ be the motion-planning problem where: $x_{\text{init}} \in \ensuremath{\ensuremath{\mathcal{X}}_{\text{free}}}$ is an initial free configuration and $\ensuremath{\mathcal{X}}_{goal} \subseteq \ensuremath{\ensuremath{\mathcal{X}}_{\text{free}}}$ is the goal region. A *collision-free path* $\sigma : [0,1] \rightarrow \ensuremath{\ensuremath{\mathcal{X}}_{\text{free}}}$ is a continuous mapping to the free space. It is *feasible* if $\sigma(0)\!=\!x_{\text{init}}$ and $\sigma(1)\!\in\!X_{goal}$.

We will make use of the following procedures throughout the paper: `sample_free`, a procedure returning a random free configuration; `nearest_neighbor`$(x,V)$ and `nearest_neighbors`$(x,V,k)$ are procedures returning the nearest neighbor and $k$ nearest neighbors of $x$ within the set $V$, respectively. Let `steer`$(x,y)$ return a configuration $z$ that is closer to $y$ than $x$ is, `collision_free`$(x,y)$ tests if the straight line segment connecting $x$ and $y$ is contained in $\ensuremath{\mathcal{X}}_{\text{free}}$ and let `cost`$(x,y)$ be a procedure returning the cost of the straight-line path connecting $x$ and $y$. Let us denote by $\texttt{cost}_{\ensuremath{\mathcal{G}}}(x)$ the minimal cost of reaching a node $x$ from $x_{\text{init}}$ using a roadmap $\mathcal{G}$. These are standard procedures used by the RRT or RRT\* algorithms. Finally, we use the (generic) predicate `construct_roadmap` to assess if a stopping criterion has been reached to terminate the algorithm[^3].

## Algorithmic background

The RRT, RRG and RRT\* algorithms share the same high-level structure. They maintain a roadmap as the underlying data structure which is a directed tree for RRT and RRT\* and a directed graph for RRG. At each iteration a configuration $x_{\text{rand}}$ is sampled at random. Then, $x_{\text{nearest}}$, the nearest configuration to $x_{\text{rand}}$ in the roadmap is found and extended in the direction of $x_{\text{rand}}$ to a new configuration $x_{\text{new}}$. If the path between $x_{\text{nearest}}$ and $x_{\text{new}}$ is collision-free, $x_{\text{new}}$ is added to the roadmap  (see Alg. [\[alg_RRT_orig\]](#alg_RRT_orig){reference-type="ref" reference="alg_RRT_orig"}, [\[alg_RRG\]](#alg_RRG){reference-type="ref" reference="alg_RRG"} and [\[alg_RRT_star\]](#alg_RRT_star){reference-type="ref" reference="alg_RRT_star"}, lines 3-9).

:::: algorithm
::: algorithmic
$\ensuremath{\mathcal{T}}.V \leftarrow \ensuremath{\{ x_{\text{init}}\}}$

$x_{\text{rand}} \leftarrow \texttt{sample\_free()}$ $x_{\text{nearest}} \leftarrow
 											\texttt{nearest\_neighbor}(	x_{\text{rand}}, \ensuremath{\mathcal{T}}.V)$ $x_{\text{new}} \leftarrow
 											\texttt{steer}(	x_{\text{nearest}}, x_{\text{rand}})$

CONTINUE

$\ensuremath{\mathcal{T}}.V \leftarrow \ensuremath{\mathcal{T}}.V \cup \ensuremath{\{ x_{\text{new}}\}}$ $\ensuremath{\mathcal{T}}.\texttt{parent}(x_{\text{new}}) \leftarrow x_{\text{nearest}}$
:::
::::

:::: algorithm
::: algorithmic
$\ensuremath{\mathcal{G}}.V \leftarrow \ensuremath{\{ x_{\text{init}}\}}$ $\ensuremath{\mathcal{G}}.E \leftarrow \emptyset$

$x_{\text{rand}} \leftarrow \texttt{sample\_free()}$ $x_{\text{nearest}} \leftarrow
 											\texttt{nearest\_neighbor}(	x_{\text{rand}}, \ensuremath{\mathcal{G}}.V)$ $x_{\text{new}} \leftarrow
 											\texttt{steer}(	x_{\text{nearest}}, x_{\text{rand}})$

CONTINUE

$\ensuremath{\mathcal{G}}.V \leftarrow \ensuremath{\mathcal{G}}.V \cup \ensuremath{\{ x_{\text{new}}\}}$ $\ensuremath{\mathcal{G}}.E \leftarrow 
 											\ensuremath{\{ (x_{\text{nearest}}, x_{\text{new}}) , (x_{\text{new}}, x_{\text{nearest}})\}}$

$X_{\text{near}} \leftarrow \texttt{nearest\_neighbors}(	x_{\text{new}},$\
$\ensuremath{\mathcal{G}}.V , k_{RRG} \log(|\ensuremath{\mathcal{G}}.V |))$ $\ensuremath{\mathcal{G}}.E \leftarrow 
 													\ensuremath{\{ (x_{\text{near}}, x_{\text{new}}) , (x_{\text{new}}, x_{\text{near}})\}}$
:::
::::

:::: algorithm
::: algorithmic
$\ensuremath{\mathcal{T}}.V \leftarrow \ensuremath{\{ x_{\text{init}}\}}$

$x_{\text{rand}} \leftarrow \texttt{sample\_free()}$ $x_{\text{nearest}} \leftarrow
 											\texttt{nearest\_neighbor}(	x_{\text{rand}}, \ensuremath{\mathcal{G}}.V)$ $x_{\text{new}} \leftarrow
 											\texttt{steer}(	x_{nearest}, x_{rand})$

CONTINUE

$\ensuremath{\mathcal{T}}.V \leftarrow \ensuremath{\mathcal{T}}.V \cup \ensuremath{\{ x_{\text{new}}\}}$ $\ensuremath{\mathcal{T}}.\texttt{parent}(x_{\text{new}}) \leftarrow x_{\text{nearest}}$

$X_{\text{near}} \leftarrow \texttt{nearest\_neighbors}(	x_{\text{new}},$\
$\ensuremath{\mathcal{T}}.V , k_{RRG} \log(|\ensuremath{\mathcal{T}}.V |))$

`rewire_RRT`$^*$($x_{\text{near}}, x_{\text{new}}$ )

`rewire_RRT`$^*$($x_{\text{new}}, x_{\text{near}}$ )
:::
::::

:::: algorithm
::: algorithmic
$c \leftarrow$ `cost`($x_{\text{potential\_parent}}, x_{\text{child}}$) $\ensuremath{\mathcal{T}}.\texttt{\text{parent}}(x_{\text{child}}) \leftarrow 
    						x_{\text{potential\_parent}}$
:::
::::

The algorithms differ in the connections added to the roadmap. In RRT, only the edge $(x_{\text{nearest}}, x_{\text{new}})$ is added. In RRG and RRT\*, a set $X_{\text{near}}$ of $k_{RRG} \log(|V|)$ nearest neighbors of $x_{\text{new}}$ is considered. Here, $k_{RRG}$ is a constant ensuring that the cost of paths produced by RRG and RRT\* indeed converges to the optimal cost almost surely as the number of samples grows. A valid choice for all problem instances is $k_{RRG} = 2e$ [@KF11]. For each neighbor $x_{\text{near}} \in X_{\text{near}}$ of $x_{\text{new}}$, RRG checks if the path between $x_{\text{near}}$ and $x_{\text{new}}$ is collision-free and if so, $(x_{\text{near}} , x_{\text{new}})$ and $(x_{\text{new}}, x_{\text{near}})$ are added to the roadmap (lines 10-13). RRT\* maintains a sub-graph of the RRG roadmap. This is done by an additional rewiring procedure (Alg. [\[alg_update_rrt_star\]](#alg_update_rrt_star){reference-type="ref" reference="alg_update_rrt_star"}) which is invoked twice: The first time, it is used to find the node $x_{\text{near}} \in X_{\text{near}}$ which will minimize the cost to reach $x_{\text{new}}$ (Alg. [\[alg_RRT_star\]](#alg_RRT_star){reference-type="ref" reference="alg_RRT_star"}, lines 11-12). The second time, the procedure is used to to minimize the cost to reach every node $x_{\text{near}} \in X_{\text{near}}$ by considering $x_{\text{new}}$ as its parent (Alg. [\[alg_RRT_star\]](#alg_RRT_star){reference-type="ref" reference="alg_RRT_star"}, lines 13-14). Thus, at all time, RRT\* maintains a tree which, as mentioned, is a subgraph of the RRG roadmap.

Given a sequence of $n$ random samples, the cost of the path obtained using the RRG algorithm is a lower bound on the cost of the path obtained using the RRT\* algorithm. However, RRG requires both additional memory (to explicitly store the set of $O(\log n)$ neighbours) and exhibits longer running times (due to the additional calls to the local planner). In practice, this excess in running time is far from negligible (see Section [4](#sec:eval){reference-type="ref" reference="sec:eval"}), making RRT\* a more suitable algorithm for asymptotically-optimal motion planning.

# Asymptotically near-optimal motion-planning {#sec:alg}

Clearly the asymptotic optimality of the RRT\* and RRG algorithms comes at the cost of the additional $O(k_{RRG}\log(|V|))$ calls to the local planner at each stage (and some additional overhead). If we are not concerned with *asymptotically optimal* solutions, we do not have to consider all of the $k_{RRG} \log(|V|)$ neighbors when a node is added. Our idea is to initially only *estimate* the quality of each edge. We use this estimate of the quality of the edge to decide if to discard it, use it *without* checking if it is collision-free or use it after validating that it is indeed collision-free. Thus, many calls to the local planner can be avoided, though we still need to estimate the quality of many edges. Our approach is viable in cases where such an assessment can be carried out efficiently. Namely, more efficiently than deciding if an edge is collision-free. This condition holds naturally when the quality measure is *path length* which is the cost function considered in this paper; for a discussion on different cost functions, see Section [6](#sec:con){reference-type="ref" reference="sec:con"}.

## Single-sink shortest-path problem

As we will see, our algorithm needs to maintain the shortest path from $x_{\text{init}}$ to any node in a graph. Moreover, this graph undergoes a series of edge insertions and edge deletions. This problem is referred to as the fully dynamic *single-source shortest-path problem* or SSSP for short. Efficient algorithms [@FMN00; @RR96] exist that can store the minimal cost to reach each node (and the corresponding path) in such settings from a source node. In our setting, this source node is $x_{\text{init}}$. We make use of the following procedures which are provided by SSSP algorithms: `delete_edge`$_{\text{SSSP}}$($\ensuremath{\mathcal{G}}, (x_1, x_2)$) and `insert_edge`$_{\text{SSSP}}$($\ensuremath{\mathcal{G}}, (x_1, x_2)$) which delete and insert, respectively, the edge $(x_1, x_2)$ from/into the graph $\ensuremath{\mathcal{G}}$ while maintaining cost$_\ensuremath{\mathcal{G}}$ for each node. We assume that these procedures return the set of nodes whose cost has changed due to the edge deletion or edge insertion. Furthermore, let `parent`$_{\texttt{SSSP}}$($\ensuremath{\mathcal{G}}, x$) be a procedure returning the parent of $x$ in the shortest path from the source to $x$ in $\ensuremath{\mathcal{G}}$.

## LBT-RRT

We propose a modification to the RRG algorithm by maintaining two roadmaps $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, \ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ simultaneously. Both roadmaps have the same set of vertices but differ in their edge set. $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ is a graph and $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ is a tree rooted at $x_{\text{init}}$[^4].

Let $\ensuremath{\mathcal{G}}_{RRG}$ be the roadmap constructed by RRG if run on the same sequence of samples used for LBT-RRT. The following invariants are maintained by the LBT-RRT algorithm:\

::: framed
**Bounded approximation invariant** - For every node $x \in \ensuremath{\ensuremath{\mathcal{T}}_{apx}}, \ensuremath{\ensuremath{\mathcal{G}}_{lb}}$, $\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{T}}_{apx}}}(x) 
			\leq 
	(1+\varepsilon) \cdot \texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x).$
:::

and

::: framed
**Lower bound invariant** - For every node $x \in \ensuremath{\ensuremath{\mathcal{G}}_{lb}}$, $\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x) \leq \texttt{cost}_{\ensuremath{\mathcal{G}}_{RRG}}(x).$
:::

The lower bound invariant is maintained by ensuring that the edges of $\ensuremath{\mathcal{G}}_{RRG}$ are a subset of the edges of $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$. As we will see, $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ may possibly contain some edges that $\ensuremath{\mathcal{G}}_{RRG}$ considered but found to be in collision.

The main body of the algorithm (see Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"}) follows the structure of the RRT, RRT\* and RRG algorithms with respect to adding a new milestone (lines 3-7) but differs in the connections added. If a path between the new node $x_{\text{new}}$ and its nearest neighbor $x_{\text{nearest}}$ is indeed collision-free, it is added to both roadmaps together with an edge from $x_{\text{nearest}}$ to $x_{\text{new}}$ (lines 8-11).

Similar to RRG and RRT\*, LBT-RRT locates the set $X_{\text{near}}$ of $k_{RRG}\log(|V|)$ nearest neighbors of $x_{\text{new}}$ (line 12). Then, for each edge connecting a node from $X_{\text{near}}$ to $x_{\text{new}}$ and for each edge connecting $x_{\text{new}}$ to a node from $X_{\text{near}}$, it uses a procedure `consider_edge` (Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}) to assess if the edge should be inserted to either roadmaps. The edge is first lazily inserted into $\ensuremath{\mathcal{G}}_{lb}$ without checking if it is collision-free. This *may* cause the bounded approximation invariant to be violated, which in turn will induce a call to the local planner for a set of edges. Each such edge might either be inserted into $\ensuremath{\mathcal{T}}_{apx}$ or removed from $\ensuremath{\mathcal{G}}_{lb}$.

This is done as follows, first, the edge considered is inserted to $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ while updating the shortest path to reach each vertex in $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ (Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}, line 1). Denote by $I$ the set of updated vertices after the edge insertion. Namely, for every $x \in I$, `cost`$_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x)$ has decreased due to the edge insertion. This cost decrease may, in turn, cause the bounded approximation invariant to be violated for some nodes in $U$. All such nodes are collected and inserted into a priority queue $Q$ (line 2) ordered according to $\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}$ from low to high. Now, the algorithm proceeds in iterations until the queue is empty (lines 3-15). At each iteration, the head of the queue $x$ is considered (line 4). If the bounded approximation invariant does not hold (line 5), the algorithm checks if the edge in $\ensuremath{\mathcal{G}}_{lb}$ connecting the node $x$ to its parent along the shortest path to $x_{\text{init}}$ is collision free (lines 6-7). If this is the case, the approximation tree is updated (line 8) and the head of the queue is removed (line 9). If not, the edge is removed from $\ensuremath{\mathcal{G}}_{lb}$(line 11). This causes an increase in cost$_{\text{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}}$ for a set $D$ of nodes, some of which are already in the priority queue. Clearly, the bounded approximation invariant holds for the nodes $x \in D$ that are not in the priority queue. Thus, we take only the nodes $x \in D$ that are already in $Q$ and update their location in $Q$ according to their new cost (lines 12-13) . Finally, if the bounded approximation invariant holds for $x$ then it is removed from the queue (lines 15).

:::: algorithm
::: algorithmic
$\ensuremath{\ensuremath{\mathcal{T}}_{lb}}.G \leftarrow \ensuremath{\{ x_{\text{init}}\}}$ $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}.V \leftarrow \ensuremath{\{ x_{\text{init}}\}}$

$x_{\text{rand}} \leftarrow \texttt{sample\_free()}$ $x_{\text{nearest}} \leftarrow
 											\texttt{nearest\_neighbor}(	x_{rand}, \ensuremath{\ensuremath{\mathcal{T}}_{lb}}.V)$ $x_{\text{new}} \leftarrow
 											\texttt{steer}(	x_{\text{nearest}}, x_{\text{rand}})$

CONTINUE

$\ensuremath{\ensuremath{\mathcal{T}}_{apx}}.V \leftarrow \ensuremath{\ensuremath{\mathcal{T}}_{apx}}.V \cup \ensuremath{\{ x_{\text{new}}\}}$ $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}.\texttt{parent}(x_{\text{new}}) \leftarrow x_{\text{nearest}}$

$\ensuremath{\ensuremath{\mathcal{G}}_{lb}}.V \leftarrow \ensuremath{\ensuremath{\mathcal{G}}_{lb}}.V \cup \ensuremath{\{ x_{\text{new}}\}}$ `insert_edge`$_{\text{SSSP}}$($\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, (x_{\text{nearest}}, x_{\text{new}})$)

$X_{\text{near}} \leftarrow \texttt{nearest\_neighbors}(	x_{\text{new}},$\
$\ensuremath{\ensuremath{\mathcal{G}}_{lb}}.V , k_{RRG} \log(|\ensuremath{\ensuremath{\mathcal{G}}_{lb}}.V |))$

`consider_edge`$(x_{\text{near}}, x_{\text{new}})$

`consider_edge`$(x_{\text{new}}, x_{\text{near}})$
:::
::::

:::: algorithm
::: algorithmic
$I \leftarrow$`insert_edge`$_{\text{SSSP}}$($\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, (x_{1}, x_{2})$) $Q \leftarrow \ensuremath{\{  x \in I \ | \
 		\text{cost}_{\ensuremath{\ensuremath{\mathcal{T}}_{apx}}}(x) > (1 + \varepsilon) \cdot \text{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x) \}}$ $x \leftarrow Q.\texttt{top}()$; $x_{parent} \leftarrow \texttt{parent}_{\texttt{SSSP}}(\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, x)$

$\ensuremath{\ensuremath{\mathcal{T}}_{apx}}.\texttt{\text{parent}}(x) \leftarrow  x_{\text{parent}}$ $Q.\texttt{pop}()$ $D \leftarrow$`delete_edge`$_{\text{SSSP}}$($\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, (x_{\text{parent}}, x)$) $Q$.`update_cost`$(y)$ $Q.\texttt{pop}()$
:::
::::

## Analysis {#susbsec:analysis}

In this section we show that Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"} maintains the lower bound invariant (Corollary [5](#cor_lb){reference-type="ref" reference="cor_lb"}) and that after every iteration of the algorithm the bounded approximation invariant is maintained (Lemma [8](#lem_invariant){reference-type="ref" reference="lem_invariant"}). We then report on the time complexity of the algorithm (Corollary [10](#cor_complex){reference-type="ref" reference="cor_complex"}).

We note the following straightforward, yet helpful observations comparing LBT-RRT and RRG when run on the same sequence of random samples:

::: {#obs:1 .obs}
**Observation 1**. *A node $x$ is added to $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ and to $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ if and only if $x$ is added to $\ensuremath{\mathcal{G}}_{RRG}$ (Alg. [\[alg_RRG\]](#alg_RRG){reference-type="ref" reference="alg_RRG"} lines 3-8 and [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"}, lines 3-11).*
:::

::: obs
**Observation 2**. *Both LBT-RRT and RRG consider the same set of $k_{RRG}\log(|V|)$ nearest neighbors of $x_{\text{new}}$ (Alg. [\[alg_RRG\]](#alg_RRG){reference-type="ref" reference="alg_RRG"}, line 10 and Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"}, line 12).*
:::

::: obs
**Observation 3**. *Every edge added to the RRG roadmap (Alg. [\[alg_RRG\]](#alg_RRG){reference-type="ref" reference="alg_RRG"} line 13) is added to $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ (Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"} lines 14, 16 and Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"} line 1).*
:::

Note that some additional edges may be added to $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ which are not added to the RRG roadmap as they are not collision-free.

::: {#obs:4 .obs}
**Observation 4**. *Every edge of $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ is collision free (Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"}, line 9 and Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}, line 8).*
:::

Thus, the following corollary trivially holds:

::: {#cor_lb .cor}
**Corollary 5**. *After every iteration of LBT-RRT(Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"}, lines 3-16) the lower bound invariant is maintained.*
:::

We continue with the following observations relevant to the analysis of the procedure `consider_edge`($x_{1}, x_{2}$):

::: {#obs:5 .obs}
**Observation 6**. *The only place where cost$_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}$ is decreased is during a call to `insert_edge`$_{\text{SSSP}}$($\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, (x_{1}, x_{2})$ (Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}, line 1).*
:::

::: {#obs:7 .obs}
**Observation 7**. *A node $x$ is removed from the queue $Q$ (Alg [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}, lines 9,15) only if the bounded approximation invariant holds for $x$.*
:::

Showing that the bounded approximation invariant is maintained is done by induction on the number of calls to `consider_edge`($x_{1}, x_{2}$). Using Obs. [6](#obs:5){reference-type="ref" reference="obs:5"}, prior to the first call to `consider_edge`($x_{1}, x_{2}$) the bounded approximation invariant is maintained. Thus, we need to show that:

::: {#lem_invariant .lem}
**Lemma 8**. *If the bounded approximation invariant holds prior to a call to the procedure `consider_edge`($x_{1}, x_{2}$) (Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}), then the procedure will terminate with the invariant maintained.*
:::

::: proof
*Proof.* Assume that the bounded approximation invariant was maintained prior to a call to `consider_edge`($x_{1}, x_{2}$). By Observation [6](#obs:5){reference-type="ref" reference="obs:5"} inserting a new edge (line 1) may cause the bounded approximation invariant to be violated for a set of nodes. Moreover, it is the *only* place where such an event can occur. Observation [7](#obs:7){reference-type="ref" reference="obs:7"} implies that the bounded approximation invariant holds for every vertex *not* in $Q$.

Recall that in the priority queue we order the nodes according to $\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}$ (from low to high) and at each iteration of `consider_edge`($x_{1}, x_{2}$) the top of the priority queue $x$ is considered. The parent $x_{\text{parent}}$ of $x$, that has a smaller cost value, cannot be in the priority queue. Thus, the bounded approximation invariant holds for $x_{\text{parent}}$. Namely, $$\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{T}}_{apx}}}(x_{\text{parent}}) 
			\leq 
	(1+\varepsilon) \cdot \texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x_{\text{parent}}).$$ Now, if the edge between $x_{\text{parent}}$ and $x$ is found to be free (line 7), we update the approximation tree (line 8). It follows that after such an event, $$\begin{eqnarray}
\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{T}}_{apx}}}(x)
		&		= 	&		
\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{T}}_{apx}}}(x_{parent}) + 
 		\nonumber \\
		&			&		\texttt{cost}(x_{\text{parent}}, x)
 		\nonumber \\
		&		\leq 	&		
(1+\varepsilon) \cdot \texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x_\text{parent}) + 
 		\nonumber \\
		&			&		\texttt{cost}(x_\text{parent},x)
 		\nonumber \\
		&		\leq 	&		
(1+\varepsilon) \cdot  \texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x). \nonumber
\end{eqnarray}$$ Namely, after updating the approximation tree, the bounded approximation invariant holds for the node $x$.

To summarize, at each iteration of Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"} (lines 3-16), either: (i) we remove a node $x$ from $Q$ (line 9 or line 15) or (ii) we remove an incoming edge to the node $x$ from the lower bound graph (line 11). If the node $x$ was removed from $Q$ (case (i)), the bounded approximation invariant holds---either it was not violated to begin with (line 15) or it holds after updating the approximation tree (lines 8-9).

To finish the proof we need to show that the main loop (lines 3-15) in Alg. [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"} indeed terminates. Recall that the degree of each node is $O(\log n)$. Thus, a node $x$ cannot be at the head of the queue more than $O(\log n)$ times (after each time we either remove an incoming edge or remove $x$ from the queue). This in turn implies that after at most $O(n\log n)$ iterations $Q$ is empty and the main loop terminates. ◻
:::

From Corollary [5](#cor_lb){reference-type="ref" reference="cor_lb"}, Lemma [8](#lem_invariant){reference-type="ref" reference="lem_invariant"} and using the asymptotic optimality of RRG we conclude,

::: thm
**Theorem 9**. *LBT-RRT is asymptotically near-optimal with an approximation factor of $(1+\varepsilon)$.*
:::

Namely, the cost of the path computed by LBT-RRT converges to a cost at most $(1+\varepsilon)$ times the cost of the optimal path almost surely.

We continue now to discuss the time complexity of the algorithm. If $\delta$ is the number of nodes updated during a call to an SSSP procedure[^5] (namely, `insert_edge`$_{\text{SSSP}}$ or `delete_edge`$_{\text{SSSP}}$), then the complexity of the procedure is $O(\delta \log n)$ when using the algorithm of Ramalingam et al. [@RR96]. Set $\hat{\delta}$ to be the maximum value of $\delta$ over all calls to SSSP procedures (Alg [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"} line 11 and Alg [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"}, lines 1 and 11) and let $n$ denote the final number of samples used by LBT-RRT.

We have $O(n\log n)$ edges and each edge will be inserted to $\ensuremath{\mathcal{G}}_{lb}$ once (Alg [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"} line 11 or Alg [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"} line 1) and possibly be removed from $\ensuremath{\mathcal{G}}_{lb}$ once (Alg [\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"} line 11). Therefor, the total complexity due to the SSSP procedures is $O(\hat{\delta} \cdot n\log^2 n)$. The time-complexity of all the other operations (nearest neighbours, collision detection etc.) is similar to RRG which runs in time $O( n \log n)$.

::: {#cor_complex .cor}
**Corollary 10**. *LBT-RRT runs in time $O(\hat{\delta} \cdot n\log^2 n)$, where $n$ is the number of samples and $\hat{\delta}$ is the maximal number of nodes updated over all SSSP procedures .*
:::

While this running time may seem discouraging, we note that in practice, the local planning dominates the actual running time of the algorithm in practice. As we demonstrate in Section [4](#sec:eval){reference-type="ref" reference="sec:eval"} through various simulations, LBT-RRT produces high-quality results in an efficient manner.

## Implementation details

We describe the following optimizations that we use in order to speed up the running-time of the algorithm. The first is that the set $X_{\text{near}}$ is ordered according to the cost to reach $x_{\text{new}}$ from $x_{\text{init}}$ through an element $x$ of $X_{\text{near}}$. Hence, the set $X_{\text{near}}$ will be traversed from the node that yields the smallest lower bound to reach $x_{\text{new}}$ to the node that will yield the highest lower bound. After the first edge that does *not* violate the bounded approximation invariant, no subsequent node can improve the cost to reach $x_{\text{new}}$ and `insert_edge`$_{\texttt{SSSP}}$ will not need to perform any updates. This ordering was previously used to speed up RRT\* (see, e.g., [@PKSFTW11; @WvdB13]).

The second optimization comes to avoid the situation where `insert_edge`$_{\texttt{SSSP}}$ is called and immediately afterwards the same edge is removed. Hence, given an edge, we first check if the bounded approximation invariant will be violated had the edge been inserted. If this is indeed the case, the local planner is invoked and only if the edge is collision free `insert_edge`$_{\texttt{SSSP}}$ is called.

## Discussion

Let ${\rm T}_{ALG}^{\omega}$ denote the time needed for an algorithm $ALG$ to find a feasible solution on a sequence $\omega$of random samples. Clearly, ${\rm T}_{\rm RRT}^{\omega} \leq {\rm T}_{\rm RRG}^{\omega}$ (as RRG may require more calls to the collision detector than the RRT algorithm). Moreover, for every $\varepsilon_1 \leq \varepsilon_2$ it holds that $$%T_{\eRRT(\infty)}^{\omega} 
{\rm T}_{\rm RRT}^{\omega} 
	\leq 
{\rm T}_{\rm LBT-RRT(\varepsilon_2)}^{\omega} 
	\leq
{\rm T}_{\rm LBT-RRT(\varepsilon_1)}^{\omega} 
	\leq 
{\rm T}_{\rm RRG}^{\omega}.
%T_{\eRRT(0)}^{\omega}.$$

Thus, given a limited amount of time, RRG may fail to construct any solution. On the other hand, RRT may find a solution fast but will not improve its quality (if the goal is a single configuration). LBT-RRT allows to find a feasible path quickly while continuing to search for a path of higher quality.

**Remark** The conference version of this paper contained an oversight with regard to how the bounded approximation invariant was maintained. Specifically, instead of storing $\ensuremath{\mathcal{G}}_{lb}$ as a graph, a tree was stored which was rewired locally. When the algorithm tested if the bounded approximation invariant was violated for a node $x$, it only considered the *children* of $x$ in the tree. This local test did not take into account the fact that changing the cost of $x$ in the tree could also change the cost of nodes $y$ that are descendants of $x$ (but not its children). The implications of the oversight is that the algorithm was not asymptotically near optimal. The experimental results presented in the conference version of this paper suggest that in certain scenarios this oversight did not have a significant effect on the convergence to high quality solutions. Having said that, LBT-RRT as presented in this paper is both asymptotically near optimal and converges to high quality solutions faster than the original algorithm.

# Evaluation {#sec:eval}

We present an experimental evaluation of the performance of LBT-RRT as an anytime algorithm on different scenarios consisting of 3,6 and 12 DoFs (Fig. [1](#fig:scenarios){reference-type="ref" reference="fig:scenarios"}). The algorithm was implemented using the Open Motion Planning Library (OMPL 0.10.2) [@SMK12] and our implementation is currently distributed with the OMPL release. All experiments were run on a 2.8GHz Intel Core i7 processor with 8GB of memory. RRT\* was implemented by using the ordering optimization described in Section [3](#sec:alg){reference-type="ref" reference="sec:alg"} and [@PKSFTW11]).

:::: {#fig:scenarios .figure latex-placement="t,b,h"}
::: caption
Benchmark scenarios. The start and goal configuration are depicted in green and red, respectively.
:::
::::

:::: wrapfigure
r0.18

::: center
![image](Salzman2013Asymptotically_figs/barrier7.png){height="1.8 cm"}
:::
::::

The Maze scenario (Fig. [\[fig:maze\]](#fig:maze){reference-type="ref" reference="fig:maze"}) consists of a planar polygonal robot that can translate and rotate. The Alternating barriers scenario (Fig. [\[fig:alternating\]](#fig:alternating){reference-type="ref" reference="fig:alternating"}) consists of a robot with three perpendicular rods free-flying in space. The robot needs to pass through a series of barriers each containing a large and a small hole. For an illustration of one such barrier, see Fig. [\[fig:barrier\]](#fig:barrier){reference-type="ref" reference="fig:barrier"}. The large holes are located at alternating sides of consecutive barriers. Thus, an easy path to find would be to cross each barrier through a large hole. A high-quality path would require passing through a small hole after each large hole. Finally, the cubicles scenario consists of two L-shaped robots free-flying in space that need to exchange locations amidst a sparse collection of obstacles[^6].

We compare the performance of LBT-RRT with RRT, RRG and RRT\* when a fixed time budget is given. We add another algorithm which we call RRT+RRT\* which initially runs RRT and once a solution is found runs RRT\*. RRT+RRT\* will find a solution as fast as RRT and is asymptotically-optimal. For LBT-RRT we consider $(1+\varepsilon)$ values of $1.2, 1.4, 1.8$ and report on the success rate of each algorithm (Fig. [2](#fig:suc){reference-type="ref" reference="fig:suc"}). Additionally, we report on the path length after applying shortcuts (Fig. [4](#fig:len){reference-type="ref" reference="fig:len"}). Each result is averaged over 100 different runs.

:::: {#fig:suc .figure latex-placement="t,b,h"}
::: caption
Success rate for algorithms on different scenarios (RRT and RRT+RRT\* have almost identical success rates; the plot for RRT+RRT\* is omitted to avoid cluttering of the graph).
:::
::::

:::: {#fig:len .figure latex-placement="t,b,h"}
::: caption
Path lengths for algorithms on different scenarios. Length values are normalized such that a length of one represents the length of an optimal path.
:::
::::

Fig. [2](#fig:suc){reference-type="ref" reference="fig:suc"} depicts similar behaviour for all scenarios: As one would expect, the success rate for all algorithms has a monotonically increasing trend as the time budget increases. For a specific time budget, the success rate for RRT and RRT+RRT\* is typically highest while that of the RRT\* and RRG is lowest. The success rate for LBT-RRT for a specific time budget, typically increases as the value of $\varepsilon$ increases. Fig. [4](#fig:len){reference-type="ref" reference="fig:len"} also depicts similar behavior for all scenarios: the average path length decreases for all algorithms (except for RRT). The average path length for LBT-RRT typically decreases as the value of $\varepsilon$ decreases and is comparable to that of RRT\* for low values of $\varepsilon$. RRT+RRT\* behaves similarly to RRT\* but with a "shift" along the time-axis which is due to the initial run of RRT. We note that although RRG and RRT+RRT\* are asymptotically-optimal, their overhead makes them poor algorithms when one desires a *high-quality* solution very fast.

Thus, Fig. [2](#fig:suc){reference-type="ref" reference="fig:suc"} and [4](#fig:len){reference-type="ref" reference="fig:len"} should be looked at simultaneously as they encompass the tradeoff between speed to find *any* solution and the quality of the solution found. Let us demonstrate this on the alternating barriers scenario: If we look at the success rate of each algorithm to find *any* solution (Fig. [\[fig:alternating_suc\]](#fig:alternating_suc){reference-type="ref" reference="fig:alternating_suc"}), one can see that RRT manages to achieve a success rate of 70% after 30 seconds. RRT\*, on the other hand, requires 70 seconds to achieve the same success rate (more than double the time). For all different values of $\varepsilon$, LBT-RRT manages to achieve a success rate of 70% after 50 seconds (around 60% overhead when compared to RRT). Now, considering the path length at 50 seconds, typically the paths extracted from LBT-RRT yield the same quality when compared to RRT\* while ensuring a high success rate.

The same behavior of finding paths of high-quality (similar to the quality that RRT\* produces) within the time-frames that RRT requires in order to find *any* solution has been observed for both the Maze scenario and the Cubicles scenario. Results omitted in this text. For supplementary material the reader is referred to <http://acg.cs.tau.ac.il/projects/LBT-RRT>.

# Lazy, goal-biased LBT-RRT {#sec:extensions}

In this section we show to further reduce the number of calls to the local planner by incorporating a lazy approach together with a goal bias.

:::: algorithm
::: algorithmic
$c_{\min}^{\text{apx}} \leftarrow$ `cost`$_{\text{LPA*}}$($\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$) $\texttt{insert\_edge$_{\text{LPA*}}$}(\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, x_1, x_2)$ $x \leftarrow$ `shortest_path`$_{\text{LPA*}}$($\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$) $x_{parent} \leftarrow 
			\texttt{parent}_{\texttt{LPA*}}(\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, x)$ $c_{\min}^{\text{lb}} \leftarrow$ `cost`$_{\text{LPA*}}$($\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$)

$\texttt{insert\_edge$_{\text{LPA*}}$}(\ensuremath{\ensuremath{\mathcal{T}}_{apx}}, x_{parent},x)$ `shortest_path`$_{\text{LPA*}}$($\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$)

$c_{\min}^{\text{apx}} \leftarrow$ `cost`$_{\text{LPA*}}$($\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$) $x \leftarrow 
				\texttt{parent}_{\texttt{LPA*}}(x)$ `delete_edge`$_{\text{LPA*}}$$(\ensuremath{\ensuremath{\mathcal{G}}_{lb}}, x_{parent}, x)$ **GoTo** line 3
:::
::::

LBT-RRT maintains the lower bound invariant to *every* node. This is desirable in settings where a high-quality path to every point in the configuration space is required. However, when only a high-quality path to the goal is needed, this may lead to unnecessary time-consuming calls to the local planner.

Therefore, we suggest the following variant of LBT-RRT where we relax the bounded approximation invariant such that it holds only for nodes $x \in X_{goal}$. This variant is similar to LBT-RRT but differs with respect to the calls to the local planner and with respect to the dynamic shortest-path algorithm used. As we only maintain the bounded approximation invariant to the goal nodes, we do not need to continuously update the (approximate) shortest path to every node in $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$. We replace the SSSP algorithm, which allows to compute the shortest paths to *every* node in a dynamic graph, with Lifelong Planning A\* (LPA\*) [@KLF04]. LPA\* allows to repeatedly find shortest paths from a given start to a given goal while allowing for edge insertions and deletions. Similiar to A\* [@P84], this is done by using heuristic function $h$ such that for every node $x$, $h(x)$ is an estimate of the cost to reach the goal from $x$.

Given a start vertex $x_{init}$, a goal region $X_{Goal}$, we will use the following functions which are provided when implementing LPA\*: `shortest_path`$_{\text{LPA*}}$$(G)$, recomputes the shortest path to reach $X_{Goal}$ from $x_{init}$ on the graph $G$ and returns the node $x \in X_{Goal}$ such that $x \in X_{Goal}$ and $\texttt{cost}_{\ensuremath{\ensuremath{\mathcal{G}}_{lb}}}(x)$ is minimal among all $x' \in X_{Goal}$. Once the function has been called, the following functions take constant running time: `cost`$_{\text{LPA*}}$$(G)$ returns the minimal cost to reach $X_{Goal}$ from $x_{init}$ on the graph $G$ and for every node $x$ lying on a shortest path to the goal, `parent`$_{\texttt{LPA*}}(G, x)$ returns the predecessor of the node $x$ along this path. Additionally, $\texttt{insert\_edge$_{\text{LPA*}}$}(G, x, y)$ and `delete_edge`$_{\text{LPA*}}$$(G, x, y)$ inserts (deletes) the edge $(x,y)$ to (from) the graph $G$, respectively.

We are now ready to describe Lazy, goal-biased LBT-RRT which is similar to LBT-RRT except for the way new edges are considered. Instead of the function `consider_edge` called in lines 14 and 16 of Alg. [\[alg_RRT\]](#alg_RRT){reference-type="ref" reference="alg_RRT"}, the function `consider_edge_goal_biased` is called.

`consider_edge_goal_biased`$(x_1, x_2)$, outlined in Alg. [\[alg_update2\]](#alg_update2){reference-type="ref" reference="alg_update2"}, begins by computing the cost to reach the goal in $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ (line 1) and in $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ after adding the edge $(x_1, x_2)$ lazily to $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ (lines 2-5). Namely, the edge is added with no call to the local planner and without checking if the bounded approximation invariant is violated. Note that the *relaxed* bounded approximation invariant is violated (line 6) only if a path to the goal is found. Clearly, if all edges along the shortest path to the goal are found to be collision free, then the invariant holds. Thus, the algorithm attempts to follow the edges along the path (starting at the last edge and backtracking towards $x_{init}$) one by one and test if they are indeed collision-free. If an edge is collision free (line 7), it is inserted to $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ (line 8), and a path to the goal in $\ensuremath{\ensuremath{\mathcal{T}}_{apx}}$ is recomputed (line 9). This is repeated as long as the relaxed bounded approximation invariant is violated. If the edge is found to be in collision (line 12), it is removed from $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ (line 13) and the process is repeated (line 14).

Following similar arguments as described in Section [3](#sec:alg){reference-type="ref" reference="sec:alg"}, one can show the correctness of the algorithm. We note that as long as no path has been found, the algorithm performs no more calls to the local planner than RRT. Additionally, it is worth noting that the planner bares resemblance with Lazy-RRG\* [@H15].

We compared Lazy, goal-biased LBT-RRT with LBT-RRT, RRT\* and RRG on the Home scenario (Fig. [\[fig:home_scene\]](#fig:home_scene){reference-type="ref" reference="fig:home_scene"}). In this scenario, a low quality solution is typically easy to find and all algorithms (except RRG) find a solution with roughly the same success rate as RRT (results omitted). Converging to the optimal solution requires longer running times as low-quality paths are easy to find yet high-quality ones pass through narrow passages. Fig. [\[fig:home_cost\]](#fig:home_cost){reference-type="ref" reference="fig:home_cost"} depicts the path length obtained by the algorithms as a function of time. The convergence to the optimal solution of RRG is significantly slower than all other algorithms. Both LBT-RRT and RRT\* find a low quality solution (between five and six times longer than the optimal solution) within the allowed time frame and manage to slightly improve upon its cost (with RRT\* obtaining slightly shorter solutions than LBT-RRT). When enhancing LBT-RRT with a lazy approach together with goal-biasing, one can observe that the convergence rate improves substantially.

:::: {#fig:len .figure latex-placement="t,b,h"}
::: caption
Simulation results comparing Lazy, goal-biased LBT-RRT with LBT-RRT, RRT\* and RRG. (a) Home scenario (provided by the OMPL distribution). Start and target table-shaped robots are depicted in green and red, respectively. (b) Path lengths as a function of computation time. Length values are normalized such that a length of one represents the length of an optimal path
:::
::::

# Conclusion and future work {#sec:con}

In this work we presented an asymptotically near-optimal motion planning algorithm. Using an approximation factor allows the algorithm to avoid calling the computationally-expensive local planner when no substantially better solution may be obtained. LBT-RRT, together with the lazy, goal-biased variant, make use of *dynamic shortest path algorithms*. This is an active research topic in many communities such as artificial intelligence and communication networks.

Hence, the algorithms we proposed in this work may benefit from any advances made for dynamic shortest path algorithms. For example, recently D'Andrea et al. [@DDFLP13] presented an algorithm that allows for dynamically maintaining shortest path trees under *batches* of updates which can be used by LBT-RRT instead of the SSSP algorithm.

Looking to further extend our framework, we seek natural stopping criteria for LBT-RRT. Such criteria could possibly be related to the rate at which the quality is increased as additional samples are introduced. Once such a criterion is established, one can think of the following framework: Run LBT-RRT with a large approximation factor (large $\varepsilon$) , once the stopping criterion has been met, decrease the approximation factor and continue running. This may allow an even quicker convergence to find any feasible path while allowing for refinement as time permits (similar to [@APD11]). While changing the approximation factor in LBT-RRT may possibly require a massive rewiring of $\ensuremath{\ensuremath{\mathcal{G}}_{lb}}$ (to maintain the bounded approximation invariant) this is not the case in Lazy, goal-biased LBT-RRT. In this variant of LBT-RRT the approximation factor can change at any stage of the algorithm without any modifications at all.

An interesting question to be further studied is can our framework be applied to different quality measures. For certain measures, such as bottleneck clearance of a path, this is unlikely, as bounding the quality of an edge already identifies if it is collision-free. However, for some other measures such as energy consumption, we believe that the framework could be effectively used.

# Acknowledgements {#sec:ack}

We wish to thank Leslie Kaelbling for suggesting the RRT+RRT\* algorithm, Chengcheng Zhong for feedback on the implementation of the algorithm and Shiri Chechik for advice regrading dynamic shortest path algorithms.

::: thebibliography
10 url@samestyle

L. E. Kavraki, P. Švestka, J.-C. Latombe, and M. H. Overmars, "Probabilistic roadmaps for path planning in high dimensional configuration spaces," *IEEE Trans. Robot.*, vol. 12, no. 4, pp. 566--580, 1996.

J. J. Kuffner and S. M. LaValle, "RRT-Connect: An efficient approach to single-query path planning," in *ICRA*, 2000, pp. 995--1001.

H. Choset, K. M. Lynch, S. Hutchinson, G. Kantor, W. Burgard, L. E. Kavraki, and S. Thrun, *Principles of Robot Motion: Theory, Algorithms, and Implementation*.MIT Press, June 2005.

S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *I. J. Robotic Res.*, vol. 30, no. 7, pp. 846--894, 2011.

O. Nechushtan, B. Raveh, and D. Halperin, "Sampling-diagram automata: A tool for analyzing path quality in tree planners," in *WAFR*, 2010, pp. 285--301.

R. Geraerts and M. H. Overmars, "Creating high-quality paths for motion planning," *I. J. Robotic Res.*, vol. 26, no. 8, pp. 845--863, 2007.

B. Raveh, A. Enosh, and D. Halperin, "A little more, a lot better: Improving path quality by a path-merging algorithm," *IEEE Trans. Robot.*, vol. 27, no. 2, pp. 365--371, 2011.

N. M. Amato, O. B. Bayazit, L. K. Dale, C. Jones, and D. Vallejo, "OBPRM: an obstacle-based PRM for 3D workspaces," in *WAFR*, 1998, pp. 155--168.

J.-M. Lien, S. L. Thomas, and N. M. Amato, "A general framework for sampling on the medial axis of the free space," in *ICRA*, 2003, pp. 4439--4444.

C. Urmson and R. G. Simmons, "Approaches for heuristically biasing RRT growth," in *IROS*, 2003, pp. 1178--1183.

A. C. Shkolnik, M. Walter, and R. Tedrake, "Reachability-guided sampling for planning under differential constraints," in *ICRA*, 2009, pp. 2859--2865.

T. Siméon, J.-P. Laumond, and C. Nissoux, "Visibility-based probabilistic roadmaps for motion planning," *Advanced Robotics*, vol. 14, no. 6, pp. 477--493, 2000.

N. A. Wedge and M. S. Branicky, "On heavy-tailed runtimes and restarts in rapidly-exploring random trees," in *AAAI*, 2008, pp. 127--133.

O. Salzman, D. Shaharabani, P. K. Agarwal, and D. Halperin, "Sparsification of motion-planning roadmaps by edge contraction," *I. J. Robotic Res.*, vol. 33, no. 14, pp. 1711--1725, 2014.

J. D. Marble and K. E. Bekris, "Computing spanners of asymptotically optimal probabilistic roadmaps," in *IROS*, 2011, pp. 4292--4298.

------, "Asymptotically near-optimal is good enough for motion planning," in *ISRR*, 2011.

------, "Towards small asymptotically near-optimal roadmaps," in *ICRA*, 2012, pp. 2557--2562.

A. Dobson and K. E. Bekris, "Sparse roadmap spanners for asymptotically near-optimal motion planning," *I. J. Robotic Res.*, vol. 33, no. 1, pp. 18--47, 2014.

A. Perez, S. Karaman, A. Shkolnik, E. Frazzoli, S. Teller, and M. Walter, "Asymptotically-optimal path planning for manipulation using incremental sampling-based algorithms," in *IROS*, 2011, pp. 4307--4313.

F. Islam, J. Nasir, U. Malik, Y. Ayaz, and O. Hasan, "RRT\*-Smart: Rapid convergence implementation of RRT\* towards optimal solution," *Int. J. Adv. Rob. Sys.*, vol. 10, pp. 1--12, 2013.

O. Arslan and P. Tsiotras, "Use of relaxation methods in sampling-based algorithms for optimal motion planning," in *ICRA*, 2013, pp. 2413--2420.

L. Janson and M. Pavone, "Fast marching trees: a fast marching sampling-based method for optimal motion planning in many dimensions," *CoRR*, vol. abs/1306.3532, 2013.

J. Luo and K. Hauser, "An empirical study of optimal motion planning," in *IROS*, 2014, pp. 1761 -- 1768.

O. Salzman and D. Halperin, "Asymptotically-optimal motion planning using lower bounds on cost," *CoRR*, vol. abs/1403.7714, 2014.

Z. Littlefield, Y. Li, and K. E. Bekris, "Efficient sampling-based motion planning with asymptotic near-optimality guarantees for systems with dynamics," in *IROS*, 2013, pp. 1779--1785.

D. Ferguson and A. Stentz, "Anytime RRTs," in *IROS*, 2006, pp. 5369 -- 5375.

R. Alterovitz, S. Patil, and A. Derbakova, "Rapidly-exploring roadmaps: Weighing exploration vs. refinement in optimal motion planning," in *ICRA*, 2011, pp. 3706--3712.

R. Luna, I. A. Şucan, M. Moll, and L. E. Kavraki, "Anytime solution optimization for sampling-based motion planning," in *ICRA*, 2013, pp. 5053--5059.

S. Karaman, M. Walter, A. Perez, E. Frazzoli, and S. Teller, "Anytime motion planning using the RRT," in *ICRA*, 2011, pp. 1478--1483.

O. Salzman and D. Halperin, "Asymptotically near-optimal RRT for fast, high-quality, motion planning," in *ICRA*, 2014, pp. 4680--4685.

D. Frigioni, A. Marchetti-Spaccamela, and U. Nanni, "Fully dynamic algorithms for maintaining shortest paths trees," *J. Algorithms*, vol. 34, no. 2, pp. 251--281, 2000.

G. Ramalingam and T. W. Reps, "On the computational complexity of dynamic graph problems," *Theor. Comput. Sci.*, vol. 158, no. 1&2, pp. 233--277, 1996.

D. J. Webb and J. van den Berg, "Kinodynamic RRT\*: Asymptotically optimal motion planning for robots with linear dynamics," in *ICRA*, 2013, pp. 5054--5061.

I. A. Şucan, M. Moll, and L. E. Kavraki, "The Open Motion Planning Library," *IEEE Robotics & Automation Magazine*, vol. 19, no. 4, pp. 72--82, 2012.

S. Koenig, M. Likhachev, and D. Furcy, "Lifelong planning A∗," *Artificial Intelligence*, vol. 155, no. 1, pp. 93--146, 2004.

J. Pearl, *Heuristics: Intelligent Search Strategies for Computer Problem Solving*.Addison-Wesley, 1984.

K. Hauser, "Lazy collision checking in asymptotically-optimal motion planning," in *ICRA*, 2015, to appear.

A. D'Andrea, M. D'Emidio, D. Frigioni, S. Leucci, and G. Proietti, "Dynamically maintaining shortest path trees under batches of updates," in *Structural Information and Communication Complexity*, ser. Lecture Notes in Computer Science, T. Moscibroda and A. Rescigno, Eds.Springer International Publishing, 2013, vol. 8179, pp. 286--297.

L. Jaillet and J. M. Porta, "Asymptotically-optimal path planning on manifolds," in *RSS*, 2012.

B. Akgun and M. Stilman, "Sampling heuristics for optimal motion planning in high dimensions," in *IROS*, 2011, pp. 2640--2645.

N. M. Amato and L. K. Dale, "Probabilistic roadmap methods are embarrassingly parallel," in *ICRA*, 1999, pp. 688--694.

J. Ichnowski and R. Alterovitz, "Parallel sampling-based motion planning with superlinear speedup," in *IROS*, 2012, pp. 1206--1212.

J. Bialkowski, S. Karaman, and E. Frazzoli, "Massively parallelizing the RRT and the RRT\*," in *IROS*, 2011, pp. 3513--3518.

W. Wang, D. Balkcom, and A. Chakrabarti, "A fast streaming spanner algorithm for incrementally constructing sparse roadmaps," *IROS*, pp. 1257--1263, 2013.
:::

::: IEEEbiography
Oren Salzman is a PhD-student at the School for Computer Science, Tel-Aviv University, Tel Aviv 69978, ISRAEL.
:::

::: IEEEbiography
Dan Halperin is a Professor at the School for Computer Science, Tel-Aviv University, Tel Aviv 69978, ISRAEL.
:::

[^1]: This work has been supported in part by the 7th Framework Programme for Research of the European Commission, under FET-Open grant number 255827 (CGL---Computational Geometry Learning), by the Israel Science Foundation (grant no. 1102/11), by the German-Israeli Foundation (grant no. 1150-82.6/2011), and by the Hermann Minkowski--Minerva Center for Geometry at Tel Aviv University.

[^2]: A preliminary and partial version of this manuscript appeared in the proceedings of the 2014 IEEE International Conference on Robotics and Automation (ICRA 2014), pages 4680-4685.

[^3]: A stopping criterion can be, for example, reaching a certain number of samples or exceeding a fixed time budget.

[^4]: The subscript of $\ensuremath{\mathcal{G}}_{lb}$ is an abbreviation for lower bound and the subscript of $\ensuremath{\mathcal{T}}_{apx}$ is an abbreviation for approximation.

[^5]: The number of nodes $\delta$ updated during an SSSP procedure depends on the topology of the graph and the edge weights. Theoretically, in the worst case $\delta = O(n)$ and a dynamic SSSP algorithm cannot perform better than recomputing shortest paths from scratch. However, in practice this value is much smaller.

[^6]: The Maze Scenario and the Cubicles Scenario are provided as part of the OMPL distribution.
