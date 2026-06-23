---
citation_key: Jiao2025Integration
arxiv_id: 2508.18627
arxiv_url: "https://arxiv.org/abs/2508.18627"
title: "Integration of Robot and Scene Kinematics for Sequential Mobile Manipulation Planning"
authors_short: "Ziyuan Jiao et al."
year: 2025
direction_tag: G_subgoal_optimization
source: pymupdf4llm
converted_at: 2026-06-23T18:21:52Z
origin: ai+web
reviewed: false
---

1 

# Integration of Robot and Scene Kinematics for Sequential Mobile Manipulation Planning 

Ziyuan Jiao, _Member, IEEE_ , Yida Niu, _Student Member, IEEE_ , Zeyu Zhang, _Member, IEEE_ , Yangyang Wu, Yao Su, _Member, IEEE_ , Yixin Zhu, _Member, IEEE_ , Hangxin Liu, _Member, IEEE_ and Song-Chun Zhu, _Fellow, IEEE_ 

_**Abstract**_ **—We present a Sequential Mobile Manipulation Planning (SMMP) framework that can solve long-horizon multi-step mobile manipulation tasks with coordinated whole-body motion, even when interacting with articulated objects. By abstracting environmental structures as kinematic models and integrating them with the robot’s kinematics, we construct an Augmented Configuration Apace (A-Space) that unifies the previously separate task constraints for navigation and manipulation, while accounting for the joint reachability of the robot base, arm, and manipulated objects. This integration facilitates efficient planning within a tri-level framework: a task planner generates symbolic action sequences to model the evolution of A-Space, an optimizationbased motion planner computes continuous trajectories within A-Space to achieve desired configurations for both the robot and scene elements, and an intermediate plan refinement stage selects action goals that ensure long-horizon feasibility. Our simulation studies first confirm that planning in A-Space achieves an 84.6% higher task success rate compared to baseline methods. Validation on real robotic systems demonstrates fluid mobile manipulation involving (i) seven types of rigid and articulated objects across 17 distinct contexts, and (ii) long-horizon tasks of up to 14 sequential steps. Our results highlight the significance of modeling scene kinematics into planning entities, rather than encoding task-specific constraints, offering a scalable and generalizable approach to complex robotic manipulation.** 

_**Index Terms**_ **—Sequential mobile manipulation planning, kinematics, trajectory optimization, and service robot.** 

## I. INTRODUCTION 

**A** UTONOMOUSinto diverse environments in human society. Whether as-robots are increasingly being integrated sisting people in daily activities [3, 4] or operating in outposts such as space stations or extraterrestrial bases [5, 6], robot operations face significant challenges in performing sequential 

_Corresponding author: Hangxin Liu._ 

This article is an extended version of IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), Oct., 2021 [1, 2]. 

This work was supported in part by the National Natural Science Foundation of China (Grant No.52305007). 

Ziyuao Jiao, Yida Niu, Zeyu Zhang, Yangyang Wu, Yao Su, Hangxin Liu, and Song-Chun Zhu are with State Key Laboratory of General Artificial Intelligence, Beijing Institute for General Artificial Intelligence (BIGAI), Beijing 100080, China (emails: jiaoziyuan@bigai.ai; niuyida@bigai.ai; zhangzeyu@bigai.ai; wuyangyang@bigai.ai; suyao@bigai.ai; liuhx@bigai.ai; sczhu@bigai.ai). 

Yida Niu is also with Institute for Artificial Intelligence, Peking University, Beijing 100871, China. 

Yixin Zhu is with the School of Psychological and Cognitive Sciences, and the Institute for Artificial Intelligence, Peking University, Beijing 100871, China (email: yixin.zhu@pku.edu.cn). 

Song-Chun Zhu is also with Institute for Artificial Intelligence and School of Artificial Intelligence, Peking University, Beijing 100871, China, and also with Department of Automation, Tsinghua University, Beijing 100084, China. 

mobile manipulation tasks that require a range of manipulation skills and the ability to sequence these skills in expansive workspaces. 

Fig. 1(a) illustrates a typical Sequential Mobile Manipulation Planning (SMMP) scenario. Operating in cluttered workspaces poses significant challenges due to complex obstacle configurations [7]. Robots are often required to balance both navigation and manipulation, _i.e_ ., mobile manipulation, to accomplish their goals [8, 9]. Moreover, contact with diverse structures and objects introduces a wide range of task objectives and constraints, which are difficult to emulate in advance, particularly when dealing with articulated objects [1, 10, 11]. Compounding this difficulty, robot actions can change the environment in ways that hinder the feasibility of future steps in long-horizon tasks [12–15]. Therefore, the successful execution of an action in long-horizon mobile manipulation requires not only coordinating base-arm-object trajectories for individual steps, but also reasoning about the long-term implications of each action on future task feasibility. 

Achieving coordinated trajectories of the robot’s base, arm, and manipulated object can become computationally intractable in long-horizon tasks due to the inherently interdependent configuration spaces during interactions, as shown in Fig. 1(b). Consequently, the likelihood of finding connected feasible paths across consecutive steps is low, and costly backtracking is often required when the planner encounters dead ends. A hierarchical strategy is typically employed to decompose the task execution into a sequence of primitive motions [12, 14, 16], facilitating more efficient trajectory generation and reducing computation costs in the face of errors. However, current hierarchical methods such as Task and Motion Planning (TAMP) are primarily effective only for pick-and-place tasks [17–19], failing to scale to complex mobile manipulation tasks. This limitation arises because complex mobile manipulation tasks require tightly coordinated navigation and manipulation, which are difficult to express symbolically. Semantic symbols often fail to capture critical geometric constraints necessary for task success, such as valid base positioning, interdependent base and arm movements, and collision avoidance. For example, the tasks in Fig. 1 involve coupled base-arm-object interactions that would demand an intractable number of symbolic predicates to model accurately. 

In stark contrast, humans exhibit fluid manipulation skills and interact adeptly with their environment. Theories in cognitive psychology and philosophy suggest the concept of body schema: humans maintain a flexible representation of their 

2 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0002-01.png)


Fig. 1: **An exemplar household task illustrating the advancement of proposed Sequential Mobile Manipulation Planning (SMMP) framework with A-Space compared to traditional planning.** (a) In this long-horizon task, the robot must (T1) remove the chair to approach the bedroom door, (T2) open the door and pass through it, and (T3) open the kitchen drawer. (b) Separated base-arm-object planning faces inherent challenges: as the base moves, the arm and object’s configuration space evolves, frequently making initially feasible trajectories infeasible. This approach simplifies the planning complexity but may require costly backtracking across different configuration spaces, particularly in tasks demanding whole-body coordination. (c) By leveraging A-Space, separate configuration spaces are unified through Augmented Kinematic Representation (AKR), incorporating various task constraints to enable coordinated base-arm-object trajectories across multiple steps via trajectory optimization, reducing the need for hierarchical backtracking. 

bodies, enabling them to treat manipulated objects as extensions of their limbs during interactions [20, 21]. Embodied cognition studies further highlight that human intelligence is deeply intertwined with the environment [22, 23]. 

Drawing from these insights, we propose to treat the environment and the robot embodiment as a whole for an efficient solution to mobile manipulation tasks. Specifically, we consolidate kinematic abstractions of scene elements [24], robot arm, and navigational movements into an Augmented Kinematic Representation (AKR). This consolidation merges originally separated yet entangled robot and object’s configuration spaces into a single one, which we termed Augmented Configuration Space (A-Space), as depicted in Fig. 1(c). From this perspective, planning sequential mobile manipulation in A-Space can jointly account for the reachability of the robot base, arm, and manipulated objects and their inherent motion constraints, thus better ensuring spatial feasibility of sophisticated robot movements and resolving action temporal dependency among long-horizon tasks. 

As A-Space is highly complex due to the extended Degree of Freedoms (DoFs), we design a tri-level planning framework for efficient planning within it. By formulating an optimization-based motion planner, we can compute continuous trajectories to reach the desired configurations of both robot and scene entities, resulting in coordinated whole- 

body motions that satisfy relevant constraints. Furthermore, we design a task planner that defines symbolic states more intuitively and models actions along with their effects on A-Space, thereby enabling validation of motion feasibility over extended horizons by traversing temporally successive configuration spaces. Extending our previous foundation in task planning and motion planning [1, 2], a newly designed plan refinement algorithm further combines them to resolve potential conflicts between anticipated future actions. Together, these components form a scalable SMMP framework capable of handling long-horizon mobile manipulation tasks involving diverse interactions within complex environments. We demonstrate the framework’s effectiveness on a real robot system by performing coordinated base-arm-object motions across 17 diverse scenarios involving complex environmental structures. Moreover, the system successfully completes a 14-step longhorizon mobile manipulation task in a cluttered living room, with each step characterized by unique contact configurations. Additional simulation studies further validate our approach, quantifying improvements in execution efficiency and planning success rates when using A-Space compared to traditional planning paradigms. 

Our contribution is fourfold: 

1) We introduce an SMMP framework that solves longhorizon mobile manipulation tasks, with a newly proposed 

3 

   - plan refinement algorithm that considers future actions while generating the motion planning problem for the current action, effectively increasing task success rates in complex long-horizon SMMP problems. 

- 2) We model the mobile manipulation planning problem from the AKR perspective, formulating the mobile manipulation planning problem as a trajectory optimization problem within the A-Space that integrates task specifications. 

- 3) We design a Planning Domain Definition Language (PDDL)-based task planning domain describing the evolution of the A-Space, generalizing it to various daily longhorizon indoor mobile manipulation tasks. 

- 4) Through simulations, we validate the proposed method, achieving an 84.6% improvement in success rate over baseline methods. With extensive experiments on physical mobile manipulators, we demonstrate the proposed method’s feasibility across 7 types of rigid and articulated objects in 17 different contexts, with long-horizon tasks involving up to 14 steps. 

## _A. Overview_ 

The remainder of this article is organized as follows. Sec. II reviews the literature and compares existing research with the contributions of this work. Sec. III introduces the proposed AKR-based modeling method for mobile manipulation. Based on the idea of AKR, Sec. IV formulates the corresponding motion planning and task planning setups, and Sec. V elaborates the newly proposed plan refinement algorithm that bridges AKR-based motion planning with task planning components into a coherent SMMP system. Finally, Sec. VI and Sec. VII demonstrate the efficacy of AKRs through simulations and experiments, respectively. Sec. VIII concludes the paper with an in-depth discussion of key findings and future directions. 

## II. RELATED WORK 

## _A. Mobile Manipulation_ 

Recently, notable efforts have focused on algorithms and system implementations to coordinate navigation and manipulation for mobile manipulation, especially within household environments. For instance, graph search [25], equilibrium point control [26], adaptive control [10], impedance control [27], and model predictive control [28] have been introduced for tasks like opening doors and drawers. For object retrieval or relocation in confined and cluttered spaces, methods such as the coevolutionary algorithm in [29], which jointly optimizes grasping and base poses, and adaptive dimensionality reduction in [30], which manages the high DoFs search space, have shown promise. Other techniques include inverse kinematics branching for iterative optimization of base and joint motions [31] and holistic control of the arm and base as a unified structure [32]. While existing robotic planning methods achieve promising results on isolated tasks, such as door opening or object retrieval in controlled environments, their specialized, task-specific designs cannot generalize to broader scenarios requiring coordinated manipulation by the mobile base, manipulator arm, and target object. Yet, our SMMP scenario demands manipulation of objects with diverse 

kinematic structures in varied environments, where successful task execution critically depends on coordination among the mobile base, manipulator arm, and target object. In addition, deep Reinforcement Learning (RL) has recently gained popularity for manipulation tasks involving rich interactions. For example, [33] trains an RL policy for object retrieval on a physical manipulator, and [34] uses deep RL for whole-body control in door-opening tasks, while [35] abstracts the action space into base and arm sub-goals for long-horizon tasks in simulated environments. Although RL offers advantages for complex interaction planning, learned policies often suffer from poor transferability from simulation to real-world applications and do not scale effectively to long-horizon tasks due to substantial training time. 

## _B. Multi-Modal Motion Planning (MMMP)_ 

