---
citation_key: Grothe2022STRRT
arxiv_id: 2203.02176
arxiv_url: "https://arxiv.org/abs/2203.02176"
title: "ST-RRT*: Asymptotically-Optimal Bidirectional Motion Planning through Space-Time"
authors_short: "Francesco Grothe et al."
year: 2022
direction_tag: D_asymptotically_optimal_sampling;O_dense_forest_narrow_passage
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:35:06Z
origin: ai+web
reviewed: false
---

a

C

# ST-RRT\*: Asymptotically-Optimal Bidirectional Motion Planning through Space-Time

Francesco Grothe<sup>1</sup>, Valentin N. Hartmann<sup>1,2</sup>, Andreas Orthey<sup>1</sup>, Marc Toussaint<sup>1</sup>

Abstract— We present a motion planner for planning through space-time with dynamic obstacles, velocity constraints, and unknown arrival time. Our algorithm, Space-Time RRT\* (ST-RRT\*), is a probabilistically complete, bidirectional motion planning algorithm, which is asymptotically optimal with respect to the shortest arrival time. We experimentally evaluate ST-RRT\* in both abstract (2D disk, 8D disk in cluttered spaces, and on a narrow passage problem), and simulated robotic path planning problems (sequential planning of 8DoF mobile robots, and 7DoF robotic arms). The proposed planner outperforms RRT-Connect and RRT\* on both initial solution time, and attained final solution cost. The code for ST-RRT\* is available in the Open Motion Planning Library (OMPL).

## I. INTRODUCTION

Motion planning is a fundamental challenge in robotics [1]. In many real-world applications, obstacles change positions over time and goals are only valid at specific times. For applications such as multi-robot assembly, multiple motion scheduling subproblems need to be solved [2]. Assuming that obstacle trajectories are given a priori, the subproblems can be modelled as navigation through dynamic environments. Mathematically, this is formulated as planning through a space-time state space.

Efficient and optimal planning through space-time raises three fundamental challenges. First, since goal arrival times are unknown upfront, it becomes difficult, yet crucial, to define and adjust the time range in a coordinated and meaningful way. The second challenge is the representation of kinodynamic constraints in the planning model. Whether a movement is possible depends on kinematic parameters, velocity, and acceleration. Lastly, robots should minimize arrival time. Arrival time is crucial for long-horizon planning problems, where optimization of intermediate arrival times is one of the central challenges [2]. These challenges make planning through space-time a demanding problem. We are not aware of any sampling-based method which either op erates in unbounded space-time or is asymptotically optimal with respect to shortest arrival time.

To address those challenges, we develop Space-Time RRT\* (ST-RRT\*). The basic operating principle of ST-RRT\* is illustrated in Fig. 1: (a) We compute an initial estimate of a feasible goal time (blue dashed line), and grow both a forward tree from the start state (blue), and a set of reverse trees from the goal regions (red). If no solution is found given a certain number of samples, the upper time limit in which we generate samples is increased (b). If a solution (orange) is found (c), the parts of the trees that can not lead to an improved solution are pruned. This process continues to improve the solution path, and tighten the upper time bound until a termination condition is reached (d).

![](Grothe2022STRRT_figs/0091f64805949ded8cfb5bff748f0ad66e7662d20ed388e5874f47322f48eb94.jpg)

![](Grothe2022STRRT_figs/f57d722390719d8de208a3e8885c388d48dd3164cd685535f0a3928b9461b2cf.jpg)

b  
![](Grothe2022STRRT_figs/07da1e66cfd513d20c2f6a8b6c0412f846c930c34dc32533cbfb738c3a74ab06.jpg)

d  
![](Grothe2022STRRT_figs/3d5e55218b6fd1393ae0e984b09f33f43a625eef556708828a0f4319a589fa14.jpg)  
Fig. 1: Four snapshots of ST-RRT\* in $\mathbb { R } ^ { 1 + 1 }$ (one space, plus one time dimension). The forward tree is blue, the backward trees are red, obstacles are black, and the goal regions are yellow. (a) Using the initial batch of samples, no solution was found. (b) The upper bound of the time space (dashed line) is expanded, more goal nodes are sampled and the trees are grown. (c) An initial solution is found (orange), and the upper bound is decreased accordingly. (d) Parts of the trees that can not contribute to the solution anymore are pruned (lower opacity), and the final solution after convergence.

ST-RRT\* is a bidirectional motion planning algorithm that is probabilistically complete and asymptotically optimal with respect to shortest arrival time. ST-RRT\* is able to operate in unbounded time spaces and model velocity constraints. ST-RRT\* is inspired by RRT-Connect [3], with three changed components to attain the stated qualities in space-time. Our main contributions are:

• Progressive Goal Region Expansion: ST-RRT\* gradually increases the sampled time range to efficiently operate in unbounded time spaces. Simultaneously, we adjust the sampling densities over the time dimension to ensure a more uniform sampling distribution.

• Conditional Sampling: We develop a novel sampling method that prevents the sampling of states which cannot be part of a solution path due to velocity constraints.

