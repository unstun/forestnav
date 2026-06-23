---
citation_key: Cherenson2025Autonomy
arxiv_id: 2504.03001
arxiv_url: "https://arxiv.org/abs/2504.03001"
title: "Autonomy Architectures for Safe Planning in Unknown Environments Under Budget Constraints"
authors_short: "Daniel M. Cherenson et al."
year: 2025
direction_tag: G_subgoal_optimization
source: pymupdf4llm
converted_at: 2026-06-23T18:11:27Z
origin: ai+web
reviewed: false
---

# **Autonomy Architectures for Safe Planning in Unknown Environments Under Budget Constraints** 

Daniel M. Cherenson, Devansh R. Agrawal, and Dimitra Panagou 

_**Abstract**_ **— Mission planning can often be formulated as a constrained control problem under multiple path constraints (i.e., safety constraints) and budget constraints (i.e., resource expenditure constraints). In** _**a priori**_ **unknown environments, verifying that an offline solution will satisfy the constraints for all time can be difficult, if not impossible. We present ReRoot, a novel sampling-based framework that enforces safety and budget constraints for nonlinear systems in unknown environments. The main idea is that ReRoot grows multiple reverse RRT* trees online, starting from renewal sets, i.e., sets where the budget constraints are renewed. The dynamically feasible backup trajectories guarantee safety and reduce resource expenditure, which provides a principled backup policy when integrated into the gatekeeper safety verification architecture. We demonstrate our approach in simulation with a fixed-wing UAV in a GNSS-denied environment with a budget constraint on localization error that can be renewed at visual landmarks. [Code]** 

## I. INTRODUCTION 

Robotic and autonomous systems often operate with limited knowledge of their environment and limited sensing capabilities, which poses challenges to guaranteeing their safe operation. Safety requirements are typically given in the form of a set of states in which the robot must always remain, called the safe set. In unknown environments, the safe set is not fully known _a priori_ and must be built online with information from the sensor measurements. 

In addition to instantaneous safety requirements, many robotic systems have a limited budget on resources or quantities that are depleted throughout a mission. Constraints on finite resources have been studied under various names, including integral constraints [1], budget constraints [2], [3], and cost constraints [4]. Previously studied examples include constraints on battery charge [5], localization error [6], or time spent visible to an enemy observer [7]. We consider a generalized case of the budget-constrained, safety-critical planning problem where resources can be renewed at specific regions in the state space. 

Various offline methods to enforce budget constraints have been introduced. The methods in [1], [2] solve trajectoryoptimization problems with renewable budget constraints. 

This research was supported by the Center for Autonomous Air Mobility and Sensing (CAAMS), an NSF IUCRC, under Award Number 2137195, and an NSF CAREER under Award Number 1942907. 

Daniel Cherenson is with the Department of Robotics, University of Michigan, Ann Arbor, MI 48109 USA dmrc@umich.edu 

Devansh Agrawal is with the Department of Aerospace Engineering, University of Michigan, Ann Arbor, MI 48109 USA devansh@umich.edu Dimitra Panagou is with the Department of Robotics and Department of Aerospace Engineering, University of Michigan, Ann Arbor, MI 48109 USA dpanagou@umich.edu 

> _∗_ Correspondence: dmrc@umich.edu 

However, these approaches rely on searching over large-scale graphs or solving partial differential equations derived from dynamic programming, which is computationally expensive and better suited for offline planning in known environments. An offline reinforcement-learning approach is studied in [8], where budget constraints for high-dimensional, nonlinear systems are incorporated in the training process, however no strict guarantees of constraint satisfaction are obtained. 

In this paper, we instead focus on the problem of online safety and budget constraint satisfaction, where lack of knowledge of the environment requires constant replanning and infinite horizon guarantees. Previous work on online budget constraint satisfaction used simplified robot and budget dynamics [4], [9]. The solutions were designed for specific use cases, limiting their general applicability. 

Our approach relies on a run-time safety filter. Many safety-critical robotic systems apply these filters with a backup or recovery policy that reaches an invariant backup set to guarantee safety over an infinite horizon [10]. For systems with instantaneous safety constraints, finding a backup set is often trivial, as most robots can stop in place or return to a known safe configuration. Typical backup policies include braking maneuvers, model predictive control approaches, and learned RL policies [11]–[14]. However, to guarantee budget constraint satisfaction, the design of backup policies is more challenging because the budget must be renewed in the backup set, which may only occur in limited subsets of the state space. Additionally, the trajectories to reach the backup sets must satisfy all safety constraints, which forms the backup trajectory generation problem. 

To the best of the authors’ knowledge, there are no solutions that explicitly guarantee safety and budget constraint satisfaction with limited environmental knowledge and general, non-trivial budget expenditure dynamics. This paper aims to narrow this gap by proposing a recursively feasible algorithm for the online trajectory generation of nonlinear systems under budget and safety constraints in unknown environments. The key idea and contribution is the samplingbased method called ReRoot, which efficiently generates backup trajectories to minimize resource expenditure while ensuring that the system reaches budget-renewal sets, where resources are replenished. The algorithm is demonstrated on a UAV that uses visual odometry to reach a goal in an unknown, GNSS-denied environment, with guaranteed satisfaction of budget and safety constraints. 

The paper is organized as follows. In Section II, we introduce the problem formulation. Section III describes the proposed method, highlighting the safe trajectory planner and 

