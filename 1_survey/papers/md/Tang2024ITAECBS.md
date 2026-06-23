---
citation_key: Tang2024ITAECBS
arxiv_id: 2404.05223
arxiv_url: "https://arxiv.org/abs/2404.05223"
title: "ITA-ECBS: A Bounded-Suboptimal Algorithm for the Combined Target-Assignment and Path-Finding Problem"
authors_short: "Yimin Tang et al."
year: 2024
direction_tag: E_bounded_suboptimal_search
source: pymupdf4llm
converted_at: 2026-06-23T19:08:25Z
origin: ai+web
reviewed: false
---

# **ITA-ECBS: A Bounded-Suboptimal Algorithm for the Combined Target-Assignment and Path-Finding Problem** 

## **Yimin Tang**[1] **, Sven Koenig**[1] **, Jiaoyang Li**[2] 

1University of Southern California, USA 

2Carnegie Mellon University, USA 

_{_ yimint,skoenig _}_ @usc.edu, jiaoyangli@cmu.edu 

## **Abstract** 

Multi-Agent Path Finding (MAPF), i.e., finding collisionfree paths for multiple robots, plays a critical role in many applications. Sometimes, assigning a target to each agent also presents a challenge. The Combined Target-Assignment and Path-Finding (TAPF) problem, a variant of MAPF, requires one to simultaneously assign targets to agents and plan collision-free paths for agents. Several algorithms, including CBM, CBS-TA, and ITA-CBS, optimally solve the TAPF problem, with ITA-CBS being the leading algorithm for minimizing flowtime. However, the only existing boundedsuboptimal algorithm ECBS-TA is derived from CBS-TA rather than ITA-CBS. So, it faces the same issues as CBSTA, such as searching through multiple constraint trees and spending too much time on finding the next-best target assignment. We introduce ITA-ECBS, the first boundedsuboptimal variant of ITA-CBS. Transforming ITA-CBS to its bounded-suboptimal variant is challenging because different constraint tree nodes can have different assignments of targets to agents. ITA-ECBS uses focal search to achieve efficiency and determines target assignments based on a new lower bound matrix. We show that it runs faster than ECBSTA in 87.42% of 54,033 test cases. 

## **Introduction** 

The Multi-Agent Path Finding (MAPF) problem requires planning collision-free paths for multiple agents from their respective start locations to pre-assigned target locations in a known environment while minimizing a given cost function. Many algorithms have been developed to solve this problem optimally, such as Conflict-Based Search (CBS) (Sharon et al. 2015), _M[∗]_ (Wagner and Choset 2011), and Improved CBS (ICBS) (Boyarski et al. 2015). Solving the MAPF problem optimally is known to be NP-hard (Yu and LaValle 2013), so optimal MAPF solvers face challenges in scalability and efficiency. In contrast, suboptimal MAPF solvers, such as Prioritized Planning (PP) (Erdmann and LozanoPerez 1987; Silver 2005), PBS (Ma et al. 2019) and their variants (Chan et al. 2023; Li et al. 2022), exhibit better scalability and efficiency. However, these algorithms lack theoretical guarantees for the quality of their solutions for a given cost function. Bounded-suboptimal MAPF solvers 

Copyright © 2024, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

trade off between efficiency and solution quality. Enhanced CBS (ECBS) (Barer et al. 2014), EECBS (Li, Ruml, and Koenig 2021), and LaCAM (Okumura 2023) guarantee to find collision-free solutions whose costs are at most a userdefined suboptimality factor away from the optimal cost. 

Sometimes, assigning a target to each agent also presents a challenge. This paper explores a variant of the MAPF problem, the Combined Target-Assignment and Path-Finding (TAPF) problem (Ma and Koenig 2016; H¨onig et al. 2018). Inspired by warehouse automation, where robots deliver shelves to packing stations and can initially select which shelf to retrieve (Wurman, D’Andrea, and Mountz 2008), TAPF assigns each agent a target (location) from a set of possible targets. Subsequently, it finds collision-free paths for all agents to minimize a given cost function. TAPF is a more general problem and becomes MAPF if the size of the target set is restricted to one per agent. So, TAPF inherits the NP-hard complexity of MAPF. 

Several algorithms have been proposed to solve the TAPF problem optimally, including CBM (Ma and Koenig 2016), CBS-TA (H¨onig et al. 2018), and ITA-CBS (Tang et al. 2023), with ITA-CBS being the state-of-the-art optimal algorithm for flowtime (i.e., the sum of all path costs). However, they all face scalability issues as optimal TAPF solvers. To the best of our knowledge, ECBS-TA (H¨onig et al. 2018) is the only existing bounded-suboptimal TAPF solver. It directly applies the ECBS algorithm to CBS-TA and can find collision-free (valid) solutions more quickly than CBS-TA. However, since ECBS-TA is based on CBS-TA, ECBS-TA encounters efficiency problems due to the same two issues as CBS-TA: (1) ECBS-TA maintains multiple Constraint Trees (CT) and explores each sequentially, leading to many CT nodes. (2) It involves solving a K-best target assignment problem (Chegireddy and Hamacher 1987), which is often time-consuming. To address these issues, we have developed a bounded-suboptimal algorithm inspired by the single CT structure of ITA-CBS, aiming to avoid the computational bottlenecks of ECBS-TA. 

While ITA-CBS is a CBS-like algorithm with a single CT, developing a bounded-suboptimal algorithm from ITA-CBS is not straightforward since the target assignment (TA) solution, an arrangement that specifies a target for each agent, varies at each CT node. Simply applying ECBS to ITA-CBS can lead to the returned valid solution not being bounded by 

a suboptimal factor. By incorporating an additional Lower Bound (LB) matrix and deriving the TA solution from it, we develop Incremental Target Assignment with Enhanced CBS (ITA-ECBS), a bounded-suboptimal variant of ITACBS with flowtime. It can avoid producing unbounded valid solutions, a risk present when directly applying ECBS to ITA-CBS. Furthermore, it uses the shortest path costs as LB values, thereby accelerating path searching algorithm. Our experimental results show that ITA-ECBS runs faster than the baseline algorithm ECBS-TA in 87.42% of 54,033 test cases with 8 different suboptimality factors. 

## **Problem Definition** 

The Combined Target-Assignment and PathFinding (TAPF) problem is defined as follows: Let _I_ = _{_ 1 _,_ 2 _, · · · , N }_ denote a set of _N_ agents. _G_ = ( _V, E_ ) represents an undirected graph, where each vertex _v ∈ V_ represents a possible location of an agent in the workspace, and each edge _e ∈ E_ is a unit-cost edge between two vertices that moves an agent from one vertex to the other. Self-loop edges are allowed, which represent “wait-inplace” actions. Each agent _i ∈ I_ has a start location _si ∈ V_ . Let _G_ = _{g_ 1 _, g_ 2 _, · · · , gM } ⊆ V_ denote a set of _M_ targets ( _M ≥ N_ ). Let _A_ denote a binary _N × M target matrix_ , where each entry _A_ [ _i_ ][ _j_ ] (the _i_ -th row and _j_ -th column in _A_ ) is one if agent _i_ is eligible to be assigned to target _gj_ and zero otherwise. We refer to the set of targets _{gj ∈G|A_ [ _i_ ][ _j_ ] = 1 _}_ as the _target set_ for agent _i_ . Our task is to assign each agent _i_ a target _gj_ from its target set and plan corresponding collision-free paths for all agents. We cannot assign an agent without specifying a target. 

