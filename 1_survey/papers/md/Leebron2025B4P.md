---
citation_key: Leebron2025B4P
arxiv_id: 2504.04598
arxiv_url: "https://arxiv.org/abs/2504.04598"
title: "B4P: Simultaneous Grasp and Motion Planning for Object Placement via Parallelized Bidirectional Forests and Path Repair"
authors_short: "Benjamin H. Leebron et al."
year: 2025
direction_tag: J_homotopy_topology
source: pymupdf4llm
converted_at: 2026-06-23T18:11:37Z
origin: ai+web
reviewed: false
---

# **B4P: Simultaneous Grasp and Motion Planning for Object Placement via Parallelized Bidirectional Forests and Path Repair** 

Benjamin H. Leebron, Kejia Ren, Yiting Chen, and Kaiyu Hang 

_**Abstract**_ **— Robot pick and place systems have traditionally decoupled grasp, placement, and motion planning to build sequential optimization pipelines with an assumption that the individual components will be able to work together. However, this separation introduces sub-optimality, as grasp choices may limit, or even prohibit, feasible motions for a robot to reach the target placement pose, particularly in cluttered environments with narrow passages. To this end, we propose a forest-based planning framework to simultaneously find grasp configurations and feasible robot motions that explicitly satisfy downstream placement configurations paired with the selected grasps. Our proposed framework leverages a bidirectional sampling-based approach to build a start forest, rooted at the feasible grasp regions, and a goal forest, rooted at the feasible placement regions, to facilitate the search through randomly explored motions that connect valid pairs of grasp and placement trees. We demonstrate that the framework’s inherent parallelism enables superlinear speedup, making it scalable for applications for redundant robot arms, e.g., 7 DoF, to work efficiently in highly cluttered environments. Extensive experiments in simulation demonstrate the robustness and efficiency of the proposed framework in comparison with multiple baselines under diverse scenarios.** 

## I. INTRODUCTION 

Robot pick and place is a fundamental manipulation skill needed in various application scenarios [1], [2]. To relocate an object to the target pose, such systems are required to: 1) find a feasible grasp configuration; 2) find a feasible placement configuration; and 3) generate a feasible motion plan to connect theses two configurations under kinematic and environmental constraints. Traditionally, these topics have been investigated individually e.g., grasp planning [3]– [5], motion planning [6], and placement planning [7]. More recently, they have been also studied as coupled problems, e.g., motion planning for grasping or placement, and grasping for placement [8], [9]. 

However, a unified framework that addresses pick, motion, and placement planning simultaneously to ensure that all internal constraints are satisfied is yet to be developed. For example, a planner needs to select a grasp that can pass through all narrow passages through a robot motion to finally reach a selected placement pose. Note that even if both the grasp and placement poses are valid, it is often an issue that there is no robot motion to connect them due to the collisions rendered by the selected grasp. See Fig. 1 for an example. 

To this end, we propose **B4P** (Bidirectionally Picking, Planning, and Placing in Parallel), a joint planning frame- 

The authors are with the Department of Computer Science, Rice University, Houston, TX 77005, USA. This project is supported by the US National Science Foundation grant FRR-2240040. 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0001-09.png)


Fig. 1: A motivational scenario where the robot is tasked to reposition the target object, the yellow stick, to the shelf. It must pass through a narrow passage and of the three pictured grasps, only the grasp in the center of the object (white) will allow the robot to reach the placement location. However, all grasps are feasible initially, and we must somehow find which initial grasp will allow for the robot to reach the downstream placement location. 

work for object pick and place in spatially constrained environments. Specifically, the framework first identifies a grasp region – a set of robot configurations that ensure a feasible grasp; and a placement region – a set of configurations that reach the target placement poses. We do not make any assumptions on how such regions can be found so that any existing planner can be used, e.g., [5]. Thereafter, through a sampling-based scheme, the proposed B4P builds a _pick forest_ (with trees rooted inside the identified grasp region) and a _place forest_ (with trees rooted inside the identified placement region), and simultaneously grows those trees bidirectionally to find paired connections between starts and goals. Once a connection is made, a grasp configuration and a placement configuration will be paired, and a complete robot motion will be simultaneously provided. 

Our B4P algorithm design offers an inherent internal structure that can be parallelized to achieve superlinear speedups thanks to its non-deterministic nature of samplingbased algorithms [10]. The framework is also designed to offer application flexiblity, allowing modular integration with any grasp method that can find feasible end-effector poses, and with any placement planning methods that can generate end-effctor or object final poses. In brief, the proposed B4P: 

- 1) finds grasps that are guaranteed to be suitable for downstream placement through narrow passages or in cluttered environments; 

- 2) leverages the parallelizability of forest-based planning and to achieve a superlinear speedup; 

- 3) can smoothly integrate with any grasp planners and placement planners to work with various robots. 

## II. RELATED WORKS 

