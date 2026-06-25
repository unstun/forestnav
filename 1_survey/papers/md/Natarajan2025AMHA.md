---
citation_key: Natarajan2025AMHA
arxiv_id: 2508.21637
arxiv_url: "https://arxiv.org/abs/2508.21637"
title: "A-MHA*: Anytime Multi-Heuristic A*"
authors_short: "Ramkumar Natarajan et al."
year: 2025
direction_tag: E_bounded_suboptimal_search
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:15:11Z
origin: ai+web
reviewed: false
---

# A-MHA\*: Anytime Multi-Heuristic A\*

Ramkumar Natarajan<sup>†</sup>\*, Muhammad Suhail Saleem<sup>†</sup>\*, William Xiao<sup>†</sup>, Sandip Aine<sup>‡</sup>, Howie Choset<sup>†</sup>, Maxim Likhachev<sup>†</sup> <sup>†</sup>The Robotics Institute, Carnegie Mellon University <sup>‡</sup> Apple Inc.

## Abstract

Designing good heuristic functions for graph search requires adequate domain knowledge. It is often easy to design heuristics that perform well and correlate with the underlying true cost-to-go values in certain parts of the search space but these may not be admissible throughout the domain thereby affecting the optimality guarantees of the search. Bounded suboptimal search using several such partially good but inadmissible heuristics was developed in Multi-Heuristic A\* (MHA\*) (Aine et al. 2016). Although MHA\* leverages multiple inadmissible heuristics to potentially generate a faster suboptimal solution, the original version does not improve the solution over time. It is a one shot algorithm that requires careful setting of inflation factors to obtain a desired one time solution. In this work, we tackle this issue by extending MHA\* to an anytime version that finds a feasible suboptimal solution quickly and continually improves it until time runs out. Our work is inspired from the Anytime Repairing A\* (ARA\*) algorithm (Likhachev, Gordon, and Thrun 2004). We prove that our precise adaptation of ARA\* concepts in the MHA\* framework preserves the original suboptimal and completeness guarantees and enhances MHA\* to perform in an anytime fashion. Furthermore, we report the performance of A-MHA\* in 3-D path planning domain and sliding tiles puzzle and compare against MHA\* and other anytime algorithms.

## Introduction

Real world and real-time planning requires utilizing the limited amount of time available to find a solution that is as close as possible to the optimal one. To that end, anytime algorithms have been developed that can generate a quick suboptimal solution and keep improving it over time. In addition, it is vital to know the quality of such intermediate solutions to decide whether to continue running the planner or to terminate it. Bounded suboptimal search algorithms deals with this problem and provides guarantees on the solution cost. Informed search or heuristic search is an important subclass of these search algorithms that employ underestimates of the true cost-to-go called heuristics to ensure completeness and find bounds on the solution quality. In order to obtain such quantifiable solutions, these heuristics have to satisfy critical properties called admissibility and consistency for all the states in the entire search space. However, crafting heuristics that can obey those properties for large state spaces and high-dimensional planning problems are incredibly hard.

In many real world scenarios, it is often easy to deduce heuristics that aims to partially solve the bigger problem in hand. Multi-Heuristic A\* (Aine et al. 2016) is a recent work that tries to combine such arbitrarily inadmissible heuristics to speed up the search while ensuring strong guarantees. It needs the user to specify the desired suboptimality factor of the output solution prior to beginning the search. This is an extremely tricky step as one requires thorough domain knowledge to strike a balance between runtime and solution quality. In the absence of such domain knowledge, an anytime planner that can rapidly find a low quality solution and steer towards asymptotic convergence is preferred. However, this class of planners can provide guarantees only with consistent heuristics. Anytime Multi-Heuristic A\* brings together the best of both worlds. It makes use of multiple inadmissible but informative heuristics supported by an admissible heuristic, to find a suboptimal path as quickly as possible and continues to improve it until the expiration of the allocated time.

The rest of the paper is organized as follows: In the next section, we briefly go over the related work from anytime and multi-heuristic search. It will be followed by the proposed algorithm and the theoretical properties. We conclude with experimental results and future work.

## Related Work

