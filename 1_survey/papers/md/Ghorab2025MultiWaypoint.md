---
citation_key: Ghorab2025MultiWaypoint
arxiv_id: 2507.23350
arxiv_url: https://arxiv.org/abs/2507.23350
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:21:05Z
origin: ai+web
reviewed: false
---

::: keywords
Motion Planning and Control, Agricultural Robots, Dubins Traveling Salesman Problem, Model Predictive Control.
:::

# Introduction

Autonomous navigation in unstructured agricultural environments, such as meadows, poses significant challenges due to unpredictable terrain, the non-holonomic system dynamics of many mobile robots, and the possible presence of both static and dynamic obstacles [@mammarellaCooperationUnmannedSystems2022a]. An ecological weed control system is a prime application where efficient navigation is crucial, enabling the reduction of herbicide use and minimizing human intervention. In the considered application, the process begins by selecting a geo-fence that defines the field's safety boundaries, ensuring the robot operates within a designated area. Next, the target weeds are autonomously detected and mapped during a scanning phase. Once the scanning and mapping are complete, the robot is tasked with navigating to the identified weeds and eliminating them using a mechanical weed removal tool, avoiding the use of chemical herbicides. This last phase is the primary focus of this work, where the proposed DTSP-based global path planner, as well as the NMPC local path planner and waypoint-following controller are integrated to efficiently guide the robot to each detected weed, while considering the different robot and environmental constraints.

However, the order in which the targets should be visited is not determined a priori. Hence, the objective of the global path planner is to generate a feasible path of minimum length that efficiently visits all the targets. The problem of determining the order of waypoints to minimize travel distance is typically formulated as an Euclidean Traveling Salesman Problem (ETSP). However, solving the ETSP alone does not consider the vehicle's non-holonomic constraints or environmental constraints, such as avoiding damage to soil and healthy grass by preventing arbitrarily sharp turns in the path. Therefore, the planner has to consider curvature constraints, by generating a minimum length path making use of Dubins curves instead of straight line segments. This formulation, known as the Dubins Traveling Salesman Problem (DTSP), extends the classical ETSP to non-holonomic vehicles with a minimum turning radius constraint [@savlaPointtopointTravelingSalesperson2005].

While the DTSP based planner provides a feasible global path to guide the robot towards each waypoint, a local planner and controller is essential for ensuring safe and adaptive navigation in dynamic environments and computing the necessary control input. The presence of static obstacles and dynamic agents, such as animals, human workers or other robots operating in the field, requires real-time local path replanning. To this end, Nonlinear Model Predictive Control (NMPC) is employed as both the local path planner and waypoint following controller within the same framework.

## Related Work {#subsec:related_work}

Various formulations and extensions of the DTSP and NMPC have been presented in the literature, each with its own advantages and trade-offs. Selecting the right combination of DTSP and NMPC formulations is crucial for achieving efficient and reliable navigation in agricultural environments. The choice directly impacts the optimality of the generated paths, the overall motion control objectives, and the ability to meet specific task requirements while adhering to overall system's constraints.

Approaches to solving DTSP primarily differ in how they determine the ordering of waypoints and compute the associated orientations. These differences influence the accuracy of the near optimal solution, and the computational effort. Similarly, NMPC formulations vary in terms of cost function design, constraints handling, and real-time performance, making the selection process highly application-dependent.

This work emphasizes the importance of choosing the most suitable DTSP and NMPC formulations tailored to agricultural applications, balancing global path feasibility, motion planning adaptability, and considering real-world operational constraints.

### DTSP-based Global Path Planning {#subsubsec:dtsp}

In [@dubinsCurvesMinimalLength1957] Dubins introduced a method for determining the shortest path in a 2D space, given curvature constraints as well as the entry and exit orientations between two points as input. The resulting path consists of a combination of straight line segments and arcs with radii that adhere to the vehicle's curvature constraints.

