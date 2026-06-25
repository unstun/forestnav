---
citation_key: Hu2024Swept
arxiv_id: 2412.16875
arxiv_url: https://arxiv.org/abs/2412.16875
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:49:43Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
LIDAR, Multi-Axle, AMRs, SDF, Trajectory Estimation.
:::

# Introduction

Logistics is a vital component of modern society, which facilitates the flow of goods and services. Although large multi-axle trucks [@zhao2019modelling; @islam2020planning] offer capacity and efficiency, they face several significant maneuverability challenges [@yuan2021survey] in constrained urban environments.

A critical challenges is the swept volume [@zhang2023continuous; @wang2024implicit] of multi-axle vehicles, as the rear axles follow different paths from the front during turns [@liu2020experimental], as shown in Fig. [1](#fig:firstpage){reference-type="ref" reference="fig:firstpage"}. This increases the risk of entering adjacent lanes, sidewalks, or obstacles. Current automated driving systems are insufficient for addressing this problem, as they are primarily designed for smaller vehicles [@yang2024e2e] (i.e., cars) and fail to optimize for the unique dynamics of multi-axle configurations [@zhao2019modelling].

![This work aims to reduce the minimal swept volume and ensure stable trajectory tracking, enhancing safety in industrial applications..](Hu2024Swept_figs/motivation.png){#fig:firstpage width="100%"}

The challenge lies in managing the swept volume while ensuring that each axle follows a safe and efficient path in real-time [@wang2024implicit; @zhang2023continuous]. Existing methods for path planning [@bai2021multi; @bian2023risk; @jin2024gs; @liu2023safe; @cao2023path; @cao2023neptune; @li2024jacquard; @zhao2024design; @yang2024trace; @fan2024flying; @yu2024aggressive; @Bai2025Realm] and control [@cao2019bearing; @liu2023non; @hu2023stackelberg; @cao2020online; @liu2023multiple; @xu2024cost; @er2013development; @jia2023evolver; @liu2024distance; @ji2024integration] typically simplify the vehicle as a single rigid body [@lee2022cyclops], which does not account for the independent control needed for each axle in multi-axle systems. As a result, these approaches [@bai2021multi; @bian2023risk; @jin2024gs; @liu2023safe; @cao2023path; @cao2023neptune; @li2024jacquard; @zhao2024design; @yang2024trace; @fan2024flying; @yu2024aggressive; @Bai2025Realm; @cao2019bearing; @liu2023non; @hu2023stackelberg; @cao2020online; @liu2023multiple; @xu2024cost; @er2013development; @jia2023evolver; @liu2024distance; @ji2024integration] struggle to minimize swept volume, especially in complex environments.

To address this challenge, we propose a novel approach that integrates swept volume-aware path planning with model predictive control (MPC) for Swerve-Drive autonomous mobile robots (AMR) systems. Our method optimizes the trajectory of the vehicle in real-time, minimizing the swept volume while allowing each wheel to turn independently. By utilizing MPC, we can predict the future state of the vehicle and adjust the turning radius of each wheel, ensuring precise navigation through tight spaces without compromising safety or efficiency.

This approach not only tackles the limitations of current systems, but also sets the foundation for safer and more robust multi-axle AMR operations in real-world environments. By reducing swept volume and improving control over each axle, our method paves the way for more reliable autonomous heavy vehicles, particularly in logistics and industrial applications.

The main contributions of this work are as follows.

- We propose a unified approach that integrates swept volume-aware path planning with MPC to optimize the trajectory and independently control each wheel of multi-axle AMRs, ensuring precise maneuverability in constrained environments.

- We propose a method for calculating the steering angles of each wheel group in multi-axle vehicles based on velocity vectors, simplifying the vehicle model and facilitating the use of MPC control.

- We validate the approach, showing significant reductions in swept volume and improved real-time trajectory tracking using CUDA, enabling more reliable and efficient autonomous heavy-duty AMR applications.

- We will open-source our work for the benefit of the community. <https://github.com/ccwss-maker/svplan>

:::: {#fig:process .figure latex-placement="t"}
![](Hu2024Swept_figs/processflow.png){width="80%"}

::: caption
The proposed solution uses LiDAR inertial odometry [@nguyen2024eigen] for front-end odometry, with multi-stage back-end planning and MPC to minimize swept volume iteratively.
:::
::::

# Related Work

In trajectory planning, swept volume detection is critical for obstacle avoidance of semi-trucks and service AMRs, yet few works address this issue comprehensively [@zhao2019modelling; @liu2020experimental; @baxter2020deep; @chiang2021fast; @zips2015optimisation; @cao2019preview]. Basic methods, such as [@ilic2018vehicle], rely on GPS for odometry [@chen2024salient; @esfahani2019deepdsair; @yang2024fast; @10612831; @ji2022robust; @Li2024graph; @esfahani2018new; @10801455; @esfahani2020local; @10802614; @jin2024robust; @10802691; @li2024hcto; @Nguyen2025ULOC; @li2024ua; @yin2024outram; @ji2024sgba; @esfahani2021learning; @esfahani2019towards; @lyu2023spins] and body frame integration, leading to significant calculation errors. Täubig et al. [@Täubigsweptvolume] propose a two-stage approach, combining broad-phase detection for quick collision identification [@yuan2014Autonomous] with narrow-phase detection [@wang2015automatic; @wang2017heterogeneous] using the GJK algorithm for precise calculations [@wu2019depth]. Although this method balances speed and accuracy, it performs poorly in complex environments compared to the SDF-based approach [@WangSDF]. However, the SDF-based approach [@WangSDF; @wang2024implicit; @zhang2023continuous] often lacks real-time performance, suffers from heading tracking issues, and does not integrate traffic rules, which limits its applicability in more practical scenarios.

For trajectory tracking [@lyu2021vision; @qi2024air], controlling the steering angles of each wheel in multi-axle Swerve-Drive AMRs in real-time is a highly complex task. While dynamic models with varying degrees of freedom have been studied [@xu2022hierarchical; @wang2023multi; @gao2014turning; @zhang2022dual; @hu2016control; @wu2017optimizing], these works often overlook the geometric aspects of steering, failing to fully utilize the flexibility of multi-axle independent steering. To address this, models such as Ackerman Steering [@chaudhuri2009kinematic; @wu2021learn], Active Front and Rear Steering (AFRS) [@ye2016steering], and Front Wheel Steering (FWS) [@xu2022hierarchical] have been proposed, but their steering centers are typically constrained along the first, last or middle axles, limiting maneuverability. In contrast, D-based steering models [@zhang2016study; @zhang2015steering; @zhang2015steering1] allow the steering center to be distributed more flexibly, enhancing steering performance. However, transitioning between different steering modes depending on road conditions still introduces transient disturbances.

# Proposed Solution

## Problem Statement

Let $\xi \in \mathbb{R}$ represent the two-dimensional top-view area of the AMR, assuming the vehicle shape remains constant during motion. The objective of this work is to minimize the swept volume $\mathbb{V} = \cup_{t \in [t_{s}, t_{e}]} \xi \mathcal{L}(t) h$, where $h \in \mathbb{R}$ is the constant height of the vehicle and $\mathcal{L}(t)$ denotes the trajectory. The swept volume is defined as the three-dimensional volume swept by the vehicle during its motion. For computational efficiency, we neglect the vehicle's lateral tilt. Since $h$ is constant, minimizing $\mathbb{V}$ is equivalent to minimizing the swept area $\mathbb{S}$, which is the two-dimensional top-view projection of $\mathbb{V}$. This minimization is achieved by optimizing the trajectory control points $\mathcal{L} = \left\{ \left( x_j, y_j, \varphi_j \right) \in \mathbb{SE}(2) \mid j = 1, 2, \dots, N-1 \right\}$ and implementing an MPC controller with control input $u = [V_x, V_y, \omega]^\top \in \mathbb{R}^3$, where $V_x$, $V_y$, and $\omega$ represent the longitudinal, lateral, and rotational velocities of the AMR, respectively.

## Trajectory Planning

As shown in Fig. [2](#fig:process){reference-type="ref" reference="fig:process"}, the trajectory planning process consists of four steps. First, the A\* algorithm is used to generate an initial feasible path. Then, based on this path, a corresponding heading sequence is estimated. Together, the path and heading sequence form the initial trajectory, denoted by $\mathcal{L}^{A*}(t)$. Subsequently, $\mathcal{L}^{A*}(t)$ is utilized in the first optimization step to generate an initial smoothed continuous trajectory $\mathcal{L}^{F}_{M}(t)$. Finally, $\mathcal{L}^{F}_{M}(t)$ is further optimized in the second optimization step to avoid obstacles and minimize the swept volume $\mathbb{S}$, resulting in the final continuous trajectory $\mathcal{L}^{S}_{M}(t)$.

The superscript in $\mathcal{L}^{F}_{M}(t)$ and $\mathcal{L}^{S}_{M}(t)$ denotes the first and second optimization steps, respectively, where both trajectories are represented using the minimum control effort polynomial trajectory class (MINCO) [@wang2022geometrically]. The MINCO is designed to optimize a trajectory by minimizing the control effort while fitting a set of $N$ discrete path points into $N-1$ continuous polynomial segments. Each polynomial segment $P_j(t)$ represents a quintic curve and is optimized over time durations $T_j$. The complete trajectory is represented by: $$\mathcal{L}_M = \left\{ P_j(t) : [0, T_j] \to \mathbb{R}^3 \mid j = 1, 2, \dots, N-1 \right\},$$ where each segment $P_j(t)$ is described by a quintic polynomial: $$P_j(t) = C_{0,j} + C_{1,j} t + C_{2,j} t^2 + C_{3,j} t^3 + C_{4,j} t^4 + C_{5,j} t^5.$$ The coefficients $C_{i,j} \in \mathbb{R}^{3}$ are determined by the control points of the trajectory $q = [q_1, q_2, \dots, q_{N-1}] \in \mathbb{R}^{(N-1)\times3}$ and the for each polynomial segment $T = [T_1, T_2, \dots, T_{N-1}]\in \mathbb{R}^{N-1}$, as defined by the mapping function: $$C_{i,j} = M(i, j, q, T),$$ where: $i~\in~[0, 5]$ denotes the index of coefficients in $C_{i,j}$ for the j-th component.

### First Optimization

The first optimization is intended for smoothing of the trajectory by minimizing energy consumption and time consumption of the trajectory while ensuring that the trajectory follows $\mathcal{L}^{A*}(t)$. The optimization problem is defined as: $$\begin{equation}
\min_{q, T} \; \mathbb{W}_E \cdot J_E + \mathbb{W}_T \cdot J_T + \mathbb{W}_P \cdot J_P,
\end{equation}$$ where $\mathbb{W}_E$, $\mathbb{W}_T$, and $\mathbb{W}_P$ are the weights for energy consumption, time consumption, and trajectory deviation, respectively, and $J_E$, $J_T$, and $J_P$ represent energy loss, time loss, and trajectory deviation loss. The gradients of $J_E$ and $J_T$ with respect to $C_{i,j}$ and $T_j$, including $\partial J_E / \partial T_j$, $\partial J_E / \partial C_{i,j}$, $\partial J_T / \partial T_j$, and $\partial J_T / \partial C_{i,j}$, have been rigorously derived in [@wang2024implicit] and will not be revisited in this paper. $J_P$ and its gradients are shown as follows: $$\begin{equation}
J_P = \sum_{j=1}^{N-1} (P_j - P_{A^*, j})^2,
\end{equation}$$ $$\begin{equation}
\frac{\partial J_P}{\partial P_j} = 2(P_j - P_{A^*, j}),
\end{equation}$$ $$\begin{equation}
\frac{\partial J_P}{\partial T_j} = \frac{\partial J_P}{\partial P_j} \cdot \frac{\partial P_j}{\partial T_j} = \frac{\partial J_P}{\partial P_j} \cdot V_j.
\end{equation}$$ Here, $P_{A^*, j}$ represents the initial trajectory points in $\mathcal{L}^{A*}(t)$, and $V_j = [V_X, V_Y, \omega]^T$ is the velocity matrix at the corresponding trajectory point, where $V_X$ and $V_Y$ are the velocities in the vehicle $X$- and $Y$-coordinates, and $\omega$ is the angular velocity. The optimization is performed using the LBFGS [@coppola2020lbfgs], resulting in the initial optimized trajectory $\mathcal{L}^{F}_{M}(t)$.

### Second Optimization

In this stage, the optimization objectives are to minimize energy, total time, and safety distance, and to reduce the size of the swept area. Therefore, the optimization problem is defined as: $$\begin{equation}
\min_{q, T} \; \mathbb{W}_E \cdot J_E + \mathbb{W}_T \cdot J_T + \mathbb{W}_{ob} \cdot J_{ob} + \mathbb{W}_{sv} \cdot J_{sv}.
\end{equation}$$ Here, $\mathbb{W}_E$, $\mathbb{W}_T$, $J_E$, and $J_T$ are the same as those in the previous stage. $\mathbb{W}_{ob}$ and $\mathbb{W}_{sv}$ represent the weights for obstacle safety distance and swept area, respectively, while $J_{ob}$ and $J_{sv}$ are their corresponding cost functions. The cost function $J_{ob}$ and its partial derivatives with respect to $P_j$ and $T_j$, i.e., $\partial J_{ob} / \partial T_j$ and $\partial J_{ob} / \partial P_j$, are calculated using the Signed Distance Field (SDF) [@zhang2023continuous]. In the top-down view as shown in Fig. [3](#fig:modeling){reference-type="ref" reference="fig:modeling"}, the vehicle is approximated as a rectangle. The vehicle coordinate system is defined with its origin located at the geometry center of the vehicle. The X- and Y-axes are aligned with the vehicle's longitudinal and lateral directions, respectively. For a point $P_{veh} = [X_{veh}, Y_{veh}]^T$ in the vehicle coordinate system, its distances to the vehicle's boundary, denoted as $dx$ and $dy$, are given by: $$\begin{equation}
dx = \lvert X_{veh} \rvert - \frac{L}{2}, \quad dy = \lvert Y_{veh} \rvert - \frac{W}{2},
\end{equation}$$ where $L$ and $W$ denote the length and width of the vehicle, respectively. Therefore, the SDF function $f_{SDF}(P_{veh})$ is defined as: $$\begin{equation}
\begin{cases} 
\sqrt{dx^2 + dy^2}, & \text{if } dx > 0 \text{ and } dy > 0, \\
\max(dx, dy), & \text{otherwise}.
\end{cases}
\label{eq:fsdf}
\end{equation}$$ Thus, the gradient of the SDF, $\nabla f_{\text{SDF}}(P_{\text{veh}})$, is computed as follows: $$\begin{equation}
\begin{cases}
\left( \frac{dx\cdot \text{sign}(X_{\text{veh}})}{\sqrt{dx^2 + dy^2}}, \frac{dy\cdot \text{sign}(Y_{\text{veh}})}{\sqrt{dx^2 + dy^2}} \right), & \text{if } dx > 0 \text{ and } dy > 0, \\
\left( \text{sign}(X_{\text{veh}}), 0 \right), & \text{else if } dx \geq dy, \\
\left( 0, \text{sign}(Y_{\text{veh}}) \right), & \text{otherwise}.
\end{cases}
\end{equation}$$

![Vehicle Parametric Model](Hu2024Swept_figs/model.png){#fig:modeling width="100%"}

Therefore, when the vehicle is at the $j$-th control point, the obstacle $P_{\text{ob}} = [X_{\text{ob}}, Y_{\text{ob}}]^T$ in the global coordinate system (with its origin at the first control point) is characterized by the vehicle's SDF and gradient as: $$\begin{equation}
F_{\text{SDF}}(P_{ob}, j) = f_{\text{SDF}}(R^{-1}(j)(P_{\text{ob}} - T(j)),
\end{equation}$$ $$\begin{equation}
\nabla F_{\text{SDF}}(P_{ob}, j) = R(j) \nabla f_{\text{SDF}}(R^{-1}(j)(P_{\text{ob}} - T(j))),
\end{equation}$$ where $R(j)$ and $T(j)$ represent the rotation matrix and translation vector of the AMR from the first to the $j$-th control point, respectively. The cost function $J_{\text{ob}}$ is defined as follows: $$\begin{equation}
J_{\text{ob}} = \sum_{j=1}^{N-1} \sum_{k=1}^{N_{ob}} J^{'}_{\text{ob}}(k, j),
\end{equation}$$ where $k$ represents the obstacle index, and $N_{ob}$ represents the number of obstacles. The cost function $J^{'}_{\text{ob}}(k, j)$ is defined as follows: $$\begin{equation}
\begin{cases}
(d_{\text{th}}-F_{\text{SDF}}(P_{\text{ob}}(k), j))^3, & \text{if } F_{\text{SDF}}(P_{\text{ob}}(k), j) < d_{\text{th}}, \\
0, & \text{otherwise},
\end{cases}
\end{equation}$$ where $d_{\text{th}}$ represents the safety distance threshold. In conclusion, the gradients of $J_{\text{ob}}$ with respect to $P_j$ and $T_j$, i.e., $\partial J_{\text{ob}} / \partial P_j$ and $\partial J_{\text{ob}} / \partial T_j$, are given by: $$\begin{equation}
\frac{\partial J_{\text{ob}}}{\partial P_j} = \sum_{k=1}^{N_{ob}}\nabla F_{\text{SDF}}(P_{\text{ob}}(k, j)),
\end{equation}$$ $$\begin{equation}
\frac{\partial J_{\text{ob}}}{\partial T_j} = \frac{\partial J_{\text{ob}}}{\partial P_j} \cdot \frac{\partial P_j}{\partial T_j} = \frac{\partial J_{\text{ob}}}{\partial P_j} \cdot V_j.
\end{equation}$$ For the swept area, ensuring that the shortest side of the vehicle is always perpendicular to the trajectory, i.e., the long axis of the vehicle is tangent to the trajectory, can reduce the swept area. Therefore, the cost function $J_{\text{sv}}$ and its gradients are given as follows: $$\begin{equation}
\Delta \varphi_j =  \varphi_j - \arctan\left(\frac{V_{Y, j}}{V_{X, j}}\right),
\end{equation}$$ $$\begin{equation}
J_{\text{sv}} =  \sum_{j=0}^{N_{\text{p}}} (\Delta \varphi_j)^2,
\end{equation}$$ $$\begin{equation}
\frac{\partial J_{\text{sv}}}{\partial \varphi_j} = 2 \Delta \varphi_j,
\end{equation}$$ $$\begin{equation}
\frac{\partial J_{\text{sv}}}{\partial X_j} = 2 \Delta \varphi_j \left( \frac{- V_{Y, j}}{V_{X, j}^2 + V_{Y, j}^2} \right),
\end{equation}$$ $$\begin{equation}
\frac{\partial J_{\text{sv}}}{\partial Y_j} = 2 \Delta \varphi_j \left( \frac{V_{X, j}}{V_{X, j}^2 + V_{Y, j}^2} \right),
\end{equation}$$ $$\begin{equation}
\frac{\partial J_{\text{sv}}}{\partial T_j} = \frac{\partial J_{\text{sv}}}{\partial \varphi_j} \cdot \omega_j + \frac{\partial J_{\text{sv}}}{\partial X_j} \cdot V_{X, j} + \frac{\partial J_{\text{sv}}}{\partial Y_j} \cdot V_{Y, j},
\end{equation}$$ where $\omega_j$ represents the yaw rate, and $V_{X, j}$ and $V_{Y, j}$ represent the velocities of AMR in the X- and Y-directions at the $j$-th control point, respectively. The final trajectory $\mathcal{L}^{S}_{M}(t)$ is obtained by optimizing using the LMBM [@karmitsa2020limited].

### Swept Area Estimation

From Equation ([\[eq:fsdf\]](#eq:fsdf){reference-type="ref" reference="eq:fsdf"}), the SDF of a point $P$ in space with respect to the vehicle's trajectory at time $t$ is given by: $$\begin{equation}
F_{\text{SDF}}(P, t) = f_{\text{SDF}}(R^{-1}(t)(P - T(t))),
\label{eq:fsdft}
\end{equation}$$ where $R(t)$ and $T(t)$ represent the vehicle's rotation matrix and translation matrix from time 0 to time $t$. To compute the swept-volume SDF of the vehicle along its trajectory, for each point on the map, we compute its minimum distance to the vehicle's swept area by evaluating all vehicle poses from initial time $t_{\text{min}}$ to final time $t_{\text{max}}$. Since for any point, there exists a unique time instant $t^*$ at which the minimum distance occurs, the Armijo line search method [@armijo1966minimization] can be employed to find this optimal time $t^*$. By substituting $t^*$ into Equation ([\[eq:fsdft\]](#eq:fsdft){reference-type="ref" reference="eq:fsdft"}), we can obtain the minimum distance $f_{\text{SDF}}^* = F_{\text{SDF}}(P, t^*)$ at a point $P$.

To calculate the SDF for the swept area, an $\mathbb{N} \times \mathbb{N}$ grid map is constructed over the region of interest. For each of the $\mathbb{N}^2$ grid points, multiple iterations of the Armijo line search method are required to determine the optimal time $t^*$. Once $t^*$ is obtained, it is then used to calculate $f_{\text{SDF}}^*$. This process is computationally intensive and time-consuming. However, using CUDA, we can assign $\mathbb{N}^2$ threads to simultaneously compute $t^*$ for all grid points, greatly accelerating the computation.

## Trajectory Tracking

As shown in Fig. [4](#fig:MPCcontrol){reference-type="ref" reference="fig:MPCcontrol"}, the $i$-th wheel is located at $X_{wi} \in \left(-{L}/{2}, {L}/{2}\right)$ along the vehicle's X-axis, with the left and right wheels positioned at $Y_{wi} \in \left\{ -{W}/{2}, {W}/{2} \right\}$ along the Y-axis.

![Multi-Axle AMR MPC tracking control.](Hu2024Swept_figs/MPCcontrol.png){#fig:MPCcontrol width="90%"}

The state vector is chosen as $\mathbf{X} = [x, y, \varphi]^T$, and the control vector is $u = [V_{x}, V_{y}, \omega]^T$. The discretized vehicle control state-space equation can be obtained as: $$\begin{equation}
 \mathbf{X}(k+1) = A\mathbf{X}(k)+Bu(k),
\label{eq:3}
\end{equation}$$ where $A$ is identity matrix, $B$ is a diagonal matrix with $T$ on its main diagonal. Therefore, based on the recursive application of Equation ([\[eq:3\]](#eq:3){reference-type="ref" reference="eq:3"}), the state vector of the vehicle from time step $k+1$ to $k+N_p$ can be obtained and is expressed as follows: $$\begin{equation}
Y = \Psi \mathbf{X}(k) + \Theta U,
\label{eq:4}
\vspace{-5pt}
\end{equation}$$ where $N_p$ represents the prediction horizon, $N_c$ represents the control horizon, and $Y$, $\Psi$, $U$, and $\Theta$ are expressed as follows: $$Y =
\begin{bmatrix}
\mathbf{X}(k+1) \\
\mathbf{X}(k+2) \\
\vdots \\
\mathbf{X}(k+N_p)
\end{bmatrix}
,
\Psi = 
\begin{bmatrix}
A \\
A^2 \\
\vdots \\
A^{N_p}
\end{bmatrix}
, 
 U = 
\begin{bmatrix}
u(k) \\
u(k+1) \\
u(k+2) \\
\vdots \\
u(k+N_c-1)
\end{bmatrix}$$ $$\Theta = \begin{bmatrix} 
B & 0 & 0 & \cdots & 0 \\
AB & B & 0 & \cdots & 0 \\
A^2B & AB & B & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
A^{N_c-1}B & A^{N_c-2}B & A^{N_c-3}B & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
A^{N_p-1}B & A^{N_p-2}B & A^{N_p-3}B & \cdots & A^{N_p-N_c+1}B
\end{bmatrix}$$ To ensure that the vehicle follows the expected trajectory $Y_t$, while maintaining driving stability, the objective function is defined as: $$\begin{equation}
J = (Y - Y_t)^T Q_Q (Y - Y_t) + U^T R_R U,
\label{eq:5}
\end{equation}$$ where $Q_Q$ and $R_R$ are weight matrices. By combining Equation ([\[eq:4\]](#eq:4){reference-type="ref" reference="eq:4"}) and Equation ([\[eq:5\]](#eq:5){reference-type="ref" reference="eq:5"}), we obtain: $$\begin{equation}
J = 2\left( \frac{1}{2} U^T H U + g^T U \right) + \mathbb{C},
\label{eq:27}
\end{equation}$$ where $\mathbb{C}$ is a constant, and $H$ and $g$ are expressed as follows: $$\begin{aligned}
H &= \Theta^T Q_Q \Theta + R_R, \\
g &= \Theta^T Q_Q (\Psi \mathbf{X}(k) - Y_t).
\end{aligned}$$ To ensure the stability of the vehicle, the ranges of $U$ and $\Delta U$ must be limited, i.e., $U_{\min} < U < U_{\max}$, and $\Delta U_{\min} < \Delta U < \Delta U_{\max}$. The relationship between $U$ and $\Delta U$ is defined as follows: $$\begin{equation}
\Delta U = E_{N_c}^{-1}(U - U_{k-1}),
\label{eq:6}
\end{equation}$$ And, $E_{N_c}$, $U_{k-1}$ are expressed as follows: $$\Delta U = 
\begin{bmatrix}
\Delta u(k) \\
\Delta u(k+1) \\
\vdots \\
\Delta u(k+N_c-1)
\end{bmatrix}
, \quad
U_{k-1} = 
\begin{bmatrix}
u(k-1) \\
u(k-1) \\
\vdots \\
u(k-1)
\end{bmatrix},$$ $$E_{N_c} = 
\begin{bmatrix}
E_3 & 0 & \cdots & 0 \\
E_3 & E_3 & \cdots & 0 \\
\vdots & \vdots & \ddots & 0 \\
E_3 & E_3 & \cdots & E_3
\end{bmatrix}.$$ In summary, the path tracking problem has now been transformed into a quadratic programming problem: $$\begin{equation}
\begin{split}
\min_U J &= \frac{1}{2} U^T H U + g^T U ,\\
\text{s.t.}
&\left\{
\begin{aligned}
&U_{\min} \leq U \leq U_{\max} \\
&\Delta U_{\min} \leq \Delta U \leq \Delta U_{\max}
\end{aligned}
\right.
\end{split}
\label{eq:7}
\end{equation}$$ By optimizing the objective function $J$, the optimal value of $U$ under the constraint conditions can be obtained. Consequently, the vehicle's optimal control vector $u_{\text{best}} = [V_{x}, V_{y}, \omega]^T$ is determined. Next, the control vector will be used to calculate the rotational speed and steering angle of each wheel.

![Experimental results show the proposed MPC accurately tracks the planned trajectory while minimizing robot travel in LiDAR blind spots. ](Hu2024Swept_figs/hureulst.png){#fig:simulation width="100%"}

![Trajectory tracking error comparison.](Hu2024Swept_figs/ERROR.png){#fig:Trajectory tracking error comparison width="100%"}

![Experiment Result, Proposed solution offers minimal swept volume compared to another baseline model. ](Hu2024Swept_figs/resultcompare.png){#fig:simulation1 width="95%"}

As shown in Fig. [3](#fig:modeling){reference-type="ref" reference="fig:modeling"}, in the vehicle coordinate system, the rotational velocity $\omega$ of the vehicle can be decomposed to the X-axis and Y-axis are represented as $V_{\tau ix}$ and $V_{\tau iy}$, respectively. Therefore, the resultant velocity of the wheel $\vec{V}_i = [V_{ix}, V_{iy}]^T$ can be expressed as: $$\begin{equation}
\vec{V}_i = 
\begin{bmatrix}
V_{ix} \\
V_{iy}
\end{bmatrix}
=
\begin{bmatrix}
V_x + V_{\tau ix} \\
V_y + V_{\tau iy}
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 & Y_{wi} \\
0 & 1 & X_{wi}
\end{bmatrix}
\begin{bmatrix}
V_x \\
V_y \\
\omega
\end{bmatrix}.
\label{eq:1}
\end{equation}$$ Therefore, the final steering angles $\gamma_{i}$ and the linear speed $V_{i}$ of each wheel group are expressed as follows: $$\begin{equation}
\gamma_{i} = \arctan\left(\frac{V_{iy}}{V_{ix}}\right),
\label{eq:2}
\end{equation}$$ $$\begin{equation}
V_{i} = \sqrt{(V_{ix})^2 + (V_{iy})^2}.
\label{eq:speed}
\end{equation}$$ By combining Equations ([\[eq:1\]](#eq:1){reference-type="ref" reference="eq:1"}), ([\[eq:2\]](#eq:2){reference-type="ref" reference="eq:2"}), and ([\[eq:speed\]](#eq:speed){reference-type="ref" reference="eq:speed"}), the vehicle's point mass control vector $u_{\text{best}}$ can be transformed into the linear speed $V{i}$ and steering angle $\gamma_{i}$ for each wheel group, thereby controlling the vehicle to follow the target trajectory.

# Experiment

## System Setup

This work is designed for multi-axle swerve-drive AMRs in future logistics. However, due to hardware limitations, we rely on simulations to verify performance. As shown in Fig. [5](#fig:simulation){reference-type="ref" reference="fig:simulation"}, a street map is set up in Gazebo, where a pedestrian is standing at a crosswalk, preparing to cross the road. A 5-axle Swerve-Drive Vehicle, approximately 8.1m long and 2.7m wide, equipped with a LiDAR sensor in front, is making a left turn at the intersection. The objective is to plan a path that minimizes the $\mathbb{S}$ while keeping the Swept area away from obstacles to ensure pedestrian safety. The path is tracked using an MPC controller. All the experiments are done on a Gen 13 i7 Notebook PC with Nvidia 4060 GPU.

## Evaluation Metric

The evaluation metric for our work is listed as follows:

- **Excess Swept Area $\mathbb{S}_{\text{excess}}$:** The additional volume covered by the vehicle beyond the minimal swept area, defined as the difference between the actual and minimal swept area, as illustrated in Fig. [1](#fig:firstpage){reference-type="ref" reference="fig:firstpage"}.

- **Planning Time $t$:** Quick trajectory generation is vital for real-time applications.

- **Tracking Error $e_y$, $e_{\varphi}$:** Accurate tracking ensures safe and efficient path execution.

## Result and Discussion

::: {#tab:comparison}
  **Method**                            **$\mathbb{S}_{\text{excess}}$ ($m^2$)**   **$t$ ($s$)**   **$e_y$ ($m$)**   **$e_{\varphi}$ (°)**  
  ------------------------------------ ------------------------------------------ --------------- ----------------- ----------------------- --
  Classic[@zhao2019modelling]                            82.15                         1.50             ±1.38                ±3.6           
  SVSDF [@wang2024implicit]                              75.62                          2.5             ±0.04                ±0.04          
  Hierarchical [@xu2022hierarchical]                     48.37                         1.38             ±0.13                ±0.12          
  Proposed                                             **23.14**                     **1.17**         ±**0.04**            ±**0.03**        

  : Comparison of Metrics for Different Methods
:::

[]{#tab:comparison label="tab:comparison"} Classic [@zhao2019modelling] and Hierarchical [@xu2022hierarchical] are designed solely for tracking the trajectory generated by our proposed multi-axle AMR planner. SVSDF [@wang2024implicit] only has planning, and control is done using our proposed MPC .

**Table [1](#tab:comparison){reference-type="ref" reference="tab:comparison"}** and **Fig. [6](#fig:Trajectory tracking error comparison){reference-type="ref" reference="fig:Trajectory tracking error comparison"}** present a comparison of various methods based on selected evaluation metrics. The Classic method refers to the trajectory tracking approach proposed by [@zhao2019modelling], where we set the model to allow only the front wheels to steer, simulating a traditional truck. The Hierarchical method is based on the trajectory tracking approach from [@xu2022hierarchical]. The SVSDF method corresponds to the trajectory planning approach from [@wang2024implicit], and it is designed to use our MPC controller to track the generated trajectory. Both the Classic and Hierarchical methods are designed solely for tracking the trajectory generated by our proposed multi-axle AMR planner. For the Hierarchical and SVSDF methods, we use a Multi-Axle Swerve-Drive AMR model, where all-wheel groups are steerable.

The proposed method achieves the smallest $\mathbb{S}_{\text{excess}}$, measuring 23.14 m$^2$, which is the minimal excessive swept area by the vehicle. This is crucial for avoiding obstacles and ensuring pedestrian safety. Although the Classic and Hierarchical methods track the trajectory generated by our proposed approach, their poor tracking performance results in a significantly larger $\mathbb{S}_{\text{excess}}$ making them much less effective compared to our method. In terms of trajectory planning time, our method significantly outperforms others, with a reduced planning time of 1.17 seconds. The Classic and Hierarchical methods are designed to use the trajectory generated by our proposed approach, which results in similarly fast trajectory generation times. This improvement is critical for real-time applications where rapid responses to environmental changes are required.

For trajectory tracking performance, our approach maintains the lateral tracking error, $e_y$, within ±0.04 m and the heading angle error, $e_{\varphi}$, within ±0.03°. Compared to the Hierarchical method, our approach demonstrates substantial improvements in both precision and reliability, thereby enhancing the safety and maneuverability of the vehicle. Since the SVSDF method is designed to use our proposed tracking method, it achieves similar accuracy in tracking error performance.

We conducted a comparative analysis with different AMR models, as shown in Fig. [7](#fig:simulation1){reference-type="ref" reference="fig:simulation1"}. The proposed methods achieve minimal swept areas and accurate trajectory tracking without collisions, providing significant improvements for modern AMRs. While SVSDF reduces collision risk, its swept volume is still suboptimal. The classical truck control method performed the worst, with the largest swept area and frequent collisions, as commonly reported in industrial settings and news sources. This highlights the effectiveness of our approach in minimizing swept volume and enhancing safety.

# Conclusion

This paper presented a unified approach combining swept volume-aware path planning with MPC to optimize trajectories and independently control each wheel of multi-axle AMRs for precise maneuvering in constrained environments. By calculating wheel group steering angles from velocity vectors, we simplify the vehicle model and enhance MPC control. Simulations show reduced swept volume and improved real-time trajectory tracking using CUDA, supporting reliable and efficient autonomous heavy-duty AMR applications.

[^1]: This research is supported by the National Research Foundation, Singapore, under its Medium-Sized Center for Advanced Robotics Technology Innovation (CARTIN).

[^2]: All authors are with the School of Electrical and Electronic Engineering, Nanyang Technological University, 50 Nanyang Avenue, Singapore 639798, Email: {shyuan, elhxie}@ntu.edu.sg, tianxin001@e.ntu.edu.sg.

[^3]: $^*$ Corresponding Author, $^1$ Equal contribution.
