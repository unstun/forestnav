---
citation_key: Rustagi2026MultiRobot
arxiv_id: 2603.13748
arxiv_url: "https://arxiv.org/abs/2603.13748"
title: "Multi-Robot Coordination for Planning under Context Uncertainty"
authors_short: "Pulkit Rustagi et al."
year: 2026
direction_tag: G_subgoal_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:05:12Z
origin: ai+web
reviewed: false
---

# Multi-Robot Coordination for Planning under Context Uncertainty

Pulkit Rustagi<sup>1</sup>, Kyle Hollins Wray<sup>2</sup> and Sandhya Saisubramanian<sup>1</sup>

Abstract— Real-world robots often operate in settings where objective priorities depend on the underlying context of operation. When the underlying context is unknown apriori, multiple robots may have to coordinate to gather informative observations to infer the context, since acting based on an incorrect context can lead to misaligned and unsafe behavior. Once the underlying true context is inferred, the robots optimize their task-specific objectives in the preference order induced by the context. We formalize this problem as a Multi-Robot Context-Uncertain Stochastic Shortest Path (MR-CUSSP), which captures context-relevant information at landmark states through joint observations. Our two-stage solution approach is composed of: (1) CIMOP (Coordinated Inference for Multi-Objective Planning) to compute plans that guide robots toward informative landmarks to efficiently infer the true context, and (2) LCBS (Lexicographic Conflict-Based Search) for collisionfree multi-robot path planning with lexicographic objective preferences, induced by the context. We evaluate the algorithms using three simulated domains and demonstrate its practical applicability using five mobile robots in the salp domain setup.

## I. INTRODUCTION

Multi-robot systems in the real world must often perform multi-objective planning for task completion and robot coordination. The preference ordering over objectives is often determined by the underlying context of operation [1], [2], [3], defined based on factors such as resource availability, geographic, or temporal aspects of the environment. For example, salp-inspired underwater robots [4] must prioritize minimizing ecological disturbance in coral zones over energy and speed. In areas of strong eddy currents, they must prioritize stability and energy conservation over speed.

When robots do not have prior knowledge of the exact underlying context, they must actively gather information before task execution, as operating under an incorrect context can lead to inefficient coordination or unsafe behavior [5], [6], [7], [8]. Crucially, in many settings such as salps and disaster rescue [1], informative observations require joint sensing in certain configurations. For example, distinguishing between a coral zone and an eddy current zone requires multiple robots to form a ring around the crevice and perform synchronized measurements of flow and particulates. Individual measurements can only measure local velocity and particulate concentration and are insufficient to infer global circulation patterns. Moreover, robots may need to repeatedly form specific configurations (e.g., ring, chain, star) to obtain context-revealing observations (Fig. 1). This motivates our key question: how to effectively coordinate multiple robots to infer the underlying context to enable computing collisionfree paths that optimize context-dependent objective preferences?

![](Rustagi2026MultiRobot_figs/1c2c2654a9593d13eb50a1c551585c01711f98430b5861a71f1436145462ae4d.jpg)  
Fig. 1: Illustration of multiple GTernal robots [9] with a shared belief over true context. Accurate context-relevant observations are available only when robots are in a required configuration at a landmark (e.g., chain at $\ell _ { 1 }$ and ring at $\ell _ { 2 } )$ . After context inference, robots compute plans aligned with the context-induced objective preferences to reach their goal.

Existing approaches to preference-based planning typically assume that the relevant preference ordering is known a priori, and do not model its dependence on latent context that must be inferred from observations [10]. A common alternative is to compute a Pareto frontier over the objectives when their preference ordering is unknown, as widely used in multi-objective multi-agent path finding (MO-MAPF) works [11], [12], [13]. However, selecting a solution from the Pareto frontier for execution ultimately requires knowledge of the true context. Meanwhile, planning approaches that incorporate active information gathering for planning typically assume that robots can obtain informative observations independently [7], [8]. These methods, therefore, do not support scenarios that require coordination for joint sensing by multiple robots to collect informative observations about the context. Finally, once the context and corresponding objective ordering are known, Pareto-based approaches become computationally inefficient as they fail to exploit the available preference information during planning.

We present Multi-Robot Context-Uncertain Stochastic Shortest Path (MR-CUSSP), a framework designed to model settings where objective preferences depend on a fixed but unknown context that can only be inferred via joint observations. The robots maintain a shared belief over possible contexts, which is updated based on observations. We consider contexts to map to fixed lexicographic preferences over objectives, and assume the existence of belief-collapsing observations at landmark states that uniquely identify the governing preference ordering that must be followed for task completion. These belief-collapsing observations depend on the joint state and actions, enforcing robot coordination for context inference. We focus on navigation tasks in which robots must reach goal locations, while avoiding collisions with other robots and optimizing context-induced lexicographic ordering over objectives.

Our two-stage solution approach (Fig. 1) involves computing: (1) joint plans to visit landmark states such that the underlying context can be quickly inferred; and (2) collisionfree individual paths for task completion using the lexicographic ordering over objectives, induced by the inferred context. For the first stage, we present CIMOP (Coordinated Inference for Multi-Objective Planning) which computes joint plans to visit landmark states in an order that accelerates belief collapse through informative observations. For the second stage, we present Lexicographic Conflict-Based Search (LCBS), an algorithm that builds on conflict-based search (CBS) [14] to compute a collision-free path for each robot, aligned with the context-induced objective ordering. LCBS uses lexicographic $A ^ { * }$ and constraint branching [11] to produce collision-free paths for the robots. Our proposed two-stage structure separates the challenges of information gathering and task execution, enabling each to be solved with algorithms tailored to their structure. By first inferring the context and then planning with a known preference ordering, the approach enables scalable, collision-free robot planning.

Our empirical evaluations using three domains in simulation and five physical robots show that our proposed twostage approach outperforms combinations of state-of-the-art baselines for each stage.

## II. BACKGROUND AND RELATED WORKS