The DTSP was first introduced by [@savlaPointtopointTravelingSalesperson2005]. In this extension of the classical TSP, the path connecting any two points must be a Dubins curve and two curves that meet at the same point must share the same orientation.

The core distinctions between methods addressing the DTSP lie in how they determine the ordering of the waypoints and calculate the orientations associated with the points. Interested readers are referred to the comprehensive survey [@macharetSurveyRoutingProblems2018] for a detailed review of the various routing methods.

Existing literature mostly adopted a decoupled approach for route generation [@savlaPointtopointTravelingSalesperson2005; @maRecedingHorizonPlanning2006; @rathinamResourceAllocationAlgorithm2007; @macharetDataGatheringTour2012]. Thereby, first, the visiting sequence is determined solving the ETSP. Then, the vehicle's orientation at each point is defined, for example, using the Alternating Algorithm (AA) [@savlaPointtopointTravelingSalesperson2005]. Finally, the waypoints are connected with Dubins curves. However, relying solely on the Euclidean distance metric to define the visit order does not necessarily yield efficient results when using Dubins curves for path generation. This approach can lead to excessive circular maneuvers, especially in dense waypoint configurations typical of autonomous weed control applications. Since the optimization of waypoint coordinates and headings is inherently coupled, decoupling them compromises optimality [@vanaOptimalSolutionGeneralized2020]. As a result, a tour based solely on the ETSP ordering cannot achieve an approximation ratio better than $O(n)$ (i.e., the best solution is within a factor of $n$ of the optimal solution) see [@nyDubinsTravelingSalesman2012].

In the coupled approach, the sequence is determined by directly using the lengths of the Dubins curves between pairs of points. However, the main challenge here is to find the right mechanism to determine the entry and exit orientations without even having a predefined sequence of points. In [@lenyApproximationAlgorithmCurvatureConstrained2010], the orientations of all points are initially set to zero (or a fixed random value), and all interconnecting curves are calculated and connected to form a complete graph. An instance of the Asymmetric TSP (ATSP) is then solved to find the shortest path in this graph. This method was later extended to include a complete heading discretization [@lenyPerformanceOptimizationUnmanned2008]. The technique involves selecting a finite set of $k$ possible headings at each waypoint. A graph is created with $n$ clusters, each representing a waypoint and containing $k$ nodes that correspond to different headings. Subsequently, the Dubins distance between configurations of node pairs from different clusters is computed. Finally, a tour through all clusters, containing exactly one point per cluster, is then determined. A logarithmic approximation ratio $O(log(n))$ for this ATSP can be achieved by directly solving the problem using available algorithms implementations, such as those described in [@helsgaunEffectiveImplementationLin2000; @friezeWorstcasePerformanceAlgorithms1982; @kaplanApproximationAlgorithmsAsymmetric2003].

In both DTSP formulations and most global planners in general, solutions are computed under tight time constraints, often resulting in suboptimal paths based on simplified models. Consequently, there is considerable room for improvement by integrating appropriate motion planning and control systems to further locally optimize the global path.

### NMPC-based Motion Planning

The fundamental principle of MPC is to use the system's model to forecast its future behavior and optimally adjust control actions by solving a constrained optimization problem over a receding horizon at each sampling time [@rawlingsModelPredictiveControl2017; @gruneNonlinearModelPredictive2017]. By minimizing a cost function that incorporates possible nonlinear multi-input multi-output (MIMO) system dynamics along with state and input constraints, NMPC has proven to be a promising approach for various applications, including stabilization, tracking, and motion planning of mobile robots in unstructured and dynamic environments [@mehrezPredictivePathFollowing2017; @britoModelPredictiveContouring2019; @solopertoNonlinearMPCScheme2023; @lorenzenMPCbasedMotionPlanning2025].

