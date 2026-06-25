---
citation_key: Saxena2021AMRA
arxiv_id: 2110.05328
arxiv_url: https://arxiv.org/abs/2110.05328
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:40:04Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

:::: {#fig:intro .figure latex-placement="t"}
![](Saxena2021AMRA_figs/amra-intro-eps-converted-to.png){width="0.8\\columnwidth"}

::: caption
*Effect of Resolution:* local minima can be explored quicker at coarser resolutions (a), while finer resolutions help navigate through narrow passageways (b); *Effect of Heuristics:* a less informed heuristic (c) expands many more states than an informed heuristic (d); and *Anytime behaviour*: an initial suboptimal solution (e) can be improved over time (f). The pictures show start states in [green]{style="color: Green"}, goal states in [red]{style="color: Red"}.
:::
::::

Heuristic search algorithms for robot motion planning find least-cost solutions in discretised approximations of the continuous state space of the robot. They have shown impressive results in robot manipulation [@CohenCL14], navigation [@LiuMAK18], task planning [@GarrettLK14], and multi-robot coordination [@WagnerC11]. The size of the search space for these algorithms is determined by the dimensionality of the robot state space and, crucially, the discretisation level of each of these dimensions [@L2006]. If the state space is discretised finely the search needs to explore a greater number of possible robot states in order to find a solution which is computationally costly. However at the same time, this higher resolution allows the search to find potential solutions through narrow passageways and dense obstacle clutter. A coarse discretisation of the state space is useful in relatively obstacle-free areas of the environment, and for the search to escape local minima where the heuristic estimate of the cost-to-goal is weakly correlated with the true cost-to-goal. The downside is that the search might fail to find a solution at that resolution.

At the same time, it is important for heuristic search algorithms to be instantiated with useful heuristics as they determine the computational effort spent exploring areas of the search space to find a solution. If a heuristic estimate of the cost-to-goal is poorly correlated with the true cost-to-goal, search algorithms can spend a lot of time expanding states in these local minima before finding a path to goal [@Hoffmann01]. Multi-heuristic search algorithms [@AineSNHL16] were developed to alleviate this problem by allowing search algorithms to be instantiated with multiple heuristics. These are not only easier to define for the practitioner, but also allow for information sharing between heuristics to better guide the search.

In this work we present [AMRA\*]{.sans-serif}, an **A**nytime Multi-Heuristic **M**ulti-**R**esolution **[A\*]{.sans-serif}** search algorithm that is capable of searching a state space at multiple levels of discretisation, share information between multiple heuristics, and improve the quality of the solution found over time. It is able to determine the appropriate resolution for exploring local minima and navigating across obstacle-free space and narrow passageways. It takes advantage of different heuristics being better correlated with the true cost-to-goal in different regions of the search space. Finally, with every iteration of the search loop, [AMRA\*]{.sans-serif} is able to improve its solution with tighter suboptimality bounds and find the optimal solution in-the-limit of time.

Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} shows simple examples of three aspects of heuristic search that [AMRA\*]{.sans-serif} encapsulates in one general algorithm while maintaining important theoretical properties of completeness and (sub-)optimality. First, in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} (a), if we follow a greedy heuristic to the goal, the obstacle introduces a local minima with many more states at the fine resolution (light red grid) than the coarse resolution (black grid). In this case, running a search at coarse resolution will find a path to the goal with less computation. The downside of using only a coarse resolution is shown in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} (b), where a solution only exists at the fine resolution. Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} (c-d) show the effect of using a less informed heuristic (Euclidean distance) vis-a-vis a perfect heuristic (backward Dijkstra search from the goal). For more complicated problems, different heuristics can be informative in different regions of the state space, and a search algorithm that can take advantage of this can greatly improve performance. Finally, an anytime algorithm like [AMRA\*]{.sans-serif} relies heavily on the coarse resolution to quickly find an initial solution in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} (e) (coarse states are highlighted in gray). It goes on to improve this solution over time to also include fine resolution states (highlighted in light red) in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} (f).

# Related Work {#sec:litreview}

[AMRA\*]{.sans-serif} is an anytime, multi-heuristic, multi-resolution search algorithm for solving robot motion planning problems. It builds on the family of best-first search algorithms that traces its roots back to classic [A\*]{.sans-serif} and Weighted A\* ([wA\*]{.sans-serif}) search algorithms [@HartNR68; @Pohl70]. For a large class of real-world robotics applications, optimal motion planning can be intractable due to the expansive nature of robot state spaces. Anytime algorithms allow us to solve problems in these domains by finding an initial highly suboptimal solution quickly, and spending any remaining planning budget to improve that solution. [ARA\*]{.sans-serif} [@LikhachevGT03] is an anytime version of [wA\*]{.sans-serif} and provides bounds on solution suboptimality that Anytime [A\*]{.sans-serif} [@ZhouH02] does not. van den Berg et. al [@BergSHG11] present [ANA\*]{.sans-serif}, a non-paramateric version of [ARA\*]{.sans-serif}[^2].

While anytime algorithms have the ability to refine solutions over time, their performance is determined by the heuristic. The use of multiple heuristics within a search algorithm can dramatically improve search performance since different heuristics can offer better guidance in different regions of state space [@Helmert06; @AineSNHL16]. Recently, Natarajan et. al. [@NatarajanSALC19] have also developed an anytime multi-heuristic algorithm.

