---
citation_key: K2025Asymptotically
arxiv_id: 2503.16164
arxiv_url: https://arxiv.org/abs/2503.16164
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:28:10Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Motion and Path Planning; Planning, Scheduling and Coordination
:::

# Introduction

::: {.figure latex-placement="!ht"}
  -------------------------------------------------------------- ----------------------------------------------------
   ![image](K2025Asymptotically_figs/star_563.3686097378923_gray-1.png){width="22%"}   ![image](K2025Asymptotically_figs/informed_554_gray-1.png){width="22%"}
                         RRT\*, cost 563                                       Informed-RRT\*, cost 554
         ![image](K2025Asymptotically_figs/PI-RRT_532_gray-1.png){width="22%"}          ![image](K2025Asymptotically_figs/convex_531_gray-1.png){width="22%"}
                        PI-RRT\*, cost 532                                        C-RRT\*, cost 531
  -------------------------------------------------------------- ----------------------------------------------------
:::

task of optimal path planning is to find a collision-free path with the lowest cost (e.g., path length) from a start configuration to a goal configuration. Low-dimensional configuration spaces can be discretized, and the optimal path can be searched using, e.g., A\*. Sampling-based motion planners, e.g., Rapidly-exploring Random Tree (RRT) [@lavalle1998rapidly], search the configuration space using randomized sampling, and they are more suitable for searching high-dimensional spaces than the discretization methods. RRT\* [@karaman2011sampling] is an asymptotically optimal variant of the RRT algorithm. RRT\* continues the search even after the first feasible solution is found. Moreover, RRT\* uses a rewiring technique to optimize node connection within the tree, so the costs of the nodes decrease with the increasing number of samples. The rewiring process relies on nearest-neighbor search, and it becomes more computationally intensive with the increasing size of the tree, which leads to the well-known slow convergence of RRT\* [@gammel2014informed; @armstrong2021rrt; @gammell2015batch].

RRT\* samples the whole configuration space (Fig. [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"}a), which is not necessary, as there exist states that cannot possibly improve the existing solution. This was first observed in [@gammel2014informed] where the "omniscient set" is defined. The omniscient set is a subset of the configuration space suitable for finding the optimal solution. In obstacle-free environments, it has a form of prolate n-dimensional hyperellipsoid. Drawing samples only from the hyperellipsoid has been shown to improve the convergence towards the optimal solution. However, for long zig-zag paths, the volume of the hyperellipsoid may still be too large, which causes Informed-RRT\* to perform similarly as RRT\* (Fig. [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"}a,b).

In this paper, we propose two approaches to approximate the omniscient set. The first proposed approach employs multiple small hyperellipsoids defined by subsections of the current best solution (Fig. [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"}c). This set ensures asymptotic optimality. The second approach computes a convex hull of a path rotated along a line from start to goal (Fig. [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"}d). Finally, we combine these two approaches and show how to achieve asymptotic optimality with them. We show how to efficiently sample these sets. Both approaches can be extended to higher dimensions. In comparison to state-of-the-art methods, the proposed approaches converge faster towards the optimal solution.

# Related Work

The family of sampling-based planners attempts to solve the path planning problem by randomized sampling of the configuration space. A popular method is RRT [@lavalle1998rapidly], and its variants [@verasSystematicLiteratureReview2019; @elbanhawiSamplingBasedRobotMotion2014b]. The original RRT provides a feasible solution, but it cannot guarantee finding the optimal solution.

In [@karaman2011sampling], asymptotically optimal sampling-based planners RRT\* and PRM\* were proposed. In RRT\*, the connection of the tree's nodes is optimized using a rewiring procedure to achieve near-optimal solutions. In contrast to basic RRT, where the tree growth is terminated if it reaches the goal configuration, RRT\* continues to grow (and rewire) the tree even after the first feasible solution is found. Various improvements of RRT\* were proposed: a) methods changing the sampling distribution, b) using multiple trees, c) improved rewiring procedures, and d) other techniques focusing on low-level routines. The surveys [@gammell2021asymptotically; @verasSystematicLiteratureReview2019; @orthey2023samplingbased; @noreen2016optimal] cover the contributions to the field of asymptotically optimal motion planning.

*Adapting the sampling distribution*. The original RRT\* samples the (whole) configuration space. As was shown in [@gammell2018informed; @gammel2014informed], not all configurations can improve the quality of the existing solution. Therefore, the sampling can be made within a subset of the configuration space. In Informed-RRT\* [@gammel2014informed], the authors define a set of configurations that can improve the path cost. Generally, this set is an n-dimensional prolate hyperspheroid. After the initial feasible solution is found, the random samples are generated from this subset. This reduces the volume of space to be sampled and improves the convergence rate. The BIT\* planner [@gammell2015batch] processes the samples of the hyperspheroid in batches: random samples are generated in the given area and processed (i.e., used for tree expansion) in the order given by a chosen heuristic. Cloud RRT\* [@donghyuk2014cloud] decomposes the search space by a set of spheres with various priorities and uses the spheres to generate random samples. Initially, the spheres are computed using a Generalized Voronoi Graph of the workspace and updated if a new, better path is found.

The work [@wang2020neural] employs a Convolutional Neural Network (CNN) to provide the sampling distribution. CNN is trained on a 2D map where optimal paths are computed using A\*, but due to representing the map as an RGB image, the method [@wang2020neural] is limited only to 2D configuration spaces. The works [@qureshiPotentialFunctionsBased2016; @fan2022uav] proposed to steer the new nodes of RRT\* towards the goal using the Potential Field method. In [@ichter2018learning], the sampling distribution is learned using a variational autoencoder from a set of successful motion plans. The learned distribution improves the convergence rate of BIT\*. The work [@wang2022gmr] uses the Gaussian Mixture model to learn the sampling distribution from human-demonstrated trajectories. RRT# [@arslan2013use] is a two-stage planner: exploration, which captures the topology of the space and extends the tree, and exploitation, which attempts to improve the current solution. Nodes having the potential to be a part of the optimal solution are estimated using available knowledge about the cost of the best path and cost-to-come values, which allows to focus the sampling to promising regions of the configuration space.

*RRT\* with multiple trees.* RRT\*-Connect employs the bidirectional search [@klemm2015rrt]: two trees are grown (from the start and goal), both in the RRT\* manner, and a new node extending one tree is also tested for extending the other tree. The work [@mashayekhi2020informed] combines Informed-RRT\* with the bidirectional search [@mashayekhi2020informed]. The bidirectional IB-RRT [@qureshi2015intelligent] estimates the best tree (and its best node) where to insert the random samples. The work [@strub2022adaptively] is based on BIT\* and uses the bidirectional backward and forward search. The backward search is fast as it checks collisions approximately, and its purpose is to estimate the heuristic. On the contrary, the forward search checks the collisions fully, grows in the BIT\* manner, and uses the heuristic from the backward search. The forward search informs the backward search about invalid (colliding) edges, so the heuristic is updated during the search.

