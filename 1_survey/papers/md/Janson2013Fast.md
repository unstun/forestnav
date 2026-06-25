---
citation_key: Janson2013Fast
arxiv_id: 1306.3532
arxiv_url: "https://arxiv.org/abs/1306.3532"
title: "Fast Marching Tree: a Fast Marching Sampling-Based Method for Optimal Motion Planning in Many Dimensions"
authors_short: "Lucas Janson et al."
year: 2013
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T10:05:02Z
origin: ai+web
reviewed: false
---

# Fast Marching Tree: a Fast Marching Sampling-Based Method for Optimal Motion Planning in Many Dimensions∗

Lucas Janson Department of Statistics, Stanford University ljanson@stanford.edu

Edward Schmerling Institute for Computational & Mathematical Engineering, Stanford University schmrlng@stanford.edu

Ashley Clark Department of Aeronautics and Astronautics, Stanford University aaclark@stanford.edu

Marco Pavone Department of Aeronautics and Astronautics, Stanford University pavone@stanford.edu

February 9, 2015

## Abstract

In this paper we present a novel probabilistic sampling-based motion planning algorithm called the Fast Marching Tree algorithm (FMT<sup>∗</sup>). The algorithm is specifically aimed at solving complex motion planning problems in high-dimensional configuration spaces. This algorithm is proven to be asymptotically optimal and is shown to converge to an optimal solution faster than its state-of-the-art counterparts, chiefly PRM<sup>∗</sup> and RRT<sup>∗</sup>. The FMT<sup>∗</sup> algorithm performs a “lazy” dynamic programming recursion on a predetermined number of probabilistically-drawn samples to grow a tree of paths, which moves steadily outward in cost-to-arrive space. As such, this algorithm combines features of both single-query algorithms (chiefly RRT) and multiple-query algorithms (chiefly PRM), and is reminiscent of the Fast Marching Method for the solution of Eikonal equations. As a departure from previous analysis approaches that are based on the notion of almost sure convergence, the FMT<sup>∗</sup> algorithm is analyzed under the notion of convergence in probability: the extra mathematical flexibility of this approach allows for convergence rate bounds—the first in the field of optimal samplingbased motion planning. Specifically, for a certain selection of tuning parameters and configuration spaces, we obtain a convergence rate bound of order $O ( n ^ { - 1 / d + \rho } )$ , where n is the number of sampled points, d is the dimension of the configuration space, and $\rho$ is an arbitrarily small constant. We go on to demonstrate asymptotic optimality for a number of variations on FMT , namely when the configuration space is sampled non-uniformly, when the cost is not arc length, and when connections are made based on the number of nearest neighbors instead of a fixed connection radius. Numerical experiments over a range of dimensions and obstacle configurations confirm our theoretical and heuristic arguments by showing that FMT<sup>∗</sup>, for a given execution time, returns substantially better solutions than either PRM<sup>∗</sup> or RRT<sup>∗</sup>, especially in highdimensional configuration spaces and in scenarios where collision-checking is expensive.

## 1 Introduction

Probabilistic sampling-based algorithms represent a particularly successful approach to robotic motion planning problems in high-dimensional configuration spaces, which naturally arise, e.g., when controlling the motion of high degree-of-freedom robots or planning under uncertainty (Thrun et al., 2005; Lavalle, 2006). Accordingly, the design of rapidly converging sampling-based algorithms with sound performance guarantees has emerged as a central topic in robotic motion planning and represents the main thrust of this paper.

Specifically, the key idea behind probabilistic sampling-based algorithms is to avoid the explicit construction of the configuration space (which can be prohibitive in complex planning problems) and instead conduct a search that probabilistically probes the configuration space with a sampling scheme. This probing is enabled by a collision detection module, which the motion planning algorithm considers as a “black box” (Lavalle, 2006). Probabilistic sampling-based algorithms may be classified into two categories: multiple-query and single-query. Multiple-query algorithms construct a topological graph called a roadmap, which allows a user to eficiently solve multiple initial-state/goal-state queries. This family of algorithms includes the probabilistic roadmap algorithm (PRM) (Kavraki et al., 1996) and its variants, e.g., Lazy-PRM (Bohlin and Kavraki, 2000), dynamic PRM (Jaillet and Sim´eon, 2004), and PRM<sup>∗</sup> (Karaman and Frazzoli, 2011). In single-query algorithms, on the other hand, a single initial-state/goal-state pair is given, and the algorithm must search until it finds a solution, or it may report early failure. This family of algorithms includes the rapidly exploring random trees algorithm (RRT) (LaValle and Kufner, 2001), the rapidly exploring dense trees algorithm (RDT) (Lavalle, 2006), and their variants, e.g., RRT<sup>∗</sup> (Karaman and Frazzoli, 2011). Other notable sampling-based planners include expansive space trees (EST) (Hsu et al., 1999; Phillips et al., 2004), sampling-based roadmap of trees (SRT) (Plaku et al., 2005), rapidly-exploring roadmap (RRM) (Alterovitz et al., 2011), and the “cross-entropy” planner in (Kobilarov, 2012). Analysis in terms of convergence to feasible or even optimal solutions for multiple-query and single-query algorithms is provided in (Kavraki et al., 1998;

Hsu et al., 1999; Barraquand et al., 2000; Ladd and Kavraki, 2004; Hsu et al., 2006; Karaman and Frazzoli, 2011). A central result is that these algorithms provide probabilistic completeness guarantees in the sense that the probability that the planner fails to return a solution, if one exists, decays to zero as the number of samples approaches infinity (Barraquand et al., 2000). Recently, it has been proven that both RRT<sup>∗</sup> and PRM<sup>∗</sup> are asymptotically optimal, i.e., the cost of the returned solution converges almost surely to the optimum (Karaman and Frazzoli, 2011). Building upon the results in (Karaman and Frazzoli, 2011), the work in (Marble and Bekris, 2012) presents an algorithm with provable “sub-optimality” guarantees, which “trades” optimality with faster computation, while the work in (Arslan and Tsiotras, 2013) presents a variant of RRT<sup>∗</sup>, named RRT<sup>#</sup>, that is also asymptotically optimal and aims to mitigate the “greediness” of RRT<sup>∗</sup>.

Statement of Contributions: The objective of this paper is to propose and analyze a novel probabilistic motion planning algorithm that is asymptotically optimal and improves upon state-of-the-art asymptotically-optimal algorithms, namely RRT<sup>∗</sup> and PRM<sup>∗</sup> . Improvement is measured in terms of the convergence rate to the optimal solution, where convergence rate is interpreted with respect to execution time. The algorithm, named the Fast Marching Tree algorithm (FMT<sup>∗</sup>), is designed to reduce the number of obstacle collisionchecks and is particularly eficient in high-dimensional environments cluttered with obstacles. FMT<sup>∗</sup> essentially performs a forward dynamic programming recursion on a predetermined number of probabilistically-drawn samples in the configuration space, see Figure 1. The recursion is characterized by three key features, namely (1) it is tailored to disk-connected graphs, (2) it concurrently performs graph construction and graph search, and (3) it lazily skips collision-checks when evaluating local connections. This lazy collision-checking strategy may introduce suboptimal connections—the crucial property of FMT is that such suboptimal connections become vanishingly rare as the number of samples goes to infinity.

FMT<sup>∗</sup> combines features of PRM and SRT (which is similar to RRM) and grows a tree of trajectories like RRT. Additionally, FMT<sup>∗</sup> is reminiscent of the Fast Marching Method, one of the main methods for solving stationary Eikonal equations (Sethian, 1996). We refer the reader to (Valero-Gomez et al., 2013) and references therein for a recent overview of path planning algorithms inspired by the Fast Marching Method. As in the Fast Marching Method, the main idea is to exploit a heapsort technique to systematically locate the proper sample point to update and to incrementally build the solution in an “outward” direction, so that the algorithm needs never backtrack over previously evaluated sample points. Such a one-pass property is what makes both the Fast Marching Method and FMT<sup>∗</sup> (in addition to its lazy strategy) particularly eficient<sup>1</sup>.

The end product of the FMT<sup>∗</sup> algorithm is a tree, which, together with the connection to the Fast Marching Method, gives the algorithm its name. Our simulations across a variety of problem instances, ranging in obstacle clutter and in dimension from 2D to 7D, show that FMT outperforms state-of-the-art algorithms such as PRM<sup>∗</sup> and RRT<sup>∗</sup>, often by a significant margin. The speedups are particularly prominent in higher dimensions and in scenarios where collision-checking is expensive, which is exactly the regime in which sampling-based algorithms excel. FMT also presents a number of “structural” advantages, such as maintaining a tree structure at all times and expanding in cost-to-arrive space, which have been recently leveraged to include diferential constraints (Schmerling et al., 2014a,b), to provide a bidirectional implementation (Starek et al., 2014), and to speed up the convergence rate even further via the inclusion of lower bounds on cost (Salzman and Halperin, 2014) and heuristics (Gammell et al., 2014).

It is important to note that in this paper we use a notion of asymptotic optimality (AO) diferent from the one used in (Karaman and Frazzoli, 2011). In (Karaman and Frazzoli, 2011), AO is defined through the notion of convergence almost everywhere (a.e.). Explicitly, in (Karaman and Frazzoli, 2011), an algorithm is considered AO if the cost of the solution it returns converges a.e. to the optimal cost as the number of samples n approaches infinity. This definition is apt when the algorithm is sequential in $n ,$ , such as $\mathrm { R R T ^ { * } }$ (Karaman and Frazzoli, 2011), in the sense that it requires that with probability 1 the sequence of solutions converges to an optimal one, with the solution at $n { + 1 }$ heavily related to that at n. However, for non-sequential algorithms such as PRM<sup>∗</sup> and $\mathrm { F M T ^ { * } }$ , there is no connection between the solutions at n and $n + 1$ . Since these algorithms process all the samples at once, the solution at $n + 1$ is based on $n + 1$ new samples, sampled independently of those used in the solution at n. This motivates the definition of AO used in this paper, which is that the cost of the solution returned by an algorithm must converge in probability to the optimal cost. Although convergence in probability is a mathematically weaker notion than convergence a.e. (the latter implies the former), in practice there is no distinction when an algorithm is only run on a predetermined, fixed number of samples. In this case, all that matters is that the probability that the cost of the solution returned by the algorithm is less than an ε fraction greater than the optimal cost goes to 1 as $n \to \infty$ , for any $\varepsilon > 0 .$ , which is exactly the statement of convergence in probability. Since this convergence is a mathematically weaker, but practically identical condition, we sought to capitalize on the extra mathematical flexibility, and indeed find that our proof of AO for FMT allows for a tighter theoretical lower bound on the search radius of $\mathrm { P R M ^ { * } }$ than was found in (Karaman and Frazzoli, 2011). In this regard, an additional important contribution of this paper is the analysis of AO under the notion of convergence in probability, which is of independent interest and could enable the design and analysis of other AO sampling-based algorithms.

Most importantly, our proof of AO gives a convergence rate bound with respect to the number of sampled points both for FMT<sup>∗</sup> and PRM<sup>∗</sup> —the first in the field of optimal sampling-based motion planning. Specifically, for a certain selection of tuning parameters and configuration space, we derive a convergence rate bound of $O ( n ^ { - 1 / d + \rho } )$ , where n is the number of sampled points, d is the dimension of the configuration space, and $\rho$ is an arbitrarily small constant. While the algorithms exhibit the slow convergence rate typical of sampling-based algorithms, the rate is at least a power of $n$ .

Organization: This paper is structured as follows. In Section 2 we formally define the optimal path planning problem. In Section 3 we present a high-level description of FMT<sup>∗</sup>, describe the main intuition behind its correctness, conceptually compare it to existing AO algorithms, and discuss its implementation details. In Section 4 we prove the asymptotic optimality of FMT<sup>∗</sup>, derive convergence rate bounds, and characterize its computational complexity. In Section 5 we extend FMT along three main directions, namely non-uniform sampling strategies, general cost functions, and a variant of the algorithm that relies on knearest-neighbor computations. In Section 6 we present results from numerical experiments supporting our statements. Finally, in Section 7, we draw some conclusions and discuss directions for future work.

![](Janson2013Fast_figs/369a0ae70ebea21fa02b5b849d25aef68c4836b3c305db580432fe7793089068.jpg)  
Figure 1: The FMT<sup>∗</sup> algorithm generates a tree by moving steadily outward in cost-to-arrive space. This figure portrays the growth of the tree in a 2D environment with 2,500 samples (only edges are shown).

Notation: Consider the Euclidean space in d dimensions, i.e., $\mathbb { R } ^ { d }$ . A ball of radius $r > 0$ centered at $\bar { x } \in \mathbb { R } ^ { d }$ is defined as $B ( \bar { x } ; \ r ) : = \{ x \in \mathbb { R } ^ { d } | \| x - \bar { x } \| < r \}$ . Given a subset of $\mathbb { R } ^ { d }$ its boundary is denoted by ∂ and its closure is denoted by cl( ). Given two points x and y in $\mathbb { R } ^ { d }$ , the line connecting them is denoted by xy. Let $\zeta _ { d }$ denote the volume of the unit ball in d-dimensional Euclidean space. The cardinality of a set S is written as card S. Given a set $\mathcal { X } \subseteq \mathbb { R } ^ { d } , \mu ( \mathcal { X } )$ denotes its d-dimensional Lebesgue measure. Finally, the complement of a probabilistic event A is denoted by A<sup>c</sup>.

## 2 Problem Setup

The problem formulation follows closely the problem formulation in (Karaman and Frazzoli, 2011), with two subtle, yet important diferences, namely a notion of regularity for goal regions and a refined definition of path clearance. Specifically, let $\mathcal { X } = [ 0 , 1 ] ^ { d }$ be the configuration space, where the dimension, d, is an integer larger than or equal to two. Let $\mathcal { X } _ { \mathrm { o b s } }$ be the obstacle region, such that ${ \mathcal { X } } \setminus { \mathcal { X } } _ { \mathrm { o b s } }$ is an open set (we consider $\partial \mathcal { X } \subset \mathcal { X } _ { \mathrm { o b s } } )$ . The obstacle-free space is defined as $\mathcal X _ { \mathrm { f r e e } } = \mathrm { c l } ( \mathcal X \setminus \mathcal X _ { \mathrm { o b s } } )$ . The initial condition $x _ { \mathrm { i n i t } }$ is an element of $\chi _ { \mathrm { f r e e } } .$ , and the goal region $\mathcal { X } _ { \mathrm { g o a l } }$ is an open subset of $\mathcal { X } _ { \mathrm { f r e e } }$ . A path planning problem is denoted by a triplet $( \mathcal { X } _ { \mathrm { f r e e } } , \boldsymbol { x } _ { \mathrm { i n i t } } , \mathcal { X } _ { \mathrm { g o a l } } )$ . A function $\sigma : [ 0 , 1 ] \to \mathbb { R } ^ { d }$ is called a path if it is continuous and has bounded variation, see (Karaman and Frazzoli, 2011, Section 2.1) for a formal definition. In the setup of this paper, namely, for continuous functions on a bounded, one-dimensional domain, bounded variation is exactly equivalent to finite length. A path is said to be collision-free if $\sigma ( \tau ) \in \mathcal { X } _ { \mathrm { f r e e } }$ for all $\tau \in [ 0 , 1 ]$ . A path is said to be a feasible path for the planning problem $( \mathcal { X } _ { \mathrm { f r e e } } , \boldsymbol { x } _ { \mathrm { i n i t } } , \mathcal { X } _ { \mathrm { g o a l } } )$ if it is collision-free, $\sigma ( 0 ) = x _ { \mathrm { i n i t } }$ , and $\sigma ( 1 ) \in \mathrm { c l } ( \mathcal { X } _ { \mathrm { g o a l } } )$

A goal region $\mathcal { X } _ { \mathrm { g o a l } }$ is said to be regular if there exists $\xi > 0$ such that $\forall x \in \partial \mathcal { X } _ { \mathrm { g o a l } }$ , there exists a ball in the goal region, say $B ( \bar { x } ; \xi ) \subseteq \mathcal { X } _ { \mathrm { g o a l } }$ , such that $x$ is on the boundary of the ball, i.e., $x \in \partial B ( \bar { x } ; \xi )$ . In other words, a regular goal region is a “well-behaved” set where the boundary has bounded curvature. We will say $\mathcal { X } _ { \mathrm { g o a l } }$ is ξ-regular if $\mathcal { X } _ { \mathrm { g o a l } }$ is regular for the parameter $\xi .$ Such a notion of regularity, not present in (Karaman and Frazzoli, 2011), is needed because to return a feasible solution, there must be samples in $\mathcal { X } _ { \mathrm { g o a l } }$ , and for that solution to be near-optimal, some samples must be near the edge of $\mathcal { X } _ { \mathrm { g o a l } }$ where the optimal path meets it. The notion of ξ-regularity essentially formalizes the notion of $\mathcal { X } _ { \mathrm { g o a l } }$ having enough measure near this edge to ensure that points are sampled near it.

Let Σ be the set of all paths. A cost function for the planning problem $( \mathcal { X } _ { \mathrm { f r e e } } , \boldsymbol { x } _ { \mathrm { i n i t } } , \mathcal { X } _ { \mathrm { g o a l } } )$ is a function $c : \Sigma  \mathbb { R } _ { > 0 }$ from the set of paths to the set of nonnegative real numbers; in this paper we will mainly consider cost functions $c ( \sigma )$ that are the arc length of $\sigma$ with respect to the Euclidean metric in $\mathcal { X }$ (recall that $\sigma$ is, by definition, rectifiable). Extension to more general cost functions, potentially not satisfying the triangle inequality are discussed in Section 5.2. The optimal path planning problem is then defined as follows:

Optimal path planning problem: Given a path planning problem $( \mathcal { X } _ { \mathrm { f r e e } } , \boldsymbol { x } _ { \mathrm { i n i t } } , \mathcal { X } _ { \mathrm { g o a l } } )$ with a regular goal region and an arc length function $c : \ \Sigma  \mathbb { R } _ { \geq 0 }$ , find a feasible path $\sigma ^ { * }$ such that $c ( \sigma ^ { * } ) = \operatorname* { m i n } \{ c ( \sigma ) : \sigma$ is feasible<sub>}</sub>. If no such path exists, report failure.

Finally, we introduce some definitions concerning the clearance of a path, i.e., its “distance” from $\mathcal { X } _ { \mathrm { o b s } }$ (Karaman and Frazzoli, 2011). For a given $\delta > 0$ , the δ-interior of $\mathcal { X } _ { \mathrm { f r e e } }$ is defined as the set of all points that are at least a distance $\delta$ away from any point in $\mathcal { X } _ { \mathrm { o b s } }$ . A collision-free path $\sigma$ is said to have strong δ-clearance if it lies entirely inside the δ-interior of $\mathcal { X } _ { \mathrm { f r e e } }$ . A path planning problem with optimal path cost $c ^ { * }$ is called δ-robustly feasible if there exists a strictly positive sequence $\delta _ { n } \to 0$ , with $\delta _ { n } \leq \delta \ \forall n \in \mathbb { N } .$ , and a sequence $\{ \sigma _ { n } \} _ { n = 1 } ^ { \infty }$ of feasible paths such that $\begin{array} { r } { \operatorname* { l i m } _ { n \to \infty } c ( \sigma _ { n } ) = c ^ { * } } \end{array}$ and for all $n \in \mathbb { N } , \sigma _ { n }$ has strong $\delta _ { n } \mathrm { - c l e a r a n c e } .$ $\sigma _ { n } ( 1 ) \in \partial \mathcal { X } _ { \mathrm { g o a l } } , \sigma _ { n } ( \tau ) \notin \mathcal { X } _ { \mathrm { g o a l } }$ for all $\tau \in ( 0 , 1 )$ , and $\sigma _ { n } ( 0 ) = x _ { \mathrm { i n i t } }$ . Note this definition is slightly diferent mathematically than admitting a robustly optimal solution as in (Karaman and Frazzoli, 2011), but the two are nearly identical in practice. Briefly, the diference is necessitated by the definition of a homotopy class only involving pointwise limits, as opposed to limits in bounded variation norm, making the conditions of a robustly optimal solution potentially vacuously satisfied.

## 3 The Fast Marching Tree Algorithm (FMT∗)

In this section we present the Fast Marching Tree algorithm (FMT<sup>∗</sup>). In Section 3.1 we provide a high-level description. In Section 3.2 we present some basic properties and discuss the main intuition behind $\mathrm { F M T ^ { * } s }$ design. In Section 3.3 we conceptually compare $\mathrm { F M T ^ { * } }$ to existing AO algorithms and discuss its structural advantages. Finally, in Section 3.4 we provide a detailed description of $\mathrm { F M T ^ { * } }$ together with implementation details, which will be instrumental to the computational complexity analysis given in Section 4.3.

## 3.1 High-Level Description

The FMT<sup>∗</sup> algorithm performs a forward dynamic programming recursion over a predetermined number of sampled points and correspondingly generates a tree of paths by moving steadily outward in cost-to-arrive space (see Figure 1). The dynamic programming recursion performed by FMT<sup>∗</sup> is characterized by three key features:

It is tailored to disk-connected graphs, where two samples are considered neighbors, and hence connectable, if their distance is below a given bound, referred to as the connection radius.

It performs graph construction and graph search concurrently.

For the evaluation of the immediate cost in the dynamic programming recursion, the algorithm “lazily” ignores the presence of obstacles, and whenever a locally-optimal (assuming no obstacles) connection to a new sample intersects an obstacle, that sample is simply skipped and left for later as opposed to looking for other connections in the neighborhood.

The first feature concerns the fact that FMT<sup>∗</sup> exploits the structure of disk-connected graphs to run dynamic programming for shortest path computation, in contrast with successive approximation schemes (as employed, e.g., by label-correcting methods). This aspect of the algorithm is illustrated in Section 3.2, in particular, in Theorem 3.2 and Remark 3.3. An extension of FMT<sup>∗</sup> to k-nearest-neighbor graphs, which are structurally very similar to disk-connected graphs, is studied in Section 5.3 and numerically evaluated in Section 6. The last feature, which makes the algorithm “lazy” and represents the key innovation, dramatically reduces the number of costly collision-check computations. However, it may cause suboptimal connections. A central property of FMT<sup>∗</sup> is that the cases where a suboptimal connection is made become vanishingly rare as the number of samples goes to infinity, which is key in proving that the algorithm is AO (Sections 3.2 and 4).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Fast Marching Tree Algorithm (FMT$^*$): Basics

Require: sample set $V$ comprising of $x_{\text{init}}$ and $n$ samples in $\mathcal{X}_{\text{free}}$, at least one of which is also in $\mathcal{X}_{\text{goal}}$

1: Place $x_{\text{init}}$ in $V_{\text{open}}$ and all other samples in $V_{\text{unvisited}}$; initialize tree with root node $x_{\text{init}}$

2: Find lowest-cost node $z$ in $V_{\text{open}}$

3: For each of $z$'s neighbors $x$ in $V_{\text{unvisited}}$:

4: Find neighbor nodes $y$ in $V_{\text{open}}$

5: Find locally-optimal one-step connection to $x$ from among nodes $y$

6: If that connection is collision-free, add edge to tree of paths

7: Remove successfully connected nodes $x$ from $V_{\text{unvisited}}$ and add them to $V_{\text{open}}$

8: Remove $z$ from $V_{\text{open}}$ and add it to $V_{\text{closed}}$

9: Repeat until either:

(1) $V_{\text{open}}$ is empty $\Rightarrow$ report failure

(2) Lowest-cost node $z$ in $V_{\text{open}}$ is in $\mathcal{X}_{\text{goal}} \Rightarrow$ return unique path to $z$ and report success
</div>

A basic pseudocode description of FMT<sup>∗</sup> is given in Algorithm 1. The input to the algorithm, besides the path planning problem definition, i.e., $( \mathcal { X } _ { \mathrm { f r e e } } , \boldsymbol { x } _ { \mathrm { i n i t } } , \mathcal { X } _ { \mathrm { g o a l } } )$ , is a sample set $V$ comprising $x _ { \mathrm { i n i t } }$ and n samples in $\chi _ { \mathrm { { f r e e } } } \ ( \mathrm { { l i n e } \ 1 ) }$ . We refer to samples added to the tree of paths as nodes. Two samples u, $v \in V$ are considered neighbors if their Euclidean distance is smaller than

$$
r _ {n} = \gamma \left(\frac {\log (n)}{n}\right) ^ {1 / d},
$$

where $\gamma > 2 \left( 1 / d \right) ^ { 1 / d } \left( \mu ( \mathcal { X } _ { \mathrm { f r e e } } ) / \zeta _ { d } \right) ^ { 1 / d }$ is a tuning parameter. The algorithm makes use of a partition of $\dot { V }$ into three subsets, namely $V _ { \mathrm { u n v i s i t e d } } , V _ { \mathrm { o p e n } } ,$ and $V _ { \mathrm { c l o s e d } }$ . The set $V _ { \mathrm { u n v i s i t e d } }$ consists of all of the samples that have not yet been considered for addition to the incrementally grown tree of paths. The set $V _ { \mathrm { o p e n } }$ contains samples that are currently active, in the sense that they have already been added to the tree $( \mathrm { i . e . , a }$ collision-free path from $x _ { \mathrm { i n i t } }$ with a given cost-toarrive has been found) and are candidates for further connections to samples in $V _ { \mathrm { u n v i s i t e d } }$ . The set $V _ { \mathrm { c l o s e d } }$ contains samples that have been added to the tree and are no longer considered for any new connections. Intuitively, these samples are not near enough to the edge of the expanding tree to actually have any new connections made with $V _ { \mathrm { u n v i s i t e d } }$ . Removing them from $V _ { \mathrm { o p e n } }$ reduces the number of nodes that need to be considered as neighbors for sample x. The FMT<sup>∗</sup> algorithm initially places $x _ { \mathrm { i n i t } }$ into $V _ { \mathrm { o p e n } }$ and all other samples in $V _ { \mathrm { u n v i s i t e d } }$ , while $V _ { \mathrm { c l o s e d } }$ is initially empty (line 1). The algorithm then progresses by extracting the node with the lowest cost-to-arrive in $V _ { \mathrm { o p e n } }$ (line 2, Figure $2 ( \mathrm { a } ) )$ , call it $z ,$ and finds all its neighbors within $V _ { \mathrm { u n v i s i t e d } }$ , call them x samples (line 3, Figure $2 ( \mathrm { a } ) )$ ). For each sample $x ,$ , FMT<sup>∗</sup> finds all its neighbors within $V _ { \mathrm { o p e n } } ,$ , call them $y$ nodes (line 4, Figure 2(b)). The algorithm then evaluates the cost of all paths to $x$ obtained by concatenating previously computed paths to nodes y with straight lines connecting them to $x ,$ referred to as “local one-step” connections. Note that this step lazily ignores the presence of obstacles. FMT<sup>∗</sup> then picks the path with lowest cost-to-arrive to $x$ (line 5, Figure $2 ( \mathrm { b } ) )$ . If the last edge of this path, i.e., the one connecting x with one of its neighbors in $V _ { \mathrm { o p e n } }$ , is collision-free, then it is added to the tree (line 6, Figure $2 ( \mathrm { c } ) )$ . When all samples $x$ have been considered, the ones that have been successfully connected to the tree are added to $V _ { \mathrm { o p e n } }$ and removed from $V _ { \mathrm { u n v i s i t e d } }$ (line $^ { 7 , }$ Figure $2 ( \mathrm { d } ) )$ , while the others remain in $V _ { \mathrm { u n v i s i t e d } }$ until a further iteration of the algorithm<sup>2</sup>. Additionally, node z is inserted into $V _ { \mathrm { c l o s e d } }$ (line 8, Figure 2(d)), and FMT<sup>∗</sup> moves to the next iteration (an iteration comprises lines 2–8). The algorithm terminates when the lowest-cost node in $V _ { \mathrm { o p e n } }$ is also in the goal region or when $V _ { \mathrm { o p e n } }$ becomes empty. Note that at the beginning of each iteration every sample in V is either in $V _ { \mathrm { o p e n } } \ o r$ in $V _ { \mathrm { u n v i s i t e d } } ~ o r$ in $V _ { \mathrm { c l o s e d } }$

