---
citation_key: Natarajan2025AMHA
arxiv_id: 2508.21637
arxiv_url: "https://arxiv.org/abs/2508.21637"
title: "A-MHA*: Anytime Multi-Heuristic A*"
authors_short: "Ramkumar Natarajan et al."
year: 2025
direction_tag: E_bounded_suboptimal_search
source: pymupdf4llm
converted_at: 2026-06-23T18:26:05Z
origin: ai+web
reviewed: false
---

# **A-MHA*: Anytime Multi-Heuristic A*** 

# **Ramkumar Natarajan** _[†]_[*] **, Muhammad Suhail Saleem** _[†]_[*] **, William Xiao** _[†]_ **, Sandip Aine** _[‡]_ **, Howie Choset** _[†]_ **, Maxim Likhachev** _[†]_ 

> _†_ The Robotics Institute, Carnegie Mellon University 

_‡_ Apple Inc. 

## **Abstract** 

Designing good heuristic functions for graph search requires adequate domain knowledge. It is often easy to design heuristics that perform well and correlate with the underlying true cost-to-go values in certain parts of the search space but these may not be admissible throughout the domain thereby affecting the optimality guarantees of the search. Bounded suboptimal search using several such partially good but inadmissible heuristics was developed in Multi-Heuristic A* (MHA*) (Aine et al. 2016). Although MHA* leverages multiple inadmissible heuristics to potentially generate a faster suboptimal solution, the original version does not improve the solution over time. It is a one shot algorithm that requires careful setting of inflation factors to obtain a desired one time solution. In this work, we tackle this issue by extending MHA* to an anytime version that finds a feasible suboptimal solution quickly and continually improves it until time runs out. Our work is inspired from the Anytime Repairing A* (ARA*) algorithm (Likhachev, Gordon, and Thrun 2004). We prove that our precise adaptation of ARA* concepts in the MHA* framework preserves the original suboptimal and completeness guarantees and enhances MHA* to perform in an anytime fashion. Furthermore, we report the performance of A- MHA* in 3-D path planning domain and sliding tiles puzzle and compare against MHA* and other anytime algorithms. 

## **Introduction** 

Real world and real-time planning requires utilizing the limited amount of time available to find a solution that is as close as possible to the optimal one. To that end, anytime algorithms have been developed that can generate a quick suboptimal solution and keep improving it over time. In addition, it is vital to know the quality of such intermediate solutions to decide whether to continue running the planner or to terminate it. Bounded suboptimal search algorithms deals with this problem and provides guarantees on the solution cost. Informed search or heuristic search is an important subclass of these search algorithms that employ underestimates of the true cost-to-go called heuristics to ensure completeness and find bounds on the solution quality. In order to ob- 

*These authors contributed equally. Copyright © 2019, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

tain such quantifiable solutions, these heuristics have to satisfy critical properties called admissibility and consistency for all the states in the entire search space. However, crafting heuristics that can obey those properties for large state spaces and high-dimensional planning problems are incredibly hard. 

In many real world scenarios, it is often easy to deduce heuristics that aims to partially solve the bigger problem in hand. Multi-Heuristic A* (Aine et al. 2016) is a recent work that tries to combine such arbitrarily inadmissible heuristics to speed up the search while ensuring strong guarantees. It needs the user to specify the desired suboptimality factor of the output solution prior to beginning the search. This is an extremely tricky step as one requires thorough domain knowledge to strike a balance between runtime and solution quality. In the absence of such domain knowledge, an anytime planner that can rapidly find a low quality solution and steer towards asymptotic convergence is preferred. However, this class of planners can provide guarantees only with consistent heuristics. Anytime Multi-Heuristic A* brings together the best of both worlds. It makes use of multiple inadmissible but informative heuristics supported by an admissible heuristic, to find a suboptimal path as quickly as possible and continues to improve it until the expiration of the allocated time. 

The rest of the paper is organized as follows: In the next section, we briefly go over the related work from anytime and multi-heuristic search. It will be followed by the proposed algorithm and the theoretical properties. We conclude with experimental results and future work. 

