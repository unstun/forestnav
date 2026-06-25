---
citation_key: Leebron2025B4P
arxiv_id: 2504.04598
arxiv_url: "https://arxiv.org/abs/2504.04598"
title: "B4P: Simultaneous Grasp and Motion Planning for Object Placement via Parallelized Bidirectional Forests and Path Repair"
authors_short: "Benjamin H. Leebron et al."
year: 2025
direction_tag: J_homotopy_topology
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:12:39Z
origin: ai+web
reviewed: false
---

# B4P: Simultaneous Grasp and Motion Planning for Object Placement via Parallelized Bidirectional Forests and Path Repair

Benjamin H. Leebron, Kejia Ren, Yiting Chen, and Kaiyu Hang

Abstract— Robot pick and place systems have traditionally decoupled grasp, placement, and motion planning to build sequential optimization pipelines with an assumption that the individual components will be able to work together. However, this separation introduces sub-optimality, as grasp choices may limit, or even prohibit, feasible motions for a robot to reach the target placement pose, particularly in cluttered environments with narrow passages. To this end, we propose a forest-based planning framework to simultaneously find grasp configurations and feasible robot motions that explicitly satisfy downstream placement configurations paired with the selected grasps. Our proposed framework leverages a bidirectional sampling-based approach to build a start forest, rooted at the feasible grasp regions, and a goal forest, rooted at the feasible placement regions, to facilitate the search through randomly explored motions that connect valid pairs of grasp and placement trees. We demonstrate that the framework’s inherent parallelism enables superlinear speedup, making it scalable for applications for redundant robot arms, e.g., 7 DoF, to work efficiently in highly cluttered environments. Extensive experiments in simulation demonstrate the robustness and efficiency of the proposed framework in comparison with multiple baselines under diverse scenarios.

## I. INTRODUCTION

Robot pick and place is a fundamental manipulation skill needed in various application scenarios [1], [2]. To relocate an object to the target pose, such systems are required to: 1) find a feasible grasp configuration; 2) find a feasible placement configuration; and 3) generate a feasible motion plan to connect theses two configurations under kinematic and environmental constraints. Traditionally, these topics have been investigated individually e.g., grasp planning [3]– [5], motion planning [6], and placement planning [7]. More recently, they have been also studied as coupled problems, e.g., motion planning for grasping or placement, and grasping for placement [8], [9].

However, a unified framework that addresses pick, motion, and placement planning simultaneously to ensure that all internal constraints are satisfied is yet to be developed. For example, a planner needs to select a grasp that can pass through all narrow passages through a robot motion to finally reach a selected placement pose. Note that even if both the grasp and placement poses are valid, it is often an issue that there is no robot motion to connect them due to the collisions rendered by the selected grasp. See Fig. 1 for an example.

To this end, we propose B4P (Bidirectionally Picking, Planning, and Placing in Parallel), a joint planning framework for object pick and place in spatially constrained environments. Specifically, the framework first identifies a grasp region – a set of robot configurations that ensure a feasible grasp; and a placement region – a set of configurations that reach the target placement poses. We do not make any assumptions on how such regions can be found so that any existing planner can be used, e.g., [5]. Thereafter, through a sampling-based scheme, the proposed B4P builds a pick forest (with trees rooted inside the identified grasp region) and a place forest (with trees rooted inside the identified placement region), and simultaneously grows those trees bidirectionally to find paired connections between starts and goals. Once a connection is made, a grasp configuration and a placement configuration will be paired, and a complete robot motion will be simultaneously provided.

![](Leebron2025B4P_figs/8212eea8b504662fb5e7a78c4095009e0efe67a65c895338dac4f85c0a65d6a4.jpg)  
Fig. 1: A motivational scenario where the robot is tasked to reposition the target object, the yellow stick, to the shelf. It must pass through a narrow passage and of the three pictured grasps, only the grasp in the center of the object (white) will allow the robot to reach the placement location. However, all grasps are feasible initially, and we must somehow find which initial grasp will allow for the robot to reach the downstream placement location.

Our B4P algorithm design offers an inherent internal structure that can be parallelized to achieve superlinear speedups thanks to its non-deterministic nature of samplingbased algorithms [10]. The framework is also designed to offer application flexiblity, allowing modular integration with any grasp method that can find feasible end-effector poses, and with any placement planning methods that can generate end-effctor or object final poses. In brief, the proposed B4P:

1) finds grasps that are guaranteed to be suitable for downstream placement through narrow passages or in cluttered environments;

2) leverages the parallelizability of forest-based planning and to achieve a superlinear speedup;

3) can smoothly integrate with any grasp planners and placement planners to work with various robots.

## II. RELATED WORKS