A few comments are in order. First, the choice of the connection radius relies on a trade-of between computational complexity (roughly speaking, more neighbors lead to more computation) and quality of the computed path (roughly speaking, more neighbors lead to more paths to optimize over), and is an important parameter in the analysis and implementation of FMT<sup>∗</sup>. This choice will be studied theoretically in Section 4 and numerically in Section 6.3.2. Second, as shown in Figure 2, $\mathrm { F M T ^ { * } }$ concurrently performs graph construction and graph search, which is carried out via a dynamic programming recursion tailored to disk graphs (see Section 3.2). This recursion lazily skips collision-checks and may indeed introduce suboptimal connections. In Section 3.2 we will intuitively discuss why such suboptimal connections are very rare and still allow the algorithm to asymptotically approach an optimal solution (Theorem 4.1). Third, the lazy collision-checking strategy employed by FMT<sup>∗</sup> is fundamentally diferent from the one proposed in the past within the probabilistic roadmap framework (Bohlin and Kavraki, 2000), (S´anchez and Latombe, 2003). Specifically, the lazy PRM algorithm presented in (Bohlin and Kavraki, 2000) first constructs a graph assuming that all connections are collision-free (refer to this graph as the optimistic graph). Then, it searches for a shortest collision-free path by repeatedly searching for a shortest path over the optimistic graph and then checking whether it is collision-free or not. Each time a collision is found, the corresponding edge is removed from the optimistic graph and a new shortest path is computed. The “Single-query, Bi-directional, Lazy in collision-checking” algorithm, SBL (S´anchez and Latombe, 2003), implements a similar idea within the context of bidirectional search. In contrast to lazy PRM and SBL, FMT concurrently performs graph construction and graph search, and as soon as a shortest path to the goal region is found, that path is guaranteed to be collision-free. This approach provides computational savings in especially cluttered environments, wherein lazy PRM-like algorithms will require a large number of attempts to find a collision-free shortest path.

## 3.2 Basic Properties and Intuition

This section discusses basic properties of the FMT<sup>∗</sup> algorithm and provides intuitive reasoning about its correctness and efectiveness. We start by showing that the algorithm terminates in at most n steps, where n is the number of samples.

Theorem 3.1 (Termination). Consider a path planning problem $( \mathcal { X } _ { f r e e } , \boldsymbol { x } _ { i n i t } , \mathcal { X } _ { g o a l } )$ and any $n \in \mathbb N$ The FMT<sup>∗</sup> algorithm always terminates in at most n iterations $( i . e . ,$ in n loops through Algorithm 1 lines 2–8).

Proof. Note two key facts: (i) FMT<sup>∗</sup> terminates and reports failure if $V _ { \mathrm { o p e n } }$ is ever empty, and (ii) the lowest-cost node in $V _ { \mathrm { o p e n } }$ is removed from $V _ { \mathrm { o p e n } }$ at each iteration. Therefore, to prove the theorem it sufices to prove the invariant that any sample that has ever been added to $V _ { \mathrm { o p e n } }$ can never be added again. To establish the invariant, observe that at a given iteration, only samples in $V _ { \mathrm { u n v i s i t e d } }$ can be added to $V _ { \mathrm { o p e n } ; }$ and each time a sample is added, it is removed from $V _ { \mathrm { u n v i s i t e d } }$ . Finally, since $V _ { \mathrm { u n v i s i t e d } }$ never has samples added to it, a sample can only be added to $V _ { \mathrm { o p e n } }$ once. Thus the invariant is proved, and, in turn, the theorem.

To understand the correctness of the algorithm, consider first the case without obstacles and where there is only one sample in $\mathcal { X } _ { \mathrm { g o a l } }$ , denoted by $x _ { \mathrm { { t e r m i n a l } } }$ . In this case $\mathrm { F M T ^ { * } }$ uses dynamic programming to find the shortest path from $x _ { \mathrm { i n i t } }$ to $x _ { \mathrm { { t e r m i n a l } } } .$ if one exists, over the $r _ { n } { \mathrm { - d i s k } }$ graph induced by $V , \mathrm { i . e . }$ , over the graph where there exists an edge between two samples $u , v \in V$ if and only $\mathrm { i f ~ } \| u - v \| ~ < r _ { n }$ . This fact is proven in the following theorem, the proof of which highlights how FMT<sup>∗</sup> applies dynamic programming over an $r _ { n } .$ -disk graph.

Theorem 3.2 (FMT<sup>∗</sup> in obstacle-free environments). Consider a path planning problem $( \mathcal { X } _ { f r e e } , \boldsymbol { x } _ { \mathrm { i n i t } } , \mathcal { X } _ { g o a l } )$ , where $\mathcal { X } _ { f r e e } = \mathcal { X } ~ ( i . e .$ , there are no obstacles) and $\mathcal { X } _ { g o a l } = \{ x _ { \mathrm { t e r m i n a l } } \} ~ ( i . e .$

![](Janson2013Fast_figs/88ea54615e1ec5b7040b3e88b2b4c0e3bdf7e1961f34e9425dac34a7aa0d2a9e.jpg)  
(a) Lines 2–3: FMT<sup>∗</sup> selects the lowest-cost node z from set $V _ { \mathrm { o p e n } }$ and finds its neighbors within V<sub>unvisited</sub>.

![](Janson2013Fast_figs/e814682fdb1be0baed7a69ce03d31481ff801073556022e43db5226b2754a943.jpg)  
(b) Lines 4–5: given a neighboring node $x ,$ FMT<sup>∗</sup> finds the neighbors of x within $V _ { \mathrm { o p e n } }$ and searches for a locally-optimal one-step connection. Note that paths intersecting obstacles are also lazily considered.

![](Janson2013Fast_figs/f9290a6631db099f6e5b603cd2f41357923d81a4386eaeff2d77224c76059063.jpg)  
(c) Line 6: FMT<sup>∗</sup> selects the locally-optimal onestep connection to x ignoring obstacles, and adds that connection to the tree if it is collision-free.

![](Janson2013Fast_figs/e93c3828627c6cad0b85352c7c0a47a2dc37ecae80cd854207f8a7c01e5ce8f9.jpg)  
(d) Lines 7–8: After all neighbors of z in V<sub>unvisited</sub> have been explored, FMT<sup>∗</sup> adds successfully connected nodes to $V _ { \mathrm { o p e n } } ,$ places z in $V _ { \mathrm { c l o s e d } }$ , and moves to the next iteration.  
Figure 2: An iteration of the FMT<sup>∗</sup> algorithm. FMT<sup>∗</sup> lazily and concurrently performs graph construction and graph search. Line references are with respect to Algorithm 1. In panel (b), node z is re-labeled as node y since it is one of the neighbors of node x.

there is a single node in $\mathcal { X } _ { g o a l } )$ . Then, FMT<sup>∗</sup> computes a shortest path from $x _ { \mathrm { i n i t } }$ to x<sub>terminal</sub> $( i f$ one exists) over the $r _ { n } { - } d i s k$ graph induced by V .

Proof. For a sample $v \in V .$ , let $c ( v )$ be the length of a shortest path to v from $x _ { \mathrm { i n i t } }$ over the $r _ { n ^ { - } }$ disk graph induced by V , where $c ( v ) = \infty$ if no path to v exists. Furthermore, let Cost $( u , v )$ be the length of the edge connecting samples u and $v \ \mathrm { ( i . e . } ,$ , its Euclidean distance). It is well known that shortest path distances satisfy the Bellman principle of optimality (Cormen et al., 2001, Chapter 24), namely

$$
c (v) = \min _ {u: \| u - v \| <   r _ {n}} \left\{c (u) + \operatorname{Cost} (u, v) \right\}.\tag{1}
$$

FMT<sup>∗</sup> repeatedly applies this relation in a way that exploits the geometry of $r _ { n }$ -disk graphs. Specifically, FMT<sup>∗</sup> maintains two loop invariants:

Invariant 1: At the beginning of each iteration, the shortest path in the $r _ { n } .$ -disk graph to a sample $v \in V _ { \mathrm { u n v i s i t e d } }$ must pass through a node $u \in V _ { \mathrm { o p e n } }$

To prove Invariant 1, assume for contradiction that the invariant is not true, that is there exists a sample $v \in V _ { \mathrm { u n v i s i t e d } }$ with a shortest path that does not contain any node in $V _ { \mathrm { o p e n } }$ . At the first iteration this condition is clearly false, as $x _ { \mathrm { i n i t } }$ is in $V _ { \mathrm { o p e n } }$ . For subsequent iterations, the contradiction assumption implies that along the shortest path there is at least one edge $( u , w )$ where $u \in V _ { \mathrm { c l o s e d } }$ and $w \in V _ { \mathrm { u n v i s i t e d } }$ . This situation is, however, impossible as before u is placed in $V _ { \mathrm { c l o s e d } }$ , all its neighbors, including v, must have been extracted from $V _ { \mathrm { u n v i s i t e d } }$ and inserted into $V _ { \mathrm { o p e n } } ,$ since insertion into $V _ { \mathrm { o p e n } }$ is ensured when there are no obstacles. Thus, we have a contradiction.

The second invariant is:

Invariant 2: At the end of each iteration, all neighbors of z in $V _ { \mathrm { u n v i s i t e d } }$ are placed in $V _ { \mathrm { o p e n } }$ with their shortest paths computed.

To see this, let us induct on the number of iterations. At the first iteration, Invariant 2 is trivially true. Consider, then, iteration $i + 1$ and let $x \in V _ { \mathrm { u n v i s i t e d } }$ be a neighbor of z. In line 5 of Algorithm 1, $\mathrm { F M T ^ { * } }$ computes a path to x with cost $\tilde { c } ( x )$ given by

$$
\tilde {c} (x) = \min _ {u \in V _ {\mathrm{open}}: \| u - x \| <   r _ {n}} \bigl \{c (u) + \mathsf {C o s t} (u, x) \bigr \},
$$

where by the inductive hypothesis the shortest paths to nodes in $V _ { \mathrm { o p e n } }$ are all known, since all nodes placed in $V _ { \mathrm { o p e n } }$ before or at iteration i have had their shortest paths computed. To prove that $\tilde { c } ( x )$ is indeed equal to the cost of a shortest path to $x , { \mathrm { i . e . , } } c ( x )$ , we need to prove that the Bellman principle of optimality is satisfied, that is

$$
\min _ {u \in V _ {\text {open}}: \| u - x \| <   r _ {n}} \left\{c (u) + \mathsf {C o s t} (u, x) \right\} = \min _ {u: \| u - x \| <   r _ {n}} \left\{c (u) + \mathsf {C o s t} (u, x) \right\}.\tag{2}
$$

To prove the above equality, note first that there are no nodes $u \in V _ { \mathrm { c l o s e d } }$ such that $\| u - x \| <$ $r _ { n }$ , otherwise x could not be in $V _ { \mathrm { u n v i s i t e d } }$ (by using the same argument from the proof of Invariant 1). Consider, then, samples $u \in V _ { \mathrm { u n v i s i t e d } }$ such that $\| u - v \| < r _ { n }$ . From Invariant 1 we know that a shortest path to u must pass through a node $w \in V _ { \mathrm { o p e n } }$ . If w is within a distance $r _ { n }$ from x, then, by the triangle inequality, we obtain a shorter path by concatenating a shortest path to w with the edge connecting w and x—hence, u can be discarded when looking for a shortest path to x. If, instead, w is farther than a distance $r _ { n }$ from x, we can write by repeatedly applying the triangle inequality:

$$
c (u) + \operatorname{Cost} (u, x) \geq c (w) + \operatorname{Cost} (w, x) \geq c (w) + r _ {n}.
$$

Since $c ( w ) \geq c ( z )$ due to the fact that nodes are extracted from $V _ { \mathrm { o p e n } }$ in order of their cost-to-arrive, and since Cost $( z , x ) < r _ { n }$ , we obtain

$$
c (u) + \mathsf {C o s t} (u, x) > c (z) + \mathsf {C o s t} (z, x),
$$

which implies that, again, u can be discarded when looking for a shortest path to x. Thus, equality (2) is proved and, in turn, Invariant 2.

Given Invariant 2, the theorem is proven by showing that, if there exists a path from $x _ { \mathrm { i n i t } }$ to $x _ { \mathrm { { t e r m i n a l } } } .$ , at some iteration the lowest-cost node in $V _ { \mathrm { o p e n } }$ is $x _ { \mathrm { { t e r m i n a l } } }$ and $\mathrm { F M T ^ { * } }$ terminates, reporting “success,” see line 9 in Algorithm 1. We already know, by Theorem 3.1, that FMT<sup>∗</sup> terminates in at most n iterations. Assume by contradiction that upon termination $V _ { \mathrm { o p e n } }$ is empty, which implies that $x _ { \mathrm { { t e r m i n a l } } }$ never entered $V _ { \mathrm { o p e n } }$ and hence is in $V _ { \mathrm { u n v i s i t e d } }$ . This situation is impossible, since the shortest path to $x _ { \mathrm { t e r m i n a l } }$ would contain at least one edge $( u , w )$ with $u \in V _ { \mathrm { c l o s e d } }$ and $w \in V _ { \mathrm { u n v i s i t e d } }$ , which as argued in the proof of Invariant 1 cannot happen. Thus the theorem is proved. □

Remark 3.3 (FMT<sup>∗</sup>, dynamic programming, and disk-graphs). The functional equation (1) does not constitute an algorithm, it only stipulates an optimality condition. FMT implements equation (1) by exploiting the structure of disk-connected graphs. Specifically, in the obstaclefree case, the disk-connectivity structure ensures that FMT<sup>∗</sup> visits nodes in a ordering compatible with directly computing (1), that is, while computing the left hand side of equation (1) (i.e., the shortest path value c(v)), all the relevant shortest path values on the right hand side (i.e., the values c(u)) have already been computed (see proof of Invariant 2). In this sense, FMT computes shortest paths by running direct dynamic programming, as opposed to performing successive approximations as done by label-setting or label-correcting algorithms, e.g., Dijkstra’s algorithm or the Bellman–Ford algorithm (Bertsekas, 2005, Chapter 2). We refer the reader to Sniedovich (2006) for an in-depth discussion of the diferences between direct dynamic programming methods (such as FMT ) and successive approximation methods (such as Dijkstra’s algorithm) for shortest path computation. Such a direct approach is desirable since the cost-to-arrive value for each node is updated only once, and thus only one collision check is required per node in the obstacle-free case. When obstacles are introduced, FMT<sup>∗</sup> sacrifices the ability to return an exact solution on the obstacle-free disk graph in order to retain the computational eficiency of the direct approach. The suboptimality introduced in this way is slight, as we prove in Section 4, and only one collision check is required for the majority of nodes. FMT ’s strategy is reminiscent of the approach used for the computation of shortest paths over acyclic graphs (Sniedovich, 2006). Indeed, the idea of leveraging graph structure to compute shortest paths over disk graphs is not new and was recently investigated in (Roditty and Segal, 2011)—under the name of bounded leg shortest path problem—and in (Cabello and Jejˇciˇc, 2014). Both works, however, do not use “direct” dynamic programming arguments, but rather combine Dijkstra’s algorithm with the concept of bichromatic closest pairs (Chan and Efrat, 2001).

Theorem 3.2 shows that in the obstacle-free case $\mathrm { F M T ^ { * } }$ returns a shortest path, if one exists, over the $r _ { n } .$ -disk graph induced by the sample set V . This statement no longer holds, however, when there are obstacles, as in this case $\mathrm { F M T ^ { * } }$ might make connections that are suboptimal, i.e., that do not satisfy the Bellman principle of optimality. Specifically, FMT<sup>∗</sup> will make a suboptimal connection when exactly four conditions are satisfied. Let $u _ { 1 }$ be the optimal parent of x with respect to the r<sub>n</sub>-disk graph where edges intersecting obstacles are removed. This graph is the “correct” graph $\mathrm { F M T ^ { * } }$ should plan over if it were not lazy. The sample x will not be connected to $u _ { 1 }$ by $\mathrm { F M T ^ { * } }$ only if when $u _ { 1 }$ is the lowestcost node in $V _ { \mathrm { o p e n } }$ , there is another node $u _ { 2 } \in V _ { \mathrm { o p e n } }$ such that (a) $u _ { 2 }$ is within a radius $r _ { n }$ of x, (b) $u _ { 2 }$ has greater cost-to-arrive than $u _ { 1 } , \mathrm { ( c ) }$ obstacle-free connection of x to $u _ { 2 }$ would have lower cost-to-arrive than connection to $u _ { 1 }$ , and (d) $u _ { 2 }$ is blocked from connecting to x by an obstacle. These four conditions are illustrated in Figure 3. Condition (a) is required because in order for $u _ { 2 }$ to be connected to $x ,$ it must be within the connection radius of $x .$ Conditions (b), (c), and (d) combine as follows: condition (b) dictates that $u _ { 1 }$ will be pulled from $V _ { \mathrm { o p e n } }$ before $u _ { 2 }$ is. Due to (c), $u _ { 2 }$ will be chosen as the potential parent of x. Condition (d) will cause the algorithm to discard the edge between them, and $u _ { 1 }$ will be removed from $V _ { \mathrm { o p e n } } .$ , never to be evaluated again. Thus, in the future, the algorithm will never realize that $u _ { 1 }$ was a better parent for x. If condition (b) were to fail, then $u _ { 2 }$ would be pulled from $V _ { \mathrm { o p e n } }$ first, would unsuccessfully attempt to connect to $x ,$ and then would be removed from $V _ { \mathrm { o p e n } }$ , leaving x free to connect to $u _ { 1 }$ in a future iteration. If condition (c) were to fail, the algorithm would attempt to connect x to $u _ { 1 }$ instead of $u _ { 2 }$ and would therefore find the optimal connection. If condition (d) were to fail, then $u _ { 2 }$ would indeed be the optimal parent of $x ,$ and so the optimal connection would be formed. Thus, if any of one these four conditions fail, then at some iteration (possibly not the first), x will be connected optimally with respect to the “correct” graph. Note that the combination of conditions (a), (b), (c), and (d) make such suboptimal connections quite rare. Additionally, samples must be within distance $r _ { n }$ of an obstacle to achieve joint satisfaction of conditions (a), (b), (c), and (d), and Lemma C.2 shows that the fraction of samples which lie within $r _ { n }$ of an obstacle goes to zero as $n \to \infty$ . Furthermore, Theorem 4.1 shows that such suboptimal connections do not afect the AO of FMT<sup>∗</sup> .

## 3.3 Conceptual Comparison with Existing AO Algorithms and Advantages of FMT∗

When there are no obstacles, FMT<sup>∗</sup> reports the exact same solution or failure as PRM<sup>∗</sup> . This property follows from the fact that, without obstacles, FMT<sup>∗</sup> is indeed using dynamic programming to build the minimum-cost spanning tree, as shown in Theorem 3.2. With obstacles, for a given sample set, FMT finds a path with a cost that is lower-bounded by, and does not substantially exceed, the cost of the path found by PRM<sup>∗</sup>, due to the suboptimal connections made by lazily ignoring obstacles in the dynamic programming recursion. However, as will be shown in Theorem 4.1, the cases where FMT<sup>∗</sup> makes a suboptimal connection are rare enough that as $n  \infty , \mathrm { F M T ^ { * } }$ , like PRM<sup>∗</sup>, converges to an optimal solution.

![](Janson2013Fast_figs/7be6193afb61deb86436ee8d43e6b6e537e4dff1580bd0877955b17cde51a1ae.jpg)  
Figure 3: Illustration of a case where FMT<sup>∗</sup> would make a suboptimal connection. FMT<sup>∗</sup> is designed so that suboptimal connections are “rare” in general, and vanishingly rare as n <sub>∞</sub><sup>.</sup>

While lazy collision-checking might introduce suboptimal connections, it leads to a key computational advantage. By only checking for collision on the locally-optimal (assuming no obstacles) one-step connection, as opposed to every possible connection as is done in PRM<sup>∗</sup>, FMT<sup>∗</sup> saves a large number of costly collision-check computations. Indeed, the ratio of the number of collision-check computations in FMT<sup>∗</sup> to those in PRM<sup>∗</sup> goes to zero as the number of samples goes to infinity. Hence, we expect FMT<sup>∗</sup> to outperform PRM<sup>∗</sup> in terms of solution cost as a function of time.

A conceptual comparison to RRT<sup>∗</sup> is more dificult, given how diferently RRT<sup>∗</sup> generates paths as compared with FMT<sup>∗</sup>. The graph expansion procedure of RRT<sup>∗</sup> is fundamentally diferent from that of FMT<sup>∗</sup>. While FMT<sup>∗</sup> samples points throughout the free space and makes connections independently of the order in which the samples are drawn, at each iteration RRT<sup>∗</sup> steers towards a new sample only from the regions it has reached up until that time. In problems where the solution path is necessarily long and winding it may take a long time for an ordered set of points traversing the path to present steering targets for RRT<sup>∗</sup>. In this case, a lot of time can be wasted by steering in inaccessible directions before a feasible solution is found. Additionally, even once the search trees for both algorithms have explored the whole space, one may expect FMT<sup>∗</sup> to show some improvement in solution quality per number of samples placed. This improvement comes from the fact that, for a given set of samples, FMT creates connections nearly optimally (exactly optimally when there are no obstacles) within the radius constraint, while RRT<sup>∗</sup>, even with its rewiring step, is fundamentally a greedy algorithm. It is, however, hard to conceptually assess how long the algorithms might take to run on a given set of samples, although in terms of collision-check computations, we will show in Lemma C.2 that FMT<sup>∗</sup> performs O(1) collision-checks per sample, while RRT performs O(log(n)) per sample. In Section 6.2 we will present results from numerical experiments to make these conceptual comparisons concrete and assess the benefits of FMT<sup>∗</sup> over RRT<sup>∗</sup> .

An efective approach to address the greedy behavior of RRT<sup>∗</sup> is to leverage relaxation methods for the exploitation of new connections (Arslan and Tsiotras, 2013). This approach is the main idea behind the RRT<sup>#</sup> algorithm (Arslan and Tsiotras, 2013), which constructs a spanning tree rooted at the initial condition and containing lowest-cost path information for nodes which have the potential to be part of a shortest path to the goal region. This approach is also very similar to what is done by FMT<sup>∗</sup>. However, $\mathrm { R R T } ^ { \# }$ grows the tree in a fundamentally diferent way, by interleaving the addition of new nodes and corresponding edges to the graph with a Gauss–Seidel relaxation of the Bellman equation (1); it is essentially the same relaxation used in the $\mathrm { L P A } ^ { * }$ algorithm (Koenig et al., 2004). This last step propagates the new information gained with a node addition across the whole graph in order to improve the cost-to-arrive values of “promising” nodes (Arslan and Tsiotras, 2013). In contrast, FMT directly implements the Bellman equation (1) and, whenever a new node is added to the tree, considers only local, i.e. within a neighborhood, connections. Furthermore, and perhaps most importantly, $\mathrm { F M T ^ { * } }$ implements a lazy collision-checking strategy, which on the practical side may significantly reduce the number of costly collision-checks, while on the theoretical side requires a careful analysis of possible suboptimal local connections (see Section 3.2 and Theorem 4.1). It is also worth mentioning that over n samples FMT<sup>∗</sup> has a computational complexity that is $O ( n$ log n) (Theorem 4.7), while $\mathrm { R R T } ^ { \# }$ has a computational complexity of $O ( n ^ { 2 } \log { n } )$ (Arslan and Tsiotras, 2013).

Besides providing fast convergence to high quality solutions, FMT<sup>∗</sup> has some “structural” advantages with respect to its state-of-the-art counterparts. First, $\mathrm { F M T ^ { * } }$ , like PRM<sup>∗</sup>, relies on the choice of two parameters, namely the number of samples and the constant appearing in the connection radius in equation (3). In contrast, RRT<sup>∗</sup> requires the choice of four parameters, namely, the number of samples or termination time, the steering radius, the goal biasing, and the constant appearing in the connection radius. An advantage of $\mathrm { F M T ^ { * } }$ over PRM<sup>∗</sup>, besides the reduction in the number of collision-checks (see Section 3.1), is that FMT<sup>∗</sup> builds and maintains paths in a tree structure at all times, which is advantageous when diferential constraints are added to the paths. In particular, far fewer two-point boundary value problems need to be solved (see the recent work in (Schmerling et al., 2014a)). Also, the fact that the tree grows in cost-to-arrive space simplifies a bidirectional implementation, as discussed in (Starek et al., 2014). Finally, while $\mathrm { F M T ^ { * } }$ , by running on a predetermined number of samples, is not an anytime algorithm (roughly speaking, an algorithm is called anytime ${ \mathrm { i f } } ,$ given extra time, it continues to run and further improve its solution until time runs out—a notable example is $\mathrm { R R T ^ { * } } )$ , it can be cast into this framework by repeatedly adding batches of samples and carefully reusing previous computation until time runs out, as recently presented in (Salzman and Halperin, 2014).

## 3.4 Detailed Description and Implementation Details

This section provides a detailed pseudocode description of Algorithm 1, which highlights a number of implementation details that will be instrumental to the computational complexity analysis given in Section 4.3.