Efficiency of informed search algorithms, such as A\* rely heavily on the accuracy of the heuristic functions. A\* with an admissible heuristic is a provable optimal algorithm. However, its runtime and memory requirements often makes it unusable for large state spaces. Weighted A\* (WA\*) (Pohl 1970) can dramatically improve the runtime as it inflates the heuristic with a factor w > 1.0, providing a greedy flavor to the search. It is also a bounded suboptimal algorithm, i.e., the solution obtained is bounded by w times the optimal cost. With WA\*, the reliance on the heuristic accuracy is magnified (compared to $\mathbf { A } ^ { * } )$ , and its performance can suffer significantly if the heuristic is subject to large local minima (Wilt and Ruml 2012).

Multi Heuristic $\mathbf { A } ^ { * } \mathbf { \Sigma } ^ { 1 } \mathbf { \Sigma } ( \mathrm { A i n e }$ et al. 2016) alleviates this problem of careful heuristic construction by using multiple heuristics simultaneously to explore a search space. $\mathrm { M H A ^ { * } }$ uses one consistent heuristic and multiple (possibly) inadmissible heuristics, to guide the search around local minima. It often performs better by exploiting the synergy provided by different heuristics, each of which maybe useful in different parts of the search space. MHA\* provides guarantees on completeness and bounded suboptimality along with bounds on state expansion (at most 2 expansions per state). There are variants of the $\mathrm { M H A ^ { * } }$ that improves upon the original by using intelligent scheduling or better bounding (Narayanan, Aine, and Likhachev 2015). MHA\* and its variants have been recently applied to several complex search problems including fullbody planning (Islam, Narayanan, and Likhachev 2015).

A\*, WA\*, MHA\* are all one shot algorithm, as such these do not provide a handle to reason about the trade-off between solution quality and runtime. Anytime search algorithms, on the other hand, iteratively improve the solution quality, and thus provide the user an opportunity to tradeoff runtime with solution quality. Anytime Repairing $\mathbf { A } ^ { * }$ (ARA\*) (Likhachev, Gordon, and Thrun 2004), is an anytime search algorithm that uses $\mathrm { W A ^ { * } }$ for a particular iteration, and runs in an anytime mode by decreasing the suboptimality bound over time. $\mathbf { A } \mathbf { R } \mathbf { A } ^ { * }$ has been successfully applied to many domains, such as autonomous cars, mobile manipulation, footstep planning, drones, etc. Other anytime search algorithms include, algorithms based on $\mathrm { W A ^ { * } }$ (Richter, Thayer, and Ruml 2010) (Van Den Berg et al. 2011), beam search (Zhou and Hansen 2005), sliding window search (Aine, Chakrabarti, and Kumar 2007) etc.

## Anytime Multi-Heuristic A\* (A-MHA\*)

Notations: Let $s \in S$ denote the finite set of discrete states over which we search for a path from $s _ { s t a r t } \ \mathbf { t o } \ s _ { g o a l }$ . The search typically proceeds by expanding states to generate successors $s ^ { \prime } \in S u c c ( s )$ based on a priority. The current best cost and the optimal cost to arrive at a state s is denoted $g ( s )$ and $g ^ { * } ( s ) . c ( s , s ^ { \prime } )$ denotes the cost between any two states s and $s ^ { \prime }$ connected by an edge.

As mentioned before, $\mathrm { M H A ^ { * } }$ incorporates a single admissible heuristic $h _ { 0 } ( s )$ and multiple inadmissible heuristics denoted by $h _ { i } ( s ) , \ i = 1 , . . . , N$ . In this paper, we refer to this admissible search as the anchor search and the other searches as inadmissible searches. We assume that we have access to such admissible and inadmissible heuristics. Let the inflation of the anchor search be $w _ { 1 }$ and let $w _ { 2 }$ be the inflation factor to prioritize inadmissible search. Because of the anytime nature of the algorithm, the inflation factors are updated and the found solution is improved over time. They are initialized to $w _ { 1 } ^ { 0 }$ and $w _ { 2 } ^ { 0 }$ and updated using $\Delta w _ { 1 }$ and $\Delta w _ { 2 }$ . With one admissible heuristic and N inadmissible heuristics, the $N + 1$ priority queues of expansion are given by $O P E N _ { 0 }$ and $\dot { O P E N _ { i } } , \dot { i } \stackrel { \cdot } { = } 1 , . . . , N$ respectively. The priority of the states in $O P E N _ { i }$ and $O P E N _ { 0 }$ are given by $k e y ( s , i ) = g ( s ) + w _ { 1 } * h _ { i } ( s )$ . In order to track and prevent re-expansions within a single search improvement routine, we have anchor and inadmissible closed lists and an inconsistent list denoted as $C L O S E D _ { a n c h } , C L O S E D _ { i n a d } .$ , and INCONS respectively.