_1) Grasp and Placement Planning:_ Grasp planning is a critical component in robot pick and place systems, focusing on determining how the robot’s end-effector should be placed to pick up an object securely. Current research on grasp planning can be roughly divided into two categories: modelbased [11] and data-driven [12]. Model-based methods [5], [13]–[15] rely on prior knowledge of the target object and analytically compute grasp configurations that meet grasp criteria such as force closure. Data-driven approaches [3], [4], [16] aim to derive a direct mapping from visual input to grasp poses from well-annotated datasets. On the other end of the problem spectrum, placement planning has investigated object-centric optimization problems, such as placement stability and functionality, as well as task and environmental constraints [8]. However, it is still an open problem in the field that grasp and placement configurations, when planned separately, are not necessarily connectable with any feasible robot motions. 

_2) Sampling-based Motion Planning:_ Motion planning computes a collision-free path in the robot’s configuration space to connect the grasp with the placement configuration in pick and place systems. Sampling-based planners [17] have proven efficient and generalizable in exploring the highdimensional configuration space of manipulators. Significant acceleration can be obtained through parallelism [18]–[22] on both GPU and CPU-based computing. Key properties of sampling-based planners include probabilistic completeness [23] and Voronoi bias [24]. The former ensures that a solution will eventually be found as long as it exists in the search space, while the latter contributes to exploration efficiency in high-dimensional spaces. Based on the advantages of sampling-based approaches, and along with a novel forest-based planning strategy, the proposed B4P can simultaneously pair valid grasp and placement configurations while generating feasible motion plans to connect them. 

_3) Pick and Place Planning:_ Pick and place planning in robotics primarily focuses on grasping a target object and relocating it to a specified location. Grasp planning and motion planning are both critical components during this process. Zeng [25] presents a system design solely focusing on multi-modality grasp planning in the Amazon Robotics Challenge. Saut [26] proposes a dual-arm approach to achieve larger workspace. Haustein [8] aims at finding a feasible placement configuration in cluttered environments. While taking placement compatibility into consideration during grasp planning [27], [28], however, a geometrically valid placement configuration might still be unreachable [29] by any collision-free robot motions due to kinematic and 

environmental constraints. In an effort to unify and integrate these key functionalities, our B4P focuses on building a planning that can be compatible with any existing pick planning and placement planning approaches, while coordinate in the middle to ensure the compatibility of individual solutions. 

## III. PRELIMINARIES AND PROBLEM STATEMENT 

In this section, we first review the preliminaries of the proposed work, based on which we formulate robot pick and place as a problem of simultaneously finding pick, motion, and placement solutions. 

## _A. Preliminaries_ 

In this work, we consider the pick and place problem as relocating a target object from a start pose to a target pose through a collision-free robot motion. To unify our planning framework as aforementioned, the grasp configurations, the placement configurations, as well as the robot motion paths are all expressed in the _robot configuration space_ . 

The configuration space of a _n−_ DoF robot is denoted by _Q ⊂_ R _[n]_ . The robot’s forward kinematics is denoted by Γ : _Q �→ SE_ (3), such that any valid robot joint configuration _q ∈Q_ can be mapped to an robot end-effector’s pose _x ∈ SE_ (3). Accordingly, the inverse kinematics is denoted by Γ _[−]_[1] . Note that these definitions are not limited to arm robots, but also can be applied to any robots that have a controlled end-effector. For example, as shown later in Fig. 3, a mobile robot with a fixed gripper can also map from its base configuration to an end-effector’s pose. 

For an object inside the workspace of the robot, let us denote its pose by _x[obj] ∈ SE_ (3), a grasp planner will be able to generate feasible pick configuration relative to _p[obj]_ . Let us denote by PLANPICK( _·_ ) : _SE_ (3) _�→Q_ the function of this planner that generates picking configurations: 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0002-14.png)


In practice and for many grasp planners, every given _p[obj]_ can result in 0 _,_ 1 or many picking configuration solutions. Without loss of generality, in this work as we focus on building the joint framework for pick, motion, and place planning that is compatible with existing grasp planners, we treat PLANPICK( _·_ ) as a sampler that can generate a picking configuration every time it is called. The output configuration can be the same or different across function calls. 

Inside the workspace of the robot, let us denote by a region _Y ⊂ SE_ (3) where the placement of an object is expected. A placement planner, which finds a pose within _Y_ for the object, is denoted as PLANPLACE( _·_ ) : _SE_ (3) _�→ SE_ (3) to generate a stable placement under given task constraints: 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0002-17.png)


Similarly to grasp planning, to be compatible with exisiting placement planners, we treat this place planner as a sampler that can generate the same, or different, placement plans every time it is called. Furthermore, to keep our planning 

framework operating with robot configurations only as aforementioned, every planned placement pose will be converted to a robot configuration by: 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0003-01.png)


where the end-effector’s pose at placement calculated by _x[place]_ ( _x[obj]_ ) _[−]_[1] Γ( _q[pick]_ ) ensures that the grasp on the object has not changed during the robot motion execution. 