Each action of agents, either waiting in place or moving to an adjacent vertex, takes one time unit. Let _vt[i][∈][V]_[be the] location of agent _i_ at timestep _t_ . Let _πi_ = [ _v_ 0 _[i][, v]_ 1 _[i][, ..., v] T[i][i]_[]] denote a path of agent _i_ from its start location _v_ 0 _[i]_[to its target] _v[i] T[i]_[. We assume that agents rest at their targets after complet-] ing their paths, i.e., _vt[i]_[=] _[ v] T[i][i][,][ ∀][t > T][ i]_[. The cost of agent] _[ i]_[’s] path is _T[i]_ . We refer to the path with the minimum cost as the shortest path. We consider two types of agent-agent collisions. The first type is a _vertex collision_ , where two agents _i_ and _j_ occupy the same vertex at the same timestep. The second type is an _edge collision_ , where two agents move in opposite directions along the same edge. We use ( _i, j, t_ ) to denote a vertex collision between agents _i_ and _j_ at timestep _t_ or a edge collision between agents _i_ and _j_ at timestep _t_ to _t_ +1. The requirement of being collision-free implies the targets assigned to the agents must be distinct from each other. 

The objective of the TAPF problem is to find a set of paths _{πi|i ∈ I}_ for all agents such that, for each agent _i_ : 

1. Agent _i_ starts from its start location (i.e., _v[[i]]_ 

   - 0 _[[i]]_[=] _[ s][i]_[);] 

2. Agent _i_ stops at a target _gj_ in its target set (i.e., _vt[i]_[=] _gj, ∀t ≥ T[i]_ and _A_ [ _i_ ][ _j_ ] = 1); 

3. Every pair of adjacent vertices on path _πi_ is connected by an edge (i.e., ( _vt[i][, v] t[i]_ +1[)] _[ ∈][E,][ ∀]_[0] _[ ≤][t][ ≤][T][ i]_[); and] 

4. _{πi|i ∈ I}_ is collision-free and minimize the _flowtime_ � _Ni_ =1 _[T][ i]_[.] 

## **Related Work** 

## **Focal Search** 

Focal search (Pearl and Kim 1982; Cohen et al. 2018) is bounded-suboptimal search. Given a user-defined suboptimality factor _w ≥_ 1, it is guaranteed to find a solution with a cost at most _w · c[opt]_ , where _c[opt]_ is the cost of an optimal solution. Focal search has two queues: OPEN and FOCAL. OPEN stores all candidates that need to be searched and sort each candidate _n_ by _f_ ( _n_ ) = _g_ ( _n_ ) + _h_ ( _n_ ), where _g_ ( _n_ ) and _h_ ( _n_ ) are the cost and an admissible heuristic value of candidate _n_ , respectively, which are identical to the _g_ and _h_ values in _A[∗]_ search. FOCAL includes all candidates _n_ satisfying _f_ ( _n_ ) _≤ w · ffront_ , where _ffront_ is the minimum _f_ value in OPEN. FOCAL sorts candidates by another heuristic function _d_ ( _n_ ) which could be any function defined by users.[1] Focal search searches candidates in order of FOCAL—the FOCAL aids in quickly identifying a solution through its heuristic function. When we find a solution with cost _c[val]_ , we call current _ffront_ as this solution’s lower bound (LB) because of _ffront ≤ c[opt]_ and _ffront ≤ c[val] ≤ wffront_ . Therefore, focal search outputs two key pieces of information: an LB value _c[g]_ and a solution with cost _c_ . If there is no solution, we set both _c[g]_ and _c_ to _∞_ . 

## **Multi-Agent Path Finding (MAPF)** 

MAPF has a long history (Silver 2005), and many algorithms have been developed to solve it or its variants. The problem is to find collision-free paths for multiple agents from their start locations to pre-assigned targets while minimizing a given cost function. Decoupled algorithms (Silver 2005; Luna and Bekris 2011; Wang and Botea 2008) independently plan a path for each agent and then combine all paths to one solution. Coupled algorithms (Standley 2010; Standley and Korf 2011) plan for all agents together. There also exist dynamically-coupled algorithms (Sharon et al. 2015; Wagner and Choset 2015) that independently plan each agent and re-plan multiple agents together when needed to resolve their collisions. Among them, ConflictBased Search (CBS) (Sharon et al. 2015) is a popular centralized optimal MAPF algorithm. Some boundedsuboptimal algorithms are based on it, such as ECBS (Barer et al. 2014) and EECBS (Li, Ruml, and Koenig 2021). 

**CBS** Conflict-Based Search (CBS) is an optimal two-level search algorithm. Its low level plans the shortest paths for agents from their start locations to targets, while its high level searches a binary Constraint Tree (CT). Each CT node _H_ = ( _c,_ Ω _, π_ ) includes a constraint set Ω, a solution _π_ , which is a set of shortest paths satisfying Ω for all agents, and a cost _c_ , which is the flowtime of _π_ . When a solution _π_ or a path does not include any agent actions or positions that are restricted by a Ω, we say this solution or path satisfies the Ω. As long as _π_ satisfies Ω, _pi_ could have collisions. We call a CT node solution _π_ a valid solution when 

1Since OPEN and FOCAL are for sorting purposes and FOCAL is a subset of OPEN, in implementation, we store candidate pointers in them. If one candidate appears in both queues, only one copy exists and two pointers point to this candidate copy. 

it is collision-free. When expanding a node _H_ , CBS selects the first collision in _H.π_ , even when multiple collisions occur in _H.π_ , and formulates two constraints, each prohibiting one agent from occupying the colliding location or executing its intended original action at the colliding timestep. We have two types of constraints: vertex constraint ( _i, v, t_ ) that prohibits agent _i_ from occupying vertex _v_ at timestep _t_ and edge constraint ( _i, u, v, t_ ) that prohibits agent _i_ from going from vertex _u_ to vertex _v_ at timestep _t_ . Then CBS generates two successor nodes identical to _H_ and adds each of the two constraints to the constraint set of the two respective successor nodes. After adding a new constraint, each node should re-plan the path that does not satisfy this constraint. By maintaining a priority queue OPEN based on each node’s cost, CBS repeats this process until expanding a node that has no collisions, in which case, its solution is an optimal valid solution. CBS is optimal for the flowtime minimization (Sharon et al. 2015). 