## Algorithm

The psuedocode of the proposed algorithm is presented in Algorithm 1. The structure of the $\mathbf { A } \mathbf { - } \mathbf { M } \mathbf { H } \mathbf { A } ^ { * }$ is similar to anytime search algorithms like $\mathbf { A } \mathbf { R } \mathbf { A } ^ { * }$ (Likhachev, Gordon, and Thrun 2004) or ANA\* (Van Den Berg et al. 2011). The MAIN() function consists of the outer loop from which the IMPROVEPATH() function is called with the updated suboptimality bound. The IMPROVEPATH() function is a modified $\mathrm { { \bf M H A } ^ { * } }$ routine that guarantees $w _ { 1 } * w _ { 2 }$ suboptimality and keeps track of inconsistent states to reuse the search results during the next iteration. It consists of two parts, the one that exploits the $w _ { 1 }$ bounded anchor search (Lines 23-24) and the other that explores the $w _ { 1 } * w _ { 2 }$ bounded paths through inadmissible search (Lines 20-21).

During every iteration of the IMPROVEPATH() function, the option of expanding a state from $O P E N _ { 0 }$ or $O P E N _ { i }$ is decided depending on their minimum key and $w _ { 2 }$ (Line 19). We build on the notion of local inconsistency from $\mathbf { A } \mathbf { R } \mathbf { A } ^ { * }$ (Likhachev, Gordon, and Thrun 2004) to introduce the inconsistent list in $\mathbf { A } \mathbf { - } \mathbf { M } \mathbf { H } \mathbf { A } ^ { * }$ and keep track of the states which were already expanded and whose $g ( s )$ is reduced. During the EXPAND() operation, the state s being expanded is popped from all the $N + 1$ queues and checked if it could be a better predecessor (lower $\operatorname { \dot { \theta } } ( s ) + c ( s , s ^ { \prime } ) )$ to any of the successors $s ^ { \prime } .$ An update of $g ( s ^ { \prime } )$ with a better predecessor could cause a local inconsistency between the g-value of $s ^ { \prime }$ and all its successors which has to be propagated by putting $s ^ { \prime }$ into $O P E N _ { 0 }$ and $O P E N _ { i }$ . In case $s ^ { \prime }$ is already expanded $( i . e . ~ s ^ { \prime } ~ \in ~ C L O S E D _ { a n c h }$ or $C L O S E D _ { i n a d } ) ,$ we delay this propagation by maintaining an $I N C O N S$ list, an idea developed in $\mathbf { A } \mathbf { R } \mathbf { A } ^ { * }$ (Lines 8-12). We note that only one INCONS list is needed despite having two $C L O S \bar { E } D$ lists. This can be understood from the observation that all the states added to any $O P E N _ { i }$ are also added to $O P E N _ { 0 }$ and when a state is expanded from $O P E N _ { 0 } ,$ , it is never re-expanded from any other $O P E N _ { i }$ in the same IMPROVEPATH() iteration. So if we find a better predecessor to a state which has not been expanded by $O P E N _ { 0 }$ yet, the priority of the state is updated in $O P E N _ { 0 }$ and if it has been expanded, it is added to the INCONS list. Thus, after exiting IMPROVEPATH(), the states from both $O P E N _ { 0 }$ and $I N C O N S$ are added to both $O P E N _ { 0 }$ and $O P E N _ { i }$ , thereby making sure that all the inconsistent states are tracked by just using $O P E N _ { 0 }$ and a single INCONS list.

After exiting from the IMPROVEPATH(), the solution obtained is guaranteed to be $w _ { 1 } ~ * ~ w _ { 2 }$ suboptimal (proof in next subsection). Before the next call to IM-

