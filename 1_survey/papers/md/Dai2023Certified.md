---
citation_key: Dai2023Certified
arxiv_id: 2302.12219
arxiv_url: https://arxiv.org/abs/2302.12219
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:33:57Z
origin: ai+web
reviewed: false
---

# Introduction {#S: Introduction}

The notion of configuration space (C-space) has played a foundational role in robot motion planning since its proposal in the seminal work [@lozano1983spatial]. In the presence of obstacles in the Cartesian task space, a fundamental challenge is describing the collision-free C-space (C-free): the full range of configurations for which a robot is not in collision. Prior work has taken two complementary approaches to this problem.

The first approach attempts to find an explicit description of the C-space obstacles from their task-space description and the inverse kinematics (IK). We refer to this approach as the negative approach, as C-free is described as the complement of the set of C-space obstacles. In its full generality, the problem of describing C-space obstacles is intractable [@canny1988complexity], and so limiting assumptions on the robot are often made. For example, [@kavraki1995computation] develops a method for computing C-space obstacles based on the Fast Fourier Transform under the assumption that the robot can only translate in the workspace. In [@branicky1990computing], explicit descriptions of C-space obstacle due to the presence of point, line, and planar task-space obstacles are presented for two and three degree of freedom (DOF) robots. A thorough review of describing C-space obstacles can be found in [@latombe2012robot Chapter 3]. There it is shown that if all the task-space obstacles are described as semi-algebraic sets (i.e. as the intersection and union of polynomial inequalities) then C-space obstacles are also semi-algebraic. This is an important result from a complexity-theoretic standpoint as it shows that describing the C-space obstacles is at least decidable, though still very hard.

We refer to the second approach as the positive approach, as it seeks to directly describe C-free as a union of simpler sets. This description is attractive as a variety of optimization-based motion planning methods can efficiently leverage such descriptions, particularly when the simpler sets are convex [@deits2015efficient; @schouwenaars2001mixed; @marcucci2021shortest; @marcucci2022motion].

Rapidly-exploring Random Trees (RRT) [@lavalle1998rapidly], Probabilistic Roadmaps (PRM) [@kavraki1996probabilistic], and their variants can all be considered examples of this approach, describing C-free using piecewise-linear paths. Frequently, these methods provide probabilistic guarantees that the paths contain no collisions via sampling along the paths. To avoid false positive claims of non-collision, rigorous certification procedures such as [@schwarzer2004exact] can be used. Works such as [@verghese2022configuration; @han2019configuration; @wong2014adaptive] all seek to describe non-zero volume subsets of C-free. Similar to RRTs and PRMs, these methods have the advantage of working in arbitrary configuration spaces, make no assumptions on the C-space obstacles, and proceed via sampling. Therefore, they are typically relatively simple to implement and quite fast in low dimensions. Unfortunately, these methods only provide probabilistic guarantees of non-collision.

When the C-space obstacles are assumed to be convex, rigorous descriptions of C-free may be possible, though hardness results exist. For example, in two and three dimensions with polyhedral C-space obstacles, it is known that finding a minimal decomposition is NP-hard [@lingas1982power] to solve exactly and even APX-hard [@eidenbenz2003approximation] to approximate[^1]. Works such as [@lien2007approximate] and [@ghosh2013fast] overcome these hardness results by finding decompositions that are unions of approximately convex sets.

In arbitrary dimensions and under the assumption of known, convex C-space obstacles, C-free can be decomposed into convex polyhedra by using the  algorithm of [@deits2015computing]. As it is based on convex programming,  is relatively fast, and is also able to generate *rigorous certificates* of non-collision. Unfortunately, it is often the case that obstacles are naturally described as convex sets in *task space*, which are rarely convex in C-space.

