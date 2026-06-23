---
citation_key: Chung2023Distributed
arxiv_id: 2303.11279
arxiv_url: https://arxiv.org/abs/2303.11279
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:45:04Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

Distributed multi-robot systems are increasingly being deployed in many settings. Dynamic production facilities and modern warehouses are examples of settings that are becoming more reliant on multiple robots to perform material handling operations. However, such settings can heavily affect the collaborative navigation performance of a robot team since there can be narrow corridors and crossroads which may induce deadlock situations between the robots. A competent trajectory planner should be able to reactively avoid imminent collisions, and predictively avoid deadlocks between the robots' future trajectories as well.

:::: {#fig:avoidance .figure latex-placement="hbt"}
::: {#fig:avoidance_a .figure}
![image](Chung2023Distributed_figs/reactive_definition.png){width="95%"} []{#fig:avoidance_a label="fig:avoidance_a"}
:::

::: {#fig:avoidance_b .figure}
![image](Chung2023Distributed_figs/predictive_definition.png){width="95%"} []{#fig:avoidance_b label="fig:avoidance_b"}
:::

::: caption
Two types of collision avoidance. Dashed lines represent the intended trajectories. Solid lines represent the trajectories generated with collision avoidance.
:::
::::

We illustrate these two types of collision avoidance scenarios in [3](#fig:avoidance){reference-type="ref+label" reference="fig:avoidance"} . In a reactive avoidance scenario, the robots only need to avoid each other at the position where a potential collision may occur based on their intended trajectories. In a predictive avoidance scenario, the avoidance maneuver needs to be performed in advance, at a position prior to where a potential collision may occur. The related works in online trajectory planning can handle reactive collision avoidance, but not predictive deadlock avoidance which is currently solved in general using discrete graph-based methods [@Hoy2014]. Therefore, in this paper, we propose a novel planner that combines Prioritized Planning with a Distributed Timed Elastic Band (DTEB) Planner to handle both reactive and predictive collision avoidance.

# Related Work {#sec:related_work}

For the multi-robot trajectory planning problem, a classical approach is Velocity Obstacle (VO). VO considers the set of velocities of the ego robot that will result in a collision with another robot based on their current positions and velocities, and then finds the optimal control velocity that lies outside this forbidden velocity zone [@Fiorini1993]. There are many extensions to improve the performance of VO, such as Reciprocal Velocity Obstacle (RVO) [@vandenBerg2008] and Hybrid Reciprocal Velocity Obstacle (HRVO) [@Snape2011]. These papers have shown the effectiveness of VO-based approaches in local reactive collision avoidance. However, VO-based approaches optimize a single constant velocity input for a short period of time, which makes them unable to predictively avoid future deadlocks.

There are more advanced approaches which solve an Optimal Control Problem (OCP) and optimize a control sequence instead of a single control input. Recent examples include[@Defoort2010; @Filho2017; @Luis_2020; @tordesillas2020mader], but these approaches have two issues that undermine their ability in predictive deadlocks avoidance.

First, the prediction horizon is short for non-holonomic robots. For UAVs or holonomic robots, the trajectory can be planned efficiently using parametric B-spline as in [@Luis_2020; @tordesillas2020mader]. For non-holonomic robots, the optimization problem is non-linear as in [@Defoort2010; @Filho2017], and is difficult to be efficiently solved. Therefore, these approaches limit the prediction horizon to a short period of time to ensure efficiency. However, the short prediction horizon reduces the ability to avoid deadlocks, as the collision avoidance constraint is no longer considered beyond the prediction horizon. In contrast, our approach solves an unconstrained least squares problem, using the soft-constraints proposed by the TEB approach in [@roesmann2017], which has better computational efficiency than the original OPC [@roesmann2020online]. The improved efficiency allows a longer prediction horizon.

Second, the sequence of planning is unordered. However, the researches in Prioritized Planning (PP) show that the order of planning in a decoupled planning has a significant influence on the optimality and the completeness of the overall plan [@Parker2009] [@priority2001]. In particular, [@priority2001] shows that the corridor scenario in [2](#fig:avoidance_b){reference-type="ref+label" reference="fig:avoidance_b"} can be solved if the robots plan their trajectories in this order: Robot 1 should plan first, and Robot 0 should avoid it at the doorway. If Robot 0 plans first, there is no solution for Robot 1, as it will collide with Robot 0 before reaching the doorway.

To address the above issues, this paper proposes a novel DTEB planner for multi-robot trajectory planning by contributing the following:

- A Prioritized Planning scheme for reactive, as well as, predictive collision avoidance

- Extending the efficient TEB approach to include an improved obstacle model that can handle robots moving at arbitrary trajectories.

- A *novel* H-signature for the evaluation of homotopy classes of the generated trajectories. The evaluation is computationally efficient and able to handle arbitrary trajectories

- An open-source implementation of the Voronoi-diagram-based approach for trajectory sampling in narrow environments

# Distributed Timed Elastic Band Planner

The core idea of this paper is a distributed variant of the Timed Elastic Band (TEB) approach. Each robot in the multi-robot system cyclically broadcasts their latest planned trajectory, and the TEB approach combined with Prioritized Planning (PP) is used to plan its local optimal trajectory with consideration of the latest trajectory information.

TEB approach [@roesmann2013] is a single-robot trajectory planning method and can be considered as a special form of open-loop MPC. Instead of optimizing the control inputs, TEB approach directly optimizes the robot poses (and the time sequence) with soft-constraints and then extract control inputs from the poses [@roesmann2020online].

Prioritized Planning (PP) is an efficient decoupled planning method to solve potential deadlocks between robots [@Parker2009]. In PP, each robot is given a priority. High priority robots plan first, while low priority robots plan later and treat high priority robots as dynamic obstacles. Previous works in PP use discrete graph-based methods, such as RRT with A\* Algorithm [@Dewangan2017].

Since the original TEB approach is designed for single robot but not the aforementioned purpose, we modify the original TEB approach and also incorporate new features as explained in the following subsections.

::: myhl
[3.1](#sec:assumptions){reference-type="ref+label" reference="sec:assumptions"} states the assumptions in the implementation. [3.2](#sec:optimal_control){reference-type="ref+label" reference="sec:optimal_control"} formulates the planning problem as a soft-contrained optimization. [3.3](#sec:obstacle_constraint){reference-type="ref+label" reference="sec:obstacle_constraint"} explain how collision avoidance between robot trajectories is included into the optimization. [3.4](#sec:trajectory_sharing){reference-type="ref+label" reference="sec:trajectory_sharing"}

explains the sharing of this trajectory information between robots. [3.5](#sec:H_sign){reference-type="ref+label" reference="sec:H_sign"} and [3.6](#sec:voronoi){reference-type="ref+label" reference="sec:voronoi"} explain the improvement in homotopy class planning which is used to avoid local minimum problem in the optimization. [3.7](#sec:PP){reference-type="ref+label" reference="sec:PP"} explains the Prioritized Planning scheme used to resolve deadlocks between trajectories.

## Assumptions {#sec:assumptions}

1.  The robot team can be non-holonomic and heterogeneous.

2.  Each robot is controlled by an on-board computer and can communicate with each other within the planning horizon to share information as per [3.4](#sec:trajectory_sharing){reference-type="ref+label" reference="sec:trajectory_sharing"} .

3.  The planning is asynchronous among the team but has a fixed frequency of 20Hz.
:::

## Optimal Control Formulation {#sec:optimal_control}

For the proposed DTEB Planner, we adopted the existing optimal control formulation from the single-robot TEB Planner in [@roesmann2013] and [@roesmann2017] with a modification to the minimum obstacle separation constraint.

A Timed-Elastic-Band $\mathcal{B}$ is a tuple of sequences of $n$ robot configurations ($s_k = [x_k,y_k,\theta _k]^T)_{k=1,2,...,n}$ and time differences between them $(\Delta T_k)_{k=1,2,...,n-1}$: $$\begin{equation}
   \mathcal{B} := \{ s_1, \Delta T_1, s_2, \Delta T_2 ,..., s_{n-1}, \Delta T_{n-1}, s_n \} 
   \label{eqn:teb}
\end{equation}$$ Both the configurations and time differences are optimized against a soft constrained time optimal cost function to obtain an optimized TEB $\mathcal{B}^*$ as the robot trajectory: $$\begin{equation}
\mathcal{B}^{*} =\mathop{\mathrm{arg\,min}}_{\mathcal{B} \setminus \{ s_1,s_n \}} \tilde{V}(\mathcal{B})
\end{equation}$$ The time optimal cost function is given by: $$\begin{equation}
\resizebox{0.91\hsize}{!}{
$\begin{aligned}
\tilde{V}(\mathcal{B}) = &\sum_{k=1}^{n-1} [\Delta T_k^2 + \phi(\mathbf{h}_k, \sigma_h) + \chi(\tilde{r}_k,\sigma_r) + \chi(\boldsymbol{\nu}_k,\sigma_\nu) \\ & +\chi(\mathbf{o}_k,\sigma_\mathbf{o}) + \chi(\boldsymbol{\alpha}_k,\sigma_\alpha)] + \chi(\boldsymbol{\alpha}_n,\sigma_\alpha)
\end{aligned}
$
}
\label{eqn:cost_function}
\end{equation}$$

::: myhl
$\phi$ and $\chi$ are quadratic penalties approximating the kinematics, dynamics and collision-free constraints: $$\begin{equation}
\phi(\cdot, \sigma) =  \sigma \left\lVert\cdot\right\rVert^2_2.
\end{equation}$$ $$\begin{equation}
\chi(\cdot, \sigma) = \sigma \left\lVert min \{ \mathbf{0}, \cdot \} \right\rVert^2_2.
\end{equation}$$ where $\sigma$ is the scalar weight of the penalty term.

$\phi(\mathbf{h}_k, \sigma_h)$ is the penalty approximating the equality constraint of non-holonomic kinematics: $$\begin{equation}
\mathbf{h}_k = 
\begin{pmatrix}
cos(\theta_k) + cos(\theta_{k+1}) \\
sin(\theta_k) + sin(\theta_{k+1}) \\
0
\end{pmatrix}  
\times 
\begin{pmatrix}
x_{k+1} - x_k\\
y_{k+1} - y_k\\
0 
\end{pmatrix}  
= 0
\end{equation}$$ and $\chi(\tilde{r}_k,\sigma_r)$, $\chi(\boldsymbol{\nu}_k,\sigma_\nu)$, $\chi(\boldsymbol{\alpha}_k,\sigma_\alpha)$ and $\chi(\mathbf{o}_k,\sigma_\mathbf{o})$ are the penalties approximating the inequality constraints of minimum turning radius, maximum velocities, maximum accelerations and minimum obstacle separation, respectively: $$\begin{equation}
\tilde{r}_k = r_k - r_{min} \geq 0
\end{equation}$$ $$\begin{equation}
 \boldsymbol{\nu}_k = [{v}_{max} - |v_k|, {\omega}_{max} - |\omega_k|]^T \geq \mathbf{0}
\end{equation}$$ $$\begin{equation}
 \boldsymbol{\alpha}_k = [\mathrm{{a}}_{max} - |\mathrm{a}_k|, {\alpha}_{max} - |\alpha_k|]^T \geq \mathbf{0}
\end{equation}$$
:::

The above constraints are the same as the original TEB approach (for details, see[@roesmann2017]), while the inequality constraint of minimum obstacle separation is modified: $$\begin{equation}
\mathbf{o}_k(s_k) =
\begin{pmatrix}
\delta(s_k,O_1(T_k))\\
\delta(s_k,O_2(T_k))\\
\vdots\\
\delta(s_k,O_R(T_k))
\end{pmatrix}  
-
\begin{pmatrix}
\delta_{min}\\
\delta_{min}\\
\vdots\\
\delta_{min}
\end{pmatrix}
\geq \mathbf{0}
\end{equation}$$ where $\delta(s_k,O(T_k))$ describes the minimal Euclidean distance between obstacle $O$ at time $T_k$ and pose $s_k$ of the ego robot.

We modify the $\mathbf{o}_k(s_k)$ function because the original TEB Planner has the limitation that it only considers dynamic obstacles moving in constant velocity. Such limitation is not suitable for our application, since other robots, considered as obstacles by the ego robot, move in arbitrary trajectories.

The corresponding functions for the obstacle separation $\delta$ and homotopy class evaluation $\mathcal{H}$ are then extended accordingly as discussed in [3.3](#sec:obstacle_constraint){reference-type="ref+label" reference="sec:obstacle_constraint"} and [3.5](#sec:H_sign){reference-type="ref+label" reference="sec:H_sign"} , respectively.

## Obstacle Separation Extension {#sec:obstacle_constraint}

The dynamic obstacle separation $\delta$ is calculated using obstacle trajectory. A discrete trajectory $\tau$ can be directly obtained from TEB $\mathcal{B}$ in [\[eqn:teb\]](#eqn:teb){reference-type="ref+label" reference="eqn:teb"} by summing the total time up to that pose. $$\begin{equation}
\tau:= \{(T_1, s_1),(T_2, s_2),...,(T_n, s_n)\}
\end{equation}$$ where $T_k = \Delta T_1+\Delta T_2+...+\Delta T_{k-1}$

To estimate the obstacle pose at any time $t$, the obstacle pose is interpolated between two successive points in its trajectory. For holonomic robot, the obstacle pose is estimated by linear interpolation. For non-holonomic robot, each segment is assumed to be a circular arc.

The implementation of linear interpolation of obstacle pose is trivial. The circular interpolation is computed by considering the geometry of the circular arc, as shown in Fig.[4](#fig:constantArc){reference-type="ref" reference="fig:constantArc"}.

:::: {#fig:constantArc .figure latex-placement="htb"}
![](Chung2023Distributed_figs/constantArc2.png){width="90%"}

::: caption
Constant circular motion
:::
::::

By trigonometry: $$\begin{equation}
 \resizebox{0.91\hsize}{!}{
$\begin{cases}
& x(t_k + \Delta T) = x(t_k) + \frac{v(t_k)}{\omega(t_k)}(sin( \theta(t_k) + \omega(t_k) \Delta T) - sin(\theta(t_k)) ) \\
& y(t_k + \Delta T) = y(t_k) - \frac{v(t_k)}{\omega(t_k)}(cos( \theta(t_k) + \omega(t_k) \Delta T) - cos(\theta(t_k)) ) \\
& \theta(t_k + \Delta T) = \theta(t_k) + \omega(t_k)  \Delta T
\end{cases}$
}
\label{eqn:circularInterpolation}
\end{equation}$$

After obtaining the obstacle pose, the obstacle footprint is projected onto the pose, and the separation between the obstacle and the ego robot $\delta(s_k,O)$ can be computed accordingly by solving the geometric problem of minimum separation between two 2D shapes.

The above calculations require linear and angular velocities. These velocities need to be computed during trajectory generation, and then the trajectories containing poses, velocities and time are published among the robots.

## Trajectory Sharing {#sec:trajectory_sharing}

The latest planned trajectory is shared among robots through unidirectional broadcasting. The actual implementation is in the form of standard ROS publisher-subscriber communication. The trajectory is defined by the following message:

    std_msgs/Header header
    time priority
    teb_local_planner/ObstacleFootprint footprint
    teb_local_planner/TrajectoryPointSE2[] trajectory

$header$ which contains the timestamp of message generation is used to compensate communication delays while packet loss can be intrinsically handled by TCP. $priority$ is used in Prioritized Planning which will be discussed in [3.7](#sec:PP){reference-type="ref+label" reference="sec:PP"} . $footprint$ describes the dynamic obstacle (other robot) footprint, which can be point, circle, line, pill shape and polygon. $trajectory$ is represented by a series of trajectory points. Each point contains the $SE(2)$ pose \[x, y, $\theta$\], time and velocity which are necessary for the calculations in [3.3](#sec:obstacle_constraint){reference-type="ref+label" reference="sec:obstacle_constraint"} .

## New H-signature for Homotopic Planning {#sec:H_sign}

Parallel planning of multiple trajectories in different homotopy classes is a feature in TEB planner to avoid the optimization of TEB being trapped in a local minimum [@roesmann2015]. TEB approach uses H-signature to distinguish homotopy classes. The detailed definition of H-signature is given in \[15\]. The idea is briefly explained as follows:

::: myhl
The H-signature for a robot trajectory $\tau$ is the line integral of the magnetic field $\mathbf{B}$ created by a virtual current flowing along the trajectory of the obstacle(s): $$\begin{equation}
\mathcal{H}(\tau) = \int _{\tau} \mathbf{B}(l) \cdot d \mathbf{l}
\label{eqn:Hsigature}
\end{equation}$$ where the magnetic field $\mathbf{B}$ at any arbitrary point $\mathbf{r}$, due to the current flow in the obstacle trajectory $\mathcal{S}$, is given by: $$\begin{equation}
\mathbf{B}(\mathbf{r}) = \frac{1}{4\pi} \int _{\mathcal{S}} \frac{(\mathbf{x}-\mathbf{r}) \times  d \mathbf{x} }{ \left\lVert\mathbf{x}-\mathbf{r}\right\rVert^3 }
\label{eqn:bField}
\end{equation}$$
:::

Two trajectories generate the same H-signature if they are in the same homotopic class, according to Ampere's law: for a loop enclosing the obstacle trajectory, the line integral is one, otherwise zero. Considering two trajectories $\tau_1$ and $\tau_2$ which have the same start and goal and are in the same homotopy class, the loop $\tau_1 \cup -\tau_2$ will not enclose an obstacle, the H-signature of the loop will be zero: $$\begin{equation}
\resizebox{0.91\hsize}{!}{$
\begin{aligned}
& \mathcal{H}(\tau_1 \cup -\tau_2) = \int _{\tau_1 \cup -\tau_2} \mathbf{B} \cdot d \mathbf{l} = \int _{\tau_1} \mathbf{B} \cdot d \mathbf{l} - \int _{\tau_2} \mathbf{B} \cdot d \mathbf{l} = 0 
\\
\iff & \mathcal{H}(\tau_1) = \mathcal{H}(\tau_2)
\end{aligned}
$}
\label{same_H}
\end{equation}$$

However, the calculation of the H-signature requires double integration. For the original TEB planner, this is not a problem, since it only considers obstacles with constant velocity. In that case, the obstacle trajectory $\mathcal{S}$ will be a straight line in the 3D space and the $\mathbf{B}$-field has an analytical solution [@Bhatt2011].

In this work, we propose an alternative H-signature which requires only one line integral instead of two as proposed in the original paper. This is important as the H-signature needs to be efficiently computed multiple times in each planning cycle. The proposed $\mathbf{B}$-field is a fictional magnetic field that at any point on the obstacle trajectory $\mathcal{S}$, the $\mathbf{B}$-field is considered as a local horizontal planar magnetic field generated by an upward current I.

Let $\mathbf{x} = (f(t), g(t), t)^T$ be a point on the obstacle trajectory $\mathcal{S}$. At any point $\mathbf{r}$ in space-time $(x, y, t)^T$, the $\mathbf{B}$ field experienced by the robot is: $$\begin{equation}
\resizebox{0.91\hsize}{!}{$
\mathbf{B}(\mathbf{r}) = \frac{1}{2 \pi}(\frac{y-g(t)}{(x-f(t))^2+(y-g(t))^2}, -\frac{x-f(t)}{(x-f(t))^2+(y-g(t))^2}, 0)^T
$}
\label{eqn:newB}
\end{equation}$$ Or in cross product form: $$\begin{equation}
\mathbf{B}(\mathbf{r}) = \frac{1}{2 \pi} \frac{(\mathbf{x}-\mathbf{r}) \times \boldsymbol{\hat{{k}}} }{ \left\lVert\mathbf{x}-\mathbf{r}\right\rVert^2 }
\end{equation}$$ The factor $\frac{1}{2\pi}$ is chosen for scaling and has no actual effect.\
This $\mathbf{B}$-field shows correct behaviours in distinguishing homotopy classes during testing.

After analysing this $\mathbf{B}$-field, we find that this $\mathbf{B}$-field is a good approximation under general conditions.\
The curl of field $\mathbf{B}$, $\nabla \times \mathbf{B}$ is: $$\begin{equation}
\resizebox{0.91\hsize}{!}{$
\begin{aligned}
& \frac{f'(t) ((x-f(t))^2 - (y-g(t))^2)+2g'(t)(x-f(t))(y-g(t))}{((x - f(t))^2 + (y - g(t))^2)^2} \boldsymbol{\hat{{\imath}}} \\
 & + \frac{g'(t) ((y-g(t))^2 - (x-f(t))^2)+2f'(t)(x-f(t))(y-g(t))}{((x - f(t))^2 + (y - g(t))^2)^2} \boldsymbol{\hat{{\jmath}}}\\
 & + 0 \boldsymbol{\hat{{k}}}\\
\end{aligned}
$}
\label{eqn:curl}
\end{equation}$$

For the x and y component, the numerator part is a hyperbolic paraboloid with the position of the obstacle at the centre. The denominator part is the inverse of obstacle distance to the fourth power. For example, if the obstacle velocity $f'(t) = g'(t) = 1$ with obstacle position (f(t), g(t)) being the origin, the x and y components become $\frac{\pm (x^2-y^2)+2xy}{(x^2+y^2)^2}$, which equates to zero other than at the position of the obstacle, as shown in [5](#fig:contour_plot){reference-type="ref+label" reference="fig:contour_plot"} .

By Kelvin--Stokes theorem, the line integral along a loop is equal to the surface integral of the curl over the surface bounded by the loop. The surface integral will be almost zero when the loop does not enclose the obstacle and does not have a small obstacle separation compared to obstacle velocity. For two trajectories that have the same homotopic class, the overall H-signature is approximately zero and fulfil [\[same_H\]](#same_H){reference-type="ref+label" reference="same_H"} . Therefore, the proposed alternative H-signature satisfies our application.

:::: {#fig:contour_plot .figure latex-placement="htb"}
![](Chung2023Distributed_figs/contour_plot.png){width="50%"}

::: caption
Contour plot of $|\frac{x^2 - y^2 +2xy}{(x^2+y^2)^2}|$
:::
::::

## Voronoi Roadmap {#sec:voronoi}

Since our DTEB Planner is designed to be used in industrial environment, we need to further improve the planner's ability in sampling trajectories for homotopy class planning.

The original TEB planner creates a Probabilistic Roadmap in each planning cycle, and candidate trajectories are sampled from the roadmap by comparing their homotopy classes with the existing candidates [@roesmann2015]. The roadmap is efficient in an open space scenario where the obstacle space constitutes only a small part of the overall workspace. However, in a warehouse environment where there are only narrow aisles in which the robots can travel, a simple probabilistic roadmap can hardly sample any feasible trajectory as shown in [6](#fig:roadmap_a){reference-type="ref+label" reference="fig:roadmap_a"} .

:::: {#fig:voronoi_rviz .figure latex-placement="!htb"}
::: {#fig:roadmap_a .figure}
![image](Chung2023Distributed_figs/roadmap_rviz_cropped.png){width="90%"} []{#fig:roadmap_a label="fig:roadmap_a"}
:::

::: {#fig:roadmap_b .figure}
![image](Chung2023Distributed_figs/voronoi_rviz_narrow.png){width="90%"} []{#fig:roadmap_b label="fig:roadmap_b"}
:::

::: caption
Homotopy class planning using roadmap
:::
::::

We extend the homotopy class planning by using a generalized Voronoi diagram (GVD). Similar approaches of homotopy class planning by sampling paths from GVD are proposed in [@Kuderer2014] and [@Roesmann2017IntegratedOT]. In [@Kuderer2014] a grid-based approach is used, which has a total computation time of GVD construction and graph search in the magnitude of 100ms. Such computation time is too large for TEB planner, as the planner is expected to run at 20Hz. [@Roesmann2017IntegratedOT] reports an implementation using Boost library which is based on sweepline algorithm in [@Fortune1987] and has computation time in the magnitude of 10ms. However, the actual implementation is not explained in the paper or open-sourced. Therefore, we implement a new open-source ROS plugin using OpenCV and Boost library. The total time for GVD and graph search takes only 10-20ms for a 300x300 pixels local costmap.

## Prioritized Planning {#sec:PP}

The researches in Prioritized Planning show that some deadlocks can only be solved by Prioritized Planning, but not Reciprocal Avoidance [@CAP2015] [@priority2001]. In this work, we propose a 2-stage priority scheme that takes the advantages of both Reciprocal Avoidance and Prioritized Planning.

The planning is divided into 2 stages according to the robot's Euclidean distance to the obstacle. The first stage is the prioritized stage. In this stage, Prioritized Planning similar to [@CAP2015] is carried out, with the difference that the planning order of our planner is not synchronized in sequential manner. The robots are given an initial priority. The lower priority robots treat the higher priority robots as moving obstacles following their latest published trajectories. This priority can be manually assigned or determined by heuristic metrics. In our implementation, for simplicity, the priority is determined according to chronological order. The robot with a more recent navigation task has a higher priority. The planner first tries to find a locally optimal solution according to the initial priority. If there is no feasible solution, the planner would raise the priority of the ego robot, similar to the method used in [@andreychuk2018techniques].

The second stage is reciprocal avoidance stage, in this stage the ego robot considers all robots as obstacles regardless of their priority. The target of this stage is to find a solution that can only be reached by a reciprocal strategy. Since all other robots are considered as moving obstacles by the ego robot, this stage also ensures safety when the robots are in the vicinity.

# Experiments

In this section, we demonstrate the effectiveness of our planner in comparison to the related work in terms of the reactive and predictive avoidance scenarios. Two separate sets of tests are designed for the two scenarios respectively. The first test is designed for reactive avoidance, in which the robots on the perimeter of a circle have to travel to their antipodal positions. This circle test is also widely used in other multi-robot planners, such as [@Snape2011] [@Defoort2010]. The second test is designed for predictive avoidance, in which the robots have to travel in a warehouse map consisting of narrow corridors, so as to simulate an environment full of potential deadlocks.

## Reactive Avoidance Tests

:::: {#fig:stage_six .figure latex-placement="htb"}
![](Chung2023Distributed_figs/stage_six_no_num.png){width="45%"}

::: caption
Setup for testing of reactive behaviour between six robots
:::
::::

To study the reactive behaviour involving multiple robots, the planner is tested in Stage simulator using the setup shown in [9](#fig:stage_six){reference-type="ref+label" reference="fig:stage_six"} . Six robots are placed in a circle of diameter of 10 m, and the antipodal positions are used as the goals. Each test is repeated five times to ensure consistent results. The computer environment is Ubuntu 20.04 with an Intel(R) Xeon(R) X5675 \@3.07GHz CPU. The simulation is run at 60% speed due to computational burdens of running multiple instances of the planner.

Since HRVO is a well-proven planner for reactive collision avoidance as mentioned in [2](#sec:related_work){reference-type="ref+label" reference="sec:related_work"} , the same test is performed with a HRVO planner for comparison. For this purpose, the ROS implementation by [@Claes2012] is used. [\[tab:comparison_reactive\]](#tab:comparison_reactive){reference-type="ref+label" reference="tab:comparison_reactive"} shows the average values of the distance travelled, the duration to finish a run and the computation time, along with their standard deviations.

As seen in [12](#fig:sample_trajectories){reference-type="ref+label" reference="fig:sample_trajectories"} , the trajectories of DTEB are less regular than HRVO. It is caused by the symmetrical setting in this scenario as it has the same cost for a robot to go around another robot on left or on the right. In contrast, HRVO has a heuristic rule to favour one side and produce more regular trajectories (For details see[@Snape2011]). Although the proposed DTEB Planner has less regular trajectories, it outperforms the HRVO planner in travel time by a small margin. The major reason is that the HRVO planner has a simple (non-time optimal) homing strategy for the selection of preferred velocity. The planner performs unnecessary deceleration and turning in place at the goal to satisfy the goal orientation. In contrast, the DTEB planner already considers a time optimal deceleration and turning as part of the planning.

:::: {#fig:sample_trajectories .figure latex-placement="!htb"}
::: {#fig:teb1 .figure}
![image](Chung2023Distributed_figs/teb_large.png){width="95%"} []{#fig:teb1 label="fig:teb1"}
:::

::: {#fig:hrvo .figure}
![image](Chung2023Distributed_figs/hrvo_large.png){width="95%"} []{#fig:hrvo label="fig:hrvo"}
:::

::: caption
:::
::::

## Predictive Avoidance Tests

The existing HRVO planners do not consider deadlocks in the long-term future time. Therefore, we mainly use a Multi-Robot Route Planner $tuw\_multi\_robot$ in [@Binder2019] for comparison instead. The TUW Route Planner is an offline trajectory planner, which generates a centralized routing plan consisting of robot paths from start to goal positions and their temporal information. The robots' local planner then simply follow the routing plan.

:::: {#fig:stage_8_robots .figure latex-placement="htb"}
![](Chung2023Distributed_figs/stage_8_robots.png){width="50%"}

::: caption
Eight-robot predictive avoidance test in a warehouse map
:::
::::

To further examine the proposed planner's capability in predictive collision avoidance, we test the planner using more robots in Stage simulator. A warehouse-like map from [@Binder2019] is modified for the testing, as shown in [13](#fig:stage_8_robots){reference-type="ref+label" reference="fig:stage_8_robots"} .

:::: {#fig:warehouse_tuw_1 .figure latex-placement="htb"}
::: {#fig:warehouse_teb_1 .figure}
![image](Chung2023Distributed_figs/warehouse_teb_1_run2.png){width="95%"} []{#fig:warehouse_teb_1 label="fig:warehouse_teb_1"}
:::

::: {#fig:warehouse_tuw_1 .figure}
![image](Chung2023Distributed_figs/tuw_warehouse_1.png){width="95%"} []{#fig:warehouse_tuw_1 label="fig:warehouse_tuw_1"}
:::

::: caption
Predictive test using opposite positions as goals
:::
::::

:::: {#fig:warehouse_tuw_2 .figure latex-placement="htb"}
::: {#fig:warehouse_teb_2 .figure}
![image](Chung2023Distributed_figs/warehouse_teb_2.png){width="95%"} []{#fig:warehouse_teb_2 label="fig:warehouse_teb_2"}
:::

::: {#fig:warehouse_tuw_2 .figure}
![image](Chung2023Distributed_figs/warehouse_tuw_2.png){width="95%"} []{#fig:warehouse_tuw_2 label="fig:warehouse_tuw_2"}
:::

::: caption
Predictive test using asymmetric goal positions
:::
::::

First, we assign the robots' opposite positions as the goals. The proposed planner is able to perform avoidance and wait at the crossroads as shown in [14](#fig:warehouse_teb_1){reference-type="ref+label" reference="fig:warehouse_teb_1"} .

To add more variety, the test is repeated, but the upper 4 robots use opposite positions as their goals while the lower 4 robots use the diagonal positions as their goals so that the goal positions are asymmetric. Now, there are potential deadlocks involving 3-4 robots in the middle of the map. The proposed planner is still able to handle this scenario without collisions or deadlocks, as shown in [17](#fig:warehouse_teb_2){reference-type="ref+label" reference="fig:warehouse_teb_2"} .

The TUW Route Planner which also employs Prioritized Planning is able to handle these scenarios. The resultant robot trajectories are shown in [16](#fig:warehouse_tuw_1){reference-type="ref+label" reference="fig:warehouse_tuw_1"} and [19](#fig:warehouse_tuw_2){reference-type="ref+label" reference="fig:warehouse_tuw_2"} . The comparison between the proposed DTEB Planner and TUW Planner is shown in [\[tab:comparision_predictive\]](#tab:comparision_predictive){reference-type="ref+label" reference="tab:comparision_predictive"} .

For the first task, the TUW Route Planner has worse performance, as it takes a detouring path on the left. For the second task, the two planners have similar performance as the task is more complicated. If the task and map become more complicated, TUW Route Planner should outperform the proposed planner, as it has centralized and global information about the planning task. However, since the TUW Route Planner is not an online trajectory/motion planner, it cannot perform reactive avoidance itself.

In comparison to other methods, the HRVO Planner fails to avoid deadlocks in this map. The planner assumes the robots maintain constant velocity for a short period of time and cannot find the solution of avoiding and waiting at a crossroad. The robots will either be stuck in deadlocks or even collide, as shown in [20](#fig:warehouse_hrvo){reference-type="ref+label" reference="fig:warehouse_hrvo"} .

:::: {#fig:warehouse_hrvo .figure latex-placement="htb"}
![](Chung2023Distributed_figs/new_HRVO_fail.png){width="80%"}

::: caption
HRVO Planner is trapped in deadlock in the warehouse map
:::
::::

# Discussion and Conclusion

In this paper, we proposed a novel Distributed Timed Elastic Band Planner for multi-robot trajectory planning. The planner combines Prioritized Planning and TEB to allow both reactive and predictive collision avoidance.

Our proposed planner shows better versatility than the previous planners. Reactive planners like HRVO cannot predict long term deadlocks, and route planners like TUW Route Planner cannot perform reactive avoidance. Meanwhile, our proposed planner has a performance similar to or even slightly better than these planners under the discussed environment settings. Also, our proposed planner is integrated into ROS navigation stack and has the consideration of robot perception. Beside considering other robots as obstacles using their shared trajectory, the planner can also consider other obstacles perceived by the laser scanner, such as unknown objects on the floor or human operators. The existing pipeline from the single-robot TEB planner is used to track the obstacles.

However, the well-rounded functionality comes at the cost of relatively high computational burden. Although the computational efficiency of the proposed planner is still similar to the original TEB Planner, it is not as efficient as the HRVO or TUW Route Planner, which can control a dozen of robots using a single computer.

Future study can use real world robots to further validate the planner's performance in real-life application, and GPU accelerated optimization can be implemented to further improve the efficiency.

The ROS implementation and test sets are published in GitHub repository <https://github.com/chungym/distributed_teb_multi_robot>.

[^1]: This work was partially supported by Bundesministerium für verkehr und digitale infrastruktur (BMVI) in the context of the project 45KI02B021 \"Silicon Economy Logistics Ecosystem\"

[^2]: $^{1}$Faculty of Electrical Engineering and Information Technology, Technische Universität Dortmund, 44227 Dortmund, Germany

[^3]: $^{2}$Chair of Material Handling and Warehousing, Faculty of Mechanical Engineering, Technische Universität Dortmund, 44227 Dortmund, Germany

[^4]: `{yiu-ming.chung, hazem.youssef, moritz.roidl} @tu-dortmund.de`
