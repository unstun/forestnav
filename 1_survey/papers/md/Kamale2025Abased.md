---
citation_key: Kamale2025Abased
arxiv_id: 2511.16844
arxiv_url: "https://arxiv.org/abs/2511.16844"
title: "A*-based Temporal Logic Path Planning with User Preferences on Relaxed Task Satisfaction"
authors_short: "Disha Kamale et al."
year: 2025
direction_tag: E_bounded_suboptimal_search
source: pymupdf4llm
converted_at: 2026-06-23T18:50:41Z
origin: ai+web
reviewed: false
---

# **A** _[∗]_ **-based Temporal Logic Path Planning with User Preferences on Relaxed Task Satisfaction** 

Disha Kamale, Xi Yu, Cristian-Ioan Vasile 

_**Abstract**_ **— In this work, we consider the problem of planning for temporal logic tasks in large robot environments. When full task compliance is unattainable, we aim to achieve the best possible task satisfaction by integrating user preferences for relaxation into the planning process. Utilizing the automata-based representations for temporal logic goals and user preferences, we propose an A** _[∗]_ **-based planning framework. This approach effectively tackles large-scale problems while generating nearoptimal high-level trajectories. To facilitate this, we propose a simple, efficient heuristic that allows for planning over large robot environments in a fraction of time and search memory as compared to uninformed search algorithms. We present extensive case studies to demonstrate the scalability, runtime analysis as well as empirical bounds on the suboptimality of the proposed heuristic.** 

## I. INTRODUCTION 

With the rapidly growing integration of robots into realworld applications, the need for time-efficient, sophisticated frameworks for successfully executing complex tasks is increasingly prominent. In this work, we consider the problem of planning for tasks expressed as temporal logic (TL) goals. TL formulations are particularly valuable due to their rich semantics, which enable precise articulation of complex requirements for robotic systems [1]–[4]. Traditionally, the problem of planning for TL specifications is approached using automata-based, sampling-based, optimization-based or learning-based techniques [5]–[9]. 

In this work, we are interested in designing a fast, scalable path-planning framework over large environments for given temporal logic specifications. A critical challenge in TL planning is that failing to meet even a minor sub-requirement can render the entire task infeasible. In such scenarios, it becomes crucial to still achieve meaningful satisfaction of the task as closely as possible. To facilitate this, we incorporate user preferences for relaxation of specifications into the planning framework. In the literature, various notions of relaxation including _maximizing probability of satisfaction [10], [11]_ , _deadline relaxation_ [12], _minimum revision_ , _minimum violation_ [5], _partial satisfaction_ [7], [13]. These methods often employ automata-based techniques, constructing explicit product automata for graph search to find optimal high-level trajectories. While this approach provides a clear notion of progress towards satisfaction, its scalability is limited when dealing with large environments or complex tasks. 

*This work was not supported by any organization 

Disha Kamale and Cristian-Ioan Vasile are with the Mechanical Engineering and Mechanics Department at Lehigh University, PA, USA, _{_ ddk320, cvasile _}_ @lehigh.edu 

Xi Yu is with the School of Manufacturing Systems and Networks at Arizona State University, AZ, USA, xyu@asu.edu 

For large robot environments, complex task specifications, and large number of user preferences, the runtime of path planning can rapidly increase. Several works consider the path planning problems over large environments utilizing techniques ranging from contraction hierarchies [14], sampling-based methods [2], [15] to hierarchical planning. Informed search algorithms such as A _[∗]_ have been found useful at efficiently solving these large-scale problems over discrete search spaces [13], [16]–[18]. However, the efficiency of A _[∗]_ depends largely on the heuristic function, which provides an estimate of the cost to reach the goal. The worstcase time and memory complexity of A _[∗]_ is exponential in depth of search. To address this, several variants, such as the weighted A _[∗]_ [19], [20], have been proposed to enhance search performance, though at the expense of optimality guarantees [21]. 

We propose a heuristic function for TL task planning that efficiently reduces the number of nodes explored to find a solution by leveraging the problem’s structure. The primary objective of this work is to develop a fast planning approach for robots deployed in large environments with syntactically co-safe Linear Temporal Logic (scLTL) tasks and user preferences on relaxed satisfaction in case of infeasibility. Similar to our previous works [6], [22], we represent the user preferences as a weighted-finite-state-edit system. By leveraging the abstractions to encapsulate robot motion, specification and user preferences, we propose a heuristic-based path planning framework. We trade-off optimality guarantees in planning for search efficiency, measured by the reduction in explored nodes and improved runtime performance. 

This work differs from closely related works [6], [13], [17], [22] in several aspects. In [6], we considered an explicit product automaton construction to handle multiple notions of relaxations. As opposed to the optimization-based approach in [22], this work considers a heuristic-based search method. In [17], the authors address the problem of TL planning, without allowing relaxations to the specification. In [13], the authors present an efficient A _[∗]_ -based approach to address TL planning with partial satisfaction. On the contrary, we consider multiple notions of relaxations such as minimum revision problem (MRP), minimum violation problem (MVP). 

The main contributions of this work are threefold: 1) We propose a heuristic-based planning algorithm for temporal logic tasks and user preferences for relaxation that achieves near-optimal trajectories. 2) We propose an efficient heuristic based on progress in the relaxed specification automaton which captures the specification and all user-preferred relaxations in case of infeasible sub-specifications 3) Our ex- 

