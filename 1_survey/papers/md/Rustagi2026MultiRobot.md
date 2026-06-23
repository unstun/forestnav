---
citation_key: Rustagi2026MultiRobot
arxiv_id: 2603.13748
arxiv_url: "https://arxiv.org/abs/2603.13748"
title: "Multi-Robot Coordination for Planning under Context Uncertainty"
authors_short: "Pulkit Rustagi et al."
year: 2026
direction_tag: G_subgoal_optimization
source: pymupdf4llm
converted_at: 2026-06-23T17:52:22Z
origin: ai+web
reviewed: false
---

## **Multi-Robot Coordination for Planning under Context Uncertainty** 

Pulkit Rustagi[1] , Kyle Hollins Wray[2] and Sandhya Saisubramanian[1] 

_**Abstract**_ **— Real-world robots often operate in settings where objective priorities depend on the** _**underlying context**_ **of operation. When the underlying context is unknown apriori, multiple robots may have to coordinate to gather informative observations to infer the context, since acting based on an incorrect context can lead to misaligned and unsafe behavior. Once the underlying true context is inferred, the robots optimize their task-specific objectives in the preference order induced by the context. We formalize this problem as a** _**MultiRobot Context-Uncertain Stochastic Shortest Path**_ **(MR-CUSSP), which captures context-relevant information at landmark states through joint observations. Our two-stage solution approach is composed of: (1)** _**CIMOP**_ **(Coordinated Inference for MultiObjective Planning) to compute plans that guide robots toward informative landmarks to efficiently infer the true context, and (2)** _**LCBS**_ **(Lexicographic Conflict-Based Search) for collisionfree multi-robot path planning with lexicographic objective preferences, induced by the context. We evaluate the algorithms using three simulated domains and demonstrate its practical applicability using five mobile robots in the salp domain setup.** 

## I. INTRODUCTION 

Multi-robot systems in the real world must often perform multi-objective planning for task completion and robot coordination. The preference ordering over objectives is often determined by the _underlying context_ of operation [1], [2], [3], defined based on factors such as resource availability, geographic, or temporal aspects of the environment. For example, salp-inspired underwater robots [4] must prioritize minimizing ecological disturbance in coral zones over energy and speed. In areas of strong eddy currents, they must prioritize stability and energy conservation over speed. 

When robots do not have prior knowledge of the exact underlying context, they must actively gather information before task execution, as operating under an incorrect context can lead to inefficient coordination or unsafe behavior [5], [6], [7], [8]. Crucially, in many settings such as salps and disaster rescue [1], informative observations require _joint sensing_ in certain configurations. For example, distinguishing between a coral zone and an eddy current zone requires multiple robots to form a ring around the crevice and perform synchronized measurements of flow and particulates. Individual measurements can only measure local velocity and particulate concentration and are insufficient to infer global circulation patterns. Moreover, robots may need to repeatedly form specific configurations (e.g., ring, chain, star) to obtain context-revealing observations (Fig. 1). This motivates our 

> 1Collaborative Robotics and Intelligent Systems (CoRIS) Institute, Oregon State University, Corvallis, OR 97331, USA rustagip, sandhya.sai@oregonstate.edu 

> 2Khoury College of Computer Sciences, Northeastern University, Boston, MA 02115, USA k.wray@northeastern.edu 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0001-09.png)


Fig. 1: Illustration of multiple GTernal robots [9] with a shared belief over true context. Accurate context-relevant observations are available only when robots are in a required configuration at a landmark (e.g., chain at _ℓ_ 1 and ring at _ℓ_ 2). After context inference, robots compute plans aligned with the context-induced objective preferences to reach their goal. 

key question: _how to effectively coordinate multiple robots to infer the underlying context to enable computing collisionfree paths that optimize context-dependent objective preferences_ ? 

Existing approaches to preference-based planning typically assume that the relevant preference ordering is known a priori, and do not model its dependence on latent context that must be inferred from observations [10]. A common alternative is to compute a Pareto frontier over the objectives when their preference ordering is unknown, as widely used in multi-objective multi-agent path finding (MO-MAPF) works [11], [12], [13]. However, selecting a solution from the Pareto frontier for execution ultimately requires knowledge of the true context. Meanwhile, planning approaches that incorporate active information gathering for planning typically assume that robots can obtain informative observations independently [7], [8]. These methods, therefore, do not support scenarios that require coordination for joint sensing by multiple robots to collect informative observations about the context. Finally, once the context and corresponding objective ordering are known, Pareto-based approaches become computationally inefficient as they fail to exploit the available preference information during planning. 

We present _Multi-Robot Context-Uncertain Stochastic Shortest Path_ (MR-CUSSP), a framework designed to model settings where objective preferences depend on a fixed but unknown context that can only be inferred via joint observations. The robots maintain a _shared_ belief over pos- 

sible contexts, which is updated based on observations. We consider contexts to map to fixed lexicographic preferences over objectives, and assume the existence of belief-collapsing observations at _landmark states_ that uniquely identify the governing preference ordering that must be followed for task completion. These belief-collapsing observations depend on the joint state and actions, enforcing robot coordination for context inference. We focus on navigation tasks in which robots must reach goal locations, while avoiding collisions with other robots and optimizing context-induced lexicographic ordering over objectives. 

