---
citation_key: Bhat2026Optimal
arxiv_id: 2603.21880
arxiv_url: "https://arxiv.org/abs/2603.21880"
title: "Optimal Solutions for the Moving Target Vehicle Routing Problem with Obstacles via Lazy Branch and Price"
authors_short: "Anoop Bhat et al."
year: 2026
direction_tag: I_corridor_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:06:03Z
origin: ai+web
reviewed: false
---

# Optimal Solutions for the Moving Target Vehicle Routing Problem with Obstacles via Lazy Branch and Price

Anoop Bhat<sup>1</sup> and Geordan Gutow<sup>2</sup> and Surya Singh<sup>3</sup> and Zhongqiang Ren<sup>4</sup> and Sivakumar Rathinam<sup>5</sup> and Howie Choset<sup>1</sup>

Abstract— The Moving Target Vehicle Routing Problem with Obstacles (MT-VRP-O) seeks trajectories for several agents that collectively intercept a set of moving targets. Each target has one or more time windows where it must be visited, and the agents must avoid static obstacles and satisfy speed and capacity constraints. We introduce Lazy Branch-and-Price with Relaxed Continuity (Lazy BPRC), which finds optimal solutions for the MT-VRP-O. Lazy BPRC applies the branch-and-price framework for VRPs, which alternates between a restricted master problem (RMP) and a pricing problem. The RMP aims to select a sequence of target-time window pairings (called a tour) for each agent to follow, from a limited subset of tours. The pricing problem adds tours to the limited subset. Conventionally, solving the RMP requires computing the cost for an agent to follow each tour in the limited subset. Computing these costs in the MT-VRP-O is computationally intensive, since it requires collision-free motion planning between moving targets. Lazy BPRC defers cost computations by solving the RMP using lower bounds on the costs of each tour, computed via motion planning with relaxed continuity constraints. We lazily evaluate the true costs of tours as-needed. We compute a tour’s cost by searching for a shortest path on a Graph of Convex Sets (GCS), and we accelerate this search using our continuity relaxation method. We demonstrate that Lazy BPRC runs up to an order of magnitude faster than two ablations.

## I. INTRODUCTION

Finding trajectories for multiple agents to visit multiple moving targets is necessary in applications such as defense [1], [2], [3], orbital refueling [4], and recharging mobile robots collecting data from the seafloor [5]. These applications can be modeled as variations of the Vehicle Routing Problem (VRP) [6], [7]. The VRP assumes a set of stationary targets and a set of agents, where the agents start at a common location called the depot. Each target has a demand of goods, and each agent has a capacity on the amount of goods it can deliver. Given the travel cost between every pair of targets, and between the targets and the depot, the VRP seeks a sequence of targets for each agent with minimal sum of costs, such that the sum of demands of targets visited by an agent does not exceed the capacity. In the Moving Target VRP (MT-VRP) [8], the targets are moving, and we seek not only a sequence of targets for each agent, but a trajectory. Each target must be met in a particular time window(s), and the agents have a speed limit. Prior work on the MT-VRP assumes piecewise-linear target trajectories [8], and we make the same assumption. When the agents must avoid static obstacles, we have the MT-VRP with Obstacles (MT-VRP-O), shown in Fig. 1.

![](Bhat2026Optimal_figs/962954eca19b3db4277c691e835256009a45a5bc97e059e7cd812caa1fe1eaa7.jpg)  
Fig. 1. Targets move through obstacle environment and must be intercepted within time windows, shown in bold-colored lines. Agents begin and end at depot, intercepting targets while avoiding obstacles.

The MT-VRP-O generalizes the Traveling Salesman Problem (TSP), and thus finding an optimal solution is NP-hard [9], [1]. No prior methods find an optimal solution for the MT-VRP-O. The closest related work finds optimal solutions for the MT-VRP without obstacles [8], using the branchand-price framework [10]. In this work, we develop a new branch-and-price algorithm for the MT-VRP-O called Lazy Branch-and-Price with Relaxed Continuity (Lazy BPRC).

We define the pairing of a target with one of its time windows as a target-window. We define a tour as a sequence of target-windows, meant to be followed by a single agent. The cost of a tour is the distance traveled by a collisionfree trajectory intercepting the tour’s targets in order. The MT-VRP-O seeks a least-cost set of tours for the agents to follow, from the set of all possible tours. Since explicitly enumerating all possible tours is intractable, we employ column generation [11], where we initially generate a limited subset F of all possible tours, then alternate between selecting a set of tours from F and adding tours to F .

Traditionally, the selection step within column generation (known as the restricted master problem) aims to minimize the sum of selected tours’ costs. In the MT-VRP-O, however, computing tour costs is expensive, since it requires collisionfree motion planning. Our key idea is to instead perform column generation using cheap-to-compute lower bounds on tour costs. We compute these lower bounds by solving a motion planning problem with relaxed continuity constraints. Thus, we incorporate an outer alternation between (i) column generation using lower bounds on tour costs, and (ii) lazily evaluating only the costs of tours selected by column generation. We evaluate the cost of a tour by searching for a shortest path in a Graph of Convex Sets (GCS) [12]; we use our continuity relaxation strategy to provide a heuristic for the search. If column generation selects a set of tours whose costs have all been evaluated, we terminate the alternation between (i) and (ii). Our numerical results show that Lazy BPRC runs up to 46 times faster than a non-lazy ablation, and up to 26 times faster than an ablation using an existing obstacle-unaware heuristic [13].

## II. RELATED WORK

While the MT-VRP-O has not been studied in prior work, several related problems have been studied. [5] studies a multi-agent Moving Target TSP with Obstacles (multi-agent MT-TSP-O), which lacks the capacity constraints from the MT-VRP-O. However, their approach only allows interception at sampled points along the targets’ trajectories, and thus [5] does not provide optimal solutions. On the other hand, for the single-agent MT-TSP-O, [13] presents a solver that finds optimal solutions. [13] alternates between a high-level search to generate a tour, and a low-level search to find a trajectory intercepting the tour’s targets to determine its cost. The low-level search in [13] solves a Shortest Path Problem on a GCS (SPP-GCS). We similarly solve an SPP-GCS to evaluate a tour’s cost, and we provide a novel heuristic for the search that we show outperforms the heuristic from [13].

[8] studies the MT-VRP without obstacles using an approach called Branch-and-Price with Relaxed Continuity (BPRC). Our approach, Lazy BPRC, extends BPRC to handle obstacles, using a new obstacle-aware continuity relaxation strategy, as well as lazy tour cost evaluation. We show in Section VII that our lazy evaluation outperforms BPRC’s non-lazy tour cost evaluation.

## III. PROBLEM SETUP

We consider $n _ { \mathrm { t a r } }$ targets moving in $\mathbb { R } ^ { 2 }$ , and $\{ 1 , 2 , \dots , n _ { \mathrm { t a r } } \}$ is the set of targets. Each target i has a demand $d _ { i }$ . Target i has $n _ { \mathrm { w i n } } ( i )$ time windows, and $[ \underline { { t } } _ { i , j } , \bar { t } _ { i , j } ]$ is the jth time window of target i. The trajectory of target i is $\tau _ { i } : \mathbb { R } \to \mathbb { R } ^ { 2 }$ and we assume $\tau _ { i }$ has constant velocity within each time window, but possibly different velocities in different time windows. Without loss of generality, we assume targets do not pass through obstacles during their time windows.<sup>1</sup>

Let the number of agents be $n _ { \mathrm { a g t } }$ . Each agent has a capacity $d _ { \mathrm { m a x } }$ on the amount of demand it can serve. When visiting a target, an agent must serve the target’s full demand. Each agent has a speed limit $v _ { \mathrm { m a x } }$ , and no target moves faster than $v _ { \mathrm { m a x } }$ within its time windows. We denote an agent’s trajectory as $\tau _ { \mathrm { a } }$ . An agent trajectory $\tau _ { \mathrm { a } }$ intercepts target i if $\mathrm { ( i ) } \ \tau _ { \mathrm { a } } ( t ) = \tau _ { i } ( t )$ for some t within some time window of target i, and (ii) $\tau _ { \mathrm { a } }$ claims target i at time t. The notion of claiming is needed when we plan a trajectory $\tau _ { \mathrm { a } }$ to intercept some target i, then $i ^ { \prime } ,$ , but $\tau _ { \mathrm { a } }$ matches space-time locations with some target $i ^ { \prime \prime }$ unintentionally. As long as $\tau _ { \mathrm { a } }$ does not claim $i ^ { \prime \prime }$ , the agent’s capacity is not depleted when it meets $i ^ { \prime \prime } .$ All agents start at a depot $p _ { \mathrm { d } } \in \mathbb { R } ^ { 2 }$ . Finally, the agents must avoid collisions with stationary obstacles. We refer to a collision-free agent trajectory satisfying the speed limit as a feasible agent trajectory.

The MT-VRP-O seeks a feasible trajectory for each agent such that every target is intercepted by some agent’s trajectory, and for each agent, the sum of demands of targets it intercepts does not exceed its capacity. In this work, we aim to minimize the sum of the agents’ distances traveled.

## IV. INTEGER LINEAR PROGRAM (ILP) FOR MT-VRP-O

