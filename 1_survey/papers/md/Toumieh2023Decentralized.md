---
citation_key: Toumieh2023Decentralized
arxiv_id: 2304.09462
arxiv_url: https://arxiv.org/abs/2304.09462
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:45:51Z
origin: ai+web
reviewed: false
---

**video**: <https://youtu.be/eKwYNU1Q0wY>

# INTRODUCTION

## Problem statement

Multi-agent planning has been gaining in popularity in the research community due to recent advances. These advances are making it a viable solution to many commercial, industrial, and military applications. There are multiple challenges that face a multi-agent planning framework such as the problem of synchronizing agents for synchronous planning methods and dealing with communication latency. It is the purpose of this paper to extend upon our previous state-of-the-art work [@toumieh2022multi] that outperformed other state-of-the-art methods in computation efficiency, trajectory speed, and smoothness in a cluttered environment. We provide a new approach derived from [@toumieh2022multi] that is fully online and robust to arbitrary communication latency. We also study the effect of communication latency on the overall performance of our planner and compare it with other state-of-the-art methods.

## Related work {#sect:related_works}

### Multi-agent planning for multirotors

In [@Hoenig2018], the authors present a centralized multi-agent planning framework that uses time-aware Safe Corridors. The method has 3 sequential steps: roadmap generation, then discrete planning, and finally continuous refinement. The approach presented by the authors is centralized although some steps can be decentralized. While the computation time is not suitable for online high-speed planning and replanning, the method used served as an inspiration for many subsequent methods in the state-of-the-art. Such methods include [@Park2022] and [@toumieh2022multi] which in turn served as an inspiration for the work presented in this paper.

Buffered Voronoi Cells have been used by multiple works [@Zhu2019bvc], [@Zhou2017] for multi-agent collision avoidance but do not account for static obstacles. Other approaches [@Luis2019dmpc] use separating hyperplanes to avoid collisions between agents and model static obstacles in the form of ellipsoid constraints in a decentralized MPC formulation. The generation of ellipsoid representation of the environment is not trivial and is not addressed by the authors of [@Luis2019dmpc].

MADER, an asynchronous multi-agent planning framework has been proposed in [@tordesillas2020mader]. The method allows for avoiding static, and dynamic obstacles, as well as other planning agents. The authors combine a search-based approach with an optimization approach, where the output of the search-based approach is taken as initialization for the optimization problem. This choice was made since the optimization problem defined by the authors is non-convex and requires a good initial guess.

EGO-Swarm was proposed in [@Zhou2021EGOSwarmAF] as an asynchronous and decentralized trajectory planner. It requires each planning agent to broadcast its generated trajectory at a fixed frequency. When each agent receives the trajectories of other agents, it proceeds immediately to do a collision check. While the approach has been demonstrated in real-world experiments, it still suffers from collisions due to communication delays between agents.

In a similar fashion to [@Hoenig2018], the authors of [@Park2022] present a distributed and online trajectory generation framework for multi-agent quadrotor systems using time-aware Safe Corridors (or Linear Safe Corridors). The environment representation used by the authors is an octomap [@hornung2013octomap]. The Safe Corridor used to generate the time-aware Safe Corridor contains only one polyhedron which leads to slow and conservative trajectories.

In [@soria2021distributed], a decentralized model predictive control approach is used for collision avoidance and cohesive flight. The obstacles are described as mathematical functions (cylinders, paraboloids \...) in order to include them in the decentralized MPC formulation as constraints. It is however not trivial to describe an arbitrary cluttered environment through continuous mathematical functions that are easy to add as constraints to an MPC formulation.

Finally, in our previous work [@toumieh2022multi], we proposed a decentralized and synchronous planning framework that is inspired by [@Hoenig2018]. The approach takes into account static obstacles using Safe Corridors (generated from a voxel grid representation [@toumieh2020mapping]). Safe Corridors are then augmented to time-aware Safe Corridors to avoid intra-agent collisions. The proposed approach outperforms state-of-the-art methods in all performance metrics, including robustness, computation time, and trajectory speed.

### Latency robust multi-agent planning

The previously cited works do not account for communication delay, or can passively handle latency up to a fixed limit [@toumieh2022multi]. Some multi-agent planning frameworks take into account communication delay and will be presented in this section.

In [@senbaslar2022asynchronous], an asynchronous and decentralized trajectory planner is presented. The planner guarantees safety using separating hyperplanes from previous planning iterations. While the presented approach can handle communication delays, it does not account for any type of obstacles (static or dynamic), which limits its applicability to the real world.

Finally, RMADER (Robust MADER) is proposed in [@kondo2022robust], which is an extension of MADER [@tordesillas2020mader]. They convexify the optimization problem in order to improve the computation time. However, they inherit from MADER the polyhedral representation of the obstacles in the environment. This representation is not trivial to generate and can add significant overhead to the planning framework.

## Contribution

The main contribution of our paper is an improved decentralized and synchronous planning framework that is robust to communication latency. The proposed framework is built on our previous work [@toumieh2022multi] and conserves its advantages. Thus, the proposed method has low computation time and takes into account static obstacles and other planning agents. The improvements are:

1.  The addition of a mechanism to deal with arbitrary communication latency by dynamically adapting the planning frequency to avoid collisions and guarantee safety.

2.  The integration of 2 previously offline steps in [@toumieh2022multi] (global path generation step and Safe Corridor generation step) to make the framework fully online and suitable for real-world applications.

3.  The modification of the stalemate/deadlock resolution mechanism to guarantee safety.

The method is tested in simulations to show the effect of communication latency on the performance of the planner. It is also compared to 3 recent works: EGO-Swarm [@Zhou2021EGOSwarmAF], MADER [@tordesillas2020mader] and RMADER [@kondo2022robust] in terms of trajectory safety/performance as well as computation time.