**ECBS** Enhanced CBS (ECBS) (Barer et al. 2014) is based on CBS and uses focal search with the same suboptimality factor _w_ in both two-level searches. In its low-level search, the focal search returns an LB value _c[g] i_[and][a][valid][path] _[π][i]_ with cost _ci_ for agent _i_ from its start location to target. The path and value satisfy: _c[g] i[≤][c][opt] i ≤ ci ≤ w · c[g] i_[, where] _[ c][opt] i_ is the cost of agent _i_ ’s shortest path satisfying Ω, and _w_ is the suboptimality factor. In its high-level search, comparing to CBS, each CT node _H_ = ( _c,_ Ω _, π, L, cL_ ) in ECBS has an additional cost array _L_ , which stores all LB values _c[g] i_[for] all paths in _π_ , and cost _cL_ which is the sum of _c[g] i_[in] _[ L]_[. The] high-level search of ECBS maintains two priority queues: FOCAL and OPEN. OPEN stores all CT nodes sorted in ascending order of _cL_ . Let the front CT node in OPEN be _Hfront_ , ECBS adds all CT nodes _H_ in OPEN that satisfy _H.c ≤ w · Hfront.cL_ into FOCAL. FOCAL is sorted in ascending order of a user-defined heuristic function _d_ ( _H_ ). ECBS guarantees that its returned solution _H[sol] .π_ satisfies _H[sol] .c ≤ w · c[opt]_ , where _c[opt]_ is the cost of the optimal valid solution. 

## **Combined Target-Assignment and Path-Finding (TAPF)** 

The Combined Target-Assignment and Path-Finding (TAPF) problem is a combination of the MAPF problem and the target-assignment problem. While MAPF has a pre-defined target for each agent, TAPF involves simultaneously assigning targets to agents and finding collision-free paths for them. There are several TAPF algorithms such as CBM (Ma and Koenig 2016), CBS-TA (H¨onig et al. 2018), ECBS-TA (H¨onig et al. 2018), and ITA-CBS (Tang et al. 2023). CBM combines CBS with maxflow algorithms to optimally minimize the makespan max _i∈I {T[i] }_ . However, CBM works only for makespan, while other algorithms also work for flowtime. CBS-TA tries different Target Assignments (TA) for agents and then seeks the optimal valid solution across multiple CTs, one CT for each TA (forming a forest). Targets are assigned to agents by Hungarian algorithm, that minimizes the sum of costs in a given cost matrix. ECBS-TA, a bounded-suboptimal 

version of CBS-TA, incorporates focal search (Pearl and Kim 1982; Barer et al. 2014). Both CBS-TA and ECBS-TA require a substantial amount of time to determine the next-best TA as they lazily traverse each CT. In contrast to CBS-TA and ECBS-TA, ITA-CBS searches for optimal valid solutions within a single CT and uses the dynamic Hungarian algorithm (Mills-Tettey, Stentz, and Dias 2007). However, scalability remains a challenge for ITA-CBS due to its optimality. We propose ITA-ECBS to overcome this issue. 

**CBS-TA and ECBS-TA** CBS-TA (H¨onig et al. 2018), inspiring many extensions (Ren, Rathinam, and Choset 2023; Zhong et al. 2022; Chen et al. 2021; Okumura and D´efago 2023), operates on the following principle: a fixed TA transforms a TAPF instance to a MAPF instance, and CBS can solve each MAPF instance with one CT. CBS-TA efficiently explores all nodes of the different CTs (CT forest) by enumerating every TA solution. In CBS-TA, TA solutions are derived from an _N × M_ cost matrix _Mc_ , which records the path costs from agents’ start locations to targets, without considering any constraints. Each CT node _H_ = ( _c,_ Ω _, π, πta, r_ ) of CBS-TA has two extra fields compared to a node of CBS: a TA solution _πta_ that assigns each agent a unique target and a root flag _r_ signifying if _H_ is the root of a CT. CBS-TA maintains a priority queue OPEN to store nodes from the CT forest and lazily generates roots of new CTs with different TA solutions. CBS-TA first generates one CT root with the optimal TA which has the minimum cost based on _Mc_ . It does not need to generate a new CT until all CT nodes in the queue are larger than the cost of a new CT root because the cost of a CT root is no larger than the cost of any child node in the CT. Consequently, it generates a new root with the next-best TA solution only when the CT root in OPEN has been expanded. Based on the K- best task-assignment algorithm (Chegireddy and Hamacher 1987) and the Successive Shortest Path (SSP) algorithm (Engquist 1982), CBS-TA finds the next-best TA solution with complexity _O_ ( _N_[3] _M_ ). Using the ECBS algorithm to search each CT transforms CBS-TA to the bounded-suboptimal algorithm ECBS-TA (H¨onig et al. 2018). 

**ITA-CBS** Since many CT nodes in different CTs of CBSTA have identical constraint sets, which leads CBS-TA to repeat searches, ITA-CBS is a CBS-like algorithm that uses only one CT to search for the optimal valid solution. Each CT node _H_ = ( _c,_ Ω _, π, πta, Mc_ ) in ITA-CBS has two extra fields compared to a node of CBS: a TA solution _πta_ and an _N × M_ cost matrix _Mc_ . Each entry _Mc_ [ _i_ ][ _j_ ] is the minimum cost of paths from _si_ to _gj_ satisfying Ω. _Mc_ [ _i_ ][ _j_ ] = _∞_ if _A_ [ _i_ ][ _j_ ] = 0 (i.e., target _gj_ is not included in the target set of agent _i_ ) or there is no path satisfying Ω. In implementation, ITA-CBS stores costs in _Mc_ together with their corresponding paths, so that it can construct _π_ directly from _Mc_ after obtaining _πta_ . In this paper, when we mention _Mc_ , it could represent costs or the corresponding paths depending on context. _πta_ is the optimal TA solution of _Mc_ , _π_ is the set of paths selected from _Mc_ based on _πta_ , and _c_ is the flowtime of _π_ . 

During node expansion, ITA-CBS retrieves a node from 


![](1_survey/papers/md/Tang2024ITAECBS_figs/Tang2024ITAECBS.pdf-0004-00.png)


**----- Start of picture text -----**<br>
H! !! $!<br>A B C A B C<br>X 1 2 X 2 3<br>Y 4 3 3 Y 4 6 6<br>Real "! = 4 " : 7<br>"!: 6<br>d(H"): 1<br>Constraint of X Constraint of Y<br>H" H#<br>!! $! !! $!<br>A B C A B C A B C A B C<br>X 2 3 X 4 5 X 1 2 X 2 3<br>Y 4 3 3 Y 4 6 6 Y 4 3 4 Y 4 6 4<br>Real "! = 5 " : 9 Real "! = 4 " : 6<br>"!: 7 "!: 5<br>d(H#): 0 d(H$): 2<br>**----- End of picture text -----**<br>


Figure 1: This figure shows the unbounded problem if we directly use ECBS in ITA-CBS. We have 2 agents _{X, Y }_ and target sets _X_ : _{A, B}_ and _Y_ : _{A, B, C}_ . Red numbers represent the matrix’s optimal TA solution. Orange cells represent the row update since the new constraint is related to only one agent. The suboptimality factor _w_ is 2. ITA-CBS utilizes _Mc_ to obtain the optimal TA solution. Here, _πta_ is the TA solution of _Mc_ . _c_ represents the flowtime based on _πta_ . _cL_ is the sum of LB values selected from _ML_ based on _πta_ . Real _cL_ is the cost of the optimal TA solution of _ML_ . _d_ ( _H_ ) represents the user-defined heuristic function used in FOCAL. 

