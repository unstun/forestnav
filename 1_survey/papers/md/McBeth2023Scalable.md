---
citation_key: McBeth2023Scalable
arxiv_id: 2311.10176
arxiv_url: https://arxiv.org/abs/2311.10176
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:11:16Z
origin: ai+web
reviewed: false
---

# Introduction

Multi-robot systems are becoming increasingly prevalent in settings like warehouses and factories. These often constrained environments require careful yet computationally fast motion planning for each robot to accomplish its task without collision. Some navigation approaches compute individual decoupled paths for each robot and resolve conflicts online [@sl-uppccdpmrs-2002]; however, in congested environments, this introduces the risk of deadlock. Alternatively, *coupled* offline multi-robot motion planning (MRMP) approaches [@sl-uppccdpmrs-2002] plan for all robots together in the *composite space*, the joint planning space of all robots. While these methods provide the high level of coordination required to solve difficult problems, due to the large size of the search space, they are computationally intractable for large robot teams. *Hybrid* methods [@smsa-romrmpucbs-21; @wc-mcmppapb-2011; @hpksga-tpqs-2018] seek to combine the benefits of decoupled and coupled planning, providing an increased level of coordination when necessary while also maintaining scalability. While existing approaches [@smqma-arc-24; @wkc-pppfmrwse-12] reactively provide coordination after conflicts occur during planning, our proposed method aims to improve efficiency by predicting when coordination between robots is necessary.

To model when coordination between robots is needed, we build our method off of the Decomposable State Space Hypergraph (DaSH) [@mcbma-hbmrtamp-23] framework. DaSH presents a general structure for hybrid planning that benefits from a sparse high-level representation of the task space that composes robots into the same planning space when necessary and allows the planner to stay in low-dimensional search spaces when possible. This representation directs the construction of a motion solution. DaSH proposes an approach to exhaustively constructing the high-level representation that performs well for problems like multi-manipulator rearrangement [@mcbma-hbmrtamp-23], where the task space has an exploitable structure since actions can be classified as pick, place, handoff, etc., but becomes intractable for problems which lack this highly structured task space. Because of this, we cannot directly apply DaSH to mobile robot motion planning.