1) Grasp and Placement Planning: Grasp planning is a critical component in robot pick and place systems, focusing on determining how the robot’s end-effector should be placed to pick up an object securely. Current research on grasp planning can be roughly divided into two categories: modelbased [11] and data-driven [12]. Model-based methods [5], [13]–[15] rely on prior knowledge of the target object and analytically compute grasp configurations that meet grasp criteria such as force closure. Data-driven approaches [3], [4], [16] aim to derive a direct mapping from visual input to grasp poses from well-annotated datasets. On the other end of the problem spectrum, placement planning has investigated object-centric optimization problems, such as placement stability and functionality, as well as task and environmental constraints [8]. However, it is still an open problem in the field that grasp and placement configurations, when planned separately, are not necessarily connectable with any feasible robot motions.

2) Sampling-based Motion Planning: Motion planning computes a collision-free path in the robot’s configuration space to connect the grasp with the placement configuration in pick and place systems. Sampling-based planners [17] have proven efficient and generalizable in exploring the highdimensional configuration space of manipulators. Significant acceleration can be obtained through parallelism [18]–[22] on both GPU and CPU-based computing. Key properties of sampling-based planners include probabilistic completeness [23] and Voronoi bias [24]. The former ensures that a solution will eventually be found as long as it exists in the search space, while the latter contributes to exploration efficiency in high-dimensional spaces. Based on the advantages of sampling-based approaches, and along with a novel forest-based planning strategy, the proposed B4P can simultaneously pair valid grasp and placement configurations while generating feasible motion plans to connect them.

3) Pick and Place Planning: Pick and place planning in robotics primarily focuses on grasping a target object and relocating it to a specified location. Grasp planning and motion planning are both critical components during this process. Zeng [25] presents a system design solely focusing on multi-modality grasp planning in the Amazon Robotics Challenge. Saut [26] proposes a dual-arm approach to achieve larger workspace. Haustein [8] aims at finding a feasible placement configuration in cluttered environments. While taking placement compatibility into consideration during grasp planning [27], [28], however, a geometrically valid placement configuration might still be unreachable [29] by any collision-free robot motions due to kinematic and environmental constraints. In an effort to unify and integrate these key functionalities, our B4P focuses on building a planning that can be compatible with any existing pick planning and placement planning approaches, while coordinate in the middle to ensure the compatibility of individual solutions.

## III. PRELIMINARIES AND PROBLEM STATEMENT

In this section, we first review the preliminaries of the proposed work, based on which we formulate robot pick and place as a problem of simultaneously finding pick, motion, and placement solutions.

## A. Preliminaries

In this work, we consider the pick and place problem as relocating a target object from a start pose to a target pose through a collision-free robot motion. To unify our planning framework as aforementioned, the grasp configurations, the placement configurations, as well as the robot motion paths are all expressed in the robot configuration space.

The configuration space of a n−DoF robot is denoted by $\mathcal Q \subset \mathbb R ^ { n }$ . The robot’s forward kinematics is denoted by $\Gamma : \mathcal { Q } \mapsto S E ( 3 )$ , such that any valid robot joint configuration $q \in \mathcal { Q }$ can be mapped to an robot end-effector’s pose $x \in S E ( 3 )$ . Accordingly, the inverse kinematics is denoted by $\Gamma ^ { - 1 }$ . Note that these definitions are not limited to arm robots, but also can be applied to any robots that have a controlled end-effector. For example, as shown later in Fig. 3, a mobile robot with a fixed gripper can also map from its base configuration to an end-effector’s pose.

For an object inside the workspace of the robot, let us denote its pose by $x ^ { o b j } \in S E { ( 3 ) }$ , a grasp planner will be able to generate feasible pick configuration relative to $p ^ { o b j }$ Let us denote by $\operatorname { P L A N P I C K } ( \cdot ) : S E ( 3 ) \mapsto \mathcal { Q }$ the function of this planner that generates picking configurations:

$$
q ^ {p i c k} = \mathtt {P L A N P I C K} (x ^ {o b j})\tag{1}
$$

In practice and for many grasp planners, every given $p ^ { o b j }$ can result in 0, 1 or many picking configuration solutions. Without loss of generality, in this work as we focus on building the joint framework for pick, motion, and place planning that is compatible with existing grasp planners, we treat PLANPICK(·) as a sampler that can generate a picking configuration every time it is called. The output configuration can be the same or different across function calls.

Inside the workspace of the robot, let us denote by a region $Y \subset S E ( 3 )$ where the placement of an object is expected. A placement planner, which finds a pose within Y for the object, is denoted as $\operatorname { P L A N P L A C E } ( \cdot ) : S E ( 3 ) \mapsto S E ( 3 )$ to generate a stable placement under given task constraints:

$$
x ^ {p l a c e} = \mathrm{PLANPLACE} (Y)\tag{2}
$$

Similarly to grasp planning, to be compatible with exisiting placement planners, we treat this place planner as a sampler that can generate the same, or different, placement plans every time it is called. Furthermore, to keep our planning framework operating with robot configurations only as afore mentioned, every planned placement pose will be converted to a robot configuration by:

$$
q ^ {p l a c e} = \Gamma^ {- 1} (x ^ {p l a c e} (x ^ {o b j}) ^ {- 1} \Gamma (q ^ {p i c k}))\tag{3}
$$