OPEN and checks if its _π_ is collision-free. If so, this _π_ is an optimal valid solution, and ITA-CBS terminates. Otherwise, like CBS, ITA-CBS generates two child CT nodes and adds new constraints to their Ωs. When creating a CT node _H_ , ITA-CBS first re-plans all paths in _Mc_ that do not satisfy _H._ Ω. Then, it obtains a new _H.πta_ from _H.Mc_ . Based on _H.πta_ , ITA-CBS obtains a new _H.π_ from _H.Mc_ and then inserts _H_ into OPEN. In summary, the order of modification of the variables is Ω _→ Mc → πta → π →_ children’s Ω. Since each CT node has only one new constraint compared to its parent and at most one row in _Mc_ is changed, ITA-CBS uses dynamic Hungarian algorithm (Mills-Tettey, Stentz, and Dias 2007) with complexity _O_ ( _NM_ ) to obtain a new TA, which largely reduces the runtime of TA compared to using Hungarian algorithm. ITA-CBS is faster than CBSTA in experiments. However, its scalability is still limited since it is an optimal algorithm for TAPF. 

## **ITA-ECBS** 

Adapting the optimal ITA-CBS algorithm to its boundedsuboptimal counterpart is challenging since the optimal TA often changes from CT node to CT node. In ITA-CBS, we derive _πta_ from _Mc_ and a solution _π_ based on _πta_ . Directly applying focal search during low-level path search in ITACBS can yield two _N × M_ matrices for each CT node _H_ : an LB matrix _ML_ , which stores all LB values _c[g]_ returned from focal search, and a cost matrix _Mc_ satisfying _ML_ [ _i_ ][ _j_ ] _≤ Mc_ [ _i_ ][ _j_ ] _≤ w · ML_ [ _i_ ][ _j_ ] _, i_ = 1 _, ..., N, j_ = 1 _, ..., M_ . We can apply a target assignment algorithm to either one of these two matrices: _πta_ obtained from _ML_ provides a lower bound 

Algorithm 1: ITA-ECBS-v0 and ITA-ECBS 

**Input** : Graph _G_ , start locations _{si}_ , target locations _{gi}_ , target matrix _A_ , suboptimality factor _w_ , algorithm type ALGO ~~T~~ YPE **Output** : A valid TAPF solution within the suboptimality factor _w_ 1: _H_ 0 = new CTnode() 2: _H_ 0 _._ Ω = _∅_ 3: **for each** ( _i, j_ ) _∈{_ 1 _, · · · , N } × {_ 1 _, · · · , M }_ **do** 4: _H_ 0 _.Mc_ [ _i_ ][ _j_ ] = _H_ 0 _.ML_ [ _i_ ][ _j_ ] = _∞_ 5: **if** _A_ [ _i_ ][ _j_ ] = 1 **then** 6: _H_ 0 _.ML_ [ _i_ ][ _j_ ], _H_ 0 _.Mc_ [ _i_ ][ _j_ ]=lowLevelSearch( _G, si, gj, H_ 0 _, w_ ) 7: _H_ 0 _.πta_ = optimalTargetAssignment( _H_ 0 _.ML_ ) 8: _H_ 0 _.c, H_ 0 _.π_ = getPlan( _H_ 0 _.πta_ , _H_ 0 _.Mc_ ) 9: _H_ 0 _.cL_ = getLowerBound( _H_ 0 _.πta_ , _H_ 0 _.ML_ ) 10: FOCAL = OPEN = PriorityQueue() 11: Calculate _d_ ( _H_ 0) and insert _H_ 0 into OPEN 12: **while** OPEN not empty **do** 13: _Hfront_ = OPEN.front() 14: FOCAL = FOCAL _∪{_ H _∈_ OPEN _| H.c ≤ w·Hfront.cL}_ 15: _Hcur_ = FOCAL.front(); FOCAL.pop() 16: Delete _Hcur_ from OPEN 17: **if** _Hcur.π_ has no collision **then** 18: **return** _Hcur.π_ 19: ( _i, j, t_ ) = getFirstCollision( _Hcur.π_ ) 20: **for each** agent _k_ in ( _i, j_ ) **do** 21: _Q_ = a copy of _Hcur_ 22: **if** ( _i, j, t_ ) is a vertex collision **then** 23: _Q._ Ω = _Q._ Ω _∪_ ( _k_ , _vt[k]_[,] _[ t]_[) // vertex constraint] 24: **else** 25: _Q._ Ω = _Q._ Ω _∪_ ( _k_ , _vt[k] −_ 1[,] _[ v] t[k]_[,] _[ t]_[) // edge constraint] 26: **for each** _x_ with _A_ [ _k_ ][ _x_ ] = 1 **do** 27: _Q.ML_ [ _k_ ][ _x_ ], _Q.Mc_ [ _k_ ][ _x_ ]=lowLevelSearch( _G, sk, gx, Q, w_ ) 28: _Q.πta_ = optimalTargetAssignment( _Q.ML_ ) 29: _Q.c, Q.π_ = getPlan( _Q.πta_ , _Q.Mc_ ) 30: _Q.cL_ = getLowerBound( _Q.πta_ , _Q.ML_ ) 31: **if** Q.c _< ∞_ **then** 32: Calculate _d_ ( _Q_ ) and insert _Q_ into OPEN 

33: **return** No valid solution 34: **function** lowLevelSearch( _G_ , _sk_ , _gx_ , _Q, w_ ) 35: **if** ALGO ~~T~~ YPE = ITA-ECBS-v0 **then** 36: _c[g]_ , _c_ = focalSearch( _G_ , _sk_ , _gx_ , _Q._ Ω, _Q.Mc_ , _w_ ) 37: **if** ALGO ~~T~~ YPE = ITA-ECBS **then** 38: _c[g]_ = shortestPathSearch( _G_ , _sk_ , _gx_ , _Q._ Ω) 39: _c_ = searchWithLB( _G_ , _sk_ , _gx_ , _Q._ Ω, _Q.Mc_ , _w_ , _c[g]_ ) 40: **return** _c[g]_ , _c_ 

on the cost of all TAPF solutions that meet _H._ Ω, whereas _πta_ obtained from _Mc_ has the minimum flowtime among all possible TA solutions in _Mc_ . These two TA can differ. If we simply apply ECBS in ITA-CBS to make it boundedsuboptimal version, the returned valid solution _π_ , derived from _πta_ of _Mc_ , may not be bounded-suboptimal. 

Figure 1 provides an example with suboptimality factor _w_ = 2. _H_ 1 is a parent CT node with _πta_ = _{X → B, Y → A}_ based on _H_ 1 _.Mc_ . The sum of LB values selected from _H_ 1 _.ML_ based on _πta_ is _cL_ = 6, whereas the minimum LB sum _Real cL_ is 4 in _ML_ . _H_ 1 generates two child nodes _{H_ 2 _, H_ 3 _}_ , assuming both child node solutions _π_ are collision-free. Since _H_ 2 _.c ≤ w ·_ min( _H_ 2 _.cL, H_ 3 _.cL_ ), we add _H_ 2 to FOCAL and the same applies to _H_ 3. Assume _H_ 2 has a lower heuristic value _d_ ( _H_ 2) and should be eval- 


![](1_survey/papers/md/Tang2024ITAECBS_figs/Tang2024ITAECBS.pdf-0005-00.png)


**----- Start of picture text -----**<br>
10 [1] 10 [1] 10 [1]<br>10 [0] 10 [0] 10 [0]<br>10 1 10 1 10 1<br>10 2 1x 10 2 1x 10 2 1x<br>5x 5x 5x<br>100x 100x 100x<br>10 2 10 1 10 [0] 10 [1] 10 2 10 1 10 [0] 10 [1] 10 2 10 1 10 [0] 10 [1]<br>w=1.0, ITA-ECBS runtime (s) w=1.02, ITA-ECBS runtime (s) w=1.2, ITA-ECBS runtime (s)<br>ECBS-TA runtime (s)<br>**----- End of picture text -----**<br>


Figure 2: Each subfigure contains 9,600 (8 _·_ 15 _·_ 4 _·_ 20) distinct test cases. We have chosen three suboptimality factors _w {_ 1.00, 1.02, 1.20 _}_ to find optimal and bounded-suboptimal valid solutions with small and large suboptimality factors. 


![](1_survey/papers/md/Tang2024ITAECBS_figs/Tang2024ITAECBS.pdf-0005-02.png)


**----- Start of picture text -----**<br>
H! Ω"<br>!! !' 1 " ⋅$%. &&<br>'%&, "! ', ", *(+") FOCAL :  H# H(<br>H" 2 H# 4<br>Ω# Ω$ OPEN : H( H" H# H$<br>!! !' !! !'<br>'%&, "! ', ", *(+") '%&, "! ', ", *(+$)<br>3<br>H!<br>**----- End of picture text -----**<br>