tensive case studies demonstrate the efficacy of the proposed heuristic in terms of a significant improvement in memory and computation time across various examples. Moreover, we present the runtime analysis of the proposed heuristic with respect to different components of TL planning problem. **Notation** The symbols R, Z, and B represent the sets of real, integer, and binary numbers respectively. The set of integers greater than or equal to _a_ is denoted by Z _≥a_ . For a set _X_ , 2 _[X]_ and _|X|_ denote its power set and cardinality, respectively. If Σ is an alphabet, then Σ _[∗]_ represents the language consisting of all finite words over Σ. 

## II. PROBLEM SETUP 

In this section, we formally introduce the problem of temporal logic path planning with relaxation. We begin with a detailed description of models expressing the robot’s motion in the environment, the temporal logic task description as well as formal model encapsulating the user’s preferences for relaxation in case the original specification is infeasible. 

composes symbols from Σ = 2 _[AP]_ with logical and temporal operators with the following syntax: 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0002-04.png)


where, _π ∈ AP_ , _⊤_ denotes logical true value, _negation_ ( _¬_ ) and _conjunction_ ( _∧_ ) are Boolean operators while _next_ ( **X** ) and _until_ ( _U_ ) denote the temporal operators. Additional Boolean operators such as _disjunction_ ( _∨_ ) and temporal operators such as _eventually_ ( **F** ) can be derived using 1. Intuitively, the formula **X** _φ_ denotes that _φ_ holds true at the next step, **F** _φ_ indicates that _φ_ is satisfied at some point in the future, and _φ_ 1 _Uφ_ 2 denotes that _φ_ 1 is true until _φ_ 2 becomes true. For a detailed description of the syntax and semantics of scLTL, we refer the reader to [23]. 

Although the semantics of scLTL formulae is defined over infinite words, such as the ones produced by _T_ , its satisfaction can be decided in finite time enabled by _finite good prefixes_ [25]. An scLTL formula is said to be satisfied by trajectory **x** , denoted as **x** _|_ = _ϕ_ , if and only if the resulting output word satisfies _ϕ_ , i.e., **o** _|_ = _ϕ_ . 

## _A. Robot and Environment Model_ 

We consider a robot deployed in a fully known planar environment within which the robot can move deterministically. The environment may contain multiple labeled regions. We consider a finite abstraction of the robot’s motion in the environment as a weighted transition system, a widely followed approach in formal control synthesis [5], [23], [24]. 

_Definition 2.1 (Transition System):_ A weighted transition system (TS) is a tuple _T_ = ( _X, x[T]_ 0 _[, δ][T][, AP, ℓ, w][T]_[)][,][where] _X_ is a finite set of states indicating regions in the environment; _x[T]_ 0 _∈ X_ is the initial state; _δT ⊆ X × X_ is a set of transitions which captures the set of permissible robot movements in the environment; _AP_ is a set of labels (atomic propositions); _ℓ_ : _X → AP_ is a labeling function; _wT_ : _δT →_ R _≥_ 0 is a weight function. 

Note that in addition to transitions between regions, _δT_ also contains self-loop transitions, allowing the robot to stay stationary at any state _x ∈ X_ . The weight function _wT_ ( _xk, xk_ +1) represents path length from _xk_ to _xk_ +1. Naturally, traversing a self-loop incurs a cost of 0. 

As the robot moves through the environment, it generates a (potentially infinite) sequence of states **x** = _x_ 0 _, x_ 1 _. . ._ , referred to as a _trajectory_ (or run) of a robot, such that ( _xk, xk_ +1) _∈ δT_ for all _k ∈_ Z _≥_ 0 and _x_ 0 = _x[T]_ 0[.][When][the] robot is at a state _x_ labeled with _π ∈ AP_ , the atomic proposition _π_ is said to be true. The set of all trajectories of _T_ is _Runs_ ( _T_ ). A state trajectory **x** generates an _output trajectory_ **o** = _o_ 0 _o_ 1 _. . ._ , where _ok_ = _h_ ( _xk_ ) for all _k ≥_ 0. We also denote an output trajectory by **o** = _ℓ_ ( **x** ). The _(generated) language_ corresponding to a TS _T_ is the set of all generated output words, which we denote by _L_ ( _T_ ). We define the weight of a trajectory as _wT_ ( **x** ) =[�] _[|] k_ **[x]** =1 _[|][w][T]_[ (] _[x][k][−]_[1] _[, x][k]_[)][.] 

## _B. Temporal Logic Specification_ 

In this work, we use syntactically co-safe Linear Temporal Logic (scLTL) to formally define the robot tasks. scLTL 

## _C. User preferences for relaxation_ 

If part of the task specification _ϕ_ should become infeasible, the user relaxation preferences facilitate meaningful satisfaction of the task. 

_Definition 2.2 (User Relaxation Preference):_ Let _L_ be a language over the alphabet 2 _[AP]_ . A _user task preference_ is a pair ( _R, wR_ ), where _R ⊆ L ×_ (2 _[AP]_ ) _[∗]_ is a relation that captures how words in _L_ can be transformed to words from (2 _[AP]_ ) _[∗]_ and is of the form _σ �→[p] σ[′]_ where _σ ∈ L, σ[′] ∈_ (2 _[AP]_ ) _[∗]_ . _wR_ : _R →_ R represents the cost of the word transformations. The relation _R_ can also be understood as a multi-valued function _R_ : _L_ ⇒ (2 _[AP]_ ) _[∗]_ . 