where the end-effector’s pose at placement calculated by $x ^ { p l a c e } ( x ^ { o b j } ) ^ { - 1 } \Gamma ( q ^ { p i c k } )$ ensures that the grasp on the object has not changed during the robot motion execution.

## B. Trees and Forests

Same as in most sampling-based motion planning approaches, we use trees to represent the exploration of the valid robot configurations and robot motions to connect between them in the configuration space Q. In our bidirectional framework, we denote by $\dot { \mathcal { T } } _ { i } ^ { p i c k }$ a motion tree rooted at the i−th sampled picking configuration, and by $\mathcal { T } _ { j } ^ { p l a c e }$ a motion tree rooted at the j−th sampled placement configuration. We also denote ${ \mathcal { T } } _ { i } ^ { p i c k }$ .pick to be the SE(3) transformation of the gripper relative to the object. In the trees, every node is a collision-free robot configuration and every edge is a collision free path. To enable all trees to simultaneously explore the configuration space and find potential valid pairings between $\mathcal { T } _ { i } ^ { p i c \breve { k } }$ and $\mathcal { T } _ { i } ^ { p l \bar { a } c e }$ , we collect the trees into two motion forests $\mathcal { F } ^ { p i c k } = \bar { \{ T _ { i } ^ { p i c k } \} } _ { i = 1 : n }$ and $\mathcal { F } ^ { p l a c e } = \{ \mathcal { T } _ { j } ^ { p l a c e } \} _ { j = 1 : m } ,$ with n and m trees respectively. While the trees grow from two forests toward each other, only connections between trees from different forests are allowed.

## C. Problem Formulation

The pick, motion, and place planning problem in this work is formalized as follows. Given an object in the robot workspace at $x ^ { o b j }$ , and a placement region Y , find a picking configuration $q ^ { p i c k }$ for $x ^ { o b j }$ , and a robot motion plan $\pi =$ $\{ q ^ { p i c k } , \ldots , q _ { k } , \ldots , q ^ { p l a c e } \}$ , such that:

• the final object pose $x ^ { p l a c e }$ , as calculated by Eq. 3, satisfies $x ^ { p l a c e } \in Y ;$

• all intermidiate robot states $q _ { k }$ together with the object with its in-hand pose determined by $q ^ { p i c k }$ at the beginning will be collision-free.

## IV. METHOD: B4P

We begin this section with an overview of the proposed B4P algorithm and then delve into the details of its key components of forest building and path repair.

## A. Algorithm Overview

In Eq.(3) we can see that a robot configuration $q ^ { p l a c e }$ for placement can be calculated only if the initial picking configuration $q ^ { p i c k }$ is known. While exact pick and place configuration pairing is ensured, this requirement, however, will pose a hard constraint that a pick tree ${ \mathcal { T } } _ { i } ^ { p i c k }$ and a place tree $\dot { T } _ { j } ^ { p l a c e }$ in the forests can be potentially connected only if their roots share the same picking configuration relative to the object, i.e., $\mathcal { T } _ { i } ^ { p i c k } . p i c k \dot { = } \mathcal { T } _ { j } ^ { p l a c \epsilon }$ .pick. As such, the bidirectional forests will be divided by root configurations into sub-forests, and the ability of fully exploring motion possibilities will be significantly reduced.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 The B4P algorithm
Input: Object pose $x^{obj}$, placement region Y, number of pick and place trees $N^{pick}$ and $N^{place}$
Output: Robot motion path $\pi$
1: $\mathcal{F}^{pick}, \mathcal{F}^{place} \leftarrow \text{SPAWNFOREST}(x^{obj}, Y, N^{pick}, N^{place}) \triangleright$ Alg. 2
2: Workers $\leftarrow$ LAUNCHPARAWORKERS($\mathcal{F}^{pick}, \mathcal{F}^{place}$)
3: parfor w $\in$ Workers do $\triangleright$ Parallel Workers
4: if w.BUILDFOREST() then $\triangleright$ Alg. 3
5: $\pi \leftarrow$ w.PATH() $\triangleright$ Initial Path
6: $\pi \leftarrow$ PATHREPAIR($\pi$) $\triangleright$ Alg. 4
7: if $\pi \neq \{\}$ then $\triangleright$ Success
8: Workers.FINISH()
9: end if
10: end if
11: end parfor
12: return $\pi$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 SpawnForest(·)
Input: Object pose  $x^{obj}$ , placement region Y, number of pick and place trees  $N^{pick}$  and  $N^{place}$ 
Output: Pick forest  $F_{pick}$ , place forest  $F_{place}$ 

1:  $F_{pick} \leftarrow \{\}, F_{place} \leftarrow \{\}$ 

2: for  $i = 1, \ldots, N_{pick}$  do

3:  $q_{pick} = \text{PLANPICK}(x^{obj})$ $\triangleright$  Eq. (1)