## **Related Work** 

Efficiency of informed search algorithms, such as A* rely heavily on the accuracy of the heuristic functions. A* with an admissible heuristic is a provable optimal algorithm. However, its runtime and memory requirements often makes it unusable for large state spaces. Weighted A* (WA*) (Pohl 1970) can dramatically improve the runtime as it inflates the heuristic with a factor _w >_ 1 _._ 0, providing a greedy flavor to the search. It is also a bounded suboptimal algorithm, _i.e._ , the solution obtained is bounded by _w_ times the optimal cost. With WA*, the reliance on the heuristic accuracy is 

magnified (compared to A*), and its performance can suffer significantly if the heuristic is subject to large local minima (Wilt and Ruml 2012). 

Multi Heuristic A*[1] (Aine et al. 2016) alleviates this problem of careful heuristic construction by using multiple heuristics simultaneously to explore a search space. MHA* uses one consistent heuristic and multiple (possibly) inadmissible heuristics, to guide the search around local minima. It often performs better by exploiting the synergy provided by different heuristics, each of which maybe useful in different parts of the search space. MHA* provides guarantees on completeness and bounded suboptimality along with bounds on state expansion (at most 2 expansions per state). There are variants of the MHA* that improves upon the original by using intelligent scheduling or better bounding (Narayanan, Aine, and Likhachev 2015). MHA* and its variants have been recently applied to several complex search problems including fullbody planning (Islam, Narayanan, and Likhachev 2015). 

A*, WA*, MHA* are all one shot algorithm, as such these do not provide a handle to reason about the trade-off between solution quality and runtime. Anytime search algorithms, on the other hand, iteratively improve the solution quality, and thus provide the user an opportunity to tradeoff runtime with solution quality. Anytime Repairing A* (ARA*) (Likhachev, Gordon, and Thrun 2004), is an anytime search algorithm that uses WA* for a particular iteration, and runs in an anytime mode by decreasing the suboptimality bound over time. ARA* has been successfully applied to many domains, such as autonomous cars, mobile manipulation, footstep planning, drones, etc. Other anytime search algorithms include, algorithms based on WA* (Richter, Thayer, and Ruml 2010) (Van Den Berg et al. 2011), beam search (Zhou and Hansen 2005), sliding window search (Aine, Chakrabarti, and Kumar 2007) etc. 

## **Anytime Multi-Heuristic A* (A-MHA*)** 

**Notations:** Let _s ∈S_ denote the finite set of discrete states over which we search for a path from _sstart_ to _sgoal_ . The search typically proceeds by expanding states to generate successors _s[′] ∈ Succ_ ( _s_ ) based on a priority. The current best cost and the optimal cost to arrive at a state _s_ is denoted by _g_ ( _s_ ) and _g[∗]_ ( _s_ ). _c_ ( _s, s[′]_ ) denotes the cost between any two states _s_ and _s[′]_ connected by an edge. 

As mentioned before, MHA* incorporates a single admissible heuristic _h_ 0( _s_ ) and multiple inadmissible heuristics denoted by _hi_ ( _s_ ) _, i_ = 1 _, ..., N_ . In this paper, we refer to this admissible search as the anchor search and the other searches as inadmissible searches. We assume that we have access to such admissible and inadmissible heuristics. Let the inflation of the anchor search be _w_ 1 and let _w_ 2 be the inflation factor to prioritize inadmissible search. Because of the anytime nature of the algorithm, the inflation factors are updated and the found solution is improved over time. They are initialized to _w_ 1[0][and] _[w]_ 2[0][and][updated][using][∆] _[w]_[1] 

1We refer to the Shared version of MHA* in the original paper as MHA* 

and ∆ _w_ 2. With one admissible heuristic and _N_ inadmissible heuristics, the _N_ + 1 priority queues of expansion are given by _OPEN_ 0 and _OPENi, i_ = 1 _, ..., N_ respectively. The priority of the states in _OPENi_ and _OPEN_ 0 are given by _key_ ( _s, i_ ) = _g_ ( _s_ ) + _w_ 1 _∗ hi_ ( _s_ ). In order to track and prevent re-expansions within a single search improvement routine, we have anchor and inadmissible closed lists and an inconsistent list denoted as _CLOSEDanch_ , _CLOSEDinad_ , and _INCONS_ respectively. 

