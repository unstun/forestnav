---
citation_key: Qureshi2017Intelligent
arxiv_id: 1703.08944
arxiv_url: "https://arxiv.org/abs/1703.08944"
title: "Intelligent bidirectional rapidly-exploring random trees for optimal motion planning in complex cluttered environments"
authors_short: "Ahmed Hussain Qureshi et al."
year: 2017
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:52:51Z
origin: ai+web
reviewed: false
---

# Intelligent bidirectional rapidly-exploring random trees for optimal motion planning in complex cluttered environments∗

Ahmed Hussain Qureshi<sup>1,2</sup>, Yasar Ayaz<sup>1</sup>

<sup>1</sup>Robotics And Intelligent Systems Engineering (RISE) Lab Department of Robotics and Artificial Intelligence School of Mechanical And Manufacturing Engineering (SMME) National University of Sciences And Technology (NUST) H-12 Campus, Islamabad, 44000, Pakistan.

<sup>2</sup>Department of System Innovation Graduate School of Engineering Science Osaka University, 1-3 Machikaneyama, Toyonaka, Osaka, Japan.

March 27, 2017

## Abstract

The sampling based motion planning algorithm known as Rapidly-exploring Random Trees (RRT) has gained the attention of many researchers due to their computational eficiency and efectiveness. Recently, a variant of RRT called RRT\* has been proposed that ensures asymptotic optimality. Subsequently its bidirectional version has also been introduced in the literature known as Bidirectional-RRT\* (B-RRT\*). We introduce a new variant called Intelligent Bidirectional-RRT\* (IB-RRT\*) which is an improved variant of the optimal RRT\* and bidirectional version of RRT\* (B-RRT\*) algorithms and is specially designed for complex cluttered environments. IB-RRT\* utilizes the bidirectional trees approach and introduces intelligent sample insertion heuristic for fast convergence to the optimal path solution using uniform sampling heuristics. The proposed algorithm is evaluated theoretically and experimental results are presented that compares IB-RRT\* with RRT\* and B-RRT\*. Moreover, experimental results demonstrate the superior eficiency of IB-RRT\* in comparison with RRT\* and B-RRT in complex cluttered environments.

## 1 Introduction

Motion planning is a well-known problem in robotics [24]. It can be defined as the process of finding a collision-free path for a robot from its initial to goal point while avoiding collisions with any static obstacles or other agents present in its environment. Although motion planning is not the only fundamental problem of robotics, perhaps it has gained popularity among researchers due to widespread applications such as in robotics [21], assembly maintenance [3], computer animation [7], computer-aided surgery [9], manufacturing [22], and many other aspects of daily life.

The journey of finding solution to motion planning problems started with complete planning algorithms that comprised of deterministic path planning ap proach. Complete motion planning algorithms [35] [28] are those algorithms that converges to a path solution, if one exists, in finite time. These algo rithms are proven to be computationally ineficient [2] in most of the practical motion planning problems [13]. Resolution complete algorithms were then introduced that require fine tuning of resolution pa rameters for providing the motion planning solution, if one exists, in a finite time period. Artificial Po tential Fields (APF) [16] is a well-known resolution complete algorithm. However, APF sufers from the problem of local minima [18] and does not performed well in the environment with narrow passages. Hence, the search for an eficient solution to the problem continued and the idea of exact roadmaps was introduced in the literature which relies on the discretization of the given search space. This discretization of search space makes the algorithm computationally expen sive for higher dimensional spaces, that is why the application of such algorithms like Cell Decomposition methods [19] [1], Delaunay Triangulations [10] and Dynamic Graph Search methods [4] [25] are lim ited to low dimensional spaces only [5]. Moreover the algorithms that combine the set of allowed mo tions with the graph search methods thus generat ing state lattices, such as in [8] [31] [30], also suf fered from the undesirable efects of discretization. Hence to solve the higher dimensional planning prob lems, the sampling-based algorithms were introduced [5]; the main advantage of sampling-based algorithms as compared to other state-of-the-art algorithms is avoidance of explicit construction of obstacle config uration space. These algorithms ensure probabilistic completeness which implies that as the number of iterations increases to infinity, the probability of find ing a solution, if one exists, approaches one. The sampling-based algorithms have proven to be computationally eficient [2] solution to motion planning problems. Arguably, the most well-known sampling based algorithms include Probabilistic Road Maps (PRM) [14] [15] and Rapidly exploring Random Trees (RRT) [23]. However, PRMs tend to be ineficient when obstacle geometry is not known beforehand [13]. Therefore, in order to derive eficient solu tions for motion planning in the practical world, th

Rapidly-exploring Random Trees (RRT) algorithms [23] have been extensively explored. Various algorithms enhancing original RRT algorithm have been proposed [26], [6], [20], [13]. These algorithms present a solution regardless of whether specific geometry of the obstacles is known beforehand or not. One of the most remarkable variant of RRT algorithm is RRT\*, an algorithm which guarantees eventual convergence to an optimal path solution [13], unlike the original RRT algorithm. Just like the RRT algorithm, RRT\* is able to generate an initial path towards the goal very quickly. It then continues to refine this initial path in successive iterations, eventually returning an optimal or near optimal path towards the goal as the number of iterations approach infinity [12]. This additional guarantee of optimality makes the RRT\* algorithm very useful for real-time applications [29]. However, some major constraints still exist in this RRT variant which are presented in this paper. For example:

(i) its slow convergence rate in achieving the optimal solution;

(ii) its significantly large memory requirements due to the large number of iterations utilized to calculate the optimal path; and

(iii) its rejection of samples which may not be directly connectable with the existing nodes in the tree, but may lie closer to the goal region and hence could aid the algorithm in determining an optimal path much faster.

Various heuristics have been introduced, such as [32] [33] [34] [17], which perform guided search of the given space instead of pure uniform search (as by RRT and RRT\*). Although these biased sampling heuristics make the original RRT\* algorithm fast but there is a drawback of computational overload caused by biased sampling. This computational overload limits their application to a limited number of fields [27]. Moreover another disadvantage of deterministic sampling heuristics is that they may interfere with the algorithm characteristics. For example assume a simple case of using goal-biased sampling [33] with bidirectional RRT that alternatively grows two trees. The use of this biased sampling will cause the two trees to always remain in one half of the search space, which is quite undesirable. Hence, to cover the whole search space, a separate sample generator is required for both trees which will cost a signifi cant computational load. Hence there is a need of some better approach that enhances the convergence rate of $\mathrm { R R T ^ { * } }$ for achieving the optimal path solution without afecting the randomization of its sampling heuristic. More recent proposition is the bidirectional version of RRT\* known as $\mathrm { B { - } R R T ^ { * } }$ [11]. $\mathrm { B { - } R R T ^ { * } }$ presented in [11] is a simple bidirectional implementation of RRT\*. B-RRT\* uses a slight variation of greedy RRT-Connect heuristic [20] for th connection of two trees. Two directional trees employing greedy connect heuristic for the connection of trees does not ensure asymptotic optimality [11]. The $\mathrm { B { - } R R T ^ { * } }$ uses slight variation of greedy heuris tic $\mathrm { i . e . } .$ , the tree under process first searches for the neighbor vertices before making an attempt to connect the trees using RRT-Connect heuristic [20]. This hybrid greedy connection heuristic of $\mathrm { B { - } R R T ^ { * } }$ slows down its ability to converge to the optimal solution and also makes it computationally expensive. More detailed discussion is provided in the analysis sec tion. This paper introduces a bidirectional variation to the $\mathrm { R R T ^ { * } }$ algorithm, with unique sample insertion and tree connection heuristics that allows fast con vergence to the optimal path solution. The proposed Intelligent Bidirectional- $\mathrm { \cdot R R T ^ { * } }$ (IB-RRT\*) algorithm has been tested for its robustness in both 2-D and 3-D environments and has also been compared with other state-of-art algorithms such as Bidirectional $\mathrm { R R T ^ { * } [ 1 1 ] }$ and $\mathrm { R R T ^ { * } }$ itself [12]. The rest of the paper is organized as follows. Section 2 addresses the problem definition, Section 3 explains the $\mathrm { R R T ^ { * } }$ algorithm while Section 4 describes the $\mathrm { B } { \mathrm { - R R T ^ { * } } }$ motion planning algorithm in detail. Section 5 presents the proposed Intelligent Bidirectional-RRT\* (IB-RRT\*). Section 6 presents analysis of the three algorithms un der investigation in terms of probabilistic complete ness, asymptotic optimality, convergence to the op timal solution and computational complexity. Section 7 provides experimental evidence in support of theoretical results presented in the previous section, whereas Section 8 concludes the paper, also suggesting some future areas of research in this particular domain.

## 2 Problem Definition