Stochastic Shortest Path (SSP) problem SSPs are a popular framework for modeling goal-oriented tasks that require sequential decision making under stochastic outcomes [15], such as autonomous navigation [16] and warehouse operation [17]. Formally, an SSP is represented by the tuple $\langle S , A , T , C , s _ { 0 } , s _ { g } \rangle$ , with a finite set of states $S ,$ actions $A ,$ transition function $T$ that represents probability of reaching a successor state, a cost function $C ,$ and start and goal states denoted by $s _ { 0 }$ and $s _ { g } ,$ respectively. This work extends SSPs to model settings with multiple robots and lexicographic ordering over objectives induced by a latent context.

Active information gathering Existing works on information gathering reduces uncertainty by planning informative actions [8] or sampling exploration policies [18], but assume that observations can be obtained independently by robots. A recent approach models active sensing for a single robot in partially observable settings using Locally Observable Markov Decision Processes (LOMDPs) [5], [6], These approaches, however, do not model settings where observations depend on coordinated robot configurations, which is precisely the setting we target.

Multi-Objective MAPF Multi-objective multi-agent path finding (MO-MAPF) extends multi-agent path finding (MAPF) to settings with multiple objectives, each associated with a cost function [12], [19]. Robots $\mathbf { R } = \{ 1 , \ldots , d \}$ move in discrete time on a graph $G = ( V , E )$ , with each robot $i \in \mathbf { R }$ following a path $\pi _ { i }$ from start $s _ { i }$ to goal $g _ { i } . \mathrm { ~ A ~ }$ joint plan $\Pi = \left( \pi _ { 1 } , \ldots , \pi _ { d } \right)$ is valid if it avoids vertex and edge conflicts [20]. Each robot incurs a cost vector $\mathbf { c } _ { i } ~ \in ~ \mathbb { R } _ { + } ^ { n }$ yielding total cost $\begin{array} { r } { { \bf C } ( \Pi ) = \sum _ { i \in { \bf R } } { \bf c } _ { i } } \end{array}$

MO-MAPF methods compute Pareto-optimal paths for each robot at the low level and resolving conflicts through a constraint tree at the high level. MO-CBS [12] and BB-MO-CBS [13] explicitly enumerate non-dominated joint plans, while BB-MO-CBS-ε and BB-MO-CBS-k control the size of the frontier through approximation or restriction [13], [11]. Scalarization and evolutionary approaches combine multiple objectives into a single scalar cost or fitness function before applying CBS [21]. While effective for exploring tradeoffs, these methods do not directly enforce a prescribed lexicographic ordering during search. Our approach instead integrates lexicographic comparison at both levels of CBS, ensuring that the returned solution is preference-aligned without frontier construction or scalar reduction.

## III. PROBLEM FORMULATION

Consider a setting with d robots, each with its own assigned task. The robots operate in an environment with a fixed context that is unknown a priori and must be inferred from observations obtained during execution. Since the underlying context induces a preference ordering over multiple objectives, the robots cannot successfully complete their task in a preference-aligned manner until the context is inferred. We consider tasks characterized by specific start and goal locations for each robot. The robots can independently complete their tasks but must coordinate for context inference and to avoid collisions. We formalize this setting as a Multi-Robot Context-Uncertain Stochastic Shortest Path (MR-CUSSP) problem.

Definition 1. A Multi-Robot Context-Uncertain Stochastic Shortest Path (MR-CUSSP) problem for a set of robots $\pmb { R } =$ $\{ 1 , \ldots , d \}$ is defined by $\mathcal { M } = \langle \mathcal { P } , \ X , \ A , \ T , \ C , \ \Theta , \ O \rangle$ with $P = \{ c _ { 1 } , \ldots , c _ { m } \}$ is a finite set of possible contexts, with $c _ { g } \in P$ as the true context initially unknown to the robots; $X = S \times P$ is the state space, where $\boldsymbol { S } = \times _ { k \in A } \boldsymbol { \hat { S } } _ { k }$ is the joint physical state and $P$ is the set of possible contexts; $A = \times _ { k \in A } \hat { A } _ { k }$ is the joint action space;

$T : X \times A \times X \to [ 0 , 1 ]$ is the transition function;

$C : X \times A \to \mathbb { R } ^ { n }$ is the cost for objectives $o = \{ o _ { 1 } , . . . , o _ { n } \}$

$\Theta : { \cal P }  \theta$ maps each context $c _ { i } \in P$ to a lexicographic ordering $\theta _ { i } \in \theta ,$ , where $\theta _ { i } = C _ { i 1 } \succ \dots \succ C _ { i n }$ denotes a strict priority ordering over objectives, and $C _ { i j }$ is the cost associated the $j ^ { t h }$ priority objective under context c ;

$O : A \times X \times \Omega  [ 0 , 1 ]$ is the joint observation function, where $O ( a , x ^ { \prime } , \omega ) = \operatorname* { P r } ( \omega \mid a , x ^ { \prime } )$ and $\Omega = 2 ^ { P } \dot { \backslash } \emptyset$ is the

![](Rustagi2026MultiRobot_figs/2438cb38c4cd3e92e7bfa97bffc9574783def62a21a0fe924ec887e14b26ceb7.jpg)  
Fig. 2: Solution approach overview. A most-likely-outcome determinization is first applied to obtain a discrete graph representation of the stochastic domain, enabling the use of graph-based planning methods. CIMOP prioritizes visiting landmark states that minimize the belief entropy and assigns robots accordingly, based on the current shared belief which is updated based on joint observations at landmark states. Once the context is inferred $( c _ { g } )$ , the induced lexicographic ordering $\Theta ( c _ { g } )$ and a discrete graph representation of the environment, along with a heuristic, are used for task planning. LCBS uses lexicographic $A ^ { * }$ to compute preference-aligned paths, detects conflicts in the joint plan, and iteratively adds constraints using binary branching [13] until a conflict-free solution is obtained.

## set observations

Each state is represented by $x = \langle s , c \rangle$ , with $s \in S$ and $c \in P .$ . The initial and goal states are denoted by $x _ { 0 } ~ =$ $\langle s _ { 0 } , c \rangle$ and $x _ { g } = \langle s _ { g } , c \rangle$ with $s _ { 0 } , s _ { g } \in S$ , respectively. MR-CUSSPs have mixed observable state components as s is fully observable and the partial observability is restricted to the context. Therefore, robots maintain a shared belief b : $X \to \Delta ^ { | X | - 1 }$ which is updated based on joint observations. For clarity, the rest of this paper considers homogeneous robots but MR-CUSSPs also support heterogeneous robots.

