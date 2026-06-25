---
citation_key: GonzalezGarcia2026Safe
arxiv_id: 2606.09719
arxiv_url: https://arxiv.org/abs/2606.09719
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:25:31Z
origin: ai+web
reviewed: false
---

# Introduction

[]{#sec:introduction label="sec:introduction"}

Autonomous mobile robots operate in diverse and complex environments, requiring frameworks capable of guaranteeing safe motion planning and control, especially within constrained spaces. Narrow passages are present in a multitude of applications, from indoor environments with limited clearance, or industrial facilities with dense layouts, to inland waterways with irregular canal walls. In such contexts, accurate consideration of both the physical footprint of the robot and the enclosing environment is an essential element to maneuver safely and successfully. Methods that simplify the robot's geometry to points or circles become overly conservative, discarding vital information to navigate through tight spaces. This creates a need for frameworks that consider the actual geometry of both the robot and the surrounding free space.\

Classic motion planning methods rely on graph search through occupancy grid maps [@occupancygrid]. Such graph-based methods, including *A*\* [@astar] and Dijkstra's algorithm [@dijkstra1959note], use heuristics to compute collision-free global paths. Modern extensions involve motion primitives to consider kinodynamic feasibility, or incorporate the robot footprint into the heuristic [@macenski2020marathon2]. However, these methods result in discontinuous or non-smooth solutions. Sampling-based methods, built on probabilistic roadmaps [@508439] or rapidly-exploring random trees [@11282962], can produce kinodynamically feasible trajectories, but may lack safety guarantees during execution and become intractable in cluttered or constrained spaces. Hence, there is a need for local methods to follow these approximate paths and guarantee online safety. Traditional local methods, such as approaches based on potential fields [@Khatib1985] and velocity obstacles [@Fiorini1993], are reactive and known to easily get trapped in local minima or deadlocks, which hinders deployment in real-world settings.\
Model predictive control (MPC) [@MAYNE2000789] integrates dynamics, constraints, and objectives into an optimal control problem (OCP), making it a suitable tool for real-time robot navigation [@panoc2018ecc; @9385847; @11419776]. However, standard distance-based constraint formulations in MPC require long prediction horizons to produce effective obstacle avoidance behaviors. Control barrier functions (CBFs) address this by encoding safety through set invariance [@ames2019cbftheory; @xiao2021high], and have been widely applied for obstacle avoidance [@liu2025acc; @conecbf2024acc]. By incorporating discrete-time CBF constraints into MPC [@Agrawal2017; @dcbf2021], safety can be maintained with shorter horizons, yielding a tractable strategy for real-time, safe control.\

While MPC-CBF formulations ensure safety effectively, they commonly assume point-mass or circular robot footprints. For non-circular robots, accounting for the true geometry within an OCP requires either simplifying the shape or introducing significant constraint complexity. Approaches such as [@10886807] propose ellipsoidal representations to reduce conservatism, but remain limited in their performance in tight spaces. For arbitrary shapes, [@anyshape2025iros] achieves real-time planning using swept volume signed distance fields, though safety is enforced through penalty costs rather than hard constraints to limit additional complexity. Polytope-to-polytope obstacle avoidance CBF formulations have been proposed to address formal guarantees. [@dcbf2022] uses a duality-based approach for an MPC-CBF framework, and [@Chen2025cdcMinkowski] proposes a CBF constraint using the exact signed distance via Minkowski operations. These methods provide hard safety guarantees for non-circular robots, but they formulate avoidance constraints for each obstacle pair, scaling in complexity with the number of obstacles [@Li2024]. Moreover, they require obstacles to be represented as convex polytopes, whereas real environments are typically non-convex and described through occupancy grids or raw sensor data. Extracting a consistent set of polytopic obstacles is not always straightforward or can become computationally heavy for large environments.\

An alternative to obstacle-based formulations is to decompose the free space into convex regions. Methods such as IRIS [@deits2015computing] and RILS [@Liu2017PlanningEnvironments] compute convex polytopes directly from occupancy grids or point clouds that are guaranteed to be obstacle-free, without requiring individual obstacle identification and consideration. Recent advances have significantly improved the speed of these decompositions [@werner-RSS-25], while approaches such as FIRI [@firi2025] additionally allow incorporating the robot's footprint as a seed, ensuring that the resulting region fully contains the robot geometry. These convex representations are well suited for optimization, as each region translates into a compact set of linear constraints. Trajectories through sequences of convex regions have been generated using optimization-based methods [@deits2015icra; @Marcucci2024; @Marcucci-RSS-25; @Scheffe2023] or joint optimization of trajectory and convex cover [@wural2025]. Recently, [@corridor2025cdc] proposed a CBF formulation to keep a robot within a free-space corridor, though the robot is assumed circular. As shown in Fig. [1](#fig:conservatism){reference-type="ref" reference="fig:conservatism"}, this over-approximation for polytopic robots does not permit navigation through narrow spaces which are accessible considering the robot's actual geometry. In [@Li2024], containment of robots with general geometry inside convex free regions is addressed through polynomial positivity certificates and semidefinite programming, though the formulation optimizes a single-step control command rather than a receding-horizon trajectory.\

:::: {#fig:conservatism .figure latex-placement="tb"}
![](GonzalezGarcia2026Safe_figs/conservatism_firi.png){width="95%"}

::: caption
Circular footprint approximations do not permit to traverse through narrow spaces (a) where the robot should be able to pass based on its actual footprint (b). Construction of the free-space polytope based on a heading-aligned bounding box (c).
:::
::::

This work proposes a local motion planning and control method that guarantees to keep a polytopic robot inside convex free-space polytopes. It exploits free-space generation through FIRI, which produces convex polytopes guaranteed to contain the robot footprint. A set of discrete CBF constraints inside an MPC problem guarantees the containment of the robot's polytopic footprint within the local free-space polytope over an horizon. Because safety is encoded against the free-space boundary rather than individual obstacles, the constraint complexity scales with the number of polytope hyperplanes rather than with the number of obstacles in the environment. The formulation is decoupled from the global reference generation and can be paired with any higher-level planner that provides a path or trajectory to follow. The main contributions are:

- A polytope-in-polytope CBF (PiP-CBF) formulation for MPC, guaranteeing that a convex polytopic footprint remains inside a local free-space region,

- A comparative analysis against a polytopic obstacle-based CBF method, demonstrating favorable scaling of the MPC problem size with increasing environmental complexity.

- Experimental validation in a vessel simulation environment and a real-world autonomous mobile robot, constructing free-space regions from either prior occupancy grids or online LiDAR data, implicitly considering changes in the environment.

# Preliminaries

[]{#sec:preliminaries label="sec:preliminaries"}

This section addresses the problem of motion planning with a polytopic robot inside an unstructured environment using a polytopic free-space decomposition. In addition, this section introduces required preliminaries on discrete-time CBFs for MPC.

## Problem Formulation

Consider a robot operating in a planar environment $\mathcal{W} \subseteq \mathbb{R}^2$. The region occupied by obstacles is denoted $\mathcal{O} \subset \mathcal{W}$, and the free space is $\mathcal{F} = \mathcal{W} \setminus \mathcal{O}$. The environment is assumed to be represented by an occupancy grid or a set of points from a range sensor. No assumptions are made on any explicit obstacle decomposition. The robot's footprint is modeled as a convex polytope $\mathcal{P}_r$ with $n_r$ vertices, whose pose depends on the robot's state. A motion is considered safe if the footprint remains entirely within the free space, i.e., $\mathcal{P}_r(\boldsymbol{x}) \subseteq \mathcal{F}$, at all times. Since $\mathcal{F}$ is generally non-convex, enforcing this containment often renders the MPC hard and costly to solve. Instead, this work constructs a local convex inner approximation $\mathcal{P}_f \subseteq \mathcal{F}$ and reformulates the safety condition as $\mathcal{P}_r(\boldsymbol{x}) \subseteq \mathcal{P}_f$, which can be encoded into the MPC as a set of linear inequality constraints. The robot is assumed to receive approximate global information from a higher-level planner, and the objective is to follow this guidance while satisfying the safety condition.

## Discrete-Time Control Barrier Functions

Consider a discrete-time system described by states $\boldsymbol{x} \in \mathcal{X} \subset \mathbb{R}^{n_x}$ and controls $\boldsymbol{u} \in \mathcal{U} \subset \mathbb{R}^{n_u}$, governed by $$\begin{equation}
    \boldsymbol{x}_{k+1} = \boldsymbol{f}_d(\boldsymbol{x}_k, \boldsymbol{u}_k),
    \label{eq:dynamics}
\end{equation}$$ where $\boldsymbol{f}_d$ is locally Lipschitz. Let $h : \mathcal{X} \to \mathbb{R}$ be a continuous function, and define the associated safe set as $$\begin{equation}
    \mathcal{C} = \{ \boldsymbol{x} \in \mathcal{X} \;|\; h(\boldsymbol{x}) \geq 0 \}.
    \label{eq:safe_set}
\end{equation}$$

::: {#def:dcbf .definition}
****Definition** 1** (Discrete-Time Control Barrier Function [@dcbf2021]). *The function $h$ is a discrete-time control barrier function (DCBF) for system [\[eq:dynamics\]](#eq:dynamics){reference-type="eqref" reference="eq:dynamics"} with respect to the set $\mathcal{C}$ if for all $\boldsymbol{x} \in \mathcal{C}$, there exists $\boldsymbol{u} \in \mathcal{U}$ such that $$\begin{equation}
    h(\boldsymbol{f}_d(\boldsymbol{x}, \boldsymbol{u})) \geq (1 - \gamma)\, h(\boldsymbol{x}) \; , \quad 0 < \gamma \leq 1.
    \label{eq:dcbf}
\end{equation}$$*
:::

The parameter $\gamma$ controls how aggressively the system may approach the boundary of $\mathcal{C}$: smaller values impose a slower decay of $h$, keeping the state further from the boundary.

::: {#prop:invariance .proposition}
****Proposition** 1** ([@Agrawal2017]). *If $h$ is a DCBF for system [\[eq:dynamics\]](#eq:dynamics){reference-type="eqref" reference="eq:dynamics"}, $h(\boldsymbol{x}_0) \geq 0$, and a control input satisfying [\[eq:dcbf\]](#eq:dcbf){reference-type="eqref" reference="eq:dcbf"} is applied at every time step, then $\boldsymbol{x}_k \in \mathcal{C}$ for all $k \geq 0$.*
:::

## Model Predictive Control with DCBF Constraints

The DCBF condition [\[eq:dcbf\]](#eq:dcbf){reference-type="eqref" reference="eq:dcbf"} can be enforced over a finite horizon within a MPC formulation [@dcbf2021]. Over each control cycle, the following OCP is solved: $$\label{eq:mpc_dcbf}
\begin{align}
    \min_{\boldsymbol{x}_{k}, \boldsymbol{u}_{k}} \quad & \sum_{k=0}^{N-1} \ell(\boldsymbol{x}_{k}, \boldsymbol{u}_{k}) + \ell_{N}(\boldsymbol{x}_{N}) \label{eq:cost_function} \\
    \text{s.t.} \quad & \boldsymbol{x}_{0} = \hat{\boldsymbol{x}}, \label{eq:initial_condition} \\
    & \boldsymbol{x}_{k+1} = \boldsymbol{f}_d(\boldsymbol{x}_{k}, \boldsymbol{u}_{k}), \label{eq:dynamics_ocp} \\
    & \boldsymbol{x}_{k} \in \mathcal{X}, \quad \boldsymbol{u}_{k} \in \mathcal{U}, \label{eq:state_input_sets} \\
    & h(\boldsymbol{f}_d(\boldsymbol{x}_{l}, \boldsymbol{u}_{l})) \geq (1 - \gamma)\, h(\boldsymbol{x}_{l}), \label{eq:cbf_constraint} \\
    & l = 0, \ldots, N_{\text{cbf}} - 1, \nonumber \\
    & k = 0, \ldots, N - 1. \nonumber
\end{align}$$ where $\ell$ and $\ell_N$ are the stage and terminal costs, $\hat{\boldsymbol{x}}$ is the current state estimate, and $N_{\text{cbf}}$ is the horizon over which the safety constraint is enforced. Setting $1 < N_{\text{cbf}} < N$ leaves the remaining horizon stages free to progress towards the goal while not impacting safety on the control sequence $\boldsymbol{u}_l$. The first element of the optimal control sequence $\boldsymbol{u}_0$ is applied, and the problem is re-solved at the next time step.

# Methodology

[]{#sec:methodology label="sec:methodology"} This section first describes the proposed framework for motion planning and control. Second, it details the proposed discrete-time CBF formulation to guarantee robot containment inside a free-space polytope. Last, it covers an inflation method to compute such free-space polytopes, including proposed heuristics to bias the inflation.

## Overview

The proposed approach formulates safety as containment of the robot's polytopic footprint inside a convex free-space region, rather than as avoidance of individual obstacles. The environment is represented as a set of points, either extracted from an occupancy grid or obtained directly from a range sensor. From these points, a local convex polytope $\mathcal{P}_f \subseteq \mathcal{F}$ is constructed around the robot, and the MPC enforces a DCBF constraint that keeps the robot polytope inside this polytope throughout the safety horizon. A higher-level planner provides an approximate reference for the MPC to track. It is important to note that the containment formulation is a local safety layer and the MPC does not address global navigation. Without external global information, the robot may remain safely inside the current polytope indefinitely. The choice of higher-level planner is independent of the proposed method.

## Polytope-in-Polytope Control Barrier Function

Instead of representing the environment as a set of obstacles, this paper proposes to model the local free-space as a $d$-dimensional convex polytope $\mathcal{P}_f$. A polytope $\mathcal{P}$ is fully described by a set of $n_{h}$ hyperplanes such that any point $\boldsymbol{p} \in \mathbb{R}^d$ inside the polytope satisfies $$\begin{equation}
    \boldsymbol{W}\boldsymbol{p} + \boldsymbol{b} \geq 0,
    \label{eq:polytope}
\end{equation}$$ with $\boldsymbol{W} \in \mathbb{R}^{n_{h} \times d}$ and $\boldsymbol{b} \in \mathbb{R}^{n_{h}}$ being the normals and offsets of the hyperplanes, assumed to point inwards. Consider the robot modeled as a convex polytope $\mathcal{P}_{r}$ with $n_{r}$ vertices denoted by $\boldsymbol{v}^r_{i}$. It is fully contained inside $\mathcal{P}_f$ if and only if: $$\begin{equation}
    \boldsymbol{W}^f\boldsymbol{v}^r_{i} + \boldsymbol{b}^f \geq 0 \quad \forall \,i \in [1, n_{r}].
\end{equation}$$

Let $\boldsymbol{w}^f_j \in \mathbb{R}^d$ be the $j$-th row of $\boldsymbol{W}^f$, representing the normal of the $j$-th hyperplane. For a robot at state $\boldsymbol{x}_{l}$, one can define the distance functions: $$\begin{equation}
    h_{ij}(\boldsymbol{x}_{l}) = \boldsymbol{w}^f_j \cdot \boldsymbol{v}^r_i(\boldsymbol{x}_{l}) + b^f_{j} \label{eq:pip_cbf}
\end{equation}$$ for all $j \in [1, n_{h, f}]$ and $i \in [1, n_{r}]$. Enforcing $h_{ij}(\boldsymbol{x}_{l}) \geq 0$ on all vertices and hyperplanes guarantees containment of the robot inside $\mathcal{P}_f$. Subsequently, the discrete-time CBF condition [\[eq:cbf_constraint\]](#eq:cbf_constraint){reference-type="eqref" reference="eq:cbf_constraint"} is formulated using all $n_r \times n_{h,f}$ functions $h_{ij}$: $$\begin{equation}
    h_{ij}(\boldsymbol{f}_d(\boldsymbol{x}_{l}, \boldsymbol{u}_{l})) \geq (1 - \gamma)\, h_{ij}(\boldsymbol{x}_{l})
    % &\forall \,j \in [1, n_{h, f}] \, , \, i \in [1, n_{r}].
    \label{eq:pip_cbf_discrete}
\end{equation}$$ This ensures the robot's entire footprint remains safely contained within the free-space boundaries, strictly bounding the rate at which it may approach them.

::: remark
****Remark** 1**. *For systems where the relative degree of the containment constraint with respect to the control input exceeds one, the PiP-CBF can be formulated as a discrete-time high-order CBF [@DHOCBF].*
:::

## Free-Space Polytope Generation {#sec:firi}

To construct the free-space polytope $\mathcal{P}_f$, the convex region inflation method FIRI [@firi2025] is employed as visualized in Fig. [1](#fig:conservatism){reference-type="ref" reference="fig:conservatism"}c. It produces a polytope, described by a set of hyperplanes, from a set of occupied points or polytopic obstacle descriptions, and a convex polygon as seed. The algorithm iteratively selects hyperplanes that separate the seed from nearby occupied regions while maximizing the volume of an inscribed ellipsoid. The resulting convex polytope is guaranteed to contain the seed without overlapping with occupied space. FIRI maximizes the inscribed ellipsoid volume, which produces the largest possible convex region around the seed.

In the proposed framework, the robot's rectangular footprint, slightly inflated by a safety margin, serves as the seed polygon. Occupied points are obtained either from occupancy grid cell corners or directly from a LiDAR point cloud. The polytope is regenerated at every control cycle to guarantee containment of the robot, and its hyperplanes $(\boldsymbol{W}^f, \boldsymbol{b}^f)$ enter the MPC formulation [\[eq:mpc_dcbf\]](#eq:mpc_dcbf){reference-type="eqref" reference="eq:mpc_dcbf"} as constraint parameters through [\[eq:pip_cbf\]](#eq:pip_cbf){reference-type="eqref" reference="eq:pip_cbf"}. Because the CBF constraint is only dependent on the free-space boundary, the framework does not require detecting, segmenting, or tracking individual obstacles. This improves uptake in real-world environments where obstacle decomposition is not trivial. Any environment representation that provides a set of occupied points is a valid input to the polytope generation.

### Heuristic for Task-Informed Polytope Inflation {#heuristic-for-task-informed-polytope-inflation .unnumbered}

To shape the polytope towards a region of interest, a bounding box is constructed around the robot, and the box's edges form the initial set of hyperplanes prior to ellipsoid inflation. This confines the inflation in large maps and biases the resulting polytope. The bounding box dimensions are a design choice that can reflect a preferred direction of motion. Additionally, the seed can incorporate both the current footprint and future footprints or waypoints, on the condition that the resulting seed remains convex and is trivially verifiable to be collision-free. In this work, a longer extent of the bounding box ahead of the robot and a shorter one behind is used, favoring forward navigation. The design of the bounding box or the choice of seed are heuristics. If the local geometry does not admit a polytope extending in a useful direction, the robot remains safe inside the current region but cannot progress toward the goal.

# Scalability Analysis

[]{#sec:scalability label="sec:scalability"} MPC on a real-world setup must adhere to strict computational time limits to match the required control frequency of the system. Hence, tractability of the MPC is of the utmost importance. State-of-the-art interior-point NLP solvers such as `Ipopt` [@ipopt] and `Fatrop` [@vanroye2023fatrop] solve a symmetric, indefinite perturbed Karush-Kuhn-Tucker (KKT) system at every iteration. The worst-case computational complexity to solve this system scales cubically with the number of variables and constraints per control interval [@nocedal]. As such, keeping the problem size small and as convex as possible are two essential characteristics to keep this complexity low and adhere to limited computational resources. This section first discusses the theoretical scalability of the MPC dimensions for the PiP-CBF formulation compared to a benchmark method, with both methods assuming obstacles given as polytopes. Afterwards it provides quantitative validation of the practical implications of this scalability on extensive benchmark experiments.

## Theoretical Scalability

The duality-based CBF (D-CBF) approach from [@dcbf2022] is taken as the benchmark method. Table [1](#tab:constraints_variables){reference-type="ref" reference="tab:constraints_variables"} summarizes the additional constraints and variables that both methods add to [\[eq:mpc_dcbf\]](#eq:mpc_dcbf){reference-type="eqref" reference="eq:mpc_dcbf"}. To enforce safety, [@dcbf2022] adds both variables and constraints to the MPC problem. On the other hand, PiP-CBF only adds the constraints through [\[eq:pip_cbf\]](#eq:pip_cbf){reference-type="eqref" reference="eq:pip_cbf"}. In terms of their environmental complexity (individual obstacles vs free-space region), the number of variables ($N_x$) and constraints ($N_g$) added per control interval $[t_k, t_{k+1}]$ are: $$\begin{align}
    \text{D-CBF}: \; &N_{x} + N_{g} = N_{o}(2n_{h, o} + 2n_r + 6)\label{eq:scalability_theory_dcbf}\\
    \text{PiP-CBF}: \; &N_{x} + N_{g} = n_{h, f}n_{r},
    \label{eq:scalability_theory_pip}
\end{align}$$ where $n_{h, o}$ and $n_{h, f}$ are the number of hyperplanes used to respectively represent an obstacle or the free-space and $N_{o}$ is the number of obstacles in the environment. As demonstrated in [\[eq:scalability_theory_dcbf\]](#eq:scalability_theory_dcbf){reference-type="eqref" reference="eq:scalability_theory_dcbf"} and  [\[eq:scalability_theory_pip\]](#eq:scalability_theory_pip){reference-type="eqref" reference="eq:scalability_theory_pip"}, PiP-CBF is independent of the number of obstacles and only depends on the geometric complexity of the free-space polytope. In contrast, D-CBF is dependent on both the environment and the obstacles' geometric complexity. Note that in cases with linear system dynamics, PiP-CBF requires only linear constraints, easing its adoption for (S)QP solvers.

Figure [2](#fig:scalability){reference-type="ref" reference="fig:scalability"} visualizes the number of extra constraints and variables per control interval for each method against its own measure of environmental complexity: the number of obstacles for D-CBF and the number of free-space hyperplanes for PiP-CBF. These relations clearly show that PiP-CBF scales favorably compared to D-CBF in terms of environmental complexity. D-CBF adds a significant amount of variables and constraints per control interval while PiP-CBF only adds a small amount of constraints, without a direct dependency on the number of obstacles. For a comparable problem size, PiP-CBF accommodates a free-space polytope of twelve hyperplanes, whereas D-CBF supports only two obstacles, illustrating how much more efficiently PiP-CBF captures environmental complexity. Applying PiP-CBF enables us to safely navigate through complex environments while keeping the MPC problem tractable.

![Theoretical comparison of the inflation of the MPC problem size for D-CBF (left) and PiP-CBF (right) in terms of their environmental complexity (number of obstacles vs. number of free-space hyperplanes). All full, dashed and dash-dotted lines correspond to the results for $n_{r}$ being four, six or eight, respectively.](GonzalezGarcia2026Safe_figs/scalability.png){#fig:scalability width="100%"}

::: {#tab:constraints_variables}
                                                           Variables                                                                                                                                        Constraints
  -------------------- --------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                                                                         
   $i \in [1, N_{o}]$                                  $\begin{aligned}                                                                                                                                  $\begin{aligned}
                                \lambda_{k}^{\mathcal{O}_{i}} &\in \mathbb{R}^{n_{h,o}} \nonumber \\          -\lambda_{k}^{\mathcal{O}_{i}}\boldsymbol{b}^{\mathcal{O}_{i}} - \lambda_{k, i}^{\mathcal{R}_{i}}\boldsymbol{b}^{\mathcal{R}} &\geq \omega_{k, i}(\Pi_{j=0}^k\gamma_{j})h_{i}(\boldsymbol{x}_{k})\\[-0.5ex]
                              \lambda_{k, i}^{\mathcal{R}} &\in \mathbb{R}^{n_{r}} \nonumber \\[-0.5ex]                                                               \|\lambda_{k}^{\mathcal{O}_{i}}\boldsymbol{W}^{\mathcal{O}_{i}}\|_{2}^{2} &\leq 1\\[-0.5ex]
                                               \omega_{k, i} &\in \mathbb{R} \nonumber                                                         \lambda_{k}^{\mathcal{O}_{i}}\boldsymbol{W}^{\mathcal{O}_{i}} + \lambda_{k, i}^{\mathcal{R}}\boldsymbol{W}^{\mathcal{R}} &= 0 \\[-0.5ex]
                                                         \end{aligned}$                                                                                            \lambda_{k}^{\mathcal{O}_{i}} \; ; \; \lambda_{k, i}^{\mathcal{R}} \; ; \; \omega_{k, i} &\geq 0
                                                                                                                                                                                                           \end{aligned}$
                                                                                                         
   $l \in [1, n_{r}]$                                          /                                                                                                       $\boldsymbol{W}^{f}\boldsymbol{p}_l(\boldsymbol{x}_{k}) + \boldsymbol{b}^{f} \leq 0$

  : D-CBF and PiP-CBF formulation per interval $[t_k, t_{k+1}]$.
:::

::: table*
+-----------------------------------+---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| Metric                            | Method  | 1            | 2            | 3            | 4             | 5             | 6             | 7             | 8             | 9             | 10            |
+==================================:+:=======:+:============:+:============:+:============:+:=============:+:=============:+:=============:+:=============:+:=============:+:=============:+:=============:+
| Iterations \[-\]                  | D-CBF   | 7            | 9            | 9            | 10            | 13            | 14            | 14            | 15            | 16            | 16            |
|                                   +---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
|                                   | PiP-CBF | **5**        | **5**        | **5**        | **6**         | **8**         | **10**        | **10**        | **11**        | **9**         | **10**        |
+-----------------------------------+---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| $N_x$ \[-\]                       | D-CBF   | 393          | 602          | 811          | 1020          | 1129          | 1438          | 1647          | 1856          | 2065          | 2274          |
|                                   +---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
|                                   | PiP-CBF | **184**      | **184**      | **184**      | **184**       | **184**       | **184**       | **184**       | **184**       | **184**       | **184**       |
+-----------------------------------+---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| $N_g$ \[-\]                       | D-CBF   | **525**      | 810          | 1095         | 1380          | 1665          | 1950          | 2235          | 2520          | 2805          | 3090          |
|                                   +---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
|                                   | PiP-CBF | 620          | **696**      | **772**      | **772**       | **848**       | **848**       | **1000**      | **1000**      | **848**       | **848**       |
+-----------------------------------+---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| Max. $n_{h, f}$ \[-\]             | PiP-CBF | 5            | 6            | 7            | 7             | 8             | 8             | 10            | 10            | 8             | 8             |
+-----------------------------------+---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| Reduction $t_{\text{wall}}$ \[-\] |         | 1.41$\times$ | 3.54$\times$ | 6.33$\times$ | 10.67$\times$ | 17.47$\times$ | 23.31$\times$ | 31.36$\times$ | 42.90$\times$ | 75.39$\times$ | 91.65$\times$ |
+-----------------------------------+---------+--------------+--------------+--------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
:::

## Quantitative Comparison {#sec:quant}

To quantify the practical implications of the increased problem dimensions, a scalability benchmark is conducted for both methods. Experiments are performed on a Nvidia Jetson Orin AGX using `Fatrop` [@vanroye2023fatrop] through `CasADi` [@Andersson2019] to solve the MPC problem. 100 environments, containing up to ten obstacles, are pseudo-randomly generated. Both methods have to navigate a rectangular robot through each environment between four distinct start and goal pose combinations, using *A\** [@astar] as global reference path. This results in more than 130,000 MPC solutions composing our scalability data. FIRI [@firi2025] computes the free-space polytope for PiP-CBF using the robot footprint plus two points of the global path in front of the robot as seed. FIRI directly uses the polytopic obstacles as input. The horizons $N$ and $N_{\text{cbf}}$ are chosen as 30 and 20, with $\gamma= 0.2$. Fig. [3](#fig:scalability_kkt_total){reference-type="ref" reference="fig:scalability_kkt_total"} reports the wall time per iteration spent in `Fatrop` to compute a new search direction (i.e., solve the KKT system, determine step size, etc.) and the total wall time to solve the MPC problem. Table [\[tab:scalability_results\]](#tab:scalability_results){reference-type="ref" reference="tab:scalability_results"} reports the number of constraints and variables added to the MPC problem, the median number of iterations, the maximum number of free-space hyperplanes $n_{h, f}$ per number of obstacles, and the reduction of the median wall time required to solve the MPC problem. Across all generated environments, both methods achieve a 100% success rate in reaching the goal while maintaining strict collision avoidance throughout the trajectory.

First, Table [\[tab:scalability_results\]](#tab:scalability_results){reference-type="ref" reference="tab:scalability_results"} shows that PiP-CBF adds up to 12$\times$ fewer variables and 3.6$\times$ fewer constraints due to its independence of the number of obstacles. This effect is reflected in the time spent to compute a new search direction, shown at the top of Fig. [3](#fig:scalability_kkt_total){reference-type="ref" reference="fig:scalability_kkt_total"}. D-CBF's wall time increases cubically with the number of obstacles while PiP-CBF's wall time stays almost constant. The bottom figure shows a similar trend for the total computation time. The median wall time is reduced between $1.4\times$ and $91\times$ for environments up to ten obstacles. Both reductions are attributed to the limited increase in the complexity of the free-space polytope and thus the MPC problem dimensions in [\[eq:scalability_theory_pip\]](#eq:scalability_theory_pip){reference-type="eqref" reference="eq:scalability_theory_pip"} for an increasingly cluttered environment. At a required control rate of 10 Hz, D-CBF remains tractable only up to four obstacles, beyond which its median wall time exceeds the 100 ms budget. Restricting D-CBF to the nearest obstacles could circumvent this limitation. However, the bottom row of Table [\[tab:scalability_results\]](#tab:scalability_results){reference-type="ref" reference="tab:scalability_results"} shows that even with this restriction, PiP-CBF reduces computation time by $1.4\times$ to $10.67\times$. This improvement allows to: i) increase the control frequency or horizon, ii) control more complex systems or iii) perform other necessary computations. Second, PiP-CBF requires between 7% and 44% fewer iterations at the median to solve the MPC problem. This is due to PiP-CBF's convex structure, compared to D-CBF's non-convex formulation, in turn also contributing to lower total computation times.

![Quantitative validation for an increasing amount of obstacles of the scalability of D-CBF and PiP-CBF in terms of the wall time per iteration to solve the KKT system (top) and the total wall time to solve the MPC problem (bottom).](GonzalezGarcia2026Safe_figs/total_kkt_per_iter_violin_allenvs.png){#fig:scalability_kkt_total width="100%"}

# Experimental Validation

[]{#sec:experiments label="sec:experiments"} This section addresses the experimental validation of the proposed framework, including simulation experiments with an autonomous surface vessel, and real-world experiments with an autonomous mobile robot prototype. Furthermore, a discussion of the benefits and limitations is presented.

:::: {#fig:amr_photo .figure latex-placement="tb"}
![](GonzalezGarcia2026Safe_figs/output9.png){width="95%"}

::: caption
Visualization of the real-world lab setup including the AMR platform, the constructed free-space polytope based on the LiDAR's point cloud and the global A\* reference.
:::
::::

:::: {#fig:sim_environments .figure latex-placement="tb"}
![image](GonzalezGarcia2026Safe_figs/vessel_sim.png){width="85%"} ![image](GonzalezGarcia2026Safe_figs/dynamic_parking-lc5-2.png){width="85%"}

::: caption
Illustration of runs for the ASV (a, b) and AMR (c, d) cases using occupancy grids (a, c) and LiDAR (b, d). The traveled path is visualized in blue, free-space polytopes at various time instances are indicated in green. (d-1) and (d-2) depict different time instances of a dynamic environment showing the AMR safely navigating around a dynamic obstacle.
:::
::::

:::: {#fig:conservatism_ts .figure latex-placement="t"}
![](GonzalezGarcia2026Safe_figs/map_1_timeseries.png){width="100%"}

::: caption
Visualization of PiP-CBF's conservatism for the environment in Fig. [5](#fig:sim_environments){reference-type="ref" reference="fig:sim_environments"}a in terms of the clearance to the edge of the free-space polytope (blue) and the actual obstacles (red).
:::
::::

## Setup

The framework is validated in simulation with an Autonomous Surface Vehicle (ASV) and on hardware with an Autonomous Mobile Robot (AMR) with bicycle kinematics. For each case, two sets of experiments are conducted: i) using static occupancy grids, and ii) using LiDAR sensing. These configurations exercise distinct aspects of the framework. The ASV and AMR platforms test the approach under holonomic and non-holonomic dynamics respectively. The occupancy grid and scan configurations correspond to two standard operating regimes: a known environment, where a global path can be computed on a static map, and a reactive, unknown setting where the free space is constructed solely from online sensing. The LiDAR configuration additionally lets us evaluate performance in dynamic environments, with slowly moving obstacles that are not part of any prior map. All experiments run on a NVIDIA Jetson Orin AGX, with a desired update rate of 10 Hz. The MPC is solved using `Fatrop` [@vanroye2023fatrop] through `CasADi` [@Andersson2019]. The prediction horizon is $N=40$ for the ASV and $N=20$ for the AMR, with $N_{\text{cbf}}=10$ for ASV grid map runs, $N_{\text{cbf}}=20$ for ASV LiDAR runs, and $N_{\text{cbf}}=18$ for all AMR runs. The CBF decay rate is $\gamma = 0.2$, and the OCP accepts a maximum of 20 hyperplanes per polytope.

The ASV simulator follows the dynamics of [@WeiICRA2018], implemented in ROS [@Quigley09]. The grid map configuration covers four segments based on Amsterdam canals, with *A\** providing global guidance and polytopes are generated directly from the occupancy grid. The LiDAR configuration uses Gazebo [@gazebo] to simulate sensor data in three cluttered canal intersections, computes an approximate plan via lexicographic search [@Shan2020], and builds a polytope using only current laser scan data.

The AMR prototype (Fig. [4](#fig:amr_photo){reference-type="ref" reference="fig:amr_photo"}) uses a KELO Drive 100 as a steerable front wheel, with a wheelbase of $L_0 = 0.42$ m and a $0.55 \times 0.35$ m rectangular footprint. Localization is provided by an HTC VIVE Tracker 3.0 with four base stations. An Ouster OS0 LiDAR is mounted on the robot and used for obstacle sensing in the LiDAR configuration. The full AMR software stack is built on ROS 2 [@macenski2022robot]. For each run, manual goal positions are issued, and *A\** computes an approximate reference path in both configurations. For grid map runs, both the global path and polytopes are built online with the static maps across ten indoor scenarios. For LiDAR runs, the robot accumulates scans during navigation into an online map for *A\** guidance while polytopes are generated from the point cloud data; these experiments include scenarios with slowly moving dynamic obstacles. Environmental features such as the occupancy grid, the point clouds and the free-space polytope are visualized as projections onto the laboratory floor.

## Results & Discussion

Table [2](#tab:results){reference-type="ref" reference="tab:results"} summarizes the MPC wall time and polytope statistics across all four experiment configurations. Representative trajectories are shown in Fig. [5](#fig:sim_environments){reference-type="ref" reference="fig:sim_environments"}, and the supplementary video shows runs from each configuration.

::: {#tab:results}
+-------------+------+--------------------------------+------------------------------+
|             | Runs | $t_\text{wall}$ \[ms\]         | $n_{h,f}$                    |
+:============+:====:+:========:+:========:+:========:+:====:+:=====:+:=============:+
| 3-5 (lr)6-8 |      | median   | p99      | max      | mean | range | ${>}15$ \[%\] |
+-------------+------+----------+----------+----------+------+-------+---------------+
| ASV (map)   | 4    | 5.5      | 10.6     | 100.9    | 9.9  | 5--20 | 3.2           |
+-------------+------+----------+----------+----------+------+-------+---------------+
| ASV (scan)  | 3    | 11.1     | 38.6     | 100.8    | 9.9  | 7--16 | 0.2           |
+-------------+------+----------+----------+----------+------+-------+---------------+
| AMR (map)   | 10   | 34.2     | 79.8     | 91.5     | 10.5 | 7--17 | 0.5           |
+-------------+------+----------+----------+----------+------+-------+---------------+
| AMR (scan)  | 15   | 46.4     | 89.4     | 124.3    | 11.3 | 7--16 | 0.1           |
+-------------+------+----------+----------+----------+------+-------+---------------+

: MPC with PiP-CBF solve time and polytope statistics.
:::

In the ASV simulations, fewer than 0.04% of computation times exceeded the desired 100 ms control period and no collisions were observed. The number of active hyperplanes averaged around 10 in both sensing modes. This confirms that, independent of the sensor input, the polytope complexity is governed by the local geometry. Since the free-space polytope is a convex inner approximation of the true (generally non-convex) obstacle-free region, it necessarily discards some navigable space. Fig. [6](#fig:conservatism_ts){reference-type="ref" reference="fig:conservatism_ts"} illustrates this effect for the ASV occupancy grid run from Fig. [5](#fig:sim_environments){reference-type="ref" reference="fig:sim_environments"}a by showing the time evolution of the minimum distance from the footprint to the polytope boundary alongside the minimum distance from the footprint to the nearest occupied point. Near bends and intersections, where the free space is highly non-convex, the polytope boundary is closer to the footprint than the actual obstacles, reflecting the space lost by the convex approximation. In tight passages, where the obstacles are the binding constraint, both distances converge and the approximation is near-exact. In Fig. [6](#fig:conservatism_ts){reference-type="ref" reference="fig:conservatism_ts"}, the minimum footprint-to-polytope distance was 2.6 cm and the minimum footprint-to-obstacle distance 2.7 cm, both occurring at the tightest point of the trajectory.

On the AMR case, computation times were higher due to the combination of the complex kinematics with the steerable front wheel and the navigation through narrow spaces. The median and 99th percentile nevertheless remained below the desired 100 ms budget in both configurations, with fewer than 0.1% of outliers above the threshold. No collisions were observed across any run, including the ten AMR LiDAR runs in which humans (pushing carts in some cases) crossed the workspace during navigation. Fig. [5](#fig:sim_environments){reference-type="ref" reference="fig:sim_environments"}c shows the AMR executing a reverse parking maneuver, where the footprint always remains inside the generated polytopes throughout the turn. Fig. [5](#fig:sim_environments){reference-type="ref" reference="fig:sim_environments"}d shows the polytope contracting as a dynamic obstacle enters the previously constructed polytope and re-expanding after it passes.

Setting $N_{\text{cbf}} < N$ allows the prediction horizon to extend beyond the current free-space polytope. This guides the robot toward the goal and avoids explicit corridor sequencing. Our bounding box heuristic biases the convex coverage toward the robot's forward direction, and produced a polytope covering a feasible path at every replanning cycle across the 32 reported runs. The heuristic is a tuning choice rather than a guarantee of navigation completeness: when the feasible path requires motion outside the box, or when the reference itself is infeasible, the robot stops safely but cannot make progress. Generating convex free-space regions that satisfy downstream navigation requirements is not a trivial task [@firi2025], and coupling the construction of the bounding box to the reference path or to the robot's dynamics is a direction for future work.

Across all experiments, the free-space hyperplane count remained between 5 and 20 regardless of the environment or its representation, with fewer than 4% exceeding 15 in any configuration. The framework operated without structural modification to the MPC or CBF formulation across holonomic and non-holonomic dynamics; grid map and LiDAR inputs; and simulated and physical environments. No collisions were observed in any of the 32 reported runs. Although dynamic obstacles are not explicitly considered in the formulation, recomputing the polytope at every time step allows the method to directly react to changes in the environment, including slowly moving obstacles or people.

# Conclusions & Future Work

This work presented a polytope-in-polytope MPC-CBF formulation that keeps a convex robot footprint inside a free-space polytope. Because safety is encoded against the free-space boundary rather than against individual obstacles, the constraint complexity scales with the number of free-space hyperplanes and robot vertices, independent of the number of obstacles in the environment. This also eliminates the need for obstacle segmentation or tracking in the perception pipeline: the controller operates directly on occupancy grids or point clouds, and is compatible with any reference source that provides a path or goal position. The approach is validated across holonomic and non-holonomic dynamics, grid map and LiDAR inputs, and simulated and physical environments. All computations are executed online on an onboard embedded platform. Future work includes coupling the polytope generation to the robot's dynamics or the planned trajectory, so that the free-space region accounts for future robot navigation instead of only the current status. This will improve safety and overall smoothness as consecutive polytopes account for the robot's behaviour over subsequent control inputs. The polytope construction will inherently follow the robot's intended motion direction, removing the need for a heuristic to progress towards the goal. Involving the (estimated) motion of dynamic obstacles into the construction of (a sequence) of free-space regions forms an interesting future research direction. Formal guarantees on corridor continuity over consequent MPC solutions and navigation completeness remain open challenges.

[^1]: This work was supported by the Flanders Make SBO projects ARENA (Agile & Reliable Navigation) and LearnOpTra (Learning meets optimization for robust and multimodal trajectory planning).

[^2]: All authors are with MECO Research Team, Department of Mechanical Engineering, KU Leuven, Belgium and Flanders Make@KU Leuven, Belgium. `{alex.gonzalezgarcia, dries.dirckx, jan.swevers, wilm.decre}@kuleuven.be`

[^3]: $^\dagger$A. Gonzalez-Garcia and D. Dirckx are equal contributors to this work.