ReRoot. Section IV discusses a simulation case study of a UAV in a GNSS-denied environment navigating to a goal with safety and budget constraints related to visual odometry. 

## II. PROBLEM FORMULATION 

We represent the robot motion by the nonlinear dynamics: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-03.png)


where _x ∈X ⊂_ R _[n]_ is the state and _u ∈U ⊂_ R _[m]_ is the control input, and _f_ : _X × U →_ R _[n]_ a locally Lipschitz function. Under a (locally Lipschitz) feedback controller _π_ : _X →U_ and an initial condition _x_ ( _t_ 0) = _x_ 0 _∈X_ , the closedloop system dynamics read: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-05.png)


We consider a resource that is subject to a budget constraint, and which can be renewed in a subset _R_ of the state space _X_ . The budget state _b_ is governed by the following hybrid dynamical system: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-07.png)


where _L_ : _X × U →_ R _≥_ 0 is piecewise continuous and _b_[+] = _b_ reset _≥_ 0 is the reset value of the budget state after the jump. We assume that _L_ is known, but _R_ is _not_ fully known. We aim to satisfy the following constraints: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-09.png)


where _S ⊂X_ is the set of states that satisfy safety requirements and _B_ is the budget constraint that must not be exceeded. We assume that _B > b_ reset, that _S_ has a nonempty interior, and that it is not fully known, but can be sensed online from sensor measurements. We introduce the known subset of the safe set at time _tk_ , _Fk ⊂S_ , where _k ∈_ N. Similarly, we denote the known renewal set as _Rk ⊂R ⊂S_ , where we have assumed the renewal set is safe. 

At time _tk_ +1, new information is acquired by the robot to update _Fk_ and _Rk_ such that the following relations hold: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-12.png)


Moreover, _Rk_ can be composed of _NC ≥_ 1 disjoint, compact subsets. At time _tk_ , we denote the _i_ -th subset as _R[i] k_[for] _[i][ ∈{]_[1] _[, . . . , N][C][}]_[such][that] _[R][k]_[=] _[ ∪][N] i_ =1 _[C][R][i] k_[.] Our method relies on concepts in set invariance to guarantee constraint satisfaction [15]. 

**Definition 1** (Controlled Invariant Set) **.** _A set C ⊂X is controlled invariant for the system_ (1) _, if there exists a controller π_ : _X →U that assures the existence of a unique solution to the closed-loop system_ (2) _such that C is positively invariant for the closed-loop system_ (2) _, i.e., ∀x_ ( _t_ 0) _∈C, x_ ( _t_ ) _∈C, ∀t ≥ t_ 0 _._ 

**Definition 2** (Backup Set) **.** _A set B ⊂X is a_ _**backup set** if there exists a controller π[B]_ : _X →U such that for the closed-loop system_ (2) _, ∀ x_ ( _t_ 0) _in a neighborhood N ⊂X , there exists a finite time_ 0 _≤ TB_ ( _x_ ( _t_ 0)) _< ∞ such that B_ 

_is reachable at t_ 0 + _TB and controlled invariant thereafter, i.e., x_ ( _t_ ) _∈B, ∀t ≥ t_ 0 + _TB._ 

**Assumption 1.** We assume that the budget renewal set _Rk_ is a backup set for the closed loop system (2) for all _k ∈_ N. Then, from (3), the budget constraint is satisfied for all time in _Rk_ : 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-18.png)


**Definition 3** (Trajectory) **.** _A_ _**trajectory** with horizon TH is a pair of functions p_ : _T →X and u_ : _T →U defined on T_ = [ _t_ 0 _, t_ 0 + _TH_ ] _⊂_ R _≥_ 0 _that satisfy_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-20.png)


_The set of all trajectories at t ∈_ R _starting from x ∈X is_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0002-22.png)


We assume there exists a nominal planner to generate trajectories that aim to fulfill the mission objectives. 

**Definition 4** (Nominal Trajectory) **.** _At time tk ∈_ R _at state xk ∈X , the planner generates the_ _**nominal trajectory**_ ( _p_[nom] _k , u_[nom] _k_ ) _∈_ Φ( _tk, xk_ ) _defined over the interval T_ = [ _tk, tk_ + _TH_ ] _._ 

With the above preliminaries, we state the main problem: 

**Problem 1.** _Given the known safe set Fk and budget renewal set Rk updated at each k ∈_ N _, design a safe planning algorithm that recursively constructs a trajectory p_ ( _t_ ) _that satisfies all safety and budget constraints, i.e., p_ ( _t_ ) _∈S and b_ ( _t_ ) _≤ B for all t ≥ t_ 0 _._ 

## III. METHOD OVERVIEW 

To address Problem 1, we propose a framework that recursively generates trajectories that are guaranteed to satisfy the safety and budget constraints over an infinite horizon. The solution has two components: A) gatekeeper, an algorithm to construct and validate safe trajectories using the nominal trajectory and a backup trajectory, and B) ReRoot, a sampling-based algorithm that allows for efficient online generation of backup trajectories. See Figure 1 for a block diagram showing where the gatekeeper and ReRoot components fit into the general autonomy stack. 

## _A. Guaranteed Constraint Satisfaction_ 

Here, we list the key steps of our method, and then we provide mathematical definitions of each type of trajectory along with a proof of correctness. We use the gatekeeper framework [16], [17], which recursively filters the output of the nominal planner by constructing a trajectory that is guaranteed to remain in the safe set for all time. We make use of the reformulated budget dynamics in (3) in the gatekeeper framework to augment the definition of the safe set to include the budget constraint. Algorithm 1 details the _k_ -th iteration, where _k ∈_ N _\_ 0. 

