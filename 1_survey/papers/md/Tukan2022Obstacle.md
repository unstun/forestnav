---
citation_key: Tukan2022Obstacle
arxiv_id: 2203.04075
arxiv_url: https://arxiv.org/abs/2203.04075
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:19:22Z
origin: ai+web
reviewed: false
---

# Introduction

Path finding is one of the oldest problems in robotics. The goal of path planning is to find a feasible path from an initial state to a final state, that does not collide with any obstacles. The main challenge stems from the usually immense search space that is needed to explore, especially for the continuous problem. A common approach is to cleverly *sample* the state in hopes of finding a path. Indeed, sampling-based path planners, such as Rapidly-exploring Random Trees (RRTs) [@lavalle1998rapidly], and Probabilistic Road maps (PRMs) [@kavraki1996probabilistic], are a popular choice for path finding.

One limitation of sampling-based planners is that they allow sampling *inside* obstacles, potentially leading to computational waste. If the map contains very large obstacles, a path might not be found due to a limited number of iterations, or the convergence time of such path planners increases. The problem is further exacerbated when the obstacles are not known in advance. Mapping the obstacles out can be a considerable challenge on its own.

The goal of this paper is to provide a *pre-processing* algorithm that discovers obstacles and removes redundant areas from the state space, giving a form of *conscience* to any sampling-based path planner, for faster convergence and possibly shorter generated paths. It can potentially be used with any sampling-based path planning routine. The challenge lies in that, contrary to the more common setting, the locations and shapes of the obstacles are hidden, and must be inferred using a membership oracle. To do so, we efficiently bound the volume of an obstacle as soon as it is encountered, using the concept of a *coreset* for a given implicit body approximation.