• Simplified Rewiring: To obtain optimal solutions, states are rewired similar to $\mathrm { R R T ^ { * } }$ [4]. In contrast to $\mathrm { R R T ^ { * } }$ we perform a simplified rewiring step, where only nodes in the set of goal trees are rewired.

We demonstrate our algorithm on both abstract (planning for a disk in up to $\mathbb { R } ^ { 8 + 1 } )$ , and simulated robotic motion planning problems (both robotic arms and mobile robots).

## II. RELATED WORK

In the following two sections, we review literature on planning in dynamic environments and time-optimal path planning. For an exhaustive discussion of path planning methods we refer to [5] and [6] for an overview on (asymptotically optimal) sampling based path planning methods.

## A. Planning in Dynamic environments

Planning in dynamic environments can be roughly divided in two approaches. First, we have reactive methods, which work with the assumption that the trajectories of the moving obstacles are unknown, whereas the second category assumes full knowledge of the obstacles’ trajectories.

Reactive methods such as Execution-extended RRT [7], Closed-loop RRT [8], [9], RRTX [10] or Real-time RRT\* [11] are methods specifically developed for rapid replanning. Rapid replanning is necessary when previously computed paths become invalid during execution. Risk-RRT [12] incorporates predictions about the obstacles’ movement, and computes partial motion paths to keep the probability of a collision under a given threshold. However, frequent replanning is still needed as only partial paths are returned. Various methods exist to enable efficient replanning, i.e. to reuse as much prior work as possible from previously planned paths, or to establish coarse connectivity of the space, and only replan for dynamic obstacles ([13], [14], [15], [16]).

Contrary to reactive methods, the following methods assume full knowledge of obstacle trajectories, and thus do not rely on replanning. Time-Based RRT [17] expands the configuration state space by the time dimension and plans unidirectionally to a set of known goal states. However, knowledge of the specific time for each goal configuration is assumed, and only unidirectional planning is supported. Safe Interval Path planning [18] finds optimal paths with respect to shortest time by constructing a discrete search space with states defined by their configuration and a corresponding ‘safe interval’. However, a graph needs to be constructed for the entire state space, and thus it suffers the inherent problems: it is only feasible for problems with few dimensions.

In this work, we assume full knowledge of all paths of the moving obstacles, but no a priori knowledge of the arrival time, as is the case in multi-robot assembly planning tasks [2]. Thus, our method does not require replanning and is able to efficiently find feasible and time-optimal paths. Our method also enables to plan bidirectionally in unbounded time spaces, leading to a more efficient planner than other RRT-based planners in the space-time setting.

## B. Time-optimal Trajectory planning

A common approach to find kinodynamically feasible paths is based on path-velocity decomposition: first find a geometrically feasible path, and then find a valid timeparametrization for this path [19]. Extensions to this approach were presented e.g. in [20], which relaxes the quasistatic requirement. However, this approach is inapplicable here, as obstacles are dynamic and the time optimization on a fixed path might render it infeasible.

Other approaches to planning include optimization approaches (e.g. STOMP [21], or sequential convex optimization [22]), or extending the configuration space with velocity coordinates [23]. Optimization based approaches work well to incorporate complex constraints, but suffer from the well known non-convexity of the general planning problem. Furthermore, optimizing for arrival time is not straightforward. In general, these methods are not complete and therefore can not achieve global optimality.

Sampling based kinodynamic planning on the other hand, doubles the dimensionality of the state space we plan in, and thus makes planning with high DoF-robots slow or even infeasible. Since time is not taken into account explicitly, planning with dynamic obstacles is not straightforward.

By extending the configuration space with a time component, and planning and optimizing in this space-time state space, we retain these guarantees. Through usage of bidirectional planning, conditional sampling, and simplified rewiring, we achieve a high efficiency.

## III. THE SPACE-TIME RRT\* ALGORITHM

We consider the motion planning problem in space-time with unbounded arrival time. Our objective is to minimize arrival time under given velocity constraints. By adding a time dimension to the configuration space we obtain the Space-Time state-space ${ \mathcal { X } } \ = \ { \mathcal { Q } } \times { \mathcal { T } }$ , where is the underlying configuration state space and  is the time state space. Note that can be unbounded in time. Let $\mathcal { X } _ { \mathrm { f r e e } } \in \mathcal { X }$ be the obstacle-free subset of states, $x _ { \mathrm { s t a r t } }$ the start state, and $\chi _ { \mathrm { g o a l } } = \mathcal { Q } _ { \mathrm { g o a l } } \times \mathcal { T } _ { \mathrm { g o a l } }$ the goal region. In the following, we assume full knowledge of the obstacles’ trajectories, and plan for holonomic robots with a given maximum velocity. We define $v _ { \operatorname* { m a x } } \ \in \ \mathbb { R } ^ { | \mathcal { Q } | }$ as a vector containing the maximum velocity for each space component.

