---
citation_key: Neville2022DITAGS
arxiv_id: 2209.13092
arxiv_url: "https://arxiv.org/abs/2209.13092"
title: "D-ITAGS: A Dynamic Interleaved Approach to Resilient Task Allocation, Scheduling, and Motion Planning"
authors_short: "Glen Neville et al."
year: 2022
direction_tag: E_bounded_suboptimal_search
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:37:27Z
origin: ai+web
reviewed: false
---

# D-ITAGS: A Dynamic Interleaved Approach to Resilient Task Allocation, Scheduling, and Motion Planning

Glen Neville, Sonia Chernova, Harish Ravichandar

Abstract—Complex, multi-task missions require the coordination of heterogeneous robots at multiple inter-connected levels, such as coalition formation, scheduling, and motion planning. This challenge is exacerbated by dynamic changes, such as sensor and actuator failures, communication loss, and unexpected delays. We introduce Dynamic Iterative Task Allocation Graph Search (D-ITAGS) to simultaneously address coalition formation, scheduling, and motion planning in dynamic settings involving heterogeneous teams. D-ITAGS achieves resilience via two key characteristics: i) interleaved execution, and ii) targeted repair. Interleaved execution enables an effective search for solutions at each layer while avoiding incompatibility with other layers. Targeted repair identi<sup></sup>es and repairs parts of the existing solution impacted by a given disruption, while conserving the rest. In addition to algorithmic contributions, we derive accurate bounds on schedule suboptimality and provide insights into the inherent trade-off between time and resource optimality in these settings. Our experiments reveal that i) D-ITAGS is signi<sup></sup>cantly faster than recomputation from scratch in dynamic settings, with little to no loss in solution quality, and ii) the theoretical bounds on optimality gap consistently hold in practice.

## I. INTRODUCTION

Heterogeneous multi-robot systems (MRS) bring together robots with complementary capabilities. They have been proved useful in domains as diverse as agriculture [1], assembly [2], and warehouse automation [3]. To achieve effective teaming in such complex domains, researchers have addressed challenging problems in coalition formation (who) [4], scheduling (when) [5], multi-robot motion planning (how) [3], and the combination of all these problems [6], [7].

Many algorithms developed for heterogeneous MRS coordination assume a static problem domain – one in which speci<sup></sup>cations and resources remain constant. However, realworld MRS do not enjoy the luxury of a predictable world, much less an unchanging one. Sensor and actuator failures, communication loss, and unexpected delays are all but a few examples. These events, even at the individual robot level, could cascade into catastrophic system-wide failures [8]. Note that robust task allocation methods [9], [10], while capable of effectively handling various forms of uncertainty, do not consider abrupt dynamic changes to the problem domain.

An obvious way to handle dynamic problems is to recompute the solution when unexpected events occur. However, as we demonstrate, this na¨<sup>ı</sup>ve approach is inef<sup></sup>cient. Ef<sup></sup>cient approaches have been developed within the contexts of homogeneous robots [8], single-robot or decomposable tasks [11], and instantaneous task allocation [12]. However, we still lack approaches that can simultaneously handle task allocation, scheduling, and motion planning in dynamic settings involving multi-robot tasks and heterogeneous teams.

This work introduces the Dynamic Trait-Based Time Extended Task Allocation problem. Our formulation can be seen as an instance of the well-known ST-MR-TA problem [13], with additional constraints to account for motion planning and dynamic changes. Speci<sup></sup>cally, we consider a variety of changes to the environment or the team (e.g., robot failures, task delays, etc.) that are unknown until after the fact.

To address the above, we develop Dynamic Incremental Task Allocation Graph Search (D-ITAGS), an ef<sup></sup>cient algorithm to solve dynamic problems (see Fig. 1 for the architecture). D-ITAGS provides resilience against dynamic events due to two important characteristics: i) interleaved executions of individual modules, and ii) targeted repair of existing solutions.

First, leveraging our recent work [7], [14] which interleaves the execution of task allocation, scheduling, and motion planning, D-ITAGS effectively searches for solutions at each layer while ensuring compatibility with those at downstream layers. For instance, D-ITAGS will only consider allocations that do not violate scheduling constraints, and schedules with realizable motion plans. Indeed, we recently demonstrated that this interleaved approach is signi<sup></sup>cantly more ef<sup></sup>cient than the often-used sequential approach [7], [14]. Compared to our prior methods, D-ITAGS includes a more ef<sup></sup>cient scheduler, and accounts for travel times to more tightly integrate scheduling and motion planning (see Sec. VII-A).

Second, we leverage the insight that many events do not render all computations performed for the existing solution invalid. For instance, when a robot is damaged, only allocations involving the damaged robot and the ones downstream are impacted. We develop a targeted repair mechanism that i) identi<sup></sup>es and conserves parts of the solution that remain valid after an event, and ii) only recomputes parts that are now stale. Our approach can handle changes to i) robot capabilities, ii) task requirements, and iii) task duration, covering a wide spectrum of unexpected events. We demonstrate that targeted repair signi<sup></sup>cantly decreases computation time compared to recomputing solutions from scratch, with little to no loss in solution quality (see Sec. VII-B).

In addition to the above computational and empirical bene<sup></sup>ts, we contribute theoretical insights into the operation of D-ITAGS. Speci<sup></sup>cally, we demonstrate that trait-based timeextended task allocation can be viewed as an inherent tradeoff between time optimality (shortest makespan) and resource optimality (fewest allocations), and that one could traverse this trade-off spectrum by altering a single hyperparameter in our search heuristic. Leveraging this insight, we derive bounds on D-ITAGS’ sub-optimality in terms of makespan under mild assumptions. These bounds provide guarantees on solution quality, and guide users in choosing hyperparameters. We also demonstrate that these bounds consistently hold in practice.

In summary, we contribute i) a formal de<sup></sup>nition of the dynamic trait-based time-extended task allocation problem, ii)

![](Neville2022DITAGS_figs/c3b5028e09664361a406613ce6f7a54a7f861d35e984fa372d5ec42f12ecd027.jpg)  
Figure 1: The proposed D-ITAGS algorithm leverages targeted repair and interleaved execution to simultaneously address coalition formation, scheduling, and motion planning in dynamic settings involving heterogeneous teams.

a resilient and ef<sup></sup>cient algorithm to handle dynamic changes, iii) theoretical insights into the inherent trade-off between time and resource optimality, and iv) performance guarantees.

## II. RELATED WORK