Contemporaneous to the development of anytime and multi-heuristic algorithms, there has been work on developing algorithms that utilise multiple levels of discretisation of the robot state space. These multi-resolution algorithms rely on a coarser discretisation to navigate large regions of obstacle-free space, and revert to a finer discretisation to maneuver through narrow passageways [@MooreA95; @GarciaKB14; @DuIL20].

Most of the algorithms discussed above have provable bounds on solution suboptimality. Some sampling-based planners for robot motion planning [@KaramanF11] offer a different notion of solution optimality. They are *asymptotically* optimal, and thus will find the optimal solution given infinite time. As such, they can be interrupted early to exhibit an anytime behaviour.

We compare the performance of [AMRA\*]{.sans-serif} in this paper with the three most closely related heuristic search algorithms ([ARA\*]{.sans-serif} [@LikhachevGT03], [MRA\*]{.sans-serif} [@DuIL20] and [A-MHA\*]{.sans-serif} [@NatarajanSALC19]) and against an asymptotically optimal sampling-based algorithm ([RRT\*]{.sans-serif} [@KaramanF11]).

# Problem Formulation {#sec:problem}

We define a robot motion planning problem with the tuple $(\mathcal{X}, x_s, \mathcal{G})$, where $\mathcal{X}$ is the state space of the robot, $x_s \in \mathcal{X}$ is the start state, and $\mathcal{G} \subset \mathcal{X}$ is a set of goal states. $\mathcal{X}_{\text{free}} \subset \mathcal{X}$ denotes the obstacle-free space in the environment. A solution to the motion planning problem, if one exists, is a collision-free path from $x_s$ to $\mathcal{G}$.

We assume access to a cost function $c: \mathcal{X} \times \mathcal{X} \rightarrow \mathbb{R}_{\geq 0}$ to compute the cost of an action between two robot states. The cost of a potential solution path $\pi = \{x_1, \ldots, x_n\}$ is denoted by overloading the definition of cost function $c$ as $c(\pi) = \sum_{i = 1}^{N-1} c(x_i, x_{i+1})$. Our goal in this paper is to solve the least-cost path planning problem and find the optimal path $\pi^* = \mathop{\mathrm{arg\,min}}_\pi c(\pi)$.

# Graph Construction and Search {#sec:graph}

We solve the least-cost robot motion planning problem with a heuristic search algorithm over a graph $G = (V, E)$. The vertex set $V \subset \mathcal{X}$ contains robot states. Edges $e = (x_i, x_j) \in E$ connect two vertices $x_i, x_j \in V$ if the robot can execute an action that takes it from $x_i$ to $x_j$. Thus each edge $e \in E$ is also an action $a$ in the robot action space $\mathcal{A}$.

## Action Spaces {#sec:actions}

[AMRA\*]{.sans-serif} constructs its vertex set $V = \bigcup_r V_r$ as a union over different levels of discretisation or resolutions $r$ of $\mathcal{X}$. Each vertex set $V_r$ has a corresponding edge set $E_r$ which make up the edges $E = \bigcup_r E_r$ used by [AMRA\*]{.sans-serif} when constructing $G$. We represent each edge set $E_r$ with an action space $\mathcal{A}_r$ available to the robot. The core underlying assumption in this work and robot motion planning with multiple resolutions in general is that for every resolution $r$ being used, the robot has access to actions $\mathcal{A}_r$ that take it between two states $x_u, x_v \in V_r$. Note that this formulation allows for a state $x \in \mathcal{X}$ to exist at multiple resolutions $r$, and thus in multiple vertex and edge sets $V_r, E_r$.