*RRT\* with improved rewiring*. In RRT\*, parents for the newly added node are vertices in the hypersphere around the new node. Quick-RRT\*[@jeong2019quick] extends this set also to the ancestors of these vertices. F-RRT\* [@liao2021f] further extends this idea by creating new parent nodes instead of selecting them amongst nodes in the tree. T-RRT\* [@devaurs2016optimal] extends RRT\* by the transition test to prefer extension by nodes with lower costs.

*Improving low-level routines.* RRT\* performs a vast amount of collision checks, which can be computationally intensive. The paper [@hauser2015lazy] proposed to perform collision detection of edges only if a new path is computed. The work [@adiyatov2017sparse] associates obstacle proximity information with each node, and collision detection is computed only if the nearest neighbor is too far or if the node is close to obstacles. In memory-efficient RRT\* [@adiyatov2013rapidly], authors limit the maximum size of the tree, which is achieved by removing provably useless nodes every time a new node is added to the tree. The authors of [@armstrong2021rrt] extend RRT\* for the purpose of online path planning. Besides the standard Euclidean metric, the work [@armstrong2021rrt] employs a second assistive metric that helps to improve the convergence rate. An extension of the node expansion for kinodynamic systems without a BVP (Boundary Value Problem) solution was proposed in [@li2016asymptotically]. The tree is propagated using the forward system simulation. Moreover, the nodes are pruned based on their cost, which reduces the size of the trees and speeds up the nearest neighbor search.

