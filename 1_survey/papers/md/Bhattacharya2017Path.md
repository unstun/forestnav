---
citation_key: Bhattacharya2017Path
arxiv_id: 1710.02871
arxiv_url: "https://arxiv.org/abs/1710.02871"
title: "Path Homotopy Invariants and their Application to Optimal Trajectory Planning"
authors_short: "Subhrajit Bhattacharya et al."
year: 2017
direction_tag: J_homotopy_topology
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:53:42Z
origin: ai+web
reviewed: false
---

# Path Homotopy Invariants and their Application to Optimal Trajectory Planning

Subhrajit Bhattacharya

Robert Ghrist

Department of Mechanical Engineering

Department of Mathematics,

and Mechanics, Lehigh University, PA.

University of Pennsylvania, PA.

E-mail: sub216@lehigh.edu

E-mail: ghrist@math.upenn.edu

## Abstract

We consider the problem of optimal path planning in different homotopy classes in a given environment. Though important in robotics applications, path-planning with reasoning about homotopy classes of trajectories has typically focused on subsets of the Euclidean plane in the robotics literature. The problem of finding optimal trajectories in different homotopy classes in more general configuration spaces (or even characterizing the homotopy classes of such trajectories) can be difficult. In this paper we propose automated solutions to this problem in several general classes of configuration spaces by constructing presentations of fundamental groups and giving algorithms for solving the word problem in such groups. We present explicit results that apply to knot and link complements in 3-space, discuss how to extend to cylindrically-deleted coordination spaces of arbitrary dimension, and also present results in the coordination space of robots navigating on an Euclidean plane.

## 1 Introduction

In the context of robot motion planning, one often encounters problems requiring optimal trajectories (paths) in different homotopy classes. For example, consideration of homotopy classes is vital in planning trajectories for robot teams separating/caging and transporting objects using a flexible cable [Bhattacharya et al., 2015], or in planning optimal trajectories for robots that are tethered to a base using a fixed-length flexible cable [Kim et al., 2014], or in humanrobot collaborative exploration problems in context of search-and-rescue missions [Govindarajan et al., 2014]. This paper addresses the problem of optimal path planning with homotopy class as the optimization constraint.

There is, certainly, a large literature on minimal path-planning in computational geometry (for a brief sampling and overview, see [Mitchell and Sharir, 2004]). The topology of a configuration space plays a key role in solving path-planning problems. To that end, the study of the topological invariants of robot configuration spaces and the properties of motion planning problems in such configuration spaces is not new [Farber, 2001, Costa and Farber, 2010, Farber et al., 2006, Cohen and Pruidze, 2007]. However, most of this body of research has primarily focused on deduction of topological invariants of configuration/coordination spaces, addressed existence questions, have studied properties of the motion planning problem itself, but do not explicitly implement algorithms for finding optimal paths in configuration spaces of robots. Classification of paths based on homotopy has also been studied in the robotics literature in two-dimensional planar workspaces using geometric methods [Grigoriev and Slissenko, 1998, Hershberger and Snoeyink, 1991], probabilistic road-map construction [Schmitzberger et al., 2002] techniques and triangulationbased path planning [Demyen and Buro, 2006]. While in a planar configuration space such methods can be used for determining whether or not two trajectories belong to the same homotopy class, efficient planning for least cost trajectories with homotopy class constraints is difficult using such representations even in 2-dimensions. To that end in prior work we developed a graph search-based method for computing shortest paths in different homology classes in 2, 3 and higher dimensional Euclidean spaces with obstacles [Bhattacharya et al., 2012, 2013], and in different homotopy classes in planar configuration spaces with obstacles [Bhattacharya et al., 2015].

Of course, since the problem of computing shortest paths (even for a 3-d simply-connected polygonal domain) is NP-hard [Canny and Reif, 1987], we must restrict attention to subclasses of spaces, even when using homotopy path constraints. In particular, we construct a discrete graph representation of a configuration space and thus reduce the problem to shortest path computation on the graph. This representation, along with path homotopy invariants of the configuration space, allows us to compute shortest paths in different homotopy classes using graph search-based path planning algorithms.

This paper focuses on computation of optimal paths in different homotopy classes in two interesting and completely different types of configuration spaces: (1) knot and link complements in $3 \mathrm { - } \mathrm { d } ;$ and (2) cylindrically-deleted coordination spaces [Ghrist and LaValle, 2006]. Compared to our prior conference publication [Bhattacharya and Ghrist, 2015], in this paper we have (i) provided a rigorous Proposition on the presentation of the fundamental group of knot/link complements in 3-d and hence the justification behind the proposed homotopy invariants in such spaces, (ii) have provided an explicit presentation of the fundamental group of cylindrically deleted coordination space for robots navigating on a plane, and (iii) hence have demonstrated through simulation the problem of optimal path computation in different homotopy classes for three robots navigating on a simple planar domain.

## 2 Configuration Spaces with Free Fundamental Groups

## 2.1 Preliminaries

In this section we introduce a few fundamental definitions and concepts. Each definition is accompanied by a reference to a standard text on the subject, where the reader can find more details on these topics.

Homotopy Classes of Paths: Consider oriented/directed curves in a topological space, X. Two curves $\gamma _ { 1 } , \gamma _ { 2 } :$ $[ 0 , 1 ] \to X$ connecting the same start and end points, $q _ { s } , q _ { e } \in X$ , are called homotopic (or belonging to the same homotopy class) if one can be continuously deformed into the other without intersecting any obstacle $( i . e .$ . there exists a continuous map $\eta : [ 0 , 1 ] \times [ 0 , 1 ] \to X$ such that $\eta ( \alpha , 0 ) = \gamma _ { 1 } ( \alpha ) , \eta ( \alpha , 1 ) = \gamma _ { 2 } ( \alpha )$ ∀α $\in [ 0 , 1 ]$ , and $\eta ( 0 , \beta ) = q _ { s } , \eta ( 1 , \beta ) = q _ { e } \forall \beta \in [ 0 , 1 ]$ [Hatcher, 2001]). A set of all homotopically equivalent paths $( i . e .$ , homotopic paths) constitute a homotopy class. We denote the homotopy class of a path $\gamma \textbf { a } [ \gamma ]$

