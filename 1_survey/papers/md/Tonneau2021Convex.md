---
citation_key: Tonneau2021Convex
arxiv_id: 2109.07977
arxiv_url: https://arxiv.org/abs/2109.07977
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:39:44Z
origin: ai+web
reviewed: false
---

# Introduction

Trajectory generation is the computation of both a continuous path and its time parametrisation, subject to geometric, continuity and dynamic constraints. The problem is of importance in robotics, with applications in various fields including autonomous vehicles, manipulators, UAVs and legged robots.

Trajectory generation is commonly addressed as a Trajectory Optimisation (TO) problem aiming to find the minimum time trajectory satisfying the constraints. The non-linearity of the problem makes it hard to solve globally and efficiently, especially as real-time computation is often a requirement.

We consider the Polytope Traversal problem (PT), a TO problem where the trajectory is constrained to traverse a sequence of polytopes (Fig. [1](#fig:teaser){reference-type="ref" reference="fig:teaser"}) in a given order. Trajectory generation under collision avoidance constraints is a typical application of the problem, where the polytopes represent the free configuration space of an UAV [@gao18] or a car. In this case the time-parametrisation requires the computation of the time that the trajectory will spend in each of the polytopes.

::::: {#fig:teaser .figure}
::: overpic
figures/teaser
:::

::: caption
Illustration of the Polytope Traversal problem in 3D. The coloured polytopes correspond to constraints that concern specific parts of the Bezier curve displayed. The resulting curve is constrained on the initial / terminal positions and subject to constraints on the derivatives.
:::
:::::

## Current approaches for PT require an initial guess

Under the (common) assumption that the dynamic constraints are linear, if the time allocations are fixed the problem is convex. Likewise if the path is fixed, the problem is again convex[@Verscheure09]. This fact motivates the use of a decoupled approach to first compute a geometrically valid path, then the optimal time parametrisation of the path [@TOPP14; @hauser2014fast]. While the decoupling implies that there is no guarantee of obtaining a global minimum, the reliability of this approach has been demonstrated. Bilevel formulations that exploit the gradients of each of the problems can successfully be used to iteratively improve the results in spite of their non-linear structure[@Sun20; @Tang20].

Such approaches will be efficient under the assumption that the geometric path is always feasible, which is the case in several instances of the problem (including UAVs): if the dynamics of the system allow to accelerate freely in any direction and the problem has a solution, any geometric path will be feasible given arbitrarily large time allocations.

Unfortunately this assumption does not hold when the constraints make it impossible to accelerate in one direction. This happens in CROC [@Fernbach:ccroc], an instance of the problem where the trajectory represents the motion of the centre of mass of a legged robot, subject to switching contact constraints. In such cases, providing a good initial guess for the bi-level optimisation can prove challenging.

We are thus primarily concerned with the efficient computation of a feasible trajectory. A feasible trajectory would provide a good initial guess to the aforementioned methods and could allow to include time as a variable for mixed-integer problems that try to compute the optimal polytope traversal order[@deits2015efficient]. Furthermore, the efficient computation of a good initial guess is critical for the performances of sampling-based rejection methods that are only interested in the feasibility rather than the optimality to solve more complex problems [@tsounis2020deepgait; @tonneau-TRO18].

## Contribution

We observe that when the proportion of the trajectory spent in each polytope is specified, the PT problem can be formulated as a convex Quadratically Constrained Quadratic Program (QCQP). This allows the simultaneous computation of the path and the total time of the trajectory. This formulation can be obtained by representing the trajectory as a Bezier curve of arbitrary degree and exploiting its De Casteljau decomposition. The formulation guarantees a minimum time trajectory for the given distribution.

To evaluate the success rate of our framework, we semi-randomly generate PT problems. To identify problems that admit a solution, we implement an evolutionary strategy that efficiently samples the proportion of the trajectory spent in each polytope. The CMA-ES algorithm that we use does not scale well as the number of polytopes grows but provides satisfying performances for problems with less than 5 polytopes, which are those that we target.

We propose two contributions that advance the state of the art with respect to this objective:

- A convex formulation of the Polytope Traversal (PT) problem that simultaneously computes a path and its time parametrisation for the polytope traversal problem. The formulation is conservative but guaranteed to converge to locally optimal feasible solutions.

- An evolutionary algorithm that exploits our convex formulation to find a better minimum time trajectory, in addition to determining the feasibility of a problem.

Our formulation and implementation are efficient (less than 100 ms are required to solve problems with less than 10 polytopes), and work in arbitrary dimension with polynomials of arbitrary degree. Our code is implemented using the NDCurves library [@ndcurve] and is entirely open source.

In the remainder of this paper, we first recall important notions on Bezier curves and provide additional definitions (Section [2](#sec:def){reference-type="ref" reference="sec:def"}). We then formalise the PT problem (Sections [3](#sec:polytope){reference-type="ref" reference="sec:polytope"} and [4](#sec:problem){reference-type="ref" reference="sec:problem"}), before deriving a convex formulation of it (Section [5](#sec:convex){reference-type="ref" reference="sec:convex"}) and presenting our evolutionary strategy (Section [6](#sec:cma){reference-type="ref" reference="sec:cma"}). After presenting our experiments (Section [7](#sec:impl){reference-type="ref" reference="sec:impl"}) we discuss the results obtained (Section [8](#sec:discussion){reference-type="ref" reference="sec:discussion"}).

# Preliminaries {#sec:def}

## A reminder on Bezier curves

We first recall relevant properties of Bezier curves [@de1959courbes].

### Trajectory as a Bezier curve {#trajectory-as-a-bezier-curve .unnumbered}

We define a trajectory $\mathbf{x}(t) , t \in [0,T]$ as a polynomial of arbitrary degree $n$ that takes its values in $\mathbb{R}^{dim}$, with $dim$ the dimension of the problem, $T \in \mathbb{R}^+$ the duration of the trajectory and $t$ a time parameter. Any polynomial can be written as a Bezier curve of the same degree $n$:$$\begin{equation*}
\label{eq:contribution:bezier_generic}
\mathbf{x}(t) =   \sum_{i=0}^n B_i^n(t / T) \mathbf{x}_i
\end{equation*}$$ where the $B_i^n$ are the Bernstein polynomials and the $\mathbf{x}_i$ are the $n+1$ control points of the curve. We also define the vector $\mathbf{x}= [\mathbf{x}_0, \dots, \mathbf{x}_n]$ that contains all the control points. The main variables of our problem will be the control points $\mathbf{x}$ and the total time $T$.

The control points of any derivative of a Bezier curve are expressed as a linear combination of its control points. We note their expression for the velocity $\dot{\mathbf{x}}(t)$ and acceleration $\ddot{\mathbf{x}}(t)$ curves of concern to us: $$\begin{flalign*}
\dot{\mathbf{x}}(t) =   \sum_{i=0}^{n-1} B_i^{n-1}(t / T) \mathbf{D}^1_i\frac{\mathbf{x}}{T} \\
\ddot{\mathbf{x}}(t) =   \sum_{i=0}^{n-2} B_i^{n-2}(t / T) \mathbf{D}^2_i\frac{\mathbf{x}}{T^2}
\end{flalign*}$$

with the $\mathbf{D}^1_i$ and $\mathbf{D}^2_i$ constant matrices of appropriate size.[^2]\

### Curve decomposition with the De Casteljau algorithm {#curve-decomposition-with-the-de-casteljau-algorithm .unnumbered}

$\forall t_c \in [0,T]$ there always exists a decomposition of a Bezier curve into two curves $\mathbf{x}(t)^0$ and $\mathbf{x}(t)^r$ such that:

$$\begin{flalign*}
\forall t \in [0, t_c], \mathbf{x}^0(t) = \mathbf{x}(t) \\ 
\forall t \in [t_c, T], \mathbf{x}^r(t) = \mathbf{x}(t)
\end{flalign*}$$

The continuity between the curves is $\mathcal{C}^\infty$ and their degree is also $n$. The curves are given by the De Casteljau algorithm and their control points are, as for the derivatives, obtained as a linear combination of control points of $\mathbf{x}(t)$:

$$\begin{flalign*}
\label{castel}
\forall i \in \{0, \dots, n\}, \mathbf{x}^0_i = \mathbf{C}^0_i\mathbf{x}\\ 
\forall i \in \{0, \dots, n\}, \mathbf{x}^r_i = \mathbf{C}^r_i\mathbf{x}
\end{flalign*}$$

with $\mathbf{C}^{\{0,r\}}$ constant matrices of appropriate size. Any sub-curve can be decomposed with the same guarantees.

## Linear constraint definitions

We now detail how any constraint considered can be written in as a linear combination of the control points $\mathbf{x}$.

### Convexity properties of Bezier curves {#convexity-properties-of-bezier-curves .unnumbered}

A Bezier curve is entirely contained in the convex hull of its control points: $\forall t \in [0,T], \mathbf{x}(t) \in conv(\mathbf{x}_0, \dots, \mathbf{x}_n)$, where $conv$ denotes the convex hull operation. Therefore, a sufficient condition to verify any constraint of the form $$\begin{equation*}
  \forall t, \mathbf{B} \mathbf{x}(t) \oplus \mathbf{b}
\end{equation*}$$ with $\mathbf{B}$ and $\mathbf{b}$ constant matrix and vector of appropriate size and $\oplus$ describing either an equality ($=$) or inequality ($\leq$) constraint, is to simply verify $$\begin{equation*}
 \forall i \in \{0, \dots, n\},  \mathbf{B} \mathbf{x}_i \oplus \mathbf{b}.
\end{equation*}$$ By stacking appropriately $n+1$ times $\mathbf{B}$ and $\mathbf{b}$ into the matrix $\mathbf{K}$ and vector $\mathbf{k}$, we can write the equivalent constraint:

$$\begin{equation}
\label{kin} \mathbf{K} \mathbf{x}\oplus \mathbf{k}
\end{equation}$$ Although the condition is not necessary it is commonly used due to its practical interest, the main advantage being that it guarantees continuously that the curve satisfies the constraints. The current alternative consists in discretising the curve and evaluating the constraint at those discrete points, as is commonly done in numerical optimisation. Our formulation works with either approach. In the remainder of the paper we assume that the continuous formulation holds.\

### Derivative constraints {#derivative-constraints .unnumbered}

The trajectory can be constrained with respect to velocity and / or acceleration.

The velocity can be linearly constrained by a set of linear equations $\mathcal{L} := \{\mathbf{x}\in \mathbb{R}^{dim} | \mathbf{L} \mathbf{x}\oplus \mathbf{l} \}$. We express the constraints in terms of the control points of $\dot{\mathbf{x}}(t)$: $$\begin{equation*}
 \forall i \in \{0, \dots, n-1\},   \mathbf{L} \mathbf{D}^1_i \frac{\mathbf{x}}{T} \oplus \mathbf{l}
\end{equation*}$$

We stack all the constraints in matrix and vector $\mathbf{V}$ and $\mathbf{v}$ of appropriate size to write the velocity constraints in a single block and multiply by $T$ on both sides to obtain:

$$\begin{equation}
 \mathbf{V} \mathbf{x}\oplus \mathbf{v} T \label{vel}
\end{equation}$$

We can proceed similarly for the acceleration constraints and obtain constraints of the form:

$$\begin{equation}
 \mathbf{A} \mathbf{x}\oplus \mathbf{a} T^2 \label{acc}
\end{equation}$$

### Geometric constraints {#geometric-constraints .unnumbered}

As shown in (Fig. [1](#fig:teaser){reference-type="ref" reference="fig:teaser"}), our trajectory is constrained by a sequence of $m+1$ polytopes $\mathcal{H}^j, j \in \{0, \dots, m\}$ defined as $$\begin{equation}
\label{H}\mathcal{H}^j := \{\mathbf{y} \in \mathbb{R}^{dim} | \mathbf{H}^j \mathbf{y} \leq \mathbf{h}^j\}
\end{equation}$$

with $\mathbf{H}^j$ and $\mathbf{h}^j$ constant matrix and vector.

## The CMA-ES algorithm {#the-cma-es-algorithm .unnumbered}

In this work we compare our method with the CMA-ES [@hansen2006cma] algorithm, which is our best available approximation of a ground truth that can be obtained with a reasonable amount of time. CMA-ES is a derivative free evolutionary algorithm that aims at finding a solution to an optimisation problem by sampling values of its variables. A population of samples is evaluated based on the cost function of the problem. A new population is the generated based on a stochastic variation of the best samples and this iterative process is repeated until a termination criteria is met.

# Handling of the polytope traversal constraints {#sec:polytope}

We make use of the De Casteljau algorithm to express the constraints requiring $\mathbf{x}(t)$ to belong to the polytopes $\mathcal{H}^j$, based on the following conservative assumption.

We define $s_j, 0 < s_j < 1$ the proportion of the total time spent by the trajectory $\mathbf{x}(t)$ in $\mathcal{H}^j$, such that $\sum_{j=0}^{m}s_j = 1$. Given the total time $T$, the time spent in $\mathcal{H}^j$ thus amounts to $T *  s_j$.

We define $\mathbf{s}= [s_0, \dots, s_m]$ and $s_{-1} = 0$.

By recursively applying the De Casteljau algorithm on our curves, we can define $m+1$ curves $\mathbf{x}^j, 0 \leq j \leq m$: $$\begin{flalign*}
\forall j \in \{0, \dots, m\}, t \in [s_{j-1}*T, s_{j}*T] \Rightarrow \mathbf{x}^j(t) = \mathbf{x}(t)
\end{flalign*}$$

All the control points of $\mathbf{x}^j(t)$ are expressed as linear combination of $\mathbf{x}$ as guaranteed by the De Casteljau algorithm.

We can now easily constrain a curve $\mathbf{x}^j(t)$ to its assigned polytope $\mathcal{H}^j$ by constraining each of its control point using equation ([\[H\]](#H){reference-type="ref" reference="H"}):

$$\begin{align*}
\forall i \in \{0, \dots, n\},  \mathbf{H}^j \mathbf{C}^j_i \mathbf{x}\leq \mathbf{h}^j
\end{align*}$$

Stacking all the constraints we obtain $m+1$ constraints of the form: $$\begin{flalign*}
\forall j \in \{0, \dots, m\}, \mathbf{G}^j \mathbf{x}\leq \mathbf{g}^j
\end{flalign*}$$

In summary, our trajectory is given by a Bezier curve of arbitrary degree. Assuming that the proportion of the time spent in each curve is given, every constraint of our problem has the form of ([\[kin\]](#kin){reference-type="ref" reference="kin"}), ([\[vel\]](#vel){reference-type="ref" reference="vel"}) or ([\[acc\]](#acc){reference-type="ref" reference="acc"}).

# Problem definition {#sec:problem}

The inputs of our Polytope Traversal problem are:

- the set of $m+1$ polytopes $\mathcal{H}^j$;

- the proportion variable $\mathbf{s}$;

- optionally, a set of initial and terminal constraints on $\mathbf{x}(t)$. They can be constraints on the initial / end positions with the form of ([\[kin\]](#kin){reference-type="ref" reference="kin"});

- optionally, a set of dynamics constraints in the form of either ([\[vel\]](#vel){reference-type="ref" reference="vel"}) or ([\[acc\]](#acc){reference-type="ref" reference="acc"}), possibly constraining the initial and terminal velocities / acceleration.

The objective is to find a minimum-time feasible trajectory $\mathbf{x}(t)$ satisfying all the constraints. Because $\mathbf{s}$ is fixed, the approach is conservative.

The general form of our problem is given by

$$\begin{align}
\label{eqn:TO}
\mathbf{find} \quad & \mathbf{x}, T & \\ 
\mathbf{min} \quad & T & \\
\mathop{\mathrm{\mathbf{s.t.}\,}}\quad &\mathbf{K} \mathbf{x}\oplus \mathbf{k}    \\
    \quad &\mathbf{V} \mathbf{x}\oplus \mathbf{v}T \label{tov}  \\
    \quad &\mathbf{A} \mathbf{x}\oplus \mathbf{a}T^2 \label{toa}
\end{align}$$ which is non-linear in the general case.

# Convexification of the PT problem {#sec:convex}

We first note that for instances where constraint ([\[toa\]](#toa){reference-type="ref" reference="toa"}) is missing, ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}) is a linearly constrained convex problem that can be solved with a Linear Program (LP) solver. In the case where ([\[tov\]](#tov){reference-type="ref" reference="tov"}) is absent, we can simply replace variable $T^2$ with a scalar variable $y$ and minimize it:

$$\begin{equation*}
\begin{aligned}
\mathbf{find} \quad & \mathbf{x}, y & \\ 
\mathbf{min} \quad & y & \\
\mathop{\mathrm{\mathbf{s.t.}\,}}\quad &\mathbf{K} \mathbf{x}\oplus \mathbf{k}    \\
    \quad &\mathbf{A} \mathbf{x}\oplus \mathbf{a}y 
\end{aligned}
\end{equation*}$$

in which case $T = \sqrt{y}$.

Otherwise, we need an additional assumption to make the problem convex[^3].

## An always feasible convex relaxation {#sec:feasi}

We add the additional constraint $T \geq 1$, needed for our following proof. This can easily be satisfied without loss of generality by scaling $T$ appropriately. We thus relax the problem ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}):

$$\begin{align}
\label{eqn:TORelax}
\mathbf{find} \quad & \mathbf{x}, T, y  &  \\
\mathbf{min} \quad & y - T& \\
\mathop{\mathrm{\mathbf{s.t.}\,}}\quad &\mathbf{K} \mathbf{x}\oplus \mathbf{k}  \notag \\
    \quad &\mathbf{V} \mathbf{x}\oplus \mathbf{v}T \notag \\
    \quad &\mathbf{A} \mathbf{x}\oplus \mathbf{a}y \notag\\
    \quad &T^2  \leq y \label{relax} \\
    \quad &T \geq 1 \notag
\end{align}$$

Problem ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}) is a Quadratically Constrained Quadratic Program (QCQP) [@Boyd:2004:CO:993483], which is convex as ([\[relax\]](#relax){reference-type="ref" reference="relax"}) is a quadratic convex constraint. If the velocity constraints include equalities, then the solution of problem ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}) is valid for ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}) if and only if constraint ([\[relax\]](#relax){reference-type="ref" reference="relax"}) is saturated, meaning that $T^2 = y$. Fortunately at the optimum this is always the case. We can also prove that the optimum of both problems is the same.

**Proof by contradiction:** We consider $T_{opt} \geq 1$, the global minimum time trajectory for problem ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}) and the optimal control points $\mathbf{x}_{opt}$. $\mathbf{x}= \mathbf{x}_{opt}$, $T = T_{opt}$ and $y = T_{opt}^2$ define a valid solution for problem ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}). Indeed, the constraints on ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}) are a relaxation of the constraints on ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}) with respect to $T$ and $\mathbf{x}$, such that any solution of ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}) is a solution to ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}).

Let $(T_{*}, y_*, \mathbf{x}_{*})$ be an optimal solution for ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}).

We thus have three cases to consider:

- Either $T_{*} = T_{opt}$. Then it is clear that the minimum value $y - T_{*}$ is achieved when $y_* = T_{opt}^2$. Therefore the two problems share the same optimum;

- Either $T_{*} < T_{opt}$. This means that the active constraint for $T$ in ([\[eqn:TO\]](#eqn:TO){reference-type="ref" reference="eqn:TO"}) is ([\[toa\]](#toa){reference-type="ref" reference="toa"}), implying that $y_* \ge T_{opt}^2$. In such case $T_{opt}^2 -  T_{opt} < y_* - T_{*}$, which contradicts the fact that $(T_{*}, y_*, \mathbf{x}_{*})$ is optimal;

- Either $T_{*} > T_{opt}$. As $y - T$ is bounded by the strictly increasing function $T^2 - T$ for $T \ge 1$, this means that $y_* -  T_{*} > T_{opt}^2 -  T_{opt}$, which contradicts again the fact that $(T_{*}, y_*, \mathbf{x}_{*})$ is optimal[^4].

As a result, the only admissible case is the one where $T_{*} = T_{opt}$ and $y_{*} = T_{opt}^2$.$\square$

# Evolutionary strategy {#sec:cma}

To test our approach we need a ground truth to determine the feasibility of the problems we consider. We implement the CMA-ES algorithm to sample values for the proportion variable $\mathbf{s}$, given as input to a slightly modified version ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}), where we add a slack variable $\alpha \in \mathbb{R}^+$ to the inequalities:

$$\begin{equation}
\begin{aligned}
\label{CMA}
\mathbf{find} \quad & \mathbf{x}, T, y, \alpha  & \\ 
\mathbf{min} \quad & y - T + w * \alpha& \\
\mathop{\mathrm{\mathbf{s.t.}\,}}\quad &\mathbf{K} \mathbf{x}\oplus \mathbf{k}  \notag  \\
    \quad &\mathbf{V}^\leq \mathbf{x}\leq + \mathbf{1} \alpha + \mathbf{v}^\leq T \notag  \\
    \quad &\mathbf{A}^\leq \mathbf{x}\leq + \mathbf{1} \alpha + \mathbf{a}^\leq y \notag \\
    \quad &\mathbf{V}^= \mathbf{x}= \mathbf{v}^=T \notag  \\
    \quad &\mathbf{A}^= \mathbf{x}= \mathbf{a}^=y \notag \\
    \quad &T^2  \leq y  \\
    \quad &T \geq 1 \notag
\end{aligned}
\end{equation}$$

with $w$ a large positive scalar and the $\mathbf{V}^{=,\leq}$ terms denote the lines of $\mathbf{V}$ that are equalities (respectively inequalities). The resulting problem is always feasible if the original problem admits a solution and the cost conveniently feedbacks information regarding the extent to which the constraints are violated to the upper level. We empirically observed that CMA-ES converges faster with this formulation.

# Implementation and experiments {#sec:impl}

Our code is entirely written in python, using the open source curve library NDcurves [@ndcurve]. NDcurves allows to compute automatically all the derivatives and the De Casteljau decomposition of the control variables.

The optimisation problems are solved using Gurobi [@gurobi], while the CMA-ES algorithm is solved using the pycma library [@hansen2019pycma]. Although we report favourable computation times our primary objective is to measure the success rate of our approach in terms of feasibility.

## Problem generation

We pseudo-randomly generate PT problems in 2D and 3D for which we check the feasibility using the CMA-ES algorithm. A problem consists in a sequence of $m+1$ polytopes where each polytope intersects the one after it (Fig. [1](#fig:teaser){reference-type="ref" reference="fig:teaser"}), as well as randomly sampled initial and terminal states along with randomly sampled velocity inequality constraints. The generation of the acceleration constraints is biased such that there is a probability $p = 0.4$ that deceleration along one or more axis is impossible. Such constraints are relevant for applications to legged locomotion [^5].

To determine a polytope we uniformly sample 10 points, compute their convex hull and translate the resulting polytope positively along the x direction and randomly along the others. The translation amount along x is equal to a random number multiplied by the index $j$ of the polytope. To ensure that the polytopes share an intersection a random point is sampled along a line segment of two randomly generated points in two consecutive polytopes, and added to both polytopes (Fig. [1](#fig:teaser){reference-type="ref" reference="fig:teaser"}).

The generation of the problem is obviously not a random process (which would be too inefficient). As a result the numbers presented here are not representative of all the instances of the PT problem. They are however shading a light on the potential benefits of the method.

## Testing variables

In our tests we vary the number $m+1$ of polytopes that must be traversed, as well as the degree of the Bezier curve $\mathbf{x}(t)$. The number of polytopes vary from 2 to 20, the degree from 2 to 20.

## Evaluation

For each selected pair (number of polytopes, degree of the trajectory curve $\mathbf{x}(t)$), we compute 100 feasible problems with the CMA-ES algorithm. Each feasible problem is tested against problem ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}). The ratio between the two numbers determine the success rate of the formulation.

We use two means of initialisation for the proportion variable $\mathbf{s}$. One option is to heuristically define $\mathbf{s}$ by computing the shortest geometric path (ignoring the derivative constraints) and using the ratio of distance of each segment associated with one polytope over the total distance as the allocated proportion for each polytope, as commonly done [@gao18]. The other option simply consists in an even distribution of the proportion spent in each polytope.

We also compute the success rate of a naive initialisation that allocates arbitrary large times to each polytope.

### Success rate interpretation

::::: {#fig:plot .figure latex-placement="!b"}
::: overpic
figures/plot
:::

::: caption
Averaged success rate of the different approaches as a function of the number of polytopes.
:::
:::::

::: tabular
\| P3mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| P2mm \| &\
& & & &\
Deg &N &**O**& Oh & N & O & **Oh** &N & O & **Oh** &N & O & **Oh**\
& 31 & 96 & 80 & 56 & 66 & 80 & 64 & 71 & 90 & 59 & 78 & 64\
10 & 31 & 94 & 77 & 62 & 80 & 85 & 63 & 80 & 85 & 75 & 83 & 88\
20 & 34 & 93 & 74 & 51 & 84 & 85 & 68 & 81 & 87 & 75 & 92 & 92\
:::

The success rates are reported in Table [\[tab:succ\]](#tab:succ){reference-type="ref" reference="tab:succ"}. We also present the success rate for each polytope, obtained by averaging the success rate according to the degree of $\mathbf{x}(t)$ in Fig. [2](#fig:plot){reference-type="ref" reference="fig:plot"}. We observe that our approach always outperforms the naive time allocation, but that the difference depends on the configuration of the scenarios.

For scenarios involving 2 or 3 of polytopes our approach is successful more than $80\%$ of the time in this context. These scenarios are those of particular interest for the CROC problem [@Fernbach:ccroc] and suggest that the method is particularly suited for such problems.

As the number of polytopes increases we observe that the minimum distance heuristic becomes almost immediately relevant. Our approach performs better with the heuristic for any number of polytopes above 2, while the success rate of the naive heuristic increases as well.

Likewise for small scenarios the degree of the curve has a limited influence on the success rate, suggesting that $\mathbf{s}$ is primarily responsible for determining the success of our approach. The degree of the curve plays a more determinant role as the number of polytopes increases.

As a conclusion, it appears that our approach is mostly relevant for scenarios involving a low number of polytopes, while providing for marginally superior results over the naive heuristic larger problems.

### Computation times

We report the computation time required to solve ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}), the naive Linear Program with fixed time allocation and CMA-ES in Fig. [3](#fig:comp){reference-type="ref" reference="fig:comp"}. For CMA-ES we report the computation time require to solve feasibility rather than the time to converge as the scales are not compatible. For the optimal problem, CMA-ES requires in average 3 seconds to converge for the smallest problems, one minute for handling problems with 10 polytopes and several minutes to handle scenarios with 20 polytopes.

Because our implementation is in Python the results are useful for comparing the approaches but leave significant room for improvement. Computation times inferior to 10 ms were counted at 10 ms. As expected, CMA-ES scales rapidly with the number of considered variables, but provides decent performances for relatively small problems to solve for feasibility. The naive approach and ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}) are similar problems in size, but the quadratic constraint makes the resolution of our approach slower, although the computation times remain comparable.

::::: {#fig:comp .figure latex-placement="!b"}
::: overpic
figures/comp
:::

::: caption
Computational performance of the methods averaged over 20 runs. The times given for CMA-ES are those required to find a feasible solution
:::
:::::

### Optimality

The naive approach involves excessive traversal times by definition, thus it is only relevant to compare the times found by ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}) and CMA-ES. We computed the average trajectory time to travel over scenarios comprising 2 and 5 polytopes and reported the results in Table [\[tab:optim\]](#tab:optim){reference-type="ref" reference="tab:optim"}. As expected, our approach does not provide optimal times but the values are in the same order of magnitude as the approximated optimum. Again, these results do not have statistical significance and are illustrative. Solving for feasibility remains our objective.

::: tabular
P4mm \| P2mm \| P2mm \| P2mm \| &\
&C &O& Oh\
& 24 & 33 & 28\
:::

# Discussion {#sec:discussion}

Our experiments demonstrate that there are scenarios where finding a feasible initial guess for the Polytope Traversal problem is not trivial. Those cases primarily involve a small number of polytopes with non-symmetric constraints on the derivatives. Our approach appears as a promising candidate for rapidly computing a feasible solution to such scenarios. Further research is required to demonstrate the interest of the approach for scenarios involving more polytopes. Indeed, it is quite possible that the reason why the naive approach performs better with larger sets of polytopes is mainly the result of the methodology to generate the problems, which may generate easier scenarios.

A strong advantage of the approach is that a problem instance can be solved in a single optimisation call. This makes it compatible with mixed integer solvers such as [@deits2015efficient; @tordesillas2019faster]. A significant part of the combinatorics could be removed by delegating the time and trajectory optimisation to ([\[eqn:TORelax\]](#eqn:TORelax){reference-type="ref" reference="eqn:TORelax"}), as it is guaranteed to provide the optimum for a given proportion allocation $\mathbf{s}$.

The proposed method also allows to provide convex approaches for locomotion [@Fernbach:ccroc] with a mean to handle time as a variable when planning for the motion of legged robots, without breaking the convexity, thus providing an exciting avenue of research.

# Conclusion

In this paper we proposed a conservative formulation of the Polytope Traversal problem that simultaneously computes the duration of the trajectory and the path it follows.

The method is convex and was proven to always converge to a locally optimal feasible solution. We have experimentally established the interest of the approach for generating feasible solutions over naive time allocation strategies.

Future work will investigate the possibilities offered by the approach in the context of robotics legged locomotion.

[^1]: Steve Tonneau is at the University of Edinburgh, Scotland.

[^2]: In this paper we often introduce similar matrices and vectors. For brevity we do not introduce specific variables to specify their size. The number of rows is always problem dependent while the number of columns is equal to the size of the variables.

[^3]: One can also observe that if no equality constraints appear in the velocity constraints and that the velocity bounds include the null velocity, the formulation can remain linearly constrained and solved with a LP solver.

[^4]: Note that we need the constraint $T \ge 1$ for this to be verified.

[^5]: For instance, when the center of mass of the robot projection on the ground is outside of the support region defined by the effectors in contact it becomes impossible to accelerate towards the support region.
