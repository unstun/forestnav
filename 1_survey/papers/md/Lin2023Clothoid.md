---
citation_key: Lin2023Clothoid
arxiv_id: 2308.10049
arxiv_url: "https://arxiv.org/abs/2308.10049"
title: "Clothoid Curve-based Emergency-Stopping Path Planning with Adaptive Potential Field for Autonomous Vehicles"
authors_short: "Pengfei Lin et al."
year: 2023
direction_tag: K_dubins_reeds_shepp;O_dense_forest_narrow_passage
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:32:39Z
origin: ai+web
reviewed: false
---

# Clothoid Curve-based Emergency-Stopping Path Planning with Adaptive Potential Field for Autonomous Vehicles

Pengfei Lin, Ehsan Javanmardi, and Manabu Tsukada

Abstract—The Potential Field (PF)-based path planning method is widely adopted for autonomous vehicles (AVs) due to its real-time efficiency and simplicity. PF often creates a rigid road boundary, and while this ensures that the ego vehicle consistently operates within the confines of the road, it also brings a lurking peril in emergency scenarios. If nearby vehicles suddenly switch lanes, the AV has to veer off and brake to evade a collision, leading to the ”blind alley” effect. In such a situation, the vehicle can become trapped or confused by the conflicting forces from the obstacle vehicle PF and road boundary PF, often resulting in indecision or erratic behavior, even crashes. To address the above-mentioned challenges, this research introduces an Emergency-Stopping Path Planning (ESPP) that incorporates an adaptive PF (APF) and a clothoid curve for urgent evasion. First, we design an emergency triggering estimation to detect the ”blind alley” problem by analyzing the PF distribution. Second, we regionalize the driving scene to search the optimal breach point on the road PF and the final stopping point for the vehicle by considering the possible motion range of the obstacle. Finally, we use the optimized clothoid curve to fit these calculated points under vehicle dynamics constraints to generate a smooth emergency avoidance path. The proposed ESPP-based APF method was evaluated by conducting the co-simulation between MATLAB/Simulink and CarSim Simulator in a freeway scene. The simulation results reveal that the proposed method shows increased performance in emergency collision avoidance and renders the vehicle safer, in which the duration of wheel slip is 61.9% shorter, and the maximum steering angle amplitude is 76.9% lower than other potential field-based methods.

Index Terms—Autonomous vehicles, collision avoidance, path planning, potential field, clothoid curve

## I. INTRODUCTION

PPROXIMATELY 1.3 million people lose their lives every year due to traffic crashes, and there are 20 to 50 million people suffer non-fatal injuries, with many suffering the perpetual disability andor mental handicap [1], [2]. Therefore, a novel generation of intelligent transportation systems (ITS) with autonomous vehicles (AVs) as the core component is proposed and developed worldwide to reduce casualties in the next decade. Soon after, the manufacturers started to conduct road tests for the AVs to fast commercialization. However, the immature AVs have unfortunately caused a series of traffic tragedies. According to the autonomous vehicle collision reports from the Department of Motor Vehicles (DMV), California [3], there have been approximately 546 traffic collision events related to AVs until January 2023.

Path planning, as a crucial module of autonomous driving systems, is responsible for generating a collision-free trajectory. Typically, path planning is divided into two main categories: global path planning (also known as route planning) and local path planning. Global path planning assumes knowing the environment in advance, such as an available map. And then, graph search-based methods are usually used to obtain the globally shortest path with the given current position and destination [4], [5]. Local path planning refers to real-time generating trajectories in the surrounding environment known locally and can be reconstructed based on the sensors. Function-optimized methods and parametric curves are frequently applied in local path planning due to the requirement of high real-time performance [6].

Potential field (PF), one of the most popular path planning methods, is the function-optimized approach with a welldefined mathematical formulation, a high real-time performance, and a simple structure. The PF was first applied to tackle the path-planning tasks of mobile robots [7]. It is originally inspired by classical mechanics, formulating virtual forces from the obstacles and the target point [8]. This method assigns an attractive force to the goal position for driving the robot toward its goal while establishing a repulsive force on obstacle vehicles to prevent a collision. Due to the complex traffic conditions, real-time performance and driving safety are two cardinal indicators to evaluate the level of AVs [9]. Therefore, the PF satisfies the aforementioned requirements and has become one of the mainstream in the current planning algorithms. [5].

Collision avoidance is the primary task of path planning. Compared to mobile robots, the difficulty of collision avoidance for AVs requires higher standardization, as the nonholonomic constraints of an urban vehicle are more complicated than those of an indoor mobile robot [10]. In particular, AVs should handle more significant emergency obstacle avoidance, including unexpected events on the freeway, such as sudden lane-changed obstacles without a pre-warning. Therefore, to address the “blind alley” problem where the AVs can be trapped or indecisive leading to crashes, we propose a unique Emergency-Stopping Path Planning (ESPP) method with the clothoid curve and the adaptive potential field (APF) to enable AVs to achieve safe emergency collision avoidance and stop manoeuvers. The contributions of this study are briefly summarized as follows:

• We introduced a clothoid curve to design the ESPP; the clothoidal coefficients are obtained by solving a constrained quadratic programming (QP) problem.

• We propose to open a breach on the road PF based on the local reference waypoints, which can navigate the vehicle for a safe stopping maneuver on the roadside.

• We computed the terminal side of the ESPP by consid ering the road structure and the predicted motion range of the obstacle.

![](Lin2023Clothoid_figs/c36537b4462901daf3fa4eee802c4597feb3742c89fb302adf13b86ceef99160.jpg)  
Fig. 1. Overall autonomous driving system framework with the embedded ESPP method: Sensing data gathers the information collected by sensors; Plannin layer monitors the emergency and triggers the ESPP computation if the emergency is sensed; Control system outputs the direct signals to Vehicle Actuators for longitudinal and lateral maneuvers

The proposed ESPP method is embedded mainly in the planning module, including the APF, emergency triggering, and ESPP computation, as shown in Fig. 1 (red dotted frames). The complete autonomous driving system framework includes the Sensing, Planning, Control, and Vehicle Actuation. In addition, we list the following assumptions in this study.

• We assume that this work mainly concentrates on straight roads.

• We assume that the collision can not be avoided within the road and an emergency stopping lane or open space is needed.

• We assume that the ego vehicle performs a total (maximum) braking maneuver when an emergency occurs.

The rest arrangement of this article is as follows: Section II discusses the related work in the past few years. And then, the adaptive potential field is introduced in Section III. Next, Section IV studies the clothoid curve-based ESPP method. Section V describes the model predictive controller for the path-tracking task. Then, Section VI illustrates the numerical analysis for validation. Finally, the conclusion and discussion are made in Section VII.

## II. RELATED WORK

Ji et al. [11] combined the PF with a specific multiconstrained MPC to tackle path planning and tracking tasks for AVs. However, the generated path did not always conform to vehicle dynamics. Moreover, they only studied a single forward obstacle with constant speed or acceleration, no emergencies were considered. Rasekhipour et al. [12] used the signed distance (SD) to calculate the minimum distance between the ego vehicle and obstacles that were applied in the potential functions; the scenarios were focused on vehicle merging problems, and the local minima were not considered, which was unable to deal with urgent events. Li et al. and Wang et al. [13], [14] designed a novel driving safety field that contains a PF, a kinetic field, and a behavior field to consider the static and moving objects and pedestrians, as well as the individual characteristics of human drivers. However, the safety driving field model was used as a threat-assessment strategy, which had a finite discussion on the path generation, including the path quality, determination of the model parameters, etc.

Wang et al. [15], [16] proposed to include the crash severity and artificial PF into the objective function of an MPC to achieve conventional collision avoidance with the lowest crash mitigation. However, the case studies assumed that collisions were unavoidable. Similarly, Lin et al. [17], [18] studied the integration of the PF with a clothoid curve for collision avoidance in a waypoint tracking scenario; however, they assumed that the obstacles were driven only in a straight lane without lane-changing behavior, lacking emergency analysis. Lu et al. [19] proposed an improved APF to adapt both the acceleration/deceleration and the mass of the obstacle to a potential function by using two Gaussian-like functions on both curve and straight roads. However, the local minima were ignored by assuming that the obstacles’ motions were preknown and did not discuss emergency scenarios.

Recently, Wang et al. [20] proposed a PF-based path planning that is adjusted to a kinematic vehicle model for curvy roads, but the simulation was evaluated under the assumption of constant speed, and the obstacles are either stationary or traveling in a straight line at a constant low speed. To solve the zigzag path caused by traditional PF, Li et al. [21] proposed an optimization-based path planning that used a dynamic enhanced firework algorithm (dynEFWA)- APF. However, the road PF was set to be inviolable, and the speed was also assumed constant. Lin et al. [22], [23] presented a unique safe tunnel-based model predictive pathplanning controller (STMPC) with the APF to solve the local minima problem that appeared on the highway; however, the longitudinal speed is assumed to be constant, and the road PF cannot be adjusted. To tackle the overtaking problem, Xie et al. [24] presented a distributed motion planning framework via artificial PF to introduce the notion of velocity difference PF and acceleration difference PF for vehicle platoons. However, the road PF remained unchangeable, and local minima weren’t taken into account. Similarly, Wu et al. [25] proposed a human-like motion planning algorithm for expressway lanechanging behavior that used the artificial PF to analyze the coupling relationship, but the study did not discuss the local minima and assumed the PF is always working. Ji et al. [26] proposed a three-dimensional PF (TriPField) that combines the ellipsoid PF with a Gaussian velocity field (GVF) to conquer local minima by considering the road user’s geometric shape. However, road PF was not discussed because it assumes collision avoidance can be completed within the road. To improve the tracking accuracy, Chu et al. [27] used the artificial PF to compute the reference trajectory and combined the MPC with PID feedback for the tracking task. Still, this study established an unalterable road PF and focused more on tracking performance. Shang et al. [28] presented a novel artificial PF that has the flexibility to fit different shapes of road structures. Particularly the proposed PF was implemented in an MPC controller with collision mitigation. However, a tremendous potential value was allocated to the road edges, which means the road edge is also unbreakable. To further improve the motion planning and tracking performance, Du et al. [29] developed global heuristic planning-based artificial PF to generate the optimal sequence for the reinforcement learning-based predictive control, achieving the real-time application, but it concentrated on the unstructured roads where the road PF was not utilized.