The goal is to compute a continuous path $p : [ 0 , 1 ] $ $\chi _ { \mathrm { f r e e } } .$ , such that $p ( 0 ) = x _ { \mathrm { s t a r t } } , p ( 1 ) \in \mathcal { X } _ { \mathrm { g o a l } } .$ and the velocity constraints are satisfied. We are interested in finding not only feasible, but paths which minimize the arrival-time, $c ( p ) = t _ { 1 }$ with $t _ { 1 }$ being the time element of $p ( 1 ) = ( q _ { 1 } , t _ { 1 } )$

In space-time, the distance that can be covered in a given time is constrained by $v _ { \mathrm { m a x } }$ and it is not possible to move backwards in time. Thus, we define our distance function d between two states, $x _ { 1 } = ( q _ { 1 } , t _ { 1 } )$ and $x _ { 2 } = ( q _ { 2 } , t _ { 2 } )$ as

```python
Algorithm 1 ST-RRT*
Input: X, x_start, X_goal, d, PTC, t_max, p_goal, P
1: Ta ← {x_start}; Tb ← ∅
2: B ← INITIALIZEBOUNDVARIABLES(P)
3: while ¬PTC do
4: B ← UPDATEGOALREGION(B, P, t_max)
5: if p_goal ≥ RND(0, 1) then
6: B ← SAMPLEGOAL(x_start, X_goal, T_goal, t_max, B)
7: x_rand ← SAMPLECONDITIONALLY(x_start, X, B, d)
8: if not EXTEND(Ta, x_rand, d) = Trapped then
9: B.samplesInBatch += 1
10: B.totalSamples += 1
11: REWIRETREE(Ta, T_goal, x_new)
12: if CONNECT(Tb, x_new, d) = Reached then
13: solution ← UPDATESOLUTION(x_new)
14: t_max ← COSTPATH(solution)
15: B.batchProbability ← 1
16: PRUNETREES(t_max, Ta, Tb)
17: SWAP(Ta, Tb)
18: return solution
```

$$
d (x _ {1}, x _ {2}) = \left\{ \begin{array}{l l} \lambda d _ {\mathcal {Q}} (q _ {1}, q _ {2}) + (1 - \lambda) (t _ {2} - t _ {1}), \\ \quad \text { if } t _ {1} <   t _ {2}, v ^ {i} \leq v _ {\max} ^ {i} \forall i \in [ 1, | \mathcal {Q} | ] \\ \infty , & \text { else }. \end{array} \right.\tag{1}
$$

where $d _ { \mathcal { Q } }$ is the intrinsic metric of the configuration space, $\lambda \in \mathsf { \Gamma } ( 0 , 1 )$ weights the importance of $d _ { \mathcal { Q } }$ with respect to the time-distance (but does not influence optimality), and $v ^ { i }$ is the required speed in dimension i, such that $q _ { 2 }$ can be reached from $q _ { 1 }$ in time $t _ { 2 } - t _ { 1 }$ . As d is not symmetric, it is only a pseudometric.

## A. Algorithm

The algorithmic details of ST-RRT\* are shown in Algorithms 1–5. In addition to ${ \mathcal { X } } , x _ { \mathrm { s t a r t } } , \ x _ { \mathrm { g o a l } } .$ , and d it requires a planner termination condition PTC, a time bound $t _ { \mathrm { m a x } } \in$ $( 0 , \infty ]$ , a probability to sample a new goal $p _ { \mathrm { g o a l } } \in ( 0 , 1 ]$ , and several bound parameters contained in $P$ (see Section III-A.1). The basic framework is similar to RRT-Connect [3]: In each iteration a new goal is sampled with probability $p _ { \mathrm { g o a l } }$ (Line $5 \ \& \ 6 )$ . Then, a random state $x _ { \mathrm { r a n d } }$ is sampled (Line 7). If possible, the current tree $T _ { a }$ is expanded by the new state $x _ { \mathrm { n e w } }$ (i.e. the extension between $x _ { \mathrm { n e a r } }$ and $x _ { \mathrm { r a n d } } )$ and a connection from $x _ { \mathrm { n e w } }$ to the other tree $T _ { b }$ is attempted (Line 8 & 12). In case of a successful connection, the solution is updated (Line 13). Finally, $T _ { a }$ and $T _ { b }$ are swapped and the next iteration begins (Line 17). Our extensions to RRT-Connect are:

• Progressive Goal Region Expansion, which progressively enlarges the time component of the space (Line 4), and samples new goals for the goal tree (Line 6),

• Conditional Sampling (Line 7), which first samples a state from , and then samples a corresponding valid time, with which $x _ { \mathrm { r a n d } }$ is constructed, and

![](Grothe2022STRRT_figs/c33033500d9dc5faa7387b595f1a0974c86f263cdeab672333076495cfe8c8ab.jpg)  
Fig. 2: Illustration of the search trees after the same computation time with naive and weighted sampling strategy with similar numbers of samples (for naive sampling, not all samples are visible, and the time bound was increased beyond the shown range).

• Simplified Rewiring, which improves the solution (Line 11) by optimizing for minimal arrival time.

We also prune the trees (Line 16) to remove parts which cannot improve the solution anymore.

1) Progressive Goal Region Expansion: If the time-space <sub>T</sub> is unbounded it is difficult to generate samples distributed throughout the whole space. However, when imposing an arbitrary time-bound, the problem might become infeasible [24], [25]. Therefore, we expand the sampled goal region progressively whenever a new batch of samples is added. To do that, we introduce several parameters contained in the bound struct B: B.timeRange determines the time bound for goal sampling and B.batchSize determines after how many generated samples the expansion takes place. When a batch is full, B.timeRange is increased by P.rangeFactor and B.batchSize is increased accordingly.

