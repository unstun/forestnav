---
citation_key: Ren2022Bubble
arxiv_id: 2202.12177
arxiv_url: https://arxiv.org/abs/2202.12177
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:17:10Z
origin: ai+web
reviewed: false
---

# Introduction

Quadrotors are proved to be one of the most agile platforms which perform increasingly complex missions in different scenarios. However, high-speed flight in unknown environments is still an open problem. The limits on payload and onboard sensing make this task especially challenging for aerial robots [@tordesillas2021faster]. To achieve high-speed flights, trajectory planning is of vital importance to ensure the safety (i.e., collision avoidance [@huang2019collision]), smoothness, and fast maneuvers facing unknown obstacles.

High-speed trajectory planning in unknown environments is a great challenge, especially in the replanning phase where the high quadrotor speeds require extremely agile maneuvers to avoid newly-sensed obstacles. Existing (re-)planning methods [@zhou2019robust; @liu_sfc; @tgk_planner] typically consist of a frontend that aims to find a guiding path (or flight corridor) and a backend that smooths the trajectory around the guiding path (or optimizes a smooth trajectory within the corridor). The main difficulty in this framework is how to design the frontend such that the replanned guiding path (or flight corridor) is feasible: at least one dynamically-feasible and obstacle-free solution can be found in the backend optimization. A poorly-designed frontend may leave too little space for the quadrotor to avoid obstacles (*e*.*g*., decelerate or make turns), hence leaving no dynamically feasible solution in the subsequent trajectory optimization. Another difficulty is the backend optimization, which needs to perform both temporal and spatial deformation in an efficient manner such that the maximal speed can be attained.