## **Algorithm** 

The psuedocode of the proposed algorithm is presented in Algorithm 1. The structure of the A-MHA* is similar to anytime search algorithms like ARA* (Likhachev, Gordon, and Thrun 2004) or ANA* (Van Den Berg et al. 2011). The MAIN() function consists of the outer loop from which the IMPROVEPATH() function is called with the updated suboptimality bound. The IMPROVEPATH() function is a modified MHA* routine that guarantees _w_ 1 _∗ w_ 2 suboptimality and keeps track of inconsistent states to reuse the search results during the next iteration. It consists of two parts, the one that exploits the _w_ 1 bounded anchor search (Lines 23-24) and the other that explores the _w_ 1 _∗ w_ 2 bounded paths through inadmissible search (Lines 20-21). 

During every iteration of the IMPROVEPATH() function, the option of expanding a state from _OPEN_ 0 or _OPENi_ is decided depending on their minimum key and _w_ 2 (Line 19). We build on the notion of local inconsistency from ARA* (Likhachev, Gordon, and Thrun 2004) to introduce the inconsistent list in A-MHA* and keep track of the states which were already expanded and whose _g_ ( _s_ ) is reduced. During the EXPAND() operation, the state _s_ being expanded is popped from all the _N_ + 1 queues and checked if it could be a better predecessor (lower _g_ ( _s_ ) + _c_ ( _s, s[′]_ )) to any of the successors _s[′]_ . An update of _g_ ( _s[′]_ ) with a better predecessor could cause a local inconsistency between the g-value of _s[′]_ and all its successors which has to be propagated by putting _s[′]_ into _OPEN_ 0 and _OPENi_ . In case _s[′]_ is already expanded ( _i.e. s[′] ∈ CLOSEDanch_ or _CLOSEDinad_ ), we delay this propagation by maintaining an _INCONS_ list, an idea developed in ARA* (Lines 8-12). We note that only one _INCONS_ list is needed despite having two _CLOSED_ lists. This can be understood from the observation that all the states added to any _OPENi_ are also added to _OPEN_ 0 and when a state is expanded from _OPEN_ 0, it is never re-expanded from any other _OPENi_ in the same IMPROVEPATH() iteration. So if we find a better predecessor to a state which has not been expanded by _OPEN_ 0 yet, the priority of the state is updated in _OPEN_ 0 and if it has been expanded, it is added to the _INCONS_ list. Thus, after exiting IMPROVEPATH(), the states from both _OPEN_ 0 and _INCONS_ are added to both _OPEN_ 0 and _OPENi_ , thereby making sure that all the inconsistent states are tracked by just using _OPEN_ 0 and a single _INCONS_ list. 

After exiting from the IMPROVEPATH(), the solution obtained is guaranteed to be _w_ 1 _∗ w_ 2 suboptimal (proof in next subsection). Before the next call to IM- 

PROVEPATH(), we move the _INCONS_ states to _OPEN_ 0 and _OPENi_ , re-heap the queues, clear the _CLOSEDanch_ & _CLOSEDinad_ and update the _w_ 1 and _w_ 2 with ∆ _w_ 1 and ∆ _w_ 2 (Lines 31-40). 

## **Algorithm 1** Anytime Multi Heuristic A* algorithm 