Lazy BPRC considers a target-window graph $\begin{array} { r l } { \mathcal { G } _ { \mathrm { t w } } } & { { } = } \end{array}$ $( \nu _ { \mathrm { t w } } , \mathcal { E } _ { \mathrm { t w } } )$ . Each node in $\nu _ { \mathrm { t w } }$ is a pairing of a target i with one of its time windows, called a target-window. For example, $\gamma _ { i , j } = ( i , [ \underline { { t } } _ { i , j } , \overline { { t } } _ { i , j } ] )$ denotes the jth target-window of target i. $\nu _ { \mathrm { t w } }$ contains all possible target-windows, as well as a fictitious target-window $\gamma _ { 0 , 1 } = \gamma _ { 0 } = ( 0 , [ 0 , \infty ) )$ , referring to a fictitious stationary target 0 at the depot, with time window $[ 0 , \infty )$ . An agent trajectory $\tau _ { \mathrm { a } }$ intercepts target-window $\gamma _ { i , j }$ if $\tau _ { \mathrm { a } }$ intercepts target i at some $t \in [ \underline { { t } } _ { i , j } , \overline { { t } } _ { i , j } ]$

${ \mathcal E } _ { \mathrm { t w } }$ contains an edge from $\gamma _ { i , j }$ to $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ if $i \neq i ^ { \prime } .$ . Each edge $( \gamma _ { i , j } , \gamma _ { i ^ { \prime } , j ^ { \prime } } ) \in \mathcal { E } _ { \mathrm { t w } }$ contains a value $\mathrm { L F D T } ( \gamma _ { i , j } , \gamma _ { i ^ { \prime } , j ^ { \prime } } , \bar { t } _ { i ^ { \prime } , j ^ { \prime } } )$ called the latest feasible departure time. The LFDT is the latest time $t \in [ \underline { { t } } _ { i , j } , \bar { t } _ { i , j } ]$ such that a feasible agent trajectory exists beginning at space-time point $( \tau _ { i } ( t ) , t )$ and intercepting $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ at time $\bar { t } _ { i ^ { \prime } , j ^ { \prime } }$ . We compute LFDT for all edges at the beginning of BPRC using the method from [14].

A tour is a path in $\mathcal { G } _ { \mathrm { t w } }$ beginning and ending at $\gamma _ { 0 } ,$ visiting at most one target-window per non-fictitious target, such that (i) the sum of demands of visited targets is no larger than $d _ { \mathrm { m a x } }$ , and (ii) a feasible agent trajectory exists intercepting the target-windows in the tour in sequence. For a tour Γ, let Γ[n] denote the nth element of Γ; in the subsequent text, we use the same bracket notation to indicate the nth element of any sequence. Let Len(Γ) denote the number of target-windows in Γ. An agent trajectory $\tau _ { \mathrm { a } }$ executes Γ if $\tau _ { \mathrm { a } }$ intercepts the target-windows in Γ in sequence, and $\tau _ { \mathrm { a } }$ is feasible. For a tour Γ, the cost of Γ, denoted as $c ^ { * } ( \Gamma )$ , is the distance traveled by a minimum-distance trajectory executing Γ. We compute the cost of a tour by solving an SPP-GCS, described in Section V-G.

Let the set of all tours be S. Lazy BPRC formulates the MT-VRP-O as the problem of selecting a set ${ \mathcal { F } } _ { \mathrm { s o l } } \subseteq { \mathcal { S } }$ containing up to $n _ { \mathrm { a g t } }$ tours, such that every target is visited by some selected tour, and the sum of tour costs is minimized. In particular, for a tour Γ, let $\alpha ( i , \Gamma ) = 1$ if Γ visits target i and let $\alpha ( i , \Gamma ) = 0$ otherwise. Define a binary variable $\theta _ { k }$ which equals 1 if tour k is selected and 0 otherwise. We formulate the MT-VRP-O as the following ILP:

$$
\min _ {\{\theta_ {k} \} _ {\Gamma_ {k} \in \mathcal {S}}} \quad \sum_ {\Gamma_ {k} \in \mathcal {S}} c ^ {*} (\Gamma_ {k}) \theta_ {k}\tag{1a}
$$

$$
\text { s.t. } \quad \sum_ {\Gamma_ {k} \in \mathcal {S}} \theta_ {k} \leq n _ {\mathrm{agt}}\tag{1b}
$$

$$
\sum_ {\Gamma_ {k} \in \mathcal {S}} \alpha (i, \Gamma_ {k}) \theta_ {k} \geq 1 \forall i \in \{1, \dots , n _ {\mathrm{tar}} \}\tag{1c}
$$

$$
\theta_ {k} \in \{0, 1 \} \forall k \in \{1, \dots , | \mathcal {S} | \}\tag{1d}
$$

(1a) minimizes the sum of tour costs, (1b) ensures that no more than $n _ { \mathrm { a g t } }$ tours are selected, (1c) ensures all targets are visited, and (1d) enforces that each $\theta _ { k }$ is binary.

## V. LAZY BPRC

## A. Preliminaries