In automated weed control applications, the primary objective is for the robot to reach and stop at each designated waypoint. This is ensured by making the state corresponding to the desired pose a stable attractor of the feedback control loop. A conventional approach to ensure this with NMPC involves enforcing terminal costs and/or terminal region constraints near the desired set-point. However, when the set-point is located at relatively long distance from the robot, the prediction horizon required becomes prohibitively long for practical applications. An alternative strategy is to reformulate the problem as one of path following by generating a global path that connects all waypoints and then following this path piece-wise [@faulwasserModelPredictivePathfollowing2009; @yuNonlinearModelPredictive2015; @mehrezPredictivePathFollowing2017].

In the considered application, as in many other applications, the goal is to reach the target while satisfying constraints rather than strictly following a specific path. As noted in Section [1.1.1](#subsubsec:dtsp){reference-type="ref" reference="subsubsec:dtsp"}, global planners often yield suboptimal paths when computed in finite time, particularly under kinematic and dynamic constraints. Therefore, exactly following these paths can complicate motion control and make it impossible when real-time obstacle avoidance is required. Instead, a flexible approach that allows the motion planner to dynamically optimize the global path and find shortcuts is preferred.

A novel NMPC formulation, proposed in [@lorenzenMPCbasedMotionPlanning2025], guarantees convergence to a desired target while ensuring closed-loop stability, adherence to system constraints, and collision avoidance with obstacles. The method optimally selects an artificially generated reference set-point, dynamically adjusted along the global reference path, which guides the robot without requiring strict path following. This artificial reference is used to define feasible stabilizing terminal constraints.

This work adapts and integrates the coupled DTSP formulation from [@lenyPerformanceOptimizationUnmanned2008] with the NMPC-based motion planner from [@lorenzenMPCbasedMotionPlanning2025] to enable an automated, robot-based weed control application. The resulting integrated framework addresses a critical gap in applied research by combining a multi-waypoint, curvature-constrained DTSP-based global planner with an advanced NMPC-based local motion planner and controller tailored for agricultural robots.

The remainder of the paper is organized as follows. Section [2](#sec:methods){reference-type="ref" reference="sec:methods"} details the proposed system, explaining the integration of the DTSP-based global path planner with the NMPC-based local path planner and waypoint follower. Section [3](#sec:results){reference-type="ref" reference="sec:results"} describes the simulation setup and presents a comparative analysis of the results. Finally, Section [4](#sec:Summary_Outlook){reference-type="ref" reference="sec:Summary_Outlook"} concludes the paper and outlines directions for future work.

# Proposed Navigation and Control System {#sec:methods}

## System Overview

The proposed system integrates a two-layer architecture for autonomous navigation. The global path planner, based on the coupled DTSP formulation, processes unordered multi-waypoint coordinates to compute an optimal sequence of curvature-constrained Dubins paths connecting these waypoints. These paths minimize travel distance while adhering to curvature constraints tailored specifically for agricultural applications, where sharp turns can damage the soil and grass. The NMPC-based local path planning and waypoint following algorithm utilizes the resulting global Dubins path to ensure precise convergence to each waypoint while respecting different system constraints.

## DTSP Algorithm

Given $W$ waypoints in a 2D space, the DTSP aims to determine the shortest path that connects all points while adhering to curvature constraints. Consequently, the path between any two points should be a Dubins curve, and the curves meeting at the same point must share the same orientation.

The following steps present the DTSP routing problem based on [@lenyPerformanceOptimizationUnmanned2008]:

1.  For each of the $W$ target points, select $K$ candidate headings (e.g., $k\frac{2\pi}{K}$ for $k\in \{0,1,...,K-1\}$).

2.  Represent each target as a cluster of $K$ nodes, where each node corresponds to a configuration $q_i = (p_i,\theta_i)$ with position $p$ and a candidate heading $\theta$. The total number of nodes is $nK$.

3.  For each pair of nodes $q_i$ and $q_j$ that belong to different clusters (i.e., different targets), compute the Dubins curve with minimum distance $\mathcal{D}_\rho(q_i,q_j)$. This curve is parameterized by the minimum turning radius $\rho$, defines the cost for traveling from a specific configuration at target $i$ to a different one at target $j$.

4.  Arrange the computed Dubins distances into a cost matrix $M$ of size $N \times N$, where $N = nK$.

From the matrix $M$, one can construct an ordered sequence $\mathbf{Q}_{\Sigma} \;=\;(q_{\Sigma (0)}, q_{\Sigma (1)} , \dots , q_{\Sigma (N-1)} )$ which represent some permutation $\Sigma$ of configurations $q_{\Sigma (i)} = (p_{\Sigma (i)},\theta_{\Sigma (i)})$ of a complete tour of the mobile robot, after excluding transitions between configurations within the same target.

Based on this representation, the corresponding objective function can be formulated as follows: $$\begin{equation}
    \underset{\theta, \, \Sigma}{\text{minimize}} \quad \mathcal{L}_{\rho} (\mathbf{Q}_{\Sigma})
    \label{eq:dtsp_obj}
\end{equation}$$ Where the cost function is defined as: $$\begin{equation}
     \mathcal{L}_{\rho} (\mathbf{Q}_{\Sigma}) = \mathcal{D}_{\rho} (q_{\Sigma (N-1)}, q_{\Sigma (0)}) + \sum_{i=0}^{N-2} \mathcal{D}_{\rho} (q_{\Sigma (i)}, q_{\Sigma (i+1)})
    \label{eq:dtsp_cost}
\end{equation}$$

## NMPC Algorithm

The robot's motion is governed by a discrete-time, nonlinear dynamic system, described by the following difference equation: $$\begin{equation}
    \mathbf{x}(n+1) = f(\mathbf{x}(n), \mathbf{u}(n)),
\end{equation}$$ where $f : \mathbb{R}^{n_x} \times \mathbb{R}^{n_u} \to \mathbb{R}^{n_x}$ is a continuous function that models the system dynamics. Here, $x(n) \in \mathbb{R}^{n_x}$ represents the system state, while $u(n) \in \mathbb{R}^{n_u}$ denotes the control input at the sampling time $t_n$, where $n = 0, 1, 2, \dots$.

The global path $\mathcal{P}_d$ generated from the DTSP-based planner can be represented as a sequence of path segments connecting each pair of consecutive waypoint poses as follows: $$\begin{equation}
    \mathcal{P}_d = (p_0, p_1, \dots, p_{W-1}),
\end{equation}$$

where $W$ is the total number of waypoints. Each path segment $p_w$ is described as a continuous function: $$\begin{equation}
    p_w : [0, 1] \mapsto \mathbb{R}^{n_{x}},
\end{equation}$$ where $p_w(0)$ represents the initial configuration of the path segment, while $p_w(1)$ represents the target configuration.

The following NMPC formulation used in this work was originally proposed in [@lorenzenMPCbasedMotionPlanning2025]. This approach ensures that both constraint satisfaction and convergence to a desired target can be guaranteed. Unlike traditional path-following approaches, this method does not require the robot to strictly follow the reference path $p_w$. Instead, the path only serves as a guidance mechanism to identify a suitable terminal constraint, which guarantees that at each control step, the local solution computed by the NMPC algorithm can be suitably extended to reach the target pose. This is achieved by introducing an artificial reference, which serves as an intermediate target configuration and is optimized within the NMPC optimization problem.

In the following, the predicted state and control input trajectories over the finite prediction horizon $N$ are denoted as $\mathbf{\bar{x}}(\cdot) \in X$ and $\mathbf{\bar{u}}(\cdot) \in U$, where $X$ and $U$ represent the set of admissible states and inputs respectively. These trajectories are defined as $$\begin{align}
    \mathbf{\bar{x}}(\cdot) & = (\mathbf{\bar{x}}(1), \mathbf{\bar{x}}(2), \dots, \mathbf{\bar{x}}(N)),   \\
    \mathbf{\bar{u}}(\cdot) & = (\mathbf{\bar{u}}(0), \mathbf{\bar{u}}(1), \dots, \mathbf{\bar{u}}(N-1)).
\end{align}$$

The artificial reference is chosen along the current path segment $p_w$. With the additional optimization variable $\bar{s}\in [0, 1]$ and the path $p_w$, this artificial reference is given by $p_w(\bar{s})$.

The MPC cost function is defined by $$\begin{equation}
    J_N(\mathbf{x}_0, \mathbf{\bar{x}}(\cdot), \mathbf{\bar{u}}(\cdot), \bar{s}) = \sum_{k=0}^{N-1} \ell(\mathbf{\bar{x}}(k), \mathbf{\bar{u}}(k)) + V_o(\bar{s}),
\end{equation}$$ where the stage cost $\ell : \mathbb{R}^{n_{x}+n_{u}} \to \mathbb{R}_{\leq 0}$ and offset cost $V_0 : [0, 1] \to \mathbb{R}_{\geq 0}$ are positive definite functions. We define the stage cost $$\begin{equation}
    \ell(\mathbf{\bar{x}}(k), \mathbf{\bar{u}}(k)) = \left\Vert \mathbf{\bar{x}}(k) - p(\bar{s}) \right\Vert^4_{Q} + \left\Vert \mathbf{\bar{u}}(k) \right\Vert^4_{R},
\end{equation}$$ where $Q$ and $R$ are positive definite weighting matrices that penalize the deviation of the predicted states from the intermediate artificial reference pose and penalize excessive control effort, respectively.

The offset cost $V_o(\bar{s})$ ensures that the artificial reference progresses forward toward the final target pose $p_w(1)$ as it penalizes the distance along the path between the current artificial reference and the target pose. Is defined by $$\begin{equation}
    V_o(\bar{s}) = q_s (1 - \bar{s})^2,
\end{equation}$$ where $q_s$ is a positive weighting scalar that penalizes the deviation between the final reference index $1$ and the current optimal intermediate artificial reference $\bar{s}$.

Finally, the NMPC algorithm at each sampling time $t_n$, $n = 0, 1, 2, \dots$, can be described as follows:

1.  Measure the state $\mathbf{x}(n) \in X$ of the robot.

2.  Set $\mathbf{x}_0 = \mathbf{x}(n)$, solve the optimal control problem (OCP) defined by: $$\label{ocp}
                  \begin{align}
                      \underset{\mathbf{\bar{u}}(\cdot), \, \bar{s}}{\text{minimize}} & \quad J_N(\mathbf{x}_0, \mathbf{\bar{x}}(\cdot), \mathbf{\bar{u}}(\cdot), \bar{s}) \label{ocp:a} \\[6pt]
                      %
                      \text{s.t.} \quad \mathbf{\bar{x}}(0)                           & = \mathbf{x}_0 \label{ocp:b}                                                                     \\
                      %
                      \mathbf{\bar{x}}(k+1)                                           & = f\bigl(\mathbf{\bar{x}}(k), \mathbf{\bar{u}}(k)\bigr), \quad k \in [0,\, N-1] \label{ocp:c}    \\
                      %
                      \mathbf{\bar{x}}(k)                                             & \in X, \quad k \in [1,\, N] \label{ocp:box_x}                                                    \\% \why called box_x_ This is not a box constraint.                                                  \\
                      %
                      \mathbf{\bar{u}}(k)                                             & \in U, \quad k \in [0,\, N-1] \label{ocp:box_u}                                                  \\
                      %
                      \mathbf{\bar{x}}(N)                                             & = p(\bar{s}) \label{ocp:terminal_constraints}
                      \\
                      %
                      \bar{s}                                                         & \in [0,1] \label{ocp:art_ref}                                                                    \\
                      %
                      \mathcal{B}\bigl(\mathbf{\bar{x}}(k)\bigr)\cap\mathcal{O}_i
                                                                                      & = \varnothing, \quad k \in [1,\,N],\; i \in [1,\,N_{o}]
                      \label{ocp:obstaceles_avoidance}
                  \end{align}$$

3.  Denote the obtained optimal solution $\mathbf{u}^*(\cdot)$, $\mathbf{x}^*(\cdot)$, $s^*$.

4.  Apply the control input $\mathbf{u}(n) = \mathbf{{u}}^*(0)$ to the system.

5.  Repeat until the robot reaches the final waypoint, then start over using the next path segment.

General constraints on states and control inputs for nonlinear systems are incorporated into the OCP in the form of set membership conditions, as defined in [\[ocp:box_x\]](#ocp:box_x){reference-type="eqref" reference="ocp:box_x"} and [\[ocp:box_u\]](#ocp:box_u){reference-type="eqref" reference="ocp:box_u"}, respectively. Furthermore, static obstacle avoidance can be also considered in the optimization problem by considering constraints [\[ocp:obstaceles_avoidance\]](#ocp:obstaceles_avoidance){reference-type="eqref" reference="ocp:obstaceles_avoidance"}. Where $\mathcal{B}$ represents the robot's footprint, and $\mathcal{O}_i$ denotes the $i$-th obstacle in the environment.

# Results {#sec:results}

The proposed system is evaluated in a simulated agricultural scenario, where a mobile robot navigates to a set of target weeds. The results are presented in terms of path planning and waypoint-following performance metrics, including path length, target reaching, smoothness, and curvature constraints adherence. A comparative analysis is conducted between the proposed DTSP planner with angle discretization and the decoupled approach based on the Alternating Algorithm (AA), see Section [1.1](#subsec:related_work){reference-type="ref" reference="subsec:related_work"} and [@savlaPointtopointTravelingSalesperson2005]. The results demonstrate the effectiveness of the integrated global planner and NMPC methods adapted in this work.

## Simulation Setup

The simulation scenario consists of a 2D field with a set of target weeds distributed across the area. In this phase, the global path planner generates a Dubins path that connects all target weeds in the field, while the NMPC controller optimizes the robot's trajectory to reach each detected weed accurately while adhering to constraints from the robot's kinematics and the environment.

After formulating the DTSP and transforming it into an ATSP, the problem was solved using the LKH optimizer, which is an effective implementation of the Lin-Kernighan traveling salesman heuristic [@helsgaunEffectiveImplementationLin2000].

The NMPC problem is symbolically formulated in MATLAB using the CasADi framework [@anderssonCasADiSoftwareFramework2019]. To ensure a smooth and continuously differentiable path function, the global Dubins reference path is first sampled at 5 cm intervals and then converted into a CasADi function, $p(s)$, using CasADi's linear interpolation utilities. This function is parameterized over the normalized domain $s \in [0,1]$.

In this agricultural application a differential-driven mobile robot model as described in [@siegwartIntroductionAutonomousMobile2004] is utilized: $$\begin{equation}
    \dot{\mathbf{x}} =
    \begin{bmatrix}
        \dot{x} \\
        \dot{y} \\
        \dot{\theta}
    \end{bmatrix}
    =
    \begin{bmatrix}
        v \cos(\theta) \\
        v \sin(\theta) \\
        \omega
    \end{bmatrix}
\end{equation}$$ The robot's control inputs are defined as $\mathbf{u} = [v \; \omega]^T$, where $v$ and $\omega$ represent the linear and angular velocity respectively. The output states of the robot are given by $\mathbf{x} = [x \; y \; \theta]^T$, which represent the 2D pose of the robot, including its position $(x, y)$ and orientation $\theta$. This mathematical model is employed for both the simulation and prediction models, without taking into account possible process or measurement noise.

The prediction model is integrated using the fourth-order Runge-Kutta (RK4) method to compute the state evolution over each discretization interval. The continuous-time OCP is discretized via direct multiple shooting, which converts it into a nonlinear programming (NLP) problem that is then solved with the Interior Point Optimizer (IPOPT) [@wachterImplementationInteriorpointFilter2006].

The NMPC problem is parameterized by a sampling time of $\Delta t = 0.1$ seconds and a prediction horizon of $N = 20$. The weight matrices are defined as $$\begin{equation*}
    \begin{aligned}
        Q   & = \operatorname{diag}(0.1,\ 0.1,\ 0.01),\, \\
        R   & = \operatorname{diag}(0.1,\ 1.0),\,        \\
        q_s & = 10^{4}.
    \end{aligned}
\end{equation*}$$ The minimum turning radius constraint, required in this application, is enforced by the inequality constraint $$\begin{equation*}
    \bar{v}(k) \geq r_{\text{min}} |\bar{\omega}(k)|
\end{equation*}$$ which is added to the optimal control problem. Furthermore, control inputs box constraints $$\mathbf{u}_{min} \leq  \mathbf{\bar{u}}(k)  \leq
    \mathbf{u}_{max}$$ are taken into account to limit the robot's linear and angular velocity. Finally, to ensure smooth motion, in such agricultural application it is convenient to also consider constraints on the rate of change of control inputs (i.e., acceleration of the robot) $$\Delta \mathbf{u}_{min} \leq  \mathbf{\bar{u}}(k) - \mathbf{\bar{u}}(k-1)  \leq
    \Delta \mathbf{u}_{max}.$$ The robot considered in this work has maximum linear velocity of 0.5 m/s and a maximum angular velocity of 1.9 rad/s. The rate of change constraints are defined as a fraction of the maximum control values, allowing adaptation based on operational requirements (e.g., $\mathbf{u}_{max}/n$), where $n \in [1,\,N_{o}]$

## Simulation Results

The test scenario illustrated in Fig. [1](#fig:dtsp_compare){reference-type="ref" reference="fig:dtsp_compare"} evaluates the performance of the proposed DTSP global path planner (Fig. [\[fig:case_a\]](#fig:case_a){reference-type="ref" reference="fig:case_a"}) against a DTSP planner from the decoupled category (Fig. [\[fig:case_b\]](#fig:case_b){reference-type="ref" reference="fig:case_b"}), as discussed in Section [1.1](#subsec:related_work){reference-type="ref" reference="subsec:related_work"}. This planner utilizes the Alternating Algorithm (AA) to determine the waypoints orientations, whereas the DTSP method applied in this work incorporates 10 angle discretization levels for each waypoint. Both planners were tested on the same dataset, consisting of 150 target weeds distributed across approximately 20$\times$`<!-- -->`{=html}60 square meters field, with a vehicle turning radius constraint of 0.5 meters.

In both cases, the proposed NMPC algorithm was able to optimize the reference paths and accurately reach each waypoint, while still respecting the turning radius constraints required to protect the soil and grass from damage. A steady-state error of no more than 0.05 meters was achieved at each target pose.

:::: {#fig:dtsp_compare .figure latex-placement="thpb"}
::: caption
Comparison of Dubins tours (red arrows) for approximately 20 m $\times$ 60 m field containing 150 target weeds (green stars), with a vehicle turning radius of 0.5 m. The proposed coupled DTSP-based planner [\[sub@fig:case_a\]](#sub@fig:case_a){reference-type="ref" reference="sub@fig:case_a"} chooses a different order of the waypoints, thereby allowing for a smoother path, whereas the decoupled DTSP-based planner [\[sub@fig:case_b\]](#sub@fig:case_b){reference-type="ref" reference="sub@fig:case_b"} results in a less optimal path with redundant loops. In both cases, the NMPC closed-loop state trajectory (blue arrows) successfully reaches all waypoints while locally optimizing motion by smoothing sharp turns and taking efficient shortcuts when beneficial.
:::
::::

The proposed DTSP planner presented in Fig. [\[fig:case_a\]](#fig:case_a){reference-type="ref" reference="fig:case_a"}, achieved a total path length of 323.49 meters, outperforming the decoupled approach shown in Fig. [\[fig:case_b\]](#fig:case_b){reference-type="ref" reference="fig:case_b"}, which resulted in a path length of 384.58 meters, i.e. nearly 19% longer. For reference, the shortest possible path computed by only solving the ETSP without considering curvature constraints was 314.20 meters.

As observed in Fig. [\[fig:case_b\]](#fig:case_b){reference-type="ref" reference="fig:case_b"}, the path generated by the DTSP planner using the alternating algorithm is suboptimal, characterized by numerous loops that are necessary to reach the next waypoint given the curvature constraints. In contrast, the proposed DTSP planner with 10 angle discretization levels, as shown in Fig. [\[fig:case_a\]](#fig:case_a){reference-type="ref" reference="fig:case_a"}, leads to a different order of the waypoints, allowing for a significantly smoother path. This path connects all targets with hardly any redundant loops, which can effectively guide the NMPC towards the targets. Experiments with angle discretization, starting from three orientations per waypoint and incrementally increasing, showed that higher discretization levels generally reduced path cost but also increased computational time. This trade-off depends on factors such as the density of targets and the turning-radius constraints. Furthermore, the benefits of using a coupled approach quickly grow with a higher target density and a larger minimum turning radius.

As depicted in Fig. [1](#fig:dtsp_compare){reference-type="ref" reference="fig:dtsp_compare"}, the robot successfully navigates all target weeds accurately while adhering to curvature constraints. Thereby the proposed NMPC does not strictly follow the reference path but locally optimizes the trajectory based on the NMPC cost function. E.g., to protect the soil, tight turns are discouraged, leading to wider turns to smooth out tight turns from the global planner, as long as this does not significantly increase the path length. On the other hand, it takes shortcuts by making tighter turns when this helps to significantly reduce the travel distance. This local planning behavior of the NMPC can be tuned by adjusting the prediction horizon length, the cost function weights, and the allowable turning radius.

# Summary and Outlook {#sec:Summary_Outlook}

This paper has presented a practical autonomous navigation framework for non-holonomic mobile robots in agricultural applications. Given target coordinates, the proposed framework integrates a global path planner based on a coupled DTSP formulation with an NMPC-based motion planning and control strategy to generate feasible reference paths and compute optimal control inputs that satisfy both the robotic system constraints and the operational demands of the agricultural environment.

The system's performance was validated through a comparative analysis with a reference path generated by a global planner based on a decoupled DTSP formulation, demonstrating the advantages of the applied DTSP approach and its effectiveness as a reference input for the local motion planner and controller. By optimally selecting a feasible artificial reference and corresponding terminal constraint along the planned path, the NMPC methodology smooths out sharp turns, identifies efficient shortcuts, and ensures precise waypoint navigation while maintaining overall system stability under various constraints.

Future research will focus on enhancing local motion planning by considering complex obstacle scenarios, including moving humans, animals, other robots and machinery into the NMPC's OCP formulation for safe, real-time adaptation to moving agents. Experimental field validation is planned under varying terrain conditions to address challenges arising from process and measurements noise, bridging the gap between simulation and practical agricultural robotics.

[^1]: This work was supported by the BMBF, Deutsche Agentur für Transfer und Innovation within the program DATIpilot.

[^2]: Mahmoud Ghorab and Matthias Lorenzen are with Institute for Applied Artificial Intelligence and Robotics (IKR), Kempten University of Applied Sciences, Bahnhofstraße 61, 87435 Kempten (Allgäu), Germany `{mahmoud.ghorab, matthias.lorenzen}@hs-kempten.de`