Let the given state space be denoted by a set $X \subset \mathbb { R } ^ { n }$ where n represents the dimension of the given space i.e., $n \in \mathbb { N } , n \geq 2 .$ The configuration space is further classified into obstacle and obstacle-free regions denoted by $X _ { \mathrm { o b s } } \subset X$ and $X _ { \mathrm { f r e e } } = X \backslash X _ { \mathrm { o b s } } ,$ respectively. $X _ { \mathrm { g o a l } } \subset X _ { \mathrm { f r e e } }$ is the goal region. Let $T _ { \mathrm { a } } = ( V _ { \mathrm { a } } , E _ { \mathrm { a } } ) \stackrel { \smile } { \subset } X _ { \mathrm { f r e e } }$ and $T _ { \mathrm { b } } = ( V _ { \mathrm { b } } , E _ { \mathrm { b } } ) \subset X _ { \mathrm { f r e e } }$ represent two growing random trees, where V denotes the nodes and E denotes the edges connecting these nodes. $x _ { \mathrm { i n i t } } ^ { \mathrm { a } } \in X _ { \mathrm { f r e e } }$ and $x _ { \mathrm { i n i t } } ^ { \mathrm { b } } \in X _ { \mathrm { g o a l } }$ represent the starting states for $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } } .$ . The function $\mu ( )$ computes the Lebesgue measure of any given state space $\begin{array} { r l } { \mathrm { e . g . } } & { { } \mu ( X ) } \end{array}$ denotes the Lebesgue measure of the whole state space X. It is also called the n-dimensional volume of any given configuration. This paper only considers Euclidean space and posi tive Euclidean distance between any two states $\mathrm { e . g . }$ $x _ { 1 } \in X$ and $x _ { 2 } \in X$ is denoted by $\mathrm { d } ( x _ { 1 } , x _ { 2 } )$ . The closed ball region of radius $r \in \mathbb { R } , r > 0$ centered at x is denoted as $\mathfrak { B } _ { x , r } : = \{ x _ { 2 } \in X : d ( x , x _ { 2 } ) \leq r \}$ where $x \in X$ can be any given configuration state. Let the path connecting any two states $x _ { 1 } \in X _ { \mathrm { f r e e } }$ and $x _ { 2 } \in X _ { \mathrm { f r e e } }$ be denoted by $\sigma : [ 0 , s ^ { \prime } ]$ , such that $\sigma ( 0 ) = x _ { 1 }$ and $\sigma ( s ^ { \prime } ) = x _ { 2 }$ , whereas, $s ^ { \prime }$ is the positive scalar length of the path. The set of all collision-free paths σ is denoted as $\sum \mathrm { _ { f r e e } }$ . Given any random state $x \in X _ { \mathrm { f r e e } }$ , the path function connecting initial state $x _ { \mathrm { i n i t } }$ and random state x is denoted as $\sigma _ { \mathrm { a } } ^ { \prime } [ 0 , s _ { \mathrm { a } } ] ~ \subset$ $X _ { \mathrm { f r e e } } | \{ \sigma _ { \mathrm { a } } ^ { \prime } ( 0 ) = x _ { \mathrm { i n i t } }$ and $\sigma _ { \mathrm { a } } ^ { \prime } ( s _ { \mathrm { a } } ) = x \}$ , while the path function connecting random state x and goal region $X _ { \mathrm { g o a l } }$ is denoted as $\sigma _ { \mathrm { b } } ^ { \prime } [ 0 , s _ { \mathrm { b } } ] \subset X _ { \mathrm { f r e e } } | \{ \sigma _ { \mathrm { b } } ^ { \prime } ( 0 ) = x$ and $\sigma _ { \mathrm { b } } ^ { \prime } ( s _ { \mathrm { b } } ) \ \in \ { \cal X } _ { \mathrm { g o a l } } \}$ . The complete, end-to-end path function $\mathrm { i . e . } .$ the path function from root to the goal is denoted by $\sigma _ { \mathrm { f } } ^ { \prime } ( \mathrm { s } ) = \sigma _ { \mathrm { a } } ^ { \prime } | \sigma _ { \mathrm { b } } ^ { \prime } : [ 0 , s ] \in X$ , where s represents the scalar length of the end-to-end path. The expression $\sigma _ { \mathrm { a } } ^ { \prime } | \sigma _ { \mathrm { b } } ^ { \prime } \in X$ describes the concatenation of the two path functions, $\sigma _ { \mathrm { a } } ^ { \prime }$ and $\sigma _ { \mathrm { b } } ^ { \prime } .$ . The path function $\sigma _ { \mathrm { f } }$ is the end-to-end feasible path in obstacle-free configuration space, i.e., $\sigma _ { \mathrm { f } } ~ \in ~ X _ { \mathrm { f r e e } }$ . The set of all end-to-end collision-free paths is denoted as $\textstyle \sum _ { \mathrm { f } }$ i.e., $\sigma _ { \mathrm { f } } \in \sum _ { \mathrm { ~ \Gamma ~ } } .$ . The cost function c( ) computes the cost in terms of Euclidean distance.

The following motion planning problems will be considered in the proposed algorithm:

Problem 1 (Feasible path solution) Find a path $\sigma _ { \mathrm { f } } : [ 0 , s ]$ , if one exists, in obstacle-free space $X _ { \mathrm { { f r e e } } } \subset { \dot { X } }$ such that $\sigma _ { \mathrm { f } } ( 0 ) = x _ { \mathrm { i n i t } } \in X _ { \mathrm { f r e e } }$ and $\sigma _ { \mathrm { f } } ( s ) \in X _ { \mathrm { g o a l } }$ . If no such path exists, report failure.

Problem 2 (Optimal path solution) Find an optimal path $\sigma _ { \mathrm { f } } ^ { * } : [ 0 , s ]$ connecting $x _ { \mathrm { i n i t } }$ and $X _ { \mathrm { g o a l } }$ in obstacle-free space $X _ { \mathrm { f r e e } } \subset X _ { \mathrm { : } }$ , such that the cost of the path $\sigma _ { \mathrm { f } } ^ { * }$ is minimum, $\begin{array} { r } { i . e . , \ c ( \sigma _ { \mathrm { f } } ^ { * } ) = \{ \operatorname* { m i n } _ { \sigma _ { \mathrm { s } } } c ( \sigma _ { \mathrm { f } } ) : } \end{array}$ $\sigma _ { \mathrm { f } } \in \Sigma _ { \mathrm { f } } \}$

Problem 3 (Convergence to Optimal Solution) Find the optimal path $\sigma _ { \mathrm { f } } ^ { * } : [ 0 , s ]$ in obstacle-free space $X _ { \mathrm { f r e e } } \subset X$ in the least possible time $t \in \mathbb { R }$

## 3 RRT\* Algorithm

This section describes the RRT\* algorithm [12]. Algorithm 1 is a slightly modified implementation of RRT\*. In this version, improvements were made to the original algorithm in order to enhance the computational eficiency of $\mathrm { R R T ^ { * } }$ by reducing the number of calls to the ObstacleFree procedure [29]. Following are some of the processes employed by RRT\*:

```txt
Algorithm 1: RRT*(xinit)

1 V ← {xinit}; E ← ∅; T ← (V, E);
2 for i ← 0 to N do
3    xrand ← Sample(i)
4    Xnear ← NearVertices(xrand, T)
5    if Xnear = ∅ then
6    Xnear ← NearestVertex(xrand, T)
7    Ls ← GetSortedList(xrand, Xnear)
8    xmin ← ChooseBestParent(Ls)
9    if xmin ≠ ∅ then
10    T ← InsertVertex(xrand, xmin, T)
11    T ← RewireVertices(xrand, Ls, E)
12 return T = (V, E)
```

Random Sampling: the Sample procedure returns an independent and uniformly distributed random sample from the obstacle free space, i.e., $x _ { \mathrm { r a n d } } ~ \in$ $X _ { \mathrm { f r e e } }$

Collision Check: the procedure ObstracleFree(σ) checks whether the given path $\sigma : [ 0 , 1 ]$ belongs to

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: GetSortedList( $x_{rand}, X_{near}$ )

1  $L_{s} \leftarrow \emptyset$ 

2 for  $x' \in X_{near}$  do

3  $\sigma' \leftarrow Steer(x', x_{rand})$ 