Figure 3: ITA-ECBS overview: There are two CT nodes _{H_ 0 _, H_ 1 _}_ in OPEN. (1) Although _H_ 0 has a lower _cL_ value and precedes _H_ 1 in OPEN, the heuristic function _d_ ( _H_ ) may result in _H_ 1 being selected for expansion. (2) We verify whether _H_ 1 _.π_ is collision-free. If not, we generate two child CT nodes with new constraint sets Ω2 and Ω3 and then use focal search to obtain new _ML_ and _Mc_ for each node. A new _ML_ leads to a new _πta_ and _cL_ . The updated _πta_ and _Mc_ give us a bounded-suboptimal solution _π_ and the cost _c_ . We then calculate _d_ ( _H_ ). (3) We insert these two nodes into OPEN, indicated by the red values. (4) All CT nodes in OPEN with cost _c ≤ w · H_ 0 _.cL_ are added to FOCAL. _H_ 2 could be positioned ahead of _H_ 0 in FOCAL by the heuristic function _d_ . 

uated before _H_ 3, leading to _H_ 2 _.π_ becoming the returned valid solution. The flowtime of _H_ 2 _.π_ is 9. However, based on _Real cL_ = 4 in _H_ 3, it might be possible to find a child node of _H_ 3 that has a valid solution with a flowtime _c[opt]_ equal to _Real cL_ = 4. In this case, _H_ 2 _.c ≥ w · c[opt]_ . This suggests that _H_ 2’s solution may not be bounded by _w_ , which we call the unbounded problem. 

Focal search thus cannot turn ITA-CBS into a boundedsuboptimal algorithm. We need to obtain _πta_ from _ML_ rather than _Mc_ . As shown in Figure 3 and Algorithm 1, we propose two bounded-suboptimal TAPF algorithms: ITAECBS-v0 and its enhanced version ITA-ECBS. We first in- 

troduce ITA-ECBS-v0. Each CT node of ITA-ECBS-v0 is represented as _H_ = ( _c,_ Ω _, π, πta, Mc, ML, cL_ ). It has two extra fields compared to a node of ITA-CBS: an LB matrix _ML_ and cost _cL_ which is the sum of LB values selected from _ML_ based on _πta_ . The two matrices _ML_ and _Mc_ can be generated concurrently because focal search returns an LB value and a path satisfying Ω in one search. Each entry _ML_ [ _i_ ][ _j_ ] represents the LB value of paths from _si_ to _gj_ , and _Mc_ [ _i_ ][ _j_ ] denotes the actual path and _Mc_ [ _i_ ][ _j_ ] _≤ w · ML_ [ _i_ ][ _j_ ]. If focal search has no solution for a path satisfying Ω or _A_ [ _i_ ][ _j_ ] = 0, we set both _ML_ [ _i_ ][ _j_ ] and _Mc_ [ _i_ ][ _j_ ] to _∞_ . A key distinction of ITA-ECBS-v0 from ITA-CBS is that _πta_ is the optimal TA solution obtained from _ML_ rather than _Mc_ . This change helps to avoid the unbounded problem. _π_ is the set of paths selected from _Mc_ based on _πta_ . _c_ is the flowtime of _π_ . 

Algorithm 1 shows the pseudocode of ITA-ECBS-v0. It starts by generating the root node _H_ 0, including creating an empty constraint set _H_ 0 _._ Ω and the corresponding matrices _H_ 0 _.Mc_ and _H_ 0 _.ML_ using focal search. Subsequently, a target assignment algorithm, such as the dynamic Hungarian algorithm, determines _H_ 0 _.πta_ based on _H_ 0 _.ML_ . Then _H_ 0 _.π_ is obtained from _H_ 0 _.Mc_ based on _H_ 0 _.πta_ (Lines 1-9). In the high-level search, ITA-ECBS-v0, like ECBS, maintains two priority queues: OPEN and FOCAL. OPEN has all CT nodes sorted by their _cL_ . FOCAL contains only those CT nodes _H_ with _H.c ≤ w · Hfront.cL_ , where _Hfront_ is the OPEN front node. FOCAL is sorted by a given heuristic function _d_ ( _H_ ). ITA-ECBS-v0 first gets _Hfront_ from OPEN in each iteration. Based on _Hfront.cL_ , it adds all eligible CT nodes in OPEN to FOCAL. Then, it chooses the front node _Hcur_ in FOCAL and removes it from OPEN (Lines 10-16). 

ITA-ECBS-v0 checks if _Hcur.π_ is collision-free. If so, this _π_ is a bounded-suboptimal valid solution (Lines 17-18). Otherwise, like ECBS, ITA-ECBS-v0 utilizes the first identified collision to generate two constraints. It then creates two child CT nodes identical to _Hcur_ and adds one constraint to Ω of the first child CT node and the other constraint to Ω of the second child CT node (Lines 19-25). For each child CT node _Q_ with a constraint for agent _k_ added, all 


![](1_survey/papers/md/Tang2024ITAECBS_figs/Tang2024ITAECBS.pdf-0006-00.png)


Figure 4: The success rates of different algorithms as a function of the suboptimality factor. 


![](1_survey/papers/md/Tang2024ITAECBS_figs/Tang2024ITAECBS.pdf-0006-02.png)