Our two-stage solution approach (Fig. 1) involves computing: (1) joint plans to visit landmark states such that the underlying context can be quickly inferred; and (2) collisionfree individual paths for task completion using the lexicographic ordering over objectives, induced by the inferred context. For the first stage, we present _CIMOP_ (Coordinated Inference for Multi-Objective Planning) which computes joint plans to visit landmark states in an order that accelerates belief collapse through informative observations. For the second stage, we present _Lexicographic Conflict-Based Search_ (LCBS), an algorithm that builds on conflict-based search (CBS) [14] to compute a collision-free path for each robot, aligned with the context-induced objective ordering. LCBS uses lexicographic _A[∗]_ and constraint branching [11] to produce collision-free paths for the robots. Our proposed two-stage structure separates the challenges of information gathering and task execution, enabling each to be solved with algorithms tailored to their structure. By first inferring the context and then planning with a known preference ordering, the approach enables scalable, collision-free robot planning. 

Our empirical evaluations using three domains in simulation and five physical robots show that our proposed twostage approach outperforms combinations of state-of-the-art baselines for each stage. 

## II. BACKGROUND AND RELATED WORKS 

**Stochastic Shortest Path (SSP) problem** SSPs are a popular framework for modeling goal-oriented tasks that require sequential decision making under stochastic outcomes [15], such as autonomous navigation [16] and warehouse operation [17]. Formally, an SSP is represented by the tuple _⟨S, A, T, C, s_ 0 _, sg⟩_ , with a finite set of states _S_ , actions _A_ , transition function _T_ that represents probability of reaching a successor state, a cost function _C_ , and start and goal states denoted by _s_ 0 and _sg_ , respectively. This work extends SSPs to model settings with multiple robots and lexicographic ordering over objectives induced by a latent context. 

**Active information gathering** Existing works on information gathering reduces uncertainty by planning informative actions [8] or sampling exploration policies [18], but assume that observations can be obtained independently by robots. A recent approach models active sensing for a single robot in partially observable settings using Locally Observable Markov Decision Processes (LOMDPs) [5], [6], These approaches, however, do not model settings where 

observations depend on coordinated robot configurations, which is precisely the setting we target. 

**Multi-Objective MAPF** Multi-objective multi-agent path finding (MO-MAPF) extends multi-agent path finding (MAPF) to settings with multiple objectives, each associated with a cost function [12], [19]. Robots **R** = _{_ 1 _, . . . , d}_ move in discrete time on a graph _G_ = ( _V, E_ ), with each robot _i ∈_ **R** following a path _πi_ from start _si_ to goal _gi_ . A joint plan Π = ( _π_ 1 _, . . . , πd_ ) is _valid_ if it avoids vertex and edge conflicts [20]. Each robot incurs a cost vector **c** _i ∈_ R _[n]_ +[,] yielding total cost **C** (Π) =[�] _i∈_ **R[c]** _[i]_[.] 

MO-MAPF methods compute Pareto-optimal paths for each robot at the low level and resolving conflicts through a constraint tree at the high level. MO-CBS [12] and BB-MOCBS [13] explicitly enumerate non-dominated joint plans, while BB-MO-CBS- _ε_ and BB-MO-CBS- _k_ control the size of the frontier through approximation or restriction [13], [11]. Scalarization and evolutionary approaches combine multiple objectives into a single scalar cost or fitness function before applying CBS [21]. While effective for exploring tradeoffs, these methods do not directly enforce a prescribed lexicographic ordering during search. Our approach instead integrates lexicographic comparison at both levels of CBS, ensuring that the returned solution is preference-aligned without frontier construction or scalar reduction. 

## III. PROBLEM FORMULATION 

Consider a setting with _d_ robots, each with its own assigned task. The robots operate in an environment with a fixed context that is unknown a priori and must be inferred from observations obtained during execution. Since the underlying context induces a preference ordering over multiple objectives, the robots cannot successfully complete their task in a preference-aligned manner until the context is inferred. We consider tasks characterized by specific start and goal locations for each robot. The robots can independently complete their tasks but must coordinate for context inference and to avoid collisions. We formalize this setting as a _Multi-Robot Context-Uncertain Stochastic Shortest Path_ (MR-CUSSP) problem. 

**Definition 1.** _A Multi-Robot Context-Uncertain Stochastic Shortest Path (MR-CUSSP) problem for a set of robots_ _**R**_ = _{_ 1 _, . . . , d} is defined by M_ = _⟨P, X, A, T, C,_ Θ _, O⟩ with_ 

- _P_ = _{c_ 1 _, . . . , cm} is a finite set of possible contexts, with cg ∈ P as the true context initially unknown to the robots;_ 

- _X_ = _S × P is the state space, where S_ = _×k∈AS_[ˆ] _k is the joint physical state and P is the set of possible contexts;_ 

- _A_ = _×k∈AA_[ˆ] _k is the joint action space;_ 

- _T_ : _X × A × X →_ [0 _,_ 1] _is the transition function;_ 

- _C_ : _X×A →_ R _[n] is the cost for objectives o_ = _{o_ 1 _,...,on};_ 

- Θ : _P → θ maps each context ci ∈ P to a lexicographic ordering θi ∈ θ, where θi_ = _Ci_ 1 _≻· · · ≻ Cin denotes a strict priority ordering over objectives, and Cij is the cost associated the j[th] priority objective under context ci;_ 

- _O_ : _A × X ×_ Ω _→_ [0 _,_ 1] _is the joint observation function, where O_ ( _a, x[′] , ω_ ) = Pr( _ω | a, x[′]_ ) _and_ Ω= 2 _[P] \ ∅ is the_ 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0003-00.png)


Fig. 2: Solution approach overview. A most-likely-outcome determinization is first applied to obtain a discrete graph representation of the stochastic domain, enabling the use of graph-based planning methods. CIMOP prioritizes visiting landmark states that minimize the belief entropy and assigns robots accordingly, based on the current shared belief which is updated based on joint observations at landmark states. Once the context is inferred ( _cg_ ), the induced lexicographic ordering Θ( _cg_ ) and a discrete graph representation of the environment, along with a heuristic, are used for task planning. LCBS uses lexicographic _A[∗]_ to compute preference-aligned paths, detects conflicts in the joint plan, and iteratively adds constraints using binary branching [13] until a conflict-free solution is obtained. 