In sequential manipulation tasks, robots must repeatedly establish and release contact with various objects, exhibiting multi-modal behavior: contact states (discrete modes) constrain robot motions, effectively partitioning the environment’s configuration space into interconnected manifolds. Transitions between manifolds indicate potential mode changes. Building on this concept, MMMP methods [36–40] aim to find feasible trajectories across different manifolds, producing motion plans applicable to sequential mobile manipulation tasks. For example, Hauser _et al_ . [38] propose a scalable algorithm that randomly samples mode switches and motion paths on a known mode transition graph to generate a solution plan, while Toussaint _et al_ . [40] abstracts contact modes using differentiable physics, enabling tool-use planning. These methods yield impressive results in planning multi-step actions, but they share a limitation common to MMMP: their planning domains are specifically designed and restricted to geometric features, necessitating extensive efforts in custom planner design and mode transition definitions for numerous contact modes. This proves inadequate for semantically rich environments where object relationships transcend simple contacts [18]. While the MMMP approach shares similarities with our work in terms of abstracting actions through contacts, the proposed AKR enables the use of off-the-shelf planning languages and aims to accommodate a broad range of mobile manipulation tasks without defining specific actions for each task. 

## _C. TAMP_ 

Thanks to the development of PDDL [41] and other planning languages, complex symbolic planning can be solved using standard algorithms [42, 43]. While symbolic planning effectively captures abstract concepts, it struggles to represent the feasibility of robot motions. This limitation has led the robotics community to integrate MMMP concepts with symbolic task planners, forming the field of TAMP [18]. Current TAMP approaches typically employ a bidirectional interface between task and motion planning [12, 44–46], but they remain computationally expensive due to their reliance on dense sampling in high-dimensional spaces [7]. Recent work has sought to address these inefficiencies: Zhang _et al_ . [47] optimize symbolic state spaces to reduce redundant 

4 

navigation actions, Yang _et al_ . [48] leverage Vision-Language Models (VLMs) to propose high-level subgoals to prune search spaces, and Sung _et al_ . [49] learns back-jump heuristics that identify the culprit action and bypass irrelevant backtracking steps. However, the iterative nature of TAMP approaches still imposes significant computational overhead, as failed motion planning attempts trigger backtracking and replanning of action sequences. As a result, many TAMP approaches simplify motion planning and limit themselves to basic manipulation tasks, avoiding the complexity of designing intricate planning domains and specific motion planners for complex mobile manipulation tasks. 

Departing from traditional efforts in TAMP approaches that either optimize search strategies or redesign task-motion interfaces, this work proposes a new perspective by planning mobile manipulation tasks through the AKR. The proposed AKR constitutes an effective intermediate representation that can benefit TAMP in solving challenging sequential mobile manipulation tasks by improving computational efficiency through reducing intermediate variables and facilitating optimizationbased motion planning. 

This work builds upon our preliminary results presented in Jiao _et al_ . [1, 2]. The extension features a more comprehensive literature review, the introduction of a new plan refinement algorithm that enhances planning success rates by selecting key AKR configurations throughout the action sequence, and extensive benchmarking that compares our SMMP framework to baselines using off-the-shelf motion planners. Additionally, we include implementation and large-scale experimentation on a physical mobile manipulator platform. 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0004-04.png)


Fig. 2: **Modeling a mobile manipulation task from the proposed SMMP perspective.** Constructing an AKR involves four key inputs: the manipulator’s kinematics _T[R]_ , object kinematics _T[O]_ , a virtual mobile base _T[B]_ , and a virtual attachment joint _sea_ . Given the articulated nature of the drawer, its kinematic model requires inversion to maintain a tree. 

## _B. AKR Modeling for Mobile Manipulation_ 

## III. AKR MODELING 

This section describes three key steps for integrating robot and scene models into one cohesive kinematic representation, termed Augmented Kinematic Representation (AKR). 

## _A. Kinematic Representation_ 

The kinematic representation used in this article is defined as a tree _T_ “ p _V, S_ q where the rigid bodies of an articulated object are described as links _vi_ P _V_ , while their inherent motion constraints and spatial relations are represented by joints _sij_ P _S_ . Specifically, the node set _V_ includes a set of links _vi_ “ x _oi, Fi_ y; each encodes a full geometry model _oi_ ( _e.g_ ., a triangular mesh or empty for dummy link), and a link frame _Fi_ . In addition, the root node of _T_ is denoted as _vr_ . The edge set _S_ includes a set of joints _sij_ “ x _rij,[i] j[T]_[y][;][each] encodes the motion constraints _rij_ ( _e.g_ ., bounded revolute or prismatic motion along an axis) between the parent link _vi_ and the child link _vj_ , and a spatial transformation _[i] j[T]_[from] the parent link frame _Fi_ to the child link frame _Fj_ . Based on the above notations, a kinematic chain _Cij_ “ p _Vij, Sij_ q contains only nodes _Vij_ Ď _V_ and edges _Sij_ Ď _S_ that belong to a path between a node _vi_ and one of its descendant nodes _vj_ in _T_ . 

To construct an AKR, _T[A]_ , four key inputs are required: the manipulator’s kinematics _T[R]_ , object kinematics _T[O]_ , a virtual mobile base _T[B]_ , and a virtual attachment joint _sea_ between the robot end-effector and the link to be grasping on the object. Fig. 2 illustrates the constructed AKR for opening a cabinet door with a physical mobile manipulator platform. 

**AKR modeling** for a mobile manipulation planning problem first involves integrating the virtual mobile base into the kinematic model of the manipulator. During interactions, the post-inversion object’s kinematics is further integrated into the AKR through a virtual attachment joint. The AKR is extended to the inverted object model’s terminal link while maintaining its serial chain structure (see Fig. 2). In our application, we assume that _T[R]_ and _T[O]_ are known. However, obtaining the virtual mechanisms and constructing _T[A]_ involve more nuanced operations. The following section will detail these operations. 

**Virtual mobile base** _T[B]_ reflects the motion possibilities of the mobile base. In Fig. 2, the manipulator with an omnidirectional mobile base can theoretically achieve free, stable motion on the ground plane. Consequently, a kinematic chain with three consecutive joints (two perpendicular prismatic joints are connected in serial to imitate linear motion, followed by one revolute joint at the rotation center of the mobile base to imitate angular motion) is sufficient to describe the motion of the base. 

5 

**Algorithm 1:** Kinematics Inversion 

||**Algorithm 1:** Kinematics Inversion|
|---|---|
||**Input**<br>**:** The kinematics: _T_ “ p_V, S_q,|
|**1** <br>**2** <br>**3** <br>**4** <br>**5**|The root node of _T_: _vr_,<br>The attachable link node: _va_.<br>(not necessarily the terminal node)<br>**Output :** The inverted kinematics: _T_ inv “ p_V, S_invq.<br> // Initialization<br> _S_inv Ð tu;<br> // Get kinematic chain from _vr_ to _va_<br> p_Vra, Sra_q Ð_FindPath_p_T , vr, va_q;<br> // Inversion of the kinematic chain|
|**6 **<br>**7**|**foreach** t_sij, sjk_u Ă_Sra_ **do**<br>p_rij, i_<br>_jT_q Ð_sij_, p_rjk, j_<br>_kT_q Ð_sjk_;|
|**8**<br>**9**<br>**10**<br>**11**<br>**12**|**if** _vk is equal to va_ **then**<br>_s_˚<br>_ji_ Ð p_rji, j_<br>_kT_´1q;<br>_s_˚<br>_kj_ Ð p_rkj, I_4q;<br>_S_inv Ð_S_inv Y t_s_˚<br>_ji, s_˚<br>_kj_u;<br>**else**|
|**13**<br>**14**|_s_˚<br>_ji_ Ð p_rji, j_<br>_kT_´1q;<br>_S_inv Ð_S_inv Y t_s_˚<br>_ji_u;|
|||
|**15**|// Inversion of branches|
|**16 **<br>**17**<br>**18**<br>**19**<br>**20**<br>**21**|**foreach** _vj_ P_Vra and vj_ ‰_vr_ **do**<br>**foreach** _sjk_ P_S and sjk_ R_Sra_ **do**<br>p_rjk, j_<br>_kT_q Ð_sjk_;<br>p_rij, i_<br>_jT_q Ð_sij,_ where _sij_ P_S_inv;<br>_s_˚<br>_jk_ Ð p_rjk, i_<br>_jT j_<br>_kT_q;<br>_S_inv Ð_S_inv Y t_s_˚<br>_jk_u;|
|||
|**22 **|**foreach** _vi_ P_V and vi_ R_Vra_ **do**|
|**23**<br>**24**|**if** D_sij_ P_S_ **then**<br>_S_inv Ð_S_inv Y t_sij_u;|
|||
|**25**|// Get the inverted kinematics|
|**26**|_T_ inv Ð p_V, S_invq;|



**Virtual attachment joint** _sea_ characterizes the motion constraints and spatial relation between the robot and the scene after integration. As shown in Fig. 2, by inserting the _sea_ between the manipulator’s end-effector link _ve_ and an attachable link _va_ in the object model, the kinematics of the mobile manipulator and the manipulated object are integrated. If a manipulated object _T[O]_ is articulated and the attachable link is not the root node of _T[O]_ , its kinematic model must be inverted before integration to ensure that _T[A]_ remains a tree ( _i.e_ ., each node within a tree has at most one parent node). 

**Kinematics inversion** process reverses the kinematic model of the manipulated object while retaining its motion constraints and geometric consistencies, as shown in Alg. 1. Our kinematic tree representation defines transformations from parent to child link frames, with motion constraints ( _i.e_ ., joints) specified relative to the child frame. Therefore, kinematics inversion requires non-trivial adjustments to each joint’s spatial transformation, in addition to simple parent-child inversions, since joints constrain child link motion relative to their local frame. The algorithm first identifies the main branch (Line 4) between the base link (the root node of _T_ ) and the attachable link (identified in _sea_ ), including all intermediate joints and nodes. Transformations along this kinematic chain (between _vr_ and _va_ ) are then updated (Lines 6-14). The motion planner treats side branches as static, but their proper geometric transformation (Lines 16-24) remains critical for maintaining self-collision avoidance in the AKR representation. Fig. 2 illustrates the post-inversion cabinet kinematics and its inte- 

gration into the AKR. 

From the AKR perspective, we can formulate a _single-step mobile manipulation_ task as motion planning in A-Space ( _i.e_ ., the configuration space of AKR), with task execution represented by AKR state transitions. Unlike decoupled approaches that treated the object as task-specific constraints imposed on the robot, _e.g_ ., [50], the AKR simultaneously incorporates: 1) kinematic constraints for both robot and manipulated object, 2) path constraints for end-effector during interaction, and 3) self-collision avoidance—enabling generation of safe, coordinated base-arm-object motions. By generalizing to objects with known kinematics, the AKR eliminates task-specific modeling requirements for diverse objects and environments. This approach achieves effective whole-body motion optimization by eliminating the need for iterative backtracking in basearm-object coordination at the task level. 

## IV. PLANNING IN THE A-SPACE 

In this section, we first formulate motion planning problems for _single-step_ mobile manipulation tasks in A-Space, and solve them via warm-started trajectory optimization. Then, we tackle the _multi-step_ SMMP problem through an AKRbased task planning, supporting the generation of whole-body trajectories for interacting with multiple objects sequentially, implemented via three action predicates. 

## _A. Motion Planning in A-Space_ 

Consider a standard single-arm mobile manipulation task, in which a mobile manipulator interacts with an articulated object within the scene. The state vector _**q**_[J] “ r _**q**[B] ,_ _**q**[R] ,_ _**q**[O]_ s[J] P _Q_[free] describes the state of the virtual mobile base _T[B]_ , the manipulator _T[R]_ , and the articulated object _T[O]_ , respectively. Notably, these joints belong to a serial kinematic chain _C_ , which consists of a root node _vw_ and a non-root node _vb_ , as illustrated in Fig. 2. The remaining joints that do not belong to _C_ are assumed to be fixed during motion planning. _Q_[free] Ă R _[n]_ is the collision-free subset of A-Space. The motion planning problem in A-Space is equivalent to finding a _T_ -step path _**q**_ 1: _T_ “ x _**q**_ 1 _,_ _**q**_ 2 _, . . . ,_ _**q** T_ y P _Q_[free] , which can be formulated and solved by trajectory optimization. 

