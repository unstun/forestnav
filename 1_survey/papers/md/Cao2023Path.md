---
citation_key: Cao2023Path
arxiv_id: 2305.00271
arxiv_url: https://arxiv.org/abs/2305.00271
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:46:12Z
origin: ai+web
reviewed: false
---

# Supplementary Material {#supplementary-material .unnumbered}

A video illustrating the simulation and experiments is available at https://youtu.be/igP7eaOyZuc. The supplementary document and the source code can be found at https://github.com/caomuqing/tethered_robots_path_planning.

# Introduction

Tethered robots are connected to fixed or mobile objects via tether cables [@Tognon2017tether]. Depending on the applications, a tether cable may supply uninterrupted power to a robot, ensure a robust communication link, or act as a physical connection to an item for transportation. Despite the benefits, a cable is prone to entanglements with surrounding obstacles, which may greatly limit the reachable space of the robot and even cause collisions. Therefore, the path planning of tethered robots is an important topic to ensure the safety of the operations. Path planning of a single tethered robot has been well studied by the research community and efficient algorithms have been proposed to navigate a tethered robot around the obstacles in a planar or 3-D environment [@Teshnizi2014; @Yang2022; @kim2014path]. Recently, collaborative tethered robots have also been studied for applications such as search and exploration [@Shapovalov2020Exploration; @Petit2022], object gathering and removal [@Su2022; @Bhattacharya2015], and item transportation [@Kotaru2020]. Despite increasing interest in the path planning of multiple tethered robots, it is still a challenging problem due to the complex interactions among the cables and the difficulty in modeling the entanglement.