## _B. Trees and Forests_ 

Same as in most sampling-based motion planning approaches, we use trees to represent the exploration of the valid robot configurations and robot motions to connect between them in the configuration space _Q_ . In our bidirectional framework, we denote by _Ti[pick]_ a motion tree rooted at the _i−_ th sampled picking configuration, and by _Tj[place]_ a motion tree rooted at the _j−_ th sampled placement configuration. We also denote _Ti[pick] .pick_ to be the _SE_ (3) transformation of the gripper relative to the object. In the trees, every node is a collision-free robot configuration and every edge is a collision free path. To enable all trees to simultaneously explore the configuration space and find potential valid pairings between _Ti[pick]_ and _Tj[place]_ , we collect the trees into two motion forests _F[pick]_ = _{Ti[pick] }i_ =1: _n_ and _F[place]_ = _{Tj[place] }j_ =1: _m_ , with _n_ and _m_ trees respectively. While the trees grow from two forests toward each other, only connections between trees from different forests are allowed. 

## _C. Problem Formulation_ 

The pick, motion, and place planning problem in this work is formalized as follows. Given an object in the robot workspace at _x[obj]_ , and a placement region _Y_ , find a picking configuration _q[pick]_ for _x[obj]_ , and a robot motion plan _π_ = _{q[pick] , . . . , qk, . . . , q[place] }_ , such that: 

- the final object pose _x[place]_ , as calculated by Eq. 3, satisfies _x[place] ∈ Y_ ; 

- all intermidiate robot states _qk_ together with the object with its in-hand pose determined by _q[pick]_ at the beginning will be collision-free. 

## IV. METHOD: B4P 

We begin this section with an overview of the proposed B4P algorithm and then delve into the details of its key components of forest building and path repair. 

## _A. Algorithm Overview_ 

In Eq.(3) we can see that a robot configuration _q[place]_ for placement can be calculated only if the initial picking configuration _q[pick]_ is known. While exact pick and place configuration pairing is ensured, this requirement, however, will pose a hard constraint that a pick tree _Ti[pick]_ and a place tree _Tj[place]_ in the forests can be potentially connected only if their roots share the same picking configuration relative to the object, i.e., _Ti[pick] .pick_ = _Tj[place] .pick_ . As such, the bidirectional forests will be divided by root configurations 

**Algorithm 1** The B4P algorithm 

|**Algorithm 1** The B4P algorithm|**Algorithm 1** The B4P algorithm|||
|---|---|---|---|
|**Input:** Object pose _xobj_, placement region _Y_||, number of|pick and place|
||trees _Npick_ and _Nplace_|||
|**Output:** Robot motion path _π_||||
|1:|_Fpick, Fplace ←_SPAWNFOREST(_xobj, Y, Npick, Nplace_) _▷_Alg. 2|||
|2:|Workers _←_LAUNCHPARAWORKERS(_Fpick, Fplace_)|||
|3:|**parfor** w _∈_Workers **do**|_▷_Parallel Workers||
|4:|**if** w.BUILDFOREST() **then**||_▷_Alg. 3|
|5:|_π ←_w.PATH()||_▷_Initial Path|
|6:|_π ←_PATHREPAIR(_π_)||_▷_Alg. 4|
|7:|**if** _π _=_{}_ **then**||_▷_Success|
|8:|Workers.FINISH()|||
|9:|**end if**|||
|10:|**end if**|||
|11:|**end parfor**|||
|12:|**return** _π_|||



## **Algorithm 2** SpawnForest( _·_ ) 

|**Algorithm 2** SpawnForest(_·_)|**Algorithm 2** SpawnForest(_·_)|**Algorithm 2** SpawnForest(_·_)|
|---|---|---|
|**Input:** Object pose _xobj_, placement region _Y_, number of pick and place|||
||trees _Npick_ and _Nplace_||
|**Output:** Pick forest _Fpick_, place forest _Fplace_|||
|1:|_Fpick ←{}, Fplace ←{}_||
|2:|**for** _i_= 1_, . . . , Npick_ **do**||
|3:|_qpick_ = PLANPICK(_xobj_)|_▷_Eq. (1)|
|4:|_Fpick._ADDROOT(_qpick_)||
|5:|**end for**||
|6:|**for** _i_= 1_, . . . , Nplace_ **do**||
|7:|_xplace_ = PLANPLACE(_Y_)|_▷_Eq. (2)|
|8:|_qpick_ = PLANPICK(_xobj_)||
|9:|_qplace_ = Γ_−_1(_xplace_(_xobj_)_−_1Γ(_qpick_))|_▷_Eq. (3)|
|10:|_Fplace._ADDROOT(_qplace_)||
|11:|**end for**||
|12:|**return** _Fpick, Fplace_||



into sub-forests, and the ability of fully exploring motion possibilities will be significantly reduced. 