ST-MR-TA methods: While the multi-robot task allocation problem has many variants [13], [15], we limit our focus to single-task (ST) robots, multi-robot (MR) tasks, and timeextended (TA) allocation, as it closely relates to our work. ST-MR-TA problems require assigning coalitions of agents to tasks under temporal constraints. These constraints can take many forms, including precedence and ordering constraints, spatio-temporal constraints (e.g., travel time), and deadlines.

Auction-based methods to solve ST-MR-TA problems involve auctioning tasks to robots through a bidding process based on a utility function that combines the robot’s (or the coalition’s) ability to perform the task with any temporal constraints [16], [17]. Auctions have been shown to be highly effective, but typically either i) require multi-robot tasks to be decomposable into sub-tasks, each solvable by a single robot, or ii) assume that the ideal distribution of agents for each task is known (e.g., Task 1 requires one ground and one aerial robot). Optimization-based methods form another class of solutions that formulate the ST-MR-TA problem as a mixed-integer linear program (MILP) to optimize the overall makespan or a utility function [18]. However, these methods assume that some tasks can be left uncompleted [19] or require that all tasks be decomposable into single-agent tasks [20]. In contrast to auction-based and optimization-based approaches, our approach does not require task decompatibility and ensures the completion of all tasks.

Our approach to task allocation is most closely related to trait-based methods [4], [6], [14], [21], [22], which utilize a <sup></sup>exible modeling framework that encodes task requirements in terms of traits $( \mathrm { e . g . }$ ., Task 1 involves traveling at 10m/s while carrying a 50-lb payload). Each task is not limited to a speci<sup></sup>c set or number of agents. Instead, the focus is on <sup></sup>nding a coalition of agents that collectively possess the required capabilities. However, most existing trait-based approaches are limited to ST-MR-IA problems that do not require scheduling [4], [14], [21], [22], with one notable exception [6]. Further, none of them can handle dynamic problems involving changes to the domain.

Dynamic Task Allocation: The approaches discussed above deal with static domains in which all aspects of the problem are known a priori and remain constant. Researchers have studied dynamic task allocation problems that consider unexpected events that occur during execution [23]. Similar to static problems, solutions to dynamic problems include game-theoretic methods [24], auction-based methods [11], and optimization methods [25]. However, these approaches do not solve the ST-MR-TA variant of task allocation. Further, existing approaches to dynamic problems inherit the limitations of their underlying methodology, and i) are limited to single-robot (SR) tasks [11], [23], ii) rely on decomposable tasks [20], iii) require speci<sup></sup>cation of ideal agent distribution [23], or iv) entirely ignore scheduling and motion planning [12]. Complementary to approaches that explicitly consider dynamic events, robust task allocation methods [9], [10] attempt to <sup></sup>nd allocations that are robust to uncertainty and more likely to be valid even when information about the environment is uncertain. However, robust approaches require pre-speci<sup></sup>ed models of uncertainty. In contrast, D-ITAGS leverages trait-based modeling and provides an ef<sup></sup>cient approach to handle unexpected changes in ST-MR-TA problems with heterogeneous robots.

## III. PROBLEM DESCRIPTION

We begin by formalizing the problem of dynamic trait-based time-extended task allocation with spatial constraints. We <sup></sup>rst present the static variant, which closely aligns with prior work [4], [6], [22], [26], and then introduce the dynamic variant.

Consider a team of N heterogeneous robots, with the ith robot’s capabilities described by a collection of traits $q ^ { ( i ) } =$ $\left\lceil q _ { 1 } ^ { ( i ) } , \ q _ { 2 } ^ { ( i ) } , \ \cdots \ , q _ { U } ^ { ( i ) } \right\rceil$ , where $q _ { u } ^ { ( i ) } \in \mathbb { R } _ { \geq 0 }$ corresponds to the $u ^ { t h }$ trait for the $i ^ { t h }$ robot. We assign $q _ { u } ^ { ( i ) } = 0$ when the $i ^ { t h }$ robot does not possess the $u ^ { t h }$ trait $( \mathrm { e . g }$ . <sup></sup>retrucks have a water capacity, but other robots may not). As such, the capabilities of the team can be de<sup></sup>ned by a team trait matrix:

$$
\boldsymbol {Q} = \left[ q ^ {(1) ^ {\intercal}}, \dots , q ^ {(N) ^ {\intercal}} \right] ^ {\intercal} \in \mathbb {R} _ {+} ^ {N \times U}
$$

where $Q _ { i u }$ corresponds to the ith robot and uth trait.

We model the set of M tasks that need to be completed as a Task Network $\tau { : }$ a directed graph $G = ( \mathcal { E } , \mathcal { V } )$ , with vertices V representing a set of tasks $\{ a _ { m } \} _ { m = 1 } ^ { M }$ , and edges $\mathcal { E }$ represent relationships between any two tasks $a _ { i }$ and $a _ { j }$ , such as a precedence constraint $( a _ { i } \prec a _ { j } )$ requiring that Task $a _ { i }$ be completed before the Task $a _ { j }$ can begin (e.g., a <sup></sup>re must be put out before repairs can begin) and a mutex constraint $( a _ { i } \neq a _ { j } )$ ensuring that $a _ { i }$ and $a _ { j }$ do not occur simultaneously (e.g. a robot cannot pick up two objects simultaneously). The team is required to complete all tasks, and robots can complete tasks individually or collaborate as a coalition, depending on the available resources.

Let the traits required to complete the mth task be denoted by $y ^ { ( m ) } = \left\lceil y _ { 1 } ^ { ( m ) } , \dot { y } _ { 2 } ^ { ( m ) } , \cdot \cdot \cdot , y _ { U } ^ { ( \hat { m } ) } \right\rceil$ , where $y _ { u } ^ { ( m ) } \in \mathbb { R } _ { \ge 0 }$ is the amount of $\hat u ^ { \hat t h }$ trait required for Task m. If the $u ^ { t h }$ trait is not required by the $m ^ { t h }$ task, we set $y _ { u } ^ { ( m ) } = 0 .$ . We can thus model the requirements of all tasks using the desired trait matrix:

$$
\boldsymbol {Y} ^ {*} = \left[ y ^ {(1) ^ {\intercal}}, \dots , y ^ {(N) ^ {\intercal}} \right] ^ {\intercal} \in \mathbb {R} _ {+} ^ {M \times U}
$$

where $Y ^ { * } { _ m u }$ corresponds to the mth task and uth trait.