:::: {#fig:actions .figure latex-placement="t"}
![](Saxena2021AMRA_figs/actions-eps-converted-to.png){width="0.25\\columnwidth"}

::: caption
Multi-resolution action space for 8-connected grid navigation. The robot (at the [blue]{style="color: Blue"} state) can execute fine resolution actions to [green]{style="color: Green"} states, and coarse resolution actions to [red]{style="color: Red"} states.
:::
::::

Fig. [2](#fig:actions){reference-type="ref" reference="fig:actions"} shows an example of a multi-resolution action space for 2D grid navigation. [AMRA\*]{.sans-serif} does not require that coarse actions be made up of fine actions, nor does it require any action to end in states that exist at multiple resolutions. However as we discuss in Section [4.2](#sec:heuristics){reference-type="ref" reference="sec:heuristics"}, especially for multi-heuristic search, it can be useful to construct action spaces that lead to significant overlap between vertex sets at different resolutions.

## Multi-Heuristic Search {#sec:heuristics}

A heuristic function $h: V \rightarrow \mathbb{R}_{\geq 0}$ is an estimate of the *cost-to-goal* from a state $x \in V$ on the graph $G$. Heuristics are *admissible* if they under-estimate the true cost-to-goal from $x$ to $\mathcal{G}$ on $G$. [AMRA\*]{.sans-serif} executes a multi-heuristic search derived from [MHA\*]{.sans-serif} [@AineSNHL16] which allows the use of multiple inadmissible heuristics. [AMRA\*]{.sans-serif} parameterises heuristics by the resolution $r$ for which they are applicable. The search is initialised with a set of heuristics, at least one per resolution $r$ used. The [MHA\*]{.sans-serif} framework allows us to use any number of additional heuristics for each resolution.

As with [MHA\*]{.sans-serif} and [MRA\*]{.sans-serif}, it is necessary to initialise [AMRA\*]{.sans-serif} with an *anchor* heuristic which is *consistent*, i.e. a heuristic function $h$ such that $h(x_i) \leq h(x_j) + c(x_i, x_j) \forall e = (x_i, x_j) \in E$. We reserve the resolution $r = 0$ to refer to this anchor search. The anchor search uses the full action space of the robot $\mathcal{A}_0 = \bigcup_{r > 0} \mathcal{A}_r$ to construct the graph $G_0 = (V_0, E_0)$. This implies $V_0 = \bigcup_{r > 0} V_r$, and we refer to the anchor search vertex set as the *union space*. If all coarse resolution states coincide with some state at the finest resolution ($V_r \subset V_1 \,\forall\, r > 1$), this is easily achieved by running the anchor search at the finest resolution ($V_0 \equiv V_1$).

Using multiple heuristics at the same resolution allows us to share information between these heuristics by maintaining a single *cost-to-come* value (cost of the current best path between the start and some state) and multiple cost-to-goal estimates for a state. This information sharing allows the search to potentially escape local minima for some heuristic in a region of the state space on the basis of guidance from another heuristic at that resolution in that region.

# Algorithm {#sec:algo}

::::: algorithm
:::: small
::: algorithmic
$g(x) + w_1 \times h_i(x)$

$r \gets \texttt{Res}(i)$ []{#line:open_clear label="line:open_clear"} Remove $x$ from $OPEN_j$ []{#line:succs label="line:succs"} $g(x^\prime) \gets g(x)  + c(x, x^\prime)$ $bp(x^\prime) \gets x$ []{#line:incons label="line:incons"} $\texttt{Insert}(x^\prime, INCONS)$ $\texttt{Update}(x^\prime, OPEN_0, \textsc{Key}(x^\prime, 0)$[]{#line:succ_open label="line:succ_open"} $l \gets \texttt{Res}(j)$ **continue** $\texttt{Update}(x^\prime, OPEN_j, \textsc{Key}(x^\prime, j))$[]{#line:succ_inad label="line:succ_inad"}

[]{#line:fail label="line:fail"} $i \gets \texttt{ChooseQueue}()$[]{#line:roundrobin label="line:roundrobin"} $x \gets OPEN_i.\text{top}()$[]{#line:expand_inad label="line:expand_inad"} $\textsc{Expand}(x, i)$ $r \gets \texttt{Res}(i)$ $\texttt{Insert}(x, CLOSED_r)$[]{#line:close_inad label="line:close_inad"} []{#line:goal_inad label="line:goal_inad"} $x_{\text{goal}} \gets x$ true[]{#line:solve_inad label="line:solve_inad"} $x \gets OPEN_0.\text{top}()$[]{#line:expand_anchor label="line:expand_anchor"} $\textsc{Expand}(x, 0)$ $\texttt{Insert}(x, CLOSED_0)$[]{#line:close_anchor label="line:close_anchor"} []{#line:goal_anchor label="line:goal_anchor"} $x_{\text{goal}} \gets x$ true[]{#line:solve_anchor label="line:solve_anchor"}

$w_1 \gets w_1^{\text{init}}, w_2 \gets w_2^{\text{init}}$ $g(x_s) = 0$ $bp(x_s) \gets NULL$ $OPEN_i.\text{clear}()$ $\texttt{Insert}(x_s, INCONS)$ []{#line:amra_loop label="line:amra_loop"} []{#line:incons_to_anchor label="line:incons_to_anchor"} $\texttt{Update}\left(x, OPEN_0, \textsc{Key}(x, 0)\right)$ $INCONS.\text{clear}()$ []{#line:anchor_to_inad label="line:anchor_to_inad"} $\texttt{Update}\left(x, OPEN_j, \textsc{Key}(x, j)\right)$ $CLOSED_r.\text{clear}()$ Publish current solution by tracing $bp(x_{\text{goal}})$ till $x_s$ **break** Update $w_1, w_2$ []{#line:w_update label="line:w_update"}
:::
::::
:::::

Algorithm [\[alg:amra\]](#alg:amra){reference-type="ref" reference="alg:amra"} contains the full [AMRA\*]{.sans-serif} search procedure. [AMRA\*]{.sans-serif} is initialised with the start state $x_s$, goal set $\mathcal{G}$, action spaces $\{\mathcal{A}_0, \ldots, \mathcal{A}_N\}$, and heuristics $\{h_0, \ldots, h_M\}$. The state space $\mathcal{X}$ is discretised into $N$ levels. For $i < j$, resolution $i$ is finer than resolution $j$. The anchor action space is the union action space ($\mathcal{A}_0 = \bigcup_{r=1}^N \mathcal{A}_r$), and the anchor search is run at the finest resolution ($V_0 \equiv V_1$). The anchor heuristic $h_0$ is consistent (and thus admissible), while the other heuristics may be inadmissible. There is at least one heuristic per resolution, thus $M \geq N$.

## Connections to Existing Algorithms

[AMRA\*]{.sans-serif} is a generalisation of several existing search algorithms. With a single heuristic per resolution, if we do not run [AMRA\*]{.sans-serif} anytime, [AMRA\*]{.sans-serif} is the same as [MRA\*]{.sans-serif} [@DuIL20]. We can also run [AMRA\*]{.sans-serif} for a single resolution, with multiple heuristics at that resolution, and obtain either [A-MHA\*]{.sans-serif} [@NatarajanSALC19] or [MHA\*]{.sans-serif} [@AineSNHL16] depending on whether it is run anytime or not. In slightly more contrived scenarios, for a single resolution and a single heuristic, [AMRA\*]{.sans-serif} can also devolve to [ARA\*]{.sans-serif} [@LikhachevGT03] and Weighted A\* ([wA\*]{.sans-serif}) [@Pohl70]. The connections stem from the fact that [AMRA\*]{.sans-serif} utilises multiple resolutions, multiple heuristics, and is anytime.

## [AMRA\*]{.sans-serif} Desiderata

We denote the cost-to-come for a state with the function $g: V \rightarrow \mathbb{R}_{\geq 0}$. The *parent* of a state $x$, denoted by $bp(x)$ is its predecessor on the best known path from $x_s$ to $x$. `Resolutions`$(x)$ returns the set of resolutions state $x$ lies on: $r \in \texttt{Resolutions}(x) \Rightarrow x \in V_r$. Each resolution $r$ is associated with a container for states expanded at that resolution, $CLOSED_r$. `Res`$(i)$ returns the resolution associated with heuristic $h_i$. Each heuristic $h_i$ is associated with a priority queue $OPEN_i$. `Succs`$(x, \mathcal{A}_r)$ generates all valid successors of $x$ at resolution $r$ using the appropriate action space $\mathcal{A}_r$. For $r = 0$, this generates all valid successors of $x$ for all resolutions in `Resolutions`$(x)$.

## Algorithmic Details

The anytime nature of [AMRA\*]{.sans-serif} is controlled by the loop in Line [\[line:amra_loop\]](#line:amra_loop){reference-type="ref" reference="line:amra_loop"}. The suboptimality of the solution is controlled by parameters $w_1, w_2$. At the end of each iteration, [AMRA\*]{.sans-serif} returns a solution which is at most $w_1\times w_2$ suboptimal with respect to the graph $G_0 = (V_0, E_0)$ (from Theorem [3](#thm:suboptimality){reference-type="ref" reference="thm:suboptimality"}). $w_1, w_2$ are decreased in Line [\[line:w_update\]](#line:w_update){reference-type="ref" reference="line:w_update"} in order to potentially improve the solution quality in the next iteration. To facilitate this, [AMRA\*]{.sans-serif} maintains $INCONS$ - a container for all *inconsistent* states. These are states whose cost-to-come, or $g$-value, is improved after they have been expanded from the admissible anchor search. If a state becomes inconsistent, a better solution through it might be found than the current best known solution. Hence these states are added back into the appropriate $OPEN_i$ for consideration by the search (Lines [\[line:incons_to_anchor\]](#line:incons_to_anchor){reference-type="ref" reference="line:incons_to_anchor"} and [\[line:anchor_to_inad\]](#line:anchor_to_inad){reference-type="ref" reference="line:anchor_to_inad"}).

[ImprovePath]{.smallcaps} is the core function that searches for a path between $x_s$ and $\mathcal{G}$. $x_{\text{goal}} \in \mathcal{G}$ is some state which satisfies the termination condition in Line [\[line:goal_inad\]](#line:goal_inad){reference-type="ref" reference="line:goal_inad"} or Line [\[line:goal_anchor\]](#line:goal_anchor){reference-type="ref" reference="line:goal_anchor"}. If no such $x_{\text{goal}}$ is found before all $OPEN_i$ are exhausted (Line [\[line:fail\]](#line:fail){reference-type="ref" reference="line:fail"}), [AMRA\*]{.sans-serif} terminates with failure. Line [\[line:roundrobin\]](#line:roundrobin){reference-type="ref" reference="line:roundrobin"} controls the scheduling policy over all heuristics. While many options exist [@PhillipsNAL15], for [AMRA\*]{.sans-serif} we use a simple round robin.

The core modification in [AMRA\*]{.sans-serif} over [MRA\*]{.sans-serif} and [MHA\*]{.sans-serif} is the way in which the graph is constructed in [Expand]{.smallcaps}. Any time a state is expanded at a particular resolution, it is removed from all inadmissible (non-anchor) heuristics at that resolution (in the loop in Line [\[line:open_clear\]](#line:open_clear){reference-type="ref" reference="line:open_clear"})[^3]. This is because the $g$-value of an inadmissibly expanded state is independent of the heuristic it was expanded from. The [Expand]{.smallcaps} function generates the successors of state $x$ by using the appropriate action space $\mathcal{A}_r$ (Line [\[line:succs\]](#line:succs){reference-type="ref" reference="line:succs"}). After checking for successor consistency in Line [\[line:incons\]](#line:incons){reference-type="ref" reference="line:incons"}, a newly generated state is inserted at all appropriate resolutions (Lines [\[line:succ_open\]](#line:succ_open){reference-type="ref" reference="line:succ_open"} to [\[line:succ_inad\]](#line:succ_inad){reference-type="ref" reference="line:succ_inad"}).

# Theoretical Analysis {#sec:analysis}

::: {#thm:expansions .theorem}
**Theorem 1**. *[AMRA\*]{.sans-serif} expands each state at most $N+1$ times per iteration.*
:::

::: proof
*Proof.* Any state that is expanded must be in some $OPEN_i$ (Lines [\[line:expand_inad\]](#line:expand_inad){reference-type="ref" reference="line:expand_inad"} and [\[line:expand_anchor\]](#line:expand_anchor){reference-type="ref" reference="line:expand_anchor"}). Upon admissible expansion from the anchor search, the state is inserted into $CLOSED_0$ (Line [\[line:close_anchor\]](#line:close_anchor){reference-type="ref" reference="line:close_anchor"}) and never inserted into $OPEN_0$ again (Line [\[line:incons\]](#line:incons){reference-type="ref" reference="line:incons"}). For inadmissible expansions, the state is removed from all $OPEN_i$ for the appropriate resolution $r$ in the loop in Line [\[line:open_clear\]](#line:open_clear){reference-type="ref" reference="line:open_clear"}, and inserted into $CLOSED_r$ in Line [\[line:close_inad\]](#line:close_inad){reference-type="ref" reference="line:close_inad"}. This can happen once per resolution. Thus a state can be expanded at most $N + 1$ times per iteration of [AMRA\*]{.sans-serif}. ◻
:::

::: {#thm:complete .theorem}
**Theorem 2**. *[AMRA\*]{.sans-serif} is complete with respect to the graph $G_0 = (V_0, E_0)$.*
:::

::: proof
*Proof.* [AMRA\*]{.sans-serif} can either terminate after finding a solution in Line [\[line:solve_inad\]](#line:solve_inad){reference-type="ref" reference="line:solve_inad"} or [\[line:solve_anchor\]](#line:solve_anchor){reference-type="ref" reference="line:solve_anchor"}, or without a solution after exhausting all $OPEN_i$ and exiting the loop in Line [\[line:fail\]](#line:fail){reference-type="ref" reference="line:fail"}. Since $\mathcal{A}_0 = \bigcup_{r > 0}\mathcal{A}_r$ and any edge $e \in E_0$ is an action $a \in \mathcal{A}_0$, $V_0 = \bigcup_{r > 0} V_r$. A consequence of this is that any solution at any resolution $r \geq 0$ must exist in $G_0$. Furthermore, if [AMRA\*]{.sans-serif} exits the loop in Line [\[line:fail\]](#line:fail){reference-type="ref" reference="line:fail"}, no states in $V_0$ remain to be expanded. Thus, [AMRA\*]{.sans-serif} terminates in failure *iff* there is no solution in the graph $G_0$. ◻
:::

::: {#thm:suboptimality .theorem}
**Theorem 3**. *At the end of each iteration [AMRA\*]{.sans-serif} returns a solution, if one exists, that is at most $w_1 \times w_2$ suboptimal with respect to the optimal solution in graph $G_0 = (V_0, E_0)$.*
:::

::: proof
*Proof.* (Sketch) [AMRA\*]{.sans-serif} is complete with respect to $G_0$ (from Theorem [2](#thm:complete){reference-type="ref" reference="thm:complete"}). The anchor search is a [wA\*]{.sans-serif} search with a consistent heuristic and suboptimality factor $w_1$. Thus if [AMRA\*]{.sans-serif} terminates via the anchor search in Line [\[line:solve_anchor\]](#line:solve_anchor){reference-type="ref" reference="line:solve_anchor"}, $g(x_{\text{goal}}) \leq w_1 \times g^*(x_{\text{goal}})$ (from [@ARAFormal]). If [AMRA\*]{.sans-serif} terminates via an inadmissible heuristic in Line [\[line:solve_inad\]](#line:solve_inad){reference-type="ref" reference="line:solve_inad"}, $g(x_{\text{goal}}) \leq w_2 \times OPEN_0.\text{min}() \leq w_2 \times w_1 \times g^*(x_{\text{goal}})$ (from [@AineSNHL16]). Thus any solution returned by [AMRA\*]{.sans-serif} is at most $w_1 \times w_2$ suboptimal with respect to $G_0$. ◻
:::

# Experimental Results {#sec:exps}

## Illustrative Example

:::: {#fig:amra_ex .figure latex-placement="t"}
![](Saxena2021AMRA_figs/culdesac-eps-converted-to.png){width="0.9\\columnwidth"}

::: caption
[AMRA\*]{.sans-serif} execution on a 2D grid map with non-uniform costs. Start state (inside cul-de-sac) is in green, goal state in red, states expanded in cyan, and solution path in yellow. Each row is one iteration within [AMRA\*]{.sans-serif}, and each column shows expansions from different state space discretisations. Cell costs increase from purple to orange. Best viewed in colour.
:::
::::

Fig. [3](#fig:amra_ex){reference-type="ref" reference="fig:amra_ex"} shows a 2D grid navigation example to illustrate the behaviour showed by [AMRA\*]{.sans-serif}. We run [AMRA\*]{.sans-serif} on a $50 \times 50$ map with three levels of discretisation: high ($1 \times 1$), mid ($3 \times 3$), and low ($9 \times 9$). Each $1 \times 1$ cell in the map has an assigned cost in the range $[10, 260]$. The robot can execute actions on an 8-connected grid at all resolutions, and the cost of an action is the sum of costs of $1 \times 1$ cells along that action. Only a single Euclidean distance heuristic was used. After finding an initial solution mostly at the low resolution, [AMRA\*]{.sans-serif} expands more states at the finer resolutions over subsequent iterations to improve solution quality and finally terminates with the optimal solution for $w_1 = 1, w_2 = 1$.

## 2D Grid Navigation {#sec:2dexps}

::: table*
+--------------------------------------------------------+--------------------------------------------+-----------------------------+-------------------------------------+-------------------------------------------+---------------------------------------+-------------------------------------------+
|                                                        | **[AMRA\*]{.sans-serif}**                  | **[MRA\*]{.sans-serif}**    | **[ARA\*]{.sans-serif}** (High)     | **[ARA\*]{.sans-serif}** (Mid)            | **[ARA\*]{.sans-serif}** (Low)        | **[RRT\*]{.sans-serif}**                  |
+:=======================================================+:====================:+:===================:+:============:+:============:+:================:+:================:+:===================:+:===================:+:===============:+:===================:+:===================:+:===================:+
| 2-3(lr)4-5(lr)6-7(lr)8-9(lr)10-11(lr)12-13 **Metrics** | Cauldron (M1)        | TheFrozenSea (M2)   | M1           | M2           | M1               | M2               | M1                  | M2                  | M1              | M2                  | M1                  | M2                  |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
| Success $\%$                                           | 100                  | 100                 | 100          | 100          | 100              | 100              | 98                  | 99                  | 20              | 30                  | 100                 | 100                 |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
| $T_i (\si{\milli\second})$                             | 1.2 $\pm$ 0.98       | 1.08 $\pm$ 1.04     | 1.03$\times$ | 1.01$\times$ | 11.27$\times$    | 13.63$\times$    | 0.73$\mathbf\times$ | 0.49$\times$        | 0.27$\times$    | 0.32$\mathbf\times$ | 158.84$\times$      | 256.85$\times$      |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
| $T_f (\si{\milli\second})$                             | 280.39 $\pm$ 302.88  | 223.81 $\pm$ 280.36 | 1.4$\times$  | 1.37$\times$ | 1.13$\times$     | 1.46$\times$     | 0.07$\mathbf\times$ | 0.04$\mathbf\times$ | 0.07$\times$    | 0.05$\times$        | 53.88$\times$       | 30.36$\times$       |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
| $c_i$                                                  | 1163.06 $\pm$ 574.31 | 953.14 $\pm$ 480.8  | 1$\times$    | 1$\times$    | 1.02$\times$     | 1.01$\times$     | 1$\times$           | 0.98$\times$        | 1.19$\times$    | 1.38$\times$        | 0.74$\mathbf\times$ | 0.81$\mathbf\times$ |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
| $c_f$                                                  | 902.12 $\pm$ 403.27  | 754.7 $\pm$ 367.75  | 1$\times$    | 1$\times$    | 1$\times$        | 1$\times$        | 1.06$\times$        | 1.03$\times$        | 1.32$\times$    | 1.61$\times$        | 0.86$\mathbf\times$ | 0.85$\mathbf\times$ |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
| $\lvert V_0 \lvert \,(\times 10^4)$                    | 11.87 $\pm$ 11.63    | 9.51 $\pm$ 11.44    | 1.57$\times$ | 1.5$\times$  | 2.17$\times$     | 2.66$\times$     | 0.1$\mathbf\times$  | 0.1$\mathbf\times$  | 0.12$\times$    | 0.1$\mathbf\times$  | 6.1$\times$         | 1.71$\times$        |
+--------------------------------------------------------+----------------------+---------------------+--------------+--------------+------------------+------------------+---------------------+---------------------+-----------------+---------------------+---------------------+---------------------+
:::

We test the performance of [AMRA\*]{.sans-serif} for a 2D grid navigation task on two $1024\times1024$ maps from the MovingAI benchmark [@sturtevant2012benchmarks] shown in Fig. [4](#fig:2dmaps){reference-type="ref" reference="fig:2dmaps"}. The state space was discretised at three levels: high ($1 \times 1$), mid ($7 \times 7$), and low ($21 \times 21$). A four-connected action space was used at each resolution and a single Manhattan distance heuristic was used. For each map, 100 random start and goal states were sampled at the low resolution. In this experiment, we compare the multi-resolution and anytime behaviour of [AMRA\*]{.sans-serif} against [MRA\*]{.sans-serif} and also [ARA\*]{.sans-serif} run at each of the three resolutions denoted as "[ARA\*]{.sans-serif}(High)", "[ARA\*]{.sans-serif}(Mid)" and "[ARA\*]{.sans-serif}(Low)". Since [MRA\*]{.sans-serif} is not anytime, we ran a succession of [MRA\*]{.sans-serif} searches with the same schedule of suboptimality weights as [AMRA\*]{.sans-serif}. Additionally, we compare against an asymptotically optimal sampling-based planner [RRT\*]{.sans-serif} [@KaramanF11] from OMPL [@sucan2012the-open-motion-planning-library].

Table [\[tab:2dexps\]](#tab:2dexps){reference-type="ref" reference="tab:2dexps"} presents the result of these experiments. We report six metrics: success rate, times to initial and final solutions ($T_i$ and $T_f$ respectively, in milliseconds), costs of initial and final solutions ($c_i$ and $c_f$ respectively), and the number of state expansions $\lvert V_0 \lvert$[^4]. All planners were given a $5 \si{\second}$ timeout. We report raw numbers for [AMRA\*]{.sans-serif} and relative numbers for the other algorithms, averaged over the 100 trials.

[AMRA\*]{.sans-serif} is faster than the complete search-based baselines ([MRA\*]{.sans-serif} and [ARA\*]{.sans-serif}(High)) and expands fewer states, while converging to the optimal solution. The convergence behaviour of these algorithms is shown in Fig. [5](#fig:converge){reference-type="ref" reference="fig:converge"}. [AMRA\*]{.sans-serif} is also much faster than [RRT\*]{.sans-serif}[^5], albeit finding costlier solutions on a discretised grid representation of the environment.

:::: {#fig:2dmaps .figure latex-placement="t"}
![](Saxena2021AMRA_figs/2d-eps-converted-to.png){width="0.7\\columnwidth"}

::: caption
The four Starcraft maps from the MovingAI benchmark used for 2D grid navigation experiments: Cauldron (*left*) and TheFrozenSea (*right*). [Green]{style="color: Green"} and black areas are obstacles.
:::
::::

:::: {#fig:converge .figure latex-placement="t"}
![](Saxena2021AMRA_figs/trend-eps-converted-to.png){width="0.6\\columnwidth"}

::: caption
Performance of search algorithms on TheFrozenSea map from Fig. [4](#fig:2dmaps){reference-type="ref" reference="fig:2dmaps"}. Data was averaged over 100 runs. The x-axis is in log scale. [MRA\*]{.sans-serif} was run iteratively as described in Sec. [7.2](#sec:2dexps){reference-type="ref" reference="sec:2dexps"}.
:::
::::

## UAV Navigation {#sec:uavexps}

::: table*
+-----------------------------------------------+-----------------------------------------+---------------------------------+---------------------------------------+-------------------------------------------+------------------------------------------+
|                                               | **[AMRA\*]{.sans-serif}**               | **[MRA\*]{.sans-serif}** (E)    | **[MRA\*]{.sans-serif}** (Dubins)     | **[MRA\*]{.sans-serif}** (Dijkstra)       | **[A-MHA\*]{.sans-serif}** (High)        |
+:==============================================+:==================:+:==================:+:==============:+:==============:+:=================:+:=================:+:===================:+:===================:+:=================:+:====================:+
| 2-3(lr)4-5(lr)6-7(lr)8-9(lr)10-11 **Metrics** | Boston (M1)        | NewYork (M2)       | M1             | M2             | M1                | M2                | M1                  | M2                  | M1                | M2                   |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
| $T_i (\si{\second})$                          | 0.31 $\pm$ 0.25    | 0.26 $\pm$ 0.23    | 0.69$\times$   | 1.4$\times$    | 1.11$\times$      | 0.33$\times$      | 1.01$\mathbf\times$ | 1.04$\times$        | 0.94$\times$      | 0.94$\mathbf\times$  |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
| $T_f (\si{\second})$                          | 10.46 $\pm$ 10.77  | 9.54 $\pm$ 10.65   | 1.9$\times$    | 1.97$\times$   | 3.4$\times$       | 3.46$\times$      | 0.74$\mathbf\times$ | 0.75$\mathbf\times$ | 12.32$\times$     | 19.89$\times$        |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
| $c_i$                                         | 135.64 $\pm$ 66.15 | 109.48 $\pm$ 49.52 | 1.12$\times$   | 1.06$\times$   | 1.36$\times$      | 1.37$\times$      | 1.04$\times$        | 0.98$\times$        | 1.86$\times$      | 2.07$\times$         |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
| $c_f$                                         | 105.34 $\pm$ 46.61 | 92.47 $\pm$ 39.46  | 1$\times$      | 1$\times$      | 1$\times$         | 1$\times$         | 1$\times$           | 1$\times$           | 2.23$\times$      | 2.35$\times$         |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
| $\lvert V_0 \lvert \,(\times 10^5)$           | 1.74 $\pm$ 1.9     | 1.56 $\pm$ 1.87    | 1.27$\times$   | 1.4$\times$    | 4.84$\times$      | 4.15$\times$      | 0.82$\mathbf\times$ | 0.83$\mathbf\times$ | 20.59$\times$     | 42.99$\mathbf\times$ |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
| Timeout $\%$                                  | 15                 | 12                 | 39             | 29             | 30                | 23                | 6                   | 4                   | 74                | 82                   |
+-----------------------------------------------+--------------------+--------------------+----------------+----------------+-------------------+-------------------+---------------------+---------------------+-------------------+----------------------+
:::

The second set of experiments studies the multi-heuristic capabilities of [AMRA\*]{.sans-serif} in addition to the multi-resolution and anytime behaviour. We solve kinodynamic motion planning problems for a 4D UAV robot modeled with double integrator dynamics. The state space of the robot is $(x, y, \theta, v)$ - its 2D pose in $SE(2)$ and linear velocity. The motion primitives used for the search algorithms are shown in Fig. [6](#fig:mprims){reference-type="ref" reference="fig:mprims"}. They exist at two resolutions for the 2D position: $3\si{\meter}$ (high) and $9\si{\meter}$ (low). The heading $\theta$ can take 12 discrete values in $[0, 2\pi)$, and the velocity $v$ can be $\{0, 3, 8\} \si{\meter\per\second}$ at the end of a primitive. The cost of an action is its duration, thus we are solving for the least-time path in this experiment.

:::: {#fig:mprims .figure latex-placement="t"}
![](Saxena2021AMRA_figs/mprims-eps-converted-to.png){width="0.55\\columnwidth"}

::: caption
Motion primitives for UAV navigation. High resolution primitives are in [green]{style="color: Green"}, and low resolution primitives are in [red]{style="color: Red"}.
:::
::::

We use three inadmissible heuristics for this experiment: Euclidean distance to the goal (always used as the admissible anchor heuristic as well), Dubins path [@Dubins] distance to the goal, and a backwards Dijkstra search from the goal. [AMRA\*]{.sans-serif} uses all three heuristics at both resolutions. 100 random start and goal states were sampled in two maps shown in Fig. [7](#fig:uavmaps){reference-type="ref" reference="fig:uavmaps"} at the low resolution, and planners were given a timeout of $30 \si{\second}$. We compare against two search-based algorithms: [MRA\*]{.sans-serif} and [A-MHA\*]{.sans-serif}. The former is not a multi-heuristic algorithm, thus we compare against instantiations which use different heuristics: "[MRA\*]{.sans-serif}(E)", "[MRA\*]{.sans-serif}(Dubins)", and "[MRA\*]{.sans-serif}(Dijkstra)". We also compare against "[A-MHA\*]{.sans-serif}(High)" since that is not a multi-resolution algorithm. "[A-MHA\*]{.sans-serif}(Low)" was unable to find any solutions across the $2\times100$ problems.

Table [\[tab:uavexps\]](#tab:uavexps){reference-type="ref" reference="tab:uavexps"} shows the results of these experiments. As in Section [7.2](#sec:2dexps){reference-type="ref" reference="sec:2dexps"}, we present raw numbers for [AMRA\*]{.sans-serif} and relative numbers for the other baselines, averaged over 100 trials. Since all these algorithms succeeded in finding an initial solution, we report the timeout percentage (percentage of problems that reached the planning timeout before finding the final solution) in place of success rate. Overall, [AMRA\*]{.sans-serif} is the most consistent algorithm when compared against the baselines. It finds the optimal solution much faster than "[MRA\*]{.sans-serif}(E)", "[MRA\*]{.sans-serif}(Dubins)", and "[A-MHA\*]{.sans-serif}(High)" and with fewer timeouts. In most cases it is also quicker to find the first solution than all [MRA\*]{.sans-serif} variants. "[MRA\*]{.sans-serif}(Dijkstra)" is the most competitive baseline as it finds the optimal solution quicker, with fewer expansions and fewer timeouts. This comparison shows the effect of the overhead of [AMRA\*]{.sans-serif} using multiple heuristics and multiple resolutions.

:::: {#fig:uavmaps .figure latex-placement="t"}
![](Saxena2021AMRA_figs/uav-eps-converted-to.png){width="0.7\\columnwidth"}

::: caption
The two city/street maps from the MovingAI benchmark used for UAV navigation experiments: Boston_0_1024 (*left*) and NewYork_0_1024 *right*. Given the fixed discretisations for $\theta$ and $v$, there are roughly $2.8 \times 10^7$ valid states in these maps.
:::
::::

# Discussion & Future Work {#sec:future}

In this work we present [AMRA\*]{.sans-serif} an anytime, multi-resolution, multi-heuristic search algorithm that generalises several existing search algorithms into one unified algorithm. It it very flexible for robot motion planning problems that have previously benefited from anytime algorithms, multiple heuristics, and multiple resolutions in separate lines of research. [AMRA\*]{.sans-serif} exhibits impressive performance on two very different planning domains in 2D grid navigation and 4D kinodynamic UAV planning.

[AMRA\*]{.sans-serif} at its core utilises multiple action spaces. Plenty of robotic systems are capable of a diverse set of actions that may dynamically become available to the robot given the state it is in. For example, a robot arm might plan in free space with simple motor primitives (independent joint angle changes), but might need to resort to prehensile and non-prehensile interaction actions in the vicinity of clutter. [AMRA\*]{.sans-serif} opens the door for developing search algorithms that reason about such dynamically evolving action spaces that include both robot-centric and object-centric actions.

[^1]: The authors are with the Robotics Institute, Carnegie Mellon University, Pittsburgh, PA 15213, USA. e-mail: `{dsaxena, tkusnur, mlikhach}@andrew.cmu.edu`. This work was sponsored by Mitsubishi Heavy Industries, Ltd.

[^2]: van den Berg et. al [@BergSHG11] also contain a more thorough list of anytime [A\*]{.sans-serif} algorithms.

[^3]: For the sake of simplicity, we refer to all non-anchor heuristics as 'inadmissible'.

[^4]: For [RRT\*]{.sans-serif}, $\lvert V_0 \lvert$ is the number of vertices in the final tree.

[^5]: The termination criteria for [RRT\*]{.sans-serif} was computing 10 solutions in a row whose costs were within $10\%$ of each other.
