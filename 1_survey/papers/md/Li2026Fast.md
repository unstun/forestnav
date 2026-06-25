---
citation_key: Li2026Fast
arxiv_id: 2601.18548
arxiv_url: "https://arxiv.org/abs/2601.18548"
title: "Fast and Safe Trajectory Optimization for Mobile Manipulators With Neural Configuration Space Distance Field"
authors_short: "Yulin Li et al."
year: 2026
direction_tag: B_trajectory_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:31:43Z
origin: ai+web
reviewed: false
---

# Fast and Safe Trajectory Optimization for Mobile Manipulators With Neural Configuration Space Distance Field

Yulin Li<sup>1,2</sup>, Zhiyuan Song<sup>1</sup>, Yiming Li<sup>3</sup>, Zhicheng Song<sup>1</sup>, Kai Chen<sup>1</sup>, Chunxin Zheng<sup>1</sup>, Zhihai Bi<sup>1</sup>, Jiahang Cao<sup>4</sup>, Sylvain Calinon<sup>3</sup>, Fan Shi<sup>2</sup>, and Jun Ma<sup>1</sup>

Abstract—Mobile manipulators promise agile, long-horizon behavior by coordinating base and arm motion, yet wholebody trajectory optimization in cluttered, confined spaces remains difficult due to high-dimensional nonconvexity and the need for fast, accurate collision reasoning. Configuration Space Distance Fields (CDF) enable fixed-base manipulators to model collisions directly in configuration space via smooth, implicit distances. This representation holds strong potential to bypass the nonlinear configuration-to-workspace mapping while preserving accurate whole-body geometry and providing optimizationfriendly collision costs. Yet, extending this capability to mobile manipulators is hindered by unbounded workspaces and tighter base–arm coupling. We lift this promise to mobile manipulation with Generalized Configuration Space Distance Fields (GCDF), extending CDF to robots with both translational and rotational joints in unbounded workspaces with tighter base–arm coupling. We prove that GCDF preserves Euclidean-like local distance structure and accurately encodes whole-body geometry in configuration space, and develop a data generation and training pipeline that yields continuous neural GCDFs with accurate values and gradients, supporting efficient GPU-batched queries. Building on this representation, we develop a high-performance sequential convex optimization framework centered on GCDFbased collision reasoning. The solver scales to large numbers of implicit constraints through (i) online specification of neural constraints, (ii) sparsity-aware active-set detection with parallel batched evaluation across thousands of constraints, and (iii) incremental constraint management for rapid replanning under scene changes. Extensive randomized high-density benchmarks and real-robot experiments demonstrate consistently superior success rates, trajectory quality, and solve times compared to strong baselines, enabling fast, safe, and reliable whole-body planning with minimal initialization effort. Source code is available at the project website<sup>\*</sup>.

## I. INTRODUCTION

Mobile manipulators have emerged as essential tools for real-world robotic applications, combining mobility, dexterity, and workspace coverage to enable complex, contact-rich, and long-horizon tasks across both structured and unstructured environments [1], [2], [3], [4]. To accomplish these tasks, mobile manipulators must leverage their multiple degrees of freedom to coordinate arm and base motion, continuously reconfiguring whole-body posture to adapt to complex, cluttered environments while maintaining agility and ensuring safety. However, this synergy of mobility and manipulation introduces a fundamental planning challenge: planners must make rapid, reliable decisions in high-dimensional configuration spaces while respecting collision constraints derived from accurate geometric models of both the robot and the scene, which are essential for achieving agile, non-conservative performance [5], [6], [7], [8]. Despite recent advances in perception, whole-body planning, and optimization-based control for mobile manipulation [9], [10], [11], [12], [13], fast and reliable trajectory generation in cluttered, confined remains an open challenge.

![](Li2026Fast_figs/ab964911748f8264b3819bf3d42badc34edcbd298412c480e5be62eb958977ac.jpg)

![](Li2026Fast_figs/a11f1e33f78a296260e0d9f8de33dc884cfabd91c96fc977a278fe4aad7b2a55.jpg)

(b)  
![](Li2026Fast_figs/d16cd1ecbde7355f91430aae10fa83efecfd3442ef53af6a64b790e72061bd7c.jpg)  
Fig. 1: Trajectory generation in complex environments for mobile manipulators using the proposed numerical optimization algorithm with neural Generalized Configuration Space Distance Fields. Starting from a trivial initial guess (the mobile base linearly interpolated between start and goal while the manipulator joints are all zeros, i.e., kept upright), the solver generates collision-free trajectories from scratch, exhibiting smooth and agile maneuvers that leverage whole-body coordination for safe obstacle avoidance. (a) Simulation results are shown from front and top views. (b) Real-world experiments in a similarly cluttered setup.

Background. Traditional hierarchical “move-and-act” schemes [14], [15] decompose mobile manipulation into separate planning subproblems for the base and the arm, offering simplicity but constraining coordinated whole-body behaviors. This decoupling neglects the interdependence between base and manipulator, precluding whole-body reconfiguration to expand reachability in confined environments and leading to conservative or infeasible behavior [16], [17], [18]. To overcome these limitations, recent work has shifted toward whole-body planning, typically grouped into three families: sampling-based methods, reinforcement learning (RL), and optimizationbased planning.

Sampling-based methods such as PRM/RRT and their variants [19], [20], [21], [22] explore feasible connectivity through random sampling and collision checking, offering theoretical guarantees and broad applicability. Recent works extend these to mobile manipulation by unifying base and arm in highdimensional configuration space [23], [24]. However, in cluttered environments with narrow passages requiring tight basearm coordination, uniform or heuristic sampling becomes computationally burdensome and prone to connectivity failures. A couple of frameworks mitigate this by predefining constrained sampling regions or heuristic guidance [10], [17], but such strategies reintroduce scenario-dependent tuning and reduce planner generality. RL-based approaches learn control policies end-to-end, directly from state or sensor inputs to actions, typically by interacting with a simulator [25], [26], [27], [28]. Such methods typically demand substantial simulation training for each new scenario, often requiring millions of timesteps and extensive hyperparameter tuning to achieve strong performance [29]. While effective in structured settings, the resulting policies often generalize poorly to novel layouts and dynamics and are sensitive to distribution shift and partial observability. Moreover, discrepancies in perception, dynamics, and actuation create a sim-to-real gap that can significantly degrade real-world performance [30], necessitating careful engineering for reliable transfer.

In contrast, optimization-based methods offer a compelling alternative and serve as the focus of our work. By formulating whole-body mobile manipulation as a constrained optimization problem, they seek feasible, collision-free trajectories while optimizing task-relevant objectives such as smoothness, energy efficiency, or execution time [31], [32]. A key merit of this paradigm is its robustness and generalizability: once the environment is represented in a unified geometric [33] or distance-field form [34], the same optimization framework can be applied across diverse scenarios without scenariospecific retraining, enabling rapid adaptation to novel layouts and dynamic changes. Moreover, the kinematic and actuation redundancy inherent in mobile manipulators naturally lends itself to optimization techniques, allowing the system to exploit its full configuration space to generate agile, safe maneuvers that reach targets while simultaneously satisfying task-space collision avoidance and other operational constraints.

Challenges. Unlike fixed-base manipulators, mobile manipulators operate in unbounded workspaces and must navigate complex, cluttered obstacle layouts. Current state-of-the-art methods adopt a two-stage pipeline with front-end path search followed by back-end trajectory optimization [10], [35]. In practice, the front end carries the primary burden through elaborate, multi-layer search strategies aimed at reducing sampling difficulty over the combined translational and rotational motion space. A common approach decouples the problem by first planning a base trajectory and then searching for arm configurations along this fixed base path. The back-end optimizer is consequently reduced to a post-processing module that smooths and slightly refines the front-end solution locally, often converging within only a few iterations.

Despite its computational efficiency, this paradigm suffers from fundamental limitations in both stages. On the frontend side, decoupling the base and arm search undermines holistic whole-body coordination. In complex environments where simultaneous coordination is required amid intricate obstacle layouts, the front-end search can fail; this would cause the entire pipeline to collapse since the back-end optimizer is constrained to local refinements near the front-end solution. Once the front end produces a poor-quality trajectory, the optimizer cannot recover, despite its potential exploration capability. On the back-end side, these methods typically rely on the environment Euclidean signed distance field (ESDF) and approximate the robot with collision spheres. While this reduces collision constraints complexity, it creates a fundamental mismatch: collision costs are defined in workspace as the sum of ESDF penalties over spheres, whereas the position of each sphere is coupled through highly nonlinear forward kinematics. Moreover, a sparse set of spheres can inaccurately represent the true collision geometry, leading to overly conservative or unsafe clearance estimates. From the optimization perspective, the nonlinear coupling yields a strongly nonconvex landscape; with imperfect initial trajectories, gradientbased solvers easily become trapped in poor local minima as workspace gradients induce misleading configuration-space updates.

Overall, the difficulty stems from three root causes: (i) the nonlinear mapping between configuration-space variables and workspace-based collision constraints; (ii) the inherent computational intractability of enforcing whole-body collision avoidance with precise link geometries [36], [37], which necessitates simplified proxies (e.g., spheres or point sets [38], [39]) that compromise geometric fidelity; (iii) the unbounded workspace and intricate obstacle layouts, which make the optimizer highly sensitive to initialization yet render high-quality initial guesses non-trivial to obtain. It leaves an interesting question: Can we enforce collision avoidance directly in configuration space to circumvent the intricate nonlinear mapping between configuration variables and workspace constraints while preserving accurate robot geometries?

Recently, inspired by the robot-centric signed distance field (SDF) [40], [41], [42], which measures the Euclidean distance between a robot surface and environment points, the concept of the Configuration Space Distance Field (CDF) has been proposed to measure the minimum distance from a current robot configuration to environment points using configuration metrics for robot manipulators [43]. Specifically, for an obstacle point p, CDF measures the minimum configuration space distance between the current configuration and the zero-level configuration set, where the latter comprises all configurations that result in contact between any point on the robot’s surface and p. Thus, CDF naturally incorporates whole-body geometries without conservative approximation, while simultaneously embedding the inverse kinematic problem within its formulation to maintain Euclidean distance properties in the high-dimensional configuration space despite the highly nonlinear propagation along kinematic chains.

Crucially, we recognize that these properties make CDF particularly well-suited for gradient-based trajectory optimization. The constraint Jacobian matrices derived from CDF provide accurate local models that facilitate faster convergence in iterative solvers [44], [45], [46], while their continuous neural representation enables efficient batched queries of collision constraints and their derivatives across trajectory waypoints. This naturally motivates us to investigate how CDF can be effectively integrated into trajectory optimization frameworks to address the computational challenges outlined above.

Contributions. In this work, we address the following research problems: (i) How to generalize CDF to mobile manipulators with additional translational DoFs in an unbounded workspace, while preserving its merits for purely rotational joints. (ii) How to learn implicit neural CDF representations for mobile manipulators that provide accurate values and gradients, while enabling fast, parallel online queries for numerical optimization. (iii) How to design a high-performance numerical optimization algorithm with CDF-based constraints that enforces collision avoidance directly in configuration space, enabling rapid generation of agile, collision-free trajectories in complex obstacle layouts, even from naive initial guesses.

Specifically, we first propose the concept of Generalized CDF (GCDF) for robots with both translational and rotational joints. We show that, from both theoretical and experimental perspectives, the properties of the original CDF can be extended to GCDF with minimal modification. Unlike fixedbase manipulators, the introduction of translational dimensions leads to exponential growth in data requirements, and the quality and coverage of data on the zero-level set significantly impact both training effectiveness and subsequent optimization performance. To solve these, we carefully develop a data collection and training pipeline based on the established theories to obtain neural CDF functions for mobile manipulators, yielding continuous and accurate implicit representations that support efficient GPU-accelerated queries and are well-suited for integration with numerical optimization.

Second, we develop and open-source a high-performance C++ sequential convex optimization solver for large-scale trajectory optimization with implicit GCDF constraints. The solver employs an ℓ<sub>1</sub>-penalty formulation and iteratively solves QP subproblems using first-order constraint information within a local trust region, together with globalization mechanisms that enable recovery from initial guesses far from the optimum. To support neural implicit collision reasoning, we extend the framework to (a) transform neural network outputs as implicit constraints; (b) batch-evaluate constraint values and gradients in parallel and exploit the sparsity pattern of active collision constraints at each iteration, substantially reducing both problem assembly and solve time under thousands of constraints; and (c) allow online injection and removal of GCDF constraints without problem reconstruction, which is critical for rapid replanning as robot–obstacle interactions change. As previewed in Fig. 1, the resulting solver optimizes directly in configuration space and can recover from a trivial initial guess to produce agile, collision-free motions in highly cluttered scenes.

We emphasize that obstacle density and distribution complexity are critical factors for validating planning performance, as both the computational burden (due to the number of constraints) and the difficulty of escaping inferior local minima increase dramatically with environmental complexity. Finally, to rigorously validate the superiority of our framework, we design multiple randomized high-density obstacle scenarios and conduct extensive comparisons with benchmark methods in these challenging environments. Results demonstrate that the developed numerical algorithm, with GCDF constraints, can rapidly compute safe, robust, and non-trivial whole-body motions even in highly cluttered spaces. We further deploy the algorithm on a real mobile manipulator system in complex real-world scenarios, demonstrating its robustness and effectiveness in practical applications.

To summarize, our contributions are:

• Generalized CDF. We introduce GCDF for robots with both translational and rotational joints, and show, both theoretically and empirically, that core CDF properties carry over with minimal modification.

• Neural GCDF. We develop a scalable data generation and training pipeline that avoids data explosion in unbounded workspaces by reconstructing high-quality coverage of the zero-level set through translation-equivariant aggregation of grid-based subsets, yielding neural GCDFs with accurate values/gradients and fast GPU-parallel queries.