_Example 2.1:_ Consider the task of picking up bread and ice-cream from a supermarket. The scLTL specification is _ϕ_ = ( **F** _breads_ ) _∧_ **F** _ice_ ~~_c_~~ _reams_ , where _breads_ and _ice_ ~~_c_~~ _reams_ are atomic propositions. If infeasible, the user-preferred relaxation options are 1) picking up bread from the nearest local bakery for a penalty of 5, 2) picking up ice cream from the nearest shop for a penalty of 7, 3) removing ice-cream from the list for a penalty of 12. The formal representation for these preferences is 1) _breads �→_[5] _breadbakery,_ 2) _ice_ ~~_c_~~ _reams �→_[7] _ice_ ~~_c_~~ _reamshop,_ 3) _ice_ ~~_c_~~ _reams �→_[12] _ϵ_ . Note that (1) and (2) are instances of MRP while (3) is an instance of MVP. 

## _D. Problem definition_ 

The problem of optimal temporal logic path planning with relaxation is defined as follows. 

_Problem 2.1 (Optimal TL Path Planning with Relaxations):_ Given the robot motion abstraction as a weighted transition system _T_ , an scLTL task specification _ϕ_ as well as user preferences for relaxation ( _R, wR_ ), find a path **˜x** in _T_ that satisfies the specification _ϕ_ while only performing necessary relaxations and minimizes the cost of the trajectory. 

Formally, 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0003-01.png)


**o** _[relax]_ = _ℓ_ ( **x** ) _,_ ( **o** _,_ **o** _[relax]_ ) _∈ R_ (Relaxation preferences) where _λ_ represents a blending parameter, **o** _[relax]_ = _ℓ_ ( **x** ) denotes the output word of the _T_ , and **o** _∈_ (2 _[AP]_ ) _[∗]_ is a word satisfying _ϕ_ . 

## III. APPROACH 

In this section, we elaborate on our approach to Problem 2.1 which involves several key steps. Given the task specification and user preferences for relaxation, we begin by converting them into automata. This facilitates the construction of a _Relaxed Satisfaction Automaton_ , introduced in [22], which efficiently encapsulates the original task specification and all user-preferred relaxations along with their associated penalties. The primary advantage this offers is that the progress toward task satisfaction can be explicitly considered even in the case of infeasible sub-specifications. Building upon this representation, we present the A _[∗]_ -based search algorithm for temporal logic planning with relaxations, which is the main contribution of this work. Finally we present a discussion on practical considerations regarding the design of the heuristic for TL planning. 

## _A. Automata models for temporal logic_ 

Any scLTL formula _ϕ_ can be translated [26] into a deterministic _finite state automaton_ (FSA) which accepts the set of all good prefixes of all words that satisfy _ϕ_ [25], defined as follows. 

_Definition 3.1 (Deterministic Finite State Automaton):_ A deterministic finite state automaton (DFA) is a tuple _Aϕ_ = ( _SAϕ, s[A]_ 0 _[ϕ][,]_[ Σ] _[, δ][A] ϕ[, F][A] ϕ_[)][,][where:] _[S][A] ϕ_[is][a][finite][set] of states; _s[A]_ 0 _[ϕ] ∈ SAϕ_ is the initial state; Σ is the input alphabet; _δAϕ_ : _SAϕ ×_ Σ _→ SAϕ_ is the transition function; _FAϕ ⊆ SAϕ_ is the set of accepting states. 

A trajectory of the DFA **s** = _s_ 0 _s_ 1 _. . . sn_ +1 is generated by a finite sequence of symbols _**σ**_ = _σ_ 0 _σ_ 1 _. . . σn_ where _s_ 0 = _s[A]_ 0 _[ϕ]_ is the initial state of _Aϕ_ and _sk_ +1 = _δAϕ_ ( _sk, σk_ ) for all 0 _≤ k ≤ n_ . This trajectory is said to be accepting if _sk_ +1 _∈ FAϕ_ . The _(accepted) language_ of a DFA _Aϕ_ is the set of accepted input words denoted by _L_ ( _Aϕ_ ). Thus, in order to ensure the satisfaction of a formula _ϕ_ by a trajectory **x** in environment _T_ , it is necessary that **o** = _ℓ_ ( **x** ) _∈LAϕ_ . 

In order to handle infeasibilities in _ϕ_ , the user preferences for relaxation are converted into a weighted finite state edit system defined as follows: 

_Definition 3.2 (Weighted Finite State Edit System):_ A weighted finite state edit system (WFSE) is a weighted DFA _E_ = ( _ZE , z_ 0 _[E][,]_[ Σ] _[E][, δ][E][, F][E][, w][E]_[)][,] where Σ _E_ = �2 _[AP] ∪{ϵ}_ � _×_ �2 _[AP] ∪{ϵ}_ � _\ {_ ( _ϵ, ϵ_ ) _}_ , _ϵ_ denotes a missing or deleted symbol, and _wE_ : _δE →_ R is the transition weight function. 

The alphabet Σ _E_ captures word edit operations such as addition, substitution, or deletion of symbols. A transition _z[′]_ = _δE_ ( _z,_ ( _σ, σ[′]_ )) has input, output symbols _σ_ and _σ[′]_ . 

**Remark:** We add pass-through transitions to the WFSE with 0 weights to ensure that the satisfaction is not relaxed if the entire original specification is feasible. 

_Example 3.1 (Continuation of Example 2.1):_ Consider states _z, z[′] ∈ ZE_ . Preference 1 can be captured by states _z, z[′]_ such that _z[′] ∈_ ( _z, δE_ ( _σ, σ[′]_ )) where _σ_ is the input symbol such that _breads ∈ σ_ , _σ[′]_ denotes the output symbol _breadbakery ∈ σ[′]_ and _wE_ ( _z,_ ( _σ, σ[′]_ ) _, z[′]_ ) = 5. 