We also summarize the steps below: 

- For all _TS ∈_ [0 _, TH_ ], propagate the nominal trajectory _p_[nom] _k_ (black line in Figure 2) on the interval [ _tk, tk_ + _TS_ ], 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0003-00.png)


Fig. 1. Block diagram of our proposed layered autonomy architecture, with our module gatekeeper + ReRoot highlighted in the dashed line. 

Fig. 2. Snapshots of gatekeeper with ReRoot trees rooted at budget renewal sets. The trees are grown in the free set _Fk_ . The robot discovers new budget renewal sets as it uncovers more of the unknown space. 

**Algorithm 1:** gatekeeper with ReRoot 

**1** _TS ← TH_ **2 while** _TS ≥_ 0 **do 3** _p_[can] _k[,T][S] , b_[nom] _←_ propagate( _p_[nom] _k , x_ ( _tk_ ) _,_ [ _tk, tk_ + _TS_ ]) **4** _p_[bck,T˙S] _k , b[bck] ←_ GetBackupFromReRoot( _Gk, p_[can] _k[,T][S]_ ( _tk_ + _TS_ ) _, Fk_ ) **5** _p_[can] _k[,T][S] ←_ append( _p_[can] _k[,T][S] , p_[bck,T˙S] _k_ ) **6** _b[−] ← b_[nom] + _b_[bck] **7 if** _p_[can] _k[,T][S] is valid by Definition 7_ **then 8** _p_[com] _k_ = _p_[can] _k[,T][S]_ **9 return** _p_[com] _k_ **10** _TS ← TS −_ ∆ _T_ **11** _p_[com] _k_ = _p_[com] _k−_ 1 **12 return** _p_[com] _k_ 

   - then generate a backup trajectory _p_[bck] _k[,T][S]_ that reaches _Rk_ with ReRoot, which forms a set of _candidate trajectories_ . 

- For each candidate trajectory, compute the budget state time history _b_ ( _t_ ) with (3) and verify that constraints (4) are satisfied, forming a set of _valid trajectories_ . In Figure 2 when _k_ = 2, candidate trajectories that enter the red unsafe area are deemed invalid. 

- Select the valid trajectory that maximizes _TS_ as the _committed trajectory p_[com] _k_ . In Figure 2, the committed trajectory is composed of a red nominal portion and a green backup portion, which is generated from ReRoot and will be detailed in the following subsections. If there are no valid trajectories, select the ( _k −_ 1)-th committed trajectory _p_[com] _k−_ 1[.][This][step][guarantees][recursive] feasibility. 

Overall, Figure 2 depicts the gatekeeper trajectories and ReRoot growth as the robot expands the known budget renewal subsets _R[i] k_[during][the][mission.] 

To formally prove that all committed trajectories are 

guaranteed to satisfy all constraints for all time, we need to introduce the notion of a backup trajectory. 

**Definition 5** (Backup Trajectory) **.** _A trajectory_ ( _p_[bck] _k[,T][S] , u_[bck] _k[,T][S]_ ) _∈_ Φ( _tk_ + _TS, x_ ( _tk_ + _TS_ )) _over the interval T_ = [ _tk_ + _TS, ∞_ ) _is a_ _**backup trajectory** to a set B ⊂X if the following two conditions hold:_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0003-12.png)



![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0003-13.png)


The backup trajectory is dynamically feasible and enters a backup set within _TB_ seconds after the switching time _TS_ . After entering _B_ , the trajectory remains in _B_ for all time because the control policy _π[B]_ renders _B_ controlled-invariant. 

Note that the backup trajectory is not required to satisfy constraints (4) – the validation step of the candidate trajectories will filter out unsafe backup trajectories. In general, finding a backup trajectory from any initial condition to a backup set is a key step in the gatekeeper framework, which is covered in the next subsection on ReRoot. 

A candidate trajectory follows the nominal trajectory then switches to a backup trajectory. 

**Definition 6** (Candidate Trajectory) **.** _At time tk ∈_ R _and starting from xk ∈X , let the nominal trajectory be_ ( _p_[nom] _k , u_[nom] _k_ ) _∈_ Φ( _tk, xk_ ) _. Let tkS_ = _tk_ + _TS and TS_ = [ _tk, tkS_ ) _. For any switching time TS ∈_ [0 _, TH_ ] _, the backup trajectory is_ ( _p_[nom] _k , u_[nom] _k_ ) _∈_ Φ( _tkS, p_[nom] _k_ ( _tkS_ )) _. A_ _**candidate trajectory**_ ( _p_[can] _k[, u] k_[can] ) _∈_ Φ( _tk, xk_ ) _with switching time TS is defined as_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0003-18.png)


A candidate trajectory is valid if it satisfies all constraints 

at every point along the trajectory and reaches a budget renewal set in finite time. 

**Definition 7** (Valid Trajectory) **.** _A candidate trajectory is_ _**valid** if it remains in the known safe set:_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-02.png)


_the solution to_ (3) _remains below the budget B:_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-04.png)


_and the trajectory reaches Rk:_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-06.png)


Finally, the committed trajectory is chosen to be the valid trajectory that maximizes _TS_ . If no committed trajectory can be found, the previously committed trajectory is followed. 

