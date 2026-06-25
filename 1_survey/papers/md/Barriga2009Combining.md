---
citation_key: Barriga2009Combining
arxiv_id: 0912.0266
arxiv_url: https://arxiv.org/abs/0912.0266
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:27:31Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
artificial intelligence; motion planning; RRT; Multi-stage; local search; greedy heuristics; probabilistic sampling;
:::

# Introduction

The *dynamic path-planning* problem consists in finding a suitable plan for each new configuration of the environment by recomputing a collision free path using the new information available at each time step [@Hwang92]. This kind of problem can be found for example by a robot trying to navigate through an area crowded with people, such as a shopping mall or supermarket. The problem has been addressed widely in its several flavors, such as cellular decomposition of the configuration space [@Stentz95], partial environmental knowledge [@Stentz94], high-dimensional configuration spaces [@Kavraki96] or planning with non-holonomic constraints [@Lavalle99]. However, simpler variations of this problem are complex enough that cannot be solved with deterministic techniques, and therefore they are worthy to study.

This paper is focused on finding and traversing a collision-free path in two dimensional space, for a holonomic robot [^1], without kinodynamic restrictions [^2], in two different scenarios:

- Dynamic environment: several unpredictably moving obstacles or adversaries.

- Partially known environment: some obstacles only become visible when approached by the robot.

Besides from one (or few) new obstacle(s) in the second scenario we assume that we have perfect information of the environment at all times.

We will focus on continuous space algorithms and won't consider algorithms that use discretized representations of the configuration space, such as D\* [@Stentz95], because for high dimensional problems, the configuration space becomes intractable in terms of both memory and computation time, and there is the extra difficulty of calculating the discretization size, trading off accuracy versus computational cost.

The offline RRT is efficient at finding solutions but they are far from being optimal, and must be post-processed for shortening, smoothing or other qualities that might be desirable in each particular problem. Furthermore, replanning RRTs are costly in terms of computation time, as well as evolutionary and cell-decomposition approaches. Therefore, the novelty of this work is the mixture of the feasibility benefits of the RRTs, the repairing capabilities of local search, and the computational inexpensiveness of greedy algorithms, into our lightweight multi-stage algorithm.