To this end, in our work, as outlined in Alg. 1, in order to facilitate the tree expansion by sufficiently exploring pairings between the two forests, we opt to omit the constraints of an explicit picking configuration for all place trees _Tj[place]_ . For this, when a placement pose _x[place]_ is sampled, a random picking configuration will be assigned to it to compute _q[place]_ . When our algorithm B4P expands the forests from both sides and tries to make connections, the condition of _Ti[pick] .pick_ = _Tj[place] .pick_ is not checked when making connections between pick and place trees. Once a connection is made, it is possible that the picking configuration _q[pick]_ of the pick tree’s root does not match with the the _q[place]_ in the place tree’s root per the constraints in Eq. (3). In that case, B4P recalculates _q[place]_ for the place tree, using Eq. (3) and the _q[pick]_ from the pick tree, to enforce the pairing to create an initial path (line #5 in Alg. 1). 

However, when initially the pick and place trees used different picking configurations, the collision checking for them was also using different object poses in the hands. After enforcing the place tree to take the picking configuration from the paired pick tree, obtained trajectory corresponding to the place tree can potentially have collisions. To address this problem, our proposed B4P develops a post-planning _path repair_ mechanism (line #6 in Alg. 1), as detailed in Sec. IV-C, to locally fix minor collisions in an efficient way. 

**Algorithm 3** Worker.BuildForest() 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0004-01.png)


**----- Start of picture text -----**<br>
Input: Worker w<br>Output: Boolean done<br>1: done ← false<br>2: while TIME.AVAILABLE() ∧ not done do<br>3: q ← SAMPLEROBOTCONFIG()<br>4:5: Tqnew [pick] near [pick][←][←] [E][F][XPAND][IND][N][EAREST][T][REE][(] [T] [P] near [pick] [ICK][T] [, q] [REE][)] [(] [q] [)] ▷ Forward Expansion<br>6: Tnear [place] ← FINDNEARESTPLACETREE( q )<br>7: qnew [place] ← EXPANDTREE( Tnear [place][, q] [)] ▷ Backward Expansion<br>8: if CONNECT( qnew [pick][, q] new [place] [)] [then] ▷ Try Pairing<br>9: Worker.Path ← EXTRACTPATH( Tnear [pick][,][ T] near [place] [)]<br>10: done ← true<br>11: end if<br>12: end while<br>13: return done<br>Configuration Space Solution Path<br>Pick Forest Place Forest<br>**----- End of picture text -----**<br>


Fig. 2: An illustration of the forest building in the robot configuration space with 4 pick trees and 3 place trees. 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0004-03.png)


Fig. 3: An example path repair procedure for a 2D mobile robot (blue) pick and place task. The red dashedline represents the initial path before repair, and the purple dotted lines are the repairs made. States in red are collisions when the grasp is used, and states in purple are the replanned nodes. 

spent on different trees are fully determined by the random samples and not biased by any root picking or placement configurations. 

## _C. Path Repair_ 

## _B. Path Planning by Building Forest_ 

