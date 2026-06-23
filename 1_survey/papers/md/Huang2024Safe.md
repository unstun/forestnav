---
citation_key: Huang2024Safe
arxiv_id: 2409.10647
arxiv_url: https://arxiv.org/abs/2409.10647
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:16:06Z
origin: ai+web
reviewed: false
---

# Introduction

Trajectory generation for autonomous navigation in static environments has been widely applied in various fields, including forestry, industry, and agriculture [@https://doi.org/10.1002/rob.20403; @10.1007/978-3-030-33950-0_17; @9720974]. However, the assumption of a static or nearly static environment may not always hold, especially in urban low-altitude scenarios. Previous works adhered to the static assumption and triggered replanning whenever the map was updated [@1013481; @KOENIG200493]. Despite increasing the frequency of an online replanning framework, finding a feasible trajectory remains challenging in such dynamic environments.

A straightforward method for extending motion planning algorithms from static to dynamic environments involves introducing an additional time dimension [@doi:10.1177/0278364915614386; @5152860; @topo1; @1642056]. However, this significantly expands the state space, leading to redundant map traversal and making online solutions challenging in the presence of moving obstacles. Traditional approaches mainly focus on reducing the search space by finding safe intervals in planning and searching paths as an initial guess for trajectory generation, aiming to find solutions within limited time budgets [@SIPP1; @anytimeSIPP; @lazysipp; @kinoSIPP; @8740885]. However, there is no comprehensive and fundamental method that ensures the dynamic feasibility of high-order systems while remaining efficient for onboard planning in dynamic environments.

:::: {#fig:fig_env_show .figure latex-placement="!t"}
![](Huang2024Safe_figs/fig1.png){width="0.95\\columnwidth"}

::: caption
A representative experiment of dynamic obstacle avoidance. The quadrotor plans a trajectory (purple) and navigates between static obstacles (cylinders) and moving obstacles (ground robots).
:::
::::

To address these issues, we propose a complete dynamic connected visibility graph construction method and evaluate path equivalence using the concept of *Uniform Temporal Visibility Deformation* to get multiple topological distinct initial paths. To incorporate robot dynamics into the graph construction process, we employ the double integrator model for velocity profile to approximate minimum travel durations. This ensures the lower-order dynamic feasibility of safe intervals and temporal corridors while providing sufficient flexibility for higher-order adjustments during the back-end optimization. To ensure smoothness, B-spline trajectories are then optimized within the spatial-temporal corridors generated from initial paths. The trajectory with the minimum control effort is selected. We analyze that our method is probabilistic complete and optimal given dynamic bounds. Our contributions can be summarized as follows,

- We propose a safe interval motion planning framework for dynamic environments consisting of front-end topological path searching and back-end optimization using spatial-temporal corridors.

- We introduce a dynamic connected visibility graph construction method with guarantees of second-order dynamic feasibility. We define *Uniform Temporal Visibility Deformation* (UTVD) to evaluate the spatial-temporal topological equivalence.

- We conduct extensive simulation comparisons and hardware experiments to validate the effectiveness of the proposed framework.

# Related Works

## Moving Obstacle Avoidance

Motion planning in the presence of moving obstacles introduces challenges for finding complete and efficient strategies to resolve conflicts. A two-stage planning framework, studied in [@10610207], efficiently generates high-quality trajectories by using a front-end planner to identify collision-free paths and then optimize trajectories for smoothness, feasibility, and safety. Graph-based front-end methods like Probabilistic Roadmaps (PRM) [@508439] and its variations [@1041613; @jaillet2008path; @fasttopo] generate multiple distinct initial paths to avoid potential infeasible local minima and improve overall performance. With feasible initial paths, optimization-based approaches such as Model Predictive Control [@MPC] or minimum control trajectory generation based on flatness properties [@5980409] can be effectively employed. In [@fasttopo], a relaxed formulation for homotopy equivalence was proposed as Uniform Visibility Deformation (UVD). This approach was subsequently applied in [@topo1] for practical evaluation in the context of moving obstacle avoidance. This work was further improved in [@topo2] by accommodating multiple goals in Visibility-PRM and incorporating homotopy constraints into the optimization process. However, the equivalence evaluation becomes incomplete when considering paths in different temporal domains, i.e., the start and end times of two paths are not the same. To address this, we introduce a complete criterion for spatial-temporal topological evaluation to generate initial paths for further trajectory optimizations.

## Planning with Safe Intervals

To efficiently generate a path or trajectory in non-convex static environments, [@Deits14computinglarge] proposed the use of convex decomposition for space reduction and approximation, which was further extended in [@7839930] to create safe flight corridors. To address the challenge of moving obstacle avoidance, spatial-temporal corridors [@ding2019safe] have been directly generated on semantic maps with temporal information for 2-D scenarios of autonomous driving. Refining existing 3-D static corridors in global maps to accommodate moving objects has been explored in [@9981447], enabling the online update and reconstruction of these corridors. However, these methods rely on the availability of feasible initial paths within the same fixed temporal corridors, lacking the flexibility to adapt to different temporal interval combinations.

The Safe Interval Path Planning (SIPP) algorithm [@SIPP1] proposed a complete approach that decomposes the temporal domain into intervals on grid maps to reduce the size of the search space. However, evaluating time intervals for all grids is still computationally expensive and the robot dynamics are not considered in this phase. Various SIPP-based algorithms are subsequently introduced to solve these issues [@anytimeSIPP; @lazysipp; @kinoSIPP]. However, the computation cost for setting up time intervals in 3D environments remains high. To reduce the space complexity, graph structures like Probabilistic Roadmaps (PRMs) are used to represent the environment. Temporal PRM [@TPRM] applied safe intervals to PRM, reducing the complexity by only sampling vertices in static environments, and enabling multiple queries on the roadmap. However, this approach relies on simplistic motion assumptions. It only evaluates the collision at vertices for efficiency by limiting the maximum length of edges. This requires a dense graph, and the quality of paths largely depends on the maximum edge length. Our method addresses these challenges by incorporating safe intervals of edges and low-order dynamics in the dynamic connected visibility graph, extending distinct topological paths into spatial-temporal corridors, and further optimizing the trajectories based on flatness-based dynamics to ensure feasibility and smoothness.

# Prerequisites

## Problem Formulation

We consider a quadrotor navigating a 3D environment containing static and moving obstacles. The environment is fully observed within a finite time range $T= [t_s, t_e]$. It can be expressed as $\mathbb{R}^3 = \mathcal{X}_{free}^t  \cup \mathcal{X}_{obs}^t, \forall t \in T$, where $\mathcal{X}_{free}^t$ is the free space and $\mathcal{X}_{obs}^t$ is the obstacle space at any time in $T$. The moving obstacles' trajectories are known in $T$ and have bounded dynamics. Our objective is to generate a trajectory that has minimum control cost while ensuring safety, smoothness, and dynamical feasibility from the start location to the goal region within $T$.

:::: {#fig: fig_UTVD_show .figure latex-placement="!ht"}
::: caption
In this example, red grids are occupied by moving obstacles at specific time durations, colored solid line segments represent multiple paths from start to end vertex, while red dash lines represent collisions detected, otherwise, they are black. According to the definition of UTVD, paths in red and blue belong to the same UTVD class. The path in green is in a different UTVD class.
:::
::::

## Temporal Topology Equivalence

The geometrically topological complexity of the environment can be captured by the number of homotopy or homology classes of trajectories [@Munkres1974TopologyAF; @bhattacharya2010search]. One relation is to check the visibility deformation (VD), proposed in [@jaillet2008path]. The Uniform Visibility Deformation (UVD) [@fasttopo] employs VD's subset to evaluate the equivalence in the static environment efficiently. In dynamic environments, using UVD in time-extended state space[@topo1] cannot be directly applied since trajectories (paths) are within different temporal domains, and it also may result in time resolution incompleteness. Therefore, we introduce an enhanced version of UVD, namely Uniform Temporal Visibility Deformation (UTVD), to capture trajectories in different spatial-temporal Topological classes.

::: definition
**Definition 1**. *(Uniform Temporal Visibility Deformation (UTVD)) Two trajectories $\sigma_1(s), \sigma_2(s')$, parameterized by $s \in [0, 1]$, $s' = \alpha s + \theta, \alpha \in \mathbb{R}^+, \theta \in \mathbb{R}$, and satisfying $\sigma_1(0)= \sigma_2(\theta)$, $\sigma_1(1)= \sigma_2(\alpha + \theta)$, belong to the [same uniform temporal visibility deformation]{.underline} (UTVD) class if for all s, line segment $\sigma_1(s)\sigma_2(\alpha s + \theta)$ is collision-free during $[s, \alpha s + \theta]$.*
:::

We propose an exact approach to perform collision checking for lines within specific temporal Intervals (see section IV.A). Fig. [2](#fig: fig_UTVD_show){reference-type="ref" reference="fig: fig_UTVD_show"} showcases a simple example of UTVD evaluation. There are three moving obstacles with speeds of $1m/s$ in the environment. A robot can travel along the same geometrical path at x=\[5,6\] safely with three paths in different temporal domains, the red and green paths belong to the different UTVD classes because collisions with obstacle a and obstacle b are detected in the grids (x=\[5,6\], y=\[2,3\]) and (x=\[5,6\], y=\[1,2\]) within temporal interval t=\[2,3\], respectively. UTVD can help us evaluate the paths within different safe intervals.

## Safe Intervals and Temporal Corridors

Two vertices can be connected by an edge in a graph. The quadrotor can travel along the edge, where the minimum travel duration $t_{min}$ can be practically computed using a trapezoidal velocity profile. Here we assume the quadrotor travels on edges with rest start and end states and approximate the duration accordingly to provide a lower bound of traveling time, which is practical to provide a feasible heuristic for higher-order systems [@7839930]. We now introduce the definition of safe interval for edge as

::: {#def: safeinterval .definition}
**Definition 2**. *(Safe Intervals for Edge) For an edge $e$ in the time range $T$, The Collision intervals ${\rm CI(e)}$ is defined as a series of time intervals $\bigcup_i (t_i, t_{i+1})$, where $e \cap \mathcal{X}_{obs}^{t} \neq \emptyset$ for $\forall t \in {\rm CI}$. Subsequently, the Safe intervals ${\rm SI(e)}$ are a series of time intervals $\bigcup_j (t_j, t_{j+1})$ that satisfy $(t_j, t_{j+1}) \in T \backslash {\rm CI}(e) \cap (t_{j+1} - t_{j} > t_{min})$.*
:::

Note that safe intervals for vertices can be defined similarly. In our method, we focus on the safe intervals of edges, as the safe intervals of edges are subsets of the safe intervals of vertices, thus providing safer solutions if the lengths of the edges in the graph are larger than the dimensions of the obstacles. Given a path consists of consecutive edges with safe intervals, its temporal corridor can be defined as

::: {#def: tempcorr .definition}
**Definition 3**. *(Temporal Corridor for Path) A temporal corridor for a path is a series of time intervals where the safe intervals of any two consecutive edges in the path overlap.*
:::

By Definition [3](#def: tempcorr){reference-type="ref" reference="def: tempcorr"}, temporal corridors are directed. In this work, we consider both directions of temporal corridors for a complete evaluation (see Algo. [\[alg: graph\]](#alg: graph){reference-type="ref" reference="alg: graph"}) for spatial-temporal topological equivalence.

# Spatial-Temporal Topological Path Planning

## Graph Construction with Safe Intervals

### Safe Intervals Generation for Edges

We represent the static environment with a 3D occupancy map and dynamic obstacles as bounded ellipsoids with trajectories parameterized by polynomials. For each edge in the graph, a cuboid covering it is generated and inflated by a margin equal to the Minkowski sum of the quadrotor and moving obstacles. Collision time stamps are determined by solving the points of intersection between the hyperplanes of the cuboid and moving obstacles' trajectories. Finally Definition [2](#def: safeinterval){reference-type="ref" reference="def: safeinterval"} is applied for calculating the safe intervals.

### Dynamic Connected Visibility Graph Construction

To reduce space complexity, ensure the safety on edges, and preserve the multi-query property within a given time horizon, we generate a dynamic connected visibility graph as shown in Fig. [3](#fig:approximation){reference-type="ref" reference="fig:approximation"}.

:::: {#fig:approximation .figure latex-placement="!ht"}
::: caption
\(a\) Illustration of dynamically connected visibility graphs in dynamic environments. A dynamic connected graph has edges that are valid in their safe intervals. Valid paths in distinct UTVD classes are shown in purple and green. (b) Simulation result of the front-end graph search, the red objects are moving obstacles with trajectories in dash lines, and the black ones are static obstacles. The graph is shown in green, and multiple distinct paths are represented in yellow.
:::
::::

The algorithm for constructing the graph is detailed in Algorithm [\[alg: graph\]](#alg: graph){reference-type="ref" reference="alg: graph"}. Within a dynamic connected visibility graph, vertices are classified as either Guards or Connectors. Vertices are classified as Connectors if they can connect with any other two Guards; otherwise, they are classified as Guards.

The start and goal vertices are initiated as Guards($Guard()$) into the graph. In the main loop, **getSample()** function employs a heuristic strategy to sample vertices uniformly from regions with lower Connector-Guard ratios. The **findVisibleGuard()** identifies Guards $g_1, g_2$ that can connect to a sampled vertex $v$. Safe intervals are determined for the edge connecting $g_1, v$ and the edge connecting $g_2, v$. They can be connected if any of these safe intervals overlap. Neighbors for $g_1, g_2$ are then identified by **neighbors()**. As the connection direction is ambiguous, both the forward path $\overrightarrow{\varsigma_1}$ and the reverse path $\overleftarrow{\varsigma_1}$ are considered. UTVD class is checked between newly sampled path and neighbor paths by **checkEquiv()**, each path within their safe intervals is discretized into a set of points with time stamps, and then UTVD is employed to assess equivalence. If they belong to the same class and the newly sampled path is shorter, the neighbor vertex is replaced with the sampled vertex. Otherwise, the sampled vertex is designated as a Connector($Connector()$), generating new edges for both $g_1$ and $g_2$ in **addNewEdge()**. This dynamically connected visibility graph meets the dynamic feasibility requirements and guarantees collision-free edges, allowing for various parameterizations along each edge. For instance, the quadrotor can smoothly accelerate, decelerate, and stop along edges while avoiding collisions within safe intervals.

::: algorithm
$G \leftarrow \varnothing$,\
$G \cup Guard(x_s) \cup Guard(x_g)$,\

$v$ = **getSample**()\
$guards$ = **findVisibleGuard**($v, \mathcal{X}_{obs}, G, T$)\
$G \cup Guard(v)$\
continue\

$\varsigma_1 \leftarrow (g_1, v ,g_2$)\
${\rm SI}(g_1, v) \leftarrow$ **findSafeIntervals($g_1, v$)** \
${\rm SI}(v ,g_2) \leftarrow$ **findSafeIntervals($v ,g_2$)** \
continue

$\varsigma _2 \leftarrow (g_1 , n_g , g_2)$\
isSameTopo = **checkEquiv**($\overrightarrow{\varsigma _1}$, $\overrightarrow{\varsigma _2}$) $\vee$**checkEquiv**($\overleftarrow{\varsigma _1}$, $\overleftarrow{\varsigma _2}$)\
$n_g \leftarrow v$\
break\
$G \cup Connector(v, {\rm SI}(g_1, v), {\rm SI}(v ,g_2))$\
**addNewEdge($v, g_1, g_2$)**
:::

Given a graph, the depth-first search algorithm is employed to explore multiple distinct topological paths. For each path, vertex parameterization by time is implemented by the rule similar to [@SIPP1] (i.e., reach vertices as early as possible). The initial temporal corridors are constructed by Definition [3](#def: tempcorr){reference-type="ref" reference="def: tempcorr"}.

## Theoretical Analysis

With the assumption that the environment can be fully represented by graphs, we further discuss the optimality and completeness of the proposed approach. SIPP-based methods discretize an environment into grids with the subsequent composition of vertices within a graph, and the time domain is continuously evaluated. The SIPP is proven to be complete and resolution-optimal[@SIPP1] without dynamic constraints and action availability. Safe Interval-based methods are intrinsically equivalent to finding a feasible temporal corridor. By introducing PRM-based strategies and dynamic considerations, our proposed method can achieve probabilistic complete and optimal path planning within a finite duration.

# Trajectory Planning with Spatial-Temporal Corridors

The front-end method provides the initial paths in distinct UTVD classes and corresponding temporal corridors. To further ensure the smoothness of the third-order systems, We apply the uniform B-spline curve to represent the trajectory, with the advantages of its convex hull property to enforce dynamic feasibility and geometric constraints.

## Trajectory Optimization Formulation

We can efficiently parameterize the continuous trajectory in its flat space because of differential flatness[@5980409]. Given a collision-free path generated considering lower-order dynamics $\Gamma :[t_s, t_e] \ \mapsto \in \mathbb{R}^3$, we can generate a n-dimension $p_b$ degree uniform B-spline constructed by control points $\mathbf{Q} = [\mathbf{Q}_1, \cdots, \mathbf{Q}_{N_c} ]^T, \mathbf{Q}_i \in \mathbb{R}^3$, and a knot vector $\mathbf{t} = [t_1, \cdots, t_{N_c+p_b} ]^T \in  \mathbb{R}^{N_c+p_b}$ with identical knot span $t_s$. Hence, we formulate the optimization problem as $$\begin{align}
        \min_{ \bm{Q, t} } \  \sum_d^D \lambda_d J_d(\bm{Q, t}),
\end{align}$$ where $D = \{ c, od, ct, f \}$, $J$ represents the control cost (c), the collision cost with moving obstacles (od), the spatial-temporal corridor cost (ct), and the dynamic feasibility cost (f), and $\lambda$ denotes the corresponding weights. We adopt a framework similar to that in [@fasttopo; @9309347] for optimizing control points with fixed time knots and iteratively refining time allocation. The one with minimum control cost is selected among multiple trajectories.

## Spatial-Temporal Corridor Inflation

The front-end path is an initial spatial-temporal corridor, where edges define spatial corridors and time intervals set temporal corridors. However, the spatial corridors are confined to geometric edges, limiting trajectory flexibility. Hence, we need to inflate both the spatial and temporal corridors in 4-D space [@ding2019safe]. Specifically, for each edge, we incrementally select two successive seed points along it, inflating the spatial corridors as axis-aligned cuboids in 3-D space while inflating the temporal corridors by checking potential collisions in these cuboids. Each spatial-temporal corridor is defined by a feasible temporal interval $(t_l, t_u)$ within which the cuboid is collision-free, and boundary points of the cuboid $\{b_l, b_u\}$, where $b_l$ and $b_u$ are the lower bound and upper bound in each 3-D dimension, respectively. Fig. [4](#fig:infla){reference-type="ref" reference="fig:infla"} provides a 1-D example of spatial-temporal corridor inflation.

:::: {#fig:infla .figure latex-placement="!ht"}
::: caption
Demonstration of spatial-temporal corridors inflation in one dimension, (a) denoted by position (x) versus time (t). The initial path and initial spatial-temporal corridors are represented in blue and green, static obstacles are shown in black while moving obstacles 1 and 2 are colored in red. (b) The inflated spatial-temporal corridors are shown in yellow, which are generated by seed points in triangular shapes. The optimized B-spline trajectory with control points is colored in purple.
:::
::::

## Objectives Evaluation

We derive control points for higher-order velocity, acceleration, and jerk to evaluate the minimum control and dynamics cost of the B-spline trajectory. We represent the velocity control points $\mathbf{V} = [\mathbf{V}_1, \cdots, \mathbf{V}_{N_c-1} ]^T$, acceleration control points $\mathbf{A} = [\mathbf{A}_1, \cdots, \mathbf{A}_{N_c-2} ]^T$ and jerk control points $\mathbf{J} = [\mathbf{J}_1, \cdots, \mathbf{J}_{N_c-3} ]^T$ using control points $\mathbf{Q}$ and knot span $t_s$, as $$\begin{gather}
    \mathbf{V}_i = \frac{\mathbf{Q}_{i+1} - \mathbf{Q}_{i}}{t_s}, \quad  
    \mathbf{A}_i = \frac{\mathbf{V}_{i+1} - \mathbf{V}_{i}}{t_s}, \quad 
    \mathbf{J}_i = \frac{\mathbf{A}_{i+1} - \mathbf{A}_{i}}{t_s}.
\end{gather}$$ The control cost function $J_c$ is also formulated as penalizing the jerk of the trajectory, $$\begin{equation}
       J_c = \sum_{i=p_b-3}^{N_c-p_b}\|\mathbf{J}_i\|_2^2 .
\end{equation}$$ The dynamically feasible cost is formulated to penalize the trajectory with exceeding maximum velocity $v_m$ and maximum acceleration $a_m$ with respect to each dimension: $$\begin{equation}
       J_f = \sum_{i=p_b-1}^{N_c-p_b}\|\mathbf{V}_{i} - v_{m}\|_2^2 + 
             \sum_{i=p_b-2}^{N_c-p_b}\|\mathbf{A}_{i} - a_{m}\|_2^2 .
\end{equation}$$ We also incorporate a collision cost for dynamic obstacles, as the generated trajectory may come too close to the boundaries of cuboids. $$\begin{gather}
    J_{od} = \sum_{i=0}^m\sum_{j=0}^k J_{ij}, \\ 
       J_{ij} = \left\{
        \begin{array}{ll}
            0 & \text{if } d(p_i, o_{j}) > d_{th} \\
            (d(p_i, o_{j}) - dth)^2 & \text{if } d(p_i, o_{j}) \leq d_{th}
        \end{array} \right.,
\end{gather}$$ where $m$ is the number of samples, $k$ is the number of dynamic obstacles. We applied the Euclidean distance function, $d(p_i, o_j) = \|E_j^{-1}(p_i - o_{j})\|_2$ between $i^{th}$ sampled point and $j^{th}$ dynamic obstacle center, $E_j$ is the coefficient matrix of an ellipsoid-shaped moving obstacle, $d_{th}$ is the minimum distance threshold.

The spatial-temporal corridor cost is defined as the L1 norm of the distance between control points and cuboids, $$\begin{equation}
       J_{ct} = \sum_{i=p_b}^{N_c-p_b}(\|b_{l,j} - \mathbf{Q}_{i}\|_1 + \|\mathbf{Q}_{i} - b_{u, j}\|_1).
\end{equation}$$ We identify the cuboid corresponding to $\mathbf{Q}_{i}$ by locating the spatial corridor whose temporal interval includes the knot of $\mathbf{Q}_{i}$.

Fig. [5](#fig: traj){reference-type="ref" reference="fig: traj"} visualizes back-end optimization with spatial-temporal corridors. The top-down view shows a quadrotor's trajectory (0s--9s), the initial B-spline (blue), corridor cuboids (yellow), moving obstacles (red) with IDs, static obstacles (black), and the quadrotor's position (green circles). The optimized trajectory with minimal control cost is in pink.

:::: {#fig: traj .figure latex-placement="!ht"}
![](Huang2024Safe_figs/traj.png){width="1.0\\columnwidth"}

::: caption
Simulation result (top-down view in 3-D environment) of the back-end optimization. Each cuboid is valid within its temporal intervals. The yellow cuboid demonstrates the spatial-temporal corridor.
:::
::::

# Results

:::: {#fig: bench_fig .figure latex-placement="!ht"}
![](Huang2024Safe_figs/result.png){width="2.0\\columnwidth"}

::: caption
Simulation results for front-end methods for 100 trials in three different complexity levels maps. Density is calculated as the ratio of occupied grid cells to total grid cells in the bounded space. The density range of sparse, moderate, and dense maps are $[0, 0.01]$, $[0.05, 0.1]$, and $[0.15, 0.2]$, and the range of number of dynamic obstacles are $[0, 20]$, $[20,  40]$, and $[40, 60]$, respectively.
:::
::::

## Implementation Details

We apply the parameterized environment generation in [@10610207] and extend to moving obstacles with varying ellipsoidal sizes and minimum acceleration trajectories in three types of maps with different levels of complexity. The collision-free start and goal positions are randomly generated for each trial, and each map is re-generated randomly every three trials. The plan is considered successful if the quadrotor can find a path or trajectory from the start to the goal position without collision.

## Simulation Experiments

### Front-end Paths Benchmarks

We compared the performance of our front-end approach with four different path planners: T_PRM [@TPRM], VIS_PRM [@topo1], SIPP [@SIPP1], and SIPP_IP [@kinoSIPP]. To demonstrate dynamical feasibility, we incorporate kinodynamic checking into VIS_PRM and T_PRM by determining the feasible traversal time using a trapezoidal velocity profile instead of assuming a constant maximum speed, denoted as "(dyn)\". We evaluate these methods with respect to success rate, computational time, path length, and flight time. The safety for success rate computation is evaluated by checking if edges are collision-free within the duration of start and end vertices. As shown in Fig. [6](#fig: bench_fig){reference-type="ref" reference="fig: bench_fig"}, our method achieves a higher success rate in all environments of different density levels. In addition, the proposed method achieves relatively low flight times in all cases.

SIPP-based methods, which rely on pre-computing time intervals for each grid, experience significantly longer computation times and performance degradation in denser environments. T_PRM demonstrates a high success rate and low computation time, with slightly longer path lengths than our methods. As collision avoidance of T_PRM is guaranteed by checking the vertices, the edge lengths should be constrained into a reasonable range to prevent unsafe connection, which results in more convoluted paths. VIS_PRM samples vertices with timestamps and connects them if the edge remains collision-free during a defined period. It has a lower success rate as moving obstacles increase, compared with methods that leverage the completeness of safe interval planning.

The success rate of T_PRM (dyn) decreases, and flight times significantly increase compared to the original T_PRM, showing that the maximum edge length alone cannot ensure complete safety when dynamic feasibility is taken into account. VIS_PRM (dyn) doesn't demonstrate a significant change compared to the original VIS_PRM, because random sampling of vertex time stamps usually yields sufficient time durations to ensure dynamic feasibility. The SIPP_IP algorithm has the longest computational time and often stops after reaching the maximum number of expanded vertices.

### Trajectory Evaluations

To further validate the effectiveness of our framework, we evaluate our planner by comparing its performance with a baseline planner: TPRMO, which uses TPRM as the front-end method and optimizes it without the use of spatial-temporal corridors. The front-end and back-end planning framework is triggered when a collision is detected on an initial B-spline trajectory. Trajectories are generated and evaluated if the front-end planner can find a valid path. For the baseline method, we include the Euclidean distances towards moving obstacles as cost functions and use the static obstacle avoidance strategy mentioned in [@9309347]. We conducted 100 trials for each type of map. The results in Table [5](#table1){reference-type="ref" reference="table1"} show that the success rate in one-time optimization (without re-optimizing upon failure), the average trajectory length, and duration are comparable between the two methods. However, the average control cost (integral of the squared jerk) is significantly reduced using our method. It demonstrates that our two-stage method, utilizing the spatial-temporal corridor, produces smoother trajectories. Re-parameterizing trajectory time within the corridor ensures both safety and efficiency.

[]{#table1 label="table1"}

::: {#table1}
+----------+---------+------------------------+------------------------+------------------------+------------------------+
| Env.     | Methods | ::: {#table1}          | ::: {#table1}          | ::: {#table1}          | ::: {#table1}          |
|          |         |   -------              |   ----------           |   ----------           |   -------------------- |
|          |         |    Opt.                |     Traj.              |     Flight             |        Ctrl. Cost      |
|          |         |    Succ.               |    Len. (m)            |    Time (s)            |    Avg. (m$^2$/s$^5$)  |
|          |         |    Rate                |   ----------           |   ----------           |   -------------------- |
|          |         |   -------              |                        |                        |                        |
|          |         |                        |   : Planner comparison |   : Planner comparison |   : Planner comparison |
|          |         |   : Planner comparison | :::                    | :::                    | :::                    |
|          |         | :::                    |                        |                        |                        |
+:=========+:=======:+:======================:+:======================:+:======================:+:======================:+
| Sparse   | Ours    | 100%                   | 7.66                   | 6.04                   | **17.71**              |
|          +---------+------------------------+------------------------+------------------------+------------------------+
|          | TPRMO   | 99%                    | 7.89                   | 5.55                   | 72.67                  |
+----------+---------+------------------------+------------------------+------------------------+------------------------+
| Moderate | Ours    | 98%                    | 7.93                   | 6.05                   | **26.20**              |
|          +---------+------------------------+------------------------+------------------------+------------------------+
|          | TPRMO   | 97%                    | 8.11                   | 5.72                   | 73.27                  |
+----------+---------+------------------------+------------------------+------------------------+------------------------+
| Dense    | Ours    | 97%                    | 7.44                   | 5.69                   | **30.53**              |
|          +---------+------------------------+------------------------+------------------------+------------------------+
|          | TPRMO   | 97%                    | 7.52                   | 5.36                   | 70.31                  |
+----------+---------+------------------------+------------------------+------------------------+------------------------+

: Planner comparison
:::

## Hardware Experiments

We validated our proposed framework with extensive real-world experiments. To create moving obstacles, we employed two Scarab ground robots [@Scarab2008]. Each Scarab is equipped with a Hokuyo UTM30LX laser and an onboard computer with an Intel i7-8700K CPU. In addition, we mount a $0.91m \times 0.16m$ cylinder on each of them. We set up static obstacles with three $1.2m \times 0.3m$ cylinders. A customized Dragonfly 230 quadrotor is used to carry out the experiments. It carries a VOXL flight board, a forward-facing Time-of-Flight camera, and a downward-facing tracking camera, as detailed in work [@10.1007/978-3-030-71151-1_37]. The Vicon Motion Capture system is used to set up the common reference frame and provide odometry information. One set of our experiments is demonstrated in Fig. [7](#fig: real-world experiment){reference-type="ref" reference="fig: real-world experiment"}. The quadrotor first took off from the bottom-right corner while the scarab robots were tracking a rectangle trajectory, as illustrated in white dotted lines. A navigation goal centered on top of the black box was set and the planner was triggered. As shown in the upper-right corner, the spatial-temporal corridor was built and a minimum control cost trajectory was generated. The quadrotor tracked the planned trajectory closely and reached the navigation goal, as illustrated in the sub-figures. Subsequent navigation goals were set after the quadrotor reached the first goal.

:::: {#fig: real-world experiment .figure latex-placement="!t"}
![](Huang2024Safe_figs/experiment.png){width="1.0\\columnwidth"}

::: caption
Real-world experiment with two moving obstacles and three static obstacles. In the upper-right visualization in the top-down view, the red and black polygons correspond to the moving obstacles and static obstacles. Besides, the red curve and green arrows represent the quadrotor trajectory and odometry, respectively. The experiment video is available at <https://youtu.be/Bx_q_11eOrg>.
:::
::::

# Conclusion {#sec:conclusion}

This paper addresses the dynamic obstacle avoidance problem and introduces a complete two-stage planning approach to efficiently identify the feasibility of the environment setting and generate smooth trajectories. We apply a front-end graph construction and search method to identify multiple distinct paths in different spatial-temporal topological classes based on the concept of UTVD. Spatial-temporal corridors are subsequently constructed to optimize B-spline trajectories, ensuring safety, dynamical feasibility, and smoothness in environments filled with both static and moving obstacles. For future work, we plan to integrate the proposed method with onboard perception systems to achieve more robust and reliable performance in dynamic environments featuring obstacles with complex movement patterns.

[^1]: $^{*}$Equal contribution. The authors are with the GRASP Laboratory, University of Pennsylvania, Philadelphia, PA, 19104 USA `{songhaoh, yuweiwu, yztao, kumar}@seas.upenn.edu`.

[^2]: This research was sponsored by TILOS under NSF grants CCR-2112665.