**Definition 8** (Committed Trajectory) **.** _At iteration k, the set of valid candidate trajectories parameterized by TS is_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-09.png)



![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-10.png)


_If Ik_ = _∅, the_ _**committed trajectory** is_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-12.png)


The following assumption is required for the inductive recursive feasibility property of gatekeeper. 

**Assumption 2.** We are given an initial dynamically feasible valid candidate trajectory _p_[can] 0 _[,T][S]_ which by definition satisfies all safety and budget constraints.[1] 

Now we can state the following theorem which shows that gatekeeper guarantees constraint satisfaction for all time. 

**Theorem 1.** _Suppose p_ 0[can] _[,T][S] is a dynamically feasible candidate trajectory defined on_ [ _t_ 0 _, ∞_ ) _that is valid by Def. 7 for some TS ≥_ 0 _. If p_[com] _k is determined via Def. 8, then_ 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-17.png)


_Proof._ The proof by induction is based on Theorem 1 in [16]. _Base Case:_ Let _k_ = 0. Since _p_ 0[can] _[,T][S]_ is valid, it is committed as _p_[com] 0 = _p_[can] 0 _[,T][S]_ . Then for the committed trajectory, 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-19.png)


> 1This assumption is not restrictive to satisfy in practice. The initial candidate trajectory can be arbitrarily short and planned within the known safe set, as long as it ends in a backup set. For example, in our case study in Section IV, the initial candidate trajectory is a short out-and-back loop that stays within the initial field of view of the UAV and returns to the controlled-invariant orbit. 

where _t_ 0 _,B_ = _t_ 0 + _TS_ + _TB_ . We used the fact that _R_ 0 is a backup set by Definition 2 and is thus controlled invariant. Hence, _p_[com] 0 satisfies all constraints for all time. Then for the budget state solution to (3) with _p_ ( _t_ ) and the corresponding _u_ ( _t_ ), 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-22.png)


_Induction Step:_ Now suppose the claim in Theorem 1 is true for some _k ∈_ N. To show the claim holds for _k_ + 1, consider the two possible definitions for _p_[com] _k_ +1[from] Definition 8: 

_Case 1:_ If _Ik_ +1 = _∅_ , then 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-25.png)


_Case 2:_ If _Ik_ +1 = _∅_ , the committed trajectory is 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-27.png)


Therefore, _p_[com] _k_ ( _t_ ) _∈S ∀t ∈_ [ _tk, tk_ +1) _, ∀k ∈_ N = _⇒ p_ ( _t_ ) _∈S ∀t ≥ t_ 0. Moreover, the solution to (3) with the corresponding _p_ ( _t_ ) and _u_ ( _t_ ) satisfies _b_ ( _t_ ) _≤ B ∀t ≥ t_ 0. 

We have shown the gatekeeper framework guarantees constraint satisfaction when paired with a suitable backup policy that ensures all candidate trajectories reach _Rk_ . An open challenge is how to construct a general backup policy that applies to a wide range of nonlinear system dynamics and non-convex safety constraints. To address this challenge, we introduce an algorithm to efficiently construct backup trajectories as the robot gathers information in the environment. 

## _B. ReRoot for Backup Trajectory Construction_ 

We leverage the well-known RRT* path planner in a novel manner to propose a sampling-based algorithm called ReRoot that efficiently generates a dynamically feasible trajectory from any location to a backup set in which the budgeted resource is renewed. 

_1) Backup Trajectory Generation Problem:_ Consider a valid candidate trajectory _p_ ( _t_ ) and the corresponding budget state prediction _b_ ( _t_ ). Let the pre-jump budget state be the one-sided limit as _t_ approaches _tkB_ from below: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0004-33.png)


where _tkB_ = _tk_ + _TS_ + _TB_ is the finite time when _p_ reaches _Rk_ . For any switch time _TS_ , the ideal backup trajectory is the one that minimizes the budget expenditure. The goal is to find such a backup trajectory to form the gatekeeper candidate trajectory. 

**Problem 2.** _At the k-th iteration and for a given switch time TS, given the known budget renewal set Rk at time tk, first return a set of dynamically feasible trajectories starting at p_[can] _k[,T][S]_ ( _tkS_ ) _and reaching Rk while remaining in the known_ 

**Algorithm 2:** Main Autonomy Loop 

|**1**|_Gk_|_Gk_|=InitReRoot(_R_0)||
|---|---|---|---|---|
|**2 **|**for**||_k ∈_[1_, . . . , K_] **do**||
|**3**|||_Fk, Rk ←_UpdateFreeSpace()||
|**4**|||**if** _Rk ∩Rk−_1 =_∅_**then**||
|**5**|||AddRootNodes(_Gk, Rk ∩Rk−_1)||
|**6**|||GrowReRoot(_Gk, Rk, Fk, n_update)||
|**7**|||_p_com<br>_k_<br>=gatekeeper(_p_nom<br>_k_|_, Gk, x_(_tk_)_, b_(_tk_))|
|**8**|||Track _p_com<br>_k_||
|**9**|||Update _b_(_t_) via (3)||



_safe set Fk. Select among them the trajectory p_[bck] _k[,T][S] with minimal budget expenditure b[−] ._ 

