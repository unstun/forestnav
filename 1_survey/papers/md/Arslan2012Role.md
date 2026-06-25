---
citation_key: Arslan2012Role
arxiv_id: 1204.6453
arxiv_url: "https://arxiv.org/abs/1204.6453"
title: "The Role of Vertex Consistency in Sampling-based Algorithms for Optimal Motion Planning"
authors_short: "Oktay Arslan et al."
year: 2012
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T10:07:20Z
origin: ai+web
reviewed: false
---

# The Role of Vertex Consistency in Sampling-based Algorithms for Optimal Motion Planning

Oktay Arslan<sup>∗</sup>

Panagiotis Tsiotras<sup>†</sup>

## Abstract

Motion planning problems have been studied by both the robotics and the controls research communities for a long time, and many algorithms have been developed for their solution. Among them, incremental sampling-based motion planning algorithms, such as the Rapidlyexploring Random Trees (RRT), and the Probabilistic Road Maps (PRM) have become very popular recently, owing to their implementation simplicity and their advantages in handling high-dimensional problems. Although these algorithms work very well in practice, the quality of the computed solution is often not good, i.e., the solution can be far from the optimal one. A recent variation of RRT, namely the RRT algorithm, bypasses this drawback of the traditional RRT algorithm, by ensuring asymptotic optimality as the number of samples tends to infinity. Nonetheless, the convergence rate to the optimal solution may still be slow. This paper presents a new incremental sampling-based motion planning algorithm based on Rapidly-exploring Random Graphs (RRG), denoted RRT<sup>#</sup> (RRT “sharp”) which also guarantees asymptotic optimality but, in addition, it also ensures that the constructed spanning tree of the geometric graph is consistent after each iteration. In consistent trees, the vertices which have the potential to be part of the optimal solution have the minimum cost-come-value. This implies that the best possible solution is readily computed if there are some vertices in the current graph that are already in the goal region. Numerical results compare with the RRT algorithm.

Keywords: optimal motion planning, RRT, RRG, RRT<sup>∗</sup>, RRT<sup>#</sup>, vertex consistency, consistent tree.

## 1 Introduction

Motion planning problems are crucial for the realization of truly autonomous vehicles and robots. Many approaches have been proposed in the literature (see for example, the excellent books by LaValle [15] and Choset et al [1]). A bottleneck in most motion planning problems, especially those involving systems with high state dimensionality, is the computational overhead associated with discretizing (i.e., gridding) the state space. Hence, deterministic searches [5] are impractical for high dimensional state spaces. Probabilistic roadmap methods [2, 10, 22, 11], [1, Ch. 7], as well as methods that use rapidly exploring random trees (RRTs) [16, 17, 6, 3, 21], are among the most popular. They can address the vehicle’s kinematic and dynamic constraints during motion planning in high dimensional state spaces. In these methods, random samples of the obstacle-free space are connected to each other by feasible trajectories, and the resulting graph is searched for a sequence of connected samples from the initial state to the goal state. Sampling-based algorithms require eficient low-level collision detection and trajectory planning algorithms to find collision-free trajectories between diferent samples [17].

Incremental sampling-based algorithms were first proposed by Kavraki during the late 1990s. The so-called Probabilistic Road Map (PRM) was successfully implemented to solve multi-query motion planning problems and gained a lot of attention, both in industry and academia [12]. In PRM a graph of the environment is constructed by taking random samples from the configuration space of the robot and testing them to determine whether they belong to the free space. The PRM algorithm uses a local planner that attempts to find a feasible path between the sampled points. Once a reasonable graph is constructed, the initial and the goal states are added to the graph, and the optimal path is computed using a graph search algorithm.

Another important class of incremental sampled-based motion planning algorithm is the Rapidlyexploring Random Tree (RRT) and its numerous variants [17]. RRTs have achieved great success in solving single-query motion planning problems in many real-time applications. However, the quality of RRT-based algorithms is often poor (i.e., highly suboptimal). As a result, a lot of effort has been devoted to the development of heuristic techniques in order to refine the quality of the solution obtained from RRTs. However, it has been recently shown that the best path returned by RRTs when the algorithm converges is almost always (i.e., with probability one) far from optimal [9]. This has renewed the interest to develop incremental sampled-based algorithms for motion-planning problems with optimality guarantees. In [7] the authors proposed the Rapidlyexploring Random Graphs (RRG) algorithm, which has asymptotic optimality properties, that is, it ensures that the optimal path will be found as the number of samples tends to infinity. Based on RRG, the same authors later proposed a new algorithm, namely RRT<sup>∗</sup> that extracts a tree from the graph constructed by RRG [8, 9].

In this paper we present a new incremental sampling-based motion planning algorithm based on RRG, denoted RRT<sup>#</sup>(RRT “sharp”), which also guarantees asymptotic optimality but, in addition, it also ensures that, at each step, the constructed spanning tree of the graph is consistent. Vertex consistency (see Section 2) implies that the accumulated cost-to-come of each vertex equals to the optimal cost-to-come. This allows us classify the vertices according to their potential of being part of the optimal path, and thus to quickly identify the region where the optimal solution is more likely to be found. This information can be subsequently used to improve the speed of convergence of the standard RRT algorithm, as well as in order to more eficiently explore the obstacle-free space. Three variants of the baseline RRT<sup>#</sup> algorithm are proposed that take advantage of this vertex classification to speed up convergence.

The organization of the paper is as follows: The problem formulation is given in the next section. In Section 3, an overview of the RRT<sup>#</sup> algorithm is introduced. The fundamental concepts and primitive functions used in the RRT<sup>#</sup> algorithm are explained. In Section 4, each step of the proposed approach is explained in detail, along with the pseudo-code of the algorithm and the main procedures used in the main algorithm. In Sections 5, simulation results are used to compare the solutions of the proposed approach with the well-known RRT<sup>∗</sup> algorithm. In Section 6, several variants of the baseline algorithm are presented by using simple vertex rejection techniques and improvements are demonstrated by doing extensive simulations in the subsequent section. We conclude the paper with some possible extensions for future work.

## 2 Problem Formulation

## 2.1 Notation and Definitions

Let X denote the state space, which is assumed to be an open subset of $\mathbb { R } ^ { d }$ , where $d \in \mathbb { N }$ with $d \geq 2$ . Let the obstacle region and the goal region be denoted by $\mathcal { X } _ { \mathrm { o b s } }$ and $\mathcal { X } _ { \mathrm { g o a l } }$ , respectively. The obstacle-free space is defined by $\chi _ { \mathrm { f r e e } } = \chi \setminus \chi _ { \mathrm { o b s } }$ . Let the initial state be denoted by $x _ { \mathrm { i n i t } } \in \mathcal { X } _ { \mathrm { f r e e } }$ The neighborhood of a state $x \in \mathcal { X }$ is defined as the open ball of radius $r \in \mathbb { R } _ { + }$ centered at $x ,$ , that is, $B _ { r } ( { \boldsymbol { x } } ) = \{ { \boldsymbol { x } } ^ { \prime } \in \mathcal { X } : \| { \boldsymbol { x } } - { \boldsymbol { x } } ^ { \prime } \| < r \}$ . Let $\mathcal { G } = ( V , E )$ denote a graph, where V and $E \subseteq V \times V$ are finite sets of vertices and edges, respectively. In the sequel, we will use graphs to represent the connections between a (finite) set of points selected randomly from $\chi _ { \mathrm { f r e e } }$ . With a slight abuse of notation, we will use x to denote both the point in the space X and the corresponding vertex in the graph.

Geometric r-disc graph: Let $V \subset \mathbb { R } ^ { d }$ be a finite set, and $r \geq 0$ . A geometric r-disc graph $\mathcal { G } ( V ; r ) = ( V , E )$ in d dimensions is an undirected graph with vertex set V and edge set $E =$ $\{ ( u , v ) : u , v \in \mathcal { V }$ and $\| u - v \| < r \big \}$

Successor vertices: Given a vertex $v \in V$ , the set-valued function succ $: ( \mathcal G , v ) \mapsto V ^ { \prime } \subseteq V$ returns the vertices in V that can be reached from vertex v,

$$
\operatorname{succ} (\mathcal {G}, v) := \{u \in V: (v, u) \in E \}
$$

Predecessor vertices: Given a vertex $v \in V$ in a directed graph $\mathcal { G } ~ = ~ ( V , E )$ , the function pred : $( \mathcal { G } , v ) \mapsto V ^ { \prime } \subseteq V$ returns the vertices in V that are the tails of the edges going into v,

$$
\operatorname{pred} (\mathcal {G}, v) := \{u \in V: (u, v) \in E \}
$$

Parent vertex : Given a vertex $v \in V$ , the function parent $: v \mapsto u$ returns the unique vertex $u \in V$ such that $( u , v ) \in E$ and $u \in { \tt p r e d } ( \mathcal { G } , v )$

Spanning tree: Given the graph $\mathcal { G } = ( V , E )$ , a spanning tree of G can be defined such that $\mathcal { T } = ( V _ { s } , E _ { s } )$ , where $V _ { s } = V$ and $E _ { s } = \{ ( u , v ) : u , v \in V , ( u , v ) \in E$ and parent $( v ) = u \}$