4:  $F_{pick}.ADDROOT(q_{pick}')$ 

5: end for

6: for  $i = 1, \ldots, N_{place}$  do

7:  $x_{place} = \text{PLANPLACE}(Y)$ $\triangleright$  Eq. (2)

8:  $q_{pick} = \text{PLANPICK}(x^{obj})$ 

9:  $q_{place} = \Gamma^{-1}(x_{place}^{(obj)^{-1}}\Gamma(q_{pick}))$ $\triangleright$  Eq. (3)

10:  $F_{place}.ADDROOT(q_{place}')$ 

11: end for

12: return  $F_{pick}, F_{place}$
</div>

To this end, in our work, as outlined in Alg. 1, in order to facilitate the tree expansion by sufficiently exploring pairings between the two forests, we opt to omit the constraints of an explicit picking configuration for all place trees $\mathcal { T } _ { j } ^ { p l a c e }$ . For this, when a placement pose $x ^ { p l a c e }$ is sampled, a random picking configuration will be assigned to it to compute $q ^ { p l a c e }$ . When our algorithm B4P expands the forests from both sides and tries to make connections, the condition of $\mathcal { T } _ { i } ^ { p i c k } . p i c k ~ = ~ \mathcal { T } _ { j } ^ { p l a c \epsilon }$ .pick is not checked when making connections between pick and place trees. Once a connection is made, it is possible that the picking configuration $q ^ { p i c k }$ of the pick tree’s root does not match with the the $q ^ { p l a c e }$ in the place tree’s root per the constraints in Eq. (3). In that case, B4P recalculates $\bar { q } ^ { p l a c e }$ for the place tree, using Eq. (3) and the $q ^ { p i c k }$ from the pick tree, to enforce the pairing to create an initial path (line #5 in Alg. 1).

However, when initially the pick and place trees used different picking configurations, the collision checking for them was also using different object poses in the hands. After enforcing the place tree to take the picking configuration from the paired pick tree, obtained trajectory corresponding to the place tree can potentially have collisions. To address this problem, our proposed B4P develops a post-planning path repair mechanism (line #6 in Alg. 1), as detailed in Sec. IV-C, to locally fix minor collisions in an efficient way.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 Worker.BuildForest()

Input: Worker w
Output: Boolean done
1: done ← false
2: while TIME.AVAILABLE() ∧ not done do
3:    q ← SAMPLEROBOTCONFIG()
4:    $T_{near}^{pick} \leftarrow FINDNEARESTPICKTREE(q)$
5:    $q_{new}^{pick} \leftarrow EXPANDTREE(T_{near}^{pick}, q)$   ▷ Forward Expansion
6:    $T_{near}^{place} \leftarrow FINDNEARESTPLACETREE(q)$
7:    $q_{new}^{place} \leftarrow EXPANDTREE(T_{near}^{place}, q)$   ▷ Backward Expansion
8:    if CONNECT($q_{new}^{pick}, q_{new}^{place}$) then    ▷ Try Pairing
9:    Worker.Path ← EXTRACTPATH($T_{near}^{pick}, T_{near}^{place}$)
10:    done ← true
11:    end if
12: end while
13: return done
</div>

![](Leebron2025B4P_figs/76c3fc52c1f845fef26e4d46fccbb9d6486dc403672fc18065b62ab233376672.jpg)  
Fig. 2: An illustration of the forest building in the robot configuration space with 4 pick trees and 3 place trees.

## B. Path Planning by Building Forest

B4P begins by spawning a forest with trees rooted at both pick and place configuration regions. For this, as detailed in Alg. 2, the forests are initialized as empty sets, and then iteratively populated with roots provided by PLANPICK(·) and PLANPLACE(·). Once the roots are ready, B4P launches parallel workers to grow the trees from both pick and place forests toward each other. As described in Alg. 3, each worker is independently working on building the shared forest. By sampling a random robot configuration $q \in \mathcal { Q }$ (line #3), B4P first finds the nearest tree $\mathcal { T } _ { n e a r } ^ { p i c k }$ in the pick forest $\mathcal { F } ^ { p i c k }$ that has a node closest to $q .$ The tree $\mathcal { T } _ { n e a r } ^ { p i c k }$ will then expand towards q with a linear motion as much as possible, until collisions are detected, to add a new configuration $q _ { n e w } ^ { p i c k }$ into $\mathcal { T } _ { n e a r } ^ { p i c k }$ . In the backward direction, this worker will then try to grow the nearest place tree $\mathcal { T } _ { n e a r } ^ { p l a c e }$ towards q to add a new configuration $q _ { n e w } ^ { p l a c e }$

An important step in Alg. 3 is the active attempt to connect $q _ { n e w } ^ { p i c k }$ and $q _ { n e w } ^ { p l a c e }$ by every worker in every iteration (line #8). If such a connection can be made with a valid motion, an initial solution path will be constructed. If not, the worker will continue to build the forest until one of the workers has found a solution. A configuration space illustration of Alg. 3 is shown in Fig. 2. Note that dependent on the sampled configuration q, a parallel worker can work on different pairs of pick and place trees in different iterations, so that the work spent on different trees are fully determined by the random samples and not biased by any root picking or placement configurations.

![](Leebron2025B4P_figs/aa346fb9e7cd203987b5a1389df424c512a0ebcc7e296fce7c2a58d76cff4886.jpg)  
Fig. 3: An example path repair procedure for a 2D mobile robot (blue) pick and place task. The red dashedline represents the initial path before repair, and the purple dotted lines are the repairs made. States in red are collisions when the grasp is used, and states in purple are the replanned nodes.

## C. Path Repair

As discussed above, an initial solution found by Alg. 3 can contain local collisions due to the enforced pairing of pick and place trees. As shown in line #5-6 of Alg. 1, such an initial solution will go through a PATHREPAIR(·) proce dure to eliminate such collisions to produce a completely collision-free path for the pick and place task. Concretely, given an initial path π, PATHREPAIR(·) will iteratively check through every waypoint in π and find all continuous collision-involved segments to repair. As detailed in Alg. 4, two pointers begin and end are used to keep track of the range of the collision-involved segments as the iterator i moves through π. Once a segment is identified, meaning that there is no collision at the waypoints immediately before and after the segment, a fast parallel local repair procedure PARALOCALREPLAN(begin, end) will be invoked to generate a detour path η to avoid the detected collisions. This PARALOCALREPLAN(begin, end) is a highly parallelized local motion planner implemented in a similar way to Alg. 3, with the only modification that all workers are now working on a fixed pair of begin and end roots.

When PARALOCALREPLAN(begin, end) finishes, it is possible that there is no path repair solution can be found. In that case, Alg. 4 will return an empty path to let B4P know that the search needs to continue. Otherwise, B4P will return with a successfully found path π for the pick and place task (line #7 in Alg. 1). An example path repair is visualized for a 2D mobile robot pick and place task in Fig. 3.

![](Leebron2025B4P_figs/c5f8ce550231e4f55ded87de39f892a6dafd2f2670543547468847c318e9be1d.jpg)  
Fig. 4: [2D Maze] The robot needs to find a feasible path to carry the grasped object from the start pose (left bottom corner) to the target region (red area in the right top corner); [Stick on Shelf] The manipulator needs to grasp the stick and place it on the target region on shelf; [Grocery Shelf] The manipulator needs to grasp the target object on the shelf in a grocery scenarios; [Example Picking Configurations] Left: Sampled grasp poses on each edge of the planar object; Middle: Sampled grasp poses on the green stick; Right: Sampled grasp poses on the spam object. For each task, grasp poses are uniformly randomly sampled. The optimal number of pick and place trees generated depends on the task.

```txt
Algorithm 4 PathRepair(·)
Input: Motion path π
Output: Repaired motion path π*
1: π* ← {π.GETNOTE(1)}
2: collision ← false
3: k ← 0
4: for i = 1, . . . , π.LEN() - 1 do
5:    begin ← π.GETNODE(i - k)
6:    temp ← π.GETNODE(i)
7:    end ← π.GETNODE(i + 1)
8:    if CHECKCOLLISION(temp, end) then ▷ Collision Found
9:    k ← k + 1
10:    collision ← true
11:    else if collision ∧ not CHECKCOLLISION(temp, end) then
12:    η ← PARALOCALREPLAN(begin, end) ▷ Locally Repair
13:    if η ≠ {} then
14:    π*.ADDPATH(η)
15:    k ← 0
16:    else
17:    return {} ▷ Repair Failed
18:    end if
19:    else
20:    π*.ADDNODE(end) ▷ Collision-Free Nodes
21:    end if
22: end for
23: return π* ▷ Success
```

## V. EXPERIMENTS

In this section, we first provide an overview of our experiments, including task design, baseline selection, and system environment. Then, we demonstrate the experimental result in both challenging 2D and 3D tasks to validate the effectiveness and efficiency of the proposed B4P framework.

## A. Overview

1) Task Scenarios: We evaluate the proposed framework across challenging 2D and 3D scenarios as illustrated in Figure. 4, including:

• a 2D maze task where a robot needs to pick the target object and navigate to the target region;

• a 3D stick-on-shelf task where a 7-DoF Franka Emika Panda manipulator needs to pick the target stick and safely place it in a specific region on the shelf;

• a 3D grocery-shelf task where the same manipulator needs to pick the target object and place it in a specific region in challenging grocery scenarios.

All tasks are designed to create a spatially constrained workspace for the robot; therefore, a majority of feasible grasp poses are incompatible with the task placement requirement due to infeasible placement configuration or unreachable motion trajectory plan.

2) Baselines: To provide a comprehensive evaluation, we introduce two bidirectional RRT parallel algorithms as our baseline to compare with the proposed B4P approach. These planners sample 1 placement with their sampled grasp and only use one placement as a goal.

• RRT-Individual: Each thread t performs bidirectional RRT using its own individual sampled grasp $q _ { t } ^ { p i c k }$

• RRT-Shared: All threads perform one bidirectional RRT in parallel using a single grasp. In this approach, we set a small time limit and when it expires, the planner restarts and uses a new grasp.

3) System Environment: All experiments are carried out on AMD Ryzen 9 5950X 16-Core Processor and 32GB of

![](Leebron2025B4P_figs/18fd04871741dcc8229b07a3ae12a6932249a6cc0ca5969ef1792ba0fd61dbd3.jpg)  
Fig. 5: Speedup observed for B4P for the Stick-on-Shelf task

RAM on Ubuntu 20.04. We implemented the algorithms in C++ and adopted MuJoCo [30] as the task simulator.

B. 2D Evaluation with Maze Task

<table><tr><td rowspan="2">#Threads</td><td colspan="2">Shared</td><td colspan="2">Individual</td><td colspan="2">B4P (Ours)</td></tr><tr><td>Time</td><td>Rate</td><td>Time</td><td>Rate</td><td>Time</td><td>Rate</td></tr><tr><td>1</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td>N/A</td><td>0/10</td></tr><tr><td>2</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $135.37 \pm 32.56$ </td><td>3/10</td></tr><tr><td>4</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $60.26 \pm 25.9$ </td><td>10/10</td></tr><tr><td>8</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $27.53 \pm 14.81$ </td><td>10/10</td></tr><tr><td>16</td><td>-</td><td>0/10</td><td>89.13</td><td>2/10</td><td> $12.56 \pm 6.66$ </td><td>10/10</td></tr><tr><td>30</td><td>-</td><td>0/10</td><td> $63.16 \pm 37.69$ </td><td>4/10</td><td> $5.42 \pm 2.79$ </td><td>10/10</td></tr></table>

TABLE I: Computation time (in seconds) for each method on the 2D Maze Task to output a feasible trajectory plan. The time budget is 120 seconds.

A 2D maze environment is designed to create a narrow passage in the plane for a robot to carry the target object to a target region. As shown in the bottom row of Fig. 4, we consider each edge of the target object associated with one feasible grasp. Incompatible grasp poses will easily lead to getting stuck at some flexural corner in the maze. After a stable grasp is formed, we consider the object and the robot undergoes the same rigid body transformation. We evaluate our planner on success rate, time, and speedup for different numbers of threads and the result is listed in Table. I. Though there are 21 grasps available in total, only one is compatible with the narrow passages in the maze. The proposed framework shows superiority in both the efficiency and success rate, while the naive bidirectional RRT-based methods lack the ability to find a feasible motion plan in the given time budget. Due to the inherent probabilistic completeness, we also observe an increasing success rate with increasing number of threads.

## C. 3D Pick and Place Evaluation

<table><tr><td rowspan="2">#Threads</td><td colspan="2">Shared</td><td colspan="2">Individual</td><td colspan="2">B4P (Ours)</td></tr><tr><td>Time</td><td>Rate</td><td>Time</td><td>Rate</td><td>Time</td><td>Rate</td></tr><tr><td>1</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td>172</td><td>1/10</td></tr><tr><td>2</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td>49.8</td><td>2/10</td></tr><tr><td>4</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $24.19 \pm 10.62$ </td><td>6/10</td></tr><tr><td>8</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $8.20 \pm 8.54$ </td><td>10/10</td></tr><tr><td>16</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $4.66 \pm 2.33$ </td><td>10/10</td></tr><tr><td>30</td><td>-</td><td>0/10</td><td>103</td><td>2/10</td><td> $2.03 \pm 1.45$ </td><td>10/10</td></tr></table>

TABLE II: Computation time (in seconds) for each method on the Stick-on-Shelf Task to output a feasible trajectory plan. The time budget is 180 seconds.

![](Leebron2025B4P_figs/73232dba8916a19441cfb155c751e08492077c518bb3af0196c88959c9489cc4.jpg)  
Fig. 6: Speedup observed for B4P for the Grocery-Shelf task

To further demonstrate our approach’s effectiveness, we evaluate it with more realistic and challenging task environments in 3D. Our results for the speedup of B4P are compared against using B4P with only one thread.

1) Stick on Shelf Task: In this task, the manipulator needs first to pick the yellow stick and place it in the green goal region on the blue shelf (as shown in Fig. 4-Stick on Shelf ). The evaluated performance is demonstrated in Table. II. As the dimension increases, the naive RRT-based baselines mostly fail to deliver a feasible plan in such a short time budget. Due to the relaxed formulation of tree connections and the path repair design, the proposed method balances the result completeness and efficiency. The proposed B4P possesses a substantial performance increase compared to the two baseline methods in accuracy and speed, along with a superlinear speedup as visualized in Fig. 5.

<table><tr><td rowspan="2">#Threads</td><td colspan="2">Shared</td><td colspan="2">Individual</td><td colspan="2">B4P (Ours)</td></tr><tr><td>Time</td><td>Rate</td><td>Time</td><td>Rate</td><td>Time</td><td>Rate</td></tr><tr><td>1</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $4.50 \pm 6.38$ </td><td>10/10</td></tr><tr><td>2</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $1.93 \pm 1.03$ </td><td>10/10</td></tr><tr><td>4</td><td>-</td><td>0/10</td><td>-</td><td>0/10</td><td> $0.924 \pm 0.69$ </td><td>10/10</td></tr><tr><td>8</td><td>-</td><td>0/10</td><td>28.52</td><td>2/10</td><td> $0.484 \pm 0.253$ </td><td>10/10</td></tr><tr><td>16</td><td>-</td><td>0/10</td><td> $27.4 \pm 37.3$ </td><td>3/10</td><td> $0.237 \pm 0.13$ </td><td>10/10</td></tr><tr><td>30</td><td>-</td><td>0/10</td><td> $26.2 \pm 24.7$ </td><td>5/10</td><td> $0.124 \pm 0.034$ </td><td>10/10</td></tr></table>

TABLE III: Computation time (in seconds) for each method on the Grocery-Shelf Task to output a feasible trajectory plan. The time budget is 120 seconds.

2) Grocery Shelf Task: In this task, the target object, the can of spam, must be placed in the goal region in an upward orientation. Compared with the stick-on-shelf problem, additional obstacles are added to the environment to simulate the challenging narrow passage. Three different grasp pose examples are visualized in the right figure from the bottom row of Fig. 4. Such an intricate task environment creates a narrow path in the configuration space for the pick and place task, only the horizontal grasp pose can satisfy a placement configuration simultaneously with a feasible motion trajectory as displayed in the solution path in Fig. 4. The experimental result is listed in Table. III. As the proposed B4P framework expands unbiased different trees that can fully explore the configuration space, it outperforms both baselines by a large margin and guarantees a feasible trajectory plan in the given time budget. Meanwhile, we also observe a superlinear speed when increasing the threads for computing as shown in Fig. 6. This feature possesses an inherent advantage for accelerating scalable applications in the real world. The speedup observed for this task is lower than that of the Stick-on-Shelf task, likely due to the greater number of valid grasps available for this task.

## VI. CONCLUSION

In this work, we proposed B4P, a framework to address the problem of simultaneously finding grasp pose and motion plan for downstream placement tasks. By leveraging the parallelized bidirectional forests with path repair, the proposed framework demonstrates significant efficiency together with result completeness on diverse scenarios. Additionally, we investigated its inherent parallelism to achieve a superlinear speedup.

We plan to extend the current work in the following directions: adding perception modules to get rid of the assumption of a perfect description of the environment and extending a re-grasping policy to tackle extreme situations that no compatible grasp poses in the initial object state.

## REFERENCES

[1] N. Correll, K. E. Bekris, D. Berenson, O. Brock, A. Causo, K. Hauser, K. Okada, A. Rodriguez, J. M. Romano, and P. R. Wurman, “Analysis and observations from the first amazon picking challenge,” IEEE Transactions on Automation Science and Engineering, vol. 15, no. 1, pp. 172–188, 2016.

[2] T. Wisspeintner, T. Van Der Zant, L. Iocchi, and S. Schiffer, “Robocup@ home: Scientific competition and benchmarking for domestic service robots,” Interaction Studies, vol. 10, no. 3, pp. 392–426, 2009.

[3] D. Morrison, P. Corke, and J. Leitner, “Closing the loop for robotic grasping: A real-time, generative grasp synthesis approach,” Robotics: Science and Systems XIV, pp. 1–10, 2018.

[4] H.-S. Fang, C. Wang, M. Gou, and C. Lu, “Graspnet-1billion: A largescale benchmark for general object grasping,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2020, pp. 11 444–11 453.

[5] K. Hang, M. Li, J. A. Stork, Y. Bekiroglu, F. T. Pokorny, A. Billard, and D. Kragic, “Hierarchical fingertip space: A unified framework for grasp planning and in-hand grasp adaptation,” IEEE Transactions on robotics, vol. 32, no. 4, pp. 960–972, 2016.

[6] M. Elbanhawi and M. Simic, “Sampling-based robot motion planning: A review,” IEEE Access, vol. 2, pp. 56–77, 2014.

[7] K. Harada, T. Tsuji, K. Nagata, N. Yamanobe, H. Onda, T. Yoshimi, and Y. Kawai, “Object placement planner for robotic pick and place tasks,” in IEEE/RSJ International Conference on Intelligent Robots and Systems, 2012, pp. 980–985.

[8] J. A. Haustein, K. Hang, J. Stork, and D. Kragic, “Object placement planning and optimization for robot manipulators,” in 2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2019, pp. 7417–7424.

[9] J. A. Haustein, K. Hang, and D. Kragic, “Integrating motion and hierarchical fingertip grasp planning,” in 2017 IEEE International Conference on Robotics and Automation (ICRA), 2017, pp. 3439– 3446.

[10] E. Plaku, K. E. Bekris, B. Y. Chen, A. M. Ladd, and L. E. Kavraki, “Sampling-based roadmap of trees for parallel motion planning,” IEEE Transactions on Robotics, vol. 21, no. 4, pp. 597–608, 2005.

[11] A. Bicchi and V. Kumar, “Robotic grasping and contact: A review,” in Proceedings 2000 ICRA. Millennium conference. IEEE international conference on robotics and automation. Symposia proceedings (Cat. No. 00CH37065), vol. 1. IEEE, 2000, pp. 348–353.

[12] R. Newbury, M. Gu, L. Chumbley, A. Mousavian, C. Eppner, J. Leitner, J. Bohg, A. Morales, T. Asfour, D. Kragic, et al., “Deep learning approaches to grasp synthesis: A review,” IEEE Transactions on Robotics, vol. 39, no. 5, pp. 3994–4015, 2023.

[13] M. T. Ciocarlie and P. K. Allen, “Hand posture subspaces for dexterous robotic grasping,” The International Journal of Robotics Research, vol. 28, no. 7, pp. 851–867, 2009.

[14] T. Liu, Z. Liu, Z. Jiao, Y. Zhu, and S.-C. Zhu, “Synthesizing diverse and physically stable grasps with arbitrary hand structures using differentiable force closure estimator,” IEEE Robotics and Automation Letters, vol. 7, no. 1, pp. 470–477, 2021.

[15] Y. Chen, X. Gao, K. Yao, L. Niederhauser, Y. Bekiroglu, and A. Billard, “Differentiable robot neural distance function for adaptive grasp synthesis on a unified robotic arm-hand system,” arXiv preprint arXiv:2309.16085, 2023.

[16] M. Sundermeyer, A. Mousavian, R. Triebel, and D. Fox, “Contactgraspnet: Efficient 6-dof grasp generation in cluttered scenes,” in 2021 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2021, pp. 13 438–13 444.

[17] A. Orthey, C. Chamzas, and L. E. Kavraki, “Sampling-based motion planning: A comparative review,” Annual Review of Control, Robotics, and Autonomous Systems, vol. 7, 2023.

[18] W. Thomason, Z. Kingston, and L. E. Kavraki, “Motions in microseconds via vectorized sampling-based planning,” in 2024 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2024, pp. 8749–8756.

[19] J. Bialkowski, S. Karaman, and E. Frazzoli, “Massively parallelizing the rrt and the rrt,” in 2011 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE, 2011, pp. 3513–3518.

[20] A. Fishman, A. Murali, C. Eppner, B. Peele, B. Boots, and D. Fox, “Motion policy networks,” in conference on Robot Learning. PMLR, 2023, pp. 967–977.

[21] B. Sundaralingam, S. K. S. Hari, A. Fishman, C. Garrett, K. Van Wyk, V. Blukis, A. Millane, H. Oleynikova, A. Handa, F. Ramos, et al., “Curobo: Parallelized collision-free robot motion generation,” in 2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, pp. 8112–8119.

[22] M. Bhardwaj, B. Sundaralingam, A. Mousavian, N. D. Ratliff, D. Fox, F. Ramos, and B. Boots, “Storm: An integrated framework for fast joint-space model-predictive control for reactive manipulation,” in Conference on Robot Learning. PMLR, 2022, pp. 750–759.

[23] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in Proceedings 2000 ICRA. Millennium conference. IEEE international conference on robotics and automation. Symposia proceedings (Cat. No. 00CH37065), vol. 2. IEEE, 2000, pp. 995–1001.

[24] S. R. Lindemann and S. M. LaValle, “Incrementally reducing dispersion by increasing voronoi bias in rrts,” in IEEE International Conference on Robotics and Automation, 2004. Proceedings. ICRA’04. 2004, vol. 4. IEEE, 2004, pp. 3251–3257.

[25] A. Zeng, S. Song, K.-T. Yu, E. Donlon, F. R. Hogan, M. Bauza, D. Ma, O. Taylor, M. Liu, E. Romo, et al., “Robotic pick-and-place of novel objects in clutter with multi-affordance grasping and cross-domain image matching,” The International Journal of Robotics Research, vol. 41, no. 7, pp. 690–705, 2022.

[26] J.-P. Saut, M. Gharbi, J. Cortes, D. Sidobre, and T. Sim ´ eon, “Planning ´ pick-and-place tasks with two-hand regrasping,” in 2010 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE, 2010, pp. 4528–4533.

[27] M. D. Shanthi and T. Hermans, “Pick and place planning is better than pick planning then place planning,” IEEE Robotics and Automation Letters, vol. 9, no. 3, pp. 2790–2797, 2024.

[28] Z. He, N. Chavan-Dafle, J. Huh, S. Song, and V. Isler, “Pick2place: Task-aware 6dof grasp estimation via object-centric perspective affordance,” in 2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, pp. 7996–8002.

[29] R. A. Brooks, “Planning collision-free motions for pick-and-place operations,” The International Journal of Robotics Research, vol. 2, no. 4, pp. 19–44, 1983.

[30] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, 2012, pp. 5026–5033.