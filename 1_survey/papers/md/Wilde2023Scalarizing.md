---
citation_key: Wilde2023Scalarizing
arxiv_id: 2312.07227
arxiv_url: https://arxiv.org/abs/2312.07227
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:14:15Z
origin: ai+web
reviewed: false
---

# Introduction

:::: {#fig:intro .figure latex-placement="ht"}
![Ground set of feasible trajectories. Pareto-optimal solutions are highlighted in colour.](Wilde2023Scalarizing_figs/ground_set.png){#fig:intro_all width="100%"}

![Attainable solutions for weighted sum (WS) optimization.](Wilde2023Scalarizing_figs/weighted_sum.png){#fig:intro_lin width="100%"}

![Attainable solutions for the proposed weighted maximum (WM) optimization.](Wilde2023Scalarizing_figs/weighted_max.png){#fig:intro_cheb width="100%"}

::: caption
A simple planning problem with two objectives: trajectory length and the minimum distance to an obstacle. Shown are the ground set of trajectories (a), the solutions when using a weighted sum objective (b), and the solutions when using the proposed weighted maximum objective (c). In each subfigure the left plot shows the set of trajectories and the right plot shows the corresponding trade-offs. Colored trade-offs are Pareto-optimal, *i.e.,* show the Pareto-front.
:::
::::

Automated planning and decision making plays a central role in designing intelligent robotic systems. In many real-world settings, autonomous robots are faced with complex scenarios that require them to balance between different objectives simultaneously. For instance, autonomous vehicles need to navigate to a goal, while ensuring safety, passenger comfort and ideally fuel-efficiency [@levinson2011towards; @christianos2023planning; @botros2022tunable]. Similarly, mobile robots navigating in human-centered spaces such as offices, hospitals or public areas need to consider task efficiency and conforming to social norms [@wilde2020improving; @biswas2022socnavbench].

In multi-objective optimization (MOO) problems -- such as finding trajectories trading off different objectives -- the optimal solution is usually not unique, but rather there is a set of *Pareto-optimal* solutions. A solution is Pareto-optimal when none of the individual objectives can be improved without worsening at least one other objective. Thus, an important challenge in motion planning remains the design of objective functions that balance between several potentially competing objectives and allow for computing Pareto-optimal solutions. A common approach is to formulate a weighted sum of the objective functions [@wilde2020improving; @zucker2013chomp; @christianos2023planning; @lu2020motion]. Often, the weights on the objectives are tuning-parameters, requiring careful calibration. In human-robot interaction (HRI) user preferences for robot behaviour is commonly modelled as a weighted sum of features [@abbeel2004apprenticeship; @hadfield2016cooperative; @sadigh2017active; @biyik2019asking; @wilde2020improving; @habibian2022here]. The linear structure allows for designing efficient algorithms for both motion planning and learning from human feedback making this approach very popular.

However, it can fail to describe all optimal trade-offs since it is unable to explore non-convex regions of Pareto-fronts. This issue persists even in simple planning problems, as illustrated in Figure [4](#fig:intro){reference-type="ref" reference="fig:intro"}. Here we compute trajectories between a fixed start and goal position around two static obstacles. To optimize for trajectory length and the minimal distance to an obstacle we can inflate the obstacles and then plan paths on visibility graphs. Subplot [1](#fig:intro_all){reference-type="ref" reference="fig:intro_all"} shows the ground set of feasible trajectories together with the corresponding Pareto-front. Subplot [2](#fig:intro_lin){reference-type="ref" reference="fig:intro_lin"} shows the trajectories that can be computed with the weighted sum (WS) method for different weights. We observe that the trajectories found by the WS method are only a small subset of the Pareto-optimal solutions from [1](#fig:intro_all){reference-type="ref" reference="fig:intro_all"}: While there are numerous trajectories available that pass between the two obstacles, there are only few that go around. It is important to notice that this is not due to the choice or resolution of the weights. Rather, *there does not exist any tuning of weights* such that the motion planner returns a more intermediate trade-off, since parts of the Pareto-front are non-convex [@branke2008multiobjective]. This problem occurs when parts of the Pareto-front are non-convex: the solutions of the weighted sum method do only cover the convex hull of the Pareto-front [@branke2008multiobjective].

We study an alternative form of scalar objective function, the *weighted maximum* (WM) of objectives, also known as Chebyshev scalarization [@branke2008multiobjective]. This allows for finding a richer set of trade-offs between the two objectives as shown in subplot [3](#fig:intro_cheb){reference-type="ref" reference="fig:intro_cheb"}, covering all parts of the Pareto-front. Indeed, this approach is able to find all Pareto-optimal solutions, *i.e.,* is *Pareto-complete* [@branke2008multiobjective]. Despite the theoretical foundations established in the optimization literature, more expressive scalarization methods such as the WM have not found much attention in robot motion planning. To demonstrate the potential of WM optimization in robot motion planning we discuss fundamental shortcomings of widely used WS cost functions, independent of how weights are selected. We revisit established results from optimization to describe theoretical differences between WS and WM cost functions: WM cost is a provably more expressive tool for motion planning, yet only requires the same number of parameters. We show how WM costs can be used in continuous and discrete space planning problems. For discrete planning, we consider a general monotonic utility function to combine objective values of discrete actions (*e.g.,* edges in graphs), allowing for complex planning.

## Contributions

Our contributions are as follows: First, we consider continuous-space planning problems and show how existing optimization techniques can be used to solve planning problems with WM cost functions. Further, show NP-hardness of graph based path planning with a WM cost. Second, we present a novel optimal path planning algorithm for the WM cost and establish its correctness. Further, we show how our algorithm can be enhanced with a cost-to-go heuristic and discuss a budgeted suboptimal version that runs in polynomial time. Third, in a series of simulations, we demonstrate that the proposed WM method finds a substantially richer set of trade-offs in various motion planning problems, and showcase that the proposed graph search finds optimal solutions within a practical runtime.

## Related work

Many robot planning problems consider multiple, potentially competing objectives. The most prominent approach is to formulate a weighted sum of a given set of objective functions and then solve the resulting scalar optimization problem. This approach is used in trajectory planning for autonomous driving [@tunable_traj_planner_urban; @levinson2011towards; @christianos2023planning; @karkusdiffstack; @botros2022tunable; @zuo2020mpc; @hang2020integrated], local planning in cluttered environments [@lu2020motion; @de2022risk] or social spaces [@che2020efficient; @brito2019model], trajectory generation for manipulators [@zucker2013chomp; @marcucci2022motion], and multi-robot planning [@luis2020online; @cap2018multi].

Researcher in HRI use weighted sums of objective functions -- usually referred to as features -- to model how users evaluate robot behaviour [@abbeel2004apprenticeship; @wilde2021learning; @hadfield2016cooperative; @sadigh2017active; @wilde2020active; @biyik2019asking; @wilde2022learning; @habibian2022here]. In human-in-the-loop learning frameworks users provide feedback to a robot in form of demonstrations, choice, labels, critic, and others, allowing the robot to learn weights for the objective functions and thus adapt their behaviour to the user's preferences.

Different approaches that address the shortcomings of WS objectives include alternative scalar functions such as the WM approach, or incremental algorithms that iteratively explore the entire Pareto-front [@branke2008multiobjective]. A popular approach that can explore non-convex Pareto-fronts is the Adapt Weighted Sum Method [@kim2005adaptive; @kim2006adaptive]. Here solutions are sampled iteratively using equality constraints to force new samples to close gaps in the Pareto-front. Yet, this approach is solving a slightly different problem than we are addressing: The method iteratively creates a set of potential solutions that cover the Pareto-front. Thus, it does not have tuning parameters such that carefully choosing them allows for obtaining the desirable solution. Further, the approach does not come with a completeness guarantee and can get stuck when the Pareto-front is discontinuous. Lastly, satisfying the added equality constraints can be infeasible or computationally hard in practice, especially in discrete-space planning. In our work, we propose using a WM cost function which has tunable weights such that any Pareto-optimal solution can be attained for a specific weight vector. Further, we explicitly address the challenges in discrete space planning and propose a novel graph search for minimizing WM costs for different types of individual objective functions.

Overall, the limitations of WS costs find less discussion in the context of robot planning. Recently, [@thoma2023prioritizing] compared different scalar objective functions. Our work focuses on the WM cost function only, yet provides a theoretical analysis of its expressiveness and presents a novel algorithm for discrete space planning. Other works directly address MOO for specific problems. For instance, the authors of [@yi2015morrf] studied weighted sum and weighted minimum approach for exploring Pareto-fronts of sampling based motion planning problems, while [@sakcak2021complete] addresses the problem of simultaneously optimizing for path length and clearance in the plane, proposing a complete and efficient algorithm. WM cost functions also found attention in multi-objective Reinforcement Learning (RL) [@van2013scalarized; @chen2019meta]. The works of [@ding2014hierarchical] and [@bopardikar2015multiobjective] study hierarchical frameworks based on a multi-objective Probabilistic Roadmap (MO-PRM) and explicitly consider two objectives: path length and risk [@ding2014hierarchical], and path length and state-estimation error [@bopardikar2015multiobjective]. The MO-PRM separates objectives in primary and secondary costs, and then plans using a discretization of values for the secondary costs, similar to the $\epsilon$-constrained method [@branke2008multiobjective]. A drawback of that method is that it depends on the resolution of the constraint on the secondary cost and can require solving multiple optimization problems in order to verify Pareto-optimality. In contrast to these works, our paper does not address a specific multi-objective motion planning problem, but rather proposes an alternative to weighted sums for *any* collection of objective functions.

# Problem Statement

In this section, we revisit some preliminary concepts before introducing our formal problem statement.

## Preliminaries

#### Pareto-optimality

Consider a multi-objective optimization problem where the domain is some vector space $\mathcal{X}$. We want to find a solution $\boldsymbol{x}\in \mathcal{X}$ that simultaneously minimizes $n$ different functions, *i.e.,* that solves $\min_{\boldsymbol{x}}\{f_1(\boldsymbol{x}), \dots, f_n(\boldsymbol{x})\}$. In general, the solution to a MOO problem is not a unique vector $\boldsymbol{x}$, but a set of *Pareto-optimal* solutions. We briefly review the definitions of *dominated solutions* and the Pareto-front.

::: definition
**Definition 1** (Dominated solution). Given a MOO problem and two solutions $\boldsymbol{x},\boldsymbol{x}'\in\mathcal{X}$. Vector $\boldsymbol{x}$ *dominates* $\boldsymbol{x}'$ when $f_i(\boldsymbol{x})\leq f_i(\boldsymbol{x}')$ holds for all $i=1,\dots,n$, and $f_j(\boldsymbol{x})< f_j(\boldsymbol{x}')$ holds for at least one $j$ where $1\leq j\leq n$.
:::

::: definition
**Definition 2** (Pareto-front). Given a MOO problem, the set of *Pareto-optimal* solutions -- called *Pareto-front* -- is the subset of all solution that are not *dominated* by another solution.
:::

#### Graph theory

Following [@korte2011combinatorial], a graph is a tuple $G=(V,E)$ where $V$ are vertices and $E$ is a set of edges. In a weighted graph $G=(V,E,d)$ edges are associated with some cost $d:E\to \mathbb{R}$. A walk is a sequence $v_1, e_1, v_2,\dots, v_k,e_k,v_{k+1}$ such that $e_i=(v_i,v_{i+1})\in E$ and $e_i\neq e_j$ for $i,j=1,\dots,k$. We define a path $P$ as a sequence of vertices $(v_1, \dots, v_{k+1})$ with no duplicate entries for which there exists a walk $v_1, e_1, v_2,\dots, v_k,e_k,v_{k+1}$ in $G$.

## Problem Formulation

We consider a planning problem described by a robot's state and action space $(\mathcal{X}, \mathcal{A})$, a start state $x_s$ and a set of goal states $X_g\subset\mathcal{X}$. Let $\mathcal{T}$ be the set of all feasible trajectories starting at $x_s$ and ending at some state $x_g\in X_g$. Note that the set $\mathcal{T}$ is typically defined implicitly as set of constraints on the robot's state and actions, such as kinodynamic constraints on motion, or spatial constraints for obstacle avoidance. We keep this set abstract at this point, but give specific examples in Section [5](#sec:results){reference-type="ref" reference="sec:results"}.

To define the desired robot behaviour the designer of a motion planner considers a set objectives to be minimized. Let these objectivess be denoted by $f_1, \dots, f_n$ where $f_i:\mathcal{T}\to \mathbb{R}_{\geq0}$ for $i=1,\dots,n$. The optimal solution to the motion planning problem is some trajectory $T^*\in\mathcal{T}$. Assuming that the objectives $f_1, \dots, f_n$ contain all aspects under consideration, $T^*$ is a Pareto-optimal solution to the problem $$\begin{equation}
\min_{T\in \mathcal{T}}\{f_1(T), \dots, f_n(T)\}.
\label{eq:MOO problem}
\end{equation}$$ Let $\mathcal{T}'\subseteq \mathcal{T}$ denote the set of all Pareto-optimal solutions. Given above definitions, we can pose our main problem.

::: {#prob:main_prob .problem}
**Problem 1** (Parametric single objective planning).

Given state and action space $(\mathcal{X}, \mathcal{A})$, initial state $x_s$ and goal states $X_g$, and objectives $f_1, \dots, f_n$ find an algorithm such that, for any Pareto-optimal solution $T^*\in \mathcal{T}'$, there exists algorithm parameters for which the algorithm returns $T^*$.
:::

Our approach to Problem [1](#prob:main_prob){reference-type="ref" reference="prob:main_prob"} is writing [\[eq:MOO problem\]](#eq:MOO problem){reference-type="eqref" reference="eq:MOO problem"} as a scalar function where tuning weights $\boldsymbol{w}$ define the balance between objectives. The scalar function needs to be solvable, and for any Pareto-optimal trajectory $T^*\in\mathcal{T}$ there exist a choice of weights such that $T^*$ is the solution to the scalar optimization problem.

# Approach

A common approach to tackle Problem [1](#prob:main_prob){reference-type="ref" reference="prob:main_prob"} is solving the MOO problem from [\[eq:MOO problem\]](#eq:MOO problem){reference-type="eqref" reference="eq:MOO problem"} via means of linear scalarization, also referred to as the weighted sum (WS) method or cost [@branke2008multiobjective]. This yields the following cost function $$\begin{equation}
c^{\mathtt{sum}}(T) = \sum_{i=1}^n f_i(T) w_i = \boldsymbol{f}(T)\cdot \boldsymbol{w},
\label{eq:lin_cost}
\end{equation}$$ where $\boldsymbol{w}\in[0,1]^n$ is a vector of tunable weights. While this approach has been widely used and been proven to be effective, its simplicity limits the expressiveness. In this paper, we offer an alternative model-based approach. We propose a weighted maximum approach for a scalar cost functions, where the summation is replaced by taking the maximum: $$\begin{equation}
c'(T) = \max_{i=1,\dots,n} f_i(T) w_i.
\label{eq:cheb_cost_raw}
\end{equation}$$

The cost of a trajectory is now given by the objective that attains the largest value when multiplied by its weight. That is, a trajectory is evaluated only based on the most prominent weighted objective value, and disregards other objectives. We notice that when the solution to [\[eq:cheb_cost_raw\]](#eq:cheb_cost_raw){reference-type="eqref" reference="eq:cheb_cost_raw"} is unique, it is Pareto-optimal. However, if there are multiple solutions, then one is Pareto-optimal, while all others are only *weakly* Pareto-optimal [@branke2008multiobjective]. In order to only attain Pareto-optimal solutions, we add $\rho\sum_{i=1}^n f_i(T)$ as a tie-break in the cost function, where $\rho> 0$ is a sufficiently small constant: $$\begin{equation}
c^{\mathtt{max}}(T) = \max_{i=1,\dots,n} f_i(T) w_i + \rho \sum_{i=1}^n f_i(T).
\label{eq:cheb_cost}
\end{equation}$$

We refer to this as the weighted maximum (WM), or *augmented Chebyshev problem* [@branke2008multiobjective]. Next, we characterize its expressiveness compared to the WS. Given a planning problem with the ground set of feasible trajectories $\mathcal{T}$, let $\mathcal{T}'\subseteq \mathcal{T}$ be the set of all Pareto-optimal trajectories. Further, let $\mathcal{T}^{\mathtt{sum}} \subseteq\mathcal{T}$ be the set of trajectories that are optimal for *some* weight in [\[eq:lin_cost\]](#eq:lin_cost){reference-type="eqref" reference="eq:lin_cost"} and let $\mathcal{T}^{\mathtt{max}} \subseteq\mathcal{T}$ be the set of trajectories that are optimal for *some* weights in [\[eq:cheb_cost\]](#eq:cheb_cost){reference-type="eqref" reference="eq:cheb_cost"}. In detail, we have $\mathcal{T}^{\mathtt{sum}} = \{T' \in \mathcal{T}\ | \ T' = \arg\min_T c^{\mathtt{sum}}(T),\ \boldsymbol{w}\in[0,1]^n\}$, and $\mathcal{T}^{\mathtt{max}} = \{T' \in \mathcal{T}\ | \ T' = \arg\min_T c^{\mathtt{max}}(T),\ \boldsymbol{w}\in[0,1]^n\}$. We revisit a known result:

::: lemma
**Lemma 1** (Pareto-optimality of scalarization). For any planning problem $\mathcal{T}^{\mathtt{sum}} \subseteq\mathcal{T}^{\mathtt{max}} \subseteq\mathcal{T}'$.
:::

A proof is omitted since this is a well established result in multi-objective optimization [@branke2008multiobjective]. The lemma ensures that any solution to the two scalarized optimization methods is always a Pareto-optimal solution. However, a lesser known result is while all solutions to [\[eq:lin_cost\]](#eq:lin_cost){reference-type="eqref" reference="eq:lin_cost"} are Pareto-optimal, there can exist Pareto-optimal solutions that are not a solution to [\[eq:lin_cost\]](#eq:lin_cost){reference-type="eqref" reference="eq:lin_cost"} for any $\boldsymbol{w}$. Thus, the WS is less expressive than the WM.

::: {#prop:expressive .proposition}
**Proposition 1** (Expressiveness). Given a planning problem where trajectories $T$ are parametrized in $\mathbb{R}^m$, and auxiliary cost functions $\boldsymbol{f}(T)=[f_1(T)\, \dots\, f_n(T)]$. If at least one of the cost functions $f_i(T)$ is not a proper convex[^3] and continuous function over $\mathbb{R}^m$ then $\mathcal{T}^{\mathtt{sum}}\subset \mathcal{T}^{\mathtt{max}}$, *i.e.,* optimizing [\[eq:lin_cost\]](#eq:lin_cost){reference-type="eqref" reference="eq:lin_cost"} is strictly less expressive than optimizing [\[eq:cheb_cost\]](#eq:cheb_cost){reference-type="eqref" reference="eq:cheb_cost"}.
:::

The proof follows directly from Theorem 6.3 and Remark 6.4 in [@censor1977pareto]: Linear scalarization is only Pareto-complete when the costs are proper convex and continuous. Thus, when that condition is violated we have $\mathcal{T}^{\mathtt{sum}}\subset \mathcal{T}'$. In contrast, the WM is Pareto-complete [@branke2008multiobjective], *i.e.,* $\mathcal{T}^{\mathtt{max}}=  \mathcal{T}'$ always holds.

The effect of Proposition [1](#prop:expressive){reference-type="ref" reference="prop:expressive"} becomes apparent in Figure [4](#fig:intro){reference-type="ref" reference="fig:intro"}. When there is more than one homotopy class for navigating around obstacles, the objective for minimizing closeness to obstacles becomes non-convex. As a consequence, the Pareto-front is non-convex. The WS method is then only able to find solutions lying on the convex hull of the Pareto-front, while the WM method finds solutions in all parts of the Pareto-front.

# Motion planning with weighted maximum cost

We now consider the problem of finding an optimal trajectory for the proposed WM cost for given weights $\boldsymbol{w}$. Thus, we study how the WM cost can be used in continuous space motion planners such as Model-Predictive Control (MPC), and in discrete, graph-based planners such as state-lattices.

## Continuous space planning

We consider a discrete time, continuous space planning problem to find an optimal trajectory $T$, subject to kinodynamical constraints $g(T) \leq 0$. When minimizing the proposed WM cost, the problem may be written as $$\begin{equation}
\begin{aligned}
\label{eq:continuous}
\min_{T} &\,\max_i f_i(T) w_i + \rho\sum_{i=1}^n f_i(T)\\
s.t.&\, g(T)\leq 0.
\end{aligned}
\end{equation}$$ Following [@boyd2004convex], this can be reformulated as follows $$\begin{equation}
\label{eq:continuous_reformulated}
\begin{aligned}
    \min_T &\;t + \rho\sum_{i=1}^n f_i(T)\\
    s.t.&\,\max_i\ w_i f_i(T)  \leq t\; \text{for } i=1,\dots,n,\\
    &\,g(T)\leq0.
\end{aligned}
\end{equation}$$ The newly introduced max constraint can be written out as $n$ constraints of the form $w_i f_i(T)  \leq t$ for $i=1,\dots, n$. We observe that this removes the maximization from the problem, such that the objective and constraints are linear compositions of the individual objective $f_i$. In case constraints $g(T)$ are non-convex, solving for the weighted maximum does not make the problem fundamentally harder than optimizing for the weighted sum. However, the same does not hold for graph-based planners as we will show next.

## Graph based planning

We now consider the WM cost for discrete space motion planners such as graph or lattice based methods and characterize the hardness of the problem. Let $G=(V,E)$ be a graph where we associate each edge $e\in E$ with non-negative and bounded trajectory costs $f'_1(e), \dots, f'_n(e)$.\

#### LP formulation

We briefly consider the simple case where the costs of a path are the sum of the edge costs $f_i(P)=\sum_{e\in E(P)} f_i(e)$. We recall the linear program (LP) formulation of a shortest path problem, *i.e.,* a path minimizing [\[eq:lin_cost\]](#eq:lin_cost){reference-type="eqref" reference="eq:lin_cost"}. Thus, the cost of an edge $e$ is given by $\boldsymbol{f}(e) \cdot \boldsymbol{w}$, and the network flow constraints are summarized as $F(\boldsymbol{x})\leq\boldsymbol{b}$. The well-known LP-formulation [@bertsimas1997introduction] then is $$\begin{equation}
\begin{aligned}
    \min_{\boldsymbol{x}} &\; \sum_{(v,u)} x_{vu}\cdot\boldsymbol{f}(e_{vu}) \cdot \boldsymbol{w}\\
    s.t.&\, F(\boldsymbol{x})\leq \boldsymbol{b}.
\end{aligned}
\label{eq:shortest_path_LP}
\end{equation}$$ Here $\boldsymbol{x}$ is a binary vector, where $x_{vu}=1$ indicates that edge $(v,u)$ is contained in the path. When now considering the WM cost, the objective is $\min_{\boldsymbol{x}} \;\max_i \  w_i \sum_{(v,u)} x_{vu}\cdot f'_i(e_{vu})+ \rho\sum_{i=1}^n f_i(e_{vu})$. In principle, we can apply the same re-formulation technique as in equation [\[eq:continuous_reformulated\]](#eq:continuous_reformulated){reference-type="eqref" reference="eq:continuous_reformulated"} and still obtain an LP. However, the solution will not have integer values since the constraints are no longer totally-unimodular. Hence, the LP solution will not solve the shortest path problem [@bertsimas1997introduction].

#### Formal problem analysis

Given that the LP-formulation for shortest paths does not work for the WM cost, we study the problem of finding a path that minimizes [\[eq:cheb_cost\]](#eq:cheb_cost){reference-type="eqref" reference="eq:cheb_cost"} in more detail. We consider the general case where the costs of a path $P$ are not necessarily the sum of the edge costs in the path. Instead, the cost for a path $P$ with edges $E(P)$ is $$\begin{equation}
\label{eq:path_costs}
f_i(P)=\beta(f'_i(e_1), f'_i(e_2), \dots), \text{ where } e_1, e_2, \dots \in E(P).
\end{equation}$$ We refer to $\beta$ as the composition function and assume that $\beta$ is monotonically increasing. This captures two widely used concepts of defining costs over a robot's trajectory: i) summation or integration over the trajectory to compute its length, time, integral square jerk, accumulated risk or similar costs, and ii) taking the maximum value over a trajectory such as the maximum jerk or maximum risk. Thus, we can state the problem of finding a path of minimal maximum weighted cost.

::: {#prob:mincostPath .problem}
**Problem 2** (Min-max cost path (MMCP)). Given a strongly connected graph $G=(V,E)$ with start and goal vertices $s,g$ in $V$, edge cost functions $f'_1(e), \dots, f'_n(e)$, a composition function $\beta$, and weights $w_1, \dots, w_n$, find a path that solves $$\begin{equation}
    \min_P \max_i w_i f_i(P)+ \rho\sum_{i=1}^n f_i(P).
\end{equation}$$
:::

The problem is closely related to the multi-objective shortest path (MOSP) problem, which is NP-hard for two or more objectives. [@ehrgott2005multicriteria]. The main difference is that MOSP considers that $\beta$ is taking the sum over different edge cost, which makes it a special case of Problem [2](#prob:mincostPath){reference-type="ref" reference="prob:mincostPath"}. We formally establish hardness of our problem.

::: proposition
**Proposition 2** (Hardness of MMCP). The MMCP is NP-hard.
:::

We consider the special case that $f_i(P) = \sum_{e\in E(P)} f_i(e)$. The decision version of MMCP decides if there exists a path such that the $\max_i w_i f_i(P) \leq \alpha$ for some constant $\alpha$. We can reduce MOSP to MMCP. MOSP takes as an input a graph $G=(V,E)$ and some cost functions $\gamma_1,\dots, \gamma_n$ assigning costs to edges. The decision version answers if there exists a path $P$ such that $\sum_{e\in E(P)}\gamma_i(e)\leq \alpha$ for all $i$ and some constant $\alpha$. Given an instance of MOSP, we use the same graph as an input for MMCP, choose costs $f_i(e)=\gamma_i(e)$, and set $w_i=1$ for $i=1,\dots,n$. The solution to MMCP then indicates if $\max_i\sum_{e\in E(P)}\gamma_i(e)\leq \alpha$, which trivially also decides the MOSP instance.

#### Algorithm description

We now present a complete algorithm for MMCP, detailed in Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"}. Our approach is a modification to Dijkstra's algorithm where we record all paths to a vertex, similar to the *Martin algorithm* for MOSP [@gandibleux2006martins]. To that end, the elements in our $\mathtt{open\_list}$ are tuples consisting of a cost, a vertex, and a path (*i.e.,* a sequence of preceding vertices) from the start to this vertex. Similar to Dijkstra's our algorithm retrieves the lowest cost element from the $\mathtt{open\_list}$ (line 3). We then expand the neighbouring vertices $u$ (line 7) and ensure that the path to the neighbour is not in the $\mathtt{open\_list}$, is not dominated by another path to $u$, and does not contain cycles (lines 8-10). We then add the path to $u$ with its WM cost to the $\mathtt{open\_list}$ (line 12-13). Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} is able to handle any monotonically increasing composition function $\beta$ (see equation [\[eq:path_costs\]](#eq:path_costs){reference-type="eqref" reference="eq:path_costs"}) as opposed to the sum of edge costs considered in MOSP. Opposed to MOSP, we are only interested in finding one solution for a given weight instead of the set of all Pareto-optimal paths. Thus, Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} terminates once the goal is reached (lines 4-5).\

::: algorithm
$\mathtt{open\_list} = \{(0, s, (s)) \}$\
$(cost, v, P)\leftarrow \mathtt{open\_list}.\mathtt{pop()}$ [// get by min cost]{style="color: gray"}\
:::

#### Theoretical properties

First, we characterize the runtime. In the worst case, Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} explores all paths from $s$ to any vertex $u$, leading to $2^{|V|}$ (the size of the power set for all sequences of vertices) executions of the while loop. For each subpath, we compute its cost only once in line 12, which requires evaluating $f_i(e)$ for all its edges and all $n$ objective functions. The number of edges is upper bound by $|V|^2$. Assuming that the evaluation of the costs $f_i(e)$ takes constant time, the total runtime is $O(2^{|V|}\cdot |V|^2 \cdot n$). While the runtime only grows linearly with the number of objective functions, it can scale exponentially with the number of vertices. However, due to the stopping criteria in line 4, the algorithm does not enumerate all $2^{|V|}$ solutions in practice. In our simulations we show that it is able to solve instances with $|V|=2000$.

Next we will establish correctness of the algorithm. We begin by considering the subpath elimination in line 9.

::: {#lem:subpath .lemma}
**Lemma 2** (Subpath elimination). Let $P'$ and $P^u$ be two subpaths from $s$ to $u$ such that $P'$ dominates $P^u$. If the composition function $\beta$ is monotone, then $P^u$ cannot be part of an optimal path from $s$ to the goal $g$.
:::

If $P'$ dominates $P^u$ then $f_i(P')\leq f_i(P^u)$ for all $i$. Now consider any possible path $Q$ from $u$ to the goal $g$. Since $f_i$ is *monotone* we then have $f_i(P'\cup Q)\leq f_i(P^u\cup Q)$. Finally, $c(P'\cup Q)\leq c(P^u\cup Q)$ follows directly from [\[eq:cheb_cost\]](#eq:cheb_cost){reference-type="eqref" reference="eq:cheb_cost"}. Hence, $P^u$ cannot lead to a path to the goal of lower cost than $P'$ and thus may be disregarded from the search. The result is similar to the analysis in [@ehrgott2005multicriteria], yet extends to the case of any monotone composition function $\beta$ instead of only sums. Based on Lemma [2](#lem:subpath){reference-type="ref" reference="lem:subpath"}, we can ensure that our algorithm finds the optimal solution.

::: {#prop:correct .proposition}
**Proposition 3** (Correctness). For any given weight $\boldsymbol{w}$, Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} returns the optimal solution $P^* = \arg\min_P\max_i f_i(P) \cdot w_i$.
:::

The proof follows three steps: (i) Lemma [2](#lem:subpath){reference-type="ref" reference="lem:subpath"} ensures that we never eliminate the optimal path during the search. (ii) Eventually, a tuple $(cost, v, P)$ where $v=g$ will be pulled from the open list and we thus find a path to the goal. (iii) the first time such a tuple is retrieved from the open list, it must have the minimal cost in the open list, and since it is the element of minimal cost in the open list and the cost is monotone, there cannot be another subpath in the open list that, when extended until $g$, achieves a smaller cost.

#### Cost-to-go heuristic

While Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} is optimal, its runtime scales exponentially with the size of the graph. The runtime can be improved with a cost-to-go heuristic as in an [A$^*$]{.smallcaps} or [D$^*$]{.smallcaps} algorithms [@koenig2004lifelong]. To use a heuristic, we augment the path $P^u$ with a virtual edge to the goal. This virtual edge allows for including an estimate for the cost-to-go. An [A$^*$]{.smallcaps} algorithm simply adds a heuristic value for the cost-to-go to the current cost. In contrast, our problem considers a maximization in the cost as well as a potentially non-linear composition function. Thus, we explicitly add an edge and then calculate the WM cost in line 12 for the augmented path. The objective values of the virtual edge must be chosen such that the WM cost of the augmented path is an underestimate of the optimal path to the goal. For instance, if one objective is length, we can set the length of virtual edge to the Euclidean distance while other objective values are zero.\

#### Runtime Budgeting {#sec:runtime_budget}

Finally, we can modify Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} to find potentially suboptimal solutions in polynomial runtime, similar to anytime algorothms such as ARA\* [@likhachev2003ara]. To that end, we introduce a budget $b$ for the number of predecessor paths leading to every vertex that we can store. We then only add a new tuple in line 13 when the number of tuples with a path ending at $u$ in the open list is below $b$. This prevents the $\mathtt{open\_list}$ to grow exponentially, yet might prevent the algorithm from finding an optimal solution.

In summary, we have shown how the WM cost can be incorporated in continuous- and discrete-space planning problems. For graph based planning we provided hardness results together with a complete algorithm.

# Numerical Results {#sec:results}

To illustrate the advantages of the WM method, we consider several motion planning problems with multiple objectives and compare the attainable solutions when using either WS and WM. Further, we investigate the runtime of Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"}.

## Comparison of WS and WM cost functions

For given objective functions, we compare how expressive WM ans WS approaches are. We approximate the sets of attainable solutions $\mathcal{T}^{\mathtt{sum}}$ and $\mathcal{T}^{\mathtt{max}}$ for the WS and WM cost functions as follows: We randomly sample a large set of weights $\boldsymbol{w}^1, \dots, \boldsymbol{w}^k$ and then compute the respective sets of optimal solutions $\mathcal{S}^{\mathtt{sum}}=\{T^{\mathtt{sum}}(\boldsymbol{w}^1), \dots, T^{\mathtt{sum}}(\boldsymbol{w}^k)\}$ solving [\[eq:lin_cost\]](#eq:lin_cost){reference-type="eqref" reference="eq:lin_cost"} and $\mathcal{S}^{\mathtt{max}}=\{T^{\mathtt{max}}(\boldsymbol{w}^1), \dots, T^{\mathtt{max}}(\boldsymbol{w}^k)\}$ solving [\[eq:cheb_cost\]](#eq:cheb_cost){reference-type="eqref" reference="eq:cheb_cost"}. Thus, $\mathcal{S}^{\mathtt{sum}}$ and $\mathcal{S}^{\mathtt{max}}$ are both subsets of the Pareto-front of the MOO described by the given objective functions, *i.e.,* consist of Pareto-optimal solutions.

We use three quantitative measures to compare $\mathcal{S}^{\mathtt{sum}}$ and $\mathcal{S}^{\mathtt{max}}$: dispersion, coverage and number of unique solutions on the Pareto-fronts. The dispersion captures *gaps* in the approximation of the Pareto-front, and is defined as follows:

::: definition
**Definition 3** (Dispersion). Given solutions $\mathcal{S}=\{T^1, \dots, T^k\}$, the dispersion of $\mathcal{S}$ is the maximum distance between a point $\boldsymbol{p}$ on the Pareto-front and the closest $\boldsymbol{f}(T^i)$ for $i=1,\dots, k$.
:::

In principle, this distance should be defined as a measure along the Pareto-front, yet for practical purposes we use the Euclidean distance. Note that for a useful interpretation of dispersion measure, we require objectives to be normalized. Coverage captures the volume of the set of points that is dominated by the solutions $\mathcal{S}$ [@zitzler1999multiobjective]. In a minimization problem with normalized features we sample over the set $[0,1]^n$ to estimate coverage. Lastly, sampling $k$ different weights does often not lead to $k$ different solutions. Thus, given a set $\mathcal{S}=\{T^1, \dots, T^k\}$, we compute the number of trajectories $T^i$ where the Euclidean distance between $\boldsymbol{f}(T^i)$ and $\boldsymbol{f}(T^j)$ is above some threshold $\delta$ for all $i, j=1,\dots,k$. We refer to this measure as the number of unique solutions. All experiments run with $k=200$ samples and distance threshold $\delta=0.01$.\

#### Simple Obstacles

First, we revisit the example from Figure [4](#fig:intro){reference-type="ref" reference="fig:intro"} and provide numerical results in Table [1](#tab:exp1){reference-type="ref" reference="tab:exp1"} (labelled *Obstacles*). We observe that WM outperforms WS on all three metrics, and with a large margin on dispersion on and number of solutions. This highlights the significant shortcomings of the WS even in very simple planning problems.\

#### Continuous space motion planning

The second experiments considers a continuous space motion planner. We use the driver experiment that is popular in numerous studies on reward learning in HRI, for instance [@sadigh2017active; @biyik2019asking; @wilde2020active]. An autonomous car navigates on a three lane road in the presence of a human-driven vehicle. The problem considers four objectives: heading, position in the lane, speed and distance to the other car. We solve the problem numerically using a numerical solver for constrained non-convex optimization. The min-max objective is implemented as in equation [\[eq:continuous_reformulated\]](#eq:continuous_reformulated){reference-type="eqref" reference="eq:continuous_reformulated"}.

Qualitative results are shown in Figure [7](#fig:eval_driver){reference-type="ref" reference="fig:eval_driver"}. Since the numerical solver may return suboptimal solutions, we filtered all trajectories that were dominated by another trajectory. Overall, the WM yields a larger variety of solutions. In particular, the solutions for the WS method are only variations of few types of trajectories, while WM offers more nuanced solutions. On the evaluation measures, the WM clearly outperforms the WS with respect to dispersion and the number of unique solutions, yet by a smaller margin than in the *Obstacles* experiment. For coverage WM has only a small benefit.\

:::: {#fig:eval_driver .figure latex-placement="t"}
![Weighted sum (WS).](Wilde2023Scalarizing_figs/Driver_WS.png){#fig:eval_drver_lin width="100%"}

\

![Weighted maximum (WM).](Wilde2023Scalarizing_figs/Driver_WM.png){#fig:eval_driver_cheb width="100%"}

::: caption
Results for the driver experiments. White shows the human driven car, red trajectories show solutions for the autonomous car.
:::
::::

#### Graph-based motion planning

In the third setup we consider a probabilistic roadmap (PRM) with $1000$ vertices, shown in Figure [10](#fig:eval_graph){reference-type="ref" reference="fig:eval_graph"}. Similar to the first experiment, the objectives are path length and closeness to obstacles. We consider two problem variations for closeness: the summed closeness, labelled as Graph-1 in Table [1](#tab:exp1){reference-type="ref" reference="tab:exp1"} with an example shown in Figure [10](#fig:eval_graph){reference-type="ref" reference="fig:eval_graph"}, and minimum closeness, labelled as Graph-2.

In Figure [10](#fig:eval_graph){reference-type="ref" reference="fig:eval_graph"} we observe that the WM finds a larger variety of paths, some falling into a homotopy class for which the WS method does not find any path. In the Pareto-fronts WS exhibits several large gaps, while the WM covers the Pareto-front more densely. The gaps of the WS correspond to non-convex parts of the Pareto-front, implying that these parts cannot be covered by the WS for any choice of weights. The measures in Table [1](#tab:exp1){reference-type="ref" reference="tab:exp1"} show again a substantially smaller dispersion, slightly higher coverage and higher number of solutions for WM compared to WS in both graph problems.

:::: {#fig:eval_graph .figure latex-placement="t"}
![Weighted sum (WS).](Wilde2023Scalarizing_figs/graph_linear.png){#fig:eval_graph_lin width=".9\\textwidth"}

![Weighted maximum (WM).](Wilde2023Scalarizing_figs/graph_max.png){#fig:eval_graph_cheb width=".9\\textwidth"}

::: caption
Optimal paths for a graph based motion planning problem with two objectives: Path length, and the summed distance to an obstacle. Upper: colored trajectories are solutions found by the weighted sum (a) and weighted maximum (b), respectively. Lower: Objective values of the trajectories of the upper plot.
:::
::::

::: {#tab:exp1}
  Problem                 Cost  $\downarrow$ Dispersion   $\uparrow$ Coverage   $\uparrow$ $\#$ Solutions
  ----------- ---------------- ------------------------- --------------------- ---------------------------
  Obstacles     $\mathtt{SUM}$           0.49                    0.49                       9
                $\mathtt{MAX}$           0.15                    0.65                      17
  Driver        $\mathtt{SUM}$           0.52                    0.95                      22
                $\mathtt{MAX}$           0.28                    0.97                      29
  Graph-1       $\mathtt{SUM}$           0.26                    0.71                      11
                $\mathtt{MAX}$           0.19                    0.75                      40
  Graph-2       $\mathtt{SUM}$           0.42                    0.73                       6
                $\mathtt{MAX}$           0.20                    0.80                      10

  : Numerical results for different planning problems.
:::

In summary, in all three planning problems the proposed method is able to find better sets of Pareto-optimal trade-offs compared to the weighted sum method.

## Performance of WM planning on graphs {#sec:experiment_runtime}

In a second experiment, we investigate the performance of Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} when using the computation budget and the cost-to-go heuristic. As a heuristic, we add a virtual edge where the length equals the Euclidean distance to the goal and the closeness is zero. We use a PRM with $2000$ vertices, similar to the one in Figure [10](#fig:eval_graph){reference-type="ref" reference="fig:eval_graph"}. In $1000$ trials, we randomise start and goal locations, as well as the weights in the cost function. Figure [11](#fig:eval_alg_performance){reference-type="ref" reference="fig:eval_alg_performance"} shows the cost ratio compared to optimal and the computation time for various computation budgets $b$. For the standard implementation without heuristic, we observe that for $b=50$, all returned solutions are almost optimal (ratio $<1.001$). This comes with an increase in computation time by a factor of $250$ on average, but still remains below $3$ seconds (Hardware specification: Intel i7-11800H \@2.3GHz, 32Gb RAM.). Using the cost-to-go heuristic keeps average the runtime increase below a factor of $35$ (or $<.5$ seconds). Moreover, the heuristic also allows for finding close-to-optimal solutions with a very small budget of $b=5$, where the runtime increase is negligible. Only for $b=1$ the heuristic can misguide the search and yield suboptimal solutions. Yet, this does not invalidate the admissibility of the chosen heuristic: For small $b$ the algorithm has no guarantee for finding an optimal solution, independent of the heuristic. In conclusion, the cost-to-go heuristic and computation budget allow for finding paths with minimal WM cost within a practical runtime.

:::: {#fig:eval_alg_performance .figure latex-placement="t"}
![](Wilde2023Scalarizing_figs/performance_MMCP.png){width=".45\\textwidth"}

::: caption
Performance of heuristic variants of Algorithm [\[alg:graph search\]](#alg:graph search){reference-type="ref" reference="alg:graph search"} with different computation budgets $b$. Shown are the cost ratio over an optimal solution and the computation time ratio over Dijkstra's algorithm.
:::
::::

# Discussion

We studied WM cost functions as an alternative to commonly used WS costs in motion planning problems with multiple objectives. We showed that while the WS method is widely used, it might only represent a small subset of all optimal trade-offs when at least one of the objectives is non-convex. We proposed a WM approach as an alternative cost function, which is Pareto-complete. Further, we showed how the WM cost can be used in continuous-space planning, characterized the hardness for graph-based planning and presented a novel path planning algorithm. Our simulations showed that the proposed WM cost is substantially more expressive than the WS across different motion planning problems, and that our proposed path planning algorithm can efficiently find close-to-optimal solutions. While the WM formulation makes path planning on graphs NP-hard, our simulation results show that it allows for finding substantially richer sets of solutions, recovering all parts of the Pareto-front. Further, using runtime budgeting and the cost-to-go heuristic allows for computing close-to-optimal solutions within a practical computation time.

Future work should consider how WM costs can used for learning user preferences in human-in-the-loop learning problems. Given its advantageous expressiveness the WM allows for designing user models that represent a wider variety of user preferences with the same number of parameters. Another research direction is investigating how robot complex multi-robot routing problems can be solved for a WM cost. Further, for discrete space planning we assumed a monotonic composition function. Future work could include non-monotonic cost functions to broaden the range of applications. Lastly, finding suitable parameters for the WM cost remains a challenge. Thus, we plan to adapt our earlier work [@botros2022error] to find sets of representative weights for the WM cost.

::: thebibliography
10 url@samestyle

J. Levinson, J. Askeland, J. Becker, J. Dolson, D. Held, S. Kammel, J. Z. Kolter, D. Langer, O. Pink, V. Pratt *et al.*, "Towards fully autonomous driving: Systems and algorithms," in *2011 IEEE intelligent vehicles symposium (IV)*.IEEE, 2011, pp. 163--168.

F. Christianos, P. Karkus, B. Ivanovic, S. V. Albrecht, and M. Pavone, "Planning with occluded traffic agents using bi-level variational occlusion models," in *2023 IEEE International Conference on Robotics and Automation (ICRA)*.IEEE, 2023, pp. 5558--5565.

A. Botros and S. L. Smith, "Tunable trajectory planner using g 3 curves," *IEEE Transactions on Intelligent Vehicles*, vol. 7, no. 2, pp. 273--285, 2022.

N. Wilde, A. Blidaru, S. L. Smith, and D. Kulić, "Improving user specifications for robot behavior through active preference learning: Framework and evaluation," *International Journal of Robotics Research (IJRR)*, vol. 39, no. 6, pp. 651--667, 2020.

A. Biswas, A. Wang, G. Silvera, A. Steinfeld, and H. Admoni, "Socnavbench: A grounded simulation testing framework for evaluating social navigation," *ACM Transactions on Human-Robot Interaction (THRI)*, vol. 11, no. 3, pp. 1--24, 2022.

M. Zucker, N. Ratliff, A. D. Dragan, M. Pivtoraiko, M. Klingensmith, C. M. Dellin, J. A. Bagnell, and S. S. Srinivasa, "Chomp: Covariant hamiltonian optimization for motion planning," *The International Journal of Robotics Research*, vol. 32, no. 9-10, pp. 1164--1193, 2013.

Z. Lu, Z. Liu, G. J. Correa, and K. Karydis, "Motion planning for collision-resilient mobile robots in obstacle-cluttered unknown environments with risk reward trade-offs," in *2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*.IEEE, 2020, pp. 7064--7070.

P. Abbeel and A. Y. Ng, "Apprenticeship learning via inverse reinforcement learning," in *Proceedings of the twenty-first international conference on Machine learning*.ACM, 2004, p. 1.

D. Hadfield-Menell, S. J. Russell, P. Abbeel, and A. Dragan, "Cooperative inverse reinforcement learning," *Advances in neural information processing systems*, vol. 29, 2016.

D. Sadigh, A. D. Dragan, S. S. Sastry, and S. A. Seshia, "Active preference-based learning of reward functions," in *Proceedings of Robotics: Science and Systems (RSS)*, Jul. 2017.

E. Biyik, M. Palan, N. C. Landolfi, D. P. Losey, and D. Sadigh, "Asking easy questions: A user-friendly approach to active reward learning," in *Proceedings of the 3rd Conference on Robot Learning (CoRL)*, 2019.

S. Habibian, A. Jonnavittula, and D. P. Losey, "Here's what i've learned: Asking questions that reveal reward learning," *ACM Transactions on Human-Robot Interaction (THRI)*, vol. 11, no. 4, pp. 1--28, 2022.

J. Branke, K. Deb, K. Miettinen, and R. Slowiński, *Multiobjective optimization: Interactive and evolutionary approaches*.Springer Science & Business Media, 2008, vol. 5252.

T. Gu, J. Atwood, C. Dong, J. M. Dolan, and J.-W. Lee, "Tunable and stable real-time trajectory planning for urban autonomous driving," in *2015 IEEE/RSJ IROS*.IEEE, 2015, pp. 250--256.

P. Karkus, B. Ivanovic, S. Mannor, and M. Pavone, "Diffstack: A differentiable and modular control stack for autonomous vehicles," in *Conference on Robot Learning*.PMLR, 2023, pp. 2170--2180.

Z. Zuo, X. Yang, Z. Li, Y. Wang, Q. Han, L. Wang, and X. Luo, "Mpc-based cooperative control strategy of path planning and trajectory tracking for intelligent vehicles," *IEEE Transactions on Intelligent Vehicles*, vol. 6, no. 3, pp. 513--522, 2020.

P. Hang, C. Lv, C. Huang, J. Cai, Z. Hu, and Y. Xing, "An integrated framework of decision making and motion planning for autonomous vehicles considering social behaviors," *IEEE transactions on vehicular technology*, vol. 69, no. 12, pp. 14 458--14 469, 2020.

P. De Petris, M. Dharmadhikari, H. Nguyen, and K. Alexis, "Risk-aware motion planning for collision-tolerant aerial robots subject to localization uncertainty," in *2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*.IEEE, 2022, pp. 4561--4568.

Y. Che, A. M. Okamura, and D. Sadigh, "Efficient and trustworthy social navigation via explicit and implicit robot--human communication," *IEEE Transactions on Robotics*, vol. 36, no. 3, pp. 692--707, 2020.

B. Brito, B. Floor, L. Ferranti, and J. Alonso-Mora, "Model predictive contouring control for collision avoidance in unstructured dynamic environments," *IEEE Robotics and Automation Letters*, vol. 4, no. 4, pp. 4459--4466, 2019.

T. Marcucci, M. Petersen, D. von Wrangel, and R. Tedrake, "Motion planning around obstacles with convex optimization," *arXiv preprint arXiv:2205.04422*, 2022.

C. E. Luis, M. Vukosavljev, and A. P. Schoellig, "Online trajectory generation with distributed model predictive control for multi-robot motion planning," *IEEE Robotics and Automation Letters*, vol. 5, no. 2, pp. 604--611, 2020.

M. Cáp and J. Alonso-Mora, "Multi-objective analysis of ridesharing in automated mobility-on-demand," in *Robotics: Science and Systems (RSS)*, 2018.

N. Wilde, A. Sadeghi, and S. L. Smith, "Learning submodular objectives for team environmental monitoring," *IEEE Robotics and Automation Letters*, vol. 7, no. 2, pp. 960--967, 2021.

N. Wilde, D. Kulić, and S. L. Smith, "Active preference learning using maximum regret," in *2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2020, pp. 10 952--10 959.

N. Wilde, E. Biyik, D. Sadigh, and S. L. Smith, "Learning reward functions from scale feedback," in *Conference on Robot Learning*.PMLR, 2022, pp. 353--362.

I. Y. Kim and O. L. De Weck, "Adaptive weighted-sum method for bi-objective optimization: Pareto front generation," *Structural and multidisciplinary optimization*, vol. 29, pp. 149--158, 2005.

I. Y. Kim and O. De Weck, "Adaptive weighted sum method for multiobjective optimization: a new method for pareto front generation," *Structural and multidisciplinary optimization*, vol. 31, no. 2, pp. 105--116, 2006.

A. Thoma, K. Thomessen, A. Gardi, A. Fisher, and C. Braun, "Prioritizing paths: An improved cost function for local path planning for uav in medical applications," in *AIAC 2023: 20th Australian International Aerospace Congress: 20th Australian International Aerospace Congress*.Engineers Australia Melbourne, 2023, pp. 324--329.

D. Yi, M. A. Goodrich, and K. D. Seppi, "Morrf\*: Sampling-based multi-objective motion planning," in *Twenty-Fourth International Joint Conference on Artificial Intelligence*, 2015.

B. Sakcak and S. M. LaValle, "Complete path planning that simultaneously optimizes length and clearance," in *2021 IEEE International Conference on Robotics and Automation (ICRA)*. IEEE, 2021, pp. 10 100--10 106.

K. Van Moffaert, M. M. Drugan, and A. Nowé, "Scalarized multi-objective reinforcement learning: Novel design techniques," in *2013 IEEE Symposium on Adaptive Dynamic Programming and Reinforcement Learning (ADPRL)*.IEEE, 2013, pp. 191--199.

X. Chen, A. Ghadirzadeh, M. Björkman, and P. Jensfelt, "Meta-learning for multi-objective reinforcement learning," in *2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*.IEEE, 2019, pp. 977--983.

X. D. Ding, B. Englot, A. Pinto, A. Speranzon, and A. Surana, "Hierarchical multi-objective planning: From mission specifications to contingency management," in *2014 IEEE international conference on robotics and automation (ICRA)*.IEEE, 2014, pp. 3735--3742.

S. D. Bopardikar, B. Englot, and A. Speranzon, "Multiobjective path planning: Localization constraints and collision probability," *IEEE Transactions on Robotics*, vol. 31, no. 3, pp. 562--577, 2015.

B. H. Korte, J. Vygen, B. Korte, and J. Vygen, *Combinatorial optimization*.Springer, 2011, vol. 1.

Y. Censor, "Pareto optimality in multiobjective problems," *Applied Mathematics and Optimization*, vol. 4, no. 1, pp. 41--59, 1977.

S. Boyd and L. Vandenberghe, *Convex optimization*.Cambridge university press, 2004.

D. Bertsimas and J. N. Tsitsiklis, *Introduction to linear optimization*.Athena scientific Belmont, MA, 1997, vol. 6.

M. Ehrgott, *Multicriteria optimization*.Springer Science & Business Media, 2005, vol. 491.

X. Gandibleux, F. Beugnies, and S. Randriamasy, "Martins' algorithm revisited for multi-objective shortest path problems with a maxmin cost function," *4OR*, vol. 4, no. 1, pp. 47--59, 2006.

S. Koenig, M. Likhachev, and D. Furcy, "Lifelong planning a\*," *Artificial Intelligence*, vol. 155, no. 1-2, pp. 93--146, 2004.

M. Likhachev, G. J. Gordon, and S. Thrun, "Ara\*: Anytime a\* with provable bounds on sub-optimality," *Advances in neural information processing systems*, vol. 16, 2003.

E. Zitzler and L. Thiele, "Multiobjective evolutionary algorithms: a comparative case study and the strength pareto approach," *IEEE transactions on Evolutionary Computation*, vol. 3, no. 4, pp. 257--271, 1999.

A. Botros, A. Sadeghi, N. Wilde, J. Alonso-Mora, and S. L. Smith, "Error-bounded approximation of pareto fronts in robot planning problems," in *15th International Workshop on Algorithmic Foundations of Robotics (WAFR)*, 2022.
:::

[^1]: This research is supported by the European Union's Horizon 2020 research and innovation program under Grant 101017008.

[^2]: N. Wilde and J. Alonso-Mora are with the Department for Cognitive Robotics, 3ME, Delft University of Technology, Delft, Netherlands, `{n.wilde, j.alonsomora}@tudelft.nl`. S. L. Smith is with the Department for Electrical and Computer Engineering, University of Waterloo, Waterloo, Canada, `stephen.smith@uwaterloo.ca`

[^3]: A convex function $f(x)$ is proper convex over its domain $\mathcal{X}$ if it never attains $-\infty$, and if there exists at least some $x_0$ where $f(x_0)<\infty$.