To execute Task $a _ { m } ,$ , a robot (or a coalition) requires a collision-free paths from its current con<sup></sup>guration to the task’s initial con<sup></sup>guration $\mathcal { C } _ { I } ^ { m }$ , as well as from $\mathcal { C } _ { I } ^ { m }$ to the task’s <sup></sup>nal terminal con<sup></sup>guration $\mathcal { C } _ { T } ^ { m }$ (e.g., in a transport task, a robot needs collision-free paths to the package, as well as from the pickup to the dropoff). To compute such paths, a world model W is provided which describes all of the static geometric information about the environment, including obstacles.

With the above de<sup></sup>nitions, we can de<sup></sup>ne the problem domain using the tuple $\pmb { \mathcal { D } } \ = \ \langle \pmb { \mathcal { T } } , \ \pmb { Q } , \ \pmb { Y ^ { * } } , \ I _ { c } , \ L _ { T } , \ W \rangle$ where $\tau$ is the task network, Q is the team trait matrix, $Y ^ { * }$ is the desired trait matrix, $I _ { c }$ and $L _ { T }$ are respectively the sets of all initial and terminal con<sup></sup>gurations associated with tasks and $W$ is a description of the world state. Note that non-spatial tasks can be modeled by setting their initial and terminal con<sup></sup>gurations to be equal.

A solution to the problem speci<sup></sup>ed by <sup>D</sup> consists of three components: i) an allocation of robots to tasks, ii) a task schedule, and iii) a set of associated motion plans.

We denote the allocation of robots to tasks using the allocation matrix $\mathbf { A } \in { \pmb { A } }$ as follows

$$
\mathbf {A} = \left[ \begin{array}{c c c} o _ {1, 1} & \dots & o _ {1, n} \\ \vdots & \ddots & \vdots \\ o _ {m, 1} & \dots & o _ {m, n} \end{array} \right]
$$

where $o _ { n , m } ~ = ~ 1 ~ \mathrm { i f } ~ n ^ { t h }$ robot is assigned to the $m ^ { t h }$ task. An allocation is considered valid when the aggregated traits of each coalition satisfy the trait requirements of the task to which it is assigned [4]. Formally, A is a valid allocation if and only if AQ is element-wise greater than or equal to $Y _ { \pi } ^ { * }$ We denote the set of all valid by $\mathcal { N } _ { s o l }$

Formally, we de<sup></sup>ne the solution to the problem de<sup></sup>ned by <sup>D</sup> using the tuple $S = \langle \mathbf { A } , \mathbf { \nabla } X , \mathbf { \nabla } \sigma \rangle$ where A is a valid allocation, X is a <sup></sup>nite set of collision-free motion plans, and <sup>σ</sup> is a schedule, represented by the set of start times for all tasks $\{ s _ { i } \} _ { i = 1 } ^ { M }$ , that respects all temporal constraints.

Note that the problem formulation from above assumes that all elements of the problem (e.g., tasks, requirements, robots, and world model) are static. As such, any valid solution $_ { s }$ to the problem de<sup></sup>ned in <sup>D</sup> would be rendered invalid when an unexpected change occurs (e.g., robot failures and introduction of new tasks). To capture dynamic environments with unforeseen changes, we de<sup></sup>ne a new class of problems we call Dynamic Trait-Based Time Extended Task Allocation.

Formally, we model the dynamic problem domain as

$$
\boldsymbol {\mathcal {D}} _ {k} = \left\langle \boldsymbol {\mathcal {T}} _ {k}, \boldsymbol {Q} _ {k}, \boldsymbol {Y} _ {k} ^ {*}, I _ {c k}, L _ {\mathcal {T} k}, W _ {k} \right\rangle ,
$$

where the subscript k is used to denote the fact each domain de<sup></sup>nition is only valid for Iteration k until an unexpected change rede<sup></sup>nes the problem domain to $\scriptstyle \mathcal { D } _ { k + 1 }$ . Similarly, we denote a solution to the current problem de<sup></sup>nition using $S _ { k } = \langle \mathbf { A } _ { k } , ~ X _ { k } , ~ \sigma _ { k } \rangle$ where $\mathbf { A } _ { k }$ is a valid allocation, $X _ { k }$ is a <sup></sup>nite set of motion plans, and $\sigma _ { k }$ is a schedule for all tasks.

As we solve the dynamic trait-based time-extended task allocation problem, we are interested in two objectives: i) time efciency: measured by the makespan $C ( \sigma )$ of the Schedule σ, and ii) resource sufciency: when aggregated traits $\mathbf { A } Q$ are element-wise greater than or equal to the requirements $Y ^ { * }$

Problem statement: Given any new problem de<sup></sup>nition speci<sup></sup>ed by $\scriptstyle { \mathcal { D } } _ { k }$ , compute the solution $S _ { k }$ by optimizing for time ef<sup></sup>ciency while ensuring resource suf<sup></sup>ciency.

## IV. OVERVIEW OF APPROACH

To solve the dynamic trait-based time-extended task allocation problems with spatial constraints, as de<sup></sup>ned in Section III, we introduce our Dynamic Incremental Task Allocation Graph Search (D-ITAGS) algorithm. Though several approaches have been proposed for instantaneous trait-based task assignment [4], [21], [22], we are aware of only one approach – ITAGS [6] – that addresses the time-extended trait-based task allocation problem. Since D-ITAGS can be seen as a direct extension of ITAGS, we begin with a high-level summary of the similarities and differences, and provide details in Section V.

D-ITAGS shares two fundamental properties with ITAGS. First, D-ITAGS adopts a three-layer nested architecture from ITAGS, in which the processes of Task Allocation, Scheduling, and Motion Planning are interleaved. Second, D-ITAGS and ITAGS compute solutions incrementally by performing graphbased searches while leveraging heuristics.

D-ITAGS differs from and improves upon ITAGS in several ways. First, D-ITAGS constructs schedules by solving mixedinteger linear programs (MILPs) using GUROBI’s branch-andcut (B&C) solver, while ITAGS employs TABU search (TS). Note that the B&C solver we use can encode more temporal constraints and, unlike TS, provide bounds on suboptimality. While TS can produce schedules of comparable makespan, our experiments reveal that D-ITAGS is more ef<sup></sup>cient than ITAGS. Second, unlike ITAGS, D-ITAGS accounts for travel times between tasks while optimizing schedules by ef<sup></sup>ciently querying the motion planner for estimates. We demonstrate that these two differences signi<sup></sup>cantly improve computational ef<sup></sup>ciency without sacri<sup></sup>cing solution quality (see Section VII). Note that these improvements persist even when solving static time-extended trait-based task allocation.