4  $C' \leftarrow c(x_{init}, x') + c(x', x_{rand})$ 

5  $L_{s} \leftarrow (x', C', \sigma')$ 

6  $L_{s} \leftarrow SortList(L_{s})$ 

7 return  $L_{s}$
</div>

$X _ { \mathrm { f r e e } }$ or not. A true value is reported if $\sigma ( s ) \in$ $X _ { \mathrm { f r e e } } \forall s [ 0 , 1 ]$

Near Vertices: given a sample $x \in X$ , the tree $T =$ $( V , E )$ and the ball region $\mathfrak { B } _ { x , r }$ of radius r centered at x, the set of near vertices is defined as:

Nea $\left. x , T , r \right. : = \left\{ v \in V : v \in \mathfrak { B } _ { x , r } \right\} \mapsto X _ { \mathrm { n e a r } } \subseteq$ V . More specifically, $X _ { \mathrm { n e a r } } = \{ v \in V : d ( x , v ) \leq$ $\gamma ( l o g i / i ) ^ { 1 / n } \}$ where i is the number of vertices, n represents the dimensions and $\gamma$ is a constant.

Nearest Vertex: As its name suggests, this procedure returns the nearest vertex in the tree from any given state $x \in X$ . Given the tree $T = ( V , E )$ , the nearest vertex procedure can be defined as:

Neares $\begin{array} { r } { \langle T , x \rangle : = \mathrm { a r g m i n } _ { v \in V } d ( x , v ) \mapsto x _ { \operatorname* { m i n } } . } \end{array}$ Getting Sorted List: the procedure GetSortedList in Algorithm 2 constructs a tuple and returns it as the list $L _ { \mathrm { s } } .$ Each element of this list is a triplet of form $( x ^ { \prime } , c ( \sigma ) , \sigma ^ { \prime } ) \in L _ { \mathrm { s } }$ where $x ^ { \prime } \in X _ { \mathrm { n e a r } }$ . The list $L _ { \mathrm { s } }$ is sorted in the ascending value of the cost function.

Steering: the steering function utilised in this modified version of $\mathrm { R R T ^ { * } }$ takes two states as an input and returns the straight trajectory connecting those two states. For example, for two given states $x _ { 1 } ~ \in ~ X$ and $x _ { 2 } \in X .$ , the path $\sigma : [ 0 , 1 ]$ will be the path connecting these two states, i.e., $\sigma ( 0 ) ~ = ~ x _ { 1 }$ and $\sigma ( 1 ) ~ = ~ x _ { 2 }$ The steering is done from $x _ { 1 }$ to $x _ { 2 }$ in small, discrete steps and can be summarized as $\sigma ( s ^ { \prime } ) = ( 1 - s ^ { \prime } ) x _ { 1 } + s ^ { \prime } x _ { 2 } ; \forall s ^ { \prime } [ 0 , 1 ]$

Choosing Best Parent: this procedure is used to search the list $L _ { \mathrm { s } }$ for a state, $x _ { \mathrm { m i n } } \in L _ { \mathrm { s } }$ which provides the shortest, collision-free path $\sigma ^ { \prime }$ from the initial state $x _ { \mathrm { i n i t } }$ to the random sample $x _ { \mathrm { r a n d } }$ . Alternatively, $\sigma ^ { \prime }$ is the shortest collision-free path connecting the initial state $x _ { \mathrm { i n i t } }$ and the random sample $x _ { \mathrm { r a n d } }$ via

$x _ { \mathrm { m i n } } \in L _ { \mathrm { s } }$ . Algorithm 3 outlines the implementation of this procedure.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: ChooseBestParent( $L_{s}$ )

1 for  $(x', C', \sigma') \in L_{s}$  do
2 if ObstacleFree( $\sigma'$ ) then
3 return  $x'$ 
4 return  $\emptyset$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4: RewireVertices($x_{\text{rand}}, L_s, E$)
1 for $(x', C', \sigma') \in L_s$ do
2 if $(c(x_{\text{init}}, x_{\text{rand}}) + c(x_{\text{rand}}, x')) &lt; c(x_{\text{init}}, x')$
    then
3 if ObstacleFree($\sigma_{\text{new}}$) then
4 $x_{\text{parent}} \leftarrow \text{Parent}(E, x')$
5 $E \leftarrow (E \setminus \{(x_{\text{parent}}, x')\}) \cup (\{x_{\text{rand}}, x'\})$
6 return $E$
</div>

The $\mathrm { R R T ^ { * } }$ algorithm provides asymptotic optimality. In reference to Algorithm 1, the $\mathrm { R R T ^ { * } }$ algorithm after preliminary initialization process starts its iterative process by sampling the random sample $x _ { \mathrm { r a n d } }$ from the given configuration space $X _ { \mathrm { f r e e } }$ (Line 3). After this, the $\mathrm { R R T ^ { * } }$ finds the set of near vertices $X _ { \mathrm { n e a r } }$ from the tree lying inside the ball region centered at $x _ { \mathrm { r a n d } }$ . If the set of near vertices $X _ { \mathrm { n e a r } }$ computed by NearVertices procedure is empty, then the set $X _ { \mathrm { n e a r } }$ is filled by the NearestVertex procedure (Line 4-6). The populated set $X _ { \mathrm { n e a r } }$ is then sorted by the GetSortedList procedure to form a list of form $( x ^ { \prime } , c ( \sigma ) , \sigma ^ { \prime } )$ , arranged in ascending order of cost function $c ( \sigma )$ (Line 7). The procedure ChooseBestParent iterates over the sorted list $L _ { \mathrm { s } }$ (Line 8), returning the best parent vertex $x _ { \mathrm { m i n } } ~ \in$ $X _ { \mathrm { n e a r } }$ through which $x _ { \mathrm { i n i t } }$ and $x _ { \mathrm { r a n d } }$ can be connected in obstacle-free space. Once such a state is located, i.e, the best parent vertex $x _ { \mathrm { m i n } }$ is no longer empty, $x _ { \mathrm { m i n } }$ is inserted into the tree by making $x _ { \mathrm { r a n d } }$ its child and then the rewiring step is executed (Line 9-11). Algorithm 4 presents the pseudocode of the rewiring process. Here, the algorithm examines each vertex $x ^ { \prime } \in X _ { \mathrm { n e a r } }$ lying inside the ball region centered at $x _ { \mathrm { r a n d } }$ . If the cost of the path connecting $x _ { \mathrm { i n i t } }$ and $x ^ { \prime }$ through $x _ { \mathrm { r a n d } }$ is less than the existing cost of reaching $x ^ { \prime }$ and if this path lies in obstacle-free space $X _ { \mathrm { f r e e } }$ (Algorithm 4 Line 1-3), then $x _ { \mathrm { r a n d } }$ is made the parent of $x ^ { \prime }$ (Algorithm 4 Line 4-5). If these conditions do not hold true, no change is made to the tree and the algorithm moves on to check the next vertex. This process is iteratively performed for every vertex $x ^ { \prime }$ present in the sorted list $L _ { \mathrm { s } } .$

```txt
Algorithm 5: B-RRT*(xinit, xgoal)

1 V ← {xinit, xgoal}; E ← ∅;
    Ta ← (xinit, E); Tb ← (xgoal, E);

2 σbest ← ∞

3 for i ← 0 to N do

4    xrand ← Sample(i)
5    xnearest ← NearestVertex(xrand, Ta)
6    xnew ← Extend(xnearest, xrand)
7    Xnear ← NearVertices(xnew, Ta)
8    Ls ← GetSortedList(xnew, Xnear)
9    xmin ← ChooseBestParent(Ls)
10    if xmin ≠ ∅ then
11    T ← InsertVertex(xnew, xmin, Ta)
12    T ← RewireVertices(xnew, Ls, E)
13    xconn ← NearestVertex(xnew, Tb)
14    σnew ← Connect(xnew, xconn, Tb)
15    if σnew ≠ ∅&&c(σnew) < c(σbest) then
16    σbest ← σnew
17    SwapTrees(Ta, Tb)

18 return Ta, Tb = (V, E)
```

## 4 B-RRT\* algorithm

This section explains the implementation of Bidirectional-RRT\*(B-RRT\*) [11]. Algorithm 5 outlines the implementation of B-RRT\*; extra procedures employed by B-RRT\* are explained below while the rest are exactly the same as they were for RRT\*.

Extend: given two nodes $x _ { 1 } , x _ { 2 } \in X$ , the

Extend $( x _ { 1 } , x _ { 2 } )$ procedure returns a new node $x _ { \mathrm { n e w } } \in \mathbb { R } ^ { n }$ such that $x _ { \mathrm { n e w } }$ is more closer to $x _ { 2 }$ than $x _ { 1 }$ in the direction from $x _ { 1 }$ to $x _ { 2 }$

Connect: connect heuristic employed by $\mathrm { B } -$ $\mathrm { R R T ^ { * } }$ is slight variation of greedy RRT-Connect heuristic[20]. Algorithm 6 outlines the implementation of Connect heuristic of B-RRT\*. Typical RRT\* iteration is performed on the input nodes $x _ { 1 } , x _ { 2 }$ 2 where $x _ { 1 }$ plays the role of $x _ { \mathrm { r a n d } }$ while the set of near vertices is computed from the other tree (Line 1-2). After computing a set of near vertices from tree $^ { \mathrm { b , } }$ the procedure GetSortedList (explained in previous section) is executed, and the best vertex is selected from the sorted list such that it provides collision-free low-cost connection between the trees $T _ { \mathrm { a } } , T _ { \mathrm { b } }$ Finally, this procedure ends by generating and returning the end-to-end feasible path solution, connecting $x _ { \mathrm { i n i t } }$ and $X _ { \mathrm { g o a l } }$

In reference to Algorithm 5, the B-RRT\* works in exactly the same manner as the original $\mathrm { R R T ^ { * } }$ algorithm in its initial phases $\mathrm { i . e . , }$ , it starts with sampling of the configuration space $X _ { \mathrm { f r e e } } ,$ then various operations (just like RRT\*) are performed on this random sample $x _ { \mathrm { r a n d } }$ (Line 4-12 ). After successful insertion of random sample into the tree under operation (Line 11-12), the algorithm computes nearest vertex $x _ { \mathrm { c o n n } }$ from $x _ { \mathrm { n e w } }$ in the tree $T _ { \mathbf { b } } .$ , and then executes the connect procedure for the connection of two trees (Line 13-14). If the attempt to make connection is successful, the collision-free path $\sigma _ { \mathrm { n e w } }$ connecting $x _ { \mathrm { i n i t } }$ and $X _ { \mathrm { g o a l } }$ is returned by the connect function. The cost of this $\sigma _ { \mathrm { n e w } }$ is then compared with the previously computed path $\sigma _ { \mathrm { b e s t } }$ . If the cost of $\sigma _ { \mathrm { n e w } }$ is less than the cost of $\sigma _ { \mathrm { b e s t } } ,$ then $\sigma _ { \mathrm { b e s t } }$ is overwritten by $\sigma _ { \mathrm { n e w } }$ (Line 15-16). Finally, the iteration ends by swapping the trees (Line 17) and in the next iteration the same procedure is executed on the other tree.

## 5 IB-RRT\* algorithm

This section presents our proposed IB-RRT\* algorithm<sup>1</sup>. IB-RRT\* is specifically designed for motion

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 6: Connect($x_1, x_2, T_b$)
1 $x_{\text{new}} \leftarrow \text{Extend}(x_2, x_1)$
2 $X_{\text{near}} \leftarrow \text{NearVertices}(x_{\text{new}}, T_b)$
3 $L_s \leftarrow \text{GetSortedList}(x_1, X_{\text{near}})$
4 $x_{\text{min}} \leftarrow \text{ChooseBestParent}(L_s)$
5 if $x_{\text{min}} \neq \emptyset$ then
6 $E \leftarrow E \cup ((x_{\text{min}}, x_1))$
7 $\sigma_f \leftarrow \text{GeneratePath}(x_{\text{min}}, x_1)$
8 return $\sigma_f$
9 return NULL
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 7: IB-RRT* ($x_{\text{init}}^{\text{a}}, x_{\text{init}}^{\text{b}}$)
1 $V_{\text{a}} \leftarrow \{x_{\text{init}}^{\text{a}}\}; E_{\text{a}} \leftarrow \emptyset; T_{\text{a}} \leftarrow (V_{\text{a}}, E_{\text{a}})$
2 $V_{\text{b}} \leftarrow \{x_{\text{init}}^{\text{b}}\}; E_{\text{b}} \leftarrow \emptyset; T_{\text{b}} \leftarrow (V_{\text{b}}, E_{\text{b}})$
3 $\sigma_{\text{f}} \leftarrow \infty; E \leftarrow \emptyset$
4 Connection $\leftarrow$ True
5 for $i \leftarrow 0$ to $N$ do
6    $x_{\text{rand}} \leftarrow \text{Sample}(i)$
7    $\{X_{\text{near}}^{\text{a}}, X_{\text{near}}^{\text{b}}\} \leftarrow \text{NearVertices}(x_{\text{rand}}, T_{\text{a}}, T_{\text{b}})$
8    if $X_{\text{near}}^{\text{a}} = \emptyset$ &amp; &amp; $X_{\text{near}}^{\text{b}} = \emptyset$ then
9    $\begin{array}{c}\{X_{\text{near}}^{\text{a}}, X_{\text{near}}^{\text{b}}\} \leftarrow \\ \text{NearestVertex}(x_{\text{rand}}, T_{\text{a}}, T_{\text{b}}) \\ \text{Connection} \leftarrow \text{False}\end{array}$
10
11    $L_{\text{s}}^{\text{a}} \leftarrow \text{GetSortedList}(x_{\text{rand}}, X_{\text{near}}^{\text{a}})$
12    $L_{\text{s}}^{\text{b}} \leftarrow \text{GetSortedList}(x_{\text{rand}}, X_{\text{near}}^{\text{b}})$
13    $\{x_{\text{min}}, \text{flag}, \sigma_{\text{f}}\} \leftarrow \\ \quad \text{GetBestTreeParent}(L_{\text{s}}^{\text{a}}, L_{\text{s}}^{\text{b}}, \text{Connection})$
14    if (flag) then
15    $\begin{array}{c}\mathsf{T}_{\mathsf{a}} \leftarrow \text{InsertVertex}(x_{\text{rand}}, x_{\text{min}}, T_{\mathsf{a}}) \\ \mathsf{T}_{\mathsf{a}} \leftarrow \text{RewireVertices}(x_{\text{rand}}, L_{\mathsf{s}}, E_{\mathsf{a}})\end{array}$
16    else
18    $\begin{array}{c}\mathsf{T}_{\mathsf{b}} \leftarrow \text{InsertVertex}(x_{\text{rand}}, x_{\text{min}}, T_{\mathsf{b}}) \\ \mathsf{T}_{\mathsf{b}} \leftarrow \text{RewireVertices}(x_{\text{rand}}, L_{\mathsf{s}}, E_{\mathsf{b}})\end{array}$
20    $E \leftarrow E_{\mathsf{a}} \cup E_{\mathsf{b}}$
21    $V \leftarrow V_{\mathsf{a}} \cup V_{\mathsf{b}}$
22 return ($\{T_{\mathsf{a}}, T_{\mathsf{b}}\} = V, E$)
</div>

![](Qureshi2017Intelligent_figs/cf251a2133d5a977afe9d7ada40bab206c0646a347781e8e1096c12c1987848a.jpg)  
(a) Computing set of near nodes

![](Qureshi2017Intelligent_figs/17ee373fe1cbb91d5446c52013811225d8dca4f652aee3bdf89ab3bdfd87c842.jpg)

![](Qureshi2017Intelligent_figs/abffaf52af269a6b9e5a98149dd60c4317127886c375bb2319389ffa67201bbe.jpg)  
(c) Choosing best parent vertex and rewiring

(b) Choosing best parent  
![](Qureshi2017Intelligent_figs/08c59f783c040777e7010516ca871a5a1ca9fddebb9094aa373e90bf8aa9310d.jpg)  
(d) Connecting trees

![](Qureshi2017Intelligent_figs/57e46efafd6012ce3307e09791bbbbcb43316843947e1cf9e75a8c6b6a532af6.jpg)  
(e) end-to-end path  
Figure 1: Intelligent Bidirectional Trees

planning in complex cluttered environments where exploration of configuration space is dificult. Let the sets of near vertices from tree $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ be denoted by $X _ { \mathrm { n e a r } } ^ { \mathrm { a } }$ and $X _ { \mathrm { n e a r } } ^ { \mathrm { b } } ,$ respectively. The path connecting $x _ { \mathrm { i n i t } } ^ { \mathrm { a } }$ and $x _ { \mathrm { r a n d } }$ is denoted by $\sigma _ { \mathrm { a } } ^ { \prime } : [ 0 , s _ { \mathrm { a } } ]$ while the path connecting $x _ { \mathrm { i n i t } } ^ { \mathrm { b } }$ and $x _ { \mathrm { r a n d } }$ is denoted by $\sigma _ { \mathrm { b } } ^ { \prime } : [ 0 , s _ { \mathrm { b } } ]$ . Algorithm $7$ outlines the implementation of IB-RRT\*. In Algorithm $^ { 7 , }$ the boolean variable Connection represents the feasibility of connecting the two trees while the boolean variable flag indicates the best selected tree. IB-RRT\* builds the bidirectional trees incrementally. It starts by picking a random sample $x _ { \mathrm { r a n d } }$ from the obstaclefree configuration space $X _ { \mathrm { f r e e } }$ i.e., $x _ { \mathrm { r a n d } } ~ \in ~ X _ { \mathrm { f r e e } }$ (Line 6). It then populates the set of near vertices $X _ { \mathrm { n e a r } } ^ { \mathrm { a } } , X _ { \mathrm { n e a r } } ^ { \mathrm { b } }$ for both trees using the NearVertices procedure (Line 7). It should be noted that a ball region centered at $x _ { \mathrm { r a n d } }$ of radius r is formed and the sets of the near vertices from both trees are computed $\mathrm { i . e . , ~ } X _ { \mathrm { n e a r } } ^ { \mathrm { a } } : = \{ v \in V _ { \mathrm { a } } : v \in \mathfrak { B } _ { x _ { \mathrm { r a n d } } , r } \}$ and $X _ { \mathrm { n e a r } } ^ { \mathrm { b } } : = \{ v \in V _ { \mathrm { b } } : v \in \mathfrak { B } _ { x _ { \mathrm { r a n d } } , r } \}$ , as shown in figure 1(a). $X _ { \mathrm { n e a r } } ^ { \mathrm { a } }$ and $X _ { \mathrm { n e a r } } ^ { \mathrm { b } }$ now contain near vertices of $x _ { \mathrm { r a n d } }$ from trees $T _ { a }$ and $T _ { b } .$ , respectively. In case of both sets of near vertices being found empty, these sets are filled with the closest vertex from their respective trees instead, $\mathrm { i . e , }$ the vertex on their respective tree which lies closest to the random sample(Line 8-9). Both sets are then sorted by the GetSortedList procedure (Line 11-12) outlined in Algorithm 2. Once the list is in ascending order, the random vertex $x _ { \mathrm { r a n d } }$ is inserted in the best selected tree (Line 13-19). The procedure BestSelectedTree (explained later in this section) returns the nearest vertex on best selected tree which is eligible to become parent of the random sample.

Additional features included in IB-RRT\* are explained below. The rest of the procedures employed by our algorithm are the same as those outlined in the previous section.

Selecting Best Tree Parent: the operation GetBestTreeParent replaces the ChooseBestParent procedure of the RRT\* algorithm. The implementation of this procedure is outlined in Algorithm 8. Initially the best parent vertex from both the trees is calculated, as shown in figure 1(b). This process (Line 2-9) is similar to ChooseBestParent procedure outlined in algorithm 3. The best selected triplets from each tree $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ are assigned to $\{ x _ { \mathrm { m i n } } ^ { \mathrm { a } } , C _ { \mathrm { m i n } } ^ { \mathrm { a } } , \sigma _ { \mathrm { a } } \} ~ \in ~ L _ { \mathrm { s } } ^ { \mathrm { a } }$ and $\{ x _ { \mathrm { m i n } } ^ { \mathrm { b } } , C _ { \mathrm { m i n } } ^ { \mathrm { b } } , \sigma _ { \mathrm { b } } \} \ \in \ L _ { \mathrm { s } } ^ { \mathrm { b } }$ respectively. Following this, the GetBestTreeParent procedure selects the best tree from amongst $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ on the basis of costs $C _ { \mathrm { m i n } } ^ { \mathrm { a } }$ and $C _ { \mathrm { m i n } } ^ { \mathrm { b } }$ associated with each best selected triplet. The best selected vertex of the best selected tree, i.e. either $x _ { \mathrm { m i n } } ^ { \mathrm { a } }$ or $x _ { \operatorname* { m i n } } ^ { \mathrm { b } } ,$ is then assigned to $x _ { \mathrm { m i n } }$ for the insertion process. For the scenario depicted in Figure 1, tree $T _ { \mathrm { a } }$ is selected as the best tree and therefore $x _ { \mathrm { m i n } } ^ { \mathrm { a } }$ is assigned to $x _ { \mathrm { m i n } }$ as shown in the figure 1c. The boolean variable flag indicates which tree has been selected as the best tree for any single iteration (Line 10-14). The algorithm then attempts to connect the bidirectional trees (Line 15) on the basis of the boolean variable connection. This is explained further on in the paper. The GetBestTreeParent procedure concludes by returning the best vertex x , the boolean flag and, if it exists, the final path $\sigma _ { \mathrm { f } }$ connecting the initial state to the goal region.

Bidirectional Trees Connection: Algorithm 9 gives the pseudocode of the procedure ConnectTrees. Given collision-free paths $\sigma _ { \mathrm { a } } : ~ [ 0 , s _ { \mathrm { a } } ]$ and $\sigma _ { \mathrm { b } } : \sigma .$ $[ 0 , \mathrm { b } ]$ 2 where $\sigma _ { \mathrm { a } } ( 0 ) = x _ { \mathrm { i n i t } } ^ { \mathrm { a } } , \sigma _ { \mathrm { b } } ( \mathrm { \bar { 0 } } ) = x _ { \mathrm { i n i t } } ^ { \mathrm { b } }$ and $\sigma _ { \mathrm { a } } ( s _ { \mathrm { a } } ) = \sigma _ { \mathrm { b } } ( s _ { \mathrm { b } } ) = x _ { \mathrm { r a n d } } .$ This procedure updates the end-to-end collision-free path $\sigma _ { \mathrm { f } } : ~ [ 0 , s ]$ connecting $\sigma _ { \mathrm { f } } ( 0 ) ~ = ~ x _ { \mathrm { i n i t } } ^ { \mathrm { a } }$ and $\sigma _ { \mathrm { f } } ( s ) \ = \ x _ { \mathrm { i n i t } } ^ { \mathrm { b } }$ if the cost of concatenated paths, $c ( \sigma _ { \mathrm { a } } | \sigma _ { \mathrm { b } } )$ , is found to be less than the cost of the existing end-to-end path $c ( \sigma _ { \mathrm { f } } )$ (Line 1-2). Connection between the trees is only successful if the boolean variable connection is true. As mentioned in previous explanation, the occurrence of empty sets for both $X _ { \mathrm { n e a r } } ^ { \mathrm { a } }$ and $X _ { \mathrm { n } } ^ { \mathrm { b } }$ ear causes the procedure NearestVertex to be called (Algorithm 7, Line 7-8). The NearestVertex changes the boolean variable connection to false. Therefore, the boolean connection is true only when the procedure NearVertices populates both sets. This implies that the two trees are connected if ball of region centered at $x _ { \mathrm { r a n d } }$ contains near vertices from both trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } } .$ Hence, unlike the connect heuristic [20], the IB-RRT\* is not greedy since the connection is only made inside the ball region as shown in the figure 1(d). Finally the tree connection generates end-to-end global path, as shown in figure 1(e).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 8: GetBestTreeParent( $L_{s}^{a}, L_{s}^{b}$ , Connection)

1 flag ← True
2 for ( $x_{a}^{\prime}, C_{a}^{\prime}, \sigma_{a}^{\prime}$ ) ∈  $L_{s}^{a}$  do
3    if ObstacleFree( $\sigma_{a}^{\prime}$ ) then
4    { $x_{min}^{a}, C_{min}^{a}, \sigma_{a}$ } ← { $x_{a}^{\prime}, C_{a}^{\prime}, \sigma_{a}^{\prime}$ }
5    Break
6 for ( $x_{b}^{\prime}, C_{b}^{\prime}, \sigma_{b}^{\prime}$ ) ∈  $L_{s}^{b}$  do
7    if ObstacleFree( $\sigma_{b}^{\prime}$ ) then
8    { $x_{min}^{b}, C_{min}^{b}, \sigma_{b}$ } ← { $x_{b}^{\prime}, C_{b}^{\prime}, \sigma_{b}^{\prime}$ }
9    Break
10 if ( $C_{min}^{a} \leq C_{min}^{b}$ ) then
11    $x_{min} \leftarrow x_{min}^{a}$ 
12 else if ( $C_{min}^{b} &lt; C_{min}^{a}$ ) then
13    $x_{min} \leftarrow x_{min}^{b}$ 
14    flag ← False
15 if Connection then
16    $\sigma_{f} \leftarrow ConnectTrees(\sigma_{a}, \sigma_{b})$ 
17 return { $x_{min}, flag, \sigma_{f}$ }

Algorithm 9: ConnectTrees( $\sigma_{a}, \sigma_{b}$ )

1 if  $c(\sigma_{f}) &lt; c(\sigma_{a}|\sigma_{b})$  then
2    $\sigma_{f} \leftarrow \sigma_{a}|\sigma_{b}$ 
3 return  $\sigma_{f}$
</div>

## 6 Analysis

## 6.1 Probabilistic Completeness

In any configuration space, an algorithm is said to be Probabilistically Complete if the probability of finding a path solution, if ones exist, approaches one as the number of samples taken from the configuration space reaches infinity. It is known that RRT is a probabilistically complete algorithm, as its optimal variant $\mathrm { R R T ^ { * } }$ [13]. Since our proposed IB-RRT\* algorithm performs the random sampling function exactly like the aforementioned algorithms and is merely a bidirectional version of RRT\* with intelligent sample insertion, it can be reasonably profered that it also inherits the probabilistic completeness property of RRT\*.

## 6.2 Asymptotic Optimality

It is known that RRT and its variant RRT-Connect do not ensure optimality even if the number of iterations are increased to infinity [13]. However, $\mathrm { R R T ^ { * } }$ is an optimal variant of RRT, ensuring almost-sure convergence to an optimal solution [12]. As explained earlier, IB-RRT\* attempts to connect both trees, $T _ { \mathrm { a } } ~ = ~ \left( V _ { \mathrm { a } } , E _ { \mathrm { a } } \right)$ and $T _ { \mathrm { b } } ~ = ~ ( V _ { \mathrm { b } } , E _ { \mathrm { b } } )$ , in every iteration. A random sample $x _ { \mathrm { r a n d } }$ is used as a point of connection between the two trees (shown in figure 1(d)) if the ball region centered at $x _ { \mathrm { r a n d } }$ is found to contain near vertices from both the trees, i.e., $v _ { \mathrm { a } } \in V _ { \mathrm { a } } : v _ { \mathrm { a } } \in \mathfrak { B } _ { x _ { \mathrm { r a n d } } , r }$ and $v _ { \mathrm { b } } \in V _ { \mathrm { b } } : v _ { \mathrm { b } } \in \mathfrak { B } _ { x _ { \mathrm { r a n d } } , r } . \ \mathrm { A }$ similar procedure is employed by the RRT\* algorithm [12] to connect the random sample with its chosen parent. Since there is no extra connection heuristic required for connection of the two trees and the two trees are generated exactly as the tree generated in the original $\mathrm { R R T ^ { * } }$ algorithm, it can be reasonably proposed that the IB-RRT\* algorithm inherits the asymptotic optimality property of RRT\*.

## 6.3 Rapid Convergence to Optimal Path

This section provides proof of IB-RRT\*’s rapid convergence to the optimal solution and that this algorithm provides faster convergence rates as compared to state of the art algorithms $\mathrm { R R T ^ { * } }$ and $\mathrm { B { - } R R T ^ { * } }$ . For simplicity, the following assumptions are are made:

Assumption 1 (Uniform Sampling) The sampling operation take samples from a configuration space $\bar { X }$ such that the samples are continuously distributed.

Assumption 2 (Cluttered Configuration Space) The configuration space X is cluttered such that the tree initially grows near its initial state $x _ { \mathrm { i n i t } }$ and then incrementally grows towards the unsearched configuration space.

Assumption 3 (Uniformity and Additivity of Cost Function) For a given set of path functions, the cost function must sa $t i s f y \colon \ c ( \sigma _ { 1 } ) \ \leq \ c ( \sigma _ { 1 } | \sigma _ { 2 } ) \ :$ $\begin{array} { r } { c ( \sigma _ { 1 } | \sigma _ { 2 } ) = c ( \sigma _ { 1 } ) + c ( \sigma _ { 2 } ) \forall \sigma _ { 1 } , \sigma _ { 2 } \in \sum _ { \mathrm { f r e e } } . } \end{array}$

Assumption 1 ensures that the sampling operation is not biased or goal directed. Biasing the samples for rapid convergence to the optimal solution is computationally ineficient, specifically in higher dimension configuration spaces [13]. Assumption 2 states that the environment contains obstacles that hinder the expansion of the two trees in the configuration space. Finally, Assumption 3 simply asserts that the longer path has a higher cost than the shorter one.

As mentioned in section II, $\sum _ { \mathrm { f r e e } }$ denote the set of all collision free paths in the tree $T = ( V , E )$ . Let $\sigma _ { i } , \sigma _ { i } ^ { \prime } \in \Sigma _ { \mathrm { f r e e } }$ such that $\boldsymbol { \sigma } _ { i } ^ { \prime }$ is closest to $\sigma _ { i }$ in terms of Euclidean distance function. The following Lemma states that any sampling-based algorithm can provide almost-sure convergence to the optimal path solution if distance variation $\| \sigma _ { i } ^ { \prime } - \sigma _ { i } \|$ approaches zero as the number of iterations approaches infinity.

Lemma 1 ([13]) A sampling-based algorithm ensures asymptotic optimality, such that

$$
\mathbb {P} (\lim _ {i \to \infty} \| \sigma_ {i} ^ {\prime} - \sigma_ {i} \| = 0; \forall \sigma_ {i}, \sigma_ {i} ^ {\prime} \in \sum_ {\mathrm{free}}) =
$$

With lemma 1 following corollary immediate.

Corollary 1 By increasing the number of path variations minimized per iteration, the algorithm can greatly improve its rate of convergence to an optimal solution.

Given a tree $T ~ = ~ ( V , E )$ , random configuration state $x \in X _ { \mathrm { f r e e } }$ and a set of near vertices $X _ { \mathrm { n e a r } }$ inside a ball region $\mathfrak { B } _ { x , r }$ centered at x, the intensity of near vertices around $x ,$ denoted by $\mathrm { J } _ { x }$ , can be defined as:

$$
\mathrm{J} _ {x} := \{\operatorname{card} (X _ {\text {near}}) / \mu (\mathfrak {B} _ {x, r}): X _ {\text {near}} | x = \mathfrak {B} _ {x, r} \cap V \}.
$$

Regarding the intensity of near vertices Lemma 2 is stated as follows:

Lemma 2 If Assumptions 1,2,3 hold, then Intensity $\mathrm { J } _ { x }$ is higher in the regions closer to the point of generation of the tree.

Sketch of Proof: Let $\epsilon \in \mathbb { R } _ { + } . \ X _ { \mathrm { f r e e } }$ is obstaclefree configuration space. $X _ { \mathrm { f r e e } }$ is searched for the set of near neighbors $X _ { \mathrm { n e a r } }$ that lie inside a ball region $\mathfrak { B } _ { x , r }$ of radius $r > 0$ centered at the random state $x \in X _ { \mathrm { f r e e } } .$ Any state $x ^ { \prime } \in X _ { \mathrm { n e a r } }$ can become the parent of $x _ { \mathrm { r a n d } }$ , if it provides a lower cost path connecting $x _ { \mathrm { r a n d } }$ to $x _ { \mathrm { i n i t } }$ than the one provided by all other vertices in $X _ { \mathrm { n e a r } }$ This implies that $\| x - x ^ { \prime } \| = \epsilon ,$ where $\epsilon < r = \gamma ( l o g i / i ) ^ { 1 / n }$ This ensures that the growth of the algorithm presented in this paper is incremental as the tree grows in small incremental distances . For the incremental or wavefront expansion of the trees it is proven that the regions near the point of generation of trees are more dense [23]. Therefore, there is a high probability of having high cardinality of set $X _ { \mathrm { n e a r } } .$ , if the random state lies closer to the point of generation of tree.

Hence, with corollary 1 and Lemma 2 holds the following theorem stating efectiveness of IB-RRT\* is given below.

Theorem 1 IB-RRT\* algorithm converges to optimal solution more quickly as compared to RRT\* and $B { - } R R T ^ { * } $

Sketch of Proof: Given a random configuration $x _ { \mathrm { r a n d } }$ and minimum cost path functions $\sigma _ { \mathrm { a } } [ 0 , s _ { \mathrm { a } } ] : =$ $\{ \sigma _ { \mathrm { a } } ( 0 ) = x _ { \mathrm { i n i t } } ^ { \mathrm { a } } , \sigma _ { \mathrm { a } } ( s _ { \mathrm { a } } ) = x _ { \mathrm { r a n d } } \}$ and $\sigma _ { \mathrm { b } } [ 0 , s _ { \mathrm { b } } ] : =$ $\{ \sigma _ { \mathrm { b } } ( 0 ) = x _ { \mathrm { i n i t } } ^ { \mathrm { b } } , \sigma _ { \mathrm { b } } ( s _ { \mathrm { b } } ) = x _ { \mathrm { r a n d } } \}$ , then insertion process of $\mathrm { I B { - } R R T ^ { * } }$ can be summarized as $\{ x _ { \mathrm { r a n d } } \in V _ { \mathrm { a } }$ $c ( \sigma _ { \mathrm { a } } ) \leq c ( \sigma _ { \mathrm { b } } )$ otherwise $x _ { \mathrm { r a n d } } \in V _ { \mathrm { b } } : c ( \sigma _ { \mathrm { b } } ) < c ( \sigma _ { \mathrm { a } } ) \}$ (Algorithm 8). As the random sample $x _ { \mathrm { r a n d } }$ is always inserted into the tree whose initial state is closer to x , this ensures that the sample is inserted into a region in the configuration space where the intensity of near vertices $\mathrm { J } _ { \mathrm { x } }$ is high. Since the rewiring process explained earlier tries to minimize the distance variation $\| \sigma _ { i } ^ { \prime } - \sigma _ { i } \|$ between any two closest paths in each tree. This is done by checking viability of the random sample $x _ { \mathrm { r a n d } }$ as the parent of each vertex in the set $X _ { \mathrm { n e a r } }$ . If the cost to reach a particular vertex $x ^ { \prime }$ in the near set $X _ { \mathrm { n e a r } }$ through random sample x<sub>rand</sub> is lower then the existing cost, then $x _ { \mathrm { r a n d } }$ becomes the parent of that particular vertex $x ^ { \prime } \in X _ { \mathrm { n e a r } }$ Hence, IB-RRT\* inserts the sample into high intensity regions $\operatorname { J } _ { x } ,$ , maximizing the rewiring process per iteration. This step allows rapid convergence to optimal solution and serves as evidence that $\mathrm { I B { - } R R T ^ { * } }$ provides better convergence rates than both RRT\* and B- $\mathrm { \cdot R R T ^ { * } }$ algorithms. Furthermore, trees connection heuristic employed by $\mathrm { B { - } R R T ^ { * } }$ [11] is partially greedy, similar to the the connect heuristic [20]. It has already been proved that if the bidirectional version of $\mathrm { R R T ^ { * } }$ uses purely RRT-Connect heuristic [20] for the connection of two trees, it is no longer asymptotically optimal [11]. This happens because when only the connect heuristic [20] is used, an edge originating from $T _ { \mathrm { a } }$ for example, tries to reach the closest vertex on $T _ { \mathrm { b } }$ . This implies that near vertices present inside the ball region are never considered for best parent selection. $\mathrm { { \bar { B } { - } R R T ^ { * } } }$ does eventually converge to an optimal solution but the convergence process is slowed down due to its partially greedy characteristic. Nevertheless, compared to $\mathrm { R R T ^ { * } }$ , the $\mathrm { B { - } R R T ^ { * } }$ has faster convergence rate due to its generation of two trees. However, in comparison to $\mathrm { I B { - } R R T ^ { * } }$ , it has significantly less convergence rate. This is later on evident from the experimental results as well.

## 6.4 Computational Complexity

This section compares computational complexities of $\mathrm { I B { - } R R T ^ { * } }$ with complexities of RRT\* and the bidirectional version of RRT. Let $S _ { i } ^ { \mathrm { R R T ^ { * } } }$ and $S _ { i } ^ { \mathrm { B i R R T } }$ denotes the number of processes executed per iteration by $\mathrm { R R T ^ { * } }$ and bidirectional-RRT (BiRRT), respectively. Let $S _ { i } ^ { \mathrm { { O u r s } } }$ denote the number of processes executed by IB-RRT\*. Theorem 2 and 3 propose that the running time of all processes executed per iteration by $\mathrm { I B { - } R R T ^ { * } }$ is a constant times higher than both $\mathrm { R R T ^ { * } }$ and BiRRT.

<table><tr><td>Environment</td><td>Algorithm</td><td> $i_{\text{min}}$ </td><td> $i_{\text{max}}$ </td><td> $i_{\text{avg}}$ </td><td> $t_{\text{min}}(s)$ </td><td> $t_{\text{max}}(s)$ </td><td> $t_{\text{avg}}(s)$ </td><td>C</td><td>Fail</td></tr><tr><td rowspan="3">2D-Cluttered (A) (figures 2 &amp; 3)</td><td>IB-RRT*</td><td>159861</td><td>181521</td><td>162809</td><td>37.9</td><td>42.3</td><td>39.6</td><td>93.1</td><td>0</td></tr><tr><td>B-RRT*</td><td>438785</td><td>463526</td><td>458328</td><td>90.8</td><td>97.8</td><td>95.3</td><td>93.1</td><td>3</td></tr><tr><td>RRT*</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>50</td></tr><tr><td rowspan="3">2D-Cluttered (B) (figures 4 &amp; 5)</td><td>IB-RRT*</td><td>78652</td><td>141936</td><td>95192</td><td>18.9</td><td>33.4</td><td>23.3</td><td>69.4</td><td>0</td></tr><tr><td>B-RRT*</td><td>261716</td><td>375341</td><td>286721</td><td>55.2</td><td>78.2</td><td>60.3</td><td>69.4</td><td>0</td></tr><tr><td>RRT*</td><td>981431</td><td>1219628</td><td>1059268</td><td>168.9</td><td>210.9</td><td>183.4</td><td>69.4</td><td>7</td></tr><tr><td rowspan="3">3D-Multiple Barriers (figure 8)</td><td>IB-RRT*</td><td>193593</td><td>218586</td><td>204321</td><td>45.8</td><td>53.6</td><td>47.8</td><td>81.9</td><td>0</td></tr><tr><td>B-RRT*</td><td>810581</td><td>853248</td><td>838692</td><td>167.3</td><td>178.1</td><td>176.3</td><td>81.9</td><td>4</td></tr><tr><td>RRT*</td><td>1941613</td><td>1978581</td><td>1961825</td><td>329.7</td><td>337.4</td><td>332.2</td><td>81.9</td><td>11</td></tr><tr><td rowspan="3">3D-Narrow Passages (figure 7)</td><td>IB-RRT*</td><td>29651</td><td>34239</td><td>32361</td><td>6.8</td><td>8.2</td><td>7.8</td><td>69.8</td><td>1</td></tr><tr><td>B-RRT*</td><td>46971</td><td>57891</td><td>54916</td><td>9.8</td><td>12.4</td><td>11.3</td><td>69.8</td><td>5</td></tr><tr><td>RRT*</td><td>163872</td><td>168494</td><td>165627</td><td>27.2</td><td>29.4</td><td>28.6</td><td>69.8</td><td>8</td></tr><tr><td rowspan="3">3D-Maze (figure 6)</td><td>IB-RRT*</td><td>148786</td><td>171543</td><td>168932</td><td>33.9</td><td>41.5</td><td>39.8</td><td>299.2</td><td>3</td></tr><tr><td>B-RRT*</td><td>753861</td><td>764926</td><td>758438</td><td>155.3</td><td>161.2</td><td>159.7</td><td>299.2</td><td>7</td></tr><tr><td>RRT*</td><td>2174180</td><td>2189742</td><td>2184761</td><td>368</td><td>372</td><td>371</td><td>299.2</td><td>16</td></tr></table>

Table 1: Experimental results for computing optimal path solution.

![](Qureshi2017Intelligent_figs/ebaae643e2e196ac278b73e8da0f92fdea00b2b12cd09c289e58eaa0dd6680f1.jpg)  
(a) i=7988,t=1.8s,C=95

![](Qureshi2017Intelligent_figs/70a9bcf957a9c060293bd8ba481c1ed12004a45caf254b069998d1de60e242f8.jpg)  
(b) i=22164,t=4.9s,C=93.9

![](Qureshi2017Intelligent_figs/4c4efc7a36fe380e7d126da15added3401fb31b1a3b7cf3f1d82455febf35d52.jpg)  
(c) i=79187,t=18.8s,C=93.4

![](Qureshi2017Intelligent_figs/e506c10f16dad0769dfee5e26fdf4a835d8d4f5939604ba7d682d9ec7d5b9095.jpg)  
(d) i=161437,t=40s,C=93.1  
Figure 2: IB-RRT\* performance in 2-D Environment (A)

![](Qureshi2017Intelligent_figs/de345170f5aa62f48386101315be29df705afb91c47de9f5746aa732d6b79527.jpg)  
(a) $\mathrm { i { = } 1 0 2 0 1 6 , t { = } 1 7 s , C { = } 9 7 . 0 }$

![](Qureshi2017Intelligent_figs/7270ad430b4fffa79d2e297041604ea42c14b325941cec98738d58d842d8f443.jpg)

![](Qureshi2017Intelligent_figs/b9b796242ed6eabeb8958b87ada9ae5e1d95c8e3c6a9b823a2bd58a52b528d28.jpg)  
(b) $\mathrm { i { = } 5 1 0 9 8 2 , t { = } 8 4 s , C { = } 9 6 . 5 }$ (c) $\mathrm { i = 1 5 3 2 1 9 1 , t = 2 5 5 s , C = 9 6 . 3 }$ (d) i=3192640,t=510s,C=96.0

![](Qureshi2017Intelligent_figs/f630517603a9c612e44e2121a3f51c07eae1af21153a36104087cc8cd48562dc.jpg)  
Figure 3: RRT\* performance in 2-D Environment (A)

![](Qureshi2017Intelligent_figs/074cf7160293e2fdeb6e1ae677c0a694ca69144b4681a64e96aa1bd9cc23fc8b.jpg)  
(a) i=1812,t=0.42s,C=83.4

![](Qureshi2017Intelligent_figs/732b365c344196fb8dbcca5401ad4a079e44a9343d1b2d0f0467be00c9765cec.jpg)  
(b) i=5026,t=1.22s,C=75.4

![](Qureshi2017Intelligent_figs/cfa8de10c4dee6beb1a53f94e4fceb6d947adb0c922f702360cb59869bf7238e.jpg)  
(c) i=30641,t=7.8s,C=70.8

![](Qureshi2017Intelligent_figs/a9d5866f98d5681c2e51c76577770ba8f595636cbae604c25a7e1589151ef2cb.jpg)  
(d) i=94865,t=21.6s,C=69.4  
Figure 4: IB-RRT\* performance in 2-D environment (B)

Theorem 2 The computational ratio of IB- $. R R T ^ { * }$ and $R R T ^ { * }$ is such that there exists a constant $\phi _ { 1 }$ i.e.,

$$
\lim _ {i \to \infty} \mathbb {E} \left[ \frac {S _ {i} ^ {\mathrm{Ours}}}{S _ {i} ^ {\mathrm{RRT*}}} \right] \leq \phi_ {1}.
$$

Theorem 3 The computational ratio of $I B { - } R R T ^ { * }$ and BiRRT is such that there exists a constant φ i.e.,

$$
\lim _ {i \to \infty} \mathbb {E} \left[ \frac {S _ {i} ^ {\text { Ours }}}{S _ {i} ^ {\text { BiRRT }}} \right] \leq \phi_ {2}.
$$

Similar to RRT\*, our proposed algorithm calls the procedures Sample and RewireVertices exactly once. The procedure of choosing best parent in $\mathrm { R R T ^ { * } }$ is replaced by FindBestTree in the IB-RRT\* algorithm, which also includes the ConnectTrees procedure. As explained earlier, the ConnectTrees function has negligible computational overhead since it merely concatenates two paths. In Intelligent Bidirectional-RRT\* (IB-RRT\*), for every iteration the procedures NearestVertex and NearVertices are executed for both trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ . It has already been proved that both procedures have to run in logi expected time [12]. Furthermore, while $\mathrm { I B { - } R R T ^ { * } }$ makes its best efort to increase the cardinality of the near vertices, the number of near vertices per tree returned by the procedure NearVertices cannot exceed a constant number [12]. Hence, it can be concluded that the execution of NearestVertex and NearVertices procedures on both trees per iteration adds up a constant computational complexity overhead as compared to RRT\*. Hence, it can be concluded that IB-RRT\* has the same computational complexity as $\mathrm { R R T ^ { * } }$ . The proof for theorem 3 is exactly the same to one provided for the computational ratio of RRT\* and RRT in [12].

## 7 Experimental Results

This section presents simulations performed on a 2.4GHz Intel corei5 processor with 4GB RAM. Here, performance results of our IB-RRT\* algorithm are compared with RRT\* and B-RRT\*. Since exploration of the configuration space by B-RRT\* after a large number of iterations is similar to that of IB-RRT\*, snap shots presented here only depict the IB-RRT\* and $\mathrm { R R T ^ { * } }$ algorithms. This is to better demonstrate the diference between the expansion of trees of the two types of algorithms. For proper comparison, experimental conditions and size of the configuration space were kept constant for all algorithms. Since randomized sampling-based algorithms exhibit large variations in results, the algorithms were run up to 50 times with diferent seed values for each type of environment. Maximum, minimum and average number of iterations i as well as time t utilized by each algorithm to reach the optimal path solution is presented in the Table 1. To restrain the computational time within reasonable limits, the maximum limit for the number of tree nodes was kept at 5 million. The column fail in the table denotes the number of runs for which the corresponding algorithm failed to find an optimal path solution within node limits when executed with diferent seed values for random function. Although, algorithms were able to deter-

![](Qureshi2017Intelligent_figs/5f85041a3b83b54bd39ec39f3e6ef84c8239c1f31e2c10ed0f8046694cffb0b5.jpg)  
(a) i=31971,t=5.61s,C=72.4

![](Qureshi2017Intelligent_figs/28a3503cf4609b42de22782437853548fcb9579285038ef0b8f1b89305127c36.jpg)  
(b) i=74119,t=12.81s,C=71.4

![](Qureshi2017Intelligent_figs/0ee923e86be501418d470bdbe2afb1dc897c2722b9acc1f81ae50dc81813eb44.jpg)  
(c) i=317951,t= 55.6s,C=70.6

![](Qureshi2017Intelligent_figs/84d3410d2e4d4ab0bb1629cdba1c13ef77666d62e0fe708ccc4ae92df1ab710a.jpg)  
,t=184.2s,C=69.4  
i=107186  
Figure 5: RRT\* performance in 2-D environment (B)

mine feasible path solution, this is still considered as a failure, since the table provides comparison for the determination of an optimal path solution only. Figures 2 and 3 illustrate the trees maintained by IB-RRT\* and RRT\* respectively at diferent numbers of iterations. The cost C of the path in terms of Euclidean distance is also indicated at each iterations. Table I summarizes the number of iterations and time consumed by IB-RRT\*, B-RRT\* and RRT\* to reach an optimal path in this problem. It should be noted that the RRT\* algorithm is unable to fully sample the given configuration space and thus fails to converge to the optimal solution within the limit of 5 million iterations. Although both IB-RRT\* and B-RRT\* were successful in finding the optimal solution, B-RRT\* took an extremely large number of iterations to converge in comparison with IB-RRT\*. B-RRT\* utilizes the partial greedy heuristic approach as discussed earlier (algorithm line), this significantly reduces its ability of convergence to optimal path solution. Figures 4 and 5 represent particularly challenging maze type of cluttered 2D test environment. The environment has been set up in such a way that the starting and goal regions, while placed close together, are separated by the maze. All algorithms were tested, figure 4(a) to figure 4(d) and 5(a) to figure 5(d) show the convergence from the initial path solution to the optimal path solution by IB-RRT\* and RRT\*, respectively. For determination of the optimal path, the IB-RRT\* algorithm takes the least number of average iterations $( i _ { \mathrm { a v g } } { = } 9 5 1 9 2 )$ as compared to ${ \mathrm { B } } { \mathrm { - R R T } } ^ { * } ( i _ { \mathrm { a v g } } { = } 2 8 6 7 2 1 )$ and the extraordinarily large number of iterations taken up by RRT\* $( i _ { \mathrm { a v g } } { = } 1 0 5 9 2 6 8 )$ as shown in Table 1.

Figure 8 shows the 3-D environment containing a multiple of barriers which separate the initial state and the goal region. IB-RRT\* determines an optimal path most quickly (i=204321) as compared to B-RRT\* (i=838692) and RRT\* $( i { = } 1 9 6 1 8 2 5 )$ . Although all algorithms utilises uniform sampling heuristic, however, IB-RRT\* maximizes the rewiring process per iteration due to intelligent sample insertion heuristic and hence quickly converges to the optimal path solution as compared to B-RRT\* and RRT\*. Figures 6 and 7 depict diferent scenarios in threedimensional space. Their results are summarized in the Table 1. It can be seen that a similar trend is followed by the algorithms in all environments i.e., IB-RRT\* rapidly converges to the optimal solution followed by B-RRT\* and then RRT\*. Moreover, in the maze problem depicted in Figure 6, RRT\* was unable to sample the area close to the goal region even after an extremely large number of iterations while IB-RRT\* was able to fully explore the space in a few thousand iterations.

Figure 9 summarizes the experimental test results performed in 10 diferent complex cluttered 2D and 3D environments for the comparison of IB-RRT\*, B-RRT\* and RRT\*. The comparison is done in terms of: (a) iterations and time consumed to determine initial path as well as optimal path solution; (b) memory consumed in term of bytes for the determination of optimal path solution (c) convergence rate. From figure 9(a) to figure 9(e), it can be seen that IB-RRT\* consumes lesser iterations, time and memory as compared to $\mathrm { B { - } R R T ^ { * } }$ and $\mathrm { R R T ^ { * } }$ for the determination of feasible path solution. Figure 9(f) provides another type of comparison using boxplot. In this the convergence rate of IB-RRT\*, B-RRT\* and RRT\* are compared in these 10 diferent complex cluttered environments. Let the initial feasible path, denoted by $\sigma _ { i n i t } .$ , is computed in $t _ { \mathrm { i n i t } }$ time while the optimal path solution, denoted as σ , is computed in t time. Then the convergence rate is defined as $\frac { c ( \sigma _ { \mathrm { i n i t } } ) - c ( \sigma ^ { * } ) } { t * - t _ { \mathrm { i n i t } } }$ . Since the process of convergence to the optimal path solution begins after finding initial feasible path solution, convergence rate is calculated after initial path computation. It is clear from the box plot that convergence rates of IB-RRT\* are highest, followed by B-RRT\* and RRT\*. There also exists a sizable diference between the convergence rates of IB-RRT\* and B-RRT\*

![](Qureshi2017Intelligent_figs/73ead1d4b2c68a9390ed0f92f7bab615c06297ff8895c9ab09328f80fa864ef1.jpg)  
(a) IB-RRT\*: i=162491,t=39.5s,C=299.2

![](Qureshi2017Intelligent_figs/31fb92c063624b51030711c11f3208219ebc1d4b7ba95c5634d884bb8fa12cf6.jpg)  
(b) RRT\*: i=2177186,t=376.4s,C=299.2

![](Qureshi2017Intelligent_figs/123d3b4857e7bdbe59aad2333f6f7136f9abe3ef944ca2ee640f345cb87fc1e7.jpg)  
(c) IB-RRT\*: Optimal path solution

![](Qureshi2017Intelligent_figs/4df42964b328f54ae886a5b3f5ea25097072fd8ff6c1765312b613395c83eeea.jpg)  
(d) RRT\*: Optimal path solution  
Figure 6: Performance of IB-RRT\* and RRT\* in Complex Maze Environment

![](Qureshi2017Intelligent_figs/eecc1a6699baef60d17b620f67ef53fbd0dcb3a002b7f3c1b855419203d3794e.jpg)

![](Qureshi2017Intelligent_figs/3d6f19e880bbdbbef5a7d2be30a6788ac80ac85506d5734dd4a530d7f86e690a.jpg)  
(a) IB-RRT\*: i=79483,t=18.9s,C=69.8 (b) RRT\*: i=1364129,t=235.9s,C=69.8

![](Qureshi2017Intelligent_figs/b8690b5728949170a870e92b7f2847bf63d6bdc18361feae37afb5c63a685db1.jpg)  
(c) Optimal path solution  
Figure 7: Sequence of narrow passages

Figure 10 shows the running time ratio of a) IB-RRT\* over BiRRT and b) IB-RRT\* over RRT\* after the execution of each iteration. The running time ratio of algorithm A (AL-A) over algorithm B (AL-B) is defined as the ratio of time consumed by AL-A over the time consumed by AL-B. It can be seen that as the number of iterations increases, the running time ratio reaches a constant value in both cases. Hence, large numbers of iterations imply that the random samples are fully and uniformly distributed in the obstacle-free space. However, before that time, computational complexity of IB-RRT\* remains fairly lower than BiRRT and almost equal to RRT\*. As a matter of fact, in this specific environment, the average amount of time taken by our proposed IB-RRT\* algorithm to determine a viable path to the goal was seen to be barely four times that of BiRRT and 1.4 times that of RRT\*.

## 8 Conclusions and Future work

This paper presents a detailed comparative analysis of performance of our proposed IB-RRT\* algorithm with the existing algorithms RRT\* and B-RRT\*. It is proven both analytically and experimentally that our proposed algorithm i) has almost similar computational complexity as RRT\* and BiRRT; ii) provides almost-sure convergence to the optimal path solution; iii) has the higher convergence rate meaning that it rapidly converges to the optimal solution as compared to both state of the art algorithms RRT\* and B-RRT\*; iv) consumes lesser memory to converge to the optimal solution, as it utilizes lesser iterations and each iteration consumes memory. This paper also presents path planning problems in which the original RRT\* algorithm fails to reach the optimal path solution within reasonable limit of iterations. Experimental results supporting theoretical analysis are also presented in this paper. The proposed algorithm IB- $\mathbf { \cdot R R T ^ { * } }$ allows rapid convergence to optimal solution without tuning of the sampling operation for optimal paths. Therefore, the proposed planner is of importance in the field of real time motion planning. Hence, we anticipate employing IB-RRT\* for online motion planning of animated characters in complex 3-D environments.