Joint observations at landmark states. Every joint action produces an observation $\omega \in \Omega$ . At landmark states, ${ \mathcal { L } } \subseteq S ,$ observations provide accurate information about a subset of potential contexts. For each $s \in { \mathcal { L } } .$ , let Ω denote the set of observations corresponding to context information that can be inferred from that state. Each $\omega \in \Omega _ { i }$ <sub>s</sub> provides information about maximal set of contexts. Similar to locality-based observation models [5], [6], landmark states correspond to informative physical states where observations become available only when the required joint robot configuration and actions are satisfied. For example, salp robots arranged in a ring around a crevice receive accurate flow information, reducing uncertainty over contexts. Thus, $\forall a \in A , x ^ { \prime } = \langle s ^ { \prime } , c ^ { \prime } \rangle$

$$
O (a, x ^ {\prime}, \omega) = \left\{ \begin{array}{l l} 1, & \text { if } s ^ {\prime} \in \mathcal {L} \wedge \omega \in \Omega_ {s ^ {\prime}} \wedge c _ {g} \in \omega , \\ 0, & \text { if } s ^ {\prime} \in \mathcal {L} \wedge \omega \in \Omega_ {s ^ {\prime}} \wedge c _ {g} \notin \omega , \\ \frac {1}{| \Omega |}, & \text { if } s ^ {\prime} \notin \mathcal {L}. \end{array} \right.
$$

Belief update. Belief $b ( x )$ is semantically a belief over contexts since the physical state s in $x = \langle s , c \rangle$ is fully observable. The updated belief for $x ^ { \prime } = \langle { s } ^ { \prime } , { c } ^ { \prime } \rangle$ after receiving an observation ω is calculated as:

$$
\begin{array}{r l} {b ^ {\prime} (x ^ {\prime} | b, a, \omega)} & {= \operatorname * {P r} (c ^ {\prime} | b, a, \omega , s ^ {\prime}) \operatorname * {P r} (s ^ {\prime} | b, a, \omega , s)} \\ & {\quad = \operatorname * {P r} (c ^ {\prime} | b, a, \omega , s ^ {\prime}) T (s, a, s ^ {\prime})} \\ & {\quad = \eta O (a, x ^ {\prime}, \omega) b (c) T (s, a, s ^ {\prime}),} \end{array}\tag{1}
$$

where $\eta = \operatorname* { P r } ( \omega | b , a , s ^ { \prime } ) ^ { - 1 }$ is a normalization constant and $b ( c )$ is the belief over a context c. By definition, the observation function produces a belief-collapsing observation or no information at all. Therefore, the belief is either collapsed $( b ^ { \prime } ( c ) = \{ 0 , 1 \} )$ ) or remains the same $( b ^ { \prime } ( c ) = b ( c ) )$ . Since |S| is finite, belief update following Eqn. 1 results in a finite number of reachable beliefs for MR-CUSSP.

Belief entropy. Efficient task completion requires quick context inference by optimizing the visitation order of landmark states, based on current uncertainty over contexts. To quantify current uncertainty, we define belief entropy as the number of contexts that remain feasible under belief b:

$$
H (b) \triangleq \sum_ {x \in X} \mathbb {1} [ b (x) > 0 ] - 1.\tag{2}
$$

We use $H ( b )$ to denote the entropy associated with a belief b and $H ( b ^ { \prime } | b , \omega _ { \ell } ^ { k } )$ to denote the entropy associated with an updated belief b<sup>′</sup> as a result of joint observation $( \omega _ { \ell } ^ { k } )$ made by k robots at landmark ℓ. By Eqn. 2, $H ( b ) = 0$ only when the belief is non-zero for exactly one context, which indicates the inference of the true context, as belief collapse with incorrect context is impossible under our observation function.

In the following section, we present our two-stage solution approach that first infers the underlying context and then computes collision-free paths for task completion, using the context-induced objective ordering.

## IV. SOLUTION APPROACH

Solving MR-CUSSPs involves four high-level steps (Figure 2): (1) identify informative sequence of landmark states for fast context inference, and assign robot groups to visit them; (2) visit the assigned landmarks and update shared belief based on observations; (3) repeat steps (1)-(2) until belief collapse; and (4) once the true context is inferred, plan for task completion under induced objective preferences. For steps (1) and (2), we present an algorithm, CIMOP (Coordinated Inference for Multi-Objective Planning). CIMOP (Alg.1) determines the order in which landmarks states should be visited, based on the initial belief, and computes coordinated plans to obtain informative observations at landmark states. For step (4), we present Lexicographic Conflict-Based Search (LCBS) that computes a plan for each robot independently, while avoiding collisions with other robots. To enable checking for potential collisions between robots in steps (2) and (4), we use most-likely outcome determinization [22] to construct a deterministic approximation by using the most likely successor for each state-action pair, during planning. This is complemented with replanning when robots reach a state for which they do not have a prescribed action. Determinization enables planning over a discrete graph $G = ( V , E )$ , where vertices correspond to physical states and edges correspond to mostlikely transitions. This enables both CIMOP and LCBS to perform efficient heuristic search while avoiding reasoning over full stochastic branching.

## A. Coordinated Context Inference using CIMOP

Alg. 1 first initializes the available robot set, visited landmark set, and active robot groups (Line 1). If $H ( b _ { 0 } ) > 0 .$ we compute the minimum number of robots required to obtain an informative observation at each landmark, denoted by $N _ { \mathcal { L } } [ \ell ]$ (Lines 4–6). This is computed by searching over possible team sizes to find the smallest k that yields the maximum entropy reduction $H ( b _ { 0 } ) - H ( b ^ { \prime } | \omega _ { \ell } ^ { k } )$