Fundamental Group: The fundamental group or the first homotopy group of a topological space, $X ,$ , is the set of all homotopy classes of oriented closed loops (paths with $q _ { s } = q _ { e } = : q _ { 0 } )$ in X with a group structure imposed on the set as follows: i. The identity element is the class of all loops that can be contracted/homotoped to the point $q _ { 0 } ;$ ii. The inverse of a homotopy class, [γ], is the homotopy class of loops constituting of the same loops as in $[ \gamma ]$ , but with reversed orientation, and is denoted as $[ - \gamma ] \ \mathbf { o r } \ [ \gamma ] ^ { - 1 }$ ; iii. The composition (group operation) of two classes $[ \gamma _ { 1 } ]$ and $[ \gamma _ { 2 } ]$ is the class of loops that are obtained by concatenating a curve in $[ \gamma _ { 1 } ]$ ] with a curve in $\left[ \gamma _ { 2 } \right] ( i . e .$ , it is the class of the loop $\gamma ( t ) = \left\{ \begin{array} { l l } { \gamma _ { 1 } ( 2 t ) , 0 \leq t < \frac { 1 } { 2 } } \\ { \gamma _ { 2 } ( 2 t - 1 ) , \frac { 1 } { 2 } \leq t \leq 1 } \end{array} \right. )$

Free Group and Free Product of Groups: A free group over a set of letters/symbols is the group whose elements consists of all words constructed out of the letters and their formal inverses, with identity element being the empty word, and the group operation being word concatenation (with any letter juxtaposed with its inverse reducing to the identity) [Scott and Scott, 1964]. Given two groups, G and $H _ { \cdot }$ , the free product of the groups is the group of words that can be constructed with all the elements of the groups as the letters. The free product is thus written as $G * H = \{ g _ { 1 } h _ { 1 } g _ { 2 } h _ { 2 } \cdot \cdot \cdot | g _ { i } \in G , h _ { i } \in H \}$

## 2.2 Motivation: Homotopy Invariant in $\left( \mathbb { R } ^ { 2 } - \mathcal { O } \right)$

We are interested in constructing computable homotopy invariants for trajectories in a configuration space that are amenable to graph search-based path planning. To that end there is a very simple construction for configuration spaces of the form $\mathbb { R } ^ { 2 } - \mathcal { O }$ (Euclidean plane punctured by obstacles) [Grigoriev and Slissenko, 1998, Hershberger and Snoeyink, 1991, Tovar et al., 2008, Bhattacharya et al., 2015, Kim et al., 2014]: We start by placing representative points, $\zeta _ { i }$ , inside the $i ^ { t h }$ connected component of the obstacles, $O _ { i } \subset \mathcal { O }$ . We then construct non-intersecting rays, $r _ { 1 } , r _ { 2 } , \cdots , r _ { m }$ , emanating from the representative points (this is always possible, for example, by choosing the rays to be parallel to each other). Now, given a curve γ in $\mathbb { R } ^ { 2 } - \mathcal { O }$ , we construct a word by tracing the curve, and every time we cross a ray $r _ { i }$ from its right to left, we insert the letter $^ { \bullet } { \boldsymbol { r } } _ { i } ^ { , \bullet }$ into the word, and every time we cross it from left to right, we insert a letter $^ { \ast } r _ { i } ^ { - 1 \ast }$ into the word, with consecutive $r _ { j }$ and $r _ { i } ^ { - 1 }$ canceling each other. The word thus constructed is written as $h ( \gamma )$ . For example, in Figure $1 ( \mathrm { a } ) , h ( \gamma ) = { ^ { \ast } r } _ { 1 } ^ { - 1 } r _ { 4 } r _ { 2 } ^ { - 1 } r _ { 4 } ^ { - 1 } r _ { 4 } r _ { 4 } ^ { - 1 } r _ { 6 } ^ { - 1 , \nu } = { ^ { \ast } r } _ { 1 } ^ { - 1 } r _ { 4 } r _ { 2 } ^ { - 1 } r _ { 4 } ^ { - 1 } r _ { 6 } ^ { - 1 , \nu }$ . This word, called the reduced word for the trajectory γ, is a complete homotopy invariant for trajectories connecting the same set of points. That $\mathrm { i s } , \gamma _ { 1 } , \gamma _ { 2 } : [ 0 , 1 ] \to ( \mathbb { R } ^ { 2 } - \mathcal { O } )$ , with $\gamma _ { i } ( 0 ) = q _ { s } , \gamma _ { i } ( 1 ) = q _ { e }$ are homotopic if and only if $h ( \gamma _ { 1 } ) = h ( \gamma _ { 2 } )$

![](Bhattacharya2017Path_figs/ffe50c0693332c87eca96637c9481fd69664739e8933196e7428135eebb66e96.jpg)  
Figure 1: Homotopy invariants of curves such as γ in $( \mathbb { R } ^ { 2 } - \mathcal { O } )$ are words constructed by tracing γ and inserting letters in the word for every crossing of the chosen oriented sub-manifolds, $U _ { i }$ (in red).

## 2.3 Words as Homotopy Invariants in Spaces with Free Fundamental Groups

In a more general setting the aforesaid construction can be generalized as follows:

Construction 1 Given a D-dimensional manifold (possibly with boundary), X, suppose $U _ { 1 } , U _ { 2 } , \cdots U _ { n }$ are $( D - 1 )$ dimensional orientable sub-manifolds (not necessarily smooth and possibly with boundaries) such that $\partial U _ { i } \subseteq \partial X$ Then, for any curve, γ (connecting fixed start and end points, $x _ { s } , x _ { e } \in X )$ , which is in general position (transverse) w.r.t. the $U _ { i } { ' } s ,$ one can construct a word by tracing the curve and inserting into the word a letter, $u _ { i } o r u _ { i } ^ { - 1 }$ , whenever the curve intersects $U _ { i }$ with a positive or negative orientation respectively.

The proposition below is a direct consequence of a simple version of the Van Kampen’s Theorem (of which several different generalizations are available in the literature).

Proposition 1 Words constructed as described in Construction 1 are complete homotopy invariants for curves in X joining the given start and end points if the following conditions hold:

$$
1. U _ {i} \cap U _ {j} = \emptyset , \forall i \neq j.
$$

2. $\textstyle X - \bigcup _ { i = 1 } ^ { n } U _ { i }$ is path connected and simply-connected, and,

$$
3. \pi_ {1} (X - \bigcup_ {i = 1, i \neq j} ^ {n} U _ {i}) \simeq \mathbb {Z}, \forall j = 1, 2, \dots , n,
$$

Proof. Consider the spaces $X _ { 0 } = X - \textstyle \bigcup _ { i = 1 } ^ { n } U _ { i }$ and $\begin{array} { r } { X _ { j } = X - \bigcup _ { i = 1 , i \ne i } ^ { n } U _ { i } , \ j = 1 , 2 , \cdot \cdot \cdot , n } \end{array}$ . Due to the aforesaid properties of the $U _ { i } { ^ { \star } } \mathrm { s }$ the set ${ \mathcal { C } } _ { X } = \{ X _ { 0 } , X _ { 1 } , \cdot \cdot \cdot , X _ { n } \}$ constitutes an open cover of $X ,$ is closed under intersection, the pairwise intersections $X _ { i } \cap X _ { j } = X _ { 0 } , i \neq j$ are simply-connected (and hence path connected), and so are $X _ { i } \cap X _ { j } \cap X _ { k } = X _ { 0 } , i \neq j \neq k$

The proof, when $\gamma$ is a closed loop $( i . e . \ x _ { s } = x _ { e } )$ , then follows directly from the Seifert-van Kampen theorem [Hatcher, 2001, Crowell, 1959] by observing that $\pi _ { 1 } ( X ) \simeq \pi _ { 1 } ( X _ { 0 } ) * \pi _ { 1 } ( X _ { 1 } ) * \pi _ { 1 } ( X _ { 2 } ) * \cdot \cdot \cdot *$ $\pi _ { 1 } ( X _ { n } ) \simeq * _ { i = 1 } ^ { n } \mathbb { Z } .$ , the free product of n copies of $\mathbb { Z } ,$ each $\mathbb { Z }$ generated due to the restriction of the curve ${ \mathrm { t o } X } _ { i } , i = 1 , 2 , \cdots , n$

When $\gamma _ { 1 }$ and $\gamma _ { 2 }$ are curves (not necessarily closed) joining points $x _ { s }$ and $x _ { e } .$ , they are in the same homotopy class iff $\gamma _ { 1 } \cup - \gamma _ { 2 }$ is null-homotopic — that is, $h ( \gamma _ { 1 } ) \circ h ( - \gamma _ { 2 } ) = \cdots \Leftrightarrow h ( \gamma _ { 1 } ) = h ( \gamma _ { 2 } )$ (where by $" _ { \bigcirc } \cdot \cdot$ we mean word concatenation).

The Construction 1 gives a presentation [Epstein, 1992] of the fundamental group of X (which, in this case, is a free group due to the Van Kampen’s theorem) as the group generated by the set of letters $\mathbf { U } = \{ u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot , u _ { q } \}$ , and is written as $G = \pi _ { 1 } ( X ) = < u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot , u _ { q } > = < \mathbf { U } >$ . In our earlier construction with the rays, $X = \mathbb { R } ^ { 2 } - \mathcal { O }$ was the configuration space, and $U _ { i } = X \cap r _ { i }$ were the support of the rays in the configuration space. It is easy to check that the conditions in the above proposition are satisfied with these choices. However such choices of rays is not the only possible construction of the $U _ { i } { ^ \mathrm { , } } \mathrm { s }$ satisfying the conditions of Proposition 1. Figure 1(b) shows a different choice of the $U _ { i } { ^ { \star } } \mathrm { s }$ that satisfy all the conditions.

![](Bhattacharya2017Path_figs/ef5ed83aead3da2836216841f37d153da3d7f2b63414f5f567abc12c1e0f01ba.jpg)  
(a) The surfaces, $U _ { i } { \ ' } { \bf s } ,$ satisfy the (b) With a genus-2 unknotted obstacle, one (c) When the obstacle is a trefoil knot, it’s not conditions of Proposition 1. h(γ) = can still find, U<sub>i</sub>’s satisfying the conditions possible to find $U _ { i }$ ’s satisfying the conditions of $^ { \ast } u _ { 2 } \ u _ { 1 } ^ { - 1 } u _ { 2 } ^ { , , }$ of Proposition 1. Proposition 1.  
Figure 2: The fundamental groups of configuration spaces, $\mathbb { R } ^ { 3 } - \mathcal { O }$ , may or may not be free.

## 2.4 Simple Extension to $( \mathbb { R } ^ { 3 } - \mathcal { O } )$ with Unlinked Unknotted Obstacles

The construction described in Section 2.2 can be easily extended to the 3-dimensional Euclidean space punctured by a finite number of un-knotted and un-linked toroidal (possibly of multi-genus) obstacles. Instead of $" \mathrm { { r a y s } } ^ { \prime \ }$ , in this case the $U _ { i } { ^ \mathrm { * } } { } $ are 2-dimensional sub-manifolds that satisfy the conditions in Proposition 1, with a letter, $u _ { i } ( \mathrm { o r } u _ { i } ^ { - 1 } )$ , being inserted in $h ( \gamma )$ every time the curve, $\gamma ,$ crosses/intersects a $U _ { i }$ . This is illustrated in Figures $2 ( \mathrm { a } )$ and 2(b).

However, a little investigation makes it obvious that such 2-dimensional sub-manifolds cannot always be constructed when the obstacle are knotted or linked (Figure 2(c)). One can indeed construct surfaces (e.g. Seifert surfaces) satisfying some of the properties, but not all.

## 2.5 Application to Graph Search-based Path Planning

Using the homotopy invariants described in the previous sub-section, we describe a graph construction for use in search-based path planning for computing optimal (in the graph) trajectories in different homotopy classes. Suppose $G = ( V , E )$ is a discrete graph representation of a configuration space, X. That is, V , is a set of points (vertices) sampled from X, and for any two neighboring points $x _ { 1 } , x _ { 2 } \in V$ (where neighbors are typically determined by a distance threshold), there exists an edge $( x _ { 1 } , x _ { 2 } ) \in E . ^ { 2 }$ We assume $x _ { s } \in V$

We first fix the set of sub-manifolds $\{ U _ { 1 } , U _ { 2 } , \cdots , U _ { n } \}$ as described earlier. Now, given a discrete graph representation of the configuration space, $G = ( V , E )$ , we construct an h-augmented graph, $G _ { h } = ( V _ { h } , E _ { h } )$ , which is essentially a lift of G into the universal covering space of X [Hatcher, 2001]. The construction of such augmented graphs has been described in our prior work [Bhattacharya et al., 2015, Kim et al., 2014, Govindarajan et al., 2014], and the explicit construction of $G _ { h }$ can be described as follows:

i. Vertices in $V _ { h }$ are tuples of the form $( x , w )$ , where $x \in V$ and w is a word made out of letters $u _ { i }$ and $u _ { i } ^ { - 1 }$ .

$$
\mathrm{ii.} (x _ {s}, \text {``}) \in V _ {h}
$$

iii. For every edge $[ x _ { 1 } , x _ { 2 } ] \in E$ and every vertex $( x _ { 1 } , w ) \in V _ { h }$ , there exists an edge $[ ( x _ { 1 } , w ) , ( x _ { 2 } , w o h ( \overrightarrow { x _ { 1 } x _ { 2 } ^ { \prime } } ) ) ] \in E _ { h }$ where $\overrightarrow { x _ { 1 } x _ { 2 } }$ denotes the directed curve that constitutes the edge $[ x _ { 1 } , x _ { 2 } ]$

![](Bhattacharya2017Path_figs/ff6bba28419ff534a1842d9f03d8ef8f5ed1cc39691fa5b0509884e6f38750ea.jpg)  
(a) The configuration space, X (light gray), and (b) The universal covering space, ${ \cal \widetilde X } ,$ and the vertex set, $V _ { h }$ . Note how the the vertex set, V (blue dots). trajectories lift to have different end points.

Figure 3: The h-augmented graph, $G _ { h } ,$ is a lift of G into $\widetilde { X }$ .  
![](Bhattacharya2017Path_figs/bb03c81058be28d750bd3ca742f43953775e391c7a619d9508ac27b92c30d69c.jpg)  
(a) 5 shortest trajectories in G (b) The trajectories after being (c) By setting $x _ { s } ~ = ~ x _ { e } ~ = ~ x _ { 0 } .$ , (d) Similar computation in $\mathbb { R } ^ { 3 } - \mathcal { O }$ belonging to different homotopy shortened, but belonging to same the same method can be used to find when its fundamental group is free. classes. (obstacles in gray) homotopy classes. shortest loops passing through x .  
Figure 4: Simple results in configuration spaces that have free fundamental groups. The dot/dash pattern and colors are shown to distinguishing between the trajectories.

iv. The length/cost of an edge in $G _ { h }$ is same as its projection in $\Im \colon C _ { G _ { h } } \left( [ ( x _ { 1 } , w _ { 1 } ) , ( x _ { 2 } , w _ { 2 } ) ] \right) = C _ { G } ( [ x _ { 1 } , x _ { 2 } ] ) .$

The item $\mathit { \Psi } _ { \mathrm { 1 . } } ^ { \bullet } \mathit { \Psi } _ { \mathrm { 1 . } } ^ { \bullet }$ is just a qualitative description of the vertices in $G _ { h }$ . Item $\because \mathrm { i i . } \ ' { }$ describes one particular vertex in $G _ { h }$ , and using that, item $\ddot { \cdot } _ { \mathrm { i i i . } } \dot { \cdot }$ ’ describes an incremental construction of the entire graph $G _ { h }$ . The topology of $G _ { h }$ can be described as a lift of G into the universal covering space, $\widetilde { X } .$ , of X, and is illustrated in Figure 3 for a uniform cylindrically discretized space with a single disk-shaped obstacle.

Such an incremental construction is well-suited for use in graph search algorithms such as Dijkstra’s or $\mathbf { A } ^ { * }$ [Cormen et al., 2001], in which one initiates an open set using the start vertex (in item ii.), and then gradually expands vertices, generating only the neighbors at every expansion (the recipe for which is given by item ‘iii.’). Executing a search (Dijkstra’s/A\*) in $G _ { h }$ from $( x _ { s } , \cdots \ r )$ to vertices of the form $( x _ { e } , * )$ (where $\cdot _ { * } ,$ denotes any word), and projecting it back to $G ,$ gives us optimal trajectories in G that belong to different homotopy classes. Figure 4(a) shows 5 such optimal trajectories in the graph, connecting a given start and goal vertex, where $G$ was constructed by an uniform hexagonal discretization of the planar configuration space. One can then employ a simple curve shortening algorithm [Kim et al., 2014] to obtain ones more optimal than the ones restricted to G (Figure 4(b)). Similarly, shortest trajectories connecting $x _ { s }$ and $x _ { e }$ can be obtained in 3-dimensional configuration spaces with free fundamental group (e.g., Figure 4(d), showing 4 paths connecting two fixed points in $\mathbb { R } ^ { 3 }$ with two un-linked toroidal obstacles).

![](Bhattacharya2017Path_figs/96c2335f6118e5056514187ea7f27306aa7a71764c14b725d565771d56ad39f5.jpg)  
(a) Knot diagram, showing one of the poly- (b) The surfaces, U<sub>i</sub>, shown in different colors. The closed loop γ is null-homotopuc, but gons, Q<sub>3</sub> (in cyan). $\overset { \cdot } { h } ( \gamma ) = \overset { \cdot \cdot } { \cdots } u _ { 1 } ^ { - 1 } u _ { 2 } ^ { \cdot } u _ { 3 } ^ { - 1 } ,$ . Top and side views.

Figure 5: Constructing the surfaces, $U _ { i } .$ from polygonal knot/link diagrams (polygon segments shown as thickened cylinders for easy visualization). Null-homotopic loops as $\gamma$ have non-empty words.

## 3 Knot and Link Complements

As described earlier, when the obstacle set in $\mathbb { R } ^ { 3 }$ consists of knots and links, it is in general not possible to find the sub-manifolds $U _ { i } \subset ( \mathbb { R } ^ { 3 } - \mathcal { O } )$ as required by Proposition 1. However, thankfully we have more generalized versions of the Van Kampen theorem at our disposal that lets us extend the proposed methodology to such spaces. We first illustrate the generalization in $\mathbb { R } ^ { 3 } - \mathcal { O }$ using knot/link diagrams.

## 3.1 Dehn Presentation of Fundamental Group of Knot/Link Complements

For simplicity we consider knots and links in $\mathbb { R } ^ { 3 }$ as obstacles. We assume that the knots/links are described by polygons, all of which together constitute $O \subset \mathbb { R } ^ { 3 }$ . The thickened obstacles (the knots/links with the tubular neighborhoods) will be referred to as O. We consider a knot/link diagram [Lickorish, 1997] of the obstacles: Given a projection map, $p : \mathbb { R } ^ { 3 }  \mathbb { R } ^ { 2 }$ , the knot/link diagram is the projection of the knot/link, $p ( O )$ , along with additional information about the $z { \mathrm { - } } o r d e r i n g$ at the self-intersections of $p ( O )$ . We assume that in this diagram the self-intersections are all transverse (which can always be achieved through infinitesimal perturbations) and that the diagram divides the plane into simply-connected regions (say $q$ counts of them) each bounded by segments of the projected obstacles, and one unbounded exterior region. The boundary (the boundary of the closure) of each of the bounded regions is itself a polygon, $Q _ { i } \subseteq p ( O ) , i = 1 , 2 , \cdot \cdot \cdot , q$ (Figure 5(a)). Clearly $p ^ { - 1 } ( Q _ { i } ) \cap O$ (the preimage of $Q _ { i }$ in the original obstacle) will be a discontinuous polygon, with discontinuities at the preimages of the self-intersection points on the knot diagram. But these discontinuities can be removed simply by “connecting” the preimages at each self-intersection point, resulting into a spatial polygon, $\widetilde { Q } _ { i }$ with the property that $p ( \widetilde { Q } _ { i } ) = Q _ { i }$ . A simple triangulation can then be employed to construct a surface, $U _ { i } .$ , in $\mathbb { R } ^ { 3 } - O$ , such that its boundary is $Q _ { i }$ and $p ( U _ { i } )$ is the simply-connected region bounded by $Q _ { i }$ (this can be achieved by first triangulating the planar region, $p ( U _ { i } )$ ), and then lifting the triangulation to $\mathbb { R } ^ { 3 } ) \mathrm { - }$ see Figure 5(a).

The $U _ { i } { ^ { \star } } \mathbf { s }$ thus constructed satisfy properties (2) and (3) of Proposition 1, but not property (1), nor do they satisfy the property $\partial U _ { i } \subseteq \partial X$ . The consequence of this is that near the regions where the $U _ { i } { ^ { \star } } \mathbf { s }$ intersect, there can be closed loops in $\mathbb { R } ^ { 3 } - O$ which are null-homotopic, but words constructed simply by tracing the loop and inserting letters corresponding to intersections with the $U _ { i } { } ^ { \prime } \mathbf { s } ,$ as we did earlier, may not be the empty word (identity element). An example is illustrated in Figure 5(b)). Due to our construction, such intersection of the $U _ { i } { ^ \mathrm { * } } { }$ happen only along lines passing through the pre-image of the self-intersections in the knot diagram, for each of which we end up getting a null-homotopic closed loop with non-empty word.

The Dehn presentation [Weinbaum, 1971] uses surfaces as constructed to describe the fundamental group of knot/link complements. We consider the free group, $G = < u _ { 1 } , u _ { 2 } , \cdot \cdot \cdot , u _ { q } > = < \mathbf { U } >$ . In general, for every selfintersection in the knot/link diagram, there are four adjacent surfaces, $U _ { i _ { 1 } } , U _ { i _ { 2 } } , U _ { i _ { 3 } }$ and $U _ { i _ { 4 } }$ in the order as shown in Figure 6 (when the self-intersection is adjacent to the unbounded region in the knot diagram, there are only three). Correspondingly, there is a closed null-homotopic loop, $\gamma _ { i } .$ , that has a word $\rho _ { i } = { \mathrm { { } } ^ { \ast } } u _ { i _ { 1 } } u _ { i _ { 2 } } ^ { - 1 } u _ { i _ { 3 } } u _ { i _ { 4 } } ^ { - 1 , \ast }$ . Thus we have such words $\rho _ { 1 } , \rho _ { 2 } , \cdots , \rho _ { m }$ (assuming there are m counts of self-intersections) that represent null-homotopic loops.

![](Bhattacharya2017Path_figs/da6252b72f67e07454cd19c65ee5413de4268a31397f9e7d58be1155f71dd109.jpg)

Figure 6: A “self-intersection” in a knot/link diagram, with a null-homotopic loop, $\gamma _ { i } ,$ intersecting the surfaces adjacent to the intersection. $h ( \gamma _ { i } ) = { } ^ { \mathfrak { C } } u _ { i _ { 1 } } u _ { i _ { 2 } } ^ { - 1 } u _ { i _ { 3 } } u _ { i _ { 4 } } ^ { - 1 , \ \mathrm { { , } } }$ . One or more of the surfaces can be non-existent, in which case the corresponding letters are simply absent from the word. These words constitute $\mathbf { R } ,$ , and should map to the identity element in $\pi _ { 1 } ( X ) = < \mathbf { U } \mid \mathbf { R } >$

These words are called relations and we call the set $\mathbf { R } = \{ \rho _ { 1 } , \rho _ { 2 } , \cdot \cdot \cdot , \rho _ { m } \}$ the relation set. It can be easily noted that inverses and cyclic permutations of each $\rho _ { i }$ also corresponds to null-homotopic loops. We thus define the symmetricized relation set, R, as the set containing all the words in $\mathbf { R } ,$ , all their inverses, and all cyclic permutation of each of those.

Let the normal subgroup of G generated by R be $N = \{ { } ^ { \ast \ast } \alpha _ { 1 } \rho _ { i _ { 1 } } \alpha _ { 1 } ^ { - 1 } \alpha _ { 2 } \rho _ { i _ { 2 } } \alpha _ { 2 } ^ { - 1 } \cdot \cdot$

$\alpha _ { \kappa } ^ { - 1 } \alpha _ { \kappa } \rho _ { i _ { \kappa } } \cdot \cdot \cdot ^ { , \cdot , } | \alpha _ { k } \in G , \rho _ { i _ { k } } \in \overline { { \mathbf { R } } } \} = < \overline { { \mathbf { R } } } ^ { G } >$ (normal closure of R in $G )$ . It is easy to observe that a closed loop, $\gamma ,$ in $X = \mathbb { R } ^ { 3 } - \mathcal { O }$ , has a word that is an element of N iff it is null-homotopic. Due to a more general version of the Van Kampen’s theorem [Hatcher, 2001], the fundamental group of X is the quotient group, $\pi _ { 1 } ( X ) = G / N = < \mathbf { U } \mid \mathbf { R } >$ — the group in which, under the quotient map, elements of N are mapped to the identity element. This is summarized and generalized in the following proposition.

Proposition 2 Given a D-dimensional manifold (possibly with boundary), X, suppose $U _ { 1 } , U _ { 2 } , \cdots U _ { n }$ are $\partial U _ { i } \subseteq \partial X$ $( D - 1 )$ )-<sub>∪</sub> $\textstyle \bigcup _ { j \neq i } U _ { j }$ and

$1 . a )$ The intersections $o f U _ { i }$ and $U _ { j } ,$ , if non-empty, are transverse (hence (D − 2)-dimensional),