In this work, we similarly provide a method for describing C-free using convex polyhedra in a bijective, rational parametrization of C-space known as the tangent configuration space (TC-space). Our primary technical contributions are two convex (specifically Sums-of-Squares (SOS)) programs which can certify that a polyhedron in TC-space contains no collision when the obstacles are specified as convex sets in *task space*. Similar to [@deits2015computing], we then construct certified, collision-free polytopic regions by alternating between a pair of convex programs. Our method works in arbitrary dimensions and is the first to our knowledge to provide rigorous certificates for non-zero volume sets in this setting. Moreover, we provide a fast, mature implementation technique in the open-source robotics toolbox [Drake](https://drake.mit.edu/)[^2].

A conference version of this paper is published in [@amice2022finding], which assumes a robotic manipulator composed of revolute joints operating in a scene where all task-space obstacles are decomposed as a union of vertex representation (V-rep) polytopes. This journal version extends these results in many ways.

First, we demonstrate how our approach can be extended to handle other common, non-polytopic geometries such as spheres, capsules, and cylinders. Moreover, we describe how to extend our approach to handle a robot composed of any of the algebraic joints: revolute, prismatic, spherical, planar, and cylindrical. Our second technical contribution introduces a second method for certifying non-collision inspired by the dual of the separating hyperplane approach used in the conference paper. This approach takes the form of certifying the emptiness of a set of polynomial equations and inequalities which can also be written as an optimization program. The third technical contribution of this work is to show that feasibility of the optimization programs we use for certification is not only sufficient, but also necessary for a TC-space region to be collision free provided the degree of certain polynomials are chosen sufficiently large. Finally, we provide new examples of our algorithm deployed on various robots including 2-DOF robots to visualize the TC-space, a robot containing a prismatic joint, and a UR3e robot with collision geometries approximate by cylinders.

We begin in Section [2](#S: Problem Statement){reference-type="ref" reference="S: Problem Statement"} by formally introducing our problem and our assumptions. We proceed in Section [3](#S: Background){reference-type="ref" reference="S: Background"} by introducing necessary mathematical background for describing our technical approach. In Section [4](#S: Certification){reference-type="ref" reference="S: Certification"}, we present our most technical results: two convex programs which can certify whether a region of TC-space is collision-free. We also state the conditions under which feasibility of these programs are guaranteed when a proposed region is collision-free. We describe how to leverage the certification programs to generate convex decompositions of TC-free in Section [5](#S: Bilinear Alternation){reference-type="ref" reference="S: Bilinear Alternation"}. We conclude in Section [6](#S: Results){reference-type="ref" reference="S: Results"} with examples of our algorithm deployed on various robots. We will first illustrate the algorithm on two simple 2-DOF systems where both the task and configuration spaces can be visualized and the entire configuration space can be quickly covered. We next demonstrate the ability of our algorithm to certify a wide range of postures for two realistic, 7-DOF manipulators interacting with a shelf. We conclude by showing our algorithm's ability to scale by exploring two 12-DOF, bimanual manipulators.

**Notation:** Throughout the paper, we will use calligraphic letters ($\ensuremath{\mathcal{S}}$) to denote sets, Roman capitals ($X$) to denote matrices, and Roman lower case ($x$) to denote vectors. We use $[N] = \{1, \dots, N\}$, denote the set of all multivariate polynomials in the vector of variables $x$ as $\ensuremath{\mathbb{R}}[x]$, and denote the cone of Sums-of-Squares (SOS) polynomials as $\ensuremath{\bm{\Sigma}}$. Additionally, we will adopt the monogram notation of [@tedrakeManip] for rigid transforms.

# Problem Statement {#S: Problem Statement}

We consider a known, task-space environment where our robot and all obstacles have been decomposed as a union of compact, convex bodies[^3] for example cylinders, capsule, spheres, or vertex representation (V-rep) polytopes. Such collision geometries of our task space are readily available through standard tools such as V-HACD [@mamou2009simple] and are often a required step for simulating any given environment.

Our robot is a mechanism composed of $N + 1$ links connect via either revolute or prismatic joints [@wampler2011numerical]:

- Revolute (R): a 1-DOF joint permitting revolution about an axis of symmetry. An example is a door handle.

- Prismatic (P): a 1-DOF joint permitting translation along an axis. An example is a linear rail.

We will assume that all revolute joints are constrained from undergoing complete rotations and all prismatic joints have bounded translation. Formally, if $\theta$ is the configuration-space variable associated to revolute joint, then: $$\begin{align}
 \label{E: joint limit angles}
    -\pi < \theta_{l} \leq \theta \leq \theta_{u} < \pi,
\end{align}$$ and if $z$ is the configuration-space variable associated to a displacement then: $$\begin{align}
 \label{E: joint limit prismatic}
    z_{l} \leq z \leq z_{u}.
\end{align}$$ where the bounds $\theta_{l}$, $\theta_{u}$, $z_{l}$, and $z_{u}$ are fixed constants.

Our objective is to find large, convex regions of TC-free regardless of the dimension of the configuration space. This objective is beyond the scope of current decomposition for non-convex spaces/objects such as V-HACD due to the dimensionality of the problem for interesting robots and the complexity of the non-linear kinematics.

::: remark
**Remark 1**. *Our approach can handle a robot composed of any of the five algebraic joints: revolute, prismatic, planar, cylindrical, planar, and spherical [@wampler2011numerical]. We restrict ourselves to R and P joints as the other joints can be seen as a composition of these two (see appendix [9](#A: alg kin){reference-type="ref" reference="A: alg kin"} for details).*
:::

# Background {#S: Background}

This section introduces key notions from convex analysis and algebraic geometry that will be essential for our approach presented in Section [4](#S: Certification){reference-type="ref" reference="S: Certification"}. We begin by recalling some classic theorems pertaining to the separation of convex bodies. We next review the Positivstellensatz, a central theorem from algebraic geometry that forms the basis for many applications of the Sums-of-Squares method that we will leverage. We conclude by recalling a parameterization of a robot's forward kinematics using rational functions.

## Separating Convex Bodies {#S: separating convex bodies}

In this section, we review two dual ways to check whether two compact, convex sets $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ intersect by using convex optimization. Our certification programs in Section [4](#S: Certification){reference-type="ref" reference="S: Certification"} will rely on generalizations of the programs introduced in this section.

A well-known result from convex optimization theory is the Separating Hyperplane Theorem [@boyd2004convex Section 2.5] which states that $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ do not intersect, if and only if there exists a hyperplane $\ensuremath{\mathcal{H}}(a,b) = \{x \mid a^{T}x + b = 0, (a, b)\neq (0, 0)\}$ which strictly separates the two bodies. The hyperplane $\ensuremath{\mathcal{H}}(a,b)$ serves as a *certificate* of non-intersection. Such a hyperplane is visualized in Figure [\[F: sep hyperplane\]](#F: sep hyperplane){reference-type="ref" reference="F: sep hyperplane"} and is described by the solution to program [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"}. Many previous works [@brossette2017collision; @lin2022reduce] have applied the Separating Hyperplane Theorem to find a *single* collision-free posture; in this paper we apply the theorem to find a convex set of collision-free postures.

Conversely, if $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ do intersect, then it is possible to certify this by finding a point in $\ensuremath{\mathcal{A}}\cap \ensuremath{\mathcal{B}}$. Such a point can be found by solving the convex optimization program [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"}. A certificate of the *infeasibility* of [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} proves that $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ do not intersect. Finding a certificate of infeasibility can be obtained by considering the dual of [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} and is a standard notion in convex optimization [@boyd2004convex Section 5.8].

A solution to program [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} has the advantage of being able to quantify the magnitude of separation between the two bodies. Therefore, in Section [5](#S: Bilinear Alternation){reference-type="ref" reference="S: Bilinear Alternation"} we will prefer to base our algorithm on a generalization of [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"}. However, we will see that certain results will be easier to show by considering the *infeasibility* of program [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"}.

:::::::: {#F: convex interseciton .figure}
::: minipage
$$\label{E: sep hyperplane generic}
    \begin{gather} 
    % \bmax_{a,b, \epsilon} ~\epsilon~ \subjectto \nonumber  \\
    \textbf{Find } a,~ b \nonumber
    \\
    a^{T}x + b > 0
    , ~ \forall~x \in \ensuremath{\mathcal{A}}\label{E: sep hyperplane generic A}
    \\
    a^{T}y + b < 0
    ,~ \forall~y \in \ensuremath{\mathcal{B}}\label{E: sep hyperplane generic B}
    \\
    \nonumber
    % \\ \varepsilon > 0 \label{E: sep hyperplane generic positive margin}
\end{gather}$$
:::

::: minipage
$$\label{E: intersection via same point generic}
\begin{gather}
    \ensuremath{\textbf{Find }}x,~ y \nonumber~ \mathop{\mathrm{\textbf{subject\ to}}}\\
    x \in \ensuremath{\mathcal{A}}, ~ y \in \ensuremath{\mathcal{B}}\label{E: in set constraint generic}
    \\
    x = y \label{E: same point constraint generic}
\end{gather}$$
:::

::: minipage
[]{#F: sep hyperplane label="F: sep hyperplane"}
:::

::: minipage
[]{#F: convex interseciton label="F: convex interseciton"}
:::

::: caption
Program [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} searches for a hyperplane which separates $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ while program [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} searches for a point in $\ensuremath{\mathcal{A}}\cap \ensuremath{\mathcal{B}}$. Both of these are convex optimization programs, and exactly one of these programs is feasible.
:::
::::::::

We conclude by noting that programs [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} and [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} are *strong alternatives*; exactly one of the two programs is feasible. The key to solving either program is to find a finite parameterization of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"}, [\[E: sep hyperplane generic B\]](#E: sep hyperplane generic B){reference-type="eqref" reference="E: sep hyperplane generic B"}, and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"}. In Table [13](#Tab: shape conditions table){reference-type="ref" reference="Tab: shape conditions table"}, we provide a convenient reference for some common geometries.

::: {#Tab: shape conditions table}
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |
+:======================================================================================================================================================================================================================================================================================================================================================+:======================================================================================================================================================================================================================================================================================================================================================+:======================================================================================================================================================================================================================================================================================================================================================+
| ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    |
|   ------------------------------                                                                                                                                                                                                                                                                                                                      |   -------------------------------------------------------------                                                                                                                                                                                                                                                                                       |   ----------------------------------------                                                                                                                                                                                                                                                                                                            |
|   $$\{v_{1}, \dots, v_{m}\}.$$                                                                                                                                                                                                                                                                                                                        |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |
|   ------------------------------                                                                                                                                                                                                                                                                                                                      |       a^{T}v_{i} + b \geq 1, ~ \forall~ i \in \{1, \dots, m\}                                                                                                                                                                                                                                                                                         |       x = \sum_{i=1}^{m} \mu_{i}v_{i}, ~                                                                                                                                                                                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                       |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |       \sum_{i=1} \mu_{i} = 1,                                                                                                                                                                                                                                                                                                                         |
|   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |   -------------------------------------------------------------                                                                                                                                                                                                                                                                                       |       \\                                                                                                                                                                                                                                                                                                                                              |
| :::                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                       |       \mu_{i} \geq 0                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |
|                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |   ----------------------------------------                                                                                                                                                                                                                                                                                                            |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    |
|   --                                                                                                                                                                                                                                                                                                                                                  |   -------------------------------------------------------------                                                                                                                                                                                                                                                                                       |   --------------------------------------------------------                                                                                                                                                                                                                                                                                            |
|   --                                                                                                                                                                                                                                                                                                                                                  |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |   $$\ensuremath{\left\| x - o \right\|}^{2} \leq r^{2}$$                                                                                                                                                                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                       |           a^{T} o + b \geq r\ensuremath{\left\| a \right\|}\\                                                                                                                                                                                                                                                                                         |   --------------------------------------------------------                                                                                                                                                                                                                                                                                            |
|   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |           a^{T}o + b \ge 1                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                       |
| :::                                                                                                                                                                                                                                                                                                                                                   |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |
|                                                                                                                                                                                                                                                                                                                                                       |   -------------------------------------------------------------                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                       |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    |
|   --                                                                                                                                                                                                                                                                                                                                                  |   -----------------------------------------------------------------------------------------------------------------------------                                                                                                                                                                                                                       |   -----------------------------------------------------------------------------                                                                                                                                                                                                                                                                       |
|   --                                                                                                                                                                                                                                                                                                                                                  |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |
|                                                                                                                                                                                                                                                                                                                                                       |    a^{T} o_{1} + b \geq r_{1} \ensuremath{\left\| a \right\|} \\ a^{T} o_{2} + b \geq r_{2} \ensuremath{\left\| a \right\|}\\                                                                                                                                                                                                                         |       o_{\mu} = \mu o_{1} + (1-\mu)o_{2}                                                                                                                                                                                                                                                                                                              |
|   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |       a^To_1+b\ge 1                                                                                                                                                                                                                                                                                                                                   |       \\                                                                                                                                                                                                                                                                                                                                              |
| :::                                                                                                                                                                                                                                                                                                                                                   |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |       \ensuremath{\left\| x - o_{\mu} \right\|} \leq \mu r_{1} + (1-\mu)r_{2}                                                                                                                                                                                                                                                                         |
|                                                                                                                                                                                                                                                                                                                                                       |   -----------------------------------------------------------------------------------------------------------------------------                                                                                                                                                                                                                       |       \\                                                                                                                                                                                                                                                                                                                                              |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |       0 \leq \mu \leq 1                                                                                                                                                                                                                                                                                                                               |
|                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |
|                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |   -----------------------------------------------------------------------------                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    | ::: {#Tab: shape conditions table}                                                                                                                                                                                                                                                                                                                    |
|   --                                                                                                                                                                                                                                                                                                                                                  |   -----------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                                                                                         |   -----------------------------------------------------------------------                                                                                                                                                                                                                                                                             |
|   --                                                                                                                                                                                                                                                                                                                                                  |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |   $$\begin{gather*}                                                                                                                                                                                                                                                                                                                                   |
|                                                                                                                                                                                                                                                                                                                                                       |           % h = \norm{o_{1} - o_{2}} \\                                                                                                                                                                                                                                                                                                               |           o_{\mu} = \mu o_{1} + (1-\mu) o_{2}                                                                                                                                                                                                                                                                                                         |
|   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |           \frac{a_{z}\ensuremath{\left\| o_{1} - o_{2} \right\|}}{2} + b \geq r_1 \ensuremath{\left\| \begin{bmatrix} a_{x} & a_{y}\end{bmatrix} \right\|}                                                                                                                                                                                            |           \\                                                                                                                                                                                                                                                                                                                                          |
| :::                                                                                                                                                                                                                                                                                                                                                   |           \\                                                                                                                                                                                                                                                                                                                                          |           v ^{T} (o_{1} - o_{2}) = 0                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                       |           \frac{-a_{z}\ensuremath{\left\| o_{1} - o_{2} \right\|}}{2} + b \geq r_2 \ensuremath{\left\| \begin{bmatrix} a_{x} & a_{y}\end{bmatrix} \right\|}                                                                                                                                                                                           |           \\                                                                                                                                                                                                                                                                                                                                          |
|                                                                                                                                                                                                                                                                                                                                                       |           \\                                                                                                                                                                                                                                                                                                                                          |           x = o_{\mu} + v                                                                                                                                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                                                                                                       |           a^{T}\left(\frac{o_{1}+o_2}{2}\right) + b \geq 1                                                                                                                                                                                                                                                                                            |           \\                                                                                                                                                                                                                                                                                                                                          |
|                                                                                                                                                                                                                                                                                                                                                       |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |           \ensuremath{\left\| v \right\|} \leq \mu r_{1} + (1-\mu)r_{2}                                                                                                                                                                                                                                                                               |
|                                                                                                                                                                                                                                                                                                                                                       |   -----------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                                                                                         |           \\                                                                                                                                                                                                                                                                                                                                          |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |           0 \leq \mu \leq 1                                                                                                                                                                                                                                                                                                                           |
|                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |   \end{gather*}$$                                                                                                                                                                                                                                                                                                                                     |
|                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |   -----------------------------------------------------------------------                                                                                                                                                                                                                                                                             |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       |   : Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies. |
|                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                       | :::                                                                                                                                                                                                                                                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

: Parameterizations of conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: in set constraint generic\]](#E: in set constraint generic){reference-type="eqref" reference="E: in set constraint generic"} respectively for particular convex bodies.
:::

::: remark
**Remark 2**. *Problem [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} is frequently written with non-strict inequalities [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: sep hyperplane generic B\]](#E: sep hyperplane generic B){reference-type="eqref" reference="E: sep hyperplane generic B"} to make it compatible with modern solvers. Such a formulation requires excluding the trivial solution $(a,b) = (0,0)$ via extra constraints as well as planes which are not strictly separating. The conditions given in Table [13](#Tab: shape conditions table){reference-type="ref" reference="Tab: shape conditions table"} accomplish both with the constraint $a^Tx + b \ge 1$ with $x = v_{i}$ for polytopic geometries and $x = o$ for sphere, cylinder, and capsules.*
:::

## Certificates of Positivity and Infeasibility {#S: Psatz}

In Section [4](#S: Certification){reference-type="ref" reference="S: Certification"}, we will show how to generalize programs [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} and [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} to be able to certify non-collision for a range of robot configurations. Both generalizations will reduce to well-studied polynomial problems. Specifically, given the set $$\ensuremath{\mathcal{S}}_{g, h} = \{x \mid g_{i}(x) \geq 0, h_{j}(x) = 0, i \in [n], j \in [m]\},$$ where $g_i(x)$ and $h_{j}(x)$ are all given polynomial functions of $x$, then certifying the separating hyperplane conditions [\[E: sep hyperplane generic A\]](#E: sep hyperplane generic A){reference-type="eqref" reference="E: sep hyperplane generic A"} and [\[E: sep hyperplane generic B\]](#E: sep hyperplane generic B){reference-type="eqref" reference="E: sep hyperplane generic B"} will be akin to a certifying a polynomial implication of the form $$\begin{align}
 \label{E: Gen Cert Prob}
     x \in \ensuremath{\mathcal{S}}_{g,h}  \implies p(x) \geq 0
\end{align}$$ where $p(x)$ is again a polynomial.

Moreover, certifying the infeasibility of [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} will be akin to certifying that $$\begin{align}
 \label{E: Gen Infeasible}
    \ensuremath{\mathcal{S}}_{g, h} = \emptyset.
\end{align}$$

Both of these polynomial problems are tractable. In particular, a class of results known as Positivstellensatz Theorems (Psatz) can be used to reduce both problems to a convex optimization program [@parrilo2000structured; @blekherman2012semidefinite]. In this section, we review the Psatz results that we will use.

Our assumption [\[E: joint limit angles\]](#E: joint limit angles){reference-type="eqref" reference="E: joint limit angles"} and [\[E: joint limit prismatic\]](#E: joint limit prismatic){reference-type="eqref" reference="E: joint limit prismatic"} that our robot has joint limits implies that the subsets of TC-free we wish to certify will be Archimedean sets, a property slightly stronger than compactness formally defined in Appendix [10](#A: Archimedean){reference-type="ref" reference="A: Archimedean"}. This will enable us to use a very strong Psatz Theorem for proving implications of the form [\[E: Gen Cert Prob\]](#E: Gen Cert Prob){reference-type="eqref" reference="E: Gen Cert Prob"} known as Putinar's Positivstellensatz.

::: {#T: Putinar .theorem}
**Theorem 1** (Positivstellensatz [@putinar1993positive]). *Suppose $\ensuremath{\mathcal{S}}_{g, h}$ is Archimedean and suppose that $p(x) > 0$ for all $x \in \ensuremath{\mathcal{S}}_{g,h}$. Then there exists polynomials $\phi_{j}(x),~j = 0, \dots, m$ and SOS polynomials $\lambda_{i}(x),~ i=0,\dots,n$ such that: $$\begin{align}
    p(x) = \lambda_{0}(x) + \sum_{i=1}^n\lambda_{i}(x)g_{i}(x) + \sum_{j=1}^m \phi_{j}(x) h_{j}(x) \label{E: Putinar Psatz}.
\end{align}$$*

*Moreover, if $p(x)$ is any polynomial that can be expressed as in [\[E: Putinar Psatz\]](#E: Putinar Psatz){reference-type="eqref" reference="E: Putinar Psatz"}, then $$\begin{align}
 \label{E: poly positive implication}
    x \in \ensuremath{\mathcal{S}}_{g,h} \implies p(x) \geq 0
\end{align}$$*
:::

As an immediate corollary, the previous theorem can be used to prove that $\ensuremath{\mathcal{S}}_{g,h}$ is empty.

::: {#T: Putinar Dual .theorem}
**Theorem 2** ( [@parrilo2004sum]). *Suppose $\ensuremath{\mathcal{S}}_{g, h}$ is Archimedean. Then $\ensuremath{\mathcal{S}}_{g,h} = \emptyset$ if and only if there exists polynomials $\phi_{j}(x)$ and SOS polynomials $\lambda_{i}(x)$ such that $$\begin{align}
-1 = \lambda_{0}(x) + \sum_{i} \lambda_{i}(x)g_{i}(x) + \sum_{j} \phi_{j}(x) h_{j}(x) \label{E: Putinar Dual Psatz}.
\end{align}$$*
:::

In both cases, the multiplier polynomials $\lambda$ and $\phi$ serve as *certificates* that the conditions [\[E: Gen Cert Prob\]](#E: Gen Cert Prob){reference-type="eqref" reference="E: Gen Cert Prob"} or [\[E: Gen Infeasible\]](#E: Gen Infeasible){reference-type="eqref" reference="E: Gen Infeasible"} hold. These certificates can be searched for using a convex optimization technique known as Sums-of-Squares (SOS) programming, a subset of semidefinite programming (SDP) [@parrilo2000structured]. The SOS technique has been widely used in robotics, for example in stability verification [@tedrake2010lqr; @majumdar2017funnel; @shen2020sampling], reachability analysis [@jarvis2003some; @yin2021backward] and geometric modeling [@ahmadi2016geometry]. In this paper, we will use SOS programming to generate certificates that subsets of TC-space are contained in TC-free.

## Rational Forward Kinematics {#S: Rat Forward}

Our method in Section [4](#S: Certification){reference-type="ref" reference="S: Certification"} will rely critically on parameterizing the forward kinematics of our robot using polynomials. Many robots contain rotational joints and so their forward kinematics are naturally specified as trigonometric functions. In this section, we review a standard change of variables of our robot kinematics which will enable us to parameterize the forward kinematics as a rational function.

The forward kinematics of a rigid-body robot with $N$ joints can be written by composing rigid transforms [@craig2005introduction; @tedrakeManip]. Written in homogeneous coordinates, and using the monogram notation [@tedrakeManip][^4], the pose of a frame $A$, expressed in the reference frame $F$, as a function of the robot configuration $q$ assumes the form: $$\begin{align}
\label{E: gen forward kin}
    \leftidx{^F}X^{A} = \begin{bmatrix}
        \leftidx{^F}R^{A}(q) & \leftidx{^F}p^{A}(q) \\
        0_{1 \times 3} & 1 \\
    \end{bmatrix}
    =
    \prod_{i \in \ensuremath{\mathcal{I}}_{F, A}} 
    \leftidx{^{P_{i}}}X^{C_i}(q_{i})\ \leftidx{^{C_i}}{X}^{P_{i+1}}
\end{align}$$ In equation [\[E: gen forward kin\]](#E: gen forward kin){reference-type="eqref" reference="E: gen forward kin"}, $\ensuremath{\mathcal{I}}_{F, A} =\{i_1,\hdots, i_n\}\subseteq [N]$ is the set of joints lying on the kinematic chain between $F$ and $A$. We attach two frames to each joint, with $P_i$ rigidly fixed to the parent link of the $i$^th^ joint, and $C_i$ rigidly fixed to the child link of the same joint. The two frames $P_i$ and $C_i$ coincide when the joint configuration $q_i=0$. The subset of configuration variables $q_{i}$ defines the degrees of freedom at the $i$^th^ joint, $\leftidx{^{P_i}}X^{C_i}(q_i)$ is the relative transform of the joint after the joint moves by $q_i$. The rigid transform $\leftidx{^{C_i}}X^{P_{i+1}}$ describes the physical properties of the $i$^th^ link such as its length. We assume that the reference frame $F$ is the $P_{i_1}$, the parent frame of the first joint $i_1$; while the frame $A$ is $C_{i_n}$, the child frame of the last joint $i_n$. [^5] We choose to be explicit about the reference frame $F$ at the risk of being pedantic, as the choice of reference frame $F$ will have important consequences for the scalability of the approach described in Section [5](#S: Bilinear Alternation){reference-type="ref" reference="S: Bilinear Alternation"} (see Appendix [14.1](#A: Frame Selection){reference-type="ref" reference="A: Frame Selection"} for a detailed discussion).

The matrices $\leftidx{^{P_{i}}}X^{C_{i}}(q_{i})$ assume the following forms [@wampler2011numerical] $$\begin{align}
 \label{E: gen low order pair}
    \leftidx{^{P_{i}}}X^{C_i}(q_{i}) &=
    \begin{cases}
    \begin{bmatrix}
        \cos(\theta_{i}) & -\sin(\theta_{i}) & 0 & 0 \\
        \sin(\theta_{i}) &  \cos(\theta_{i}) & 0 & 0 \\
        0  & 0  & 1 & 0 \\
        0 & 0 & 0 & 1
    \end{bmatrix}
    &
    \text{if $i$\textsuperscript{th} joint is Revolute}
    \\
    \begin{bmatrix}
        1 & 0 & 0 & 0 \\
        0 & 1 & 0 & 0 \\
        0 & 0  & 1 & z_{i} \\
        0 & 0 & 0 & 1
    \end{bmatrix}
    &
    \text{if $i$\textsuperscript{th} joint is Prismatic}
    \end{cases}
\end{align}$$

Expression [\[E: gen forward kin\]](#E: gen forward kin){reference-type="eqref" reference="E: gen forward kin"} expresses the position of our robot as an *multilinear trigonometric polynomial function*. Concretely, the $w$^th^ component (where $w\in\{x, y, z\}$) of the position of $A$ relative to $F$ and expressed in $F$ is an expression of the form: $$\begin{align}
 \label{E: gen forward kin pos}
    \leftidx{^F}p^{A}_{w}(q) = \sum_{j} c_{jw} \prod_{i \in \ensuremath{\mathcal{I}}_{F,A}} \xi_{ij,w}(q_{i})
\end{align}$$ with $\xi_{ij,w}(q_{i}) \in \{\cos(\theta_{i}), \sin(\theta_{i}), z_{i}\}$. The scalar constants $c_{jw}$ are determined by the robot kinematic parameters (link length, joint axis, etc). Therefore, our configuration-space variables are $$\begin{align*}
    q = \bigcup_{i} \{\theta_{i}, z_{i}\}.
\end{align*}$$

Multilinear trigonometric functions have many fortunate algebraic properties which we exploit throughout this paper, the first of which will be a change of variables enabling us to write [\[E: gen forward kin pos\]](#E: gen forward kin pos){reference-type="eqref" reference="E: gen forward kin pos"} as a rational function.

Specifically, we will introduce the substitution: $$\begin{align}
 \label{E: rational sub}
    t_{i} \coloneqq \tan\left( \frac{\theta_{i}}{2}\right),
\end{align}$$ which allows us to write $$\begin{align*}
    \cos(\theta_{i}) &= \frac{1-t_{i}^{2}}{1+t_{i}^{2}}, ~~
    \sin(\theta_{i}) = \frac{2t_{i}}{1+t_{i}^{2}}.
\end{align*}$$ This substitution is known as the stereographic projection [@spivakCalc] and is bijective if $\theta_{i} \in (-\pi, \pi)$ which we have assumed is the case for our robotic system[^6]. After performing this change of variables, our forward kinematics variables are $$\begin{align*}
    s =  \bigcup_{i} \{t_{i}, z_{i}\}.
\end{align*}$$ We refer to the configuration-space variable $s$ as the *tangent-configuration-space* (TC-space) variable.

In the TC-space variable, our forward kinematics are a *rational function* with a polynomial numerator and positive, polynomial denominator. This is an expression of the form $$\begin{gather}
\label{E: rational forward kinematics gen}
\leftidx{^F}p^{A}_{w}(s) =  \sum_{j} c_{jw} \prod_{i \in \ensuremath{\mathcal{I}}_{F,A}} \frac{\leftidx{^F}f_{ij,w}^{A}(s_{i})}{\leftidx{^F}g_{ij,w}^{A}(s_{i})}  = 
    \frac{\leftidx{^F}f^{A}_{w}(s)}{\leftidx{^F}g^{A}_{w}(s)},\; ~w\in\{x, y, z\},
\end{gather}$$ where $$\frac{\leftidx{^F}f_{ij,w}^{A}(s_{i})}{\leftidx{^F}g_{ij,w}^{A}(s_{i})} \in \left\{\frac{1-t_{i}^{2}}{1+t_{i}^{2}}, \frac{2t_{i}}{1+t_{i}^{2}}, \frac{z_{i}}{1}\right\}.$$ We will abbreviate the vector quantity: $$\begin{align}
\leftidx{^F}p^{A}(s) 
=
\frac{\leftidx{^F}f^{A}(s)}{\leftidx{^F}g^{A}(s)}
% \begin{bmatrix}
%     \frac{\leftidx{^F}f^{A}_{x}(s)}{\leftidx{^F}g^{A}_{x}(s)} \\
%     \frac{\leftidx{^F}f^{A}_{y}(s)}{\leftidx{^F}g^{A}_{y}(s)} \\
%     \frac{\leftidx{^F}f^{A}_{z}(s)}{\leftidx{^F}g^{A}_{z}(s)}
% \end{bmatrix}
% =
% \frac{1}{\prod_{w \in \{x,y,z\}}
% \begin{bmatrix}
% \leftidx{^F}f^{A}_{x}(s)\leftidx{^F}g^{A}_{y}(s)\leftidx{^F}g^{A}_{z}(s) 
% \\
% \leftidx{^F}f^{A}_{y}(s)\leftidx{^F}g^{A}_{x}(s)\leftidx{^F}g^{A}_{z}(s) 
% \\
% \leftidx{^F}f^{A}_{z}(s)\leftidx{^F}g^{A}_{x}(s)\leftidx{^F}g^{A}_{y}(s) 
% \end{bmatrix}
\end{align}$$ where $\leftidx{^F}f^{A}(s)$ is a *vector of polynomials* and $\leftidx{^F}g^{A}(s)$ is a single, positive polynomial. Notice that $\leftidx{^F}g^{A} (s) > 0$ since each denominator $\leftidx{^F}g_{ij, w}^{A}(s_{i}) = 1+t_i^2 \text{ or } 1$, which is strictly positive.

We emphasize again that we have assumed: $$\begin{gather*}
    -\pi < \theta_{l,i} \leq \theta_{i} \leq \theta_{u,i} < \pi,
    \\
    z_{l, i} \leq z_{i} \leq z_{u, i}.
\end{gather*}$$ and therefore generically $s_{l} \leq s \leq s_{u}$ component-wise.

Therefore, our substitution between $q$ and $s$ is bijective and so trajectories in TC-space correspond unambiguously to trajectories in C-space. Moreover, this assumption on boundedness of our configuration space allows us to seek collision-free regions $\ensuremath{\mathcal{P}}$ that are contained within $\ensuremath{\mathcal{P}}_{lim}$, a polytope encoding our joint limit: $\ensuremath{\mathcal{P}}\subseteq \ensuremath{\mathcal{P}}_{lim} = \{s \mid s_{l} \leq s \leq s_{u}\}$.

::: example
**Example 1**. *As an example, we consider the double pendulum [@underactuated].*

:::: {.figure latex-placement="htb"}
::: caption
*The forward kinematics of the double pendulum described in [@underactuated] can be described in the form [\[E: gen forward kin\]](#E: gen forward kin){reference-type="eqref" reference="E: gen forward kin"}.*
:::
::::

*The pose of the tip of the second pendulum can be written as: $$\begin{multline*}
    \left[
        \begin{array}{ c | c}
        R(\theta) &
        \begin{array}{c}
            p_{x}(\theta) \\
            p_{y}(\theta) 
            \end{array} 
            \\
            \hline
            0 & 1
        \end{array}
        \right]
        =
        \begin{bmatrix}
            \cos(\theta_{1}) & \sin(\theta_{1}) & 0 \\
            \sin(\theta_{1}) & -\cos(\theta_{1}) & 0\\
            0 & 0 & 1
        \end{bmatrix}
        \begin{bmatrix}
            1 & 0 & 0 \\
            0 & 1 & l_{1} \\
            0 & 0 & 1
        \end{bmatrix}
        *\\
        \begin{bmatrix}
            \cos(\theta_{2}) & \sin(\theta_{2}) & 0 \\
            \sin(\theta_{2}) & -\cos(\theta_{2}) & 0\\
            0 & 0 & 1
        \end{bmatrix}
        \begin{bmatrix}
            1 & 0 & 0 \\
            0 & 1 & l_{2} \\
            0 & 0 & 1
        \end{bmatrix}
\end{multline*}$$ The difference in the sign of the trigonometric part ensures that the $y$-axis is pointing down. Expanding out this product enables us to write the $x$ coordinate of the tip of the system as: $$\begin{align*}
        p_{x}(\theta_{1}, \theta_{2}) &=
        l_{2}(\sin(\theta_{2})\cos(\theta_{1}) - \sin(\theta_{1})\cos(\theta_{2})) + l_{1} \sin(\theta_{1})\\
        p_{y}(\theta_1, \theta_2) &=l_2(\sin(\theta_1)\sin(\theta_2) + \cos(\theta_1)\cos(\theta_2)) - l_1\cos(\theta_1)
\end{align*}$$ Notice that these are multilinear trigonometric polynomials, i.e. no term contains $\cos(\theta_{i})\sin(\theta_{i})$. We can perform the substitution given in [\[E: rational sub\]](#E: rational sub){reference-type="eqref" reference="E: rational sub"} to express the position as a rational function: $$\begin{align*}
        p_{x}(t_{1}, t_{2}) &=
        \frac{2l_{2}(t_{2}(1-t_{1})^{2} - t_{1}(1-t_{2})^{2}) + 2l_{1} t_{1}(1+t_{2})^{2}}
        {(1+t_{1}^{2})(1+t_{2}^{2})}\\
        p_y(t_1, t_2) &= \frac{l_2(4t_1t_2+(1-t_1)^2(1-t_2)^2) - l_1(1-t_1)^2(1+t_2)^2}{(1+t_1)^2(1+t_2)^2}
\end{align*}$$ .*
:::

# Certification of Set-Membership in TC-Free {#S: Certification}

In this section, we will consider the problem of certifying the non-collision of two convex bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ whose poses in task space are a function of the configuration of our robot. While programs [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} and [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} can be used to certify non-collision between $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ for any fixed configuration, they are insufficient to certify $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ do not intersect for all configurations in an entire region $\ensuremath{\mathcal{P}}$ of the configuration space. Therefore, in Sections [4.1](#S: Hyperplane Cert){reference-type="ref" reference="S: Hyperplane Cert"} and [4.2](#S: infeasible non-collision cert){reference-type="ref" reference="S: infeasible non-collision cert"}, we will show how to combine the ingredients of Section [3](#S: Background){reference-type="ref" reference="S: Background"} to generalize programs [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} and [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"}.

The presence of trigonometric functions when the forward kinematics are expressed in the variable $q$ precludes using SOS programming, our tool of choice. Therefore, we will assume that $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ are convex sets in task space with their poses expressed as *rational functions* in the TC-space variable $s$. This can be achieved using the developments in Section [3.3](#S: Rat Forward){reference-type="ref" reference="S: Rat Forward"}. Our objective will be to certify that $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ do not intersect for all $s \in \ensuremath{\mathcal{P}}= \{s \mid Cs \leq d\} \subseteq \ensuremath{\mathcal{P}}_{lim} = \{s \mid s_{l} \leq s \leq s_{u}\}$.

Under these assumptions, the generalizations of [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} and [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} will respectively take the form of certifying a polynomial implication and certifying the emptiness of a basic-semialgebraic set. We give a formulation of each as a SOS program. We will conclude in Section [4.3](#S: cert power){reference-type="ref" reference="S: cert power"} by proving that feasibility of our convex optimization programs is both necessary and sufficient for $\ensuremath{\mathcal{P}}$ to be collision-free.

## Parametrized Hyperplane Certificates of Non-Collision {#S: Hyperplane Cert}

In this section, we generalize [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"} and use SOS to search for a polynomial family of hyperplanes parametrized by the TC-space variable $s$ which will certify the non-collision of $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ for all $s \in \ensuremath{\mathcal{P}}= \{s \mid Cs \leq d\}$.

We begin by remarking that even if $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ do not collide for all $s \in \ensuremath{\mathcal{P}}$, there may not be a single, static hyperplane $\ensuremath{\mathcal{H}}= (a, b)$ which certifies this fact. An example of this can be seen in Figure [2](#F: svm){reference-type="ref" reference="F: svm"}.

:::: {#F: svm .figure latex-placement="htb"}
::: caption
The convex collision geometries $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ are collision-free if and only if there exists a family of hyperplanes $\ensuremath{\mathcal{H}}(s)$ separating the two for each configuration $s_{0}$. The planes act as a certificate of non-collision.
:::
::::

We therefore will look for a *polynomial family* of hyperplanes $\ensuremath{\mathcal{H}}(s) = \{x \mid a(s)^{T}x + b(s)=0\}$ parametrized by our TC-space variable $s$. Inspection of Table [13](#Tab: shape conditions table){reference-type="ref" reference="Tab: shape conditions table"} shows that we must generalize $$\begin{gather}
   s \in \ensuremath{\mathcal{P}}\implies  a^{T}(s) \ \leftidx{^F}p^{v}(s) + b(s) \geq 1,  \label{E: polynomial polytope point in set}
\end{gather}$$ for particular points $v$ specific to each of the geometries, and $$\begin{gather}
    s \in \ensuremath{\mathcal{P}}\implies  a^{T}(s) \ \leftidx{^F}p^{o}(s) + b(s) \geq r\ensuremath{\left\| a(s) \right\|} \label{E: polynomial round in set},
\end{gather}$$ for center $o$ if $\ensuremath{\mathcal{A}}(s)$ is either a sphere or capsule. The generalization of the conditions for the cylinder are similar to those of the sphere and capsule, and so we defer its complete derivation to Appendix [12](#A: cylinder matrix sos){reference-type="ref" reference="A: cylinder matrix sos"}.

To generalize [\[E: polynomial polytope point in set\]](#E: polynomial polytope point in set){reference-type="eqref" reference="E: polynomial polytope point in set"} and [\[E: polynomial round in set\]](#E: polynomial round in set){reference-type="eqref" reference="E: polynomial round in set"}, we recall that the position of any point $A \in \ensuremath{\mathcal{A}}(s)$ (and similarly $\ensuremath{\mathcal{B}}(s)$) can be expressed as a rational function $\leftidx{^F}p^{A}(s) = \frac{\leftidx{^F}f^{A}(s)}{\leftidx{^F}g^{A}(s)}$ where $\leftidx{^F}g^{A}(s) > 0$.

Therefore, we can express [\[E: polynomial polytope point in set\]](#E: polynomial polytope point in set){reference-type="eqref" reference="E: polynomial polytope point in set"} as: $$\begin{align}
    s \in \ensuremath{\mathcal{P}}\implies a^{T}(s) \ \leftidx{^F}f^{v}(s) + (b(s)-1) \ \leftidx{^F}g^{v}(s)  \geq 0 \label{E: polynomial polytope point in set 2}
\end{align}$$ This is an polynomial implication of the form [\[E: poly positive implication\]](#E: poly positive implication){reference-type="eqref" reference="E: poly positive implication"}. As $\ensuremath{\mathcal{P}}\subseteq \ensuremath{\mathcal{P}}_{lim}$ is compact polytope, $\ensuremath{\mathcal{P}}$ is Archimedean [@marshall2008positive Theorem 7.1.3] and so we can use Theorem [1](#T: Putinar){reference-type="ref" reference="T: Putinar"} to express condition [\[E: polynomial polytope point in set\]](#E: polynomial polytope point in set){reference-type="eqref" reference="E: polynomial polytope point in set"} as: $$\begin{align}
 \label{E: polytope separation psatz condition}
    a^{T}(s) \ \leftidx{^F}f^{v}(s)  + (b(s)-1) \ \leftidx{^F}g^{v}(s) 
    =
    \lambda_{01}(s) +  \sum_{j=1}^{m} \lambda_{j1}(s)(d_{j}-c^{T}_{j}s) 
    % \underbrace{\lambda_{01}(s) +  \sum_{j=1}^{m} \lambda_{j1}(s)(d_{j}-c^{T}_{j}s)}_{\Lambda_{1}(s, C, d)},
\end{align}$$ where $\lambda_{j1}, j=0,\hdots, m$ are all SOS polynomials.

The condition [\[E: polynomial round in set\]](#E: polynomial round in set){reference-type="eqref" reference="E: polynomial round in set"}, can be expressed as a polynomial, matrix inequality using the Schur complement[^7] [@boyd2004convex] $$\begin{align}
 \label{E: shur complement implication}
    s \in \ensuremath{\mathcal{P}}\implies
    \begin{bmatrix}
        \left((a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)\right)I_{3} & ra(s) \ \leftidx{^F}g^{o}(s) \\ r(a(s))^T \ \leftidx{^F}g^{o}(s) & (a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)
    \end{bmatrix}
    \succeq 0.
\end{align}$$ This is known as a *matrix SOS* condition which can be represented as a set of semidefinite constraints [@nie2011polynomial]. Specifically, by introducing a vector auxillary variable $u$, we can write [\[E: shur complement implication\]](#E: shur complement implication){reference-type="eqref" reference="E: shur complement implication"} as: $$\begin{multline}
s \in \ensuremath{\mathcal{P}}, u^{T}u = 1 \implies
\\
u^{T}
    \begin{bmatrix}
        \left(a^{T}(s) \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)\right)I_{3} & ra(s) \ \leftidx{^F}g^{o}(s) \\ r(a(s))^T\ \leftidx{^F}g^{o}(s) & (a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)
    \end{bmatrix}
    u
    \geq 0
\end{multline}$$ which can be expressed as the SOS condition: $$\begin{multline}
\label{E: psatz round}
u^{T}
    \begin{bmatrix}
        \left((a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)\right)I_{3} & ra(s) \ \leftidx{^F}g^{o}(s) \\ r(a(s))^T\ \leftidx{^F}g^{o}(s) & (a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)
    \end{bmatrix}
    u = 
    \\
    \lambda_{02}(u,s) + \sum_{j=1}^{m} \lambda_{j2}(u,s)(d_{j}-c^{T}_{j}s) + \phi(u,s)(1-u^{T}u)
    % \underbrace{\lambda_{02}(u,s) + \sum_{j=1}^{m} \lambda_{j2}(s)(d_{j}-c^{T}_{j}s) + \phi(u,s)(1-u^{T}u)}_{\Phi_{2}(s,C,d)} 
    % \\
    % \lambda_{i} \in \bSigma
\end{multline}$$ where $\lambda_{j2}$ are all SOS polynomials, and $\phi \in \ensuremath{\mathbb{R}}[u,s]$. We introduce the additional equality $u^Tu = 1$ to make the set $\{(u, s) | s\in\ensuremath{\mathcal{P}}, u^Tu=1\}$ an Archimedean set.

We are now ready to describe our convex program certifying that $\ensuremath{\mathcal{P}}$ is a region of TC-space containing no collision. For each pair of bodies $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ which can collide in the scene, we search for a polynomial hyperplane via the optimization program: $$\label{E: cert by hyperplane poly}
\begin{gather} 
    {\forall~ \text{pairs } \ensuremath{\mathcal{A}},\ensuremath{\mathcal{B}}} ~\ensuremath{\textbf{Find }}a_{\ensuremath{\mathcal{A}},\ensuremath{\mathcal{B}}}, b_{\ensuremath{\mathcal{A}},\ensuremath{\mathcal{B}}}
    ~~\textbf{subject to}
    \\
    \forall~s \in \ensuremath{\mathcal{P}}, ~ a^{T}_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)x + b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s) > 0, ~\forall x \in \ensuremath{\mathcal{A}}(s) \label{E: cert by hyperplane poly A}
    \\
    \forall~s \in \ensuremath{\mathcal{P}}, ~  a^{T}_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)y + b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s) < 0 ~\forall y \in \ensuremath{\mathcal{B}}(s) \label{E: cert by hyperplane poly B}
    \\
    \lambda_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u,s),~ \mu_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u,s) \in \ensuremath{\bm{\Sigma}}, ~ \phi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u,s),~ \chi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u,s) \in \ensuremath{\mathbb{R}}[u,s] \label{E: cert by hyperplane multiplier constraint}
    % \Lambda_{\calA, \calB}(s,v_{\calA}), \Omega_{\calA, \calB}(s,v_{\calB}) \in \bSigma \label{E: multiplier PSD}
\end{gather}$$ where $(a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s),b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s))$ are the parameters of the polynomial hyperplane separating $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$, the polynomials $\lambda_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)$ and $\phi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)$ collect all the multiplier polynomials for enforcing [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"}, and $\mu_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)$ and $\chi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)$ collect all the multiplier polynomials for enforcing [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} by using [\[E: polytope separation psatz condition\]](#E: polytope separation psatz condition){reference-type="eqref" reference="E: polytope separation psatz condition"} and [\[E: psatz round\]](#E: psatz round){reference-type="eqref" reference="E: psatz round"} depending on the geometry of $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. We stress in the above program that the decision variables are the *coefficients* of the polynomials $a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}$, $b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}$, and the multiplier polynomials. The symbols $u$ and $s$ are known as *indeterminates* and are not explicitly searched over.

In Table [18](#Tab: poly point in set){reference-type="ref" reference="Tab: poly point in set"}, we summarize the conditions for enforcing [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"} and [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} for common families of sets. We call a feasible solution to [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} a *certificate* for the polytope $\ensuremath{\mathcal{P}}$ which we denote: $$\begin{align}
\label{E: hyperplane certificate}
    \ensuremath{\mathcal{C}}_{\ensuremath{\mathcal{P}}} = \bigcup_{(\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}})} \{a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s),~b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s),~\lambda_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u, s),~\phi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u, s), ~\mu_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u, s),~\chi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(u, s)\}
\end{align}$$

::: {#Tab: poly point in set}
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---+
|                                                                                                                                                                                                                                                                                                                                                                                                                |   |
+:===============================================================================================================================================================================================================================================================================================================================================================================================================+:==+
| ::: {#Tab: poly point in set}                                                                                                                                                                                                                                                                                                                                                                                  |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|                                                                                                                                                                                                                                                                                                                                                                                                                |   |
|   : SOS conditions for the constraint [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"} and [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} depending on the geometry of bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. |   |
| :::                                                                                                                                                                                                                                                                                                                                                                                                            |   |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---+
| ::: {#Tab: poly point in set}                                                                                                                                                                                                                                                                                                                                                                                  |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|                                                                                                                                                                                                                                                                                                                                                                                                                |   |
|   : SOS conditions for the constraint [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"} and [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} depending on the geometry of bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. |   |
| :::                                                                                                                                                                                                                                                                                                                                                                                                            |   |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---+
| ::: {#Tab: poly point in set}                                                                                                                                                                                                                                                                                                                                                                                  |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|                                                                                                                                                                                                                                                                                                                                                                                                                |   |
|   : SOS conditions for the constraint [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"} and [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} depending on the geometry of bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. |   |
| :::                                                                                                                                                                                                                                                                                                                                                                                                            |   |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---+
| ::: {#Tab: poly point in set}                                                                                                                                                                                                                                                                                                                                                                                  |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|   --                                                                                                                                                                                                                                                                                                                                                                                                           |   |
|                                                                                                                                                                                                                                                                                                                                                                                                                |   |
|   : SOS conditions for the constraint [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"} and [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} depending on the geometry of bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. |   |
| :::                                                                                                                                                                                                                                                                                                                                                                                                            |   |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---+

: SOS conditions for the constraint [\[E: cert by hyperplane poly A\]](#E: cert by hyperplane poly A){reference-type="eqref" reference="E: cert by hyperplane poly A"} and [\[E: cert by hyperplane poly B\]](#E: cert by hyperplane poly B){reference-type="eqref" reference="E: cert by hyperplane poly B"} depending on the geometry of bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$.
:::

## Polynomial Infeasibility Certificates {#S: infeasible non-collision cert}

As we remarked in section [3.1](#S: separating convex bodies){reference-type="ref" reference="S: separating convex bodies"}, non-collision of two convex shapes $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ can be checked by certifying the *infeasibility* of [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"}. The infeasibility of [\[E: intersection via same point generic\]](#E: intersection via same point generic){reference-type="eqref" reference="E: intersection via same point generic"} can be extended to the case when the locations of $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ are a function of $s$. $$\label{E: dual psatz poly cert abstract}
    \begin{gather} 
    \textbf{Certify that } \nexists~ s \in \ensuremath{\mathcal{P}},~ x, y \in \ensuremath{\mathbb{R}}^{3} \textbf{ such that} \\
    x \in \ensuremath{\mathcal{A}}(s), y \in \ensuremath{\mathcal{B}}(s) \label{E: in set constraint generic poly}
    \\
    x = y \label{E: same point constraint generic poly}
\end{gather}$$

An equivalent, and perhaps more instructive, way of expressing [\[E: dual psatz poly cert abstract\]](#E: dual psatz poly cert abstract){reference-type="eqref" reference="E: dual psatz poly cert abstract"} is to consider the set $$\begin{align}
    \ensuremath{\mathcal{S}}_{\ensuremath{\mathcal{P}}, \ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}} &= \{x, s \mid s \in \ensuremath{\mathcal{P}},~x \in \ensuremath{\mathcal{A}}(s),~x \in \ensuremath{\mathcal{B}}(s)\} \label{E: set to prove infeasible}
    \\
    &=
    \left\{x,~ s,~ u_{\ensuremath{\mathcal{A}}},~ u_{\ensuremath{\mathcal{B}}~}~ \middle |~
    \begin{gathered}
    Cs \leq d,
    \\
    \gamma_{i}^{\ensuremath{\mathcal{A}}}(s, x, u_{\ensuremath{\mathcal{A}}}) \geq 0,
    ~ h_{j}^{\ensuremath{\mathcal{A}}}(s,x, u_{\ensuremath{\mathcal{A}}}) = 0
    \\
    \gamma_{k}^{\ensuremath{\mathcal{B}}}(s, x, u_{\ensuremath{\mathcal{B}}}) \geq 0,
    h_{l}^{\ensuremath{\mathcal{B}}}(s, x, u_{\ensuremath{\mathcal{B}}}) = 0,
    \\
    ~i \in [n_{\ensuremath{\mathcal{A}}}], ~j \in [m_{\ensuremath{\mathcal{A}}}],
    ~k \in [n_{\ensuremath{\mathcal{B}}}], ~l \in [m_{\ensuremath{\mathcal{B}}}]
    \end{gathered}
    \right\}
    \label{E: set to prove infeasible explicit}
\end{align}$$ and to consider the problem $$\begin{align}
 \label{E: opt prove infeasible abstract}
\textbf{Certify that } \ensuremath{\mathcal{S}}_{\ensuremath{\mathcal{P}}, \ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}} = \emptyset,
\end{align}$$

In [\[E: set to prove infeasible explicit\]](#E: set to prove infeasible explicit){reference-type="eqref" reference="E: set to prove infeasible explicit"}, $\gamma_{i}^{\ensuremath{\mathcal{A}}}(s, x, u_{\ensuremath{\mathcal{A}}})$ and $h_{j}^{\ensuremath{\mathcal{A}}}(s, x, u_{\ensuremath{\mathcal{A}}})$ are the polynomials encoding the condition that $x \in \ensuremath{\mathcal{A}}(s)$ and $u_{\ensuremath{\mathcal{A}}}$ collects any extra variables needed to write this condition. Similarly, $u_{\ensuremath{\mathcal{B}}}$, $\gamma_{k}^{\ensuremath{\mathcal{B}}}(s, x, u_{\ensuremath{\mathcal{B}}})$, and $h_{l}^{\ensuremath{\mathcal{B}}}(s, x, u_{\ensuremath{\mathcal{B}}})$ encode that $x \in \ensuremath{\mathcal{B}}(s)$. We provide explicit expressions for $\gamma_{i}^{\ensuremath{\mathcal{A}}}, \gamma_{k}^{\ensuremath{\mathcal{B}}}$ and $h_j^{\ensuremath{\mathcal{A}}}, h_l^{\ensuremath{\mathcal{B}}}$ in Table [31](#Tab: shape conditions table poly){reference-type="ref" reference="Tab: shape conditions table poly"} (given in Appendix [11](#A: Semialgebraic Set Memebership){reference-type="ref" reference="A: Semialgebraic Set Memebership"}) for a few common geometries.

::: example
**Example 2**. *If $\ensuremath{\mathcal{A}}$ is a polytope with $n_{\ensuremath{\mathcal{A}}}$ vertices given by $v_{\ensuremath{\mathcal{A}}_{i}}$, and $\ensuremath{\mathcal{B}}$ is a sphere with center $o_{\ensuremath{\mathcal{B}}}$ and radius $r_{\ensuremath{\mathcal{B}}}$, then we can write $$\begin{align*}
\ensuremath{\mathcal{S}}_{\ensuremath{\mathcal{P}}, \ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}
    &=
    \left\{x,~ s,~ \mu_{\ensuremath{\mathcal{A}}_{i}} ~\middle |~
    \begin{gathered}
    Cs \leq d,
    \\
    %\calA eqs
    \left(\prod_{i}\leftidx{^F}g^{v_{\ensuremath{\mathcal{A}}_i}}\right) \left(x-
         \sum_{i=1}^{m} \mu_{\ensuremath{\mathcal{A}}_i}\left(\frac{\leftidx^{F}f^{v_{\ensuremath{\mathcal{A}}_i}}(s)}{\leftidx^{F}g^{v_{\ensuremath{\mathcal{A}}_i}}(s)} \right)\right) = 0 ,
         \\
    1 - \sum_{i=1}^{m} \mu_{\ensuremath{\mathcal{A}}_i}    = 0,
    \\
    \mu_{\ensuremath{\mathcal{A}}_i} \geq 0 ~ \forall ~ i \in [n_{\ensuremath{\mathcal{A}}}],
    %end \calA eqs
    \\
    \left(\leftidx^{F}g^{o_{\ensuremath{\mathcal{B}}}}(s)\right)^{2}
    \left(r_{\ensuremath{\mathcal{B}}}^{2}- \ensuremath{\left\| x - \frac{\leftidx^{F}f^{o_{\ensuremath{\mathcal{B}}}}(s)}{\leftidx^{F}g^{o_{\ensuremath{\mathcal{B}}}}(s)} \right\|}^{2}\right)
    \geq 0
    \end{gathered}
    \right\}
\end{align*}$$*
:::

Now, we note that $\ensuremath{\mathcal{S}}_{\ensuremath{\mathcal{P}}, \ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}$ is an Archimedean set. This implies that we can use Theorem [2](#T: Putinar Dual){reference-type="ref" reference="T: Putinar Dual"} to write [\[E: opt prove infeasible abstract\]](#E: opt prove infeasible abstract){reference-type="eqref" reference="E: opt prove infeasible abstract"} as an optimization problem. Denoting $u = \{u_{\ensuremath{\mathcal{A}}}, u_{\ensuremath{\mathcal{B}}}\}$, this can be written explicitly as

$$\label{E: dual psatz poly cert}
\begin{gather} 
    \ensuremath{\textbf{Find }}\lambda_{0},~\lambda_{j}^{\ensuremath{\mathcal{P}}},~ \lambda_{j}^{\ensuremath{\mathcal{A}}},~ \lambda_{j}^{\ensuremath{\mathcal{B}}}, ~ \phi_{k}^{\ensuremath{\mathcal{A}}},~ \phi_{k}^{\ensuremath{\mathcal{B}}}
    \\
    \begin{multlined}
    -1 =
    \lambda_{0}(s,x,u) +  \sum_{j=1}^{n}\lambda_{j}^{\ensuremath{\mathcal{P}}}(s,x,u)(d_{j} - c^{T}_{j}s)
    + \\
    \sum_{i = 1}^{n_{\ensuremath{\mathcal{A}}}}
    \lambda_{i}^{\ensuremath{\mathcal{A}}}(s,x,u)\gamma_{i}^{\ensuremath{\mathcal{A}}}(s,x,u_{\ensuremath{\mathcal{A}}}) +
    \sum_{j = 1}^{m_{\ensuremath{\mathcal{A}}}}
    \phi_{j}^{\ensuremath{\mathcal{A}}}(s,x,u)h_{j}^{\ensuremath{\mathcal{A}}}(s,x,u_{\ensuremath{\mathcal{A}}}) 
    + \\
    \sum_{l = 1}^{n_{\ensuremath{\mathcal{B}}}}
    \lambda_{l}^{\ensuremath{\mathcal{B}}}(s,x,u)\gamma_{l}^{\ensuremath{\mathcal{B}}}(s,x,u_{\ensuremath{\mathcal{B}}}) +
    \sum_{k = 1}^{m_{\ensuremath{\mathcal{B}}}}
    \phi_{k}^{\ensuremath{\mathcal{B}}}(s,x,u)h_{k}^{\ensuremath{\mathcal{B}}}(s,x,u_{\ensuremath{\mathcal{B}}}) 
    \end{multlined}
    \label{E: dual psatz poly cert -1 constraint}
    \\
    \lambda_{0},~\lambda_{j}^{\ensuremath{\mathcal{P}}},~ \lambda_{i}^{\ensuremath{\mathcal{A}}},~ \lambda_{l}^{\ensuremath{\mathcal{B}}} \in \ensuremath{\bm{\Sigma}}
    \label{E: dual psatz poly cert psd constraint}
    \\
    \phi_{j}^{\ensuremath{\mathcal{A}}},~ \phi_{k}^{\ensuremath{\mathcal{B}}} \in \ensuremath{\mathbb{R}}[s,x,u]
    \label{E: dual psatz poly cert free poly constraint}
\end{gather}$$

We again emphasize that in program [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} the decision variables are the coefficients of $\lambda_{0},~ \lambda_{j}^{\ensuremath{\mathcal{P}}},~  \lambda_{i}^{\ensuremath{\mathcal{A}}},~ \lambda_{l}^{\ensuremath{\mathcal{B}}},~ \phi_{j}^{\ensuremath{\mathcal{A}}},~ \text{and }\phi_{k}^{\ensuremath{\mathcal{B}}}$, while the symbols $\{x,s,u\}$ are not decision variables but rather polynomial indeterminates. Similar to the program in [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"}, a certificate of non-collision can be obtained by solving [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} for each pair $(\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}})$ with the multipliers acting as the certificate.

## Power of the Certification Programs {#S: cert power}

In this section, we consider the power of both certification programs. Specifically, in Sections [4.1](#S: Hyperplane Cert){reference-type="ref" reference="S: Hyperplane Cert"} and [4.2](#S: infeasible non-collision cert){reference-type="ref" reference="S: infeasible non-collision cert"} we argued that feasibility of [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} are sufficient to prove that $\ensuremath{\mathcal{P}}$ is collision-free. In this section, we present two theorems showing that the feasibility of these programs is also *necessary*.

Such a result is important given the fact that as stated, [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} are infinite dimensional and therefore in practice must be solved by selecting a basis of finite degree for the polynomials. Other subtleties about the power of our formulation are discussed in Appendix [13](#A: necessary and sufficient){reference-type="ref" reference="A: necessary and sufficient"}. Fortunately, we can prove that there do exist finite degrees such that both programs become feasible when $\ensuremath{\mathcal{P}}$ is truly collision-free.

::: {#T: hyperplane poly cert is always feasible .theorem}
**Theorem 3**. *Let all multiplier polynomials from [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} have degree at least $\rho$ and let all of the polynomials in the parameterization of the hyperplane have degree at least $\kappa$. Suppose $\ensuremath{\mathcal{P}}\subseteq \ensuremath{\mathcal{P}}_{lim}$ is a subset of TC-free.*

*Then there exists finite $\kappa$ and $\rho$ sufficiently large such that [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} is feasible.*
:::

A similar theorem can be stated for the program in [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"}.

::: {#T: dual psatz poly cert is always feasible .theorem}
**Theorem 4**. *Let $\ensuremath{\mathcal{P}}\subseteq \ensuremath{\mathcal{P}}_{lim}$ be a compact, polytopic subset of TC-free and let all multiplier polynomials from [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} have degree at least $\rho$. There exists a finite $\rho$ sufficiently large such that [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} is feasible.*
:::

We delay the proofs and further discussion of these results to Appendix [13](#A: necessary and sufficient){reference-type="ref" reference="A: necessary and sufficient"}. For now, we simply remark that Theorems [3](#T: hyperplane poly cert is always feasible){reference-type="ref" reference="T: hyperplane poly cert is always feasible"} and [4](#T: dual psatz poly cert is always feasible){reference-type="ref" reference="T: dual psatz poly cert is always feasible"} assert that the certification programs presented in this section are both complete in the sense that any collision-free polytope $\ensuremath{\mathcal{P}}$ can be certified with our technique.

# Polyhedral Decomposition of TC-free {#S: Bilinear Alternation}

In this section, we describe our algorithm for rapidly generating certified, polyhedral decomposition of TC-free. Our algorithm can be seen as a generalization of the  algorithm of [@deits2015computing] to non-convex TC-space obstacles and so we name it  (Configuration-Space, Iterative Regional Inflation by Semidefinite programming). The key idea is to iteratively grow certified convex polytopes of increasing size around various important configurations in the TC-space. This is achieved by solving a series of convex optimization programs. The complete algorithm is summarized in Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}.

We begin by discussing how we will measure the size of our polytope $\ensuremath{\mathcal{P}}=\{s \mid Cs\le d\}$. While it may be attractive to measure the size of a polytope by its volume, it is known that computing the volume of a half-space representation (H-Rep) polytope is #P-hard[^8] [@dyer1988complexity] and therefore intractable as an objective. A useful surrogate for the volume of $\ensuremath{\mathcal{P}}$ used in [@deits2015computing] is the volume of the maximum volume inscribed ellipse of $\ensuremath{\mathcal{P}}$: the set $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}} = \{Qs + s_{0}\mid \ensuremath{\left\| s \right\|}_2 \leq 1\}$ where $Q$ is a positive-semidefinite matrix describing the shape of the ellipsoid and $s_{0}$ its center. The problem of finding the maximum volume inscribed ellipsoid in a polytope is a semidefinite program described in [@boyd2004convex Section 8.4.2]. $$\label{E: max inscribed ellipse in polytope}
\begin{gather}
\ensuremath{\boldsymbol\max}_{Q, s_0}~ \ensuremath{\text{logdet}}Q ~\mathop{\mathrm{\textbf{subject\ to}}}
    \\
    \ensuremath{\left\| Qc_{i} \right\|}_{2} \leq d_{i} - c_{i}^Ts_{0} ~~\forall~ i\in [m]
    \label{E: ellipse in polytope}
    \\
    Q \succeq 0 \label{E: ellipse psd}
\end{gather}$$

As we wish our polytopes to cover diverse areas of TC-free, we will grow each polytope $\ensuremath{\mathcal{P}}$ around some nominal configuration $s_{s}$ we call the seed point. New seed points are typically chosen using rejection sampling to obtain a point outside of the existing certified regions. The polytope $\ensuremath{\mathcal{P}}$ is required to contain $s_{s}$ as it grows.

A maximal volume, certified polytope around $s_{s}$ can be obtained by solving the following optimization program which combines the ellipsoidal program [\[E: max inscribed ellipse in polytope\]](#E: max inscribed ellipse in polytope){reference-type="eqref" reference="E: max inscribed ellipse in polytope"} with the certification program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} from Section [4.1](#S: Hyperplane Cert){reference-type="ref" reference="S: Hyperplane Cert"}.

$$\label{E: bilinear program}
\begin{gather}
    \ensuremath{\boldsymbol\max}_{
    \substack{
    Q, s_0, C, d,
    \\
    \forall (\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}})
    \\
    \lambda_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~ \phi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},
    \\
    \mu_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~ \chi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}
    \\
    a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~ b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}}}~ \ensuremath{\text{logdet}}Q ~\mathop{\mathrm{\textbf{subject\ to}}}
    \\
    \eqref{E: ellipse in polytope}, \eqref{E: ellipse psd} \label{E: max inscribed ellipse in polytope constraints}
    \\
    Cs_{s} \leq d\label{E: cert with ellipse contain sample}
    \\ 
    ~\ensuremath{\left\| c_{i} \right\|}_{2}  \leq 1 ~\forall~ i \in [m]
    \label{E: polytope scaling}
    \\
    \eqref{E: cert by hyperplane poly A},
    ~\eqref{E: cert by hyperplane poly B},
    ~\eqref{E: cert by hyperplane multiplier constraint}
    \label{E: poly sep condition}
    \end{gather}
    \label{E: cert with ellipse}$$ The condition $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}}\subset\ensuremath{\mathcal{P}}$ is given by the constraints [\[E: max inscribed ellipse in polytope constraints\]](#E: max inscribed ellipse in polytope constraints){reference-type="eqref" reference="E: max inscribed ellipse in polytope constraints"}. Constraint [\[E: cert with ellipse contain sample\]](#E: cert with ellipse contain sample){reference-type="eqref" reference="E: cert with ellipse contain sample"} enforces that $\ensuremath{\mathcal{P}}$ grows around $s_{s}$. The added constraint [\[E: polytope scaling\]](#E: polytope scaling){reference-type="eqref" reference="E: polytope scaling"} prevents numerically undesirable scaling. Finally, [\[E: poly sep condition\]](#E: poly sep condition){reference-type="eqref" reference="E: poly sep condition"} enforces that we search for hyperplanes $(a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s), b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s))$ which separate each collision pair $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$.

While this program is attractive as a specification, it is not convex due to bilinearity between $Q$ and $c_i$ in [\[E: ellipse in polytope\]](#E: ellipse in polytope){reference-type="eqref" reference="E: ellipse in polytope"} and the bilinearity between the multipliers and the defining equations of $\ensuremath{\mathcal{P}}$ implicit in [\[E: poly sep condition\]](#E: poly sep condition){reference-type="eqref" reference="E: poly sep condition"} (see Section [4.1](#S: Hyperplane Cert){reference-type="ref" reference="S: Hyperplane Cert"}). This bilinearity precludes simultaneous search of the polytope $\ensuremath{\mathcal{P}}$, inscribed ellipsoid $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}}$, and the corresponding certificate $\ensuremath{\mathcal{C}}_{\ensuremath{\mathcal{P}}}$. Therefore, we will approximate the solution to [\[E: bilinear program\]](#E: bilinear program){reference-type="eqref" reference="E: bilinear program"} by alternating between two convex programs; one of which will generate certificates of non-collision and one which will improve our polytope without violating the previous certificate.

::: remark
**Remark 3**. *It is possible to replace [\[E: poly sep condition\]](#E: poly sep condition){reference-type="eqref" reference="E: poly sep condition"} with the equivalent constraints from program [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"}. We prefer to base our algorithm on [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} as it can be visualized (i.e. planes in the task space) and the polynomials contain fewer indeterminates and hence the optimization problem size is smaller. Also the separating planes approach produces separating certificates with quantifiable margins by measuring the distance from the collision geometries to the plane in task space.*
:::

We begin by demonstrating how a certified polytopic region can be improved. Suppose that a convex polytope $\ensuremath{\mathcal{P}}= \{s|Cs \leq d\}$ has been certified with certificate $\ensuremath{\mathcal{C}}_{\ensuremath{\mathcal{P}}}$ and the maximum inscribed ellipse $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}}$ has been computed using [\[E: max inscribed ellipse in polytope\]](#E: max inscribed ellipse in polytope){reference-type="eqref" reference="E: max inscribed ellipse in polytope"}. A new, larger polytope $\ensuremath{\mathcal{P}}'$ can be found by solving the convex optimization program [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} which pushes the faces of $\ensuremath{\mathcal{P}}'$ as far away from the surface of $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}}$ without violating the certificate $\ensuremath{\mathcal{C}}_{\ensuremath{\mathcal{P}}}$. This procedure is visualized in Figure [3](#F: pushback){reference-type="ref" reference="F: pushback"}.

:::: {#F: pushback .figure}
::: caption
In [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} we search for the maximum amount the polytopes faces can be pushed away from the current inscribed ellipse without violating the certificate found in the previous step.
:::
::::

This can be achieved with the following optimization program: $$\label{E: polytope growth program}
\begin{gather}
    \max_{
    \substack{
    C, d, \delta, 
    \\
    \forall (\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}})
    \\
    \lambda_{01}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~ \lambda_{02}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~  \phi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}
    \\
    \mu_{01}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~ \mu_{02}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}} ,~ \chi^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}
    \\
    a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}},~ b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}}
    }~ \prod_{i=1}^{m} (\delta_{i} + \varepsilon_{0}) ~\mathop{\mathrm{\textbf{subject\ to}}}
    \\
    \ensuremath{\left\| Qc_{i} \right\|}_{2} \leq d_{i} - \delta_{i} - c_{i}^Ts_{0}, ~ \delta_{i} \geq 0 ~\forall~ i\in [m]
    \\
    \eqref{E: cert with ellipse contain sample}, \eqref{E: polytope scaling},
    \eqref{E: poly sep condition}~ \forall \text{pairs } (\ensuremath{\mathcal{A}}(s), \ensuremath{\mathcal{B}}(s))
        \label{E: growth sep constraints}
\end{gather}$$ where $\varepsilon_{0} > 0$ is some positive constant ensuring that the objective is never $0$. We recall that [\[E: growth sep constraints\]](#E: growth sep constraints){reference-type="eqref" reference="E: growth sep constraints"} is either a constraint of the form [\[E: polytope separation psatz condition\]](#E: polytope separation psatz condition){reference-type="eqref" reference="E: polytope separation psatz condition"} or [\[E: psatz round\]](#E: psatz round){reference-type="eqref" reference="E: psatz round"}. We emphasize that in [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"}, $\lambda_{i1}, \lambda_{i2}, \mu_{i1}, \mu_{i2}, i\ge 1$ are all fixed and it is the variables $c_{j}$ and $d_{j}$ which are searched over.

::: algorithm
$i \gets 0$\
$(\ensuremath{\mathcal{P}}_{i}, \ensuremath{\mathcal{C}}_{\ensuremath{\mathcal{P}}_{i}})$
:::

Our complete algorithm proceeds in three steps. First, an initial, collision-free polytope $\ensuremath{\mathcal{P}}_{0}$ containing a seed point $s_{s}$ is certified using [\[E: hyperplane certificate\]](#E: hyperplane certificate){reference-type="eqref" reference="E: hyperplane certificate"} to obtain $\ensuremath{\mathcal{C}}_{\ensuremath{\mathcal{P}}_{0}}$. Next, the maximum inscribed ellipsoid $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}_{0}}$ is computed using [\[E: max inscribed ellipse in polytope\]](#E: max inscribed ellipse in polytope){reference-type="eqref" reference="E: max inscribed ellipse in polytope"}. Finally, $\ensuremath{\mathcal{P}}_{0}$ is improved using [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} to obtain a new polytope $\ensuremath{\mathcal{P}}_{1}$. This polytope $\ensuremath{\mathcal{P}}_{1}$ has the same number of defining inequalities as $\ensuremath{\mathcal{P}}_{0}$. We iterate this process until the volume of $\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}}$ stops improving. This algorithm is formalized in Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}. Every step of this process involves solving an *convex program* for which very fast, commercial solvers exist [@mosek; @andersen2000mosek].

::: remark
**Remark 4**. *Some practical considerations for improving the runtime of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} are discussed in the appendices. Specifically, in Appendix [14](#A: Practical Aspects){reference-type="ref" reference="A: Practical Aspects"} we expand on design choices which substantially impact the size of the optimization programs as well as which part of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} can be parallelized. Additionally, in Appendix [15](#A: Seeding){reference-type="ref" reference="A: Seeding"} we discuss a heuristic strategy for proposing a large, initial regions $\ensuremath{\mathcal{P}}_{0}$.*
:::

# Results {#S: Results}

We demonstrate the use of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} on systems of varying complexity. We begin with very simple robots where both the task and configuration space can be visualized and demonstrate that our algorithm can find very large portions of TC-space and achieve near-complete coverage for simple systems in reasonable time.

We then demonstrate the use of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} on various robots commonly found in industry. These include a KUKA iiwa reaching into a shelf, a bimanual KUKA iiwa, and similar setups for the Franka UR3. Our objective is show the scalability of our algorithm in realistic settings as well as demonstrate the diversity of shapes our approach can handle.

A mature implementation of our algorithm is available in the open-source robotics toolbox [Drake](https://drake.mit.edu/) [@drake]. We furthermore provide examples of our algorithm in interactive [Python notebooks](https://deepnote.com/workspace/alexandre-amice-c018b305-0386-4703-9474-01b867e6efea/project/C-IRIS-7e82e4f5-f47a-475a-aad3-c88093ed36c6/notebook/2d_example_bilinear_alternation-14f1ee8c795e499ca7f577b6885c10e9). Animations of various figures in this section can also be found on this project's [website](https://alexandreamice.github.io/project/c-iris).

The implementation details of all experiments in this section, such as the choice of reference frame for each plane, the degree of the polynomials parametrizing the hyperplanes, and the degree of the multipliers polynomials in each program are expounded on in Appendix [14](#A: Practical Aspects){reference-type="ref" reference="A: Practical Aspects"}.

## Simple Robots {#S: Simple Robots}

In this section, we consider two simple robots each containing only two degrees of freedom. This enables us to visualize both the task space, as well as the configuration space. Though containing few degrees of freedom, each environment maintains rich, realistic collision geometries.

### Pendulum on a Rail {#S: Pend on Rail}

:::::: {#F: pend on rail .figure latex-placement="htb"}
::: minipage
[]{#F: pend on rail task space label="F: pend on rail task space"}
:::

::: minipage
[]{#F: pend on rail cspace label="F: pend on rail cspace"}
:::

::: caption
A 2-DOF robot consisting of a revolute joint at the base of the orange link and a prismatic joint between the base and the box.
:::
::::::

Our first robot shown in Figure [\[F: pend on rail task space\]](#F: pend on rail task space){reference-type="ref" reference="F: pend on rail task space"} consists of a single arm, shown in orange, connected to a base via a revolute joint and placed within a box. The base of the robot is connected to the box via a prismatic joint. The collision geometries of the robot and box are approximated using polytopic boxes. A total of $42$ pairs of geometries can collide in this scene (i.e. certifying non-collision requires solving $42$ instances of either [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} or [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"}). In Figure [\[F: pend on rail cspace\]](#F: pend on rail cspace){reference-type="ref" reference="F: pend on rail cspace"}, we visualize the two dimensional tangent configuration space of our robot with the TC-space obstacle shown in red. We emphasize the highly non-convex shape of TC-free.

We run Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} starting with a regular octagon of side length $0.01$ centered at the configuration $(0,0)$, a configuration with the arm fully extended upwards and centered in the box. We obtain a sequence of certified polytopes of increasing size in the TC-space which are plotted in varying colors in Figure [\[F: pend on rail cspace\]](#F: pend on rail cspace){reference-type="ref" reference="F: pend on rail cspace"}.

The algorithm terminates after 86 iterations of the while loop from Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} taking a total of 314 seconds of wall time. During the course of the algorithm, the volume of the maximum inscribed ellipsoid improves by a factor of $83$, from a starting value of $0.021$ to $1.746$. The improvement in the volume of the inscribed ellipsoid, as well as the average time to solve both the certification program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} are reported in Figure [5](#F: pend on rail volume improvement){reference-type="ref" reference="F: pend on rail volume improvement"} and Table [7](#F: pend on rail stats){reference-type="ref" reference="F: pend on rail stats"} respectively.

After completion, we select a single random configuration within our final certified region. In Figure [4](#F: pend on rail){reference-type="ref" reference="F: pend on rail"}, we highlight the tip of the pendulum in black. Additionally, we color each collision body for which the tip can collide in a separate color and plot the separating plane certificate between the tip and the body in the same color.

:::: {#F: pend on rail stats .figure latex-placement="htb"}
![The volume of the maximum inscribed ellipsoids of the TC-free regions shown in Figure [\[F: pend on rail cspace\]](#F: pend on rail cspace){reference-type="ref" reference="F: pend on rail cspace"} is plotted over iterations of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}. This volume grows by a factor of $83$ over the course of 86 iterations Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}.](figures/iiwa_on_rail/pen_rail_vol.pdf){#F: pend on rail volume improvement width="\\textwidth"}

:::: {#F: pend on rail stats .figure}
  Number of collision pairs                                                                                                                               42
  ---------------------------------------------------------------------------------------------------------------------------------------------------- --------
  Size of the largest PSD variable                                                                                                                        2
  Average time to solve [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"}    0.191s
  Average time to solve [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"}    0.423s
  Wall time to grow single region                                                                                                                        314s

::: caption
Statistics dominating the run time of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} for the pendulum on a rail system. The complexity scales with the number of collision geometries as well as the size of the largest PSD matrix variable for enforcing the Psatz conditions in Programs [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"}.
:::
::::

::: caption
The progress of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} on the pendulum on a rail system for a single polytopic region is plotted. Statistics dominating the run time of the algorithm are also reported.
:::
::::

### Pinball Flipper {#S: Pinball}

:::: {#F: pinball cspace .figure}
![The pinball flipper system consists of pendulums each with a revolute joint between the orange link and the gray base. All collision geometries in the scene are approximate using boxes.](Dai2023Certified_figs/pinball_iiwa.png){#F: pinball task space width="98%"}

:::: {#F: pinball cspace .figure}
::: caption
The TC-space of the 2DOF pendulum flipper system. The TC-space obstacle is shown in red. Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} is run for five different polytopes each initially centered around the black dots. The polytopes output by the algorithm are plotted in various colors. These polytopes almost fully cover TC-free and are guaranteed to be collision-free by construction.
:::
::::

::: caption
The pinball flipper system and its TC-space. Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} is successfully able to cover TC-free with polytopic regions. An animation of the regions growing to cover this space is available [here](https://alexandreamice.github.io/project/c-iris/pinball_growth.html)
:::
::::

We refer to our second system shown in Figure [8](#F: pinball task space){reference-type="ref" reference="F: pinball task space"} as the pinball flipper. Each orange arm is connected to its gray base via a revolute joint. Each collision geometry in the scene is approximated with a box and a total of $130$ collision pairs exist. We similarly plot the TC-space in Figure [10](#F: pinball cspace){reference-type="ref" reference="F: pinball cspace"} with the TC-space obstacle highlighted in red. In this experiment, we attempt to almost completely cover TC-free with polytopic regions in order to enable a motion plan where the flippers exchange positions. Overall, this scene exhibits a much more complicated TC-space obstacle as well as substantially more collision pairs when compared to the system from Section [6.1.1](#S: Pend on Rail){reference-type="ref" reference="S: Pend on Rail"}.

We run Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} seeded with octagonal regions of side length $0.01$, each centered at one of $5$ different configurations shown as the black dots in Figure [10](#F: pinball cspace){reference-type="ref" reference="F: pinball cspace"}. The resulting regions are also plotted in Figure [10](#F: pinball cspace){reference-type="ref" reference="F: pinball cspace"} and almost completely cover the space. Though each region was initially seeded with a polytope of the same shape, our algorithm successfully adapts the shape of each polytope to fill the space. Our algorithm also is not conservative; it successfully finding regions which are tight to the TC-space obstacle in all cases.

The change in volume of the maximum inscribed ellipsoid of each region is shown in Figure [11](#F: pinball vol growth){reference-type="ref" reference="F: pinball vol growth"}. We remark that the volume of each region exhibits a diverse set of behaviors over the iterations. Each region was grown sequentially, with a total wall time to cover the space of $1439$s. This wall time could easily be improved by growing each region in parallel.

In Figure [24](#F: pinball trajectory){reference-type="ref" reference="F: pinball trajectory"}, we demonstrate the behavior of our certificates for various poses of our robot. In the top panel, we highlight in black the two tips of each flipper. The current configuration is highlighted as the green dot in the bottom panel. For each configuration, we also plot the hyperplane that proves the separation between the two black tips. Notice that in Figures [20](#F: pinball cspace1){reference-type="ref" reference="F: pinball cspace1"}, [21](#F: pinball cspace2){reference-type="ref" reference="F: pinball cspace2"}, and [22](#F: pinball cspace3){reference-type="ref" reference="F: pinball cspace3"}, the current configuration is contained in multiple regions at once. Therefore, each hyperplane in Figure [14](#F: pinball traj0){reference-type="ref" reference="F: pinball traj0"} - [18](#F: pinball traj4){reference-type="ref" reference="F: pinball traj4"} is drawn in the same color as its associated TC-space region in Figures [19](#F: pinball cspace0){reference-type="ref" reference="F: pinball cspace0"} - [23](#F: pinball cspace4){reference-type="ref" reference="F: pinball cspace4"}.

We draw attention to the fact that at every configuration $s_{0}$ in TC-free, many different separating hyperplanes exist. The hyperplane obtained by evaluating the output of our certifier at $s_{0}$ is highly dependent on the region which is being certified. For example, in Figure [21](#F: pinball cspace2){reference-type="ref" reference="F: pinball cspace2"}, the blue region corresponds largely to a change in the position of the left flipper, while the green region corresponds largely to a change in the right flipper. We see in Figure [16](#F: pinball traj2){reference-type="ref" reference="F: pinball traj2"}, that the algorithm finds different separating planes for the blue and the green region, even for the same configuration, so as to accommodate the different range of robot motion in each region. For the blue region, which includes a large rotation of the left flipper, the blue plane would continue to separate the left flipper from the right flipper as the left flipper moves. Similarly, the green plane would continue to separate the right flipper from the left as the right flipper moves.

:::: {#F: pinball stats main .figure}
![The volume of the maximum inscribed ellipsoid as the polytope is grown around various seedpoints is improved during Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}. The final polytopes associate to each color are shown in Figure [10](#F: pinball cspace){reference-type="ref" reference="F: pinball cspace"}.](figures/pinball_iiwa/pinball_vol.pdf){#F: pinball vol growth width="98%"}

:::: {#F: pinball stats .figure}
                                                                                                                                   130
  ------------------------------------------------------------------------------------------------------------------------------ --------
                                                                                                                                    2
  [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"}    0.638s
                                                                                                                                  1.319s
                                                                                                                                  1439s

::: caption
Statistics dominating the run time of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} for the pinball flipper system. The complexity scales with the number of collision geometries as well as the size of the largest PSD matrix variable for enforcing the Psatz conditions in Programs [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"}.
:::
::::

::: caption
The progress of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} on the pinball flipper system for each polytopic region is plotted. Statistics dominating the run time of the algorithm are also reported.
:::
::::

:::: {#F: pinball trajectory .figure}
![](Dai2023Certified_figs/task_space0.png){#F: pinball traj0 width="\\textwidth"}

![](Dai2023Certified_figs/task_space1.png){#F: pinball traj1 width="\\textwidth"}

![](Dai2023Certified_figs/task_space2.png){#F: pinball traj2 width="\\textwidth"}

![](Dai2023Certified_figs/task_space3.png){#F: pinball traj3 width="\\textwidth"}

::: {#F: pinball traj4 .figure}
![image](Dai2023Certified_figs/task_space4.png){width="\\textwidth"} []{#F: pinball traj4 label="F: pinball traj4"}
:::

![](Dai2023Certified_figs/cspace_p0.png){#F: pinball cspace0 width="98%"}

![](Dai2023Certified_figs/cspace_p1.png){#F: pinball cspace1 width="98%"}

![](Dai2023Certified_figs/cspace_p2.png){#F: pinball cspace2 width="98%"}

![](Dai2023Certified_figs/cspace_p3.png){#F: pinball cspace3 width="98%"}

![](Dai2023Certified_figs/cspace_p4.png){#F: pinball cspace4 width="98%"}

::: caption
We approximate almost the entirety of TC-free for the robot flipper system using 5 polytopic regions. The top panel shows the hyperplanes certifying that the two black tips of the system do not collide. The bottom panel shows the configuration of the robot as a green dot. An example of this system undergoing a trajectory is available [here](https://alexandreamice.github.io/project/c-iris/pinball_trajectory.html).
:::
::::

## KUKA IIWA robot {#S: iiwa}

In this section we demonstrate our algorithm deployed on the KUKA iiwa arm in two scenes relevant to robot manipulation. The collision geometry of the iiwa is approximated as a union of convex polytopes as are all obstacles in the scene. We begin by considering a single iiwa to demonstrate the practicality of our algorithm before considering a bimanual manipulator to demonstrate the scalability of our approach.

### 7-DOF IIWA With a Shelf {#S: iiwa and shelf}

:::: {#F: collision constraint .figure}
![](Dai2023Certified_figs/iiwa_shelf_upper1.png){width="100%"}

![](Dai2023Certified_figs/iiwa_shelf_upper2.png){width="100%"}

![](Dai2023Certified_figs/iiwa_shelf_upper3.png){width="100%"}

::: caption
7-DOF iiwa example. We highlight one pair of collision geometries (blue on robot gripper and red on the shelf), together with their separating plane (green).
:::
::::

We apply Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} to the scene shown in Figure [25](#F: collision constraint){reference-type="ref" reference="F: collision constraint"}: a 7-DOF KUKA iiwa arm reaching into a shelf. Our approach successfully finds many collision-free configurations, and we plot in green the separating hyperplane certificate between the end-effector, highlighted in blue, and the top shelf highlighted in red.

The run time of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} is dominated by the certification of non-collision between the pairs with the longest kinematic chain, as this leads to the highest degree polynomials and hence semidefinite variables in programs [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"}. For this program, the largest positive semidefinite matrix variable has $16$ rows. Overall, the largest certification program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} takes 54s to solve, while the program [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} takes on average 8s to solve.

In Figure [28](#fig:iiwa_shelf_volume){reference-type="ref" reference="fig:iiwa_shelf_volume"}, we demonstrate the behavior of one certified region. In Figure [26](#F: iiwa multi posture){reference-type="ref" reference="F: iiwa multi posture"}, we show that the configurations of one of our certified polytopic region of TC-space (with 24 faces in the polytope) corresponds to many task-space end-effector positions. The configurations from Figure [26](#F: iiwa multi posture){reference-type="ref" reference="F: iiwa multi posture"} are drawn from a region which grows by a factor of $10,000$ using $11$ iterations of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}. This improvement in volume is reported in Figure [27](#F: iiwa vol growth){reference-type="ref" reference="F: iiwa vol growth"}, where we also compare the volume of the maximum volume inscribed ellipsoid against the volume of the polytopic region.

:::: {#fig:iiwa_shelf_volume .figure}
![The configurations in our certified regions correspond to a wide range of task-space positions. We sample three configurations from the same certified region and plot the corresponding task-space position in different colors.](Dai2023Certified_figs/iiwa_shelf_multiple_postures.png){#F: iiwa multi posture width="1.\\textwidth"}

![A single region for the 7-DOF KUKA iiwa is grown over the course of 11 iterations of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}. We compare the volume of the maximum volume inscribed ellipsoid to the volume of the polytopic region at each iteration and show that the volume improves by a factor of 10,000.](figures/iiwa_shelf_volume.pdf){#F: iiwa vol growth width="1.\\textwidth"}

::: caption
Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} grows certified regions which contain configurations reaching a large portion of the task space. We show that our algorithm is capable of growing the volume of a certified region by a factor 10,000 over the course of just 11 iterations.
:::
::::

### 12-DOF Bimanual KUKA IIWA Example {#S: bimanual iiwa}

We next consider designing regions to avoid self-collision for a robot consisting of two KUKA iiwa arms with the final joint welded (rotation of the final joint does not change the configuration of any geometry for this robot). This robot contains 12-DOF. This system tests the scalability of our algorithm due to the degree of the polynomials involved in the forward kinematics, as well as the complexity of the collision geometries.

Solving the largest certification program in [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} takes 105 minutes, while the program in [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} takes 4 minutes. The increase in solve times compared to the single iiwa environment from Section [6.2.1](#S: iiwa and shelf){reference-type="ref" reference="S: iiwa and shelf"} is best attributed to the increase in the size of the semidefinite variables due to the larger DOF. The largest semidefinite matrix in both programs have $64$ rows and correspond to certifying that the two tips of the iiwas do not collide.

Nonetheless, our algorithm again finds certified, 30-face polytopic regions of TC-space which correspond to a wide range of task-space positions as seen in Figure [29](#F: bimanual iiwa position){reference-type="ref" reference="F: bimanual iiwa position"}. Moreover, the same region is quite tight to the TC-space obstacle; one sampled configuration in the certified region, shown in Figure [30](#F: bimanual close){reference-type="ref" reference="F: bimanual close"}, corresponds to just $7.3$mm of separation between the two arms.

:::: {#Fig: dual_iiwa .figure latex-placement="htb"}
::: {#F: bimanual iiwa position .figure}
![image](Dai2023Certified_figs/dual_iiwa1.png){width="90%"} []{#F: bimanual iiwa position label="F: bimanual iiwa position"}
:::

::: {#F: bimanual close .figure}
![image](Dai2023Certified_figs/dual_iiwa5.png){width="90%"} []{#F: bimanual close label="F: bimanual close"}
:::

::: caption
Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} finds certified polytopic regions of TC-free even for high DOF systems in reasonable times. The algorithm is also not conservative. It finds large regions which correspond to a broad range of task-space positions. Moreover, the regions are very tight to the TC-space obstacle, finding configurations which lead to very small separation between the task-space objects.
:::
::::

## UR3e Robot

In this section, we test our algorithm on a UR3e robot with a gripper mounted at the wrist. The robot's links are approximated by cylinders and we weld the gripper's prismatic joints so that each UR3e has a total of 6 DOFs. This section differs from the KUKA iiwa experiment in Section [6.2](#S: iiwa){reference-type="ref" reference="S: iiwa"} due to the introduction of non-polytopic collision geometries into the scene. Similar to Section [6.2](#S: iiwa){reference-type="ref" reference="S: iiwa"}, we test our approach for a scene where the robot is reaching into a shelf, as well as a bimanual set up.

### 6-DOF UR3e With a Shelf

:::: {#fig:ur_shelf .figure latex-placement="htb"}
::: {#figure:ur_shelf1 .figure}
![image](Dai2023Certified_figs/ur_shelf1.png){width="95%"} []{#figure:ur_shelf1 label="figure:ur_shelf1"}
:::

::: {#figure:ur_shelf2 .figure}
![image](Dai2023Certified_figs/ur_shelf2.png){width="95%"} []{#figure:ur_shelf2 label="figure:ur_shelf2"}
:::

::: {#figure:ur_shelf3 .figure}
![image](Dai2023Certified_figs/ur_shelf3.png){width="95%"} []{#figure:ur_shelf3 label="figure:ur_shelf3"}
:::

::: {#figure:ur_shelf4 .figure}
![image](Dai2023Certified_figs/ur_shelf4.png){width="95%"} []{#figure:ur_shelf4 label="figure:ur_shelf4"}
:::

::: caption
Different postures sampled within one certified TC-space region for a UR3e robot with gripper. The certified-region include both the gripper reaching the red box in the center of the shelf (Fig.[32](#figure:ur_shelf1){reference-type="ref" reference="figure:ur_shelf1"}), retracting from the shelf (Fig.[34](#figure:ur_shelf3){reference-type="ref" reference="figure:ur_shelf3"}), and reaching different regions within the shelf while avoiding the red box (Fig.[33](#figure:ur_shelf2){reference-type="ref" reference="figure:ur_shelf2"} and [35](#figure:ur_shelf4){reference-type="ref" reference="figure:ur_shelf4"}). An animation of the range of configurations attainable in this region are available [here](https://alexandreamice.github.io/project/c-iris/ur_single.html).
:::
::::

In Figure [36](#fig:ur_shelf){reference-type="ref" reference="fig:ur_shelf"}, we consider a UR3e robot reaching into a shelf to grasp a small box shaped object. To simulate a situation where the robot is attempting to pick up the red object, we use Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} to grow a certified, TC-free polytope (with 12 faces) near the object. Figure [36](#fig:ur_shelf){reference-type="ref" reference="fig:ur_shelf"} shows a variety of postures sampled from the final TC-free polytope and demonstrates that within a single region, our robot is able to reach into the shelf to grasp the object, retract away from the shelf, and maneuver within the shelf while avoiding the object.

Similar to Section [6.2.1](#S: iiwa and shelf){reference-type="ref" reference="S: iiwa and shelf"}, the largest semidefinite variables in programs [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} has $16$ rows with program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} taking about $56$s to solve.

### 12-DOF Bimanual UR3e

:::: {#fig:dual_ur .figure latex-placement="htb"}
![](Dai2023Certified_figs/dual_ur_posture1.png){#fig:dual_ur_posture1 width="98%"}

![](Dai2023Certified_figs/dual_ur_posture2.png){#fig:dual_ur_posture2 width="98%"}

::: caption
Top down view of two postures sampled within one certified TC-space region on the dual UR3e platform. In the right figure we highlight the two collision geometries that are separated by only 0.3mm. A dynamic visualization of the range of attainable postures is available by running this [notebook](https://deepnote.com/workspace/alexandre-amice-c018b305-0386-4703-9474-01b867e6efea/project/C-IRIS-7e82e4f5-f47a-475a-aad3-c88093ed36c6/notebook/dual_ur-8fc84da71e494588bbc82350826b417a)
:::
::::

Finally, we demonstrate our algorithm on a dual UR3e platform shown in Figure [39](#fig:dual_ur){reference-type="ref" reference="fig:dual_ur"}. Again, we emphasize that we are able to find large regions of TC-configuration space which correspond to diverse positions in task space with the postures in Figure [37](#fig:dual_ur_posture1){reference-type="ref" reference="fig:dual_ur_posture1"} and [38](#fig:dual_ur_posture2){reference-type="ref" reference="fig:dual_ur_posture2"} being drawn from the same certified region (a 13-face polytope). Moreover, these regions are very tight to the TC-configuration space obstacle with the two bodies highlighted in red in Figure [38](#fig:dual_ur_posture2){reference-type="ref" reference="fig:dual_ur_posture2"} being just $0.3$mm apart. For this example, the largest positive semidefinite matrices in [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} has 128 rows with the largest program taking about $35$ minutes to solve. This program solves faster than the analogous program for the bimanual iiwa from Section [6.2.2](#S: bimanual iiwa){reference-type="ref" reference="S: bimanual iiwa"} because we require fewer polynomial positivity conditions to certify that the UR3e's cylindrical geometries are on a given side of a plane compared to the polytopic approximation used for the iiwa.

# Conclusion {#S: Conclusion}

Understanding the complicated geometry of C-free is an essential step to designing safe, collision-free motion plans. In this work, we presented an approach for describing a rational parametrization of C-free, known as TC-free, using a union of polytopes. Our primary contributions are two Sums-of-Squares program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} which can certify that a polytopic region of TC-space is collision-free, as well as another program [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} which finds a local improvement that increases the size of a TC-free polytope. We prove that feasibility of our certification programs [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} are both necessary and sufficient for proving that a polytopic region of TC-space is collision-free and we combine programs [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} into a practical algorithm for describing TC-free as a union of certified, collision-free polytopes in the TC-space. We deployed our algorithm on both simple and realistic environments and demonstrate that Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} finds large TC-space regions which correspond to diverse positions in task space. We demonstrate that these regions are not conservative and very tight to the TC-space obstacle even for 12-DOF systems by showing postures with just millimeters of separation.

The presented method works for TC-spaces of arbitrary dimensions, makes only very mild assumptions on the kinematics of our robot, and makes no assumptions about the shape of the TC-space obstacles. Moreover, it only relies on the mild assumption that obstacles in the task space are described as unions of convex sets, an assumption that is frequently satisfied whenever a given environment is simulated.

Such certified descriptions of TC-free find practical application in both randomized and optimization-based collision-free motion planning algorithms, providing a means to certify safety of an entire trajectory by checking membership in a set rather than by finite sampling which can be prone to false assertions of safety. Moreover, the convexity of the generated regions is particularly attractive to optimization-based methods such as the GCS framework of [@marcucci2022motion]. Future work intends to further explore these applications as well as practical algorithms for seeding Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} to obtain good coverage of TC-free with few regions.

# Acknowledgement

This work was supported by the MIT Quest For Intelligence.

# Algebraic Kinematics {#A: alg kin}

An in depth review of algebraic kinematics and low order pairs can be found in [@wampler2011numerical Chapter 4]. We include a brief review in this appendix for completeness.

A mechanism composed of $N+1$ links is considered algebraic if each link is connected by one of the following five joints:

- Revolute (R): a 1-DOF joint permitting revolution about an axis of symmetry. An example is a door handle.

- Prismatic (P): a 1-DOF joint permitting translation along an axis. An example is a linear rail.

- Cylindrical (C): a 2-DOF joint permitting both revolution about an axis of symmetry and independent translation along a given axis. An example is the rods of a Foosball table.

- Planar (E): A 3-DOF joint permitting translation and rotation in a two-dimensional plane. An example is hockey puck moving on the surface of the ice.

- Spherical (S): A 3-DOF joint permitting free rotation between two links. An example is the human shoulder.

We recall from Section [3.3](#S: Rat Forward){reference-type="ref" reference="S: Rat Forward"} that the pose of a point $A$ expressed in the reference frame $F$, written as a function of the robot configuration $q$ can be expressed as $$\begin{align}
%\label{E: gen forward kin}
    \begin{bmatrix}
        \leftidx{^F}R^{A}(q) & \leftidx{^F}p^{A}(q) \\
        0_{1 \times 3} & 1 \\
    \end{bmatrix}
    =
    \prod_{i \in \ensuremath{\mathcal{I}}_{F, A}} \leftidx{^{P_{i}}}X^{C_i}(q_{i}) \ \leftidx{^{C_i}} X ^{P_{i+1}}
\end{align}$$ where $\leftidx{^{P_{i}}}X^{C_{i}}(q_{i})$ is a rigid transform describing the relative motion allowed by the $i$^th^ joint. The matrices $\leftidx{^{P_{i}}}X^{C_{i}}(q_{i})$ are in general restriction of the following forms $$\begin{align}
 \label{E: gen low order pair complete}
    \leftidx{^{P_{i}}}X^{C_{i}}(q_{i}) &=
    \begin{cases}
    \begin{bmatrix}
        \cos(\theta_{i}) & -\sin(\theta_{i}) & 0 & x_{i} \\
        \sin(\theta_{i}) &  \cos(\theta_{i}) & 0 & y_{i} \\
        0  & 0  & 1 & z_{i} \\
        0 & 0 & 0 & 1
    \end{bmatrix}
    &
    \text{if $i$\textsuperscript{th} joint is one of R, P, C, or E}
    \\
    \begin{bmatrix}
        U(\psi_{i}) & 0_{3 \times 1} \\ 0 _{1 \times 3} & 1
    \end{bmatrix}
    &
    \text{if $i$\textsuperscript{th} joint is S}
    \end{cases}
\end{align}$$ The specific restrictions for R, P, C, and E joints are given in Table [19](#Tab: gen low order pair complete){reference-type="ref" reference="Tab: gen low order pair complete"}. The matrix $U$ is an element of $SO(3)$ parametrized using Euler angles $\{\phi_{i,x}, \phi_{i,y}, \phi_{i,z}\}$.

::: {#Tab: gen low order pair complete}
   Joint                                                 Restriction                                                               Definition of $q_{i}$
  ------- ---------------------------------------------------------------------------------------------------------- --------------------------------------------------
     R                                           $x_{i} = y_{i} = z_{i} = 0$                                                      $q_{i} = \{\theta_{i}\}$
     P                                         $\theta_{i} = x_{i} = y_{i} = 0$                                                     $q_{i} = \{z_{i}\}$
     C                                               $x_{i} = y_{i} = 0$                                                      $q_{i} = \{\theta_{i}, z_{i}\}$
     E                                                   $z_{i} = 0$                                                       $q_{i} = \{\theta_{i}, x_{i}, y_{i}\}$
     S     see equation [\[E: sphere joint\]](#E: sphere joint){reference-type="eqref" reference="E: sphere joint"}   $q_{i} = \{\phi_{i,x}, \phi_{i,y}, \phi_{i,z}\}$

  : parameterization of algebraic joints in terms of the matrix given in [\[E: gen low order pair complete\]](#E: gen low order pair complete){reference-type="eqref" reference="E: gen low order pair complete"}.
:::

We remark that the joints C, E, and S can be constructed by the composition of R and P joints.

- A C joint is a composition of an R joint and a P joint: $$\begin{align}
          \begin{bmatrix}
          \cos(\theta_{i}) & -\sin(\theta_{i}) & 0 & 0 \\
          \sin(\theta_{i}) &  \cos(\theta_{i}) & 0 & 0 \\
          0  & 0  & 1 & z_{i} \\
          0 & 0 & 0 & 1
      \end{bmatrix}
      =
      \begin{bmatrix}
          \cos(\theta_{i}) & -\sin(\theta_{i}) & 0 & 0 \\
          \sin(\theta_{i}) &  \cos(\theta_{i}) & 0 & 0 \\
          0  & 0  & 1 & 0 \\
          0 & 0 & 0 & 1
      \end{bmatrix}
      \begin{bmatrix}
          1 & 0 & 0 & 0 \\
          0 &  1 & 0 & 0 \\
          0  & 0  & 1 & z_{i} \\
          0 & 0 & 0 & 1
      \end{bmatrix}
  \end{align}$$

- An E joint is the composition of one R joint and two P joints $$\begin{align}
          \begin{bmatrix}
          \cos(\theta_{i}) & -\sin(\theta_{i}) & 0 & x_{i} \\
          \sin(\theta_{i}) &  \cos(\theta_{i}) & 0 & y_{i} \\
          0  & 0  & 1 & 0 \\
          0 & 0 & 0 & 1
      \end{bmatrix}
      =
      \begin{bmatrix}
          1 & 0 & 0 & x_{i} \\
          0 &  1 & 0 & 0 \\
          0  & 0  & 1 & 0 \\
          0 & 0 & 0 & 1
      \end{bmatrix}
      \begin{bmatrix}
          1 & 0 & 0 & 0 \\
          0 &  1 & 0 & y_{i} \\
          0  & 0  & 1 & 0 \\
          0 & 0 & 0 & 1
      \end{bmatrix}
      \begin{bmatrix}
          \cos(\theta_{i}) & -\sin(\theta_{i}) & 0 & 0 \\
          \sin(\theta_{i}) &  \cos(\theta_{i}) & 0 & 0 \\
          0  & 0  & 1 & 0 \\
          0 & 0 & 0 & 1
      \end{bmatrix}
  \end{align}$$

- An S joint is the composition of three R joints expressed as Euler angles. $$\begin{align}
   \label{E: sphere joint}
      % \footnotesize{
      U(\psi_{i})
      =
      \begin{bmatrix}
          \cos(\psi_{i,x}) & -\sin(\psi_{i,x}) & 0 \\
          \sin(\psi_{i,x}) &  \cos(\psi_{i,x}) & 0 \\
          0 & 0 & 1
      \end{bmatrix}
      \begin{bmatrix}
          \cos(\psi_{i,y}) & 0 & -\sin(\psi_{i,y}) \\
           0 &  1 & 0 \\
          \sin(\psi_{i,y})  & 0  & \cos(\psi_{i,y}) \\
      \end{bmatrix}
      \begin{bmatrix}
          1 & 0 & 0  \\
          0 & \cos(\psi_{i,z}) & -\sin(\psi_{i,z}) \\
          0 & \sin(\psi_{i,z}) &  \cos(\psi_{i,z})   \\
      \end{bmatrix}
      % }
  \end{align}$$

  Our approach presented for a robot composed of R and P joints can be extended to handle any algebraic mechanism by consider the other algebraic joints as compositions of R and P joints.

# Definition of Archimedean {#A: Archimedean}

In this section we formally define the Archimedean property that appears in Theorem [1](#T: Putinar){reference-type="ref" reference="T: Putinar"} and Theorem [2](#T: Putinar Dual){reference-type="ref" reference="T: Putinar Dual"}.

::: {#D: Archimedean .definition}
**Definition 1**. *A semialgebraic set $\ensuremath{\mathcal{S}}_{g} = \{x \mid g_{i}(x) \geq 0, i \in [n]\}$ is Archimedean if there exists $N \in \ensuremath{\mathbb{N}}$ and $\lambda_{i}(x) \in \ensuremath{\bm{\Sigma}}$ such that: $$\begin{align*}
    N - \sum_{i=1}^{n}x_{i}^2 = \lambda_{0}(x) + \sum_{i=1}^{n} \lambda_{i}(x)g_i(x)
\end{align*}$$*
:::

# Semialgebraic Descriptions of Set Membership for Common Convex Bodies {#A: Semialgebraic Set Memebership}

::: {#Tab: shape conditions table poly}
+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                |                                                                                                                |                                                                                                                                                                                                          |
+:===============================================================================================================+:===============================================================================================================+:=========================================================================================================================================================================================================+
| ::: {#Tab: shape conditions table poly}                                                                        | ::: {#Tab: shape conditions table poly}                                                                        | ::: {#Tab: shape conditions table poly}                                                                                                                                                                  |
|   --                                                                                                           |   ----------------                                                                                             |   ----------------------------------------------------------------------------------------------------------------                                                                                       |
|   --                                                                                                           |   $\{s,x, \mu\}$                                                                                               |   $$\begin{gather*}                                                                                                                                                                                      |
|                                                                                                                |   ----------------                                                                                             |           h_{1}(s, x, \mu) = \left(\prod_{i}\leftidx{^F}g^{v_{i}}\right) \left(x-                                                                                                                        |
|   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |                                                                                                                |            \sum_{i=1}^{m} \mu_{i}\left(\frac{\leftidx^{F}f^{v_{i}}(s)}{\leftidx^{F}g^{v_{i}}(s)} \right)\right)                                                                                          |
| :::                                                                                                            |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |           \\                                                                                                                                                                                             |
|                                                                                                                | :::                                                                                                            |            h_{2}(\mu) = 1-\sum_{i=1} \mu_{i}                                                                                                                                                             |
|                                                                                                                |                                                                                                                |           \\                                                                                                                                                                                             |
|                                                                                                                |                                                                                                                |           \gamma_{i}(\mu_{i}) = \mu_{i}, ~ i \in [m]                                                                                                                                                     |
|                                                                                                                |                                                                                                                |   \end{gather*}$$                                                                                                                                                                                        |
|                                                                                                                |                                                                                                                |   ----------------------------------------------------------------------------------------------------------------                                                                                       |
|                                                                                                                |                                                                                                                |                                                                                                                                                                                                          |
|                                                                                                                |                                                                                                                |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$.                                                                                           |
|                                                                                                                |                                                                                                                | :::                                                                                                                                                                                                      |
+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: {#Tab: shape conditions table poly}                                                                        | ::: {#Tab: shape conditions table poly}                                                                        | ::: {#Tab: shape conditions table poly}                                                                                                                                                                  |
|   --                                                                                                           |   -----------                                                                                                  |   -----------------------------------------------------------------------------------------------------------------                                                                                      |
|   --                                                                                                           |   $\{s,x\}$                                                                                                    |   $$\begin{multline*}                                                                                                                                                                                    |
|                                                                                                                |   -----------                                                                                                  |       \gamma_{1}(s,x) =                                                                                                                                                                                  |
|   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |                                                                                                                |       \left(\leftidx^{F}g^{o}(s)\right)^{2}                                                                                                                                                              |
| :::                                                                                                            |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |       \left(r^{2}- \ensuremath{\left\| x - \frac{\leftidx^{F}f^{o}(s)}{\leftidx^{F}g^{o}(s)} \right\|}^{2}\right)                                                                                        |
|                                                                                                                | :::                                                                                                            |   \end{multline*}$$                                                                                                                                                                                      |
|                                                                                                                |                                                                                                                |   -----------------------------------------------------------------------------------------------------------------                                                                                      |
|                                                                                                                |                                                                                                                |                                                                                                                                                                                                          |
|                                                                                                                |                                                                                                                |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$.                                                                                           |
|                                                                                                                |                                                                                                                | :::                                                                                                                                                                                                      |
+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: {#Tab: shape conditions table poly}                                                                        | ::: {#Tab: shape conditions table poly}                                                                        | ::: {#Tab: shape conditions table poly}                                                                                                                                                                  |
|   --                                                                                                           |   ---------------                                                                                              |   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   |
|   --                                                                                                           |   $\{s,x,\mu\}$                                                                                                |   $$\begin{gather*}                                                                                                                                                                                      |
|                                                                                                                |   ---------------                                                                                              |           \frac{\leftidx^{F}f^{o_{\mu}}}{\leftidx^{F}g^{o_{\mu}}} = \mu \frac{\leftidx^{F}f^{o_{1}}(s)}{\leftidx^{F}g^{o_{1}}(s)} + (1-\mu)\frac{\leftidx^{F}f^{o_{2}}(s)}{\leftidx^{F}g^{o_{2}}(s)}     |
|   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |                                                                                                                |           \\                                                                                                                                                                                             |
| :::                                                                                                            |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |           r_{\mu} = \mu r_{1} + (1-\mu) r_{2}                                                                                                                                                            |
|                                                                                                                | :::                                                                                                            |           \\                                                                                                                                                                                             |
|                                                                                                                |                                                                                                                |       \gamma_{1}(s, x,\mu) =\left(\leftidx^{F}g^{o_{\mu}}(s)\right)^{2}                                                                                                                                  |
|                                                                                                                |                                                                                                                |       \left(                                                                                                                                                                                             |
|                                                                                                                |                                                                                                                |       r_{\mu}^{2}                                                                                                                                                                                        |
|                                                                                                                |                                                                                                                |       -  \ensuremath{\left\| x - \frac{\leftidx^{F}f^{o_{\mu}}}{\leftidx^{F}g^{o_{\mu}}} \right\|}^{2}                                                                                                   |
|                                                                                                                |                                                                                                                |       \right)                                                                                                                                                                                            |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |       \gamma_{2}(\mu) = \mu                                                                                                                                                                              |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |           \gamma_{3}(\mu) = 1-\mu                                                                                                                                                                        |
|                                                                                                                |                                                                                                                |   \end{gather*}$$                                                                                                                                                                                        |
|                                                                                                                |                                                                                                                |   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   |
|                                                                                                                |                                                                                                                |                                                                                                                                                                                                          |
|                                                                                                                |                                                                                                                |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$.                                                                                           |
|                                                                                                                |                                                                                                                | :::                                                                                                                                                                                                      |
+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: {#Tab: shape conditions table poly}                                                                        | $\{s,x,v, \mu\}$                                                                                               | ::: {#Tab: shape conditions table poly}                                                                                                                                                                  |
|   --                                                                                                           |                                                                                                                |   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|   --                                                                                                           |                                                                                                                |   $$\begin{gather*}                                                                                                                                                                                      |
|                                                                                                                |                                                                                                                |       \frac{\leftidx^{F}f^{o_{\mu}}(s)}{\leftidx^{F}g^{o_{\mu}}(s)} = \mu \frac{\leftidx^{F}f^{o_{1}}(s)}{\leftidx^{F}g^{o_{1}}(s)} + (1-\mu)\frac{\leftidx^{F}f^{o_{2}}(s)}{\leftidx^{F}g^{o_{2}}(s)}   |
|   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$. |                                                                                                                |           \\                                                                                                                                                                                             |
| :::                                                                                                            |                                                                                                                |       r_{\mu} = \mu r_{1} + (1-\mu) r_{2}                                                                                                                                                                |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |       h_{1}(v, s) = v^{T}\left(\frac{\leftidx^{F}f^{o_{1}}(s)}{\leftidx^{F}g^{o_{1}}(s)} -\frac{\leftidx^{F}f^{o_{2}}(s)}{\leftidx^{F}g^{o_{2}}(s)}\right)                                               |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |       h_{2}(s, x, \mu, v) = x - \frac{\leftidx^{F}f^{o_{\mu}}(s)}{\leftidx^{F}g^{o_{\mu}}(s)} - v                                                                                                        |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |       \gamma_{1}(v, \mu) = r_{\mu}^{2} - v^{T}v                                                                                                                                                          |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |       \gamma_{2}(\mu) = \mu                                                                                                                                                                              |
|                                                                                                                |                                                                                                                |       \\                                                                                                                                                                                                 |
|                                                                                                                |                                                                                                                |       \gamma_{3}(\mu) = 1-\mu                                                                                                                                                                            |
|                                                                                                                |                                                                                                                |   \end{gather*}$$                                                                                                                                                                                        |
|                                                                                                                |                                                                                                                |   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|                                                                                                                |                                                                                                                |                                                                                                                                                                                                          |
|                                                                                                                |                                                                                                                |   : Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$.                                                                                           |
|                                                                                                                |                                                                                                                | :::                                                                                                                                                                                                      |
+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

: Parameterizations of the condition that $x$ lies in a convex body that moves rigidly as a function of $s$.
:::

# Parametrized Hyperplane Separation Condition for the Cylinder {#A: cylinder matrix sos}

To derive the hyperplane separation condition for cylinder, we first attach a geometric frame $G$ to the cylinder, as shown in Fig.[40](#fig:cylinder){reference-type="ref" reference="fig:cylinder"}. The cylinder's geometric frame $G$'s origin coincides with the cylinder's center, with the $z$ axis of the $G$ frame along the cylinder axis. The height of the cylinder is $2h$, with the top/bottom circle radius being $r_1$ and $r_2$ respectively.

![Illustration of the cylinder on one side of the plane $\mathcal{H}$, with the plane normal being $\leftidx{^G}a$, expressed in the cylinders geometry frame $G$.](Dai2023Certified_figs/cylinder.png){#fig:cylinder width="50%"}

We first write the plane $\mathcal{H}$ with its parameters $\leftidx{^G}a(s), \leftidx{^G}b(s)$ in the cylinder's geometric frame $G$ and derive the conditions on $\leftidx{^G}a(s), \leftidx{^G}b(s)$. The cylinder is in the positive side of the plane if and only if both its top and bottom rim are on the positive side of the plane, namely $$\begin{align}
\left(\leftidx{^G}a(s)\right)^T \begin{bmatrix} r_1\cos\alpha\\
r_1\sin\alpha\\
h
\end{bmatrix} + \leftidx{^G}b(s) \ge 0\; \forall \alpha\\
\left(\leftidx{^G}a(s)\right)^T \begin{bmatrix} r_2\cos\alpha\\
r_2\sin\alpha\\
-h
\end{bmatrix} + \leftidx{^G}b(s) \ge 0\; \forall \alpha.
\end{align}$$ Taking the infimum of both sides with respect to $\alpha$ makes the above conditions equivalent to $$\begin{align}
\leftidx{^G}a_z(s) h + \leftidx{^G}b(s) \ge r_1 \ensuremath{\left\| \begin{bmatrix} \leftidx{^G}a_x(s) & \leftidx{^G}a_y(s)\end{bmatrix} \right\|}\label{eq:cylinder_separation1}\\
-\leftidx{^G}a_z(s) h + \leftidx{^G}b(s) \ge r_2 \ensuremath{\left\| \begin{bmatrix} \leftidx{^G}a_x(s) & \leftidx{^G}a_y(s)\end{bmatrix} \right\|}\label{eq:cylinder_separation2}
\end{align}
\label{eq:cylinder_separation}$$

Next, we use the Schur complement, to reformulate [\[eq:cylinder_separation1\]](#eq:cylinder_separation1){reference-type="eqref" reference="eq:cylinder_separation1"} and [\[eq:cylinder_separation2\]](#eq:cylinder_separation2){reference-type="eqref" reference="eq:cylinder_separation2"} the positive semidefinite matrix conditions. For example, [\[eq:cylinder_separation1\]](#eq:cylinder_separation1){reference-type="eqref" reference="eq:cylinder_separation1"} is equivalent to $$\begin{gather}
\begin{bmatrix}
\leftidx{^G}a_z(s)h+\leftidx{^G}b(s) & 0 & r_1\ \leftidx{^G}a_x(s) \\
0 & \leftidx{^G}{a}_z(s)h + \leftidx{^G}b(s) & r_1\ \leftidx{^G}a_y(s)\\
r_1\ \leftidx{^G}a_x(s) & r_1\ \leftidx{^G}a_y(s) &\leftidx{^G}{a}_z(s)h + \leftidx{^G}b(s)
\end{bmatrix}\succeq 0
\end{gather}

As explained in Section \ref{S: Hyperplane Cert}, this polynomial PSD condition can be reformulated as the condition
\begin{gather}
u^T\begin{bmatrix}
\leftidx{^G}a_z(s)h+\leftidx{^G}b(s) & 0 & r_1\ \leftidx{^G}a_x(s) \\
0 & \leftidx{^G}{a}_z(s)h + \leftidx{^G}b(s) & r_1\ \leftidx{^G}a_y(s)\\
r_1\ \leftidx{^G}a_x(s) & r_1\ \leftidx{^G}a_y(s) &\leftidx{^G}{a}_z(s)h + \leftidx{^G}b(s)
\end{bmatrix}u\geq 0 \;\forall u. \label{E: cylinder_matrix_sos}
\end{gather}$$

To avoid the trivial solution $\leftidx{^G}a(s) = 0, \leftidx{^G}b(s) = 0$ (which is not in fact a separating plane), we add the extra constraint $\leftidx{^G}a^T \left(\frac{\leftidx{^G}p^{o_1} + \leftidx{^G}p^{o_2}}{2}\right) + \leftidx{^G}b \geq 1$. Here $\frac{\leftidx{^G}p^{o_1} + \leftidx{^G}p^{o_2}}{2}$ is the position of the cylinder center expressed in the geometric frame $G$ which coincides with the frame's origin. Therefore $\frac{\leftidx{^G}p^{o_1} + \leftidx{^G}p^{o_2}}{2} = 0$, and so it is sufficient to introduce the constraint $$\begin{align}
\leftidx{^G}b(s) \ge 1 \label{E: cylinder_b>1}
\end{align}$$ to exclude the trivial solution $\leftidx{^G}a=0, \leftidx{^G}b=0$.

In our optimization program, we express the separating plane in a frame $F$ (where the choice of frame $F$ is discussed in [14.1](#A: Frame Selection){reference-type="ref" reference="A: Frame Selection"}), not in cylinder's geometric frame $G$. Hence we need to compute $\leftidx{^G}a(s), \leftidx{^G}b(s)$ from their corresponding terms $\leftidx{^F}a(s), \leftidx{^F}b(s)$ expressed in frame $F$ and the relative transform $\leftidx{^F}X^G$ between the two frames $$\begin{gather}
\leftidx{^G}a(s) = \leftidx{^G}R^F(s) \;\leftidx{^F}a(s)\\
\leftidx{^G}b(s) = \leftidx{^F}b(s) + \left(\leftidx{^F}a(s)\right)^T \;\leftidx{^F}p^G(s)
\end{gather}
\label{E: plane frame transform}$$

As described in Section [3.3](#S: Rat Forward){reference-type="ref" reference="S: Rat Forward"}, both the position $\leftidx{^F}p^G(s)$ and orientation $\leftidx{^G}R^F(s)$ are rational functions of $s$. By replacing $\leftidx{^G}a(s), \leftidx^{G}b(s)$ in [\[E: cylinder_matrix_sos\]](#E: cylinder_matrix_sos){reference-type="eqref" reference="E: cylinder_matrix_sos"} and [\[E: cylinder_b\>1\]](#E: cylinder_b>1){reference-type="eqref" reference="E: cylinder_b>1"} with [\[E: plane frame transform\]](#E: plane frame transform){reference-type="eqref" reference="E: plane frame transform"} and requiring the resulting numerator of the rational function to be non-negative, we derive that the plane separating cylinders can be enforced via a polynomial non-negativity condition which can be formulated as sums-of-squares condition.

# The Certification Programs are Necessary and Sufficient {#A: necessary and sufficient}

In this section, we expand our discussion on the power of the certification programs presented in Sections [4.1](#S: Hyperplane Cert){reference-type="ref" reference="S: Hyperplane Cert"} and [4.2](#S: infeasible non-collision cert){reference-type="ref" reference="S: infeasible non-collision cert"}. As remarked previously, Theorems [4](#T: dual psatz poly cert is always feasible){reference-type="ref" reference="T: dual psatz poly cert is always feasible"} and [3](#T: hyperplane poly cert is always feasible){reference-type="ref" reference="T: hyperplane poly cert is always feasible"} are necessary as programs [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} and [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} are infinite dimensional. It is not immediately obvious that for every robot and every scene, there exists a finite degree where in each program must become feasible when $\ensuremath{\mathcal{P}}$ truly contains no collisions.

A second subtlety applies specifically to [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"}. When generalizing [\[E: sep hyperplane generic\]](#E: sep hyperplane generic){reference-type="eqref" reference="E: sep hyperplane generic"}, we argued that it was beneficial to search for a parametric hyperplane as a function of our TC-space variable $s$ and asserted that a polynomial parameterization was a good choice. However, it is not obvious that a polynomial parameterization is sufficient, and perhaps we require a rational or even more complicated parameterization of the plane.

These questions about the power of SOS programming arise in other domains. For example, SOS is commonly used to search for polynomial Lyapunov functions to prove the stability of polynomial dynamical systems [@majumdar2017funnel]. However, it is known that not every stable polynomial dynamical system admits a polynomial Lyapunov function [@ahmadi2011globally], and therefore SOS programming is a sufficient, but not necessary tool for proving the stability of dynamical systems.

Fortunately, our certification programs from [4.1](#S: Hyperplane Cert){reference-type="ref" reference="S: Hyperplane Cert"} and [4.2](#S: infeasible non-collision cert){reference-type="ref" reference="S: infeasible non-collision cert"} are indeed *necessary and sufficient*, in the sense that there will always exist a finite degree such that the programs become feasible if $\ensuremath{\mathcal{P}}$ contains no collision. The proof of this for the program [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} follows immediately from Theorem [2](#T: Putinar Dual){reference-type="ref" reference="T: Putinar Dual"}.

::: proof
*Proof.* **(of Theorem [4](#T: dual psatz poly cert is always feasible){reference-type="ref" reference="T: dual psatz poly cert is always feasible"})** Our assumptions on $\ensuremath{\mathcal{P}}, ~\ensuremath{\mathcal{A}}$, and $\ensuremath{\mathcal{B}}$ imply that $\ensuremath{\mathcal{S}}_{\ensuremath{\mathcal{P}}, \ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}$ is an Archimedean set. Therefore, the feasibility of [\[E: dual psatz poly cert\]](#E: dual psatz poly cert){reference-type="eqref" reference="E: dual psatz poly cert"} for sufficiently high degree $\rho$ follows immediately from "effective\" versions of Theorem [2](#T: Putinar Dual){reference-type="ref" reference="T: Putinar Dual"} such as those given in [@nie_complexity_2007; @baldi2021moment] which give explicit degree bounds. 0◻ ◻
:::

Though the proof of Theorem [3](#T: hyperplane poly cert is always feasible){reference-type="ref" reference="T: hyperplane poly cert is always feasible"} is more technically involved, the key idea is simple. In short, we construct a family of continuous functions which map each TC-space configuration $s \in \ensuremath{\mathcal{P}}$ to a separating plane. We then argue that this family of continuous functions must contain hyperplanes which are parametrized as polynomials. Finally, we again appeal to "effective\" versions of Theorem [1](#T: Putinar){reference-type="ref" reference="T: Putinar"} such as those given in [@nie_complexity_2007; @baldi2021moment] to show that these polynomials can be found using SOS programming.

We proceed in steps, first establishing that the set of separating planes at a point $s$ in TC-free is open.

::: {#P: sep set non empty and open .proposition}
**Proposition 1**. *Let $\Phi(s)$ denote the set of strictly separating hyperplanes at the point $s$ for bodies $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ and let $\ensuremath{\mathcal{P}}$ be a non-empty, polytopic subset of TC-free. Then $s \in \ensuremath{\mathcal{P}}$ implies that $\Phi(s)$ is a non-empty, open set. 0◻*
:::

::: proof
*Proof.* By definition, a hyperplane $\begin{bmatrix} a \\ b \end{bmatrix} \in \ensuremath{\mathbb{R}}^{4}$ strictly separates $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ if and only if there exist positive constants $\varepsilon_{\ensuremath{\mathcal{A}}}$ and $\varepsilon_{\ensuremath{\mathcal{B}}}$ such that $a^{T}x + b \geq \varepsilon_{\ensuremath{\mathcal{A}}}~ \forall x \in \ensuremath{\mathcal{A}}(s)$and $a^{T}x + b \leq -\varepsilon_{\ensuremath{\mathcal{B}}}~ \forall x \in \ensuremath{\mathcal{B}}(s)$. Since the bodies $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ are strictly separating for every point $s \in \ensuremath{\mathcal{P}}$, the Separating Hyperplane theorem guarantees the existence of such a vector and so $\Phi(s)$ is non-empty.

Now consider $\begin{bmatrix} a \\ b \end{bmatrix} \in \Phi(s) \subseteq \ensuremath{\mathbb{R}}^{4}$ and its $\delta$ neighborhood $$\begin{align*}
        \ensuremath{\mathcal{N}}(\delta) = 
        \left\{\begin{bmatrix} a \\ b \end{bmatrix} + \delta\begin{bmatrix} v_{a} \\ v_{b} \end{bmatrix} 
        \middle| \ensuremath{\left\| \begin{bmatrix} v_{a} \\ v_{b} \end{bmatrix}  \right\|} \leq 1\right\},
\end{align*}$$ with $\delta > 0$.

We have that for all $x \in \ensuremath{\mathcal{A}}$ $$\begin{align*}
    (a^{T} + \delta v^{T}_{a})x + (b + \delta v_{b}) 
    \geq
    \varepsilon_{\ensuremath{\mathcal{A}}} + \delta \min_{\ensuremath{\left\| v \right\|} \leq 1,~ x \in \ensuremath{\mathcal{A}}}  v^{T}_{a}x + v_{b}
\end{align*}$$ and similarly for all $x \in \ensuremath{\mathcal{B}}$ $$\begin{align*}
(a^{T} + \delta v^{T}_{a})x + (b + \delta v_{b}) 
    \leq
    -\varepsilon_{\ensuremath{\mathcal{B}}} + \delta \max_{\ensuremath{\left\| v \right\|} \leq 1,~ x \in \ensuremath{\mathcal{B}}}  v^{T}_{a}x + v_{b}.
\end{align*}$$

Letting $M_{l} = \displaystyle{\min_{\ensuremath{\left\| v \right\|} = 1,~ x \in \ensuremath{\mathcal{A}}}}  v^{T}_{a}x + v_{b}$ and $M_{u} = \displaystyle{\max_{\ensuremath{\left\| v \right\|} = 1,~ x \in \ensuremath{\mathcal{B}}}}  v^{T}_{a}x + v_{b}$, we have that all planes $\ensuremath{\mathcal{N}}(\delta)$ are separating if $$\begin{align*}
    0 < \delta < 
    \min \left\{
    \frac{\varepsilon_{\ensuremath{\mathcal{A}}}}{\ensuremath{{\left\vert M_{l} \right\vert}}},~
    \frac{\varepsilon_{\ensuremath{\mathcal{B}}}}{\ensuremath{{\left\vert M_{u} \right\vert}}}
    \right\}
\end{align*}$$ and so $\Phi(s)$ is open. 0◻ ◻
:::

::: {#P: minimal neighborhood exists .proposition}
**Proposition 2**. *Define $$\begin{align*}
        \ensuremath{\mathcal{N}}(s, \delta) =
        \bigcap_{\ensuremath{\left\| v \right\|} \leq 1} \Phi(s + \delta v)
\end{align*}$$*

*For all $s \in \ensuremath{\mathcal{P}}$ there exists $\delta_{\min}(s) > 0$, not necessarily finite such that, $\ensuremath{\mathcal{N}}(s, \delta)$ is non-empty and open for every $0 < \delta < \delta_{\min}$.*
:::

::: proof
*Proof.* Recall that the position of every point in $\ensuremath{\mathcal{A}}(s)$ is a continuous function of $s$ and that the distance from a point to a set is a continuous function [@rudin1976principles]. Therefore, the distance of every point in $\ensuremath{\mathcal{A}}(s)$ to every element of $\Phi(s)$ changes continuously. For every $\delta > 0$ and $\begin{bmatrix} a \\ b \end{bmatrix} \in \Phi(s)$ we define: $$\begin{align*}
M_{\delta}(s)
\coloneqq
\sup_{\ensuremath{\left\| v \right\|} \leq 1}
\ensuremath{{\left\vert 
\inf_{x \in \ensuremath{\mathcal{A}}(s)}
a^{T}x + b 
-
 \inf_{x \in \ensuremath{\mathcal{A}}(s + \delta v)}
a^{T}x + b 
 \right\vert}}
\end{align*}$$

We have that $$\begin{align*}
   \inf_{\ensuremath{\left\| v \right\|} \leq 1} \inf_{\substack{x \in \ensuremath{\mathcal{A}}(s + \delta v)}}
    a^{T}x + b 
    \geq
    \inf_{x \in \ensuremath{\mathcal{A}}(s)}
    a^{T}x + b 
    - M_{\delta}(s)
    \geq 
    \varepsilon_{\ensuremath{\mathcal{A}}} - M_{\delta}(s)
\end{align*}$$

Moreover, if $\delta_{2} < \delta_{1}$, then $M_{\delta_{2}}(s) \leq M_{\delta_{1}}(s)$. By continuity and monotonicity, $M_{\delta}(s) \rightarrow 0$ as $\delta \rightarrow 0$ and so there exists $\delta$ sufficiently small such that $\varepsilon_{\ensuremath{\mathcal{A}}} - M_{\delta}(s) > 0$. A similar argument shows that $\delta$ can be chosen sufficiently small such that the plane $\begin{bmatrix} a \\ b \end{bmatrix}$ continues to satisfy the separating plane conditions for $\ensuremath{\mathcal{B}}$. Therefore $\begin{bmatrix} a \\ b \end{bmatrix}  \in \Phi(s + \delta v)$ for all $v$ such that $\ensuremath{\left\| v \right\|} \leq 1$ if $\delta$ is chosen sufficiently small. It is clear that choosing $\delta$ smaller continues to ensure that $\ensuremath{\mathcal{N}}(s, \delta)$ is non-empty. Openness is immediate following a similar argument to Proposition [1](#P: sep set non empty and open){reference-type="ref" reference="P: sep set non empty and open"}. 0◻ ◻
:::

The above proposition enables us to establish that there exists an open family of continuous functions $f(s)$ such that their outputs are always separating hyperplanes.

::: {#P: calF non-empty .proposition}
**Proposition 3**. *Let $\ensuremath{\mathcal{F}}$ be the set of continuous functions mapping $$f: s \mapsto \begin{bmatrix} a \\ b \end{bmatrix}$$ such that $f(s) \in \Phi(s)$ for all $s \in \ensuremath{\mathcal{P}}$. The set $\ensuremath{\mathcal{F}}$ is non-empty and open under the pointwise metric $$d(f,g) = \sup_{s \in \ensuremath{\mathcal{P}}} \ensuremath{\left\| f(s) - g(s) \right\|}.$$*
:::

::: proof
*Proof.* Suppose $\ensuremath{\mathcal{F}}$ were empty. Then every function satisfying $f(s) \in \Phi(s) ~\forall s \in \ensuremath{\mathcal{P}}$ is not a continuous function. Namely, for every $f$ there exists a point $s_{0}$ such that for all $\delta > 0$, $f(s_{0}) \in \Phi(s_{0})$ but $f(s_{0}) \notin \ensuremath{\mathcal{N}}(s_{0}, \delta)$. This contradicts the openness of $\ensuremath{\mathcal{N}}(s_{0}, \delta)$ for a sufficiently small $\delta$ from Proposition [2](#P: minimal neighborhood exists){reference-type="ref" reference="P: minimal neighborhood exists"} and so $\ensuremath{\mathcal{F}}$ is non-empty. Openness follows from the fact that if $\delta > 0$ is chosen sufficiently small, then for every continuous $g$ satisfying $d(f,g) < \delta$, then $g$ must also separate $\ensuremath{\mathcal{A}}(s)$ and $\ensuremath{\mathcal{B}}(s)$ for every $s \in \ensuremath{\mathcal{P}}$.

0◻ ◻
:::

We are now ready to prove Theorem [3](#T: hyperplane poly cert is always feasible){reference-type="ref" reference="T: hyperplane poly cert is always feasible"}

::: proof
*Proof.* **(of Theorem [3](#T: hyperplane poly cert is always feasible){reference-type="ref" reference="T: hyperplane poly cert is always feasible"})** By Proposition [3](#P: calF non-empty){reference-type="ref" reference="P: calF non-empty"}, $\ensuremath{\mathcal{F}}$ is a non-empty open subset of continuous functions defined on the compact domain $\ensuremath{\mathcal{P}}$. The Stone-Weierstrass theorem [@rudin1976principles] states that the set of polynomial functions on a compact domain is dense in the set of continuous functions in that domain under the pointwise metric. Therefore, $\ensuremath{\mathcal{F}}$ must contain a map $p: s \mapsto \begin{bmatrix} a(s) \\ b(s) \end{bmatrix}$ such that each component is a polynomial. This polynomial is of finite degree and is a strictly separating hyperplane and therefore by "effective\" versions of Theorem [1](#T: Putinar){reference-type="ref" reference="T: Putinar"} such as [@nie_complexity_2007; @baldi2021moment], there exists a Putinar certificates of finite degree certifying that $p(s)$ is a separating hyperplane. 0◻ ◻
:::

# Practical aspects {#A: Practical Aspects}

In this section, we discuss some practical aspects for essential for enabling Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} to realistic examples. These include the choice of reference frame in which to express the forward kinematics, the selection of a finite basis for the polynomials in our SOS programs, and which aspects of [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} can be parallelized.

## Choosing the Reference Frame {#A: Frame Selection}

The polynomial implications upon which the certification program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and polytope growth program [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} are based require choosing a coordinate frame between each collision pair $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. However, as the collision-free certificate between two different collision pairs can be computed independently of each other, we are free to choose a different coordinate frame to express the kinematics for each collision pair. This is important in light of [\[E: gen forward kin\]](#E: gen forward kin){reference-type="eqref" reference="E: gen forward kin"} and [\[E: rational forward kinematics gen\]](#E: rational forward kinematics gen){reference-type="eqref" reference="E: rational forward kinematics gen"} that indicate that the degree of the polynomials $\leftidx{^F}f^{\ensuremath{\mathcal{A}}_{j}}$ and $\leftidx{^F}g^{\ensuremath{\mathcal{A}}_{j}}$ are equal to two times the number of joints lying on the kinematic chain between frame $F$ and the frame for $\ensuremath{\mathcal{A}}$. For example, the tangent-configuration-space polynomial in the variable $s$ describing the position of the end-effector of a 7-DOF robot is of total degree $14$ when written in the coordinate frame of the robot base. However, when written in the frame of the third link, the polynomial describing the position of the end effector is only of total degree $(7-3)\times 2=8$. This observation is also used in [@trutman2020globally] to reduce the size of the optimization program.

The size of the semidefinite variables in [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} scale as the square of the degree of the polynomial used to express the forward kinematics. Supposing there are $n$ links in the kinematics chain between $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$, then choosing the $j$th link along the kinematics chain as the reference frame $F$ leads to scaling of order $j^{2} + (n-j)^{2}$. Choosing the reference frame in the middle of the chain minimizes this complexity to scaling of order $\frac{n^2}{2}$ and we therefore adopt this convention in our experiments.

## Basis Selection {#A: Basis Selection}

The condition that a polynomial can be written as a sum of squares can be equivalently formulated as an equality constraint between the coefficients of the polynomial and an associated semidefinite variable known as the Gram matrix [@parrilo2004sum]. Namely, a polynomial $p(s)$ is sums-of-squares if and only if $p(s) = z(s)^T X z(s), X\succeq 0$ where $z(s)$ is a vector of monomials and $X$ is the Gram matrix. The number of rows in the positive semidefinite Gram matrix equals to the size of the vector $z(s)$. In general, a sums-of-squares polynomial in $k$ variables of total degree $2d$ requires a Gram matrix of size ${k +d} \choose {d}$ to represent which can quickly become prohibitively large. Fortunately, the polynomials in our programs contain substantially more structure which will allow us to select a small-sized vector of monomials $z(s)$, and hence drastically reduce the size of the Gram matrices and speed up the optimization problem.

### Polytopic collision geometry

We begin with the separating plane condition for polytopic collision geometries. Note that from [\[E: rational forward kinematics gen\]](#E: rational forward kinematics gen){reference-type="eqref" reference="E: rational forward kinematics gen"} that while both the numerator and denominator of the forward kinematics are of total degree $2n$, with $n$ the number of links of the kinematics chain between frame $A$ and $F$, both polynomials are of *coordinate* degree of at most two (i.e. the highest degree of $s_{i}$ in any term is $s_{i}^2$). We will refer to this basis as $\nu(s)$ which is a vector containing terms of the form $\prod_{i = 1}^{n} s_{i}^{\text{degree}(s_i)}$ with $\text{degree}(s_i) \in \{0,1,2\}$ for all $3^n$ possible permutations of the exponents $\text{degree}(s_i)$.

We recall that we parametrize our hyperplane using polynomial entries. If $a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)= a^T_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}\eta(s)$, $b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s) = b^T_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}\eta(s)$ for some basis $\eta$ in the variable $s$. The position of $x(s) \in \ensuremath{\mathcal{A}}(s)$ is expressed in basis $\nu(s)$, then the left hand side of [\[E: polytope separation psatz condition\]](#E: polytope separation psatz condition){reference-type="eqref" reference="E: polytope separation psatz condition"} can be expressed as a linear function of the basis $\gamma(s)$, where $\gamma(s)$ contains all the possible entries that appear in the outer product $\eta(s) \nu(s)^{T}$.

::: example
**Example 3**. *Suppose $$\eta(s) = \begin{bmatrix} 1 & s_{1} & s_{2} \end{bmatrix}^{T}$$ and $$\nu(s) =\begin{bmatrix} 1 & s_{1} & s_{1}^{2} & s_{2} & s_{2}^{2} & s_{1}s_{2} & s_{1}^{2}s_{2} &  s_{1}s_{2}^{2} &  s_{1}^{2}s_{2}^{2}\end{bmatrix}^{T}$$.*

*Then: $$\begin{multline*}
    \gamma(s) =
    \Big[
        1 \quad 
        s_{1} \quad s_{1}^{2} \quad s_{1}^{3} \quad
        s_{2} \quad s_{2}^{2} \quad s_{2}^{3} \quad
        s_{1}s_{2} \quad s_{1}^{2}s_{2} \quad s_{1}^{3}s_{2} \quad
        s_{1}s_{2}^{2} \quad s_{1}^{2}s_{2}^{2} \quad s_{1}^{3}s_{2}^{2} \quad
        s_{1}s_{2}^{3} \quad s_{1}^{2}s_{2}^{3}
        % 1 & 
        % s_{1} & s_{1}^{2} & s_{1}^{3} &
        % s_{2} & s_{2}^{2} & s_{2}^{3} \\
        % s_{1}s_{2} & s_{1}^{2}s_{2} & s_{1}^{3}s_{2} &
        % s_{1}s_{2}^{2} & s_{1}^{2}s_{2}^{2} & s_{1}^{3}s_{2}^{2} &
        % s_{1}s_{2}^{3} & s_{1}^{2}s_{2}^{3} & s_{1}^{3}s_{2}^{3}
    \Big]
    % \end{bmatrix}
\end{multline*}$$ Namely $\gamma(s)$ contains the monomials whose degree for each $s_i$ is at most 3, and only one of $s_i$ can have degree 3 (hence $s_1^3s_2^3$ is not included in $\gamma(s)$).*
:::

Similarly, we must select a basis $\rho(s)$ for our multiplier polynomials $\lambda_{ij}^{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)$. The equality in [\[E: polytope separation psatz condition\]](#E: polytope separation psatz condition){reference-type="eqref" reference="E: polytope separation psatz condition"} determines the minimum necessary basis $\rho(s)$. If the polynomial $p(s)$ is expressed in basis $\gamma(s)$, then the minimal such basis is related to an object known in computational algebra as the Newton polytope of $\gamma$ denoted $\textbf{New}(\gamma(s))$ [@sturmfels1994newton]. Denoting the linear basis $$\begin{align*}
    l(s) = \begin{bmatrix} 1 & s_{1} & s_{2} & \dots & s_{N} \end{bmatrix},
\end{align*}$$ then exact condition is that $$\textbf{New}(\gamma(s)) = \textbf{New}(\eta(s)) + \textbf{New}(\nu(s)) \subseteq \textbf{New}(\rho(s)) + \textbf{New}(l(s))$$ where the sum in this case is the Minkowski sum.

By using affine polynomials for separating plane parameters $a_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s), b_{\ensuremath{\mathcal{A}}, \ensuremath{\mathcal{B}}}(s)$, we know that $\eta(s)$ is the same as the linear basis $l(s)$, then we obtain the condition that $\textbf{New}(\rho(s)) = \textbf{New}(\nu(s))$ and since $\nu(s)$ is a dense, even degree basis we must take $\rho(s) = \nu(s)$. A sums-of-squares polynomial in the basis of $\nu(s)$ has Gram matrix with $2^{n}$ rows. Choosing $\eta(s)$ as the constant basis would in fact result in the same condition, and therefore searching for separating planes which are linear functions of the tangent-configuration-space variable does not increase the size of the semidefinite variables. As the complexity of [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} are dominated by the size of these semidefinite variables, separating planes which are linear functions changes do not substantially affect the solve time but can dramatically increase the size of the regions which we can certify.

Because of this, we choose to parametrize all of our hyperplanes throughout our experiments as linear functions of the TC-space variables. We stress that in general, the choice of a linearly parametrized hyperplane, and the selection of $\rho(s)$ to be the minimum size to match the degree of the left hand side of [\[E: polytope separation psatz condition\]](#E: polytope separation psatz condition){reference-type="eqref" reference="E: polytope separation psatz condition"} may not be sufficient to prove that a region $\ensuremath{\mathcal{P}}$ is collision-free, even if $\ensuremath{\mathcal{P}}$ truly is collision-free. Indeed due of many complexity-theoretic results, we expect that in general $\eta(s)$ and $\rho(s)$ may need to have exponentially high degree for some robots, scenes, and polytopes $\ensuremath{\mathcal{P}}$ [@stengle1996complexity]. However, in practice we have observed that the choices in this section are sufficient to certify many regions of interest, while keeping the optimization problem size tractable for state-of-art numerical solvers.

::: remark
**Remark 5**. *Attempting to certifying that the end-effector of a 7-DOF robot will not collide with the base using program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} using linearly parametrized hyperplanes and choosing to express conditions [\[E: polytope separation psatz condition\]](#E: polytope separation psatz condition){reference-type="eqref" reference="E: polytope separation psatz condition"} in the world frame with naïvely chosen bases would result in semidefinite variables of size ${7+7 \choose 7} = 3432$. Choosing to express the same conditions according to the discussion in Section [14.1](#A: Frame Selection){reference-type="ref" reference="A: Frame Selection"} and choosing the basis $\gamma(s)$ described in this section results in semidefinite matrices of rows at most $2^{\lceil7/2\rceil} = 2^{4} = 16$. The division by 2 comes from choosing the middle link as the expressed frame, hence halving the kinematic chain length.*
:::

### Non-polytopic collision geometry

In this section, we use the sphere as a running example for explaining how we choose the monomial bases for certifying separation of the non-polytopic geometries; the monomial bases for capsules and cylinders can be derived in a similar manner.

As mentioned in [\[E: shur complement implication\]](#E: shur complement implication){reference-type="eqref" reference="E: shur complement implication"}, we need to impose $$\begin{align}
\label{E: sphere_matrix_sos}
s \in \ensuremath{\mathcal{P}}\implies
    \begin{bmatrix}
        \left((a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)\right)I_{3} & ra(s) \ \leftidx{^F}g^{o}(s) \\ r(a(s))^T \ \leftidx{^F}g^{o}(s) & (a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)
    \end{bmatrix}
    \succeq 0.
\end{align}$$ By the definition of positive semidefinite matrix [^9] , we know that the $4\times 4$ matrix in the right of $\implies$ in [\[E: sphere_matrix_sos\]](#E: sphere_matrix_sos){reference-type="eqref" reference="E: sphere_matrix_sos"} is positive semidefinite if and only if $$\begin{align}
\forall \bar{u}\in\mathbb{R}^3,\underbrace{ \begin{bmatrix}\bar{u}\\1\end{bmatrix}^T \begin{bmatrix}
        \left((a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)\right)I_{3} & ra(s) \ \leftidx{^F}g^{o}(s) \\ r(a(s))^T \ \leftidx{^F}g^{o}(s) & (a(s))^T \ \leftidx{^F}f^{o}(s)+b(s) \ \leftidx{^F}g^{o}(s)
    \end{bmatrix}\begin{bmatrix}\bar{u}\\1\end{bmatrix}}_{\sigma(\bar{u}, s)} \geq 0. \label{E: sphere_matrix_sos_sigma}
\end{align}$$

We impose the following sufficient condition for [\[E: sphere_matrix_sos\]](#E: sphere_matrix_sos){reference-type="eqref" reference="E: sphere_matrix_sos"}, where $\ensuremath{\mathcal{P}}= \{ s | c_j^T(s)\le d_j, j=1,\hdots,m\}$ $$\begin{align}
\sigma(\bar{u}, s) = \lambda_0(\bar{u}, s) + \sum_{j=1}^{m}\lambda_j(\bar{u}, s) (d_j - c_j^Ts)\\
\text{for } j=0, \hdots, m, \lambda_j(\bar{u}, s) \ge 0 \;\forall \bar{u}, s.
\end{align}
\label{E: sphere_psatz}$$

Now we analyze the degree of the polynomial $\sigma(\bar{u}, s)$ defined in [\[E: sphere_matrix_sos_sigma\]](#E: sphere_matrix_sos_sigma){reference-type="eqref" reference="E: sphere_matrix_sos_sigma"}. As mentioned in the previous subsection, each monomial in $\leftidx^{F}f^o(s), \leftidx{^F}g^o(s)$ are of the form $\prod_{i=1}^n s_i^{\text{degree}(s_i)}, \text{degree}(s_i)\in\{0, 1, 2\}$. Combining this with the choice of a separating plane $a(s), b(s)$ being affine functions of $s$, we derive that each monomial in $\sigma(\bar{u}, s)$ is of the form $\bar{u}_j^{\text{degree}(\bar{u}_j)} \prod_{i=1}^n s_i^{\text{degree}(s_i)}, \text{ where 
 } \text{degree}(\bar{u}_j)\in\{0, 1, 2\}$, $\text{degree}(s_i)\in\{0, 1, 2, 3\}$, and at most one of $\text{degree}(s_i)$ can be 3. As an example, $\bar{u}_1^2 s_1^3s_2s_3^2$ is a valid monomial in $\sigma(\bar{u}, s)$ but $\bar{u}_1\bar{u}_2$ is not (because $\sigma(\bar{u}, s)$ doesn't contain the cross product between $\bar{u}_j, \bar{u}_k, j\neq k$). Similarly, $s_1^3s_2^3$ is not in the basis because at most one of $s_i$ can have degree 3. Given these properties on the monomials in $\sigma(\bar{u}, s)$- specifically there being no cross-product term $\bar{u}_j\bar{u}_k, j\neq k$ in $\sigma(\bar{u}, s)$- we can write the positive polynomials $\lambda_j(\bar{u}, s)$ as the summation of three SOS polynomials $$\begin{align}
 \lambda_j(\bar{u}, s) = \sum_{k=1}^3\lambda_{j, k}(\bar{u}_k, s)\\ \lambda_{j, k}(\bar{u}_k, s)\in\ensuremath{\bm{\Sigma}}.
 \end{align}$$ For each monomial in the SOS polynomial $\lambda_{j, k}(\bar{u}_k, s)$, the degree of $\bar{u}_k \text{ and } s_i$ for $i=1,\hdots, n$ is either 0, 1, or 2. Hence the number of rows in the Gram matrix in $\lambda_{j, k}(\bar{u}_k, s)$ is of size $2^{n+1}$. By choosing the reference frame according to the convention from Appendix [14.1](#A: Frame Selection){reference-type="ref" reference="A: Frame Selection"}, $n$ is no larger than $\left \lceil N/2 \right \rceil$ where $N$ is the number of joints in the robot.

::: remark
**Remark 6**. *For a 6-DOF UR3erobot whose collision geometries are approximated by cylinders, to certify the collision-avoidance between the robot and objects in the world (or self-collision), the largest positive semidefinite matrix in our optimization problem has rows at most $2^{\lceil 6 / 2\rceil + 1} = 2^4 = 16$, where the division by 2 comes from choosing the middle link as the expressed link, hence halving the kinematic chain length to $\lceil6 / 2 \rceil$.*
:::

## Parallelization {#A: Parallelization}

While it is attractive from a theoretical standpoint to write [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} as a single, large program it is worth noting that it can in fact be viewed as $K$ individual SOS programs, where $K$ is the number of collision pairs in the environment. Indeed, certifying whether pairs $(\ensuremath{\mathcal{A}}_{1}, \ensuremath{\mathcal{A}}_{2})$ are collision-free for all $s$ in the polytope $\ensuremath{\mathcal{P}}$ can be done completely independently of the certification of another pair $(\ensuremath{\mathcal{A}}_{1},  \ensuremath{\mathcal{A}}_{3})$ as the constraint are not coupled between any pairs. Similarly, the search for the largest inscribed ellipsoid can be done independently of the search for the separating hyperplanes.

Solving the certification program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} as $K$ individual SOS programs has several advantages. First, as written [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} has $2(m+1)K\sum_{i} \ensuremath{{\left\vert \ensuremath{\mathcal{A}}_{i} \right\vert}}$ semidefinite variables of various sizes, where $m$ is the number of inequalities in $\ensuremath{\mathcal{P}}$ and $\ensuremath{{\left\vert \ensuremath{\mathcal{A}}_{i} \right\vert}}$ denotes the number of inequalities required to express that body $\ensuremath{\mathcal{A}}_{i}$ is on a particular side of the plane (see Table [31](#Tab: shape conditions table poly){reference-type="ref" reference="Tab: shape conditions table poly"}). In the example from Section [6.1.2](#S: Pinball){reference-type="ref" reference="S: Pinball"} this corresponds to $18,720$ semidefinite variables. This can be prohibitively large to store in memory as a single program as the size of these semidefinite variables grow. Solving for the separating plane for each pair of collision bodies independently also enables us to determine which collision bodies cannot be certified as collision-free and allows us to terminate our search as soon as a single pair cannot be certified. Finally, decomposing the problems into subproblems enables us to increase computation speed by leveraging parallel processing.

The program [\[E: max inscribed ellipse in polytope\]](#E: max inscribed ellipse in polytope){reference-type="eqref" reference="E: max inscribed ellipse in polytope"} can also be solved completely independently of the certification program [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} and is in general a much smaller SDP than any individual certification program. Therefore, lines $3$ and $4$ of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} can be solved in parallel.

We note that [\[E: polytope growth program\]](#E: polytope growth program){reference-type="eqref" reference="E: polytope growth program"} cannot be similarly decomposed as on this step the variables $c_{i}^T$ and $d_{i}$ affect all of the constraints. However, this program is substantially smaller as we have fixed $2mK\sum_{i} \ensuremath{{\left\vert \ensuremath{\mathcal{A}}_{i} \right\vert}}$ of the semidefinite variables as constants and replaced them with $2m$ linear variables representing the polytope. This program is much more amenable to being solved as a single program.

# Seeding Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} {#A: Seeding}

Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} must be initialized with a polytope $\ensuremath{\mathcal{P}}_{0}$ for which [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"} is feasible. In principle, the alternation proposed in Section [5](#S: Bilinear Alternation){reference-type="ref" reference="S: Bilinear Alternation"} can be seeded with an arbitrarily small polytope around a collision-free seed point. This seed polytope is then allowed to grow using Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}. However, this may require running several dozens of iterations of Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} for each seed point which can become prohibitive as the number of degrees of freedom in our robot or the complexity of the scene grows. It is therefore advantageous to seed with as large a region as can be initially certified.

Here we discuss an extension of the  algorithm in [@deits2015computing] which uses nonlinear optimization to rapidly generate large regions in TC-space. These regions are not guaranteed to be collision-free and therefore they must still be passed to Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} to be certified, but do provide good initial guesses. In this section, we will assume that the reader is familiar with  and will only discuss the modification required to use it to grow TC-space regions. Detailed pseudocode is available in Appendix [16](#S: iris pseudocode){reference-type="ref" reference="S: iris pseudocode"}.

 grows regions in a given space by alternating between two subproblems: and . The is exactly the program described in [@boyd2004convex Section 8.4.2] and we do not need to modify it. The subproblem finds a set of hyperplanes which separate the ellipse generated by from all of the obstacles. This subproblem is solved by calling two subroutines: and . The former finds the closest point on a given obstacle to the ellipse, while the latter places a plane at the point found in that is tangent to the ellipsoid.

The original work of [@deits2015computing] assumes convex obstacles which enables to be solved as a convex program and for the output of to be globally separating plane between the obstacle and the ellipsoid of the previous step. Due to the non-convexity of the TC-space obstacles in our problem formulation, finding the closest point on an obstacle exactly becomes a computationally difficult problem to solve exactly [@ferrier2000computation]. Additionally, placing a tangent plane at the nearest point will be only a locally separating plane, not a globally separating one.

To address the former difficulty, we formulate as a nonlinear program. Let the current ellipse be given as $\ensuremath{\mathcal{E}}= \{Qs + s_{0}\mid \ensuremath{\left\| s \right\|}_2 \leq 1 \}$ and suppose we have the constraint that $s \in \ensuremath{\mathcal{P}}= \{s \mid Cs \leq d\}$. Let $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ be two collision pairs and ${}^{\ensuremath{\mathcal{A}}}p_{\ensuremath{\mathcal{A}}}, {}^{\ensuremath{\mathcal{B}}}p_{\ensuremath{\mathcal{B}}}$ be some point in bodies $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ expressed in some frame attached to $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$. Also, let ${}^{W}X^{\ensuremath{\mathcal{A}}}(s)$ and ${}^{W}X^{\ensuremath{\mathcal{B}}}(s)$ denote the rigid transforms from the reference frames $\ensuremath{\mathcal{A}}$ and $\ensuremath{\mathcal{B}}$ to the world frame respectively. We remind the reader that this notation is drawn from [@tedrakeManip]. The closest point on the obstacle subject to being contained in $\ensuremath{\mathcal{P}}$ can be found by solving the program $$\begin{gather} 
\min_{s, {}^{\ensuremath{\mathcal{A}}}p_{\ensuremath{\mathcal{A}}}, {}^{\ensuremath{\mathcal{B}}}p_{\ensuremath{\mathcal{B}}}} (s - s_{0})^TQ^TQ(s-s_{0}) \mathop{\mathrm{\textbf{subject\ to}}}\\
{}^{W}X^{\ensuremath{\mathcal{A}}}(s){}^{\ensuremath{\mathcal{A}}}p_{\ensuremath{\mathcal{A}}} = {}^{W}X^{\ensuremath{\mathcal{B}}}(s){}^{\ensuremath{\mathcal{B}}}p_{\ensuremath{\mathcal{B}}} \label{E: same point constraint}\\
Cs \leq d
\end{gather}\label{E: closest point}$$ This program searches for the nearest configuration in the metric of the ellipse such that two points in the collision pair come into contact. We find a locally optimal solution $(s^{\star},  {}^{\ensuremath{\mathcal{A}}}p_{\ensuremath{\mathcal{A}}}^{\star}, {}^{\ensuremath{\mathcal{B}}}p_{\ensuremath{\mathcal{B}}}^{\star})$ to the program using a fast, general-purpose nonlinear solver such as [@gill2005snopt]. The tangent plane to the ellipse $\ensuremath{\mathcal{E}}$ at the point $s^{\star}$ is computed by calling , then appended to the inequalities of $\ensuremath{\mathcal{P}}$ to form $\ensuremath{\mathcal{P}}'$. This routine is looped until [\[E: closest point\]](#E: closest point){reference-type="eqref" reference="E: closest point"} is infeasible at which point is called again.

Once a region $\ensuremath{\mathcal{P}}=\{s \mid Cs \leq d\}$ is found by Algorithm [\[A: SNOPT IRIS\]](#A: SNOPT IRIS){reference-type="ref" reference="A: SNOPT IRIS"}, it will typically contain some minor violations of the non-collision constraint. To find an initial, feasible polytope $\ensuremath{\mathcal{P}}_{0}$ to use in Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"}, we search for a minimal uniform contraction $\delta$ of $\ensuremath{\mathcal{P}}$ such that $\ensuremath{\mathcal{P}}_{\delta} = \{s \mid Cs \leq d - \delta*1\}$ is collision-free. This can be found by bisecting over the variable $\delta \in [0, \delta_{\max}]$ and solving repeated instances of [\[E: cert by hyperplane poly\]](#E: cert by hyperplane poly){reference-type="eqref" reference="E: cert by hyperplane poly"}.

Seeding Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} with a $\ensuremath{\mathcal{P}}_{0}$ as above can dramatically reduce the number of alternations required to obtain a fairly large region and is frequently faster than seeding Algorithm [\[Alg: Bilinear Alternation\]](#Alg: Bilinear Alternation){reference-type="ref" reference="Alg: Bilinear Alternation"} with an arbitrarily small polytope.

# Supplementary Algorithms {#S: iris pseudocode}

We present a pseudocode for the algorithm presented in Appendix [15](#A: Seeding){reference-type="ref" reference="A: Seeding"}. A mature implementation of this algorithm can be found in [Drake](https://github.com/RobotLocomotion/drake/blob/2f75971b66ca59dc2c1dee4acd78952474936a79/geometry/optimization/iris.cc)[^10].

::: algorithm
$(C, d) \gets$ robot joint limits\
$\ensuremath{\mathcal{P}}_{0} \gets \{s \mid Cs \leq d\}$\
$\ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}_{0}} \gets$ $(\ensuremath{\mathcal{P}}_{0})$\
$j \gets$ number of rows of $C$\
$(\ensuremath{\mathcal{P}}_{i}, \ensuremath{\mathcal{E}}_{\ensuremath{\mathcal{P}}_{i}})$
:::

[^1]: A problem is said to be APX-hard if no polynomial time algorithm can achieve an approximation ratio of $1+\delta$ for some $\delta > 0$ unless $P = NP$.

[^2]: <https://drake.mit.edu/>

[^3]: For technical reasons, we formally assume that the bodies are compact, convex sets expressible as a Archimedean, basic semi-algebraic sets. See Appendix [10](#A: Archimedean){reference-type="ref" reference="A: Archimedean"} for the definition of Archimedean

[^4]: In monogram notation, the pose of a frame $A$ expressed in a frame $F$ is denoted as $\leftidx{^F}X^{A}$.

[^5]: Since joint $i_n$ is the last joint on this chain $\mathcal{I}_{F, A}$, we assume $\leftidx{^{C_{i_n}}}X^{P_{i_{n+1}}} = I$.

[^6]: An alternative approach is to write the forward kinematics $p_w(q)$ as a multilinear polynomial of indeterminates $c_i=\cos(\theta_i)$ and $s_i=\sin(\theta_i)$, with the additional constraints $c_i^2+s_i^2=1$. We don't choose this parameterization as it is hard to integrate the volume on the quotient ring $c_i^2+s_i^2=1,\;\forall i$. Also this parameterization requires introducing two variables $c_i, s_i$ for each revolute joint, rather than one variable $t_i$.

[^7]: We have that $\gamma \ge r \ensuremath{\left\| a \right\|}$ if and only if the Schur complement $\begin{bmatrix}\gamma I_3 &ra\\ ra^T & \gamma\end{bmatrix}\succeq 0$.

[^8]: #P-hard problems are at least as hard as NP-complete problems [@provan1983complexity].

[^9]: A matrix $X$ is positive semidefinite if and only if $\forall\bar{u}, \begin{bmatrix}\bar{u}\\1\end{bmatrix}^TX\begin{bmatrix}\bar{u}\\1\end{bmatrix}\ge 0$

[^10]: <https://github.com/RobotLocomotion/drake/blob/2f75971b66ca59dc2c1dee4acd78952474936a79/geometry/optimization/iris.cc#L440>