**----- Start of picture text -----**<br>
w=1.0 ECBS-TA w=1.02 ECBS-TA w=1.2 ECBS-TA<br>w=1.0 ITA-ECBS-v0 w=1.02 ITA-ECBS-v0 w=1.2 ITA-ECBS-v0<br>w=1.0 ITA-ECBS w=1.02 ITA-ECBS w=1.2 ITA-ECBS<br>random-32-32-10 den312d empty-32-32 maze-32-32-2<br>1.00<br>0.75<br>0.50<br>0.25<br>0.00<br>10 40 70 100 130 10 40 70 100 130 10 40 70 100 130 10 40 70 100 130<br>room-64-64-8 warehouse-10-20-10-2-1 orz900d Boston<br>1.00<br>0.75<br>0.50<br>0.25<br>0.00<br>10 40 70 100 130 10 40 70 100 130 10 40 70 100 130 10 40 70 100 130<br>Number of agents Number of agents Number of agents Number of agents<br>Success rate<br>Success rate<br>**----- End of picture text -----**<br>


Figure 5: The success rates of three algorithms with three selected suboptimality factors as a function of the number of agents. 

LB values in _Q.ML_ and all paths in _Q.Mc_ related to agent _k_ have to be replanned subject to the new constraint set _Q._ Ω (Lines 26-27, 36). Since _Q.ML_ changes, the TA _Qπta_ , solution _Q.π_ , and costs _Q.c_ and _Q.cL_ have to be updated as well (Lines 28-30). Because focal search returns _∞_ if no solution exists, _Q.c_ = _∞_ means that there is no _π_ satisfying _Q._ Ω and ITA-ECBS-v0 can ignore this CT node. Otherwise, it insert _Q_ into OPEN (Lines 31-32). 

Usually, bounded-suboptimal algorithms aim to find a bounded-suboptimal valid solution swiftly. In the low-level search, we could have more candidates in FOCAL by obtaining larger LB values. Since all candidates in FOCAL have a bounded-suboptimal solution, more candidates in FOCAL increases our chances of rapidly discovering a valid solu- 

tion if _d_ ( _n_ ) is properly designed. For an LB value _c[g]_ , we have _c[g] ≤ c[opt]_ where _c[opt]_ is the shortest path cost. Rather than obtaining an LB value _c[g]_ from focal search, we can directly use _c[opt]_ as the LB value from a shortest path algorithm such as _A[∗]_ . Using _c[opt]_ as the LB value can give us more freedom to get a path leading to a valid _π_ . We use a new function named _searchWithLB_ to identify paths with the lowest _d_ ( _n_ ) values, using an given LB value _c[v]_ as a guideline. _searchWithLB_ is similar to focal search but only has FOCAL contains all candidates with costs _w · c[v]_ . If a candidate cost is larger than _w · c[v]_ , it cannot contain a boundedsuboptimal solution and we can ignore it. 

The final version of ITA-ECBS is shown in Algorithm 1. The only difference between ITA-ECBS-v0 and ITA-CBS 

|**Average of Success Rate**|**Average of Success Rate**|**Number of Agents**|**Number of Agents**|**Number of Agents**|**Number of Agents**|**Number of Agents**|**Percentage of Shared Targets**|**Percentage of Shared Targets**|**Percentage of Shared Targets**|**Percentage of Shared Targets**|
|---|---|---|---|---|---|---|---|---|---|---|
|_w_|**algorithms**|**30**|**60**|**90**|**120**|**150**|**0%**|**30%**|**60%**|**100%**|
|**1.01**|ECBS<br>~~T~~A<br>ITA-ECBS-v0<br>ITA-ECBS|0.854<br>0.864<br>**0.875**|0.582<br>0.589<br>**0.639**|0.396<br>0.379<br>**0.453**|0.240<br>0.190<br>**0.267**|0.150<br>0.150<br>**0.223**|0.537<br>0.545<br>**0.578**|0.498<br>0.498<br>**0.562**|0.515<br>0.487<br>**0.564**|0.466<br>0.427<br>**0.480**|
|**1.03**|ECBS<br>~~T~~A<br>ITA-ECBS-v0<br>ITA-ECBS|0.873<br>0.878<br>**0.890**|0.782<br>0.762<br>**0.820**|0.640<br>0.603<br>**0.707**|0.406<br>0.376<br>**0.515**|0.200<br>0.215<br>**0.387**|0.698<br>0.701<br>**0.76**|0.610<br>0.635<br>**0.741**|0.625<br>0.618<br>**0.719**|0.600<br>0.528<br>**0.612**|
|**1.04**|ECBS<br>~~T~~A<br>ITA-ECBS-v0<br>ITA-ECBS|0.889<br>0.893<br>**0.906**|0.817<br>0.792<br>**0.843**|0.701<br>0.657<br>**0.770**|0.482<br>0.471<br>**0.607**|0.279<br>0.315<br>**0.490**|0.743<br>0.747<br>**0.795**|0.647<br>0.678<br>**0.787**|0.673<br>0.672<br>**0.777**|0.660<br>0.582<br>**0.672**|
|**1.05**|ECBS<br>~~T~~A<br>ITA-ECBS-v0<br>ITA-ECBS|0.898<br>0.904<br>**0.932**|0.837<br>0.810<br>**0.859**|0.737<br>0.696<br>**0.810**|0.529<br>0.509<br>**0.671**|0.320<br>0.373<br>**0.551**|0.771<br>0.775<br>**0.831**|0.669<br>0.719<br>**0.822**|0.703<br>0.702<br>**0.814**|0.701<br>0.607<br>**0.708**|
|**1.10**|ECBS<br>~~T~~A<br>ITA-ECBS-v0<br>ITA-ECBS|0.959<br>0.964<br>**0.985**|0.868<br>0.848<br>**0.873**|0.85<br>0.804<br>**0.854**|0.692<br>0.684<br>**0.801**|0.485<br>0.571<br>**0.757**|0.871<br>0.868<br>**0.901**|0.752<br>0.842<br>**0.902**|0.787<br>0.806<br>**0.889**|**0.820**<br>0.699<br>0.790|



Table 1: Average success rates across variables not specified in the table. The highest average success rates are shown in bold. Due to space constraints, only five numbers of agents are shown. 

lies in Lines 37-39. We first use shortest path search to determine _c[opt]_ based on Ω. _c[opt]_ is then utilized as _c[v]_ in the _searchWithLB_ function to identify a path with a cost of at most _w · c[opt]_ , thus enabling quicker discovery of a bounded-suboptimal valid solution. As demonstrated in our experimental section, ITA-ECBS is more efficient than ITAECBS-v0 despite requiring twice path searches. 

