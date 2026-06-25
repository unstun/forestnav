---
citation_key: Kamale2025Abased
arxiv_id: 2511.16844
arxiv_url: "https://arxiv.org/abs/2511.16844"
title: "A*-based Temporal Logic Path Planning with User Preferences on Relaxed Task Satisfaction"
authors_short: "Disha Kamale et al."
year: 2025
direction_tag: E_bounded_suboptimal_search
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:19:43Z
origin: ai+web
reviewed: false
---

# A<sup>∗</sup>-based Temporal Logic Path Planning with User Preferences on Relaxed Task Satisfaction

Disha Kamale, Xi Yu, Cristian-Ioan Vasile

Abstract— In this work, we consider the problem of planning for temporal logic tasks in large robot environments. When full task compliance is unattainable, we aim to achieve the best possible task satisfaction by integrating user preferences for relaxation into the planning process. Utilizing the automata-based representations for temporal logic goals and user preferences, we propose an A<sup>∗</sup>-based planning framework. This approach effectively tackles large-scale problems while generating nearoptimal high-level trajectories. To facilitate this, we propose a simple, efficient heuristic that allows for planning over large robot environments in a fraction of time and search memory as compared to uninformed search algorithms. We present extensive case studies to demonstrate the scalability, runtime analysis as well as empirical bounds on the suboptimality of the proposed heuristic.

## I. INTRODUCTION

With the rapidly growing integration of robots into realworld applications, the need for time-efficient, sophisticated frameworks for successfully executing complex tasks is increasingly prominent. In this work, we consider the problem of planning for tasks expressed as temporal logic (TL) goals. TL formulations are particularly valuable due to their rich semantics, which enable precise articulation of complex requirements for robotic systems [1]–[4]. Traditionally, the problem of planning for TL specifications is approached using automata-based, sampling-based, optimization-based or learning-based techniques [5]–[9].

In this work, we are interested in designing a fast, scalable path-planning framework over large environments for given temporal logic specifications. A critical challenge in TL planning is that failing to meet even a minor sub-requirement can render the entire task infeasible. In such scenarios, it becomes crucial to still achieve meaningful satisfaction of the task as closely as possible. To facilitate this, we incorporate user preferences for relaxation of specifications into the planning framework. In the literature, various notions of relaxation including maximizing probability of satisfaction [10], [11], deadline relaxation [12], minimum revision, minimum violation [5], partial satisfaction [7], [13]. These methods often employ automata-based techniques, constructing explicit product automata for graph search to find optimal high-level trajectories. While this approach provides a clear notion of progress towards satisfaction, its scalability is limited when dealing with large environments or complex tasks.

For large robot environments, complex task specifications, and large number of user preferences, the runtime of path planning can rapidly increase. Several works consider the path planning problems over large environments utilizing techniques ranging from contraction hierarchies [14], sampling-based methods [2], [15] to hierarchical planning. Informed search algorithms such as A<sup>∗</sup> have been found useful at efficiently solving these large-scale problems over discrete search spaces [13], [16]–[18]. However, the efficiency of A<sup>∗</sup> depends largely on the heuristic function, which provides an estimate of the cost to reach the goal. The worstcase time and memory complexity of A<sup>∗</sup> is exponential in depth of search. To address this, several variants, such as the weighted A<sup>∗</sup> [19], [20], have been proposed to enhance search performance, though at the expense of optimality guarantees [21].

We propose a heuristic function for TL task planning that efficiently reduces the number of nodes explored to find a solution by leveraging the problem’s structure. The primary objective of this work is to develop a fast planning approach for robots deployed in large environments with syntactically co-safe Linear Temporal Logic (scLTL) tasks and user preferences on relaxed satisfaction in case of infeasibility. Similar to our previous works [6], [22], we represent the user preferences as a weighted-finite-state-edit system. By leveraging the abstractions to encapsulate robot motion, specification and user preferences, we propose a heuristic-based path planning framework. We trade-off optimality guarantees in planning for search efficiency, measured by the reduction in explored nodes and improved runtime performance.

This work differs from closely related works [6], [13], [17], [22] in several aspects. In [6], we considered an explicit product automaton construction to handle multiple notions of relaxations. As opposed to the optimization-based approach in [22], this work considers a heuristic-based search method. In [17], the authors address the problem of TL planning, without allowing relaxations to the specification. In [13], the authors present an efficient A<sup>∗</sup>-based approach to address TL planning with partial satisfaction. On the contrary, we consider multiple notions of relaxations such as minimum revision problem (MRP), minimum violation problem (MVP).

The main contributions of this work are threefold: 1) We propose a heuristic-based planning algorithm for temporal logic tasks and user preferences for relaxation that achieves near-optimal trajectories. 2) We propose an efficient heuristic based on progress in the relaxed specification automaton which captures the specification and all user-preferred relaxations in case of infeasible sub-specifications 3) Our extensive case studies demonstrate the efficacy of the proposed heuristic in terms of a significant improvement in memory and computation time across various examples. Moreover, we present the runtime analysis of the proposed heuristic with respect to different components of TL planning problem.

Notation The symbols <sup>R</sup>, $\mathbb { Z } ,$ and <sup>B</sup> represent the sets of real, integer, and binary numbers respectively. The set of integers greater than or equal to a is denoted by $\mathbb { Z } _ { \geq a } .$ . For a set $X , ^ { - } 2 ^ { X }$ and |X| denote its power set and cardinality, respectively. If $\Sigma$ is an alphabet, then $\Sigma ^ { * }$ represents the language consisting of all finite words over Σ.

## II. PROBLEM SETUP

In this section, we formally introduce the problem of temporal logic path planning with relaxation. We begin with a detailed description of models expressing the robot’s motion in the environment, the temporal logic task description as well as formal model encapsulating the user’s preferences for relaxation in case the original specification is infeasible.

## A. Robot and Environment Model

We consider a robot deployed in a fully known planar environment within which the robot can move deterministically. The environment may contain multiple labeled regions. We consider a finite abstraction of the robot’s motion in the environment as a weighted transition system, a widely followed approach in formal control synthesis [5], [23], [24].