The most signi<sup></sup>cant difference is that D-ITAGS employs a targeted repair module when dynamic and unexpected changes render the existing solution invalid. In contrast, ITAGS was not designed to handle such unexpected events and thus would have to resort to recomputing a new solution from scratch.

## V. D-ITAGS

In this section, we discuss each module within D-ITAGS.

## A. Task Allocation

The task allocation layer of D-ITAGS uses a greedy best-<sup></sup>rst search through the task allocation space, <sup>A</sup>. The task allocation space is modeled as a directed graph in which

Node N denotes the allocation $\mathbf { A } _ { N }$ . The directed edge from a parent node $N _ { p }$ to a child node N represents the incremental allocation of a single robot to a particular task, with the root node containing no allocations. As such, all possible allocations exist within the full graph. Further, each node N also contains a schedule $\sigma _ { N }$ associated with its allocation ${ \bf A } _ { N }$ This graphical representation allows us to start from a node with no assignments and incrementally assign robots until we satisfy the trait requirements of all tasks.

Similar to ITAGS [6], we consider two heuristics to search the task allocation graph: i) APR: Allocation Percentage $R e \mathrm { - }$ maining guides the search based on allocation quality, and ii) NSQ: Normalized Schedule Quality guides the search based on schedule quality. To balance the bene<sup></sup>ts of both heuristics, we use their convex combination, which we call TETAQ: Time-Extended Task Allocation Quality.

APR computes the percentage trait mismatch error as below

$$
f _ {a p r} (\bar {N}) = \frac {| | \max (E (\mathbf {A} _ {\bar {N}}) , 0) | | _ {1 , 1}}{| | Y ^ {*} | | _ {1 , 1}}\tag{1}
$$

where $\bar { N }$ is the node being evaluated and ${ \bf A } _ { \bar { N } }$ is its allocation, and $| | \cdot | | _ { 1 , 1 }$ is the element-wise $l _ { 1 }$ norm. The trait mismatch error $E ( \mathbf { A } _ { \bar { N } } )$ is de<sup></sup>ned as $E ( { \bf A } _ { \bar { N } } ) \triangleq Y ^ { * } { - } ( { \bf A } _ { \bar { N } } Q )$ , where ${ \bf A } _ { \bar { N } } \ : Q$ denotes the resources aggregated at each of the tasks given the allocation ${ \bf A } _ { \bar { N } }$ . Note that any element of max $( E ( \mathbf { A } _ { \bar { N } } )$ , 0) will be zero if aggregated traits surpass the required traits of the corresponding task. As such, $f _ { a p r } \in [ 0 , 1 ]$ quanti<sup></sup>es the degree to which a given allocation meets the requirements.

NSQ measures the relative reduction in makespan as below

$$
f _ {n s q} (\bar {N}) = \frac {C (\sigma_ {\bar {N}}) - C (\sigma_ {L B})}{C (\sigma_ {U B}) - C (\sigma_ {L B})}\tag{2}
$$

where $C ( \cdot )$ returns the makespan of a given schedule, $\sigma _ { \bar { N } }$ is the schedule associated with the node N<sup>¯</sup> being evaluated, $\sigma _ { L B }$ is the estimated shortest schedule constructed by ignoring any constraints from allocation and motion planning, and $\sigma _ { U B }$ is the longest schedule constructed by total ordering with the longest possible motion plans. While any upper bound on path length can be used, we use the sum of all edges in the task network $\tau$ in our experiments. As such, $f _ { n s q } \in [ 0 , 1 ]$ quanti<sup></sup>es the relative length of the schedule being evaluated.

TETAQ is a convex combination of APR and NSQ as below

$$
f _ {t e t a q} (\bar {N}) = \alpha f _ {a p r} (\bar {N}) + (1 - \alpha) f _ {n s q} (\bar {N})\tag{3}
$$

where $\alpha \in [ 0 , 1 ]$ is a user-speci<sup></sup>ed parameter that controls the relative weighting of NSQ and APR heuristic.

## B. Scheduling and Motion Planning

D-ITAGS’ scheduling layer checks the feasibility of scheduling a particular assignment and helps compute NSQ. We consider three different temporal constraints: precedence constraints, mutex constraints, and travel time constraints. Precedence constraints P ensure that one task happens before another (e.g., <sup></sup>re must be doused before repairs). Mutex constraints M ensure that two tasks do not happen simultaneously (e.g. a robot cannot pick up two objects simultaneously). Travel time constraints ensure that robots have suf<sup></sup>cient time to travel between task sites (e.g., traveling to the location of <sup></sup>re before dousing). We formulate and solve the mixed-integer linear program as:

$$
\begin{array}{l} \min _ {\{s _ {i} \} _ {i = 1} ^ {M}} C \\ \text {s.t.} C \geq s _ {i} + d _ {i}, \forall i = 1,.., M \\ s _ {j} \geq s _ {i} + d _ {i} + x _ {i j}, \forall (i, j) \in \mathcal {P} \\ s _ {i} \geq x _ {i}, \forall i = 1,.., M \\ s _ {j} \geq s _ {i} + d _ {i} + x _ {i j} - M (1 - p _ {i j}) \quad \forall (i, j) \in \mathcal {M} ^ {R} \\ s _ {i} \geq s _ {j} + d _ {j} + x _ {j i} - M p _ {i j} \quad \forall (i, j) \in \mathcal {M} ^ {R} \end{array}\tag{4}
$$

where C is the makespan, $s _ { i }$ and $d _ { i }$ are the start time and duration of Task $a _ { i } , x _ { i j }$ is the time required to transition from $a _ { i }$ to $a _ { j } , p _ { i j } = 1$ iff $a _ { i }$ precedes $a _ { j } , \beta \in \mathbb { R } _ { + }$ is a large scalar, $\mathcal { P }$ and M are sets of integer pairs containing the lists of precedence and mutex constraints, with $\mathcal { M } ^ { R } = \mathcal { M } - \mathcal { P } \cap \mathcal { M }$ denoting mutex constraints with precedence constraints removed.

D-ITAGS constructs an initial schedule by estimating travel times based on the Euclidean distance between travel sites. As the search proceeds, the scheduling layer iteratively queries the motion planner to account for and accurately estimate travel times, until all motion plans required by the schedule are instantiated. Note that while our implementation uses the probabilistic roadmap planner [27], D-ITAGS is agnostic to the choice of motion planner.

