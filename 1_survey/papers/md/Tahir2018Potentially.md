---
citation_key: Tahir2018Potentially
arxiv_id: 1807.08325
arxiv_url: "https://arxiv.org/abs/1807.08325"
title: "Potentially Guided Bidirectionalized RRT* for Fast Optimal Path Planning in Cluttered Environments"
authors_short: "Zaid Tahir et al."
year: 2018
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:52:00Z
origin: ai+web
reviewed: false
---

# Potentially Guided Bidirectionalized RRT\* for Fast Optimal Path Planning in Cluttered Environments

Zaid Tahir<sup>1</sup>∗, Ahmed H. Qureshi<sup>1,2</sup>∗, Yasar Ayaz<sup>1</sup>∗, Raheel Nawaz<sup>3</sup>∗

<sup>1</sup>Robotics And Intelligent Systems Engineering (RISE) Lab, Department of Robotics and Artificial Intelligence, School of Mechanical And Manufacturing Engineering (SMME), National University of Sciences And Technology (NUST), H-12 Campus, Islamabad, 44000, Pakistan.

<sup>2</sup>Department of Electrical and Computer Engineering, University of California San Diego, 9500 Gilman Dr, La Jolla, CA 92093.

<sup>3</sup>School of Computing, Mathematics and Digital Technology, Manchester Metropolitan University (MMU), Manchester M15 6BH, England.

## Abstract

Rapidly-exploring Random Tree star (RRT\*) has recently gained immense popularity in the motion planning community as it provides a probabilistically complete and asymptotically optimal solution without requiring the complete information of the obstacle space. In spite of all of its advantages, RRT\* converges to optimal solution very slowly. Hence to improve the convergence rate, its bidirectional variants were introduced, the Bi-directional RRT\* (B-RRT\*) and Intelligent Bi-directional RRT\* (IB-RRT\*). However, as both variants perform pure exploration, they tend to sufer in highly cluttered environments. In order to overcome these limitations we introduce a new concept of potentially guided bidirectional trees in our proposed Potentially Guided Intelligent Bi-directional RRT\* (PIB-RRT\*) and Potentially Guided Bi-directional RRT\* (PB-RRT\*). The proposed algorithms greatly improve the convergence rate and have a more eficient memory utilization. Theoretical and experimental evaluation of the proposed algorithms have been made and compared to the latest state of the art motion planning algorithms under diferent challenging environmental conditions and have proven their remarkable improvement in eficiency and convergence rate.

Keywords: Motion planning, Sampling based planning algorithms, RRT\*, Optimal path planning, Artificial Potential Fields, Bidirectional trees.

## 1. Introduction

Motion planning has been a major problem since late 1980s [1] and due to the rise in robotics becoming a part of our everyday life, the research in this field has even become a greater need. In the motion planning problem, given the initial and goal configuration of the robot, the objective is to plan from the initial state to the goal region while avoiding obstacles along the way. Motion planning finds its application in our everyday life, in fields such as smart cars [2], robotic surgery [3], aerial, underwater and amphibious robotics [2], humanoid robotics [4] and in countless others [5] [6] [7] [8]. As humans explore the outer-space more and more, motion planning in outer-space [9] is also a becoming a challenging task. With the advancement in micro chip and nano-technology motion planning finds its application in nano-robotics and in micro-flow control and automation of bio-molecular computation (MF-BMC) [10].

Due to such a comprehensive requirement of motion planning, many motion planning algorithms were developed as mentioned in [11] [12] [13] [14] [15] [16] [17] [18]. Motion planning algorithms are either complete which return a solution if one exists in finite time and reports a failure if a solution does not exist, or are not complete but assure resolution or probabilistic completeness [11]. Complete motion planning algorithms such as Visibility Graphs have been developed. But these algorithms require explicit representation of the configuration space. Such a representation requires a lot of computational power especially for higher degree of freedom systems which renders such algorithms ineficient for practical purposes. In case of resolution or probabilistic complete algorithms, these algorithms either first discretize the given configuration space and then apply graph-based searches or use random sampling in case of sampling based algorithms respectively [11]. Graph-based search algorithms up to their resolution, find the optimal solution if one exists. One such example is “exact road maps”, which discretizes the given configuration space that in turn places a heavy computational burden in higher dimensions. Another resolution complete algorithm, Artificial Potential Fields (APF) [19] also exists. But it is only efective if its resolution parameters are finely tuned, and another issue with APF is that it is greedy i.e it performs pure exploitation. Although exploitation might help compute the path quickly in some situations but it also causes the robot to get stuck in the local minima in APF [19].

Hence in order to avoid discretization of the state space and to avoid the above stated problems such as the local minima, sampling based stochastic searches were introduced such as Expansive Space Trees (ESTs) [20], Probabilistic Road Maps (PRMs) [21] and Rapidly-exploring Random Trees (RRTs) [22]. These stochastic sampling based searches are probabilistically complete, meaning that probability of finding a solution goes to one as the number of samples approach infinity. These algorithms performed very well in high dimensional spaces as well due to the fact that these algorithms do not require the complete construction of obstacle space. A major limitation of the above stated sampling-based algorithms is that they did not take into account the path cost and hence could not guarantee an optimal solution [23] [24]. Urmson and Simmons used heuristic-based sampling named h-RRT, to improve the path cost of RRT [25]. Ferguson et al. [26] used the anytime version of RRT, the anytime-RRTs improved the cost iteratively after finding an initial solution path. However, both these h-RRTs and anytime-RRTs did not guarantee optimal solution. Recently Karaman et al. [27] introduced an optimal variant of RRT, the RRT\*. The RRT\* first finds an initial path quickly, it then improves the solution by re-wiring the samples and replacing old parents with new parents whose cost in terms of Euclidean distance from initial state is less than them. This makes RRT\* asymptotically optimal, meaning it guarantees convergence to optimal solution as the number of samples go to infinity. RRT\* performs pure exploration, which can cause it to have very slow rates of convergence to optimal solution in highly cluttered environments and high dimensional spaces.

In order to improve the rates of convergence to optimal solution of RRT\*, techniques such as sample-biasing [28] [29] [30], sample-rejection [31], sampling-heuristics [25], multiple trees [32], iterative searches [31] and anytime searches [26] were used. Qureshi et al. [29] used potential biasing on the randomly sampled states in RRT\* to get to the optimal solution faster in his P-RRT\* algorithm, which is an extension of previously proposed $\mathrm { A P G D - R R T ^ { * } }$ algorithm [33]. Karaman et al. [31] implemented the anytime version of $\mathrm { R R T ^ { * } }$ using graph pruning. Multiple tree search based methods such as Bi-directional RRT\* (B-RRT\*) [32] and Intelligent Bi-directional $\mathrm { R R T ^ { * } }$ (IB-RRT\* ) [34] have recently been introduced and have shown to increase the convergence rate to optimal solution. In such a bidirectional search one Rapidly-exploring Random Tree (RRT) is grown from the initial state and the other Rapidly-exploring Random Tree is grown from one of the goal states. The bidirectional nature of these algorithms makes them inherently faster than the single-tree versions due to the fact that the samples that are too far away from the initial starting state are closer to the goal state. Whereas these samples are not directly connectable to the nodes of the growing tree in the single-tree version and could be used eficiently by connecting to the tree growing from the goal region in the bidirectional tree version. However, the problem with these bidirectional variants of $\mathrm { R R T ^ { * } }$ is that they perform pure exploration, even though two trees are involved but there exist no sample-biasing to guide the two trees towards each other for faster convergence to optimal solution. In $\mathrm { B { - } R R T ^ { * } }$ pure exploration is performed and each tree is grown one by one and a hybrid greedy connection heuristic checks if a connection between the two trees is possible or not. While IB-RRT\* also performs pure exploration, a simple sampling heuristic adds the randomly sampled state to that tree out of the two bidirectional trees, from which the cost (in terms of Euclidean distance) of an obstacle free path from that tree to the randomly sampled state is less than the other tree. Then a connection heuristic checks if the two trees are connectable. Since, B-RRT\* and $\mathrm { I B { - } R R T ^ { * } }$ perform pure exploration, they also sufer in highly cluttered environments. In this paper, we introduce the concept of potentially guiding two Rapidly-exploring Random Trees towards each other in bidirectional sampling based motion planning by incorporating the proposed bidirectional potential gradient heuristics for alternativel directing each successive randomly sampled state towards each of the two trees out of the bidi.

rectional trees and hence guiding both trees towards each other for faster convergence to optimal solution. This paper presents new bidirectional potential gradient heuristics, to potentially guide and directionalize two Rapidly-exploring Random trees towards each other in the bidirectional versions of RRT\*, and hence the two proposed algorithms are the Potentially Guided Bi-directional RRT\* (PB-RRT\*) and Potentially Guided Intelligent Bi-directional RRT\* (PIB-RRT\*). The idea of potentially guiding two Rapidly exploring Random Trees towards each other for faster rate of convergence to optimal solution, as per authors knowledge, is novel.

In this paper PB-RRT\* and PIB-RRT\* have been rigorously tested in challenging 2-D and 3-D environments and are compared with the latest optimal sampling based algorithms such as RRT\*, IB-RRT\* and $\mathrm { P - R R T ^ { * } }$ . The remainder of the paper is divided into following sections. Section 2 and 3 gives an explanation of our problem definition and a review of some previous algorithms. Section 4 explains our proposed algorithms, PB-RRT\* and PIB-RRT\*. Section 5 presents in depth analysis of the proposed PB-RRT\* and PIB-RRT\* algorithms regarding their probabilistic completeness, asymptotic optimality, rapid asymptotic convergence to optimal path, computational complexity and eficiency. Section 6 follows up with experimental proof, supporting the theoretical implications. Section 7 concludes the paper with some suggestions for further research in the future. Section 8 closes the paper with acknowledgments followed by references.

## 2. Problem definition

This section describes the motion planning algorithms that will be addressed in this paper along with the notations used. In the motion planning problem, a feasible path from initial state to the goal region has to be found in the least amount of time possible. Let $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ represent the two Rapidly-exploring Random Trees growing from initial and goal state, respectively. The state space of the configuration space is represented by the set $\mathrm { ~ Z ~ } \subset \ \mathbb { R } ^ { \mathrm { n } } , \ n \in \mathbb { N }$ and $n \geq 2 .$ , where n is the number of dimensions and $z \in \mathrm { Z }$ is a particular configuration of the robot. $Z _ { \mathrm { o b s } } \subset \mathrm { Z }$ are the states that are present in our obstacle configuration space and are a no go configuration for the robot. $Z _ { \mathrm { f r e e } }$ are the traversable states for the robot such that $Z _ { \mathrm { f r e e } } = Z / Z _ { \mathrm { o b s } }$ . Let $V _ { \mathrm { a } }$ and $E _ { \mathrm { a } }$ be the vertices and edges of the tree $T _ { \mathrm { a } }$ such that $T _ { \mathrm { a } } = ( V _ { \mathrm { a } } , E _ { \mathrm { a } } ) \subset Z _ { \mathrm { f r e e } } .$ Similarly for tree $T _ { \mathrm { b } } ,$ $T _ { \mathrm { b } } = ( V _ { \mathrm { b } } , E _ { \mathrm { b } } ) \subset Z _ { \mathrm { f r e e } }$ . Let $\mu ( . )$ be the Lebesgue measure, which denotes the n-dimensional volume of the given state space. Let a path be denoted by $\tau : [ 0 , 1 ]$ and $\Sigma _ { \mathrm { f r e e } }$ is the set of all collision free paths. Let $\tau _ { \mathrm { a } } ^ { ' }$ be the path of tree $T _ { \mathrm { a } }$ from initial state $z _ { \mathrm { i n i t } }$ to any random state z, such that $\tau _ { \mathrm { a } } ^ { ' } [ 0 , 1 ] \right. \{ \tau _ { \mathrm { a } } ^ { ' } ( 0 ) \stackrel { \left. } { = } z _ { \mathrm { i n i t } } , \tau _ { \mathrm { a } } ^ { ' } ( 1 ) = z \} \subset Z _ { \mathrm { f r e e } }$ . Similarly for tree $T _ { \mathrm { b } } , \tau _ { \mathrm { b } } ^ { ' }$ is the path from goal state $z _ { \mathrm { g o a l } }$ to any random state z such that $\tau _ { \mathrm { b } } ^ { ' } [ 0 , 1 ]  \{ \tau _ { \mathrm { b } } ^ { ' } ( 1 ) = z , \tau _ { \mathrm { b } } ^ { ' } ( 0 ) = z _ { \mathrm { g o a l } } \} \subset Z _ { \mathrm { f r e e } }$ . In order to get a solution, both trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ must be connected such that $\tau _ { \mathrm { a } } ^ { ' } ( 1 ) = \tau _ { \mathrm { b } } ^ { ' } ( 1 ) = z$ . Then the resulting concatenated solution will be given by $\tau _ { \mathrm { f } } ^ { ' } = \tau _ { \mathrm { a } } ^ { ' } \mid \tau _ { \mathrm { b } } ^ { ' } \in Z _ { \mathrm { f r e e } }$ . Finally, let $J ( \tau )$ be the cost of the path τ in terms of Euclidean metric in $Z . ~ U : \mathbb { R } ^ { \mathrm { d } }  \mathbb { R }$ describes the artificial potential function. Let $I _ { \mathrm { z } }$ describe the intensity of near vertices and $\vartheta _ { \mathrm { A L G } }$ denote the total rewiring per iteration of Algorithm ALG. Optimal path planning is a very basic requirement of motion planning. It is formally defined below.

Optimal Path Planning: Optimal path planning problem is formally defined as given a path planning triplet $\{ z _ { \mathrm { i n i t } } , Z _ { \mathrm { g o a l } } , Z _ { \mathrm { f r e e } } \}$ and a path cost function $J ( . )$ . From all the feasible collision-free paths $\Sigma _ { \mathrm { f r e e } } .$ , find a path $\tau ^ { * } \in \Sigma _ { \mathrm { f r e e } }$ that minimizes the given function of path cost $J : \Sigma _ { \mathrm { f r e e } }  \mathbb { R } \geq 0$ such that $\tau ^ { * } : [ 0 , 1 ] \to \tau ^ { * } ( 0 ) = z _ { \mathrm { i n i t } } , \tau ^ { * } ( 1 ) = Z _ { \mathrm { g o a l } }$ . Optimal path $\tau ^ { * }$ can hence be formally written as the following.

$$
J (\tau^ {*}) = \underset {\tau \in \Sigma_ {\mathrm{free}}} {\operatorname{argmin}} \{J (\tau) | \tau (0) = z _ {\mathrm{init}}, \tau (1) = Z _ {\mathrm{goal}}, \tau : [ 0, 1 ] \in \Sigma_ {\mathrm{free}} \}
$$

## 3. Related work

In this section, previously proposed algorithms such as Potential Function Based-RRT\* (P-RRT\*) [29], Bi-directional RRT\* (B-RRT\*) [32] and Intelligent Bi-directional RRT\* (IB-RRT\*) [34] are briefly explained. These algorithms form the base of our proposed Potentially Guided Bidirectionalized RRT\*.

(a) i=197344,t=47s,J=241

![](Tahir2018Potentially_figs/a8ff36e1d9fc5001702dc82a88e76ef1fcc2b7140b303f0d4d39e93b278256db.jpg)

![](Tahir2018Potentially_figs/034b9e972f070ab880fc027b3b99c1b5d7e910a8bf44b364d91a3b00b101f411.jpg)

![](Tahir2018Potentially_figs/9c7974d714cfac20d561684eb8d448b1a27ad4ae49274733651214ce4c0a4996.jpg)

![](Tahir2018Potentially_figs/bd6ae6aa54c751fce60042ae2d36963cd20f19b2baffc59921a2c97183f56d52.jpg)

Figure 1: PIB-RRT\*, PB-RRT\* & RRT\* performance comparison in 2-D Maze  
```txt
Algorithm 1: P-RRT* (zinit, zgoal)

1 Va ← {zinit};
2 Ea ← ∅;
3 T ← (V, E);
4 for i ← 0 to N do
5    zrand ← RandSample(i);
6    zprand ← RGD(zrand);
7    Znear ← NeighboringVertices(i, T, zprand);
8    if Znear = ∅ then
9    Znear ← NearestVertex(T, zprand);
10    L ← ListSorting(zprand, Znear);
11    zparent ← PickBestParent(L);
12    if zparent then
13    T(V, E) ← VertexInsert(zprand, zparent, T);
14    E ← RewiringVertices(zprand, L, E);
15 return T(V, E)
```

## 3.1. P-RRT\* Algorithm

The P-RRT\* [29] Algoithm extends the RRT\* Algorithm for better convergence properties by introducing a Random Gradient Descent (RGD) method. The RGD method guides the randomly sampled states towards the goal region using APF [19]. This guiding by P-RRT\* results into faster computation of an optimal solution as compared to the original RRT\* method. Algorithm 1 outlines the pseudo-code of P-RRT\*. The procedures used in Algorithm 1 are described below.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: ListSorting( $z_{rand}$ ,  $Z_{near}$ )

1  $L \leftarrow \emptyset$ ;

2 while  $z' \in Z_{near}$  do

3  $\tau' \leftarrow Steer(z', z_{rand})$ ;