B4P begins by spawning a forest with trees rooted at both pick and place configuration regions. For this, as detailed in Alg. 2, the forests are initialized as empty sets, and then iteratively populated with roots provided by PLANPICK( _·_ ) and PLANPLACE( _·_ ). Once the roots are ready, B4P launches parallel workers to grow the trees from both pick and place forests toward each other. As described in Alg. 3, each worker is independently working on building the shared forest. By sampling a random robot configuration _q ∈Q_ (line #3), B4P first finds the nearest tree _Tnear[pick]_[in][the][pick][forest] _F[pick]_ that has a node closest to _q_ . The tree _Tnear[pick]_[will][then] expand towards _q_ with a linear motion as much as possible, until collisions are detected, to add a new configuration _qnew[pick]_ into _Tnear[pick]_[.][In][the][backward][direction,][this][worker][will][then] try to grow the nearest place tree _Tnear[place]_ towards _q_ to add a new configuration _qnew[place]_[.] 

An important step in Alg. 3 is the active attempt to connect _qnew[pick]_[and] _[q] new[place]_[by][every][worker][in][every][iteration][(line][#8).] If such a connection can be made with a valid motion, an initial solution path will be constructed. If not, the worker will continue to build the forest until one of the workers has found a solution. A configuration space illustration of Alg. 3 is shown in Fig. 2. Note that dependent on the sampled configuration _q_ , a parallel worker can work on different pairs of pick and place trees in different iterations, so that the work 

As discussed above, an initial solution found by Alg. 3 can contain local collisions due to the enforced pairing of pick and place trees. As shown in line #5-6 of Alg. 1, such an initial solution will go through a PATHREPAIR( _·_ ) procedure to eliminate such collisions to produce a completely collision-free path for the pick and place task. Concretely, given an initial path _π_ , PATHREPAIR( _·_ ) will iteratively check through every waypoint in _π_ and find all continuous collision-involved segments to repair. As detailed in Alg. 4, two pointers _begin_ and _end_ are used to keep track of the range of the collision-involved segments as the iterator _i_ moves through _π_ . Once a segment is identified, meaning that there is no collision at the waypoints immediately before and after the segment, a fast parallel local repair procedure PARALOCALREPLAN( _begin, end_ ) will be invoked to generate a detour path _η_ to avoid the detected collisions. This PARALOCALREPLAN( _begin, end_ ) is a highly parallelized local motion planner implemented in a similar way to Alg. 3, with the only modification that all workers are now working on a fixed pair of _begin_ and _end_ roots. 

When PARALOCALREPLAN( _begin, end_ ) finishes, it is possible that there is no path repair solution can be found. In that case, Alg. 4 will return an empty path to let B4P know that the search needs to continue. Otherwise, B4P will return with a successfully found path _π_ for the pick and place task (line #7 in Alg. 1). An example path repair is visualized for a 2D mobile robot pick and place task in Fig. 3. 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0005-00.png)


**----- Start of picture text -----**<br>
2D Maze Stick on Shelf Grocery Shelf<br>Example Picking Configurations<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0005-01.png)


Fig. 4: [2D Maze] The robot needs to find a feasible path to carry the grasped object from the start pose (left bottom corner) to the target region (red area in the right top corner); [Stick on Shelf] The manipulator needs to grasp the stick and place it on the target region on shelf; [Grocery Shelf] The manipulator needs to grasp the target object on the shelf in a grocery scenarios; [Example Picking Configurations] Left: Sampled grasp poses on each edge of the planar object; Middle: Sampled grasp poses on the green stick; Right: Sampled grasp poses on the spam object. For each task, grasp poses are uniformly randomly sampled. The optimal number of pick and place trees generated depends on the task. 

**Algorithm 4** PathRepair( _·_ ) 

|**Algorithm 4** PathRepair(_·_)||
|---|---|
|**Input:** Motion path _π_<br>**Output:** Repaired motion path _π∗_<br>1: _π∗←{π._GETNOTE(1)_}_||
|2: collision _←false_||
|3: _k ←_0<br>4: **for** _i_= 1_, . . . , π._LEN()_−_1 **do**<br>5:<br>begin _←π._GETNODE(_i −k_)||
|6:<br>temp _←π._GETNODE(_i_)||
|7:<br>end _←π._GETNODE(_i_+ 1)<br>8:<br>**if** CHECKCOLLISION(temp, end) **then**<br>9:<br>_k ←k_+ 1|_▷_Collision Found|
|10:<br>collision _←true_<br>11:<br>**else if** collision _∧_**not** CHECKCOLLISION(temp, end) **then**<br>12:<br>_η ←_PARALOCALREPLAN(begin, end)<br>_▷_Locally Repair<br>13:<br>**if** _η _=_{}_ **then**||
|14:<br>_π∗_.ADDPATH(_η_)<br>15:<br>_k ←_0<br>16:<br>**else**||
|17:<br>**return** _{}_|_▷_Repair Failed|
|18:<br>**end if**<br>19:<br>**else**<br>20:<br>_π∗_.ADDNODE(end)|_▷_Collision-Free Nodes|
|21:<br>**end if**||
|22: **end for**<br>23: **return** _π∗_|_▷_Success|



## V. EXPERIMENTS 

In this section, we first provide an overview of our experiments, including task design, baseline selection, and system environment. Then, we demonstrate the experimental result in both challenging 2D and 3D tasks to validate the effectiveness and efficiency of the proposed B4P framework. 

## _A. Overview_ 

_1) Task Scenarios:_ We evaluate the proposed framework across challenging 2D and 3D scenarios as illustrated in Figure. 4, including: 

- a 2D maze task where a robot needs to pick the target object and navigate to the target region; 

- a 3D stick-on-shelf task where a 7-DoF Franka Emika Panda manipulator needs to pick the target stick and safely place it in a specific region on the shelf; 

- a 3D grocery-shelf task where the same manipulator needs to pick the target object and place it in a specific region in challenging grocery scenarios. 

All tasks are designed to create a spatially constrained workspace for the robot; therefore, a majority of feasible grasp poses are incompatible with the task placement requirement due to infeasible placement configuration or unreachable motion trajectory plan. 

_2) Baselines:_ To provide a comprehensive evaluation, we introduce two bidirectional RRT parallel algorithms as our baseline to compare with the proposed B4P approach. These planners sample 1 placement with their sampled grasp and only use one placement as a goal. 

- RRT- _Individual_ : Each thread _t_ performs bidirectional RRT using its own individual sampled grasp _qt[pick]_ . 

- RRT- _Shared_ : All threads perform one bidirectional RRT in parallel using a single grasp. In this approach, we set a small time limit and when it expires, the planner restarts and uses a new grasp. 

- _3) System Environment:_ All experiments are carried out 