In the following sections, we present several path planning methods that can be applied to the problem described above. In section [2.1](#sec:RRT){reference-type="ref" reference="sec:RRT"} we review the basic offline, single-query RRT, a probabilistic method that builds a tree along the free configuration space until it reaches the goal state. Afterward, we introduce the most popular replanning variants of the RRT: ERRT in section [2.2](#sec:ERRT){reference-type="ref" reference="sec:ERRT"}, DRRT in section [2.3](#sec:DRRT){reference-type="ref" reference="sec:DRRT"} and MP-RRT in section [2.4](#sec:MPRRT){reference-type="ref" reference="sec:MPRRT"}. Then, in section [3](#sec:hillclimbing){reference-type="ref" reference="sec:hillclimbing"} we present our new hybrid multi-stage algorithm with the experimental results and comparisons in section [4](#sec:results){reference-type="ref" reference="sec:results"}. Finally, the conclusions and further work are discussed in section [5](#sec:conclusions){reference-type="ref" reference="sec:conclusions"}.

# Previous and Related Work {#sec:stateofart}

## Rapidly-Exploring Random Tree {#sec:RRT}

One of the most successful probabilistic sampling methods for offline path planning currently in use, is the Rapidly-exploring Random Tree (RRT), a single-query planner for static environments, first introduced in [@Lavalle98]. RRTs work towards finding a continuous path from a state $q_{init}$ to a state $q_{goal}$ in the free configuration space $C_{free}$, by building a tree rooted at $q_{init}$. A new state $q_{rand}$ is uniformly sampled at random from the configuration space $C$. Then the nearest node, $q_{near}$, in the tree is located, and if $q_{rand}$ and the shortest path from $q_{rand}$ to $q_{near}$ are in $C_{free}$, then $q_{rand}$ is added to the tree. The tree growth is stopped when a node is found near $q_{goal}$. To speed up convergence, the search is usually biased to $q_{goal}$ with a small probability.\
In [@Kuffner00], two new features are added to RRTs. First, the EXTEND function is introduced, which, instead of trying to add directly $q_{rand}$ to the tree, makes a motion towards $q_{rand}$ and tests for collisions.

Then a greedier approach is introduced, which repeats EXTEND until an obstacle is reached. This ensures that most of the time, we will be adding states to the tree, instead of just rejecting new random states. The second extension is the use of two trees, rooted at $q_{init}$ and $q_{goal}$, which are grown towards each other. This significantly decreases the time needed to find a path.

## ERRT {#sec:ERRT}

The execution extended RRT presented in [@Bruce02] introduces two RRTs extensions to build an on-line planner: the *waypoint cache* and the *adaptive cost penalty search*, which improves re-planning efficiency and the quality of generated paths. The waypoint cache is implemented by keeping a constant size array of states, and whenever a plan is found, all the states in the plan are placed in the cache with random replacement. Then, when the tree is no longer valid, a new tree must be grown, and there are three possibilities for choosing a new target state. With probability P\[*goal*\], the goal is chosen as the target; With probability P\[*waypoint*\], a random waypoint is chosen, and with remaining probability a uniform state is chosen as before. Values used in [@Bruce02] are P\[*goal*\]$=0.1$ and P\[*waypoint*\]$=0.6$.\
In the other extension --- the adaptive cost penalty search --- the planner dynamically modifies a parameter $\beta$ to help it finding shorter paths. A value of $1$ for $\beta$ will always extend from the root node, while a value of $0$ is equivalent to the original algorithm. Unfortunately, the solution presented in [@Bruce02] lacks of implementation details and experimental results on this extension.

## Dynamic RRT {#sec:DRRT}

The Dynamic Rapidly-exploring Random Tree (DRRT) described in [@Ferguson06] is a probabilistic analog to the widely used D\* family of algorithms. It works by growing a tree from $q_{goal}$ to $q_{init}$. The principal advantage is that the root of the tree does not have to be changed during the lifetime of the planning and execution. Also, in some problem classes the robot has limited range sensors, thus moving obstacles (or new ones) are typically near the robot and not near the goal. In general, this strategy attempts to trim smaller branches and farther away from the root. When new information concerning the configuration space is received, the algorithm removes the newly-invalid branches of the tree, and grows the remaining tree, focusing, with a certain probability(empirically tuned to $0.4$ in [@Ferguson06]) to a vicinity of the recently trimmed branches, by using the a similar structure to the waypoint cache of the ERRT. In experimental results DRRT vastly outperforms ERRT.

## MP-RRT {#sec:MPRRT}

The Multipartite RRT presented in [@Zucker07] is another RRT variant which supports planning in unknown or dynamic environments. The MP-RRT maintains a forest $F$ of disconnected sub-trees which lie in $C_{free}$, but which are not connected to the root node $q_{root}$ of $T$, the main tree. At the start of a given planning iteration, any nodes of $T$ and $F$ which are no longer valid are deleted, and any disconnected sub-trees which are created as a result are placed into $F$. With given probabilities, the algorithm tries to connect $T$ to a new random state, to the goal state, or to the root of a tree in $F$. In [@Zucker07], a simple greedy smoothing heuristic is used, that tries to shorten paths by skipping intermediate nodes. The MP-RRT is compared to an iterated RRT, ERRT and DRRT, in 2D, 3D and 4D problems, with and without smoothing. For most of the experiments, MP-RRT modestly outperforms the other algorithms, but in the 4D case with smoothing, the performance gap in favor of MP-RRT is much larger. The authors explained this fact due to MP-RRT being able to construct much more robust plans in the face of dynamic obstacle motion. Another algorithm that utilizes the concept of forests is the Reconfigurable Random Forests (RRF) presented in [@Li02], but without the success of MP-RRT.

# A Multi-stage Probabilistic Algorithm {#sec:hillclimbing}

In highly dynamic environments, with many (or a few but fast) relatively small moving obstacles, regrowing trees are pruned too fast, cutting away important parts of the trees before they can be replaced. This reduce dramatically the performance of the algorithms, making them unsuitable for these class of problems. We believe that a better performance could be obtained by slightly modifying a RRT solution using simple obstacle-avoidance operations on the new colliding points of the path by informed local search. Then, the path could be greedily optimized if the path has reached the feasibility condition.

## Problem Formulation

At each time-step, the proposed problem could be defined as an optimization problem with satisfiability constraints. Therefore, given a path our objective is to minimize an evaluation function (i.e. distance, time, or path-points), with the $C_{free}$ constraint. Formally, let the path $\rho=p_1p_2\ldots p_n$ a sequence of points, where $p_i \in \mathbb{R}^n$ a $n$-dimensional point ($p_1 = q_{init}, p_n = q_{goal}$), $O_t\in \mathcal{O}$ the set of obstacles positions at time $t$, and $eval:\mathbb{R}^n \times \mathcal{O} \mapsto \mathbb{R}$ an evaluation function of the path depending on the object positions. Then, our ideal objective is to obtain the optimum $\rho*$ path that minimize our $eval$ function within a feasibility restriction in the form

$$\begin{equation}
\displaystyle\rho*=arg\min_{\rho}[eval(\rho,O_t)]  \textrm{ with }  feas(\rho,O_t) = C_{free}
\label{eq:problem}
\end{equation}$$

where $feas(\cdot,\cdot)$ is a *feasibility* function that equals to $C_{free}$ iff the path $\rho$ is collision free for the obstacles $O_t$. For simplicity, we use very naive $eval(\cdot,\cdot)$ and $feas(\cdot,\cdot)$ functions, but this could be extended easily to more complex evaluation and feasibility functions. The used $feas(\rho,O_t)$ function assumes that the robot is a punctual object (dimensionless) in the space, and therefore, if all segments $\overrightarrow{p_i p_{i+1}}$ of the path do not collide with any object $o_j \in O_t$, we say that the path is in $C_{free}$. The $eval(\rho,O_t)$ function will be the length of the path, i.e. the sum of the distances between consecutive points. This could be easily changed to any metric such as the time it would take to traverse this path, accounting for smoothness, clearness or several other optimization criteria.

## A Multi-stage Probabilistic Strategy

If solving equation [\[eq:problem\]](#eq:problem){reference-type="ref" reference="eq:problem"} is not a simple task in static environments, solving dynamic versions turns out to be even more difficult. In dynamic path planning we cannot wait until reaching the optimal solution because we must deliver a "good enough" plan within some time quantum. Then, a heuristic approach must be developed to tackle the on-line nature of the problem. The heuristic algorithms presented in sections [2.2](#sec:ERRT){reference-type="ref" reference="sec:ERRT"}, [2.3](#sec:DRRT){reference-type="ref" reference="sec:DRRT"} and [2.4](#sec:MPRRT){reference-type="ref" reference="sec:MPRRT"}, extend a method developed for static environments, which produce a poor response to highly dynamic environments and an unwanted complexity of the algorithms.

We propose a multi-stage combination of three simple heuristic probabilistic techniques to solve each part of the problem: feasibility, initial solution and optimization.

::::: {#fig:diag .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/diag.png){width="50%"}
:::

::: {.caption short-caption="A Multi-stage Strategy for Dynamic Path Planning"}
**A Multi-stage Strategy for Dynamic Path Planning**. This figure describes the life-cycle of the multi-stage algorithm presented here. The RRT, informed local search, and greedy heuristic are combined to produce an expensiveness solution to the dynamic path planning problem.
:::
:::::

### Feasibility

The key point in this problem is the hard constraint in equation [\[eq:problem\]](#eq:problem){reference-type="ref" reference="eq:problem"} which must be met before even thinking about optimizing. The problem is that in highly dynamic environments a path turns rapidly from feasible to unfeasible --- and the other way around --- even if our path does not change. We propose a simple *informed local search* to obtain paths in $C_{free}$. The idea is to randomly search for a $C_{free}$ path by modifying the nearest colliding segment of the path. As we include in the search some knowledge of the problem, the *informed* term is coined to distinguish it from blind local search. The details of the operators used for the modification of the path are described in section [3.3](#sec:implementation){reference-type="ref" reference="sec:implementation"}.

### Initial Solution

The problem with local search algorithms is that they repair a solution that it is assumed to be near the feasibility condition. Trying to produce feasible paths from scratch with local search (or even with evolutionary algorithms [@Xiao97]) is not a good idea due the randomness of the initial solution. Therefore, we propose feeding the informed local search with a *standard RRT* solution at the start of the planning, as can be seen in figure [1](#fig:diag){reference-type="ref" reference="fig:diag"}.

### Optimization

Without an optimization criteria, the path could grow infinitely large in time or size. Therefore, the $eval(\cdot,\cdot)$ function must be minimized when a (temporary) feasible path is obtained. A simple *greedy* technique is used here: we test each point in the solution to check if it can be removed maintaining feasibility, if so, we remove it and check the following point, continuing until reaching the last one.

## Algorithm Implementation {#sec:implementation}

::::: {#alg:main .figure latex-placement="ht"}
::: algorithmic
$q_{robot} \leftarrow$ is the current robot position $q_{goal} \leftarrow$ is the goal position $(time)$ $(time)$
:::

::: caption
**Main()**
:::
:::::

The multi-stage algorithm proposed in this paper works by alternating environment updates and path planning, as can be seen in Algorithm [2](#alg:main){reference-type="ref" reference="alg:main"}. The first stage of the path planning (see Algorithm [3](#alg:process){reference-type="ref" reference="alg:process"}) is to find an initial path using a RRT technique, ignoring any cuts that might happen during environment updates. Thus, the RRT ensures that the path found does not collide with static obstacles, but might collide with dynamic obstacles in the future. When a first path is found, the navigation is done by alternating a simple informed local search and a simple greedy heuristic as is shown in Figure [1](#fig:diag){reference-type="ref" reference="fig:diag"}.

::::: {#alg:process .figure latex-placement="ht"}
::: algorithmic
$q_{robot} \leftarrow$ is the current robot position $q_{start} \leftarrow$ is the starting position $q_{goal} \leftarrow$ is the goal position $T_{init} \leftarrow$ is the tree rooted at the robot position $T_{goal} \leftarrow$ is the tree rooted at the goal position $path \leftarrow$ is the path extracted from the merged RRTs $q_{robot} \leftarrow q_{start}$ $T_{init}.init(q_{robot})$ $T_{goal}.init(q_{goal})$ $(T_{init},T_{goal})$ firstCol $\leftarrow$ collision point closest to robot arc$(path, firstCol)$ mut$(path, firstCol)$ $(path)$
:::

::: caption
**process$(time)$**
:::
:::::

::::: {#fig:arc .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/arc.png){width="45%"}
:::

::: {.caption short-caption="The arc operator"}
**The arc operator**. This operator draws an offset value $\Delta$ over a fixed interval called vicinity. Then, one of the two axises is selected to perform the arc and two new consecutive points are added to the path. $n_1$ is placed at a $\pm \Delta$ of the point $b$ and $n_2$ at $\pm \Delta$ of point $c$, both of them over the same selected axis. The axis, sign and value of $\Delta$ are chosen randomly from an uniform distribution.
:::
:::::

::::: {#fig:mut .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/mut.png){width="45%"}
:::

::: {.caption short-caption="The mutation operator"}
**The mutation operator**. This operator draws two offset values $\Delta_x$ and $\Delta_y$ over a vicinity region. Then the same point $b$ is moved in both axises from $b=[b_x,b_y]$ to $b'=[b_x \pm \Delta_x, b_y\pm \Delta_y]$, where the sign and offset values are chosen randomly from an uniform distribution.
:::
:::::

The second stage is the informed local search, which is a two step function composed by the *arc* and *mutate* operators (Algorithms [6](#alg:arc){reference-type="ref" reference="alg:arc"} and [7](#alg:mut){reference-type="ref" reference="alg:mut"}). The first one tries to build a square arc around an obstacle, by inserting two new points between two points in the path that form a segment colliding with an obstacle, as is shown in Figure [4](#fig:arc){reference-type="ref" reference="fig:arc"}. The second step in the function is a mutation operator that moves a point close to an obstacle to a random point in the vicinity, as is graphically explained in Figure [5](#fig:mut){reference-type="ref" reference="fig:mut"}. The mutation operator is inspired by the ones used in the Adaptive Evolutionary Planner/Navigator(EP/N) presented in [@Xiao97], while the arc operator is derived from the arc operator in the Evolutionary Algorithm presented in [@Alfaro05].\
Even though the local search usually produce good results for minor changes in the environment, it does not when is faced to significant changes and is quite prone to getting stuck in an obstacle. To overcome this limitation, our algorithm recognizes this situation, and restarts an RRT from the current location, before continuing with the navigation phase.

::::: {#alg:arc .figure latex-placement="ht"}
::: algorithmic
vicinity $\leftarrow$ some vicinity size randDev $\leftarrow$ random$(-vicinity, vicinity)$ point1 $\leftarrow$ path\[firstCol\] point2 $\leftarrow$ path\[firstCol+1\] newPoint1 $\leftarrow$ (point1\[X\]+randDev,point1\[Y\]) newPoint2 $\leftarrow$ (point2\[X\]+randDev,point2\[Y\]) newPoint1 $\leftarrow$ (point1\[X\],point1\[Y\]+randDev) newPoint2 $\leftarrow$ (point2\[X\],point2\[Y\]+randDev) add new points between point1 and point2 drop new point2
:::

::: caption
**arc$(path, firstCol)$**
:::
:::::

::::: {#alg:mut .figure latex-placement="ht"}
::: algorithmic
vicinity $\leftarrow$ some vicinity size path\[firstCol\]\[X\] $+=$ random$(-vicinity, vicinity)$ path\[firstCol\]\[Y\] $+=$ random$(-vicinity, vicinity)$ accept new point reject new point
:::

::: caption
**mut$(path, firstCol)$**
:::
:::::

The third and last stage is the greedy optimization heuristic, which can be seen as a post-processing for path shortening, that eliminates intermediate nodes if doing so does not create collisions, as is described in the Algorithm [8](#alg:postProcess){reference-type="ref" reference="alg:postProcess"}.

::::: {#alg:postProcess .figure latex-placement="ht"}
::: algorithmic
i $\leftarrow$ 0 delete path\[i+1\] i $\leftarrow$ i+1
:::

::: caption
**postProcess$(path)$**
:::
:::::

# Experiments and Results {#sec:results}

The multi-stage strategy proposed here has been developed to navigate highly-dynamic environments, and therefore, our experiments should be aimed towards that purpose. Therefore, we have tested our algorithm in a highly-dynamic situation on two maps, shown in figures [9](#fig:office-dynamic){reference-type="ref" reference="fig:office-dynamic"} and [10](#fig:800-dynamic){reference-type="ref" reference="fig:800-dynamic"}. For completeness sake, we have tested on the same two maps, but modified to be a partially known environment. Also, we have ran the DRRT and MP-RRT algorithms over the same situations in order to compare the performance of our proposal.

## Experimental Setup

The first environment for our experiments consists on two maps with 30 moving obstacles the same size of the robot, with a random speed between 10% and 55% the speed of the robot. This *dynamic environments* are shown in figures [9](#fig:office-dynamic){reference-type="ref" reference="fig:office-dynamic"} and [10](#fig:800-dynamic){reference-type="ref" reference="fig:800-dynamic"}.\

::::: {#fig:office-dynamic .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/office-dynamic.png){width="45%"}
:::

::: caption
The dynamic environment, Map 1. The *green* square is our robot, currently at the start position. The *blue* squares are the moving obstacles. The *blue* cross is the goal.
:::
:::::

::::: {#fig:800-dynamic .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/800-dynamic.png){width="45%"}
:::

::: caption
The dynamic environment, Map 2. The *green* square is our robot, currently at the start position. The *blue* squares are the moving obstacles. The *blue* cross is the goal.
:::
:::::

The second environment uses the same maps, but with a few obstacles, three to four times the size of the robot, that become visible when the robot approaches each one of them. This *partially known environments* are shown in figure [11](#fig:office-partial){reference-type="ref" reference="fig:office-partial"} and [12](#fig:800-partial){reference-type="ref" reference="fig:800-partial"}.\

::::: {#fig:office-partial .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/office-partial.png){width="45%"}
:::

::: caption
The partially know environment, Map 1. The *green* square is our robot, currently at the start position. The *yellow* squares are the suddenly appearing obstacles. The *blue* cross is the goal.
:::
:::::

::::: {#fig:800-partial .figure latex-placement="ht"}
::: center
![](Barriga2009Combining_figs/800-partial.png){width="45%"}
:::

::: caption
The partially know environment, Map 2. The *green* square is our robot, currently at the start position. The *yellow* squares are the suddenly appearing obstacles. The *blue* cross is the goal.
:::
:::::

The three algorithms were ran a hundred times in each environment. The cutoff time was five minutes for all tests, after which, the robot was considered not to have reached the goal. Results are presented concerning:

- *success rate:* the percentage of times the robot arrived to the goal

- *number of nearest neighbor lookups performed by each algorithm(N.N.):* one of the possible bottlenecks for tree-based algorithms

- *number of collision checks performed(C.C.),* which in our specific implementation takes a significant percentage of the running time

- *time* it took the robot to reach the goal

## Implementation Details

The algorithms where implemented in C++ using a framework [^3] developed by the same authors.\
There are several variations that can be found in the literature when implementing RRTs. For all our RRT variants, the following are the details on where we departed from the basics:

- We always use two trees rooted at $q_{init}$ and $q_{goal}$.

- Our EXTEND function, if the point cannot be added without collisions to a tree, adds the mid point between the nearest tree node and the nearest collision point to it.

- In each iteration, we try to add the new randomly generated point to both trees, and if successful in both, the trees are merged, as proposed in [@Kuffner00].

- We found that there are significant performance differences with allowing or not the robot to advance towards the node nearest to the goal when the trees are disconnected, as proposed in [@Zucker07]. The problem is that the robot would become stuck if it enters a small concave zone of the environment(like a room in a building) while there are moving obstacles inside that zone, but otherwise it can lead to better performance. Therefore we present results for both kinds of behavior: DRRT-adv and MPRRT-adv, moves even when the trees are disconnected, while DRRT-noadv and MPRRT-noadv only moves when the trees are connected.

In MP-RRT, the forest was handled simply replacing the oldest tree in it if the forest had reached the maximum size allowed.

Concerning the parameter selection, the probability for selecting a point in the vicinity of a point in the waypoint cache in DRRT was set to 0.4 as suggested in [@Ferguson06]. The probability for trying to reuse a sub tree in MP-RRT was set to 0.1 as suggested in [@Zucker07]. Also, the forest size was set to 25 and the minimum size of a tree to be saved in the forest was set to 5 nodes.

## Dynamic Environment Results

The results in tables [1](#table:dynamic1){reference-type="ref" reference="table:dynamic1"} and [2](#table:dynamic2){reference-type="ref" reference="table:dynamic2"} show that it takes our algorithm considerably less time than it takes the DRRT and MP-RRT to get to the goal, with far less collision checks. It was expected that nearest neighbor lookups would be much lower in the multi-stage algorithm than in the other two, because they are only performed in the initial phase, not during navigation.

::: {#table:dynamic1}
    Algorithm     Success %    C.C.    N.N.   Time\[s\]
  -------------- ----------- -------- ------ -----------
   Multi-stage       99       23502    1122     6.62
    DRRT-noadv       100      91644    4609     20.57
     DRRT-adv        98       107225   5961     23.72
   MP-RRT-noadv      100      97228    4563     22.18
    MP-RRT-adv       94       118799   6223     26.86

  : Dynamic Environment Results, Map 1.
:::

::: {#table:dynamic2}
    Algorithm     Success %    C.C.    N.N.   Time\[s\]
  -------------- ----------- -------- ------ -----------
   Multi-stage       100      10318    563      8.05
    DRRT-noadv       99       134091   4134     69.32
     DRRT-adv        100      34051    2090     18.94
   MP-RRT-noadv      100      122964   4811     67.26
    MP-RRT-adv       100      25837    2138     16.34

  : Dynamic Environment Results, Map 2.
:::

## Partially Known Environment Results

The results in tables [3](#table:partial1){reference-type="ref" reference="table:partial1"} and [4](#table:partial2){reference-type="ref" reference="table:partial2"} show that our multi-stage algorithm, although designed for dynamic environments, is also faster than the other two in a partially known environment, though not as much as in the previous cases.

::: {#table:partial1}
    Algorithm     Success %   C.C.    N.N.   Time\[s\]
  -------------- ----------- ------- ------ -----------
   Multi-stage       100      12204   1225     7.96
    DRRT-noadv       100      37618   1212     11.66
     DRRT-adv        99       12131   967      8.26
   MP-RRT-noadv      99       49156   1336     13.82
    MP-RRT-adv       97       26565   1117     11.12

  : Partially Known Environment Results, Map 1.
:::

::: {#table:partial2}
    Algorithm     Success %   C.C.    N.N.   Time\[s\]
  -------------- ----------- ------- ------ -----------
   Multi-stage       100      12388   1613     17.66
    DRRT-noadv       99       54159   1281     32.67
     DRRT-adv        100      53180   1612     32.54
   MP-RRT-noadv      100      48289   1607     30.64
    MP-RRT-adv       100      38901   1704     25.71

  : Partially Known Environment Results, Map 2.
:::

# Conclusions {#sec:conclusions}

The new multi-stage algorithm proposed here has a very good performance in very dynamic environments. It behaves particularly well when several small obstacles are moving around seemingly randomly. This is explained by the fact that if the obstacles are constantly moving, they will sometimes move out of the way by themselves, which our algorithm takes advantage of, but the RRT based ones do not, they just drop branches of the tree, that could have been useful again just a few moments later.\
In partially known environments the multi-stage algorithm outperforms the RRT variants, but the difference is not as much as in dynamic environments.

## Future Work

There are several areas of improvement for the work presented in this paper. The most promising seems to be to experiment with different on-line planners such as the EP/N presented in [@Xiao97], a version of the EvP([@Alfaro05] and [@Alfaro08]) modified to work in continuous configuration space or a potential field navigator. Also, the local search presented here, could benefit from the use of more sophisticated operators.

Another area of research that could be tackled is extending this algorithm to other types of environments, ranging from totally known and very dynamic, to static partially known or unknown environments. An extension to higher dimensional problems would be one logical way to go, as RRTs are know to work well in higher dimensions.

Finally, as RRTs are suitable for kinodynamic planning, we only need to adapt the on-line stage of the algorithm to have a new multi-stage planner for problem with kinodynamic constraints.

[^1]: A holonomic robot is a robot in which the controllable degrees of freedom is equal to the total degrees of freedom.

[^2]: Kinodynamic planning is a problem in which velocity and acceleration bounds must be satisfied

[^3]: MoPa homepage: https://csrg.inf.utfsm.cl/twiki4/bin/view/CSRG/MoPa
