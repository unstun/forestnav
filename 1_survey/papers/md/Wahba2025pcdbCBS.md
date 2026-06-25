---
citation_key: Wahba2025pcdbCBS
arxiv_id: 2505.10355
arxiv_url: https://arxiv.org/abs/2505.10355
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:29:44Z
origin: ai+web
reviewed: false
---

# Introduction

Physically-coupled systems, such as multirotors collaboratively transporting cable-suspended payloads [@sreenath2013dynamics] or multiple mobile manipulators transporting objects [@tallamraju2019motion], are increasingly used in real-world tasks requiring coordinated interaction. These systems are particularly valuable in environments such as construction sites for carrying tools or materials and in precision tasks requiring synchronized motion. The robot coupling introduces additional challenges, as the planned motions must respect both inter-robot dependencies and the system's dynamic constraints. There has been a significant focus on controlling such systems [@sun2023nonlinear; @li2023nonlinear] and only limited work on planning feasible motions in cluttered environments that require team formation changes. Moreover, existing planners produce motions that are rather slow and fail to exploit the agility of the underlying single-robot systems. This limitation arises from the reliance on a simplified model of the system, where the planner generates suboptimal, almost quasi-static plans [@wahba2024kinodynamic].

:::: {#fig:real_envs .figure latex-placement="ht"}
![image](Wahba2025pcdbCBS_figs/frame_0225.png){width="23%"} ![image](Wahba2025pcdbCBS_figs/frame_0421.png){width="23%"}

::: caption
Real experiments validation scenarios. Left: Three multirotors transporting a cable-suspended payload in a forest-like environment. Right: Three differential drive robots connected with rigid rods collecting items while avoiding obstacles.
:::
::::

In this work, we address the limitations of the current state-of-the-art [@wahba2024kinodynamic], and present an anytime, probabilistically complete, motion planner for physically-coupled multi-robot systems in cluttered environments. To the best of our knowledge, this is the first work to offer this combination of simplicity, strong theoretical guarantees, and superior performance in the physically-coupled systems domain. Our approach builds on discontinuity-bounded Conflict-Based Search (db-CBS) [@moldagalieva2024db], a multi-robot motion planning algorithm designed for uncoupled robots. Although db-CBS reasons over the stacked state space of the robots, it only accounts for collision avoidance and neglects other interactions. Directly enforcing physical coupling constraints during trajectory optimization is also impractical. The redundancy in the state space with the coupling constraints, results in numerical instabilities and ill-conditioned optimization problems, causing failure. On the other hand, pc-dbCBS introduces a tri-level conflict detection and resolution that (i) embeds the rigidity constraints between the robots and (ii) switches between state space representations while retaining all the completeness and optimality guarantees of db-CBS.

The main algorithmic contribution of this work is a general anytime, probabilistically complete, kinodynamic motion planning framework for **physically-coupled multi-robot systems**, relying only on single-robot motion primitives. Moreover, we provide a key idea of alternating between state space representations from the stacked to a minimal representation in the same planning framework while having completeness and asymptotic optimality guarantees. Empirically, we test our method in simulation and real experiments on two case studies: multirotors transporting payloads with cables and differential drive robots connected by rigid rods as shown in [1](#fig:real_envs){reference-type="ref+label" reference="fig:real_envs"}. We show that our method has higher success rate than the current state-of-the-art [@wahba2024kinodynamic] and outperforms it in terms of cost, energy consumption, and computational time.

# Related Work

Existing physically-coupled multi-robot systems include humanoid robots transporting payloads [@rapetti2021shared], multi-robot mobile manipulators moving objects [@tallamraju2019motion], and aerial transport systems [@afifi2022toward; @wahba2024kinodynamic; @gorlo2024geranos]. The problem of aerial manipulation with a single robot [@tognon2019truly] and high-dimensional articulated robots [@gayle2007efficient; @kulkarni2020reconfigurable; @saleem2021search] are also related, as they have to consider very large search spaces for motion planning.

In principle such motion planning problems can be solved with any existing single-robot kinodynamic motion planner by stacking the states and actions. Common formulations use search-[@saleem2021search], sampling- [@AO-RRT], or optimization-based [@malyutaConvexOptimizationTrajectory2022a; @howell2019altro] approaches. Special extensions for the multi-robot case can improve the scalability by leveraging the sparsity of the problem. These methods include sampling-based approaches such as K-CBS [@kottinger2022conflict], optimization and control-inspired methods such as S2M2 [@chen2021scalable], or hybrid methods such as db-CBS [@moldagalieva2024db].

Motion planners for the physically-coupled case exist as well, especially for aerial transport of payloads. One approach extends a sampling-based method to the *Fly-Crane*, a system where three multirotors use two cables each to transport a rigid body [@manubens2013motion]. In cases with few or no obstacles, a formation controller might also be used, rather than a full motion planner [@de2019flexible]. Other approaches rely on differential flatness [@gabellieri2023differential] that provides a simplified framework for trajectory planning by leveraging flat outputs, but it typically leads to suboptimal solutions and is unable to directly account for motor actuation limits. Alternative methods that includes the motor actuation limits combine ideas from sampling and optimization to compute feasible trajectories [@wahba2024kinodynamic; @zhang2023if]. In particular for cable-suspended payload transportation, [@wahba2024kinodynamic] adopts this framework. Here, a simplified model is first used to warm-start a trajectory optimization step that incorporates necessary constraints. However, this method has two major limitations: i) the simplified model often produces suboptimal quasi-static hovering states, and ii) the lack of feedback between levels hinders completeness by limiting solution space exploration. One shortcoming of all existing methods is that the resulting motions are slow and do not exploit the full agile capabilities of the robots.

In contrast, this paper proposes an anytime planner that can produce time-optimal solutions, given enough computational effort. Our work is inspired by recent hybrid methods for uncoupled kinodynamic motion planning [@moldagalieva2024db] and empirically compares to a hierarchical planner that was previously used for aerial transport [@wahba2024kinodynamic].

# Problem Formulation

We consider the motion planning problem of $N$ robots that are physically-coupled with rigid connections, forming an actuated multi-robot system. The state of the system is represented as a stacked vector of each individual robot's state as follows $$\begin{equation}
    \label{eq:stacked_state}
    \mathbf{x}= (\mathbf{x}^{1}, \mathbf{x}^{2}, \ldots, \mathbf{x}^{N})^\top \in \mathcal{X}\subseteq \mathbb{R}^{d_{x}},