With an increasing time-bound, the sample density is higher at the lower time values due to the previously generated samples. Figure 2 shows how naive sampling may lead to cases where it becomes increasingly unlikely to find any solution. Thus we use weighted sampling, where the old and newly expanded region are explicitly sampled with probability B.batchProbability and 1 <sub>−</sub> B.batchProbability, respectively, to ensure a uniform distribution over the total space.

Precisely, the Progressive Goal Region Expansion works as follows: The parameters P.rangeFactor, P.initialBatchSize, and P.sampleRatio are user-specified. All variables of B are initialized at the start (Algorithm 2) and updated during execution. While B.timeRange is used when the current goal region is sampled, B.newTimeRange is used to sample the newly expanded one. After the first expansion, B.newTimeRange is always higher than B.timeRange by a factor equal to P.rangeFactor (Alg. 3, Line 2 & 3). The minimum amount of the new batch size is given by (P.rangeFactor  1)  B.totalSamples. That is, when all samples of the new batch are placed in the new region, the overall distribution would be uniform over the time-space. To ensure that the old region is also sampled, B.batchSize is further increased by P.sampleRatio (0, 1) (Line 4). The probability to sample the old batch B.batchProbability is calculated in dependence of P.rangeFactor and P.sampleRatio (Line 5). Due to the exponential growth of the batch size, the choice of the configuration parameters is important for performance.

![](Grothe2022STRRT_figs/169f24f542308e3fa8ba5cd07e9bb9ee539d7a4eea3e0e9e78ec005871decd80.jpg)  
Fig. 3: The start and goal cones contain all states that can be reached from the start or can reach the goal respectively. The intersection contains all states that can be part of a solution.

To sample a goal state, its space component q is sampled first (Alg 4, Line 1). The lower and upper bounds for the time, t<sub>lb</sub> and $t _ { \mathrm { u b } } .$ , are calculated in dependence on whether the time is explicitly bounded (Line 4), the current region is sampled (Line 6), or the newly expanded one is sampled (Line 8). The sampling of nongoal-states is subject to the sampled goal states and therefore implicitly bounded by the time value of the sampled goal states (Section III-A.2).