# Assumptions {#sect:assumptions}

![We show the global pipeline of the planning framework of a single planning agent. It is run in a loop at a varying/adaptive frequency.](Toumieh2023Decentralized_figs/diagram.png){#fig:diagram width="100%"}

We assume perfect control (the controller executes the generated trajectory perfectly) and perfect localization (each agent can localize itself and other agents at any moment to an arbitrary accuracy). These assumptions are made by all of the previously cited state-of-the-art methods. In addition to these assumptions, we assume that the clocks of the agents are synchronized. We assume 2 cases:

1.  We can synchronize all agents at the beginning of a given mission.

2.  If an agent (not synchronized) is getting close to a cluster of other synchronized agents, we assume the range of communication is big enough so that the agent can synchronize its clock with the cluster before getting close enough for collision avoidance.

Furthermore, we assume symmetric behavior of the communication: if there is a latency in the delivery of a message from agent $i$ to agent $j$ in a given planning iteration/period, the same latency happens when agent $j$ is trying to deliver a message to agent $i$.

:::: {#fig:update_sc .figure}
![Safe Corridor at iteration $k$.](Toumieh2023Decentralized_figs/sc_evo_1.png){#fig:sc_evo_1 width="80%"}

![Safe Corridor at iteration $k+1$.](Toumieh2023Decentralized_figs/sc_evo_2.png){#fig:sc_evo_2 width="90%"}

::: caption
The obstacles are shown in **red**. The predicted positions of the agent are shown as **yellow** circles (MPC trajectory). They get increasingly transparent as we move forward in time. At iteration $k$ (Fig. [2](#fig:sc_evo_1){reference-type="ref" reference="fig:sc_evo_1"}), all polyhedra (in **blue**) contain at least one point of the MPC trajectory. At the next iteration $k+1$ (Fig. [3](#fig:sc_evo_2){reference-type="ref" reference="fig:sc_evo_2"}), the first position of the MPC trajectory moves out of the first polyhedron (in **dashed blue** lines). Thus, we remove it from the Safe Corridor and generate another polyhedron (in **green**) using the global path. The new polyhedron is added to the Safe Corridor.
:::
::::

# The planner {#sect:the_method}

Our planner is run concurrently on each agent in a swarm. The dynamical model of each agent is the same as presented in [@toumieh2022multi]. We use a voxel grid representation of the environment, which can be trivially and efficiently generated [@toumieh2020mapping]. Each agent has a voxel grid that is of fixed size and that moves with the agent such that the agent is always at its center. This voxel grid is used for global path finding and Safe Corridor generation. The clocks of the agents are synchronized.

In [@toumieh2022multi], the planning is divided into 2 stages: an offline stage for global path finding and Safe Corridor generation; then an online stage where the time-aware Safe Corridors and the dynamically feasible trajectory are generated. In the planner proposed in this paper, the offline stage is now integrated into the online planning stage so the whole planning/replanning framework is run online. This makes it suitable for real-world deployment and missions such as exploration. The steps of the proposed planner are (Fig. [1](#fig:diagram){reference-type="ref" reference="fig:diagram"}):

1.  Generate a global path (Sect. [3.1](#sect:global_path){reference-type="ref" reference="sect:global_path"}).

2.  Generate a Safe Corridor (Sect. [3.2](#sect:sc){reference-type="ref" reference="sect:sc"})

3.  Generate a time-aware Safe Corridor (Sect. [3.3](#sect:ta_sc){reference-type="ref" reference="sect:ta_sc"}).

4.  Generate a local reference trajectory (Sect. [3.4](#sect:loc_ref){reference-type="ref" reference="sect:loc_ref"}).

5.  Solve the Mixed-Integer Quadratic Program (MIQP)/Model Predictive Control (MPC) problem to generate a locally optimal trajectory (Sect. [3.5](#sect:form){reference-type="ref" reference="sect:form"}).

In the first step, we generate a global path from the position of the agent to the goal position. This path avoids all static obstacles and is used to generate the Safe Corridor and to generate the local reference trajectory. In the second step, we generate a Safe Corridor (a series of overlapping convex polyhedra) that covers only the free space in the environment. These convex polyhedra are used as linear constraints in an optimization formulation to constrain the trajectory to the free space and avoid collisions with static obstacles. In the third step, we use the recently generated trajectories of the agents and the Safe Corridor to generate time-aware Safe Corridors. This allows the agents to avoid intra-agent collisions. In the fourth step, we sample the global path at a given velocity to generate a local reference trajectory that the dynamically feasible trajectory tries to follow as closely as possible. In the fifth and final step, we generate the dynamically feasible trajectory to be executed by the agent. It is generated by solving an optimization problem that takes time-aware Safe Corridors and a local reference trajectory and guarantees that there are no collisions of any nature (intra-agent or static obstacles) while the agent moves closer to its goal.

These steps were run sequentially and periodically at a fixed frequency in our previous work [@toumieh2022multi]. However, in this work, we vary the planning frequency to account for communication latency. As in [@toumieh2022multi], each agent broadcasts its planned trajectory at the end of the planning iteration so that other agents can know it. In addition to the planned trajectory, we also broadcast the times we started and finished generating the trajectory so that other agents can estimate the communication latency (not done in [@toumieh2022multi] - more details in Sect. [3.6](#sect:com_latency){reference-type="ref" reference="sect:com_latency"}). We briefly explain each step in this section while focusing more on the steps where changes were made with respect to [@toumieh2022multi].

## Generate a global path {#sect:global_path}

In this step, a global path is generated connecting the current position of the agent to the desired final position using the local voxel grid. The occupied voxels in the voxel grid are inflated by each agent's size before feeding the grid to the path planning algorithm. In case the goal position is outside the local voxel grid of the agent, we choose an intermediate goal in the grid as presented in [@toumieh2020planning]. The main idea is to draw a line connecting the position of the agent to the goal and get the intersection with the borders of the voxel grid. This intersection is a voxel and is set as an intermediate goal. We also clear/set to **free** all the border voxels of the voxel grid to help the agent find a path to the intermediate goal in extremely cluttered environments.

At each iteration, the starting point for the global path search is the last point in the local reference trajectory generated in the previous planning iteration (Sect. [3.4](#sect:loc_ref){reference-type="ref" reference="sect:loc_ref"}). The local reference trajectory is then connected to the path found through the global search to generate the final global path used in the subsequent sections (for generating the local reference trajectory of the current iteration).

We use JPS (Jump Point Search) [@harabor2011online] and DMP (Distance Map Planner) for path planning. JPS employs pruning techniques on the A\* algorithm to potentially speed up the generation time by an order of magnitude. DMP uses artificial potential fields to push the path generated by JPS away from obstacles. This adds an additional margin of safety and improves the trajectory generated in the last step (MIQP optimization output) in terms of speed and smoothness (see [@toumieh2020planning] for more details).

:::: {#fig:stalemate .figure}
![Stalemate caused by a symmetrical position.](Toumieh2023Decentralized_figs/stalemate_1.png){#fig:stalemate_1 width="90%"}

![Perturbing hyperplanes asymmetrically.](Toumieh2023Decentralized_figs/stalemate_2.png){#fig:stalemate_2 width="90%"}

![Perturbing hyperplanes symmetrically.](Toumieh2023Decentralized_figs/stalemate_3.png){#fig:stalemate_3 width="90%"}

::: caption
A stalemate/deadlock happens when 2 agents are trying to move towards opposite goals and the solver is stuck on the borders of the hyperplanes (Fig. [5](#fig:stalemate_1){reference-type="ref" reference="fig:stalemate_1"}). Any movement up or down would not decrease the distance to the goal. If the hyperplanes are perturbed asymmetrically as done in [@toumieh2022multi] (Fig. [6](#fig:stalemate_2){reference-type="ref" reference="fig:stalemate_2"}), the distance between the agents can potentially become lower than the safety distance. We modify the perturbation vector (Sect. [3.3](#sect:ta_sc){reference-type="ref" reference="sect:ta_sc"}) to make the perturbation symmetrical and guarantee safety when the agents move in the direction of the **magenta** vectors or any other direction (Fig. [7](#fig:stalemate_3){reference-type="ref" reference="fig:stalemate_3"}).
:::
::::

![We show the trajectories of 2 agents (in **red** and **yellow**) and the corresponding discrete positions that get more transparent as we move forward in time. We ignore the positions of each trajectory that have no corresponding position in the other ($k-2$ and $k+3$). The separating hyperplanes (**dashed lines** in different colors) are generated between the positions of the agents corresponding to the same time in the future starting from the current iteration $k$. The last separating hyperplane $k+2$ is used to fill the remaining $N-3$ hyperplanes required to generate the TASC.](Toumieh2023Decentralized_figs/sep_planes.png){#fig:sep_planes width="100%"}

## Generate a Safe Corridor around the global path {#sect:sc}

Safe Corridors are a series of overlapping convex shapes that cover only free space in the environment. They are used by many state-of-the-art planning methods to constrain a dynamically feasible trajectory inside them, and thus guarantee safety [@toumieh2022near], [@toumieh2020planning], [@toumieh2022multi]. Many methods exist in the literature for Safe Corridor generation [@deits2015computing], [@liu2017planning], [@toumieh2020convex] [@toumieh2022shape]. The method used for the generation is [@toumieh2020convex] since it provides the best performance among the state-of-the-art methods for trajectory planning.

The Safe Corridor generation method takes as input a voxel grid (the local voxel grid centered around the agent) and the global path around which we want to generate the Safe Corridor. At each iteration, we always make sure that we have a certain number $P_{\text{hor}}$ of polyhedra that cover the free space of the environment.

At the first iteration of planning, we use the global path at the first iteration to generate a Safe Corridor that contains up to $P_{\text{hor}}$ number of polyhedra (polyhedra horizon). Subsequently, at each planning period, we use the global path generated in this planning period to update the Safe Corridor generated in the last step. The update consists of the following (Fig. [4](#fig:update_sc){reference-type="ref" reference="fig:update_sc"}): all the polyhedra that contain at least one point of the last generated MPC trajectory are kept. The other polyhedra are removed and new polyhedra are generated in their place until we have $P_{\text{hor}}$ polyhedra in total. To generate each polyhedron, we sample the global path at a constant step (voxel size). We then use the first point of the sampled global path that is outside all the remaining polyhedra as a seed voxel to generate an additional polyhedron.

## Generate a time-aware Safe Corridor (TASC) {#sect:ta_sc}

After generating the Safe Corridor, we use it along with the trajectories generated by all the other agents at the previous iterations to create a time-aware Safe Corridor (TASC). The future positions predicted by the MPC trajectories of the agents at the previous planning iterations are used to generate hyperplanes to constrain the future/MPC positions at the current iteration. These hyperplanes are added to the constraints of the Safe Corridor. This creates a series of Safe Corridors at each planning iteration that we call time-aware Safe Corridors in [@toumieh2022multi]. We refer the reader to [@toumieh2022multi] for a detailed explanation of how time-aware Safe Corridors are generated.

We augment/improve the TASC generation method to account for trajectories that were not generated at the same planning iteration $k$ (Fig. [9](#fig:sep_planes){reference-type="ref" reference="fig:sep_planes"}). We ignore the positions of each trajectory that have no corresponding positions in the other trajectory ($k-1$ and $k+3$ in Fig. [9](#fig:sep_planes){reference-type="ref" reference="fig:sep_planes"}). Then, starting with the position of the current iteration $k$, we generate separating hyperplanes for the rest of the common positions ($k$, $k+1$ and $k+2$ in Fig. [9](#fig:sep_planes){reference-type="ref" reference="fig:sep_planes"}). Since we need $N$ separating hyperplanes to generate the TASC (as shown in [@toumieh2022multi]), we set the rest of the hyperplanes equal to the last separating hyperplanes ($k+2$ in Fig. [9](#fig:sep_planes){reference-type="ref" reference="fig:sep_planes"}).

### Dealing with stalemates/deadlocks

In [@toumieh2022multi], in order to avoid stalemates/deadlocks, we modified the normal vectors of the separating hyperplanes by perturbing them constantly through time (a time-varying right-hand rule). This would avoid adding an explicit mechanism that creates subgoals for each agent to avoid stalemates/deadlocks like in [@Park2022DecentralizedDT]. We defined the normalized plane normal $\boldsymbol{n}_{\text{hyp,norm}}$, the *right* vector $\boldsymbol{r}$ that is the cross product between $\boldsymbol{n}_{\text{hyp,norm}}$ and $\boldsymbol{z}_W$ plus the cross product between $\boldsymbol{n}_{\text{hyp,norm}}$ and $\boldsymbol{y}_W$, a perturbation $m$, and a user-chosen coefficient $c$ that defines how tilted the final normal vector of the hyperplane $\boldsymbol{n}_{\text{hyp,final}}$ is with respect to the initial vector $\boldsymbol{n}_{\text{hyp}}$: $$\begin{gather}
    \boldsymbol{n}_{\text{hyp,norm}} =    \dfrac{\boldsymbol{n}_{\text{hyp}}}{||\boldsymbol{n}_{\text{hyp}}||_2} \\
    \boldsymbol{z}_W = [0, 0, 1]^T, \quad
    \boldsymbol{y}_W = [0, 1, 0]^T \\ \boldsymbol{r} = \boldsymbol{n}_{\text{hyp,norm}} \times \boldsymbol{z}_W + \boldsymbol{n}_{\text{hyp,norm}} \times \boldsymbol{y}_W\\
    \boldsymbol{n}_{\text{pert}} = (c + m)\cdot \dfrac{\boldsymbol{r}}{||\boldsymbol{r}||_2} + c\cdot\boldsymbol{z}_W\\
    \boldsymbol{n}_{\text{hyp,final}} = \boldsymbol{n}_{\text{pert}} + \boldsymbol{n}_{\text{hyp,norm}} \label{eqn:pert}
\end{gather}$$

However, a component of the perturbation vector $\boldsymbol{n}_{\text{pert}}$ is non-symmetric ($c\cdot\boldsymbol{z}_W$), which can generate normal vectors that are non-colinear. This can result in cases where the distance between agents is lower than the safety/collision distance $2\cdot d_{\text{rad}}$ (Fig. [8](#fig:stalemate){reference-type="ref" reference="fig:stalemate"}). For this reason, we replace the non-symmetric term with the following symmetric term: $c\cdot(\boldsymbol{z}_W \times \boldsymbol{n}_{\text{hyp,norm}})$. The final perturbation vector then becomes: $$\begin{gather}
    \boldsymbol{n}_{\text{pert}} = (c + m)\cdot \dfrac{\boldsymbol{r}}{||\boldsymbol{r}||_2} + c\cdot(\boldsymbol{z}_W \times \boldsymbol{n}_{\text{hyp,norm}})
\end{gather}$$

It is then added to $\boldsymbol{n}_{\text{hyp,norm}}$ to generate $\boldsymbol{n}_{\text{hyp,final}}$ as in equation ([\[eqn:pert\]](#eqn:pert){reference-type="ref" reference="eqn:pert"}).

## Generate a local reference trajectory {#sect:loc_ref}

We use the global path to generate a local reference trajectory that is used as a reference for the MPC to follow. The generation of such reference trajectory is done by sampling the global path at a constant velocity $v_{\text{samp}}$. The number of sampled points is equal to the number of discretization steps ($N$) in the MPC/MIQP formulation.

We only generate a new local reference trajectory in the following case: the last point of the MPC trajectory is within a distance $d_{\text{thresh}}$ from the last point of the local reference trajectory generated at the previous iteration. Otherwise, we keep the local reference trajectory generated at the previous planning iteration.

![We show an example of how different agents handle communication delays between each other. In this example agent 2 communicates with agents 1 and 3, whereas agents 1 and 3 do not communicate with each other (not within the range of communication). We show in **green** the computation time of each agent, in **blue** the communication latency between agents 1 and 2, and in **red** the communication latency between agents 2 and 3. The arrows indicate the time at which an agent $i$ receives the trajectory $\boldsymbol{T}_{j,k}$ of another agent $j$ generated at iteration $k$. At the first iteration, all agents synchronize their first planning iteration to be at the same time. At the subsequent iterations, an agent skips planning in one of 2 cases: 1) At least one agent within the communication range is yet to receive its last generated trajectory 2) It is yet to receive a new generated trajectory of another agent within the communication range and it has used all the previously received trajectories of this agent to generate its own trajectory.](Toumieh2023Decentralized_figs/com_example.png){#fig:com_example width="100%"}

## Solving the MIQP/MPC problem {#sect:form}

In this final step, we take the reference trajectory, and we solve an MPC optimization problem that minimizes the distance of the generated trajectory to the reference trajectory while also minimizing the jerk for smoothness. The generated trajectory consists of $N+1$ discrete states $\boldsymbol{x}_i$, $i = 0,1,...,N$ that contain the position, velocity, and acceleration of the agent. Each consecutive pair of discrete states are separated by a time step $h$. Thus, the time horizon of the planning is $N\cdot h$. The velocity and acceleration of the last state $\boldsymbol{x}_N$ are constrained/set to 0 to guarantee a safe trajectory for all agents in case subsequent optimizations fail (see [@toumieh2022multi] for more details).

The time-aware Safe Corridor is used to ensure the safety of the trajectory. We add the linear constraints of the time-aware Safe Corridor to the MPC optimization problem. By forcing each segment of the MPC trajectory be in at least one of the polyhedra of the time-aware Safe Corridor, we ensure no collision happens between the agent and the static obstacles as well as other planning agents. The final formulation of the optimization problem is a Mixed-Integer Quadratic Problem (MIQP) exactly like the one presented in [@toumieh2020planning], [@toumieh2022multi].

## Handling communication delay {#sect:com_latency}

:::: algorithm
::: algorithmic
delay_planning = **false** traj_old\[$j$\].add($\boldsymbol{T}_j$) delay_planning = **true** $dt_{\text{delay},i,j}$ = ComputeLatency(traj_old\[$j$\]\[0\]) $> t_{\text{cur}}$ delay_planning = **true** GenerateTASC(traj_old\[$j$\]\[0\], $\boldsymbol{T}_{i,\text{last}}$) traj_old\[$j$\].RemoveFirstElement()
:::
::::

Our previous work [@toumieh2022multi] ran the planning algorithm at a constant period equal to the MPC discretization step $dt_{\text{plan}} = h$. It was able to handle communication delay passively by assuming that the communication delay was lower than a time variable $dt_{\text{max,delay}}$ equal to the planning period $dt_{\text{plan}}$ minus the planner computation time $dt_{\text{comp}}$ ($dt_{\text{max,delay}} = dt_{\text{plan}} -  dt_{\text{comp}}$). However, no mechanism was in place to handle the communication latency when it exceeds $dt_{\text{max,delay}}$.

In this work, we propose to adapt the planning period to be able to guarantee safety no matter the communication delay. In addition to broadcasting the trajectory $\boldsymbol{T}_j$ when it finishes generating it, each agent $j$ broadcasts the time at which it started generating its trajectory i.e. the time at the start of the planning period ($\boldsymbol{T}_j$.start). It also broadcasts the time it finished generating the trajectory i.e. the time it sent it ($\boldsymbol{T}_j$.end). This allows another agent $i$ to estimate the communication delay between it and agent $j$ since their clocks are synchronized. The delay can be estimated by subtracting $\boldsymbol{T}_j$.end from the reception time of agent $i$, $t_{\text{rec},i}$: $$\begin{gather}
     dt_{\text{delay},i,j}= t_{\text{rec},i} - \boldsymbol{T}_j\text{.end} \label{eqn:delay}
\end{gather}$$ This in turn allows agent $i$ to know whether its last generated trajectory $\boldsymbol{T}_{i,\text{last}}$ was received by agent $j$ before the start time of the current planning period $t_{\text{cur}}$. The last generated trajectory of agent $i$ is not yet received by agent $j$ if the following condition is true: $$\begin{gather}
 dt_{\text{delay},i,j} +  \boldsymbol{T}_{i,\text{last}}.\text{end} >  t_{\text{cur}}  \label{eqn:delay_check}
\end{gather}$$ The planner will skip planning at the start of the current planning period and wait for the next period if one of these 2 cases is true:

1.  It knows that there is another agent within its communication range that is yet to receive its last planned trajectory.

2.  It is yet to receive a new planned trajectory of another agent within its communication range and it has used all the old received trajectories of this agent for planning.

We propose the following algorithm to handle communication latency (Alg. [\[alg:latency\]](#alg:latency){reference-type="ref" reference="alg:latency"}). At every planning iteration (which happens every $dt_{\text{plan}} = h$), every agent $i$ checks if it received a trajectory from every other agent $j$ (line 3). If it did, it adds the received trajectory to a 2D vector (traj_old) whose first index indicates the number or ID of the other agent i.e. $j$ (line 4). If agent $i$ did not receive a trajectory from agent $j$, it checks if there is an unused old trajectory in the vector traj_old\[$j$\] (line 5-6). If not, we delay the planning since we have no new or old trajectory to use for generating the TASC (line 7). If the planning should not be delayed due to previous conditions (line 8), we check if it should be delayed because agent $j$ hasn't received the trajectory of agent $i$ yet. This is done by first computing the communication delay using equation ([\[eqn:delay\]](#eqn:delay){reference-type="ref" reference="eqn:delay"}) (line 9), and then checking the condition ([\[eqn:delay_check\]](#eqn:delay_check){reference-type="ref" reference="eqn:delay_check"}) (lines 10-11). Finally, we check if the planning should be delayed after going through all agents (line 12). If not, we compute the TASC using the oldest unused trajectory of each agent $j$ and remove it from the vector of old trajectories (lines 13-15). The starting time $\boldsymbol{T}_j$.start allows to know at which iteration $k$ the trajectory was generated, which is important in TASC generation (Fig. [9](#fig:sep_planes){reference-type="ref" reference="fig:sep_planes"}).

We show an example of how this algorithm would perform in Fig. [10](#fig:com_example){reference-type="ref" reference="fig:com_example"}. In this example, agent 2 sees and communicates with agents 1 and 3, but agents 1 and 3 do not see and communicate with each other. Still, the algorithm allows for safe planning and coordination between all agents.

# Simulation Results {#sect:sim_res}

The testing setup is similar to what is presented in [@kondo2022robust]. Thus, we will use their results as a reference for our comparison. The simulations are run on Intel i7 CPUs with a base frequency of 2.6GHz and a turbo boost of 4GHz. The testing consists of 10 agents in a circular configuration (Fig. [11](#fig:our_100){reference-type="ref" reference="fig:our_100"}) exchanging positions. We compare our method with RMADER [@kondo2022robust] and 2 versions of Ego-Swarm [@Zhou2021EGOSwarmAF]. We set the maximum velocity $v_{\text{max}} = 10\ \text{m/s}$, the maximum acceleration $a_{\text{max}} = 20\ \text{m/s\textsuperscript{2}}$ and the maximum jerk $j_{\text{max}} = 30\ \text{m/s\textsuperscript{3}}$ for RMADER, Ego-Swarm and our method (along the $x$, $y$ and $z$ directions). For Ego-Swarm, we also consider a more conservative version (slow Ego-Swarm) with a maximum acceleration $a_{\text{max}} = 10\ \text{m/s\textsuperscript{2}}$ and a maximum velocity $v_{\text{max}} = 5\ \text{m/s}$.

For MADER and RMADER, each agent is represented as a bounding box of size $0.25\times0.25\times0.25$ m. For Ego-Swarm and our planner, each agent is represented as a sphere of diameter $0.25$ m as per the experiments in [@kondo2022robust] (at the time of writing, the bounding box dimensions and sphere diameter were not mentioned in [@kondo2022robust], but they were communicated to us by the authors of [@kondo2022robust]). The comparison is done with 100 simulated runs for communication latencies equal to $0$, $50$, and $100$ milliseconds. The comparison metrics are:

1.  Collision %: percentage of simulations where there was at least one collision.

2.  Average number of stops expected in a single simulation from all agents.

3.  Mean of the jerk cost $J_{\text{cost}} = \int_{t_{\text{ini}}}^{t_{\text{fin}}} ||\boldsymbol{j}(t)||^2\mathrm{d}t$ where $t_{\text{ini}}$ and $t_{\text{fin}}$ are the initial and final time of the trajectory.

4.  Mean of the acceleration cost $A_{\text{cost}} = \int_{t_{\text{ini}}}^{t_{\text{fin}}} ||\boldsymbol{a}(t)||^2\mathrm{d}t$.

5.  Mean and max flight time.

6.  Computation time.

::: table*
  ------------------------------- ------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------ ----------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------- --
              Method                                                         Collision \[%\]                                                                                              Mean \# stops                                                                                                  Accel. cost (m/s^2^)                                                                                                  Jerk cost (10^3^ m/s^3^)                                                                                                  Mean flight time (s)                                                                                                    Max flight time (s)                                                  
     ES [@Zhou2021EGOSwarmAF]      [64]{style="color: blue"} $\mid$ [84]{style="color: OliveGreen"} $\mid$ [84]{style="color: magenta"}     [0.004]{style="color: blue"} $\mid$ [0]{style="color: OliveGreen"} $\mid$ [0.01]{style="color: magenta"}            [662]{style="color: blue"} $\mid$ [700]{style="color: OliveGreen"} $\mid$ [788]{style="color: magenta"}               [9.07]{style="color: blue"} $\mid$ [9.46]{style="color: OliveGreen"} $\mid$ [10.4]{style="color: magenta"}              [7.19]{style="color: blue"} $\mid$ [7.24]{style="color: OliveGreen"} $\mid$ [7.28]{style="color: magenta"}             [7.38]{style="color: blue"} $\mid$ [7.51]{style="color: OliveGreen"} $\mid$ [7.63]{style="color: magenta"}       
   Slow ES [@Zhou2021EGOSwarmAF]   [14]{style="color: blue"} $\mid$ [25]{style="color: OliveGreen"} $\mid$ [22]{style="color: magenta"}         [0]{style="color: blue"} $\mid$ [0]{style="color: OliveGreen"} $\mid$ [0]{style="color: magenta"}               [110]{style="color: blue"} $\mid$ [113]{style="color: OliveGreen"} $\mid$ [113]{style="color: magenta"}               [15.4]{style="color: blue"} $\mid$ [15.5]{style="color: OliveGreen"} $\mid$ [15.5]{style="color: magenta"}              [11.6]{style="color: blue"} $\mid$ [11.7]{style="color: OliveGreen"} $\mid$ [11.8]{style="color: magenta"}               [11.9]{style="color: blue"} $\mid$ [12]{style="color: OliveGreen"} $\mid$ [13]{style="color: magenta"}         
   MADER [@tordesillas2020mader]   [15]{style="color: blue"} $\mid$ [38]{style="color: OliveGreen"} $\mid$ [42]{style="color: magenta"}       [0]{style="color: blue"} $\mid$ [0.001]{style="color: OliveGreen"} $\mid$ [0]{style="color: magenta"}           [78.1]{style="color: blue"} $\mid$ [74.2]{style="color: OliveGreen"} $\mid$ [74.5]{style="color: magenta"}              [1.59]{style="color: blue"} $\mid$ [1.64]{style="color: OliveGreen"} $\mid$ [1.64]{style="color: magenta"}              [6.28]{style="color: blue"} $\mid$ [6.25]{style="color: OliveGreen"} $\mid$ [6.26]{style="color: magenta"}             [7.15]{style="color: blue"} $\mid$ [7.35]{style="color: OliveGreen"} $\mid$ [7.04]{style="color: magenta"}       
     RMADER [@kondo2022robust]      [0]{style="color: blue"} $\mid$ [0]{style="color: OliveGreen"} $\mid$ [0]{style="color: magenta"}      [0.46]{style="color: blue"} $\mid$ [0.347]{style="color: OliveGreen"} $\mid$ [1.75]{style="color: magenta"}          [127]{style="color: blue"} $\mid$ [148]{style="color: OliveGreen"} $\mid$ [190]{style="color: magenta"}               [2.94]{style="color: blue"} $\mid$ [3.71]{style="color: OliveGreen"} $\mid$ [5.94]{style="color: magenta"}              [7.28]{style="color: blue"} $\mid$ [7.95]{style="color: OliveGreen"} $\mid$ [10.4]{style="color: magenta"}             [8.41]{style="color: blue"} $\mid$ [8.80]{style="color: OliveGreen"} $\mid$ [11.9]{style="color: magenta"}       
             proposed               [0]{style="color: blue"} $\mid$ [0]{style="color: OliveGreen"} $\mid$ [0]{style="color: magenta"}     [**0**]{style="color: blue"} $\mid$ [**0**]{style="color: OliveGreen"} $\mid$ [**0**]{style="color: magenta"}   [**109**]{style="color: blue"} $\mid$ [**114**]{style="color: OliveGreen"} $\mid$ [**119**]{style="color: magenta"}   [**2.27**]{style="color: blue"} $\mid$ [**2.49**]{style="color: OliveGreen"} $\mid$ [**5.03**]{style="color: magenta"}   [**6.77**]{style="color: blue"} $\mid$ [**6.79**]{style="color: OliveGreen"} $\mid$ [**7.1**]{style="color: magenta"}   [**7.1**]{style="color: blue"} $\mid$ [**7.3**]{style="color: OliveGreen"} $\mid$ [**7.7**]{style="color: magenta"}  
  ------------------------------- ------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------ ----------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------- --

[]{#table:comparison_table_mader label="table:comparison_table_mader"}
:::

:::: {#fig:our_dt .figure}
![Our planner: 10 agents with $dt = 100$ ms with the setup in Tab. [\[table:comparison_table_mader\]](#table:comparison_table_mader){reference-type="ref" reference="table:comparison_table_mader"}.](Images/our_100.png){#fig:our_100 width="105%"}

![Our planner: 12 agents with $dt = 0$ ms and obstacles (Sect. [4.3](#sect:sim_obs){reference-type="ref" reference="sect:sim_obs"}).](Images/our_obs_0.png){#fig:our_obs_0 width="105%"}

![Our planner: 12 agents with $dt = 150$ ms and obstacles (Sect. [4.3](#sect:sim_obs){reference-type="ref" reference="sect:sim_obs"}).](Images/our_obs_150.png){#fig:our_obs_150 width="105%"}

::: caption
The agents start in a circular configuration and swap positions. We show an overhead view of the trajectories generated by our planner in different settings (with and without obstacles), different communication latencies, and different dynamic limits.
:::
::::

::: {#table:comp_time_our}
  ------------ ----------------- ------------------- -----------------
                  $dt = 0$ ms       $dt = 50$ ms       $dt = 100$ ms
   Comp. (ms)   10.4 / 61 / 6.6   10.1 / 54.7 / 6.4   11.4 / 70 / 6.7
  ------------ ----------------- ------------------- -----------------

  : Computation time of our planner for the results in Tab. [\[table:comparison_table_mader\]](#table:comparison_table_mader){reference-type="ref" reference="table:comparison_table_mader"}. We show the **mean / max / standard deviation**.
:::

[]{#table:comp_time_our label="table:comp_time_our"}

## Planner parameters

The local voxel grid around each agent is of size $15\times 15\times 3.3$ m and has a voxel size of $0.3$ m. We choose the following parameters: $N = 9$, $h = 100$ ms, $v_{\text{samp}} = 4.5$ m/s, $P_{\text{hor}} = 3$, $d_{\text{thresh}}= 0.4$ m. The rest of the parameters are chosen the same as in [@toumieh2022multi] with the exception of the maximum velocity, acceleration, and jerk which are the same for all planners (Sect. [4](#sect:sim_res){reference-type="ref" reference="sect:sim_res"}).

## Comparison with the state-of-the-art

We show in Tab. [\[table:comparison_table_mader\]](#table:comparison_table_mader){reference-type="ref" reference="table:comparison_table_mader"} the results of the planners with different communication latencies ($0$, $50$, and $100$ ms). Our planner and Ego-Swarm [@Zhou2021EGOSwarmAF] use voxel girds as representations of the obstacles in the environment. MADER [@tordesillas2020mader] and RMADER [@kondo2022robust] on the other hand use a polyhedral representation of the environment i.e. all obstacles are represented by a series of convex polyhedra. This representation is not trivial to generate and may add considerable overhead to the autonomous navigation pipeline.

Our planner and RMADER [@kondo2022robust] are the only planners that are able to generate collision-free trajectories in all simulations, so we will focus our comparison on them. Our planner outperforms RMADER in trajectory smoothness across all latencies using both the acceleration ($25$% better on average) and the jerk ($24$% better on average) metrics.

The mean and max flight times of our planner grow slower than those of RMADER with the increase in latency. Over all latencies, our planner outperforms RMADER in mean flight time by an average of $18$% and max flight time by an average of $23$%.

### Computation time {#sect:comp_time}

Ego-Swarm is the most computationally efficient with an average computation time of $0.5$ ms. RMADER improves on MADER [@tordesillas2020mader] in computation time by changing the optimization problem from non-convex to convex. This improves the mean computation time by $20$% (from $39.23$ ms to $31.08$ ms) and the max computation time by $40$% (from $724$ ms to $433$ ms) as reported in [@kondo2022robust]. While our planner is not as efficient as Ego-Swarm, it is much more efficient than RMADER as shown in Tab. [1](#table:comp_time_our){reference-type="ref" reference="table:comp_time_our"}. The mean computation time across all latencies is $10.6$ ms and the max is $70$ ms.

::: table*
  ----- ----------- -------------------- -------------------- -------------------- ------------------- -------------------- ------------------------- --
   \#    $dt$ (ms)      Distance (m)        Velocity (m/s)      Flight time (s)      Comp. time (ms)    Acc. cost (m/s^2^)   Jerk cost (10^3^m/s^3^)  
             0       21.6 / 23.1 / 0.72   2.52 / 4.21 / 1.24    8.47 / 9.5 / 0.4     5.5 / 48.7 / 3      121 / 170 / 26.2       3.5 / 5.56 / 0.94     
   2-8      50       21.6 / 23.1 / 0.72   2.51 / 4.21 / 1.24    8.47 / 9.5 / 0.4    5.4 / 48.1 / 2.9     121 / 170 / 26.2       3.5 / 5.56 / 0.95     
   2-8      100      21.6/ 23.4 / 0.76    2.43 / 4.24 / 1.22    8.7 / 9.5 / 0.42     6.2 / 35 / 3.8      124 / 182 / 26.7      6.59 / 9.11 / 0.96     
   2-8      150      21.6 / 23.4 / 0.76   2.43 / 4.24 / 1.22    8.7 / 9.5 / 0.42    6.1 / 33.3 / 3.8     124 / 182 / 26.5      6.59 / 9.11 / 0.96     
             0       21.7 / 24.2 / 0.73   2.45 / 4.5 / 1.23     8.7 / 9.9 / 0.45     8.7 / 72.4 / 6      130 / 207 / 26.8      3.76 / 5.65 / 0.84     
   2-8      50       21.7 / 24.1 / 0.73   2.46 / 4.5 / 1.24     8.7 / 9.9 / 0.43    8.4 / 69.6 / 5.8     136 / 207 / 27.6      4.19 / 6.56 / 0.88     
   2-8      100      21.6 / 23.9 / 0.71   2.38 / 4.36 / 1.2    8.98 / 10.3 / 0.46   9.2 / 85.9 / 7.3     134 / 240 / 28.7      6.86 / 10.8 / 0.97     
   2-8      150      21.7 / 23.7 / 0.7    2.36 / 4.86 / 1.22   9.08 / 10.4 / 0.44   10.8 / 86.6 / 8.4    146 / 308 / 34.2      8.41 / 17.1 / 1.46     
   1-8                                                                                                                                                
  ----- ----------- -------------------- -------------------- -------------------- ------------------- -------------------- ------------------------- --

[]{#table:comp_obs label="table:comp_obs"}
:::

## Environment with obstacles {#sect:sim_obs}

We add obstacles to the environment as well as delay to see how our planner performs as the communication latency increases. The obstacles have already been inflated by the agent's radius at their generation. We test for $8$ and $12$ agents. Furthermore, we change the diameter of each agent to $0.3$ m, $v_{\text{samp}} = 3.5$ m/s, $a_{\text{max}} = 30$ m/s^2^, $j_{\text{max}} = 60$ m/s^3^, $N = 7$ and $d_{\text{thresh}} = 0.2$ m for experimental diversity. We generate $70$ obstacles of size $0.2\times0.2\times1.5$ m with random positions at each simulation run (uniform distribution - Fig. [12](#fig:our_obs_0){reference-type="ref" reference="fig:our_obs_0"}, [13](#fig:our_obs_150){reference-type="ref" reference="fig:our_obs_150"}). We do 10 simulation runs for each latency $dt = 0, 50, 100$, and $150$ ms. The performance metrics used are the distance traversed by each agent, the flight velocity and time, the computation time, and the acceleration and jerk costs. The **mean / max / standard deviation** of each metric are shown in Tab. [\[table:comp_obs\]](#table:comp_obs){reference-type="ref" reference="table:comp_obs"}.

In all test runs for 8 and 12 agents, all agents were able to reach their intended goal/destination safely i.e. the safety distance between the agents was not violated and they did not get stuck along the way.

For 8 agents, the results for $dt = 0$ ms and $dt = 50$ ms are similar. This is due to the fact that in both cases, all agents receive the trajectories before the start of the next planning iteration since the maximum computation time is below $50$ ms. The results for $dt = 100$ ms and $dt = 150$ ms are also similar due to the same reason: in both cases, all agents receive the trajectories of other agents every 2 planning iterations (the planning period is effectively $2h$ due to our latency handling algorithm [\[alg:latency\]](#alg:latency){reference-type="ref" reference="alg:latency"}).

For 8 and 12 agents, the jerk cost and computation time both increase as the latency increases. This is due to the more frequent slowdown of each agent as the latency increases. The slowdown is due to passing through narrow spaces and avoiding other agents at the same time as well as the latency handling mechanism (see video link after the abstract).

# Conclusions and Future Works

In this paper, we presented an improved decentralized, real-time, and synchronous framework for multi-agent planning. The method improves on our previous work [@toumieh2022multi] by making it fully online and suitable for real-world applications (the global path planning and Safe Corridor generation steps were done offline in [@toumieh2022multi]). Furthermore, we added a mechanism to handle arbitrary communication latency and adapt the planning frequency accordingly. Our previous work was only able to handle communication latency when it is lower than a predetermined threshold. We compared our work to 3 state-of-the-art multi-agent planning methods: Ego-Swarm [@Zhou2021EGOSwarmAF], MADER [@tordesillas2020mader] and RMADER [@kondo2022robust]. We showed that our planner generates the safest trajectories with a $0$% collision rate. Furthermore, it generates smoother and faster trajectories than the only other safe and latency robust planner (RMADER) while also being at least $3\times$ more computationally efficient.

In the future, we plan on implementing our planning method on embedded drone systems for swarm autonomous navigation. This would require implementing relative localization algorithms between agents, obstacle detection for collision avoidance, as well as a communication mechanism for broadcasting information between agents. Finally, we intend on developing a formation flight version of our planner. This can be done by adding a cost to the objective function of our planner that makes agents preserve a predefined shape.

[^1]: The author is an independent researcher (e-mail: [charbel.toumieh@gmail.com](charbel.toumieh@gmail.com){.uri})