1: **procedure** KEY( _s, i_ ) 2: **return** _g_ ( _s_ ) + _w_ 1 _∗ hi_ ( _s_ ); 3: **procedure** EXPAND( _s, i_ ) 4: Remove _s_ from _OPENi ∀ i_ = 0 _,_ 1 _...N_ 5: **for** each _s[′]_ in Succ(s) 6: **if** _g_ ( _s[′]_ ) _> g_ ( _s_ ) + _c_ ( _s, s[′]_ ) 7: _g_ ( _s[′]_ ) = _g_ ( _s_ ) + _c_ ( _s, s[′]_ ) 8: **if** _s[′]_ in _CLOSEDanch_ 9: Add _s[′]_ to _INCONS_ 10: **else** 11: Insert/Update _s[′]_ in _OPEN_ 0 with KEY( _s[′] ,_ 0) 12: **if** _s[′]_ not in _CLOSEDinad_ 13: **for** _i_ = 1 to _n_ 14: **if** KEY( _s[′] , i_ ) _≤ w_ 2 _∗_ KEY( _s[′] ,_ 0) 15: Insert/Update _s[′]_ in _OPENi_ with KEY( _s[′] , i_ ) 16: **procedure** IMPROVEPATH() 17: **while** _f_ ( _sgoal_ ) _> w_ 2 _∗ OPEN_ 0 _.Min_ () 18: **for** _i_ = 1 _...N_ 19: **if** ( _OPENi.Min_ () _≤ w_ 2 _∗ OPEN_ 0 _.Min_ ()) 20: s = _OPENi.Top_ () 21: EXPAND( _s, i_ ) and Insert s in _CLOSEDinad_ 22: **else** 23: s = _OPEN_ 0 _.Top_ () 24: EXPAND( _s,_ 0) and Insert s in _CLOSEDanch_ 25: **procedure** MAIN() 26: _w_ 1 = _w_ 1[0][;] _[ w]_[2][=] _[ w]_ 2[0][;] _[ g]_[(] _[s][start]_[) = 0][;] _[ g]_[(] _[s][goal]_[) =] _[ ∞]_[;] 27: **for** _i_ = 0 _...N_ 28: _OPENi_ = NULL 29: Insert _sstart_ in _OPENi_ with KEY( _s, i_ ) 30: **while** _w_ 1 _≥_ 1 and _w_ 2 _≥_ 1 31: _CLOSEDanch_ = _CLOSEDinad_ = NULL 32: _INCONS_ = NULL 33: IMPROVEPATH() 34: Publish current _w_ 1 _∗ w_ 2 suboptimal solution 35: **if** _w_ 1 == 1 and _w_ 2 == 1 36: **return** 37: _wi_ = _max_ ( _wi −_ ∆ _wi,_ 1); _i_ = 1 _,_ 2 38: Move states from _INCONS_ into _OPEN_ 0 39: Copy all states from _OPEN_ 0 to _OPENi_ 40: Update the priorities _∀s ∈ OPENi_ ; _∀i_ = 0 _..N_ 

## **Properties of A-MHA*** 

In this subsection, we provide two important properties of A-MHA*. First, we show that the solution provided by any IMPROVEPATH() call is _w_ 1 _∗ w_ 2 suboptimal. Next, we show that within each call of IMPROVEPATH(), a state is expanded at-most twice. 

**Theorem 1.** _At the exit of_ IMPROVEPATH() _, the cost of the greedy path from sstart to any state s, g_ ( _s_ ) _, is upperbounded by w_ 1 _∗ w_ 2 _times the cost of the optimal path to the_ 

_goal g[∗]_ ( _sgoal_ ) _._ 

_Proof._ From WA* we know that any state _s_ expanded by the anchor search has a priority (and thereby _g_ ( _s_ )) lesser than _w_ 1 times the optimal path cost _g[∗]_ ( _sgoal_ ) (since the admissible heuristic is an underestimate of the actual cost). By imposing the condition specified in line 19, we restrict the inadmissible expansions only to states whose priority is lesser than _w_ 1 _∗ w_ 2 times the optimal cost. Thus, for any state _s ∈ OPENi_ (whose heuristic could be an overestimate) to have a priority lesser than _w_ 1 _∗w_ 2 times the optimal cost, would imply that the current cost to reach that particular state _g_ ( _s_ ) is lesser than _w_ 1 _∗ w_ 2 times optimal path cost. Thus any expansion in the inadmissible search is bounded by _w_ 1 _∗ w_ 2 times optimal path cost, including the expansion of the _sgoal_ . Hence, the path found by IMPROVEPATH() is guaranteed to be _w_ 1 _∗ w_ 2 suboptimal. 