CIMOP iteratively computes a visitation sequence $\mathcal { T }$ over landmark states, based on current belief (Lines 7,8). Specifically, CIMOP uses Alg. 2 to compute I by estimating the reduction in entropy that can be achieved with $N _ { \mathcal { L } } [ \ell ]$ robots at a landmark $\ell , \bar { H ( b ) } - H \big ( b ^ { \prime } \mid b , \ \omega _ { \ell } ^ { N _ { \mathcal { L } } [ \ell ] } \big )$ . The landmarks are then sorted in the decreasing order of entropy reduction and used for robot assignment. Note that $N _ { \mathcal { L } } [ \ell ]$ is determined using b<sub>0</sub> (Line 6, Alg. 1) while I is determined using b (Line 1, Alg. 2). If $| \mathbf { R } _ { a v } | \geq N _ { \mathcal { L } } [ \ell ]$ , the nearest $N _ { \mathcal { L } } [ \ell ]$ robots are assigned to unvisited $\ell \in \mathcal { T }$ (Lines 9-11). The assigned landmark is recorded within the group object and its robots are removed from the available pool (Lines 12-14). The process continues until either available robots are insufficient or all prioritized landmarks are examined. While any planner can be used to compute a joint plan for the group to reach its assigned landmark, our experiments use a standard conflict-based search (CBS) planner with determinization and replanning as needed [14] (Line 15). When a group g reaches its assigned landmark $g . \ell ,$ the robots are returned to the available pool (Line 18), the landmark is marked as visited (Line 19), and the shared belief is updated (Line 20). Since the belief does not change in non-landmark states, following our observation function, it is sufficient to update the shared beliefs when a landmark is visited.

The process of recomputing landmark priorities under the updated belief and reallocating robots is repeated until $H ( b ) = 0$ (Lines 7-20). Once belief collapses, the context is inferred as $c _ { g } = \arg \operatorname* { m a x } _ { c \in P } b .$ , and associated lexicographic ordering is returned for task planning (Lines 21-22).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 CIMOP: Inference plan with belief sync

Require: Robots R, contexts P, landmarks L, init. belief  $b_{0}$ 

Ensure: Joint plan  $\Pi$  (or  $\emptyset$ ), inferred context  $c_{g}$ 

1: Init:  $R_{av} \leftarrow R$ ,  $L_{vis} \leftarrow \{\}$ ,  $Groups \leftarrow []$ ,  $b \leftarrow b_{0}$ 

2: if  $H(b_{0}) = 0$  then

3: return ( $\emptyset$ , arg max $_{c \in P} b_{0}$ )

4:  $N_{L}[l] \leftarrow |R| \forall l \in L$ $\triangleright$  initialize #robots needed at  $\ell$ 

5: for all  $\ell \in L$  do