• Solver Implementation. We release an open-source high-performance C++ solver that enforces collision avoidance directly in configuration space via neural implicit GCDF constraints, with online constraint specification, batched GPU evaluation, and sparsity-aware handling of large-scale constraints.

• Performance. Our method achieves consistently superior performance for rapid, safe, and reliable collision-free whole-body planning, outperforming strong baselines in randomized high-density clutter and validating on real hardware.

Paper organization. We review related work in Section II. We present the theory and training pipeline for GCDF in Section III, followed by its integration with the numerical algorithm for trajectory optimization in Section IV. Experimental results are demonstrated in Section V. We conclude with future

directions in Section VI.

## II. RELATED WORKS

## A. Collision Avoidance

Approaches to collision avoidance in robot motion planning can be broadly categorized into two distinct paradigms, defined by their underlying representation of safety. The first paradigm focuses on explicitly constructing a representation of the collision-free space, and the second paradigm operates by modeling collision pairs and enforcing safety margins.

1) Motion Planning in Collision-Free Space: This category treats motion planning as a two-stage process: first constructing a structural representation of the collision-free space, then computing feasible trajectories within that structure. Classical approaches, including cell decomposition [47], [48], visibility graphs [49], [50], and Voronoi diagrams [51], systematically partition or reduce the configuration space into discrete geometric structures. While effective in low-dimensional settings, these deterministic methods become computationally intractable in high-dimensional spaces. Sampling-based planners [52], [53], [21] address this by probabilistically capturing connectivity, achieving widespread adoption in robot manipulations [54], [55], [56]. More recently, modern optimizationbased approaches favor decomposing free space into sequences of convex regions [57], [58], [59], [60], [61]. These methods grow convex polytopes in collision-free space and then constrain robot motion by enforcing containment relationships between robot geometry and these safe regions [62], [63]. Depending on the geometric representation, such as points [59], [64], polytopes [65], [66], or semialgebraic sets [36], different containment constraints can be formulated within the optimization framework. This paradigm has been extended to manipulators and mobile manipulators by allocating separate convex regions to each link [66], [33], [38], enabling coordinated whole-body planning.

2) Safety Margins Between Collision Pairs: The second category focuses on explicitly modeling the geometric relationship between robot and obstacles to enforce positive distance margins. Compared to convex decomposition methods, which face combinatorial challenges in selecting which free region the robot should occupy at each time step [64], [67] and ensuring safe transitions between regions [36] (as overlapping quality between adjacent regions is often difficult to guarantee), distance-based methods provide a more direct and complete solution: safety can be absolutely guaranteed by enforcing minimum distance thresholds between the robot and all obstacles. The most straightforward approach explicitly constructs distance functions between robot-obstacle collision pairs and enforces safety thresholds [6], [7], [68], [69]. However, distance functions for general geometries in complex configuration spaces are inherently difficult to obtain, typically leading to oversimplified collision representations such as points or spheres. Some indirect methods have been developed to handle more general shapes for single rigid bodies: control barrier functions (CBFs) based on the dual formulation of minimum distance between polytopes [70], and bi-level optimization that enforces scaling factors on geometric primitives to ensure collision-free configurations [37].

Another approach computes separating hyperplanes between the robot and obstacle convex hulls [71], [72]. In principle, these methods jointly optimize both the trajectory variables and the hyperplane parameters at each time step, ensuring that a separating plane can be found between the robot and obstacles throughout the motion.

However, for multi-link robotic systems such as manipulators and mobile manipulators, these direct approaches remain difficult to generalize due to kinematic coupling between links and the high dimensionality of the configuration space. As an alternative, distance fields have been widely adopted. The principle behind this approach is to build an implicit representation that encodes the minimum distance between environmental points and their nearest robot surface points [73], [42], [74] or nearest obstacle points [75], [76], [77]. This implicit structure allows querying minimum distance values and their gradients with respect to robot configurations, which can be utilized to detect collisions and generate repulsive forces that push the robot away from obstacles [43], [78]. These methods have great potential for application to robotic systems with complex configurations and are the focus of this paper. We provide a comprehensive review of distance fields and their evolution toward configuration-space representations in Section II-B.

## B. Distance Fields and their Applications

Distance fields, and in particular SDFs, encode at every point the signed distance to the closest surface. This scalar field captures three essential aspects of safety in a unified way: the zero level set indicates whether a point is in collision, the distance value measures how much clearance it has, and the gradient specifies in which direction clearance increases. In robotics, this makes SDFs a natural choice for linking perception and motion generation. Voxel-based TSDF/ESDF maps support dense 3D reconstruction and local planning for mobile robots and MAVs [75], [34], while continuous and neural SDFs [77], [79], [73] provide compact scene representations with efficient distance and gradient queries. These environment-centric distance fields are routinely used as smooth collision costs or repulsive potentials in trajectory optimization [6] and MPC-based planners [80], giving motiongeneration algorithms a continuous “safety landscape” instead of a binary collision oracle.

More recently, there has been a shift from environmentcentric to robot-centric distance fields, in which the robot itself is represented as a distance field. This removes the need to update a global scene SDF online as the environment changes, enabling more efficient distance queries and improving responsiveness in dynamic scenarios [40], [42]. Moreover, a robot SDF provides derivatives with respect to joint angles, encoding both proximity to collision and directions in joint space that increase clearance, which aligns well with gradient-based motion optimization. A central challenge is how to couple the distance representation with the robot joint configuration. Existing methods address this in two principal ways: kinematicchain-based models explicitly propagate fixed link-wise SDFs through forward kinematics, whereas end-to-end learning approaches embed geometry and kinematics into a single jointdependent distance function. Methods such as [42], [81], [82], [83] explicitly encode link geometries and compose them along the known kinematic chain, preserving geometric fidelity and yielding well-structured derivatives from task space to joint space, which is advantageous in scenarios with tight clearances and detailed contact reasoning. In contrast, endto-end neural approaches learn a single implicit model that maps joint configurations and workspace points directly to distances and gradients [40], [41]. These models trade some geometric accuracy for highly efficient, uniform inference, making them suitable for high-frequency reactive control and large-scale motion generation where many distance queries must be evaluated online. In both cases, representing the robot as a distance field yields a unified, differentiable representation for reasoning about self-collision, contact, and clearance.

While most distance-field methods operate in task space, there is increasing interest in lifting distance reasoning directly to configuration space. CDF [43] defines a scalar field over joint configurations, where the value at each configuration equals the minimal joint motion required to reach the collision manifold, with its gradient providing the corresponding avoidance direction. In contrast to task-space SDFs, CDF satisfies an eikonal property in configuration space: its level sets are uniformly spaced, and its gradient has unit norm and consistently points away from the collision set. This eliminates distortions or vanishing gradients induced by the nonlinear mapping between task space and joint space, and enables onestep gradient projection for inverse kinematics. Consequently, motion generation schemes built around distance fields can be applied directly in joint space by replacing a workspace SDF with a joint-space CDF. Building on this idea, subsequent work has leveraged CDF for motion planning and control by integrating it with barrier-function formulations [84], gradientbased trajectory optimization [85], and model predictive path integral control [86], highlighting CDF as an effective representation for efficient and safe motion generation in joint space. However, these approaches focus primarily on fixedbase manipulators, and CDF for mobile manipulators where the configuration space couples Euclidean base motion with joint orientations, have not yet been systematically explored. Moreover, efficient and robust numerical solvers capable of handling such structured, implicitly defined constraints are still lacking, limiting the practicality of existing methods.

## III. NEURAL CONFIGURATION SPACE DISTANCE FIELD FOR MOBILE MANIPULATORS

## A. Preliminaries

Let us first recall the original definition of CDF.

1) Signed Distance Field: Before introducing the definition of CDF, we first examine SDF, a widely adopted concept in collision checking and avoidance tasks, as it helps illuminate the advantages of CDF.

SDF was originally defined in task space as the distance from a query point $\pmb { p }$ to the boundary of a set Ω, with positive and negative signs indicating whether the point lies outside or inside Ω, respectively. As illustrated in Fig. 2-left , this concept has been extended to represent the distance between a workspace point $\pmb { p }$ and the robot surface, denoted as $\partial r .$ , at a given configuration $\mathbf { \nabla } q \mathbf { \cdot }$

$$
f _ {s} (\boldsymbol {p}, \boldsymbol {q}) = \pm \min _ {\boldsymbol {p} ^ {\prime} \in \partial r (\boldsymbol {q})} \| \boldsymbol {p} ^ {\prime} - \boldsymbol {p} \|.\tag{1}
$$

While the signed distance $f _ { s }$ maintains Euclidean properties in workspace (or task space), the forward kinematics embedded in the manifold constraint ${ \pmb p } ^ { \prime } \in \partial r ( { \pmb q } )$ introduces significant nonlinearity in configuration space, where the optimization is conducted.

![](Li2026Fast_figs/3ac0fa41f8765a7cac513639801a251cf4097c766b3e4c8f1dacb7004e7a7734.jpg)  
Fig. 2: Illustration of SDF (left) and CDF (right) for a query point $\pmb { p }$ at configuration $\mathbf { \delta } \mathbf { q } .$ SDF measures the taskspace distance from $\pmb { p }$ to the nearest point $\pmb { p } ^ { \prime }$ on the robot surface, as defined in (1). In contrast, CDF measures the configuration-space (angular) distance from q to the nearest contact configuration $\pmb q ^ { \prime }$ on the zero-level set induced by $^ { p , }$ as defined in (3).

2) Configuration Space Distance Field: We now present the concept of CDF. In contrast to the minimum distance in task space as defined in (1), CDF is defined as the minimum distance in configuration space. Specifically, for an articulated robotic system with pure rotational joints, this represents the minimum distance in radius [43], as illustrated in Fig. 2-right.

First, we define the zero-level configuration set for a given workspace point $\pmb { p }$ as:

$$
\mathcal {Z} (\boldsymbol {p}) = \{\boldsymbol {q} \mid f _ {s} (\boldsymbol {p}, \boldsymbol {q}) = 0 \},\tag{2}
$$

where, based on the SDF definition in (1), Z represents the set of all configurations where $\pmb { p }$ lies on the robot surface. The CDF is then formally defined as:

$$
f _ {c} (\boldsymbol {p}, \boldsymbol {q}) = \min _ {\boldsymbol {q} ^ {\prime} \in \mathcal {Z} (\boldsymbol {p})} \| \boldsymbol {q} ^ {\prime} - \boldsymbol {q} \|.\tag{3}
$$

For a given point $^ { p , }$ CDF measures the minimum radial distance from the current configuration to any configuration that results in contact with $\mathbf { \delta } _ { p . }$

Remark 1. CDF effectively bridges task space and configuration space while preserving several advantageous properties: it maintains the implicit structure and Boolean operations of SDF, and more significantly, it preserves the uniform gradient property with Euclidean distance in configuration space. These characteristics collectively make CDF an ideal candidate for integration with gradient-based numerical optimization algorithms, enabling simultaneous safety guarantees and task achievement. Moreover, the efficient data collection and network training proposed in [43] provides a practical pipeline for neural network-encoded CDF function that enables fast batch-parallel computation of both distance values and gradients during online operation.

B. Configuration Space Distance Field for Mobile Manipulator

1) Generalized CDF: Originally, when training the CDF function, only rotational joints are considered since the planar translation motion $( \mathrm { i . e . , } ~ q ^ { t } )$ would make the workspace unbounded, and there are inherently different scales between translational and rotational movements.

Theoretically, the shift caused by base translation can be mitigated by transforming obstacle points to the mobile base frame, and the gradients with respect to translational degrees of freedom can be obtained through the chain rule by utilizing the gradients of obstacle point positions. However, in practical training scenarios, fixing the mobile base significantly constrains the actual workspace and confines the reachable space. This leads to insufficient and non-general zero-levelset data, resulting in obstacle gradients that lack physical intuition. Therefore, in our training process, we redefine the CDF to incorporate translational degrees of freedom while introducing appropriate scaling factors to balance translational distances and rotational angles. Similar to (3), we introduce the definition of the generalized CDF with translational Dofs:

Definition 1 (Generalized CDF). For a robot configuration $\pmb q \in \mathbb R ^ { n }$ comprising a translational component $q ^ { t }$ and a rotational component $\pmb q ^ { r } ,$ , and an environmental point $\pmb { p } \in \mathbb { R } ^ { 3 }$ , the generalized configuration space distance field (GCDF) $f _ { c } ^ { g } ( \pmb { p } , \pmb { q } ) : \mathbb { R } ^ { n } \times \mathbb { R } ^ { 3 }  \mathbb { R }$ is:

$$
f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}) = \pm \min _ {\boldsymbol {q} ^ {\prime} \in \mathcal {Z} (\boldsymbol {p})} \| \boldsymbol {q} ^ {\prime} - \boldsymbol {q} \| _ {M},\tag{4}
$$

where $\mathcal { Z } ( \pmb { p } )$ denotes the zero level set manifold $o f$ configurations satisfying the contact condition at point ${ \pmb p } ,$ and $M \ \in \ S _ { + } ^ { n }$ is a positive semidefinite diagonal weighting matrix that induces the weighted norm $\lVert \cdot \rVert _ { M }$ . The positive and negative signs indicate whether p lies outside or inside the robot surface $\Omega ( q )$

Remark 2. The introduction of the weighting matrix M in this generalized formulation serves two crucial purposes. First, it controls the relative influence of translational and rotational distances on the CDF value. Second, it shapes the characteristics of the nearest configuration by influencing the gradient direction and consequently the robot’s motion tendency in proximity to objects.

A key theoretical foundation of the original CDF is its satisfaction of the eikonal equation in configuration space, which ensures unit gradient norms and enables single-step projections to the zero level set. This property theoretically guarantees closed-form whole-body inverse kinematic solutions without numerical iterations. To maintain this valuable property during training, gradient norm and projection error regularization terms are incorporated into the loss function. However, when extending CDF to the full configuration space with weighted norms, a critical issue emerges: following the gradient direction no longer guarantees reaching the zero level set surface, and the optimal step size becomes undetermined. This challenges both the theoretical properties and their corresponding training objectives. Following the spirit of the original CDF framework, we extend its theoretical properties to the weighted configuration space through the following theorem:

Theorem 1 (Properties of GCDF). For any configuration q and environmental points p where $f _ { c } ^ { g } ( \pmb { p } , \pmb { q } )$ is differentiable with respect to q, the following properties hold:

1) (Weighted Eikonal Equation). The partial derivative of f <sup>g</sup> with respect to q satisfies the weighted eikonal equation:

$$
\| \nabla_ {\boldsymbol {q}} f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}) \| _ {M ^ {- 1}} = 1
$$

2) (Single-Step Projection). For any initial configuration q<sub>0</sub>, its closest configuration $\pmb q _ { z } \in \mathcal { Z } ( \pmb p )$ can be reached through a single-step projection:

$$
\boldsymbol {q} _ {z} = \boldsymbol {q} _ {0} - \lambda d,
$$

where $\lambda ~ = ~ f _ { c } ^ { g } ( { \pmb p } , { \pmb q } _ { 0 } )$ denotes the step length and $d = M ^ { - 1 } \nabla _ { \pmb { q } } f _ { c } ^ { g } ( \pmb { p } , \pmb { q } _ { 0 } )$ defines the projection direction.

Proof. See Appendix A.

While Theorem 1 provides theoretical guidance for training effective GCDF and enables finding the nearest configurations on the zero-level set through biased gradient projection, practical considerations necessitate the signed formulation in Definition 1. Specifically, the unsigned nature of the original CDF definition in (3) would cause numerical issues for gradientbased optimization when the robot is currently intersecting with obstacles. To illustrate this, consider the one-dimensional case shown in Fig. 3. If the configuration q to be optimized initially lies between two points on the zero-level set, gradientbased numerical methods theoretically cannot escape the local maximum at ${ { q } _ { 0 } } \mathrm { ~ } ( i . e . ,$ , pushing the obstacle away from the robot). Therefore, the signed GCDF formulation resolves this by reversing the sign for penetrating configurations, ensuring gradients consistently point toward collision-free space.

## C. Neural GCDF

Having established the definition and properties of GCDF, we now present the training methodology for neural GCDF representations mapping from workspace-configuration pairs to their corresponding GCDF values, which ensure highquality distance fields suitable for numerical optimization. Our pipeline generally follows the procedure proposed in [43]:

(i) Robot SDF Construction. We obtain the SDF representation of the mobile manipulator, i.e., $f _ { s } ( p , q )$ , using the method in [42], enabling efficient distance queries and gradient computation.

![](Li2026Fast_figs/fdf8cf7d3b8394e5b4e29b1be510af807077704df17c075b8ed5d9089033a3df.jpg)

![](Li2026Fast_figs/cb892adc901bef37dfe36f62ca134335b4f75542ab368c548d9dba1f293491b5.jpg)  
Fig. 3: Illustration of GCDF values for a 1-DoF planar arm. The obstacle induces two symmetric contact configurations on the zero-level set, denoted by $\pmb q _ { 1 }$ and $\pmb { q } _ { 2 }$ . For the unsigned GCDF, the distance function exhibits a spurious local maximum at $\pmb q _ { 0 }$ , where the obstacle is equally distant from both arm sides, which can mislead gradient-based numerical solvers. Introducing the sign based on penetration removes this pathology, yielding smooth and consistent gradient directions toward the contact set.

(ii) Zero-Level Set Approximation. We collect a workspace point set $\mathcal { P } \subset \mathbb { R } ^ { 3 }$ . For each $\pmb { p } \in \mathcal { P }$ , we approximate the zero-level set $\mathcal { Z } ( \pmb { p } )$ by performing gradient descent on the robot SDF, starting from configurations q sampled from a configuration set $\mathcal Q \subset \mathbb { R } ^ { n }$

(iii) Dataset Preparation. For each newly sampled workspace-configuration pair $( p , q )$ we compute the ground-truth GCDF value according to Definition 1 by finding the minimum distance from $\pmb q$ to the approximated zero level set $\mathcal Z ( p )$

(iv) Neural Network Training. We design the network architecture and loss functions, then train the neural implicit function to regress GCDF values across the configuration space.

However, extending this pipeline to mobile manipulators introduces several critical challenges that must be addressed. The first challenge stems from the exponential growth of zero-level sets. Unlike fixed-base manipulators with bounded workspaces, mobile manipulators operate in unbounded translational spaces. For a given workspace point $^ { p , }$ the corresponding zero-level set $\mathcal { Z } ( \pmb { p } )$ contains exponentially more configurations due to the infinite reachability from different base positions. This leads to two major issues: (i) the computational cost of approximating $\mathcal { Z } ( \pmb { p } )$ can take days to complete, and (ii) gradient descent from slightly different base positions often converges to nearly identical arm configurations, resulting in massive redundancy. Consequently, the standard approach of sampling a fixed number of configurations becomes insufficient to construct informative zero-level sets, leading to significant bias when querying GCDF values during training.

The second challenge involves balancing model complexity and efficiency. To ensure compatibility with downstream numerical optimization, we must carefully balance inference efficiency against model accuracy. This requires joint consideration of network architecture complexity and data density.

![](Li2026Fast_figs/1e97eb56d702d63b251846539f58956f09d3351d0bdf72745f14459d20f728ab.jpg)

Reconstruction of(c) $\mathcal { Z } ( \pmb { p } )$ from $\widetilde { \pmb { \mathscr { Z } } } ( \pmb { p } _ { i } )$ with all $\pmb { p _ { i } }$  
![](Li2026Fast_figs/488df9eea0198e8a411d12cd8aa595d2b6cbe4b861c867929c92cb5a5374daa4.jpg)  
Fig. 4: Construction of zero-level set for mobile manipulators. (a) For each workspace point p on the grid centered at the robot origin, we construct a representative subset $\tilde { \mathcal { Z } } ( p ) \subset$ $\mathcal { Z } ( \pmb { p } )$ by fixing the base translation and solving for contact configurations over the arm joints and base rotations. (b) For a new query point $\pmb { p }$ with height $p _ { z } .$ , we gather all grid points $\pmb { p } _ { i }$ on the same horizontal slice $( { \bf p } _ { i , z } ~ = ~ { \bf p } _ { z } )$ in a neighborhood around $\mathbf { \delta } _ { p . }$ (c) We reconstruct the full zero-level set $\mathcal { Z } ( \pmb { p } )$ by taking the union of the precomputed subsets on that slice and compensating for their horizontal offsets, effectively translating the base while reusing the same arm contact configurations.

Indeed, overly complex networks or dense sampling dramatically increase training costs, while insufficient capacity or sparse data compromise the smoothness and accuracy of the learned GCDF, degrading optimization performance.

The third challenge concerns loss function design. The standard loss functions designed for fixed-base manipulators fail to capture the unique properties of mobile manipulator GCDFs. We require modified loss formulations that account for the increased dimensionality and ensure the learned distance field exhibits the smoothness and gradient consistency necessary for effective collision avoidance optimization. We now present our solutions to these challenges.

Data Preparation. Our data preparation process consists of two phases: (1) offline computation of zero-level sets, and (2) online sampling of representative workspace-configuration pairs with their corresponding GCDF values. As we noted earlier, when constructing the zero-level sets of ${ \mathbf { } } p ,$ considering all possible base positions $( q _ { x } ^ { t } , q _ { y } ^ { t } )$ would lead to data explosion and information redundancy, as the reachable workspace becomes unbounded when the base can translate freely. To mitigate this issue, we fix the base position at the origin $( q _ { x } ^ { t } = q _ { y } ^ { t } = 0 )$ during the offline phase, computing only a representative subset of the true zero-level set:

$$
\tilde {\mathcal {Z}} (\boldsymbol {p}) = \{\boldsymbol {q} \in \mathcal {Z} (\boldsymbol {p}) \mid q _ {x} ^ {t} = 0, q _ {y} ^ {t} = 0 \}\tag{5}
$$

Specifically, as shown in Fig. 4(a), we first discretize the workspace around the robot center into a $T \times T \times T$ volumetric grid. For each grid point p, we compute a dense subset $\tilde { \mathcal { Z } } ( p )$ efficiently by concurrently solving the following unconstrained optimization problem from a batch of randomly sampled initial arm configurations of N initial arm and base rotational configurations using a quasi-Newton method [87]:

$$
\min _ {\boldsymbol {q}} f _ {s} ^ {2} (\boldsymbol {p}, \boldsymbol {q}),\tag{6}
$$

Note that we freeze the translational elements in q at the origin during optimization, focusing solely on finding optimal arm and base rotations. This subset $\tilde { \mathcal { Z } } ( p )$ addresses the computational challenge and avoids the data explosion problem, but it inevitably loses information about base mobility.

To recover the missing information during the online phase, we leverage a key insight about mobile manipulators: the arm’s relative reachability with respect to obstacles is translationequivariant in the horizontal plane.. In other words, if a manipulator can reach a point $\pmb { p }$ from base position $( 0 , 0 )$ with joint configuration $\pmb q ^ { r }$ , then it can reach point $\pmb { p } ^ { \prime }$ from base position $( \Delta x , \Delta y )$ with the same joint configuration $\pmb q ^ { r }$ where $\pmb { p } ^ { \prime } = \pmb { p } + [ \Delta x , \Delta y , 0 ] ^ { \top }$

Based on this observation, for a new query point ${ \textbf { \em p } } =$ $[ p _ { x } , p _ { y } , p _ { z } ] ^ { \top }$ , we can reconstruct its complete zero-level set $\mathcal { Z } ( \pmb { p } )$ by aggregating the precomputed subsets from all grid points $\mathbf { \nabla } p _ { i }$ centered around p with the same height, as illustrated in Fig. 4(b)-Fig. 4(c), while compensating for the horizontal displacement:

$$
\mathcal {Z} (\boldsymbol {p}) = \bigcup_ {i: \boldsymbol {p} _ {i, z} = \boldsymbol {p} _ {z}} \left\{\left[ \boldsymbol {p} _ {i, x}, \boldsymbol {p} _ {i, y}, \boldsymbol {q} ^ {r ^ {\top}} \right] ^ {\top} \mid \boldsymbol {q} ^ {r} \in \tilde {\mathcal {Z}} (\boldsymbol {p} _ {i}) \right\}.\tag{7}
$$

Intuitively, this is equivalent to virtually translating the robot base to position $\mathbf { \nabla } p _ { i }$ , treating it as the new origin, and then combining the configurations from $\tilde { \mathcal { Z } } ( \pmb { p } _ { i } )$ to reach the target point. This concatenation of zero-level sets from the $T \times T$ grid points ${ \mathbf { } } p _ { i } ,$ , with appropriate base position adjustments, recovers the rich information about base mobility that was sacrificed in the offline phase.

For each workspace-configuration pair $( p , q )$ , the ground truth GCDF value is computed as:

$$
f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}) = \operatorname{sgn} (f _ {s}) \min _ {\boldsymbol {q} _ {i} \in \mathcal {Z} (\boldsymbol {p})} \| \boldsymbol {q} - \boldsymbol {q} _ {i} \| _ {M},\tag{8}
$$

where M is the weight matrices defined in Definition 1, and $\operatorname { s g n } ( f _ { s } )$ indicates the collision status determined by the sign of the SDF value $f _ { s } ( p , q )$ . This formulation accounts for both the joint-space distance and the horizontal displacement cost, providing a comprehensive measure of configuration proximity.

Network Architecture and Loss Design. The Neural GCDF employs a 7-layer MLP architecture. The MLP is trained using the concatenation of $\pmb { p }$ and q as input, we randomly sample $b _ { 1 }$ grid points in the workspace and $b _ { 2 }$ configurations for each point, resulting in an input tensor of size $\mathbb { R } ^ { \mathsf { \breve { ( } } b _ { 1 } b _ { 2 } ) \times ( 3 + n ) }$ . The network outputs the corresponding GCDF value for each input pair, resulting in an output of size $\mathbb { R } ^ { b _ { 1 } \times b _ { 2 } }$ The design of our neural GCDF loss function is inspired by the original CDF framework [43] and tailored to the theoretical properties of GCDF established in Theorem 1. Specifically, we incorporate the distance loss ${ \mathcal { L } } _ { \mathrm { d i s t } }$ for distribution fitting, the gradient loss $\mathcal { L } _ { \mathrm { g r a d } }$ for gradient direction regularization, the tension loss L for smoothness enhancement, and the eikonal loss $\mathcal { L } _ { \mathrm { e i k o n a l } }$ to enforce the weighted eikonal property. These loss terms collectively ensure that the trained implicit neural GCDF possesses valid field values and gradient magnitudes/directions that conform to the theoretical guarantees in Theorem 1, enabling nearest configurations on the zero-level set to be reached via single-step gradient projection.

TABLE I: Loss function design for training neural GCDF.

<table><tr><td>Loss</td><td>Definition</td></tr><tr><td> $\mathcal{L}_{\text{dist}}$ </td><td> $\frac{1}{b_1 b_2} \sum_{i=1}^{b_1} \sum_{j=1}^{b_2} \left( \hat{f}_c^g(p_i, q_j) - f_c^g(p_i, q_j) \right)^2$ </td></tr><tr><td> $\mathcal{L}_{\text{grad}}$ </td><td> $\frac{1}{b_1 b_2} \sum_{i=1}^{b_1} \sum_{j=1}^{b_2} \left( 1 - \frac{\nabla_q \hat{f}_c^g(\boldsymbol{p}_i, \boldsymbol{q}_j)^T \cdot \nabla_q f_c^g(\boldsymbol{p}_i, \boldsymbol{q}_j)}{\|\nabla_q f_c^g(\boldsymbol{p}_i, \boldsymbol{q}_j)\| \| \nabla_q f_c^g(\boldsymbol{p}_i, \boldsymbol{q}_j)\| } \right)^2$ </td></tr><tr><td> $\mathcal{L}_{\text{eikonal}}$ </td><td> $\frac{1}{b_1 b_2} \sum_{i=1}^{b_1} \sum_{j=1}^{b_2} (\|\nabla_q f_c^g(\boldsymbol{p}, \boldsymbol{q})\|_{M^{-1}} - 1)^2$ </td></tr><tr><td> $\mathcal{L}_{\text{tension}}$ </td><td> $\frac{1}{b_1 b_2} \sum_{i=1}^{b_1} \sum_{j=1}^{b_2} \|\nabla_q \hat{f}_c^g(p_i, q_j)\|^2$ </td></tr></table>

