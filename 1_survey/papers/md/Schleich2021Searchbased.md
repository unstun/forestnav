---
citation_key: Schleich2021Searchbased
arxiv_id: 2103.14607
arxiv_url: https://arxiv.org/abs/2103.14607
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:32:11Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

The application of micro aerial vehicles (MAVs) to surveillance, inspection, and search & rescue tasks has gained increasing popularity in recent years. Generating fast, dynamically feasible MAV trajectories for such scenarios is a challenging task, since one usually has to deal with large, initially unknown environments. Fast trajectory replanning is necessary to avoid dynamic or previously unknown obstacles. Many existing methods generate trajectories in a two-stage approach: First, a 3D position-only obstacle-free path is planned using search-based or sampling-based methods [@hart1968formal; @lavalle1998rapidly]. Afterwards, this path is refined to a high-dimensional trajectory including velocities. Refinement strategies include quadratic programming [@richter2016polynomial], B-Spline path planning [@koyuncu2008probabilistic] and gradient-based optimization methods [@kalakrishnan2011stomp] as used in [@nieuwenhuisen2019search]. These approaches only generate locally optimal trajectories. However, incorporating the system's dynamics into the planning process allows to generate globally optimal trajectories. Liu et al. [@liu2017search] propose a search-based method to directly plan second- and third-order MAV trajectories. They unroll motion primitives to generate a state lattice graph, from which they extract trajectories using A\* with a heuristic based on the solution of a Linear Quadratic Minimum Time problem. Since velocities are explicitly considered during planning, their approach can be extended to generate trajectories through doors that are narrower than the MAV diameter [@liu2018search]. However, searching high-dimensional state spaces is computationally expensive. Thus, such approaches either lack the capability for fast replanning or are restricted to small or low-resolutional environment representations. A common approach for reducing the state space size for spatial path planning is local multiresolution [@behnke2003local]. Here, only the vicinity of the robot is represented at high resolution, while the resolution decreases with increasing distance from the robot. In this work, we apply the concept of local multiresolution to the state lattice graph of Liu et al. [@liu2017search]. Thus, we are able to significantly reduce planning times. This increases the applicability of the approach to large dynamic environments, where frequent replanning is necessary. In summary, the main contributions of this paper are:

- The introduction of local multiresolutional state lattices,

- an expansion scheme for the A\* algorithm addressing the issues of multiresolutional state representations, and

- a search heuristic based on the solution of 1D sub-problems.

