---
citation_key: Guo2023Efficient
arxiv_id: 2306.14409
arxiv_url: https://arxiv.org/abs/2306.14409
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:59:46Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

We study the *labeled* Multi-Robot Motion Planning ([MRPP]{.smallcaps}) problem under a graph-theoretic setting, also known as Multi-Agent Path Finding (MAPF). The basic objective of [MRPP]{.smallcaps} is to find a set of collision-free paths to route multiple robots from a start configuration to a goal configuration. In practice, solution optimality is also of key importance; yet optimally solving [MRPP]{.smallcaps} in terms of makespan and sum-of-cost is generally NP-hard [@YuLav13AAAI; @Sur10; @Yu2015IntractabilityPlanar]. [MRPP]{.smallcaps} algorithms find many important large-scale applications, including, e.g., in warehouse automation for general order fulfillment [@wurman2008coordinating], grocery order fulfillment [@mason2019developing], and parcel sorting [@wan2018lifelong]. Other application scenarios include formation reconfiguration [@PodSuk04], agriculture [@cheein2013agricultural], object transportation [@RusDonJen95], swarm robotics [@preiss2017crazyswarm].

Given the potential of employing its solutions in a wide range of impactful applications, even though [MRPP]{.smallcaps} had been studied since the 1980s in the robotics domain [@KorMilSpi84; @ErdLoz86; @LavHut98b; @GuoPar02], it remains a highly active research topic. Many effective algorithms, for example [@YuLav16TRO; @boyarski2015icbs; @cohen2016improved], have been proposed recently that balance fairly well between computational efficiency and solution optimality. Existing [MRPP]{.smallcaps} algorithms have been tested on randomly generated instances and yield decent performance for instances with relatively limited robot-robot interactions, i.e., either the number of robots is limited, or the density of robots is relatively low. However, they frequently fail in instances that are both large and dense.