$$
b) \bigcap_ {i = 1} ^ {n} U _ {i} = \emptyset ,
$$

2. $\textstyle X - \bigcup _ { i = 1 } ^ { n } U _ { i }$ is path connected and simply-connected, and,

$$
3. \pi_ {1} (X - \bigcup_ {i = 1, i \neq j} ^ {n} U _ {i}) \simeq \mathbb {Z}, \forall j = 1, 2, \dots , n,
$$

For a loop in $X ,$ as before, one can construct a word as described in Construction 1. Let the set of all the letters constituting such words be U.

For every $\left( D - 2 \right)$ -dimensional intersection of the $U _ { i } \cap U _ { j } , i \neq j ,$ , one can construct a loop in the tubular neighborhood of $U _ { i } \cap U _ { j }$ in X that links with $U _ { i } \cap U _ { j }$ . Let the set of words corresponding to such loops be R.

Then the fundamental group of X is isomorphic to $< \mathbf { U } \mid \mathbf { R } >$

## 3.2 The Word Problem and Dehn Algorithm

Due to the discussion above, two trajectories, $\gamma _ { 1 } , \gamma _ { 2 } .$ , connecting $x _ { s }$ and $x _ { e }$ in the knot/link complement, $X ,$ , belong to the same homotopy class iff the word $h ( \gamma _ { 1 } \cup - \gamma _ { 2 } ) = h ( \gamma _ { 1 } ) \circ h ( \gamma _ { 2 } ) ^ { - 1 }$ belongs to $N = < \overline { { \mathbf { R } } } ^ { G } >$ . This problem in group theory is known as the word problem [Epstein, 1992], and there are various algorithms, each suitable for specific types of groups, for solving the word problem. We, in particular, will focus on a very simple algorithm due to Max Dehn [Lyndon and Schupp, 2001, Greendlinger and Greendlinger, 1986], which is applicable to a wide class of groups and their presentations.