In code implementation, we use the number of collisions in _H.π_ as the heuristic function _d_ for both the low-level path search and the high-level CT node search. However, this heuristic is more advantageous for the low-level search of ECBS-TA than ITA-ECBS. ECBS-TA updates a single path for one agent and does not need to modify the TA solution of CT nodes, which ensures _d_ ( _n_ ) is accurate when using low-level focal search to find a path. In ITA-ECBS, the accuracy is compromised because changes in the TA can lead to changes in the paths of multiple agents. When calculating the number of collisions for a path in ITA-ECBS, the paths of the other agents are not finalized. For example, we need to re-plan paths for two agents _a_ 1 and _a_ 2 one by one due to a new _πta_ . We want to calculate the number of collisions for the focal search of _a_ 1. However, it is impossible to accurately count collisions between _a_ 1 and _a_ 2 because we do not know _a_ 2’s new path. So we can only use _a_ 2’s old path to count collisions between _a_ 1 and _a_ 2. 

## **Experimental Results** 

We compare the success rate and runtime of ITA-ECBS with ECBS-TA since, to the best of our knowledge, ECBS-TA is the only bounded-suboptimal TAPF algorithm that minimizes flowtime. We implement ITA-ECBS and ECBS-TA in C++, partially based on the existing ITA-CBS implementation.[2] All experiments are conducted on an Ubuntu 20.04.1 

2The ITA-ECBS and ECBS-TA code and test data are available at https://github.com/TachikakaMin/ITA-CBS2. Based on tests, our ECBS-TA implementation runs faster than the original one. 

system with an AMD Ryzen 3990X 64-Core Processor with 2133 MHz 64GB RAM. 

## **Test Settings** 

We test ITA-ECBS and ECBS-TA with the suboptimality factors _w_ = 1 _._ 00 _,_ 1 _._ 01 _,_ 1 _._ 02 _,_ 1 _._ 03 _,_ 1 _._ 04 _,_ 1 _._ 05 _,_ 1 _._ 10, and 1 _._ 20 on 8 maps from the MAPF Benchmark (Stern et al. 2019). These maps are shown in Figure 4 and previously to evaluate ITA-CBS and CBS-TA (Tang et al. 2023): (1) random-32-32-10 (32x32) and empty-32-32 (32x32) are grid maps with and without random obstacles, (2) den312d (65x81) is a grid map from the video game Dragon Age Origins, (3) maze-32-32-2 (32x32) is a maze-like grid map, (4) room-64-64-8 (64x64) is a room-like grid map, (5) warehouse-10-20-10-2-1 (161x63) is a grid map inspired by real-world autonomous warehouses, and (6) orz900d (1491x656) and Boston-0-256 (256x256) are the largest and second largest benchmark maps. 

The number of agents ranges from 10 to 150 in increments of 10. For each map, every agent has a target set of the same size, which is 5, 15, 5, 4, 20, 30, 10, 10 for maps random-3232-10, den312d, empty-32-32, maze-32-32-2, room-64-648, warehouse-10-20-10-2-1, orz900d, Boston-0-256 respectively. Each target set has unique targets and targets shared among all agents. We vary the percentage of shared targets in target sets from 0%, 30%, 60% to 100%. All numbers round down.[3] However, we ensure that each target set al- 

> 3The size of the target set for each map is determined by the number of cells available to be assigned to agents, except large maps orz900d and Boston-0-256. For instance, the empty-32-32 map has 1,024 cells. With a maximum of 150 agents, the target set size is calculated as 1 _,_ 024 _/_ 150 = 6 _._ 82, and we use 5 as the target set size. On large maps, the size of the target set is 10 to prevent ITA-ECBS and ECBS-TA from timing out. Because most of the time on a large map will be occupied by low-level searches, the number of CT nodes that can be searched within 30 seconds is only a few dozen if the size of the target set is larger. 


![](1_survey/papers/md/Tang2024ITAECBS_figs/Tang2024ITAECBS.pdf-0008-00.png)


**----- Start of picture text -----**<br>
task assignment heuristic calculation for CT nodes other<br>low-level search time CT node creation<br>ITA-ECBS<br>ITA-ECBS-v0<br>ECBS-TA<br>0.000 0.005 0.010 0.015 0.020<br>Average Time per CT Node (s)<br>ITA-ECBS<br>ITA-ECBS-v0<br>ECBS-TA<br>0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5<br>Average Total Time (s)<br>**----- End of picture text -----**<br>


Figure 6: Runtime breakdown (seconds) for target assignment (Algorithm 1 Line 28), low-level search (Line 27), heuristic calculation for CT nodes (Line 32), CT node creation (Line 21), which requires copying variables and other tasks. 

ways includes at least one unique target to guarantee agents have enough targets to allocate. 

For each map, number of agents, and percentage of shared targets, we generate 20 test cases with randomly selected start and target locations. An algorithm is considered to have failed for a given test case if it does not find a valid solution within 30 seconds. The success rate is the percentage of the 20 test cases where the algorithm succeeds. 

## **Performance** 

Overall, we have 76,800 test cases. Among these, 48,334 test cases are solved by both ITA-ECBS and ECBS-TA, 5,190 are solved only by ITA-ECBS, 509 are solved only by ECBS-TA, and 22,767 are not solved by either algorithm. Out of the 54,033 test cases solved by at least one algorithm, ITA-ECBS was faster than ECBS-TA in 87.42% of the test cases and 5 times faster in 24.71% of them. Figure 2 showcases their performance for three selected suboptimality factors. As the suboptimality factor increases, ITA-ECBS and ECBS-TA solve more test cases and the success rates of ITA-ECBS are larger than those of ECBS-TA. 

Figure 4 displays the success rates of different algorithms as the suboptimality factor increases. Figure 5 displays the success rates of different algorithms as the number of agents increases for three selected suboptimality factors. The success rates of all algorithms tend to decrease as the number of agents increases, as expected. The success rates of all algorithms increase as the suboptimality factor increases. In orz900d, the success rate of ITA-ECBS-v0 decreases significantly, likely because orz900d is the largest map (1491x656) and the low-level focal search of ITA-ECBS-v0 is slow due to the uninformed heuristic function. Table 1 summarizes the average success rates for various algorithms as a function of their suboptimality factors, numbers of agents, and percentages of shared targets. ITA-ECBS outperforms ECBS-TA in 

most scenarios. 

Figure 6 shows the average runtimes of different components of three algorithms, on those test cases that they solved within the runtime limit across different suboptimality factors. ITA-ECBS-v0 is slower than ECBS-TA in processing each CT node, primarily due to its slower low-level focal search. But it is faster than ECBS-TA because ITA-ECBS-v0 uses a single CT and generates fewer CT nodes. ITA-ECBS improves on ITA-ECBS-v0 by obtaining a larger LB value to increase the number of nodes in FOCAL, which reduces the path search time both per CT node and the average time. Additionally, ITA-ECBS and ITA-ECBS-v0 benefit from using the dynamic Hungarian algorithm, which is considerably faster than the next-best target assignment algorithm used in ECBS-TA, as their task-assignment runtimes show. 

## **Conclusion** 

This work presented a new algorithm, Incremental Target Assignment with Enhanced CBS (ITA-ECBS), designed to solve the TAPF problem with a bounded-suboptimal flowtime. It is the first bounded-suboptimal algorithm derived from ITA-CBS, a leading optimal algorithm for TAPF. By using an LB matrix to derive the TA solution, ITA-ECBS avoids the unbounded problem, a risk present when directly converting the CBS algorithm of ITA-CBS to its boundedsuboptimal version ECBS. Furthermore, ITA-ECBS uses shortest path costs as LB values, which accelerate the focal search for pathfinding. Although ITA-ECBS could be improved further, such as by designing a good heuristic function for its CT nodes despite different CT nodes having different TA solutions, our experimental results demonstrate that ITA-ECBS is significantly faster than the prior best bounded-suboptimal TAPF algorithm ECBS-TA. 