_2) ReRoot (Reverse Rooted Forest):_ We build a graph _Gk_ = ( _Vk, Ek_ ) with a set of nodes _Vk ⊂X_ and a set of edges _Ek ⊂Vk × Vk_ . The underlying algorithm for building _Gk_ is either the standard RRT* algorithm [18], or extensions of RRT* that attempt to generate kinodynamically feasible paths [19], [20]. The novelty in our approach is the manner of initialization and interpretation of the generated graph _Gk_ . Algorithm 2 details the overall autonomy algorithm that runs at each iteration _k_ , including the novel ReRoot initialization and growth steps. We summarize the key steps of ReRoot: 

- **Root Nodes:** The graph _Gk_ is a rooted forest, i.e., a union of disjoint rooted trees where all root nodes are in the renewal set _Rk_ . The initialization step, Algorithm 2, creates the set of root nodes _V_ 0 in _R_ 0. During the mission, further updates via Algorithm 2 add more root nodes to _Vk_ in the expanded renewal set _Rk_ . The root nodes serve as the endpoints of the backup trajectories. 

- **Online Growth:** In Algorithm 2 at each iteration _k_ , the RRT* algorithm is used to add _n_ update nodes to _Gk_ , including the standard rewiring step. The path cost function used in RRT* is the budget dynamics (3) evaluated along the path. During the rewiring step, a node can switch trees, meaning that the path to the root of the new tree has a lower cost than the node’s path to its previous root node. 

- **Path of Waypoints:** From any node _v ∈Vk_ in the forest, there is a single path of waypoints _W_ ( _v_ ) to a root node in _Rk_ , which is not necessarily dynamically feasible. This path is used to generate a dynamically feasible trajectory by forward propagation of the closedloop dynamics, which we describe below. This step occurs in Algorithm 1 of Alg. 1, called at each switching time _TS_ . 

**Remark 1.** Some popular variants of RRT/RRT* involve growing two trees with one root at the initial location and one at the goal location [21]–[23]. By contrast, ReRoot grows multiple trees by placing new roots as more components of the renewal set _Rk_ are discovered online. 

Next, we describe the in further detail the process of extracting a backup trajectory from the ReRoot graph during the gatekeeper candidate trajectory propagation 

step (Algorithm 1 of Algorithm 1). 

_3) Backup Trajectory Generation:_ Denote _d_ : _Vk →_ R _≥_ 0 as the depth of a node, which is the number of edges between _v_ and the root of its tree. A root node has depth _d_ = 0. For _v ∈Vk_ , define _W_ ( _v_ ) = _{v, P_ ( _v_ ) _, P_[2] ( _v_ ) _, . . . , P[d]_ ( _v_ ) _}_ (19) 

as the set of waypoints from _v_ to the root of its tree, where _P_ : _Vk →Vk_ is the parent node of _v_ . Let _V_ near be the set of all nodes within a ball of radius _R >_ 0 of the desired starting location of the backup trajectory, that is, 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0005-12.png)


Then, for each _v ∈V_ near, we generate the corresponding trajectory ( _pv, uv_ ) by propagating the closed loop trajectory of tracking the waypoints _W_ ( _v_ ) over the horizon [ _tkS, tkB_ ]: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0005-14.png)


where _π[T]_ : _X ×_ 2 _[V] k[→U]_[is][a][waypoint][tracking][controller][2][,] e.g. see [24]–[26]. 2 _[V] k_[is][the][power][set][of] _[V][k]_[,][i.e.,][the][set][of] all sets of _Vk_ . This forms a set _Nk[T][S] ⊂_ Φ( _tkS, p_[nom] _k_ ( _tkS_ )) of _|V_ near _|_ trajectories. Additionally, let _b[−] v_[be][the][budget][state] expenditure over the trajectory _pv_ by solving (3). Finally, the trajectory with minimal _b[−] v_[that is safe for all time is selected] as the backup trajectory: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0005-16.png)


The resulting candidate trajectory _p_[can] _k[,T][S]_ is validated by Definition 7, i.e., checking that _b[−] ≤ B_ by forward propagating (3) along _p_[can] _k[,T][S]_ . If there does not exist a feasible backup trajectory for a given switching time _TS_ , then the gatekeeper algorithm decrements _TS_ until either a feasible backup trajectory is found or _TS_ = 0 and the previous committed trajectory _p_[com] _k−_ 1[is][selected][as][the][next] committed trajectory. 

In summary, we solve Problem 2 by selecting the backup trajectory of minimal budget expenditure among a set of potential backup paths in the ReRoot forest. Through the forward propagation in (21) and the validation step in (23), we show that the backup trajectory is dynamically feasible and safe by construction. Finally, the gatekeeper committed validation step checks budget constraint satisfaction of the candidate trajectory. 

## IV. SIMULATION CASE STUDY 

We evaluate our method in a simulation case study of a fixed-wing UAV flying in a GNSS-denied environment, using visual-inertial odometry to estimate its position. The horizontal planar dynamics are modeled as a Dubins vehicle: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0005-21.png)


> 2The path is not required to be tracked perfectly. Safety violations of the propagated trajectory is checked in the validation step. 

where [ _rN , rE_ ] _[⊤] ∈_ R[2] is the horizontal position in a NorthEast-Down (NED) coordinate frame, _ψ ∈_ [0 _,_ 2 _π_ ) is the heading, _V >_ 0 is a fixed velocity and _u_ is the input turn rate. _u_ is constrained by the minimum turn radius of the UAV, _ρ >_ 0, such that _u ∈U_ = [ _−[V] ρ[,][V] ρ_[]][. For simplicity and] visualization purposes, we constrain the UAV to fly at a fixed altitude, but our method extends trivially to 3D trajectories, or for more complicated dynamics. 