::::: {#fig:teaser .figure latex-placement="t"}
::: center
![](Schleich2021Searchbased_figs/teaser.jpg){width="40%"}
:::

::: caption
The MAV following a trajectory in a simulated outdoor environment. The start is at the red circle and the goal is marked by the green square. The trajectory is replanned online at 1 Hz. Red cubes mark the start positions of each replanning step.
:::
:::::

# Related Work {#sec:related_work}

Multiresolutional approaches are commonly used to accelerate planning. Behnke [@behnke2003local] proposed A\*-based path planning on robot-centered local multiresolution grids, where the spatial resolution decreases with increasing distance from the robot. Nieuwenhuisen et al. [@nieuwenhuisen2014hierarchical] extend this approach to plan 3D trajectories for MAVs. In [@nieuwenhuisen2016local], local multiresolution in time is used to enable fast reoptimization of an initial path from a grid-based planner. Du et al. [@du2020multi] perform multiple A\* searches simultaneously on grids with different resolutions while sharing states that lie on multiple resolution grids.

Multiresolution has also been used in combination with state lattices. González-Sieira et al. [@gonzalez2016adaptive] choose the resolution level based on the complexity of the local environment, i.e., on the distance from obstacles. They apply different sets of motion primitives for each level. In [@gonzalez2019graduated], the same authors group motion primitives in categories. When expanding a state, the longest collision-free motion from each category is applied. Pivtoraiko et al. [@pivtoraiko2008differentially] use a uniform 2D grid but apply different state transitions for start and goal area than for the other areas. This framework is extended by Andersson et al. [@andersson2018receding]. They propose a receding-horizon method, where the first half of the planning time is used for planning in a high-dimensional space. The search is continued afterwards with lower dimension and a reduced action set. All of the above state lattice methods use different action sets dependent on the current representation level. However, all levels share the same spatial resolutions. In contrast to those methods, our approach reduces the spatial resolution with increasing distance from the current MAV position.

Likhachev et al. [@likhachev2009planning] propose multi-resolutional state lattices to plan trajectories for autonomous ground vehicles. The action set of the lower-resolution level is a strict subset generated from the higher-level action set by choosing only actions whose end states lie on the low-dimensional grid. The state representation used by Likhachev et al. only includes movement directions, but their approach is expanded by Rufli et al. [@rufli2009smooth] to also consider velocities. Petereit et al. [@petereit2013mobile] use two representation levels with different dimensionality. The representation level of a state is chosen based on the time it takes to reach this state. Similar to the method of Likhachev et al., transitions from higher to lower representation levels are only possible for states that match the resolution of the lower level.

Our method uses the same dimensionality for all representation levels but reduces spatial and velocity resolutions for higher levels. In contrast to the approaches mentioned above, we do not rely on a fixed precomputed set of motion primitives. For transitions between different representation levels, we adjust the motion primitives such that the resulting states match the resolution of the target level.

# Method {#sec:method}

Our trajectory planning method is based on the framework of Liu et al. [@liu2017search]. In this work, we restrict ourselves to second-order systems and leave the extensions to third-order systems for future work. Thus, we model the MAV state as a $6$-tuple $s=(\mathbf{p}, \mathbf{v}) \in \mathbb R^6$ consisting of a 3D position $\mathbf{p}$ and velocity $\mathbf{v}$. Mind, that we do not explicitly model the MAV yaw, since it does not influence the system's dynamics. Instead, we choose the yaw in a post-processing step based on the flight direction of the planned trajectory.

The state space is discretized by unrolling motion primitives from the initial MAV state $s_0=(\mathbf{p_0}, \mathbf{v_0})$, resulting in a state lattice graph $\mathcal G(\mathcal S, \mathcal E)$. Here, $\mathcal S$ denotes the set of discretized MAV states, and $\mathcal E$ is the set of motion primitives connecting the states. Each motion primitive is generated by applying a constant acceleration $\mathbf{u}$ from a discrete control set $\mathcal U_M \subset \mathbb R^3$ over a short time interval $\tau$. Thus, the motion primitive $F_{\mathbf{u},s}$ connecting the states $s$ to $s':=F_{\mathbf{u},s}(\tau)$ can be expressed as a time-parameterized polynomial $$\begin{equation}
F_{\mathbf{u},s}(t) = \begin{pmatrix}\mathbf{p}+ t \mathbf{v} + \frac{t^2}{2} \mathbf{u}\\\mathbf{v} + t \mathbf{u}\end{pmatrix},\,\text{ for } t\in[0,\tau].
\label{eq:primitive}
\end{equation}$$ An example for the resulting state lattice graph is depicted in Fig. [2](#fig:state_lattices){reference-type="ref" reference="fig:state_lattices"} a.

The costs for a motion primitive are defined as the weighted sum of control effort and primitive duration, i.e.,  $$\begin{equation}
C(F_{\mathbf{u},s}) = ||\mathbf{u}||^2_2\tau + \rho\tau.
\label{eq:primitive_cost}
\end{equation}$$

The optimal trajectory can be planned in the state lattice graph $\mathcal G$ by applying graph search methods like A\*. For more details, we refer to [@liu2017search].

In the following, we introduce multiple concepts to reduce planning times. In Sec. [3.1](#sec:mres_lattice){reference-type="ref" reference="sec:mres_lattice"}, we reduce the state space size by applying the concept of local multiresolution to the state lattice graph $\mathcal G$. The idea is to restrict the state positions to the corners of a MAV-centered local multiresolution grid, as shown in Fig. [2](#fig:state_lattices){reference-type="ref" reference="fig:state_lattices"} b. Additionally, we reduce the number of discrete velocities for states whose positions are far from the current MAV position.

In Sec. [3.2](#sec:heuristic){reference-type="ref" reference="sec:heuristic"}, we propose a search heuristic based on the solution of 1D sub-problems. To avoid overshooting the goal position, we introduce special goal action sequences in Sec. [3.3](#sec:goal_actions){reference-type="ref" reference="sec:goal_actions"}. Finally, Sec. [3.4](#sec:level_astar){reference-type="ref" reference="sec:level_astar"} details an expansion scheme for the A\* algorithm, specially designed to overcome issues of multiresolutional state representations.

::::: {#fig:state_lattices .figure}
::: center
a)![image](Schleich2021Searchbased_figs/uniform_lattice.png){width="20%"} b)![image](Schleich2021Searchbased_figs/mres1_lattice.png){width="20%"}
:::

::: caption
Top-down view of 2D state lattice graphs. a) Uniform. b) Local multiresolution. The spatial position of nodes is fixed to the corners of a multiresolution grid with high resolution at the center, i.e., the current MAV position, and coarser resolution for more distant areas. Bright red represents high absolute velocity along the x-axis, bright blue represents high velocity along the y-axis.
:::
:::::

## Local Multiresolutional State Lattices {#sec:mres_lattice}

We define multiple levels of state discretization, dependent on the distance to the initial MAV position $\mathbf{p_0}$. *Level-1* covers all states whose positions are close to $\mathbf{p_0}$. The resolution represents the smallest possible position and velocity changes $\Delta^{(1)}_p$ and $\Delta^{(1)}_v$ of a motion primitive. They depend on the primitive duration $\tau$ and the minimal non-zero acceleration command $u_\text{min}$, and they can be obtained from [\[eq:primitive\]](#eq:primitive){reference-type="eqref" reference="eq:primitive"}: $$\begin{equation}
\Delta^{(1)}_p = \frac{1}{2}\tau^2 u_\text{min}\,\text{, } \Delta^{(1)}_v = \tau u_\text{min}.
\label{eq:resolutions}
\end{equation}$$ The spatial resolutions of the higher levels are obtained by halving the resolution of the next lower level. For *Level*-$i$, we get $\Delta^{(i)}_p:=2^{i-1}\Delta^{(1)}_p$. If we choose $\tau < 1$, the velocity resolution is much coarser than the spatial resolution. Therefore, we only halve the velocity resolution after every second resolution level, i.e., we define $$\begin{equation}
 \Delta^{(2)}_v := \Delta^{(1)}_v,\text{ and } \Delta^{(3)}_v := \Delta^{(4)}_v := 2\Delta^{(1)}_v.
\end{equation}$$ Each resolution level covers an eight times larger volume than the next lower level. They are embedded into each other such that the center of a higher level is replaced by the next lower level. Fig. [2](#fig:state_lattices){reference-type="ref" reference="fig:state_lattices"} b shows an example with two levels.

When generating the state lattice graph by unrolling motion primitives, we have to ensure that the target states of the motion primitives match the discretization of the corresponding resolution level. This is done by carefully defining control sets $\mathcal U^{(i)}$ and time steps $\tau^{(i)}$ for each level. Mind that we define control sets independently for each spatial dimension. With respect to the choice of the time steps, there are two different approaches, which we explain in the following and evaluate against each other in Sec. [4](#sec:evaluation){reference-type="ref" reference="sec:evaluation"}.

#### Fixed time steps per level

From [\[eq:resolutions\]](#eq:resolutions){reference-type="eqref" reference="eq:resolutions"}, it follows that the velocity resolution is halved when doubling the time step, while the spatial resolution is reduced by a factor of four. Thus, by choosing $\tau^{(i)} := 2^{i-1}\tau^{(1)}$, we ensure that position and velocity changes are multiples of the *Level-*$i$ resolutions. If we additionally halve the acceleration commands, the velocity resolution does not change. Thus, for each command $u^{(1)}\in\mathcal U^{(1)}$, we define the corresponding higher-level commands as $$\begin{equation}
 u^{(2)} := u^{(3)} := \frac{1}{2}u^{(1)}\,\text{ and } u^{(4)} := \frac{1}{4}u^{(1)}.
\end{equation}$$ Halving the commands while doubling durations significantly reduces maneuverability, however. We mitigate this effect by adding two special actions to each level: decelerate to zero velocity and accelerate to the maximum allowed velocity in current flight direction.

::::: {#fig:primitive_adjustment .figure}
::: center
a)![image](Schleich2021Searchbased_figs/not_adjusted2.png){width="14.9%"} b)![image](Schleich2021Searchbased_figs/adjusted.png){width="14.9%"}
:::

::: caption
Adjusting motion primitives to the local multiresolution grid. First, the lower-level motion primitives are unrolled (a). Then, the closest grid corners to the primitive end positions are determined (red arrows). Finally, primitives ending at those grid corners are generated (b).
:::
:::::

The above method enforces that end states of all motion primitives starting in *Level-*$i$ also lie on the *Level-*$i$ grid. However, level transitions have to be specially addressed (see Fig. [3](#fig:primitive_adjustment){reference-type="ref" reference="fig:primitive_adjustment"}): We predict the end state of a motion primitive, determine the closest position $\mathbf{p_g}$ on the target resolution grid, and choose the acceleration command $\mathbf{u}$ such that the primitive ends at $\mathbf{p_g}$: $$\begin{equation}
\mathbf{u}=2\frac{\mathbf{p_g}-\mathbf{p}-\tau^{(i)}\mathbf{v}}{(\tau^{(i)})^2},
\end{equation}$$ where $(\mathbf{p}, \mathbf{v})$ denotes the start state of the motion primitive. Using $\Delta_v = \tau^{(i)}\mathbf u$, it follows that the resulting velocity change always is a multiple of the *Level-1* velocity resolution, but for higher levels, the velocity might not match the coarser resolution. Intermediately, we allow this offset for the end states of the adjusted primitives and correct it only when generating their successors.

#### Variable time steps per level

Position changes do not only depend on $\tau$ and $u_\text{min}$ but also on the initial velocity. Using large time steps for high velocities results in a much lower spatial resolution. Thus, many motion primitives with high initial velocities become invalid in the presence of obstacles. Valid trajectories can still be found by choosing lower velocities. However, this increases the trajectory costs, which leads to a significant increase of node expansions during the search (compare Sec. [4.2](#sec:eval_astar){reference-type="ref" reference="sec:eval_astar"}). Thus, it might be a good idea to choose the time steps dependent on the current velocity. For each command $u$ and initial velocity $v$, we choose the smallest time step $\tau^{(i)}\in\{2^k\tau^{(1)},\,k\in\mathbb N_0\}$, such that the position change $\tau^{(i)}v + \frac{1}{2}(\tau^{(i)})^2 u$ is larger than the spatial resolution $\Delta_p^{(i)}$ of the current level. If the position does not change, we set $\tau^{(i)}=\tau^{(1)}$. Mind that we use the same command set for each resolution level. Additionally, we adjust the motion primitive end points to the multiresolution grid as described above.

## 1D Heuristic {#sec:heuristic}

Liu et al. [@liu2017search] use a heuristic based on the solution of a Linear Quadratic Minimum Time problem. Their heuristic considers constraints on the maximum velocity but assumes continuous instead of piecewise-constant control commands. Furthermore, the commands are only implicitly bounded by optimizing the control effort and thus might violate constraints on the maximum acceleration.

We propose a heuristic based on precomputing the actual costs for a 1D problem. To reduce the size of the look-up table, we assume that all goal states have zero velocity. For each pair of signed distance to the goal position and start velocity, we precompute the costs of the optimal 1D trajectory using the *Level-1* resolutions.

The costs of a trajectory $\mathbf{u}_{0:N-1}$ of length $N$ and duration $T=\sum_{k=0}^{N-1}\tau_k$ can be approximated by $$\begin{equation}
\begin{split} 
& C(\mathbf{u}_{0:N-1}) = \rho T + \sum\limits_{k=0}^{N-1} ||\mathbf{u}_k||_2^2 \tau_k \\
&= \rho T + \sum\limits_{k=0}^{N-1} {(u_k)}_x^2 \tau_k + \sum\limits_{k=0}^{N-1} {(u_k)}_y^2 \tau_k + \sum\limits_{k=0}^{N-1} {(u_k)}_z^2 \tau_k \\
&>= \rho T + c_x + c_y + c_z,
\end{split}
\end{equation}$$ where $c_x, c_y, c_z$ are lower bounds on the control efforts along the individual dimensions.

During search, we look up the times $T^\text{1D}_x, T^\text{1D}_y, T^\text{1D}_z$ and control efforts $c^\text{1D}_x, c^\text{1D}_y, c^\text{1D}_z$ of the corresponding 1D sub-problems. The total time $T$ of the 3D trajectory is given by $T=\max\{T^\text{1D}_x, T^\text{1D}_y, T^\text{1D}_z\}$. Without loss of generality, let $T=T^\text{1D}_x$. Thus, we can set $c_x=c^\text{1D}_x$. However, $c^\text{1D}_y$ and $c^\text{1D}_z$ might overestimate $c_y$ and $c_z$ if the 1D trajectories have lower durations than the 3D trajectory. Therefore, we choose $c_y$ and $c_z$ dependent on the current flight direction along the corresponding dimensions:

- When flying towards the goal, we choose the control costs that correspond to a full stop.

- If the velocity is zero, we choose the control costs that correspond to applying minimal acceleration $u_\text{min}$ followed by deceleration $-u_\text{min}$.

- When flying away from the goal, the MAV has to stop, accelerate towards the goal, and decelerate again. Thus, the resulting control cost is the sum of the above cases.

Note that the 1D heuristic is admissible but not consistent: If the dimension, for which the maximum time is achieved, changes, the control costs of a different 1D sub-problem will be used. Thus, the decrease of the estimated 3D control costs might be larger than the costs of the applied action.

## Goal Actions {#sec:goal_actions}

When increasing the motion primitive duration for higher-resolution levels, we might overshoot the goal position frequently during search. Thus, when expanding a state $s$, we check whether the goal is reachable: Let $s$ be represented within *Level*-$i$. We determine lower and upper bounds $p_\text{min}, p_\text{max} \in \mathbb R^3$ of the area that the MAV can reach within the next time step. Here, we assume a possible acceleration of $\pm u_\text{max}$ for a duration of $2 ^{i-1}\tau^{(1)}$ along each dimension. If the goal position lies within $[p_\text{min}$, $p_\text{max}]$, we check whether it can be reached from $s$ using a sequence of *Level-1* motion primitives with a total duration of at most $2 ^{i-1}\tau^{(1)}$. If so, we add the goal state as a neighbor of $s$, connected by the resulting motion primitive sequence. As for the heuristic, we do not consider any obstacles and assume that the goal state has zero velocity. Thus, the sequences of *Level-1* motion primitives can be efficiently precomputed for 1D sub-problems and looked up based on the current velocity and distance to the goal.

## Level-Based Expansion Scheme {#sec:level_astar}

The state space size is significantly reduced when using local multiresolution. However, experiments show that the A\* algorithm tends to expand much more states when applied to multiresolutional state lattices compared to uniform lattices. We found that a reason for this behavior is the fact that the A\* algorithm expands all states whose estimated costs are lower than the costs of the optimal solution (see Sec. [4.2](#sec:eval_astar){reference-type="ref" reference="sec:eval_astar"}). Thus, we adapt the A\* algorithm such that it does not always expand the state with the lowest estimated costs, i.e., lowest $f$-value, but also might expand states with higher values. This might result in sub-optimal solutions, which we accept since the multiresolutional lattice representation already introduces sub-optimality.

For each resolution level, we use a separate priority queue. To determine which node to expand, we compare the state with lowest $f$-value from each level. A state is considered an expansion candidate if the difference between its $f$-value and the globally minimal value is at most the cost of one step in the corresponding resolution level. From all candidates, we expand the one with the lowest heuristic value. We stop the search as soon as the goal state is added to the *OPEN*-list, instead of waiting until the goal state is expanded. This further reduces the runtime at the cost of possible suboptimality.

# Evaluation {#sec:evaluation}

:::: {#fig:arena .figure}
a)![image](Schleich2021Searchbased_figs/arena.png){width="25%"} b)![image](Schleich2021Searchbased_figs/arena_top_down.png){width="19%"}

::: caption
The evaluation environment. a) 3D. b) Top-down. The start position is at the map center (red sphere). Goal positions are marked with squares which are brighter for larger height values.
:::
::::

We use the following parameters for uniform planning as well as for $\textit{Level-1}$ of multiresolutional planning:

::: center
   $\rho$   $\tau$   $v_\text{max}$   $u_\text{max}$     $du$
  -------- -------- ---------------- ---------------- -----------
     16     0.5 s      4 m s^−1^        2 m s^−2^      2 m s^−2^

.
:::

The control set $\mathcal U^{(1)}$ for each dimension is obtained by discretizing $[-u_\text{max}, u_\text{max}]$ uniformly with resolution $du$. This results in *Level-1* resolutions of $\Delta_p^{(1)} = \SI{0.25}{\meter}$ and $\Delta_v^{(1)} = \SI{1}{\meter\per\second}$. The time cost factor $\rho=4u_\text{max}^2$ was chosen as proposed by Liu et al. [@liu2018search].

We evaluate the proposed methods in a simulated outdoor environment of size 128$\times$`<!-- -->`{=html}128 m containing several buildings (see Fig. [4](#fig:arena){reference-type="ref" reference="fig:arena"}). The allowed flight altitude is 0 m--10 m and positions which are closer to obstacles than $\SI{1.5}{\meter}$ are considered invalid.

All planning methods are applied to the same set of 100 trajectory generation tasks. The start position for all tasks is located at the map center with altitude 2 m. Goal positions are sampled uniformly at random with the additional constraint that the distance to the closest obstacle or the map border is at least the spatial resolution of the corresponding level.

We are interested in evaluating the ability for frequent replanning. Thus, after a trajectory is generated, we refine it by replanning from the MAV state that will be reached after one second. This process is repeated until the goal state is reached. For each planning task, we consider the maximum replanning time and expansion number over all replanning steps. Furthermore, we report the costs of the fully refined trajectories. If no solution is found within three million node expansions, we abort the planning process. If a solution is found, the average number of replanning steps lies between $13$ and $18$. Depending on the success rate, each method is thus applied to $900$ to $1400$ different planning tasks.

## 1D Heuristic {#d-heuristic}

::::: {#fig:heuristic .figure}
::: center
a)![image](Schleich2021Searchbased_figs/h_baseline.png){width="20%"} b)![image](Schleich2021Searchbased_figs/h_1D.png){width="20%"}
:::

::: caption
Expanded nodes using different heuristics for a planning task in two spatial dimensions. a) Baseline Heuristic (115988 expansions). b) 1D Heuristic (63769 expansions). Positions of expanded nodes are marked with blue squares. The start position is marked with a red circle, the goal with a green square.
:::
:::::

We evaluate the effect of our proposed 1D Heuristic separately for the different planning methods (see Tab. [1](#tab:heuristic){reference-type="ref" reference="tab:heuristic"}). The number of node expansions is significantly reduced for all three methods. The largest effect is achieved for uniform planning, where the number of expansions is reduced by $93\%$. For the multiresolutional planning methods, there is a reduction of $80\%$ and $85\%$, respectively. Since the 1D heuristic is not consistent, the generated trajectories are not optimal anymore. However, the trajectory costs only increase about $0.75\%$ for uniform planning and multiresolution with variable time steps. The increase for fixed level-dependent time steps is slightly larger with $1.46\%$. Fig. [5](#fig:heuristic){reference-type="ref" reference="fig:heuristic"} visualizes the set of expanded nodes for a uniform planning task in 2D. Since our 1D heuristic significantly accelerates the A\* search, we use it for all subsequent experiments.

:::: center
::: {#tab:heuristic}
+-----------------+------------+------------+-------------+----------------+
|                 |            | Uniform    | MRes~fixed~ | MRes~variable~ |
+================:+:===========+===========:+============:+===============:+
| $h_\text{base}$ | Expansions | 1133136    | 877041      | 890564         |
|                 +------------+------------+-------------+----------------+
|                 | Costs      | **243.69** | **260.79**  | **270.14**     |
+-----------------+------------+------------+-------------+----------------+
| $h_\text{1D}$   | Expansions | **75562**  | **175528**  | **135571**     |
|                 +------------+------------+-------------+----------------+
|                 | Costs      | 245.49     | 264.59      | 272.16         |
+-----------------+------------+------------+-------------+----------------+

:  Comparison of the baseline heuristic $h_\text{base}$ from [@liu2017search] and our proposed 1D heuristic $h_\text{1D}$. For each planning method, the number of expansions and trajectory costs are averaged over all tasks where the corresponding method found valid trajectories with both heuristics. Note that the considered tasks might be different for different planning methods.
:::
::::

[]{#tab:heuristic label="tab:heuristic"}

## Multiresolutional State Lattices with Standard A\* {#sec:eval_astar}

:::: center
::: {#tab:astar}
+:---------------+----------------:+----------------------:+-----------:+----------:+
|                | Mean Maximum    | Time                  | Expansions | Costs     |
+----------------+-----------------+-----------------------+            |           |
|                | Replanning Time | \> 1 s                |            |           |
+----------------+-----------------+-----------------------+------------+-----------+
| Uniform        | 3.54 s          | $\mathbf{46.07}$**%** | 228805     | **261.2** |
+----------------+-----------------+-----------------------+------------+-----------+
| MRes~fixed~    | 6.44 s          | $62.92\%$             | 309526     | 273.2     |
+----------------+-----------------+-----------------------+------------+-----------+
| MRes~variable~ | **2.73 s**      | $58.43\%$             | **160032** | 274.6     |
+----------------+-----------------+-----------------------+------------+-----------+

:  Planning statistics for different state lattice representations. Maximum replanning times, number of expansions and trajectory costs are averaged over the tasks where all three planning methods found valid solutions. Additionally, the fraction of tasks for which the longest replanning step exceeds 1 s are given.
:::
::::

[]{#tab:astar label="tab:astar"}

To evaluate the effect of multiresolutional state lattices, we record for each trajectory generation task the maximal replanning time and maximum number of node expansions. Tab. [2](#tab:astar){reference-type="ref" reference="tab:astar"} reports the averages of these values over the tasks where all three planning methods generated valid trajectories. Interestingly, using multiresolutional state lattices with fixed level-dependent motion primitive durations significantly increases the maximum replanning time. Furthermore, maximum replanning times exceed 1 s more often for both multiresolutional state lattice variants. Although the size of the state space is reduced when using multiresolution, those methods tend to expand more states during A\* search for some tasks.

:::: center
::: {#tab:level_astar}
+:---------------+----------------:+---------------------------:+-----------:+----------:+
|                | Mean Maximum    | Time                       | Expansions | Costs     |
+----------------+-----------------+----------------------------+            |           |
|                | Replanning Time | \> 1 s                     |            |           |
+----------------+-----------------+----------------------------+------------+-----------+
| Uniform        | 0.65 s          | $16.85\%$                  | 50880      | 273.8     |
+----------------+-----------------+----------------------------+------------+-----------+
| MRes~fixed~    | 0.57 s          | $12.36\%$                  | 26078      | **272.3** |
+----------------+-----------------+----------------------------+------------+-----------+
| MRes~variable~ | **0.30 s**      | $\mathbf{6.74}\textbf{\%}$ | **17772**  | 276.2     |
+----------------+-----------------+----------------------------+------------+-----------+

:  Planning statistics using the level-based expansion scheme. Maximum replanning times, number of expansions and trajectory costs are averaged over the same tasks as in Tab. [2](#tab:astar){reference-type="ref" reference="tab:astar"}.
:::
::::

[]{#tab:level_astar label="tab:level_astar"}

:::: {#fig:f_value_histogram .figure latex-placement="t"}
a)![image](Schleich2021Searchbased_figs/f_histogram_16.png){width="24%"} b)![image](Schleich2021Searchbased_figs/f_histogram_8.png){width="24%"}

::: caption
Histograms for the $f$-values of each expanded state with different time cost weights $\rho$. a) $\rho=16$. b) $\rho=8$.
:::
::::

:::: table*
::: center
+:-------------------------------------------+--------------------:+----------------:+----------------------:+-----------:+-----------:+
|                                            | Success             | Mean Maximum    | Time \> 1 s           | Expansions | Costs      |
+--------------------------------------------+                     +-----------------+                       |            |            |
|                                            |                     | Replanning Time |                       |            |            |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| Uniform, $h_\text{base}$, A\*              | $71.43\%$           | 22.52 s         | $89.80\%$             | 1085740    | **241.31** |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~fixed~, $h_\text{base}$, A\*          | $79.59\%$           | 17.87 s         | $89.80\%$             | 744640     | 249.91     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~variable~, $h_\text{base}$, A\*       | $87.76\%$           | 14.21 s         | $87.76\%$             | 664036     | 253.85     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| Uniform, $h_\text{1D}$, A\*                | $91.84\%$           | 1.14 s          | $51.02\%$             | 70085      | 243.16     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~fixed~, $h_\text{1D}$, A\*            | $95.92\%$           | 2.87 s          | $66.33\%$             | 143822     | 254.33     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~variable~, $h_\text{1D}$, A\*         | $98.98\%$           | 1.60 s          | $62.24\%$             | 89085      | 255.85     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| Uniform, $h_\text{base}$, Level-A\*        | $95.92\%$           | 0.41 s          | $29.59\%$             | 24190      | 246.15     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~fixed~, $h_\text{base}$, Level-A\*    | $97.96\%$           | 0.20 s          | $20.41\%$             | **5684**   | 246.69     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~variable~, $h_\text{base}$, Level-A\* | $\mathbf{100}$**%** | **0.19 s**      | $16.33\%$             | 8505       | 248.84     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| Uniform, $h_\text{1D}$, Level-A\*          | $\mathbf{100}$**%** | 0.20 s          | $22.45\%$             | 16739      | 253.94     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~fixed~, $h_\text{1D}$, Level-A\*      | $\mathbf{100}$**%** | 0.21 s          | $20.41\%$             | 8284       | 252.15     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
| MRes~variable~, $h_\text{1D}$, Level-A\*   | $\mathbf{100}$**%** | 0.20 s          | $\mathbf{12.24}$**%** | 10945      | 255.28     |
+--------------------------------------------+---------------------+-----------------+-----------------------+------------+------------+
:::

[]{#tab:overview label="tab:overview"}
::::

To further investigate this behavior, we have a closer look at the tasks where uniform planning outperforms multi­resolution planning. We compare the $f$-values of each state $s$, i.e., the sum of the costs for moving from the start state to $s$ and the heuristic costs for reaching the goal from $s$. Fig. [6](#fig:f_value_histogram){reference-type="ref" reference="fig:f_value_histogram"} shows histograms for the $f$-values of each expanded state during an example search for the different state lattice representations. The number of states grows approximately cubic with increasing $f$-value. Due to the reduced number of states, the curves for the multiresolutional lattices grow at lower rates. The A\* algorithm expands all states whose $f$-value are smaller than the optimal path costs. Since the costs of the paths in multiresolutional lattices are higher than the optimal costs in the uniform lattice, states up to a higher $f$-value have to be expanded. Due to the cubic increase, this overhead might result in an overall larger amount of expanded states for multiresolutional search. Note that the difference between the maximum $f$-values for the different state representations is only $8$. This corresponds to the smallest possible cost for one action. When reducing the time cost factor $\rho$, multiresolutional planning expands fewer states than uniform planning (Fig. [6](#fig:f_value_histogram){reference-type="ref" reference="fig:f_value_histogram"} b), but the resulting trajectory durations might be suboptimal. Instead, the issue can be addressed by removing the constraint that all states whose $f$-value are smaller than the optimal path costs have to be expanded. This is evaluated in the next section.

## Level-Based Expansion Scheme {#level-based-expansion-scheme}

We apply the level-based expansion scheme from Sec. [3.4](#sec:level_astar){reference-type="ref" reference="sec:level_astar"} to all three state lattice representations and evaluate them on the same set of tasks that was used in Sec. [4.2](#sec:eval_astar){reference-type="ref" reference="sec:eval_astar"}. The results are summarized in Tab. [3](#tab:level_astar){reference-type="ref" reference="tab:level_astar"}. All three methods benefit from using the adapted expansion scheme. While the average maximum replanning times for uniform state lattices are reduced by around $80\%$, the reduction for multiresolutional lattices is even higher with around $90\%$. Similar reductions are achieved with respect to the number of state expansions. The trajectory costs for uniform lattices increases by roughly $5\%$. Interestingly, the costs for multiresolutional planning do not change much. When using fixed level-dependent time steps, the costs even decrease slightly, which is possible because the used heuristic is not consistent.

In Tab. [\[tab:overview\]](#tab:overview){reference-type="ref" reference="tab:overview"}, we compare the method of [@liu2017search] against all methods presented in this work. Note that average planning times, expansion numbers and trajectory costs only consider tasks solved by the baseline. The costs of all trajectories are at most $6\%$ longer than the optimal trajectory generated by the baseline. However, the average maximum replanning time can be reduced by up to two orders of magnitude.

## Online Replanning

::::: {#fig:online_replanning .figure}
::: center
![](Schleich2021Searchbased_figs/simulation_times.png){width="40%"}
:::

::: caption
Replanning times in simulation.
:::
:::::

Finally, we test our approach in simulation using the RotorS simulator [@furrer2016rotors]. We start with an initial OctoMap [@hornung13auro] of the environment (Fig. [4](#fig:arena){reference-type="ref" reference="fig:arena"}), but add additional unmapped static obstacles such that frequent replanning is necessary. Replanning is triggered at 1 Hz and the map is constantly updated using measurements of a simulated 3D laser scanner. Fig. [7](#fig:online_replanning){reference-type="ref" reference="fig:online_replanning"} shows the corresponding planning times of uniform lattices and MRes~variable~. Both methods use our 1D heuristic and the level-based expansion scheme. While our approach has a maximal replanning time of 0.69 s, uniform planning exceeds 1 s in one third of all replanning steps. Fig. [8](#fig:trajectories){reference-type="ref" reference="fig:trajectories"} shows the corresponding trajectories. A 3D view of the environment and the trajectory generated by our method is given in Fig. [1](#fig:teaser){reference-type="ref" reference="fig:teaser"}.

Additionally, we successfully employed our approach to online trajectory planning on a real MAV. For details on the integrated system and corresponding experiments, we refer to [@schleich2021icuas].

::::: {#fig:trajectories .figure}
::: center
![](Schleich2021Searchbased_figs/trajectories_new.png){width="40%"}
:::

::: caption
Trajectories from online replanning (top-down view). Obstacle heights are represented by the color, reaching from purple (low) to blue (high). The trajectory of MRes~variable~ is shown in red, the trajectory from uniform planning in black. The start position is marked by the red circle and the goal by a green square. Start positions of replanning steps are marked with red and gray squares. The initially unknown obstacles are circled.
:::
:::::

# Conclusion {#sec:conclusion}

In this paper, we introduced high-dimensional local multiresolution state lattices. MAV velocities are directly incorporated into the planning to generate dynamically feasible trajectories. We showed that multiresolution combined with standard A\* search might result in higher planning times compared to uniform state lattices. However, in combination with a level-based expansion scheme, multiresolutional state lattices significantly reduce the maximal planning times, while only moderately increasing trajectory costs. For some challenging tasks, planning times still exceed 1 s, but our approach was able to maintain a replanning frequency of 1 Hz for most cases. In summary, we demonstrated how multiresolution can increase the applicability of search-based high-dimensional trajectory planning for large dynamic environments.

[^1]: All authors are with the Autonomous Intelligent Systems group, University of Bonn, Germany; `schleich@ais.uni-bonn.de`

[^2]: This work has been funded by the German Federal Ministry of Education and Research (BMBF) in the project "Kompetenzzentrum: Aufbau des Deutschen Rettungsrobotik-Zentrums (A-DRZ)".