Dehn’s metric algorithm: Given a presentation of a group, $\pi _ { 1 } = < \textbf { U } | \textbf { R } >$ , we construct the symmetricized relation set R as described earlier. Given a cyclically reduced word, w, made up of letters (and their inverses) from

U, one checks for every element $\boldsymbol { \rho } \in \overline { { \mathbf { R } } }$ if w and $\rho$ share a common sub-words that is of length greater than $| \rho | / 2$ $( | \rho |$ being the length of $\rho )$ . If they do (say, $\rho = \alpha \beta \gamma$ , with β being a sub-word appearing in w, and $| \beta | > | \rho | / 2 )$ , we replace the sub-word with the shorter equivalent that one obtains by setting $\rho$ to the identity element (i.e., replace β by $\alpha ^ { - 1 } \gamma ^ { - 1 }$ in w). This process is repeated, and the algorithm terminates when no more such sub-words are found. The final word at which the algorithm terminates indicates if the initial word, $w ,$ is in N (whether it maps to the identity element in $\pi _ { 1 } )$ .

This algorithm can be used in conjunction with search in $G _ { h }$ as before for finding optimal trajectories in different homotopy classes, with two vertices $( x , w _ { 1 } ) , ( x , w _ { 2 } ) \in V _ { h }$ being the same iff $h ( w _ { 1 } ) \circ h ( - w _ { 2 } )$ reduces to the empty word upon applying the Dehn’s metric algorithm

## 3.3 Guarantees of Dehn Algorithm

It’s well known [Greendlinger and Greendlinger, 1986] that if Dehn algorithm terminates at the empty word, then $w \in N$ . However, the converse is not necessarily true. One can derive several sufficient (and often highly restrictive) conditions on the presentation $< \mathbf { U } \mid \mathbf { R } >$ under which the converse holds [Lyndon and Schupp, 2001]. If, for a given presentation of a group the converse holds, we say that Dehn algorithm is complete for that presentation (or that the presentation is complete with respect to the Dehn algorithm, or that the word problem is solvable using the specific presentation and Dehn algorithm).

Due to the result of [Weinbaum, 1971], the Dehn presentation of the fundamental groups of the complement of a tame, alternating, prime knot is complete with respect to the Dehn algorithm. It is also known [Epstein, 1992] that automatic groups (including hyperbolic groups) have presentations that are complete with respect to Dehn algorithm.

## 4 Cylindrically-deleted Configuration Spaces

The previous results are limited to 3-dimensional spaces: one suspects that higher dimensions are more difficult. However, there are some classes of spaces for which optimal path-planning with homotopy constraints is still computable via a Dehn algorithm, independent of dimension. The following class of examples is inspired by robot coordination problems, in which individual agents with predetermined motion paths have to coordinate their motions so as to avoid collision.

Consider a collection of n graphs $( \Gamma _ { i } ) _ { 1 } ^ { n }$ , each embedded in a common workspace (usually $\mathbb { R } ^ { 2 } \ o \mathbf { r } \mathbb { R } ^ { 3 } )$ with intersections permitted. In the simplest case, each $\Gamma _ { i }$ will be homeomorphic to a closed interval, but more general graphs are permitted, such as roadmap approximations to a configuration space. On each $\Gamma _ { i } ,$ a robot $R _ { i }$ with some particular fixed size/shape is free to move. Such motion may be Euclidean (by translation/rotation); more general motions are possible, so long as the region occupied by the robot $R _ { i }$ in the workspace is purely a function of location on $\Gamma _ { i } . \mathrm { ~ A ~ }$ point in the product space $\Pi _ { i } \Gamma _ { i }$ determines the locations of the n robots in the common workspace. Certain configurations are illegal, due to collisions. For example, if the robots are point-like, and each $\Gamma _ { i } = \Gamma$ is identical, then the configuration space of n points on $\Gamma$ is the cross product $\Pi _ { i } \Gamma _ { i }$ minus the pairwise diagonal $\Delta$ . If the robots are given finite extent, then this system has a configuration space obtained by the graph product $\Pi _ { i } \Gamma _ { i }$ minus an -neighborhood of the pairwise diagonal. However, more general types of collisions can be defined, say, if the robots are irregularly shaped and the graphs $\Gamma _ { i }$ are all different. In this most general case, the natural analogue of a configuration space is the coordination spaces of [Ghrist and LaValle, 2006].

The coordination space of this system is defined to be the space of all configurations in $\Pi _ { i } \Gamma _ { i }$ for which there are no collisions – the geometric robots $R _ { i }$ have no overlaps in the workspace. Under the assumption that collisions between robots are pairwise-defined, the coordination space is cylindrically deleted and of the form

$$
X = \left(\prod_ {i = 1} ^ {n} \Gamma_ {i}\right) - \mathcal {O} \quad \text { where } \quad \mathcal {O} = \bigcup_ {i <   j} \left\{(x _ {k}) _ {1} ^ {N} \in \prod_ {k = 1} ^ {N} \Gamma_ {k}: (x _ {i}, x _ {j}) \in \Delta_ {i, j} \right\},
$$

for some (open, “collision”) sets $\Delta _ { i , j } \subset \Gamma _ { i } \times \Gamma _ { j }$ where $1 \leq i < j \leq N$ . In what follows, we assume that the $\Delta _ { i , j }$ are sufficiently tame (e.g., semialgebraic) so as to avoid issues of non-finitely-generated $\pi _ { 1 }$ . Given (internal, path-) metrics on each $\Gamma _ { i }$ , the coordination space X inherits a locally-Euclidean metric on products of edges in the graphs. Such X are complete path-spaces and thus the problem of geodesics is well-posed. Their fundamental groups can be (highly) nontrivial, depending on the obstacle set O. However, finding optimal paths subject to homotopy classes is still computable. To that end one can construct the subspaces $U _ { i } \subset X$ of co-dimension 1, and the relation set $\mathbf { R } ,$ and use them to design complete homotopy invariants as before. We do not discuss the explicit construction of the $U _ { i } { ^ { \star } } \mathrm { s }$ for cylindrically-deleted coordination spaces in this paper, but provide the following theorem on solvability of the word problem in such spaces.

## Theorem 1 Any compact cylindrically-deleted coordination space X admits a Dehn algorithm for $\pi _ { 1 }$

Proof. Any such X is realized as a Hausdorff limit of cubcial complexes which were shown in [Ghrist and LaValle, 2006, Thm 4.4] to be nonpositively-curved and to stabilize in $\pi _ { 1 }$ by tameness. All nonpositivelycurved piecewise-Euclidean cube complexes have fundamental groups which are, by a famous result of Niblo-Reeves [Niblo and Reeves, 1998], biautomatic. Biautomatic groups all admit a Dehn algorithm (specifically, there is a quadratic isoperimetric inequality) [Epstein, 1992].