D-ITAGS includes careful design choices that reduce the burden of motion planning placed on the scheduler. First, D-ITAGS memoizes all motion plans for future use. Second, it shares motion plans across robots with identical capabilities since their travel times between any two locations are likely similar. Further, our prior work has demonstrated that the interleaved approach adopted by D-ITAGS can handle signi<sup></sup>cantly more tasks and robots than other existing approaches [6], [7].

In addition to constructing a valid schedule, the scheduling layer is also responsible for computing the bounds $\sigma _ { U B }$ and $\sigma _ { L B }$ used in the NSQ heuristic. For estimating the upper bound, we compute the worst-case makespan as follows

$$
C (\sigma_ {U B}) = \frac {2 M z}{w} + \sum_ {m = 1} ^ {M} d _ {m}\tag{5}
$$

where $z$ is the length of the longest possible path (e.g., the sum of all edges in the probabilistic roadmap) in $W$ , and w is the speed of the slowest robot. We set lower bound to be equal to the duration of the longest task: $C ( \sigma _ { L B } ) = \operatorname* { m a x } _ { m } d _ { m }$

## C. Targeted Repair

When an unexpected event renders the current solution invalid, D-ITAGS ef<sup></sup>ciently recomputes a solution via targeted repair of the task allocation graph. D-ITAGS can speci<sup></sup>cally handle three categories of unexpected changes: i) changes in robots’ capabilities, ii) changes in task requirements, iii) changes in task duration. Note that these three classes of changes encompass a wide variety of events, such as loss or reinforcement of robots, unexpected additional tasks, partial loss of robot capabilities, and unforeseen delays due to environmental conditions. Our only assumption is that any of the above speci<sup></sup>ed events can be detected and identi<sup></sup>ed using other techniques (e.g., [12]). In Section VII, we demonstrate D-ITAGS’ ability to handle eight distinct event types.

To enable ef<sup></sup>cient repair, D-ITAGS leverages the inherent structure of the task allocation graph to identify and repair only a subset of the nodes. For example, when a robot’s sensor is damaged or lost, D-ITAGS will identify nodes in the graph that allocated the damaged robot and recompute their APR, ignoring other nodes that will not contribute to a new solution.

D-ITAGS makes changes to three types of nodes: i) open set: collection of unexpanded nodes, ii) the closed set: collection of expanded nodes, and the iii) pruned set: collection of nodes deemed infeasible. We provide a detailed <sup></sup>owchart describing D-ITAGS’ targeted repair mechanism in Fig. 2. D-ITAGS begins by adding the (now invalid) existing solution to the open set. Then, it incrementally checks for <sup></sup>ve speci<sup></sup>c changes and makes modi<sup></sup>cations as described below:

• Agent or Task Loss: When an agent or a task is lost, D-ITAGS removes nodes that utilize the lost agent or those that involve the lost task. When a task is lost in particular, D-ITAGS checks to <sup></sup>nd nodes in the open and closed set that might satisfy the requirements $( A P R = 0 )$ after the task loss, and then continues the search with only the newly-identi<sup></sup>ed solutions.

• Reduced Traits or Increased Requirements: When agent capabilities decrease or task requirements increase, the nodes in the closed and pruned sets remain infeasible $( A P R < 0 )$ . As such, D-ITAGS ignores them and only updates the APR of the nodes in the open set.

• Increased Traits or Reduced Requirements: When agent capabilities increase or task requirements decrease, D-ITAGS updates the APR of the nodes in the open set and checks if any of nodes in the closed and pruned sets have now become viable $( A P R = 0 )$ after the increase (decrease) in capabilities (requirements).

• Changed Duration: When task duration or travel times change, APR remains unchanged. As such, D-ITAGS updates the NSQ of the nodes in the open set and ignores all other nodes as they remain infeasible $( A P R < 0 )$

• New Agent: When a new agent becomes available, D-ITAGS adds a new node as a child of the root node, and in turn appends the open set.

Leveraging the above insights, D-ITAGS avoids unnecessary recomputations when responding to dynamic events.

## VI. THEORETICAL ANALYSES

To better understand D-ITAGS’ performance, we analyze the effect of α – the user-speci<sup></sup>ed parameter that determines the relative importance of our two heuristics – on the optimality of the obtained solution. We consider two notions of optimality: i) time optimality (shortest makespan), and resource optimality (fewest assignments). We demonstrate that the choice of α determines the trade-off between the two notions of optimality, with each extreme value, $\alpha = 0$ or $\alpha = 1$ , respectively guaranteeing time or resource optimality.

A. Analysis of Time Optimality

We derive strict bounds on the time optimality gap of solutions generated by D-ITAGS as measured by makespan.

Theorem 1. For a given trait-based time-extended task assignment problem, let $C ( \sigma ^ { * } )$ be the optimal makespan and $C ( \hat { \sigma } )$ be the makespan of the solution generated by D-ITAGS. $I f \alpha < 0 . 5$ in Eq. (3), then

$$
C (\hat {\sigma}) - C (\sigma^ {*}) \leq \frac {\alpha}{1 - \alpha} (C (\sigma_ {U B}) - C (\sigma_ {L B}))\tag{6}
$$

where $C ( \sigma _ { L B } )$ and $C ( \sigma _ { U B } )$ are estimated lower and upper bounds, respectively, on the makespan of any valid solution.

Proof. Since any expansion of a parent node represents the addition of an assignment, any given node N is guaranteed to have more agents assigned than its parent $N _ { p }$ . This observation, when combined with the fact that adding assignments can never reduce the makespan (as adding assignments can only introduce new constraints to the MILP), yields

$$
f _ {n s q} (N) \geq f _ {n s q} (N _ {p})\tag{7}
$$

Consequently, we can infer that the NSQ value of all nodes in the unopened set $\mathcal { U } \subseteq \mathcal { N }$ of a D-ITAGS graph is lower bounded by that of their respective predecessors in the opened set $\mathcal { O } \subseteq \mathcal { N }$ . As such, the smallest NSQ value in the unopened set must be greater than that in the opened set:

$$
\min _ {N \in \mathcal {U}} f _ {n s q} (N) \geq \min _ {N \in \mathcal {O}} f _ {n s q} (N)\tag{8}
$$

Irrespective of the location of the node $N ^ { * }$ with optimal makespan $C ( \sigma ^ { * } )$ , the inequality in (8) implies that

$$
C (\sigma^ {*}) \geq \min _ {N \in \mathcal {O}} C (\sigma_ {N})\tag{9}
$$

As we require any valid solution to satisfy all trait requirements, the solution node (N<sup>ˆ</sup> ) will have an APR value of zero. Thus, the TETAQ heuristic (de<sup></sup>ned in (3)) of N<sup>ˆ</sup> is given by