Detailed definitions of these loss components are provided in Table I, with the variables denoted by a hat (ˆ) representing the ground truth values. The total loss is formulated as a weighted sum of the four components:

$$
\mathcal {L} _ {\mathrm{total}} = \lambda_ {1} \mathcal {L} _ {\mathrm{dist}} + \lambda_ {2} \mathcal {L} _ {\mathrm{grad}} + \lambda_ {3} \mathcal {L} _ {\mathrm{eikonal}} + \lambda_ {4} \mathcal {L} _ {\mathrm{tension}}.\tag{9}
$$

## IV. FAST AND SAFE TRAJECTORY OPTIMIZATION

Building upon the neural GCDF representation trained offline (Section III), which provides dense value and gradient information of GCDF through a PyTorch model, this section presents our trajectory optimization framework for mobile manipulators. We describe: (1) the collision-free trajectory optimization formulation and GCDF-based constraint handling to ensure gradient and value validity; (2) the numerical algorithm for solving the nonlinear program and our efficient implementation that bridges the $\mathrm { P y }$ Torch model with a C++ solver by exploiting parallelization and constraint sparsity; and (3) a perception-integrated navigation framework that enables continuous, safe, and fast online replanning for long-range navigation in unknown environments.

A. Collision-Free Trajectory Optimization for Mobile Manipulator

We now formalize the trajectory optimization problem for a mobile manipulator system composed of a mobile base and an articulated robot arm.

Problem Formulation. Denote the optimization horizon as $N ,$ and $\ b { q } _ { i } \in \mathbb { R } ^ { n }$ the configuration at the ith step for $\forall i =$

$1 , 2 , \ldots , N$ . By separating the configuration variables into base translational and rotational DoFs, and incorporating velocity control variables, we define the full state variable at time step i as:

$$
\boldsymbol {x} _ {i} = \underbrace {[ \boldsymbol {q} _ {i} ^ {t} , \boldsymbol {q} _ {i} ^ {r} ,} _ {\text { configuration }} \underbrace {\boldsymbol {v} _ {i} ^ {t} , \boldsymbol {v} _ {i} ^ {r} ]} _ {\text { velocity }} \in \mathbb {R} ^ {2 n}.\tag{10}
$$

The translational components (with superscript t) describe the mobile base’s planar motion in the x-y plane, while the rotational components (with superscript r) correspond to the base orientation and manipulator joint angles. Let us further denote the first elements of the rotational joint angles and velocities, $q _ { i , 0 } ^ { r }$ and $v _ { i , 0 } ^ { r } ,$ as the base rotation angle and angular velocity, respectively. By collecting the state variables across all time steps into $\mathcal { X } = \{ \pmb { x } _ { 1 } , \pmb { x } _ { 2 } , \ldots , \pmb { x } _ { N } \}$ , the optimization problem takes the following form:

$$
\min _ {\mathcal {X} \in \mathbb {R} ^ {2 n N}} J _ {c} + J _ {t}\tag{11a}
$$

subject to

$$
\boldsymbol {q} _ {i + 1, y} ^ {t} = \boldsymbol {q} _ {i, y} ^ {t} + (v _ {i, x} ^ {t} \sin q _ {i, 0} ^ {r} + v _ {i, y} ^ {t} \cos q _ {i, 0} ^ {r}) d t,
$$

$$
\begin{array}{c} \boldsymbol {q} _ {i + 1} ^ {r} = \boldsymbol {q} _ {i} ^ {r} + \boldsymbol {v} _ {i} ^ {r} d t, \\ \forall i = 1, 2, \ldots , N - 1 \end{array}
$$

$$
\pmb {h} (\pmb {x} _ {i}) = \mathbf {0},\tag{11b}
$$

$$
\boldsymbol {g} (\boldsymbol {x} _ {i}) \geq \mathbf {0},
$$

$$
\forall i = 1, 2, \dots , N\tag{11c}
$$

$$
f _ {c} ^ {g} (\boldsymbol {p} _ {j}, \boldsymbol {q} _ {i}) - \delta \geq 0,
$$

$$
\forall i = 1, 2, \dots , N, \forall j = 1, 2, \dots , M\tag{11d}
$$

$$
\pmb {x} _ {0} = \pmb {x} _ {s}.\tag{11e}
$$

The objective function (11a) consists of two terms: $J _ { c }$ represents the control cost and $J _ { t }$ denotes the tracking error for desired states, both formulated as standard quadratic costs in our case. The velocity-controlled system is governed by the kinematic constraints (11b): The first two equations describe the translational motion of the mobile base, while the last one updates all rotational joints, including both the base orientation and manipulator joint angles. The general equality and inequality constraints are organized as h and g in (11c), where the comparisons are element-wise. Importantly, safety constraints are enforced through (11d), which generates $N { \times } M$ constraints ensuring that the GCDF value between the robot and each of the M obstacle points remains above a safety threshold δ throughout the N-step optimization horizon. The initial condition is specified by (11e).

Remark 3. In practice, the safety threshold δ must be chosen to balance neural approximation error and avoidance conservativeness. If δ is too small, it may not compensate for the approximation error of the neural implicit function, potentially violating collision avoidance. If δ is too large, the resulting behavior becomes overly conservative and may render the problem infeasible in narrow environments.

Algorithm. To solve the nonlinear programming problem (11), we adopt the sequential convex optimization algorithm, which iteratively approximates a local model (first-order constraint information and second-order objective information)

around the current iterate $\mathcal { X } _ { k }$ and solves a convex subproblem at each step. We chose this algorithm for the following reasons. First, as discussed in Section III, the trained neural GCDF directly exploits distance information in configuration space and explicitly maintains accurate gradient information that ensures the quality of local linearization. This accurate local model enables larger effective step sizes within the trust region or longer line search steps at each iteration, leading to faster convergence. Second, considering the large number of GCDF constraints between the robot and each obstacle point in (11), sequential convex optimization offers computational efficiency through well-established large-scale sparsity-aware QP subproblem solvers. This makes our approach particularly suitable for fast trajectory planning in obstacle-dense environments where the number of constraints can scale significantly.

Specifically, at the k-th iteration, we approximate a local model around the current iterate $\mathcal { X } _ { k }$ and solve the following $\ell _ { 1 }$ penalty with $\ell _ { \infty }$ trust region convex subproblem, following the formulation in CRISP [88]:

$$
\begin{array}{c} \min _ {p _ {k}, v, w, t} J _ {k} + \nabla J _ {k} ^ {\mathsf {T}} p _ {k} + \frac {1}{2} p _ {k} ^ {\mathsf {T}} \nabla_ {x x} ^ {2} J _ {k} p _ {k} \\ + \mu \sum_ {i \in \mathcal {E}} (v _ {i} + w _ {i}) + \mu \sum_ {i \in \mathcal {I}} t _ {i} \end{array}\tag{12a}
$$

$$
\text { subject   to } \nabla c _ {i} (x _ {k}) ^ {\mathsf {T}} p _ {k} + c _ {i} (x _ {k}) = v _ {i} - w _ {i}, i \in \mathcal {E}\tag{12b}
$$

$$
\nabla c _ {i} (x _ {k}) ^ {\mathsf {T}} p _ {k} + c _ {i} (x _ {k}) \geq - t _ {i}, i \in \mathcal {I}\tag{12c}
$$

$$
v, w, t \geq 0\tag{12d}
$$

$$
\| p _ {k} \| _ {\infty} \leq \Delta_ {k}.\tag{12e}
$$

Here, we denote the sum of $J _ { c }$ and $J _ { t }$ in (11) as $^ { J , }$ and stack all the equality and inequality constraints in c with the corresponding index sets E and I. $J _ { k } , \nabla J _ { k }$ , and $\nabla _ { x x } ^ { 2 } J _ { k }$ represent the objective function’s value, gradient, and Hessian at the current iterate $\mathcal { X } _ { k }$ , respectively. The nonnegative slack variables $v , w , t$ are introduced to penalize constraint violations. The constraints $c _ { i }$ are linearized around $\mathcal { X } _ { k }$ , and $p _ { k }$ is the current trial step subject to the trust region constraint in (12e) to find an optimal step within a local range. To obtain accurate GCDF queries aligned with our training distribution, we transform obstacle points into the robot’s local base frame at each time step. Specifically, we treat the robot base pose as the origin and bias all obstacle points p into this coordinate frame before querying the neural GCDF. This ensures queries remain within the coverage of our training data, providing reliable distance estimates and gradients for optimization.

Remark 4. Advanced solvers for such large-scale optimization problems have increasingly exploited problem-specific sparsity structures to improve computational efficiency. For instance, the chain-like sparsity in the system dynamics [89]. These solvers typically rely on one of two approaches: either using automatic differentiation tools (e.g., CppAD) to compute sparse Jacobians of explicitly defined functions [88], [90], [91], or requiring manual specification of sparsity patterns for constraint mapping [92]. However, our GCDF-based collision avoidance constraints are defined implicitly through neural networks, making direct application of these approaches challenging. Moreover, the sparsity pattern of GCDF constraints varies with different obstacle configurations and robot query point distributions, requiring a flexible representation that can be efficiently reconstructed online.

In this work, we choose CRISP [88] as our backbone solver for its computational efficiency with CppAD-based automatic differentiation, capability to generate informed trajectories from naive initial guesses, and trust-region framework that naturally leverages GCDF’s accurate gradient information. To integrate our implicit neural collision constraints with CRISP, we extend the solver with the following key modifications. First, we enable GPU-parallel querying of implicit function values and gradients during the solving process. The gradients from parallel GCDF queries form a dense matrix in <sup>RNM×n</sup>. Second, we design a compact representation for the structure of GCDF constraints that enables online reconstruction of constraint mappings and automatic derivation of their sparsity patterns. This representation captures the relationship between robot query points, obstacle points, and configuration variables, allowing efficient adaptation to varying obstacle configurations. Third, we implement efficient memory-level sparse mapping from the dense GCDF gradient matrix into the overall problem’s sparse Jacobian matrix. This process, combined with GPU-parallel querying, significantly improves computational efficiency.

Implementation. To enable cross-platform GPU querying of the trained neural network, we first convert the PyTorch GCDF model into a batch-queryable CasADi [93] function using the L4CasADi library [94], which automatically computes gradients through CasADi’s symbolic differentiation. We then generate C++ code from this CasADi function and compile it into a dynamic library. Leveraging CasADi’s cross-platform compatibility, our solver dynamically loads this library during the online phase, providing efficient inference functions for both GCDF values and gradients that can be seamlessly integrated into the optimization loop. The implementation of this pipeline involves numerous GPU-related and environmentspecific engineering challenges. Detailed instructions and source code are provided on our project website.

Remark 5. In obstacle-dense environments, the GCDF collision avoidance constraints constitute the largest component of the optimization problem (11). Beyond enabling the solver to efficiently obtain constraint values and Jacobians through GPU batch queries, it is crucial to exploit the sparsity structure of these constraints.

For the GCDF constraints in (11d), where each obstacle point is considered for all time steps, this would result in $N \times M$ constraints, which is a prohibitively large number. For mobile manipulation tasks, since the workspace is relatively larger due to base movements, it is clearly unnecessary to consider all possible collision pairs. We apply a straightforward approach to partition obstacle points based on the reference base positions, only considering obstacle points within a certain range of each reference base position. To this end, we design a straightforward data structure consisting of two components: one storing the spatial coordinates of all obstacle points, and another storing the indices of obstacle points to be considered at each time step. This structure enables efficient retrieval of the number of constraints and the sparsity pattern of the obstacle constraints. Moreover, both components can be modified online to accommodate changes in obstacle layouts, allowing for dynamic updates to the sparsity pattern and constraint count during online replanning. Let us now mathematically formulate this partitioning scheme.

![](Li2026Fast_figs/7cb76f5ffbb3aa60a8de6e23d659efca39551f82b228a97e489ec15adccc9b61.jpg)  
Fig. 5: Visualization of the Jacobian sparsity pattern induced by GCDF constraints, together with the dense-to-sparse mapping that assembles the full GCDF gradient vector queried from the implicit neural model into the sparse Jacobian.

Suppose the obstacle set $\mathbb { I } _ { M }$ contains M points. We divide it into N partitions, denoted by $\mathbb { I } _ { M , i }$ for $i \in { 1 , 2 , \dots N } ,$ representing potential collision points at each step. This gives us:

$$
\mathbb {I} _ {M} \subseteq \mathbb {I} _ {M, 1} \cup \mathbb {I} _ {M, 2} \cup \ldots \cup \mathbb {I} _ {M, N},\tag{13}
$$

where these sets typically have overlaps, with the ith set containing $m _ { i }$ points. Let us analyze all GCDF constraints and its Jacobian matrix in vectorized form. The GCDF constraints can be organized in $c _ { \mathrm { g c d f } }$ as :