:::: {#fig:fig1 .figure latex-placement="t"}
![](Ren2022Bubble_figs/fig1.png){width="40%"}

::: caption
High-speed navigation in the wild. (a) The generated point cloud map during the flight. (b) Composite images of the same flight. (c) The generated sphere-shaped flight corridor. Video is available at <https://youtu.be/7tQCV6KBzSY>
:::
::::

:::: {#fig:real_vel .figure latex-placement="t"}
![](Ren2022Bubble_figs/fig2.png){width="40%"}

::: caption
Comparison of the maximum speed in real-world experiments (the flight speed of other methods are read from their original papers). The Faster\* [@tordesillas2021faster] baseline uses a motion capture system as state feedback and a depth camera to detect obstacles. The proposed method and SFC [@liu_sfc] use a LiDAR with IMU for navigation while NanoMap [@florence2018nanomap], Learning [@loquercio2021learning], TGK-Planner [@tgk_planner] use a RGB-D camera with IMU. All of the above methods except Faster are performed in real-world forests, and Faster is tested in an indoor artificial environment. Our approach reaches a maximum speed of over $13.7~m/s$.
:::
::::

In this paper, we propose a robust and efficient motion planning algorithm to address the above issues systematically. The overall algorithm is based on a corridor approach. In the backend, we adopt a state-of-the-art minimum control effort optimization (MINCO) framework [@wang2022geometrically] to deform the trajectory temporal and spatial parameters efficiently. Our contribution in this paper mainly lies in the frontend, including:

- A novel sampling-based corridor generation method that preserves large corridor volume by considering the size of each sphere and their overlapped spaces. The increased corridor volume allows more space for the quadrotor to maneuver (hence succeed) at high speeds.

- A *Receding Horizon Corridors* (RHC) scheme that reuses corridors in the previous planning cycle. Specifically, in each replan, the first part of the flight corridor is directly from the previous planning cycle, and the second part is generated according to newly-sensed obstacles. This receding scheme ensures the corridor in each replan always contains sufficient space for the quadrotor to maneuver from its current state, significantly improving the replan process's success rate and convergence speed under high-speed flight.

- A real-time planning system that integrates these two designs of frontend with the MINCO backend [@wang2022geometrically]. A comprehensive benchmark comparison and an ablation study are conducted in simulation to show the superiority of our system and the effectiveness of the two designs.

- Implementation and validation the proposed method on a fully autonomous quadrotor system. Multiple real-world tests show that our methods achieve flight speeds over $13.7~m/s$ (see Fig. [1](#fig:fig1){reference-type="ref" reference="fig:fig1"}).

# Related Works

## High-Speed Navigation in the Wild

Various approaches have been proposed to enable autonomous quadrotor flights in unknown environments. Florence *et al*.  [@florence2020integrated] propose a reactive planner, which takes depth image as input and selects the best trajectory from a pre-built motion primitives library. The work in [@florence2018nanomap] proposes an uncertainty-aware lazy search map called NanoMap on the reactive controller and achieves a maximum flight speed of $10~m/s$. Although it has a low computation complexity, the pre-built set of motion primitives is relatively small, making it difficult to cover fine maneuvering skills that are necessary when the quadrotor is facing new, unexpected obstacles during high-speed flights. Similar motion primitive-based method is used (as a frontend) by Zhou *et al*. [@zhou2019robust], Liu *et al*. [@liu2017search], Zhang *et al*. [@zhang2020falco] and Kong *et al*. [@kong2021avoiding], which therefore suffer from similar drawbacks. Ye *et al*. [@tgk_planner] utilizes a frontend based on RRT\* kinodynamic sampling. Similar to the motion primitive methods, the sampled states are usually in low dimensions (*e*.*g*., position and velocity) and few in numbers in order to ensure sufficient computation efficiency, making it very difficult to produce fine quadrotor maneuvers in high-speed flights. Unlike the previous methods [@tgk_planner; @zhou2019robust; @liu_sfc], which typically have a frontend planning a rough path from the quadrotor's current position to the target one and a backend which further refines the trajectory by optimization, Zhou *et al*. [@zhou2020ego] proposed to plan a whole trajectory without considering any obstacle in the first stage and then locally modify the trajectory to fly around the detected obstacles. The local trajectory modification is achieved efficiently by directly incorporating a repulsive force from obstacles in the trajectory optimization cost function. The repulsive force is similar to a coarse-level distance field and hence suffers from the local minimum problem, hence unsuitable for high-speed trajectory planning. Another interesting method is proposed by Loquercio *et al*. [@loquercio2021learning], they use imitation learning to generate a trajectory directly from the depth image and current state. Limited by the sensing range and noise, the success rate of their methods decreases when forward speed is over 10 $m/s$. Compared with the methods mentioned above, our method achieves much higher flight speed in both simulation and experiments (see Fig. [2](#fig:real_vel){reference-type="ref" reference="fig:real_vel"}).

## Corridor-based Trajectory Planning

Corridor-based trajectory planning methods, which use geometrical shapes to represent free space, have been popular in recent years. Chen *et al*. [@chen2015real] build a discrete graph from an OctoMap structure [@hornung2013octomap] and directly use free cubes in OctoMap as the corridor constraints. Liu *et al*. [@liu_sfc] use polyhedrons to represent the free space, also called convex decomposition. Each cube or polyhedron on the flight corridor then imposes multiple linear hyperplane constraints in the subsequent trajectory optimization. Sphere-shaped corridors are also very commonly used. Compared with polyhedrons, a sphere imposes only one constraint in the trajectory optimization. It can often be quickly obtained by *Nearest Neighbor Search* (NN-Search) using a KD-Tree structure. Gao *et al*. [@gao2019flying] propose a sphere-shaped corridor generation scheme under the RRT\* framework. Ji *et al*. [@ji2021mapless] propose a forward-spanning-tree-based spherical corridor generation scheme. These two methods can generate corridors in a relatively short time. However, their corridor generation process only considers the connectivity of adjacent spheres. The found spheres often have small overlaps between adjacent ones, which over constrains the subsequent trajectory optimization and leaves tiny space for the quadrotor to maneuver at high speeds. Another problem is the lack of explicit consideration of the quadrotor's current speed, the resultant flight corridor often does not contain sufficient space for the quadrotor to maneuver from its current speed. The two problems will considerably reduce the feasible solution space and cause the backend optimization to fail. In contrast, our frontend attempts to find large individual spheres and their overlaps, while the receding scheme automatically incorporates the quadrotor current speed in each replan. These two designs greatly improve the success rate and convergence speed of the subsequent trajectory optimization.

Trajectory optimization with the corridor constraint is also well studied by some recent works. Ji *et al*. [@ji2021mapless] use an alternating minimization method [@am_traj] and iteratively insert waypoints to ensure that the trajectory completely falls in the corridor. However, the waypoints are selected heuristically, which leads to sub-optimal solutions. Mellinger *et al*. [@mellinger2011minimum] use piece-wise polynomial to represent the trajectory and generate a minimum-snap trajectory by solving a quadratic programming (QP) problem. The corridor constraints are used as inequality constraints in the QP. Gao *et al*. [@gao2019flying] use B-spline to represent trajectories and formulate the corridor constraints and trajectory optimization into a second-order cone programming (SOCP) problem. Both methods solve the optimization problem with hard constraints and have quite significant computation time. Our approach is most similar to [@wang2022geometrically]. The corridor constraints are first eliminated by a $C^2$-continuous barrier function. Then, a spatial-temporal deformation is performed. The optimization problem is finally turned into an unconstrained one that can be solved by Quasi-Newton methods efficiently and robustly.

# Preliminaries {#sec:minco}

:::: {#fig:poly_traj .figure latex-placement="t"}
![](Ren2022Bubble_figs/poly_traj.png){width="40%"}

::: caption
The whole trajectory is composed of $M$ pieces, contained in their respective sphere. The green areas $\mathcal B_i$ are the spheres. The orange points $q_i$ are the intermediate waypoints, which are always constrained in the intersecting space of two adjacent spheres. $T_i$ is the time allocation of each piece. $\mathbf d_0,\mathbf d_g$ are the given initial and goal states.
:::
::::

In this section, we briefly go through the backend trajectory optimization used in our algorithm. We model the quadrotor to a non-linear dynamic system following [@mellinger2011minimum], which is proved to be differential flat with flat output $\sigma = [x,y,z,\psi]^T$ with $p = [x,y,z]^T$ the quadrotor position in the world frame and $\psi$ the yaw angle. Due to the differential flatness, it is sufficient to plan the flat output trajectory $\sigma(t)$. In this work, we only plan the position trajectory $p(t)$ and specify the yaw angle trajectory $\Phi(t)$ as the tangent direction of $p(t)$ such that the quadrotor is always facing forward during a flight.

As shown in Fig. [3](#fig:poly_traj){reference-type="ref" reference="fig:poly_traj"}, given a flight corridor $\mathcal B$ that consists of a sequence of overlapping spheres (each is denoted by $\mathcal{B}_i, i = 1, \cdots, M$, see Sec. [4.1](#sec:sfc){reference-type="ref" reference="sec:sfc"}), the goal of the trajectory optimization is to find a smooth trajectory $p(t): [0, t_M] \mapsto \mathbb{R}^3$ over time duration $t_M$ that connects the initial position $q_0 \in \mathbb{R}^3$ at time zero to the terminal one $q_M \in \mathbb{R}^3$ at time $t_M$ and is completely contained in the sphere-shaped corridor $\mathcal B$.

In practice, the smoothness of the trajectory is quantitatively represented by the magnitude of its $s$-th order derivative $\| p^{(s)}(t) \|_2^2$ ($s=4$ in experiments). Moreover, the trajectory $p(t)$ is usually decomposed into $M$ pieces, each piece $p_i(t)$ is contained in sphere $\mathcal{B}_i$ for the time period $t \in [t_{i-1}, t_i]$, *i*.*e*., $$\begin{equation}
 p(t) = p_i(t - t_{i-1}) \in \mathcal{B}_i, t \in [t_{i-1}, t_i]
\end{equation}$$

Adjacent trajectory pieces $p_{i}(t)$ and $p_{i+1}(t)$ should meet at the same point $q_i \in \mathbb{R}^3$ at time $t_i$. Moreover, the trajectory $p(t)$ should start at a given initial state $\mathbf{d}_0$ (up to $(s-1)$-th order derivative) and terminate at a given goal state $\mathbf{d}_g$ (up to $(s-1)$-th order derivative). Considering these constraints and kinodynamic constraints (*e*.*g*., speed and acceleration), the trajectory optimization can be formulated as $$\label{eq:optimization}
 \begin{alignat}{4}
 \min\limits_{p(t)} & \int_{0}^{t_{M}} \| p^{(s)} (t) \|_2^2 dt + \rho_T t_M \label{eqa:obj_a}\\ 
 s.t.~~&p^{(0:s-1)}(0) = \mathbf{d}_0, p^{(0:s-1)}(t_M) = \mathbf{d}_g \label{eqa:obj_b}\\
 & p(t_i) = q_i, \forall 1 \leq i < M \label{eqa:obj_c} \\ 
 & t_{i-1} < t_i, \forall 1 \leq i \leq M \label{eqa:obj_d} \\
 &\|p^{(1)}(t) \|_2^2 \leq v_{max}^2, \|p^{(2)}(t) \|_2^2 \leq a^2_{max}, \label{eqa:obj_e} \\
 & p(t) = p_i(t-t_i) \in \mathcal{B}_i, \forall 1\leq i \leq M, t \in [t_{i-1}, t_i] \label{eqa:obj_f}
 \end{alignat}$$ where $\rho_T$ is the weight penalizing the total trajectory time $t_M$ such that the maximal allowed speed $v_{max}$ can be attained.

The optimization in ([\[eq:optimization\]](#eq:optimization){reference-type="ref" reference="eq:optimization"}) can be solved in two steps: in the first step, we fix the intermediate way point $\mathbf q = (q_1,\dots,q_{M-1})$ and time allocation vector $\mathbf T = (T_1,\dots,T_{M})$, where $T_i \triangleq t_{i} - t_{i-1} > 0$, and optimize only the first part (*i*.*e*., the smoothness) of ([\[eqa:obj_a\]](#eqa:obj_a){reference-type="ref" reference="eqa:obj_a"}) considering only the constraints in ([\[eqa:obj_b\]](#eqa:obj_b){reference-type="ref" reference="eqa:obj_b"}) and ([\[eqa:obj_c\]](#eqa:obj_c){reference-type="ref" reference="eqa:obj_c"}). Shown in [@wang2022geometrically], this optimization problem leads to an optimal solution where each piece $p_i(t)$ is a $(2s-1)$-th order polynomial and its coefficients are uniquely determined from $(\mathbf q, \mathbf T)$, *i*.*e*., $$\begin{equation}
\label{eq:minco_trajectory}
 p_i(t) = \mathbf c_i(\mathbf q, \mathbf T)^T \beta(t), t \in [0, T_i]
\end{equation}$$ where $\mathbf c_i \in \mathbb R^{2s\times 3}$ is the coefficient matrix depending on $(\mathbf q, \mathbf T)$ and $\beta(t)= [1 ,t,\dots , t^{2s-1}]^T$ is the time basis function.

In the second step, the complete problem in ([\[eq:optimization\]](#eq:optimization){reference-type="ref" reference="eq:optimization"}) is optimized from the class of trajectories parameterized in ([\[eq:minco_trajectory\]](#eq:minco_trajectory){reference-type="ref" reference="eq:minco_trajectory"}). Since the trajectory in ([\[eq:minco_trajectory\]](#eq:minco_trajectory){reference-type="ref" reference="eq:minco_trajectory"}) naturally satisfies the constraints in ([\[eqa:obj_b\]](#eqa:obj_b){reference-type="ref" reference="eqa:obj_b"}) and ([\[eqa:obj_c\]](#eqa:obj_c){reference-type="ref" reference="eqa:obj_c"}), the complete optimization only needs to consider the constraints in ([\[eqa:obj_d\]](#eqa:obj_d){reference-type="ref" reference="eqa:obj_d"}-[\[eqa:obj_f\]](#eqa:obj_f){reference-type="ref" reference="eqa:obj_f"}). Even this, the constrained optimization is typically time-consuming. To address this issue, the MINCO framework [@wang2022geometrically] transforms it into an unconstrained optimization problem detailed as follows. First, the time constraints in ([\[eqa:obj_d\]](#eqa:obj_d){reference-type="ref" reference="eqa:obj_d"}) are equivalent to $T_i > 0$, which can be parameterized as $T_i = e^{\tau_i}, 1 \leq i \leq M$ that always satisfies ([\[eqa:obj_d\]](#eqa:obj_d){reference-type="ref" reference="eqa:obj_d"}) for $\tau_i \in \mathbb{R}$. Then, the feasibility constraints ([\[eqa:obj_e\]](#eqa:obj_e){reference-type="ref" reference="eqa:obj_e"}) and ([\[eqa:obj_f\]](#eqa:obj_f){reference-type="ref" reference="eqa:obj_f"}) can be softly penalized in the cost function by a $C^2$-continuous barrier function [@wang2021robust]: $$\begin{equation}
 \mathcal L_\mu (x) = \begin{cases}0 & \text { if } x \leq 0, \\ (\mu-x / 2)(x / \mu)^{3} & \text { if } 0<x<\mu, \\ x-\mu / 2 & \text { if } x \geq \mu .\end{cases}
\end{equation}$$ where $\mu$ is a constant smoothness factor (0.02 in this paper), thus a finite weight for penalty can enforce the constraint at any specified precision. As a consequence, the optimization in ([\[eq:optimization\]](#eq:optimization){reference-type="ref" reference="eq:optimization"}) can be turned to an unconstrained form as: $$\begin{equation}
 \label{eqa:obj}
 \begin{aligned}
 \min\limits_{\boldsymbol{\tau},\mathbf q} \mathcal J &=\sum\limits_{i=1}^M \left( \int_{0}^{T_i} \| p_i^{(s)}(t) \|_2^2 dt + \rho_T e^{\tau_i} \right) \\
 % vel rate 
 + &{{\rho_{\mathrm{vel}} \sum\limits_{i=1}^M}\int_{{0}}^{T_i}\mathcal L_\mu\left( 
 \|p^{(1)}_i(t) \|_2^2 - v_{max}^2
 \right) \mathrm dt}\\
 % acc max 
 + &{{\rho_{\mathrm{acc}} \sum\limits_{i=1}^M}\int_{0}^{T_i}\mathcal L_\mu\left( 
 \|p^{(2)}_i(t) \|_2^2 - a_{max}^2
 \right) \mathrm dt}\\
 % collision free
 + &{{\rho_{\text{c}} \sum\limits_{i=1}^M}\int_{0}^{T_i}\mathcal L_\mu\left( 
 \|p_i(t) - {o_i} \|_2^2- r_i
 \right) \mathrm dt}
 \end{aligned}
\end{equation}$$

where $\rho_{\mathrm{vel}},\rho_{\mathrm {acc}},\rho_{\text{c}}$ are the corresponding weight of maximum speed, maximum acceleration and collision-free penalty, and $o_i$ is the center and $r_i$ is the radius of the $i$-th sphere. As shown in [@wang2022geometrically], all gradient of the objective ([\[eqa:obj\]](#eqa:obj){reference-type="ref" reference="eqa:obj"}) with respect to waypoints $\mathbf q$ and time allocation $\boldsymbol{\tau}$ can be computed analytically, so a Quasi-Newton method (*i*.*e*. LBFGS[^3]) is used to solve the optimization problem effectively.

# Planner

In this section, we present the frontend design that enables high-speed trajectory optimization, which is the main contribution of this paper.

## Sphere-Shaped Corridor {#sec:sfc}

As shown in Fig. [4](#fig:bubble_def){reference-type="ref" reference="fig:bubble_def"}, a sphere is defined by its center $o\in\mathbb R^3$, the nearest obstacle point $n \in\mathbb R^3$, and the radius: $$\begin{equation}
 \label{eqa:radi}
 r = \left\| o - n\right\|_2 - r_d
\end{equation}$$ where $r_d$ is the radius of the drone. During the trajectory optimization process, each piece of trajectory is constrained in the corresponding sphere to satisfy safety constraints.

:::: {#fig:bubble_def .figure latex-placement="htpb"}
![](Ren2022Bubble_figs/bub_def.png){width="35%"}

::: caption
The definition of one sphere and a piece of trajectory in it. $q_s,q_e$ are the start and end point of the trajectory and $T$ is the time allocation. $o$ is the center of the sphere and $n$ is the nearest obstacle point.
:::
::::

To generate a new sphere, we first build a KD-Tree with the obstacle point cloud. Then, for a given center of the sphere $o$, a nearest neighbor search (NN-Search) is performed on that KD-Tree to find the nearest obstacle point $n$, which then determines the radius as in ([\[eqa:radi\]](#eqa:radi){reference-type="ref" reference="eqa:radi"}). We call this process **GenerateOneSphere**$(o)$, which will be used in the sequel.

## Flight Corridor Generation {#sec:genbub}

The main workflow of the flight corridor generation is described in Alg. [\[alg:genbubs\]](#alg:genbubs){reference-type="ref" reference="alg:genbubs"}, where a complete flight corridor $\mathcal{B}$ is generated from the given initial position ${p}_0$, goal position ${p}_g$, and a global guide path $\mathcal T$ generated by A\*[@astar]. The algorithm initializes with a largest possible sphere $\mathcal B_{cur}$ around the initial position ${p}_0$ (Line 2-3). Then, in Line [\[alg:genbubs:getforward\]](#alg:genbubs:getforward){reference-type="ref" reference="alg:genbubs:getforward"}, a local guide point $p_h$ is selected from the guide path $\mathcal T$, which is the nearest point out of the current sphere $\mathcal B_{cur}$, and a new sphere is generated by **BatchSample**($p_h, \mathcal{B}_{cur}$) (Sec. [4.2.1](#sec:batch_sample){reference-type="ref" reference="sec:batch_sample"}) and added to $\mathcal B$. This process repeats until the goal position $p_g$ is included in the new generated sphere (Line 8-10).

With the found flight corridor $\mathcal{B}$, the initial waypoint position $\mathbf q$ and time allocation $\mathbf{T}$ are initialized by the function **WaypointAndTimeInitialization** ($\mathcal B$)(Sec. [4.2.2](#sec:tpallo){reference-type="ref" reference="sec:tpallo"}) and then optimized in the backend (Sec. [3](#sec:minco){reference-type="ref" reference="sec:minco"}).

::: algorithm
**Notation**: The flight corridor $\mathcal B$; global guide path $\mathcal{T}$; Initial and goal position: $p_0, p_g$; local guide point $p_h$\
[]{#alg:genbubs_init label="alg:genbubs_init"} Initialize $\mathcal{B}_{cur}$ = GenerateOneSphere($p_0$) $\mathcal B$.PushBack($\mathcal{B}_{cur}$) []{#alg:genbubs_end_while label="alg:genbubs_end_while"}

WaypointAndTimeInitialization($\mathcal B$)
:::

### Batch sample {#sec:batch_sample}

The problem of trajectory optimization under flight corridor constraints is highly non-convex, which means overly conservative constraints may lead to local-minimum or even infeasible solution when the quadrotor initial speed is high. Existing methods [@gao2019flying; @ji2021mapless] only considered the connectivity between two adjacent spheres. To preserve larger space for the quadrotor to maneuver hence improve the feasibility of the trajectory optimization ([\[eqa:obj\]](#eqa:obj){reference-type="ref" reference="eqa:obj"}) at high-speeds, we propose a novel batch sample method to generate a high-quality corridor. We consider this problem in the following aspects: **(a)** the volume of each sphere: a sphere with larger size can better approximate the real free space with fewer number of spheres, making the optimization problem less constrained, **(b)** the volume of the overlapped spaces between two adjacent spheres: as discussed in Sec. [3](#sec:minco){reference-type="ref" reference="sec:minco"}, all waypoints of the trajectory are constrained in the intersecting space, a larger intersecting space means more freedom for the optimization process.

:::: {#fig:samp .figure latex-placement="ht"}
![](Ren2022Bubble_figs/batch_sample.png){width="45%"}

::: caption
The green circle $\mathcal{B}_f$ is the sphere generated in last round of batch sample. The yellow point is the guide point $p_h$. The purple points are the sampled points according to the probability distribution represented by the orange-shaded area. The blue circle is the best sphere in this round.
:::
::::

::: algorithm
[]{#alg:batchsample label="alg:batchsample"} **Notation**: Last sphere $\mathcal B_f$; Guide point $p_h$; Best sphere in this round $\mathcal B_{best}$; Random sampler $\mathcal S$; Maximum sample num $K$; Safe distance $r_d$; Priority queue sorted by sphere's score: $\mathcal{Q}$;\
Initialize: $\mathcal S$.init($\mathcal B_f$, $p_h$), $k=0$ []{#alg:batchsample_init label="alg:batchsample_init"} []{#alg:samp_while_end label="alg:samp_while_end"} ()$\mathcal{Q}.empty()$ return BatchSampleFailed $\mathcal B_{best}$ = $\mathcal{Q}$.top()
:::

The sampling process is shown in Alg. [\[alg:batchsample\]](#alg:batchsample){reference-type="ref" reference="alg:batchsample"}. We first initialize the sampler $\mathcal S$ in Line [\[alg:batchsample_init\]](#alg:batchsample_init){reference-type="ref" reference="alg:batchsample_init"}. As shown in the orange area of Fig. [5](#fig:samp){reference-type="ref" reference="fig:samp"}, the sampler generates a random candidate point $p_{cand}\in \mathbb R^3$ under a 3D Gaussian distribution $N(\mu,\Sigma)$, where the mean is set at the guide point $\mu = p_h$ and the covariance is set as $\Sigma = \text{diag} \left(\sigma_x, \sigma_y, \sigma_z \right)$, $\sigma_x = \frac{1}{3}\left\| o_f - p_h \right\|_2, \sigma_z = \sigma_y = 2\sigma_x$, where $o_f$ is the center of last sphere and the $\sigma_x$ direction is aligned with the direction of $o_f-p_h$.

Then in Line [\[alg:samp_while\]](#alg:samp_while){reference-type="ref" reference="alg:samp_while"}-[\[alg:samp_while_end\]](#alg:samp_while_end){reference-type="ref" reference="alg:samp_while_end"}, a total number of $K$ points (called a batch) are randomly sampled with $\mathcal S$, each has its score computed by the function **ComputeScore**($\mathcal B_{cand}$) defined below: $$\begin{equation}
 \label{eqa:heu}
 \begin{aligned}
 \text{Score} &= \rho_r V_{\text{cand}} + \rho_v V_{\text{inter}}
 %+\rho_a \arccos\left( \frac{v_1\cdot v_2}{||v_1||\cdot ||v_2||}\right)\\
 \end{aligned}
\end{equation}$$ where $\rho_r,\rho_v \in \mathbb R_+$ are positive weights, $V_{\text{cand}}$ is the volume of the candidate sphere $\mathcal B_{cand}$ and $V_{\text{inter}}$ is the overlapped volume between $\mathcal{B}_{cand}$ and $\mathcal{B}_f$. Finally, the best sphere with the highest score is selected in Line 13.

As shown in Fig. [6](#fig:bub_cmp){reference-type="ref" reference="fig:bub_cmp"}, compared with Gao [@gao2019flying], the proposed method can better approximate the real free space with fewer spheres and larger sphere sizes. Furthermore, our algorithm has lower computational complexity than Gao's approach, which uses an RRT-like method and takes samples from the whole space. Our process follows a coarse-to-fine manner, where we first use A\* to find the shortest path and then take batch samples only around this path. In this way, the sample space, hence computation time, is significantly reduced. We test 100 times in the same environment shown in Fig. [6](#fig:bub_cmp){reference-type="ref" reference="fig:bub_cmp"}. The proposed method only takes an average $0.74~ms$ to generate the corridor, while Gao's method takes an average $100~ms$.

:::: {#fig:bub_cmp .figure latex-placement="t"}
![](Ren2022Bubble_figs/bub_cmp.png){width="40%"}

::: caption
Corridor generation comparison. (a) The corridor generated by our proposed method in one test (b) The corridor generated by Gao *et al*. [@gao2019flying] in the same test. (c) The comparison of overlapped volume between two adjacent spheres over 100 tests. (d) The volume of each sphere over 100 tests. The shaded area denotes the maximum and minimum value over 100 tests.
:::
::::

### Waypiont and Time Initialization {#sec:tpallo}

For a given flight corridor $\mathcal{B}$, we adopt a *Default Initialization* strategy, where the waypoint are initialized as the center of the overlap space between two adjacent spheres (pink points in Fig. [7](#fig:rhp){reference-type="ref" reference="fig:rhp"}(b)), and the time allocation is initialized as $T_i = \frac{\left\| q_{i} - q_{i-1}\right\|_2}{v_{max}}$.

:::: {#fig:rhp .figure latex-placement="htbp"}
![](Ren2022Bubble_figs/rhc.png){width="40%"}

::: caption
The receding horizon corridors strategy. (a) The green and pink dashed circle are respectively the planing horizon in last and current replan. (b) The pink point is the center of the overlap area, which is used by the *Default Initialization*. (c) Spherical corridor in green are previously generated, using the *Hot Initialization*. And corridor in blue are newly generated, using the *Default Initialization*.
:::
::::

## Receding Horizon Corridors in Replan {#sec:rhc}

During a high-speed flight in an unknown environment, the quadrotor needs to replan frequently to avoid newly sensed obstacles. We use a distance-triggering replaning strategy. Specifically, the trajectory is planned (both frontend corridor generation and backend optimization) in a fixed distance $D$ (*i*.*e*. planning horizon) depending on the sensing range. Denote the position of last replan as $p_{last}$ and current quadrotor position as $p_{curr}$. The replan process is triggered if $\left\|p_{last} - p_{curr}\right\|_2>\gamma \cdot D$, where $\gamma \in [0,1]$ is a constant ratio. In this way, as the drone moves forward, the newly sensed obstacle can be actively handled by the replan process. A replan is also triggered when the current trajectory under execution is found to collide with any obstacles.

A major challenge in the replan occurs when the quadrotor speed is high, which requires sufficient space for the quadrotor to maneuver such that the newly sensed obstacles can be avoided successfully. Corridor generation without considering the quadrotor's current state [@liu_sfc; @gao2019flying; @ji2021mapless] often causes too small feasible region in the trajectory optimization ([\[eq:optimization\]](#eq:optimization){reference-type="ref" reference="eq:optimization"}), which is difficult (or even impossible) to solve (*e*.*g*., by optimizing ([\[eqa:obj\]](#eqa:obj){reference-type="ref" reference="eqa:obj"})). Another problem is that with the increase of the current speed, the objective function becomes highly non-convex. As described in Sec. [3](#sec:minco){reference-type="ref" reference="sec:minco"}, our optimization problem is turned into an unconstrained one. The non-convexity of the objective function may cause the optimization with the *Default Initialization* to easily stuck at a bad local minimum which violates the collision-free or kinodynamic constraints.

We solve these problems by a *Receding Horizon Corridors* (RHC) strategy shown in Fig. [7](#fig:rhp){reference-type="ref" reference="fig:rhp"}. The key is to reuse a few spheres from the previous planning cycle in current replan. Concretely, when a new replan is triggered, the nearest future waypoint $\mathbf d_{rp}$ in $\mathbf{q}$ is selected as the initial state. A few spheres after $\mathbf d_{rp}$ will be reused to constitute the first part of the new corridor, followed by newly generated spheres reaching the current planning horizon $D$. This receding scheme ensures the corridor in each replan always contains sufficient space for the quadrotor to maneuver from its current state (since the current quadrotor state is on the previous trajectory, which is contained in the previous corridor), hence significantly enlarging the feasible region in the backend trajectory optimization. In experiments, we reuse spheres that fall within a certain distance (*e*.*g*., $3m$) of the current quadrotor position $p_{curr}$. Furthermore, to speed up the trajectory optimization and mitigate the local minimum issue, the waypoints $\mathbf q$ and time allocation $\mathbf T$ contained in the reused corridor, which were optimized in the previous planning cycle, are used to initialize the current trajectory optimization (*i*.*e*. *Hot Initialization*). The waypoints and time allocation in the newly generated spheres are still initialized by the default scheme (Sec. [4.2.2](#sec:tpallo){reference-type="ref" reference="sec:tpallo"}).

# Experiments

## Benchmark Comparison {#sec:bench}

:::: {#fig:limit .figure latex-placement="htbp"}
![](Ren2022Bubble_figs/compare_with_uzh.png){width="40%"}

::: caption
\(a\) The executed trajectory in Loquercio *et al*. [@loquercio2021learning]. (b) The executed trajectory with the proposed method is colored with forward speed from $0~m/s$ to $15~m/s$. The yellow star is the initial position of the drone, and the green points are the simulated LiDAR points.
:::
::::

In this section, we compare the proposed method with a most recent planning work based on imitation learning [@loquercio2021learning] (Learning), and two model-based planning methods evaluated by it, including a frontend-backend type optimization-based method from Zhou *et al*. [@zhou2019robust] (FastPlanner) and a reactive planner designed for the high-speed flight from Florence *et al*. [@florence2020integrated] (Reactive). We evaluate the performance of our method in a simulated forest environment used by the learning method. Due to the unavailability of the simulation environment used by the original work [@loquercio2021learning], we reproduce the environment according to their description. Specifically, the forest has trees distributed in a rectangular region $R(l,w)$ of width $w$ and length $l$, the origin lies in the center of $R$. Trees are randomly placed according to a homogeneous Poisson point process $P$ with the intensity $\delta~tree/(m^2)$. The sensor input in the simulation includes a simulated LiDAR point cloud, with the sensing range of $8~m$ at $30~Hz$ (see green points in Fig. [8](#fig:limit){reference-type="ref" reference="fig:limit"}(b)). The quadrotor full state is assumed to be known to eliminate the influence of state estimation.

:::: {#fig:bench .figure latex-placement="htbp"}
![](Ren2022Bubble_figs/heatmap.png){width="40%"}

::: caption
The success rate comparison for different methods. The proposed method keeps a high success rate in all simulated test environments with varying forest densities.
:::
::::

:::: {#fig:ablation .figure latex-placement="t"}
![](Ren2022Bubble_figs/bench.png){width="100%"}

::: caption
The ablation study of the proposed method. The green line is the proposed method (*Ours(Front+MINCO+RHC)*). The blue line (*Gao*) is the original version of Gao *et al*.'s work [@gao2019flying]. The yellow line (*Gao+MINCO*) uses corridor generation from [@gao2019flying], but with trajectory optimization replaced by MINCO in Sec.[3](#sec:minco){reference-type="ref" reference="sec:minco"}. The purple line (*Ours(Front + MINCO)*) is our method without the RHC strategy. The red line (*Gao+MINCO+RHC*) uses Gao *et al*.'s corridor generation method and the same MINCO optimization and RHC strategy as ours.
:::
::::

We use exactly the same configuration in [@loquercio2021learning] to make a fair comparison: $w = 30~m$ and $l = 60~m$, and the start zone of the drone is at $(-{l}/{2}, 0)$, the goal position $({l}/{2}, 0)$. Three different tree densities with $\delta = {1}/{49}$ (low), $\delta = {1}/{36}$ (medium), and $\delta = 1/25$ (high) are tested. In each experiment, we use different random seed to generate different simulated maps. One flight is considered to be successful only if the drone reaches the goal without violating the velocity, acceleration, or collision-free constraints. The results are shown in Fig. [9](#fig:bench){reference-type="ref" reference="fig:bench"}. Similar to [@loquercio2021learning], we test our method 10 times in each different density or speed and compute the success rate of each, and the results of other baseline are directly obtained from [@loquercio2021learning]. Noting that in [@loquercio2021learning], the maximum mass-normalized thrust of the simulated drone is limited to $35.3~m/s^2$, while we limit our simulated drone to $15~m/s^2$. As can be seen, our approach outperforms others in all cases, even with a lower thrust limit. Moreover, compared with Loquercio *et al*. [@loquercio2021learning], the proposed method generates much smoother trajectories, which is usually easier to track (see Fig. [8](#fig:limit){reference-type="ref" reference="fig:limit"}).

## Ablation Study

To further validate each module of the proposed method, we compare our method in detail with Gao *et al*. [@gao2019flying], which generates sphere-shaped corridors in an RRT\* style and optimizes a minimal snap trajectory with fixed time allocation. We use the same simulated map configuration mentioned in Sec.[5.1](#sec:bench){reference-type="ref" reference="sec:bench"}, but further add tests with $\delta = 1/12$ (super high). The key three elements of our approach includes the trajectory optimization in Sec. [3](#sec:minco){reference-type="ref" reference="sec:minco"} (MINCO), the frontend corridor generation in Sec. [4.2](#sec:genbub){reference-type="ref" reference="sec:genbub"} (Front), and the receding horizon corridors strategy (RHC) in Sec. [4.3](#sec:rhc){reference-type="ref" reference="sec:rhc"}. A series of ablation studies are performed, and the results are shown in Fig. [10](#fig:ablation){reference-type="ref" reference="fig:ablation"}. *Gao* is the original version from [@gao2019flying]. This method fails to generate trajectory with speed over $2~m/s$ due to the inability to optimize time allocation in the backend. To fix this issue, we replace the backend of *Gao* by MINCO (*Gao+MINCO*) and compare it with our method without RHC strategy (*Ours (Front+MINCO)*). The performances of the two are very close, showing that MINCO can generate more aggressive trajectories and that our frontend alone does not improve the success rate much. Furthermore, we incorporate the RHC strategy to the method *Gao* (*Gao + MINCO + RHC*) and compare it with our full algorithm (with both frontend and RHC). As can be seen, each method with RHC has a significantly higher success rate at high speeds on all map densities, verifying the effectiveness of the RHC strategy. Moreover, our full algorithm with our frontend (*Ours(Front + MINCO + RHC)*) achieves a higher success rate than *Gao* with the same MINCO and RHC strategy (*Gao+MINCO+RHC*), showing the effectiveness of our frontend in the overall planning system.

## Run Time Analysis

In this section, we compare the run time of the proposed method with the baseline. We test our method both on the desktop computer, with a 2.90 GHz Intel i7-10700 CPU, and an onboard computer with a 1.1 GHz Intel i7-10710U CPU. The baseline FastPlanner [@zhou2019robust] and Gao [@gao2019flying] are tested on the same desktop computer. The test environment is a simulated forest with $\delta = \frac{1}{25}$ shown in Fig. [8](#fig:limit){reference-type="ref" reference="fig:limit"}(b). The computation time is divided into two parts: mapping and planning. For FastPlanner, the mapping process includes building a Euclidean signed distance field (ESDF), and planning includes frontend path-search and backend trajectory optimization. For Gao's method, the mapping process includes a static KD-Tree update, and the planning includes corridor generation and SOCP optimization. For the proposed method, the mapping includes the update of an OctoMap [@hornung2013octomap] (no ray-casting) and an incremental KD-Tree (*i*.*e*., ikd-tree [@cai2021ikd]). The planning includes frontend A\* search, corridor generation, and trajectory optimization. As shown in Table [1](#tab:run_time){reference-type="ref" reference="tab:run_time"}, the proposed method enjoys much lower computational complexity, which can replan at over $50~Hz$ even on the onboard platform.

::: {#tab:run_time}
+--------------------------------+------------+--------------+-----------------+--------------+---+---+
| Method                         | Components | $\mu$ \[ms\] | $\sigma$ \[ms\] | Total \[ms\] |   |   |
+:==============================:+:==========:+:============:+:===============:+:============:+:=:+:=:+
| Fast-Planner [@zhou2019robust] | Mapping    | 38.20        | 6.90            | 42.92        |   |   |
|                                +------------+--------------+-----------------+              +---+---+
|                                | Planning   | 4.72         | 1.60            |              |   |   |
+--------------------------------+------------+--------------+-----------------+--------------+---+---+
| Gao [@gao2019flying]           | Mapping    | 12.78        | 3.69            | 167.01       |   |   |
|                                +------------+--------------+-----------------+              +---+---+
|                                | Planning   | 154.23       | 40.60           |              |   |   |
+--------------------------------+------------+--------------+-----------------+--------------+---+---+
| **Ours**                       | Mapping    | 3.16         | 0.76            | **4.69**     |   |   |
|                                +------------+--------------+-----------------+              +---+---+
|                                | Planning   | 1.53         | 0.63            |              |   |   |
+--------------------------------+------------+--------------+-----------------+--------------+---+---+
| Ours (onboard)                 | Mapping    | 8.97         | 6.51            | 13.31        |   |   |
|                                +------------+--------------+-----------------+              +---+---+
|                                | Planning   | 4.34         | 2.33            |              |   |   |
+--------------------------------+------------+--------------+-----------------+--------------+---+---+

: Run Time Comparison
:::

## Real-world Experiments

::: {#tab:real_trajs}
            Executing time \[s\]   Length \[m\]   Average Vel. \[m/s\]   Max Vel.\[m/s\]     
  -------- ---------------------- -------------- ---------------------- ----------------- -- --
   Test1           15.59              111.18              7.05                8.02           
   Test2            5.81              41.61               6.97              **13.72**        
   Test3            5.69              40.65               6.92                12.00          
   Test4            6.16              34.63               5.47                8.80           
   Test5           17.21              79.17               4.54                5.01           
   Test6            9.90              42.75               4.23                6.54           
   Test7            9.60              58.65               6.01                7.00           
   Test8            6.99              37.55               5.21                7.05           
   Test9            6.02              45.72               7.34                11.64          
   Test10           5.70              29.39               5.01                7.00           
   Test11           5.40              45.08             **8.11**              12.00          

  : Detailed Profile of 11 Real-world Tests
:::

To verify our planning method in real-world environments, we build a LiDAR-based quadrotor platform. The platform has a total weight of $1.45~kg$ and can produce a maximum thrust over $60~N$, resulting in a thrust-to-weight ratio of $4.1$. For localization and mapping, we use the Livox Mid360 LiDAR and PixHawk flight controller's built-in IMU running FAST-LIO2 [@xu2022fast] (the sensors are initialized by LI-Init[@zhu2022robust]), which provides 100 $Hz$ high-accuracy state estimation and $25~Hz$ point cloud. The trajectory tracking controller is an on-manifold model predictive controller in [@lu2021model], the planning horizon is set to $D = 15~m$ and replan ratio $\gamma = 0.4$. All perception, planning, and control algorithm are running on an Intel NUC with CPU i7-10710U in real-time. We have done 12 experiments in a forest environment with maximal speed ranging from $5~m/s$ to $14~m/s$. All the experiments succeeded except one due to a controller failure. Fig. [11](#fig:all_real_traj){reference-type="ref" reference="fig:all_real_traj"} shows the experimental environment and all the trajectories colored by their speed. As can be seen, our planner is robust by accomplishing all the tests in the real-world environment. Fig. [1](#fig:fig1){reference-type="ref" reference="fig:fig1"} shows the third person of the quadrotor in one flight. More quantitatively, Table [2](#tab:real_trajs){reference-type="ref" reference="tab:real_trajs"} summarizes the detailed trajectory profiles including the trajectory executing time, total length, average and maximum speed. As can be seen, our method achieves an average speed up to $8.11m/s$ and a maximum speed of $13.7m/s$. To the best of our knowledge, this is the highest speed that a fully autonomous quadrotor can achieve in a real-world, cluttered, and unknown environment (see Fig. [2](#fig:real_vel){reference-type="ref" reference="fig:real_vel"}). More visual illustration of the experiments is shown in our video[^4].

Fig. [12](#fig:log){reference-type="ref" reference="fig:log"} shows the speed and acceleration profiles of two typical flights, called *Test 1* (long trajectory length) and *Test 2* (high flight speed). For *Test 1*, we limit the maximum speed to $8~m/s$ and the maximum acceleration to $8~m/s^2$. In *Test 2*, a more agile flight is performed where the maximum speed is $14~m/s$ and the maximum acceleration is $10~m/s^2$. As can be seen, both speed and acceleration constraints are well satisfied.

:::: {#fig:all_real_traj .figure latex-placement="t"}
![](Ren2022Bubble_figs/realworld_tests.png){width="40%"}

::: caption
Composite image of 11 real-world flight trajectories colored by their speed. Each experiment (trajectory) is conducted independently with real-time mapping. After all experiments, the executed trajectory along with the map built during each flight are registered together to produce this composite image. The tree crown are removed to better show the trajectories.
:::
::::

:::: {#fig:log .figure latex-placement="t"}
![](Ren2022Bubble_figs/plot_csv.png){width="45%"}

::: caption
The norm of velocity and acceleration. The executed trajectory of *Test 1* is about $111.18~m$, and *Test 2* is about $41.61~m$. The average speed is about $7~m/s$ for both test, and the maximum speed is over $13.7~m/s$ in *Test 2*.
:::
::::

# Conclusion and Future Work

In this paper, we propose a novel motion planning algorithm that generates smooth, collision-free, and high-speed trajectories in real-time. The whole planning system can work with fully onboard sensing, and computation at a replan frequency over $50~Hz$. To enable high-speed flight in the wild, we proposed two novel designs. One is a sampling-based sphere-shaped corridor generation method, which can generate high-quality corridors (*i*.*e*. larger size and bigger overlaps) in a relatively short time. Another is a *Receding Horizon Corridors* strategy, which fully utilizes previously generated corridors and the optimized trajectory. With these designs, the proposed method significantly increases the replan success rate in high-speed cases.

One limitation of our algorithm is that the reused corridors from last planning cycle are not guaranteed to be obstacle-free due to newly sensed obstacles that may be occluded in previous LiDAR measurements. This will cause the reused corridor to be discarded and hence occasionally lower the success rate when the environment is extremely cluttered. This limitation can be overcome by placing the first few corridors of a (re-)plan in known free spaces (instead of free and unknown spaces), so that these free corridors can be safely reused in the next planning cycle. Restraining the first few spheres in free spaces also enables the planning of a safe backup trajectory like [@tordesillas2021faster] which guarantees a safe flight. In the future, we will explore these designs and extend the method to more different missions and environments.

# Acknowledgment {#acknowledgment .unnumbered}

The authors gratefully acknowledge DJI for fund support and Livox Technology for equipment support during the whole project. The authors would like to thank Guozheng Lu and Wei Xu for the helpful discussions.

[^1]: \*These two authors contributed equally to this work.

[^2]: Y. Ren, F. Zhu, and F. Zhang are with the Department of Mechanical Engineering, University of Hong Kong `{renyf, zhufc}@connect.hku.hk, fuzhang@hku.hk`, W. Liu is with School of Electronics and Information Engineering, Harbin Institute of Technology, Shenzhen `180210215@stu.hit.edu.cn`, Z. Wang and F. Gao are with the College of Control Science and Engineering, Zhejiang University `{wangzhepei, fgaoaa}@zju.edu.cn` Y. Lin is with Dji Co. `ylinax@connect.ust.hk`.

[^3]: https://github.com/ZJU-FAST-Lab/LBFGS-Lite

[^4]: <https://youtu.be/7tQCV6KBzSY>