6:  $N_{L}[l] \leftarrow \min\{k|k = \arg\max_{k \leq |R|} H(b_{0}) - H(b'|b_{0}, \omega_{\ell}^{k})\}$ 

7: while  $H(b) &gt; 0$  do

8:  $I \leftarrow GETLANDMARKVISITSEQUENCE(N_{L}, L, b)$ 

9: for  $\ell \in I \setminus L_{vis}$  do  $\triangleright$  highest to lowest visit priority

10: if  $|R_{av}| \geq N_{L}(l)$  then

11:  $g \leftarrow ASSIGNNEARESTROBOTS(R_{av}, N_{L}[l])$ 

12:  $g.l \leftarrow l$ 

13: Groups.APPEND(g)

14:  $R_{av} \leftarrow R_{av} \backslash g.R$ 

15:  $\Pi.APPEND(PLANTOLANDMARK(R, Groups))$ 

16: for  $g \in Groups$  do

17: if g reached g.l then

18:  $R_{av} \leftarrow R_{av} \cup g$ 

19:  $L_{vis} \leftarrow L_{vis}.APPEND(g.l)$ 

20:  $b \leftarrow UPDATEBELIEF(\Pi)$ $\triangleright$  shared belief

21:  $c_{g} \leftarrow \arg\max_{c \in P} b$ 

22: return  $\Theta(c_{g})$ $\triangleright$  preferences under  $c_{g}$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 GETLANDMARKVISITSEQUENCE
Require: landmark requirements  $N_{L}$ , landmarks L, belief b
Ensure: Visitation sequence I
1:  $\forall\ell\in\mathcal{L}:I_{H}(\ell)\leftarrow H(b)-H(b'\mid b,\omega_{\ell}^{N_{\mathcal{L}}[\ell]})$ 
2:  $I\leftarrow L.SORT(I_{H},order=descending)$ 
3: return I
</div>

## B. Multi-Robot Planning under Inferred Context using LCBS

To plan under the inferred lexicographic preferences $\Theta ( c _ { g } )$ , we present Lexicographic Conflict-Based Search (LCBS), an algorithm that extends the two-level framework of Conflict-Based Search (CBS) [14] to settings with strict priority ordering over multiple objectives. In LCBS, the lowlevel search computes a plan for each robot independently; the high-level search detects conflicts in the joint plan and iteratively generates constraints for the low-level planner. Any heuristic can be used in practice but optimality guarantees depend on the heuristic admissibility. In our experiments, we use Euclidean distance between the current location and the goal as the heuristic.

To compare two cost vectors u and v, we define u $< _ { \mathrm { l e x } }$ v as the lexicographic comparison under Θ. Specifically, u $< _ { \mathrm { l e x } }$ v iff $\exists j \in \{ 1 , \ldots , n \}$ s.t. $ { \mathbf { u } } ^ { j } <  { \mathbf { v } } ^ { j }$ and $\forall k < j , \ \mathbf { u } ^ { k } = \mathbf { v } ^ { k }$ The $< _ { \mathrm { l e x } }$ is used by LCBS to prune dominated cost vectors during planning.

Low-Level Search The low-level planner in LCBS is lexicographic A<sup>∗</sup> (LA<sup>∗</sup>) (Alg. 3), which computes individual robot paths under the ordering induced by Θ. LA<sup>∗</sup> searches over time-augmented states $z = ( v , t )$ with cumulative vector cost ${ \bf g } ( v , t )$ and admissible heuristic h(v). The evaluation key is ${ \bf f } ( \boldsymbol { v } , t ) = { \bf g } ( \boldsymbol { v } , t ) + { \bf h } ( \boldsymbol { v } )$ . The open list O is queried by POPMIN to extract the lexicographically smallest f under $< _ { \mathrm { l e x } }$ (Line 6), so states with lexicographically smaller f are expanded first.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 LA* (Lexicographic A*)
Input: G = (V, E), start-goal (s, g), edge cost  $c_{e} : E \to R_{+}^{d}$ , heuristic h : V →  $R_{+}^{d}$ , constraints  $\Gamma$ 
Output: Optimal path  $\pi$  from s to g (or  $\emptyset$ )
1: Init: timed states  $z = (v, t)$  with  $v \in V$ ,  $t \in N$ ;
2:  $z_{0} \leftarrow (s, 0)$ ;  $\mathbf{g}(z_{0}) \leftarrow \mathbf{0}$ ;  $\mathbf{f}(z_{0}) \leftarrow \mathbf{h}(s)$ ;
3: open list  $O \leftarrow \{\}$ ; cost map  $C \leftarrow \{\}$ ; plan  $\pi \leftarrow \{\}$ ;
4:  $O.PUSH(z_{0})$ ;  $C[z_{0}] \leftarrow 0$ ;
5: while  $O \neq \emptyset$  do
6:    $z = (v, t) \leftarrow O.POPMIN()$ $\triangleright$  lex-min f
7:    if v = g and not VIOLATES(z,  $\Gamma$ ) then
8:    $\pi \leftarrow RECONSTRUCTPATH(z)$ 
9:    break
10:    for each  $u \in SUCCESSORS(v)$  do
11:    $y \leftarrow (u, t+1)$ 
12:    if VIOLATES(z → y,  $\Gamma$ ) then
13:    continue
14:    $g'(y) \leftarrow g(z) + c_{e}(v, u)$ ;  $f'(y) \leftarrow g'(y) + h(u)$ 
15:    if  $y \notin C$  or  $g'(y) &lt;_{lex} C[y]$  then
16:    $C[y] \leftarrow g'(y)$ ; PARENT(y) ← z; f(y) ← f'(y)
17:    $O.PUSH(y)$ 
18: return  $\pi$
</div>

Alg. 3 initializes O with (s, 0) and maintains a closed map $\mathcal { C }$ storing the best g per state (Lines 4). If the popped state reaches the goal and satisfies constraints Γ, the path is returned (Lines 6-9, 18). Otherwise, successor states from outgoing edges are generated, and transitions violating Γ are skipped (Lines 10-13). A successor is inserted only if its g improves under $< _ { \mathrm { l e x } }$ (Line 14-17), ensuring that each state maintains a single best cost vector following Θ.

Optimizing a lexicographic ordering using $\mathrm { L A ^ { * } }$ is more than just a tie-breaking. As node selection (Line 6) and state updates (Line 15) are governed by $< _ { \mathrm { l e x } }$ , lexicographicallyworse path candidates for a state are discarded immediately. The search, thus, directly and efficiently optimizes the strict priority ordering specified by Θ.

High-Level Search For the high-level search (Alg. 4), we adopt the constraint-tree (CT) framework from BB-MO-CBS-pex [11]. Each CT node denotes a joint plan N .Π, joint cost vector N .C, and constraint set N .Γ. The lexicographic comparator $< _ { \mathrm { l e x } }$ is first defined according to Θ, along side initialization of root node $\mathcal { N } _ { 0 }$ , high-level open list $\mathcal { O } _ { \mathrm { H L } } .$ constraint set $\Gamma _ { 0 }$ and robot policies $\pi _ { i } \forall i \in \mathbf { R }$ (Line 1, 2). The high-level open list ${ \mathcal { O } } _ { \mathrm { H L } }$ is ordered lexicographically by N .C (Line 9). The root node is constructed by invoking $\mathrm { L A ^ { * } }$ for each robot under empty constraints (Lines 3–6), and the joint cost is computed, $\begin{array} { r } { \mathcal { N } _ { 0 } . { \bf C } = \sum _ { i \in { \bf R } } { \bf c } _ { e } ( \pi _ { i } ) } \end{array}$ (Line 7). At each iteration, the node with lexicographically smallest joint cost is popped (Line 9). If no conflict is detected, the joint plan is returned (Lines 10–12). Otherwise, the earliest conflict is identified and the node is split into two child nodes, each imposing a constraint on one of the conflicting robots (Lines 13–16). The affected robot is replanned using $\mathrm { L A ^ { * } }$ under the updated constraint set (Line 17). Feasible children update their joint plan and cost (Lines 18–19) and are pushed into $\mathcal { O } _ { \mathrm { H L } }$ (Line 20).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4 LCBS (High-Level Search)

Input:  $G = (V, E)$ , robots  $R = \{1, \ldots, d\}$ , start-goal pairs  $(s^{i}, g^{i}) \forall i \in \mathbf{R}$ , edge cost  $c_{e}$ , heuristic h, lexicographic preferences  $\Theta$ 

Output: Conflict-free joint plan  $\Pi = (\pi_{1}, \ldots, \pi_{d})$  (or  $\emptyset$ )

1: Init:  $&lt;_{lex} \leftarrow \Theta; N_{0} \leftarrow \emptyset; O_{HL} \leftarrow \{\}$ ;

2: Init:  $\Gamma_{0} \leftarrow \{\}; \pi_{i} \leftarrow \emptyset \forall i \in \mathbf{R}$ ;

3: for each robot  $i \in R$  do

4:  $\pi_{i} \leftarrow LA*(G, s^{i}, g^{i}, c_{e}, h, \Gamma_{0})$ 

5: if  $\pi_{i} = \emptyset$  then

6: return  $\emptyset$ 

7:  $N_{0}.Π \leftarrow [\pi_{i}]_{i \in R}; N_{0}.C \leftarrow \sum_{i} c_{e}(\pi_{i}); O_{HL}.PUSH(N_{0})$ ;

8: while  $O_{HL} \neq \emptyset$  do

9:  $N \leftarrow O_{HL}.POPMIN() \quad \triangleright lex-min C(N.\Pi)$ 

10: conflict  $\leftarrow DETECTFIRSTCONFLICT(N.\Pi)$ 

11: if conflict =  $\emptyset$  then

12: return  $\Pi \leftarrow N.\Pi \quad \triangleright return conflict-free plan$ 

13: (type, loc, time,  $id_{i}, id_{j}$ )  $\leftarrow conflict$ 

14:  $\{\gamma^{i}, \gamma^{j}\} \leftarrow GENERATECONSTRAINTS(conflict)$ 

15: for each  $a \in \{i, j\}$  do

16: Create child  $N_{a}; N_{a}.Γ \leftarrow N.\Gamma \cup \{\gamma^{a}\}$ 

17:  $\pi_{a}' \leftarrow LA*(G, s^{a}, g^{a}, c_{e}, h, N_{a}.Γ)$ 

18: if  $\pi_{a}' \neq \emptyset$  then

19:  $N_{a}.Π[a] \leftarrow \pi_{a}'; N_{a}.C \leftarrow \sum_{i} c_{e}(\pi_{i})$ 

20:  $O_{HL}.PUSH(N_{a})$ 

21: return  $\Pi$
</div>

The first conflict-free CT node popped is lexicographically optimal as both high-level and low-level search order nodes under $< _ { \mathrm { l e x } }$ and $\mathrm { L A ^ { * } }$ returns lexicographically optimal paths under constraints.

## V. EXPERIMENTS

We evaluate our solution approach in simulation using three domains and on hardware using five mobile robots.

Baselines: We compare the performance of our two-stage approach with combinations of state-of-the-art for each stage. Specifically, for the first stage, we compare CIMOP with (1) ARVI [8] and (2) SAIA [18]. As both these approaches assume robots can gather information independently, we modify them to work with our observation function, for fair comparison. For the second stage, we compare LCBS against (1) BB-MO-CBS-k (k = 1) [11] that returns a single nondominated solution, serving as a fast Pareto baseline, (2) Scalarized CBS that uses scalarization in low level search using CBS [14] to combine multiple objectives into a single weighted value, and (3) MO-CBS [12] that maintains Pareto frontiers at the robot level and combines them through CBS-style conflict resolution, providing a principled Paretooptimal multi-objective baseline without explicitly searching the full joint state space. For Scalarized CBS, scalarization weights follow geometric scaling: $C _ { 1 } M ^ { n - 1 } + C _ { 2 } M ^ { n - 2 } +$ $\cdots + C _ { n } ,$ where M must be sufficiently large to preserve $C _ { 1 } \ \succ \ \cdots \ \succ \ C _ { n }$ . In practice, objective cost magnitudes are not known a priori, making weight selection non-trivial. Following [21], we sample 50 random trajectories from start to goal to estimate the scale of each objective, and choose M to exceed the largest observed lower-priority cost for a single instance in each domain. The same M value is used for all other instances of that domain.

![](Rustagi2026MultiRobot_figs/3dd61ec48b3f5a37028244f8f060a18892c29b39405dc79a33859725df1afc77.jpg)  
Fig. 3: Summary of experimental results across three domains. The first column shows the domain maps. The second and third columns show entropy-of-belief trends for 5 and 35 robots, respectively. The fourth column shows path cost with increasing percentage of redundant landmarks for analysis in cluttered environments. The fifth column shows plan computation time with increasing numbers of robots. All results are averaged over five instances with randomized robot starting locations.

All algorithms were implemented in C++ and tested on a macOS machine with 18 GB RAM. Robot evaluation is performed with five robots in the Robotarium testbed [9].

Metrics. We compare the algorithms using stage-specific metrics in simulation and the overall performance of the twostage approach using mobile robots. The stage-specific metrics are: (i) Entropy of belief over contexts during execution (Eqn. 2); (ii) Cumulative entropy of the belief sequence to measure the duration of uncertainty until belief collapse (as opposed to uncertainty associated with a particular belief as in (i)); (iii) Scalability with increasing number of robots; and (iv) Performance with varying planning time budget.

## A. Evaluation in simulation

In the following domains, robots begin with a uniform initial belief over a finite set of contexts and coordinate to obtain informative observations at landmark states.

$^ { a ) }$ Sample Collection with Salps: In this domain, salpinspired [23] underwater robots are tasked with collecting samples in environments with crevices and boulder ridges that act as informative landmarks. Robots begin with a uniform belief over three contexts: $c _ { 1 }$ (strong-current region), $c _ { 2 }$ (coral-sensitive region), and $c _ { 3 }$ (nominal condition). In all contexts, robots should minimize energy consumption $( o _ { e } ) .$ minimize coral damage $( o _ { c } )$ , and minimize time to goal $( o _ { t } ) .$ but their priority depends on the context. The context to objective ordering is $c _ { 1 } : o _ { e } \succ o _ { c } \succ o _ { t } ; c _ { 2 } : o _ { c } \succ o _ { e } \succ o _ { t } ;$ and c<sub>3</sub> $: o _ { t } \succ o _ { e } \succ o _ { c }$ . Coordinated sampling at landmarks reveals flow and surface characteristics that distinguish among these contexts. Across instances, we vary the number and spatial distribution of informative landmarks and robots.

b) Heavy-Lift Warehouse: Autonomous warehouse robots transport shelves through shared aisles to fulfillment stations, with designated monitoring stations serving as informative landmarks. Robots begin with a uniform belief over three contexts: $c _ { 1 }$ (backlogged), $c _ { 2 }$ (congested), and $c _ { 3 }$ (humantraffic). In all contexts, robots balance completion time $\left( o _ { t } \right)$ minimizing congestion in primary aisles, $( o _ { c } )$ and avoiding human zones $\left( o _ { h } \right)$ , but the priority depends on context. The context to objective ordering is as follows: $c _ { 1 } : o _ { t } \succ o _ { c } \succ o _ { h } ;$ $c _ { 2 } : o _ { c } \succ o _ { t } \succ o _ { h } ;$ and $c _ { 3 } : o _ { h } \succ o _ { c } \succ o _ { t }$ . At monitoring stations, two robots must arrive simultaneously at paired checkpoints to obtain a joint observation of aisle-level traffic and human presence, which cannot be determined from a single robot’s local view. Across instances, we vary the number of robots, shelf locations, and the placement of primary aisles and monitoring stations.

c) Forest Firefighting: Aerial robots are assigned to reach designated fire-control locations in an evolving wildfire. Since large-scale wind and smoke conditions cannot be determined from local sensing alone, robots coordinate at designated vantage points that serve as informative landmarks before planning traversal. Robots begin with a uniform belief over three contexts: $c _ { 1 }$ (high-wind), $c _ { 2 }$ (dense-smoke), and $c _ { 3 }$ (rapid-spread). In all contexts, robots should minimize completion time $( o _ { t } ) .$ minimize energy consumption $( o _ { e } ) .$ and minimize path length $( o _ { l } )$ , but the priority depends on the context. The context to objective ordering is $c _ { 1 } : o _ { e } \ \succ$ $o _ { l } ~ \succ ~ o _ { t } ; ~ c _ { 2 } ~ : ~ o _ { l } ~ \succ ~ o _ { e } ~ \succ ~ o _ { t } ;$ and $c _ { 3 } : o _ { t } \ \succ \ o _ { e } \ \succ o _ { l }$ Coordinated observations at vantage points reveal wind and smoke conditions that distinguish among these contexts. Across instances, we vary the number of robots, vantage point placement, and the locations of wind and fire spots.