Following Jiao _et al_ . [1], the trajectory optimization problem is formulated as: 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0005-12.png)



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0005-13.png)



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0005-14.png)


where Eq. (1) penalizes the overall traveled distance and overall non-smoothness of the trajectory _**q**_ 1: _T_ . _**W** v_ and _**W** a_ are two diagonal weighting matrices for each DoF, _δ_ _**q** t_ and _δ_ _**q**_ 9 _t_ are the finite forward difference and second-order finite central difference of _**q** t_ , respectively. The equality constraint Eq. (2) specifies the physical constraints of the object or the environment during interactions. Failing to account for this type of constraint ( _e.g_ ., the kinematic constraint of the robot and the scene) may damage the robot or the manipulated 

6 

object, resulting in failed executions. The goal of a mobile manipulation task is bounded through an inequality constraint Eq. (3) with a tolerance _ξ_ goal. The function _f_ task : R _[n]_ Ñ R _[k]_ maps _**q** T_ from the configuration space _Q_ to the task-dependent goal space _G_ P R _[k]_ . For instance, in an object-picking task, _f_ task represents the forward kinematics used to compute the robot’s end-effector pose, while _**g**_ goal denotes the end-effector goal pose before grasping. In a door-opening task, _f_ task maps the AKR state to the door’s joint configuration, and _**g**_ goal represents the desired joint angle for the door. 

Additional safety constraints are imposed during trajectory optimization. Without loss of generality, we assume an omnidirectional base and only kinematic constraints in this paper. However, additional constraints, such as nonholonomic constraints for non-omnidirectional mobile bases could be formulated into the optimization problem by incorporating additional terms [51]: 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0006-03.png)



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0006-04.png)



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0006-05.png)


where | ¨ |[`] is defined as | _x_ |[`] “ maxp _x,_ 0q. Eqs. (4) to (6) are inequality constraints that define the joint capability and implicitly constrain the workspace of both the robot and the scene. Eq. (7) and Eq. (8) penalize collisions with obstacles and self-collisions, respectively. _N_ link and _N_ obj are the number of links that belong to the AKR and the number of obstacle objects within the scene, respectively. distsafe is a predefined safety distance, and _sd_ p¨q is a function that calculates the signed distance between a pair of objects. _ξ_ dist is a collision tolerance parameter. The formulated problem is solved through trajectory optimization [52]. 

Unlike sampling-based methods, optimization-based motion generation methods rely on gradient descent algorithms and can easily become trapped in undesired local minima near the initial guess [52, 53]. Consequently, a proper trajectory initialization ( _i.e_ ., warm start) is essential to improve the optimization results. However, the high dimensionality of AKR presents significant challenges. While sampling-based methods can provide paths as initialization seeds for optimization, they become computationally expensive in high-dimensional AKR spaces. Simple interpolation between start and goal states is insufficient, as base movements are often constrained by cluttered obstacles. Solving for coordinated movements simultaneously creates a complex optimization landscape with many poor local minima, making convergence difficult without good initialization. Therefore, an efficient initialization strategy that balances computational cost with solution quality is crucial for making AKR-based planning practical. 

Therefore, we devise an A[‹] -based trajectory initialization method to effectively guide trajectory optimization away from 

poor local minima without requiring excessive computational time. Given the initial state _**q** i_ and the goal state _**q** g_ , this method utilizes A[‹] to find a feasible path from the current location _**q**[B] i_ to the goal location _**q**[B] g_ of the mobile base. Subsequently, it linearly interpolates the manipulator’s joint state from _**q**[R] i_ to _**q**[R] g_[.][While][the][method][itself][is][presented] as a simple design, it is pivotal to our framework’s practical efficacy. The initialization phase aims to generate coarse, collision-free base paths (via _A_[‹] ) to guide subsequent trajectory optimization. Without this step, the solver often converges to local minima—for example, favoring shorter but colliding base paths over safer, longer ones. Appendix A provides quantitative comparisons with baselines, effectiveness analysis, and discussions of trade-offs and limitations. 

## _B. Task Planning for Sequential Tasks_ 

To solve a SMMP problem, a robot must break it down into a sequence of temporally feasible actions, necessitating task planning. Following the classic formalization of task planning, we describe the environment by a set of states _E_ (of note, _E_ and _Q_ are unnecessarily identical). Possible transitions between these states are defined by _A_ Ď _E_ ˆ _E_ , where a transition _a_ “ x _e, e_[1] y P _A_ alters the environment state from _e_ P _E_ to _e_[1] P _E_ . The task planning goal is to identify a sequence of transitions _a_ 1: _N_ that alter the environment from its initial state _e_ 0 P _E_ to a goal state _eN_ P _Eg_ , where _Eg_ Ď _E_ is a set of goal states. Traditional task planning involves defining meaningful symbolic actions _A_ and states _E_ and often assumes a robot can execute the elementary actions. However, these symbolic actions necessitate substantial manual design effort to be instantiated successfully at the motion level. From the AKR perspective, the action is defined as changes to the AKR structure and corresponding A-Space, transforming the SMMP problem into a series of AKR structural modifications. 

In this section, we describe how actions defined using standard planning language ( _e.g_ ., PDDL [41]) can be used to properly formulate a task planning problem, and how the planned actions sequence can be realized by motion planning within A-Space. We start by making connections between the action semantics and the actual manipulation behaviors, before explaining how motion planners process the predicates and variables in the action definitions. 

**goto-akr (akr,** _**q**_ **1 ,** _**q**_ **2 ):** This predicate moves the A- Space state from pose _**q**_ 1 to the desired pose _**q**_ 2. It represents the tasks that do not require interaction with the environment, wherein the AKR structure remains unchanged. Pure navigation is a typical action that falls into this category. 

**pick-akr (akr, o, s):** This predicate moves the AKR to an object, o, with kinematics _T_ and extends the current AKR’s kinematics, by adding a virtual attachment joint sÐ _sea_ to connect the object and the arm’s end-effector. In practice, _sea_ encodes both the end-effector’s grasping pose and the associated grasp constraints between the robot and the object. pick-akr represents the group of tasks that require mobile manipulators to interact with the environment, _e.g_ ., picking up an object or grasping a handle. 

7 

**place-akr (akr, o, g):** This predicate moves the object, o, connected to akr to an object-specific goal state g, while the object to be manipulated is incorporated into the AKR and imposes kinematic constraints. For example, g represents the target door state ( _e.g_ ., opened) in door-opening tasks or the desired object placement location ( _e.g_ ., onTable) in object relocation tasks. Once the goal state is reached, place-akr breaks the current AKR at the virtual attachment joint where it connects the mobile manipulator and the object, and the object will be placed where it was disconnected from the AKR. place-akr represents the group of tasks for which mobile manipulators stop interacting with the environment, such as placing an object on the table. 

The primary challenge in generalizing actions across objects stems from heterogeneous task-specific constraints tied to scenes and objects, which is pivotal for generating executable trajectories in different mobile manipulation tasks. By embedding these constraints into scene kinematics, the AKR achieves a unified action definition and enables a general formulation of trajectory optimization for both rigid and articulated objects with known kinematics. This AKR-based formulation alleviates the need to define task-specific actions for manipulating different objects, which in turn reduces the need for intermediate subgoals ( _e.g_ ., moving the mobile base near the object before manipulation) and allows more dexterous exploration of the A-Space. 

## V. SEQUENTIAL MOBILE MANIPULATION PLANNING 

In this section, we first present the operation of the plan refinement algorithm. We then describe how the algorithm resolves motion infeasibility in sequential tasks by selecting favorable action parameters through a goal selection process. 

## _A. Plan Refinement for Sequential Tasks_ 

To illustrate how symbolic action predicates (as defined in Sec. IV-B) govern the evolution of the AKR structure and how plan refinement resolves motion feasibility, consider the example in Fig. 1(a). The robot must first relocate a chair blocking a door (T1) and then open the door to exit (T2), interacting with two articulated objects. The action sequence includes four steps as shown in Fig. 3. 

The AKR evolving with each action depicts possible end states for each step. The first action, pick-akr, generates a whole-body motion for the akr (virtual mobile base and manipulator) to grasp the chair. After grasping, akr integrates the chair’s kinematics into a new akr. The resulting A- Space captures the kinematics of the mobile base, manipulator, and chair, while enforcing a planar constraint on the new akr’s end-effector ( _i.e_ ., the chair’s base link) to emulate the chair’s planar motion across the floor. These constraints are collectively considered during trajectory optimization. 

For place-akr, the robot must choose a chair placement that avoids blocking subsequent door access. We sample valid configurations within A-Space and illustrate two representative configurations (second column in Fig. 3(c)). Without considering future actions, both placements are acceptable, as the chair no longer obstructs the door. After placing the chair, 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0007-09.png)


Fig. 3: **An illustration of the proposed plan refinement algorithm for a sequential task.** The task planner first generates a sequence of symbolic actions representing the evolution of the AKR configuration space, indicating robot-environment interactions. Then, the plan refinement algorithm ensures motion feasibility among sampled AKR end configurations for consecutive actions. 

the akr detaches it, reverting to the mobile manipulator. The subsequent pick-akr action finds the path to approach the door handle. By sampling valid configurations (third column in Fig. 3), we can distinguish between motion-infeasible (red) and motion-feasible (green) pairs. Due to the presence of motion-infeasible pairs, plan refinement becomes necessary. 

The plan refinement process acts as a receding horizon, evaluating feasibility across the action sequence. For instance, the last configuration in Fig. 3(c) (fourth column) is infeasible due to the subsequent action that approaches the drawer, which requires the robot to pass through the door. This example demonstrates how previously defined actions govern the evolution of the AKR structure and underscores the necessity of plan refinement in resolving motion feasibility. The subsequent section formalizes this procedure, focusing specifically on the selection of action parameters. 

## _B. Action Parameter Selection from Key Configuration Set_ 

The AKR-based motion planner requires two sets of action parameters to generate trajectories. The first, end-effector poses s, specifies grasps between the robot’s end-effector and objects during pick-akr actions. These poses are obtained through grasp synthesis methods ( _e.g_ ., [54]) or predefined for known objects, as grasp generation lies beyond the scope of this work. The second set, g, defines object-centric states aligned with symbolic predicates, such as an opened door or an object placement goal like onTable, and must be instantiated appropriately within the object’s configuration space for trajectory optimization [55]. 

Improper action parameters values can lead to motion infeasibility, as they do not fully capture the state of the akr, and variations in akr states impose different feasibility conditions on subsequent actions, as illustrated in Fig. 3. While multiple 

8 

## **Algorithm 2:** Select KCS 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0008-02.png)


**----- Start of picture text -----**<br>
Input : Action sequence segment: an : n ` l<br>Current AKR: Ta [A] n ´1<br>Current AKR state: q an ´1<br>Ouput : Preferred key configuration set: q [˚] an : n ` l<br>Params: No. of candidate configurations: Nc<br>No. of clusters: Nk<br>No. of anticipated subsequent actions: l<br>1 q an ´1: n ´1 Ð x q an ´1 y<br>2 K Ð t q an ´1: n ´1 u<br>3 for i  P  n  :  n  `  l do<br>4 Ktemp Ð H<br>5 // Update A-Space according to Sec. IV-B.<br>6 Ta [A] i [Ð] [ ConstructAKR] [p] [T] a [A] i ´1 [, a][i] [q]<br>7 // Generate valid configurations within<br>A-Space.<br>8 Qai Ð  SampleV alidConfigurations p Ta [A] i [, N][c] [q]<br>9 // Pruning similar configurations through<br>down-sampling.<br>10 Q [1] ai [Ð] [ Downsample] [p] [Q][a] i [, N] k [q]<br>11 // Predict and store feasible KCS<br>12 for q an ´1: i ´1 P  K do<br>13 for q ai P  Q [1] ai [do]<br>14 if CheckMotionFeasibility p Ta [A] i [,] [q] [a] n ´1: i ´1 [,] [q] [a] i [q]<br>then<br>15 q an ´1: i Ð q an ´1: i ´1 .append p q ai q<br>16 Ktemp Ð  Ktemp  Y t q an ´1: i u<br>17 K Ð  Ktemp<br>18 // Select KCS of lowest cost<br>19 q [˚] an ´1: n ` l [Ð] [ SelectBest] [p] [K] [q]<br>20 q [˚] an : n ` l [Ð] [q] [˚] an ´1: n ` l [zt] [q] [a] n ´1 [u]<br>**----- End of picture text -----**<br>