## _set observations_ 

Each state is represented by _x_ = _⟨s, c⟩_ , with _s ∈ S_ and _c ∈ P_ . The initial and goal states are denoted by _x_ 0 = _⟨s_ 0 _, c⟩_ and _xg_ = _⟨sg, c⟩_ with _s_ 0 _, sg ∈ S_ , respectively. MRCUSSPs have mixed observable state components as _s_ is fully observable and the partial observability is restricted to the context. Therefore, robots maintain a shared belief _b_ : _X →_ ∆ _[|][X][|−]_[1] which is updated based on joint observations. For clarity, the rest of this paper considers homogeneous robots but MR-CUSSPs also support heterogeneous robots. 

**Joint observations at landmark states.** Every joint action produces an observation _ω ∈_ Ω. At _landmark states_ , _L ⊆ S_ , observations provide accurate information about a subset of potential contexts. For each _s ∈L_ , let Ω _s_ denote the set of observations corresponding to context information that can be inferred from that state. Each _ω ∈_ Ω _s_ provides information about maximal set of contexts. Similar to locality-based observation models [5], [6], landmark states correspond to informative physical states where observations become available only when the required joint robot configuration and actions are satisfied. For example, salp robots arranged in a ring around a crevice receive accurate flow information, reducing uncertainty over contexts. Thus, _∀a ∈ A, x[′]_ = _⟨s[′] , c[′] ⟩_ : 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0003-05.png)


**Belief update.** Belief _b_ ( _x_ ) is semantically a belief over contexts since the physical state _s_ in _x_ = _⟨s, c⟩_ is fully observable. The updated belief for _x[′]_ = _⟨s[′] , c[′] ⟩_ after receiving an observation _ω_ is calculated as: 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0003-07.png)


where _η_ = Pr( _ω|b, a, s[′]_ ) _[−]_[1] is a normalization constant and _b_ ( _c_ ) is the belief over a context _c_ . By definition, the observation function produces a belief-collapsing observation or no information at all. Therefore, the belief is either collapsed ( _b[′]_ ( _c_ ) = _{_ 0 _,_ 1 _}_ ) or remains the same ( _b[′]_ ( _c_ ) = _b_ ( _c_ )). Since _|S|_ is finite, belief update following Eqn. 1 results in a finite number of reachable beliefs for MR-CUSSP. 

**Belief entropy.** Efficient task completion requires quick context inference by optimizing the visitation order of landmark states, based on current uncertainty over contexts. To quantify current uncertainty, we define _belief entropy_ as the number of contexts that remain feasible under belief _b_ : 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0003-10.png)


We use _H_ ( _b_ ) to denote the entropy associated with a belief _b_ and _H_ ( _b[′] |b, ωℓ[k]_[)][to][denote][the][entropy][associated][with][an] updated belief _b[′]_ as a result of joint observation ( _ωℓ[k]_[) made by] _k_ robots at landmark _ℓ_ . By Eqn. 2, _H_ ( _b_ ) = 0 only when the belief is non-zero for exactly one context, which indicates the inference of the true context, as belief collapse with incorrect context is impossible under our observation function. 

In the following section, we present our two-stage solution approach that first infers the underlying context and then computes collision-free paths for task completion, using the context-induced objective ordering. 

## IV. SOLUTION APPROACH 

Solving MR-CUSSPs involves four high-level steps (Figure 2): (1) identify informative sequence of landmark states for fast context inference, and assign robot groups to visit them; (2) visit the assigned landmarks and update shared belief based on observations; (3) repeat steps (1)-(2) until belief collapse; and (4) once the true context is inferred, plan for task completion under induced objective preferences. For steps (1) and (2), we present an algorithm, _CIMOP_ (Coordinated Inference for Multi-Objective Planning). CIMOP (Alg.1) determines the order in which landmarks states 

should be visited, based on the initial belief, and computes coordinated plans to obtain informative observations at landmark states. For step (4), we present Lexicographic Conflict-Based Search (LCBS) that computes a plan for each robot independently, while avoiding collisions with other robots. To enable checking for potential collisions between robots in steps (2) and (4), we use most-likely outcome determinization [22] to construct a deterministic approximation by using the most likely successor for each state-action pair, during planning. This is complemented with replanning when robots reach a state for which they do not have a prescribed action. Determinization enables planning over a discrete graph _G_ = ( _V, E_ ), where vertices correspond to physical states and edges correspond to mostlikely transitions. This enables both CIMOP and LCBS to perform efficient heuristic search while avoiding reasoning over full stochastic branching. 

## _A. Coordinated Context Inference using CIMOP_ 

Alg. 1 first initializes the available robot set, visited landmark set, and active robot groups (Line 1). If _H_ ( _b_ 0) _>_ 0, we compute the minimum number of robots required to obtain an informative observation at each landmark, denoted by _NL_ [ _ℓ_ ] (Lines 4–6). This is computed by searching over possible team sizes to find the smallest _k_ that yields the maximum entropy reduction _H_ ( _b_ 0) _− H_ ( _b[′] |ωℓ[k]_[)][.] 