## VI. RESULTS AND DISCUSSION

a) Belief entropy reduction: Fig. 3 (columns (i)–(ii)) reports belief entropy during execution, computed using Eqn. 2, where lower values indicate faster context inference. Across all settings, CIMOP consistently infers the context faster than both baselines. For five robots, CIMOP reaches zero entropy within 20 steps in the salp and warehouse domains, compared to 60–80 steps for the baselines, and collapses substantially faster in the forest firefighting domain where baselines require several hundred steps. While we observe an improved performance with 35 robots, across methods, CIMOP remains consistently faster in context inference.

b) Cumulative entropy with increasing redundant landmarks: To quantify how long it takes to infer the true context and whether useful landmarks are prioritized correctly over time, we measure the cumulative entropy of a belief sequence induced by the policy. This complements the entropy of a single belief point (Eqn. 2) and evaluates the sequential nature of uncertainty reduction. We measure this by varying the percentage of landmark states whose associated observations are redundant with respect to observations available at other landmark states and therefore visiting them does not reduce belief entropy. Figure 3 (column (iii)) shows cumulative entropy, averaged over five instances in each domain, with increasing percentage of redundant landmarks. Lower cumulative entropy indicates faster inference of the true context. CIMOP maintains consistently low cumulative entropy across all domains and clearly outperforms baselines, with low variance despite sparse informative observations.