$$
f _ {t e t a q} (\hat {N}) = (1 - \alpha) f _ {n s q} (\hat {N})\tag{10}
$$

Given the relationship in (8) and the fact that D-ITAGS selects a solution from the open set based on a best-<sup></sup>rst search, the TETAQ value of the solution node can be bounded as follows

$$
f _ {t e t a q} (\hat {N}) \leq f _ {t e t a q} (N), \forall N \in \mathcal {O}\tag{11}
$$

Expanding the de<sup></sup>nition of TETAQ and using (10) leads to

$$
\begin{array}{l} (1 - \alpha) \frac {C (\hat {\sigma}) - C (\sigma_ {L B})}{C (\sigma_ {U B}) - C (\sigma_ {L B})} \leq \\ \alpha f _ {a p r} (N) + (1 - \alpha) \frac {C (\sigma_ {N}) - C (\sigma_ {L B})}{C (\sigma_ {U B}) - C (\sigma_ {L B})}, \forall N \in \mathcal {O} \end{array}\tag{12}
$$

Using the inequality in (8), the bound in (9), and the fact that $f _ { a p r } ( \cdot ) \leq 1$ , we rewrite the above equation as

$$
(1 - \alpha) \frac {C (\hat {\sigma}) - C (\sigma_ {L B})}{C (\sigma_ {U B}) - C (\sigma_ {L B})} \leq \alpha + (1 - \alpha) \frac {C (\sigma^ {*}) - C (\sigma_ {L B})}{C (\sigma_ {U B}) - C (\sigma_ {L B})}
$$

By simplifying and cancelling equivalent terms, we get

$$
\begin{array}{l} (1 - \alpha) (C (\hat {\sigma}) - C (\sigma_ {L B})) \leq \\ \alpha (C (\sigma_ {U B}) - C (\sigma_ {L B})) + (1 - \alpha) (C (\sigma^ {*}) - C (\sigma_ {L B})) \end{array}\tag{13}
$$

On rearranging the terms, we arrive at the bound in (6). <sup>□</sup>

Note that the above result on time optimality gap is sensible only when $\alpha \ : \ : < \ : \ : 0 . 5$ . When $\alpha \ \geq \ 0 . 5 .$ the bound in (6)

![](Neville2022DITAGS_figs/9912f7c757bd7d5551a340d869fcfb386cfe849cde70f34eb10e9d1fd6a16852.jpg)  
Figure 2: Flow chart illustrating D-ITAGS’ targeted repair mechanism when responding to different unexpected events.

![](Neville2022DITAGS_figs/bf851e48971ee29b40d94694b2d3aba33c512f76750506c534c73725a698d949.jpg)

![](Neville2022DITAGS_figs/75dffd5ba47f912162a03c0b4b8b424f0d3fafa76cf3b3de2042bfa6315c6a8f.jpg)  
Figure 3: D-ITAGS is considerably faster than ITAGS (left), without sacri<sup></sup>cing solution quality (right). Runs in which D-ITAGS is better (worse) than ITAGS are shown in green (red).

loses signi<sup></sup>cance as it grows beyond the maximum difference possible difference in makespan $( C ( \sigma _ { U B } ) \cdot C ( \sigma _ { L B } ) )$

The bound presented in (6) can be tightened after the execution of the D-ITAGS, facilitating post-hoc performance analyses. Speci<sup></sup>cally, instead of bounding $f _ { a p r } ( N ) , \forall N \in \mathcal { O }$ by 1, we can compute the exact minimum $( \mathrm { m i n } _ { N \in \mathcal { O } } f _ { a p r } ( N ) )$ Following similar algebraic manipulations as in the proof above, a tighter bound can then be derived as

$$
C (\hat {\sigma}) - C (\sigma^ {*}) \leq \frac {\alpha}{1 - \alpha} (C (\sigma_ {U B}) - C (\sigma_ {L B})) \min _ {N \in \mathcal {O}} f _ {a p r} (N)\tag{14}
$$

## B. Analysis of Resource Optimality

Below, we show that we achieve resource optimality (i.e., the fewest number of assignments) when $\alpha = 1$

Theorem 2. Let $R ( A ) = \| A \| _ { 1 }$ <sub>1</sub> denote the total number of assignments in A, and $A _ { N _ { A } }$ <sub>∗</sub> be the allocation with the fewest assignments. Then, when $\alpha = 1$

$$
R (\pmb {A} _ {\hat {N}}) - R (\pmb {A} _ {N _ {A ^ {*}}}) = 0\tag{15}
$$

Proof. Since any expansion of a parent node represents the addition of an assignment, any given node N is guaranteed to have more agents assigned than its parent $N _ { p }$ . As additional agents can never increase APR, we have

$$
f _ {a p r} (N) <   f _ {a p r} (N _ {p}), \quad \forall N \in \mathcal {N}\tag{16}
$$

The above inequality and the fact that D-ITAGS will only consider APR (and ignore NSQ) when α = 1 suggest that D-ITAGS will begin at the root node and continue along the same branch until <sup></sup>nding a solution, expanding only the nodes that decrease APR by the largest amount. As such, D-ITAGS will take the shortest route to the solution when $\alpha = 1$ , leading to the fewest assignments (i.e., resource optimality). □

We do not include the bound on resource suboptimality in the interest of space and due to the fact that true resource optimality gap can be ef<sup></sup>ciently computed post-hoc since D-ITAGS takes the least amount of time to compute the resource optimal solution (α = 1), in stark contrast to the time-optimal solution (α = 0) required to compute the time optimality gap.

## VII. EVALUATION

We evaluated D-ITAGS using three sets of experiments in a simulated emergency response domain [6], [26], [28]– [30] in which a team of robots must rescue survivors, deliver medicines, douse <sup></sup>res, and rebuild damaged buildings. We generated problems from this domain by varying the number of robots between 8 and 16, the number of tasks between 20 and 40, and the location of tasks. In all experiments, we used maps from the Robocup Rescue Competition [30].

## A. Comparison to Existing Task Allocation Algorithms

In the <sup></sup>rst set of experiments, we analyzed how D-ITAGS performed on 20 static problems in our survivor domain relative to the ITAGS [6]. We chose to compare our approach with ITAGS as i) it has been shown to perform better than other state-of-the-art time-extended task allocation algorithms, and ii) ITAGS’ trait-based task allocation inspired our approach.