4  $J' \leftarrow J(z_{init}, z') + J(z', z_{rand})$ ;

5  $L \leftarrow (z', J', \tau')$ ;

6  $L \leftarrow Sort(L)$ ;

7 return L
</div>

RandSample: This function returns independent and identically distributed (i.i.d.) samples form the obstacle-free space as $z _ { \mathrm { r a n d } } \in Z _ { \mathrm { f r e e } }$

RGD: This heuristic guides the randomly sampled state z incrementally downhill in the direction of decreasing potential so that the resulting guided samples is z<sub>prand</sub>.

NeighboringVertices: This procedure returns the vertices that are the neighboring vertices of the randomly sampled state $z _ { \mathrm { r a n d } }$ located inside a ball of volume $B _ { z , r }$ of radius r centered at z such that $r = \gamma ( \log n / n ) ^ { 1 / d }$ , where $\gamma$ is a constant, n is the number of vertices and d is the dimension of the state space.

NearestVertex: As suggested from its name, this function returns the vertex from the tree $T ( V , E )$ which is nearest to the randomly sampled vertex in terms of cost determined by the cost heuristic function $J ( )$

ListSorting: This function sorts the list L in terms of ascending order of its cost $J ^ { \prime }$ as seen in Algorithm 2.

Steer: This function takes two states $z _ { 1 }$ and $z _ { 2 }$ as inputs and connects them in such a way that a straight trajectory collision-free path $\tau : [ 0 , 1 ]$ is formed such that $\tau ( 0 ) = z _ { 1 }$ and $\tau ( 1 ) = z _ { 2 }$ Steering is done in small incremental step.

PickBestParent: This procedure chooses the parent $z _ { \mathrm { p a r e n t } } \in Z _ { \mathrm { n e a r } }$ for the randomly sampled state which returns a collision-free path $\tau ^ { \prime }$ with the minimum cost from $z _ { \mathrm { i n i t } }$ to the randomly sampled state.

VertexInsert: Given a vertex z, this method assigns a parent $z _ { \mathrm { p a r e n t } }$ to the $\mathrm { v e r t e x ~ } z .$ , and then computes the edge connecting the assigned parent $z _ { \mathrm { p a r e n t } }$ and the vertex z. Furthermore, it also determines the cost connecting $z _ { \mathrm { i n i t } }$ to z via z . Finally, this vertex z and edge are interested into the tree $T ( V , E )$

RewiringVertices: This function checks if the cost of the vertices in $Z _ { \mathrm { n e a r } }$ in terms of Euclidean distance from the root state of the tree they belong to, is less through the new randomly sampled state than through their original parents. If so, then their original parents are removed and the randomly sampled vertex/state is made their new parent.

The P-RRT\* Algorithm presented in Algorithm 1 is also asymptotically optimal like its baseline Algorithm $\mathrm { R R T ^ { * } }$ . Along with being asymptotically optimal it is also probabilistically complete. But due to incorporation of $\mathrm { A P F }$ into $\mathrm { R R T ^ { * } }$ in $\mathrm { P - R R T ^ { * } }$ it is many folds faster than its parent $\mathrm { R R T ^ { * } }$ in finding the optimal solution especially in cluttered environments. First the tree $T ( V , E )$ is initialized with its first vertex $z _ { \mathrm { i n i t } }$ . Then as iteration, i, goes from 0 to N, $z _ { \mathrm { r a n d } } \in Z _ { \mathrm { f r e e } }$ is randomly sampled from obstacle-free configuration space $Z _ { \mathrm { f r e e } } .$ . After this the randomly sampled state $z _ { \mathrm { r a n d } }$ is potentially guided by the RGD() heuristic downhill towards decreasing potential so that it becomes $z _ { \mathrm { p r a n d } }$ (line $6 ,$ Algorithm 1). Then the $\mathrm { P - R R T ^ { * } }$ searches its neighboring vertices located around the potentially guided randomly sampled state $z _ { \mathrm { p r a n d } }$ in a ball of of volume $\boldsymbol { B } _ { z , r }$ to form the set $Z _ { \mathrm { n e a r } }$ . If this set $Z _ { \mathrm { n e a r } }$ is empty it then populates $Z _ { \mathrm { n e a r } }$ with the nearest vertex to $z _ { \mathrm { p r a n d } }$ located anywhere in the tree (line 8–9, Algorithm 1). $\mathrm { P - R R T ^ { * } }$ then makes a list $L$ of neighboring vertices $Z _ { \mathrm { n e a r } }$ in the function ListSorting() as explained in Algorithm 2. This list $L$ is made in ascending order of the total cost $J ^ { \prime }$ . The total cost $J ^ { \prime }$ (line 4, Algorithm 2) is the sum of the cost of a collision-free path (in terms of Euclidean distance) of the neighboring vertex $z ^ { \prime } \in Z _ { \mathrm { n e a r } }$ from root state $z _ { \mathrm { i n i t } }$ plus the cost of the collision-free path from the neighboring vertex $z ^ { \prime } \in Z _ { \mathrm { n e a r } }$ to the potentially guided randomly sampled state $z _ { \mathrm { p r a n d } }$ . Then coming back to Algorithm 1, the function P ickBestP arent() chooses the vertex $z ^ { \prime } \in \mathrm { \bar { Z } } _ { \mathrm { n e a r } }$ as the parent of the sample $z _ { \mathrm { p r a n d } }$ which has the least cost $J ^ { \prime }$ returning a collision-free path $\tau ^ { \prime } .$ . Then the vertex $z _ { \mathrm { p r a n d } }$ is added to the tree $T ( V , E )$ and rewiring is done around $z _ { \mathrm { p r a n d } }$ (line 12–14, Algorithm 1). This process is repeated until $i  N$

## 3.2. B-RRT\* Algorithm

Jordan and Perez [32] came up with optimal Bi-directional Rapidly-exploring Random trees in their B-RRT\* Algorithm. It is implemented as shown in Algorithm 3. Some of the new functions used by B-RRT\* are as follows.

Extend: Extend $\begin{array} { r l } {  { \operatorname { l } ( z _ { 1 } , z _ { 2 } ) } } \end{array}$ returns a new vertex $z _ { \mathrm { n e w } }$ such that $z _ { \mathrm { n e w } } \in Z _ { \mathrm { f r e e } }$ and $z _ { \mathrm { n e w } }$ is closer to $z _ { 2 }$ than $z _ { 1 }$ in terms of cost, the Euclidean distance.

Connect: Algorithm 4 states the Connect heuristic in detail. Just like RRT-connect heuristic [35] it is greedy.

```txt
Algorithm 3: B-RRT* (zinit, zgoal)

1 Va ← {zinit}; Vb ← {zgoal};
2 Ea ← ∅; Eb ← ∅;
3 Ta ← (Va, Ea); Tb ← (Vb, Eb);
4 τbest ← ∞;
5 for i ← 0 to N do
6    zrand ← RandSample(i)
7    znearest ← NearestVertex(zrand, Ta)
8    znew ← Extend(znearest, zrand)
9    Znear ← NeighboringVertices(znew, Ta)
10    L ← ListSorting(znew, Znear);
11    zparent ← PickBestParent(L);
12    if zparent then
13    Ta(Va, Ea) ← VertexInsert(znew, zparent, Ta);
14    Ea ← RewiringVertices(znew, L, Ea);
15    zconn ← NearestVertex(znew, Tb)
16    τnew ← Connect(znew, zconn, Tb)
17    if τnew ≠ ∅ and J(τnew) < J(τbest) then
18    τbest ← τnew;
19    SwapTrees(Ta, Tb);
20 return {Ta, Tb} = (V, E)
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4: Connect($z_1, z_2, T_b$)
1 $z_{\text{new}} \leftarrow Extend(z_2, z_1)$
2 $Z_{\text{near}} \leftarrow NeighboringVertices(z_{\text{new}}, T_b)$
3 List $\leftarrow$ ListSorting($z_1, Z_{\text{near}}$);
4 $z_{\text{parent}} \leftarrow$ PickBestParent(List);
5 if $z_{\text{parent}}$ then
6    $E \leftarrow (z_{\text{parent}}, z_1)$;
7    $\tau_{\text{free}} \leftarrow MakePath(z_{\text{parent}}, z_1)$;
8    return $\tau_{\text{free}}$
9 return NULL
</div>

B-RRT\* is explained in detail in Algorithm 3. It first initializes two trees, $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ $T _ { \mathrm { a } }$ is initialized by $z _ { \mathrm { i n i t } }$ as its root vertex such that $z _ { \mathrm { i n i t } } \in Z _ { \mathrm { f r e e } } . \quad T _ { \mathrm { b } }$ is initialized with $z _ { \mathrm { g o a l } }$ as its root vertex where $z _ { \mathrm { g o a l } } \in Z _ { \mathrm { g o a l } }$ . The initial operations are just like $\mathrm { R R T ^ { * } }$ where first a vertex is randomly sampled, then after insertion and rewiring of the sample into the selected tree $T _ { \mathrm { a } } ,$ zconn is searched, which is the nearest vertex from tree $T _ { \mathrm { b } }$ to the node z . Then the Connect heuristic tries to connect the two trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } } .$ , returning a path $\tau _ { \mathrm { n e w } } \in \Sigma _ { \mathrm { f r e e } }$ . If the cost of the new path $J ( \tau _ { \mathrm { n e w } } )$ is less than the previously calculated best cost $J ( \tau _ { \mathrm { b e s t } } ) , \tau _ { \mathrm { b e s t } }$ is overwritten by $\tau _ { \mathrm { n e w } }$ . Then the trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ are swapped and the whole procedure is again executed until $i  N$

## 3.3. IB-RRT\* Algorithm

Qureshi et al. [34] proposed their optimal bidirectional variant of $\mathrm { R R T ^ { * } }$ in his Intelligent Bidirectional RRT\* (IB-RRT\*) Algorithm. The procedures used by this Algorithm are same as the ones used in $\mathrm { R R T ^ { * } }$ except for the GetBestT reeP arent heuristic, which has been explained below.

GetBestTreeParent: This heuristic calculates the best parent with the minimum cost from both trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ around the randomly sampled $z _ { \mathrm { r a n d } }$ . Then the parent which has the least cost among the two trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ is made the parent of the randomly sampled state $z _ { \mathrm { r a n d } }$

Algorithm 5 outlines the implementation of $\mathrm { I B { - } R R T ^ { * } }$ . First the two trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ are initialized with their respective vertices (line 1–2). Then a vertex is randomly sampled and the near neighbor vertices from both trees are calculated in $Z _ { \mathrm { n e a r } } ^ { \mathrm { a } }$ and $Z _ { \mathrm { n e a r } } ^ { \mathrm { b } }$ (line 6–9). Both the neighboring vertex sets $Z _ { \mathrm { n e a r } } ^ { \mathrm { a } }$ and $Z _ { \mathrm { n e a r } } ^ { \mathrm { b } }$ are sorted in ascending order by the function ListSorting (line 10–11). Then the GetBestT reeP arent heuristic selects the best parent $z _ { \mathrm { m i n } }$ from $T _ { \mathrm { a } }$ or $T _ { \mathrm { b } }$ . If the best parent $z _ { \mathrm { m i n } }$ is from $T _ { \mathrm { a } }$ then $z _ { \mathrm { r a n d } }$ is inserted in $T _ { \mathrm { a } }$ along with its edges and is then rewired (line 13–15). And if the best parent $z _ { \mathrm { m i n } }$ is from $T _ { \mathrm { b } }$ then $z _ { \mathrm { r a n d } }$ is inserted in $T _ { \mathrm { b } }$ and rewired (line 16–18). This process continues till $i  N$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5: IB-RRT* (zinit, zgoal)

1  $V_{a} \leftarrow \{z_{init}\}; V_{b} \leftarrow \{z_{goal}\};$ 

2  $E_{a} \leftarrow \emptyset; E_{b} \leftarrow \emptyset;$ 

3  $T_{a} \leftarrow (V_{a}, E_{a}); T_{b} \leftarrow (V_{b}, E_{b});$ 

4  $\tau_{best} \leftarrow \infty;$ 

5 Connection  $\leftarrow$  True

6 for i  $\leftarrow$  0 to N do

7    $z_{rand} \leftarrow RandSample(i)$ 

8    $\{Z_{near}^{a}, Z_{near}^{b}\} \leftarrow NeighboringVertices(z_{rand}, T_{a}, T_{b})$ 

9    if  $Z_{near}^{a} = \emptyset$  and  $Z_{near}^{b} = \emptyset$  then

10    $\{Z_{near}^{a}, Z_{near}^{b}\} \leftarrow NearestVertex(z_{rand}, T_{a}, T_{b})$ 

11    Connection  $\leftarrow$  False

12    $L_{a} \leftarrow ListSorting(z_{rand}, Z_{near}^{a})$ 

13    $L_{b} \leftarrow ListSorting(z_{rand}, Z_{near}^{b})$ 

14    $\{z_{parent}, flag, \tau_{free}\} \leftarrow GetBestTreeParent(L_{a}, L_{b}, Connection)$ 

15    if (flag) then

16    $T_{a} \leftarrow VertexInsert(z_{rand}, z_{parent}, T_{a})$ 

17    $T_{a} \leftarrow RewiringVertices(z_{rand}, L_{a}, E_{a})$ 

18    else

19    $T_{b} \leftarrow VertexInsert(z_{rand}, z_{parent}, T_{b})$ 

20    $T_{b} \leftarrow RewiringVertices(z_{rand}, L_{b}, E_{b})$ 

21   $E \leftarrow E_{a} \cup E_{b}$ 

22   $V \leftarrow V_{a} \cup V_{b}$ 

23 return ( $\{T_{a}, T_{b}\} = V, E$ )
</div>

## 4. Potentially Guided Bidirectionalized RRT\*

## 4.1. PB-RRT\* & PIB-RRT\*

In this section we present our proposed algorithms, PB-RRT\* (Potentially Guided Bi-directional RRT\*) and PIB-RRT\* (Potentially Guided Intelligent Bi-directional RRT\*). The proposed algorithms PB-RRT\* and PIB-RRT\* incorporate APF (Artificial Potential Fields) [19] into Bidirectional RRT\* (B-RRT\*) [32] and Intelligent Bi-directional RRT\* (IB-RRT\*) [34] respectively by using the proposed $B P G ( )$ (Bi-directional Potential Gradient) heuristic. $B P G ( )$ heuristic has been explained later in this section. The APF was introduced by Khatib [19]. In this method the artificial potential field $U _ { \mathrm { a t t } }$ pulls the robot $R _ { \mathrm { i } }$ located at position $z \in Z _ { \mathrm { f r e e } }$ towards the goal region $z _ { \mathrm { g } } \in Z _ { \mathrm { g o a l } }$ and the artificial potential field $U _ { \mathrm { r e p } }$ repels the robot away from obstacles lying in the obstacle configuration space $Z _ { \mathrm { o b s } }$ . Force $\hat { F } _ { \mathrm { r } }$ generated on the robot is the negative gradient of the resultant potential i.e, $\hat { F } _ { \mathrm { r } } = - g r a d [ U _ { \mathrm { r } } ]$

$$
U _ {\mathrm{att}} = \left\{ \begin{array}{l l} \frac {1}{2} k _ {\mathrm{p}} \| z - z _ {\mathrm{g}} \| ^ {2}, & \mathrm{if} \| z - z _ {\mathrm{g}} \| > r _ {\mathrm{g}} \\ \frac {1}{2} k _ {\mathrm{p}} (r _ {\mathrm{g}} \| z - z _ {\mathrm{g}} \| - r _ {\mathrm{g}} ^ {2}), & \mathrm{if} \| z - z _ {\mathrm{g}} \| \leq r _ {\mathrm{g}} \end{array} \right.\tag{1}
$$

$$
\hat {F} _ {\mathrm{att}} = \left\{ \begin{array}{l l} - k _ {\mathrm{p}} \| z - z _ {\mathrm{g}} \|, & \mathrm{if} \| z - z _ {\mathrm{g}} \| > r _ {\mathrm{g}} \\ - k _ {\mathrm{p}} r _ {\mathrm{g}} \frac {\| z - z _ {\mathrm{g}} \|}{d (z , z _ {\mathrm{g}})}, & \mathrm{if} \| z - z _ {\mathrm{g}} \| \leq r _ {\mathrm{g}} \end{array} \right.\tag{2}
$$

Where $r _ { \mathrm { g } }$ is the radius of the boundary around the goal region $z _ { \mathrm { g } } \in Z _ { \mathrm { g o a l } } . \ k _ { \mathrm { p } }$ is the attractive potential gain.

$$
d _ {\mathrm{nearest}} ^ {*} = \underset {z ^ {\prime} \in Z _ {\mathrm{obs}}} {\mathrm{argmin}} \| z - z ^ {\prime} \|\tag{3}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 6: PB-RRT* (zinit, zgoal)

1  $V_{a} \leftarrow \{z_{init}\}; V_{b} \leftarrow \{z_{goal}\};$ 

2  $E_{a} \leftarrow \emptyset; E_{b} \leftarrow \emptyset;$ 

3  $T_{a} \leftarrow (V_{a}, E_{a}); T_{b} \leftarrow (V_{b}, E_{b});$ 

4  $\tau_{best} \leftarrow \infty;$ 

5 for i  $\leftarrow 0$  to N do

6  $z_{rand} \leftarrow RandSample(i)$ 

7  $z_{pb} \leftarrow BPG(z_{rand}, i)$ 

8  $z_{nearest} \leftarrow NearestVertex(z_{pb}, T_{a})$ 

9  $z_{new} \leftarrow Extend(z_{nearest}, z_{pb})$ 

10  $Z_{near} \leftarrow NeighboringVertices(z_{new}, T_{a})$ 

11  $L \leftarrow ListSorting(z_{new}, Z_{near});$ 

12  $z_{parent} \leftarrow PickBestParent(L);$ 

13 if  $z_{parent}$  then

14  $T_{a}(V_{a}, E_{a}) \leftarrow VertexInsert(z_{new}, z_{parent}, T_{a});$ 

15  $E_{a} \leftarrow RewiringVertices(z_{new}, L, E_{a});$ 

16  $z_{conn} \leftarrow NearestVertex(z_{new}, T_{b})$ 

17  $\tau_{new} \leftarrow Connect(z_{new}, z_{conn}, T_{b})$ 

18 if  $\tau_{new} \neq \emptyset$  and  $J(\tau_{new}) &lt; J(\tau_{best})$  then

19  $\tau_{best} \leftarrow \tau_{new};$ 

20 SwapTrees( $T_{a}, T_{b}$ );

21 return  $\{T_{a}, T_{b}\} = (V, E)$
</div>

$$
U _ {\mathrm{rep}} = \left\{ \begin{array}{l l} \frac {1}{2} k _ {\mathrm{rep}} (\frac {1}{d _ {\mathrm{nearest}} ^ {*}} - \frac {1}{d _ {\mathrm{obs}}}) ^ {2}, & \text {if} d _ {\mathrm{nearest}} ^ {*} \leq d _ {\mathrm{obs}} ^ {*} \\ 0, & \text {if} d _ {\mathrm{nearest}} ^ {*} > d _ {\mathrm{obs}} ^ {*} \end{array} \right.\tag{4}
$$

$$
U _ {\mathrm{r}} = U _ {\mathrm{att}} + U _ {\mathrm{rep}}\tag{5}
$$

$$
\hat {F} _ {\mathrm{r}} = \hat {F} _ {\mathrm{att}} + \hat {F} _ {\mathrm{rep}}\tag{6}
$$

In reference to Equation 3, $d _ { \mathrm { n e a r e s t } } ^ { \ast }$ is the distance of the robot to the nearest obstacle. $d _ { \mathrm { o b s } }$ is a constant value and is usually very small. In Equation 4, $k _ { \mathrm { r e p } }$ is the repulsive potential gain. The resultant force on the robot is $\hat { F } _ { \mathrm { r } }$ i.e, $\hat { F } _ { \mathrm { r } } = - g r a d [ U _ { \mathrm { r } } ]$ where $U _ { \mathrm { r } } = U _ { \mathrm { a t t } } + U _ { \mathrm { r e p } }$ as seen in Equation 5. Force $F _ { \mathrm { r } }$ keeps acting on the robot until $- g r a d [ U _ { \mathrm { r } } ] = 0$ and when this zero potential gradient condition happens and $\hat { F } _ { \mathrm { r } } = 0$ then the robot has either reached its goal or is stuck in a local minima configuration.

The proposed PB-RRT\* and PIB-RRT\* fuse APF (Artificial Potential Fields) [19] with bidirectional variants of RRT\* [32] [34] using the BP G() heuristic. The pseudo code of PB-RRT\* and PIB-RRT\* is given in Algorithm 6 and 7 respectively. The flow of the algorithms PB-RRT\* and PIB-RRT\* is the same as that of B-RRT\* (Algorithm 3) and $\mathrm { I B { - } R R T ^ { * } }$ (Algorithm 4) respectively, with only diference of BP G() heuristic. Hence only BP G() heuristic is discussed in detail.

## 4.2. BPG()

APF [19] is incorporated in the proposed algorithms PB-RRT\* and PIB-RRT\* using the proposed BP G() (Bi-directional Potential Gradient) heuristic. Pseudo-code of $B P G ( )$ heuristic is presented in Algorithm 8. Let $z _ { \mathrm { r a n d } } \in Z _ { \mathrm { f r e e } }$ be the randomly sampled state. After being potentially guided by the BP G() heuristic, the randomly sampled state $z _ { \mathrm { r a n d } }$ becomes potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ such that $z _ { \mathrm { r a n d } }  z _ { \mathrm { p b } }$ , where $z _ { \mathrm { p b } } \in Z _ { \mathrm { f r e e } }$ . Some of the new heuristics used by BP G() are discussed below.

BPGgoal $( Z _ { \mathrm { g o a l } } , z _ { \mathrm { p b } } ) { : }$ BP Ggoal() (Bi-directional Potential Gradient towards goal state) implements Equation 1 and Equation 2 of the APF Algorithm in the form of Equation 7 and Equation 8 as shown below.

$$
U _ {\mathrm{att}} = \frac {1}{2} k _ {\mathrm{p}} \| z _ {\mathrm{rand}} - z _ {\mathrm{goal}} \| ^ {2}: z _ {\mathrm{goal}} \in Z _ {\mathrm{goal}}\tag{7}
$$

$$
\hat {F} _ {\mathrm{att}} = - k _ {\mathrm{p}} \left\| z _ {\mathrm{rand}} - z _ {\mathrm{goal}} \right\|: z _ {\mathrm{goal}} \in Z _ {\mathrm{goal}}\tag{8}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 7: PIB-RRT* (zinit, zgoal)

1  $V_{a} \leftarrow \{z_{init}\}; V_{b} \leftarrow \{z_{goal}\};$ 

2  $E_{a} \leftarrow \emptyset; E_{b} \leftarrow \emptyset;$ 

3  $T_{a} \leftarrow (V_{a}, E_{a}); T_{b} \leftarrow (V_{b}, E_{b});$ 

4  $\tau_{best} \leftarrow \infty;$ 

5 Connection  $\leftarrow$  True

6 for  $i \leftarrow 0$  to N do

7  $z_{rand} \leftarrow \text{RandSample}(i)$ 

8  $z_{pb} \leftarrow \text{BPG}(z_{rand}, i)$ 

9  $\{Z_{near}^{a}, Z_{near}^{b}\} \leftarrow \text{NehighboringVertices}(z_{pb}, T_{a}, T_{b})$ 

10 if  $Z_{near}^{a} = \emptyset$  and  $Z_{near}^{b} = \emptyset$  then

11  $\{Z_{near}^{a}, Z_{near}^{b}\} \leftarrow \text{NearestVertex}(z_{pb}, T_{a}, T_{b})$ 

12 Connection  $\leftarrow$  False

13  $L_{a} \leftarrow \text{ListSorting}(z_{pb}, Z_{near}^{a})$ 

14  $L_{b} \leftarrow \text{ListSorting}(z_{pb}, Z_{near}^{b})$ 

15  $\{z_{parent}, flag, \tau_{free}\} \leftarrow \text{GetBestTreeParent}(L_{a}, L_{b}, \text{Connection})$ 

16 if (flag) then

17  $T_{a} \leftarrow \text{VertexInsert}(z_{pb}, z_{parent}, T_{a})$ 

18  $T_{a} \leftarrow \text{RewiringVertices}(z_{pb}, L_{a}, E_{a})$ 

19 else

20  $T_{b} \leftarrow \text{VertexInsert}(z_{pb}, z_{parent}, T_{b})$ 

21  $T_{b} \leftarrow \text{RewiringVertices}(z_{pb}, L_{b}, E_{b})$ 

22  $E \leftarrow E_{a} \cup E_{b}$ 

23  $V \leftarrow V_{a} \cup V_{b}$ 

24 return ( $\{T_{a}, T_{b}\} = V, E$ )
</div>

As seen in Algorithm 8 in the $B P G ( )$ heuristic if the iteration count i is even then the potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ is passed to the $B P G g o a l ( )$ heuristic. In the $B P G g o a l ( )$ heuristic, Equation 8 is used for the calculation of attractive potential force vector $\hat { F } _ { \mathrm { a t t } } . \quad \hat { F } _ { \mathrm { a t t } }$ is acting on $z _ { \mathrm { p b } }$ with the goal region $Z _ { \mathrm { g o a l } }$ acting as the attractive pole pulling $z _ { \mathrm { p b } }$ towards it. Hence the name $B P G g o a l ( )$ is given to this function. $k _ { \mathrm { p } }$ is the attractive potential gain. It is to be noted that the canonical portion of Equation 1 and Equation 2 is ignored in their implementation in Equation 7 and Equation 8 of $B P G g o a l ( )$ as the potential force is being applied on the randomly sampled state and not physically on the robot hence it does not need to be slowed down by the canonical portion of the equation for avoidance of over-shooting $Z _ { \mathrm { g o a l } }$

NearestObstacleSearch $\prime ( Z _ { \mathrm { o b s } } , z _ { \mathrm { p b } } )$ : This heuristic computes the distance $d _ { \mathrm { n e a r e s t } } ^ { \ast }$ of the nearest obstacle in the obstacle-space from the bidirectional potential gradient randomly sampled state $z _ { \mathrm { p b } }$

$B P G i n i t ( z _ { \mathrm { i n i t } } , z _ { \mathrm { p b } } ) { : }$ BP Ginit() (Bi-directional Potential Gradient towards initial state) uses the Equation 1 and Equation 2 of the APF Algorithm in their modified form in Equation 9 and Equation 10 as shown below.

$$
U _ {\mathrm{att}} ^ {\prime} = \frac {1}{2} k _ {\mathrm{p}} \| z _ {\mathrm{rand}} - z _ {\mathrm{init}} \| ^ {2}: z _ {\mathrm{init}} \in Z _ {\mathrm{free}}\tag{9}
$$

$$
\hat {F} _ {\mathrm{att}} ^ {\prime} = - k _ {\mathrm{p}} \big \| z _ {\mathrm{rand}} - z _ {\mathrm{init}} \big \|: z _ {\mathrm{init}} \in Z _ {\mathrm{free}}\tag{10}
$$

When the iteration count i is odd in $B P G ( )$ heuristic then the potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ is passed to the BP Ginit() heuristic. Using Equation 9 and Equation 10, $B P G n i t ( )$ heuristic computes the attractive potential force vector $\hat { F } _ { \mathrm { a t t } } ^ { \prime }$ acting on $z _ { \mathrm { p b } }$ with the initial root state $z _ { \mathrm { i n i t } }$ acting as the attractive pole for $z _ { \mathrm { p b } }$ . Hence the name $B P G n i t ( )$ is given to this heuristic. Similarly as in $B P F G o a l ( )$ heuristic, the canonical portion of Equation 1 and Equation 2 are ignored. $k _ { \mathrm { p } }$ is the attractive potential gain.

Algorithm 8 explains in detail $B P G ( )$ (Bi-directional Potential Gradient) heuristic. The randomly sampled state $z _ { \mathrm { r a n d } }$ is first fed to potentially guided bidirectional randomly sampled state variable $z _ { \mathrm { p b } }$ (line 1). The iteration count i being currently run in the main loop is taken in $B P G ( )$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 8: BPG ( $z_{rand}, i$ )

1  $z_{pb} \leftarrow z_{rand};$ 

2 if i mod 2 = 0 then

3 for  $k \leftarrow 0$  to n do

4  $\hat{F}_{att} = BPGgoal(Z_{goal}, z_{pb});$ 

5  $d_{nearest}^{*} \leftarrow NearestObstacleSearch(Z_{obs}, z_{pb});$ 

6 if  $d_{nearest}^{*} \leq d_{obs}^{*}$  then

7 return  $z_{pb}$ 

8 else

9  $z_{pb} \leftarrow z_{pb} + \epsilon \frac{\hat{F}_{att}}{\|\hat{F}_{att}\|}$ 

10 else

11 for  $k \leftarrow 0$  to n do

12  $\hat{F}_{att}' = BPGinit(z_{init}, z_{pb});$ 

13  $d_{nearest}^{*} \leftarrow NearestObstacleSearch(Z_{obs}, z_{pb});$ 

14 if  $d_{nearest}^{*} \leq d_{obs}^{*}$  then

15 return  $z_{pb}$ 

16 else

17  $z_{pb} \leftarrow z_{pb} + \epsilon \frac{\hat{F}_{att}'}{\|\hat{F}_{att}'\|}$ 

18 return  $z_{pb}$
</div>

heuristic as an input. If the iteration count i is even then $z _ { \mathrm { p b } }$ is passed to the $B P G g o a l ( )$ heuristic which computes the potential force vector $\hat { F } _ { \mathrm { a t t } }$ acting on $z _ { \mathrm { p b } }$ with the goal region $Z _ { \mathrm { g o a l } }$ acting as the attractive pole for $z _ { \mathrm { p b } }$ (line 4). Then the distance to the nearest obstacle $d _ { \mathrm { n e a r e s t } } ^ { \ast }$ from the sample $z _ { \mathrm { p b } }$ is computed (line 5). If this distance $d _ { \mathrm { n e a r e s t } } ^ { \ast }$ is smaller than a certain constant value $d _ { \mathrm { o b s } } ^ { \ast }$ then the loop breaks and returns $z _ { \mathrm { p b } } . ~ d _ { \mathrm { o b s } } ^ { \ast }$ must be a very small value, its importance will be told in the coming section. But if $d _ { \mathrm { n e a r e s t } } ^ { \ast } > d _ { \mathrm { o b s } } ^ { \ast }$ then the sample $z _ { \mathrm { p b } }$ is directed down-hill in direction of decreasing potential towards goal region in $\epsilon$ sized small steps (line 9). This loop continues in the same way until $k  n$ where $n \in \mathbb { N } .$ . But if i is odd then the potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ is passed to the $B P G n i t ( )$ heuristic which computes th potential force vector $\hat { F } _ { \mathrm { a t t } } ^ { \prime }$ acting on the potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ with the initial root state $z _ { \mathrm { i n i t } }$ acting as the attractive pole for $z _ { \mathrm { p b } }$ (line 12). The rest of the procedure is same as mentioned above until either $d _ { \mathrm { n e a r e s t } } ^ { \ast } \leq d _ { \mathrm { o b s } } ^ { \ast }$ or until $k  n$ . In this way for even iterations i, the potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ is potentially directed down-hill towards goal region $Z _ { \mathrm { g o a l } }$ by the potential force vector $\hat { F } _ { \mathrm { a t t } } ,$ , bringing it closer to tree $T _ { \mathrm { b } }$ being grown from the goal region $Z _ { \mathrm { g o a l } }$ . While for odd iterations i, the potentially guided bidirectional randomly sampled state $z _ { \mathrm { p b } }$ is pulled towards initial root state $z _ { \mathrm { i n i t } }$ by the potential force vector $\hat { F } _ { \mathrm { a t t } } ^ { \prime }$ where the tree $T _ { \mathrm { a } }$ was grown hence bringing close both the trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ faster by the application of $B P G ( )$ (Bi-directional Potential Gradient) heuristic, hence achieving faster rate of convergence to optimal path as shown in the following sections. In order to keep a balance between exploitation and exploration, the value of n in $k \gets 0$ to $n$ (line 3,11), has to be chosen such that it is not too high that too much exploitation occurs or is too low that no exploitation occurs almost. In the following section we will be analysing our proposed algorithms.

## 5. Analysis

## 5.1. Probabilistic Completeness

Let ALG denote any Algorithm and $G _ { \mathrm { i } }$ denote the sampling-based tree search graph with i total iterations. $V _ { \mathrm { i } }$ is the set of vertices of the tree generated by Algorithm $A L G$ in $\breve { G } _ { \mathrm { i } } ^ { \mathrm { A L \bar { G } } }$

Probabilistic Completeness: For an Algorithm ALG $A L G .$ , it is probabilistically complete, if for any path planning problem triplet $\{ Z _ { \mathrm { f r e e } } , z _ { \mathrm { i n i t } } , Z _ { \mathrm { g o a l } } \}$ , as the total number of iterations i go to infinity, the probability of finding a feasible solution path from initial to goal configuration goes to one.

RRT\* also ensure probabilistic completness (Karaman and Frazzoli 2011) [27] as formally stated below.

Theorem $\mathbf { 1 } ( [ 2 7 ] ) ~ R R T ^ { * }$ is a probabilistically complete Algorithm. For any robustly feasible path planning problem triplet $\{ Z _ { \mathrm { f r e e } } , z _ { \mathrm { i n i t } } , Z _ { \mathrm { g o a l } } \}$ , as the number of iterations approach infinity, the probability of finding a feasible solution approaches one.

$$
\lim _ {i \to \infty} P (\{\exists z _ {\mathrm{goal}} \in V _ {\mathrm{i}} ^ {\mathrm{RRT} *} \cap Z _ {\mathrm{goal}} i n G _ {\mathrm{i}} ^ {\mathrm{RRT} *} \}) = 1
$$

Similarly the proposed algorithms $\mathrm { P B - R R T ^ { * } }$ and $\mathrm { P I B - R R T ^ { * } }$ ensure probabilistic completness as stated in the following Theorem 2.

Theorem 2 For a given feasible path planning problem triplet $\{ Z _ { \mathrm { f r e e } } , z _ { \mathrm { i n i t } } , Z _ { \mathrm { g o a l } } \}$ , the probability of finding a feasible solution is as follows.

$$
\lim _ {i \to \infty} P (\{\exists z _ {\mathrm{goal}} \in V _ {\mathrm{i}} ^ {\mathrm{PB-RRT*}} \cap Z _ {\mathrm{goal}} i n G _ {\mathrm{i}} ^ {\mathrm{PB-RRT*}} \}) = 1
$$

$$
\lim _ {i \to \infty} P (\{\exists z _ {\mathrm{goal}} \in V _ {\mathrm{i}} ^ {\mathrm{PIB-RRT*}} \cap Z _ {\mathrm{goal}} i n G _ {\mathrm{i}} ^ {\mathrm{PIB-RRT*}} \}) = 1
$$

As the number of iterations i approach infinity, probability of finding a feasible solution if one exists, goes to one.

Sketch of proof: For the proof of the above theorem we will use the following three arguments: 1) The bidirectional trees generated by PB-RRT\* and $\mathrm { P I B - R R T ^ { * } }$ just as in $\mathrm { R R T ^ { * } }$ are connected trees i.e, whenever a state is randomly sampled, it is connected to its nearest neighbor state within the particular tree which is selected to grow by the $\mathrm { P B - R R T ^ { * } }$ and $\mathrm { P I B - R R T ^ { * } }$ algorithms respectively; 2) By convention we have $V _ { \mathrm { o } } ^ { \mathrm { R R T * } } \ \stackrel { \sim } { = } \ V _ { \mathrm { o } } ^ { \mathrm { P \tilde { B } } - \mathrm { R R T * } } \ = \ V _ { \mathrm { o } } ^ { \mathrm { P I B - R R T * } } \ = \ z _ { \mathrm { i n i t } }$ , hence the random trees generated by $\mathrm { P B - R R T ^ { * } }$ and $\mathrm { P I B - R R T ^ { * } }$ have $z _ { \mathrm { i n i t } }$ as one of its states just like $\mathrm { R R T ^ { * } ; 3 ) }$ ) PB-RRT\* and $\mathrm { P I B - R R T ^ { * } }$ direct randomly sampled states towards goal region $Z _ { \mathrm { g o a l } }$ and initial root state $z _ { \mathrm { i n i t } }$ at every even and odd loop iteration i respectively by using the $B P G ( )$ heuristic. Therefore in the proposed algorithms $\mathrm { P B - R R T ^ { * } }$ and $\mathrm { P I B - R R T ^ { * } }$ , the probability that the two bi-directional trees grown with their roots at $z _ { \mathrm { i n i t } }$ and $Z _ { \mathrm { g o a l } }$ respectively, will connect to each other and hence find a feasible path approaches to one as the number of iterations i approach infinity. Based on the above stated arguments, it can be stated that the proposed algorithms $\mathrm { P B - R R T ^ { * } }$ and PIB-RRT\* ensure Probabilistic Completeness.

![](Tahir2018Potentially_figs/beba54b0a35bb6c36b7758770cd50f99d154e6b0eaed2bc87c32fd8711233ff4.jpg)  
(a) i=155375,t=38s,J=183

![](Tahir2018Potentially_figs/8aa47ad9ef35bad38d3128cb999854d341772920d3622edfe06353fb708f43b4.jpg)  
(b) i=124782,t=30s,J=183

![](Tahir2018Potentially_figs/22b87ac065ec2481659f68309917181c0c545794b4e37b254e52877c0050a164.jpg)  
(c) i=2830541,t=705s,J=18

![](Tahir2018Potentially_figs/327ecdffc71db080453fd8abb7c6990078025bbd333e494d5af3f550663972d9.jpg)  
(d) Optimal path solution:J∗=183  
Figure 2: PIB-RRT\*, $\mathrm { P B - R R T ^ { * } }$ & RRT\* performance comparison in 2-D Box

## 5.2. Asymptotic Optimality

Let $\tau ^ { * } \in Z _ { \mathrm { f r e e } }$ denotes the optimal path such that for a sequence of feasible paths $\{ \tau _ { \mathrm { n } } \}$ where $\{ \tau _ { \mathrm { n } } \} \in Z _ { \mathrm { f r e e } } \forall n \in \mathbb { N }$ such that lim $\tau _ { \mathrm { n } } = \tau ^ { * }$ and $\operatorname * { l i m } _ { n \to \infty } J ( \tau _ { \mathrm { { n } } } ) = J ( \tau ^ { * } ) = J ^ { * }$ , where $J ^ { * }$ is the n→8 optimal path cost. An Algorithm is asymptotically optimal if it computes a minimum cost feasible path $\tau ^ { * } : [ 0 , 1 ] \to \tau ^ { * } ( 0 ) = z _ { \mathrm { i n i t } } , \tau ^ { * } ( 1 ) = Z _ { \mathrm { g o a l } } $ and the optimal cost $J ^ { * }$ of the optimal path $\tau ^ { * }$ is the minimum achievable cost of any feasible path in the particular path planning problem $\{ Z _ { \mathrm { f r e e } } , z _ { \mathrm { i n i t } } , Z _ { \mathrm { g o a l } } \}$ . Let $Y _ { \mathrm { n } } ^ { \mathrm { A L G } }$ be the extended random variable which corresponds to the minimumcost solution returned in graph $G _ { \mathrm { n } } ^ { \mathrm { A L G } }$ by the Algorithm ALG at iteration n. Asymptotic optimality

![](Tahir2018Potentially_figs/ea10e3388f240090cdcb22570f23e35aa86094765ae9978f267e8dbea614be5c.jpg)  
Figure 3: PIB-RRT\*, PB-RRT\* & RRT\* performance comparison in 2-D Cluttered

has been formally defined below.

Asymptotic Optimality: An Algorithm ALG is asymptotically optimal if for a cost function $J : \Sigma  \mathbb { R } \geq 0$ it admits a robustly feasible solution with cost $J ^ { * }$

$$
P (\{\limsup _ {n \to \infty} Y _ {\mathrm{n}} ^ {\mathrm{ALG}} = J ^ {*} \}) = 1
$$

Theorem 3 Let the conditions mentioned above in the definition of asymptotic optimality hold, then the proposed algorithms PB-RRT\* and PIB-RRT\* are asymptotically optimal if $d \geq 2$ and $\begin{array} { r } { \gamma > \gamma ^ { * } : = 2 ^ { \mathrm { d } } ( 1 + \frac { 1 } { d } ) \mu ( Z _ { \mathrm { f r e e } } ) } \end{array}$

Sketch of proof: In reference to theorem 38 (Karaman and Frazzoli 2011) [27], PB-RRT\* and PIB-RRT\* our proposed potentially guiding bi-directional variants of RRT\*, after potentially guiding the randomly sampled state z<sub>rand</sub> Z<sub>free</sub>, attempt to add nearby vertices in a radius of $\begin{array} { r } { r _ { \mathrm { n } } ^ { \mathrm { P B - R R T * } } = \gamma ^ { \mathrm { P B - R R T * } } \dot { ( } \frac { l o g n } { n } ) ^ { \frac { 1 } { \mathrm { d } } } } \end{array}$ and $\begin{array} { r } { r _ { \mathrm { n } } ^ { \mathrm { P I B - R R T * } } = \gamma ^ { \mathrm { P I B - R R T * } } ( \frac { l o g n } { n } ) ^ { \frac { 1 } { 4 } } } \end{array}$ <sup>1</sup>d respectively to form an edge so that the bi-directional trees are grown outwards in PB-RRT\* and PIB-RRT\*. As the same procedures happen is RRT\*, therefore from Lemma 56, 71 and 72 (Karaman and Frazzoli 2011) [27] it can be derived that PB-RRT\* and PIB-RRT\* are asymptotically optimal as shown by the following derived relations.

$$
\begin{array}{l} P (\{\operatorname * {l i m s u p} _ {n \to \infty} Y _ {\mathrm{n}} ^ {\mathrm{PB-RRT*}} = J ^ {*} \}) = 1 \\ P (\{\operatorname * {l i m s u p} _ {n \to \infty} Y _ {\mathrm{n}} ^ {\mathrm{PIB-RRT*}} = J ^ {*} \}) = 1 \end{array}
$$

## 5.3. Swift Convergence to Optimal Path

Proof of swift convergence to optimal path of PB-RRT\* and PIB-RRT\* is given in this section based on the following assumptions.

Assumption 1: Let $\Sigma _ { \mathrm { f r e e } }$ denote set of all collision free paths. Given two paths τ and $\tau _ { 2 } ,$ let $\tau _ { 1 } \ | \ \tau _ { 2 }$ denote their concatenation and J(.) be the cost function such that for all $\tau _ { 1 } , \tau _ { 2 } \in \Sigma _ { \mathrm { f r e e } } .$ $J ( \tau _ { 1 } ) \leq J ( \tau _ { 1 } \mid \tau _ { 2 } )$

Assumption 2: For $z \in Z _ { \mathrm { f r e e } }$ , there exists a ball of volume $B _ { z ^ { \prime } , \delta } \subset Z _ { \mathrm { f r e e } }$ of radius $\delta \subset \mathbb { R } > 0$ centered around $z ^ { \prime } \in Z _ { \mathrm { f r e e } }$ such that $z ^ { \prime } \in \mathcal { B } _ { z ^ { \prime } , \delta }$

Assumption 1 defines that if two paths are concatenated, then the combined cost will be no less than the individual cost of the paths. Assumption 2 tells us about the existence of collision free space around an obstacle and the path τ known as δ-spacing which can be used to converge the path τ to optimal solution $\tau ^ { * }$ . Having Assumption 2 under consideration let us define two terms, δ-interior state $i n t _ { \delta } ( Z _ { \mathrm { f r e e } } )$ and δ-exterior state $e x t _ { \delta } ( Z _ { \mathrm { f r e e } } )$ If a ball region of volume $B _ { z , \delta }$ of radius δ centered at z lies entirely inside the collision-free space $Z _ { \mathrm { f r e e : } }$ , then z is said to be in the δ-interior state of $Z _ { \mathrm { f r e e } }$ . The δ-interior of $Z _ { \mathrm { f r e e } }$ is defined as $i n t _ { \delta } ( Z _ { \mathrm { f r e e } } ) : = \{ z \in Z _ { \mathrm { f r e e } } \mid \mathcal { B } _ { z , \delta } \subseteq Z _ { \mathrm { f r e e } } \}$ . While δ-exterior states are those states that are close to the obstacles but not entirely inside, such that for a state $z ^ { \prime } \in Z _ { \mathrm { f r e e } }$ a ball region of volume $B _ { z ^ { \prime } , \delta }$ of radius δ centered at $z ^ { \prime }$ lies partially inside the collision-free space $Z _ { \mathrm { f r e e } }$ and some of the states in its volume lie in obstacle space $Z _ { \mathrm { o b s } } .$ , then $z ^ { \prime }$ is said to lie in the δ-exterior state. The δ-exterior state is represented as $e x t _ { \delta } ( Z _ { \mathrm { f r e e } } ) : = Z _ { \mathrm { f r e e } } / i n t _ { \delta } ( Z _ { \mathrm { f r e e } } )$ Paths with a strong and a weak δ-clearance will be explained below.

![](Tahir2018Potentially_figs/6c08f83d9342ad2b7ac221850c73ba8eba547379394b54770de08408f7b4dd57.jpg)  
(a) i=18762,t=12s,J=220

![](Tahir2018Potentially_figs/485fb04e3cfd894b8cead79f5d4e930a21793c3c4fc18755ff17c23789800c7e.jpg)  
(b) i=21474,t=14s,J=220

![](Tahir2018Potentially_figs/53e01234492428574a289d13a123272dae97d8bb8cf43ece2e489a3a6cabedf0.jpg)  
(c) i=544852,t=106s,J=265

![](Tahir2018Potentially_figs/83bbc8c86b0bcb5e491cb91cf5c91b50d3399a372ae947af9e8b94ee0769e82f.jpg)  
(d) Optimal path solution:J∗=220

Figure 4: PIB-RRT\*, PB-RRT\* & RRT\* performance comparison in 3-D Maze

Path with strong δ-clearance: If a feasible path $\tau \in \Sigma _ { \mathrm { f r e e } }$ comprises entirely of δ-interior states of $Z _ { \mathrm { f r e e } }$ , then that path is said to have a strong δ-clearance for $\delta > 0$

Path with weak δ-clearance: Let $\tau _ { 1 } : [ 0 , 1 ]$ and $\tau _ { 2 } : [ 0 , 1 ]$ be two collision free paths. Both paths have same initial and goal states $\tau _ { 1 } ( 0 ) = \tau _ { 2 } ( 0 ) , \tau _ { 1 } ( 1 ) = \tau _ { 2 } ( 1 )$ respectively. The path $\tau _ { 1 }$ is homotopic to the path $\tau _ { 2 }$ by the homotopy function $\psi : [ 0 , 1 ]$ such that $\psi ( q )$ is a collision free path where $q  [ 0 , 1 ]$ and $\psi ( 0 ) = \tau _ { 1 }$ has weak δ-clearance and $\psi ( 1 ) = \tau _ { 2 }$ has strong δ-clearance and for all $\beta \in [ 0 , 1 ]$ , their is $\delta _ { \beta } > 0$ such that $\psi ( \beta )$ has δ -clearance.

The following lemma states that the proposed $B P G ( )$ heuristic potentially guides the random samples $z \in Z _ { \mathrm { f r e e } }$ towards weak δ-clearance region where optimal solution exists.

Lemma 1 The $B P G ( )$ heuristic directs the random sample $z \in Z _ { \mathrm { f r e e } }$ towards δ-exterior $e x t _ { \delta } ( Z _ { \mathrm { f r e e } } )$ region, where δ-clearance is weak.

Sketch of proof: The BP G() heuristic causes the random sample $z \in Z _ { \mathrm { f r e e } }$ to be potentially pulled by the attractive pole which is either the goal region $Z _ { \mathrm { g o a l } }$ or the initial root state region $z _ { \mathrm { i n i t } }$ which are swapped on each alternate iteration. As the random sample is being potentially guided down the slope towards the attracting pole in small  steps for n time or till a very minute distance $d _ { \mathrm { o b s } } ^ { \ast }$ from any obstacle is reached as seen in Algorithm 8. The minute distance $d _ { \mathrm { o b s } } ^ { \ast }$ causes the random sample to achieve weak δ-clearance as it is being potentially guided there.

Let $\tau _ { \mathrm { n } } ^ { \prime }$ and $\tau _ { \mathrm { n } }$ be two paths such that $\tau _ { \mathrm { n } } ^ { \prime } \in \Sigma _ { \mathrm { f r e e } }$ and $\tau _ { \mathrm { n } } \in \Sigma _ { \mathrm { f r e e } }$ and $\tau _ { \mathrm { n } } ^ { \prime }$ is closest to $\tau _ { \mathrm { n } }$ in terms of bounded variation norm among all paths in $\Sigma _ { \mathrm { f r e e } }$ . The following lemma states that convergence to optimal solution is surely guaranteed if, the random variable $\| { \boldsymbol { \tau } } _ { \mathrm { n } } ^ { \prime } - { \boldsymbol { \tau } } _ { \mathrm { n } } \| _ { \mathrm { B V } }$ converges to zero

Lemma $\mathbf { 2 } ( [ 4 ] )$ A sampling based Algorithm converges to optimal solution if, the random variable $\left\| { \tau _ { \mathrm { n } } ^ { \prime } - \tau _ { \mathrm { n } } } \right\| .$ converges to zero i.e,

$$
P (\{\lim _ {n \to \infty} \| \tau_ {\mathrm{n}} ^ {\prime} - \tau_ {\mathrm{n}} \| _ {\mathrm{BV}} = 0 \}) = 1
$$

Corollary 2 As the number of iterations approach infinity $\tau _ { \mathrm { n } } ^ { \prime }$ will eventually converge to the optimal path $\tau ^ { * }$

$$
P (\{\lim _ {n \to \infty} \tau_ {\mathrm{n}} ^ {\prime} = \tau^ {*} \}) = 1
$$

Let $I _ { \mathrm { z } }$ denote the intensity of near vertices $Z _ { \mathrm { n e a r } }$ around a random state $z \in Z _ { \mathrm { f r e e } }$ in a ball of radius r such that

$$
I _ {\mathrm{z}} := \left\{\operatorname{card} \left(Z _ {\text {near}} / \mu \left(\mathcal {B} _ {z, r}\right): Z _ {\text {near}} \mid z = \mathcal {B} _ {z, r} \cap V _ {\mathrm{n}} \right. \right\}
$$

Sketch of proof: Let $\varepsilon \in \mathbb { R } . \ Z _ { \mathrm { n e a r } }$ is the set of near vertices around a randomly sampled state $z _ { \mathrm { r a n d } } \in$ $Z _ { \mathrm { f r e e } }$ located inside a ball of volume $B _ { z , r }$ of radius r centered at z such that $r = \gamma ( \log n / n ) ^ { 1 / d } ;$ where γ is a constant, n is the number of vertices and d is the dimension of the state space. The randomly sampled state $z _ { \mathrm { r a n d } }$ can make any state $z ^ { \prime } \in Z _ { \mathrm { n e a r } }$ as its parent which has the lowest cost of connecting $z _ { \mathrm { r a n d } }$ to the root $z _ { \mathrm { i n i t } }$ of the tree out of all the vertices in $Z _ { \mathrm { n e a r } }$ . This means that $\| z _ { \mathrm { r a n d } } - z ^ { \prime } \| = \varepsilon .$ , where $\varepsilon < r = \gamma ( \log n / n ) ^ { 1 / d }$ . This ensures that the tree in the algorithm grows in small incremental steps of $d ^ { \prime }$ where $d ^ { \prime } \leq \varepsilon .$ For incremental expansion or wavefront expansion of trees it is proven that regions near the root of trees are more dense [22]. Hence if the randomly sampled state $z _ { \mathrm { r a n d } }$ lies closer to the generation of the tree, there is a high probability of having high cardinality of set $Z _ { \mathrm { n e a r } }$

The proposed algorithms PB-RRT\* and PIB-RRT\* are designed to converge to optimal solution very quickly. Since the intensity of near vertices $I _ { \mathrm { z } }$ is higher in region closer to the generation of the tree [22], following Lemma 2 states that Bi-directional Potential Gradient $B P G ( )$ heuristic directs the random samples towards higher intensity $I _ { \mathrm { z } }$ regions where higher probability of optimal solution exists.

Lemma 3 The proposed BP G() heuristic guides the random sample $z \in Z _ { \mathrm { f r e e } }$ towards the regions closer to point of generation of the trees where the intensity of near vertices $I _ { \mathrm { z } }$ is much higher.

Sketch of proof: The $B P G ( )$ heuristic of the proposed PB-RRT\* and PIB-RRT\* guides the random sample $z \in Z _ { \mathrm { f r e e } }$ towards the goal region $Z _ { \mathrm { g o a l } }$ and initial root state $z _ { \mathrm { i n i t } }$ as the poles of attraction change on every iteration in $B P G ( )$ , directing the random sample down the slope under the influence of the attractive pole, either it be $z _ { \mathrm { i n i t } }$ or $Z _ { \mathrm { g o a l } }$ region pole. These are the points of generation of the bidirectional trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ , generated at $z _ { \mathrm { i n i t } }$ and $Z _ { \mathrm { g o a l } }$ respectively. Hence this means that the intensity of near vertices $I _ { \mathrm { z } }$ is much higher at the root of the trees and the random sample $z \in Z _ { \mathrm { f r e e } }$ is directed towards higher $I _ { \mathrm { z } }$ region causing increased rewiring per iteration of both proposed algorithms represented as $\vartheta _ { \mathrm { P B - R R T * } }$ and $\vartheta _ { \mathrm { P I B - R R T } }$ respectively. Such potential fields in bidirectional tree search do not exist in $\mathrm { R R T ^ { * } }$ hence, $\begin{array} { r } { \vartheta _ { \mathrm { P B - R R T * } } > \vartheta _ { \mathrm { R R T } } , } \end{array}$ and $\vartheta _ { \mathrm { P I B - R R T * } } ~ > ~ \vartheta _ { \mathrm { R R T * } }$ Since rewiring tries to minimize the bounded variation $\| { \boldsymbol { \tau } } _ { \mathrm { n } } ^ { \prime } - { \boldsymbol { \tau } } _ { \mathrm { n } } \| _ { \mathrm { B V } }$ as mentioned before, causes convergence to optimal path faster than RRT\*.

Based on Lemma 2 and Lemma 3, Theorem 4 is formalized as follows stating that the convergence to the optimal solution of the proposed $\mathrm { P B - R R T ^ { * } }$ and PIB-RRT\* is faster than RRT\* due to increased rewiring per iterations in the proposed algorithms than $\mathrm { R R T ^ { * } }$ as explained above.

Theorem 4 From Lemma 2 and Lemma 3 it is derived that $B P G ( )$ heuristic in $P B  – R R T ^ { * }$ and $P I B – R R T ^ { * }$ guides the random sample $z \in Z _ { \mathrm { f r e e } }$ towards higher intensity $I _ { \mathrm { z } }$ regions such that $\begin{array} { r } { \vartheta _ { \mathrm { P B - R R T * } } > \vartheta _ { \mathrm { R R T } } , } \end{array}$ and $\vartheta _ { \mathrm { P I B - R R T * } } > \vartheta _ { \mathrm { R R T * } }$

(d) Optimal path solution:J∗=70  
![](Tahir2018Potentially_figs/1b683b93825def4e7490b7786754f4e5f2da5a3727e54d03dbee25cda75a4543.jpg)  
(a) i=26902,t=11.1s,J=70

![](Tahir2018Potentially_figs/f8e5eb40d8c6df3310f0515cf90b9d7c7fb336f9b61ec21497d94a96b28aad5d.jpg)

![](Tahir2018Potentially_figs/d4d54ad3cbe00dd5a1d507bf94338311fcdbbaf0115e3406eafbc86a48d92213.jpg)  
(c) i=1355329,t=150s,J=70

![](Tahir2018Potentially_figs/d42a476c17b35ead14f63556d2766a799a99d24c0ea7362b2e65995efc170293.jpg)  
Figure 5: PIB-RRT\*, $\mathrm { P B - R R T ^ { * } }$ & $\mathrm { R R T ^ { * } }$ performance comparison in 3-D Columns

On the basis of Theorem 4, Lemma 4 has been derived and is stated as follows.

Lemma 4 In the given path planning problem $\{ Z _ { \mathrm { f r e e } } , z _ { \mathrm { i n i t } } , Z _ { \mathrm { g o a l } } \}$ , the proposed $B P G ( )$ heuristic guides the random sample $z \in Z _ { \mathrm { f r e e } }$ in such a manner that the two tree in the bi-directional search are potentially pulled towards each other.

Sketch of proof: The $B P G ( )$ heuristic contains $B P F g o a l ( )$ and $B P F i n i t ( )$ heuristics. $B P F g o a l ( )$ heuristic causes the goal region $Z _ { \mathrm { g o a l } }$ to become the attractive pole while BP F init() heuristic causes the initial root state region $z _ { \mathrm { i n i t } }$ to become the attractive pole. As there are two trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ initial root state and goal region respectively in the proposed PB-RRT\* and PIB-RRT\*. $B P F g o a l ( )$ and $B P F i n i t ( )$ potentially pull the random sample towards the attracting pole which is either the goal region where the origin of tree $T _ { \mathrm { b } }$ is located or towards $z _ { \mathrm { i n i t } }$ which is the origin of tree $T _ { \mathrm { a } }$ and on the next iteration the pole is swapped. This causes the random sample $z \in Z _ { \mathrm { f r e e } }$ to be potentially pulled towards origins of both trees, $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ on alternate iterations causing both trees to grow and be potentially pulled towards each other due to the BP G() heuristic resulting faster convergence to optimal solution. Based on Corollary 2 and Lemmas 1,2,3 and 4, Theorem 5 formally states the faster convergence of $\mathrm { P B - R R T ^ { * } }$ and $\mathrm { P I B - R R T ^ { * } }$ due to the $B P G ( )$ heuristic.

![](Tahir2018Potentially_figs/fb238ac2a093ec4e66333cf8fa015011bafe004e6164fc4e97d421172e120312.jpg)  
(a) i=134682,t=29s,J=79

![](Tahir2018Potentially_figs/2071e7a26a06d33d59000bc81b96c333794a118372955d4dbbea5ff21f09b4d5.jpg)  
(b) i=160652,t=43s,J=79

![](Tahir2018Potentially_figs/bff215dbb803edca09cb1e0141a2bff69bdd93f8fc5c5abbffc5fe8253cc80f9.jpg)  
(c) i=1949183,t=545s,J=79

(d) Optimal path solution:J∗=79  
![](Tahir2018Potentially_figs/8792ffefd90e4ebd8c5f8c59440858a399ea5781fb509c075a66f8f3fac4e068.jpg)  
Figure 6: PIB-RRT\*, $\mathrm { P B - R R T ^ { * } }$ & $\mathrm { R R T ^ { * } }$ Initial performance comparison in 3-D Cluttered

Theorem 5 The BP G() (Bi-directional Potential Gradient) heuristic (1) potentially directs the random sample $z \in Z _ { \mathrm { f r e e } }$ towards higher intensity $I _ { \mathrm { z } }$ regions where rewirings per iteration are related as, $\begin{array} { r } { \vartheta _ { \mathrm { P B - R R T * } } > \vartheta _ { \mathrm { R R T } } , } \end{array}$ and ϑ<sub>PIB RRT</sub> > ϑ<sub>RRT</sub> ; (2) the random sample after being potentially guided becomes $z _ { \mathrm { p b } }$ so that $P ( z _ { \mathrm { p b } } \in Z _ { \mathrm { e x t } _ { \delta } } ) > 0 ;$ (3) The resulting solution path τ very quickly converges to optimal path $\tau ^ { * }$ so that $\| { \tau } _ { \mathrm { n } } ^ { \prime } - { \tau } _ { \mathrm { n } } \| = 0$ where $\tau _ { \mathrm { n } } ^ { \prime } = \tau ^ { * }$

Hence from Theorem 1,2,3,4 and 5 it has been deduced that the proposed PB-RRT\* and PIB-RRT\* algorithms find the feasible solution to a motion planning problem and converge to optimal solution very quickly.

## 5.4. Computational Complexity

The computational complexity of PB-RRT\* and PIB-RRT\* has been discussed in this section. Let $M _ { \mathrm { n } } ^ { \mathrm { A L G } }$ define the total computations performed by Algorithm $A L G . ~ M _ { \mathrm { n } } ^ { \mathrm { P B - R R T * } }$ and $M _ { \mathrm { n } } ^ { \mathrm { P I B - R R T * } }$ are the total processes performed by PB-RRT\* and PIB-RRT\* respectively. Theorem 6 proposes that the computational complexity of PB-RRT\* and PIB-RRT\* are a constant times higher than that of RRT\* where as Theorems $7$ and Theorem 8 state the comparison of PB-RRT\* with B-RRT\* and PIB-RRT\* with IB-RRT\* respectively.

Theorem 6 There exists constants $\Phi _ { 1 } , \Phi _ { 2 } \in \mathbb { R } _ { + }$ such that the computational complexity ratio of $P B  – R R T ^ { * }$ and $P I B – R R T ^ { * }$ with $R R T ^ { * }$ is as follows.

$$
\begin{array}{r} \underset {n \to \infty} {\limsup} \mathbb {E} \left[ \frac {M _ {\mathrm{n}} ^ {\mathrm{PB-RRT*}}}{M _ {\mathrm{n}} ^ {\mathrm{RRT*}}} \right] \leq \Phi_ {1} \\ \underset {n \to \infty} {\limsup} \mathbb {E} \left[ \frac {M _ {\mathrm{n}} ^ {\mathrm{PIB-RRT*}}}{M _ {\mathrm{n}} ^ {\mathrm{RRT*}}} \right] \leq \Phi_ {2} \end{array}
$$

Theorem 7 The computational complexity ratio of $P B  – R R T ^ { * }$ and $B { - } R R T ^ { * }$ is such that there exists a constant $\Phi _ { 3 } \in \mathbb { R } .$ +

$$
\limsup _ {n \to \infty} \mathbb {E} \left[ \frac {M _ {\mathrm{n}} ^ {\mathrm{PB-RRT*}}}{M _ {\mathrm{n}} ^ {\mathrm{B-RRT*}}} \right] \leq \Phi_ {3}
$$

Theorem 8 Let $\Phi _ { 4 } \in \mathbb { R } _ { + }$ be a constant so that the computational complexity ratio of $P I B – R R T ^ { * }$ and $I B { - } R R T ^ { * }$ is as follows.

$$
\operatorname * {l i m s u p} _ {n \to \infty} \mathbb {E} \left[ \frac {M _ {\mathrm{n}} ^ {\mathrm{PIB-RRT*}}}{M _ {\mathrm{n}} ^ {\mathrm{IB-RRT*}}} \right] \leq \Phi_ {4}.
$$

Sketch of proof: When compared to $\mathrm { R R T ^ { * } }$ along with being bi-directional another procedure BP G() has been incorporated in the proposed $\mathrm { P B - R R T ^ { * } }$ and PIB-RRT\*. PB-RRT\* has an additional Connect() heuristic along with BP G() heuristic. PIB-RRT\* has GetBestT reeP arent() in place of P ickBestP arent() in RRT\* and $B P G ( )$ heuristic. $B P G ( )$ heuristic can be executed in a constant number of iterations and does not depend upon the number of vertices in the tree. It has to find nearest obstacle form the random sample $z \in Z _ { \mathrm { f r e e } }$ which requires at least $\Omega ( \log _ { 1 0 } n )$ time. Furthermore in PB-RRT\* and PIB-RRT\* both execute NearestV ertex() and NeighbouringV ertices() procedure for both trees $T _ { \mathrm { a } }$ and $T _ { \mathrm { b } }$ just like RRT\* which adds up a constant computation overhead when compared to RRT\* in $\log _ { 1 0 }$ n terms. Hence as seen in Theorem 6, PB-RRT\* and PIB-RRT\* only vary from RRT\* by $\Phi _ { 1 }$ and $\Phi _ { 2 }$ in terms of computational complexity ratio.

In Theorem 7 the computational complexity ratio of PB-RRT\* and B-RRT\* is given and as BP G() heuristic is the only additional procedure in PB-RRT\* as compared to B-RRT\*, hence their computational complexity only difers by a constant ratio $\Phi _ { 3 } \in \mathbb { R } _ { + }$ . Similarly in Theorem 8 PIB-RRT\* difers from IB-RRT\* by a constant $\Phi _ { 4 } \in \mathbb { R } _ { + }$ in computational complexity ratio.

<table><tr><td>Environment</td><td>Algorithm</td><td> $i_{\text{min}}$ </td><td> $i_{\text{max}}$ </td><td> $i_{\text{avg}}$ </td><td> $t_{\text{min}}(s)$ </td><td> $t_{\text{max}}(s)$ </td><td> $t_{\text{avg}}(s)$ </td><td> $\vartheta_{\text{avg}}$ </td><td> $J(\tau*)$ </td><td>Fail</td></tr><tr><td rowspan="5">2D-Maze (Fig 1)</td><td>PIB-RRT*</td><td>180,484</td><td>224,306</td><td>198,608</td><td>44</td><td>57</td><td>48</td><td>1.09</td><td>241</td><td></td></tr><tr><td>PB-RRT*</td><td>191,273</td><td>234,547</td><td>215,505</td><td>47</td><td>58.7</td><td>53</td><td>1.02</td><td>241</td><td></td></tr><tr><td>IB-RRT*</td><td>256,374</td><td>335,877</td><td>290,126</td><td>62</td><td>70</td><td>66</td><td>0.74</td><td>241</td><td></td></tr><tr><td>P-RRT*</td><td>300,001</td><td>375,661</td><td>332,127</td><td>67</td><td>74</td><td>72</td><td>0.66</td><td>241</td><td></td></tr><tr><td>RRT*</td><td>3,234,592</td><td>3,799,518</td><td>3,371,861</td><td>922</td><td>1140</td><td>1045</td><td>0.35</td><td>241</td><td>70%</td></tr><tr><td rowspan="5">2D-Box (Fig 2)</td><td>PIB-RRT*</td><td>122,355</td><td>189,826</td><td>157,941</td><td>34</td><td>43</td><td>38</td><td>0.84</td><td>183</td><td></td></tr><tr><td>PB-RRT*</td><td>100,001</td><td>158,870</td><td>125,186</td><td>25</td><td>39</td><td>30.4</td><td>0.93</td><td>183</td><td></td></tr><tr><td>IB-RRT*</td><td>214,341</td><td>271,247</td><td>232,315</td><td>54</td><td>61</td><td>59</td><td>0.70</td><td>183</td><td></td></tr><tr><td>P-RRT*</td><td>247,984</td><td>330,541</td><td>294,187</td><td>61</td><td>71</td><td>66</td><td>0.65</td><td>183</td><td></td></tr><tr><td>RRT*</td><td>2,247,984</td><td>2,830,541</td><td>2,424,187</td><td>611</td><td>705</td><td>687</td><td>0.31</td><td>183</td><td>50%</td></tr><tr><td rowspan="5">2D-Cluttered (Fig 3)</td><td>PIB-RRT*</td><td>13,452</td><td>26,731</td><td>20,539</td><td>6.3</td><td>9.9</td><td>8.1</td><td>1.25</td><td>125</td><td></td></tr><tr><td>PB-RRT*</td><td>17,537</td><td>31,345</td><td>22,124</td><td>7.2</td><td>10.1</td><td>8.7</td><td>1.18</td><td>125</td><td></td></tr><tr><td>IB-RRT*</td><td>35,164</td><td>39,402</td><td>38,152</td><td>12</td><td>14</td><td>13.5</td><td>0.97</td><td>125</td><td></td></tr><tr><td>P-RRT*</td><td>66,373</td><td>71,324</td><td>68,332</td><td>24</td><td>28</td><td>26.5</td><td>0.63</td><td>125</td><td></td></tr><tr><td>RRT*</td><td>1,458,373</td><td>1,926,184</td><td>1,670,140</td><td>320</td><td>531</td><td>420</td><td>0.39</td><td>125</td><td>50%</td></tr><tr><td rowspan="5">3D-Maze (Fig 4)</td><td>PIB-RRT*</td><td>14,011</td><td>19,719</td><td>17,430</td><td>10.5</td><td>13</td><td>11.5</td><td>0.98</td><td>220</td><td></td></tr><tr><td>PB-RRT*</td><td>18,602</td><td>24,361</td><td>21,459</td><td>11.7</td><td>15</td><td>14.1</td><td>0.88</td><td>220</td><td></td></tr><tr><td>IB-RRT*</td><td>33,400</td><td>42,100</td><td>38,213</td><td>18.2</td><td>22</td><td>19.5</td><td>0.77</td><td>220</td><td></td></tr><tr><td>P-RRT*</td><td>74,300</td><td>79,613</td><td>77,641</td><td>28</td><td>31.5</td><td>29.6</td><td>0.62</td><td>220</td><td></td></tr><tr><td>RRT*</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>100%</td></tr><tr><td rowspan="5">3D-Columns (Fig 5)</td><td>PIB-RRT*</td><td>23,484</td><td>26,902</td><td>24,629</td><td>9.3</td><td>11.1</td><td>10.4</td><td>0.99</td><td>70</td><td></td></tr><tr><td>PB-RRT*</td><td>17,624</td><td>21,337</td><td>19,647</td><td>6.2</td><td>8.1</td><td>7.5</td><td>1.05</td><td>70</td><td></td></tr><tr><td>IB-RRT*</td><td>35,444</td><td>43,404</td><td>39,583</td><td>14</td><td>21</td><td>18</td><td>0.71</td><td>70</td><td></td></tr><tr><td>P-RRT*</td><td>81,561</td><td>84,321</td><td>83,523</td><td>32.5</td><td>34</td><td>33</td><td>0.58</td><td>70</td><td></td></tr><tr><td>RRT*</td><td>678,001</td><td>1,246,149</td><td>900,132</td><td>124</td><td>271</td><td>174</td><td>0.43</td><td>70</td><td>70%</td></tr><tr><td rowspan="5">3D-Cluttered (Fig 6)</td><td>PIB-RRT*</td><td>110,629</td><td>151,784</td><td>131,542</td><td>26.3</td><td>32</td><td>28.5</td><td>1.31</td><td>79</td><td></td></tr><tr><td>PB-RRT*</td><td>130,242</td><td>177,804</td><td>153,358</td><td>31</td><td>47</td><td>41</td><td>1.12</td><td>79</td><td></td></tr><tr><td>IB-RRT*</td><td>200,963</td><td>244,618</td><td>223,493</td><td>59</td><td>64</td><td>61</td><td>1.02</td><td>79</td><td></td></tr><tr><td>P-RRT*</td><td>352,693</td><td>385,284</td><td>369,381</td><td>72</td><td>75</td><td>74</td><td>0.91</td><td>79</td><td></td></tr><tr><td>RRT*</td><td>1,857,381</td><td>1,949,183</td><td>1,908,392</td><td>514</td><td>545</td><td>529</td><td>0.63</td><td>79</td><td>60%</td></tr></table>

## 6. Experimental Results

In this section the numerical path planning experiments are provided that make a comparison of the proposed PB-RRT\* and PIB-RRT\* algorithms with other aysmptotically optimal sampling based algorithms such as IB-RRT\*,P-RRT\* and RRT\* on a variety of environments. Diferent state dimensions were used in diferent environments to thoroughly test the algorithms. The size and configuration space of the diferent environments was varied from very large to very small but was kept constant for a particular environment so that a just comparison could be made between diferent algorithms while simulating on that environment. Due to randomization the algorithms were run up to 50 times with a common pseudo-random seed which was varied on every re-run of the Algorithm. The simulations were performed on a 2.30GHz Intel core i3 processor with 2GB RAM.

If the total number of iterations exceeded $5 \times 1 0 ^ { 6 }$ , the simulation was terminated and the result was declared as failed to restrict the computational time. The results of the above mentioned algorithms in diferent environments are provided in Table 1. Maximum, minimum and average iterations and time are provided in Table 1. Fail columns denote the percentage of the total 50 reruns the Algorithm has failed to find the optimal solution. The column $\vartheta _ { \mathrm { a v g } }$ rewiring per iteration denotes the average number of rewiring occurring from start to termination of the simulation. $J ^ { * }$ indicates the optimal path cost in terms of Euclidean metric of the particular environment within a specified tolerance of the true optimum. $\mathrm { P B - R R T ^ { * } }$ and $\mathrm { P I B - R R T ^ { * } }$ along with the above mentioned algorithms were tested in a variety of environments (e.g, Figs 1-6), though only the figures of simulations of PB-RRT\*, PIB-RRT\* and $\mathrm { R R T ^ { * } }$ are displayed due to limited space available. Each environment tested a diferent aspect of the Algorithm. Results of the testing and simulations are discussed below.

![](Tahir2018Potentially_figs/18af36682d4d29e38f17d0f442fd27c7449ba4827a5cc2469be2808236f1b450.jpg)  
(a) Iterations for initial solution.

![](Tahir2018Potentially_figs/9fa9fd2501fc740283055b84b6b67edd813576a7587ead164ff8f326abf40d66.jpg)  
(b) Time consumed for initial solution.

![](Tahir2018Potentially_figs/9adf886db1631bcc7b374b6346d990d2aed62df412907e82a5961ae43165c5f2.jpg)  
(c) Iterations for optimal solution.

![](Tahir2018Potentially_figs/5e62c0d701fee478246ba8057df07567bb463325b93ac8ed015ee0ecf78d7a49.jpg)  
(d) Time consumed for optimal solution.  
Figure 7: Performance Comparison in 10 complex cluttered environments

Fig 1 is a 2-D highly cluttered environment used to test the eficiency of the above mentioned algorithms in an environment ladened with obstacles, where it is very hard to find the optimal solution. As seen from Table 1, PIB-RRT\* is able to find the optimal solution in this highly cluttered environment the most quickly $( i _ { \mathrm { a v g } } = 1 9 8 , 6 0 8 )$ with highest rewiring per iteration average $( \vartheta _ { \mathrm { P I B - R R T * } } = 1 . 0 9 )$ . After PIB-RRT\*, PB-RRT\*, $\mathrm { I B { - } R R T ^ { * } }$ and P-RRT\* find the optimal solution the quickest respectively while RRT failed to find the optimal solution 70% of the times within the specified range. PIB-RRT\* is quickest to find the optimal solution due to the Intelligent Sample Insertion it inherited from IB-RRT\* which was specifically designed for highly cluttered environments and coupling Intelligent Sample Insertion with the proposed $B P G ( )$ heuristic for PIB-RRT\* gave us the optimal solution in the least amount of time. After PIB-RRT\*, PB-RRT\* was the quickest in finding the optimal solution of Fig 1 due to the BP G() heuristic coupled with Bi-directional $\mathrm { R R T ^ { * } }$ (B-RRT\*). Fig 2 is another 2-D environment, as seen it is not as highly cluttered as Fig 1 and PB-RRT\* is the quickest to find the optimal solution in this environment due to the BP G() heuristic pulling both Bi-directional trees towards each other, coupled with the partial greedy heuristic of $\mathrm { B { - } R R T ^ { * } }$ it has given the optimal solution in this environment the most quickly taking least number of average iterations to optimal solution at $( i _ { \mathrm { a v g } } = 1 2 5 , 1 8 6 )$ . After PB-RRT\*, PIB-RRT\* was second in least number of iterations to optimal solution at $( i _ { \mathrm { a v g } } = 1 5 7 , 9 4 1 )$ . Then came $\mathrm { I B { - } R R T ^ { * } }$ and $\mathrm { P - R R T ^ { * } }$ respectively at higher average iterations to optimal solution, while $\mathrm { R R T ^ { * } }$ had failed to converge to an optimal solution $5 0 \%$ of the times.

Fig 3 is another 2-D environment which is highly cluttered and $\mathrm { P I B - R R T ^ { * } }$ was the quickest to find the optimal solution with the least number of average iterations to optimal solution $( i _ { \mathrm { a v g } } =$ 20, 539) and it had the highest average rewiring per iteration rate $( \vartheta _ { \mathrm { P I B - R R T * } } = 1 . 2 5 )$ . While $\mathrm { P B - R R T ^ { * } }$ was second with $( i _ { \mathrm { a v g } } = 2 2 , 1 2 4 )$ and $( \vartheta _ { \mathrm { P B - R R T * } } = 1 . 1 8 )$ Then came $\mathrm { I B { - } R R T ^ { * } }$ and P-RRT\* respectively in quickness too find the optimal solution while $\mathrm { R R T ^ { * } }$ failed 50% of the times to find the optimal solution in this environment. Fig 4 shows a 3-D environment which is highly cluttered, having many obstacles between initial and goal regions. PIB- $\mathrm { . R R T ^ { * } }$ due to its $B P G ( )$ heuristic coupled with Intelligent Sample Insertion was able to find the optimal path the quickest $( i _ { \mathrm { a v g } } ~ = ~ 1 7 , 4 3 0 )$ Then came $\mathrm { P B } \mathrm { - R R T ^ { \ast } } ~ ( i _ { \mathrm { a v g } } ~ = ~ 2 1 , 4 5 9 )$ and then $\mathrm { I B } { \mathrm { - R R T ^ { * } } } \ ( i _ { \mathrm { a v g } } \ = \ 3 8 , 2 1 3 )$ and P-RRT\* $( i _ { \mathrm { a v g } } = 7 7 , 6 4 1 )$ while RRT\* failed to find the optimal path. Fig 5 shows a 3-D environment with narrow passages through vertical columns and as seen from Table 1, $\mathrm { P B - R R T ^ { * } }$ was the quickest in finding the optimal solution in this environment $( i _ { \mathrm { a v g } } = 1 9 , 6 4 7 )$ with rewiring per iteration of $( \vartheta _ { \mathrm { P B - R R T * } } = 1 . 0 5 )$ . PIB-RRT\* was the second $( i _ { \mathrm { a v g } } = 2 4 , 6 2 9 )$ while IB-RRT\* $( i _ { \mathrm { a v g } } = 3 9 , 5 8 3 )$ and $\mathrm { P \mathrm { - R R T ^ { \ast } } } \left( i _ { \mathrm { a v g } } = 8 3 , 5 2 3 \right)$ came third and fourth respectively in quickness to optimal solution and RRT\* took an extraordinary number of iterations to converge to the optimal solution $( i _ { \mathrm { a v g } } = 9 0 0 , 1 3 2 )$

Fig 6 is a 3-D environment and has a highly obstacle ridden cluttered environment from initial to goal regions. We found $\mathrm { P I B - R R T ^ { * } }$ to be the fastest to optimal solution in this environment $( i _ { \mathrm { a v g } } =$ 131, 542) with highest rewiring per iteration rate $( \vartheta _ { \mathrm { P I B - R R T * } } = 1 . 3 1 )$ and PB- $\mathrm { . R R T ^ { * } }$ was second in quickness to optimal solution $( i _ { \mathrm { a v g } } = 1 5 3 , 3 5 8 )$ with rewiring per iteration of $( \vartheta _ { \mathrm { P B - R R T * } } = 1 . 1 2 )$ and IB- $\mathrm { R R T ^ { * } } ~ ( i _ { \mathrm { a v g } } = 2 2 3 , 4 9 3 )$ , P-RRT\* $( i _ { \mathrm { a v g } } = 3 6 9 , 3 8 1 )$ and $\mathrm { R R T ^ { * } } \left( i _ { \mathrm { a v g } } = 1 , 9 0 8 , 3 9 2 \right)$ came third, fourth and fifth respectively in quickness to optimal path. In this environment $\mathrm { R R T ^ { * } }$ failed 60% of the times to reach an optimal solution. In Fig 7 diferent bar graphs are presented. These bar graphs have been obtained after experimentation and simulation in 10 diferent 2-D and 3-D environments for comparing $\mathrm { P I B - R R T ^ { * } }$ , PB-RRT\*, IB-RRT\*, $\mathrm { P - R R T ^ { * } }$ and $\mathrm { R R T ^ { * } }$ . In Fig 7(a) the comparison is made in iterations required to find the initial feasible path in all environments for each Algorithm. Fig 7(b) shows the time required to find the initial feasible path for all the environments. Similarly Fig 7(c) and $\mathrm { F i g ~ 7 ( d ) }$ show the comparison of iterations required to find the optimal path and time required to find the optimal solution respectively. It is seen from Fig 7 that $\mathrm { P I B - R R T ^ { * } }$ and $\mathrm { P B - R R T ^ { * } }$ require very less iterations and time to find the initial path and the optimal solution when compared to IB-RRT\*, $\mathrm { P - R R T ^ { * } }$ and $\mathrm { R R T ^ { * } }$ . It is noted that in some cases PIB-RRT\* performs better than $\mathrm { P B - R R T ^ { * } }$ and in some cases $\mathrm { P B - R R T ^ { * } }$ performs better than $\mathrm { P I B - R R T ^ { * } }$ . Mainly in highly cluttered environments $\mathrm { P I B - R R T ^ { * } }$ has shown to perform better than $\mathrm { P B - R R T ^ { * } }$ due to the inclusion of IntelligentSampleInsertion with $B P G ( )$ heuristic while in less cluttered environments PB- $\mathrm { . R R T ^ { * } }$ takes the lead in performance due to its greedy heuristic coupled with $B P G ( )$ heuristic. But this greedy heuristic becomes less eficient in highly cluttered environments.

![](Tahir2018Potentially_figs/d28f117756e6cc04211843e14bd19b5760863804294f9d805333304a1dc44c2e.jpg)  
Figure 8: Cost vs Running Time

![](Tahir2018Potentially_figs/b45dc431d72eca4ce759e7695f2c5468688fd15ced1d93755f8ee9a92e7f59be.jpg)  
Figure 9: Running Time Ratio w.r.t RRT\*

In Fig 8, after several runs in an obstacle filled 3D environment, the cost (in terms of Eu clidean distance) versus the running time graph was plotted for PIB-RRT\*, PB-RRT\* and $\mathrm { R R T ^ { * } }$ algorithms respectively. It can be seen that $\mathrm { P I B - R R T ^ { * } }$ and $\mathrm { P B - R R T ^ { * } }$ converge to optimal cost solution quite quickly as compared to $\mathrm { R R T ^ { * } }$ due to $B P G ( )$ heuristic combined with bidirectional tree search. Fig 9 shows the running time ratio of $\mathrm { P I B - R R T ^ { * } }$ over $\mathrm { R R T ^ { * } }$ and $\mathrm { P B - R R T ^ { * } }$ over $\mathrm { R R T ^ { * } }$ after numerous runs in an obstacle-free 3D environment. As expected from the computational complexity analysis of Section 5.4 and as stated in Theorem 6, Fig 9 shows that the running time ratios of $\mathrm { P I B - R R T ^ { * } }$ and $\mathrm { P B - R R T ^ { * } }$ w.r.t $\mathrm { R R T ^ { * } }$ settle at a constant value as the number of iterations increase.

![](Tahir2018Potentially_figs/2ad24f723319dbd35e14bf7d7129b13405b2db461576418ba7c85b314d320b59.jpg)  
(a) PIB-RRT\*: i=30000, k=1

![](Tahir2018Potentially_figs/d4edacbd124ce4dba2243aec901dd9b35750fd95ca505ffc966e49f559dd3616.jpg)

(b) PIB-RRT\*: i=2500, k=300  
![](Tahir2018Potentially_figs/f3a3931df73ac8d811547bea8e2cdd70a8c69135f3754a15bb6726f6acf8ad60.jpg)  
(c) PIB-RRT\*: i=1500, k=600  
Figure 10: Efect of k on exploitation/exploration

![](Tahir2018Potentially_figs/a0e142aed5c70b9485bd30115b83de6377b8585c1ebd245af869fe14f1a91894.jpg)  
Figure 11: PIB-RRT\*

![](Tahir2018Potentially_figs/c4a21120c7212b8ba0a7c230f45808775af1a64bc5069ae972116191f9328fb5.jpg)  
Figure 12: 30 Samples PIB-RRT\*

![](Tahir2018Potentially_figs/7503c19141c5b8cd1c5349bb3c36088dfe30b5cb29743154f85e37f0933c19f5.jpg)  
Figure 13: RRT\*

![](Tahir2018Potentially_figs/cb3719475bcdbaf222ba89cf719ea01eb1047aa65437516eb932345c0d2f6f8a.jpg)  
Figure 14: 1398 Samples RRT\*

Fig 10 displays the efect of k parameter of the $B P G ( )$ heuristic used in the proposed PIB-$\mathrm { R R T ^ { * } }$ and PB- $\mathrm { . R R T ^ { * } }$ algorithms. The efects of k parameter on exploitation and exploration can be clearly seen in Fig 10. As seen in the figure, lower values of k biases our Algorithm towards more exploration while higher values of k causes more exploitation. A balance has to be kept between exploration and exploitation for the proposed algorithms to work in all kinds of environments.

In Figure 11,12,13 and 14, PIB-RRT\* and $\mathrm { R R T ^ { * } }$ were run in the same environment till initial path was found. As seen in Fig 13 and Fig 14, $\mathrm { R R T ^ { * } }$ took 1398 samples to find the initial solution path. The Voronoi biasing of $\mathrm { R R T ^ { * } }$ is depicted in Fig $^ { 1 4 , }$ as observed it is quite uniform as no sample-biasing is present hence it took $\mathrm { R R T ^ { * } }$ 1398 samples just to find the initial solution path and the resultant path had a non optimal cost. Where as in Fig 11, PIB- $\mathrm { { . R R T ^ { * } } }$ took only 30 samples to find the solution path in the same environment. Fig 12 shows the efect of $B P G ( )$ heuristic of $\mathrm { P I B - R R T ^ { * } }$ on the Voronoi biasing. As seen the $B P G ( )$ heuristic potentially guides the random samples towards regions of higher intensity $I _ { \mathrm { z } }$ regions where rewiring rate is higher as stated in Theorem 4 and Theorem 5, hence the initial solution path was found in only 30 iterations and as seen in Fig 11, the initial path has optimal cost.

## 7. Conclusions and Future work

In this paper we have presented Bi-directional potential functions based asymptotically optimal, sampling path planning algorithms, PIB-RRT\* and $\mathrm { P B - R R T ^ { * } }$ which use $B P G ( )$ heuristic to potentially guide two Rapidly-exploring Random Trees towards each other, arguably the first of its kind, these algorithms $\mathrm { P I B - R R T ^ { * } }$ and $\mathrm { P B - R R T ^ { * } }$ have proven to be both theoretically and experimentally (1) similar in computational complexity as IB-RRT\*, $\mathrm { B { - } R R T ^ { * } }$ and $\mathrm { R R T } ^ { * } ; ( { \bf 2 } )$ provide asymptotic optimality; (3) avoids getting stuck in local minima as $A P F$ does; (4) converges to optimal solution faster than its state of the art counter parts such as IB-RRT\*, P-RRT\* and RRT\*; (5) lesser memory is consumed by PIB-RRT\* and PB-RRT\* as lesser iterations and time is required by them. By employing Bi-directional potential fields for the first time through fusing $\mathrm { A P F \ [ 1 9 ] }$ into bi-directional variants of $\mathrm { R R T ^ { * } }$ by using the proposed $B P G ( )$ heuristic, we have shown our proposed algorithms converge to optimal solution in the least amount of time and hence are of great importance in the physical real-time applications of motion planning of robots and online motion panniing of virtual characters and even can be used in nano robotics for surgery in the future.

In our future research, we plan to extend our algorithm for motion planning in dynamic environments [36] due to its rapid convergence to optimal solutions. Moreover, we also plan to leverage machine learning to cache feasible motion paths for experience-based motion planning that will enable our method to perform informed search for planning in new unseen environments.

## 8. Ackowledgements

The authors are greateful to Dr. Sertac Karaman of MIT for sharing the implementation of RRT\* Algorithm.

[1] J. Canny, The complexity of robot motion planning, The MIT press, 1988.

[2] J.-C. Latombe, Motion planning: A journey of robots, molecules, digital actors, and other artifacts, The International Journal of Robotics Research 18 (11) (1999) 1119–1128.

[3] R. D. Howe, Y. Matsuoka, Robotics for surgery, Annual Review of Biomedical Engineering 1 (1) (1999) 211–240.

[4] J.-C. Latombe, ROBOT MOTION PLANNING.: Edition en anglais, Springer, 1990.

[5] H. Chang, T.-Y. Li, Assembly maintainability study with motion planning, in: Robotics and Automation. Proceedings. IEEE International Conference on, Vol. 1, IEEE, 1995, pp. 1012– 1019.

[6] M. Girard, A. A. Maciejewski, Computational modeling for the computer animation of legged figures, in: ACM SIGGRAPH Computer Graphics, Vol. 19, ACM, 1985, pp. 263–270.

[7] J. T. Schwartz, M. Sharir, On the piano movers problem. ii. general techniques for computing topological properties of real algebraic manifolds, Advances in applied Mathematics 4 (3) (1983) 298–351.

[8] T. Lozano-P´erez, M. A. Wesley, An algorithm for planning collision-free paths among polyhedral obstacles, Communications of the ACM 22 (10) (1979) 560–570.

[9] T. L. Kunii, Visual Computing Integrating Computer Graphics with Computer Vision, Springer-Verlag, 1992.

[10] J. Reif, Z. Sun, Nano-robotics motion planning and its applications in nanotechnology and biomolecular computing, Tech. Rep. Duke University, Durham, NC 27705, Department of Computer Science, Duke University (May 1999).

[11] S. M. LaValle, Planning algorithms, Cambridge university press, 2006.

[12] D. Kuan, J. Zamiska, R. A. Brooks, Natural decomposition of free space for path planning, in: Robotics and Automation. Proceedings. IEEE International Conference on, Vol. 2, IEEE, 1985, pp. 168–173.

[13] R. A. Brooks, T. Lozano-Perez, A subdivision algorithm in configuration space for findpath with rotation.

[14] Y. Koren, J. Borenstein, Potential field methods and their inherent limitations for mobile robot navigation, in: Robotics and Automation. Proceedings. IEEE International Conference on, IEEE, 1991, pp. 1398–1404.

[15] R. Glasius, A. Komoda, S. C. Gielen, Neural network dynamics for path planning and obstacle avoidance, Neural Networks 8 (1) (1995) 125–133.

[16] S. R. Lindemann, S. M. LaValle, Incrementally reducing dispersion by increasing voronoi bias in RRTs, in: Robotics and Automation. Proceedings. ICRA’04. IEEE International Conference on, Vol. 4, IEEE, 2004, pp. 3251–3257.

[17] L. Kavraki, J.-C. Latombe, Randomized preprocessing of configuration for fast path planning, in: Robotics and Automation. Proceedings. IEEE International Conference on, IEEE, 1994, pp. 2138–2145.

[18] J. D. Gammell, S. S. Srinivasa, T. D. Barfoot, Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic, in: IEEE/RSJ International Conference on Intelligent Robots and Systems, 2014, pp. 2997–3004.

[19] O. Khatib, Real-time obstacle avoidance for manipulators and mobile robots, The international journal of robotics research 5 (1) (1986) 90–98.

[20] D. Hsu, J. C. Latombe, R. Motwani, Path planning in expansive configuration spaces, in: Proceedings of International Conference on Robotics and Automation, Vol. 3, 1997, pp. 2719– 2726 vol.3. doi:10.1109/ROBOT.1997.619371.

[21] L. E. Kavraki, P. Svestka, J. C. Latombe, M. H. Overmars, Probabilistic roadmaps for path planning in high-dimensional configuration spaces, IEEE Transactions on Robotics and Automation 12 (4) (1996) 566–580. doi:10.1109/70.508439.

[22] S. M. LaValle, Rapidly-exploring random trees a new tool for path planning, Tech. Rep. TR-98-11, Computer Science Department Iowa State University, Ames, Iowa, United States (October 1998).

[23] S. Karaman, E. Frazzoli, Incremental sampling-based algorithms for optimal motion planning, arXiv preprint arXiv:1005.0416.

[24] A. Perez, S. Karaman, A. Shkolnik, E. Frazzoli, S. Teller, M. R. Walter, Asymptoticallyoptimal path planning for manipulation using incremental sampling-based algorithms, in: IEEE/RSJ International Conference on Intelligent Robots and Systems, 2011, pp. 4307–4313. doi:10.1109/IROS.2011.6094994.

[25] C. Urmson, R. Simmons, Approaches for heuristically biasing RRT growth, in: International Conference on Intelligent Robots and Systems (IROS 2003), Vol. 2, IEEE, 2003, pp. 1178– 1183.

[26] D. Ferguson, A. Stentz, Anytime RRTs, in: International Conference on Intelligent Robots and Systems (IROS), IEEE, 2006, pp. 5369–5375.

[27] S. Karaman, E. Frazzoli, Sampling-based algorithms for optimal motion planning, The International Journal of Robotics Research 30 (7) (2011) 846–894.

[28] F. Islam, J. Nasir, U. Malik, Y. Ayaz, O. Hasan, RRT\*-Smart: Rapid convergence implementation of RRT\* towards optimal solution, in: IEEE International Conference on Mechatronics and Automation, 2012, pp. 1651–1656. doi:10.1109/ICMA.2012.6284384.

[29] A. H. Qureshi, Y. Ayaz, Potential functions based sampling heuristic for optimal path planning, Autonomous Robots 40 (6) (2016) 1079–1093.

[30] I. Garcia, J. P. How, Improving the eficiency of rapidly-exploring random trees using a potential function planner, in: Decision and Control and European Control Conference. CDC-ECC’05. 44th IEEE Conference on, IEEE, 2005, pp. 7965–7970.

[31] S. Karaman, M. R. Walter, A. Perez, E. Frazzoli, S. Teller, Anytime motion planning using the RRT\*, in: IEEE International Conference on Robotics and Automation, 2011, pp. 1478–1483. doi:10.1109/ICRA.2011.5980479.

[32] M. Jordan, A. Perez, Optimal bidirectional rapidly-exploring random trees, Tech. Rep. MIT-CSAIL-TR-2013-021, Computer Science and Artificial Intelligence Laboratory, Massachusetts Institute of Technology, Cambridge, MA (August 2013).

[33] A. H. Qureshi, S. Mumtaz, K. F. Iqbal, B. Ali, Y. Ayaz, F. Ahmed, M. S. Muhammad, O. Hasan, W. Y. Kim, M. Ra, Adaptive potential guided directional-RRT, in: IEEE International Conference on Robotics and Biomimetics (ROBIO), 2013.

[34] A. H. Qureshi, Y. Ayaz, Intelligent bidirectional rapidly-exploring random trees for optimal motion planning in complex cluttered environments, Robotics and Autonomous Systems 68 (2015) 1 – 11.

[35] J. J. Kufner Jr, S. M. LaValle, RRT-connect: An eficient approach to single-query path planning, in: Robotics and Automation. Proceedings. ICRA’00. IEEE International Conference on, Vol. 2, IEEE, 2000, pp. 995–1001.

[36] A. H. Qureshi, S. Mumtaz, W. Khan, A. A. A. Sheikh, K. F. Iqbal, Y. Ayaz, O. Hasan, Augmenting RRT\* planner with local trees for motion planning in complex dynamic environments, in: 19th International Conference on Methods and Models in Automation and Robotics (MMAR), 2014, pp. 657–662. doi:10.1109/MMAR.2014.6957432.