It is worth noting that \`<sub>2</sub>-shortest paths are perhaps not the most natural optimization for coordination spaces. It would be interesting to consider other $( \ell _ { 1 } , \ell _ { \infty } )$ pointwise norms.

In the next section we consider point robots navigating on a plane. The configuration space of each robot is the Euclidean plane. For such a configuration space for the individual robots, the result of Theorem 1 may not hold, since the fundamental group of the coordination space may not be biautomatic. Nevertheless, we can construct a presentation of the fundamental group, which we do, and still apply Dehn metric algorithm to it, although the Dehn algorithm may not be complete for the proposed presentation.

## 4.1 Presentation of the Fundamental Group of a Cylindrically Deleted Coordination Space for Point Robots Navigating on a Plane

We consider point robots navigating on a plane. Thus, in this case $\Gamma _ { i } ,$ the configuration space of the $i ^ { t h }$ robot, is the Euclidean plane coordinatized by $( x _ { i } , y _ { i } )$ . A collision set $\Delta _ { i , j } = \{ ( x _ { i } , y _ { i } , x _ { j } , y _ { j } ) \mid x _ { i } = x _ { j } , y _ { i } = y _ { j } \} \subset \Gamma _ { i } \times \Gamma _ { j } \simeq$ $\mathbb { R } ^ { 4 } , \ 1 \le i < j \le N$ , is a 2-dimensional hyperplane embedded in the joint configuration space of the robots i and $j .$

The joint configuration space of $N$ robots (with the collision sets included) is $\begin{array} { r } { \bar { \Gamma } = \prod _ { k = 1 } ^ { N } \Gamma _ { k } \simeq \mathbb { R } ^ { 2 N } } \end{array}$ . The “cylindrical” obstacles in this configuration space created due to $\Delta _ { i , j }$ are thus

$$
\mathcal {O} _ {i, j} = \Delta_ {i, j} \times \left(\prod_ {k \neq i, j} \Gamma_ {k}\right) = \left\{\left(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}\right) \mid x _ {i} = x _ {j}, y _ {i} = y _ {j} \right\} \subset \overline {{\Gamma}},
$$

which are co-dimension 2 subspaces (hyperplanes) embedded in the 2N dimensional joint configuration space. Thus the coordination space is $\begin{array} { r } { X = \overline { { \Gamma } } - \bigcup _ { 1 < i < j < N } \mathcal { O } _ { i , j } } \end{array}$

## 4.1.1 Design of co-dimension 1 manifolds, $U _ { * }$ <sub>∗</sub>:

As before, we are interested in constructing a set of $( 2 N - 1 )$ )-dimensional sub-manifolds, $\{ U _ { \alpha } \}$ , in X such that removing all but one of these sub-manifolds will give us a space with fundamental group isomorphic to $\mathbb { Z } .$ . This would let us apply the generalized Van Kampen theorem as before by allowing us to construct words based on transverse intersection of paths with the surfaces, $U ,$ <sub>∗</sub> (which would be of co-dimension 1 in $X )$ . We outline a general construction, and then show how that can be specialized for $N = 3$

Consider a single $( 2 N - 2 )$ -dimensional obstacle $\mathcal { O } _ { i , j }$ , which is a hyperplane of co-dimension 2 in ${ \overline { { \Gamma } } } .$ . Thus the homotopy group of $Y _ { i , j } = \overline { { \Gamma } } - \mathcal { O } _ { i , j }$ is isomorphic to $\mathbb { Z }$ and is generated by a 1-dimensional loop that links with $\mathcal { O } _ { i , j }$ in this space. Our first construction corresponding to the obstacle $\mathcal { O } _ { i , j }$ is thus the following half-space:

$$
\mathcal {U} _ {i, j} = \left\{\left(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}\right) \mid x _ {i} = x _ {j}, y _ {i} <   y _ {j} \right\}
$$

This a $( 2 N - 1 )$ -dimensional (co-dimension 1 in Γ) half-hyperplane with $\mathcal { O } _ { i , j }$ at its boundary. However, for another pair of indices, $( i ^ { \prime } , j ^ { \prime } ) , 1 \le i ^ { \prime } < j ^ { \prime } \le N$ , the obstacle $\mathcal { O } _ { i ^ { \prime } , j ^ { \prime } }$ in general intersects $\mathcal { U } _ { i , j }$ in $\textbf { a } ( 2 N - 3 )$ -dimensional half-hyperplane, and the space $\mathcal { U } _ { i , j }$ intersects $\mathcal { U } _ { i , j }$ in a $( 2 N - 2 )$ -dimensional half-hyperplane. In particular,

$$
\mathcal {U} _ {i, j} \cap \mathcal {O} _ {i ^ {\prime}, j ^ {\prime}} = \left\{\left(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}\right) \mid x _ {i} = x _ {j}, x _ {i ^ {\prime}} = x _ {j ^ {\prime}}, y _ {i} <   y _ {j}, y _ {i ^ {\prime}} = y _ {j ^ {\prime}} \right\}
$$

is of co-dimension 2 in $\mathcal { U } _ { i , j }$ , and,

$$
\mathcal {U} _ {i, j} \cap \mathcal {U} _ {i ^ {\prime}, j ^ {\prime}} = \left\{\left(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}\right) \mid x _ {i} = x _ {j}, x _ {i ^ {\prime}} = x _ {j ^ {\prime}}, y _ {i} <   y _ {j}, y _ {i ^ {\prime}} <   y _ {j ^ {\prime}} \right\}
$$

is of co-dimension 1 in $\mathcal { U } _ { i , j }$ (a half-hyperplane) and is non-empty. This is schematically shown in Figure $\mathrm { 7 ( a ) }$

Lemma 1 $\begin{array} { r } { X - \bigcup _ { 1 \leq i < j \leq N } \mathcal { U } _ { i , j } \ = \ \overline { { \Gamma } } - \bigcup _ { 1 \leq i < j \leq N } \mathcal { O } _ { i , j } - \bigcup _ { 1 \leq i < j \leq N } \mathcal { U } _ { i , j } } \end{array}$ is path connected.

Sketch of proof. Suppose $\mathbf { p } ^ { 0 } = ( x _ { 1 } ^ { 0 } , y _ { 1 } ^ { 0 } , x _ { 2 } ^ { 0 } , y _ { 2 } ^ { 0 } , \cdots , x _ { N } ^ { 0 } , y _ { N } ^ { 0 } ) , \mathbf { p } ^ { 1 } = ( x _ { 1 } ^ { 1 } , y _ { 1 } ^ { 1 } , x _ { 2 } ^ { 1 } , y _ { 2 } ^ { 1 } , \cdots , x _ { N } ^ { 1 } , y _ { N } ^ { 1 } ) \in X .$ $\mathrm { I f ~ } x _ { i } ^ { 0 } < x _ { j } ^ { 0 }$ , but $x _ { i } ^ { 1 } \geq x _ { i } ^ { 1 }$ , then whichever path, $t \mapsto \mathbf { p } ^ { t } , ~ t \in [ 0 , 1 ]$ , is chosen to connect $ { \mathbf { p } } ^ { 0 }$ and $\mathbf { p } ^ { 1 }$ , there will be $\mathrm { ~ a ~ } \tau$ for which $x _ { i } ^ { \tau } = x _ { j } ^ { \tau }$ . However, if at this point, if $y _ { i } ^ { \tau } \leq y _ { i } ^ { \tau }$ , then the path will be intersecting $\mathcal { O } _ { i , j }$ or $\mathcal { U } _ { i , j }$ . Clearly, this can be prevented by simply altering the $y _ { i } ^ { t }$ and $y _ { j } ^ { t }$ in a small neighborhood of $t = \tau$ , without altering any other coordinate and hence the alteration itself not leading to intersection with any other $\mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$ . Thus an arbitrary pair of points in X an be connected using a path that does not intersect any of the $\mathcal { U } _ { i , j } { ' } \mathrm { s }$

Lemma 2 Any loop in Γ linked only with $\mathcal { O } _ { i , j }$ can be homotoped into any other loop linked only with $\mathcal { O } _ { i , j }$ , through a sequence of loops linked to $\mathcal { O } _ { i , j }$

i. without intersecting $\mathcal { O } _ { i ^ { \prime } , j ^ { \prime } }$

ii. not without intersecting $\mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$ if either $\scriptstyle i = i ^ { \prime } , j ^ { \prime } < j o r i < i ^ { \prime } , j = j ^ { \prime }$ , otherwise without intersecting $\mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$

Sketch of proof. The proof is based on being able to construct, or an obstruction to constructing, a homotopy satisfying certain properties between small loops (in a tubular neighborhood of $\mathcal { O } _ { i , j } )$ lying in a plane transverse to $\mathcal { O } _ { i , j }$ and linking to it.

Case I: Distinct $i , j , i ^ { \prime }$ and $j ^ { \prime } .$ :

We first consider the case when $i , j , i ^ { \prime }$ and $j ^ { \prime }$ are all distinct. Consider a 2-dimensional affine plane transverse to $\mathcal { O } _ { i , j }$ described by $\mathscr { P } _ { i , j } ( c _ { * } , d _ { * } ) = \{ ( x _ { 1 } , y _ { 1 } , x _ { 2 } , y _ { 2 } , \cdot \cdot \cdot , x _ { N } , y _ { N } ) \ : | \ : x _ { i } + x _ { j } = c _ { i j } , y _ { i } + y _ { j } =$ $d _ { i j } , x _ { k } = c _ { k } , y _ { k } = d _ { k } , \forall k \neq i , j \}$ (where $c _ { * }$ and $d _ { * }$ refers to the set of parameters describing the plane), and coordinatized by $X _ { i j } = x _ { i } - x _ { j }$ and $Y _ { i j } = y _ { i } - y _ { j }$ (so that $\mathcal { O } _ { i , j }$ intersects the plane at its origin).

The intersection of this plane with $\mathcal { O } _ { i ^ { \prime } , j ^ { \prime } }$ is, in general, empty except for carefully chosen values for the parameters (in particular, for parameters such that $c _ { i ^ { \prime } } = c _ { j ^ { \prime } } , d _ { i ^ { \prime } } = d _ { j ^ { \prime } } )$ , when they intersect over the entire $\mathcal { P } _ { i , j } ( c _ { * } , d _ { * } )$ . Likewise, the intersection of this plane with $\mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$ is, in general, empty except when the parameters are such tha $c _ { i ^ { \prime } } = c _ { j ^ { \prime } } , d _ { i ^ { \prime } } < d _ { j ^ { \prime } } )$ , when, again, they intersect at the entire $\mathcal { P } _ { i , j } ( c _ { * } , d _ { * } )$

Given two such affine planes, $\mathcal { P } _ { i , j } ( c _ { * } ^ { 0 } , d _ { * } ^ { 0 } )$ and $\mathcal { P } _ { i , j } ( c _ { * } ^ { 1 } , d _ { * } ^ { 1 } )$ , for two different sets of parameters, one can easily choose a path, $t \mapsto ( c _ { * } ^ { t } , d _ { * } ^ { t } ) , \ t \in [ 0 , 1 ]$ , through the parameter space avoiding $c _ { i ^ { \prime } } ^ { t } = c _ { j ^ { \prime } } ^ { t } , d _ { i ^ { \prime } } ^ { t } = d _ { j } ^ { t }$ simultaneously at any t. This gives a homotopy for a loop in $\mathcal { P } _ { i , j } ( c _ { * } ^ { 0 } , d _ { * } ^ { 0 } )$ around the origin (linking $\mathrm { w i t h } { \mathcal { O } } _ { i , j } )$ to a loop in $\mathcal { P } _ { i , j } ( c _ { * } ^ { 1 } , d _ { * } ^ { 1 } )$ around the origin, without intersecting $\mathcal { O } _ { i ^ { \prime } , j ^ { \prime } }$

Similarly, it is possible to choose the path such that $c _ { i ^ { \prime } } ^ { t } = c _ { j } ^ { t } .$ <sub>0</sub> and $d _ { i ^ { \prime } } ^ { t } < d _ { j } ^ { t }$ <sub>0</sub> does not happen simultaneously.

Case $I I \colon i , j , i ^ { \prime }$ and $j ^ { \prime }$ not all distinct:

Next consider the case when $i , j , i ^ { \prime } , j ^ { \prime }$ are not distinct. Choose $1 \leq m < n < p \leq N$ to be the nondistinct indices such that either $\scriptstyle i = i ^ { \prime } = m < j ^ { \prime } = n < j = p $ , or $\ i = m < i ^ { \prime } = n < j = j ^ { \prime } = p$ . Then the possible obstacles are $\mathcal { O } _ { m , n } , \mathcal { O } _ { n , p }$ and $\mathcal { O } _ { m , p } .$ with the indices of any pair of obstacle not all distinct.

Consider the plane $\mathcal { P } _ { m , n } ( c _ { * } , d _ { * } )$ , on which $x _ { m } + x _ { n } = c _ { m n } , y _ { m } + y _ { n } = d _ { m n }$ and $x _ { p } = c _ { p } , y _ { p } =$ $d _ { p }$ . This intersects obstacle ${ \mathcal { O } } _ { n , p }$ at points where $x _ { n } = x _ { p } = c _ { p }$ and $y _ { n } ~ = ~ y _ { p } ~ = ~ d _ { p }$ This gives $x _ { m } = c _ { m n } - c _ { p } , y _ { m } = d _ { m n } - d _ { p } .$ Thus, on the plane, the coordinates of the intersection point are $X _ { m n } = c _ { m n } - 2 c _ { p } , Y _ { m n } = d _ { m n } - 2 d _ { p }$ . Once again, it is possible to choose the path $( c _ { * } ^ { t } , d _ { * } ^ { t } )$ from $\left( c _ { \ast } ^ { 0 } , d _ { \ast } ^ { 0 } \right) \mathrm { t o } \left( c _ { \ast } ^ { 1 } , d _ { \ast } ^ { 1 } \right)$ such that $c _ { m n } ^ { t } - 2 c _ { p } ^ { t }$ and $d _ { m n } ^ { t } - 2 d _ { p } ^ { t }$ are not simultaneously zero for any $t \in [ 0 , 1 ]$ This argument also holds for the other two pairs of obstacles.

Again, using the chosen coordinates on $\mathcal { P } _ { m , n } ( c _ { * } , d _ { * } ) , \mathcal { P } _ { m , n } ( c _ { * } , d _ { * } )$ intersects $\mathcal { U } _ { n , p }$ at the ray $X _ { m n } ~ =$ $c _ { m n } - 2 c _ { p } , Y _ { m n } > d _ { m n } - 2 d _ { p }$ , and intersects $\mathcal { U } _ { m , p }$ at the ray $X _ { m n } = c _ { m n } - 2 c _ { p } , Y _ { m n } < - ( d _ { m n } - 2 d _ { p } )$ Because the rays point in opposite directions along the $X _ { m n }$ axis, given the parameters $( c _ { * } ^ { 0 } , d _ { * } ^ { 0 } )$ and $( c _ { * } ^ { 1 } , d _ { * } ^ { 1 } )$ , it is always possible to find the path $( c _ { * } ^ { t } , d _ { * } ^ { t } )$ (in particular, $d _ { p } ^ { t } )$ such that the rays of intersection with $\mathcal { U } _ { n , p }$ and $\mathcal { U } _ { m , p }$ on $\mathcal { P } _ { m , n } ( c _ { * } ^ { t } , d _ { * } ^ { t } )$ does not pass through the origin (if $c _ { m n } ^ { 0 } - 2 c _ { p } ^ { 0 }$ and $c _ { m n } ^ { 1 } - 2 c _ { p } ^ { 1 }$ are of opposite signs, and if $c _ { m n } ^ { \tau } - 2 c _ { p } ^ { \tau } = 0$ for some $\tau \in [ 0 , 1 ]$ , this can be achieved by choosing $d _ { m n } ^ { \tau } - 2 \dot { d } _ { p } ^ { \tau } > 0 )$ Similar argument holds for intersection of $\mathcal { P } _ { n , p } ( c _ { * } , d _ { * } )$ with $\mathcal { U } _ { m , n }$ and $\mathcal { U } _ { m , p } .$

However, $\mathcal { P } _ { m , p } ( c _ { * } , d _ { * } )$ intersects $\mathcal { U } _ { m , n }$ at the ray $X _ { m p } = 2 c _ { n } - c _ { m p } , Y _ { m p } < 2 d _ { n } - d _ { m p }$ , and $\mathcal { U } _ { n , p }$ at the ray $X _ { m p } = 2 \bar { c } _ { n } - c _ { m p } , Y _ { m p } < - ( 2 d _ { n } - d _ { m p } )$ . These rays point in the same direction. Clearly, given the parameters $( c _ { * } ^ { 0 } , d _ { * } ^ { 0 } )$ and $\dot { ( c _ { * } ^ { 1 } , d _ { * } ^ { 1 } ) } , \mathrm { i f } 2 c _ { n } ^ { 0 } - \dot { c } _ { m p } ^ { 0 }$ and $2 c _ { n } ^ { 1 } - c _ { m p } ^ { 1 }$ are of opposite sign, it is not possible to find the path $( c _ { * } ^ { t } , d _ { * } ^ { t } )$ such that neither of these rays of intersection do not pass through the origin in $\mathcal { P } _ { m , p } ( c _ { * } ^ { t } , d _ { * } ^ { t } )$

The consequence of the above Lemma is that the obstruction to fundamental group of $X _ { m , p } = X - \cup _ { ( i ^ { \prime } , j ^ { \prime } ) \neq ( m , p ) , 1 \leq i ^ { \prime } < j ^ { \prime } \leq N } \mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$ being $\mathbb { Z }$ are the intersections of $\mathcal { U } _ { m , p }$ with $\mathcal { U } _ { m , n }$ and $\mathcal { U } _ { n , p }$ , for every n such that m $< n < p$ . This leads us to split $\mathcal { U } _ { m , p }$ by the the hyperplane at which it is intersected by $\mathcal { U } _ { m , n }$ or $\mathcal { U } _ { n , p } ,$ for every $m < n < p .$ . It can however be noted that for $1 \leq m < n < p \leq N , \mathcal { U } _ { m , p } \cap \mathcal { U } _ { m , n }$ and $\mathcal { U } _ { m , p } \cap \mathcal { U } _ { n , p }$ are subsets of the same $( 2 N - 2 )$ -dimensional hyperplane. Thus we have the following splitting for $\mathcal { U } _ { m , p }$ only due to its intersection with $\mathcal { U } _ { m , n }$ and $\mathcal { U } _ { n , p } \colon$

$$
\begin{array}{r c l} \mathcal {U} _ {m, p / -} & = & \left\{(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}) \mid x _ {m} = x _ {p} \leq x _ {n}, y _ {m} <   y _ {p} \right\} \\ \mathcal {U} _ {m, p / +} & = & \left\{(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}) \mid x _ {m} = x _ {p} \geq x _ {n}, y _ {m} <   y _ {p} \right\} \end{array}
$$

In general, we have partitions of the form

$$
\mathcal {U} _ {m, p / \sigma_ {m + 1}, \sigma_ {m + 2}, \dots , \sigma_ {p - 1}} = \left\{(x _ {1}, y _ {1}, x _ {2}, y _ {2}, \dots , x _ {N}, y _ {N}) \mid y _ {m} <   y _ {p}, \left( \begin{array}{l} x _ {m} = x _ {p} \leq x _ {n} \text {if} \sigma_ {n} = ^ {\prime} - ^ {\prime} \\ x _ {m} = x _ {p} \geq x _ {n} \text {if} \sigma_ {n} = ^ {\prime} + ^ {\prime}, \forall m <   n <   p \end{array} , \forall m <   n <   p\right) \right\}\tag{1}
$$

Note that the $\boldsymbol { \sigma } ^ { \prime } \boldsymbol { \mathrm { s } }$ are indexed by integers from m+1 to $p { - } 1$ just for convenience (instead of indexing using $1 , 2 \cdots , p -$ $m - 1 )$ .

The following is a direct consequence

Corollary 1 The fundamental group of

$$
X_{i,j / \sigma_{i + 1},\sigma_{j + 2},\dots ,\sigma_{j - 1}}\quad := \quad X\text{-}\bigcup_{\substack{(i^{\prime},j^{\prime},\varsigma_{i^{\prime} + 1},\dots ,\varsigma_{j^{\prime} - 1})\neq (i,j,\sigma_{i + 1},\dots ,\sigma_{j - 1}),\\ 1\leq i^{\prime} <   j^{\prime}\leq N, \varsigma_{k}\in \{+, - \} \forall i^{\prime} <   k^{\prime} <   j^{\prime}}} \mathcal{U}_{i^{\prime},j^{\prime} / \varsigma_{i^{\prime} + 1},\dots ,\varsigma_{j^{\prime} - 1}}
$$

is isomorphic to $\mathbb { Z } .$

Thus, the $( 2 N - 1 )$ dimensional spaces, $\mathcal { U } _ { m , p / \sigma _ { m + 1 } , \sigma _ { m + 2 } , \cdots , \sigma _ { p - 1 } }$ , where $1 \leq i < j \leq N$ , and $\sigma _ { k }$ is either $\cdot _ { + } ,$ $\mathrm { o r } \ ^ { \bullet } - \ '$ , satisfy the conditions of Proposition 2. The set U is freely generated by letters, $\begin{array} { r } { u _ { m , p / \sigma _ { m + 1 } , \sigma _ { m + 2 } , \cdots , \sigma _ { p - 1 } } , } \end{array}$ corresponding to each of these spaces.

## 4.1.2 The Relation Set:

The relation set, R, contains the following types of words:

i. Due to the intersection of $\mathcal { U } _ { m , p } , \mathcal { U } _ { m , n }$ and $\mathcal { U } _ { n , p } \ ( m < n < p ) \colon \mathcal { U } _ { m , p } , \mathcal { U } _ { m , n }$ and $\mathcal { U } _ { n , p }$ intersect at a common $( 2 N - 2 )$ -dimensional hyperplane on which $x _ { m } = x _ { n } = x _ { p } ,$ , and for $y _ { m } < y _ { n } < y _ { p }$ . Let $\mathcal { P } _ { m , n , p } ( c _ { * } , d _ { * } )$ be a plane transverse to this intersection, coordinatized by $X _ { m n } = x _ { m } - x _ { n }$ and $X _ { n p } = x _ { n } - x _ { p }$ , so that $\mathcal { U } _ { m , p } \cap \mathcal { U } _ { m , n } \cap \mathcal { U } _ { n , p }$ intersects it at the origin on this plane. A loop around the origin in $\mathcal { P } _ { m , n , p } ( c _ { * } , d _ { * } )$ (Figure 7(b)) has the following word:

$$
\begin{array}{r l r} & & {“ u _ {m, n / \alpha_ {m + 1}, \dots , \alpha_ {n - 1}} \cdot u _ {m, p / \sigma_ {m + 1}, \dots , \sigma_ {n} ^ {(1)} = -, \dots , \sigma_ {p - 1}} \cdot u _ {n, p / \beta_ {n + 1}, \dots , \beta_ {p - 1}} \cdot} \\ & & {u _ {m, n / \alpha_ {m + 1}, \dots , \alpha_ {n - 1}} ^ {- 1} \cdot u _ {m, p / \sigma_ {m + 1}, \dots , \sigma_ {n} ^ {(2)} = +, \dots , \sigma_ {p - 1}} ^ {- 1} \cdot u _ {n, p / \beta_ {n + 1}, \dots , \beta_ {p - 1}} ”} \end{array}\tag{2}
$$

![](Bhattacharya2017Path_figs/921d30277dd3c5f2b99ed6a2c123dbd12e1c553f7133f01cf458e5cd1bda41be.jpg)  
(a) Schematic illustration of $\mathcal { O } _ { i , j } , \mathcal { U } _ { i , j }$ and its intersection with $\mathcal { O } _ { i ^ { \prime } , j ^ { \prime } } , \mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$  
(b) Plane $\mathcal { P } _ { m , n , p } ( c _ { * } , d _ { * } )$ transverse to $\mathcal { U } _ { m , p } \cap \mathcal { U } _ { m , n } \cap$ U<sub>n,p</sub>.  
Figure 7: Schematic illustration of the intersection of the constructed half-spaces, U .

for any choice of signs $\alpha _ { a } , \beta _ { b } \in \{ + , - \} , m < a < n , n < b < p ,$ , and $\sigma _ { k } = \left\{ { \begin{array} { l l } { \alpha _ { k } , { \mathrm { i f } } \ m < k < n } \\ { \beta _ { k } , { \mathrm { i f } } \ n < k < p } \end{array} } \right.$ (in order to ensure non-empty intersection). Note that the sign value of $\sigma _ { n }$ in the second letter of the word above is $\cdot \_ ,$ while it is $\cdot _ { + } ,$ in the fifth letter.

It can be noted that there exists non-empty intersection $\mathcal { U } _ { m , p } \cap \mathcal { U } _ { m , n }$ and $\mathcal { U } _ { m , p } \cap \mathcal { U } _ { n , p }$ that are outside the aforementioned common intersection of the three (the former when $y _ { m } < y _ { n } , y _ { m } < y _ { p } \leq y _ { n }$ and the later when $y _ { n } < y _ { p } , y _ { n } \leq y _ { m } < y _ { p } )$ . These intersections result in the following additional words in the relation set:

$$
\begin{array}{c} \text {``u} _ {m, n / \alpha_ {m + 1}, \dots , \alpha_ {n - 1}} \cdot u _ {m, p / \sigma_ {m + 1}, \dots , \sigma_ {n} ^ {(1)} = -, \dots , \sigma_ {p - 1}} \\ u _ {m, n / \alpha_ {m + 1}, \dots , \alpha_ {n - 1}} ^ {- 1} \cdot u _ {m, p / \sigma_ {m + 1}, \dots , \sigma_ {n} ^ {(2)} = +, \dots , \sigma_ {p - 1}} ^ {- 1} \end{array} .\tag{3}
$$

and

$$
\begin{array}{c} \text {``u} _ {m, p / \sigma_ {m + 1}, \dots , \sigma_ {n} ^ {(1)} = -, \dots , \sigma_ {p - 1}} \cdot u _ {n, p / \beta_ {n + 1}, \dots , \beta_ {p - 1}} \cdot \\ u _ {m, p / \sigma_ {m + 1}, \dots , \sigma_ {n} ^ {(2)} = +, \dots , \sigma_ {p - 1}} ^ {- 1} \cdot u _ {n, p / \beta_ {n + 1}, \dots , \beta_ {p - 1}} \end{array}\tag{4}
$$

ii. Due to the intersection of $\mathcal { U } _ { i , j }$ and $\mathcal { U } _ { i ^ { \prime } , j ^ { \prime } } \left( \mathrm { w i t h } i \leq i ^ { \prime } \right)$ , where $i , j , i ^ { \prime } , j ^ { \prime }$ are all distinct: Without loss of generality, assume either $i < i ^ { \prime } \mathrm { o r } i = \bar { i } ^ { \prime } , j < j ^ { \prime } . \mathcal { U } _ { i , j }$ and $\mathcal { U } _ { i ^ { \prime } , j ^ { \prime } }$ intersect at a $( 2 N - 2 )$ -dimensional hyperplane on which $x _ { i } = x _ { j } , x _ { i ^ { \prime } } = x _ { j ^ { \prime } }$ . The letters corresponding to these spaces simply commute. Thus we have the words:

$$
\begin{array}{c} \text {``u_{i,j / \sigma_{i + 1},\cdots,\sigma_{j - 1}} \cdot u_{i^{\prime},j^{\prime} /\gamma_{i^{\prime} + 1},\cdots,\gamma_{j^{\prime} - 1}} \cdot} \\ u _ {i, j / \sigma_ {i + 1}, \dots , \sigma_ {j - 1}} ^ {- 1} \cdot u _ {i ^ {\prime}, j ^ {\prime} / \gamma_ {i ^ {\prime} + 1}, \dots , \gamma_ {j ^ {\prime} - 1}} ^ {- 1} \end{array}\tag{5}
$$

for all $\sigma _ { k } , \gamma _ { l } \in \{ + , - \}$

The relation set, R, thus consists of all the words of the forms described in (2), (3), (4) and (5).

## 4.1.3 Explicit Example for $N = 3$

We consider the simple, yet non-rival case of $N = 3$ (coordination space of 3 robots navigating on a plane). The letters in U are $u _ { 1 , 2 } , u _ { 2 , 3 } , u _ { 1 , 3 / + }$ and $u _ { 1 , 3 / - }$ corresponding to respectively crossing of the manifolds $\mathcal { U } _ { 1 , 2 } =$ $\{ \mathbf { p } \mid x _ { 1 } = x _ { 2 } , y _ { 1 } < y _ { 2 } \} , \mathcal { U } _ { 2 , 3 } = \{ \mathbf { p } \mid x _ { 2 } = x _ { 3 } , y _ { 2 } < y _ { 3 } \} , \mathcal { U } _ { 1 , 3 / + } = \{ \mathbf { p } \mid x _ { 1 } = x _ { 3 } > x _ { 2 } , y _ { 1 } < y _ { 3 } \}$ and $\mathcal { U } _ { 1 , 3 / - } = \{ \mathbf { p } \mid x _ { 1 } = x _ { 3 } < x _ { 2 } , y _ { 1 } < y _ { 3 } \}$ . The relation set consists of the following words:

$$
\begin{array}{r l} \mathbf {R} = & \left\{ \begin{array}{l l} u _ {1, 2} u _ {1, 3 / -} u _ {2, 3} u _ {1, 2} ^ {- 1} u _ {1, 3 / +} ^ {- 1} u _ {2, 3} ^ {- 1}, \\ u _ {1, 2} u _ {1, 3 / -} u _ {1, 2} ^ {- 1} u _ {1, 3 / +} ^ {- 1}, \\ u _ {1, 3 / -} u _ {2, 3} u _ {1, 3 / +} ^ {- 1} u _ {2, 3} ^ {- 1} \end{array} \right\} \end{array}
$$

For simplicity, define $a \ = \ u _ { 1 , 2 } , \ b \ = \ u _ { 1 , 3 / + } , \ c \ = \ u _ { 1 , 3 / - } , \ d \ = \ u _ { 2 , 3 }$ . Rewriting the relation set, ${ \textbf { R } } =$ $\{ a c d a ^ { - 1 } b d ^ { - 1 } , a c a ^ { - 1 } b , c d b d ^ { - 1 } \}$ . This can be easily shown (by isolating b by setting the last relation to identity, and substituting it in the other two relations) to be isomorphic to the group $< a , c , d \mid a c d ( d a c ) ^ { - 1 } , c d a ( d a c ) ^ { - 1 } >$ Which in turn (using substitution $p = c d , q = d a c )$ can be shown to be isomorphic to the group

$< a , p , q \mid a p ( p a ) ^ { - 1 } , a q ( q a ) ^ { - 1 } > ( a$ commutes with both $p$ and $q ,$ but $p$ and $q$ themselves do not commute). This is clearly the group $\mathbb { Z } \times ( \mathbb { Z } * \mathbb { Z } )$ . In fact, simply using geometric arguments, it is easy to verify that the homotopy type of the coordination space of 3 robots on a plane is indeed that of $\mathbb { S } ^ { \bar { 1 } } \times ( \mathbb { S } ^ { 1 } \vee \mathbb { S } ^ { 1 } )$ ) (see [Arslan et al., 2016] for example).

## 5 Simulation Results

## 5.1 Knot and Link Complements

Given obstacles $\mathcal { O } \subset \mathbb { R } ^ { 3 }$ , and their “skeletons” (1-dimensional homotopy equivalents), $O \subseteq { \mathcal { O } }$ as polygons in $\mathbb { R } ^ { 3 }$ we first choose a projection map, $p : \mathbb { R } ^ { 3 }  \mathbb { R } ^ { 2 }$ , for the knot/link diagram. With this information, we implemented the automated construction of the surfaces, $U _ { i } .$ , for the Dehn presentation of the knot/link complement, and the symmetricized relation set, R, by computing the self-intersections in $p ( O )$ . We then used a uniform cubical discretization of $\mathbb { R } ^ { 3 } - \mathcal { O }$ to construct the graph G as a discrete representation of the free space, and in the h-augmented graph, $G _ { h } ,$ we find trajectories from $( x _ { s } , \cdots ) \mathrm { ~ t o ~ } ( x _ { g } , * )$ . We then employ a curve shortening algorithm to shorten the obtained trajectories. All our implementations were done in C++ programming language and visualization were done using OpenGL. The program ran on a laptop running on a Intel i7-4500U processor @ 1.80GHz with 8 GB memory.

Figure 8(a) shows results in the complement of a trefoil knot. The inset figure shows the surfaces, $U _ { i } .$ , used for Dehn presentation. The graph G was constructed out of uniform $1 0 0 \times 1 0 0 \times 1 0 0$ cubical discretization of the environment. As seen in the figure, using the proposed search-based algorithm we computed 5 shortest paths in different homotopy classes and used curve-shortening algorithms to shorten them to obtain the piece-wise linear paths. The entire computation (computation of the surfaces, the symmetricized relation set R, and computation of the 5 shortest trajectories) required about 8.1 s. Likewise, Figure 8(b) shows results in the complement of a simple Hopf link, with the same discretization of the environment, and total computation time of about 8.2 s.

Figure 8(c) shows a much more complex obstacle involving a torus knot linked to a genus-2 obstacle, and the entire computation of 20 trajectories took about 2.6 s. While in a complex space as this, the completeness of Dehn algorithm is not guaranteed, numerical computation still gives us reasonable results as can be seen in this simulation result.

It is interesting to observe that computing shortest paths in 5 different classes in the environments of Figures 8(a) and 8(b) took significantly longer than the computation of 20 classes in the environment of Figure 8(c). This is because in Figure $8 ( \mathrm { c ) }$ , although much more complex, the obstacles themselves occupy a large part of the environment. This significantly reduces the number of vertices and edges in the discrete graph representing the free configuration space than the trefoil knot and Hopf link complements. Thus the graph search runs much faster in the configuration space of Figure 8(c).

## 5.2 Coordination Space of 3 Robots Navigating on a Plane

Similar to the method described in Section 2.5, we implemented the graph search based approach for finding optimal paths in the coordination space of 3 robots navigating on a planar region. We constructed a graph using a uniform hyper-cubical discretization of the configuration space, $\overline { { \Gamma } } = \mathbb { R } ^ { 6 }$ , placing a vertex in each cell, and establishing edges between neighboring cells that correspond to robot motions parallel to the coordinate axes. The optimality criteria in the $\mathbf { A } ^ { * }$ search was chosen to be the sum of the total lengths of the paths (which, because of the chosen discretization, is the length due to the Manhattan metric on the plane) traversed by the robots. The h-augmented graph construction from this graph is similar to what has been described in Section 2.5. However for checking whether or not two h-signatures are the same, we use the Dehn algorithm on the presentation described in Example 4.1.3.

Figure 9 (also, in attached multimedia file) shows paths found in 5 different homotopy classes for the coordination space of 3 robots navigating on a plane. With the plane discretized into $7 \times 7$ grid, and the degree of each vertex in the corresponding joint configuration space being 124 (allowing each robot to move north, south, east or west, or stay in place), the computation of paths in 5 different homotopy classes in the coordination space took about 31.7 s. A careful observation of the figures will indeed reveal that the paths shown in each of the Figures $9 \ ( { \mathrm { a } } ) \mathbf { - } ( { \mathrm { e } } )$ correspond to the robots taking distinct homotopy classes in the joint configuration space.

![](Bhattacharya2017Path_figs/eb7e37e02360a601a69a992fa4533052866644d25d9a0dbff0786304d172fe26.jpg)  
(a) 5 trajectories in a trefoil knot complement.

![](Bhattacharya2017Path_figs/04f3a07028afd550b8f6d7487becd5ca1762f7ac4c70e4c9d473a1a783af1f0b.jpg)  
(b) 5 trajectories in a Hopf link complement.

![](Bhattacharya2017Path_figs/f24e90cf0afa5d1d79b708220c4a2dd31a06f9a8dfa4af54db5538697a8fdd0d.jpg)  
(c) 20 trajectories in the complement of a (3, 8) torus knot linked to a genus-2 torus.

Figure 8: Optimal trajectories (in discrete graph representation, followed by curve shortening) in different homotopy classes in complements of knots and links. Insets show the surfaces, $U _ { i }$

## 5.3 Some Remarks on Number of Homotopy Classes:

As described earlier, we compute the paths in the different homotopy classes by executing graph search algorithms (Dijkstra’s/A\*) on the h-augmented graph, $G _ { h }$ . As a result we obtain the paths in the different homotopy classes in order of their path lengths/costs. Technically, the number of homotopy classes in any of the configuration spaces described earlier infinite. This is because a path can loop/wind round an obstacle arbitrarily many times, thus creating arbitrarily many different homotopy classes. In the simulations we restrict ourselves to the computation of the first few homotopy classes in each configuration space since those are the classes that are most relevant in robotics applications.

## 6 Conclusion and Future Work

We presented explicit construction of presentations of the fundamental group of two different classes of spaces: Knot/link complements in Euclidean 3-dimensional spaces, and cylindrically deleted coordination space of multiple robots. We thus used graph search-based optimal path planning method for computing optimal paths in different homotopy classes in such environments. These spaces are highly relevant in many robot motion planning problems, for example unmanned aerial vehicles (UAVs) navigating inside buildings, and multiple ground robots navigating on a plane. Being able to compute optimal paths in different homotopy classes allow us to efficiently solve motion planning problems for complex systems such as tethered robots and systems involving cables, and design strategies for effectively deploying groups of robots in coverage and exploration tasks.

Moving forward, we will use the developed technique for homotopy path planning in 3-dimensional spaces with obstacles for computing optimal traversable paths for tethered unmanned aerial vehicles (UAVs). One of the greatest challenges currently faced by UAVs is the limited battery life, which in turn limits the UAVs’ flight time. Having the UAV tethered to a power supply will help alleviate the problem. But in that case one needs to carefully plan paths that satisfy the cable length constraints and prevents the cable from getting tangled in obstacles. Since a real UAV experiment will involve significant amount of investment in terms of equipments, time and development of low-level controllers, we believe an experiment as that is outside the scope of the current paper and will require significant deviation from the theoretical & algorithmic focus of the current paper. We thus propose such an experiment as a future work. But we believe that the new algorithmic tools proposed in this paper will be helpful in solving this real problem in 3-d.

## 7 Acknowledgements

The authors acknowledge the support of federal contracts FA9550-12-1-0416 and FA9550-09-1-0643. The first author acknowledges the support of ONR grant number N00014-14-1-0510 and University of Pennsylvania subaward number 564436.

![](Bhattacharya2017Path_figs/0050923bee66012a0e9368db541bf81a5d95676ae0fad18962e049777214c12b.jpg)  
(a) First homotopy class. Left-most figure: Initial configuration of the robots, with the robots’ indices labeled. Right-most figure: Final configuration of the robots. Intermediate figures illustrate the paths taken by the robots. Word corresponding to this class is $\tilde { } { } ^ {  } u _ { 1 , 3 / - } ^ { - 1 } \cdot \stackrel { \sim } { u _ { 1 , 2 } ^ { - 1 , 9 } }$

![](Bhattacharya2017Path_figs/95418634de30fa4fd337b38d6413d5ef16f455ed484621b87bf22a86947b9fe1.jpg)  
(b) Second homotopy class corresponding to word “u<sub>2,3</sub>”.

![](Bhattacharya2017Path_figs/7be35021f18c29a8654ceb1caee34bd28d2798467a09319253860bc408d6e7bc.jpg)  
(c) Third homotopy class corresponding to word “u<sub>2,3</sub> · u<sup>−1</sup> 1,3/+

![](Bhattacharya2017Path_figs/4759c78de36812d2a64e6b33f40343a9355147423135b38140e2f4528588d24e.jpg)  
(d) Fourth homotopy class corresponding to word “u<sub>2,3</sub> · u · u<sub>2,3</sub>” −1 −1

![](Bhattacharya2017Path_figs/e3fd1a07d919276ae82852fc5062e836e41956878406ce01fae090920c174026.jpg)  
(e) Fifth homotopy class corresponding to word “ ”  
Figure 9: Paths in 5 different homotopy classes in the coordination space of 3 robots navigating on a plane for an initial configuration to a final goal configuration. The classes found are in ascending order of the sum of the lengths of the paths of the three robots (where length is induced by the Manhattan metric on the plane).

## References

O. Arslan, D. P. Guralnik, and D. E. Koditschek. Coordinated robot navigation via hierarchical clustering. IEEE Transactions on Robotics, 32(2):352–371, April 2016. ISSN 1552-3098.

S. Bhattacharya, S. Kim, H. Heidarsson, G. Sukhatme, and V. Kumar. A topological approach to using cables to separate and manipulate sets of objects. International Journal of Robotics Research, online first publication, February 2015. DOI: 10.1177/0278364914562236.

Subhrajit Bhattacharya and Robert Ghrist. Path homotopy invariants and their application to optimal trajectory planning. In Proceedings of IMA Conference on Mathematics of Robotics (IMAMR), St Anne’s College, University of Oxford, September 9-11 2015.

Subhrajit Bhattacharya, Maxim Likhachev, and Vijay Kumar. Topological constraints in search-based robot path planning. Autonomous Robots, pages 1–18, June 2012. ISSN 0929-5593. DOI: 10.1007/s10514-012-9304-1.

Subhrajit Bhattacharya, David Lipsky, Robert Ghrist, and Vijay Kumar. Invariants for homology classes with application to optimal search and planning problem in robotics. Annals of Mathematics and Artificial Intelligence (AMAI), 67(3):251–281, March 2013. DOI: 10.1007/s10472-013-9357-7.

J. Canny and J. H. Reif. New lower bound techniques for robot motion planning problems. In Proc. 28th Annu. IEEE Sympos. Found. Comput. Sci., pages 49–60, 1987.

D. C. Cohen and G. Pruidze. Motion planning in tori. ArXiv Mathematics e-prints, March 2007.

T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein. Introduction to algorithms. MIT Press, 2nd edition, 2001.

Armindo Costa and Michael Farber. Motion planning in spaces with small fundamental groups. Communications in Contemporary Mathematics, 12(01):107–119, 2010. doi: 10.1142/S0219199710003750.

Richard H. Crowell. On the van kampen theorem. Pacific J. Math., 9(1):43–50, 1959.

Douglas Demyen and Michael Buro. Efficient triangulation-based pathfinding. In AAAI’06: Proceedings of the 21st national conference on Artificial intelligence, pages 942–947. AAAI Press, 2006. ISBN 978-1-57735-281-5.

D. B. A. Epstein. Word Processing in Groups. Ak Peters Series. Taylor & Francis, 1992.

M. Farber. Topological complexity of motion planning. ArXiv Mathematics e-prints, November 2001.

M. Farber, M. Grant, and S. Yuzvinsky. Topological complexity of collision free motion planning algorithms in the presence of multiple moving obstacles. ArXiv Mathematics e-prints, September 2006.

R. Ghrist and S. LaValle. Nonpositive curvature and pareto optimal motion planning. SIAM Journal of Control and Optimization, 45(5):1697–1713, 2006.

Vijay Govindarajan, Subhrajit Bhattacharya, and Vijay Kumar. Human-robot collaborative topological exploration for search and rescue applications. In International Symposium on Distributed Autonomous Robotic Systems (DARS), 2014.

E. Greendlinger and M. Greendlinger. On dehn presentations and dehn algorithms. Illinois J. Math., 30(2):360–363, 06 1986.

D. Grigoriev and A. Slissenko. Polytime algorithm for the shortest path in a homotopy class amidst semi-algebraic obstacles in the plane. In ISSAC ’98: Proceedings of the 1998 international symposium on Symbolic and algebraic computation, pages 17–24, New York, NY, USA, 1998. ACM.

Allen Hatcher. Algebraic Topology. Cambridge Univ. Press, 2001.

J. Hershberger and J. Snoeyink. Computing minimum length paths of a given homotopy class. Comput. Geom. Theory Appl, 4:331–342, 1991.

S. Kim, S. Bhattacharya, and V. Kumar. Path planning for a tethered mobile robot. In Proceedings of IEEE International Conference on Robotics and Automation, Hong Kong, China, May 31 - June 7 2014.

W.B.R. Lickorish. An Introduction to Knot Theory. Graduate Texts in Mathematics. Springer New York, 1997. ISBN 9780387982540.

R.C. Lyndon and P.E. Schupp. Combinatorial Group Theory. Classics in Mathematics. Springer Berlin Heidelberg, 2001. ISBN 9783540411581.

Joseph S. B. Mitchell and Micha Sharir. New results on shortest paths in three dimensions. In Proceedings of the Twentieth Annual Symposium on Computational Geometry, pages 124–133. ACM, 2004.

G. A. Niblo and L. D. Reeves. The geometry of cube complexes and the complexity of their fundamental groups. Topology, 37(3):621–633, 1998.

E. Schmitzberger, J.L. Bouchet, M. Dufaut, D. Wolf, and R. Husson. Capture of homotopy classes with probabilistic road map. In International Conference on Intelligent Robots and Systems, volume 3, pages 2317–2322, 2002.

W.R. Scott and W.R. Scott. Group Theory. Dover Books on Mathematics Series. Dover Publ., 1964. ISBN 9780486653778.

Benjamn Tovar, Fred Cohen, and Steven M. LaValle. Sensor beams, obstacles, and possible paths. In Workshop on the Algorithmic Foundations of Robotics, pages 317–332, 2008.

C. M. Weinbaum. The word and conjugacy problems for the knot group of any tame, prime, alternating knot. Proceedings of the American Mathematical Society, 30(1):22–26, September 1971.