CIMOP iteratively computes a visitation sequence _I_ over landmark states, based on current belief (Lines 7,8). Specifically, CIMOP uses Alg. 2 to compute _I_ by estimating the reduction in entropy that can be achieved with _NL_ [ _ℓ_ ] robots at a landmark _ℓ_ , _H_ ( _b_ ) _−H_ � _b[′] | b, ωℓ[N][L]_[[] _[ℓ]_[]] �. The landmarks are then sorted in the decreasing order of entropy reduction and used for robot assignment. Note that _NL_ [ _ℓ_ ] is determined using _b_ 0 (Line 6, Alg. 1) while _I_ is determined using _b_ (Line 1, Alg. 2). If _|_ **R** _av| ≥ NL_ [ _ℓ_ ], the nearest _NL_ [ _ℓ_ ] robots are assigned to unvisited _ℓ ∈I_ (Lines 9-11). The assigned landmark is recorded within the group object and its robots are removed from the available pool (Lines 12-14). The process continues until either available robots are insufficient or all prioritized landmarks are examined. While any planner can be used to compute a joint plan for the group to reach its assigned landmark, our experiments use a standard conflict-based search (CBS) planner with determinization and replanning as needed [14] (Line 15). When a group _g_ reaches its assigned landmark _g.ℓ_ , the robots are returned to the available pool (Line 18), the landmark is marked as visited (Line 19), and the shared belief is updated (Line 20). Since the belief does not change in non-landmark states, following our observation function, it is sufficient to update the shared beliefs when a landmark is visited. 

The process of recomputing landmark priorities under the updated belief and reallocating robots is repeated until _H_ ( _b_ ) = 0 (Lines 7-20). Once belief collapses, the context is inferred as _cg_ = arg max _c∈P b_ , and associated lexicographic ordering is returned for task planning (Lines 21-22). 

**Algorithm 1** CIMOP: Inference plan with belief sync 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0004-06.png)


## 7: **while** _H_ ( _b_ ) _>_ 0 **do** 

8: _I ←_ GETLANDMARKVISITSEQUENCE( _NL, L, b_ ) 9: **for** _ℓ ∈I \ Lvis_ **do** _▷_ highest to lowest visit priority 10: **if** _|_ **R** _av| ≥ NL_ ( _ℓ_ ) **then** 11: _g ←_ ASSIGNNEARESTROBOTS( **R** _av, NL_ [ _ℓ_ ]) 12: _g.ℓ ← ℓ_ 13: _Groups._ APPEND( _g_ ) 14: **R** _av ←_ **R** _av \g._ **R** 15: Π _._ APPEND(PLANTOLANDMARK( **R** _, Groups_ )) 16: **for** _g ∈ Groups_ **do** 17: **if** _g_ reached _g.ℓ_ **then** 18: **R** _av ←_ **R** _av ∪ g_ 19: _Lvis ←Lvis._ APPEND( _g.ℓ_ ) 20: _b ←_ UPDATEBELIEF(Π) _▷_ shared belief 21: _cg ←_ arg max _c∈P b_ 22: **return** Θ( _cg_ ) _▷_ preferences under _cg_ 

## **Algorithm 2** GETLANDMARKVISITSEQUENCE 

**Require:** landmark requirements _NL_ , landmarks _L_ , belief _b_ **Ensure:** Visitation sequence _I_ 1: _∀ℓ ∈L_ : _IH_ ( _ℓ_ ) _← H_ ( _b_ ) _− H_ � _b[′] | b, ωℓ[N][L]_[[] _[ℓ]_[]] � 2: _I ←L._ SORT( _IH ,_ order = descending) 3: **return** _I_ 

## _B. Multi-Robot Planning under Inferred Context using LCBS_ 

To plan under the inferred lexicographic preferences Θ( _cg_ ), we present _Lexicographic Conflict-Based Search_ (LCBS), an algorithm that extends the two-level framework of Conflict-Based Search (CBS) [14] to settings with strict priority ordering over multiple objectives. In LCBS, the lowlevel search computes a plan for each robot independently; the high-level search detects conflicts in the joint plan and iteratively generates constraints for the low-level planner. Any heuristic can be used in practice but optimality guarantees depend on the heuristic admissibility. In our experiments, we use Euclidean distance between the current location and the goal as the heuristic. 

To compare two cost vectors **u** and **v** , we define **u** _<_ lex **v** as the lexicographic comparison under Θ. Specifically, **u** _<_ lex **v** iff _∃j ∈{_ 1 _, . . . , n}_ s.t. **u** _[j] <_ **v** _[j]_ and _∀k < j,_ **u** _[k]_ = **v** _[k] ._ The _<_ lex is used by LCBS to prune dominated cost vectors during planning. 

**Low-Level Search** The low-level planner in LCBS is 

**Algorithm 3** LA _[∗]_ (Lexicographic A _[∗]_ ) 

**Input** : _G_ = ( _V, E_ ), start-goal ( _s, g_ ), edge cost **c** _e_ : _E →_ R _[d]_ +[,] heuristic **h** : _V →_ R _[d]_[constraints][Γ] +[,] **Output** : Optimal path _π_ from _s_ to _g_ (or _∅_ ) 

1: **Init:** timed states _z_ = ( _v, t_ ) with _v ∈ V_ , _t ∈_ N; 

2: _z_ 0 _←_ ( _s,_ 0); **g** ( _z_ 0) _←_ **0** ; **f** ( _z_ 0) _←_ **h** ( _s_ ); 

3: open list _O ←{}_ ; cost map _C ←{}_ ; plan _π ←{}_ ; 

4: _O._ PUSH( _z_ 0); _C_ [ _z_ 0] _←_ **0** ; 

- 5: **while** _O_ = _∅_ **do** 