Definition 2.1 (Transition System): A weighted transition system (TS) is a tuple $\mathcal { T } = ( X , x _ { 0 } ^ { \mathcal { T } } , \delta _ { \mathcal { T } } , A \bar { P , } \ell , w _ { \mathcal { T } } )$ , where $X$ is a finite set of states indicating regions in the environment; $x _ { 0 } ^ { \mathcal { T } } \in X$ is the initial state; $\delta _ { \mathcal { T } } \subseteq X \times X$ is a set of transitions which captures the set of permissible robot movements in the environment; $A P$ is a set of labels (atomic propositions); $\ell \colon X  A P$ is a labeling function; $w _ { T } \colon \delta _ { T }  \mathbb { R } _ { > 0 }$ is a weight function.

Note that in addition to transitions between regions, $\delta \tau$ also contains self-loop transitions, allowing the robot to stay stationary at any state $x \in X$ . The weight function $w _ { T } ( x _ { k } , x _ { k + 1 } )$ represents path length from $x _ { k } ~ \mathrm { t o } ~ x _ { k + 1 }$ Naturally, traversing a self-loop incurs a cost of 0.

As the robot moves through the environment, it generates a (potentially infinite) sequence of states $\mathbf { x } ~ = ~ x _ { 0 } , x _ { 1 } \ldots ,$ referred to as a trajectory (or run) of a robot, such that $( x _ { k } , x _ { k + 1 } ) \in \delta _ { T }$ for all $k \in \mathbb { Z } _ { > 0 }$ and $x _ { 0 } = x _ { 0 } ^ { \mathcal { T } }$ . When the robot is at a state x labeled with $\pi \in A P$ , the atomic proposition π is said to be true. The set of all trajectories of $\tau$ is $R u n s ( \mathcal { T } )$ . A state trajectory x generates an output trajectory $\mathbf { o } = o _ { 0 } o _ { 1 } \ldots .$ where $o _ { k } \ : = \ : h ( x _ { k } )$ for all $k \geq 0$ . We also denote an output trajectory by $\mathbf { o } = { \boldsymbol { \ell } } ( \mathbf { x } )$ . The (generated) language corresponding to a TS T is the set of all generated output words, which we denote by $\mathcal { L } ( \mathcal { T } )$ . We define the weight of a trajectory as $\begin{array} { r } { w _ { \mathcal { T } } ( \mathbf { x } ) = \sum _ { k = 1 } ^ { | \mathbf { x } | } w _ { \mathcal { T } } ( x _ { k - 1 } , x _ { k } ) } \end{array}$

## B. Temporal Logic Specification

In this work, we use syntactically co-safe Linear Temporal Logic (scLTL) to formally define the robot tasks. scLTL composes symbols from $\Sigma = 2 ^ { A P }$ with logical and temporal operators with the following syntax:

$$
\varphi := \top \mid \pi \mid \neg \varphi \mid \varphi \land \varphi \mid \varphi \mathcal {U}   \varphi \mid \mathbf {X} \varphi\tag{1}
$$

where, $\pi \in A P .$ ⊤ denotes logical true value, negation (¬) and conjunction (∧) are Boolean operators while next (X) and until (U) denote the temporal operators. Additional Boolean operators such as disjunction (∨) and temporal operators such as eventually (F) can be derived using 1. Intuitively, the formula $\mathbf { X } { \boldsymbol { \varphi } }$ denotes that $\varphi$ holds true at the next step, $\mathbf { F } \varphi$ indicates that $\varphi$ is satisfied at some point in the future, and $\varphi _ { 1 } \mathcal { U } \varphi _ { 2 }$ denotes that $\varphi _ { 1 }$ is true until $\varphi _ { 2 }$ becomes true. For a detailed description of the syntax and semantics of scLTL, we refer the reader to [23].

Although the semantics of scLTL formulae is defined over infinite words, such as the ones produced by $\tau ,$ , its satisfaction can be decided in finite time enabled by finite good prefixes [25]. An scLTL formula is said to be satisfied by trajectory x, denoted as $\mathbf { x } \Vdash \phi ,$ if and only if the resulting output word satisfies $\phi , \operatorname { i . e . , o } \ p = \phi$

## C. User preferences for relaxation

If part of the task specification $\phi$ should become infeasible, the user relaxation preferences facilitate meaningful satisfaction of the task.

Definition 2.2 (User Relaxation Preference): Let L be a language over the alphabet $2 ^ { A P } , \mathrm { \bf ~ A }$ user task preference is a pair $( R , w _ { R } )$ , where $R \subseteq L \times ( 2 ^ { A P } ) ^ { * }$ is a relation that captures how words in L can be transformed to words from $( 2 ^ { A P } ) ^ { * }$ and is of the form $\sigma \mapsto ^ { p } \sigma ^ { \prime }$ where $\sigma \in$ $L , \sigma ^ { \prime } \in ( 2 ^ { { \overset { \triangledown } { A ^ { \prime } } } } ) ^ { * }$ . w<sub>R</sub> : R → <sup>R</sup> represents the cost of the word transformations. The relation R can also be understood as a multi-valued function $R \colon L  ( 2 ^ { A P } ) ^ { * }$

Example 2.1: Consider the task of picking up bread and ice-cream from a supermarket. The scLTL specification is $\begin{array} { l l l } { \phi } & { = } & { \left( { \bf F } \mathrm {  ~ \psi ~ } _ { b r e a d _ { s } } \right) \wedge { \bf F } } \end{array}$ ice $. c r e a m _ { s } ,$ where $b r e a d _ { s }$ and ice cream are atomic propositions. If infeasible, the user-preferred relaxation options are 1) picking up bread from the nearest local bakery for a penalty of 5, 2) picking up ice cream from the nearest shop for a penalty of 7, 3) removing ice-cream from the list for a penalty of 12. The formal representation for these preferences is $1 ) b r e a d _ { s } \mapsto 5 b r e a d _ { b a k e r y } , 2 ) i c e \_ c r e a m _ { s } \mapsto 7$ ice cream<sub>shop</sub>, 3)ice cream<sub>s</sub> $\mapsto ^ { 1 2 } \ \epsilon .$ . Note that (1) and (2) are instances of MRP while (3) is an instance of MVP.