- on AMD Ryzen 9 5950X 16-Core Processor and 32GB of 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0006-00.png)


**----- Start of picture text -----**<br>
80 Observed Speedup<br>Linear Speedup<br>60<br>40<br>20<br>0<br>0 5 10 15 20 25 30<br>#Threads<br>Speedup<br>**----- End of picture text -----**<br>


Fig. 5: Speedup observed for B4P for the Stick-on-Shelf task 

RAM on Ubuntu 20.04. We implemented the algorithms in C++ and adopted MuJoCo [30] as the task simulator. 

_B. 2D Evaluation with Maze Task_ 

|#Threads|Shared<br>Time<br>Rate|Shared<br>Time<br>Rate|Individual<br>Time<br>Rate|Individual<br>Time<br>Rate|B4P (Ours)<br>Time<br>Rate|B4P (Ours)<br>Time<br>Rate|
|---|---|---|---|---|---|---|
|1<br>2<br>4<br>8<br>16<br>30|-<br>-<br>-<br>-<br>-<br>-|0/10<br>0/10<br>0/10<br>0/10<br>0/10<br>0/10|-<br>-<br>-<br>-<br>89.13<br>63.16 _±_ 37.69|0/10<br>0/10<br>0/10<br>0/10<br>2/10<br>4/10|N/A<br>135.37 _±_ 32.56<br>60.26 _±_ 25.9<br>27.53 _±_ 14.81<br>12.56 _±_6.66<br>5.42 _±_ 2.79|0/10<br>3/10<br>10/10<br>10/10<br>10/10<br>10/10|



TABLE I: Computation time (in seconds) for each method on the 2D Maze Task to output a feasible trajectory plan. The time budget is 120 seconds. 

A 2D maze environment is designed to create a narrow passage in the plane for a robot to carry the target object to a target region. As shown in the bottom row of Fig. 4, we consider each edge of the target object associated with one feasible grasp. Incompatible grasp poses will easily lead to getting stuck at some flexural corner in the maze. After a stable grasp is formed, we consider the object and the robot undergoes the same rigid body transformation. We evaluate our planner on success rate, time, and speedup for different numbers of threads and the result is listed in Table. I. Though there are 21 grasps available in total, only one is compatible with the narrow passages in the maze. The proposed framework shows superiority in both the efficiency and success rate, while the naive bidirectional RRT-based methods lack the ability to find a feasible motion plan in the given time budget. Due to the inherent probabilistic completeness, we also observe an increasing success rate with increasing number of threads. 

## _C. 3D Pick and Place Evaluation_ 

|#Threads|Shared<br>Time<br>Rate|Shared<br>Time<br>Rate|Individual<br>Time<br>Rate|Individual<br>Time<br>Rate|B4P (Ours)<br>Time<br>Rate|B4P (Ours)<br>Time<br>Rate|
|---|---|---|---|---|---|---|
|1<br>2<br>4<br>8<br>16<br>30|-<br>-<br>-<br>-<br>-<br>-|0/10<br>0/10<br>0/10<br>0/10<br>0/10<br>0/10|-<br>-<br>-<br>-<br>-<br>103|0/10<br>0/10<br>0/10<br>0/10<br>0/10<br>2/10|172<br>49.8<br>24.19 _±_10_._62<br>8.20 _±_8.54<br>4.66 _±_ 2.33<br>2.03 _±_ 1.45|1/10<br>2/10<br>6/10<br>10/10<br>10/10<br>10/10|



TABLE II: Computation time (in seconds) for each method on the Stick-on-Shelf Task to output a feasible trajectory plan. The time budget is 180 seconds. 


![](1_survey/papers/md/Leebron2025B4P_figs/Leebron2025B4P.pdf-0006-10.png)


**----- Start of picture text -----**<br>
80 Observed Speedup<br>Linear Speedup<br>60<br>40<br>20<br>0<br>0 5 10 15 20 25 30<br>#Threads<br>Speedup<br>**----- End of picture text -----**<br>


Fig. 6: Speedup observed for B4P for the Grocery-Shelf task 

To further demonstrate our approach’s effectiveness, we evaluate it with more realistic and challenging task environments in 3D. Our results for the speedup of B4P are compared against using B4P with only one thread. 

_1) Stick on Shelf Task:_ In this task, the manipulator needs first to pick the yellow stick and place it in the green goal region on the blue shelf (as shown in Fig. 4- _Stick on Shelf_ ). The evaluated performance is demonstrated in Table. II. As the dimension increases, the naive RRT-based baselines mostly fail to deliver a feasible plan in such a short time budget. Due to the relaxed formulation of tree connections and the path repair design, the proposed method balances the result completeness and efficiency. The proposed B4P possesses a substantial performance increase compared to the two baseline methods in accuracy and speed, along with a superlinear speedup as visualized in Fig. 5. 