```txt
Algorithm 2 InitializeBoundVariables
Input: P
1: B.timeRange ← P.rangeFactor
2: B.newTimeRange ← P.rangeFactor
3: B.batchSize ← P.initialBatchSize
4: B.samplesInBatch ← 0; B.totalSamples ← 0
5: B.batchProbability ← 1
6: B.goals ← ∅; B.newGoals ← ∅
7: return B
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 UpdateGoalRegion
Input: B, P,  $t_{max}$ 
1: if  $t_{max} = \infty$  and B.samplesInBatch = B.batchSize then
2: B.timeRange ← B.newTimeRange
3: B.newTimeRange *= P.rangeFactor
4: B.batchSize ←  $\frac{(P.\text{rangeFactor}-1)B.\text{totalSamples}}{P.\text{sampleRatio}}$ 
5: B.batchProbability ←  $\frac{1-P.\text{sampleRatio}}{P.\text{rangeFactor}}$ 
6: B.goals ← B.goals ∪ B.newGoals
7: B.newGoals ← ∅; B.samplesInBatch ← 0
8: return B
</div>

2) Conditional Sampling: Any state that can be part of a solution path must have a finite distance d to the start and at least one goal state. Due to velocity-constraints, only states in the intersection of the start and goal cones (see Fig. 3 for an illustration) meet this requirement. Thus, similar to

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4 SampleGoal

Input:  $x_{start}$ ,  $X_{goal}$ ,  $T_{goal}$ ,  $t_{max}$ , B
1:  $q \leftarrow \text{SAMPLEUNIFORM}(Q_{goal})$ 
2:  $t_{min} \leftarrow \text{LOWERBOUNDARRIVALTIME}(q_{start}, q)$ 
3: SAMPLEOLDBATCH  $\leftarrow \text{RND}(0, 1) \leq B.\text{batchProbability}$ 
4: if  $t_{max} \neq \infty$  then
5:  $t_{lb} \leftarrow t_{min};\quad t_{ub} \leftarrow t_{max}$ 
6: else if SAMPLEOLDBATCH then
7:  $t_{lb} \leftarrow t_{min};\quad t_{ub} \leftarrow t_{min} \cdot B.\text{timeRange}$ 
8: else
9:  $t_{lb} \leftarrow t_{min} \cdot B.\text{timeRange}$ 
10:  $t_{ub} \leftarrow t_{min} \cdot B.\text{newTimeRange}$ 
11: if  $t_{ub} &gt; t_{lb}$  then
12:  $t \leftarrow \text{SAMPLEUNIFORM}(t_{lb}, t_{ub})$ 
13:  $T_{goal} \leftarrow T_{goal} \cup \{(q, t)\}$ 
14: if SAMPLEOLDBATCH then
15: B.goals  $\leftarrow$  B.goals  $\cup \{(q, t)\}$ 
16: else
17: B.newGoals  $\leftarrow$  B.newGoals  $\cup \{(q, t)\}$ 
18: return B
</div>

Informed RRT\* [26], we only sample the region that can produce solutions. Ideally, one would sample directly from the union of intersections of start and goal velocity-cones.

However, as the explicit computation of the intersection is not possible for multiple goal states, we use Conditional Sampling: We first uniformly sample a configuration q (Alg 5, Line 2). Using $q ,$ we then sample a feasible time from the range of possible times conditioned upon $q .$ The range of possible times is dependent on $x _ { \mathrm { s t a r t } }$ and the previously sampled goal states. To sample more uniformly, we use two goal sets: B.goals for the current goal states and B.newGoals for the goal states in the newly expanded region. The time bounds $t _ { \mathrm { l b } } , \ t _ { \mathrm { u b } }$ are obtained by the minimal arrival time from the start configuration $q _ { \mathrm { s t a r t } }$ until $q$ (Line 3) and the maximum valid time given by:

$$
\begin{array}{c} \text { MAXVALIDTIME } (q _ {\text { rnd }}, G) = \\ \max _ {(q _ {g}, t _ {g}) \in G} \left(t _ {g} - \min _ {i} \frac {d _ {\mathcal {Q}} (q _ {\text { rnd }} ^ {i} , q _ {g} ^ {i})}{v _ {\text { max }} ^ {i}}\right) \end{array}\tag{2}
$$

The specific calculation of $t _ { \mathrm { l b } } , ~ t _ { \mathrm { u b } }$ is dependent on whether the current (Line 4) or the new region is sampled (Line 7).

3) Simplified Rewiring: To compute time-optimal solutions ST-RRT\* uses similar methods as $\mathrm { R R T ^ { * } }$ and preserves its property of asymptotic optimality. Equal to RRT\*, ST-RRT\* tries to rewire a set of states near to the newly added state, $x _ { \mathrm { n e w } }$ , after tree expansion. Contrary to RRT\*, rewiring is only performed in the goal trees. This is due to the fact that rewiring nodes in the start tree can never lead to a better arrival time in the path. Rewiring states in the start tree can not change their arrival time, whereas in the goal trees a node can be rewired to a root node with a smaller time value. One more deviation is the check of which nodes should be rewired. For all nodes in the goal trees simply the time value of their respective root node has to be considered.

```latex
Algorithm 5 SampleConditionally
Input: \( x_{\text{start}}, \mathcal{X}, B \)
1: repeat
2: \( q \leftarrow \text{SAMPLEUNIFORM}(\mathcal{Q}) \)
3: \( t_{\text{min}} \leftarrow t_{\text{start}} + \text{LOWERBOUNDARRIVALTIME}(q_{\text{start}}, q) \)
4: if \( \text{RANDOM}(0, 1) < B.\text{batchProbability} \) then
5: \( t_{\text{lb}} \leftarrow t_{\text{min}} \)
6: \( t_{\text{ub}} \leftarrow \text{MAXVALIDTIME}(q, B.\text{goals}) \quad \triangleright \text{eq (2)}
7: else
8: \( t_{\text{min}}^{*} \leftarrow \text{MAXVALIDTIME}(q, B.\text{goals}) \)
9: \( t_{\text{lb}} \leftarrow \text{MAX}(t_{\text{min}}, t_{\text{min}}^{*}) \)
10: \( t_{\text{ub}} \leftarrow \text{MAXVALIDTIME}(q, B.\text{newGoals}) \)
11: until \( t_{\text{lb}} < t_{\text{ub}} \)
12: \( t \leftarrow \text{SAMPLEUNIFORM}(t_{\text{lb}}, t_{\text{ub}}) \)
13: return \( (q, t) \)
```

## B. Proof Sketches

To prove probabilistic completeness in space-time, we distinguish between two cases. In case of bounded time, planning with a quasi-metric reverts to kinodynamic planning, where we refer to results from [27] and [28] for completeness proofs.

The second case is unbounded time: If a solution exists, there needs to be a feasible goal region at a finite time. Since we iteratively increase the upper bound, we will, eventually, have increased the goal region to include the feasible goal region. Due to the use of uniform sampling of the time range, there will be positive probability that the feasible goal region will be sampled. Since conditional sampling always gives a positive probability of sampling any open set, this makes ST-RRT\* retain probabilistic completeness [29].

Apart from probabilistic completeness, ST-RRT\* is also asymptotically optimal with respect to arrival time. Since ST-RRT\* is modelled after RRT-Connect, it can be made asymptotically optimal by tree rewiring [4], [30]. Inside the rewiring step, we connect newly added states to the nearest goal tree which minimizes arrival time. This ensures asymptotic optimality with respect to final arrival time.

## IV. EVALUATION

We compared ST-RRT\* to other planners on 4 different scenarios using the benchmarking capabilities of OMPL [31]. All evaluations were performed over 100 runs with different pseudorandom seeds of 30s each (if not stated otherwise). ST-RRT\* is compared to RRT-Connect<sup>1</sup> and RRT\* in spacetime using their OMPL implementations in default configuration. Since RRT\* and RRT-Connnect algorithms can not operate on unbounded time, three different time bounds are measured. The lowest time bound was determined according to the best solutions of ST-RRT\* and set to a higher value to ensure feasibility. Without knowing a solution this is generally not possible. For planning through Space-Time, most of the planners in OMPL [32] do not work either due to only working with metric spaces, only working with euclidean spaces, not supporting asymmetric distance function (e.g. due to using undirected graph structures), or were never able to find solutions in the specified runtime.

![](Grothe2022STRRT_figs/9e2c0b7f3b5dc062f4cc3f8a167c65ca655b66449fac728c3ca70ef3edbf7914.jpg)  
(a) Narrow passage in time $( \mathbb { R } ^ { 1 + 1 } )$

![](Grothe2022STRRT_figs/6809248cca7464861dd993c7f45f5a5c7d9c4363262079ad3cde5352d673930c.jpg)

![](Grothe2022STRRT_figs/c8a272d5044d6de7482235299453fe642f13923a4f4ce8a9d9e0e0aa01561d31.jpg)

(b) Rnd. moving obstacles (<sup>R2+1</sup>). Obstacle start in black, end position in grey.  
![](Grothe2022STRRT_figs/718099482fc93028c64ac7f468eba67d4405c279420c05ebaa2be5472708ab9a.jpg)  
(c) Mobile robots.  
(d) Robotic arms.  
Fig. 4: Illustrations of the scenarios: Starts are shown in blue, goals and goal regions in yellow, and obstacles in black. The dashed lines are the paths of the moving obstacles.

## A. Scenarios

We evaluate the method on the following scenarios<sup>2</sup>:

(i) Narrow passage: A point has to move from start configuration q<sub>0</sub> to goal configuration q<sub>F</sub> in an environment where the configuration space is split into two parts by an obstacle up to a certain point in time except for three narrow periods of time (Fig. 4a).

(ii) Cluttered space: A (hyper-)sphere has to move from q<sub>0</sub> to $q _ { F }$ in an environment with randomly moving obstacles (Fig. 4b).

(iii) Sequential mobile robot planning: A robot with a mobile base and a robot arm on top (<sup>R8</sup>) has to move from q<sub>0</sub> to q<sub>F</sub> in an environment with randomly distributed obstacles, and other moving mobile robots that move on a fixed trajectory (Fig. 4c). This is a common subproblem in prioritized multi robot planning [33].

(iv) Sequential robot arm planning: A robotic arm (<sup>R7</sup>) has to move from configuration q<sub>0</sub> to q<sub>F</sub> in an environment with previously planned panda robotic arms (Fig. 4d). Such a scenario may arise in e.g. simultaneous binpicking with multiple robots.

We show the narrow passage problem in $\mathbb { R } ^ { 1 + 1 }$ and $\mathbb { R } ^ { 8 + 1 }$ and the cluttered env. in $\mathbb { R } ^ { \bar { 2 } + 1 }$ and $\mathbb { R } ^ { 8 + 1 }$ . For the robotic settings, we test the planners in the $6 ^ { \mathrm { { t h } } }$ and the $1 1 ^ { \mathrm { t h } }$ agent (i.e. the previous 5, and 10 agents, respectively, already have a trajectory).

![](Grothe2022STRRT_figs/b8e3842df43d1e0e0cb72112f82a0e9cf6bec21a3c4466e2fd7e550e4051a9be.jpg)  
(a) Narrow passage in time: <sup>R1+1</sup>(b)

![](Grothe2022STRRT_figs/4ca406806ee8f06537e17677931e04618469977a81b2d6c1eda47d870a41c5f0.jpg)

![](Grothe2022STRRT_figs/078cd4d7c94f65354ddbeb52fa3ba19d6476eb2447a13bb0729158df2c46e5de.jpg)  
(c) Rnd. moving obstacles: <sup>R2+1</sup>

![](Grothe2022STRRT_figs/032cf4900096e1cef5484bbae37a28c4ad87fedf0b06d186ee27b0884eae07ba.jpg)  
(d) Rnd. moving obstacles: <sup>R8+1</sup>

![](Grothe2022STRRT_figs/5a0685e9eb959f84aae8a05dcdd94863dc89e0c4d027b5edd1b04b8d07f525f4.jpg)  
(e) Mobile robots: $6 ^ { \mathrm { t h } }$ agent

![](Grothe2022STRRT_figs/855ae325c5d13e54cb34772580f6182bd0cee8f2a39fad93cc7807fc923fe6c1.jpg)  
(f) Mobile robots: $1 1 ^ { \mathrm { t h } }$ agent: 100s

![](Grothe2022STRRT_figs/07897b5b1a7404f723f95a189c7dc1c9cf4aa27eef85d560af4b5f4376525b92.jpg)  
(g) Robot arms: $6 ^ { \mathrm { t h } }$ arm

![](Grothe2022STRRT_figs/ae9bfe6a8740af0fc9dcc3182c5fdc822b57d47c69cc05697482e995bead26e9.jpg)  
(h) Robot arms: $1 1 ^ { \mathrm { t h } }$ arm  
Fig. 5: Success rates and cost plots for the experiments (Section IV-A) for ST-RRT\*, RRT-Connect, and RRT\* over 100 runs. RRT-Connect and RRT\* were run with 3 different upper bounds, $t _ { \mathrm { u b } }$ for the time (indicated in the figure), since they can not operate in unbounded time-spaces. The thick line is the median, and the shaded area in the cost plot shows the 95% nonparametric confidence interval. Cost for RRT-Connect is shown as the median with error bars for the 95% nonparametric confidence interval. Unsuccessful runs are treated as infinite cost. The upper time limits for RRT\* and RRT-Connect are listed in the figures. Planners that are not shown were not able to find any solution in the given time.

## B. Experimental Results

We analyze the results of both the abstract experiments (Fig. 5a - Fig. 5d), and the simulated robot experiments (Fig. 5e - Fig. 5h). We compare the success rates and the cost-convergence plots of the different algorithms.

1) Initial solution time: In almost all cases the median initial solution time of ST-RRT\* is lower than for both RRT-Connect and RRT\*, even with the tightest time-bound. This can be attributed to the conditional sampling, which helps avoid exploring areas that are clearly not reachable.

2) Success Rate: A low time bound helps to more quickly find solutions for RRT-Connect and RRT\*; however, it can lead to the inability to find solutions at all. This is especially problematic for RRT-Connect which stops sampling goal states at some point, leading to RRT-Connect sometimes not reaching 100% success rate even though the time bound is specified such that a solution would be attainable.

3) Cost: ST-RRT\* converges to the best found solution more quickly than RRT\*. Additionally, while the initial cost of the solution of ST-RRT\* is sometimes higher than RRT-Connect’s solution, the final solution cost of ST-RRT\* is in all cases lower or equal than for the other methods.

Summarizing the results, a special treatment of the timespace is clearly necessary in a planner to achieve good performance in the motion planning process and ST-RRT\* outperforms the other planners on the tested problems.

## V. CONCLUSION

We proposed ST-RRT\*, a planning algorithm that is able to efficiently deal with unbounded time spaces and optimizes for arrival time in an environment with moving obstacle on known trajectories. We guarantee probabilistic completeness and asymptotic optimality by introducing progressive expansion of the goal space and generate new samples accordingly. Our algorithm efficiently deals with many goals and converges to the optimal path quickly by making use of conditional sampling and shrinking the goal spaces.

The current implementation of ST-RRT\* still has two limitations: the batch size and the expansion factor must be chosen in the beginning with a crude estimate of when the goal can be reached. In practice this is not a large limitation since real settings usually impose some upper limit on the acceptable maximum time to reach a goal state. Additionally, acceleration and more complex kinodynamic constraints (e.g. torque limits) are not taken into account. While this does not pose a problem in our applications, it would not be applicable to robots which have to be in quasi-static equilibrium.

We experimentally demonstrated that ST-RRT\* scales well to high dimensions on both abstract and simulated robotic experiments. Our algorithm outperforms state of the art algorithms on both initial solution time and convergence to the optimal solution. An initial version of ST-RRT\* was used in work on large-scale multi-robot coordination [2].

[1] B. Siciliano and O. Khatib, Springer handbook of robotics. Springer, 2016.

[2] V. N. Hartmann, A. Orthey, D. Driess, O. S. Oguz, and M. Toussaint, “Long-horizon multi-robot rearrangement planning for construction assembly,” ArXiv, vol. abs/2106.02489, 2021.

[3] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), vol. 2, 2000, pp. 995–1001.

[4] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” International Journal of Robotics Research, vol. 30, no. 7, pp. 846–894, 2011.

[5] J. D. Gammell and M. P. Strub, “Asymptotically optimal samplingbased motion planning methods,” Annual Review of Control, Robotics, and Autonomous Systems, vol. 4, pp. 295–318, 2021.

[6] M. Elbanhawi and M. Simic, “Sampling-based robot motion planning: A review,” Ieee access, vol. 2, pp. 56–77, 2014.

[7] J. Bruce and M. M. Veloso, “Real-time randomized path planning for robot navigation,” in Robot Soccer World Cup. Springer, 2002, pp. 288–295.

[8] B. D. Luders, S. Karaman, E. Frazzoli, and J. P. How, “Bounds on tracking error using closed-loop rapidly-exploring random trees,” in American Control Conference, 2010, pp. 5406–5412.

[9] Y. Kuwata, J. Teo, S. Karaman, G. Fiore, E. Frazzoli, and J. How, “Motion planning in complex environments using closed-loop prediction,” in AIAA Guidance, Navigation and Control Conference and Exhibit, 2008, p. 7166.

[10] M. Otte and E. Frazzoli, “Rrtx: Asymptotically optimal single-query sampling-based motion planning with quick replanning,” International Journal of Robotics Research, vol. 35, no. 7, pp. 797–822, 2016.

[11] K. Naderi, J. Rajamäki, and P. Hämäläinen, “Rt-rrt\* a real-time path planning algorithm based on rrt,” in ACM SIGGRAPH Conference on Motion in Games, 2015, pp. 113–118.

[12] C. Fulgenzi, A. Spalanzani, C. Laugier, and C. Tay, “Risk based motion planning and navigation in uncertain dynamic environment,” Research Report, Oct. 2010.

[13] L. Jaillet and T. Siméon, “A prm-based motion planner for dynamically changing environments,” in IEEE International Conference on Intelligent Robots and Systems, vol. 2, 2004, pp. 1606–1611.

[14] Y. Yang and O. Brock, “Elastic roadmaps—motion generation for autonomous mobile manipulation,” Autonomous Robots, vol. 28, no. 1, p. 113, 2010.

[15] D. Ferguson, N. Kalra, and A. Stentz, “Replanning with rrts,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2006, pp. 1243–1248.

[16] M. Zucker, J. Kuffner, and M. Branicky, “Multipartite rrts for rapid replanning in dynamic environments,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2007, pp. 1603–1609.

[17] A. Sintov and A. Shapiro, “Time-based rrt algorithm for rendezvous planning of two dynamic systems,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2014, pp. 6745–6750.

[18] M. Phillips and M. Likhachev, “Sipp: Safe interval path planning for dynamic environments,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2011, pp. 5628–5635.

[19] K. Kant and S. W. Zucker, “Toward efficient trajectory planning: The path-velocity decomposition,” International Journal of Robotics Research, vol. 5, no. 3, pp. 72–89, 1986.

[20] Q.-C. Pham, S. Caron, P. Lertkultanon, and Y. Nakamura, “Admissible velocity propagation: Beyond quasi-static path planning for highdimensional robots,” International Journal of Robotics Research, vol. 36, no. 1, pp. 44–67, 2017.

[21] M. Kalakrishnan, S. Chitta, E. Theodorou, P. Pastor, and S. Schaal, “Stomp: Stochastic trajectory optimization for motion planning,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2011, pp. 4569–4574.

[22] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, S. Patil, K. Goldberg, and P. Abbeel, “Motion planning with sequential convex optimization and convex collision checking,” International Journal of Robotics Research, vol. 33, no. 9, pp. 1251–1270, 2014.

[23] D. J. Webb and J. Van Den Berg, “Kinodynamic rrt\*: Asymptotically optimal motion planning for robots with linear dynamics,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2013, pp. 5054–5061.

[24] J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, “Batch informed trees (bit\*): Sampling-based optimal planning via the heuristically guided search of implicit random geometric graphs,” in Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA), 2015, pp. 3067– 3074.

[25] J. D. Gammell, “Informed anytime search for continuous planning problems,” Ph.D. dissertation, University of Toronto, Feb. 2017.

[26] J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, “Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic,” in Proc. of the IEE/RSJ Int. Conf. on Intelligent Robots and Systems (IROS), 2014, pp. 2997–3004.

[27] M. Kleinbort, K. Solovey, Z. Littlefield, K. E. Bekris, and D. Halperin, “Probabilistic completeness of rrt for geometric and kinodynamic planning with forward propagation,” IEEE Robotics and Automation Letters, vol. 4, no. 2, pp. x–xvi, 2018.

[28] L. Janson, E. Schmerling, A. Clark, and M. Pavone, “Fast marching tree: A fast marching sampling-based method for optimal motion planning in many dimensions,” International Journal of Robotics Research, vol. 34, no. 7, pp. 883–921, 2015.

[29] L. Janson, B. Ichter, and M. Pavone, “Deterministic sampling-based motion planning: Optimality, complexity, and performance,” International Journal of Robotics Research, vol. 37, no. 1, pp. 46–61, 2018.

[30] O. Salzman and D. Halperin, “Asymptotically near-optimal RRT for fast, high-quality motion planning,” IEEE Transactions on Robotics, vol. 32, no. 3, pp. 473–483, 2016.

[31] M. Moll, I. A. ¸Sucan, and L. E. Kavraki, “Benchmarking motion planning algorithms: An extensible infrastructure for analysis and visualization,” IEEE Robotics and Automation Magazine, vol. 22, no. 3, pp. 96–102, September 2015.

[32] I. A. ¸Sucan, M. Moll, and L. E. Kavraki, “The Open Motion Planning Library,” IEEE Robotics and Automation Magazine, vol. 19, no. 4, pp. 72–82, December 2012.

[33] A. Orthey, S. Akbar, and M. Toussaint, “Multilevel motion planning: A fiber bundle formulation,” 2020, arXiv:2007.09435 [cs.RO].