## D. Problem definition

The problem of optimal temporal logic path planning with relaxation is defined as follows.

Problem 2.1 (Optimal TL Path Planning with Relaxations): Given the robot motion abstraction as a weighted transition system $\tau ,$ an scLTL task specification $\phi$ as well as user preferences for relaxation $( R , w _ { R } )$ , find a path $\tilde { \bf x }$ in $\tau$ that satisfies the specification $\phi$ while only performing necessary relaxations and minimizes the cost of the trajectory.

Formally,

$$
\begin{array}{l} \min _ {\mathbf {x}} \hat {J} (\mathbf {x}) = w _ {\mathcal {T}} (\mathbf {x}) + \lambda \cdot w _ {R} (\mathbf {o}, \mathbf {o} ^ {r e l a x}) \\ \quad \text {s.t.} \mathbf {x} _ {0} = x _ {0} ^ {\mathcal {T}} \quad (\text {Initial state}), \\ \quad \mathbf {o} \models \phi \quad (\text {Task satisfaction}), \end{array}
$$

$\mathbf { o } ^ { r e l a x } = \ell ( \mathbf { x } ) , \ : ( \mathbf { o } , \mathbf { o } ^ { r e l a x } ) \in R$ (Relaxation preferences) where λ represents a blending parameter, $\mathbf { o } ^ { r e l a x } \ = \ \ell ( \mathbf { x } )$ denotes the output word of the $\tau$ , and $\mathbf { o } ~ \in ~ ( 2 ^ { A P } ) ^ { * }$ is a word satisfying ϕ.

## III. APPROACH

In this section, we elaborate on our approach to Problem 2.1 which involves several key steps. Given the task specification and user preferences for relaxation, we begin by converting them into automata. This facilitates the construction of a Relaxed Satisfaction Automaton, introduced in [22], which efficiently encapsulates the original task specification and all user-preferred relaxations along with their associated penalties. The primary advantage this offers is that the progress toward task satisfaction can be explicitly considered even in the case of infeasible sub-specifications. Building upon this representation, we present the $\mathbf { A } ^ { * }$ -based search algorithm for temporal logic planning with relaxations, which is the main contribution of this work. Finally we present a discussion on practical considerations regarding the design of the heuristic for TL planning.

## A. Automata models for temporal logic

Any scLTL formula $\phi$ can be translated [26] into a deterministic finite state automaton (FSA) which accepts the set of all good prefixes of all words that satisfy $\phi$ [25], defined as follows.

Definition 3.1 (Deterministic Finite State Automaton): A deterministic finite state automaton (DFA) is a tuple $\mathcal { A } _ { \phi } = ( S _ { \mathcal { A } _ { \phi } } , s _ { 0 } ^ { A _ { \phi } } , \Sigma , \delta _ { \mathcal { A } _ { \phi } } , F _ { \mathcal { A } _ { \phi } } )$ , where: $S _ { A _ { \phi } }$ is a finite set of states; $s _ { 0 } ^ { \mathcal { A } _ { \phi } } ~ \in ~ S _ { \mathcal { A } _ { \phi } }$ is the initial state; Σ is the input alphabet; $\delta _ { \mathcal { A } _ { \phi } } \colon S _ { \mathcal { A } _ { \phi } } \times \Sigma \to S _ { \mathcal { A } _ { \phi } }$ is the transition function; $F _ { \mathrm { \mathcal { A } _ { \phi } } } \subseteq S _ { \mathrm { \mathcal { A } _ { \phi } } }$ is the set of accepting states.

A trajectory of the $\mathrm { D F A } \ \mathbf { s } = s _ { 0 } s _ { 1 } \dots s _ { n + 1 }$ is generated by a finite sequence of symbols $\pmb { \sigma } = \sigma _ { 0 } \sigma _ { 1 } \ldots \sigma _ { n }$ where $s _ { 0 } =$ $s _ { 0 } ^ { \mathcal { A } _ { \phi } }$ is the initial state of $\mathcal { A } _ { \phi }$ and $\boldsymbol { s } _ { k + 1 } = \delta _ { \boldsymbol { A } _ { \phi } } ( \boldsymbol { s } _ { k } , \sigma _ { k } )$ for all $0 \leq k \leq n$ . This trajectory is said to be accepting if $s _ { k + 1 } \in F _ { A _ { \phi } }$ . The (accepted) language of a DFA $\mathcal { A } _ { \phi }$ is the set of accepted input words denoted by $\mathcal { L } ( A _ { \phi } )$ . Thus, in order to ensure the satisfaction of a formula ϕ by a trajectory x in environment T , it is necessary that $\mathbf { o } = \ell ( \mathbf { x } ) \in \mathcal { L } _ { A _ { \phi } }$

In order to handle infeasibilities in $\phi ,$ the user preferences for relaxation are converted into a weighted finite state edit system defined as follows:

Definition 3.2 (Weighted Finite State Edit System):

A weighted finite state edit system (WFSE) is a weighted DFA $\begin{array} { r l r } { \mathcal { E } } & { { } = } & { ( Z _ { \mathcal { E } } , z _ { 0 } ^ { \mathcal { E } } , \Sigma _ { \mathcal { E } } , \delta _ { \mathcal { E } } , F _ { \mathcal { E } } , w _ { \mathcal { E } } ) } \end{array}$ , where ${ \Sigma } _ { { \mathcal E } } ^ { { } ^ { - } } = { \bf \Sigma } \left( 2 ^ { A P } \cup \{ { \epsilon } \} \right) \times { \bf \Sigma } \left( 2 ^ { A P } \cup \{ { \epsilon } \} \right) \setminus \{ ( { \epsilon } , { \epsilon } ) \} , { \bf \Sigma } _ { { \epsilon } } ^ { { } ^ { - } }$ denotes a missing or deleted symbol, and $w \varepsilon \colon \delta \varepsilon \  \ \mathbb { R }$ is the transition weight function.

The alphabet $\Sigma \varepsilon$ captures word edit operations such as addition, substitution, or deletion of symbols. A transition $z ^ { \prime } = \delta \varepsilon ( z , ( \sigma , \sigma ^ { \prime } ) )$ has input, output symbols σ and $\sigma ^ { \prime }$