We compared the performance of D-ITAGS and ITAGS in terms of computation time and solution makespan (see Fig. 3). As can be seen, D-ITAGS is capable of producing high-quality solutions on par with ITAGS while requiring far less computation time. The superior computational ef<sup></sup>ciency of D-ITAGS demonstrates that the D-ITAGS’ branch-andcut method is considerably more ef<sup></sup>cient than ITAGS’ Tabu search. Given these observations and the fact that ITAGS has been shown to outperform state-of-the-art algorithms for ST-MR-TA [6], [7], we can conclude that D-ITAGS offers stateof-the-art computational ef<sup></sup>ciency without sacri<sup></sup>cing quality.

## B. Performance on Dynamic Reallocation

We evaluated D-ITAGS on dynamic task allocation problems in which unexpected events can alter the problem domain at any point of execution, and compared it against the default strategy of existing approaches: running the task allocation algorithm from scratch given the updated problem domain. Note that the baseline used in these experiments is identical to D-ITAGS, except for missing the crucial targeted repair module. As such, any observed improvements can be attributed to the repair module and not to other improvements introduced by D-ITAGS (e.g., the MILP-based scheduler). We created a set of 500 dynamic repair problems in our survivor domain, and separated them into ten groups of 50 problems each. We measured the performance of both D-ITAGS and simple reallocation in terms of computation time and solution makespan.

Across a wide variety of dynamic conditions, we found that D-ITAGS produced high-quality solutions on par with reallocation from scratch (see Fig. 5), but required signi<sup></sup>cantly less computation time (see Fig. 4). These improvements in computation ef<sup></sup>ciency are likely due to D-ITAGS’ ability to identify and repair only the impacted nodes, while reusing the other nodes. We also found that D-ITAGS is particularly faster on problems that affect the allocations of nodes (e.g., changes to agents traits or the loss/addition of agents) as such changes do not require D-ITAGS to recompute the schedules of the affected nodes, saving expensive optimizations. Even for problems that require D-ITAGS to recompute schedules (e.g., task duration changes and lost/gained tasks), D-ITAGS performs signi<sup></sup>cantly better than naive reallocation as it reuses cached motion plans and allocations from the existing solution that remain valid. It is important to note that D-ITAGS solution quality could be worse than simple reallocation when a new agent is gained unexpectedly. This is caused by the fact that D-ITAGS’ targeted repair favors ef<sup></sup>ciency by reusing valid existing nodes, even if they do not utilize the newly available agent. While the baseline bene<sup></sup>ts from the new agent as it reallocates, it takes longer to compute a solution.

![](Neville2022DITAGS_figs/d04d70cd19ce0a95a78fa35c0a04cf4ffdf5e011a8089bb0f72815f9aac66925.jpg)  
Figure 4: After unexpected changes, D-ITAGS (targeted repair) is signi<sup></sup>cantly faster than recomputing solutions from scratch. Green (Red) dots indicate instances in which targeted repair performs better (worse) than complete reallocation.

![](Neville2022DITAGS_figs/c3ffa7f0641cf3be9c26d915bf01c6f64ac96c9d3d54c26eba84dbdc3979b036.jpg)  
Figure 5: D-ITAGS (targeted repair) generates solutions of quality (makespan) similar to recomputing solutions from scratch. Green (Red) dots indicate instances in which targeted repair performs better (worse) than complete reallocation.

## C. Validation of Makespan Guarantees

In our <sup></sup>nal experiment, we empirically examined the validity of our theoretical guarantees on makespan from Sec. VI-A.

We created a set of 35 problems in our survivor domain, each of which was solved multiple times while varying α between [0, 0.5]. For every combination of problem and α value, we computed the actual normalized time optimality gap and the corresponding normalized theoretical bound. As can be seen from Fig. 6, the time optimality gaps consistently respect the theoretical bound across all values of α. As expected, the values α = 0 (ignore APR) and α = 1 (ignore NSQ) respectively result in the shortest and longest schedules.

## VIII. CONCLUSIONS

We introduced D-ITAGS, an algorithm for task allocation in dynamic environments involving heterogeneous robots. D-ITAGS achieves ef<sup></sup>cient resilience by estimating and conserving portions of the existing solution that remain unaffected by the change. We showed that D-ITAGS trades-off between time and resource optimality and comes with theoretical guarantees on performance. Our detailed experiments conclusively demonstrate the effectiveness of D-ITAGS and its relative computational bene<sup></sup>ts over existing state-of-the-art task algorithms that resort to complete reallocation. A notable limitation of our work is that D-ITAGS assumes that unexpected events can be detected and identi<sup></sup>ed. While such approaches are currently being developed (e.g., [12]), we still require tools that can detect events and solve the credit assignment problem.

![](Neville2022DITAGS_figs/bd3d32efc35f6d9c53cb10de65796daca2c17fe9e0ba67e737787bebf0790afc.jpg)  
Figure 6: The theoretical bound consistently holds for varying values of α. A value of zero for a normalized time-optimality gap represents an optimal schedule, and a value of one represents the longest schedule seen during allocation.

While D-ITAGS provides an ef<sup></sup>cient mechanism to solve dynamic ST-MR-TA problems, there are opportunities for improvement. First, the relative bene<sup></sup>ts of repair over complete reallocation are yet to be fully characterized. While D-ITAGS always chooses to repair, it might sometimes be bene<sup></sup>cial to reallocate from scratch to better leverage positive changes despite the additional computation cost (e.g., our results show that reallocation might produce better-quality solutions when new agents become available, albeit at a signi<sup></sup>cantly higher computational burden). Second, not all events require repair. For instance, when requirements reduce, we could continue using the current solution as it would remain valid despite becoming inef<sup></sup>cient. In such circumstances, the bene<sup></sup>ts of repair must be weighed against its computational cost.

## REFERENCES

[1] J. J. Roldan, P. Garcia-Aunon, M. Garz ´ on, J. de Le ´ on, J. del Cerro, ´ and A. Barrientos, “Heterogeneous multi-robot system for mapping environmental variables of greenhouses,” Sensors (Switzerland), vol. 16, no. 7, 2016.

[2] A. W. Stroupe, T. Huntsberger, B. Kennedy, H. Aghazarian, E. T. Baumgartner, A. Ganino, M. Garrett, A. Okon, M. Robinson, and J. A. Townsend, “Heterogeneous robotic systems for assembly and servicing,” European Space Agency, (Special Publication) ESA SP, no. 603, pp. 625–631, 2005.

[3] N. Baras and M. Dasygenis, “An algorithm for routing heterogeneous vehicles in robotized warehouses,” in 5th Panhellenic Conference on Electronics and Telecommunications, 2019.

