---
citation_key: Beck2024Model
arxiv_id: 2402.04730
arxiv_url: https://arxiv.org/abs/2402.04730
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:57:47Z
origin: ai+web
reviewed: false
---

::: keywords
Model Predictive Trajectory Optimization, Waypoints, Dynamic Replanning
:::

# INTRODUCTION {#sec:introduction}

Tasks for robotic manipulators in unstructured human environments demand sophisticated planning techniques. The dynamic nature and incomplete measurements in such environments require online replanning capabilities to ensure proper execution. Planning for such tasks can be roughly classified into a discrete sequence of actions to be executed by the robot, referred to as task planning, and planning the robot's motion to complete such actions, i.e., motion planning [@Garrett2021]. This work considers discrete actions that can be abstracted by waypoints in the robot's task space, e.g., moving to an object to grasp it from a specific pre-grasp point. In trajectory optimization, action sequences or waypoints can be modeled as constraints [@Toussaint2015]. This requires trajectory optimization over a long planning horizon that covers the action sequence's length. Such an optimization procedure is computationally expensive and, hence, unsuitable for environments where conditions change dynamically, requiring online replanning. Consider, for example, picking an object and placing it in a cabinet. Depending on the available sensors, the robot may not detect whether the cabinet is already open or whether there is any space left in its initial state when starting to plan. In this case, new observations that become available when approaching the cabinet with an object can require putting the object down and opening the cabinet door before placing the object.