Remark: We add pass-through transitions to the WFSE with 0 weights to ensure that the satisfaction is not relaxed if the entire original specification is feasible.

Example 3.1 (Continuation of Example $2 . l ) .$ : Consider states $z , z ^ { \prime } \in Z _ { \mathcal { E } }$ . Preference 1 can be captured by states $z , z ^ { \prime }$ such that $z ^ { \prime } ~ \in ~ ( z , \delta { \varepsilon } ( \sigma , \sigma ^ { \prime } ) )$ where $\sigma$ is the input symbol such that brea $d _ { s } \in \sigma , \sigma ^ { \prime }$ denotes the output symbol $b r e a d _ { b a k e r y } \in \sigma ^ { \prime }$ and $w \varepsilon ( z , ( \sigma , \sigma ^ { \prime } ) , z ^ { \prime } ) = 5$

## B. Relaxed Specification Product Automaton

All permissible relaxations of the scLTL specification $\phi$ are captured using a product non-deterministic finite state automaton [22] between the DFA $\mathcal { A } _ { \phi }$ and the WFSE $\mathcal { E }$

Definition 3.3 (Relaxed Specification Automaton): Given a specification DFA $\begin{array} { r l r } { A _ { \phi } } & { { } = } & { ( S _ { A _ { \phi } } , s _ { 0 } ^ { A _ { \phi } } , \Sigma , \delta _ { A _ { \phi } } , F _ { A _ { \phi } } ) } \end{array}$ the user task preferences represented as a WFSE $\mathcal { E } ~ = ~ ( Z _ { \mathcal { E } } , z _ { 0 } ^ { \mathcal { E } } , \Sigma _ { \mathcal { E } } , \delta _ { \mathcal { E } } , F _ { \mathcal { E } } , w _ { \mathcal { E } } )$ , the relaxed specification automaton is a tuple $\begin{array} { c c l } { A } & { = } & { \left( Q _ { A } , q _ { A } ^ { 0 } , \Sigma _ { A } , \delta _ { A } , F _ { A } , w _ { A } \right) } \end{array}$ where $\begin{array} { c c c } { { Q _ { \cal A } } } & { { = } } & { { Z \varepsilon \times S _ { { \cal A } _ { \phi } } } } \end{array}$ represents the state space; $q _ { 0 } ^ { \ A } \ = \ ( z _ { 0 } ^ { \varepsilon } , s _ { 0 } ^ { \ A _ { \phi } } )$ is the initial state; $\Sigma _ { \mathcal { A } } = \Sigma _ { \mathcal { A } _ { \phi } }$ denotes the alphabet; $\delta _ { \cal A } \subseteq Q _ { \cal A } \times \Sigma _ { \cal A } \times Q _ { \cal A }$ is a transition relation; $F _ { \mathcal { A } } = F _ { \mathcal { E } } \times F _ { \mathcal { A } _ { \phi } } \subseteq Q _ { \mathcal { A } }$ represents the set of final (accepting) states; $w _ { \mathcal { A } } : \delta _ { \mathcal { A } }  \mathbb { R } _ { \geq 0 }$ is the weight function where $w _ { \mathcal { A } } ( q , q ^ { \prime } ) = w \varepsilon ( z , z ^ { \prime } )$

We direct the reader to [22] for the relaxed satisfaction automaton construction.

## C. Heuristic-based for TL planning with relaxation

For $\mathbf { A } ^ { * }$ search on an arbitrary graph, the cost of node n is given as $f ( n ) = g ( n ) + h ( n )$ . Thus, the cost computation utilizes two components of information: 1) the distance already covered to reach node n from some initial node $n _ { 0 }$ , and 2) an estimated cost to reach a final node $n _ { f }$ from node $n .$ . The function $f ( \cdot )$ is often referred to as the f-score of node $n .$ . The search continues by exploring the nodes with best f-scores until $n _ { f }$ is reached. The solution obtained by $\mathbf { A } ^ { * }$ is guaranteed to be optimal if the heuristic is an underestimation of the actual cost to reach the goal for all nodes. The informativeness of the heuristic directly impacts the efficiency of the search.

For TL planning, designing such an informative heuristic is challenging. Unlike the traditional graph search problems where the final node $n _ { f }$ is given, temporal logic tasks may require visiting multiple regions in the environment, where each visit to a location containing a desired label (atomic proposition) results in progress towards task satisfaction in the specification automaton. Potentially, the same atomic proposition could be satisfied at multiple locations in the environment. Thus, the state in the environment that results into reaching a final state in the specification automaton cannot be uniquely specified.

Heuristic We consider the distance to satisfaction in the relaxed satisfaction automaton scaled by a factor $\gamma .$ . Since $\mathcal { A }$ contains multiple final states $q \in F _ { A }$ , we add a virtual final state $q ^ { \bowtie }$ to $\mathcal { A }$ with only incoming edges $\{ ( q , q ^ { \bowtie } ) | q \in F _ { A } \}$ The heuristic value for node $( x , q )$ is,

$$
h (x, q) = \gamma \cdot d _ {m i n} (q, q ^ {\bowtie})\tag{2}
$$

where $d _ { m i n } ( q , q ^ { \prime } )$ denotes the minimum distance between nodes $q$ and $q ^ { \prime }$ in ${ \mathcal { A } } .$ . The search is performed over the solution space consisting of $\tau$ and A. Note that, we avoid the explicit product construction and instead only enumerate the reachable states in this space by keeping track of labels of $\tau$ and the resulting transitions in $\mathcal { A }$ Given a sequence of states $( ( x _ { 0 } , q _ { 0 } ) , ( x _ { 1 } , q _ { 1 } ) , \dots , ( x _ { k } , q _ { k } ) )$ , the graph distance for node $( x _ { k + 1 } , q _ { k + 1 } )$ is

$$
g (x _ {k + 1}, q _ {k + 1}) = \Sigma_ {0} ^ {i = k - 1} w _ {\mathcal {T}} (x _ {i}, x _ {i + 1}) + \lambda \cdot w _ {\mathcal {A}} (q _ {i}, q _ {i + 1})\tag{3}
$$