chair placements are feasible in a bedroom, some configurations (marked red) obstruct the robot from approaching the door due to self-blocking. This challenge is exacerbated in confined spaces with limited configuration space. To ensure feasibility across action sequences, our method jointly optimizes goal states with future steps, resolving conflicts during plan refinement to avoid such pitfalls. 

The exhaustive motion planning for all possible action parameters is computationally demanding, with time complexity growing exponentially with action sequence length, rendering it impractical. To address this challenge, we propose a plan refinement algorithm designed to efficiently select the goal AKR state by considering a given number of anticipated subsequent actions. This approach aims to improve the likelihood of success for sequential tasks. 

Specifically, let _**q** an_ be a possible goal AKR configuration for the action _an_ and _Qan_ be the A-Space during that action, and _Qan_ : _n_ ` _l_ be the Cartesian product of A-Spaces: _Qan_ : _n_ ` _l_ “ _Qan_ ˆ _Qan_ `1 ˆ _. . ._ ˆ _Qan_ ` _l_ , where _l_ is the window length suggesting the number ( _l_ ` 1) of anticipated subsequent actions. Our aim is to find a Key Configuration Set (KCS) _**q**_[˚] _an_ : _n_ ` _l_[“][x] _**[q]**[a] n[,]_ _**[q]**[a] n_ `1 _[, . . . ,]_ _**[q]**[a] n_ ` _l_[y][P] _[Q][a] n_ : _n_ ` _l_[so] that transition among every two consecutive configurations is valid and efficient. 

Alg. 2 details the process. The algorithm takes three inputs: 1) a segment of the action sequence _an_ : _n_ ` _l_ , 2) the current AKR structure _Ta[A] n_ ´1[,][and][3)][the][current][AKR][state] _**[q]**[a] n_ ´1[.] Parameters include _Nc_ , the number of candidate configurations sampled per action; _Nk_ , the number of clusters for downsampling; and _l_ , the horizon length for anticipated actions. 

**Algorithm 3:** SampleValidConfigurations 

||**Input**<br>**:** An AKR: _T A_<br>_ai_<br>**Ouput :** The Set of Valid Confgurations: _Qai_<br>**Params:** Max. Cardinality of _Qai_: |_Qai_|_max_||
|---|---|---|
|**1** <br>**2** <br>**3 **<br>**4**<br>**5**<br>**6**|Max. Tries of IK Calculation: MAX<br>TRIES<br> _Qai_ Ð H<br> _counts_Ð0<br> **while** |_Qai_| ă |_Qai_|_max or counts_ă_MAX_<br>_TRIES_ **do**<br>**_q_**_ai_ Ð_computeIK_p_T A_<br>_ai_ q //w.r.t. Eq. (9)<br>**if** **_q_**_ai satisfy Eqs._ (10) _to_ (13) **then**<br>_Qai_ Ð_Qai_ Y t**_q_**_ai_u||
|**7**|_counts_++||



The subsequent paragraphs detail phases of the workflow. 

**A-Space construction (line 6):** For each action _ai_ in the sequence _an_ : _n_ ` _l_ , the algorithm first updates the AKR structure _Ta[A] i_[by][integrating][the][kinematics][of][the][manipulated][object] ( _e.g_ ., a door or chair) into the robot’s kinematics, as detailed in Sec. III-B. This constructs the A-Space, which encodes the combined configuration space of the robot and object. 

**Configuration sampling (line 8):** We define _Qai_ Ă _Qai_ as the finite set of sampled configurations for AKR _Ta[A] i_ ´1[,] where each _**q** ai_ P _Qai_ satisfies task-specific goal constraints and collision-free conditions. To fully explore possible goal configurations, we formulate an optimization problem: 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0008-12.png)



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0008-13.png)


where Eq. (9) penalizes the violation of the environment and the goal constraint corresponding to Eqs. (2) and (3), Eqs. (10) and (11) bound the objective with a small tolerance to reduce undesirable results, Eq. (12) constrains the _**q** ai_ to be within the joint limit of the AKR, including both the robot and the manipulated object, Eq. (13) ensures _**q** ai_ is collisionfree in the environment. Alg. 3 details how to solve the problem to generate a finite _Qai_ for _ai_ . We first randomly sample goal AKR configurations based on the constructed AKR _Ta[A] i_[from a uniform distribution to initialize] _[ computeIK]_ and compute the inverse kinematics problem ( _i.e_ ., Eq. (9)) numerically on _Ta[A] i_[.][Solutions][satisfying][Eqs.][(10)][to][(12)] are added to _Qai_ until reaching its maximum cardinality. Then, we prune out configurations that are in collisions ( _i.e_ ., violating Eq. (13)). Note that the collision check is reserved until the last step because collisions frequently happen in a confined and cluttered environment, and checking collisions is computationally heavy. 

**Configuration down-sampling (line 10):** Even after discarding configurations that are in collision, the candidate set _Qai_ often remains large. This can make motion feasibility checking computationally expensive due to the combinatorial nature of validating transitions across a sequence of actions—requiring up to | _Qan_ | ˆ | _Qan_ `1| ˆ _. . ._ ˆ | _Qan_ ` _l_ | checks. While retaining all candidates helps preserve completeness, in practice, down-sampling the configuration set 

9 

can significantly improve planning efficiency by reducing the number of costly, repetitive feasibility checks. Thus, we downsample configurations based on the assumption that those located close to each other in configuration space ( _i.e_ ., with similar joint values and small Euclidean distances) exhibit similar motion feasibility. This is justified by the nature of our AKR-based trajectory optimization: Eq. (3) constrains only a subset of the AKR state variables via _f_ task. As a result, nearby configurations often converge to the same local minima during trajectory optimization, making it redundant to plan from each configuration individually. 

To down-sample _Qai_ and avoid redundant computations for similar configurations, we use the k-means++ method [56] to partition _Qai_ into _Nk_ clusters by minimizing the variance within the cluster: _Qai_ “ t _Q_[1] _ai[, . . . , Q] a[k] i_[u][ with the correspond-] ing cluster centroid _Q_[¯] _[k] ai_[.][Then][we][construct][a][downsampled] set _Q_[1] _ai_[“][t] _**[q]**_[1] _a_[1] _i[,]_ _**[q]** a_[1][2] _i[, . . . ,]_ _**[q]** a_[1] _[k] i_[u][by][selecting] _**[q]**_[1] _a[k] i_[that][is][closest] to the centroid in each cluster as the key configuration for the whole action sequence. Note that the cluster centroid itself may not be a valid configuration. We acknowledge that the down-sampling step introduces some incompleteness. However, we wish to clarify that downsampling is primarily a practical strategy to improve efficiency, as further experiments in Sec. VI-D demonstrate. While the current implementation focuses on empirical performance, we believe that completeness can be achieved through a more sophisticated and structured sampling strategy, as suggested by previous work [47, 49, 55]. 

**Feasibility Checking (line 12-17):** As the above procedure produces a much more compact _Q_[1] _an_ : _n_ ` _l_[,][checking the][motion] feasibility among its elements becomes feasible. Specifically, _checkMotionFeasibility_ estimates the motion feasibility for x _**q** ai,_ _**q** ai_ `1y by applying the _A_[‹] algorithm (the map and base path are reused for trajectory initialization to reduce computational effort) to find a path between the mobile base poses encoded in key configurations. We will record the key configuration in _K_ if there is a feasible base path. In the example shown in Fig. 3(c), the key configuration in red is removed because no viable path connects it to the upcoming action of grasping the door handle or passing through the door. 

**Optimal KCS Selection (line 19):** The procedure iterates until all actions within horizon _l_ are checked, resulting in the construction of _K_ , which consists of feasible KCS. Subsequently, we employ an objective function to penalize the total traveling distance and select the best KCS _**q**_[˚] _an_ : _n_ ` _l_[with] minimal cost: 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0009-05.png)


where _**W** R_ and _**W** B_ represent weight matrices, and the cost function exclusively penalizes the traveling distance for both the mobile base and the manipulator joints between two configurations. 

## VI. SIMULATION 

This section presents the results from extensive simulations that evaluate the proposed SMMP framework. The simulations 

demonstrate the effectiveness of generating coordinated basearm-object motion in the proposed A-Space, quantitatively compared to several baselines. Additionally, an object rearrangement task highlights the advantages of the AKR-based planning domain design in simplifying the task planning by reducing unnecessary action predicates of separately moving the mobile base and the arm. An ablation study on a complex, 18-step long-horizon SMMP task further examines the plan refinement algorithm. 

## _A. Simulation Setup_ 

The simulated mobile manipulator platform comprises a Clearpath Husky mobile base and a Universal Robot UR5e robotic manipulator equipped with a Robotiq 2-finger gripper positioned at the mobile base’s rotation center. The mobile base is assumed to be omnidirectional during trajectory optimization. As the four wheels can be controlled independently, its trajectory is then processed by adjusting the orientation of the mobile base to match the direction of movement, and the shoulder joint of the manipulator is adjusted accordingly to ensure the correctness of the trajectory. 

## _B. Comparisons with Baselines_ 

We developed two mobile manipulation scenarios to evaluate the benefits of SMMP as compared to approaches that treat the base and arm separately. The first task, depicted in Fig. 4(a), is to approach a door and open it by pushing. The door has a single revolute joint and is located at the end of a corridor. The second task, illustrated in Fig. 4(b), involves reaching a drawer in a confined kitchen space and opening it by pulling its prismatic joint. The initial position of the robot is randomly selected from within the shaded purple region. 

In addition to our SMMP framework, referred to as SMMP+TO ( _i.e_ ., trajectory optimization), we introduce three alternative setups to solve the above two mobile manipulation tasks for comparing the performance. To compare with a sampling-based constrained motion planner, we adopt the well-known RRT-Connect method [57] from the Open Motion Planning Library (OMPL) [58, 59] to solve the constrained motion planning problems formulated by SMMP, referred to as SMMP+RC. To compare the SMMP-based approaches with typical non-SMMP approaches, we introduce two additional baselines that independently compute trajectories for the mobile base and manipulator. Baseline 1 (BL1) utilizes A[‹] to search for a feasible mobile base path and subsequently smooth through trajectory optimization. The arm pose is then determined by solving the inverse kinematics from the door handle to the mobile base at each way-point. Building upon BL1, Baseline 2 (BL2) further optimizes the poses of the manipulator and manipulated object at each way-point for collision avoidance. 

Notably, our SMMP-based approaches (SMMP+TO and SMMP+RC) only needs to specify one task goal: the desired door angle or the desired drawer length to open. In contrast, non-SMMP approaches (BL1 and BL2) require specification of the pose of the mobile base when reaching the doorknob as well as after having opened the door, as the base and the 

10 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0010-01.png)


**----- Start of picture text -----**<br>
�����������������<br>����������������<br>�������������������<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0010-02.png)



![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0010-03.png)


**----- Start of picture text -----**<br>
(a) Door opening task (b) Drawer opening task<br>(c) Door opening task successful trail (d) Drawer opening task successful trail<br>������������ �������������� ������� ������������ �������������� �������<br>��������� ���������<br>���������� ����������<br>��� ��� ����������� ��� ��� �����������<br>(e) Door opening task failure cases (f) Drawer opening task failure cases<br>��������<br>��������<br>���<br>���<br>� �� ��� � � �� �� � �� �� �� �� � �� ��� ��� ��� ���<br>��������<br>��������<br>���<br>���<br>� �� ��� � � �� �� � �� �� �� �� ����� ��� ��� ���<br>���������������� �������������� ��������������� �������������������<br>(g) Experiment results. Upper: door opening task; lower: drawer opening task.<br>**----- End of picture text -----**<br>