## _B. Relaxed Specification Product Automaton_ 

All permissible relaxations of the scLTL specification _ϕ_ are captured using a product non-deterministic finite state automaton [22] between the DFA _Aϕ_ and the WFSE _E_ . _Definition 3.3 (Relaxed Specification Automaton):_ Given a specification DFA _Aϕ_ = ( _SAϕ, s[A]_ 0 _[ϕ][,]_[ Σ] _[, δ][A] ϕ[, F][A] ϕ_[)][,] the user task preferences represented as a WFSE _E_ = ( _ZE , z_ 0 _[E][,]_[ Σ] _[E][, δ][E][, F][E][, w][E]_[)][,][the][relaxed][specification] automaton is a tuple _A_ = ( _QA, qA_[0] _[,]_[ Σ] _[A][, δ][A][, F][A][, w][A]_[)][,] where _QA_ = _ZE × SAϕ_ represents the state space; _q_ 0 _[A]_ = ( _z_ 0 _[E][, s][A]_ 0 _[ϕ]_[)][is][the][initial][state;][Σ] _[A]_[=][Σ] _[A] ϕ_[denotes] the alphabet; _δA ⊆ QA ×_ Σ _A × QA_ is a transition relation; _FA_ = _FE × FAϕ ⊆ QA_ represents the set of final (accepting) states; _wA_ : _δA →_ R _≥_ 0 is the weight function where _wA_ ( _q, q[′]_ ) = _wE_ ( _z, z[′]_ ). 

We direct the reader to [22] for the relaxed satisfaction automaton construction. 

## _C. Heuristic-based for TL planning with relaxation_ 

For A _[∗]_ search on an arbitrary graph, the cost of node _n_ is given as _f_ ( _n_ ) = _g_ ( _n_ ) + _h_ ( _n_ ). Thus, the cost computation utilizes two components of information: 1) the distance already covered to reach node _n_ from some initial node _n_ 0, and 2) an estimated cost to reach a final node _nf_ from node _n_ . The function _f_ ( _·_ ) is often referred to as the _f-score_ of node _n_ . The search continues by exploring the nodes with best _f-scores_ until _nf_ is reached. The solution obtained by A _[∗]_ is guaranteed to be optimal if the heuristic is an underestimation of the actual cost to reach the goal for all nodes. The informativeness of the heuristic directly impacts the efficiency of the search. 

For TL planning, designing such an informative heuristic is challenging. Unlike the traditional graph search problems where the final node _nf_ is given, temporal logic tasks may require visiting multiple regions in the environment, where each visit to a location containing a desired label (atomic proposition) results in progress towards task satisfaction in the specification automaton. Potentially, the same atomic proposition could be satisfied at multiple locations in the environment. Thus, the state in the environment that results into reaching a final state in the specification automaton cannot be uniquely specified. 

**Heuristic** We consider the distance to satisfaction in the relaxed satisfaction automaton scaled by a factor _γ_ . Since _A_ contains multiple final states _q ∈ FA_ , we add a virtual final state _q[▷◁]_ to _A_ with only incoming edges _{_ ( _q, q[▷◁]_ ) _|q ∈ FA}_ . The heuristic value for node ( _x, q_ ) is, 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0003-21.png)


where _dmin_ ( _q, q[′]_ ) denotes the minimum distance between nodes _q_ and _q[′]_ in _A_ . The search is performed over the solution space consisting of _T_ and _A_ . Note that, we avoid the explicit product construction and instead only enumerate the reachable states in this space by keeping track of labels of _T_ and the resulting transitions in _A_ . Given a sequence of states (( _x_ 0 _, q_ 0) _,_ ( _x_ 1 _, q_ 1) _, . . . ,_ ( _xk, qk_ )), the graph distance for node ( _xk_ +1 _, qk_ +1) is 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0004-01.png)


Alg. 1 outlines the search algorithm for TL planning with relaxation. Given the input _T , Aϕ_ and _E_ , we construct the relaxed product automaton using the algorithm from [22] (line 2). The initial node ( _x[T]_ 0 _[, q] A_[0][)][ is added to the] _[ queue]_[ to be] processed. For node ( _x, q_ ), the _f-score_ is given by _f_ ( _x, q_ ) = _g_ ( _x, q_ )+ _h_ ( _x, q_ ) where _g_ ( _x, q_ ) is the graph distance of node _x_ from the initial node in _T_ and a graph distance in _Aϕ_ as in (3) and _h_ ( _x, q_ ) is obtained from (2). The _queue_ keeps track of the _f-score_ , current node, graph distances, and parent nodes. Given the current state ( _x, q_ ), all neighbors of _x_ in _T_ and the corresponding generated input symbols inform the next states _q[′]_ in _A_ leading to a new state ( _x[′] , q[′]_ ) in the solution space (lines 10-11). If unexplored, this node is investigated for graph score _g_ ¯ and heuristic value. If the current path to ( _x, q_ ) from source is shorter than a previously stored path to ( _x, q_ ), we update the _gscore_ set. The _queue_ is updated with node ( _x, q_ ) and the associated information. Upon reaching the final state in _A_ , the search stops and the resulting trajectory in the solution space is obtained using the stored parent nodes. Finally the _path_ is projected onto the robot environment to obtain the trajectory in the robot environment, denoted by **x** = _path⊥T_ (lines 6-8), where _⊥_ ( _·_ ) is the projection operator with _⊥_ ( _xk, qk_ ) = _xk_ . If the final state in _A_ cannot be reached, the routine returns infeasibility. 