\end{equation}$$ where $\mathbf{x}^{i} \in \mathcal{X}^{i} \subseteq \mathbb{R}^{d_{x}^{i}}$ is the state of the $i^{\text{th}}$ robot, and $\mathcal{X}$ is the stacked state space. Similarly, the stacked action vector is defined as $$\begin{equation}
    \label{eq:stacked_action}
    \mathbf{u}= (\mathbf{u}^{1}, \mathbf{u}^{2}, \ldots, \mathbf{u}^{N})^\top \in \mathcal{U}\subseteq \mathbb{R}^{d_{u}},
\end{equation}$$ where $\mathbf{u}^{i} \in \mathcal{U}^{i} \subseteq \mathbb{R}^{d_{u}^{i}}$ is the controls applied to the $i^{\text{th}}$ robot. The dynamics of the stacked system are governed by $$\begin{equation}
    \label{eq:system_dynamics}
    \dot{\mathbf{x}}= \mathbf{f}(\mathbf{x}, \mathbf{u}).
\end{equation}$$

To employ gradient-based optimization, we assume that the Jacobian of $\mathbf{f}$ with respect to $\mathbf{x}$ and $\mathbf{u}$ is available, as is typical for motion planning in actuated multi-robot systems.

Let $\mathbf{X}= \langle \mathbf{x}_0, \mathbf{x}_1, \hdots, \mathbf{x}_T \rangle$ and $\mathbf{U}= \langle \mathbf{u}_0, \mathbf{u}_1, \hdots, \mathbf{u}_{T-1} \rangle$ be a sequence of states and controls sampled at time $0, \Delta t, \hdots, T\Delta t$ respectively, where $\Delta t$ is a small timestep and the controls are constant during this timestep. We denote the start state as $\mathbf{x}_s$, the goal state as $\mathbf{x}_f$, and the collision-free state space as $\mathcal{X}_{\text{free}} \subset \mathcal{X}$, which accounts for robots as well as collisions against the environment. Our goal is to find a solution of states and actions from a start to a goal state in the minimal time $T$, which can be framed as the following optimization problem $$\begin{align}
    &\min_{\mathbf{X}, \mathbf{U}, T} \hspace{0.2cm} J(\mathbf{X}, \mathbf{U}, T), \label{eq:general-optimization-problem}\\
    &\text{\noindent s.t.}\begin{cases}
     \mathbf{x}_{k+1} = \text{step}(\mathbf{x}_k, \mathbf{u}_k) \quad \forall k\in\{0, \ldots, T-1\}, \nonumber \\
     \mathbf{u}_k \in \mathcal{U}  \quad \forall k\in\{0, \ldots, T-1\}, \nonumber \\
     \mathbf{x}_0 = \mathbf{x}_s, \hspace{0.2cm} \mathbf{x}_T = \mathbf{x}_f, \nonumber \\
      \mathbf{x}_k \in \mathcal{X}_{\text{free}} \subset \mathcal{X}\quad \forall k\in\{0, \ldots, T\}, \\
     \mathbf{g}(\mathbf{x}) = 0, \nonumber \\
    \end{cases}
\end{align}$$ where the cost function is $T$ and other task objectives (e.g., energy). The first constraint is the time-discretized system dynamics and the second constraint bounds actions to the admissible space $\mathcal{U}$. The third set of constraints enforces the given start and goal states. The final constraint $\mathbf{g}(\mathbf{x})$, assumed to be continuously differentiable (similar to [@de2005feedback]), enforces the physical rigidity coupling between robots, ensuring their motions satisfy the kinematic and dynamic interactions. We assume that the constraint set $\{\mathbf{x}\in \mathcal{X}\mid \mathbf{g}(\mathbf{x}) = 0\}$ admits a local mapping $\Phi: \mathcal{X}_m \rightarrow \mathcal{X}$ with minimal coordinates $\mathbf{x}_m \in \mathcal{X}_m$.

To demonstrate the generality of the framework across embodiments, we present two robot platforms: (i) Unicycles, low-dimensional non-holonomic robots, rigidly connected in a "line"-formation. (ii) Multirotors transporting payloads with cables (modeled as rigid rods), high-dimensional underactuated robots. These examples are illustrative only. Our framework applies to any rigidly-coupled robot teams.

## Unicycles with Rigid Rods (UR)

Consider a team of $N$ unicycles connected by $N-1$ rigid rods of fixed lengths in a line formation. The state of the $i^{\text{th}}$ unicycle is described as $\mathbf{x}^{i} = (p_x^{i}, p_y^{i}, \theta^{i})^\top,$ where $\mathbf{p}^i = (p_x^i, p_y^i)^\top$ denote the position of the $\emph{i}^{th}$ unicycle, and $\theta^i$ represents its orientation. The kinematic model for the unicycle is given by $\dot{\mathbf{x}}^{i} = \mathbf{C}^{i}\mathbf{u}^{i}$ as $$\begin{equation}
    \label{eq:unicycle}
    \dot{\mathbf{x}}^{i} = 
    \begin{pmatrix}
        \cos(\theta^{i}) & 0 \\
        \sin(\theta^{i}) & 0 \\
        0 & 1
    \end{pmatrix}
    \begin{pmatrix}
        v^{i} \\ \omega^{i}
    \end{pmatrix},
\end{equation}$$ where $\mathbf{u}^{i} = (v^{i}, \omega^{i})^\top$ represents the linear and angular velocities, respectively. Let the length of the rod connecting the $i^{\text{th}}$ and $(i+1)^{\text{th}}$ unicycles be $l^i$. Then the coupling constraint $\mathbf{g}(\mathbf{x})=0$ is $$\begin{align}
    \| \mathbf{p}^{i} - \mathbf{p}^{i+1} \| - l^i = 0, \quad i=1,\ldots, N-1.
\end{align}$$

## Multirotors Transporting a Payload (MP) {#sec:multirotor}

Consider a team of $N$ multirotors transporting a cable-suspended payload. The $i^{\text{th}}$ multirotor is modeled as a rigid floating base with state $\mathbf{x}^{i} = (\mathbf{p}^{i}, \mathbf{R}^{i}, \mathbf{v}^{i}, \boldsymbol{\Omega}^{i})^\top$. Here, $\mathbf{p}^{i}, \mathbf{v}^{i} \in \mathbb{R}^3$ represent the position and velocity in the world frame, $\mathbf{R}^{i} \in SO(3)$ represents the rotation matrix, and $\boldsymbol{\Omega}^{i} \in \mathbb{R}^3$ is the angular velocity expressed in the body frame. The action $\mathbf{u}^{i} \in \mathbb{R}^4$ is defined as the forces at the rotors, $\mathbf{u}^{i} = (f_{1}^{i}, f_{2}^{i}, f_{3}^{i}, f_{4}^{i})^\top$. The dynamics are derived from Newton-Euler equations for rigid bodies as $$\begin{align}
    \label{eq:multirotor}
    \dot{\mathbf{p}}^{i} &= \mathbf{v}^{i}, \quad &m^i \dot{\mathbf{v}}^{i} &= \mathbf{R}^{i} f_T^{i} \mathbf{e}_3- m^i g\mathbf{e}_3, \quad \\
    \dot{\mathbf{R}}^{i} &= \mathbf{R}^{i} \hat{\boldsymbol{\Omega}}^{i}, \quad
    &\mathbf{J}^i \dot{\boldsymbol{\Omega}}^{i} &= \mathbf{J}^i \boldsymbol{\Omega}^{i} \times \boldsymbol{\Omega}^{i} + \mathbf{M}^{i}, \nonumber