## **Acknowledgments** 

Our research was supported by the National Science Foundation (NSF) under grant numbers 1817189, 1837779, 1935712, 2121028, 2112533, and 2321786 as well as gifts from Amazon Robotics and the CMU Manufacturing Futures Institute, made possible by the Richard King Mellon Foundation. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the sponsoring organizations, agencies, or the U.S. government. 

## **References** 

Barer, M.; Sharon, G.; Stern, R.; and Felner, A. 2014. Suboptimal variants of the conflict-based search algorithm for the multi-agent pathfinding problem. In _Proceedings of the International Symposium on Combinatorial Search (SoCS)_ , volume 5, 19–27. 

Boyarski, E.; Felner, A.; Stern, R.; Sharon, G.; Betzalel, O.; Tolpin, D.; and Shimony, E. 2015. ICBS: The improved conflict-based search algorithm for multi-agent pathfinding. In _Proceedings of the International Symposium on Combinatorial Search (SoCS)_ , volume 6, 223–225. 

Chan, S.-H.; Stern, R.; Felner, A.; and Koenig, S. 2023. Greedy priority-based search for suboptimal multi-agent path finding. In _Proceedings of the International Symposium on Combinatorial Search (SoCS)_ , volume 16, 11–19. 

Chegireddy, C. R.; and Hamacher, H. W. 1987. Algorithms for finding k-best perfect matchings. _Discrete Applied Mathematics_ , 18(2): 155–165. 

Chen, Z.; Alonso-Mora, J.; Bai, X.; Harabor, D.; and Stuckey, P. J. 2021. Integrated task assignment and path planning for capacitated multi-agent pickup and delivery. _IEEE Robotics and Automation Letters_ , 6(3): 5816–5823. 

Cohen, L.; Greco, M.; Ma, H.; Hern´andez, C.; Felner, A.; Kumar, T. S.; and Koenig, S. 2018. Anytime focal search with applications. In _Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)_ , 1434–1441. 

Engquist, M. 1982. A successive shortest path algorithm for the assignment problem. _Information Systems and Operational Research (INFOR)_ , 20(4): 370–384. 

Erdmann, M.; and Lozano-Perez, T. 1987. On multiple moving objects. _Algorithmica_ , 2: 477–521. 

H¨onig, W.; Kiesel, S.; Tinka, A.; Durham, J. W.; and Ayanian, N. 2018. Conflict-based search with optimal task assignment. In _Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS)_ , 757–765. 

Li, J.; Chen, Z.; Harabor, D.; Stuckey, P. J.; and Koenig, S. 2022. MAPF-LNS2: Fast repairing for multi-agent path finding via large neighborhood search. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , volume 36, 10256–10265. 

Li, J.; Ruml, W.; and Koenig, S. 2021. EECBS: A boundedsuboptimal search for multi-agent path finding. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , volume 35, 12353–12362. 

Luna, R. J.; and Bekris, K. E. 2011. Push and swap: Fast cooperative path-finding with completeness guarantees. In _Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)_ , 294–300. 

Ma, H.; Harabor, D.; Stuckey, P. J.; Li, J.; and Koenig, S. 2019. Searching with consistent prioritization for multiagent path finding. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , volume 33, 7643–7650. 

Ma, H.; and Koenig, S. 2016. Optimal target assignment and path finding for teams of agents. In _Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS)_ , 1144–1152. 

Mills-Tettey, G. A.; Stentz, A.; and Dias, M. B. 2007. The dynamic Hungarian algorithm for the assignment problem with changing costs. _Robotics Institute, Pittsburgh, PA, Tech. Rep. CMU-RI-TR-07-27_ . 

Okumura, K. 2023. LaCAM: Search-based algorithm for quick multi-agent pathfinding. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , volume 37, 11655–11662. 

Pearl, J.; and Kim, J. H. 1982. Studies in semi-admissible heuristics. _IEEE Transactions on Pattern Analysis and Machine Intelligence (PAMI)_ , 4: 392–399. 

Ren, Z.; Rathinam, S.; and Choset, H. 2023. CBSS: A new approach for multiagent combinatorial path finding. _IEEE Transactions on Robotics_ , 39(4): 2669–2683. 

Sharon, G.; Stern, R.; Felner, A.; and Sturtevant, N. R. 2015. Conflict-based search for optimal multi-agent pathfinding. _Artificial Intelligence_ , 219: 40–66. 

Silver, D. 2005. Cooperative pathfinding. In _Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment (AIIDE)_ , volume 1, 117–122. 

Standley, T. 2010. Finding optimal solutions to cooperative pathfinding problems. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , volume 24, 173–178. 

Standley, T.; and Korf, R. 2011. Complete algorithms for cooperative pathfinding problems. In _Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)_ , 668–673. 

Stern, R.; Sturtevant, N. R.; Felner, A.; Koenig, S.; Ma, H.; Walker, T. T.; Li, J.; Atzmon, D.; Cohen, L.; Kumar, T. K. S.; Boyarski, E.; and Bartak, R. 2019. Multi-Agent pathfinding: Definitions, variants, and benchmarks. In _Proceedings of the International Symposium on Combinatorial Search (SoCS)_ , 1, 151–158. 

Tang, Y.; Ren, Z.; Li, J.; and Sycara, K. 2023. Solving multi-agent target assignment and path finding with a single constraint tree. In _IEEE International Symposium on Multi-Robot and Multi-Agent Systems (MRS)_ , 8–14. 

Wagner, G.; and Choset, H. 2011. M*: A complete multirobot path planning algorithm with performance bounds. In _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 3260–3267. 

Wagner, G.; and Choset, H. 2015. Subdimensional expansion for multirobot path planning. _Artificial Intelligence_ , 219: 1–24. 

Wang, K.-H. C.; and Botea, A. 2008. Fast and memoryefficient multi-agent pathfinding. In _Proceedings of the International Conference on Automated Planning and Scheduling (ICAPS)_ , 380–387. 

Wurman, P. R.; D’Andrea, R.; and Mountz, M. 2008. Coordinating hundreds of cooperative, autonomous vehicles in warehouses. _AI Magazine_ , 29(1): 9–19. 

Yu, J.; and LaValle, S. 2013. Structure and intractability of optimal multi-robot path planning on graphs. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , volume 27, 1443–1449. 

Zhong, X.; Li, J.; Koenig, S.; and Ma, H. 2022. Optimal and bounded-suboptimal multi-goal task assignment and path finding. In _Proceedings of IEEE International Conference on Robotics and Automation (ICRA)_ , 10731–10737. 

Okumura, K.; and D´efago, X. 2023. Solving simultaneous target assignment and path planning efficiently with timeindependent execution. _Artificial Intelligence_ , 321: 103946. 