## **Algorithm 1:** _A[∗] -based search for TL relaxation()_ 

||**Input:** _T , ϕ, E, γ_|**Input:** _T , ϕ, E, γ_|**Input:** _T , ϕ, E, γ_||||
|---|---|---|---|---|---|---|
||**Result: x**||||||
|**1**|Initialize _queue ←∅_, _explored ←∅, g_<br>_scores ←∅_||||||
|**2**|_A_||= construct<br>~~_A_~~(_E, Aϕ_)|using|[22]||
|**3**|_g_||~~_s_~~_cores ←{_(_xT_<br>0 _, q_0<br>_A_) = 0_}, queue ←_(0_,_(_xT_<br>0 _, q_0<br>_A_)_,_0_, None_)||||
|**4 **|**while** _queue _= _∅_**do**||||||
|**5**|||(_x, q_) _←queue.pop_()||||
|**6**|||**if** _q ∈FA_ **then**||||
|**7**|||reconstruct _path_ = ((_xT_<br>0 _, q_0<br>_A_)_, ._|_. . ,_(_x, q_)) return _path⊥T_|||
|**8**|||**if** (_x, q_) _in explored_ **then** continue||||
|**9**|||_explored ←_(_x, q_)||||
|**10**|||**forall** (_x, x′_) _∈δT_ **do**||||
|**11**|||**forall** (_q,_(_ℓ_(_x′_)_, σ′_)_, q′_) _∈δA_ **do**||||
|**12**|||**if** (_x′, q′_) _in explored_ **then**||||
|**13**|||continue||||
|**14**|||¯_g ←g_<br>~~_s_~~_cores_(_x, q_) +_wT_|(_x, x′_) +||_λ · wA_(_q, q′_) 3|
|**15**|||_h_(_x′, q′_) _←get_<br>~~_h_~~_euristic_(_q, q′_)|||2|
|**16**|||**if** (_x′, q′_) _∈g_<br>~~_s_~~_cores_ **then**||||
|**17**|||**if** _g_<br>_scores_(_x′, q′_) _<_|¯_g_ **then** continue|||
|**18**|||**else** _g_<br>~~_s_~~_cores_(_x′, q′_) _←_¯_g_||||
|**19**|||_queue ←_((¯_g_+_h_(_qA, q′_)_,_(_x′, q′_)_,_¯_g,_(_x, q_)))||||
||||||||
|**20**|||return _Infeasible_||||



_Lemma 3.1 (correctness):_ The solution given by the proposed search algorithm always satisfies the specification. i.e., **˜o** _[relax]_ = _h_ (˜ **x** ) _|_ = _ϕ_ . 

_Proof:_ Follows by construction and the stopping criterion the Alg. 1. 

## _D. Heuristic discussion_ 

The explicit product computation scales multi-linearly with _|T |_ , _|Aϕ|_ and _|E|_ restricting the scalability due to the exhaustive search of the reachable space for solutions. By implicitly enumerating the states in the solution space, the proposed search algorithm Alg. 1 offers a significant improvement in terms of runtime and memory even with zero heuristic. 

Further improvement in search performance can be achieved by carefully crafting a heuristic function that balances informativeness and computational efficiency. While a highly informative heuristic can reduce the number of explored nodes, it may worsen overall performance due to increased computational cost compared to simple node expansion. For instance, consider the runtime and search results in Fig. 1. _hinfo_ refers to an informative heuristic which takes into account the symbol _σ_ needed to transition closer to the final state in _A_ and computes the distance to one of the nodes in the environment that contains this symbol. As shown in Fig. 1, even though _hinfo_ reduces the number of nodes explored, it significantly increases the runtime due to complex computations involved at each step. A commonly followed approach to circumvent this problem involves precomputing the necessary values. With slight changes to the problem setting, repeating these precomputations can quickly become impractical for large scale environments. 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0004-10.png)


Fig. 1. Runtime, memory, and precomputation time for _h_ = 0 _, hinfo_ and proposed heuristic _h_ . 

## IV. CASE STUDIES 

In this section, we show the functionality of the proposed search algorithm, a comparison with a baseline uninformed search, and a runtime analysis. These studies were performed on Dell Precision 3640 Intel i9 with 64 GB RAM using Python 3.9.7. For all following studies, we set _λ_ = 1. 

## _A. Functionality_ 

**Empirically determining the scaling factor** . To determine the value of _γ_ for a given problem, we consider a fixed problem setup by keeping the environment size, labeled locations, specifications and relaxation preference unchanged across iterations. Thus, the same problem instance is solved for different values of _γ_ . We assess the resulting cost, runtime as well as number of nodes searched in the solution space. 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0005-00.png)


Fig. 2. Trajectories obtained using baseline and the proposed heuristic. Nodes with atomic propositions of interest are shown in yellow. 

Fig. 3 shows one such example for a grid environment of size (50,50) for a task of visiting 5 locations in no specific order, _ϕ_ = **F** _a∧_ **F** _b∧_ **F** _c∧_ **F** _d∧_ **F** _e_ . We choose _γ_ = 4 since it corresponds to an optimal cost while reducing the time and memory usage considerably. The choice of _γ_ is thus a design decision that balances the trade-off between computational cost and search efficiency. 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0005-03.png)


Fig. 3. Empirical determination of the scaling factor 