PROVEPATH(), we move the INCONS states to $O P E N _ { 0 }$ and $O P E N _ { i } ,$ , re-heap the queues, clear the $C L O S E D _ { a n c h }$ & $C L O S E D _ { i n a d }$ and update the $w _ { 1 }$ and $w _ { 2 }$ with $\Delta w _ { 1 }$ and $\Delta w _ { 2 }$ (Lines 31-40).

```txt
Algorithm 1 Anytime Multi Heuristic A* algorithm
1: procedure KEY(s, i)
2:    return g(s) + w₁ * hᵢ(s);
3: procedure EXPAND(s, i)
4:    Remove s from OPENᵢ ∀ i = 0, 1...N
5:    for each s' in Succ(s)
6:    if g(s') > g(s) + c(s, s')
7:    g(s') = g(s) + c(s, s')
8:    if s' in CLOSEDₐₙch
9:    Add s' to INCONS
10:    else
11:    Insert/Update s' in OPEN₀ with KEY(s', 0)
12:    if s' not in CLOSEDₐₙad
13:    for i = 1 to n
14:    if KEY(s', i) ≤ w₂ * KEY(s', 0)
15:    Insert/Update s' in OPENᵢ with KEY(s', i)
16: procedure IMPROVEPATH()
17:    while f(s_goal) > w₂ * OPEN₀.Min()
18:    for i = 1...N
19:    if(OPENᵢ.Min() ≤ w₂ * OPEN₀.Min())
20:    s = OPENᵢ.Top()
21:    EXPAND(s, i) and Insert s in CLOSEDₐₙad
22:    else
23:    s = OPEN₀.Top()
24:    EXPAND(s, 0) and Insert s in CLOSEDₐₙch
25: procedure MAIN()
26:    w₁ = w₁⁰; w₂ = w₂⁰; g(sₛₜₐₜ) = 0; g(sₛₜₐₗ) = ∞;
27:    for i = 0...N
28:    OPENᵢ = NULL
29:    Insert sₛₜₐₜ in OPENᵢ with KEY(s, i)
30:    while w₁ ≥ 1 and w₂ ≥ 1
31:    CLOSEDₐₙch = CLOSEDₐₙad = NULL
32:    INCONS = NULL
33:    IMPROVEPATH()
34:    Publish current w₁ * w₂ suboptimal solution
35:    if w₁ == 1 and w₂ == 1
36:    return
37:    wᵢ = max(wᵢ - Δwᵢ, 1); i = 1, 2
38:    Move states from INCONS into OPEN₀
39:    Copy all states from OPEN₀ to OPENᵢ
40:    Update the priorities ∀s ∈ OPENᵢ; ∀i = 0..N
```

## Properties of A-MHA\*

In this subsection, we provide two important properties of A-MHA\*. First, we show that the solution provided by any IMPROVEPATH() call is $w _ { 1 } * w _ { 2 }$ suboptimal. Next, we show that within each call of IMPROVEPATH(), a state is expanded at-most twice.

Theorem 1. At the exit of IMPROVEPATH(), the cost of the greedy path from $s _ { s t a r t }$ to any state $s , \ g ( s )$ , is upperbounded by $w _ { 1 }$ ∗ w<sub>2</sub> times the cost of the optimal path to the

goal $g ^ { \ast } \big ( s _ { g o a l } \big ) .$

Proof. From $\mathrm { W A ^ { * } }$ we know that any state s expanded by the anchor search has a priority (and thereby $g ( s ) )$ lesser than $w _ { 1 }$ times the optimal path cost $g ^ { \ast } \big ( s _ { g o a l } \big )$ (since the admissible heuristic is an underestimate of the actual cost). By imposing the condition specified in line 19, we restrict the inadmissible expansions only to states whose priority is lesser than $w _ { 1 } * w _ { 2 }$ times the optimal cost. Thus, for any state $s \in O P E N _ { i }$ (whose heuristic could be an overestimate) to have a priority lesser than $w _ { 1 } * w _ { 2 }$ times the optimal cost, would imply that the current cost to reach that particular state $g ( s )$ is lesser than $w _ { 1 } * w _ { 2 }$ times optimal path cost. Thus any expansion in the inadmissible search is bounded by $w _ { 1 } * w _ { 2 }$ times optimal path cost, including the expansion of the $s _ { g o a l }$ . Hence, the path found by IMPROVEPATH() is guaranteed to be w1 ∗ w2 suboptimal.