|#Threads|Shared<br>Time<br>Rate|Shared<br>Time<br>Rate|Individual<br>Time<br>Rate|Individual<br>Time<br>Rate|B4P (Ours)<br>Time<br>Rate|B4P (Ours)<br>Time<br>Rate|
|---|---|---|---|---|---|---|
|1<br>2<br>4<br>8<br>16<br>30|-<br>-<br>-<br>-<br>-<br>-|0/10<br>0/10<br>0/10<br>0/10<br>0/10<br>0/10|-<br>-<br>-<br>28.52<br>27.4 _±_ 37.3<br>26.2 _±_ 24.7|0/10<br>0/10<br>0/10<br>2/10<br>3/10<br>5/10|4.50 _±_ 6.38<br>1.93 _±_ 1.03<br>0.924 _±_ 0.69<br>0.484 _±_ 0.253<br>0.237 _±_ 0.13<br>0.124 _±_ 0.034|10/10<br>10/10<br>10/10<br>10/10<br>10/10<br>10/10|



TABLE III: Computation time (in seconds) for each method on the Grocery-Shelf Task to output a feasible trajectory plan. The time budget is 120 seconds. 

_2) Grocery Shelf Task:_ In this task, the target object, the can of spam, must be placed in the goal region in an upward orientation. Compared with the stick-on-shelf problem, additional obstacles are added to the environment to simulate the challenging narrow passage. Three different grasp pose examples are visualized in the right figure from the bottom row of Fig. 4. Such an intricate task environment creates a narrow path in the configuration space for the pick and place task, only the horizontal grasp pose can satisfy a placement configuration simultaneously with a feasible motion trajectory as displayed in the solution path in Fig. 4. The experimental result is listed in Table. III. As the proposed B4P framework expands unbiased different trees that can fully explore the configuration space, it outperforms both baselines by a large margin and guarantees a feasible trajectory plan in the given time budget. Meanwhile, we also observe a superlinear speed when increasing the threads for computing as shown in Fig. 6. This feature possesses an 

inherent advantage for accelerating scalable applications in the real world. The speedup observed for this task is lower than that of the Stick-on-Shelf task, likely due to the greater number of valid grasps available for this task. 

## VI. CONCLUSION 

In this work, we proposed B4P, a framework to address the problem of simultaneously finding grasp pose and motion plan for downstream placement tasks. By leveraging the parallelized bidirectional forests with path repair, the proposed framework demonstrates significant efficiency together with result completeness on diverse scenarios. Additionally, we investigated its inherent parallelism to achieve a superlinear speedup. 

We plan to extend the current work in the following directions: adding perception modules to get rid of the assumption of a perfect description of the environment and extending a re-grasping policy to tackle extreme situations that no compatible grasp poses in the initial object state. 

## REFERENCES 

- [1] N. Correll, K. E. Bekris, D. Berenson, O. Brock, A. Causo, K. Hauser, K. Okada, A. Rodriguez, J. M. Romano, and P. R. Wurman, “Analysis and observations from the first amazon picking challenge,” _IEEE Transactions on Automation Science and Engineering_ , vol. 15, no. 1, pp. 172–188, 2016. 

- [2] T. Wisspeintner, T. Van Der Zant, L. Iocchi, and S. Schiffer, “Robocup@ home: Scientific competition and benchmarking for domestic service robots,” _Interaction Studies_ , vol. 10, no. 3, pp. 392–426, 2009. 

- [3] D. Morrison, P. Corke, and J. Leitner, “Closing the loop for robotic grasping: A real-time, generative grasp synthesis approach,” _Robotics: Science and Systems XIV_ , pp. 1–10, 2018. 

- [4] H.-S. Fang, C. Wang, M. Gou, and C. Lu, “Graspnet-1billion: A largescale benchmark for general object grasping,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 11 444–11 453. 

- [5] K. Hang, M. Li, J. A. Stork, Y. Bekiroglu, F. T. Pokorny, A. Billard, and D. Kragic, “Hierarchical fingertip space: A unified framework for grasp planning and in-hand grasp adaptation,” _IEEE Transactions on robotics_ , vol. 32, no. 4, pp. 960–972, 2016. 

- [6] M. Elbanhawi and M. Simic, “Sampling-based robot motion planning: A review,” _IEEE Access_ , vol. 2, pp. 56–77, 2014. 

- [7] K. Harada, T. Tsuji, K. Nagata, N. Yamanobe, H. Onda, T. Yoshimi, and Y. Kawai, “Object placement planner for robotic pick and place tasks,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2012, pp. 980–985. 

- [8] J. A. Haustein, K. Hang, J. Stork, and D. Kragic, “Object placement planning and optimization for robot manipulators,” in _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2019, pp. 7417–7424. 

- [9] J. A. Haustein, K. Hang, and D. Kragic, “Integrating motion and hierarchical fingertip grasp planning,” in _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , 2017, pp. 3439– 3446. 