Let SampleFree $( n )$ be a function that returns a set of $n \in \mathbb N$ points (samples) sampled independently and identically from the uniform distribution on $\mathcal { X } _ { \mathrm { f r e e } }$ We discuss the extension to non-uniform sampling distributions in Section 5.1. Let V be a set of samples containing the initial state $x _ { \mathrm { i n i t } }$ and a set of $n$ points sampled according to SampleFree(n). Given a subset $V ^ { \prime } \subseteq V$ , and a sample $v \in V$ , let $\mathtt { S a v e } ( V ^ { \prime } , v )$ be a function that stores in memory a set of samples $V ^ { \prime }$ associated with sample $v .$ Given a set of samples $V .$ , a sample $v \in V$ , and a positive number $r _ { \mathrm { : } }$ let Near $( V , v , r )$ be a function that returns the set of samples $\{ u \in V : \| u - v \| < r \}$ . Near checks first to see if the required set of samples has already been computed and saved using Save, in which case it loads the set from memory, otherwise it computes the required set from scratch. Paralleling the notation in the proof of Theorem 3.2, given a tree $T = ( V ^ { \prime } , E )$ , where the node set $V ^ { \prime } \subseteq V$ contains $x _ { \mathrm { i n i t } }$ and E is the edge set, and a node $v \in V ^ { \prime }$ , let $c ( v )$ be the cost of the unique path in the graph $T$ from $x _ { \mathrm { i n i t } }$ to v. Given two samples $u , v \in V$ , let Cost $( u , v )$ be the cost of the straight line joining u and v (in the current setup Cost $( u , v ) = \| v - u \|$ , more general costs will be discussed in Section 5.2). Note that Cost $( u , v )$ is well-defined regardless of the line joining u and v being collision-free. Given two samples $u , v \in V$ , let CollisionFree $( u , v )$ denote the boolean function which is true if and only if the line joining u and v does not intersect an obstacle. Given a tree $T = ( V ^ { \prime } , E )$ , where the node set $V ^ { \prime } \subseteq V$ contains $x _ { \mathrm { i n i t } }$ and $E$ is the edge set, and a node $v \in V ^ { \prime }$ , let Path $( v , T )$ be the function returning the unique path in the tree $T$ from $x _ { \mathrm { i n i t } }$ to v. The detailed $\mathrm { F M T ^ { * } }$ algorithm is given in Algorithm 2.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Fast Marching Tree Algorithm (FMT*): Details
1  $V \leftarrow \{x_{init}\} \cup SampleFree(n); E \leftarrow \emptyset$ 
2  $V_{unvisited} \leftarrow V \backslash \{x_{init}\}; V_{open} \leftarrow \{x_{init}\}, V_{closed} \leftarrow \emptyset$ 
3  $z \leftarrow x_{init}$ 
4  $N_z \leftarrow Near(V \backslash \{z\}, z, r_n)$ 
5  $Save(N_z, z)$ 
6 while  $z \notin X_{goal}$  do
7  $V_{open,new} \leftarrow \emptyset$ 
8  $X_{near} = N_z \cap V_{unvisited}$ 
9 for  $x \in X_{near}$  do
10  $N_x \leftarrow Near(V \backslash \{x\}, x, r_n)$ 
11  $Save(N_x, x)$ 
12  $Y_{near} \leftarrow N_x \cap V_{open}$ 
13  $y_{min} \leftarrow arg min_{y \in Y_{near}} \{c(y) + Cost(y, x)\} // dynamic programming equation$ 
14 if CollisionFree( $y_{min}, x$ ) then
15  $E \leftarrow E \cup \{(y_{min}, x)\} // straight line joining y_{min} and x is collision-free$ 
16  $V_{open,new} \leftarrow V_{open,new} \cup \{x\}$ 
17  $V_{unvisited} \leftarrow V_{unvisited} \backslash \{x\}$ 
18  $c(x) = c(y_{min}) + Cost(y_{min}, x) // cost-to-arrive from x_{init} in tree T = (V_{open} \cup V_{closed}, E)$ 
19 end if
20 end for
21  $V_{open} \leftarrow (V_{open} \cup V_{open,new}) \backslash \{z\}$ 
22  $V_{closed} \leftarrow V_{closed} \cup \{z\}$ 
23 if  $V_{open} = \emptyset$  then
24 return Failure
25 end if
26  $z \leftarrow arg min_{y \in V_{open}} \{c(y)\}$ 
27 end while
28 return Path( $z, T = (V_{open} \cup V_{closed}, E)$ )
</div>

The set $V _ { \mathrm { o p e n } }$ should be implemented as a binary min heap, ordered by cost-to-arrive, with a parallel set of nodes that exactly tracks the nodes in $V _ { \mathrm { o p e n } }$ in no particular order, and that is used to eficiently carry out the intersection operation in line 12 of the algorithm. Set $V _ { \mathrm { o p e n } . }$ , new contains successfully connected x samples that will be added to $V _ { \mathrm { o p e n } }$ once all x samples have been considered (compare with line 7 in Algorithm 1). At initialization (line 5) and during the main while loop (line 11), $\mathrm { F M T ^ { * } }$ saves the information regarding the nearest neighbor set of a node v, that is $N _ { v }$ . This operation is needed to avoid unnecessary repeated computations of near neighbors by allowing the Near function to load from memory, and will be important for the characterization of the computational complexity of $\mathrm { F M T ^ { * } }$ in Theorem 4.7. Substituting lines 10–12 with the line $Y _ { \mathrm { n e a r } } \gets \mathtt { N e a r } ( V _ { \mathrm { o p e n } } , x , r _ { n } )$ , while algorithmically correct, would cause a larger number of unnecessary near neighbor computations. Additionally, for each node $u \in$ $N _ { v }$ , one should also save the real value Cos $; ( u , v )$ and the boolean value CollisionFree $( u , v )$ Saving both of these values whenever they are first computed guarantees that FMT<sup>∗</sup> will never compute them more than once for a given pair of nodes.

## 4 Analysis of FMT∗

In this section we characterize the asymptotic optimality of $\mathrm { F M T ^ { * } }$ (Section 4.1), provide a convergence rate to the optimal solution (Section 4.2), and finally characterize its computational complexity (Section 4.3).

## 4.1 Asymptotic Optimality

The following theorem presents the main result of this paper.

Theorem 4.1 (Asymptotic optimality of $\mathrm { F M T ^ { * } } )$ . Let $( \mathcal { X } _ { f r e e } , \boldsymbol { x } _ { i n i t } , \mathcal { X } _ { g o a l } )$ be a δ-robustly feasible path planning problem in d dimensions, with $\delta > 0$ and $\mathcal { X } _ { g o a l }$ being ξ-regular. Let $c ^ { * }$ denote the arc length of an optimal path $\sigma ^ { * }$ , and let $c _ { n }$ denote the arc length of the path returned by FMT<sup>∗</sup> (or if FMT<sup>∗</sup> returns failure) with n samples using the following radius,

$$
r _ {n} = (1 + \eta) 2 \left(\frac {1}{d}\right) ^ {1 / d} \left(\frac {\mu (\mathcal {X} _ {f r e e})}{\zeta_ {d}}\right) ^ {1 / d} \left(\frac {\log (n)}{n}\right) ^ {1 / d},\tag{3}
$$

for some $\eta > 0$ . Then $\begin{array} { r } { \operatorname* { l i m } _ { n  \infty } \mathbb { P } ( c _ { n } > ( 1 + \varepsilon ) c ^ { * } ) = 0 } \end{array}$ for all $\varepsilon > 0$

Proof. Note that $c ^ { * } = 0$ implies $x _ { \mathrm { i n i t } } \in \mathrm { c l } ( \mathcal { X } _ { \mathrm { g o a l } } )$ , and the result is trivial, therefore assume $c ^ { * } > 0$ . Fix $\theta \in ( 0 , 1 / 4 )$ and define the sequence of paths $\sigma _ { n }$ such that $\begin{array} { r } { \operatorname* { l i m } _ { n \to \infty } c ( \sigma _ { n } ) = c ^ { * } } \end{array}$ $\sigma _ { n } ( 1 ) \in \partial \mathscr { X } _ { \mathrm { g o a l } } , \sigma _ { n } ( \tau ) \notin \mathscr { X } _ { \mathrm { g o a l } }$ for all $\tau \in ( 0 , 1 ) , \sigma _ { n } ( 0 ) = x _ { \mathrm { i n i t } }$ , and $\sigma _ { n }$ has strong $\delta _ { n } \mathrm { - c l e a r a n c e }$ where $\begin{array} { r } { \delta _ { n } = \operatorname* { m i n } \{ \delta , \frac { 3 + \theta } { 2 + \theta } r _ { n } \} } \end{array}$ . Such a sequence of paths must exist by the δ-robust feasibility of the path planning problem. The parameter $\theta$ will be used to construct balls that cover a path of interest, and in particular will be the ratio of the separation of the ball centers to their radii (see Figure 4 for an illustration).

The path $\sigma _ { n }$ ends at $\partial \mathcal { X } _ { \mathrm { g o a l } } ;$ we will define $\sigma _ { n } ^ { \prime }$ as $\sigma _ { n }$ with a short extension into the interior of $\mathcal { X } _ { \mathrm { g o a l } }$ . Specifically, $\boldsymbol { \sigma } _ { n } ^ { \prime }$ is $\sigma _ { n }$ concatenated with the line of length min $\textstyle \left\{ \xi , { \frac { r _ { n } } { 2 ( 2 + \theta ) } } \right\}$ that extends from $\sigma _ { n } ( 1 )$ into $\mathcal { X } _ { \mathrm { g o a l } }$ , exactly perpendicular to the tangent hyperplane of $\partial \mathcal { X } _ { \mathrm { g o a l } }$ at $\sigma _ { n } ( 1 )$ . Note that this tangent hyperplane is well-defined, since the regularity assumption for $\mathcal { X } _ { \mathrm { g o a l } }$ ensures that its boundary is diferentiable. Note that, trivially, lim $\begin{array} { r } { \mathfrak { l } _ { n \to \infty } c ( \sigma _ { n } ^ { \prime } ) = } \end{array}$ $\begin{array} { r } { \operatorname* { l i m } _ { n \to \infty } c ( \sigma _ { n } ) = c ^ { * } } \end{array}$ This line extension is needed because a path that only reaches the boundary of the goal region can be arbitrarily well-approximated in bounded variation norm by paths that are not actually feasible because they do not reach the goal region, and we need to ensure that FMT<sup>∗</sup> finds feasible solution paths that approximate an optimal path.

Fix $\varepsilon \in ( 0 , 1 )$ , suppose $\alpha , \beta \in ( 0 , \theta \varepsilon / 8 )$ , and pick $n _ { 0 } \in \mathbb { N }$ such that for all $n \geq n _ { 0 }$ the following conditions hold: $\begin{array} { r } { ( 1 ) \frac { r _ { n } } { 2 ( 2 + \theta ) } < \xi , ( 2 ) \frac { 3 + \theta } { 2 + \theta } r _ { n } < \delta , ( 3 ) c ( \sigma _ { n } ^ { \prime } ) < ( 1 + \frac { \varepsilon } { 4 } ) c ^ { * } } \end{array}$ , and (4) $\begin{array} { r } { \frac { r _ { n } } { 2 + \theta } < \frac { \varepsilon } { 8 } c ^ { * } } \end{array}$ . Both α and $\beta$ are parameters for controlling the smoothness of $\mathrm { F M T ^ { * } } { \mathrm { ? } }$ s solution, and will be used in the proofs of Lemmas 4.2 and 4.3.

For the remainder of this proof, assume $n \geq n _ { 0 }$ . From conditions (1) and $( 2 ) , \sigma _ { n } ^ { \prime }$ has strong $\frac { 3 + \theta } { 2 + \theta } r _ { n }$ -clearance. For notational simplicity, let $\kappa ( \alpha , \beta , \theta ) : = 1 + ( 2 \alpha + 2 \beta ) / \theta$ , in which case conditions (3) and (4) imply,

$$
\begin{array}{l} \kappa (\alpha , \beta , \theta)   c (\sigma_ {n} ^ {\prime}) + \frac {r _ {n}}{2 + \theta} \leq \kappa (\alpha , \beta , \theta) \bigg (1 + \frac {\varepsilon}{4} \bigg)   c ^ {*} + \frac {\varepsilon}{8}   c ^ {*} \\ \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \leq \bigg (\bigg (1 + \frac {\varepsilon}{2} \bigg) \bigg (1 + \frac {\varepsilon}{4} \bigg) + \frac {\varepsilon}{8} \bigg)   c ^ {*} \leq (1 + \varepsilon) c ^ {*}. \end{array}
$$

Therefore,

$$
\mathbb {P} \left(c _ {n} > (1 + \varepsilon) c ^ {*}\right) = 1 - \mathbb {P} \left(c _ {n} \leq (1 + \varepsilon) c ^ {*}\right) \leq 1 - \mathbb {P} \left(c _ {n} \leq \kappa (\alpha , \beta , \theta)   c (\sigma_ {n} ^ {\prime}) + \frac {r _ {n}}{2 + \theta}\right).\tag{4}
$$

Define the sequence of balls $B _ { n , 1 } , \ldots , B _ { n , M _ { n } } \subseteq { \mathcal { X } } _ { \mathrm { f r e e } }$ parameterized by $\theta$ as follows. For $m = 1$ we define $B _ { n , 1 } : = B { \biggl ( } \sigma _ { n } ( \tau _ { n , 1 } ) ; { \begin{array} { l } { r _ { n } } \\ { 2 + \theta } \end{array} } { \biggr ) }$ with $\tau _ { n , 1 } = 0$ . For $m = 2 , 3 , . . . ,$ let

$$
\Gamma_ {m} = \left\{\tau \in (\tau_ {n, m - 1}, 1): \| \sigma_ {n} (\tau) - \sigma_ {n} (\tau_ {n, m - 1}) \| = \frac {\theta r _ {n}}{2 + \theta} \right\};
$$

if $\Gamma _ { m } \neq \emptyset$ we define $\begin{array} { r } { B _ { n , m } : = B \bigg ( \sigma _ { n } ( \tau _ { n , m } ) ; \frac { r _ { n } } { 2 + \theta } \bigg ) } \end{array}$ with $\tau _ { n , m } = \operatorname* { m i n } _ { \tau } \Gamma _ { m }$ . Let $M _ { n }$ be the first m such that $\Gamma _ { m } = \emptyset$ , then, $B _ { n , M _ { n } } : = B { \biggl ( } \sigma _ { n } ^ { \prime } ( 1 ) ; { \frac { r _ { n } } { 2 ( 2 + \theta ) } } { \biggr ) }$ , and we stop the process, i.e., $B _ { n , M _ { n } }$ is the last ball placed along the path $\sigma _ { n }$ (note that the center of the last ball is $\sigma _ { n } ^ { \prime } ( 1 ) )$ .

![](Janson2013Fast_figs/ba0f6ac0a444bb5a568097889b82a96f0410d534a9038039c481fdc38d3666a6.jpg)  
Figure 4: An illustration of the covering balls $B _ { n , m }$ and associated smaller balls $B _ { n , m } ^ { \beta }$ . The figure also illustrates the role of $\xi$ in $\mathcal { X } _ { \mathrm { g o a l } }$ and the construction of $B _ { n , M _ { n } }$ . Note that θ (the ratio of the separation of the centers of the $B _ { n , m }$ to their radii) is depicted here as being around $2 / 3$ for demonstration purposes only, as the proof requires $\theta < 1 / 4$

Considering the construction of $\sigma _ { n } ^ { \prime }$ and condition (1) above, we conclude that $B _ { n , M _ { n } } \subseteq { \mathcal { X } } _ { \mathrm { g o a l } }$ See Figure 4 for an illustration of this construction.

Recall that V is the set of samples available to algorithm $\mathrm { F M T ^ { * } }$ (see line 1 in Algorithm 2). We define the event $\begin{array} { r } { A _ { n , \theta } : = \bigcap _ { m = 1 } ^ { M _ { n } } \{ B _ { n , m } \cap V \neq \emptyset \} ; A _ { n , \theta } } \end{array}$ is the event that each ball contains at least one (not necessarily unique) sample in $V$ . For clarity, we made the event’s dependence on $\theta ,$ due to the dependence on θ of the balls, explicit. Further, for all $m \in \{ 1 , \ldots , M _ { n } - 1 \}$ let $B _ { n , m } ^ { \beta }$ be the ball with the same center as $B _ { n , m }$ and radius $\frac { \beta r { } _ { n } } { 2 + \theta }$ , where $0 \leq \beta \leq 1$ , and let $K _ { n } ^ { \beta }$ be the number of smaller balls $B _ { n , m } ^ { \beta }$ not containing any of the samples in V , i.e., K<sup>β</sup> := card $\{ m \in \{ 1 , \dots , M _ { n } - 1 \} : B _ { n , m } ^ { \beta } \cap V = \emptyset \}$ . We again point the reader to Figure 4 to see the $B _ { n , m } ^ { \beta }$ depicted.

We now present three important lemmas; their proofs can be found in Appendix A.

Lemma 4.2 (FMT<sup>∗</sup> path quality). Under the assumptions of Theorem 4.1 and assuming $n \geq n _ { 0 }$ , the following inequality holds:

$$
\mathbb {P} \left(c _ {n} \leq \kappa (\alpha , \beta , \theta) c \left(\sigma_ {n} ^ {\prime}\right) + \frac {r _ {n}}{2 + \theta}\right) \geq 1 - \mathbb {P} \left(K _ {n} ^ {\beta} \geq \alpha \left(M _ {n} - 1\right)\right) - \mathbb {P} \left(A _ {n, \theta} ^ {c}\right).
$$

Lemma 4.3 (Tight approximation to most of the path). Under the assumptions of Theorem 4.1, for all $\alpha \in ( 0 , 1 )$ and $\beta \in \left( 0 , \theta / 2 \right)$ , it holds that

$$
\lim _ {n \to \infty} \mathbb {P} (K _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1)) = 0.
$$

Lemma 4.4 (Loose approximation to all of the path). Under the assumptions of Theorem $4 . 1 ,$ assume that

$$
r _ {n} = \gamma \left(\frac {\log n}{n}\right) ^ {1 / d},
$$

where

$$
\gamma = (1 + \eta) \cdot 2 \left(\frac {1}{d}\right) ^ {1 / d} \left(\frac {\mu (\mathcal {X} _ {f r e e})}{\zeta_ {d}}\right) ^ {1 / d},
$$

and $\eta > 0$ . Then for all $\begin{array} { r } { \theta < 2 \eta , \operatorname* { l i m } _ { n  \infty } \mathbb { P } ( A _ { n , \theta } ^ { c } ) = 0 } \end{array}$

Essentially, Lemma 4.2 provides a lower bound for the arc length of the solution delivered by FMT<sup>∗</sup> in terms of the probabilities that the “big” balls and “small” balls do not contain samples in V . Lemma 4.3 states that the probability that the fraction of small balls not containing samples in V is larger than an α fraction of the total number of balls is asymptotically zero. Finally, Lemma 4.4 states that the probability that at least one “big” ball does not contain any of the samples in V is asymptotically zero.

The asymptotic optimality claim of the theorem then follows easily. Let $\varepsilon \in ( 0 , 1 )$ and pick $\theta \in ( 0 , \operatorname* { m i n } \{ 2 \eta , 1 / 4 \} )$ and $\alpha , \beta \in ( 0 , \theta \varepsilon / 8 ) \subset ( 0 , \theta / 2 )$ . From equation (4) and Lemma 4.2, we can write

$$
\lim _ {n \to \infty} \mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \leq \lim _ {n \to \infty} \mathbb {P} (K _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1)) + \lim _ {n \to \infty} \mathbb {P} (A _ {n, \theta} ^ {c}).
$$

The right-hand side of this equation equals zero by Lemmas 4.3 and 4.4, and the claim is proven. The case with general ε follows by monotonicity in ε of the above probability.

Remark 4.5 (Application of Theorem 4.1 to PRM<sup>∗</sup>). Since the solution returned by $F M T ^ { * }$ is never better than the one returned by PRM<sup>∗</sup> on a given set of nodes, the exact same result holds for PRM<sup>∗</sup>. Note that this proof uses a γ which is a factor of $( d \mathrm { + } 1 ) ^ { 1 / d }$ smaller, and thus a $r _ { n }$ which is $( d \mathrm { + } 1 ) ^ { 1 / d }$ smaller, than that in Karaman and Frazzoli $( 2 0 1 1 )$ . Since the number of cost computations and collision-checks scales approximately as $r _ { n } ^ { d } ,$ this factor should reduce run time substantially for a given number of nodes, especially in high dimensions. This reduction is due to the diference in definitions of AO mentioned earlier which, again, makes no practical diference for PRM<sup>∗</sup> or FMT<sup>∗</sup> .

## 4.2 Convergence Rate

In this section we provide a convergence rate bound for $\mathrm { F M T ^ { * } }$ (and thus also for $\mathrm { P R M ^ { * } } )$ , assuming no obstacles. As far as the authors are aware, this bound is the first such convergence rate result for an optimal sampling-based motion planning algorithm and represents an important step towards understanding the behavior of this class of algorithms. The proof is deferred to Appendix B.

Theorem 4.6 (Convergence rate of $\mathrm { F M T ^ { * } } )$ . Let the configuration space be $[ 0 , 1 ] ^ { d }$ with no obstacles and the goal region be $[ 0 , 1 ] ^ { d } \cap B ( \vec { 1 } ; \xi )$ , where $\vec { 1 } = ( 1 , 1 , \dots , 1 )$ . Taking $x _ { i n i t }$ to be the center of the configuration space, the shortest path has length $c ^ { * } = \sqrt { d } / 2 - \xi$ and has clearance $\delta = \xi \sqrt { ( d - 1 ) / d }$ Denote the arc length of the path returned by FMT<sup>∗</sup> with n samples as $c _ { n }$ . For FMT<sup>∗</sup> run using the radius given by equation (3), namely,

$$
r _ {n} = (1 + \eta) 2 \left(\frac {1}{d}\right) ^ {1 / d} \left(\frac {\mu (\mathcal {X} _ {f r e e})}{\zeta_ {d}}\right) ^ {1 / d} \left(\frac {\log (n)}{n}\right) ^ {1 / d},
$$

for all $\varepsilon > 0$ , we have the following convergence rate bounds,