In this paper, we focus on adapting the sampling space. The most relevant work is the Informed RRT\* [@gammel2014informed; @gammell2018informed] which defines the sampling space as a hyperellipsoid guaranteed to contain the optimal path. The hyperellipsoid is parametrized by the best (shortest) path found so far. The downside of [@gammel2014informed] is that when the current shortest path is too wiggly, the hyperellipsoid may be even bigger than the whole free configuration space. We propose several techniques to approximate the omniscient set [@gammell2018informed] and to focus the sampling to more relevant regions of the configuration space, as is demonstrated in Fig. [1](#fig:diferences){reference-type="ref" reference="fig:diferences"}.

# Problem Formulation

Let $\mathcal{C}$ denote the configuration space, and let $\mathcal{C}_{free}\subseteq \mathcal{C}$ denote the free region where the robot can move. A path $\mathcal{P}= (p_1, p_2,\ldots,p_n),\ p_i \in \mathcal{C}$ is a sequence of configurations. A subsection of the path is defined as a sequence $\mathcal{P}_{j,k} = (p_i),\ i=j,\dots,k,\ p_i \in \mathcal{P}$. The length of the path $\mathcal{P}$ is denoted $len(\mathcal{P})$, and it corresponds to the sum of distances between path elements $\sum_{i=2}^{n} ||p_{i-1}-p_{i}||$.

The task is to find the optimal (i.e., minimizing $len(\mathcal{P})$) collision-free path $\mathcal{P}_{opt} = (p_i),\ p_i \in \mathcal{C}_{free}$ from the start configuration $q_{start}\in \mathcal{C}_{free}$ to the goal region $Q_{goal}\subseteq \mathcal{C}$, i.e., $p_1 = q_{start}$ and $p_n \in Q_{goal}$. In the rest of the paper, $n$ refers to the cardinality of $\mathcal{P}$.

# The Motivation behind Proposed Methods

The original RRT and RRT\* algorithms sample the whole configuration space $\mathcal{C}$ uniformly. We define the sampling space $\mathcal{S}\subseteq \mathcal{C}$ as the region from which the random samples are drawn (i.e., in RRT and RRT\*, $\mathcal{S}=\mathcal{C}$). As was shown in [@gammell2018informed], only a subset of the configuration space contains samples that can possibly improve the cost of the path $\mathcal{P}$ (and it is guaranteed that samples outside this set cannot improve the cost of the path $\mathcal{P}$). This set is called the "omniscient set" $\mathcal{O}$: $$\begin{equation}
    \mathcal{O} = \{q|\ len(\mathcal{P}_{to}) + len(\mathcal{P}_{from}) \le len(\mathcal{P});\ q \in \mathcal{C}\},
\end{equation}$$

where $\mathcal{P}_{to}$ is a path from $q_{start}$ to a configuration $q$ and $\mathcal{P}_{from}$ is a path from a configuration $q$ to $q_{goal}$. The lengths of the paths can be approximated with a heuristic. The Euclidean distance heuristic would lead to the "informed set" $S_i$, which is a prolate hyperellipsoid $$\begin{equation}
    \mathcal{S}_{i} = \{q|\ \lVert q_{start}- q\rVert + \lVert q - q_{goal}\rVert \le len(\mathcal{P});\ q \in \mathcal{C}\}.
\end{equation}$$

To improve the length of the path, it is sufficient to draw random samples only from the informed set $\mathcal{S}_i$, as no configurations outside $\mathcal{S}_i$ can improve the cost of the path. This is the core of Informed-RRT\* [@gammel2014informed; @gammell2018informed] which draws random samples only from $\mathcal{S}_i$, and where the set $\mathcal{S}_i$ is defined using the length of the current best path.

However, the volume of $\mathcal{S}_i$ can still be quite high (especially for long zig-zag paths), which is depicted in Fig. [1](#fig:diferences){reference-type="ref" reference="fig:diferences"}. Moreover, it is not guaranteed that all configurations from the informed set $\mathcal{S}_i$ can improve the path.

:::: {#fig:diferences .figure latex-placement="htb"}
::: caption
Comparison of $\mathcal{C}_{free}$ (white) and the sampling spaces (blue).
:::
::::

The smaller the volume of $\mathcal{S}$, the less time will be spent sampling non-improving configurations. Ideally, the sampling space would be exactly the desired optimal path (i.e., $\mathcal{S}= \mathcal{P}_{opt}$). However, $\mathcal{P}_{opt}$ is not known in advance.

To reduce the number of samples that do not improve the solution, we propose several approaches to approximate the omniscient set $\mathcal{O}$, and we propose methods for their sampling.

# Locally Informed Sampling Space

The first proposed sampling space is a modification of $\mathcal{S}_i$ of Informed-RRT\* [@gammel2014informed]. Instead of constructing a hyperellipsoid from the whole path, many smaller hyperellipsoids are constructed from various subsections of the path. Each path subsection $\mathcal{P}_{j,k}$ has a corresponding hyperellipsoid $s_{j,k}$: $$\begin{equation}
    s_{j,k} = \{q|\ (\lVert q-p_{j}\rVert + \lVert q-p_{k} \rVert) \le len(\mathcal{P}_{j,k});\ q \in \mathcal{C};\},
\end{equation}$$ $s_{j,k}$ constructed in this manner is guaranteed to contain the shortest path from $p_{j}$ to $p_{k}$ as proven in the original Informed-RRT\* paper [@gammel2014informed], section III.

The Locally Informed Sampling Space, which we will denote $\mathcal{S}_{l}$, is the union of all local hyperellipsoids $s_{j,k}$, which satisfy constraints given by the parameter $c,\ 2 \le c \le n$: $$\begin{equation}
\label{eq:sl_def}
    \mathcal{S}_{l} = \bigcup_{\substack{j,k \; \in \; \{1, ..., n\} \\ k > j\;,\; k - j \ge c}} s_{j,k}.
\end{equation}$$

With $\mathcal{S}_l$, the sampling approach of Informed-RRT\* gets applied to parts of the current shortest found path, as can be seen in Fig [2](#fig:local){reference-type="ref" reference="fig:local"}.

:::: {#fig:local .figure latex-placement="h"}
![](K2025Asymptotically_figs/local.png){width="50%"}

::: caption
Visualization of one $s_{j,k}$ in blue on the path $\mathcal{P}$. []{#fig:local label="fig:local"}
:::
::::

The parameter $c$ controls the explore-exploit tradeoff. With the parameter $c=n$, sampling from $\mathcal{S}_l$ is equivalent to sampling from $\mathcal{S}_i$ (i.e., in the same manner as in the Informed-RRT\* planner). High values of $c$ lead to exploration, as the set $\mathcal{S}_l$ contains only the larger hyperellipsoids, and it supports the discovery of new alternative optimal solutions. In contrast, with the low values of $c$, the set $\mathcal{S}_l$ contains more small hyperellipsoids (computed from path subsections $\mathcal{P}_{j,k}$ of cardinality at least $c$), which leads to the exploitation of the current best solution (i.e., smoothing). Setting the parameter $c$ high (close to the $n$ of the initially found path) can lead to a premature halt of the smoothing and the use of $\mathcal{S}_i$ on a path not yet smoothed out.

In the following subsection, we show how to efficiently sample $\mathcal{S}_l$ without explicitly constructing all the hyperellipsoids, which would be computationally very demanding.

:::: {#fig:convex3d .figure latex-placement="!ht"}
::: caption
[]{#fig:convex3d label="fig:convex3d"} An example of the convex sampling space $\mathcal{S}_c$ for a path $P = (p_1, \ldots, p_5) = ((-3,0,0), (0,-2,-2), (2,2,0), (3,2,2), (5,0,0))$ (a). Sampling space $\mathcal{S}_c$ (visualized using the blue mesh) is defined by $\mathcal{P}$ rotated around the SG-axis (blue) (b). The path can be transformed using Eq. [\[eq:transf\]](#eq:transf){reference-type="ref" reference="eq:transf"} to a plane. The 2D convex hull of the transformed points defines the slice (blue polygon). The convex hull of the slice is described by $V = (v_1,\ldots, v_4)$ (c).
:::
::::

## Drawing random samples from $\mathcal{S}_l$ {#sub:local_sampling}

To draw a random sample from $\mathcal{S}_l$, a random length of the subpath $\mathcal{P}_{j,k}$ is selected from range $[c,n]$, then the beginning of the path $j$ is selected randomly, the ellipsoid $s_{j,k}$ is constructed, and the random sample is generated from this ellipsoid (similarly, as Informed-RRT\* does). The random sampling of $\mathcal{S}_l$ is summarized in Alg. [\[alg:loc\]](#alg:loc){reference-type="ref" reference="alg:loc"} (we use symbol $U(a,b)$ for uniform sampling in the inverval $[a,b]$). This procedure is repeated for each new random sample.

::: algorithm

------------------------------------------------------------------------

$size \gets U(c,\ |\mathcal{P}|) \in \mathbb{Z}$ $j \gets U(1, |\mathcal{P}|-size) \in \mathbb{Z}$ $k \gets j + size$ $path \gets (p_j, ..., p_k)$ $sample \gets informed\_sample(p_j,\ p_k,\ len(path))$ **return** $sample$
:::

# Convex Sampling Space[]{#sec:convex label="sec:convex"}

The second proposed sampling space is obtained as a convex hull of revolution of $\mathcal{P}$ around the axis connecting $q_{start}$ and $q_{goal}$ (we refer to this axis as the SG-axis (start-goal-axis) in the rest of the paper) (Fig. [\[subfig:3dpath\]](#subfig:3dpath){reference-type="ref" reference="subfig:3dpath"}, [\[subfig:3dsc\]](#subfig:3dsc){reference-type="ref" reference="subfig:3dsc"}). We denote this sampling space as $\mathcal{S}_c$. Computing $\mathcal{S}_c$ of the rotated path (a convex hull of an infinite set) would be complicated and unnecessary. Since the resulting hull is axially symmetric along the SG-axis, we can utilize that knowledge to represent $\mathcal{S}_c$ by a two-dimensional slice.

We can define a "slice" of the convex hull, which is an intersection of $\mathcal{S}_c$ and a plane going through the SG-axis (Fig. [\[subfig:scslice\]](#subfig:scslice){reference-type="ref" reference="subfig:scslice"}). Such a slice is two-dimensional, allowing us to represent $\mathcal{S}_c$ in 2D. A point inside the slice can be represented by the distance along the SG-axis and the distance from the axis to the point. Defining the slice and its coordinate system enables us to generate random points inside $\mathcal{S}_c$ by first drawing a random sample inside the slice and then distributing the sample into the volume of $\mathcal{S}_c$.

Let $A$ be the orthogonal projection matrix onto the SG-axis. For a configuration $q \in \mathcal{C}$, we define the distance along the SG-axis $a(q)$ and the distance from the axis $f(q)$ as $$\begin{equation}
\label{eq:dists}
    a(q) = \lVert o - Aq \rVert, \quad f(q) = \lVert q - Aq \rVert,
\end{equation}$$ introducing a transformation function $transf : \mathcal{C}\to \mathbb{R}^2$ $$\begin{equation}
\label{eq:transf}
    transf(q) = (a(q),\ f(q)).
\end{equation}$$

![The $\mathcal{S}_c$ transformed with the function $transf$ (Eq. [\[eq:transf\]](#eq:transf){reference-type="ref" reference="eq:transf"}) is equal to the convex hull of the set $V$, which is easier to compute. The $transf(\mathcal{P})$ is a transformation of the path from the Fig. [2](#fig:local){reference-type="ref" reference="fig:local"} []{#fig:repres label="fig:repres"} ](fig/2d_transf.pdf){#fig:repres width="80%"}

## Slice computation []{#sec:slicecomputation label="sec:slicecomputation"}

We project each configuration $p_i$ of the path $\mathcal{P}$ onto the SG-axis using $A$ and denote the first and the last projected configurations $o$ and $t$, respectively (the projections are ordered by their scalar projection on the SG-axis, i.e., according to their distance $a(\cdot)$ along the axis). Note that $transf(o) = (0,0)$. The coordinate system of the slice is depicted in Fig. [4](#fig:repres){reference-type="ref" reference="fig:repres"}.

**Computation of the slice**. Let $transf(\mathcal{P}\cup \{o,t\})$ denote a set of 2D points obtained by applying the transformation to each point of the path $\mathcal{P}$ and to the points $o$ and $t$. As all these points now lie on a 2D plane, we can compute their 2D convex hull and obtain the set of extremal points of the hull that we denote $V$. The points $v_i \in V$ then define the shape (polygon) of the slice, and the whole $\mathcal{S}_c$ would be achieved by rotating this polygon around the SG-axis. Computing the 2D convex hull of $m$ points (here, $m= n + 2$, i.e., number of waypoints plus two points $o$ and $t$) has time complexity $\mathcal{O}(m \log m)$. Practically, the method can be slightly sped up.

**Efficient computation of the slice.** The efficient computation of the convex hull of the slice points is based on a modified Graham scan [@GRAHAM1972132]. Graham scan decides whether the point lies within the hull (and therefore can not be an extremal point) by checking whether three consecutive points form a right or a left turn.

We modify the Graham scan using prior knowledge about the resulting hull of the set of points $V=transf(\mathcal{P}\cup \{o,t\})$. First, one edge of the convex hull is already known (it is the line segment $\overline{o,t}$). Second, all points are located only in one direction from this edge (all points of the slice have a positive $f(\cdot)$ value).

With the mentioned constraints, we can simplify the Graham scan as follows. Let $V=transf(\mathcal{P}\cup \{o,t\})$ and we sort points in $V$ by their $a(\cdot)$ values. As the set $V$ is sorted, we can define the previous point $v_p \in V$ and the following point $v_f \in V$ for a given point $v \in V$.

We can use the already known distance from the known edge (the $f(\cdot)$ value) and omit from $V$ all such points $v$ that are located between the known edge (SG-axis) and the line segment $\overline{v_p,v_f}$ since they lie inside the convex hull and can not be extremal. The algorithm for omitting non-extremal points of the two-dimensional convex hull is listed in Alg. [\[alg:scan\]](#alg:scan){reference-type="ref" reference="alg:scan"} and the process of deciding if a single point can be extremal is in Alg. [\[alg:in\]](#alg:in){reference-type="ref" reference="alg:in"}.

::: algorithm

------------------------------------------------------------------------

$V \gets \mbox{sort}\ V \mbox{ by scalar projection on SG-axis}$ $i \gets 2$
:::

::: algorithm

------------------------------------------------------------------------

$l \gets line\ segment\ from\ v_p\ to\ v_f$ $SG \gets line\ segment\ from\ q_{start}\ to\ q_{goal}$
:::

## Inlier query {#sub:inlier}

To check if a configuration $q \in \mathcal{C}$ lies inside $\mathcal{S}_c$, we construct set $R = \{transf(q)\} \cup V$ and order the elements of $R$ by their scalar projection into the SG-axis (i.e., according to their distance $a(\cdot)$ along the axis). Then we proceed to find $v_p~\in~R$ and $v_f~\in~R$ for the query configuration $q$. With these points, we can use Alg. [\[alg:in\]](#alg:in){reference-type="ref" reference="alg:in"} to decide whether $transf(q)$ lies inside the slice of $\mathcal{S}_c$. If $transf(q)$ lies inside the slice, then $q \in \mathcal{S}_c$.

## Drawing random samples from $\mathcal{S}_c$[]{#sec:sampl label="sec:sampl"}

We can sample the set $\mathcal{S}_c$ either directly or with rejection sampling. The rejection sampling approach is simple to implement but less efficient for high dimensional $\mathcal{C}$ or if the volume of $\mathcal{S}_c$ is low (in comparison to the volume of the whole $\mathcal{C}$). Sampling $\mathcal{S}_c$ in higher dimensions (or when the volume of $\mathcal{S}_c$ is low) can be efficiently achieved using the direct sampling.

*Rejection Sampling of $\mathcal{S}_c$*. Let $r \in \mathcal{C}$ be a random sample from $\mathcal{C}$, and $v' = transf(r)$. We accept the sample $r$ as being in $\mathcal{S}_c$ if the point $v'$ is located inside the 2D convex hull of the slice.

*Direct sampling of $\mathcal{S}_c$*. First sample $a'$ from interval $[0,\ \lVert o - t \rVert]$ (see definitions in subsection [\[sec:slicecomputation\]](#sec:slicecomputation){reference-type="ref" reference="sec:slicecomputation"}), the sampling should be weighted by $f_{max}$ ($2f_{max}$ is the width of the slice of $\mathcal{S}_c$ for a given value of $a(\cdot)$) at each $a'$. The sampled value of $a'$ determines the maximal value $f_{max}$ that $f'$ can obtain. Then, sample $f'$ uniformly from the interval $[0,\ f_{max}]$. This forms a random sample $g = (a',\ f')$. The random configuration $q \in \mathcal{C}$ is computed as: $q = a' \vec{d} + f' \vec{r}$, where $\vec{d}$ is a unit vector in direction from $q_{start}$ to $q_{goal}$, and $\vec{r}$ is a random unit vector perpendicular to $\vec{d}$. The reconstruction process is illustrated in Fig. [5](#fig:sampl){reference-type="ref" reference="fig:sampl"}.

:::: {#fig:sampl .figure latex-placement="h"}
![](K2025Asymptotically_figs/sampling.png){width="80%"}

::: caption
Direct sampling of the set $\mathcal{S}_c$. []{#fig:sampl label="fig:sampl"}
:::
::::

# Locally Informed Convex Sampling Space[]{#sec:combination label="sec:combination"}

The previously defined sampling spaces $\mathcal{S}_l$ and $\mathcal{S}_c$ can be combined; this leads to another sampling space $\mathcal{S}_{cl} = \mathcal{S}_l \cap \mathcal{S}_c$. While $\mathcal{S}_{c}$ will bring down the volume of the sampling space, $\mathcal{S}_{l}$ will put more weight on sampling in the proximity of the found path, locally smoothing out the fast converging solution. Example of the space $\mathcal{S}_{cl}$ is depicted in Fig. [6](#fig:combination){reference-type="ref" reference="fig:combination"}.

:::: {#fig:combination .figure latex-placement="h"}
![](K2025Asymptotically_figs/combination.png){width="80%"}

::: caption
An intersection of $\mathcal{S}_{c}$ and $\mathcal{S}_l$, denoted as $\mathcal{S}_{cl}$. []{#fig:combination label="fig:combination"}
:::
::::

## Drawing random samples from $\mathcal{S}_{cl}$ {#sec:space_scl}

To draw a random sample from $\mathcal{S}_{cl}$, first a random sample is generated in $\mathcal{S}_l$ (which is described in section [5.1](#sub:local_sampling){reference-type="ref" reference="sub:local_sampling"}), and the sample is accepted only if it is also located in $\mathcal{S}_c$ (which is realized using the Alg. [\[alg:in\]](#alg:in){reference-type="ref" reference="alg:in"}).

# Discussion

The proposed approximations of the omniscient set and methods for their sampling can be integrated into any RRT\*-based planner (instead of drawing random samples from the whole $\mathcal{C}$, the planner draws random samples from $\mathcal{S}_l$, $\mathcal{S}_c$ or $\mathcal{S}_{cl}$). Similarly to Informed-RRT\*, where the set $\mathcal{S}_i$ is updated when a new (shorter) path is found, the proposed sets $\mathcal{S}_l$, $\mathcal{S}_c$, and $\mathcal{S}_{cl}$ can be updated every time a new path is found.

Sampling from $\mathcal{S}_l$ (Section [5.1](#sub:local_sampling){reference-type="ref" reference="sub:local_sampling"}) is computationally not demanding. It only requires selecting a subsection of the current best solution and defining the hyperellipsoid using its first and last configurations. Therefore, sampling from $\mathcal{S}_l$ has the same complexity $\mathcal{O}(1)$ as sampling in Informed-RRT\*.

Drawing random samples from $\mathcal{S}_c$ (and also from $\mathcal{S}_{cl}$) is computationally more demanding. Every time a new solution is found, it is required to apply transformation in Eq. [\[eq:transf\]](#eq:transf){reference-type="ref" reference="eq:transf"} to all points of the current best solution $\mathcal{P}$ and to compute the convex hull as described in section [\[sec:sampl\]](#sec:sampl){reference-type="ref" reference="sec:sampl"}. The time complexity of the convex hull computation is $\mathcal{O}(n \log n)$ for a path $\mathcal{P}$ with $n$ waypoints. More frequent hull reconstruction will result in a faster decrease of $\mathcal{S}_c$ volume. However, reconstructing the hull too often can slow down the planning, without much improving the convergence. We observed that it is not necessary to construct $\mathcal{S}_c$ every time the current best solution is improved, but it is satisfactory to update it in every $m$ iterations (in our experiments, we used $m=1,000$).

The locally informed sampling space $\mathcal{S}_l$ enables more frequent sampling close to the current best-known path. The planners using $\mathcal{S}_l$ tend to have a faster convergence rate than ones using $\mathcal{S}_c$ in environments where less topologically distinct paths are present (for example, the Hard, Comb, and 3Dcomb environments) and slower in the opposite case. The $\mathcal{S}_{cl}$ can be used as a compromise when there is not enough information about the environment. Sampling from $\mathcal{S}_l$ preserves asymptotic optimality.

*Proof:* The equation ([\[eq:sl_def\]](#eq:sl_def){reference-type="ref" reference="eq:sl_def"}) is satisfied by all subpaths of cardinality from the interval $[c, n]$. Therefore, there are $n-c+1$ possible cardinalities of subpaths, including the whole path with the cardinality $n$. When generating a random sample from $\mathcal{S}_l$, we first randomly (uniformly) select a cardinality from the interval $[c,n]$ (Alg. [\[alg:loc\]](#alg:loc){reference-type="ref" reference="alg:loc"}). Therefore, with the probability $\frac{1}{n-c+1}$, we select the subpath of the cardinality $n$. The hyperellipsoid defined by $\mathcal{P}$ is $\mathcal{S}_i$. Therefore, when sampling from $\mathcal{S}_l$, we sample from $\mathcal{S}_i$ with probability $\frac{1}{n-c+1}$. In [@gammel2014informed] section III, it was proven that sampling of $\mathcal{S}_i$ leads to asymptotically optimal planning. Since sampling of $\mathcal{S}_i$ guarantees asymptotic optimality and we perform it with nonzero probability, sampling of $\mathcal{S}_l$ also guarantees asymptotic optimality. $\hfill \blacksquare$

On the contrary, the spaces $\mathcal{S}_c$ and $\mathcal{S}_{cl}$ do not guarantee to fully cover the omniscient set as $\mathcal{S}_i$ and $\mathcal{S}_l$ do, and drawing random samples only from these would result in a planner that does not ensure asymptotic optimality. Therefore, to ensure asymptotic optimality when using $\mathcal{S}_c$ or $\mathcal{S}_{cl}$, random samples should also be generated from $\mathcal{S}_i$ with a non-zero probability. This is an often adopted trick that combines Informed-RRT\* (which samples from $\mathcal{S}_i$) with other methods because the combination preserves asymptotic optimality.

:::: {#fig:search .figure latex-placement="htb"}
::: caption
The tree built using PI-RRT\* and C-RRT\* (sampling from $\mathcal{S}_c$), the set $\mathcal{S}_c$ is in blue. []{#fig:search label="fig:search"}
:::
::::

# Experiments and Results

The proposed approximations of the omniscient set (and their sampling) were implemented and integrated in state-of-the-art planners. A method with the prefix 'PI-' (partially informed) generates the random samples from $\mathcal{S}_l$ (Section [5.1](#sub:local_sampling){reference-type="ref" reference="sub:local_sampling"}), the prefix 'C-' (convex) denotes sampling from the convex hull $\mathcal{S}_c$ (Section [\[sec:sampl\]](#sec:sampl){reference-type="ref" reference="sec:sampl"}), and finally, the prefix 'PIC-' (partially informed convex) denotes the combination of 'PI-' and 'C-' methods $\mathcal{S}_{cl}$ (the procedure of generating the samples for 'PIC-' planners is described in [7.1](#sec:space_scl){reference-type="ref" reference="sec:space_scl"}). We integrated our approaches into RRT\* and BIT\* methods (e.g., PI-RRT\* is the RRT\* planner that generates the samples from $\mathcal{S}_l$).

The methods were tested on path planning for a rectangle object in four 2D environments (Comb, Hard, Wall, Maze) of size $500\times500$ (Fig. [9](#fig:2denvs){reference-type="ref" reference="fig:2denvs"}), i.e., in 3D configuration space as the robot can translate and rotate. The size of the object is $10\times10$ units in Comb, Wall, and Maze environments. The Hard environment (Fig. [\[fig:hard_tree\]](#fig:hard_tree){reference-type="ref" reference="fig:hard_tree"}) was designed specifically to pose a challenge to methods utilizing $\mathcal{S}_c$. In this case, the robot size is $50\times50$, and the environment contains two distinct homotopy classes (Fig. [8](#fig:2dhard){reference-type="ref" reference="fig:2dhard"}): one is the bottom 'zig-zag' path, and the other one is the top path. When the convex set $\mathcal{S}_c$ is computed from either path, it will not fully cover the other path. Therefore, the 'C-' planners should have a worse average performance in this case.

:::: {#fig:2dhard .figure latex-placement="htb"}
::: caption
The design of the Hard environment.
:::
::::

:::: {#fig:2denvs .figure latex-placement="htb"}
::: caption
The two-dimensional environments used, with a search tree and path generated using $\mathcal{S}_{c}$.
:::
::::

We also tested the performance in two 3D environments: Random (size $215\times215\times215)$, which is cluttered with many random obstacles, and 3D Comb (size $110\times160\times160$) containing walls. Planning was realized for a cubic robot of size ($10\times10\times10$). The 3D environments are depicted in Fig. [10](#fig:3denvs){reference-type="ref" reference="fig:3denvs"}. As the robot can rotate and translate in 3D, the path planning leads to a search in 6D configuration space.

:::: {#fig:3denvs .figure latex-placement="t"}
::: caption
3D environments, obstacles are in red, the goal region in green, and the robot (in $q_{start}$) in blue. []{#fig:3denvs label="fig:3denvs"}
:::
::::

We compared our planners (PI-RRT\*, C-RRT\*, PIC-RRT\*, PI-BIT\*, C-BIT\*, PIC-BIT\*) with state-of-the-art asymptotically optimal path planners from the OMPL benchmark [@OMPL]: Informed-RRT\*, RRT\*, RRTX [@Otte2014RRTXRM], RRT#. Despite OMPL also containing the BIT\* planner, we did not use it due to its poor performance. Therefore, we used our implementation of BIT\* (with batch size 1,000) for the comparison. We run each planner for $10^5$ iterations. In the case of 'PI-' planners, the random samples are drawn solely from the set $\mathcal{S}_l$, as this set ensures asymptotical optimality. In the case of planners with 'C-' and 'PIC-' prefix (i.e., drawing random samples from $\mathcal{S}_c$ and $\mathcal{S}_{cl}$, respectively), we also generated random samples from $\mathcal{S}_i$ with the the probability $10^{-5}$. Each planner was run 100 times in each planning scenario. The parameter $c$ was set to $5$, and goal region $Q_{goal}$ was represented by a box of size $10$ units in 3D environments and of size $5$ units in 2D environments, respectively.

::: {#tab:res_3D}
+:-------------------+:----------:+:-----:+:----:+:----------:+:-----:+:----:+
| Environment        | Random                    | 3Dcomb                    |
+--------------------+------------+-------+------+------------+-------+------+
| Planner            | Avg        | Std   | Mad  | Avg        | Std   | Mad  |
+--------------------+------------+-------+------+------------+-------+------+
| **C-RRT\***        | 347.03     | 3.65  | 1.44 | 201.48     | 6.51  | 2.74 |
+--------------------+------------+-------+------+------------+-------+------+
| **PIC-RRT\***      | **340.81** | 0.81  | 0.67 | 197.84     | 5.80  | 4.90 |
+--------------------+------------+-------+------+------------+-------+------+
| **PI-RRT\***       | 344.15     | 13.16 | 0.76 | 198.25     | 4.09  | 5.45 |
+--------------------+------------+-------+------+------------+-------+------+
| **PIC-BIT\***      | 340.85     | 1.42  | 1.00 | **197.11** | 4.13  | 2.09 |
+--------------------+------------+-------+------+------------+-------+------+
| **C-BIT\***        | 347.10     | 1.34  | 1.27 | 197.69     | 17.00 | 2.72 |
+--------------------+------------+-------+------+------------+-------+------+
| **PI-BIT\***       | 341.74     | 3.31  | 0.97 | 198.07     | 4.60  | 2.85 |
+--------------------+------------+-------+------+------------+-------+------+
| **BIT\***          | 348.37     | 4.74  | 2.61 | 200.55     | 1.16  | 1.02 |
+--------------------+------------+-------+------+------------+-------+------+
| **RRT#**           | 352.51     | 3.78  | 3.29 | 206.68     | 2.13  | 2.23 |
+--------------------+------------+-------+------+------------+-------+------+
| **Informed-RRT\*** | 349.45     | 4.10  | 3.11 | 204.28     | 2.95  | 3.08 |
+--------------------+------------+-------+------+------------+-------+------+
| **RRT\***          | 349.61     | 3.54  | 3.17 | 204.47     | 2.63  | 2.95 |
+--------------------+------------+-------+------+------------+-------+------+
| **RRTXstatic**     | 350.45     | 3.81  | 3.48 | 205.10     | 2.73  | 3.23 |
+--------------------+------------+-------+------+------------+-------+------+

: Length of path found by planners in 3D environments after ten seconds runtime.
:::

::: table*
+:-------------------+:----------:+:-----:+:----:+:----------:+:-----:+:-----:+:----------:+:------:+:------:+:----------:+:-----:+:----:+
| Environment        | Hard                      | Maze                       | Wall                         | Comb                      |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| Planner            | Avg        | Std   | Mad  | Avg        | Std   | Mad   | Avg        | Std    | Mad    | Avg        | Std   | Mad  |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **C-RRT\***        | 462.27     | 11.56 | 1.58 | 534.54     | 5.09  | 3.37  | **522.53** | 27.72  | 7.39   | 552.34     | 1.51  | 1.42 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **PIC-RRT\***      | 461.41     | 11.96 | 0.94 | 534.31     | 7.21  | 5.03  | 543.10     | 56.26  | 30.72  | 551.19     | 9.39  | 0.72 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **PI-RRT\***       | **458.98** | 10.33 | 0.41 | 551.18     | 16.35 | 16.75 | 593.59     | 120.25 | 53.80  | 553.67     | 10.96 | 0.69 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **PIC-BIT\***      | 462.43     | 12.80 | 0.95 | **533.82** | 7.92  | 3.93  | 544.20     | 54.25  | 33.37  | **550.53** | 6.29  | 0.75 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **C-BIT\***        | 464.35     | 13.31 | 1.28 | 534.80     | 4.68  | 3.60  | 523.87     | 34.19  | 5.39   | 552.03     | 1.23  | 1.25 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **PI-BIT\***       | 461.57     | 12.25 | 0.43 | 551.22     | 16.24 | 17.67 | 572.85     | 76.14  | 56.22  | 554.24     | 11.54 | 0.53 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **BIT\***          | 461.37     | 9.22  | 1.69 | 579.20     | 13.42 | 8.05  | 588.77     | 68.51  | 79.99  | 553.18     | 1.44  | 1.40 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **RRT#**           | 464.53     | 7.64  | 2.97 | 607.58     | 28.67 | 14.41 | 705.88     | 96.73  | 96.60  | 564.32     | 1.58  | 1.30 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **Informed-RRT\*** | 462.55     | 6.39  | 3.14 | 605.17     | 33.08 | 14.14 | 699.56     | 92.22  | 101.44 | 563.97     | 1.55  | 1.38 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **RRT\***          | 462.69     | 6.49  | 3.01 | 602.64     | 26.78 | 12.89 | 695.13     | 90.10  | 98.33  | 563.92     | 1.55  | 1.45 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
| **RRTXstatic**     | 463.10     | 6.77  | 2.98 | 604.89     | 28.66 | 14.54 | 699.23     | 90.04  | 99.68  | 564.05     | 1.57  | 1.40 |
+--------------------+------------+-------+------+------------+-------+-------+------------+--------+--------+------------+-------+------+
:::

The convergence graph in Fig. [11](#fig:3denvs_res){reference-type="ref" reference="fig:3denvs_res"} shows the performance of the state-of-the-art planners and our planner PIC-RRT\* in the Random 3D environment. For visibility reasons, we omitted the curves of our other planners from the graph. From the tested planner, PIC-RRT\* achieved the fastest convergence to the optimal solution.

The results achieved in the 6D configuration space are summarized in Tab. [1](#tab:res_3D){reference-type="ref" reference="tab:res_3D"}. The table shows the average path length (column 'Avg'), standard deviation (column 'Std'), and median absolute deviation (column 'Mad'). The proposed methods (the upper part of the table) found shorter paths at the given time (ten seconds of computation).

The performance (the convergence towards the optimal solution) of the planners in the Hard 2D environment is depicted in Fig. [12](#fig:2denvs_res){reference-type="ref" reference="fig:2denvs_res"}. The graph shows convergence curves for state-of-the-art planners and for our PI-RRT\* planner. We omitted our other planners ('PI-' and 'PIC-') from this graph due to visibility.

The length of the paths found by the tested planners in 2D environments is summarized in Tab. [\[tab:res_2D\]](#tab:res_2D){reference-type="ref" reference="tab:res_2D"}. The table shows the path length after six seconds of runtime (after this time, most of the planners do not improve their path length). The best average path lengths (shown in boldface in the table) were found by the proposed methods. In the tested environments, the start and goal can be connected using topologically distinct paths. In such cases, the first path found by the sampling-based planners may be different in each trial, and it may take a longer time to converge to the optimal one. This is indicated by the high standard deviation, especially for Maze and Wall environments, which contain many possible ways to connect the start and goal. Yet, our planners showed a smaller standard deviation in finding paths than the other methods. The progress of PI-RRT\* and C-RRT\* is visualized in Fig. [7](#fig:search){reference-type="ref" reference="fig:search"}.

In comparison to state-of-the-art planners, the C-RRT\* and C-BIT\* planners had the worst relative performance in the Hard environment, as expected. However, in other environments, sampling in the space $\mathcal{S}_c$ (C-RRT\* and C-BIT\*) enabled to find better paths than were found by other state-of-the-art planners.

![Convergence graph of methods in a randomly generated 3D environment.](K2025Asymptotically_figs/random_ompl_t_flat.png){#fig:3denvs_res width="80%"}

![Convergence graph of methods in the Hard environment.](K2025Asymptotically_figs/hard_ompl_t_flat.png){#fig:2denvs_res width="80%"}

In all tested 2D and 3D environments, the proposed methods outperformed the state-of-the-art planners: they have a faster rate of convergence and provide shorter paths.

# Conclusion

The well-known issue of asymptotically optimal path planning using RRT\* is its slow convergence towards the optimal path. In this paper, we have proposed novel methods to approximate the omniscient set, i.e., the subset of the configuration space that is known to contain samples that can improve the quality of the path. The first proposed approach uses multiple hyperellipsoids that are defined by a subsection of the current best path. In the second approach, we construct a convex hull of the current best path. We describe how to sample these spaces. The proposed methods can be integrated into any RRT\*-based planner. The experiments show the superior performance of our methods in comparison to the state-of-the-art planners from the OMPL benchmark.

::: thebibliography
10 url@samestyle

S. M. Lavalle, "Rapidly-exploring random trees: A new tool for path planning," *Research Report 9811*, 1998.

=plus 4minus S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *The International Journal of Robotics Research*, vol. 30, no. 7, pp. 846--894, 2011. \[Online\]. Available: https://doi.org/10.1177/0278364911406761

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Informed rrt\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic," in *2014 IEEE/RSJ International Conference on Intelligent Robots and Systems*, 2014, pp. 2997--3004.

D. Armstrong and A. Jonasson, "Am-rrt\*: Informed sampling-based planning with assisting metric," in *2021 IEEE International Conference on Robotics and Automation (ICRA)*.IEEE, 2021, pp. 10 093--10 099.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Batch informed trees (bit\*): Sampling-based optimal planning via the heuristically guided search of implicit random geometric graphs," in *IEEE international conference on robotics and automation (ICRA)*, 2015, pp. 3067--3074.

L. G. D. O. Veras, F. L. L. Medeiros, and L. N. F. Guimaraes, "Systematic Literature Review of Sampling Process in Rapidly-Exploring Random Trees," *IEEE Access*, vol. 7, pp. 50 933--50 953, 2019.

M. Elbanhawi and M. Simic, "Sampling-Based Robot Motion Planning: A Review," *IEEE Access*, vol. 2, pp. 56--77, 2014.

J. D. Gammell and M. P. Strub, "Asymptotically optimal sampling-based motion planning methods," *Annual Review of Control, Robotics, and Autonomous Systems*, vol. 4, pp. 295--318, 2021.

A. Orthey, C. Chamzas, and L. E. Kavraki, "Sampling-based motion planning: A comparative review," 2023.

I. Noreen, A. Khan, and Z. Habib, "Optimal path planning using rrt\* based approaches: a survey and future directions," *International Journal of Advanced Computer Science and Applications*, vol. 7, no. 11, 2016.

J. D. Gammell, T. D. Barfoot, and S. S. Srinivasa, "Informed sampling for asymptotically optimal path planning," *IEEE Transactions on Robotics*, vol. 34, no. 4, pp. 966--984, 2018.

D. Kim, J. Lee, and S.-e. Yoon, "Cloud RRT\*: Sampling cloud based RRT\*," in *IEEE International Conference on Robotics and Automation (ICRA)*, 2014, pp. 2519--2526.

J. Wang *et al.*, "Neural rrt\*: Learning-based optimal path planning," *IEEE Transactions on Automation Science and Engineering*, vol. 17, no. 4, pp. 1748--1758, 2020.

A. H. Qureshi and Y. Ayaz, "Potential functions based sampling heuristic for optimal path planning," *Autonomous Robots*, vol. 40, no. 6, pp. 1079--1093, Aug. 2016.

J. Fan *et al.*, "Uav trajectory planning in cluttered environments based on pf-rrt\* algorithm with goal-biased strategy," *Engineering Applications of Artificial Intelligence*, vol. 114, p. 105182, 2022.

B. Ichter, J. Harrison, and M. Pavone, "Learning sampling distributions for robot motion planning," in *2018 IEEE International Conference on Robotics and Automation (ICRA)*.IEEE, 2018, pp. 7087--7094.

J. Wang *et al.*, "Gmr-rrt\*: Sampling-based path planning using gaussian mixture regression," *IEEE Transactions on Intelligent Vehicles*, vol. 7, no. 3, pp. 690--700, 2022.

O. Arslan and P. Tsiotras, "Use of relaxation methods in sampling-based algorithms for optimal motion planning," in *2013 IEEE International Conference on Robotics and Automation*.IEEE, 2013, pp. 2421--2428.

S. Klemm *et al.*, "Rrt\*-connect: Faster, asymptotically optimal motion planning," in *2015 IEEE international conference on robotics and biomimetics (ROBIO)*.IEEE, 2015, pp. 1670--1677.

R. Mashayekhi *et al.*, "Informed rrt\*-connect: An asymptotically optimal single-query path planning method," *IEEE Access*, vol. 8, pp. 19 842--19 852, 2020.

A. H. Qureshi and Y. Ayaz, "Intelligent bidirectional rapidly-exploring random trees for optimal motion planning in complex cluttered environments," *Robotics and Autonomous Systems*, vol. 68, pp. 1--11, 2015.

M. P. Strub and J. D. Gammell, "Adaptively informed trees (ait\*) and effort informed trees (eit\*): Asymmetric bidirectional sampling-based path planning," *The International Journal of Robotics Research*, vol. 41, no. 4, pp. 390--417, 2022.

I.-B. Jeong, S.-J. Lee, and J.-H. Kim, "Quick-RRT\*: Triangular inequality-based implementation of RRT\* with improved initial solution and convergence rate," *Expert Systems with Applications*, vol. 123, pp. 82--90, 2019.

B. Liao *et al.*, "F-rrt\*: An improved path planning algorithm with improved initial solution and convergence rate," *Expert Systems with Applications*, vol. 184, p. 115457, 2021.

D. Devaurs, T. Siméon, and J. Cortés, "Optimal path planning in complex cost spaces with sampling-based algorithms," *IEEE Transactions on Automation Science and Engineering*, vol. 13, no. 2, pp. 415--424, 2016.

K. Hauser, "Lazy collision checking in asymptotically-optimal motion planning," in *2015 IEEE international conference on robotics and automation (ICRA)*.IEEE, 2015, pp. 2951--2957.

O. Adiyatov *et al.*, "Sparse tree heuristics for rrt\* family motion planners," in *2017 IEEE International Conference on Advanced Intelligent Mechatronics (AIM)*.IEEE, 2017, pp. 1447--1452.

O. Adiyatov and H. A. Varol, "Rapidly-exploring random tree based memory efficient motion planning," in *2013 IEEE international conference on mechatronics and automation*.IEEE, 2013, pp. 354--359.

Y. Li, Z. Littlefield, and K. E. Bekris, "Asymptotically optimal sampling-based kinodynamic planning," *The International Journal of Robotics Research*, vol. 35, no. 5, pp. 528--564, 2016.

R. Graham, "An efficient algorithm for determining the convex hull of a finite planar set," *Information Processing Letters*, vol. 1, no. 4, pp. 132--133, 1972.

I. A. Şucan, M. Moll, and L. E. Kavraki, "The Open Motion Planning Library," *IEEE Robotics & Automation Magazine*, vol. 19, no. 4, pp. 72--82, December 2012, https://ompl.kavrakilab.org.

M. W. Otte and E. Frazzoli, "Rrtx: Real-time motion planning/replanning for environments with unpredictable obstacles," in *Workshop on the Algorithmic Foundations of Robotics*, 2014.
:::

[^1]: Manuscript received: September, 16, 2024; Revised January, 2, 2025; Accepted January, 31, 2025.

[^2]: This paper was recommended for publication by Editor Aniket Bera upon evaluation of the Associate Editor and Reviewers' comments. This work was supported by the Czech Science Foundation (GAČR) under project No. 24-12360S, by the European Union under the project Robotics and advanced industrial production (no. CZ.02.01.01/00/22_008/0004590), and by CTU grant no. SGS23/177/OHK3/3T/13. Computational resources were provided by the e-INFRA CZ project (ID:90254), supported by the Ministry of Education, Youth and Sports of the Czech Republic.

[^3]: The authors are with the Faculty of Electrical Engineering, Czech Technical University in Prague, Czech Republic.

[^4]: Digital Object Identifier (DOI): see top of this page.
