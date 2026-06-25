---
citation_key: Holmes2020Reachable
arxiv_id: 2002.01591
arxiv_url: https://arxiv.org/abs/2002.01591
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:43:09Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

To maximize utility in arbitrary environments, especially when operating near people, robotic arms should plan collision-free motions in real time. Such performance requires sensing and reacting to the environment as the robot plans and executes motions; in other words, it must perform *receding-horizon planning*, where it iteratively generates a plan while executing a previous plan. This paper addresses **guaranteed-safe receding-horizon trajectory planning for robotic arms**. We call the proposed method Autonomous Reachability-based Manipulator Trajectory Design, or **ARMTD**, introduced in Fig. [1](#fig:fetch_intro){reference-type="ref" reference="fig:fetch_intro"}.

:::: {#fig:fetch_intro .figure latex-placement="t"}
![](Holmes2020Reachable_figs/fetch_timelapse.png){width="0.95\\columnwidth"}

::: caption
ARMTD performs safe, real-time receding-horizon planning for a Fetch arm around a cabinet in real time, from a start pose (purple, low shelf) to a goal (green, high shelf). Several intermediate poses are shown (transparent). The callout on the left, corresponding to the blue intermediate pose, shows a single planning iteration, with the shelf in light red. In grey is the arm's reachable set for a continuum of parameterized trajectories over a short time horizon. The smaller blue set is the subset of the reachable set corresponding to the particular trajectory that was selected for this planning iteration, which is guaranteed not to collide with the obstacle. Over many such trials in simulation and on hardware, ARMTD never crashed. See our video: [`youtu.be/ySnux2owlAA`](https://youtu.be/ySnux2owlAA).
:::
::::

Motion planning can be broadly split into three paradigms, depending on whether safety is enforced by (1) a path planner, (2) a trajectory planner, or (3) a tracking controller.

The first paradigm is commonly used for robotic arm planning, wherein the path planner is responsible for safety. One generates a collision-free path, then smooths it and parameterizes it by time (i.e., converts it into a trajectory) [@pfeiffer1987_old_traj_planning; @Kunz2012_traj_gen]. Such methods often have a tradeoff between safety and real-time performance because they represent paths with discrete points in configuration space [@lavalle2001randomized; @kavraki1996probabilistic]. Ensuring safety requires approximations such as buffering the volume of the arm at each discrete point to account for the discretization, or computing the swept volume along the path assuming, e.g., straight lines between points [@lavalle_textbook]. If one treats the path as a decision variable in a nonlinear optimization program, the gradient of the distance between the arm's volume and obstacles may "push" each configuration out of collision [@chomp; @trajopt; @itomp]. This means the output path can be treated directly as a trajectory, if the optimization uses path smoothness as the cost. However, this relies on several approximations to achieve real-time performance: finite differencing to bound joint speeds and accelerations, collision penalties in the cost instead of hard constraints, and finite differencing [@chomp] or linearization [@trajopt] for the collision-avoidance penalty gradient. This necessitates finer discretization to faithfully represent the robot's kinematics. To enable real-time performance without gradients, one can compute many paths offline, then collision-check at runtime [@Murray2016_motion_planning_on_chip; @kunz2010_PRM]; but for arbitrary tasks, it can be unclear how many paths are necessary, or how to ensure safety if the arm's volume changes (e.g., by grasping an object). Another approach to real-time performance is to plan iteratively in a receding-horizon either by gradient descent (with the same drawbacks as above) [@itomp] or assuming the underlying path planner is safe [@Hauser2012_receding_horizon]. In summary, in this paradigm, one must discretize finely, or buffer by a large amount, to achieve safety at the expense of performance.

In the second paradigm, the path planner generates a (potentially unsafe) path, then the trajectory planner attempts to track the path as closely as possible while maintaining safety. In this paradigm, one computes a *reachable set* (RS) for a family of trajectories instead of computing a swept volume for a path. Methods in this paradigm can achieve both safety and real-time performance in receding-horizon planning by leveraging sums-of-squares programming [@majumdar2016funnel; @kousik2018_RTD_ijrr; @Vaskov2019_RSS] or zonotope reachability analysis [@kousik2019_quadrotor_rtd]. Unfortunately, the methods in this paradigm suffer from the curse of dimensionality, preventing their use with the high-dimensional models of typical arms.

In the third paradigm, one attempts to ensure safety via the tracking controller, instead of in a path or trajectory. Here, one builds a supervisory safety controller for pre-specified trajectories [@althoff2019_safe_modular_bots] or a set of safe states [@singletary2019_arm_barrier_function]. Another approach is to compute a safety buffer and associated controller using Hamilton-Jacobi reachability analysis [@herbert2017_fastrack; @chen2018_hjb_decomposition], but the curse of dimensionality has prevented applying this to arms.

To the best of our knowledge, RSs in manipulator planning have only been used for either collision-checking a single, precomputed trajectory [@althoff2019_safe_modular_bots; @fraichard2012guaranteeing], or for controlling to a predefined setpoint [@majumdar2014control]. In contrast, our proposed ARMTD method generates RSs for a continuum of trajectories, allowing optimization over sets of safe trajectories. Computing such RSs directly is challenging because of the high-dimensional configuration space and nonlinear transformation to workspace used for a typical arm [@kousik2018_RTD_ijrr; @chen2018_hjb_decomposition].

Our proposed ARMTD method overcomes these challenges by composing a high-dimensional RS in workspace from low-dimensional reachable sets of joint configurations. ARMTD extends the second planning paradigm above by using these RSs to plan safe trajectories in real time. The RS also provides subdifferentiable collision-avoidance, self-intersection, and joint limit constraints for trajectory optimization. Importantly, the RS composition, constraint generation, and gradient evaluation are all parallelizable.

We now provide an overview of ARMTD, also shown in Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}. ARMTD begins by specifying a parameterized continuum of kinematic configuration space trajectories, each of which includes a fail-safe maneuver. Offline, ARMTD computes parameterized joint reachable sets, or JRSs, of these trajectories in configuration space. At runtime (in each receding-horizon), it constructs a parameterized RS from the precomputed JRSs. ARMTD intersects the RS with obstacles to generate provably-correct safety constraints. ARMTD then performs trajectory optimization over the parameters, subject to the safety constraints. If it cannot find a feasible solution within a prespecified time limit, the arm continues executing the trajectory from its previous planning iteration (which includes a fail-safe maneuver), guaranteeing perpetual safety [@kousik2018_RTD_ijrr; @Hauser2012_receding_horizon]. In this work, we only discuss static environments, but this approach can extend to dynamic environments [@Vaskov2019_RSS].

## Contributions

We make the following contributions. First, a method to conservatively construct the RS of high-dimensional redundant robotic manipulators (Sections [3](#sec:reachability){reference-type="ref" reference="sec:reachability"}--[4](#sec:online_planning){reference-type="ref" reference="sec:online_planning"}). Second, a parallelized method to perform real-time, provably-safe, receding-horizon trajectory optimization (Section [4](#sec:online_planning){reference-type="ref" reference="sec:online_planning"}). Third, a demonstration in simulation and on hardware, with no collisions (Section [5](#sec:demos){reference-type="ref" reference="sec:demos"} and Supplemental Video), plus a comparison to CHOMP [@chomp]. The remaining sections are Section [2](#sec:preliminaries){reference-type="ref" reference="sec:preliminaries"} (Arm, Obstacles, and Trajectory Parameters) and Section [6](#sec:conclusion){reference-type="ref" reference="sec:conclusion"} (Conclusion). See our video: [`youtu.be/ySnux2owlAA`](https://youtu.be/ySnux2owlAA). Our code is available: [`github.com/ramvasudevan/arm_planning`](https://github.com/ramvasudevan/arm_planning). All proofs, plus additional explanations, are available in the appendices included at the end of this document.

## Notation

The $n$-dimensional real numbers are $\ensuremath \mathbb{R}^n$, natural numbers are $\ensuremath \mathbb{N}$, the unit circle is $\mathbb{S}^1$, and the set of $3\times 3$ rotation matrices is $\mathrm{\textnormal{\small{SO}}}(3)$. Vectors are either $[x_1,\cdots,x_n]^\top$ or $(x_1,\cdots,x_n)$ depending on if the size/shape is relevant. Let $U, V \subset \ensuremath \mathbb{R}^n$. For a point $p \in U$, $\{p\} \subset U$ is the set containing $p$. The power set of $U$ is $\ensuremath \mathcal{P}(U)$. The Minkowski sum is $U \oplus V = \{u + v~|~u \in U,\ v \in V\}$. For a matrix $A \in \ensuremath \mathbb{R}^{n\times n}$, $AU = \{Au~|~u \in U\}$. For matrices, $\prod$ performs right multiplication with increasing index (e.g., $\prod_{i=1}^3 A_i = A_1A_2A_3$). Greek lowercase letters in angle brackets are indeterminate variables (e.g., $\langle\sigma\rangle$). Superscripts on points index elements of a set. Subscripts are joint indices or contextual information.

# Arm, Obstacles, and Trajectory Parameters {#sec:preliminaries}

The goal of this work is to plan collision-free trajectories for a robotic arm operating around obstacles in a receding-horizon framework. We now discuss the arm and its environment, then our receding-horizon framework and parameterized trajectories.

## Arm and Obstacles

### Arm

Consider an arm with $n_q \in \ensuremath \mathbb{N}$ joints (i.e., $n_q$ DOFs) and $n_q + 1$ links, including the $0$^th^ link, or *baselink*. We make the following assumptions/definitions. Each joint is a single-axis revolute joint, attached between a *predecessor* link and a *successor* link. The arm is a single kinematic chain from baselink to end effector; link $i-1$ is joined to link $i$ by joint $i$ for $i = 1,\cdots,n_q$. One can create multi-DOF joints using virtual links of zero volume. The *configuration space* is $Q \subseteq \mathbb{S}^{n_q}$, containing *configurations* $q = (q_1, q_2, \cdots, q_{n_q}) \in Q$. The space of joint velocities is $\dot{Q} \subset \ensuremath \mathbb{R}^{n_q}$. There exists a default configuration $0 \in Q$. The *workspace*, $W \subset \ensuremath \mathbb{R}^3$, is the all points in space reachable by any point on the arm in any configuration. The robot's physical limits are as follows. Each joint $i$ has a minimum and maximum position $q_{i,\mathrm{\textnormal{lim}}}^-$ and $q_{i,\mathrm{\textnormal{lim}}}^+$, maximum absolute speed $\dot{q}_{i,\mathrm{\textnormal{lim}}}$ and maximum absolute acceleration $\ddot{q}_{i,\mathrm{\textnormal{lim}}}$.

We now describe the kinematic chain. Each link has a local coordinate frame with the origin located at the link's predecessor joint (the baselink's frame is the global frame). The rotation matrix $R_i(q_i) \in \mathrm{\textnormal{SO}}(3)$ describes the rotation of link $i$ relative to link $i-1$ (by joint $i$). The displacement $l_i \in \ensuremath \mathbb{R}^3$ denotes the position of joint $i$ on link $i$ relative to joint $(i-1)$ in the frame of link $i$. The set $L_i \subset \ensuremath \mathbb{R}^3$ denotes the volume occupied by the $i$^th^ link, with respect to its predecessor joint, in the frame of link $i$. Let $\mathrm{\textnormal{\small{FO}}}_i: Q \to \ensuremath \mathcal{P}(W)$ give the forward occupancy of link $i$. That is, the $i$^th^ link occupies the volume $$\begin{equation}
\label{eq:forward_occupancy_i}
    \mathrm{\textnormal{\small{FO}}}_i(q)~=~\left\{\sum_{j < i}\Bigg(\prod_{n \leq j}R_n(q_n)\,l_j\Bigg)\right\} \oplus \left(\prod_{n\leq i}R_n(q_n) L_i \right) \subset W.
\end{equation}$$ Let $\mathrm{\textnormal{\small{FO}}}: Q \to \ensuremath \mathcal{P}(W)$ give the occupancy of the entire arm: $\mathrm{\textnormal{\small{FO}}}(q) = \bigcup_{i = 1}^{n_q} \mathrm{\textnormal{\small{FO}}}_i(q)$. Note, the first expression in [\[eq:forward_occupancy_i\]](#eq:forward_occupancy_i){reference-type="eqref" reference="eq:forward_occupancy_i"} gives the position of joint $(i-1)$ and the second gives the rotated volume of link $i$. See Appendix [10.1](#apdx:explanation:FO){reference-type="ref" reference="apdx:explanation:FO"} for an example.

### Obstacles

We denote an *obstacle* as a set $O \subset W$. If the arm's volume at $q \in Q$ is intersecting the obstacle, we say the arm is in *collision*, i.e. $\mathrm{\textnormal{\small{FO}}}(q) \cap O \neq \emptyset$. We assume the following about obstacles. Each obstacle is compact and static with respect to time (note, one can extend ARMTD to dynamic obstacles [@Vaskov2019_RSS]). At any time, there are at most $n_\mathrm{\textnormal{obs}}\in \ensuremath \mathbb{N}$, $(n_\mathrm{\textnormal{obs}}< \infty)$ obstacles in the workspace, and the arm has access to a conservative estimate of the size and location of all such obstacles (we are only concerned with planning, not perception). Let $\mathscr{O}= \{O_1,\cdots,O_{n_O}\}$ denote a set of obstacles.

## Receding-Horizon Planning and Timing

ARMTD plans in a receding-horizon way, meaning it generates a short plan, then executes it while generating its next short plan. Every such plan is specified over a compact time interval $T \subset \ensuremath \mathbb{R}$. Without loss of generality (WLOG), since time can be shifted to $0$ at the beginning of any plan, we denote $T = [0, t_\mathrm{\textnormal{f}}]$. We further specify that ARMTD must generate a new plan every $t_\mathrm{\textnormal{plan}}< t_\mathrm{\textnormal{f}}$ seconds. If a collision-free plan cannot be found within $t_\mathrm{\textnormal{plan}}$ s, the robot must continue the plan from the previous receding-horizon iteration; therefore, we include a fail-safe (braking) maneuver in each plan. The durations $t_\mathrm{\textnormal{f}}$ and $t_\mathrm{\textnormal{plan}}$ are chosen such that $(t_\mathrm{\textnormal{f}}- t_\mathrm{\textnormal{plan}})$ is large enough for the arm to stop from its maximum joint speeds given its maximum accelerations. This ensures every plan can include a fail-safe maneuver. We abuse notation to let $q: T \to Q$ denote a trajectory plan and $q_i: T \to Q$ denote the trajectory of the $i^{th}$ joint. A plan is *collision-free* if $\mathrm{\textnormal{\small{FO}}}(q(t)) \cap O = \emptyset \, \forall t \in T,\ \forall\ O \in \mathscr{O}$. Next, we specify the form of each plan.

## Trajectory Parameterization {#subsec:reachability_theory}

ARMTD plans using parameterized trajectories. We describe the theory, then present our implementation.

### Theory

Let $K \subset \ensuremath \mathbb{R}^{n_k}$, $n_k \in \ensuremath \mathbb{N}$, be a compact space of *trajectory parameters*, meaning each $k \in K$ maps to a trajectory $q: T \to Q$. We use $q(t;k)$ to denote the configuration parameterized by $k \in K$ at time $t \in T$. So, in each receding-horizon planning iteration, ARMTD attempts to select a single $k \in K$ (via trajectory optimization with obstacles represented as constraints on $K$.

::: {#def:traj_param_generic .defn}
**Definition 1**. *We require $q: T \to Q$ to satisfy three properties for all $k \in K$. First, $q(\cdot\,; k)$ is at least once-differentiable w.r.t. time. Second, $q(0;k) = 0$. Third, $\dot{q}(t_\mathrm{\textnormal{f}};k) = 0$.*
:::

The second property uses the fact that all joints are revolute, so $q(0 ;k) = 0$ WLOG. The third property guarantees each parameterized trajectory includes a fail-safe braking maneuver.

Note, the parameterized trajectories are kinematic, not dynamic. This is common in motion planning [@chomp; @trajopt; @itomp; @Murray2016_motion_planning_on_chip; @kunz2010_PRM], because existing controllers can track such trajectories closely (e.g., within 0.01 rad for revolute joints [@paden1988globally; @giusti2017_arm_traj_dyn_zono]) in the absence of disturbances such as collisions. We find these trajectories sufficient to avoid collision in real-world hardware demonstrations (Sec. [5](#sec:demos){reference-type="ref" reference="sec:demos"}). Also, methods exist for quantifying tracking error [@giusti2017_arm_traj_dyn_zono; @kousik2019_quadrotor_rtd] and accounting for it at runtime [@kousik2018_RTD_ijrr; @Vaskov2019_RSS].

### Implementation

We choose a parameterization that is simple yet sufficient for safe planning in arbitrary scenarios (see Sec. [5](#sec:demos){reference-type="ref" reference="sec:demos"}). We define a *velocity parameter* $k^{\mathrm{\textnormal{v}}}\in \ensuremath \mathbb{R}^{n_q}$ for the initial velocity $\dot{\tilde{q}}$, and an *acceleration parameter* $k^{\mathrm{\textnormal{a}}}\in \ensuremath \mathbb{R}^{n_q}$ that specifies a constant acceleration over $[0, t_\mathrm{\textnormal{plan}})$. We write $k^{\mathrm{\textnormal{v}}}= (k^{\mathrm{\textnormal{v}}}_1,\cdots,k^{\mathrm{\textnormal{v}}}_{n_q})$ and similarly for $k^{\mathrm{\textnormal{a}}}$. We denote $k = (k^{\mathrm{\textnormal{v}}},k^{\mathrm{\textnormal{a}}}) \in K \subset \ensuremath \mathbb{R}^{n_k}$, where $n_k = 2n_q$. The trajectories are given by $$\begin{align}
\label{eq:traj_parameterization}
    \dot{q}(t;k) = \begin{cases}
        k^{\mathrm{\textnormal{v}}}+ k^{\mathrm{\textnormal{a}}}t, &t \in [0,t_\mathrm{\textnormal{plan}}) \\
        \frac{k^{\mathrm{\textnormal{v}}}+ k^{\mathrm{\textnormal{a}}}t_\mathrm{\textnormal{plan}}}{t_\mathrm{\textnormal{f}}- t_\mathrm{\textnormal{plan}}}(t_\mathrm{\textnormal{f}}- t), &t \in [t_\mathrm{\textnormal{plan}},t_\mathrm{\textnormal{f}}],
    \end{cases},
\end{align}$$ with $q_i(0;k) = 0$ for all $k$ to satisfy Def. [1](#def:traj_param_generic){reference-type="ref" reference="def:traj_param_generic"}. These trajectories brake to a stop over $[t_\mathrm{\textnormal{plan}}, t_\mathrm{\textnormal{f}}]$ with constant acceleration.

We require that $K$ is compact to perform reachability analysis (Sec. [3](#sec:reachability){reference-type="ref" reference="sec:reachability"}). Let $K_i$ denote the parameters for joint $i$. For each joint $i$, we specify $K_i = K_{i}^{\mathrm{\textnormal{v}}}\times K_{i}^{\mathrm{\textnormal{a}}}$, where $$\begin{align}
    K_{i}^{\mathrm{\textnormal{v}}}= \left[\overline{k_{i}^{\mathrm{\textnormal{v}}}}- \Delta k_{i}^{\mathrm{\textnormal{v}}},~\overline{k_{i}^{\mathrm{\textnormal{v}}}}+\Delta k_{i}^{\mathrm{\textnormal{v}}}\right],\quad K_{i}^{\mathrm{\textnormal{a}}}= \left[\overline{k_{i}^{\mathrm{\textnormal{a}}}}- \Delta k_{i}^{\mathrm{\textnormal{a}}},~\overline{k_{i}^{\mathrm{\textnormal{a}}}}+\Delta k_{i}^{\mathrm{\textnormal{a}}}\right],
\end{align}$$ with $\overline{k_{i}^{\mathrm{\textnormal{v}}}}$, $\overline{k_{i}^{\mathrm{\textnormal{a}}}}$, $\Delta k_{i}^{\mathrm{\textnormal{v}}}$, $\Delta k_{i}^{\mathrm{\textnormal{a}}}\in \ensuremath \mathbb{R}$ and $\Delta k_{i}^{\mathrm{\textnormal{v}}}, \Delta k_{i}^{\mathrm{\textnormal{a}}}\geq 0$. To implement acceleration limits (i.e., to bound $K_{i}^{\mathrm{\textnormal{a}}}$), we ensure $$\begin{align}
\label{eq:accel_limit_implementation}
    K_{i}^{\mathrm{\textnormal{a}}}= \left[\max\left\{-\ddot{q}_{i,\mathrm{\textnormal{lim}}}, \overline{k_{i}^{\mathrm{\textnormal{a}}}} - \Delta k_{i}^{\mathrm{\textnormal{a}}}\right\}, \min\left\{\ddot{q}_{i,\mathrm{\textnormal{lim}}}, \overline{k_{i}^{\mathrm{\textnormal{a}}}} + \Delta k_{i}^{\mathrm{\textnormal{a}}}\right\} \right].
\end{align}$$

Next, we use these parameterized trajectories to build parameterized reachable sets of joint configurations.

# Offline Reachability Analysis {#sec:reachability}

ARMTD uses short parameterized trajectories of joint angles for trajectory planning. We now describe a Joint Reachable Set (JRS) containing all such parameterized trajectories. All computations in this section are performed offline.

### Theory

Since each $q_i$ represents a rotation, we examine trajectories of $\cos(q_i)$ and $\sin(q_i)$, as shown in Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}. By Def. [1](#def:traj_param_generic){reference-type="ref" reference="def:traj_param_generic"}, $q(\cdot\,;k)$ is at least once differentiable. We can write a differential equation of the sine and cosine as a function of the joint trajectory, where $k$ is a constant: $$\begin{align}
\label{eq:sin_and_cos_diffeq}
    \frac{d}{dt}\begin{bmatrix}
        \cos(q_i(t;k)) \\ \sin(q_i(t;k)) \\ k
    \end{bmatrix} =
    \begin{bmatrix}
        -\sin(q_i(t;k))\dot{q}_i(t;k) \\ \cos(q_i(t;k))\dot{q}_i(t;k) \\ 0
    \end{bmatrix}.
\end{align}$$ We then define the parameterized JRS of the $i$^th^ joint: $$\begin{align}
\begin{split}\label{eq:cos_sin_reach_set}
    \mathscr{J}_i = \bigg\{&(c,s,k)\in \ensuremath \mathbb{R}^2\times K\,\mid\,\exists\,t \in T\ \mathrm{\textnormal{s.t.}}\ q_i \mathrm{\textnormal{ as in Def. \ref{def:traj_param_generic}, }}\\
    & c = \cos(q_i(t;k)),\ s = \sin(q_i(t;k)),\\
    & \mathrm{\textnormal{and }} \tfrac{d}{dt}\big(\cos(q_i(t;k)),\sin(q_i(t;k)),k\big)\ \mathrm{\textnormal{as in \eqref{eq:sin_and_cos_diffeq}}}\bigg\}.
\end{split}
\end{align}$$ We account for different initial joint angles, and use the JRSs to overapproximate the forward occupancy $\mathrm{\textnormal{\small{FO}}}$, in Sec. [4](#sec:online_planning){reference-type="ref" reference="sec:online_planning"}.

### Implementation {#subsec:reachability_implementation}

We represent [\[eq:cos_sin_reach_set\]](#eq:cos_sin_reach_set){reference-type="eqref" reference="eq:cos_sin_reach_set"} using zonotopes, a subclass of polytopes amenable to reachable set computation [@girard2005reachability]. A *zonotope* is a set in $\ensuremath \mathbb{R}^n$ in which each element is a linear combination of a *center* $x \in \ensuremath \mathbb{R}^n$ and *generators* $g^1,\cdots,g^p \in \ensuremath \mathbb{R}^n,\ p \in \ensuremath \mathbb{N}$: $$\begin{align}
\label{eq:zono_long}
Z = \left\lbrace  y \in \mathbb{R}^n \ \Big| \ y = x + \sum_{i = 1}^{p} \beta^i g^i,\ -1 \leq \beta^i \leq 1 \right\rbrace.
\end{align}$$ We denote $Z = (x, g^i, \langle\beta^i\rangle)^p$ as shorthand for a zonotope with center $x$, a set of generators $\{g^i\}_{i=1}^p$, and a set of indeterminate coefficients $\{\langle\beta^i\rangle\}_{i=1}^p$ corresponding to each generator. When an indeterminate coefficient $\langle\beta^i\rangle$ is *evaluated*, or assigned a particular value, we write $\beta^i$ (i.e., without angle brackets).

To represent the JRS, we first choose a time step $\Delta t \in \ensuremath \mathbb{R}$ such that $\frac{t_\mathrm{\textnormal{f}}}{\Delta t} \in \ensuremath \mathbb{N}$ and partition $T$ into $\frac{t_\mathrm{\textnormal{f}}}{\Delta t}$ closed intervals each of length $\Delta t$, indexed by $\ensuremath \mathbb{N}_T = \left\{0,1,\cdots,\tfrac{t_f}{\Delta t}-1\right\}$. We represent $\mathscr{J}_i$ with one zonotope per time interval, which is returned by $J_i: \ensuremath \mathbb{N}_T \to \ensuremath \mathcal{P}(\ensuremath \mathbb{R}^2\times K)$. For example, the zonotope $J_i(n)$ corresponds to the time interval $[n\Delta t, (n+1)\Delta t]$. We abuse notation and let $t$ index the subinterval of $T$ that contains it, so that $J_i(t)= J_i\left(\lfloor t/\Delta t\rfloor\right)$ where $\lfloor\cdot\rfloor$ rounds down to the nearest integer. We use similar notation for the center, generators, and indeterminates.

Next, we make an initial condition zonotope $J_i(0)\subset \ensuremath \mathbb{R}^2\times K$: $$\begin{equation}
\label{eq:CORAinitialSet}
    J_i(0)= \bigg(\tilde{x_i}, \left\{\tilde{g}_{i}^{\mathrm{\textnormal{v}}}, \tilde{g}_{i}^{\mathrm{\textnormal{a}}}\right\}, \left\{\langle\tilde{\kappa}_{i}^{\mathrm{\textnormal{v}}}\rangle,\langle\tilde{\kappa}_{i}^{\mathrm{\textnormal{a}}}\rangle\right\}\bigg),
\end{equation}$$ with $\tilde{x_i}= [1, 0, \overline{k_{i}^{\mathrm{\textnormal{v}}}}, \overline{k_{i}^{\mathrm{\textnormal{a}}}}]^\top$, $\tilde{g}_{i}^{\mathrm{\textnormal{v}}}= [0, 0, \Delta k_{i}^{\mathrm{\textnormal{v}}}, 0 ]^\top$, $\tilde{g}_{i}^{\mathrm{\textnormal{a}}}= [0, 0, 0, \Delta k_{i}^{\mathrm{\textnormal{a}}}]^\top$. The indeterminates $\langle\tilde{\kappa}_{i}^{\mathrm{\textnormal{v}}}\rangle$ and $\langle\tilde{\kappa}_{i}^{\mathrm{\textnormal{a}}}\rangle$ correspond to $\tilde{g}_{i}^{\mathrm{\textnormal{v}}}$ and $\tilde{g}_{i}^{\mathrm{\textnormal{a}}}$. $J_i(0)$ contains $K_{i}^{\mathrm{\textnormal{v}}}$ and $K_{i}^{\mathrm{\textnormal{a}}}$ in the $k_{i}^{\mathrm{\textnormal{v}}}$ and $k_{i}^{\mathrm{\textnormal{a}}}$ dimensions.

Finally, we use an open-source toolbox [@althoff_cora] with the time partition, differential equation [\[eq:sin_and_cos_diffeq\]](#eq:sin_and_cos_diffeq){reference-type="eqref" reference="eq:sin_and_cos_diffeq"} and [\[eq:traj_parameterization\]](#eq:traj_parameterization){reference-type="eqref" reference="eq:traj_parameterization"}, and initial set $J_i(0)$ to overapproximate [\[eq:cos_sin_reach_set\]](#eq:cos_sin_reach_set){reference-type="eqref" reference="eq:cos_sin_reach_set"}. Importantly, by [@althoff2010reachability Thm. 3.3 and Prop. 3.7], one can prove the following: $$\begin{equation}
    \label{eq:zono_overapprox}
    \mathscr{J}_i \subseteq \bigcup_{t \in T}J_i(t).
\end{equation}$$

JRSs are illustrated in Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}. Next, we use the JRSs online to build an RS for the arm and identify unsafe plans in each receding-horizon iteration.

![An overview of the proposed method for a 2-D, 2-link arm. Offline, ARMTD computes the JRSs, shown as the collection of small grey sets $J_i(t)$ overlaid on the unit circle (dashed) in the sine and cosine spaces of two joint angles. Note that each JRS is conservatively approximated, and parameterized by trajectory parameters $K$. Online, the JRSs are composed to form the arm's reachable set $V_i(t)$ (large light grey sets in $W$), maintaining a parameterization by $K$. The obstacle $O$ (light red) is mapped to the unsafe set of trajectory parameters $K_\mathrm{\textnormal{u}}\subset K$ on the left, by intersection with each $V_i(t)$. The parameter $k^{\mathrm{\textnormal{a}}}$ represents a trajectory, shown at five time steps (blue arms in $W$, and blue dots in joint angle space). The subset of the arm's reachable set corresponding to $k^{\mathrm{\textnormal{a}}}$ is shown for the last time step (light blue boxes with black border), critically not intersecting the obstacle, which is guaranteed because $k^{\mathrm{\textnormal{a}}}\not\in K_\mathrm{\textnormal{u}}$. ](Holmes2020Reachable_figs/JRS_explanation.png){#fig:method_overview width="0.95\\columnwidth"}

# Online Planning {#sec:online_planning}

We now present ARMTD's online algorithm for a single receding-horizon iteration (see Alg. [\[alg:online_planning\]](#alg:online_planning){reference-type="ref" reference="alg:online_planning"} and Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}). First, we construct the parameterized RS of the entire arm from the JRS of each joint. Second, we identify unsafe trajectory plans. Third, we optimize over the safe plans to minimize an arbitrary cost function. If no solution is found, we execute the previous plan's fail-safe maneuver. Note, we present self-intersection constraints in Appendix [9](#apdx:self_intersection){reference-type="ref" reference="apdx:self_intersection"}.

## Reachable Set Construction

### Theory

Recall that ARMTD plans while the robot is executing its previous plan. Therefore, ARMTD must estimate its future initial condition $(\tilde{q},\dot{\tilde{q}}) \in Q\times\dot{Q}$ as a result of its previous plan by integrating [\[eq:sin_and_cos_diffeq\]](#eq:sin_and_cos_diffeq){reference-type="eqref" reference="eq:sin_and_cos_diffeq"} for $t_\mathrm{\textnormal{plan}}$ seconds. At the beginning of each online planning iteration, we use $(\tilde{q},\dot{\tilde{q}})$ to compose the RS of the arm from the low-dimensional JRSs. Denote each link's RS $\mathscr{L}_i$, formed from all $\mathscr{J}_j$ with $j \leq i$: $$\begin{align}
\begin{split}\label{eq:RS_of_link_i}
    \mathscr{L}_i = \bigg\{&\big(Y, k\big) \in \ensuremath \mathcal{P}(W) \times K \ \Big|\ \exists\,t\in T\ \mathrm{\textnormal{s.t.}}\\
    &\dot{q}_i(0;k) = \dot{\tilde{q}}_{i},\ Y = \mathrm{\textnormal{\small{FO}}}_i(q(t; k) + \tilde{q}),\\
    &\mathrm{\textnormal{and}}\ \left(\cos(q_j(t; k)), \sin(q_j(t; k)), k\right) \in \mathscr{J}_j\ \forall\ j \leq i \bigg\} 
\end{split}
\end{align}$$ with $\mathrm{\textnormal{\small{FO}}}_i$ as in [\[eq:forward_occupancy_i\]](#eq:forward_occupancy_i){reference-type="eqref" reference="eq:forward_occupancy_i"}. Each $\mathscr{L}_i$ is formed by trajectories which start at the given initial conditions $(\tilde{q},\dot{\tilde{q}})$. The RS of the entire arm, $\mathscr{L}\subset W\times K$, is then $\mathscr{L}= \bigcup_i \mathscr{L}_i$.

### Implementation {#sec:online_RS_implementation}

It is important that we overapproximate $\mathscr{L}$ to guarantee safety when planning. To do this, we overapproximate $\mathrm{\textnormal{\small{FO}}}$ for all configurations in each $\mathscr{J}_i$ (see Alg. [\[alg:compose_reachable_sets\]](#alg:compose_reachable_sets){reference-type="ref" reference="alg:compose_reachable_sets"}).

First, we fix $\dot{\tilde{q}}$ by obtaining subsets of the JRSs containing trajectories with the given initial velocity. To do so, we note a property of the zonotope JRS:

::: {#lem:one_k_sliceable_gen_per_tope .lem}
**Lemma 2**. *There exist $J_i: \ensuremath \mathbb{N}_T \to \ensuremath \mathcal{P}(\ensuremath \mathbb{R}^2\times K)$ that overapproximate $\mathscr{J}_i$ as in [\[eq:zono_overapprox\]](#eq:zono_overapprox){reference-type="eqref" reference="eq:zono_overapprox"} such that, for each $t \in T$, $J_i(t)$ has only one generator with a nonzero element, equal to $\Delta k_{i}^{\mathrm{\textnormal{v}}}$, in the dimension corresponding to $k_{i}^{\mathrm{\textnormal{v}}}$; we denote this generator $g_{i}^{\mathrm{\textnormal{v}}}(t)$. Similarly, $J_i(t)$ has only one generator $g_{i}^{\mathrm{\textnormal{a}}}(t)$ (distinct from $g_{i}^{\mathrm{\textnormal{v}}}(t)$) with a nonzero element, $\Delta k_{i}^{\mathrm{\textnormal{a}}}$, for $k_{i}^{\mathrm{\textnormal{a}}}$.*
:::

Note, the zonotopes created by the open-source toolbox [@althoff_cora] satisfy Lem. [2](#lem:one_k_sliceable_gen_per_tope){reference-type="ref" reference="lem:one_k_sliceable_gen_per_tope"}. For each $J_i(t)$, we denote the center $x_i(t)$, the generators $\{g_{i}^{\mathrm{\textnormal{v}}}(t),g_{i}^{\mathrm{\textnormal{a}}}(t),g_i^j(t)\}$, and the corresponding indeterminates $\left\{\langle\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\rangle,\langle\kappa_{i}^{\mathrm{\textnormal{a}}}(t)\rangle,\langle\beta_i^j(t)\rangle\right\}$ for $j = 1,\cdots, p(t) \in \ensuremath \mathbb{N}$. We write $p(t)$ since the number of generators is not necessarily the same for each $J_i(t)$ [@althoff_cora]. For all $t$ except $0$, $g_{i}^{\mathrm{\textnormal{v}}}(t)$ and $g_{i}^{\mathrm{\textnormal{a}}}(t)$ may have nonzero elements in the cosine and sine dimensions, due to nonzero dynamics and linearization error. The generators $g_{i}^{\mathrm{\textnormal{v}}}(t)$ and $g_{i}^{\mathrm{\textnormal{a}}}(t)$ are important because they let us obtain a subset of the JRS corresponding to a particular choice of parameters $k_{i}^{\mathrm{\textnormal{v}}}$ and $k_{i}^{\mathrm{\textnormal{a}}}$. We refer to this operation as *slicing*, and we call $g_{i}^{\mathrm{\textnormal{v}}}(t)$ and $g_{i}^{\mathrm{\textnormal{a}}}(t)$ *$k^{\mathrm{\textnormal{v}}}$-sliceable* and *$k^{\mathrm{\textnormal{a}}}$-sliceable*, respectively.

To this end, we define $\textnormal{\texttt{slice}}$ in Alg. [\[alg:slice\]](#alg:slice){reference-type="ref" reference="alg:slice"}. We slice a zonotope by taking in a set of indeterminate coefficients and corresponding values with which to evaluate them. We evaluate an indeterminate by multiplying its associated generator by the given value. We then *remove* the corresponding indeterminate from the set. Since any zonotope generator has only one indeterminate, once its indeterminate is evaluated, it is called *fully-sliced*, and added to the center of the zonotope. Later in this section (Def. [4](#def:rotatotope){reference-type="ref" reference="def:rotatotope"}), we construct zonotope-like objects called *rotatotopes*, which have multiple indeterminates per generator (so, a generator could be sliced without being fully-sliced). For additional explanation of slicing, see Appendix [10.2](#apdx:explanation:slicing){reference-type="ref" reference="apdx:explanation:slicing"}.

:::: algorithm
::: algorithmic
// Let $Z = (x,g^i,\langle\beta^i\rangle)^p$ denote the input zonotope or rotatotope

$Z_{\mathrm{\textnormal{sliced}}} \leftarrow (x,g^i,\langle\beta^i\rangle)^p$ // allocate output

$i = 1,\cdots,p$ // iterate over generator/indeterminate pairs

$j = 1,\cdots,n$ // iterate over input values

$\langle\sigma^j\rangle \in \langle\beta^i\rangle$

$g^i \leftarrow \sigma^j g^i$ // multiply generator by value

$\langle\beta^i\rangle \leftarrow \langle\beta^i\rangle \setminus \langle\sigma^j\rangle$ // remove evaluated indeterminate

$\langle\beta^i\rangle = \emptyset$ // if fully-sliced, then $g^i$ is no longer needed

$x \leftarrow x + g^i$ and $g^i \leftarrow \emptyset$ // shift center, remove generator
:::
::::

For each joint $i$, recall that each $J_i(t)$ has generator $g_{i}^{\mathrm{\textnormal{v}}}(t)$, with indeterminate $\langle\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\rangle$ and nonzero element $\Delta k_{i}^{\mathrm{\textnormal{v}}}$ corresponding to the $k_{i}^{\mathrm{\textnormal{v}}}$ dimension. Also, $x_i(t)$ (the center of $J_i(t)$) has the value $\overline{k_{i}^{\mathrm{\textnormal{v}}}}$ in that same dimension. We use $\dot{\tilde{q}}$ to slice each $J_i(t)$: $$\begin{equation}
    S_{i}(t)= \textnormal{\texttt{slice}}\left(J_i(t),\ \langle\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\rangle,\ (\dot{\tilde{q}}- \overline{k_{i}^{\mathrm{\textnormal{v}}}})/\Delta k_{i}^{\mathrm{\textnormal{v}}}\right) \label{eq:slice_init_qdot}
\end{equation}$$ Note, we ensure $\dot{\tilde{q}}\in K_v$ later in this section. We denote $S_{i}(t)= (x_{i}^{\mathrm{\textnormal{v}}}(t), \big\{g_{i}^{\mathrm{\textnormal{a}}}(t),g_i^j(t)\big\}, \big\{\langle\kappa_{i}^{\mathrm{\textnormal{a}}}(t)\rangle,\langle\beta_i^j(t)\rangle\big\})^{p(t)}$, where $x_{i}^{\mathrm{\textnormal{v}}}(t)$ is the new (shifted) center and $p(t) \in \ensuremath \mathbb{N}$ is the new number of generators, other than $g_{i}^{\mathrm{\textnormal{a}}}(t)$, left after slicing. $S_{i}(t)$ contains a set of $\cos(q_i(t ;k))$ and $\sin(q_i(t ;k))$ reachable for a single value of $k_{i}^{\mathrm{\textnormal{v}}}$, but for a range of $k_{i}^{\mathrm{\textnormal{a}}}$. Denote the components of $S_{i}(t)$ as $x_{i}^{\mathrm{\textnormal{v}}}(t)=  [c_i^{\mathrm{\textnormal{v}}},s_i^{\mathrm{\textnormal{v}}}, \dot{\tilde{q}}_i, \overline{k_{i}^{\mathrm{\textnormal{a}}}}]^\top$, $g_{i}^{\mathrm{\textnormal{a}}}(t)= [c_i^{\mathrm{\textnormal{a}}},s_i^{\mathrm{\textnormal{a}}},0,\Delta{k_{i}^{\mathrm{\textnormal{a}}}}]^\top$ and $g_i^j(t)= [c_i^j,s_i^j,0,0]^\top$ for each $j = 1,...,p(t)$. Note from Lem. [2](#lem:one_k_sliceable_gen_per_tope){reference-type="ref" reference="lem:one_k_sliceable_gen_per_tope"} that $c_i^{\mathrm{\textnormal{a}}}$ and $s_i^{\mathrm{\textnormal{a}}}$ are generally non-zero, and $\Delta k_{i}^{\mathrm{\textnormal{a}}}$ is constant.

The forward occupancy map $\mathrm{\textnormal{\small{FO}}}$ uses rotation matrices formed from the cosine and sine of each joint. By overapproximating these matrices, we can overapproximate $\mathrm{\textnormal{\small{FO}}}$. To this end, we represent sets of rotation matrices with matrix zonotopes. A *matrix zonotope* $M \subset \ensuremath \mathbb{R}^{n \times n}$ is a set of matrices parameterized by a center $X$ and generators $G^{1},\cdots, G^{m}$: $$\begin{equation}
    M = \left\lbrace A \in \ensuremath \mathbb{R}^{n \times n} \ \Big| \ A = X + \sum_{j=1}^m G^j\lambda^j, -1 \leq \lambda^j \leq 1 \right\rbrace.
\end{equation}$$ We use $M = (X, G^j, \langle\lambda^j\rangle)^m$ as shorthand for a matrix zonotope with center $X$, generators $\{G^j\}_{j=1}^m$, and indeterminate coefficients $\{\langle\lambda^j\rangle\}_{j=1}^m$. Note, superscripts are indices, not exponentiation, of matrix zonotope generators.

We use each sliced zonotope $S_{i}(t)$ to produce a matrix zonotope $M_i(t)$ that overapproximates the rotation matrices for each joint $i$ at each time $t$. We do so by reshaping the center and generators of $S_{i}(t)$ (and keeping its indeterminates), then rotating the resulting matrix zonotope by the initial joint angle $\tilde{q}$; we call this the `makeMatZono` function in Alg. [\[alg:compose_reachable_sets\]](#alg:compose_reachable_sets){reference-type="ref" reference="alg:compose_reachable_sets"}. See Appendix [10.3](#apdx:explanation:mat_zono){reference-type="ref" reference="apdx:explanation:mat_zono"} for an example of $M_i(t)$.

Importantly, $M_i(t)$ satisfies the following property:

::: {#lem:mat_zono_overapprox_R .lem}
**Lemma 3**. *For any parameterized trajectory $q: T \to Q$ with $k_{i}^{\mathrm{\textnormal{v}}}= \dot{\tilde{q}}$, every $R_i(q_i(t;k)) \in M_i(t)$.*
:::

Now we use $M_i(t)$ to overapproximate the link RS $\mathscr{L}_i$. Given the joint displacements $l_i$ and link volumes $L_i$, we specify $l_j \in \ensuremath \mathbb{R}^3$ as a zonotope with center $l_j$ and no generators, and $L_i$ as a zonotope overapproximating the volume of link $i$. We multiply the matrix zonotopes $M_i(t)$ by $L_i$ to overapproximate a swept volume, hence the following definition:

::: {#def:rotatotope .defn}
**Definition 4**. *Let $Z = (x, g^i, \langle\beta^i\rangle)^p$ be a zonotope and $M = (X, G^j, \langle\lambda^j\rangle)^m$ be a matrix zonotope. Let $MZ := \{y \in \ensuremath \mathbb{R}^n\ |\ y = Az,\ A \in M,\ z \in Z\} \subset \ensuremath \mathbb{R}^n$. We call $MZ$ a *rotatotope*, which can be written: $$\begin{align}
\begin{split}\label{eq:matrix_zono_times_zono}
    MZ = \bigg\{y \in \ensuremath \mathbb{R}^n\ \mid\ &y = Xx + {\textstyle\sum}_i\,\beta^{i}Xg^{i}+ {\textstyle\sum}_j \lambda^{j}G^{j}x + \\
    &+{\textstyle\sum}_{i,j}\, \beta^{i}\lambda^{j}G^{j}g^{i},\ -1 \leq (\beta,\lambda) \leq 1 \bigg\},
\end{split}
\end{align}$$ where $i = 1,\cdots, p$ and $j = 1,\cdots, m$.*
:::

We use the shorthand $MZ = \left(\hat{x}, \hat{g}^r, \langle\gamma^r\rangle\right)^s$ where $\hat{x} = Xx$, $s = (p+1)(m+1)-1$, and the generator and coefficient sets are $$\begin{align*}
    \{\hat{g}^r\}_{r=1}^{s} &= \{Xg^1, \cdots, Xg^p, G^1x, \cdots, G^mx, G^1g^1, \cdots, G^mg^p\} \\
    \{\langle\gamma^r\rangle\}_{r=1}^{s} &= \{\langle\beta^1\rangle,\cdots,\langle\beta^p\rangle,\langle\lambda^1\rangle,\cdots,\langle\lambda^m\rangle,\langle\beta^1\lambda^1\rangle,\cdots,\langle\beta^p\lambda^m\rangle\}.
\end{align*}$$ Rotatotopes are a special class of polynomial zonotopes [@althoff_cora]. Each $\langle\gamma^r\rangle$ for $r > p+m$ is a product of indeterminate coefficients from $M$ and $Z$. For a pair of indeterminate coefficients $\langle\gamma^1\rangle$ and $\langle\gamma^2\rangle$, the notation $\langle\gamma^1\gamma^2\rangle$ indicates the product $\langle\gamma^1\rangle\langle\gamma^2\rangle$. We call $\langle\gamma^1\rangle$ and $\langle\gamma^2\rangle$ the *factors* of $\langle\gamma^1\gamma^2\rangle$.

As noted earlier, we use $\textnormal{\texttt{slice}}$ with rotatotopes, for which we now define removing factors generically. We denote the *removal* of the $i$^th^ indeterminate coefficient of $\langle\gamma^1\gamma^2\cdots\gamma^n\rangle$ as: $$\begin{align}
\label{eq:remove}
    \langle\gamma^1\gamma^2\cdots\gamma^n\rangle\setminus\langle\gamma^i\rangle = \langle\gamma^1\gamma^2\cdots\gamma^{i-1}\gamma^{i+1}\cdots\gamma^n\rangle.
\end{align}$$ We define $\langle\gamma^1\gamma^2\cdots\gamma^n\rangle\setminus\langle\gamma^1\gamma^2\cdots\gamma^n\rangle = \emptyset$. We write $\langle\sigma\rangle \in \langle\gamma^1\gamma^2\cdots\gamma^n\rangle$ to denote that $\langle\sigma\rangle$ is a factor of $\langle\gamma^1\gamma^2\cdots\gamma^n\rangle$.

Two useful properties follow from the rotatotope definition:

::: {#lem:matzono_times_zono_equals_rotato .lem}
**Lemma 5**. *A matrix zonotope times a rotatotope is a rotatotope.*
:::

::: {#lem:mink_sums .lem}
**Lemma 6**. *(Zono/rotatotope Minkowski sum) Consider two zonotopes $X = (x,g_X^i,\langle\zeta^i\rangle)^n$ and $Y = (y,g_Y^j,\langle\psi^j\rangle)^m$. Then $X\oplus Y = (x+y,\{g_X^i,g_Y^j\},\{\langle\zeta^i\rangle,\langle\psi^j\rangle\})_{i=1,j=1}^{i=n,j=m}$, which is a zonotope centered at $x+y$ with all the generators and indeterminates of both $X$ and $Y$. Similarly, for two rotatotopes, $V = (v, g_V^i, \langle\mu^i\rangle)^n$ and $W = (w, g_W^j, \langle\omega^j\rangle)^m)$, $$\begin{align}
\label{eq:mink_sum_rotatotope}
    V \oplus W = \left(v+w, \{g_V^i, g_W^j\}, \{\langle\mu^i\rangle,\langle\omega^j\rangle\}\right)_{i=1,j=1}^{i=n,j=m}.
\end{align}$$*
:::

That is, the Minkowski sum is given by the sum of the centers and the union of the generators/indeterminate sets.

We use rotatotopes to overapproximate the forward occupancy map of each link by *stacking* rotatotopes representing link volume on top of rotatopes representing joint positions:

::: {#lem:rotatotopes_overapprox_FO .lem}
**Lemma 7**. *For any $t \in T$ and $k \in K$, $\mathrm{\textnormal{\small{FO}}}_i(q(t;k)) \subseteq V_i(t)$, where $$\begin{align}
\label{eq:stacking}
    V_i(t)= \bigoplus_{j < i} \Bigg(\prod_{n \leq j}M_n(t)\,\{l_j\}\Bigg) \oplus \left(\prod_{n\leq i}M_n(t)L_i\right) \subset W.
\end{align}$$*
:::

Lem. [7](#lem:rotatotopes_overapprox_FO){reference-type="ref" reference="lem:rotatotopes_overapprox_FO"} lets us overapproximate the RS: $\mathscr{L}_i \subseteq \bigcup_{t \in T}V_i(t)\implies \mathscr{L}\subseteq \bigcup_{t, i} V_i(t)$, as shown in Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}. Alg. [\[alg:compose_reachable_sets\]](#alg:compose_reachable_sets){reference-type="ref" reference="alg:compose_reachable_sets"} computes $V_i(t)$ (see Appendix [10.4](#apdx:explanation:reduction){reference-type="ref" reference="apdx:explanation:reduction"} for further computational details).

Though $V_i(t)\subset W$, many of its generators are $k^{\mathrm{\textnormal{a}}}$-sliceable, because they are the product of $k^{\mathrm{\textnormal{a}}}$-sliceable matrix zonotope generators. Denote $V_i(t)= (\hat{x}_i(t), \hat{g}_i^j(t), \langle\hat{\beta}_i^j(t)\rangle)^{p(t)}$. Formally, the $j$^th^ generator $\hat{g}_i^j(t)$ is $k^{\mathrm{\textnormal{a}}}$-sliceable if there exists at least one $\langle\kappa_{n}^{\mathrm{\textnormal{a}}}(t)\rangle \in \langle\hat{\beta}_i^j(t)\rangle$ with $n \leq i$. This means, by slicing by $k^{\mathrm{\textnormal{a}}}$, we can obtain a subset of $V_i(t)$ corresponding to that parameter. We make the distinction that a generator $\hat{g}_i^j(t)$ is *fully-$k^{\mathrm{\textnormal{a}}}$-sliceable* if *all* of its indeterminates are evaluated when sliced by $k^{\mathrm{\textnormal{a}}}$, i.e. $\langle\hat{\beta}_i^j(t)\rangle \subseteq \bigcup_{n \leq i}\langle\kappa_{n}^{\mathrm{\textnormal{a}}}(t)\rangle$. Fully-$k^{\mathrm{\textnormal{a}}}$-sliceable generators are created by multiplying $k^{\mathrm{\textnormal{a}}}$-sliceable generators with each other or with centers in [\[eq:stacking\]](#eq:stacking){reference-type="eqref" reference="eq:stacking"}. These generators are important because all of their indeterminates are evaluated by the trajectory optimization decision variable $k^{\mathrm{\textnormal{a}}}$, which we use in Sec. [4.2.2](#sec:online_constraint_generation){reference-type="ref" reference="sec:online_constraint_generation"}.

:::: algorithm
::: algorithmic
$t \in T$ // parallel for each time step

$i = 1:n_q$ // for each joint

$\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\leftarrow (\dot{\tilde{q}}- \overline{k_{i}^{\mathrm{\textnormal{v}}}})/(\Delta k_{i}^{\mathrm{\textnormal{v}}})$ // get value for [\[eq:slice_init_qdot\]](#eq:slice_init_qdot){reference-type="eqref" reference="eq:slice_init_qdot"}

$S_{i}(t)\leftarrow \texttt{slice}(J_i(t), \langle\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\rangle, \kappa_{i}^{\mathrm{\textnormal{v}}}(t))$ // slice JRS

$M_i(t)\leftarrow \texttt{makeMatZono}(S_{i}(t),\tilde{q})$

$V_i(t)\leftarrow M_i(t)L_i$ // init $V_i(t)$ for link volume RS

$U_i(t)\leftarrow l_{i-1}$ // init rotatotope for joint location

$j = (i-1):-1:1$ // predecessor joints

$V_i(t)\leftarrow M_j^t V_i(t)$ // rotate link volume

$U_i(t)\leftarrow M_j^t U_i(t)$ // rotate joint location

$j = (i-1):-1:1$ // predecessor joints

$V_i(t)\leftarrow V_i(t)\oplus U_j(t)$ // stack link on joints
:::
::::

## Constraint Generation

### Theory

With the RS composed, we now use $\mathscr{L}$ to find all unsafe trajectory parameters $k \in K_\mathrm{\textnormal{u}}\subseteq K$ that could cause collisions with obstacles. We treat $K_\mathrm{\textnormal{u}}$ as a constraint for trajectory optimization, shown in Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}. Recall $q_{i,\mathrm{\textnormal{lim}}}^-$, $q_{i,\mathrm{\textnormal{lim}}}^+$, and $\dot{q}_{i,\mathrm{\textnormal{lim}}}$ are joint limits. Let $\mathscr{O}$ be a set of obstacles. At each planning iteration, the unsafe trajectory parameters are $K_\mathrm{\textnormal{u}}= K_\mathrm{\textnormal{lim}}\cup K_\mathrm{\textnormal{obs}}$, where $$\begin{align}
\begin{split}K_\mathrm{\textnormal{lim}}&= \big\{k\ |\ \exists\ t \in T\ \mathrm{\textnormal{s.t.}} \ q(t;k) < q_{i,\mathrm{\textnormal{lim}}}^- \ \mathrm{\textnormal{or}}\ q(t;k) > q_{i,\mathrm{\textnormal{lim}}}^+ \label{eq:K_lim}\\
&\quad\quad\quad\mathrm{\textnormal{or}}\ |\dot{q}(t;k)| > \dot{q}_{i,\mathrm{\textnormal{lim}}}\big\}\end{split}\\
    K_\mathrm{\textnormal{obs}}&= \big\{k\ |\ Y \cap O\neq \emptyset,\, (Y,k) \in \mathscr{L},\, O \in \mathscr{O}\big\}.\label{eq:K_obs}
    % \begin{split}K\self &= \big\{k\ |\ Y_i\cap Y_j\neq \emptyset,\, (i,j)\in\selfidx, \label{eq:K_self}\\
    % &\quad\quad\quad(Y_i,k) \in \linkfrs_i,\ \regtext{and}\ (Y_j,k) \in \linkfrs_j\big\}\end{split} \\
\end{align}$$

### Implementation {#sec:online_constraint_generation}

We represent $K_\mathrm{\textnormal{lim}}$ with functions $h_\mathrm{\textnormal{lim}}: K^{\mathrm{\textnormal{a}}}\to \ensuremath \mathbb{R}$. Notice in [\[eq:traj_parameterization\]](#eq:traj_parameterization){reference-type="eqref" reference="eq:traj_parameterization"} that $q(t; k)$ is piecewise quadratic in $k$ and $\dot{q}(t;k)$ is piecewise linear in $k$, so the parameterized trajectory extrema can be computed analytically. We construct $h_\mathrm{\textnormal{lim}}$ from $\dot{\tilde{q}}_{i}$, $q_{i,\mathrm{\textnormal{lim}}}$, and $\dot{q}_{i,\mathrm{\textnormal{lim}}}$, such that $h_\mathrm{\textnormal{lim}}(k^{\mathrm{\textnormal{a}}}) < 0$ when feasible.

To represent $K_\mathrm{\textnormal{obs}}$ (depicted in Fig. [2](#fig:method_overview){reference-type="ref" reference="fig:method_overview"}), first consider a particular $k^{\mathrm{\textnormal{a}}}$. We test if the corresponding subset of each rotatotope $V_i(t)$ could intersect any obstacle $O \in \mathscr{O}$. We overapproximate each $O$ by a zonotope, which is always possible for compact, bounded sets [@althoff2010reachability] that appear in common obstacle representations such as octrees [@meagher1982geometric] or convex polytopes [@lien2007approximate]. To proceed, we must test if two zonotopes intersect:

::: {#lem:zono_int .lem}
**Lemma 8**. *[@guibas2003zonotopes Lem. 5.1] For two zonotopes $X = (x, g^i, \langle\beta^i\rangle)^n$ and $Y = (y, g^j, \langle\beta^j\rangle)^m$, $X \cap Y \neq \emptyset$ iff $y$ is in the zonotope $X_\mathrm{\textnormal{buf}}= (x, g^i, \langle\beta^i\rangle)^n \oplus (0, g^j, \langle\beta^j\rangle)^m$, where the subscript indicates $X$ is buffered by the generators of $Y$.*
:::

Since zonotopes are convex polytopes [@guibas2003zonotopes], by [@althoff2010reachability Theorem 2.1], one can implement Lem. [8](#lem:zono_int){reference-type="ref" reference="lem:zono_int"} by computing a *half-space representation* $(A_\mathrm{\textnormal{buf}},b_\mathrm{\textnormal{buf}})$ of $X_\mathrm{\textnormal{buf}}$ for which $A_\mathrm{\textnormal{buf}}z - b_\mathrm{\textnormal{buf}}\leq 0 \iff z \in X_\mathrm{\textnormal{buf}}$, where the inequality is taken elementwise. Using this representation, $X \bigcap Y = \emptyset \iff \max(A_\mathrm{\textnormal{buf}}y - b_\mathrm{\textnormal{buf}}) > 0$. We can use Lem. [8](#lem:zono_int){reference-type="ref" reference="lem:zono_int"} for collision avoidance by replacing $X$ (resp. $Y$) with a zonotope representing the arm (resp. an obstacle).

However, since we use rotatotopes, we need the following:

::: {#lem:zono_overapprox_rotatotope .lem}
**Lemma 9**. *Any rotatotope $MZ$ as in [\[eq:matrix_zono_times_zono\]](#eq:matrix_zono_times_zono){reference-type="eqref" reference="eq:matrix_zono_times_zono"} can be overapproximated by a zonotope.*
:::

So, we can overapproximate the intersection of each $V_i(t)$, sliced by $k^{\mathrm{\textnormal{a}}}$, with each $O \in \mathscr{O}$. Note, we only slice the fully-$k^{\mathrm{\textnormal{a}}}$-sliceable generators of $V_i(t)$, and treat all other generators conservatively by applying Lemma [9](#lem:zono_overapprox_rotatotope){reference-type="ref" reference="lem:zono_overapprox_rotatotope"}. That is, we do not slice any generators that have any indeterminates in addition to $\langle\kappa_{i}^{\mathrm{\textnormal{a}}}(t)\rangle$, and instead use those generators to (conservatively) buffer obstacles.

To check intersection, we separate $V_i(t)$ into two rotatotopes, $$\begin{align}
\label{eq:vit_split_slice_and_buff}
    V_{i,\mathrm{\textnormal{slc}}}(t)= \left(x_i(t), g_\mathrm{\textnormal{slc}}^j, \langle\kappa_\mathrm{\textnormal{slc}}^j\rangle\right)\ \mathrm{\textnormal{and}}\ V_{i,\mathrm{\textnormal{buf}}}(t)= \left(0, g_\mathrm{\textnormal{buf}}^n, \langle\beta_\mathrm{\textnormal{buf}}^n\rangle\right),
\end{align}$$ such that $V_i(t)= V_{i,\mathrm{\textnormal{slc}}}(t)\oplus V_{i,\mathrm{\textnormal{buf}}}(t)$, where $V_{i,\mathrm{\textnormal{slc}}}(t)$ has only fully-$k^{\mathrm{\textnormal{a}}}$-sliceable generators. That is, each $\langle\kappa_\mathrm{\textnormal{slc}}^j\rangle$ is a product of *only* $\langle\kappa_{i}^{\mathrm{\textnormal{a}}}(t)\rangle$ for one or more $i \in \{1,\cdots,n_q\}$. Note, the number of generators/indeterminates in $V_{i,\mathrm{\textnormal{slc}}}(t)$ and $V_{i,\mathrm{\textnormal{buf}}}(t)$ is omitted to ease notation. For any $k^{\mathrm{\textnormal{a}}}\in K^{\mathrm{\textnormal{a}}}$, since every generator of $V_{i,\mathrm{\textnormal{slc}}}(t)$ is $k^{\mathrm{\textnormal{a}}}$-sliceable, slicing $V_{i,\mathrm{\textnormal{slc}}}(t)$ by $k^{\mathrm{\textnormal{a}}}$ returns a point. We express this with $\textnormal{\texttt{eval}}: \ensuremath \mathcal{P}(W) \times K^{\mathrm{\textnormal{a}}}\to \ensuremath \mathbb{R}^3$ for which $$\begin{align}
\label{eq:eval}
    \textnormal{\texttt{eval}}(V_{i,\mathrm{\textnormal{slc}}}(t), k^{\mathrm{\textnormal{a}}}) = \textnormal{\texttt{slice}}\left(V_{i,\mathrm{\textnormal{slc}}}(t),\big\{\langle\kappa_{i}^{\mathrm{\textnormal{a}}}(t)\rangle\big\}_{i=1}^{n_q},\{\kappa(i)\}_{i=1}^{n_q}\right)
\end{align}$$ where $\kappa(i) = (k_{i}^{\mathrm{\textnormal{a}}}- \overline{k_{i}^{\mathrm{\textnormal{a}}}})/\Delta k_{i}^{\mathrm{\textnormal{a}}}$. Note, $\textnormal{\texttt{eval}}$ can be implemented as the evaluation of polynomials.

Now, let $A_\mathrm{\textnormal{obs}}$ and $b_\mathrm{\textnormal{obs}}$ be the halfspace representation of $O_\mathrm{\textnormal{buf}}= O \oplus V_{i,\mathrm{\textnormal{buf}}}(t)$, and let $x = \textnormal{\texttt{eval}}(V_{i,\mathrm{\textnormal{slc}}}(t),k^{\mathrm{\textnormal{a}}})$. Then, $$\begin{equation}
 \label{eq:sliced_rotato_int_obs}
    \left(\{x\} \oplus V_{i,\mathrm{\textnormal{buf}}}(t)\right) \cap O = \emptyset \iff -\max\{ A_\mathrm{\textnormal{obs}}x - b_\mathrm{\textnormal{obs}}\} < 0
\end{equation}$$ where $\{x\} \oplus V_{i,\mathrm{\textnormal{buf}}}(t)$ is overapproximated as a zonotope by applying Lem. [9](#lem:zono_overapprox_rotatotope){reference-type="ref" reference="lem:zono_overapprox_rotatotope"}. We use [\[eq:sliced_rotato_int_obs\]](#eq:sliced_rotato_int_obs){reference-type="eqref" reference="eq:sliced_rotato_int_obs"} to overapproximate the parameters $K_\mathrm{\textnormal{obs}}$ [\[eq:K_obs\]](#eq:K_obs){reference-type="eqref" reference="eq:K_obs"} with $h_\mathrm{\textnormal{obs}}: \ensuremath \mathbb{N}\times T\times \mathscr{O}\times K^{\mathrm{\textnormal{a}}}\to \ensuremath \mathbb{R}$ for which $$\begin{align}
    \label{eq:h_obs}
    h_\mathrm{\textnormal{obs}}(*,k^{\mathrm{\textnormal{a}}}) = -\max\big\{A_\mathrm{\textnormal{obs}}(*)\textnormal{\texttt{eval}}(V_{i,\mathrm{\textnormal{slc}}}(t),k^{\mathrm{\textnormal{a}}}) - b_\mathrm{\textnormal{obs}}(*)\big\}.
\end{align}$$ where $* = (i,t,O)$ for space. Here, $A_\mathrm{\textnormal{obs}}(i, t, O)$ and $b_\mathrm{\textnormal{obs}}(i, t, O)$ return the halfspace representation of $O \oplus V_{i,\mathrm{\textnormal{buf}}}(t)$. Importantly, for each obstacle, time, and joint, $h_\mathrm{\textnormal{obs}}$ is a max of a linear combination of polynomials in $k^{\mathrm{\textnormal{a}}}$ (per [\[eq:eval\]](#eq:eval){reference-type="eqref" reference="eq:eval"} and Alg. [\[alg:slice\]](#alg:slice){reference-type="ref" reference="alg:slice"}), so we can take its subgradient with respect to $k^{\mathrm{\textnormal{a}}}$ [@boyd2003subgradient] (also see [@polak2012optimization Thm. 5.4.5]). This constraint conservatively approximates $K_\mathrm{\textnormal{obs}}$:

::: {#lem:hobs_is_conservative .lem}
**Lemma 10**. *If $k^{\mathrm{\textnormal{a}}}\in K_\mathrm{\textnormal{obs}}$, then there exists $i \in \ensuremath \mathbb{N}$, $t \in T$, and $O \in \mathscr{O}$ such that $h_\mathrm{\textnormal{obs}}(i,t,O,k^{\mathrm{\textnormal{a}}}) \geq 0$.*
:::

## Trajectory Optimization

### Theory

ARMTD performs trajectory optimization over $K \setminus K_\mathrm{\textnormal{u}}$ for an arbitrary user-specified cost function $f: K \to \ensuremath \mathbb{R}$ (which encodes information such as completing a task). ARMTD attempts to solve the following within $t_\mathrm{\textnormal{plan}}$: $$\begin{align}
\label{prog:trajopt_general}
    k_\mathrm{\textnormal{opt}}= \mathrm{\textnormal{argmin}}_{k}\big\{f(k)\ |\ k \not\in K_\mathrm{\textnormal{u}}\big\}.
\end{align}$$ If no solution is found in time, the robot tracks the fail-safe maneuever from its previous plan.

### Implementation {#sec:online_trajopt}

We implement [\[prog:trajopt_general\]](#prog:trajopt_general){reference-type="eqref" reference="prog:trajopt_general"} as a nonlinear program, denoted `optTraj` in Alg. [\[alg:online_planning\]](#alg:online_planning){reference-type="ref" reference="alg:online_planning"}. $$\begin{align}
\label{prog:trajopt}
    \underset{k^{\mathrm{\textnormal{a}}}\,\in\,K^{\mathrm{\textnormal{a}}}}{\mathrm{\textnormal{argmin}}}\left\{f(k^{\mathrm{\textnormal{a}}})\ |\ h_\mathrm{\textnormal{obs}}(i,t,O,k^{\mathrm{\textnormal{a}}}) < 0,\ h_\mathrm{\textnormal{lim}}(k^{\mathrm{\textnormal{a}}}) < 0\right\}%& \forall\ i \in \{1,\cdots,n_q\}
\end{align}$$ where the constraints hold for all $i \in \{1,\cdots,n_q\},\ t \in T,\ O \in \mathscr{O}$.

::: {#thm:constraints_are_conservative .thm}
**Theorem 11**. *Any feasible solution to [\[prog:trajopt\]](#prog:trajopt){reference-type="eqref" reference="prog:trajopt"} parameterizes a trajectory that is collision-free and obeys joint limits over the time horizon $T$.*
:::

ARMTD uses Alg. [\[alg:online_planning\]](#alg:online_planning){reference-type="ref" reference="alg:online_planning"} at each planning iteration. If the arm does not start in collision, this algorithm ensures that the arm is always safe (see Appendix [8](#apdx:safe_planning){reference-type="ref" reference="apdx:safe_planning"}, also see [@kousik2018_RTD_ijrr Remark 70] or [@Hauser2012_receding_horizon Theorem 1]).

:::: algorithm
::: algorithmic
$\{V_i(t)\} \leftarrow \texttt{composeRS}(\tilde{q},\dot{\tilde{q}})$ // Sec. [4.1.2](#sec:online_RS_implementation){reference-type="ref" reference="sec:online_RS_implementation"} []{#lin:construct_frs label="lin:construct_frs"}

$(h_\mathrm{\textnormal{obs}},h_\mathrm{\textnormal{lim}}) \leftarrow \texttt{makeCons}(\tilde{q},\dot{\tilde{q}},\mathscr{O},\{V_i(t)\})$ // Sec. [4.2.2](#sec:online_constraint_generation){reference-type="ref" reference="sec:online_constraint_generation"}

// solve [\[prog:trajopt\]](#prog:trajopt){reference-type="eqref" reference="prog:trajopt"} within $t_\mathrm{\textnormal{plan}}$ or else return $q_\mathrm{\textnormal{prev}}$

$q_\mathrm{\textnormal{plan}}\leftarrow \texttt{optTraj}\left(f, h_\mathrm{\textnormal{obs}}, h_\mathrm{\textnormal{lim}}, t_\mathrm{\textnormal{plan}}, q_\mathrm{\textnormal{prev}}\right)$ // Sec. [4.3.2](#sec:online_trajopt){reference-type="ref" reference="sec:online_trajopt"} []{#lin:trajopt label="lin:trajopt"}
:::
::::

# Demonstrations {#sec:demos}

We now demonstrate ARMTD in simulation and on hardware using the Fetch mobile manipulator (Fig. [1](#fig:fetch_intro){reference-type="ref" reference="fig:fetch_intro"}). ARMTD is implemented in MATLAB, CUDA, and C++, on a 3.6 GHz computer with an Nvidia Quadro RTX 8000 GPU. See our video: [`youtu.be/ySnux2owlAA`](https://youtu.be/ySnux2owlAA). Our code is available: [`github.com/ramvasudevan/arm_planning`](https://github.com/ramvasudevan/arm_planning).

## Implementation Details

### Manipulator

The Fetch arm has $7$ revolute DOFs [@wise2016fetch]. We consider the first $6$ DOFs, and treat the body as an obstacle. The $7$^th^ DOF controls end effector orientation, which does not affect the volume used for collision checking. We command the hardware via ROS [@quigley2009ros] over WiFi.

### Comparison

To assess the difficulty of our simulated environments, we ran CHOMP [@chomp] via MoveIt [@moveit] (default settings, straight-line initialization). We emphasize that CHOMP is not a receding-horizon planner [@moveit]; it attempts to find a plan from start to goal with a single optimization program. However, CHOMP provides a useful baseline to measure the performance of ARMTD. To the best of our knowledge, no open-source, real-time receding-horizon planner is available for a direct comparison. Note, we report solve times to illustrate that ARMTD is real-time feasible, but the goal of ARMTD is not to solve as fast as possible; instead, we care about finding provably collision-free trajectories in the allotted time $t_\mathrm{\textnormal{plan}}$.

### High-level Planner

Recall that ARMTD performs trajectory optimization using an arbitrary user-specified cost function. In this work, in each planning iteration, we create a cost function for ARMTD using an intermediate waypoint between the arm's current configuration and a global goal. These waypoints are generated by a high-level planner (HLP). Note, the RS and safety constraints generated by ARMTD are independent of the HLP, which is only used for the cost function. To illustrate that ARMTD can enforce safety, we use two different HLPs, neither of which is guaranteed to generate collision-free waypoints. First, a straight-line HLP that generates waypoints along a straight line between the arm and a global goal in configuration space. Second, an RRT\* [@karaman2011sampling] that only ensures the arm's end effector is collision-free. Thus, **ARMTD can act as a safety layer on top of RRT\***. Note, we allot a portion of $t_\mathrm{\textnormal{plan}}$ to the HLP in each iteration, and give ARTMD the rest of $t_\mathrm{\textnormal{plan}}$. We cannot use CHOMP as a receding-horizon planner with these HLP waypoints, because it requires a collision-free goal configuration. For further discussion of the comparison to CHOMP, see Appendix [10.7](#apdx:explanation:seeding_chomp){reference-type="ref" reference="apdx:explanation:seeding_chomp"}.

### Algorithm Implementation

Alg. [\[alg:compose_reachable_sets\]](#alg:compose_reachable_sets){reference-type="ref" reference="alg:compose_reachable_sets"} runs at the start of each ARMTD planning iteration. We use a GPU with CUDA to execute Alg. [\[alg:compose_reachable_sets\]](#alg:compose_reachable_sets){reference-type="ref" reference="alg:compose_reachable_sets"} in parallel, taking approximately $10$--$20$ ms to compose a full RS. The constraint generation step in Alg. [\[alg:online_planning\]](#alg:online_planning){reference-type="ref" reference="alg:online_planning"} is also parallelized across obstacles and time steps (this takes approximately $10$--$20$ ms for $20$ obstacles).

We solve ARMTD's trajectory optimization [\[prog:trajopt\]](#prog:trajopt){reference-type="eqref" reference="prog:trajopt"} using IPOPT [@wachter2006implementation]. The cost function $f$ is $||q(t_\mathrm{\textnormal{f}};k) - q_\mathrm{\textnormal{des}}||_{2}^{2}$, where $q_\mathrm{\textnormal{des}}$ is the waypoint specified by the HLP (straight-line or RRT\*) at each planning iteration. We compute analytic gradients/sub-gradients of the cost function and constraints, and evaluate the constraints in parallel. IPOPT takes $100$--$200$ ms when it finds a feasible solution in a scene with $20$ random obstacles.

### Hyperparameters

To reduce conservatism, we partition $K_{i}^{\mathrm{\textnormal{v}}}$ into $n_{\mathrm{\textnormal{JRS}}} \in \ensuremath \mathbb{N}$ equally-sized intervals and compute one JRS for each interval. At runtime, for each joint, we pick the JRS containing the initial speed $\dot{\tilde{q}}_i$. In each JRS, we set $\Delta k_{i}^{\mathrm{\textnormal{a}}}= \max\left\{ r_{a_2},\ r_{a_1}|\overline{k_{i}^{\mathrm{\textnormal{v}}}}|\right\}$, with $r_{a_1}, r_{a_2} > 0$ so the range of accelerations scales with the absolute value of the mean velocity of each JRS. This reduces conservativism at low speeds, improving maneuverability near obstacles.

We also use these values: $t_\mathrm{\textnormal{plan}}= 0.5$ s, $t_\mathrm{\textnormal{f}}= 1.0$ s, $\Delta t = 0.01$ s, $n_{\mathrm{\textnormal{JRS}}} = 400$, $\dot{q}_{i,\mathrm{\textnormal{lim}}}= \pi \frac{\mathrm{\textnormal{rad}}}{s}$, $\ddot{q}_{i,\mathrm{\textnormal{lim}}}= \pi/3 \frac{\mathrm{\textnormal{rad}}}{s^2}$, $\overline{k_{i}^{\mathrm{\textnormal{a}}}} = 0 \frac{\mathrm{\textnormal{rad}}}{s^2}$, $r_{a_1} = 1/3 s^{-1}$, and $r_{a_2} = \pi/24 \frac{\mathrm{\textnormal{rad}}}{s^2}$. For collision checking, we overapproximate the Fetch's links with cylinders of radius 0.146 m. For further discussion of design choices and hyperparamters, see Appendix [10.6](#apdx:explanation:design){reference-type="ref" reference="apdx:explanation:design"}.

## Simulations

### Setup

:::: {#fig:armtd_chomp_random_scene .figure latex-placement="t"}
![](Holmes2020Reachable_figs/armtd_vs_chomp.png){width="\\columnwidth"}

::: caption
A Random Obstacles scene with $8$ obstacles in which CHOMP [@chomp] converged to a trajectory with a collision (collision configurations shown in red), whereas ARMTD successfully navigated to the goal (green); the start pose is shown in purple. CHOMP fails to move around a small obstacle close to the front of the Fetch.
:::
::::

We created two sets of scenes. The first set, Random Obstacles, shows that ARMTD can handle arbitrary tasks (see Fig. [3](#fig:armtd_chomp_random_scene){reference-type="ref" reference="fig:armtd_chomp_random_scene"}). This set contains 100 tasks with random (but collision-free) start and goal configurations, and random box-shaped obstacles. Obstacle side lengths vary from $1$ to $50$ cm, with 10 scenes for each $n_O = 4, 8, ..., 40$.

The second set, Hard Scenarios, shows that ARMTD guarantees safety where CHOMP converges to an unsafe trajectory. There are seven tasks in the Hard Scenarios set: (1) from below to above a table, (2) from one side of a wall to another, (3) between two vertical posts, (4) from one set of shelves to another, (5) from inside to outside of a box on the ground, (6) from a sink to a cupboard, (7) through a small window. These scenarios are shown in Fig. [4](#fig:hard_scenarios){reference-type="ref" reference="fig:hard_scenarios"} in Appendix [10.5](#apdx:explanation:hard_scenarios){reference-type="ref" reference="apdx:explanation:hard_scenarios"}.

### Results

Table [1](#tab:random_obstacles_results){reference-type="ref" reference="tab:random_obstacles_results"} presents ARMTD (with a straight-line HLP) and CHOMP's results for the Random Obstacles scenarios. ARMTD reached $84/100$ goals and had $0/100$ crashes, meaning ARMTD stopped safely $16/100$ times without finding a new safe trajectory. CHOMP reached $82/100$ goals and had $18/100$ crashes. CHOMP always finds a trajectory, but not necessarily a collision-free one; it can converge to infeasible solutions because it considers a non-convex problem with obstacles as areas of high cost (not as hard constraints). We did not attempt to tune CHOMP to only find feasible plans (e.g., by buffering the arm), since this incurs a tradeoff between safety and performance. Note, in MoveIt, infeasible CHOMP plans are not executed (if detected by an external collision-checker).

We report the mean solve time (MST) of ARMTD over all planning iterations, while the MST for CHOMP is the mean over all 100 tasks. Directly comparing timing is not possible since ARMTD and CHOMP use different planning paradigms; we report MST to confirm ARMTD is capable of real-time planning (note that that ARMTD's MST is less than $t_\mathrm{\textnormal{plan}}= 0.5$).

We also report the mean normalized path distance (MNPD) of the plans produced by each planner (the mean is taken over all 100 tasks). The normalized path distance is a path's total distance (in configuration space), divided by the distance between the start and goal. For example, the straight line from start to goal has a (unitless) normalized path distance of $1$. ARMTD's MNPD is $24\%$ smaller than CHOMP's, which may be because CHOMP's cost rewards path smoothness, whereas ARMTD's cost rewards reaching an intermediate waypoint at each planning iteration (note, path smoothness could be included in ARMTD's cost function).

Table [2](#tab:hard_scenarios_results){reference-type="ref" reference="tab:hard_scenarios_results"} presents results for the Hard Scenarios. With the straight-line HLP, ARMTD does not complete any of the tasks but also has no collisions. With the RRT\* HLP [@karaman2011sampling], ARMTD completes $5/7$ scenarios. CHOMP converges to trajectories with collisions in all of the Hard Scenarios.

## Hardware

See our video: [`youtu.be/ySnux2owlAA`](https://youtu.be/ySnux2owlAA). ARMTD completes arbitrary tasks while safely navigating the Fetch arm around obstacles in scenarios similar to Hard Scenarios (1) and (4). We demonstrate real-time planning by suddenly introducing obstacles (a box, a vase, and a quadrotor) in front of the moving arm. The obstacles are tracked using motion capture, and treated as static in each planning iteration. Since ARMTD performs receding-horizon planning, it can react to the sudden obstacle appearance and continue planning without crashing.

::: {#tab:random_obstacles_results}
    **Random Obstacles**  \% goals   \% crashes   MST \[s\]   MNPD
  ---------------------- ---------- ------------ ----------- -------
              ARMTD + SL     84          0          0.273     1.076
                   CHOMP     82          18         0.177     1.511

  : MST is mean solve time (per planning iteration for ARMTD with a straight-line planner, total for CHOMP) and MNPD is mean normalized path distance. MNPD is only computed for trials where the task was successfully completed, i.e. the path was valid.
:::

::: {#tab:hard_scenarios_results}
    **Hard Scenarios** 1   2   3   4   5   6   7
  -------------------- --- --- --- --- --- --- ---
            ARMTD + SL S   S   S   S   S   S   S
         ARMTD + RRT\* O   O   O   S   O   S   O
                 CHOMP C   C   C   C   C   C   C

  :  Results for the seven Hard Scenario simulations. ARMTD uses straight-line (SL) and RRT\* HLPs. The entries are "O" for task completed, "C" for a crash, or "S" for stopping safely without reaching the goal.
:::

[]{#tab:hard_scenarios_results label="tab:hard_scenarios_results"}

# Conclusion {#sec:conclusion}

This work proposes ARMTD as a real-time, receding-horizon manipulator trajectory planner with safety guarantees. The method proposes novel reachable sets for arms, which enable safety. ARMTD can enforce safety on top of an unsafe path planner such as RRT\*, shown in both simulation and on hardware. Of course, ARMTD has limitations: it may not perform in real time without parallelization, is only demonstrated on 6-DOF planning problems, and has not yet been demonstrated planning around humans. However, because ARMTD uses time-varying reachable sets, it can readily extend to dynamic environments, uncertainty such as tracking error, and planning with grasped objects. The results in this work show promise for practical, safe robotic arm trajectory planning.

::: appendices
# Proofs {#apdx:proofs}

Here, we provide the proof of each mathematical claim in the paper, plus a short explanation of how each claim is useful.

First, we examine the structure of the JRS zonotope representation. This structure enables the creation of *fully-$k$-sliceable* generators when we use the JRS to produce rotatotopes. That is, this lemma enables us to slice the arm's RS to find subsets corresponding to particular trajectory parameters. There exist $J_i: \ensuremath \mathbb{N}_T \to \ensuremath \mathcal{P}(\ensuremath \mathbb{R}^2\times K)$ that overapproximate $\mathscr{J}_i$ as in [\[eq:zono_overapprox\]](#eq:zono_overapprox){reference-type="eqref" reference="eq:zono_overapprox"} such that, for each $t \in T$, $J_i(t)$ has only one generator with a nonzero element, equal to $\Delta k_{i}^{\mathrm{\textnormal{v}}}$, in the dimension corresponding to $k_{i}^{\mathrm{\textnormal{v}}}$, and only one (distinct) generator with a nonzero element, $\Delta k_{i}^{\mathrm{\textnormal{a}}}$, for $k_{i}^{\mathrm{\textnormal{a}}}$. Given $J_i(0)$, the subsequent zonotope $J_i(\Delta t)$ is computed as $J_i(\Delta t) = e^{F\Delta T}J_i(0)+ E$, where $F$ is found by linearizing the dynamics [\[eq:sin_and_cos_diffeq\]](#eq:sin_and_cos_diffeq){reference-type="eqref" reference="eq:sin_and_cos_diffeq"} at $t = 0$ and $E$ is a set that overapproximates the linearization error and the states reached over the interval $[0,\Delta t]$ [@althoff2010reachability Section 3.4.1]. This linearized forward-integration and error-bounding procedure is applied to $J_i(\Delta t)$ to produce $J_i(2\Delta t)$, and so on, to compute all $J_i(t)$ in [\[eq:zono_overapprox\]](#eq:zono_overapprox){reference-type="eqref" reference="eq:zono_overapprox"}. Since $\dot{k} = 0$, we have that $e^{F\Delta}\tilde{g}_{i}^{\mathrm{\textnormal{v}}}$ equals $\tilde{g}_{i}^{\mathrm{\textnormal{v}}}$ in the $k$ dimensions (and therefore each $g_{i}^{\mathrm{\textnormal{v}}}(t)$ does as well, and similarly for $g_{i}^{\mathrm{\textnormal{a}}}(t)$). Since the zero dynamics have no linearization error, one can define $E$ to have zero volume in the $k$ dimensions [@althoff2010reachability Proposition 3.7], meaning no generator of any $J_i(t)$ has a nonzero element in the $k$ dimensions, except for $g_{i}^{\mathrm{\textnormal{v}}}(t)$ and $g_{i}^{\mathrm{\textnormal{a}}}(t)$ (which are defined with such nonzero elements).

We now note that all rotation matrices are contained in the matrix zonotopes $M_i(t)$, which are produced by slicing and reshaping the JRS zonotopes. This enables us to conservatively approximate the forward occupancy map.

For any parameterized trajectory $q: T \to Q$ with $k_{i}^{\mathrm{\textnormal{v}}}= \dot{\tilde{q}}$, every $R_i(q_i(t;k)) \in M_i(t)$. By [@althoff2010reachability Thm. 3.3 and Prop. 3.7], all values attained by the sines and cosines of the joint angles are contained in each $J_i(t)$. By Alg. [\[alg:slice\]](#alg:slice){reference-type="ref" reference="alg:slice"} and [\[eq:slice_init_qdot\]](#eq:slice_init_qdot){reference-type="eqref" reference="eq:slice_init_qdot"}, each $S_{i}(t)$ only contains the values of sine and cosine of $q(t;k)$ for which $k_{i}^{\mathrm{\textnormal{v}}}= \dot{\tilde{q}}$. Since $M_i(t)$ only reshapes $S_{i}(t)$, the proof is complete.

The following lemma confirms that the product of multiple matrix zonotopes times a zonotope is still a rotatotope. This is necessary to overapproximate the forward occupancy map, wherein the arm's joint rotation matrices are multiplied together (and, analogously, the matrix zonotopes are multiplied together).

A matrix zonotope times a rotatotope is a rotatotope. This follows from the rotatotope definition.

We use the Minkowski sums of zonotopes and rotatotopes to enable stacking, which is how we build an RS of the entire arm from the low-dimensional JRSs. We also use the Minkowski sum to dilate obstacles, which is necessary to check for intersection with our arm's RS per Lem. [8](#lem:zono_int){reference-type="ref" reference="lem:zono_int"} (which we do not prove here, as it is proven in [@guibas2003zonotopes]).

Consider two zonotopes $X = (x,g_X^i,\langle\zeta^i\rangle)^n$ and $Y = (y,g_Y^j,\langle\psi^j\rangle)^m$. Then $X\oplus Y = (x+y,\{g_X^i,g_Y^j\},\{\langle\zeta^i\rangle,\langle\psi^j\rangle\})_{i=1,j=1}^{i=n,j=m}$, which is a zonotope centered at $x+y$ with all the generators and indeterminates of both $X$ and $Y$. Similarly, for two rotatotopes, $V = (v, g_V^i, \langle\mu^i\rangle)^n$ and $W = (w, g_W^j, \langle\omega^j\rangle)^m)$, $$\begin{align}
    V \oplus W = \left(v+w, \{g_V^i, g_W^j\}, \{\langle\mu^i\rangle,\langle\omega^j\rangle\}\right)_{i=1,j=1}^{i=n,j=m}.\tag{\ref{eq:mink_sum_rotatotope}}
\end{align}$$ This follows from the zonotope definition [\[eq:zono_long\]](#eq:zono_long){reference-type="eqref" reference="eq:zono_long"} and rotatotope definition (Def. [4](#def:rotatotope){reference-type="ref" reference="def:rotatotope"}).

The following lemma confirms that the sliced and stacked rotatotopes $V_i(t)$ overapproximate the forward occupancy map $\mathrm{\textnormal{\small{FO}}}$ for each $i$^th^ link.

For any $t \in T$ and $k \in K$, $\mathrm{\textnormal{\small{FO}}}_i(q(t;k)) \subseteq V_i(t)$, where $$\begin{align}
    V_i(t)= \bigoplus_{j < i} \Bigg(\prod_{n \leq j}M_n(t)\,\{l_j\}\Bigg) \oplus \left(\prod_{n\leq i}M_n(t)L_i\right) \subset W.\tag{\ref{eq:stacking}}
\end{align}$$ First, note [\[eq:stacking\]](#eq:stacking){reference-type="eqref" reference="eq:stacking"} is defined analogously to [\[eq:forward_occupancy_i\]](#eq:forward_occupancy_i){reference-type="eqref" reference="eq:forward_occupancy_i"}. We have $R_i(q_i(t;k)) \in M_i(t)$ from Lem. [3](#lem:mat_zono_overapprox_R){reference-type="ref" reference="lem:mat_zono_overapprox_R"}. The product of matrix zonotopes multiplied by a zonotope is a rotatope by Def. [4](#def:rotatotope){reference-type="ref" reference="def:rotatotope"}, and the Minkowski sum of rotatotopes are given exactly using Lem. [6](#lem:mink_sums){reference-type="ref" reference="lem:mink_sums"}. Therefore, all sets and operations in [\[eq:stacking\]](#eq:stacking){reference-type="eqref" reference="eq:stacking"} are exact or conservative (note, we can overapproximate $L_i$ with a zonotope), so $\mathrm{\textnormal{\small{FO}}}_i(q(t ;k)) \subseteq V_i(t)$.

We use this next lemma to overapproximate the swept volume of the arm (represented with rotatotopes); the overapproximation means that ARMTD is provably conservative, which enables safety guarantees.

Any rotatotope $MZ$ as in [\[eq:matrix_zono_times_zono\]](#eq:matrix_zono_times_zono){reference-type="eqref" reference="eq:matrix_zono_times_zono"} can be overapproximated by a zonotope. Consider the components of the indeterminate coefficients of $MZ = (x,g^r,\langle\gamma^r\rangle)^s$ that can be written as $\langle\beta^i\lambda^j\rangle$. When evaluated, $\beta^i\lambda^j \in [-1,1]$. Consider a zonotope $\hat{Z} = (x,g^r,\langle\sigma^r\rangle)^s$ with the same center and generators as $MZ$, but where each product $\langle\beta^i\lambda^j\rangle$ is replaced with a single new symbolic coefficient $\langle\sigma^r\rangle$. If $z \in MZ$, $\exists\ \sigma^r \in [-1,1]$ such that $z \in \hat{Z}$.

The following lemma confirms that our unsafe set representation (the function $h_\mathrm{\textnormal{obs}}$) is conservative.

If $k^{\mathrm{\textnormal{a}}}\in K_\mathrm{\textnormal{obs}}$, then there exists $i \in \ensuremath \mathbb{N}$, $t \in T$, and $O \in \mathscr{O}$ such that $h_\mathrm{\textnormal{obs}}(i,t,O,k^{\mathrm{\textnormal{a}}}) \geq 0$. This follows from Lems. [7](#lem:rotatotopes_overapprox_FO){reference-type="ref" reference="lem:rotatotopes_overapprox_FO"} and [8](#lem:zono_int){reference-type="ref" reference="lem:zono_int"}; $h_\mathrm{\textnormal{obs}}$ is positive when the zonotope produced by slicing $V_i(t)$ intersects $O$, and $V_i(t)$ provably contains all points in workspace reachable by the arm under the trajectory parameterized by $k^{\mathrm{\textnormal{a}}}$.

The following theorem, the main result in this paper, confirms that feasible parameters for the constraints we generate are collision free and obey joint limits. Note, we consider self-intersection below, in Appx. [9](#apdx:self_intersection){reference-type="ref" reference="apdx:self_intersection"}.

Any feasible solution to [\[prog:trajopt\]](#prog:trajopt){reference-type="eqref" reference="prog:trajopt"} parameterizes a trajectory that is collision-free and obeys joint limits over the time horizon $T$. The conservatism of $h_\mathrm{\textnormal{obs}}$ follows from Lem. [9](#lem:zono_overapprox_rotatotope){reference-type="ref" reference="lem:zono_overapprox_rotatotope"}, since each $J_i(t)$ is conservatively transformed into $V_i(t)$; $h_\mathrm{\textnormal{lim}}$ is conservative by construction.

# Safe Receding-Horizon Planning {#apdx:safe_planning}

ARMTD uses Alg. [\[alg:online_planning\]](#alg:online_planning){reference-type="ref" reference="alg:online_planning"} at each planning iteration. Recall that, without loss of generality, each iteration generates a plan over the time horizon $T = [0,t_\mathrm{\textnormal{f}}]$ (by shifting the current time to $0$). Also recall, at each iteration, we allot $t_\mathrm{\textnormal{plan}}$ s within which to find a new plan. The initial position and velocity of each joint in each iteration is the position and velocity, at time $t_\mathrm{\textnormal{plan}}$, of the trajectory plan of the previous iteration. ARMTD attempts to find a safe trajectory within $t_\mathrm{\textnormal{plan}}$ by optimizing over a set of safe trajectory parameters; Thm. [11](#thm:constraints_are_conservative){reference-type="ref" reference="thm:constraints_are_conservative"} ensures that any feasible solution is actually collision-free. If no safe trajectory is found within the allotted time, the arm executes the braking maneuver specified by the previous safe trajectory. Assuming the arm does not start in collision, this algorithm ensures that the arm is always safe (see [@kousik2018_RTD_ijrr Remark 70] or [@Hauser2012_receding_horizon Theorem 1]).

# Self-Intersection Constraints {#apdx:self_intersection}

Typical arms must avoid self-intersection between their links. We specify $I_\mathrm{\textnormal{self}}\subset \ensuremath \mathbb{N}^2$ as a set of joint index pairs for which the links can intersect. That is, for $(i,j) \in I_\mathrm{\textnormal{self}}$, there exist $q \in Q$ such that $\mathrm{\textnormal{\small{FO}}}_i(q) \cap \mathrm{\textnormal{\small{FO}}}_j(q) \neq \emptyset$. For example, one may have $I_\mathrm{\textnormal{self}}= \{(1,3),(1,4),(2,4)\}$ for an arm with 4 links and three possible self-intersections.

We represent self-intersection constraints similarly to how we represent collision-avoidance constraints, with a function $h_\mathrm{\textnormal{self}}: \ensuremath \mathbb{N}\times\ensuremath \mathbb{N}\times T \times K^{\mathrm{\textnormal{a}}}\to \ensuremath \mathbb{R}$. Suppose $(i,j) \in I_\mathrm{\textnormal{self}}\subset \ensuremath \mathbb{N}^2$ indexes a pair of links that could intersect, whose volume is overapproximated by $V_i(t)$ and $V_j(t)$. In analogy to [\[eq:vit_split_slice_and_buff\]](#eq:vit_split_slice_and_buff){reference-type="eqref" reference="eq:vit_split_slice_and_buff"}, define $$\begin{align}
    V_\mathrm{\textnormal{self}}(i,j,t) &= V_{i,\mathrm{\textnormal{slc}}}(t)\oplus (-V_{j,\mathrm{\textnormal{slc}}}(t)) \quad \mathrm{\textnormal{and}} \\
    V_\mathrm{\textnormal{buf}}(i,j,t) &= V_{i,\mathrm{\textnormal{buf}}}(t)\oplus V_{j,\mathrm{\textnormal{buf}}}(t),
\end{align}$$ where $-V_{j,\mathrm{\textnormal{slc}}}(t)$ means the center and generators are multiplied by $-1$. Let $A_\mathrm{\textnormal{self}}(i,j,t)$ and $b_\mathrm{\textnormal{self}}(i,j,t)$ return the half-space representation of $V_\mathrm{\textnormal{buf}}(i,j,t)$. Then, using $*$ in place of the arguments $(i,j,t)$ for space, $$\begin{align}
    h_\mathrm{\textnormal{self}}(*,k^{\mathrm{\textnormal{a}}}) = -\max\left(A_\mathrm{\textnormal{self}}(*)\textnormal{\texttt{eval}}(V_\mathrm{\textnormal{self}}(*),k^{\mathrm{\textnormal{a}}}) - b_\mathrm{\textnormal{self}}(*)\right).
\end{align}$$ As with $h_\mathrm{\textnormal{obs}}$, $h_\mathrm{\textnormal{self}}$ is a max of a linear combination of polynomials in $k^{\mathrm{\textnormal{a}}}$, so we can take the subgradient with respect to $k^{\mathrm{\textnormal{a}}}$. Note one can prove a similar result to Lem. [10](#lem:hobs_is_conservative){reference-type="ref" reference="lem:hobs_is_conservative"} for $h_\mathrm{\textnormal{self}}$.

With these self-intersection constraints, we again implement [\[prog:trajopt_general\]](#prog:trajopt_general){reference-type="eqref" reference="prog:trajopt_general"} as a nonlinear program, denoted `optTraj` in Alg. [\[alg:online_planning\]](#alg:online_planning){reference-type="ref" reference="alg:online_planning"}. $$\begin{align}
\label{prog:trajopt_self}
\begin{array}{cll}
    \underset{k^{\mathrm{\textnormal{a}}}\in K^{\mathrm{\textnormal{a}}}}{\mathrm{\textnormal{argmin}}} & f(k^{\mathrm{\textnormal{a}}}) & \\
    \mathrm{\textnormal{s.t.}} & h_\mathrm{\textnormal{obs}}(i,t,O,k^{\mathrm{\textnormal{a}}}) < 0 & \forall\ i \in \{1,\cdots,n_q\},\ t \in T,\ O \in \mathscr{O}\\
    & h_\mathrm{\textnormal{self}}(i,j,t,k^{\mathrm{\textnormal{a}}}) < 0 & \forall\ (i,j) \in I_\mathrm{\textnormal{self}},\ t \in T \\
    & h_\mathrm{\textnormal{lim}}(k^{\mathrm{\textnormal{a}}}) < 0 & \forall\ i \in \{1,\cdots,n_q\}.
\end{array}
\end{align}$$

# Additional Explanations {#apdx:explanation}

## Forward Occupancy Example {#apdx:explanation:FO}

For an arm with $n_q > 2$, $\mathrm{\textnormal{\small{FO}}}_i$ as in [\[eq:forward_occupancy_i\]](#eq:forward_occupancy_i){reference-type="ref" reference="eq:forward_occupancy_i"} can be written: $$\begin{align}
\begin{split}
    \mathrm{\textnormal{\small{FO}}}_i(q)~=~&\Bigg\{R_1(q_1)l_1 + R_1(q_1)R_2(q_2)l_2 + \cdots\\
    &\cdots + \prod_{j\leq (i-1)}R_j(q_j)l_{i-1}\Bigg\}\oplus \left(\prod_{j\leq i}R_j(q_j)L_i\right).
\end{split}
\end{align}$$ Notice that in this example, the rotated link volume of the $i$^th^ given by $\left(\prod_{j\leq i}R_j(q_j)L_i\right)$ is \"stacked\" on top of the sum of the positions of all predecessor joints.

## Slicing {#apdx:explanation:slicing}

ARMTD uses zonotopes and rotatotopes to represent RSs of parameterized trajectories of an arm. In Sec. [4](#sec:online_planning){reference-type="ref" reference="sec:online_planning"}, our trajectory optimization implementation requires obtaining subsets of the RS corresponding to a particular choice of trajectory parameters. We call this operation *slicing*, because it takes in a zono/rotatotope, evaluates some (or all) of its coefficients, and returns a zono/rotatotope that is a subset of the original with potentially fewer (or no) generators.

We define the $\textnormal{\texttt{slice}}$ function in Alg. [\[alg:slice\]](#alg:slice){reference-type="ref" reference="alg:slice"} using indeterminate evaluation and removal. This function takes in a zono/rotatotope $Z = (x,g^i,\langle\beta^i\rangle)^p$, a set of indeterminate coefficients $\{\langle\sigma^j\rangle\}_{j=1}^m$, and a set of values for the indeterminate coefficients $\{\sigma^j\}_{j=1}^m$, and outputs a sliced zono/rotatotope. For each generator in $Z$, if $\langle\sigma^j\rangle$ is a factor of that generator's coefficients (as in [\[eq:remove\]](#eq:remove){reference-type="eqref" reference="eq:remove"}), then the generator is multiplied by the value $\sigma^j$. If a generator becomes fully-sliced (and therefore has no more indeterminate coefficients), it is added to the center of the output zono/rotatotope, and removed from the set of generators. For zonotopes, each generator becomes fully-sliced if its coefficient is evaluated because each coefficient has only one factor. If a rotatotope is sliced until each generator has only one coefficient factor, the rotatotope becomes a zonotope.

To understand slicing, consider a particular choice of the trajectory parameter $k_{i}^{\mathrm{\textnormal{v}}}$, as in [\[eq:slice_init_qdot\]](#eq:slice_init_qdot){reference-type="eqref" reference="eq:slice_init_qdot"}. We want to obtain the subset of the JRS representing reachable joint angles corresponding to this particular trajectory parameter. For each $J_i(t)$, only the generator $g_{i}^{\mathrm{\textnormal{v}}}(t)$ is non-zero in the dimension corresponding to this trajectory parameter, meaning this $k^{\mathrm{\textnormal{v}}}$-sliceable generator is solely responsible for the volume of the reachable set in this dimension. Choosing a particular value of the trajectory parameter means fixing this generator's indeterminate $\langle\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\rangle$ to a particular value. Since the $k^{\mathrm{\textnormal{v}}}$-sliceable generator is (generally) non-zero in the cosine and sine dimensions as well, the slicing operation returns a subset of the JRS in those dimensions (that is, by fixing the value of this indeterminate, we do not lose all of the JRS's volume in the cosine/sine dimensions, whereas the volume in the $k$-dimensions goes to zero). For example, $\textnormal{\texttt{slice}}\left(J_i(t),\left\{\langle\kappa_{i}^{\mathrm{\textnormal{v}}}(t)\rangle\right\},\left\{\frac{\pi}{6}\right\} \right)$ returns the subset of $J_i(t)$ corresponding to setting $k_{i}^{\mathrm{\textnormal{v}}}= \frac{\pi}{6}$ rad/$s$ (provided that $\frac{\pi}{6} \in K_{i}^{\mathrm{\textnormal{v}}}$).

## Matrix Zonotope Example {#apdx:explanation:mat_zono}

This example constructs $M_i(t)$ from $S_{i}(t)$ by reshaping the center and generators. Suppose joint $i$ rotates about the $3$-axis of link $i-1$. Then:, by [@lavalle_textbook (3.39)], we have $$\begin{align}
\label{eq:mat_zono_construct_implementation}
    M_i(t)&= R_i(\tilde{q}_{i})\left(X_{i}^{\mathrm{\textnormal{v}}}(t),\left\{G_{i}^{\mathrm{\textnormal{a}}}(t),G_i^j(t)\right\},\left\{\langle\kappa_{i}^{\mathrm{\textnormal{a}}}(t)\rangle,\langle\beta_i^j(t)\rangle\right\}\right)^{p(t)},\\
    X_{i}^{\mathrm{\textnormal{v}}}(t)&= \begin{bmatrix}
        c_i^{\mathrm{\textnormal{v}}} & -s_i^{\mathrm{\textnormal{v}}} & 0 \\
        s_i^{\mathrm{\textnormal{v}}} & c_i^{\mathrm{\textnormal{v}}} & 0 \\
        0 & 0 & 1
    \end{bmatrix} ,\ 
    G_{i}^{\mathrm{\textnormal{a}}}(t) = \begin{bmatrix}
        c_i^{\mathrm{\textnormal{a}}} & -s_i^{\mathrm{\textnormal{a}}} & 0 \\
        s_i^{\mathrm{\textnormal{a}}} & c_i^{\mathrm{\textnormal{a}}} & 0 \\
        0 & 0 & 0 \\
    \end{bmatrix},\\
    G_i^j(t)&= \begin{bmatrix}
        c_i^j & -s_i^j & 0 \\
        s_i^j & c_i^j & 0 \\
        0 & 0 & 0 \\
    \end{bmatrix}.
\end{align}$$ Since each $S_{i}(t)$ is computed assuming $q_i(0 ;k) = 0$, we include $R_i(\tilde{q}_i)$ when constructing $M_i(t)$ to correct for each initial joint angle. For different joint axes, $M_i(t)$ can be constructed accordingly [@lavalle_textbook Chapter 3.2.3].

## Reduction of Generators {#apdx:explanation:reduction}

Creating the rotatotopes $V_i(t)$ in [\[eq:stacking\]](#eq:stacking){reference-type="eqref" reference="eq:stacking"} requires multiplying generators together and storing their product. For example, a matrix zonotope described by $10$ matrices (a center and $9$ generators) multiplied by a zonotope described $2$ vectors (a center and $1$ generator) yields a rotatotope described by $20$ vectors (a center and $19$ generators). Because this process is repeated for each joint, the number of generators theoretically required to represent each rotatotope grows exponentially with the number of joints. In practice, many of these generators are very small, and their effect can be overapproximated without adding much conservatism to the RS.

We conservatively approximate [\[eq:stacking\]](#eq:stacking){reference-type="eqref" reference="eq:stacking"} by reducing the number of generators after each product, with a $\textnormal{\texttt{reduce}}$ function implemented as in [@althoff2010reachability Proposition 2.2 and Heuristic 2.1]. The $\textnormal{\texttt{reduce}}$ function keeps the largest $n_\mathrm{\textnormal{red}}$ generators according to a user-defined metric (we used the $L^2$-norm), then overapproximates the rest of the generators with an axis-aligned box. This ensures the number of rotatotope generators never exceeds a user-specified size. From Lem. [2](#lem:one_k_sliceable_gen_per_tope){reference-type="ref" reference="lem:one_k_sliceable_gen_per_tope"}, each $M_i(t)$ has $k^{\mathrm{\textnormal{a}}}$-sliceable generators. If a $k^{\mathrm{\textnormal{a}}}$-sliceable generator is chosen for reduction, we no longer consider it $k^{\mathrm{\textnormal{a}}}$-sliceable. This is a conservative approach, because slicing reduces the volume of a rotatotope in Alg. [\[alg:slice\]](#alg:slice){reference-type="ref" reference="alg:slice"}. A generator that is no longer $k^{\mathrm{\textnormal{a}}}$-sliceable cannot decrease the volume of the RS for any choice of $k^{\mathrm{\textnormal{a}}}$.

## Hard Scenarios {#apdx:explanation:hard_scenarios}

:::: {#fig:hard_scenarios .figure latex-placement="!ht"}
![](Holmes2020Reachable_figs/hard_scenarios.png){width="\\textwidth"}

::: caption
The set of seven Hard Scenarios (number in the top left), with start pose shown in purple and goal pose shown in green. There are seven tasks in the Hard Scenarios set: (1) from below to above a table, (2) from one side of a wall to another, (3) between two vertical posts, (4) from one set of shelves to another, (5) from inside to outside of a box on the ground, (6) from a sink to a cupboard, (7) through a small window.
:::
::::

The set of Hard Scenarios is shown in Fig. [4](#fig:hard_scenarios){reference-type="ref" reference="fig:hard_scenarios"}.

## Design Choices and Hyperparameters {#apdx:explanation:design}

ARMTD has several design choices and hyperparameters, all of which can impact the time required for online planning, but none of which impact the strict safety guarantees. That is, **ARMTD guarantees safety independent of design choices**.

The first design choice to consider is the trajectory parameterization. While we provide a generic definition (Def. [1](#def:traj_param_generic){reference-type="ref" reference="def:traj_param_generic"}), we find that parameterizing velocities and accelerations in our implementation provides a physical intuition for the planned trajectories. For future work, we plan to explore other parameterizations that provide, for example, smoother motion profiles.

The next design choice to consider are those that define the user-specified cost function, generated at each receding-horizon planning iteration. A more non-convex cost function can slow down online planning. In this work, we generate the cost function by using a high-level planner (HLP) such as an RRT\* to generate waypoints between the robot's current location and the global goal. Importantly, the waypoints need not be collision-free; they are used to create a cost function that rewards reaching the waypoint, but ARMTD's safety constraints take care of collision-avoidance. Therefore, **ARMTD provides a safety layer on top of RRT\*** or any other HLP (e.g., PRM, or simply picking a waypoint along a straight-line between the robot and the goal).

There are two hyperparameters that determine a tradeoff between conservatism and online planning speed (without impacting safety). The first is the density of the time partition for the JRS. That is, if we partition time more finely to generate the zonotope JRS, then it takes longer to generate and evaluate constraints at runtime (because we have to consider more zonotopes), but the JRS is also less conservative (so, the robot has more free space to move through).

The second hyperparameter is the range of parameters in the trajectory parameterization. A larger range produces a more conservative JRS, because the same number of zonotopes (determined by the time partition) must contain a larger range of joint angles achieved by all parameterized trajectories. We mitigate this problem in practice by precomputing many JRSs (in this work, we used $400$), each of which has a narrow range of initial velocity parameters $K_{i}^{\mathrm{\textnormal{v}}}$. We choose the range of acceleration parameters $K_{i}^{\mathrm{\textnormal{a}}}$ to vary with the velocity parameters, so that at higher speeds, there is a larger range of available control actions. This reduces conservatism at lower speeds so that ARMTD can maneuver tightly around obstacles.

Note, each JRS only takes around $1$ s to compute, since it is only for a single joint, and for the low-dimensional cosine/sine dynamics. At runtime, to construct the RS of the entire arm, we first select the JRS (for each joint) containing the current initial velocity within its narrow range. Then, we slice by the exact initial velocity to produce the RS, and the corresponding collision-avoidance constraints.

## Seeding CHOMP with RRT\* {#apdx:explanation:seeding_chomp}

CHOMP performs better when seeded with a path output by RRT\*, as opposed to the default straight-line initialization [@chomp; @moveit]. Given that ARMTD uses RRT\* to generate waypoints at each receding-horizon planning iteration, one may wonder why we do not use the same RRT\* to seed CHOMP. However, ARMTD and CHOMP use RRT\* in fundamentally different ways. ARMTD plans in a receding-horizon way, so its runtime and safety guarantees are not dependent on the RRT\* output. On the other hand, CHOMP would require the RRT\* to run for some (unknown) duration, then perform trajectory optimization. In other words, CHOMP requires additional planning time for seeding, whereas ARMTD does not. So, in terms of the most important metric in this work (finding a collision-free trajectory in under $t_\mathrm{\textnormal{plan}}= 0.5$ s), it is unclear how much time to dedicate for RRT\* and how much for CHOMP.

The challenge of generating a fair comparison is compounded by the fact that ARMTD does not require the output of the RRT\* to be collision-free. One could potentially use CHOMP in a receding-horizon way, by attempting to reach an intermediate waypoint generated by RRT\* in each planning iteration. But, the available open-source CHOMP implementation (via MoveIt! [@moveit]) requires the goal (i.e., intermediate waypoint) to be collision-free. Implementing CHOMP in a more generalized receding-horizon framework is outside the scope of the present work.
:::

[^1]: This work is supported by the Ford Motor Company via the Ford-UM Alliance under award N022977, and the Office of Naval Research under award number N00014-18-1-2575.

[^2]: $^{1}$Mechanical Engineering, University of Michigan, Ann Arbor, MI. `@umich.edu`

[^3]: $^{2}$Robotics Institute, University of Michigan, Ann Arbor, MI. `daphraz@umich.edu`

[^4]: $^{3}$Mechanical and Industrial Engineering, Louisiana State University, Baton Rouge, LA. `cbarbalata@lsu.edu`

[^5]: $^{4}$Naval Architecture and Marine Engineering, University of Michigan, Ann Arbor, MI. `mattjr@umich.edu`
