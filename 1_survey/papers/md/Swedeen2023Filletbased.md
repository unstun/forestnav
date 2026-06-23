---
citation_key: Swedeen2023Filletbased
arxiv_id: 2302.11648
arxiv_url: https://arxiv.org/abs/2302.11648
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:33:41Z
origin: ai+web
reviewed: false
---

Paper Categories: (1), (2), (3)

# Introduction

The ability to plan paths through complex obstacles is a fundamental requirement of many mobile robot applications and has been shown to be an NP-complete problem in general [@Lavalle2006]. A variety of methods exist to decompose this NP-complete problem into manageable subproblems. One class of methods that has seen explosive growth in recent years is sample-based motion planning techniques [@Gammell2014; @Hussain2015; @Karaman2011; @Moon2015; @Nasir2013; @Noreen2016; @Yang2014]. Of particular note is the Rapidly-exploring Random Tree (RRT) and its optimal variant, RRT\* [@Karaman2011]. RRT quickly plans obstacle free paths for systems with arbitrary motion primitives. RRT\* provides probabilistic guarantees for asymptotically converging to the optimal path, although it is not well-suited for nonholonomic motion constraints. This work contributes to the RRT\* literature by developing techniques that can naturally consider the curvature constraints of a mobile robot with convergence times similar to that of straight-line motion primitives.

In its most simple form, RRT iteratively builds a search tree to randomly explore the environment. A sample point is randomly selected at each iteration and primitive motions are used to extend the tree in the direction of the sampled point. The use of general primitive motions enables the application of RRT to a wide range of problems with guarantees of probabilistic completeness [@Lavalle2006]. However, the path that RRT finds is typically far from optimal. [@Karaman2011] developed RRT\*, which makes two modifications to the RRT algorithm that probabilistically result in asymptotic optimality. Both modifications perform local optimizations to the tree using a neighborhood of nodes around each new point being added to the tree. These local optimizations work to add and remove edges between existing nodes, requiring the motion primitives to be able to find a continuous path to connect the corresponding states represented by the nodes. This exact connection requirement is not required by the original RRT algorithm, so the RRT\* changes are not generally applicable to all applications of RRT. Moreover, the same random sampling that ensures that RRT finds a solution causes the asymptotic convergence to the optimal solution by RRT\* to be quite slow [@Akgun2011; @Gammell2014; @Kobilarov2012; @Nasir2013; @Noreen2016].

Exactly connecting two states can become difficult when considering the motion constraints of wheeled vehicles, such as path curvature. One common method for considering curvature constraints is to plan with straight-lines and arcs using techniques such as Dubin's and Reed-Shepp paths [@Beard2012; @Lavalle2006]. While these techniques provide the shortest paths between oriented waypoints, they are not well-suited for the local optimization procedures in RRT\* due to the inclusion of orientation [@cui2018]. The path exactly connecting two oriented points can vary significantly with small changes in orientation. An alternative motion primitive in the form of a fillet was used in [@Yang2014; @{spline_rrt*}]. Instead of connecting two points, a fillet connects two straight-line segments with a curve that starts on the first segment and ends on the second segment. Small changes in each line will produce small changes in the path length, making the fillet approach amenable to the local optimizations required by RRT\*. In the case of [@Yang2014; @{spline_rrt*}], Bézier curves were used to connect the line segments, with the added benefit that continuous change in curvature is guaranteed.

While fillets enable the use of local optimization techniques, convergence to the optimal solution is naturally rather slow in RRT\*. To overcome slow convergence rates, many alternative sampling and path refinement procedures have been introduced [@Akgun2011; @Gammell2014; @Kobilarov2012; @Nasir2013; @Tahir2018]. This work utilizes two such approaches. In [@Gammell2014], Informed RRT\* (I-RRT\*) attempts to reduce the sampling space by providing a conservative estimate of the area that will contain the optimal solution. In [@Nasir2013], Smart RRT\* (S-RRT\*) provides an alternative sampling heuristic as well as a path refinement procedure to avoid waiting for the probabilistic sampling to straighten the path. We then combine ideas from [@Gammell2014] and [@Nasir2013] to develop the novel Smart and Informed RRT\* (SI-RRT\*) which provides greedy refinement of the solution without as many parameters to tune as S-RRT\*.

This paper develops a Fillet-based RRT\* (FB-RRT\*) algorithm for curvature constrained path planning. Similar to [@Yang2014; @{spline_rrt*}], a fillet approach is used to locally connect points. Contributions to [@Yang2014; @{spline_rrt*}] include the generalization of the fillet structure for RRT planning, a relaxation of connection assumptions that increases flexibility in growing the tree, and a newly developed rewiring procedure to ensure continuity and cost improvement in the resulting path. Established sampling and path refinement procedures are also extended to the fillet structure. A minor contribution of this work is the combination of two sampling heuristics [@Gammell2014; @Nasir2013] within the fillet framework.