When solving ILP (1), explicitly having decision variables for every $\Gamma _ { k } \in \textit { s }$ is intractable, since the number of tours grows factorially with the numbers of targets. Thus, Lazy BPRC maintains a subset ${ \mathcal { F } } \subseteq S .$ , which is enlarged throughout the algorithm, and only selects tours from F. For each tour $\Gamma \in \mathcal { F }$ , we maintain a lower bound c(Γ) and an upper bound c(Γ) on $c ^ { * } ( \Gamma )$ . At the time when we add a tour Γ into ${ \mathcal { F } } _ { : }$ we compute the lower bound using the method from Section V-D and the upper bound using the method from Section V-E, and we refer to Γ as unevaluated. Over the course of the algorithm, we compute $c ^ { * } ( \Gamma )$ for certain tours Γ, then set their lower and upper bounds equal to c<sup>∗</sup>(Γ); we refer to such tours Γ as evaluated. For a set of tours $\mathcal { F } _ { \mathrm { s o l } }$ that is feasible for ILP (1), let $\overline { { c } } ( \mathcal { F } _ { \mathrm { s o l } } ) = \sum _ { \Gamma \in \mathcal { F } _ { \mathrm { s o l } } } \overline { { c } } ( \Gamma )$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Lazy BPRC
1: $\mathcal{F}_{\mathrm{inc}} = \text{GenerateFeasibleSolution}()$
2: if $\mathcal{F}_{\mathrm{inc}} = \emptyset$ then return INFEASIBLE
3: $\mathcal{F} = \text{Copy}(\mathcal{F}_{\mathrm{inc}})$
4: STACK = [$\emptyset$]
5: while STACK is not empty do
6:    $\mathcal{B} = \text{STACK.pop}()$
7:    while true do
8:    $\theta, \underline{c}(\theta) = \text{SolveLP-}\mathcal{B}(\mathcal{F}, \mathcal{F}_{\mathrm{inc}})$
9:    if $\theta$ is purely integer AND $\underline{c}(\theta) &lt; \overline{c}_{\mathrm{inc}}$ then
10:    $\mathcal{F}_{\mathrm{sol}} = \text{ExtractTours}(\theta, \mathcal{F})$
11:    $\mathcal{F}_{\mathrm{uneval}} = \text{GetUnevaluatedTours}(\mathcal{F}_{\mathrm{sol}})$
12:    ComputeTourCosts($\mathcal{F}_{\mathrm{uneval}}$)
13:    if $\overline{c}(\mathcal{F}_{\mathrm{sol}}) &lt; \overline{c}_{\mathrm{inc}}$ then $\mathcal{F}_{\mathrm{inc}} = \mathcal{F}_{\mathrm{sol}}$
14:    else break
15:    if $\underline{c}(\theta) \geq \overline{c}_{\mathrm{inc}}$ then continue
16:    $\mathcal{B}', \mathcal{B}'' = \text{GenerateSuccessors}(\mathcal{B}, \theta, \mathcal{F})$
17:    STACK.push($B'$)
18:    STACK.push($\mathcal{B}''$)
19: return $\mathcal{F}_{\mathrm{inc}}$
</div>

## B. Branch and Bound

Lazy BPRC solves ILP (1) via the branch-and-bound procedure shown in Alg. 1. The algorithm begins by generating an initial feasible solution ${ \mathcal { F } } _ { \mathrm { i n c } }$ for ILP (1), using the method in Section V-H. We call ${ \mathcal { F } } _ { \mathrm { i n c } }$ the incumbent, and we continually update ${ \mathcal { F } } _ { \mathrm { i n c } }$ to be the best solution to ILP (1) found so far, where “best” refers to smallest c-value. We initialize the subset ${ \mathcal F } ,$ introduced in Section V-A, to ${ \mathcal { F } } _ { \mathrm { i n c } }$ Define $\overline { { c } } _ { \mathrm { i n c } }$ as always taking the value of $\overline { { c } } ( \mathcal { F } _ { \mathrm { i n c } } )$

Next, we initialize a stack of branch-and-bound nodes, where each node B is a set of disallowed edges in ${ \mathcal E } _ { \mathrm { t w } }$ . Let ILP-B be ILP (1), with the constraint $\theta _ { k } = 0$ for any $\Gamma _ { k }$ traversing an edge in B. Let LP-B be the convex relaxation of ILP-B which replaces constraint (1d) with $\theta _ { k } \ge 0 \colon \mathrm { L P } { - } B$ is often called the master problem in branch-and-price. Let $c ^ { * } ( B )$ be the optimal cost of LP-B.

When we expand B, we compute a lower bound on the optimal cost of ILP-B, which we obtain from a lower bound on the optimal cost of LP-B. In particular, we enter a loop that solves LP-B with lazy evaluation of tours in $\mathcal { F }$ (Line 7). On Line 8, we solve LP-B, but replace $c ^ { * } ( \Gamma _ { k } )$ in the objective (1a) with $\underline { { c } } ( \Gamma _ { k } )$ : we call this problem the surrogate master problem, LP-B. We obtain a solution θ to LP-B using column generation, which may add tours to $\mathcal { F }$ and update ${ \mathcal { F } } _ { \mathrm { i n c } }$ (Section V-C). On Line $8 , \ \underline { c } ( \theta )$ denotes the cost of θ within LP-B. Note that θ may not be optimal for LP-B, but we ensure that

$$
\underline {{c}} (\theta) \leq c ^ {*} (\mathcal {B})\tag{2}
$$

as described in Section V-F.

We then check if θ is purely integer and $\underline { { c } } ( \theta ) < \overline { { c } } _ { \mathrm { i n c } }$ (Line 9). If so, θ corresponds to a set of tours $\mathcal { F } _ { \mathrm { s o l } }$ whose actual cost may be lower than $\overline { { c } } _ { \mathrm { i n c } }$ . Let $\mathcal { F } _ { \mathrm { u n e v a l } }$ be the set of unevaluated tours in $\mathcal { F } _ { \mathrm { s o l } }$ . We must have $\mathcal { F } _ { \mathrm { u n e v a l } } \neq \emptyset$ , since as we explain in Section V-C, while solving LP-B, whenever we obtain an integer solution θ whose corresponding set $\mathcal { F } _ { \mathrm { s o l } }$ has all tours evaluated, we set $\mathcal { F } _ { \mathrm { i n c } } = \mathcal { F } _ { \mathrm { s o l } }$ . Thus, we evaluate each $\Gamma _ { k } \in \mathcal { F } _ { \mathrm { u n e v a l } }$ by solving an SPP-GCS (Section V-G), then solve LP-B again.

After exiting the lazy evaluation loop, if $\underline { { c } } ( \theta ) \geq \overline { { c } } _ { \mathrm { i n c } } .$ , we continue to the next expansion. Otherwise, the failure of the conditions on Lines 9 and 15 imply that θ contains noninteger values. We create two successors for B, denoted as $B ^ { \prime }$ and $B ^ { \prime \prime }$ , such that θ is feasible for neither $\mathrm { L P } { \cdot } B ^ { \prime }$ nor LP- $\cdot B ^ { \prime \prime } .$ but all integer solutions to ILP-B are feasible for both ILP-B<sup>′</sup> and $\mathrm { I L P } { - } B ^ { \prime \prime }$ . To do so, we apply “conventional branching” [15]. In particular, for an edge $e \in \mathcal { E } _ { \mathrm { t w } }$ , define the flow along e as the sum of $\theta _ { k }$ values for all $\Gamma _ { k }$ traversing e. We select the edge e with flow closest to 0.5 and let $B ^ { \prime } = B \cup \{ e \}$ . We then define $B ^ { \prime \prime }$ so that e is required be traversed by some tour in a solution to $\mathrm { I I } \mathrm { { } P } { - } B ^ { \prime \prime }$ , by disallowing other edges appropriately (see [15]). We push $B ^ { \prime }$ and $B ^ { \prime \prime }$ onto the stack.

## C. Column Generation

We now describe how we find a solution θ for LP-B satisfying (2). As stated in Section V-A, enumerating all the decision variables for LP-B is intractable, so we use column generation [11]. In particular, define the restricted surrogate master problem (RSMP) on $\mathcal { F }$ as LP-B with the constraint that $\theta _ { k } = 0$ for all tours $\Gamma _ { k } \notin \mathcal { F }$ . Note that to solve the RSMP, we do not have to solve for $\theta _ { k }$ with $\Gamma _ { k } \notin { \mathcal { F } } .$ To find a solution θ to $\underline { { \mathrm { L P } ^ { - } } } B$ satisfying (2), we alternate between solving the RSMP on $\mathcal { F }$ and adding tours to ${ \mathcal F } .$ To find tours to add to ${ \mathcal F } ,$ we solve a pricing problem (Section V-F). Whenever we obtain an integer solution θ to the RSMP, this corresponds to a feasible solution $\mathcal { F } _ { \mathrm { s o l } }$ to the MT-VRP-O. In this case, if $\overline { { c } } ( \mathcal { F } _ { \mathrm { s o l } } ) < \overline { { c } } _ { \mathrm { i n c } }$ , we set $\mathcal { F } _ { \mathrm { i n c } } = \mathcal { F } _ { \mathrm { s o l } }$

We alternate between the RSMP and pricing problem until the pricing problem finds no new tours, and we return the optimal RSMP solution θ. The first time we solve the RSMP, it may be infeasible, because all feasible MT-VRP-O solutions that can be constructed from tours in $\mathcal { F }$ traverse some edge in B. In this case, we use the method from Section V-H to generate a set of tours $\mathcal { F } _ { \mathrm { n e w } }$ feasible for the MT-VRP-O, add these tours to $\mathcal { F } _ { \mathrm { s o l } } .$ , and solve the RSMP again. If we fail to generate $\mathcal { F } _ { \mathrm { n e w } }$ , we return $\theta = { \mathrm { N U L I } }$ and $\underline { { c } } ( \theta ) = \infty$

## D. Computing Lower Bound on Tour Cost

This section describes how we compute the lower bound $\underline { { c } } ( \Gamma )$ for a tour Γ in Section V. Our method, illustrated in Fig. $^ { 2 , }$ extends the procedure from BPRC [8] to handle obstacles. At the beginning of Lazy BPRC, we divide each targetwindow $\gamma _ { i , j }$ into segments, where $\xi _ { i , j , k } = ( i , [ t _ { i , j , k } , \bar { t } _ { i , j , k } ] )$ denotes the kth segment of $\gamma _ { i , j }$ , and Segments $( \gamma _ { i , j } )$ is the set of segments of $\gamma _ { i , j }$ . To determine the number of segments per target-window, we first specify a number of segments to allocate per target, denoted as $n _ { \mathrm { s e g , t a r } }$ . Then for each target i, we allocate segments to its windows using the formula from BPRC [8], which gives more segments to longer windows. The depot gets a single segment $\xi _ { 0 }$ . For a target-window $\gamma , n _ { \mathrm { s e g } } ( \gamma )$ is the number of segments allocated to $\gamma$ . The segment indices for a target-window are ordered in increasing order of start time. An agent trajectory $\tau _ { \mathrm { a } }$ intercepts segment $\xi _ { i , j , k }$ if $\tau _ { \mathrm { a } }$ intercepts target i at a time $t \in [ \underline { { t } } _ { i , j , k } , \overline { { t } } _ { i , j , k } ]$

For every pair of segments $( \xi , \xi ^ { \prime } )$ corresponding to different targets, we compute a lower bound $c _ { \mathrm { s e g } } ( \xi , \xi ^ { \prime } )$ on the cost of a feasible agent trajectory that intercepts ξ, then $\xi ^ { \prime }$ . To do so, we compute the shortest collision-free path in space from $\xi$ to $\xi ^ { \prime }$ ignoring time constraints, via the method from [16]. Let c be the path’s distance traveled. Let t be the start time of $\xi ,$ and let t<sup>′</sup> be the end time of $\xi ^ { \prime }$ . We set $c _ { \mathrm { s e g } } ( \xi , \xi ^ { \prime } ) = c$ if $t + c / v _ { \mathrm { m a x } } \le t ^ { \prime }$ , and $c _ { \mathrm { s e g } } ( \xi , \xi ^ { \prime } ) = \infty$ otherwise.

Next, given a tour Γ, we define a segment-graph $\mathcal { G } _ { \mathrm { s e g } } =$ $( \nu _ { \mathrm { s e g } } , \mathcal { E } _ { \mathrm { s e g } } )$ , where the set of nodes $\mathcal { V } _ { \mathrm { s e g } }$ is the set of all segments whose target-windows are visited by Γ. For each edge $( \Gamma [ n ] , \Gamma [ n + 1 ] ) \in \mathcal { E } _ { \mathrm { t w } }$ traversed by Γ, we connect edges in $\mathcal { E } _ { \mathrm { s e g } }$ from every segment of Γ[n] to every segment of $\Gamma [ n + 1 ]$ . The cost of each edge $( \xi , \xi ^ { \prime } )$ is $c _ { \mathrm { s e g } } ( \xi , \xi ^ { \prime } )$

Let $g _ { \mathrm { s e g } } ( \xi )$ be the cost of the shortest path in $\mathcal { G } _ { \mathrm { s e g } }$ from $\xi _ { 0 }$ to $\xi . \ \underline { { c } } ( \Gamma )$ , computed as follows, lower-bounds $c ^ { * } ( \Gamma )$

$$
\underline {{c}} (\Gamma) = \min _ {\xi \in \text { Segments } (\Gamma [ \text { Len } (\Gamma) - 1 ])} (g _ {\text { seg }} (\xi) + c _ {\text { seg }} (\xi , \xi_ {0}))\tag{3}
$$

$g _ { \mathrm { s e g } } ( \xi _ { 0 } ) ~ = ~ 0 .$ , and for a segment $\xi ^ { \prime }$ of $\Gamma [ n ]$ with $1 \_ <$ $n < \mathrm { L e n } ( \Gamma )$ , we have $g _ { \mathrm { s e g } } ( \xi ^ { \prime } ) = \operatorname* { m i n } _ { \xi \in \mathrm { S e g m e n t s } ( \Gamma \left[ n - 1 \right] ) } \left( g _ { \mathrm { s e g } } ( \xi ) + \right.$ $c _ { \mathrm { s e g } } ( \xi , \xi ^ { \prime } ) )$ . Thus to compute $\underline { { c } } ( \Gamma )$ we can iterate from $n = 2$ to $n = \mathrm { L e n } ( \Gamma ) - 1$ , and for each $n ,$ , compute the g-values of the segments of $\Gamma [ n ]$ using the g-values for $\Gamma [ n - 1 ]$

![](Bhat2026Optimal_figs/e4c907f9940da9f55307d8a4f18233bbd139c9f222b07293349c5143232339af.jpg)  
Fig. 2. Computing bounds on the cost of an example tour Γ. To compute the lower bound $\underline { { c } } ( \Gamma )$ , we divide each target-window visited by Γ into segments. We then construct a segment-graph $\mathcal { G } _ { \mathrm { s e g } } ,$ where the nodes are the segments, and an edge connects every segment of Γ[n] to every segment of $\Gamma [ \breve { n } + 1 ] .$ . The edge cost from segment ξ to $\xi ^ { \prime }$ is the distance traveled along the shortest path in space from ξ to $\check { \xi } ^ { \prime } ,$ , if this path satisfies the relaxed timing constraints from in Section V-D, and ∞ otherwise. $\underline { { c } } ( \Gamma )$ is the cost of the shortest path in $\mathcal { G } _ { \mathrm { s e g } }$ from $\xi _ { 0 }$ to $\xi _ { 0 }$ visiting all target-windows in Γ. To compute the upper bound ${ \overline { { c } } } ,$ we construct a segment-start-graph $\mathcal { G } _ { \mathrm { s t a r t } } ,$ where the nodes are the starting points of the segments, and an edge connects every segment-start of $\Gamma [ n ]$ to every segment-start of $\Gamma [ n + 1 ]$ . The edge cost from s to $s ^ { \prime }$ is distance traveled by a feasible minimum-distance agent trajectory from s to $s ^ { \prime } ,$ if such a trajectory exists or if $s ^ { \prime } = s _ { 0 }$ , and ∞ otherwise. Our upper bound is the cost of the shortest path in $\mathcal { G } _ { \mathrm { s t a r t } }$ from s to $s _ { 0 }$ that visits all target-windows in Γ.

After this, we can compute c(Γ) via (3). As shown in Fig. 2, these computations correspond to finding an agent trajectory executing Γ subject to relaxed continuity constraints.

For tours generated in the pricing problem (Section V-F), these g-values are computed as a byproduct of solving the pricing problem. For tours generated using the feasible solution generation method in Section V-H, we perform these g-value computations after generating the tours.

## E. Computing Upper Bound on Tour Cost

This section describes how we compute the upper bound $\overline { { c } } ( \Gamma )$ for a tour Γ in Section V. Recall that in Section V-D, we divided each target-window into segments. Let the starting point in space-time of segment $\xi _ { i , j , k }$ be $s _ { i , j , k } = ( \tau _ { i } ( \underline { { t } } _ { i , j , k } ) , \underline { { t } } _ { i , j , k } )$ . Denote the starting point of the depot segment as $s _ { 0 } ~ = ~ s _ { 0 , 1 , 1 }$ . For a target-window $\gamma$ , let SegmentStarts(γ) denote the set of segment-starts of $\gamma$ . We construct a segment-start-graph $\mathcal { G } _ { \mathrm { s t a r t } } = ( \nu _ { \mathrm { s t a r t } } , \mathcal { E } _ { \mathrm { s t a r t } } )$ . The set of nodes $\mathcal { V } _ { \mathrm { s t a r t } }$ is the set of all segment-starts whose targetwindows are visited by Γ. For each edge $( \gamma , \gamma ^ { \prime } ) ~ \in ~ \mathcal { E } _ { \mathrm { t w } }$ traversed by Γ, we connect an edge in ${ \mathcal E } _ { \mathrm { s t a r t } }$ from every segment-start of γ to every segment-start of $\gamma ^ { \prime } .$

To determine the cost of an edge from $s ~ = ~ ( q , t )$ to $s ^ { \prime } = ( q ^ { \prime } , t ^ { \prime } )$ , denoted as $c _ { \mathrm { s t a r t } } ( s , s ^ { \prime } )$ , we compute the shortest collision-free path in space from q to $q ^ { \prime }$ using [17]. Let the distance traveled by this path be c. If $t + c / v _ { \mathrm { m a x } } \le t ^ { \prime }$ or $s ^ { \prime } =$ $s _ { 0 }$ , we set $c _ { \mathrm { s t a r t } } ( s , s ^ { \prime } ) = c ,$ and otherwise $c _ { \mathrm { s t a r t } } ( s , s ^ { \prime } ) = \infty$

Define $g _ { \mathrm { s t a r t } } ( s )$ as the cost of a shortest path in G<sub>start</sub> from $s _ { 0 }$ to $s . \ { \overline { { c } } } ( \Gamma )$ , computed as follows, upper-bounds $c ^ { * } ( \Gamma )$ :

$$
\overline {{c}} (\Gamma) = \min _ {s \in \text { SegmentStarts } (\Gamma [ \text { Len } (\Gamma) - 1 ])} (g _ {\text { start }} (s) + c _ {\text { start }} (s, s _ {0}))\tag{4}
$$

To compute c(Γ), we note that $g ( s _ { 0 } ) ~ = ~ 0 \quad$ , and for a segment $\xi ^ { \prime }$ of $\Gamma [ n ]$ with $1 < n < \mathsf { L e n } ( \Gamma )$ , we have $g _ { \mathrm { s t a r t } } ( s ^ { \prime } ) = \operatorname* { m i n } _ { s \in \mathrm { S e g m e n t S t a r t s } ( \Gamma \left\lceil n - 1 \right\rceil ) } \left( g _ { \mathrm { s t a r t } } ( s ) + c _ { \mathrm { s t a r t } } ( s , s ^ { \prime } ) \right)$ . Thus, we can iterate from $n \stackrel { . } { = } \mathrm { { 2 } } \ \mathrm { t o } \tilde { n } = \mathrm { { L e n } } ( \Gamma ) - 1$ , and for each $n ,$ compute the g-values of the segment-starts of Γ[n] using the g-values for $\Gamma [ n - 1 ]$ . Then we can compute $\overline { { c } } ( \Gamma )$ using (4). For tours generated within the pricing problem (Section V-F), this computation happens as a byproduct and does not require extra computation. For tours generated using the feasible solution generation method in Section V-H, we must compute these g-values separately from the tour generation.

We place points $s _ { i , j , k }$ at the segment-starts rather than at arbitrary points because, within the pricing problem (Section V-F), we need an upper bound on the cost of reaching each segment-start for dominance checking.

## F. Pricing Problem

The pricing problem seeks a set of tours $\mathcal { F } _ { \mathrm { p r i c e } }$ such that the RSMP on $\mathcal { F } \cup \mathcal { F } _ { \mathrm { p r i c e } }$ has a smaller optimal cost than the RSMP on $\mathcal { F }$ . To solve the pricing problem, we first note that when the RSMP produces a solution θ (specifically, its primal solution), the RSMP also produces a dual solution $( \lambda _ { 0 } , \lambda _ { 1 } , \ldots , \lambda _ { n _ { \mathrm { t a r } } } )$ , where $\lambda _ { 0 } ~ \in ~ \mathbb { R } _ { < 0 }$ is the dual variable corresponding to (1b), and for $i > 0 , \lambda _ { i } \in \mathbb { R } _ { \ge 0 }$ is the dual variable corresponding to (1c). Similarly to prior VRP work [11], we define the reduced cost of Γ as follows:

$$
\underline {{c}} _ {\mathrm{red}} (\Gamma) = \underline {{c}} (\Gamma) - c _ {\mathrm{dual}} (\Gamma)\tag{5}
$$

where $c _ { \mathrm { d u a l } } ( \Gamma ) = \sum _ { i = 1 } ^ { n _ { \mathrm { t a r } } } \alpha ( i , \Gamma ) \lambda _ { i } + \lambda _ { 0 }$ . To improve the RSMP’s optimal cost, $\mathcal { F } _ { \mathrm { p r i c e } }$ must contain a tour with negative reduced cost [11]. Therefore, as in prior work, we search for tours with negative reduced cost.

In contrast to prior work, we do not guarantee returning a tour with negative reduced cost if such a tour exists. Instead, we only guarantee returning some Γ such that $c ^ { * } ( \Gamma ) - c _ { \mathrm { { d u a l } } } ( \Gamma ) < 0 .$ , if such Γ exists. This is sufficient to ensure that if we do not return any tours, then (2) is satisfied, as shown in the proof of Lemma 1.

We search for tours with negative reduced cost by mod ifying the labeling algorithm from [8] to handle obstacles. First, we define a partial tour, which has the same definition as a tour from Section IV, except that a partial tour does not need to end with the depot.

1) Labels and Label Dominance: Within our labeling algorithm, we represent a partial tour Γ using a label $l =$ $( \gamma _ { i , j } , t , \sigma , \vec { b } , \vec { g } _ { \mathrm { u b } } , \vec { g } _ { \mathrm { l b } } , \lambda )$ , where