Edge cost value: Given an edge $e = ( u , v ) \in E$ , the function ${ \mathsf { c } } : e \mapsto r$ returns a non-negative real number. Then $\mathsf { c } ( u , v )$ where $v \in { \mathsf { s u c c } } ( { \mathcal G } , u )$ is the cost incurred by moving from u to v. Costto-come value: Given a vertex $v \in V$ , the function $\mathbf { g } : v \mapsto r$ returns a non-negative real number $r ,$ which is the cost of the path to v from a given initial state $x _ { \mathrm { i n i t } } \in \mathcal { X } _ { \mathrm { f r e e } }$ . Let $\boldsymbol { \mathsf { g } } ^ { * } ( \boldsymbol { v } )$ be the optimal cost-to-come value of the vertex v. The optimal cost-to-come satisfies the following relationship:

$$
\mathbf {g} ^ {*} (v) = \left\{ \begin{array}{l l} 0, & \text {if v = x_{init}}, \\ \min _ {u \in \operatorname * {p r e d} (\mathcal {G}, v)} (\mathbf {g} ^ {*} (u) + \mathsf {c} (u, v)), & \text {otherwise}. \end{array} \right.
$$

Each vertex v is associated with two estimates of the optimal cost-to-come value $\boldsymbol { \mathsf { g } } ^ { * } ( \boldsymbol { v } )$ , namely, $\mathbf { g } ( v ) \ \mathrm { ( g \mathrm { - v a l u e ) } }$ and lmc(v) (locally minimum cost-to-come estimate, or lmc-value). The $\mathtt { l m c } ( v )$ is the best estimate of the cost-to-come of the vertex v, computed based on the g-value of the vertices in the predecessor set pred(v). The lmc-value (also called rhs-value in [13]) is a one-step ahead lookahead value based on the g-value and is thus potentially better informed than the g-value of the vetrex. The lmc-value satisfies the following relationship

$$
\operatorname{lmc} (v) = \left\{ \begin{array}{l l} 0, & \text {if v = x_{init}}, \\ \min _ {u \in \operatorname * {p r e d} (\mathcal {G}, v)} (\mathsf {g} (u) + \mathsf {c} (u, v)), & \text {otherwise}. \end{array} \right.
$$

Heuristic value: Given a vertex $v \in V$ , and a goal region $\chi _ { \mathrm { g o a l } }$ , the function h : $( v , \mathcal { X } _ { \mathrm { g o a l } } ) \mapsto r \in$ <sup>R</sup> returns an estimate of the optimal cost from v to $\chi _ { \mathrm { g o a l } } ;$ ; it is 0 if $v \in \mathcal { X } _ { \mathrm { g o a l } }$ . It is an admissible heuristic if it never overestimates the actual cost of reaching $\chi _ { \mathrm { g o a l } }$ . In this paper, we always assume an admissible heuristic. It is well known that inadmissible heuristics can be used to speed-up the algorithm, but they lead to suboptimal paths [19].

Relevant region: Let $x _ { \mathrm { g o a l } } ^ { \ast } \in \mathcal { X } _ { \mathrm { g o a l } }$ be the point in the goal region that has the lowest optimal cost-to-come value in $\chi _ { \mathrm { g o a l } }$ , i.e., ${ x _ { \mathrm { g o a l } } ^ { * } = \mathrm { a r g m i n } _ { x \in { \mathcal { X } _ { \mathrm { g o a l } } } } { \mathbf { g } ^ { * } } ( x ) }$ . The relevant region of $\chi _ { \mathrm { f r e e } }$ is the set of points x for which the optimal cost-to-come value of $x ,$ plus the estimate of the optimal cost moving from x to $\mathcal { X } _ { \mathrm { g o a l } }$ is less than the optimal cost-to-come value of $x _ { \mathrm { g o a l } } ^ { * }$ , that is,

$$
\mathcal {X} _ {\text { rel }} = \{x \in \mathcal {X} _ {\text { free }}: \mathrm{g} ^ {*} (x) + \mathrm{h} (x) <   \mathrm{g} ^ {*} (x _ {\text { goal }} ^ {*}) \}
$$

Points that lie in the $\mathcal { X } _ { \mathrm { r e l } }$ have the potential to be part of the optimal path starting at $x _ { \mathrm { i n i t } }$ and reaching $\mathcal { X } _ { \mathrm { g o a l } }$

Key value: Given a vertex $v \in V$ , the function Key $: v \mapsto k$ returns a real vector $k \in \mathbb { R } ^ { 2 }$ , whose components are $k _ { 1 } ( v ) = \mathrm { m i n } ( \mathbf { g } ( v ) , \mathrm { 1 m c } ( v ) ) + \mathtt { h } ( v )$ and $k _ { 2 } ( v ) = \operatorname* { m i n } ( \mathbf { g } ( v ) , \mathtt { l m c } ( v ) )$ , respectively. Components of the keys correspond to the f-values and g-values in the $\mathrm { A } ^ { * }$ algorithm, respectively [18].

Promising vertices: Let $v _ { \mathrm { g o a l } } ^ { * } \in \ V$ be the vertex that has the lowest key value, i.e., $v _ { \mathrm { g o a l } } ^ { * } =$ $\mathrm { a r g m i n } _ { v \in V \cap \mathcal { X } _ { \mathrm { g o a l } } } \mathsf { K e y } ( v )$ . The promising vertices $V _ { \mathrm { p r o m } } \subseteq V$ is the set of vertices that have better key value than $v _ { \mathrm { g o a l } } ^ { * } ,$ that is,

$$
V _ {\text { prom }} = \{v \in V: \operatorname{Key} (v) \prec \operatorname{Key} (v _ {\text { goal }} ^ {*}) \}
$$

Priority $o f$ vertices: The priority of vertices in the queue is the same as the priority of their associated keys, and the precedence relation between keys is determined according to lexicographical ordering. Given two keys $k , k ^ { \prime } \in \mathbb { R } ^ { 2 }$ , the Boolean function $\preccurlyeq : ( k , k ^ { \prime } ) \mapsto \{ \mathtt { F a l s e } , \mathtt { T r u e } \}$ returns True if and only if either $k _ { 1 } < k _ { 1 } ^ { \prime }$ or $( k _ { 1 } = k _ { 1 } ^ { \prime }$ and $k _ { 2 } \leq k _ { 2 } ^ { \prime } )$ , and False otherwise.

Consistency: A vertex $v \in V$ is called locally consistent if and only if its g-value equals its lmc-value [13]. Otherwise, it is an inconsistent vertex. The notion of consistency is very important because it allows one to update cost-to-come values of all vertices by propagating the efects of the changes in the topology of the graph. This way, an incremental search can reuse information from the previous searches, thus speeding up the whole algorithm. The lmc-value always keeps the best up-to-date estimate of the cost-to-come value based on the current topology of the graph, whereas the g-value keeps an estimate of the cost-to-come value computed from a previous topology of the graph. Equality of the ${ \mathrm { g } } _ { - }$ and lmc-values of a vertex implies that the changes in the topology of the graph will not efect the cost-to-come value of that vertex, that is, the topology of the graph is consistent with its previous configuration in the locality of the vertex.

A tree $\mathcal { T } = ( V _ { s } , E _ { s } )$ is called a consistent tree if and only if all of its promising vertices are consistent.

The g-value of all vertices equals to their respective optimal cost-to-come value if and only if all vertices are locally consistent [13]. The g-values have the following form when all vertices are locally consistent

$$
\mathsf {g} (v) = \left\{ \begin{array}{l l} 0, & \text {if v = x_{init}}, \\ \min _ {u \in \mathsf {p r e d} (\mathcal {G}, v)} (\mathsf {g} (u) + \mathsf {c} (u, v)), & \text {otherwise}. \end{array} \right.
$$

Then, the shortest path from $x _ { \mathrm { i n i t } } \in \mathcal { X } _ { \mathrm { f r e e } }$ to any vertex $v \in V$ can be found by starting at v and traversing iteratively from the current vertex $u \in V$ to any of its predecessor $u ^ { \prime } \in \mathsf { p r e d } ( \mathcal { G } , u )$ that minimizes $\mathtt { g } ( u ^ { \prime } ) + \mathtt { c } ( u ^ { \prime } , u )$ (ties can be broken arbitrarily), until $x _ { \mathrm { i n i t } }$ is reached.

## 2.2 Problem Definition

The proposed $\mathrm { R R T } ^ { \# }$ algorithm solves the following motion planning problem: Given a bounded and connected open set $\boldsymbol { \mathcal { X } } \subset \mathbb { R } ^ { d }$ , and the sets $\chi _ { \mathrm { f r e e } }$ and $\mathcal { X } _ { \mathrm { o b s } } = \mathcal { X } \backslash \mathcal { X } _ { \mathrm { f r e e } } .$ , and given an initial point $x _ { \mathrm { i n i t } } \in \mathcal { X } _ { \mathrm { f r e e } }$ and a goal region $\chi _ { \mathrm { g o a l } } \subset \mathcal { X } _ { \mathrm { f r e e } }$ , find the minimum-cost path connecting $x _ { \mathrm { i n i t } }$ to the goal region $\chi _ { \mathrm { g o a l } }$ . If no such path exists, then report that no solution is possible.

## 3 The $\mathrm { R R T } ^ { \# }$ Algorithm - Overview

A brief description of each function used in the $\mathrm { R R T } ^ { \# }$ algorithm is given below.

Sampling: Sample $: \mathbb { N }  \mathcal { X } _ { \mathrm { f r e e } }$ is a function that returns independent, identically distributed (i.i.d) samples from $\chi _ { \mathrm { f r e e } }$

Nearest neighbor : Nearest is a function that returns a point from a given finite set $V .$ , which is the closest to a given point x in terms of a given distance function.

Near vertices: Near is a function that returns n number of points from a given finite set $V ,$ which is the closest to a given point x in terms of a given distance function.

Steering: Steer is a function that returns the closest point in a ball centered around a given state x to another given point $x _ { \mathrm { n e w } }$

Collision checking: Given two points, the Boolean function ObstacleFree checks whether the minimum distance path connecting these two points belongs to $\chi _ { \mathrm { f r e e } }$ . It returns True if the line segment is a subset of the $\chi _ { \mathrm { f r e e } }$

Tree extension: Extend is a function that extends the nearest vertex of the tree T towards the randomly sampled point $x _ { \mathrm { r a n d } }$

Reducing inconsistency: Given a graph $\mathcal { G } = ( V , E )$ , a corresponding spanning tree $\mathcal { T } = ( V _ { s } , E _ { s } )$ where $V _ { s } = V$ and $E _ { s } \subset V \times V$ and a goal region $\chi _ { \mathrm { g o a l } } \subset \mathcal { X } _ { \mathrm { f r e e } }$ , the function ReduceInconsistency : $( \mathcal G , T , \chi _ { \mathrm { g o a l } } ) \mapsto ( \mathcal G , T ^ { \prime } )$ operates on the inconsistent vertices of the tree $\tau$ iteratively, and continues until the tree becomes consistent, that is, all vertices of the tree that are promising (see Section 4) are consistent. The ReduceInconsistency function is used to propagate the efects of the topological changes in the graph $\mathcal { G }$ as new vertices are added with each iteration.

A priority queue is used to sort all of the inconsistent vertices of the tree $\tau$ based on their respective key values. The following functions are defined to manage the priority queue.

Update queue: Given a vertex $v \in V$ , the function UpdateQueue changes the content of the queue based on the g- and lmc-values of the vertex v. If the vertex v is inconsistent, then it is either inserted into the queue or its priority in the queue is updated based on its up-to-date key value if it is already inside the queue. Otherwise, the vertex is removed from the queue if it is a consistent vertex.

Find minimum: The function f indmin() returns the vertex with the highest priority of all vertices in the queue, i.e., the vertex of minimum key value.

Remove a vertex : Given a vertex $v \in V$ , the function remove() deletes the vertex v from content of the queue.

Update priority: Given a vertex $v \in V$ , and a key value k, the function update() changes the priority of the vertex v in priority queue q, i.e., it reassigns the key value of the vertex v with the new given key value $k .$

Inserting a vertex : Given a vertex $v \in V$ , and a key $k ,$ the function insert() adds the vertex v with the key value k into queue.

## 4 The RRT<sup>#</sup> Algorithm - Details

The body of the $\mathrm { R R T } ^ { \# }$ algorithm is given in Algorithm 1 and it is similar to the other RRT-variants (RRT, RRG, RRT<sup>∗</sup>, etc) with the notable exception that it keeps track of vertex consistency using the key values of all current vertices in the graph. One of the important diference between the $\mathrm { R R T ^ { * } }$ and $\mathrm { R R T } ^ { \# }$ algorithms is that all vertices in the tree computed by the $\mathrm { R R T ^ { * } }$ algorithm have a uniform type based on their finite cost-to-come value, whereas in the $\mathrm { R R T } ^ { \# }$ algorithm the vertices have diferent types based on their pair of estimates of the cost-to-come value. In the $\mathrm { R R T } ^ { \# }$ algorithm, each vertex v can be classified in one of the following four categories based on the values of its $( \mathbf { g } ( v ) , \mathtt { l m c } ( v ) )$ pair.

• Consistent with finite key value: $\mathbf { g } ( v ) < \infty , \mathtt { l m c } ( v ) < \infty$ and $\mathtt { g } ( v ) = \mathtt { l m c } ( v )$

• Consistent with infinite key value: $\mathbf { g } ( v ) = \infty , \mathtt { l m c } ( v ) = \infty$

• Inconsistent with finite key value: $\begin{array} { r } { \mathbf { g } ( v ) < \infty , } \end{array}$ , lmc $( v ) < \infty$ and $\mathtt { g } ( v ) \neq \mathtt { l m c } ( v )$

• Inconsistent with infinite g-value and finite lmc-value: $\mathbf { g } ( v ) = \infty , \mathtt { l m c } ( v ) < \infty$

Vertices in the second category are always non-promising, whereas vertices in the rest of categories can be either promising or non-promising. The promising vertices can be used to approximate the region $\chi _ { \mathrm { r e l } } \subseteq \chi _ { \mathrm { f r e e } }$ of the free space that may contain the optimal path.

```matlab
Algorithm 1: Body of the RRT# Algorithm

1 RRT#(xinit, Xgoal, X)

2 V ← {xinit}; E ← ∅;

3 G ← (V, E);

4 for i = 1 to N do

5 xrand ← Sample(i);

6 G ← Extend(G, xrand);

7 ReduceInconsistency(G, Xgoal);

8 (V, E) ← G; E' ← ∅;

9 foreach x ∈ V do

10 E' ← E' ∪ {(parent(x), x)}

11 return T = (V, E')
```

The algorithm starts by adding the initial point $x _ { \mathrm { i n i t } }$ into the vertex set of the underlying graph. Then, it incrementally grows the graph in $\chi _ { \mathrm { f r e e } }$ by sampling a random point $x _ { \mathrm { r a n d } }$ from $\chi _ { \mathrm { f r e e } }$ and extending some parts of the graph towards $x _ { \mathrm { r a n d } } .$ . Later, the ReduceInconsistency procedure, which is provided in Algorithm 3, propagates the new information due to the extension across the whole graph in order to improve the estimate of the cost-to-come value of the promising vertices in the graph. All computations due to the sampling and extension steps, followed by information propagation (Lines 4-7 of Algorithm 1), form a single iteration of the algorithm. The process is repeated for a given fixed number of iterations, and the consistent spanning tree of the final graph is returned at the end.

The key diference between the $\mathrm { R R T } ^ { \# }$ algorithm and other RRT-variants is that a unique consistent spanning tree of the graph is maintained at the end of the each iteration of the algorithm. Since this tree is consistent, it contains information of the lowest-cost path, which can be achieved on the current graph, for each promising vertex of the graph. In addition, the g-value of the promising vertices equals to their respective optimal cost-to-come value that can be achieved through the edges of the tree. Therefore, each new vertex is initialized with the minimum possible estimate of its respective optimal cost-to-come value during extension (since all of its promising neighbor vertices have the lowest g-value), and this estimate keeps improving to the best possible value whenever new information becomes available on any part of the graph. Hence, the g-value of each promising vertex of the graph converges to its optimal cost-to-come value very quickly.

```csv
Algorithm 2: Extend Procedure for RRT# Algorithm
1 Extend(G,x)
2 (V,E) ← G; E' ← ∅;
3 xnearest ← Nearest(G,x);
4 xnew ← Steer(xnearest,x);
5 if ObstacleFree(xnearest,xnew) then
6 g(xnew) ← ∞;
7 lmc(xnew) = g(xnearest) + c(xnearest,xnew);
8 parent(xnew) = xnearest;
9 Xnear ← Near(G,xnew,|V));
10 foreach xnear ∈ Xnear do
11 if ObstacleFree(xnear,xnew) then
12 if lmc(xnew) > g(xnear) + c(xnear,xnew) then
13 lmc(xnew) = g(xnear) + c(xnear,xnew);
14 parent(xnew) = xnear;
15 E' ← E' ∪ {(xnear,xnew),(xnew,xnear)};
16 V ← V ∪ {xnew};
17 E ← E ∪ E';
18 UpdateQueue(xnew);
19 return G' ← (V,E)
```

The Extend procedure for the $\mathrm { R R T } ^ { \# }$ algorithm is given in Algorithm 2. During each iteration, the Extend procedure tries to extend the graph towards the randomly sampled point $x _ { \mathrm { { r a n d } } } \in \mathcal { X } _ { \mathrm { { f r e e } } } .$ First, the closest vertex in the graph $x _ { \mathrm { n e a r e s t } }$ is found in Line 3, then $x _ { \mathrm { n e a r e s t } }$ is steered towards the randomly sampled point $x _ { \mathrm { r a n d } }$ in the next line. If the line segment connecting the steered point $x _ { \mathrm { n e w } }$ and $x _ { \mathrm { n e a r e s t } }$ is feasible, then the new point $x _ { \mathrm { n e w } }$ is prepared for inclusion to the vertex set of the graph. First, its cost-to-come estimate, i.e., the g-value and lmc-values, and the parent vertex are initialized by using information of the nearest vertex $x _ { \mathrm { n e a r e s t } }$ . Then, a local search is performed in some neighborhood of $x _ { \mathrm { n e w } }$ , i.e., the set of vertices returned by the Near procedure, in order to find the local minimum cost-to-come estimate value in Lines 10-15 and the corresponding parent vertex. The new vertex $x _ { \mathrm { n e w } }$ and all extensions resulting in feasible trajectories are added to the vertex and edge set of the graph in Lines 16-17, respectively. In the end, the new vertex is decided to be inserted in the priority queue or not based on its consistency in the UpdateQueue procedure.

Inclusion of each new vertex may result in an inconsistent vertex in the graph if a finite lmc-value is achieved. Therefore, consistency of the spanning tree needs to be checked, and appropriate operations must be performed in order to make it consistent, if necessary. The ReduceInconsistency procedure, which is provided in Algorithm 3, is called to make the spanning tree consistent by operating on the inconsistent and promising vertices of the graph, iteratively. It simply pops the most promising inconsistent vertex from the priority queue, if there are any, and this inconsistent vertex is made consistent by assigning its lmc-value to its g-value. Then, its new g-value informa tion is propagated among its neighbors in order to improve their lmc-values in Lines 7-11. However, this information propagation may also cause some vertices to be inconsistent; therefore, all resulting inconsistent vertices are inserted in the priority queue as well. This process continues until a consistent spanning tree is computed, that is, there is no inconsistent promising vertex left in the priority queue.

```matlab
Algorithm 3: ReduceInconsistency Procedure
1 ReduceInconsistency(G, Xgoal)
2 while q.findmin() < Key(x*goal) do
3    x = q.findmin();
4    g(x) = lmc(x);
5    q.delete(x);
6    foreach s ∈ succ(G, x) do
7    if lmc(s) > g(x) + c(x, s) then
8    parent(s) = x;
9    lmc(s) = g(x) + c(x, s);
10    UpdateQueue(s);
```

```matlab
Algorithm 4: Auxiliary Procedures

1 Initialize(x)
2 g(x) ← ∞;
3 lmc(x) ← ∞;
4 parent(x) ← ∅;

5 UpdateQueue(x)
6 if g(x) ≠ lmc(x) and x ∈ q then
7    q.update(x, Key(x));
8 else if g(x) ≠ lmc(x) and x ∉ q then
9    q.insert(x, Key(x));
10 else if g(x) = lmc(x) and x ∈ q then
11    q.delete(x);

12 Key(x)
13 g_min = min(g(x), lmc(x));
14 f = g_min + h(x);
15 return key = (f, g_min);
```

## 5 Numerical Simulations 1

The $\mathrm { R R T } ^ { \# }$ algorithm was developed in C++ and run on a computer with a 2.40 GHz processor and 12GB RAM running the Ubuntu 11.10 Linux operating system. A Fibonacci heap was implemented as priority queue to store inconsistent vertices during the search [4]. Extensive simulations were run to compare the performance of the RRT<sup>#</sup> algorithm with the RRT<sup>∗</sup> algorithm, whose C implementation is available to download from the RRT<sup>∗</sup> authors’ website (http://sertac.scripts.mit.edu/rrtstar/).

Both $\mathrm { R R T } ^ { \# }$ and RRT<sup>∗</sup> algorithms were run on three diferent problem types with the same sample sequence in order to demonstrate the diference in their behavior while growing the tree. All problems tested require finding an optimal path in a square environment minimizing the Euclidean path length. The heuristic value of a vertex is the Euclidean distance from the vertex to the goal. In the first problem type, there are no obstacles in the environment, whereas there are some box-like obstacles in the second and third problem types. In the third problem type, the environment is more cluttered than the one in the second problem type, containing many widely distributed small obstacles.

For the first problem type, the trees computed by both algorithms at diferent stages are shown in Figure 1. The initial state is plotted as a yellow square and the goal region is shown in blue with magenta border (upper right). The minimal-length path is shown in red. As shown in Figure 1, the best path computed by the $\mathrm { R R T } ^ { \# }$ algorithm converges to the optimal path. As mentioned earlier, one of the important diferences between the $\mathrm { R R T ^ { * } }$ and $\mathrm { R R T } ^ { \# }$ algorithms is that the latter classifies the vertices in one of the following four categories based on the values of its $( \mathtt { g } ( v ) , \mathtt { l m c } ( v ) )$ pair: Consistent with finite key value (shown in green), consistent with infinite key value (shown in black), inconsistent with finite key value (shown in blue), and inconsistent with infinite g-value and finite lmc-value (shown in red).

Since only the points in the relevant region $\mathcal { X } _ { \mathrm { r e l } }$ have the potential to be part of the optimal path, the $\mathrm { R R T } ^ { \# }$ algorithm tries to approximate $\mathcal { X } _ { \mathrm { r e l } }$ with the set of promising vertices $V _ { \mathrm { p r o m } }$ and tends to stop rewiring the parts of the tree which lie outside of the $\mathcal { X } _ { \mathrm { r e l } }$ as iterations $_ \mathrm { g o }$ to infinity. As seen in Figure 1, for this particular scenario, $\mathcal { X } _ { \mathrm { r e l } }$ is an elliptic region, which is much smaller than the whole $\chi _ { \mathrm { f r e e } }$ . Therefore, uniform random sampling on $\chi _ { \mathrm { f r e e } }$ results in too many vertices of diferent types (green, black, red, and blue vertices) outside of the relevant region during the search. The estimate of $\mathcal { X } _ { \mathrm { r e l } }$ can be used to implement more intelligent sampling strategies, if needed, although this possibility was not pursued in this paper, where all sampling was uniform.

![](Arslan2012Role_figs/eb731c39fc8a1ead52448cc2dbd7bb05882fd6d552aec58b06bfd30186133094.jpg)  
(a)

![](Arslan2012Role_figs/89f9b56cea25bf3167f2a91c1047d856683a38ffae67c2814723e2598ff95238.jpg)  
(b)

![](Arslan2012Role_figs/bbbc0cb8ac909e994ededb5859f7efb5b4e002f8266a896e63ba06d6660d82d3.jpg)

![](Arslan2012Role_figs/f0d15d57d3f9bd3e32e37dd6baaba0977548809e1781b124eb39929404b2f6e1.jpg)  
(c)  
(d)

![](Arslan2012Role_figs/2118d5f9bc2d97d15327e0a6ce6b8e589bce0ad9a5594136304e98a9a3353271.jpg)  
(e)

![](Arslan2012Role_figs/3965dabff1abdf2557e066272169f28f3298fb90dc20b046a14efe93708f5878.jpg)  
(f)

![](Arslan2012Role_figs/db1a434ea3bfc25c8dec897676e66e1ffbca33cd4e4d1ecfcd2bfbdff55bd0d6.jpg)  
(g)

![](Arslan2012Role_figs/9cd489fb2116285469b331674cc91d8428195ab64ac680e05c9811ddf260f866.jpg)  
(h)  
Figure 1: The evolution of the tree computed by $\mathrm { R R T ^ { * } }$ and $\mathrm { R R T } ^ { \# }$ algorithms is shown in $\mathrm { ( a ) } \mathrm { - ( d ) }$ and (e)-(h), respectively. The configuration of the trees (a), (e) is at 250 iterations, (b), (f) is at 500 iterations, (c), (g) is at 2500 iterations, and (d), (h) is at 25000 iterations.

![](Arslan2012Role_figs/d4fb8f73796bb318fece48751d5e9202e1966d1fae0585d1cb132d76778337f9.jpg)  
(a)

![](Arslan2012Role_figs/7fe3ab49896885045725280f625e5d7ec154f0ef9c8c60b027b828a09ed3a718.jpg)  
(b)  
Figure 2: The change in the cost of the best paths computed by RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms, and the variance in the trials are shown in (a) and (b), respectively.

In the second problem type, the same experiment was carried out and both algorithms were run in an environment with several obstacles. The configuration of the trees for both the RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms at diferent stages are shown in Figure 3.

![](Arslan2012Role_figs/14948a5faeb70b1b59c79ee15afc24cb33e0ee1163a333727ef211e503b85caa.jpg)  
(a)

![](Arslan2012Role_figs/1da3c6641fd5fb303ace349d4d62599bde6fd288e947edf7008103c6f7ce77c5.jpg)  
(b)

![](Arslan2012Role_figs/d91376ee1bb2f4c53b4cb41346a6acee0a0ddebbb770be6b39fbeaf4f792a46e.jpg)  
(c)

![](Arslan2012Role_figs/e91bb6294e98af26bc5469e7b8534ea3c7f23980443fa82f1077a98481d0630b.jpg)  
(d)

![](Arslan2012Role_figs/2870957a3b75eb481277318753e97486de016ae5b7973b3d458f8ef014d05140.jpg)  
(e)

![](Arslan2012Role_figs/a16f8cbd3116bf78fd0e8929215cf242a50abbcc025a78c5847387cd0e59957d.jpg)  
(f)

![](Arslan2012Role_figs/372ab320ea9d32a92e5e894865a98bd5a408d2f54b412aa1abb67041bd6e6535.jpg)  
(g)

![](Arslan2012Role_figs/0efd542615e4fed43cf45799b318afb853f26e1db9621c4d25e8c73a04123b70.jpg)  
(h)  
Figure 3: The evolution of the tree computed by RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms is shown in (a)-(d) and (e)-(h), respectively. The configuration of the trees (a), (e) is at 250 iterations, (b), (f) is at 500 iterations, (c), (g) is at 2500 iterations, and (d), (h) is at 25000 iterations.

![](Arslan2012Role_figs/5b04d97e79636ae08533f9ce6ca3af7609bedeb192924ca05991e9f396320291.jpg)  
(a)

![](Arslan2012Role_figs/623aaa8511e007b23f3fffd751513a25f85d62357f7068e0f1273f5fb962992c.jpg)  
(b)  
Figure 4: The change in the cost of the best paths computed by RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms and the variance in the trials are shown in (a) and (b), respectively.

In the third problem type, both algorithms were run in a more cluttered environment, where there are many diferent homotopy classes containing the local minimum solution for the problem. As shown in Figure 5, both algorithms switch between paths which have locally best cost, eventually converging to the optimal solution.

![](Arslan2012Role_figs/4556c3f64c53f85b99b977e4c39c103ae9d5038cc655448577ac6a5ef745a6f0.jpg)  
(a)

![](Arslan2012Role_figs/566bf3d9bc862141df4aeb96b21b7edd5ae32ff8b952813c17ae6adb04b192bd.jpg)  
(b)

![](Arslan2012Role_figs/78a7699d66048ae5e9f578f77c2dda68760a9c86969bd97d4c41694102fa0ca1.jpg)  
(c)

![](Arslan2012Role_figs/ef54d46fe2c0ba9c764a447c40577f55a2a51376f9bae1a3dba5575b425850fa.jpg)  
(d)

![](Arslan2012Role_figs/9f809066f255fc2f075b3b03e1595578dcc7fd8a6a5ab5eaee55a7a97f0f4be8.jpg)  
(e)

![](Arslan2012Role_figs/4069b66c6a8b69a48190b3dd58079e9cebfb7f8ddae4755ada9716dcf1eb9799.jpg)  
(f)

![](Arslan2012Role_figs/3a0b1fc4a0bcfdf6df083f63995f601ef53a89e2a44284faa5329e1667043d0e.jpg)  
(g)

![](Arslan2012Role_figs/a0251214b0bac4e1120b0e8bf3cefb6a1aca070387ff2f472e54344e47eb6694.jpg)  
(h)  
Figure 5: The evolution of the tree computed by RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms is shown in (a)-(d) and (e)-(h), respectively. The configuration of the trees (a), (e) is at 250 iterations, (b), (f) is at 500 iterations, (c), (g) is at 2500 iterations, and (d), (h) is at 25000 iterations.

![](Arslan2012Role_figs/ed36d8a37f7ada3cdf978ceabf32e33cc351bf35921a638ba2761168b37e837c.jpg)  
(a)

![](Arslan2012Role_figs/c271713904ea41c81ab821b442a340b4cd7c1f8c0f61f48e7c3e2f544731b8cb.jpg)  
(b)  
Figure 6: The change in the cost of the best paths computed by RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms and the variance in the trials are shown in (a) and (b), respectively.

Finally, in the fourth problem type, both algorithms were run in a obstacle-free environment where there are diferent cost zones. The cost coeficient of each zone from top to bottom is 1.5, 0.75, 2.5, 0.75, and 1.5, respectively and 1 elsewhere. As seen in Figure 7, both algorithms compute the optimal path which has longer segments in low-cost zones.

![](Arslan2012Role_figs/c55b2ce76395213520c8e54007e22d186c14f74779deecbb11126e2b8f036568.jpg)  
(a)

![](Arslan2012Role_figs/dab981e1cd6e79dff037b962615b8fdaec1e6c8ca18035227d5d9ec8470b64f5.jpg)  
(b)

![](Arslan2012Role_figs/8b43b7ea1e701066bb66928b86c5ff623d14dd8df162c071bca2fe5c2375f89c.jpg)  
(c)

![](Arslan2012Role_figs/469d7d57368d85d8934a135a0f0de2ff5a63aa5187c84a1c501b367e206d3574.jpg)  
(d)

![](Arslan2012Role_figs/7a39f7a0c1afa360dea827f93ee5fa0ba7224533a0236503c89d989fd519e425.jpg)  
(e)

![](Arslan2012Role_figs/c8c0525feea8c426fa35aa0b3802e88d65c3a1d60721ff43a15fdef8d0ddc2d9.jpg)  
(f)

![](Arslan2012Role_figs/f033a3896161c4647289a9142b32db260407a6b22860b9efaf3c0d7a4ada09f2.jpg)  
(g)

![](Arslan2012Role_figs/78d33de9a6c99db89a1d46547a9a46c0e74ce73a2155202d75f2bb049bdc60f1.jpg)  
(h)  
Figure 7: The evolution of the tree computed by RRT<sup>∗</sup> and RRT<sup>#</sup> algorithms is shown in (a)-(d) and (e)-(h), respectively. The configuration of the trees (a), (e) is at 250 iterations, (b), (f) is at 500 iterations, (c), (g) is at 2500 iterations, and (d), (h) is at 25000 iterations.

![](Arslan2012Role_figs/b8e38148025c1fcb4f996eb00d33666f2ba35ff2847bfcb14b1d42f6a9cf8ff9.jpg)  
(a)

![](Arslan2012Role_figs/24717b339a3c7b6f7a9e50635d5128ff32799d2e066f0d10d697646ad2b0560d.jpg)  
(b)  
Figure 8: The change in the cost of the best paths computed by $\mathrm { R R T ^ { * } }$ and $\mathrm { R R T } ^ { \# }$ algorithms, and the variance in the trials are shown in (a) and (b), respectively.

## 6 Variants of the $\mathrm { R R T } ^ { \# }$ Algorithm

Too many non-promising vertices are included in the tree computed by the $\mathrm { R R T } ^ { \# }$ algorithm as observed in the previous simulations. This is owing to the fact that the $\mathrm { R R T } ^ { \# }$ algorithm includes all new vertices in the graph regardless of their type. A simple vertex selection criterion can be used in the Extend procedure in order to prevent the algorithm from growing the tree towards the region outside $\mathcal { X } _ { \mathrm { r e l } }$ . However, being over-selective on vertex inclusion may degrade the performance of the algorithm – and thus lead to a suboptimal solution – since the cost-to-come value of all vertices, which is used to decide if a new vertex is promising or not, is an estimate of the optimal one. In this section, we propose three variants of the baseline $\mathrm { R R T } ^ { \# }$ algorithm.

RRT $^ { \ast } _ { V 1 }$ : In the first variant, which is given in Algorithm 5, if a new vertex happens to be consistent with infinite key value (black vertex), it is not included in the graph. This situation can happen if all of the neighbor vertices of the new vertex happen to be inconsistent with infinite g-value and finite lmc-value (red vertices). First, the estimates of the cost-to-come-value of the new vertex $x _ { \mathrm { n e w } }$ are initialized with infinite cost, and its parent vertex is set to ‘null in Line 6. Then, a better value for the lmc-value of the new vertex is searched among its neighbor vertices. During this search, the parent of the new vertex remains unassigned only if there are no any neighboring vertices with finite g-value.

RRT $^ { \# } _ { V 2 }$ : In the second variant, the algorithm becomes more selective on vertices to be added to the graph and the “parent $( x _ { \mathrm { n e w } } ) \neq \emptyset \ \land \ \mathsf { K e y } ( \mathsf { p a r e n t } ( x _ { \mathrm { n e w } } ) ) \prec \mathsf { K e y } ( x _ { \mathrm { g o a l } } ^ { * } ) ^ { , , }$ condition is checked in Line 14. Simply, a new vertex is included to the graph only if its parent is a promising vertex.

RRT $^ { \# } _ { V 3 }$ : Lastly, the third variant is most selective on vertex for inclusion and $\mathrm { { K e y } } ( x _ { \mathrm { { n e w } } } ) \prec$ $\mathtt { K e y } ( x _ { \mathrm { g o a l } } ^ { * } )$ condition is checked, that is, only promising new vertices are included in the graph.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5: Extend Procedure for RRT $^{\#}$ V1 Algorithm

1 Extend(G,x)
2 (V,E) ← G; E' ← ∅;
3 xnearest ← Nearest(G,x);
4 xnew ← Steer(xnearest,x);
5 if ObstacleFree(xnearest, xnew) then
6 Initialize(xnew);
7 Xnear ← Near(G, xnew, |V|);
8 foreach xnear ∈ Xnear do
9 if ObstacleFree(xnear, xnew) then
10 if lmc(xnew) &gt; g(xnear) + c(xnear, xnew) then
11 lmc(xnew) = g(xnear) + c(xnear, xnew);
12 parent(xnew) = xnear;
13 E' ← E' ∪ {(xnear, xnew), (xnew, xnear)};
14 if parent(xnew) ≠ ∅ then
15 V ← V ∪ {xnew};
16 E ← E ∪ E';
17 UpdateQueue(xnew);
18 return G' ← (V, E)
</div>

## 7 Numerical Simulations 2

The same experiments as before were carried out for the three variants of the $\mathrm { R R T } ^ { \# }$ algorithm. As seen in the figures below, all variants successfully prevent the inclusion of vertices which lie in the unfavorable regions of the search space. As seen in Figures $9 ( \mathrm { e } ) , 1 2 ( \mathrm { e } ) , 1 5 ( \mathrm { e } )$ , and $1 8 ( \mathrm { e } )$ , the $\mathrm { R R T } _ { V 1 } ^ { \# }$ algorithm does not include any black vertices in the tree (these are the vertices that are consistent with infinite key value, hence non-promising), but still computes a solution to the problem, which is as good as the one computed by the $\mathrm { R R T ^ { * } }$ and $\mathrm { R R T } ^ { \# }$ algorithms. However, there are still many red (i.e., non-promising and inconsistent with infinite g-value and finite lmc-value) vertices included in the tree. This is owing to the fact that they are never made consistent until the last iteration, since they mostly lie outside of $\mathcal { X } _ { \mathrm { r e l } }$ . Therefore, they remain in the priority queue and need to be sorted during each iteration. This makes the ReduceInconsistency procedure slower. In the $\mathrm { R R T } _ { V 2 } ^ { \# }$ algorithm, the number of red vertices included into the tree is reduced by simply enforcing to have a promising parent vertex for the new vertex that is considered for extension. Red vertices are mostly included into the branches of the tree that are formed outside of the $\mathcal { X } _ { \mathrm { r e l } }$ during exploration phase. As seen in Figures 9(v), 12(v), 15(v), and $1 8 ( \mathrm { v } )$ , the $\mathrm { R R T } _ { V 2 } ^ { \# }$ algorithm tends not to include vertices into the branches of the tree which are very far away from the optimal solution. Lastly, the $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithm includes a new vertex into the tree only if it is a promising one. Therefore, all vertices in the tree, other than the goal vertices, are either green or blue, which are located around the boundary of $\mathcal { X } _ { \mathrm { r e l } }$

The convergence rate and variance in the computation of the best path for all algorithms are shown in Figures 11, 14, 17, and 20. Since this is a two-dimensional problem, the optimal path for each problem type can be computed visually and the cost of the paths for each algorithm is normalized with respect to the cost of the optimal solution. The ratio of the cost of the best path over the optimal cost for the $\mathrm { R R T ^ { * } } , \mathrm { R R T ^ { \# } } , \mathrm { R R T } _ { V 1 } ^ { \# } , \mathrm { R R T } _ { V 2 } ^ { \# }$ , and $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithms is shown in red, blue, green, magenta, and black colors, respectively.

![](Arslan2012Role_figs/6134305ba1d3072219af260c963df28519755bed63058d565a84ca55debbf29b.jpg)  
(a)

![](Arslan2012Role_figs/08ababce8a12f2b5fe7793bc622f523c48f780eff15074a81ef4e5db6518d15b.jpg)  
(b)

![](Arslan2012Role_figs/0d66a8a92bd2beaf738f11765c398f14c23e2f7efc7eb1072f187167a7c4bf4e.jpg)

![](Arslan2012Role_figs/5ee9fc2df5ac4d93e38f2204e023ba35ff2ce82b629d2da86be7c896f2a6550f.jpg)  
(c)

![](Arslan2012Role_figs/34de8e9d8cd39b33368ae1453869e610c83421be26286cb9cf4e8c9bb5f2093c.jpg)

![](Arslan2012Role_figs/0eb46dfd2638c80e3ed7ac4c3ff91266a66bf7e8f5b516749f86abaa1d6c4a05.jpg)  
(i)  
(ii)

(d)  
![](Arslan2012Role_figs/4fb11fecf6eb5a028be160267c39a2a3a5bcde831e779439fe166b17343c6a2b.jpg)  
(iii)

![](Arslan2012Role_figs/431e8b1949565bf1460c0725d12cff48851fa3fe84095e5e875ac32aa8913955.jpg)  
(iv)

![](Arslan2012Role_figs/0e01567ab99cf18a3884fc32f2460162749404ae8db253198f9ec8c3ea249ebf.jpg)  
(e)

![](Arslan2012Role_figs/2e57fe3b6e3a7a91c927952e6d85476e2e9eed46ef9cbb97f097592ad4d812af.jpg)  
(v)  
Figure 9: The evolution of the tree computed by $\operatorname { R R T } _ { V 1 } ^ { \# }$ and $\mathrm { R R T } _ { V 2 } ^ { \# }$ algorithms is shown in $\mathrm { ( a ) } \mathrm { - ( e ) }$ and $( \mathrm { i } ) \mathrm { - } ( \mathrm { v } )$ , respectively. The configuration of the trees (a), (i) is at 250 iterations, (b), (ii) is at 500 iterations, (c), (iii) is at 2500 iterations, (d), (iv) is at 10000 iterations, and (e), (v) is at 25000 iterations.

![](Arslan2012Role_figs/97d0560d6e9102e390a8e33c14dedb88c244b0c5a95d1508bdada802bd93a3c5.jpg)  
(a)

![](Arslan2012Role_figs/fafcce21342bbc45eae482e3470509abd21aee1827902ebb8244848e9b484c94.jpg)  
(b)

![](Arslan2012Role_figs/aab900503cb4baf909e1e7c4c8061ffcf16c24fae6f5ed97d6b6badfdff4d53d.jpg)  
(c)

![](Arslan2012Role_figs/3c9f69e76201bf6e71f5e6a3a5d827d3e41558e05129e508b239d61382c03eee.jpg)  
(d)

![](Arslan2012Role_figs/c5b8a14d970923e75783824060985668bef44f066e7372ac5d77c088839328be.jpg)  
(e)

![](Arslan2012Role_figs/68d823741c08b755428c640c0fdfa7285a99e2ceb27fd13ae23bc984f8351135.jpg)  
(f)  
Figure 10: The evolution of the tree computed by $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithm is shown in (a)-(f). The configuration of the trees in (a) is at 250 iterations, in (b) is at 500 iterations, in (c) is at 2500 iterations, in (d) is at 5000 iterations, in (e) is at 10000 iterations, and in (f) is at 25000 iterations.

![](Arslan2012Role_figs/94a20eaf3662df4b17e433a4816fec62ae678e0c406ef064b98463df6e82fbfa.jpg)  
(a)

![](Arslan2012Role_figs/08016057ef647ccb860a4556031d8f2738082d55021cd5997a5d90b3e9d9b00a.jpg)  
(b)  
Figure 11: The change in the cost of the best paths computed by RRT<sup>∗</sup>, RRT<sup>#</sup>, and its variant algorithms and the variance in the trials are shown in (a) and (b), respectively.

![](Arslan2012Role_figs/ae3cf755a902458d3aefbaaff0e24a2f702521be9a229b86fadf800b821be1d8.jpg)  
(a)

![](Arslan2012Role_figs/3f41e7f26825aefa1a5050f0d52fef8318bfd29ab5af3a7d99cbd645325821bb.jpg)  
(b)

![](Arslan2012Role_figs/065f38144abbce9c84e2cabe6b20ca6dd4c54dc0f6216c3f520e27439df83bce.jpg)

![](Arslan2012Role_figs/4a4882fdce5ae5c56072f3d33173c1b87fba5c696238a187fd83291eedc2681d.jpg)

![](Arslan2012Role_figs/dc08f409a1f6aea78b3d137c703ae0c1b63b3f2cf7658e1730e4de75c072d142.jpg)  
(i)

(d)  
![](Arslan2012Role_figs/de327b7a72e9edf115035a84fcf9da55f0adbc16bf6c8c3930d82700ac5b61f6.jpg)  
(ii)

(c)  
![](Arslan2012Role_figs/22c5340490e93c0c780b2ccfeadfe516fb4e57a94982040fba485e0b49614160.jpg)  
(iii)

![](Arslan2012Role_figs/824dd992831f51484960c72ed0367ad8256a853574abd905943f32253bad3fd0.jpg)  
(iv)

![](Arslan2012Role_figs/91765a275e31f8ea91c620dc732b1e1a45c80f529114bb7f72d960c2be076b71.jpg)  
(e)

![](Arslan2012Role_figs/c5b340d8455b1481148c0ccf81ac826829f7b33391a8fed53aed2dcab9579039.jpg)  
(v)  
Figure 12: The evolution of the tree computed by $\operatorname { R R T } _ { V 1 } ^ { \# }$ and $\mathrm { R R T } _ { V 2 } ^ { \# }$ algorithms is shown in $\mathrm { ( a ) } \mathrm { - ( e ) }$ and $( \mathrm { i } ) \mathrm { - } ( \mathrm { v } )$ , respectively. The configuration of the trees (a), (i) is at 250 iterations, (b), (ii) is at 500 iterations, (c), (iii) is at 2500 iterations, (d), (iv) is at 10000 iterations, and (e), (v) is at 25000 iterations.

![](Arslan2012Role_figs/5a2ee226965d07100e3329c9d7c3e02f57ebc05b64f46eedd6838e14e9adb829.jpg)  
(a)

![](Arslan2012Role_figs/ac92d5ceee92afbd4ba744909437cf9a16400aa86ea75529184bd131f4db0e4f.jpg)  
(b)

![](Arslan2012Role_figs/f971c6aae29ce96206c421476ffc35944449e3fe38304595ee9fc5472b5b319a.jpg)  
(c)

![](Arslan2012Role_figs/a9d4258b3422a4490e56473024a687160e40e0fc162cf418c888c68aeec83a66.jpg)  
(d)

![](Arslan2012Role_figs/fce0ed6d87f74ab9756d739e7094598edc8fed4611cbafeb916825d4b4c830bb.jpg)  
(e)

![](Arslan2012Role_figs/c07fb913620e1351c7bbb116bb3cab7bbc44bcc1682ea41007a30f5ea94def1a.jpg)  
(f)  
Figure 13: The evolution of the tree computed by $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithm is shown in (a)-(f). The configuration of the trees in (a) is at 250 iterations, in (b) is at 500 iterations, in (c) is at 2500 iterations, in (d) is at 5000 iterations, in (e) is at 10000 iterations, and in (f) is at 25000 iterations.

![](Arslan2012Role_figs/1b01457d94e812d5992ac44e9e73317ef39dfab92d970205d8cde195d7c168ac.jpg)  
(a)

![](Arslan2012Role_figs/a502a7b1461ed68f8fc1c5e64d3208d16678c2f7396f7e355015d3897e27d633.jpg)  
(b)  
Figure 14: The change in the cost of the best paths computed by RRT<sup>∗</sup>, RRT<sup>#</sup>, and its variant algorithms and the variance in the trials are shown in (a) and (b), respectively.

![](Arslan2012Role_figs/2b2265bfab14f3386e2966f788579dd220cd671499d52c223832131946e8bb7b.jpg)  
(a)

![](Arslan2012Role_figs/17ec319ed01bf7e7f6d466fcba55acf5ebf4ec6282381f0e91b71280c66d98a1.jpg)  
(b)

![](Arslan2012Role_figs/dda71330b0dd0a8c1ee033864b26c2938daa13135976adef5f4c4ea68fa82a35.jpg)

![](Arslan2012Role_figs/de0f001f5fbe18c081059fbfb499d38cb63fb16269b772a0f5b54e441e1ffaa5.jpg)

![](Arslan2012Role_figs/ea39010a167868b07f66b2355a42a26943f1f0aaa23c4d5cfcb839c044d1e733.jpg)  
(i)

![](Arslan2012Role_figs/66b6d3389bf376de00c6d6677a5fa869e15d5b44ed8b943aa0f6ceb131ab6d46.jpg)  
(ii)

(d)  
(c)  
![](Arslan2012Role_figs/724e8b0bfee57eaafa686edd2a84e5cbd397db04c18dedd8b2d1e1e29624a354.jpg)  
(iii)

![](Arslan2012Role_figs/3b1f4773a84940d7d17bfb98877eb677cd8cfa93973b94a014679c51a6492ed8.jpg)  
(iv)

![](Arslan2012Role_figs/2a275b7168da5eb695085f0cf0040c450d7eae3ba8d59f0e0566e4cadaaa9f38.jpg)  
(e)

![](Arslan2012Role_figs/d2ce9798b2ed21fa913e3f91edfd36609e97d897170fbd783f2e06fd977c5799.jpg)  
(v)  
Figure 15: The evolution of the tree computed by $\operatorname { R R T } _ { V 1 } ^ { \# }$ and $\mathrm { R R T } _ { V 2 } ^ { \# }$ algorithms is shown in $\mathrm { ( a ) } \mathrm { - ( e ) }$ and $( \mathrm { i } ) \mathrm { - } ( \mathrm { v } )$ , respectively. The configuration of the trees (a), (i) is at 250 iterations, (b), (ii) is at 500 iterations, (c), (iii) is at 2500 iterations, (d), (iv) is at 10000 iterations, and (e), (v) is at 25000 iterations.

![](Arslan2012Role_figs/afcaf7205c647171a0504c204a10fba3c97ed66a5650175137ad9e332a76f157.jpg)  
(a)

![](Arslan2012Role_figs/d6285f82e91a0c3bfb8a48e17f194ec1853ac4363efc768d438a784c0ff42b88.jpg)  
(b)

![](Arslan2012Role_figs/ff25890bc9d90d2d5b9da8609ca4c8e3ee6dbbe5e5e479f9f4188b7dd0e8d2ae.jpg)  
(c)

![](Arslan2012Role_figs/eb63b68143d77ed53ee7350905334caf390efc91b922266b6d023a93c3ddea39.jpg)  
(d)

![](Arslan2012Role_figs/3add031fc820714a0ac2522c1df61dcc5dcbc5bd079a13665da2dca27593004f.jpg)  
(e)

![](Arslan2012Role_figs/4aa03eb858b57e04eb844de27016d58befb736eedb5c7c9e1e84bacb1ac42cfa.jpg)  
(f)  
Figure 16: The evolution of the tree computed by $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithm is shown in (a)-(f). The configuration of the trees in (a) is at 250 iterations, in (b) is at 500 iterations, in (c) is at 2500 iterations, in (d) is at 5000 iterations, in (e) is at 10000 iterations, and in (f) is at 25000 iterations.

![](Arslan2012Role_figs/f35d0dd0a637c919bcb659a4e6665fab5fb1f47c8ae00499f2cabd3e8268e7df.jpg)  
(a)

![](Arslan2012Role_figs/2b69891dac576d28ae0792876b652cbb2ce4a36d881cd640ee021e49a559563a.jpg)  
(b)  
Figure 17: The change in the cost of the best paths computed by RRT<sup>∗</sup>, RRT<sup>#</sup>, and its variant algorithms and the variance in the trials are shown in (a) and (b), respectively.

![](Arslan2012Role_figs/9b1e650668741a57c4aed0016e7e70f673b4b2a0e8e9db49f91d325a28650432.jpg)  
(a)

![](Arslan2012Role_figs/5491a734d04e8879b6c030dc9a0eb7ba602647ce4b83b4c0e61f10ef613b61a8.jpg)  
(b)

![](Arslan2012Role_figs/c36ce384ffccb358f0cd5b2f9151de2457a9c09ddd465340604d12fa8bbfa856.jpg)

![](Arslan2012Role_figs/88a24fa2239ea6acf0134df2a81717e660992a46bd120cfd7fa1c55030f558be.jpg)  
(c)

![](Arslan2012Role_figs/35bca21ac93f438755de45a5641cf24414061601ec22bb580e10da36170cf357.jpg)

![](Arslan2012Role_figs/7e291bfb2cf8821f0aba90f16312e23710644386d50fb61bc4a42f41bc5ee7bb.jpg)  
(i)  
(ii)

(d)  
![](Arslan2012Role_figs/936e3e848684a114daac69ae71c8d98dd5bd414884fdda279f4a3e273b06cc58.jpg)  
(iii)

![](Arslan2012Role_figs/82d39f11f65c9bc5ab210813494a40f570935e380039be5fbe65af110b061a73.jpg)  
(iv)

![](Arslan2012Role_figs/e8cfd94b11095ae69eb82219c2bb9b6ff5e17e6ec436f2c0fdee72a434520e51.jpg)  
(e)

![](Arslan2012Role_figs/67fdd96a0da1bcddbdefce2c0718cca7b5c4fd17e7ba745e2a428167bd444c22.jpg)  
(v)  
Figure 18: The evolution of the tree computed by $\operatorname { R R T } _ { V 1 } ^ { \# }$ and $\mathrm { R R T } _ { V 2 } ^ { \# }$ algorithms is shown in $\mathrm { ( a ) } \mathrm { - ( e ) }$ and $( \mathrm { i } ) \mathrm { - } ( \mathrm { v } )$ , respectively. The configuration of the trees (a), (i) is at 250 iterations, (b), (ii) is at 500 iterations, (c), (iii) is at 2500 iterations, (d), (iv) is at 10000 iterations, and (e), (v) is at 25000 iterations.

![](Arslan2012Role_figs/7cc6667cad58760e6705c72cd9b9338ef3ca1fcf903c0319af9d9797e91fe991.jpg)  
(a)

![](Arslan2012Role_figs/6f3a4f4360c20965a0636087a74d6b2c609423fa389e3aee9a37d7d36c9229a5.jpg)  
(b)

![](Arslan2012Role_figs/dad3517b33dc112426513079940e40a0c201a5e7d13db01b388b632f755055ee.jpg)  
(c)

![](Arslan2012Role_figs/c5f0cc30da66d6d50fc96ad00bda62e930ca4f77fd9b6919af8f7adf8d2e36ac.jpg)  
(d)

![](Arslan2012Role_figs/e333e690a5d24e89341f5287e7057da4a421e92bd6c971ea0a974bb36283f165.jpg)  
(e)

![](Arslan2012Role_figs/0c16524195132172c042e3533382e4d2772c2a62065809e2c15a9777194ea704.jpg)  
(f)  
Figure 19: The evolution of the tree computed by $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithm is shown in (a)-(f). The configuration of the trees in (a) is at 250 iterations, in (b) is at 500 iterations, in (c) is at 2500 iterations, in (d) is at 5000 iterations, in (e) is at 10000 iterations, and in (f) is at 25000 iterations.

![](Arslan2012Role_figs/9f7d1fdbb13b3f0b357df8681ef7831b4a962f9e997b30d6aa3e0f44d157c1ae.jpg)  
(a)

![](Arslan2012Role_figs/05d873e73e38f16e5f80c278f8d12bd2dc77210a3ce26179305940e71bace2e3.jpg)  
(b)  
Figure 20: The change in the cost of the best paths computed by RRT<sup>∗</sup>, RRT<sup>#</sup>, and its variant algorithms and the variance in the trials are shown in (a) and (b), respectively.

A Monte-Carlo study was performed in order to compare the convergence rate and variance in the trials of all algorithms in a high dimensional search space. All algorithms were run up until 4 million iterations 100 times in a 5-dimensional search space for Problem types 1 and 2. In the second problem type, several 5-dimensional hypercubes of diferent size were randomly placed in the environment in order to represent obstacles. As shown in Figures 21 and 22, the $\mathrm { R R T } _ { V 2 } ^ { \# }$ and $\mathrm { R R T } _ { V 3 } ^ { \# }$ algorithms find the solution in a similar amount of time, and they are faster than the other algorithms. In addition, they compute solutions of lower cost than the other algorithms with smaller variance in the trials.

![](Arslan2012Role_figs/e29b3a025ce7703974cc110c0ef2e73f6af5cd1f7457286ea27c14a0175d7628.jpg)  
(a)

![](Arslan2012Role_figs/5595e64491f081783f2614498358a34ce751f0db74e0b9653d28dde04fa327e4.jpg)  
(b)  
Figure 21: The change in the cost of the best paths computed by RRT<sup>∗</sup>, $\mathrm { R R T } ^ { \# }$ , and its variant algorithms and the variance of the trials is shown in (a) and (b), respectively (problem type 1, 5D search space).

![](Arslan2012Role_figs/573a9d38b505d8e6e6ae2849f689f68a0e1c91ba04bf2fe7243c56bdf3013dae.jpg)  
(a)

![](Arslan2012Role_figs/bdd906145a9a31e802932d9d3c681af125111e69ac240698d55d22782d253b0d.jpg)  
(b)  
Figure 22: The change in the cost of the best paths computed by $\mathrm { R R T ^ { * } } , \mathrm { R R T ^ { \# } }$ , and its variant algorithms and the variance of the trials are shown in (a) and (b), respectively (problem type 2, 5D search space).

The execution times of all algorithms were also compared. Results of the $\mathrm { R R T } ^ { \# } , \mathrm { R R T } _ { V 1 } ^ { \# }$ $\mathrm { R R T } _ { V 2 } ^ { \# }$ , and $\mathrm { R R T } _ { V 3 } ^ { \# }$ are plotted in blue, green, magenta, and black, respectively. All algorithms were run in a 2D and a 5D environment with no obstacles for up to 750,000 and 4,000,000 iterations, respectively. The execution time of the $\mathrm { R R T } ^ { \# }$ and its variant algorithms is normalized over that of the RRT algorithm and is plotted versus the number of iterations averaged over 50 trials for the 2D search space in Figure $2 3 ( \mathrm { a } )$ . A similar plot is also created for 100 trials in the 5D search space

![](Arslan2012Role_figs/e2cc51fbab9c7669c56833df8a38bcbc9e607cfff741cc956b4cefe15272cb55.jpg)  
(a)

![](Arslan2012Role_figs/f8d717b22a063dff6656fc26c9c5afd28defd4089566fad77f465012ed73c2ae.jpg)  
(b)  
Figure 23: Comparison of execution time of all algorithms (Problem type 1)

## 8 Conclusion

In this paper, a new incremental sampling-based algorithm, denoted by $\mathrm { R R T } ^ { \# }$ is presented, which ofers asymptotically optimal solutions for solving motion planning problems. The $\mathrm { R R T } ^ { \# }$ algorithm relies heavily on the random geometric graph data structure and the RRG algorithm [20], which is also known to have asymptotic optimality properties. A bottleneck of optimal sampling-based algorithms is the slow convergence to the optimal solution, although sampling-based algorithms are capable of finding a feasible solution, often almost in real-time. By incorporating consistency information of all current vertices in the tree (essentially by comparing the current cost-to-come values of the vertices with the cost-to-come values via one of the neighboring vertices) we can have more informed estimates of the optimal values of the potential paths, thus speeding up convergence. Furthermore, once a feasible path has been found, vertex consistency can be used to estimate the region where the optimal solution should be found. This results in an initial convergence rate that is better than the one of the RRT<sup>∗</sup> algorithm.

We have also introduced three variants to improve the convergence rate of the baseline $\mathrm { R R T } ^ { \# }$ algorithm by implementing two key features: preventing the expansion of the tree towards unfavorable regions in search space, and propagating new information throughout the tree in an eficient way. The first feature allows us to limit the number of vertices in the tree, thus resulting to the algorithm running faster. The second feature allows us to compute solutions with a less number of vertices in the tree since any new information is exploited to the highest degree. As a result, the convergence rate of the baseline $\mathrm { R R T } ^ { \# }$ can be improved significantly. Extensive numerical results have verified these observations in several simulation scenarios.

The work in this paper can be extended in several directions. First, a thorough theoretical analysis is warranted in order to provide strict bounds on the convergence rate of $\mathrm { R R T } ^ { \# }$ . Second, since $\mathrm { R R T } ^ { \# }$ decomposes the vertex set into “promising” and “non-promising” ones, smarter sampling strategies can be developed to exploit this information. It is also crucial for the algorithm to reach the target set as early as possible in order to converge to the optimal solution faster. In that respect, a bi-directional version of the $\mathrm { R R T } ^ { \# }$ (like the RRT-connect in [14]) can be developed in order to shorten the first time-to-connect to the goal set. Also, a parallel version of the algorithm could be implemented by running the Extend and ReduceInconsistency procedures as separate threads. A possible implementation would be to have multiple threads implementing the Extend procedure and single thread implementing the ReduceInconsistency. Finally, the algorithm can be modified to solve motion planning problems for vehicles with complex dynamics (ground vehicles, aircraft, helicopters etc) by implementing specific local steering functions.

## References

[1] H. Choset, K. Lynch, S. Hutchinson, G. Kantor, W. Burgard, L. Kavraki, and S. Thrun. Principles of Robot Motion: Theory, Algorithms, and Implementations. The MIT Press, 2005.

[2] B. Donald, P. Xavier, J. Canny, and J. Reif. Kinodynamic motion planning. Journal of the Association for Computing Machinery, 40(5):1048–1066, November 1993.

[3] E. Frazzoli, M. A. Dahleh, and E. Feron. Real-time motion planning for agile autonomous vehicles. Journal of Guidance, Control, and Dynamics, 25(1):116–129, 2002.

[4] M. L. Fredman and R. E. Tarjan. Fibonacci heaps and their uses in improved network optimization algorithms. Journal of the ACM (JACM), 34(3):596–615, 1987.

[5] T. Howard and A. Kelly. Optimal rough terrain trajectory generation for wheeled mobile robots. The International Journal of Robotics Research, 26(2):141 – 166, February 2007.

[6] D. Hsu, R. Kindel, J.-C. Latombe, and S. Rock. Randomized kinodynamic motion planning with moving obstacles. International Journal of Robotics Research, 21(3):233–255, March 2002.

[7] S. Karaman and E. Frazzoli. Sampling-based motion planning with deterministic µ-calculus specifications. In Decision and Control, 2009 held jointly with the 2009 28th Chinese Control Conference. CDC/CCC 2009. Proceedings of the 48th IEEE Conference on, pages 2222–2229. IEEE, 2009.

[8] S. Karaman and E. Frazzoli. Incremental sampling-based algorithms for optimal motion planning. In Robotics: Science and Systems (RSS). Citeseer, 2010.

[9] S. Karaman and E. Frazzoli. Sampling-based algorithms for optimal motion planning. The International Journal of Robotics Research, 30(7):846–894, 2011.

[10] L. E. Kavraki and J.-C. Latombe. Randomized preprocessing of configuration space for fast path planning. Technical Report STAN-CS-93-1490, Dept. Computer Science, Stanford University, Stanford, CA, 1993.

[11] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars. Probabilistic roadmaps for <sup>ˇ</sup> path planning in high-dimensional configuration spaces. IEEE Transactions on Robotics and Automation, 12(4):566–580, 1996.

[12] L.E. Kavraki, P. Svestka, J.C. Latombe, and M.H. Overmars. Probabilistic roadmaps for path planning in high-dimensional configuration spaces. Robotics and Automation, IEEE Transactions on, 12(4):566–580, 1996.

[13] S. Koenig, M. Likhachev, and D. Furcy. Lifelong planning A\*. Artificial Intelligence, 155(1- 2):93–146, 2004.

[14] J.J. Kufner Jr. and S.M. LaValle. RRT-connect: An eficient approach to single-query path planning. In Robotics and Automation, 2000. Proceedings. ICRA’00. IEEE International Conference on, volume 2, pages 995–1001. IEEE, 2000.

[15] S. M. LaValle. Planning Algorithms. Cambridge University Press, 2006.

[16] S. M. LaValle and J. J. Kufner. Rapidly-exploring random trees: Progress and prospects. In B. R. Donald, K. Lynch, and D. Rus, editors, New Directions in Algorithmic and Computational Robotics, pages 293–308. AK Peters, 2001.

[17] S. M. LaValle and J.J. Kufner. Randomized kinodynamic planning. The International Journal of Robotics Research, 20(5):378, 2001.

[18] N.J. Nilsson. Problem-solving methods in artificial intelligence. 1971.

[19] J. Pearl. Heuristics: intelligent search strategies for computer problem solving. 1984.

[20] M. Penrose. Random geometric graphs, volume 5. Oxford University Press, USA, 2003.

[21] E. Plaku, L. E. Kavraki, and M. Y. Vardi. Motion planning with dynamics by a synergistic combination of layers of planning. IEEE Transactions on Robotics, 26(3):469–482, 2010.

[22] P. Svestka. A probabilistic approach to motion planning for car-like robots. Technical Report<sup>ˇ</sup> RUU-CS-1993-18, Dept. Computer Science, Utrecht University, Utrecht, The Netherlands, 1993.