Overall, most of the aforementioned related work used the road PF and assigned a large potential value, making it unbreakable. Those studies generally assume that collision avoidance can be accomplished within the confine of the road, ignoring the “blind alley” problem. However, it might be necessary for a vehicle to maneuver in a way that makes it partially or entirely off the road to ensure safety in some cases, such as impending collision for a greater safety margin, avoiding secondary collisions, and unexpected intention of obstacles. Therefore, we focus on studying emergency collision avoidance that requires driving off the road to complete safe maneuvers.

## III. ADAPTIVE POTENTIAL FIELD

In this section, we present the concept of the adaptive potential field, a paradigm that encompasses the road PF, obstacle PF, and target PF, collectively revolutionizing collision avoidance strategies for a safer driving experience.

## A. Road Potential Field

The road PF usually prevents the vehicle from driving out of the road, and the vehicle can stay in the middle of the lane, ensuring safety. Therefore, we must establish the repulsive potential of the road edges and lane divider to enhance vehicle guidance and prevent unintended deviations. We use the following functions to represent the lane divider PF, $U _ { l a n e }$ , and road edge PF, $U _ { e d g e }$ , [30]:

$$
U _ {l a n e} = \sum_ {i = 1} ^ {N _ {l a n e}} A _ {l a n e} \exp \left(- \frac {(Y - Y _ {c , i}) ^ {2}}{2 \zeta^ {2}}\right),\tag{1}
$$

$$
U _ {e d g e} = \frac {1}{2} \eta \left(\frac {1}{Y - Y _ {l , u}}\right) ^ {2},\tag{2}
$$

where $N _ { l a n e }$ determines the number of lanes, $A _ { l a n e }$ denotes the maximum amplitude of the lane divider PF, Y is the lateral position of the ego vehicle, $Y _ { c , i }$ is the lateral position of the $i ^ { t h }$ lane divider, ζ represents the slope of lane PF that is directly proportional to the lane width and determines the rate at which the potential rises or falls., η is a scale factor that determines the steepness of the road PF, and $Y _ { l , u }$ denotes the lateral position of the lower and upper boundaries of the road. It should note that the value of $A _ { l a n e }$ is small when lane-change behavior is encouraged.

## B. Obstacle Potential Field

The obstacle PF is responsible for maintaining the ego vehicle at a safe distance from the obstacle. Therefore, the ego vehicle can be guided to perform lane-changing and/or braking maneuvers, based on the variation of the obstacle PF. The foundation of the obstacle PF, $U _ { o b s } ,$ is the probability density function (PDF) of the Gaussian distribution [19]:

$$
U _ {o b s} = \frac {A _ {o b s}}{2 \pi \sqrt {| \Sigma |}} e ^ {\left(- \frac {1}{2} (\ell - \mu) ^ {T} \Sigma^ {- 1} (\ell - \mu)\right)},\tag{3}
$$

where $A _ { o b s }$ is the maximum amplitude of the obstacle PF, ${ \ell } = ( s , d ) ^ { T }$ is the position of the ego vehicle in the Frenet frame [31] that s and d are the tangential and normal directions in the Frenet coordinate, and $\Sigma$ and $\mu$ are the covariance matrix and mean of the PDF, respectively. Therefore, we use Eq. (3) to adapt the motion of the obstacle along with the longitudinal and lateral directions $U _ { A o b s }$ as follows:

$$
U _ {A o b s} = \sum_ {j = 1} ^ {N _ {o b s}} w _ {1} U _ {o b s, j} ^ {1} + w _ {2} U _ {o b s, j} ^ {2},\tag{4}
$$

where

$$
\begin{array}{l l} w _ {1} \in [ 0. 5, 1 ], & w _ {2} = 1 - w _ {1}, \\ \mu_ {1} = (s _ {1}, d _ {1}) ^ {T}, & \Sigma_ {1} = \left[ \begin{array}{c c} \sigma_ {s _ {1}} ^ {2} & 0 \\ 0 & \sigma_ {d _ {1}} ^ {2} \end{array} \right], \\ \mu_ {2} = (s _ {2}, d _ {2}) ^ {T}, & \Sigma_ {2} = \left[ \begin{array}{c c} \sigma_ {s _ {2}} ^ {2} & 0 \\ 0 & \sigma_ {d _ {2}} ^ {2} \end{array} \right], \end{array}
$$

where $N _ { o b s }$ denotes the number of obstacle vehicles, $w _ { 1 , 2 }$ is the weight factor, $\mu _ { 1 }$ and $\mu _ { 2 }$ denote the mean of the corresponding PDF that is related to obtaining the safe distance from the position of the obstacle in the Frenet frame, $\Sigma _ { 1 }$ and $\Sigma _ { 2 }$ represent the covariance matrix of the corresponding PDF, and $\sigma _ { s , d }$ denotes the variance terms of the corresponding covariance matrix, which is combined with the longitudinal and lateral accelerations of the obstacle. The obstacle PF is shown in Fig. 2.

## C. Target Potential field

The target PF constantly produces an attractive force to drive the ego vehicle forward or towards the target lane or position. Therefore, we simply used the following function to design the target PF, $U _ { t a r } \mathbf { : }$

$$
U _ {t a r} = \frac {| X - X _ {r} | + | Y - Y _ {r} |}{1 0 0}\tag{5}
$$

where $( X _ { r } , Y _ { r } )$ denotes the position of the target location and $X$ is the longitudinal position of the ego vehicle. It should be noted that Eq. (5) is used in conventional driving scenarios where the emergency has not been sensed while driving toward the target position. Thus, we can calculate the total PF by summing Eq. (1)–(5):

![](Lin2023Clothoid_figs/3bc90f3f6250547d59981f81997c09882bde54058daaf916d19983cd51ec8178.jpg)  
Fig. 2. Emergency merging behavior of the adjacent vehicle (black) owing to the unexpected animal (brown): From the oblique view, the obstacle PF intersects with lower road PF, leading to a blind alley (local minima)

![](Lin2023Clothoid_figs/384d8e5f863bbb3f9564759a462a7a4064db44272418cff2a076f083a683f676.jpg)  
Fig. 3. Explanation of the emergency triggering estimation: With $\psi _ { r e f }$ given by APF, making an extension line from the current position of ego-vehicle (green) to intersect with the lower road boundary $P _ { i n t } ; D _ { E 2 R }$ is the distance between green vehicle and $P _ { i n t }$

$$
U _ {t o l} = U _ {l a n e} + U _ {e d g e} + U _ {A o b s} + U _ {t a r},\tag{6}
$$

We then applied the gradient descent method to obtain the desired path information:

$$
F _ {t o l} = - \nabla U _ {t o l} = - \left[ \frac {\partial U _ {t o l}}{\partial X} \quad \frac {\partial U _ {t o l}}{\partial Y} \right] ^ {T},\tag{7}
$$

$$
\psi_ {r e f} = t a n ^ {- 1} \frac {F _ {t o l} (Y)}{F _ {t o l} (X)}.\tag{8}
$$

where $\psi _ { r e f }$ is the desired yaw angle. The overall APF is illustrated in Fig. 2, including the road structure and the obstacle.

## IV. CLOTHOID CURVE-BASED EMERGENCY-STOPPING PATH PLANNING

In this section, we present the detailed design process of the proposed ESPP-based on the clothoid curve.

## A. Blind Alley Problem

Although the APF from Sec. III can model the collision risk with high accuracy by considering the longitudinal and lateral accelerations of the obstacle, it ignores the local minima problem with the assumption that the motion of the obstacle PF is known. However, traffic emergencies mostly occur because of the unpredictable motions of the surrounding obstacles, such as sudden deceleration and reckless lane changes [32]. As shown in 2, the sudden lane-changing obstacle with a full braking maneuver will lead to a rapidly expanding obstacle PF, which intersects with the road PF. Subsequently, the “blind alley” phenomenon occurs because there are no feasible paths for the ego vehicle to track. This is a case of local minima. As described by Koren and Borenstein [33], the local minima problem causes a trap situation for a mobile robot. However, considering the dynamic characteristics of the ego vehicle, it is difficult to stop at the local minima region owing to the large inertia. Instead, the ego vehicle could have driven into either the obstacle PF or road PF and received an excessive repulsive force [22], which can cause severe yawing and even vehicle crashes. A simple way is to directly remove the road PF (the side to which the vehicle is heading) so that the ego vehicle can drive out of the road to obtain sufficient space for emergency braking and obstacle avoidance. However, the ego vehicle is prone to wheel slipping during emergency obstacle avoidance after removing the road PF due to the instantaneous disappearance of the road repulsive force. There has an imbalance in the virtual forces, leading to oversized repulsion from the obstacle PF experienced by the vehicle. In severe cases, they could lose control of the vehicle body. Although removing the road PF can eliminate the “blind alley” problem, it will lead to an imbalance of virtual forces because the repulsive force of the road PF disappears instantly, and the excessive repulsive force of the obstacle PF causes slipping, as shown in Fig. 12. Therefore, we proposed a triggering estimation to detect the “blind alley” problem and then generate an emergency-stopping path based on the clothoid curve for completing a safe stop.

## B. Emergency Triggering Estimation

In this study, we propose an emergency triggering estimation to detect the blind alley problem that is described above. As described in Section III, the APF can obtain $\psi _ { r e f }$ at each time step, which we can use to estimate the emergency. Firstly, we use $\psi _ { r e f }$ to generate the local reference waypoints $( X _ { r e f } , \ Y _ { r e f } )$ for the controller to track, which is computed

![](Lin2023Clothoid_figs/bde749a4d4e5a5dc1811315d28950d1ea80a83e6f095ac6055240140a9d360e0.jpg)  
Fig. 4. System flow chart of the proposed emergency triggering estimation

with a given step length L:

$$
\left\{ \begin{array}{l} X _ {r e f} = X + L \cos \psi_ {r e f} \\ Y _ {r e f} = X + L \sin \psi_ {r e f} \end{array} \right.\tag{9}
$$

Note that Eq. (9) is iterated in a control loop according to the number of required waypoints, and L is usually dependent on the current speed and sampling time, for example, $L = V T _ { s }$ where V is the longitudinal speed of the ego vehicle and $T _ { s }$ is the sampling time. Then, as depicted in Fig. 3, the green star-shape waypoints are produced by APF, which we can monitor the last waypoint $\bar { ( X } _ { r e f } ^ { l a s t } , \ Y _ { r e f } ^ { l \bar { a } s t } )$ , whether it reaches or cross the road edge at each time step. If yes, we can make an extension line along the $\psi _ { r e f }$ (if $\psi _ { r e f } \neq 0 )$ angle from the current position of the ego-vehicle, as stated in Fig. 3. And the extension line will have an intersect point (denoted as $P _ { i n t } )$ with the lower road boundary. Second, we can measure the distance $D _ { E 2 R }$ from the current position of the ego-vehicle to the intersect point. We mark the minimum braking distance of the ego-vehicle from the current position as $D _ { b r a k e }$ . It should note that $D _ { b r a k e }$ depends on multiple factors, including the reaction time, braking deceleration, road conditions, etc. D. Lyubenov [34] has summarized the empirical formula to compute the minimum braking distance in accident investigation the cases for emergency braking behavior. If $D _ { E 2 R }$ is greater than or equal to $D _ { b r a k e }$ , the ego vehicle can promptly stop before reaching the road PF. In this case, the ESPP computation will not be triggered, and the ego vehicle can regain its orientation to follow the obstacle vehicle if the obstacle vehicle returns to regular driving after an emergency lane change. Otherwise, the ESPP computation will be triggered to navigate the egovehicle to a safe stop. In general, the overall process of the emergency triggering estimation is summarized in Fig. 4.

## C. Clothoid Curve

To tackle the ”blind alley” situation, we propose an ESPP method based on the clothoid curve that is also known as cubic (3rd order) polynomial. The clothoid curve is usually used in waypoint tracking and highway road design to generate an easy-to-follow path with linear curvature [35], [36]. The typical representation of the clothoid curve is denoted as [37]:

$$
f _ {c} (r) = c _ {0} + c _ {1} r + c _ {2} r ^ {2} + c _ {3} r ^ {3},\tag{10}
$$

where

$$
\kappa = 6 c _ {3} s + 2 c _ {2},
$$

where r denotes the arc length, $c _ { 0 }$ denotes the lateral offset from the lane center at $r = 0 , c _ { 1 }$ denotes the heading angle error at $r = 0$ , κ denotes the curvature of the clothoid curve, $2 c _ { 2 }$ denotes the road curvature at $r = 0$ , and $3 c _ { 3 }$ denotes the curvature rate. To estimate the clothoidal coefficients, at least 4 waypoints are required for curve fitting, as illustrated below:

$$
\left[ \begin{array}{c c c c} 1 & x _ {1} & x _ {1} ^ {2} & x _ {1} ^ {3} \\ 1 & x _ {2} & x _ {2} ^ {2} & x _ {2} ^ {3} \\ \vdots & \vdots & \vdots \\ 1 & x _ {N} & x _ {N} ^ {2} & x _ {N} ^ {3} \end{array} \right] \left[ \begin{array}{c} c _ {0} \\ c _ {1} \\ c _ {2} \\ c _ {3} \end{array} \right] = \left[ \begin{array}{c} f (x _ {1}) \\ f (x _ {2}) \\ \vdots \\ f (x _ {N}) \end{array} \right] \approx \left[ \begin{array}{c} y _ {1} \\ y _ {2} \\ \vdots \\ y _ {N} \end{array} \right].\tag{11}
$$

For $N \geq 4$ waypoints, we calculate the coefficients, ${ \bf C } = { \bf \partial }$ $\left[ c _ { 0 } \mathrm { ~ \textit ~ { ~ c ~ } ~ } c _ { 2 } \mathrm { ~ \textit ~ { ~ c ~ } ~ } _ { 3 } \right] ^ { T } . \mathrm { ~ \textit ~ { ~ ( ~ x ~ } _ { N } , y _ { N } ) }$ is defined with reference to the vehicle coordinates xyz, whereas the waypoints from the APF and GPS sensors are defined with reference to the local projected coordinates $X Y Z$ . Therefore, the coordinate transformation is required to present the waypoints in the vehicle coordinates for curve fitting, given by:

$$
\left[ \begin{array}{c} x _ {i} \\ y _ {i} \\ 1 \end{array} \right] = \overbrace {\left[ \begin{array}{c c c} \cos \phi & - \sin \phi & 0 \\ \sin \phi & \cos \phi & 0 \\ 0 & 0 & 1 \end{array} \right]} ^ {\operatorname{Rot} (z, \phi)} \overbrace {\left[ \begin{array}{c c c} 1 & 0 & d _ {x} \\ 0 & 1 & d _ {y} \\ 0 & 0 & 1 \end{array} \right]} ^ {\operatorname{Trans} (d _ {x}, d _ {y})} \left[ \begin{array}{c} X _ {i} \\ Y _ {i} \\ 1 \end{array} \right],\tag{12}
$$

for $i = 1 , 2 , \dots , N$ , where

$$
\phi = - \psi , d _ {x} = - X, d _ {y} = - Y.
$$

with $\psi$ is the heading angle of the ego vehicle. Typically, the clothoid curve is used to fit waypoints from the leading vehicle in a car-following scenario. However, in this study, we used a clothoid curve to fit a set of specific waypoints to create the ESPP.

## D. Emergency-Stopping Path Planning

As depicted in Fig. 5, when the adjacent vehicle suddenly merges without a pre-warning, the waypoints produced by the APF from the ego vehicle will lead to the lower road borderline. In this situation, the ego vehicle hits the PF of the lower road boundary, even with complete braking. An excessive repulsive force is imposed on the ego vehicle because the road PF restricts the vehicles from driving out of the road, leading to a severe heading oscillation of the ego vehicle. Herein, opening a breach from the road PF is necessary to navigate the ego vehicle to stop at a non-conflicting position. From the waypoints (green stars) generated by the APF, we can estimate the heading angle of the ego vehicle when it drives toward the road boundary. The estimated heading angle is then used to find the waypoint (red star) intersecting the road boundary as the breach spot. Subsequently, the most crucial step is to determine the stop point (purple star). Thus far, the selection of the stop point should consider the following constraints:

![](Lin2023Clothoid_figs/34c0865bf265f6e685d9c5fcc065dbb95693b1b9cac29a3e7e8a4262c262690b.jpg)  
Fig. 5. Emergency-Stopping Path Planning on the expressway: Regionalization within the brown dashed box $( S _ { 1 } , \ S _ { 2 } , \ S _ { 3 }$ , S<sub>4</sub>); three star-shape points are then obtained (red, blue, purple); interpolation points (circle) are used for computing the clothoid curve (light blue).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Selecting Stop Point of the ESPP
1: Initialization: $P_{bp}, P_{sp}, D_{manha} \leftarrow 0$
2: Compute $P_{sp} \leftarrow \{x_{sp}, y_{sp}\}$
3: Compute $S_2$ based on Eq. (13)
4: for $x_{sp,cand} \in [x_{bp}, x_{bp} + D_{brake}]$ do
5:    for $y_{sp,cand} \in [Y_l, Y_{esl} - l_w/2]$ do
6:    if $\psi_o \leq 0$ then
7:    Obtain $P_{dp}^i \leftarrow \{x_{dp}^i, y_{dp}^i\}$
8:    Optimize $D_{manha}$ Eq. (14) for $P_{sp}^*$
9:    else
10:    Optimize $D_{manha}$ Eq. (14), without Eq. (13a) and (13b) for $P_{sp}^*$,
11:    end if
12:    end for
13: end for
Output: selected stop point $P_{sp}^*$
</div>

• The stop point should not be within the predicted motion range of the obstacle.

• The stop point should not be in the restricted region (denoted as the blue double-dotted line).

• The total length of the ESPP should consider the distance and time from braking to a safe stop.

Based on these requirements, we can regionalize the selected area (denoted by the brown dashed frame in Fig. 5) by twodimensional geometry. The predicted motion range of the obstacle vehicle is denoted by $S _ { 2 }$ as follows:

$$
S _ {2} = \frac {1}{2} \alpha R ^ {2},\tag{13}
$$

where

$$
\alpha = 2 \Delta \psi_ {o, m a x}, R = N _ {p} V _ {o b s} T _ {s},
$$

where α is the central angle and R is the motion radius of the obstacle vehicle. $\Delta { \psi } _ { o , m a x }$ denotes the maximum heading angle of the obstacle vehicle and $V _ { o b s }$ is the velocity of the obstacle vehicle. $N _ { p }$ denotes the prediction horizon (consistent with the MPC controller), and $T _ { s }$ denotes the sampling time. In this study, we use approximate estimation to predict the motion range of the obstacle vehicle. At each time step, the ego vehicle measures $\Delta { \psi } _ { o , m a x }$ and $V _ { o b s }$ that we can roughly estimate the possible motion range considering the maximum mechanical steering limitation. Then, we can then calculate the coordinates of the three dividing points (denoted as $P _ { d p } ^ { 1 } , P _ { d p } ^ { 2 } ,$ and $P _ { d p } ^ { 3 }$ , from top to bottom) using the geometric solution. Therefore, we should assign the stop point (denoted as $P _ { s p } )$ outside $S _ { 2 }$ and $S _ { 3 }$ , because the collision risk is higher than $S _ { 1 }$ and $S _ { 4 }$ . Moreover, if $P _ { s p }$ is located in $S _ { 3 }$ , it leads to a tortuous curve. Therefore, we hope that $P _ { s p }$ can be selected from $S _ { 1 }$ , which is the safest area. Nevertheless, if the length of the ESPP is less than the minimum braking distance of the ego vehicle, $S _ { 4 }$ should be considered for $P _ { s p } .$ . Finally, we can arrange it into an optimization problem with the following constraints:

$$
\max _ {x _ {s p}, y _ {s p}} | x _ {s p} - x _ {b p} | + | y _ {s p} - y _ {b p} |\tag{14}
$$

$$
\mathrm{s.t.} - \psi_ {E S P P} <   \arctan (\frac {y _ {s p} - y _ {b p}}{x _ {s p} - x _ {b p}}) <   0,\tag{14a}
$$

$$
\left\{ \begin{array}{l l} P _ {s p} = \{x _ {s p}, y _ {s p} \} \in S _ {1}, & i f \quad L _ {E S P P} \geq D _ {b r a k e}, \\ P _ {s p} = \{x _ {s p}, y _ {s p} \} \in S _ {4}, & i f \quad L _ {E S P P} <   D _ {b r a k e}, \end{array} \right.\tag{14b}
$$

where ψ<sub>ESP</sub> <sub>P</sub> denotes the heading angle of the ESPP, L<sub>ESP</sub> <sub>P</sub> denotes the length of the ESPP, and $D _ { b r a k e }$ denotes the minimum braking distance. The objective of Eq. (14) is to maximize the Manhattan distance between $P _ { s p }$ and the breach point, $P _ { b p }$ , because we need to stop as far as possible, considering that the car needs a sufficient distance to brake and also needs to be as far away from dangerous areas as possible. Therefore, we have specified the safe zone $( S _ { 1 }$ and $S _ { 4 } )$ in the constraints (14a) and (14b) with regionalization. By solving the above constrained objective function, we can get the optimal point for $P _ { s p } .$ . The detailed procedure for selecting $P _ { s p }$ is presented in Algorithm 1. $Y _ { e s l }$ refers to the lower boundary of the emergency stopping lane, and $l _ { w }$ is the vehicle’s width. Provided that if we determine $P _ { b p }$ and $P _ { s p } .$ we can compute an intersection point, $P _ { i p }$ , using two line segments extending from points $P _ { b p }$ and $P _ { s p } .$ . The tilt angle of the line segment extending from $P _ { b p }$ is equal to the heading angle of the ego vehicle. By doing this, we can ensure that the ego vehicle will not have serious fluctuations in heading when entering the ESPP. Moreover, the line segment from $P _ { s p }$ should be parallel to the road direction, which conforms to traffic rules when using the emergency stopping lane (ESL). Therefore, we can interpolate certain waypoints (red and purple dots) between the two line segments for curve fitting. We subsequently reformulate Eq. (11) through the waypoints belonging to three categories: APF, the first line segment (red dotted line), and the second line segment (purple dotted line).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Curve Fitting with Hybrid Waypoints
1: Initialization: $P_{ip}, P_{new} \leftarrow 0$ and $N_{b2i}, N_{i2s}, p_{num}$
2: Compute $P_{ip} \leftarrow \text{Intersect}(P_{bp}, P_{sp})$
3: Interpolate $N_{b2i}$ Waypoints between $P_{bp}$ and $P_{ip}$
4: Interpolate $N_{i2s}$ Waypoints between $P_{ip}$ and $P_{sp}$
5: Conduct Curve Fitting based on Eq. (14) and (15), respectively.
6: Obtain c* based on Eq. (16) and (17)
7: while $p_{num}$ do
8: Compute $U_{ESPP}$ based on Eq. (18), (19), and (20):
9: Obtain $P_{new}$ by Gradient Descent
10: $p_{num} \leftarrow p_{num} - 1$
11: end while
Output: new waypoints $P_{new}$
</div>

$$
\underbrace {\left[ \begin{array}{c c c c} 1 & x _ {1 , a p f} & x _ {1 , a p f} ^ {2} & x _ {1 , a p f} ^ {3} \\ 1 & x _ {2 , a p f} & x _ {2 , a p f} ^ {2} & x _ {2 , a p f} ^ {3} \\ \vdots & \vdots & \vdots & \vdots \\ 1 & x _ {M - 1 , b p} & x _ {M - 1 , b p} ^ {2} & x _ {M - 1 , b p} ^ {3} \\ 1 & x _ {M , b p} & x _ {M , b p} ^ {2} & x _ {M , b p} ^ {3} \\ \vdots & \vdots & \vdots & \vdots \\ 1 & x _ {N - 2 , i p} & x _ {N - 2 , i p} ^ {2} & x _ {N - 2 , i p} ^ {3} \\ 1 & x _ {N - 1 , i p} & x _ {N - 1 , i p} ^ {2} & x _ {N - 1 , i p} ^ {3} \\ 1 & x _ {s p} & x _ {s p} ^ {2} & x _ {s p} ^ {3} \end{array} \right]} _ {\mathbf {X}} \underbrace {\left[ \begin{array}{c} c _ {0} \\ c _ {1} \\ c _ {2} \\ c _ {3} \end{array} \right]} _ {\mathbf {C} _ {v}} = \underbrace {\left[ \begin{array}{c} f (x _ {1 , a p f}) \\ f (x _ {2 , a p f}) \\ \vdots \\ f (x _ {M - 1 , s p}) \\ f (x _ {M , s p}) \\ \vdots \\ f (x _ {N - 2 , i p}) \\ f (x _ {N - 1 , i p}) \\ f (x _ {s p}) \end{array} \right]} _ {\mathbf {F}}\tag{15}
$$

where $P _ { a p f } = ( x _ { a p f } , \ f ( x _ { a p f } ) )$ is the position pair of the waypoints from the APF, $P _ { b p } = ( x _ { b p } , ~ f ( x _ { b p } ) )$ denotes the position pair of the breach points, $P _ { i p } ~ = ~ ( x _ { i p } , ~ f ( x _ { i p } ) )$ represents the position pair of the intersection points, and $P _ { s p } = ( x _ { s p } , ~ f ( x _ { s p } ) )$ is the position pair of the stop point. Subsequently, we can obtain the clothoidal coefficients through the method of least-squares. Considering that the least square method cannot make the curve pass through all the selected waypoints accurately, it might lead to low accuracy at the end of the curve. Therefore, we introduce a weight matrix W into Eq. (15), as follows:

$$
W \mathbf {X} \mathbf {C} _ {v} = W \mathbf {F},\tag{16}
$$

where

$$
W = d i a g (w _ {1}, w _ {2}, \ldots , w _ {N}) _ {N \times N}.
$$

Thus, the fitting accuracy at the end of the curve can be improved by adjusting the weight matrix to stop the ego vehicle at the desired location. Subsequently, the clothoidal coefficients are obtained as follows:

$$
\mathbf {C} _ {v} = ((W \mathbf {X}) ^ {T} W \mathbf {X}) ^ {- 1} (W \mathbf {X}) ^ {T} W \mathbf {F}.\tag{17}
$$

Eq. (17) still does not consider vehicle dynamics; thus, it cannot ensure that the path is always trackable for the ego vehicle, particularly with different dynamic characteristics [38]. To overcome this, we reformulate Eq. (17) to a standard QP form with the following constraints:

$$
\mathbf {c} ^ {*} = \arg \min _ {\mathbf {c} \in C} \frac {1}{2} \mathbf {c} ^ {T} \mathbf {H} \mathbf {c} + \mathbf {f} ^ {T} \mathbf {c}\tag{18}
$$

$$
\mathrm{s.t.} \quad \mathbf {c} _ {m i n} \preceq \mathbf {c} \preceq \mathbf {c} _ {m a x},\tag{18a}
$$

where

$$
\begin{array}{r l} & H = \mathbf {X} ^ {T} W \mathbf {X}, f = - \mathbf {X} ^ {T} W \mathbf {F}, \\ & \mathbf {c} _ {m i n} = \left[ \begin{array}{l l l l} e _ {y} ^ {m i n} & e _ {\psi} ^ {m i n} & - \frac {\omega_ {m a x} ^ {2}}{2 v g} & - \frac {\dot {\kappa} _ {m a x}}{6} \end{array} \right] ^ {T}, \\ & \mathbf {c} _ {m a x} = \left[ \begin{array}{l l l l} e _ {y} ^ {m a x} & e _ {\psi} ^ {m a x} & \frac {\omega_ {m a x} ^ {2}}{2 v g} & \frac {\dot {\kappa} _ {m a x}}{6} \end{array} \right] ^ {T}, \kappa_ {m a x} = 1 / R _ {m i n}, \end{array}
$$

where $e _ { y } ^ { m i n , m a x }$ denotes the minimum and maximum lateral position errors, and $e _ { \psi } ^ { m i n , m a x }$ represent the minimum and maximum yaw angle errors, respectively; $\omega _ { m a x }$ is the maximum angular velocity of the ego vehicle, υ is the friction coefficient, g is the gravitational acceleration, $\kappa _ { m a x }$ denotes the maximum curvature, and $\dot { \kappa } _ { m a x }$ determines the maximum curvature rate to empirically indicate that the ego vehicle can only steer the wheel within a limited range under its current speed [39], $R _ { m i n }$ is the minimum turning radius that is determined by the vehicle model. The objective of Eq. (18) is to compute the optimal clothoidal coefficients under specific constraints. It should be noted that Eq. (17) only considers the fitting accuracy of the waypoints. However, the obtained waypoints are not guaranteed to be trackable. Furthermore, the numerical values of the clothoidal coefficients vary around zero $( \mathrm { e } . \mathrm { g } . , \mathrm { } c _ { 3 } )$ , which can easily affect the shape of the curve. Therefore, we solve the Eq. (18) with constraints (18a) to consider the fitting errors, angular speed, and curvature rate that ensures the clothoid curve is properly generated and conforms to vehicle dynamics at the current speed.

Further, we can use the obtained clothoid curve to establish the PF for the ESPP through the following formulas, including the lower and upper boundary PFs, $( U _ { E S P P } ^ { l b }$ and $U _ { E S P P } ^ { r b } )$ , and the attractive PF, ${ \cal U } _ { E S P P } ^ { a t t r } ,$ , as follows:

$$
\begin{array}{l} U _ {E S P P} ^ {l b} = \\ A _ {e} \left(1 - e ^ {- b _ {w} s i g n (y - f _ {c r} (x)) \sqrt {\left(\frac {y - b _ {y}}{m _ {y}} - x\right) ^ {2} + (f _ {c r} (x) - y) ^ {2}}}\right) ^ {2} \end{array}\tag{19}
$$

$$
U _ {E S P P} ^ {r b} =
$$

$$
A _ {e} \left(1 - e ^ {b _ {w} s i g n (y - f _ {c l} (x)) \sqrt {\left(\frac {y - b _ {y}}{m _ {y}} - x\right) ^ {2} + (f _ {c l} (x) - y) ^ {2}}}\right) ^ {2}\tag{20}
$$

![](Lin2023Clothoid_figs/6cc879f92044fe879fa8fe4da9b724fe698c6fbe2c37f1e30568649c0d81e56a.jpg)  
Fig. 6. Detailed system architecture of the proposed ESPP method

$$
U _ {E S P P} ^ {a t t r} = \frac {1}{2} \xi D (X _ {d}, Y _ {d}) ^ {2},
$$

where

$$
b _ {y} = f _ {c r} (x) - m _ {y} x, \quad m _ {y} = - \frac {1}{\dot {f} _ {c} (x)},\tag{21}
$$

with $A _ { e }$ is the maximum amplitude of the ESPP’s PF, $( x , y )$ is the position pair of the ego vehicle in vehicle coordinate, $b _ { w }$ denotes the parameter controlling the road PF width [40], $f _ { c } ( x )$ is the optimal curve that is obtained from Eq. (18), $f _ { c r } ( x )$ and $f _ { c l } ( x )$ are the right and left boundaries of the ESPP, respectively, which are acquired by shifting $f _ { c } ( x ) , \xi$ is the influence factor of the attractive PF, ${ \cal U } _ { E S P P } ^ { a t t r } ;$ and $D ( X _ { d } , Y _ { d } )$ denotes the Euclidean distance between the ego vehicle and the temporary target point from the clothoid curve. Note that Eqs. (19) and (20) are used to establish an impenetrable PF that keeps the vehicle tracking around the ESPP trajectory. In addition, we use Eq. (21) to produce the attractive force instead of Eq. (5) when the “blind alley” problem is detected, considering Eq. (21) can generate a more potent force to lead the ego-vehicle to follow the optimized clothoid curve. Finally, we can model the 3D PF of the ESPP and obtain the emergency collision-free path by repeating the process described in Section 3, as shown in Fig. 9. We also present the curve-fitting process using hybrid points in Algorithm 2. Therefore, the ESPP can guide the ego vehicle to conduct emergency collision avoidance and safe stop maneuvers. Overall, the proposed system architecture of the ESPP method is depicted in Fig. 6, which indicates the workflow of the internal modules.

## V. MODEL PREDICTIVE CONTROLLER

In this section, we will comprehensively illustrate the specific MPC for path-tracking tasks, encompassing vehicle dynamics, thorough constraints analysis, detailed optimization function formulation, and effective quadratic programming techniques.

![](Lin2023Clothoid_figs/3c1baef7ac9afcc17c7124865af1b900ae99d080d96be1be119c04fb7ce4482d.jpg)  
Fig. 7. Vehicle lateral dynamics model for path tracking

## A. Vehicle Dynamics Model

One of the advantages of the MPC is that it has a builtin vehicle dynamics model, which can predict the motion states of the vehicle within a given prediction horizon. The four-wheel vehicle dynamics model is usually simplified as a bicycle model by assuming the front (rear) two wheels have the same steering. Another important postulation is that the bicycle model is two-degree-of-freedom (2DOF) and neglects the angular momentum of the vehicle body in roll, yaw, and pitch, as shown in Fig. 7. The vehicle dynamics model can then be mathematically formulated by the following equations [41]:

$$
m V (\dot {\beta} + \dot {\psi}) = F _ {y f} + F _ {y r}
$$

$$
I _ {z} \ddot {\psi} = l _ {f} F _ {y f} - l _ {r} F _ {y r}\tag{22}
$$

(23)

where

$$
\begin{array}{l} \dot {\beta} = \frac {- (C _ {r} + C _ {f})}{m V} \beta + \left(\frac {C _ {r} l _ {r} - C _ {f} l _ {f}}{m V ^ {2}} - 1\right) \dot {\psi} + \frac {C _ {f}}{m V} \delta_ {f}, \\ \ddot {\psi} = \frac {C _ {r} l _ {r} - C _ {f} l _ {f}}{I _ {z}} \beta - \frac {C _ {r} l _ {r} ^ {2} + C _ {f} l _ {f} ^ {2}}{I _ {z} V} \dot {\psi} + \frac {C _ {f} l _ {f}}{I _ {z}} \delta_ {f}, \\ F _ {y f} = C _ {f} \alpha_ {f} = C _ {f} \left(\delta_ {f} - \beta - \frac {l _ {f} \dot {\psi}}{V}\right), \\ F _ {y r} = C _ {r} \alpha_ {r} = C _ {r} \left(- \beta + \frac {l _ {r} \dot {\psi}}{V}\right) \end{array}
$$

with $m$ is the vehicle mass, $\beta$ and $\dot { \boldsymbol { \beta } }$ denote the sideslip angle and the sideslip rate of the vehicle, respectively. $\dot { \psi }$ denotes the yaw rate of the vehicle, $I _ { z }$ is the yaw moment of inertia, $l _ { f }$ and $l _ { r }$ are the front and rear distances from CG (center of gravity) to front and rear tires, respectively. $F _ { y f }$ and $F _ { y r }$ denote the front and rear lateral tire forces, respectively. $C _ { f }$ and $C _ { r }$ represent the cornering stiffness of the front and rear tires respectively. $\alpha _ { f }$ and $\alpha _ { r }$ are the tire slip angles. $\delta _ { f }$ is the front tire steering angle of the vehicle. To facilitate matrix operation in MPC, we should transform the vehicle dynamics model into discrete state-space formulation [42], as shown below:

$$
\boldsymbol {x} (k + 1) = \mathbf {A} \boldsymbol {x} (k) + \mathbf {B} \delta_ {f}
$$

$$
\pmb {y} = \mathbf {C x} (k)\tag{24}
$$

(25)

where

$$
\begin{array}{r l} & {\pmb {x} = \left[ \begin{array}{l l l l} Y & \beta & \psi & \dot {\psi} \end{array} \right] ^ {T},} \\ & {\mathbf {A} = \left[ \begin{array}{c c c c} 1 & T _ {s} V & T _ {s} V & 0 \\ 0 & 1 - T _ {s} \frac {C _ {r} + C _ {f}}{m V} & 0 & T _ {s} \frac {C _ {r} l _ {r} - C _ {f} l _ {f}}{m V ^ {2}} - T _ {s} \\ 0 & 0 & 1 & T _ {s} \\ 0 & T _ {s} \frac {C _ {r} l _ {r} - C _ {f} l _ {f}}{I _ {z}} & 0 & 1 - T _ {s} \frac {C _ {r} l _ {r} ^ {2} + C _ {f} l _ {f} ^ {2}}{I _ {z} V} \end{array} \right]} \\ & {\mathbf {B} = \left[ \begin{array}{l l l l} 0 & T _ {s} \frac {C _ {f}}{m V} & 0 & T _ {s} \frac {C _ {f} l _ {f}}{I _ {z}} \end{array} \right] ^ {T},   \mathbf {C} = \left[ \begin{array}{l l l l} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{array} \right].} \end{array}
$$

Therefore, we use the above discrete state-space model for the motion prediction and optimization.

## B. Optimization Function

The significance of the optimization cost function is to enable the controller to follow the desired trajectory quickly and smoothly, which minimizes the deviation of the system state variables and the control variables. Therefore, three items constitute the complete optimization function: (i) Deviation between state variables and desired trajectory; (ii) Variation of the control variables; (iii) Penalization on the violation of the constraints [43], as illustrated below:

$$
\begin{array}{l} \boldsymbol {J} = \sum_ {\boldsymbol {k} = 1} ^ {N _ {P}} \left\| \boldsymbol {y} (k | t) - \boldsymbol {y} ^ {d} (k | t) \right\| _ {\boldsymbol {Q}} ^ {2} \\ \qquad + \sum_ {k = 0} ^ {N _ {C} - 1} \| \Delta \mathrm{u} (k | t) \| _ {\boldsymbol {R}} ^ {2} + \lambda \epsilon , \end{array}\tag{26}
$$

where $N _ { c }$ denotes the control horizon, Q and R are the weighting matrices, ${ \mathbf { } } y ( k | t )$ means the model outputs at k steps from the current time $t , \boldsymbol { y } ^ { d } ( \boldsymbol { k } | t )$ denotes the desired reference signals at k steps from the current time $t , \Delta \mathrm { u } ( k | t )$ is the increment of the $u ( k | t ) = \delta _ { f }$ . λ is a weight coefficient and ϵ is a slack variable. After that, we need to add conditional constraints to the optimization function to reflect the vehicle’s mechanical structure limitations, road structure, etc. Thus, the following constraints are considered:

$$
\Delta \delta_ {f} ^ {m i n} \leq \Delta \mathrm{u} (k | t) \leq \Delta \delta_ {f} ^ {m a x},\tag{27}
$$

$$
\delta_ {f} ^ {m i n} \leq \Delta \mathrm{u} (k | t) + \mathrm{u} (k - 1 | t) \leq \delta_ {f} ^ {m a x},\tag{28}
$$

$$
\pmb {y} _ {m i n} \leq \pmb {y} (k | t) \leq \pmb {y} _ {m a x},\tag{29}
$$

where $\Delta \delta _ { f } ^ { m i n }$ and $\Delta \delta _ { f } ^ { m a x }$ represent the minimum and maximum incremental front tire steering angles, respectively. $\delta _ { f } ^ { m i n }$ and $\delta _ { f } ^ { m a x }$ are the minimum and maximum front tire steering angles, respectively. $\pmb { y } _ { m i n } = \left[ Y _ { l } \beta _ { m i n } \dot { \psi } _ { m i n } \right] ^ { T }$ and $\pmb { y } _ { m a x } = \left[ Y _ { u } \beta _ { m a x } \dot { \psi } _ { m a x } \right] ^ { \prime }$ denote the minimum and maximum output constraints, respectively, where $\beta _ { m i n }$ <sub>,</sub> <sub>max</sub> is the minimum and maximum sideslip angle and $\psi _ { m i n , m a x }$ is the minimum and maximum yaw rate of the vehicle. It should be noted that the position constraints in ${ \bf { y } } _ { m i n }$ and ${ \pmb y } _ { m a x }$ only consider the regular road structure such as the lower and upper road boundaries. However, referring to the traffic emergency in Fig. 2, the usual road constraints in MPC will prevent the ESPP method from working; because the ESPP method is to open a breach point from the road boundary so that the vehicle can be navigated to stop at a safe region. Therefore, to guarantee the ESPP method still work in traffic emergencies, we make adjustments in the road structure constraints of the MPC controller accordingly. The overall optimization function with constraints is demonstrated as follows:

$$
\min _ {\Delta \mathrm{u}, \epsilon} \boldsymbol {J} (\boldsymbol {x} (k | t), \Delta \mathrm{u} (k | t))\tag{30}
$$

$$
\text { s.t. } \boldsymbol {x} (k + 1) = \mathbf {A} \boldsymbol {x} (k) + \mathbf {B} \delta_ {f}
$$

$$
\pmb {y} = \mathbf {C x} (k)\tag{30a}
$$

$$
\Delta \delta_ {f} ^ {m i n} \leq \Delta \mathrm{u} (k | t) \leq \Delta \delta_ {f} ^ {m a x},\tag{30b}
$$

$$
\delta_ {f} ^ {m i n} \leq \mathrm{u} (k | t) \leq \delta_ {f} ^ {m a x},\tag{30c}
$$

$$
\mathrm{u} (k | t) = \mathrm{u} (k - 1 | t) + \Delta \mathrm{u} (k | t)\tag{30d}
$$

$$
k = t, \dots , t + N _ {p} - 1,\tag{30e}
$$

$$
\left\{ \begin{array}{l l} \boldsymbol {y} _ {m i n} \leq \boldsymbol {y} (k | t) \leq \boldsymbol {y} _ {m a x}, & D _ {E 2 R} > D _ {b r a k e} \\ \boldsymbol {y} _ {m i n} ^ {e m e r} \leq \boldsymbol {y} (k | t) \leq \boldsymbol {y} _ {m a x}, & D _ {E 2 R} \leq D _ {b r a k e} \end{array} \right.,\tag{30f}
$$

where

$$
\pmb {y} _ {m i n} ^ {e m e r} = \left[ \begin{array}{c c c} Y _ {e s l} & \beta_ {m i n} & \dot {\psi} _ {m i n} \end{array} \right] ^ {T}
$$

Note that constraint (30f) is determined by the emergency triggering estimation introduced in Sec. IV-B. Furthermore, we can transform Eq. 30 into the standard quadratic programming (QP) form and then choose the preferred QP solver to reduce time consumption [44].

## VI. SIMULATION RESULTS

This section introduces the initial environmental setup and detailed simulation results. We conducted a comprehensive co-simulation study using MATLAB/Simulink and CarSim simulator to verify the proposed ESPP-based APF method. To compare the effectiveness of the proposed method, we computed four types of path planners as follows: (i) conventional PF with constant speed (denoted as CPF with CS) [22]; (ii) adaptive PF with full braking maneuver (denoted as APF with FB) [19]; (iii) adaptive PF without the lower road PF when sensing the emergency (denoted as APF without LR); and (iv) ESPP-based adaptive PF (denoted as ESPP-based APF). The overall simulation was conducted on a laboratory laptop with Intel(R) Core(TM) i9-10980HK CPU@2.40GHz and RAM 32GB.

## A. Environment Settings

To simulate the high-speed scene, we initialized the longitudinal speed of the adjacent obstacle at 115.2 km/h, and the longitudinal speed of the ego vehicle was initially set at 108 km/h. The adjacent obstacle is suddenly steered without a pre-warning when it is one body position ahead of the ego vehicle to simulate an extreme emergency scene. For longitudinal control, we assume that the ego vehicle conducts a full brake with a maximum deceleration after the reaction time. Therefore, we directly apply the anti-lock brake system (ABS) controller in the CarSim Simulator when the “blind alley” problem is detected. In addition, we applied five different vehicle mechanical models with 27 degrees of freedom (DOF) [45] provided in CarSim to simulate different vehicle dynamics, including Sedan, full-size SUV, large Van, full-size pickup, and cargo trucks. The 3D model of the ESPP is shown in Fig. 9, where we can observe that the ESPP-based APF can extend an emergent PF from the road PF for emergency navigation. The emergent PF restricts the ego vehicle from driving within the planned route and achieves a safe stop. The parameter settings of ESPP-based APF are described in Table. I. It is worth noting that $A _ { o b s }$ should be set to an immense value, which ensures the obstacle PF is not traversable. Besides, the numerical value of $A _ { l a n e }$ should be small because the vehicle needs to violate the lane PF when a lane-change decision has been made. The numerical values of $\omega _ { m a x }$ and $R _ { m i n }$ are determined based on the selected car model in the CarSim simulator; for example, the D-class sedan is chosen in this study. In addition, $l _ { w } , l _ { f }$ and $l _ { r }$ can also be available from the CarSim simulator. The parameter settings of the MPC controller are denoted in Table. II.

TABLE I  
PARAMETERS OF ESPP-BASED PF

<table><tr><td>Parm.</td><td>Val.</td><td>Parm.</td><td>Val.</td></tr><tr><td> $A_{lane}$ </td><td>20</td><td> $A_{obs}$ </td><td>150</td></tr><tr><td> $l_w$ </td><td>1.6 m</td><td>L</td><td>0.3</td></tr><tr><td> $\zeta$ </td><td>1</td><td> $Y_c$ </td><td>4</td></tr><tr><td> $v$ </td><td>0.75</td><td> $\xi$ </td><td>0.2</td></tr><tr><td> $\eta$ </td><td>3</td><td> $e_y^{min,max}$ </td><td>± 0.7 m</td></tr><tr><td> $l_f$ </td><td>1.232 m</td><td> $e_\psi^{min,max}$ </td><td>± 0.05 rad</td></tr><tr><td> $Y_{u,l}$ </td><td>(8,0)</td><td> $\omega_{max}$ </td><td>4.9</td></tr><tr><td> $l_r$ </td><td>1.468 m</td><td> $R_{min}$ </td><td>6.12 m</td></tr></table>

TABLE II  
PARAMETERS OF MPC CONTROLLER

<table><tr><td>Parm.</td><td>Val.</td><td>Parm.</td><td>Val.</td></tr><tr><td> $N_p$ </td><td>20</td><td> $N_c$ </td><td>5</td></tr><tr><td> $T_s$ </td><td>10 [ms]</td><td> $u_{max}$ </td><td>0.2 [rad]</td></tr><tr><td> $\Delta u_{max}$ </td><td>0.015 [rad]</td><td> $\psi_{max}$ </td><td>0.4 [rad]</td></tr><tr><td>V</td><td>108 [km/h]</td><td>λ</td><td>0.15</td></tr><tr><td>Q</td><td> $\begin{bmatrix} 0.01 & 0 \\ 0 & 0.001 \end{bmatrix}$ </td><td>R</td><td>0.1</td></tr></table>

## B. Simulation Results

In Table. III, we can observe the overall performance of the four planners under different high speeds. Although both the CPF with CS and APF with FB can produce a smoother path, their response times are relatively shorter than the APF without LR and ESPP-based APF due to the “blind alley” problem. Consequently, they fail to accomplish collision avoidance as well as the safe stop for all scenarios. On the other hand, the APF without LR can achieve collision avoidance and safe stop for the scenarios of 20 m/s, 25 m/s, and 30 m/s, but its average curvature is larger than other planners, which means the smoothness of the path and the ride comfort performs worse. Besides, we found the response time of the APF without LR is similar to that of the ESPP-based APF but slightly larger because the planner will stop its response when the vehicle is stopped, which implicitly indicates the APF without LR takes longer to complete the safe stop. In the scenario of 35 m/s, the APF without LR fails to accomplish collision avoidance and has the shortest response time than other planners because it quickly hits the boundary of the emergency stopping lane due to the entire loss of control. On the opposite, the ESPPbased APF can finish all the tasks and produce a smoother path. Next, we will compare and analyze more detailed data. The trajectories of the ego vehicle obtained by applying the 4 different path planners are shown in Fig. 8. We can observe that the trajectory of the CPF with CS (denoted by the red dash-dotted line) experiences a side collision with the obstacle (blue vehicle), while that of the APF with FB (denoted by the cyan dashed line) ends up with a rear-end collision with the obstacle. On the other hand, the trajectory of the APF without LR (denoted by the magenta dotted line) successfully avoids the obstacle; however, experiences an apparent tortuous part from 200–160 m. The trajectory of the ESPP-based APF also avoids the obstacle while ensuring a smoother curvature in the stopping maneuver. In addition, the total length of the ESPPbased APF trajectory was shorter than that of the APF without LR, resulting in a faster-stopping maneuver.

As depicted in Fig. 10, the front wheel steering angles of the CPF with CS and the APF with FB end up at the time 3.96 s and 4.2 s, respectively, owing to the collision. When the front wheel steering angle of the APF without LR reaches the maximum at 0.13 rad and the minimum at -0.12 rad, during the emergency collision avoidance from 2.67–6.18 s. On the contrary, the front wheel steering angle of the ESPP-based APF varies between 0.03 rad and -0.02 rad, which is smaller than that of the APF without LR. Correspondingly, the heading angle of the APF without LR reaches -0.28 and 0.22 rad, which are more extensive than that of the ESPP-based APF (with the minimum value at -0.18 rad), as depicted in Fig. 11. The longitudinal speeds of the four wheels of the ego vehicle are shown in Fig. 12 and 13. We observed that the four wheels of the APF without LR exhibited severe oscillations from 3– 5.2 s, which is caused by the excessive wheel slip, requiring a longer time to complete the entire braking maneuver. In contrast, the four wheels of the ESPP-based APF exhibited a marginal vibration from 3.2–3.8 [s] that enabled the ego vehicle to complete the braking procedure earlier than the APF without LR. The lateral accelerations of the ego vehicle are shown in Fig. 14; the APF without LR exhibited a larger lateral acceleration (up to $0 . 9 \mathrm { m } / \mathrm { s } ^ { 2 } )$ than the ESPP-based APF (up to $- 0 . 4 8 ~ \mathrm { m / s ^ { 2 } } )$ during the emergency collision avoidance. Fig. 15 shows the variation of the stop point that is calculated from Algorithm 1. The stop point’s X- and Y-axes can jump first at 3.56 s when the emergency situation occurs, and the X-axis varies two times at 4.33 and 6.28 s, respectively, because of the preset constraint conditions. The coordinates of the stop point are finally initialized to (0, 0) when the ego vehicle stops. In addition, Figs. 10, 11, and 14 show smoother and smaller responses and control inputs of the system with the proposed ESPP method compared to other methods.

From Fig. 16 to Fig. 19, the rotational dynamics can be observed, including the rolling resist moment (RRM) of four tires and the roll rate (RR) of four wheels. In Fig. 16, we can see that the RRMs of Tire L1 and Tire R1 are over 100 N-m in APF without LR-based path planner, while that of ESPP-based path planner maintains between 53 N-m to 102 N-m from 3.2 s to 7.2 s, as depicted in Fig. 17. Besides, the RRM of Tire L1 of the APF without LR-based path planner drops dramatically from 104.3 N-m to 13.21 N-m at $T = 3 . 8 \ \mathrm { s } ,$ possibly due to the tire slip. In addition, the RRMs of the rear tires from both planners vary around 0 N-m. On the other hand, the roll rates of four wheels from the APF without LR-based path planner have obvious oscillations during the braking period (from 3.2 s to 6.7 s) that reaches 10.1 deg/s at $T = 4 . 5$ s and -11.6 deg/s at $T = 5 . 8 \ \mathrm { s } ,$ as shown in Fig. 18. Conversely, as stated in Fig. 19, the roll rates of four wheels from the ESPP-based path planner vary under ±3.8 deg/s with a shorter oscillation period.

TABLE III PERFORMANCE EVALUATIONS

<table><tr><td rowspan="2">Planners</td><td colspan="4">20 m/s</td><td colspan="4">25 m/s</td><td colspan="4">30 m/s</td><td colspan="4">35 m/s</td></tr><tr><td>AC (1/m)</td><td>RT (s)</td><td>CA</td><td>SS</td><td>AC (1/m)</td><td>RT (s)</td><td>CA</td><td>SS</td><td>AC (1/m)</td><td>RT (s)</td><td>CA</td><td>SS</td><td>AC (1/m)</td><td>RT (s)</td><td>CA</td><td>SS</td></tr><tr><td>CPF w CS</td><td>5.2e-3</td><td>5.73</td><td>✘</td><td>✘</td><td>6.3e-4</td><td>4.07</td><td>✘</td><td>✘</td><td>2.5e-3</td><td>4.01</td><td>✘</td><td>✘</td><td>1.2e-3</td><td>4.05</td><td>✘</td><td>✘</td></tr><tr><td>APF w FB</td><td>2.6e-3</td><td>6.18</td><td>✘</td><td>✘</td><td>1.4e-3</td><td>5.55</td><td>✘</td><td>✘</td><td>1.1e-3</td><td>4.21</td><td>✘</td><td>✘</td><td>7.2e-4</td><td>4.11</td><td>✘</td><td>✘</td></tr><tr><td>APF w/o LR</td><td>4.3e-2</td><td>6.95</td><td>✓</td><td>✓</td><td>3.0e-1</td><td>6.64</td><td>✓</td><td>✓</td><td>3.2e-1</td><td>7.54</td><td>✓</td><td>✓</td><td>3.7e-3</td><td>3.85</td><td>✘</td><td>✘</td></tr><tr><td>ESPP-APF</td><td>3.7e-3</td><td>6.87</td><td>✓</td><td>✓</td><td>4.4e-3</td><td>6.49</td><td>✓</td><td>✓</td><td>1.3e-3</td><td>7.25</td><td>✓</td><td>✓</td><td>2.8e-3</td><td>8.11</td><td>✓</td><td>✓</td></tr></table>

AC: Average Curvature RT: Response Time CA: Collision Avoidance SS: Safe Stop

![](Lin2023Clothoid_figs/dac24125db4dee767bd9825d1cbbc652ecb35cf6faf8baf474d2a629a1cff9e4.jpg)  
Fig. 8. Vehicle trajectories of different path planners: the gray area represents the typical freeway, and the orange area denotes the emergency stopping lane or open space.

![](Lin2023Clothoid_figs/44aaf5edd6b17f41e00368279b474274a2b4b14a4c30828c457717c07a8c333b.jpg)  
Fig. 9. 3D potential field modeling of the ESPP: Opening a breach for the ego-vehicle to avoid collision

The computational time is depicted in Fig. 20, we can observe that the initial computational time of ESPP-based APF is higher than other planners because it has more parameters to be initialized. From $T = 3 . 2 \mathrm { ~ s ~ t o ~ } T = 4 . 5 \mathrm { ~ s } ,$ we can see that the computational time of ESPP-based APF is also increasing more rapidly than other planners due to the activation of the ESPP. In addition, more peaks exist in the green solid line than in other lines after $T \ = \ 3 \ \mathrm { ~ s ~ }$ because the emergency triggering estimation detects the “blind alley” problem and activates the ESPP to reach a safe stop, involving solving several constrained optimizations at those peaks. Although the average computational time of the proposed method is higher than other methods, the overall performance is still under 0.04 s, which has conformed to the real-time requirement (within 100 ms) in autonomous driving [46].

## VII. CONCLUSIONS AND DISCUSSIONS

In this study, we proposed an ESPP-based APF combined with a clothoid curve to overcome an extreme emergency situation in which the obstacle steers recklessly without a pre-warning. We compared our proposed method with three other path planners in a co-simulation study using MAT-LAB/Simulink and CarSim simulator to verify its performance. The simulation results revealed that the proposed method demonstrates effective emergency collision avoidance capabilities, enabling the vehicle to come to a safer stop compared to conventional methods. Moreover, the proposed approach exhibits the advantage of generating a smoother trajectory, contributing to improved ride comfort for passengers. Despite its longer response time when compared to other methods, even in high-speed scenarios, the proposed method still exhibits reliable collision avoidance performance. Additionally, the proposed method addresses the issue of wheel slip, a phenomenon that typically occurs during sudden braking, and effectively mitigates its effects. By doing so, it ensures a more stable and controlled deceleration, enhancing overall safety during critical braking maneuvers. Furthermore, the benefits of the proposed method extend beyond safety considerations, as it also generates a more comfortable lateral acceleration. This improvement in lateral dynamics contributes to a smoother and more pleasant ride experience for vehicle occupants. Taken together, the simulation results demonstrate the effectiveness and versatility of the proposed method, making it a promising solution for enhancing both safety and ride quality in emergency scenarios.

![](Lin2023Clothoid_figs/8598eeb0e28b8d25b885997ccde80d2ec94c15577a4e746a16f241ef76580ae3.jpg)  
Fig. 10. Front wheel steering angles of the ego vehicle.

![](Lin2023Clothoid_figs/b4ee95844e9450f5daee70eaad0e5de51b25e8003a59dc04df87c36ce85a407b.jpg)  
Fig. 12. (Linear) Longitudinal speeds of four wheels of APF without LR: L1 is the left front wheel; R1 is the right front wheel; L2 is the left rear wheel; R2 is the right rear wheel

![](Lin2023Clothoid_figs/57e4be2e85c587bcdf96b59f30626ebff7875c7a86f829e52dfc07891d171f14.jpg)  
Fig. 14. Lateral accelerations of the ego vehicle.

In this study, we have an underlying assumption that the ego vehicle possesses complete knowledge of obstacle information. However, this assumption could result in failures when encountering occlusion problems, where certain obstacles might not be fully visible or detectable. Additionally, we need to further verify the robustness of the proposed algorithm against parameter changes to avoid potential failures under varying conditions. Regarding the current limitations, our investigation has been limited to simulations on straight roads, which poses a foreseeable restriction on the applicability of the proposed approach to other road types, such as curved roads and intersections. Expanding our research to include different road scenarios would provide a more comprehensive evaluation of the algorithm’s effectiveness and practicality. Furthermore, we employed a 2-degree-of-freedom (2-DOF) vehicle model in the MPC controller, which may require enhancements to represent real-world driving conditions accurately. For instance, paying attention to the road bank angle might lead to suboptimal control decisions. To address this, we intend to explore a higher degree of freedom vehicle dynamics model for the tracking controller in future work. However, a higher dimensional vehicle model will increase computational costs that should be considered based on specific application scenarios and performance requirements. Adopting a more sophisticated vehicle model could yield different outcomes when integrating it with the proposed ESPP method.

![](Lin2023Clothoid_figs/529395f95a97662c2424defa4f3f277c5ab7d19c169247ce2b64a079f13088dc.jpg)  
Fig. 11. Heading angles of the ego vehicle.

![](Lin2023Clothoid_figs/4be5dd0c8b3c76395854a8faa941d6cd5ad4a9826025dc6b62b7c2418b492361.jpg)  
Fig. 13. (Linear) Longitudinal speeds of four wheels of ESPP-based APF: L1 is the left front wheel; R1 is the right front wheel; L2 is the left rear wheel; R2 is the right rear wheel

![](Lin2023Clothoid_figs/5615d178abfacd4a7f4af3606b291372fddd6dfbeff0c658cfae769d45441521.jpg)  
Fig. 15. Longitudinal and lateral coordinates of the stop point (SP).

## ACKNOWLEDGMENT

We extend our heartfelt gratitude to Dr. Maxime Clement from Tier IV Inc. for his invaluable insights, guidance, and thought-provoking suggestions throughout the course of this research. These research results were partly sponsored by the China Scholarship Council (CSC) program (No.202208050036) and the Japan Society for the Promotion of Science (JSPS) Research Fellowship for Young Scientists (DC2) program (grant number: 23KJ0391).

![](Lin2023Clothoid_figs/75d431535260e3c3d6c08a850d2f3bea7b78351163cd23b068f0e25185460193.jpg)  
Fig. 16. Rolling resist moment of four tires from the APF without LR-based planner: L1 is the left front tire; R1 is the right front tire; L2 is the left rear tire; R2 is the right rear tire

![](Lin2023Clothoid_figs/96ffbafea34f4a9501ebff7e1a242bbf395dc2407fbf8f51864e323179b6aa5c.jpg)  
Fig. 18. Roll rate of four wheels from the APF without LR-based planner

![](Lin2023Clothoid_figs/fd4d17b873b34337358b20f8cbc343c430c83bda705442cfea4c16b6504eba43.jpg)  
Fig. 20. Computational time of the planners.

## REFERENCES

[1] W. H. Organization, “Road traffic injuries,” WHO.int, Accessed: Jan. 2022. [Online.] Available: https://www.who.int/news-room/factsheets/detail/road-traffic-injuries.

[2] S. C. Curtin, H. Hedegaard, and P. Martinez, “Death rates for motorvehicle-traffic injuries, suicide, and homicide among adolescents and young adults aged 15-24 years-united states, 1999-2019,” Morb. Mortal. Wkly. Rep., vol. 70, no. 5, pp. 184–184, Feb. 2021.

[3] D. of Motor Vehicles, “Autonomous vehicle collision reports,” DMV.ca.gov, Accessed: Aug. 2022. [Online.] Available: https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomousvehicles/autonomous-vehicle-collision-reports/.

[4] D. Gonzalez, J. P´ erez, V. Milan´ es, and F. Nashashibi, “A review of´ motion planning techniques for automated vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 17, no. 4, pp. 1135–1145, Apr. 2016.

[5] B. Li, H. Du, and W. Li, “A potential field approach-based trajectory control for autonomous electric vehicles with in-wheel motors,” IEEE Trans. Intell. Transp. Syst., vol. 18, no. 8, pp. 2044–2055, Aug. 2017.

[6] L. Claussmann, M. Revilloud, D. Gruyer, and S. Glaser, “A review of motion planning for highway autonomous driving,” IEEE Trans. Intell. Transp. Syst., vol. 21, no. 5, pp. 1826–1848, May 2020.

[7] O. Khatib, “Real-time obstacle avoidance for manipulators and mobile robots,” in Proc. IEEE Int. Conf. Robot. Autom., vol. 2, Mar. 1985, pp. 500–505.

![](Lin2023Clothoid_figs/99814557bd27cccd996d9e5c210fe375fc94cd0ab948e91cff4bf8a0683afa6f.jpg)  
Fig. 17. Rolling resist moment of four tires from the ESPP-based planner: L1 is the left front tire; R1 is the right front tire; L2 is the left rear tire; R2 is the right rear tire

![](Lin2023Clothoid_figs/6858b8e987649323eb4d85cd86112f3b9591c4c5369bed3fe1bd13d98bc78bc0.jpg)  
Fig. 19. Roll rate of four wheels from the ESPP-based planner

[8] A. K. Pamosoaji and K.-S. Hong, “A path-planning algorithm using vector potential functions in triangular regions,” IEEE Trans. Syst. Man Cybern., vol. 43, no. 4, pp. 832–842, Jul. 2013.

[9] C. Katrakazas, M. Quddus, W.-H. Chen, and L. Deka, “Real-time motion planning methods for autonomous on-road driving: State-of-the-art and future research directions,” Transp. Res. Part C Emerg. Technol., vol. 60, pp. 416–442, Nov. 2015.

[10] M. Samuel, M. Hussein, and M. Binti, “A review of some pure-pursuit based path tracking techniques for control of autonomous vehicle,” Int. J. Comput. Appl., vol. 135, no. 1, pp. 35–38, Feb. 2016.

[11] J. Ji, A. Khajepour, W. W. Melek, and Y. Huang, “Path planning and tracking for vehicle collision avoidance based on model predictive control with multiconstraints,” IEEE Trans. Veh. Technol., vol. 66, no. 2, pp. 952–964, Feb. 2017.

[12] Y. Rasekhipour, A. Khajepour, S.-K. Chen, and B. Litkouhi, “A potential field-based model predictive path-planning controller for autonomous road vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 18, no. 5, pp. 1255–1267, May 2017.

[13] Y. Li, K. Li, Y. Zheng, B. Morys, S. Pan, and J. Wang, “Threat assessment techniques in intelligent vehicles: A comparative survey,” IEEE Intell. Transp. Syst. Mag., vol. 13, no. 4, pp. 71–91, 2021.

[14] J. Wang, J. Wu, and Y. Li, “The driving safety field based on Driver– Vehicle–Road interactions,” IEEE Trans. Intell. Transp. Syst., vol. 16, no. 4, pp. 2203–2214, Aug. 2015.

[15] H. Wang, Y. Huang, A. Khajepour, Y. Zhang, Y. Rasekhipour, and D. Cao, “Crash mitigation in motion planning for autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 20, no. 9, pp. 3313–3323, Sep. 2019.

[16] H. Wang, Y. Huang, A. Khajepour, and others, “Ethical decision-making platform in autonomous vehicles with lexicographic optimization based model predictive controller,” IEEE Trans. Veh. Technol., vol. 69, no. 8, pp. 8164–8175, May 2020.

[17] P. Lin, W. Y. Choi, and C. C. Chung, “Local path planning using artificial potential field for waypoint tracking with collision avoidance,” Proc. IEEE 23rd Int. Conf. Intell. Transp. Syst., pp. 1–7, Dec. 2020.

[18] P. Lin, J. H. Yang, Y. S. Quan, and C. C. Chung, “Potential field-based path planning for emergency collision avoidance with a clothoid curve in waypoint tracking,” Asian J. Control, vol. 24, no. 3, pp. 1074–1087, May 2022.

[19] B. Lu, G. Li, H. Yu, H. Wang, J. Guo, D. Cao, and H. He, “Adaptive potential field-based path planning for complex autonomous driving scenarios,” IEEE Access, vol. 8, pp. 225 294–225 305, Dec. 2020.

[20] J. Wang, Y. Yan, K. Zhang, Y. Chen, M. Cao, and G. Yin, “Path planning on large curvature roads using driver-vehicle-road system based on the kinematic vehicle model,” IEEE Trans. Veh. Technol., vol. 71, no. 1, pp. 311–325, Nov. 2021.

[21] H. Li, W. Liu, C. Yang, W. Wang, T. Qie, and C. Xiang, “An Optimization-Based path planning approach for autonomous vehicles using the DynEFWA-Artificial potential field,” IEEE Trans. Intell. Veh., vol. 7, no. 2, pp. 263–272, Jun. 2022.

[22] P. Lin and M. Tsukada, “Model predictive path-planning controller with potential function for emergency collision avoidance on highway driving,” IEEE Rob. Autom. Lett., vol. 7, no. 2, pp. 4662–4669, Apr. 2022.

[23] P. Lin, Y. S. Quan, J. H. Yang, C. C. Chung, and M. Tsukada, “Safety Tunnel-Based model predictive Path-Planning controller with potential functions for emergency navigation,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 4, pp. 3974–3985, Dec. 2022.

[24] S. Xie, J. Hu, P. Bhowmick, Z. Ding, and F. Arvin, “Distributed motion planning for safe autonomous vehicle overtaking via artificial potential field,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 11, pp. 21 531– 21 547, Nov. 2022.

[25] P. Wu, F. Gao, and K. Li, “Humanlike decision and motion planning for expressway lane changing based on artificial potential field,” IEEE Access, vol. 10, no. 3, pp. 4359–4373, Jan. 2022.

[26] Y. Ji, L. Ni, C. Zhao, C. Lei, Y. Du, and W. Wang, “TriPField: A 3D potential field model and its applications to local path planning of autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 3, pp. 3541–3554, Mar. 2023.

[27] D. Chu, H. Li, C. Zhao, and T. Zhou, “Trajectory tracking of autonomous vehicle based on model predictive control with PID feedback,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 2, pp. 1–12, 2022.

[28] X. Shang and A. Eskandarian, “Emergency collision avoidance and mitigation using model predictive control and artificial potential function,” IEEE Trans. Intell. Veh., vol. 8, no. 5, pp. 3458–3472, May 2023.

[29] G. Du, Y. Zou, X. Zhang, Z. Li, and Q. Liu, “Hierarchical motion planning and tracking for autonomous vehicles using global heuristic based potential field and reinforcement learning based predictive control,” IEEE Trans. Intell. Transp. Syst., Apr. 2023, early access. doi: 10.1109/TITS.2023.3266195.

[30] M. T. Wolf and J. W. Burdick, “Artificial potential functions for highway driving with collision avoidance,” in Proc. IEEE Int. Conf. Robot. Autom., May 2008, pp. 3731–3736.

[31] M. Werling, J. Ziegler, S. Kammel, and S. Thrun, “Optimal trajectory generation for dynamic street scenarios in a frenet frame,” in Proc. IEEE Int. Conf. Robot. Autom., Jul. 2010, pp. 987–993.

[32] D. Parker, J. T. Reason, A. S. R. Manstead, and S. G. Stradling, “Driving errors, driving violations and accident involvement,” Ergonomics, vol. 38, no. 5, pp. 1036–1048, May 1995.

[33] Y. Koren and J. Borenstein, “Potential field methods and their inherent limitations for mobile robot navigation,” in Proc. IEEE Int. Conf. Robot. Autom., vol. 2, Apr. 1991, pp. 1398–1404.

[34] D. Lyubenov, “Research of the stopping distance for different road conditions,” Transp. Probl., vol. T. 6, z. 4, no. 4, pp. 119–126, 2011.

[35] H. Cheng, Autonomous Intelligent Vehicles: Theory, Algorithms, and Implementation. Springer Science & Business Media, Nov. 2011, pp. 23–29.

[36] U. Ozguner, T. Acarman, and K. A. Redmill, Autonomous Ground Vehicles. Artech House, Feb. 2011, pp. 13–56.

[37] S. J. Jeon, C. M. Kang, S.-H. Lee, and C. C. Chung, “Gps waypoint fitting and tracking using model predictive control,” in Proc. IEEE Int. Veh. Sym., Jun. 2015, pp. 298–303.

[38] C. M. Kang, S.-H. Lee, and C. C. Chung, “On-road path generation and control for waypoints tracking,” IEEE Intell. Transp. Syst. Mag., vol. 9, no. 3, pp. 36–45, Jul. 2017.

[39] A. Scheuer and T. Fraichard, “Continuous-curvature path planning for car-like vehicles,” in Proc. IEEE Int. Conf. Intell. Robots Syst., vol. 2, Sep. 1997, pp. 997–1003.

[40] E. Snapper, “Model-based path planning and control for autonomous vehicles using artificial potential fields,” M.S. Thesis, Dept. Mech. Eng., TU Delft, Delft, Netherlands, 2018, [Online]. Available: https://repository.tudelft.nl/islandora/object/uuid:453a26ea-8556-4927- 8d9f-2058f7dcda15.

[41] R. Rajamani, Vehicle Dynamics and Control. Springer Science & Business Media, Dec. 2011, pp. 15–49.

[42] A. Eckert, B. Hartmann, M. Sevenich, and P. Rieth, “Emergency steer & brake assist: a systematic approach for system integration of two complementary driver assistance systems,” in Proc. Int. Tech. Conf. Enhanced Saf. Veh., 2011, pp. 13–16.

[43] P. Falcone, F. Borrelli, J. Asgari, H. E. Tseng, and D. Hrovat, “Predictive active steering control for autonomous vehicle systems,” IEEE Trans. Control Syst. Technol., vol. 15, no. 3, pp. 566–580, Apr. 2007.

[44] Y. Gao, “Model predictive control for autonomous and semiautonomous vehicles,” Ph.D. Dissertation, Univ. California, Berkeley, CA, USA, 2014, [Online]. Available: https://escholarship.org/uc/item/8xd0b56h.

[45] Y. Yin, H. Wen, L. Sun, and W. Hou, “The influence of road geometry on vehicle rollover and skidding,” Int. J. Environ. Res. Public Health, vol. 17, no. 5, pp. 1648–1664, Mar. 2020.

[46] J. Ren, Autonomous driving algorithms and Its IC Design. Springer Verlag, Singapore, Aug. 2023, pp. 1–23.