$\gamma _ { i , j }$ is the final target-window in Γ

• t is the minimum time required to execute Γ

• $\sigma$ is the sum of demands of targets visited by Γ

$\dot { b }$ is a binary vector with length $n _ { \mathrm { t a r } }$ where $\vec { b } [ i ^ { \prime } ] = 1$ for any target i<sup>′</sup> such that either (i) Γ visits $i ^ { \prime } , \mathrm { ( i i ) } t >$ $\mathrm { L F D T } ( \gamma _ { i , j } , \gamma _ { i ^ { \prime } , j ^ { \prime } } )$ for all $j ^ { \prime } \in \{ 1 , 2 , \dots , n _ { \mathrm { w i n } } ( i ^ { \prime } ) \}$ , or (iii) $\sigma + d _ { i ^ { \prime } } > d _ { \operatorname* { m a x } }$

$\vec { g } _ { \mathrm { u b } }$ is a vector with length $n _ { \mathrm { s e g } } ( \gamma _ { i , j } )$ where, if Γ is not a tour, ${ \vec { g } } _ { \mathrm { u b } } [ k ] = g _ { \mathrm { s t a r t } } ( s _ { i , j , k } )$ within the segment-startgraph for all tours extending from Γ. If Γ is a tour, $\vec { g } _ { \mathrm { u b } }$ contains a single element equal to c(Γ), as computed in Section V-E (i.e. not the true tour cost)