## **Theorem 2.** _Within a single_ IMPROVEPATH() _call, any state is expanded atmost twice._ 

_Proof._ If a state is expanded by a call to EXPAND(S) from anchor search in line 24, it is added to _CLOSEDanch_ and can never be expanded by both inadmissible and anchor search again (note the nested if condition between lines 8 and 15). Next, if a state is expanded by a call to EXPAND(S) from inadmissible search in line 21, it is added to _CLOSEDinad_ and can only be expanded by the anchor search (lines 12-15). Hence, in a single call to IMPROVEPATH(), a state can only be expanded atmost twice. 

## **Experimental Results** 

We evaluate the performance of A-MHA* on the sliding tiles puzzle and 3D navigation (x,y,orientation) domains and compare it with the performance of other state of the art search algorithms. The experiments are setup similar to those in the original MHA* paper (Aine et al. 2016), to accurately evaluate the performance of our algorithm and compare in a fair manner. 

## **3D Path Planning** 

Here, we plan for a polygonal robot with three degrees of freedom (x,y,orientation) in a 2-D planar environment. The plan has to satisfy the minimum turning radius constraints of the robot, which is imposed using motion primitives for generating successors from a state (similar to the lattice type planner (Likhachev and Ferguson 2009)). 

The consistent heuristic, which is the same across all the different planners, is the euclidean distance from the goal. In addition to this, the inadmissible heuristics used for MHA* and A-MHA* include an 8-connected Dijkstra search assuming the robot to have zero size and two other progressive heuristics obtained by running 8-connected Dijkstra search on a map created by blocking the narrow passages (passage width _≤_ robot size) present in the current map. 

From Figure 1 and 2, it is clear that A-MHA* is capable of producing a high quality solution much quicker than the 


![](1_survey/papers/md/Natarajan2025AMHA_figs/Natarajan2025AMHA.pdf-0004-00.png)


**----- Start of picture text -----**<br>
10 [5] Solution Cost vs Time<br>4.5<br>ARA*<br>4 A-MHA*<br>MHA*<br>ANA*<br>3.5<br>3<br>2.5<br>2<br>1.5<br>1<br>0.5<br>0<br>0 2 4 6 8 10<br>Time<br>Solution Cost<br>**----- End of picture text -----**<br>


Figure 1: Solution Cost vs Time for 3D planning 


![](1_survey/papers/md/Natarajan2025AMHA_figs/Natarajan2025AMHA.pdf-0004-02.png)


**----- Start of picture text -----**<br>
G/G* vs Time<br>12<br>ARA*<br>A-MHA*<br>10 MHA*<br>ANA*<br>8<br>6<br>4<br>2<br>0<br>0 0.5 1 1.5 2 2.5 3 3.5 4<br>Time<br>G/G*<br>**----- End of picture text -----**<br>


Figure 2: Suboptimality of solution vs Time for 3D planning 

other algorithms, which it continues to improve over time. However, it has to be noted that the usage of inadmissible heuristics delays the convergence to optimal solution. 

## **Sliding Tiles Puzzle** 

In this subsection, we present the results for 48 and 63 sliding tiles puzzle, a domain commonly used to evaluate search algorithms. The consistent heuristic for this domain which is widely used in this literature is the sum of the Manhattan Distance ( _MD_ ) and the Linear Conflict ( _LC_ ). Similar to the original MHA* paper, the inconsistent heuristics are a 

|**Metric**|**A-MHA***|**ARA***|**ANA***|**MHA***|
|---|---|---|---|---|
|Success rate|88.24|70.59|44.18|88.24|
|_Tinitial_|9.69|18.99|23.13|9.69|
|_Tfinal_|39.70|29.82|41.73|9.69|
|_ϵinitial_|25|25|3.58e+07|25|
|_ϵfinal_|4|5.1667|3.31|25|



Table 1: Average statistics for 50 instances of 63 tile sliding puzzle: _Tinitial_ - Time to produce the first solution; _Tfinal_ - Time to produce the final solution; _ϵinitial_ - Reported Initial suboptimality bound; _ϵfinal_ - Reported final suboptimality bound. 

