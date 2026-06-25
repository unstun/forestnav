---
citation_key: Marcucci2021Shortest
arxiv_id: 2101.11565
arxiv_url: https://arxiv.org/abs/2101.11565
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:31:34Z
origin: ai+web
reviewed: false
---

::: keywords
Shortest-path problem, graph problems with neighborhoods, mixed-integer convex programming, perspective formulation, optimal control.
:::

::: MSCcodes
52B05, 90C11, 90C25, 90C35, 90C57, 93C55, 93C83.
:::

# Introduction {#sec:intro}

:::: {#fig:toy_example .figure latex-placement="t"}
![](Marcucci2021Shortest_figs/spp_in_gcs.png){height="3.2cm"}

::: caption
Example of an SPP in GCS. The source set is on the left and the target set is on the right. The graph edges are arrows, and the shortest path is shown in dashed green. The dotted red lines connect the optimal positions of the vertices along the shortest path.
:::
::::

The Shortest-Path Problem (SPP) is one of the most important and ubiquitous problems in combinatorial optimization. In its single-source single-target version, this problem asks for a path of minimum length connecting two prescribed vertices of a graph, where the length of a path is defined as the sum of the lengths of its edges. Typically, the edge lengths are fixed scalars, given as problem data, and the assumptions made on their values have a dramatic impact on the problem complexity [@schrijver2003combinatorial Chapters 6 to 8]. In this paper we introduce the SPP in Graph of Convex Sets (GCS), a variant of the SPP in which the edge lengths are convex functions of continuous variables representing the position of the vertices (see Figure [1](#fig:toy_example){reference-type="ref" reference="fig:toy_example"}). More precisely, a GCS is a directed graph in which each vertex is paired with a convex set. The spatial position of a vertex is a continuous variable, constrained to lie in the corresponding convex set. The length of an edge is a given convex function of the position of the vertices that this edge connects. When looking for a path of minimum length in a GCS, we then have the extra degree of freedom of optimizing the position of the vertices visited by the path. According to the literature, this problem could also be classified as an SPP *with neighborhoods*; we call it SPP in GCS to highlight the crucial role that convexity plays in the developments of this paper.

Many problems of practical interest can be formulated as SPPs in GCS: for some of those the convex sets and the edge-length functions are naturally suggested by the application, for others the construction of the GCS requires more thinking. As an example of the former class of problems, scheduling the flight of a drone with limited batteries is immediately cast as an SPP in GCS like the one in Figure [1](#fig:toy_example){reference-type="ref" reference="fig:toy_example"}. The start region is on the left, the goal region is on the right, and the remaining regions can be used for recharging. Pairs of regions that are close enough for the drone to fly between are connected by an edge. The objective is to minimize the overall length of the flight. Optimal control of discrete-time hybrid dynamical systems [@bemporad1999control] is a main application that we target in this paper, and is an example of a problem whose formulation as an SPP in GCS is nontrivial. In this case we let the convex sets live in the joint state and control space of the dynamical system. Each discrete time step corresponds to an edge transition in the GCS, and the edge lengths quantify, e.g., the energy consumed to move between states (a length that is infinite if the motion is not compatible with the system dynamics). This is explained in detail in Section [8](#sec:optimal_control){reference-type="ref" reference="sec:optimal_control"}.

## Contributions

The following are the main contributions of this article.

### Problem statement (Section [2](#sec:statement){reference-type="ref" reference="sec:statement"}) {#problem-statement-section-secstatement .unnumbered}

The SPP in GCS represents an unexplored class of problems at the interface of combinatorial and convex optimization. It lends itself to a simple problem statement and, at the same time, it is a versatile framework that includes as special cases many problems of practical relevance.

### Mixed-integer convex formulation (Section [5](#sec:micp){reference-type="ref" reference="sec:micp"}) {#mixed-integer-convex-formulation-section-secmicp .unnumbered}

The SPP in GCS is easily seen to be NP-hard (Section [3](#sec:complexity){reference-type="ref" reference="sec:complexity"}). Our main contribution is the formulation of this problem as a strong and lightweight Mixed-Integer Convex Program (MICP). This program extends in a natural way the classical network-flow formulation of the SPP, and it allows us to efficiently find shortest paths in large graphs (hundreds of vertices) and high-dimensional spaces (tens of dimensions). In addition, the design principles of this MICP can be applied to improve existing mixed-integer formulations of other graph problems with neighborhoods, which are limited to small graphs and sets in two or three dimensions (see Appendix [11](#sec:extensions){reference-type="ref" reference="sec:extensions"}).

### Set-based convex relaxation of bilinear constraints (Section [7](#sec:relaxation){reference-type="ref" reference="sec:relaxation"}) {#set-based-convex-relaxation-of-bilinear-constraints-section-secrelaxation .unnumbered}

The main building block of our MICP is a tight and compact convex relaxation for a class of bilinear constraints that emerge naturally in our problem. This relaxation is *set based*, in the sense that it does not rely on the explicit constraints that define the sets in our GCS, but it works directly with their abstract set representations. This makes our MICP usable even when these sets are black boxes accessible only through a separation oracle. This relaxation is similar in spirit to the Lovász-Schrijver one [@lovasz1991cones], and is based on perspective operators (a popular tool in mixed-integer optimization [@ceria1999convex; @stubbs1999branch; @frangioni2006perspective; @gunluk2010perspective]).

### Control applications (Section [8](#sec:optimal_control){reference-type="ref" reference="sec:optimal_control"}) {#control-applications-section-secoptimal_control .unnumbered}

Computation times are the main limitation to a widespread application of mixed-integer optimization in control of hybrid systems [@naik2017embedded; @stellato2018embedded; @marcucci2020warm]. Our shortest-path formulation of these problems is substantially different from the state of the art [@moehle2015perspective; @marcucci2019mixed], as we do not use binary variables to encode the discrete mode in which the system is at each time step but, instead, we use them to select the transitions between modes. This different parameterization yields slightly larger but much stronger MICPs that, in our computational experiments, are orders of magnitude faster to solve.

## Related graph problems {#sec:related_works}

In this subsection we overview a few variants of classical graph problems that are closely related to our problem formulation.

### Graph problems with neighborhoods {#sec:graph_problems_with_neighborhoods .unnumbered}

Graph problems where the vertices are allowed to move within corresponding sets are often called problems with neighborhoods. The SPP with neighborhoods has been analyzed in [@disser2014rectilinear] under stringent assumptions that ensure polynomial-time solvability: the sets are disjoint rectilinear polygons in the plane, and the edge lengths penalize the $\mathcal L_1$ distance between the vertices. The applications we target with this paper, however, do not verify any of these hypotheses. A special case of the SPP with neighborhoods is the touring-polygon problem, which asks for the shortest path between two points that visits a set of polygons in a given order [@dror2003touring]. Our problem differs from this in that our sets are convex and the order in which we visit them is not predefined. Other problems akin to the touring polygon, but substantially different from the SPP in GCS, are the safari, the zookeeper, and the watchman route; see [@li2011euclidean Part IV] and the references therein.

The Traveling-Salesman Problem (TSP) and the Minimum-Spanning-Tree Problem (MSTP) are the two combinatorial problems that have been studied most extensively in their variants with neighborhoods [@arkin1994approximation; @yang2007minimum]. Exact algorithms for these generally rely on expensive mixed-integer nonconvex optimization [@gentilini2013travelling; @blanco2017minimum; @burdick2021multi], and do not scale beyond two or three dimensions. Although the techniques we propose in this paper are particularly well suited to the structure of the SPP, they can be used without modifications to formulate other graph problems with neighborhoods as very tractable MICPs (see Appendix [11](#sec:extensions){reference-type="ref" reference="sec:extensions"}).

### Graph problems with clusters {#graph-problems-with-clusters .unnumbered}

Generalized Steiner problems [@dror2000generalizedsteiner] (otherwise known as generalized network-design problems [@feremans2003generalized; @pop2012generalized]) can be thought as the discrete counterpart of the graph problems with neighborhoods: the vertex set is partitioned into clusters and the problem constraints are expressed in terms of these clusters, rather than the original vertices. A clustered version of the SPP has been presented in [@li1995shortest]: each vertex in the graph is assigned a nonnegative weight, and the total vertex weight incurred by the shortest path within each cluster must not exceed a given value. The problem we analyze in this paper can be approximated as an SPP with clusters in a natural way. In low-dimensional spaces, this approximation can be computationally efficient and sufficiently accurate for practical applications. However, this strategy is infeasible in high dimensions, where covering a volume of space with a cluster requires an exponential number of points.

### Euclidean shortest paths {#euclidean-shortest-paths .unnumbered}

Another related variant of the SPP is the Euclidean SPP [@li2011euclidean], where we look for a continuous path that connects two points and avoids given polygonal obstacles. In two dimensions, this problem can be reduced to a discrete search and is solvable in polynomial time [@lozano1979algorithm]. In three dimensions or more the problem is NP-hard [@canny1987new Theorem 2.3.2], and common algorithms rely on a grid discretization of the space [@kim2003discrete]. More recently, a moment-based technique that handles semialgebraic obstacles has been proposed in [@khadir2020piecewise].

# Problem statement {#sec:statement}

We start with a formal statement of the SPP in GCS. Let $G := (\mathcal V, \mathcal E)$ be a directed graph with vertex set $\mathcal V$ and edge set $\mathcal E$. For each vertex $v \in \mathcal V$, we have a nonempty compact convex set $\mathcal X_v \subset \mathbb R^n$ and a point $\bm x_v$ contained in it.[^3] The length of an edge $e=(u,v) \in \mathcal E$ is determined by the location of the points $\bm x_u$ and $\bm x_v$ via the expression $\ell_e(\bm x_u,\bm x_v)$. The *edge length* function $\ell_e$ takes values in $\mathbb R_{\geq 0} \cup \{\infty\}$ and is assumed to be proper, closed, and convex. Note that, despite its name, we do not assume $\ell_e$ to be a valid metric, and properties like symmetry or the triangle inequality are not required to hold. Given a source vertex $s$ and a target vertex $t  \neq s$, an $s$-$t$ path $p$ is a sequence of distinct vertices $(v_0, \ldots, v_K)$ such that $v_0=s$, $v_K=t$, and $(v_k, v_{k+1})\in \mathcal E$ for all $k=0, \ldots, K-1$. We denote with $\mathcal E_p := \{(v_0, v_1), \ldots, (v_{K-1}, v_K)\}$ the set of edges traversed by this path, and with $\mathcal P$ the set of all $s$-$t$ paths in the graph $G$. The SPP in GCS is then stated as $$\label{eq:spp_in_gcs}
\begin{tcolorbox}[ams align]
\label{eq:spp_objective}
\mathrm{minimize}\quad & \sum_{e = (u,v) \in \mathcal E_p} \ell_e(\bm x_u,\bm x_v) \\
\mathrm{subject \ to}\quad
\label{eq:spp_path}
& p \in \mathcal P, \\
\label{eq:spp_v}
& \bm x_v \in \mathcal X_v, && \forall v \in p.
\end{tcolorbox}\noindent$$ The decision variables are the discrete path $p$ and the continuous values $\bm x_v$. The cost [\[eq:spp_objective\]](#eq:spp_objective){reference-type="eqref" reference="eq:spp_objective"} minimizes the total path length. Constraint [\[eq:spp_v\]](#eq:spp_v){reference-type="eqref" reference="eq:spp_v"} is enforced only for the vertices visited by the path, since the positions of the other vertices are irrelevant.

The edge length used in Figure [1](#fig:toy_example){reference-type="ref" reference="fig:toy_example"} is the Euclidean distance: $$\begin{align}
\label{eq:2norm}
\ell_e (\bm x_u, \bm x_v) := \|\bm x_v - \bm x_u\|_2.
\end{align}$$ With this choice the polygonal line connecting the points $\bm x_v$ along a shortest path is as straight as possible, perfectly straight if $(s,t) \in \mathcal E$. Conversely, if the edge length is the Euclidean distance squared, $$\begin{align}
\label{eq:2norm_squared}
\ell_e (\bm x_u, \bm x_v) := \|\bm x_v - \bm x_u\|_2^2,
\end{align}$$ straight trajectories may be suboptimal if they require long steps $\bm x_v - \bm x_u$. Note also that by letting $\ell_e$ take infinite value outside a convex set $\mathcal X_e$ we are effectively enforcing the edge constraint $(\bm x_u,\bm x_v) \in \mathcal X_e$. This will be used in Section [8](#sec:optimal_control){reference-type="ref" reference="sec:optimal_control"} to formulate optimal-control problems as SPPs in GCS: there the edge constraints will couple the vertex positions according to the system dynamics.

# Complexity analysis {#sec:complexity}

If we fix the vertex positions $\bm x_v$, problem [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"} simplifies to the classical SPP with scalar nonnegative edge lengths, which is easily solvable using, e.g., Linear Programming (LP). Similarly, if we fix the path $p$, problem [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"} simplifies to a convex program that can be efficiently solved for most convex sets $\mathcal X_v$ and edge lengths $\ell_e$. In this section we show that the simultaneous optimization of the vertex positions and the path makes the SPP in GCS an NP-hard problem.

Recall that an $s$-$t$ path $p := (v_0, \ldots, v_K)$ is said to be Hamiltonian if it visits every vertex in the graph (i.e., if $K = |\mathcal V|-1$), and a graph is Hamiltonian if it contains such a path. The Hamiltonian-Path Problem (HPP) asks if a given graph is Hamiltonian. As an example, the graph in Figure [1](#fig:toy_example){reference-type="ref" reference="fig:toy_example"} is not Hamiltonian.

::: theorem
[]{#th:complexity label="th:complexity"} The SPP in GCS [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"} is NP-hard.
:::

::: proof
*Proof.* We show that the HPP is polynomial-time reducible to the SPP in GCS. The thesis will then follow since the HPP is NP-complete [@karp1972reducibility]. We construct an SPP in GCS that shares the same graph $G$ as the given HPP. We let the source $\mathcal X_s := \{0\}$ and target $\mathcal X_t := \{1\}$ sets be singletons on the real line, while we define $\mathcal X_v := [0,1]$ for all $v \neq s, t$. The length of each edge is the Euclidean distance squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}. Given these choices, the optimal positioning of the vertices for a fixed path $p$ is given by $\bm x_{v_k} = k /K$ for $k=0, \ldots, K$. The length of this path is $K (1 / K)^2 = 1 / K$. We conclude that an optimal path is one for which $K$ is maximized, and is Hamiltonian if and only if $G$ is Hamiltonian. This reduction operates in polynomial time. ◻
:::

This simple reduction shows that, even if the convex sets $\mathcal X_v$ are one-dimensional intervals, the SPP in GCS can be a hard problem. Nonetheless, one might wonder if additional assumptions on the problem data could turn the SPP in GCS into a problem that is solvable in polynomial time.

- What if the graph $G$ is acyclic? In case of an acyclic graph the HPP is solvable in linear time [@ahuja1993network Section 4.4], and our hardness proof is not valid.

- What if the sets $\mathcal X_v$ are disjoint? In fact, some graph problems with neighborhoods can be solved more efficiently in case of disjoint neighborhoods [@disser2014rectilinear; @burdick2021multi].

- What if the edge lengths $\ell_e$ are positively homogeneous? An edge length like the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"} could not be used in our reduction since it would not force the optimal path $p$ to visit as many vertices as possible.

It turns out that all these questions have a negative answer. This is summarized in the following theorem, whose proof is omitted since it is a long and relatively straightforward adaptation of the complexity analysis of the Euclidean SPP from [@canny1987new].

::: theorem
[]{#th:complexity2 label="th:complexity2"} Assume that the graph $G$ is acyclic, the sets $\mathcal X_v$ are disjoint, and the edge lengths $\ell_e$ are positively homogeneous. The SPP in GCS [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"} is NP-hard.
:::

# Convex-analysis background {#sec:tools}

This section introduces two basic concepts in convex analysis: perspective operators (homogenization) and valid inequalities (duality). These are the main tools that we will use in the design and the analysis of our MICP. Our goal here is to set the notation and collect some important definitions and properties; for a comprehensive introduction to these topics see [@rockafellar1970convex Parts II and III] or [@hiriart2013convex Chapters III and IV].

## Perspective operators {#sec:perspective}

There is a natural construction that maps a set in $n$ dimensions to a cone in $n+1$ dimensions. This is sometimes called *homogenization*, or the *cone over* the set. Here we call it *perspective*, for coherence with the name commonly used for the same operation applied to functions [@hiriart2013convex Section IV.2.2].

::: definition
[]{#def:perspective_cone label="def:perspective_cone"} We define the *perspective* of a closed convex set $\mathcal X\subseteq \mathbb R^n$ as $$\tilde \mathcal X:= \mathop{\mathrm{cl}}\{(\bm x, \lambda) : \lambda \geq 0, \ \bm x\in \lambda \mathcal X\},$$ where $\mathop{\mathrm{cl}}$ denotes the closure of the set.
:::

::: remark
[]{#rem:bounded_set label="rem:bounded_set"} The closure operation in Definition [\[def:perspective_cone\]](#def:perspective_cone){reference-type="ref" reference="def:perspective_cone"} is unnecessary for bounded sets $\mathcal X$. While, when the set $\mathcal X$ is unbounded, it ensures that the perspective $\tilde \mathcal X$ contains all its limit points with $\lambda = 0$ [@rockafellar1970convex Theorem 8.2].
:::

Importantly, the perspective operation preserves convexity, and the set $\tilde \mathcal X$ is a closed convex cone. The next example shows that the perspective of a set represented in conic form can be computed very easily.

::: example
[]{#ex:perspective_conic label="ex:perspective_conic"} Let $\mathcal X:= \{\bm x: \bm A\bm x+ \bm b\in \mathcal K\}$, for some matrix $\bm A$, vector $\bm b$, and closed convex cone $\mathcal K$. We have $\tilde \mathcal X= \{(\bm x, \lambda) : \lambda \geq 0, \bm A\bm x+ \bm b\lambda \in \mathcal K\}$.
:::

This example has great practical relevance since, informally, it tells us that if a conic-optimization solver can handle the set $\mathcal X$ then it can also handle its perspective $\tilde \mathcal X$. For instance, we see that the perspective of a polyhedral, ellipsoidal, and spectrahedral set can be represented through a set of linear, second-order-cone, and semidefinite constraints, respectively. More in general, if the set $\mathcal X$ is bounded, the formal equivalence of optimizing over $\mathcal X$ and its perspective $\tilde \mathcal X$ can be established using the ellipsoid method [@grotschel2012geometric Chapter 4], since the separation problems for these two sets are easily seen to be equivalent.

The next definition uses the construction from [@rockafellar1970convex Page 39] to describe what the perspective operation does to a convex function.

::: definition
[]{#def:perspective_function label="def:perspective_function"} We define the *perspective* of a closed convex function $f: \mathbb R^n \rightarrow \mathbb R\cup \{\infty\}$ as the unique function $\tilde f$ whose epigraph is the perspective of the epigraph of $f$, i.e., $$\tilde f (\bm x, \lambda) := \inf \{\sigma : (\bm x, \sigma, \lambda) \in \widetilde{\mathop{\mathrm{epi}}f}\},$$ where $\mathop{\mathrm{epi}}f := \{(\bm x, \sigma) : f(\bm x) \leq \sigma\}$.[^4]
:::

Since its epigraph is closed and convex, the perspective function $\tilde f$ is closed and jointly convex in $\bm x$ and $\lambda$.

::: remark
[]{#rem:perspective_values label="rem:perspective_values"} For $\lambda > 0$, noticing that $\lambda \mathop{\mathrm{epi}}f = \{(\bm x, \sigma) : \lambda f(\bm x/ \lambda) \leq \sigma\}$, we have that the perspective function is $\tilde f(\bm x, \lambda) = \lambda f(\bm x/ \lambda)$. For $\lambda < 0$, we immediately see that $\tilde f(\bm x, \lambda) = \infty$. The behavior for $\lambda = 0$ is more complicated [@rockafellar1970convex Corollary 8.5.2], but for the scope of this paper it suffices to note that if $f$ is proper then, by the closedness of $\tilde f$, we must have $\tilde f(\bm 0, 0) = 0$.
:::

Although Definition [\[def:perspective_function\]](#def:perspective_function){reference-type="ref" reference="def:perspective_function"} might seem unsuitable for numerical optimization, the perspectives of most common functions $f$ can be minimized using standard solvers. In fact, given a conic representation of the epigraph of $f$, we can compute the epigraph of $\tilde f$ as in Example [\[ex:perspective_conic\]](#ex:perspective_conic){reference-type="ref" reference="ex:perspective_conic"}, and minimize $\tilde f$ using a slack variable.

The next two examples draw further useful parallels between the perspective operation applied to sets and to functions.

::: example
[]{#ex:perspective_extended_values label="ex:perspective_extended_values"} Let $\mathcal X$ be a nonempty closed convex set and $g$ be a finite convex function. Define $f(\bm x) := g(\bm x)$ if $\bm x\in \mathcal X$ and $f(\bm x) := \infty$ otherwise. We have $\tilde f (\bm x, \lambda) = \tilde g (\bm x, \lambda)$ if $(\bm x, \lambda) \in \tilde \mathcal X$ and $\tilde f (\bm x, \lambda) = \infty$ otherwise.
:::

::: example
[]{#ex:perspective_functional_description label="ex:perspective_functional_description"} For a set $\mathcal X:= \{\bm x: f_i(\bm x) \leq 0 \mathrm{\ for \ all \ }i \in \mathcal I\}$, where the functions $f_i$ are closed and convex, we have $\tilde \mathcal X= \{(\bm x, \lambda) : \tilde f_i (\bm x, \lambda) \leq 0 \mathrm{\ for \ all \ }i \in \mathcal I\}$. Equivalently, using Remark [\[rem:perspective_values\]](#rem:perspective_values){reference-type="ref" reference="rem:perspective_values"}, we have $\tilde \mathcal X= \mathop{\mathrm{cl}}\{(\bm x, \lambda) : \lambda > 0, \lambda f_i (\bm x/ \lambda) \leq 0 \mathrm{\ for \ all \ }i \in \mathcal I\}$.
:::

## Valid inequalities

A second cone that is naturally associated with a convex set is the cone of its valid inequalities. This will play an important role in the analysis of our MICP in Section [7](#sec:relaxation){reference-type="ref" reference="sec:relaxation"}. We report here a formal definition and a useful property.

::: definition
[]{#def:valid_inequalities label="def:valid_inequalities"} We define the *cone of valid inequalities* of a set $\mathcal X\subseteq \mathbb R^n$ as $$\mathcal X^\circ := \{(\bm a, b) : \bm a^\top \bm x+ b \geq 0 \mathrm{\ for \ all \ }\bm x\in \mathcal X\}.$$
:::

The cone $\mathcal X^\circ$ is easily seen to be closed and convex, even when $\mathcal X$ is neither closed nor convex. Note also that the cone of valid inequalities is closely related to the *polar set*, but the latter lives in $n$ dimensions.

The next lemma relates the two operations defined in this section. Recall that the *dual cone* of a closed convex cone $\mathcal K$ is the set $\mathcal K^* := \{\bm a: \bm a^\top \bm x\geq 0 \mathrm{\ for \ all \ }\bm x\in \mathcal K\}$.

::: lemma
[]{#lemma:polar_description label="lemma:polar_description"} Let $\mathcal X$ be a closed convex set. The closed convex cones $\tilde \mathcal X$ and $\mathcal X^\circ$ are dual to each other.
:::

::: proof
*Proof.* The perspective cone $\tilde \mathcal X$ can be equivalently defined as the closure of the cone generated by $\mathcal X\times \{1\}$. By applying [@rockafellar1970convex Corollary 11.7.2] to the latter set, we obtain $\tilde \mathcal X= \{ (\bm x, \lambda) : \bm a^\top \bm x+ b \lambda \geq 0 \mathrm{\ for \ all \ }(\bm a, b) \in \mathcal X^\circ \}$. This shows that $\tilde \mathcal X= (\mathcal X^\circ)^*$. The other direction follows from the bipolar theorem [@rockafellar1970convex Theorem 14.1]. ◻
:::

# Mixed-integer convex formulation {#sec:micp}

We now present the main contribution of this paper: the formulation of the SPP in GCS [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"} as a strong and lightweight MICP. This program is designed in two steps. First, in Section [5.2](#sec:bilinear){reference-type="ref" reference="sec:bilinear"}, we extend the network-flow formulation of the classical SPP (recalled in Section [5.1](#sec:network_flow){reference-type="ref" reference="sec:network_flow"}) to our setting. This yields an optimization problem with bilinear equality constraints. Second, in Section [5.3](#sec:convexification_bilinearities){reference-type="ref" reference="sec:convexification_bilinearities"}, we construct a convex relaxation tailored to these bilinear constraints and we formulate our MICP. The relaxation technique used in this section will be described at a higher level of generality and thoroughly analyzed in Section [7](#sec:relaxation){reference-type="ref" reference="sec:relaxation"}.

## Network-flow formulation of the SPP {#sec:network_flow}

The starting point for the design of our MICP is the network-flow formulation of the SPP with scalar nonnegative edge lengths (see, e.g., [@ahuja1993network Section 4.1]): $$\label{eq:network_flow}
\begin{align}
\label{eq:network_flow_objective}
\mathrm{minimize}
\quad & \sum_{e \in \mathcal E} l_e y_e \\
\mathrm{subject \ to}\quad
\label{eq:network_st}
& \sum_{e \in \mathcal E_s^\mathrm{out}} y_e =1, \ \sum_{e \in \mathcal E_t^\mathrm{in}} y_e = 1, \\
\label{eq:network_v}
& \sum_{e \in \mathcal E_v^\mathrm{in}} y_e  = \sum_{e \in \mathcal E_v^\mathrm{out}} y_e, \ \sum_{e \in \mathcal E_v^\mathrm{out}} y_e \leq 1, && \forall v \in \mathcal V- \{s,t\}, \\
\label{eq:network_flow_nonnegativity}
& y_e \geq 0, && \forall e \in \mathcal E.
\end{align}$$ In this LP the decision variables $y_e$ parameterize a path $p$, with $y_e = 1$ if the edge $e$ is traversed by $p$ and $y_e = 0$ otherwise. The scalar $l_e \geq 0$ represents the length of the edge $e$. The sets $\mathcal E_v^\mathrm{in}:= \{(u,v) \in \mathcal E\}$ and $\mathcal E_v^\mathrm{out}:= \{(v,u) \in \mathcal E\}$ collect the edges incoming and outgoing vertex $v$. Without loss of generality, we assume $|\mathcal E_s^\mathrm{in}| = |\mathcal E_t^\mathrm{out}| = 0$, i.e., the source and the target have no incoming and outgoing edges, respectively. Interpreting the value of $y_e$ as the *flow* carried by the edge $e$, constraint [\[eq:network_st\]](#eq:network_st){reference-type="eqref" reference="eq:network_st"} asks that one unit of flow is injected in the source and ejected from the target. For all the other vertices, constraint [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"} enforces the *flow conservation* and a *degree constraint*. The latter enforces a limit of one to the total flow traversing the vertex.

::: remark
[]{#rem:integrality label="rem:integrality"} Note that we do not explicitly require the flows $y_e$ to be binary, but we only enforce their nonnegativity in [\[eq:network_flow_nonnegativity\]](#eq:network_flow_nonnegativity){reference-type="eqref" reference="eq:network_flow_nonnegativity"}. This is because all the basic feasible solutions of the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"} can be shown to have binary value (see, e.g., [@ahuja1993network Section 11.12]), and the constraints $y_e \in \{0,1\}$ would not affect the optimal value of this program.
:::

::: remark
[]{#rem:degree label="rem:degree"} Since we assumed the edge lengths $l_e$ to be nonnegative, the degree constraint in [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"} is actually redundant for the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"}, as well as for problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} below. However, as we will see in Section [5.4](#sec:degree_constraints){reference-type="ref" reference="sec:degree_constraints"}, this constraint is not redundant for our final MICP. Therefore we include it in our formulation from the start.
:::

## Biconvex formulation {#sec:bilinear}

As an intermediate step towards our MICP, we formulate the SPP in GCS as a *biconvex* optimization problem. Specifically, a nonlinear program whose nonconvexity comes only from products between the vertex locations and the flow variables parameterizing a path. Note that this is consistent with the observation from Section [3](#sec:complexity){reference-type="ref" reference="sec:complexity"} that the SPP in GCS simplifies to a convex program if we fix either the vertex locations or the path through the graph.

A natural attempt to extend the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"} to the SPP in GCS is to proceed as done for other graph problems with neighborhoods [@gentilini2013travelling; @blanco2017minimum; @burdick2021multi]: include the vertex locations $\bm x_v$ among our decision variables, enforce the constraint $\bm x_v \in \mathcal X_v$ for all $v \in \mathcal V$, and substitute the addends in the cost [\[eq:network_flow_objective\]](#eq:network_flow_objective){reference-type="eqref" reference="eq:network_flow_objective"} with $\ell_e(\bm x_u, \bm x_v) y_e$. However, one immediate issue with this approach is that the latter product is undefined if $\ell_e(\bm x_u, \bm x_v) = \infty$ and $y_e = 0$, while we would like the cost contribution of the edge $e$ to always be zero if $y_e = 0$. Perspective functions give us a convenient and rigorous way to "turn on and off" the length of an edge using the corresponding flow variable.

Let us introduce two auxiliary variables $\bm z_e := y_e \bm x_u$ and $\bm z_e' := y_e \bm x_v$ per edge $e = (u,v)$, and consider the perspective function $\tilde \ell_e(\bm z_e, \bm z_e', y_e)$.[^5] When the flow $y_e$ is positive, this function coincides with the product above: $$\tilde \ell_e(\bm z_e, \bm z_e', y_e)
= \ell_e (\bm z_e/y_e, \bm z_e'/y_e) y_e
= \ell_e (y_e \bm x_u/y_e, y_e \bm x_v/y_e) y_e
= \ell_e(\bm x_u, \bm x_v) y_e,$$ where the first equality comes from Remark [\[rem:perspective_values\]](#rem:perspective_values){reference-type="ref" reference="rem:perspective_values"}. When the flow $y_e$ is zero, the function $\tilde \ell_e$ is well defined and correctly evaluates to zero, even when $\ell_e(\bm x_u, \bm x_v) = \infty$. In fact, $y_e = 0$ implies $\bm z_e = \bm z_e' = \bm 0$, and $\tilde \ell_e(\bm 0,\bm 0,0) = 0$ as discussed in Remark [\[rem:perspective_values\]](#rem:perspective_values){reference-type="ref" reference="rem:perspective_values"}.

Overall, we then have the following biconvex formulation of the SPP in GCS: $$\label{eq:bilinear_spp}
\begin{tcolorbox}[ams align]
\label{eq:bilinear_objective}
\mathrm{minimize}
\quad & \sum_{e \in \mathcal E} \tilde \ell_e(\bm z_e, \bm z_e', y_e) \\
\mathrm{subject \ to}\quad
\label{eq:bilinear_flow}
& \text{constraints of problem~\eqref{eq:network_flow}}, \\
\label{eq:bilinear_Xv}
& \bm x_v \in \mathcal X_v, && \forall v \in \mathcal V, \\
\label{eq:bilinear_yz}
& \bm z_e = y_e \bm x_u, \ \bm z_e'= y_e \bm x_v, && \forall e = (u,v) \in \mathcal E.
\end{tcolorbox}\noindent$$ The decision variables are the flows $y_e$, the vertex positions $\bm x_v$, and the auxiliary variables $\bm z_e$ and $\bm z_e'$. The role of the latter is to match the vertices $\bm x_u$ and $\bm x_v$ when $y_e = 1$, and collapse to zero when $y_e = 0$. This behavior is driven by the bilinear equality constraints [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"}, which are the only nonconvexity in our formulation and whose convexification is the focus of the next subsection. Before that, let us formally verify that, as mentioned in Remark [\[rem:integrality\]](#rem:integrality){reference-type="ref" reference="rem:integrality"} for the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"}, forcing the flows $y_e$ to be binary does not affect the optimal value of the biconvex program [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}.

::: proposition
[]{#prop:integrality label="prop:integrality"} For any local minimum $L \in \mathbb R_{\geq 0}$ of problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}, there exists a feasible point of [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} with cost equal to $L$ and such that $y_e \in \{0,1\}$ for all $e \in \mathcal E$.
:::

::: proof
*Proof.* Given a local minimizer of [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} with cost $L$, we fix the vertex positions $\bm x_v$. This reduces problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} to an LP of the form [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"}. The optimal value of this LP must be $L$, otherwise we would have found a descent direction and our solution of [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} would not be locally optimal. Furthermore, because of Remark [\[rem:integrality\]](#rem:integrality){reference-type="ref" reference="rem:integrality"}, we can assume that the optimal flows of this LP are binary. Paired with the previously fixed variables $\bm x_v$, these binary flows yield a feasible solution of [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} with cost $L$. ◻
:::

## Convex relaxation of the bilinear constraints {#sec:convexification_bilinearities}

The biconvex program [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} is our first formulation of the SPP in GCS that can be tackled numerically. However, the bilinear constraints [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"} make this optimization problem challenging to solve, even just locally. In this subsection we show how to reformulate problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} as a lightweight and strong MICP, that can be reliably solved to global optimality using branch-and-bound algorithms.

The next lemma allows us to construct a tight envelope around the constraints of the biconvex program [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} through a small number of perspective cones. In its statement we let $\mathcal E_v := \mathcal E_v^\mathrm{in}\cup \mathcal E_v^\mathrm{out}$ denote the set of edges incident with vertex $v \in \mathcal V$. Recall also that a valid constraint for an optimization problem is a constraint that is verified by all the feasible points.

::: lemma
[]{#lemma:valid_constraint label="lemma:valid_constraint"} For some vertex $v \in \mathcal V$, assume that the linear inequality $$\begin{align}
\label{eq:valid_inequality}
\sum_{e \in \mathcal E_v} c_e y_e + d \geq 0
\end{align}$$ is valid for problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}. Partitioning the summation over $\mathcal E_v$ in incoming and outgoing edges, we have that the following convex constraint is also valid for [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}: $$\begin{align}
\label{eq:implied_constraint}
\left(\sum_{e \in \mathcal E_v^\mathrm{in}} c_e \bm z_e' + \sum_{e \in \mathcal E_v^\mathrm{out}} c_e \bm z_e + d \bm x_v, \ \sum_{e \in \mathcal E_v} c_e y_e + d \right)
\in \tilde \mathcal X_v.
\end{align}$$
:::

::: proof
*Proof.* Constraint [\[eq:implied_constraint\]](#eq:implied_constraint){reference-type="eqref" reference="eq:implied_constraint"} requires two conditions to hold. One is [\[eq:valid_inequality\]](#eq:valid_inequality){reference-type="eqref" reference="eq:valid_inequality"}, which is assumed. The other is verified by multiplying both sides of $\bm x_v \in \mathcal X_v$ from [\[eq:bilinear_Xv\]](#eq:bilinear_Xv){reference-type="eqref" reference="eq:bilinear_Xv"} by the left-hand side of [\[eq:valid_inequality\]](#eq:valid_inequality){reference-type="eqref" reference="eq:valid_inequality"}, and then using the bilinear constraints [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"}. ◻
:::

::: remark
[]{#rem:valid_equality label="rem:valid_equality"} If the valid constraint [\[eq:valid_inequality\]](#eq:valid_inequality){reference-type="eqref" reference="eq:valid_inequality"} holds with equality, Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"} simply amounts to multiplying this equality by $\bm x_v$, and it gives us a valid linear equality of the form $\sum_{e \in \mathcal E_v^\mathrm{in}} c_e \bm z_e' + \sum_{e \in \mathcal E_v^\mathrm{out}} c_e \bm z_e + d \bm x_v = \bm 0$.
:::

::: remark
[]{#rem:rlt label="rem:rlt"} Generating new valid constraints by multiplying existing ones is a standard procedure at the core of many relaxation techniques [@mccormick1976computability; @sherali1990hierarchy; @lovasz1991cones; @lasserre2001global; @parrilo2003semidefinite]. Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"} will be analyzed at a higher level of generality in Section [7](#sec:relaxation){reference-type="ref" reference="sec:relaxation"}, where its similarities with existing methods will be clearly drawn.
:::

Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"} lifts any valid linear constraint on the flows incident with vertex $v$ into a convex constraint that envelops the feasible set of problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}. Our MICP is obtained by applying this lemma to each flow constraint in the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"}, and by replacing the constraints of the biconvex program [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} with the envelope resulting from this process. Let us first state our MICP and then prove its equivalence to the SPP in GCS (Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"} below): $$\label{eq:micp}
\begin{tcolorbox}[ams align]
\label{eq:micp_objective}
\mathrm{minimize}
\quad & \sum_{e \in \mathcal E} \tilde \ell_e(\bm z_e, \bm z_e', y_e) \\
\mathrm{subject \ to}\quad
\label{eq:micp_st}
& \sum_{e \in \mathcal E_s^\mathrm{out}} y_e =1, \ \sum_{e \in \mathcal E_t^\mathrm{in}} y_e = 1, \\
\label{eq:micp_degree}
& \sum_{e \in \mathcal E_v^\mathrm{out}} y_e \leq 1, && \forall v \in \mathcal V- \{s,t\}, \\
\label{eq:micp_conservation}
& \sum_{e \in \mathcal E_v^\mathrm{in}} (\bm z_e', y_e) = \sum_{e \in \mathcal E_v^\mathrm{out}} (\bm z_e, y_e), && \forall v \in \mathcal V- \{s,t\}, \\
\label{eq:micp_nonnegativity}
& (\bm z_e, y_e) \in \tilde \mathcal X_u, \  (\bm z_e', y_e)  \in \tilde \mathcal X_v, && \forall e = (u,v) \in \mathcal E,\\
\label{eq:micp_integrality}
& y_e \in \{0,1\}, && \forall e \in \mathcal E.
\end{tcolorbox}$$ Constraint [\[eq:micp_conservation\]](#eq:micp_conservation){reference-type="eqref" reference="eq:micp_conservation"} is obtained as in Remark [\[rem:valid_equality\]](#rem:valid_equality){reference-type="ref" reference="rem:valid_equality"} from the flow conservation in [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"}, and [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"} is the result of applying Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"} to the nonnegativity constraint [\[eq:network_flow_nonnegativity\]](#eq:network_flow_nonnegativity){reference-type="eqref" reference="eq:network_flow_nonnegativity"}. Note that the application of the same technique to the equalities [\[eq:micp_st\]](#eq:micp_st){reference-type="eqref" reference="eq:micp_st"} and to the degree constraint in [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"} would give us $$\label{eq:reconstruct}
\begin{align}
\label{eq:reconstruct_st}
& \bm x_s = \sum_{e \in \mathcal E_s^\mathrm{out}} \bm z_e, \
\bm x_t = \sum_{e \in \mathcal E_t^\mathrm{in}} \bm z_e', \\
\label{eq:reconstruct_v}
& \bm x_v - \sum_{e \in \mathcal E_v^\mathrm{out}} \bm z_e \in \left(1 -\sum_{e \in \mathcal E_v^\mathrm{out}} y_e \right) \mathcal X_v, && \forall v \in \mathcal V- \{s,t\}.
\end{align}$$ However these constraints would be redundant since the vertex positions $\bm x_v$ for $v \in \mathcal V$ do not appear in the rest of problem [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"}. Note also that the combination of [\[eq:reconstruct\]](#eq:reconstruct){reference-type="eqref" reference="eq:reconstruct"} and [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"} implies the constraints $\bm x_v \in \mathcal X_v$ for all $v \in \mathcal V$, which would also be redundant for our MICP. The convex relaxation of [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} is obtained simply by dropping the integrality constraint [\[eq:micp_integrality\]](#eq:micp_integrality){reference-type="eqref" reference="eq:micp_integrality"} (the nonnegativity of the flows $y_e$ is imposed by the cost and also by [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"}). Observe that, unlike the biconvex program [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}, the optimal value of the MICP can decrease if the flows are allowed to be fractional.

::: theorem
[]{#th:validity_micp label="th:validity_micp"} The MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} has optimal value equal to the SPP in GCS [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"}. An optimal path $p$ for problem [\[eq:spp_in_gcs\]](#eq:spp_in_gcs){reference-type="eqref" reference="eq:spp_in_gcs"} is recovered from the solution of [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} through the relation $\mathcal E_p := \{e \in \mathcal E: y_e = 1\}$. An optimal positioning of the vertices is reconstructed for the source and the target as in [\[eq:reconstruct_st\]](#eq:reconstruct_st){reference-type="eqref" reference="eq:reconstruct_st"}, and for all the other vertices by letting $\bm x_v$ be any point such that [\[eq:reconstruct_v\]](#eq:reconstruct_v){reference-type="eqref" reference="eq:reconstruct_v"} holds.
:::

In Section [7.3](#sec:conic){reference-type="ref" reference="sec:conic"} we will see that this theorem follows from a simple geometric property of Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"}. Here we give a direct proof that explicitly illustrates the logic behind our formulation.

::: proof
*Proof.* The only flows that can satisfy the constraints in [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} are such that the set $\mathcal E_p$ defined above describes the vertex-disjoint union of an $s$-$t$ path and cycles. However, the presence of cycles can be excluded since the edge lengths $\ell_e$ are nonnegative, and traversing a cycle that is disjoint from the main path cannot decrease the cost. Therefore, at optimality, $\mathcal E_p$ identifies a path $p$. For all the edges $e \notin \mathcal E_p$, constraint [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"} simplifies to $\bm z_e = \bm z_e' = \bm 0$, and the corresponding cost addends give $\tilde \ell_e(\bm 0, \bm 0, 0) = 0$. For the vertices $v \notin p$, constraint [\[eq:micp_conservation\]](#eq:micp_conservation){reference-type="eqref" reference="eq:micp_conservation"} is trivially satisfied and [\[eq:reconstruct_v\]](#eq:reconstruct_v){reference-type="eqref" reference="eq:reconstruct_v"} reads $\bm x_v \in \mathcal X_v$. For an edge $e =(u,v)$ along the path $p$, constraint [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"} becomes $\bm z_e \in \mathcal X_u$ and $\bm z_e' \in \mathcal X_v$, and the cost addend is $\tilde \ell_e(\bm z_e, \bm z_e', 1) = \ell_e(\bm z_e, \bm z_e')$. Denoting with $f=(v,w) \in \mathcal E_p$ the edge after $e$ in the path, the flow conservation [\[eq:micp_conservation\]](#eq:micp_conservation){reference-type="eqref" reference="eq:micp_conservation"} reads $\bm z_e' = \bm z_f$. Finally, the conditions in [\[eq:reconstruct\]](#eq:reconstruct){reference-type="eqref" reference="eq:reconstruct"} give us $\bm x_u = \bm z_e$ and $\bm x_v = \bm z_e'$ for all edges $e =(u,v) \in \mathcal E_p$. ◻
:::

::: remark
[]{#rem:singletons label="rem:singletons"} If the sets $\mathcal X_v$ are singletons, the SPP in GCS simplifies to the SPP with nonnegative edge lengths. In this case our MICP reduces to the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"} and its convex relaxation is exact, as discussed in Remark [\[rem:integrality\]](#rem:integrality){reference-type="ref" reference="rem:integrality"}.
:::

::: remark
[]{#rem:set_based label="rem:set_based"} For the edge lengths $\ell_e$ and convex sets $\mathcal X_v$ that typically appear in practice, the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} can be solved to global optimality with standard solvers (see the discussion in Section [4.1](#sec:perspective){reference-type="ref" reference="sec:perspective"}). However, problem [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} can be tackled numerically even when the sets in our GCS are not defined by explicit constraints (e.g., convex inequalities). For example, each set $\mathcal X_v$ may be very complex and accessible only through an oracle that, given a point $\bm x_v$, either certifies that $\bm x_v \in \mathcal X_v$ or returns a separating hyperplane. In fact, such an oracle is easily adapted to checking membership to the perspective cones in [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"}, and this black-box access to the problem constraints is sufficient for efficient optimization algorithms like the ellipsoid method [@grotschel2012geometric].
:::

## Degree constraints {#sec:degree_constraints}

In Remark [\[rem:degree\]](#rem:degree){reference-type="ref" reference="rem:degree"} we anticipated that, although redundant for the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"}, the degree constraints [\[eq:micp_degree\]](#eq:micp_degree){reference-type="eqref" reference="eq:micp_degree"} play an important role in our MICP. This is illustrated in the next example, which shows how the optimal flows from [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} can induce cycles if the degree constraints are not enforced.

::: example
Consider a graph with vertices $\mathcal V:= \{s,1,2,t\}$ and edges $\mathcal E:= \{(s,1),(1,2),(2,1),(1,t)\}$. Define the sets $\mathcal X_s := \{-1\}$, $\mathcal X_1 := [-1,1]$, $\mathcal X_2 := \{0\}$, and $\mathcal X_t := \{1\}$. Let the length of each edge be the Euclidean distance squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}. The optimal value of this SPP in GCS is $2$ and the optimal path is $p=(s, 1, t)$. However, if we do not enforce the degree constraints [\[eq:micp_degree\]](#eq:micp_degree){reference-type="eqref" reference="eq:micp_degree"}, our MICP has optimal value equal to $1$ and its optimal flows are $y_e =1$ for all $e \in \mathcal E$, i.e., they induce the cycle $(1,2,1)$.
:::

In case of an acyclic graph $G$, the issues just described do not arise and the degree constraints are redundant for our MICP and its convex relaxation. Nonetheless, we still include them in our formulation since they are computationally light and their explicit presence can trigger the use of specialized generalized-upper-bound branching rules in the solver [@conforti2014integer Section 9.2].

# Alternative formulations {#sec:alternative_formulations}

Multiple alternative MICP formulations of the SPP in GCS can be designed and finding the most effective one is a tradeoff between the size of the program and the tightness of its convex relaxation. The MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} is very compact: it has only $O(|\mathcal E|)$ binary variables, $O(n|\mathcal E|)$ continuous variables, and $O(n(|\mathcal V| + |\mathcal E|))$ constraints (assuming that the cones in [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"} are described by $O(n)$ constraints). In addition, in the experiments in Section [9](#sec:examples){reference-type="ref" reference="sec:examples"}, we will see that the relaxation of our MICP is typically very tight (although a carefully designed instance in Section [9.4](#sec:example_failures){reference-type="ref" reference="sec:example_failures"} shows that our relaxation can, in principle, be arbitrarily loose).

A simple alternative way to reformulate the biconvex problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} as an MICP is to enforce the integrality constraints $y_e \in \{0,1\}$ for all $e \in \mathcal E$, and relax each bilinear constraint [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"} independently using a McCormick envelope [@mccormick1976computability]. With our notation, this amounts to replacing [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"} with $$\begin{align}
\label{eq:mc_relaxation}
(\bm z_e, y_e) \in \tilde \mathcal B_u, \
(\bm z_e', y_e) \in \tilde \mathcal B_v, \
(\bm x_u - \bm z_e, 1- y_e) \in \tilde \mathcal B_u, \
(\bm x_v - \bm z_e', 1- y_e) \in \tilde \mathcal B_v,
\end{align}$$ where, for each $v \in \mathcal V$, we let $\mathcal B_v$ be an axis-aligned box that contains $\mathcal X_v$. Especially if the convex sets $\mathcal X_v$ are defined by many constraints, this MICP is more compact than ours. However, as we will see in Section [9](#sec:examples){reference-type="ref" reference="sec:examples"}, this formulation has loose convex relaxation and its solution times are generally much larger than with our approach.

At the other end of the spectrum, a variety of stronger but potentially more expensive formulations could be devised. For example, we have found that subtour-elimination constraints like [@taccari2016integer Section 2.2] can tighten the relaxation of our MICP for some classes of problems. Alternatively, we could formulate our MICP by grouping the constraints in [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} vertex by vertex, and by computing the convex hull of each group (see Section [7.2](#sec:tightness_relaxation){reference-type="ref" reference="sec:tightness_relaxation"} below). We could also use more expensive semidefinite relaxations [@lovasz1991cones; @lasserre2001global; @parrilo2003semidefinite] of the bilinear constraints [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"}. In our computational experience, the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} represents the best compromise between a lightweight and a strong formulation, and its solution times are lower than any other formulation we have tested.

# Analysis of the mixed-integer formulation {#sec:relaxation}

In this section we describe and analyze at a more abstract level the method used in Section [5.3](#sec:convexification_bilinearities){reference-type="ref" reference="sec:convexification_bilinearities"} to formulate the SPP in GSC as an MICP. We show that Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"} can be used to design convex relaxations of a large class of bilinear constraints, and we connect this result to existing relaxation techniques for nonconvex optimization. Finally, we give a simpler geometric proof of the validity of our MICP (already shown in Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"}).

## Set-based relaxation of bilinear constraints {#sec:set_based_relaxation}

Our first step in this analysis is to show that Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"} is, in fact, a general-purpose relaxation technique for nonconvex sets of the form $$\begin{align}
\label{eq:bilinear_set}
\mathcal S:= \{(\bm x, \bm y, \bm Z) : \bm x\in \mathcal X, \ \bm y\in \mathcal Y, \ \bm Z= \bm x\bm y^\top\},
\end{align}$$ where $\mathcal X\subseteq \mathbb R^n$ and $\mathcal Y\subseteq \mathbb R^m$ are closed convex sets. In particular, here $\mathcal X$ takes the place of a generic set $\mathcal X_v$ in our GCS, while $\mathcal Y$ plays the role of the linear constraints on the flow variables incident with vertex $v$ (see Remark [\[rem:coincise_bilinear\]](#rem:coincise_bilinear){reference-type="ref" reference="rem:coincise_bilinear"} below for more details).

A natural approach to construct a convex envelope around the set $\mathcal S$ is to multiply all the valid inequalities $\bm a^\top \bm x+ b \geq 0$ for the set $\mathcal X$ by all the valid inequalities $\bm c^\top \bm y+ d \geq 0$ for the set $\mathcal Y$, and then use the bilinear equality $\bm Z= \bm x\bm y^\top$ to linearize these products. This gives us an infinite family of valid linear inequalities for $\mathcal S$, which form our convex relaxation: $$\begin{multline}
\label{eq:relaxation}
\mathcal S\subseteq \mathcal S' := \{(\bm x, \bm y, \bm Z) : \bm a^\top \bm Z\bm c+ d \bm a^\top \bm x+ b \bm c^\top \bm y+ b d \geq 0 \\
\mathrm{\ for \ all \ }(\bm a, b) \in \mathcal X^\circ \mathrm{\ and \ }(\bm c, d) \in \mathcal Y^\circ\}.
\end{multline}$$ Note that the conditions $\bm x\in \mathcal X$ and $\bm y\in \mathcal Y$ are implied by the inequalities in [\[eq:relaxation\]](#eq:relaxation){reference-type="eqref" reference="eq:relaxation"} that correspond to $(\bm 0, 1) \in \mathcal Y^\circ$ and $(\bm 0, 1) \in \mathcal X^\circ$, respectively.

The relaxation [\[eq:relaxation\]](#eq:relaxation){reference-type="eqref" reference="eq:relaxation"} is not obviously implementable on a computer, since it involves an infinite number of constraints. However, if one of the two sets is a polytope (i.e., a bounded polyhedron) then the convex set $\mathcal S'$ can be efficiently described by a finite number of perspective-cone constraints.

::: proposition
[]{#prop:relaxation_polytopic label="prop:relaxation_polytopic"} Let $\mathcal Y$ be a polytope with halfspace representation $\{ \bm y: \bm c_i^\top \bm y+ d_i \geq 0 \mathrm{\ for \ all \ }i \in \mathcal I\}$. We have $$\begin{align}
\label{eq:relaxation_polytopic}
\mathcal S' =
\{ (\bm x, \bm y, \bm Z) :
(\bm Z\bm c_i  + d_i\bm x, \ \bm c_i^\top \bm y+ d_i)
\in \tilde \mathcal X\mathrm{\ for \ all \ }i \in \mathcal I
\}.
\end{align}$$
:::

::: proof
*Proof.* To recover [\[eq:relaxation\]](#eq:relaxation){reference-type="eqref" reference="eq:relaxation"} from [\[eq:relaxation_polytopic\]](#eq:relaxation_polytopic){reference-type="eqref" reference="eq:relaxation_polytopic"} we first use Lemma [\[lemma:polar_description\]](#lemma:polar_description){reference-type="ref" reference="lemma:polar_description"} to rewrite the membership to $\tilde \mathcal X$ as $\bm a^\top (\bm Z\bm c_i  + d_i \bm x) + b (\bm c_i^\top \bm y+ d_i) \geq 0$ for all $(\bm a, b) \in \mathcal X^\circ$. Then we notice that listing only the valid inequalities $(\bm c_i, d_i)$ for $i \in \mathcal I$ is equivalent to listing all the valid inequalities $(\bm c, d) \in \mathcal Y^\circ$. In fact, since $\mathcal Y$ is bounded, any vector $(\bm c, d) \in \mathcal Y^\circ$ can be expressed as $\sum_{i \in \mathcal I} \alpha_i (\bm c_i, d_i)$ for some nonnegative coefficients $\alpha_i$. Using these coefficients, the inequality $\bm a^\top \bm Z\bm c+ d \bm a^\top \bm x+ b \bm c^\top \bm y+ b d \geq 0$ is seen to be implied by the inequalities generated by $(\bm c_i, d_i)$ for $i \in \mathcal I$. ◻
:::

We then have two descriptions of the relaxation $\mathcal S'$: the symmetric one [\[eq:relaxation\]](#eq:relaxation){reference-type="eqref" reference="eq:relaxation"} that clearly exposes the logic behind the technique, and the asymmetric one [\[eq:relaxation_polytopic\]](#eq:relaxation_polytopic){reference-type="eqref" reference="eq:relaxation_polytopic"} that is computationally efficient, provided that one of the two sets is polytopic and has a small number of facets. The asymmetric relaxation generalizes Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"}, with $\bm c_i^\top \bm y+ d_i \geq 0$ taking the place of the flow inequality [\[eq:valid_inequality\]](#eq:valid_inequality){reference-type="eqref" reference="eq:valid_inequality"}. The asymmetric relaxation is also set based, in the sense that it does not rely on the explicit constraints defining $\mathcal X$, but it works directly with its abstract set representation. Besides making the analysis very concise, this has also the practical advantages discussed in Remark [\[rem:set_based\]](#rem:set_based){reference-type="ref" reference="rem:set_based"}.

::: remark
[]{#rem:coincise_bilinear label="rem:coincise_bilinear"} The constraints of the biconvex program [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} can be restated in terms of the set $\mathcal S$ as follows. First, we collect in the vector $\bm y_v := (y_e)_{e \in \mathcal E_v}$ the flows incident with vertex $v$. Second, we let $\mathcal Y_v$ be the polytope defined by the linear constraints acting on $\bm y_v$. Constraint [\[eq:network_st\]](#eq:network_st){reference-type="eqref" reference="eq:network_st"} and the flow nonnegativity [\[eq:network_flow_nonnegativity\]](#eq:network_flow_nonnegativity){reference-type="eqref" reference="eq:network_flow_nonnegativity"} make $\mathcal Y_s$ and $\mathcal Y_t$ unit simplices (recall that $|\mathcal E_s^\mathrm{in}| = |\mathcal E_t^\mathrm{out}| = 0$). For $v \neq s,t$, the polytope $\mathcal Y_v$ is defined by the flow nonnegativity [\[eq:network_flow_nonnegativity\]](#eq:network_flow_nonnegativity){reference-type="eqref" reference="eq:network_flow_nonnegativity"} together with the conservation and degree constraints in [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"}. Third, we stack in the columns of the matrix $\bm Z_v$ the auxiliary variables $\bm z_e'$ for $e \in \mathcal E_v^\mathrm{in}$ and $\bm z_e$ for $e \in \mathcal E_v^\mathrm{out}$, so that the bilinear constraints [\[eq:bilinear_yz\]](#eq:bilinear_yz){reference-type="eqref" reference="eq:bilinear_yz"} take the form $\bm Z_v = \bm x_v \bm y_v^\top$. By defining the sets $\mathcal S_v$ as in [\[eq:bilinear_set\]](#eq:bilinear_set){reference-type="eqref" reference="eq:bilinear_set"}, the constraints of problem [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"} become $(\bm x_v, \bm y_v, \bm Z_v) \in \mathcal S_v$ for all $v \in \mathcal V$. Our relaxation of the SPP in GCS is then obtained by replacing the constraint sets $\mathcal S_v$ with $\mathcal S_v'$ defined as in [\[eq:relaxation_polytopic\]](#eq:relaxation_polytopic){reference-type="eqref" reference="eq:relaxation_polytopic"}.
:::

## Tightness of the relaxation $\mathcal S'$ {#sec:tightness_relaxation}

Ideally, we would like our relaxation to be as tight as possible, and the set $\mathcal S'$ to coincide with the convex hull of $\mathcal S$. This equality holds, for example, when $\mathcal X$ and $\mathcal Y$ are intervals on the real line, in which case $\mathcal S'$ simplifies to the McCormick envelope [@mccormick1976computability]. However, the inclusion $\mathop{\mathrm{conv}}\mathcal S\subset \mathcal S'$ can be strict in general. In fact, for polytopic sets $\mathcal X$ and $\mathcal Y$, our approach of multiplying valid inequalities simplifies to the first level of the Reformulation-Linearization Technique (RLT) [@sherali1990hierarchy], which does not yield the convex hull of $\mathcal S$ if, e.g., $\mathcal X:= \mathcal Y:= [0,1]^2$.

The convex hull of $\mathcal S$ can be efficiently described when $\mathcal Y$ is a polytope with a small number of extreme points $\{\hat \bm y_j\}_{j \in \mathcal J}$. Specifically, by using disjunctive-programming techniques [@ceria1999convex], it can be verified that $$\begin{align}
\label{eq:ch}
\mathop{\mathrm{conv}}\mathcal S= \left\{
\sum_{j \in \mathcal J} (\bm x_j, \lambda_j \hat \bm y_j, \bm x_j \hat \bm y_j^\top) :
\sum_{j \in \mathcal J} \lambda_j = 1, \
(\bm x_j, \lambda_j) \in \tilde \mathcal X\mathrm{\ for \ all \ }j \in \mathcal J
\right\}.
\end{align}$$ Note that this (lifted) description is convex and also set based. While our relaxation $\mathcal S'$ has size proportional to the number $|\mathcal I|$ of facets of $\mathcal Y$, this description of the convex hull has size proportional to the number $|\mathcal J|$ of extreme points of $\mathcal Y$. For the SPP in GCS, the polytopes $\mathcal Y_v$ have $O(|\mathcal E_v^\mathrm{in}| + |\mathcal E_v^\mathrm{out}|)$ facets and only $O(|\mathcal E_v^\mathrm{in}| |\mathcal E_v^\mathrm{out}|)$ extreme points, and this difference can be relatively small if the graph is sparse. However, in our experience the MICPs obtained with our method provide a better tradeoff between strength and size, and are typically much faster to solve.

::: remark
That our relaxation $\mathcal S'$ is not always the convex hull of $\mathcal S$ should be fully expected. In fact, for $\mathcal X:= [0,1]^n$ and $\mathcal Y:= [0,1]^m$, the bilinear program $$\begin{align}
\label{eq:bilinear_optimization}
\mathrm{minimize}\quad \bm p^\top \bm x+ \bm q^\top \bm y+ \bm x^\top \bm R\bm y
\quad \mathrm{subject \ to}\quad \bm x\in \mathcal X, \ \bm y\in \mathcal Y,
\end{align}$$ is NP-hard [@punnen2015bipartite], and equivalent to minimizing a linear function over $\mathcal S$. The equality $\mathcal S' = \mathop{\mathrm{conv}}\mathcal S$ would then allow us to solve an NP-hard problem in polynomial time.
:::

## Geometric proof of Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"} {#sec:conic}

In the proof of Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"} we have shown the correctness of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} by analyzing all the feasible values that the variables in this program can take. We now present a simple property of the relaxation $\mathcal S'$ that will lead to a geometric and more concise proof of Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"}. This result will also generalize a known property of RLT.

::: lemma
[]{#lemma:extreme label="lemma:extreme"} Let $\mathcal Y$ be a polytope and $\hat \bm y$ one of its extreme points. We have $(\bm x, \hat \bm y, \bm Z) \in \mathcal S$ if and only if $(\bm x, \hat \bm y, \bm Z) \in \mathcal S'$.
:::

::: proof
*Proof.* One direction follows from $\mathcal S\subseteq \mathcal S'$. For the other direction we show that if $(\bm x, \hat \bm y, \bm Z) \in \mathcal S'$ then $\bm Z= \bm x\hat \bm y^\top$. Since $\hat \bm y$ is an extreme point of $\mathcal Y$, there are $m$ linearly independent inequalities that are active at $\hat \bm y$. Let $\bm C\in \mathbb R^{m \times m}$ and $\bm d\in \mathbb R^m$ collect the coefficients $(\bm c_i, d_i)$ of these inequalities, so that $\bm C\hat \bm y+ \bm d= \bm 0$. For the same inequalities, the constraints in [\[eq:relaxation_polytopic\]](#eq:relaxation_polytopic){reference-type="eqref" reference="eq:relaxation_polytopic"} give us $\bm Z\bm c_i  + d_i \bm x= \bm 0$ or, equivalently, $\bm Z\bm C^\top  + \bm x\bm d^\top = \bm 0$. We then have $\bm Z\bm C^\top  = \bm x\hat\bm y^\top \bm C^\top$ and, since $\bm C$ is invertible, $\bm Z= \bm x\hat \bm y^\top$. ◻
:::

::: proof
*Alternative proof of Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"}.* As in the first proof of Theorem [\[th:validity_micp\]](#th:validity_micp){reference-type="ref" reference="th:validity_micp"}, note that the optimal solution of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} is such that the edges traversed by a unit of flow identify a path $p$. Note also that, for all $v \in \mathcal V$, the flow vectors $\bm y_v$ corresponding to a path $p$ are extreme points of the polytopes $\mathcal Y_v$. Then the validity of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} follows since our relaxation is exact in these points by Lemma [\[lemma:extreme\]](#lemma:extreme){reference-type="ref" reference="lemma:extreme"}. ◻
:::

::: remark
Consider the bilinear program [\[eq:bilinear_optimization\]](#eq:bilinear_optimization){reference-type="eqref" reference="eq:bilinear_optimization"} with polytopic sets $\mathcal X$ and $\mathcal Y$, and the additional constraint $\bm y\in \{0,1\}^m$. Assuming $\mathcal Y\subseteq [0,1]^m$, the first-level RLT is known to yield a valid mixed-integer linear formulation of this program [@adams1990linearization Theorem 1]. Lemma [\[lemma:extreme\]](#lemma:extreme){reference-type="ref" reference="lemma:extreme"} extends this result to generic closed convex sets $\mathcal X$. In fact, $\mathcal Y\subseteq [0,1]^m$ ensures that any vector $\bm y\in \mathcal Y\cap \{0,1\}^m$ is an extreme point of $\mathcal Y$, and the relaxation $\mathcal S'$ is exact in correspondence of these points.
:::

## Related relaxation techniques

The basic idea of generating new valid constraints by multiplying existing ones is classical, and has many incarnations: from the simple McCormick envelope [@mccormick1976computability] to semidefinite hierarchies for polynomial optimization [@lasserre2001global; @parrilo2003semidefinite], passing through RLT [@sherali1990hierarchy]. Among this family of techniques, the Lovász-Schrijver hierarchy [@lovasz1991cones] is the closest to ours, since it is set based and includes constraints of the form [\[eq:relaxation_polytopic\]](#eq:relaxation_polytopic){reference-type="eqref" reference="eq:relaxation_polytopic"}; see [@lovasz1991cones Theorem 1.6 and Conditions (iii) to (iii")]. However, this hierarchy focuses on binary optimization and symmetric quadratic maps, and its naive application to the bilinear set $\mathcal S$ would produce multiple redundant variables and constraints. Our approach leverages the bilinear structure of the set $\mathcal S$, that emerges naturally in the SPP in GCS, to construct a relaxation $\mathcal S'$ that is smaller and as tight as the first level of the Lovász-Schrijver hierarchy, without semidefinite constraints. (As discussed in Section [6](#sec:alternative_formulations){reference-type="ref" reference="sec:alternative_formulations"}, our practical experience is that higher levels of the hierarchy and semidefinite constraints lead to MICPs that, although stronger, are significantly slower to solve.)

If both the sets $\mathcal X$ and $\mathcal Y$ are polytopes, the convex hull of $\mathcal S$ in [\[eq:ch\]](#eq:ch){reference-type="eqref" reference="eq:ch"} is also a polytope, and its extreme points are $\mathop{\mathrm{ext}}\mathcal S= \{(\bm x, \bm y, \bm x\bm y^\top): \bm x\in \mathop{\mathrm{ext}}\mathcal X, \bm y\in \mathop{\mathrm{ext}}\mathcal Y\}$. In general, this yields an exponential-size description of $\mathop{\mathrm{conv}}\mathcal S$. Nevertheless, if the sets $\mathcal X$ and $\mathcal Y$ have further special structure then specialized techniques can be applied to efficiently generate additional valid inequalities for $\mathop{\mathrm{conv}}\mathcal S$; see, e.g., the techniques developed for network-interdiction problems [@davarnia2017simultaneous], pooling problems [@gupte2017relaxations], bipartite bilinear programs [@dey2019new], and bipartite boolean quadratic programs [@sripratak2022bipartite].

The recent work [@zhen2021extension] shows how perspective functions can be used to allow the multiplication of nonlinear convex constraints in the RLT algorithm. However, the relaxation in that work is not set based, and requires an explicit analysis of all the possible products of basic cone inequalities.

# Control applications {#sec:optimal_control}

A main application of the framework presented in this paper is optimal control of discrete-time dynamical systems. In this section we show how two simple control problems can be cast as SPPs in GCS. These examples illustrate some basic modeling techniques that can also be applied to control problems involving more complex discrete decision making.

## Minimum-time control

Consider the linear dynamical system $\bm s_{\tau+1} = \bm A\bm s_\tau + \bm B\bm a_\tau$, where $\bm s_\tau \in \mathbb R^q$ and $\bm a_\tau \in \mathbb R^r$ are the system state and control action at time step $\tau$. Given an initial state $\bm s_0$, we look for a sequence of controls that drives the system state to the origin in the minimum number $T$ of time steps. At each time $\tau$, the state and control pair $(\bm s_\tau, \bm a_\tau)$ is constrained in a compact convex set $\mathcal D$.

To formulate this problem as an SPP in GCS we proceed as in Figure [\[fig:minimum_time\]](#fig:minimum_time){reference-type="ref" reference="fig:minimum_time"}. The vertices $\mathcal V$ in our graph are ordered in a sequence. The source $s$ is the first vertex and the target $t$ is the last. The number of vertices is equal to $\bar T+1$, where $\bar T$ is a given upper bound on the optimal time horizon $T$. Each vertex that is not the target has two outgoing edges: one that connects it to the next vertex in the sequence and one that goes to the target. For each $v \in \mathcal V$, the continuous variable $\bm x_v$ represents a state and control pair $(\bm s_v, \bm a_v)$. These variables are constrained by the following sets: $\mathcal X_s :=\mathcal D\cap (\{\bm s_0\} \times \mathbb R^r)$ for the source, $\mathcal X_t := \{(\bm 0,\bm 0)\}$ for the target (the value of $\bm a_t$ is actually irrelevant), and $\mathcal X_v := \mathcal D$ for all the other vertices. To minimize the number of edges in the optimal path (i.e., the time steps to reach the origin), the length of each edge $(u,v)$ is $1$ if $\bm s_{v} = \bm A\bm s_u + \bm B\bm a_u$ and infinite otherwise. (See Example [\[ex:perspective_extended_values\]](#ex:perspective_extended_values){reference-type="ref" reference="ex:perspective_extended_values"} for the perspective of such a function.)

The solution of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} gives us a path $p := (v_0, \ldots, v_K)$. The optimal time horizon is $T := K$, and the corresponding control sequence is $\bm a_\tau := \bm a_{v_\tau}$ for $\tau = 0, \ldots, T-1$. The state trajectory is retrieved similarly, and is such that $\bm s_T := \bm s_t = \bm 0$.

:::: {.figure latex-placement="t"}
::: caption
Graphs for the formulation of the optimal-control problems in Section [8](#sec:optimal_control){reference-type="ref" reference="sec:optimal_control"} as SPPs in GCS.
:::
::::

## Control of hybrid systems {#sec:control_pwa}

PieceWise-Affine (PWA) systems are a popular framework for modeling hybrid dynamics. Loosely speaking, almost any dynamical system whose nonlinearity is exclusively due to discrete logics can be written in PWA form [@heemels2001equivalence]. Among the many applications of PWA systems, we have automotive [@borrelli2006mpc], power electronics [@geyer2008hybrid], and robotics [@marcucci2017approximate]. Given a finite collection $\{\mathcal D_\nu\}_{\nu \in \mathcal N}$ of compact convex subsets of the state and control space, a PWA system has dynamics $\bm s_{\tau+1} = \bm A_{\nu_\tau} \bm s_\tau + \bm B_{\nu_\tau} \bm a_\tau + \bm c_{\nu_\tau}$ if $(\bm s_\tau, \bm a_\tau) \in \mathcal D_{\nu_\tau}$. The index $\nu_\tau \in \mathcal N$ represents the system discrete *mode* at time $\tau$, which is itself a decision variable. We consider the problem of driving a PWA system from a given initial state $\bm s_0$ to the origin, in a fixed number $T$ of time steps. The objective is to minimize the sum of the stage costs $\gamma(\bm s_\tau, \bm a_\tau)$ for $\tau=0, \ldots, T-1$. The function $\gamma$ is convex and finite.

We model this problem through the GCS in Figure [\[fig:pwa\]](#fig:pwa){reference-type="ref" reference="fig:pwa"}. The source $s$ is the leftmost vertex and the target $t$ is the rightmost. In between, we have $T$ layers with $|\mathcal N|$ vertices each. The source is connected via an edge to each vertex in the first layer, and all the vertices in the last layer are connected to the target. Each pair of consecutive layers is fully connected. Also in this case the continuous variables $\bm x_v$ represent state and control pairs $(\bm s_v, \bm a_v)$. The source is paired with the set $\mathcal X_s := \{(\bm s_0,\bm 0)\}$, the target with $\mathcal X_t := \{(\bm 0,\bm 0)\}$, and the $\nu$th vertex $v$ of each layer with $\mathcal X_v := \mathcal D_\nu$. To enforce the initial conditions, the edges $(s,v)$ outgoing from the source have zero length if $\bm s_v = \bm s_s$, and infinite length otherwise. (Note that here the values of both $\bm a_s$ and $\bm a_t$ are irrelevant.) The length of any other edge $(u,v)$, where $u$ is the $\nu$th vertex in its layer, is $\gamma(\bm s_u, \bm a_u)$ if $\bm s_v = \bm A_\nu \bm s_u + \bm B_\nu \bm a_u + \bm c_\nu$ and infinite otherwise.

A shortest path $p := (v_0, \ldots, v_K)$ has now $T+2$ vertices. The optimal control at time $\tau = 0, \ldots, T-1$ is $\bm a_\tau := \bm a_{v_{\tau+1}}$. The state trajectory is defined similarly.

::: remark
Frequently in optimal control we need to enforce convex terminal constraints of the form $\bm s_T \in \mathcal D_T$, as well as convex terminal penalties $\gamma_T(\bm s_T)$. These are easily incorporated in our construction through a suitable modification of the set $\mathcal X_t$ and the lengths of the edges incoming to the target vertex.
:::

::: remark
The size of the GCS we just constructed is linear in the time horizon $T$ and quadratic in the number $|\mathcal N|$ of discrete modes. Conversely, common formulations for these problems have size linear in both $T$ and $|\mathcal N|$ [@marcucci2019mixed]. We will see in Section [9.3](#sec:example_pwa){reference-type="ref" reference="sec:example_pwa"} that the greater strength of our MICPs can be well worth this price.
:::

# Numerical results {#sec:examples}

This section collects multiple numerical experiments. We start in Section [9.1](#sec:example_2d){reference-type="ref" reference="sec:example_2d"} with a simple two-dimensional problem. Section [9.2](#sec:example_large_scale){reference-type="ref" reference="sec:example_large_scale"} presents a statistical analysis of the performance of our MICP on large-scale instances of the SPP in GCS. In Section [9.3](#sec:example_pwa){reference-type="ref" reference="sec:example_pwa"} we compare our approach with state-of-the-art mixed-integer formulations for control. Finally, in Section [9.4](#sec:example_failures){reference-type="ref" reference="sec:example_failures"} we use a carefully designed problem to show how symmetries in the GCS can loosen the relaxation of our MICP.

The code necessary to reproduce these results is available at <https://github.com/TobiaMarcucci/shortest-paths-in-graphs-of-convex-sets>. All the experiments are run using the commercial solver MOSEK 10.0 with default options on a laptop computer with processor 2.4 GHz 8-Core Intel Core i9 and memory 64 GB 2667 MHz DDR4. A mature implementation of the techniques presented in this paper is also provided by the open-source software Drake [@tedrake2019drake].

## Two-dimensional example {#sec:example_2d}

We consider the two-dimensional problem in Figure [\[fig:2d_setup\]](#fig:2d_setup){reference-type="ref" reference="fig:2d_setup"}. We have a graph $G$ with $|\mathcal V|=9$ vertices, $|\mathcal E|=22$ edges, and multiple cycles. The source $\mathcal X_s := \{\bm \theta_s\}$ and target $\mathcal X_t := \{\bm \theta_t\}$ sets are single points, while the remaining regions are full dimensional. The geometry of the sets $\mathcal X_v$ and the edge set $\mathcal E$ can be deduced from Figure [\[fig:2d_setup\]](#fig:2d_setup){reference-type="ref" reference="fig:2d_setup"}. As edge lengths we consider the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"} and the Euclidean distance squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}, whose corresponding shortest paths are shown in Figure [\[fig:2d_setup\]](#fig:2d_setup){reference-type="ref" reference="fig:2d_setup"} in orange and blue. As expected, the first path is almost straight, while the lengths of the segments in the second are better balanced.

In Figure [\[fig:2d_results\]](#fig:2d_results){reference-type="ref" reference="fig:2d_results"} we compare the optimal values of the SPP in GCS, the relaxation of our MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"}, and the relaxation of the McCormick formulation [\[eq:mc_relaxation\]](#eq:mc_relaxation){reference-type="eqref" reference="eq:mc_relaxation"}. Both relaxations are Second-Order-Cone Program (SOCPs), and for the McCormick one the bounding boxes $\mathcal B_v$ are chosen as small as the corresponding sets $\mathcal X_v$ allow. We run this comparison for different values of a parameter $\sigma>0$ that controls the volume of the sets $\mathcal X_v$. The value $\sigma=1$ corresponds to the GCS in Figure [\[fig:2d_setup\]](#fig:2d_setup){reference-type="ref" reference="fig:2d_setup"}. While for $\sigma \neq 1$ each set $\mathcal X_v$ is shrunk or enlarged via a uniform scaling, with scale factor $\sigma$, relative to a fixed Chebyshev center of the set.

:::: {.figure latex-placement="t"}
::: caption
Two-dimensional SPP in GCS from Section [9.1](#sec:example_2d){reference-type="ref" reference="sec:example_2d"}. The tightness of the convex relaxation of our MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} is analyzed for two edge lengths (the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"} and the Euclidean distance squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}) and different sizes of the sets $\mathcal X_v$ (parameterized by the scalar $\sigma$). As a baseline, we also report the optimal value of the relaxation of the McCormick formulation [\[eq:mc_relaxation\]](#eq:mc_relaxation){reference-type="eqref" reference="eq:mc_relaxation"}.
:::
::::

When the edge length is the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"}, the top panel in Figure [\[fig:2d_results\]](#fig:2d_results){reference-type="ref" reference="fig:2d_results"} shows that our relaxation is exact for all values of $\sigma$. This was expected for $\sigma$ close to zero, since by Remark [\[rem:singletons\]](#rem:singletons){reference-type="ref" reference="rem:singletons"} our relaxation is exact when the sets are singletons. Similarly, the problem is trivial for very large $\sigma$, when the regions are so big that, no matter the discrete path we take, we can always reach the target via a straight line. However, that our relaxation is exact for all the intermediate values of $\sigma$ is not an obvious result. The McCormick relaxation is also exact for small $\sigma$, but gives a trivial lower bound of zero when the sets are large.

With the Euclidean length squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}, both relaxations are still guaranteed to be tight as $\sigma$ goes to zero. This is confirmed by the bottom panel of Figure [\[fig:2d_results\]](#fig:2d_results){reference-type="ref" reference="fig:2d_results"}. When $\sigma$ is very large, we have seen in Section [3](#sec:complexity){reference-type="ref" reference="sec:complexity"} that our problem is equivalent to the HPP, and the argument from Theorem [\[th:complexity\]](#th:complexity){reference-type="ref" reference="th:complexity"} shows that its optimal value is $\|\bm \theta_t - \bm \theta_s\|_2^2/K = 11.6$, where $K=7$ is the number of edges in the longest $s$-$t$ path in the graph in Figure [\[fig:2d_setup\]](#fig:2d_setup){reference-type="ref" reference="fig:2d_setup"}. A close inspection of the bottom of Figure [\[fig:2d_results\]](#fig:2d_results){reference-type="ref" reference="fig:2d_results"} reveals that, for large $\sigma$, our relaxation yields the lower bound $\|\bm \theta_t - \bm \theta_s\|_2^2/(|\mathcal V|-1) = 10.1$, which corresponds to the simple inequality $K \leq |\mathcal V| -1$. (Using a duality argument, it can be verified that our relaxation always recovers this bound.) Conversely, the lower bound provided by the McCormick relaxation is again equal to zero.

## Large-scale random instances {#sec:example_large_scale}

We present a statistical analysis of the performance of our formulation. We generate a variety of random large-scale SPPs in GCS, and we analyze the relaxation tightness and the solution times of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} as functions of various problem parameters. We stress that generating random graphs representative of the "typical" SPP in GCS we might encounter in practice is a difficult operation. Inevitably, the instances we describe below are not completely representative, and our algorithm might perform worse or better on other classes of random graphs. Our goal here is to show that our MICP is not limited to small-scale problems.

We construct an SPP in GCS as follows. We set $\mathcal X_s := \{\bm 0\}$ and $\mathcal X_t := \{\bm 1\}$. The rest of the sets $\mathcal X_v$ are axis-aligned cubes with volume $\Lambda$ and center drawn uniformly at random in $[0,1]^n$. Given a number $|\mathcal E|$ of edges, we construct the edge set in two steps. First we generate multiple $s$-$t$ paths such that every vertex $v \neq s,t$ is traversed exactly by one path. These are determined via a random partition of the set $\mathcal V- \{s, t\}$: the number of sets in the partition (number of paths) is drawn uniformly from the interval $[1, |\mathcal V| - 2]$, and also the number of vertices in each set (length of each path) is a uniform random variable. Then we extend the edge set by drawing edges uniformly at random from the set $\{(u,v) \in \mathcal V^2 : v \neq s, u \neq t, u \neq v \}$ until a desired cardinality $|\mathcal E|$ is reached. As edge lengths we consider the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"} and the Euclidean distance squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}, which both make our formulation [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} a mixed-integer SOCP.

For each edge length, we first solve $100$ random instances with the following nominal parameters: volume $\Lambda = 0.01$, $n = 4$ dimensions, $|\mathcal V| = 50$ vertices, and $|\mathcal E|=100$ edges. Then we solve four other batches of $100$ problems where, in each batch, a different subset of these parameters is increased by a factor of $5$. Specifically, these additional batches test our formulation in case of large sets $\mathcal X_v$ ($\Lambda$ from $0.01$ to $0.05$), high dimensions ($n$ from $4$ to $20$), dense graphs ($|\mathcal E|$ from $100$ to $500$), and large graphs ($|\mathcal V|$ and $|\mathcal E|$ from $50$ and $100$ to $250$ and $500$). To give an idea of what these problems look like, the projection onto two dimensions of a GCS generated using the nominal parameters is shown in Figure [2](#fig:random_instance){reference-type="ref" reference="fig:random_instance"}.

:::: {#fig:random_instance .figure latex-placement="t"}
![](Marcucci2021Shortest_figs/random_instance.png){height="3.2cm"}

::: caption
Projection onto two dimensions of a random instance of the SPP in GCS from Section [9.2](#sec:example_large_scale){reference-type="ref" reference="sec:example_large_scale"}. The problem parameters have nominal value.
:::
::::

:::: {#fig:statistical_analysis .figure latex-placement="t"}
![](Marcucci2021Shortest_figs/statistical_analysis.png){width=".99\\columnwidth"}

::: caption
Relaxation gap versus MICP solution time for the 500 random instances described in Section [9.2](#sec:example_large_scale){reference-type="ref" reference="sec:example_large_scale"}. Two edge lengths are analyzed: the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"} and the Euclidean distance squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}. For each edge length, 100 nominal instances are generated with the nominal problem parameters, and four other batches of 100 instances each are obtained by increasing a different subset of the parameters. Our relaxation is almost always exact with the Euclidean length. While, with the Euclidean length squared, it is more sensitive to the dimension $n$ of the space and the density of the graph $G$. (Note the different horizontal scales of the two plots.)
:::
::::

Figure [3](#fig:statistical_analysis){reference-type="ref" reference="fig:statistical_analysis"} shows the relaxation gap (cost gap between the MICP and its relaxation, normalized by the MICP cost) versus the MICP solution time for all the instances described above. As observed in the previous example, the Euclidean edge length [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"} results in easier programs: our relaxation is tight in almost all the instances and the solution times are relatively low. The squared edge length [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"} leads to more challenging problems, even though the maximum relaxation gap and runtime are only $2.1\%$ and $0.66$s in the nominal case. When the volume of the cubes $\mathcal X_v$ is increased to $\Lambda=0.05$ these values increase to $9.1\%$ and $1.12$s, and the performance of our MICP is minimally affected. Note that this is not in contrast with the previous example, where we analyzed the regime of extremely large sets $\mathcal X_v$. Note also that the volume of the sets does not affect the MICP size. The growth of the space dimension to $n=20$ increases the size of our programs, and also loosens the relaxation. The largest relaxation gap is $28.9\%$, and our MICP takes $72$s to be solved in the worst case. Similarly, when the number $|\mathcal E|$ of edges is increased to $500$ the maximum relaxation gap and runtime become $32.9\%$ and $174$s. This is due to the combination of the quadratic edge length and the large number of cycles that we have in a graph with high density of edges $|\mathcal E|/|\mathcal V|$. To show this, in the last batch of problems we keep $|\mathcal E|=500$ and we increase the number of vertices to $|\mathcal V| = 250$. This increases the MICP size further but makes the graph sparser, reducing the maximum relaxation gap and runtime to $5.3\%$ and $5.4$s.

Also for the problems in this analysis our formulation outperforms the McCormick one in [\[eq:mc_relaxation\]](#eq:mc_relaxation){reference-type="eqref" reference="eq:mc_relaxation"}. With the nominal parameters, the McCormick median (maximum) runtime is $12.9$ ($4.3$) times larger than ours for the Euclidean length [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"}, and $10.3$ ($2.7$) times larger for the Euclidean length squared [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}. This performance difference grows larger for the other batches of problems, where the McCormick formulation reaches our time limit of one hour very often. The slowness of the McCormick approach is due to its loose relaxation: even with the nominal parameters, we have a median (maximum) relaxation gap of $29\%$ ($52\%$) for [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"}, and $34\%$ ($58\%$) for [\[eq:2norm_squared\]](#eq:2norm_squared){reference-type="eqref" reference="eq:2norm_squared"}.

## Optimal control {#sec:example_pwa}

We apply the method from Section [8.2](#sec:control_pwa){reference-type="ref" reference="sec:control_pwa"} to solve the optimal-control problem shown in Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"}. We have a mechanical system with position $\bm q\in \mathbb R^2$, velocity $\bm v\in \mathbb R^2$, and force $\bm a\in \mathbb R^2$. The system has the dynamics of a double integrator: $\bm q_{\tau + 1} = \bm q_\tau + \bm v_\tau$ and $\bm v_{\tau + 1}  = \bm v_\tau + \eta \bm a_\tau$, where $\eta$ is a scalar parameter that regulates the system controllability. The system state at time $\tau$ is $\bm s_\tau := (\bm q_\tau, \bm v_\tau)$. The initial position is $\bm q_0:= (0.5,-3.5)$ (green plus at the bottom left of Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"}), the initial velocity is $\bm v_0 := \bm 0$. At each time step $\tau=1, \ldots, T-1$, the position $\bm q_\tau$ must belong to one of the seven regions in Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"}, while the velocity and the controls are limited by the constraints $\| \bm v_\tau \|_\infty \leq 1$ and $\| \bm a_\tau \|_\infty \leq 1$. The goal is to reach the point $\bm q_T := (6.5,3.5)$ (green cross at the top right of Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"}) with zero velocity $\bm v_T$ in $T := 30$ time steps. The cost function is the sum of the stage costs $\gamma(\bm s_\tau, \bm a_\tau) := \| \bm v_\tau \|_2^2/5 + \| \bm a_\tau \|_2^2$.

We let the parameter $\eta$ vary between the seven regions. The five regions in the range $-5 \leq q_2 \leq 5$ (light blue in Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"}) have $\eta=1$. While in the other two regions (red in Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"}) we make the system more expensive to control by setting $\eta=0.1$. Since the parameter $\eta$ varies with the state, the system dynamics is PWA and the control problem falls into the class considered in Section [8.2](#sec:control_pwa){reference-type="ref" reference="sec:control_pwa"}. The GCS beneath this problem (depicted in Figure [\[fig:pwa\]](#fig:pwa){reference-type="ref" reference="fig:pwa"}) has $|\mathcal V| = 212$ vertices and $|\mathcal E| = 1435$ edges, and the convex sets $\mathcal X_v$ live in $\mathbb R^6$. Also in this case problem [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} is a mixed-integer SOCP.

:::: {#fig:footstep .figure latex-placement="t"}
::: caption
Control problem from Section [9.3](#sec:example_pwa){reference-type="ref" reference="sec:example_pwa"} of driving a dynamical system from start (green plus) to goal (green cross). The light-blue and red regions have high and low controllability, respectively. The optimal positions $\bm q_\tau$ are white circles, the optimal controls $\bm a_\tau$ are blue arrows. The triangles are the auxiliary variables $\bm q_\tau^\nu$ whose convex combination yields $\bm q_\tau$. The opacity of the triangles equals the optimal value of the variables $b_\tau^\nu$ that serve as weights in this convex combination.
:::
::::

Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"} shows the optimal trajectory $(\bm q_0, \ldots, \bm q_T)$ (white circles) and the optimal controls $(\bm a_0, \ldots, \bm a_{T-1})$ (blue arrows). Geometrically, the red regions would be shortcuts to the goal, but the low controllability in these areas makes it too expensive not to fall out of the feasible set. The optimal strategy is then to follow a winding trajectory and incur a cost of $9.37$.

As a baseline, we first solve the problem using the state-of-the-art perspective formulation from [@moehle2015perspective Section 6] (see also [@marcucci2019mixed Section 5.2.2]). At each time step $\tau$, this expresses the system state $\bm s_\tau$ as a convex combination of one auxiliary variable $\bm s_\tau^\nu$ per region $\nu=1, \ldots, 7$. The control $\bm a_\tau$ is decomposed similarly. When the coefficients $b_\tau^\nu$ of this combination are required to be binary, the solver is forced to make a hard selection of the region in which the system must be at each time step. When the coefficients $b_\tau^\nu$ can be fractional, the system evolves according to a convex combination of the dynamics in each region. Figure [\[fig:footstep_pf\]](#fig:footstep_pf){reference-type="ref" reference="fig:footstep_pf"} illustrates the solution of the convex relaxation of this formulation (which, thanks to a perspective reformulation of the stage cost, is also an SOCP). It reports the position $\bm q_\tau$, the barely visible controls $\bm a_\tau$, and the auxiliary copies $\bm q_\tau^\nu$ of the position vector. The latter have triangular markers and opacity equal to the value of the indicator $b_\tau^\nu$. As it can be seen, this relaxation is insensitive to the arrangement of the regions, and its optimal trajectory heads straight to the goal. Also the indicator variables $b_\tau^\nu$ are uninformative, and take nonzero value in the regions with low controllability (visible triangles in the red regions). The optimal value of this relaxation is $0.67$, which is only $7\%$ of the MICP value ($93\%$ relaxation gap). The MICP solution time is $1011\text{s}\approx 17$min.

The convex relaxation of our formulation is much tighter: its optimal value is $7.46$, which is $80\%$ of the MICP value ($20\%$ relaxation gap). This has a dramatic effect on computation times that are now reduced to $7.1$s. To make a plot comparable to Figure [\[fig:footstep_pf\]](#fig:footstep_pf){reference-type="ref" reference="fig:footstep_pf"} we leverage the structure of our GCS in Figure [\[fig:pwa\]](#fig:pwa){reference-type="ref" reference="fig:pwa"}. The equivalent of the indicator variable $b_\tau^\nu$ is the total flow traversing the $\nu$th vertex in the $\tau$th layer of the graph. Similarly, the position of the same vertex plays the role of the auxiliary variables $(\bm s_\tau^\nu, \bm a_\tau^\nu)$, which can then be combined using the coefficients $b_\tau^\nu$ to get candidate values for the state $\bm s_\tau$ and the control $\bm a_\tau$. Figure [\[fig:footstep_spp\]](#fig:footstep_spp){reference-type="ref" reference="fig:footstep_spp"} illustrates these values, and shows that the trajectory reconstructed from our relaxation resembles the MICP solution in Figure [\[fig:footstep_micp\]](#fig:footstep_micp){reference-type="ref" reference="fig:footstep_micp"} much more closely. All the markers in the regions with low controllability are now invisible, indicating that our relaxation correctly identifies these as regions of high cost. The visible points $\bm q_\tau^\nu$ are clustered along the optimal trajectory of the MICP, suggesting that our relaxation contains detailed information about the optimal path to reach the goal.

## Symmetries in the GCS {#sec:example_failures}

:::: {#fig:symmetry .figure latex-placement="t"}
::: caption
Instance of the SPP in GCS from Section [9.4](#sec:example_failures){reference-type="ref" reference="sec:example_failures"} that shows how symmetries in the GCS can deteriorate the convex relaxation of our MICP. For the relaxation, the cost contribution of edge $e$ is obtained by multiplying the flow $y_e$ by the distance between $\bar \bm z_e$ and $\bar \bm z_e'$. Since only the mean of $\bar \bm z_{(1,3)}'$ and $\bar \bm z_{(2,3)}'$ is required to match $\bar \bm z_{(3,t)}$, the cost is minimized by moving these two points closer to $\bar \bm z_{(1,3)}$ and $\bar \bm z_{(2,3)}$, respectively.
:::
::::

We conclude by showing how symmetries in the GCS can deteriorate the convex relaxation of our MICP and, in principle, make it arbitrarily loose. We illustrate this through the following carefully designed problem.

We consider the SPP in GCS depicted in Figure [\[fig:symmetry_mip\]](#fig:symmetry_mip){reference-type="ref" reference="fig:symmetry_mip"}. We have an acyclic graph with $|\mathcal V| = 5$ vertices and $|\mathcal E| = 5$ edges. All the sets $\mathcal X_v$ are singletons $\{ \bm \theta_v \}$, except for $\mathcal X_3$ which is a full-dimensional rectangle. As an edge length, we use the Euclidean distance [\[eq:2norm\]](#eq:2norm){reference-type="eqref" reference="eq:2norm"}. Solving this problem, we obtain the optimal path $p = (s,1,3,t)$ with length $7.4$ (the symmetric solution $p = (s,2,3,t)$ would also be optimal). The corresponding vertex positions are connected by an orange line in Figure [\[fig:symmetry_mip\]](#fig:symmetry_mip){reference-type="ref" reference="fig:symmetry_mip"}.

Figure [\[fig:symmetry_relaxation\]](#fig:symmetry_relaxation){reference-type="ref" reference="fig:symmetry_relaxation"} illustrates the solution of the relaxation of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"}. For each edge $e$, we connect the optimal points $\bar \bm z_e := \bm z_e / y_e$ and $\bar \bm z_e' := \bm z_e' / y_e$ with an orange line, labeled in blue with the corresponding flow $y_e$. Note that, for $y_e > 0$, we have $\tilde \ell_e (\bm z_e, \bm z_e', y_e) = \ell_e (\bar \bm z_e, \bar \bm z_e') y_e$, and the vectors $\bar \bm z_e$ and $\bar \bm z_e'$ are the actual points where the length of the edge $e$ is evaluated. Note also that, by [\[eq:micp_nonnegativity\]](#eq:micp_nonnegativity){reference-type="eqref" reference="eq:micp_nonnegativity"}, we have $\bar \bm z_e \in \mathcal X_u$ and $\bar \bm z_e' \in \mathcal X_v$. The relaxation splits the unit of flow injected in the source into two: half unit is shipped to the target via the top path, the other half via the bottom path. The optimal value of this convex program is $7.0$.

The looseness of the relaxation can be explained as follows. If we denote with $\rho$ the flow traversing edge $(1,3)$, the flow conservation gives $y_{(2,3)} = 1 - \rho$, while the flow through the edge $(3,t)$ is always one. Since the variables $\bar \bm z_{(1,3)}$, $\bar \bm z_{(2,3)}$, and $\bar \bm z_{(3,t)}'$ are forced to match $\bm \theta_1$, $\bm \theta_2$, and $\bm \theta_t$, respectively, the cost terms in [\[eq:micp_objective\]](#eq:micp_objective){reference-type="eqref" reference="eq:micp_objective"} corresponding to the edges $(1,3)$, $(2,3)$, and $(3,t)$ read $$\begin{align}
\label{eq:symmetry_objective}
\rho \| \bar \bm z_{(1,3)}' - \bm \theta_1 \|_2 + (1 - \rho) \| \bar \bm z_{(2,3)}' - \bm \theta_2 \|_2 + \| \bm \theta_t - \bar \bm z_{(3,t)} \|_2.
\end{align}$$ The only constraint that links these variables is [\[eq:micp_conservation\]](#eq:micp_conservation){reference-type="eqref" reference="eq:micp_conservation"} for $v=3$, which gives $\rho \bar \bm z_{(1,3)}' + (1 - \rho) \bar \bm z_{(2,3)}' = \bar \bm z_{(3,t)}$. When $\rho = 1/2$, this constraint asks the mean of $\bar \bm z_{(1,3)}'$ and $\bar \bm z_{(2,3)}'$ to match $\bar \bm z_{(3,t)}$, as opposed to forcing either one of the first two points to match the third, as it would be for $\rho \in \{0,1\}$. Therefore, while keeping their mean equal to $\bar \bm z_{(3,t)}$, the points $\bar \bm z_{(1,3)}'$ and $\bar \bm z_{(2,3)}'$ can move vertically, and get closer to $\bm \theta_1$ and $\bm \theta_2$. This reduces the first two terms in [\[eq:symmetry_objective\]](#eq:symmetry_objective){reference-type="eqref" reference="eq:symmetry_objective"}, and keeps the third term unchanged.

Although this example leads to a relaxation gap of only $5\%$, a simple variation of it shows that our relaxation can be arbitrarily loose. In particular, if we let $\ell_{(s,1)} := \ell_{(s,2)} := 0$ and we shift the centers of the sets $\mathcal X_3$ and $\mathcal X_t$ to the origin, then the cost of the MICP and its relaxation are reduced to $2$ and $0$, and the relaxation gap becomes $100\%$. Nevertheless, we emphasize that this is a contrived problem, and the instances we encounter in practice lead to these phenomena very rarely.

# Conclusions {#sec:conclusions}

In this paper we have introduced the SPP in GCS, a versatile generalization of the classical SPP. Our main contribution is a compact MICP formulation for the solution of this NP-hard problem. Numerical experiments show that the convex relaxation of our formulation is typically very tight, and it enables us to quickly solve large problems to global optimality. We have demonstrated the applicability of the proposed framework to control systems: many optimal control problems are interpretable as SPPs in GCS and, in our tests, the proposed formulation outperforms state-of-the-art techniques for their solution.

# Acknowledgments {#acknowledgments .unnumbered}

We would like to thank Hongkai Dai for all the time spent improving the solver interface used in the numerical experiments of this paper.

# Other graph problems in GCS {#sec:extensions}

Existing exact algorithms for graph problems with neighborhoods rely on expensive mixed-integer nonconvex optimization [@gentilini2013travelling; @burdick2021multi; @blanco2017minimum]. Here we show that, under standard convexity assumptions, the techniques from Section [7](#sec:relaxation){reference-type="ref" reference="sec:relaxation"} apply beyond the SPP, and yield exact MICP reformulations for a wide variety of graph problems. A thorough numerical evaluation of these novel formulations will be the object of future works.

Given a directed graph $G:=(\mathcal V,\mathcal E)$, many combinatorial problems require finding a set of edges $\mathcal E^\star \subseteq \mathcal E$ that is optimal according to a given criterion and given feasibility conditions. Typically, these are formulated as integer linear programs of the form $$\begin{align}
\label{eq:ilp}
\mathrm{minimize}\quad \sum_{e \in \mathcal E} l_e y_e \quad \mathrm{subject \ to}\quad \bm y\in \mathcal Y\cap \{0,1\}^{|\mathcal E|},
\end{align}$$ where $\bm y:= (y_e)_{e \in \mathcal E}$. The edge set $\mathcal E^\star$ is parameterized by the variables $y_e$ as $\mathcal E^\star = \{e \in \mathcal E: y_e = 1\}$, the polyhedron $\mathcal Y\subseteq [0,1]^{|\mathcal E|}$ embodies the feasibility conditions, and the cost is a linear function that assigns a weight $l_e \geq 0$ to each edge $e \in \mathcal E$.

We extend the graph problem modeled by [\[eq:ilp\]](#eq:ilp){reference-type="eqref" reference="eq:ilp"} to its version in GCS as done for the SPP. We let the position $\bm x_v \in \mathbb R^n$ of vertex $v$ be a decision variable, constrained in the set $\mathcal X_v$, and we let the length of the edge $e = (u,v)$ be $\ell_e (\bm x_u, \bm x_v)$. The sets $\mathcal X_v$ and the functions $\ell_e$ satisfy the assumptions from Section [2](#sec:statement){reference-type="ref" reference="sec:statement"}. We define two auxiliary variables $\bm z_e := y_e \bm x_u$ and $\bm z_e' := y_e \bm x_v$ per edge $e = (u,v)$, and we formulate our graph problem in GCS as in [\[eq:bilinear_spp\]](#eq:bilinear_spp){reference-type="eqref" reference="eq:bilinear_spp"}, with the condition $\bm y\in \mathcal Y\cap \{0,1\}^{|\mathcal E|}$ in place of [\[eq:bilinear_flow\]](#eq:bilinear_flow){reference-type="eqref" reference="eq:bilinear_flow"}. This yields a mixed-integer program with bilinear constraints. At this point, in the case of the SPP, we grouped the constraints in our problem vertex by vertex, and we applied the relaxation from Lemma [\[lemma:valid_constraint\]](#lemma:valid_constraint){reference-type="ref" reference="lemma:valid_constraint"}. However, in general, the polyhedron $\mathcal Y$ might not enjoy this convenient separability, as it might couple flows that do not share a common vertex. There are two ways around this issue.

One option is just to separate the flow constraints that are vertex-wise separable from the ones that are not. Using only the first to define the polyhedra $\mathcal Y_v \subseteq [0,1]^{|\mathcal E_v|}$, we can then proceed as in Remark [\[rem:coincise_bilinear\]](#rem:coincise_bilinear){reference-type="ref" reference="rem:coincise_bilinear"}. The MICP we get is a valid problem formulation since any point in $\mathcal Y_v \cap \{0,1\}^{|\mathcal E_v|}$ is an extreme point of $\mathcal Y_v$ and, by Lemma [\[lemma:extreme\]](#lemma:extreme){reference-type="ref" reference="lemma:extreme"}, our relaxation is exact for those points. The formulation resulting from this approach is compact but it might be weak.

The second option is to introduce new variables that represent the product of each flow $y_e$ and vertex position $\bm x_v$, even if edge $e$ is not incident with vertex $v$. This gives us a total of $n |\mathcal V| |\mathcal E|$ continuous variables $\bm Z:=  \bm x\bm y^\top$, where $\bm x:= (\bm x_v)_{v \in \mathcal V}$ lives in the Cartesian product $\mathcal X:= \prod_{v \in \mathcal V} \mathcal X_v$. Defining the set $\mathcal S$ as in [\[eq:bilinear_set\]](#eq:bilinear_set){reference-type="eqref" reference="eq:bilinear_set"}, the constraints of our problem become $\bm y\in \{0,1\}^{|\mathcal E|}$ and $(\bm x, \bm y, \bm Z) \in \mathcal S$. We then use the relaxation $\mathcal S'$ of $\mathcal S$ from [\[eq:relaxation_polytopic\]](#eq:relaxation_polytopic){reference-type="eqref" reference="eq:relaxation_polytopic"} to get an MICP whose validity is ensured again by Lemma [\[lemma:extreme\]](#lemma:extreme){reference-type="ref" reference="lemma:extreme"}. This second option yields larger but potentially stronger MICPs.

# Dual optimization problem {#sec:dual}

In this appendix we analyze the dual of the convex relaxation of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"}, and we draw additional parallels between this problem and the network-flow formulation [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"} of the SPP.

## Dual of the SPP {#sec:dual_lp}

As a reference for the discussion below, the dual of the LP [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"} is $$\label{eq:dual_lp}
\begin{align}
\mathrm{maximize}\quad & p_s - p_t \\
\label{eq:dual_lp_potential}
\mathrm{subject \ to}\quad & p_u - p_v \leq l_e, && \forall e = (u,v) \in \mathcal E.
\end{align}$$ Here $p_s$ and $p_t$ are the multipliers of the two constraints in [\[eq:network_st\]](#eq:network_st){reference-type="eqref" reference="eq:network_st"}, and $p_v$ for $v \neq s,t$ are the multiplier of the flow conservation in [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"}. These multipliers are interpretable as potentials: the objective asks to maximize the potential jump between source and target, and the constraints ensure that the potential jump along each edge does not exceed the edge length. Since the degree constraints in [\[eq:network_v\]](#eq:network_v){reference-type="eqref" reference="eq:network_v"} are redundant (see Remark [\[rem:degree\]](#rem:degree){reference-type="ref" reference="rem:degree"}), their multipliers do not appear in the dual problem.

For the LPs [\[eq:network_flow\]](#eq:network_flow){reference-type="eqref" reference="eq:network_flow"} and [\[eq:dual_lp\]](#eq:dual_lp){reference-type="eqref" reference="eq:dual_lp"}, complementary slackness reads $(l_e - p_u + p_v) y_e = 0$ for all edges $e =(u,v)$. Therefore, at optimality, each edge $e \in \mathcal E_p$ along the shortest path must have a potential jump equal to its edge length.

## Dual of the SPP in GCS {#sec:dual_convex_relaxation}

The convex relaxation of the MICP [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} is a conic program, and its dual is derived in the standard way. To make the interpretation of the dual program easier, we assume that the graph $G$ is acyclic, and we remove the degree constraints [\[eq:micp_degree\]](#eq:micp_degree){reference-type="eqref" reference="eq:micp_degree"} from the primal. This leads to the following optimization problem: $$\label{eq:dual}
\begin{align}
\label{eq:dual_objective}
\mathrm{maximize}\quad & p_s - p_t \\
\label{eq:dual_potential}
\mathrm{subject \ to}\quad
& \bm r_u^\top \bm x_u + p_u - \bm r_v^\top \bm x_v - p_v \leq \ell_e(\bm x_u, \bm x_v), \\
\nonumber & \qquad\qquad\qquad\qquad\qquad\qquad \ \ \forall \bm x_u \in \mathcal X_u, \bm x_v \in \mathcal X_v, e =(u,v) \in \mathcal E, \\
\label{eq:dual_auxiliary}
& \bm r_s = \bm r_t = 0.
\end{align}$$ The dual variables are $p_v$ and $\bm r_v$ for all $v \in \mathcal V$. The first are paired with the flow constraints as above. The second correspond to the portion of the flow conservation [\[eq:micp_conservation\]](#eq:micp_conservation){reference-type="eqref" reference="eq:micp_conservation"} that involves the auxiliary variables $\bm z_e$ and $\bm z_e'$ (the additional variables $\bm r_s$ and $\bm r_t$ have only the role of simplifying the presentation).

Similarly to the LP [\[eq:dual_lp\]](#eq:dual_lp){reference-type="eqref" reference="eq:dual_lp"}, the dual [\[eq:dual\]](#eq:dual){reference-type="eqref" reference="eq:dual"} can be interpreted in terms of potentials. For each vertex $v \in \mathcal V$, the linear function $\bm r_v^\top \bm x_v + p_v$ defines the potential of the point $\bm x_v \in \mathcal X_v$. Because of [\[eq:dual_auxiliary\]](#eq:dual_auxiliary){reference-type="eqref" reference="eq:dual_auxiliary"}, these functions are constant over the source and target sets, and the objective [\[eq:dual_objective\]](#eq:dual_objective){reference-type="eqref" reference="eq:dual_objective"} maximizes the potential jump between $s$ and $t$ as in the classical SPP. Like [\[eq:dual_lp_potential\]](#eq:dual_lp_potential){reference-type="eqref" reference="eq:dual_lp_potential"}, constraint [\[eq:dual_potential\]](#eq:dual_potential){reference-type="eqref" reference="eq:dual_potential"} asks the potential jump along an edge to be smaller than the edge length. By setting all the potential functions to zero, we see that the dual problem is always feasible and has nonnegative optimal value.

For the primal-dual pair [\[eq:micp\]](#eq:micp){reference-type="eqref" reference="eq:micp"} and [\[eq:dual\]](#eq:dual){reference-type="eqref" reference="eq:dual"}, complementary slackness requires $$\bm r_u^\top \bm z_e + p_u y_e - \bm r_v^\top \bm z_e' - p_v y_e = \tilde\ell_e(\bm z_e, \bm z_e', y_e)$$ for all edges $e=(u,v)$. As for the classical SPP, this is trivially satisfied if $y_e = 0$. While, for $y_e > 0$, we get $\bm r_u^\top \bar \bm z_e + p_u - \bm r_v^\top \bar \bm z_e' - p_v = \ell_e (\bar \bm z_e, \bar \bm z_e')$, with $\bar \bm z_e := \bm z_e/y_e$ and $\bar \bm z_e' := \bm z_e'/y_e$. In words, at optimality, the potential jump along edge $e$ is tight to the edge length $\ell_e$ at the point $(\bar \bm z_e, \bar \bm z_e')$.

[^1]: Department of Electrical Engineering and Computer Science, Massachusetts Institute of Technology, Cambridge, MA (, , , ).

[^2]: Submitted to the editors DATE.

[^3]: The results presented in this paper are easily extended to the case in which the sets $\mathcal X_v$ do not have common dimension $n$.

[^4]: More precisely the sets $\mathop{\mathrm{epi}}\tilde f$ and $\widetilde{\mathop{\mathrm{epi}}f}$ are isomorphic: $\mathop{\mathrm{epi}}\tilde f := \{(\bm x, \lambda, \sigma): (\bm x, \sigma, \lambda) \in \widetilde{\mathop{\mathrm{epi}}f}\}$.

[^5]: We are slightly abusing notation here: since in Definition [\[def:perspective_function\]](#def:perspective_function){reference-type="ref" reference="def:perspective_function"} we defined the perspective of functions with a single argument, to be precise, we should write $\tilde \ell_e((\bm z_e, \bm z_e'), y_e)$.