• ⃗g<sub>lb</sub> is a vector with length $n _ { \mathrm { s e g } } ( \gamma _ { i , j } )$ where, if Γ is not a tour, we have $\vec { g } _ { \mathrm { l b } } [ k ] = g _ { \mathrm { s e g } } ( \xi _ { i , j , k } )$ within the segmentgraph for all tours extending from Γ. If Γ is a tour, ⃗g<sub>lb</sub> contains a single element equal to $\underline { { c } } ( \Gamma )$ , as computed in Section V-E (i.e. not the true tour cost)

$$
\lambda = c _ {\text { dual }} (\Gamma)
$$

Consider two labels $l = ( \gamma _ { i , j } , t , \sigma , \vec { b } , \vec { g } _ { \mathrm { u b } } , \vec { g } _ { \mathrm { l b } } , \lambda )$ and $l ^ { \prime } =$ $( \gamma _ { i , j } , t ^ { \prime } , \sigma ^ { \prime } , \vec { b } ^ { \prime } , \vec { g } _ { \mathrm { u b } } ^ { \prime } , \vec { g } _ { \mathrm { l b } } ^ { \prime } , \lambda ^ { \prime } )$ , both at target-window $\gamma _ { i , j } . \mathrm { ~ H f ~ }$ $\gamma _ { i , j } = \gamma _ { 0 }$ , we say l dominates l<sup>′</sup> if $\begin{array} { r } { \vec { g } _ { \mathrm { u b } } [ \breve { 1 } ] - \lambda \le \vec { g } _ { \mathrm { l b } } ^ { \prime } [ \breve { 1 } ] ^ { \cup } - \lambda . } \end{array}$ Otherwise, l dominates l<sup>′</sup> if

$$
\sigma \leq \sigma^ {\prime}\tag{6}
$$

$$
\vec {b} [ i ^ {\prime} ] \leq \vec {b} ^ {\prime} [ i ^ {\prime} ], \forall i ^ {\prime} \in \{1, \dots , n _ {\mathrm{tar}} \}\tag{7}
$$

$$
\vec {g} _ {\mathrm{ub}} [ k ] + \delta (\xi_ {i, j, k}) - \lambda \leq \vec {g} _ {\mathrm{lb}} ^ {\prime} [ k ] - \lambda^ {\prime}, \forall k \in \{1, \dots , n _ {\mathrm{seg}} (\gamma_ {i, j}) \}\tag{8}
$$

where $\delta ( \xi _ { i , j , k } )$ is the length of segment $\xi _ { i , j , k }$ in space. Let Γ be the partial tour represented by l and $\Gamma ^ { \prime }$ be the partial tour represented by $l ^ { \prime } .$ . Let Ω be the tour extending Γ such that $c ^ { * } ( \Omega ) - c _ { \mathrm { d u a l } } ( \Omega )$ is minimal, and let $\Omega ^ { \prime }$ be the tour extending $\Gamma ^ { \prime }$ such that $c ^ { * } ( \Omega ^ { \prime } ) - c _ { \mathrm { d u a l } } ( \Omega ^ { \prime } )$ is minimal. If l dominates $\bar { l ^ { \prime } }$ by our definition above, then $c ^ { * } ( \Omega ) - c _ { \mathrm { d u a l } } ( \Omega ) < c ^ { * } ( \Omega ^ { \prime } ) -$ $c _ { \mathrm { d u a l } } ( \Omega ^ { \prime } )$ ([8], Theorem 1).

In particular, (6) and (7) are standard dominance conditions from the VRP literature [10], ensuring that any sequence of target-windows that can be appended to Γ can also be appended to $\Gamma ^ { \prime }$ without the violating the capacity constraint or causing a target to be revisited.

Condition (8) is specific to moving targets. Consider trajectories $\tau _ { \mathrm { a } }$ and $\tau _ { \mathrm { a } } ^ { \prime }$ that execute Γ and $\Gamma ^ { \overline { { \prime } } }$ , respectively, and terminate by intercepting $\xi _ { i , j , k } ,$ , with minimum distance traveled. Define the reduced cost of $\tau _ { \mathrm { a } }$ as the distance traveled minus $\lambda ,$ , and the reduced cost of $\tau _ { \mathrm { a } } ^ { \prime }$ likewise using $\lambda ^ { \prime } .$ . The term $\vec { g } _ { \mathrm { u b } } [ k ]$ on the LHS of (8) upper-bounds the distance an agent must travel to execute Γ and travel to the start of $\xi _ { i , j , k } ,$ , and $\delta ( \xi _ { i , j , k } )$ is the distance an agent must travel from the start of $\xi _ { i , j , k }$ to the end, i.e. to visit every point in the segment. Thus, the sum of these two terms upperbounds the cost of $\tau _ { \mathrm { a } } ,$ since $\tau _ { \mathrm { a } }$ cannot do worse than travel to the start of $\xi _ { i , j , k }$ , then move along $\xi _ { i , j , k }$ to the point of interception. Thus the LHS upper-bounds the reduced cost of $\tau _ { \mathrm { a } } .$ . The $\vec { g } _ { \mathrm { 1 b } } ^ { \prime }$ lower-bounds the distance traveled by $\tau _ { \mathrm { a } } ^ { \prime } \mathrm { : }$ , so the RHS lower-bounds the reduced cost of $\tau _ { \mathrm { a } } ^ { \prime }$ . If condition (8) holds, $\tau _ { \mathrm { a } }$ cannot be worse (i.e. cannot have more positive reduced cost) than $\tau _ { \mathrm { a } } ^ { \prime }$ and we can discard $l ^ { \prime } .$

2) Labeling Algorithm: Our labeling algorithm maintains a set of mutually nondominated labels at each target-window, as well as a priority queue, where labels with lexicographically smaller $( t , \sigma , \operatorname* { m i n } ( g _ { \mathrm { l b } } ) - \lambda )$ have higher priority. When we expand a label $l = ( \gamma _ { i , j } , t , \sigma , \vec { b } , \vec { g } _ { \mathrm { u b } } , \vec { g } _ { \mathrm { l b } } , \lambda )$ , we iterate over all successor target-windows of l, i.e. all target-windows $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ satisfying the following conditions:

$$
1) \left(\gamma_ {i, j}, \gamma_ {i ^ {\prime}, j ^ {\prime}}\right) \in \mathcal {E} _ {\mathrm{tw}} \setminus \mathcal {B}
$$

2) $t \leq \mathrm { L F D T } ( \gamma _ { i , j } , \gamma _ { i ^ { \prime } , j ^ { \prime } } )$

3) $\sigma + d _ { i ^ { \prime } } \leq d _ { \operatorname* { m a x } }$

4) If ${ \mathit { i } } ^ { \prime } \neq 0 ,$ then $\vec { b } [ i ^ { \prime } ] = 0$

For each successor target-window $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ , we generate a successor label $l ^ { \prime } = ( \gamma _ { i ^ { \prime } , j ^ { \prime } } , t ^ { \prime } , \sigma ^ { \prime } , \vec { b } ^ { \prime } , \vec { g } _ { \mathrm { u b } } ^ { \prime } , \vec { g } _ { \mathrm { l b } } ^ { \prime } , \lambda ^ { \prime } )$ , where

$t ^ { \prime } = \mathrm { E F A T } ( \gamma _ { i , j } , \gamma _ { i ^ { \prime } , j ^ { \prime } } , t )$ , where EFAT is the earliest time at which a feasible agent trajectory can intercept $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ after intercepting $\gamma _ { i , j }$ at time t. EFAT stands for “earliest feasible arrival time,” and we compute it using the method from [14].