Alg. 1 outlines the search algorithm for TL planning with relaxation. Given the input $\tau , A _ { \phi }$ and $\mathcal { E } ,$ we construct the relaxed product automaton using the algorithm from [22] (line 2). The initial node $( x _ { 0 } ^ { \mathcal { T } } , q _ { \mathcal { A } } ^ { 0 } )$ is added to the queue to be processed. For node $( x , q )$ , the f-score is given by $f ( x , q ) =$ $g ( x , q ) + h ( x , q )$ where $g ( x , q )$ is the graph distance of node x from the initial node in $\tau$ and a graph distance in $\mathcal { A } _ { \phi }$ as in (3) and $h ( x , q )$ is obtained from (2). The queue keeps track of the f-score, current node, graph distances, and parent nodes. Given the current state (x, q), all neighbors of $x$ in $\tau$ and the corresponding generated input symbols inform the next states $q ^ { \prime }$ in $\mathcal { A }$ leading to a new state $( x ^ { \prime } , q ^ { \prime } )$ in the solution space (lines 10-11). If unexplored, this node is investigated for graph score g¯ and heuristic value. If the current path to $( x , q )$ from source is shorter than a previously stored path to $( x , q )$ , we update the $g _ { s c o r e }$ set. The queue is updated with node $( x , q )$ and the associated information. Upon reaching the final state in A, the search stops and the resulting trajectory in the solution space is obtained using the stored parent nodes. Finally the path is projected onto the robot environment to obtain the trajectory in the robot environment, denoted by $\textbf { x } = p a t h _ { \perp \tau }$ (lines 6-8), where $\perp \mathbf { \tau } ( \cdot )$ is the projection operator with $\perp \left( x _ { k } , q _ { k } \right) = x _ { k }$ . If the final state in A cannot be reached, the routine returns infeasibility.

```txt
Algorithm 1: A*-based search for TL relaxation()

Input: T, φ, E, γ
Result: x

1 Initialize queue ← ∅, explored ← ∅, g_scores ← ∅
2 A = construct_A(E, Aφ) using [22]
3 g_scores ← {(x₀ᵀ, qₐ⁰) = 0}, queue ← (0, (x₀ᵀ, qₐ⁰), 0, None)
4 while queue ≠ ∅ do
5    (x, q) ← queue.pop()
6    if q ∈ Fₐ then
7    reconstruct path = ((x₀ᵀ, qₐ⁰), ..., (x, q)) return path⊥ₜ
8    if (x, q) in explored then continue
9    explored ← (x, q)
10    forall (x, x') ∈ δₜ do
11    forall (q, (ℓ(x'), σ'), q') ∈ δₐ do
12    if (x', q') in explored then
13    continue
14    ḡ ← g_scores(x, q) + wₜ(x, x') + λ · wₐ(q, q') 3
15    h(x', q') ← get_heuristic(q, q') 2
16    if (x', q') ∈ g_scores then
17    if g_scores(x', q') < ḡ then continue
18    else g_scores(x', q') ← ḡ
19    queue ← ((ḡ + h(qₐ, q'), (x', q'), ḡ, (x, q)))
20    return Infeasible
```  
Lemma 3.1 (correctness): The solution given by the proposed search algorithm always satisfies the specification. i.e., $\ \bar { \mathbf { o } } ^ { r e l a x } = h ( \tilde { \mathbf { x } } ) \bar { \mathbf { \rho } } = \phi .$

Proof: Follows by construction and the stopping criterion the Alg. 1. ■

## D. Heuristic discussion

The explicit product computation scales multi-linearly with $| \mathcal { T } | , \ | \mathcal { A } _ { \phi } |$ and |E| restricting the scalability due to the exhaustive search of the reachable space for solutions. By implicitly enumerating the states in the solution space, the proposed search algorithm Alg. 1 offers a significant improvement in terms of runtime and memory even with zero heuristic.

Further improvement in search performance can be achieved by carefully crafting a heuristic function that balances informativeness and computational efficiency. While a highly informative heuristic can reduce the number of explored nodes, it may worsen overall performance due to increased computational cost compared to simple node expansion. For instance, consider the runtime and search results in Fig. 1. $h _ { i n f o }$ refers to an informative heuristic which takes into account the symbol σ needed to transition closer to the final state in A and computes the distance to one of the nodes in the environment that contains this symbol. As shown in Fig. 1, even though $h _ { i n f o }$ reduces the number of nodes explored, it significantly increases the runtime due to complex computations involved at each step. A commonly followed approach to circumvent this problem involves precomputing the necessary values. With slight changes to the problem setting, repeating these precomputations can quickly become impractical for large scale environments.

![](Kamale2025Abased_figs/b477ff71979de603bdbacb001078625575e3fa0e03eaaca3ed9cdd9ad19b99b2.jpg)  
Fig. 1. Runtime, memory, and precomputation time for $h = 0 , h _ { i n f o }$ and proposed heuristic h.

## IV. CASE STUDIES

In this section, we show the functionality of the proposed search algorithm, a comparison with a baseline uninformed search, and a runtime analysis. These studies were performed on Dell Precision 3640 Intel i9 with 64 GB RAM using Python 3.9.7. For all following studies, we set λ = 1.

## A. Functionality

Empirically determining the scaling factor. To determine the value of γ for a given problem, we consider a fixed problem setup by keeping the environment size, labeled locations, specifications and relaxation preference unchanged across iterations. Thus, the same problem instance is solved for different values of γ. We assess the resulting cost, runtime as well as number of nodes searched in the solution space.

![](Kamale2025Abased_figs/3b52b9b4ef344e81990d9a5580466c667b2c25505e24cf27fb9775b9e4498bee.jpg)  
Fig. 2. Trajectories obtained using baseline and the proposed heuristic. Nodes with atomic propositions of interest are shown in yellow.

Fig. 3 shows one such example for a grid environment of size (50,50) for a task of visiting 5 locations in no specific order, $\phi = \mathbf { F } a \wedge \mathbf { F } b \wedge \mathbf { F } c \wedge \mathbf { F } d \wedge \mathbf { F } e$ . We choose $\gamma = 4$ since it corresponds to an optimal cost while reducing the time and memory usage considerably. The choice of $\gamma$ is thus a design decision that balances the trade-off between computational cost and search efficiency.

