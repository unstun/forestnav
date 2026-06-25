---
citation_key: Yang2023Sparse
arxiv_id: 2308.15931
arxiv_url: https://arxiv.org/abs/2308.15931
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:05:11Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Tethered Path Planning, Self-entanglement-free Path Planning
:::

# Introduction

:::: {#fig:fig1 .figure latex-placement="t"}
::: caption
Examples of various tethered robot paths to visit the predefined goals, depicted as small circles. The base point anchoring the tether is depicted as a triangle. For simplicity, no obstacle is presented, and the maximum tether length constraint is ignored. The mobile unit (depicted as a polygon) is differential-driven, with the tether (blue curve) being hooked (a)(b) to the back and (c)(d) to the right. (a) In this case, the circular path is valid for an untethered robot but not suitable for a tethered robot. The tether would contact the rear wheel after the robot visits goal $2$, leading to self-entanglement. (b) To avoid self-entanglement, the robot, after visiting goal $2$, executes a backward motion to an intermediate pose that allows for the subsequent self-entanglement-free path. (c) In this case, for a robot whose tether extends to the right, even a straight forward path would result in self-entanglement. The admissible tether retracting orientation at the tether-robot anchoring point is depicted by the notch on the robot footprint. (d) A self-entanglement-free resulting path for the case described in (c).
:::
::::

Tethered robots, which are mobile robots equipped with a tether anchoring to a fixed base point, have natural advantages in maintaining stable communication links and ensuring continuous power and material supplies. This makes them highly suitable for executing energy-intensive tasks and operating in environments where wireless communication is unreliable or unfeasible. This is often the case such as sewer pipe inspection [@Nassiraei2007Concept], highway maintenance [@Hong1997Tethered], coverage tasks [@Shnaps2014Online] [@Mechsy2017Novel] [@Sharma20192], disaster recovery missions [@Pratt2008Use], mountain climbing tasks [@Abad2011Motion] [@Tanner2013Online], and exploration tasks [@Shapovalov2020Exploration]. However, in most of these scenarios, the deployed mobile robots were not originally designed for tethered applications. As a result, they lack an omni-directional tether-robot anchoring mechanism. In this case, a phenomenon referred to as *self-entanglement* arises which impacts the safety of the tethered robot movement: If the mobile unit executes cyclic rotations, then the tether would entangle with the mobile unit. The self-entanglement problem fundamentally stems from the inappropriate relative angle between the robot's heading direction and the tether stretching direction. See Fig. [1](#fig:fig1){reference-type="ref" reference="fig:fig1"} for the visual illustration of how the tether orientation may influence the movement of a tethered differential-driven robot with the aim to avoid self-entanglement. Furthermore, due to the force of gravity, physically the tether will always sag. Consequently, self-entanglement may further translate to the wheels rolling over the tether, resulting in unexpected tethered robot configurations (with a self-crossing tether shape) and causing damage to the tether structure. Addressing this specialised path planning problem for tethered robots, referred to as the *Self-Entanglement-Free Tethered Path Planning* (SEFTPP) task, is the objective of this paper.

Given a self-entanglement-free (SEF) tethered robot configuration, the admissible robot motion must be conditioned by not only established modules like collision avoidance, differential-driven robot kinematic constraints, and maximum tether length constraint, but also by the tether stretching direction. The necessity of maintaining the SEF property makes the SEF path solution non-intuitive even for seemingly straightforward tasks, as illustrated by the SEF paths in Fig. [\[fig:fig1b\]](#fig:fig1b){reference-type="ref" reference="fig:fig1b"} and Fig. [\[fig:fig1d\]](#fig:fig1d){reference-type="ref" reference="fig:fig1d"}. It is noteworthy that all existing works in the field of tethered robot planning (to be recounted in Section [2](#section_related_works){reference-type="ref" reference="section_related_works"}) have assumed scenarios involving either particle robots or omni-directional (2D) robots. In these cases, the self-entanglement problem was safely ignored. However, such assumptions are far from practical when dealing with real-world challenging applications. And one can expect that, restricting the admissible robot heading orientation will significantly constrain the range of valid movements, making the SEFTPP problem non-trivial and more complex compared to untethered planning problems.

This work advocates for reporting the first solution to the guaranteed self-entanglement-free path for a tethered differential-driven robot. The proposed algorithm departs from all existing tethered robot planners. It explicitly takes into account the orientation difference between the robot's heading direction and the tether stretching direction, which naturally motivates a constrained path planner to solve the SEFTPP problem. The contributions of this paper can be summarised as:

1.  The modelling of the SEFTPP problem into a constrained path planning problem, with explicit consideration of the relative angle between the robot's heading direction and the tether stretching direction.

2.  A constrained searching-based SEFTPP solution for tethered differential-driven mobile robots.

3.  The proofs demonstrating that under specific conditions during the node expansion phase of the searching-based path planner, the validity of the endpoint configurations of a primitive path ensure the validity of all intermediate waypoint configurations. As a result, there is no necessity to explicitly construct any waypoint configuration, nor is there a need to check their validity individually. This property is denoted as the *sparsity* of the waypoint configuration validity checking.

4.  The open-sourcing [^3] of the algorithm.

The remainder of this paper is organised as follows. Section [2](#section_related_works){reference-type="ref" reference="section_related_works"} reviews and contextualises the problem within the existing literature. Section [3](#section_problem){reference-type="ref" reference="section_problem"} formally models the SEFTPP problem. Section [4](#section_algorithm){reference-type="ref" reference="section_algorithm"} delves into details to describe the proposed solver to generate the SEFTPP solution. The sparsity of waypoint configuration validity checking during node expansion is discussed in Section [5](#section:sparsity){reference-type="ref" reference="section:sparsity"}. Experimental illustrations and comparisons are collected in Section [6](#section_exp){reference-type="ref" reference="section_exp"}, with final concluding remarks gathered in Section [7](#section_conclusion){reference-type="ref" reference="section_conclusion"}.

# Related Works {#section_related_works}

The *tethered path planning* (TPP) task has been intensively investigated in the past decades. Numerous applications of tethered robots have been explored in various domains [@Hong1997Tethered] [@Nassiraei2007Concept] [@Pratt2008Use] [@Abad2011Motion] [@Tanner2013Online] [@Shnaps2014Online] [@Shapovalov2020Exploration]. Main concentrations have been paid on constructing the shortest tethered robot path complying with the maximum tether length constraint. It has been observed [@Bhattacharya2012Topological] that the tether states will be non-homotopic if the robot reaches the same goal following paths in different topological routes, and the shortest path for an untethered robot is in all likelihood untrackable by a tethered robot.

Early work confined their scope to polygonal environments [@Teshnizi2014Computing] [@Salzman2015Optimal] so that the algorithmic complexity can be calculated [@Xavier1999Shortest] [@Brass2015Shortest] as a polynomial of the number of straight segments in the initial tether state and the number of obstacle vertices. In recent years, a notable advancement is the ability to distinguish between different tethered robot configurations with the same mobile unit pose. This is achieved by calculating the homotopy classes of the tether states. And the most popular solutions to find the tethered robot path are based on the path-finding within the pre-calculated set of all valid configurations, referred to as the homotopy augmented graph [@Bhattacharya2012Topological]. Later, with the utilisation of a locally obstacle-free shortest path planner, the deformation of robot tether becomes easier to estimate. This improvement enhances the efficiency of the pre-calculation process [@Kim2014Path] [@Kim2015Path]. Moreover, [@Teshnizi2014Computing] pre-computed the reachable cell for tethered robots, which improves the efficiency of querying process during the planning phase.

It is important to note that all the previously mentioned works have focused on the scenarios involving either particle robots or omni-directional robots. In these studies, the primary consideration was the tether entanglement with environmental obstacles, ignoring the self-entanglement which is the main motivation of this work. In this paper, special treatment of the tether self-entanglement will be incorporated into the proposed algorithm, leading to the generation of robot paths that are guaranteed to be free from self-entanglement, filling in the gap between simulated tethered path planners and real-world execution.

# Problem Modelling {#section_problem}

:::: {#fig:robot .figure latex-placement="t"}
![](Yang2023Sparse_figs/robot_phi_to_Phi.png){width="35%"}

::: caption
Illustration of definitions and notations.
:::
::::

This section introduces notations for the environmental settings and the kinematics of the tethered differential-driven robot, along with the formulation of the self-entanglement-free tethered path planning (SEFTPP) problem.

## Definitions and Robot Kinematics

Let $M\subset \mathbb{R}^2$ represent the environment where the tethered robot operates. The footprint of the robot's mobile unit is assumed as a polygon. The anchoring point of the tether on the robot, defined within the robot's egocentric frame, is denoted as $s$. The other endpoint of the tether is anchored at a fixed base point in the environment, which is denoted as $b$. The tether is assumed to be taut, allowing its shape to be characterised by a sequence of contact points between the tether and the vertices of environmental obstacles. The last tether-obstacle contact point is denoted as $o$. Please refer to Fig. [2](#fig:robot){reference-type="ref" reference="fig:robot"} for a visual illustration of these notations.

::: definition
**Definition 1**. *(Configuration) The configuration, denoted as $c$, of a tethered differential-driven robot consists of two components: the pose of the differential-driven robot and the shape of the tether. It is represented as: $$\begin{equation}
c = \{x, y, \theta, O\}
\end{equation}$$ where $x$, $y$, and $\theta$ represent the $SE(2)$ pose of the mobile unit of the tethered robot, and $O$ maintains a record of the tether-obstacle contact points, from the base point $b$ to the last tether-obstacle contact point $o$.*
:::

::: definition
**Definition 2**. *(Relative Angle) Under the assumption that the tether remains taut, the direction of tether retraction, denoted as $\phi$, is estimated as: $$\begin{equation}
\phi = \frac{\vec{so}}{\parallel \vec{so}\parallel}
\end{equation}$$ then $\Phi$ is defined as the relative angle between the tether retracting direction and the robot's heading direction, $$\begin{equation}
\Phi = \phi - \theta
\end{equation}$$*
:::

Given the geometric structure of the tethered robot, without an omni-directional tether-robot anchoring mechanism, the range of admissible relative angles, denoted as $\Phi$, is not $[0, 2\pi)$ but falls within an interval denoted as $[\Phi_1, \Phi_2]$. This forms the basis of the self-entanglement-free property, as discussed in the next subsection.

## Self-Entanglement-Free Tethered Path Planning

Given the initial configuration of the robot $c_s = (x_s, y_s, \theta_s, O_s)$ and the goal location $p_{\rm goal}=(x_g, y_g)$, the solution to the SEFTPP problem is a curve of mobile unit waypoints, represented as: $$\begin{equation}
\begin{aligned}
\alpha: [0, 1]\rightarrow &\mathbb{R}^2,\ t\mapsto (x(t), y(t))\in \mathbb{R}^2, t\in [0, 1]\\
&s.t.\ x(0) = x_s, y(0) = y_s, x(1) = x_g, y(1) = y_g
\end{aligned}
\end{equation}$$ where each *induced* configuration [^4] $(x(t), y(t), \theta(t), O(t))$ is *valid*, i.e., subject to the following conditions:

1.  **(Collision-free):** The mobile unit at $(x(t), y(t), \theta(t))$ remains free of collisions.

2.  **(Tether-length-admissible, TLA):** The length of tether remains shorter than the maximum allowable tether length.

3.  **(Non-selfcrossing, NS):** The robot is prohibited from traversing across the tether.

4.  **(Self-entanglement-free, SEF):** The SEF condition is defined by the boundedness of the *relative angle function* which is defined as $$\begin{equation}
    \label{eqn:Phi}
    \Phi(t) = \arctan\left( \frac{o_y(t) - \tilde{y}(t)}{o_x(t)-\tilde{x}(t)} \right) - \theta(t),\ t\in [0, 1]
    \end{equation}$$ where $(\tilde{x}(t), \tilde{y}(t))$ is the position of $s$ and $(o_x(t), o_y(t))$ is the position of $o$. The SEF condition mandates that this function is bounded by the admissible interval: $$\begin{equation}
    \label{equ:sef}
    \Phi_1 \leq {\rm wrapToPi}(\Phi(t)) \leq \Phi_2, \forall t\in [0, 1]
    \end{equation}$$

It should be noted that SEFTPP has been framed as a path planning problem with multiple potential goals. In this context, the goal is represented not as a single configuration but as a 2D location in the environment. There can be multiple "goal configurations\" that correspond to a given "goal location\". The path planning task is deemed finished as soon as the robot reaches any of these goal configurations. This setting is justified because, regarding the target configuration of the tethered robot, the admissibility of the robot's final heading direction $\theta$ (if assigned) is inherently determined by the retracting direction of the tether. However, the final shape of the tether, which is further constrained by the tether-length-admissible property, cannot be intuitively determined based solely on human empirical knowledge. Therefore, it is a reasonable practice for users to provide a goal location without fully specifying a goal configuration.

:::: algorithm
::: algorithmic
Map $M$, Initial configuration $c_0$, Goal location $p_{\rm goal}$, Base point $b$, Maximum tether length $L$, Resolution $x_{\rm res}, y_{\rm res}, \theta_{\rm res}$ Resultant path $R$ % Initialize Data Structure $\{\zeta_i\}$ = getRepresentativePointOfObstacles($M$) $n_0$ = initialiseNode($c_0$)[]{#line:init_start label="line:init_start"} $[x_d, y_d, \theta_d]$ = getIndex($n_0, x_{\rm res}, y_{\rm res}, \theta_{\rm res}$) $V(x_d, y_d, \theta_d).{\rm push}(n_0)$ % grid-based discretisation $Q.{\rm push}(n_0)$ % The priority queue[]{#line:init_end label="line:init_end"} $n_{\rm cur}$ = $Q.{\rm pop}()$ $R$ = \[tracePath($V$, $n_{\rm cur}$);$p_{\rm goal}$\] **return** $R$ $N_{\rm succ}$ = nodeExpansion($n_{\rm cur}$)[]{#line:getSuccessor label="line:getSuccessor"} $[x_{\rm ds}, y_{\rm ds}, \theta_{\rm ds}]$ = getIndex($n_{\rm succ}, x_{\rm res}, y_{\rm res}, \theta_{\rm res}$) $n_{\rm homo}$ = findHomoNode($n_{\rm succ}$,$V(x_{\rm ds}$,$y_{\rm ds}$,$\theta_{\rm ds})$)[]{#line:findSimilarNode label="line:findSimilarNode"} $Q.{\rm push}(n_{\rm succ})$ $V(x_{\rm ds}, y_{\rm ds}, \theta_{\rm ds}).{\rm push}(n_{\rm succ})$ remove $n_{\rm homo}$ from $Q$ $Q.{\rm push}(n_{\rm succ})$ $V(x_{\rm ds}, y_{\rm ds}, \theta_{\rm ds}).{\rm push}(n_{\rm succ})$ $R = \varnothing$ $R$
:::
::::

# Algorithm {#section_algorithm}

In this section, the SEFTPP problem is effectively addressed using a constrained path searching algorithm. The pseudo code of the proposed algorithm is shown in **Algorithm [\[alg:main_planner\]](#alg:main_planner){reference-type="ref" reference="alg:main_planner"}**.

## Node Definition

The proposed algorithm constructs a searching tree of valid tethered robot configurations that satisfy all the constraints stated in the previous subsection. The path searching process is similar to the constrained searching-based optimal path planner [@Dolgov2010Path] [@Bhattacharya2012Topological]. To formally present this, the term *node* is defined as follows:

::: definition
**Definition 3**. *(Node) A *node* during the pathfinding consists of the following elements: $$\begin{equation}
\begin{aligned}
n = \{&\{i, x, y, \theta, O, s, \phi, h\} (\mbox{configuration related}), \\
&\qquad \{gCost, hCost, i_{\rm prev}\} (\mbox{searching-tree related}), \\
&\qquad\qquad \{steer, dir\} (\mbox{cost related})\} \\
\end{aligned}
\end{equation}$$ where $i$ is the index of the node, $\{x, y, \theta, O\}$ is the pose of the mobile unit. The location of tether-robot anchoring point $s$ and the tether stretching orientation $\phi$ are derived variables from the robot configuration. $h$ is the $h$-signature of the robot configuration, which is also a derived variable and whose calculation will be elaborated upon later. Other components are introduced specifically for node expansion, which are presented in the next subsection.*
:::

## Node Expansion

At the beginning of the algorithm, a representative point for each obstacle is firstly distinguished, denoted as $\zeta_1, \cdots, \zeta_n$. Then, parallel non-overlapping rays are constructed, denoted as $r_1, \cdots, r_n$. The initial configuration of the robot (which must satisfy all constraint) is employed to construct the first node. This node, denoted as $n_0$, is constructed with cost-to-move $n_0.gCost = 0$ and $h$-signature $n_0.h = \varnothing$. It is then pushed into a priority queue. In each iteration, the node $n_{\rm cur}$ with the lowest cost is popped from the queue, and all of its child nodes are generated. Multiple primitive paths may be applicable. In the particular SEFTPP case, given that in-situ rotational movements rarely comply with the SEF constraint, the primitive paths are selected as car-like circular paths, parameterised by $dis$ (path length), $dir$ (where $1$ represents forward and $-1$ represents backward), and $steer$ (which determines the turning radius). The validity of a primitive movement is rigorously examined, with "validity\" encompassing not only the collision-free property, tether-length-admissibility, tether non-selfcrossing property, and self-entanglement-free property of the child node, but also extending to all intermediate waypoint configurations along the primitive path. The set of valid child nodes is denoted as $N_{\rm succ}$. The node expansion process is detailed in **Algorithm [\[alg:succ\]](#alg:succ){reference-type="ref" reference="alg:succ"}** [^5].

:::: {#fig:hsign .figure latex-placement="t"}
![](Yang2023Sparse_figs/hsignature.png){width="38%"}

::: caption
Illustration of $h$-signature calculation. In this example, the word representation of the green path and the blue path are "$r_2r_2^{-1}r_2r_2^{-1}r_1^{-1}r_1r_2r_3$\" and "$r_2r_3$\", respectively, which are equivalent under the process of word reduction. Consequently, the two paths are homotopic. If the tethered robot moves along the two paths, the configurations will be exactly the same.
:::
::::

For each valid child node, elements of the robot configuration is calculated, denoted as $n_{\rm succ}.x$, $n_{\rm succ}.y$, $n_{\rm succ}.\theta$, $n_{\rm succ}.O$. If the primitive path traverses across $r_i$ from left to right, then $r_i$ is appended to the $h$-signature, whilst $r_i^{-1}$ is appended if the crossing is from right to left. If $r_i$ and $r_i^{-1}$ are adjacent, then they are reduced. Through this process, $n_{\rm succ}.h$ is calculated based on $n_{\rm cur}.h$. See Fig. [3](#fig:hsign){reference-type="ref" reference="fig:hsign"} for illustration. The author is referred to [@Kim2014Path] for a more theoretical explanation. Various non-negative movement cost functions may be applicable for calculating the cost. In our implementation, the cost is calculated as a composite function that considers the robot's travelling distance, changes in steering angle, and alternations in moving direction, as $$\begin{equation}
\begin{aligned}
n_{\rm succ}.gCost = &n_{\rm cur}.gCost + k_1 dis\\
&+ k_2\parallel n_{\rm succ}.steer - n_{\rm cur}.steer\parallel \\
&+ k_3\parallel n_{\rm succ}.dir - n_{\rm cur}.dir\parallel\\
&\qquad \qquad k_1, k_2, k_3 > 0
\end{aligned}
\end{equation}$$ where $k_1$, $k_2$, and $k_3$ are parameters. The index of the parent node is stored in the child node as $n_{\rm succ}.i_{\rm prev}$. The estimated cost-to-go, denoted as $n_{\rm succ}.hCost$, is calculated as the Euclidean distance to the goal. Nodes are managed in a resolutionally complete manner, meaning that the space of the mobile unit's poses $(x, y, \theta)$ is discretised based on pre-defined grid solutions $x_{\rm res}$, $y_{\rm res}$, $\theta_{\rm res}$. In cases where multiple nodes with the same $h$-signature reside in the same grid, only the one with the lowest cost is preserved. However, it is permitted to have multiple nodes with pairwise distinct $h$-signature within the same grid.

The algorithm iteratively expands the least-cost node in the queue, until it reaches the goal location. A valid path is then reported by back-tracing through the nodes following the child-parent relation.

## Discussions on Completeness and Distance-Optimality

**Completeness.** The completeness property of a path planning algorithm means that the algorithm is guaranteed to either find a resultant path or to determine that no path exists in finite time. The completeness of the proposed algorithm follows the similar vein as that of the Hybrid A\* [@Dolgov2010Path] algorithm. By discretising the map into small grids (regarding $x$, $y$, and $\theta$), allowing the existence of multiple nodes with distinct $h$-signature within the same node, and choosing short primitive paths, the algorithm can effectively find a resultant path within a reasonable computation time. However, there is no formal guarantee that the searching branch of the proposed algorithm can explore all grids within the same connected component of the grid containing the initial node.

**Optimality.** The proposed algorithm is sub-optimal. Evaluating the quality of the resultant path involves two perspectives: local (among all paths within the same homotopy class of paths) and global (among the best-possible paths found in each individual homotopy class). From a local standpoint, the optimality of the proposed algorithm is sub-optimal. This is because if multiple nodes in the same grid have homotopic tether shapes, the proposed algorithm only preserves the least-cost one, disregarding the others. This behaviour aligns with observations made in prior searching-based algorithms [@Dolgov2010Path]. From the global perspective, the proposed algorithm maintains path searching branches in all homotopy class of paths, enabling it to identify and compare sub-optimal paths across multiple homotopy classes and select the best one.

# Sparse Waypoint Validity Checking {#section:sparsity}

The proposed path searching algorithm adopts straight movement and arc-like movements as primitive paths. However, a critical concern is how the validity of the primitive paths can be efficiently validated. The most straightforward strategy is discretising the primitive path into a sufficiently dense sequence of waypoint configurations of the tethered robot, based on a set distance resolution, and verifying the validity of each individual waypoint configuration. Nonetheless, this process is extremely inefficient due to the computational cost associated with the explicit calculation of the tether shape for each waypoint configuration. Given that the validity checking module is executed during the expansion of every child node, the inefficiency of this module directly impacts the efficiency of the overall algorithm. In this section, it is proven that under specific conditions, there is no necessity to examine the validity of the waypoint configurations: they are guaranteed to be valid. This is referred to as the *sparsity* of the validity checking.

To simplify the discussions presented in this section, our scope is limited to the situations where the contact points between the tether and obstacles remain unchanged throughout the primitive motion. In this regard, we first show the existence of a method for identifying the constancy of tether-obstacle contact points.

::: lemma
**Lemma 4**. *(Unchanged Tether-Obstacle Contact Points) Let the starting configuration be $c_0 = (x_0, y_0, \theta_0, O_0)$ and the ending configuration be $c_1 = (x_1, y_1, \theta_1, O_1)$. If*

1.  *$O_0$ and $O_1$ are the identical. The last tether-obstacle contact point is referred to as $o$.*

2.  *Using $o$ and the path of $s$ to generate a convex hull, this convex hull is obstacle-free.*

*then the tether-obstacle contact points will remain unchanged throughout the primitive motion.*
:::

::: proof
*Proof.* Because the final part of the tether (between $o$ and $s$) always resides within this convex hull, it will not encounter any obstacle. ◻
:::

## The Sparsity of Validity Checking

Typically, there are four properties that must be checked to determine whether a primitive path is valid: the collision-free property, the non-selfcrossing (NS) property, the self-entanglement-free (SEF) property, and the tether-length-admissible (TLA) property.

To begin with, verifying the collision-free property only involves the verification that the footprint of the mobile unit does not intersect with any obstacle during the motion. It is essentially the collision checking module used for untethered differential-driven robots which has been an established module. Next, it is observed that the starting segment of the tether (from the base point $b$ to $o$) remains unchanged throughout the motion. Therefore, verifying the non-selfcrossing property is simply implemented as verifying the collision-free property between the robot path and the starting part of the tether (from $b$ to $o$). The non-selfcrossing starting configuration implies that the mobile unit will hit the static part of the tether before the tether becomes selfcrossing. See Fig. [4](#fig:selfcrossing){reference-type="ref" reference="fig:selfcrossing"} for illustration.

Checking the SEF property and the TLA property of a primitive path are challenging because these tasks are directly related to the deformed shape of the final part of the tether (from $o$ to $s$). As a result, the kernel of the sparsity of the validity checking is exploring conditions under which the properties of the primitive path can be fully characterised by the endpoint configurations. This is formally presented as follows.

:::: {#fig:selfcrossing .figure latex-placement="t"}
![](Yang2023Sparse_figs/selfcrossing_motion.png){width="40%"}

::: caption
Illustration of a selfcrossing robot path.
:::
::::

::: {#def:sparsity .definition}
**Definition 5**. *(Sparsity of Validity Checking) Let the robot path be a straight path or a circular path. The starting configuration is given as $c_0 = (x_0, y_0, \theta_0, O)$. The ending configuration is denoted as $c_1$. The sparsity of validity checking is defined as the sufficiency that $$\begin{align}
c_0\mbox{ and }c_1\mbox{ are SEF}&\Rightarrow \mbox{ all waypoints are SEF}\label{eqn:sef_condition}\\
c_0\mbox{ and }c_1\mbox{ are TLA}&\Rightarrow \mbox{ all waypoints are TLA}\label{eqn:tla_condition}
\end{align}$$*
:::

When the sparsity is established, there is no requirement to explicitly construct waypoint configurations, leading to significant computational time savings. The circumstances under which the sparsity is confirmed, in other words, the sufficient conditions for the sparsity, are discussed in the subsequent subsections. To enhance clarity, the following notations are formally recalled.

::: definition
**Definition 6**. *($\Delta x$, $\Delta y$) The location of the tether-robot contact point $s$ in the robot's egocentric frame is denoted as ($\Delta x$, $\Delta y$).*
:::

::: definition
**Definition 7**. *($\tilde{x}$, $\tilde{y}$) The location of $s$ in the world frame is denoted as ($\tilde{x}$, $\tilde{y}$).*
:::

::: definition
**Definition 8**. *($o_x$, $o_y$) The location of the last tether-obstacle contact point $o$ in the world frame is denoted as ($o_x$, $o_y$).*
:::

:::: {#fig:primitive_motions .figure latex-placement="t"}
::: caption
Illustration of the starting configuration and the ending configuration of two primitive paths with an unchanged last tether-obstacle contact point.
:::
::::

## The Monotonicity of Relative Angle Function {#sec:mono_SEF}

On noticing the significance of endpoint configurations in a primitive path, it is natural to consider the cases when the relative angle function and the tether length function are monotonic. Taking $\Phi$ as an example. If $\Phi$ is monotonic and the boundary values of $\Phi$ are within the admissible interval $[\Phi_1, \Phi_2]$, then all values of $\Phi$ also lie within the admissible interval. In other words, the monotonicity of the relative angle function is a sufficient condition that makes Eqn. ([\[eqn:sef_condition\]](#eqn:sef_condition){reference-type="ref" reference="eqn:sef_condition"}) correct.

As an introductory proposition, the monotonicity of the relative angle function when the robot path is a straight path is proven in detail.

::: {#thm:SEF_Straight .theorem}
**Theorem 9**. *(Relative Angle Monotonicity, Straight) Let the robot path be a Straight path. Then the relative angle function is monotonic.*
:::

::: proof
*Proof.* See Fig. [5](#fig:primitive_motions){reference-type="ref" reference="fig:primitive_motions"} for illustration. The robot path is parameterised as $$\begin{align}
x(t) &= x_0 + t\cos\theta_0\\
y(t) &= y_0 + t\sin\theta_0\\
\theta(t) &= \theta_0
\end{align}$$ where $t$ is the arc-length parameter, and $t_{\rm max}$ is the length of the straight path. Then, the path of of $s$ is $$\begin{align}
&\tilde{x}(t) = x_0 + t\cos\theta_0 + \cos\theta_0\Delta x - \sin\theta_0\Delta y\\
&\tilde{y}(t) = y_0 + t\sin\theta_0 + \sin\theta_0\Delta x + \cos\theta_0\Delta y
\end{align}$$ The relative angle function is expressed as follows $$\begin{equation}
\Phi(t) = \arctan\left( \frac{o_y - \tilde{y}(t)}{o_x-\tilde{x}(t)} \right) - \theta(t),\ t\in (0, t_{\rm max})
\end{equation}$$ Calculating the derivative of $\tilde{x}$, $\tilde{y}$, and $\theta$ with respect to $t$ gives $$\begin{align}
\frac{d\tilde{x}}{dt} &= \cos\theta_0\\
\frac{d\tilde{y}}{dt} &= \sin\theta_0\\
\frac{d\theta}{dt} &= 0
\end{align}$$ The derivative of $\Phi$ is calculated as $$\begin{equation}
\frac{d\Phi}{dt} = \frac{-\frac{d\tilde{y}}{dt}(o_x-\tilde{x})+\frac{d\tilde{x}}{dt}(o_y-\tilde{y})}{(o_y - \tilde{y})^2 + (o_x - \tilde{x})^2} -\frac{d\theta}{dt}
\end{equation}$$ Before we advance further, it should be noted that we are only interested in the monotonicity of $\Phi$, specifically the comparison between $\frac{d\Phi}{dt}$ and $0$. The denominator $(o_x-\tilde{x})^2 + (o_y - \tilde{y})^2$ is always a positive value, rendering it irrelevant to our focus. Hence, the denominator is safely ignored by introducing $\frac{d\tilde{\Phi}}{dt}$ as follows: $$\begin{equation}
\label{eqn:SEF_straight_tilde_Phi}
\begin{aligned}
\frac{d\tilde{\Phi}}{dt} \triangleq& \left( (o_x-\tilde{x})^2 + (o_y - \tilde{y})^2\right) \frac{d\Phi}{dt}\\
=& -\frac{d\tilde{y}}{dt}(o_x-\tilde{x}) + \frac{d\tilde{x}}{dt}(o_y-\tilde{y})\\
=& -\sin\theta_0(o_x - x_0 - t\cos\theta_0 - \cos\theta_0\Delta x+\sin\theta_0 \Delta y)\\
& +\cos\theta_0(o_y - y_0 - t\sin\theta_0 - \sin\theta_0\Delta x - \cos\theta_0 \Delta y)\\
=& -\sin\theta_0(o_x - x_0 - \cos\theta_0\Delta x+\sin\theta_0 \Delta y)\\
&+\cos\theta_0(o_y - y_0 - \sin\theta_0\Delta x - \cos\theta_0 \Delta y)
\end{aligned}
\end{equation}$$ Surprisingly, $\frac{d\tilde{\Phi}}{dt}$ is not a function of $t$, meaning that $$\begin{equation}
\frac{d\tilde{\Phi}}{dt} > 0\mbox{ or }\frac{d\tilde{\Phi}}{dt} < 0\mbox{ or }\frac{d\tilde{\Phi}}{dt} = 0,\ \forall t\in (0, t_{\rm max})
\end{equation}$$ therefore $$\begin{equation}
\frac{d\Phi}{dt} > 0\mbox{ or }\frac{d\Phi}{dt} < 0\mbox{ or }\frac{d\Phi}{dt} = 0,\ \forall t\in (0, t_{\rm max})
\end{equation}$$ In all the cases, $\Phi$ is monotonic, implying that its maximum and minimum value are achieved at endpoints. ◻
:::

For circular primitive paths, the discussion is spanned based on four different path types: Forward and Right-turning, Forward and Left-turning, Backward and Right-turning, and Backward and Left-turning.

::: {#thm:SEF_FR .theorem}
**Theorem 10**. *(Relative Angle Monotonicity, F-R) Let the robot path be a Forward and Right-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the relative angle function is monotonic if one of the following equations is satisfied, $$\begin{align}
&\frac{A^2+B^2}{\sqrt{C^2+D^2}} > \max\{\cos(t - \theta_0 - \varphi)\},\ \forall t\in (0, t_{\rm max})\label{eqn:FR_cond1}\\
&\frac{A^2+B^2}{\sqrt{C^2+D^2}} < \min\{\cos(t - \theta_0 - \varphi)\},\ \forall t\in (0, t_{\rm max})\label{eqn:FR_cond2}
\end{align}$$ where $$\begin{align}
&A = o_x - x_0 - R\sin\theta_0\\
&B = o_y - y_0 - R\cos\theta_0\\
&C = A\Delta x + BR + B\Delta y\\
&D = AR +A\Delta y - B\Delta x
\end{align}$$ and $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2+D^2}}
\end{equation}$$*
:::

::: proof
*Proof.* See **Appendix [8](#sec:appendix_SEF_FR){reference-type="ref" reference="sec:appendix_SEF_FR"}**. ◻
:::

::: {#thm:SEF_FL .theorem}
**Theorem 11**. *(Relative Angle Monotonicity, F-L) Let the robot path be a Forward and Left-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the relative angle function is monotonic if one of the following equations is satisfied, $$\begin{align}
&\frac{A^2+B^2}{\sqrt{C^2+D^2}} > \max\{\cos(t+\theta_0-\varphi)\},\ \forall t\in (0, t_{\rm max})\\
&\frac{A^2+B^2}{\sqrt{C^2+D^2}} < \min\{\cos(t+\theta_0-\varphi)\},\ \forall t\in (0, t_{\rm max})
\end{align}$$ where $$\begin{align}
&A = o_x - x_0 + R\sin\theta_0\\
&B = o_y - y_0 + R\cos\theta_0\\
&C = A\Delta x - BR + B\Delta y\\
&D = AR - A\Delta y +B\Delta x
\end{align}$$ and $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2 + D^2}}
\end{equation}$$*
:::

::: proof
*Proof.* The proof is very similar to that of **Theorem [10](#thm:SEF_FR){reference-type="ref" reference="thm:SEF_FR"}**, except many changes in the signs, which is put in **Appendix [9](#sec:appendix_SEF_FL){reference-type="ref" reference="sec:appendix_SEF_FL"}**. ◻
:::

Given the fact that a B-L path is the inverse of a F-R path, and a B-R path is the inverse of a F-L path, the following remarks are concluded.

::: {#rem:SEF_BL .remark}
**Remark 12**. *(Relative Angle Monotonicity, B-L) Let the robot path be a Backward and Left-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the relative angle function is monotonic if the condition in **Theorem [10](#thm:SEF_FR){reference-type="ref" reference="thm:SEF_FR"}** is satisfied, with the interval of $t$ being changed from $(0, t_{\rm max})$ to $(-t_{\rm max}, 0)$.*
:::

::: {#rem:SEF_BR .remark}
**Remark 13**. *(Relative Angle Monotonicity, B-R) Let the robot path be a Backward and Right-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the relative angle function is monotonic if the condition in **Theorem [11](#thm:SEF_FL){reference-type="ref" reference="thm:SEF_FL"}** is satisfied, with the interval of $t$ being changed from $(0, t_{\rm max})$ to $(-t_{\rm max}, 0)$.*
:::

## The Monotonicity of Tether Length Variation {#sec:mono_TLA}

In this subsection, sufficient conditions that guarantee the monotonicity of the tether length function are presented.

::: theorem
**Theorem 14**. *(Tether Length Monotonicity, Straight) Let the robot path be a Straight path. The length of the path is $t_{\rm max}$. Then the tether length function is monotonic if one of the following equations is satisfied, $$\begin{align}
&o_x + o_y - x_0\cos\theta_0 - y_0\sin\theta_0 - \Delta x < 0\\
&o_x + o_y - x_0\cos\theta_0 - y_0\sin\theta_0 - \Delta x > t_{\rm max}
\end{align}$$*
:::

::: proof
*Proof.* See **Appendix [10](#sec:appendix_TLA_Straight){reference-type="ref" reference="sec:appendix_TLA_Straight"}**. ◻
:::

:::: algorithm
::: algorithmic
current node $n_{\rm cur}$, Map $M$, Maximum tether length $L$, representative obstacle $\zeta$ Child node list $N_{\rm succ}$ $P$ = allPrimitives() []{#alg:node_expansion:prior_start label="alg:node_expansion:prior_start"} $N_{\rm succ} = \varnothing$ $P_{\rm waypoint}$ = generatePath($n_{\rm cur}, (steer, dir, dis)$) % $P_{\rm waypoint}$ is the $x$-$y$-$\theta$ value of the waypoints $n$ = size($P_{\rm waypoint}$) % $n$ is large is_path_valid = true is_path_valid = false **break** **continue** []{#alg:node_expansion:prior_end label="alg:node_expansion:prior_end"} []{#alg:node_expansion:valid_start label="alg:node_expansion:valid_start"} $n_{\rm mid}$ = generateConf($n_{\rm cur}.O, P_{\rm waypoint}, i$)[]{#alg:node_expansion:construction label="alg:node_expansion:construction"} is_path_valid = false **break** **continue** []{#alg:node_expansion:valid_end label="alg:node_expansion:valid_end"} $n_{\rm succ}$ = generateConf($n_{\rm cur}.O, P_{\rm waypoint}, n$)[]{#alg:node_expansion:post_start label="alg:node_expansion:post_start"} $n_{\rm succ}.gCost$ = movementCost($n_{\rm cur}$) $n_{\rm succ}.h$ = calculateHsignature$(n_{\rm succ}, \zeta)$ $N_{\rm succ}$.push_back($n_{\rm nucc}$) []{#alg:node_expansion:post_end label="alg:node_expansion:post_end"}
:::
::::

:::: algorithm
::: algorithmic
current node $n_{\rm cur}$, Map $M$, Maximum tether length $L$, representative obstacle $\zeta$ Child node list $N_{\rm succ}$ (line [\[alg:node_expansion:prior_start\]](#alg:node_expansion:prior_start){reference-type="ref" reference="alg:node_expansion:prior_start"} $\sim$ line [\[alg:node_expansion:prior_end\]](#alg:node_expansion:prior_end){reference-type="ref" reference="alg:node_expansion:prior_end"} in **Algorithm [\[alg:succ\]](#alg:succ){reference-type="ref" reference="alg:succ"}**) $n_{\rm succ}$ = generateConf$(n_{\rm cur}.O, P_{\rm waypoint}, n)$ **continue** is_o_not_changed = $\sim$isOChanged($n_{\rm cur}$, $M$, $P_{\rm waypoint}$) is_sef_guaranteed = is_o_not_changed && isSEFGuaranteed($steer$, $dis$) is_tla_guaranteed = is_o_not_changed && isTLAGuaranteed($steer$, $dis$) (line [\[alg:node_expansion:valid_start\]](#alg:node_expansion:valid_start){reference-type="ref" reference="alg:node_expansion:valid_start"} $\sim$ line [\[alg:node_expansion:valid_end\]](#alg:node_expansion:valid_end){reference-type="ref" reference="alg:node_expansion:valid_end"} in **Algorithm [\[alg:succ\]](#alg:succ){reference-type="ref" reference="alg:succ"}**) (line [\[alg:node_expansion:post_start\]](#alg:node_expansion:post_start){reference-type="ref" reference="alg:node_expansion:post_start"} $\sim$ line [\[alg:node_expansion:post_end\]](#alg:node_expansion:post_end){reference-type="ref" reference="alg:node_expansion:post_end"} in **Algorithm [\[alg:succ\]](#alg:succ){reference-type="ref" reference="alg:succ"}**)
:::
::::

::: {#thm:TLA_FR .theorem}
**Theorem 15**. *(Tether Length Monotonicity, F-R) Let the robot path be a Forward and Right-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the tether length function is monotonic if one of the following equations is satisfied, $$\begin{align}
&\cos(t-\theta_0-\varphi) < 0,\ \forall t\in (0, t_{\rm max})\\
&\cos(t-\theta_0-\varphi) > 0,\ \forall t\in (0, t_{\rm max})
\end{align}$$ where $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2+D^2}}
\end{equation}$$ where $$\begin{align}
C =& B\Delta x - AR - A\Delta y\\
D =& A\Delta x - BR - B\Delta y
\end{align}$$ and $$\begin{align}
A =& o_x - x_0 - R\sin\theta_0\\
B =& o_y - y_0 + R\cos\theta_0
\end{align}$$*
:::

::: proof
*Proof.* See **Appendix [11](#sec:appendix_TLA_FR){reference-type="ref" reference="sec:appendix_TLA_FR"}**. ◻
:::

::: {#thm:TLA_FL .theorem}
**Theorem 16**. *(Tether Length Monotonicity, F-L) Let the robot path be a Forward and Left-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the tether length function is monotonic if one of the following equations is satisfied, $$\begin{align}
&\cos(t+\theta_0 + \varphi) < 0,\ \forall t\in (0, t_{\rm max})\\
&\cos(t+\theta_0 + \varphi) > 0,\ \forall t\in (0, t_{\rm max})
\end{align}$$ where $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2+D^2}}
\end{equation}$$ where $$\begin{align}
C =& A\Delta y - AR - B\Delta x\\
D =& A\Delta x - BR + B\Delta y
\end{align}$$ and $$\begin{align}
A =& o_x - x_0 + R\sin\theta_0\\
B =& o_y - y_0 + R\cos\theta_0
\end{align}$$*
:::

::: proof
*Proof.* See **Appendix [12](#sec:appendix_TLA_FL){reference-type="ref" reference="sec:appendix_TLA_FL"}** ◻
:::

::: {#rem:TLA_BL .remark}
**Remark 17**. *(Tether Length Monotonicity, B-L) Let the robot path be a Backward and Left-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the tether length function is monotonic if the condition in **Theorem [15](#thm:TLA_FR){reference-type="ref" reference="thm:TLA_FR"}** is satisfied, with the interval of $t$ being changed from $(0, t_{\rm max})$ to $(-t_{\rm max}, 0)$.*
:::

::: {#rem:TLA_BR .remark}
**Remark 18**. *(Tether Length Monotonicity, B-R) Let the robot path be a Backward and Right-turning arc. The centre angle of the arc is $t_{\rm max}$. Then the tether length function is monotonic if the condition in **Theorem [16](#thm:TLA_FL){reference-type="ref" reference="thm:TLA_FL"}** is satisfied, with the interval of $t$ being changed from $(0, t_{\rm max})$ to $(-t_{\rm max}, 0)$.*
:::

:::: {#fig:exp_case_studies .figure latex-placement="t"}
::: caption
Illustration of tethered motions from the same start configuration to the same goal location. (a)(b)(c) Motions satisfying specified SEF constraints. (d)(e) Commonplace (untethered) differential-driven robot motions, where (d) violates the SEF constraint and (e) violates both the SEF constraint and the TLA constraint.
:::
::::

:::: {#fig:exp_Phi .figure latex-placement="t"}
::: caption
Illustration of the angular difference between robot's heading orientation and the tether retracting direction. Admissible upper bounds and lower bounds are depicted.
:::
::::

## Summary (Improved Node Expansion)

As the result of the aforementioned discussions, the established sufficient conditions are incorporated into **Algorithm [\[alg:succ\]](#alg:succ){reference-type="ref" reference="alg:succ"}**. The improved node expansion module is presented in **Algorithm [\[alg:improved_node_expansion\]](#alg:improved_node_expansion){reference-type="ref" reference="alg:improved_node_expansion"}**. The most apparent difference between the two algorithms is the re-location of the most time-consuming command, the construction of all waypoint configurations (line [\[alg:node_expansion:construction\]](#alg:node_expansion:construction){reference-type="ref" reference="alg:node_expansion:construction"} in **Algorithm [\[alg:succ\]](#alg:succ){reference-type="ref" reference="alg:succ"}**), into an **if** structure. After the primitive path is generated, the collision-free property and the non-selfcrossing property of the path are validated. Whether the tether-obstacle contact points are changing is also assessed. Then, based on the type of the robot path (straight, F-R, F-L, B-R, or B-L), known parameters are $\Delta x$, $\Delta y$, $o_x$, $o_y$, $x_0$, $y_0$, $\theta_0$, $R$, and $t_{\rm max}$. By calculating the corresponding $A$, $B$, $C$, $D$, and $\varphi$, the corresponding conditions (to be precise, one among **Theorem [10](#thm:SEF_FR){reference-type="ref" reference="thm:SEF_FR"}**, **Theorem [11](#thm:SEF_FL){reference-type="ref" reference="thm:SEF_FL"}**, **Remark [12](#rem:SEF_BL){reference-type="ref" reference="rem:SEF_BL"}**, and **Remark [13](#rem:SEF_BR){reference-type="ref" reference="rem:SEF_BR"}** for SEF, and one among **Theorem [15](#thm:TLA_FR){reference-type="ref" reference="thm:TLA_FR"}**, **Theorem [16](#thm:TLA_FL){reference-type="ref" reference="thm:TLA_FL"}**, **Remark [17](#rem:TLA_BL){reference-type="ref" reference="rem:TLA_BL"}**, **Remark [18](#rem:TLA_BR){reference-type="ref" reference="rem:TLA_BR"}** for TLA) are verified. These are reflected in the Boolean variables "is_o_not_changed\", "is_sef_guaranteed\", and "is_tla_guaranteed\" as either "True\" or "False\". If all these variables evaluate to "True\", then all waypoint configurations are guaranteed to be valid, avoiding the need for explicit construction and inspection. The computational cost is hereby reduced.

# Experimental Results {#section_exp}

The proposed algorithm is designed to construct self-entanglement-free paths for tethered differential-driven robots with polygonal mobile unit operating in arbitrary planar environment. To the best of the authors' knowledge, there did not exist a prior self-entanglement-free tethered path planner. Therefore, in Section [6.1](#sec:case_study){reference-type="ref" reference="sec:case_study"}, the resultant paths generated by the proposed algorithm are demonstrated, alongside those produced by a commonly used differential-driven planner which does not consider the SEF constraint. In Section [6.2](#section_exp_comparison){reference-type="ref" reference="section_exp_comparison"}, the efficiency of the improved node expansion module is closely evaluated by comparing the computational time of both node expansion strategies. This assessment is conducted under various settings, including different robot kinematics, different lengths of primitive paths, and different distance resolutions for waypoint configuration validity checking. Finally, four real-world demonstrations are provided in Section [6.3](#section_realworld){reference-type="ref" reference="section_realworld"} to validate the practicality of the proposed algorithm in real-world settings. An open-sourcing implementation has been provided here:

<https://github.com/ZJUTongYang/seftpp>.

## Case Studies {#sec:case_study}

Refer to Fig. [6](#fig:exp_case_studies){reference-type="ref" reference="fig:exp_case_studies"} for illustrations. These illustrations take place on a $100\times 100$ grid-based planar map containing 8 internal obstacles. The base point, the start location, and the goal location are set at $(80.50, 44.50)$, $(88.50, 9.50)$, and $(41.50, 71.50)$, respectively. These locations are unchanged throughout all testing scenarios. The initial robot tether state is initialised as the local shortening of the Dijkstra's shortest path from the base point to the start location. The initial robot heading direction is initialised such that the tether stretching direction aligns with the middle of the admissible interval. The maximum tether length constraint is set at $80$ (grids). Base point is illustrated as a triangle and is treated as an obstacle. Tether states are depicted as grey lines, whilst robot paths are drawn as thick blue curves. In Case 1, 2, and 3, various tethered robot kinematics are demonstrated, with the tether extending to the back, right, and left, respectively. The corresponding admissible intervals $[\Phi_1, \Phi_2]$ are set as follows: \[2.36, 3.93\], \[3.93, 5.50\], \[0.51, 1.11\], respectively. Utilising the proposed algorithm, the resultant paths are guaranteed to adhere to the SEF constraint, as depicted in Fig. [6](#fig:exp_case_studies){reference-type="ref" reference="fig:exp_case_studies"}(a)$\sim$(c). Notably, Case 3 is the most difficult task for the robot to execute because the admissible $\Phi$ interval $[0.51, 1.11]$ is the narrowest. The variation of $\Phi$ during the robot motion is visualised in Fig. [7](#fig:exp_Phi){reference-type="ref" reference="fig:exp_Phi"}(a). In contrast, using a path planner without explicit consideration of the SEF constraint, the resultant paths, as visualised in Fig. [6](#fig:exp_case_studies){reference-type="ref" reference="fig:exp_case_studies"}(d)$\sim$(e), violate the SEF constraint. The corresponding $\Phi$ variations are shown in Fig. [7](#fig:exp_Phi){reference-type="ref" reference="fig:exp_Phi"}(b). The reader is referred to the supplementary video for the animation of the robot motions.

:::: table*
+-----------------------------------+-------------------------------------------------------------------+
|                                   | Distance Resolution between Consecutive Waypoints (grid)          |
+:===========================:+:===:+:==============:+:==============:+:==============:+:==============:+
| 3-6                         | 1.0 | 0.7            | 0.4            | 0.1            |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
|                                   | Case 1                                                            |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
|                             | 1   |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             | 2   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 55438 / 508563 (**90.17%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 32217 / 340386 (**91.35%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 38614 / 369212 (**90.53%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 34864 / 327846 (**90.39%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 3   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 52063 / 328729 (**86.33%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 40220 / 270946 (**87.07%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 37649 / 251797 (**86.99%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 36424 / 236765 (**86.67%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 4   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 47769 / 236709 (**83.21%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 42076 / 208312 (**83.20%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 43679 / 212518 (**82.95%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 39562 / 189695 (**82.74%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 5   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 43403 / 170840 (**79.74%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 41722 / 163427 (**79.66%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 40558 / 156883 (**79.46%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 41084 / 154362 (**78.98%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 6   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 26571 / 92546 (**77.69%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 24308 / 84090 (**77.58%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 25054 / 84908 (**77.22%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 24049 / 80592 (**77.02%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
|                                   | Case 2                                                            |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
|                             | 1   |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             | 2   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 43406 / 167300 (**79.40%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 22051 / 77320 (**77.81%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 41686 / 126885 (**75.27%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 26907 / 74202 (**73.39%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 3   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 52545 / 111075 (**67.89%**) |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 42840 / 83278 (**66.03%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 27483 / 49670 (**64.38%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 22432 / 38035 (**62.90%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 4   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 46312 / 61572 (**57.07%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 21813 / 26968 (**55.28%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 30238 / 34761 (**53.48%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 17949 / 19317 (**51.84%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 5   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 37874 / 36126 (**48.82%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 26745 / 25309 (**48.62%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 18408 / 17048 (**48.08%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 10968 / 11615 (**51.43%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 6   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 24416 / 17965 (**42.39%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 11490 / 8756 (**43.25%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 13418 / 9905 (**42.47%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 8162 / 5059 (**38.26%**)    |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
|                                   | Case 3                                                            |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
|                             | 1   |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             |     |                |                |                |                |
|                             +-----+----------------+----------------+----------------+----------------+
|                             | 2   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 13448 / 90343 (**87.04%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 11187 / 78749 (**87.56%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 13625 / 83647 (**85.99%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 13112 / 76473 (**85.36%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 3   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 12466 / 56802 (**82.00%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 8541 / 43027 (**83.44%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 10078 / 46166 (**82.08%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 11487 / 47525 (**80.53%**)  |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 4   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 9221 / 33008 (**78.16%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 7746 29611 (**79.26%**)     |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 9348 / 31045 (**76.86%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 9120 / 30223 (**76.82%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 5   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 7254 / 21316 (**74.61%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 6576 / 20188 (**75.43%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 5901 / 18973 (**76.28%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 5773 / 18126 (**75.84%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 2-6                         | 6   |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 5142 / 12850 (**71.42%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 4880 / 12341 (**71.66%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 5121 / 12336 (**70.67%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+
| 3878 / 10477 (**72.99%**)   |     |                |                |                |                |
+-----------------------------+-----+----------------+----------------+----------------+----------------+

::: tablenotes
All results have been averaged over $20$ runs for a fair evaluation.
:::
::::

## Efficiency of the Improved Node Expansion {#section_exp_comparison}

In line with the algorithm presented earlier, the computational advantage of the improved node expansion module is eliminating the need for validity checking on the waypoint configurations of primitive paths. Importantly, this computational improvement is not a trade-off: It makes no difference on the result of the node expansion process, including the number of nodes expanded, the order of expansion, parent-child relationship among nodes, and the optimality of the resultant path. To substantiate the computational improvement, the normal node expansion module and the improved node expansion module are compared. The comparative assessments consider different robot kinematics, different primitive path lengths, and different distance resolutions for validity checking.

In this comparative study, the robot kinematics are set identical to the Case $1$(tether extending to the back), Case $2$(tether extending to the right), and Case $3$(tether extending to the left) in the previous case study. The lengths of primitive paths are varied across multiple tests, ranging from $1$ to $6$ grids. Each primitive path is discretely sampled into waypoint poses of the mobile unit, based on different distance resolutions $1.0$, $0.7$, $0.4$, and $0.1$. Relative statistics are collected in Table. [\[tab:data_in_cases\]](#tab:data_in_cases){reference-type="ref" reference="tab:data_in_cases"} as follows:

1.  The top row reports the computational time of the normal node expansion module and the computational time of the improved node expansion module.

2.  The bottom row provides the number of primitive paths that require waypoint discretisation and detailed validity checking, the number of primitive paths whose validity is guaranteed, and the proportion of the guaranteed valid primitive paths among all primitive paths.

Examining each row in Table, [\[tab:data_in_cases\]](#tab:data_in_cases){reference-type="ref" reference="tab:data_in_cases"} it can be seen that, when the distance resolution for validity checking is reduced, the time required for checking the validity of each primitive path increases. As a result, the computational time of both node expansion module are increasing. However, the computational time of the improved node expansion module experiences a slower rate of growth. Furthermore, when comparing data in the same column, another observation is that as the length of primitive paths increases, the likelihood of the guaranteed valid primitive paths decreases. In the best case, with a primitive path length of 1 grid, over 95% of primitive paths are guaranteed to be valid. Notably, even with unusually lengthy primitive paths (6 grids, equivalent to 6% of the size of the map), the improved node expansion module can safely ignore the validity checking of approximately 40% of primitive paths. Finally, it is crucial to highlight that the improved node expansion module consistently reduces the computational load across all testing cases. This is because the replacement of the validity checking of waypoint configurations is simply a sequence calculation of float-point numbers, $A$, $B$, $C$, $D$, and $\varphi$. Result show that except the left-top test in Case 2, the improved node expansion offers computational advantages in all other testings.

:::: {#fig:real_world .figure latex-placement="t"}
::: caption
\(a\) The real-world robot kinematics. The tether is anchoring at the front bottom of the robot chassis, below the laser, and extends to the back, in the middle of two rear casters. (b) The environment used for real-world tests, modelled by a gridmap. A resultant path is also depicted.
:::
::::

:::: {#fig:real_world_stills .figure latex-placement="t"}
::: caption
Video stills of the tethered robot motions to track the paths.
:::
::::

## Real-world Illustrations {#section_realworld}

Finally, the proposed algorithm is evaluated in four real-world scenarios. The structure of the robot is depicted in Fig. [\[fig:robot_kinematic\]](#fig:robot_kinematic){reference-type="ref" reference="fig:robot_kinematic"}. The front wheels are differential-driven and the rear wheels are passive casters. No omni-directional tether retracting mechanism is equipped on the robot. Maps are off-line pre-constructed, as shown in Fig. [\[fig:real_world_map\]](#fig:real_world_map){reference-type="ref" reference="fig:real_world_map"}. Throughout all testing cases, the proposed algorithm successfully generates self-entanglement-free resultant paths for the differential-driven robot. The reader is referred to Fig. [9](#fig:real_world_stills){reference-type="ref" reference="fig:real_world_stills"} for the illustrations of the real-world testings and the supplementary video for real-world executions.

# Conclusion and Future Work {#section_conclusion}

This work presents a novel mechanism for generating self-entanglement-free (SEF) paths for tethered differential-driven robots. The primary motivation of this work is the tethered path planning problem in the absence of an omni-directional tether-robot anchoring mechanism. No existing algorithm has previously addressed this self-entanglement phenomenon. The proposed algorithm is a searching-based constrained path planner that generates sub-optimal valid path for differential-driven robots within any planar map. A series of simulated case studies, comparative analysis, and real-world experiments conducted in challenging scenarios have proven the effectiveness of the proposed algorithm. These have been supplemented by an open-sourced implementation for the benefit of the community.

The potentials for further development of the proposed algorithm exist in several key directions: First, from an algorithmic perspective, the sparsity of validity checking can be developed when tether-obstacle contact points is changing during a primitive motion. Second, addressing the movement errors during real-world robot execution, particularly when deviations from the predefined SEF path occur, will become an urgent need. Online path deformation mechanism can be explored for this purpose. Last but not least, given the imprecise modelling of the real-world environment, implementing a maximal likelihood estimation approach to determine the state of the tether, including the last tether-obstacle contact point, would be crucial for robust SEF movement.

# Proof of Relative Angle Monotonicity (F-R) {#sec:appendix_SEF_FR}

The pivoting centre of the robot's circular movement is $$\begin{equation}
\label{eqn:FR_pivoting_center}
\left(x_0 + R\cos(\theta_0 - \frac{\pi}{2}), y_0 + R\sin(\theta_0 - \frac{\pi}{2})\right)
\end{equation}$$ The robot path is parameterised as $$\begin{equation}
\alpha(t) = (x(t), y(t), \theta(t)),\ t\in (0, t_{\rm max})
\end{equation}$$ where $x(t)$, $y(t)$, and $\theta(t)$ are calculated as follows: $$\begin{align}
\label{eqn:xytheta}
x(t) &= x_0 + R\cos(\theta_0 - \frac{\pi}{2}) - R\cos(\theta_0 - \frac{\pi}{2}-t)\\
&=x_0 +R\sin\theta_0-R\sin(\theta_0-t)\notag \\
y(t) &= y_0 + R\sin(\theta_0 - \frac{\pi}{2}) - R\sin(\theta_0 - \frac{\pi}{2}-t)\\
&=y_0-R\cos\theta_0 + R\cos(\theta_0-t)\notag \\
\theta(t) &= \theta_0 - t
\end{align}$$ The path of $s$ can be calculated as $$\begin{align}
\tilde{x}(t) =& x(t)  + \cos(\theta_0-t)\Delta x - \sin(\theta_0-t)\Delta y\\
\tilde{y}(t) =& y(t) + \sin(\theta_0-t)\Delta x + \cos(\theta_0-t)\Delta y
\end{align}$$ The relative angle function is expressed as follows $$\begin{equation}
\Phi(t) = \arctan\left(\frac{o_y-\tilde{y}(t)}{o_x-\tilde{x}(t)}\right)-\theta(t),\ t\in (0, t_{\rm max})
\end{equation}$$ Calculating the derivative of $\tilde{x}$, $\tilde{y}$, and $\theta$ with respect to $t$ gives $$\begin{align}
&\frac{d\tilde{x}}{dt} = R\cos(\theta_0-t)+\sin(\theta_0-t)\Delta x +\cos(\theta_0-t)\Delta y\\
&\frac{d\tilde{y}}{dt} = R\sin(\theta_0-t) - \cos(\theta_0-t)\Delta x + \sin(\theta_0-t)\Delta y\\
&\frac{d\theta}{dt} = -1
\end{align}$$ Then, the derivative of $\Phi$ is calculated as $$\begin{equation}
\frac{d\Phi}{dt} = \frac{-\frac{d\tilde{y}}{dt}(o_x-\tilde{x})+\frac{d\tilde{x}}{dt}(o_y-\tilde{y})}{(o_y - \tilde{y})^2 + (o_x - \tilde{x})^2} -\frac{d\theta}{dt}
\end{equation}$$ We ignore the denominator by introducing $\frac{d\tilde{\Phi}}{dt}$: $$\begin{equation}
\label{eqn:FR_tilde_Phi_1}
\begin{aligned}
\frac{d\tilde{\Phi}}{dt} \triangleq& \left( (o_x-\tilde{x})^2+(o_y-\tilde{y})^2 \right)\frac{d\Phi}{dt}\\
=&-\frac{d\tilde{y}}{dt}(o_x-\tilde{x}) + \frac{d\tilde{x}}{dt}(o_y-\tilde{y}) +(o_x-\tilde{x})^2+(o_y-\tilde{y})^2\\
=& (o_x - \tilde{x}-\frac{d\tilde{y}}{dt})(o_x - \tilde{x}) + (o_y + \frac{d\tilde{x}}{dt} - \tilde{y})(o_y - \tilde{y})
\end{aligned}
\end{equation}$$ By calculation, $$\begin{align}
o_x - \tilde{x} - \frac{d\tilde{y}}{dt} =& o_x - x(t) - R\sin(\theta_0-t)\\
=& o_x - x_0 -R\sin\theta_0\notag\\
o_y + \frac{d\tilde{x}}{dt} - \tilde{y} =& o_y - y(t) + R\cos(\theta_0-t)\\
=& o_y - y_0 +R\cos\theta_0
\end{align}$$ hence $$\begin{equation}
\label{eqn:FR_tilde_Phi_2}
\begin{aligned}
&\cdots (\mbox{Eqn.~(\ref{eqn:FR_tilde_Phi_1}}))\\
=& (o_x - x_0 -R\sin\theta_0)\\
&\qquad*(o_x-x(t)-\cos(\theta_0-t)\Delta x + \sin(\theta_0-t)\Delta y)\\
&+ (o_y - y_0 +R\cos\theta_0)\\
&\qquad*(o_y - y(t) - \sin(\theta_0-t)\Delta x - \cos(\theta_0-t)\Delta y)
\end{aligned}
\end{equation}$$ By letting $$\begin{align}
&A \triangleq o_x - x_0 - R\sin\theta_0\\
&B \triangleq o_y - y_0 + R\cos\theta_0
\end{align}$$ the equation is further simplified to $$\begin{equation}
\begin{aligned}
&\cdots (\mbox{Eqn.~(\ref{eqn:FR_tilde_Phi_2}}))\\
=& A(A + R\sin(\theta_0-t) - \cos(\theta_0-t)\Delta x+ \sin(\theta_0-t)\Delta y)\\
&+ B(B - R\cos(\theta_0-t) - \sin(\theta_0-t)\Delta x - \cos(\theta_0-t)\Delta y)\\
=& -\cos(\theta_0-t)[A\Delta x+ BR + B\Delta y]\\
&+ \sin(\theta_0-t)[AR + A\Delta y - B\Delta x] + A^2 + B^2
\end{aligned}
\end{equation}$$ Finally, we have $$\begin{equation}
\frac{d\tilde{\Phi}}{dt} = -\sqrt{C^2+D^2}\cos(t-\theta_0-\varphi) + A^2 + B^2
\end{equation}$$ where $$\begin{align}
C &\triangleq A\Delta x + BR + B\Delta y\\
D &\triangleq AR + A\Delta y - B\Delta x
\end{align}$$ and $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2 + D^2}}
\end{equation}$$ Hence, the cases when $\Phi$ is monotonic are calculated as $$\begin{equation}
\begin{aligned}
&\frac{d\Phi}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{\Phi}}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& A^2+B^2 > \sqrt{C^2+D^2}\cos(t-\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{A^2+B^2}{\sqrt{C^2+D^2}} > \cos(t-\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$ or $$\begin{equation}
\begin{aligned}
&\frac{d\Phi}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{\Phi}}{dt} < 0,\ \forall t\in (0, t_{\rm max}) \\
\Leftrightarrow& A^2 + B^2 < \sqrt{C^2+D^2}\cos(t-\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{A^2+B^2}{\sqrt{C^2+D^2}} < \cos(t-\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$

# Proof of Relative Angle Monotonicity (F-L) {#sec:appendix_SEF_FL}

The pivoting centre of the robot's circular movement is $$\begin{equation}
\left(x_0 + R\cos(\theta_0 + \frac{\pi}{2}), y_0 + R\sin(\theta_0 + \frac{\pi}{2})\right)
\end{equation}$$ The robot path is parameterised as $$\begin{equation}
\alpha(t) = (x(t), y(t), \theta(t)),\ t\in (0, t_{\rm max})
\end{equation}$$ where $x(t)$, $y(t)$, and $\theta(t)$ are calculated as follows: $$\begin{align}
x(t) &= x_0 + R\cos(\theta_0 + \frac{\pi}{2}) - R\cos(\theta_0 + \frac{\pi}{2}+t)\\
&=x_0 -R\sin\theta_0+R\sin(\theta_0+t)\notag \\
y(t) &= y_0 + R\sin(\theta_0 + \frac{\pi}{2}) - R\sin(\theta_0 + \frac{\pi}{2}+t)\\
&=y_0-R\cos\theta_0 - R\cos(\theta_0+t)\notag \\
\theta(t) &= \theta_0 + t
\end{align}$$ The path of $s$ can be calculated as $$\begin{align}
\tilde{x}(t) &= x(t) + \cos(\theta_0 + t)\Delta x - \sin(\theta_0+t)\Delta y\\
\tilde{y}(t) &= y(t) + \sin(\theta_0 + t)\Delta x + \cos(\theta_0+t)\Delta y
\end{align}$$ Then the relative angle function is expressed as follows $$\begin{equation}
\Phi(t) = \arctan\left(\frac{o_y-\tilde{y}(t)}{o_x-\tilde{x}(t)}\right)-\theta(t),\ t\in (0, t_{\rm max})
\end{equation}$$ Calculating the derivative of $\tilde{x}$, $\tilde{y}$, and $\theta$ with respect to $t$ gives $$\begin{align}
&\frac{d\tilde{x}}{dt} = R\cos(\theta_0+t) - \sin(\theta_0+t)\Delta x - \cos(\theta_0+t)\Delta y\\
&\frac{d\tilde{y}}{dt} = R\sin(\theta_0+t) + \cos(\theta_0+t)\Delta x - \sin(\theta_0+t)\Delta y\\
&\frac{d\theta}{dt} = 1
\end{align}$$ Then, the derivative of $\Phi$ is calculated as $$\begin{equation}
\frac{d\Phi}{dt} = \frac{-\frac{d\tilde{y}}{dt}(o_x-\tilde{x})+\frac{d\tilde{x}}{dt}(o_y-\tilde{y})}{(o_y - \tilde{y})^2 + (o_x - \tilde{x})^2} -\frac{d\theta}{dt}
\end{equation}$$ We ignore the denominator by introducing $\frac{d\tilde{\Phi}}{dt}$: $$\begin{equation}
\label{eqn:FL_tilde_Phi_1}
\begin{aligned}
\frac{d\tilde{\Phi}}{dt} \triangleq& \left( (o_x-\tilde{x})^2+(o_y-\tilde{y})^2 \right)\frac{d\Phi}{dt}\\
=&-\frac{d\tilde{y}}{dt}(o_x-\tilde{x}) + \frac{d\tilde{x}}{dt}(o_y-\tilde{y}) - (o_x-\tilde{x})^2 - (o_y-\tilde{y})^2\\
=&(-o_x + \tilde{x} - \frac{d\tilde{y}}{dt})(o_x - \tilde{x}) + (-o_y + \frac{d\tilde{x}}{dt} + \tilde{y})(o_y - \tilde{y})
\end{aligned}
\end{equation}$$ By calculation, $$\begin{align}
-o_x + \tilde{x} - \frac{d\tilde{y}}{dt} =& -o_x + x(t) - R\sin(\theta_0+t)\\
=& -o_x + x_0 - R\sin\theta_0\notag\\
-o_y + \frac{d\tilde{x}}{dt} + \tilde{y} =& o_y + y(t) + R\cos(\theta_0+t)\\
=& -o_y + y_0 - R\cos\theta_0\notag
\end{align}$$ hence $$\begin{equation}
\label{eqn:FL_tilde_Phi_2}
\begin{aligned}
&\cdots(\mbox{Eqn.~(\ref{eqn:FL_tilde_Phi_1})})\\
=&(-o_x + x_0- R\sin\theta_0)\\
&\qquad*(o_x-x(t) - \cos(\theta_0+t)\Delta x + \sin(\theta_0+t)\Delta y)\\
&+(-o_y + y_0 - R\cos\theta_0)\\
&\qquad*(o_y - y(t) - \sin(\theta_0+t)\Delta x - \cos(\theta_0+t)\Delta y)
\end{aligned}
\end{equation}$$ By letting $$\begin{align}
A &\triangleq o_x - x_0 + R\sin\theta_0\\
B &\triangleq o_y - y_0 + R\cos\theta_0
\end{align}$$ the equation is further simplified to $$\begin{equation}
\begin{aligned}
&\cdots(\mbox{Eqn.~(\ref{eqn:FL_tilde_Phi_2})})\\
=& -A(A - R\sin(\theta_0+t) - \cos(\theta_0+t)\Delta x + \sin(\theta_0+t)\Delta y)\\
&-B(B + R\cos(\theta_0+t) - \sin(\theta_0+t)\Delta x - \cos(\theta_0+t)\Delta y)\\
=& \cos(\theta_0+t)[A\Delta x - BR + B\Delta y]\\
&+ \sin(\theta_0+t)[AR-A\Delta y + B\Delta x] - A^2 - B^2
\end{aligned}
\end{equation}$$ Finally,we have $$\begin{equation}
\frac{d\tilde{\Phi}}{dt} = \sqrt{C^2+D^2}\cos(t+\theta_0-\varphi) - A^2- B^2
\end{equation}$$ where $$\begin{align}
C &\triangleq A\Delta x - BR + B\Delta y\\
D &\triangleq AR - A\Delta y + B\Delta x
\end{align}$$ and $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2+D^2}}
\end{equation}$$ Hence, the cases when $\Phi$ is monotonic are calculated as $$\begin{equation}
\begin{aligned}
&\frac{d\Phi}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{\Phi}}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& A^2+B^2 < \sqrt{C^2+D^2}\cos(t+\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{A^2+B^2}{\sqrt{C^2+D^2}} < \cos(t+\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$ or $$\begin{equation}
\begin{aligned}
&\frac{d\Phi}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{\Phi}}{dt} < 0,\ \forall t\in (0, t_{\rm max}) \\
\Leftrightarrow& A^2+B^2 > \sqrt{C^2+D^2}\cos(t+\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{A^2+B^2}{\sqrt{C^2+D^2}} > \cos(t+\theta_0-\varphi),\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$

# Proof of Tether Length Monotonicity (Straight) {#sec:appendix_TLA_Straight}

The robot path is parameterised as $$\begin{align}
x(t) &= x_0 + t\cos\theta_0\\
y(t) &= y_0 + t\sin\theta_0\\
\theta(t) &= \theta_0
\end{align}$$ Then, the path of $s$ is $$\begin{align}
\tilde{x}(t) =& x_0 + t\cos\theta_0 + \cos\theta_0\Delta x - \sin\theta_0\Delta y\\
\tilde{y}(t) =& y_0 + t\sin\theta_0 + \sin\theta_0\Delta x + \cos\theta_0\Delta y
\end{align}$$ The tether length function is expressed as follows $$\begin{equation}
L(t) = L_o + \sqrt{(o_x - \tilde{x}(t))^2 + (o_y - \tilde{y}(t))^2}
\end{equation}$$ where $L_o$ is the consumed tether length from the base point to the last tether-obstacle contact point $o$. Calculating the derivative of $\tilde{x}$, $\tilde{y}$, and $\theta$ with respect to $t$ gives $$\begin{align}
\frac{d\tilde{x}}{dt} &= \cos\theta_0\\
\frac{d\tilde{y}}{dt} &= \sin\theta_0\\
\frac{d\theta}{dt} &= 0
\end{align}$$ After that, the derivative of $L$ with respect to $t$ is calculated as $$\begin{equation}
\frac{dL}{dt} = \frac{-(o_x-\tilde{x})\frac{d\tilde{x}}{dt} - (o_y - \tilde{y})\frac{d\tilde{y}}{dt}}{\sqrt{(o_x-\tilde{x})^2 + (o_y - \tilde{y})^2}}
\end{equation}$$ We ignore the denominator by introducing $\frac{d\tilde{L}}{dt}$: $$\begin{equation}
\begin{aligned}
\frac{d\tilde{L}}{dt} \triangleq& \sqrt{(o_x-\tilde{x})^2 + (o_y - \tilde{y})^2} \frac{dL}{dt}\\
=& -(o_x - x_0 - t\cos\theta_0-\cos\theta_0\Delta x + \sin\theta_0\Delta y)\cos\theta_0\\
&- (o_y - y_0 - t\sin\theta_0 - \sin\theta_0\Delta x - \cos\theta_0\Delta y)\sin\theta_0\\
=& t - (o_x + o_y - x_0\cos\theta_0 - y_0\sin\theta_0 - \Delta x)
\end{aligned}
\end{equation}$$ Hence, the cases when $L$ is monotonic are calculated as $$\begin{equation}
\begin{aligned}
&\frac{dL}{dt} >0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{L}}{dt}>0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& 0 > o_x + o_y - x_0\cos\theta_0 - y_0\sin\theta_0 - \Delta x
\end{aligned}
\end{equation}$$ or $$\begin{equation}
\begin{aligned}
&\frac{dL}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{L}}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& t_{\rm max} < o_x + o_y - x_0\cos\theta_0 - y_0\sin\theta_0 - \Delta x
\end{aligned}
\end{equation}$$

# Proof of Tether Length Monotonicity (F-R) {#sec:appendix_TLA_FR}

The pivoting centre of the robot's circular movement is $$\begin{equation}
\left( x_0 + R\cos(\theta_0 - \frac{\pi}{2}),\ y_0 + R\sin(\theta_0 - \frac{\pi}{2}) \right)
\end{equation}$$ The robot path is parameterised as $$\begin{equation}
\alpha(t)= (x(t), y(t), \theta(t)), \forall t\in (0, t_{\rm max})
\end{equation}$$ where $x(t)$, $y(t)$, and $\theta(t)$ are calculated as follows: $$\begin{align}
x(t) &= x_0 + R\cos(\theta_0 - \frac{\pi}{2}) - R\cos(\theta_0 - \frac{\pi}{2}-t)\\
&=x_0 +R\sin\theta_0-R\sin(\theta_0-t)\notag \\
y(t) &= y_0 + R\sin(\theta_0 - \frac{\pi}{2}) - R\sin(\theta_0 - \frac{\pi}{2}-t)\\
&=y_0-R\cos\theta_0 + R\cos(\theta_0-t)\notag \\
\theta(t) &= \theta_0 - t
\end{align}$$ The path of $s$ can be calculated as $$\begin{align}
\tilde{x}(t) =& x(t) + \cos(\theta_0-t)\Delta x - \sin(\theta_0-t)\Delta y\\
=& x_0 + R\sin\theta_0 - (R+\Delta y)\sin(\theta_0-t) + \cos(\theta_0-t)\Delta x  \notag\\
\tilde{y}(t) =& y(t) + \sin(\theta_0-t)\Delta x + \cos(\theta_0-t)\Delta y\\
=& y_0 - R\cos\theta_0 + (R+\Delta y)\cos(\theta_0-t) + \sin(\theta_0-t)\Delta x\notag
\end{align}$$ The tether length function is expressed as follows $$\begin{equation}
L(t) = L_o + \sqrt{ (o_x-\tilde{x}(t))^2 + (o_y - \tilde{y}(t))^2}
\end{equation}$$ where $L_o$ is the consumed tether length from the base point to the last tether-obstacle contact point $o$. Calculating the derivative of $\tilde{x}$, $\tilde{y}$, and $\theta$ with respect to $t$ gives $$\begin{align}
\frac{d\tilde{x}}{dt} =& (R+\Delta y) \cos(\theta_0-t) + \sin(\theta_0-t)\Delta x\\
\frac{d\tilde{y}}{dt} =& (R+\Delta y)\sin(\theta_0-t) - \cos(\theta_0-t)\Delta x\\
\frac{d\theta}{dt} =& -1
\end{align}$$ The derivative of $L$ is calculated as $$\begin{equation}
\frac{dL}{dt} = \frac{-(o_x-\tilde{x})\frac{d\tilde{x}}{dt} - (o_y - \tilde{y})\frac{d\tilde{y}}{dt}}{\sqrt{(o_x-\tilde{x})^2 + (o_y - \tilde{y})^2}}
\end{equation}$$ We ignore the denominator by introducing $\frac{d\tilde{L}}{dt}$: $$\begin{equation}
\label{eqn:FR_tilde_L_1}
\begin{aligned}
\frac{d\tilde{L}}{dt} \triangleq& \sqrt{(o_x - \tilde{x})^2+(o_y - \tilde{y})^2}\frac{dL}{dt}\\
=& -(o_x - x_0 - R\sin\theta_0 + (R+\Delta y)\sin(\theta_0-t) - \cos(\theta_0-t)\Delta x)\\
&*((R+\Delta y)\cos(\theta_0-t) + \sin(\theta_0-t)\Delta x)\\
&-(o_y - y_0 + R\sin\theta_0 - (R+\Delta y)\cos(\theta_0-t) - \sin(\theta_0-t)\Delta x)\\
&*((R+\Delta y)\sin(\theta_0-t) - \cos(\theta_0-t)\Delta x)
\end{aligned}
\end{equation}$$ By letting $$\begin{align}
A\triangleq& o_x - x_0 - R\sin\theta_0\\
B\triangleq& o_y - y_0 + R\sin\theta_0
\end{align}$$ the equation is further simplified to $$\begin{equation}
\begin{aligned}
&\cdots(\mbox{Eqn.~(\ref{eqn:FR_tilde_L_1})})\\
=& \sin(\theta_0-t)\cos(\theta_0-t)[-(R+\Delta y)^2 + \Delta x^2 + (R+\Delta y)^2 - \Delta x^2]\\
&+ \sin^2(\theta_0-t)[-(R+\Delta y)\Delta x + \Delta x(R + \Delta y)]\\
&+\cos^2(\theta_0-t)[\Delta x(R + \Delta y) - (R+\Delta y)\Delta x]\\
&-A((R+\Delta y)\cos(\theta_0-t)+\sin(\theta_0-t)\Delta x))\\
&-B((R + \Delta y)\sin(\theta_0-t) - \cos(\theta_0-t)\Delta x)\\
=& (B\Delta x - AR - A\Delta y)\cos(\theta_0-t)\\ 
&\qquad- (A\Delta x - BR - B\Delta y)\sin(\theta_0-t)
\end{aligned}
\end{equation}$$ Further simplify the notations, we have $$\begin{equation}
\frac{d\tilde{L}}{dt} = \sqrt{C^2 + D^2}\cos(t-\theta_0 - \varphi)
\end{equation}$$ where $$\begin{align}
&C \triangleq B\Delta x - AR - A\Delta y\\
&D \triangleq A\Delta x - BR - B\Delta y
\end{align}$$ and $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2+D^2}}
\end{equation}$$ Hence, the cases when $L$ is monotonic are calculated as $$\begin{equation}
\begin{aligned}
&\frac{dL}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow&\frac{d\tilde{L}}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \sqrt{C^2+D^2}\cos(t - \theta_0 - \varphi) > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \cos(t - \theta_0 - \varphi) > 0,\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$ or $$\begin{equation}
\begin{aligned}
&\frac{dL}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \frac{d\tilde{L}}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \sqrt{C^2+D^2}\cos(t - \theta_0 - \varphi) < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \cos(t - \theta_0 - \varphi) < 0,\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$

# Proof of Tether Length Monotonicity (F-L) {#sec:appendix_TLA_FL}

The pivoting centre of the robot's circular movement is $$\begin{equation}
\left(x_0 + R\cos(\theta_0 + \frac{\pi}{2}),\ y_0 + R\sin(\theta_0 + \frac{\pi}{2})\right)
\end{equation}$$ The robot path is parameterised as $$\begin{equation}
\alpha(t) = (x(t), y(t), \theta(t)),\ t\in (0, t_{\rm max})
\end{equation}$$ where $x(t)$, $y(t)$, and $\theta(t)$ are calculated as follows: $$\begin{align}
x(t) &= x_0 + R\cos(\theta_0 + \frac{\pi}{2}) - R\cos(\theta_0 + \frac{\pi}{2}+t)\\
&=x_0 -R\sin\theta_0+R\sin(\theta_0+t)\notag \\
y(t) &= y_0 + R\sin(\theta_0 + \frac{\pi}{2}) - R\sin(\theta_0 + \frac{\pi}{2}+t)\\
&=y_0-R\cos\theta_0 - R\cos(\theta_0+t)\notag \\
\theta(t) &= \theta_0 + t
\end{align}$$ The path of $s$ can be calculated as $$\begin{align}
\tilde{x}(t) =&x(t) + \cos(\theta_0+t)\Delta x - \sin(\theta_0+t)\Delta y\\
=& x_0-R\sin\theta_0 + (R - \Delta y)\sin(\theta_0+t) + \cos(\theta_0+t)\Delta x\notag\\
\tilde{y}(t) =& y(t) + \sin(\theta_0+t)\Delta x + \cos(\theta_0+t)\Delta y\\
=& y_0 - R\cos\theta_0 - (R-\Delta y)\cos(\theta_0+t) + \sin(\theta_0+t)\Delta x \notag
\end{align}$$ The tether length function is expressed as follows $$\begin{equation}
L(t) = L_o + \sqrt{ (o_x-\tilde{x}(t))^2 + (o_y - \tilde{y}(t))^2}
\end{equation}$$ where $L_o$ is the consumed tether length from the base point to the last tether-obstacle contact point $o$. Calculating the derivative of $\tilde{x}$, $\tilde{y}$, and $\theta$ with respect to $t$ gives $$\begin{align}
&\frac{d\tilde{x}}{dt} = (R-\Delta y)\cos(\theta_0+t) - \sin(\theta_0+t)\Delta x\\
&\frac{d\tilde{y}}{dt} = (R-\Delta y)\sin(\theta_0+t) +\cos(\theta_0+t)\Delta x\\
&\frac{d\theta}{dt} = 1
\end{align}$$ The derivative of $L$ is calculated as $$\begin{equation}
\frac{dL}{dt} = \frac{-(o_x-\tilde{x})\frac{d\tilde{x}}{dt} - (o_y - \tilde{y})\frac{d\tilde{y}}{dt}}{\sqrt{(o_x-\tilde{x})^2 + (o_y - \tilde{y})^2}}
\end{equation}$$ We ignore the denominator by introducing $\frac{d\tilde{L}}{dt}$: $$\begin{equation}
\label{eqn:FL_tilde_L_1}
\begin{aligned}
\frac{d\tilde{L}}{dt} \triangleq& \sqrt{(o_x-\tilde{x})^2 + (o_y - \tilde{y})^2} \frac{dL}{dt}\\
=& -(o_x - x_0 + R\sin\theta_0 - (R-\Delta y)\sin(\theta_0+t) - \cos(\theta_0+t)\Delta x)\\
&*((R - \Delta y)\cos(\theta_0+t) - \sin(\theta_0+t)\Delta x)\\
&-(o_y - y_0 + R\cos\theta_0 + (R-\Delta y)\cos(\theta_0+t) - \sin(\theta_0+t)\Delta x)\\
&*((R - \Delta y)\sin(\theta_0+t) +\cos(\theta_0+t)\Delta x)
\end{aligned}
\end{equation}$$ By letting $$\begin{align}
A \triangleq& o_x - x_0 + R\sin\theta_0\\
B \triangleq& o_y - y_0 + R\cos\theta_0
\end{align}$$ the equation is further simplified to $$\begin{equation}
\begin{aligned}
&\cdots(\mbox{Eqn.~(\ref{eqn:FL_tilde_L_1})})\\
=& \sin(\theta_0+t)\cos(\theta_0+t)[(R-\Delta y)^2 - \Delta x^2 - (R - \Delta y)^2 + \Delta x^2]\\
&+\sin^2(\theta_0+t)[-(R-\Delta y)\Delta x + \Delta x(R-\Delta y)]\\
&+\cos^2(\theta_0+t)[\Delta x(R-\Delta y) - (R-\Delta y)\Delta x]\\
&- A((R-\Delta y)\cos(\theta_0+t) - \sin(\theta_0+t)\Delta x)\\
&- B((R-\Delta y)\sin(\theta_0+t) + \cos(\theta_0+t)\Delta x)\\
=& (A\Delta y - AR - B\Delta x)\cos(\theta_0+t)\\
&\qquad - (A\Delta x - BR + B\Delta y)\sin(\theta_0+t)
\end{aligned}
\end{equation}$$ Further simplify the notations, we have $$\begin{equation}
\frac{d\tilde{L}}{dt}= \sqrt{C^2 + D^2}\cos(t + \theta_0 + \varphi)
\end{equation}$$ where $$\begin{align}
C &\triangleq A\Delta y - AR - B\Delta x\\
D &\triangleq A\Delta x - BR + B\Delta y
\end{align}$$ and $\varphi$ is the angle such that $$\begin{equation}
\cos\varphi = \frac{C}{\sqrt{C^2+D^2}},\ \sin\varphi = \frac{D}{\sqrt{C^2+D^2}}
\end{equation}$$ Hence, the cases when $L$ is monotonic are calculated as $$\begin{equation}
\begin{aligned}
&\frac{dL}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow&\frac{d\tilde{L}}{dt} > 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \sqrt{C^2+D^2}\cos(t + \theta_0 + \varphi)>0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \cos(t + \theta_0 + \varphi)>0,\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$ or $$\begin{equation}
\begin{aligned}
&\frac{dL}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow&\frac{d\tilde{L}}{dt} < 0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \sqrt{C^2+D^2}\cos(t + \theta_0 + \varphi)<0,\ \forall t\in (0, t_{\rm max})\\
\Leftrightarrow& \cos(t + \theta_0 + \varphi)<0,\ \forall t\in (0, t_{\rm max})
\end{aligned}
\end{equation}$$

[^1]: This work was supported by the National Key R&D Program of China under Grant 2021ZD0114500. *(Corresponding author: Yue Wang and Rong Xiong.)*

[^2]: Tong Yang, Jiangpin Liu, Yue Wang, and Rong Xiong are with the State Key Laboratory of Industrial Control and Technology, Zhejiang University, P.R. China.

[^3]: <https://github.com/ZJUTongYang/seftpp>

[^4]: The robot's heading direction $\theta(t)$ is the tangent of the path. The tether state $O$ is calculated by the locally obstacle-free tautening of the concatenation of the robot path and the trace of the tether-robot anchoring point $s$.

[^5]: The module is the same as the Algorithm 2 in [@Yang2023Self], but is presented in a slightly lengthy form for the easy re-usage in the **Algorithm [\[alg:improved_node_expansion\]](#alg:improved_node_expansion){reference-type="ref" reference="alg:improved_node_expansion"}** of this paper. Also, the pseudocode is arranged next to **Algorithm [\[alg:improved_node_expansion\]](#alg:improved_node_expansion){reference-type="ref" reference="alg:improved_node_expansion"}** for easy comparison.