## References

[1] R. A. Brooks and T. Lozano-Perez. A subdivision algorithm in configuration space for findpath with rotation. 1982.

[2] J. Canny. The complexity of robot motion planning. The MIT press, 1988.

[3] H. Chang and T.-Y. Li. Assembly maintainability study with motion planning. In Robotics and Automation, 1995. Proceedings., 1995 IEEE International Conference on, volume 1, pages 1012–1019. IEEE, 1995.

[4] P. C. Chen and Y. K. Hwang. Sandros: a dynamic graph search algorithm for motion planning. Robotics and Automation, IEEE Transactions on, 14(3):390–403, 1998.

[5] M. Elbanhawi and M. Simic. Sampling-based robot motion planning: a review. IEEE Access, 2:56–77, 2014.

[6] I. Garcia and J. P. How. Improving the eficiency of rapidly-exploring random trees using a

![](Qureshi2017Intelligent_figs/b26df5cca3d926f093e577dd228da426718682dbc3194063e85d335f231b2906.jpg)  
(a) IB-RRT\*: i=186731,t=45.4s,C=81.9

![](Qureshi2017Intelligent_figs/b3df3ded155c3f9b4e4149566c56b366d32559a3a45211ae7bc6e6febdc6cdcb.jpg)  
(b) RRT\*: i=2106391,t=364s,C=81.9

