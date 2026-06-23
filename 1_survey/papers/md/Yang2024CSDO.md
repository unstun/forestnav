---
citation_key: Yang2024CSDO
arxiv_id: 2405.20858
arxiv_url: https://arxiv.org/abs/2405.20858
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:09:38Z
origin: ai+web
reviewed: false
---

Yang *et al.*: CSDO_LargeScaleMVTP

::: IEEEkeywords
Multi-robot systems, Path planning for multiple mobile robots or agents, nonholonomic motion planning.
:::

# Introduction

Trajectory Planning (MVTP) seeks to generate a set of collision-free trajectories for multiple vehicles, from current positions to pre-set goals in a known unstructured environment, while minimizing travel time [@li_optimal_2021]. It is a fundamental problem with diverse applications, such as cooperative parking and warehouse automation. In practical applications, there is a need to efficiently obtain solutions within a limited time [@huang2023general]. As a non-convex optimization problem, MVTP necessitates a trade-off between solution quality and computational efficiency [@wen_cl-mapf_2022]. Particularly in scenarios involving a large number of vehicles, the frequency of vehicle-to-obstacle and vehicle-to-vehicle conflicts increases, complicating the search for optimal or even feasible solutions [@li_efficient_2021]. This work aims to develop an efficient algorithm that quickly finds feasible solutions with a high success rate for large-scale MVTP problems.

## Related Work