$$
\sigma^ {\prime} = \sigma + d _ {i ^ {\prime}}
$$

$\vec { b ^ { \prime } }$ is identical to $\vec { b , }$ except for the following modifications. First, if $i ^ { \prime } \ne 0$ , we set $\vec { b } ^ { \prime } [ i ^ { \prime } ] = 1$ . Then, we set $\vec { b ^ { \prime } } [ i ^ { \prime \prime } ] = 1$ for each target $i ^ { \prime \prime }$ such that either (i) $\sigma ^ { \prime } + d _ { i ^ { \prime \prime } } > d _ { \mathrm { m a x } }$ , or (ii) for all $j ^ { \prime \prime } \in \{ 1 , 2 , \dots , n _ { \mathrm { w i n } } ( i ^ { \prime \prime } ) \}$ $t ^ { \prime } > \mathrm { L F D T } ( \gamma _ { i ^ { \prime } , j ^ { \prime } } , \gamma _ { i ^ { \prime \prime } j ^ { \prime \prime } } )$

• For each $k ^ { \prime } \in \{ 1 , 2 , \dotsc , n _ { \mathrm { s e g } } ( \gamma _ { i ^ { \prime } , j ^ { \prime } } ) \}$ , we compute

$$
\vec {g} _ {\mathrm{ub}} ^ {\prime} [ k ^ {\prime} ] = \min _ {k \in \{1, 2, \dots , n _ {\text {seg}} (\gamma_ {i, j}) \}} \vec {g} _ {\mathrm{ub}} [ k ] + c _ {\text {start}} (s _ {i, j, k}, s _ {i ^ {\prime}, j ^ {\prime}, k ^ {\prime}})\tag{9}
$$

• For each $k ^ { \prime } \in \{ 1 , 2 , \dots , n _ { \mathrm { s e g } } ( \gamma _ { i ^ { \prime } , j ^ { \prime } } ) \}$ , we compute

$$
\vec {g} _ {\mathrm{lb}} ^ {\prime} [ k ^ {\prime} ] = \min _ {k \in \{1, 2, \dots , n _ {\mathrm{seg}} (\gamma_ {i, j}) \}} \vec {g} _ {\mathrm{lb}} [ k ] + c _ {\mathrm{seg}} (\xi_ {i, j, k}, \xi_ {i ^ {\prime}, j ^ {\prime}, k ^ {\prime}})\tag{10}
$$

• λ<sup>′</sup> = λ, if $i ^ { \prime } = 0 .$ , and $\lambda ^ { \prime } = \lambda + \lambda _ { i ^ { \prime } }$ ′ otherwise

We then check if any labels at $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ dominate $l ^ { \prime } .$ If so, we prune $l ^ { \prime } .$ Otherwise, we prune labels at $\gamma _ { i ^ { \prime } , j ^ { \prime } }$ dominated by $l ^ { \prime } ,$ , and we mark them to be discarded upon expansion from the priority queue. Then we push l<sup>′</sup> onto the priority queue. Any time we generate a successor label l at $\gamma _ { 0 }$ with $\vec { g } _ { \mathrm { l b } } [ 1 ] -$ $\lambda \overset { \cdot } { < } 0 , ^ { 2 }$ , and l is not dominated, we reconstruct the tour Γ represented by l via backpointer traversal, then add Γ to the set of tours to be returned. At this step, if Γ has already been evaluated, we do not add it to this set, since $c _ { \mathrm { r e d } } ^ { * } ( \Gamma )$ cannot be negative. The search ends when the priority queue becomes empty.

## G. Computing Tour Cost via SPP-GCS

At the beginning of Lazy BPRC, we decompose free space into convex regions $\mathcal { A } _ { 1 } , \mathcal { A } _ { 2 } , \dotsc , \mathcal { A } _ { n _ { \mathrm { r e g } } } .$ , where $n _ { \mathrm { r e g } }$ is the number of regions. We then define a GCS $\mathcal { G } _ { \mathrm { c s } } = ( \dot { \mathcal { V } } _ { \mathrm { c s } } , \mathcal { E } _ { \mathrm { c s } } )$ where the set of nodes $\nu _ { \mathrm { c s } }$ consists of convex sets in spacetime. For each region A in our free space decomposition, we have a region-node $\mathcal { X } _ { \mathcal { A } } = \mathcal { A } \times \mathbb { R }$ . For each target-window $\gamma _ { i , j }$ visited by Γ, we have a window-node $\mathcal { X } _ { i , j }$ , consisting of the set of space-time points along $\tau _ { i }$ within $[ \underline { { t } } _ { i , j } , \bar { t } _ { i , j } ]$ . Since we assumed that a target’s velocity is constant within a time window, $\mathcal { X } _ { i , j }$ is a line segment in space-time, which is a convex set. We refer to nodes in $\mathcal { G } _ { \mathrm { c s } }$ as GCS-nodes. An edge connects a set $\mathcal { X }$ to a set $\mathcal { X } ^ { \prime }$ if X intersects $\mathcal { X } ^ { \prime }$ . We refer to a path in $\mathcal { G } _ { \mathrm { c s } }$ as a GCS-path. We say a GCS-path $P$ visits target-window $\gamma _ { i , j }$ if $P$ contains $\mathcal { X } _ { i , j }$

We find a trajectory executing Γ using an algorithm similar to FMC\* [13], but without the various speedup techniques that $\mathrm { F M C ^ { \ast } }$ implements particularly for a minimum-time objective, since we aim to minimize distance traveled. We also replace the heuristic from $\mathrm { F M C ^ { \ast } }$ with the heuristic described later in the section, and we replace the focal search from FMC\* with a best-first search, since we seek optimal solutions rather than bounded-suboptimal solutions.

We search the GCS using a priority queue called OPEN, containing GCS-paths. We initialize OPEN with the GCSpath $( \mathcal { X } _ { 0 , 1 } )$ , i.e. a path that stays at the depot. Each GCSpath on OPEN has an f-value. The initial GCS-path $( \mathcal { X } _ { 0 , 1 } )$ has an f-value of 0; we discuss the computation of f for other GCS-paths shortly. GCS-paths with smaller f -values have higher priority.

Each iteration pops a GCS-path P from OPEN, then iterates over each GCS-node X adjacent to $P [ - 1 ]$ . If X is a window-node $\mathcal { X } _ { i , j }$ , and $P$ has not visited the target-windows occurring before $\gamma _ { i , j }$ in Γ, we discard X . If X is a regionnode, and X already occurs in $P$ after the final window-node in $P _ { \mathrm { { : } } }$ , we discard X . If we do not discard X , we construct a successor GCS-path $P ^ { \prime }$ by appending X to $P ,$ , then compute its f -value as follows.

Suppose the first target-window in Γ unvisited by $P ^ { \prime }$ is $\Gamma [ n ]$ . We optimize a trajectory $\tau _ { \mathrm { a } }$ with a collision-free portion $\tau _ { \mathrm { a , 1 } }$ passing through the sets in P in sequence, followed by an obstacle-unaware portion $\tau _ { \mathrm { a } , 2 }$ that travels to $\Gamma [ n ]$ . We parameterize $\tau _ { \mathrm { a , 1 } }$ with a line segment per set in $P ,$ and $\tau _ { \mathrm { a } , 2 }$ with a single line segment. The objective of the trajectory optimization is a g-value plus an h-value. The g-value is the distance traveled by $\tau _ { \mathrm { a , 1 } }$ . The h-value is the distance traveled by $\tau _ { \mathrm { a } , 2 }$ , plus a term $h _ { n } ( t )$ which depends on the ending time t of $\tau _ { \mathrm { a } , 2 } . \ h _ { n } ( t )$ lower bounds the cost of intercepting the remaining targets in Γ after departing Γ[n] at time t, and we describe how to compute $h _ { n }$ in Section V-G.1.

The trajectory optimization is the same as the optimization performed for a GCS-path in $\mathrm { F M C ^ { \ast } }$ [13], except for two differences. First, FMC\* also optimizes an obstacle-unaware portion of the trajectory that departs $\Gamma [ n ]$ and intercepts all remaining targets, in place of our $h _ { n }$ value. Second, we constrain our computed trajectory to intercept $\Gamma [ n ]$ no later than a value $t _ { \mathrm { m a x } , n } ,$ which is the latest time at which a feasible agent trajectory could depart $\Gamma [ n ]$ , then intercept the remaining sequence of target-windows in Γ. We compute $t _ { \mathrm { m a x } , n }$ for each $n \in \{ 1 , 2 , \ldots , \mathrm { L e n } ( \Gamma ) \}$ } before beginning the search as follows. For $n = \mathrm { L e n } ( \Gamma )$ , we set $t _ { \operatorname* { m a x } , n } = \infty$ . We then iterate backwards from $n = \mathrm { L e n } ( \Gamma ) - 1$ to $n = 1$ , and $t _ { \mathrm { m a x } , n } = \mathrm { L F D T } ( \Gamma [ n ] , \Gamma [ n + 1 ] , t _ { \mathrm { m a x } , n + 1 } )$

Finally, if the trajectory optimization is infeasible, we discard $P ^ { \prime }$ . Otherwise, the trajectory optimization’s optimal cost is the f -value for $P ^ { \prime }$ , and we push $P ^ { \prime }$ onto OPEN.