:::: {#fig:wmpc_illustration .figure latex-placement="t"}
![](Beck2024Model_figs/fig_wmpc_illustration_qw.png)

::: caption
[]{#fig:wmpc_illustration label="fig:wmpc_illustration"} The proposed wMPC planner first plans towards the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$, avoiding the obstacle $\mathcal{O}$. The planner splits the horizon at $k = N_s$ as soon as the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ is reachable within a tolerance $\varepsilon$. Then, the waypoint is constrained by the planner with $\boldsymbol{\mathbf{q}}_{N_s - 1 | n} \in \mathcal{Q}_{\mathrm{w}}$ to be within the tolerance band around the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$, and the remaining samples are used to optimize towards the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$.
:::
::::

A typical approach for online trajectory optimization is model predictive control (MPC) [@GhazaeiArdakani2019; @Kraemer2020; @Schoels2020a] over a short, receding horizon. As discussed before, complex manipulation tasks are often divided into discrete actions obtained from a task planner. However, it is not apparent how to systematically include discrete-time constraints, such as waypoints, in a receding horizon concept, as these waypoints might only be reachable in future iterations. Furthermore, the timing of such waypoints is challenging to obtain. Current attempts to solve this problem rely on a tracked reference path or trajectory to maintain this global view of discrete constraints [@Toussaint2022; @Romero2022]. The disadvantage of such approaches is the need to compute such a reference. Due to the online requirement, only simplified reference paths or trajectories can be computed, i.e., collision checking is typically neglected. The approach presented in this work alleviates the requirement of global references for including waypoints in model predictive trajectory optimization with short horizons. Only the waypoints themselves are needed as inputs to the planner. The main point is that the objective function is used to plan towards a waypoint, and then a constraint is introduced to split the planning horizon at this waypoint so that planning can continue to the next waypoint or goal point. Fig. [1](#fig:wmpc_illustration){reference-type="ref" reference="fig:wmpc_illustration"} illustrates the proposed planning approach, which is described in Section [4](#sec:rhtp){reference-type="ref" reference="sec:rhtp"}.

After discussing related work in Section [2](#sec:related_work){reference-type="ref" reference="sec:related_work"}, the mathematical model is introduced in Section [3](#sec:math_model){reference-type="ref" reference="sec:math_model"}. Subsequently, the proposed waypoint MPC (wMPC) is described in Section [4](#sec:rhtp){reference-type="ref" reference="sec:rhtp"}. The wMPC algorithm is compared to (global) RRT-type planners in a simulated environment in Section V-A to demonstrate that the trajectory duration and path length are comparable despite the local nature of the MPC. A [KUKA]{.smallcaps} LBR iiwa 14 R820 robot is used to experimentally demonstrate the online replanning capabilities of the proposed approach in a pick-and-place scenario. Section [6](#sec:conclusion){reference-type="ref" reference="sec:conclusion"} concludes the paper and provides an outlook on future work.

# RELATED WORK {#sec:related_work}

## Trajectory Optimization

Classical trajectory optimization, e.g., [@Schulman2014; @RZBS2009; @BCBP2019; @Jankowski2023], optimizes an entire trajectory from an initial configuration to a goal. Waypoints can be introduced by constraining points along the trajectory. If the trajectory duration is fixed, the timing for the waypoints must also be fixed. On the other hand, if the trajectory duration is free and the end time serves as an additional optimization variable, the trajectory optimization problem becomes challenging to solve. An efficient algorithm for calculating time-optimal trajectories through waypoints offline for quadrotor flight is proposed in [@Foehn2021].

## MPC Through Waypoints

Recent years have shown extensive interest in extending trajectory optimization to online planning using MPC. This includes gradient-based methods [@GhazaeiArdakani2019; @Kraemer2020; @Schoels2020a] and sampling-based methods [@Williams2016; @Bhardwaj2022]. However, these works do not explicitly consider the problem of going through desired waypoints. Therefore, several point-to-point motions must be planned for each waypoint, which implies either stopping or specifying a desired velocity at the waypoint in advance.

In contrast, an approach based on model-predictive contouring control for time-optimal quadrotor flight with waypoints was proposed in [@Romero2022], where the waypoint timing is not predefined. This approach relies on a pre-computed reference path through the waypoints. The MPC algorithm then tracks the path, allowing more significant deviations from the path between the waypoints to obtain an approximately time-optimal trajectory. The reference path serves as a progress measure through the waypoints. However, it introduces additional complexity, which the task does not require since only passing the waypoints is necessary. Furthermore, the authors do not investigate obstacle avoidance or dynamic replanning with changing waypoints.

The sequence-of-constraints MPC proposed in [@Toussaint2022] splits a task-and-motion-planning (TAMP) problem into three steps. First, the waypoints are obtained from planning a task. Second, the timing of the waypoints is optimized, resulting in a reference trajectory. In the third step, the reference trajectory is tracked with MPC to compute collision-free trajectories over a short planning horizon. Similar to [@Romero2022], a global reference is required to consider waypoints in the MPC.

In contrast to [@Toussaint2022], the proposed approach does not compute a reference trajectory through all waypoints to determine their timing. Instead, the presented MPC formulation uses a cost-to-go towards the waypoints. It establishes a constraint for a specific timing of the waypoint as soon as the waypoint appears in the optimization horizon of the planner. Hence, the proposed approach does not need to compute a reference trajectory for the tracking MPC, which reduces the computational complexity and avoids problems with potentially infeasible reference trajectories.

In summary, the scientific contributions of this paper are three-fold:

- The proposed wMPC algorithm enables model-predictive trajectory optimization through waypoints with a receding horizon for fast online replanning without a global reference.

- The simulation results show that our wMPC successfully traverses waypoints, and the planned trajectories result in similar durations and path lengths compared to RRT\*, RRTConnect, and T-RRT in an online fashion.

- The feasibility of the proposed wMPC is demonstrated experimentally in the online replanning application of a dynamic pick-and-place scenario for the [KUKA]{.smallcaps} LBR iiwa 14 R820 robot.

# MATHEMATICAL MODEL {#sec:math_model}

The generalized coordinates $\boldsymbol{\mathbf{q}} \in \mathbb{R}^m$ define the robot's configuration. A double integrator model can be used, assuming that a suitable inverse dynamics control law, e.g., [@Ott2008], compensates for the nonlinear dynamics of the robot manipulator. For additional smoothness, however, a triple integrator model is used. The state vector is defined as $\boldsymbol{\mathbf{x}}^\mathrm{T} = [\boldsymbol{\mathbf{q}}^\mathrm{T}, \dot{\boldsymbol{\mathbf{q}}}^\mathrm{T}, \ddot{\boldsymbol{\mathbf{q}}}^\mathrm{T}]$ with the input $\boldsymbol{\mathbf{u}} = %
  {\mathop{\kern\z@\boldsymbol{\mathbf{q}}}\limits^{\makebox[0pt][c]{\vbox to-1.4\ex@{\kern-\tw@\ex@
   \hbox{\normalfont ...}\vss}}}}$. Assuming piecewise-linear inputs $\boldsymbol{\mathbf{u}}_k$ with the sampling time $h$ leads to the first-order-hold discrete-time state-space formulation $$\begin{align}
  \boldsymbol{\mathbf{x}}_{k + 1} = \boldsymbol{\mathbf{\Phi}} \boldsymbol{\mathbf{x}}_k + \boldsymbol{\mathbf{\Gamma}}_1 \boldsymbol{\mathbf{u}}_k  + \boldsymbol{\mathbf{\Gamma}}_2 \boldsymbol{\mathbf{u}}_{k + 1}\label{eqn:sys_d}\text{~,}
\end{align}$$ where $$\begin{align}
  \boldsymbol{\mathbf{\Phi}} &= \begin{bmatrix}
                  1 & h & \frac{h^2}{2} \\
                  0 & 1 & h \\
                  0 & 0 & 1    
                \end{bmatrix}\otimes \boldsymbol{\mathbf{I}}_{m}\text{~,}\quad\nonumber \\
  \boldsymbol{\mathbf{\Gamma}}_1 &= \begin{bmatrix}
                  \frac{h^3}{8} \\
                  \frac{h^2}{3} \\
                  \frac{h}{2}
               \end{bmatrix} \otimes \boldsymbol{\mathbf{I}}_{m} \text{~,}\quad
  \boldsymbol{\mathbf{\Gamma}}_2 = \begin{bmatrix}
                  \frac{h^3}{24} \\
                  \frac{h^2}{6} \\
                  \frac{h}{2}
               \end{bmatrix} \otimes \boldsymbol{\mathbf{I}}_{m}\text{~\@.}\label{eqn:sys_d_mat}
\end{align}$$ The symbol $\otimes$ denotes the Kronecker product, and $\boldsymbol{\mathbf{I}}_m$ is the identity matrix of size $m$.

# WAYPOINT MPC {#sec:rhtp}

This section presents the wMPC algorithm for trajectory optimization with waypoints over a receding horizon. For formulating the optimization problem, a waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ and a goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ in the joint space are considered. The planner must pass the waypoint and finally stop at the goal point. The MPC horizon length is initially set to its maximum $N_{\mathrm{max}}$ until the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ is reachable. Then, the horizon is split into two parts at the time index $N_{\mathrm{s}}$, where $(N_{\mathrm{s}} - 1)h$ refers to the time for reaching the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ and the remaining time from $N_{\mathrm{s}}h$ to $(N_{\mathrm{max}} - 1)h$ serves for planning towards the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$. The actual horizon length $N$ is then successively reduced when the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ appears within the horizon. Section [4.2](#sec:planning_algorithm){reference-type="ref" reference="sec:planning_algorithm"} discusses in more detail how to split the maximum horizon $N_{\mathrm{max}}$ and how to calculate $N_{\mathrm{s}}$ and the reduction of the horizon length.

## Optimization Problem {#sec:opt_problem}

The computation of the optimal trajectory for the system state $\boldsymbol{\mathbf{x}}_{0 | n}, \dots, \boldsymbol{\mathbf{x}}_{N - 1 | n}$ and the system input $\boldsymbol{\mathbf{u}}_{0|n}, \dots, \boldsymbol{\mathbf{u}}_{N - 1 | n}$ for the MPC iteration $n$ is formulated as the discrete-time optimization problem $$\label{eqn:jerk_opt}
  \begin{alignat}{2}
    &\min_{\substack{\boldsymbol{\mathbf{x}}_{0 | n}, \dots, \boldsymbol{\mathbf{x}}_{N - 1 | n}, \\\boldsymbol{\mathbf{u}}_{0 | n}, \dots, \boldsymbol{\mathbf{u}}_{N - 1 | n}}} &&\sum_{k = 0}^{N_{\mathrm{s}} - 1}  w_1 l_1(\boldsymbol{\mathbf{x}}_{k|n}) + \sum_{k = N_{\mathrm{s}}}^{N - 1}  w_2 l_2(\boldsymbol{\mathbf{x}}_{k|n}) \nonumber \\ &\quad && + \sum_{k = 0}^{N - 1} \left\lVert \boldsymbol{\mathbf{u}}_{k|n} \right\rVert_2^2 + w_3 l_{\mathrm{col}}(\boldsymbol{\mathbf{x}}_{k|n}) \label{eqn:opt_cost}\\
    &\quad \text{s.t.} && \boldsymbol{\mathbf{x}}_{k + 1 | n} = \boldsymbol{\mathbf{\Phi}} \boldsymbol{\mathbf{x}}_{k | n } + \boldsymbol{\mathbf{\Gamma}}_1 \boldsymbol{\mathbf{u}}_{k | n} + \boldsymbol{\mathbf{\Gamma}}_2 \boldsymbol{\mathbf{u}}_{k + 1 | n},\nonumber \\ &\quad && k = 0, \dots, N - 2 \label{eqn:opt_dyn}\\
    & \quad && \boldsymbol{\mathbf{x}}_{0 | n} = \boldsymbol{\mathbf{x}}_{1 | n - 1},\quad \boldsymbol{\mathbf{u}}_{0 | n} = \boldsymbol{\mathbf{u}}_{1 | n - 1} \label{eqn:init_cond_1}\\
    %& \quad && \vect{u}_{0 | n} = \vect{u}_{1 | n - 1} \label{eqn:init_cond_2}\\
    & \quad && \boldsymbol{\mathbf{x}}_{N - 1 | n} = \boldsymbol{\mathbf{\Phi}} \boldsymbol{\mathbf{x}}_{N - 1 | n},\quad \boldsymbol{\mathbf{u}}_{N - 1 | n} = \boldsymbol{\mathbf{0}}\label{eqn:steady_state_x}\\
    %& \quad && \vect{u}_{N - 1 | n} = \vect{0} \label{eqn:steady_state_u}\\
    &                  \quad && \underline{\boldsymbol{\mathbf{x}}} \le \boldsymbol{\mathbf{x}}_{k | n} \le \overline{\boldsymbol{\mathbf{x}}},\quad \underline{\boldsymbol{\mathbf{u}}} \le \boldsymbol{\mathbf{u}}_{k | n} \le \overline{\boldsymbol{\mathbf{u}}} \label{eqn:x_limit} \\
    %&             \quad &&\underline{\vect{u}} \le \vect{u}_{k | n} \le \overline{\vect{u}} \label{eqn:u_limit} \\
    & \quad && \boldsymbol{\mathbf{q}}_{N_{\mathrm{s}} - 1} \in \mathcal{Q}_{\mathrm{w}},\quad \boldsymbol{\mathbf{q}}_{N - 1} \in \mathcal{Q}_{\mathrm{g}} \label{eqn:end_point_way} %\\
    %& \quad && \vect{q}_{N - 1} \in \mathcal{Q}_{\mathrm{d}} \label{eqn:end_point_goal}
  \end{alignat}$$ where ([\[eqn:opt_dyn\]](#eqn:opt_dyn){reference-type="ref" reference="eqn:opt_dyn"}) ensures the trajectory adheres to the system dynamics. The initial states are given by ([\[eqn:init_cond_1\]](#eqn:init_cond_1){reference-type="ref" reference="eqn:init_cond_1"}) for the system state and input, where $\boldsymbol{\mathbf{x}}_{1 | n - 1}$ and $\boldsymbol{\mathbf{u}}_{1 | n - 1}$ result from the previous MPC iteration. In order to ensure that the final state in the horizon is a steady state, ([\[eqn:steady_state_x\]](#eqn:steady_state_x){reference-type="ref" reference="eqn:steady_state_x"}) is required, c.f. [@Schoels2020a]. The advantage of always ending in a steady state is that each optimized trajectory is valid and safe, resulting in an anytime property of the wMPC algorithm for static environments. For the trajectory to be executable on the robot, boundary constraints on the states and inputs ([\[eqn:x_limit\]](#eqn:x_limit){reference-type="ref" reference="eqn:x_limit"}) must be fulfilled, with the lower limits $\underline{\boldsymbol{\mathbf{x}}}$, $\underline{\boldsymbol{\mathbf{u}}}$ and the upper limits $\overline{\boldsymbol{\mathbf{x}}}$, $\overline{\boldsymbol{\mathbf{u}}}$. The final point $\boldsymbol{\mathbf{q}}_{N_{\mathrm{s}} - 1}$ in the first part of the horizon up to $N_{\mathrm{s}} - 1$ must be in the set $\mathcal{Q}_{\mathrm{w}}$ such that the waypoint is passed and the final point $\boldsymbol{\mathbf{q}}_{N - 1}$ of the overall horizon in the set $\mathcal{Q}_{\mathrm{g}}$, which is ensured by ([\[eqn:end_point_way\]](#eqn:end_point_way){reference-type="ref" reference="eqn:end_point_way"}). Depending on the reachability of the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ and the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$, $N_\mathrm{s}$ and $N$ will be reduced, as discussed in Section [4.2](#sec:planning_algorithm){reference-type="ref" reference="sec:planning_algorithm"}. The shrinking horizons ensure that only the minimum amount of required samples is used for planning, which avoids oscillations towards the end of the trajectory.

Two cases must be distinguished to determine the terminal constraint sets $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$. First, if the waypoint or the goal point is not reachable within the horizons $N_{\mathrm{s}} - 1$ or $N - 1$, respectively, the terminal constraint sets $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ are only restricted by the joint limits of the robot. Otherwise, the sets $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ are defined by a tolerance band around the waypoint $\boldsymbol{\mathbf{q}}_\mathrm{w}$ and the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ for each component $i = 0, \dots, m-1$, with the tolerance distance $\varepsilon > 0$, see ([\[eqn:qw\]](#eqn:qw){reference-type="ref" reference="eqn:qw"}) and ([\[eqn:qd\]](#eqn:qd){reference-type="ref" reference="eqn:qd"}). Thus, the sets $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ are defined as $$\begin{equation}
  \label{eqn:qw}
  \mathcal{Q}_{\mathrm{w}} = \begin{cases}
    \begin{aligned} &\{ \boldsymbol{\mathbf{q}}~|~|q_i - q_{i, \mathrm{w}}| \le \varepsilon,\\&\phantom{\{ \boldsymbol{\mathbf{q}}~|~}i = 0, \dots, m - 1 \}, \end{aligned} &\quad N_{\mathrm{s}} < N - 1 \\
    \{ \boldsymbol{\mathbf{q}}~|~\underline{\boldsymbol{\mathbf{q}}} \le \boldsymbol{\mathbf{q}} \le \overline{\boldsymbol{\mathbf{q}}} \}, &\quad \text{otherwise}  \text{~,}\\
  \end{cases}
\end{equation}$$ and $$\begin{equation}
  \label{eqn:qd}
  \mathcal{Q}_{\mathrm{g}} = \begin{cases}
    \begin{aligned} &\{ \boldsymbol{\mathbf{q}}~|~|q_i - q_{i, \mathrm{g}}| \le \varepsilon,\\&\phantom{\{ \boldsymbol{\mathbf{q}}~|~}i = 0, \dots, m - 1 \}, \end{aligned} &\quad N - 1 < N_{\mathrm{max}} \\
    \{ \boldsymbol{\mathbf{q}}~|~\underline{\boldsymbol{\mathbf{q}}} \le \boldsymbol{\mathbf{q}} \le \overline{\boldsymbol{\mathbf{q}}} \}, &\quad \text{otherwise} \text{~\@.}
  \end{cases}
\end{equation}$$

::: remark
**Remark 1**. *The change in the terminal constraint sets $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ when $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ or $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ become reachable does not impact the recursive feasibility of the optimization problem. When the environment is static, the reachability in a previous iteration implies reachability in the next iteration. If the environment changes, recursive feasibility is not ensured. However, in that case, $N_{\mathrm{s}}$ and $N$ are reset, and $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ contain the robot's reachable workspace again.*
:::

The objective functions $l_1(\boldsymbol{\mathbf{x}}_{k|n})$ and $l_2(\boldsymbol{\mathbf{x}}_{k|n})$ with the weights $w_1, w_2 > 0$ in ([\[eqn:opt_cost\]](#eqn:opt_cost){reference-type="ref" reference="eqn:opt_cost"}) give a cost-to-go towards the waypoint and the goal point, respectively. The cost-to-go is chosen as a smooth approximation of the 1-norm, resulting in $$\begin{align}
  \label{eqn:l1}
  l_1(\boldsymbol{\mathbf{x}}_{k|n}) &= \sum_{i = 0}^{m - 1} \sqrt{(q_{k, i|n} - q_{\mathrm{w}, i})^2 + \gamma^2} - \gamma \text{~,}
\end{align}$$ and $$\begin{align}
  \label{eqn:l2}
  l_2(\boldsymbol{\mathbf{x}}_{k|n}) &= \sum_{i = 0}^{m - 1} \sqrt{(q_{k, i|n} - q_{\mathrm{g}, i})^2 + \gamma^2} - \gamma \text{~,}
\end{align}$$ with a parameter $\gamma > 0$. For smaller $\gamma$, the approximation is more accurate. Convergence difficulties can occur if $\gamma$ is too small because the gradient increases close to the waypoint and goal point, respectively.

::: remark
**Remark 2**. *Choosing a 1-norm cost function for ([\[eqn:l1\]](#eqn:l1){reference-type="ref" reference="eqn:l1"}) and ([\[eqn:l2\]](#eqn:l2){reference-type="ref" reference="eqn:l2"}) has additional advantages in terms of the qualitative properties of the planned trajectories through waypoints. However, it may entail numerical issues due to the discontinuity of the gradient at the waypoint and goal point.*
:::

The objective function $l_{\mathrm{col}}(\boldsymbol{\mathbf{x}}_{k|n})$ in ([\[eqn:opt_cost\]](#eqn:opt_cost){reference-type="ref" reference="eqn:opt_cost"}) is a collision avoidance term with the weight $w_3 > 0$. Calculating the distances to the obstacles is outside the scope of this paper. It is assumed that a signed distance $d_{i, j}(\boldsymbol{\mathbf{q}}_{k|n})$ between each collision object $\mathcal{O}_i$, $i = 0, \dots, N_{O} - 1$ and each part of the collision model of the robot (including the gripper) $\mathcal{R}_j$, $j = 0, \dots, N_{R} - 1$ is available. The signed distance is easily calculated for simple geometries, like spheres and capsules. For more complex geometries, algorithms exist in the literature, e.g., [@Cameron1997]. Similar to [@Vu2020], a smooth approximation of the maximum function is employed, resulting in the collision cost term $$\begin{align}
  \varphi_{i, j}(\boldsymbol{\mathbf{q}}_{k|n}) = \frac{1}{\alpha} \log\left(1 + \exp(-\alpha(d_{i, j}(\boldsymbol{\mathbf{q}}_{k|n}) + \beta))\right) \text{~,}
\end{align}$$ with the parameters $\alpha > 0$ describing the steepness of the approximation and $\beta > 0$ shifts the curve such that $\varphi_{i, j}(\boldsymbol{\mathbf{q}}_{k|n}) > 0$ only if the robot is close to contact. The overall collision objective function $l_{\mathrm{col}}(\boldsymbol{\mathbf{x}}_{k|n})$ is then $$\begin{align}
  l_{\mathrm{col}}(\boldsymbol{\mathbf{x}}_{k|n}) = \sum_{i = 0}^{N_O - 1} \sum_{j = 0}^{N_R - 1} \varphi_{i, j}(\boldsymbol{\mathbf{q}}_{k|n}) \text{~\@.}
\end{align}$$

The weights $w_1$ and $w_2$ in ([\[eqn:opt_cost\]](#eqn:opt_cost){reference-type="ref" reference="eqn:opt_cost"}) are chosen indirectly proportional to the distances between the starting point $\boldsymbol{\mathbf{q}}_{\mathrm{init}}$ and the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ and between the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ and the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$, respectively. This results in $$\begin{align}
  %\label{eqn:weights}
  w_1 &= \frac{\sigma}{\max(\left\lVert \boldsymbol{\mathbf{q}}_{\mathrm{w}} - \boldsymbol{\mathbf{q}}_{\mathrm{init}} \right\rVert_2, d_{\mathrm{min}})}\label{eqn:w1} \\
  w_2 &= \frac{\sigma}{\max(\left\lVert \boldsymbol{\mathbf{q}}_{\mathrm{g}} - \boldsymbol{\mathbf{q}}_{\mathrm{w}} \right\rVert_2, d_{\mathrm{min}})}\label{eqn:w2} \text{~,}
\end{align}$$ where $\sigma > 0$ is a scaling factor, and $d_{\mathrm{min}} > 0$ prevents division by zero. By choosing the weights according to ([\[eqn:w1\]](#eqn:w1){reference-type="ref" reference="eqn:w1"}) and ([\[eqn:w2\]](#eqn:w2){reference-type="ref" reference="eqn:w2"}), the planner computes trajectories that take less time for shorter segments, i.e., the weights for the cost-to-go become larger for shorter segments. Hence, similar distances require similar time, making the trajectory's velocity profile consistent throughout the planned segments. When $\sigma$ is increased, the resulting trajectories are more aggressive, resulting in higher velocity. The planner can achieve approximately time-optimal behavior for large $\sigma$ and $N$, c.f. [@Verschueren2017]. The weight for the collision avoidance $w_3$ has to be larger than $w_1$ and $w_2$ to ensure collision avoidance since no constraint for collision avoidance is present in the planner.

## Planning Algorithm {#sec:planning_algorithm}

Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"} plans from the current robot state $\boldsymbol{\mathbf{x}}_{1|n - 1}$ to a Cartesian goal pose, described by the homogeneous transformation $\boldsymbol{\mathbf{T}}_{\mathrm{g}}$, through a waypoint described by $\boldsymbol{\mathbf{T}}_{\mathrm{w}}$. If a new goal arrives, the horizon lengths $N_{\mathrm{s}}$ and $N$ are set to the maximum horizon length $N_{\mathrm{max}}$, and $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ and $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ are calculated by an inverse kinematics algorithm. Then, the state and input trajectories are initialized using the solution of a previous MPC iteration if available, and the weights $w_1$ and $w_2$ are computed according to ([\[eqn:w1\]](#eqn:w1){reference-type="ref" reference="eqn:w1"}) and ([\[eqn:w2\]](#eqn:w2){reference-type="ref" reference="eqn:w2"}). Lines 1 - 10 of Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"} show this procedure.

In lines 11 - 13, the planner examines whether the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ is reachable within the maximum horizon length $N_{\mathrm{max}}$ using Algorithm [4](#alg:check_goal_distance){reference-type="ref" reference="alg:check_goal_distance"}. This algorithm checks whether the components $q_{\mathrm{g}, j}$, $j = 0, \dots, m - 1$, of a goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ (or a waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$) can be reached within the tolerance band $\varepsilon$ in the interval $[N_{\mathrm{start}}, \dots, N_{\mathrm{stop} - 1}]$, see lines 5 - 11. For this purpose, the boolean array $reached$ in line 1 of Algorithm [4](#alg:check_goal_distance){reference-type="ref" reference="alg:check_goal_distance"} keeps track of which joints can reach their goal. Even if not all components $j = 0, \dots, m - 1$ at a time instant $i \in [N_{\mathrm{start}}, \dots, N_{\mathrm{stop} - 1}]$ satisfy the condition $|q_{i,j} - q_{\mathrm{g}, j}| < \varepsilon$, the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ is reachable if $\mathop{\mathrm{sign}}(q_{i, j} - q_{\mathrm{g},j}) \neq \mathop{\mathrm{sign}}(q_{i - 1, j} - q_{\mathrm{g}, j})$ is fulfilled. Fig. 2 illustrates such a case for $m = 2$, where the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ is reachable within the tolerance band $\varepsilon$ although $|q_{i - 1,0} - q_{\mathrm{g}, 0}| > \varepsilon$ and $|q_{i, 0} - q_{\mathrm{g}, 0}| > \varepsilon$ since the connecting line goes through the tolerance band, which is indicated by the change in sign of $q_{i - 1, 0} - q_{\mathrm{g}, 0}$ and $q_{i, 0} - q_{\mathrm{g}, 0}$.

:::: {#fig:reachability_sketch .figure latex-placement="ht"}
![](Beck2024Model_figs/fig_reachability_check_sketch.png)

::: caption
[]{#fig:reachability_sketch label="fig:reachability_sketch"} This figure illustrates when a goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ counts as reachable within the horizon for $m = 2$. First, if all components $j = 0, \dots, m - 1$ of a point $\boldsymbol{\mathbf{q}}_{i}$ are within the tolerance band $\varepsilon$, then the goal is reachable. In this example, this is only the case for the second component $q_{i - 1, 1}$ and $q_{i, 1}$. However, it is evident for the first component that the connecting line between $q_{i - 1, 0}$ and $q_{i, 0}$ goes through the tolerance band.
:::
::::

If the waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}}$ is reachable at a time instant $i < N_{\mathrm{max}}$, then $N_{\mathrm{s}} = i - 1$; see lines 11 - 14 of Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"}. Analogously, if the goal point $\boldsymbol{\mathbf{q}}_{\mathrm{g}}$ can be reached at a time instant $i$ within the maximum horizon length $N_{\mathrm{max}}$, the actual horizon length $N$ is chosen as $N = i - 1$; see lines 15 - 20 of Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"}.

::: remark
**Remark 3**. *Note that when the goal is reachable for the first time, i.e., line 16 returns a value smaller than $N_{\mathrm{max}}$, an appropriate minimum horizon length must be chosen. A minimum length of at least three steps (dead-beat behavior) is necessary to drive the dynamics ([\[eqn:opt_dyn\]](#eqn:opt_dyn){reference-type="ref" reference="eqn:opt_dyn"}) from an initial condition ([\[eqn:init_cond_1\]](#eqn:init_cond_1){reference-type="ref" reference="eqn:init_cond_1"}) to the goal ([\[eqn:end_point_way\]](#eqn:end_point_way){reference-type="ref" reference="eqn:end_point_way"}) without state and input constraints. For the practical implementation, this minimum horizon length was increased to 5.*
:::

The sets $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ are determined in line 22 of Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"} according to ([\[eqn:qw\]](#eqn:qw){reference-type="ref" reference="eqn:qw"}) and ([\[eqn:qd\]](#eqn:qd){reference-type="ref" reference="eqn:qd"}), respectively. Then, the optimization problem ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"}) is solved to obtain the optimal trajectory planning result, and the first step of the trajectories $\boldsymbol{\mathbf{x}}_{0|n}$ and $\boldsymbol{\mathbf{u}}_{0|n}$ is sent to the controller and executed on the robot.

In future iterations of the same waypoint and goal point, the planner repeats the reachability checks if the waypoint or goal point was not reachable before. Otherwise, the horizon lengths are reduced by one in each iteration. The minimum horizon length towards the waypoint $N_\mathrm{s}$ is zero; see line 14 in Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"}. In contrast, the minimum horizon length for the goal point $N$ is two, see line 19 of Algorithm [3](#alg:planning){reference-type="ref" reference="alg:planning"}, because the first step in the optimization ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"}) is already constrained to the initial value of the previous MPC iteration in ([\[eqn:init_cond_1\]](#eqn:init_cond_1){reference-type="ref" reference="eqn:init_cond_1"}).

::::: {#alg:planning .figure latex-placement="!t"}
::: algorithm
$N_{\mathrm{s}} = N_{\mathrm{max}}$ $N = N_{\mathrm{max}}$ $\boldsymbol{\mathbf{q}}_{\mathrm{w}} \leftarrow~$ $\boldsymbol{\mathbf{q}}_{\mathrm{g}} \leftarrow~$ $\boldsymbol{\mathbf{x}}_{0 | n}, \dots, \boldsymbol{\mathbf{x}}_{N - 1 | n}, \boldsymbol{\mathbf{u}}_{0 | n}, \dots, \boldsymbol{\mathbf{u}}_{N - 1 | n} \leftarrow~$ $\boldsymbol{\mathbf{q}}_{\mathrm{init}} \leftarrow \boldsymbol{\mathbf{q}}_{0|n}$

$N_{\mathrm{s}} \leftarrow$ $N_{\mathrm{s}} \leftarrow \max(N_{\mathrm{s}} - 1, 0)$ $N \leftarrow$ $N \leftarrow \max(N, 5)$ $N \leftarrow \max(N - 1, 2)$

Compute $\mathcal{Q}_{\mathrm{w}}$ and $\mathcal{Q}_{\mathrm{g}}$ using ([\[eqn:qw\]](#eqn:qw){reference-type="ref" reference="eqn:qw"}) and ([\[eqn:qd\]](#eqn:qd){reference-type="ref" reference="eqn:qd"})

$\boldsymbol{\mathbf{x}}_{0 | n}, \dots, \boldsymbol{\mathbf{x}}_{N - 1 | n}, \boldsymbol{\mathbf{u}}_{0 | n}, \dots, \boldsymbol{\mathbf{u}}_{N - 1 | n} \leftarrow~$ solve optimization problem ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"})
:::

::: caption
[]{#alg:planning label="alg:planning"} wMPC Motion Planning Algorithm
:::
:::::

::::: {#alg:check_goal_distance .figure latex-placement="!t"}
::: algorithm
$\reached \leftarrow \zeros{m}$

$d \leftarrow q_{i, j} - q_{\mathrm{g}, j}$ $\reached(j) \leftarrow 1$ $\reached(j) \leftarrow 1$ $i$ $i + 1$
:::

::: caption
[]{#alg:check_goal_distance label="alg:check_goal_distance"} Check Goal Reachability
:::
:::::

## Extension to Multiple Waypoints {#sec:multiple_waypoints}

The presented wMPC algorithm can be readily extended to a sequence of waypoints $\mathcal{W} = \{\boldsymbol{\mathbf{q}}_{\mathrm{w}, 0}, \boldsymbol{\mathbf{q}}_{\mathrm{w}, 1}, \dots, \boldsymbol{\mathbf{q}}_{\mathrm{w}, N_{\mathrm{way}} - 1}\}$. There are two possibilities to achieve this. On the one hand, the optimization problem ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"}) can be extended to include several horizons instead of only two. The main advantage of this approach is that several waypoints can be considered simultaneously during the optimization, which can be necessary if the waypoints lie close together. However, this is not easy to implement because the number of waypoints is unknown in advance, and each waypoint adds computational complexity. Therefore, on the other hand, only one waypoint and one goal point are considered in the optimization problem. The current waypoint and goal point are chosen according to which waypoints the robot has passed. A waypoint is considered as reached if $N_{\mathrm{s}}$ becomes zero. In this case, the current goal $\boldsymbol{\mathbf{q}}_{\mathrm{g}} = \boldsymbol{\mathbf{q}}_{\mathrm{w}, c}$ is the new waypoint $\boldsymbol{\mathbf{q}}_{\mathrm{w}} = \boldsymbol{\mathbf{q}}_{\mathrm{w}, c}$, and the next waypoint in the sequence $\boldsymbol{\mathbf{q}}_{\mathrm{w}, c + 1}$ is chosen as the new goal $\boldsymbol{\mathbf{q}}_{\mathrm{g}} = \boldsymbol{\mathbf{q}}_{\mathrm{w}, c + 1}$ for the wMPC planner.

# SIMULATION AND EXPERIMENTAL RESULTS {#sec:results}

The presented algorithm is demonstrated for two scenarios on a [KUKA]{.smallcaps} LBR iiwa 14 R820 robot with 7-DoF.

::: {#tab:wmpc_params}
   $h$   $N_{\mathrm{max}}$   $w_3$   $\varepsilon$   $\gamma$   $\alpha$   $\beta$   $\sigma$   $d_{\mathrm{min}}$
  ----- -------------------- ------- --------------- ---------- ---------- --------- ---------- --------------------
   0.1           20            100       0.0005         0.1        1000      0.001       20             0.01

  : Planning Algorithm Parameters
:::

::: {#tab:bounds}
                                            Symbol                                                                                 Value                                          Unit
  ------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------- ------------
          $\overline{\boldsymbol{\mathbf{q}}}$, $\underline{\boldsymbol{\mathbf{q}}}$          $\pm\frac{\pi}{180}\left[170, 120, 170, 120, 170, 120, 175\right]^\mathrm{T}$       rad
    $\overline{\dot{\boldsymbol{\mathbf{q}}}}$, $\underline{\dot{\boldsymbol{\mathbf{q}}}}$     $\pm\frac{\pi}{180}\left[85, 85, 100, 75, 130, 135, 135\right]^\mathrm{T}$      rad s^−1^
   $\overline{\ddot{\boldsymbol{\mathbf{q}}}}$, $\underline{\ddot{\boldsymbol{\mathbf{q}}}}$                 $\pm\left[5, 5, 5, 5, 5, 5, 5\right]^\mathrm{T}$                   rad s^−2^

  : Upper and lower bounds for $\boldsymbol{\mathbf{q}}$, $\dot{\boldsymbol{\mathbf{q}}}$, and $\ddot{\boldsymbol{\mathbf{q}}}$.
:::

:::: {#fig:sim .figure latex-placement="!t"}
::: caption
[]{#fig:sim label="fig:sim"} Sequential manipulation task in MuJoCo [@Todorov2012]: The robot starts from an initial configuration in (a) and then moves through a sequence of waypoints to open the cabinet door in (b). Afterwards, the robot must avoid the cylindrical obstacle while approaching and grasping the object in (c). Finally, the robot places the object into the cabinet in (d).
:::
::::

::: table*
+:-----------:+:-------:+:-------:+:-------:+:-------:+:---------:+:---------:+:---------:+:--------:+:--------:+:--------:+
|             |         | Path Length \[rad\]         | Trajectory Duration \[s\]         | Planning Time \[s\]            |
+-------------+---------+---------+---------+---------+-----------+-----------+-----------+----------+----------+----------+
| Algorithm   | Type    | min     | max     | avg     | min       | max       | avg       | min      | max      | avg      |
+-------------+---------+---------+---------+---------+-----------+-----------+-----------+----------+----------+----------+
| RRTConnect  | offline | 31.0896 | 43.2777 | 36.3912 | 13.0539   | 21.1495   | 15.3991   | 0.0997   | 0.2355   | 0.1613   |
+-------------+---------+---------+---------+---------+-----------+-----------+-----------+----------+----------+----------+
| T-RRT       | offline | 29.7765 | 53.5128 | 32.8817 | 13.0094   | 20.1818   | 14.2923   | 0.1119   | 8.8188   | 0.8361   |
+-------------+---------+---------+---------+---------+-----------+-----------+-----------+----------+----------+----------+
| RRT\*       | offline | 29.5847 | 34.8799 | 31.5359 | 13.0449   | 15.6965   | 14.0404   | 130.0704 | 130.1232 | 130.0838 |
+-------------+---------+---------+---------+---------+-----------+-----------+-----------+----------+----------+----------+
| WMPC (ours) | online  | 33.4563                     | 15.1                              | 0.1                            |
+-------------+---------+-----------------------------+-----------------------------------+--------------------------------+
:::

In the first scenario, the robot must move through several waypoints to solve a sequential manipulation task in simulation using MuJoCo [@Todorov2012], placing an object in a cabinet where the robot must open the door first. This simulation experiment intends to assess the performance of the proposed online wMPC planner in terms of the resulting path length and trajectory duration compared to state-of-the-art sampling-based motion planners implemented in MoveIt [@Coleman2014].

In a second lab experiment, the proposed wMPC planner shows its unique feature to account dynamically for new and removed waypoints in real-time. To this end, the robot must grasp a cylinder from a table and insert it into a cup. The cylinder and the cup can be moved, forcing the robot to replan dynamically. Waypoints determine the approach directions for the grasping and insertion motions.

Table [1](#tab:wmpc_params){reference-type="ref" reference="tab:wmpc_params"} shows the parameters for the wMPC algorithm used in the experiments unless stated otherwise. Table [2](#tab:bounds){reference-type="ref" reference="tab:bounds"} gives the bounds for the optimization problem ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"}). Input bounds $\underline{\boldsymbol{\mathbf{u}}}$, and $\overline{\boldsymbol{\mathbf{u}}}$ are neglected because jerk is already regularized in the objective function ([\[eqn:opt_cost\]](#eqn:opt_cost){reference-type="ref" reference="eqn:opt_cost"}), and the RRT-type algorithms used in Section [5.1](#sec:sequential_manipulation){reference-type="ref" reference="sec:sequential_manipulation"} cannot account for them. The optimization problem ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"}) is implemented as a [ROS]{.smallcaps} node [@Quigley2009] in Python using CasADi [@Andersson2019] and solved with the nonlinear interior point solver IPOPT [@Waechter2006] and MA57. Planning times of $\SI{100}{\milli\second}$ are achieved, including the online solution for the analytic inverse kinematics [@Shimizu2008] for new Cartesian waypoints and a desired goal. Compatible inverse kinematics solutions for the waypoints are obtained by choosing the solution closest to the previous one in a least-squares sense. For collision checking, the robot and the robot's gripper are approximated with spheres in the relevant locations. The collision object cylinders are modeled as capsules, and the ground plane is an additional obstacle restricting the motion in $z$-direction. No collision checking is done for the cup in the dynamic replanning experiment because modeling the hollow object is more involved. Instead, waypoints are used to approach the cup from above, which ensures that no collision occurs with the cup. A video of the presented scenarios and additional scenarios can be found at [www.acin.tuwien.ac.at/8a92](www.acin.tuwien.ac.at/8a92){.uri}.

## First Scenario: Simulation Experiment for Sequential Manipulation {#sec:sequential_manipulation}

In this simulation experiment, the ability of the proposed planning algorithm to pass several waypoints to achieve a sequential manipulation task is tested and compared to offline planning algorithms in MoveIt [@Coleman2014] regarding path length and trajectory duration. The robot must move through waypoints to first open a cabinet door. Afterward, the robot must grasp a cylindrical object while avoiding an obstacle. Finally, the object must be placed in the cabinet before the robot can retreat to its initial configuration again. Fig. [5](#fig:sim){reference-type="ref" reference="fig:sim"} shows the scene setup, including the waypoints.

In order to assess the performance of the proposed (local) online wMPC planner, the same scenario is solved using (global) offline sampling-based planners implemented in MoveIt [@Coleman2014], specifically RRTConnect [@Kuffner2000], RRT\* [@Karaman2011], and T-RRT [@Jaillet2010]. A path segment is planned between each waypoint. The same analytic inverse kinematics [@Shimizu2008] solution is used to calculate the corresponding waypoints in the joint space, as in the presented wMPC approach. A time parametrization is obtained for the entire path using the Time-Optimal Trajectory Generation (TOTG) algorithm [@Kunz2012]. Table [2](#tab:bounds){reference-type="ref" reference="tab:bounds"} specifies the acceleration limits, and the velocity limits are halved to obtain meaningful interaction speeds. The scaling factor is chosen as $\sigma = 2000$ to achieve a near-time-optimal behavior. Furthermore, the collision avoidance cost is set to $w_3 = 10 \sigma$.

Table [\[tab:comparison\]](#tab:comparison){reference-type="ref" reference="tab:comparison"} summarizes the results of the comparison. Due to the stochastic nature of the RRT-type planners, the results are averaged over 50 runs. The reported planning time for the RRT-type planners includes the planning time for all path segments and the calculation of the time parametrization. The results show that the proposed online wMPC planner achieves a path length close to the average of T-RRT, which does not quite reach as short paths as RRT\* but is shorter on average than RRTConnect. The trajectory duration achieved by wMPC is slightly longer than the average duration achieved by RRT\* and T-RRT and comparable to the average trajectory duration of RRTConnect. However, the minimum duration is still shorter for RRTConnect, T-RRT, and RRTConnect, which is related to the smaller minimum path lengths for these approaches. One reason for the longer trajectory duration of the proposed wMPC approach is that by minimizing the jerk, trajectories are smoother. While the proposed approach is permanently restricted to 0.1 s planning time, RRTConnect is the only algorithm that does not exceed this planning time in rare cases. RRT\* is looking for an asymptotically optimal solution and is planning until the time limit of 10 s per path segment is reached.

The results show that the proposed wMPC approach can successfully plan in real-time through the desired waypoints with a receding horizon while still obtaining good performance in path length and trajectory duration compared to the full-horizon RRT-type planners in this scenario. Compared to the sampling-based planners, the proposed approach is susceptible to local minima due to the nonlinear optimization and the receding horizon. Hence, wMPC might fail to find a suitable solution for more cluttered scenes. However, due to the possibility of incorporating the waypoints, the planning problem can often be significantly simplified by intelligent task planning and waypoint placement. The main advantage of the proposed approach is that kinematic and dynamic constraints, in addition to waypoints, can systematically be considered in the optimization problem while planning over a receding horizon to keep planning times low.

## Second Scenario: Lab Experiment for Dynamic Replanning and Reactive Behavior {#sec:dynamic_replanning}

In this lab experiment, the robot must grasp a cylinder with a height of $h = \SI{0.15}{\metre}$ and a radius of $r = \SI{0.02}{\metre}$ and place it into a cup. The locations of the cylinder and the cup are tracked using [OptiTrack]{.smallcaps} with markers placed on their surface. Fig. [6](#fig:title_overlay){reference-type="ref" reference="fig:title_overlay"} shows an overview of the experimental setup and the scenario sequence - executed by the robot.

:::: {#fig:title_overlay .figure latex-placement="!t"}
::: caption
[]{#fig:title_overlay label="fig:title_overlay"} Robotic grasping scenario with waypoints and dynamic replanning: The robot grasps the cylinder in (a) after passing through a waypoint above it. The cup is approached in (b) through a waypoint to align the approach direction. After moving the cup, the robot adjusts the waypoint and the goal for the new cup position (c) and places the object in (d).
:::
::::

A simple task planner ensures good approach directions for the grasp and placement by placing waypoints 0.1 m and 0.15 m above the objects, respectively.

A joint-space inverse dynamics control law follows the planned trajectory after interpolating it using first-order-hold according to ([\[eqn:sys_d\]](#eqn:sys_d){reference-type="ref" reference="eqn:sys_d"}) to adapt to the higher rate of the control law. Fig. [7](#fig:replanning_3d_traj){reference-type="ref" reference="fig:replanning_3d_traj"} shows the Cartesian end-effector trajectory, and Fig. [8](#fig:replanning_plot){reference-type="ref" reference="fig:replanning_plot"} depicts the corresponding motion in the joint space. The robot moves through the waypoint to grasp the cylinder . One can observe that the motion is smooth throughout the waypoint to reach the goal. Similarly, when the robot approaches the final pair of waypoint and goal , the robot passes smoothly through the waypoint without stopping. The smoothness and continuous motion are due to the split-horizon formulation of the optimization problem ([\[eqn:jerk_opt\]](#eqn:jerk_opt){reference-type="ref" reference="eqn:jerk_opt"}), which simultaneously optimizes the movement through the waypoint and the motion to the goal. The cup is moved by hand between the retreating waypoint and the waypoint for the placement . Therefore, the algorithm has to replan several times to adjust to a new waypoint and a new goal generated by the vision system. Nevertheless, the resulting motion remains smooth between and in Fig. [8](#fig:replanning_plot){reference-type="ref" reference="fig:replanning_plot"}. One of the waypoints and the corresponding goal while moving the cup are shown at , where the robot attempts to place the cylinder in the cup before the cup is moved again, requiring the algorithm to replan for the final waypoint and goal .

:::: {#fig:replanning_3d_traj .figure latex-placement="t"}
![](Beck2024Model_figs/fig_replanning_3d_path_matlab.png)

::: caption
[]{#fig:replanning_3d_traj label="fig:replanning_3d_traj"}Cartesian end-effector trajectory for the dynamic replanning experiment: The robot starts at , moves towards the cylinder through a waypoint at , and grasps the cylinder at . Afterward, the robot moves back through and attempts to put the cylinder in the cup at , moving to the appropriate waypoint. However, the cup is moved, and the robot adjusts the trajectory to move through a waypoint at and places the cylinder in the cup at . Finally, the robot returns to the initial pose at .
:::
::::

:::: {#fig:replanning_plot .figure latex-placement="t"}
![](Beck2024Model_figs/fig_dynamic_replanning_plot.png)

::: caption
[]{#fig:replanning_plot label="fig:replanning_plot"} Planned joint-space trajectories for the dynamic replanning scenario.
:::
::::

# CONCLUSIONS {#sec:conclusion}

This work presents a novel waypoint model predictive control (wMPC) approach for systematically incorporating dynamically changing waypoints into a receding horizon trajectory optimization. When a waypoint becomes reachable within the optimization horizon, it is added to the optimization problem as a constraint. This way, the waypoint is passed with a certain tolerance but without necessarily stopping there. This approach enables dynamic replanning in real-time and reactive tracking of waypoints, which may result from superordinate task planning algorithms. Simulation results show that the proposed (local) real-time receding horizon approach yields path lengths and trajectory durations in a sequential manipulation task similar to (global) sampling-based RRT-type planners, however, with online capability. Furthermore, experimental results on a [KUKA]{.smallcaps} LBR iiwa 14 R820 robot demonstrate the reactive online replanning capabilities of the proposed algorithm, see the video in [www.acin.tuwien.ac.at/8a92](www.acin.tuwien.ac.at/8a92){.uri}.

In future work, finding waypoints for sequential manipulation tasks in a dynamically changing scene and utilizing the replanning capabilities of the wMPC algorithm to adapt to changes and feedback from the environment will be further explored.

[^1]: $^{1}$F. Beck, M. N. Vu, C. Hartl-Nesic, and A. Kugi are with the Automation and Control Institute, Technische Universität Wien (TUW), 1040 Vienna, Austria (e-mail: `beck@acin.tuwien.ac.at, vu@acin.tuwien.ac.at, hartl@acin.tuwien.ac.at,`\
    `kugi@acin.tuwien.ac.at)`

[^2]: $^{2}$A. Kugi and M. N. Vu are with the AIT Austrian Institute of Technology GmbH, 1210 Vienna, Austria (e-mail: `Andreas.Kugi@ait.ac.at, Minh.Vu@ait.ac.at)`