c) Planning time: Figure 3 (column (iv)) evaluates scalability through wall-clock planning time for context inference. CIMOP scales substantially better than both baselines in all domains. For 35 robots, CIMOP consistently plans in under two minutes, while ARVI exceeds 40 minutes and SAIA exceeds 80 minutes. This consistent gap demonstrates CIMOP’s ability to scale to larger robot teams while maintaining practical planning times.

![](Rustagi2026MultiRobot_figs/9aa61273a19ca658ddcff4b28976bccc6524cd97a86a084cdfcca2b625ef0607.jpg)

Fig. 4: Success rate on 15 instances (five from each of the three domains) under constrained planning time limit with five robots and three objectives.  
![](Rustagi2026MultiRobot_figs/c58cc98e96c3a79cef29a40303fcdd20881175421100d8a308fc54428b9f289f.jpg)  
Fig. 5: Execution sequence with five GTernal robots [9]: (1) start with uniform belief over three contexts, (2) form a chain to observe the cave landmark and update belief, (3) four robots form a ring to observe the crevice landmark and collapse belief, after which (4) the robots independently plan prioritizing minimizing coral damage over energy consumption and time to goal as imposed by the inferred context $c _ { 2 } .$

d) Performance in time-constrained settings: The efficiency of planning in time-constrained settings is measured in terms of success rate [11], [12]: the fraction of problem instances where the algorithm was able to generate an optimal solution for the lexicographic ordering over objectives, which can be verified by comparing the results with a Pareto-frontier approach (such as MO-CBS). Fig. 4 reports the success rate on 15 environment instances (five from each of the three domains) as the planning-time budget decreases from 120 to 5 seconds for five robots and three objectives. LCBS maintains 100% success across all budgets and remains consistent even at five seconds, while BB-MO-CBS (k = 1), MO-CBS, and Scalarized CBS drop significantly as the time limit decreases. The consistent performance of LCBS under tight budgets highlights that eliminating lexicographically dominated nodes during search allows it to compute preferencealigned solutions reliably in time-sensitive settings.

e) Hardware experiments: We validate the practical feasibility of our approach using five mobile robots in the salp domain. Fig. 5 shows shared belief evolution, where robots adapt formations based on observation requirements at landmarks, and collapse the belief in real time before executing preference-aligned plans. Fig. 6 reports total planning time (stage 1 + stage 2), where CIMOP + LCBS completes both stages in under 6 seconds, while other combinations require 40–120 seconds. Combinations using LCBS maintain low second-stage times, and CIMOP substantially reduces context inference time, thus demonstrating the run time benefits of both CIMOP and LCBS which enable real-time execution on physical robots.

![](Rustagi2026MultiRobot_figs/727c0dfc98a96d96878e84b374760770c1004543ff3404d423f5ac75f30d4a28.jpg)

<table><tr><td>Label</td><td>Approach</td></tr><tr><td>Ours</td><td>CIMOP + LCBS</td></tr><tr><td>B1</td><td>CIMOP + Scalarized CBS</td></tr><tr><td>B2</td><td>CIMOP + BB-MO-CBS-k (k=1)</td></tr><tr><td>B3</td><td>CIMOP + MO-CBS</td></tr><tr><td>B4</td><td>ARVI + LCBS</td></tr><tr><td>B5</td><td>ARVI + Scalarized CBS</td></tr><tr><td>B6</td><td>ARVI + BB-MO-CBS-k (k=1)</td></tr><tr><td>B7</td><td>ARVI + MO-CBS</td></tr><tr><td>B8</td><td>SAIA + LCBS</td></tr><tr><td>B9</td><td>SAIA + Scalarized CBS</td></tr><tr><td>B10</td><td>SAIA + BB-MO-CBS-k (k=1)</td></tr><tr><td>B11</td><td>SAIA + MO-CBS</td></tr></table>