Theorem 2. Within a single IMPROVEPATH() call, any state is expanded atmost twice.

Proof. If a state is expanded by a call to EXPAND(S) from anchor search in line 24, it is added to $C L O S E D _ { a n c h }$ and can never be expanded by both inadmissible and anchor search again (note the nested if condition between lines 8 and 15). Next, if a state is expanded by a call to EXPAND(S) from inadmissible search in line 21, it is added to $C L O S E D _ { i n a d }$ and can only be expanded by the anchor search (lines 12-15). Hence, in a single call to IMPROVEPATH(), a state can only be expanded atmost twice. □

## Experimental Results

We evaluate the performance of $\mathbf { A } \mathbf { - } \mathbf { M } \mathbf { H } \mathbf { A } ^ { * }$ on the sliding tiles puzzle and 3D navigation (x,y,orientation) domains and compare it with the performance of other state of the art search algorithms. The experiments are setup similar to those in the original MHA\* paper (Aine et al. 2016), to accurately evaluate the performance of our algorithm and compare in a fair manner.

## 3D Path Planning

Here, we plan for a polygonal robot with three degrees of freedom (x,y,orientation) in a 2-D planar environment. The plan has to satisfy the minimum turning radius constraints of the robot, which is imposed using motion primitives for generating successors from a state (similar to the lattice type planner (Likhachev and Ferguson 2009)).

The consistent heuristic, which is the same across all the different planners, is the euclidean distance from the goal. In addition to this, the inadmissible heuristics used for $\mathbf { \bar { M H A } ^ { * } }$ and A-MHA\* include an 8-connected Dijkstra search assuming the robot to have zero size and two other progressive heuristics obtained by running 8-connected Dijkstra search on a map created by blocking the narrow passages (passage width ≤ robot size) present in the current map.

From Figure 1 and 2, it is clear that $\mathbf { A } \mathbf { - } \mathbf { M } \mathbf { H } \mathbf { A } ^ { \ast }$ is capable of producing a high quality solution much quicker than the other algorithms, which it continues to improve over time. However, it has to be noted that the usage of inadmissible heuristics delays the convergence to optimal solution.

![](Natarajan2025AMHA_figs/29002fbfb800b6ef895db13830b1c50948a503c79cb0b37ed908c7ed90d6ab38.jpg)  
Figure 1: Solution Cost vs Time for 3D planning

![](Natarajan2025AMHA_figs/fd436e2e2eb1b7006b96d1c0ab2e4ad607fd36de461bc72d7eea44fbab350ef3.jpg)  
Figure 2: Suboptimality of solution vs Time for 3D planning

## Sliding Tiles Puzzle

In this subsection, we present the results for 48 and 63 sliding tiles puzzle, a domain commonly used to evaluate search algorithms. The consistent heuristic for this domain which is widely used in this literature is the sum of the Manhattan Distance (MD) and the Linear Conflict (LC). Similar to the original MHA\* paper, the inconsistent heuristics are a weighted sum of the number of misplaced tiles (MT ), MD and LC, where the weights are randomly generated during execution.

<table><tr><td>Metric</td><td>A-MHA*</td><td>ARA*</td><td>ANA*</td><td>MHA*</td></tr><tr><td>Success rate</td><td>88.24</td><td>70.59</td><td>44.18</td><td>88.24</td></tr><tr><td> $T_{initial}$ </td><td>9.69</td><td>18.99</td><td>23.13</td><td>9.69</td></tr><tr><td> $T_{final}$ </td><td>39.70</td><td>29.82</td><td>41.73</td><td>9.69</td></tr><tr><td> $\epsilon_{initial}$ </td><td>25</td><td>25</td><td>3.58e+07</td><td>25</td></tr><tr><td> $\epsilon_{final}$ </td><td>4</td><td>5.1667</td><td>3.31</td><td>25</td></tr></table>

Table 1: Average statistics for 50 instances of 63 tile sliding puzzle: $T _ { i n i t i a l }$ - Time to produce the first solution; $T _ { f i n a l } -$ Time to produce the final solution; $\epsilon _ { i n i t i a l }$ - Reported Initial suboptimality bound; $\epsilon _ { f i n a l }$ - Reported final suboptimality bound.