::::: {#fig:dense_example .figure latex-placement="t"}
::: overpic
./figures/dense_ins.pdf (12.5, 36.5) (a) (47.5,36.5) (b) (82.5, 36.5) (c) (20.5, -3) (d) (75.5, -3) (e)
:::

::: caption
(a)-(c) A challenging *locally-dense* [MRPP]{.smallcaps} example on $20\times 20$ map with 49 robots. It requires rearranging the robots from the start configuration (a) to the goal configuration (c). By "sparsifying" the configuration using our methods, as shown in an intermediate step (b), the problem can be solved quickly with decent solution optimality. (d)-(e) A challenging *globally-dense* [MRPP]{.smallcaps} example on a $24\times 18$ warehouse map with 203 robots. In both settings, each robot has a unique start and goal.
:::
:::::

Recently, [MRPP]{.smallcaps} algorithms have been applied in high-density applications, such as autonomous vehicle parking systems [@Guo2023TowardEP; @okoso2022high], to increase space utilization efficiency. In such dense scenarios, robots' motions are strongly correlated and may block the paths of each other, which makes the problem extremely difficult for existing [MRPP]{.smallcaps} solvers.

**Results and contributions.** This research proposes efficient heuristics and uses them to build complete solvers for tackling dense and difficult [MRPP]{.smallcaps} instances. We address two classes of dense [MRPP]{.smallcaps}: *globally* dense instances where the number of robots is large with high average robot density (more than $40\%$, see Fig. [1](#fig:dense_example){reference-type="ref" reference="fig:dense_example"}(c)), and *locally* dense instances where the robot distribution is unbalanced with high local robot density (i.e. $100\%$, see Fig. [1](#fig:dense_example){reference-type="ref" reference="fig:dense_example"}(a)-(b)).

We develop two hybrid [MRPP]{.smallcaps} algorithms to address the above-mentioned challenges. In the first algorithm, we introduce a (motion-primitive) database-based conflict resolution mechanism inspired by [@han2019ddm] to augment a conflict-based search [@sharon2015conflict]. We also design a set of rules to maintain the solution quality as well as the completeness of the resulting algorithm. We call the algorithm [DCBS]{.smallcaps}, standing for *database-accelerated enhanced conflict-based search*.

While our first algorithm works for both globally dense and locally dense scenarios, our second algorithm is designed specifically for locally dense instances. Inspired by [@guo2022sub], we first convert the challenging configuration to a *sparsified* configuration, which is relatively easier to solve, using *unlabeled* [MRPP]{.smallcaps} planning solutions. To reduce the extra overhead of the conversion, we adopt a best-first heuristic for finding a proper sparsified configuration and a path refinement technique for better concatenating the intermediate paths. We call the second algorithm [SCBS]{.smallcaps}, standing for *sparsified enhanced conflict-based search*.

Experiments on diverse environment maps demonstrate the effectiveness of our proposed methods in solving instances with robot densities greater than $60\%$-$70\%$ with a high success rate and decent levels of solution quality. [DCBS]{.smallcaps} and [SCBS]{.smallcaps} outperform previous [MRPP]{.smallcaps} algorithms in terms of combined speed and solution quality.

**Organization.** The rest of the paper is organized as follows. Sec. [3](#sec:problem){reference-type="ref" reference="sec:problem"} covers the preliminaries, including the problem formulation and two suboptimal algorithms [ECBS]{.smallcaps} and [DDM]{.smallcaps}. In Sec. [5](#sec:algo-trans){reference-type="ref" reference="sec:algo-trans"}-Sec. [4](#sec:algo-ddecbs){reference-type="ref" reference="sec:algo-ddecbs"}, we describe our heuristics and algorithms for solving dense [MRPP]{.smallcaps}. We perform thorough evaluations and discussions of the proposed algorithms in Sec. [6](#sec:evaluation){reference-type="ref" reference="sec:evaluation"} and conclude with Sec. [7](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}.

# Related Research

[MRPP]{.smallcaps}/MAPF has been widely studied in the field of robotics. In the static or one-shot setting [@stern2019multi], given a graph environment and a number of robots with each robot having a unique start position and a goal position, the task is to find collision-free paths for all the robots from start to goal. It has been proven that solving one-shot [MRPP]{.smallcaps} optimally in terms of minimizing either makespan or sum of costs is NP-hard [@surynek2010optimization; @yu2013structure]. Moreover, it is also NP-hard to approximate within any constant factor less than 4/3 if the solution makespan is to be minimized [@ma2016multi].

Existing solvers for [MRPP]{.smallcaps} can be broadly categorized into *reduction-based*, *search-based*, and *rule-based*.

Reduction-based solvers reduce [MRPP]{.smallcaps} to other well-studied problems, such as ILP[@yu2016optimal], SAT[@surynek2010optimization] and ASP[@erdem2013general]. These solvers are able to find optimal solutions and are efficient for small and dense instances. There are dividing-and-conquer heuristics for enhancing their scalability [@guo2021spatial; @yu2016optimal] at the cost of optimality. Unfortunately, these reduction-based methods are still incapable of dealing with the extremely dense scenarios we study in this paper.

Another more popular approach develops search-based algorithms for [MRPP]{.smallcaps} problems that can be viewed are high-sophisticated A\* [@hart1968formal] variants. Coupled A\* [@silver2005cooperative], ICTS [@sharon2013increasing], and CBS [@sharon2015conflict] are optimal solvers and efficient on large maps but with sparse robots. ECBS [@barer2014suboptimal] is the bounded-suboptimal version of CBS with enhanced scalability and bounded suboptimality. The search-based algorithms rely heavily on the heuristic for reducing the number of node expansions, i.e., Number Of Conflicts ([NOC]{.smallcaps}) which is used in [ECBS]{.smallcaps}. In dense scenarios, since robots are strongly correlated, this heuristic is not enough since there are lots of nodes with the same [NOC]{.smallcaps}. As a result, the number of nodes needed to expand to find a solution for existing [CBS]{.smallcaps} variants grows exponentially with respect to the robot density, even if there is only a small number of robots.

Rule-based solvers are another class of suboptimal [MRPP]{.smallcaps} solvers. Prioritized planners [@silver2005cooperative; @okumura2019priority] assign priorities to robots and low-priority robots avoid conflicts with high-priority robots by treating them as dynamic obstacles. This is efficient but can easily cause dead-lock issues in dense scenarios, which leads to a low success rate. Another class of rule-based solvers introduces motion primitives for swapping the position of robots, such as Push-And-Swap [@luna2011push] and Rubik Table [@szegedy2020rearrangement; @guo2022sub; @GuoFenYu22IROS]. They are polynomial-time algorithms and can even solve extremely dense instances, but the solution quality is far from optimal. DDM[@han2019ddm] resolves the inter-robot conflicts efficiently by utilizing the precomputed motion primitive within the $3\times 3$ sub-grid. It finds near-optimal solutions when the robot density is not high but has the same optimality issue in dense scenarios.

# Preliminaries {#sec:problem}

## Multi-Robot Path Planning on Graphs

A graph-based Multi-Robot Path Planning ([MRPP]{.smallcaps}) problem is defined on a graph $\mathcal{G} = (\mathcal{V},\mathcal{ E})$. We assume that $\mathcal{G}$ is a grid graph. That is, given integers $w$ and $h$ as the graph's *width* and *height*, the vertex set can be represented as $\mathcal{V} \subseteq \{(i, j) \mid 1 \leq i \leq w, 1 \leq j \leq h,i\in \mathbb{Z},j\in \mathbb{Z}\}$. The graph is $4$-way connected, i.e., for a vertex $v = (i, j)$, the set of its neighboring vertices are defined as $\mathcal{N}(v) = \{(i + 1, j),(i - 1, j),(i, j + 1),(i, j - 1)\} \bigcap \mathcal{V}$. The problem involves $n$ robots $r_1, \dots, r_n$, where each robot $r_i$ has a unique start state $s_i \in \mathcal{V}$ and a unique goal state $g_i \in \mathcal{V}$. We denote the joint start configuration as $X_S = \{s_1, \dots, s_n\}$ and the goal configuration as $X_G = \{g_1, \dots, g_n\}$.

The objective of [MRPP]{.smallcaps} is to find a set of feasible paths for all robots. Here, a *path* for robot $r_i$ is defined as a sequence of $T + 1$ vertices $P_i = (p_i^0, \dots, p_i^T)$ that satisfies: (i) $p_i^0 = s_i$; (ii) $p_i^T = g_i$; (iii) $\forall 1 \leq t \leq T, p_i^{t - 1} \in N(p_i^t)$. Apart from the feasibility of each individual path, for $P$ to be collision(conflict)-free , $\forall 1 \leq t \leq T, 1 \leq i < j \leq n$, $P_i, P_j$ must satisfy

1.  There is no *vertex collision*: $p_i^t \neq p_j^t$;

2.  There is no *edge collision*: $(p_i^{t - 1}, p_i^t) \neq (p_j^t, p_j^{t - 1})$.

and the following criteria are used to evaluate solution quality:

1.  Makespan ([MKPN]{.smallcaps}): the time required to move all robots to their desired positions;

2.  Sum-of-cost ([SOC]{.smallcaps}): the cumulative cost function that sums over all robots of the number of time steps required to reach the goals. For each robot, denoting $t_i$ such that $\forall t_i \leq t \leq T, p_i^t = g_i$, the sum-of-costs objective is calculated as $\min \sum_{1 \leq i \leq n} t_i$.

In general, these two objectives create a Pareto front [@yu2013structure], and it is not always possible to simultaneously optimize these objectives.

## Enhanced Conflict Based Search (ECBS)

[ECBS]{.smallcaps}($w_1$)[@barer2014suboptimal] is a variant of CBS [@sharon2015conflict] that is $w_1$-suboptimal, which employs the focal search method [@pearl1982studies] in both its high-level and low-level searches rather than best-first searches.

A focal search, like A\*, uses an OPEN list whose nodes $n$ are sorted in increasing order of their $f$-values $f(n)=g(n)+h(n)$, where $h(n)$ are the primary heuristic values. Unlike A\*, a focal search with suboptimality factor $w_1$ also uses a FOCAL list of all nodes currently in the OPEN list whose $f$-values are no larger than $w_1$ times the currently smallest $f$-value in the OPEN list. The nodes in the FOCAL list are sorted in increasing order of their secondary heuristic values. A\* expands a node in the OPEN list with the smallest $f$-value, but a focal search expands a node in the FOCAL list instead with the smallest secondary heuristic value. Thus, the secondary heuristic values should favor a node in the FOCAL list close to a goal node to speed up the search and thus exploit the leeway afforded by $w_1$ that A\* does not have available. If the primary heuristic values are admissible, then a focal search is $w_1$-suboptimal. The secondary heuristic values can be inadmissible.

The high-level and low-level searches of ECBS($w_1$) are both focal searches. During the generation of a high-level node $N$, ECBS($w_1$) performs a low-level focal search with OPEN list $\text{OPEN}_i(N)$ and FOCAL list $\text{FOCAL}_i(N)$ for the robot $i$ affected by the added constraint. The number of collisions([NOC]{.smallcaps}) is used as the secondary heuristic value for the high-level and low-level searches, allowing ECBS ($w_1$) to generate high-level nodes with fewer collisions compared to CBS, which improves its efficiency. However, the path costs can become large for ECBS($w_1$) with large values of $w_1$ due to the larger leeway afforded by $w_1$. The robots might move around in wiggly lines, increasing the chance of collisions, thus increasing the number of collisions in the high-level and low-level nodes of ECBS($w_1$) and slowing it down. Thus, larger values of $w_1$ do not necessarily entail smaller runtimes of ECBS($w_1$). In this paper, the [SOC]{.smallcaps} suboptimality bound is chosen to be $w_1=1.5$, which is a good choice according to the original paper[@barer2014suboptimal].

## DDM

[DDM]{.smallcaps} [@barer2014suboptimal], standing for ***d**iversified path and **d**atabase-driven **m**ulti-robot path planner*, is a fast suboptimal [MRPP]{.smallcaps} solver. It first generates a shortest path between each pair of start and goal vertices and then resolves local conflicts among the initial paths. In generating the initial paths, a path diversification heuristic is introduced that attempts to make the path ensemble use all graph vertices in a balanced manner, which minimizes the chance that many robots aggregate in certain local areas, causing unwanted congestion, in order to reduce the number of conflicts of the initial paths.

Then, in resolving the path conflicts, a database resolution heuristic is introduced, which builds a min-makespan solution database for all $2\times 3$ and $3\times3$ sub-problems and ensures quick local conflict resolution via database retrievals. Specifically, for each conflicting robot pair in each step, [DDM]{.smallcaps} tries to find a $2\times 3$ or $3\times 3$ subgraph that contains these robots. Temporary goals are assigned to the robots within the subgraph to resolve the conflict. The paths for routing them to the temporary goals can be obtained easily by accessing the precomputed database. Obviously, each time resolving a conflict using subgraphs will introduce an extra overhead to the paths' length. In dense environments, the number of conflicts needed to resolve is high, and as a result, [DDM]{.smallcaps} can be very suboptimal under these scenarios.

# Database Conflict Resolution in [ECBS]{.smallcaps} {#sec:algo-ddecbs}

Dense instances are challenging for [ECBS]{.smallcaps} to solve. Fig. [2](#fig:stuck_example){reference-type="ref" reference="fig:stuck_example"} shows an example of applying [ECBS]{.smallcaps} to solve a dense instance in $20\times 20$ that has 272 robots with random starts and goals. The [NOC]{.smallcaps} decreases as the number of iterations of high-level expansion increases.

When robot density is not very high, every time a constraint is added to a high-level node, it will lead to the [NOC]{.smallcaps} decreasing by at least one. Meanwhile, the [NOC]{.smallcaps} of the initial node is not very large for sparse instances. Therefore, [ECBS]{.smallcaps} finds a conflict-free solution efficiently when robot density is not very high. However, when robot density is high, the [NOC]{.smallcaps} will be stuck at some non-zero point. This is because robots' interactions are strongly correlated in high-density settings. Adding one constraint to resolve a given conflict may cause the low-level planner to find a path conflicting with another robot. As a result, the [NOC]{.smallcaps} does not decrease and there would be a large number of nodes with the same [NOC]{.smallcaps} in the OPEN list. The stagnation of [NOC]{.smallcaps} will continue for a long period of high-level expansion until it accidentally expands the correct node. Even worse, it is possible that [ECBS]{.smallcaps} cannot find a feasible solution after expanding all the nodes with the stagnated [NOC]{.smallcaps} in the current OPEN list and it needs to expand nodes with higher [NOC]{.smallcaps}, which makes [ECBS]{.smallcaps} very inefficient.

:::: {#fig:stuck_example .figure latex-placement="!htbp"}
![](Guo2023Efficient_figs/ecbs_stuck.png){width="\\linewidth"}

::: caption
Left: Number of iterations to enter [NOC]{.smallcaps} stagnation on 10 random instances on $20\times 20$ map with 272 robots. Right: An example of [NOC]{.smallcaps} stagnation phenomenon when applying [ECBS]{.smallcaps} to solve a dense instance in $20\times 20$ map with 272 robots.
:::
::::

To address the issue, we propose *database-accelerated enhanced conflict-based search* ([DCBS]{.smallcaps}) (Alg. [\[alg:decbs\]](#alg:decbs){reference-type="ref" reference="alg:decbs"}), which introduces a database-driven conflict resolution mechanism into [ECBS]{.smallcaps} to speed up the high-level expansion and circumvent the [NOC]{.smallcaps} stagnation. [DCBS]{.smallcaps} expands the high-level nodes regularly as [ECBS]{.smallcaps} does initially. When the [NOC]{.smallcaps} of the node to expand drops to a specific point, the database conflict resolution mechanism is triggered and is applied to that node (Line 7). The paths of the current node are used as the initial paths for conflict resolution. We apply the database heuristics to resolve all the conflicts in the paths, in a local $2\times 3$ sub-graph or $3\times 3$ sub-graph. There is the possibility that we cannot find a sub-graph for a pair of conflicting robots if the map is not a low-resolution graph [@han2019ddm].

When we could not resolve the conflicts, we return to the [ECBS]{.smallcaps} high-level expansion routine and continue to use focal search in the low level to resolve the conflicts. If $\texttt{DbResolution}$ succeeds in finding a solution, to ensure the solution quality, we check if the [MKPN]{.smallcaps}([SOC]{.smallcaps}) suboptimality ratio of paths is within the bound of $w_2$, where $w_2>w_1$ is another user-defined suboptimality bound. When the solution, after resolving all the conflicts using database heuristics satisfies the optimality need, we return the solution. Otherwise, we continue the [ECBS]{.smallcaps} high-level expansion.

:::: algorithm
::: small
$\text{Root}\leftarrow$`InitializeRoot()` $\text{OPEN}.push(\text{Root})$
:::
::::

Because [DCBS]{.smallcaps} preserves the general structure of [ECBS]{.smallcaps}, the bounded-suboptimality guarantee of [ECBS]{.smallcaps} is inherited.

::: proposition
**Proposition 1**. *[DCBS]{.smallcaps} is complete and $w_2$ bounded-suboptimal.*
:::

To make [DCBS]{.smallcaps} efficient, we observe that we must pay careful attention to a few key points. First, we must choose the right time to trigger the database-driven conflict resolution. Second, the [NOC]{.smallcaps} of the node should drop as quickly as possible and enter the [NOC]{.smallcaps} stagnation state as fast as possible. For example, in Fig. [2](#fig:stuck_example){reference-type="ref" reference="fig:stuck_example"}, the blue curve is better than the yellow curve for [DCBS]{.smallcaps} since it "converges\" to the stagnation point in a much shorter time. Third, if we want a suboptimality guarantee at some desired level, $\omega_2$ should be also carefully chosen to balance runtime and optimality. We certainly hope that the [NOC]{.smallcaps} of the node to apply database conflict resolution is small enough. Otherwise, if the node still contains a lot of conflicts, the resulting paths would be very sub-optimal. On the other hand, in dense scenarios, if the desired [NOC]{.smallcaps} is too small, it might take a very long time for the [NOC]{.smallcaps} of the node to drop to this value.

Based on the observations above, we introduce several additional techniques to enhance the performance of [DCBS]{.smallcaps}. We first apply a DFS-like expansion mechanism to speed up the [NOC]{.smallcaps} descent. The high level is a best-first search which always first expands the node with the smallest [NOC]{.smallcaps} in the FOCAL. When the density is high, as mentioned before, adding one constraint for avoiding a given conflict may cause a new conflict in the child node. As a result, there would be a lot of nodes with the same [NOC]{.smallcaps}. The high-level may randomly pick one node among them, which can be very inefficient. Using [SOC]{.smallcaps} of the paths as the tie-breaker is a common way for the high-level search. However, this makes the high-level search inclined to expand nodes with shorter paths, which is efficient in sparse environments. In dense environments, robots inevitably need to take more detours, and shorter paths do not really have fewer conflicts.

Since shorter paths can be wasteful to sift through, we speed up the expansion in [DCBS]{.smallcaps} by adopting a DFS-like strategy. Specifically, among the nodes with the same [NOC]{.smallcaps}, we choose to first explore the node that was *most lately* pushed to the OPEN list. With this choice, the high-level search is more inclined to explore as far as possible along a branch. As it goes deeper along a branch more quickly, the [NOC]{.smallcaps} descent enters stagnation in less time. In the example from Fig. [2](#fig:stuck_example){reference-type="ref" reference="fig:stuck_example"}, the blue curve uses the second strategy while the orange one uses [SOC]{.smallcaps} as the tie-breaker. Using DFS-like expansion strategy leads to "steeper\" [NOC]{.smallcaps} descent, which is more suitable for [DCBS]{.smallcaps}.

In our method, the proper time to trigger the database can be based on the following rules:

1.  The [NOC]{.smallcaps} of the current high-level node is less than a predefined value $NOC_p$.

2.  The [NOC]{.smallcaps} is in stagnation. For example, the value-change of the [NOC]{.smallcaps} in the high-level expansion is within a range for a number of iterations.

Rule (1) is straightforward. The solution quality of the database conflict resolution mechanism is heavily affected by the [NOC]{.smallcaps} of the node. If the [NOC]{.smallcaps} of the current node is small enough, applying the database to resolve the conflicts will introduce only small overheads, and leads to a solution with good quality. However, the suitable $NOC_p$ may vary in different maps and densities. If the $NOC_p$ is set very small in a very dense environment, the high-level search may enter [NOC]{.smallcaps} stagnation before its [NOC]{.smallcaps} drops below $NOC_p$. As a result, it takes a long time to trigger the database conflict resolution. In rule (2), the database conflict resolution is applied when the searching enters [NOC]{.smallcaps} stagnation, which is more flexible than the rule (1). The main drawback of this rule is that there might be multiple stagnations. If the high-level search enters one stagnation but the [NOC]{.smallcaps} is still large, the final solution can be very sub-optimal.

# Configuration Sparsification {#sec:algo-trans}

In this section, we describe *sparsified enhanced conflict-based search* ([SCBS]{.smallcaps}), a new algorithm for solving the locally-dense [MRPP]{.smallcaps} instances. In locally-dense [MRPP]{.smallcaps} instances, the total number of robots in a map is not necessarily high. But in the start/goal configurations, robots might be distributed unevenly. In these instances, the local density at some locations is extremely high, i.e., $\approx 100\%$. Assume that the local area of the vertex $v$ is the $W\times W$ square area centered at $v$. The local density at vertex $v$ is defined as $\rho_l(v)=\frac{n_v}{A_v}$, where $n_v$ is the number of robots located in the local area of $v$ and $A_v$ is the number of non-obstacle vertices in the local area of $v$.

The hybrid [SCBS]{.smallcaps} algorithm is outlined in Alg. [\[alg:secbs\]](#alg:secbs){reference-type="ref" reference="alg:secbs"} and Alg. [\[alg:greedy\]](#alg:greedy){reference-type="ref" reference="alg:greedy"}. The basic idea of [SCBS]{.smallcaps} is to convert the congested configurations into some intermediate configurations that are less dense and correlated and thus easier to solve. [SCBS]{.smallcaps} first tries to find an intermediate start configuration $X_S'$ and an intermediate goal configuration $X_G'$ which are more sparse than original starts and goals. Then the original problem breaks into three sub-problems, $P_1(\mathcal{G},X_S,X_S'),P_2(\mathcal{G},X_S',X_G'),P_3(\mathcal{G},X_G',X_G)$. Since the intermediate states are less dense than the original starts and goals, robots are less correlated, and as a consequence, solving $P_2(\mathcal{G},X_S',X_G')$ using [ECBS]{.smallcaps} takes less time than solving the original problem. While for $P_1$ and $P_3$, they can be formulated as unlabeled [MRPP]{.smallcaps} and be solved in polynomial time using algorithms in [@yu2012distance; @yu2013multi] (line 4-5). The final solution can be obtained by merging the paths for the sub-problems (line 7).

Obviously, the sparsification procedure introduces additional overhead on the optimality. Finding a good intermediate state is essential for balancing the computation time and solution quality. The intermediate configurations should try to satisfy the following: (i). $X_S'$ and $X_G'$ should be close to the original states as much as possible; (ii). The local density for each robot is controlled under a preferred robot density $\rho^{*}$, if possible. Finding the intermediate state can be formulated as an optimal assignment problem, which may be solved using integer linear programming. However, this would be very time-consuming. Instead, we develop an efficient suboptimal greedy algorithm for finding the assignment.

:::: algorithm
::: small
:::
::::

Alg. [\[alg:secbs\]](#alg:secbs){reference-type="ref" reference="alg:secbs"} describes how we find the intermediate configuration. It runs in a decoupled manner and finds the best location for each robot one by one greedily. For each robot $i$, we use A\* to explore the nodes in the graph where the A\* heuristic is set to be the sum of the distance from its start and goal. For the node $u$ to expand, we check if we choose $u$ as the intermediate vertex for robot $i$ whether the local density at each vertex in CONFIG is still less than $\rho^{*}$. If that is true, we set $u$ as an intermediate vertex and add it to CONFIG. The configurations found by the greedy algorithm are used as the unlabeled configurations $X_S''$ and $X_G''$. The unlabeled [MRPP]{.smallcaps} solver finds the intermediate paths $P_S$ and $P_G$ and assigns the intermediate vertices to the robots to get the labeled configurations $X_S', X_G'$.

:::: algorithm
::: small
$\text{CONFIG}\leftarrow\{\}$ CONFIG
:::
::::

As for merging the paths, simply concatenating the paths which may make the solution very suboptimal in terms of [SOC]{.smallcaps}[@guo2021spatial]. This is because robots need to be synchronized to execute the planned paths of each subproblem and some of the robots have to wait unnecessarily. We use the method based on Minimum Communication Policy (MCP) [@ma2016information] in [@Guo2023TowardEP]. This method tries to move the robots to their next vertex in their original plan as quickly as possible, which leads to a solution with better [SOC]{.smallcaps} optimality.

# Evaluation {#sec:evaluation}

In this section, we evaluate the proposed algorithms on dense instances. All experiments are performed on an Intel^®^ Core^TM^ i7-9700 CPU at 3.0GHz. We compare the proposed methods with [ECBS]{.smallcaps}($w=1.5$)[@barer2014suboptimal] and [DDM]{.smallcaps} [@han2019ddm]. All algorithms are implemented in C++. We evaluate the makespan, [SOC]{.smallcaps}, computation time, and success rate on a diverse set of maps and under different robot density levels. We repeated each experiment 20 times for each specific setting using different randomly generated instances for the agents, and report the mean values. Each algorithm is given 60 seconds time limit for each instance and the success rate is the number of solved instances divided by the total number of instances. The source code and evaluation data associated with this research will be made available at <https://github.com/arc-l/dcbs>.

## Evaluation on globally dense instances

In this section, we evaluate [DCBS]{.smallcaps} on different maps with different high robot densities. Here, the starts and goals are *uniformly* randomly generated. We evaluate the algorithms on three maps as shown in Fig. [3](#fig:maps_used){reference-type="ref" reference="fig:maps_used"}. The results are presented in Fig. [4](#fig:20x20_data){reference-type="ref" reference="fig:20x20_data"}-[6](#fig:lak103_data){reference-type="ref" reference="fig:lak103_data"}. Here, we tested three variants of [DCBS]{.smallcaps}. They differ in the strategy used to start database conflict resolution. [DCBS]{.smallcaps}(NOC=20) applies the database conflict resolution when [NOC]{.smallcaps} of the high-level node drops below 20 and uses $w_2=\infty$. [DCBS]{.smallcaps}(POC=$10\%$) applies the database conflict resolution when the ratio of the [NOC]{.smallcaps} of the current node to the [NOC]{.smallcaps} of the initial node is less than $10\%$ and uses $w_2=\infty$. [DCBS]{.smallcaps}($w_2=2$) applies the database conflict resolution when it finds that the [NOC]{.smallcaps} enters stagnation for 100 iterations and uses $w_2=2$. Here for [DCBS]{.smallcaps}($w_2=2$), we check the [MKPN]{.smallcaps} suboptimality.

::::: {#fig:maps_used .figure latex-placement="h!"}
::: overpic
./figures/maps_used.pdf (15.5, -3) (a) (48.5, -3) (b) (81.5, -3) (c)
:::

::: caption
The map used in the evaluation. (a) $20\times 20$ empty grid graph. (b) $24\times 18$ warehouse-like map. It has 360 non-blocked vertices. (c) $24\times 24$ "lak103\" game map adapted from DAO benchmarks [@stern2019mapf]. It has 293 non-blocked vertices.
:::
:::::

:::: {#fig:20x20_data .figure latex-placement="h!"}
![](Guo2023Efficient_figs/20x20_data-e.png){width="\\linewidth"}

::: caption
Performance (computation time, conservative makespan optimality ratio, conservative sum-of-cost optimality ratio, and success rate) on $20\times 20$ empty grid graph (Fig. [3](#fig:maps_used){reference-type="ref" reference="fig:maps_used"}(a)) for DDM, ECBS, multiple [DCBS]{.smallcaps} variants. [DCBS]{.smallcaps} with $w_2 = 2$ scales much better than ECBS without losing much optimality guarantee. [DCBS]{.smallcaps} with POC- and NOC-based heuristics achieves an excellent balance between computation time and solution optimality.
:::
::::

:::: {#fig:warehouse_data .figure latex-placement="h!"}
![](Guo2023Efficient_figs/warehouse_data-e.png){width="\\linewidth"}

::: caption
Performance (computation time, conservative makespan optimality ratio, conservative sum-of-cost optimality ratio, and success rate) on the warehouse map (Fig. [3](#fig:maps_used){reference-type="ref" reference="fig:maps_used"}(b)) for DDM, ECBS, multiple [DCBS]{.smallcaps} variants. All [DCBS]{.smallcaps} variants achieve an excellent balance between computation time and solution optimality compared to DDM and ECBS; [DCBS]{.smallcaps} with $w_2 =2$ does especially well.
:::
::::

:::: {#fig:lak103_data .figure latex-placement="h!"}
![](Guo2023Efficient_figs/lak103_data.png){width="\\linewidth"}

::: caption
Performance (computation time, conservative makespan optimality ratio, conservative sum-of-cost optimality ratio, and success rate) on the DAO gamp map (Fig. [3](#fig:maps_used){reference-type="ref" reference="fig:maps_used"}(c)) for DDM, ECBS, multiple [DCBS]{.smallcaps} variants. [DCBS]{.smallcaps} still does reasonably well in balancing solution computation speed and optimality.
:::
::::

From the experimental data, we observe that the [MKPN]{.smallcaps} and [SOC]{.smallcaps} suboptimality ratio of [DCBS]{.smallcaps} variants are much better than [DDM]{.smallcaps}. When enabling the suboptimality checking mechanism, the suboptimality ratio of [DCBS]{.smallcaps} is around $1.x$, which is quite acceptable. On the other hand, [DCBS]{.smallcaps} variants and [DDM]{.smallcaps} are more scalable than [ECBS]{.smallcaps} and thus yield a higher success rate. On the empty grid and the warehouse map, the success rate of [DCBS]{.smallcaps} variants is almost always $100\%$, capable of tackling instances with robot density more than $60\%$-$70\%$. On the DAO map that is more complex and has some narrow passages, [DCBS]{.smallcaps} is still able to solve more instances than [ECBS]{.smallcaps}. Despite the lower success rate, the suboptimality checking mechanism is essential to preserve the solution quality.

## Evaluation on locally dense instances

In this section, we evaluate [SCBS]{.smallcaps} with DDM, ECBS, and [SCBS]{.smallcaps} in two classes of locally dense instances, named multi-robot rearrangement and Gaussian distributed [MRPP]{.smallcaps} instance. To generate a Gaussian distributed [MRPP]{.smallcaps} instance, for each point, we generate a 2D vector $(\lfloor x \rfloor,\lfloor y\rfloor)$ where $x,y\sim \mathcal{N}(0,\sigma^2)$ if point $(\lfloor x \rfloor,\lfloor y\rfloor)$ has not been used yet. In the first class, the robots are randomly concentrated in the lower-left corner square area in start/goal configurations (e.g., the top row of Fig. [1](#fig:dense_example){reference-type="ref" reference="fig:dense_example"}). In the second class, the configurations are generated following a two-dimensional normal distribution with $\sigma=5$. In both classes, the graph size can be arbitrarily large (we set a sufficiently large boundary in the actual implementation).

The results are shown in Fig. [7](#fig:rearrangement){reference-type="ref" reference="fig:rearrangement"}-[8](#fig:gauss){reference-type="ref" reference="fig:gauss"}. In the first class (rearrangement), robots are so strongly-correlated that [ECBS]{.smallcaps} struggles to solve instances with more than 36 robots. [SCBS]{.smallcaps}($\rho^{*}=50\%$) yields $100\%$ success rate and is able to deal with 100+ robots. The unlabeled [MRPP]{.smallcaps} only introduces small overheads to the solution, and the suboptimality ratio of [SCBS]{.smallcaps} is around $1.x$-$2.x$.

:::: {#fig:rearrangement .figure latex-placement="h!"}
![](Guo2023Efficient_figs/rearrangement_data.png){width="\\linewidth"}

::: caption
Performance (computation time, conservative makespan optimality ratio, conservative sum-of-cost optimality ratio, and success rate) on multi-robot rearrangement settings (e.g., the top row of Fig. [1](#fig:dense_example){reference-type="ref" reference="fig:dense_example"}) for DDM, ECBS, [DCBS]{.smallcaps}, and [SCBS]{.smallcaps}. Whereas [DCBS]{.smallcaps} does better than DDM and ECBS, [SCBS]{.smallcaps} leaves all methods far behind in achieving an excellent balance between optimality and computational efficiency.
:::
::::

:::: {#fig:gauss .figure latex-placement="h!"}
![](Guo2023Efficient_figs/gauss_data.png){width="\\linewidth"}

::: caption
Performance (computation time, conservative makespan optimality ratio, conservative sum-of-cost optimality ratio, and success rate) on Gaussian distributed [MRPP]{.smallcaps} instances for DDM, ECBS, [DCBS]{.smallcaps}, and [SCBS]{.smallcaps}. Again, [SCBS]{.smallcaps} trades very nicely between scalability and solution optimality.
:::
::::

# Conclusion and Discussions {#sec:conclusion}

In this paper, we present two novel heuristics-based algorithms for multi-robot path planning ([MRPP]{.smallcaps}) in dense and congested environments, with the goal to provide to quickly provide high-quality solutions for these problems. The first method, [DCBS]{.smallcaps}, incorporates a database-driven conflict resolution mechanism to resolve node conflicts in dense setups. Optimality protection rules are also instilled to maintain reasonable solution quality. Whereas [DCBS]{.smallcaps} addresses *globally* dense scenarios, the second method, [SCBS]{.smallcaps}, tackles *locally* dense settings by converting ultra-dense configurations into sparser ones through a greedy start-goal assignment and then solving an unlabeled [MRPP]{.smallcaps}. The sparsification step, while incurring some overhead, makes the overall problem significantly easier. Through extensive experiments, we show that our proposed methods achieve excellent performance in balancing success rate, running time, and solution quality.

Currently, [DCBS]{.smallcaps} only uses a fairly basic solution database, which is limiting the speed and flexibility of [DCBS]{.smallcaps}. In future work, we plan to significantly expand the solution database while keeping it sufficiently small for fast look-ups. Portions of the database may also be augmented using machine learning. We expect this to provide a sizable performance boost for [DCBS]{.smallcaps}.

There are also many open questions that should be investigated further. For example, as of now, the way we trigger the conflict resolution mechanism is somewhat rigid. Can we devise a better approach, e.g., using a data-driven method, to figure out the optimal time to trigger conflict resolution? As another example, there is still a lack of understanding of the exact relationship between time complexity and robot density and distribution. Can we establish a deeper, or better yet, quantitative, relationship between the two?

::: thebibliography
10 url@rmstyle

J. Yu and S. M. LaValle, "Structure and intractability of optimal multi-robot path planning on graphs," in *Proceedings AAAI National Conference on Artificial Intelligence*, 2013, pp. 1444--1449.

P. Surynek, "An optimization variant of multi-robot path planning is intractable," in *Proceedings AAAI National Conference on Artificial Intelligence*, 2010, pp. 1261--1263.

J. Yu, "Intractability of optimal multi-robot path planning on planar graphs," *IEEE Robotics and Automation Letters*, vol. 1, no. 1, pp. 33--40, 2016.

P. R. Wurman, R. D'Andrea, and M. Mountz, "Coordinating hundreds of cooperative, autonomous vehicles in warehouses," *AI magazine*, vol. 29, no. 1, pp. 9--9, 2008.

R. Mason, "Developing a profitable online grocery logistics business: Exploring innovations in ordering, fulfilment, and distribution at ocado," in *Contemporary Operations and Logistics*.Springer, 2019, pp. 365--383.

Q. Wan, C. Gu, S. Sun, M. Chen, H. Huang, and X. Jia, "Lifelong multi-agent path finding in a dynamic environment," in *2018 15th International Conference on Control, Automation, Robotics and Vision (ICARCV)*.IEEE, 2018, pp. 875--882.

S. Poduri and G. S. Sukhatme, "Constrained coverage for mobile sensor networks," in *Proceedings IEEE International Conference on Robotics & Automation*, 2004.

F. A. A. Cheein and R. Carelli, "Agricultural robotics: Unmanned robotic service units in agricultural tasks," *IEEE industrial electronics magazine*, vol. 7, no. 3, pp. 48--58, 2013.

D. Rus, B. Donald, and J. Jennings, "Moving furniture with teams of autonomous robots," in *Proceedings IEEE/RSJ International Conference on Intelligent Robots & Systems*, 1995, pp. 235--242.

J. A. Preiss, W. Hönig, G. S. Sukhatme, and N. Ayanian, "Crazyswarm: A large nano-quadcopter swarm," in *IEEE Int. Conf. on Robotics and Automation (ICRA)*, 2017.

D. Kornhauser, G. Miller, and P. Spirakis, "Coordinating pebble motion on graphs, the diameter of permutation groups, and applications," in *Proceedings IEEE Symposium on Foundations of Computer Science*, 1984, pp. 241--250.

M. A. Erdmann and T. Lozano-Pérez, "On multiple moving objects," in *Proceedings IEEE International Conference on Robotics & Automation*, 1986, pp. 1419--1424.

S. M. LaValle and S. A. Hutchinson, "Optimal motion planning for multiple robots having independent goals," *IEEE Transactions on Robotics & Automation*, vol. 14, no. 6, pp. 912--925, Dec. 1998.

Y. Guo and L. E. Parker, "A distributed and optimal motion planning approach for multiple mobile robots," in *Proceedings IEEE International Conference on Robotics & Automation*, 2002, pp. 2612--2619.

J. Yu and S. M. LaValle, "Optimal multi-robot path planning on graphs: Complete algorithms and effective heuristics," *IEEE Transactions on Robotics*, vol. 32, no. 5, pp. 1163--1177, 2016.

E. Boyarski, A. Felner, R. Stern, G. Sharon, O. Betzalel, D. Tolpin, and E. Shimony, "Icbs: The improved conflict-based search algorithm for multi-agent pathfinding," in *Eighth Annual Symposium on Combinatorial Search*, 2015.

L. Cohen, T. Uras, T. Kumar, H. Xu, N. Ayanian, and S. Koenig, "Improved bounded-suboptimal multi-agent path finding solvers," in *International Joint Conference on Artificial Intelligence*, 2016.

T. Guo and J. Yu, "Toward efficient physical and algorithmic design of automated garages," *arXiv preprint arXiv:2302.01305*, 2023.

A. Okoso, K. Otaki, S. Koide, and T. Nishi, "High density automated valet parking via multi-agent path finding," in *2022 IEEE 25th International Conference on Intelligent Transportation Systems (ITSC)*.IEEE, 2022, pp. 2146--2153.

S. D. Han and J. Yu, "Ddm: Fast near-optimal multi-robot path planning using diversified-path and optimal sub-problem solution database heuristics," *ArXiv*, vol. abs/1904.02598, 2019.

G. Sharon, R. Stern, A. Felner, and N. R. Sturtevant, "Conflict-based search for optimal multi-agent pathfinding," *Artificial Intelligence*, vol. 219, pp. 40--66, 2015.

T. Guo and J. Yu, "Sub-1.5 Time-Optimal Multi-Robot Path Planning on Grids in Polynomial Time," in *Proceedings of Robotics: Science and Systems*, New York City, NY, USA, June 2022.

R. Stern, N. Sturtevant, A. Felner, S. Koenig, H. Ma, T. Walker, J. Li, D. Atzmon, L. Cohen, T. Kumar, *et al.*, "Multi-agent pathfinding: Definitions, variants, and benchmarks," *arXiv preprint arXiv:1906.08291*, 2019.

P. Surynek, "An optimization variant of multi-robot path planning is intractable," in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 24, no. 1, 2010.

J. Yu and S. M. LaValle, "Structure and intractability of optimal multi-robot path planning on graphs," in *Twenty-Seventh AAAI Conference on Artificial Intelligence*, 2013.

H. Ma, C. Tovey, G. Sharon, T. Kumar, and S. Koenig, "Multi-agent path finding with payload transfers and the package-exchange robot-routing problem," in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 30, no. 1, 2016.

J. Yu and S. M. LaValle, "Optimal multirobot path planning on graphs: Complete algorithms and effective heuristics," *IEEE Transactions on Robotics*, vol. 32, no. 5, pp. 1163--1177, 2016.

E. Erdem, D. G. Kisa, U. Öztok, and P. Schueller, "A general formal framework for pathfinding problems with multiple agents." in *AAAI*, 2013.

T. Guo, S. D. Han, and J. Yu, "Spatial and temporal splitting heuristics for multi-robot motion planning," in *2021 IEEE International Conference on Robotics and Automation (ICRA)*, 2021, pp. 8009--8015.

P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100--107, 1968.

D. Silver, "Cooperative pathfinding." *AIIDE*, vol. 1, pp. 117--122, 2005.

G. Sharon, R. Stern, M. Goldenberg, and A. Felner, "The increasing cost tree search for optimal multi-agent pathfinding," *Artificial Intelligence*, vol. 195, pp. 470--495, 2013.

M. Barer, G. Sharon, R. Stern, and A. Felner, "Suboptimal variants of the conflict-based search algorithm for the multi-agent pathfinding problem," in *Seventh Annual Symposium on Combinatorial Search*, 2014.

K. Okumura, M. Machida, X. Défago, and Y. Tamura, "Priority inheritance with backtracking for iterative multi-agent path finding," *arXiv preprint arXiv:1901.11282*, 2019.

R. J. Luna and K. E. Bekris, "Push and swap: Fast cooperative path-finding with completeness guarantees," in *Twenty-Second International Joint Conference on Artificial Intelligence*, 2011.

M. Szegedy and J. Yu, "On rearrangement of items stored in stacks," in *The 14th International Workshop on the Algorithmic Foundations of Robotics*, 2020.

T. Guo, S. W. Feng, and J. Yu, "Polynomial Time Near-Time-Optimal Multi-Robot Path Planning in Three Dimensions with Applications to Large-Scale UAV Coordination," in *2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2022.

J. Pearl and J. H. Kim, "Studies in semi-admissible heuristics," *IEEE transactions on pattern analysis and machine intelligence*, no. 4, pp. 392--399, 1982.

J. Yu and M. LaValle, "Distance optimal formation control on graphs with a tight convergence time guarantee," in *2012 IEEE 51st IEEE Conference on Decision and Control (CDC)*.IEEE, 2012, pp. 4023--4028.

J. Yu and S. M. LaValle, "Multi-agent path planning and network flow," in *Algorithmic foundations of robotics X*.Springer, 2013, pp. 157--173.

K.-C. Ma, L. Liu, and G. S. Sukhatme, "An information-driven and disturbance-aware planning method for long-term ocean monitoring," in *Intelligent Robots and Systems (IROS), 2016 IEEE/RSJ International Conference on*.IEEE, 2016, pp. 2102--2108.

R. Stern, N. R. Sturtevant, A. Felner, S. Koenig, H. Ma, T. T. Walker, J. Li, D. Atzmon, L. Cohen, T. K. S. Kumar, E. Boyarski, and R. Bartak, "Multi-agent pathfinding: Definitions, variants, and benchmarks," *Symposium on Combinatorial Search (SoCS)*, pp. 151--158, 2019.
:::

[^1]: G. Teng, and J. Yu are with the Department of Computer Science, Rutgers, the State University of New Jersey, Piscataway, NJ, USA. Emails: `{ teng.guo, jingjin.yu}@rutgers.edu`.

[^2]: This work was supported in part by NSF award IIS-1845888 and an Amazon Research Award.
