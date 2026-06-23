---
citation_key: Nawaz2025Graphbased
arxiv_id: 2504.12616
arxiv_url: https://arxiv.org/abs/2504.12616
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:12:48Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

(Semi)autonomous parking addresses the growing demand for efficient and safe vehicle maneuvering in constrained environments [@valet_pappas; @urban_autonomous]. Urbanization and increased vehicle traffic have resulted in congested parking lots, necessitating precise, collision-free navigation. This task is further complicated by the presence of dynamic obstacles [@dynamic_parking], such as pedestrians and moving vehicles, in addition to static obstacles [@static_parking], including parked vehicles and structural elements. A functional planning module for autonomous parking must account for these complexities while ensuring safety, reliability, and computational efficiency.

:::: {#fig:intro .figure latex-placement="!t"}
![](Nawaz2025Graphbased_figs/intro_scenario.png){width="85%"}

::: caption
A parallel parking scenario with static cars (black), pedestrians, and a moving car (red). The brown car is the ego vehicle. The more transparent images of the red car and the pedestrian denote their respective predictions.
:::
::::

Consider the scenario in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"}, where the brown ego vehicle is trying to park in the spot between the two black vehicles. Meanwhile, a red car in the adjacent lane is overtaking the ego vehicle, and a pedestrian is walking across the empty parking spot to get on the sidewalk. The more transparent images denoted the predictions of the pedestrian and the red car. Path planning techniques in such scenarios must effectively model and avoid both static and dynamic obstacles, generate precise maneuvers for navigating tight spaces, and ensure computational efficiency to react swiftly in dynamic environments. The complexity is primarily attributed to the non-convex geometry of the obstacle-free space, in addition to the non-linear and non-holonomic nature of vehicle dynamics [@rajamani2011vehicle], which impose strict motion constraints during the planning process. Furthermore, it has been formally established that identifying a collision-free path in such scenarios is, in general, an NP-hard problem [@NP_hard], underscoring the computational intractability of this task. Thus, the current research gap is to generate path that simultaneously ensure (i) real-time efficiency, (ii) kinematic feasibility, and (iii) safety in the presence of both static and dynamic obstacles. To address these problems, *we develop a computationally efficient planning strategy that generates safe and reliable paths for autonomous parking maneuvers by explicitly accounting for the motion of dynamic obstacles in our graph-based search algorithm.* We summarize our contributions below.

**Contributions:** We propose a novel *time-indexed variant* of the conventional Hybrid A$^\star$ algorithm that explicitly uses the *motion predictions of dynamic obstacles* to generate collision-free paths. Then, we present a strategy for path planning in larger parking lots that utilizes the *time-indexed* Hybrid A$^\star$ algorithm as a sub-routine to compute local paths at each planning step by choosing an adaptive intermediate goal based on look-ahead point from the current state. We exploit the static map information and incorporate the vanilla A\* cost as a heuristic to guide the ego vehicle towards the goal, resulting in improved computational performance and dynamically feasible paths.

We demonstrate through simulations in diverse parking scenarios that our method is computationally efficient compared to the state of the art spline-based approach while generating safer and smoother paths. The simulation videos are available at <https://sites.google.com/view/t-ha-star/home>.

# RELATED WORK

Path planning approaches for autonomous vehicles typically fall into three categories: search-based, optimization-based, and learning-based methods. Search-based techniques, such as A$^\star$[@a_star_orig] and its variants [@a_star_2], generate coarse obstacle-free paths, which serve as a guide for a low-level trajectory planner. Optimization-based methods incorporate detailed vehicle dynamics, optimizing trajectories for precision, comfort, and safety, but often result in computationally expensive and nonlinear NP-hard problems. Learning-based methods typically employ black-box models that map sensor inputs (e.g., camera or LiDAR data) to control actions or intermediate trajectories, often lacking interpretability.

### Graph search-based methods

Algorithms such as conventional A$^\star$ [@lavalle2006planning] work only for holonomic robots since the motion primitives are linear (horizontal, vertical, diagonal). Rapidly-exploring Random Trees (RRT) [@rrt_orig] and its variants [@rrt_inf; @rrt_lqr] are a set of search techniques that randomly sample points within the grid-world and connect them to the tree used for planning. While such stochastic methods have greater potential to not get stuck at local optimum, they often produce paths with sharp curvature, making them difficult for the low-level trajectory follower to track. Hybrid A$^\star$ [@hybrid_A_star] is a search algorithm that improves upon normal A$^\star$ for non-holonomic robots. In Hybrid A$^\star$, motion between nodes follow the bicycle dynamics [@rajamani2011vehicle] with a given time discretization and a fixed set of motion primitives based on speed, gear, and steering angle. Therefore, the path generated by Hybrid A$^\star$ is dynamically feasible and makes it easier for the low-level trajectory planner to track. Our work builds upon conventional Hybrid A$^\star$ and extends it to avoid dynamic obstacles using their motion predictions.

### Optimization-based methods

Advances in computational power and numerical optimization have popularized optimization-based planning methods such as Model Predictive Control [@MPC]. However, obstacle avoidance often results in non-convex problems [@static_parking; @time_optimal_MPC; @rcms], sometimes requiring integer variables [@mixed_integer_ad; @slas], making real-time implementation challenging. Prior work [@OBCA; @OBCA_dynamic_park] use dual variables [@boyd2004convex] to smoothen constraints, enabling gradient and Hessian-based solvers. Other approaches [@rapid_it; @recurr_spline] leverage differential flatness [@diff_flat] of the kinematic bicycle model [@rajamani2011vehicle] to generate spline-based trajectories, but still face computational complexity due to iterative optimization and curvature constraints. Hybrid methods [@hybrid1; @hybrid2] combine search and optimization to handle dynamic obstacles, but are not validated in tightly constrained environments such as parking lots. A time-dependent Hybrid A star algorithm was also proposed in [@time_hybrid_A], which, unlike our approach, does not exploit closed-form Reeds-Shepp path solutions, relies on a precomputed free-space representation, and employs conservative Voronoi-based collision checking. Overall, the core challenge remains the non-convexity and computational burden of optimization-based planning in dynamic settings, making real-time planning difficult.

### Learning-based methods

The rich class of deep neural network models are leveraged to learn driving policies using large data from simulations or expert demonstrations. Companies such as Tesla [@tesla_progress; @tesla_limit] and Waymo [@waymo_imit; @waymo_rl] have made significant progress in autonomous driving by using learning-based methods like deep reinforcement learning or imitation learning. The ability of deep models to handle complex, unstructured environments has been explored for parking maneuvers that utilize techniques such as supervised policy learning [@rl_expert] or hybrid methods combining learning with optimization techniques [@hope_rl]. Despite these advancements, learning-based approaches still face challenges in generalization, safety guarantees, and real-time deployment, particularly in highly constrained scenarios with dynamic obstacles [@waymo_circ].

# TECHNICAL BACKGROUND

Let $\boldsymbol{x} = (X, Y, \theta)$ be the state of the vehicle, where $(X, Y)$ is the center of the rear axis and $\theta$ is the heading angle. To model vehicle dynamics, we employ the kinematic bicycle model which is well suited for vehicle at low speeds [@rajamani2011vehicle], expressed as $$\begin{equation}
\dot{\boldsymbol{x}} = f(\boldsymbol{x}, \boldsymbol{u}) \Leftrightarrow \begin{bmatrix} \dot{X} \\ \dot{Y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix}
v \cos(\theta) \\ v \sin(\theta) \\ \frac{v}{L}\tan(\delta)
\end{bmatrix} .
    \label{dynamics}
\end{equation}$$ The control input is $\boldsymbol{u} = \begin{bmatrix}
    v \\ \delta
\end{bmatrix}$, where $v$ and $\delta$ is the longitudinal velocity and steering angle of the front wheel, respectively. The wheelbase of the vehicle is $L$. A path ${\mathcal{P}:=\boldsymbol{x}(t)}$, defined as the state trajectory ${\boldsymbol{x} : \mathbb{R}_{\geq 0} \to \mathbb{R}^3}$, is said to be *dynamically feasible* if there exists control inputs ${\boldsymbol{u}(t) \in \mathbb{R}^2}$ for all time $t \geq 0$ such that ${\boldsymbol{x}(t) = \int_0^t f(\boldsymbol{x}(s), \boldsymbol{u}(s)) ds}$ for a given initial condition $\boldsymbol{x}(0)$.

The vehicle is modeled as a rectangle, and each obstacle is modeled as a 2D Cartesian point as given in Fig. [2](#fig:vehicle){reference-type="ref" reference="fig:vehicle"}. Let $o_x$ be the distance from the edge of the vehicle to the obstacle along the vehicle's longitudinal direction, and let $o_y$ be the distance along the lateral direction. The obstacle avoidance constraint is $$\begin{equation}
\max(o_x, o_y) \geq d,
    \label{obst_avoid}
\end{equation}$$ where $d > 0$ is a safety margin that intuitively enlarges the actual size of the vehicle. Constraint [\[obst_avoid\]](#obst_avoid){reference-type="eqref" reference="obst_avoid"} precisely determines the proximity of each obstacle to the vehicle's edge, in contrast to methods that approximate obstacle distance using Euclidean distance [@CBF_circle; @park_circle]. Prior work also assume the obstacle to be either a polytope [@OBCA_dynamic_park; @OBCA] or a circle [@CBF_circle; @park_circle], but we do not assume any specific shape for the obstacle. Each point on the boundary of any arbitrary shaped obstacle can be represented as the red point in Fig. [2](#fig:vehicle){reference-type="ref" reference="fig:vehicle"}, which aligns with the raw point cloud data that we typically receive from sensors to detect obstacles [@nvidia_obst_detect; @obst_detect].

:::: {#fig:vehicle .figure latex-placement="!t"}
![](Nawaz2025Graphbased_figs/vehicle.png){width="90%"}

::: caption
Geometry of the vehicle and obstacle avoidance. The vehicle is the brown rectangle and obstacle is the red circle.
:::
::::

The boundaries of static obstacles are represented as a sequence of 2D Cartesian points ${\mathcal{B} = \{\boldsymbol{b}_i\}_{i=1}^{B}}$, where ${\boldsymbol{b}_i \in \mathbb{R}^2}$ and $B$ is the number of points used to model the static obstacles. For example, consider the scenario in Fig. [3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"}, where the ego vehicle should move from the blue state to the green state while avoiding the dynamic obstacle in red, and the static vehicles represented as black rectangles. The set $\mathcal{B}$ consists of linearly spaced points along the edges of each static vehicle, in addition to the boundaries of the drivable area. The trajectory of the $i^{\textnormal{th}}$ dynamic obstacle is given by the output of a prediction model as $\boldsymbol{y}^i(t) \in \mathbb{R}^2$ for all $i \in \{1,2,\ldots,O\}$ and time $t \geq 0$ where $O$ is the number of dynamic obstacles. In Fig. [3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"}, the dynamic obstacle moves horizontally from right to left at a constant velocity. Given the 2D Cartesian points for both the static and dynamic obstacles, the obstacle avoidance constraint is given by [\[obst_avoid\]](#obst_avoid){reference-type="eqref" reference="obst_avoid"}.

# PROBLEM STATEMENT

In this section, we formally define two problem statements to address the autonomous parking problem.

::: {#prob_1 .problem}
**Problem 1**. *Given the initial state of the ego vehicle $\boldsymbol{x}_0$ and the goal state $\boldsymbol{e}$, a map of static obstacles $\mathcal{B}$, the predictions of dynamic obstacles $\{\boldsymbol{y}^i(s)\}_{i=1}^O$ for all $s \geq 0$, find a path $\mathcal{P} := \boldsymbol{x}(s)$ such that $\boldsymbol{x}(0) = \boldsymbol{x}_0$ and $\boldsymbol{x}(s) = \boldsymbol{e}$ for all $s \geq S$ where $S \geq 0$ is some finite time, $\mathcal{P}$ is dynamically feasible, and avoids all the static and dynamic obstacles.*
:::

In Problem [1](#prob_1){reference-type="ref" reference="prob_1"}, the aim is to generate a *single path* from start to goal that avoids both the static and dynamic obstacles. Fig. [3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"} illustrates a target scenario for Problem [1](#prob_1){reference-type="ref" reference="prob_1"}.

::: {#prob_2 .problem}
**Problem 2**. *Given the initial state of the ego vehicle $\boldsymbol{x}_0$ and the global goal state $\boldsymbol{g}$, a map of static obstacles $\mathcal{B}$, the current state of ego vehicle $\boldsymbol{x}_t$ at time $t$, the predictions of dynamic obstacles $\boldsymbol{y}^i(s)$ for all $i \in \{1,2,\ldots,O\}$ and $s \geq 0$, find a local path $\mathcal{P}_t := \boldsymbol{x}^t(s)$ at each time $t$ such that ${\boldsymbol{x}^t(0) = \boldsymbol{x}_t}$, $\boldsymbol{x}^t(s) = \boldsymbol{g}$ for all $t \geq T, s \geq S$ where $S, T \geq 0$ is some finite time, $\mathcal{P}_t$ is dynamically feasible, and avoids all the static and dynamic obstacles.*
:::

In Problem [2](#prob_2){reference-type="ref" reference="prob_2"}, the aim is to generate a local path at each time step $t$ from the current state of the vehicle $\boldsymbol{x}_t$ such that the vehicle eventually reaches the goal $\boldsymbol{g}$ without colliding with the static and dynamic obstacles. We refer to Problem [2](#prob_2){reference-type="ref" reference="prob_2"} as an *online planning* problem where the vehicle should maneuver in a large parking lot as given in Fig. [4](#fig:prob_state_2){reference-type="ref" reference="fig:prob_state_2"} by planning locally at each time step. Problem [1](#prob_1){reference-type="ref" reference="prob_1"} is viewed as an *one-time planning* problem either for the final parking maneuver as given in Fig. [3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"} or to a local goal as shown in Fig. [4](#fig:prob_state_2){reference-type="ref" reference="fig:prob_state_2"}.

::: {#remark_1 .remark}
**Remark 1**. *[ In principle, for the given $\boldsymbol{x}_0$ in Problem [2](#prob_2){reference-type="ref" reference="prob_2"}, any solution that solves Problem [1](#prob_1){reference-type="ref" reference="prob_1"} with $\boldsymbol{e} = \boldsymbol{g}$ also solves Problem [2](#prob_2){reference-type="ref" reference="prob_2"} with $T = 0$. However, finding a single path $\mathcal{P}_0$ from $\boldsymbol{x}(0)$ to $\boldsymbol{g}$ in a large parking lot such as Fig. [4](#fig:prob_state_2){reference-type="ref" reference="fig:prob_state_2"} will be computationally expensive. Additionally, the vehicle typically has access only to the predicted trajectories of dynamic obstacles within its local sensing region. Predictions for obstacles located very far away or for very long time horizons are often highly uncertain. Hence, we decouple the *one-time planning* problem, and the *online planning* problem, referring to them as Problem [1](#prob_1){reference-type="ref" reference="prob_1"} and Problem [2](#prob_2){reference-type="ref" reference="prob_2"}, respectively. ]{.nodecor}*
:::

:::: {#fig:prob_state_1 .figure latex-placement="!b"}
![](Nawaz2025Graphbased_figs/problem_state.png){width="40%"}

::: caption
Target scenario for Problem [1](#prob_1){reference-type="ref" reference="prob_1"}. The black rectangles are static vehicles, and the dynamic obstacle moves from right to left.
:::
::::

:::: {#fig:prob_state_2 .figure latex-placement="!b"}
![](Nawaz2025Graphbased_figs/prob_state_2.png){width="49%"}

::: caption
Target scenario for Problem [2](#prob_2){reference-type="ref" reference="prob_2"} with four dynamic obstacles where the local path of an intermediate time step is shown. The light brown rectangles denote the trajectory of the ego vehicle, and the black arrows denote the motion of dynamic obstacles.
:::
::::

# TIME-INDEXED HYBRID A STAR

In this section, we propose Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} that aims to solve Problem [1](#prob_1){reference-type="ref" reference="prob_1"}. Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} is a variant of the conventional Hybrid A$^\star$ algorithm [@hybrid_A_star] where we index each node in the search procedure by time $t$ in addition to the state $\boldsymbol{x}$ of the vehicle. The additional time dimension allows us to account for the behavior of dynamic obstacles and subsequently check for collision during the search procedure. The details of Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} are given as follows.

::: algorithm
**Input**: $\boldsymbol{x}_0, \boldsymbol{e}, \mathcal{B}, \boldsymbol{y}^i(s)$ for all $i \in \{1,2,\ldots,O\}$ and $s \geq 0$, maximum iteration $I_m$ **Output**: Path $\mathcal{P}$ from $\boldsymbol{x}_0$ to $\boldsymbol{e}$ **Initialize:** Start node $\boldsymbol{N}$, Goal node $\boldsymbol{e_N}$, iteration $j = 0, \mathcal{P} \gets [\boldsymbol{x}_0]$ [ClosedSet]{.smallcaps} = $\{\}$, [CostQueue]{.smallcaps}$[\boldsymbol{N} ] = \boldsymbol{N}.c_g + \boldsymbol{N}.c_h$
:::

::: {#defn:node .definition}
**Definition 1**. *A node $\boldsymbol{N}$ is defined as an object with the following attributes.*

- *$\boldsymbol{N.x}$: state $\boldsymbol{x} = (X, Y, \theta)$ of the vehicle in node $\boldsymbol{N}$*

- *$\boldsymbol{N.}t$: time $t \geq 0$ at node $\boldsymbol{N}$*

- *$\boldsymbol{N.P}$: parent node of $\boldsymbol{N}$, where $\boldsymbol{N.P}$ is the immediate predecessor of $\boldsymbol{N}$ in the graph traversal.*

- *$\boldsymbol{N.}\tau$: state trajectory from the parent node $\boldsymbol{N.P}$ to the current node $\boldsymbol{N}$ for a time horizon $H$ where ${\boldsymbol{N.}\tau(0) = \boldsymbol{N.P.}\tau(H)}$ and ${\boldsymbol{N.}\tau(H) = \boldsymbol{x}}$.*

- *$\boldsymbol{N.}\tau_o$: trajectory of the dynamic obstacles from the parent node $\boldsymbol{N.P}$ to the current node $\boldsymbol{N}$ for a time horizon $H$ where ${\boldsymbol{N.}\tau_o(0) = \boldsymbol{N.P.}\tau_o(H)}$ and ${\boldsymbol{N.}\tau_o(H) = \{\boldsymbol{y}^i(\boldsymbol{N}.t)\}_{i=1}^O}$.*

- *$\boldsymbol{N}.c_g$: cost from the start node to node $\boldsymbol{N}$*

- *$\boldsymbol{N}.c_h$: heuristic cost from node $\boldsymbol{N}$ to the goal node.*
:::

The node $\boldsymbol{N}$ is the fundamental entity in Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} that enables us to plan a collision-free path. It serves the same purpose as a typical node in graph-based planning algorithms [@hybrid_A_star; @survey_path_plan], but we have an additonal time dimension $\boldsymbol{N.}t$ and the predictions of dynamic obstacles $\boldsymbol{N.}\tau_o$. Definition [1](#defn:node){reference-type="ref" reference="defn:node"} describes that the state of the vehicle at node $\boldsymbol{N}$ is $\boldsymbol{N.x}$ at time $\boldsymbol{N.}t$. The vehicle's trajectory to reach $\boldsymbol{N.x}$ from its parent node $\boldsymbol{N.P}$ is $\boldsymbol{N}.\tau$ and the corresponding trajectory of dynamic obstacles is $\boldsymbol{N.}\tau_o$.

**Description of Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"}**: We initialize a [closedset]{.smallcaps} that contains all the explored nodes and a [costqueue]{.smallcaps} that stores the nodes to be explored sorted by the cost function $\boldsymbol{N}.c_g + \boldsymbol{N}.c_h$. In line 8, we "pop\" node $\boldsymbol{N}$ from the [costqueue]{.smallcaps} that has the least cost. If we are "close" to the goal as measured using the heuristic cost $\boldsymbol{N}.c_h$ in line 14, we check if there is a direct obstacle free path to the goal using **Reeds-Shepp** paths [@reeds_shepp]. If there is no such path, we explore the neighbors of the current node and add it to the [costqueue]{.smallcaps} as given in lines 22-24. We repeat the procedure until we reach the goal, or if the iteration $j$ to explore nodes has reached $I_m$. Once we reach the goal, we **backtrack** the path by retracing the nodes from the goal to the start by following the parent nodes stored during the search. The maximum iteration $I_m$ sets an upper limit on the computation time allocated for searching a path. If $j=I_m$, the path $\mathcal{P}$ defaults to keeping the vehicle stationary as initialized in line 3. This will be further clarified in Section [6](#sec:global){reference-type="ref" reference="sec:global"}.

## Neighbors

In lines 21-23 of Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"}, we explore neighboring nodes from the current node $\boldsymbol{N}$ to find a path to the goal. The bicycle model [\[dynamics\]](#dynamics){reference-type="eqref" reference="dynamics"} is used to generate the neighbors with a discrete set of velocity inputs $v \in [-v_{\textrm{max}}, v_{\textrm{max}}]$ and steering inputs $\delta \in [-\delta_{\textrm{max}}, \delta_{\textrm{max}}]$. A neighbor $\boldsymbol{N'}$ to the current node $\boldsymbol{N}$ for an input $\boldsymbol{u} =\begin{bmatrix}
    v \\ \delta
\end{bmatrix}$ and time horizon $H$ is obtained as follows. $$\begin{equation}
\begin{aligned}
\boldsymbol{N'}.\tau(r) &= \int_{0}^r f(\boldsymbol{x}(s), \boldsymbol{u}) dt \ \forall \ r \in [0, H], \boldsymbol{x}(0) = \boldsymbol{N.x} \\
\boldsymbol{N'}.\tau_o(r) &= \{\boldsymbol{y}^i(\boldsymbol{N}.t +r)\}_{i=1}^O \ \forall \ r\in[0, H] , \\
\boldsymbol{N'.x} &= \boldsymbol{N'}.\tau(H), \ \boldsymbol{N'}.t = \boldsymbol{N}.t + H, \ \boldsymbol{N'.P} = \boldsymbol{N}.   
\end{aligned}
    \label{neighbor_node}
\end{equation}$$ A neighboring node $\boldsymbol{N'}$ is valid if and only if the state trajectory $\boldsymbol{N'}.\tau$ does not collide with the dynamic obstacles' trajectory $\boldsymbol{N'}.\tau_o$ and the static obstacles $\mathcal{B}$. In practice, we discretize the trajectories and the roll out of dynamics in [\[neighbor_node\]](#neighbor_node){reference-type="eqref" reference="neighbor_node"} at times $\{r_1,  r_2,\ldots, r_K\}$ where $r_1 = 0$ and $r_K = H$. Collision with dynamic obstacles is checked for each $k\in\{1,2,\ldots,K\}$ by evaluating the pair of points $\left(\boldsymbol{N'}.\tau(r_k), \boldsymbol{N'}.\tau_o(r_k\right)$ using [\[obst_avoid\]](#obst_avoid){reference-type="eqref" reference="obst_avoid"}.

## Reeds-Shepp

If the current node $\boldsymbol{N}$ is "close\" to the goal, we check if there exists a continuous obstacle free path to the goal. The current node is"close\" to the goal if the heuristic cost function $\boldsymbol{N}.c_h$ is less than a threshold $h_{\textnormal{thresh}}$. We compute all possible Reeds-Sheep paths [@reeds_shepp] from the current state $\boldsymbol{N.x}$ to the goal state $\boldsymbol{e}$. A Reeds-Shepp path is the optimal path between two states for a vehicle with bicycle dynamics [\[dynamics\]](#dynamics){reference-type="eqref" reference="dynamics"} that moves only forward ${(v = v_{\textnormal{max}})}$ or backward ${(v = -v_{\textnormal{max}})}$ with extreme steering inputs ${\delta \in \{-\delta_{\textrm{max}}, \delta_{\textrm{max}}\}}$. The obstacle free Reeds-Shepp Paths $\mathcal{R}$ are sorted as per the user-defined cost $c_g$ and the path with the least cost is chosen to move from the current state to the goal state.

## Cost

The node $\boldsymbol{N}$ in line 8 has the least cost $\boldsymbol{N}.c_g + \boldsymbol{N}.c_h$ amongst all the nodes in [costqueue]{.smallcaps}. The cost function $\boldsymbol{N}.c_g$ penalizes path length, steering angle, reverse motion and change in direction of motion and steering between subsequent nodes. The heuristic cost $\boldsymbol{N}.c_h$ guides the search direction towards the goal using an under-estimate of the actual cost to the goal $\boldsymbol{e_N}.g$. We use the solution of the $A^\star$ algorithm [@a_star_orig] for the heuristic cost which computes the shortest paths from each discrete point in a grid-world environment to the goal without using bicycle dynamics. We pre-compute the $A^\star$ costs using only the static obstacles, since dynamic obstacle avoidance is handled by our time-indexed Hybrid A$^\star$ algorithm.

As described in Remark [1](#remark_1){reference-type="ref" reference="remark_1"}, computing a single path from start to the global goal for a scenario such as Fig. [4](#fig:prob_state_2){reference-type="ref" reference="fig:prob_state_2"} will not be feasible and practical. In the next section, we present an online planning strategy for parking in larger lots.

# ONLINE PLANNER {#sec:global}

In this section, we propose Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"} that aims to solve Problem [2](#prob_2){reference-type="ref" reference="prob_2"}, where we find a local path $\mathcal{P}_t$ at each online planning step $t$ that moves the vehicle towards the goal while avoiding dynamic obstacles.

We first initialize a global path $\mathcal{G}$ from $\boldsymbol{x}_0$ to $\boldsymbol{g}$ using conventional Hybrid A$^\star$ [@hybrid_A_star] that avoids the static obstacles. Then, at each online planning step $t$, given the current state $\boldsymbol{x}_t$ and the predictions of dynamic obstacles $\boldsymbol{y}^i(s)$ for all ${i\in\{1,2,\ldots,O\}}$ and $s \geq 0$, we compute a local path $\mathcal{P}_t$ that follows the global path $\mathcal{G}$ while avoiding dynamic obstacles. We utilize Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} as a sub-routine in Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"} to plan the local path. The key idea in Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"} is to choose an appropriate intermediate goal $\boldsymbol{e}$ for Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} to return a feasible local path $\mathcal{P}_t$.

::: algorithm
**Given**: $\boldsymbol{x}_0, \boldsymbol{g}, \mathcal{B}$, maximum look-ahead=$N_m$, maximum iteration =$I_m$ **Initialize:** $\mathcal{G} \gets$ global path from $\boldsymbol{x}_0$ to $\boldsymbol{g}$ using vanilla Hybrid A$^\star$ that avoids $\mathcal{B}$ **Input**: $\boldsymbol{x}_t, \boldsymbol{y}^i(s)$ for all $i \in \{1,2,\ldots,O\}$ **Output**: Local path $\mathcal{P}_t$ **Initialize:** $\mathcal{P}_t \gets [\boldsymbol{x}_t]$ $i_c \gets \textrm{argmin}_{i \in \{1,2,\ldots,|\mathcal{G}|\}} \|\boldsymbol{x}_t - \mathcal{G}[i]\|$ $i_g \gets i_c + N_m$ $\boldsymbol{e} \gets \mathcal{G}[i_g]$ $\mathcal{P}_t \gets$ [Algorithm1](#alg_1)$\left(\boldsymbol{x}_t,\boldsymbol{e}, \mathcal{B}, \{\boldsymbol{y}^i(s)\}_{i=1}^O, I_m\right)$ $i_g \gets i_g - 1$
:::

**Choosing intermediate goal**: At the current planning step, we find the closest point on the global path $\mathcal{G}$ to the current state $\boldsymbol{x}_t$. Then, we initialize the intermediate goal using a look-ahead $N_m$ from the closest point on $\mathcal{G}$. In line 10, we try to compute a path from $\boldsymbol{x}_t$ to the intermediate goal $\boldsymbol{e}$ that avoids all the obstacles within a finite time, which is directly proportional to the runtime of Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"}. Instead of the actual runtime, we use the maximum iteration $I_m$ of Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} as the stopping criteria. If Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} does not find a path within iteration $I_m$, then we adapt the intermediate goal to be one index closer to $\boldsymbol{x}_t$ along $\mathcal{G}$ and run Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} again. We repeatedly adapt the intermediate goal as given in lines $9-11$ until we find a path $\mathcal{P}_t$. If the intermediate goal is the closest point on $\mathcal{G}$ to $\boldsymbol{x}_t$, we return the local path to be $[\boldsymbol{x}_t]$ as initialized in line 5 of Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"}, which commands the vehicle to stay stationary. This intuitively explains that if the planner cannot find a feasible local path that follows the global path within a reasonable time, the vehicle stays stationary.

# EXPERIMENTS

We evaluate our proposed Algorithms on a set of common parking scenarios, assuming that the perception system provides real-time information on static vehicles, curb boundaries, and dynamic pedestrians within the system's perception range. The task for the ego vehicle is to navigate from the initial position to a goal state while avoiding collisions. The vehicle dynamics are described by the kinematic bicycle model [\[dynamics\]](#dynamics){reference-type="eqref" reference="dynamics"} discretized with a time step of $0.1$ s for our simulations. The vehicle parameters are given in Table [\[table:veh_params\]](#table:veh_params){reference-type="ref" reference="table:veh_params"}. We use Honda Odyssey [@honda_od] as a reference to set the dimensions of the vehicle. We use $1$ m/s as the velocity limit in our Algorithms to encourage caution, but will increase this limit in our future work. All simulations are performed in Python 3.8 on Ubuntu 20.04 with Intel Xeon E5-2643 v4 CPU.

Our time-indexed Hybrid A$^\star$ implementation uses a state grid size of 2 m in both $X$ and $Y$ directions, and $20$ deg in the heading angle. The steering input is discretized using 5 points in $[-\delta_{\textrm{max}}, \delta_{\textrm{max}}]$ and velocity is discretized using 3 points in $[-v_{\textrm{max}}, v_{\textrm{max}}]$. The length of each parking space is $6.5$ m, and the width is $3.5$ m as referred from  [@park_dim]. The inclination angle with respect to the driving direction is $70$ deg for angle parking. Each static vehicle is modeled as a rectangle with length and width given in Table [\[table:veh_params\]](#table:veh_params){reference-type="ref" reference="table:veh_params"}, and each dynamic obstacle is modeled as a circle of radius $0.5$ m. Collision is checked using the geometry of the vehicle in Fig. [2](#fig:vehicle){reference-type="ref" reference="fig:vehicle"} with a safety threshold of $d = 0.5$ m.

::: tabular
\|\|P1.2 cm\|P2.1cm\|P1.2cm\|\| **Parameter** & **Description** & **Value**\
$L$ & Wheelbase length & 3  m\
$V_L$ & Vehicle length & 5  m\
$V_W$ & Vehicle width & 2  m\
$v_{\textnormal{max}}$ & Velocity limit & 1  m s$^{-1}$\
$\delta_{\textnormal{max}}$ & Steering limit & 40  deg\
:::

[]{#table:veh_params label="table:veh_params"}

:::: {#fig:spline_ours .figure latex-placement="!b"}
![](Nawaz2025Graphbased_figs/ours_spline.png){width="\\textwidth"}

::: caption
Comparison of paths generated by our time-indexed Hybrid A\* method (t-HA\* + A\*) and the iterative spline-based method (ItCA).
:::
::::

:::: {#fig:snaps_stop_go .figure latex-placement="!b"}
![](Nawaz2025Graphbased_figs/snaps.png){width="\\textwidth"}

::: caption
Illustration of the ego vehicle's stationary behaviors at different time steps $s$ in the paths generated by Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} (t-HA\* + A\*).
:::
::::

## One-time Planning {#sec:exp_local}

We validate Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} with $I_m=500$ for the following parking scenarios as given in Fig. [5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"}: perpendicular head-in, perpendicular reverse-in, angle head-in and parallel. In all the cases presented in this work, the ego vehicle parks in confined spaces with defined outer boundaries in the presence of other parked vehicles and dynamic obstacles. We compare Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} --- the time-indexed Hybrid A\* (**t-HA\***) --- with the state of the art iterative spline-based collision avoidance method [@rapid_it] (ItCA). The work in [@rapid_it] iteratively refines $5^{\textrm{th}}$-order spline trajectories to track a reference path (e.g., Hybrid A\* avoiding static obstacles). If collisions with (possibly dynamic) obstacles occur, the tracking cost is relaxed at collision points in each iteration, until the path is collision-free, or a maximum iteration count is reached.

In Fig. [5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"}, we qualitatively compare the paths generated by ItCA [@rapid_it] with that of Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} using the A\* heuristic (**t-HA\* + A\***). The paths generated by

t-HA\* + A\* avoids both static and dynamic obstacles in all scenarios. The ItCA method generates collision-free paths in the absence of dynamic obstacles for all the parking scenarios presented in this work. However, in the presence of multiple dynamic obstacles, the ItCA path for reverse-in parking collides with a static obstacle, and the paths for angle and parallel parking collide with obstacles at multiple points. We rigorously test our simulation runs across different initial positions and velocities of the dynamic obstacles. The initial point of each obstacle are regularly spaced within the bounds given in Table [\[table:park_params\]](#table:park_params){reference-type="ref" reference="table:park_params"}. The bounds in Table [\[table:park_params\]](#table:park_params){reference-type="ref" reference="table:park_params"} are chosen so that the dynamic obstacles cover a sufficient area of the drivable region and are possibly on a collision course with the ego vehicle to verify if the algorithms can avoid the obstacles. We generate 100 initial points for the one obstacle in perpendicular head-in parking (Fig. [3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"}). We choose 15 points for each obstacle in perpendicular reverse-in, angled head-in, and parallel parking (Fig. [5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"}), resulting in a total of $15^2 = 225$ initial position pairs. The velocity of obstacles in the $X$ and $Y$ directions for each candidate initial point is sampled from the uniform distribution $[-0.7, 0.7]$ m/s. We run 50 tests for each set of initial points and velocities. We also evaluate two variations of t-HA\*, one with a Eucledian heuristic cost function (t-HA\* + Eucledian) and a grid-based A\* cost (**t-HA\* + A\***).

The average performance and trajectory quality metrics for the experiments, along with one standard deviation, are presented in Table [\[table:graph_results\]](#table:graph_results){reference-type="ref" reference="table:graph_results"}. The average runtime of t-HA\* + A\* is 10-100 times faster than ItCA or when using the Eucledian heuristic. Since the A\* heuristic exploits the information of static obstacles, the search procedure in Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"} explores nodes more optimally than when the Eucledian heuristic is used. The heading rate and curvature in ItCA are significantly larger than in t-HA\*, rendering the spline paths infeasible for the vehicle to follow given its velocity and steering limits (Table [\[table:veh_params\]](#table:veh_params){reference-type="ref" reference="table:veh_params"}). The curvature is computed using the formula provided in Section III-E of [@recurr_spline].

::: tabular
\|\|P2.2 cm\|P1.8cm\|P3.2 cm\|\| **Scenario** & **Initial, Goal State $[X, Y, \theta ]$** & **Initial Position of Dynamic Obstacles**\
Perpendicular head-in (Fig. [3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"}) & $[2.0, 11.5, 0]$,\
$[20.0, 5.0, -90]$ & $X_1, Y_1\sim[15, 30], [7, 17]$\
Perpendicular reverse-in (Fig. [5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"}) & $[2.0, 9.5, 0]$,\
$[16.0, 1.0, 90]$ & $X_1, Y_1\sim[12, 25], [8, 13]\newline X_2, Y_2\sim[10, 18], [5, 8]$\
Angle head-in (Fig. [5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"}) & $[2.0, 11.5, 0]$,\
$[21.0, 5.0, -70]$ & $X_1, Y_1\sim[11, 16], [5, 9], \newline X_2, Y_2\sim[16, 25], [10, 15]$\
Parallel (Fig. [5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"}) & $[4.0, 3.0, 0]$,\
$[17.0, 0.0, 0]$ & $X_1, Y_1\sim[10, 15], [1, 3], \newline X_2, Y_2\sim[20, 28], [2, 4]$\
:::

[]{#table:park_params label="table:park_params"}

In Fig. [6](#fig:snaps_stop_go){reference-type="ref" reference="fig:snaps_stop_go"}, the paths generated by t-HA\* show that the ego vehicle yields to dynamic obstacles before proceeding to the parking spot. This mirrors typical human driving behavior by pausing to assess and adapt, ensuring both safety and smooth navigation. In contrast, ItCA often produces sharp turns, leading to infeasible curvature or failure to find a collision-free path within the iteration limit. Even with an increased limit of 100 --- compared to 10 used in [@rapid_it] --- ItCA exhibits a high failure rate as given in Table. [\[table:graph_results\]](#table:graph_results){reference-type="ref" reference="table:graph_results"}, except when dynamic obstacles are positioned far from the initial reference path.

:::: {#fig:lot_15 .figure latex-placement="!b"}
![](Nawaz2025Graphbased_figs/snaps_lot_15.png){width="\\textwidth"}

::: caption
Perpendicular reverse-in parking in a large surface lot with 15 dynamic obstacles shown as different coloured circles.
:::
::::

:::: table*
::: tabular
\|\|P1.4 cm\|P1.1 cm\|P1.5 cm\|P0.8 cm\|P1.7 cm\|P1.9cm\|P1.7cm\|P1.9cm\|P1.7cm\|\| **Scenario** & **Number of dynamic obstacles** & **Method** & **Failure Rate $\downarrow$** & **Runtime**\
$\downarrow$ (s) & **Path length**\
$\downarrow$ (m) & **Distance to closest obstacle**\
$\uparrow$ (m) & **Heading rate**\
$\downarrow$ $\left(\textnormal{deg} \ \textnormal{s}^{-1}\right)$ & **Curvature**\
$\downarrow$ $\left(\textnormal{m}^{-1}\right)$\
& & ItCA & 8% & $0.823 \pm 0.144$ & $44.902 \pm   8.277$ & $2.246 \pm 0.247$ & $5.711 \pm    4.202$ & $0.118 \pm  0.098$\
& & t-HA\* + Eucledian & 0.00% & $0.448\pm 0.061$ & $43.223 \pm 6.084$& $2.314 \pm  0.261$ & $4.708 \pm  4.165$ & $0.074 \pm 0.071$\
& & **t-HA\* + A\*** & **0.00%** & **0.018 $\pm$ 0.004** & **40.578 $\pm$ 8.312** & **2.983 $\pm$ 0.476** & **3.009 $\pm$ 1.461** & **0.051 $\pm$ 0.026**\
& & ItCA & 67.6% & $1.485 \pm 0.84$ & $33.624 \pm 9.216$ & $1.538 \pm 0.182$ & $13.85 \pm  20.355$ & $1.21 \pm 9.7$\
& & t-HA\* + Eucledian & 0.00% & $9.716 \pm    0.217$ & $40.902 \pm 8.936$ & $1.592 \pm  0.435$ & $4.867 \pm 5.843$ & $0.086 \pm  0.101$\
& & **t-HA\* + A\*** & **0.00%** & **0.048** $\pm$ **0.007** & **28.967 $\pm$ 4.569** & **1.75 $\pm$ 0.347** & **4.401 $\pm$ 2.388** & **0.072 $\pm$ 0.036**\
& & ItCA & 85.7% & $4.998 \pm 0.428$ & $56.134 \pm 11.934$ & $0.616 \pm 0.241$ & $25.67 \pm  33.327$ & $0.628 \pm  2.294$\
& & t-HA\* + Eucledian & 0.00% & $4.749 \pm 0.211$ & $34.872 \pm 10.944$ & $1.374 \pm   0.385$ & $3.826 \pm 0.917$ & $0.047 \pm 0.041$\
& & **t-HA\* + A\*** & **0.00%** & **0.034 $\pm$ 0.005** & **27.08 $\pm$ 6.813** & **1.374 $\pm$ 0.065** & **2.471 $\pm$ 0.779** & **0.042 $\pm$ 0.013**\
& & ItCA & 92% & $0.781 \pm    0.309$ & $38.924 \pm   9.869$ & $0.953 \pm  0.176$ & $40.949 \pm    41.067$ & $0.852 \pm  2.463$\
& & t-HA\* + Eucledian & 0.00% & $6.077 \pm 0.432$ & **30.179 $\pm$ 7.557** & **2.045 $\pm$ 0.336** & **3.619 $\pm$ 5.514** & **0.058 $\pm$ 0.088**\
& &**t-HA\* + A\*** & **0.00%** & **0.026 $\pm$ 0.001** & $32.713 \pm 2.481$ & $1.686 \pm    0.169$ & $6.421 \pm 0.819$ & $0.106 \pm 0.014$\
& 4 & **t-HA\* + A\*** & 15% & $0.012 \pm    0.005$ & $92.368 \pm 6.829$ & $2.058 \pm 0.191$ & $3.694 \pm 0.58$ & $0.062 \pm  0.028$\
& 10 & **t-HA\* + A\*** & 30% & $0.012 \pm  0.002$ & $95.353 \pm 19.461$ & $1.912 \pm  0.159$ & $3.278 \pm  4.32$ & $0.051 \pm  0.07$\
& 15 & **t-HA\* + A\*** & 35% & $0.011 \pm  0.016$ & $76.141 \pm 11.19$ & $1.546 \pm    0.213$ & $2.804 \pm 4.314$ & $0.043 \pm  0.07$\
:::

[]{#table:graph_results label="table:graph_results"}
::::

## Online Planning {#sec:exp_global}

We validate Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"} for perpendicular reverse-in parking in a large surface lot depicting a dense traffic situation that includes multiple parked cars and dynamic obstacles as given in Fig. [7](#fig:lot_15){reference-type="ref" reference="fig:lot_15"}. We use a maximum look-ahead of $N_m = 5$ to choose an intermediate goal from the initial global path $\mathcal{G}$, and maximum iteration $I_m = 100$ as the stopping criteria in Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"}. All other vehicle parameters and parking dimensions are the same as used in Section [7.1](#sec:exp_local){reference-type="ref" reference="sec:exp_local"}. The road width that separates adjacent parking rows is $10$ m.

The trajectory of the ego vehicle navigating to a designated parking spot is illustrated in Fig. [7](#fig:lot_15){reference-type="ref" reference="fig:lot_15"} with 15 dynamic obstacles. Each local path connects the current state of the ego vehicle to an intermediate goal, selected as described in Section [6](#sec:global){reference-type="ref" reference="sec:global"}. The maximum iteration limit $I_m$ ensures that Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"} operates at a high enough frequency, enabling frequent refinement of the local path to closely track the global path while avoiding obstacles.

::: tabular
\|\|P2.2 cm\|P2.2cm\|P3 cm\|\| **Total number of dynamic obstacles** & **Split of dynamic obstacles** & **Initial Position** $X \ \textrm{m}, Y \ \textrm{m}\sim$\
& 2 & \[0, 15\], \[7 , 40\]\
& 2 & \[25, 40\], \[0, 40\]\
& 6 & \[0, 20\], \[7, 60\]\
& 4 & \[20, 40\], \[0, 60\]\
& 5 & \[0, 20\], \[7, 20\]\
& 4 & \[0, 20\], \[20, 60\]\
& 6 & \[20, 40\], \[0, 60\]\
:::

[]{#table:lot_15_params label="table:lot_15_params"}

We run experiments for three cases in the large surface lot environment, where each case corresponds to different number of dynamic obstacles: 4, 10 and 15. We conduct 20 experiments for each of the three cases, and 10 test runs for each experiment. The initial positions of the dynamic obstacles in each experiment are randomly sampled from the uniform distributions specified in Table [\[table:lot_15_params\]](#table:lot_15_params){reference-type="ref" reference="table:lot_15_params"}. Different bounds are used for different obstacle sets so that the ego vehicle encounters dense traffic situations at varying time instances. The velocity of obstacles in the $X$ and $Y$ directions for each candidate initial point is sampled from the uniform distribution $[-0.7, 0.7]$ m/s. The initial state is $(8\ \textrm{m}, 1\ \textrm{m}, 90\ \textrm{deg})$ and the goal state is $(40\ \textrm{m}, 24\ \textrm{m}, 180\ \textrm{deg})$. The performance metrics for the surface lot scenarios are also summarized in Table [\[table:graph_results\]](#table:graph_results){reference-type="ref" reference="table:graph_results"}. The relatively higher failure rate of t-HA\* + A\* in the surface lot environment is due to the absence of a feasible path caused by dense traffic conditions. In contrast, ItCA and t-HA\* + Euclidean always generate unsafe paths, even when the iteration limit is increased to 1000, corresponding to an average maximum timeout of 10 seconds. The runtime for the surface lot scenario in Fig.[7](#fig:lot_15){reference-type="ref" reference="fig:lot_15"} corresponds to Algorithm [\[alg_2\]](#alg_2){reference-type="ref" reference="alg_2"}, which computes a local path at each time step, unlike other scenarios described in Section [7.1](#sec:exp_local){reference-type="ref" reference="sec:exp_local"} that use Algorithm [\[alg_1\]](#alg_1){reference-type="ref" reference="alg_1"}. The lower run-time for Fig. [7](#fig:lot_15){reference-type="ref" reference="fig:lot_15"} is due to planning toward a nearer intermediate goal compared to the more distant goals in Figs.[3](#fig:prob_state_1){reference-type="ref" reference="fig:prob_state_1"} and[5](#fig:spline_ours){reference-type="ref" reference="fig:spline_ours"} The trajectory metrics, including path length, distance to the closest obstacle, heading rate, and curvature, for the surface lot scenario, are calculated over the entire trajectory, from the start to the final goal state, while deviating slightly from the global path to avoid obstacles.

# CONCLUSION AND FUTURE WORK

We proposed a *time-indexed* Hybrid A\* algorithm that explicitly incorporates dynamic obstacle predictions to generate safe, reliable, and smooth paths across diverse parking scenarios. This was further extended to an online planning strategy for large surface lots via an adaptive goal-selection mechanism. Simulations across multiple parking settings demonstrate improved computational efficiency, safety, and feasibility over the state-of-the-art spline-based planner.

Future work will address the assumption of perfect trajectory predictions by the current method for dynamic obstacles, which overlooks uncertainties and latencies in the planning pipeline. We also aim to relax the assumption of a known goal state by extending our approach to actively explore the parking lot and identify suitable parking spots, all while accounting for uncertainty in the behavior of other agents.

[^1]: $^{1}$Honda Research Institute (HRI), San Jose, CA 95134, USA.

[^2]: $^{2}$GRASP Lab, University of Pennsylvania, PA 19104, USA.

[^3]: $^{3}$University of Illinois at Urbana-Champaign, USA.

[^4]: $^{4}$University of California at Riverside, Riverside, CA, 92521, USA

[^5]: $^{*}$Corresponding authors: `farhadn@seas.upenn.edu` &\
    `faizan_tariq@honda-ri.com`

[^6]: All work was done when Farhad Nawaz, Minjun Sung and Darshan Gadginmath were employed by HRI.