6: _z_ = ( _v, t_ ) _←O._ POPMIN() _▷_ lex-min **f** 7: **if** _v_ = _g_ **and not** VIOLATES( _z,_ Γ) **then** 8: _π ←_ RECONSTRUCTPATH( _z_ ) 9: **break** 10: **for** each _u ∈_ SUCCESSORS( _v_ ) **do** 11: _y ←_ ( _u, t_ +1) 12: **if** VIOLATES( _z → y,_ Γ) **then** 13: **continue** 14: **g** _[′]_ ( _y_ ) _←_ **g** ( _z_ ) + **c** _e_ ( _v, u_ ); **f** _[′]_ ( _y_ ) _←_ **g** _[′]_ ( _y_ ) + **h** ( _u_ ) 15: **if** _y ∈C/_ **or g** _[′]_ ( _y_ ) _<_ lex _C_ [ _y_ ] **then** 16: _C_ [ _y_ ] _←_ **g** _[′]_ ( _y_ ); PARENT( _y_ ) _← z_ ; **f** ( _y_ ) _←_ **f** _[′]_ ( _y_ ) 17: _O._ PUSH( _y_ ) 18: **return** _π_ 

_lexicographic A[∗]_ (LA _[∗]_ ) (Alg. 3), which computes individual robot paths under the ordering induced by Θ. LA _[∗]_ searches over time-augmented states _z_ = ( _v, t_ ) with cumulative vector cost **g** ( _v, t_ ) and admissible heuristic **h** ( _v_ ). The evaluation key is **f** ( _v, t_ ) = **g** ( _v, t_ ) + **h** ( _v_ ). The open list _O_ is queried by POPMIN to extract the lexicographically smallest **f** under _<_ lex (Line 6), so states with lexicographically smaller **f** are expanded first. 

Alg. 3 initializes _O_ with ( _s,_ 0) and maintains a closed map _C_ storing the best **g** per state (Lines 4). If the popped state reaches the goal and satisfies constraints Γ, the path is returned (Lines 6-9, 18). Otherwise, successor states from outgoing edges are generated, and transitions violating Γ are skipped (Lines 10-13). A successor is inserted only if its **g** improves under _<_ lex (Line 14-17), ensuring that each state maintains a single best cost vector following Θ. 

Optimizing a lexicographic ordering using LA* is more than just a tie-breaking. As node selection (Line 6) and state updates (Line 15) are governed by _<_ lex, lexicographicallyworse path candidates for a state are discarded immediately. The search, thus, directly and efficiently optimizes the strict priority ordering specified by Θ. 

**High-Level Search** For the high-level search (Alg. 4), we adopt the constraint-tree (CT) framework from BB-MOCBS-pex [11]. Each CT node denotes a joint plan _N ._ Π, joint cost vector _N ._ **C** , and constraint set _N ._ Γ. The lexicographic comparator _<_ lex is first defined according to Θ, along side initialization of root node _N_ 0, high-level open list _O_ HL, constraint set Γ0 and robot policies _πi ∀i ∈_ **R** (Line 1, 2). The high-level open list _O_ HL is ordered lexicographically by _N ._ **C** (Line 9). The root node is constructed by invoking LA _[∗]_ for each robot under empty constraints (Lines 3–6), and 

**Algorithm 4** LCBS (High-Level Search) 

**Input** : _G_ = ( _V, E_ ), robots **R** = _{_ 1 _, . . . , d}_ , start-goal pairs ( _s[i] , g[i]_ ) _∀i ∈_ **R** , edge cost **c** _e_ , heuristic **h** , lexicographic preferences Θ **Output** : Conflict-free joint plan Π = ( _π_ 1 _, . . . , πd_ ) (or _∅_ ) 

1: **Init:** _<_ lex _←_ Θ; _N_ 0 _←∅_ ; _O_ HL _←{}_ ; 

- 2: **Init:** Γ0 _←{}_ ; _πi ←∅∀i ∈_ **R** ; 

3: **for** each robot _i ∈_ **R do** 4: _πi ←_ LA*( _G, s[i] , g[i] ,_ **c** _e,_ **h** _,_ Γ0) 5: **if** _πi_ = _∅_ **then** 6: **return** _∅_ 7: _N_ 0 _._ Π _←_ [ _πi_ ] _i∈_ **R** ; _N_ 0 _._ **C** _←_[�] _i_ **[c]** _[e]_[(] _[π][i]_[)][;] _[ O]_[HL] _[.]_[P][USH][(] _[N]_[0][)][;] 8: **while** _O_ HL = _∅_ **do** 9: _N ←O_ HL _._ POPMIN() _▷_ lex-min **C** ( _N ._ Π) 10: _conflict ←_ DETECTFIRSTCONFLICT( _N ._ Π) 11: **if** _conflict_ = _∅_ **then** 12: **return** Π _←N ._ Π _▷_ return conflict-free plan 13: ( _type, loc, time, idi, idj_ ) _← conflict_ 14: _{γ[i] , γ[j] } ←_ GENERATECONSTRAINTS( _conflict_ ) 15: **for** each _a ∈{i, j}_ **do** 16: Create child _Na_ ; _Na._ Γ _←N ._ Γ _∪{γ[a] }_ 17: _πa[′][←]_[LA*][(] _[G, s][a][, g][a][,]_ **[ c]** _[e][,]_ **[ h]** _[,][ N][a][.]_[Γ)] 18: **if** _πa[′]_[=] _[ ∅]_ **[then]** 19: _Na._ Π[ _a_ ] _← πa[′]_[;] _[N][a][.]_ **[C]** _[ ←]_[�] _i_ **[c]** _[e]_[(] _[π][i]_[)] 20: _O_ HL _._ PUSH( _Na_ ) 21: **return** Π 