**TL planning** . It is important to note that the potential sub-optimality of the proposed heuristic does not affect the precise satisfaction of the temporal logic goals. In this case study, we aim to compare the trajectories given by the proposed approach with a baseline case of zero heuristic (uninformed search) denoted by _h_ 0. The baseline is guaranteed to find an optimal solution for the given environment and specification. However, the optimal solution may not be unique. 

Consider a 20x20 grid environment given as a weighted transition system _T_ with seven atomic propositions (labels) _AP_ = _{a, b, c, d, e, h, i}_ . Each transition has a unit weight and the self-loop transitions incur zero cost. The task specification is _ϕ_ = ( **F** _a ∧_ ( **F** ( _b ∧_ **F** _c_ )) _∧_ ( **F** ( _d ∧_ **F** _e_ )) _∧_ **F** _h ∧_ ( _¬ i U h_ )). In plain English, this translates to _“At some point in the future, visit a followed by b then visit c. Visit d followed by e. Visit h and do not visit i until h is visited.”_ Notice that the specification does not impose any ordering on _a_ , _d_ and _h_ . Thus, there are multiple possible ways in which the specification can be satisfied in _T_ . 

For evaluating our approach, we set _γ_ = 15 and the initial state to (0 _,_ 0). The atomic propositions are then randomly assigned to the nodes in _T_ . As shown in Fig. 2, our approach provides at least an order of magnitude speedup in runtime and reduction of nodes explored. As expected, in some cases, this speedup is achieved at a cost of optimality (Fig. 2(b)). 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0005-08.png)


Fig. 4. Trajectories with relaxation obtained using baseline and the proposed heuristic. The green circles indicate satisfaction of a minimally relaxed subspecification. The red circle denotes a sub-optimal relaxation. 

Compared to _h_ 0, our heuristic finds an optimal solution with 93.5% reduction in time, 93.2% reduction in memory for scenario 1 and a close-to-optimal solution for 94% reduction in time, 93% reduction in memory for scenario 2. 

**Relaxation** For the same specification, if labels _b_ and _e_ are not present in the environment, the user preferences are (1) MRP: in place of _b_ , _k_ can be visited with a penalty of 3, (2) MRP: instead of _b_ , _j_ can be visited while incurring a penalty of 5, (3) MVP: visit to _e_ can be canceled with a penalty of 2. In other words, 1) _b �→_[3] _k_ , 2) _b �→_[5] _j_ , 3) _e �→_[2] _ϵ_ . We set _γ_ = 15. The resulting trajectories are shown in Fig. 4. As depicted in scenario 1, the proposed heuristic finds an optimal path by substituting for _b_ with the lowest revision penalty and violating _e_ for the minimum violation penalty with 92.6% and 92.13% improvements in time and memory respectively. On the other hand, for scenario 2, our approach yields a sub-optimal path by using a relaxation preference with higher penalty resulting in a cost overhead of 16 while improving the time and memory usage by 91.8% and 90.4% compared to _h_ 0. 

## _B. Large Scale Robot Environments_ 

To showcase the computational efficiency of the proposed heuristic, we use the New York City motorways network from OSMNX [27] consisting of 378,040 nodes and 1,131,664 edges as _T_ . We consider three representative cases: 1) sparse locations by considering only 3 labeled locations in the entire environment to be visited sequentially, 

TABLE I 

COMPARISON W.R.T. BASELINE FOR LARGE SCALE ROBOT ENVIRONMENT 

|**Specifcation**|**Solution**<br>**Space Size**|_|_**AP**_|_|_γ_|**Precomp.**<br>**Time (ms)**|**Runtime (s)**|**Nodes**<br>**searched**|**Nodes**<br>**searched**|**Cost**|**Cost**|
|---|---|---|---|---|---|---|---|---|---|
|_ϕ_1|nodes: 1512160<br>edges: 11316640|3|-<br>_γ_1 = 27000|-<br>0.11|8.34 (_h_0)<br>3.83|689193(_h_0)<br>326860||43151.37(_h_0)<br>43151.37||
|_ϕrelax_<br>1|nodes: 4536480<br>edges: 45266560|4|_γ_1 = 27000|0.11|147(_h_0)<br>114|844181(_h_0)<br>649860|||67546(_h_0)<br>67546|
|_ϕ_2|nodes: 13609440<br>edges: 298759296|7|-<br>_γ_21 = 500<br>_γ_22 = 800|-<br>1.1<br>1.1|28(_h_0)<br>10.8<br>6.58|1643956(_h_0)<br>669695<br>460877|||28996(_h_0)<br>28996<br>33654|
|_ϕrelax_<br>2|nodes: 40828320<br>edges: 1195037184|9|-<br>_γ_21 = 500<br>_γ_22 = 800|-<br>1.9<br>1.7|233.8(_h_0)<br>68.3<br>44.98|1364344(_h_0)<br>611298<br>422999||22746.3(_h_0)<br>22766.5<br>29973.8||
|_ϕ_3|nodes: 18145920<br>edges: 611098560|8|-<br>_γ_31 = 2000<br>_γ_32 = 5000|-<br>2.8<br>2.76|237.17 (_h_0)<br>53.04<br>16.87|13|941839 (_h_0)<br>3757966<br>1216287|81844(_h_0)<br>81850<br>84446||
|_ϕrelax_<br>3|nodes: 54437760<br>edges: 2444394240|9|-<br>_γ_31 = 2000<br>_γ_32 = 5000|-<br>4.73<br>4.78|2957.40(_h_0)<br>520.96<br>269.6|20333049(_h_0)<br>4493701<br>2507799||78199(_h_0)<br>94626.48<br>94626.48||