1) Constructing $h _ { n }$ Function: Consider the segmentgraph $\mathcal { G } _ { \mathrm { s e g } }$ for Γ, as defined in Section V-D. For a segment $\xi$ in $\mathcal { G } _ { \mathrm { s e g } } ,$ let $h _ { \mathrm { s e g } } ( \xi )$ be the cost of the shortest path in $\mathcal { G } _ { \mathrm { s e g } }$ from $\xi$ to $\xi _ { 0 }$ . Note that $h ( \xi _ { 0 } ) = 0$ , and for a segment $\xi$ of Γ[n] with $1 < n < \mathsf { L e n } ( \Gamma )$ , we have

$$
h _ {\text {seg}} (\xi) = \min _ {\xi^ {\prime} \in \text {Segments} (\Gamma [ n + 1 ])} (c _ {\text {seg}} (\xi , \xi^ {\prime}) + h _ {\text {seg}} (\xi^ {\prime})).\tag{11}
$$

Before searching $\mathcal { G } _ { \mathrm { c s } } .$ , we compute $h _ { \mathrm { s e g } }$ for all ξ in $\mathcal { G } _ { \mathrm { s e g } }$ as follows. We iterate backward from $n = \mathrm { L e n } ( \Gamma ) - 1$ to $n = 2 ,$ and for each $n ,$ , we compute the h-values for the segments of Γ[n] using the h-values for $\Gamma [ n + 1 ]$ ] using (11).

Next, for each $n \in \{ 1 , 2 , \ldots , \operatorname { L e n } ( \Gamma ) \}$ , we do the following. Let $\gamma _ { i , j }$ be $\Gamma [ n ]$ . We construct a matrix $A _ { n } \in$ $\mathbb { R } ^ { n _ { \mathrm { s e g } } ( \breve { \Gamma } [ n ] ) \times 2 }$ whose kth row is $[ \underline { { t } } _ { i , j , k } , 1 ]$ . We construct a vector $\vec { b } _ { n } \in \mathbb { R } ^ { n _ { \mathrm { s e g } } ( \Gamma [ n ] ) }$ whose kth element is $h ( \xi _ { i , j , k } )$ . We then find the least-squares solution $\phi _ { n } \in \mathbb { R } ^ { 2 }$ to the equation $A _ { n } \phi _ { n } = \vec { b } _ { n }$ . For a time $t \in [ \underline { { t } } _ { i , j } , \overline { { t } } _ { i , j } ] , \phi _ { n } [ 1 ] t + \phi _ { n } [ 2 ]$ approximates the minimum cost to intercept all remaining targetwindows in Γ after departing Γ[n] at time t. To adjust this into a lower bound, we construct another matrix $B _ { n }$ whose kth row is $[ \bar { t } _ { i , j , k } , 1 ]$ , then compute a value $r _ { \mathrm { m a x } }$ as the max element of the vector vertcat $( A _ { n } , B _ { n } ) \phi _ { n } - \mathrm { v e r t c a t } ( \vec { b } _ { n } , \vec { b } _ { n } )$ where vertcat concatenates two matrices vertically. $r _ { \mathrm { m a x } }$ is the largest overestimation of $h _ { \mathrm { s e g } } ( \xi _ { i , j , k } )$ that our approximation makes over all segment start and end times of $\gamma _ { i , j } .$ . Then $h _ { n } ( t ) = \phi _ { n } [ 1 ] t + \phi _ { n } [ 2 ] - r _ { \operatorname* { m a x } }$ lower-bounds the remaining cost of executing Γ after departing $\Gamma [ n ]$ at time t.

## H. Feasible Solution Generation

To generate the initial incumbent, as well as a feasible set of tours $\mathcal { F } _ { \mathrm { n e w } }$ when the RSMP is infeasible, we extend the feasible solution generation from [8] to handle obstacles. This algorithm requires the EFAT and LFDT functions described previously. In [8], the values were computed using closed-form expressions, since [8] did not consider obstacles. Since we consider obstacles, we instead compute the values using the method from [14]. Otherwise, our initial feasible solution generation method is identical to BPRC’s.

## I. Caching EFAT and LFDT Values

Lazy BPRC computes EFAT and LFDT several times, possibly with the same arguments. We cache the values for each unique set of arguments to speed up the algorithm.

## VI. THEORETICAL ANALYSIS

Lemma 1. When we return no tours in the pricing problem, (2) is satisfied.

Proof. Referring to values from the first paragraph of Section V-F, strong duality implies

$$
\underline {{c}} (\theta) = \sum_ {i = 1} ^ {n _ {\mathrm{tar}}} \lambda_ {i} + n _ {\mathrm{agt}} \lambda_ {0}\tag{12}
$$

where the RHS is the cost of λ for the dual of the RSMP: this dual is the same as (18)-(21) in [11], but costs are replaced with lower bounds. If we return no tours, $c ^ { * } ( \Gamma ) - c _ { \lambda } ( \Gamma ) \geq 0$ for all tours. This implies λ is feasible for the dual of LP-B (the same dual as (18)-(21) in [11]). The cost of λ for the dual of LP-B is $\sum _ { i = 1 } ^ { n _ { \mathrm { t a r } } } \lambda _ { i } + n _ { \mathrm { a g t } } \lambda _ { 0 }$ , which lower-bounds $c ^ { * } ( B )$ by weak duality. Combining this with (12), we have (2).

## Theorem 1. Lazy BPRC finds an optimal solution.

Proof. Let $\mathcal { F } _ { \mathrm { o p t } }$ be an optimal MT-VRP-O solution, let $c _ { \mathrm { o p t } }$ be its cost, and let $\theta _ { \mathrm { o p t } }$ be the corresponding solution to ILP (1). We show by induction that whenever we execute $\mathrm { A l g }$ 1, Line 5, either $\overline { { c } } _ { \mathrm { i n c } } = c _ { \mathrm { o p t } }$ , or $\theta _ { \mathrm { o p t } }$ is feasible for LP-B for some $\boldsymbol { B }$ on the stack.

Base Case The first node pushed onto the stack is $B = \varnothing .$ and LP-B is a relaxation of ILP (1), so $\theta _ { \mathrm { o p t } }$ is feasible for LP-B.

Induction Hypothesis Suppose on Line 5, either (i) $\bar { c } _ { \mathrm { i n c } } =$ $c _ { \mathrm { o p t } } ,$ or (ii) $\theta _ { \mathrm { o p t } }$ is feasible for LP-B for some B on the stack.

Induction Step Suppose (i) holds. We never increase $\overline { { c } } _ { \mathrm { i n c } } ,$ and $\overline { { c } } _ { \mathrm { i n c } }$ cannot become smaller than $c _ { \mathrm { o p t } }$ by the optimality of $c _ { \mathrm { o p t } }$ , so if Line 5 is ever executed again, (i) will still hold.

Now suppose (ii) holds. If B is not popped at this iteration, (ii) trivially holds at the next iteration. Next, suppose B is popped. Combining Lemma (1) with the feasibility of $\theta _ { \mathrm { o p t } }$ for LP-B, we have $\underline { { c } } ( \theta ) \leq c _ { \mathrm { o p t } }$ . Now we have two cases.

Case 1 Within the lazy evaluation loop, we set $\overline { { c } } _ { \mathrm { i n c } } = c _ { \mathrm { o p t } }$ Then (i) holds when we execute Line 5 next.

Case $\underline { { { 2 } } } \ \bar { c } _ { \mathrm { i n c } } \ \ne \ c _ { \mathrm { o p t } }$ after the lazy evaluation loop. The optimality of $c _ { \mathrm { o p t } }$ then implies that $\overline { { c } } _ { \mathrm { i n c } } ~ > ~ c _ { \mathrm { o p t } }$ . Combining this with $\underline { { c } } ( \theta ) \ \leq \ c _ { \mathrm { o p t } }$ , we have $\underline { { c } } ( \theta ) ~ < ~ \overline { { c } } _ { \mathrm { i n c } } .$ This means the condition on Line 15 fails and we attempt to generate successors for B. No edge traversed by $\mathcal { F } _ { \mathrm { o p t } }$ is in $\begin{array} { r } { B ; { } } \end{array}$ if any edge traversed by $\mathcal { F } _ { \mathrm { o p t } }$ were in B, this would contradict (ii). Thus we have some edge to branch on when generating the successors $B ^ { \prime }$ and $B ^ { \prime \prime }$ . If we branch on an edge not traversed by $\mathcal { F } _ { \mathrm { o p t } } .$ , then $\theta _ { \mathrm { o p t } }$ is feasible for $\mathrm { L P } { \cdot } B ^ { \prime }$ and $\mathrm { L P } { \cdot } B ^ { \prime \prime }$ . If we branch on an edge e traversed by $\mathcal { F } _ { \mathrm { o p t } } , \theta _ { \mathrm { o p t } }$ is feasible for $\mathrm { L P } { \cdot } B ^ { \prime \prime }$ . Thus (ii) holds the next time we execute Line 5.

Thus, the induction hypothesis holds the next time we execute Line 5. Since the number of branch-and-bound nodes expanded in Alg. 1 cannot be larger than the finite number of subsets of ${ \mathcal { E } } _ { \mathrm { t w } } , { \mathrm { A l g } } .$ 1 terminates. Termination only occurs when the stack becomes empty. This means at some point, we check Line 5, and the stack is empty, which means (ii) from the induction hypothesis cannot hold. Thus (i) holds at termination, implying that we found an optimal solution.