![](Kamale2025Abased_figs/e229b65da8de75ffac0baed4affba2c8b2a27751ed161e14c1c72347be93f59d.jpg)  
Fig. 3. Empirical determination of the scaling factor

TL planning. It is important to note that the potential sub-optimality of the proposed heuristic does not affect the precise satisfaction of the temporal logic goals. In this case study, we aim to compare the trajectories given by the proposed approach with a baseline case of zero heuristic (uninformed search) denoted by $h _ { 0 }$ . The baseline is guaranteed to find an optimal solution for the given environment and specification. However, the optimal solution may not be unique.

Consider a 20x20 grid environment given as a weighted transition system T with seven atomic propositions (labels) $A P = \{ a , \dot { b } , c , d , e , h , i \}$ . Each transition has a unit weight and the self-loop transitions incur zero cost. The task specification is $\phi = ( \mathbf { F } \ a \wedge ( \mathbf { F } ( b \wedge \mathbf { F } \ c ) ) \wedge ( \mathbf { F } ( d \wedge \mathbf { F } \ e ) )$ ∧ F h ∧ $( \lnot \ i \ u \ h ) )$ . In plain English, this translates to “At some point in the future, visit a followed by b then visit c. Visit d followed $b y \ e .$ Visit h and do not visit i until h is visited.” Notice that the specification does not impose any ordering on $^ { a , }$ d and h. Thus, there are multiple possible ways in which the specification can be satisfied in T .

For evaluating our approach, we set $\gamma = 1 5$ and the initial state to (0, 0). The atomic propositions are then randomly assigned to the nodes in T . As shown in Fig. 2, our approach provides at least an order of magnitude speedup in runtime and reduction of nodes explored. As expected, in some cases, this speedup is achieved at a cost of optimality (Fig. 2(b)).

![](Kamale2025Abased_figs/57f9f6b962a9d56db9325d4c02ad429c68a181f56d523ca97a07987005614210.jpg)  
Fig. 4. Trajectories with relaxation obtained using baseline and the proposed heuristic. The green circles indicate satisfaction of a minimally relaxed subspecification. The red circle denotes a sub-optimal relaxation.

Compared to $h _ { 0 } ,$ our heuristic finds an optimal solution with 93.5% reduction in time, 93.2% reduction in memory for scenario 1 and a close-to-optimal solution for 94% reduction in time, 93% reduction in memory for scenario 2.

Relaxation For the same specification, if labels b and e are not present in the environment, the user preferences are (1) MRP: in place of $b ,$ k can be visited with a penalty of 3, (2) MRP: instead of $b , j$ can be visited while incurring a penalty of 5, (3) MVP: visit to e can be canceled with a penalty of 2. In other words, 1) $b \mapsto ^ { 3 } k , 2 ) \ b \mapsto ^ { 5 } j , 3 ) \ e \mapsto ^ { 2 } \ \epsilon$ . We set $\gamma = 1 5$ . The resulting trajectories are shown in Fig. 4. As depicted in scenario 1, the proposed heuristic finds an optimal path by substituting for b with the lowest revision penalty and violating e for the minimum violation penalty with 92.6% and 92.13% improvements in time and memory respectively. On the other hand, for scenario 2, our approach yields a sub-optimal path by using a relaxation preference with higher penalty resulting in a cost overhead of 16 while improving the time and memory usage by 91.8% and 90.4% compared to $h _ { 0 }$

## B. Large Scale Robot Environments

To showcase the computational efficiency of the proposed heuristic, we use the New York City motorways network from OSMNX [27] consisting of 378,040 nodes and 1,131,664 edges as T . We consider three representative cases: 1) sparse locations by considering only 3 labeled locations in the entire environment to be visited sequentially,

![](Kamale2025Abased_figs/68076ae8fbe210592e532d983e067ffdbcacf2b293a4cc315548b260b5ece87b.jpg)

COMPARISON W.R.T. BASELINE FOR LARGE SCALE ROBOT ENVIRONMENT

<table><tr><td>Specification</td><td>Solution Space Size</td><td>|AP|</td><td> $\gamma$ </td><td>Precomp. Time (ms)</td><td>Runtime (s)</td><td>Nodes searched</td><td>Cost</td></tr><tr><td> $\phi_1$ </td><td>nodes: 1512160edges: 11316640</td><td>3</td><td>- $\gamma_1 = 27000$ </td><td>-0.11</td><td>8.34 ( $h_0$ ) $\underline{3.83}$ </td><td>689193( $h_0$ ) $\underline{326860}$ </td><td>43151.37( $h_0$ ) $\underline{43151.37}$ </td></tr><tr><td> $\phi_1^{relax}$ </td><td>nodes: 4536480edges: 45266560</td><td>4</td><td>- $\gamma_1 = 27000$ </td><td>-0.11</td><td>147( $h_0$ ) $\underline{114}$ </td><td>844181( $h_0$ )649860</td><td>67546( $h_0$ )67546</td></tr><tr><td> $\phi_2$ </td><td>nodes: 13609440edges: 298759296</td><td>7</td><td>- $\gamma_{21} = 500$  $\gamma_{22} = 800$ </td><td>-1.11.1</td><td>28( $h_0$ ) $\underline{10.8}$  $\underline{6.58}$ </td><td>1643956( $h_0$ ) $\underline{669695}$  $\underline{460877}$ </td><td>28996( $h_0$ ) $\underline{28996}$  $\underline{33654}$ </td></tr><tr><td> $\phi_2^{relax}$ </td><td>nodes: 40828320edges: 1195037184</td><td>9</td><td>- $\gamma_{21} = 500$  $\gamma_{22} = 800$ </td><td>-1.91.7</td><td>233.8( $h_0$ ) $\underline{68.3}$  $\underline{44.98}$ </td><td>1364344( $h_0$ ) $\underline{611298}$  $\underline{422999}$ </td><td>22746.3( $h_0$ )22766.529973.8</td></tr><tr><td> $\phi_3$ </td><td>nodes: 18145920edges: 611098560</td><td>8</td><td>- $\gamma_{31} = 2000$  $\gamma_{32} = 5000$ </td><td>-2.82.76</td><td>237.17 ( $h_0$ ) $\underline{53.04}$  $\underline{16.87}$ </td><td>13941839 ( $h_0$ ) $\underline{3757966}$  $\underline{1216287}$ </td><td>81844( $h_0$ )8185084446</td></tr><tr><td> $\phi_3^{relax}$ </td><td>nodes: 54437760edges: 2444394240</td><td>9</td><td>- $\gamma_{31} = 2000$  $\gamma_{32} = 5000$ </td><td>-4.734.78</td><td>2957.40( $h_0$ ) $\underline{520.96}$  $\underline{269.6}$ </td><td>20333049( $h_0$ ) $\underline{4493701}$  $\underline{2507799}$ </td><td>78199( $h_0$ )94626.4894626.48</td></tr></table>