Fig. 4: **Quantitative comparisons between the SMMP and three baselines in door manipulation and drawer manipulation tasks.** The robot starts from a randomized location within the purple region and (a) opens the door to a specific angle or (b) pulls out the drawer by a specific length. The orange and blue regions indicate the feasible poses that must be given to the mobile base for baselines. The regions are empirically found to guarantee a valid IK solution for the robot. (c) and (d) are successful trials of two tasks, respectively, and (e) and (f) are typical failure cases of baseline methods and the proposed SMMP method. (g) The planning success rate and the box plots with kernel density plots of the base effort, arm effort, and planning time of the four methods in these two tasks. 

manipulator are planned individually. We compute the mobile base’s intermediate poses by sampling from feasible regions that are empirically determined ( _i.e_ ., for mobile base poses in this region, the existence of an arm pose to grasp the handle is guaranteed); see the orange areas in Fig. 4(a)(b) for reaching, and the blue areas for final poses. 

We evaluate the planning results using four criteria: (i) _success rate_ as the percentage of task completion without 

violating constraints, (ii) the _base’s effort_ as the total base travel distance, (iii) the _arm’s effort_ as the sum of each joint’s cumulative angular displacement throughout task execution, and (iv) the _planning time_ . The results are summarized in Fig. 4(g). Planning the base, arm, and manipulated object separately (BL1) results in a success rate of 1% for opening doors and 36% for opening drawers. The primary cause of the failures in BL1 is collisions between the mobile manipulator 

11 

and the door or drawer, as shown in Fig. 4(e)(f). Although implementing robot-object collision checks to refine motions (BL2) enhances the success rate to 51%, the proposed SMMPbased approaches still outperform the non-SMMP approaches. Failure cases of BL2 primarily arise from kinematic constraint violations, such as the end-effector disengaging from the handle, due to the absence of feasible IK solutions caused by the bulky mobile base. This highlights the necessity of simultaneous coordination of the base, arm, and object, as illustrated in the BL2 failures shown in Fig. 4(e)(f). 

The SMMP+TO and SMMP+RC both generate feasible trajectories for the given task, with SMMP+TO achieving higher success rates than SMMP+RC. SMMP+TO produces more efficient trajectories in terms of shorter base and arm travel distances. Typically, sampling-based motion planners struggle to incorporate kinematic and safety constraints, necessitating extra effort to accommodate additional kinematic constraints [59]. Fig. 4(e)(f) also demonstrate failure cases of violating kinematic constraints. The typical failure mode of SMMP+RC is that the planner fails to find a feasible solution within the allowable time budget (300 seconds). 

Our comparative experiments suggest that SMMP-based approaches are better suited for complex mobile manipulation tasks by jointly optimizes base–arm–object movements. Moreover, trajectory optimization proves more effective for solving SMMP-based motion planning problems due to the intricate constraints involved. However, this comes at the cost of increased planning time compared to non-SMMP baselines, as AKR introduces a higher DoF compared to robot kinematics. 

## _C. Analysis on Efficiency Improvement in Task Planning_ 