the joint cost is computed, _N_ 0 _._ **C** =[�] _i∈_ **R[c]** _[e]_[(] _[π][i]_[)][(Line][7).] At each iteration, the node with lexicographically smallest joint cost is popped (Line 9). If no conflict is detected, the joint plan is returned (Lines 10–12). Otherwise, the earliest conflict is identified and the node is split into two child nodes, each imposing a constraint on one of the conflicting robots (Lines 13–16). The affected robot is replanned using LA _[∗]_ under the updated constraint set (Line 17). Feasible children update their joint plan and cost (Lines 18–19) and are pushed into _O_ HL (Line 20). 

The first conflict-free CT node popped is lexicographically optimal as both high-level and low-level search order nodes under _<_ lex and LA _[∗]_ returns lexicographically optimal paths under constraints. 

## V. EXPERIMENTS 

We evaluate our solution approach in simulation using three domains and on hardware using five mobile robots. 

**Baselines:** We compare the performance of our two-stage approach with combinations of state-of-the-art for each stage. Specifically, for the first stage, we compare CIMOP with (1) ARVI [8] and (2) SAIA [18]. As both these approaches assume robots can gather information independently, we modify them to work with our observation function, for fair comparison. For the second stage, we compare LCBS against (1) BB-MO-CBS- _k_ ( _k_ = 1) [11] that returns a single nondominated solution, serving as a fast Pareto baseline, (2) Scalarized CBS that uses scalarization in low level search 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0006-00.png)


**----- Start of picture text -----**<br>
Map (i) Entropy for 5 robots ( ↓ ) (ii) Entropy for 35 robots ( ↓ ) (iii) Cumulative entropy for 5 robots ( ↓ ) (iv) Planning time ( ↓ )<br>(a) Salp<br>(b) Warehouse<br>(c) Forest firefighting<br>**----- End of picture text -----**<br>


Fig. 3: Summary of experimental results across three domains. The first column shows the domain maps. The second and third columns show entropy-of-belief trends for 5 and 35 robots, respectively. The fourth column shows path cost with increasing percentage of redundant landmarks for analysis in cluttered environments. The fifth column shows plan computation time with increasing numbers of robots. All results are averaged over five instances with randomized robot starting locations. 

using CBS [14] to combine multiple objectives into a single weighted value, and (3) MO-CBS [12] that maintains Pareto frontiers at the robot level and combines them through CBS-style conflict resolution, providing a principled Paretooptimal multi-objective baseline without explicitly searching the full joint state space. For Scalarized CBS, scalarization weights follow geometric scaling: _C_ 1 _M[n][−]_[1] + _C_ 2 _M[n][−]_[2] + _· · ·_ + _Cn_ , where _M_ must be sufficiently large to preserve _C_ 1 _≻· · · ≻ Cn_ . In practice, objective cost magnitudes are not known a priori, making weight selection non-trivial. Following [21], we sample 50 random trajectories from start to goal to estimate the scale of each objective, and choose _M_ to exceed the largest observed lower-priority cost for a single instance in each domain. The same _M_ value is used for all other instances of that domain. 

All algorithms were implemented in C++ and tested on a macOS machine with 18 GB RAM. Robot evaluation is performed with five robots in the Robotarium testbed [9]. 

**Metrics.** We compare the algorithms using stage-specific metrics in simulation and the overall performance of the twostage approach using mobile robots. The stage-specific metrics are: (i) Entropy of belief over contexts during execution (Eqn. 2); (ii) Cumulative entropy of the belief sequence to measure the duration of uncertainty until belief collapse (as opposed to uncertainty associated with a particular belief as in (i)); (iii) Scalability with increasing number of robots; and (iv) Performance with varying planning time budget. 

## _A. Evaluation in simulation_ 

In the following domains, robots begin with a uniform initial belief over a finite set of contexts and coordinate to obtain informative observations at landmark states. 

_a) Sample Collection with Salps:_ In this domain, salpinspired [23] underwater robots are tasked with collecting samples in environments with crevices and boulder ridges that act as informative landmarks. Robots begin with a uniform belief over three contexts: _c_ 1 (strong-current region), _c_ 2 (coral-sensitive region), and _c_ 3 (nominal condition). In all contexts, robots should minimize energy consumption ( _oe_ ), minimize coral damage ( _oc_ ), and minimize time to goal ( _ot_ ), but their priority depends on the context. The context to objective ordering is _c_ 1 : _oe ≻ oc ≻ ot_ ; _c_ 2 : _oc ≻ oe ≻ ot_ ; and _c_ 3 : _ot ≻ oe ≻ oc_ . Coordinated sampling at landmarks reveals flow and surface characteristics that distinguish among these contexts. Across instances, we vary the number and spatial distribution of informative landmarks and robots. 

_b) Heavy-Lift Warehouse:_ Autonomous warehouse robots transport shelves through shared aisles to fulfillment stations, with designated monitoring stations serving as informative landmarks. Robots begin with a uniform belief over three contexts: _c_ 1 (backlogged), _c_ 2 (congested), and _c_ 3 (humantraffic). In all contexts, robots balance completion time ( _ot_ ), minimizing congestion in primary aisles, ( _oc_ ) and avoiding human zones ( _oh_ ), but the priority depends on context. The context to objective ordering is as follows: _c_ 1 : _ot ≻ oc ≻ oh_ ; _c_ 2 : _oc ≻ ot ≻ oh_ ; and _c_ 3 : _oh ≻ oc ≻ ot_ . At monitoring 

stations, two robots must arrive simultaneously at paired checkpoints to obtain a joint observation of aisle-level traffic and human presence, which cannot be determined from a single robot’s local view. Across instances, we vary the number of robots, shelf locations, and the placement of primary aisles and monitoring stations. 