|**Metric**|**A-MHA***|**ARA***|**ANA***|**MHA***|
|---|---|---|---|---|
|Success rate|100|75|75|100|
|_Tinitial_|17.51|15.05|42.41|17.51|
|_Tfinal_|42.90|31.075|111.42|17.51|
|_ϵinitial_|25|25|2.95e+07|25|
|_ϵfinal_|7.33|8.77|7.90|25|



Table 2: Average statistics for 50 instances of 48 tile sliding puzzle: _Tinitial_ - _Tinitial_ - Time to produce the first solution; _Tfinal_ - Time to produce the final solution; _ϵinitial_ - Reported Initial suboptimality bound; _ϵfinal_ - Reported final suboptimality bound. 

weighted sum of the number of misplaced tiles ( _MT_ ), _MD_ and _LC_ , where the weights are randomly generated during execution. 

From Table. 1 and 2, we understand that A-MHA* has the highest success rate (number of instances for which the puzzle was solved within a limited time) and clearly outperforms the other algorithms consistently. For 63 tile sliding puzzles, similar to the previous domain, A-MHA* produces high quality solutions in much lesser time, while converging to the final suboptimality bound slower. However, for the 48 tiles sliding puzzle environment, the performance of A- MHA* is comparable to that of ARA*. This is because the effect of the additional heuristics in a smaller environment might not have the same impact as it did in a bigger/complex environment and hence might not outweigh the overhead in maintaining several heaps. 

## **Conclusion** 

We presented an anytime version of MHA*, while preserving completeness, expansion and suboptimality guarantees. Experimental results in two different domains strongly favor A-MHA* over the other anytime algorithms. This simple algorithm brings together the benefits of both ARA* and MHA*, thereby maximizing the performance in terms of both solution quality and run-time. One interesting future work could be nonparametrize the inflation factors of A-MHA* to circumvent the tedious process of tuning them. 

## **References** 

Aine, S.; Swaminathan, S.; Narayanan, V.; Hwang, V.; and Likhachev, M. 2016. Multi-heuristic a. _The International Journal of Robotics Research_ 35(1-3):224–243. 

Aine, S.; Chakrabarti, P.; and Kumar, R. 2007. Awa*-a window constrained anytime heuristic search algorithm. In _IJCAI_ , 2250–2255. 

Islam, F.; Narayanan, V.; and Likhachev, M. 2015. Dynamic multi-heuristic a. In _2015 IEEE International Conference on Robotics and Automation (ICRA)_ , 2376–2382. IEEE. 

Likhachev, M., and Ferguson, D. 2009. Planning long dynamically feasible maneuvers for autonomous vehicles. _The International Journal of Robotics Research_ 28(8):933–945. 

Likhachev, M.; Gordon, G. J.; and Thrun, S. 2004. Ara*: Anytime a* with provable bounds on sub-optimality. In _Advances in neural information processing systems_ , 767–774. 

Narayanan, V.; Aine, S.; and Likhachev, M. 2015. Improved multi-heuristic a* for searching with uncalibrated heuristics. In _Eighth Annual Symposium on Combinatorial Search_ . 

Pohl, I. 1970. Heuristic search viewed as path finding in a graph. _Artificial intelligence_ 1(3-4):193–204. 

Richter, S.; Thayer, J. T.; and Ruml, W. 2010. The joy of forgetting: Faster anytime search via restarting. In _Twentieth International Conference on Automated Planning and Scheduling_ . 

Van Den Berg, J.; Shah, R.; Huang, A.; and Goldberg, K. 2011. Anytime nonparametric a. In _Twenty-Fifth AAAI Conference on Artificial Intelligence_ . 

Wilt, C. M., and Ruml, W. 2012. When does weighted a* fail? In _SOCS_ , 137–144. 

Zhou, R., and Hansen, E. A. 2005. Beam-stack search: Integrating backtracking with beam search. In _ICAPS_ , 90– 98. 