$$
\boldsymbol {c} _ {\mathrm{gcdf}} = \left[ \begin{array}{c} f _ {c} ^ {g} (\boldsymbol {p} _ {1, 1}, \boldsymbol {q} _ {1}) \\ \vdots \\ f _ {c} ^ {g} (\boldsymbol {p} _ {1, m _ {1}}, \boldsymbol {q} _ {1}) \\ \vdots \\ f _ {c} ^ {g} (\boldsymbol {p} _ {i, 1}, \boldsymbol {q} _ {i}) \\ \vdots \\ f _ {c} ^ {g} (\boldsymbol {p} _ {i, m _ {i}}, \boldsymbol {q} _ {i}) \\ \vdots \\ f _ {c} ^ {g} (\boldsymbol {p} _ {N, 1}, \boldsymbol {q} _ {N}) \\ \vdots \\ f _ {c} ^ {g} (\boldsymbol {p} _ {N, m _ {N}}, \boldsymbol {q} _ {N}) \end{array} \right] = \left[ \begin{array}{c} \boldsymbol {c} _ {\boldsymbol {q} _ {1}} \\ \vdots \\ \boldsymbol {c} _ {\boldsymbol {q} _ {i}} \\ \vdots \\ \boldsymbol {c} _ {\boldsymbol {q} _ {N}} \end{array} \right] \in \mathbb {R} ^ {m _ {1} + m _ {2} + \dots + m _ {N}}.\tag{14}
$$

For simplicity, we omit the constant term $\delta .$ The constraints are indexed by time step, where obstacle points $p _ { i , 1 }$ to ${ p } _ { i , m _ { i } }$ belonging to $I _ { M , i }$ are considered for ${ \bf \Xi } _ { { \bf \Lambda } } \mathbf { \Lambda } _ { q _ { i } } ,$ with related constraints stacked in $c _ { q _ { i } }$ as shown in the second equality. While $c _ { \mathrm { g c d f } }$ is a dense vector that can be efficiently queried using batch operations, its Jacobian matrix exhibits high sparsity due to the partition. This sparsity pattern must be carefully exploited in the optimization process to ensure efficient solving of the problem (11).

Specifically, the Jacobian matrix $\nabla _ { \pmb q } ^ { \top } \pmb { c } _ { \mathrm { g c d f } }$ is sparse with dimension $( m _ { 1 } + m _ { 2 } + . . . + m _ { N } ) \times \dot { 2 } N n$ , and its sparsity pattern is visualized in Fig. 5. While the intermediate gradient matrix obtained directly from the implicit neural CDF, denoted as $\nabla _ { \pmb q } ^ { \top } \tilde { \pmb c } ,$ has dimension $( m _ { 1 } + m _ { 2 } + \ldots + m _ { N } ) \times n$ . We need to project values from $\nabla _ { \pmb q } ^ { \top }$ c˜ into their proper positions in the sparse matrix $\nabla _ { q } ^ { \top } c _ { \mathrm { g c d f } }$ . This process can be formalized as:

$$
\nabla_ {\boldsymbol {q}} ^ {\top} \tilde {\boldsymbol {c}} = \left[ \begin{array}{c} \nabla_ {\boldsymbol {q} _ {1}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {1}} \\ \vdots \\ \nabla_ {\boldsymbol {q} _ {i}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {i}} \\ \vdots \\ \nabla_ {\boldsymbol {q} _ {N}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {N}} \end{array} \right] \in \mathbb {R} ^ {(m _ {1} + m _ {2} + \ldots + m _ {N}) \times n},\tag{15}
$$

where

$$
\nabla_ {\boldsymbol {q} _ {i}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {i}} \in \mathbb {R} ^ {m _ {i} \times n}. \quad \forall i = 1, 2, \dots N\tag{16}
$$

We now show that this mapping can be treated as dense-sparse matrix multiplication, we construct a sequence of N sparse projection matrices $P = \{ P _ { 1 } , P _ { 2 } , . . . P _ { N } \}$ . The projection can be achieved through block operations:

$$
\nabla_ {\boldsymbol {q}} ^ {\top} \boldsymbol {c} = \left[ \begin{array}{c} \nabla_ {\boldsymbol {q} _ {1}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {1}} \boldsymbol {P} _ {1} \\ \vdots \\ \nabla_ {\boldsymbol {q} _ {i}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {i}} \boldsymbol {P} _ {i} \\ \vdots \\ \nabla_ {\boldsymbol {q} _ {N}} ^ {\top} \boldsymbol {c} _ {\boldsymbol {q} _ {N}} \boldsymbol {P} _ {N} \end{array} \right] \in \mathbb {R} ^ {(m _ {1} + m _ {2} + \ldots + m _ {N}) \times 2 N n},\tag{17}
$$

where the projection matrices $P _ { i } \in \mathbb { R } ^ { n \times 2 N n }$ are defined as:

$$
(\boldsymbol {P} _ {i}) _ {r, c} = \left\{ \begin{array}{l l} 1, & \text { if } r = c - 2 N n (i - 1) \\ 0, & \text { otherwise } \end{array} \right.\tag{18}
$$

As shown in Fig. 5, in essence, $P _ { i }$ is constructed by placing an identity matrix $I _ { n }$ at row 1, column $2 N n ( i - 1 ) + 1$ , effectively positioning the n elements of each row of $\nabla _ { \pmb q _ { i } } ^ { \top } \pmb c _ { \pmb q _ { i } }$ to their proper positions.

Remark 6. It is worth noting that the focus is on utilizing the sparsity pattern to develop high-performance tailored numerical methods, rather than specific implementation details. For instance, while MATLAB would benefit from the dense-sparse matrix multiplications shown in (17), our $C + +$ implementations use direct memory operations to position values correctly.

## V. EXPERIMENTS

In this section, we design experiments to comprehensively evaluate our framework from three complementary perspectives. First, we validate the theoretical properties of GCDF and the effectiveness of our training pipeline by assessing the learned neural GCDF. In particular, we examine whether the properties in Theorem 1 hold in practice and whether the neural GCDF provides sufficiently accurate values and gradients to support the single-step projection, which maps a configuration onto the queried obstacle point’s zero-level set using first-order information. Second, we benchmark our GCDF-constrained trajectory optimization algorithm against the state-of-the-art (SOTA) pipelines in multiple randomized maps to demonstrate efficiency, robustness, and solution quality in obstacle-dense environments. Third, we deploy the full system on a real mobile manipulator to verify practicality in real-world scenes.

![](Li2026Fast_figs/537e73e8868f9a15909b452fafd9e3a97b023ad879f4100dcb358da1b30d5f65.jpg)  
Fig. 6: Residual reduction comparison between our GCDFbased analytical projection and an iterative workspace SDF baseline. Targets are sampled within three x–y ranges (±4 m, ±5 m, ±6 m), and results aggregate 128 targets with 128 random arm initializations per target. Shaded regions indicate variability across trials.

![](Li2026Fast_figs/a16c597bfd532da27950566c97744fb8930ba7d01ce8fcedb913c1bfbb112151.jpg)  
Fig. 7: Visualization of the analytical single-step projection using the trained neural GCDF. The red dot denotes the queried target point. The initial configuration and the projected configuration after one step are overlaid for comparison. The result highlights the accuracy of the learned GCDF (values/gradients) and shows that the proposed projection moves directly in configuration space toward the target point’s nearest zero-level set.

![](Li2026Fast_figs/bdbf08758ad77a1ad8598ecd9e53ba4be816bd0f22224fdd22b9d3bd0d8e0c08.jpg)  
Fig. 8: Visualization of the goalkeeper example with online GCDF-based control. Each row shows a different shot with a distinct initial ball state; frames progress left-to-right in time. At each time step, the controller evaluates the value and gradient of the GCDF online and applies the corresponding projection to generate real-time, collision-aware motions that intercept the incoming ball.

## A. Simulation Experiments

1) Training Results: We begin by reporting the training settings and outcomes for GCDF. We set the loss weights to $\lambda _ { 1 } ~ = ~ 5 . 0 , ~ \lambda _ { 2 } ~ = ~ 0 . 1 , ~ \lambda _ { 3 } ~ = ~ 0 . 0 1$ , and $\lambda _ { 4 } ~ = ~ 0 . 0 1$ and optimize the network by minimizing $\mathcal { L } _ { \mathrm { t o t a l } }$ in (9) to achieve accurate GCDF approximation while enforcing the desired regularization. For each training iteration, we sample $b _ { 1 } ~ = ~ 2 0$ environment points from the grid and, for each point, draw $b _ { 2 } ~ = ~ 1 0 0$ configurations, resulting in a batch size of $2 0 \times 1 0 0$ . We train for 14,900 epochs using Adam with an initial learning rate of 0.005, decayed by a factor of 0.5. Training takes approximately 2 hours on four NVIDIA RTX 3090 GPUs. The final loss terms are $\mathcal { L } _ { \mathrm { d i s t } } ~ = ~ 0 . 2 7 4$ $\mathcal { L } _ { \mathrm { g r a d ~ } } = ~ 0 . 1 0 0 , ~ \mathcal { L } _ { \mathrm { e i k o n a l ~ } } = ~ 0 . 2 2 8$ , and $\mathcal { L } _ { \mathrm { t e n s i o n } } ~ = ~ 1 8 . 5 7 1$ Unless otherwise specified, we use this model throughout the following experiments. The training code and pretrained weights are available on the project website.

2) Properties of Neural GCDF: Next, we validate the Euclidean projection property and evaluate the accuracy of the value and gradient information provided by the learned implicit GCDF. Preserving this property with accurate firstorder information is a core theoretical pillar of our framework: it underpins the use of GCDF values and gradients to enforce collision avoidance and perform trajectory optimization directly in configuration space, thereby avoiding the intricate nonlinear mapping and kinematic coupling between workspace collision constraints and configuration space variables.

Concretely, we quantitatively evaluate this property by comparing the residual reduction achieved by our GCDFbased analytical projection against iterative algorithm using workspace SDF directly. Specifically, we randomly sample 128 target environment points within three x–y ranges (±4 m, $\pm 5 \mathrm { m }$ , and ±6 m) around the mobile base to cover varying proximity and difficulty. For each target point p, we initialize the robot from 128 different arm configurations q and apply the projection in Theorem 1 to obtain a projected configuration $\pmb q ^ { + }$ . We quantify convergence by measuring the residual ratio between the initial and projected states, computed using SDF values evaluated at the corresponding configurations. Since the projection is closed-form, its runtime is negligible. As a baseline, we implement standard gradient descent with Armijo line search to solve the unconstrained problem min ${ \bf \nabla } _ { q } f _ { s } ^ { 2 } ( q , p )$ and record the residual ratio after each iteration. The results are shown in Fig. 6. Our GCDF projection brings the robot to (or extremely close to) the target point’s zero-level set in a single step across all ranges, whereas the SDF-based method often requires multiple iterations. This gap is as expected: the SDF gradient must be back-propagated through nonlinear forward kinematics, so its induced updates in configuration space are strongly coupled and effective only locally, leading to slower contraction toward the contact manifold. Some results of our single-step projection are visualized in Fig. 7.

Additionally, we design a goalkeeper scenario as an intuitive demonstration of the practical utility of GCDF projection in real-time closed-loop control. In this example, a ball is launched toward the goal mouth from different initial states, and the mobile manipulator reacts online by querying GCDF values and gradients and using the resulting projection as a time-varying control target. The target is recomputed at every timestep, yielding smooth and continuous motions that drive the robot toward interception. As visualized in Fig. 8, the robot approaches the incoming ball and makes contact to block the shot, preventing a goal.

3) Benchmark Comparisons: In this part, we conduct a comprehensive benchmark study to demonstrate the effectiveness and superiority of the proposed trajectory optimization algorithm in complex environments.

Environment Settings. As illustrated in Fig. 9, we construct a 14 m × 14 m map and randomly populate it with a prescribed number of rectangular obstacles placed at varying heights. We remark that our setup is substantially more challenging than commonly used discrete pillar-forest environments: obstacles have diverse sizes and configurations, are allowed to overlap, and their vertical stacking naturally induces highly non-convex geometry across different height levels, which poses significant difficulty for coordinated base–arm motion. We consider three difficulty tiers by varying the obstacle count to 80, 100, and 120, respectively. The robot starts at the map center with the arm initialized to the zero configuration (upright). We randomly sample 50 collisionfree and kinematically feasible goal whole-body poses whose base locations are at least 3 m away from the center. For each difficulty tier, we generate 5 random maps, resulting in $5 0 \times 5 = 2 5 0$ planning trials per tier.

![](Li2026Fast_figs/bd3cfca6828e7c5a7d1d743615650a534ac77a5d7850cc5537289bf5f3e9c40b.jpg)  
Fig. 9: Environment setting for benchmark evaluation. We generate 50 random feasible start–goal configurations in each map. The robot arm is a 6-DoF Kinova Gen3.

Baselines. We remark that, under our benchmark setting, most existing methods fail to produce feasible solutions as the environments are deliberately dense and geometrically complex. We compare our method against four representative baselines. (1) RRT [95]: a direct sampling-based planner that searches in the full whole-body configuration space and performs collision checking using the environment ESDF. (2) LocalDecomp [33]: a SOTA free-space decomposition method that acts as a local reactive controller. At each step, it constructs link-wise safe regions from obstacle information and plans the next motion within these regions to maintain safety. For fairness, we assume the full map is known in advance and thus exclude perception-induced errors. (3) REMANI [10] and (4) TopAY [35]: SOTA two-stage pipelines that decouple base and arm planning in the front end, followed by trajectory optimization in the back end. REMANI plans the base using Hybrid A\* and then searches for a discrete arm trajectory along the base path via constrained RRT\*-Connect. TopAY first performs parallel topological search on the mobile base to generate multiple independent candidate base references, then refines each candidate by searching nearby arm motions using constrained Bi-RRT\*, selecting the best trajectory among candidates with parallel acceleration. Both methods employ penalty-based back-end optimization that augments constraints into the objective as soft penalties, requiring tuning of penalty weights for reliable convergence. For collision avoidance, they rely on the environment ESDF and approximate the robot using a set of collision spheres, minimizing the sum of ESDF values over spheres. This formulation is common in aerial robotics, where the robot can often be approximated as a point (or a single sphere), and it has the practical advantage that the collision-evaluation cost does not grow with obstacle density. Tuning the penalty weights across multiple terms can be challenging for these methods. We therefore adopt a unified strategy that prioritizes collision costs and reports the best performance achieved after careful parameter tuning. The collision spheres are also carefully fitted to closely approximate the robot’s link geometries to avoid conservative behaviors.