\end{align}$$ where $m^i$ is the mass, $\mathbf{J}^i$ is the inertia matrix, g is the gravitational acceleration constant, $\mathbf{e}_3= (0, 0, 1)^\top$. The $(\hat{\cdot})$ denotes the skew-symmetric mapping $\mathbb{R}^3 \rightarrow \mathfrak{s}\mathfrak{o} (3)$.

The collective thrust and torques, $\boldsymbol{\eta}^{i} = (f_T^{i}, \mathbf{M}^{i})^\top$, are linearly related to the motor forces $\mathbf{u}^{i}$ via a fixed and known actuation matrix.

Each multirotor is connected with a cable modeled as a rigid rod of length $l^i$ to a point mass payload at $\mathbf{p}^0$ with mass $m^0$. Then the coupling constraint $\mathbf{g}(\mathbf{x})=0$ is $$\begin{align}
    \| \mathbf{p}^{0} - \mathbf{p}^{i} \| - l^i = 0, \quad i=1,\ldots N.
\end{align}$$

# Approach

## pc-dbCBS

Our motion planning approach, pc-dbCBS, extends and adapts db-CBS to the high-dimensional physically-coupled systems that are subject to physical constraints between the robots. Building upon this foundation, pc-dbCBS utilizes the three-level iterative framework of db-CBS by integrating additional definition of conflicts and conversions of state representations to manage physical coupling constraints. In principle, pc-dbCBS utilizes the efficiency of the discrete search with the stacked state space, allowing the usage of pre-computed motion primitives for the single robot, along with the effectiveness of trajectory optimization on a minimal representation of the coupled system. The pseudo code in [\[alg:dbcbs\]](#alg:dbcbs){reference-type="ref+label" reference="alg:dbcbs"} highlights major changes compared to db-CBS.

### Single Robot Planning

The *first level* uses $\text{db-A}^\ast$ [@ortiz2024idb] to plan for each robot a trajectory with state discontinuous up to $\delta$ from a graph constructed of precomputed motion primitives $\mathcal{M}$. A motion primitive is defined as a tuple $\langle \mathbf{X}^i, \mathbf{U}^i, K \rangle$ of state and action sequences over $K$ steps that satisfy the dynamics of the robot. For each robot $i$, $\text{db-A}^\ast$ outputs state and action sequences which adhere to the single robot dynamics, such as [\[eq:unicycle\]](#eq:unicycle){reference-type="ref+label" reference="eq:unicycle"} for unicycles and [\[eq:multirotor\]](#eq:multirotor){reference-type="ref+label" reference="eq:multirotor"} for multirotors. These sequences form *$\delta$-discontinuity-bounded* solutions under the condition $$\begin{align}
    &d(\mathbf{x}_{k+1}^i, \text{step}(\mathbf{x}_k^i, \mathbf{u}_k^i)) \leq \delta \quad \forall k, \\
    &\mathbf{u}_k^i \in \mathcal{U}^i, \quad \mathbf{x}_k^i \in \mathcal{X}^i, \nonumber \\
    &d(\mathbf{x}_0^i, \mathbf{x}_s^i) \leq \delta, \quad d(\mathbf{x}_K^i, \mathbf{x}_f^i) \leq \delta \nonumber,
\end{align}$$ where $d$ is a metric $d : \mathcal{X}^i \times \mathcal{X}^i \to \mathbb{R}$, which measures the distance between two states. In this work, we pre-compute each robot's set of motion primitives offline as in db-CBS.

::: algorithm
:::

### Conflict Resolution

The *second level* employs a search to analyze the motions generated by the first level, identifying conflicts between robots, and creating constraints that are then iteratively resolved by the first level. Conflicts are resolved through a hierarchical process that sequentially addresses three types of conflicts: inter-robot collisions, physical coupling violations, and coupling elements (e.g., rods) and environment collisions. These conflicts are resolved in . Each type of conflict is resolved up to the tolerance $\delta$ over the full time horizon of the planned trajectory, before the next conflict type is considered.

The first level resolves robot-robot collisions by using the `ResolveRobotCollision` function ([\[alg:line9\]](#alg:line9){reference-type="ref+label" reference="alg:line9"}) to detect overlaps in planned motions. When conflicts are found, constraints are added to the priority queue $\mathcal{O}$, and the `HLDiscreteSearch` process iterates with these updates. This behavior is identical to db-CBS.

The second level resolves the physical coupling constraints. The `ResolvePhysicalConstraint` function ([\[alg:line10\]](#alg:line10){reference-type="ref+label" reference="alg:line10"}) evaluates the solution of the robots' formations up to given bounds. For each step $k$, the constraint $\|\mathbf{g}(\mathbf{x})\| < \delta$ is checked. If a violation is detected, only a single new node is added to $\mathcal{O}$, constraining a randomly picked single robot motion. Note that in the traditional CBS framework $N$ nodes would need to be added, as it is unknown which combination of robots is causing the constraint violation. Picking a single robot instead reduces the size of $\mathcal{O}$, but has some theoretical drawbacks, as discussed later.

The final level of conflict resolution involves collision checking between the physical coupling elements (e.g., rods) and the obstacles in the environment. The `ResolvePCCollision` function ([\[alg:line11\]](#alg:line11){reference-type="ref+label" reference="alg:line11"}) constructs artificial collision shapes for the coupling elements and evaluates whether they collide with obstacles. If a collision is identified, one additional node is added to $\mathcal{O}$, constraining the affected robot. In principle, inter-cable collisions could be defined as conflicts; however, this would significantly increase computational overhead as they are already addressed during the optimization step as collision shapes (e.g., rods or cylinders), we find that this is not needed in practice.

If no conflicts are detected at all levels, the algorithm returns a stacked space solution that adheres to all robot-robot, physical coupling, and obstacle collisions constraints up to the bounded tolerance $\delta$.

### Stacked to Constrained Systems

The next step involves converting the stacked space solution from the discrete search to the constrained physically-coupled dynamical system ([\[alg:line4\]](#alg:line4){reference-type="ref+label" reference="alg:line4"}). This is achieved by representing the state into a minimal representation $\mathbf{x}_m \in \mathcal{X}_m$. The dynamics of the physically coupled system can be projected on the coupling constraints $\mathbf{g}(\mathbf{x})$ in [\[eq:general-optimization-problem\]](#eq:general-optimization-problem){reference-type="ref+label" reference="eq:general-optimization-problem"} using the minimal representation, which are governed by $\dot{\mathbf{x}}_{m} = \mathbf{f}_m(\mathbf{x}_{m}, \mathbf{u})$.

### Trajectory Optimization

After the discrete stacked state solution is mapped to the minimal state representation, we use trajectory optimization to refine the solution from the discrete search and to repair all the discontinuities of $\delta$. The optimization problem is reformulated using the minimal state representation as $$\begin{align}
    \label{eq:opticost}
    &\min_{\mathbf{X}, \mathbf{U}, \Delta t} \hspace{0.2cm} \sum_{k} (\Delta t - \Delta t_0)^2  + \beta_1 \|\mathbf{u}_k\|^2 \\ & + \beta_2 \|\ddot{\boldsymbol{x}}_m(\mathbf{x}_{m_k}, \mathbf{u}_k)\|^2  \nonumber \\
&\text{\noindent s.t.}\begin{cases}
     \mathbf{x}_{m_{k+1}} = \text{step}(\mathbf{x}_{m_k}, \mathbf{u}_k) \quad \forall k\in\{0, \ldots, T-1\}, \\
     \mathbf{u}_k \in \mathcal{U}  \quad \forall k\in\{0, \ldots, T-1\},  \\
     \mathbf{x}_{m_0} = \mathbf{x}_{m_s}, \hspace{0.2cm} \mathbf{x}_{m_T} = \mathbf{x}_{m_f}, \nonumber \\
      \mathbf{x}_{m_k} \in \mathcal{X}_{m_\text{free}} \subset \mathcal{X}_m  \quad \forall k\in\{0, \ldots, T\}. 
    \end{cases}
\end{align}$$ Here, the cost function minimizes the deviation of the time step $\Delta t$ from a nominal value $\Delta t_0$, penalizes the control effort $\|\mathbf{u}_k\|^2$, and reduces the system's dynamic accelerations $\|\ddot{\boldsymbol{x}}(\mathbf{x}_k, \mathbf{u}_k)\|^2$ to improve trajectory smoothness. The weighting parameters $\beta_1$ and $\beta_2$ are used to balance the contributions of the control effort and dynamic smoothness terms. This part is identical to prior formulations such as [@wahba2024kinodynamic].

### Anytime Planning {#sec:anytimeplanning}

Our method iteratively refines solutions by updating two parameters ([\[alg:line2\]](#alg:line2){reference-type="ref+label" reference="alg:line2"}). First, $\delta$ is gradually decreased with a predefined rate. Second, solutions from the optimization step, including failed ones, are extracted, split, and transformed from the minimal representation to single-robot motion primitives. Then these are added to the motion primitive database $\mathcal{M}$ alongside newly sampled primitives with a predefined rate.

## Case Study: Unicycles with Rigid Rods (UR)

### Constrained Dynamics

The system can be minimally represented by the state vector $$\begin{equation}
    \label{eq:unicyclemin}
    \mathbf{x}_{m} = (p_x^{1}, p_y^{1}, \theta^{1}, \cdots, \theta^{N}, \alpha^{1}, \cdots, \alpha^{N-1})^\top,
\end{equation}$$ where $\alpha^{i}$ represents the orientation of the $i^{\text{th}}$ rod. We have $\mathbf{x}_{m} \in \mathbb R^{2N} \times (SO(2))^{2N-1}$, and the position of the $({i+1})^{\text{th}}$ unicycle is expressed by $$\begin{equation}
    \label{eq:unicycles_constraints}
    p_x^{i+1} = p_x^{i} + l^i\cos(\alpha^{i}), \quad 
    p_y^{i+1} = p_y^{i} + l^i\sin(\alpha^{i}).
\end{equation}$$

The kinematics of the $N$ unicycles with rigid rods are governed by the constraints imposed by the distance between the connected unicycles. Let the relative position and its derivative with respect to time of two neighboring robots $i$ and $j$ be $$\begin{align}
    \label{eq:constraint1}
    dx_{ij} &= p_x^{j} - p_x^{i}, & dy_{ij} &= p_y^{j} - p_y^{i} \\
 \dot{dx}_{ij} &= \dot{p}_x^{j} - \dot{p}_x^{i}, & \dot{dy}_{i} &= \dot{p}_y^{j} - \dot{p}_y^{i} \nonumber
\end{align}$$ Thus, the constraint enforcing a fixed distance between the $i^{\text{th}}$ and $j^{\text{th}}$ consecutive unicycles is given by $$\begin{equation}
    \label{eq:constraint}
    dx_{ij}^2 + dy_{ij}^2 = {l^i}^2.
\end{equation}$$ Differentiating [\[eq:constraint\]](#eq:constraint){reference-type="ref+label" reference="eq:constraint"} with respect to time yields $$\begin{equation}
    \label{eq:velocity_constraint}
    2dx_{ij} \dot{dx}_{ij} + 2dy_{ij} \dot{dy}_{ij} = 0,
\end{equation}$$ which ensures that the velocities of the unicycles are consistent with the physical constraints imposed by the rods. To incorporate these constraints into the system kinematics, we construct the Jacobian matrix $\mathbf{A}$ with dimensions $(n-1) \times 3n$. The rod constraints in [\[eq:velocity_constraint\]](#eq:velocity_constraint){reference-type="ref+label" reference="eq:velocity_constraint"} can then be expressed compactly as $$\begin{equation}
    \mathbf{A} \dot{\mathbf{x}}^{ur} = 0,
\end{equation}$$ where $\mathbf{x}^{ur} = (p_x^{1}, p_y^{1}, \theta^{1}, \cdots,p_x^{N}, p_y^{N}, \theta^{N})$. This formulation ensures that the system dynamics remain consistent with the physical constraints imposed by the rods.

Inspired by [@de2005feedback], the kinematics are then projected into the constraint-consistent space using a projection matrix $\mathbf{G}\in \mathbb R^{3n\times2n}$ $$\begin{align}
    \label{eq:urdyn}
    \dot{\mathbf{x}}^{ur} = \mathbf{G} \mathbf{u}, &\quad \mathbf{G} = \mathbf{B} - \mathbf{A}^\dagger (\mathbf{A} \mathbf{B}),
\end{align}$$ with $\mathbf{A}^\dagger = \mathbf{A}^\top (\mathbf{A} \mathbf{A}^\top)^{-1}$. The input mapping matrix for the unicycles $\mathbf{B} \in \mathbb R^{2n \times 2n}$ is a block-diagonal matrix defined as $\mathbf{B} = \text{diag}(\mathbf{C}^{1}, \mathbf{C}^{2}, \dots, \mathbf{C}^{N}),$ where each $\mathbf{C}^{i}$ is defined in [\[eq:unicycle\]](#eq:unicycle){reference-type="eqref" reference="eq:unicycle"}.

The angle of each rod $\alpha^{i}$ and its angular velocity $\dot{\alpha}^{i}$ are computed by $$\begin{align}
    \label{eq:rodangle}
\alpha^{i} &= \arctan(dy_{ij}, dx_{ij})  \\ 
\quad \dot{\alpha}^{i} &= \frac{1}{{l^i}^2}dx_{ij}\dot{d}y_{ij} - dy_{ij}\dot{d}x_{ij} \quad, i \in \{1, \ldots, N\}\nonumber.
\end{align}$$ The dynamics $\mathbf{f}_m$ is then computed using [\[eq:urdyn\]](#eq:urdyn){reference-type="eqref" reference="eq:urdyn"}, [\[eq:rodangle\]](#eq:rodangle){reference-type="eqref" reference="eq:rodangle"} and the action vector $\mathbf{u}$.

### Conflicts

The conflict in the second level arises from maintaining a certain distance decided by the length of the rigid rod. Consider $l_{c_k}^i= \sqrt{dx_{ij,k}^2 + dy_{ij,k}^2} \quad \forall (i,i+1)$ to be the actual relative distance between each consecutive pair of unicycles at the $k^{\text{th}}$ step. Then, a conflict for the robot pair $(i, i+1)$ occurs if $$\begin{equation}
    | l_{c_k}^i- l^i | > \delta,
\end{equation}$$ where $l^i$ is the nominal rod length, and $\delta$ defines the allowable tolerance.

:::: {#fig:sim_envs .figure latex-placement="ht"}
![image](Wahba2025pcdbCBS_figs/window.png){width="23%"} ![image](Wahba2025pcdbCBS_figs/forest.png){width="23%"} ![image](Wahba2025pcdbCBS_figs/wall.png){width="23%"} ![image](Wahba2025pcdbCBS_figs/window_uni.png){width="23%"}

::: caption
Simulation environments from left to right: window (5 multirotors), forest (4 multirotors), wall (3 unicycles), window (4 unicycles). Note that the forest environment is the same for both robot types.
:::
::::

## Case Study: Multirotors Transporting a Payload (MP)

### Constrained Dynamics

The dynamics of multirotors with cable-suspended payloads, as presented in [@wahba2024kinodynamic], are described using the minimal state representation $$\begin{equation}
    \label{eq:statespace}
    \mathbf{x}_m = (\mathbf{p}^0, \dot{{\mathbf{p}}}^0, \mathbf{s}^1, \boldsymbol{\omega}^1, \mathbf{R}^1, \boldsymbol{\Omega}^1, \ldots, \mathbf{s}^N, \boldsymbol{\omega}^N, \mathbf{R}^N, \boldsymbol{\Omega}^N)^\top,
\end{equation}$$ where $\mathbf{p}^0\in \mathbb{R}^3$ is the payload's position, $\dot{{\mathbf{p}}}^0\in \mathbb{R}^3$ is the payload velocity, $\mathbf{s}^i\in \mathbb{S}^2$ are the cable unit vectors pointing from the UAV to the payload (with $\mathbb{S}^2 = \{\mathbf{s} \in \mathbb{R}^3 \big| \|\mathbf{s}\| = 1\}$), and $\boldsymbol{\omega}^i \in \mathbb{R}^3$ are the cable angular velocities, where $i \in \{1, \ldots, N\}$.

The UAV position and velocity vectors are $\mathbf{p}^i\in \mathbb{R}^3$ and $\dot{\mathbf{p}}^i \in \mathbb{R}^3$ are computed as $$\begin{equation}
    \label{eq:uavpos}
    \mathbf{p}^i = \mathbf{p}^0- l^i\mathbf{s}^i, \quad \dot\mathbf{p}^i = \dot \mathbf{p}^0 - l^i \dot{\mathbf{s}}^i.
\end{equation}$$

The dynamics $\mathbf{f}_m$ of the system is defined as $$\begin{align}
    \label{eq:mpdynamics}
    &\dot{\mathbf{s}}^i= \boldsymbol{\omega}^i\times \mathbf{s}^i, \quad \mathbf{s}^i= \frac{\mathbf{p}^0 - \mathbf{p}^i}{\|\mathbf{p}^0 - \mathbf{p}^i\|},\\
    &\mathbf{M_{t}}(\ddot{\mathbf{p}}^{0}+g\mathbf{e}_3)  = \sum_{i=1}^n (f_{T}^i\mathbf{R}^i\mathbf{e}_3- m^i l^i\|\boldsymbol{\omega}^i\|^2\mathbf{s}^i), \nonumber\\
    &m^i l^i\dot{\boldsymbol{\omega}}^i = m^i \hat{\mathbf{s}}^i(\ddot{\mathbf{p}}^{0}+g\mathbf{e}_3) - f^i_{T}\hat{\mathbf{s}}^i\mathbf{R}^i\mathbf{e}_3, \nonumber\\
    &\dot{\mathbf{R}}^i = \mathbf{R}^i \hat{\boldsymbol{\Omega}}^i,
    \quad \mathbf{J} \dot{\boldsymbol{\Omega}}^i = \mathbf{J} \boldsymbol{\Omega}^i \times \boldsymbol{\Omega}^i + \mathbf{M}^i, \nonumber
\end{align}$$ where $\ddot{\mathbf{p}}^{0}$ is the payload acceleration, $\mathbf{M}_{t} = m^0 \mathbf{I}_{3} + \sum_{i=1}^n m^i \mathbf{s}^i{\mathbf{s}^i}^\top$ and $g$ is the gravitational acceleration.

### Conflicts

::: table*
+------------------+-----------------------------------------------+------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| **Environment**  | **Success** \[%\] $\uparrow$                  | **Cost** \[s\] $\downarrow$                                                              | **Time** \[s\] $\downarrow$                                                                  |
+:================:+:=========:+:=========:+:=========:+:=========:+:=========:+:===============================:+:=========:+:==============================:+:=========:+:================================:+:=========:+:=================================:+
| 2-13             | **UR**                | **MP**                | **UR**                                      | **MP**                                     | **UR**                                       | **MP**                                        |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| 2-13             | **Ours**  | **BL**    | **Ours**  | **BL**    | **Ours**  | **BL**                          | **Ours**  | **BL**                         | **Ours**  | **BL**                           | **Ours**  | **BL**                            |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Window, 2 robots | **100.0** | **100.0** | **100.0** | 90.0      | **4.9**   | 10.4 [0.1]{style="color: gray"} | **2.0**   | 5.5 [0.9]{style="color: gray"} | **0.2**   | 350.7 [0.1]{style="color: gray"} | **5.2**   | 364.8 [2.6]{style="color: gray"}  |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Window, 3 robots | **100.0** | **100.0** | **100.0** | 70.0      | **6.1**   | 14.9 [1.6]{style="color: gray"} | **2.0**   | 5.2 [0.1]{style="color: gray"} | **2.1**   | 351.5 [0.2]{style="color: gray"} | **14.0**  | 376.0 [4.1]{style="color: gray"}  |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Window, 4 robots | 80.0      | **90.0**  | **100.0** | 0.0       | **9.1**   | 15.4 [3.1]{style="color: gray"} | **2.1**   | F                              | **54.5**  | 352.7 [1.0]{style="color: gray"} | **41.4**  | F                                 |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Window, 5 robots | 90.0      | **100.0** | **100.0** | 10.0      | **7.7**   | 13.3 [1.8]{style="color: gray"} | **2.1**   | 5.1 [0.0]{style="color: gray"} | **36.3**  | 353.1 [0.6]{style="color: gray"} | **90.4**  | 433.3 [0.0]{style="color: gray"}  |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Window, 6 robots | **60.0**  | 50.0      | 30.0      | 30.0      | **10.4**  | 19.2 [2.5]{style="color: gray"} | **2.8**   | 5.7 [0.4]{style="color: gray"} | **24.5**  | 356.5 [1.4]{style="color: gray"} | **153.4** | 511.2 [42.2]{style="color: gray"} |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Forest, 2 robots | **100.0** | **100.0** | **100.0** | **100.0** | **8.8**   | 12.5 [1.1]{style="color: gray"} | **2.2**   | 6.2 [1.3]{style="color: gray"} | **0.9**   | 350.9 [0.2]{style="color: gray"} | **22.6**  | 364.6 [1.7]{style="color: gray"}  |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Forest, 3 robots | **100.0** | 90.0      | 80.0      | **90.0**  | **10.8**  | 12.7 [0.5]{style="color: gray"} | **2.5**   | 5.3 [0.1]{style="color: gray"} | **4.3**   | 351.1 [0.3]{style="color: gray"} | **86.3**  | 375.8 [6.2]{style="color: gray"}  |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Forest, 4 robots | **100.0** | 50.0      | 70.0      | **90.0**  | **11.8**  | 15.9 [0.8]{style="color: gray"} | **2.5**   | 5.3 [0.1]{style="color: gray"} | **5.8**   | 353.3 [0.5]{style="color: gray"} | **64.3**  | 380.9 [12.0]{style="color: gray"} |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Forest, 5 robots | **90.0**  | 30.0      | 0.0       | **80.0**  | **14.3**  | 19.8 [2.8]{style="color: gray"} | F         | **6.9**                        | **10.4**  | 355.0 [0.9]{style="color: gray"} | F         | **485.6**                         |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+
| Forest, 6 robots | **60.0**  | 0.0       | 10.0      | **70.0**  | **16.1**  | F                               | **3.2**   | 6.5 [0.8]{style="color: gray"} | **57.4**  | F                                | **227.3** | 478.7 [19.1]{style="color: gray"} |
+------------------+-----------+-----------+-----------+-----------+-----------+---------------------------------+-----------+--------------------------------+-----------+----------------------------------+-----------+-----------------------------------+

[]{#table1 label="table1"}
:::

A challenge for the conflict detection is that the constraint $\mathbf{g}(\mathbf{x})$ depends on the payload position $\mathbf{p}^0$, which is not part of the stacked state. Thus, we estimate the payload positions $\mathbf{p}^{0_e}_k$ by solving the following optimization problem $$\begin{align}
    \label{eq:payload-optimization}
    \min_{\mathbf{p}^{0_e}_k} \sum_{i=1}^{N} &(\|\mathbf{p}^{0_e}_k - \mathbf{p}_k^i\| - l^i)^2 + 
    \mu \|\mathbf{p}^{0_e}_k - \mathbf{p}^{0_d}_{k}\| \\ & +  
    \lambda (\min_{i}\{p_{z_k}^i\} - p^{0_e}_{z_k} - l_{\text{min}})^2,    \nonumber
\end{align}$$ where $\mu$ and $\lambda$ are weighting parameters, $\mathbf{p}^{0_d}_{k}$ is used to penalize jumps of the payload estimate from the previous solution, and $l_{\text{min}}$ is the cable length associated with the robot closest to the payload $\min_{i}\{p_{z_k}^i\}$ in the $z$-axis among all robots. This cost function ensures that the payload position minimizes deviations from nominal cable lengths, penalizes significant changes in the payload position, and guarantees the estimated payload position remains below the robots' positions.

Once the payload position $\mathbf{p}^{0_e}_k$ is estimated, the actual cable lengths are computed as $$\begin{equation}
    l_{c_k}^i= \|\mathbf{p}^{0_e}_k - \mathbf{p}_k^i\|, \quad \forall i \in \{1, \dots, N\}.
\end{equation}$$ A conflict in the second level for all robots arises if any cable length $l_{c_k}^i$ deviates from the nominal cable length $l^i$ by more than the tolerance $\delta$ $$\begin{equation}
    | l_{c_k}^i- l^i | > \delta.
\end{equation}$$ Note that in this case all robots participate in the conflict.

## Theoretical Remarks

pc-dbCBS inherits the probabilistic completeness and asymptotic optimality of db-CBS [@moldagalieva2024db Theorem 1]. In particular [@moldagalieva2024db Theorem 1] states that db-CBS is asymptotically optimal (implying probabilistic completeness), i.e., $$\begin{equation}
 \label{dbcbs-proof}
    \lim_{n\to\infty}P(c_n - c^{\ast} > \varepsilon)=0\quad\forall\,\varepsilon>0,
\end{equation}$$ where $c_n$ is the cost in iteration $n$ and $c^{\ast}$ is the optimal cost. In db-CBS, at each iteration $n$, the discrete search finds the optimal solution within $\delta$, if one exists, yielding the optimal discrete cost $c_n$. At each iteration the motion primitive library grows and $\delta$ shrinks, expanding the discrete search graph. For pc-dbCBS, the same argument of the proof as in [@moldagalieva2024db Theorem 1] still holds with the highlighted changes in [\[alg:dbcbs\]](#alg:dbcbs){reference-type="ref+label" reference="alg:dbcbs"}, because the outer-loop () is unchanged.

We note that the inner loop of our proposed algorithm violates some key assumptions of CBS: i) for completeness, all possible alternatives need to be considered in the open list (which we violate in `ResolvePhysicalConstraints` by only including a randomly-picked single new entry); and ii) for optimality, we need to resolve conflicts in the order of their occurrence in time (which we violate using our hierarchical approach that checks for a certain type of conflict over the whole time horizon). These changes might result producing near-optimal results of a single inner loop iteration; however the discrete search does not deterministically prune potential solution trajectories, thus the key properties of asymptotic optimality and probabilistic completeness are retained. However, our choice impacts the runtime as potentially more outer loop iterations are needed.

# Results

To validate the performance of our method, we compare with a state-of-the-art baseline method for physically-coupled multi-robot kinodynamic planning [@wahba2024kinodynamic], in both simulation and real experiments. We evaluate both methods on two systems: unicycles connected by rigid rods and multirotors transporting payloads with cables. To this end, we extend the baseline to the unicycle case with rigid rods.

The baseline relies in the first planning stage on OMPL [@OMPL] and for optimization on Dynoplan [@ortiz2024idb], a motion planning framework built on Crocoddyl [@Crocoddyl]. We extend the implementation of Dynoplan to include the unicycles with rods, implemented in C++. Both kinodynamic motion planners use the Flexible Collision Library (FCL) [@FCL] for collision checking. For solving [\[eq:payload-optimization\]](#eq:payload-optimization){reference-type="eqref" reference="eq:payload-optimization"}, we rely on NLopt. We will publicly release the code and problem instances after the double-blind peer-review.

## Simulations

For multirotors with cable-suspended payload, we validate our method in simulation using a software-in-the-loop setup. This setup executes the actual flight controller code [@wahba2023efficient] designed for Bitcraze Crazyflie 2.1 multirotors. For unicycles, we implemented a nonlinear controller [@kanayama1990stable] in Python. In simulation, as shown in [2](#fig:sim_envs){reference-type="ref+label" reference="fig:sim_envs"}, we test pc-dbCBS (**Ours**) and the baseline (**BL**) on three distinct scenarios for both systems (see supplemental video). For $n$-unicycles with rods and multirotors with cable-suspended payloads, the first scenario involves a window environment where the goal is to pass through a narrow passage. The second scenario is a forest-like environment with dense obstacles. To evaluate the completeness of both methods, we designed a third scenario specifically for unicycles with rods: we constrain the angular velocity of each unicycle in a wall environment, allowing only clockwise rotations $(\omega^i \in [0, 0.5] \ \si{rad/s})$. For each scenario, we evaluate five different problem instances, gradually increasing the number of robots from two to six. We denote (F) as failed attempts.

::: {#table2}
+--------------------+---------------------------------+---------------------------------+---------------------------------+
| **Environment**    | **Success \[%\]** $\uparrow$    | **Cost** \[s\] $\downarrow$     | **Time** \[s\] $\downarrow$     |
+:==================:+:==============:+:==============:+:==============:+:==============:+:==============:+:==============:+
| 2-7                | **Ours**       | **BL**         | **Ours**       | **BL**         | **Ours**       | **BL**         |
+--------------------+----------------+----------------+----------------+----------------+----------------+----------------+
| 2-7 Wall, 2 robots | **90.0**       | 0.0            | **13.0**       | F              | **3.7**        | F              |
+--------------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Wall, 3 robots     | **90.0**       | 0.0            | **12.7**       | F              | **18.0**       | F              |
+--------------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Wall, 4 robots     | **50.0**       | 0.0            | **12.6**       | F              | **18.5**       | F              |
+--------------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Wall, 5 robots     | **80.0**       | 0.0            | **12.8**       | F              | **56.8**       | F              |
+--------------------+----------------+----------------+----------------+----------------+----------------+----------------+
| Wall, 6 robots     | **70.0**       | 0.0            | **12.9**       | F              | **25.3**       | F              |
+--------------------+----------------+----------------+----------------+----------------+----------------+----------------+

: Simulation Results for unicycles with rods (UR). Shown are mean values for the success rate, cost, and computational time over 10 trials with a time limit of 350 s.
:::

[]{#table2 label="table2"}

All experiments were conducted on a workstation (AMD Ryzen Threadripper PRO 5975WX @ 3.6 GHz, 128 GB RAM, Ubuntu 22.04). Each experiment was repeated 10 times, with a runtime limit for both planners of 350 s.

### Comparison Metrics

To evaluate the performance of our method, we consider three key metrics on 25 problem instances: success rate, cost, and computation time. The results are summarized in Tables [\[table1\]](#table1){reference-type="ref" reference="table1"} and [1](#table2){reference-type="ref" reference="table2"}. The success rate is defined as the proportion of problem instances where a feasible trajectory is successfully computed by the motion planner. The cost metric is the total time of the trajectory from the optimization process for both methods, as both utilize the same trajectory optimization step. Finally, the computation time is the motion planner's runtime required to compute a feasible trajectory.

### Results

For multirotors with cable-suspended payloads tested in window and forest environments, pc-dbCBS consistently generates $60\%$ lower cost (i.e., faster trajectories) than the baseline. **Ours** achieves a higher success rate in narrow-passage scenarios(e.g., window environment).

For unicycles connected by rods in dense environments, pc-dbCBS outperforms the baseline in both success rate and cost. However, in dense scenes like the forest for multirotors with cable-suspended payloads, the success rate of pc-dbCBS decreases as the team grows, due to the combinatorial explosion in cable-obstacles collision conflicts, as the finite set of motion primitives cannot explore every branch in the graph. These failures arise from practical limits on time and the number of primitives, thus, this does not contradict with pc-dbCBS retaining its probabilistic completeness.

Furthermore, pc-dbCBS demonstrates in [1](#table2){reference-type="ref+label" reference="table2"} high success rates in the wall environment, where unicycles are restricted to clockwise rotation. In contrast, the baseline fails to generate any feasible trajectories in this scenario, because it does not reason about dynamic limits, causing the optimization step to consistently fail.

In terms of computation time, the geometric planner in the baseline executes until it times out, followed by additional time for the optimization step. In contrast, pc-dbCBS applies the anytime planning property across the entire framework, allowing us to report both the cost and computation time of the first valid solution, highlighting its efficiency in finding solutions fast with better cost.

### Optimality and Anytime Planning

In our work, we use the term anytime synonymously with asymptotic optimality, which is typical in the motion planning literature.The formal properties of *anytime* [@zilberstein1996using], with the exception of the interruptibility before the first solution is found, are maintained. By decreasing $\delta$ and adding more motion primitives to the graph search step ([4.1.5](#sec:anytimeplanning){reference-type="ref+label" reference="sec:anytimeplanning"}), we achieve a consistent cost reduction at each iteration, thereby demonstrating the method's asymptotic optimality as shown in [3](#fig:cost){reference-type="ref+label" reference="fig:cost"} for two, three, and four multirotors with payloads in the window environment.

![Anytime planning of pc-dbCBS for three different example scenarios for multirotors with payload (MP).](Wahba2025pcdbCBS_figs/plot_cost2.png){#fig:cost width="90%"}

Furthermore, the optimization process operates in an anytime manner, allowing it to improve the solution over time and stops when the predefined time limit is reached. This ensures that the method can effectively balance solution quality and computational efficiency.

## Physical Experiments

To validate the simulation results, we conduct real-world experiments on both platforms: multirotors with cable-suspended payload and unicycles connected by rigid rods, see [1](#fig:real_envs){reference-type="ref+label" reference="fig:real_envs"}. We describe the physical setup of each platform an the results for the problem instances. For the multirotors with payload platform, we test scenarios with two and three multirotors. The experiments include two environments: a window-like environment requiring the robots to pass through a narrow passage and a forest-like environment with dense obstacles, similar to the scenarios that were tested for the baseline. For the unicycles with rigid rods platform, we conduct experiments with two and three robots in a wall-like environment. Here, the dynamic constraints on the angular velocities of the unicycles are $\omega^i \in [-0.5, 0.5] \ \si{rad/s}$. Additionally, we demonstrate a practical use-case involving three unicycles functioning as garbage collectors, as shown in the supplemental material.

### Multirotors with Payloads

::: {#table3}
+------------------+----------------------------------------------------+---------------------------------------------------+---------------------------------+
| **Environment**  | **Energy** \[Wh\] $\downarrow$                     | **Error** \[m\] $\downarrow$                      | **Time** \[s\] $\downarrow$     |
+:================:+:===============:+:================================:+:================================:+:==============:+:==============:+:==============:+
| 2-7              | **Ours**        | **BL**                           | **Ours**                         | **BL**         | **Ours**       | **BL**         |
+------------------+-----------------+----------------------------------+----------------------------------+----------------+----------------+----------------+
| Window, 2 robots | **0.006**       | 0.01 [0.00]{style="color: gray"} | 0.08 [0.05]{style="color: gray"} | **0.05**       | **4.3**        | 7.5            |
+------------------+-----------------+----------------------------------+----------------------------------+----------------+----------------+----------------+
| Window, 3 robots | **0.007**       | 0.02 [0.00]{style="color: gray"} | 0.15 [0.06]{style="color: gray"} | **0.08**       | **4.2**        | 8.5            |
+------------------+-----------------+----------------------------------+----------------------------------+----------------+----------------+----------------+
| Forest, 2 robots | **0.007**       | 0.01 [0.00]{style="color: gray"} | 0.06 [0.03]{style="color: gray"} | **0.03**       | **5.0**        | 8.2            |
+------------------+-----------------+----------------------------------+----------------------------------+----------------+----------------+----------------+
| Forest, 3 robots | **0.009**       | 0.01 [0.00]{style="color: gray"} | 0.12 [0.06]{style="color: gray"} | **0.07**       | **4.5**        | 7.7            |
+------------------+-----------------+----------------------------------+----------------------------------+----------------+----------------+----------------+

: Physical experiments with multirotors with payload (MP). Energy, tracking error, and trajectory cost over 10 trials.
:::

[]{#table3 label="table3"}

The experiments utilize Bitcraze Crazyflie 2.1 (CF) multirotors, which are small (9 cm rotor-to-rotor) and lightweight (34 g), and are commercially available. An existing flight controller [@wahba2023efficient] is run on-board the STM32-based flight controller (168 MHz, 192 kB RAM), which also handles an extended Kalman filter for state estimation. For all scenarios, we use the open-sourced baseline implementation [@wahba2024kinodynamic]. On the host side, we used Crazyswarm2, an extension of Crazyswarm [@preiss2017crazyswarm], which leverages ROS 2 [@macenski2022robot] for commanding multiple CFs.

### Unicycles with Rods

We use commercially off-the-shelf differential-drive robots of type Polulu 3pi+ 2040. The Cortex M0+ microcontroller runs MicroPython with a nonlinear controller [@kanayama1990stable]. For state estimation, we equip the robots with low-latency radios (nRF52840) and broadcast the motion capture pose at 50 Hz. Robots are physically connected with 3D-printed rigid rods using revolute joints.

### Results

We successfully execute the generated trajectories for both systems across all environments over 10 trials, except for the baseline in the three-unicycle scenario, where no successful attempts were recorded, see Tables [2](#table3){reference-type="ref" reference="table3"}. The trajectory times of pc-dbCBS are on average 50% faster than the baseline and were successfully tracked by the existing controllers. For the cable-suspended system, the executed trajectories demonstrate that our method on average consumes $50\%$ less energy than the baseline. As expected, the average tracking error of pc-dbCBS for the multirotors with payloads degrades at the higher execution speed due to system uncertainties, such as model mismatches and state estimation inaccuracies. However, this does not impact the success rate of the experiments. For the unicycles, the average tracking error for pc-dbCBS three robots is $\SI{0.12}{m}$ executed in $\SI{8.9}{s}$. Similarly for two robots, the average tracking error is $\SI{0.12}{m}$ executed in $\SI{6.4}{s}$ and the baseline is $\SI{0.27}{m}$ in $\SI{13.2}{s}$. This is because the generated path from the baseline is overly curved, even though it is feasible. This suboptimality explains why the baseline results in collisions with obstacles for three robots.

# Conclusion

We present pc-dbCBS, a novel kinodynamic motion planner for physically-coupled robot teams. Algorithmically, our kinodynamic planner extends db-CBS for physically-coupled multi-robot systems. Our key insight is that it is beneficial to use different state representations in the same planning framework simultaneously. Specifically, we use a stacked state representation for a discrete search over motion primitives and a minimal state representation for optimization with differential dynamic programming.

Empirically, we demonstrate that our approach computes significantly higher-quality motion plans compared to a state-of-the-art baseline on two different systems: ground robots connected via rods in a line formation, and aerial robots connected through a payload in various formations. To this end, we derive and add a new physically-coupled example system using unicycle robots. Our approach, pc-dbCBS, achieves a 50-60% lower cost than the baseline, and energy consumption is reduced to 10-40% in comparison to the baseline, depending on the number of robots and their type.

In the future, the scalability of the proposed method needs to be improved further to handle larger teams in complex environments. Moreover, a closer coupling of motion planning and controls is needed in order to plan agile trajectories that can be tracked robustly on real robots.