![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0006-03.png)


Fig. 5. a) Effect of randomized AP assignment, b) Effect of varying _T_ size 2) a complex grouping of tasks with choices, and 3) a complex sequential task. The scLTL specifications are: 1) _ϕ_ 1 = ( **F** ( _groceries ∧_ **F** ( _fuel ∧_ **F** _bakery_ ))) 

- 2) _ϕ_ 2 = (( **F** _lunch ∧_ **F** ( _groceries ∨ coffee_ ) _∧_ **F** _bakery_ ) _∨_ ( **F** _fuel ∧_ **F** ( _breakfast ∧_ ( **F** _bookstore_ )))) 

- 3) _ϕ_ 3 = ( **F** _lunch ∧_ **F** ( _groceries ∧_ **F** _coffee_ ) _∧_ **F** _bakery∧_ **F** ( _fuel ∧_ **F** ( _breakfast∧_ ( **F** _bookstore_ ))) _∧_ ( _¬ rest U bakery_ )) 

Additionally, the user preferences for relaxation in case of infeasibility are _fuel �→_[5] _rest_ for _ϕ_ 1; _bakery �→_[5] _mall, coffee �→_[3] _lunch_ for _ϕ_ 2 and _ϕ_ 3. Table I summarizes the results. We denote by _ϕ[relax] i_ the cases wherein relaxation is taken into account. The solution space size refers to the total number of nodes and edges given by _|X|×|SAϕ|×|ZE |_ and _|δT | × |δAϕ| × |δE |_ . It is crucial to note that we do not explicitly construct the solution space. _|AP |_ denotes the number of locations allocated in the environment. As evident from these results, the proposed heuristic is simple enough to be pre-computed in a few milliseconds while drastically improving the search and runtime performance for a city-scale robot environment for complex tasks. Moreover, it can be seen that some values of _γ_ achieve the optimal cost in a fraction of time and memory as compared to the baseline ( _γ_ 1 _, γ_ 21 _, γ_ 31). Increasing this scaling factor further may improve the search time and memory considerably but may worsen the cost incurred ( _γ_ 22 and _γ_ 32). 

## _C. Runtime analysis_ 

**Randomized locations** For a 50x50 grid environment and _ϕ_ = **F** _a∧_ **F** _b∧_ **F** _c∧_ **F** _d∧_ **F** _e_ , and _γ_ = 4, we vary the number of locations of each type (atomic proposition) and randomly assign minimum 1 and maximum 4 instances of each label. This gives rise to multiple possible paths that satisfy _ϕ_ with varying path lengths. The results are shown in Fig. 5(a). For 


![](1_survey/papers/md/Kamale2025Abased_figs/Kamale2025Abased.pdf-0006-09.png)


Fig. 6. Relative error between the cost for the proposed heuristic and the optimal cost 

some problem instances, our approach chooses the labeled states in the environment that can be reached faster, albeit at a slightly higher cost. 

**Environment size** For the same _ϕ_ and _γ_ = 10, we vary the environment size from a 25 states to 30000 states. The scaling factor is substantially smaller due to simpler structure of the specification. The improvement in runtime (and reduction of nodes explored) increases consistently with the increasing environment size and is more pronounced for larger environments as shown in Fig. 5(b). Notably, except for a few cases between _|X|_ = 5000 and _|X|_ = 10000, the proposed heuristic achieves the optimal cost across all remaining instances. 

## _D. Empirical study on bounded suboptimality_ 

We consider a 100x100 grid environment wherein a robot is tasked to perform _ϕ_ = ( **F** _a ∧_ ( **F** ( _b ∧_ **F** _c_ )) _∧_ ( **F** ( _d ∧_ **F** _e_ )) _∧_ **F** _h ∧_ ( _¬iUh_ )). Varying _γ_ from 0 to 30000, we compare the relative error ∆ in cost _J_[ˆ] ( **x** ) between the baseline and proposed approaches where ∆= ( _J_[ˆ] _h − J_[ˆ] _h_ 0) _/J_[ˆ] _h_ 0. The results are depicted in Fig. 6. This study underscores that the suboptimality of the proposed heuristic is bounded and the approximate empirical bound is _J_[ˆ] _h ≤_ 1 _._ 5 _J_[ˆ] _h_ 0. 

## V. CONCLUSION 

This work presents an A _[∗]_ -based search algorithm for planning for temporal logic tasks and user preferences for relaxation to address potential infeasibilities. The proposed approach avoids explicit product construction and instead implicitly searches through the reachable solution space. To facilitate this search, we propose an efficient, practicable 

heuristic that informs the search based on the distance from satisfaction with respect to the relaxed TL task. The proposed heuristic significantly reduces memory usage and runtime while achieving near-optimal costs. We provide runtime analysis and empirical suboptimality bounds. Future work will focus on a deeper investigation of the algorithm’s theoretical properties and rigorous suboptimality bounds. 

## REFERENCES 

- [1] G. E. Fainekos, H. Kress-Gazit, and G. J. Pappas, “Hybrid controllers for path planning: A temporal logic approach,” in _Proceedings of the 44th IEEE Conference on Decision and Control_ . IEEE, 2005, pp. 4885–4890. 

- [2] C. I. Vasile and C. Belta, “Sampling-based temporal logic path planning,” in _2013 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2013, pp. 4817–4822. 

