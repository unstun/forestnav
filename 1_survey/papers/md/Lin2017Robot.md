---
citation_key: Lin2017Robot
arxiv_id: 1701.07549
arxiv_url: https://arxiv.org/abs/1701.07549
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:01:57Z
origin: ai+web
reviewed: false
---

# Introduction

The Coverage Path Planning (CPP) problem is to determine a path that passes through all points in a given geometric domain. It is a classical problem in robotics and motion planning and is of fundamental value to many applications that require a robot or multiple robots to sweep over the target area, such as vacuum cleaning robots, lawn mowers, underwater imaging/scanning robots, window cleaners, and many others.

In general the coverage path planning problem has multiple goals: full coverage (i.e., every point in the domain $\Omega$ is covered), no overlapping or repetition (no point is visited multiple times), and/or a variety of objectives on the simplicity or quality of the paths. Satisfying all such requirements is difficult if not impossible. Therefore priorities are often set on these possibly conflicting objectives and the goal is to obtain a good tradeoff.

The geometric shape of the domain to be covered is crucial in the design of coverage path planning algorithms. Simple shapes such as convex polygons can be covered by simple zigzag motion patterns (lawn mower patterns). Therefore, most algoritms for coverage path planning first decompose the target region into 'simple cells'. The cell decomposition can be represented by a cell adjacency graph in which each cell is a vertex and two vertices are connected if they share common boundaries. Within each cell we can use a simple zig-zag pattern and to cover the entire domain we need to visit each cell at least once.

In all the decomposition methods, there are two general issues that may affect the final performance. First we need to find a path on the cell adjacency graph that visits each cell at least once -- ideally exactly once (to keep the path short). Finding a path that visits each vertex of a graph exactly once is the well known Hamiltonian path problem, which is NP-hard [@Garey1990computers]. The adjacency graph may not admit a Hamiltonian path -- thus a robot may have to repeatedly visit some points just to get from one cell to the next cell. Second, all the algorithms above use the *extrinsic coordinate system*, i.e., the Euclidean coordinates representing the domain of interest. Such extrinsic coordinate systems, albeit being natural choices, are not the best to encode the complex geometric and topological features introduced by obstacles and boundaries. This is in fact the core challenge that the cell decomposition is mean to tackle. When the domain is not flat (e.g., on a terrain or as a general surface in 3D), the extrinsic coordinate system and the cell decomposition may lead to unnecessarily many pieces depending on the detailed implementation.