## VII. NUMERICAL RESULTS

We ran experiments on an Intel i9-9820X 3.3GHz CPU with 10 cores, hyperthreading disabled, and 128 GB RAM. We compared Lazy BPRC to two ablations. The first ablation, called “Non-Lazy BPRC,” is the same algorithm, but whenever we generate a label l representing a tour Γ, and l is not currently dominated, we set $\vec { g } _ { \mathrm { l b } } [ 1 ] = \vec { g } _ { \mathrm { u b } } [ 1 ] = c ^ { * } ( \Gamma ) ;$ if Γ was unevaluated prior to this step, we evaluate Γ, update $\vec { g } _ { \mathrm { l b } } [ 1 ]$ and $\vec { g } _ { \mathrm { u b } } [ 1 ]$ , then perform dominance checks again. The second ablation, called “No-Affine-Heuristic,” replaces our heuristic in the SPP-GCS associated with tour

![](Bhat2026Optimal_figs/0dfc5520c1f63f455136904262edc2dd0ac9f3408bab5ba43c0bb728ff346cd1.jpg)

![](Bhat2026Optimal_figs/f772a3399c8fe504db8a1bea5c9493e25df67a1a09740c3bbf1942b0a5a2ec27.jpg)

![](Bhat2026Optimal_figs/263d2c4aa0ac029dda69af5aa4fa4dab4a7536cc667ed62980c60bb02f850548.jpg)  
Fig. 3. (a) Varying the number of targets. Lazy BPRC shows smaller median runtime than the ablations, particularly for larger numbers of targets. (b) Varying the map resolution. Lazy BPRC’s advantage in median runtime grows as we increase the map resolution. (c) Varying the capacity. Lazy BPRC has smaller median runtime than the ablations for all tested capacities.

Γ in Section V-G with the heuristic from FMC\*. That ${ \mathrm { i s } } ,$ when computing the f-value trajectory for a GCS-path $P ^ { \prime }$ the obstacle-unaware portion of the trajectory is required to intercept all target-windows in Γ unvisited by $P ^ { \prime }$ , in sequence. Each algorithm parallelized successor generation in pricing and tour cost evaluation, the initial computation of pairwise distances between segments and segment-starts, and initial pairwise LFDT computations.

We generated problem instances by modifying the instance generation method from [14] to handle multiple agents. In every instance, each target had two time windows, demand 1, and speed within each time window generated uniformly at random between 0.5 and 1 m/s. Each instance had three agents with $v _ { \mathrm { m a x } } = 4 ~ \mathrm { m / s }$ . Our obstacle maps were square grids, but the agents and targets move in continuous space in the grids. We define the map resolution as the width of the obstacle map in grid cells. In our experiments, we varied the number of targets, map resolution, and capacity. We set the computation time limit to 10 min, per planner, per instance.

## A. Experiment 1: Varying the Number of Targets

We fixed the map resolution to 30 and varied $n _ { \mathrm { t a r } }$ from 3 to 15, setting the capacity $d _ { \mathrm { m a x } } = n _ { \mathrm { t a r } } / n _ { \mathrm { a g t } }$ . Fig. 3 (a) shows the results. As $n _ { \mathrm { t a r } }$ increases, Lazy BPRC notably outperforms Non-Lazy BPRC in min, median, and max runtime, demonstrating that deferring the computation of tour costs is effective. Lazy BPRC also demonstrates smaller median and max runtimes than No-Affine-Heuristic, showing that our obstacle-aware heuristic leveraging continuity relaxation outperforms a heuristic that ignores obstacles.

## B. Experiment 2: Varying the Map Resolution

We fixed $n _ { \mathrm { t a r } }$ to 12 and $d _ { \mathrm { m a x } }$ to 4, then varied the map resolution from 10 to 30. Fig. 3 (b) shows the results.

Lazy BPRC again demonstrates smaller median and max runtime than both ablations, and also smaller min runtime than Non-Lazy BPRC. Lazy BPRC’s advantage grows with the map resolution because as we increase map resolution, the numbers of nodes and edges in the GCS tend to increase, making the GCS more expensive to search. Lazy BPRC outperforms Non-Lazy BPRC because it reduces the number of SPP-GCS queries, and Lazy BPRC outperforms No-Affine-Heuristic by speeding up each SPP-GCS query.

## C. Experiment 3: Varying the Capacity

We fixed $n _ { \mathrm { t a r } }$ to 9 and the map resolution to 30, then varied the capacity $d _ { \mathrm { m a x } }$ from 3 to 7. Fig. 3 (c) shows the results. Lazy BPRC shows smaller median runtime than both ablations, and also smaller min runtime than Non-Lazy BPRC. Lazy BPRC’s max runtime hits the time limit for $d _ { \operatorname* { m a x } } \geq 4$

Note that No-Affine-Heuristic’s median runtime counterintuitively drops when we increase $d _ { \mathrm { m a x } }$ from 6 to 7. This occurs because in two instances, runtime became more than 2 times smaller when we increased $d _ { \operatorname* { m a x } } ;$ runtime did not change as significantly in the other 8 instances. The runtime dropped in these two instances for No-Affine-Heuristic because there were one or more tours whose evaluation required significant runtime for $d _ { \operatorname* { m a x } } = 6$ , but simply never needed to be evaluated for $d _ { \operatorname* { m a x } } = 7$

## VIII. CONCLUSIONS

In this paper, we introduced Lazy BPRC, a new algorithm to find optimal solutions for the MT-VRP-O, and we demonstrated its benefits via ablation studies. One direction for future work is to pursue bounded-suboptimal solutions to enable scaling to more targets.

## REFERENCES

[1] C. S. Helvig, G. Robins, and A. Zelikovsky, “The moving-target traveling salesman problem,” Journal of Algorithms, vol. 49, no. 1, pp. 153–174, 2003.

[2] C. D. Smith, Assessment of genetic algorithm based assignment strategies for unmanned systems using the multiple traveling salesman problem with moving targets. University of Missouri-Kansas City, 2021.

[3] A. Stieber and A. Fugenschuh, “Dealing with time in the multiple¨ traveling salespersons problem with moving targets,” Central European Journal of Operations Research, vol. 30, no. 3, pp. 991–1017, 2022.

[4] J.-M. Bourjolly, O. Gurtuna, and A. Lyngvi, “On-orbit servicing: a time-dependent, moving-target traveling salesman problem,” International Transactions in Operational Research, vol. 13, no. 5, pp. 461– 481, 2006.

[5] B. Li, B. R. Page, J. Hoffman, B. Moridian, and N. Mahmoudian, “Rendezvous planning for multiple auvs with mobile charging stations in dynamic currents,” IEEE Robotics and Automation Letters, vol. 4, no. 2, pp. 1653–1660, 2019.

[6] P. Toth and D. Vigo, Vehicle routing: problems, methods, and applications. SIAM, 2014.

[7] C. Archetti, L. Coelho, M. Speranza, and P. Vansteenwegen, “Beyond fifty years of vehicle routing: Insights into the history and the future,” European Journal of Operational Research, 2025.

[8] A. Bhat, G. Gutow, Z. Ren, S. Rathinam, and H. Choset, “Optimal solutions for the moving target vehicle routing problem via branch-and-price with relaxed continuity,” 2026. [Online]. Available: https://arxiv.org/abs/2603.00663

[9] M. Hammar and B. J. Nilsson, “Approximation results for kinetic variants of tsp,” in Automata, Languages and Programming: 26th International Colloquium, ICALP’99 Prague, Czech Republic, July 11–15, 1999 Proceedings 26. Springer, 1999, pp. 392–401.

[10] L. Costa, C. Contardo, and G. Desaulniers, “Exact branch-price-andcut algorithms for vehicle routing,” Transportation Science, vol. 53, no. 4, pp. 946–985, 2019.

[11] D. Feillet, “A tutorial on column generation and branch-and-price for vehicle routing problems,” 4or, vol. 8, no. 4, pp. 407–424, 2010.

[12] T. Marcucci, J. Umenberger, P. Parrilo, and R. Tedrake, “Shortest paths in graphs of convex sets,” SIAM Journal on Optimization, vol. 34, no. 1, pp. 507–532, 2024.

[13] A. Bhat, G. Gutow, B. Vundurthy, Z. Ren, S. Rathinam, and H. Choset, “A complete and bounded-suboptimal algorithm for a moving target traveling salesman problem with obstacles in 3d\*,” in 2025 IEEE International Conference on Robotics and Automation (ICRA), 2025, pp. 6132–6138.

[14] ——, “A complete algorithm for a moving target traveling salesman problem with obstacles,” in International Workshop on the Algorithmic Foundations of Robotics. Springer, 2024.

[15] G. Ozbaygin, O. E. Karasan, M. Savelsbergh, and H. Yaman, “A branch-and-price algorithm for the vehicle routing problem with roaming delivery locations,” Transportation Research Part B: Methodological, vol. 100, pp. 115–137, 2017.

[16] T. Asano, T. Asano, and H. Imai, “Shortest path between two simple polygons,” Information processing letters, vol. 24, no. 5, pp. 285–288, 1987.

[17] M. Cui, D. D. Harabor, and A. Grastien, “Compromise-free pathfinding on a navigation mesh.” in IJCAI, 2017, pp. 496–502.