- [3] L. Lindemann and D. V. Dimarogonas, “Robust control for signal temporal logic specifications using discrete average space robustness,” _Automatica_ , vol. 101, pp. 377–387, 2019. 

- [4] S. L. Smith, J. Tumova, C. Belta, and D. Rus, “Optimal path planning for surveillance with temporal-logic constraints,” _The International Journal of Robotics Research_ , vol. 30, no. 14, pp. 1695–1708, 2011. 

- [5] C.-I. Vasile, J. Tumova, S. Karaman, C. Belta, and D. Rus, “Minimumviolation scltl motion planning for mobility-on-demand,” in _2017 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2017, pp. 1481–1488. 

   - [19] I. Pohl, “Heuristic search viewed as path finding in a graph,” _Artificial intelligence_ , vol. 1, no. 3-4, pp. 193–204, 1970. 

   - [20] A. Felner, S. Kraus, and R. E. Korf, “Kbfs: K-best-first search,” _Annals of Mathematics and Artificial Intelligence_ , vol. 39, pp. 19–39, 2003. 

   - [21] R. Ebendt and R. Drechsler, “Weighted a search–unifying view and application,” _Artificial Intelligence_ , vol. 173, no. 14, pp. 1310–1342, 2009. 

   - [22] D. Kamale and C.-I. Vasile, “Optimal control synthesis with relaxed global temporal logic specifications for homogeneous multi-robot teams,” _arXiv preprint arXiv:2406.01848_ , 2024. 

   - [23] C. Baier and J.-P. Katoen, _Principles of model checking_ . MIT press, 2008. 

   - [24] T. Wongpiromsarn, U. Topcu, and R. M. Murray, “Receding horizon temporal logic planning,” _IEEE Transactions on Automatic Control_ , vol. 57, no. 11, pp. 2817–2830, 2012. 

   - [25] O. Kupferman and M. Y. Vardi, “Model checking of safety properties,” _Formal methods in system design_ , vol. 19, pp. 291–314, 2001. 

   - [26] A. Duret-Lutz, A. Lewkowicz, A. Fauchille, T. Michaud, E. Renault, and L. Xu, “Spot 2.0 — a framework for LTL and _ω_ -automata manipulation,” in _Proceedings of the 14th International Symposium on Automated Technology for Verification and Analysis (ATVA’16)_ , ser. Lecture Notes in Computer Science, vol. 9938. Springer, Oct. 2016, pp. 122–129. 

   - [27] G. Boeing, “Osmnx: A python package to work with graphtheoretic openstreetmap street networks,” _Journal of Open Source Software_ , vol. 2, no. 12, p. 215, 2017. [Online]. Available: https://doi.org/10.21105/joss.00215 

- [6] D. Kamale, E. Karyofylli, and C.-I. Vasile, “Automata-based optimal planning with relaxed specifications,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 6525–6530. 

- [7] G. A. Cardona and C.-I. Vasile, “Partial satisfaction of signal temporal logic specifications for coordination of multi-robot systems,” in _International Workshop on the Algorithmic Foundations of Robotics_ . Springer, 2022, pp. 223–238. 

- [8] K. Leung, N. Ar´echiga, and M. Pavone, “Backpropagation through signal temporal logic specifications: Infusing logical structure into gradient-based methods,” _The International Journal of Robotics Research_ , vol. 42, no. 6, pp. 356–370, 2023. 

- [9] M. Cai, E. Aasi, C. Belta, and C.-I. Vasile, “Overcoming exploration: Deep reinforcement learning for continuous control in cluttered environments from temporal logic specifications,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 4, pp. 2158–2165, 2023. 

- [10] M. Lahijanian, S. B. Andersson, and C. Belta, “Temporal logic motion planning and control with probabilistic satisfaction guarantees,” _IEEE Transactions on Robotics_ , vol. 28, no. 2, pp. 396–409, 2011. 

- [11] H. Rahmani, A. N. Kulkarni, and J. Fu, “Probabilistic planning with partially ordered preferences over temporal goals,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 5702–5708. 

- [12] C.-I. Vasile, D. Aksaray, and C. Belta, “Time window temporal logic,” _Theoretical Computer Science_ , vol. 691, pp. 27–54, 2017. 

- [13] P. Amorese and M. Lahijanian, “Optimal cost-preference trade-off planning with multiple temporal tasks,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 2071–2077. 

- [14] Y. Wang, Y. Yuan, H. Wang, X. Zhou, C. Mu, and G. Wang, “Constrained route planning over large multi-modal time-dependent networks,” in _2021 IEEE 37th International Conference on Data Engineering (ICDE)_ . IEEE, 2021, pp. 313–324. 

- [15] Y. Kantaros and M. M. Zavlanos, “Stylus*: A temporal logic optimal control synthesis algorithm for large-scale multi-robot systems,” _The International Journal of Robotics Research_ , vol. 39, no. 7, pp. 812– 836, 2020. 

- [16] M. Likhachev, G. J. Gordon, and S. Thrun, “Ara*: Anytime a* with provable bounds on sub-optimality,” _Advances in neural information processing systems_ , vol. 16, 2003. 

- [17] D. Khalidi, D. Gujarathi, and I. Saha, “T: A heuristic search based path planning algorithm for temporal logic specifications,” in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , 2020, pp. 8476–8482. 

- [18] S. Bhattacharya, M. Likhachev, and V. Kumar, “Multi-agent path planning with multiple tasks and distance constraints,” in _2010 IEEE International Conference on Robotics and Automation_ . IEEE, 2010, pp. 953–959. 