_c) Forest Firefighting:_ Aerial robots are assigned to reach designated fire-control locations in an evolving wildfire. Since large-scale wind and smoke conditions cannot be determined from local sensing alone, robots coordinate at designated vantage points that serve as informative landmarks before planning traversal. Robots begin with a uniform belief over three contexts: _c_ 1 (high-wind), _c_ 2 (dense-smoke), and _c_ 3 (rapid-spread). In all contexts, robots should minimize completion time ( _ot_ ), minimize energy consumption ( _oe_ ), and minimize path length ( _ol_ ), but the priority depends on the context. The context to objective ordering is _c_ 1 : _oe ≻ ol ≻ ot_ ; _c_ 2 : _ol ≻ oe ≻ ot_ ; and _c_ 3 : _ot ≻ oe ≻ ol_ . Coordinated observations at vantage points reveal wind and smoke conditions that distinguish among these contexts. Across instances, we vary the number of robots, vantage point placement, and the locations of wind and fire spots. 

## VI. RESULTS AND DISCUSSION 

_a) Belief entropy reduction:_ Fig. 3 (columns (i)–(ii)) reports belief entropy during execution, computed using Eqn. 2, where lower values indicate faster context inference. Across all settings, CIMOP consistently infers the context faster than both baselines. For five robots, CIMOP reaches zero entropy within 20 steps in the salp and warehouse domains, compared to 60–80 steps for the baselines, and collapses substantially faster in the forest firefighting domain where baselines require several hundred steps. While we observe an improved performance with 35 robots, across methods, CIMOP remains consistently faster in context inference. 

_b) Cumulative entropy with increasing redundant landmarks:_ To quantify how long it takes to infer the true context and whether useful landmarks are prioritized correctly over time, we measure the cumulative entropy of a belief sequence induced by the policy. This complements the entropy of a single belief point (Eqn. 2) and evaluates the sequential nature of uncertainty reduction. We measure this by varying the percentage of landmark states whose associated observations are _redundant_ with respect to observations available at other landmark states and therefore visiting them does not reduce belief entropy. Figure 3 (column (iii)) shows cumulative entropy, averaged over five instances in each domain, with increasing percentage of redundant landmarks. Lower cumulative entropy indicates faster inference of the true context. CIMOP maintains consistently low cumulative entropy across all domains and clearly outperforms baselines, with low variance despite sparse informative observations. 

_c) Planning time:_ Figure 3 (column (iv)) evaluates scalability through wall-clock planning time for context inference. CIMOP scales substantially better than both baselines in all domains. For 35 robots, CIMOP consistently plans in 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0007-06.png)


Fig. 4: Success rate on 15 instances (five from each of the three domains) under constrained planning time limit with five robots and three objectives. 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0007-08.png)


Fig. 5: Execution sequence with five GTernal robots [9]: (1) start with uniform belief over three contexts, (2) form a chain to observe the cave landmark and update belief, (3) four robots form a ring to observe the crevice landmark and collapse belief, after which (4) the robots independently plan prioritizing minimizing coral damage over energy consumption and time to goal as imposed by the inferred context _c_ 2. 

under two minutes, while ARVI exceeds 40 minutes and SAIA exceeds 80 minutes. This consistent gap demonstrates CIMOP’s ability to scale to larger robot teams while maintaining practical planning times. 

_d) Performance in time-constrained settings:_ The efficiency of planning in time-constrained settings is measured in terms of _success rate_ [11], [12]: the fraction of problem instances where the algorithm was able to generate an optimal solution for the lexicographic ordering over objectives, which can be verified by comparing the results with a Pareto-frontier approach (such as MO-CBS). Fig. 4 reports the success rate on 15 environment instances (five from each of the three domains) as the planning-time budget decreases from 120 to 5 seconds for five robots and three objectives. LCBS maintains 100% success across all budgets and remains consistent even at five seconds, while BB-MO-CBS ( _k_ =1), MOCBS, and Scalarized CBS drop significantly as the time limit decreases. The consistent performance of LCBS under tight budgets highlights that eliminating lexicographically dominated nodes during search allows it to compute preferencealigned solutions reliably in time-sensitive settings. 

_e) Hardware experiments:_ We validate the practical feasibility of our approach using five mobile robots in the salp domain. Fig. 5 shows shared belief evolution, where robots adapt formations based on observation requirements at landmarks, and collapse the belief in real time before exe- 


![](1_survey/papers/md/Rustagi2026MultiRobot_figs/Rustagi2026MultiRobot.pdf-0008-00.png)


Fig. 6: Total time taken to plan by each approach in our hardware experiment with five mobile robots and three possible contexts, each with different preference ordering over three objectives. 

cuting preference-aligned plans. Fig. 6 reports total planning time (stage 1 + stage 2), where CIMOP + LCBS completes both stages in under 6 seconds, while other combinations require 40–120 seconds. Combinations using LCBS maintain low second-stage times, and CIMOP substantially reduces context inference time, thus demonstrating the run time benefits of both CIMOP and LCBS which enable real-time execution on physical robots. 

## VII. SUMMARY AND FUTURE WORK 

This paper formalizes multi-robot planning under a fixed but initially unknown context as an MR-CUSSP. We present two algorithms that enable robot coordination to obtain informative joint observations to infer the operative context, and then compute collision-free plans aligned with the induced lexicographic preference ordering over objectives. Experimental results across three simulated domains and hardware deployments demonstrate faster belief collapse, lower cumulative entropy, and improved scalability in planning time with increasing robots and objectives compared to state-of-the-art baselines for each stage in our solution approach. Future work will relax the assumption of predefined landmark structures and extend this to learning settings. 