Existing works struggle to find feasible solutions quickly at large scales, as shown in Table [\[tab:mvtp\]](#tab:mvtp){reference-type="ref" reference="tab:mvtp"}. The main challenge lies in efficiently exploring various homotopy classes [@li_optimal_2021]. The homotopy class can be loosely defined as a set of solutions that are capable of continuous deformation into one another, without intersecting obstacles or other agents [@park2015homotopy]. Different homotopy classes can be seem as combinations of various routes and agent behaviors. The quality of local optimal solutions within each homotopy class varies significantly. In large-scale scenarios, only a few homotopy classes might contain feasible solutions, making the exploration of various homotopy classes essential [@li_optimal_2021]. Therefore, we evaluate the scalability of current MVTP algorithms in dense space based on their ability to explore homotopy classes.

*Coupled planning* methods [@li_centralized_2017] treat all vehicles as a single, high dimensional agent. This approach relies solely on the optimizer's capability to traverse between different homotopy classes. While coupled planning methods guarantee completeness and optimality, the computational complexity increases rapidly with the growing number of non-convex constraints. In general, coupled planning methods exhibit poor scalability.

*Distributed Planning* methods address MVTP in a single-agent manner, treating others as moving obstacles [@ma_decentralized_2023; @luis_online_2020; @alonso-mora_cooperative_2018], or achieve collision avoidance through communication [@ferrantiDistributedNonlinearTrajectory2023; @reyFullyDecentralizedADMM2018]. They have high efficiency in sparse scenarios but struggle with coordination, restricting the exploration of homotopy classes. In practice, these methods often struggle to generate high-quality collaboration, and the success rate decreases as scale increases, particularly in obstacle-dense scenarios.

*Sampling-based methods* [@soloveyFindingNeedleExponential2016; @lukyanenkoProbabilisticMotionPlanning2023; @shomeDRRTScalableInformed2020] mainly extend the Probabilistic Road Map (PRM) and Rapidly-exploring Random Tree (RRT) to multi-robot systems. These methods can provide probabilistic completeness and even asymptotical optimality. However, in crowded scenarios, these methods require a large number of samples, which can still lead to timeouts.

*Constraint reduction* [@li_optimal_2021; @ouyang_fast_2022; @chen_decoupled_2015] dynamically adjusts the problem's complexity by adding or removing constraints, continuously approaching a feasible or even optimal solution. They achieve transitions between different homotopy classes by solving different nonlinear programming problems (NLP). However, solving NLP can be time-consuming.

*Tube construction* methods [@honig_trajectory_2018; @park_efficient_2020; @shi2021neural] construct a safe corridor for each vehicle so the vehicle can be separated from the obstacles and other vehicles. Tube construction's solution is strictly homotopic to the reference trajectories. Therefore, it only searches limited homotopy classes and performs poorly without an approximately feasible initial guess.

*Grid search* [@li_efficient_2021; @wen_cl-mapf_2022] based methods discretize vehicle poses, actions, and space, utilizing a search algorithm to find discrete trajectories. This search algorithm is closely linked to a well-studied problem known as Multi-Agent Path Finding (MAPF), focusing on planning collision-free paths for multiple agents in a grid-like environment while minimizing travel time. Despite the NP-hard nature of MAPF, various efficient sub-optimal algorithms can generate paths for hundreds of agents in under a second [@ma_searching_2019], aligning with MVTP's need for finding feasible solutions efficiently. However, the potential of these efficient MAPF algorithms remains largely unexplored in the MVTP field [@okumura2022priority]. Moreover, akin to single-agent grid searching motion planning algorithms, when the search step size is too small, the search space becomes too large, posing challenges for real-time requirements. Conversely, when the search step size is too large, the solution space diminishes, making it challenging to find a solution, and collisions may occur between search steps, rendering the solution infeasible. Therefore, grid search-based methods are more suitable for generating a coarse initial guess containing homotopy class information than directly generating fine solutions.

## Motivations and Contributions

Based on the aforementioned literature review, existing methods search limited homotopy classes or search them inefficiently. In this letter, we propose using an efficient MAPF solver to explore various coarse initial guesses with a large step size, which implictly encode different homotopy classes. After obtaining an initial guess that contains a specific homotopy class, decentralized optimization is employed to quickly generate a nearby kinematically feasible solution, ultimately achieving rapid generation of feasible solutions within a limited time.

Accordingly, the main contributions are outlined as follows.

1.  CSDO, an efficient, scalable multi-vehicle trajectory planning algorithm, employs a hierarchical framework to enhance search capabilities across diverse homotopy classes. Experiments demonstrate CSDO outperforms existing methods in random scenarios, especially in large scale and high-density environments.

2.  A seamless adaptation of the priority-based search method from the MAPF domain into the complex non-holonomic MVTP problems, enables efficient exploration for feasible or near-feasible solutions.

3.  An efficient distributed local solver is introduced. Given a homotopically correct reference solution, the local solver can generate feasible solutions quickly.

# Problem Definition

The MVTP problem can be defined by a ten element tuple $\langle M,\mathcal{W},\mathcal{O},z,\mathcal{R},s,g,f,\mathcal{T}, X \rangle$. Consider a system consisting of $M$ front-steering agents $a^{(1)}, a^{(2)}, ..., a^{(M)}$ operating in a continuous planar workspace $\mathcal{W} \subset \mathbb{R}^2$. For simplicity, we use $[M]$ to denote the set $\{1,2,...,M\}$ and superscript $(i)$ to represent the variable related to agent $a^{(i)}$. There are some random static obstacles lying in the environment and occupying the workspace $\mathcal{O}$. $z=[x, y, \theta, \phi]^T \in \mathbb{R}^4$ refers to the state, where $(x, y)$ is the position of rear axis center, $\theta$ is yaw angle and $\phi$ is front-wheel steering angle. The control input is denoted as $u=[v,\omega]^T \in \mathbb{R}^2$, where $\omega=\dot\phi$, $v$ is the velocity. Agent $a^{(i)}$'s trajectory is represented by a sequence of its states sampled at fixed time interval $\Delta t$. It is denoted as $\mathcal{T}^{(i)} = [z_0^{(i)}, z_1^{(i)}, ..., z_{\tau_f^{(i)}}^{(i)}]$, where the $\tau_f^{(i)}+1$ is the number of states in the trajectory. For one MVTP task, $\mathcal{T}^{(i)}$ need to start from the start state $s^{(i)}$ and end at the goal state $g^{(i)}$. $$\begin{equation}
 \label{eq:boundary_ocp}
    z^{(i)}_0 = s^{(i)}, z^{(i)}_{\tau_f^{(i)}} = g^{(i)}, \forall i \in [M].
\end{equation}$$ The task finish time is $makespan$ $\tau_f$, where $\tau_f = \max_{i \in [M]} \tau_f^{(i)}$. It is assumed that the agent waits at the goal until all the agents have reached their goals, i.e. $z_t^{(i)} = g^{(i)}, \forall \tau_f^{(i)} 
\leq t \leq \tau_f$. The planned trajectory $\mathcal{T}$ should be kinematic feasible for the Ackermann-steering model $f$, i.e., $$\begin{equation}
\label{eq:kine_ocp}
\begin{aligned}
z_{t+1} &= z_{t} + \begin{bmatrix}
    v_t \cos \theta_t \\
    v_t \sin \theta_t \\
    v_t \tan(\phi_t)/L \\
    \omega \\
 \end{bmatrix} \Delta t, 
 \forall 0 \leq t < \tau_f,
\end{aligned}
\end{equation}$$

$$\begin{equation}
 \label{eq:control_max_ocp}
% \begin{aligned}
 \left | v_t \right | \leq v_{max}, \left | \omega_t \right | \leq \omega_{max}, 
 \forall 0 \leq  t < \tau_f,
% \end{aligned}
\end{equation}$$ $$\begin{equation}
 \label{eq:phi_max_ocp}
% \begin{aligned}
 \left | \phi_t \right | \leq \phi_{max},  
 \forall 0 \leq  t \leq \tau_f ,
% \end{aligned}
\end{equation}$$ where the $L$ is the vehicle's wheelbase. We use agent occupancy function $\mathcal{R}(z) : \mathbb{R}^4 \rightarrow \mathcal{W}$ to represent the workspace occupied by the agent's body at state $z$. The agents cannot collide with static obstacles or any other agents, i.e., $$\begin{equation}
 \label{eq:static_ocp}
    \mathcal{R}(z^{(i)}_{t}) \cap \mathcal{O}  = \emptyset, \forall t \geq 0, \forall i\in [M],
\end{equation}$$ $$\begin{equation}
 \label{eq:inter_ocp}
    \mathcal{R}(z^{(i)}_{t}) \cap \mathcal{R}(z^{(j)}_{t}) = \emptyset, \forall t \geq 0, \forall i,j\in [M], i \neq j.
\end{equation}$$

The solution plan $X$ comprises collision-free trajectories and control inputs of all agents. The solution quality is measured by $\tau_f$. Considering the summarized elements, a traditional optimal control problem [@li_optimal_2021] can be formulated as $$\begin{equation}
\label{eq:ocp}
\begin{aligned}
\min_{X, \tau_f} & \quad \quad \tau_f\\
\textrm{s.t.}& \quad  \textrm{Boundary Constraints (\ref{eq:boundary_ocp})},\\
  & \quad \textrm{Kinematic Constraints (\ref{eq:kine_ocp}), (\ref{eq:control_max_ocp}), (\ref{eq:phi_max_ocp}),}  \\
  & \quad \textrm{Static Collision Constraints (\ref{eq:static_ocp})}, \\
  & \quad \textrm{Inter-Agent Collision Constraints (\ref{eq:inter_ocp})}. 
\end{aligned}
\end{equation}$$

# Method

:::: {#fig:Fig1 .figure latex-placement="htpb"}
![](Yang2024CSDO_figs/Fig1.png){width="90%"}

::: caption
The CSDO framework for multi-vehicle trajectory planning.
:::
::::

The overall CSDO framework is illustrated in Fig. [1](#fig:Fig1){reference-type="ref" reference="fig:Fig1"}. Upon receiving the start poses, goal poses, and obstacle information, these components are combined to form a Multi-Vehicle Trajectory Planning (MVTP) instance. Subsequently, the centralized priority based searching phase generates coarse trajectories as an initial guess. The decentralized Sequential Quadratic Programming (SQP) refinement follows, where inter-vehicle constraints are decomposed and sent to multiple vehicles. Each vehicle utilizes the SQP solver to derive its trajectory and start to tracking simultaneously to reach their respective goals.

## Centralized Priority based Searching

:::: {#fig:Fig2 .figure latex-placement="htpb"}
![](Yang2024CSDO_figs/Fig2.png){width="100%"}

::: caption
MVTP discretization process.
:::
::::

By discretizing the MVTP problem, we can utilize search algorithms to find an initial guess. As in Fig. [2](#fig:Fig2){reference-type="ref" reference="fig:Fig2"}, the discretizing process consists of state $z$ discretization, kinematic model $f$ discretization and agent collision detection implementation in formula ([\[eq:static_ocp\]](#eq:static_ocp){reference-type="ref" reference="eq:static_ocp"}-[\[eq:inter_ocp\]](#eq:inter_ocp){reference-type="ref" reference="eq:inter_ocp"}) as in single vehicle search algorithm hybrid A\* [@dolgov_path_2010]. The discrete state $\hat z = [\hat x, \hat y, \hat \theta, 0]^T$, which contains the closest grid center position and discrete yaw angle, i.e., $\hat{z} = \mathop{\mathrm{arg\,min}}_{\hat z} || z - \hat z ||^2$. As in Fig. [2](#fig:Fig2){reference-type="ref" reference="fig:Fig2"}(a), $\hat z^{(i)}(t_k)$ is the discrete state of $z^{(i)}(t_k)$; The kinematic model $f$ is simplified to an action set and limited to constant speed due to time complexity. $Actions=\{FL, FS, FR, BL, BS, BR, Wait\}$, which stand for front-max-steering-left, front-straight, front-max-steering-right, back-max-steering-left, back-straight, back-max-steering-right and wait respectively. Except for the $Wait$ action, all the actions, travel for the same step size $\Delta S$. In the grid search process, we adopt a large step size to search a coarse trajectory; Separating Axis Theorem is utilized the to check the collision at the sampling moment.

:::: {#fig:Fig3 .figure latex-placement="htpb"}
![](Yang2024CSDO_figs/Fig3.png){width="90%"}

::: caption
Centralized priority based searching framework.
:::
::::

Our overall framework is illustrated in Fig. [3](#fig:Fig3){reference-type="ref" reference="fig:Fig3"}. It is worth noting that our CSDO architecture can achieve optimal or bounded sub-optimal solutions by applying corresponding MAPF algorithms. We choose PBS to find a feasible solution efficiently. Centralized searching is divided into two layers of search. At the high level, each node represents a subproblem, and each node contains a *constraint set* consisting of partial priority orders. Specifically, a partial priority order consists of two agents and refers to the avoidance relationship. For instance, if $a^{(i)} \prec a^{(j)}$, then $a^{(j)}$ has a lower priority than $a^{(i)}$, and $a^{(j)}$ treats $a^{(i)}$ as a dynamic obstacle to avoid in the low-level planner. For any two agents, they may not have a relationship of $a^{(i)} \prec a^{(j)}$ or $a^{(j)} \prec a^{(i)}$, meaning they ignore each other and may have collisions. If collisions arise within a node's plan, two possible partial orders according to a specific conflict will be added to generate child nodes until collisions are entirely resolved.

### High-level search

::: algorithm
$Root \gets$GENERATEROOT() STACK $\gets \{Root\}$

false;
:::

We adapt PBS [@ma_searching_2019; @li_intersection_2023] to address our problem as follows. As in algorithm [\[algo:pbs\]](#algo:pbs){reference-type="ref" reference="algo:pbs"}, the root node \[Line 1\] is initialized with an empty set of priority orders, but we employ a **warm start** technique to speed up the search process. Within the root node, we attempt to plan the agents sequentially, treating the previously planned agents as dynamic obstacles. If any agent encounters planning failure due to obstruction by preceding agents, we allow it to plan its trajectory freely; When expanding a node, we check for collisions between each vehicle pair. If no collisions are detected, the node is considered the final result \[Lines 5 to 6\]. Otherwise, we select a pair of colliding vehicles, $a^{(i)}$ and $a^{(j)}$ \[Line 7\]. The following part describes the detailed procedure of node expansion as shown in Fig. [3](#fig:Fig3){reference-type="ref" reference="fig:Fig3"}. Two constraints, $a^{(i)} \prec a^{(j)}$ and $a^{(j)} \prec a^{(i)}$, are created and added separately to form the new child nodes' constraint sets. For example, $\prec_{n_i} = \prec_{n} \cup \{a^{(i)} \prec a^{(j)} \}$ as in node $n_i$ \[Lines 10 to 11\]. One straightforward replanning method involves replanning all the agents according to $n_x$. However, to update the plan \[Line 12\] without redundant replanning, we first identify the agents violating the new constraint set $\prec_{n_x}$ and perform a topological sorting on the agents. Next, we replan the agents from higher to lower priority using the low-level planner. Finally, feasible child nodes are inserted \[Line 13\] in the non-decreasing order of the planned makespan of the nodes.

### Low-level planner

We directly adopt the complete and optimal spatiotemporal Hybrid A\* (STHA\*) from [@wen_cl-mapf_2022] as our low-level planner. Compared with Hybrid A\*, STHA\* adds a time dimension to deal with the dynamic obstacles. Given a workspace $\mathcal{W}$ and static obstacle occupancy workspace $\mathcal{O}$, the higher priority agents' trajectories $highTrajs$, a predefined start state $s_i$ and goal state $g_i$, STHA\* will search the fastest trajectory when the solution space is not empty.

### Completeness and Optimality Analysis

:::: {#fig:pbs_complete .figure latex-placement="htpb"}
p ![image](Yang2024CSDO_figs/pbs_completeness.png){width="95%"}

::: caption
PBS failed reason and well-formed scenarios.
:::
::::

Prioritized planning can fail to find a solution due to inappropriate priority orders [@yangAttentionbasedPriorityLearning2024]. The only issues are target blocking and run-over, as illustrated in Fig. [4](#fig:pbs_complete){reference-type="ref" reference="fig:pbs_complete"}. Target blocking occurs when a high-priority agent reaches its goal early and blocks a low-priority agent between its current position and goal. Run-over happens when a low-priority agent has no possible trajectory to avoid a high-priority agent. By utilizing tree search, PBS can explore all possible priority orders, making it **P-complete**. This capability allows PBS to greatly mitigate the above issues. Furthermore, in well-formed problems, all priority orders can lead to a feasible solution. So PBS can quickly find a feasible and even near-optimal solution. The key feature of well-formed problems is that agents can wait at their start and goal positions indefinitely without blocking other agents [@ma_searching_2019]. In practice, well-formed problems are very common, such as in intersection coordination[@li_intersection_2023]. Additionally, by changing the search strategy from depth-first search to best-first search, PBS can find a **P-optimal** solution, meaning it can find the best solution quality among the priorities, being optimal or near-optimal in practice [@ma_searching_2019].

## Decentralized SQP

As shown in Fig. [1](#fig:Fig1){reference-type="ref" reference="fig:Fig1"}, after inputting the initial guess, the separation planes are constructed to serve as inter-vehicle constraints. Then, multiple distributed SQP processes are employed to generate all the trajectories.

**Notation**. For clarity, the bar symbol represents the constant value. The subscript 0 denotes the constant associated with initial guess. For instance, $\bar \theta^{(i)}_{t,0}$ is the yaw angle of agent $a^{(i)}$ at timestamp $t$ in the interpolated initial guess. When there is no ambiguity, we omit the corresponding superscript $(i)$ or subscript $t$ when referring to all agents or any timestamp.

### Initial Guess Interpolation

**Input** initial guess $\bar X_{raw0}$. **Output** interpolated initial guess $\bar X_0$.

:::: {#fig:Fig4 .figure latex-placement="htpb"}
![](Yang2024CSDO_figs/Fig4.png){width="100%"}

::: caption
The initial guess and collision states after interpolation.
:::
::::

We interpolate each curve segment by inserting $n_{interp}$ points into each segment. So the time interval $\Delta t$ of adjacent points can be calculated as $\Delta t = \Delta S /((n_{interp}+1) v_{max})$. Afterwards, the initial guess may encounter three types of minor collisions, as illustrated in Fig. [5](#fig:Fig4){reference-type="ref" reference="fig:Fig4"}: type A: collisions between two vehicles, type B: collisions with obstacles, and type C: off-map states.

### Neighbor Pair Searching

**Input** Interpolated initial guess $\bar X_0$. **Output** Neighbor pairs $NPairs$.

To facilitate distance measuring for neighbor pair search and collision avoidance, we employ two uniformly distributed circles to cover the rectangular shape of the vehicle [@ouyang_fast_2022]. As illustrated in Fig. [6](#fig:Fig5){reference-type="ref" reference="fig:Fig5"}, the circle centers are positioned at the quadrant points. The formulas for calculating the centers and radii of the two circles are as follows.

:::: {#fig:Fig5 .figure latex-placement="htpb"}
![](Yang2024CSDO_figs/Fig5.png){width="100%"}

::: caption
Generate separating planes for neighbor pairs.
:::
::::

$$\label{eq:state2disc}
\begin{equation}
x^{F} = x + L_{f2x} \cos{\theta} ,
y^{F} = y + L_{f2x}  \sin{\theta} ,
\end{equation}
\begin{equation}
x^{R} = x + L_{r2x} \cos{\theta},
y^{R} = y + L_{r2x}\sin{\theta},
\end{equation}
\begin{equation}
r_v = \frac{1}{2} \sqrt{\frac{1}{4}(L_F^2 + L_B^2) + L_B^2},
\end{equation}$$ where the $L_{f2x} = (3L_F - L_B)/4$ and $L_{r2x} = (L_F - 3L_B)/4$ are distance from the rear-axis center to the front and rear disc center, $L_F$ and $L_R$ are the distance from rear axis to the front bumper and rear bumper. $Y^{F} = [x^{F}, y^{F}]^T$ and $Y^{R}=[x^{R}, y^{R}]^T$ are the center of the front and rear circle. $r_v$ is the radius of the circle. We denote $Y=[x^F,y^F,x^R,y^R]^T$ as the vector of the circles positions.

Given a distance threshold $R_{trust}$, we iterate through the plan to search pairs of agents $a^{(i)}$ and $a^{(j)}$ with a distance less than $2\sqrt{2}R_{trust}$ at the same timestamp. The distance function between two states $(z^{(i)}_t, z^{(j)}_t)$ is defined as follows: $$\begin{equation}
\begin{aligned}
    dist&(z^{(i)}_t, z^{(j)}_t) = \min( 
    \left \| Y^{F(i)}_t - Y^{F(j)}_t  \right \|, 
    \left \| Y^{F(i)}_t - Y^{R(j)}_t  \right \|, \\
  &\quad \left \| Y^{R(i)}_t - Y^{F(j)}_t  \right \|, 
    \left \| Y^{R(i)}_t - Y^{R(j)}_t  \right \| ) - 2r_v,
\end{aligned}
\end{equation}$$ where the $Y^{F(i)}_t$, $Y^{R(i)}_t$, $Y^{F(j)}_t$, $Y^{R(j)}_t$ are the agent $a^{(i)}$'s front disc center, back disc center, agent $a^{(j)}$'s front disc center and rear disc center respectively. The search result, denoted as $NPairs$, comprises neighbor pairs and their corresponding timestamps. $NPairs=\{(a^{(i)},a^{(j)},t)|dist(z^{(i)}_t, z^{(j)}_t) \leq 2\sqrt{2}R_{trust}, \forall i,j \in [M], i \neq j, \forall 0 \leq t \leq \tau_f \}$.

### Neighbor Pair Division

**Input** neighbor pairs $NPairs$. **Output** inter-collision avoidance constraints ([\[eq:inter\]](#eq:inter){reference-type="ref" reference="eq:inter"} - [\[eq:trust\]](#eq:trust){reference-type="ref" reference="eq:trust"}).

After obtaining the neighbor pairs $NPairs$, we utilize the plane derived by the perpendicular bisector of the disc's center as the constraint for mutual avoidance between vehicles. Each neighbor pair $(a^{(i)},a^{(j)},t)$ generates 4 separation planes {$C_{ffj}^{(i)}, C_{frj}^{(i)}, C_{rfj}^{(i)}, C_{rrj}^{(i)}$} for agent $a^{(i)}$. Fig. [6](#fig:Fig5){reference-type="ref" reference="fig:Fig5"} illustrates the process. Calculating perpendicular bisectors, offset by a distance of $r_v$ to obtain the separation half-plane $C_{ffj}^{(i)}$. Similarly, we generate the front-to-rear, rear-to-front and rear-to-rear separation half-planes $C_{frj}^{(i)}$, $C_{rfj}^{(i)}$ and $C_{rrj}^{(i)}$, respectively.

$$\begin{equation}
\label{eq:inter}
   \bar A_{c,0} Y \leq \overrightarrow{0},
\end{equation}$$ where the $\bar A_{c,0}$ denotes the corresponding half planes. Notably, this method seamlessly adapts RSFC [@parkOnlineTrajectoryPlanning2021] under the assumption of two-circle approximation and discrete-time collision detection.

To focus the search within the neighbor of the initial guess, we restrict the variation range of the disk to $R_{trust}$, i.e., $$\begin{equation}
\label{eq:trust}
    \left | Y - \bar Y_{0} \right |\leq R_{trust}\overrightarrow{1}.
\end{equation}$$

::: remark
**Remark 1** (). *Constraints ([\[eq:inter\]](#eq:inter){reference-type="ref" reference="eq:inter"})-([\[eq:trust\]](#eq:trust){reference-type="ref" reference="eq:trust"}) are equivalent to constraint ([\[eq:inter_ocp\]](#eq:inter_ocp){reference-type="ref" reference="eq:inter_ocp"}), guaranteeing that there are no collisions between vehicles at each discrete time step.*
:::

::: proof
*Proof.* For neighbor pairs, they are separated by the planes as in constraint ([\[eq:inter\]](#eq:inter){reference-type="ref" reference="eq:inter"}). For non-neighbor pairs, they are separated by the variation range constraint ([\[eq:trust\]](#eq:trust){reference-type="ref" reference="eq:trust"}). ◻
:::

::: remark
**Remark 2** (). *Constraints ([\[eq:inter\]](#eq:inter){reference-type="ref" reference="eq:inter"})-([\[eq:trust\]](#eq:trust){reference-type="ref" reference="eq:trust"}) decouple the trajectory variables between different vehicles.*
:::

::: proof
*Proof.* $\bar A_{c,0}$ and $\bar Y_{0}$ are constants determined by the initial guess. For any two different vehicles $a^{(i)}$ and $a^{(j)}$, their variables $z^{(i)}$ and $z^{(j)}$ will not appear in the same inequality. ◻
:::

The above process decouples agents for distributed problem-solving. Without loss of generality, we describe the processing procedure for agent $a^{(i)}$ in the following steps. This process is executed repeatedly until the stop criteria are met. **Notation**. The subscript $k$ represents the k-th iteration, with $k=0$ indicating the initial guess.

### Robust Corridor Construction

**Input** obstacles $\mathcal{O}$ and $\bar X^{(i)}_{k}$. **Output** static collision avoidance constraints ([\[eq:static\]](#eq:static){reference-type="ref" reference="eq:static"}).

To handle the static obstacle avoidance constraint ([\[eq:static_ocp\]](#eq:static_ocp){reference-type="ref" reference="eq:static_ocp"}), we adapt the method from [@li_optimization-based_2022] to generate a corridor along the last iteration solution $\bar X_k^{(i)}$ of agent $a^{(i)}$.

For clarity, ensuring that a disc with radii $r_v$ does not go out of the map is equivalent to maintaining a distance of $r_v$ from the border. As in Fig. [7](#fig:corridorConstruction){reference-type="ref" reference="fig:corridorConstruction"}, we erode the map by a distance of $r_v$ to define the safety space enclosed by the dotted line. Similarly, we dilate the obstacles by a distance of $r_v$.

As illustrated in Fig. [7](#fig:corridorConstruction){reference-type="ref" reference="fig:corridorConstruction"}, we sequentially extend the empty box clockwise in all four directions until it encounters dilated obstacles, the eroded map boundary, or reaches the maximum allowed length. Details can be found in [@li_optimization-based_2022].

Note that our initial point may be in an out-of-map or colliding state, as previously mentioned in Fig. [5](#fig:Fig4){reference-type="ref" reference="fig:Fig4"}, causing the algorithm to immediately return an empty box. Therefore, we must relocate the initial point to a safe position before generating the box. For initial points that are out-of-map, we project them onto the map boundary. If the original or projected state collides with obstacles, we move the point outside of the grey circle. If it remains unsafe due to collisions with other obstacles, we gradually rotate it around the obstacle center until it becomes safe. The corridor constraints can be summarized as follows, $$\begin{equation}
 \label{eq:static}
   \bar Y^{(i)}_{min,t,k} \leq \bar A_{static,t,k}^{(i)}Y^{(i)}_{t,k+1} \leq \bar Y^{(i)}_{max,t,k}, \forall 0 \leq t \leq \tau_f,
\end{equation}$$ where $\bar A_{static,t,k}^{(i)}$ denotes the generated corridor as in Fig. [7](#fig:corridorConstruction){reference-type="ref" reference="fig:corridorConstruction"}.

:::: {#fig:corridorConstruction .figure latex-placement="htpb"}
![](Yang2024CSDO_figs/corridorConstruction.png){width="95%"}

::: caption
Corridor construction from a legal start point.
:::
::::

### QP Formulation

**Input** constraints ([\[eq:inter\]](#eq:inter){reference-type="ref" reference="eq:inter"}-[\[eq:static\]](#eq:static){reference-type="ref" reference="eq:static"}) and last solution $\bar X^{(i)}_{k}$. **Output** Refine agent solution $\bar X^{(i)}_{k + 1}$.

Finally, we linearize the kinematic constraints. This enables the smooth speed profile generation. The linearization error will be alleviated by the following sequential refinements. The objective function is set to minimize changes in velocity and steering wheel angle, aiming to smooth the trajectory. The objective function is as follows, $$\begin{equation}
\label{eq:cost}
    J = \Sigma_{t} (\alpha_v (\Delta v_{t,k+1}^{(i)})^2 + \alpha_{\omega} (\omega_{t,k+1}^{(i)} )^2),
\end{equation}$$ where $\alpha_v$ and $\alpha_\omega$ are the weighting parameters.

The kinematic constraints are linearized as follows: $$\label{eq:linear_kine}
\begin{equation}
z_{t+1,k+1}^{(i)} = \bar A_{t,k}^{(i)} z_{t,k+1}^{(i)} +\bar B_{t,k}^{(i)} u_{t,k+1}^{(i)} + \bar c_{t,k}^{(i)}, \forall 0 \leq t < \tau_f
\end{equation}
\begin{equation}
    \bar A_{t,k}^{(i)} = \begin{bmatrix}
     1& 0 & -\bar v_{t,k}^{(i)} \sin \bar \theta_{t,k}^{(i)} *\Delta t & 0 \\ 
     0& 1 & -\bar v_{t,k}^{(i)} \cos \bar \theta_{t,k}^{(i)} *\Delta t & 0\\ 
     0& 0 & 1 & \frac{\bar v_{t,k}^{(i)}*\Delta t}{L \cos^2 \bar \phi_{t,k}^{(i)}}  \\ 
     0& 0 & 0 & 1
\end{bmatrix} ,
\end{equation}
\begin{equation}
\bar B_{t,k}^{(i)} = \begin{bmatrix}
 \cos \bar \theta_{t,k}^{(i)} \Delta t& \sin\bar \theta_{t,k}^{(i)} \Delta t &  \frac{\tan \bar \phi_{t,k}^{(i)} \Delta t}{L} &0 \\ 
 0& 0&  0&  \Delta t 
\end{bmatrix}^T,
\end{equation}
\begin{equation}    
\bar c_{t,k}^{(i)} = [\bar \theta_{t,k}^{(i)} \bar v_{t,k}^{(i)} \sin \hat{\theta_{t,k}^{(i)}} \Delta t, -\bar \theta_{t,k}^{(i)} \bar v_{t,k}^{(i)} \cos \hat{\theta_{t,k}^{(i)}} \Delta t, -\frac{\bar \phi_{t,k}^{(i)} \Delta t}{L \cos^2{\phi_{t,k}^{(i)}}}]^T, 
\label{eq:end}
\end{equation}$$ where $(\bar A_{t,k}^{(i)}, \bar B_{t,k}^{(i)}, \bar c_{t,k}^{(i)})$ are the associated coefficients.

To handle the non-linear calculation from state $z$ disc center positions $Y$, we need to linearize the Eq. ([\[eq:state2disc\]](#eq:state2disc){reference-type="ref" reference="eq:state2disc"}), i.e., $$\label{eq:linearState2Y}
\begin{equation}
    Y_{t,k+1}^{(i)} = \bar D_{t,k}^{(i)} z_{t,k+1}^{(i)} + \bar e_{t,k}^{(i)}, \forall 0 \leq t \leq \tau_f
\end{equation}
\begin{equation}
    \bar D_{t,k}^{(i)} = \begin{bmatrix}
    1 & 0 & -L_{f2x} \sin \bar \theta_{t,k}^{(i)} & 0 \\
    0 & 1 & L_{f2x} \cos \bar \theta_{t,k}^{(i)} & 0 \\
    1 & 0 & -L_{r2x} \sin \bar \theta_{t,k}^{(i)} & 0 \\
    0 & 1 & L_{r2x} \cos \bar \theta_{t,k}^{(i)} & 0      \\
    \end{bmatrix}, \\
\end{equation}
\begin{equation}
    \bar e_{t,k}^{(i)} = \begin{bmatrix}
    L_{f2x}(\cos{\bar \theta_{t,k}^{(i)}} + \bar \theta_{t,k}^{(i)} \sin \bar \theta_{t,k}^{(i)})  \\
    L_{f2x}(\sin{\bar \theta_{t,k}^{(i)}} - \bar \theta_{t,k}^{(i)} \cos \bar \theta_{t,k}^{(i)})  \\
    L_{r2x}(\cos{\bar \theta_{t,k}^{(i)}} + \bar \theta_{t,k}^{(i)} \sin \bar \theta_{t,k}^{(i)})  \\
    L_{r2x}(\sin{\bar \theta_{t,k}^{(i)}} - \bar \theta_{t,k}^{(i)} \cos \bar \theta_{t,k}^{(i)})  
\end{bmatrix}. \\
\end{equation}$$

With the aforementioned elements summarized, a complete QP is formulated as follows,

$$\begin{equation}
\begin{aligned}
\min_{{X}^{(i)}} \quad &  J \\
\textrm{s.t.} \quad & z_{0,k+1}^{(i)}=[s^{(i)T}, 0]^T, z_{\tau_f,k+1}^{(i)}=[g^{(i)T}, 0]^T, \\
  & \left | v^{(i)}_{t,k+1} \right | \leq v_{max}, \left | \omega^{(i)}_{t,k+1} \right | \leq \omega_{max}, \forall 0 \leq  t < \tau_f,\\
  & \left | \phi^{(i)}_{t,k+1} \right | \leq \phi_{max},  \forall 0 \leq  t \leq \tau_f,\\
  & \textrm{Constraints \quad (\ref{eq:inter})-(\ref{eq:linearState2Y})} \quad \textrm{related to $a^{(i)}$}
\end{aligned}
\end{equation}$$

### Stop Criteria

When the $|| \bar X_{k+1} - \bar X_k ||_2$ is less than the given threshold, or the plan is feasible, we stop the iteration.

# Experiment

To demonstrate the effectiveness of our method, we conduct experiments on randomly generated obstructed maps as well as obstacle-free maps. We incrementally increased the number of agents in the problem, resulting in more congested maps, with a specific emphasis on showcasing the effectiveness of our approach in addressing large-scale MVTP problems.

## Simulation Settings

The benchmark consists of various map sets with different sizes (50 m , 100 m), varying numbers of agents (5 to 100), and includes both random and room-like maps. Each map set contains 60 instances, resulting in a total of 2100 test instances in this testing benchmark. We assume all agents are homogeneous and share the following parameters: the vehicle's shape is 3 m × 2 m, and it has a maximum speed of 1 m/s. All algorithms are assessed using their respective open-source implementations, with most executed on an Intel Xeon Gold 622R CPU at 2.90 GHz in C++, while Fast-ASCO runs on an Intel Core i7-9750H CPU at 2.6 GHz in Matlab.

## Simulation Results

::::: {#fig:map100 .figure latex-placement="htpb"}
::: center
  --------------------------------------------------------------------
    ![image](Yang2024CSDO_figs/map50x50_title_center_bottom0.png){width="90%"}
   ![image](Yang2024CSDO_figs/map100x100_title_center_bottom0.png){width="90%"}
  --------------------------------------------------------------------
:::

::: caption
Simulation results on random maps. The solid line represents obstructed scenarios, and the dotted line represents obstacle-free scenarios.
:::
:::::

::: table*
:::

The performance of CSDO is evaluated through a comparative analysis with various MVTP algorithms, focusing on success rate, runtime, and solution quality (makespan). A general time limit of 20 s is applied, except for Fast-ASCO, which is allowed 200 s due to Matlab implementation. Figure [8](#fig:map100){reference-type="ref" reference="fig:map100"} presents the results for both map types, while Table [\[tab:result\]](#tab:result){reference-type="ref" reference="tab:result"} displays results for a map size of 50 m $\times$ 50 m.

Seq-CL-CBS (SCC) [@wen_cl-mapf_2022] is a grid search-based method and a prioritized planning version of the optimal MVTP method, CL-CBS, for large-scale problems. CL-CBS, leveraging the optimal MAPF algorithm Conflict based Search (CBS), forms the basis for SCC, which organizes agents into several groups for sequential planning with CL-CBS; each subsequent group views the prior as dynamic obstacles.

Prioritized Planning (PP) is a grid search-based prioritized planning method. It randomly assigns each agent an order and plans their trajectories sequentially based on this order. In theory, PP is not a complete or optimal method and may perform poorly if an inappropriate order is chosen.

Fast ASCO [@ouyang_fast_2022], an advanced ASCO variant [@li_optimal_2021], excels in constraint reduction, offering an optimal solution despite the high runtime. In addition, it optimizes for both travel time and comfort, and has a detailed kinematics model.

In our simulation, CSDO achieves the best success rate and runtime in general, whether on random maps or room-like maps, benefiting from PBS's efficiency and its hierarchical framework. Though SCC enhances scalability through sequential planning, its computation time still increases exponentially with large-scale problems due to CBS; PP scales better than SCC, and the solution quality does not deteriorate significantly. However, compared to CSDO, PP exhibits poorer performance in terms of success rate and runtime. CSDO relies on PBS, which searches various partial order sets and has higher completeness. Regarding solution quality, PP may outperform CSDO, as CSDO prioritizes success rate over makespan optimization; As an optimal algorithm, Fast ASCO achieves superior success rates in large scale, outperforming near-optimal methods like SCC for groups of 20 and 25 agents in a 50 m square map. It achieves a longer makespan due to the optimization for comfort and the detailed kinematics model.

## Ablation Study and Limitation Analysis

:::::: adjustbox
max width=0.47, center

::::: threeparttable
::: {#tab:scale}
  \# Agents                         30       50       70       90
  --------------------------------- -------- -------- -------- -------
  SR$^{a}$: CSDO                    96.67%   98.33%   35.00%   5.00%
  SR: CSDO w/o$^{d}$ DO$^{e}$       0        0        0        0
  SR: CSDO w/o warm start           93.33%   95.00%   11.67%   0
  FR$^{b}$: DO failure rate$^{f}$   1.66%    0        1.66%    0
  RT$^{c}$: CSDO (s)                0.63     3.42     8.99     6.62
  RT: CS w/o DO (s)                 0.49     3.24     8.74     6.43
  RT: CSDO w/o warm start (s)       1.53     9.78     14.72    \-

  : Ablation Study on 100m $\times$ 100m random map
:::

::: tablenotes
SR: Success Rate;

FR: Failure Rate;

RT: Runtime;

w/o: without;

CSDO w/o DO: Only use centralized search. The success rate means the initial guess has no collision and can be seem as a feasible solution;

DO failure rate: the percentage of cases where decentralized optimization fails to find one feasible solution despite a successful initial guess from centralized searching;
:::
:::::
::::::

Ablation experiments are conducted to validate the effectiveness of Decentralized Optimization (DO) and a warm start. Without DO, nearly all initial guesses exhibit minor collisions and are deemed infeasible. The runtime of centralized searching dominates within CSDO. Furthermore, the DO failure rate is less than 2%, indicating that the primary completeness loss in CSDO is attributed to PBS. Thus, the necessity, speed, and effectiveness of DO are validated. The warm start technique contributes to varying degrees of improvement in both success rate and runtime metrics.

In summary, regarding limitations, the PBS can be P-complete and can be modified to be P-optimal. For the DO, the completeness drop is less than 2% in simulations.

## Experimental Setup and Results

:::: {#fig:fieldtest .figure latex-placement="htpb"}
  ------- -------
          
   \(a\)   \(b\)
  ------- -------

::: caption
Real world experiments and results on 15 m square map. (a) Experiment platform. (b) The vehicle real trajectories, CSDO planned trajectories and the optimal trajectories planned by CL-CBS on 15 m map.
:::
::::

[]{#tab:field label="tab:field"}

::: {#tab:field}
+--------+----------------------------------------------------+----------------------------------------------------+
| Method | 15 m $\times$ 15 m map                             | 20 m $\times$ 20 m map                             |
+:======:+:========================:+:=======================:+:========================:+:=======================:+
| 2-5    | $\tau_f$ (s)$\downarrow$ | Runtime (s)$\downarrow$ | $\tau_f$ (s)$\downarrow$ | Runtime (s)$\downarrow$ |
+--------+--------------------------+-------------------------+--------------------------+-------------------------+
| CL-CBS | **17.4**                 | 10.075                  | **15.5**                 | 0.332                   |
+--------+--------------------------+-------------------------+--------------------------+-------------------------+
| CSDO   | 20.3                     | **0.623**               | 16.8                     | **0.014**               |
+--------+--------------------------+-------------------------+--------------------------+-------------------------+

:  Real-world experiment results
:::

Experiments are conducted with 3 forward-only 1.9 m $\times$ 1.3 m vehicles in 15 m and 20 m square areas. The vehicles are positioned using differential GNSS. The map is pre-set and known. The trajectories are calculated on a typical laptop and then transmitted to the agents via WiFi. The trajectory tracking controller operates at 10 Hz, utilizing longitudinal PID control and lateral Pure Pursuit. One scenario and results are shown in Fig. [9](#fig:fieldtest){reference-type="ref" reference="fig:fieldtest"}. As in Table [2](#tab:field){reference-type="ref" reference="tab:field"}, CSDO achieves similar solution quality while the runtime is greatly reduced.

# Conclusion

This work introduces CSDO, an efficient algorithm for large-scale multi-vehicle trajectory planning, leveraging a combination of centralized priority-based searching and decentralized optimization. Through an extensive set of experiments, we demonstrate that CSDO efficiently discovers solutions within a limited time compared to other methods, without significant loss in solution quality, especially in large-scale, high-density scenarios. In the future, we will try to strike a better balance between solution quality and runtime with SOTA MAPF algorithms, generate robust solutions allowing for tracking errors, and extend our algorithm with dynamic and intensive traffic participants.

::: thebibliography
10

B. Li, *et al.*, "Optimal Cooperative Maneuver Planning for Multiple Nonholonomic Robots in a Tiny Environment via Adaptive-Scaling Constrained Optimization," *IEEE Robot. Autom. Lett.*, vol. 6, no. 2, pp. 1511--1518, 2021.

H. Huang, *et al.*, "General optimal trajectory planning: Enabling autonomous vehicles with the principle of least action," *Engineering*, 2023.

L. Wen, *et al.*, "CL-MAPF: Multi-Agent Path Finding for Car-Like robots with kinematic and spatiotemporal constraints," *Robotics and Autonomous Systems*, vol. 150, p. 103997, 2022.

J. Li, *et al.*, "Efficient Trajectory Planning for Multiple Non-Holonomic Mobile Robots via Prioritized Trajectory Optimization," *IEEE Robot. Autom. Lett.*, vol. 6, no. 2, pp. 405--412, 2021.

J. Park, *et al.*, "Homotopy-based divide-and-conquer strategy for optimal trajectory planning via mixed-integer programming," *IEEE Trans. on Robot.*, vol. 31, no. 5, pp. 1101--1115, 2015.

B. Li, *et al.*, "Centralized and optimal motion planning for large-scale AGV systems: A generic approach," *Adv. Eng. Softw.*, vol. 106, pp. 33--46, 2017.

C. Ma, *et al.*, "Decentralized Planning for Car-Like Robotic Swarm in Cluttered Environments," in *IROS. IEEE*, 2023, pp. 9293--9300.

C. E. Luis, *et al.*, "Online Trajectory Generation With Distributed Model Predictive Control for Multi-Robot Motion Planning," *IEEE Robot. Autom. Lett.*, vol. 5, no. 2, pp. 604--611, 2020.

J. Alonso-Mora, *et al.*, "Cooperative Collision Avoidance for Nonholonomic Robots," *IEEE Trans. on Robot.*, vol. 34, no. 2, pp. 404--420, 2018.

L. Ferranti, *et al.*, "Distributed Nonlinear Trajectory Optimization for Multi-Robot Motion Planning," *IEEE Trans. Control Syst. Technol.*, vol. 31, no. 2, pp. 809--824, 2023.

F. Rey, *et al.*, "Fully Decentralized ADMM for Coordination and Collision Avoidance," in *ECC. IEEE*, pp. 825--830, 2018.

K. Solovey, *et al.*, "Finding a needle in an exponential haystack: Discrete RRT for exploration of implicit roadmaps in multi-robot motion planning," *Intl. J. Robot. Res.*, vol. 35, no. 5, pp. 501--513, 2016.

A. Lukyanenko and D. Soudbakhsh, "Probabilistic motion planning for non-Euclidean and multi-vehicle problems," *Rob. Auton. Syst.*, vol. 168, p. 104487, 2023.

R. Shome, *et al.*, "dRRT\*: Scalable and informed asymptotically-optimal multi-robot motion planning," *Auton. Robot.*, vol. 44, no. 3, pp. 443--467.

Y. Ouyang, *et al.*, "Fast and Optimal Trajectory Planning for Multiple Vehicles in a Nonconvex and Cluttered Environment: Benchmarks, Methodology, and Experiments," in *ICRA. IEEE*, 2022, pp. 10 746--10 752.

Y. Chen, *et al.*, "Decoupled multiagent path planning via incremental sequential convex programming," in *ICRA. IEEE*, 2015, pp. 5954--5961.

W. Hönig, *et al.*, "Trajectory Planning for Quadrotor Swarms," *IEEE Trans. on Robot.*, vol. 34, no. 4, pp. 856--869, 2018.

J. Park, *et al.*, "Efficient Multi-Agent Trajectory Planning with Feasibility Guarantee using Relative Bernstein Polynomial," in *ICRA. IEEE*, 2020, pp. 434--440.

G. Shi, *et al.*, "Neural-swarm2: Planning and control of heterogeneous multirotor swarms using learned interactions," *IEEE Trans. on Robot.*, vol. 38, no. 2, pp. 1063--1079, 2021.

H. Ma, *et al.*, "Searching with Consistent Prioritization for Multi-Agent Path Finding," *AAAI*, vol. 33, no. 01, pp. 7643--7650, 2019.

K. Okumura, *et al.*, "Priority inheritance with backtracking for iterative multi-agent path finding," *Artif. Intell.*, vol. 310, p. 103752, 2022.

D. Dolgov, *et al.*, "Path Planning for Autonomous Vehicles in Unknown Semi-structured Environments," *Intl. J. Robot. Res.*, vol. 29, no. 5, pp. 485--501, 2010.

J. Li, *et al.*, "Intersection Coordination with Priority-Based Search for Autonomous Vehicles," *AAAI*, vol. 37, no. 10, pp. 11 578--11 585, 2023.

Y. Yang, *et al.*, "Attention-based Priority Learning for Limited Time Multi-Agent Path Finding," in *AAMAS*, 2024, pp. 1993--2001.

J. Park and H. J. Kim, "Online Trajectory Planning for Multiple Quadrotors in Dynamic Environments Using Relative Safe Flight Corridor," *IEEE Robot. Autom. Lett.*, vol. 6, no. 2, pp. 659--666, 2021.

B. Li, *et al.*, "Optimization-Based Trajectory Planning for Autonomous Parking With Irregularly Placed Obstacles: A Lightweight Iterative Framework," *IEEE Trans. on Intell. Transp. Syst.*, vol. 23, no. 8, pp. 11 970--11 981, 2022.
:::

[^1]: Manuscript received: March, 18, 2024; Revised June, 29, 2024; Accepted July, 26, 2024.

[^2]: This paper was recommended for publication by Editor M. Ani Hsieh upon evaluation of the Associate Editor and Reviewers' comments. This work was supported in part by NSFC (52221005) and the Key Project (52131201). *(Corresponding author: Heye Huang.)*

[^3]: $^{1}$Y. Yang, J. Jiang, S. Xu, J. Wang and H. Huang are with the School of Vehicle and Mobility, Tsinghua University, Beijing 100084, China. (email: yyb19,hhy18,jiangjk21\@mails.tsinghua.edu.cn; shaobxu, wjqlws\@tsinghua.edu.cn).

[^4]: $^{2}$X. Yan is with the Department of Civil and Environmental Engineering, University of Michigan, Ann Arbor, MI 48109 USA. (email: xintaoy@umich.edu)

[^5]: Digital Object Identifier (DOI): see top of this page.