The UAV’s velocity is _V_ = 10 m/s and minimum turn radius is _ρ_ = 10 m, which corresponds to a _∼_ 45° bank angle. The sensor field of view (FoV) is defined by a radius of 60 m and an angle of 90°. The perception and mapping module runs at 5 Hz. The objective is to reach the randomly chosen goal location within the 250 m _×_ 200 m mission domain. The mission requirements are as follows: 

- **(Safety constraint)** Maintain at least _Nf_ = 8 visual features in the FoV between successive camera frames for robust feature tracking. 

- **(Budget constraint)** Maintain an absolute position error (error bound on position) below _B_ = 9 m. 

Note that the safety constraint is difficult to write in equation form, e.g., _h_ ( _x_ ) _≤_ 0, and is not differentiable. It is however easy to verify algorithmically. We assume there exist some visual landmarks that reset position error to zero when the UAV can see them. We assume that the position error is proportional to distance traveled, with an error rate of 3%, i.e, 0.03 m of error per 1 m traveled, based on [27]. 

We write the safe set as 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0006-06.png)


where FeaturesInFoV : _X →_ N is the number of visible features at state _x_ . We assume no prior knowledge of the feature locations. The UAV maps the features as it flies through the environment and builds _Fk_ . The budget state models the growth of localization error as 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0006-08.png)


We define the budget renewal set to have subsets _R[i]_ at the starting location, a mid-point landmark (unknown to the UAV at the mission start time), and around the known goal location. Since the UAV cannot hover at a single location under the dynamics (24), we define _R_ as a circular counterclockwise orbit of radius _ρ_ around the landmarks. _R_ is controlled invariant under the constant control input _u_ = _−[V] ρ_ and reachable from nearby states, i.e., a backup set. The definition for _R[i]_ is as follows: 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0006-10.png)


where _lN[i]_[and] _[l] E[i]_[are][the][north][and][east][positions][of][the] _[i]_[-] th landmark. All backup trajectories must end in a subset _R[i]_ , which means the UAV can orbit indefinitely while not accumulating localization error. 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0006-12.png)


Fig. 3. Top-down view of field environment from the VPAIR database [28]. The white dots are visual odometry features. Note the lack of features in certain areas. The orange circle is the starting location. The yellow circle is the goal location. The white circle is a landmark. The nominal trajectory in black is the path of minimum distance, which becomes unsafe at the red “!”. The magenta line is the _omniscient_ trajectory, i.e., has knowledge of all feature locations, that minimizes distance while satisfying the safety and budget constraints. 

The simulated environment is a top-down image of a field taken from an airplane as part of the VPAIR database [28] and we create the set of features using Good Features to Track [29], as shown in Figure 3. The mission domain is a 265 m _×_ 200 m region. This environment presents a challenging setting for visual odometry, as certain regions of the field contain sparse or no discernible features. gatekeeper with ReRoot ensures that the UAV does not enter these unsafe regions. In the simulation with gatekeeper and ReRoot, the UAV has no knowledge of feature locations _a priori_ and maps them online when they enter the FoV. The mid-field landmark is also unknown to the UAV and is discovered during the mission. We further discuss the trajectories in Figure 3 in the results subsection below. 

For the nominal planner, we use RRT* in a similar manner to the method in [30], which facilitates replanning from any location in the map and returns a trajectory that is dynamically feasible for the Dubins dynamics (24). 

We initialize ReRoot around the starting location to form a small tree of safe backups that return to the initial orbit. Then, at 1 Hz, nodes are added based on the newly mapped features to extend the tree into the known safe set. As landmarks are discovered, a root node is placed and nearby nodes automatically connect to the new tree. 

The Dubins dynamics in (24) allows fast backup trajectory generation because the edges of ReRoot represent dynamically feasible subpaths. Given two nodes _v_ 1 _, v_ 2 _∈Vk_ , the Dubins path of minimum distance is unique and is found algebraically [31]. The path of waypoints _W_ ( _v_ ) is dynamically feasible and the budget state _b_ ( _t_ ) along the backup trajectory is the node cost of _v_ , which is used when building ReRoot to determine the parent of a new node. 

Figure 3 depicts the nominal trajectory from the start to the goal, which becomes unsafe as there are fewer than _Nf_ = 8 features in the FoV. We include for comparison the _omniscient_ trajectory that satisfies the safety and budget 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0007-00.png)


Fig. 4. (a)-(d) Visualization of the simulated experiment of gatekeeper with ReRoot at various times in the mission. The features seen by the UAV are the white dots. The orange dot is the starting location, the gray dot is a landmark, and the yellow dot is the goal location. The colored thin lines are the branches of the ReRoot forest. The blue line is the UAV’s path up to time _t_ . The black line is the unsafe part of the nominal trajectory, and the red line is the nominal component of the committed trajectory, which is replanned from the UAV position when the committed trajectory deviates from the nominal. The green line is the backup component of the committed trajectory and reaches a budget renewal set. (e) Value of the budget state _b_ (absolute position error) over time, which resets whenever the UAV reaches a budget renewal set. The budget never exceeds the maximum allowed value of 9 m. (f) Number of features in the FoV over time, which is never below the minimum _Nf_ = 8. The gray refers to when the UAV is at a landmark. 


![](1_survey/papers/md/Cherenson2025Autonomy_figs/Cherenson2025Autonomy.pdf-0007-02.png)