[4] H. Ravichandar, K. Shaw, and S. Chernova, “STRATA: uni<sup></sup>ed framework for task assignments in large teams of heterogeneous agents,” Autonomous Agents and Multi-Agent Systems, vol. 34, no. 2, pp. 1–25, 2020.

[5] D. Matos, P. Costa, J. Lima, and A. Valente, “Multiple Mobile Robots Scheduling Based on Simulated Annealing Algorithm,” in International Conference on Optimization, Learning Algorithms and Applications, 2021.

[6] G. Neville, A. Messing, H. Ravichandar, S. Hutchinson, and S. Chernova, “An Interleaved Approach to Trait-Based Task Allocation and Scheduling,” in International Conference on Intellifent Robots and Systems, IEEE, 2021.

[7] A. Messing, G. Neville, S. Chernova, S. Hutchinson, and H. Ravichandar, “GRSTAPS: Graphically Recursive Simultaneous Task Allocation, Planning, and Scheduling,” International Journal of Robotics Research, vol. 41, no. 2, pp. 232–256, 2022.

[8] A. Prorok, M. Malencia, L. Carlone, G. S. Sukhatme, B. M. Sadler, and V. Kumar, “Beyond Robustness: A Taxonomy of Approaches towards Resilient Multi-Robot Systems,” arXiv, 2021.

[9] A. Prorok, “Redundant Robot Assignment on Graphs with Uncertain Edge Costs,” in International Symposium on Distributed Autonomous Robotic Systems (DARS), 2018.

[10] M. Rudolph, S. Chernova, and H. Ravichandar, “Desperate Times Call for Desperate Measures: Towards Risk-Adaptive Task Allocation,” in IEEE International Conference on Intelligent Robots and Systems, pp. 2592–2597, Institute of Electrical and Electronics Engineers Inc., 2021.

[11] X. Chen, P. Zhang, G. Du, and F. Li, “A distributed method for dynamic multi-robot task allocation problems with critical time constraints,” Robotics and Autonomous Systems, vol. 118, pp. 31–46, 8 2019.

[12] S. Mayya, D. S. D’Antonio, D. Saldana, and V. Kumar, “Resilient Task Allocation in Heterogeneous Multi-Robot Systems,” IEEE Robotics and Automation Letters, vol. 6, pp. 1327–1334, 4 2021.

[13] B. P. Gerkey and M. J. Mataric, “A formal analysis and taxonomy of´ task allocation in multi-robot systems,” International Journal of Robotics Research, vol. 23, no. 9, 2004.

[14] G. Neville, H. Ravichandar, K. Shaw, and S. Chernova, “Approximated dynamic trait models for heterogeneous multi-robot teams,” IEEE International Conference on Intelligent Robots and Systems, pp. 7978–7984, 2020.

[15] E. Nunes, M. Manner, H. Mitiche, and M. Gini, “A taxonomy for task allocation problems with temporal and ordering constraints,” Robotics and Autonomous Systems, vol. 90, 2017.

[16] S. Giordani, M. Lujak, and F. Martinelli, “A distributed multi-agent production planning and scheduling framework for mobile robots,” Computers and Industrial Engineering, vol. 64, no. 1, 2013.

[17] M. Krizmancic, B. Arbanas, T. Petrovic, F. Petric, and S. Bogdan, “Cooperative Aerial-Ground Multi-Robot System for Automated Construction Tasks,” IEEE Robotics and Automation Letters, vol. 5, no. 2, pp. 798–805, 2020.

[18] J. Guerrero, G. Oliver, and O. Valero, “Multi-robot coalitions formation with deadlines: Complexity analysis and solutions,” PLoS ONE, vol. 12, no. 1, 2017.

[19] M. Gombolay, R. Wilcox, and J. Shah, “Fast Scheduling of Multi-Robot Teams with Temporospatial Constraints,” 2016.

[20] P. Schillinger, M. Buerger, and D. Dimarogonas, “Improving Multi-Robot Behavior Using Learning-Based Receding Horizon Task Allocation,” Robotics: Science and Systems, 2018.

[21] M. Koes, I. Nourbakhsh, and K. Sycara, “Constraint optimization coordination architecture for search and rescue robotics,” in Proceedings - IEEE International Conference on Robotics and Automation, vol. 2006, 2006.

[22] A. Prorok, M. A. Hsieh, and V. Kumar, “The Impact of Diversity on Optimal Control Policies for Heterogeneous Robot Swarms,” IEEE Transactions on Robotics, 2017.

[23] K. Lerman, C. Jones, A. Galstyan, and M. J. Matari<sup>´</sup>cmatari<sup>´</sup>c, “Analysis of Dynamic Task Allocation in Multi-Robot Systems,” International Journal of Robotics Research, vol. 25, no. 3, 2006.

[24] A. C. Chapman, R. A. Micillo, R. Kota, and N. R. Jennings, “Decentralised Dynamic Task Allocation: A Practical Game-Theoretic Approach \*,” in International Conference on Autonomous Agents and Multiagent Systems, 2009.

[25] P. Ghassemi and S. Chowdhury, “Multi-robot task allocation in disaster response: Addressing dynamic tasks with deadlines and robots with range and payload constraints,” Robotics and Autonomous Systems, vol. 147, 1 2022.

[26] A. Messing and S. Hutchinson, “Forward Chaining Hierarchical Partial-Order Planning,” International Workshop on the Algorithmic Foundations of Robotics, vol. 14, 2020.

[27] I. Sucan, M. Moll, and L. E. Kavraki, “The Open Motion Planning Library (OMPL),” IEEE Robotics & Automation Magazine, vol. 19, no. 4, pp. 72–82, 2012.

[28] A. Whitbrook, Q. Meng, and P. W. Chung, “A novel distributed scheduling algorithm for time-critical multi-agent systems,” in IEEE International Conference on Intelligent Robots and Systems, vol. 2015- Decem, pp. 6451–6458, 2015.

[29] W. Zhao, Q. Meng, and P. W. Chung, “A Heuristic Distributed Task Allocation Method (PIA),” IEEE Transactions on Cybernetics, vol. 46, pp. 902–915, 4 2016.

[30] H. Kitano, S. Tadokoro, I. Noda, H. Matsubara, T. Takahashi, A. Shinjou, and S. Shimada, “RoboCup rescue: search and rescue in large-scale disasters as a domain for autonomous agents research,” Proceedings of the IEEE International Conference on Systems, Man and Cybernetics, vol. 6, pp. 739–743, 1999.