Fig. 6: Total time taken to plan by each approach in our hardware experiment with five mobile robots and three possible contexts, each with different preference ordering over three objectives.

## VII. SUMMARY AND FUTURE WORK

This paper formalizes multi-robot planning under a fixed but initially unknown context as an MR-CUSSP. We present two algorithms that enable robot coordination to obtain informative joint observations to infer the operative context, and then compute collision-free plans aligned with the induced lexicographic preference ordering over objectives. Experimental results across three simulated domains and hardware deployments demonstrate faster belief collapse, lower cumulative entropy, and improved scalability in planning time with increasing robots and objectives compared to state-of-the-art baselines for each stage in our solution approach. Future work will relax the assumption of predefined landmark structures and extend this to learning settings.

## ACKNOWLEDGEMENTS

Rustagi and Saisubramanian were supported in part by ONR award N00014-23-1-2171.

## REFERENCES

[1] M. Al-Husseini, K. H. Wray, and M. J. Kochenderfer, “Hierarchical framework for optimizing wildfire surveillance and suppression using human-autonomous teaming,” Journal of Aerospace Information Systems (AIAA), pp. 1–22, 2024.

[2] H. Jiang, Y. Wang, R. Veerapaneni, T. H. Duhan, G. A. Sartoretti, and J. Li, “Deploying ten thousand robots: Scalable imitation learning for lifelong multi-agent path finding,” in ICRA, 2025.

[3] P. Rustagi, Y. Anand, and S. Saisubramanian, “Multi-objective planning with contextual lexicographic reward preferences,” in Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2025.

[4] Z. Yang, Y. Zhang, M. Herbert, M. A. Hsieh, and C. Sung, “Effect of jet coordination on underwater propulsion with the multi-robot salp system,” in IEEE 8th International Conference on Soft Robotics, 2025.

[5] M. Merlin, S. Parr, N. Parikh, S. Orozco, V. Gupta, E. Rosen, and G. Konidaris, “Robot task planning under local observability,” in ICRA, 2024.

[6] M. Merlin, Z. Yang, G. Konidaris, and D. Paulius, “Least commitment planning for the object scouting problem,” in IROS, 2025.

[7] N. Atanasov, J. Le Ny, K. Daniilidis, and G. J. Pappas, “Decentralized active information acquisition: Theory and application to multi-robot slam,” in ICRA, 2015.

[8] B. Schlotfeldt, D. Thakur, N. Atanasov, V. Kumar, and G. J. Pappas, “Anytime planning for decentralized multirobot active information gathering,” Robotics and Automation Letters (RA-L), vol. 3, no. 2, pp. 1025–1032, 2018.

[9] S. Wilson, P. Glotfelter, L. Wang, S. Mayya, G. Notomista, M. Mote, and M. Egerstedt, “The robotarium: Globally impactful opportunities, challenges, and lessons learned in remote-access, distributed control of multirobot systems,” Control Systems Magazine, vol. 40, no. 1, pp. 26–44, 2020.

[10] P. Sharma, B. Sundaralingam, V. Blukis, C. Paxton, T. Hermans, A. Torralba, J. Andreas, and D. Fox, “Correcting robot plans with natural language feedback,” in RSS, 2022.

[11] F. Wang, H. Zhang, S. Koenig, and J. Li, “Efficient approximate search for multi-objective multi-agent path finding,” in Proceedings of the 34th International Conference on Automated Planning and Scheduling (ICAPS), 2024.

[12] Z. Ren, S. Rathinam, and H. Choset, “Multi-objective conflict-based search for multi-agent path finding,” in International Conference on Robotics and Automation (ICRA), 2021.

[13] Z. Ren, J. Li, H. Zhang, S. Koenig, S. Rathinam, and H. Choset, “Binary branching multi-objective conflict-based search for multi-agent path finding,” in Proceedings of the 33rd International Conference on Automated Planning and Scheduling (ICAPS), 2023.

[14] G. Sharon, R. Stern, A. Felner, and N. Sturtevant, “Conflict-based search for optimal multi-agent path finding,” in AAAI, 2012.

[15] S. Saisubramanian, K. H. Wray, L. Pineda, and S. Zilberstein, “Planning in stochastic environments with goal uncertainty,” in IROS, 2019.

[16] E. Stracca, G. Grioli, L. Pallottino, and P. Salaris, “Risk-aware routing for a robot in a shared dynamic environment,” IEEE Transactions on Robotics (TRO), 2026.

[17] C. Street, O. Grubb, and M. Mansouri, “Planning under uncertainty from behaviour trees,” in IROS, 2025.

[18] Y. Kantaros, B. Schlotfeldt, N. Atanasov, and G. J. Pappas, “Samplingbased planning for non-myopic multi-robot information gathering,” Autonomous Robots, vol. 45, no. 7, pp. 1029–1046, 2021.

[19] Z. Ren, G. Wagner, and T. K. S. Kumar, “A conflict-based search framework for multi-objective multi-agent path finding,” IEEE Transactions on Automation Science and Engineering, 2022.

[20] R. Stern, N. Sturtevant, A. Felner, S. Koenig, H. Ma, T. Walker, J. Li, D. Atzmon, L. Cohen, T. K. S. Kumar, E. Boyarski, and R. Bartak, “Multi-agent pathfinding: Definitions, variants, and benchmarks,” in Proceedings of the 12th International Symposium on Combinatorial Search (SoCS), 2019.

[21] F. Ho and S. Nakadai, “Preference-based multi-objective multi-agent path finding,” in Proceedings of the 22nd International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2023.

[22] S. Saisubramanian and S. Zilbertsein, “Adaptive outcome selection for planning with reduced models,” in IROS, 2019.

[23] K. R. Sutherland and L. P. Madin, “Comparative jet wake structure and swimming performance of salps,” Journal of Experimental Biology, vol. 213, no. 17, pp. 2967–2975, 2010.