![](Li2026Fast_figs/65554dadd6046432e7f8efad92ec802cbd63e3b07447c35277ea15ff4395831b.jpg)

(a) Base Translation  
![](Li2026Fast_figs/7192395260fa8f58c8f45dcad0621f0e8e612b828685432cfe7bf7cc9482cda9.jpg)  
(b) Rotational Joints  
Fig. 10: Boxplots of configuration-space path-length ratios in randomized clutter benchmarks. Ratios are computed over successful trials as each baseline’s trajectory length normalized by ours (lower is better) under three obstacle densities (80/100/120): (a) base translation component and (b) rotational joint component.

Finally, since our goal is a robust and efficient back-end trajectory optimization algorithm that can produce meaningful

![](Li2026Fast_figs/373348f0c53c32fa5eafe67aac6d4e754bd1a661294467fd10b0ab0cb4012393.jpg)

![](Li2026Fast_figs/57ccef835b0b1f6f721ef389ad52a9e63803f243bc56fc1c4a69f847dc02850b.jpg)

![](Li2026Fast_figs/96c2fbc59de29c5c165bfd81a7014d7da4689b79942bfa6067daf1652124a9d8.jpg)

![](Li2026Fast_figs/cefa59ed265755ad4d3cd5b55d24ce90c6aa27069897cd3136addb7b837b7527.jpg)

![](Li2026Fast_figs/4940245afeab3f9c33cf219263c4796bc1e887858daaecac3ecb9d16bd6ecc68.jpg)

![](Li2026Fast_figs/f184e207b500b8d641ebd3621c701fccf7fa1c366e4061ea8d34183cffecacfa.jpg)

![](Li2026Fast_figs/8b673579d9e742a07a577de588c4d5a9d72547853ee5ac7b68fe1cb39319719e.jpg)

![](Li2026Fast_figs/f3c047e721be08b7552eba827319e6a9b3cfd17219b1084276ea689d6f645bc0.jpg)

![](Li2026Fast_figs/e6f1867b887f3ad1ad33ee7868992f15d38b2c13857aa753fd07efb730897dd2.jpg)

![](Li2026Fast_figs/351e9293bfc275f8d3e172c1164b4a86d71596610ada6d42ece40115efdf1819.jpg)

![](Li2026Fast_figs/5f13facd091d81a61add13a146ebd716d61cb4e900ea45f4fa0e5b66952ee599.jpg)

![](Li2026Fast_figs/4171390bf39646ce07f79dbf23ed21d967be5a0a92842417f27b45b26b92a7a4.jpg)  
Fig. 11: Visualization of representative trajectories generated by Ours in randomized maps. For each map, we overlay 24 planned motions (different goals) and plot the corresponding end-effector traces. Rows correspond to obstacle densities (80/100/120). The end-effector paths reveal agile whole-body behaviors enabled by configuration-space optimization, including coordinated base– arm reconfiguration and non-conservative twisting maneuvers that pass through narrow, highly non-convex regions. Additional visualizations from multiple viewpoints are available on the project website.

TABLE II: Benchmark results under different obstacle densities. We report success rate (SR), average runtime, and the average traversed trajectory length ratio w.r.t. our method (Ours = 1.00), separated into translational and rotational components.

<table><tr><td rowspan="2">Methods</td><td colspan="4">Number of Obstacles: 80</td><td colspan="4">Number of Obstacles: 100</td><td colspan="4">Number of Obstacles: 120</td></tr><tr><td>SR(%)</td><td>Time(s)</td><td>Ratio (↓)Trans</td><td>Rot</td><td>SR(%)</td><td>Time(s)</td><td>Ratio (↓)Trans</td><td>Rot</td><td>SR(%)</td><td>Time(s)</td><td>Ratio (↓)Trans</td><td>Rot</td></tr><tr><td>LocalDecomp</td><td>86.40</td><td>—</td><td>1.49</td><td>3.34</td><td>59.60</td><td>—</td><td>1.47</td><td>4.10</td><td>56.40</td><td>—</td><td>1.45</td><td>3.45</td></tr><tr><td>REMANI</td><td>86.80</td><td>0.2858</td><td>1.23</td><td>2.15</td><td>61.50</td><td>0.3077</td><td>1.24</td><td>2.21</td><td>49.60</td><td>0.3292</td><td>1.33</td><td>2.22</td></tr><tr><td>TopAY</td><td>88.40</td><td>0.1393</td><td>1.49</td><td>2.71</td><td>67.20</td><td>0.1776</td><td>1.51</td><td>2.72</td><td>51.60</td><td>0.2727</td><td>1.47</td><td>2.78</td></tr><tr><td>Ours</td><td>92.40</td><td>0.1732</td><td>1.00</td><td>1.00</td><td>88.40</td><td>0.2446</td><td>1.00</td><td>1.00</td><td>86.80</td><td>0.2871</td><td>1.00</td><td>1.00</td></tr><tr><td>Ours (TopAY-init)</td><td>98.00</td><td>0.1341</td><td>1.25</td><td>1.81</td><td>92.50</td><td>0.1641</td><td>1.28</td><td>1.92</td><td>91.60</td><td>0.1957</td><td>1.32</td><td>1.98</td></tr></table>

<sup>\*</sup> — denotes that the runtime is not directly comparable because the method is a single-step local controller.  
<sup>\*</sup> Dark Green highlights the best results while Orange indicates the second-best. We report the runtime for all trials, while the Ratio is computed only over successful trajectories.  
<sup>\*</sup> Ours (TopAY-init) initializes our solver with the discrete front-end paths produced by TopAY; if the front-end search fails, we fall back to the original baseline initialization, i.e., linear interpolation for the mobile base and an all-zero arm configuration.

![](Li2026Fast_figs/0bdd3b52c821e787e9adae497ceede11add0d11857b32b1c4a784a54adca1393.jpg)  
Fig. 12: Real-world deployment of our planner. Top: in a laboratory obstacle course composed of stacked and overlapping blocks with limited clearance, the robot performs agile base–arm reconfiguration while traversing tight passages $( t _ { 1 } - t _ { 8 } )$ . Bottom: in an office environment, the robot follows a multi-goal route (with an intermediate waypoint) through narrow corridors and furniture-dense areas $\left( t _ { 1 } { - } t _ { 1 2 } \right)$ . Orange arrows show the direction of motion.

whole-body trajectories from trivial initial guesses within a limited number of iterations, we evaluate two variants. Ours uses a naive initialization: linear interpolation for the base between start and goal, with the arm fixed at the all-zero (upright) posture. Ours (TopAY-init) augments our GCDF-based solver with the first feasible front-end solution returned by TopAY as initialization, isolating and highlighting the strength of our numerical back end under strong initial guesses.

Main Results. We evaluate each method by its success rate (with failure cases including collision, optimization failure, and stagnation) and computation time. To quantify trajectory conservativeness and smoothness, we report the configurationspace path-length ratio over successful trials, defined as each baseline’s trajectory length normalized by that of our method. Representative trajectories produced by our approach are visualized in Fig. 11. Quantitative results are summarized in Table II, and the distribution of trajectory length ratios is further shown in Fig. 10.

RRT consistently failed to find a feasible solution within the allocated time, likely due to the high density of our experimental setup. We therefore omit RRT from Table II. The remaining results show that our method efficiently handles large-scale collision constraints across all difficulty levels and consistently achieves the highest success rates. In particular, Ours (TopAY-init) achieves the best robustness with the shortest runtime, underscoring a key practical insight: once the per-iteration cost (constraint evaluation, batching, and QP subproblem construction and solution) is optimized, the endto-end runtime of an iterative solver is largely determined by the number of iterations required to reach a high-quality feasible solution. This iteration count is influenced not only by initialization quality, but also by the choice of collision constraints: well-posed constraints with informative local firstorder geometry can dramatically accelerate convergence. In our case, GCDF enforces collision avoidance directly in configuration space and provides accurate local gradients, yielding more reliable descent directions and faster contraction toward feasibility. A stronger initialization, therefore, further reduces the iteration count and amplifies the benefit of a robust backend optimizer, while the solver’s refinement capability remains essential for improving trajectory quality.

For two-stage methods such as REMANI and TopAY, the hierarchical front-end search is typically fast when it succeeds; however, as obstacle density increases and the environment becomes more geometrically complex, front-end failures become frequent. In such cases, reverting to a naive initialization often causes the ESDF-sphere, penalty-based back end to stuck or converge to infeasible, collision-prone trajectories. TopAY’s parallel candidate strategy partially mitigates this issue by increasing the chance of finding a feasible front-end solution, but it also tends to select more conservative base routes with longer detours in dense clutter.

LocalDecomp exhibits a different failure mode due to its local, reactive nature. Because it reasons only about obstacles in a limited neighborhood, its performance is less sensitive to obstacle count than to global layout complexity; it is particularly prone to getting stuck or colliding in “bridge-like” structures and stacked non-convex geometries. Moreover, since it prioritizes local traversability rather than global path quality, it often induces large and unnecessary base and arm rotations.

In contrast, Ours and Ours (TopAY-init) optimize directly in configuration space with implicit GCDF constraints, consistently producing non-conservative whole-body motions in dense 3D clutter. In particular, the naive-initialization variant keeps the base close to a straight-line route and relies on coordinated arm reconfiguration to negotiate tight clearances, resulting in the shortest traversal distance with smooth configuration-space evolution. Fig. 11 further illustrates these safe and agile behaviors, showing coordinated base–arm maneuvers that maintain clearance without excessive detours. Overall, these results validate the effectiveness of our learned implicit GCDF and training pipeline, together with our customized high-performance numerical algorithm, and highlight the benefit of enforcing collision avoidance directly in configuration space for robust and efficient whole-body trajectory optimization.

## B. Real-World Validation

We further validate the proposed framework on a real mobile manipulator in two representative settings: (i) a laboratory obstacle course with manually arranged clutter consisting of stacked blocks of diverse shapes and heights, and (ii) an office environment that requires navigation through narrow passages while sequentially reaching multiple intermediate goals. Fig. 12 visualizes execution with snapshots along the planned trajectories. These deployments are intentionally challenging for whole-body mobile manipulation: the scenes exhibit tight 3D clearances across multiple height layers and non-convex, overlapping geometry (e.g., stacked blocks and bridge-like structures). In the laboratory course (top, $t _ { 1 } \mathrm { - } t _ { 8 } )$ , the robot navigates through densely placed obstacles with limited clearance. It exhibits non-conservative whole-body reconfiguration: the base commits to narrow passages. At the same time, the arm continuously adjusts its posture to maintain clearance against obstacles at different heights, thereby avoiding excessive detours. In the office scenario (bottom, $t _ { 1 } { - } t _ { 1 2 } )$ , the robot plans and executes a multi-goal route through confined corridors and furniture-dense areas (including an intermediate waypoint), producing smooth collision-free motions without oscillatory corrections or large unnecessary rotations. Across both settings, the executed trajectories maintain consistent clearance in tight spaces, indicating that the learned neural GCDF provides sufficiently accurate local geometry and firstorder information to support reliable configuration-space optimization on hardware. Overall, these real-world trials validate the practicality of our approach and its ability to generate safe, agile, and dynamic feasible whole-body motions.

## VI. CONCLUSION

We presented a configuration-space collision reasoning and trajectory optimization framework for whole-body mobile manipulation in dense, cluttered, and unbounded environments. We introduced GCDF as a generalization of CDF that can go beyond purely rotational manipulators and consider mobile manipulators with both translational and rotational joints. We developed a one-time offline data collection and training pipeline to learn an implicit neural GCDF with accurate values and first-order information. Building on this representation, we proposed a high-performance C++ sequential convex optimization algorithm that natively supports neural implicit constraints through batched GPU queries, sparsity-aware activeconstraint selection, and online constraint injection. Extensive randomized clutter benchmarks and real-world experiments demonstrate robust, efficient, and non-conservative wholebody motion generation, highlighting the benefit of enforcing collision avoidance directly in configuration space.

Future directions. First, in the training stage, we did not exhaustively explore how network architecture choices and hyperparameters (e.g., loss-term weights) affect the fidelity of the learned implicit GCDF. In this work, we used a standard MLP; however, more expressive architectures may better fit larger and higher-resolution datasets, yielding more accurate values and gradients and further improving downstream optimization performance. Moreover, the relative weighting between translational and rotational components in the GCDF metric can significantly influence optimization behavior. While we empirically selected a strong setting, an interesting direction is to treat these weights as conditioning inputs to the network, allowing a single model to realize different trade-offs without retraining.

Second, despite substantial efficiency optimizations, the overall computation can still be dominated by the scale of collision constraints, since obstacle geometries are represented by many sampled points. This creates a trade-off between geometric fidelity and constraint complexity: faithfully representing curved or complex obstacles may require dense sampling, whereas sparse sampling can lead to undesired solutions (e.g., the arm threading through gaps between samples). A natural extension is to move beyond point-based constraints by learning GCDF over parametric primitives. For example, by representing obstacles as spheres (or other primitives) with radius r and defining a GCDF that takes $( \boldsymbol { q } , \boldsymbol { p } , \boldsymbol { r } )$ as inputs. Such primitive-aware constraints could significantly reduce the number of constraints, improve geometric coverage, and mitigate failure modes caused by undersampling, while retaining the benefits of configuration-space collision reasoning.

## ACKNOWLEDGMENTS

We thank Long Xu, Zailin Huang, and Chengkai Wu for insightful discussions on experimental settings for mobile manipulators.

## REFERENCES

[1] V. Helm, S. Ercan, F. Gramazio, and M. Kohler, “Mobile robotic fabrication on construction sites: Dimrob,” in 2012 IEEE International Conference on Intelligent Robots and Systems (IROS), 2012, pp. 4335– 4341.