![](Qureshi2017Intelligent_figs/0582893d7b8ab99151c3197f2b0b045e44d9b51f5c450d94baa8434cfb18b69f.jpg)  
(c) Optimal path solution

Figure 8: Sequence of complex barriers.  
![](Qureshi2017Intelligent_figs/375e735b9b6919f9eb4543fdba767cad39882f471c2a82340624c312eeb9e99f.jpg)  
(a) Iterations used to find initial feasible path solution.

![](Qureshi2017Intelligent_figs/07fee220471e904e218f2d86ef03b0cfbd5aeaf82652043a0c06542f4d06f94c.jpg)

![](Qureshi2017Intelligent_figs/a21905fe2f8385e482a917b8adb6c3c251f97db38b07abcd8d75dccca0ded04a.jpg)

(b) Time consumed to find initial feasible path solution.  
![](Qureshi2017Intelligent_figs/bd4ee007b10b2a020e9d1dd15c251130d5ec789ce8654c19b357c023252f04ad.jpg)

(c) Iterations used to find optimal path solution.  
![](Qureshi2017Intelligent_figs/acaba6486593f672741280ce71ebfd18326034a04e00468addbd4f9cd0d87ce9.jpg)  
(e) Memory consumed to find optimal path solution.

(d) Time used to find optimal path solution.  
![](Qureshi2017Intelligent_figs/77ee332208214dfcf31a42f59283cf148d33f3fa3408f59eb1e069af77df5c94.jpg)  
(f) Convergence rate comparison.  
Figure 9: Comparison of IB-RRT\*, B-RRT\* and RRT\* in 10 complex cluttered environments.