Fig. 5. (a) Simulation result of the same setup as in Figure 4 but with a budget constraint of 5 m of localization error. (b) Despite never reaching the goal, the budget constraint is always satisfied and (c) the safety constraint is also always satisfied. A limit cycle-like behavior is observed, illustrating that gatekeeper can successfully prevent the robot from leaving the safe set when the mission cannot be executed safely. 

constraints in which the feature locations are known _a priori_ . 

The code and animations of the simulation are available here[3] . In the simulation, we observe that the UAV reaches the goal while satisfying all constraints in Figure 4. Figure 4a shows that the nominal trajectory across the sparse field is found to be unsafe, so a short backup trajectory is planned to return to its orbit. In Figure 4b, the UAV has not mapped enough of the area around the mid-point landmark to reach it safely and must return to the starting location to reset the localization error. Then, in Figure 4c, the UAV reaches the landmark using the ReRoot tree rooted at the landmark. Finally, in Figure 4d, the UAV is able to reach the goal location with a committed trajectory back to the landmark. Figure 4e shows the position error over time which never exceeds the budget constraint. Figure 4f shows the number of visible features over time, showing that the safety constraint is always satisfied. Table I shows the computation times of 

TABLE I 

COMPUTATION TIMES PER ITERATION 

|**Component**|**Mean [ms]**|**Std. Dev. [ms]**|
|---|---|---|
|ReRoot|2.90|7.17|
|gatekeeper|2.52|4.48|



one iteration of Algorithm 2 in Algorithm 2 for ReRoot and one iteration of Algorithm 2 for gatekeeper. 

The behavior of the UAV trajectory in Figure 4 shows the exploratory effects of gatekeeper. Since following the nominal trajectory to the goal is found to be unsafe, the UAV turns back towards the start. During the turn, it maps more features and is able to extend further into the newly mapped known safe set. Eventually, the budget constraint forces the return to the start to renew the accumulated error. Then, the nominal trajectory can be followed for a longer time as the known safe set has been mapped. This process continues until the UAV reaches the goal while mapping its environment. The shape of the resulting trajectory resembles 

3https://github.com/dcherenson/budget-constrained-planning 

the omniscient path in Figure 3 with the addition of multiple return trips to landmarks. 

We also simulate the mission with a lower, more challenging budget of _B_ = 5 m of accumulated localization error, which makes the task of reaching the goal while satisfying all constraints infeasible. In Figure 5a, the UAV is unable to reach the landmark or the goal without exceeding the limit. The resulting pattern is caused by the UAV following the nominal trajectory until gatekeeper prevents the UAV from continuing to avoid exceeding the budget, then returning to the home landmark, and the cycle continues. Figure 5b and Figure 5c show that the safety and budget constraints are satisfied, despite this infinite looping behavior, which demonstrates the guaranteed constraint satisfaction. 

## V. CONCLUSION 

In this paper, we proposed an architecture to guarantee safety and budget constraints throughout a mission in an environment where the safe set is built on-the-fly. The key contribution is ReRoot, a sampling-based backup planning framework that augments the gatekeeper architecture to construct backup policies, which are needed for guaranteeing constraint satisfaction. By growing multiple reverse RRT* trees rooted in renewal sets, ReRoot efficiently generates trajectories that satisfy constraints while minimizing resource expenditure. The efficacy of our approach was demonstrated in simulation with a case study of a fixed-wing UAV in a GNSS-denied environment navigating to a goal location. The safety constraint was to maintain a minimum of 8 visual features in the FoV and the budget constraint was to limit the localization error to below 9 m. gatekeeper with ReRoot allowed the UAV to explore and map features while always satisfying the budget and safety constraints. 

Future work could include extending our method of backup trajectory construction to time-varying safe sets, e.g., avoiding a dynamic obstacle, and time-varying budget renewal sets, e.g., a mobile charging station. Also of interest would be to incorporate multiple budget constraints into ReRoot and form a set of Pareto optimal backup trajectories. The active budget constraint in the gatekeeper iteration could then determine which backup to take. 

## REFERENCES 

- [1] A. Kumar and A. Vladimirsky, “An efficient method for multiobjective optimal control and optimal control subject to integral constraints,” _Journal of Computational Mathematics_ , pp. 517–551, 2010. 

- [2] R. Takei, W. Chen, Z. Clawson, S. Kirov, and A. Vladimirsky, “Optimal control with budget constraints and resets,” _SIAM Journal on Control and Optimization_ , vol. 53, no. 2, pp. 712–744, 2015. 

- [3] N. Tsiogkas and D. M. Lane, “Dcop: Dubins correlated orienteering problem optimizing sensing missions of a nonholonomic vehicle under budget constraints,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 4, pp. 2926–2933, 2018. 

- [4] Y. Yang, J. Khalife, J. J. Morales, and Z. M. Kassas, “Uav waypoint opportunistic navigation in GNSS-denied environments,” _IEEE Transactions on Aerospace and Electronic Systems_ , vol. 58, no. 1, pp. 663– 678, 2021. 

- [5] K. B. Naveed, D. Agrawal, C. Vermillion, and D. Panagou, “Eclares: Energy-aware clarity-driven ergodic search,” in _IEEE International Conference on Robotics and Automation_ , 2024, pp. 14 326–14 332. 

- [6] S. D. Bopardikar, B. Englot, and A. Speranzon, “Multi-objective path planning in GPS denied environments under localization constraints,” in _American Control Conference (ACC)_ , 2014, pp. 1872–1879. 