- [10] E. Plaku, K. E. Bekris, B. Y. Chen, A. M. Ladd, and L. E. Kavraki, “Sampling-based roadmap of trees for parallel motion planning,” _IEEE Transactions on Robotics_ , vol. 21, no. 4, pp. 597–608, 2005. 

- [11] A. Bicchi and V. Kumar, “Robotic grasping and contact: A review,” in _Proceedings 2000 ICRA. Millennium conference. IEEE international conference on robotics and automation. Symposia proceedings (Cat. No. 00CH37065)_ , vol. 1. IEEE, 2000, pp. 348–353. 

   - [14] T. Liu, Z. Liu, Z. Jiao, Y. Zhu, and S.-C. Zhu, “Synthesizing diverse and physically stable grasps with arbitrary hand structures using differentiable force closure estimator,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 1, pp. 470–477, 2021. 

   - [15] Y. Chen, X. Gao, K. Yao, L. Niederhauser, Y. Bekiroglu, and A. Billard, “Differentiable robot neural distance function for adaptive grasp synthesis on a unified robotic arm-hand system,” _arXiv preprint arXiv:2309.16085_ , 2023. 

   - [16] M. Sundermeyer, A. Mousavian, R. Triebel, and D. Fox, “Contactgraspnet: Efficient 6-dof grasp generation in cluttered scenes,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 13 438–13 444. 

   - [17] A. Orthey, C. Chamzas, and L. E. Kavraki, “Sampling-based motion planning: A comparative review,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 7, 2023. 

   - [18] W. Thomason, Z. Kingston, and L. E. Kavraki, “Motions in microseconds via vectorized sampling-based planning,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 8749–8756. 

   - [19] J. Bialkowski, S. Karaman, and E. Frazzoli, “Massively parallelizing the rrt and the rrt,” in _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2011, pp. 3513–3518. 

   - [20] A. Fishman, A. Murali, C. Eppner, B. Peele, B. Boots, and D. Fox, “Motion policy networks,” in _conference on Robot Learning_ . PMLR, 2023, pp. 967–977. 

   - [21] B. Sundaralingam, S. K. S. Hari, A. Fishman, C. Garrett, K. Van Wyk, V. Blukis, A. Millane, H. Oleynikova, A. Handa, F. Ramos, _et al._ , “Curobo: Parallelized collision-free robot motion generation,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 8112–8119. 

   - [22] M. Bhardwaj, B. Sundaralingam, A. Mousavian, N. D. Ratliff, D. Fox, F. Ramos, and B. Boots, “Storm: An integrated framework for fast joint-space model-predictive control for reactive manipulation,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 750–759. 

   - [23] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in _Proceedings 2000 ICRA. Millennium conference. IEEE international conference on robotics and automation. Symposia proceedings (Cat. No. 00CH37065)_ , vol. 2. IEEE, 2000, pp. 995–1001. 

   - [24] S. R. Lindemann and S. M. LaValle, “Incrementally reducing dispersion by increasing voronoi bias in rrts,” in _IEEE International Conference on Robotics and Automation, 2004. Proceedings. ICRA’04. 2004_ , vol. 4. IEEE, 2004, pp. 3251–3257. 

   - [25] A. Zeng, S. Song, K.-T. Yu, E. Donlon, F. R. Hogan, M. Bauza, D. Ma, O. Taylor, M. Liu, E. Romo, _et al._ , “Robotic pick-and-place of novel objects in clutter with multi-affordance grasping and cross-domain image matching,” _The International Journal of Robotics Research_ , vol. 41, no. 7, pp. 690–705, 2022. 

   - [26] J.-P. Saut, M. Gharbi, J. Cort´es, D. Sidobre, and T. Sim´eon, “Planning pick-and-place tasks with two-hand regrasping,” in _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2010, pp. 4528–4533. 

   - [27] M. D. Shanthi and T. Hermans, “Pick and place planning is better than pick planning then place planning,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 3, pp. 2790–2797, 2024. 

   - [28] Z. He, N. Chavan-Dafle, J. Huh, S. Song, and V. Isler, “Pick2place: Task-aware 6dof grasp estimation via object-centric perspective affordance,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 7996–8002. 

   - [29] R. A. Brooks, “Planning collision-free motions for pick-and-place operations,” _The International Journal of Robotics Research_ , vol. 2, no. 4, pp. 19–44, 1983. 

   - [30] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2012, pp. 5026–5033. 

- [12] R. Newbury, M. Gu, L. Chumbley, A. Mousavian, C. Eppner, J. Leitner, J. Bohg, A. Morales, T. Asfour, D. Kragic, _et al._ , “Deep learning approaches to grasp synthesis: A review,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3994–4015, 2023. 

- [13] M. T. Ciocarlie and P. K. Allen, “Hand posture subspaces for dexterous robotic grasping,” _The International Journal of Robotics Research_ , vol. 28, no. 7, pp. 851–867, 2009. 