![](Qureshi2017Intelligent_figs/842fffbf3b0d680efab5b8c85245dc6b26808a50fb0a30e64c28c5de70cb1b69.jpg)  
(a)

![](Qureshi2017Intelligent_figs/19054a6c91caaf45138745665cc1bd607f8d7e33d09e330051a53693ad54c76a.jpg)  
(b)  
Figure 10: Running time ratio of (a) IB-RRT\* over BiRRT (b) IB-RRT\* over RRT\*.

potential function planner. In Decision and Control, 2005 and 2005 European Control Conference. CDC-ECC’05. 44th IEEE Conference on, pages 7965–7970. IEEE, 2005.

[7] M. Girard and A. A. Maciejewski. Computational modeling for the computer animation of legged figures. In ACM SIGGRAPH Computer Graphics, volume 19, pages 263–270. ACM, 1985.

[8] T. M. Howard, C. J. Green, and A. Kelly. State space sampling of feasible motions for high performance mobile robot navigation in highly constrained environments. In Field and Service Robotics, pages 585–593. Springer, 2008.

[9] R. D. Howe and Y. Matsuoka. Robotics for surgery. Annual Review of Biomedical Engineering, 1(1):211–240, 1999.

[10] G. E. Jan, C.-C. Sun, W. C. Tsai, and T.-H. Lin. An shortest path algorithm based on delaunay triangulation. Mechatronics, IEEE/ASME Transactions on, 19(2):660–666, 2014.