<table><tr><td>Metric</td><td>A-MHA*</td><td>ARA*</td><td>ANA*</td><td>MHA*</td></tr><tr><td>Success rate</td><td>100</td><td>75</td><td>75</td><td>100</td></tr><tr><td> $T_{initial}$ </td><td>17.51</td><td>15.05</td><td>42.41</td><td>17.51</td></tr><tr><td> $T_{final}$ </td><td>42.90</td><td>31.075</td><td>111.42</td><td>17.51</td></tr><tr><td> $\epsilon_{initial}$ </td><td>25</td><td>25</td><td>2.95e+07</td><td>25</td></tr><tr><td> $\epsilon_{final}$ </td><td>7.33</td><td>8.77</td><td>7.90</td><td>25</td></tr></table>

Table 2: Average statistics for 50 instances of 48 tile sliding puzzle: $T _ { i n i t i a l } \ - \ T _ { i n i t i a l } \ -$ Time to produce the first solution; $T _ { f i n a l }$ - Time to produce the final solution; $\epsilon _ { i n i t i a l } \ -$ Reported Initial suboptimality bound; $\epsilon _ { f i n a l }$ - Reported final suboptimality bound.

From Table. 1 and 2, we understand that A-MHA\* has the highest success rate (number of instances for which the puzzle was solved within a limited time) and clearly outperforms the other algorithms consistently. For 63 tile sliding puzzles, similar to the previous domain, A-MHA\* produces high quality solutions in much lesser time, while converging to the final suboptimality bound slower. However, for the 48 tiles sliding puzzle environment, the performance of A-MHA\* is comparable to that of ARA\*. This is because the effect of the additional heuristics in a smaller environment might not have the same impact as it did in a bigger/complex environment and hence might not outweigh the overhead in maintaining several heaps.

## Conclusion

We presented an anytime version of MHA\*, while preserving completeness, expansion and suboptimality guarantees. Experimental results in two different domains strongly favor A-MHA\* over the other anytime algorithms. This simple algorithm brings together the benefits of both ARA\* and MHA\*, thereby maximizing the performance in terms of both solution quality and run-time. One interesting future work could be nonparametrize the inflation factors of A-MHA\* to circumvent the tedious process of tuning them.

## References

Aine, S.; Swaminathan, S.; Narayanan, V.; Hwang, V.; and Likhachev, M. 2016. Multi-heuristic a. The International Journal of Robotics Research 35(1-3):224–243.

Aine, S.; Chakrabarti, P.; and Kumar, R. 2007. Awa\*-a window constrained anytime heuristic search algorithm. In IJCAI, 2250–2255.

Islam, F.; Narayanan, V.; and Likhachev, M. 2015. Dynamic multi-heuristic a. In 2015 IEEE International Conference on Robotics and Automation (ICRA), 2376–2382. IEEE.

Likhachev, M., and Ferguson, D. 2009. Planning long dynamically feasible maneuvers for autonomous vehicles. The International Journal of Robotics Research 28(8):933–945.

Likhachev, M.; Gordon, G. J.; and Thrun, S. 2004. Ara\*: Anytime a\* with provable bounds on sub-optimality. In Advances in neural information processing systems, 767–774.

Narayanan, V.; Aine, S.; and Likhachev, M. 2015. Improved multi-heuristic a\* for searching with uncalibrated heuristics. In Eighth Annual Symposium on Combinatorial Search.

Pohl, I. 1970. Heuristic search viewed as path finding in a graph. Artificial intelligence 1(3-4):193–204.

Richter, S.; Thayer, J. T.; and Ruml, W. 2010. The joy of forgetting: Faster anytime search via restarting. In Twentieth International Conference on Automated Planning and Scheduling.

Van Den Berg, J.; Shah, R.; Huang, A.; and Goldberg, K. 2011. Anytime nonparametric a. In Twenty-Fifth AAAI Conference on Artificial Intelligence.

Wilt, C. M., and Ruml, W. 2012. When does weighted a\* fail? In SOCS, 137–144.

Zhou, R., and Hansen, E. A. 2005. Beam-stack search: Integrating backtracking with beam search. In ICAPS, 90– 98.