By treating the robot base, arm, and object to be manipulated as a whole, the design of the task planning domain based on the A-Space perspective can offer greater efficiency. We use an object-arrangement task as an example to quantitatively evaluate the improvement offered by the A-Space perspective, where the robot rearranges _m_ objects on _m_ ` 1 tables in a sorted order while satisfying the constraint that each table can support only one object. Fig. 5(a) shows a typical example of the initial and goal configuration of this task with _m_ “ 8 objects. Our PDDL implementation, built on top of AKR (see Appendix C for details), uses fewer predicates and supports more abstract action representations compared to domain definitions that decouple base and arm movements ( _e.g_ ., [48, 55]). Specifically, such separated base-arm domains typically require: (i) additional predicates to represent the mobile base’s state, resulting in more state predicates; (ii) an extra action explicitly dedicated to base movement; and (iii) more action parameters for manipulation planning. 

To produce a task plan, we adopt the PDDL solver from [60] which employs a hybrid strategy combining a Serialized Iterative Width (SIW) search-based planner and a Best First Search-based planner, BFS(f) [61]. We use PDDL version 2.2 throughout all task planning formulations presented in this paper. In this study, we ran 50 trials for each setup; see the results summarized in Fig. 5(b). As task complexity grows, the planning time and the number of nodes generated during the 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0011-07.png)


**----- Start of picture text -----**<br>
� � � � � � � �<br>�����<br>������<br>� � � � � � � �<br>�����<br>(a) Experimental setup<br>�<br>����<br>��������<br>�<br>�<br>�� [�]<br>�� [�]<br>�� [�]<br>�� [�]<br>�� [�] � � � � �� �� �� ��<br>�����������������<br>(b) Performance comparison<br>��������������������������<br>������������������������<br>**----- End of picture text -----**<br>


Fig. 5: **AKR-based domain specification improves the task planning efficacy.** (a) An example setup of rearranging 8 objects on 9 tables; one table can only support one object. (b) The AKR-based domain specification allows a solver to search for a feasible plan for tasks involving re-arranging 2 to 16 objects in significantly less time while generating fewer nodes in search ( _i.e_ ., less memory). 

search ( _i.e_ ., memory usage) increase much more slowly using the AKR-based approach, as compared to separated base-arm domains, which exhibit an exponential rise. This is because non-AKR-based task planning requires more action operators to accomplish each task, resulting in greater search depths. If there are, on average, _N_ nodes generated at each search depth level, and a solution is found at depth _D_ , the total nodes generated is _N[D]_ . The AKR-based approach requires fewer action operators, resulting in shallower search depths and substantially reducing both the number of expanded nodes and the frequency of backtracking during task planning. In a task involving rearranging 16 objects across 50 trials, we observed an average of 76% reduction in search depth with the AKR-based task planner, leading to a significant enhancement in planning efficiency alongside a reduction in memory usage. 

Taken together, the results of this study demonstrate that task planning based on AKR significantly reduces the need for wide and deep exploration in the search process. This improvement not only improves the efficiency and reduces memory usage of task planning, but also holds promise for reducing the number of motion planning calls required in broader TAMP frameworks. 

12 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0012-01.png)


Fig. 6: **Ablation studies of plan refinement in SMMP with a simulated household environment.** (a) The robot is tasked to place a drink on the desk in the bedroom and dispose of an object in the trash can. (b) The entire task consists of 18 actions, all represented by the two symbolic actions. The proposed AKR against a baseline method and different settings of plan refinement. (c) Two possible robot start configurations that influence the feasibility of subsequent actions. 

## _D. Ablation Studies of Plan Refinement in SMMP_ 

We conducted further ablation studies to evaluate how the plan refinement algorithm impacts the execution success rate in long-horizon tasks through simulation. In Fig. 6(a), the robot is assigned the task of bringing a drink from the fridge to the bedroom desk (Goal 1) and fetching trash located between the sofa and the coffee table before depositing it into the trash can (Goal 2). Notably, the robot has to temporarily place the drink on the dining table to free its gripper before opening the bedroom door ( _a_ 4 - _a_ 9 ), and must also use the broom to collect the trash because the space within which it is located is smaller than the robot’s base ( _a_ 13 - _a_ 17 ). This poses significant challenges to the reliability of the generated 18-step task and motion plan. Please refer to Appendix C for details on the task planning domain designed for this problem. 

In the study, we recorded the robot’s cumulative planning success rate at each step in the sequential mobile manipulation over the 18 steps across 5 settings: 

- ‚ Non-SMMP: The execution trajectories are generated using Baseline 2 (BL2) as described in Sec. VI-B, which plans the robot’s base and arm separately without incorporating the proposed AKR. 

- ‚ _l_ =0, w/o DS: The end configuration for the robot’s next action is randomly sampled, without employing plan refinement (as _l_ =0) and down-sampling. 

- ‚ _l_ =2, w/o DS: The end configuration for the robot’s next action is determined using the plan refinement algorithm _without down-sampling_ . A total of 3 subsequent actions (including the current one) are considered. 

- ‚ _l_ =2, w/ DS: The end configuration is determined using the proposed plan refinement algorithm with _down-sampling_ 

_enabled_ . The same 3 subsequent actions (including the current one) are considered to allow direct comparison with the previous setup. 

- ‚ _l_ =4, w/ DS: A total of 5 subsequent actions (including the incoming action) are considered, with the other settings remaining the same as in the previous setting. 

In each trial, the mobile manipulator is randomly positioned within the purple-dotted region depicted in Fig. 6(a); a total of 100 trials are conducted to obtain the cumulative success rate. To ensure a fair comparison, in addition to the initial and goal states of the environment, both the SMMP and non-SMMP methods received identical manually defined grasping poses for all movable objects, though not the corresponding robot configurations. 

In Fig. 6(b), the cumulative success rates for each set, as the task progresses, underscore the importance of considering future actions in long-horizon tasks. Without planning in the A-Space, the motion planner faces particular challenges at ( _a_ 2 ), when opening the fridge door in a confined space. When no plan refinement algorithm is applied ( _i.e_ ., _l_ “ 0, w/o DS), the success rate significantly drops at _a_ 3 because the opened fridge door and the kitchen table obstruct the robot’s path to picking up the drink, as illustrated in Fig. 6(c). Without considering future actions, the robot could easily trap itself during execution in a crowded scene ( _i.e_ ., select a poor end configuration as in _a_ 2 ). By anticipating the actions of picking up the drink and placing it in _a_ 3 and _a_ 4 ( _i.e_ ., _l_ “ 2, w/o DS), the robot avoids getting trapped by choosing the green end configuration instead of the red one, as in Fig. 6(c), despite this trajectory being less efficient and harder to compute at the current step, as indicated by a slight drop in motion planning success rate. 

13 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0013-01.png)


Fig. 7: **The system diagram for the mobile manipulator platform.** (a) The mobile manipulator’s hardware configuration and communication diagram. (b) The control diagram of the mobile manipulator platform. 

Furthermore, finding end configurations for each action using the down-sampling method improves the success rate by excluding robot configurations sharing similar geometric properties ( _l_ “ 2, w/ DS _v.s_ . _l_ “ 2, w/o DS), so it is more likely to find a feasible goal within the computational budget (max 5 retries are allowed for each action). Looking ahead to longer horizon tasks ( _i.e_ ., _l_ “ 4, w/ DS), one could further improve the success rate, albeit at the cost of increased computational effort. In summary, the plan refinement algorithm significantly improves the motion planning success rate by selecting action goals at each step that take into account the feasibility of future actions, making this method better suited to long-horizon tasks. 

## VII. EXPERIMENTS 

This section presents the real-world robot experiments that show that the framework can generate coordinated wholebody motions for mobile manipulation across various scenarios, solve challenging long-horizon tasks, and generalize to different robot platforms and tool-use tasks analogous to the body schema theorem. 

## _A. Robot Platform_ 

In this article, we evaluated the proposed SMMP method on three robot platforms with different structures. 

**The mobile manipulator platform** consists of dual Universal Robot UR5e robotic manipulators equipped with Robotiq 3-finger grippers installed on a Clearpath Ridgeback omnidirectional mobile platform. The on-board computational hardware is a mini PC with Intel Core i7-10700 CPU. Task and motion generation are performed on a host PC equipped with an AMD Ryzen9 5950X CPU. For perception, we utilize the Motion Capture System (MCS), operating at 500 _Hz_ , to track object poses and the mobile base’s position and orientation. MCS data is processed on its host PC and transmitted to the onboard mini PC via a local network. It is worth noting that a single UR5e manipulator serves all tasks in our setup. 

Our on-board control processes involve several steps. Firstly, the MCS tracks the mobile base’s 3D pose and 

objects’ 6D poses in the physical environment, which are then transmitted to the host PC along with the manipulator configuration (UR5e joint values in this case) to update the AKR state. Next, the proposed SMMP framework updates the AKR structure according to the previous action and then generates the trajectory based on the current action goals and A-Space. Subsequently, the host PC sends the planned trajectory to the mini PC for time parameterization, adhering to hardware constraints. The time-parameterized reference trajectory is then sent to the corresponding base and arm controllers concurrently. For manipulator control, we utilize the built-in trajectory follower of the UR5e. For the mobile base control, we develop a custom PID-based velocity tracking controller to generate velocity control signals for trajectory tracking. Fig. 7 is a schematic diagram of the platform. 

**The aerial manipulator platform** setup is similar to the mobile manipulator platform, the major difference being the flying vehicle control system. The high-level controller communicates with the MCS through Ethernet for feedback and outputs the desired attitude and thrust of each thrust generator [62]. These commands are transmitted through Crazy Radio PA antennas (2.4 GHz) to the Crazyflie 2.1 control boards, where double-loop PID controllers are implemented for 500 _Hz_ low-level control with onboard IMU feedback. Appendix B provides more details of the system. 

## _B. Coordinated Whole-body Trajectory Generation_ 

In a real household environment featuring diverse everyday objects with distinct articulation, we showcase the robot’s adept execution of various mobile manipulation tasks through coordinated whole-body motions generated by the proposed method. Snapshots in Fig. 8 depict the robot performing four typical household tasks: (a) unfolding a flip-top table with a horizontal revolute axis, (b) rolling a chair that can move around on the floor plane ( _i.e_ ., 2D displacement), (c) opening a microwave and (d) opening a closet, both involving a vertical revolute axis, with the bulky closet door requiring more sophisticated motion coordination. By formulating motion planning problems in A-Space one naturally accommodates both robot and object movements, resulting in successful and 

14 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0014-01.png)


Fig. 8: **Robot performance in mobile manipulation with articulated objects.** The robot generates coordinated base-arm-object motions for (a) unfolding the table, (b) placing the chair, (c) opening the microwave, and (d) opening the closet. The robot consistently maintains coordination in manipulations, even in the face of more challenging situated constraints due to the obstacles shaded in red. (e) The translational and rotational traveling distance. 

efficient task execution. This advantage is particularly evident in Fig. 8(e), in which each manipulation task is rendered increasingly complex by the presence of new obstacles (highlighted in red), and more sophisticated obstacle avoidance strategies, therefore, become necessary. Notably, for this kind of task, motion planning using in A-Space shares the same objectives and goal states, differing only in the constraint that specifies obstacle configurations in the surrounding space (see Sec. IV-A for details). 

We further evaluated the motion planner’s performance in terms of the efficiency of the trajectories it computes. By repeating the planning for each scenario in Fig. 8(a)-(d) five times (with random start locations) and executing the planned trajectories on physical robots, we reported statistics on base efforts and arm joint efforts measured by trajectory lengths in Fig. 8(e), to assess execution efficiency. In general, surrounding obstacles could constrain navigation, compelling the robot to compensate by increasing arm movements, and leading to notably higher joint effort when manipulating the 

chair, microwave, and closet. 

## _C. Sequential Mobile Manipulation Planning_ 

Fig. 9(a) showcases a series of the robot in a conducting complex, long-horizon sequential mobile manipulation task. The task objectives assigned to the robot are: (Goal 1) retrieving a new tissue box from a closet drawer, placing it on the tea table, and (Goal 2) disposing of the empty tissue box in the trash can. As this task involves interactions with various structures, such as the closet with a revolute joint, the drawer with a prismatic joint, and other rigid objects while navigating through confined 3D spaces, the entire task execution consists of 14 distinct actions. Our method successfully addresses this SMMP challenge, demonstrating progress at three levels. 

At the task level, the difficulties in specifying the planning domain and the computational cost in solving the task are reduced, since only two action operators are required. These improvements are quantitatively evaluated in a simplified setup (Sec. VI-C). Throughout execution, the task planner correctly 

15 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0015-01.png)


Fig. 9: **Performance of the robot in a sequential mobile manipulation task requiring multiple types of action.** (a) The robot is tasked to dispose of the empty tissue box and replace it with a new one. The task goals and environment states are defined using the PDDL. (b) The robot can solve the 14-step task using only two action operators based on the AKR-based task planner. The feasible trajectories over this long-horizon task are produced accordingly, with plan refinement based on the sequence of the actions. 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0015-03.png)


Fig. 10: **Tracking performance in a real-world SMMP task.** The figure shows the reference trajectory generated from the proposed SMMP method, alongside the actual mobile manipulator’s trajectory obtained from MCS and robot joint feedback, and the tracking error. The duration of each pick-akr action is highlighted with a darker background. 

determines the sequence of actions, such as opening the closet before accessing the drawer, and vice versa when closing them. This suggests that our task planning setup faithfully describes the scene and the associated state transitions. 

from symbolic actions are effectively solved, resulting in well-coordinated movements of the robot’s base, arm, and manipulated object during mobile manipulation (see tracking performance in Fig. 10). These whole-body motions enable 

At the motion level, motion planning problems instantiated 

16 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0016-01.png)


Fig. 11: **Applications of the AKR for different robots and robotic tool-use tasks.** (a) Planning sequential aerial manipulation tasks for an over-actuated Unmanned Aerial Manipulator (UAM). By abstracting the over-actuated UAV’s flight as a 6-DoF floating mobile base and combining the kinematics of the 3-DoF manipulator, the proposed SMMP framework is applied to solve the task of placing an object into the drawer. (b) The AKR allows the robot to utilize manipulated objects as tools to fetch the litter with a broom and (c) to close the unreachable closet door with a stick. 

the robot to perform interactive tasks within confined spaces. 

At the goal level, selecting a robot configuration that aligns with the motion planner’s goal at the end of each action is crucial for the overall success of the task. For instance, in action _**a**_ 2 : place-akr(closet), the robot could attempt to open the closet door from either the left or right side. Our plan refinement algorithm successfully accounts for the subsequent action of pulling out the drawer ( _**a**_ 3) and therefore selects a robot configuration such that the door is opened from the left, thus avoiding potential obstructions from the nearby carpet and the closet door that would have just been opened. 

These three advancements collectively enable a robot to conduct SMMP tasks proficiently. Fig. 10 illustrates the tracking performance of the mobile manipulator. The results demonstrate that the proposed SMMP method can generate executable trajectories that are trackable by the physical robot. 

## _D. Versatility of the Proposed SMMP Framework_ 

The advantages of formulating SMMP from the A-Space perspective extend beyond specific robots or tasks. Since kinematic relationships can characterize various patterns of a robot’s movements and a wide range of task goals, our SMMP framework can be extended to other non-traditional setups in mobile manipulation. As illustrated in Fig. 11(a), by applying SMMP to an over-actuated UAM, which consists of an over-actuated Unmanned Aerial Vehicle (UAV) and a 3-DoF manipulator, we open up new horizons in sequential multi-step aerial manipulation. Unlike fundamentally stable ground robots, aerial robots have to prioritize their own safety - an increasingly challenging task when interacting with the surrounding environment. We, therefore, implemented a hierarchical control framework for the aerial manipulator to stabilize itself and track desired trajectories [62, 63]. 

Planning in the A-Space also allows a robot to incorporate external objects as body extensions for non-prehensile manipulation or tool uses. Fig. 11(b)(c) illustrate two robotic tool-use tasks modeled and computed by SMMP. In the first task, the robot utilizes a broom to sweep away litter located between the tea table and the sofa, which the robot cannot approach 

directly. In the second task, the robot plans to use a stick to close the closet’s upper door which is unreachable by its manipulator. These results demonstrate that our framework is not limited to a specific setting; it can be applied to different robot embodiments and has the potential to significantly expand a robot’s capabilities by incorporating grasped objects as tools, a crucial step forward in open-world, task-rich environments. 

## VIII. DISCUSSION AND CONCLUSION 

## _A. Key Findings_ 

**Coordinated Robot-scene Motion in Human Environments:** Through a series of single-step and multi-step mobile manipulation tasks in Sec. VI-D and Sec. VII-C, we demonstrated the effectiveness of the proposed SMMP framework in generating coordinated robot-scene motions in long-horizon tasks. This type of motion coordination in various settings is crucial for robots operating in human environments that have been primarily designed with bipedal locomotion. Indoor scenes are typically organized to meet human activities, but can be too confined and cluttered for mobile manipulators to navigate and interact with [64]. Although prior work has improved the robustness and efficiency of planning algorithms in confined and cluttered environments [29, 65, 66], the absence of coordinated whole-body motion still fundamentally limits robotic capabilities in many tasks (see supplementary video for examples). After integrating the manipulated object’s kinematics with that of the robot, planning in the A- Space can facilitate a general and efficient formulation for robots needing to manipulate a variety of objects with wholebody motions, irrespective of the robot’s own morphology. This is evidenced by our experimental results in Fig. 8 and Fig. 11, where the proposed approach successfully generates coordinated base-arm-object trajectories across a variety of scenarios involving a ground mobile manipulator and an aerial manipulator. The robots effectively handle interactions with a range of articulated furniture, like doors and drawers, and achieve significantly higher success rates compared to nonSMMP methods, as quantified in Sec. VI-B. 

17 

**Integrated Representation for Sequential Tasks:** Success in solving SMMP tasks relies heavily on the fluent execution of each single-step action. One notable advantage of framing motion planning problems based on the integrated robot-scene representation, AKR, is the clarity of directly defined goal configurations ( _i.e_ ., the action parameters) at each step in terms of object states, eliminating the need to specify robot states as part of the goal. For instance, in the task of opening a microwave in Fig. 8(c), the goal is to set the microwave door to a particular angle. The robot’s pose and mobile base location are less critical, as they are optimized to adhere to the situational constraints ( _i.e_ ., the human’s location) during motion planning, which have been incorporated into the A-Space. Consequently, in Fig. 8(e), when the level of confinement for the same task increases due to obstacles, the AKR-based planner readily adapts base-arm coordination and produces different trajectories to achieve the same task goal. In contrast, planning methods that treated robot base and arm movements separately require separate goal specifications and action predicates for each component; see Fig. 5. While this approach may be computationally efficient in motion planning, it presents challenges in coordinating movements, especially when dealing with environmental constraints imposed by external objects. As shown in Fig. 4(g), baselines that separate base and arm planning suffer a significant drop in task success rates due to the lack of coordination between their respective end configurations. This misalignment becomes particularly problematic in complex SMMP setups, where the iterative nature of TAMP causes failed motion planning attempts to trigger frequent backtracking and replanning, ultimately leading to failures. 

## _B. Limitations and Future Directions_ 

**Efficient Planning for Responsive Operation:** As reported in Sec. VI-B, A-Space planning times, produced via trajectory optimization, are notably faster than sampling-based methods but still exceed those of baselines due to the incorporation of additional DoFs. While the proposed SMMP framework can generate flexible and coordinated trajectories within confined spaces, it may be less suitable for applications that require responsive operation. A recent study by Sundaralingam _et al_ . introduces a potential solution by parallelizing trajectory optimization computations on GPUs [67]. Their approach demonstrates promising results, speeding up times by a factor of 60. By integrating this GPU-accelerated motion generation library with our SMMP framework, we achieve high-DoF dexterity and responsive operation [68]. Furthermore, our approach demonstrates its applicability across a series of realistic scenes adapted from iThor [69] (see Appendix C for details), reinforcing its potential for real-world deployment. 

**Obtaining Scene Kinematics:** We also acknowledge that the success of the proposed SMMP framework relies heavily on precise knowledge of scene kinematics, which may not always be available in unstructured environments. Recent advancements in computer vision have enabled the reconstruction and inference of part-level relations among objects with articulation [70–72], offering the potential to acquire object 

kinematics from vision alone [24, 73]. Still, the precision required for manipulation exceeds the current state-of-the-art in computer vision techniques. Integrating tactile feedback at the robot’s end-effectors ( _e.g_ ., vision-based tactile sensors) and employing advanced adaptive controllers could enhance robot execution in scenarios with uncertain object kinematics due to perception noise. Moreover, by leveraging readily available environment datasets with known kinematics such as [69], the proposed SMMP framework can serve as an effective data generation platform, addressing the persistent challenge of high-quality data collection in learning-based manipulation research [4]. 

**Interacting with Scenes:** Perceiving human-made scenes and the objects within them naturally guides the actions of agents [74, 75], forming the foundations for accomplishing complex tasks. However, existing approaches typically focus on capturing 2D or 3D occupancy information for obstacle avoidance during navigation or pick-and-place manipulation. To tackle longer-horizon tasks, it is crucial to incorporate _actionable_ information, such as the actions that entities in the scene can perform and the physical constraints they impose, into robot planning [14, 24]. Identifying what information can be considered actionable and beneficial for subsequent manipulation tasks is a fundamental challenge addressed in this article. Our investigation into SMMP suggests that kinematics could serve as a key bridging stone between perception-based scene understanding and control-based manipulative robot actions. 

## _C. Conclusion_ 

In this article, we introduced the concept of the Augmented Kinematic Representation (AKR), which integrates scene kinematics into the robot’s own model to construct a unified Augmented Configuration Space (A-Space) for solving sequential mobile manipulation tasks. We developed a trilevel planning framework that combines PDDL-based task planning, trajectory optimization, and plan refinement, and validated it extensively through both simulation and realworld experiments. Our results demonstrate the framework’s effectiveness in generating coordinated whole-body motions, even in confined spaces with articulated objects, and its ability to execute complex tasks involving up to 14 sequential actions without interruption. As kinematics offers a general representation of constrained motion beyond robotic morphology alone, the proposed AKR and A-Space framework holds strong promise for broad application across diverse robot platforms and challenging manipulation scenarios. 

## APPENDIX 

## _A. Trajectory Initialization_ 

We implement two trajectory initialization baselines [76]: 

- 1) **Stationary:** The trajectory _**q**_ 1: _T_ is initialized by way-points _**q** t_ that are the same as the initial pose _**q**_ 1. 

- 2) **Interpolated:** The trajectory _**q**_ 1: _T_ is initialized by waypoints that are linearly interpolated between the initial pose _**q**_ 1 and the goal pose _**q** T_ . 

18 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0018-01.png)


**----- Start of picture text -----**<br>
(a) (b) (c) (d) ���<br>����������<br>������������<br>�� ���������<br>��<br>��<br>���������� ���������� ���������� � ���������� ���������� ����������<br>����������������<br>**----- End of picture text -----**<br>


Fig. 12: **Comparisons of motion planning on AKRs by different trajectory initialization methods.** (a)-(c) The experimental scenarios in increasing complexity. The robot’s initial pose is uniformly sampled within the blue region; it is tasked to pick up the stick and use it to reach the red cube. (d) The proposed A[‹] -based trajectory initialization has the highest success rates (almost always) in generating a feasible plan. In comparison, the _Stationary_ method fails to generate feasible plans in Scenarios 2 and 3. Similarly, the _Interpolated_ method struggles in Scenario 3 (30% success rate). 


![](1_survey/papers/md/Jiao2025Integration_figs/Jiao2025Integration.pdf-0018-03.png)


**----- Start of picture text -----**<br>
(a) (b) �������������� ��������� (c) ������������������ ������������������ (d) ��������������<br>������ ���������� �������������<br>������� �������������<br>����� ����� ���������������������� ����������<br>������������<br>�������������������� ������ �� ���� ��������������<br>������������������� ���������������<br>�������������<br>�������������� ������������ ������� ������������������<br>���������� ���������������������� ���������������� �����<br>��������������������<br>������� ������������� ����������� ������������������� ������������������ ������������������ ����������������<br>�������������� ������� ����<br>���������������� ����� �� ������������������������������ ������������������������������������ ����������������������������������������������������� ��������������������������������<br>����������������� ��������������������� ��������������������� ������������������������������������������������������� �����������������������������<br>**----- End of picture text -----**<br>


Fig. 13: **The system diagram for the aerial manipulator platform.** (a) The aerial manipulator’s communication diagram. (b) The control diagram of the platform. (c) The design of the aerial manipulator platform, and (d) the omnidirectional thrust generator. 

Next, we investigate how different trajectory initialization methods affect the planning results in three scenarios; see Fig. 12(a)-(c). The robot’s task is to pick up the rigid stick and use it to reach a target indicated by the red cube. This task consists of two steps: i) navigate to the stick and pick it up, ii) navigate to and reach the target with the stick. The three scenarios designed for evaluation are increasing in complexity: no obstacle (Fig. 12(a)), two small obstacles (Fig. 12(b)), or a much larger one (Fig. 12(c)). Experimental results reported below are the average of 50 different initial poses, each with 10 times. 

A successfully optimized trajectory is a converged result without violating any constraints ( _e.g_ ., collisions). Fig. 12(d) compares success rates. When the environment is clean (Scenario 1), even the simplest _Stationary_ trajectory initialization method performs well. When there is additional complexity introduced by the obstacles (Scenario 2), the _Stationary_ method deteriorates, whereas the _Interpolated_ method still maintains a high success rate. When the navigable space is significantly reduced (Scenario 3), only the proposed _A_[‹] - based initialization method can consistently perform well to generate feasible plans. Taken together, experimental results indicate that combining the proposed _A_[‹] -based initialization with the optimization-based motion planner can well handle the challenging motions that require combining navigation and manipulation in cluttered space with obstacle avoidance. 

## _B. Unmanned Aerial Manipulator Platform_ 

The Unmanned Aerial Manipulator (UAM) platform consists of an over-actuated omnidirectional flying vehicle and a 3-DoF robotic manipulator [63]. The flying vehicle integrates four omnidirectional thrust generators, each built with a generic quadcopter (Crazyflie 2.1 control board) and a 2-DoF 

passive gimbal mechanism [77], enabling independent position and attitude tracking capability. The robotic manipulator comprises three serial rotational DoFs and a parallel gripper. Four Dynamixel XC330-M228-T motors actuate the manipulator, while a Raspberry Pi Zero and a Dynamixel U2D2 converter are fitted to the flying vehicles to receive wireless control commands. Fig. 13 is a schematic diagram of the platform. 

## _C. Additional Materials_ 

The project page[1] for this article hosts supplementary materials that could not be included in the main manuscript due to space constraints. These materials include: 

**PDDL files:** Domain files for the simulation tasks described in Secs. VI-C, VI-D and VII-C, along with the corresponding problem files specifying the initial and goal states, are provided. These are released together with the off-the-shelf task planner to support reproducibility and further research. 

**Extended simulation results:** We tested our AKR-based mobile manipulation planner in realistic, cluttered household scenes adapted from iThor [69]. Each scene includes articulated objects selected from the PartNet-Mobility dataset [78], replacing existing objects of the same category to preserve contextual realism. Grasp poses were generated using AOGrasp [54]. These results are available on the project page. To handle the scale and complexity of this evaluation, we ported our AKR-based motion planning framework to the Curobo platform and developed a fully automated toolchain for environment setup. 

**Codebase:** The codebase used in our experiments, including that for the extended simulations, is released via the project page. 

1https://aug-kin-rep.github.io 

19 

## REFERENCES 

- [1] Z. Jiao, Z. Zhang, X. Jiang, D. Han, S.-C. Zhu, Y. Zhu, and H. Liu, “Consolidating kinematic models to promote coordinated mobile manipulations,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2021. 

- [2] Z. Jiao, Z. Zhang, W. Wang, D. Han, S.-C. Zhu, Y. Zhu, and H. Liu, “Efficient task planning for mobile manipulation: a virtual kinematic chain perspective,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2021. 

- [3] A. Billard and D. Kragic, “Trends and challenges in robot manipulation,” _Science_ , vol. 364, no. 6446, p. eaat8414, 2019. 

- [4] O. Kroemer, S. Niekum, and G. Konidaris, “A review of robot learning for manipulation: Challenges, representations, and algorithms,” _Journal of Machine Learning Research (JMLR)_ , vol. 22, no. 30, pp. 1–82, 2021. 

- [5] M. Diffler, F. Huber, C. Culbert, R. Ambrose, and W. Bluethmann, “Human-robot control strategies for the nasa/darpa robonaut,” in _IEEE Aerospace Conference Proceedings_ , vol. 8, pp. 3939–3947, IEEE, 2003. 

- [6] Z. Jiang, X. Cao, X. Huang, H. Li, and M. Ceccarelli, “Progress and development trend of space intelligent robot technology,” _Space: Science & Technology_ , 2022. 

- [7] T. Marcucci, M. Petersen, D. von Wrangel, and R. Tedrake, “Motion planning around obstacles with convex optimization,” _Science Robotics_ , vol. 8, no. 84, p. eadf7843, 2023. 

- [8] O. Khatib, K. Yokoi, O. Brock, K. Chang, and A. Casal, “Robots in human environments: Basic autonomous capabilities,” _International Journal of Robotics Research (IJRR)_ , vol. 18, no. 7, pp. 684–696, 1999. 

- [9] O. Brock, J. Park, and M. Toussaint, “Mobility and manipulation,” _Springer Handbook of Robotics_ , pp. 1007–1036, 2016. 

- [10] Y. Karayiannidis, C. Smith, F. E. V. Barrientos, P. Ogren, and D. Kragic,[¨] “An adaptive control approach for opening doors and drawers under uncertainties,” _Transactions on Robotics (T-RO)_ , vol. 32, no. 1, pp. 161– 175, 2016. 

- [11] R. Mart´ın-Mart´ın and O. Brock, “Coupled recursive estimation for online interactive perception of articulated objects,” _International Journal of Robotics Research (IJRR)_ , pp. 1–37, 2019. 

- [12] L. P. Kaelbling and T. Lozano-P´erez, “Hierarchical task and motion planning in the now,” in _International Conference on Robotics and Automation (ICRA)_ , 2011. 

- [13] M. Toussaint, “Logic-geometric programming: An optimization-based approach to combined task and motion planning.,” in _International Joint Conference on Artificial Intelligence (IJCAI)_ , 2015. 

- [14] Z. Jiao, Y. Niu, Z. Zhang, S.-C. Zhu, Y. Zhu, and H. Liu, “Sequential manipulation planning on scene graph,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2022. 

- [15] J.-P. Sleiman, F. Farshidian, and M. Hutter, “Versatile multicontact planning and control for legged loco-manipulation,” _Science Robotics_ , vol. 8, no. 81, p. eadg5014, 2023. 

- [16] T. Lozano-P´erez and L. P. Kaelbling, “A constraint-based method for solving sequential manipulation planning problems,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2014. 

- [17] N. T. Dantam, S. Chaudhuri, and L. E. Kavraki, “The task-motion kit: An open source, general-purpose task and motion-planning framework,” _IEEE Robotics and Automation Magazine (RA-M)_ , vol. 25, no. 3, pp. 61– 70, 2018. 

- [18] C. R. Garrett, R. Chitnis, R. Holladay, B. Kim, T. Silver, L. P. Kaelbling, and T. Lozano-P´erez, “Integrated task and motion planning,” _Annual Review of Control, Robotics, and Autonomous Systems_ , 2021. 

- [19] B. Kim, L. Shimanuki, L. P. Kaelbling, and T. Lozano-P´erez, “Representation, learning, and planning algorithms for geometric task and motion planning,” _International Journal of Robotics Research (IJRR)_ , vol. 41, no. 2, pp. 210–231, 2022. 

- [20] S. Gallagher, _How the body shapes the mind_ . Clarendon Press, 2006. 

- [21] N. P. Holmes and C. Spence, “Beyond the body schema: Visual, prosthetic, and technological contributions to bodily perception and awareness,” _Human body perception from the inside out: Advances in visual cognition_ , pp. 15–64, 2006. 

- [22] A. Clark and R. Grush, “Towards a cognitive robotics,” _Adaptive Behavior_ , vol. 7, no. 1, pp. 5–16, 1999. 

- [23] M. Wilson, “Six views of embodied cognition,” _Psychonomic bulletin & review_ , vol. 9, pp. 625–636, 2002. 

- [24] M. Han, Z. Zhang, Z. Jiao, X. Xie, Y. Zhu, S.-C. Zhu, and H. Liu, “Scene reconstruction with functional objects for robot autonomy,” _International Journal of Computer Vision (IJCV)_ , vol. 130, no. 12, pp. 2940–2961, 2022. 

- [25] S. Chitta, B. Cohen, and M. Likhachev, “Planning for autonomous door opening with a mobile manipulator,” in _International Conference on Robotics and Automation (ICRA)_ , 2010. 

- [26] A. Jain and C. C. Kemp, “Pulling open doors and drawers: Coordinating an omni-directional base and a compliant arm with equilibrium point control,” in _International Conference on Robotics and Automation (ICRA)_ , 2010. 

- [27] M. Stuede, K. Nuelle, S. Tappe, and T. Ortmaier, “Door opening and traversal with an industrial cartesian impedance controlled mobile robot,” in _International Conference on Robotics and Automation (ICRA)_ , 2019. 

- [28] M. V. Minniti, F. Farshidian, R. Grandia, and M. Hutter, “Whole-body mpc for a dynamically stable mobile manipulator,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 4, no. 4, pp. 3687–3694, 2019. 

- [29] D. Berenson, J. Kuffner, and H. Choset, “An optimization approach to planning for mobile manipulation,” in _International Conference on Robotics and Automation (ICRA)_ , 2008. 

- [30] K. Gochev, A. Safonova, and M. Likhachev, “Planning with adaptive dimensionality for mobile manipulation,” in _International Conference on Robotics and Automation (ICRA)_ , 2012. 

- [31] D. M. Bodily, T. F. Allen, and M. D. Killpack, “Motion planning for mobile robots using inverse kinematics branching,” in _International Conference on Robotics and Automation (ICRA)_ , 2017. 

- [32] J. Haviland, N. S¨underhauf, and P. Corke, “A holistic approach to reactive mobile manipulation,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 7, no. 2, pp. 3122–3129, 2022. 

- [33] C. Wang, Q. Zhang, Q. Tian, S. Li, X. Wang, D. Lane, Y. Petillot, and S. Wang, “Learning mobile manipulation through deep reinforcement learning,” _Sensors_ , vol. 20, no. 3, p. 939, 2020. 

- [34] H. Ito, K. Yamamoto, H. Mori, and T. Ogata, “Efficient multitask learning with an embodied predictive model for door opening and entry with whole-body control,” _Science Robotics_ , vol. 7, no. 65, p. eaax8177, 2022. 

- [35] F. Xia, C. Li, R. Mart´ın-Mart´ın, O. Litany, A. Toshev, and S. Savarese, “Relmogen: Integrating motion generation in reinforcement learning for mobile manipulation,” in _International Conference on Robotics and Automation (ICRA)_ , 2021. 

- [36] R. Alami, J.-P. Laumond, and T. Sim´eon, “Two manipulation planning algorithms,” in _Proceedings of the Workshop on Algorithmic Foundations of Robotics (WAFR)_ , pp. 109–125, AK Peters, Ltd. Natick, MA, USA, 1994. 

- [37] S. Cambon, R. Alami, and F. Gravot, “A hybrid approach to intricate motion, manipulation and task planning,” _International Journal of Robotics Research (IJRR)_ , vol. 28, no. 1, pp. 104–126, 2009. 

- [38] K. Hauser and V. Ng-Thow-Hing, “Randomized multi-modal motion planning for a humanoid robot manipulation task,” _International Journal of Robotics Research (IJRR)_ , vol. 30, no. 6, pp. 678–698, 2011. 

- [39] J. Barry, L. P. Kaelbling, and T. Lozano-P´erez, “A hierarchical approach to manipulation with diverse actions,” in _International Conference on Robotics and Automation (ICRA)_ , 2013. 

- [40] M. Toussaint, K. Allen, K. A. Smith, and J. B. Tenenbaum, “Differentiable physics and stable modes for tool-use and manipulation planning,” in _Robotics: Science and Systems (RSS)_ , 2018. 

- [41] D. McDermott, M. Ghallab, A. Howe, C. Knoblock, A. Ram, M. Veloso, D. Weld, and D. Wilkins, “Pddl-the planning domain definition language,” tech. rep., Yale Center for Computational Vision and Control, 1998. 

- [42] M. Helmert, “The fast downward planning system,” _Journal of Artificial Intelligence Research_ , vol. 26, pp. 191–246, 2006. 

- [43] E. Karpas and D. Magazzeni, “Automated planning for robotics,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 3, pp. 417– 439, 2020. 

- [44] E. Erdem, K. Haspalamutgil, C. Palaz, V. Patoglu, and T. Uras, “Combining high-level causal reasoning with low-level geometric reasoning and motion planning for robotic manipulation,” in _International Conference on Robotics and Automation (ICRA)_ , 2011. 

- [45] S. Srivastava, E. Fang, L. Riano, R. Chitnis, S. Russell, and P. Abbeel, “Combined task and motion planning through an extensible plannerindependent interface layer,” in _International Conference on Robotics and Automation (ICRA)_ , 2014. 

- [46] C. R. Garrett, T. Lozano-Perez, and L. P. Kaelbling, “Ffrob: Leveraging symbolic planning for efficient task and motion planning,” _International Journal of Robotics Research (IJRR)_ , vol. 37, no. 1, pp. 104–136, 2018. 

- [47] X. Zhang, Y. Zhu, Y. Ding, Y. Jiang, Y. Zhu, P. Stone, and S. Zhang, “Symbolic state space optimization for long horizon mobile manipulation planning,” in _International Conference on Intelligent Robots and Systems (IROS)_ , pp. 866–872, IEEE, 2023. 

- [48] Z. Yang, C. Garrett, D. Fox, T. Lozano-P´erez, and L. P. Kaelbling, “Guiding long-horizon task and motion planning with vision language models,” _arXiv preprint arXiv:2410.02193_ , 2024. 

20 

- [49] Y. Sung, Z. Wang, and P. Stone, “Learning to correct mistakes: Backjumping in long-horizon task and motion planning,” in _Conference on Robot Learning (CoRL)_ , pp. 2115–2124, PMLR, 2023. 

- [50] M. Stilman, “Global manipulation planning in robot joint space with task constraints,” _Transactions on Robotics (T-RO)_ , vol. 26, no. 3, pp. 576– 584, 2010. 

- [51] C. R¨osmann, F. Hoffmann, and T. Bertram, “Kinodynamic trajectory optimization and control for car-like robots,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2017. 

- [52] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, S. Patil, K. Goldberg, and P. Abbeel, “Motion planning with sequential convex optimization and convex collision checking,” _International Journal of Robotics Research (IJRR)_ , vol. 33, no. 9, pp. 1251–1270, 2014. 

- [53] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “Chomp: gradient optimization techniques for efficient motion planning,” in _International Conference on Robotics and Automation (ICRA)_ , 2009. 

- [54] C. P. Morlans, C. Chen, Y. Weng, M. Yi, Y. Huang, N. Heppert, L. Zhou, L. Guibas, and J. Bohg, “Ao-grasp: Articulated object grasp generation,” in _International Conference on Intelligent Robots and Systems (IROS)_ , pp. 13096–13103, IEEE, 2024. 

- [55] C. R. Garrett, T. Lozano-P´erez, and L. P. Kaelbling, “Pddlstream: Integrating symbolic planners and blackbox samplers via optimistic adaptive planning,” in _Proceedings of the International Conference on Automated Planning and Scheduling_ , 2020. 

- [56] D. Arthur and S. Vassilvitskii, “K-means++ the advantages of careful seeding,” in _Proceedings of ACM-SIAM Symposium on Discrete algorithms_ , 2007. 

- [57] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in _International Conference on Robotics and Automation (ICRA)_ , 2000. 

- [58] I. A. Sucan, M. Moll, and L. E. Kavraki, “The open motion planning library,” _IEEE Robotics and Automation Magazine (RA-M)_ , vol. 19, no. 4, pp. 72–82, 2012. 

- [59] Z. Kingston, M. Moll, and L. E. Kavraki, “Exploring implicit spaces for constrained sampling-based planning,” _International Journal of Robotics Research (IJRR)_ , vol. 38, no. 10-11, pp. 1151–1178, 2019. 

- [60] C. Muise, K. Taylor-Muise, and A. Coles, “Planning.domains.” http: //planning.domains/. 

- [61] N. Lipovetzky and H. Geffner, “Width and serialization of classical planning problems,” in _Proceedings of the 20th European Conference on Artificial Intelligence_ , ECAI’12, p. 540–545, IOS Press, 2012. 

- [62] Y. Su, P. Yu, M. Gerber, L. Ruan, and T.-C. Tsao, “Nullspace-based control allocation of overactuated uav platforms,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 6, no. 4, pp. 8094–8101, 2021. 

- [63] Y. Su, J. Li, Z. Jiao, M. Wang, C. Chu, H. Li, Y. Zhu, and H. Liu, “Sequential manipulation planning for over-actuated unmanned aerial manipulators,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2023. 

- [64] W. Wang, Z. Zhao, Z. Jiao, Y. Zhu, S.-C. Zhu, and H. Liu, “Rearrange indoor scenes for human-robot co-activity,” in _International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [65] Z. Han, J. Allspaw, G. LeMasurier, J. Parrillo, D. Giger, S. R. Ahmadzadeh, and H. A. Yanco, “Towards mobile multi-task manipulation in a confined and integrated environment with irregular objects,” in _International Conference on Robotics and Automation (ICRA)_ , 2020. 

- [66] C. Nam, S. H. Cheong, J. Lee, D. H. Kim, and C. Kim, “Fast and resilient manipulation planning for object retrieval in cluttered and confined environments,” _Transactions on Robotics (T-RO)_ , vol. 37, no. 5, pp. 1539–1552, 2021. 

- [67] B. Sundaralingam, S. K. S. Hari, A. Fishman, C. Garrett, K. Van Wyk, V. Blukis, A. Millane, H. Oleynikova, A. Handa, F. Ramos, _et al._ , “Curobo: Parallelized collision-free robot motion generation,” in _International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [68] Z. Li, Y. Niu, Y. Su, H. Liu, and Z. Jiao, “Dynamic planning for sequential whole-body mobile manipulation,” in _IEEE Conference on Industrial Electronics and Applications (ICIEA)_ , 2024. 

- [69] E. Kolve, R. Mottaghi, W. Han, E. VanderBilt, L. Weihs, A. Herrasti, M. Deitke, K. Ehsani, D. Gordon, Y. Zhu, _et al._ , “Ai2-thor: An interactive 3d environment for visual ai,” _arXiv preprint arXiv:1712.05474_ , 2017. 

- [70] K. Mo, S. Zhu, A. X. Chang, L. Yi, S. Tripathi, L. J. Guibas, and H. Su, “Partnet: A large-scale benchmark for fine-grained and hierarchical partlevel 3d object understanding,” in _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 

- [71] A. Bokhovkin, V. Ishimtsev, E. Bogomolov, D. Zorin, A. Artemov, E. Burnaev, and A. Dai, “Towards part-based understanding of rgbd scans,” in _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2021. 

- [72] Z. Zhang, L. Zhang, Z. Wang, Z. Jiao, M. Han, Y. Zhu, S.-C. Zhu, and H. Liu, “Part-level scene reconstruction affords robot interaction,” in _International Conference on Intelligent Robots and Systems (IROS)_ , 2023. 

- [73] M. Han, Z. Zhang, Z. Jiao, X. Xie, Y. Zhu, S.-C. Zhu, and H. Liu, “Reconstructing interactive 3d scenes by panoptic mapping and cad model alignments,” in _International Conference on Robotics and Automation (ICRA)_ , 2021. 

- [74] J. J. Gibson, _The perception of the visual world._ Houghton Mifflin, 1950. 

- [75] J. J. Gibson, _The senses considered as perceptual systems._ Houghton Mifflin, 1966. 

- [76] B. Magyar, N. Tsiogkas, J. Deray, S. Pfeiffer, and D. Lane, “Timedelastic bands for manipulation motion planning,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 4, no. 4, pp. 3513–3520, 2019. 

- [77] P. Yu, Y. Su, M. J. Gerber, L. Ruan, and T.-C. Tsao, “An overactuated multi-rotor aerial vehicle with unconstrained attitude angles and high thrust efficiencies,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 6, no. 4, pp. 6828–6835, 2021. 

- [78] F. Xiang, Y. Qin, K. Mo, Y. Xia, H. Zhu, F. Liu, M. Liu, H. Jiang, Y. Yuan, H. Wang, _et al._ , “Sapien: A simulated part-based interactive environment,” in _Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 11097–11107, 2020. 