Fig. 5. a) Effect of randomized AP assignment, b) Effect of varying T size

2) a complex grouping of tasks with choices, and 3) a complex sequential task. The scLTL specifications are:

$$
1) \phi_ {1} = (\mathbf {F} (g r o c e r i e s \wedge \mathbf {F} (f u e l \wedge \mathbf {F} b a k e r y)))
$$

$$
\begin{array}{l} 2) \phi_ {2} = (({\bf F}   l u n c h \wedge {\bf F} (g r o c e r i e s \vee c o f f e e) \wedge {\bf F}   b a k e r y) \vee \\ (\mathbf {F}   f u e l \wedge {\bf F} (b r e a k f a s t \wedge ({\bf F}   b o o k s t o r e)))) \end{array}
$$

$$
\begin{array}{l} 3) \phi_ {3} = (\mathbf {F} l u n c h \land \mathbf {F} (g r o c e r i e s \land \mathbf {F} c o f f e e) \land \\ \mathbf {F} b a k e r y \land \mathbf {F} (f u e l \land \mathbf {F} (b r e a k f a s t \land (\mathbf {F} b o o k s t o r e))) \land \\ (\neg r e s t U b a k e r y)) \end{array}
$$

Additionally, the user preferences for relaxation in case of infeasibility are $f u e l \ \mapsto ^ { 5 }$ rest for $\phi _ { 1 } ;$ bakery $\mapsto ^ { 5 }$ mall, $c o f f e e \mapsto ^ { 3 }$ lunch for $\phi _ { 2 }$ and $\phi _ { 3 }$ . Table I summarizes the results. We denote by $\phi _ { i } ^ { r e l a x }$ the cases wherein relaxation is taken into account. The solution space size refers to the total number of nodes and edges given by $\vert X \vert \times \vert S _ { { \mathcal { A } } _ { \phi } } \vert \times \vert Z \varepsilon \vert$ and $| \delta \_ { } | \times | \delta _ { \mathcal { A } _ { \phi } } | \times | \delta _ { \mathcal { E } } |$ . It is crucial to note that we do not explicitly construct the solution space. $\vert A P \vert$ denotes the number of locations allocated in the environment. As evident from these results, the proposed heuristic is simple enough to be pre-computed in a few milliseconds while drastically improving the search and runtime performance for a city-scale robot environment for complex tasks. Moreover, it can be seen that some values of $\gamma$ achieve the optimal cost in a fraction of time and memory as compared to the baseline $( \gamma _ { 1 } , \gamma _ { 2 1 } , \gamma _ { 3 1 } )$ . Increasing this scaling factor further may improve the search time and memory considerably but may worsen the cost incurred $( \gamma _ { 2 2 }$ and γ<sub>32</sub>).

## C. Runtime analysis

Randomized locations For a 50x50 grid environment and $\phi = \mathbf { F } a \wedge \mathbf { F } b \wedge \mathbf { F } c \wedge \mathbf { F } d \wedge \mathbf { F } e$ , and $\gamma = 4 ,$ , we vary the number of locations of each type (atomic proposition) and randomly assign minimum 1 and maximum 4 instances of each label. This gives rise to multiple possible paths that satisfy ϕ with varying path lengths. The results are shown in Fig. 5(a). For some problem instances, our approach chooses the labeled states in the environment that can be reached faster, albeit at a slightly higher cost.

![](Kamale2025Abased_figs/f94c02dee3147e1db891b4ad11ba1727af079c0ee884598d44dc6b3c948d17fb.jpg)  
Fig. 6. Relative error between the cost for the proposed heuristic and the optimal cost

Environment size For the same $\phi$ and $\gamma = 1 0 ,$ , we vary the environment size from a 25 states to 30000 states. The scaling factor is substantially smaller due to simpler structure of the specification. The improvement in runtime (and reduction of nodes explored) increases consistently with the increasing environment size and is more pronounced for larger environments as shown in Fig. 5(b). Notably, except for a few cases between $\vert X \vert \ : = \ : 5 0 0 0$ and $| X | = 1 0 0 0 0 ,$ the proposed heuristic achieves the optimal cost across all remaining instances.

## D. Empirical study on bounded suboptimality

We consider a 100x100 grid environment wherein a robot is tasked to perform $\phi = ( \mathbf { F } a \wedge ( \mathbf { F } ( b \wedge \mathbf { F } c ) ) \wedge ( \mathbf { F } ( d \wedge \mathbf { F } e ) ) \wedge$ $\mathbf { F } h \wedge ( \neg i \mathcal { U } h ) )$ . Varying $\gamma$ from 0 to 30000, we compare the relative error $\Delta$ in cost $\hat { J } ( \mathbf { x } )$ between the baseline and proposed approaches where $\Delta \mathit { \Psi } = \mathit { \Psi } ( \hat { J } _ { h } \ - \ \hat { J } _ { h _ { 0 } } ) / \hat { J } _ { h _ { 0 } }$ . The results are depicted in Fig. 6. This study underscores that the suboptimality of the proposed heuristic is bounded and the approximate empirical bound is $\hat { J } _ { h } \leq 1 . 5 \hat { J } _ { h _ { 0 } }$

## V. CONCLUSION