The remainder of the paper proceeds as follows. In Section [2](#section:backround){reference-type="ref" reference="section:backround"}, the basics of RRT and RRT\* are introduced. Section [3](#section:fillet){reference-type="ref" reference="section:fillet"} then introduces the fillet approach to local planning. Section [4](#sec:fillet-rrt-star){reference-type="ref" reference="sec:fillet-rrt-star"} develops procedures for incorporating the fillet approach into RRT\* with a brief description of reverse fillet considerations given in Appendix [9](#sec:reverse_fillet){reference-type="ref" reference="sec:reverse_fillet"}. Section [5](#section:improving_convergence){reference-type="ref" reference="section:improving_convergence"} then develops the smart-and-informed sampling and path refinement procedures and presents the Fillet-based RRT\* algorithm. Results are presented in Section [6](#sec:results){reference-type="ref" reference="sec:results"} using the Open Motion Planning Library (OMPL) [@ompl] to benchmark the performance of RRT\* using a straight-line motion primitive, an arc-based fillet, a Bézier curve fillet, Dubin's paths, and various sampling techniques. Concluding remarks are given in Section [7](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}.

# The Rapidly-exploring Random Tree {#section:backround}

RRT-based algorithms are commonly broken into a series of generalized space sampling and tree growing procedures. RRT's variants (including RRT\*) refine and augment these procedures. This section defines several basic procedures, giving them context within RRT and RRT\*. The procedures in this section are found in [@Karaman2011; @bezier_curves] with variations in notation. They are included for the sake of completeness in presenting the Fillet-Based RRT\* (FB-RRT\*) formulation and sampling heuristics in Sections [3](#section:fillet){reference-type="ref" reference="section:fillet"} through [5](#section:improving_convergence){reference-type="ref" reference="section:improving_convergence"}.

## Notation

RRT-based algorithms iteratively construct a rooted, out-branching tree to find a path through the state space. The tree is an acyclic directed graph denoted as $T=\{V,E\}$, where $V$ is the set of nodes or vertices within the tree and $E \subset V \times V$ denotes the set of edges between vertices. If an edge points from $v_1$ to $v_2$, $v_2$ is referred to as the child of $v_1$ and $v_1$ as the parent of $v_2$. The root has no parent while all other vertices have exactly one parent. Each vertex can have multiple children. Each vertex within $V$ corresponds to a state in the $d$-dimensional state space denoted as $X \subset \mathbb{R}^d$. Note that we will assume that $X \subset \mathbb{R}^2$, although that is certainly not the case for general RRT formulations. The tree is initialized with solely the root node, i.e. $V = \{x_{r}\}$, $E = \varnothing$. Nodes are added to the tree to find a path to the target set, $X_{t} \subset X$. The path must avoid the space blocked by obstacles, $X_{obs} \subset X$, staying within the free space, $X_{free} = X \setminus X_{obs}$.

Paths through the state space are written as an ordered subset of $X$. In RRT\*, the paths are assigned a cost, typically the path length. Allowing $P(X)$ to denote the power set of $X$, the cost is a mapping $c:P(X) \rightarrow \mathbb{R}_+$. The closed ball of radius $r \in \mathbb{R}_+$ centered at $x \in \mathbb{R}^d$ is denoted as $\mathcal{B}_{x,r} = \left\{y \in X : \left\|y-x\right\| \leq r \right\}$. $X_{s} \subset X_{free}$ is the set of states from which the additional nodes will be sampled. Additional notation is summarized in Table [\[tab:notation\]](#tab:notation){reference-type="ref" reference="tab:notation"}.

## Common Sampling-based Planning Procedures

The literature on sample-based planning defines planning algorithms using a number of procedures. We now define several generic procedures that can be found in [@Karaman2011] with notation changed to match the sequel.

::: procedure
**procedure 1** ($T \leftarrow Initialize(x_{r})$). *Returns an initialized tree with $x_{r} \in X$ as the root node and no edges, i.e. $T \leftarrow \{V,E\}$, $V \leftarrow \{x_{r}\}$, and $E \leftarrow \varnothing$.*
:::

::: {#procedure:sample .procedure}
**procedure 2** ($x_{rand} \leftarrow Sample(X_{s})$). *Returns a random state from the set $X_{s} \subset X$.*
:::

::: procedure
**procedure 3** ($x_{nearest} \leftarrow Nearest(x_{rand},T)$). *Finds the nearest vertex in the set $V$ to the state $x_{rand} \in X$ using the 2-norm as a distance.*
:::

::: procedure
**procedure 4** ($X_{near} \leftarrow Near_{\rho,\alpha}(x_{rand},T)$). *Finds the nearest $\alpha \in \mathbb{Z}_+$ vertices that are within a given radius[^1], $\rho \in \mathbb{R}_+$, of the point $x_{rand} \in X$.*
:::

The constant $\alpha$ is used to prevent too many connections from being attempted in a given iteration [@Lavalle2006].

::: {#procedure:steer .procedure}
**procedure 5** ($x_{n} \leftarrow Steer_\eta(x,y)$). *Returns a point that is within a predefined distance $\eta \in \mathbb{R}_+$ from $x \in X$ in the direction of $y \in X$, i.e. $$\begin{equation*}
    Steer_\eta(x,y) = argmin_{\{z \in X : \|z - x \| \leq \eta\}} \|z - y\|
\end{equation*}$$*
:::

The Steer function prevents long edges from being added to RRT search trees. This is important because it reduces the expected extension length at each iteration and likewise reduces the likelihood that a given iteration will fail to expand the search tree due to its edge being blocked by an obstacle [@lan2015].

::: procedure
**procedure 6** ($T \leftarrow InsertNode(x_{n},x_{p},T)$). *Adds the node $x_{n} \in X_{free}$ to the tree with $x_{p} \in V$ as the new node's parent, i.e. $V \leftarrow V \cup \{x_{n} \}; E \leftarrow E \cup \{(x_{p},x_{n}) \}$.*
:::

::: procedure
**procedure 7** ($X_{sol} \leftarrow Solution(x_v,T)$). *Finds the path through $T$, $X_{sol} \subset V$, that leads from the root node to $x_v$.*
:::

::: procedure
**procedure 8** ($X_{path} \leftarrow Path(x_{start},x_{end})$). *Builds an ordered set of states that connect the state $x_{start} \in X$ to $x_{end} \in X$ without considering obstacles.*
:::

Note that $Solution$ is used to search the tree while $Path$ is used to search $X$ in an attempt to grow the tree.

::: procedure
**procedure 9** ($bool \leftarrow CollisionFree(X_{path})$). *Returns true if and only if $X_{path}$ is obstacle free, i.e. $X_{path} \subset X_{free}$.*
:::

::: procedure
**procedure 10** ($x_{p} \leftarrow Parent(x_{c},T)$). *Returns the parent node of $x_{c} \in V$ in the tree $T$, or $\varnothing$ if $x_{c}$ is the root node.*
:::

::: procedure
**procedure 11** ($X_{children} \leftarrow Children(x_{p},T)$). *Returns every node from the set $V$ in $T$ that has $x_{p}$ as its parent.*
:::

::: procedure
**procedure 12** ($c_v \leftarrow Cost(x_{v},T)$). *Returns the cost of $x_{v} \in V$. The cost of a vertex is defined as the path length traveled from $x_{r}$ to $x_{v}$ along the tree, i.e. $$\begin{equation*}
    Cost(x_{v},T) = c(Solution(x_{v},T))
\end{equation*}$$*
:::

::: procedure
**procedure 13** ($c_n \leftarrow CostToCome(x_{n},x_{p},T)$). *Calculates the cost of $x_{n} \in X$ if it were connected to the tree through $x_{p} \in V$, returning an infinite cost if the path is not obstacle free. It is defined in Algorithm [\[alg:cost_to_come\]](#alg:cost_to_come){reference-type="ref" reference="alg:cost_to_come"}.*
:::

:::: algorithm
::: algorithmic
$X_{path} \leftarrow Path(x_{p},x_{n})$ []{#alg:cost_to_come:path label="alg:cost_to_come:path"} []{#alg:cost_to_come:collision_check label="alg:cost_to_come:collision_check"} $Cost(x_{p},T) + c(X_{path})$ []{#alg:cost_to_come:cost label="alg:cost_to_come:cost"} $\infty$
:::
::::

## RRT {#section:rrt}

RRT quickly searches $X_{free}$ to find a feasible (not optimal), obstacle free solution and can be used with complex motion primitives while maintaining probabilistic completeness [@nrr]. The RRT algorithm is composed of two main steps that are repeatedly performed until a solution is found. The first is taking a biased sample from $X$. The second is growing the search tree toward the random sample using the $Extend$ procedure. These two procedures are now stated.

::: procedure
**procedure 14** ($x_{rand} \leftarrow Biased\text{-}Sample(i, b_t, X_t)$). *Returns a random point at iteration $i \in \mathbb{Z}_+$ given the sampling bias, $b_t \in \mathbb{Z}_+$, and the target set, $X_t$, as described in Algorithm [\[alg:biased_sampling\]](#alg:biased_sampling){reference-type="ref" reference="alg:biased_sampling"}.*
:::

:::: algorithm
::: algorithmic
$x_{rand} \leftarrow Sample(X_{t})$ $x_{rand} \leftarrow Sample(X)$ $x_{rand}$
:::
::::

The sample is biased towards the target set by selecting the sample from $X_t$ every $b_t$ iterations. $b_t$ is a design parameter affecting exploration and exploitation. A small $b_t$ will attempt to connect the tree to the target set more frequently.

::: procedure
**procedure 15** ($\{x_{n},x_{p},c_n\} \leftarrow Extend(x_{rand},T)$). *Given a sample, $x_{rand} \in X$, and tree, $T = \{V,E\}$, the $Extend$ procedure finds the closest vertex to $x_{rand}$ that is already in $V$ and checks if a valid extension can be made from the tree towards $x_{rand}$, see Algorithm [\[alg:extend\]](#alg:extend){reference-type="ref" reference="alg:extend"}.*
:::

The $Extend$ procedure is illustrated in Figure [5](#fig:extend){reference-type="ref" reference="fig:extend"}. Note that RRT does not make use of the extension cost $c_n$; it is included for use in RRT\*.

:::: algorithm
::: algorithmic
$x_{nearest} \leftarrow Nearest(x_{rand},T)$ []{#alg:extend:nearest label="alg:extend:nearest"} $x_{n} \leftarrow Steer_\eta(x_{nearest},x_{rand})$ []{#alg:extend:steer label="alg:extend:steer"} $c_{n} \leftarrow CostToCome(x_{n},x_{nearest},T)$ []{#alg:extend:collision_check label="alg:extend:collision_check"} $\{x_{n},x_{nearest},c_{n}\}$ []{#alg:extend:return label="alg:extend:return"} $\{\varnothing,\varnothing,\infty\}$
:::
::::

=\[circle,draw=black!100,thick\] =\[circle,draw=red!100, thick\]

:::: {#fig:extend .figure latex-placement="t"}
:::: {#fig:extend:sub1 .figure}
::: caption
The tree before $x_{rand}$ is sampled and Algorithm [\[alg:extend\]](#alg:extend){reference-type="ref" reference="alg:extend"} starts.
:::
::::

:::: {#fig:extend:sub2 .figure}
::: caption
$x_{rand}$ is sampled and node D is found to be the closest node to $x_{rand}$.
:::
::::

:::: {#fig:extend:sub3 .figure}
::: caption
$x_{rand}$ is steered toward node D resulting in the new node, node E.
:::
::::

:::: {#fig:extend:sub4 .figure}
::: caption
After checking for obstacles, node E is added to the tree.
:::
::::

::: caption
An illustration of the $Extend$ procedure.
:::
::::

:::: algorithm
::: algorithmic
$T \leftarrow Initialize(x_{r})$ $x_{rand} \leftarrow Biased\text{-}Sample(i, b_t, X_t)$ $\{x_{n},x_{p},c_n\} \leftarrow Extend(x_{rand},T)$ []{#alg:rrt:extend label="alg:rrt:extend"} $T \leftarrow InsertNode(x_{n},x_{p},T)$ []{#alg:rrt:insert label="alg:rrt:insert"} []{#alg:rrt:if_finished label="alg:rrt:if_finished"} $Solution(x_{n},T)$ []{#alg:rrt:return label="alg:rrt:return"}
:::
::::

The RRT algorithm can now be described. First, a random point is sampled from the configuration space. If the tree can be extended, the new point is added to the tree. If the new point is in the target set then RRT returns a solution, as shown in Algorithm [\[alg:rrt\]](#alg:rrt){reference-type="ref" reference="alg:rrt"}. RRT is known to quickly find solutions for complex problems as it naturally explores unexplored areas of the state space, a property called the Voronoi property [@rrt_connect]. When using the vertices of the tree to create a Voronoi diagram, unexplored regions correspond to larger Voronoi cells. The probability that a Voronoi cell is sampled is proportional to the size of that cell. Thus, the RRT tree naturally extends towards regions that have not yet been explored, avoiding problems with local minima and nonconvex obstacles.

## RRT\* {#section:rrt*}

RRT\* is an extension of RRT that adds probabilistic guarantees for asymptotic optimality to the probabilistic completeness guarantees of RRT [@Karaman2011]. RRT\* does so by performing local optimizations on the edges in the tree whenever a new node is added. As the number of iterations goes to infinity, the repeated local optimization transforms the tree into a set of globally optimal paths from the root node to every reachable point in the obstacle free configuration space.

RRT\* includes two significant changes to RRT, both of which concern the neighborhood set of the node being added to the tree, i.e. $X_{near} = Near_{\rho,\alpha}(x_{n},T)$. The first modification is replacing the $Extend$ procedure with $Extend^*$. As illustrated in Figure [10](#fig:optimal_extend){reference-type="ref" reference="fig:optimal_extend"}, the $Extend^*$ procedure selects a parent from $V$ within a specified distance of the new point that minimizes the cost of the new node.

The second modification happens after $x_{n}$ is added to the tree in a new procedure called $Rewire$. Each node in a local neighborhood is tested to see if its cost would be improved by going through the new node instead of its current parent node. If so, the edges are changed so that $x_n$ becomes the node's new parent as illustrated in Figure [15](#fig:rewire){reference-type="ref" reference="fig:rewire"}.

::: procedure
**procedure 16** ($\{x_{n},x_{p}\} \leftarrow Extend^*(x_{rand},T)$). *Given a tree, $T = \{V,E\}$, the $Extend^*$ procedure finds the best "local" connection for extending the tree in the direction of $x_{rand} \in X$. It returns a new point to be added to the tree, $x_n$, and the parent, $x_p \in V$, as defined in Algorithm [\[alg:optimal_extend\]](#alg:optimal_extend){reference-type="ref" reference="alg:optimal_extend"}.*
:::

:::: algorithm
::: algorithmic
$\{x_{n},x_{p},c_{min}\} \leftarrow Extend(x_{rand},T)$ []{#alg:optimal_extend:extend label="alg:optimal_extend:extend"} []{#alg:optimal_extend:collistion_free label="alg:optimal_extend:collistion_free"} $X_{near} \leftarrow Near_{\rho,\alpha}(x_{n},T)$ []{#alg:optimal_extend:near label="alg:optimal_extend:near"} []{#alg:optimal_extend:it_over_near label="alg:optimal_extend:it_over_near"} $c_{tmp} \leftarrow CostToCome(x_{n},x_{near},T)$ []{#alg:optimal_extend:cost_to_come label="alg:optimal_extend:cost_to_come"} []{#alg:optimal_extend:if_better label="alg:optimal_extend:if_better"} $x_{p} \leftarrow x_{near}$ []{#alg:optimal_extend:update_best_vertex label="alg:optimal_extend:update_best_vertex"} $c_{min} \leftarrow c_{tmp}$ []{#alg:optimal_extend:update_best_cost label="alg:optimal_extend:update_best_cost"} $\{x_{n},x_{p}\}$ []{#alg:optimal_extend:return label="alg:optimal_extend:return"} $\{\varnothing,\varnothing\}$;
:::
::::

=\[circle,draw=black!100,thick\] =\[circle,draw=red!100, thick\] =\[circle,draw=green!100,thick\]

:::: {#fig:optimal_extend .figure latex-placement="t"}
:::: {#fig:optimal_extend:sub1 .figure}
::: caption
Tree after $Extend$ finishes.
:::
::::

:::: {#fig:optimal_extend:sub2 .figure}
::: caption
$x_{n}$'s neighborhood set is found to be node C.
:::
::::

:::: {#fig:optimal_extend:sub3 .figure}
::: caption
Connecting through nodes C and D result in total costs of $6.2$ and $9$ respectively.
:::
::::

:::: {#fig:optimal_extend:sub4 .figure}
::: caption
Because connecting through node C yields a lower total cost, node E is connected to node C.
:::
::::

::: caption
An illustration of the $Extend^*$ procedure.
:::
::::

::: procedure
**procedure 17** ($T \leftarrow Rewire(x_{n},X_{near},T)$). *Given a tree, $T = \{V,E\}$, with node $x_n \in V$ and set $X_{near} \subset V$, $Rewire$ returns a tree with a modified edge set such that $x_n$ is made the parent of elements in $X_{near}$ if it results in a lower cost for the elements of $X_{near}$. It is defined in Algorithm [\[alg:rewire\]](#alg:rewire){reference-type="ref" reference="alg:rewire"}.*
:::

:::: algorithm
::: algorithmic
[]{#alg:rewire:for label="alg:rewire:for"} $c_{near} \leftarrow CostToCome(x_{near},x_{n},T)$ []{#alg:rewire:if_optimal label="alg:rewire:if_optimal"} $x_{p} \leftarrow Parent(x_{near},T)$ []{#alg:rewire:parent label="alg:rewire:parent"} $E \leftarrow \left(E \setminus \{x_{p},x_{near}\} \right) \cup \{x_{n},x_{near}\}$ []{#alg:rewire:rewire label="alg:rewire:rewire"} $T$
:::
::::

=\[circle,draw=black!100,thick\] =\[circle,draw=red!100, thick\] =\[circle,draw=green!100,thick\]

:::: {#fig:rewire .figure latex-placement="t"}
:::: {#fig:rewire:sub1 .figure}
::: caption
The tree after $Extend^*$ adds node G to the tree.
:::
::::

:::: {#fig:rewire:sub2 .figure}
::: caption
Nodes B, E, and F are found to be G's neighborhood set.
:::
::::

:::: {#fig:rewire:sub3 .figure}
::: caption
The original costs of nodes B, E, and F are $3$, $5.9$, and $5.9$ and their potential costs are $5.5$, $4.4$, and $4.5$ respectively.
:::
::::

:::: {#fig:rewire:sub4 .figure}
::: caption
Node B is not rewired because its cost would not be lowered by the operation, however, nodes E and F are rewired.
:::
::::

::: caption
An illustration of the $Rewire$ procedure.
:::
::::

:::: algorithm
::: algorithmic
$T \leftarrow Initialize(x_{r})$ $x_{best} \leftarrow \varnothing$ []{#alg:rrt*:init_x_best label="alg:rrt*:init_x_best"} []{#alg:rrt*:for label="alg:rrt*:for"} $x_{rand} \leftarrow Biased\text{-}Sample(i, b_t, X_t)$ []{#alg:rrt*:end_choose_x_rand label="alg:rrt*:end_choose_x_rand"} $\{x_{n},x_{p}\} \leftarrow Extend^*\!(x_{rand},T)$ []{#alg:rrt*:optimal_extend label="alg:rrt*:optimal_extend"} $T \leftarrow InsertNode(x_{n},x_{p},T)$ $T \leftarrow Rewire(x_{n},Near_{\rho,\alpha}(x_{n},T),T)$ []{#alg:rrt*:rewire label="alg:rrt*:rewire"} $x_{best} \leftarrow x_{n}$ []{#alg:rrt*:store_target label="alg:rrt*:store_target"} $Solution(x_{best},T)$ []{#alg:rrt*:return label="alg:rrt*:return"} $\{\varnothing\}$
:::
::::

The RRT\* algorithm is shown in Algorithm [\[alg:rrt\*\]](#alg:rrt*){reference-type="ref" reference="alg:rrt*"}. Note that RRT and RRT\* are very similar with the main difference being the addition of the $Extend^*$ and $Rewire$ procedures. Additionally, RRT\* runs for a specific number of iterations, $n \in \mathbb{N}_+$, instead of stopping when the first solution is found.

RRT\* is both probabilistically complete and asymptotically optimal [@Karaman2011]. However, RRT\* tends to converge slowly because of the Voronoi property. The Voronoi property helps RRT-based algorithms find valid solutions by encouraging exploration. As the solution improves in RRT\*, the Voronoi regions around the solution get smaller, resulting in a diminishing probability that a given sample will improve the solution [@Akgun2011].

# The Fillet Approach for Local Planning {#section:fillet}

In many cases, planned paths must obey nonholonomic constraints, e.g. [@cui2018; @lan2015; @Lavalle2006]. The $Extend$ and $Path$ procedures can be modified to use basic atomic motions that satisfy such constraints during RRT-based planning, enabling RRT to be used with virtually any set of dynamics. RRT\* variants, however, have no additional benefit if the underlying dynamics or primitive motions do not allow the connection of any two states using a single edge in open space [@Li2016]. The reason being that the $Rewire$ procedure cannot be performed if the nodes in the neighborhood set cannot be exactly connected to each other.

This constraint is detrimental when planning with motion primitives that enforce dynamic path constraints, such as maximum curvature. A common technique for considering maximum curvature constraints is to use Dubin's paths. Dubin's paths connect orientated points with the shortest path while considering maximum curvature constraints [@Lavalle2006]. The issue with using Dubin's paths in a sample-based path planner is that a poor choice in the orientation of the points along the solution can cause a significant increase in path length, as shown in Figure [16](#fig:fillet_vs_dubins){reference-type="ref" reference="fig:fillet_vs_dubins"}. Furthermore, the orientation that minimizes overall path length changes as the solution converges to optimality.

Instead of attempting to connect two oriented points, fillets connect two line segments (defined with three unoriented points) with a curve transitioning smoothly between them, as shown in Figure [17](#fig:general_fillet){reference-type="ref" reference="fig:general_fillet"}. Without the addition of orientation, fillets naturally allow incremental improvements to the solution. The result is a path that is continuous in position and orientation. Additional path qualities may be achieved depending on the choice of fillet. This section will introduce the general fillet concept and requirements for creating a path using fillets. Two fillets are then defined, one using an arc and one using Bézier curves. Section [4](#sec:fillet-rrt-star){reference-type="ref" reference="sec:fillet-rrt-star"} utilizes these fillets as motion primitives in RRT-based algorithms.

:::: {#fig:fillet_vs_dubins .figure latex-placement="t"}
::: caption
Given the set of nodes that start with $x_s$ and end with $x_e$ their respective orientations are denoted with arrows pointing from them. The blue path is the path that is made by the arc-fillet path generation and the red path is the path that is made by Dubin's paths.
:::
::::

## General Fillets {#sec:general_fillets}

Given three input points $x_1,x_2,x_3 \in X$, a fillet connects $x_1$ to $x_3$ with the combination of two straight-line segments and a curve. The line segments constitute portions of the lines $\overline{x_1 x_2}$ and $\overline{x_2x_3}$. The curve intersects line $\overline{x_1x_2}$ at point $x_s$ and line $\overline{x_2x_3}$ at $x_e$. The resulting fillet moves in a straight line from $x_1$ to $x_s$, along the curve from $x_s$ to $x_e$, and then along the straight line from $x_e$ to $x_3$, as depicted in Figure [17](#fig:general_fillet){reference-type="ref" reference="fig:general_fillet"}. The major differentiator between the different fillets is the definition of the curve portion, which affects the placement of $x_s$ and $x_e$.

This work assumes symmetric fillets, resulting in an equivalent distance between the node that the fillet is centered at and the two ends of the fillet curve, $x_s$ and $x_e$. This distance is a function of the fillet curve type as well as the change in orientation between $\overrightarrow{x_1x_2}$ and $\overrightarrow{x_2x_3}$.

The position along the fillet can be described using a spatial index $s$. Allow $s_0$ to be where the fillet meets $x_1$, $s_1$ to be the index where the fillet's curve begins, $s_2$ to be the index of where the fillet's curve ends, and $s_3$ to be the index of where the fillet reaches $x_3$. Allow $\Psi(s)$ to be the fillet's curve such that $\Psi(0) = x_s$ and $\Psi(s_2-s_1) = x_e$. Also, define the unit vector from $x_i$ to $x_j$ as $u_{ij}$ (see Table [\[tab:notation\]](#tab:notation){reference-type="ref" reference="tab:notation"}). The position along the fillet can be written in a piecewise form as $$\begin{equation}
\label{eq:fillet_equation}
x(s) = \begin{cases}
	x_1 + s u_{12}      & s_0 \leq s \leq s_1 \\
	\Psi(s-s_1)         & s_1 <    s \leq s_2 \\
	x_e + (s-s_2)u_{23} & s_2 <    s \leq s_3
\end{cases}.
\end{equation}$$

Defining $\gamma_i \in [0,\pi)$ as the angle measured from $\overrightarrow{x_{i-1}x_i}$ to $\overrightarrow{x_i x_{i+1}}$, the fillet distance for $x_1,x_2,x_3$ can be defined as $d(\gamma_2) = \left\|x_s-x_2\right\| = \left\|x_e-x_2\right\|$. Once $d(\gamma_2)$ is found, the start and end points of the curve can be written as $$\begin{equation}
\label{eq:start_end_arc}
\begin{split}
x_s &= x_2 + d(\gamma_2) u_{21} \\
x_e &= x_2 + d(\gamma_2) u_{23}
\end{split}.
\end{equation}$$

## Fillet Paths

A smooth path to a destination node can be created using a sequence of points where fillets are formed from point triplets and then combined, as shown in Figure [17](#fig:general_fillet){reference-type="ref" reference="fig:general_fillet"}. Without loss of generality, it is assumed that the path starts at node $1$ and moves to node $n$ using the sequence $x_1, x_2, ..., x_n$. The path is thus made from $n$ nodes, using $n-2$ fillets to arrive at $x_n$. There are two major concerns when formulating the path. The first is the path continuity; not every sequence of points can be combined using fillets to create a continuous path. The second major consideration is path length; the $Extend^*$ and $Rewire$ procedures depend upon path length for local optimizations.

### Path Continuity {#path-continuity .unnumbered}

The first key to using the fillets for planning purposes is to ensure that the path resulting from joining multiple fillets is continuous. There are two conditions to ensure feasibility: one to ensure that the fillet curve ends before the final point in the fillet and one condition to ensure that all fillets end before the next one begins. Assuming $x_i$ is the middle node, these conditions can be expressed as $$\begin{equation}
  \label{equ:conditions}
    \begin{split}
      d(\gamma_i)                   &\leq \| x_i - x_{i+1} \| \\
      d(\gamma_{i-1}) + d(\gamma_i) &\leq \| x_i - x_{i-1} \|
    \end{split}.
\end{equation}$$

:::: {#fig:general_fillet .figure latex-placement="t"}
::: caption
The fillet generated to connect $x_2$ and $x_4$ is shown in blue with the fillet that comes before it shown in red. Note that $d(\gamma_2) + d(\gamma_3) \leq \left\|x_2-x_3\right\|$, providing a continuous path.
:::
::::

### Length of Fillet Paths {#length-of-fillet-paths .unnumbered}

In RRT\*'s $Extend^*$ and $Rewire$ procedures, local optimizations are made to the search tree to find the shortest path. These procedures are defined for straight-line paths where the path length can be calculated as the distance between nodes in the path. This is not the case for paths created from fillets. Thus, the path length to a particular node and the length relation to other nodes are now evaluated.

Each fillet consists of two line segments and a fillet curve. The length of a single fillet with $x_i$ as the middle node of the fillet can be expressed as $$\begin{equation}
  \label{eq:fillet_definition}
	\mathop{\mathrm{\mathcal{F}}}_i = b_{i} + \Psi_i + e_{i}
\end{equation}$$ where $b_{i}$, $\Psi_i$, and $e_{i}$ are the beginning component length, the curve length, and the end component length (see Figure [17](#fig:general_fillet){reference-type="ref" reference="fig:general_fillet"}). Given [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}, the two straight-line lengths can be expressed as $$\begin{equation}
  \label{eq:b_e}
  \begin{split}
    b_i &= \left\|x_{i-1} - x_{i}\right\| - d(\gamma_i) \\
    e_i &= \left\|x_{i+1} - x_i\right\|   - d(\gamma_i)
  \end{split}.
\end{equation}$$ This definition of fillet length allows for the expression of a recursive relationship for calculating the path length in the following lemma.

::: {#lem:recursive_length .lemma}
**Lemma 1**. *Assume an ordered sequence of nodes is used to create a path using fillets with [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} satisfied for every intermediate node. Given a resulting path length of $c_i$ to arrive at node $x_i$, $i \geq 3$, the path length to arrive at node $x_{i+1}$ can be expressed as $$\begin{equation}
    \label{eq:recursive_fillet_length}
    c_{i+1} = c_i + \mathop{\mathrm{\mathcal{F}}}_i - \left\|x_i - x_{i-1}\right\|.
\end{equation}$$*
:::

::: proof
*Proof.* The path length to node $x_i$ along a sequence of curves and lines can be written as a summation of individual parts. The path to $x_i$ contains $i-2$ curves of length $\Psi_2$ through $\Psi_{i-1}$. Let $m_{j,j+1}$ be the length of the straight-line segment that connects curve $j$ to curve $j+1$, i.e. $$\begin{equation}
    \label{eq:m}
    m_{j,j+1} = \left\|x_j - x_{j+1}\right\| - d(\gamma_j) - d(\gamma_{j+1}),
\end{equation}$$ which is positive assuming [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} is satisfied for all fillets. The length of the path to arrive at $x_i$ is $$\begin{equation}
    \label{eq:summed_length}
    c_i = b_2 + \sum_{k=2}^{i-1}\Psi_k + \sum_{k=2}^{i-2}m_{k,k+1} + e_{i-1}.
\end{equation}$$ Note that the path connecting to node $x_{i+1}$ could be expressed similarly with a length of $$\begin{equation*}
    c_{i+1} = b_2 + \sum_{k=2}^{i}\Psi_k + \sum_{k=2}^{i-1}m_{k,k+1} + e_{i},
\end{equation*}$$ which can be written in terms of $c_i$ as $$\begin{equation}
    \label{eq:c_i+1}
    c_{i+1} = c_i + \Psi_i + m_{i-1,i} + e_{i} - e_{i-1}.
\end{equation}$$ Given [\[eq:b_e\]](#eq:b_e){reference-type="eqref" reference="eq:b_e"} and [\[eq:m\]](#eq:m){reference-type="eqref" reference="eq:m"}, [\[eq:c_i+1\]](#eq:c_i+1){reference-type="eqref" reference="eq:c_i+1"} becomes $$\begin{equation}
    \label{eq:c_plus_1}
    c_{i+1} = c_i + b_i + \Psi_i + e_{i} - \left\|x_i - x_{i-1}\right\|.
\end{equation}$$ Given the definition of $\mathop{\mathrm{\mathcal{F}}}_i$ in [\[eq:fillet_definition\]](#eq:fillet_definition){reference-type="eqref" reference="eq:fillet_definition"}, [\[eq:c_plus_1\]](#eq:c_plus_1){reference-type="eqref" reference="eq:c_plus_1"} simplifies to [\[eq:recursive_fillet_length\]](#eq:recursive_fillet_length){reference-type="eqref" reference="eq:recursive_fillet_length"}. ◻
:::

A few properties can now be stated using the recursive relationship in Lemma [1](#lem:recursive_length){reference-type="ref" reference="lem:recursive_length"}, beginning with the relationship between the path length to a node and the path length to one of its descendants.

::: {#cor:no_descendant .corollary}
**Corollary 1**. *The path length to a node is not dependent upon the choice of any nodes that come after it.*
:::

::: proof
*Proof.* This can be seen by examining the summation form of the path length in [\[eq:summed_length\]](#eq:summed_length){reference-type="eqref" reference="eq:summed_length"} and noting that none of the variables depend upon any node after node $x_i$. ◻
:::

The recursive path length calculation using fillets depends on the parent as well as the grandparent node. This is different from the straight-line motion primitive where the path length to a node can be calculated using knowledge of solely the parent node. This leads to the following lemma about path length, which has significant implications for rewiring a tree connected with fillets.

::: {#lem:rewiring_tests .lemma}
**Lemma 2**. *Given a node $x_i$ with a child node $x_{i+1}$ and multiple possible parent nodes, choosing the parent for $x_i$ to minimize $c_i$ [*will not*]{.underline} necessarily result in the smallest possible value for $c_{i+1}$.*
:::

::: proof
*Proof.* The proof is given through a simple example where the shorter path to $x_i$ results in a longer path to $x_{i+1}$. Consider Figure [18](#fig:connection_alternatives){reference-type="ref" reference="fig:connection_alternatives"}. Let the path from $x_r$ to $x_6$ have the same length as the path from $x_r$ to $x_1$ and the same be true of $x_5$ and $x_2$, i.e. $$\begin{equation*}
    \begin{split}
      Cost\left(x_1,T\right) = Cost\left(x_6,T\right) \\
      Cost\left(x_2,T\right) = Cost\left(x_5,T\right)
    \end{split}.
\end{equation*}$$ Path A, shown in red, is the shortest path to $x_3$ with a path length of $1.9$. Path A also results in a path length to $x_4$ of $2.9$. On path B, shown in blue, let the fillet that connects $x_5$ to $x_4$ be an arc-fillet with $r = 0.5$, $d(\pi/2) = 1/2$, and a resulting arc length of $\pi/4$. Starting at $x_6$ and following path B results in a path length to $x_3$ of $2$, which is greater than the path length to get to $x_3$ on path A. To minimize the path length to $x_3$ path A is chosen. However, the length of the path from $x_6$ to $x_4$ is $1 + 1/2 + \pi/4 + 1/2 \approx 2.785$. Thus, minimizing path length to $x_3$ does not minimize path length to $x_4$. ◻
:::

:::: {#fig:connection_alternatives .figure latex-placement="t"}
::: caption
Let $c_{base} = Cost(x_1,T) = Cost(x_6,T)$ and $Cost(x_2,T) = Cost(x_5,T)$. Path A, shown in red, yields a shorter path length for $x_3$ than path B, shown in blue. However, path B yields a shorter path length to $x_4$ than path A.
:::
::::

Therefore, in a $Rewire$ procedure, it is not sufficient to solely check the path to the node being rewired, but the path lengths to descendants must also be evaluated. As the tree grows larger, checking all descendants would be overly cumbersome. The following corollary establishes that the only descendants that need to be checked are the children nodes.

::: {#cor:unchanged .corollary}
**Corollary 2**. *If a node's parent and grandparent remain unchanged, but the tree is rewired such that the cost of the node's parent is lowered, then the cost of the node will be lowered by the same amount as its parent.*
:::

::: proof
*Proof.* If a node's parent and grandparent remain the same then an examination of [\[eq:recursive_fillet_length\]](#eq:recursive_fillet_length){reference-type="eqref" reference="eq:recursive_fillet_length"} shows that the only portion of its path length that will change is the length to the parent's node, $c_i$, since both $\mathop{\mathrm{\mathcal{F}}}_i$ and $\left\|x_i - x_{i-1}\right\|$ remain unchanged. Thus, the same change in cost seen by a parent will be reflected in the cost of the node in question if the grandparent node remains unchanged. ◻
:::

## The Arc Fillet {#ssec:arc_fillet}

The arc-fillet formulates the curve portion of the fillet using a circle of radius $r \in \mathbb{R}_+$ that is tangential to the two line segments at $x_s$ and $x_e$, see Figure [19](#fig:arc_fillet){reference-type="ref" reference="fig:arc_fillet"}. To respect curvature constraints, the radius can be chosen as the inverse of the maximum curvature, i.e. $r = 1/\kappa_{max}$. The distance between the curve intersection points and the intermediary point of the fillet is expressed in the following Lemma:

::: lemma
**Lemma 3**. *The arc-fillet distance, $d(\gamma)$, for a circular curve of radius $r$ is $$\begin{equation}
  \label{eq:d_gamma_arc}
  d(\gamma) = \frac{r\bigl(1 - \cos(\gamma)\bigr)}{\sin(\gamma)}.
\end{equation}$$*
:::

::: proof
*Proof.* Assume that the coordinate frame $f$ is defined such that $x_s$ is at the origin and the $x$-axis is pointing along $\overrightarrow{x_1x_2}$. Using the pre-subscript $f$ to denote a point expressed in frame $f$ then ${_fx_s} = \begin{bmatrix} 0 & 0 \end{bmatrix}^T$. As $d(\gamma)$ represents the distance along $\overline{x_1x_2}$ from $x_s$ to $x_2$, the value of $x_2$ in frame $f$ is $$\begin{equation}
    \label{eq:f_x_2}
    {_fx_2} = \begin{bmatrix}
      d(\gamma) \\
      0
    \end{bmatrix}.
\end{equation}$$ As the orientation of the path must be tangential to the circle at $x_s$ for continuity, the center point of the circle will lie upon the $y$-axis at a distance $r$ from $x_s$, i.e., $$\begin{equation*}
    {_fx_c} = \begin{bmatrix}
      0 \\
      r \zeta
    \end{bmatrix}\mbox{, } \zeta \in \{-1, 1\},
\end{equation*}$$ where $\zeta = 1$ corresponds to a counter-clockwise arc and $\zeta =-1$ to a clockwise arc. Parameterizing the arc by its tangent angle, the arc can be expressed in frame $f$ as $$\begin{equation*}
    {_f\Psi_{arc}}(\theta) =
      r
      \begin{bmatrix}
        \sin(\theta) \\
        \zeta \left(1 - \cos(\theta)\right)
      \end{bmatrix}
\end{equation*}$$ where ${_fx_s} = {_f\Psi_{arc}}(0)$. The parameter $\theta \in [0,\gamma)$ represents the orientation of the path in frame $f$. The tangent of ${_f\Psi_{arc}}\left(\gamma\right)$ should be parallel to $\overline{x_2x_3}$. The task is to solve for $d(\gamma)$ such that ${_fx_e} = {_f\Psi_{arc}}(\gamma)$.

The unit vector from ${_fx_3}$ to ${_fx_2}$ can be written in terms of $\gamma$ as $-\begin{bmatrix} \cos(\gamma) & \sin(\gamma) \end{bmatrix}^T$. The point ${_fx_2}$ can be expressed as a combination of this unit vector and ${_fx_e}$ as $$\begin{equation}
  \label{eq:x_2_version2}
  \begin{split}
    {_fx_2} &= {_fx_e} - d(\gamma)
      \begin{bmatrix}
        \cos(\gamma) \\
        \sin(\gamma)
      \end{bmatrix} \\
    &=
      r
      \begin{bmatrix}
        \sin(\gamma) \\
        \zeta \left(1-\cos(\gamma)\right)
      \end{bmatrix}
    - d(\gamma)
      \begin{bmatrix}
        \cos(\gamma) \\
        \sin(\gamma)
      \end{bmatrix}
  \end{split}
\end{equation}$$ Equation [\[eq:d_gamma_arc\]](#eq:d_gamma_arc){reference-type="eqref" reference="eq:d_gamma_arc"} is found by setting [\[eq:f_x_2\]](#eq:f_x_2){reference-type="eqref" reference="eq:f_x_2"} equal to [\[eq:x_2_version2\]](#eq:x_2_version2){reference-type="eqref" reference="eq:x_2_version2"} and solving for $d(\gamma)$. ◻
:::

::: remark
**Remark 1**. *It is important to note the singularities of $d(\gamma)$ and their corresponding significance. A change of direction of $\gamma=0$ corresponds to executing a straight line. A value of $\gamma = \pm \pi$ would correspond to reversing direction.*
:::

One advantage of the arc-fillet is that the fillet curve can be directly expressed using the spatial index $s$. The orientation of $\overrightarrow{x_1x_2}$ can be written as $$\psi = atan2(u_{12, 2}, u_{12,1}).$$ The point along the fillet curve can then be expressed in the inertial frame as $$\begin{align}
  \label{eq:arc_equation}
  \Psi_{arc}(s) &= R(\psi) \cdot {_f\Psi_{arc}}\left(\frac{s}{r}\right) + x_s\mbox{,} &
  R(\psi) &=
    \begin{bmatrix}
      \cos(\psi) & -\sin(\psi) \\
      \sin(\psi) & \cos(\psi)
    \end{bmatrix}\mbox{,}
\end{align}$$ where $\theta$ has been replaced with $\frac{s}{r}$ as the arc-length of a circle is $s = \theta r$. Note that $\Psi(0) = x_s$ and $\Psi(\gamma r) = x_e$, as expected.

Finally, the spatial switching indices from [\[eq:fillet_equation\]](#eq:fillet_equation){reference-type="eqref" reference="eq:fillet_equation"} are $$\begin{equation*}
\begin{split}
	s_1 &= s_0 + \left\|x_s - x_1\right\| \\
	s_2 &= s_1 + \gamma r \\
	s_3 &= s_2 + \left\|x_3 - x_e\right\|
\end{split}.
\end{equation*}$$

:::: {#fig:arc_fillet .figure latex-placement="t"}
::: caption
The arc-fillet generated to connect $x_1$ and $x_3$.
:::
::::

The development of the arc-fillet enables a definition of a new procedure for creating a path between three points:

::: procedure
**procedure 18** ($X_{fillet} \leftarrow ArcFillet\left(x_0,x_1,x_2,x_3\right)$). *The $ArcFillet$ procedure uses [\[eq:start_end_arc\]](#eq:start_end_arc){reference-type="eqref" reference="eq:start_end_arc"}, [\[eq:d_gamma_arc\]](#eq:d_gamma_arc){reference-type="eqref" reference="eq:d_gamma_arc"}, and [\[eq:arc_equation\]](#eq:arc_equation){reference-type="eqref" reference="eq:arc_equation"} to make an arc that connects $\overline{x_1x_2}$ to $\overline{x_2x_3}$. Feasibility checks are made with respect to the arc that connects $\overline{x_0x_1}$ to $\overline{x_1x_2}$ using [\[eq:d_gamma_arc\]](#eq:d_gamma_arc){reference-type="eqref" reference="eq:d_gamma_arc"} to define $d(\gamma)$ in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}. If the checks fail the null path is returned.*
:::

::: remark
**Remark 2**. *The arc-fillet is made from straight-line segments and arcs assuming forward motion as is a Dubin's path. As a result, a path made using arc-fillets will have the same continuity properties as a Dubin's path, i.e. $\mathcal{C}^{1}$ in position and orientation with curvature assuming instantaneous changes between zero and maximum curvature [@Lavalle2006].*
:::

## The Bézier Fillet {#section:bezier_curve_gen}

The arc-fillet assumes an instantaneous change in curvature which may be inappropriate for some scenarios that require higher levels of smoothness. In this section, Bézier curves are used to generate the fillet, resulting in paths that are $\mathcal{C}^{2}$ continuous in position and orientation, and $\mathcal{C}^{1}$ continuous in curvature. A detailed description of the curve is left to [@Yang2014] and the references therein. The definition of the curve is shown as follows for the sake of completeness.

A Bézier curve connects two points and is defined as, $$\begin{equation}
  \label{equ:bezier_curve}
  P_n(\tau) = \sum^{n}_{i=0} p_i B_{n,i}(\tau),
\end{equation}$$ where $p_i \in \mathbb{R}^2$ are control points, $n \in \mathbb{Z}_+$ is the degree of the polynomial, $\tau$ is a path parameterization index such that $0 \leq \tau \leq 1$, $P_n(0) = p_0$, and $P_n(1) = p_n$. Note that there is no direct relationship between changes in $\tau$ and path length [@Gravesen1997]. The functions $B_{n,i}(\tau)$ are Berstein polynomials defined as $$\begin{equation}
  \label{equ:berstein_polynomials}
  B_{n,i}(\tau) = \binom{i}{n} \tau^i (1 - \tau)^{n-i}.
\end{equation}$$

:::: {#fig:bezier_curve .figure latex-placement="t"}
::: caption
The fillet generated to connect $x_1$ and $x_3$. Note that sets $_0p_i$ and $_1p_i$ are control points that replace $p_i$ in [\[equ:bezier_curve\]](#equ:bezier_curve){reference-type="eqref" reference="equ:bezier_curve"} and in analogy to Figure [19](#fig:arc_fillet){reference-type="ref" reference="fig:arc_fillet"}, $_0p_0 = x_s$ and $_1p_0 = x_e$.
:::
::::

[@Yang2014] combines two cubic Bézier curves to generate the curve of the fillet. In Figure [20](#fig:bezier_curve){reference-type="ref" reference="fig:bezier_curve"}, the curves are denoted as $_0P$ and $_1P$ with the connecting lines denoted as $b_2$ and $e_2$. The fillet distance can now be stated.

::: lemma
**Lemma 4**. *The distance between the intermediary point, $x_2$, and the curve's start and end points can be expressed as $$\begin{equation}
    \label{equ:d_gamma}
    d(\gamma) = \frac{\nu_4 \sin\left(\frac{\gamma}{2}\right)}{\kappa_{max} \cos^2\left(\frac{\gamma}{2}\right)},
\end{equation}$$ where $$\begin{equation*}
  \begin{tabular}{c c c c}
    $\nu_1 = 7.2364$ & $\nu_2 = \frac{2}{5}\left(\sqrt{6} - 1\right)$ & $\nu_3 = \frac{\nu_2 + 4}{\nu_1 + 6}$ & $\nu_4 = \frac{\left(\nu_2 + 4\right)^2}{54 \nu_3}$
  \end{tabular}.
\end{equation*}$$*
:::

::: proof
*Proof.* See Section 2.1 of [@Yang2014]. ◻
:::

To define the fillet curve, four control points are needed for each of the two Bézier curves. The control points for $_0P$ and $_1P$ are denoted as $_0p_i$ and $_1p_i$, respectively, and can be expressed as $$\begin{equation}
  \begin{tabular}{l l}
    $_0p_0 = \;x_2     + d \cdot u_{12}$ & $_1p_0 = \;x_2     + d \cdot u_{32}$ \\
    $_0p_1 = {_0p_0} - g \cdot u_{12}$ & $_1p_1 = {_1p_0} - g \cdot u_{32}$ \\
    $_0p_2 = {_0p_1} - h \cdot u_{12}$ & $_1p_2 = {_1p_1} - h \cdot u_{32}$ \\
    $_0p_3 = {_0p_2} + k \cdot u_d$    & $_1p_3 = {_1p_2} - k \cdot u_d$
  \end{tabular},
\end{equation}$$ where $u_d$ is the unit vector pointing from ${_0p_2}$ to ${_1p_2}$ and the weights, $h$, $g$, and $k$ are defined as $$\begin{equation}
\begin{tabular}{c c c}
  $h = \nu_3 d$ & $g = \nu_2 \nu_3 d$ & $k = \frac{6 \nu_3 \cos\left(\frac{\gamma}{2}\right)}{\nu_2 + 4}d$
\end{tabular}.
\end{equation}$$

A procedure that differs from what is found in [@Yang2014] is now defined to generate curves. In [@Yang2014], a maximum curve angle, $\gamma_{max}$, is employed with an associated distance $d_{min} = d(\gamma_{max})$. To ensure subsequent fillet curves do not overlap, connecting points are forced to be $2d_{min}$ apart. We found the $2d_{min}$ node separation to be overly restrictive as small path refinements are not allowed under such a constraint. These small path refinements prove necessary, especially around curves in the obstacles. This limitation significantly reduces the ability to rewire, during which small refinements to the tree are common.

The underlying desired constraint enforced with the $2d_{min}$ spacing is path continuity. The conditions in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} give the path generation process more flexibility. An example is given in Figure [21](#fig:spline_reach){reference-type="ref" reference="fig:spline_reach"} showing the points that could be considered under both the conditions in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} and under a $\gamma_{max}$ and $2d_{min}$ constraint. The curve generating procedure can now be stated.

::: procedure
**procedure 19** ($X_{fillet} \leftarrow BezierFillet(x_0,x_1,x_2,x_3)$). *$BezierFillet$ uses the cubic Bézier spline to generate a $\mathcal{C}^{2}$ continuous curve from $x_1$ to $x_3$ using [\[equ:bezier_curve\]](#equ:bezier_curve){reference-type="eqref" reference="equ:bezier_curve"} through [\[equ:d_gamma\]](#equ:d_gamma){reference-type="eqref" reference="equ:d_gamma"}. Feasibility checks are made with respect to the curve that starts at $x_0$ and goes to $x_2$ as is described by the combination of [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} and [\[equ:d_gamma\]](#equ:d_gamma){reference-type="eqref" reference="equ:d_gamma"}. If the checks fail the null path is returned.*
:::

## A Comparison of Arc and Bézier Fillets

Arc and Bézier fillets provide different advantages and disadvantages. A big advantage of the arc-fillet is its simplicity and speed. As can be seen in Table [1](#fig:edge_benchmark){reference-type="ref" reference="fig:edge_benchmark"}, an arc-fillet can be generated in about half the time it takes to make a Bézier-fillet. Another benefit of the arc-fillet is that it is less constrained than the Bézier-fillet, resulting in a larger reachability set for connecting points, as shown in Figure [22](#fig:fillet_reach){reference-type="ref" reference="fig:fillet_reach"}. This fact is critical to RRT because it directly affects exploration and convergence.

::: {#fig:edge_benchmark}
   Motion Primitive      Length ($m$)        Computation Time ($\mu s$)
  ------------------ -------------------- ---------------------------------
    Straight-line     $20.845 \pm 7.417$   $\,\,\, 3.371 \pm \,\,\, 1.542$
     Dubin's path     $23.797 \pm 7.729$      $19.087 \pm \,\,\, 8.670$
      Arc-fillet      $18.838 \pm 6.811$   $\,\,\, 7.965 \pm \,\,\, 2.762$
    Bézier-fillet     $18.909 \pm 6.242$         $15.568 \pm 12.517$

  : Three points, $x_1,x_2,x_3$, were randomly sampled 1 million times with each $x,y$ component bounded between 0 and 10 at each sample. For Dubin's paths, the orientation of a point was set to be tangential to the vector pointing to it from its parent. The average length of the resulting paths and time it took to find them is presented with their respective standard deviations.
:::

:::::: {#fig:reachability .figure latex-placement="ht"}
::: raggedright
:::: {#fig:spline_reach .figure}
::: caption
Comparison of the constraints in [@Yang2014] to those found in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} for Bézier curve fillets. The red shows the area that both sets of feasibility conditions deem invalid for $x_3$. The yellow is area that only [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} deems valid. The green is area that both sets of conditions deem valid.
:::
::::
:::

::: raggedleft
:::: {#fig:fillet_reach .figure}
::: caption
Visualizes the reachability regions of the arc-fillet and Bézier-fillet generation. The red shows the area that both fillets cannot reach. The yellow is area that arc-fillets can reach but Bézier-fillets cannot. The green is area that both fillets can reach.
:::
::::
:::

::: caption
Comparisons of different constraints on the position of $x_3$ if a fillet was made starting from $x_1$ through $x_2$ and to $x_3$. On the left, the constraints in [@Yang2014] are compared to those found in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} for the Bézier curve fillets. On the right, the difference in the definition of $d(\gamma)$ between arc-fillets and Bézier-fillets is expressed in terms of where [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} is satisfied. Both figures assume $x_1$ is at the origin, $x_2 = \protect\begin{bmatrix} 0 & 3 \protect\end{bmatrix}^T$, $\kappa_{max} = 2m^{-1}$, $d(\gamma_1) = 0$, $d_{min} = 1.5m$, and $\gamma_{max} = 0.624\pi$ radians.
:::
::::::

The major advantage of the Bézier-fillet is the smoothness of the resulting path. The arc-fillet, like Dubin's paths, guarantees only $\mathcal{C}^{1}$ continuity of pose. The Bézir-fillet guaranties $\mathcal{C}^{2}$ continuity of pose and $\mathcal{C}^{1}$ continuity of curvature, as is shown in Figure [24](#fig:fillet_curvature){reference-type="ref" reference="fig:fillet_curvature"}.

:::: {#fig:fillet_curvature .figure latex-placement="ht"}
:::: figure
::: caption
Fillets generated between the points $\begin{bmatrix} -2 & 0 \end{bmatrix}^T$, $\begin{bmatrix} 5 & 0 \end{bmatrix}^T$, and $\begin{bmatrix} -1 & 4 \end{bmatrix}^T$.
:::
::::

:::: figure
::: caption
The curvature of each fillet over the fillet curve.
:::
::::

:::: figure
::: caption
The first derivative of the curvature of each fillet type.
:::
::::

::: caption
An example of the arc and Bézier fillets with the corresponding curvature and curvature rate. The arc-fillet is shown in blue and the Bézier-fillet is shown in red. Note that the arc has zero curvature change as there is an instantaneous jump from zero to maximum curvature.
:::
::::

# Fillet-based RRT\* {#sec:fillet-rrt-star}

Fillet-based variants of the RRT and RRT\* algorithms are proposed in this section. The overall structure of the fillet-based variants is the same as their standard counterparts. This section will only cover the procedures that change, namely: $Initialize$, $CostToCome$, $Extend$, $Extend^*\!$, and $Rewire$. To construct the fillet-based variants, each of these procedures is redefined with a procedure of the same name but with the prefix "$FB$", i.e. $Extend$ becomes $FB\text{-}Extend$. The first four procedures have small changes to their standard counterparts and are presented first. The $FB\text{-}Rewire$ procedure is then discussed in detail. This section ends with a discussion of FB-RRT\*'s advantages. The FB-RRT\* algorithm is not presented until Section [5](#section:improving_convergence){reference-type="ref" reference="section:improving_convergence"} where a modified sampling procedure is discussed.

## Procedures with Minor Changes {#sec:procedures_with_minor_changes}

The first procedure to be modified is the $Initialize$ procedure. As defined, the $Initialize$ procedure has no consideration of the vehicle orientation, which must be respected to generate an executable path for the vehicle. $FB\text{-}Initialize$ differs from $Initialize$ in that it initializes the search tree to have an edge of length $d_{init} \in \mathbb{R}_+$ extending from the root, $x_{r}$, to a point in the direction of the initial orientation of the robot, $\psi_{r} \in [-\pi,\pi)$. Recall that connecting to a new point using a fillet requires both a parent and a grandparent node. If $x_{r}$ is returned from $Nearest$ or $Near$ any attempt to make an edge with $x_{r}$ is ignored as it has no parent, ensuring that the starting orientation is respected[^2]. The new initialization procedure is defined as follows.

::: procedure
**procedure 20** ($T \leftarrow FB\text{-}Initialize_{d_{init}}(x_{r},\psi_{r})$). *Returns a tree with two nodes and an edge of length $d_{init}$ based on the root node, $x_r$, and initial orientation, $\psi_r$, as defined in Algorithm [\[alg:fb_initialize\]](#alg:fb_initialize){reference-type="ref" reference="alg:fb_initialize"}.*
:::

:::: algorithm
::: algorithmic
$x_{n} \leftarrow x_{r} + d_{init} \begin{bmatrix} \cos\left(\psi_{r}\right) & \sin\left(\psi_{r}\right) \end{bmatrix}^T$ $V \leftarrow \{x_{r},x_n\}$ $E \leftarrow \{(x_{r},x_n)\}$ $T \leftarrow \{V,E\}$ $T$
:::
::::

The $CostToCome$ procedure is redefined to accommodate the new fillet-based path generation. Recalling Lemma [1](#lem:recursive_length){reference-type="ref" reference="lem:recursive_length"}, this depends upon both the parent and grandparent nodes of the node in question. The new procedure is given as follows.

::: procedure
**procedure 21** ($c_{n} \leftarrow FB\text{-}CostToCome(x_{n},x_{p},x_{gp},T)$). *Calculates the cost of $x_{n}$ if it is connected to the tree, T, through the parent, $x_{p}$, and the grandparent, $x_{gp}$, as in Algorithm [\[alg:fillet_cost_to_come\]](#alg:fillet_cost_to_come){reference-type="ref" reference="alg:fillet_cost_to_come"}. Note that the $Fillet$ procedure in Algorithm [\[alg:fillet_cost_to_come\]](#alg:fillet_cost_to_come){reference-type="ref" reference="alg:fillet_cost_to_come"} can be replaced by $ArcFillet$ or $BezierFillet$ depending upon the fillet being used.*
:::

:::: algorithm
::: algorithmic
$X_{fillet} \leftarrow Fillet({Parent(x_{gp},T)},x_{gp},x_{p},x_{n})$ $Cost(x_{p},T) + c(X_{fillet}) - \left\|x_p - x_{gp}\right\|$ $\infty$
:::
::::

The $Extend$ procedure is updated in two substantial ways. The first is the use of $FB\text{-}CostToCome$. The second is the use of a "node orientation" when performing the nearest neighbor search. By incorporating a sense of "node orientation", infeasible sharp turns can be avoided in the nearest neighbor searching. There is no actual "orientation" of a node as the nodes are 2D points that guide the creation of the path. However, we can bias the nearest neighbor search to penalize turns by noting that a fillet ending at a node will be oriented with the line extending from the node's parent to the node. After the fillet curve has been executed, the robot will be aligned with that orientation. Given node $x_i$ and its parent $x_{i-1}$, the orientation of $x_i$ is defined as $\psi_i = atan2(u_{i-1\mbox{ }i,2},u_{i-1\mbox{ }i,1})$. The nearest neighbor search is performed over $\begin{bmatrix} x_{i,1} & x_{i,2} & \cos(\psi_i) & \sin(\psi_i) \end{bmatrix}^T$ instead of $\begin{bmatrix} x_{i,1} & x_{i,2} \end{bmatrix}^T$. The inclusion of a pseudo "node orientation" combined with the relaxed continuity constraints, depicted in Figure [21](#fig:spline_reach){reference-type="ref" reference="fig:spline_reach"}, enables us to forgo the $k$-nearest-neighbor search that [@{spline_rrt*}] uses to aid in the success of $Extend$. The updated procedure is now defined.

::: procedure
**procedure 22** ($\{x_{n},x_{p},c_n\} \leftarrow FB\text{-}Extend(x_{rand},T)$). *Given $x_{rand} \in X$ and a tree $T$, the $FB\text{-}Extend$ procedure finds the closest vertex to $x_{rand}$ in terms of a combined position and orientation metric and attempts to extend the tree in the direction of $x_{rand}$, as defined in Algorithm [\[alg:fillet_extend\]](#alg:fillet_extend){reference-type="ref" reference="alg:fillet_extend"}.*
:::

:::: algorithm
::: algorithmic
$x_{nearest} \leftarrow Nearest(x_{rand},T)$ $x_{n} \leftarrow Steer_\eta(x_{nearest},x_{rand})$ $x_{gp} \leftarrow Parent(x_{nearest},T)$ $c_{n} \leftarrow$ $FB\text{-}CostToCome(x_{n},x_{nearest},x_{gp},T)$ $\{x_{n},x_{nearest},c_{n}\}$ $\{\varnothing,\varnothing,\inf\}$
:::
::::

The $FB\text{-}Extend^*$ procedure is identical to $Extend^*$ except for the use of $FB\text{-}Extend$ and $FB\text{-}CostToCome$. The $FB\text{-}Extend$ and $FB\text{-}Extend^*$ procedures are illustrated in Figure [31](#fig:fillet_extend){reference-type="ref" reference="fig:fillet_extend"}. Note that the numbers shown in Figure [31](#fig:fillet_extend){reference-type="ref" reference="fig:fillet_extend"} are the edge costs of the edges they are near. The same is true of Figures [5](#fig:extend){reference-type="ref" reference="fig:extend"}, [10](#fig:optimal_extend){reference-type="ref" reference="fig:optimal_extend"}, and [15](#fig:rewire){reference-type="ref" reference="fig:rewire"} except Figure [31](#fig:fillet_extend){reference-type="ref" reference="fig:fillet_extend"} uses the fillet cost calculation described in Lemma [1](#lem:recursive_length){reference-type="ref" reference="lem:recursive_length"}.

::: procedure
**procedure 23** ($\{x_{n},x_{p}\} \leftarrow FB\text{-}Extend^*\!(x_{rand},T)$). *Given $x_{rand} \in X$ and a tree $T = \{V,E\}$, the $FB\text{-}Extend^*$ uses $FB\text{-}Extend$ to find a node for extending the tree and then finds the locally optimal path in $V$ for connecting to the new point. The procedure is given in Algorithm [\[alg:fillet_optimal_extend\]](#alg:fillet_optimal_extend){reference-type="ref" reference="alg:fillet_optimal_extend"}.*
:::

:::: algorithm
::: algorithmic
$\{x_{n},x_{p},c_{min}\} \leftarrow FB\text{-}Extend(x_{rand},T)$ $X_{near} \leftarrow Near_{\rho,\alpha}(x_{n},T)$ $x_{gp} \leftarrow Parent(x_{near},T)$ $c_{tmp} \leftarrow FB\text{-}CostToCome(x_{n},x_{near},x_{gp},\!T)$ $x_{p} \leftarrow x_{near}$ $c_{min} \leftarrow c_{tmp}$ $\{x_{n},x_{p}\}$ $\{\varnothing,\varnothing\}$;
:::
::::

=\[circle,draw=black!100,thick\] =\[circle,draw=red!100, thick\] =\[circle,draw=green!100,thick\]

:::: {#fig:fillet_extend .figure latex-placement="ht"}
:::: {#fig:fillet_extend:sub1 .figure}
::: caption
The tree before $x_{rand}$ is sampled and Algorithm [\[alg:fillet_extend\]](#alg:fillet_extend){reference-type="ref" reference="alg:fillet_extend"} starts. The fillets are shown in magenta.
:::
::::

:::: {#fig:fillet_extend:sub2 .figure}
::: caption
$x_{rand}$ is sampled and node E is found to be the closest node to $x_{rand}$.
:::
::::

:::: {#fig:fillet_extend:sub3 .figure}
::: caption
$x_{rand}$ is steered toward node E and, after validity checking the new fillet, node J is created.
:::
::::

:::: {#fig:fillet_extend:sub4 .figure}
::: caption
$x_n$'s neighborhood set is found to be the singleton set of just node B.
:::
::::

:::: {#fig:fillet_extend:sub5 .figure}
::: caption
The correctness of connecting to B is verified. Connecting through B and E results in costs of $5.1$ and $14$ respectively.
:::
::::

:::: {#fig:fillet_extend:sub6 .figure}
::: caption
Because connecting through node B yields a lower total cost, node J is connected to node B. The fillets are shown in magenta.
:::
::::

::: caption
An illustration of the $FB\text{-}Extend$ and $FB\text{-}Extend^*$ procedures.
:::
::::

:::: {#fig:fillet_rewire .figure latex-placement="ht"}
:::: {#fig:fillet_rewire:sub1 .figure}
::: caption
The tree after $FB\text{-}Extend^*$ adds node J to the tree. The fillets are shown in magenta.
:::
::::

:::: {#fig:fillet_rewire:sub2 .figure}
::: caption
Node E is found to be the only element in node J's neighborhood set.
:::
::::

:::: {#fig:fillet_rewire:sub3 .figure}
::: caption
The validity of connecting E through J is checked. The original cost of node E is $11.8$ and its potential cost is $8$.
:::
::::

:::: {#fig:fillet_rewire:sub4 .figure}
::: caption
The validity of E's children is checked. The original costs of F and G are $13.7$ and $14.5$ and their potential costs are $10.5$ and $10.2$ respectively.
:::
::::

:::: {#fig:fillet_rewire:sub5 .figure}
::: caption
The validity of E's grandchildren, nodes H and I, is checked with respect to connecting node E through node J.
:::
::::

:::: {#fig:fillet_rewire:sub6 .figure}
::: caption
Node E is rewired to have node J as its parent. The fillets are shown in magenta.
:::
::::

::: caption
An illustration of the $FB\text{-}Rewire$ procedure.
:::
::::

## The Fillet-based Rewire Procedure {#sec:fb_rewire}

In the FB-RRT\* framework, care must be taken to ensure both path feasibility and cost improvement when rewiring. Unlike its straight-line counterpart, it is not sufficient to choose a parent based purely on the path length to the node. The following lemma presents a set of sufficient conditions to ensure that a rewiring will not be detrimental to the tree.

::: {#lem:fb-rewire .lemma}
**Lemma 5**. *Assume that a tree $T=\{V,E\}$ is given such that [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} is satisfied for all consecutive nodes. Rewiring $E$ to make $x_n \in V$ the new parent of $x_{near}\in V$ will result in a continuous path with all node costs unchanged or lowered if the following three conditions are met:*

1.  *[]{#rewA label="rewA"} The resulting path to $x_{near}$ using $x_n$ as its parent is obstacle free, does not violate [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}, and the cost of $x_{near}$ is improved, see Figure [34](#fig:fillet_rewire:sub3){reference-type="ref" reference="fig:fillet_rewire:sub3"}.*

2.  *[]{#rewB label="rewB"} The resulting path to each child of $x_{near}$ is obstacle free, does not violate [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}, and the cost of the child is not increased, see Figure [35](#fig:fillet_rewire:sub4){reference-type="ref" reference="fig:fillet_rewire:sub4"}.*

3.  *[]{#rewC label="rewC"} The resulting path to each grandchild of $x_{near}$ does not violate [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}, see Figure [36](#fig:fillet_rewire:sub5){reference-type="ref" reference="fig:fillet_rewire:sub5"}.*
:::

::: proof
*Proof.* The only paths that will be affected by changing the parent of $x_{near}$ will be the fillet connecting $x_{near}$ to its grandparent and the fillets connecting $x_{n}$ to the children of $x_{near}$. Conditions [\[rewA\]](#rewA){reference-type="ref" reference="rewA"}, [\[rewB\]](#rewB){reference-type="ref" reference="rewB"}, and [\[rewC\]](#rewC){reference-type="ref" reference="rewC"} employ obstacle checking and [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} to ensure that fillet curves do not overlap in the new section of path nor with the preceding or subsequent sections of the path.

The path cost to $x_{near}$ will be improved due to [\[rewA\]](#rewA){reference-type="ref" reference="rewA"}. The path costs to the children are not increased per [\[rewB\]](#rewB){reference-type="ref" reference="rewB"}. As all other parent and grandparent nodes remain unchanged, their respective path costs will not increase due to Corollary [2](#cor:unchanged){reference-type="ref" reference="cor:unchanged"}. ◻
:::

The $FB\text{-}Rewire$ procedure is now stated and illustrated in Figure [38](#fig:fillet_rewire){reference-type="ref" reference="fig:fillet_rewire"}.

::: procedure
**procedure 24** ($E \leftarrow FB\text{-}Rewire(x_{n},X_{near},T)$). *Given a tree, $T=\{V,E\}$, with node $x_n \in V$ and set $X_{near} \subset V$, $FB\text{-}Rewire$ returns a modified tree with $E$ changed to have $x_n$ be the parent to elements of $X_{near}$ if conditions in Lemma [5](#lem:fb-rewire){reference-type="ref" reference="lem:fb-rewire"} are satisfied. The procedure is given in Algorithm [\[alg:fillet_rewire\]](#alg:fillet_rewire){reference-type="ref" reference="alg:fillet_rewire"}.*
:::

:::: algorithm
::: algorithmic
$x_{p} \leftarrow Parent(x_{n},T)$ $c_{near} \leftarrow FB\text{-}CostToCome(x_{near},x_{n},x_{p},T)$ Continue $c_c \leftarrow FB\text{-}CostToCome(x_{c},x_{near},x_{n},T)$ Continue $X_{fillet} \leftarrow Fillet({x_n,x_{near},x_{c},x_{gc}})$ Continue $x_{p} \leftarrow Parent(x_{near},T)$ $E \leftarrow \left(E \setminus \{x_{p},x_{near}\} \right) \cup \{x_{n},x_{near}\}$ Continue: $T$
:::
::::

Note that the $Rewire$ procedure described above is different than that in [@{spline_rrt*}]. In [@{spline_rrt*}], the neighborhood set of $x_{n}$, $X_{near}$, is checked to ensure that:

1.  Connecting $x_{n}$ and $x_{near}$ will not violate their max angle and distance conditions.

2.  The curve formed between $x_{n}$ and $x_{near}$ is obstacle free.

3.  The cost of $x_{near}$ will be improved by the rewire operation.

Thus, condition [\[rewA\]](#rewA){reference-type="ref" reference="rewA"} is met (with a conservative continuity condition), but conditions [\[rewB\]](#rewB){reference-type="ref" reference="rewB"} and [\[rewC\]](#rewC){reference-type="ref" reference="rewC"} are not considered. If [@{spline_rrt*}]'s conditions hold, the children of $x_{near}$ are set to be the children of the parent of $x_{near}$ and the parent of $x_{near}$ is set to be $x_{n}$, see Figure [40](#fig:spline_rewire_counter:sub2){reference-type="ref" reference="fig:spline_rewire_counter:sub2"}. It is important to note that the $Rewire$ operation in [@{spline_rrt*}] could result in discontinuous paths due to not checking feasibility for all affected nodes. There is no guarantee that connecting the parent of $x_{near}$ directly to the children of $x_{near}$ will result in a valid tree. The angles and distances formed by that connection must first be checked as illustrated in Figure [41](#fig:spline_rewire_counter){reference-type="ref" reference="fig:spline_rewire_counter"}. Moreover, due to not checking costs on all affected nodes, the $Rewire$ operation in [@{spline_rrt*}] may actually increase costs to some nodes as shown in Lemma [2](#lem:rewiring_tests){reference-type="ref" reference="lem:rewiring_tests"}.

=\[circle,draw=black!100,thick\] =\[circle,draw=red!100, thick\] =\[circle,draw=green!100,thick\]

:::: {#fig:spline_rewire_counter .figure latex-placement="h"}
:::: {#fig:spline_rewire_counter:sub1 .figure}
::: caption
The Node F is being rewired around the preexisting tree, and node C is F's neighborhood set.
:::
::::

:::: {#fig:spline_rewire_counter:sub2 .figure}
::: caption
Node C is rewired to have node F as its parent, and node E becomes a child of node B.
:::
::::

::: caption
After node C has been rewired to node F the angle formed between nodes A, B, and B's child has increased, i.e. $\gamma_b > \gamma_a$. Without checking, there is no way to know if $\gamma_b$ is less then the max angle allowed.
:::
::::

Note that the FB-RRT and FB-RRT\* algorithms are not yet stated as additional improvements to the sampling and smoothing are first discussed in the following section. Also note that reverse motion considerations are discussed in Appendix [9](#sec:reverse_fillet){reference-type="ref" reference="sec:reverse_fillet"}.

# Overcoming the Voronoi Property {#section:improving_convergence}

Nonholonomic constraints exacerbate the slow convergence of RRT\*. This section introduces two refinements to FB-RRT\* designed to reduce convergence time. There are multiple variants of RRT\* that aim to improve convergence by improving sampling [@Akgun2011; @Gammell2014; @Kuwata2009; @Nasir2013]. Two such variants are used as a basis for design herein: Informed RRT\* (I-RRT\*) [@Gammell2014] and Smart RRT\* (S-RRT\*) [@Nasir2013]. These algorithms are identical to RRT\* before the first solution is found. However, after the first path to the goal is found, they use information about the solution to guide sampling toward space that will improve the final solution. In addition, S-RRT\* introduces a path smoothing procedure that continuously refines the solution path, further improving convergence. This section first presents I-RRT\* and S-RRT\*. These techniques are then combined in the Fillet-based Smart and Informed RRT\* (FB-SI-RRT\*) formulation.

## Informed RRT\* {#section:informed_rrt*}

Informed RRT\* (I-RRT\*) is an extension of RRT\* that aims to reduce the amount of time spent sampling space that will not improve the final path. It is observed that any time spent sampling outside of the set that will improve the path is wasted time. This set is referred to as the "informed" set and denoted as $X_{i} \subset X_{free}$. Naturally, it would be best to directly sample $X_{i}$. However, calculating $X_{i}$ can be difficult, if not impossible.

A conservative approximation of $X_{i}$, denoted as $X_{i}^\prime$, is defined in [@Gammell2014] based upon an approximation of the problem's optimal cost and the best cost found, $c_{best}$. The optimal cost is denoted as $c_{min}$ with its approximation denoted as $c_{min}^\prime$. The approximation for $c_{min}^\prime$ is calculated as the distance between the root node and final state in the best-found path, i.e. $c_{min}^\prime = \| x_{r} - x_{t} \|$. $X_i^\prime$ is defined as $$\begin{equation}
  X_{i}^\prime = \mathcal{E}_{x_{r},x_t}
\end{equation}$$ where $\mathcal{E}_{x_{r},x_t}$ is the open set of states in an ellipse with the focal points set at $x_{r}$ and $x_{t}$. The length of the major axis of the ellipse is $c_{best}$ and the length of the minor axis is $\sqrt{c_{best}^2 - c_{min}^{\prime2}}$, see Figure [42](#fig:ellipse){reference-type="ref" reference="fig:ellipse"}. With this definition of $X_{i}^\prime$, it is guaranteed that the best solution found so far is entirely inside the informed set.

:::: {#fig:ellipse .figure latex-placement="t"}
::: caption
The ellipse that defines $X_i^\prime$.
:::
::::

I-RRT\* samples solely within $X_{i}^\prime$ once the first solution is found, reducing the configuration space sampled and improving the probability that a given sample will improve the solution. Note that I-RRT\* is identical to RRT\* with the exception of using $X_{i}^\prime$ instead of $X_s$ for sampling new points after the first solution is found. As long as $c_{min}^\prime \le c_{min}$, it is shown in [@Gammell2014] that I-RRT\* maintains asymptotic optimality.

In an environment with small convex obstacles, I-RRT\* is shown to converge much faster than RRT\* [@Gammell2014]. If there are larger nonconvex obstacles then I-RRT\* degrades in performance to RRT\*. This is because the optimal cost, $c_{min}$, is much more than $c_{min}^\prime$, causing the informed subset to be very large.

## Smart RRT\* {#section:rrt*_smart}

Smart RRT\* (S-RRT\*) proposes two alternative approaches to improving convergence [@Nasir2013]. First, similar to I-RRT\*, the sampling set is reduced once a solution is found. Second, S-RRT\* proposes a path smoothing procedure that is used as an integral part of the algorithm to further improve convergence.

The sampling set is reduced by biasing sampling around the nodes that form the shortest found path. The idea being that improvements near the path can help to refine the chosen route around obstacles. These nodes are referred to as the beacon set, $X_b$, and can be defined as $$\begin{equation*}
  X_{b} = Solution(x_{t},T)
\end{equation*}$$ where $x_{t} \in X_{t}$ is the end of the shortest path to the target set. Subsequent iterations then bias the sampling towards the union of balls of radius $r_b$ around each beacon, i.e. $$\begin{equation*}
  X_s = \bigcup_{x_b \in X_b} \mathcal{B}_{x_b,r_b}
\end{equation*}$$ A major philosophical difference between S-RRT\* and I-RRT\* is that S-RRT\* biases the sampling around the beacon set whereas I-RRT\* seeks to reduce the size of the sampling space. The biasing encourages local path refinement with a continued sampling of $X$ for exploration.

Significant improvements are also made through the addition of a path smoothing procedure, referred to as $OptimizePath$ in [@Nasir2013]. $OptimizePath$ seeks to straighten out the path each time a better path is found. This avoids waiting for the sampling to straighten the path, something that becomes decreasingly probable as the number of samples increases due to the Voronoi property. The $OptimizePath$ procedure does this by performing rewire operations on each beacon with every other beacon, as detailed in Algorithm [\[alg:optimize_path\]](#alg:optimize_path){reference-type="ref" reference="alg:optimize_path"}. Note that the $RemoveBetween$ procedure removes all of the nodes in $X_b$ that lie between $x_{near}$ and $x_{ittr}$ not including $x_{near}$ and $x_{ittr}$. This removes nodes from the solution/beacon set that are not needed. Which straightens out the solution and reduces the number of beacons that have to be sampled.

:::: algorithm
::: algorithmic
$X_{b}^\prime \leftarrow \varnothing$ []{#alg:optimize_path:init_output label="alg:optimize_path:init_output"} []{#alg:optimize_path:first_for label="alg:optimize_path:first_for"} []{#alg:optimize_path:second_for label="alg:optimize_path:second_for"} $T \leftarrow Rewire(x_{ittr},\{x_{near}\},T)$ []{#ln:opt_path_rewire label="ln:opt_path_rewire"} $X_b \leftarrow RemoveBetween(x_{near},x_{ittr},X_b)$ []{#alg:optimize_path:end_second_for label="alg:optimize_path:end_second_for"} $X_{b}^\prime \leftarrow X_{b}^\prime \cup \{x_{ittr}\}$ $X_{b}^\prime$
:::
::::

Before the first solution is found, S-RRT\* performs identically to RRT\*. However, after the first solution is found, the convergence of S-RRT\* is much faster than RRT\*, especially for straight-line motion primitives. It is important to note that S-RRT\* has a tendency to spend more time converging on local minima than RRT\*. In fact, if only the space near the beacon set were to be sampled after the first solution was found, then S-RRT\* would lose its asymptotic optimality because it would only refine the first path found. We found that the beacon radius could be relatively small using straight-line paths, but needed to be increased significantly for curvature constrained paths.

## Smart and Informed Sampling

I-RRT\* performs well in small path planning problems where the obstacles are convex and $c_{min}^\prime$ is a good approximation of $c_{min}$. S-RRT\* converges impressively fast, especially when planning using straight-line paths. Both techniques add parameters that need to be determined -- an estimate of the best cost for informed and the beacon size for smart sampling. This work develops smart-and-informed sampling that combines S-RRT\*'s fast convergence with an adaptive sample set similar to I-RRT\*. It is designed specifically for the nonholonomic motion primitives to provide a sampling heuristic that does not require fine tuning of additional parameters.

As is the case with both of its predecessors, the sampling will be identical to RRT\* until the first solution is found. At that point, the $OptimizePath$ procedure, Algorithm [\[alg:optimize_path\]](#alg:optimize_path){reference-type="ref" reference="alg:optimize_path"}, is called on the initial solution. Instead of using a constant radius around each beacon (S-RRT\*), or an adaptive set based upon the optimality of the entire path (I-RRT\*), the beacon set, $X_{b} \subset V$, is used to generate ellipses around each adjacent pair of beacons along the path that leads from $x_{r}$ to $X_{t}$, as illustrated in Figure [43](#fig:beacons){reference-type="ref" reference="fig:beacons"}. The axes of the ellipse are adapted based on the local optimality of the path, producing a larger sampling space when path refinement is needed and a smaller space when the local path is near optimal. Similar to the sampling in S-RRT\*, the sampling after the beacons are found is biased towards the set formed by these ellipses, $$\begin{equation*}
  \mathcal{E}_{X_b} = \bigcup_{i=0}^{\mid X_b \mid-1} \mathcal{E}_{x_{b,i},x_{b,i+1}} \subset X.
\end{equation*}$$ This sampling bias encourages path refinement. The full configuration space is still sampled periodically for sake of exploration.

:::: {#fig:beacons .figure latex-placement="t"}
::: caption
The four nodes, $x_{b,0}$ through $x_{b,4}$, are connected with arc-fillets and each sampling ellipse, $\mathcal{E}_{x_{b,0},x_{b,1}}$, $\mathcal{E}_{x_{b,1},x_{b,2}}$, $\mathcal{E}_{x_{b,2},x_{b,3}}$, and $\mathcal{E}_{x_{b,3},x_{b,4}}$, is shown in red, blue, green, and orange respectively. Note that the volume of $\mathcal{E}_{x_{b,0},x_{b,1}}$ is $0$, because $c_{best,0} = c_{min,0}$.
:::
::::

For each beacon ellipse, $c_{min,i}^\prime$ is defined as the distance between the two adjacent beacons that act as the focal points for that ellipse $$\begin{equation*}
  c_{min,i}^\prime = \| x_{b,i+1} - x_{b,i} \|
\end{equation*}$$ and $c_{best,i}$ is the cost differential across the two beacons: $$\begin{equation*}
  c_{best,i} = Cost(x_{b,i+1}) - Cost(x_{b,i})
\end{equation*}$$ Note that for straight-line primitives $c_{best,i} = c_{min,i}^\prime$, causing each ellipse to degenerate to the line between $x_{b,i}$ and $x_{b,i+1}$. While sampling along this line can be beneficial, we show an example where it slows convergence because it neglects the exploration half of the exploration-exploitation paradigm. With the fillets, the ellipse rarely degenerates to a straight-line. Even when it does the $OptimizePath$ procedure removes the redundant intermediary points. The smart-and-informed sampling procedure is now presented.

::: procedure
**procedure 25** ($x_{rand} \leftarrow SI\text{-}Sample(i, b_t, b_b, X_b, X_t)$). *Returns a random point at iteration $i \in \mathbb{Z}_+$ given the sampling biases $b_t \in \mathbb{Z}_+$ and $b_b \in \mathbb{Z}_+$, the beacon set $X_b$, and the target set $X_t$ as described in Algorithm [\[alg:si_sampling\]](#alg:si_sampling){reference-type="ref" reference="alg:si_sampling"}.*
:::

The $SI\text{-}Sample$ procedure includes a biasing towards the target set and a random sampling of the configuration space for sake of exploration. Additionally, as is the case with S-RRT\*'s sampling, some percentage of the samples must be drawn from the full configuration space to maintain asymptotic optimality. This is because SI-RRT\* makes no guaranties about its ellipses containing the optimal solution as I-RRT\* does. Sampling within the ellipses of SI-RRT\* and the beacons of S-RRT\* has the effect of biasing the search to locally refine the current best path. The sampling of the beacon ellipses works in conjunction with the $OptimizePath$ procedure to seek improvements to the current best path found. The $OptimizePath$ procedure works to straighten paths while the sampling of the beacon ellipses works to see if local perturbations will improve path length.

:::: algorithm
::: algorithmic
$x_{rand} \leftarrow Sample(X_{t})$ $x_{rand} \leftarrow Sample(\mathcal{E}_{X_b})$ $x_{rand} \leftarrow Sample(X)$ $x_{rand}$
:::
::::

## Fillet-based Smart and Informed RRT\*

With the $SI\text{-}Sample$ procedure in hand, all of the components are in place for presenting the Fillet-Based Smart and Informed RRT\* (FB-SI-RRT\*) algorithm. The FB-SI-RRT\* algorithm is defined in Algorithm [\[alg:si_rrt\*\]](#alg:si_rrt*){reference-type="ref" reference="alg:si_rrt*"}. The straight-line counterpart can be expressed by removing the $FB$ prefix in all of the procedures. Furthermore, the fillet generation procedure used in $FB\text{-}CostToCome$ can be replaced with either the arc or Bézier fillets.

The FB-SI-RRT\* algorithm is very similar to the traditional RRT\* algorithm as defined in Algorithm [\[alg:rrt\*\]](#alg:rrt*){reference-type="ref" reference="alg:rrt*"}. The major differences are the use of the fillet-based procedures in place of the straight-line counterparts and the $SI\text{-}Sample$ procedure in place of the $Biased\text{-}Sample$. The path optimization procedure from S-RRT\* is also included in SI-RRT\* but is absent in traditional RRT\*.

The FB-SI-RRT\* algorithm begins on line [\[ln:fb_initialize\]](#ln:fb_initialize){reference-type="ref" reference="ln:fb_initialize"} by initializing the tree to consider the initial orientation of the vehicle and setting $X_b$ and $c_b$ to the empty set. As with RRT\*, a prefixed number of iterations is specified for refining the path. Each iteration begins with the sampling of a new point using the $SI\text{-}Sample$ procedure. This balances biasing towards the target set to find the goal, biasing towards the beacon set to refine the best path found, and sampling from the general obstacle free space for exploration. The sampled point is then used within $FB\text{-}Extend^*$ in line [\[ln:fb_extend\]](#ln:fb_extend){reference-type="ref" reference="ln:fb_extend"} to grow the tree in the direction of the new sample while respecting the fillet continuity constraints. If a connection to the tree is found, a new node is then inserted into the tree on line [\[ln:add_node\]](#ln:add_node){reference-type="ref" reference="ln:add_node"}. The edge set is then rewired around the new node on line [\[ln:fb_rewire\]](#ln:fb_rewire){reference-type="ref" reference="ln:fb_rewire"} using the $FB\text{-}Rewire$ to consider the fillet continuity and cost improvement requirements. If the first path or a shorter path to the target has been found, then the beacon set is updated in line [\[ln:fb_beacons\]](#ln:fb_beacons){reference-type="ref" reference="ln:fb_beacons"}. If $c_b$ has changed, and thus $X_b$ has changed, a $FB\text{-}OptimizePath$ procedure is used on line [\[ln:fb_opt_path\]](#ln:fb_opt_path){reference-type="ref" reference="ln:fb_opt_path"} in an attempt to refine the beacon set. Note that the $FB\text{-}OptimizePath$ has not been defined, but it can be expressed by changing line [\[ln:opt_path_rewire\]](#ln:opt_path_rewire){reference-type="ref" reference="ln:opt_path_rewire"} of Algorithm [\[alg:optimize_path\]](#alg:optimize_path){reference-type="ref" reference="alg:optimize_path"} to use the $FB\text{-}Rewire$ procedure.

:::: algorithm
::: algorithmic
$T \leftarrow FB\text{-}Initialize_{d_{init}}(x_{r},\psi_{r})$ []{#ln:fb_initialize label="ln:fb_initialize"} $X_{b} \leftarrow \varnothing$ $c_b \leftarrow \varnothing$ $x_{rand} \leftarrow SI\text{-}Sample(i, b_t, b_b, X_b, X_t)$ []{#ln:si_sampling label="ln:si_sampling"} $\{x_{n},x_{p},c_n\} \leftarrow FB\text{-}Extend^*\!(x_{rand},T)$ []{#ln:fb_extend label="ln:fb_extend"} $T \leftarrow InsertNode(x_{n},x_{p},T)$ []{#ln:add_node label="ln:add_node"} $T \leftarrow FB\text{-}Rewire(x_{n},Near_{\rho,\alpha}(x_{n},T),T)$ []{#ln:fb_rewire label="ln:fb_rewire"} $X_{b} \leftarrow Solution(x_{n},T)$ []{#ln:fb_beacons label="ln:fb_beacons"} $X_{b} \leftarrow FB\text{-}OptimizePath(X_{b},T)$ []{#ln:fb_opt_path label="ln:fb_opt_path"} $c_b \leftarrow c(X_b)$ $X_{b}$
:::
::::

Both an informed variation and smart variation to the FB-RRT\* algorithm can be created with small variations to Algorithm [\[alg:si_rrt\*\]](#alg:si_rrt*){reference-type="ref" reference="alg:si_rrt*"}. The informed algorithm can be formed by replacing line [\[ln:si_sampling\]](#ln:si_sampling){reference-type="ref" reference="ln:si_sampling"} with informed sampling and removing line [\[ln:fb_opt_path\]](#ln:fb_opt_path){reference-type="ref" reference="ln:fb_opt_path"}. The smart algorithm can be formed by replacing line [\[ln:si_sampling\]](#ln:si_sampling){reference-type="ref" reference="ln:si_sampling"} with smart sampling.

# Examples {#sec:results}

A series of examples are now shown to demonstrate the Fillet-based RRT\* approach. Three environments were chosen to illustrate the performance of various RRT\*-based planners. Within each environment, 16 series of simulations were conducted to illustrate and evaluate the sampling and motion primitive variations. RRT\*, I-RRT\*, S-RRT\*, and SI-RRT\* planned using straight-line, arc-fillet, Bézier-fillet, and Dubin's path motion primitives.

Note that a comparison between motion primitive types is not meant to show that one motion primitive is better than another. Planning with straight-line paths is going to have better convergence characteristics due to their simplicity and lack of dynamic constraints. In fact, the only primitives that can be directly compared in this fashion are arc-fillets and the Dubin's paths as both assume the same dynamic constraints. The straight-line primitive is included to show a best-case scenario, providing a pseudo cost of considering the additional dynamic constraints. This section proceeds with details on the simulations followed by a description of the different environments. A comparison is made between the fillet formulation presented herein and that of [@{spline_rrt*}] followed by an example that justifies the need to consider curvature constraints while path planning. Finally, the section ends with a discussion of the results.

## Simulation Details

The obstacles are represented with an occupancy grid with each pixel corresponding to one square millimeter. When performing obstacle collision checks clearance of $0.5m$ is required on all sides. As orientation is well defined in the case of Dubin's paths and fillets, the points that are $0.5m$ to the right and left of the paths are checked. In the case of straight-line paths, orientation is not well-defined at the nodes so points are checked $0.5m$ in every cardinal direction. Paths are generated and checked at one-centimeter resolution.

The steering constant, $\eta$, and neighbor search radius, $\rho$, are both $3m$. The max number of neighbors to search, $\alpha$, is $100$. The check target period, $b_t$, is $50$ and the target set, $X_{t}$, is a circle of radius $0.1m$. The Dubin's radius is set to $0.5m$ and likewise, the maximum curvature constraint imposed on the fillet generation is $2m^{-1}$. The root node to first node distance, $d_{init}$, is $1m$. Note that these values are somewhat aggressive for some curvature constrained applications, but they allow the straight-line primitive to provide a tighter bound on the possible performance characteristics of the curvature constrained planners. For S-RRT\*, the beacon radius is $3m$ unless otherwise stated. Note that this is not necessarily the best choice of beacon radius, as shown in Figure [49](#fig:s_rrt_beacon_size){reference-type="ref" reference="fig:s_rrt_beacon_size"}. However, smaller radius values are very detrimental to the Dubin's path results. The beacon bias, $b_b$, is $3$ for both S-RRT\* and SI-RRT\*.

Results are gathered using OMPL [@ompl]. Simulation code can be found in our open-source repository <https://gitlab.com/utahstate/robotics/fillet-rrt-star>. As the sampling is random, each simulation series consists of 100 individual simulations with the average results being presented. The results were gathered on an AMD RyzenThreadripper2990WX processor. Convergence plots were made by fitting a 10^th^ order polynomial using a least-squares fitting algorithm as described in [@Venables2002].

A least-squares approach is used as the sampling times for path length are not uniform across all simulations and not all simulations find the initial path at the same time. Note that while the path length for any one run will be monotonically decreasing with time, the least squares fitted plot does not always have the same monotonic property. The reason is that a particular run may not find a solution until well after other runs and the initial solution it finds may be much larger than the current solution of the other runs, effectively causing the average to increase at the time the run first produces path length data.

## Environments

The three environments shown in Figure [\[fig:all_worlds\]](#fig:all_worlds){reference-type="ref" reference="fig:all_worlds"} were chosen to present and evaluate the performance of differing RRT\* approaches. The environments are referred to as the Spiral world, the Cluttered world, and the Maze world.

The Spiral world is made up of one narrow passage that twists around the starting point. The world is $40m$ by $40m$, $x_r = \begin{bmatrix} 0 & 0 \end{bmatrix}^T$, and the center of $X_t$ is at $\begin{bmatrix} -15 & -15 \end{bmatrix}^T$. The only path from $x_r$ to $X_t$ is through a narrow hallway forming a "bug trap" like set of obstacles. The Spiral world tests planners' abilities to find a way out of the confined starting area and then converge through all of the passageways. The "bug trap" like design makes it difficult for Dubin's paths based planners to find an initial solution, and I-RRT\*'s cost heuristic is a poor estimate of $c_{min}$ in this environment. The environment is well suited for smart sampling as there is only one path and refinements are beneficial at each turn.

The Cluttered world is composed of many overlapping circular obstacles. The world is $100m$ by $100m$, $x_r = \begin{bmatrix} -40 & -40 \end{bmatrix}^T$, and the center of $X_t$ is at $\begin{bmatrix} 40 & 40 \end{bmatrix}^T$. The abundance of small obstacles results in many small local minima, but there are still large open areas for exploration. The Cluttered world tests the planners' ability to break out of local minima. I-RRT\* based sampling is well-suited in the environment as the I-RRT\* heuristic is a good estimate of the optimal path length.

The Maze world features a series of narrow passages and dead ends. The world is $50m$ by $50m$, $x_r = \begin{bmatrix} -11 & -22.5 \end{bmatrix}^T$, and the center of $X_t$ is at $\begin{bmatrix} 2.5 & 12.5 \end{bmatrix}^T$. The Maze world has fewer local minima than the Cluttered world and consists of long narrow corridors. This world tests the planners' ability to find high-quality initial solutions quickly and then converge past those initial solutions. While the local minima can be detrimental to beacon-based sampling, the optimal cost heuristic in I-RRT\*'s sampling is poor in this case, proving detrimental to I-RRT\*'s convergence.

::: sidewaysfigure
::: figure
:::

::: figure
:::

::: figure
:::
:::

## Comparison with Previous Work

Note that this work's FB-RRT\* differs from what is given in [@Yang2014; @{spline_rrt*}] in the following ways:

- The generalization of [@Yang2014; @{spline_rrt*}]'s $\gamma_{max}$ and $d_{min}$ based path continuity constraints to the less restrictive form given in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}. See Figure [21](#fig:spline_reach){reference-type="ref" reference="fig:spline_reach"} for an illustration of how [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} is less restrictive than using the $\gamma_{max}$/$d_{min}$ constraints.

- The addition of a pseudo "node orientation" in the nearest neighbor search heuristically penalizes turns and enables us to forgo the k-nearest-neighbor search that [@{spline_rrt*}] uses. See the explanation of $FB\text{-}Extend$ in Section [4.1](#sec:procedures_with_minor_changes){reference-type="ref" reference="sec:procedures_with_minor_changes"} for more information.

- A newly developed rewiring procedure that ensures continuity and cost improvement in the resulting path. See Section [4.2](#sec:fb_rewire){reference-type="ref" reference="sec:fb_rewire"} for more information on $FB\text{-}Rewire$.

- The generalization of the fillet-based planner structure to make use of any fillet type instead of just Bézeir-fillets.

This section uses convergence plots to compare the formulation of the fillet constraints in this work to the formulation given in [@Yang2014; @{spline_rrt*}]. Specifically, instead of constraining node addition in the tree with [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"} we use the constants given in [@Yang2014]. [@Yang2014] defines a max node-to-node angle, $\gamma_{max}$, and then uses that angle to define a minimum node-to-node distance, $d_{min} = d\!\left(\gamma_{max}\right)$. Any nodes that form an angle greater than $\gamma_{max}$ or are closer together than $2d_{min}$ are deemed invalid. This is a conservative approximation of the constraints defined in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}, see Section [3.4](#section:bezier_curve_gen){reference-type="ref" reference="section:bezier_curve_gen"} for more details. We refer to the version of FB-RRT\* that uses [@Yang2014]'s constraints as SB-RRT\*.

Note that SB-RRT\* differs from what is given in [@{spline_rrt*}] because the $FB\text{-}Rewire$ procedure is used to avoid the invalid tree configurations that result from the $Rewire$ procedure in [@{spline_rrt*}], see Figure [41](#fig:spline_rewire_counter){reference-type="ref" reference="fig:spline_rewire_counter"}. The Bézeir-fillet is used for comparison because that is the fillet used in [@Yang2014; @{spline_rrt*}]. The Cluttered world was chosen for this simulation because it is similar to the simulated environment used in [@Yang2014]. The max allowed curvature is kept at $2m^{-1}$, $\gamma_{max} = \frac{\pi}{2} rad.$, and $d_{min} = 0.7938 m$.

:::: {#fig:sb_rrt_comp .figure latex-placement="h"}
:::: {#fig:sb_rrt_convergence .figure}
::: caption
Convergence of solution cost in the Cluttered world over 5 minutes. FB-RRT\* is shown in blue and SB-RRT\* is shown in purple.
:::
::::

:::: {#fig:sb_rrt_paths .figure}
::: caption
Example solutions found in the Cluttered world after 5 minutes. FB-RRT\* is shown in blue and SB-RRT\* is shown in purple.
:::
::::

::: caption
A comparison of the solution quality found by FB-RRT\* and SB-RRT\*. FB-RRT\* converges faster and to a shorter solution then SB-RRT\*. FB-RRT\* is shown in blue and SB-RRT\* is shown in purple.
:::
::::

Figure [44](#fig:sb_rrt_convergence){reference-type="ref" reference="fig:sb_rrt_convergence"} shows the convergence of SB-RRT\* and FB-RRT\* in the scenario described. FB-RRT\* far outperforms SB-RRT\* in both initial convergence speed and the solution to which it settles over time. FB-RRT\* converges to a much shorter path then SB-RRT\* as the constraints given in [@Yang2014] force each node along the solution to be at least $2 d_{min}$ distance away from each other. As the solution converges, it becomes difficult to shorten the path further without reducing the number of nodes that make up the solution path. We emphasize that this simulation only shows the benefit of using the constraints in [\[equ:conditions\]](#equ:conditions){reference-type="eqref" reference="equ:conditions"}. A significant benefit is also received from the updated rewiring procedure that ensures continuous paths are produced.

## Curvature Constrained Paths {#sec:curvature_constrained_paths}

This section provides an example of when considering curvature constraints during path planning is advantageous. A common approach to curvature constrained path planning is to plan using straight-line motion primitives and then smooth the path after planning; see, for example, Chapter 11 of [@Beard2012]. However, this can lead to invalid paths.

:::: {#fig:curvature_demo_world .figure latex-placement="h"}
::: caption
The resulting paths from running RRT\* in an environment where the straight-line path turns sharply down a corridor. Straight-line and arc-fillet paths are shown in green and blue respectively.
:::
::::

One of the scenarios where this would be a problem is shown in Figure [47](#fig:curvature_demo_world){reference-type="ref" reference="fig:curvature_demo_world"}. Path planning using straight-line primitives converges to the solution shown in green. This is the shortest path between the start and goal locations while ensuring a minimum distance is maintained between the path and obstacles.

However, a path that goes through this hallway can not satisfy the curvature constraints of the problem without hitting the walls or performing a complex, multi-turn maneuver. See Appendix [9](#sec:reverse_fillet){reference-type="ref" reference="sec:reverse_fillet"} for details on generating a multi-turn maneuver with FB-RRT\*. If curvature constants are considered during path planning, as is the case for FB-RRT\*, then the path planner will return a solution through the second corridor, which is wide enough to make the turn.

## Results

The different motion primitives are now compared in terms of the initial solution, the convergence, and the effects of the various sampling techniques.

### Initial Solution Comparison

Table [\[tab:initialization_results\]](#tab:initialization_results){reference-type="ref" reference="tab:initialization_results"} shows the performance of each motion primitive in finding the initial solution in terms of the mean time and length of the initial solution for each environment. The results in Table [\[tab:initialization_results\]](#tab:initialization_results){reference-type="ref" reference="tab:initialization_results"} apply regardless of the sampling technique used as each sampling approach behaves identically to RRT\* before the first solution is found.

The Spiral and Maze worlds take longer on average to find an initial solution than the Cluttered world. There are a couple of reasons that this may occur. Both worlds have more narrow passages, resulting in a large number of iterations that fail to extend the tree because their paths become invalidated by obstacles. Furthermore, the Maze world has many dead-ends, allowing the tree to spend time growing in a direction that will not lead to the target set.

Planners using the arc-fillet primitive find an initial solution in a time comparable to that of the planners using straight-line paths in all of the environments considered, performing slightly faster in the Maze world. Similarly, the path lengths found are comparable, with the straight-line based paths being slightly shorter in all cases. The added cost of considering continuity in curvature is seen as the planners using Bézier-fillets require roughly twice the time to find an initial solution as their arc-fillet counterparts in all three environments. Table [3](#tab:init_cost){reference-type="ref" reference="tab:init_cost"} shows the Bézeir-fillet based planners finding a slightly shorter initial solution than their arc-fillet counterparts. This may be due to the fact that the Bézier-fillet planners take more time and iterations to find an initial solution. During that same time, the planners using arc-fillets are refining their solutions, always having a shorter path than the Bézier-fillet planners.

It takes significantly longer for planners using Dubin's paths to find an initial solution in each of the worlds tested here. The only world where Dubin's paths based planners found an initial solution in a comparable amount of time is the Cluttered world, although the initial path is also significantly longer. This is, in part, due to loops in the path, similar to that depicted in Figure [16](#fig:fillet_vs_dubins){reference-type="ref" reference="fig:fillet_vs_dubins"}. In the Cluttered world, the first path found has many loops and bends, resulting in a longer path length on average. These loops prove even more detrimental in the Spiral and Maze worlds with their narrow passageways. The path length does not increase as dramatically for Dubin's paths in the Spiral and Maze worlds as it does in the Cluttered world because there is not as much room for looping paths. However, there is a significant impact to the initial solution time as planning with Dubin's paths requires over 2 to 9 times as long as Bèzier-fillets and 5 to 15 times as long as arc-fillets.

It is important to note that the least squares fitting distorts the average transients plots in Figure [\[fig:transients\]](#fig:transients){reference-type="ref" reference="fig:transients"}. The average initial solution length for each planner is equivalent for any particular motion primitive. However, the rapid convergence of some planners cause the least squares solution to appear lower at the initial solution time.

:::: subtable
::: {#tab:init_cost}
   Motion Primitive               Spiral                    Cluttered                    Maze
  ------------------ --------------------------------- ------------------- ---------------------------------
    Straight-line     $\,\,\, 4.328 \pm \,\,\, 1.158$   $0.498 \pm 0.196$      $11.183 \pm \,\,\, 3.455$
     Dubin's path        $96.792       \pm 38.124$      $1.585 \pm 1.357$         $40.849 \pm 17.587$
      Arc-fillet      $\,\,\, 6.373 \pm \,\,\, 2.124$   $0.586 \pm 0.527$   $\,\,\, 7.473 \pm \,\,\, 2.057$
    Bézeir-fillet     $10.288       \pm \,\,\, 3.292$   $1.081 \pm 1.966$   $14.002 \pm \,\,\, 4.04 \,\,\,$

  : The means and standard deviations of the initial path length in meters after RRT\* has found an initial solution.
:::
::::

:::: subtable
::: {#tab:init_cost}
   Motion Primitive        Spiral             Cluttered                 Maze
  ------------------ ------------------- -------------------- -------------------------
    Straight-line     $136.05 \pm 3.91$   $167.42 \pm 12.14$      $142.25 \pm 7.84$
     Dubin's path     $161.68 \pm 7.73$   $275.07 \pm 39.55$      $162.65 \pm 9.86$
      Arc-fillet      $144.45 \pm 6.47$   $184.54 \pm 21.81$   $148.56 \pm 8.4 \,\,\,$
    Bézeir-fillet     $137.76 \pm 5.45$   $181.45 \pm 23.76$   $147.2 \,\,\, \pm 8.03$

  : The means and standard deviations of the initial path length in meters after RRT\* has found an initial solution.
:::
::::

::: sidewaysfigure
:::

:::: {#fig:convergence_bar_graph .figure latex-placement="ht"}
::: caption
The average time it took each planner to find a solution that was within 5 and 2 percent of the best averaged solution found after 50 seconds. Images from left to right show the results of the straight-line, arc-fillet, and Bézeir-fillet motion primitives. RRT\* is shown in blue, I-RRT\* in brown, S-RRT\* in green, and SI-RRT\* in red.
:::
::::

### Convergence Times of Motion Primitives

Once an initial solution is found, the algorithms work to converge on the shortest path. In this section, the resulting path lengths generated from planning using different motion primitives are directly compared. Note that this is inherently an unfair comparison as the primitives have different kinematic constraints. The only two motion primitives that use the same kinematic constraints are Dubin's paths and arc-fillets. The straight-line motion primitive does not respect curvature constraints while Bézeir-fillet primitive considers a curvature rate constraint in addition to the curvature constraint considered by the arc-fillet primitive. Each scenario has been designed such that the optimal path for each motion primitive will be similar, unlike the scenario in Figure [47](#fig:curvature_demo_world){reference-type="ref" reference="fig:curvature_demo_world"}. This allows the straight-line convergence rate to be a pseudo best-case solution. The results will show that the fillet-based planners have comparable results to the straight-line planners.

Figure [\[fig:transients\]](#fig:transients){reference-type="ref" reference="fig:transients"} shows the performance of each motion primitive with the four different sampling techniques. The green shaded areas start at the path length of the best averaged solution found for that world in 50 seconds. The yellow shaded area starts once the path length is within 2 percent of the best averaged solution for the respective environment. Similarly, the red shaded area starts once the path length is within 5 percent of the best averaged solution for the respective environment.

Table [4](#tab:best_planners){reference-type="ref" reference="tab:best_planners"} shows the best performing planners in each world and type of motion primitive. In the Spiral world, the best averaged solution found within 50 seconds was found by S-RRT\* planning with straight-lines with a path length of $116.14 m$. For the Cluttered world, the best was found by I-RRT\* planning with straight-lines with a path length of $128.79 m$. For the Maze world, the best was found by SI-RRT\* planning with straight-lines with a path length of $129.54 m$. Note that in each case, the planner that found the shortest averaged solution was planning with straight-line motion primitives. This is expected because the straight-line primitive is the least constrained.

::: {#tab:best_planners}
+------------------+---------------------+--------------------+---------------------+
| Motion Primitive | Spiral              | Cluttered          | Maze                |
+:================:+:========:+:========:+:=======:+:========:+:========:+:========:+
| Straight-line    | S-RRT\*  | $116.14$ | I-RRT\* | $128.79$ | SI-RRT\* | $129.54$ |
+------------------+----------+----------+---------+----------+----------+----------+
| Dubin's path     | SI-RRT\* | $122.6$  | I-RRT\* | $145.54$ | SI-RRT\* | $143.17$ |
+------------------+----------+----------+---------+----------+----------+----------+
| Arc-fillet       | SI-RRT\* | $116.34$ | I-RRT\* | $129.46$ | SI-RRT\* | $130.31$ |
+------------------+----------+----------+---------+----------+----------+----------+
| Bézeir-fillet    | SI-RRT\* | $116.49$ | I-RRT\* | $129.98$ | SI-RRT\* | $130.92$ |
+------------------+----------+----------+---------+----------+----------+----------+

: The best performing planner and associated average path length for that planner in each environment and motion primitive combination. Results are calculated after running the planners for 50 seconds.
:::

Figure [48](#fig:convergence_bar_graph){reference-type="ref" reference="fig:convergence_bar_graph"} shows the 5 and 2 percent convergence times in a bar graph for a quick comparison of results. It is worth noting that planners using the Dubin's path primitive struggle to approach the 5 percent convergence region and are subsequently left out of Figure [48](#fig:convergence_bar_graph){reference-type="ref" reference="fig:convergence_bar_graph"}. On the other hand, the arc-fillet planners perform quite well despite assuming the same motion constraints as the Dubin's primitive. The arc-fillet based planners perform comparably, and in some cases better, than the straight-line primitives in converging to the 5 percent threshold. Convergence begins to suffer for the 2 percent threshold, with some arc-fillet planners unable to cross that threshold in the Maze world.

The Bézier-fillet planners show an increase in convergence time, underscoring the cost of requiring continuity in curvature. SI-RRT\* is the only planner that is able to cross the 2 percent threshold when planning with Bèzier-fillets in the Maze world. However, when planning with Bézier-fillets in the Cluttered world, the smart sampling techniques (S-RRT\* and SI-RRT\*) fail to cross the 2 percent threshold while both RRT\* and I-RRT\* are able.

### The Effect of Sampling Techniques

The environments have little effect on the trends of ranking the performance of the motion primitives. The planning with straight-lines typically outperforms the arc-fillets, which outperforms the Bèzier-fillets, which in turn outperforms planning with Dubin's paths. However, the environment has a significant effect on the performance of the sampling procedures.

Table [4](#tab:best_planners){reference-type="ref" reference="tab:best_planners"} shows that each environment has a sampling procedure that works best in that environment. For the Cluttered world, I-RRT\* performs the best across all motion primitives. Whereas in the Spiral and Maze worlds, the greedier sampling heuristics perform better. In the Maze world, SI-RRT\* performs the best for all motion primitives. In the Spiral world, S-RRT\* performs the best when planning with straight-lines but SI-RRT\* performs best for all other motion primitives. This shows that S-RRT\*'s sampling works very well when planning with straight-lines but tends to struggle more when planning with kinematic constraints.

As mentioned, the Cluttered world is ideal for I-RRT\*'s sampling approach and, as expected, the I-RRT\* based planners perform the best in terms of 5 and 2 percent convergence. However, the transient plots in Figure [\[fig:transients\]](#fig:transients){reference-type="ref" reference="fig:transients"} show a very interesting trend. The smart approaches (S-RRT\* and SI-RRT\* based planners) show significantly faster initial convergence. This is due to the fact that the smart approaches focus on refining the best solution instead of searching the environment, which also means that they tend to spend more time in local minima. This is particularly noticeable in the Cluttered world where the smart approaches plateau for a time before dropping again. The Spiral and Maze worlds present environments in which there are fewer local minima and as such the smart approaches continue rapidly refining the solution until the 5 and 2 percent thresholds.

Figures [\[fig:transients\]](#fig:transients){reference-type="ref" reference="fig:transients"} and [48](#fig:convergence_bar_graph){reference-type="ref" reference="fig:convergence_bar_graph"} show that the SI-RRT\* based planners focus heavily on refining the current shortest solution. In the Cluttered world, this proves detrimental as it causes the planner to focus on local minima instead of searching for other paths through the obstacle topology. SI-RRT\*'s greedy convergence to local solutions is why SI-RRT\*'s solution cost plateaus in the Cluttered world, see Figure [\[fig:transients\]](#fig:transients){reference-type="ref" reference="fig:transients"}. In the Maze and Spiral worlds, it proves beneficial and results in the fastest convergence, both initially and to the 5 and 2 percent thresholds for all but the straight-line motion primitives. This may be because there are fewer local minima in the obstacle topology of these worlds. As expected, the smart-and-informed sampling does quite poorly for straight-line primitives.

Figure [49](#fig:s_rrt_beacon_size){reference-type="ref" reference="fig:s_rrt_beacon_size"} shows that the SI-RRT\* approach provides greedy refinement for fillet-based primitives without requiring the tuning of an extra beacon-size parameter. Figure [49](#fig:s_rrt_beacon_size){reference-type="ref" reference="fig:s_rrt_beacon_size"} compares the results from S-RRT\* based planners over various beacon sizes to the results of the respective SI-RRT\* based planner. In the Cluttered world, SI-RRT\* spends most of its time refining local minima and results in the worst convergence times. In both the Maze and the Spiral worlds, the smart-and-informed sampling performs near the best, except when considering straight-line primitives. While an iterative search over beacon sizes for S-RRT\* can produce similar convergence results to SI-RRT\*, the smart-and-informed sampling does not require additional tuning to find the best beacon size. Note that the resulting best beacon size for S-RRT\* sampling is dependent upon both the environment and the motion primitive, making such a search difficult prior to execution.

:::: {#fig:s_rrt_beacon_size .figure latex-placement="ht"}
::: caption
The average time it took each planner to find a solution what was within 5 and 2 percent of the best averaged solution found after 50 seconds. Images from left to right show the results of the straight-line, arc-fillet, and Bézeir-fillet motion primitives. S-RRT\* with a beacon sizes of $0.1m$, $0.5m$, $1m$, $3m$, $5m$, $10m$, and $15m$ are shown in brown, cyan, magenta, green, orange, purple, and violet respectfully. SI-RRT\* is shown in red.
:::
::::

# Conclusion {#sec:conclusion}

In this work, an RRT-based path planning algorithm is proposed that uses general fillets as motion primitives. An arc-fillet is designed to provide path continuity similar to a Dubin's path while a Bèzier-fillet is developed to provide continuity in path curvature. RRT\*-like procedures are developed to accommodate fillet-based motion primitives. Simulation results show that planning with arc-fillets significantly outperforms the use of Dubin's paths as a motion primitive. Planning with arc-fillets is shown to perform almost as well as straight-line motion primitives. Planning with Bèzier-fillets exhibits slightly worse performance than arc-fillets, although it far outperformed planning with Dubin's despite considering more complex dynamic constraints. A comparison is made between informed sampling, smart sampling, and a new smart-and-informed sampling technique. Like their straight-line counterparts, the fillet-based planners perform better with informed sampling when the heuristic for the shortest path is valid and better with smart sampling when there are fewer local minima. The smart-and-informed sampling performed well for fillet-based motion primitives and was found to be most applicable to environments with fewer local minima. In such environments, it performed on par with the best smart beacon size without the need for an iterative search for that beacon size.

# Declarations

## Funding

The authors declare that no funds, grants, or other support were received during the preparation of this manuscript.

## Competing Interests

The authors have no relevant financial or non-financial interests to disclose.

## Code Availability

Simulation code can be found in our open-source repository <https://gitlab.com/utahstate/robotics/fillet-rrt-star>.

## Author Contributions

All authors contributed to the work's conception and design. Software development, material preparation, and data collection were performed by James Swedeen. Data analyses were performed by James Swedeen and Dr. Greg Droge. James Swedeen is the primary author with major editorial and conceptual contributions made by Dr. Greg Droge and Dr. Randall Christensen at various stages of the writing process. All authors read and approved the final manuscript.

## Ethics Approval

Not applicable.

## Consent to Participate

Not applicable.

## Consent for Publication

Not applicable.

::::: appendices
# Reverse Fillet {#sec:reverse_fillet}

This section describes a novel reverse fillet formulation that enables the ability to plan paths that go forward and backward. The reverse fillet formulation uses a generic one-directional fillet internally that can be replaced by any fillet primitive desired. This section ends with an example planning problem that necessitates reverse and forward motion to follow the shortest path possible.

When using the reverse fillet motion primitive the direction state, $d$, is added to the state space. $d=1$ when the vehicle is moving forward and $d=-1$ when the vehicle is moving backward. It can be determined if a fillet should keep the direction of travel the same or change it by comparing the $d$ values of the nodes that the fillet connect. When using FB-RRT\* with the reverse fillet formulation, $d$ is randomly sampled from a uniform distribution when the state space is sampled.

Before the $ReverseFillet$ procedure can be given a few pieces of notation must be defined. We use the notion $x_{0,d}$ to denote the $d$ value of node $x_0$ and $x_{0,xy}$ to denote the position vector of node $x_0$. The function $R\left(\cdot\right)$ consumes an angle and produces a two-by-two right handed rotation matrix.

:::: algorithm
::: algorithmic
$X_{unidir} \leftarrow Fillet\left(x_{0,xy},x_{1,xy},x_{2,xy},x_{3,xy}\right)$ []{#alg:reverse_fillet:normal_fillet label="alg:reverse_fillet:normal_fillet"} $X_{fillet} \leftarrow \left\{\begin{bmatrix} x_{u,x} & x_{u,y} & x_{3,d} \end{bmatrix}^T, x_u \in X_{unidir}\right\}$ []{#alg:reverse_fillet:normal_fillet_dir label="alg:reverse_fillet:normal_fillet_dir"} $R_2 \leftarrow R\left(-atan2\left(x_{2,y} - x_{1,y}, x_{2,x} - x_{1,x}\right)\right)$ []{#alg:reverse_fillet:rot_mat label="alg:reverse_fillet:rot_mat"} $_2x_{0} \leftarrow R_2 \cdot \left[x_{0,xy} - x_{2,xy}\right]$ $_2x_{1} \leftarrow R_2 \cdot \left[x_{1,xy} - x_{2,xy}\right]$ $_2x_2 \leftarrow \begin{bmatrix} 0 & 0 \end{bmatrix}^T$ $_2x_{3} \leftarrow R_2 \cdot \left[x_{3,xy} - x_{2,xy}\right]$ []{#alg:reverse_fillet:end_frame_shift label="alg:reverse_fillet:end_frame_shift"} $_2x_{3f} \leftarrow \begin{bmatrix} -{_2x_{3,x}} & {_2x_{3,y}}\end{bmatrix}^T$ []{#alg:reverse_fillet:flip_x3 label="alg:reverse_fillet:flip_x3"} $X_{unidir} \leftarrow Fillet\left({_2x_{0}}, {_2x_{1}},{_2x_2},{_{2}x_{3f}}\right)$ []{#alg:reverse_fillet:forward_fill label="alg:reverse_fillet:forward_fill"} $X_{fillet} \leftarrow \left\{
        \begin{array}{lr}
          \begin{bmatrix}  x_{u,x} & x_{u,y} & x_{2,d} \end{bmatrix}^T & \text{for } x_{u,x} \leq 0 \\
          \begin{bmatrix} -x_{u,x} & x_{u,y} & x_{3,d} \end{bmatrix}^T & \text{for } x_{u,x} > 0
        \end{array}, x_u \in X_{unidir} \right\}$ []{#alg:reverse_fillet:flip_loop label="alg:reverse_fillet:flip_loop"} $X_{fillet} \leftarrow \left\{\begin{bmatrix} R_2^T x_{f,xy} + x_{2,xy} \\ x_{f,d} \end{bmatrix}, x_f \in X_{fillet}\right\}$ []{#alg:reverse_fillet:trans_back label="alg:reverse_fillet:trans_back"} $X_{fillet}$
:::
::::

:::: {#fig:rev_fill_demo .figure latex-placement="h"}
=\[circle,draw=black,fill=black,black,inner sep=2pt\]

:::: {#fig:rev_fill_demo:sub0 .figure}
::: caption
The four points that the fillet will be made between.
:::
::::

:::: {#fig:rev_fill_demo:sub1 .figure}
::: caption
The four points after they have been transformed.
:::
::::

:::: {#fig:rev_fill_demo:sub2 .figure}
::: caption
$_2x_3$ is flipped over the y-axis.
:::
::::

:::: {#fig:rev_fill_demo:sub3 .figure}
::: caption
The unidirectional fillet is generated.
:::
::::

:::: {#fig:rev_fill_demo:sub4 .figure}
::: caption
The second half of the unidirectional fillet is flipped to reverse it.
:::
::::

:::: {#fig:rev_fill_demo:sub5 .figure}
::: caption
The fillet is transformed back into the original coordinate frame.
:::
::::

::: caption
An illustration of the $ReverseFillet$ procedure.
:::
::::

Algorithm [\[alg:reverse_fillet\]](#alg:reverse_fillet){reference-type="ref" reference="alg:reverse_fillet"} gives the procedure for generating a reverse fillet and Figure [56](#fig:rev_fill_demo){reference-type="ref" reference="fig:rev_fill_demo"} illustrates the process. If the direction of travel for the two points being connected, $x_2$ and $x_3$, are the same then a normal fillet can be made to connect them, see lines [\[alg:reverse_fillet:normal_fillet\]](#alg:reverse_fillet:normal_fillet){reference-type="ref" reference="alg:reverse_fillet:normal_fillet"} and [\[alg:reverse_fillet:normal_fillet_dir\]](#alg:reverse_fillet:normal_fillet_dir){reference-type="ref" reference="alg:reverse_fillet:normal_fillet_dir"}. If the direction of travel changes, more logic is needed to make use of a unidirectional fillet primitive to make a fillet that changes direction. The process, shown on lines [\[alg:reverse_fillet:rot_mat\]](#alg:reverse_fillet:rot_mat){reference-type="ref" reference="alg:reverse_fillet:rot_mat"} through [\[alg:reverse_fillet:trans_back\]](#alg:reverse_fillet:trans_back){reference-type="ref" reference="alg:reverse_fillet:trans_back"}, involves flipping $x_3$ over the plane that intersects $x_2$ and is perpendicular to $\overline{x_1 x_2}$ to produce a new point, $x_{3f}$. An unidirectional fillet can be designed using $x_{3f}$. The fillet to execute is obtained by flipping the portion of the unidirectional fillet from $x_2$ to $x_{3f}$ back so that the path ends at $x_3$. The portion from $x_2$ to $x_{3}$ will then be executed in the opposite direction of that from $x_1$ to $x_2$.

First $x_0$, $x_1$, and $x_3$ are transformed into a coordinate frame with $x_2$ at the origin and $x_1$ on the x-axis, see lines [\[alg:reverse_fillet:rot_mat\]](#alg:reverse_fillet:rot_mat){reference-type="ref" reference="alg:reverse_fillet:rot_mat"} through [\[alg:reverse_fillet:end_frame_shift\]](#alg:reverse_fillet:end_frame_shift){reference-type="ref" reference="alg:reverse_fillet:end_frame_shift"} and Figure [51](#fig:rev_fill_demo:sub1){reference-type="ref" reference="fig:rev_fill_demo:sub1"}. This frame is defined to make flipping $x_3$ easier. The prescript $2$ is used to denote a point in this frame, i.e., $_2x_0$ is the point $x_{0,xy}$ in the new frame. On line [\[alg:reverse_fillet:flip_x3\]](#alg:reverse_fillet:flip_x3){reference-type="ref" reference="alg:reverse_fillet:flip_x3"}, $_2x_3$ is flipped across the y-axis, see Figure [52](#fig:rev_fill_demo:sub2){reference-type="ref" reference="fig:rev_fill_demo:sub2"}. The transformed set of points $_2x_{0}$, $_2x_{1}$, $_2x_2$, and $_{2}x_{3f}$ form a chain of nodes that do not change direction. Line [\[alg:reverse_fillet:forward_fill\]](#alg:reverse_fillet:forward_fill){reference-type="ref" reference="alg:reverse_fillet:forward_fill"} generates a unidirectional fillet called $X_{unidir}$ with these modified points, see Figure [53](#fig:rev_fill_demo:sub3){reference-type="ref" reference="fig:rev_fill_demo:sub3"}. Line [\[alg:reverse_fillet:flip_loop\]](#alg:reverse_fillet:flip_loop){reference-type="ref" reference="alg:reverse_fillet:flip_loop"} fills $X_{fillet}$ with a fillet that starts moving in the same direction at $x_2$ while the x component of $X_{unidir}$ is negative. When the x component of $X_{unidir}$ hits the y-axis the fillet switches to the direction of travel of $x_3$ and flips the fillet across the y-axis. The result is a fillet that comes to a point on the y-axis and switches direction at that point, see Figure [54](#fig:rev_fill_demo:sub4){reference-type="ref" reference="fig:rev_fill_demo:sub4"}. Line [\[alg:reverse_fillet:trans_back\]](#alg:reverse_fillet:trans_back){reference-type="ref" reference="alg:reverse_fillet:trans_back"} transforms fillet back to the original coordinate frame, as shown in Figure [55](#fig:rev_fill_demo:sub5){reference-type="ref" reference="fig:rev_fill_demo:sub5"}.

:::: {#fig:reverse_curvature_demo_world .figure latex-placement="h"}
::: caption
The resulting paths from running FB-RRT\* in an environment where the shortest path turns sharply down a corridor. Solutions from planning with arc-fillet paths are shown in blue. Solutions from planning with reverse-arc-fillet paths are shown in green when $d=1$, forward, and red when $d=-1$, reverse.
:::
::::

One scenario where the ability to plan forward and reverse fillets is beneficial is shown in Figure [57](#fig:reverse_curvature_demo_world){reference-type="ref" reference="fig:reverse_curvature_demo_world"}. Figure [57](#fig:reverse_curvature_demo_world){reference-type="ref" reference="fig:reverse_curvature_demo_world"} uses the same planning configuration as Figure [47](#fig:curvature_demo_world){reference-type="ref" reference="fig:curvature_demo_world"} from Section [6.4](#sec:curvature_constrained_paths){reference-type="ref" reference="sec:curvature_constrained_paths"}. The only difference between Figures [57](#fig:reverse_curvature_demo_world){reference-type="ref" reference="fig:reverse_curvature_demo_world"} and [47](#fig:curvature_demo_world){reference-type="ref" reference="fig:curvature_demo_world"} is that [57](#fig:reverse_curvature_demo_world){reference-type="ref" reference="fig:reverse_curvature_demo_world"} shows the result of path planning using the $ReverseFillet$ procedure in green and red instead of the solution found with straight-line primitives. The solution found from planning without the $ReverseFillet$ procedure is shown in blue. Both planners are using arc-fillets with the same maximum curvature constraint, but the red path makes use of the $ReverseFillet$ procedure.

As is described in Section [6.4](#sec:curvature_constrained_paths){reference-type="ref" reference="sec:curvature_constrained_paths"}, a path that goes through the narrow hallway cannot satisfy the curvature constraints of the problem without hitting walls when solely forward motion is considered. Figure [57](#fig:reverse_curvature_demo_world){reference-type="ref" reference="fig:reverse_curvature_demo_world"} shows that it is possible using the $ReverseFillet$ procedure. Following the green and red solution, generated with forward and reverse motion, the path turns partially into the narrow hallway. When it nears the wall, the path stops and continues the turn in reverse. The path follows the hallway in reverse until it gets to $X_t$. Without the functionality added with the $ReverseFillet$ procedure, the blue solution is unable to follow the hallway and instead must plan a significantly longer path that goes around the obstacles. Note that the inclusion of the reverse motion causes an increase in convergence time due to the added dimension in the sampling space. Future work could include methods to reduce this complexity and also to penalize long stretches of reverse motion.
:::::

[^1]: *In this work $\rho$ is held constant, but many RRT\* based algorithms vary $\rho$ [@Karaman2011].*

[^2]: In our implementation, $x_{r}$ is left out of the search in $Nearest$ and $Near$.