**Our Contribution.** In this paper we focus on solving this problem using a generic solution that is applicable to general surfaces in 3D. The novelty of our method is to abandon the extrinsic Euclidean coordinates system and adopt the *intrinsic coordinate system*, i.e., a global parametrization of the domain of interest. To get an idea, consider a standard torus, one can slice the torus open along the two generators of the fundamental group of the torus (See Figure [1](#fig:torus){reference-type="ref" reference="fig:torus"} as an example) and the torus can be flattened as a square. Thus, one can represent the points on the torus by a $uv$ coordinate system, where the $u$ coordinate represents the position of the point $p$ along one generator of the fundamental group and $v$ represents the position along the other generator. Both the geometry of the surface and the topology of the surface are inherently encoded in this new coordinate system. Finding a coverage path for the torus under the $uv$ coordinate system is now trivial -- one can simply zig-zag in the $uv$ coordinate system which becomes a spiral motion on the torus.

:::: {#fig:torus .figure latex-placement="t"}
![image](Lin2017Robot_figs/torus.png){width="0.5\\columnwidth"}![image](Lin2017Robot_figs/fundamental.png){width="0.5\\columnwidth"}

::: caption
The torus is sliced open along the two generators, $a$ and $b$, of the fundamental group of the torus.
:::
::::

We introduce the theory and algorithms for computing the intrinsic coordinate system using *holomorphic quadratic differentials*. Depending on the topology of the surface there are a constant number of *zero points* (also called critical points, singular points or singularities) which do not have such coordinates. But such singular points are of zero measure. The coordinate system is naturally represented by a complex number. One can trace out a curve by fixing the real/imaginary part of the coordinate, called the vertical/horizontal trajectory respectively. This coordinate system naturally produces a space decomposition by slicing along critical trajectories (i.e., trajectories that end at zero points). Each component is a simply connected piece with the complex coordinates as its natural parametrization. This decomposition can also be represented by a graph $G$ in which the vertices are the critical points and an edge represents a cell that touches two singular vertices. This graph and the coordinate system/parametrization are used to generate a coverage path. See Figure [2](#fig:road3:subfig){reference-type="ref" reference="fig:road3:subfig"} for an example.

:::: {#fig:road3:subfig .figure latex-placement="htbp"}
::: caption
Example of a three holes donut with trapezoid decomposition([\[fig:road3:subfig:trap\]](#fig:road3:subfig:trap){reference-type="ref" reference="fig:road3:subfig:trap"}) and our holomorphic quadratic differentials method([\[fig:road3:subfig:2form\]](#fig:road3:subfig:2form){reference-type="ref" reference="fig:road3:subfig:2form"}). In trapezoid decomposition, the donut is decomposed into $11$ cells, the CPP problem here is equivalent to find a Hamiltonian path with these cells as vertices, which is NP-hard. Instead, our method simply cuts the donut into $6$ cells, and the CPP problem in our setting is equivalent to finding Euler cycle with these cells as edges, which can be easily achieved in polynomial complexity.
:::
::::

To generate a coverage path, we need to decide what order we use to visit the decomposed cells. Again we encounter the problem of visiting each cell at least once. In our setting we actually need to visit all the edges (representing the cells) in $G$, ideally once and only once. So this is in fact the Euler cycle problem, which is, fortunately, much easier than Hamiltonian cycle problem. Any graph in which all vertices have even degree has an Euler cycle. In our case, the degree of a critical point may not be even. But we can simply double each edge in the graph to create a graph $G'$ (which satisfies the requirement) and compute an Euler cycle on $G'$ -- equivalently, each edge in $G$ is visited precisely twice. This means each cell in the decomposition is visited exactly twice and we can simply stretch and shift the zig-zag pattern in the cell such that the paths followed by the two separate visits have minimum overlap.

The main theoretical contribution of this paper lies in the new discrete algorithm for computing holomorphic quadratic differentials for parametrizing the input domain. In the literature, a special subset of holomorphic quadratic differentials, named the holomorphic differentials (holomorphic one-forms), have been widely used in computer graphics for surface registration and texture mapping [@gu2002computing; @gu2003global]. Compared to this limited subset, holomorphic quadratic differentials construct a larger family of surface parameterization with more freedom and flexibility. The algorithm presented here for holomorphic quadratic differentials is new and has never been published before. Mathematically, holomorphic quadratic differentials are obtained by multiplying two holomorphic one-forms, and their parameterizations should satisfy the property of being a curl-free vector field. It is a challenging problem to control the numerical error around critical points due to the special local structure. Fortunately our robot cover path avoids the zero points and all we need is to trace out the 3 critical trajectories through each critical point, which is carefully handled in our algorithm.

We evaluated the coverage path generated by our algorithms on a variety of different settings including flat domains with obstacles, non-flat terrains, as well as general high genus surfaces. Our method is an offline method and requires the domain to be known in advance.

# Theory on Holomorphic Quadratic Differentials {#sec:prelim}

Our solution for the CPP problem is based on a global surface parameterization, namely the *holomorphic quadratic differentials*. Holomorphic quadratic differentials possess a good property that they inherently induce non-intersecting trajectories on a surface. This benefit prompts us to develop a path planning algorithm based on the trajectories.

Holomorphic quadratic differentials form a branch of study in complex manifold. In this section, we briefly introduce some basics of holomorphic quadratic differentials. Then we design our path planning method on general surfaces. For detailed treatments, we refer readers to [@farkas1992riemann] for Riemann surface theory, [@nehari1975conformal] for complex analysis, and [@strebel1984quadratic] for holomorphic quadratic differentials.

## Riemann Surfaces {#sub:riemann_surfaces}

::: definition
**Definition 1**. *(Manifold). Let $M$ be a topological space. For each point $p\in M$, there is a neighborhood $U_{\alpha}$ and a continuous bijective map $\phi_{\alpha}:U_{\alpha}\rightarrow V_{\alpha}$ from $U_{\alpha}$ to an open set $V_{\alpha}\subset \mathbb{R}^n$. $(U_{\alpha},\phi_{\alpha})$ is called a local chart. If two neighborhoods $U_{\alpha}$ and $U_{\beta}$ intersect, then the transition map between the chart $$\begin{equation*}
		\phi_{\alpha\beta}=\phi_{\beta}\phi_{\alpha}^{-1}:\phi_{\alpha}(U_{\alpha}\cap U_{\beta})\rightarrow\phi_{\beta}(U_{\beta}\cap U_{\alpha})
\end{equation*}$$ is a continuous bijective map. $M$ is an $n$ dimensional manifold, the set of all local charts $\{(U_{\alpha},\phi_{\alpha})\}$ form an atlas.*
:::

::: definition
**Definition 2**. *(Holomorphic Function). A complex function $f :\mathbb{C}\rightarrow\mathbb{C}: x+iy \mapsto u(x,y)+iv(x,y)$ is *holomorphic*, if it satisfies the following Cauchy-Riemann equation $$\begin{equation*}
\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \,
\frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}.
\end{equation*}$$*
:::

If $f$ is invertible and $f^{-1}$ is also holomorphic, then $f$ is called a *bi-holomorphic* function.

::: definition
**Definition 3**. *(Riemann Surface). A Riemann surface is a surface with an atlas $\{(U_{\alpha},\phi_{\alpha})\}$, such that all chart transitions $\phi_{\alpha\beta}$ are bi-holomorphic. The atlas is called a conformal atlas and the local coordinates $\phi_{\alpha}(U_{\alpha})$ are called holomorphic coordinates. The maximal conformal atlas is called a conformal structure of the surface.*
:::

On a Riemann surface, we can define a differential based on the conformal structure. Intuitively, a differential can be regarded as a vector field on a surface. The integration on a differential gives a surface parameterization. The holomorphic differentials and quadratic differentials we introduce below are curl and divergence free vector fields.

::: definition
**Definition 4**. *(Holomorphic Differential). Given a Riemann surface $R$ with a conformal atlas $\{(U_{\alpha},\phi_{\alpha})\}$, a holomorphic differential $\zeta$ is a complex differential form defined by a family $(U_{\alpha},z_{\alpha},\zeta_{\alpha})$, such that $\zeta_{\alpha}=\phi_{\alpha}(z_{\alpha})dz_{\alpha}$, where $\phi_{\alpha}$ is a holomorphic function on $U_{\alpha}$, and if $z_{\alpha}=\phi_{\alpha\beta}(z_{\beta})$ is the coordinate transformation on $U_{\alpha}\cap U_{\beta}$, then $\phi_{\alpha}(z_{\alpha})\frac{dz_{\alpha}}{dz_{\beta}}=\phi_{\beta}(z_{\beta})$.*
:::

According to the Poincaré-Hopf theorem [@hazewinkel2001poincare], any vector field on a surface with non-zero Euler number must have the singularities where the vector field vanishes. Such singularities are called *zero points*. Here we define the zero points of a holomorphic differential.

::: definition
**Definition 5**. *(Zero Point). For a point $p$ on a surface $R$, if the local representation of a holomorphic differential $\zeta$ around $p$ is $\zeta_{\alpha}=\phi_{\alpha}(z_{\alpha})dz_{\alpha}$ and $\phi_{\alpha}=0$ at $p$, then $p$ is called a *zero points* of $\zeta$.*
:::

## Holomorphic Quadratic Differentials {#sub:quadratic_differential}

::: definition
**Definition 6**. *(Holomorphic Quadratic Differential). Given a Riemann surface $R$. Let $\Phi$ be a complex differential form with a conformal atlas $\{(U_{\alpha},\phi_{\alpha})\}$, such that on each local chart with the local parameter $z_{\alpha}$, $$\begin{equation*}
		\Phi_{\alpha}=\phi_{\alpha}(z_{\alpha})dz_{\alpha}^{2},
\end{equation*}$$ where $\phi_{\alpha}(z_{\alpha})$ is a holomorphic function.*
:::

### Zero Points and Trajectories {#ssub:zero}

For a holomorphic quadratic differential $\Phi$ on a surface $R$, any point $p\in R$ away from zero has the local coordinate defined as $$\begin{equation}
\label{eq:natural}
	\xi(p):=\int^{p}\sqrt{\phi_{\alpha}(z_{\alpha})}dz_{\alpha}.
\end{equation}$$ This is called the *natural coordinate* induced by $\Phi$. The curves with constant real natural coordinates are called the *vertical trajectories*; while the curves with constant imaginary natural coordinates are called the *horizontal trajectories*. A trajectory which ends in zero points is called a *critical trajectories*, otherwise it is a *regular trajectory*. The horizontal trajectories of $\Phi$ are either infinite spirals or finite closed loops. This means that the trajectories of holomorphic quadratic differentials are non-intersecting trajectories on a surface. This property is the key idea of our path planning algorithm.

::: definition
**Definition 7**. *(Genus). A genus $g$ of a surface is the largest number of cuttings along non-intersecting simple closed curves on the surface without disconnecting it.*
:::

The local structure around a zero point of a holomorphic quadratic differential is a complex function $z\rightarrow z^{\frac{3}{2}}$. For any holomorphic quadratic differential $\Phi$ on a closed surface with genus $g>1$, there are $4g-4$ zero points. For a multiply-connected surface with $n>2$ boundaries, there are $2g-2$ zero points of $\Phi$. Zero points are also called *critical points* because they are the endpoints of critical trajectories.

## Surface Decomposition {#sub:domain_decomposition}

The path planning technique proposed in this work is applicable to both multiply-connected surfaces(surface with boundaries or obstacles) and general closed surfaces. For multiply-connected surfaces, we can directly decompose the surfaces along their critical trajectories. For general closed surfaces, the holomorphic quadratic differentials whose horizontal trajectories are closed loops induce the surface decomposition. The rationale of these properties are described as follows.

::: definition
**Definition 8**. *(Multiply-Connected Surface). Suppose $M$ is a surface of genus zero with multiple boundaries. Then $M$ is called a multiply-connected surface.*
:::

**Strebel Differentials.** []{#ssub:strebel_differentials label="ssub:strebel_differentials"} For a closed surface with genus $g>1$, holomorphic quadratic differentials induce the decomposition for the surface under some conditions. Those holomorphic quadratic differentials are called *Strebel differentials*.

::: definition
**Definition 9**. *(Strebel Differential[@strebel1984quadratic; @douady1975density]). Suppose $\Phi_{s}$ is a holomorphic quadratic differential on a surface $R$ with genus $g>1$. $\Phi_{s}$ is called a *Strebel differential*, if all of its regular horizontal trajectories are closed loops.*
:::

Notice that for a Strebel differential $\Phi_{S}$ on a closed surface $R$ with genus $g>1$, all the regular horizontal trajectories are closed loops as shown in Fig. [3](#fig:strebel){reference-type="ref" reference="fig:strebel"}. The set of critical trajectories together with the critical points form the critical graph $\Gamma$ of Strebel differential $\Phi_{s}$. The critical graph $\Gamma$ decomposes the surface $R$ into $3g-3$ topological cylinders [@strebel1984quadratic].

:::: {#fig:strebel .figure latex-placement="t"}
![image](Lin2017Robot_figs/strebel.png){width="0.5\\columnwidth"}![image](Lin2017Robot_figs/star.png){width="0.5\\columnwidth"}

::: caption
The regular horizontal trajectories of a Strebel differential are closed loops on the surface.
:::
::::

**Symmetric Quadratic Differentials.** []{#ssub:symmetric_quadratic_differentials label="ssub:symmetric_quadratic_differentials"} For any given multiply-connected surface $M$ with $n>2$ boundaries, we can find a holomorphic quadratic differential which decomposes $M$ into $3n-3$ simply-connected surfaces $\{d_{1}, d_{2}, \dots, d_{3n-3}\}$.

According to the symmetric image property [@strebel1984quadratic], $M$ and its double $\bar{M}$ form a symmetric surface $\tilde{M}=\{M\cup\bar{M}\}$ on which their corresponding boundaries are identified. Any holomorphic quadratic differential $\Phi$ on $M$ is reflected to $\bar{M}$. As a result, A symmetric surface $\tilde{M}$ is with a symmetric holomorphic quadratic differential $\tilde{\Phi}$. Because the boundaries $\partial{M}$ and $\partial{\bar{M}}$ are identified, each horizontal (vertical) trajectory $\gamma$ of $M$ and its symmetric trajectory $\bar{\gamma}$ of $\bar{M}$ are connected and form a closed loop.

The symmetric surface $\tilde{M}$ is, therefore, a closed surface with genus $g=n$. The holomorphic quadratic differential $\tilde{\Phi}$ on $\tilde{M}$ is a Strebel differential, which means the critical graph decomposes $\tilde{M}$ into $3n-3$ topological cylinders. Each cylinder $c_{i}$ is symmetric along the two curves which are some intervals of $\partial{M}$. That is to say, $c_{i}$ consists of two symmetric simply-connected domain $d_i$ and $\bar{d_i}$. By considering $\{d_{1}, d_{2},\dots, d_{3n-3}\}$, we can conclude that the holomorphic quadratic differential $\Phi$ decomposes $M$ into $3n-3$ simply-connected surfaces.

# Algorithm {#sec:algorithm}

The core idea of the proposed algorithm is the *holomorphic quadratic differentials*, which induce surface parameterizations for general surfaces. In brief, holomorphic quadratic differentials inherently induce non-intersecting trajectories on a surface as shown in Figure [3](#fig:strebel){reference-type="ref" reference="fig:strebel"}. This property provides us enough freedom on manipulating the trajectories, and motivates us to develope our path planning algorithm.

Holomorphic quadratic differentials can be obtained by multiplying two holomorphic differentials.  [3.3](#ssub:Holomorphic_diff){reference-type="ref" reference="ssub:Holomorphic_diff"} briefly lists the computational steps of holomorphic differentials. The parameterizations of holomorphic quadratic differentials should satisfy the property of being a curl-free vector field. It is challenging to control the numerical error around critical points due to the special local structure. As for our robot cover path, it avoids the zero points and all we need is to trace out the 3 critical trajectories through each critical point.

For a topological torus (closed surface with genus one) and an annulus, the holomorphic quadratic differentials and holomorphic differentials are equivalent. Therefore, by connecting each path induced by the trajectories of a holomorphic differential, a path planning is obtained. The algorithm described in this section focuses on the closed surfaces with genus $g>1$, and the multiply-connected surface with $n>2$ boundaries. For a closed surface with boundaries, we can double cover the surface to become a closed surface with genus $g>1$. Then the algorithm can be directly applied.

## Discrete Approximation {#sub:discrete_approximation}

The mathematical concepts on smooth surfaces are now transformed to the numerical procedures on triangular meshes. A smooth surface is approximated by a piecewise linear triangle mesh $T$. The half-edge data structure is adopted in our implementation. We denote a vertex by $v_i$, a half-edge by $[v_{i},v_{j}]$, and an oriented triangle face by $[v_{i}, v_{j}, v_{k}]$.

A discrete differential is a function defined on the edge $\omega : E\rightarrow\mathbb{C}$. The integration of a discrete differential, $f:V\rightarrow\mathbb{C}$, gives a complex number or a $uv$-coordinate to each vertex.

## Algorithm Overview {#sub:algorithm_overview}

The following pipeline shows a summary of the main procedures of the path planning in this paper. The input is a triangular mesh of a closed surface with genus $g>1$, or a multiply-connected surface with $n>2$ boundaries. We first compute the *holomorphic differential* basis on a surface, which is then used to compute the *holomorphic quadratic differentials*. The holomorphic quadratic differential induces a global parameterization, and the resulting critical trajectories naturally decompose the surface into $3g-3$ ($3n-3$) sub-surfaces. For each sub-surface, we can compute a number of paths by tracing regular trajectories. The paths are concatenated together to become a zig-zag path on the sub-surface. Finally, we combine the sub-surfaces back to get a continuous path on the whole surface.

::: algorithm
[]{#algo:quad_mesh label="algo:quad_mesh"}

Compute a holomorphic differential basis for $T$;

Compute a holomorphic quadratic differential $\Phi$ for $T$;

Locate zero points of $\Phi$ on $T$;

Trace the critical graph $\Gamma$ from zero points;

$T$ is decomposed along the critical graph $\Gamma$ and the sub-surfaces $T\backslash\Gamma=\{d_{1},d_{2},\cdots,d_{3n-3}\}$ are obtained. For each $\{d_{i}\}$, generate a path planning $P_{i}$;

The path planning of the whole surface is formed by $P_{1}\cup P_{2}\cup \cdots\cup P_{3n-3}\cup\Gamma$
:::

## Holomorphic Differentials {#ssub:Holomorphic_diff}

The computation of holomorphic differentials is to solve an elliptic partial differential equation on a triangle mesh using finite element method. The key step is to use piecewise linear functions defined on edges to approximate differentials. Furthermore, the differentials minimize the harmonic energy, the existence and the uniqueness are guaranteed by the Hodge theory [@schoen1997lectures]. The following algorithm focuses on the closed surfaces with genus $g>1$. For a multiply-connected surface with $n>2$ boundaries, the algorithm is simplified to skip the computation of homology basis [@Yin:2008gd]. Readers can refer to the works by Gu et al. [@gu2002computing; @gu2003global] for more details.

::: algorithm
[]{#algo:holoform label="algo:holoform"}

Compute the homology group basis $\{\gamma_{1}, \gamma_{2},\cdots, \gamma_{2g}\}$ of $T$;

Compute the dual cohomology group basis $\{\psi_{1}, \psi_{2},\cdots, \psi_{2g}\}$ of $T$;

Compute the harmonic differential basis from the dual cohomology group basis $\{\psi_{1}, \psi_{2},\cdots, \psi_{2g}\}$ using heat flow method;

For each harmonic differential base $\omega_{i}$, locally rotate by a right angle about the normal to obtain $\sqrt{-1}*\omega_{i}$. $\omega_{i}+\sqrt{-1}*\omega_{i}$ forms a holomorphic differential $\zeta_i$
:::

In the algorithm below, the holomorphic differential $\omega_{i}+\sqrt{-1}*\omega_{i}$ is denoted by $\zeta_{i}$, where $i\in \{1,2,\cdots,2g\}$.

## Holomorphic Quadratic Differentials {#sub:Holomorphic_quadratic_diff}

The holomorphic quadratic differentials on a surface can be obtained from the products of any two holomorphic differentials $\Phi=\{\zeta_{i}\cdot\zeta_{j}\}$, $i,j\in \{1,2,\cdots,2g\}$.

::: algorithm
[]{#algo:hqd label="algo:hqd"}

Compute the products of the holomorphic differentials $\zeta_{i}\cdot\zeta_{j}$
:::

:::: {#fig:tripledonut .figure latex-placement="htbp"}
![](Lin2017Robot_figs/tripledonut.png){width="1\\columnwidth"}

::: caption
A three-hole donut with zero points($p_1 \sim p_4$) and simply-connected surfaces($d_1 \sim d_6$) decomposed by the critical trajectories(in blue).
:::
::::

## Surface Decomposition {#surface-decomposition}

For a closed surface with genus $g>1$, the surface decomposition is induced by Strebel differentials. Since holomorphic quadratic differentials $\zeta_{i}\cdot\zeta_{j}$ form a vector space, and Strebel differentials are the holomorphic quadratic differentials with closed horizontal trajectories. Therefore, a Strebel differential can be computed by the linear combination of holomorphic quadratic differentials. The surface is decomposed to $3g-3$ topological cylinders with two boundaries $\{c_{1}, c_{2}, \dots, c_{3g-3}\}$. For any multiply-connected surface with $n>2$ boundaries, the critical graph of a holomorphic quadratic differential decomposes the surface to $3n-3$ simply-connected surfaces $\{d_{1}, d_{2}, \dots, d_{3n-3}\}$.

In order to decompose the given surface along the critical graph of a computed holomorphic quadratic differential, we first locate the zero points on the surface. Then we trace the critical trajectories from the zero points. Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"} illustrates the surface decomposition. For a surface with three holes (inner boundaries), there are four critical points (zero points) and six simply-connected domains.

::: algorithm
[]{#algo:locatezeros label="algo:locatezeros"} Given a vertex $v\in T$, find all vertices connecting to $v$ sorted counterclock-wisely, denoted as $w_{0},w_{1},\cdots,w_{n-1}$;

Map $w_i$ to the plane using its natural coordinate $\xi(w_i):=\int^{w_i}_{v}\sqrt{\Phi}$;

The points $\xi(w_0),\xi(w_1),\cdots,\xi(w_{n-1})$ form a planar polygon and the point $\xi(v)$ is inside this polygon. Compute the summation of the angles $$\begin{equation*}
		\sum_{i=0}^{n-1}\angle\xi(w_i)\xi(v)\xi(w_{i+1}),
\end{equation*}$$ where $w_{n}=w_{0}$. If the summation is $2\pi$, then $v$ is a regular point; if the summation is no less than $3\pi$, then $v$ is a zero point
:::

::: algorithm
[]{#algo:trace1 label="algo:trace1"} For $p_i\in T$, find all faces adjacent to $p_i$ sorted counterclock-wisely, denoted as $f_{0},f_{1},\cdots,f_{n-1}$;

For each vertex $w_j$ of $f_k$, map $w_j$ to the plane using its natural coordinate $\xi(w_j):=\int^{w_j}_{p_i}\sqrt{\Phi}$. The computation of natural coordinates is shown in Algorithm [\[algo:choosesign\]](#algo:choosesign){reference-type="ref" reference="algo:choosesign"};

The points $\xi(w_0), \xi(w_1), \xi(w_2)$ form a planar triangle, where $w_{0}=p_i$ and $w_0$ is mapped to the origin. Let $y_{1},y_{2}$ be the imaginary natural coordinates of $\xi(w_1), \xi(w_2)$ respectively. If $y_{1}y_{2} < 0$, then the planar triangle, denoted as $\Delta_{\xi}$, is passed by a critical trajectory $\gamma$;

Compute the natural coordinates starting from $\Delta_{\xi}$. Find all of the parameterized triangles passed by $\gamma$. For a $g>1$ closed mesh, trace $\gamma$ until hitting a zero point; For a multiply-connected mesh with $n>2$ boundaries, trace $\gamma$ until hitting a boundary;

Interpolate the critical trajectory $\gamma$, by which the planar triangles are passed
:::

::: algorithm
[]{#algo:choosesign label="algo:choosesign"} Given a face $f\in T$, compute $\sqrt{\Phi}$. For each edge $e$ of $f$, the sign of $\sqrt{\Phi}$ is decided to satisfy $\oint_{f}\sqrt{\Phi}=0$ because $\sqrt{\Phi}$ is a curl free vector field;

For each vertex $v$ of $f$, compute the natural coordinate by the integration $\int\sqrt{\Phi}$
:::

## Coverage Path

The non-intersecting trajectories of holomorphic differential $\Phi$ give the paths for our coverage path planning. Here we take a multiply-connected surface $M$ as an example. Let the outer boundary of $M$ denoted by $l_1$, the inner boundaries denoted by $\{l_{2}, \cdots, l_{n}\}$, and the boundaries of the decomposed simply-connected surfaces denoted by $\{\partial d_{1}, \partial d_{2},\cdots, \partial d_{3n-3}\}$. Given any density step $\epsilon >0$, if $l_{1}\cap\partial d_{i}\neq\emptyset$, then we trace a regular trajectory for each density step $\epsilon$ along $l_{1}\cap\partial d_{i}$. Otherwise, there exists an inner boundary $l_i$ such that $l_{i}\cap\partial d_{i}\neq\emptyset$, and we trace a regular trajectory for each density step $\epsilon$ along $l_{i}\cap\partial d_{i}$. Once the paths are generated, we can simply connect the path together to form a zig-zag path.

:::: {#fig:dual_graph .figure latex-placement="htbp"}
![](Lin2017Robot_figs/dual_graph.png){width="0.45\\columnwidth"}

::: caption
The dual graph of Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. Here the zero points($p_1 \sim p_4$) are treated as nodes, and the decomposed simply-connected surfaces($d_1 \sim d_6$) that touched these points represent edges between nodes.
:::
::::

### Euler Cycle on Surface {#ssub:euler_cylce}

Based on our surface decomposition scheme, we discover that the zero points and the sub-surfaces can be converted to a dual graph $G_{M}$. That is, each zero point is dual to a node and each sub-surface is dual to an edge. Moreover, the necessity of visiting every sub-surface inspires the idea of finding an Euler cycle of $G_M$. By doubling each edge, it is guaranteed to find an Euler cycle which promises the visiting of every sub-surface.

Here we take the surface shown in Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"} as an example. Its dual graph is illustrated in Figure [5](#fig:dual_graph){reference-type="ref" reference="fig:dual_graph"}. Each zero point $p_i$ is dual to a node, and each decomposed simply-connected surface $d_j$ is dual to an edge. Figure [6](#fig:dual_graph_doubled){reference-type="ref" reference="fig:dual_graph_doubled"} shows the doubled dual graph of Figure [5](#fig:dual_graph){reference-type="ref" reference="fig:dual_graph"}. For each edge $d_j$, the doubled edge $\bar{d}_j$ is created. Figure [7](#fig:euler_cycle){reference-type="ref" reference="fig:euler_cycle"} shows an Euler cycle of the doubled dual graph of Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. On the dual graph, Euler cycle makes the navigation start and end at the same point.

:::: {#fig:dual_graph_doubled .figure latex-placement="htbp"}
![](Lin2017Robot_figs/dual_graph_doubled.png){width="0.55\\columnwidth"}

::: caption
The doubled dual graph of Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. We simply double each edge in the original dual graph(Figure [5](#fig:dual_graph){reference-type="ref" reference="fig:dual_graph"}).
:::
::::

:::: {#fig:euler_cycle .figure latex-placement="htbp"}
![](Lin2017Robot_figs/euler_cycle.png){width="0.55\\columnwidth"}

::: caption
An Euler cycle example of the doubled dual graph of Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. The cycle starts from $p_1$, and travels through the arrowed edge with number $1 \sim 12$, and finally goes back to $p_1$.
:::
::::

### Path Interlacement {#ssub:interlace}

Euler cycle of the dual graph of a surface implies that every sub-surface is visited twice. By interlacing two zig-zag paths with same density step, each sub-surface can be covered nicely. Figure [8](#fig:d1){reference-type="ref" reference="fig:d1"} illustrates the interlacing paths on the simply-connected domain $d_1$ in Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. There are two paths traveling from one zero points to the other, labeled as blue and orange. When a robot travels between two zero points, it can choose a color on one way (as $d_1$ in Figure [6](#fig:dual_graph_doubled){reference-type="ref" reference="fig:dual_graph_doubled"}) and the other color on the other(as $\bar{d_1}$ in Figure [6](#fig:dual_graph_doubled){reference-type="ref" reference="fig:dual_graph_doubled"}), hence provide required path density for coverage.

:::: {#fig:d1 .figure latex-placement="htbp"}
![](Lin2017Robot_figs/d1.png){width="0.3\\columnwidth"}

::: caption
An Example of paths on the simply-connected domain $d_1$ in Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. There are two paths traveling from one critical points to the other, labeled as blue and orange. When a robot travels between two zero points, it can choose a color on one way (as $d_1$ in Figure [6](#fig:dual_graph_doubled){reference-type="ref" reference="fig:dual_graph_doubled"}) and the other color on the other(as $\bar{d_1}$ in Figure [6](#fig:dual_graph_doubled){reference-type="ref" reference="fig:dual_graph_doubled"}), hence provide required path density for coverage.
:::
::::

Between the adjacent simply-connected domains, a robot can travel along the critical graph and transfer from one domain to another. By following the path interlacement and the Euler cycle scheme, the coverage path for the whole surface is performed. Figure [9](#fig:whole){reference-type="ref" reference="fig:whole"} exhibits the coverage path result for a surface with three inner boundaries.

:::: {#fig:whole .figure latex-placement="htbp"}
![](Lin2017Robot_figs/whole4.png){width="0.8\\columnwidth"}

::: caption
Coverage path for a three-hole donut.
:::
::::

:::: {#fig:dount .figure latex-placement="htbp"}
::: caption
The path coverage of three holes donut with different density step $\epsilon$ and $\delta$. The orange and blue lines are the coverage paths, the singular points are labeled as red. Here the covered area is with light blue color. Notice that $\epsilon$ is inversely proportional to the path density.
:::
::::

:::: {#fig:coverage .figure latex-placement="htbp"}
![](Lin2017Robot_figs/coverage.png){width="0.8\\columnwidth"}

::: caption
A comparison of density step $\epsilon$ and robot radius $\delta$ with coverage and overlap rate. Notice that $\epsilon$ is inversely proportional to the path density.
:::
::::

# Experimental Results {#sec:exp}

We evaluate our algorithm on various surfaces, and analyze the influence of different density step on coverage. We first demonstrate our algorithm on a 2D three holes donut as in Figure [4](#fig:tripledonut){reference-type="ref" reference="fig:tripledonut"}. The coverage path result is displayed in Figure [10](#fig:dount){reference-type="ref" reference="fig:dount"}. Here the robot covered area is colored with light blue. We fix the robot radius as $\delta$, and the density step $\epsilon$ represents the step distance on the outer boundary. Therefore, the bigger $\epsilon$ brings the sparser coverage paths. Notice that even smaller $\epsilon$ brings better coverage, but it also comes with a price of overlapped coverage. A comparison of the tradeoff between $\epsilon$, $\delta$, coverage rate and overlap rate is as Figure [11](#fig:coverage){reference-type="ref" reference="fig:coverage"}. As expected, the result shows that the overlap is more obvious on larger robot radius $\delta$ and denser density step $\epsilon$. Rather than the standard 2D domain, our algorithm is also suitable for complex 2D domain and 3D terrain with holes, the result of covering path is demonstrated in Figure [12](#fig:monster){reference-type="ref" reference="fig:monster"} and Figure [13](#fig:terrain){reference-type="ref" reference="fig:terrain"}.

:::: {#fig:monster .figure latex-placement="htbp"}
![](Lin2017Robot_figs/monster_covered.png){width="0.6\\columnwidth"}

::: caption
Example of a coverage path with a four-hole non-convex domain.
:::
::::

:::: {#fig:terrain .figure latex-placement="htbp"}
::: caption
Example of a 3-D terrain with three lakes. The lakes are represented by empty holes.
:::
::::

# Related Work

This problem has been studied extensively and one can refer to nice surveys [@Galceran:2013kg; @Choset:2001vf] for past work in this area. For 2D domains, most works use a cell decomposition to decompose the domain into simple shapes. Popular cell decomposition includes classical trapezoid decomposition[@DeCarvalho:1997bs; @Oksanen:2009gz] and boustrophedon cellular decomposition [@Choset:1998cha; @Garcia:2004kd; @Xu:2011cl], Morse decomposition [@Acar:2002fx; @Galceran:2012ix], slice decomposition [@Wong:2003fk], various grid-based algorithms [@Kapanoglu:2012bq; @Zelinsky:1993te; @Cai:2014un; @Bhattacharya:2013bj], etc. Most of these approaches are concerned of producing a small number of cells in the decomposition, and whether the decomposition can be done in the online setting (when the target domain is unknown and to be discovered). Other methods include applying spanning tree coverage[@Gabriely:2001gb; @Zheng:2005kh] and neural network based coverage[@Luo:2002fa; @Yang:2004gq; @Yan:2012dk].

Coverage path planning for surfaces in 3D is less investigated. Hert *et al.* [@Hert:1996fn] considered coverage of a projectively planar 3D volume, they project the domain in 2D and then take advantages of the 2D planar terrain-covering algorithm to solve the problem. Atkar *et al.* [@Atkar:2001wz] extended the Morse decomposition to non-planar surfaces but did not consider obstacles. In [@Bhattacharya:2014vs] Bhattacharya et al. extended their grid-based algorithm[@Bhattacharya:2013bj] into 3D cased; they first separated the domain into voronoi cells, then handled them by multiple robots. In [@Jin:2011cl; @Galceran:2013ds], the authors proposed a lawnmower type of algorithm on 3D planar domain, but the results only show terrains with boundary and without obstacles. More heuristic algorithms are adopted in application scenarios as [@Cheng:2008fn; @Galceran:2013ds; @Jin:2011cl].

The one most relevant was our earlier work for generating a space filling curve [@ban13topology]. However, the focus in [@ban13topology] was to find a curve with progressive density -- that is, we want a path such that the distance from any point to the path to be shrinking progressively when the path gets longer. The same as in a followup work [@li15space]. Although quadratic differentials were also used in [@li15space] but both the theory and the algorithms for generating the curves are totally different from here.

The coverage path problem is also related to various traveling salesman problem (TSP with neighborhoods [@Arkin:2000ir]), the lawnmower problem (full cover of a region by a path with minimum length) [@Arkin:1994ds], and the sweeping path problem (full coverage by a robot arm of fixed geometric degree of freedom) [@Kim:2003gx]. Since these problems are sufficiently different we skip the results here.

# Conclusion {#sec:conclusion}

In this paper, a brand new surface parameterization, *holomorphic quadratic differentials*, is adopted to perform the coverage path planning for general surfaces with complex topology. The natural coordinates of holomorphic quadratic differentials inherently induce non-intersecting trajectories on surfaces. This property inspires us to develope a robot coverage path planning algorithm. Moreover, holomorphic quadratic differentials intrinsically bring a regular number of surface decomposition. By converting the surface decomposition to its doubled dual graph, robots can travel on the whole surface according to the Euler cycle with great coverage.

[^1]: $^{1}$Department of Computer Science, Stony Brook University, Stony Brook, NY, USA `{yuylin,chni,jgao,gu}@cs.stonybrook.edu`

[^2]: $^{2}$School of Software, Dalian University of Technology, Liaoning, China `nalei@dlut.edu.cn`
