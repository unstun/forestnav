---
citation_key: Morozov2024MultiQuery
arxiv_id: 2409.19543
arxiv_url: https://arxiv.org/abs/2409.19543
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:16:53Z
origin: ai+web
reviewed: false
---

# Introduction

A Graph of Convex Sets (GCS) [@marcucci2024graphs] is a graph where each vertex is paired with a convex set and an optimization variable inside this set, while each edge couples adjacent vertex variables through additional convex costs and constraints. In the Shortest-Path Problem (SPP) in GCS [@marcucci2024shortest], we simultaneously seek a discrete path through this graph and optimize the continuous variables associated with the vertices along the path, while minimizing the cumulative edge costs.

Though the SPP in GCS is NP-hard [@marcucci2024shortest Section 9.2], effective solution methods have been proposed in [@marcucci2024shortest; @chia2024gcs]. This technique has shown remarkable success in various robotics applications, such as optimal control [@marcucci2024shortest], planning through contact [@graesdal2024towards], and other robotics problems [@philip2024mixed; @kurtz2023temporal; @cohn2023non]. In real-world hardware deployment, it has been especially effective in collision-free motion planning [@marcucci2023motion], addressing the challenges of non-convex obstacle avoidance constraints.

:::: {#f-robot-arm-title .figure latex-placement="!t"}
![](Morozov2024MultiQuery_figs/robot_arm_visualization.jpeg){width="\\textwidth"}

::: caption
Robotic arm in a simulated environment, tasked with moving items between shelves and bins. Shown are four queries for collision-free motion planning.
:::
::::

However, solving the SPP in GCS can sometimes be too slow for real-time applications on high-dimensional robotic systems. Consider a 7-DoF KUKA iiwa robot arm repeatedly performing online motion planning in a static environment. When the environment is simple, the GCS is small, and the shortest path queries can be solved quickly, in under 50ms [@marcucci2023motion]. However, when the environment is complex and the configuration space must be covered thoroughly, as in [1](#f-robot-arm-title){reference-type="ref+label" reference="f-robot-arm-title"}, the GCS becomes large, and the shortest path queries can take up to of 600ms. This is not practical for high-productivity applications, such as robot arms in warehouses, where the company's income is nearly proportional to the operational speed.

In an effort to reduce solve times for online shortest path queries in GCS, we seek an efficient way of precomputing optimal paths between given sets of source and target conditions in the GCS. We formulate this problem as a generalization of the SPP in GCS that is akin to the all-pairs generalization of the classical SPP. Our solution contains two phases, illustrated in [4](#f-gcs-example){reference-type="ref+label" reference="f-gcs-example"}. Offline, we solve a semidefinite program that produces convex quadratic lower bounds to the cost-to-go function over the convex sets associated with GCS vertices. Pictured in [2](#sf-g1){reference-type="ref+label" reference="sf-g1"} are the contour plots of these lower bounds at every vertex. Then, online, we use a greedy multi-step lookahead policy with the cost-to-go lower bounds to determine the next vertex to visit. Thus, as shown in [3](#sf-g2){reference-type="ref+label" reference="sf-g2"}, the path is obtained incrementally, one vertex at a time. Though the quadratic cost-to-go lower bounds can be coarse, using the lookahead policy is equivalent to producing piecewise-quadratic lower bounds, which can be very expressive. As a result, the obtained paths are nearly optimal in practice. Convexity of the quadratic cost-to-go lower bounds allows us to evaluate the greedy policy by solving a set of small convex programs in parallel, which can be done quickly at runtime. Applied to the complex scenario shown in [1](#f-robot-arm-title){reference-type="ref+label" reference="f-robot-arm-title"}, our method requires just 6s of offline computation to produce the cost-to-go lower bounds. Subsequent online queries take 2-11ms, which is up to two orders of magnitude faster than solving the SPP in GCS from scratch. []{#s-introduction label="s-introduction"}

:::: {#f-gcs-example .figure latex-placement="t!"}
![ Offline: synthesize cost-to-go over the GCS. Contour plots are shown. ](Morozov2024MultiQuery_figs/graph_cost-to-go.png){#sf-g1 width="\\textwidth"}

:::: {#sf-g2 .figure}
![](Morozov2024MultiQuery_figs/simple_graph_expand_1.png){width="\\textwidth"}

![](Morozov2024MultiQuery_figs/simple_graph_expand_3.png){width="\\textwidth"}

![](Morozov2024MultiQuery_figs/simple_graph_expand_5.png){width="\\textwidth"}

::: caption
Online: at each iteration, we evaluate all $n$-step paths from the current vertex ($n\!=\!1$ shown) and greedily select the decision that minimizes the $n$-step lookahead cost-to-go. The first three iterations are shown, as the path is built incrementally.
:::
::::

::: caption
Illustration of our approach. The GCS instance is embedded in $\mathbb R^2$, with the source vertex at the top and the target vertex at the bottom. The edges are shown as red arrows, and the edge length is the squared Euclidean distance.
:::
::::

## Literature review {#ss-related-work}

Graph search plays a central role in both modelling and solving a wide variety of planning problems in robotics. In this section we briefly connect our work to some notable examples in this literature.

A common approach to motion planning is to construct a graph where nodes correspond to collision-free configurations and edges correspond to collision-free motions. The most popular approaches based on this idea are the Rapidly exploring Random Trees (RRT) [@lavalle1998rapidly], Probabilistic Roadmap (PRM) [@kavraki1996probabilistic], and their many variants [@kuffner2000rrt; @bohlin2000path; @jaillet2004prm; @karaman2011sampling]. The GCS approach to motion planning is similar to the PRM one, but collision-free configurations are replaced with large collision-free sets [@marcucci2023motion]. GCS avoids two major drawbacks of planning with a PRM: the need to densely sample in high-dimensional spaces and post-process the motion plan to obtain a smooth trajectory. However, generating these collision-free sets can be computationally challenging and expensive. Furthermore, SPP in GCS queries can still be very expensive, motivating this current work.

The importance of the SPP has led to a breadth of literature on its solution, with Bellman's dynamic programming approach illustrating the central role of the cost-to-go function [@bellman1966dynamic; @bertsekas2012dynamic]. Given the cost-to-go, a shortest path can be extracted using a simple greedy strategy: given a vertex $v$, the next vertex in the path is the one which minimizes the cost-to-go among all the neighbors of $v$. This is captured by the famous Bellman's equation[@bellman1966dynamic].

Multi-query SPP setting has also been thoroughly investigated. The All-Pairs Shortest Paths (APSP) is the problem of finding shortest paths between every pair of vertices in a discrete graph [@cormen2022introduction Ch. 23]. One method for solving this problem, from which we draw particular inspiration, first computes the cost-to-go function between every pair of vertices in the graph (also known as a *distance oracle*). This cost-to-go is used to produce a successor along the shortest path between every pair of vertices, which is stored into the *successor matrix*. The optimal paths are retrieved by sequentially querying this matrix.

Explicit solutions to the Bellman equation exist only in a handful of contexts. In the case of purely discrete graphs, a number of efficient methods exist [@floyd1962algorithm; @warshall1962theorem; @johnson1977efficient], where the cost-to-go function can be encoded using a simple matrix. Another notable example from control is Explicit Model Predictive Control (MPC) where the cost-to-go is a piecewise quadratic [@bemporad2002explicit]. However, even in these settings, storing the cost-to-go can be prohibitively expensive for large graphs, particularly in the APSP setting. In the purely discrete setting, the description of the APSP cost-to-go function grows quadratically in the size of the graph, while in the MPC setting it grows exponentially.

In most cases, solving the Bellman equation is known to be intractable. This has motivated a breadth of literature for computing approximations for the cost-to-go in various setting [@de2003linear; @powell2007approximate; @lasserre2008nonlinear; @bertsekas2012dynamic; @lewis2013reinforcement; @wang2015approximate]. Similarly, in this paper we seek a computationally tractable way to approximate the cost-to-go function to solve the APSP in GCS. The generalization in the particular context of GCS is not straightforward and constitutes one of the contributions of this work.

# All-Pairs Shortest Paths in a Graph of Convex Sets {#s-apsp-in-gcs}

We seek to efficiently precompute optimal solutions to the SPP in GCS between given sets of source and target conditions. [2.1](#ss-apsp-in-graph){reference-type="ref+label" reference="ss-apsp-in-graph"} presents the classical APSP, which is the corresponding problem in an ordinary graph. In [2.2](#ss-spp-in-gcs){reference-type="ref+label" reference="ss-spp-in-gcs"}, we describe the single-query SPP in GCS. We then formulate the APSP in GCS in [2.3](#ss-apsp-in-gcs){reference-type="ref+label" reference="ss-apsp-in-gcs"}, and outline our approximate solution method in [2.4](#ss-solution-overview){reference-type="ref+label" reference="ss-solution-overview"}.

## All-Pairs Shortest Paths {#ss-apsp-in-graph}

#### Graphs and paths.

Let $G=(\mathcal V, \mathcal E)$ be a directed graph with vertex set $\mathcal V$ and edge set $\mathcal E$. Given a source vertex $s$ and target vertex $t$, an $s\textsf{-}t$ path is a sequence of distinct vertices $p = (s\!=\!v_0, v_1, \ldots, v_K\!=\!t)$, where each consecutive pair of vertices is connected by an edge in $\mathcal E$ and no vertex is revisited. We define $\mathcal E_p = \{(v_0, v_1), \ldots, (v_{K-1}, v_K)\}$ as the set of edges traversed by the path $p$, and denote the set of all $s\textsf{-}t$ paths in $G$ as $\mathcal P_{s,t}$.

#### Shortest Path Problem (SPP).

Let us associate with every edge $e\in\mathcal E$ a non-negative edge cost $c_e\in\mathbb R_+$. A shortest path $p$ between the vertices $s$ and $t$ minimizes the sum of the edge costs along the path: $$\underset{p}{\min} \quad \sum_{e \in \mathcal E_p} c_e \quad  \text{s.t.} \quad p \in \mathcal P_{s,t}.$$ The optimal value of this program is called the *cost-to-go* between $s$ and $t$, and is denoted by $J^*_{s,t}$. *The principle of optimality* [@bellman1966dynamic] holds in this context, stating that every subpath of a shortest path is itself a shortest path. This forms the foundation for many efficient solution algorithms to this problem.

#### All-Pairs Shortest Paths (APSP).

The APSP is the multi-query generalization of the SPP, where we seek a shortest path between all pairs of vertices in a graph. Efficient solutions to the APSP leverage the principle of optimality. Instead of computing the full path for each pair of vertices, it suffices to compute only the immediate successor along this path. The full path can thus be attained incrementally, one vertex at the time.

This solution to the APSP can be implicitly encoded via the cost-to-go function $J^*_{v,t}$ for every pair of vertices $v$ and $t$, computed via dynamic programming [@cormen2022introduction Ch. 23] [@floyd1962algorithm; @warshall1962theorem; @johnson1977efficient]. The successor is then computed by greedily picking a vertex that minimizes the one-step lookahead with respect to the cost-to-go: $$\label{e-successor-policy}
\begin{align}
\pi(v, t) \quad = \quad \underset{w}{\arg\min} \quad &  c_e + J^*_{w,t} \label{e-succp-a} \\
\text{s.t.} \quad & e = (v, w)\in\mathcal E. \label{e-succp-b}
\end{align}$$ The solution $\pi$ is a decision policy that, given the current and target vertices $v$ and $t$, selects the next vertex on the shortest $v\textsf{-}t$ path. We refer to $\pi$ as the *successor policy*.

## Shortest-Path Problem in a Graph of Convex Sets {#ss-spp-in-gcs}

#### Graph of Convex Sets.

A GCS is a directed graph $G = (\mathcal V, \mathcal E)$, where each vertex $v\in\mathcal V$ is paired with a bounded convex set $\mathcal X_v$ and a continuous variable $x_v\in\mathcal X_v$. Each edge $e = (v,w)\in\mathcal E$ is then paired with a convex set $\mathcal X_e \subseteq \mathcal{X}_v \times \mathcal{X}_w$ and a convex non-negative edge length function $l_e: \mathcal{X}_e \rightarrow \mathbb{R}_+$, such that the adjacent vertex variables satisfy the constraint $(x_v,x_w)\in\mathcal X_e$, while minimizing the length $l_e(x_v,x_w)$ [@marcucci2024graphs].

#### The Shortest Path Problem in a Graph of Convex Sets.

The SPP in GCS between point $\bar x_s\in\mathcal X_s$ of vertex $s$ and $\bar x_t\in\mathcal X_t$ of vertex $t$ is defined as follows: $$\label{e-gcs-spp}
\begin{align}
\qquad\qquad \underset{p, \;\{x_v\}_{v \in p}}{\min} \quad & \sum_{e = (v,w)\in \mathcal E_p} l_{e}(x_v,\, x_w) &&\label{e-spp-a} \\
\text{s.t.} \quad & p \in\mathcal P_{s,t}, &&\label{e-spp-b}\\
& x_s = \bar x_s, \quad x_t = \bar x_t, &&\label{e-spp-c} \\
& x_{v}\in\mathcal X_{v}, &&\forall v\in p, \label{e-spp-d} \\
& (x_v,x_w) \in \mathcal X_{e}, &&\forall e=(v,w)\in \mathcal E_p. \label{e-spp-e}
\end{align}$$ Similar to the classical SPP, the SPP in GCS searches for an $s\textsf{-}t$ path $p=(v_0, v_1, \ldots, v_K)$ though a graph, which is a sequence of distinct vertices. In addition to that, it also searches for a sequence of corresponding vertex variables ${(\bar x_s\!=\!x_{v_0}, x_{v_1}, \ldots, x_{v_K}\!=\!\bar x_t)}$, referred to as a *trajectory*. This trajectory satisfies the vertex and edge constraints ([\[e-spp-c\]](#e-spp-c){reference-type="ref+label" reference="e-spp-c"}), ([\[e-spp-d\]](#e-spp-d){reference-type="ref+label" reference="e-spp-d"}), ([\[e-spp-e\]](#e-spp-e){reference-type="ref+label" reference="e-spp-e"}), while minimizing the edge costs ([\[e-spp-a\]](#e-spp-a){reference-type="ref+label" reference="e-spp-a"}). The optimal solution to ([\[e-gcs-spp\]](#e-gcs-spp){reference-type="ref+label" reference="e-gcs-spp"}) is thus a tuple (path and trajectory). We denote the optimal value of ([\[e-gcs-spp\]](#e-gcs-spp){reference-type="ref+label" reference="e-gcs-spp"}) as $J^*_{s,t}(\bar x_s,\bar x_t)$ and refer to it as the *cost-to-go* from point $\bar x_s$ of vertex $s$ to point $\bar x_t$ of vertex $t$.

Unlike the classical SPP, the SPP in GCS is NP-hard [@marcucci2024graphs Section 9.2], and thus unlikely to have a polynomial-time solution. However, it can be reformulated as a Mixed-Integer Convex Program (MICP) with a strong convex relaxation [@marcucci2024shortest]: using a rounding strategy from [@marcucci2023motion], this relaxation often yields near-optimal solutions in practice.

For the classical SPP, the principle of optimality holds and the optimal policy is independent of past decisions, which simplifies the problem and enables many efficient solution algorithms. As demonstrated in the following example, these properties break down in the SPP in GCS.

::: example
[]{#ex-optimal-policy label="ex-optimal-policy"} Consider the GCS in [7](#f-illustrative){reference-type="ref+label" reference="f-illustrative"}, which is embedded in $\mathbb R^2$. This GCS has four vertices $\mathcal V = \{s,v,w,t\}$, where the convex sets $\mathcal X_s,\mathcal X_v,\mathcal X_t$ are points, and the convex set $\mathcal X_w$ is a segment. Every vertex is connected to every other vertex with an edge, and the edge lengths $l_e$ are the squared Euclidean distance (e.g., $l_{(v,w)} = ||x_v-x_w||_2^2$).

Due to the constraint that vertices cannot be revisited, the optimal policy is a function of the set of previously visited vertices. This is demonstrated in [5](#sf-illustrative-1){reference-type="ref+label" reference="sf-illustrative-1"}, where we plot the optimal $s\textsf{-}t$ path in orange and the optimal $v\textsf{-}t$ path in blue. The optimal decision at vertex $v$ depends on previously visited vertices: if $w$ was visited before, the optimal decision is to go to $t$ (orange), otherwise the optimal decision is to go to $w$ (blue).

:::: {#f-illustrative .figure latex-placement="t!"}
![ The optimal policy at vertex $v$ depends on previous decisions. If $w$ has been visited already, the optimal decision is to go to $t$ (orange), otherwise it is to go to $w$ (blue). ](Morozov2024MultiQuery_figs/fig2_1.png){#sf-illustrative-1 width="\\textwidth"}

![ If we allow vertex revisits, the optimal policy is independent of past decisions. Shown are the optimal $s\textsf{-}t$ (green) and $v\textsf{-}t$ (blue) solutions to the relaxed problem. ](Morozov2024MultiQuery_figs/fig2_2.png){#sf-illustrative-2 width="\\textwidth"}

::: caption
The two-dimensional GCS from [\[ex-optimal-policy\]](#ex-optimal-policy){reference-type="ref+label" reference="ex-optimal-policy"}. The convex sets paired with $s,v,t$ are points and the one paired with $w$ is a segment. The GCS is fully connected, and the edge lengths are the squared Euclidean distance.
:::
::::

Observe also that the principle of optimality does not hold for this problem: the $v\textsf{-}t$ subpath of the optimal $s\textsf{-}t$ path (orange) is not the optimal $v\textsf{-}t$ path (blue). We cannot substitute the optimal $v\textsf{-}t$ path (blue) in place of the original $v\textsf{-}t$ subpath, since the resulting vertex sequence $(s,w,v,w,t)$ ([6](#sf-illustrative-2){reference-type="ref+label" reference="sf-illustrative-2"}, green) visits vertex $w$ twice, and is therefore not a path.

The constraint that vertices cannot be revisited is a key challenge of the SPP in GCS. This is unlike the classical SPP with non-negative edge lengths, where this constraint does not increase problem complexity. It can be shown that if we allow vertex revisits, then the principle of optimality holds, and the optimal decision policy is independent of past decisions. This is illustrated in [6](#sf-illustrative-2){reference-type="ref+label" reference="sf-illustrative-2"}, where the optimal $s\textsf{-}t$ and $v\textsf{-}t$ solutions to the relaxed problem are shown in green and blue respectively.
:::

## All-Pairs Shortest Paths in a Graph of Convex Sets {#ss-apsp-in-gcs}

The APSP in GCS extends the classical APSP in a natural way. We are given a set of source vertices $\mathcal S\subset \mathcal V$ and a set of target vertices $\mathcal T\subset \mathcal V$. The goal is to solve the SPP in GCS between every pair of source and target points $\bar x_s \in \mathcal X_s$ and $\bar x_t \in \mathcal X_t$, and every pair of source and target vertices $s \in \mathcal S$ and $t \in \mathcal T$. Since the SPP in GCS is NP-hard, the APSP in GCS is at least NP-hard as well.

## Method outline {#ss-solution-overview}

Our approach generalizes the solution to the classical APSP outlined in [2.1](#ss-apsp-in-graph){reference-type="ref+label" reference="ss-apsp-in-graph"}. We proceed in two phases. Offline, we compute a coarse quadratic lower bound on the cost-to-go between relevant pairs of GCS vertices. Then online, we extend the greedy policy ([\[e-successor-policy\]](#e-successor-policy){reference-type="ref+label" reference="e-successor-policy"}) to the GCS setting. At runtime, we rollout this policy to obtain the solution path incrementally, one vertex at a time.

Unlike the classical APSP, a greedy policy with the cost-to-go $J^*_{s,t}$ is not an optimal policy for the APSP in GCS. This is because the optimal policy for paths in GCS depends on previously visited vertices, which is not captured by the cost-to-go $J^*_{s,t}(x_s,x_t)$. Thus, our approach is bound to yield approximate solutions, further limited by the coarseness of quadratic cost-to-go lower bounds.

To incorporate the challenging "no-vertex-revisit constraint" into the cost-to-go function, we relax this constraint by introducing penalties for vertex revisits. These penalties are applied to the edge lengths, producing a biased cost-to-go lower bound that discourages revisits. When rolling out a greedy policy online, we also explicitly prohibit vertex revisits. To mitigate the coarseness of quadratic cost-to-go lower bounds and better approximate the optimal policy, we employ a multi-step lookahead generalization of the greedy policy ([\[e-successor-policy\]](#e-successor-policy){reference-type="ref+label" reference="e-successor-policy"}), optimizing over $n$-step decision sequences at each iteration.

# Offline phase: synthesis of cost-to-go lower bounds {#s-cost-to-go-function-synthesis}

In [3.1](#ss-cost-to-go-synthesis){reference-type="ref+label" reference="ss-cost-to-go-synthesis"}, we present the optimization problem that produces cost-to-go lower bounds for the APSP in GCS. This program is infinite-dimensional, so in [3.2](#ss-sdp){reference-type="ref+label" reference="ss-sdp"} we present a tractable numerical approximation for it.

For clarity of presentation, we make some simplifying assumptions. First, we assume that we have just one source vertex and one target vertex, i.e., $\mathcal S=\{s\}$ and $\mathcal T=\{t\}$. Second, we assume that the set $\mathcal X_t$ corresponding to the target vertex $t$ is a singleton: $\mathcal X_t = \{ x_t\}$. Since the target vertex $t$ and point $x_t$ are fixed, we also simplify the notation and refer to $J_{v,t}^*(x_v, x_t)$ as $J^*_v(x_v)$. The extensions of our method when these assumptions do not hold are straightforward and discussed in [7](#a-further-generalization){reference-type="ref+label" reference="a-further-generalization"}.

## Cost-to-go lower bounds via infinite-dimensional LP {#ss-cost-to-go-synthesis}

The cost-to-go lower bounds are synthesized with the following optimization problem: $$\label{e-path-cost-to-go-synthesis}
\begin{align}
\max_{\{J_v,  h_v\}_{v \in \mathcal V}}  \quad &  
\int_{\mathcal X_s} J_s(x) d\phi_s(x) && \label{e-p-objective} \\
\text{s.t.} \quad & J_v: \mathcal X_v\rightarrow\mathbb R, &&\forall v\in \mathcal V, \label{e-p-value-def} \\
& h_w \geq 0  &&\forall w\in\mathcal V,\label{e-p-penalty-def}\\
&  J_v(x_v) \leq l_e(x_v, x_w) + h_w + J_w(x_w),  && \forall e=(v,w)\in\mathcal E,\! \label{e-p-lower-bound}\\
&&& \forall (x_v,x_w)\in\mathcal X_e,\! \nonumber\\
& J_t(x_t) = - \sum_{w\in\mathcal V} h_w. \label{e-p-target-value}
\end{align}$$ We now give a detailed line-by-line explanation of this program, and prove the validity of the lower bounds it produces in [\[theorem-prog-lower-bound\]](#theorem-prog-lower-bound){reference-type="ref+label" reference="theorem-prog-lower-bound"} below.

In constraint ([\[e-p-value-def\]](#e-p-value-def){reference-type="ref+label" reference="e-p-value-def"}), we associate with every vertex $v\in\mathcal V$ a (possibly non-convex) function $J_v$ defined over the set $\mathcal X_v$. These functions serve as the lower bounds on the cost-to-go $J_v^*$, as will be shown later. We emphasize that we are searching over the space of functions $J_v$, not over the individual points $x_v$.

In the objective function ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}), $\phi_s$ is a probability distribution of anticipated source conditions over the set $\mathcal X_s$. Thus, the integral in ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}) maximizes the weighted average of $J_s$ over the source set $\mathcal X_s$, effectively "pushing up" on the cost-to-go lower bound at the source vertex.

In ([\[e-p-penalty-def\]](#e-p-penalty-def){reference-type="ref+label" reference="e-p-penalty-def"}), we introduce a non-negative penalty $h_w$ for every vertex $w\in\mathcal V$. This penalty is meant to discourage revisits to vertex $w$, which is a way to relax the constraint that a path must not visit any vertex more than once.

To implement the penalty $h_w$, we increment the edge length $l_e$ for every edge $e\in\mathcal E$ that enters vertex $w$. This is formalized in ([\[e-p-lower-bound\]](#e-p-lower-bound){reference-type="ref+label" reference="e-p-lower-bound"}), which states that for every edge $e = (v,w)$ and a feasible transition $(x_v,x_w)\in\mathcal X_e$, the value $J_v(x_v)$ is a lower bound on the sum of the penalty-incremented edge length $l_e(x_v,x_w) + h_w$ and the subsequent cost-to-go lower bound $J_w(x_w)$. As written, the non-negative penalty $h_w$ increases the cost of the edges leading into vertex $w$, thereby discouraging visits to $w$. However, since our goal is to only discourage vertex revisits, we need to waive the penalty $h_w$ once. This is achieved by setting the cost-to-go lower bound $J_t(x_t)$ to $-\sum_{w\in\mathcal V} h_w$ in constraint ([\[e-p-target-value\]](#e-p-target-value){reference-type="ref+label" reference="e-p-target-value"}). Upon reaching the target vertex, we subtract the sum of all vertex penalties from the cost-to-go lower bound, effectively waiving the penalties once per vertex. We now show that these constraints produce lower bounds on the cost-to-go function.

::: lemma
[]{#theorem-prog-lower-bound label="theorem-prog-lower-bound"} Let $J_v$ and $h_v$ for $v\in \mathcal V$ be a feasible solution of problem ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}). Then $$J_v(x_v)\leq J_v^*(x_v) \text{ for all } v\in\mathcal V.$$
:::

::: proof
*Proof.* Consider the optimal solution to program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}), and let $v$ be some vertex. Let $p$ be an optimal path from a point $x_v\in\mathcal X_v$ to the target point $x_t$. Since $p$ is a path, it contains no repeated vertices. Adding the constraint ([\[e-p-lower-bound\]](#e-p-lower-bound){reference-type="ref+label" reference="e-p-lower-bound"}) along the edges $\mathcal E_p$ of this optimal path, we have: $$\begin{align}
\label{e-lower-bound-penalties}
J_v(x_v) \leq \sum_{e=(u,w)\in\mathcal E_p} l_e(x_u,x_w)  \sum_{w\in p} h_w + J_t(x_t),
\end{align}$$ where $x_u,x_w$ are the vertex variables of the optimal trajectory corresponding to $p$. Constraint ([\[e-p-target-value\]](#e-p-target-value){reference-type="ref+label" reference="e-p-target-value"}) states that $J_t(x_t)=- \sum_{w\in\mathcal V} h_w$, while the sum of the edge lengths $l_e(x_u,x_w)$ along the optimal path $p$ is by definition the cost-to-go $J_v^*(x_v)$. Substituting and rearranging terms, we obtain: $$\begin{align}
\label{e-lower-bound-penalties-2}
J_v(x_v)+ \sum_{w\notin p} h_w \;\leq\;  J_v^*(x_v).
\end{align}$$ Since the penalties $h_w$ are non-negative by ([\[e-p-penalty-def\]](#e-p-penalty-def){reference-type="ref+label" reference="e-p-penalty-def"}), the conclusion follows. 0◻ ◻
:::

By maximizing the weighted average of $J_s$ in the objective function ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}), the program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) seeks the best possible lower bound $J_s$ on the cost-to-go $J_s^*$, up to the relaxation gap introduced by the vertex penalties. This gap is clear from ([\[e-lower-bound-penalties-2\]](#e-lower-bound-penalties-2){reference-type="ref+label" reference="e-lower-bound-penalties-2"}): for $x_s\in\mathcal X_s$, the sum of the off-the-optimal-path penalty terms $\sum_{w\notin p} h_w$ need not to be zero, so $J_s(x_s)$ need not be a tight lower bound on $J_s^*(x_s)$. In other words, recall that, upon reaching the target, we waive the penalties $h_w$ for every vertex $w\in\mathcal V$. As a result, we do not just waive the first-time penalties on vertices along the optimal path $p$, we also waive the off-the-path penalties $\sum_{w\notin p} h_w$, which were never accrued in the first place. Waiving these off-the-path penalties introduces the gap between $J_s$ and $J_s^*$.

#### Example 1, continued.

Consider the solution to program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) for the GCS instance in [7](#f-illustrative){reference-type="ref+label" reference="f-illustrative"}. Setting the revisit penalty $h_w = 0$ results in $J_s=14$, which is the cost of the vertex sequence that visits $w$ twice (green in [6](#sf-illustrative-2){reference-type="ref+label" reference="sf-illustrative-2"}). By jointly optimizing over the penalties and the cost-to-go lower bounds, program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) selects the penalty $h_w=2$. Revisiting vertex $w$ is no longer advantageous, and the cost of the shortest $s\textsf{-}t$ path (orange in [5](#sf-illustrative-1){reference-type="ref+label" reference="sf-illustrative-1"}) is achieved: $J_s = J_s^* = 16$.

We note that program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) naturally generalizes the cost-to-go synthesis LP for the classical SPP [@de2003linear]. When each convex set $\mathcal X_v$ is a singleton, the problem reduces to the classical SPP, where functions $J_v$ are defined at single points and represented by a single decision variable. Setting vertex penalties $h_w=0$ recovers the standard cost-to-go synthesis LP for the classical SPP: $$\begin{equation}
\begin{aligned}
\label{discrete-cost-to-go-search}
\max_{\{J_v\}_{v\in\mathcal V}}  \quad &  J_s \\
\text{s.t.} \quad &  J_v \leq l_e + J_w,   \qquad&& \forall e=(v,w)\in\mathcal E,\\
& J_t = 0.
\end{aligned}
\end{equation}$$ Compared to the purely discrete setting of ([\[discrete-cost-to-go-search\]](#discrete-cost-to-go-search){reference-type="ref+label" reference="discrete-cost-to-go-search"}), optimization program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) is also an LP; however, it searches over the space of functions and is therefore infinite-dimensional. Next, we develop a tractable finite-dimensional approximation to ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) that is conducive to numerical methods.

## Numerical approximation via semidefinite programming {#ss-sdp}

We now produce an approximate solution to the cost-to-go synthesis program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}). We restrict each function $J_{v}$ to be convex quadratic, which allows us to cast ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) as a tractable Semidefinite Program (SDP). SDPs are mathematical programs where the objective function is linear and the constraints are either linear or linear matrix inequalities (LMIs). To help with the presentation, we first state without proof three well-known facts.

::: lemma
[]{#lemma-quadratic label="lemma-quadratic"} A quadratic function $f : \mathbb R^n \rightarrow \mathbb R$ is non-negative if and only if it is representable as a Positive-Semidefinite (PSD) quadratic form: $$\begin{align}
f(x) = \begin{bmatrix}1\\x\end{bmatrix}^\top\! Q \begin{bmatrix}1\\x\end{bmatrix} \; \text{ for some } \; Q\succeq 0.\nonumber
\end{align}$$
:::

::: lemma
[]{#lemma-non-negative-on-set label="lemma-non-negative-on-set"} Let $\mathcal{X} = \{x \in \mathbb{R}^n\;|\; g_i(x)\geq 0, \; \forall i=1,\dots,m\}$. The function $f : \mathbb R^n \rightarrow \mathbb R$ is non-negative on the set $\mathcal X$ if there exists $\lambda\in\mathbb R^m_+,$ such that $f(x) - \sum_{i=0}^m\lambda_{i}g_{i}(x)$ is non-negative for every $x\in\mathbb R^n$.
:::

::: corollary
[]{#lemma-verify-with-quadratic label="lemma-verify-with-quadratic"} Suppose that in [\[lemma-non-negative-on-set\]](#lemma-non-negative-on-set){reference-type="ref+label" reference="lemma-non-negative-on-set"}, the function $f$ is quadratic, and all $g_i$ functions are affine or convex quadratic. Then we can apply [\[lemma-quadratic\]](#lemma-quadratic){reference-type="ref+label" reference="lemma-quadratic"} to verify [\[lemma-non-negative-on-set\]](#lemma-non-negative-on-set){reference-type="ref+label" reference="lemma-non-negative-on-set"} via an LMI, i.e., we can verify if $f$ is non-negative over $\mathcal X$ by searching for a PSD matrix in an affine subspace.
:::

Using these facts, we proceed to cast program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) as an SDP.

#### Defining cost-to-go lower bounds in ([\[e-p-value-def\]](#e-p-value-def){reference-type="ref+label" reference="e-p-value-def"}).

We restrict lower bounds $J_v$ per vertex $v\in\mathcal V$ to be convex quadratic functions. By [\[lemma-quadratic\]](#lemma-quadratic){reference-type="ref+label" reference="lemma-quadratic"}, searching for such functions is equivalent to searching for appropriate PSD matrices $Q_v$. The decision variables are thus the coefficients of the quadratic polynomials. As a result, we produce coarse quadratic lower bounds on the optimal $J^*_v$; this coarseness will be mitigated via the multi-step lookahead policies.

Constraint ([\[e-p-penalty-def\]](#e-p-penalty-def){reference-type="ref+label" reference="e-p-penalty-def"}) is already linear, and constraint ([\[e-p-target-value\]](#e-p-target-value){reference-type="ref+label" reference="e-p-target-value"}) is linear in the coefficients of the quadratic polynomial $J_t$ and the decision variables $h_w$. These constraints are thus already suitable for the SDP.

#### Enforcing the lower-bound constraint ([\[e-p-lower-bound\]](#e-p-lower-bound){reference-type="ref+label" reference="e-p-lower-bound"}).

To apply [\[lemma-verify-with-quadratic\]](#lemma-verify-with-quadratic){reference-type="ref+label" reference="lemma-verify-with-quadratic"} to enforce this constraint, we impose additional restrictions. First, we restrict vertex and edge sets $\mathcal X_v$ and $\mathcal X_e$ to be intersections of ellipsoids and polyhedra. We also restrict edge lengths $l_e$ to be quadratic, ensuring that the expression in ([\[e-p-lower-bound\]](#e-p-lower-bound){reference-type="ref+label" reference="e-p-lower-bound"}) is quadratic. For non-quadratic $l_e$, such as the Euclidean distance, we use a quadratic approximation instead. Applying [\[lemma-verify-with-quadratic\]](#lemma-verify-with-quadratic){reference-type="ref+label" reference="lemma-verify-with-quadratic"}, we verify constraint ([\[e-p-lower-bound\]](#e-p-lower-bound){reference-type="ref+label" reference="e-p-lower-bound"}) with an LMI.

#### The objective function ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}).

Since $J_s$ is a quadratic polynomial, the integral in ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}) is linear in the coefficients of $J_s$, which are the decision variables of the program. Therefore, the objective function ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}) is linear in the decision variables, as required for the SDP.

Empirically, we found quadratic lower bounds to be a good balance between computational complexity and expressive power. Note that higher-degree polynomial lower bounds $J_v$ can be synthesized via the Sums-of-Squares (SOS) hierarchy [@parrilo2000structured; @parrilo2003semidefinite; @lasserre2001global]. However, in practice, the resulting programs tend to be prohibitively expensive. On the other hand, restricting $J_{v}$ to be affine yields a program that almost exactly matches the dual to the convex relaxation of the SPP in GCS, discussed in [@marcucci2024shortest App. B]. In other words, solving the SPP in GCS already gives a coarse affine cost-to-go lower bound that can be used to solve the APSP in GCS. In [5.3](#ss-ablation-example){reference-type="ref+label" reference="ss-ablation-example"}, we show that empirically, these affine lower bounds have significantly less expressive power than the quadratic lower bounds.

# Online phase: greedy multi-step lookahead policy {#s-lookahead-policies}

We now generalize the greedy successor policy ([\[e-successor-policy\]](#e-successor-policy){reference-type="ref+label" reference="e-successor-policy"}) from the classical APSP to the GCS setting. Suppose that at runtime, we are given a source vertex $v_0 \in \mathcal S$ and a source point $x_0 \in \mathcal X_{v_0}$. At iteration $k$ of the policy rollout, let $(v_k,x_k)$ be the current vertex and vertex variable, and let $p_k = (v_0, v_1, \ldots, v_{k-1})$ be the path so far. The successor policy $\pi(v_k, x_k, p_k) = (v_{k+1}, x_{k+1})$, which we will define shortly, produces the next vertex $v_{k+1}$ and the corresponding vertex variable $x_{k+1}$. We then advance to the next iteration. The rollout terminates when we reach the target vertex $t$, where we must select the target point $x_t$. Upon termination, we extract the vertex path $p = (v_0, v_1, \ldots, v_t)$ and re-optimize for the continuous vertex variables $(x_0, x_1, \ldots, x_t)$, so as to produce a trajectory that is optimal within this path.

At each iteration of the policy rollout, we solve a greedy lookahead optimization problem with the coarse quadratic lower bounds obtained in [3.2](#ss-sdp){reference-type="ref+label" reference="ss-sdp"}. For simplicity, here we present just the 1-step lookahead program: $$\label{e-policy}
\begin{align}
\pi(v_k ,x_k, p_k) \quad=\quad \underset{(w, x_w)}{\arg\min}& \quad  l_e(x_k, x_w) + J_{w}(x_w) \label{e-policy-objective} \\
\text{s.t.} & \quad e=(v_k,w)\in\mathcal E, \quad w\notin p_k, \label{e-policy-discrete-con} \\
& \quad (x_k,x_w)\in\mathcal X_e. \label{e-policy-continuous-con}
\end{align}$$ Note that we do not use the penalty-incremented edge cost $l_e(x_k,x_w) + h_w$ in ([\[e-policy-objective\]](#e-policy-objective){reference-type="ref+label" reference="e-policy-objective"}), since the penalty $h_w$ is waived the first time that $w$ is visited. Vertex revisits are then also explicitly prohibited in ([\[e-policy-discrete-con\]](#e-policy-discrete-con){reference-type="ref+label" reference="e-policy-discrete-con"}).

In a multi-step lookahead formulation, we instead solve for an $n$-step optimal decision sequence, take just the first step, and repeat at next iteration. The multi-step lookahead is key for mitigating the coarseness of the quadratic lower bounds. This is because an $n$-step lookahead from vertex $v$ effectively produces a piecewise-quadratic lower bound on the cost-to-go $J_v^*$ over $\mathcal X_v$, which has significantly more expressive power. While these lower bounds can still be loose in theory, the multi-step lookahead enables effective decision-making in practice.

Convexity of $J_{w}$ is crucial, as it allows us to solve the program ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}) efficiently at run-time. To find the minimizer to ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}), we solve multiple convex programs in parallel, one for every $n$-step lookahead sequence.

Finally, we note that the lookahead program ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}) is not guaranteed to be recursively feasible. If we end up in a vertex where ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}) has no solution, we backtrack to a previous vertex that has a different feasible outgoing edge, and retry from there. Generally, our planner is sound but not complete: it is not guaranteed to produce a solution, but every solution it produces is feasible.

# Experimental evaluation {#s-experiments}

We evaluate our approach through multiple numerical experiments. [5.1](#ss-simple-intuitive-example){reference-type="ref+label" reference="ss-simple-intuitive-example"} presents a simple two-dimensional problem that provides visual intuition to our method. In [5.2](#ss-robot-arm-example){reference-type="ref+label" reference="ss-robot-arm-example"}, we apply our approach to a complex high-dimensional scenario, the robot arm in [1](#f-robot-arm-title){reference-type="ref+label" reference="f-robot-arm-title"}. Finally, [5.3](#ss-ablation-example){reference-type="ref+label" reference="ss-ablation-example"} shows that our approach scales well to large graphs. We also discuss how the coarseness of the cost-to-go lower bounds and the multi-step lookahead horizon impact the performance.

All of the experiments are run on a desktop computer with a 4.5Ghz 16-core AMD Ryzen 9 processor and 64GB 4800MHz DDR5 memory. We use Mosek 10.2.1 [@mosek] to solve all the convex programs in this section.

## Two-dimensional example {#ss-simple-intuitive-example}

We first consider a two-dimensional GCS problem in [4](#f-gcs-example){reference-type="ref+label" reference="f-gcs-example"}. We have a graph $G$ with $|\mathcal V| = 9$ vertices, $|\mathcal E| = 25$ edges, including multiple cycles. The geometry of the convex sets $\mathcal X_v$ can be deduced from [2](#sf-g1){reference-type="ref+label" reference="sf-g1"}; no edge constraints $\mathcal X_e$ are used. The edge costs $l_e(x_v,x_w) = \|x_v-x_w\|_2^2$ are the squared Euclidean distance. The source vertex $s$ is a box, and the target vertex $t$ is a singleton.

We compute the convex quadratic lower bounds on the cost-to-go function at every vertex and visualize their contour plots in [2](#sf-g1){reference-type="ref+label" reference="sf-g1"}. In [3](#sf-g2){reference-type="ref+label" reference="sf-g2"}, we depict the first three iterations of the 1-step lookahead rollout of the successor policy ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}). At each iteration, we expand the neighbours of the current vertex and greedily select the next vertex $w$ and the vertex point $x_w$ that minimize the objective ([\[e-policy-objective\]](#e-policy-objective){reference-type="ref+label" reference="e-policy-objective"}). The rollout proceeds until the target vertex $t$ is reached.

:::: {#f-lookahead-comparison .figure latex-placement="t!"}
![](Morozov2024MultiQuery_figs/cost-to-go-comparison.png){width="\\textwidth"}

::: caption
Comparison of lower and upper bounds on the cost-to-go over a horizontal slice of the source set $\mathcal X_s$ from [2](#sf-g1){reference-type="ref+label" reference="sf-g1"}. The cost-to-go function $J_s^*$ (green) is piecewise-quadratic. Convex quadratic lower bound $J_s$ (purple) is naturally a poor lower-bound. Multi-step lookaheads (solid orange, blue) produce tighter piecewise-quadratic lower bounds. Upper bounds on the cost-to-go are obtained by rolling out the multi-step lookahead policy (dashed orange, blue), which produces near-optimal solutions.
:::
::::

We evaluate the quality of the cost-to-go lower bounds and the resulting solutions in [8](#f-lookahead-comparison){reference-type="ref+label" reference="f-lookahead-comparison"}. The optimal shortest path cost-to-go function $J_{s}^*$ (green) is piecewise-quadratic. Naturally, the convex quadratic lower bound $J_s$ (purple) is a poor lower bound to $J_{s}^*$. The quality of the lower bound is greatly improved via multi-step lookaheads (solid lines, orange for 1-step, blue for 2-step). A horizon-$n$ lookahead produces a piecewise-quadratic lower bound to $J_{s}^*$, with up to as many quadratic pieces as there are different $n$-step paths from the source vertex $s$. Though neither 1-step nor 2-step lookahead lower bounds are tight, they are sufficient for near-optimal decision making. The costs of the rollouts of the successor policy are plotted as dashed lines; 2-step lookahead rollouts (blue) attain optimal solutions nearly always.

## Collision-free motion planning for a robot arm {#ss-robot-arm-example}

We now demonstrate that our approach scales well to high-dimensional hardware systems. We study multi-query collision-free motion planning for the KUKA iiwa robotic arm ([1](#f-robot-arm-title){reference-type="ref+label" reference="f-robot-arm-title"}), tasked with moving virtual items between shelves and bins. Our methodology requires minimal additional offline computation, while delivering significant online speed up with negligible solution quality reduction.

We first produce an approximate polytopic decomposition of the 7-dimen­sional collision-free configuration space of the arm. This is done via the IRIS-NP algorithm [@petersen2023growing], and we use IRIS clique seeding [@werner2023approximating] to obtain polytopes inside the shelves and bins. We assign a GCS vertex $v$ per polytope in this decomposition. The convex set $\mathcal X_v$ is the set of linear segments contained within the region, with the segment represented by its endpoints. Two GCS vertices are connected by an edge if the corresponding regions overlap. The resulting graph contains 23 vertices and 68 edges. For each edge $e\!=\!(v,w)$, we constrain the linear segments at $v$ and $w$ to form a continuous path. The path length is the sum of the Euclidean distances of the linear segments. We define 12 source vertices (6 shelves, 2 vertices per shelf) and 3 target vertices (inside the left, front, and right bins). To generate the quadratic lower bounds on the cost-to-go function, we use the generalization of ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) discussed in [7](#a-further-generalization){reference-type="ref+label" reference="a-further-generalization"}.

:::: {#f-arm-numerics .figure latex-placement="t!"}
![](Morozov2024MultiQuery_figs/method_comparison_for_robot_arm.png){width="\\textwidth"}

::: caption
For the robot arm scenario in [5.2](#ss-robot-arm-example){reference-type="ref+label" reference="ss-robot-arm-example"}, we compare path length and solve time performance between the APSP in GCS, single-query SPP in GCS, and shortcut PRM over 120 queries. The offline phases take 106s, 100s, and 0.9s respectively. The APSP in GCS is on average 40 times faster than the SPP in GCS, with minimal reduction in solution quality. Compared to sPRM, the APSP in GCS is on average 110 times faster.
:::
::::

We evaluate our algorithm in a multi-query scenario: at runtime, the arm is given a random next position to go to, alternating between shelves and bins. We rollout a 1-step lookahead policy to generate paths from shelves to bins, and reverse them to obtain paths from bins to shelves. We evaluate our approach on a total of 120 queries. We compare our algorithm against solving the SPP in GCS from scratch, as well as against the shortcut PRM (sPRM) algorithm, which is its natural sampling based multi-query competitor. We use a high-performance implementation of sPRM based on [@prm-rob], producing a large roadmap with 10,000 vertices. Our solutions are visualized in [1](#f-robot-arm-title){reference-type="ref+label" reference="f-robot-arm-title"}; performance comparison is provided in [9](#f-arm-numerics){reference-type="ref+label" reference="f-arm-numerics"}. Similar to how the quality of the PRM solutions depends on the density of the PRM, the quality of solutions obtained with GCS depends on the quality of the polytopic decomposition of the collision-free configuration space. We thus make no claims about the optimality of the solutions in this section.

Offline, generating cost-to-go lower bounds takes only 6 seconds, which is just 6% of the time that it takes to generate the polytopic decomposition necessary to use GCS. Then online, our policy rollouts are very fast, with a median solve time of 5ms and a maximum of 11ms (we report the parallelized solver time). Our method is on average 40 time faster than the SPP in GCS, producing paths that are only 7% longer on average. Compared to sPRM, our method is on average 110 times faster and produces paths that are 5% shorter on average. We achieve consistent performance in both solve time and path length, unlike sPRM, which shows high variance in both. Overall, compared to these state-of-the-art baselines, the APSP in GCS reduces the online solve times significantly, with minimal compromise in solution quality.

## Scalability and ablation on lower bounds and lookahead horizon {#ss-ablation-example}

In this section, we demonstrate the scalability of our approach and analyze how the coarseness of the cost-to-go lower bounds and the lookahead horizon impact solution quality. First, we show that multi-step lookaheads with quadratic $J_{v}$ yield near-optimal solutions in large graphs. Second, we demonstrate that quadratic lower bounds significantly outperform the affine ones, which are available from the dual of the convex relaxation of the SPP in GCS [@marcucci2024shortest App. B].

:::: {#f-3-birchtree-plots .figure latex-placement="t!"}
![Optimal solution.](Morozov2024MultiQuery_figs/p1.png){#sf-sa width="\\textwidth"}

![Quadratic lower bounds.](Morozov2024MultiQuery_figs/p2.png){#sf-sb width="\\textwidth"}

![Affine lower bounds.](Morozov2024MultiQuery_figs/p3.png){#sf-sc width="\\textwidth"}

::: caption
A 3-step lookahead policy with quadratic $J_{v}$ (blue) yields diverse vertex paths resembling the optimal solutions (green). A 3-step lookahead with affine $J_{v}$ (orange) follows a single vertex sequence regardless of the target point, accruing much higher cost.
:::
::::

We consider a randomly generated environment depicted in [13](#f-3-birchtree-plots){reference-type="ref+label" reference="f-3-birchtree-plots"}. We assign a GCS vertex $v$ for each teal box. Each convex set $\mathcal X_v$ is the set of control points of a cubic Bézier curve within the box (see [@marcucci2023motion]). The GCS vertices are connected by a pair of edges if the corresponding teal boxes overlap. The resulting graph has 190 vertices and 540 edges. For each edge, we constrain the vertex Bézier curves to be differentiable at the transition point. The path cost is the sum of squared Euclidean distances between the consecutive control points of the Bézier curves. The source vertex $s$ is at the top, and the target vertex $t$ is at the bottom.

We synthesize the quadratic and affine lower bounds over the GCS, which takes 6s and 2s respectively. We then uniformly sample 120 pairs of source and target conditions, and rollout the greedy policy using different lower bounds and lookahead horizons. Optimal solutions are obtained by solving the MICP formulation of the SPP in GCS. Numerical results are reported in [1](#t-numerics-ablation){reference-type="ref+label" reference="t-numerics-ablation"}.

[1](#t-numerics-ablation){reference-type="ref+label" reference="t-numerics-ablation"} shows that our approach scales well to large problem instances, yielding better solve times than the SPP in GCS. A 2-3 step lookahead policy with a quadratic cost-to-go lower bound produces near-optimal solutions (8-9% median suboptimality) in under 10ms. The SPP in GCS produces slightly better solutions (7% median suboptimality), but due to the size of the graph, the solve-time increases to over 1000ms. For large graph instances, incremental search through the graph via the APSP in GCS achieves competitive solution quality while reducing solve times by up to two-three orders of magnitude.

Finally, [1](#t-numerics-ablation){reference-type="ref+label" reference="t-numerics-ablation"} shows that quadratic lower bounds with short-horizon lookaheads offer a good balance between expressive power and solve times. A 3-step lookahead policy with affine lower bounds has a median suboptimality of 80.2%, compared to 8.8% with quadratic lower bounds. Achieving similar solution quality with affine lower bounds requires a lookahead horizon of 8-9 steps, but the resulting rollouts take significantly more time. [13](#f-3-birchtree-plots){reference-type="ref+label" reference="f-3-birchtree-plots"} shows that 3-step lookahead rollouts with affine lower bounds fail to capture the diversity of optimal solutions. Additionally, low-horizon lookahead policies with affine lower bounds often fail to produce solutions within a reasonable number of iterations, as demonstrated by the failure rate statistics. Overall, we observe that the lookahead policies with quadratic lower bounds perform much better than those with affine ones.

::: {#t-numerics-ablation}
  **Solution method**           **Optimality gap, %**   **Solve time, ms**   **Failure rate, %**
  --------------------------- ----------------------- -------------------- ---------------------
  Quadratic $J_{v}$, 1-step               20.0 (62.1)                3 (3)                   0.0
  Quadratic $J_{v}$, 2-step                9.4 (22.3)                4 (4)                   0.0
  Quadratic $J_{v}$, 3-step                8.8 (15.7)                5 (6)                   0.0
  Affine $J_{v}$, 1-step                     157.1 ()              2 (657)                  27.2
  Affine $J_{v}$, 2-step                142.4 (418.8)              3 (914)                  14.0
  Affine $J_{v}$, 3-step                 80.2 (348.3)              5 (808)                   9.9
  Affine $J_{v}$, 8-step                  11.9 (37.4)           169 (1996)                   3.3
  Affine $J_{v}$, 9-step                   7.0 (26.2)           388 (2454)                   0.0
  SPP in GCS                               6.9 (12.0)           716 (1051)                   0.0

  : Impact of the degree of $J_{v}$ and lookahead horizon on performance, over 120 queries for the GCS in [13](#f-3-birchtree-plots){reference-type="ref+label" reference="f-3-birchtree-plots"}. We report optimality gaps (ratio between solution cost and optimal cost), solve times, and failure rates (rollout policy is terminated after 10,000 iterations). We report median values, with the 75th percentile in the parenthesis. Low-horizon lookahead policies with quadratic lower bounds yield near optimal solutions, perform much better than the affine bounds.
:::

# Conclusion and future work {#s-discussion}

In this work, we generalized the classical All-Pairs Shortest-Paths problem to the Graphs of Convex Sets, and developed practical approximate numerical methods for solving this problem. We demonstrated that a coarse lower bound on the cost-to-go with a greedy multi-step lookahead policy produce near-optimal paths, while significantly reducing solve times. Our methodology effectively scales to high-dimensional set scenarios and large graph instances, enabling practical robotics applications in multi-query settings. We plan to provide an efficient implementation of our approach within the Drake library [@drake].

For hardware applications in non-static environments, we are interested in ways to tackle changes to the robot's configuration space, like those arising in object manipulation, as well as addition and removal of obstacles. Assuming the changes are minor, the online search via the multi-step lookahead policy provides natural local adaptation. Changes to the environment can be incorporated into the online policy rollout program ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}) via non-convex constraints, similar to [@vonusing].

Finally, we are interested in exploring alternative incremental search policies beyond the multi-step lookahead policy. We expect randomized rollouts inspired by MCTS [@browne2012survey] and A\*-based approaches like [@chia2024gcs] to be effective.

# Extensions and variations {#a-further-generalization}

We briefly remark on various natural generalizations to program ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}).

1.  Suppose the set of source vertices $\mathcal S$ has more than one vertex. To simultaneously "push up" lower bounds $J_s$ per vertex $s\in\mathcal S$, we add extra integral terms to the objective function ([\[e-p-objective\]](#e-p-objective){reference-type="ref+label" reference="e-p-objective"}).

2.  Suppose the target set $\mathcal X_t$ is not a singleton, but a compact convex set. First, we modify the constraint ([\[e-p-value-def\]](#e-p-value-def){reference-type="ref+label" reference="e-p-value-def"}) to search for $J_{v,t}:\mathcal X_v \times \mathcal X_t \rightarrow \mathbb R$. The function $J_{v,t}(x_v,x_t)$ is a lower bound on the cost-to-go of the shortest path from $x_v$ of vertex $v$ to $x_t$ of vertex $t$. Similarly, the probability distribution $\phi_{s,t}$ is now supported on $\mathcal X_s\times\mathcal X_t$, so as to push up on $J_{s,t}(x_s,x_t)$ over all source-target pairs $(x_s,x_t)$. The lower-bound constraint ([\[e-p-lower-bound\]](#e-p-lower-bound){reference-type="ref+label" reference="e-p-lower-bound"}) is adjusted to include $x_t\in\mathcal X_t$: $$J_{v,t}(x_v, x_t) \leq  l_e(x_v, x_w) +  h_w + J_{w,t}(x_w, x_t),$$ for all edges $e=(v,w)\in\mathcal E$, and all points $(x_v,x_w)\in \mathcal X_e$ and $x_t\in\mathcal X_t$. Finally, the target constraint ([\[e-p-target-value\]](#e-p-target-value){reference-type="ref+label" reference="e-p-target-value"}) is adjusted to be $J_{t,t}(x_t, x_t) = -\sum_{w\in\mathcal V} h_w$, for all $x_t\in\mathcal X_t$.

3.  The scalar vertex penalty $h_w$ is generalized to be a non-negative function of the target state $x_t$, that is: $h_{w,t}:\mathcal X_t\rightarrow \mathbb R_+$. We thus replace $h_w$ with $h_{w,t}(x_t)$ and update the constraint ([\[e-p-target-value\]](#e-p-target-value){reference-type="ref+label" reference="e-p-target-value"}) as follows: $$J_{t,t}(x_t, x_t) = -\sum_{w\in\mathcal V} h_w(x_t),$$ further tightening the resulting lower-bounds.

4.  Suppose the set of target vertices $\mathcal T$ has more than one vertex. To obtain the cost-to-go lower bounds for every pair of vertices $v\in\mathcal V$ and $t\in\mathcal T$, we solve multiple programs ([\[e-path-cost-to-go-synthesis\]](#e-path-cost-to-go-synthesis){reference-type="ref+label" reference="e-path-cost-to-go-synthesis"}) in parallel, one per target vertex $t\in\mathcal T$.

5.  In general, the successor policy ([\[e-policy\]](#e-policy){reference-type="ref+label" reference="e-policy"}) is also a function of terminal vertex $t$ and terminal point $x_t$. The generalized 1-step lookahead program is as follows: $$\begin{align*}
    \pi(v_k ,x_k, p_k, t, x_t) \quad=\quad \underset{(w, x_w)}{\arg\min}& \quad  l_e(x_k, x_w) + J_{w,t}(x_w, x_t) \\
    \text{s.t.} & \quad e=(v_k,w)\in\mathcal E_{v_k}^{\text{out}}, \quad w\notin p_k, \nonumber\\
    & \quad (x_k,x_w)\in\mathcal X_e. \nonumber
    \end{align*}$$

6.  Other penalties, similar to the vertex visitation penalties $h_{v}$, can be added to improve the quality of the lower bounds. For instance, consider a 2-cycle with edges $(v,w)$ and $(w,v)$. We can add edge penalties $h_{v,w} = h_{w,v}$ for traversing either edge. By subtracting $h_{v,w}$ from the cost-to-go lower bound at the target, we effectively ensure that no penalty is incurred for traversing just one (but not both) of the edges. This can be extended to cycles of arbitrary length.

[^1]: This work was supported by Amazon.com Services LLC, PO No. 2D-12585006; The AI Institute; Dexai Robotics; National Science Foundation, DMS-2022448, UC Berkeley, 00010918. Corresponding author is Savva Morozov, `savva@mit.edu`.