$$
\mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \in \left\{ \begin{array}{l l} O \left((\log (n)) ^ {- \frac {1}{d}} n ^ {\frac {1}{d} (1 - (1 + \eta) ^ {d}) + \rho}\right) & i f \quad \eta \leq \frac {2}{(2 ^ {d} - 1) ^ {1 / d}} - 1, \\ O \left(n ^ {- \frac {1}{d} (\frac {1 + \eta}{2}) ^ {d} + \rho}\right) & i f \quad \eta > \frac {2}{(2 ^ {d} - 1) ^ {1 / d}} - 1, \end{array} \right.\tag{5}
$$

as $n \to \infty$ , where $\rho$ is an arbitrarily small positive constant.

In agreement with the common opinion about sampling-based motion planning algorithms, our convergence rate bound converges to zero slowly, especially in high dimensions. Although the rate is slow, it scales as a power of n rather than, say, logarithmically. We have not, however, studied how tight the bound is—studying this rate is a potential area for future work. As expected, the rate of convergence increases as η increases. However, increasing η increases the amount of computation per sample, hence, to optimize convergence rate with respect to time one needs to properly balance these two competing efects. Note that if we select $\eta = 1$ , from equation (5) we obtain a remarkably simple form for the rate, namely $O ( n ^ { - 1 / d + \rho } )$ , which holds for PRM<sup>∗</sup> as well (we recall that for a given number of samples the solution returned by PRM<sup>∗</sup> is not worse than the one returned by FMT<sup>∗</sup> using the same connection radius). Note that the rate of convergence to a feasible (as opposed to optimal) solution for PRM and RRT is known to be exponential (Kavraki et al., 1998; LaValle and Kufner, 2001); unsurprisingly, our bound for converging to an optimal solution decreases more slowly, as it is not exponential.

We emphasize that our bound does not have a constant multiplying the rate that approaches infinity as the arbitrarily small parameter (in our case $\rho )$ approaches zero. In fact, the asymptotic constant multiplying the rate is 1, independent of the value of $\rho ,$ but the earliest n at which that rate holds approaches $\infty$ as $\rho \to 0$ . Furthermore, although our bound reflects the asymptotically dominant term (see equation (14) in the proof), there are two other terms which may contribute substantially or even dominate for finite n.

It is also of interest to bound $\mathbb { P } ( c _ { n } > ( 1 + \varepsilon ) c ^ { * } )$ by an asymptotic expression in ε, but unfortunately this cannot be gleaned from our results, since the closed-form bound we use in the proof (see again equation (14)) only holds for $n \geq n _ { 0 }$ , and $n _ { 0 } \stackrel { \varepsilon \to 0 } { \longrightarrow } \infty$ . Therefore fixing n and sending $\varepsilon  0$ just causes this bound to return 1 on a set $( 0 , \varepsilon _ { 0 } ( n ) )$ , which tells us nothing about the rate at which the true probability approaches 1 as $\varepsilon \to 0$

## 4.3 Computational Complexity

The following theorem, proved in Appendix C, characterizes the computational complexity of FMT<sup>∗</sup> with respect to the number of samples. It shows that FMT<sup>∗</sup> requires $O ( n \log ( n ) )$ operations in expectation, the same as PRM<sup>∗</sup> and RRT<sup>∗</sup>. It also highlights the computational savings of FMT<sup>∗</sup> over PRM<sup>∗</sup>, since in expectation FMT<sup>∗</sup> checks for edge collisions just $O ( n )$ times, while PRM<sup>∗</sup> does so $O ( n \log ( n ) )$ times. Ultimately, the most relevant complexity measure is how long it takes for an algorithm to return a solution of a certain quality. This measure, partially characterized in Section 4.2, will be studied numerically in Section 6.

Theorem 4.7 (Computational complexity of FMT<sup>∗</sup> ). Consider a path planning problem $( \mathcal { X } _ { f r e e } , \boldsymbol { x } _ { i n i t } , \mathcal { X } _ { g o a l } )$ and a set of samples V in $\chi _ { f r e e }$ of cardinality n, and fix

$$
r _ {n} = \gamma \left(\frac {\log (n)}{n}\right) ^ {1 / d},
$$

for some positive constant $\gamma .$ . In expectation, FMT takes $O ( n \log ( n ) )$ time to compute a solution on n samples, and in doing so, makes $O ( n )$ calls to CollisionFree (again in expectation). FMT<sup>∗</sup> also takes $O ( n \log ( n ) )$ space in expectation.

## 5 Extensions

This section presents three extensions to the setup considered in the previous section, namely, (1) non-uniform sampling strategies, (2) general cost functions instead of arc length, and (3) a version of FMT<sup>∗</sup>, named k-nearest FMT<sup>∗</sup>, in which connections are sought to k nearestneighbor nodes, rather than to nodes within a given distance.

For all three cases we discuss the changes needed to the baseline FMT<sup>∗</sup> algorithm presented in Algorithm 2 and then argue how FMT<sup>∗</sup> with these changes retains AO in $\mathrm { A p \mathrm { - } }$ pendices D–F. In the interest of brevity, we will only discuss the required modifications to existing theorems, rather than proving everything from scratch.

## 5.1 Non-Uniform Sampling Strategies

## 5.1.1 Overview

Sampling nodes from a non-uniform distribution can greatly help planning algorithms by incorporating outside knowledge of the optimal path into the algorithm itself (Hsu et al., 2006). (Of course if no outside knowledge exists, the uniform distribution may be a natural choice.) Specifically, we consider the setup whereby SampleFree(n) returns n points sampled independently and identically from a probability density function $\varphi$ supported over $\mathcal { X } _ { \mathrm { f r e e } }$ . We assume that $\varphi$ is bounded below by a strictly positive number \`. This lower bound on $\varphi$ allows us to make a connection between sampling from a non-uniform distribution and sampling from a uniform distribution, for which the proof of AO already exists (Theorem 4.1). This argument is worked through in Appendix D to show that $\mathrm { F M T ^ { * } }$ with non-uniform sampling is AO.

## 5.1.2 Changes to FMT<sup>∗</sup> Implementation

The only change that needs to be made to $\mathrm { F M T ^ { * } }$ is to multiply $r _ { n }$ by $( 1 / \ell ) ^ { 1 / d }$

## 5.2 General Costs

Another extension of interest is when the cost function is not as simple as arc length. We may, for instance, want to consider some regions as more costly to move through than others, or a cost that weights/treats movement along diferent dimensions diferently. In the following subsections, we explain how $\mathrm { F M T ^ { * } }$ can be extended to other metric costs, as well as line integral costs, and why its AO still holds.

Broadly speaking, the main change that needs to happen to $\mathrm { F M T ^ { * } s }$ implementation is that it needs to consider cost instead of Euclidean distance when searching for nearby points. For metric costs besides Euclidean cost (Section 5.2.1), a few adjustments to the constants are all that is needed in order to ensure AO. This is because the proof of AO in Theorem 4.1 relies on the cost being additive and obeying the triangle inequality. The same can be said for line integral costs if $\mathrm { F M T ^ { * } }$ is changed to search along and connect points by cost-optimal paths instead of straight lines (Section 5.2.2). Since such an algorithm may be hard to implement in practice, we lastly show in Section 5.2.3 that by making some Lipschitz assumptions on the cost function, we get an approximate triangle inequality for straight-line, cost-weighted connections. We present an argument for why this approximation is suficiently good to ensure that the suboptimality introduced in how parent nodes are chosen and in the edges themselves goes to zero asymptotically, and thus that AO is retained. All arguments for AO in this subsection are deferred to Appendix E.

## 5.2.1 Metric Costs

Overview: Consider as cost function any metric on , denoted by dist : $\mathcal { X } \times \mathcal { X } $ <sup>R</sup>. If the distance between points in is measured according to dist, the FMT<sup>∗</sup> algorithm requires very minor modifications, namely just a modified version of the Near function. Generalized metric costs allow one to account for, $\mathrm { e . g . }$ , diferent weightings on diferent dimensions, or an angular dimension which wraps around at $2 \pi$

Changes to $\mathbf { F M T ^ { * } s }$ implementation: Given two samples $u , v \in V$ , Cost $( u , v ) \ =$ dist $( u , v )$ . Accordingly, given a set of samples V , a sample $v \in V .$ , and a positive number r, Near $( V , v , r )$ returns the set of samples $\{ u \in V : \mathtt { C o s t } ( u , v ) < r \}$ . We refer to such sets as cost balls. Formally, everything else in Algorithm 2 stays the same, except $\zeta _ { d }$ in the definition of $r _ { n }$ needs to be defined as the Lebesgue measure of the unit cost-ball.

## 5.2.2 Line Integral Costs with Optimal-Path Connections

Overview: In some planning problems the cost function may not be a metric, i.e., it may not obey the triangle inequality. Specifically, consider the setup where $f : \mathcal { X } $ <sup>R</sup> is such that $0 < f _ { \mathrm { l o w e r } } \leq f ( x ) \leq f _ { \mathrm { u p p e r } } < \infty$ for all $x \in \mathcal { X }$ , and the cost of a path σ is given by

$$
\int_ {\sigma} f (s) d s.
$$

Note that in this setup a straight line is not generally the lowest-cost connection between two samples $u , v \in \mathcal { X } . \ \mathrm { F M T } ^ { * }$ , however, relies on straight lines in two ways: adjacent nodes in the FMT<sup>∗</sup> tree are connected with a straight line, and two samples are considered to be within r of one another if the straight line connecting them has cost less than r. In this section we consider a version of $\mathrm { F M T ^ { * } }$ whereby two adjacent nodes in the $\mathrm { F M T ^ { * } }$ tree are connected with the optimal path between them, and two nodes are considered to be within r of one another if the optimal path connecting them has cost less than r.

Changes to $\mathbf { F M T ^ { * } s }$ implementation: Given two nodes $u , v \in V$

$$
\mathsf {C o s t} (u, v) = \min _ {\sigma^ {\prime}} \int_ {\sigma^ {\prime}} f (s) d s,
$$

where $\sigma ^ { \prime }$ denotes a path connecting u and v. Given a set of nodes V , a node $v \in V$ , and a positive number $r ,$ Near $( V , v , r )$ returns the set of nodes $\{ u \in V : \mathtt { C o s t } ( u , v ) < r \}$ . Every time a node is added to a tree, its cost-optimal connection to its parent is also stored. Lastly, the definition of $r _ { n }$ needs to be multiplied by a factor of $f _ { \mathrm { u p p e r } } .$

## 5.2.3 Line Integral Costs with Straight-Line Connections

Overview: Computing an optimal path for a line integral cost for every connection, as considered in Section 5.2.2, may represent an excessive computational bottleneck. Two strategies to address this issue are (1) precompute such optimal paths since their computation does not require knowledge of the obstacle set, or (2) approximate such paths with costweighted, straight line paths and study the impact on AO. In this section we study the latter approach, and we argue that AO does indeed still hold, by appealing to asymptotics to show that the triangle inequality approximately holds, with this approximation going away as $n \to \infty$

Changes to FMT<sup>∗</sup>’s implementation: Given two samples $u , v \in V$

$$
\operatorname{Cost} (u, v) = \int_ {\overline {{u v}}} f (s) d s.
$$

Given a set of samples V , a sample $v \in V$ , and a positive number r, Near $( V , v , r )$ returns the set of samples $\{ u \in V : \mathtt { C o s t } ( u , v ) < r \}$ . Lastly, the definition of $r _ { n }$ needs to again be increased by a factor of $f _ { \mathrm { u p p e r } } .$

## 5.3 FMT∗ Using k-Nearest-Neighbors

## 5.3.1 Overview

A last variant of interest is to have a version of $\mathrm { F M T ^ { * } }$ which makes connections based on k-nearest-neighbors instead of a fixed cost radius. This variant, referred to as k-nearest FMT<sup>∗</sup>, has the advantage of being more adaptive to diferent obstacle spaces than its costradius counterpart. This is because FMT<sup>∗</sup> will consider about half as many connections for a sample very near an obstacle surface as for a sample far from obstacles, since about half the measure of the obstacle-adjacent-sample’s cost ball is inside the obstacle. k-nearest $\mathrm { F M T ^ { * } }$ on the other hand, will consider k connections for every sample. To prove AO for k-nearest FMT<sup>∗</sup> (in Appendix F), we will stray slightly from our main proof exposition in this paper and use the similarities between FMT<sup>∗</sup> and PRM<sup>∗</sup> to leverage a similar proof for k-nearest PRM<sup>∗</sup> from (Karaman and Frazzoli, 2011).

## 5.3.2 Changes to FMT<sup>∗</sup>’s Implementation

Two parts need to change in Algorithm 2, both about how Near works. The first is in lines 4 and 8, where $N _ { z }$ should be all samples $v \in V \backslash \{ z \}$ such that both v is a $k _ { n }$ -nearest-neighbor of z and z is a $k _ { n }$ -nearest-neighbor of v. We refer to this set as the mutual $k _ { n }$ -nearest-neighbor set of z. The second change is that in lines 10 and 12, $N _ { x }$ should be the usual $k _ { n }$ -nearestneighbor set of x, namely all samples $v \in V \setminus \{ x \}$ such that v is a $k _ { n } .$ -nearest-neighbor of x. Finally, $k _ { n }$ should be chosen so that

$$
k _ {n} = k _ {0} \log (n), \qquad \mathrm{where} k _ {0} > 3 ^ {d} e (1 + 1 / d).\tag{6}
$$

With these changes, k-nearest FMT<sup>∗</sup> works by repeatedly applying Bellman’s equation (1) over a k-nearest-neighbor graph, analogously to what is done in the disk-connected graph case (see Theorem 3.2). When we want to refer to the generic algorithm k-nearest FMT using the specific sequence $k _ { n }$ , and we want to make this use explicit, we will say $k _ { n } .$ -nearest FMT<sup>∗</sup>.

## 6 Numerical Experiments and Discussion

In this section we numerically investigate the advantages of FMT<sup>∗</sup> over previous AO samplingbased motion planning algorithms. Specifically, we compare FMT<sup>∗</sup> against RRT<sup>∗</sup> and PRM<sup>∗</sup>, as these two algorithms are state-of-the-art within the class of AO planners, span the main ideas (e.g., roadmaps versus trees) in the field of sampling-based planning, and have opensource, high quality implementations. We first present in Section 6.1 a brief overview of the simulation setup. We then compare FMT<sup>∗</sup>, RRT<sup>∗</sup>, and PRM<sup>∗</sup> in Section 6.2. Numerical experiments confirm our theoretical and heuristic arguments by showing that FMT<sup>∗</sup>, for a given execution time, returns substantially better solutions than RRT<sup>∗</sup> and PRM<sup>∗</sup> in a variety of problem settings. FMT ’s main computational speedups come from performing fewer collision checks—the more expensive collision-checking is, the more FMT<sup>∗</sup> will excel. Finally, in Section 6.3, we study in-depth FMT<sup>∗</sup> and its extensions (e.g., general costs). In particular, we provide practical guidelines about how to implement and tune FMT<sup>∗</sup>.

## 6.1 Simulation Setup

Simulations were written in a mix of C++ and Julia, and run using a Unix operating system with a 2.0 GHz processor and 8 GB of RAM. The C++ simulations were run through the Open Motion Planning Library (OMPL) (S¸ucan et al., 2012), from which the reference implementation of RRT<sup>∗</sup> was taken. We took the default values of RRT<sup>∗</sup> parameters from OMPL (unless otherwise noted below), in particular a steering parameter of 20% of the maximum extent of the configuration space, and a goal-bias probability of 5%. Also, since the only OMPL implementation of RRT<sup>∗</sup> is a k-nearest implementation, we adapted a k-nearest version of PRM<sup>∗</sup> and implemented a k-nearest version of FMT<sup>∗</sup>, both in OMPL; these are the versions used in Sections 6.1–6.2. In these two subsections, for notational simplicity, we will refer to the k-nearest versions of FMT<sup>∗</sup>, RRT<sup>∗</sup>, and PRM<sup>∗</sup> simply as FMT<sup>∗</sup>, RRT<sup>∗</sup>, and PRM<sup>∗</sup>, respectively. The three algorithms were run on test problems drawn from the bank of standard rigid body motion planning problems given in the OMPL.app graphical user interface. These problems, detailed below and depicted in Figure 5, are posed within the configuration spaces SE(2) and SE(3) which correspond to the kinematics (available translations and rotations) of a rigid body in 2D and 3D respectively. The dimension of the state space sampled by these planners is thus three in the case of SE(2) problems, and six in the case of SE(3) problems.

![](Janson2013Fast_figs/4b13510f80a6f0faceb6b23a45ea00d020b4e16499d48cc7b94367043d58888f.jpg)  
(a) SE(2) bug trap.

![](Janson2013Fast_figs/a0de5a5319dc09846d75780a10ef8ca82fc206150f082504ffce7c5c581066f5.jpg)  
(b) SE(2) maze.

![](Janson2013Fast_figs/3f270a54ece95b56749d2c229429c59e2eb252bdd4258d8e4686c699e97535cf.jpg)  
(c) SE(3) maze.

![](Janson2013Fast_figs/c90a4f6c440439d744534a5938b69f1dffaee2db2908a425c27186c4ccd53974.jpg)  
(d) SE(3) Alpha puzzle.  
Figure 5: Depictions of the OMPL.app SE(2) and SE(3) rigid body planning test problems.

We chose the Julia programming language (Bezanson et al., 2012) for the implementation of additional simulations because of its ease in accommodating the FMT<sup>∗</sup> extensions studied in Section 6.3. We constructed experiments with a robot modeled as a union of hyperrectangles in high-dimensional Euclidean space moving amongst hyperrectangular obstacles. We note that for both simulation setups, FMT<sup>∗</sup>, RRT<sup>∗</sup>, and PRM<sup>∗</sup> used the exact same primitive routines (e.g., nearest-neighbor search, collision-checking, data handling, etc.) to ensure a fair comparison. The choice of k for the nearest-neighbor search phase of each of the planning algorithms is an important tuning parameter (discussed in detail for $\mathrm { F M T ^ { * } }$ in Section 6.3.2). For the following simulations, unless otherwise noted, we used these coeficients for the nearest-neighbor count $k _ { n } = k _ { 0 } \log ( n )$ : given a state space dimension $d ,$ for RRT<sup>∗</sup> we used the OMPL default value $k _ { 0 , \mathrm { R R T ^ { * } } } ~ = ~ e + e / d ,$ and for $\mathrm { F M T ^ { * } }$ and PRM<sup>∗</sup> we used the value $k _ { 0 , \mathrm { F M T ^ { * } } } = k _ { 0 , \mathrm { P R M ^ { * } } } = 2 ^ { d } ( e / d )$ This latter coeficient difers from, and is indeed less than, the lower bound in our mathematical guarantee of asymptotic optimality for k-nearest FMT<sup>∗</sup>, equation (6) (note that $k _ { 0 , \mathrm { R R T ^ { * } } }$ is also below the theoretical lower-bound presented in Karaman and Frazzoli (2011)). We note, however, that for a fixed state space dimension $d ,$ the formula for $k _ { n }$ difers only by a constant factor independent from the sample size n. Our choice of $k _ { 0 , \mathrm { F M T ^ { * } } }$ ∗ in the experiments may be understood as a constant factor e greater than the expected number of possible connections that would lie in an obstacle-free ball with radius specified by the lower bound in Theorem 4.1, i.e., $\eta = e ^ { 1 / d } - 1 > 0$ in equation (3). In practice we found that these coeficients for RRT<sup>∗</sup>, PRM<sup>∗</sup>, and FMT<sup>∗</sup> worked well on the problem instances and sample size regimes of our experiments. Indeed, we note that the choice of $k _ { 0 , \mathrm { R R T ^ { * } } }$ , although taken directly from the OMPL reference implementation, stood up well against other values we tried when aiming to ensure a fair comparison. The implementation of FMT<sup>∗</sup> and the code used for algorithm comparison are available at: http://www.stanford.edu/<sub>\~</sub>pavone/code/fmt/.

For each problem setup, we show a panel of six graphs. The first (top left) shows cost versus time, with a point on the graph for each simulation run. These simulations come in groups of 50, and within each group are run on the same number of samples. Note that this sample size is not necessarily the number of nodes in the graph constructed by each algorithm; it indicates iteration count in the case of RRT<sup>∗</sup>, and free space sample count in the cases of FMT<sup>∗</sup> and PRM<sup>∗</sup>. To be precise, RRT<sup>∗</sup> only keeps samples for which initial steering is collision-free. PRM<sup>∗</sup> does use all of the sampled points in constructing its roadmap, and while FMT<sup>∗</sup> nominally constructs a tree as a subgraph of this roadmap, it may terminate early if it finds a solution before all samples are considered. There is also a line on the first plot tracing the mean solution cost of successful algorithm runs on a particular sample count (1-standard-error of the mean error-bars are given in both time and cost). Note that for a given algorithm, a group of simulations for a given sample count is only plotted if it is at least 50% successful at finding a feasible solution. The plot below this one (middle left) shows success rate as a function of time, with each point representing a set of simulations grouped again by algorithm and node count. In this plot, all sample counts are plotted for all algorithms, which is why the curves may start farther to the left than those in the first plot. The top right and middle right plots are the analogous plots to the first two, but with sample count on the x-axis. Finally, the bottom left plot shows execution time as a function of sample count, and the bottom right plot shows the number of collision-checks as a function of sample count. Note that every plot shows vertical error bars, and horizontal error bars where appropriate, of length one standard-error of the mean, although they are often too small to be distinguished from points.

SEH2L Bug Trap HOMPL.appL  
![](Janson2013Fast_figs/240f50bb42db7ce9b30e409f4986ff72ed3b5c8644c4beaae1920a4c3eeb4d4b.jpg)  
(a)

![](Janson2013Fast_figs/791878c122291dd15b27388e3888529df484a2c6bf79b848c14993ba6473d882.jpg)  
(b)

![](Janson2013Fast_figs/c2d52a9152c68767088f84adbf408f9017e56d7e7de8b96f62cf19fb7d62dcbc.jpg)  
(c)

![](Janson2013Fast_figs/f6d412087390f0a753c4956d7879d7c84c77041be876bf9ddc8b10df169bcb1a.jpg)  
(d)

![](Janson2013Fast_figs/4adecc10e9810169a71bf628fa7a2d174e5b107c56a380c5ffdb6e23a291f427.jpg)  
(e)

SEH2L Bug Trap HOMPL.appL  
![](Janson2013Fast_figs/d609d71760a834f1d3940cc460bca952a59649b7b7b4fa6abfd357d50b7b97cb.jpg)  
(f)  
Figure 6: Simulation results for a bug trap environment in 2D space.

## 6.2 Comparison with Other AO Planning Algorithms

## 6.2.1 Numerical Experiments in an SE(2) Bug Trap

The first test case is the classic bug trap problem in SE(2) (Figure 5(a)), a prototypically challenging problem for sampling-based motion planners (Lavalle, 2006). The simulation results for this problem are depicted graphically in Figure 6. FMT<sup>∗</sup> takes about half and one tenth the time to reach similar quality solutions as RRT<sup>∗</sup> and PRM<sup>∗</sup>, respectively, on average. Note that FMT<sup>∗</sup> also is by far the quickest to reach high success rates, achieving nearly 100% in about one second, while RRT<sup>∗</sup> takes about five seconds and PRM<sup>∗</sup> is still at 80% success rate after 14 seconds. The plot of solution cost as a function of sample count shows what we would expect: FMT<sup>∗</sup> and PRM<sup>∗</sup> return nearly identical-quality solutions for the same number of samples, with PRM<sup>∗</sup> very slightly better, while $\mathrm { R R T ^ { * } }$ , due to its greediness, sufers in comparison. Similarly, FMT<sup>∗</sup> and PRM<sup>∗</sup> have similar success rates as a function of sample count, both substantially higher than RRT<sup>∗</sup> . The reason that RRT<sup>∗</sup> still beats PRM<sup>∗</sup> in terms of cost versus time is explained by the plot of execution time versus sample count: RRT<sup>∗</sup> is much faster per sample than PRM<sup>∗</sup> . However, RRT<sup>∗</sup> is still slightly slower per sample than FMT , as explained by the plot of collision-checks versus sample count, which shows FMT<sup>∗</sup> performing fewer collision-checks per sample (O(1)) than $\mathrm { R R T ^ { * } } \left( O ( \log ( n ) ) \right)$ .

SEH2L Maze HOMPL.appL  
![](Janson2013Fast_figs/60ce6c13d4f3482db4c277f3442451b5c498371cf347185c98749419fe422c4b.jpg)  
(a)

![](Janson2013Fast_figs/c80b5e4b2f43e3ef927ad21286a8a44a635e87592587953292160b4caee2d128.jpg)  
(b)

![](Janson2013Fast_figs/6339091d5ec8ad93b4cda4c11b956aa53dad548d312f54f4dcf61ac6ada910a9.jpg)  
(c)

SEH2L Maze HOMPL.appL  
![](Janson2013Fast_figs/2cdcc8928b80a12db72f6d269c65b1585633f6163d5e2e5609f5045bfe7b4ee9.jpg)  
(d)

SEH2L Maze HOMPL.appL  
![](Janson2013Fast_figs/276d4fb3c73d2a5fbed1250b516443f84f2fcd3873bfebc27bb5e54dae987f44.jpg)  
(e)

![](Janson2013Fast_figs/023b40e332eb4632cdbc66deba2ac1eb482012e8c8aa5af12a3ef84a6fa98b24.jpg)  
(f)  
Figure 7: Simulation results for a maze environment in 2D space.

The lower success rate for RRT<sup>∗</sup> may be explained as a consequence of its graph expansion process. When iterating to escape the bug trap, the closest tree node to a new sample outside the mouth of the trap will nearly always lie in one of the “dead end” lips, and thus present an invalid steering connection. Only when the new sample lies adjacent to the progress of the tree down the corridor will RRT<sup>∗</sup> be able to advance. For $\mathrm { R R T ^ { * } }$ to escape the bug trap, an ordered sequence of samples must be obtained that lead the tree through the corridor. FMT<sup>∗</sup> and PRM<sup>∗</sup> are not afected by this problem; their success rate is determined only by whether or not such a set of samples exists, not the order in which they are sampled by the algorithm.

SE(3) Cubicle Maze (OMPL.app)  
![](Janson2013Fast_figs/d002c797b1cb0901ee27f244dcd7b1c95e6c05633664811510c91e626fd69503.jpg)  
(a)

SEH3L Cubicle Maze HOMPL.appL  
![](Janson2013Fast_figs/9b7723e2a87345ab19f67b4ef86f7c293d0af1bc311ccde147977a00f3d85fd8.jpg)  
(b)

SEH3L Cubicle Maze HOMPL.appL  
![](Janson2013Fast_figs/1155ac482b301cc541e8bd991ae8066aaf8034581abf7cc2bee5774c7ba06ef6.jpg)  
(c)

SEH3L Cubicle Maze HOMPL.appL  
![](Janson2013Fast_figs/ebe2819c5260ca8dae8deb1e53e69c9a5845c9612472f1eccdaa0c585f2a2f17.jpg)  
(d)

SEH3L Cubicle Maze HOMPL.app  
![](Janson2013Fast_figs/cea864c9b61e13d2b61c8f1903e4377d8fb330bed8ec8b8094ac5dbe0315e967.jpg)  
(e)

SEH3L Cubicle Maze HOMPL.appL  
![](Janson2013Fast_figs/64f3fd59750c07a2371bdac018f61408277a58597b71c7bc90baec9dae437bc3.jpg)  
(f)  
Figure 8: Simulation results for a maze environment in 3D space.

## 6.2.2 Numerical Experiments in an SE(2) Maze

Navigating a “maze” environment is another prototypical benchmark for path planners (S¸ucan et al., 2012). This section, in particular, considers an SE(2) maze (portrayed in Figure 5(b)). The plots for this environment, given in Figure 7, tell a very similar story to those of the SE(2) bug trap. Again, FMT<sup>∗</sup> reaches given solution qualities faster than RRT<sup>∗</sup> and PRM<sup>∗</sup> by factors of about 2 and 10, respectively. Although the success rates of all the algorithms go to 100% quite quickly, FMT<sup>∗</sup> is still the fastest. All other heuristic relationships between algorithms in the other graphs remain the same as in the case of the SE(2) bug trap.

## 6.2.3 Numerical Experiments in an SE(3) Maze

Figure 8 presents simulation results for a three-dimensional maze, specifically for the maze in SE(3) depicted in Figure 5(c). These results show a few diferences from those in the previous two subsections. First of all, FMT<sup>∗</sup> is an even clearer winner in the cost versus time graph, with relative speeds compared to RRT<sup>∗</sup> and PRM<sup>∗</sup> hard to compare due to the fact that FMT<sup>∗</sup> reaches an average solution quality in less than five seconds that is below that achieved by RRT<sup>∗</sup> and PRM<sup>∗</sup> in about 20 seconds and 70 seconds, respectively. Furthermore, at 20 seconds, the FMT solution appears to still be improving faster than RRT<sup>∗</sup> after the same amount of time. The success rate as a function of time for RRT<sup>∗</sup> is much closer to, though still slightly below, FMT than it was in the previous two problem setups, with both algorithms reaching 100% completion rate in about three seconds.

A new feature of the SE(3) maze is that RRT<sup>∗</sup> now runs faster per sample than FMT<sup>∗</sup>, due to the fact that it performs fewer collision-checks per sample than FMT<sup>∗</sup>. The reason for this has to do with the relative search radii of the two algorithms. Since they work very diferently, it is not unreasonable to use diferent search radii, and although FMT<sup>∗</sup> will perform fewer collision-checks asymptotically, for finite sample sizes, the number of collisionchecks is mainly influenced by connection radius and obstacle clutter. While RRT<sup>∗</sup>’s radius has been smaller than FMT<sup>∗</sup>’s in all simulations up to this point, the previous two setups had more clutter, forcing RRT to frequently draw a sample, collision-check its nearest-neighbor connection, and then remove it when this check fails. As can be seen in Figure 5(c), the SE(3) maze is relatively open and contains fewer traps as compared to the previous two problems, thereby utilizing more of the samples that it runs collision-checks for.

## 6.2.4 Numerical Experiments for 3D, 5D, and 7D Recursive Maze

In order to illustrate a “worst-case” planning scenario in high dimensional space, we constructed a recursive maze obstacle environment within the Euclidean unit hypercube. Essentially, each instance of the maze consists of two copies of the maze in the previous dimension separated by a divider and connected through the last dimension. See Figure 9 for the first two instances of the maze in two dimensions and three dimensions, respectively. This recursive nature has the efect of producing a problem environment with only one homotopy class of solutions, any element of which is necessarily long and features sections that are spatially close, but far away from each other in terms of their distance along the solution path. Our experiments investigated translating a rigid body from one end of the maze to the other. The results of simulations in 3, 5, and 7 dimensional recursive mazes are given in Figures 10, 11, and 12. $\mathrm { F M T ^ { * } }$ once again reaches lower-cost solutions in less time than RRT<sup>∗</sup>, with the improvement increasing with dimension. The most notable trend between FMT<sup>∗</sup> and $\mathrm { R R T ^ { * } }$ , however, is in success rate. While both algorithms reach 100% success rate almost instantly in 3D, FMT<sup>∗</sup> reaches 100% in under a second, while $\mathrm { R R T ^ { * } }$ takes closer to five seconds in 5D, and most significantly RRT<sup>∗</sup> was never able to find any solution in the time alotted in 7D. This can be understood through the geometry of the maze—the maze’s complexity is exponentially increasing in dimension, and in 7D, so much of free space is blocked of from every other part of free space that RRT<sup>∗</sup> is stuck between two bad options: it can use a large steering radius, in which case nearly every sample fails to connect to its nearest-neighbor and is thrown out, or it can use a small steering radius, in which case connections are so short that the algorithm has to figuratively crawl through the maze. Even if the steering parameter were not an issue, the mere fact that $\mathrm { R R T ^ { * } }$ operates on a steering graph-expansion principle means that in order to traverse the maze, an ordered subsequence of $2 ^ { 7 }$ nodes (corresponding to each turn of the maze) must be in the sample sequence before a solution may be found. While this is an extreme example, as the recursive maze is very complex in 7D (feasible solutions are at least 43 units long, and entirely contained in the unit cube), it accentuates FMT ’s advantages in highly cluttered environments.

![](Janson2013Fast_figs/06aab57c4f445fe74c34d23d020a9eb78ddcca077e76257c50b473fe09c334a1.jpg)  
(a) 2D recursive maze.

![](Janson2013Fast_figs/dc426940bfe42a8bd2bb341fbbcf91a9646e2f1c9fd23f77d89386903e01b24e.jpg)  
(b) 3D recursive maze.  
Figure 9: Recursive maze environment.

As compared to PRM<sup>∗</sup>, FMT<sup>∗</sup> still presents a substantial improvement, but that improvement decreases with dimension. This can be understood by noting that the two algorithms achieve nearly identical costs for a given sample count, but $\mathrm { F M T ^ { * } }$ is much faster due to savings on collision-checks. However, as the plots show, the relative decrease in collision-checks from PRM<sup>∗</sup> to FMT<sup>∗</sup> decreases to only a factor of two once we reach 7D, and indeed we see that, when both algorithms achieve low cost, FMT<sup>∗</sup> does so in approximately half the time. This relative decrease in collision-checks comes from the aforementioned extreme obstacle clutter in the configuration space. FMT<sup>∗</sup> makes big savings over PRM<sup>∗</sup> when it connects many samples on their first consideration, but when most samples are close to obstacles, most samples will take multiple considerations to finally be connected. Both algorithms achieve 100% success rates in approximately the same amount of time.

3D Recursive Maze  
![](Janson2013Fast_figs/8bb0197c8920eda2ead9d506094d2f610bb7676b27cc9fc4e5cd360883eb4a88.jpg)  
(a)

![](Janson2013Fast_figs/dc6d10905421cd23226a449e694281522d244ab9a7a46219ec8c807345782f85.jpg)  
(b)

![](Janson2013Fast_figs/068d1bde45a86ff35cc72067d7c8325a6decebde9cf65cc68e003f026f1e958d.jpg)  
(c)

![](Janson2013Fast_figs/444bcb05f65a2c847bac7a0f8dcee416d9f32979970588830cb06bc902a3446a.jpg)  
(d)

3D Recursive Maze  
![](Janson2013Fast_figs/19f790bb84d224c7b2d4874b5887fffb1c260843b7930adbbee75d97e1a9cdb2.jpg)  
(e)

![](Janson2013Fast_figs/be5b540bac4b16e9690939dfdbcd94b1e764c8aeee6eb0111e9e55cbc5c182b4.jpg)  
(f)  
Figure 10: Simulation results for a recursive maze environment in 3D.

## 6.2.5 Numerical Experiments for the SE(3) Alpha Puzzle

Throughout our numerical evaluation of FMT<sup>∗</sup>, we found only one planning problem where FMT<sup>∗</sup> does not consistently outperform RRT<sup>∗</sup> (FMT<sup>∗</sup> outperformed PRM<sup>∗</sup> in all of our numerical tests). The problem is the famous 1.5 Alpha puzzle (Amato et al., 1998), which consists of two tubes, each twisted in an α shape. The objective is to separate the intertwined tubes by a sequence of translations and rotations, which leads to extremely narrow corridors in $\mathcal { X } _ { \mathrm { f r e e } }$ through which the solution path must pass (see Figure 5(d)). Simulation results show that the problem presents two homotopy classes of paths (Figure 13(a)). FMT<sup>∗</sup> converges to a 100% success rate more slowly than RRT<sup>∗</sup> (Figure 13(c)), but when FMT<sup>∗</sup> finds a solution, that solution tends to be in the “right” homotopy class and of higher quality, see Figures 13(a) and 13(b). We note that in order to achieve this high success rate for RRT<sup>∗</sup>, we adjusted the steering parameter to 1.5% of the maximum extent of the configuration space, down from 20%. Without this adjustment, RRT<sup>∗</sup> was unable to find feasible solutions at the upper range of the sample counts considered.

![](Janson2013Fast_figs/9d86c57071229d6119c3d1af859abb01f573609904f405bd19c462660c1b9911.jpg)

![](Janson2013Fast_figs/88f5976c1fbe51994c3f45493d533b410a6240eb6d53d6df681c2d9143e3085b.jpg)  
(b)

5D Recursive Maze  
![](Janson2013Fast_figs/92830139c18481f6915adf7ed469e45178c593886e6f5142486b50565fc249dc.jpg)  
(c)

5D Recursive Maze  
![](Janson2013Fast_figs/ca6f82787071925f448adf063cea0e14215ce1ca0f48d3d2a17c96e19fbd21c7.jpg)  
(d)

5D Recursive Maze  
![](Janson2013Fast_figs/f217856cd2dd7436f8c3ab2375d562b8ccb3f1694441cbb1462f03c22d0beafa.jpg)  
(e)

5D Recursive Maze  
![](Janson2013Fast_figs/304a6a12d79ad120c4d7487ea90ee77e2fcb3e309472ed79cbe52f0a1c6cd48b.jpg)  
(f)  
Figure 11: Simulation results for a recursive maze environment in 5D.

This behavior can be intuitively explained as follows. The Alpha puzzle presents “narrow corridors” in $\mathcal { X } _ { \mathrm { f r e e } }$ (Amato et al., 1998; Hsu et al., 2006). When FMT<sup>∗</sup> reaches their entrance, if no sample is present in the corridors, $\mathrm { F M T ^ { * } }$ stops its expansion, while RRT<sup>∗</sup> keeps trying to extend its branches through the corridors, which explains its higher success rates at low sample counts. On the other hand, at high sample counts, samples are placed in the corridors with high probability, and when this happens the optimal (as opposed to greedy) way by which FMT<sup>∗</sup> grows the tree usually leads to the discovery of a better homotopy class and of a higher quality solution within it (Figure 13(a), execution times larger than  25 seconds). As a result, RRT<sup>∗</sup> outperforms FMT<sup>∗</sup> for short execution times, while FMT<sup>∗</sup> outperforms RRT<sup>∗</sup> in the complementary case. Finally, we note that the extremely narrow but short corridors in the Alpha puzzle present a diferent challenge to these algorithms than the directional corridor of the SE(2) bug trap. As discussed in Section 6.2.1, the ordering of sampled points along the exit matters for RRT<sup>∗</sup> in the bug trap configuration, while for the Alpha puzzle the fact that there are no bug-trap-like “dead ends” to present false steering connections means that a less intricate sequence of nodes is required for success.

![](Janson2013Fast_figs/4ca34a69c98c90dcbff03b737036d308a7e5cc93d4eeaa7bb91f152646ee4be1.jpg)

![](Janson2013Fast_figs/be682738db40185ec43b831d84d50378b911dc3905012de871d4a5e6d74d443b.jpg)

![](Janson2013Fast_figs/2686e1d858ad80e01e7d282b0b08e29fdf3ab53aa4b0587a8a0090488d6745b3.jpg)

![](Janson2013Fast_figs/f953e1115ed8aef115fd289566cd1791654d3c9355e633a9d4feea1c1062e5bf.jpg)

![](Janson2013Fast_figs/7fa34d5688ecbef653a22bf91debdec339e8b596da84fa5e5a97b2f15e5b3c9f.jpg)

![](Janson2013Fast_figs/21ec58a239d63eabd66a2f6a4c9c5ec2d559e032abdedade4064e573fe32e2de.jpg)  
Figure 12: Simulation results for a recursive maze environment in 7D.

On the one hand, allowing FMT<sup>∗</sup> to sample new points around the leaves of its tree whenever it fails to find a solution (i.e., when $V _ { \mathrm { o p e n } }$ becomes empty) might substantially improve its performance in the presence of extremely narrow corridors. In a sense, such a modification would introduce a notion of “anytimeness” and adaptive sampling into FMT , which would efectively leverage the steadily outward direction by which the tree is constructed (see (Gammell et al., 2014) for a conceptually related idea). This is a promising area of future research (note that the theoretical foundations for non-uniform sampling strategies are provided in Section 5.1). On the other hand, planning problems with extremely narrow passages, such as the Alpha puzzle, do not usually arise in robotics applications as, fortunately, they tend to be expansive, i.e., they enjoy “good” visibility properties (Hsu et al., 2006). Collectively, these considerations suggest the superior performance of $\mathrm { F M T ^ { * } }$ in most practical settings.

SE(3) Alpha Puzzle (OMPL.app)  
![](Janson2013Fast_figs/44fb84877e7b94253ad3c69fe109cfdef15a3b8ba47469ca8c6ba14f08cce1f7.jpg)  
(a)

![](Janson2013Fast_figs/de3b3070d46dd2fa5ca01d353b3c03d0046539bd860d90589c34dbea8fe7a0e1.jpg)  
(b)

SEH3L Alpha Puzzle HOMPL.appL  
![](Janson2013Fast_figs/2e554704f4c566b1159157b2a3407949ed4ebadb5536c8c28e48baf806fe5b47.jpg)  
(c)

SEH3L Alpha Puzzle HOMPL.appL  
![](Janson2013Fast_figs/134b7fbd74951e2ec105448d0abe64f2e368eff3da70fd45ff00548b2576c8e5.jpg)  
(d)

SEH3L Alpha Puzzle HOMPL.appL  
![](Janson2013Fast_figs/cc1da2f2eb80a6c0279f2b8c65493904c892e19408fbeb6744e75ae6f53bbe65.jpg)  
(e)

SEH3L Alpha Puzzle HOMPL.appL  
![](Janson2013Fast_figs/b43b160b36590722b77c1ce657d55e69e319bbd2ae2c57af55aa95cd180bb168.jpg)  
(f)  
Figure 13: Simulation results for a Alpha puzzle.

## 6.3 In-Depth Study of FMT∗

## 6.3.1 Comparison Between FMT<sup>∗</sup> and k-Nearest FMT<sup>∗</sup>

Since we are now comparing both versions of FMT<sup>∗</sup>, we will explicitly use radial-FMT<sup>∗</sup> to denote the version of FMT that uses a fixed Euclidean distance to determine neighbors, and return to referring to k-nearest FMT by its full name throughout this section. For this set of simulations, given in Figure 14, the formula for $k _ { n }$ is still the same as in the rest of the simulations, and for comparison, the radius $r _ { n }$ of the radial-FMT<sup>∗</sup> implementation is chosen so that the expected number of samples in a collision-free $r _ { n } \mathrm { - b a l l }$ is exactly equal to $k _ { n }$ Finally, as a caveat, we point out that since k-nearest-neighborhoods are fundamentally different from r-radius-neighborhoods, the two algorithms depicted now use diferent primitive procedures. Since computing neighbors in both algorithms takes a substantial fraction of the runtime, the cost versus time plots should be interpreted with caution, since the algorithms’ relative runtimes could potentially change significantly with a better implementation of one or both neighbor-finding primitive procedures. With that said, we focus our attention more on the number of collision-checks as a proxy for algorithm speed. Since this problem has a relatively simple collision-checking module, we may expect that for more complex problems in which collision-checking dominates runtime, the number of collision-checks should approximate runtime well.

While the number of collision-checks in free space is the same between the two algorithms, since all samples connect when they are first considered, some interesting behavior is exhibited in the same plot for the 5D maze. In particular, the number of collision checks for k-nearest FMT<sup>∗</sup> increases quickly with sample count, then decreases again and starts to grow more like the linear curve for radial-FMT<sup>∗</sup>. This hump in the curve corresponds to when the usual connection distance for k-nearest FMT<sup>∗</sup> is greater than the width of the maze wall, meaning that for many of the points, some of their k<sub>n</sub>-nearest-neighbors will be much farther along in the maze. Thus k-nearest FMT tries to connect them to the tree, and fails because there is a wall in between. The same problem doesn’t occur for radial-FMT<sup>∗</sup> because its radius stays smaller than the width of the maze wall. This is symptomatic of an advantage and disadvantage of k-nearest FMT , namely that for samples near obstacles, connections may be attempted to farther-away samples. This is an advantage because for a point near an obstacle, there is locally less density around the point and thus fewer nearby options for connection, making it harder for radial-FMT<sup>∗</sup> to find a connection, let alone a good one. For small sample sizes relative to dimension however, this can cause a lot of extra collision-checks by, as just described, having k-nearest FMT<sup>∗</sup> attempt connections across walls. As this disadvantage goes away with enough points, we still find that, although the diference in free space is very small, k-nearest FMT<sup>∗</sup> outperforms radial-FMT<sup>∗</sup> in both of the settings shown, as the relative advantage of k-nearest FMT in solution cost per sample is greater than the relative disadvantage in number of collision-checks per sample.

## 6.3.2 Tuning the Radius Scale Factor

The choice of tuning parameters is a challenging and pervasive problem in the samplingbased motion planning literature. Throughout these numerical experiments, we have used the same neighbor scaling factor, which we found empirically to work well across a range of scenarios. In this section, we try to understand the relationship of k-nearest FMT with this neighbor scaling parameter, in the example of the SE(3) maze. The results of running k-nearest FMT<sup>∗</sup> with a range of tuning parameters on this problem are shown in Figure 15. The values in the legend correspond to a connection radius multiplier (RM) of $k _ { 0 , \mathrm { F M T ^ { * } } }$ as defined at the beginning of Section 6, i.e., a value of RM = 1 corresponds to using exactly $k _ { 0 , \mathrm { F M T ^ { * } } }$ , and a value of RM = 2 corresponds to using $k _ { 0 } = 2 ^ { d } \cdot k _ { 0 , \mathrm { F M T } ^ { * } }$ . We point out that to reduce clutter, we have omitted error bars from the plot, but note that they are small compared to the diferences between the curves.

5D Recursive Maze  
![](Janson2013Fast_figs/3eadf352286dd6d2324545d75b8abc36f7a2688a7478a91e4faad568206c1b9b.jpg)

![](Janson2013Fast_figs/08c9879c39120edfa4d998bc02f4e9ca6586d736ef0bcf8678bd5649caf8f3db.jpg)

![](Janson2013Fast_figs/3d61b54e33e6ca47ff0c3db09d9ca7f04fa504cefbc7462da713e111c944b8b3.jpg)

![](Janson2013Fast_figs/f440528e701dfa4321a2fba32632d8cee9b31f1d702722f0f139c81eb7b6419e.jpg)

![](Janson2013Fast_figs/34ce128202ee858a90a97c0d4f83dc04eced2a112930d778c9dec7a904d65443.jpg)

![](Janson2013Fast_figs/d368e9cbfe03a0c132f7c17c9a6b8aa1a94e7448e486a40316370bc848bf219b.jpg)  
Figure 14: Comparison between raidal-FMT<sup>∗</sup> and k-nearest FMT<sup>∗</sup> .

This graph clearly shows the tradeof in the scaling factor, namely that for small values, k-nearest FMT<sup>∗</sup> rapidly reaches a fixed solution quality and then plateaus, while for larger values, the solution takes a while to reach lower costs, but continues to show improvement for longer, eventually beating the solutions for small values. The fact that most of these curves cross one another tells us that the choice of this tuning parameter depends on available time and corresponding sample count. For this experimental setup, and for the other problems we tried, there appears to be a sweet spot around the value $\mathrm { R M } = 1$ . Indeed, this motivated our choice of $k _ { 0 , \mathrm { F M T ^ { * } } }$ in our simulations. We note that the curves for 0.7 through 0.9 start out at lower costs for very small execution times, and it appears that the curve for 1.1 is going to start to return better solutions than 1.0 before 35 seconds. That is, depending on the time/sample allowance, there are at least four regimes in which diferent scaling factors outperform the others. For a diferent problem instance, the optimal scaling profile may change, and for best performance some amount of manual tuning will be required. We note, however, that RM = 1 is never too far from the best in Figure 15, and should represent a safe default choice.

![](Janson2013Fast_figs/b227871a96037ca3ce6714f8dd60703385a447dc30045a4d3666e8bce44927d2.jpg)  
Figure 15: Performance of k-nearest $\mathrm { F M T ^ { * } }$ for diferent values of the neighbor scaling parameter.

## 6.3.3 Improvement on Convergence Rate with Simple Heuristics

In any path planning problem, the optimal path tends to be quite smooth, with only a few non-diferentiable points. However, sampling-based algorithms all locally-connect points with straight lines, resulting in some level of “jaggedness” in the returned paths. A popular post-processing heuristic for mitigating this problem is the ADAPTIVE-SHORTCUT smoothing heuristic described in (Hsu, 2000). In Figure 16, we show the efect of applying the ADAPTIVE-SHORTCUT heuristic to k-nearest FMT solutions for the 5D recursive maze. We use a point robot for this simulation as it allowed us to easily compute the true optimal cost, and thus better place the improvement from the heuristic in context. The improvement is substantial, and we see that we can obtain a solution within 10% of the optimal with fewer than 1000 samples in this complicated 5D environment. Figure 16 also displays the fact that adding the ADAPTIVE-SHORTCUT heuristic only barely increases the number of collisionchecks. We place sample count on the x-axis because it is more absolute than time, which is more system-dependent, and because the ADAPTIVE-SHORTCUT heuristic runs so quickly compared to the overall algorithm that sample count is able to act as an accurate proxy for time across the two implementations of k-nearest FMT<sup>∗</sup> .

![](Janson2013Fast_figs/2fefe881e1f7061ec11fd23abdcaa1bdb45aa21e768c94e13d6957559f06f35a.jpg)

![](Janson2013Fast_figs/4af68f325c57fa75d437b5e827b4063d1bd7da9a03937b07bbe93428db866e15.jpg)  
Figure 16: Simulation results for a maze configuration in 2D space.

## 6.3.4 Experiment With General Cost

As a demonstration of the computationally-eficient k-nearest FMT implementation described in Section 5.2.3, we set up three environments with non-constant cost-density over the configuration space. We have kept them in two dimensions so that they can be considered visually, see Figure 17. In Figure 17(a), there is a high-cost region near the root node and a low-cost region between it and the goal region. k-nearest FMT<sup>∗</sup> correctly chooses the shorter path through the high-cost region instead of going around it, as the extra distance incurred by the latter option is greater than the extra cost incurred in the former. In Figure 17(b), we have increased the cost density of the high-cost region, and k-nearest FMT<sup>∗</sup> now correctly chooses to go around it as much as possible. In Figure 17(c), the cost density function is inversely proportional to distance from the center, and k-nearest FMT<sup>∗</sup> smoothly makes its way around the higher-cost center to reach the goal region. Note that in all three plots, since cost-balls are used for considering connections, the edges are shorter in higher-cost areas and longer in lower-cost areas.

## 6.3.5 How to Best Use FMT<sup>∗</sup>?

FMT<sup>∗</sup> relies on two parameters, namely the connection radius or number of neighbors, and the number of samples. As for the first parameter, numerical experiments showed that $k _ { 0 , \mathrm { F M T ^ { * } } } ~ = ~ 2 ^ { d } \left( e / d \right)$ represents an efective and fairly robust choice for the k-nearest version of FMT —this is arguably the value that should be used in most planning problems. Correspondingly, for the radial version of FMT<sup>∗</sup>, one should choose a connection radius as specified in the lower bound in Theorem 4.1 with $\eta = e ^ { 1 / d } - 1$ (see Section 6.1). Selecting the number of samples is a more contentious issue, as it is very problem-dependent. A system designer should experiment with a variety of sample sizes for a variety of “expected” obstacle configurations, and then choose the value that statistically performs the best within the available computational resources. Such a baseline choice could be adaptively adjusted via the resampling techniques discussed in (Salzman and Halperin, 2014) or via the adaptive strategies discussed in (Gammell et al., 2014) and mentioned in Section 6.2.5.

![](Janson2013Fast_figs/708d3e7b76e7691a82c57b536a971c4c2020647e75f40848e0c39373ba3cab76.jpg)  
(a)

![](Janson2013Fast_figs/c4b49f69810e3f84871c1bfc910719184f6b1dfc5264baed652ecf7ace3ec24c.jpg)  
(b)

![](Janson2013Fast_figs/91336f2af50078c4fe9a4e8a06a9e1841ff31eb84e931283bebf86a274729bdc.jpg)  
(c)  
Figure 17: Planning with general costs.

For the problem environments and sample sizes considered in our experiments, the extents of the neighbor sets (k-nearest or radial) are macroscopic with respect to the obstacles. The decrease in available connections for many samples when their radial neighborhoods significantly intersect the obstacle set seems to adversely afect algorithm performance (see Section 6.3.1). The k-nearest version of $\mathrm { F M T ^ { * } }$ avoids this issue by attempting connection to a fixed number of samples regardless of obstacle proximity. Thus k-nearest FMT<sup>∗</sup> should be considered the default, especially for obstacle cluttered environments. If the application has mostly open space to plan through, however, radial FMT may be worth testing and tuning.

In problems with a general cost function, FMT provides a good standalone solution that provably converges to the optimum. In problems with a metric cost function, FMT (as also RRT<sup>∗</sup> and PRM<sup>∗</sup>) should be considered as a backbone algorithm on top of which one should add a smoothing procedure such as ADAPTIVE-SHORTCUT (Hsu, 2000). In this regard, FMT<sup>∗</sup> should be regarded as a fast “homotopy finder,” reflecting its quick initial convergence rate to a good homotopy class, which then needs to be assisted by a smoothing procedure to ofset its typical plateauing behavior, i.e., slow convergence to an optimum solution within a homotopy class. When combining FMT<sup>∗</sup> with a smoothing procedure one should consider values for the connection radius or number of neighbors most likely equal to about 80% or 90% of the previously suggested values, so as to ensure very fast initial rates of convergence (see Section 6.3.2). Additionally, non-uniform sampling strategies reflecting prior knowledge about the problem may also improve the speed of finding the optimal homotopy class. Finally, a bidirectional implementation is usually preferable (Starek et al., 2014).

## 7 Conclusions

In this paper we have introduced and analyzed a novel probabilistic sampling-based motion planning algorithm called the Fast Marching Tree algorithm (FMT<sup>∗</sup>). This algorithm is asymptotically optimal and appears to converge significantly faster then its state-of-theart counterparts for a wide range of challenging problem instances. We used the weaker notion of convergence in probability, as opposed to convergence almost surely, and showed that the extra mathematical flexibility allowed us to compute convergence rate bounds. Extensions (all retaining AO) to non-uniform sampling strategies, general costs, and a knearest-neighbor implementation were also presented.

This paper leaves numerous important extensions open for further research. First, it is of interest to extend the FMT algorithm to address problems with diferential motion constraints; the work in (Schmerling et al., 2014a) and (Schmerling et al., 2014b) presents preliminary results in this direction (specifically, for systems with driftless diferential con straints, and with drift constraints and linear afine dynamics, respectively). Second, we plan to explore further the convergence rate bounds provided by the proof of AO given here. Third, we plan to use this algorithm as the backbone for scalable stochastic planning algorithms. Fourth, we plan to extend the FMT algorithm for solving the Eikonal equation, and more generally for addressing problems characterized by partial diferential equations. Fifth, as discussed, FMT<sup>∗</sup> requires the tuning of a scaling factor for either the search radius or the number of nearest-neighbors, and the selection of the number of samples. It is of interest to devise strategies whereby these parameters are “self regulating” (see Section 6.3.5 for some possible strategies), thus efectively making the algorithm parameter-free and anytime. Finally, we plan to test the performance of FMT<sup>∗</sup> on mobile ground robots operating in dynamic environments.

## Acknowledgement

The authors gratefully acknowledge the contributions of Wolfgang Pointner and Brian Ichter to the implementation of FMT<sup>∗</sup> and for help on the numerical experiments. This research was supported by NASA under the Space Technology Research Grants Program, Grant NNX12AQ43G.

## Appendix A: Proofs for Lemmas 4.2–4.4

Proof of Lemma $4 . 2 .$ To start, note that $\mathbb { P } ( K _ { n } ^ { \beta } \ge \alpha ( M _ { n } - 1 ) ) + \mathbb { P } ( A _ { n } ^ { c } ) \ge \mathbb { P } ( \{ K _ { n } ^ { \beta } \ge \alpha ( M _ { n } - 1 ) \} + \mathbb { P } ( \{ M _ { n } \} ) .$ $\begin{array} { r } { 1 ) \} \cup A _ { n } ^ { c } ) = 1 - { \mathbb P } ( \{ K _ { n } ^ { \beta } < \alpha ( M _ { n } - 1 ) \} \cap A _ { n } ) } \end{array}$ , where the first inequality follows from the union bound and the second equality follows from De Morgan’s laws. Note that the event $\{ K _ { n } ^ { \beta } < \alpha ( M _ { n } - 1 ) \} \cap A _ { n }$ is the event that each $B _ { n , m }$ contains at least one node, and more than a 1 α fraction of the $B _ { n , m } ^ { \beta }$ balls also contains at least one node.

When two nodes $x _ { i }$ and $x _ { i + 1 } , i \in \{ 1 , . . . , M _ { n } - 2 \}$ , are contained in adjacent balls $B _ { n , i }$

and $B _ { n , i + 1 }$ , respectively, their distance apart $\| x _ { i + 1 } - x _ { i } \|$ can be upper bounded by,

$$
\left\{ \begin{array}{l l} \frac {\theta r _ {n}}{2 + \theta} + \frac {\beta r _ {n}}{2 + \theta} + \frac {\beta r _ {n}}{2 + \theta} & : \text {if} x _ {i} \in B _ {n, i} ^ {\beta} \text {and} x _ {i + 1} \in B _ {n, i + 1} ^ {\beta} \\ \frac {\theta r _ {n}}{2 + \theta} + \frac {\beta r _ {n}}{2 + \theta} + \frac {r _ {n}}{2 + \theta} & : \text {if} x _ {i} \in B _ {n, i} ^ {\beta} \text {or} x _ {i + 1} \in B _ {n, i + 1} ^ {\beta} \\ \frac {\theta r _ {n}}{2 + \theta} + \frac {r _ {n}}{2 + \theta} + \frac {r _ {n}}{2 + \theta} & : \text {otherwise}, \end{array} \right.
$$

where the three bounds have been suggestively divided into a term for the distance between ball centers and a term each for the radii of the two balls containing the nodes. This bound also holds for $\| x _ { M _ { n } } - x _ { M _ { n } - 1 } \|$ , although necessarily in one of the latter two bounds, since $B _ { n , M _ { n } } ^ { \beta }$ being undefined precludes the possibility of the first bound. Thus we can rewrite the above bound, for $i \in \{ 1 , . . . , M _ { n } - 1 \}$ , as $\| x _ { i + 1 } - x _ { i } \| \leq \bar { c } ( x _ { i } ) + \bar { c } ( x _ { i + 1 } )$ , where

$$
\bar {c} (x _ {k}) := \left\{ \begin{array}{l l} \frac {\theta r _ {n}}{2 (2 + \theta)} + \frac {\beta r _ {n}}{2 + \theta} & : x _ {k} \in B _ {n, k} ^ {\beta}, \\ \frac {\theta r _ {n}}{2 (2 + \theta)} + \frac {r _ {n}}{2 + \theta} & : x _ {k} \notin B _ {n, k} ^ {\beta}. \end{array} \right.\tag{7}
$$

Again, $\hat { c } ( x _ { M _ { n } } )$ is still well-defined, but always takes the second value in equation (7) above. Let $L _ { n , \alpha , \beta }$ be the length of a path that sequentially connects a set of nodes $\{ x _ { 1 } = x _ { \mathrm { i n i t } } , x _ { 2 } , \ldots , x _ { M _ { n } } \}$ such that $x _ { m } \in B _ { n , m } \forall m \in \{ 1 , \ldots , M _ { n } \}$ , and more than a $( 1 - \alpha )$ fraction of the nodes $x _ { 1 } , \ldots , x _ { M _ { n } - 1 }$ are also contained in their respective $B _ { n , m } ^ { \beta }$ balls. The length $L _ { n , \alpha , \beta }$ can then be upper bounded as follows

$$
\begin{array}{l} L _ {n, \alpha , \beta} = \sum_ {k = 1} ^ {M _ {n} - 1} \| x _ {k + 1} - x _ {k} \| \leq \sum_ {k = 1} ^ {M _ {n} - 1} 2 \bar {c} (x _ {k}) - \bar {c} (x _ {1}) + \bar {c} (x _ {M _ {n}}) \\ \quad \leq (M _ {n} - 1) \frac {\theta r _ {n}}{2 + \theta} + \lceil (1 - \alpha) (M _ {n} - 1) \rceil \frac {2 \beta r _ {n}}{2 + \theta} + \lfloor \alpha (M _ {n} - 1) \rfloor \frac {2 r _ {n}}{2 + \theta} + \frac {(1 - \beta) r _ {n}}{2 + \theta} \\ \quad \leq (M _ {n} - 1) r _ {n} \frac {\theta + 2 \alpha + 2 (1 - \alpha) \beta}{2 + \theta} + \frac {(1 - \beta) r _ {n}}{2 + \theta} \\ \quad \leq M _ {n} r _ {n} \frac {\theta + 2 \alpha + 2 \beta}{2 + \theta} + \frac {r _ {n}}{2 + \theta}. \end{array}\tag{8}
$$

In equation 8, <sub>d</sub>x<sub>e</sub> denotes the smallest integer not less than $x ,$ while $\lfloor x \rfloor$ denotes the largest integer not greater than x. Furthermore, we can upper bound $M _ { n }$ as follows,

$$
\begin{array}{l} c (\sigma_ {n} ^ {\prime}) \geq \sum_ {k = 1} ^ {M _ {n} - 2} \| \sigma_ {n} (\tau_ {k + 1}) - \sigma_ {n} (\tau_ {k}) \| + \| \sigma_ {n} ^ {\prime} (1) - \sigma_ {n} (\tau_ {M _ {n} - 1}) \| \geq (M _ {n} - 2) \frac {\theta r _ {n}}{2 + \theta} + \frac {r _ {n}}{2 (2 + \theta)} \\ = M _ {n} \frac {\theta r _ {n}}{2 + \theta} + \Big (\frac {1}{2} - 2 \theta \Big) \frac {r _ {n}}{2 + \theta} \geq M _ {n} \frac {\theta r _ {n}}{2 + \theta}, \end{array}\tag{9}
$$

where the last inequality follows from the assumption that $\theta < 1 / 4$ . Combining equations (8) and (9) gives

$$
L _ {n, \alpha , \beta} \leq c (\sigma_ {n} ^ {\prime}) \left(1 + \frac {2 \alpha + 2 \beta}{\theta}\right) + \frac {r _ {n}}{2 + \theta} = \kappa (\alpha , \beta , \theta)   c (\sigma_ {n} ^ {\prime}) + \frac {r _ {n}}{2 + \theta}.\tag{10}
$$

We will now show that when $A _ { n }$ occurs, $c _ { n }$ is no greater than the length of the path connecting any sequence of $M _ { n }$ nodes tracing through the balls $B _ { n , 1 } , \ldots , B _ { n , M _ { n } }$ (this inequality of course also implies $c _ { n } < \infty )$ . Coupling this fact with equation (10), we can then conclude that the event $\{ K _ { n } ^ { \beta } < \alpha ( M _ { n } - 1 ) \} \cap A _ { n }$ implies that $\begin{array} { r } { c _ { n } \le \kappa ( \alpha , \beta , \theta ) c ( \sigma _ { n } ^ { \prime } ) + \frac { r _ { n } } { 2 + \theta } } \end{array}$ , which, in turn, would prove the lemma.

Let $x _ { 1 } = x _ { \mathrm { i n i t } } , x _ { 2 } \in B _ { n , 2 } , . . . , x _ { M _ { n } } \in B _ { n , M _ { n } } \subseteq \mathcal { X } _ { \mathrm { g o a l } }$ . Note that the $x _ { i } \mathrm { { ^ { * } s } }$ need not all be distinct. The following property holds for all $m \in \{ 2 , \ldots , M _ { n } - 1 \}$

$$
\begin{array}{r l} & {\| x _ {m} - x _ {m - 1} \| \leq \| x _ {m} - \sigma_ {n} (\tau_ {m}) \| + \| \sigma_ {n} (\tau_ {m}) - \sigma_ {n} (\tau_ {m - 1}) \| + \| \sigma_ {n} (\tau_ {m - 1}) - x _ {m - 1} \|} \\ & {\qquad \leq \frac {r _ {n}}{2 + \theta} + \frac {\theta r _ {n}}{2 + \theta} + \frac {r _ {n}}{2 + \theta} = r _ {n}.} \end{array}
$$

Similarly, we can write $\begin{array} { r } { \| x _ { M _ { n } } - x _ { M _ { n } - 1 } \| \le \frac { r _ { n } } { 2 + \theta } + \frac { ( \theta + 1 / 2 ) r _ { n } } { 2 + \theta } + \frac { r _ { n } } { 2 ( 2 + \theta ) } = r _ { n } } \end{array}$ . Furthermore, we can lower bound the distance to the nearest obstacle for $m \in \{ 2 , \ldots , M _ { n } - 1 \}$ by:

$$
\inf _ {w \in X _ {\mathrm{obs}}} \| x _ {m} - w \| \geq \inf _ {w \in X _ {\mathrm{obs}}} \| \sigma_ {n} (\tau_ {m}) - w \| - \| x _ {m} - \sigma_ {n} (\tau_ {m}) \| \geq \frac {3 + \theta}{2 + \theta} r _ {n} - \frac {r _ {n}}{2 + \theta} = r _ {n},
$$

where the second inequality follows from the assumed δ -clearance of the path $\sigma _ { n } . \mathrm { \ A g a i n } .$ similarly, we can write $\begin{array} { r } { \operatorname* { i n f } _ { w \in X _ { \mathrm { o b s } } } \| x _ { M _ { n } } - w \| \ge \operatorname* { i n f } _ { w \in X _ { \mathrm { o b s } } } \left| | x _ { m } - \sigma _ { n } ( 1 ) | \right| - \| \sigma _ { n } ( 1 ) - w \| \ge \frac { \gamma ^ { 2 } } { 2 } . } \end{array}$ $\begin{array} { r } { \frac { 3 + \theta } { 2 + \theta } r _ { n } - \frac { r _ { n } } { 2 + \theta } = r _ { n } } \end{array}$ . Together, these two properties imply that, for $m \in \{ 2 , \ldots , M _ { n } \}$ , when a connection is attempted for $x _ { m } , \ x _ { m - 1 }$ will be in the search radius and there will be no obstacles in that search radius. In particular, this fact implies that either the algorithm will return a feasible path before considering $x _ { M _ { n } } .$ , or it will consider $x _ { M _ { n } }$ and connect it. Therefore, $\mathrm { F M T ^ { * } }$ is guaranteed to return a feasible solution when the event $A _ { n }$ occurs. Since the remainder of this proof assumes that $A _ { n }$ occurs, we will also assume $c _ { n } < \infty$

Finally, assuming $x _ { m }$ is contained in an edge, let $c ( x _ { m } )$ denote the unique cost-to-arrive of $x _ { m }$ in the graph generated by $\mathrm { F M T ^ { * } }$ at the end of the algorithm, just before the path is returned. If $x _ { m }$ is not contained in an edge, we set $c ( x _ { m } ) = \infty$ Note that $c ( \cdot )$ is well-defined, since if $x _ { m }$ is contained in any edge, it must be connected through a unique path to $x _ { \mathrm { i n i t } }$ . We claim that for all $m \in \{ 2 , \ldots , M _ { n } \}$ , either $\begin{array} { r } { c _ { n } \leq \sum _ { k = 1 } ^ { m - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ , or $\begin{array} { r } { c ( x _ { m } ) \leq \sum _ { k = 1 } ^ { m - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ . In particular, taking $n = M _ { n }$ , this inequality would imply that $c _ { n } \leq$ min $\begin{array} { r } { \{ c ( x _ { M _ { n } } ) , \sum _ { k = 1 } ^ { M _ { n } - 1 } \| x _ { k + 1 } - x _ { k } \| \} \le \sum _ { k = 1 } ^ { M _ { n } - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ , which, as argued before, would imply the claim.

The claim is proved by induction on m. The case of $m = 1$ is trivial, since the first step in the $\mathrm { F M T ^ { * } }$ algorithm is to make every collision-free connection between $x _ { \mathrm { i n i t } } = x _ { 1 }$ and the nodes contained in $B ( x _ { \mathrm { i n i t } } ; r _ { n } )$ , which will include $x _ { 2 }$ and, thus, $c ( x _ { 2 } ) = \| x _ { 2 } - x _ { 1 } \|$ . Now suppose the claim is true for $m - 1$ . There are four exhaustive cases to consider:

$$
1. c _ {n} \leq \sum_ {k = 1} ^ {m - 2} \| x _ {k + 1} - x _ {k} \|,
$$

2. $\begin{array} { r } { c ( x _ { m - 1 } ) \leq \sum _ { k = 1 } ^ { m - 2 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ and $\mathrm { F M T ^ { * } }$ terminates before considering $x _ { m }$ ·

3. $\begin{array} { r } { c ( x _ { m - 1 } ) \leq \sum _ { k = 1 } ^ { m - 2 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ and $x _ { m - 1 } \in V _ { \mathrm { o p e n } }$ when $x _ { m }$ is first considered,

4. $\begin{array} { r } { c ( x _ { m - 1 } ) \leq \sum _ { k = 1 } ^ { m - 2 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ and $x _ { m - 1 } \notin V _ { \mathrm { o p e n } }$ when $x _ { m }$ is first considered.

Case 1: $\begin{array} { r } { c _ { n } \leq \sum _ { k = 1 } ^ { m - 2 } \| x _ { k + 1 } - x _ { k } \| \leq \sum _ { k = 1 } ^ { m - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ , thus the claim is true for m. Without loss of generality, for cases 2–4 we assume that case 1 does not occur.

Case 2: $c ( x _ { m - 1 } ) < \infty$ implies that $x _ { m - 1 }$ enters $V _ { \mathrm { o p e n } }$ at some point during $\mathrm { F M T ^ { * } }$ . However, if $x _ { m - 1 }$ were ever the minimum-cost element of $V _ { \mathrm { o p e n } } , x _ { m }$ would have been considered, and thus $\mathrm { F M T ^ { * } }$ must have returned a feasible solution before $x _ { m - 1 }$ was ever the minimumcost element of $V _ { \mathrm { o p e n } }$ . Since the end-node of the solution returned must have been the minimum-cost element of $\begin{array} { r } { V _ { \mathrm { o p e n } } , \ c _ { n } \leq c ( x _ { m - 1 } ) \leq \sum _ { k = 1 } ^ { m - 2 } \| x _ { k + 1 } - x _ { k } \| \leq \sum _ { k = 1 } ^ { m - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ thus the claim is true for $m$

Case 3: $x _ { m - 1 } \in V _ { \mathrm { o p e n } }$ when $x _ { m }$ is first considered, $\| x _ { m } - x _ { m - 1 } \| \leq r _ { n } .$ , and there are no obstacles in $B ( x _ { m } ; r _ { n } )$ Therefore, $x _ { m }$ must be connected to some parent when it is first considered, and $\begin{array} { r } { c ( x _ { m } ) \leq c ( x _ { m - 1 } ) + \| x _ { m } - x _ { m - 1 } \| \leq \sum _ { k = 1 } ^ { m - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ , thus the claim is true for m.

Case 4: When $x _ { m }$ is first considered, there must exist $z \in B ( x _ { m } ; r _ { n } )$ such that $z$ is the minimum-cost element of $V _ { \mathrm { o p e n } } ,$ while $x _ { m - 1 }$ has not even entered $V _ { \mathrm { o p e n } }$ yet. Note that again, since $B ( x _ { m } ; r _ { n } )$ intersects no obstacles and contains at least one node in $V _ { \mathrm { o p e n } } , \ x _ { m }$ must be connected to some parent when it is first considered. Since $c ( x _ { m - 1 } ) < \infty$ , there is a well-defined path $\mathcal { P } = \{ v _ { 1 } , . . . , v _ { q } \}$ from $x _ { \mathrm { i n i t } } = v _ { 1 }$ to $x _ { m - 1 } = v _ { q }$ for some $q \in \mathbb { N }$ . Let $w = v _ { j }$ , where $j = \operatorname* { m a x } _ { i \in \{ 1 , \dots , q \} } \{ i : v _ { i } \in V _ { \mathrm { o p e n } }$ when $x _ { m }$ is first considered . Then there are two subcases, either $w \in B ( x _ { m } ; r _ { n } )$ or w $\notin B ( x _ { m } ; r _ { n } )$ . If $w \in B ( x _ { m } ; r _ { n } )$ , then,

$$
\begin{array}{r l} & c (x _ {m}) \leq c (w) + \| x _ {m} - w \| \leq c (w) + \| x _ {m - 1} - w \| + \| x _ {m} - x _ {m - 1} \| \\ & \quad \leq c (x _ {m - 1}) + \| x _ {m} - x _ {m - 1} \| \leq \sum_ {k = 1} ^ {m - 1} \| x _ {k + 1} - x _ {k} \|, \end{array}
$$

thus the claim is true for m (the second and third inequalities follow from the triangle inequality). If $w \not \in B ( x _ { m } ; r _ { n } )$ , then,

$$
c (x _ {m}) \leq c (z) + \| x _ {m} - z \| \leq c (w) + r _ {n} \leq c (x _ {m - 1}) + \| x _ {m} - x _ {m - 1} \| \leq \sum_ {k = 1} ^ {m - 1} \| x _ {k + 1} - x _ {k} \|,
$$

where the third inequality follows from the fact that $w \not \in B ( x _ { m } , r _ { n } )$ , which means that any path through w to $x _ { m }$ , in particular the path ${ \mathcal { P } } \cup { \boldsymbol { x _ { m } } }$ , must traverse a distance of at least $r _ { n }$ between w and $x _ { m }$ . Thus, in the final subcase of the final case, the claim is true for $m$

Hence, we can conclude that $\begin{array} { r } { c _ { n } \leq \sum _ { k = 1 } ^ { M _ { n } - 1 } \| x _ { k + 1 } - x _ { k } \| } \end{array}$ . As argued before, coupling this fact with equation (10), we can conclude that the event $\{ K _ { n } ^ { \beta } < \alpha ( M _ { n } - 1 ) \} \cap A _ { n }$ implies that $\begin{array} { r } { c _ { n } \le \kappa ( \alpha , \beta , \theta ) c ( \sigma _ { n } ^ { \prime } ) + \frac { r _ { n } } { 2 + \theta } } \end{array}$ , and the claim follows. □

Proof of Lemma $4 . 3 .$ The proof relies on a Poissonization argument. For $\nu \in ( 0 , 1 )$ , let $\tilde { n }$ be a random variable drawn from a Poisson distribution with parameter $\nu n$ (denoted as Poisson $( \nu n ) )$ . Consider the set of nodes $\widetilde V : = \mathtt { S a m p l e F r e e } ( \tilde { n } )$ , and for the remainder of the proof, ignore $x _ { \mathrm { i n i t } }$ (adding back $x _ { \mathrm { i n i t } }$ only decreases the probability in question, which we are showing goes to zero anyway). Then the locations of the nodes in $\widetilde { V }$ are distributed as a spatial Poisson process with intensity $\nu n / \mu ( \mathcal { X } _ { \mathrm { f r e e } } )$ . Therefore, for a Lebesgue-measurable region $R \subseteq \mathcal { X } _ { \mathrm { f r e e } }$ , the number of nodes in R is distributed as a Poisson random variable with distribution Poisson $\left( \nu n \mu ( R ) / \mu ( \mathcal { X } _ { \mathrm { f r e e } } ) \right)$ , independent of the number of nodes in any region disjoint with R (Karaman and Frazzoli, 2011, Lemma 11).

Let $\widetilde { K } _ { n } ^ { \beta }$ be the Poissonized analogue of $K _ { n } ^ { \beta }$ , namely $\widetilde { K } _ { n } ^ { \beta } : = \mathrm { c a r d } \Big \{ m \in \{ 1 , \dots , M _ { n } - 1 \}$ $B _ { n , m } ^ { \beta } \cap \widetilde { V } = \varnothing \}$ . Note that only the distribution of node locations has changed through Poissonization, while the balls $B _ { n , m } ^ { \beta }$ remain the same. From the definition of $\widetilde { V }$ , we can see that $\begin{array} { r } { \mathbb { P } \left( K _ { n } ^ { \beta } \geq \alpha ( M _ { n } - 1 ) ) \right) = \mathbb { P } \left( \widetilde { K } _ { n } ^ { \beta } \geq \alpha ( M _ { n } - 1 ) | \tilde { n } = n \right) } \end{array}$ . Thus, we have

$$
\begin{array}{l} \mathbb {P} \left(\widetilde {K} _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1))\right) = \sum_ {j = 0} ^ {\infty} \mathbb {P} \left(\widetilde {K} _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1)   |   \tilde {n} = j\right) \cdot \mathbb {P} \left(\tilde {n} = j\right) \\ \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \\ \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qend{array}\tag{11}
$$

where $a _ { \nu }$ is a positive constant that depends only on $\nu .$ The third line follows from the fact that $\mathbb { P } ( \widetilde { K } _ { n } ^ { \beta } \ge \alpha ( M _ { n } - 1 ) | \tilde { n } = j )$ is nonincreasing in $j$ , and the last line follows from a tail approximation of the Poisson distribution (Penrose, 2003, p. 17) and the fact that $\mathbb { E } [ \tilde { n } ] < n$ . Thus, since li $\mathrm { n } _ { n  \infty } ( 1 - e ^ { - a _ { \nu } n } ) = 1$ for any fixed $\nu \in ( 0 , 1 )$ , it sufices to show that $\begin{array} { r } { \operatorname* { l i m } _ { n \to \infty } \mathbb { P } ( \widetilde { K } _ { n } ^ { \beta } \geq \alpha ( M _ { n } - 1 ) ) = 0 } \end{array}$ to prove the statement of the lemma.

Since by assumption $\beta < \theta / 2 , B _ { n , 1 } ^ { \beta } , . . . , B _ { n , M _ { n } - 1 } ^ { \beta }$ are all disjoint. This disjointness means that for fixed $n ,$ the number of the Poissonized nodes that fall in each $B _ { n , m } ^ { \beta }$ is independent of the others and identically distributed as a Poisson random variable with mean equal to

$$
\frac {\mu (B _ {n , 1} ^ {\beta})}{\mu (\mathcal {X} _ {\mathrm{free}})} \nu n = \frac {\zeta_ {d} \left(\frac {\beta r _ {n}}{2 + \theta}\right) ^ {d}}{\mu (\mathcal {X} _ {\mathrm{free}})} \nu n = \frac {\nu \zeta_ {d} \beta^ {d} \gamma^ {d} \log (n)}{(2 + \theta) \mu (\mathcal {X} _ {\mathrm{free}})} := \lambda_ {\beta , \nu} \log (n),
$$

where $\lambda _ { \beta , \nu }$ is positive and does not depend on n. From this equation we get that for $m \in$ $\{ 1 , \ldots , M _ { n } - 1 \}$ ,

$$
\mathbb {P} (B _ {n, m} ^ {\beta} \cap \widetilde {V} = \emptyset) = e ^ {- \lambda_ {\beta , \nu} \log (n)} = n ^ {- \lambda_ {\beta , \nu}}.
$$

Therefore, $\widetilde { K } _ { n } ^ { \beta }$ is distributed according to a binomial distribution, in particular according to the Binomial $( M _ { n } - 1 , n ^ { - \lambda _ { \beta , \nu } } )$ distribution. Then for $n > \left( e ^ { - 2 } \alpha \right) ^ { - \frac { 1 } { \lambda _ { \beta , \nu } } } , e ^ { 2 } \mathbb { E } [ \widetilde { K } _ { n } ^ { \beta } ] < \alpha ( M _ { n } - 1 )$ , so from a tail approximation to the Binomial distribution (Penrose, 2003, p. 16),

$$
\mathbb {P} (\widetilde {K} _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1)) \leq e ^ {- \alpha (M _ {n} - 1)}.\tag{12}
$$

Finally, since by assumption $x _ { \mathrm { i n i t } } \notin \mathcal { X } _ { \mathrm { g o a l } }$ , the optimal cost is positive, i.e., $c ^ { * } > 0 $ ; this positivity implies that there is a lower-bound on feasible path length. Since the ball radii decrease to $0 ,$ it must be that lim $_ { \mathsf { l } _ { n \to \infty } } M _ { n } = \infty$ in order to cover the paths, and the lemma is proved. □

Proof of Lemma $4 { \cdot } 4 .$ Let $c _ { \operatorname* { m a x } } : = \operatorname* { m a x } _ { n \in \mathbb { N } } c ( \sigma _ { n } ^ { \prime } )$ ; the convergence of $c ( \sigma _ { n } ^ { \prime } )$ to a limiting value that is also a lower bound implies that $c _ { \mathrm { m a x } }$ exists and is finite. Then we have,

$$
\begin{array}{r l} & {\mathbb {P} \left(A _ {n, \theta} ^ {c}\right) \leq \sum_ {m = 1} ^ {M _ {n}} \mathbb {P} \left(B _ {n, m} \cap V = \emptyset\right) = \sum_ {m = 1} ^ {M _ {n}} \left(1 - \frac {\mu (B _ {n , m})}{\mu (\mathcal {X} _ {\mathrm{free}})}\right) ^ {n} = \sum_ {m = 1} ^ {M _ {n} - 1} \left(1 - \frac {\zeta_ {d} \left(\frac {r _ {n}}{2 + \theta}\right) ^ {d}}{\mu (\mathcal {X} _ {\mathrm{free}})}\right) ^ {n}} \\ & {\qquad + \left(1 - \frac {\zeta_ {d} \left(\frac {r _ {n}}{2 (2 + \theta)}\right) ^ {d}}{\mu (\mathcal {X} _ {\mathrm{free}})}\right) ^ {n}} \\ & {\leq M _ {n} \bigg (1 - \frac {\zeta_ {d} \gamma^ {d} \log (n)}{n (2 + \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})} \bigg) ^ {n} + \bigg (1 - \frac {\zeta_ {d} \gamma^ {d} \log (n)}{n (4 + 2 \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})} \bigg) ^ {n}} \\ & {\leq M _ {n} e ^ {- \frac {\zeta_ {d} \gamma^ {d} \log (n)}{(2 + \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})}} + e ^ {- \frac {\zeta_ {d} \gamma^ {d} \log (n)}{(4 + 2 \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})}}} \\ & {\leq \frac {(2 + \theta) c (\sigma_ {n} ^ {\prime})}{\theta r _ {n}} n ^ {- \frac {\zeta_ {d} \gamma^ {d}}{(2 + \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})}} + n ^ {- \frac {\zeta_ {d} \gamma^ {d}}{(4 + 2 \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})}}} \\ & {\leq \frac {(2 + \theta) c _ {\max}}{\theta \gamma} \log (n) ^ {- \frac {1}{d}} n ^ {\frac {1}{d} - \frac {\zeta_ {d} \gamma^ {d}}{(2 + \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})}} + n ^ {- \frac {\zeta_ {d} \gamma^ {d}}{(4 + 2 \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})}},} \end{array}\tag{13}
$$

where the third inequality follows from the inequality $( 1 ~ - ~ { \textstyle { \frac { 1 } { x } } } ) ^ { n } ~ \leq ~ e ^ { - { \frac { n } { x } } }$ , and the fourth inequality follows from the bound on $M _ { n }$ obtained in the proof of Lemma 4.2. As $n  \infty ,$ the second term goes to zero for any $\gamma > 0$ , while the first term goes to zero for any $\gamma > ( 2 + \theta ) \Big ( \mu ( \mathcal { X } _ { \mathrm { f r e e } } ) / ( d \zeta _ { d } ) \Big ) ^ { 1 / d }$ , which is satisfied by $\theta < 2 \eta$ . Thus $\mathbb { P } ( A _ { n , \theta } ^ { c } )  0$ and the lemma is proved. □

## Appendix B: Proof of Convergence Rate Bound

Proof of Theorem $4 . 6 .$ We proceed by first proving the tightest bound possible, carrying through all terms and constants, and then we make approximations to get to the final simplified result. Let $\varepsilon > 0 , \theta \in ( 0$ , min(2η, 1/4)), $\alpha , \beta \in ( 0 ,$ , min $( 1 , \varepsilon ) \theta / 8 )$ , and $\nu \in ( 0 , 1 )$ Let $H ( a ) = 1 + a ( \log ( a ) - 1 )$ , and $\begin{array} { r } { \gamma = 2 ( 1 + \eta ) \Big ( \frac { 1 } { d \zeta _ { d } } \Big ) ^ { 1 / d } } \end{array}$ so that $\begin{array} { r } { r _ { n } = \gamma \bigg ( \frac { \log ( n ) } { n } \bigg ) ^ { 1 / d } } \end{array}$ . Letting $n _ { 0 } > \left( \alpha / e ^ { 2 } \right) ^ { - \frac { ( 2 + \theta ) } { \nu \zeta _ { d } \beta ^ { d } \gamma ^ { d } } }$ and such that

$$
r _ {n _ {0}} <   \min \left\{2 \xi (2 + \theta), \frac {2 + \theta}{3 + \theta} \delta , \frac {\varepsilon (2 + \theta)}{8} c ^ {*} \right\},
$$

then for $n \geq n _ { 0 }$ , we claim that<sup>3</sup>,

$$
\begin{array}{l} \mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) <   \frac {1}{1 - e ^ {- \nu n H (\frac {n + 1}{\nu n})}} e ^ {- \frac {\alpha}{2} \left\lfloor \frac {2 + \theta}{\theta r _ {n}} c ^ {*} \right\rfloor \left(\log \left(\alpha \left\lfloor \frac {2 + \theta}{\theta r _ {n}} c ^ {*} \right\rfloor\right) + \zeta_ {d} \left(\frac {\beta r _ {n}}{2 + \theta}\right) ^ {d} \nu n\right)} \\ \qquad + \left\lfloor \frac {2 + \theta}{\theta r _ {n}} c ^ {*} \right\rfloor \left(1 - \zeta_ {d} \left(\frac {r _ {n}}{2 + \theta}\right) ^ {d}\right) ^ {n} + \left(1 - \zeta_ {d} \left(\frac {r _ {n}}{2 (2 + \theta)}\right) ^ {d}\right) ^ {n}. \end{array}
$$

(14)

To prove equation (14), note that from the proof of Theorem 4.1, equation (4) and Lemma 4.2 combine to give (using the same notation),

$$
\mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \leq \mathbb {P} (K _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1)) + \mathbb {P} (A _ {n, \theta} ^ {c}).
$$

From Equation (11) in the proof of Lemma 4.3, and a more precise tail bound (Penrose, 2003, page 17) relying on the assumptions of $n _ { 0 }$

$$
\mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \leq \left(\frac {1}{1 - e ^ {\nu n H (\frac {n + 1}{\nu n})}}\right) \mathbb {P} (\tilde {K} _ {n} ^ {\beta} \geq \alpha (M _ {n} - 1)) + \mathbb {P} (A _ {n, \theta} ^ {c}).
$$

By the same arguments that led to equation (12), but again applied with slightly more precise tail bounds (Penrose, 2003, page 16), we get,

$$
\mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \leq \left(\frac {1}{1 - e ^ {\nu n H (\frac {n + 1}{\nu n})}}\right) e ^ {- \frac {\alpha (M _ {n} - 1)}{2} \left(\log \left(\alpha (M _ {n} - 1)\right) + \frac {\nu \zeta_ {d} \beta^ {d} \gamma^ {d}}{(2 + \theta) \mu (\mathcal {X} _ {\mathrm{free}})} \log (n)\right)} + \mathbb {P} (A _ {n, \theta} ^ {c}).
$$

By the first three lines of equation (13) from the proof of Lemma 4.4 (there we upper-bounded $M _ { n } - 1$ by $M _ { n }$ for simplicity, here we carry through the whole term),

$$
\begin{array}{r l} & {\mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \leq \bigg (\frac {1}{1 - e ^ {\nu n H (\frac {n + 1}{\nu n})}} \bigg) e ^ {- \frac {\alpha (M _ {n} - 1)}{2} \Big (\log \big (\alpha (M _ {n} - 1) \big) + \frac {\nu \zeta_ {d} \beta^ {d} \gamma^ {d}}{(2 + \theta) \mu (\mathcal {X} _ {\mathrm{free}})} \log (n) \Big)}} \\ & {\qquad + (M _ {n} - 1) \bigg (1 - \frac {\zeta_ {d} \gamma^ {d} \log (n)}{n (2 + \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})} \bigg) ^ {n} + \bigg (1 - \frac {\zeta_ {d} \gamma^ {d} \log (n)}{n (4 + 2 \theta) ^ {d} \mu (\mathcal {X} _ {\mathrm{free}})} \bigg) ^ {n}.} \end{array}
$$

Finally, in this simplified configuration space, we can set all the approximating paths $\sigma _ { n }$ from the proof of Theorem 4.1 to just be the optimal path, allowing us to compute $M _ { n } - 1 =$ $\left\lfloor \frac { 2 + \theta } { \theta r _ { n } } \boldsymbol { c } ^ { * } \right\rfloor$ . Plugging this formula in, noting that $\mu ( \mathcal { X } _ { \mathrm { f r e e } } ) \leq 1$ , and simplifying by collecting terms into factors of $r _ { n }$ gives equation (14).

Grouping together constants in equation (14) into positive superconstants $A , B , C , D$ ， and E for simplicity and dropping the factor of $\frac { 1 } { 1 - e ^ { - \nu n H ( \frac { n + 1 } { \nu n } ) } }$ (which goes to 1 as $n \to \infty )$ 1 from the first term, the bound becomes,

$$
\begin{array}{l} \mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) <   e ^ {- A \left(\frac {n}{\log (n)}\right) ^ {1 / d} \left(\log (B) + \frac {1}{d} \log \left(\frac {n}{\log (n)}\right) + C \log (n)\right)} \\ \qquad \qquad + \left(\frac {n}{\log (n)}\right) ^ {1 / d} \cdot \left(1 - D \frac {\log (n)}{n}\right) ^ {n} + \left(1 - E \frac {\log (n)}{n}\right) ^ {n}, \\ \qquad \leq B ^ {- A \left(\frac {n}{\log (n)}\right) ^ {1 / d}} \cdot \left(\frac {n}{\log (n)}\right) ^ {- \frac {A}{d} \left(\frac {n}{\log (n)}\right) ^ {1 / d}} \cdot n ^ {- A C \left(\frac {n}{\log (n)}\right) ^ {1 / d}} \\ \qquad \qquad + \left(\frac {n}{\log (n)}\right) ^ {1 / d} \cdot n ^ {- D} + n ^ {- E}, \end{array}\tag{15}
$$

where the second inequality is just a rearrangement of the first term, and uses the inequality $( 1 - x / n ) ^ { n } \leq e ^ { - x }$ for the last two terms. As both n and $\frac { n } { \log ( n ) }$ approach , the first term must become negligible compared to the last two terms, no matter the values of the superconstants. Now noting that $\begin{array} { r } { E = \frac { D } { 2 ^ { d } } } \end{array}$ , we can write the asymptotic upper bound for $\mathbb { P } ( c _ { n } > ( 1 + \varepsilon ) c ^ { * } )$ as,

$$
\left(\log (n)\right) ^ {- \frac {1}{d}} n ^ {\frac {1}{d} - D} + n ^ {- \frac {D}{2 ^ {d}}}.
$$

Therefore the deciding factor in which term asymptotically dominates is whether or not $\begin{array} { r } { \frac { 1 } { d } - D \leq - \frac { D } { 2 ^ { d } } } \end{array}$ . Plugging in for the actual constants composing D, we $\mathrm { g e t }$

$$
{\frac {1}{d}} \leq \left(1 - {\frac {1}{2 ^ {d}}}\right) {\frac {1}{d}} \left({\frac {2 (1 + \eta)}{2 + \theta}}\right) ^ {d},
$$

or, equivalently,

$$
\eta \geq \frac {2 + \theta}{(2 ^ {d} - 1) ^ {1 / d}} - 1.\tag{16}
$$

However, since θ is a proof parameter that can be taken arbitrarily small (and doing so improves the asymptotic rate), if $\begin{array} { r } { \eta > \frac { 2 } { ( 2 ^ { d } - 1 ) ^ { 1 / d } } - 1 } \end{array}$ , then θ can always be chosen small enough so that equation (16) holds. Finally, we are left with,

$$
\mathbb {P} (c _ {n} > (1 + \varepsilon) c ^ {*}) \in \left\{ \begin{array}{l l} O \left((\log (n)) ^ {- \frac {1}{d}} n ^ {\frac {1}{d} \left(1 - \left((1 + \eta) \frac {2}{2 + \theta}\right) ^ {d}\right)}\right) & \text {if} \quad \eta \leq \frac {2}{(2 ^ {d} - 1) ^ {1 / d}} - 1, \\ O \left(n ^ {- \frac {1}{d} \left(\frac {1 + \eta}{2 + \theta}\right) ^ {d}}\right) & \text {if} \quad \eta > \frac {2}{(2 ^ {d} - 1) ^ {1 / d}} - 1, \end{array} \right.\tag{17}
$$

for arbitrarily small θ. By replacing θ by an arbitrarily small parameter $\rho$ that is additive in the exponent, the final result is proved. □

## Appendix C: Proof of Computational Complexity

Proof of Theorem 4.7. We first prove two results that are not immediately obvious from the description of the algorithm, about the number of computations of edge cost and how many times a node is considered for connection.

Lemma C.1 (Edge-Cost Computations). Consider the setup of Theorem 4.7. Let $M _ { F M T ^ { * } } ^ { ( 1 ) }$ be the number of computations of edge cost when $F M T ^ { * }$ is run on V using $r _ { n }$ . Similarly, let $M _ { P R M ^ { * } } ^ { ( 1 ) }$ be the number of computations of edge cost when PRM<sup>∗</sup> is run on V using $r _ { n }$ . Then in expectation,

$$
M _ {F M T ^ {*}} ^ {(1)} \leq M _ {P R M ^ {*}} ^ {(1)} \in O (n \log (n)).
$$

Proof. PRM<sup>∗</sup> computes the cost of every edge in its graph. For a given node, edges are only created between that node and nodes in the $r _ { n }$ -ball around it. The expected number of nodes in an $r _ { n }$ -ball is less than or equal to $( n / \mu ( \mathcal { X } _ { \mathrm { f r e e } } ) ) \zeta _ { d } r _ { n } ^ { d } = ( \zeta _ { d } / \mu ( \mathcal { X } _ { \mathrm { f r e e } } ) ) \gamma \log ( n )$ , and since there are n nodes, the number of edges in the PRM<sup>∗</sup> graph is $O ( n \log ( n ) )$ ). Therefore, $M _ { \mathrm { P R M } ^ { * } } ^ { ( 1 ) }$ is $O ( n \log ( n ) )$ .

For each node $x \in V , { \mathrm { F M T } } ^ { * }$ saves the associated set $N _ { x }$ of $r _ { n } \mathrm { - n e i g h b o r s } .$ . Instead of just saving a reference for each node $y \in N _ { x } , \ N _ { x }$ can also allocate memory for the real value Cost $( y , x )$ . Saving this value whenever it is first computed guarantees that $\mathrm { F M T ^ { * } }$ will never compute it more than once for a given pair of nodes. Since the only pairs of nodes considered are exactly those considered in $\mathrm { P R M ^ { * } }$ , it is guaranteed that $M _ { \mathrm { F M T ^ { * } } } ^ { ( \mathrm { \check { 1 } } ) } \le M _ { \mathrm { P R M ^ { * } } } ^ { ( \mathrm { 1 } ) }$ . Note that computation of the cost-to-arrive of a node already connected in the FMT<sup>∗</sup> graph was not factored in here, because it is just a sum of edge costs which have already been computed.

The following Lemma shows that lines 10–18 in Algorithm 2 are only run $O ( n )$ times, despite being contained in the loop at line 6, which runs $O ( n )$ times, and the loop at line 9, which runs $O ( \log ( n ) )$ times, which would seem to suggest that lines 10–18 are run $O ( n \log ( n ) )$ times.

Lemma C.2 (Node Considerations). Consider the setup of Theorem $4 . 7 .$ We say that a node is ‘considered’ when it has played the role of $x \in X _ { n e a r }$ in line 9 of Algorithm 2. Let $M _ { F M T ^ { * } } ^ { ( 2 ) }$ be the number of node considerations when $F M T ^ { * }$ is run on V using $r _ { n }$ , including multiple considerations of the same node. Then in expectation,

$$
M _ {F M T ^ {*}} ^ {(1)} \in O (n).
$$

Proof. Note that $X _ { \mathrm { n e a r } } ~ \subset ~ V _ { \mathrm { u n v i s i t e d } }$ and nodes are permanently removed from $V _ { \mathrm { u n v i s i t e d } }$ as soon as they are connected to a parent. Furthermore, if there are no obstacles within $r _ { n }$ of a given node, then it must be connected to a parent when it is first considered. Clearly then, considerations involving these nodes account for at most n considerations, so it sufices to show that the number of considerations involving nodes within $r _ { n }$ of an obstacle (denote this value by $M _ { o b s } )$ is $O ( n )$ in expectation.

Any node can only be considered as many times as it has neighbors, which is $O ( \log ( n ) )$ in expectation. Furthermore, as $n \to \infty$ , the expected number of nodes within $r _ { n }$ of an obstacle can be approximated arbitrarily well by $n \cdot S _ { o b s } \cdot r _ { n } ,$ where $S _ { o b s }$ is the constant surface area of the obstacles. This equation is just the density of points, $n _ { \mathrm { : } }$ , times the volume formula for a thin shell around the obstacles, which will hold in the large n limit, since $r _ { n } \to 0$ . Since $r _ { n } \in O ( ( \log ( n ) / n ) ^ { 1 / d } )$ , these combine to give,

$$
M _ {o b s} \in O (n (\log (n) / n) ^ {1 / d} \log (n)) = O ((\log (n)) ^ {1 + 1 / d} n ^ {1 - 1 / d}) \in O (n)
$$

in expectation, proving the lemma.

We are now ready to show that the computational complexity of $\mathrm { F M T ^ { * } }$ is $O ( n \log ( n ) )$ in expectation. As already pointed out in Lemma C.1, the number of calls to Cost is $O ( n \log ( n ) )$ . By Lemma C.2 and the fact that CollisionFree is called if and only if a node is under consideration, the number of calls to CollisionFree is $O ( n )$ . The number of calls to Near in which any computation is done, as opposed to just loading a set from memory, is bounded by $n ,$ , since neighbor sets are saved and thus are never computed more than once for each node. Since Near computation can be implemented to arbitrarily close approximation in $O ( \log ( n ) )$ time (Arya and Mount, 1995), the calls to Near also account for $O ( n \log ( n ) )$ time complexity. Since each node can have at most one parent in the graph T , E can only have at most n elements and since edges are only added, never subtracted, from E, the time complexity of building E is $O ( n )$ . Similarly, $V _ { \mathrm { u n v i s i t e d } }$ only ever has nodes subtracted and starts with n nodes, so subtracting from $V _ { \mathrm { u n v i s i t e d } }$ takes a total of $O ( n )$ time.

Operations on $V _ { \mathrm { o p e n } }$ can be done in $O ( n \log ( n ) )$ time if $V _ { \mathrm { o p e n } }$ is implemented as a binary min heap. As pointed out in Theorem 3.1, there are at most n additions to $V _ { \mathrm { o p e n } }$ , each taking O(log(card $V _ { \mathrm { o p e n } } ) )$ , and since card $V _ { \mathrm { o p e n } } \leq n _ { \mathrm { : } }$ , these additions take $O ( n \log ( n ) )$ time. Finding and deleting the minimum element of $V _ { \mathrm { o p e n } }$ also happens at most n times and also takes $O ( \log ( \mathrm { c a r d } V _ { \mathrm { o p e n } } ) )$ time, again multiplying to $O ( n \log ( n ) )$ time. There are also the intersections. Using hash maps, intersection can be implemented in time linear in the size of the smaller of the two sets (Ding and K¨onig, 2011). Both intersections, in lines 8 and 12, have $N _ { x }$ as one of the sets, which will have size $O ( \log ( n ) )$ . Since the intersection in line 8 happens once per while loop iteration, it happens at most n times, taking a total of $O ( n \log ( n ) )$ run time. Also, the intersection at line 12 is called exactly once per consideration, so again by Lemma C.2, this operation takes a total of $O ( n \log ( n ) )$ time. Finally, each computation of $y _ { \mathrm { m i n } }$ in line 13 happens once per consideration and takes time linear in card $Y _ { \mathrm { n e a r } } = O ( \log ( n ) )$ (note that computing $y _ { \mathrm { m i n } }$ does not require sorting $Y _ { \mathrm { n e a r } }$ , just finding its minimum, and that computations of cost have already been accounted for), leading to $O ( n \log ( n ) )$ in total for this operation. Note that the solution is returned upon algorithm completion, so there is no “query” phase. In addition, $V , \ V _ { \mathrm { o p e n } } , \ E$ , and $V _ { \mathrm { u n v i s i t e d } }$ all have maximum size of $n ,$ while saving $N _ { x }$ for up to n nodes requires $O ( n \log ( n ) )$ space, so $\mathrm { F M T ^ { * } }$ has space complexity $O ( n \log ( n ) )$ □

## Appendix D: AO of FMT∗ with Non-Uniform Sampling

Imagine sampling from $\varphi$ by decomposing it into a mixture density as follows. With probability $\ell ,$ draw a sample from the uniform density, and with probability $1 - \ell .$ , draw a sample from a second distribution with probability density function $( \varphi - \ell ) / ( 1 - \ell \mu ( \chi _ { \mathrm { f r e e } } ) )$ ). If $\mathrm { F M T ^ { * } }$ is run on only the (approximately $n \ell )$ nodes that were drawn from the uniform distribution, the entire proof of asymptotic optimality in Theorem 4.1 goes through after adjusting up the connection radius $r _ { n }$ by a factor of $( 1 / \ell ) ^ { 1 / d }$ . This fact can be seen by observing that the proof only relies on the expected value of the number of nodes in a $r _ { n }$ -ball, and the lower density and larger ball radius cancel out in this expectation, leaving the expected value the same as in the original proof. This cancellation formalizes the intuition that sparsely-sampled regions require searching wider to make good connections. Finally, note that adding samples before running $\mathrm { F M T ^ { * } }$ (while holding all parameters of FMT fixed, in particular acting as if n were the number of original samples for the purposes of computing $r _ { n } )$ can only improve the paths in the tree which do not come within a radius of the obstacles. Since the proof of $\mathrm { F M T ^ { * } } \mathrm { { s } \ A O }$ only employs approximating paths that are bounded away from the obstacles by at least $r _ { n } .$ the cost of these paths can only decrease if more points are added, and thus their costs must still converge to the optimal cost in probability. Thus when the (approximately $n ( 1 - \ell ) )$ nodes that were drawn from the second distribution are added back to the sample space, thus returning to the original non-uniform sampling distribution, asymptotic optimality still holds.

In our discussion of non-uniform sampling, we have repeatedly characterized a sampling distribution by its probability density function $\varphi .$ . We note for mathematical completeness that probability density functions are only defined up to an arbitrary set of Lebesgue measure 0. Thus all conditions stated in this discussion can be slightly relaxed in that they only have

to hold on a set of Lebesgue measure $\mu ( \mathcal { X } _ { \mathrm { f r e e } } )$

## Appendix E: AO of FMT∗ for General Costs

Asymptotic optimality of FMT<sup>∗</sup> for metric costs: To make the proof of AO go through, we do have the additional requirement that the cost be such that $\zeta _ { d } ,$ the measure of the unit cost-ball, be contained in (0, ). Such a cost-ball must automatically be contained in a Euclidean ball of the same center; denote the radius of this ball by $r _ { \mathrm { o u t e r } }$ . Then just three more things need to be adjusted in the proof of Theorem 4.1: First, condition (1) in the third paragraph of the proof needs to change to $\begin{array} { r } { \frac { r _ { \mathrm { o u t e r } } r _ { n } } { 2 ( 2 + \theta ) } \ < \ \xi } \end{array}$ . Second, condition (2) right after it needs to be changed to $\frac { 3 + \theta } { 2 + \theta } r _ { \mathrm { o u t e r } } r _ { n } < \delta$ . Finally, every time that length is mentioned, excepting cases when distance to the edge of obstacles or the goal region is being considered, length should be considered to mean cost instead. These replacements include the radii of the covering balls (so they are covering cost-balls), the function in the definition of $\Gamma _ { m } ,$ and the definition of $L _ { n , \alpha , \beta } ,$ for instance. The first two changes ensure that a sample is still drawn in the goal region so that the returned path is feasible, and ensure that the covering cost-balls remain collision-free. The third change is only notational, and the rest of the proof follows, since the triangle inequality still holds.

Asymptotic optimality of $\mathbf { F M T ^ { * } }$ for line integral costs with optimal-path connections: Because of the bounds on the cost density, the resulting new cost-balls with cost-radius r contain, and are contained in, Euclidean balls of radius $r / f _ { \mathrm { u p p e r } }$ and $r / f _ { \mathrm { l o w e r } }$ , respectively. Thus by adjusting constants for obstacle clearance and covering-cost-ball-radius, we can still ensure that the covering cost-balls have suficient points sampled within them, and that they are suficiently far from the obstacles. Furthermore, by only considering optimal connections, we are back to having a triangle inequality, since the cost of the optimal path connecting u to v is no greater than the sum of the costs of the optimal paths connecting u to w and w to v, for any w. Therefore we are again in a situation where the AO proof in Theorem 4.1 holds nearly unchanged.

Asymptotic optimality of FMT<sup>∗</sup> for line integral costs with straight-line connections: Assume that we can partition all of except some set of Lebesgue measure zero into finitely many connected, open regions, such that on each such region f is Lipschitz. Assume further that each of the optimum-approximating paths (from the definition of δ-robust feasibility) can be chosen such that it contains only finitely many points on the boundary of all these open regions. Note that this property does not have to hold for the optimal path itself, indeed the optimal path may run along a region’s boundary and still be arbitrarily approximated by paths that do not. Since the Lipschitz regions are open, each approximating path $\sigma _ { n }$ can be chosen such that there exist two sequences of strictly positive constants $\{ \phi _ { n , i } \} _ { i = 1 } ^ { \infty }$ and $\{ \psi _ { n , i } \} _ { i = 1 } ^ { \infty }$ such that: (a) $\phi _ { n , i } \stackrel { i \to \infty } { \longrightarrow } 0$ , and (b) for each i, for any point x on $\sigma _ { n }$ that is more than a distance $\phi _ { n , i }$ from any of the finitely many points on $\sigma _ { n }$ that lie on the boundary of a Lipschitz region, the $\psi _ { n , i } { \mathrm { - b a l l } }$ around x is entirely contained in a single Lipschitz region. This condition essentially requires that nearly all of each approximating path is bounded away from the edge of any of the Lipschitz regions. Taken together, these conditions allow for very general cost functions, including the common setting of f piecewise constant on finitely-many regions in  . To see how these conditions help prove AO, we examine the two reasons that the lack of a triangle inequality hinders the proof of AO for FMT<sup>∗</sup>.

The first is that, even if FMT<sup>∗</sup> returned a path that is optimal with respect to the straight-line PRM<sup>∗</sup> graph (this is the graph with nodes V and edges connecting every pair of samples that have a straight-line connection that is collision-free and has cost less than $r _ { n } )$ , there would be an extra cost associated with each edge (in the straight-line PRM<sup>∗</sup> graph too) for being the suboptimal path between its endpoints, and this is not accounted for in the proof. The second reason is that to ensure that each sample that is suficiently far from the obstacles is optimally connected to the existing FMT<sup>∗</sup> tree, the triangle inequality is used only in the first subcase of case 4 at the end of the proof of Lemma 4.2, where it is shown that the path returned by $\mathrm { F M T ^ { * } }$ is at least as good as any path that traces through samples in the covering balls in a particular way. This subcase is for when, at the time when a given sample $x \in \mathcal { P }$ is added to $\mathrm { F M T ^ { * } }$ , x’s parent in $\mathcal { P }$ (denoted $u )$ is not in $V _ { \mathrm { o p e n } }$ , but one of x’s ancestors in $\mathcal { P }$ is in $V _ { \mathrm { o p e n } }$ . If the triangle inequality fails, then it is possible that connecting x to the $\mathrm { F M T ^ { * } }$ tree through a path that is entirely contained in x’s search radius and runs through u (which $\mathrm { F M T ^ { * } }$ cannot do, since u $, \notin V _ { \mathrm { o p e n } } )$ would have given x a better cost-to-arrive than what it ends up with in the $\mathrm { F M T ^ { * } }$ solution. Therefore, for the proof to go through, either the triangle inequality needs to hold within all of the search balls of points contained in the covering balls (or on a sequence of balls $B _ { n , m } ^ { \mathrm { s e a r c h } }$ centered at the covering balls but with an $r _ { n } { \mathrm { - l a r g e r } }$ radius), or the triangle inequality needs to hold approximately such that this approximation, summed over all the $B _ { n , m } ^ { \mathrm { s e a r c h } }$ , goes to zero as $n  \infty$ . We venture to show that the latter case holds, using the fact that, on each of the portions of $\mathcal { X }$ on which f is Lipschitz, we have an approximate triangle inequality, and the approximation goes to zero quickly as $n \to \infty$

In particular, for a given optimum-approximating path, there are $O ( 1 / r _ { n } )$ of the $B _ { n , m } ^ { \mathrm { s e a r c h } }$ with radii $O ( r _ { n } )$ , and we can forget about the $B _ { n , m } ^ { \mathrm { s e a r c h } }$ containing points on the boundary of a Lipschitz region. Let $i _ { n } = \operatorname* { m i n } \{ i : \phi _ { i , n } >$ the radius of $B _ { n , m } ^ { \mathrm { s e a r c h } } \}$ . Note that $\sigma _ { n }$ can be taken to converge to the optimal path slowly enough that $\phi _ { i _ { n } , n } \stackrel { n \to \infty } { \longrightarrow } 0$ and $r _ { n } / \psi _ { i _ { n } , n } \stackrel { n  \infty } { \longrightarrow } 0$ . The boundary-containing $B _ { n , m } ^ { \mathrm { s e a r c h } }$ can be ignored because $\phi _ { i _ { n } , n } \stackrel { n \to \infty } { \longrightarrow } 0$ ensures that the boundarycontaining balls cover an asymptotically negligible length of the $\sigma _ { n } \mathrm { ' s }$ , and thus connections within them contribute negligibly to the cost of the $\mathrm { F M T ^ { * } }$ solution as $r _ { n } \to 0$ . Furthermore, since $r _ { n } / \psi _ { i _ { n } , n } \stackrel { n  \infty } { \longrightarrow } 0$ , we are left with $O ( 1 / r _ { n } )$ balls which, for $r _ { n }$ small enough, are each entirely inside a Lipschitz region, of which there are only finitely many, and thus there exists a global Lipschitz constant L that applies to all those balls, and does not change as $r _ { n } \to 0$ The suboptimality of a straight line contained in a ball of radius $r$ on a L-Lipschitz region is upper-bounded by its length $( 2 r )$ times the maximal cost-diferential on the ball $( 2 L r )$ Thus the total cost penalty on $\mathrm { F M T ^ { * } }$ over all the $B _ { n , m } ^ { \mathrm { s e a r c h } }$ of interest is $O ( r _ { n } ^ { 2 } / r _ { n } ) = O ( r _ { n } )$ , and $r _ { n } \to 0$ , so we expect straight-line FMT to return a solution that is asymptotically no worse than that produced by the “optimal-path” FMT in Section 5.2.2, and is therefore AO.

## Appendix F: AO of k-nearest FMT∗

Henceforth, we will call mutual-k<sub>n</sub>-nearest PRM<sup>∗</sup> the PRM<sup>∗</sup>-like algorithm in which the graph is constructed by placing edges only between mutual k<sub>n</sub>-nearest-neighbors. Three key facts ensure AO of k-nearest $\mathrm { F M T ^ { * } }$ , namely: (1) the mutual- $\cdot k _ { n }$ -nearest PRM<sup>∗</sup> graph arbitrarily approximates (in bounded variation norm) any path in $\mathcal { X } _ { \mathrm { f r e e } }$ for $k _ { n } = k _ { 0 } \log ( n )$ $k _ { 0 } > 3 ^ { d } e ( 1 { + } 1 / d ) , ( 2 ) k _ { n } .$ -nearest $\mathrm { F M T ^ { * } }$ returns at least as good a solution as any feasible path in the mutual- $\cdot k _ { n }$ -nearest PRM<sup>∗</sup> graph for which no node in the path has an obstacle between it and one of its $k _ { n }$ -nearest-neighbors, and (3) for any fixed positive clearance Υ and $k _ { n } =$ $k _ { 0 } \log ( n ) , k _ { 0 } > 3 ^ { d } e ( 1 + 1 / d )$ , the length of the longest edge containing a Υ-clear node in the $k _ { n }$ -nearest-neighbor graph (not mutual, this time) goes to zero in probability. Paralleling the terminology adopted in Section 3, we refer to samples in the mutual- $k _ { n }$ -nearest PRM<sup>∗</sup> graph as nodes. Leveraging these facts, we can readily show that $k _ { n }$ -nearest FMT<sup>∗</sup> with $k _ { n } ~ =$ $k _ { 0 }$ log(n), $k _ { 0 } > 3 ^ { d } e ( 1 + 1 / d )$ arbitrarily approximate an optimal solution with arbitrarily high probability as $n  \infty$ . Specifically, because the problem is δ-robustly feasible, we can take an arbitrarily-well-approximating path $\sigma$ that still has positive obstacle clearance, and arbitrarily approximate that path in the mutual- $\boldsymbol { { \cdot } } k _ { n }$ -nearest PRM<sup>∗</sup> graph by (1). By taking n larger and larger, since $\sigma _ { \mathrm { } } ^ { \prime } \mathrm { s }$ clearance is positive and fixed, the best approximating path in the mutual-k<sub>n</sub>-nearest $\mathrm { P R M ^ { * } }$ graph will eventually have some positive clearance with arbitrarily high probability. Then by (3), the length of the longest edge containing a point in the approximating path goes to zero in probability, and thus the probability that any node in the best approximating path in the mutual- $\cdot k _ { n }$ -nearest PRM<sup>∗</sup> graph will have one of its $k _ { n }$ -nearest-neighbors be farther away than the nearest obstacle goes to zero. Therefore by (2), k<sub>n</sub>-nearest $\mathrm { F M T ^ { * } }$ on the same samples will find at least as good a solution as that approximating path with arbitrarily high probability as $n \to \infty$ , and the result follows.

Proof of fact (1): To see why fact (1) holds, we need to adapt the proof of Theorem 35 from Karaman and Frazzoli (2011), which establishes AO of k-nearest PRM<sup>∗</sup>. Since nearly all of the arguments are the same, we will not recreate it in its entirety here, but only point out the relevant diferences, of which there are three. (a) We consider a slightly diferent geometric construction (with explanation why), which adds a factor of $3 ^ { d }$ to their $k _ { n }$ lower bound, (b) we adjust the proof for mutual- $\cdot k _ { n }$ -nearest PRM<sup>∗</sup>, as opposed to regular $k _ { n } \mathrm { - n e a r e s t }$ PRM<sup>∗</sup>, and (c) we generalize to show that there exist paths in the mutual- $\cdot k _ { n ^ { - } }$ nearest PRM<sup>∗</sup> graph that arbitrarily approximate any path in $\chi _ { \mathrm { f r e e } } .$ , as opposed to just the optimal path.

To explain diference (a), where the radius of the $B _ { n , m } ^ { \prime }$ was equal to $\delta _ { n }$ (defined at the beginning of Appendix D.2 in Karaman and Frazzoli (2011)), it should instead be given by,

$$
\min \left\{\delta , 3 (1 + \theta_ {1}) \left(\frac {(1 + 1 / d + \theta_ {2}) \mu (\mathcal {X} _ {\text {free}})}{\zeta_ {d}}\right) ^ {1 / d} \left(\frac {\log (n)}{n}\right) ^ {1 / d} \right\},\tag{18}
$$

with the salient diference being an extra factor of 3 in the second element of the min as compared to $\delta _ { n }$ . Note we are not redefining $\delta _ { n }$ , which is used to construct the smaller balls $B _ { n , m }$ as well as to determine the separation between ball centers for both sets of balls. Thus this change leaves the $B _ { n , m }$ ball unchanged, and the centers of the $B _ { n , m } ^ { \prime }$ balls unchanged, while asymptotically tripling the radius of the $B _ { n , m } ^ { \prime }$ balls. Note that this changes the picture given in (Karaman and Frazzoli, 2011, Figure 26), in that the outer circle should have triple the radius. This change is needed because in the second sentence in the paragraph after the proof of their Lemma 59, which says “Hence, whenever the balls $B _ { n , m }$ and $B _ { n , m + 1 }$ contain at least one node each, and $B _ { n , m } ^ { \prime }$ contains at most $k ( n )$ vertices, the k-nearest $\mathrm { P R M ^ { * } }$ algorithm attempts to connect all vertices in $B _ { n , m }$ and $B _ { n , m + 1 }$ with one another” might not hold in some cases. With the definition of $B _ { n , m } ^ { \prime }$ given there, for $\theta _ { 1 }$ arbitrarily small (which it may need to be), $B _ { n , m } ^ { \prime }$ is just barely wider than $B _ { n , m }$ (although it does still contain it and $B _ { n , m + 1 ; }$ since their centers get arbitrarily close as well). Then the point on the edge of $B _ { n , m }$ farthest from the center of $B _ { n , m + 1 }$ is exactly $\begin{array} { r } { \delta _ { n } - \frac { \delta _ { n } } { 1 + \theta _ { 1 } } = \frac { \theta _ { 1 } \delta _ { n } } { 1 + \theta _ { 1 } } } \end{array}$ (the diference in radii of $B _ { n , m } ^ { \prime }$ and $B _ { n , m } )$ from the nearest point on the edge of $B _ { n , m + 1 } ^ { \prime }$ , while it is $\frac { 2 + \theta _ { 1 } } { 1 + \theta } \delta _ { n }$ (the sum of the radii of $B _ { n , m }$ and $B _ { n , m + 1 }$ and the distance between their centers) from the farthest point in $B _ { n , m + 1 }$ Therefore, there may be a sample $x _ { m } \in B _ { n , m }$ and a sample in $x _ { m + 1 } \in B _ { n , m + 1 }$ that are much farther apart from one another than $x _ { m }$ is from some points which are just outside $B _ { n , m } ^ { \prime }$ , and therefore $x _ { m + 1 }$ may not be one of $x _ { m } \mathrm { { ' s } }$ k-nearest-neighbors, no matter how few samples fall in $B _ { n , m } ^ { \prime }$ . However, for n large enough, our proposed radius for $B _ { n , m } ^ { \prime }$ is exactly $3 \delta _ { n }$ , which results in the point on the edge of $B _ { n , m }$ farthest from the center of $B _ { n , m + 1 }$ being $\begin{array} { r } { 3 \delta _ { n } - \frac { \delta _ { n } } { 1 + \theta _ { 1 } } = \frac { 2 + 3 \theta _ { 1 } } { 1 + \theta _ { 1 } } \delta _ { n } } \end{array}$ (the diference in radii of $B _ { n , m } ^ { \prime }$ and $B _ { n , m } )$ from the nearest point on the edge of $B _ { n , m + 1 } ^ { \prime }$ , while it is $\frac { 2 + \theta _ { 1 } } { 1 + \theta } \delta _ { n }$ (the sum of the radii of $B _ { n , m }$ and $B _ { n , m + 1 }$ and the distance between their centers) from the farthest point in $B _ { n , m + 1 }$ (See Figure 18). Therefore, $\begin{array} { r } { \frac { 2 + 3 \theta _ { 1 } } { 1 + \theta _ { 1 } } \delta _ { n } > \frac { 2 + \theta _ { 1 } } { 1 + \theta } \delta _ { n } } \end{array}$ implies that any point in $B _ { n , m }$ is closer to every point in $B _ { n , m + 1 }$ than it is to any point outside $B _ { n , m } ^ { \prime } .$ This fact implies that if there are at most k samples in $B _ { n , m } ^ { \prime }$ , at least one of which $x _ { m + 1 }$ is in $B _ { n , m + 1 }$ and one of which $x _ { m }$ is in $B _ { n , m }$ (assume $x _ { m + 1 } \neq x _ { m }$ or they are trivially connected), then any point that is closer to $x _ { m }$ than $x _ { m + 1 }$ must be inside $B _ { n , m } ^ { \prime } ,$ of which there are only k in total, and thus $x _ { m + 1 }$ must be one of $x _ { m } ^ { \phantom { \dagger } }$ ’s k-nearest-neighbors. We have increased the volume of the $B _ { n , m } ^ { \prime }$ by a factor of $3 ^ { d }$ , making it necessary to increase the $k _ { \mathrm { P R M } }$ lower-bound (used in their Lemmas 58 and 59) by the same factor of $3 ^ { d }$ . This factor allows for the crucial part of the proof whereby it is shown that no more than $k _ { n }$ samples fall in each of the $B _ { n , m } ^ { \prime }$ On the subject of changing the $k _ { \mathrm { P R M } }$ lower-bound, we note that it may be possible to reduce k<sub>FMT</sub> $: = 3 ^ { d } e ( 1 + 1 / d )$ to $3 ^ { d } e / d$ by the same ideas used in our Theorem 4.1, since for this proof we only need convergence in probability, while Karaman and Frazzoli (2011) prove the stronger convergence almost surely.

![](Janson2013Fast_figs/d0c604c302a4b4348b65f0c3c2e87513f807808adbbd9a2776d423c58bcf9f13.jpg)  
Figure 18: An illustration of $B _ { n , m }$ and $B _ { n , m } ^ { \prime }$ in the proof of AO of k-nearest FMT<sup>∗</sup>

For diference (b), note that the proof of Karaman and Frazzoli (2011) states that when the event $A _ { n } ^ { \prime }$ holds, all samples in $B _ { n , m + 1 }$ must be in the $k _ { n }$ -nearest-neighbor sets of any samples in $B _ { n , m }$ . However a symmetrical argument shows that all samples in $B _ { n , m }$ must also be in the k-nearest-neighbor sets of any samples in $B _ { n , m + 1 }$ , and thus all samples in both balls must be mutual-k-nearest-neighbors. Since this argument is the only place in their proof that uses connectedness between samples, the entire proof holds just as well for mutual- $\cdot k _ { n }$ -nearest PRM<sup>∗</sup> as it does for $k _ { n } \mathrm { - n e a r e s t }$ PRM<sup>∗</sup>. For diference (c), there is nothing to prove, as the exposition in Karaman and Frazzoli (2011) does not use anything about the cost of the path being approximated until the last paragraph of their Appendix D. Up until then, a path (call it σ) is chosen and it is shown that the path in the $k _ { n }$ -nearest PRM<sup>∗</sup> graph that is closest to $\sigma$ in bounded variation norm converges to $\sigma$ in the same norm.

Proof of fact (2): To see why fact (2) holds, consider the nodes along a feasible path $\mathcal { P }$ in the mutual- $\boldsymbol { \cdot } \boldsymbol { k } _ { n }$ -nearest PRM<sup>∗</sup> graph, such that all of the nodes are farther from any obstacle than they are from any of their $k _ { n }$ -nearest-neighbors. We will show that for any point x along ${ \mathcal { P } } _ { : }$ , with parent in $\mathcal { P }$ denoted by $u ,$ if $k _ { n }$ -nearest FMT<sup>∗</sup> is run through all the samples (i.e., it ignores the stopping condition of $z \in \mathcal { X } _ { \mathrm { g o a l } }$ in line $6 )$ , then the cost-to-arrive of $x$ in the solution path is no worse than the cost-to-arrive of $x$ in $\mathcal { P }$ , assuming the same is true for all of $x _ { \mathrm { ~ S ~ } } ^ { \prime }$ ancestors in $\mathcal { P }$ . By feasibility, the endpoint of $\mathcal { P }$ is in $\mathcal { X } _ { \mathrm { f r e e } }$ , and then induction on the nodes in $\mathcal { P }$ implies that this endpoint either is the end of a $k _ { n }$ -nearest $\mathrm { F M T ^ { * } }$ solution path with cost no greater than that of $\mathcal { P } _ { : }$ or $k _ { n }$ -nearest $\mathrm { F M T ^ { * } }$ stopped before the endpoint of $\mathcal { P }$ was considered, in which case $k _ { n }$ -nearest FMT<sup>∗</sup> returned an even lower-cost solution than the path that would have eventually ended at the endpoint of $\mathcal { P }$ . Note that we are not restricting the edges in k-nearest $\mathrm { F M T ^ { * } }$ to be drawn from those in the mutual-k-nearest PRM<sup>∗</sup> graph, indeed $k _ { n }$ -nearest FMT<sup>∗</sup> can now potentially return a solution strictly better than any feasible path through the mutual-k-nearest PRM<sup>∗</sup> graph.

We now show that $x$ ’s cost-to-arrive in the $k _ { n }$ -nearest FMT<sup>∗</sup> solution is at least as good as x’s cost-to-arrive in $\mathcal { P } _ { \cdot }$ , given that the same is true of all of $x _ { \mathrm { ~ S ~ } } ^ { \prime }$ ancestors in $\mathcal { P }$ . Recall that by assumption, all connections in $\mathcal { P }$ are to mutual- $\cdot k _ { n }$ -nearest-neighbors, and that for all nodes $x$ in $\mathcal { P }$ , all of $x _ { \mathrm { ~ S ~ } } ^ { \prime }$ (not-necessarily-mutual) $k _ { n }$ -nearest-neighbors are closer to $x$ than the nearest obstacle is to $x _ { i }$ , and thus the line connecting $x$ to any of its $k _ { n }$ -nearest-neighbors must be collision-free. Note also that $x _ { \mathrm { ~ S ~ } } ^ { \prime }$ parent in ${ \mathcal { P } } ,$ , denoted by $u ,$ has finite cost in the $k _ { n } \mathrm { - n e a r e s t }$ $\mathrm { F M T ^ { * } }$ tree by assumption, which means it must enter $V _ { \mathrm { o p e n } }$ at some point in the algorithm. Since we are not stopping early, u must also be the minimum-cost node in $V _ { \mathrm { o p e n } }$ at some point, at which point x will be considered for addition to $V _ { \mathrm { o p e n } }$ if it had not been already. Now consider the following four exhaustive cases for when x is first considered $( \mathrm { i . e . }$ $x _ { \mathrm { ~ S ~ } } ^ { \prime }$ first iteration in the for loop at line 9 of Algorithm 2). (a) $u \in V _ { \mathrm { o p e n } } \mathrm { . }$ : then $u \in Y _ { \mathrm { n e a r } }$ and ux is collision-free, so when x is connected, its cost-to-arrive is less than that of u added to Cost $( u , x )$ , which in turn is less than the cost-to-arrive of x in $\mathcal { P }$ (by the triangle inequality). (b) u had already entered and was removed from $V _ { \mathrm { o p e n } }$ : this case is impossible, since u and x are both among one anothers’ $k _ { n } .$ -nearest-neighbors, and thus x must have been considered at the latest when u was the lowest-cost-to-arrive node in $V _ { \mathrm { o p e n } } ,$ just before it was removed. (c) $u \in V _ { \mathrm { u n v i s i t e d } }$ and $x _ { \mathrm { ~ S ~ } } ^ { \prime }$ closest ancestor in $V _ { \mathrm { o p e n } }$ , denoted $w$ , is a $k _ { n }$ -nearest-neighbor of $x { : }$ by assumption, wx is collision-free, so when x is connected, its cost-to-arrive is no more than that of w added to Cost $( w , x )$ , which in turn is less than that of the cost-to-arrive of $x$ in $\mathcal { P }$ (again, by the triangle inequality). (d) $u \in V _ { \mathrm { u n v i s i t e d } }$ and $w$ (defined as in the previous case) is not a $k _ { n }$ -nearest-neighbor of x: denoting the current lowest-cost-to-arrive node in $V _ { \mathrm { o p e n } }$ by z, we know that the cost-to-arrive of z is no more than that of $w .$ , and since $x$ is a mutual- $\cdot k _ { n }$ -nearest-neighbor of $z , z$ is also a $k _ { n } .$ -nearest-neighbor of x. Furthermore, we know that since w is not a $k _ { n } .$ -nearest-neighbor of x, Cost $( w , x ) \ge \mathtt { C o s t } ( z , x )$ . Together, these facts give us that when x is connected, its cost-to-arrive is no more than that of z added to Cost $( z , x )$ , which is no more than that of w added to $\mathtt { C o s t } ( w , x )$ , which in turn is no more than the cost-to-arrive of x in $\mathcal { P }$ (again, by the triangle inequality).

Proof of fact (3): To see why fact (3) holds, denote the longest edge in the $k _ { n }$ -nearestneighbor graph by $\hat { e } _ { n } ^ { \mathrm { m a x } }$ , let

$$
e _ {n} := \left(\frac {e k _ {0} \mu (\mathcal {X} _ {\mathrm{free}}) \log (n)}{\zeta_ {d} (n - 1)}\right) ^ {1 / d},
$$

and note that

$\mathbb { P } ( \hat { e } _ { n } ^ { \mathrm { m a x } } > e _ { n } ) \le \mathbb { P } ( \mathrm { a n y } ~ e _ { n } .$ -ball around a sample contains fewer than $k _ { n }$ neighbors)

$\leq n \mathbb { P } ( \mathrm { t h e } ~ e _ { n }$ -ball around v contains fewer than $k _ { n }$ neighbors),

(19)

where v is some arbitrary sample. Finally, observe that $e _ { n } \stackrel { n \to \infty } { \longrightarrow } 0$ and for $e _ { n } \ < \ \Upsilon$ , the number of neighbors in the $e _ { n } { \mathrm { - b a l l } }$ around any sample is a binomial random variable with parameters $n - 1$ and $\frac { e k _ { n } } { n - 1 }$ , so we can use the bounds in (Penrose, 2003, page 16) to obtain,

$$
\begin{array}{r l} & {\mathbb {P} (\hat {e} _ {n} ^ {\max} > e _ {n}) \leq n e ^ {- e k _ {n} H (\frac {k _ {n} - 1}{k _ {n}} e)}} \\ & {\qquad \leq n ^ {1 - e k _ {0} H (\frac {k _ {n} - 1}{k _ {n}} e)}} \\ & {\qquad \leq n ^ {- 1 6} \qquad \mathrm{for} n \geq 2,} \end{array}\tag{20}
$$

where $H ( a ) = 1 + a - a \log ( a )$ . Thus since $n ^ { - 1 6 } \stackrel { n \to \infty } { \longrightarrow } 0$ and $e _ { n } \stackrel { n \to \infty } { \longrightarrow } 0$ , we have the result.

## References

R. Alterovitz, S. Patil, and A. Derbakova. Rapidly-exploring roadmaps: Weighing exploration vs. refinement in optimal motion planning. In Proc. IEEE Conf. on Robotics and Automation, pages 3706–3712, 2011.

N. M. Amato, O. B. Bayazit, L. K. Dale, C. Jones, and D. Vallejo. Choosing good distance metrics and local planners for probabilistic roadmap methods. In Proc. IEEE Conf. on Robotics and Automation, volume 1, pages 630–637, May 1998.

O. Arslan and P. Tsiotras. Use of relaxation methods in sampling-based algorithms for optimal motion planning. In Proc. IEEE Conf. on Robotics and Automation, pages 2421– 2428, May 2013.

S. Arya and D. M Mount. Approximate range searching. In Proceedings of the eleventh annual symposium on Computational geometry, pages 172–181. ACM, 1995.

J. Barraquand, L. Kavraki, R. Motwani, J.-C. Latombe, Tsai-Y. Li, and P. Raghavan. A random sampling scheme for path planning. In International Journal of Robotics Research, pages 249–264. Springer, 2000.

D. P. Bertsekas. Dynamic Programming and Optimal Control, volume 1. Athena Scientific, third edition, 2005.

J. Bezanson, S. Karpinski, V. Shah, and A. Edelman. Ejulia: A fast dynamic language for technical computing. 2012. Available at http://arxiv.org/abs/1209.5145.

R. Bohlin and L. E. Kavraki. Path planning using lazy PRM. In Proc. IEEE Conf. on Robotics and Automation, pages 521–528, 2000.

S. Cabello and M. Jejˇciˇc. Shortest paths in intersection graphs of unit disks. Technical report, 2014. Available at http://arxiv.org/abs/1402.4855.

T. M. Chan and A. Efrat. Fly cheaply: On the minimum fuel consumption problem. Journal of Algorithms, 41(2):330–337, 2001.

T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein. Introduction to algorithms. MIT Press, Cambridge, second edition, 2001.

I. A. S¸ucan, M. Moll, and L. E. Kavraki. The Open Motion Planning Library. IEEE Robotics & Automation Magazine, 19(4):72–82, December 2012.

B. Ding and A. C. K¨onig. Fast set intersection in memory. Proc. VLDB Endow., 4(4): 255–266, January 2011.

J. D. Gammell, S. S. Srinivasa, , and T. D. Barfoot. BIT<sup>∗</sup> : Batch informed trees for optimal sampling-based planning via dynamic programming on implicit random geometric graphs. Technical report, 2014. Available at http://arxiv.org/abs/1405.5848v2.

D. Hsu. Randomized single-query motion planning in expansive spaces. PhD thesis, Stanford University, 2000.

D. Hsu, J. C. Latombe, and R. Motwani R. Path planning in expansive configuration spaces. International Journal of Computational Geometry & Applications, 9:495–512, 1999.

D. Hsu, J.-C. Latombe, and H. Kurniawati. On the probabilistic foundations of probabilistic roadmap planning. International Journal of Robotics Research, 25(7):627–643, 2006.

L. Jaillet and T. Sim´eon. A PRM-based motion planner for dynamically changing environments. In Proc. IEEE Conf. on Robotics and Automation, pages 1606–1611, 2004.

S. Karaman and E. Frazzoli. Sampling-based algorithms for optimal motion planning. International Journal of Robotics Research, 30(7):846–894, 2011.

L. E. Kavraki, P. Svestka, J.-C. Latombe, and M.H. Overmars. Probabilistic roadmaps for path planning in high-dimensional configuration spaces. IEEE Transactions on Robotics and Automation, 12(4):566 –580, 1996.

L. E. Kavraki, M. N. Kolountzakis, and J.-C. Latombe. Analysis of probabilistic roadmaps for path planning. IEEE Transactions on Robotics and Automation, 14(1):166–171, 1998.

M. Kobilarov. Cross-entropy motion planning. International Journal of Robotics Research, 31(7):855–871, 2012.

S. Koenig, M. Likhachev, and D. Furcy. Lifelong planning A. Artificial Intelligence, 155(1): 93–146, 2004.

A. M. Ladd and L. E. Kavraki. Measure theoretic analysis of probabilistic path planning. IEEE Transactions on Robotics and Automation, 20(2):229–242, 2004.

S. Lavalle. Planning Algorithms. Cambridge University Press, 2006.

S. M. LaValle and J. J. Kufner. Randomized kinodynamic planning. International Journal of Robotics Research, 20(5):378–400, 2001.

J. D. Marble and K. E. Bekris. Towards small asymptotically near-optimal roadmaps. In Proc. IEEE Conf. on Robotics and Automation, pages 2557–2562, 2012.

M. Penrose. Random Geometric Graphs. Oxford University Press, 2003.

J. M Phillips, N. Bedrossian, and L. E. Kavraki. Guided expansive spaces trees: A search strategy for motion- and cost-constrained state spaces. In Proc. IEEE Conf. on Robotics and Automation, pages 3968–3973, 2004.

E. Plaku, K. E. Bekris, B. Y. Chen, A. M. Ladd, and L. E. Kavraki. Sampling-based roadmap of trees for parallel motion planning. IEEE Transactions on Robotics, 21(4):597–608, 2005.

L. Roditty and M. Segal. On bounded leg shortest paths problems. Algorithmica, 59(4): 583–600, 2011.

O. Salzman and D. Halperin. Asymptotically near-optimal motion planning using lower bounds on cost. 2014. Available at http://arxiv.org/abs/1403.7714.

G. S´anchez and J.-C. Latombe. A single-query bi-directional probabilistic roadmap planner with lazy collision checking. In R. Jarvis and A. Zelinsky, editors, Robotics Research, volume 6 of Springer Tracts in Advanced Robotics, pages 403–417. Springer Berlin Heidelberg, 2003.

E. Schmerling, L. Janson, and M. Pavone. Optimal sampling-based motion planning under diferential constraints: the driftless case. Technical report, 2014a. Submitted to Proc. IEEE Conf. on Robotics and Automation, available at http://arxiv.org/abs/1403. 2483/.

E. Schmerling, L. Janson, and M. Pavone. Optimal sampling-based motion planning under diferential constraints: the drift case with linear afine dynamics. Technical report, 2014b. Submitted to Proc. IEEE Conf. on Robotics and Automation, available at http://arxiv. org/abs/1405.7421/.

J. A. Sethian. A fast marching level set method for monotonically advancing fronts. Proceedings of the National Academy of Sciences, 93(4):1591–1595, 1996.

M. Sniedovich. Dijkstra’s algorithm revisited: the dynamic programming connexion. Control and cybernetics, 35:599–620, 2006.

J. Starek, E. Schmerling, L. Janson, and M. Pavone. Bidirectional Fast Marching Trees: An optimal sampling-based algorithm for bidirectional motion planning. Technical report, 2014. Submitted to Proc. IEEE Conf. on Robotics and Automation, available at http: //www.stanford.edu/<sub>\~</sub>pavone/papers/Starek.Schmerling.ea.ICRA15.pdf.

S. Thrun, W. Burgard, and D. Fox. Probabilistic Robotics. The MIT Press, 2005.

A. Valero-Gomez, J. V. Gomez, S. Garrido, and L. Moreno. The path to eficiency: Fast marching method for safer, more eficient mobile robot trajectories. Robotics Automation Magazine, IEEE, 20(4):111–120, 2013.