:::: {#fig:tri .figure latex-placement="htb!"}
![](Tukan2022Obstacle_figs/trmap2.jpeg){width="\\linewidth"}

![](Tukan2022Obstacle_figs/trimap3.jpeg){width="\\linewidth"}

![](Tukan2022Obstacle_figs/tripam1.jpeg){width="\\linewidth"}

::: caption
Partitioning the free state space using our methods. See original maps at Fig. [8](#maps){reference-type="ref" reference="maps"}.
:::
::::

The novelty of our approach lies in excluding explored obstacles from the state space. This is by bounding each obstacle via a convex body using minimum calls to $\mathrm{oracle}$, and excluding the enclosing convex body from the state space. Our contribution is then threefold:

1.  We propose a coreset for approximating the minimum volume enclosing ellipsoid (MVEE), i.e., we suggest an algorithm that computes a small subset $S$ of a given (probably infinite) set $P\subseteq\ensuremath{\mathbb{R}}^d$, such that the volume $\mathrm{vol}(\mathrm{mvee}(P))$ of the MVEE of $P$ is larger by a factor of at most $(1+\varepsilon)$ of $\mathrm{vol}(\mathrm{mvee}(S))$ (Sec. [3.2](#sec:coreset-details){reference-type="ref" reference="sec:coreset-details"}).

2.  We then extend our result towards enclosing the ellipsoid by a simplex $C$ (which is an approximation to the convex hull of the set $P$) to exclude $C$ (sets of infeasible states) from $\mathcal{X}$; see full details in section [3.6](#covhullsec){reference-type="ref" reference="covhullsec"}.

3.  We define a novel technique for sampling from the new space which excludes the simplex $C$, by splitting the state space into regions using Delaunay triangulation (see Definition [6](#def:delaunay){reference-type="ref" reference="def:delaunay"}). Each region is chosen with probability proportional to the ratio of its volume. We then apply the sampling technique of the path planner from the region which has been chosen (from the previous sampling step); Fig. [1](#fig:tri){reference-type="ref" reference="fig:tri"} shows the triangulation of the obstacle-free state space using our methods, and Fig. [2](#fig:framework){reference-type="ref" reference="fig:framework"} sums up our methods illustratively.

## Background and related work

**The evolution of RRTs.** RRT-based algorithms were first proposed in [@lavalle1998rapidly; @lavalle2001randomized], and ever-since they were widely leveraged by the robotics community. To ensure asymptotic optimality (of the final path), RRT\* was suggested [@karaman2010incremental; @karaman2011sampling], where it allows the inclusion of optimization metrics to improve the quality of the obtained solutions as the number of samples goes to infinity. Later, Informed-RRT\* [@gammell2014informed] was proposed as an improvement, here, when a feasible path is found, the planner starts searching for the final solution in an elliptical region inside the configuration space. [@nasir2013rrt] combine path biasing with rewiring techniques to suggest the RRT\*-Smart algorithm, where, the main idea is to smooth and reduce the number of states in a founded path to its minimum number, and use these states as biases for further sampling. A numerous number of algorithms were suggested for improving RRT-based planners, giving rise to many variants [@islam2012rrt; @adiyatov2013rapidly; @sintov2014time; @naderi2015rt; @otte2016rrtx; @palmieri2016rrt; @lai2019balancing]. While most of these path planners aim to either shorten the path itself [@petit2021rrt], or to focus on certain areas leading to faster convergence [@gammell2014informed], it is hard to determine for a given map which path planner will perform better in terms of time or/and the length of the generated path.

**Coresets.** A coreset is (usually) a small weighted subset of the original input set that approximates a loss function for every feasible query up to a provable multiplicative error of $1 \pm \varepsilon$, where $\varepsilon\in (0, 1)$ is a given error parameter. The main idea is to be able to store data using small memory, and boost solvers by applying them on the coreset instead of the original data. Coreset was first suggested by [@agarwal2004approximating] in the context of computational geometry, and got increasing attention recently in various fields. For example in the context of machine learning machine learning [@lucic2015strong; @har2007maximum] coresets where suggested to improve the efficiency of widely used machine learning models such as regression [@huggins2016coresets; @munteanu2018coresets; @karnin2019discrepancy], matrix approximation [@maalouf2019fast; @feldman2010coresets; @sarlos2006improved; @maalouf2021coresets], clustering [@gu2012coreset; @bachem2018one; @jubran2020sets; @schmidt2019fair], $\ell_z$-regression [@cohen2015lp; @dasgupta2009sampling; @nearconvex; @sohler2011subspace], *SVM* [@har2007maximum; @tsang2006generalized; @tsang2005core; @tsang2005very; @tukan2021coresets], and decision trees [@jubran2021coresets]. In deep learning, the idea of coresets was leveraged for compressing deep neuronal networks [@baykal2018data; @liebenwein2019provable; @9464761], for robust training of neural networks against noisy labels [@mirzasoleiman2020coresets] and for speeding up models training time [@sinha2020small]. computational geometry and shape approximation [@agarwal2004approximating; @kumar2005minimum], and robotics [@feldman2013k; @nasser2020autonomous; @volkov2017machine] etc. For extensive surveys on coresets, we refer the reader to [@feldman2020core; @phillips2016coresets], and to [@jubran2019introduction; @maalouf2021introduction] for an introductory.

# Settings {#ProbStat}

We first introduce our setting and necessary assumptions.

**Obstacle.** We define an *obstacle* as a convex set in $\ensuremath{\mathbb{R}}^d$. Note that a non-convex shape may be treated as the union of (hopefully few) convex sets. We also assume that the obstacle is not too small, otherwise, there is no benefit to finding it, as (with high probability) we should not be sampling many times in it. More precisely, we assume that the obstacle contains a ball of radius $\varepsilon$, for a given error parameter $\varepsilon>0$.

**Oracle** is a binary function $\mathrm{oracle}:\ensuremath{\mathbb{R}}^d\to\left\{\mathrm{true},\mathrm{false}\right\}$ over the search space, where $\mathrm{oracle}(p)$ returns $\mathrm{true}$ if $p\in\ensuremath{\mathbb{R}}^d$ is inside an obstacle. For simplicity, we assume that a call to $\mathrm{oracle}$ takes $O(1)$ time, and focus on the asymptotic number of such query calls.

**Directional width.** The following definition is used to measure the width of an obstacle in a given direction. We denote by $\langle p,u \rangle$ the projection of the point $p\in \ensuremath{\mathbb{R}}^d$ on to the unit vector (direction) $u\in\ensuremath{\mathbb{R}}^d$.

::: definition
**Definition 1** ($\omega(P,u)$). *For an obstacle $P$, and for any unit vector $u\in\ensuremath{\mathbb{R}}^d$, let $P[u]=\arg\max_{p\in P} \langle p,u \rangle$ be the extreme point in $P$ along $u$, then $\omega(P,u)=\langle P[u]-P[-u],u\rangle$ is called the *directional width* of $P$ in the direction $u$.*
:::

**Obstacles separation.** We must assume some minimal distance between obstacles, otherwise, there is no hope to distinguish between them. To keep the number of parameters small, we use $\varepsilon$ and assume that we can expand an obstacle by a factor of $(1+\varepsilon)$ while not hitting other objects. Formally, for every unit vector (direction) $u\in\ensuremath{\mathbb{R}}^d$, every pair of obstacles $P$ and $Q$, and for every pair of points $p\in P$ and $q\in Q$ on these obstacles, the projection $\langle p,u \rangle$ of $p$ on $u$ has distance of at least $\varepsilon\omega(P,u)$ from the projection $\langle q,u \rangle$ of $q$ along $u$: $\forall p\in P:\forall q\in Q: |\langle q,u \rangle-\langle p,u \rangle|>\varepsilon\omega(P,u).$

# Method

Given a state space $\mathcal{X}$ that is composed of two sets $\mathcal{X}_{free}$ (the space of which the robot is allowed to pass in) and $\mathcal{X}_{obs}$ (the space that is covered by the obstacles), and a membership oracle $\mathrm{oracle}: \mathcal{X}\to \left\{0,1\right\}$ where for every $x \in \mathcal{X}$, $\mathrm{oracle}(x) = 0$ translates to $x \in \mathcal{X}_{\textbf{free}}$ and $1$ otherwise, the objective is to incrementally remove states from $\mathcal{X}$ that lie in $\mathcal{X}_{\textbf{obs}}$. The motivation is to assist the path planner cover more states in $\mathcal{X}_{\textbf{free}}$ to produce much better paths. This is extremely helpful when the obstacles are large and cover a lot of space. We apply our algorithm as a preprocessing step, a sketch of it is given as follows.

1.  $x :=$ a sampled point from $\mathcal{X}$. []{#sketch:step1 label="sketch:step1"}

2.  If $\mathrm{oracle}(x) = 0$ ($x\in \mathcal{X}_{\textbf{free}}$), then go-to [\[sketch:step1\]](#sketch:step1){reference-type="ref" reference="sketch:step1"} []{#sketch:step2 label="sketch:step2"}. Otherwise ($x\in \mathcal{X}_{\textbf{obs}}$), our algorithm is invoked as follows:

    1.  $O :=$ compute a simplex which bounds the obstacle that contains $x$ using minimal calls to $\mathrm{oracle}$. []{#step1ofouralg label="step1ofouralg"}

    2.  Remove the space that is covered by $O$ from the sampling space ($\mathcal{X}:= \mathcal{X}\setminus O$) and go-to Step [\[sketch:step1\]](#sketch:step1){reference-type="ref" reference="sketch:step1"} []{#step2ofouralg label="step2ofouralg"}

Note that our algorithm can also be applied on the fly during a normal run of the path planner, where the point $x$ from Step [\[sketch:step1\]](#sketch:step1){reference-type="ref" reference="sketch:step1"} is sampled during execution.

We define a convex hull of a set as follows:

::: {#def:convexHull .definition}
**Definition 2** (convex hull). *Let $P \subseteq \mathcal{X}$ be a (possibly infinite) set of points. Then, $\mathrm{conv}\left( P \right)$ is defined to be a subset of $P$ such that every $p\in P$ can be represent as a convex combination of the points in $\mathrm{conv}\left( P \right)$, i.e., for every $p \in P$, there exists $\Phi : \mathrm{conv}\left( P \right) \to [0,1]$ such that $\sum\limits_{q \in \mathrm{conv}\left( P \right)} \Phi(q) = 1$ and $p = \sum\limits_{q \in \mathrm{conv}\left( P \right)} \Phi\left( q \right) q$.*
:::

:::: {#fig:framework .figure latex-placement="htb!"}
![](Tukan2022Obstacle_figs/LIPTDNovel.png){width="\\linewidth" height=".4\\linewidth"}

::: caption
Framework illustration for $d=2$: (i) a point is sampled from an obstacle (the blue shape), (ii) compute a $2d=4$ external points along $d=2$ orthogonal directions (the edges of the red lines and green line), (iii) compute the ellipsoid (in yellow) which passes through the set of $2d=4$ external points, this is not the minimum volume enclosing ellipsoid but a crude approximation to it, (iv) iteratively update the ellipsoid until it admits an $\varepsilon$-approximation and finally (v) compute a bounding simplex with $O(d^{1.5}(1+\varepsilon))$ approximation towards the volume of the convex body.
:::
::::

**Problem statement.** Given an infinite set of points $P \subseteq \mathcal{X}$ which is accessed using a membership oracle $\mathrm{oracle}: \mathcal{X}\to \left\{0,1\right\}$, the objective is to find a set $C \subseteq P$, $v \in P$ and some $\alpha \in [1, d]$ such that $\mathrm{conv}\left( C \right) \subseteq \mathrm{conv}\left( P \right) \subseteq \mathrm{conv}\left( \alpha^{1.5}\left( C - v \right) + v \right).$

## Bounding obstacles - simple case: $d=1$[]{#sec1 label="sec1"}

In this section, we give an overview of our method's execution on a one-dimensional space (the interval between $0$ and $1$). In this case the obstacles are linear segments on a line, and $\mathrm{oracle}:[0,1]\to\left\{\mathrm{true},\mathrm{false}\right\}$ gets as input a scalar. While this scenario is not interesting by itself as there will be no path in the presence of an obstacle, it will help illustrate the main ideas of our core algorithm. Assume we sampled a point that lies inside the obstacle - the goal is to bound this obstacle in order to remove it from the sampling space (Steps [\[step1ofouralg\]](#step1ofouralg){reference-type="ref" reference="step1ofouralg"} and [\[step2ofouralg\]](#step2ofouralg){reference-type="ref" reference="step2ofouralg"}). Once an obstacle is hit, we would like to find the extreme points (edge) of this obstacle based on a point $p$ inside the obstacle. To do that, we run an exponential search (geometric sequence) of queries $p\pm 2^i\varepsilon$, where $i=1,2,3,\cdots$. Here we used both assumptions from Section [\[sec1\]](#sec1){reference-type="ref" reference="sec1"}: (i) that the minimum length of an obstacle is $\varepsilon$, and (ii) each obstacle can be expanded by a multiplicative factor of $1 + \varepsilon$ without hitting any other obstacles. These assumptions complete the correctness of the exponential search. The number of iterations until the oracle returns $\mathrm{false}$, i.e., the first query point outside the obstacle is at most $\ln(1/\varepsilon)$. Using this search, we obtain a point $q$ that is outside the obstacle and of distance at most $x$ from its edge, where $x$ is the length of the obstacle. We can then run a binary search on the interval between the outer point $q$ and the closest point to $q$ inside the obstacle that was returned by the oracle. An $\varepsilon$-precision of the actual extreme point of the object can be computed in additional $O(\ln(1/\varepsilon))$ queries to the oracle. We then repeat this binary search on each side of the obstacle. The above process computes an $\varepsilon$-approximation to the boundaries (convex hull) of the obstacle up to $\varepsilon$-error which serves as our coreset. It is easy to verify that the number of queries in each stage is minimal up to a constant factor that can be arbitrarily improved by changing the base of the log in the search.

## Active-Learning MVEE Coresets for $d \geq 2$ {#sec:coreset-details}

The one dimensional case $d=1$ is very simple and unique since every obstacle has exactly two boundaries or extreme points. Already in $d=2$ dimensions, each obstacle may have many extreme points. Thus, we need to use more clever techniques that are strongly related to the minimum volume enclosing ellipsoid, known as Löwner's ellipsoid.

::: {#thm:lowner .theorem}
**Theorem 3** (Löwner Ellipsoid [@ball1992ellipsoids]). *Let $L$ be a convex body in $\ensuremath{\mathbb{R}}^d$, let $v \in L$, and let $E$ be ellipsoid of minimal $d$-dimensional volume containing $P$ that is centered at $v$. Let $\frac{1}{d} \left( E - c \right) + c$ denote the shrinkage of $E$ by a factor of $\frac{1}{d}$ around its center $c$. Then $\frac{1}{d} \left( E - c \right) + c \subseteq L \subseteq E.$*
:::

In the following subsections, we present our technique for computing an $\varepsilon$-coreset with respect to the MVEE problem.

::: definition
**Definition 4** (coreset for MVEE [@kumar2005minimum][]{#coreelli label="coreelli"}[]{#MVEECoreset label="MVEECoreset"}). *For $\varepsilon>0$ and a set $X\subseteq\ensuremath{\mathbb{R}}^d$, the set $S\subseteq X$ is an *$\varepsilon$-coreset for the MVEE* (minimum volume enclosing ellipsoid) of $X$, if the volume $\mathrm{vol}(\mathrm{mvee}(X))$ of the MVEE of $X$ is larger by a factor of at most $(1+\varepsilon)$ from the volume $\mathrm{vol}(\mathrm{mvee}(S))$ of the MVEE of $S$, i.e., $\mathrm{vol}(\mathrm{mvee}(X))\leq (1+\varepsilon)\mathrm{vol}(\mathrm{mvee}(S)).$*
:::

Our MVEE coreset construction algorithm is based on three basic components: A) In Section [3.3](#sec:findetremepoint){reference-type="ref" reference="sec:findetremepoint"} we suggest an algorithm for finding an extremal point on the obstacle in a specific direction. B) At section [3.4](#sec:cudeaprox){reference-type="ref" reference="sec:cudeaprox"}, we crudely approximate the smallest enclosing ellipsoid of the obstacle, by utilizing the farthest ($2d$) points on the obstacle in a $d$ orthogonal directions, in order to construct a basis for the ellipsoid. C) Finally at Section [3.5](#sec:coresetforelip){reference-type="ref" reference="sec:coresetforelip"}, we iteratively update the ellipsoid from the previous step, using a variant of Algorithm 3 of [@kumar2005minimum] where points are accessed via an oracle.

## Finding extremal points of an implicit convex body {#sec:findetremepoint}

First, we give Algorithm [\[algtwo\]](#algtwo){reference-type="ref" reference="algtwo"} that gets as input a membership oracle, an error parameter $\varepsilon\in(0,1)$ a direction (unit vector) $u$, and a point $p$ inside an obstacle. It returns an $\varepsilon$-approximation to the farthest obstacle point $q=p+au$ from $p$ along $u$, i.e., $a$ is the supremum of the set $\left\{a\geq 0\mid \mathrm{oracle}(p+au)=\mathrm{true}\right\}$. This algorithm will serve as a key component in obtaining a crude approximation towards the convex hull of the infinite set of points.

**Overview of $\textsc{Farthest}(\mathrm{oracle},\varepsilon,u,p)$.** At Line [\[D1\]](#D1){reference-type="ref" reference="D1"}, we define an arbitrary orthonormal base of $\ensuremath{\mathbb{R}}^d$, whose last vector is $e_d=u$. For simplicity, assume that $d=3$ and $e_1, e_2, e_3$ are the $x$, $y$ and $z$-axis of $\ensuremath{\mathbb{R}}^3$ respectively. Line [\[D2\]](#D2){reference-type="ref" reference="D2"} defines a function that gets a point $(x,y)=(x_1,x_2)$ on the $xy$-plane and returns the height $f(x,y)$ of the highest obstacle point whose projection is $(x,y)$, i.e, the obstacle point $(x,y,z)$ with the maximum value of $z$. An $\varepsilon$-approximation $\tilde{f}(x,y)$ for $f(x,y)$ with respect to the obstacle can be computed using one-dimensional binary/exponential search along the $z$-axis, as explained in Section [\[sec1\]](#sec1){reference-type="ref" reference="sec1"}. The initial point is defined in Line [\[D4\]](#D4){reference-type="ref" reference="D4"} as the $(x,y)$-coordinates of the input point $p=(x,y,z)$. At Lines [\[D6\]](#D6){reference-type="ref" reference="D6"}--[\[D7\]](#D7){reference-type="ref" reference="D7"}, we compute the highest point whose projection is $(x_1,y)$ over every $x_1\in\ensuremath{\mathbb{R}}$, using $\tilde{f}$ above at the first iteration of the for loop. In the second (and in this example, last) iteration of the for loop, we compute the highest point $q$ whose projection is $(x_1,y_1)$ over every $y_1\in\ensuremath{\mathbb{R}}$. The height of this point is $z_1=\tilde{f}(x_1,y_1)$. We output this point $q=(x_1,y_1,z_1)$.

:::: algorithm
::: tabbing
**Input:** An oracle $\mathrm{oracle}$ over $\ensuremath{\mathbb{R}}^d$, an error parameter\
$\varepsilon\in(0,1)$, a unit vector $u\in\ensuremath{\mathbb{R}}^d$, and an obstacle point\
$p\in\ensuremath{\mathbb{R}}^d$, i.e, $\mathrm{oracle}(p)=\mathrm{true}$.\
**Output:** An $\varepsilon$-approximation to the farthest obstacle\
point from $p$ along $u$.
:::

[]{#D1 label="D1"}Compute an orthonormal base $e_1,\cdots,e_d$ of $\ensuremath{\mathbb{R}}^d$, such that $e_d=u$.\
Let $f:\ensuremath{\mathbb{R}}^{d-1}\to \ensuremath{\mathbb{R}}$ such that$f(x_1,\cdots,x_{d-1}):=\max_{\mathrm{oracle}(\sum_{i=1}^d x_ie_d)=\mathrm{true}}x_d.$[]{#D2 label="D2"}\
Compute a function $\tilde{f}:\ensuremath{\mathbb{R}}^{d-1}\to \ensuremath{\mathbb{R}}$ that returns an $(\varepsilon/d)$-approximation to $f(x)$ along $e_d$. []{#D3 label="D3"} Set $x_j:=\langle p, e_j \rangle$ for every $j \in [d-1]$ []{#D4 label="D4"}\
$x_d:=\tilde{f}(x_1,\cdots,x_{d-1})$\
$q := \sum_{i=1}^d x_i e_i$
::::

:::: algorithm
::: tabbing
**Input:** Ān oracle over $\ensuremath{\mathbb{R}}^d$, an error parameter $\varepsilon\in(0,1)$,\
an obstacle point $p\in\ensuremath{\mathbb{R}}^d$, i.e, $\mathrm{oracle}(p)=\mathrm{true}$.̄\
**Output:** Ā $O(2^{d})$-coreset $S$ for the obstacle.
:::

$Q:=\left\{(0,\cdots,0)\right\}$; $S\gets \emptyset$; $i:= 0$\
$S$
::::

:::: algorithm
::: tabbing
**Input:** Ān oracle over $\ensuremath{\mathbb{R}}^d$, an error parameter $\varepsilon\in(0,1)$,\
and an obstacle point $p$.\
**Output:** Ān $\varepsilon$-coreset $S$ for the obstacle.
:::

$\hat{S} :=$ [Approx-MVE-Coreset]{.smallcaps}($\mathrm{oracle},\varepsilon, p$)\
Let $L\in\ensuremath{\mathbb{R}}^{d\times d}$ and $c\in\ensuremath{\mathbb{R}}^d$ be the basis and center respectively of the MVEE of $\tilde{S}$\
$S:=\emptyset$; $c_1:=c$; $L_1:=L$; $Q_i:= L_1^TL_1$\
$S$[]{#C12 label="C12"}
::::

## Crude approximated MVEE using membership oracle {#sec:cudeaprox}

We now provide an algorithm which when given a membership oracle $\mathrm{oracle}$ and an obstacle point $p$, returns an $O(2^d)$-coreset $S$ to the minimum volume enclosing ellipsoid (MVEE for short) of the obstacle that contains the point $p$, using a small number of calls to $\mathrm{oracle}$. The error parameter $\varepsilon\in (0,1)$ defines the desired accuracy from the $\mathrm{oracle}$, during the calls to the algorithm $\textsc{Farthest}$.

**Overview of $\textsc{Approx-MVE-Coreset}(\mathrm{oracle},\varepsilon,p)$**. At Lines [\[B5\]](#B5){reference-type="ref" reference="B5"}--[\[B6\]](#B6){reference-type="ref" reference="B6"}, we compute the "leftmost" and "rightmost" points $u$ and $v$ inside the obstacle along a unit vector $x \in \ensuremath{\mathbb{R}}^d$. More precisely, it computes an $\varepsilon$-approximation to these points using the oracle and the procedure $\textsc{Farthest}$ that was previously described. We then add the points $u$ and $v$ to the coreset (Line [\[B7\]](#B7){reference-type="ref" reference="B7"}). At Line [\[B2\]](#B2){reference-type="ref" reference="B2"} we repeat the search on the orthogonal space of $Q$ which is iteratively updated at Line [\[B8\]](#B8){reference-type="ref" reference="B8"}.

## $\varepsilon$-coreset for the MVEE of an implicit convex body {#sec:coresetforelip}

In this subsection we describe our main technical result: an efficient construction of an $\varepsilon$-coreset with respect to the MVEE problem, using only a membership oracle. The construction is off-line in the sense that the space (and oracle) are unchanged over time, and the computation is not parallel. Our algorithm can work in parallel using the merge-and-reduce technique [@feldman2020core]. The algorithm gets as input a membership oracle, an error parameter $\varepsilon$ and an obstacle point $p \in \mathrm{oracle}$ ($\mathrm{oracle}(p) =$*true*), and returns an $\varepsilon$-coreset to the MVEE of a given implicit obstacle via reduction to a mixed-integer convex programming.

**Overview of $\textsc{MVE-Coreset}(\mathrm{oracle},\varepsilon,p)$.** The $i$th iteration of the for loop at Line [\[algmain:for\]](#algmain:for){reference-type="ref" reference="algmain:for"}, uses an ellipsoid that approximates the obstacle, centered at $c_i$ and is defined by the affine transformation (matrix) $L_i$. This ellipsoid is the MVEE of the current coreset $S$. The approximation is improved in Line [\[E1\]](#E1){reference-type="ref" reference="E1"} by adding a point $p_{i+1}$ to $S$. The point $p_{i+1}$ is computed in the $i$th iteration and is the farthest point in the obstacle from the current ellipsoid (defined by $L_i$ and $c_i$) vie the Mahalanobis distance. At Line [\[C12\]](#C12){reference-type="ref" reference="C12"} we output a $\varepsilon$-coreset for the MVEE of the obstacle.

## From ellipsoids to enclosing simplices {#covhullsec}

To simply the exclusion of obstacles from the state space, we further enclose our enclosing ellipsoid by a simplex; See Section [3.7](#HowtoSample){reference-type="ref" reference="HowtoSample"} for more details.

::: {#thm:boundsSimplices .theorem}
**Theorem 5**. *Let $P \subseteq \ensuremath{\mathbb{R}}^d$, be infinite set of points, and let $S \subseteq P$ such that $\mathrm{mvee}\left( \mathrm{conv}\left( S \right) \right) \subseteq \left( 1+\varepsilon \right) \mathrm{mvee}\left( \mathrm{conv}\left( P \right) \right).$ Let $E$ be $\mathrm{mvee}\left( \mathrm{conv}\left( S \right) \right)$ that is centered at some $v \in \mathrm{conv}\left( P \right)$. Let $C$ be the set of $2d$ vertices of the expanded ellipsoid $\sqrt{d} \left( E - v \right) + v$. Then, $\frac{1}{d^{1.5}} \left( \mathrm{conv}\left( C \right) - v \right) + v \subseteq \mathrm{conv}\left( P \right) \subseteq \mathrm{conv}\left( C \right).$*
:::

::: proof
*Proof.* By Theorem [3](#thm:lowner){reference-type="ref" reference="thm:lowner"}, it holds that $\frac{\left( 1 + \varepsilon \right)}{d} \left( E - v \right) + v \subseteq \mathrm{conv}\left( P \right) \subseteq \left( 1 + \varepsilon \right) \left( E - v \right) + v.$ By symmetry of $E$ around $v$, it holds by [@ball1992ellipsoids] that $\frac{1}{\sqrt{d}} \left( C - v \right) + v \subseteq E \subseteq C.$ Combining all of the inclusions above yields Theorem [5](#thm:boundsSimplices){reference-type="ref" reference="thm:boundsSimplices"}. ◻
:::

## How to sample? {#HowtoSample}

In the following, we will discuss our approach to removing obstacles from the state space to ensure no redundancy in repeated sampling from obstacles.

**Removing simplices from the state space.** Post to enclosing an obstacle with a simplex, we remove the simplex from the state space as follows. This objective is an easy task since we need to formulate the resulted state space. One way which we took to heart is to triangulate the resulted state space via constructing Delaunay triangulation.

**Region sampling.** Since we have regions that were generated via the construction of Delaunay triangulation on the state space, then the probability of sampling from any region is equal to its volume divided by the sum of volumes over every region in the triangulated state space $\mathcal{X}$.

**Sampling from inside a region.** Post to choosing some region (probabilistically), we apply the planner's own sampler on the region to obtain the next point for the planner.

**Upon discovering new obstacles.** We will enclose the obstacle by a simplex as discussed in the previous section. Instead of directly applying triangulation, we find the intersection between the simplex and the current regions that represent the Delaunay triangulation of the current state space $\mathcal{X}$. For this, we use the Gilbert--Johnson--Keerthi distance algorithm [@cameron1997enhancing] to find all intersecting regions with our new discovered simplex. We then remove our simplex from the intersecting regions followed by constructing the Delaunay triangulation on the result of such removal. This is faster than computing the Delaunay triangulation from scratch.

::: {#def:delaunay .definition}
**Definition 6** (Delaunay triangulation). *For a set $Q \subseteq \ensuremath{\mathbb{R}}^d$, A triangulation $T(Q)$ is a partitioning of the interior of the $\mathrm{conv}\left( Q \right)$ into simplices, the vertices of which are points in $Q$. A Delaunay triangulation for a set $Q$ is a triangulation $T(Q)$ such that no point in $Q$ is inside the circum-hypersphere of any simplex in $T(Q)$.*
:::

# Experimental Results {#sec:results}

## Boosting the performance of RRT-based path planners

::: center
:::

::: center
:::

In this section, we tested the effectiveness of our approach by improving $3$ variants of the RRT algorithm on $4$ different maps. The idea was to apply a single prepossessing on each map, to obtain improvements for all of the RRT variants, either in terms of path length or in terms of running time.

:::: {#maps .figure latex-placement="h"}
![](Tukan2022Obstacle_figs/map4.jpeg){#fig:map_c width="\\linewidth" height="60%"}

![](Tukan2022Obstacle_figs/map2.jpeg){#fig:map_d width="\\linewidth" height="60%"}

![](Tukan2022Obstacle_figs/map3.jpeg){#fig:map_a width="\\linewidth" height="60%"}

![](Tukan2022Obstacle_figs/maprect.jpeg){#fig:map_b width="\\linewidth" height="60%"}

![](Tukan2022Obstacle_figs/World.jpeg){#fig:univerise width="\\linewidth" height="60%"}

::: caption
Maps
:::
::::

### Unlimited steps experiments.

We ran the RRT algorithms for a large number of sampling iterations on the maps [3](#fig:map_c){reference-type="ref" reference="fig:map_c"} and [4](#fig:map_d){reference-type="ref" reference="fig:map_d"}, once with the vanilla sampling technique, and once with our sampling after applying the preprocessing. We compared the following:

::: enumerate*
the time needed for finding a solution, []{#att1 label="att1"}

the ratio percentage of sampled points from obstacle from the total number of samples, and finally []{#att2 label="att2"}

the length of the generated path. []{#att3 label="att3"}
:::

Each test was conducted across $20$ different trails, the mean and variance of [\[att1\]](#att1){reference-type="ref" reference="att1"}--[\[att3\]](#att3){reference-type="ref" reference="att3"} where reported at Table [\[table:mapc\]](#table:mapc){reference-type="ref" reference="table:mapc"} and [\[table:mapd\]](#table:mapd){reference-type="ref" reference="table:mapd"}. In the captions of each table, we refer to its corresponding map.

**Discussion.** Our proposed preprocessing technique has boosted the RRT algorithms while resulting in shorter paths from the start state to the goal state. There is a significant gap between our performance and the vanilla algorithms either in the time it took (e.g., on RRT and RRT\* in both tables [\[table:mapc\]](#table:mapc){reference-type="ref" reference="table:mapc"} and [\[table:mapd\]](#table:mapd){reference-type="ref" reference="table:mapd"}) or in the path size (e.g., on RRT Dubins at Table [\[table:mapd\]](#table:mapd){reference-type="ref" reference="table:mapd"}).

This is because our preprocessing ensured that the sampler will only sample non-obstacle points. Thus, the generated tree by RRT and its variants will be larger in size and will contain much more informative paths between any two states. To illustrate the advantage of our approach, Fig. [9](#fig:trees){reference-type="ref" reference="fig:trees"} shows that our preprocessing done for the RRT algorithm leads to less sampling of points to attain a path from start to goal states than running plain sampling techniques.

### Performance under restricted number of steps

:::: center
::: {#table:map_a}
+----------------------+----------------+--------------------------+
|                      | $\%$ of wasted | Path length              |
+:==========:+:=======:+:==============:+:===============:+:======:+
| 4-5        |         | sampled points | mean            | std    |
+------------+---------+----------------+-----------------+--------+
| RRT        | Vanilla | $26$           | $\infty$        | nan    |
|            +---------+----------------+-----------------+--------+
|            | Our     | $\mathbf{0}$   | $\mathbf{1807}$ |        |
+------------+---------+----------------+-----------------+--------+
| RRT$\ast$  | Vanilla | $23$           | $\infty$        | nan    |
|            +---------+----------------+-----------------+--------+
|            | Our     | $\mathbf{0}$   | $\mathbf{1768}$ |        |
+------------+---------+----------------+-----------------+--------+
| RRT Dubins | Vanilla | $26$           | $1771$          |        |
|            +---------+----------------+-----------------+--------+
|            | Our     | $\mathbf{0}$   | $\mathbf{1757}$ |        |
+------------+---------+----------------+-----------------+--------+

: Results for map [5](#fig:map_a){reference-type="ref" reference="fig:map_a"}
:::
::::

:::: center
::: {#table:map_b}
+----------------------+----------------+--------------------------+
|                      | $\%$ of wasted | Path length              |
+:==========:+:=======:+:==============:+:===============:+:======:+
| 4-5        |         | sampled points | mean            | std    |
+------------+---------+----------------+-----------------+--------+
| RRT        | Vanilla | $25$           | $\infty$        | nan    |
|            +---------+----------------+-----------------+--------+
|            | Our     | $\mathbf{0}$   | $\mathbf{4416}$ |        |
+------------+---------+----------------+-----------------+--------+
| RRT$\ast$  | Vanilla | $26$           | $\infty$        | nan    |
|            +---------+----------------+-----------------+--------+
|            | Our     | $\mathbf{0}$   | $\mathbf{4404}$ |        |
+------------+---------+----------------+-----------------+--------+
| RRT Dubins | Vanilla | $14$           | $4553$          |        |
|            +---------+----------------+-----------------+--------+
|            | Our     | $\mathbf{0}$   | $\mathbf{4100}$ |        |
+------------+---------+----------------+-----------------+--------+

: Results for map [6](#fig:map_b){reference-type="ref" reference="fig:map_b"}
:::
::::

:::: {#fig:trees .figure latex-placement="htb!"}
![](Tukan2022Obstacle_figs/tree.jpeg){width="\\linewidth"}

::: caption
Left: the generated trees using vanilla RRT. Right: The tree generated using RRTs with our preprocessing.
:::
::::

In this experiment, we highlight the goal and motivation from which our methods have emerged. We operate under the assumption that the number of sampling iterations is restricted and small. Mostly, when using path planners, one can not know beforehand the number of iterations needed for generating successful paths from the initial state to the goal state. Most of such problems are handled via repetition where the number of iterations is either increased to ensure successful path generation or decreased for faster results. In such a context, we have observed that random sampling-based approaches don't take into account repeated samples inside an obstacle. Such observation leads to wastage in budget based sample path planners where the number of samples is crucial for the path planner. In addition, some path planners will take into account the entire budget of samples for generating all possible paths from state to goal states. Again, even in such path planners, wasting away samples will only lead to worse results compared to the case where wastage is prevented; see RRT Dubins at Table [1](#table:map_a){reference-type="ref" reference="table:map_a"}. To solve the path planning problem, one needs to come up with either an informative sampling technique or come up with a new path planner. Throughout the paper, we have chosen to be a plug-in component for path planners rather than providing new path planners.

**Discussion.** When presented with a limited number of sampling iterations, our proposed preprocessing technique ensured the existence of successful path generation over $20$ trials on multiple RRT-based planners, opposed to sampling "blindly"; see Table [1](#table:map_a){reference-type="ref" reference="table:map_a"} where $\infty$ represents the inability to generate a path.

### Method illustration

We refer the reader to Fig [10](#fig:rrtfly){reference-type="ref" reference="fig:rrtfly"} visualizing a classic run of RRT using our methods. Here, obstacles are bounded on the fly during the RRT run once we sample from them.

:::: {#fig:rrtfly .figure latex-placement="h"}
![](Tukan2022Obstacle_figs/accRRT.PNG){height=".2\\linewidth" width=".8\\linewidth"}

::: caption
Running our methods on the fly with RRT.
:::
::::

## Bounding Convex Shapes

To confirm our theoretical guarantees, we present the performance of our method for bounding convex shapes using an approximation towards the minimum volume enclosing ellipsoid. Our error $Err$ in which is stated in Algorithm [\[algfour\]](#algfour){reference-type="ref" reference="algfour"} is shown as a function of the number of iterations. We note that the results shown in Fig. [11](#fig:synthetic){reference-type="ref" reference="fig:synthetic"} have guaranteed almost an approximation of $1+\frac{1}{1001}$ to the *MVEE*.

:::: {#fig:synthetic .figure latex-placement="htb!"}
![](Tukan2022Obstacle_figs/shapeapprox2.jpeg){width=".9\\linewidth" height=".8\\linewidth"}

::: caption
Our method's performance on convex polygons.
:::
::::

## Map approximation

We conclude our experiments by showing how our method can be used to generate an approximated map, i.e., $(1+\epsilon)$-approximation to the real map. The map is represented as a 2D binary map such that white pixels represent free space, and black pixels represent obstacle points; see Fig. [7](#fig:univerise){reference-type="ref" reference="fig:univerise"}. To highlight our performance for the task of map approximation, we have used a few known algorithms:

::: enumerate*
The *A\** algorithm, and

the *RRT* algorithm.
:::

To ensure the highest coverage of the map, we ran the $A^\ast$ algorithm where start and goal states to be the leftmost lower and rightmost upper corners of the map, respectively. As for the *RRT* algorithm is run where the start state is at the center of the map; see Table [\[fig:map_approx\]](#fig:map_approx){reference-type="ref" reference="fig:map_approx"}.

[]{#fig:map_approx label="fig:map_approx"}

*$A*$* was not good enough to represent the real map as expected. On the other hand, RRT seems to be better at exploring the space of the map. However, even after $15,000$ queries where white spots represent obstacle points, there are still many blind spots that we cannot determine whether they are obstacle points or not. Finally, we note that in less than $15,000$, our algorithm presented an almost perfect mapping of the world.

# Proof Of Correctness

In this section, we prove our results via the following.

::: {#def:cencircS .definition}
**Definition 7**. *[@grotschel1988geometric] Let $X \subseteq \ensuremath{\mathbb{R}}^d$ be a convex set, and $\epsilon > 0$ be a real number. Let $S(K,\varepsilon) = \left\{x \in \ensuremath{\mathbb{R}}^d \mid \left\| x - y \right\|_2 \leq \epsilon \text{ for some } y \in X\right\},$ defines a ball of radius $\varepsilon$ around $X$. For a pair of positive real numbers $R > r > 0$, a positive integer $d \geq 2$, a convex body $X \subset \ensuremath{\mathbb{R}}^d$, and a point $a_0 \in X$, we denote by $(X;d,R)$ a circumscribed convex body such that $X$ is contained inside a ball of radius $R$ centered at the origin, and by $(X;d,R,r,a_0)$ a body that also contains a ball of radius $r$ centered at $a_0$; such body is referred to by the notion of *centered body*.*
:::

:::: {#def:memProb .definition}
**Definition 8**. *[@grotschel1988geometric Definition 2.1.14, Weak Membership Problem] Let $X \subseteq \ensuremath{\mathbb{R}}^d$ be a convex set, then given a vector $y \in \ensuremath{\mathbb{R}}^d$ and a rational number $\delta > 0$, either,*

::: enumerate*
*assert that $y \in S(X,\delta)$, or*

*assert that $y \not \in S(X,-\delta)$.*
:::
::::

:::: {#def:optProb .definition}
**Definition 9**. *[@grotschel1988geometric Definition 2.1.10, Weak Optimization Problem]Let $X \subseteq \ensuremath{\mathbb{R}}^d$ be a convex set, then given a vector $c \in \ensuremath{\mathbb{R}}^d$ and a rational number $\varepsilon$, either*

::: enumerate*
*finds a vector $y \in \ensuremath{\mathbb{R}}^d$ such that $y \in S(X,\varepsilon)$ and $c^Tx \leq c^Ty + \varepsilon$ for every $x \in S(K,-\varepsilon)$.*

*asserts that $S(X,-\varepsilon)$ is empty.*
:::
::::

:::: {#def:vioProb .definition}
**Definition 10**. *[@grotschel1988geometric Definition 2.1.11, Weak Violation Problem]Let $X \subseteq \ensuremath{\mathbb{R}}^d$ be a convex set, then given a vector $c \in \ensuremath{\mathbb{R}}^d$, a rational number $\gamma$, and a rational number $\varepsilon > 0$, either*

::: enumerate*
*assert that $c^Tx \leq \gamma + \varepsilon$ for all $x \in S(X,-\varepsilon)$ (i.e., $c^Tx \leq \gamma$ is almost valid), or*

*find a vector $y \in S(X,\varepsilon)$ with $c^Ty \geq \gamma - \varepsilon$ (a vector almost violating $c^tx \leq \gamma$).*
:::
::::

The following lemmas, help us in establishing our results:

::: {#lem:memToVio .lemma}
**Lemma 11**. *[@grotschel1988geometric Theorem 4.3.2]There exists an polynomial time algorithm that solves the weak violation problem for every centered convex body $(X;d,R,r,a_0)$ given by a weak membership oracle, in $\tau = \left( \frac{dRr}{\varepsilon}\right)^{O(1)}$ oracle calls.*
:::

::: {#lem:vioToOpt .lemma}
**Lemma 12**. *[@grotschel1988geometric Remark 4.2.5] There exists an oracle-polynomial time algorithm that solves the weak optimization problem for every circumscribed convex body $(X;d;R)$, given by a weak violation oracle $\tau = \left( \frac{dR}{\varepsilon}\right)^{O(1)}$.*
:::

Given a vector $u \in \ensuremath{\mathbb{R}}^d$ and $\varepsilon \in \ensuremath{\mathbb{R}}_+$, the following theorem shows that $\textsc{Farthest}$ yields a point which is far at most $\varepsilon$ from the farthest point in the convex set $X$ along $u$:

:::: {#thm:farProof .theorem}
**Theorem 13**. *Let $\varepsilon \in \ensuremath{\mathbb{R}}_+$ a real number and let $\mathrm{oracle}$ be a $\varepsilon$-weak membership oracle for a centered convex body $(X; d,R,r,a_0)$; see Definition [8](#def:memProb){reference-type="ref" reference="def:memProb"} and Definition [7](#def:cencircS){reference-type="ref" reference="def:cencircS"}. Let $u \in \ensuremath{\mathbb{R}}^d$ be a unit vector, $p \in \ensuremath{\mathbb{R}}^d$ an obstacle point, and let $\hat{x} \in X$ be the output of a call to $\textsc{Farthest}\left( \mathrm{oracle}, \varepsilon, u, p \right)$. Then the following hold:*

::: enumerate*
*$\left\| \hat{x} - \arg\max_{x \in X} u^Tx \right\|_2 \leq \epsilon$. []{#en:farGuar1 label="en:farGuar1"}*

*The number of calls to the oracle is $M=\left(\frac{drR}{\varepsilon}\right)^{O(1)}$. []{#en:farGuar2 label="en:farGuar2"}*
:::
::::

::: proof
*Proof.* The problem of finding the farthest point along a given direction in convex set, accessed implicitly via a polynomial membership oracle was addressed in [@grotschel1988geometric] and is known as the optimization problem. Since we are dealing with bit-complexity problems, we are interested in the weaker version of optimization problem; See Definition [9](#def:optProb){reference-type="ref" reference="def:optProb"}. By Plugging $\mathrm{oracle}$, $(X;d,R,r,a_0)$, $\epsilon$ into Lemma [11](#lem:memToVio){reference-type="ref" reference="lem:memToVio"}, we obtain a weak violation oracle. Hence, plugging the resulted oracle in Lemma [12](#lem:vioToOpt){reference-type="ref" reference="lem:vioToOpt"}, will attains a weak optimization oracle for a centered convex body $(X;d,R,r,a_0)$. We observe that by Definition [9](#def:optProb){reference-type="ref" reference="def:optProb"} and Lemma [12](#lem:vioToOpt){reference-type="ref" reference="lem:vioToOpt"}, plugging $u$ into $c$ and using $\epsilon$, will yield [\[en:farGuar1\]](#en:farGuar1){reference-type="ref" reference="en:farGuar1"} and [\[en:farGuar2\]](#en:farGuar2){reference-type="ref" reference="en:farGuar2"} at Theorem [13](#thm:farProof){reference-type="ref" reference="thm:farProof"}. ◻
:::

:::: {#mainthm .theorem}
**Theorem 14**. *Let $\mathrm{oracle}$ be a membership oracle for a convex set $X\subseteq\ensuremath{\mathbb{R}}^d$; see Definition [8](#def:memProb){reference-type="ref" reference="def:memProb"}. Let $p\in \ensuremath{\mathbb{R}}^d$ and obstacle point and let $S \subseteq \ensuremath{\mathbb{R}}^d$ be the output of a call to $\textsc{MVE-Coreset}(\mathrm{oracle}, \varepsilon, \hat{S})$. Then*

::: enumerate*
*$S$ is an $\varepsilon$-coreset for the minimum volume enclosing ellipsoid (MVEE) of $X$, and*

*if $\cfrac{\max_{x\in X}\left\| x \right\|_2}{\min_{y\in X}\left\| y \right\|_2}\leq r$, then $S$ can be computed in time $\tau=(\frac{dr}{\varepsilon})^{O(1)}$ and additional $\tau$ calls to $\mathrm{oracle}$.*
:::
::::

:::: proof
*Proof.* First, Algorithm 4.2 in [@todd2007khachiyan] computes a coreset $S$ and an ellipsoid $E$ as defined in Theorem [14](#mainthm){reference-type="ref" reference="mainthm"}, where $X$ is a finite set of $n$ points; see [@todd2007khachiyan Corollary 4.2]. Our Algorithm [\[algfour\]](#algfour){reference-type="ref" reference="algfour"} is the same up to few modifications: (i) we use the oracle to compute Algorithm [\[algfour\]](#algfour){reference-type="ref" reference="algfour"}, which is a subroutine of Algorithm [\[algthree\]](#algthree){reference-type="ref" reference="algthree"}. Algorithm [\[algfour\]](#algfour){reference-type="ref" reference="algfour"} computes the farthest point in $X$ along a given direction $u$, i.e., $\max_{x\in X}u^T x$. This problem can be solved in $O(\tau)$ time using membership oracle by combining Remark 4.2.5 and Theorem 4.3.2 from [@grotschel1988geometric]. (ii) At Line [\[probOpt\]](#probOpt){reference-type="ref" reference="probOpt"} of Algorithm [\[algfour\]](#algfour){reference-type="ref" reference="algfour"}, we compute the farthest point $p^{+}_{i+1}\in X$ from the ellipsoid that is defined by the matrix $L_i$ and is centered at the point $c_i$. In [@todd2007khachiyan] this was done using an exhaustive search over the finite set of points in $X$. In our case, we cannot use the oracle, as in case (i), since the desired function $\left\| L_i^T(p-c_i) \right\|_2$ that we need to maximize over $p\in X$ is convex. In fact, this is a quadratic optimization over a positive-definite matrix, which is known to be NP-hard [@murty1987some]. To this end, we use a relaxation and maximizes $\left\| L_i^T(p-c_i) \right\|_1$, i.e., change the $\ell_2$ to $\ell_1$ norm. Since $\sqrt{d}\left\| x \right\|_1\leq \left\| x \right\|_2\leq \left\| x \right\|_1$ for every $x\in\ensuremath{\mathbb{R}}^d$, we get a $\sqrt{d}$ approximation. The result is a mixed integer convex optimization problem that we can solve, obtaining an approximate solution. We now prove that we may change in Algorithm 4.2 in [@todd2007khachiyan], where we replace the farthest point by a point which may not be the farthest, but only up to a factor of $\sqrt{d}$ and still get the same result. The only difference is that the number of iterations increases by a factor of $d$.

Indeed, let $p \in \mathop{\mathrm{arg\,max}}_{x \in X} \left\| L^Tx \right\|_2$, and $p^\prime \in \mathop{\mathrm{arg\,max}}_{x \in X} \left\| L^Tx \right\|_1$, where $L \in \mathbb{R}^{d \times d}$ such that $Q = LL^T$. Our proof is essentially a variant of the original proof in [@kumar2005minimum]. If $p^\prime = p$ then we have found the desired point. Otherwise, denote $y^\prime =  L^Tp^\prime$ and $y =  L^Tp$. By the properties of $\ell_p$ norms, we have $\left\| y^\prime \right\|_2 \leq \left\| y \right\|_2 \leq \left\| y \right\|_1 \leq \left\| y^\prime \right\|_1 \leq \sqrt{d} \cdot \left\| y^\prime \right\|_2.$ Hence,$\frac{\left\| y \right\|_2}{\sqrt{d}} \leq \left\| y^\prime \right\|_2 \leq \left\| y \right\|_2$. Setting $\tilde{p} := \sqrt{d} p^\prime$ proves that $\tilde{p}$ is an approximation to the farthest point. Hence using the previous inequality and (36) of [@kumar2005minimum], we have $$\begin{equation}
\label{KtoEps}
k_i \leq \tilde{k}_i \leq d \cdot k_i,
\end{equation}$$ where $k_i = \left\| y \right\|_2^2$, $\tilde{k}_i = \left\| \sqrt{d} \cdot \tilde{y}\right\|^2$. We need to compute $\tilde{\varepsilon_i}$. To do so, let $\alpha_i \geq 0$ such that $\tilde{\varepsilon_i} = \alpha_i \cdot \varepsilon_i$, and we will establish upper and lower bounds on $\alpha_i$, using [\[KtoEps\]](#KtoEps){reference-type="eqref" reference="KtoEps"}. By the left side of [\[KtoEps\]](#KtoEps){reference-type="eqref" reference="KtoEps"}, $k_i = (1 + d) \cdot (1 + \varepsilon) \leq \tilde{k}_i =(1+d) \cdot (1+\alpha \varepsilon) \Rightarrow \alpha \geq 1.$ Using the right side of [\[KtoEps\]](#KtoEps){reference-type="eqref" reference="KtoEps"}, yields an upper bound on $\alpha_i$, $\tilde{k}_i = (1 + d) \cdot (1 + \alpha_i \varepsilon_i) \leq d \cdot k_i = d (1+d) \cdot (1 + \varepsilon_i)$. Thus, $\alpha_i \leq \frac{d \cdot (1 + \varepsilon_i) - 1}{\varepsilon_i}$ By [@kumar2005minimum], the ellipsoid method halts when the following inequality holds $\varepsilon_i \leq (1 + \varepsilon)^{\frac{2}{d+1}} - 1.$ Hence, $\alpha_i \leq d$. We have computed $\tilde{k}_i, \tilde{\varepsilon}$ to compute $\tilde{\beta}_i$. This term denotes the step size used to update the weights of the points. By (37) of [@kumar2005minimum] $\tilde{\beta}_i = \frac{\tilde{k}_i - (d + 1)}{(d + 1) \cdot (\tilde{k}_i - 1)} 
= \frac{(d+1)\cdot (1 + \tilde{\varepsilon}_i) - (d + 1)}{(d + 1) \cdot (\tilde{k}_i - 1)} 
= \frac{\tilde{\varepsilon}_i}{\tilde{k}_i - 1}$. Let $v_i$ denote the logarithm of the volume of the ellipsoid at the $i^{th}$ iteration. Hence, by plugging the previous equality into (40) of [@kumar2005minimum], we obtain $v_{i+1} = v_i + d \cdot \log{\left( 1 - \tilde{\beta}_{i}\right)} + \log{\left( 1 + \tilde{\varepsilon}_i \right)} 
= v_i + d \cdot \log{\left( 1 - \frac{\tilde{\varepsilon}_i}{\tilde{k}_i - 1} \right)} + \log{\left( 1 + \tilde{\varepsilon}_i \right)} 
= v_i + d \cdot \log{\left( \frac{d \cdot (\tilde{\varepsilon}_i + 1)}{d \cdot (\tilde{\varepsilon}_i + 1) + \tilde{\varepsilon}_i}\right)} + \log{\left( 1 + \tilde{\varepsilon}_i \right)} 
= v_i - d \cdot \log{\left(1 + \frac{\tilde{\varepsilon}_i}{d \cdot (\tilde{\varepsilon}_i + 1)} \right)} + \log{\left( 1 + \tilde{\varepsilon}_i \right)}$ Since $\tilde{\varepsilon}_i \geq 0$, we obtain that $$\begin{equation}
\label{EllipsVolPerIter}
\begin{gathered}
v_{i+1} \geq v_i - \frac{\tilde{\varepsilon}_i}{d \cdot (\tilde{\varepsilon}_i + 1)} + log{\left( 1 + \tilde{\varepsilon}_i \right)} \\
\geq v_i +
\begin{cases}
log(2) - \frac{1}{2} & \tilde{\varepsilon}_i \geq 1 \\
\frac{\tilde{\varepsilon}_i^2}{8} & \tilde{\varepsilon}_i < 1
\end{cases}
\end{gathered}
\end{equation}$$ where the inequality is based on $\log{\left( 1 + x\right)} \leq x$ where $x > -1$. By [\[KtoEps\]](#KtoEps){reference-type="eqref" reference="KtoEps"} and (41) in [@kumar2005minimum], we obtain that $\tilde{k}_0 \leq d\cdot k_0 \leq d (d+1) n$. Thus, $\tilde{\varepsilon}_0 \leq dn - 1$. Plugging this inequality and [\[EllipsVolPerIter\]](#EllipsVolPerIter){reference-type="eqref" reference="EllipsVolPerIter"} into (42) of [@kumar2005minimum], yields

::: enumerate*
$v_0 \geq -\infty$,

$v^\ast - v_i \leq (d+1) \log{\left( 1 + \tilde{\varepsilon}_i\right)}$,

$v_{i+1} - v_i \geq log{\left( 1 + \tilde{\varepsilon}_i \right)} -\frac{\tilde{\varepsilon}_i}{d \cdot (\tilde{\varepsilon}_i + 1)}$, and

[]{#ourDelta label="ourDelta"} $\delta_0 = v^\ast - v_0 \leq (d + 1) \cdot (\log{n} + \log{d})$.
:::

Hence by substituting $\varepsilon$ with $d \cdot \varepsilon$ in (44) in [@kumar2005minimum], we yield the desired approximation and the number of iterations needed is $\mathcal{O}\left( \frac{1}{\epsilon} \right)$. Plugging [\[ourDelta\]](#ourDelta){reference-type="ref" reference="ourDelta"} in (43) and in [@kumar2005minimum], yields that the maximum number of iterations, $K$, needed until the ellipsoid method converges is $K = d \cdot \log{\delta_0} \in O\left( d \cdot \left(\log{(d + 1)} + \log{(\log{n} + \log{d})}  + \frac{1}{\epsilon} \right) \right).$ ◻
::::

# Conclusion

We suggested a novel preprocessing technique that discovers obstacles in a map, to remove redundancies from the sampling space, and thus improve the running time and/or the final path length of different RRT-based planners. Such preprocessing step is done once. We bound each obstacle by its minimum enclosing ellipsoid once a point is sampled from it. Thus, one can find the smallest simplex which contains this ellipsoid, to exclude it from the sampling space. Following this step, a novel sampling technique is performed via the constrained Delaunay triangulation. Each of these steps is theoretically motivated, and supported by theorems and proofs. Finally, the experimental results match the theoretical contribution where the performance was clearly improved on a variate of space sampling based algorithms.

[^1]: All authors are with the Computer Science Department, University of Haifa, Haifa 3498838, Israel `{muradtuk, alaamalouf12, dannyf.post, roi.poranne}@gmail.com`

[^2]: This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible
