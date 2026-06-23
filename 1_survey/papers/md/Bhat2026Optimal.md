---
citation_key: Bhat2026Optimal
arxiv_id: 2603.21880
arxiv_url: "https://arxiv.org/abs/2603.21880"
title: "Optimal Solutions for the Moving Target Vehicle Routing Problem with Obstacles via Lazy Branch and Price"
authors_short: "Anoop Bhat et al."
year: 2026
direction_tag: I_corridor_planning
source: pymupdf4llm
converted_at: 2026-06-23T17:52:28Z
origin: ai+web
reviewed: false
---

# **Optimal Solutions for the Moving Target Vehicle Routing Problem with Obstacles via Lazy Branch and Price** 

Anoop Bhat[1] and Geordan Gutow[2] and Surya Singh[3] and Zhongqiang Ren[4] and Sivakumar Rathinam[5] and Howie Choset[1] 

_**Abstract**_ **— The Moving Target Vehicle Routing Problem with Obstacles (MT-VRP-O) seeks trajectories for several agents that collectively intercept a set of moving targets. Each target has one or more time windows where it must be visited, and the agents must avoid static obstacles and satisfy speed and capacity constraints. We introduce Lazy Branch-and-Price with Relaxed Continuity (Lazy BPRC), which finds optimal solutions for the MT-VRP-O. Lazy BPRC applies the branch-and-price framework for VRPs, which alternates between a restricted master problem (RMP) and a pricing problem. The RMP aims to select a sequence of target-time window pairings (called a tour) for each agent to follow, from a limited subset of tours. The pricing problem adds tours to the limited subset. Conventionally, solving the RMP requires computing the cost for an agent to follow each tour in the limited subset. Computing these costs in the MT-VRP-O is computationally intensive, since it requires collision-free motion planning between moving targets. Lazy BPRC defers cost computations by solving the RMP using lower bounds on the costs of each tour, computed via motion planning with relaxed continuity constraints. We lazily evaluate the true costs of tours as-needed. We compute a tour’s cost by searching for a shortest path on a Graph of Convex Sets (GCS), and we accelerate this search using our continuity relaxation method. We demonstrate that Lazy BPRC runs up to an order of magnitude faster than two ablations.** 

## I. INTRODUCTION 

Finding trajectories for multiple agents to visit multiple moving targets is necessary in applications such as defense [1], [2], [3], orbital refueling [4], and recharging mobile robots collecting data from the seafloor [5]. These applications can be modeled as variations of the Vehicle Routing Problem (VRP) [6], [7]. The VRP assumes a set of stationary targets and a set of agents, where the agents start at a common location called the depot. Each target has a demand of goods, and each agent has a capacity on the amount of goods it can deliver. Given the travel cost between every pair of targets, and between the targets and the depot, the VRP seeks a sequence of targets for each agent with minimal sum of costs, such that the sum of demands of targets visited by an agent does not exceed the capacity. In the Moving Target VRP (MT-VRP) [8], the targets are moving, and we seek not 

> 1Robotics Institute at Carnegie Mellon University, 5000 Forbes Ave., Pittsburgh, PA 15213. Emails: _{_ agbhat, choset _}_ @andrew.cmu.edu. 

> 2Mechanical and Aerospace Engineering at Michigan Technological University, Houghton, MI 49931. Email: gmgutow@mtu.edu 

> 3Robotics and AI Institute, Cambridge, MA 02142. Email: ssingh@raiinst.com 

> 4UM-SJTU Joint Institute and Department of Automation at Shanghai Jiao Tong University, Shanghai, China. Email: zhongqiang.ren@sjtu.edu.cn 

> 5Department of Mechanical Engineering and Department of Computer Science and Engineering at Texas A&M University, College Station, TX 77843. Email: srathinam@tamu.edu 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0001-10.png)


Fig. 1. Targets move through obstacle environment and must be intercepted within time windows, shown in bold-colored lines. Agents begin and end at depot, intercepting targets while avoiding obstacles. 

only a sequence of targets for each agent, but a trajectory. Each target must be met in a particular time window(s), and the agents have a speed limit. Prior work on the MT-VRP assumes piecewise-linear target trajectories [8], and we make the same assumption. When the agents must avoid static obstacles, we have the MT-VRP with Obstacles (MT-VRPO), shown in Fig. 1. 

The MT-VRP-O generalizes the Traveling Salesman Problem (TSP), and thus finding an optimal solution is NP-hard [9], [1]. No prior methods find an optimal solution for the MT-VRP-O. The closest related work finds optimal solutions for the MT-VRP without obstacles [8], using the branchand-price framework [10]. In this work, we develop a new branch-and-price algorithm for the MT-VRP-O called Lazy Branch-and-Price with Relaxed Continuity (Lazy BPRC). 

We define the pairing of a target with one of its time windows as a _target-window_ . We define a tour as a sequence of target-windows, meant to be followed by a single agent. The cost of a tour is the distance traveled by a collisionfree trajectory intercepting the tour’s targets in order. The MT-VRP-O seeks a least-cost set of tours for the agents to follow, from the set of all possible tours. Since explicitly enumerating all possible tours is intractable, we employ _column generation_ [11], where we initially generate a limited subset _F_ of all possible tours, then alternate between selecting a set of tours from _F_ and adding tours to _F_ . 

Traditionally, the selection step within column generation (known as the restricted master problem) aims to minimize the sum of selected tours’ costs. In the MT-VRP-O, however, computing tour costs is expensive, since it requires collisionfree motion planning. Our key idea is to instead perform column generation using cheap-to-compute _lower bounds_ on tour costs. We compute these lower bounds by solving a 

motion planning problem with relaxed continuity constraints. Thus, we incorporate an outer alternation between (i) column generation using lower bounds on tour costs, and (ii) lazily evaluating only the costs of tours selected by column generation. We evaluate the cost of a tour by searching for a shortest path in a Graph of Convex Sets (GCS) [12]; we use our continuity relaxation strategy to provide a heuristic for the search. If column generation selects a set of tours whose costs have all been evaluated, we terminate the alternation between (i) and (ii). Our numerical results show that Lazy BPRC runs up to 46 times faster than a non-lazy ablation, and up to 26 times faster than an ablation using an existing obstacle-unaware heuristic [13]. 

## II. RELATED WORK 

While the MT-VRP-O has not been studied in prior work, several related problems have been studied. [5] studies a multi-agent Moving Target TSP with Obstacles (multi-agent MT-TSP-O), which lacks the capacity constraints from the MT-VRP-O. However, their approach only allows interception at sampled points along the targets’ trajectories, and thus [5] does not provide optimal solutions. On the other hand, for the single-agent MT-TSP-O, [13] presents a solver that finds optimal solutions. [13] alternates between a high-level search to generate a tour, and a low-level search to find a trajectory intercepting the tour’s targets to determine its cost. The low-level search in [13] solves a Shortest Path Problem on a GCS (SPP-GCS). We similarly solve an SPP-GCS to evaluate a tour’s cost, and we provide a novel heuristic for the search that we show outperforms the heuristic from [13]. 

[8] studies the MT-VRP without obstacles using an approach called Branch-and-Price with Relaxed Continuity (BPRC). Our approach, Lazy BPRC, extends BPRC to handle obstacles, using a new obstacle-aware continuity relaxation strategy, as well as lazy tour cost evaluation. We show in Section VII that our lazy evaluation outperforms BPRC’s non-lazy tour cost evaluation. 

## III. PROBLEM SETUP 

We consider _n_ tar targets moving in R[2] , and _{_ 1 _,_ 2 _, . . . , n_ tar _}_ is the set of targets. Each target _i_ has a demand _di_ . Target _i_ has _n_ win( _i_ ) time windows, and [ _t_ ~~_i_~~ _,j[,] ti,j_ ] is the _j_ th time window of target _i_ . The trajectory of target _i_ is _τi_ : R _→_ R[2] , and we assume _τi_ has constant velocity within each time window, but possibly different velocities in different time windows. Without loss of generality, we assume targets do not pass through obstacles during their time windows.[1] 

Let the number of agents be _n_ agt. Each agent has a capacity _d_ max on the amount of demand it can serve. When visiting a target, an agent must serve the target’s full demand. Each agent has a speed limit _v_ max, and no target moves faster than _v_ max within its time windows. We denote an agent’s trajectory as _τ_ a. An agent trajectory _τ_ a _intercepts_ target _i_ if (i) _τ_ a( _t_ ) = _τi_ ( _t_ ) for some _t_ within some time window of 

> 1If a target enters an obstacle within a time window, we can replace the single window with two time windows: one that ends when the target enters the obstacle, and another that begins when the target exits the obstacle. 

target _i_ , and (ii) _τ_ a _claims_ target _i_ at time _t_ . The notion of claiming is needed when we plan a trajectory _τ_ a to intercept some target _i_ , then _i[′]_ , but _τ_ a matches space-time locations with some target _i[′′]_ unintentionally. As long as _τ_ a does not claim _i[′′]_ , the agent’s capacity is not depleted when it meets _i[′′]_ . All agents start at a depot _p_ d _∈_ R[2] . Finally, the agents must avoid collisions with stationary obstacles. We refer to a collision-free agent trajectory satisfying the speed limit as a _feasible_ agent trajectory. 

The MT-VRP-O seeks a feasible trajectory for each agent such that every target is intercepted by some agent’s trajectory, and for each agent, the sum of demands of targets it intercepts does not exceed its capacity. In this work, we aim to minimize the sum of the agents’ distances traveled. 

## IV. INTEGER LINEAR PROGRAM (ILP) FOR MT-VRP-O 

Lazy BPRC considers a _target-window graph G_ tw = ( _V_ tw _, E_ tw). Each node in _V_ tw is a pairing of a target _i_ with one of its time windows, called a _target-window_ . For example, _γi,j_ = ( _i,_ [ _t_ ~~_i_~~ _,j[,] ti,j_ ]) denotes the _j_ th target-window of target _i_ . _V_ tw contains all possible target-windows, as well as a fictitious target-window _γ_ 0 _,_ 1 = _γ_ 0 = (0 _,_ [0 _, ∞_ )), referring to a fictitious stationary target 0 at the depot, with time window [0 _, ∞_ ). An agent trajectory _τ_ a _intercepts_ target-window _γi,j_ if _τ_ a intercepts target _i_ at some _t ∈_ [ _t_ ~~_i_~~ _,j[,] ti,j_ ]. 

_E_ tw contains an edge from _γi,j_ to _γi′,j′_ if _i ̸_ = _i[′]_ . Each edge ( _γi,j, γi′,j′_ ) _∈E_ tw contains a value LFDT( _γi,j, γi′,j′, ti′,j′_ ), called the _latest feasible departure time_ . The LFDT is the latest time _t ∈_ [ _t_ ~~_i_~~ _,j[,] ti,j_ ] such that a feasible agent trajectory exists beginning at space-time point ( _τi_ ( _t_ ) _, t_ ) and intercepting _γi′,j′_ at time _ti′,j′_ . We compute LFDT for all edges at the beginning of BPRC using the method from [14]. 

A _tour_ is a path in _G_ tw beginning and ending at _γ_ 0, visiting at most one target-window per non-fictitious target, such that (i) the sum of demands of visited targets is no larger than _d_ max, and (ii) a feasible agent trajectory exists intercepting the target-windows in the tour in sequence. For a tour Γ, let Γ[ _n_ ] denote the _n_ th element of Γ; in the subsequent text, we use the same bracket notation to indicate the _n_ th element of any sequence. Let Len(Γ) denote the number of target-windows in Γ. An agent trajectory _τ_ a _executes_ Γ if _τ_ a intercepts the target-windows in Γ in sequence, and _τ_ a is feasible. For a tour Γ, the cost of Γ, denoted as _c[∗]_ (Γ), is the distance traveled by a minimum-distance trajectory executing Γ. We compute the cost of a tour by solving an SPP-GCS, described in Section V-G. 

Let the set of all tours be _S_ . Lazy BPRC formulates the MT-VRP-O as the problem of selecting a set _F_ sol _⊆S_ , containing up to _n_ agt tours, such that every target is visited by some selected tour, and the sum of tour costs is minimized. In particular, for a tour Γ, let _α_ ( _i,_ Γ) = 1 if Γ visits target _i_ and let _α_ ( _i,_ Γ) = 0 otherwise. Define a binary variable _θk_ which equals 1 if tour _k_ is selected and 0 otherwise. We 

formulate the MT-VRP-O as the following ILP: 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0003-01.png)



![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0003-02.png)


(1a) minimizes the sum of tour costs, (1b) ensures that no more than _n_ agt tours are selected, (1c) ensures all targets are visited, and (1d) enforces that each _θk_ is binary. 

## V. LAZY BPRC 

## _A. Preliminaries_ 

When solving ILP (1), explicitly having decision variables for every Γ _k ∈S_ is intractable, since the number of tours grows factorially with the numbers of targets. Thus, Lazy BPRC maintains a subset _F ⊆S_ , which is enlarged throughout the algorithm, and only selects tours from _F_ . For each tour Γ _∈F_ , we maintain a lower bound _c_ (Γ) and an upper bound _c_ (Γ) on _c[∗]_ (Γ). At the time when we add a tour Γ into _F_ , we compute the lower bound using the method from Section V-D and the upper bound using the method from Section V-E, and we refer to Γ as _unevaluated_ . Over the course of the algorithm, we compute _c[∗]_ (Γ) for certain tours Γ, then set their lower and upper bounds equal to _c[∗]_ (Γ); we refer to such tours Γ as _evaluated_ . For a set of tours _F_ sol that is feasible for ILP (1), let _c_ ( _F_ sol) = � _c_ (Γ). Γ _∈F_ sol 

## **Algorithm 1** Lazy BPRC 

1: _F_ inc = GenerateFeasibleSolution() 

> 2: **if** _F_ inc = _∅_ **then** return INFEASIBLE 

3: _F_ = Copy( _F_ inc) 

4: STACK = [ _∅_ ] 

|3: <br>4:|_F_ = Copy(_F_inc)<br> STACK = [_∅_]||
|---|---|---|
|5:|**while** STACK is not empty **do**||
|6:|_B_ = STACK.pop()||
|7:|**while** true **do**||
|8:<br>9:|_θ, c_<br>(_θ_) = SolveLP<br>-_B_(_F_, _F_inc)<br>**if** _θ_ is purely integer AND _c_<br>(_θ_)_<_|_c_inc **then**|
|10:|_F_sol = ExtractTours(_θ_, _F_)||
|11:|_F_uneval = GetUnevaluatedTours(_F_sol)||
|12:|ComputeTourCosts(_F_uneval)||
|13:|**if**<br>_c_(_F_sol)_<_<br>_c_inc **then** _F_inc =_F_sol||
|14:<br>15:|**else** break<br>**if** _c_<br>(_θ_)_≥_<br>_c_inc **then** continue||
|16:|_B′, B′′_ = GenerateSuccessors(_B, θ, F_)||
|17:|STACK.push(_B′_)||
|18:|STACK.push(_B′′_)||
|19:|return _F_inc||



## _B. Branch and Bound_ 

Lazy BPRC solves ILP (1) via the branch-and-bound procedure shown in Alg. 1. The algorithm begins by generating an initial feasible solution _F_ inc for ILP (1), using the 

method in Section V-H. We call _F_ inc the incumbent, and we continually update _F_ inc to be the best solution to ILP (1) found so far, where “best” refers to smallest _c_ -value. We initialize the subset _F_ , introduced in Section V-A, to _F_ inc. Define _c_ inc as always taking the value of _c_ ( _F_ inc). 

Next, we initialize a stack of _branch-and-bound nodes_ , where each node _B_ is a set of disallowed edges in _E_ tw. Let ILP- _B_ be ILP (1), with the constraint _θk_ = 0 for any Γ _k_ traversing an edge in _B_ . Let LP- _B_ be the convex relaxation of ILP- _B_ which replaces constraint (1d) with _θk ≥_ 0: LP- _B_ is often called the _master problem_ in branch-and-price. Let _c[∗]_ ( _B_ ) be the optimal cost of LP- _B_ . 

When we expand _B_ , we compute a lower bound on the optimal cost of ILP- _B_ , which we obtain from a lower bound on the optimal cost of LP- _B_ . In particular, we enter a loop that solves LP- _B_ with lazy evaluation of tours in _F_ (Line 7). On Line 8, we solve LP- _B_ , but replace _c[∗]_ (Γ _k_ ) in the objective (1a) with _c_ (Γ _k_ ): we call this problem the _surrogate master problem_ , LP- _B_ . We obtain a solution _θ_ to LP- _B_ using column generation, which may add tours to _F_ and update _F_ inc (Section V-C). On Line 8, _c_ ( _θ_ ) denotes the cost of _θ_ within LP- _B_ . Note that _θ_ may not be optimal for LP- _B_ , but we ensure that 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0003-18.png)


as described in Section V-F. 

We then check if _θ_ is purely integer and _c_ ( _θ_ ) _< c_ inc (Line 9). If so, _θ_ corresponds to a set of tours _F_ sol whose actual cost may be lower than _c_ inc. Let _F_ uneval be the set of unevaluated tours in _F_ sol. We must have _F_ uneval = _∅_ , since as we explain in Section V-C, while solving LP- _B_ , whenever we obtain an integer solution _θ_ whose corresponding set _F_ sol has all tours evaluated, we set _F_ inc = _F_ sol. Thus, we evaluate each Γ _k ∈F_ uneval by solving an SPP-GCS (Section V-G), then solve LP- _B_ again. 

After exiting the lazy evaluation loop, if _c_ ( _θ_ ) _≥ c_ inc, we continue to the next expansion. Otherwise, the failure of the conditions on Lines 9 and 15 imply that _θ_ contains noninteger values. We create two successors for _B_ , denoted as _B[′]_ and _B[′′]_ , such that _θ_ is feasible for neither LP- _B[′]_ nor LP- _B[′′]_ , but all integer solutions to ILP- _B_ are feasible for both ILP- _B[′]_ and ILP- _B[′′]_ . To do so, we apply “conventional branching” [15]. In particular, for an edge _e ∈E_ tw, define the _flow_ along _e_ as the sum of _θk_ values for all Γ _k_ traversing _e_ . We select the edge _e_ with flow closest to 0.5 and let _B[′]_ = _B ∪{e}_ . We then define _B[′′]_ so that _e_ is required be traversed by some tour in a solution to ILP- _B[′′]_ , by disallowing other edges appropriately (see [15]). We push _B[′]_ and _B[′′]_ onto the stack. 

## _C. Column Generation_ 

We now describe how we find a solution _θ_ for LP- _B_ satisfying (2). As stated in Section V-A, enumerating all the decision variables for LP- _B_ is intractable, so we use column generation [11]. In particular, define the _restricted surrogate master problem_ (RSMP) on _F_ as LP- _B_ with the constraint that _θk_ = 0 for all tours Γ _k ∈F/_ . Note that to solve the RSMP, we do not have to solve for _θk_ with Γ _k ∈F/_ . To find 

a solution _θ_ to LP- _B_ satisfying (2), we alternate between solving the RSMP on _F_ and adding tours to _F_ . To find tours to add to _F_ , we solve a _pricing problem_ (Section V-F). Whenever we obtain an integer solution _θ_ to the RSMP, this corresponds to a feasible solution _F_ sol to the MT-VRP-O. In this case, if _c_ ( _F_ sol) _< c_ inc, we set _F_ inc = _F_ sol. 

We alternate between the RSMP and pricing problem until the pricing problem finds no new tours, and we return the optimal RSMP solution _θ_ . The first time we solve the RSMP, it may be infeasible, because all feasible MT-VRPO solutions that can be constructed from tours in _F_ traverse some edge in _B_ . In this case, we use the method from Section V-H to generate a set of tours _F_ new feasible for the MT-VRPO, add these tours to _F_ sol, and solve the RSMP again. If we fail to generate _F_ new, we return _θ_ = NULL and _c_ ( _θ_ ) = _∞_ . 

## _D. Computing Lower Bound on Tour Cost_ 

This section describes how we compute the lower bound _c_ (Γ) for a tour Γ in Section V. Our method, illustrated in Fig. 2, extends the procedure from BPRC [8] to handle obstacles. At the beginning of Lazy BPRC, we divide each targetwindow _γi,j_ into _segments_ , where _ξi,j,k_ = ( _i,_ [ _t_ ~~_i_~~ _,j,k[,] ti,j,k_ ]) denotes the _k_ th segment of _γi,j_ , and Segments( _γi,j_ ) is the set of segments of _γi,j_ . To determine the number of segments per target-window, we first specify a number of segments to allocate per target, denoted as _n_ seg,tar. Then for each target _i_ , we allocate segments to its windows using the formula from BPRC [8], which gives more segments to longer windows. The depot gets a single segment _ξ_ 0. For a target-window _γ_ , _n_ seg( _γ_ ) is the number of segments allocated to _γ_ . The segment indices for a target-window are ordered in increasing order of start time. An agent trajectory _τ_ a _intercepts_ segment _ξi,j,k_ if _τ_ a intercepts target _i_ at a time _t ∈_ [ _t_ ~~_i_~~ _,j,k[,] ti,j,k_ ]. 

For every pair of segments ( _ξ, ξ[′]_ ) corresponding to different targets, we compute a lower bound _c_ seg( _ξ, ξ[′]_ ) on the cost of a feasible agent trajectory that intercepts _ξ_ , then _ξ[′]_ . To do so, we compute the shortest collision-free path in space from _ξ_ to _ξ[′]_ , ignoring time constraints, via the method from [16]. Let _c_ be the path’s distance traveled. Let _t_ be the start time of _ξ_ , and let _t[′]_ be the end time of _ξ[′]_ . We set _c_ seg( _ξ, ξ[′]_ ) = _c_ if _t_ + _c/v_ max _≤ t[′]_ , and _c_ seg( _ξ, ξ[′]_ ) = _∞_ otherwise. 

Next, given a tour Γ, we define a _segment-graph G_ seg = ( _V_ seg _, E_ seg), where the set of nodes _V_ seg is the set of all segments whose target-windows are visited by Γ. For each edge (Γ[ _n_ ] _,_ Γ[ _n_ + 1]) _∈E_ tw traversed by Γ, we connect edges in _E_ seg from every segment of Γ[ _n_ ] to every segment of Γ[ _n_ + 1]. The cost of each edge ( _ξ, ξ[′]_ ) is _c_ seg( _ξ, ξ[′]_ ). 

Let _g_ seg( _ξ_ ) be the cost of the shortest path in _G_ seg from _ξ_ 0 to _ξ_ . _c_ (Γ), computed as follows, lower-bounds _c[∗]_ (Γ): 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0004-07.png)


_g_ seg( _ξ_ 0) = 0, and for a segment _ξ[′]_ of Γ[ _n_ ] with 1 _< n <_ Len(Γ), we have _g_ seg( _ξ[′]_ ) = _ξ∈_ Segmentsmin(Γ[ _n−_ 1])[(] _[g]_[seg][(] _[ξ]_[) +] _c_ seg( _ξ, ξ[′]_ )). Thus to compute _c_ (Γ) we can iterate from _n_ = 2 to _n_ = Len(Γ) _−_ 1, and for each _n_ , compute the _g_ -values of the segments of Γ[ _n_ ] using the _g_ -values for Γ[ _n −_ 1]. 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0004-09.png)


Fig. 2. Computing bounds on the cost of an example tour Γ. To compute the lower bound _c_ (Γ), we divide each target-window visited by Γ into segments. We then construct a _segment-graph G_ seg, where the nodes are the segments, and an edge connects every segment of Γ[ _n_ ] to every segment of Γ[ _n_ +1]. The edge cost from segment _ξ_ to _ξ[′]_ is the distance traveled along the shortest path in space from _ξ_ to _ξ[′]_ , if this path satisfies the relaxed timing constraints from in Section V-D, and _∞_ otherwise. _c_ (Γ) is the cost of the shortest path in _G_ seg from _ξ_ 0 to _ξ_ 0 visiting all target-windows in Γ. To compute the upper bound _c_ , we construct a _segment-start-graph G_ start, where the nodes are the starting points of the segments, and an edge connects every segment-start of Γ[ _n_ ] to every segment-start of Γ[ _n_ + 1]. The edge cost from _s_ to _s[′]_ is distance traveled by a feasible minimum-distance agent trajectory from _s_ to _s[′]_ , if such a trajectory exists or if _s[′]_ = _s_ 0, and _∞_ otherwise. Our upper bound is the cost of the shortest path in _G_ start from _s_ 0 to _s_ 0 that visits all target-windows in Γ. 

After this, we can compute _c_ (Γ) via (3). As shown in Fig. 2, these computations correspond to finding an agent trajectory executing Γ subject to relaxed continuity constraints. 

For tours generated in the pricing problem (Section V- F), these _g_ -values are computed as a byproduct of solving the pricing problem. For tours generated using the feasible solution generation method in Section V-H, we perform these _g_ -value computations after generating the tours. 

## _E. Computing Upper Bound on Tour Cost_ 

This section describes how we compute the upper bound _c_ (Γ) for a tour Γ in Section V. Recall that in Section V-D, we divided each target-window into segments. Let the starting point in space-time of segment _ξi,j,k_ be _si,j,k_ = ( _τi_ ( _t_ ~~_i_~~ _,j,k_[)] _[,][ t]_ ~~_i_~~ _,j,k_[)][.][Denote][the][starting][point][of][the] depot segment as _s_ 0 = _s_ 0 _,_ 1 _,_ 1. For a target-window _γ_ , let SegmentStarts( _γ_ ) denote the set of segment-starts of _γ_ . We construct a _segment-start-graph G_ start = ( _V_ start _, E_ start). The set 

of nodes _V_ start is the set of all segment-starts whose targetwindows are visited by Γ. For each edge ( _γ, γ[′]_ ) _∈E_ tw traversed by Γ, we connect an edge in _E_ start from every segment-start of _γ_ to every segment-start of _γ[′]_ . 

To determine the cost of an edge from _s_ = ( _q, t_ ) to _s[′]_ = ( _q[′] , t[′]_ ), denoted as _c_ start( _s, s[′]_ ), we compute the shortest collision-free path in space from _q_ to _q[′]_ using [17]. Let the distance traveled by this path be _c_ . If _t_ + _c/v_ max _≤ t[′]_ or _s[′]_ = _s_ 0, we set _c_ start( _s, s[′]_ ) = _c_ , and otherwise _c_ start( _s, s[′]_ ) = _∞_ . 

Define _g_ start( _s_ ) as the cost of a shortest path in _G_ start from _s_ 0 to _s_ . _c_ (Γ), computed as follows, upper-bounds _c[∗]_ (Γ): 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0005-03.png)


To compute _c_ (Γ), we note that _g_ ( _s_ 0) = 0, and for a segment _ξ[′]_ of Γ[ _n_ ] with 1 _< n <_ Len(Γ), we have _g_ start( _s[′]_ ) = _s∈_ SegmentStartsmin (Γ[ _n−_ 1])[(] _[g]_[start][(] _[s]_[) +] _[ c]_[start][(] _[s, s][′]_[))][.][Thus,] we can iterate from _n_ = 2 to _n_ = Len(Γ) _−_ 1, and for each _n_ , compute the _g_ -values of the segment-starts of Γ[ _n_ ] using the _g_ -values for Γ[ _n −_ 1]. Then we can compute _c_ (Γ) using (4). For tours generated within the pricing problem (Section V-F), this computation happens as a byproduct and does not require extra computation. For tours generated using the feasible solution generation method in Section V-H, we must compute these _g_ -values separately from the tour generation. 

We place points _si,j,k_ at the segment-starts rather than at arbitrary points because, within the pricing problem (Section V-F), we need an upper bound on the cost of reaching each segment-start for dominance checking. 

## _F. Pricing Problem_ 

The pricing problem seeks a set of tours _F_ price such that the RSMP on _F ∪F_ price has a smaller optimal cost than the RSMP on _F_ . To solve the pricing problem, we first note that when the RSMP produces a solution _θ_ (specifically, its primal solution), the RSMP also produces a dual solution ( _λ_ 0 _, λ_ 1 _, . . . , λn_ tar), where _λ_ 0 _∈_ R _≤_ 0 is the dual variable corresponding to (1b), and for _i >_ 0, _λi ∈_ R _≥_ 0 is the dual variable corresponding to (1c). Similarly to prior VRP work [11], we define the _reduced cost_ of Γ as follows: 

_c_ ~~r~~ ed[(Γ) =] _[c]_ (Γ) _− c_ dual(Γ) (5) _n_ tar where _c_ dual(Γ) = � _α_ ( _i,_ Γ) _λi_ + _λ_ 0. To improve the RSMP’s _i_ =1 optimal cost, _F_ price must contain a tour with negative reduced cost [11]. Therefore, as in prior work, we search for tours with negative reduced cost. 

In contrast to prior work, we do not guarantee returning a tour with negative reduced cost if such a tour exists. Instead, we only guarantee returning some Γ such that _c[∗]_ (Γ) _− c_ dual(Γ) _<_ 0, if such Γ exists. This is sufficient to ensure that if we do not return any tours, then (2) is satisfied, as shown in the proof of Lemma 1. 

We search for tours with negative reduced cost by modifying the labeling algorithm from [8] to handle obstacles. First, we define a _partial tour_ , which has the same definition as a tour from Section IV, except that a partial tour does not need to end with the depot. 

_1) Labels and Label Dominance:_ Within our labeling algorithm, we represent a partial tour Γ using a _label l_ = ( _γi,j, t, σ,[⃗] b,⃗g_ ub _,⃗g_ lb _, λ_ ), where 

- _γi,j_ is the final target-window in Γ 

- _t_ is the minimum time required to execute Γ 

- _σ_ is the sum of demands of targets visited by Γ 

- _[⃗] b_ is a binary vector with length _n_ tar where _[⃗] b_ [ _i[′]_ ] = 1 for any target _i[′]_ such that either (i) Γ visits _i[′]_ , (ii) _t >_ LFDT( _γi,j, γi′,j′_ ) for all _j[′] ∈{_ 1 _,_ 2 _, . . . , n_ win( _i[′]_ ) _}_ , or (iii) _σ_ + _di′ > d_ max 

- _⃗g_ ub is a vector with length _n_ seg( _γi,j_ ) where, if Γ is not a tour, _⃗g_ ub[ _k_ ] = _g_ start( _si,j,k_ ) within the segment-startgraph for all tours extending from Γ. If Γ is a tour, _⃗g_ ub contains a single element equal to _c_ (Γ), as computed in Section V-E (i.e. not the true tour cost) 

- _⃗g_ lb is a vector with length _n_ seg( _γi,j_ ) where, if Γ is not a tour, we have _⃗g_ lb[ _k_ ] = _g_ seg( _ξi,j,k_ ) within the segmentgraph for all tours extending from Γ. If Γ is a tour, _⃗g_ lb contains a single element equal to _c_ (Γ), as computed in Section V-E (i.e. not the true tour cost) 

## _• λ_ = _c_ dual(Γ) 

Consider two labels _l_ = ( _γi,j, t, σ,[⃗] b,⃗g_ ub _,⃗g_ lb _, λ_ ) and _l[′]_ = ( _γi,j, t[′] , σ[′] ,[⃗] b[′] ,⃗g[′]_ ub _[,⃗g][ ′]_ lb _[, λ][′]_[)][,][both][at][target-window] _[γ][i,j]_[.][If] _γi,j_ = _γ_ 0, we say _l dominates l[′]_ if _⃗g_ ub[1] _− λ ≤ ⃗g[′]_ lb[[1]] _[ −][λ]_[.] Otherwise, _l_ dominates _l[′]_ if 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0005-20.png)


where _δ_ ( _ξi,j,k_ ) is the length of segment _ξi,j,k_ in space. Let Γ be the partial tour represented by _l_ and Γ _[′]_ be the partial tour represented by _l[′]_ . Let Ω be the tour extending Γ such that _c[∗]_ (Ω) _− c_ dual(Ω) is minimal, and let Ω _[′]_ be the tour extending Γ _[′]_ such that _c[∗]_ (Ω _[′]_ ) _− c_ dual(Ω _[′]_ ) is minimal. If _l_ dominates _l[′]_ by our definition above, then _c[∗]_ (Ω) _− c_ dual(Ω) _< c[∗]_ (Ω _[′]_ ) _− c_ dual(Ω _[′]_ ) ([8], Theorem 1). 

In particular, (6) and (7) are standard dominance conditions from the VRP literature [10], ensuring that any sequence of target-windows that can be appended to Γ can also be appended to Γ _[′]_ without the violating the capacity constraint or causing a target to be revisited. 

Condition (8) is specific to moving targets. Consider trajectories _τ_ a and _τ_ a _[′]_ that execute Γ and Γ _[′]_ , respectively, and terminate by intercepting _ξi,j,k_ , with minimum distance traveled. Define the reduced cost of _τ_ a as the distance traveled minus _λ_ , and the reduced cost of _τ_ a _[′]_ likewise using _λ[′]_ . The term _⃗g_ ub[ _k_ ] on the LHS of (8) upper-bounds the distance an agent must travel to execute Γ and travel to the start of _ξi,j,k_ , and _δ_ ( _ξi,j,k_ ) is the distance an agent must travel from the start of _ξi,j,k_ to the end, i.e. to visit every point in the segment. Thus, the sum of these two terms upperbounds the cost of _τ_ a, since _τ_ a cannot do worse than travel to the start of _ξi,j,k_ , then move along _ξi,j,k_ to the point of interception. Thus the LHS upper-bounds the reduced cost of _τ_ a. The _⃗g[′]_ lb[lower-bounds][the][distance][traveled][by] _[τ]_[a] _[′]_[,][so] the RHS lower-bounds the reduced cost of _τ_ a _[′]_ . If condition 

(8) holds, _τ_ a cannot be worse (i.e. cannot have more positive reduced cost) than _τ_ a _[′]_ and we can discard _l[′]_ . 

_2) Labeling Algorithm:_ Our labeling algorithm maintains a set of mutually nondominated labels at each target-window, as well as a priority queue, where labels with lexicographically smaller ( _t, σ,_ min( _g_ lb) _− λ_ ) have higher priority. When we expand a label _l_ = ( _γi,j, t, σ,[⃗] b,⃗g_ ub _,⃗g_ lb _, λ_ ), we iterate over all _successor target-windows_ of _l_ , i.e. all target-windows _γi′,j′_ satisfying the following conditions: 

1) ( _γi,j, γi′,j′_ ) _∈E_ tw _\ B_ 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0006-03.png)


For each successor target-window _γi′,j′_ , we generate a successor label _l[′]_ = ( _γi′,j′, t[′] , σ[′] ,[⃗] b[′] ,⃗g[′]_ ub _[,⃗g][ ′]_ lb _[, λ][′]_[)][,][where] 

- _t[′]_ = EFAT( _γi,j, γi′,j′, t_ ), where EFAT is the earliest time at which a feasible agent trajectory can intercept _γi[′] ,j[′]_ after intercepting _γi,j_ at time _t_ . EFAT stands for “earliest feasible arrival time,” and we compute it using the method from [14]. 

- _σ[′]_ = _σ_ + _di′_ 

- _[⃗] b[′]_ is identical to _[⃗] b_ , except for the following modifications. First, if _i[′]_ = 0, we set _[⃗] b[′]_ [ _i[′]_ ] = 1. Then, we set _b[⃗][′]_ [ _i[′′]_ ] = 1 for each target _i[′′]_ such that either (i) _σ[′]_ + _di′′ > d_ max, or (ii) for all _j[′′] ∈{_ 1 _,_ 2 _, . . . , n_ win( _i[′′]_ ) _}_ , _t[′] >_ LFDT( _γi′,j′, γi′′j′′_ ). 

- For each _k[′] ∈{_ 1 _,_ 2 _, . . . , n_ seg( _γi′,j′_ ) _}_ , we compute 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0006-09.png)



![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0006-10.png)



![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0006-11.png)


_• λ[′]_ = _λ_ , if _i[′]_ = 0, and _λ[′]_ = _λ_ + _λi′_ otherwise 

We then check if any labels at _γi[′] ,j[′]_ dominate _l[′]_ . If so, we prune _l[′]_ . Otherwise, we prune labels at _γi′,j′_ dominated by _l[′]_ , and we mark them to be discarded upon expansion from the priority queue. Then we push _l[′]_ onto the priority queue. Any time we generate a successor label _l_ at _γ_ 0 with _⃗g_ lb[1] _− λ <_ 0,[2] , and _l_ is not dominated, we reconstruct the tour Γ represented by _l_ via backpointer traversal, then add Γ to the set of tours to be returned. At this step, if Γ has already been evaluated, we do not add it to this set, since _c[∗]_ red[(Γ)] cannot be negative. The search ends when the priority queue becomes empty. 

## _G. Computing Tour Cost via SPP-GCS_ 

At the beginning of Lazy BPRC, we decompose free space into convex regions _A_ 1 _, A_ 2 _, . . . , An_ reg , where _n_ reg is the number of regions. We then define a GCS _G_ cs = ( _V_ cs _, E_ cs), where the set of nodes _V_ cs consists of convex sets in spacetime. For each region _A_ in our free space decomposition, we have a _region-node XA_ = _A ×_ R. For each target-window _γi,j_ visited by Γ, we have a _window-node Xi,j_ , consisting of 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0006-16.png)


the set of space-time points along _τi_ within [ _t_ ~~_i_~~ _,j[,] ti,j_ ]. Since we assumed that a target’s velocity is constant within a time window, _Xi,j_ is a line segment in space-time, which is a convex set. We refer to nodes in _G_ cs as _GCS-nodes_ . An edge connects a set _X_ to a set _X[′]_ if _X_ intersects _X[′]_ . We refer to a path in _G_ cs as a _GCS-path_ . We say a GCS-path _P visits_ target-window _γi,j_ if _P_ contains _Xi,j_ . 

We find a trajectory executing Γ using an algorithm similar to FMC* [13], but without the various speedup techniques that FMC* implements particularly for a minimum-time objective, since we aim to minimize distance traveled. We also replace the heuristic from FMC* with the heuristic described later in the section, and we replace the focal search from FMC* with a best-first search, since we seek optimal solutions rather than bounded-suboptimal solutions. 

We search the GCS using a priority queue called OPEN, containing GCS-paths. We initialize OPEN with the GCSpath ( _X_ 0 _,_ 1), i.e. a path that stays at the depot. Each GCSpath on OPEN has an _f_ -value. The initial GCS-path ( _X_ 0 _,_ 1) has an _f_ -value of 0; we discuss the computation of _f_ for other GCS-paths shortly. GCS-paths with smaller _f_ -values have higher priority. 

Each iteration pops a GCS-path _P_ from OPEN, then iterates over each GCS-node _X_ adjacent to _P_ [ _−_ 1]. If _X_ is a window-node _Xi,j_ , and _P_ has not visited the target-windows occurring before _γi,j_ in Γ, we discard _X_ . If _X_ is a regionnode, and _X_ already occurs in _P_ after the final window-node in _P_ , we discard _X_ . If we do not discard _X_ , we construct a successor GCS-path _P[′]_ by appending _X_ to _P_ , then compute its _f_ -value as follows. 

Suppose the first target-window in Γ unvisited by _P[′]_ is Γ[ _n_ ]. We optimize a trajectory _τ_ a with a collision-free portion _τ_ a,1 passing through the sets in _P_ in sequence, followed by an obstacle-unaware portion _τ_ a,2 that travels to Γ[ _n_ ]. We parameterize _τ_ a,1 with a line segment per set in _P_ , and _τ_ a,2 with a single line segment. The objective of the trajectory optimization is a _g_ -value plus an _h_ -value. The _g_ -value is the distance traveled by _τ_ a,1. The _h_ -value is the distance traveled by _τ_ a,2, plus a term _hn_ ( _t_ ) which depends on the ending time _t_ of _τ_ a,2. _hn_ ( _t_ ) lower bounds the cost of intercepting the remaining targets in Γ after departing Γ[ _n_ ] at time _t_ , and we describe how to compute _hn_ in Section V-G.1. 

The trajectory optimization is the same as the optimization performed for a GCS-path in FMC* [13], except for two differences. First, FMC* also optimizes an obstacle-unaware portion of the trajectory that departs Γ[ _n_ ] and intercepts all remaining targets, in place of our _hn_ value. Second, we constrain our computed trajectory to intercept Γ[ _n_ ] no later than a value _t_ max _,n_ , which is the latest time at which a feasible agent trajectory could depart Γ[ _n_ ], then intercept the remaining sequence of target-windows in Γ. We compute _t_ max _,n_ for each _n ∈{_ 1 _,_ 2 _, . . . ,_ Len(Γ) _}_ before beginning the search as follows. For _n_ = Len(Γ), we set _t_ max _,n_ = _∞_ . We then iterate backwards from _n_ = Len(Γ) _−_ 1 to _n_ = 1, and _t_ max _,n_ = LFDT(Γ[ _n_ ] _,_ Γ[ _n_ + 1] _, t_ max _,n_ +1). 

Finally, if the trajectory optimization is infeasible, we discard _P[′]_ . Otherwise, the trajectory optimization’s optimal 

cost is the _f_ -value for _P[′]_ , and we push _P[′]_ onto OPEN. _1) Constructing hn Function:_ Consider the segmentgraph _G_ seg for Γ, as defined in Section V-D. For a segment _ξ_ in _G_ seg, let _h_ seg( _ξ_ ) be the cost of the shortest path in _G_ seg from _ξ_ to _ξ_ 0. Note that _h_ ( _ξ_ 0) = 0, and for a segment _ξ_ of Γ[ _n_ ] with 1 _< n <_ Len(Γ), we have 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0007-01.png)


Before searching _G_ cs, we compute _h_ seg for all _ξ_ in _G_ seg as follows. We iterate backward from _n_ = Len(Γ) _−_ 1 to _n_ = 2, and for each _n_ , we compute the _h_ -values for the segments of Γ[ _n_ ] using the _h_ -values for Γ[ _n_ + 1] using (11). 

Next, for each _n ∈{_ 1 _,_ 2 _, . . . ,_ Len(Γ) _}_ , we do the following. Let _γi,j_ be Γ[ _n_ ]. We construct a matrix _An ∈_ R _[n]_[seg][(Γ[] _[n]_[])] _[×]_[2] whose _k_ th row is [ _t_ ~~_i_~~ _,j,k[,]_[ 1]][.][We][construct][a] vector _[⃗] bn ∈_ R _[n]_[seg][(Γ[] _[n]_[])] whose _k_ th element is _h_ ( _ξi,j,k_ ). We then find the least-squares solution _ϕn ∈_ R[2] to the equation _Anϕn_ = _[⃗] bn_ . For a time _t ∈_ [ _t_ ~~_i_~~ _,j[,] ti,j_ ], _ϕn_ [1] _t_ + _ϕn_ [2] approximates the minimum cost to intercept all remaining targetwindows in Γ after departing Γ[ _n_ ] at time _t_ . To adjust this into a lower bound, we construct another matrix _Bn_ whose _k_ th row is [ _ti,j,k,_ 1], then compute a value _r_ max as the max element of the vector vertcat( _An, Bn_ ) _ϕn −_ vertcat( _[⃗] bn,[⃗] bn_ ), where vertcat concatenates two matrices vertically. _r_ max is the largest overestimation of _h_ seg( _ξi,j,k_ ) that our approximation makes over all segment start and end times of _γi,j_ . Then _hn_ ( _t_ ) = _ϕn_ [1] _t_ + _ϕn_ [2] _− r_ max lower-bounds the remaining cost of executing Γ after departing Γ[ _n_ ] at time _t_ . 

## _H. Feasible Solution Generation_ 

To generate the initial incumbent, as well as a feasible set of tours _F_ new when the RSMP is infeasible, we extend the feasible solution generation from [8] to handle obstacles. This algorithm requires the EFAT and LFDT functions described previously. In [8], the values were computed using closed-form expressions, since [8] did not consider obstacles. Since we consider obstacles, we instead compute the values using the method from [14]. Otherwise, our initial feasible solution generation method is identical to BPRC’s. 

## _I. Caching EFAT and LFDT Values_ 

Lazy BPRC computes EFAT and LFDT several times, possibly with the same arguments. We cache the values for each unique set of arguments to speed up the algorithm. 

for all tours. This implies _λ_ is feasible for the dual of LP- _B_ (the same dual as (18)-(21) in [11]). The cost of _λ_ for the _n_ tar dual of LP- _B_ is � _λi_ + _n_ agt _λ_ 0, which lower-bounds _c[∗]_ ( _B_ ) _i_ =1 by weak duality. Combining this with (12), we have (2). 

## **Theorem 1.** _Lazy BPRC finds an optimal solution._ 

_Proof._ Let _F_ opt be an optimal MT-VRP-O solution, let _c_ opt be its cost, and let _θ_ opt be the corresponding solution to ILP (1). We show by induction that whenever we execute Alg. 1, Line 5, either _c_ inc = _c_ opt, or _θ_ opt is feasible for LP- _B_ for some _B_ on the stack. 

**Base Case** The first node pushed onto the stack is _B_ = _∅_ , and LP- _B_ is a relaxation of ILP (1), so _θ_ opt is feasible for LP- _B_ . 

**Induction Hypothesis** Suppose on Line 5, either (i) _c_ inc = _c_ opt, or (ii) _θ_ opt is feasible for LP- _B_ for some _B_ on the stack. 

**Induction Step** Suppose (i) holds. We never increase _c_ inc, and _c_ inc cannot become smaller than _c_ opt by the optimality of _c_ opt, so if Line 5 is ever executed again, (i) will still hold. 

Now suppose (ii) holds. If _B_ is not popped at this iteration, (ii) trivially holds at the next iteration. Next, suppose _B_ is popped. Combining Lemma (1) with the feasibility of _θ_ opt for LP- _B_ , we have _c_ ( _θ_ ) _≤ c_ opt. Now we have two cases. 

Case 1 Within the lazy evaluation loop, we set _c_ inc = _c_ opt. Then (i) holds when we execute Line 5 next. 

Case 2 _c_ inc = _c_ opt after the lazy evaluation loop. The optimality of _c_ opt then implies that _c_ inc _> c_ opt. Combining this with _c_ ( _θ_ ) _≤ c_ opt, we have _c_ ( _θ_ ) _< c_ inc. This means the condition on Line 15 fails and we attempt to generate successors for _B_ . No edge traversed by _F_ opt is in _B_ ; if any edge traversed by _F_ opt were in _B_ , this would contradict (ii). Thus we have some edge to branch on when generating the successors _B[′]_ and _B[′′]_ . If we branch on an edge not traversed by _F_ opt, then _θ_ opt is feasible for LP- _B[′]_ and LP- _B[′′]_ . If we branch on an edge _e_ traversed by _F_ opt, _θ_ opt is feasible for LP- _B[′′]_ . Thus (ii) holds the next time we execute Line 5. 

Thus, the induction hypothesis holds the next time we execute Line 5. Since the number of branch-and-bound nodes expanded in Alg. 1 cannot be larger than the finite number of subsets of _E_ tw, Alg. 1 terminates. Termination only occurs when the stack becomes empty. This means at some point, we check Line 5, and the stack is empty, which means (ii) from the induction hypothesis cannot hold. Thus (i) holds at termination, implying that we found an optimal solution. 

## VI. THEORETICAL ANALYSIS 

## **Lemma 1.** _When we return no tours in the pricing problem,_ (2) _is satisfied._ 

_Proof._ Referring to values from the first paragraph of Section V-F, strong duality implies 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0007-21.png)


where the RHS is the cost of _λ_ for the dual of the RSMP: this dual is the same as (18)-(21) in [11], but costs are replaced with lower bounds. If we return no tours, _c[∗]_ (Γ) _− cλ_ (Γ) _≥_ 0 

## VII. NUMERICAL RESULTS 

We ran experiments on an Intel i9-9820X 3.3GHz CPU with 10 cores, hyperthreading disabled, and 128 GB RAM. We compared Lazy BPRC to two ablations. The first ablation, called “Non-Lazy BPRC,” is the same algorithm, but whenever we generate a label _l_ representing a tour Γ, and _l_ is not currently dominated, we set _⃗g_ lb[1] = _⃗g_ ub[1] = _c[∗]_ (Γ); if Γ was unevaluated prior to this step, we evaluate Γ, update _⃗g_ lb[1] and _⃗g_ ub[1], then perform dominance checks again. The second ablation, called “No-Affine-Heuristic,” replaces our heuristic in the SPP-GCS associated with tour 


![](1_survey/papers/md/Bhat2026Optimal_figs/Bhat2026Optimal.pdf-0008-00.png)


Fig. 3. (a) Varying the number of targets. Lazy BPRC shows smaller median runtime than the ablations, particularly for larger numbers of targets. (b) Varying the map resolution. Lazy BPRC’s advantage in median runtime grows as we increase the map resolution. (c) Varying the capacity. Lazy BPRC has smaller median runtime than the ablations for all tested capacities. 

Γ in Section V-G with the heuristic from FMC*. That is, when computing the _f_ -value trajectory for a GCS-path _P[′]_ , the obstacle-unaware portion of the trajectory is required to intercept all target-windows in Γ unvisited by _P[′]_ , in sequence. Each algorithm parallelized successor generation in pricing and tour cost evaluation, the initial computation of pairwise distances between segments and segment-starts, and initial pairwise LFDT computations. 

We generated problem instances by modifying the instance generation method from [14] to handle multiple agents. In every instance, each target had two time windows, demand 1, and speed within each time window generated uniformly at random between 0.5 and 1 m/s. Each instance had three agents with _v_ max = 4 m/s. Our obstacle maps were square grids, but the agents and targets move in continuous space in the grids. We define the _map resolution_ as the width of the obstacle map in grid cells. In our experiments, we varied the number of targets, map resolution, and capacity. We set the computation time limit to 10 min, per planner, per instance. 

## _A. Experiment 1: Varying the Number of Targets_ 

We fixed the map resolution to 30 and varied _n_ tar from 3 to 15, setting the capacity _d_ max = _n_ tar _/n_ agt. Fig. 3 (a) shows the results. As _n_ tar increases, Lazy BPRC notably outperforms Non-Lazy BPRC in min, median, and max runtime, demonstrating that deferring the computation of tour costs is effective. Lazy BPRC also demonstrates smaller median and max runtimes than No-Affine-Heuristic, showing that our obstacle-aware heuristic leveraging continuity relaxation outperforms a heuristic that ignores obstacles. 

## _B. Experiment 2: Varying the Map Resolution_ 

We fixed _n_ tar to 12 and _d_ max to 4, then varied the map resolution from 10 to 30. Fig. 3 (b) shows the results. 

Lazy BPRC again demonstrates smaller median and max runtime than both ablations, and also smaller min runtime than Non-Lazy BPRC. Lazy BPRC’s advantage grows with the map resolution because as we increase map resolution, the numbers of nodes and edges in the GCS tend to increase, making the GCS more expensive to search. Lazy BPRC outperforms Non-Lazy BPRC because it reduces the number of SPP-GCS queries, and Lazy BPRC outperforms NoAffine-Heuristic by speeding up each SPP-GCS query. 

## _C. Experiment 3: Varying the Capacity_ 

We fixed _n_ tar to 9 and the map resolution to 30, then varied the capacity _d_ max from 3 to 7. Fig. 3 (c) shows the results. Lazy BPRC shows smaller median runtime than both ablations, and also smaller min runtime than Non-Lazy BPRC. Lazy BPRC’s max runtime hits the time limit for _d_ max _≥_ 4. 

Note that No-Affine-Heuristic’s median runtime counterintuitively drops when we increase _d_ max from 6 to 7. This occurs because in two instances, runtime became more than 2 times smaller when we increased _d_ max; runtime did not change as significantly in the other 8 instances. The runtime dropped in these two instances for No-Affine-Heuristic because there were one or more tours whose evaluation required significant runtime for _d_ max = 6, but simply never needed to be evaluated for _d_ max = 7. 

## VIII. CONCLUSIONS 

In this paper, we introduced Lazy BPRC, a new algorithm to find optimal solutions for the MT-VRP-O, and we demonstrated its benefits via ablation studies. One direction for future work is to pursue bounded-suboptimal solutions to enable scaling to more targets. 

## REFERENCES 

- [1] C. S. Helvig, G. Robins, and A. Zelikovsky, “The moving-target traveling salesman problem,” _Journal of Algorithms_ , vol. 49, no. 1, pp. 153–174, 2003. 

- [2] C. D. Smith, _Assessment of genetic algorithm based assignment strategies for unmanned systems using the multiple traveling salesman problem with moving targets_ . University of Missouri-Kansas City, 2021. 

- [3] A. Stieber and A. F¨ugenschuh, “Dealing with time in the multiple traveling salespersons problem with moving targets,” _Central European Journal of Operations Research_ , vol. 30, no. 3, pp. 991–1017, 2022. 

- [4] J.-M. Bourjolly, O. Gurtuna, and A. Lyngvi, “On-orbit servicing: a time-dependent, moving-target traveling salesman problem,” _International Transactions in Operational Research_ , vol. 13, no. 5, pp. 461– 481, 2006. 

- [5] B. Li, B. R. Page, J. Hoffman, B. Moridian, and N. Mahmoudian, “Rendezvous planning for multiple auvs with mobile charging stations in dynamic currents,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 2, pp. 1653–1660, 2019. 

- [6] P. Toth and D. Vigo, _Vehicle routing: problems, methods, and applications_ . SIAM, 2014. 

- [7] C. Archetti, L. Coelho, M. Speranza, and P. Vansteenwegen, “Beyond fifty years of vehicle routing: Insights into the history and the future,” _European Journal of Operational Research_ , 2025. 

- [8] A. Bhat, G. Gutow, Z. Ren, S. Rathinam, and H. Choset, “Optimal solutions for the moving target vehicle routing problem via branch-and-price with relaxed continuity,” 2026. [Online]. Available: https://arxiv.org/abs/2603.00663 

- [9] M. Hammar and B. J. Nilsson, “Approximation results for kinetic variants of tsp,” in _Automata, Languages and Programming: 26th International Colloquium, ICALP’99 Prague, Czech Republic, July 11–15, 1999 Proceedings 26_ . Springer, 1999, pp. 392–401. 

- [10] L. Costa, C. Contardo, and G. Desaulniers, “Exact branch-price-andcut algorithms for vehicle routing,” _Transportation Science_ , vol. 53, no. 4, pp. 946–985, 2019. 

- [11] D. Feillet, “A tutorial on column generation and branch-and-price for vehicle routing problems,” _4or_ , vol. 8, no. 4, pp. 407–424, 2010. 

- [12] T. Marcucci, J. Umenberger, P. Parrilo, and R. Tedrake, “Shortest paths in graphs of convex sets,” _SIAM Journal on Optimization_ , vol. 34, no. 1, pp. 507–532, 2024. 

- [13] A. Bhat, G. Gutow, B. Vundurthy, Z. Ren, S. Rathinam, and H. Choset, “A complete and bounded-suboptimal algorithm for a moving target traveling salesman problem with obstacles in 3d*,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025, pp. 6132–6138. 

- [14] ——, “A complete algorithm for a moving target traveling salesman problem with obstacles,” in _International Workshop on the Algorithmic Foundations of Robotics_ . Springer, 2024. 

- [15] G. Ozbaygin, O. E. Karasan, M. Savelsbergh, and H. Yaman, “A branch-and-price algorithm for the vehicle routing problem with roaming delivery locations,” _Transportation Research Part B: Methodological_ , vol. 100, pp. 115–137, 2017. 

- [16] T. Asano, T. Asano, and H. Imai, “Shortest path between two simple polygons,” _Information processing letters_ , vol. 24, no. 5, pp. 285–288, 1987. 

- [17] M. Cui, D. D. Harabor, and A. Grastien, “Compromise-free pathfinding on a navigation mesh.” in _IJCAI_ , 2017, pp. 496–502. 