:::: {#fig: simulation .figure}
\[0.99\]![image](Cao2023Path_figs/no_entangle-removebg.png){width="85%"}\
\[0.99\]![image](Cao2023Path_figs/got_entangle-removebg.png){width="85%"}

::: caption
Simulations of multiple tethered UAVs to reach random targets using (a) the proposed approach and (b) a baseline approach that does not take tethers into consideration.
:::
::::

Existing works address this problem by restricting the problem settings or simplifying the cable model. @Sinden1990 considers a planar workspace and focuses on finding a permissible sequence of visiting the targets such that the straight cables do not cross each other. A planar workspace is also considered in @Zhang2019, but the robots are allowed to push the other cables when in contact. @Rajan2016 propose an entanglement detection system for a chain of tethered robots, which requires additional hardware on each robot for the measurement of tension and angles. @hert1999motion [@hert1996ties] consider the navigation of multiple robots in a 3-D workspace with fully stretched cables, and define entanglement as any bending due to cable-cable contacts. A movement of a robot results in a triangular area swept by the straight cable, hence feasible paths are found by checking intersections between the swept area and the other cables. In practice, cables are hardly fully straight, hence such an approach does not guarantee collision avoidance and non-entanglement. The recent work [@cao2022neptune] presents a distributed approach for trajectory planning of multiple tethered robots with consideration for slack cables. Relying on a topology-guided heuristic that records the crossings among the cables, the approach generates feasible paths in an efficient manner. However, the approach does not guarantee non-entanglement and falls into deadlocks when the number of robots increases.

The theories of knots and braids are important topics in the field of low-dimensional topology [@prasolov1997knots] and have seen recent applications in robotic systems to fold and unfold physical knots. Disentangling one or multiple cables using robot arms is studied in [@Yan2020; @Shivakumar-RSS-22]. @Antonio2022folding plan paths for a team of unmanned aerial vehicles (UAVs) to form a desired knot pattern using a long cable. The results of these works are not applicable to our problem, as they allow grasping and pulling at multiple locations along a cable, while a tethered robot is only connected to the end of a cable. Braid theory has also been applied in recent works to characterize the topology of the interactions among moving robots[@Diaz2017multirobot; @Mavrogiannis2019]. However, the connection between braids and tethered robots remains unrevealed.

In this work, we aim to answer the following questions: (1) is the entanglement of the cables in a multi-robot scenario associated with special topological patterns in the braids? (2) can non-entangling paths be generated for multiple tethered robots in a bounded workspace, considering a slack cable model? We first provide a formal definition of entanglement based on the concepts of isotopy and elementary moves. By introducing a parameter that defines the allowable bending in the cables, our definition of entanglement is applicable to both slack and taut cables. To answer the first question, we establish the topological equivalence between the cables and the space-time trajectories of the robots. Then, by acquiring a topological characterization of the entangled space-time trajectories using braids, we identify particular braid patterns necessary for the occurrence of entanglements. The key insight is that any entanglements, however complex, are resulted from a few interaction patterns between $2$ or $3$ robots. To address the second question, we propose a graph search algorithm that searches for a feasible topology of paths using the concept of permutation grids. The algorithm efficiently rejects path topologies that result in entangling braid patterns and hence guarantees non-entanglement for the generated paths. The proposed algorithm is evaluated in a simulation involving $6$ to $10$ robots. Comparisons with the existing approaches show that our approach is the only one that completes all tasks successfully. The main contributions of this work are summarized as follows:

- We present a formal definition of entanglement for multiple tethered robots applicable to both taut and slack cable models;

- We identify the braid patterns necessary for the occurrence of entanglement and establish the conditions for generating non-entangling trajectories;

- A permutation grid search algorithm is proposed to generate guaranteed non-entangling paths considering a slack cable model;

- The effectiveness of the algorithm in entanglement prevention is verified in realistic simulations and comparison with the existing approaches.

- Flight experiments using three UAVs verify the practicality of the approach in real tethered systems.

To the best of our knowledge, this is the first work that addresses the path planning of multiple tethered robots with guaranteed non-entanglement using a slack cable model.

The rest of this paper is organized as follows. Notations and preliminary concepts related to isotopy and braids are discussed in Section [2](#sec:prelim){reference-type="ref" reference="sec:prelim"}. In Section [3](#sec:braids){reference-type="ref" reference="sec:braids"}, we introduce a procedure to obtain a topological characterization of entanglements using the theory of braids and present detailed proofs. Section [4](#sec:planning){reference-type="ref" reference="sec:planning"} presents the path planning algorithm using permutation grids. Section [5](#sec:simulation){reference-type="ref" reference="sec:simulation"} introduces the simulation setup and discusses the simulation results. Flight experiments using small UAVs are presented in Section [6](#sec: exp){reference-type="ref" reference="sec: exp"}. Section [7](#sec:conclusion){reference-type="ref" reference="sec:conclusion"} draws the conclusion.

# Preliminaries {#sec:prelim}

## Notation

In this paper, $\mathbb{R}^n$ denotes the $n$-dimensional Euclidean space, $\mathbb{Z}^+$ indicates the set of positive integers. $\mathcal{I}_{n}$ denotes the set consisting of integers $1$ to $n$, i.e., $\mathcal{I}_{n} = \{1,\dots,n\}$. A line segment with two boundary points $a$ and $b$ is denoted by $\mkern 1.5mu\overline{\mkern-1.5muab\mkern-1.5mu}\mkern 1.5mu$. More symbols will be introduced when they appear in the paper.

## Elementary Moves and Isotopy {#subsec: elementary}

:::: {#fig: elementary .figure latex-placement="!t"}
![](Cao2023Path_figs/elementarymove.jpg){width="80%"}

::: caption
An illustration of an elementary move.
:::
::::

In this work, we consider a 3-Dimensional Euclidean space bounded by two horizontal planes, $\hat{\mathcal{Q}}=\{(x,y,z)|(x,y)\in\mathcal{Q},0\leq z\leq h\}$, where $\mathcal{Q}\subset\mathbb{R}^2$ is a simply connected 2-D region, $h$ is the height of the workspace. Denote the intersection between $\hat{\mathcal{Q}}$ and the level plane $z=l\in[0,h]$ as $\hat{\mathcal{Q}}_{l}$, i.e., $\hat{\mathcal{Q}}_{l}=\{(x,y,z)|(x,y)\in\mathcal{Q},z=l\}$. Consider a set of non-intersecting continuous curves, each starting from the floor of the workspace, $\hat{\mathcal{Q}}_0$, and ending at the ceiling of the workspace, $\hat{\mathcal{Q}}_h$. A polygonal approximation of the curves is a set of polygonal lines that shares the same starting and ending points with the original curves, and can be continuously deformed into the original curves without intersecting each other. Consider $\mkern 1.5mu\overline{\mkern-1.5muc_1c_2\mkern-1.5mu}\mkern 1.5mu$ to be an edge on a polygonal chain, as shown in Figure [2](#fig: elementary){reference-type="ref" reference="fig: elementary"}. Let $c_1'$ be a point in $\hat{\mathcal{Q}}$ such that the triangle $\Delta c_1c_1'c_2$ does not intersect with any other polygonal chains. An elementary move is an operation that replaces $\mkern 1.5mu\overline{\mkern-1.5muc_1c_2\mkern-1.5mu}\mkern 1.5mu$ by $\mkern 1.5mu\overline{\mkern-1.5muc_1c_1'\mkern-1.5mu}\mkern 1.5mu\cup\mkern 1.5mu\overline{\mkern-1.5muc_1'c_2\mkern-1.5mu}\mkern 1.5mu$, or in the case that $\mkern 1.5mu\overline{\mkern-1.5muc_1c_1'\mkern-1.5mu}\mkern 1.5mu\cup\mkern 1.5mu\overline{\mkern-1.5muc_1'c_2\mkern-1.5mu}\mkern 1.5mu$ is part of the original chain, replace it by $\mkern 1.5mu\overline{\mkern-1.5muc_1c_2\mkern-1.5mu}\mkern 1.5mu$ [@prasolov1997knots].

::: defn
**Definition 1** (Isotopy). *Two sets of polygonal lines in $\hat{\mathcal{Q}}$ are isotopic or ambient isotopic if one set of lines can be transformed into the other through a sequence of elementary moves.*
:::

Consider a projection of polygonal lines onto a plane perpendicular to the X-Y plane. At the intersections between polygonal lines, overpasses and underpasses are defined based on their spatial relations in 3-D. An elementary move in 3-D has a corresponding elementary move in 2-D, as shown in the bottom left of Figure [2](#fig: elementary){reference-type="ref" reference="fig: elementary"}. Similarly, two sets of projected polygonal lines in 2-D are isotopic or plane isotopic, if a sequence of 2-D elementary moves can be applied to transform one to another.

## Topological Braids

The Artin $n$-braid group, denoted as $B_n$, is a group with $n-1$ generators $\sigma_1, \sigma_2,\dots,\sigma_{n-1}$ and the group relations [@Kassel2008] $$\begin{align}
    \sigma_i\sigma_j=\sigma_j\sigma_i, \; i,j\in\mathcal{I}_{n-1},|i-j|\geq2,\\
    \sigma_i\sigma_{i+1}\sigma_i=\sigma_{i+1}\sigma_{i}\sigma_{i+1},\;i\in\mathcal{I}_{n-2}.\label{eq: braidgroup}
\end{align}$$ The identity element in the group is denoted as $e$. $B_2$ is generated by a single generator $\sigma_1$ with no group relations, and $B_3$ is generated by $\sigma_1, \sigma_2$ and relation ([\[eq: braidgroup\]](#eq: braidgroup){reference-type="ref" reference="eq: braidgroup"}). A braid, $b\in B_n$ can be written as a composition of group generators and their inverses, $b=\tau_1\tau_2\dots\tau_K$, where $K$ is the length of the braid, $\tau_i\in\{\sigma_1^{\pm1},\sigma_2^{\pm1},\dots,\sigma_{n-1}^{\pm1}\}$ is called an elementary braid.

A curve or a polygonal line is called ascending if it is monotonically increasing in $z$, in other words, each horizontal plane intersects with an ascending line at only one point. An $n$-braid can be represented in a 2-D diagram consisting of $n$ ascending strings $X_i(z):[0,1]\rightarrow\mathbb{R}$, $i\in\mathcal{I}_n$. The starting and ending points of each string satisfy $X_i(0)\in\mathcal{I}_n$, $X_i(1)\in\mathcal{I}_n$. Each elementary braid $\sigma_i^{\pm1}$ in the braid word corresponds to a crossing between the $i$-th string ($i$ denotes the order of the string when counting from left to right) and the $(i+1)$-th string, where an overpass by the $i$-th string is denoted as $\sigma_i$ and the underpass is denoted as $\sigma_i^{-1}$.

In the standard definition of braids, each braid string is only defined in the domain $\{z\in[0,1]\}$. In this work, we relax the definition by allowing the braid strings to have a domain $[0,t]$ for $t\in\mathbb{R}^+$. Furthermore, $b(t)$ indicates the braid obtained when the crossings among the braid strings in the interval $[0,t]$ are taken into account. Examples of braid diagrams are shown in the bottom left of Figure [3](#fig: overview){reference-type="ref" reference="fig: overview"}.

# Topological Characterization of Entanglements Using Braids {#sec:braids}

We consider a team of $n$ tethered robots navigating in the workspace $\hat{\mathcal{Q}}$, and assume the robots' movements to be constrained in the ceiling of the workspace $\hat{\mathcal{Q}}_h$. To reach a target position at a different height, a robot first moves to the same horizontal position, then descends to the target. Each robot is attached to a base station placed on the floor $\hat{\mathcal{Q}}_0$. The cables form a set of mutually disjoint topological intervals that start at the bottom of the workspace and end at the ceiling, as shown in the top left of Figure [3](#fig: overview){reference-type="ref" reference="fig: overview"}. A robot follows a path $q_i:[0,T_i]\rightarrow\mathcal{Q}$, where $q_i(0)=q_i^s$ is the same as the horizontal position of its base and $q_i(T_i)=q_i^d$ is a user-defined target. A scaled space-time trajectory of the robot is constructed as $\xi_i:[0,T]\rightarrow\hat{\mathcal{Q}}$, where $\xi_i(t)=(q_i(t),t\frac{h}{T})\in\mathbb{R}^3$ for $0\leq t<T_i$ and $\xi_i(t)=(q_i(T_i),t\frac{h}{T})$ for $T_i\leq t\leq T$. $T=\max_{i\in\mathcal{I}_{n}}T_i$ is the longest time taken by any robot to reach the target. At a height $z$, $0\leq z\leq h$, the collection of scaled space-time trajectories $\{\xi_i\}_{i\in\mathcal{I}_n}$ intersects with $\hat{\mathcal{Q}}$ at $n$ distinct points (given that the robot's trajectories are not in a collision). See the top right of Figure [3](#fig: overview){reference-type="ref" reference="fig: overview"} for an illustration of scaled space-time trajectories.

:::: {#fig: overview .figure latex-placement="!t"}
![](Cao2023Path_figs/overview3.jpg){width="100%"}

::: caption
Overview of the approach.
:::
::::

::: {#lm: isotopy .lem}
**Lemma 2**. *The set of cables connecting $n$ robots to their bases is isotopic to the scaled space-time trajectories of the robots.*
:::

::: proof
*Proof.* The shapes of the cables are closely related to the paths taken by the robots in the worksapce, because (1) a cable hanging from a robot will likely have its first contact with the ground in the neighbourhood of the X-Y coordinates of the robot, (2) when robot $i$ crosses a path that has taken by robot $j$, robot $i$'s cable will slide over the cable of robot $j$. Therefore, we construct an approximation of the configurations of the cables, labeled as $\Tilde{q}_i\in\mathbb{R}^3$, in the following way (graphic illustration in the top middle of Figure [3](#fig: overview){reference-type="ref" reference="fig: overview"}) $$\begin{align}
    \Tilde{q}_i(t) = 
    \begin{cases}
        (q_i(t),0),& t\in T_i\backslash T^{\text{cro}}_i\\
        (q_i(t),h_s), & t\in T^{\text{cro}}_i\\
        (q_i(T_i),h), &t>T_i.
    \end{cases}
\end{align}$$ $T^{\text{cro}}_i$ denotes a set of time intervals, each time interval is a small neighbourhood of the time that robot $i$ travels to a same location visited by another robot before, i.e., $T^{\text{cro}}_i=\{[t-\epsilon, t+\epsilon]|q_i(t)=q_j(t_j),\forall t\in(0,T_i], t_j\in(0,t), j\in\mathcal{I}_n\backslash i\}$. $h_s$ is a value greater than zero, indicating a small height that a cable is elevated to. Clearly, the set $\{\Tilde{q}_i\}_{i\in\mathcal{I}_n}$ is isotopic to the actual cables of the robots. To establish an isotopy between $\{\Tilde{q}_i\}_{i\in\mathcal{I}_n}$ and the space-time trajectories, note that we can transform $\Tilde{q}_i(t)$ to $\xi_i(t)$ by elementary moves for all $t\in[0,T]$, because they share the same X-Y coordinates for all $t$, and their order in the $z$-coordinates ($z$-order) are the same, i.e., for $\Tilde{q}_i(t)$ and $\Tilde{q}_j(t_j)$ such that $q_i(t)=q_j(t_j)$, $t>t_j$, $\Tilde{q}_i(t)$ has a higher $z$-coordinate than $\Tilde{q}_j(t_j)$, $\xi_i(t)$ also has a higher $z$-coordinate than $\xi_j(t_j)$. This is because a robot who travels to the same location at a later time has its space-time trajectory at a higher $z$-coordinate. Hence, the cables can be transformed to their corresponding space-time trajectories isotopically. ◻
:::

We specify a 2-D plane perpendicular to the X-Y plane as $\mathcal{P}(\alpha)=\{(x,y,z)|x\cos\alpha+y\sin\alpha=0,z\in\mathbb{R}\}$ where $\alpha\in[0,\pi]$ is the projection angle with respect to the positive X axis. A set of 2-D trajectories $\xi^{\alpha}_{i}:[0,T]\rightarrow\mathcal{P}(\alpha)$, $i\in\mathcal{I}_n$, is obtained by the projection of the space-time trajectories $\xi_i$ onto $\mathcal{P}(\alpha)$ (bottom right of Figure [3](#fig: overview){reference-type="ref" reference="fig: overview"}).

A crossing between 2-D trajectories indicates an event of two robots swapping positions in the projected axis. Such an event can be represented as a braid generator $\sigma_i^{\pm1}$, where $i$ indicates the ranking of the leftmost swapping robot in increasing order of the robots' projected positions. A braid word $b^{\alpha}(t)$ is obtained by joining the elementary braids representing the crossing events that have occurred from time $0$ to time $t$. Let $b^\alpha_{i,j,k}(t)$ be the $3$-braid obtained by removing all the trajectories except for the trajectories of robots $i,j,k$. Similarly, $b^\alpha_{i,j}(t)$ indicates the $2$-braid obtained when only considering the crossings between robots $i$ and $j$. Here, $i,j,k\in\mathcal{I}_n$ are the fixed indices of the robots. For each braid word, an equivalent braid diagram can be drawn, as shown in the bottom left of Figure [3](#fig: overview){reference-type="ref" reference="fig: overview"}.

We have introduced a procedure to obtain a topological characterization of robot paths in the form of braids. To establish a connection between the entanglements of cables and the topological braids, we first provide a formal definition of the entanglement based on the horizontal bending angles of the cables. As described in Section [2.2](#subsec: elementary){reference-type="ref" reference="subsec: elementary"}, the cables can be approximated as a set of non-intersecting polygonal segments, and elementary moves can be applied to shorten the length of the cables while preserving isotopy. Another interpretation of this shortening process is that the base station exerts tension on the cable and retracts the cable while the robots hold their positions. The cables are shortened until they are either completely straight or in contact with other cables.

::: defn
**Definition 3** (Maximum angle of rotation). *Given a poly-gonal approximation of the cables, denoted as $\mathcal{C}$, a set of projected line segments onto the X-Y plane can be obtained. Each segment is assigned a direction consistent with the direction from the base to the robot (Figure [4](#fig: ent_angle){reference-type="ref" reference="fig: ent_angle"}). $\gamma_i(\mathcal{C})$ is the maximum angle of rotation between any of the projected segments of robot $i$, $\gamma_i\in[0,\pi]$. The maximum angle of rotation of the entire team for this particular polygonal approximation is $\gamma(\mathcal{C})=\max_{i\in\mathcal{I}_n}\gamma_i(\mathcal{C})$. The minimum of $\gamma$ among all isotopic polygonal approximations of the cables is denoted as $\underline{\gamma}$, i.e., $\underline{\gamma}=\min_{\mathcal{C}}\gamma(\mathcal{C})=\min_{\mathcal{C}}\max_{i\in\mathcal{I}_n}\gamma_i(\mathcal{C})$.*
:::

Intuitively, $\gamma(\mathcal{C})$ indicates the extent of deviation from a set of straight lines for a particular polygonal approximation $\mathcal{C}$, and $\underline{\gamma}$ indicates the minimum deviation possible, which usually occurs when the cables are fully retracted. Only horizontal bending is considered because the degree of vertical bending is small when the robots move at a similar height. Now, we give the definition of entanglement based on the bending angle.

:::: {#fig: ent_angle .figure latex-placement="!t"}
![](Cao2023Path_figs/ent_angle.png){width="60%"}

::: caption
The projected polygonal segments onto X-Y plane for robot $i$. The maximum angle of rotation, $\gamma_i$, is the rotation angle between $\mkern 1.5mu\overline{\mkern-1.5muc_4c_5\mkern-1.5mu}\mkern 1.5mu$ and $\mkern 1.5mu\overline{\mkern-1.5muc_0c_1\mkern-1.5mu}\mkern 1.5mu$. The dashed line is parallel to $\mkern 1.5mu\overline{\mkern-1.5muc_0c_1\mkern-1.5mu}\mkern 1.5mu$.
:::
::::

::: defn
**Definition 4** ($\phi$-Entanglement). *The cables are said to be $\phi$-entangled or in a state of $\phi$-entanglement when $\underline{\gamma}\geq\phi$ for a chosen $\phi\in(0,\pi]$.*
:::

:::: {#fig: entangle .figure latex-placement="!t"}
![](Cao2023Path_figs/Pentangle.jpg){width="\\linewidth"}

::: caption
An illustration of entanglement. The blue and green solid lines are the cables/trajectories of robot $i$ and $j$. The blue dashed lines are the cable/trajectory of robot $i$ projected onto the X-Y plane. The bottom two plots show the projections of the cables/trajectories onto a plane $\mathcal{P}(\alpha)$. In the bottom left plot, the blue projected trajectory is non-monotonic.
:::
::::

Figure [5](#fig: entangle){reference-type="ref" reference="fig: entangle"} illustrates a polygonal approximation of two cables with $\gamma_i=\underline{\gamma}=\frac{2}{3}\pi$, thus the cables are $\frac{2}{3}\pi$-entangled. When $\phi$ is chosen close to zero, any small bending in the cables is considered an entanglement, which is in line with the definition of entanglement for taut cables in [@hert1999motion]. Slack cables generally have a higher tolerance for bending, hence a higher $\phi$ may be chosen. We neglect trivial cases of entanglement where cables are bent due to coplanarity by assuming that $\{(q_i^s,0),(q_i^d,h)\}$ are not co-planar with $\{(q_j^s,0),(q_j^d,h)\}$, $\forall i,j\in\mathcal{I}_n$, $i\neq j$.

::: {#cor: spacetime .cor}
**Corollary 5**. *If the cables are $\phi$-entangled, then the space-time trajectories of robots are also $\phi$-entangled, i.e., the space-time trajectories cannot be isotopically transformed to a polygonal approximation $\mathcal{C}$ such that $\gamma(\mathcal{C})<\phi$.*
:::

Owing to Corollary [5](#cor: spacetime){reference-type="ref" reference="cor: spacetime"}, the identification of entanglement can be done by analyzing the space-time trajectories. In the following lemma, we show that given suitable projection angles, the projections of $\phi$-entangled trajectories exhibit a special property.

::: {#lm:straightline .lem}
**Lemma 6**. *Define $\mathcal{A}(m)=\{\frac{i}{m}\pi|i=0\dots m,m\in\mathbb{Z}^+\}$ to be the set of projection angles evenly dividing the range $[0, \pi]$. By setting $m>\frac{\pi}{\phi}$, there exists $\alpha\in\mathcal{A}(m)$, such that the projection of a set of $\phi$-entangled space-time trajectories onto the plane $\mathcal{P}(\alpha)$ is non-isotopic to a set of straight lines.*
:::

::: proof
*Proof.* See Section 1 of the supplementary document. ◻
:::

In the following lemma, we show that a set of projected trajectories non-isotopic to straight lines can be identified by analyzing their corresponding $2$-braids and $3$-braids.

::: {#lm:braidword .lem}
**Lemma 7**. *For a set of projected trajectories $\{\xi_i^{\alpha}(t)\}_{i\in\mathcal{I}_n}$, $t\in[0,T]$, which is non-isotopic to a set of straight lines, there exists a corresponding $3$-braid $b^\alpha_{i,j,k}(t)$ or $2$-braid $b^\alpha_{i,j}(t)$, $t\in(0,T]$, $i,j,k\in\mathcal{I}_n$, $i<j<k$, that satisfies at least one of the following:\
(1) $b^\alpha_{i,j}(t)$ is equivalent to $\sigma_1\sigma_1$ or $\sigma_1^{-1}\sigma_1^{-1}$;\
(2) $b^\alpha_{i,j,k}(t)$ is equivalent to a word in the set $\{\sigma_f^{c}\sigma^{-c}_g\sigma_f^{c}|c\in\{1,-1\},f,g\in\{1,2\}, f\neq g \}$.*
:::

:::: {#fig: straighten .figure latex-placement="!t"}
![](Cao2023Path_figs/straighten.png){width="80%"}

::: caption
The projected trajectories of robots. The gray dashed lines outline the partitioned triangles.
:::
::::

:::: {#fig: triangles .figure latex-placement="!t"}
![](Cao2023Path_figs/triangles.png){width="60%"}

::: caption
Four types of triangles. The small circles indicate either an overpass or an underpass. An elementary move may be executed from any one (respectively, two) edge of a triangle to the other two (respectively, one) edges, provided such a move preserves plane isotopy and both the edges before and after the move are ascending. To follow a temporal sequence, the edge(s) before a move should not intersect with any outgoing trajectories, except when the edge(s) belong(s) to the original polygonal trajectory.
:::
::::

::: proof
*Proof.* Consider a set of projected trajectories among which at least one is non-straight. A non-straight projected trajectory bounds a polygon area (illustrated by the area bounded by the solid dark blue and the dashed dark blue lines in Figure [6](#fig: straighten){reference-type="ref" reference="fig: straighten"}), which can be partitioned into multiple smaller triangles of $4$ types [@prasolov1997knots] (Figure [7](#fig: triangles){reference-type="ref" reference="fig: triangles"}): (I) triangles whose interiors contain a crossing between two segments; (II) triangles that contain a vertex of a polygonal trajectory; (III) triangles containing part of a straight segment without any vertex; (IV) those containing an empty space. Figure [6](#fig: straighten){reference-type="ref" reference="fig: straighten"} illustrates a partitioned polygon. Suppose we attempt to shorten a non-straight trajectory by evaluating whether an elementary move can be applied to each of the triangles. Two conditions should be satisfied: (1) the evaluation of the triangles should follow a temporal sequence, i.e., a triangle containing a later part of a trajectory is evaluated later than a triangle containing an earlier part of the same trajectory; (2) the transformed trajectory after each elementary move should be ascending in $t$, i.e., both the edges before and after an elementary move should be ascending. Given that the initial trajectories are ascending, there always exists a set of triangles and a sequence of evaluations satisfying both conditions (see Section 2 of the supplementary document for the justification for this statement). Figure [6](#fig: straighten){reference-type="ref" reference="fig: straighten"} shows a valid sequence of moves with the numbering on each triangle. If elementary moves can be applied to all triangles, then a non-straight trajectory is isotopic to a straight line. Conversely, a trajectory non-isotopic to a straight line must have some triangles to which the elementary moves are not applicable, and we call these triangles tangles. By exhaustively listing and assessing all possible forms of the triangles, we find three such tangles (and their symmetric and mirror images), as shown in Figure [8](#fig: tangles){reference-type="ref" reference="fig: tangles"}.

:::: {#fig: tangles .figure}
\[0.45\]![image](Cao2023Path_figs/trianglea.jpg){height="2.7cm"}\
\[0.45\]![image](Cao2023Path_figs/trianglec.jpg){height="2.7cm"} \[0.45\]![image](Cao2023Path_figs/triangleb.jpg){height="2.7cm"}

::: caption
Three types of local tangles. The solid blue segments cannot be moved to the dashed segments through plane isotopy. (a) A 2-trajectory tangle with a braid word $\sigma_1\sigma_1$, (b) A 3-trajectory tangle with a braid word $\sigma_1^{-1}\sigma_2\sigma_1^{-1}$. (c) A 3-trajectory tangle with a braid word $\sigma_1\sigma_2^{-1}\sigma_1\sigma_2^{-1}\sigma_1$.
:::
::::

Suppose we have applied a sequence of elementary moves on trajectory $i$ and we encounter a tangle the same as Figure [\[fig: trianglea\]](#fig: trianglea){reference-type="ref" reference="fig: trianglea"}, representing an interaction between trajectory $i$ and $j$ from time $t_1$ to $t_2$. Since both trajectories are ascending, we can obtain a braid representation of the trajectories. The $2$-braid formed up to time $t_2$, $b^\alpha_{i,j}(t_2)$, is equivalent to $\sigma_1\sigma_1$, because $b^\alpha_{i,j}(t_1)$ has been reduced to identity through previous elementary moves. Similar analysis can be applied to the symmetric and mirror images of Figure [\[fig: trianglea\]](#fig: trianglea){reference-type="ref" reference="fig: trianglea"} to obtain all the representations for $2$-braid tangles, which are $b^\alpha_{i,j}(t)=(\sigma_1\sigma_1)^{\pm 1}$.

:::: {#fig: braid3 .figure latex-placement="!t"}
![](Cao2023Path_figs/braid3.jpg){width="50%"}

::: caption
The braid diagram containing a $3$-braid tangle in the form of Figure [\[fig: triangleb\]](#fig: triangleb){reference-type="ref" reference="fig: triangleb"}.
:::
::::

Suppose we have encountered an interaction among 3 trajectories, $i,j,k\in\mathcal{I}_n$, the same as Figure [\[fig: triangleb\]](#fig: triangleb){reference-type="ref" reference="fig: triangleb"}. The $3$-braid $b^\alpha_{i,j,k}(t_2)$ is represented as a diagram shown in Figure [9](#fig: braid3){reference-type="ref" reference="fig: braid3"}, where $b^\alpha_{j,k}(t_1)$ is a $2$-braid depending on the trajectories of robot $j$ and $k$ up to time $t_1$. We first exclude the occurrence of $2$-braid tangles by assuming that the $2$-braid $b^\alpha_{j,k}(t)$ is not equivalent to $(\sigma_1\sigma_1)^{\pm 1}$, $\forall t\in [0,t_2]$. This is only possible if $b^\alpha_{j,k}(t_1)$ is equivalent to the identity or $\sigma_1$. In the first case, we have $b^\alpha_{i,j,k}(t_2)=\sigma_1^{-1}\sigma_2\sigma_1^{-1}$; in the second case, $b^\alpha_{i,j,k}(t_2)=\sigma_2\sigma_1^{-1}\sigma_2\sigma_1^{-1}$, which has a preceding braid $b^\alpha_{i,j,k}(t_0)=\sigma_2\sigma_1^{-1}\sigma_2$ for $t_0<t_2$. By applying the same analysis to all symmetric and mirror images of Figure [\[fig: triangleb\]](#fig: triangleb){reference-type="ref" reference="fig: triangleb"} and [\[fig: trianglec\]](#fig: trianglec){reference-type="ref" reference="fig: trianglec"}, and excluding cases of $2$-braid tangles, we obtain the set of words representing the $3$-braid tangles $\{\sigma_f^{c}\sigma^{-c}_g\sigma_f^{c}|c\in\{1,-1\},f,g\in\{1,2\}, f\neq g \}$.

Since the braids are invariant to the sequence of robot indices, i.e., $b_{i,j,k}(t)=b_{j,i,k}(t)=b_{k,j,i}(t)$, $\forall i,j,k\in\mathcal{I}_n$, it is sufficient to consider distinct combinations of robot pairs and triplets in the examination of $2$-braids and $3$-braids, hence the condition $i<j<k$. ◻
:::

Putting all the tools together, we provide sufficient conditions for the avoidance of entanglements.

::: {#thm:nonentangling .thm}
**Theorem 8**. *If for all $i,j,k\in\mathcal{I}_n$, $i<j<k$, $t\in(0,T]$, $\alpha\in\mathcal{A}(m)=\{\frac{i}{m}\pi|i=0\dots m,m>\frac{\pi}{\phi},m\in\mathbb{Z}^+\}$, the $3$-braids and $2$-braids, $b^\alpha_{i,j,k}(t)$ and $b^\alpha_{i,j}(t)$, obtained by projecting the space-time trajectories of $n$ robots onto $\mathcal{P}(\alpha)$, satisfies the following:*

*(1) $b^\alpha_{i,j}(t)$ is not equivalent to $\sigma_1\sigma_1$ or $\sigma_1^{-1}\sigma_1^{-1}$,*

*(2) $b^\alpha_{i,j,k}(t)$ is not equivalent to any word in the set $\{\sigma_f^{c}\sigma^{-c}_g\sigma_f^{c}|c\in\{1,-1\},f,g\in\{1,2\}, f\neq g \}$,\
then, the cables of $n$ robots are not $\phi$-entangled for all time $t\in[0,T]$.*
:::

::: proof
*Proof.* Given that conditions (1) and (2) hold, Lemma [7](#lm:braidword){reference-type="ref" reference="lm:braidword"} guarantees that the projected trajectories $\{\xi_i^\alpha\}_{i\in\mathcal{I}_n}$ are always isotopic to a set of straight lines, $\forall \alpha\in\mathcal{A}(m)$, $t\in(0,T]$. Lemma [6](#lm:straightline){reference-type="ref" reference="lm:straightline"} ensures that the space-time trajectories are not $\phi$-entangled throughout the time interval $(0,T]$. Finally, due to the isotopy between the cables and the space-time trajectories (Lemma [2](#lm: isotopy){reference-type="ref" reference="lm: isotopy"}), the theorem is proven. ◻
:::

# Planning Using Permutation Grid {#sec:planning}

In this section, we present the approach for path planning of $n$ robots free of $\phi$-entanglement for any $\phi>\frac{\pi}{2}$. To ensure Lemma [6](#lm:straightline){reference-type="ref" reference="lm:straightline"} holds for $\phi>\frac{\pi}{2}$, we choose $m=2$ projection axes perpendicular to each other, and obtain the sequence of the robots in increasing order of their projected positions. The order of robot $i$ on the $l$-th projection axis is denoted by $p_i^l\in\mathcal{I}_n$, $l\in\{1,2\}$. A permutation grid is a $n\times n$ grid space in which each robot takes a position at $(p_i^1,p_i^2)\in\mathbb{R}^2$, and none of the robot pairs occupies the same row or column, as shown in Figure [10](#fig: permgrid){reference-type="ref" reference="fig: permgrid"}. In this way, we abstract the Euclidean workspace $\mathcal{Q}$ into a discrete grid space, and the continuous positions of the robots into permutations. A move of a robot on the permutation grid always induces an opposite movement of the adjacent robot. Hence, given a set of robot permutation positions $\Phi=\{p_i^l|i\in\mathcal{I}_n,l\in\{1,2\}\}$, the one-step action space $\mathcal{U}$ consists of exchanging the positions of the adjacent robots, $p_i^l$ and $p_j^l$, $\forall p_j^l=p_i^l+1, p_i^l\in\mathcal{I}_n\backslash n, i,j\in\mathcal{I}_n, l\in\{1,2\}$. Each action represents an elementary $2$-braid $\tau\in\sigma_1^{\pm1}$ added to the $2$-braid $b_{i,j}^l$, and an elementary $3$-braid $\tau\in\{\sigma_1^{\pm1},\sigma_2^{\pm1}\}$ added to each $3$-braid involving robot $i$ and $j$, $b_{i,j,k}^l$, $k\in\mathcal{I}_n\backslash\{i,j\}$.

:::: {#fig: permgrid .figure latex-placement="!t"}
![](Cao2023Path_figs/perm_grid.jpg){width="100%"}

::: caption
Left: the positions of robots in the projected space. Right: a $5\times5$ permutation grid.
:::
::::

::: algorithm
($\text{GraphSearch}$) InsertStartingNode(openList,$\Phi^s$,$\mathcal{B}$) $\text{node}$ = openList.pop() move $\text{node}$ to closedList return RetrievePath()[]{#ln:retrievepath label="ln:retrievepath"} $\text{childNode}$ = initializeChild($\text{node},u$)[]{#ln: childinitialize label="ln: childinitialize"} $\tau$ = compute2Braid($i,j,\text{childNode}.\Phi$)[]{#ln:2braidstart label="ln:2braidstart"}= updateCheck2Braid($\text{childNode}.b_{i,j}^l,\tau$)[]{#ln:2braidcheck label="ln:2braidcheck"}[]{#ln:if2braidvalid label="ln:if2braidvalid"} reject $\text{childNode}$ []{#ln:2braidend label="ln:2braidend"} $i,j,k$ = sort($i,j,k$) $\tau$ = compute3Braid($i,j,k,\text{childNode}.\Phi$)= updateCheck3Braid($\text{childNode}.b_{i,j,k}^l,\tau$) reject $\text{childNode}$ []{#ln:3braidend label="ln:3braidend"} updateCosts($\text{childNode}$) Update cost and parent if new cost is lower Add $\text{childNode}$ to openList return emptyPath []{#ln: endentangle label="ln: endentangle"}
:::

A graph search approach (Algorithm [\[alg: graphsearch\]](#alg: graphsearch){reference-type="ref" reference="alg: graphsearch"}) is used to generate a feasible path from a set of initial permutation positions, $\Phi^s$, to the target permutation positions, $\Phi^d$. Each graph node represents a set of robot positions on the grid, $\Phi$, and carries the $2$-braids and $3$-braids representing the crossing actions that have taken place in all 2-robot pairs and 3-robot triplets. In every iteration, a node is popped from the open list, and child nodes are generated from the set of permutation actions (line [\[ln: permset\]](#ln: permset){reference-type="ref" reference="ln: permset"}-[\[ln: childinitialize\]](#ln: childinitialize){reference-type="ref" reference="ln: childinitialize"}) by exchanging the positions of robot $i$ and robot $j$ on the $l$-th axis. Then, the elementary $2$-braid $\tau$ induced by the permutation action is computed, and the word $b_{i,j}^l$ is updated and checked against the condition in Theorem [8](#thm:nonentangling){reference-type="ref" reference="thm:nonentangling"} (line [\[ln:2braidstart\]](#ln:2braidstart){reference-type="ref" reference="ln:2braidstart"}-[\[ln:2braidcheck\]](#ln:2braidcheck){reference-type="ref" reference="ln:2braidcheck"}). A child node that does not satisfy the condition for $2$-braid is rejected immediately. Similarly, all $3$-braids involving robots $i$ and $j$ are updated and evaluated (line [\[ln:3braidstart\]](#ln:3braidstart){reference-type="ref" reference="ln:3braidstart"}-[\[ln:3braidend\]](#ln:3braidend){reference-type="ref" reference="ln:3braidend"}). The heuristic cost is the sum of the Manhattan distances for all robots to reach their targets. In practice, a bias larger than one is chosen to favor nodes closer to the targets. The search process continues until a node that reaches $\Phi^d$ is found (line [\[ln:reachestarget\]](#ln:reachestarget){reference-type="ref" reference="ln:reachestarget"}-[\[ln:retrievepath\]](#ln:retrievepath){reference-type="ref" reference="ln:retrievepath"}). The pseudocodes for the updateCheck2Braid and updateCheck3Braid functions are available in Section 3 of the supplementary document.

The output of the search algorithm is a path from the initial permutation to the target permutation, $\Phi^s,\Phi^1,\Phi^2,\dots,\Phi^d$, which defines a specific topology of the path in the real workspace. In our approach, we use a simple linear function $\theta:[0,\pi]\times(\mathcal{I}_n\times\mathcal{I}_n)\rightarrow\mathcal{Q}$ to map the permutation grid to a $n\times n$ grid in the workspace, where the grid size is larger than a safety distance between robots to ensure collision avoidance. Hence, the robots follow a set of waypoints $\theta(\alpha,\Phi^s),\theta(\alpha,\Phi^1),\dots\theta(\alpha,\Phi^d)$, and finally move to $\{q_i^d\}_{i\in\mathcal{I}_n}$ using straight paths. During the movements of robots, the $2$-braids and $3$-braids are updated when crossings between robots take place. These updated braid words can be used as initial conditions for subsequent planning with guaranteed entanglement avoidance.

# Simulations {#sec:simulation}

Simulations of multiple tethered UAVs are conducted in Unity game editor with AGX Dynamics plugin [^1] installed to accurately simulate the dynamics of the cables and the effect of entanglements on the robots. A slack and non-retractable cable of fixed length is attached to each simulated UAV. The proposed permutation grid planning algorithm is implemented as a Robot Operating System (ROS) program which transmits the planned waypoints to the simulator through ROS TCP Connector [^2]. In each simulation run, a team of $6$ to $10$ UAVs is tasked to travel to $100$ sets of target positions. A task is successful when all robots reach their assigned targets; if a set of targets cannot be reached or some of the robots are stuck, the task fails and the targets will be updated.

The following existing approaches are used for comparison: (1) Neptune [@cao2022neptune], a distributed trajectory planning approach for multiple tethered robots considering a slack cable model; (2) Hert [@hert1999motion], a centralized approach considering fully stretched cables; (3) a baseline multi-robot trajectory planner without the cable-related constraints, labeled as Neptune\* (the codes for both Neptune and Neptune\* are released by the authors of [@cao2022neptune]). In all simulations, the proposed and the compared algorithms run on a mini-computer with Intel i7-8550U CPU. Two screenshots of simulations are shown in Figure [1](#fig: simulation){reference-type="ref" reference="fig: simulation"}. A video of the simulations can be viewed in the supplementary material.

:::: {#fig: benchmark .figure latex-placement="!t"}
![](Cao2023Path_figs/benchmark.png){width="100%"}

::: caption
Plots of the success rate, the average computation time, and the average distance traveled for the proposed and the compared approaches.
:::
::::

Figure [11](#fig: benchmark){reference-type="ref" reference="fig: benchmark"} shows the success rate, the computation time, and the distance traveled for all approaches with respect to the number of robots involved. From the top plot, we can observe that the proposed approach is the only one to ensure all tasks are successfully completed. The success rate of Neptune is close to $100\%$ with $6$ robots but drops to below $80\%$ when the number of robots increases to $10$. As a distributed approach, Neptune is unable to guarantee feasible and entanglement-free paths for all robots, hence freezing robots are observed in the simulation. The success rates of Neptune\* and Hert are significantly lower than the other two approaches. In both approaches, the entanglement of the cables accumulates and results in a huge tangle in the center of the workspace (Figure [\[fig: gotentangle\]](#fig: gotentangle){reference-type="ref" reference="fig: gotentangle"}). Eventually, only the targets near the tangle can be reached by the robots. Hert generates 3-D paths that require a robot to move below a taut cable to avoid cable contacts. However, in the case of a slack cable model, moving vertically does not generate the same path topology as in the case of taut cables, because slack cables lie on the ground. Hence, the performance of Hert is only comparable to a baseline multi-robot planner where cables are not considered at all.

The middle plot shows the computation time of all approaches. Both distributed approaches generate initial trajectories within $100$ms, but the generated trajectories only ensure collision avoidance for a short planning horizon, and frequent online replanning is required. Our approach generates trajectories for all robots in a one-time computation. The computation time increases with the number of robots, but an average computation time of $3$s for $10$ robots is acceptable as a waiting time for on-demand targets. Although both our approach and Hert are centralized approaches, we rely on pre-computed reduction rules to efficiently update braids and check entanglement. On the other hand, the computation time of Hert is burdened by the expensive line-triangle intersection checking procedure to avoid cable-cable contacts.

One weakness of the proposed approach is the length of the generated paths, as seen from the bottom plot. The average distance traveled for each robot (only considering successful tasks) is considerably higher in our approach. This is due to the direct mapping of paths in a permutation grid into the real workspace. Every movement of a robot accompanies an opposite movement of another robot, which could be unnecessary and increases the distance traveled by each robot. Although direct mapping is an inefficient strategy, it is a simple implementation to validate the effectiveness of the proposed approach in generating entanglement-free paths. In our future work, efficient topology-guided path generation will be studied and integrated with the proposed permutation grid search.

# Flight Experiment {#sec: exp}

We verify the practicality of the proposed approach using three small tethered UAVs in a $5$m$\times5$m$\times2$m indoor area. Each UAV is connected to a ground power supply using a long power cable. Random targets are generated during the experiment, and a ground computer computes the paths and sends them to the UAVs through a Wifi network. Figure [12](#fig: experiment){reference-type="ref" reference="fig: experiment"} illustrates a flight experiment, where the robots and their cables are highlighted for easy identification. The supplementary video shows an experiment in which three UAVs complete $25$ sets of targets successfully and remain untangled. The average computation time on a computer with Intel i7-8750H CPU is less than $10$ms, which guarantees the online performance of the algorithm. The average completion time for a set of targets is $12.5$s with $0.7$m/s maximum velocity of the UAVs.

:::: {#fig: experiment .figure latex-placement="!t"}
![](Cao2023Path_figs/neptune2_exp.png){width="100%"}

::: caption
Left: photos of a flight experiment. Right: visualization of positions and goal points of the robots.
:::
::::

# Conclusion {#sec:conclusion}

In this work, we have investigated the problem of path planning for multiple tethered robots. The main contribution of this work is to establish the connection between the entanglements of the cables and the topological braids representing robots' trajectories. This is accomplished by (1) showing the topological equivalence between the cables and the robots' space-time trajectories, (2) converting the projected space-time trajectories into braids, and (3) identifying particular braid patterns that are necessary for the occurrence of entanglements. A graph search algorithm based on the permutation grid has been proposed for generating a feasible topology of robot paths, and paths containing the entangling braids patterns are guaranteed to be rejected. Simulations and experiments demonstrate the effectiveness of the proposed algorithm in avoiding entanglement in complex and realistic scenarios. To address the issue of long path length highlighted by the simulation results, our future research will focus on efficient multi-robot path generation in Euclidean space given a specific path topology.

# Acknowledgments {#acknowledgments .unnumbered}

This research was conducted under project WP5 within the Delta-NTU Corporate Lab with funding support from A\*STAR under its IAF-ICP programme (Grant no: I2201E0013) and Delta Electronics Inc, and the Wallenbery-NTU Presidential Postdoctoral Fellowship in Nanyang Technological University, Singapore. We thank Dr. Fedor Duzhin for providing valuable suggestions to improve the manuscript and Mr. Xinhang Xu for providing the hardware platform for simulation.

[^1]: https://www.algoryx.se/agx-dynamics/

[^2]: https://github.com/Unity-Technologies/ROS-TCP-Connector