[2] V. Pilania and K. Gupta, “Mobile manipulator planning under uncertainty in unknown environments,” The International Journal of Robotics Research, vol. 37, no. 2-3, pp. 316–339, 2018.

[3] M. Tzes, V. Vasilopoulos, Y. Kantaros, and G. J. Pappas, “Reactive informative planning for mobile manipulation tasks under sensing and environmental uncertainty,” in 2022 International Conference on Robotics and Automation (ICRA), 2022, pp. 7320–7326.

[4] J. Michaux, P. Holmes, B. Zhang, C. Chen, B. Wang, S. Sahgal, T. Zhang, S. Dey, S. Kousik, and R. Vasudevan, “Can not touch this: Real-time, safe motion planning and control for manipulators under uncertainty,” IEEE Transactions on Robotics, vol. 41, pp. 4719–4740, 2025.

[5] T. A. Howell, S. Le Cleac’h, S. Singh, P. Florence, Z. Manchester, and V. Sindhwani, “Trajectory optimization with optimization-based dynamics,” IEEE Robotics and Automation Letters, vol. 7, no. 3, pp. 6750–6757, 2022.

[6] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “CHOMP: Gradient optimization techniques for efficient motion planning,” in 2009 IEEE International Conference on Robotics and Automation (ICRA), 2009, pp. 489–494.

[7] M. Kalakrishnan, S. Chitta, E. Theodorou, P. Pastor, and S. Schaal, “STOMP: Stochastic trajectory optimization for motion planning,” in 2011 IEEE International Conference on Robotics and Automation (ICRA), 2011, pp. 4569–4574.

[8] Y. Pi, X. Liu, Z. Yang, Y. Zhong, T. Huang, H. Pu, and J. Luo, “OMEPP: Online multi-population evolutionary path planning for mobile manipulators in dynamic environments,” IEEE Transactions on Automation Science and Engineering, vol. 22, pp. 6234–6245, 2025.

[9] J. Pankert and M. Hutter, “Perceptive model predictive control for continuous mobile manipulation,” IEEE Robotics and Automation Letters, vol. 5, no. 4, pp. 6177–6184, 2020.

[10] C. Wu, R. Wang, M. Song, F. Gao, J. Mei, and B. Zhou, “Realtime whole-body motion planning for mobile manipulators using environment-adaptive search and spatial-temporal optimization,” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 1369–1375.

[11] S. Chitta, E. G. Jones, M. Ciocarlie, and K. Hsiao, “Mobile manipulation in unstructured environments: Perception, planning, and execution,” IEEE Robotics & Automation Magazine, vol. 19, no. 2, pp. 58–71, 2012.

[12] P. D. Lillo, D. D. Vito, and G. Antonelli, “Merging global and local planners: Real-time replanning algorithm of redundant robots within a task-priority framework,” IEEE Transactions on Automation Science and Engineering, vol. 20, no. 2, pp. 1180–1193, 2023.

[13] M. Giftthaler, F. Farshidian, T. Sandy, L. Stadelmann, and J. Buchli, “Efficient kinematic planning for mobile manipulators with non-holonomic constraints using optimal control,” in 2017 IEEE International Conference on Robotics and Automation (ICRA), 2017, pp. 3411–3417.

[14] A. Gawel, H. Blum, J. Pankert, K. Krämer, L. Bartolomei, S. Ercan, F. Farshidian, M. Chli, F. Gramazio, R. Siegwart, M. Hutter, and T. Sandy, “A fully-integrated sensing and control system for highaccuracy mobile robotic building construction,” in 2019 IEEE International Conference on Intelligent Robots and Systems (IROS), 2019, pp. 2300–2307.

[15] G. Oriolo and C. Mongillo, “Motion planning for mobile manipulators along given end-effector paths,” in Proceedings of the 2005 IEEE International Conference on Robotics and Automation (ICRA), 2005, pp. 2154–2160.

[16] D. Berenson, J. Kuffner, and H. Choset, “An optimization approach to planning for mobile manipulation,” in 2008 IEEE International Conference on Robotics and Automation (ICRA), 2008, pp. 1187–1192.

[17] Y. Yang, F. Meng, Z. Meng, and C. Yang, “RAMPAGE: Toward whole-body, real-time, and agile motion planning in unknown cluttered environments for mobile manipulators,” IEEE Transactions on Industrial Electronics, vol. 71, no. 11, pp. 14 492–14 502, 2024.

[18] F. Xia, C. Li, R. Martín-Martín, O. Litany, A. Toshev, and S. Savarese, “ReLMoGen: Leveraging motion generation in reinforcement learning for mobile manipulation,” arXiv:2008.07792, 2021.

[19] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” 1996 IEEE Transactions on Robotics and Automation (ICRA), vol. 12, no. 4, pp. 566–580, 1996.

[20] S. LaValle, “Rapidly-exploring random trees: A new tool for path planning,” Research Report 9811, 1998.

[21] M. Otte and E. Frazzoli, “RRTX: Asymptotically optimal single-query sampling-based motion planning with quick replanning,” The International Journal of Robotics Research, vol. 35, no. 7, pp. 797–822, 2016.

[22] A. Orthey, C. Chamzas, and L. E. Kavraki, “Sampling-based motion planning: A comparative review,” Annual Review of Control, Robotics, and Autonomous Systems, vol. 7, 2023.

[23] G. Rizzi, J. J. Chung, A. Gawel, L. Ott, M. Tognon, and R. Siegwart, “Robust sampling-based control of mobile manipulators for interaction with articulated objects,” IEEE Transactions on Robotics, vol. 39, no. 3, pp. 1929–1946, 2023.

[24] S. Thakar, P. Rajendran, H. Kim, A. M. Kabir, and S. K. Gupta, “Accelerating bi-directional sampling-based search for motion planning of non-holonomic mobile manipulators,” in 2020 IEEE International Conference on Intelligent Robots and Systems (IROS), 2020, pp. 6711– 6717.

[25] R. Yang, Y. Kim, R. Hendrix, A. Kembhavi, X. Wang, and K. Ehsani, “Harmonic mobile manipulation,” in 2024 IEEE International Conference on Intelligent Robots and Systems (IROS), 2024, pp. 3658–3665.

[26] J. Hu, P. Stone, and R. Martín-Martín, “Causal Policy Gradient for Whole-Body Mobile Manipulation,” in Proceedings of Robotics: Science and Systems (RSS), 2023.

[27] Y. Zhou, Q. Feng, Y. Zhou, J. Lin, Z. Liu, and H. Wang, “Sampleefficient deep reinforcement learning of mobile manipulation for 6-dof trajectory following,” IEEE Transactions on Automation Science and Engineering, vol. 22, pp. 11 381–11 391, 2025.

[28] J. Kindle, F. Furrer, T. Novkovic, J. J. Chung, R. Siegwart, and J. Nieto, “Whole-body control of a mobile manipulator using end-toend reinforcement learning,” arXiv:2003.02637, 2020.

[29] D. Honerkamp, T. Welschehold, and A. Valada, “N<sup>2</sup>M<sup>2</sup>: Learning navigation for arbitrary mobile manipulation motions in unseen and dynamic environments,” IEEE Transactions on Robotics, vol. 39, no. 5, pp. 3601–3619, 2023.

[30] Z. Bi, K. Chen, C. Zheng, Y. Li, H. Li, and J. Ma, “Interactive navigation for legged manipulators with learned arm-pushing controller,” in 2025 IEEE International Conference on Intelligent Robots and Systems (IROS), 2025, pp. 9–16.

[31] S. Xie, C. Hu, D. Wang, J. Johnson, M. Bagavathiannan, and D. Song, “Coupled active perception and manipulation planning for a mobile manipulator in precision agriculture applications,” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 12 665–12 671.

[32] K. Dong, K. Pereida, F. Shkurti, and A. P. Schoellig, “Catch the Ball: Accurate high-speed motions for mobile manipulators via inverse dynamics learning,” in 2020 IEEE International Conference on Intelligent Robots and Systems (IROS), 2020, pp. 6718–6725.

[33] C. Zheng, Y. Li, Z. Song, Z. Bi, J. Zhou, B. Zhou, and J. Ma, “Local reactive control for mobile manipulators with whole-body safety in complex environments,” IEEE Robotics and Automation Letters, vol. 10, no. 5, pp. 4556–4563, 2025.

[34] Y. Pan, Y. Kompis, L. Bartolomei, R. Mascaro, C. Stachniss, and M. Chli, “Voxfield: Non-projective signed distance fields for online planning and 3D reconstruction,” in 2022 IEEE International Conference on Intelligent Robots and Systems (IROS), 2022, pp. 5331–5338.

[35] L. Xu, C. Wong, M. Zhang, J. Lin, J. Hou, and F. Gao, “TopAY: Efficient trajectory planning for differential drive mobile manipulators via topological paths search and arc length-yaw parameterization,” arXiv:2507.02761, 2025.

[36] Y. Li, C. Zheng, K. Chen, Y. Xie, X. Tang, M. Y. Wang, and J. Ma, “Collision-free trajectory optimization in cluttered environments using sums-of-squares programming,” IEEE Robotics and Automation Letters, vol. 9, no. 12, pp. 11 026–11 033, 2024.

[37] K. Tracy, T. A. Howell, and Z. Manchester, “Differentiable collision detection for a set of convex primitives,” in 2023 IEEE International Conference on Robotics and Automation (ICRA), 2023, pp. 3663–3670.

[38] M. Spahn, B. Brito, and J. Alonso-Mora, “Coupled mobile manipulation via trajectory optimization with free space decomposition,” in 2021 IEEE International Conference on Robotics and Automation (ICRA), 2021, pp. 12 759–12 765.

[39] S. Zhao, X. Zhou, J. Mao, and C. Zhang, “MPC-DCBF based motion planning of mobile manipulator in dynamic environment,” in 2025 10th International Conference on Automation, Control and Robotics Engineering (CACRE), 2025, pp. 41–45.

[40] M. Koptev, N. Figueroa, and A. Billard, “Neural joint space implicit signed distance functions for reactive robot manipulator control,” IEEE Robotics and Automation Letters, vol. 8, no. 2, pp. 480–487, 2023.

[41] P. Liu, K. Zhang, D. Tateo, S. Jauhri, J. Peters, and G. Chalvatzaki, “Regularized deep signed distance fields for reactive motion generation,” in 2022 IEEE International Conference on Intelligent Robots and Systems (IROS), 2022, pp. 6673–6680.

[42] Y. Li, Y. Zhang, A. Razmjoo, and S. Calinon, “Representing robot geometry as distance fields: Applications to whole-body manipulation,” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 15 351–15 357.

[43] Y. Li, X. Chi, A. Razmjoo, and S. Calinon, “Configuration space distance fields for manipulation planning.” in Robotics: Science and Systems (RSS), 2024.

[44] A. Jordana, S. Kleff, A. Meduri, J. Carpentier, N. Mansard, and L. Righetti, “Structure-exploiting sequential quadratic programming for model-predictive control,” IEEE Transactions on Robotics, vol. 41, pp. 4960–4974, 2025.

[45] P. E. Gill and E. Wong, “Sequential quadratic programming methods,” in Mixed Integer Nonlinear Programming. New York, NY, USA: Springer, 2012, pp. 147–224.

[46] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, S. Patil, K. Goldberg, and P. Abbeel, “Motion planning with sequential convex optimization and convex collision checking,” The International Journal of Robotics Research, vol. 33, no. 9, pp. 1251–1270, 2014.

[47] J.-C. Latombe, Robot Motion Planning. New York, NY, USA: Springer, 2012.

[48] J. T. Schwartz and M. Sharir, “On the "Piano Movers" problem. ii. general techniques for computing topological properties of real algebraic manifolds,” Advances in Applied Mathematics, vol. 4, no. 3, pp. 298– 351, 1983.

[49] T. Asano, T. Asano, L. Guibas, J. Hershberger, and H. Imai, “Visibilitypolygon search and Euclidean shortest paths,” in 26th Annual Symposium on Foundations of Computer Science (SFCS), 1985, pp. 155–164.

[50] T. Lozano-Pérez and M. A. Wesley, “An algorithm for planning collisionfree paths among polyhedral obstacles,” Communications of the ACM, vol. 22, no. 10, pp. 560–570, 1979.

[51] P. Bhattacharya and M. L. Gavrilova, “Roadmap-based path planning - using the voronoi diagram for a clearance-based shortest path,” IEEE Robotics & Automation Magazine, vol. 15, no. 2, pp. 58–66, 2008.

[52] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” IEEE Transactions on Robotics and Automation, vol. 12, no. 4, pp. 566–580, 1996.

[53] S. M. LaValle et al., “Rapidly-exploring random trees: A new tool for path planning,” 1998.

[54] I. A. Sucan, M. Moll, and L. E. Kavraki, “The open motion planning library,” IEEE Robotics & Automation Magazine, vol. 19, no. 4, pp. 72–82, 2012.

[55] D. Coleman, I. Sucan, S. Chitta, and N. Correll, “Reducing the barrier to entry of complex robotic software: a MoveIt! case study,” arXiv:1404.3785, 2014.

[56] D. Berenson, S. S. Srinivasa, D. Ferguson, and J. J. Kuffner, “Manipulation planning on constraint manifolds,” in 2009 IEEE International Conference on Robotics and Automation (ICRA), 2009, pp. 625–632.

[57] R. Deits and R. Tedrake, “Computing large convex regions of obstaclefree space through semidefinite programming,” in Algorithmic Foundations of Robotics XI: Selected Contributions of the Eleventh International Workshop on the Algorithmic Foundations of Robotics (WAFR). Springer, 2015, pp. 109–124.

[58] Q. Wang, Z. Wang, M. Wang, J. Ji, Z. Han, T. Wu, R. Jin, Y. Gao, C. Xu, and F. Gao, “Fast iterative region inflation for computing large 2-D/3-D convex regions of obstacle-free space,” IEEE Transactions on Robotics, 2025.