## ACKNOWLEDGEMENTS 

Rustagi and Saisubramanian were supported in part by ONR award N00014-23-1-2171. 

## REFERENCES 

- [1] M. Al-Husseini, K. H. Wray, and M. J. Kochenderfer, “Hierarchical framework for optimizing wildfire surveillance and suppression using human-autonomous teaming,” _Journal of Aerospace Information Systems (AIAA)_ , pp. 1–22, 2024. 

- [2] H. Jiang, Y. Wang, R. Veerapaneni, T. H. Duhan, G. A. Sartoretti, and J. Li, “Deploying ten thousand robots: Scalable imitation learning for lifelong multi-agent path finding,” in _ICRA_ , 2025. 

- [3] P. Rustagi, Y. Anand, and S. Saisubramanian, “Multi-objective planning with contextual lexicographic reward preferences,” in _Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS)_ , 2025. 

- [4] Z. Yang, Y. Zhang, M. Herbert, M. A. Hsieh, and C. Sung, “Effect of jet coordination on underwater propulsion with the multi-robot salp system,” in _IEEE 8th International Conference on Soft Robotics_ , 2025. 

- [5] M. Merlin, S. Parr, N. Parikh, S. Orozco, V. Gupta, E. Rosen, and G. Konidaris, “Robot task planning under local observability,” in _ICRA_ , 2024. 

- [6] M. Merlin, Z. Yang, G. Konidaris, and D. Paulius, “Least commitment planning for the object scouting problem,” in _IROS_ , 2025. 

- [7] N. Atanasov, J. Le Ny, K. Daniilidis, and G. J. Pappas, “Decentralized active information acquisition: Theory and application to multi-robot slam,” in _ICRA_ , 2015. 

- [8] B. Schlotfeldt, D. Thakur, N. Atanasov, V. Kumar, and G. J. Pappas, “Anytime planning for decentralized multirobot active information gathering,” _Robotics and Automation Letters (RA-L)_ , vol. 3, no. 2, pp. 1025–1032, 2018. 

- [9] S. Wilson, P. Glotfelter, L. Wang, S. Mayya, G. Notomista, M. Mote, and M. Egerstedt, “The robotarium: Globally impactful opportunities, challenges, and lessons learned in remote-access, distributed control of multirobot systems,” _Control Systems Magazine_ , vol. 40, no. 1, pp. 26–44, 2020. 

- [10] P. Sharma, B. Sundaralingam, V. Blukis, C. Paxton, T. Hermans, A. Torralba, J. Andreas, and D. Fox, “Correcting robot plans with natural language feedback,” in _RSS_ , 2022. 

- [11] F. Wang, H. Zhang, S. Koenig, and J. Li, “Efficient approximate search for multi-objective multi-agent path finding,” in _Proceedings of the 34th International Conference on Automated Planning and Scheduling (ICAPS)_ , 2024. 

- [12] Z. Ren, S. Rathinam, and H. Choset, “Multi-objective conflict-based search for multi-agent path finding,” in _International Conference on Robotics and Automation (ICRA)_ , 2021. 

- [13] Z. Ren, J. Li, H. Zhang, S. Koenig, S. Rathinam, and H. Choset, “Binary branching multi-objective conflict-based search for multi-agent path finding,” in _Proceedings of the 33rd International Conference on Automated Planning and Scheduling (ICAPS)_ , 2023. 

- [14] G. Sharon, R. Stern, A. Felner, and N. Sturtevant, “Conflict-based search for optimal multi-agent path finding,” in _AAAI_ , 2012. 

- [15] S. Saisubramanian, K. H. Wray, L. Pineda, and S. Zilberstein, “Planning in stochastic environments with goal uncertainty,” in _IROS_ , 2019. 

- [16] E. Stracca, G. Grioli, L. Pallottino, and P. Salaris, “Risk-aware routing for a robot in a shared dynamic environment,” _IEEE Transactions on Robotics (TRO)_ , 2026. 

- [17] C. Street, O. Grubb, and M. Mansouri, “Planning under uncertainty from behaviour trees,” in _IROS_ , 2025. 

- [18] Y. Kantaros, B. Schlotfeldt, N. Atanasov, and G. J. Pappas, “Samplingbased planning for non-myopic multi-robot information gathering,” _Autonomous Robots_ , vol. 45, no. 7, pp. 1029–1046, 2021. 

- [19] Z. Ren, G. Wagner, and T. K. S. Kumar, “A conflict-based search framework for multi-objective multi-agent path finding,” _IEEE Transactions on Automation Science and Engineering_ , 2022. 

- [20] R. Stern, N. Sturtevant, A. Felner, S. Koenig, H. Ma, T. Walker, J. Li, D. Atzmon, L. Cohen, T. K. S. Kumar, E. Boyarski, and R. Bartak, “Multi-agent pathfinding: Definitions, variants, and benchmarks,” in _Proceedings of the 12th International Symposium on Combinatorial Search (SoCS)_ , 2019. 

- [21] F. Ho and S. Nakadai, “Preference-based multi-objective multi-agent path finding,” in _Proceedings of the 22nd International Conference on Autonomous Agents and Multiagent Systems (AAMAS)_ , 2023. 

- [22] S. Saisubramanian and S. Zilbertsein, “Adaptive outcome selection for planning with reduced models,” in _IROS_ , 2019. 

- [23] K. R. Sutherland and L. P. Madin, “Comparative jet wake structure and swimming performance of salps,” _Journal of Experimental Biology_ , vol. 213, no. 17, pp. 2967–2975, 2010. 