![A comparison of the DaSH framework and Workspace Guided-DaSH showing an example task space hypergraph for each. Hypergraph vertices show which robots and/objects are present in that task space element. (left) DaSH's exhaustive construction of the task space hypergraph for a multi-manipulator rearrangement with two robots and one object. (right) Our method uses workspace guidance to induce structure onto problems that lack this natural structure, which makes construction of a minimal portion of the task space hypergraph possible. Here, robots are composed into the same planning space based on their movement along a topological skeleton (details in Sec. [3](#sec:method){reference-type="ref" reference="sec:method"}).](figures/dash-vs-gdash-v3.png){#fig:dash-vs-gdash width="98%"}

Here, we propose extending DaSH for mobile robot motion planning in environments with narrow passages, a classical challenge in motion planning exacerbated in the multi-robot setting, where the robots may also have kinodynamic constraints that further complicate planning. Our insight is that we can leverage information about the planning problem to induce this structure while building the high-level representation and further exploit this guidance, in conjunction with a modified conflict resolution scheme, to efficiently search the planning space and support kinodynamic constraints. In mobile robot motion planning, we can effectively use workspace information to provide this guidance [@mmuma-smrmpcetg-23; @dsba-drbrrt-16; @suda-tgrcdrs-20; @rsb-beaeisbmp-2014; @pkv-mpdsclp-10]. As such, we extend the DaSH framework to present *Workspace Guided-DaSH*, a novel method for the problem of multiple mobile robot motion planning in environments with narrow passages. Our contributions include:

- A method that extends the DaSH framework to a multi-robot planning problem without a highly structured task space by leveraging the workspace to guide planning in multiple ways.

- Support for planning under kinodynamic constraints via an adapted conflict resolution structure.

- An extensive experimental validation showing that our novel approach scales to robot groups up to 128, an order of magnitude larger than previous methods.

# Preliminaries and Prior Work

In this section, we describe relevant motion planning preliminaries and discuss prior work in the field of multi-robot motion planning.

## Motion Planning Preliminaries

In motion planning, a *configuration* refers to a set of values for a robot's *degrees of freedom*, including their position in the workspace, orientation, and other parameters such as joint angles. The *configuration space* ($\mathcal{C}_{space}$) consists of all possible configurations and can be partitioned into $\mathcal{C}_{free}$ and $\mathcal{C}_{obst}$ made up of valid and invalid configurations, respectively. Motion planning is the problem of finding a path from a start configuration $q_s$ to a goal configuration $q_g$ through $\mathcal{C}_{free}$. Computing the full $\mathcal{C}_{obst}$ is intractable [@ss-otpmpiigtfctporam-83; @c-crmp-88], thus state-of-the-art methods turned to sampling-based motion planning [@kslo-prpp-96; @l-rrtntpp-1998]. Two commonly used methods, Rapidly-exploring Random Trees (RRT) [@l-rrtntpp-1998] and Probabilistic Roadmaps (PRM) [@kslo-prpp-96] build tree-based and graph-based representations of $\mathcal{C}_{free}$ respectively. These methods have also been extended to problems that require satisfying kinematic and dynamic constraints. Kinodynamic RRT [@hklr-rkmpwmo-02] extends RRT to work with kinodynamic constraints through extensions of randomly sampled control inputs for random durations until a goal region is reached.

## Multi-robot Motion Planning

The MRMP problem is an extension of the motion planning problem that consists of finding valid paths $\Pi = \{\pi_{r_1}, ..., \pi_{r_n}\}$ for a set of robots $R = \{r_1, ..., r_n\}$ that also avoid inter-robot collision. Multi-agent pathfinding (MAPF) is the discrete state space equivalent of the MRMP problem, which consists of finding collision-free paths for a set of robots over a given graph representation (e.g., a grid) rather than through continuous space. In environments with narrow passages, it is non-trivial to construct a graph representation that captures the connectivity of the planning space, hence our consideration of MRMP rather than MAPF.

Some coupled methods, including Composite PRM [@sl-uppccdpmrs-2002] and Composite RRT [@l-rrtntpp-1998], provide a high level of coordination by planning directly in the composite space, $C_0 \times ... \times C_{n-1}$ where $C_i$ is the configuration space of robot $i$. Other coupled methods, including MRdRRT [@ssh-faniaehdrfeoirimm-16] and its variants [@dsshb-sammp-17; @ssdhb-dsaiammp-20], construct single-robot roadmaps and then use these to search an implicit composite space roadmap. Searching the composite space, even implicitly, becomes intractable with large groups of robots due to the high dimensionality of the space.

Hybrid methods alternate between planning in spaces with different compositions of robots. CBS-MP [@smsa-romrmpucbs-21] performs a low-level search to find decoupled paths for each robot and resolves conflicts using a high-level search in the composite space. Kinodynamic Conflict-Based Search (K-CBS) [@kal-cbsfmrmpwkc-22] extends hybrid MRMP algorithms to accommodate kinodynamic constraints, drawing on the concepts of CBS-MP [@smsa-romrmpucbs-21]. Subdimensional Expansion RRT (sRRT) [@wkc-pppfmrwse-12] constructs individual policies by growing RRTs in the $\mathcal{C}_{space}$ of each robot backward from the goal. It then expands a tree forward in the composite space by following the individual policies until conflict occurs. Then, new configurations are sampled for expansion in the composite space of the conflicting robots. While these methods perform well in open environments, in constrained settings, they expend excess computation on conflict resolution, limiting planning efficiency. Adaptive Robot Coordination (ARC) [@smqma-arc-24] plans decoupled paths and then resolves conflicts by solving local subproblems in the composite spaces of the affected robots. Though it does focus computation within constrained settings, it does so reactively and spends excess time adjusting the local problem size to find the right resolution. Its kinodynamic variant [@qsmma-karcfmrkp-2025] similarly resolves collisions and ensures kinodynamic feasibility using trajectory optimization.

## Guided Motion Planning

*Guided* motion planning methods use external information to efficiently find paths. Many single-robot approaches use workspace skeletons, embedded graphs in which edges represent free areas of the workspace and vertices are connections between them. Examples include medial axis skeletons [@Blum_1967_6755] for 2D environments and mean curvature skeletons [@t-mcs-12] for 3D. They are generally quick to compute, for example, medial axis skeletons can be computed in $O(n \log n)$ time where $n$ is the number of obstacle edges [@l-matoaps-1982]. Skeleton-guided planning methods [@dsba-drbrrt-16; @suda-tgrcdrs-20] use dynamic sampling regions, bounded local areas of the workspace that advance along skeleton edges, to explore free areas of the environment, including narrow passages, until a path is found.

Prior work extends skeleton guidance to MRMP for scenarios with narrow passages, which require a high level of coordination during planning. Composite Dynamic Region-biased RRT (CDR-RRT) [@mmuma-smrmpcetg-23] is a coupled method that lazily builds and searches over a *composite skeleton*, which is the Cartesian product graph of the skeleton for each robot in the group. MAPF is used to generate a path over the skeleton for each robot, taking into account each edge's capacity as given by the clearance to obstacles in the environment. These paths are combined to form a path through the composite skeleton. Dynamic sampling regions advance over the composite skeleton edges, growing a tree until the goal is reached. Although CDR-RRT shows a significant improvement in scalability compared to other state-of-the-art methods in environments with narrow passages where coordination between the full robot group is required [@mmuma-smrmpcetg-23], considering the full composite space of all robots incurs significant computational overhead. We propose a hybrid method extended from CDR-RRT that uses topological guidance to inform when planning in the composite space (of all or a subgroup of robots) is necessary.

## Decomposable State Space Hypergraph Framework {#sec:dash}

The Decomposable State Space Hypergraph (DaSH) framework [@mcbma-hbmrtamp-23] for hybrid multi-robot planning leverages a directed hypergraph representation to enable coordination between relevant groups of robots without considering the full composite space unless necessary. A directed hypergraph $\mathcal{H} = (\mathcal{V}, \mathcal{E})$ is a generalization of a graph where hyperarcs $E \in \mathcal{E}$ represent directed connections between sets of vertices. This representation provides the advantage of sparsity. While an equivalent graph could be constructed, vertices would need to represent a state for every robot in the problem, leading to a combinatorial explosion as the number of robots increases. The hypergraph representation, however, only includes relevant robots in each vertex or hyperarc, allowing groups of robots to be composed and decomposed. This is especially beneficial for sampling-based motion planning where the planning time is impacted by the dimension of the $\mathcal{C}_{space}$.

The DaSH framework consists of three components: construction of the *task space hypergraph*, construction of the *motion hypergraph*, and the *query*. The *task space hypergraph*, $\mathcal{H}_{ts}$, is a high-level representation of the task space that captures when coordination between robots is required. allowing robots to move between planning spaces with different compositions of robots at different stages of planning. In DaSH, these planning spaces, which are represented by the vertices of the task space hypergraph, are referred to as *task space elements*. Task space elements are made up of a set of relevant robots and constraints (e.g., start/goal constraints, path constraints). The DaSH framework has been implemented for problems including multi-manipulator rearrangement [@mcbma-hbmrtamp-23] where the task space is highly structured and easily discretizable with task space elements representing modes such as a robot holding an object. This structure allows the sparse task space hypergraph to be constructed exhaustively. For task spaces without such structure, however, this exhaustive construction becomes intractable.

The task space hypergraph is used to build a low-level *motion hypergraph*, $\mathcal{H}_{m}$, encoding motion paths. Here, vertices represent configurations and hyperarcs represent local paths between them. The query phase consists of two parts. First, an *optimistic solution* on the motion hypergraph is found which ensures a valid transition history (i.e., guaranteeing that each robot exists in exactly one place at each point along the solution). Second, because hyperarcs in the motion hypergraph give a local plan for the subset of robots in the group being considered and do not make assumptions about the locations of the other robots, a scheduled query must then be used to validate the solution in terms of inter-robot collisions by inducing waiting.

Considering extending DaSH to a problem without a naturally highly structured task space, each of these components poses a design question, which we discuss in Section [3](#sec:method){reference-type="ref" reference="sec:method"}. Additionally, we discuss the modifications to the conflict resolution structure that we make to accommodate kinodynamic planning since we can no longer assume the robots are able to instantaneously change velocity in the scheduled query. These changes allow us to bypass the query stage entirely.

:::: algorithm
::: algorithmic
Workspace Skeleton $S$, Query $Q$ $\Pi \gets \emptyset$ $C \gets \emptyset$ $\Pi^S \gets \textsc{MAPF}(S, C, Q)$ []{#line:mapf label="line:mapf"} $\mathcal{H}_{ts} \gets \textsc{ConstructTaskSpaceHypergraph}(\Pi^S)$[]{#line:hts label="line:hts"} $\mathcal{X}_{ts} \gets \textsc{OrderByDependency}(\mathcal{H}_{ts})$[]{#line:order label="line:order"} $\mathcal{H}_m \gets \emptyset$ $\pi \gets \textsc{ComputePath}(G, x_{ts})$[]{#line:plan label="line:plan"} $C \gets C \cup \textsc{GetConstraint}(x_{ts})$[]{#line:fail label="line:fail"} **break** $\mathcal{X}_{conf} \gets \textsc{FindCollisions}(\mathcal{H}_m, \pi)$[]{#line:findcollision label="line:findcollision"} $C \gets C \cup \textsc{GetConstraints}( \mathcal{X}_{conf} \cup \{x_{ts}\})$[]{#line:getconstraints label="line:getconstraints"} **break** $\mathcal{H}_m.\textsc{AddPath}(\pi)$[]{#line:buildhm label="line:buildhm"} $\Pi \gets \textsc{ExtractMotionPaths}(\mathcal{H}_m)$[]{#line:extract label="line:extract"}
:::
::::

# Workspace Guided-DaSH Method {#sec:method}

In this section, we propose the Workspace Guided-DaSH method, which leverages the workspace skeleton to guide both the construction of $\mathcal{H}_{ts}$ and its translation into $\mathcal{H}_m$. Fig. [1](#fig:dash-vs-gdash){reference-type="ref" reference="fig:dash-vs-gdash"} compares the DaSH framework with our method, which we elaborate on below.

## Problem Formulation

We consider the problem of multiple mobile robot motion planning in congested environments with narrow passages. Given a set of $n$ robots, a set of start and goal configurations, $q_s^i~\forall i \in [1, n]$ and $q_g^i~\forall i \in [1, n]$ respectively, we aim to find a path for each robot $\pi^i~\forall i \in [1, n]$ that satisfies the criteria that $\pi^i_0 = q_s^i~\forall i \in [1, n]$ and $\pi^i_T = q_g^i~\forall i \in [1, n]$ where $\pi^i_t$ represents the path configuration at time $t$ and $T$ is the final timestep. Additionally, these paths must be inter-robot collision free. We consider two path configurations to be in collision if the geometry of the robots at these configurations intersect. Our planner is generic and we do not make assumptions about robot geometry or kinematics. We assume a known environment and precompute a workspace skeleton representation.

## High Level Task Space Hypergraph Construction

Constructing $\mathcal{H}_{ts}$ requires knowledge about the problem space to make composition decisions about when coordination between robots is required during planning and the relevant path constraints.

Considering mobile robots, coordination between robots' motions is required when they are physically near each other. Our insight is that we can leverage the skeleton to approximate when coordination is needed by modeling the movement of the robots through the workspace as movement along the skeleton. Specifically, coordination is needed when robots are traversing the same skeleton edge (either in the same or opposite direction) or traveling through the same skeleton vertex. This formulation imposes a structure on the search space.

Workspace Guided-DaSH follows the structure shown in Alg. [\[alg:guided-dash\]](#alg:guided-dash){reference-type="ref" reference="alg:guided-dash"}. Given a workspace skeleton, we first conduct a heuristic search to find a path over the skeleton for each robot using a MAPF algorithm [@ssfs-cbsfomap-15] (line [\[line:mapf\]](#line:mapf){reference-type="ref" reference="line:mapf"}). We set the capacity of each skeleton vertex and edge as given by the minimum clearance to an obstacle. We then combine these paths to form the minimal necessary portion of $\mathcal{H}_{ts}$ (line [\[line:hts\]](#line:hts){reference-type="ref" reference="line:hts"}). Fig. [2](#fig:comp-arcs){reference-type="ref" reference="fig:comp-arcs"} shows an example of the conversion of the MAPF solution into $\mathcal{H}_{ts}$. Within task space elements, constraints represent the skeleton segments that each robot must traverse at that stage. Robots traversing the same skeleton edge are grouped into the same task space element. As robots move away from each other to different edges, they are decoupled into separate task space elements, boosting planning efficiency by considering smaller $\mathcal{C}_{spaces}$.

:::: {#fig:comp-arcs .figure}
\

::: caption
\(a\) A segment of the robot paths over the skeleton (gray) and (b) the corresponding portion of the task space hypergraph. Each task space element (circle) shows the corresponding set of robots and the relevant portion of the workspace skeleton. In (b), arrows indicate robots moving along a skeleton edge and dots indicate a decoupled intermediate state. The green and red robots are initially moving in opposite directions along the same skeleton edge. Then, red and blue reach the skeleton vertex together and go on to different edges. The yellow robot begins moving in the opposite direction of the red robot when the red robot reaches the next skeleton edge.
:::
::::

## Translation to Low-level Motion Hypergraph {#sec:ll_motion}

The motion hypergraph $\mathcal{H}_m$ stores the configurations and motions between them that make up the robots' paths through the task space elements and hyperarcs from $\mathcal{H}_{ts}$. For each task space element and hyperarc $x_{ts} \in \mathcal{V}_{ts} \cup \mathcal{E}_{ts}$, ordered from start to goal (line [\[line:order\]](#line:order){reference-type="ref" reference="line:order"}), a path is computed in the composite space of the robots contained therein (line [\[line:plan\]](#line:plan){reference-type="ref" reference="line:plan"}). These paths become vertices and hyperarcs in $\mathcal{H}_m$. To ensure that the robots roughly follow their paths over the skeleton and that narrow passages in the environment are efficiently traversed, we leverage skeleton guidance during path construction. To compute paths through task space elements, we use the dynamic sampling region advancement procedure from CDR-RRT [@mmuma-smrmpcetg-23].

Considering hyperarcs that represent multiple robots moving through a skeleton vertex, we stop the movement of the robots along the incoming skeleton edges a small distance $\delta$ from the end of each edge to avoid conflicts while moving into the vertex. We've found that setting $\delta$ to the diameter of the region used for the dynamic sampling region advancement works well. We then grow an RRT [@l-rrtntpp-1998] in the composite space of these robots from the last configuration on the robots' incoming skeleton edges to a sampled configuration at least $\delta$ distance away from the skeleton vertex of the robots' next skeleton edges. Here, we simply grow an RRT rather than using CDR-RRT to avoid forcing the robots to reach the skeleton vertex at the same time, creating congestion.

We consider construction of a path to have failed if the RRT fails to be extended a given number of times during planning (line [\[line:fail\]](#line:fail){reference-type="ref" reference="line:fail"}). In this case, we impose a constraint that the MAPF solution from which we build $\mathcal{H}_{ts}$ cannot contain the same group of robots traversing along either a skeleton edge that failed or the same groups of robots traversing along the incoming or outgoing skeleton edges to a skeleton vertex that failed. We then recompute $\mathcal{H}_{ts}$ (line [\[line:hts\]](#line:hts){reference-type="ref" reference="line:hts"}) and try again to construct $\mathcal{H}_m$.

Since we know from the heuristic search over the skeleton which task space elements' motions occur concurrently, we can interleave motion hypergraph construction and conflict detection. By finding conflicts between different task space elements as they occur, we minimize wasted computation and can directly extract the motion solution from the motion hypergraph, bypassing DaSH's query stage. As we construct $\mathcal{H}_m$, after each path is computed, we check for collisions with existing paths occurring simultaneously by considering intermediate configurations along the paths (line [\[line:findcollision\]](#line:findcollision){reference-type="ref" reference="line:findcollision"}). If conflicts are found between robots traversing different portions of the skeleton simultaneously, similarly to the constraints added when path construction fails, MAPF constraints are imposed to prevent the relevant robot groups from traversing these segments of the skeleton together (line [\[line:getconstraints\]](#line:getconstraints){reference-type="ref" reference="line:getconstraints"}).

Our modification to the conflict resolution stage also allows us to support kinodynamic planning. The scheduled query proposed in the original DaSH framework resolves conflicts by inducing waiting to prevent robots from colliding with each other. When planning under kinodynamic constraints, we cannot assume the ability of robots to instantaneously change velocity. Additionally, to avoid solving computationally difficult optimal control point-to-point problems, we cannot reuse paths for task space elements occurring after conflicts in the robots' paths. Thus, we must replan affected paths to avoid conflicts.

After new MAPF constraints are added, the heuristic search recomputes $\mathcal{H}_{ts}$ (line [\[line:hts\]](#line:hts){reference-type="ref" reference="line:hts"}), and construction of $\mathcal{H}_m$ restarts. This process continues until a conflict-free motion solution is found (lines [\[line:buildhm\]](#line:buildhm){reference-type="ref" reference="line:buildhm"}- [\[line:extract\]](#line:extract){reference-type="ref" reference="line:extract"}).

## Kinodynamic Planning {#sec:k-wg-dash}

As kinodynamic constraints influence the motion of the robots, it is imperative that the low-level motion hypergraph, $\mathcal{H}_m$, incorporates the kinodynamic constraints during construction. This is achieved by substituting the underlying RRT with Kinodynamic RRT [@hklr-rkmpwmo-02].

A control input is generated by sampling the control space uniformly at random, which is then integrated forward during the RRT extension phase for a randomly sampled duration. In order to utilize the guidance provided by the CDR-RRT, we generate and integrate forward many random control inputs and select the input that moves the system closest to the dynamic sampling region. The kinodynamic RRT continues to expand until either a maximum number of states have been added, a failure, or the goal region has been reached.

:::: {#fig:exps .figure}
::: caption
\(a\) In the Warehouse environment, robots located on the top and bottom of each narrow aisle must swap places with the robot they are vertically aligned with. (b) In the Tunnels environment, robots must find and traverse multiple tunnels while moving from start positions in the back tunnel to goal positions in the front tunnel. (c) In the mining environment, robots must swap places with another robot located in an adjacent mine shaft, robot start positions are located at the front of the tunnels and at intersections between tunnels. (d-e) In the GridMaze environment, robots must move between randomly located starts (red) and goals (blue) within the maze, some of which overlap.
:::
::::

# Validation

We run scaling MRMP scenarios in environments designed to highlight the strengths and weaknesses of Workspace Guided-DaSH (abbreviated *WG-DaSH* in results) relative to other state-of-the-art approaches.

## Experimental Setup

We measure the performance of Workspace Guided-DaSH against CDR-RRT [@mmuma-smrmpcetg-23] as well as a set of other relevant approaches. Composite RRT [@l-rrtntpp-1998] operates in the full composite space, providing high coordination. MRdRRT [@ssh-faniaehdrfeoirimm-16] was originally intended for manipulators, but its implicit search of the composite space makes it pertinent for comparison. sRRT [@wkc-pppfmrwse-12] uses subdimensional expansion to limit the size of the search space which is similar in concept to our hypergraph representation. ARC [@smqma-arc-24] composes robots into higher-dimensional planning spaces based on encountered conflicts, whereas our method uses workspace guidance to preemptively avoid likely conflicts. Thus, comparing our method against ARC effectively measures the impact of this guidance. Each method was implemented in an open-source library and code will be provided in the final manuscript. In all environments, we find plans for holonomic robots considering only geometric feasibility, deferring kinodynamic feasibility to a post-processing trajectory optimization step. In the Warehouse environment, we additionally incorporate kinodynamic constraints into planning. We run 15 seeds for each scenario. Each method is given 600 seconds to solve a scenario or is considered a failure. We report planning time as well as path cost given by the makespan.

::: {#tab:warehouse}
+--------------------------------------------------------------------------+------------+----------------------+-------------------+-------------+
| **Method**                                                               | **Robots** | **Runtime (s)**      | **Cost (s)**      | **Success** |
+:=========================================================================+:==========:+==========:+=========:+========:+========:+============:+
| 3-6                                                                      |            | **Avg**   | **Std**  | **Avg** | **Std** |             |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| **WG-DaSH**                                                              | 2          | **0.7**   | **0.3**  | 31.6    | 4.4     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 1.5       | 0.8      | 22.3    | 2.6     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 9.6       | 15.3     | 22.4    | 5.3     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 3.4       | 3.7      | 29.8    | 9.5     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 Comp. RRT                                                            |            | 22.6      | 24.2     | 25.7    | 12.2    | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 MRdRRT                                                               |            | 21.6      | 26.4     | 82.1    | 35.2    | 53.3%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 4          | **1.8**   | **0.6**  | 32.8    | 3.2     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 2.4       | 1.0      | 27.6    | 6.7     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 16.7      | 18.9     | 22.8    | 7.9     | 93.3%       |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 14.7      | 9.6      | 33.2    | 18.9    | 86.7%       |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 Comp. RRT                                                            |            | 274.0     | \-       | 19.2    | \-      | 6.7%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 MRdRRT                                                               |            | 295.0     | 233.4    | 107.1   | 77.4    | 20.0%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 8          | **4.6**   | **3.2**  | 32.5    | 3.0     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 23.0      | 8.2      | 42.2    | 7.5     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 37.7      | 49.6     | 21.0    | 0.9     | 80.0%       |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 61.4      | 40.1     | 20.9    | 0.3     | 13.3%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 16         | **9.5**   | **2.1**  | 31.4    | 3.4     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 288.1     | 100.2    | 50.1    | 7.1     | 93.3%       |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 97.1      | 188.5    | 20.7    | 0.6     | 60.0%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 32         | **29.5**  | **5.8**  | 34.3    | 4.0     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 72.4      | 7.1      | 20.9    | 0.7     | 26.6%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 64         | **54.1**  | **11.4** | 35.6    | 2.7     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 128        | **250.7** | **29.4** | 36.6    | 5.0     | 60.0%       |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+

: Warehouse results. Data omitted where all seeds failed
:::

## Environments

Here, we describe our experimental environments and explain which aspects of our approach they highlight.

### Warehouse (Fig. [\[fig:warehouse\]](#fig:warehouse){reference-type="ref" reference="fig:warehouse"}) {#sec:warehouse-setup}

The Warehouse environment features narrow aisles through which the robots must swap places. In the holonomic scenario, the width of the narrow passages is 2.5 times the diameter of the disk robots we consider. We additionally run a kinodynamic variant with doubled aisle widths. This scenario measures each approach's ability to efficiently handle narrow passages within the environment. We highlight Workspace Guided-DaSH's ability to decompose the problem using topological guidance.

### Tunnels (Fig. [\[fig:tunnels\]](#fig:tunnels){reference-type="ref" reference="fig:tunnels"})

The Tunnels environment again features narrow passages. Because of the 3D workspace, the planning space becomes very large. This scenario is intended to measure each algorithm's performance with respect to the geometric complexity, rather than the congestion, of the environment. We consider L-shaped robots with the width of their longest dimension slightly less than half the width of the narrow passages. Each robot must find and traverse multiple narrow passages to reach its goal, but its shortest path does not conflict with any other robot's.

::: {#tab:tunnels}
+--------------------------------------------------------------------------+------------+----------------------+-------------------+-------------+
| **Method**                                                               | **Robots** | **Runtime (s)**      | **Cost (s)**      | **Success** |
+:=========================================================================+:==========:+==========:+=========:+========:+========:+============:+
| 3-6                                                                      |            | **Avg**   | **Std**  | **Avg** | **Std** |             |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| **WG-DaSH**                                                              | 2          | **4.2**   | **0.9**  | 166.0   | 5.1     | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 6.2       | 1.1      | 140.6   | 11.2    | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 129.6     | 175.0    | 175.3   | 26.1    | 40.0%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 4          | **8.2**   | **1.0**  | 158.3   | 9.0     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 17.3      | 3.3      | 152.9   | 16.4    | 100%        |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 327.0     | \-       | 161.7   | \-      | 6.7%        |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 8          | **14.1**  | **2.4**  | 159.8   | 8.4     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 36.0      | 6.8      | 156.1   | 9.0     | 100%        |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 16         | **22.5**  | **1.9**  | 164.8   | 9.4     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 73.1      | 8.5      | 163.9   | 16.7    | 100%        |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 32         | **54.0**  | **6.2**  | 163.0   | 8.0     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+            +-----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 252.6     | 10.0     | 159.8   | 4.7     | 93.3%       |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 64         | **132.4** | **7.0**  | 163.1   | 6.0     | 100%        |
|                                                                          |            |           |          |         |         |             |
| **WG-DaSH**                                                              |            |           |          |         |         |             |
+--------------------------------------------------------------------------+------------+-----------+----------+---------+---------+-------------+

: Tunnels results. Data omitted where all seeds failed
:::

### Mining (Fig. [\[fig:mining\]](#fig:mining){reference-type="ref" reference="fig:mining"})

The Mining environment is a 3D environment meant to mimic a set of mine shafts. Again, it features narrow passages; however, here robots must move in close proximity to each other. We use the same robots as the Tunnels environment. We show that Workspace Guided-DaSH is capable of efficiently finding paths for large robot teams in problems representative of real-world scenarios.

### GridMaze (Fig. [\[fig:gridmaze\]](#fig:gridmaze){reference-type="ref" reference="fig:gridmaze"})

The GridMaze environment is a 3D environment featuring several intersecting narrow tunnels intended to elicit high congestion for large groups of robots in addition to geometric complexity. We use a rectangular prism robot whose smallest dimension is slightly less than half the width of the narrow passages. We demonstrate Workspace Guided-DaSH's ability to efficiently find paths for large groups of robots in these congested settings.

::: {#tab:mining}
+--------------------------------------------------------------------------+------------+---------------------+-------------------+-------------+
| **Method**                                                               | **Robots** | **Runtime (s)**     | **Cost (s)**      | **Success** |
+:=========================================================================+:==========:+=========:+=========:+========:+========:+============:+
| 3-6                                                                      |            | **Avg**  | **Std**  | **Avg** | **Std** |             |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| **WG-DaSH**                                                              | 2          | **1.3**  | **0.3**  | 125.6   | 6.5     | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 1.9      | 0.4      | 113.0   | 11.7    | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 146.8    | 161.7    | 131.5   | 17.5    | 33.3%       |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 4          | **2.4**  | **0.5**  | 122.6   | 10.6    | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 16.0     | 6.1      | 151.2   | 19.5    | 100%        |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 8          | **5.0**  | **0.8**  | 132.2   | 6.7     | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 45.7     | 14.8     | 160.6   | 12.9    | 100%        |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 16         | **11.0** | **1.0**  | 130.3   | 5.8     | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 118.9    | 44.3     | 179.0   | 17.5    | 100%        |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 32         | **28.1** | **3.5**  | 127.6   | 6.7     | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 64         | **80.2** | **6.9**  | 124.5   | 4.5     | 86.7%       |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+

: Mining results. Data omitted where all seeds failed
:::

## Experimental Results

In the Warehouse scenario (Tab. [1](#tab:warehouse){reference-type="ref" reference="tab:warehouse"}), all methods except MRdRRT achieve a 100% success rate in the 2-robot scenario. However, the methods that do not leverage guidance begin to struggle with the 4-robot scenario and multiple cannot solve the 8-robot scenario. Of those, only ARC is able to solve up to the 32-robot scenario; however, with a success rate of only 26.6%. CDR-RRT and sRRT are able to solve up to the 8-robot scenario where the exponential size of the composite space leads to a significant decrease in performance. Workspace Guided-DaSH, like CDR-RRT, sees the benefit of using the skeleton representation to guide planning through narrow passages and the coordination provided by using the composite space of multiple robots. Additionally, by using the workspace to inform the planner when to move between different levels of composition, Workspace Guided-DaSH is able to focus planning within smaller spaces than CDR-RRT, making it able to plan for significantly larger robot teams, up to 128 robots, within the 600-second time limit. In this largest 128 robot scenario, the runtime of our MAPF heuristic was $16.7 \pm 6.4$ seconds, demonstrating that it maintains scalability for large robot groups as well.

In the Tunnels environment (Tab. [2](#tab:tunnels){reference-type="ref" reference="tab:tunnels"}), the size of the search space is increased significantly relative to the Warehouse environment since the robot now has six degrees of freedom. Composite RRT, MRdRRT, and ARC fail to solve the 2-robot scenario due to the complexity of the environment. sRRT performs better because of its ability to decompose the search space, but struggles with narrow passages and only one seed was able to solve the 4-robot scenario. Here, the narrow passage problem is exacerbated since the query requires the planner to find and traverse multiple narrow passages. By leveraging skeleton guidance, CDR-RRT and Workspace Guided-DaSH are able to find solutions for larger groups of robots. Searching the composite space hinders CDR-RRT's performance, leaving it unable to solve the 64-robot scenario within the time limit. Workspace Guided-DaSH is able to efficiently find solutions for up to 64 robots within the time limit due to its ability to decompose the planning space.

::: {#tab:gridmaze}
+--------------------------------------------------------------------------+------------+---------------------+-------------------+-------------+
| **Method**                                                               | **Robots** | **Runtime (s)**     | **Cost (s)**      | **Success** |
+:=========================================================================+:==========:+=========:+=========:+========:+========:+============:+
| 3-6                                                                      |            | **Avg**  | **Std**  | **Avg** | **Std** |             |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| **WG-DaSH**                                                              | 2          | **0.3**  | **0.04** | 44.0    | 5.5     | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 1.0      | 0.3      | 63.9    | 8.3     | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 146.4    | 78.2     | 25.7    | 2.0     | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 4.7      | 4.8      | 30.7    | 3.8     | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 Comp. RRT                                                            |            | 425.0    | 136.0    | 59.4    | 11.5    | 20.0%       |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 4          | **1.0**  | **0.5**  | 44.2    | 3.8     | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 CDR-RRT                                                              |            | 46.0     | 17.7     | 120.6   | 15.9    | 100%        |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 215.2    | 137.6    | 26.3    | 2.1     | 93.3%       |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 19.2     | 6.0      | 30.9    | 4.1     | 100%        |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 8          | **3.2**  | **1.5**  | 42.3    | 3.3     | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 361.4    | 144.2    | 26.4    | 2.6     | 93.3%       |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 25.5     | 10.6     | 32.8    | 9.7     | 100%        |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 16         | **3.8**  | **1.6**  | 44.2    | 4.1     | 100%        |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 ARC                                                                  |            | 437.0    | 55.9     | 26.0    | 1.9     | 40.0%       |
+--------------------------------------------------------------------------+            +----------+----------+---------+---------+-------------+
| 1-1 sRRT                                                                 |            | 38.1     | 10.8     | 29.3    | 2.6     | 100%        |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 32         | **25.5** | **7.9**  | 36.3    | 16.4    | 93.3%       |
|                                                                          |            |          |          |         |         |             |
| **WG-DaSH**                                                              |            |          |          |         |         |             |
+--------------------------------------------------------------------------+------------+----------+----------+---------+---------+-------------+

: GridMaze results. Data omitted where all seeds failed
:::

In the Mining environment (Tab. [3](#tab:mining){reference-type="ref" reference="tab:mining"}), Composite RRT and MRdRRT fail to solve the 2-robot scenario due to the large size of the search space and inter-robot conflicts. Similar to the Tunnels scenario, ARC's performance is impacted by the environment complexity since it does not use topological guidance and it fails to solve the 2-robot scenario. sRRT struggles to solve the 2-robot scenario and cannot solve the 4-robot scenario. By leveraging topological guidance to limit exploration of the composite space, CDR-RRT is able to solve up to the 16-robot scenario. However, it is unable to solve the 32-robot scenario. Workspace Guided-DaSH, by considering the composite space only when necessary, is able to efficiently solve up to the 64-robot scenario.

In the 3D GridMaze scenario (Tab. [4](#tab:gridmaze){reference-type="ref" reference="tab:gridmaze"}), as a result of the large size of the planning space as well as the difficulty posed by the long curved narrow passages, Composite RRT struggles with the 2-robot scenario and fails to solve the 4-robot scenario. MRdRRT fails to solve the 2-robot scenario. While CDR-RRT is able to solve the 4-robot scenario, the large size of the composite space prevents it from solving the 8-robot scenario within the time limit. sRRT and ARC benefit from searching a lower-dimensional space when robots are not in conflict, but fail to solve the 32-robot scenario where conflicts become prevalent due to the high level of congestion of the environment. Similar to sRRT, Workspace Guided-DaSH searches lower-dimensional spaces, however, our method also uses the workspace skeleton for conflict resolution. When a conflict is too difficult to be resolved quickly via random sampling, we impose constraints on the robots' paths over the workspace skeleton which allows us to find conflict-free paths more efficiently. Thus, Workspace Guided-DaSH is able to find solutions up to 32 robots. Although this replanning mechanism sometimes results in slightly higher solution costs relative to other methods, a post-processing trajectory optimization step is generally used in practice to smooth paths.

## Kinodynamic Experiments

To evaluate Workspace Guided-DaSH with kinodynamic constraints, we use Kinodynamic Workspace Guided-DaSH (K-WG-DaSH) incorporating the modifications in Sec. [3.4](#sec:k-wg-dash){reference-type="ref" reference="sec:k-wg-dash"}. We compare our approach to Kinodynamic-CBS [@kal-cbsfmrmpwkc-22] (K-CBS) and Kinodynamic-ARC [@qsmma-karcfmrkp-2025] (K-ARC). K-CBS uses the same Kinodynamic RRT we employ in K-WG-DaSH, however, they utilize a merge bound [@ssfs-macbsfomapp-12] creating composite robots when more coordination is needed. K-ARC uses the same reactive coordination approach employed by ARC, but additionally uses trajectory optimization to ensure kinodynamic feasibility. These allow us to evaluate the benefits of the guidance provided by K-WG-DaSH. Each method was given $45$ minutes to find a solution to planning problems in the warehouse environment, described in Section [4.2.1](#sec:warehouse-setup){reference-type="ref" reference="sec:warehouse-setup"}, using robots with $2$nd-order car dynamics: $$\begin{equation}
    \dot{x} = v \cos{\theta}, \
    \dot{y} = v \sin{\theta}, \
    \dot{\theta} = \frac{v}{l} \tan{\phi}, \
    \dot{v} = a, \
    \dot{\phi} = \gamma \
\end{equation}$$

Results for the kinodynamic warehouse environment are shown in Tab. [5](#tab:kino-warehouse){reference-type="ref" reference="tab:kino-warehouse"}. K-ARC was unable to solve the 2-robot scenario within the time limit and is omitted from Tab. [5](#tab:kino-warehouse){reference-type="ref" reference="tab:kino-warehouse"}. K-ARC struggles in this scenario because of both the large size of the environment and the constrained space in which both robots must move, which make the trajectory optimization problem difficult to solve. K-WG-DaSH finds solutions for problems with up to 6 robots consistently while K-CBS begins to struggle at 4 robots. In the 2-robot scenario, K-WG-DaSH maintains a high success rate with a lower planning time at the expense of a higher path cost as opposed to K-CBS which is inconsistent at finding solutions with a higher planning time but with a lower path cost. We attribute the scalability to the topological guidance provided by K-WG-DaSH.

::: {#tab:kino-warehouse}
+--------------------------------------------------------------------------+------------+------------------------+-------------------+-------------+
| **Method**                                                               | **Robots** | **Runtime (s)**        | **Cost (s)**      | **Success** |
+:=========================================================================+:==========:+===========:+==========:+========:+========:+============:+
| 3-6                                                                      |            | **Avg**    | **Std**   | **Avg** | **Std** |             |
+--------------------------------------------------------------------------+------------+------------+-----------+---------+---------+-------------+
| **K-WG-DaSH**                                                            | 2          | **201.2**  | **119.1** | 46.7    | 9.9     | **93.3%**   |
+--------------------------------------------------------------------------+            +------------+-----------+---------+---------+-------------+
| 1-1 K-CBS                                                                |            | 390.1      | 365.9     | 34.4    | 2.3     | 46.7%       |
+--------------------------------------------------------------------------+------------+------------+-----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 4          | 580.2      | **376.2** | 41.9    | 7.3     | **93.3%**   |
|                                                                          |            |            |           |         |         |             |
| **K-WG-DaSH**                                                            |            |            |           |         |         |             |
+--------------------------------------------------------------------------+            +------------+-----------+---------+---------+-------------+
| 1-1 K-CBS                                                                |            | **445.0**  | 473.3     | 35.1    | 2.7     | 20.0%       |
+--------------------------------------------------------------------------+------------+------------+-----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 6          | 1261.6     | **524.5** | 32.1    | 14.8    | **86.7%**   |
|                                                                          |            |            |           |         |         |             |
| **K-WG-DaSH**                                                            |            |            |           |         |         |             |
+--------------------------------------------------------------------------+            +------------+-----------+---------+---------+-------------+
| 1-1 K-CBS                                                                |            | **56.8**   | \-        | 33.5    | \-      | 6.7%        |
+--------------------------------------------------------------------------+------------+------------+-----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 8          | **2147.2** | **313.1** | 19.1    | 16.0    | **33.3%**   |
|                                                                          |            |            |           |         |         |             |
| **K-WG-DaSH**                                                            |            |            |           |         |         |             |
+--------------------------------------------------------------------------+------------+------------+-----------+---------+---------+-------------+
| ------------------------------------------------------------------------ | 10         | **2544.7** | \-        | 36.5    | \-      | **6.7%**    |
|                                                                          |            |            |           |         |         |             |
| **K-WG-DaSH**                                                            |            |            |           |         |         |             |
+--------------------------------------------------------------------------+------------+------------+-----------+---------+---------+-------------+

: Kinodynamic Warehouse results. Data omitted where all seeds failed
:::

# Conclusion and Future Work

In this work, we present Workspace Guided-DaSH, a novel hybrid MRMP method for environments with narrow passages. Our method builds off of a state-of-the-art hybrid planning framework, DaSH, using workspace guidance to enable its use for a multi-robot planning problem that lacks a highly structured search space. Additionally, we add support for kinodynamic planning via a modified conflict resolution structure, which also boosts the scalability of our method by eliminating unnecessary work when finding motion solutions.

Workspace Guided-DaSH leverages topological guidance in multiple ways, both to move between different levels of composition during planning and to guide sampling through narrow passages in the workspace. By using knowledge of the workspace, our method is able to efficiently find paths for robot groups of size up to an order of magnitude larger than existing state-of-the-art methods. Building off of this work, we plan to explore the use of different kinodynamic low-level motion planners which plan more intelligently for multi-robot systems by interleaving sampling-based planning and trajectory optimization [@moth-ddbcbsfmrkmp-23]. Additionally, we plan to explore using parallel computing to further improve the performance of this method, taking advantage of the hypergraph's ability to naturally decompose the multi-robot planning problems.

[^1]: $^{1}$Courtney McBeth, James D. Motes, Isaac Ngui, Marco Morales, and Nancy M. Amato are with the Parasol Lab, Department of Computer Science, University of Illinois Urbana-Champaign, Champaign, IL 61820 USA `{cmcbeth2, jmotes2, ingui2, moralesa, namato}@illinois.edu`

[^2]: This work was supported in part by the IBM-Illinois Discovery Accelerator Institute and the Center for Networked Intelligent Components and Environments (C-NICE) at the University of Illinois.