[11] M. Jordan and A. Perez. Optimal bidirectional rapidly-exploring random trees. Technical Report MIT-CSAIL-TR-2013-021, CSAIL, MIT, Cambridge, MA, August 2013.

[12] S. Karaman and E. Frazzoli. Incremental sampling-based algorithms for optimal motion planning. arXiv preprint arXiv:1005.0416, 2010.

[13] S. Karaman and E. Frazzoli. Samplingbased algorithms for optimal motion planning.

The International Journal of Robotics Research, 30(7):846–894, 2011.

[14] L. Kavraki and J.-C. Latombe. Randomized preprocessing of configuration for fast path planning. In Robotics and Automation, 1994. Proceedings., 1994 IEEE International Conference on, pages 2138–2145. IEEE, 1994.

[15] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars. Probabilistic roadmaps for path planning in high-dimensional configuration spaces. Robotics and Automation, IEEE Transactions on, 12(4):566–580, 1996.

[16] O. Khatib. Real-time obstacle avoidance for manipulators and mobile robots. The international journal of robotics research, 5(1):90–98, 1986.

[17] D. Kim, J. Lee, and S.-e. Yoon. Cloud rrt: Sampling cloud based rrt. In Proc. IEEE Int. Conf. Robot. Autom, 2014.

[18] Y. Koren and J. Borenstein. Potential field methods and their inherent limitations for mobile robot navigation. In Robotics and Automation, 1991. Proceedings., 1991 IEEE International Conference on, pages 1398–1404. IEEE, 1991.