[59] S. Liu, M. Watterson, K. Mohta, K. Sun, S. Bhattacharya, C. J. Taylor, and V. Kumar, “Planning dynamically feasible trajectories for quadrotors using safe flight corridors in 3D complex environments,” IEEE Robotics and Automation Letters, vol. 2, no. 3, pp. 1688–1695, 2017.

[60] C. Toumieh and A. Lambert, “Voxel-grid based convex decomposition of 3D space for safe corridor generation,” Journal of Intelligent & Robotic Systems, vol. 105, no. 4, p. 87, 2022.

[61] J. Arrizabalaga, Z. Manchester, and M. Ryll, “Differentiable collisionfree parametric corridors,” in 2024 IEEE International Conference on Intelligent Robots and Systems (IROS), 2024, pp. 1839–1846.

[62] V. Kurtz and H. Lin, “Temporal logic motion planning with convex optimization via graphs of convex sets,” IEEE Transactions on Robotics, vol. 39, no. 5, pp. 3791–3804, 2023.

[63] Y. Suh, J. Kang, and D. Lee, “A fast and safe motion planning algorithm in cluttered environment using maximally occupying convex space,” in 2020 20th International Conference on Control, Automation and Systems (ICCAS), 2020, pp. 173–178.

[64] J. Tordesillas, B. T. Lopez, M. Everett, and J. P. How, “FASTER: Fast and safe trajectory planner for navigation in unknown environments,” IEEE Transactions on Robotics, vol. 38, no. 2, pp. 922–938, 2021.

[65] H. Dai, A. Amice, P. Werner, A. Zhang, and R. Tedrake, “Certified polyhedral decompositions of collision-free configuration space,” The International Journal of Robotics Research, vol. 43, no. 9, pp. 1322– 1341, 2024.

[66] T. Oelerich, C. Hartl-Nesic, F. Beck, and A. Kugi, “Boundplanner: A convex-set-based approach to bounded manipulator trajectory planning,” IEEE Robotics and Automation Letters, vol. 10, no. 6, pp. 5393–5400, 2025.

[67] R. Deits and R. Tedrake, “Efficient mixed-integer planning for uavs in cluttered environments,” in 2015 IEEE International Conference on Robotics and Automation (ICRA), 2015, pp. 42–49.

[68] D. Mellinger and V. Kumar, “Minimum snap trajectory generation and control for quadrotors,” in 2011 IEEE International Conference on Robotics and Automation (ICRA), 2011, pp. 2520–2525.

[69] J. Ma, Z. Cheng, X. Zhang, M. Tomizuka, and T. H. Lee, “Alternating direction method of multipliers for constrained iterative LQR in autonomous driving,” IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 12, pp. 23 031–23 042, 2022.

[70] A. Thirugnanam, J. Zeng, and K. Sreenath, “Safety-critical control and planning for obstacle avoidance between polytopes with control barrier functions,” in 2022 IEEE International Conference on Robotics and Automation (ICRA), 2022, pp. 286–292.

[71] J. Tordesillas and J. P. How, “MADER: Trajectory planner in multiagent and dynamic environments,” IEEE Transactions on Robotics, vol. 38, no. 1, pp. 463–476, 2022.

[72] S. H. Nair, E. H. Tseng, and F. Borrelli, “Collision avoidance for dynamic obstacles with uncertain predictions using model predictive control,” in 2022 IEEE 61st Conference on Decision and Control (CDC), 2022, pp. 5267–5272.

[73] A. Maric, Y. Li, and S. Calinon, “Online learning of continuous´ signed distance fields using piecewise polynomials,” IEEE Robotics and Automation Letters, vol. 9, no. 6, pp. 6020–6026, 2024.

[74] J. J. Park, P. Florence, J. Straub, R. Newcombe, and S. Lovegrove, “DeepSDF: Learning continuous signed distance functions for shape representation,” in 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 165–174.

[75] H. Oleynikova, Z. Taylor, M. Fehr, R. Siegwart, and J. Nieto, “Voxblox: Incremental 3D Euclidean signed distance fields for on-board mav planning,” in 2017 IEEE International Conference on Intelligent Robots and Systems (IROS), 2017, pp. 1366–1373.

[76] X. Zhong, Y. Pan, J. Behley, and C. Stachniss, “SHINE-mapping: Large-scale 3D mapping using sparse hierarchical implicit neural representations,” in 2023 IEEE International Conference on Robotics and Automation (ICRA), 2023, pp. 8371–8377.

[77] J. Ortiz, A. Clegg, J. Dong, E. Sucar, D. Novotny, M. Zollhoefer, and M. Mukadam, “iSDF: Real-time neural signed distance fields for robot perception,” in Robotics: Science and Systems (RSS), 2022.

[78] M. Bhardwaj, B. Sundaralingam, A. Mousavian, N. D. Ratliff, D. Fox, F. Ramos, and B. Boots, “STORM: An integrated framework for fast joint-space model-predictive control for reactive manipulation,” in Conference on Robot Learning (CoRL), 2022, pp. 750–759.

[79] V. Vasilopoulos, S. Garg, J. Huh, B. Lee, and V. Isler, “HIO-SDF: Hierarchical incremental online signed distance fields,” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 17 537–17 543.

[80] M. Koptev, N. Figueroa, and A. Billard, “Reactive collision-free motion generation in joint space via dynamical systems and sampling-based MPC,” The International Journal of Robotics Research, vol. 43, no. 13, pp. 2049–2069, 2024.

[81] B. Liu, G. Jiang, F. Zhao, and X. Mei, “Collision-free motion generation based on stochastic optimization and composite signed distance field networks of articulated robot,” IEEE Robotics and Automation Letters, vol. 8, no. 11, pp. 7082–7089, 2023.

[82] X. Zhu, Y. Xin, S. Li, H. Liu, C. Xia, and B. Liang, “Efficient collision detection framework for enhancing collision-free robot motion,” in 2025 IEEE International Conference on Robotics and Automation (ICRA), 2025, pp. 16 162–16 168.

[83] Y. Chen, X. Gao, K. Yao, L. Niederhauser, Y. Bekiroglu, and A. Billard, “Implicit articulated robot morphology modeling with configuration space neural signed distance functions,” in 2025 IEEE International Conference on Robotics and Automation (ICRA), 2025, pp. 4558–4564.

[84] K. Long, K. M. B. Lee, N. Raicevic, N. Attasseri, M. Leok, and N. Atanasov, “Neural configuration-space barriers for manipulation planning and control,” arXiv:2503.04929, 2025.

[85] X. Chi, Y. Li, J. Huang, B. Dai, Z. Liu, and S. Calinon, “Safe dynamic motion generation in configuration space using differentiable distance fields,” arXiv:2412.16456, 2024.

[86] Y. Li, T. Miyazaki, and K. Kawashima, “One-step model predictive path integral for manipulator motion planning using configuration space distance fields,” arXiv:2509.00836, 2025.

[87] J. Nocedal and S. J. Wright, Numerical Optimization. New York: Springer, 1999.

[88] Y. Li, H. Han, S. Kang, J. Ma, and H. Yang, “On the surprising robustness of sequential convex optimization for contact-implicit motion planning,” in Robotics: Science and Systems (RSS), 2025.

[89] S. Kang, X. Xu, J. Sarva, L. Liang, and H. Yang, “Fast and certifiable trajectory optimization,” in International Workshop on the Algorithmic Foundations of Robotics (WAFR), 2024.

[90] F. Farshidian et al., “OCS2: An open source library for optimal control of switched systems,” [Online]. Available: https://github.com/ leggedrobotics/ocs2.

[91] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The Pinocchio C++ library – a fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in IEEE International Symposium on System Integrations (SII), 2019.

[92] R. Tedrake and the Drake Development Team, “Drake: Model-based design and verification for robotics,” 2019. [Online]. Available: https://drake.mit.edu

[93] J. A. Andersson, J. Gillis, G. Horn, J. B. Rawlings, and M. Diehl, “CasADi: a software framework for nonlinear optimization and optimal control,” Mathematical Programming Computation, vol. 11, pp. 1–36, 2019.

[94] T. Salzmann, J. Arrizabalaga, J. Andersson, M. Pavone, and M. Ryll, “Learning for CasADi: Data-driven models in numerical optimization,” in Learning for Dynamics and Control Conference (L4DC), 2024.

[95] I. A. ¸Sucan, M. Moll, and L. E. Kavraki, “The Open Motion Planning Library,” IEEE Robotics & Automation Magazine, vol. 19, no. 4, pp. 72–82, December 2012, https://ompl.kavrakilab.org.

[96] J. R. Shewchuk, “An introduction to the conjugate gradient method without the agonizing pain,” Carnegie Mellon University, Pittsburgh, PA, USA, Technical Report CMU-CS-94-125, Aug. 1994.

## APPENDIX A PROOF OF THEOREM 1

Proof.

1) Starting from Definition 1, let $\pmb { q } _ { z }$ be the closest configuration of q on $\mathcal Z ( p )$ , we have

$$
f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}) = \sqrt {\left(\boldsymbol {q} - \boldsymbol {q} _ {z}\right) ^ {\top} M \left(\boldsymbol {q} - \boldsymbol {q} _ {z}\right)},
$$

and its partial derivative with respect to $\mathbf { \nabla } q \mathbf { \cdot }$

$$
\nabla_ {\boldsymbol {q}} f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}) = \frac {\boldsymbol {M} (\boldsymbol {q} - \boldsymbol {q} _ {z})}{\sqrt {(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {\top} \boldsymbol {M} (\boldsymbol {q} - \boldsymbol {q} _ {z})}} = \frac {\boldsymbol {M} (\boldsymbol {q} - \boldsymbol {q} _ {z})}{f _ {c} ^ {g} (\boldsymbol {p} , \boldsymbol {q})}.
$$

Then, with the definition of the weighted norm, we have

$$
\begin{array}{l} \| \nabla_ {\boldsymbol {q}} f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}) \| _ {M ^ {- 1}} = \sqrt {\nabla_ {\boldsymbol {q}} f _ {c} ^ {g} (\boldsymbol {p} , \boldsymbol {q}) ^ {\top} M ^ {- 1} \nabla_ {\boldsymbol {q}} f _ {c} ^ {g} (\boldsymbol {p} , \boldsymbol {q})} \\ \qquad = \sqrt {\frac {(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {\top} M ^ {\top} M ^ {- 1} M (\boldsymbol {q} - \boldsymbol {q} _ {z})}{(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {\top} M (\boldsymbol {q} - \boldsymbol {q} _ {z})}} \\ \qquad = 1. \end{array}
$$

2) We first illustrate why we can not move along the gradient direction to get to the $\mathcal { Z }$ in one step. To reach $\mathcal { Z }$ in one step, we need to find a direction and step size λ such that

$$
\boldsymbol {q} - \boldsymbol {q} _ {z} = \lambda \nabla f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}).
$$

Substituting the gradient expressions, it gives

$$
\boldsymbol {q} - \boldsymbol {q} _ {z} = \lambda \frac {\boldsymbol {M} (\boldsymbol {q} - \boldsymbol {q} _ {z})}{\sqrt {(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {T} \boldsymbol {M} (\boldsymbol {q} - \boldsymbol {q} _ {z})}}.
$$

Let $\pmb { v } = \pmb { q } - \pmb { q } _ { z }$ . Then, it gives

$$
\boldsymbol {v} = \lambda \frac {\boldsymbol {M} \boldsymbol {v}}{\sqrt {\boldsymbol {v} ^ {T} \boldsymbol {M} \boldsymbol {v}}}.
$$

Left multiplying both sides by $v ^ { T }$ , it gives

$$
\boldsymbol {v} ^ {T} \boldsymbol {v} = \lambda \frac {\boldsymbol {v} ^ {T} \boldsymbol {M} \boldsymbol {v}}{\sqrt {\boldsymbol {v} ^ {T} \boldsymbol {M} \boldsymbol {v}}}.
$$

Therefore, it gives

$$
\lambda = \frac {\boldsymbol {v} ^ {T} \boldsymbol {v}}{\sqrt {\boldsymbol {v} ^ {T} M \boldsymbol {v}}} = \frac {\| \boldsymbol {q} - \boldsymbol {q} _ {z} \| ^ {2}}{\sqrt {(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {T} M (\boldsymbol {q} - \boldsymbol {q} _ {z})}}.
$$

Note that, unless M is an identity matrix, we cannot obtain $\lambda$ since $\pmb { q } _ { z }$ is unknown. However, inspired by the concept of conjugate gradient descent [96], we can try moving along the direction of $M ^ { - 1 } \nabla f _ { c } ^ { g } ( p , q )$ instead:

$$
\boldsymbol {q} - \boldsymbol {q} _ {z} = \lambda M ^ {- 1} \nabla f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}).
$$

Substituting the gradient gives

$$
\boldsymbol {q} - \boldsymbol {q} _ {z} = \lambda M ^ {- 1} \frac {M (\boldsymbol {q} - \boldsymbol {q} _ {z})}{\sqrt {(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {T} M (\boldsymbol {q} - \boldsymbol {q} _ {z})}}.
$$

Let $\pmb { v } = \pmb { q } - \pmb { q } _ { z }$ . Then, we have

$$
\boldsymbol {v} = \lambda \frac {\boldsymbol {v}}{\sqrt {\boldsymbol {v} ^ {T} M \boldsymbol {v}}}.
$$

Since the vectors on both sides are now aligned, we can directly solve for λ:

$$
\lambda = \sqrt {\boldsymbol {v} ^ {T} \boldsymbol {M} \boldsymbol {v}} = \sqrt {(\boldsymbol {q} - \boldsymbol {q} _ {z}) ^ {T} \boldsymbol {M} (\boldsymbol {q} - \boldsymbol {q} _ {z})} = f _ {c} ^ {g} (\boldsymbol {p}, \boldsymbol {q}).
$$