- [7] M. A. Gilles and A. Vladimirsky, “Evasive path planning under surveillance uncertainty,” _Dynamic Games and Applications_ , vol. 10, no. 2, pp. 391–416, 2020. 

- [8] Q. Lin, B. Tang, Z. Wu, C. Yu, S. Mao, Q. Xie, X. Wang, and D. Wang, “Safe offline reinforcement learning with real-time budget constraints,” in _International Conference on Machine Learning (ICML)_ , 2023, pp. 21 127–21 152. 

- [9] G. Notomista, S. F. Ruf, and M. Egerstedt, “Persistification of robotic tasks using control barrier functions,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 2, pp. 758–763, 2018. 

- [10] K. L. Hobbs, M. L. Mote, M. C. Abate, S. D. Coogan, and E. M. Feron, “Runtime assurance for safety-critical systems: An introduction to safety filtering approaches for complex control systems,” _IEEE Control Systems Magazine_ , vol. 43, no. 2, pp. 28–65, 2023. 

- [11] H. Kim, H. Yoon, W. Wan, N. Hovakimyan, L. Sha, and P. Voulgaris, “Backup plan constrained model predictive control,” in _IEEE Conference on Decision and Control (CDC)_ . IEEE, 2021, pp. 289–294. 

- [12] B. Thananjeyan, A. Balakrishna, S. Nair, M. Luo, K. Srinivasan, M. Hwang, J. E. Gonzalez, J. Ibarz, C. Finn, and K. Goldberg, “Recovery RL: Safe reinforcement learning with learned recovery zones,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 3, pp. 4915– 4922, 2021. 

- [13] J. Kiemel, L. Righetti, T. Kr¨oger, and T. Asfour, “Safe reinforcement learning of robot trajectories in the presence of moving obstacles,” _IEEE Robotics and Automation Letters_ , 2024. 

- [14] L. Jung, A. Estornell, and M. Everett, “Contingency constrained planning with MPPI within MPPI,” in _Learning for Dynamics and Control (L4DC)_ , 2025. 

- [15] F. Blanchini, “Set invariance in control,” _Automatica_ , vol. 35, no. 11, pp. 1747–1767, 1999. 

- [16] D. R. Agrawal, R. Chen, and D. Panagou, “gatekeeper: Online safety verification and control for nonlinear systems in dynamic environments,” _IEEE Transactions on Robotics_ , vol. 40, pp. 4358–4375, 2024. 

- [17] D. R. Agrawal and D. Panagou, “Online safety under multiple constraints and input bounds using gatekeeper: Theory and applications,” _IEEE Control Systems Letters_ , 2025. 

- [18] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” _The International Journal of Robotics Research_ , vol. 30, no. 7, pp. 846–894, 2011. 

- [19] A. Perez, R. Platt, G. Konidaris, L. Kaelbling, and T. Lozano-Perez, “LQR-RRT*: Optimal sampling-based motion planning with automatically derived extension heuristics,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2012, pp. 2537–2542. 

- [20] D. J. Webb and J. Van Den Berg, “Kinodynamic RRT*: Asymptotically optimal motion planning for robots with linear dynamics,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2013, pp. 5054–5061. 

- [21] J. J. Kuffner and S. M. LaValle, “RRT-connect: An efficient approach to single-query path planning,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2000, pp. 995–1001. 

- [22] M. Jordan and A. Perez, “Optimal bidirectional rapidly-exploring random trees,” 2013. 

- [23] A. H. Qureshi and Y. Ayaz, “Intelligent bidirectional rapidly-exploring random trees for optimal motion planning in complex cluttered environments,” _Robotics and Autonomous Systems_ , vol. 68, pp. 1–11, 2015. 

- [24] M. Breivik and T. I. Fossen, “Guidance-based path following for autonomous underwater vehicles,” in _MTS/IEEE OCEANS_ , 2005, pp. 2807–2814. 

- [25] N. H. Amer, H. Zamzuri, K. Hudha, and Z. A. Kadir, “Modelling and control strategies in path tracking control for autonomous ground vehicles: A review of state of the art and challenges,” _Journal of intelligent & robotic systems_ , vol. 86, no. 2, pp. 225–254, 2017. 

- [26] B. Rub´ı, R. P´erez, and B. Morcego, “A survey of path following control strategies for uavs focused on quadrotors,” _Journal of Intelligent & Robotic Systems_ , vol. 98, no. 2, pp. 241–265, 2020. 

- [27] G. Ellingson, K. Brink, and T. McLain, “Relative visual-inertial odometry for fixed-wing aircraft in GPS-denied environments,” in _IEEE/ION Position, Location and Navigation Symposium (PLANS)_ , 2018, pp. 786–792. 

- [28] M. Schleiss, F. Rouatbi, and D. Cremers, “Vpair-aerial visual place recognition and localization in large-scale outdoor environments,” _arXiv preprint arXiv:2205.11567_ , 2022. 

- [29] J. Shi and C. Tomasi, “Good features to track,” in _IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 1994, pp. 593–600. 

- [30] D. Ferguson, N. Kalra, and A. Stentz, “Replanning with RRTs,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2006, pp. 1243–1248. 

- [31] A. M. Shkel and V. Lumelsky, “Classification of the dubins set,” _Robotics and Autonomous Systems_ , vol. 34, no. 4, pp. 179–202, 2001. 