This work presents an A<sup>∗</sup>-based search algorithm for planning for temporal logic tasks and user preferences for relaxation to address potential infeasibilities. The proposed approach avoids explicit product construction and instead implicitly searches through the reachable solution space. To facilitate this search, we propose an efficient, practicable heuristic that informs the search based on the distance from satisfaction with respect to the relaxed TL task. The proposed heuristic significantly reduces memory usage and runtime while achieving near-optimal costs. We provide runtime analysis and empirical suboptimality bounds. Future work will focus on a deeper investigation of the algorithm’s theoretical properties and rigorous suboptimality bounds.

## REFERENCES

[1] G. E. Fainekos, H. Kress-Gazit, and G. J. Pappas, “Hybrid controllers for path planning: A temporal logic approach,” in Proceedings of the 44th IEEE Conference on Decision and Control. IEEE, 2005, pp. 4885–4890.

[2] C. I. Vasile and C. Belta, “Sampling-based temporal logic path planning,” in 2013 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE, 2013, pp. 4817–4822.

[3] L. Lindemann and D. V. Dimarogonas, “Robust control for signal temporal logic specifications using discrete average space robustness,” Automatica, vol. 101, pp. 377–387, 2019.

[4] S. L. Smith, J. Tumova, C. Belta, and D. Rus, “Optimal path planning for surveillance with temporal-logic constraints,” The International Journal of Robotics Research, vol. 30, no. 14, pp. 1695–1708, 2011.

[5] C.-I. Vasile, J. Tumova, S. Karaman, C. Belta, and D. Rus, “Minimumviolation scltl motion planning for mobility-on-demand,” in 2017 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2017, pp. 1481–1488.

[6] D. Kamale, E. Karyofylli, and C.-I. Vasile, “Automata-based optimal planning with relaxed specifications,” in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2021, pp. 6525–6530.

[7] G. A. Cardona and C.-I. Vasile, “Partial satisfaction of signal temporal logic specifications for coordination of multi-robot systems,” in International Workshop on the Algorithmic Foundations of Robotics. Springer, 2022, pp. 223–238.

[8] K. Leung, N. Arechiga, and M. Pavone, “Backpropagation through ´ signal temporal logic specifications: Infusing logical structure into gradient-based methods,” The International Journal of Robotics Research, vol. 42, no. 6, pp. 356–370, 2023.

[9] M. Cai, E. Aasi, C. Belta, and C.-I. Vasile, “Overcoming exploration: Deep reinforcement learning for continuous control in cluttered environments from temporal logic specifications,” IEEE Robotics and Automation Letters, vol. 8, no. 4, pp. 2158–2165, 2023.

[10] M. Lahijanian, S. B. Andersson, and C. Belta, “Temporal logic motion planning and control with probabilistic satisfaction guarantees,” IEEE Transactions on Robotics, vol. 28, no. 2, pp. 396–409, 2011.

[11] H. Rahmani, A. N. Kulkarni, and J. Fu, “Probabilistic planning with partially ordered preferences over temporal goals,” in 2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, pp. 5702–5708.

[12] C.-I. Vasile, D. Aksaray, and C. Belta, “Time window temporal logic,” Theoretical Computer Science, vol. 691, pp. 27–54, 2017.

[13] P. Amorese and M. Lahijanian, “Optimal cost-preference trade-off planning with multiple temporal tasks,” in 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2023, pp. 2071–2077.

[14] Y. Wang, Y. Yuan, H. Wang, X. Zhou, C. Mu, and G. Wang, “Constrained route planning over large multi-modal time-dependent networks,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 313–324.

[15] Y. Kantaros and M. M. Zavlanos, “Stylus\*: A temporal logic optimal control synthesis algorithm for large-scale multi-robot systems,” The International Journal of Robotics Research, vol. 39, no. 7, pp. 812– 836, 2020.

[16] M. Likhachev, G. J. Gordon, and S. Thrun, “Ara\*: Anytime a\* with provable bounds on sub-optimality,” Advances in neural information processing systems, vol. 16, 2003.

[17] D. Khalidi, D. Gujarathi, and I. Saha, “T: A heuristic search based path planning algorithm for temporal logic specifications,” in 2020 IEEE International Conference on Robotics and Automation (ICRA), 2020, pp. 8476–8482.

[18] S. Bhattacharya, M. Likhachev, and V. Kumar, “Multi-agent path planning with multiple tasks and distance constraints,” in 2010 IEEE International Conference on Robotics and Automation. IEEE, 2010, pp. 953–959.

[19] I. Pohl, “Heuristic search viewed as path finding in a graph,” Artificial intelligence, vol. 1, no. 3-4, pp. 193–204, 1970.

[20] A. Felner, S. Kraus, and R. E. Korf, “Kbfs: K-best-first search,” Annals of Mathematics and Artificial Intelligence, vol. 39, pp. 19–39, 2003.

[21] R. Ebendt and R. Drechsler, “Weighted a search–unifying view and application,” Artificial Intelligence, vol. 173, no. 14, pp. 1310–1342, 2009.

[22] D. Kamale and C.-I. Vasile, “Optimal control synthesis with relaxed global temporal logic specifications for homogeneous multi-robot teams,” arXiv preprint arXiv:2406.01848, 2024.

[23] C. Baier and J.-P. Katoen, Principles of model checking. MIT press, 2008.

[24] T. Wongpiromsarn, U. Topcu, and R. M. Murray, “Receding horizon temporal logic planning,” IEEE Transactions on Automatic Control, vol. 57, no. 11, pp. 2817–2830, 2012.

[25] O. Kupferman and M. Y. Vardi, “Model checking of safety properties,” Formal methods in system design, vol. 19, pp. 291–314, 2001.

[26] A. Duret-Lutz, A. Lewkowicz, A. Fauchille, T. Michaud, E. Renault, and L. Xu, “Spot 2.0 — a framework for LTL and ω-automata manipulation,” in Proceedings of the 14th International Symposium on Automated Technology for Verification and Analysis (ATVA’16), ser. Lecture Notes in Computer Science, vol. 9938. Springer, Oct. 2016, pp. 122–129.

[27] G. Boeing, “Osmnx: A python package to work with graphtheoretic openstreetmap street networks,” Journal of Open Source Software, vol. 2, no. 12, p. 215, 2017. [Online]. Available: https://doi.org/10.21105/joss.00215