[19] D. Kuan, J. Zamiska, and R. A. Brooks. Natural decomposition of free space for path planning. In Robotics and Automation. Proceedings. 1985 IEEE International Conference on, volume 2, pages 168–173. IEEE, 1985.

[20] J. J. Kufner Jr and S. M. LaValle. Rrt-connect: An eficient approach to single-query path planning. In Robotics and Automation, 2000. Proceedings. ICRA’00. IEEE International Conference on, volume 2, pages 995–1001. IEEE, 2000.

[21] J.-C. Latombe. ROBOT MOTION PLAN-NING.: Edition en anglais. Springer, 1990.

[22] J.-C. Latombe. Motion planning: A journey of robots, molecules, digital actors, and other artifacts. The International Journal of Robotics Research, 18(11):1119–1128, 1999.

[23] S. M. LaValle. Rapidly-exploring random trees a ew tool for path planning. 1998.

[24] S. M. LaValle. Planning algorithms. Cambridge university press, 2006.

[25] M. Likhachev, D. Ferguson, G. Gordon, A. Stentz, and S. Thrun. Anytime search in dynamic graphs. Artif. Intell., 172(14):1613–1643, Sept. 2008.

[26] S. R. Lindemann and S. M. LaValle. Incrementally reducing dispersion by increasing voronoi bias in rrts. In Robotics and Automation, 2004. Proceedings. ICRA’04. 2004 IEEE International Conference on, volume 4, pages 3251– 3257. IEEE, 2004.

[27] S. R. Lindemann and S. M. LaValle. Current issues in sampling-based motion planning. In Robotics Research, pages 36–54. Springer, 2005.

[28] T. Lozano-P´erez and M. A. Wesley. An algorithm for planning collision-free paths among polyhedral obstacles. Communications of the ACM, 22(10):560–570, 1979.

[29] A. Perez, S. Karaman, A. Shkolnik, E. Frazzoli, S. Teller, and M. R. Walter. Asymptoticallyoptimal path planning for manipulation using incremental sampling-based algorithms. In Intelligent Robots and Systems (IROS), 2011 IEEE/RSJ International Conference on, pages 4307–4313. IEEE, 2011.

[30] M. Pivtoraiko and A. Kelly. Kinodynamic motion planning with state lattice motion primitives. In Intelligent Robots and Systems (IROS), 2011 IEEE/RSJ International Conference on, pages 2172–2179. IEEE, 2011.

[31] M. Pivtoraiko, R. A. Knepper, and A. Kelly. Diferentially constrained mobile robot motion planning in state lattices. Journal of Field Robotics, 26(3):308–333, 2009.

[32] A. H. Qureshi, K. F. Iqbal, S. M. Qamar, F. Islam, Y. Ayaz, and N. Muhammad. Potential guided directional-rrt\* for accelerated motion planning in cluttered environments. In Mechatronics and Automation (ICMA), 2013 IEEE International Conference on, pages 519– 524. IEEE, 2013.

[33] A. H. Qureshi, S. Mumtaz, K. F. Iqbal, B. Ali, Y. Ayaz, F. Ahmed, M. S. Muhammad, O. Hasan, W. Y. Kim, and M. Ra. Adaptive potential guided directional-rrt. In Robotics and Biomimetics (ROBIO), 2013 IEEE International Conference on, pages 1887–1892. IEEE, 2013.

[34] A. H. Qureshi, S. Mumtaz, K. F. Iqbal, Y. Ayaz, M. S. Muhammad, O. Hasan, W. Y. Kim, and M. Ra. Triangular geometry based optimal motion planning using rrt\*-motion planner. In Advanced Motion Control (AMC), 2014 IEEE 13th International Workshop on, pages 380–385. IEEE, 2014.

[35] J. T. Schwartz and M. Sharir. On the piano movers problem. ii. general techniques for computing topological properties of real algebraic manifolds. Advances in applied Mathematics, 4(3):298–351, 1983.